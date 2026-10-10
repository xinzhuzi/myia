"""Default SQLite backend for the pluggable Store interface.

Single-file database (default ``myssia.db``, path configurable), WAL journal
mode for the single-process asyncio workload, ``busy_timeout`` so concurrent
writers from separate connections wait instead of failing with
"database is locked". A PostgreSQL backend plugs in behind
:class:`myssia.store.base.Store` in v0.2+ — no Redis/PG dependency in v0.1.

Schema versioning (v0.2 storage hardening): ``store_meta['schema_version']``
stamps the layout; opening a database runs idempotent migrations forward and
refuses — with :class:`myssia.store.errors.StoreSchemaError` — a file that is
not a usable SQLite database or was written by a *newer* MYIA. Versions:

- 1 — v0.1: items / dedup_registry / change_baseline / engine_hints / runs.
- 2 — v0.2 storage hardening: ``runs.steps`` JSON progress column
  (断点续跑) + ``store_meta`` key-value table (schema version, vacuum stamp).
- 3 — v0.2 LLM enrich (PRD 10-01-v02-enrich-llm): ``enrich_cache`` table
  (per-URL score cache, keyed by url+model+scores-fingerprint) — additive,
  legacy databases migrate without touching existing rows.
- 4 — v0.3 feedback loop (PRD 10-01-v03-feedback-loop): ``feedback`` table
  (good/bad verdicts on pushed items, associated with ``items`` via
  ``item_id`` + redundant ``dedup_key`` snapshot) and ``feedback_tuning``
  (append-only parameter-adjustment history) — additive, legacy databases
  migrate without touching existing rows.
- 5 — v0.4 trend baseline (PRD 10-01-v04-trend-baseline): ``metric_history``
  table (品类级数值快照:per-(category, metric_key, field) numeric history for
  the 「vs 昨日 / vs 上周」 comparison and keyword mention week-over-week) —
  additive, legacy databases migrate without touching existing rows.
- 7 — alert rules (PRD 10-04-alert-rules): ``alert_rules`` (条件→动作规则,
  桌面 sidecar 全量写回) + ``alert_fired`` (命中历史, ``UNIQUE (rule_id,
  dedup_key)`` 是 at-most-once 占坑门闩) — additive, no seed rows (零惊扰:
  不配规则 = 每 run 一次空表 SELECT 后短路), legacy databases migrate
  without touching existing rows.
- 8 — G9 server-side read state (PRD 10-04-read-state-server):
  ``items.read/starred/later`` 三列(0/1,DEFAULT 0 未读——迁移不猜测读态,
  首切由 store.state.import 搬运 localStorage 快照)+ ``idx_items_dedup_key``
  (置位按 dedup_key 同键多行同置;非 UNIQUE) — additive, legacy databases
  migrate without touching existing rows.

Retention & vacuum: :meth:`SQLiteStore.cleanup_expired` deletes pushed items
after ``retention`` days (anchored at ``pushed_at``), never-pushed items after
a longer grace window (anchored at ``first_seen`` — undelivered content stays
one extra window for diagnosis), stale per-URL baselines/hints and old run
rows; numeric metric history deliberately outlives items
(``BASELINE_RETENTION_MULTIPLIER × retention``, 基线期长于条目期 — week
over week needs at least two full windows of history);
:meth:`SQLiteStore.maybe_vacuum` gates ``VACUUM`` by calendar cadence
against the ``last_vacuum_at`` stamp.
"""

from __future__ import annotations

import json
import logging
import math
import sqlite3
import threading
from collections.abc import Collection, Mapping, Sequence
from datetime import datetime, timedelta, timezone, tzinfo
from pathlib import Path

from myssia.schema import VACUUM_CADENCES
from myssia.store.errors import StoreSchemaError
from myssia.store.models import (
    ALERT_ACTIONS,
    ALERT_ACTION_STATUSES,
    FEEDBACK_VERDICTS,
    METRIC_WINDOW_DAY,
    METRIC_WINDOWS,
    PUSH_SLOTS,
    RUN_STATUS_RUNNING,
    RUN_STATUSES,
    STEP_STATUSES,
    AlertFired,
    AlertRule,
    ChangeBaseline,
    DedupEntry,
    FeedbackRecord,
    ItemRecord,
    MetricRecord,
    RunRecord,
    TuningRecord,
)

logger = logging.getLogger(__name__)

#: Current layout version; bump + add a migration entry when the DDL changes.
SCHEMA_VERSION = 10

# 同进程并发「首次打开同一数据库」的串行化锁(见 SQLiteStore.__init__)。
_OPEN_LOCK = threading.Lock()

_META_SCHEMA_VERSION = "schema_version"
_META_LAST_VACUUM_AT = "last_vacuum_at"

#: Never-pushed items get this multiple of ``retention`` before cleanup:
#: delivered content has served its purpose, undelivered content stays one
#: extra window for doctor-style diagnosis / manual recovery (清理策略区分
#: 已推送与未推送条目, PRD 10-01-v02-storage-hardening).
UNPUSHED_RETENTION_MULTIPLIER = 2

#: 数值历史快照(metric_history)的保留期倍数:基线期必须长于条目期
#: (PRD 10-01-v04-trend-baseline)——周环比至少要两个完整窗口的历史,日环比
#: 亦然;按 2× retention 保留(默认 90d 条目 → 180d 数值基线)。
BASELINE_RETENTION_MULTIPLIER = 2

#: G9 读态标记词表 → ``items`` 列名(白名单显式映射:列名不可参数化,
#: 防 SQL 注入;协议层 marker 枚举与 store 层 ValueError 同源于此)。
_ITEM_STATE_COLUMNS: dict[str, str] = {"read": "read", "starred": "starred", "later": "later"}


def _item_state_column(marker: str) -> str:
    """Map a G9 marker word to its ``items`` column, refusing anything else.

    列名不可参数化——这是置位/导入路径唯一的注入面,白名单字典显式映射
    收口(未知 marker 走 ValueError,与 save_item 系字段校验同纪律)。
    """
    column = _ITEM_STATE_COLUMNS.get(marker)
    if column is None:
        raise ValueError(
            f"字段校验失败: marker 必须为 {sorted(_ITEM_STATE_COLUMNS)} 之一,得到 {marker!r}"
        )
    return column


_SCHEMA = """
CREATE TABLE IF NOT EXISTS items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    url TEXT NOT NULL,
    dedup_key TEXT NOT NULL,
    source TEXT,
    title TEXT NOT NULL,
    content TEXT,
    content_hash TEXT,
    tags TEXT,          -- JSON array of strings
    category TEXT,
    scores TEXT,        -- JSON object, reserved for v0.1 score backfill
    pushed_at TEXT,     -- ISO-8601 UTC
    push_slot TEXT,     -- 'am' | 'pm'
    first_seen TEXT NOT NULL,
    raw TEXT,           -- optional JSON object
    read INTEGER NOT NULL DEFAULT 0,      -- 1 = 已读(G9 读态迁服务端;0/1,与协议层 bool 互转)
    starred INTEGER NOT NULL DEFAULT 0,   -- 1 = 星标(策展态,同 retention 剪枝,PRD Q4.2)
    later INTEGER NOT NULL DEFAULT 0      -- 1 = 稍后读(同上;随条目剪枝会静默过期,明示)
);
CREATE INDEX IF NOT EXISTS idx_items_url ON items(url);
CREATE INDEX IF NOT EXISTS idx_items_category ON items(category);
-- 非 UNIQUE:dated-key 旋转下同 dedup_key 多行合法(sqlite.py get_item_by_dedup_key
-- docstring),置位按键同置(Q1.3);feedback 表同款先例 idx_feedback_dedup_key。
CREATE INDEX IF NOT EXISTS idx_items_dedup_key ON items(dedup_key);

CREATE TABLE IF NOT EXISTS dedup_registry (
    key TEXT PRIMARY KEY,          -- composite dedup key or bare URL
    first_seen TEXT NOT NULL,
    last_pushed_at TEXT,
    last_push_slot TEXT
);

CREATE TABLE IF NOT EXISTS change_baseline (
    url TEXT PRIMARY KEY,
    etag TEXT,
    last_modified TEXT,
    content_hash TEXT,
    last_changed TEXT
);

CREATE TABLE IF NOT EXISTS engine_hints (
    source_key TEXT PRIMARY KEY,   -- stable per-source id (v0.1: source URL)
    engine TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS runs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    category TEXT NOT NULL,
    started_at TEXT NOT NULL,
    finished_at TEXT,
    status TEXT NOT NULL,          -- running | success | partial | failed
    stats TEXT,                    -- JSON object
    error TEXT,
    steps TEXT,                    -- JSON object: per-step progress (断点续跑)
    log_run_id INTEGER             -- sidecar 会话级 run_id(日志行对齐键;10-07-logs-restart-visibility)
);

CREATE TABLE IF NOT EXISTS store_meta (
    key TEXT PRIMARY KEY,          -- schema_version / last_vacuum_at
    value TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS enrich_cache (
    url TEXT NOT NULL,             -- cached item URL (同 URL 结果缓存)
    model TEXT NOT NULL,           -- scoring model (换模型即失效)
    scores_key TEXT NOT NULL,      -- dimensions + prompt-version fingerprint
    result TEXT NOT NULL,          -- JSON: {"scores": {...}, "score": x}
    created_at TEXT NOT NULL,      -- ISO-8601 UTC
    PRIMARY KEY (url, model, scores_key)
);
CREATE INDEX IF NOT EXISTS idx_enrich_cache_url ON enrich_cache(url);

CREATE TABLE IF NOT EXISTS feedback (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    item_id INTEGER,           -- items.id 关联(条目被 retention 清理后留 NULL 语义由快照兜底)
    dedup_key TEXT NOT NULL,   -- 条目稳定身份(冗余快照,items 清理后统计仍可用)
    verdict TEXT NOT NULL,     -- 'good' | 'bad'
    channel TEXT NOT NULL,     -- 'cli' | 'telegram' | 'feishu'
    title TEXT,                -- 入库时条目标题快照(负反馈词频统计)
    category TEXT,             -- 入库时条目类目快照(负反馈类目统计)
    external_id TEXT,          -- 渠道事件身份(TG update_id/飞书 event_id;CLI 为 NULL)
    created_at TEXT NOT NULL   -- ISO-8601 UTC
);
CREATE INDEX IF NOT EXISTS idx_feedback_dedup_key ON feedback(dedup_key);
CREATE INDEX IF NOT EXISTS idx_feedback_verdict_created ON feedback(verdict, created_at);
-- 注意:(channel, external_id) 幂等唯一索引在 _migrate_v6 里创建 —— 旧库要先
-- ALTER 出 external_id 列,否则 _SCHEMA 直接建索引会 no such column。

CREATE TABLE IF NOT EXISTS feedback_tuning (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    kind TEXT NOT NULL,        -- mute_weight | category_penalty | prompt_note
    payload TEXT NOT NULL,     -- JSON(词/类目/权重/依据计数,自描述)
    created_at TEXT NOT NULL   -- ISO-8601 UTC
);

CREATE TABLE IF NOT EXISTS metric_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    category TEXT NOT NULL,    -- 品类 id
    metric_key TEXT NOT NULL,  -- 条目 dedup_key/url,或品类级约定键 keyword:<词>
    field TEXT NOT NULL,       -- 数值字段名(baseline.fields)或 "mentions"
    value REAL NOT NULL,       -- 数值快照(finite;NaN/inf 拒写)
    recorded_at TEXT NOT NULL  -- ISO-8601 UTC
);
CREATE INDEX IF NOT EXISTS idx_metric_history_lookup
    ON metric_history(category, metric_key, field, recorded_at);

CREATE TABLE IF NOT EXISTS alert_rules (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    enabled INTEGER NOT NULL DEFAULT 1,     -- 0 | 1
    scope TEXT NOT NULL DEFAULT 'global',   -- 'global' | 品类 id(七品类之一)
    when_expr TEXT NOT NULL,                -- 白名单 AST 表达式原文(SQL 保留字 when 故列名带 _expr)
    action TEXT NOT NULL,                   -- 'push' | 'tag'
    action_config TEXT NOT NULL,            -- JSON:push {channel, targets?, template?} / tag {tags: [..]}
    kind TEXT NOT NULL DEFAULT 'item',      -- 'item' | 'cron_stale'(10-05-cron-heartbeat)
    params TEXT,                            -- JSON:cron_stale {threshold_hours} 或 {auto:true};item 恒 NULL
    created_at TEXT NOT NULL,               -- ISO-8601 UTC
    updated_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS alert_fired (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    rule_id INTEGER NOT NULL,               -- 指向 alert_rules.id;规则删除后历史照留(悬挂即历史事实)
    rule_name TEXT NOT NULL,                -- snapshot at fire time:规则删除后 fired 历史仍可读
    item_id INTEGER,                        -- 可空:items 被 retention 剪枝后历史仍可读
    dedup_key TEXT NOT NULL,                -- 去重身份(None 兜底 url,digest.py 同款在引擎侧先兜底)
    title TEXT,                             -- snapshot at fire time(FeedbackRecord 先例)
    category TEXT,                          -- snapshot at fire time
    action TEXT NOT NULL,                   -- 命中时规则的动作快照 'push' | 'tag'
    action_status TEXT NOT NULL DEFAULT 'pending',  -- pending|sent|send_failed|tagged|degraded_no_channel|skipped_dry_run
    created_at TEXT NOT NULL,
    UNIQUE (rule_id, dedup_key)             -- fired 去重 = 唯一约束(grill Q5);at-most-once 门闩(grill Q3)
);
CREATE INDEX IF NOT EXISTS idx_alert_fired_created ON alert_fired(created_at);
"""


def _migrate_v2_add_run_steps(conn: sqlite3.Connection) -> None:
    """v1 → v2: add ``runs.steps`` (断点续跑进度).

    Idempotent: fresh v2 databases already created the column via
    ``_SCHEMA``; legacy v0.1 databases get it here. Rows predate the column
    and keep ``steps = NULL`` (no progress = nothing resumable, still valid).
    """
    columns = {str(row[1]) for row in conn.execute("PRAGMA table_info(runs)").fetchall()}
    if "steps" not in columns:
        conn.execute("ALTER TABLE runs ADD COLUMN steps TEXT")
        logger.info("存储迁移完成: runs 表新增 steps 列(断点续跑)")


def _migrate_v3_add_enrich_cache(conn: sqlite3.Connection) -> None:
    """v2 → v3: add ``enrich_cache`` (LLM 精评缓存表, PRD 10-01-v02-enrich-llm).

    Idempotent and purely additive: fresh v3 databases already have the table
    via ``_SCHEMA``; existing tables and rows are untouched, so a v2 database
    migrates with zero data loss (迁移兼容).
    """
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS enrich_cache (
            url TEXT NOT NULL,
            model TEXT NOT NULL,
            scores_key TEXT NOT NULL,
            result TEXT NOT NULL,
            created_at TEXT NOT NULL,
            PRIMARY KEY (url, model, scores_key)
        )
        """
    )
    conn.execute("CREATE INDEX IF NOT EXISTS idx_enrich_cache_url ON enrich_cache(url)")
    logger.info("存储迁移完成: 新增 enrich_cache 表(LLM 精评缓存)")


def _migrate_v4_add_feedback(conn: sqlite3.Connection) -> None:
    """v3 → v4: add ``feedback`` + ``feedback_tuning`` (反馈闭环, PRD 10-01-v03-feedback-loop).

    Idempotent and purely additive: fresh v4 databases already have both
    tables via ``_SCHEMA``; existing tables and rows are untouched, so a v3
    database migrates with zero data loss (迁移兼容).
    """
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            item_id INTEGER,
            dedup_key TEXT NOT NULL,
            verdict TEXT NOT NULL,
            channel TEXT NOT NULL,
            title TEXT,
            category TEXT,
            created_at TEXT NOT NULL
        )
        """
    )
    conn.execute("CREATE INDEX IF NOT EXISTS idx_feedback_dedup_key ON feedback(dedup_key)")
    conn.execute(
        "CREATE INDEX IF NOT EXISTS idx_feedback_verdict_created ON feedback(verdict, created_at)"
    )
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS feedback_tuning (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            kind TEXT NOT NULL,
            payload TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
        """
    )
    logger.info("存储迁移完成: 新增 feedback / feedback_tuning 表(反馈闭环)")


def _migrate_v5_add_metric_history(conn: sqlite3.Connection) -> None:
    """v4 → v5: add ``metric_history`` (品类级数值快照, PRD 10-01-v04-trend-baseline).

    Idempotent and purely additive: fresh v5 databases already have the table
    via ``_SCHEMA``; existing tables and rows are untouched, so a v4 database
    migrates with zero data loss (迁移兼容).
    """
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS metric_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category TEXT NOT NULL,
            metric_key TEXT NOT NULL,
            field TEXT NOT NULL,
            value REAL NOT NULL,
            recorded_at TEXT NOT NULL
        )
        """
    )
    conn.execute(
        "CREATE INDEX IF NOT EXISTS idx_metric_history_lookup "
        "ON metric_history(category, metric_key, field, recorded_at)"
    )
    logger.info("存储迁移完成: 新增 metric_history 表(趋势基线数值快照)")


def _migrate_v6_add_feedback_external_id(conn: sqlite3.Connection) -> None:
    """v5 → v6: ``feedback.external_id`` + (channel, external_id) 唯一索引.

    幂等去重(PRD 10-01-v03-feedback-loop 护栏:「one angry click must not
    mute a word forever」——一次双击/平台重试/重启重放不得记两条)。纯增量:
    ALTER 前先查列,旧库零数据损失;CLI 行 external_id 为 NULL,不受唯一索引
    约束(SQLite UNIQUE 对 NULL 放行),历史行为不变。
    """
    columns = {
        row[1] for row in conn.execute("PRAGMA table_info(feedback)").fetchall()
    }
    if columns and "external_id" not in columns:
        conn.execute("ALTER TABLE feedback ADD COLUMN external_id TEXT")
    conn.execute(
        "CREATE UNIQUE INDEX IF NOT EXISTS idx_feedback_external_id "
        "ON feedback(channel, external_id)"
    )
    logger.info("存储迁移完成: feedback.external_id 幂等去重列与唯一索引")


def _migrate_v7_add_alerts(conn: sqlite3.Connection) -> None:
    """v6 → v7: add ``alert_rules`` + ``alert_fired`` (告警规则引擎, PRD 10-04-alert-rules).

    Idempotent and purely additive (``_migrate_v4_add_feedback`` 同构先例):
    fresh v7 databases already have both tables via ``_SCHEMA``; existing
    tables and rows are untouched, so a v6 database migrates with zero data
    loss (零数据迁移:两表皆新表,无既有数据搬运)。不 seed——零惊扰默认,
    无规则时空表即合法态(grill Q2)。
    """
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS alert_rules (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            enabled INTEGER NOT NULL DEFAULT 1,
            scope TEXT NOT NULL DEFAULT 'global',
            when_expr TEXT NOT NULL,
            action TEXT NOT NULL,
            action_config TEXT NOT NULL,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        )
        """
    )
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS alert_fired (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            rule_id INTEGER NOT NULL,
            rule_name TEXT NOT NULL,
            item_id INTEGER,
            dedup_key TEXT NOT NULL,
            title TEXT,
            category TEXT,
            action TEXT NOT NULL,
            action_status TEXT NOT NULL DEFAULT 'pending',
            created_at TEXT NOT NULL,
            UNIQUE (rule_id, dedup_key)
        )
        """
    )
    conn.execute("CREATE INDEX IF NOT EXISTS idx_alert_fired_created ON alert_fired(created_at)")
    logger.info("存储迁移完成: 新增 alert_rules / alert_fired 表(告警规则引擎)")


def _migrate_v8_add_item_states(conn: sqlite3.Connection) -> None:
    """v7 → v8: add ``items.read/starred/later`` + ``idx_items_dedup_key`` (G9 读态迁服务端).

    Idempotent: fresh v8 databases already created the columns & index via
    ``_SCHEMA``; legacy v7 databases get them here. Existing rows keep the
    DEFAULT 0 (unread) -- 迁移不猜测读态,首切由 store.state.import 搬运
    localStorage 快照(Q2).dedup_key 索引非 UNIQUE:dated-key 旋转下同键
    多行合法,置位按键同置(Q1.3)。逐列独立 if(PRAGMA 幂等检查,v2 先例):
    三列 ALTER 中断后重开可续,不要求原子批。
    """
    columns = {str(row[1]) for row in conn.execute("PRAGMA table_info(items)").fetchall()}
    if "read" not in columns:
        conn.execute("ALTER TABLE items ADD COLUMN read INTEGER NOT NULL DEFAULT 0")
    if "starred" not in columns:
        conn.execute("ALTER TABLE items ADD COLUMN starred INTEGER NOT NULL DEFAULT 0")
    if "later" not in columns:
        conn.execute("ALTER TABLE items ADD COLUMN later INTEGER NOT NULL DEFAULT 0")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_items_dedup_key ON items(dedup_key)")
    logger.info("存储迁移完成: items 表新增 read/starred/later 三列 + idx_items_dedup_key(G9)")


def _migrate_v9_add_alert_rule_kind(conn: sqlite3.Connection) -> None:
    """v8 → v9: alert_rules 增 ``kind``/``params`` 列(10-05-cron-heartbeat).

    Idempotent and purely additive(``_migrate_v6_add_feedback_external_id``
    同构先例):fresh v9 库经 ``_SCHEMA`` 已带两列;既有行 kind 缺省
    'item'、params NULL——条目规则语义零漂移,心跳规则是纯新增面。
    """
    columns = {row[1] for row in conn.execute("PRAGMA table_info(alert_rules)").fetchall()}
    if columns and "kind" not in columns:
        conn.execute("ALTER TABLE alert_rules ADD COLUMN kind TEXT NOT NULL DEFAULT 'item'")
    if columns and "params" not in columns:
        conn.execute("ALTER TABLE alert_rules ADD COLUMN params TEXT")
    logger.info("存储迁移完成: alert_rules 增 kind/params 列(心跳规则类型)")


def _migrate_v10_add_runs_log_run_id(conn: sqlite3.Connection) -> None:
    """v9 → v10: runs 增 ``log_run_id`` 列(10-07-logs-restart-visibility R1).

    Idempotent and purely additive(``_migrate_v2_add_run_steps`` 同构先例):
    fresh v10 库经 ``_SCHEMA`` 已带该列;旧行保持 NULL——那批跑次的会话号
    已不可考(注册表随 sidecar 进程消亡),历史行如实不带日志对齐键,
    展开侧降级为空,不伪造。
    """
    columns = {str(row[1]) for row in conn.execute("PRAGMA table_info(runs)").fetchall()}
    if columns and "log_run_id" not in columns:
        conn.execute("ALTER TABLE runs ADD COLUMN log_run_id INTEGER")
        logger.info("存储迁移完成: runs 表新增 log_run_id 列(日志行对齐键)")


#: target version → migration (runs with the connection inside the caller's
#: transaction; every migration must be idempotent — fresh databases replay
#: them after ``CREATE TABLE IF NOT EXISTS`` already produced the new shape).
_MIGRATIONS: dict[int, object] = {
    2: _migrate_v2_add_run_steps,
    3: _migrate_v3_add_enrich_cache,
    4: _migrate_v4_add_feedback,
    5: _migrate_v5_add_metric_history,
    6: _migrate_v6_add_feedback_external_id,
    7: _migrate_v7_add_alerts,
    8: _migrate_v8_add_item_states,
    9: _migrate_v9_add_alert_rule_kind,
    10: _migrate_v10_add_runs_log_run_id,
}


def _to_iso(value: datetime | None) -> str | None:
    """Serialize an aware datetime to ISO-8601 UTC (naive input assumed UTC)."""
    if value is None:
        return None
    if value.tzinfo is None:
        value = value.replace(tzinfo=timezone.utc)
    return value.astimezone(timezone.utc).isoformat()


def _from_iso(raw: str | None) -> datetime | None:
    """Parse an ISO-8601 timestamp back to an aware datetime (UTC fallback)."""
    if raw is None:
        return None
    parsed = datetime.fromisoformat(raw)
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed


def _json_dumps(value: object) -> str | None:
    return None if value is None else json.dumps(value, ensure_ascii=False)


def _json_loads(raw: str | None) -> object | None:
    return None if not raw else json.loads(raw)


def _cadence_elapsed(cadence: str, last: datetime, now: datetime) -> bool:
    """Calendar-based cadence check (UTC): did ``cadence`` elapse since ``last``?

    daily = a later date, weekly = a later ISO week, monthly = a later
    (year, month) — calendar semantics without extra dependencies.
    """
    if cadence == "daily":
        return last.date() != now.date()
    if cadence == "weekly":
        return last.isocalendar()[:2] != now.isocalendar()[:2]
    if cadence == "monthly":
        return (last.year, last.month) != (now.year, now.month)
    raise ValueError(f"字段校验失败: vacuum 周期必须是 {sorted(VACUUM_CADENCES)} 之一,得到 {cadence!r}")


def _row_to_item(row: sqlite3.Row) -> ItemRecord:
    return ItemRecord(
        id=int(row["id"]),
        url=row["url"],
        dedup_key=row["dedup_key"],
        source=row["source"],
        title=row["title"],
        content=row["content"],
        content_hash=row["content_hash"],
        tags=_json_loads(row["tags"]) or [],
        category=row["category"],
        scores=_json_loads(row["scores"]),
        pushed_at=_from_iso(row["pushed_at"]),
        push_slot=row["push_slot"],
        first_seen=_from_iso(row["first_seen"]),
        raw=_json_loads(row["raw"]),
        read=bool(row["read"]),
        starred=bool(row["starred"]),
        later=bool(row["later"]),
    )


def _row_to_feedback(row: sqlite3.Row) -> FeedbackRecord:
    return FeedbackRecord(
        id=int(row["id"]),
        item_id=row["item_id"] if row["item_id"] is not None else None,
        dedup_key=row["dedup_key"],
        verdict=row["verdict"],
        channel=row["channel"],
        title=row["title"],
        category=row["category"],
        created_at=_from_iso(row["created_at"]),
    )


def _row_to_tuning(row: sqlite3.Row) -> TuningRecord:
    payload = _json_loads(row["payload"])
    return TuningRecord(
        id=int(row["id"]),
        kind=row["kind"],
        payload=payload if isinstance(payload, dict) else {},
        created_at=_from_iso(row["created_at"]),
    )


def _row_to_metric(row: sqlite3.Row) -> MetricRecord:
    return MetricRecord(
        id=int(row["id"]),
        category=row["category"],
        metric_key=row["metric_key"],
        field=row["field"],
        value=float(row["value"]),
        recorded_at=_from_iso(row["recorded_at"]),
    )


def _row_to_alert_rule(row: sqlite3.Row) -> AlertRule:
    config = _json_loads(row["action_config"])
    return AlertRule(
        id=int(row["id"]),
        name=row["name"],
        enabled=bool(row["enabled"]),
        scope=row["scope"],
        when=row["when_expr"],
        action=row["action"],
        action_config=config if isinstance(config, dict) else {},
        kind=row["kind"],
        params=(lambda value: value if isinstance(value, dict) else None)(
            _json_loads(row["params"]) if row["params"] is not None else None
        ),
        created_at=_from_iso(row["created_at"]),
        updated_at=_from_iso(row["updated_at"]),
    )


def _row_to_alert_fired(row: sqlite3.Row) -> AlertFired:
    return AlertFired(
        id=int(row["id"]),
        rule_id=int(row["rule_id"]),
        rule_name=row["rule_name"],
        item_id=row["item_id"] if row["item_id"] is not None else None,
        dedup_key=row["dedup_key"],
        title=row["title"],
        category=row["category"],
        action=row["action"],
        action_status=row["action_status"],
        created_at=_from_iso(row["created_at"]),
    )


def _require_finite_number(value: object, label: str) -> float:
    """Validate one numeric snapshot value (bool 不是数值;NaN/inf 拒写)."""
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(f"字段校验失败: {label} 必须是数值,得到 {value!r}")
    number = float(value)
    if not math.isfinite(number):
        raise ValueError(f"字段校验失败: {label} 必须是有限数值,得到 {value!r}")
    return number


def metric_window_start(now: datetime, window: str, tz: tzinfo | None = None) -> datetime:
    """Local start of the compare window containing ``now`` (趋势基线窗口数学).

    ``day`` = 当日本地零点(vs 昨日的分界),``week`` = 本 ISO 周周一零点
    (vs 上周的分界)。naive ``now`` 按 UTC 解释(store 全线约定);返回值
    携带 ``tz``(缺省 UTC),序列化比较前统一转 UTC。供
    :meth:`SQLiteStore.get_metric_baseline` 与推送层关键词周环比共用同一份
    窗口语义(单一实现,两处不漂)。

    Raises:
        ValueError: ``window`` 不在 :data:`myssia.store.models.METRIC_WINDOWS`。
    """
    if window not in METRIC_WINDOWS:
        raise ValueError(
            f"字段校验失败: 对比窗口必须是 {sorted(METRIC_WINDOWS)} 之一,得到 {window!r}"
        )
    zone = tz or timezone.utc
    aware = now.replace(tzinfo=timezone.utc) if now.tzinfo is None else now
    local = aware.astimezone(zone)
    if window == METRIC_WINDOW_DAY:
        return local.replace(hour=0, minute=0, second=0, microsecond=0)
    monday = local.date() - timedelta(days=local.weekday())  # ISO 周:周一为零点
    return datetime.combine(monday, datetime.min.time(), tzinfo=zone)


class SQLiteStore:
    """SQLite-backed :class:`myssia.store.base.Store`.

    Safe for cross-thread use within one process (guarded writes plus
    ``busy_timeout`` for other connections opening the same file).
    """

    def __init__(self, sqlite_path: str | Path) -> None:
        self.sqlite_path = Path(sqlite_path)
        self.sqlite_path.parent.mkdir(parents=True, exist_ok=True)
        self.conn = sqlite3.connect(str(self.sqlite_path), check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        self._lock = threading.RLock()
        try:
            # 并发首次开库串行化:journal_mode=WAL 换模式需要独占锁,且
            # busy handler 对该操作不重试(busy_timeout 挡不住),同进程
            # 多线程同时构造实例必有一个撞 database is locked。
            with _OPEN_LOCK:
                self._configure()
        except sqlite3.DatabaseError as exc:
            # PRAGMA journal_mode 是第一条真正触碰文件_bytes 的语句:
            # 损坏文件在这里暴露,统一转结构化错误(错误链保留)。
            raise self._corrupt_error(exc) from exc
        self.init_schema()

    def _corrupt_error(self, exc: sqlite3.DatabaseError) -> StoreSchemaError:
        return StoreSchemaError(
            "store_corrupt",
            f"数据库文件无法使用(损坏或不是 SQLite 库): {self.sqlite_path}({exc})",
            details={"path": str(self.sqlite_path)},
        )

    # ------------------------------------------------------------------ setup

    def _configure(self) -> None:
        # busy_timeout 必须最先设置:journal_mode=WAL 要拿写锁,并发首次开库时
        # 若另一条连接正在迁移/建表,未设超时的连接会立刻 database is locked。
        self.conn.execute("PRAGMA busy_timeout=5000")
        self.conn.execute("PRAGMA journal_mode=WAL")
        self.conn.execute("PRAGMA synchronous=NORMAL")

    def init_schema(self) -> None:
        """Create/upgrade the layout, validating the schema version.

        Raises:
            StoreSchemaError: the file is not a usable SQLite database
                (``store_corrupt``, original error chained as ``__cause__``),
                or its ``schema_version`` is newer than this binary knows
                (``schema_version_newer``).
        """
        # executescript 之前先看库里有没有我们的表:区分「全新文件」与
        # 「无版本戳的 v0.1 旧库」——前者只是首次盖章,不应谎报迁移。
        legacy = (
            self.conn.execute(
                "SELECT 1 FROM sqlite_master WHERE type = 'table' AND name = 'runs'"
            ).fetchone()
            is not None
        )
        try:
            with self._lock:
                self.conn.executescript(_SCHEMA)
                self._migrate(legacy=legacy)
                self.conn.commit()
        except sqlite3.DatabaseError as exc:
            raise self._corrupt_error(exc) from exc
        mode = self.conn.execute("PRAGMA journal_mode").fetchone()[0]
        logger.debug("存储已初始化 path=%s journal_mode=%s", self.sqlite_path, mode)

    # ------------------------------------------------------------- migrations

    def _table_columns(self, table: str) -> list[str]:
        rows = self.conn.execute(f"PRAGMA table_info({table})").fetchall()
        return [str(row[1]) for row in rows]

    def _migrate(self, *, legacy: bool) -> None:
        """Bring an opened database forward to :data:`SCHEMA_VERSION`.

        Version-stamp absence means a pre-hardening (v0.1) database
        (``legacy``) or a fresh file — both are migrated idempotently (each
        step checks before it ALTERs) and then stamped; only the former logs
        a migration line. Newer-than-binary versions are refused: silently
        misreading a future layout would corrupt user data.
        """
        raw = self.conn.execute(
            "SELECT value FROM store_meta WHERE key = ?", (_META_SCHEMA_VERSION,)
        ).fetchone()
        current = int(raw[0]) if raw is not None else 1
        if current > SCHEMA_VERSION:
            raise StoreSchemaError(
                "schema_version_newer",
                f"数据库 schema 版本过新: 库文件为 v{current},当前程序支持到 "
                f"v{SCHEMA_VERSION}(请升级 MYIA,不要降级打开新库)",
                details={"path": str(self.sqlite_path), "expected": SCHEMA_VERSION, "found": current},
            )
        if current < SCHEMA_VERSION and legacy:
            logger.info("存储迁移: v%s → v%s path=%s", current, SCHEMA_VERSION, self.sqlite_path)
        for version in range(current, SCHEMA_VERSION):
            migration = _MIGRATIONS.get(version + 1)
            if migration is None:  # 防御:没有登记迁移路径的版本缺口
                raise StoreSchemaError(
                    "schema_version_mismatch",
                    f"数据库 schema 版本 v{current} 缺少到 v{SCHEMA_VERSION} 的迁移路径",
                    details={"path": str(self.sqlite_path), "expected": SCHEMA_VERSION, "found": current},
                )
            migration(self.conn)
        self.conn.execute(
            "INSERT INTO store_meta (key, value) VALUES (?, ?) "
            "ON CONFLICT(key) DO UPDATE SET value = excluded.value",
            (_META_SCHEMA_VERSION, str(SCHEMA_VERSION)),
        )

    # -------------------------------------------------------------- key-value

    def get_meta(self, key: str) -> str | None:
        """Return the ``store_meta`` value for ``key``, or None when absent."""
        row = self._query_one("SELECT value FROM store_meta WHERE key = ?", (key,))
        return row["value"] if row is not None else None

    def set_meta(self, key: str, value: str) -> None:
        """Upsert one ``store_meta`` value (schema version, vacuum stamp)."""
        if not key:
            raise ValueError("字段校验失败: store_meta.key 不能为空")
        self._write(
            "INSERT INTO store_meta (key, value) VALUES (?, ?) "
            "ON CONFLICT(key) DO UPDATE SET value = excluded.value",
            (key, value),
        )

    # -------------------------------------------------------------- internals

    def _query_one(self, sql: str, params: tuple = ()) -> sqlite3.Row | None:
        return self.conn.execute(sql, params).fetchone()

    def _query_all(self, sql: str, params: tuple = ()) -> list[sqlite3.Row]:
        return self.conn.execute(sql, params).fetchall()

    def _write(self, sql: str, params: tuple = ()) -> sqlite3.Cursor:
        with self._lock:
            cursor = self.conn.execute(sql, params)
            self.conn.commit()
            return cursor

    # ------------------------------------------------------------------ items

    def save_item(self, item: ItemRecord) -> int:
        if not item.url:
            raise ValueError("字段校验失败: items.url 不能为空")
        if not item.dedup_key:
            raise ValueError("字段校验失败: items.dedup_key 不能为空")
        if not item.title:
            raise ValueError("字段校验失败: items.title 不能为空")
        first_seen = item.first_seen or datetime.now(timezone.utc)
        with self._lock:
            cursor = self.conn.execute(
                """
                INSERT INTO items (
                    url, dedup_key, source, title, content, content_hash,
                    tags, category, scores, pushed_at, push_slot, first_seen, raw
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    item.url,
                    item.dedup_key,
                    item.source,
                    item.title,
                    item.content,
                    item.content_hash,
                    _json_dumps(item.tags),
                    item.category,
                    _json_dumps(item.scores),
                    _to_iso(item.pushed_at),
                    item.push_slot,
                    _to_iso(first_seen),
                    _json_dumps(item.raw),
                ),
            )
            item_id = int(cursor.lastrowid)
            self.conn.commit()
        logger.debug(
            "条目入库 url=%s dedup_key=%s item_id=%s", item.url, item.dedup_key, item_id
        )
        return item_id

    def get_item(self, item_id: int) -> ItemRecord | None:
        row = self._query_one("SELECT * FROM items WHERE id = ?", (item_id,))
        return _row_to_item(row) if row is not None else None

    def get_item_by_dedup_key(self, dedup_key: str) -> ItemRecord | None:
        """Return the newest item carrying ``dedup_key``, or None when absent.

        The feedback-loop lookup (CLI ``myssia feedback mark <条目>``): the
        dedup key is the stable identity the pipeline assigns at the dedup
        stage. Dated-key templates can rotate, so multiple rows may share a
        historical key — newest wins.
        """
        if not dedup_key:
            raise ValueError("字段校验失败: items.dedup_key 不能为空")
        row = self._query_one(
            "SELECT * FROM items WHERE dedup_key = ? ORDER BY id DESC LIMIT 1",
            (dedup_key,),
        )
        return _row_to_item(row) if row is not None else None

    def _items_filter_sql(
        self,
        *,
        category: str | None,
        source: str | None,
        source_kind: str | None,
        since: datetime | None,
        before: datetime | None,
        before_id: int | None,
        query: str | None,
    ) -> tuple[str, list[object]]:
        """条目过滤的 WHERE 构造(:meth:`list_items` / :meth:`count_items`
        共用底座,F2 计数口径根治 10-09-tg-category-entry)。

        参数校验与词义同 :meth:`list_items`(游标复合键/三列 LIKE/源大类
        词表)—— 两方法吃同一组过滤参数必然产出同一 WHERE,``total`` 才与
        ``items`` 严格同口径。返回 ``(where 子句, 绑定参数)``;无条件时
        where 为空串。
        """
        if before is None and before_id is not None:
            raise ValueError("字段校验失败: before_id 需与 before 同传(复合游标)")
        # 深审 F6 校验对称:category 与 source 同门强校验(非空字符串;None =
        # 不过滤)。此前 category 完全未校验 —— 空串静默落 ``category = ''``
        # 永零命中(假空态),非字符串原样进 SQL;source 只挡空串不挡类型。
        if category is not None and (not isinstance(category, str) or not category):
            raise ValueError("字段校验失败: category 过滤需要非空字符串(不过滤请传 None)")
        if source is not None and (not isinstance(source, str) or not source):
            raise ValueError("字段校验失败: source 过滤需要非空字符串(不过滤请传 None)")
        if source_kind is not None and source_kind not in ("web", "im"):
            raise ValueError("字段校验失败: source_kind 只接受 web/im(不过滤请传 None)")
        conditions: list[str] = []
        params: list[object] = []
        if category is not None:
            conditions.append("category = ?")
            params.append(category)
        if source is not None:
            conditions.append("source = ?")
            params.append(source)
        if source_kind == "im":
            conditions.append("(source LIKE 'telegram-%' OR source LIKE 'tg-%')")
        elif source_kind == "web":
            conditions.append(
                "(source IS NULL OR (source NOT LIKE 'telegram-%' AND source NOT LIKE 'tg-%'))"
            )
        if since is not None:
            conditions.append("first_seen >= ?")
            params.append(_to_iso(since))
        if before is not None:
            if before_id is not None:
                conditions.append("(first_seen < ? OR (first_seen = ? AND id < ?))")
                params.extend([_to_iso(before), _to_iso(before), before_id])
            else:
                conditions.append("first_seen < ?")
                params.append(_to_iso(before))
        if query:
            # LIKE 转义:%/_ 按字面匹配(ESCAPE '\';方括号通配符非 SQLite 语法不涉)
            escaped = query.replace("\\", "\\\\").replace("%", r"\%").replace("_", r"\_")
            like = f"%{escaped}%"
            conditions.append(
                "(title LIKE ? ESCAPE '\\' COLLATE NOCASE"
                " OR content LIKE ? ESCAPE '\\' COLLATE NOCASE"
                " OR source LIKE ? ESCAPE '\\' COLLATE NOCASE)"
            )
            params.extend([like, like, like])
        where = (" WHERE " + " AND ".join(conditions)) if conditions else ""
        return where, params

    def list_items(
        self,
        *,
        category: str | None = None,
        source: str | None = None,
        source_kind: str | None = None,
        since: datetime | None = None,
        before: datetime | None = None,
        before_id: int | None = None,
        query: str | None = None,
        limit: int | None = None,
    ) -> list[ItemRecord]:
        """List items, newest first(桌面情报流分页的查询面).

        游标参数(10-03-v112-desktop-batch C1,与 feed-ux G1 合流形状):
        ``before`` = first_seen 严格小于;``before_id`` 与 ``before`` 组成
        ``(first_seen, id)`` 元组比较 —— 同刻(相同 first_seen)条目数超过
        单页 limit 时,单靠 ``before`` 会把同刻更旧条目整批跳过,复合游标
        才能推进直至取尽。``query`` = title/content/source 三列 LIKE
        (NOCASE,无索引单机万级可接受,如实注记)。``source`` = 源名精确
        等值(10-06-feed-channel-groups 三级下钻 L3 渠道消息流;与
        ``category`` 同门精确等值,非 LIKE)。``source_kind`` = 源大类过滤
        (10-08-tg-channel-card v2 卡片墙;``"im"`` = 通讯软件源,``"web"``
        = 其余含无源条目;与 UI 前缀判定同一词表,LIKE ASCII 不区分大小写
        —— UI 正则要求分隔符 [-._],LIKE 'telegram-%' 对 'telegramX' 形
        近似多中,源名为系统生成规约名,差异面为零,如实注记)。
        """
        if limit is not None and limit < 0:
            raise ValueError(f"字段校验失败: limit 不能为负数,得到 {limit}")
        where, params = self._items_filter_sql(
            category=category, source=source, source_kind=source_kind, since=since,
            before=before, before_id=before_id, query=query,
        )
        sql = f"SELECT * FROM items{where} ORDER BY first_seen DESC, id DESC"
        if limit is not None:
            sql += " LIMIT ?"
            params.append(limit)
        return [_row_to_item(row) for row in self._query_all(sql, tuple(params))]

    def count_items(
        self,
        *,
        category: str | None = None,
        source: str | None = None,
        source_kind: str | None = None,
        since: datetime | None = None,
        before: datetime | None = None,
        before_id: int | None = None,
        query: str | None = None,
    ) -> int:
        """Count items matching the same filters as :meth:`list_items`
        (同 WHERE 不分页的全量计数,F2 计数口径根治,10-09-tg-category-entry)。

        ``store.items`` 的 ``with_total`` 底座:与 :meth:`list_items` 同参
        同 WHERE(经 :meth:`_items_filter_sql` 单点构造,词义漂移即测试红),
        不含 ORDER/LIMIT —— 返回该过滤条件下的匹配行数,即 UI「已加载 N ·
        共 T 条」的 T。游标键(before/before_id)原样接受:游标本就是过滤
        条件的一部分,带游标计数 = 「该页之后的余量」口径。

        Raises:
            ValueError: 参数校验(词义同 :meth:`list_items`)。
        """
        where, params = self._items_filter_sql(
            category=category, source=source, source_kind=source_kind, since=since,
            before=before, before_id=before_id, query=query,
        )
        row = self._query_one(f"SELECT COUNT(*) FROM items{where}", tuple(params))
        return int(row[0]) if row is not None else 0

    def source_stats(self, *, since: datetime | None = None) -> list[dict]:
        """分源聚合(source_stats,v8 三级界面 1 级类型卡统计底座,
        10-09-tg-category-entry)。

        一条 SQL 出全库真值,UI 按类型归并(类型卡今日/未读不能从「首页
        50 条铺底」聚合——单源日增百条即可把首页吃满,其余类型落「今日 0」
        截断假象;分源聚合一次直答,零截断)。每源一行:

        - ``total``:全库条数(不限窗);
        - ``today``:``first_seen >= since`` 的条数(当日窗 03:00 窗锚与
          视图同源,UI 传 ``dayWindowStart().toISOString()``);**since 缺省
          = today 恒 0**——「无窗无今日」如实,不猜自然日边界;
        - ``unread``:未标已读(COALESCE(read,0)=0;与 feedChannelCards
          的 unread 同义,不含 later 到期重现加成——重现条目极少数且多为
          已读,偏差面由 UI 注记如实接受);
        - ``latest_first_seen`` / ``latest_title``:最新一条的入库时刻与
          标题(二遍逐源取,title 供 2 级行预览回退;分组行数 ~ 源数,
          成本可忽略)。

        NULL source 行(活库 0 条,schema 允许)照出一行 ``source: null``,
        归并口径(计入「网站」卡的 today/unread、不计渠道数)是 UI 的职责,
        store 层不裁剪。排序 = 最新入库源在前(与 UI 渠道行主序同向)。

        Raises:
            ValueError: since 与数据库时间列类型不符由 sqlite 层自然报错;
            此处只做 None 直传,非法 ISO 由协议面(`_m_store_source_stats`
            的 _parse_iso 同门)拦截。
        """
        if since is not None:
            today_expr = "SUM(CASE WHEN first_seen >= ? THEN 1 ELSE 0 END)"
            params: tuple = (_to_iso(since),)
        else:
            today_expr = "0"
            params = ()
        sql = (
            "SELECT source, COUNT(*) AS total, "
            f"{today_expr} AS today, "
            "SUM(CASE WHEN COALESCE(read, 0) = 0 THEN 1 ELSE 0 END) AS unread, "
            "MAX(first_seen) AS latest_first_seen "
            "FROM items GROUP BY source ORDER BY MAX(first_seen) DESC"
        )
        stats: list[dict] = []
        for row in self._query_all(sql, params):
            source = row["source"]
            latest_first_seen = row["latest_first_seen"]
            # 二遍取每源最新一条 title(同刻多行取 id 最大 = 最晚入库的;
            # source IS ? 对 NULL 同样成立,IS 比较不吃索引歧义)
            title_row = self._query_one(
                "SELECT title FROM items WHERE source IS ? AND first_seen = ? "
                "ORDER BY id DESC LIMIT 1",
                (source, latest_first_seen),
            )
            stats.append(
                {
                    "source": source,
                    "total": int(row["total"]),
                    "today": int(row["today"] or 0),
                    "unread": int(row["unread"] or 0),
                    "latest_first_seen": latest_first_seen,
                    "latest_title": title_row["title"] if title_row is not None else None,
                }
            )
        return stats

    def set_item_states(self, dedup_keys: list[str], marker: str, value: bool) -> int:
        """置位一批 dedup_key 的读态标记(G9,store.state.mark 底座)。

        marker ∈ {"read", "starred", "later"};``UPDATE items SET <marker> = ?
        WHERE dedup_key IN (...)`` —— 同键多行(dated-key 旋转)同置,与
        localStorage itemKey 语义一致(Q1.3);幂等(显式置目标值,无读-改-写)。
        采集管线永不携带读态(save_item 列清单不含三列),读态只由此面置位。

        Returns:
            实改行数 = SQLite UPDATE rowcount(口径:匹配行数——直连模式下
            置同值行也计入;如实回传,不做「实改值」二次核算,协议应答
            ``updated`` 即此数)。

        Raises:
            ValueError: marker 非法 / dedup_keys 空 / 含空串或非字符串。
        """
        column = _item_state_column(marker)
        if not dedup_keys:
            raise ValueError("字段校验失败: dedup_keys 不能为空")
        for key in dedup_keys:
            if not isinstance(key, str) or not key:
                raise ValueError("字段校验失败: dedup_keys 不能包含非字符串或空串")
        placeholders = ", ".join("?" for _ in dedup_keys)
        cursor = self._write(
            f"UPDATE items SET {column} = ? WHERE dedup_key IN ({placeholders})",
            (1 if value else 0, *dedup_keys),
        )
        return int(cursor.rowcount)

    def set_all_item_states(
        self,
        marker: str,
        value: bool,
        category: str | None = None,
        source_kind: str | None = None,
    ) -> int:
        """全库(可选 category / source_kind)置位(G9,store.state.mark_all 底座)。

        单条 ``UPDATE items SET <marker> = ? [WHERE ...]``;category 词义与
        :meth:`list_items` 同参(精确等值,非 LIKE;不收 query——决议 Q3.2
        钉死:LIKE 进 UPDATE 是范围蠕变)。None = 全库所有条目(含未翻页/
        未加载),这是「全部标已读」的全库语义来源。``source_kind`` = 源大类
        作用域(10-08-tg-channel-card v2,卡片墙第二层的批量语义;词义同
        :meth:`list_items`,与 category 可叠加)。

        Returns:
            rowcount(口径同 :meth:`set_item_states`:匹配行数,如实回传)。

        Raises:
            ValueError: marker 非法 / category 空串(None 表全库,空串是入参
                错误)/ source_kind 非法。
        """
        column = _item_state_column(marker)
        if category is not None and not category:
            raise ValueError("字段校验失败: category 不能为空串(全库请传 None)")
        if source_kind is not None and source_kind not in ("web", "im"):
            raise ValueError("字段校验失败: source_kind 只接受 web/im(全库请传 None)")
        sql = f"UPDATE items SET {column} = ?"
        conditions: list[str] = []
        params: list[object] = [1 if value else 0]
        if category is not None:
            conditions.append("category = ?")
            params.append(category)
        if source_kind == "im":
            conditions.append("(source LIKE 'telegram-%' OR source LIKE 'tg-%')")
        elif source_kind == "web":
            conditions.append(
                "(source IS NULL OR (source NOT LIKE 'telegram-%' AND source NOT LIKE 'tg-%'))"
            )
        if conditions:
            sql += " WHERE " + " AND ".join(conditions)
        cursor = self._write(sql, tuple(params))
        return int(cursor.rowcount)

    def import_item_states(self, states: dict[str, dict[str, bool]]) -> tuple[int, int]:
        """导入 localStorage 读态快照(G9,Q2 搬迁门;幂等旗标在调用方 handler)。

        key 三分(Q2.4):dedup_key 直配;``id:<n>`` 先 ``SELECT dedup_key
        FROM items WHERE id=<n>`` 取键(取不到 = 跳过);``id:<url>`` 及任何
        无从解析形态 = 跳过。每键单条 UPDATE(同键多行同置,与
        :meth:`set_item_states` 同红线;SET 子句只含快照中出现的标记键,
        缺省标记不写 = 逐行继承现有列值)。整键覆盖而非逐键合并——快照是
        v1 期唯一真源,合并无信息可合。

        Returns:
            ``(imported, skipped)``:imported = 有匹配行的键数(实际写了
            ≥1 行);skipped = 无匹配行 / 无法解析 / 三键全缺省(``{}``
            值条目跳写)的键数。N 键 N 条 UPDATE 单连接一次 commit(v1
            map 量级 = 用户点过的条目数,百级典型,不引入批量 CASE WHEN)。

        幂等性由 handler 侧 ``store_meta`` 旗标(``feed_state_imported_at``)
        保证;本方法本身可重复调用(重放 = 再覆盖,故旗标必须先行)。
        """
        imported = 0
        skipped = 0
        with self._lock:
            for key, snapshot in states.items():
                resolved: str | None = key
                if isinstance(key, str) and key.startswith("id:"):
                    ref = key[3:]
                    if not ref.isdigit():
                        resolved = None  # id:<url> 形态:无从解析,跳过
                    else:
                        row = self.conn.execute(
                            "SELECT dedup_key FROM items WHERE id = ?", (int(ref),)
                        ).fetchone()
                        resolved = str(row["dedup_key"]) if row is not None else None
                if resolved is None:
                    skipped += 1
                    continue
                assignments: dict[str, int] = {}
                if isinstance(snapshot, dict):
                    for name, column in _ITEM_STATE_COLUMNS.items():
                        if name in snapshot:
                            assignments[column] = 1 if snapshot[name] else 0
                if not assignments:
                    skipped += 1  # {} 值 / 全未知标记:跳写
                    continue
                set_clause = ", ".join(f"{column} = ?" for column in assignments)
                cursor = self.conn.execute(
                    f"UPDATE items SET {set_clause} WHERE dedup_key = ?",
                    (*assignments.values(), resolved),
                )
                if cursor.rowcount > 0:
                    imported += 1
                else:
                    skipped += 1  # 键合法但无匹配行(条目已剪枝):不复活,如实计
            self.conn.commit()
        return imported, skipped

    def daily_item_counts(
        self, *, days: int = 14, category: str | None = None
    ) -> list[tuple[str, int]]:
        """Per-day item counts for the last ``days`` days(采集量趋势,桌面 store.trend).

        Groups on ``substr(first_seen, 1, 10)``(UTC calendar day,如实口径 ——
        不做时区换算);窗口下界 = UTC now − days 天(仅作 SQL 过滤,零数日
        补齐归调用方/前端 ``fillDailyCounts``,store 只回有数日)。Returns
        ``[(date, count)]`` old → new,窗口内零条目时为空列表(合法空态)。

        Raises:
            ValueError: ``days`` 非正整数(与 list_feedback 的 limit 校验同口径)。
        """
        if not isinstance(days, int) or isinstance(days, bool) or days < 1:
            raise ValueError(f"字段校验失败: days 必须为正整数,得到 {days!r}")
        since = (datetime.now(timezone.utc) - timedelta(days=days)).isoformat()
        sql = (
            "SELECT substr(first_seen, 1, 10) AS day, COUNT(*) AS count "
            "FROM items WHERE first_seen IS NOT NULL AND first_seen >= ?"
        )
        params: list[object] = [since]
        if category is not None:
            sql += " AND category = ?"
            params.append(category)
        sql += " GROUP BY day ORDER BY day ASC"
        return [
            (str(row["day"]), int(row["count"]))
            for row in self._query_all(sql, tuple(params))
        ]

    def daily_run_outcomes(
        self, *, days: int = 14, category: str | None = None
    ) -> list[dict[str, object]]:
        """Per-day per-status run counts for the last ``days`` days(成功率趋势,runs.trend)。

        Groups on ``substr(started_at, 1, 10)``(UTC calendar day,与
        :meth:`daily_item_counts` 同口径);窗口下界 = UTC now − days 天
        (仅作 SQL 过滤,零数日补齐归调用方/前端)。Returns
        ``[{date, total, statuses: {<status>: count}}]`` old → new,窗口内
        零 run 时为空列表(合法空态)。statuses 为开放词表原样分组——真实
        词表 4 态 running/success/partial/failed(models.py RUN_STATUSES),
        未知状态照回,前端只消费 success/running 两键,其余求和入「完结未全成」。

        Raises:
            ValueError: ``days`` 非正整数(与 :meth:`daily_item_counts` 同口径)。
        """
        if not isinstance(days, int) or isinstance(days, bool) or days < 1:
            raise ValueError(f"字段校验失败: days 必须为正整数,得到 {days!r}")
        since = (datetime.now(timezone.utc) - timedelta(days=days)).isoformat()
        sql = (
            "SELECT substr(started_at, 1, 10) AS day, status, COUNT(*) AS n "
            "FROM runs WHERE started_at IS NOT NULL AND started_at >= ?"
        )
        params: list[object] = [since]
        if category is not None:
            sql += " AND category = ?"
            params.append(category)
        sql += " GROUP BY day, status ORDER BY day ASC"
        out: dict[str, dict[str, object]] = {}
        for row in self._query_all(sql, tuple(params)):
            date = str(row["day"])
            day = out.setdefault(date, {"date": date, "total": 0, "statuses": {}})
            statuses = day["statuses"]
            assert isinstance(statuses, dict)  # 上面 setdefault 的形状,窄化给类型器
            status = str(row["status"])
            statuses[status] = statuses.get(status, 0) + int(row["n"])
            day["total"] = int(day["total"]) + int(row["n"])
        return [out[date] for date in sorted(out)]

    def mark_item_pushed(
        self, item_id: int, slot: str, pushed_at: datetime | None = None
    ) -> None:
        if slot not in PUSH_SLOTS:
            raise ValueError(
                f"字段校验失败: push_slot 必须是 {sorted(PUSH_SLOTS)} 之一,得到 {slot!r}"
            )
        cursor = self._write(
            "UPDATE items SET pushed_at = ?, push_slot = ? WHERE id = ?",
            (_to_iso(pushed_at or datetime.now(timezone.utc)), slot, item_id),
        )
        if cursor.rowcount == 0:
            raise ValueError(f"items 记录不存在: id={item_id}")
        logger.debug("条目推送登记 item_id=%s slot=%s", item_id, slot)

    def update_item_scores(self, dedup_key: str, scores: Mapping[str, object]) -> bool:
        """Backfill one item's ``scores`` JSON column (LLM 精评回填 items 表).

        Matches on ``dedup_key`` — the stable identity assigned at the dedup
        stage and stored on the row (rows are inserted before analyze runs).

        Args:
            dedup_key: the item's dedup key (must be non-empty).
            scores: JSON-serializable payload, e.g. ``{"value": 8,
                "relevance": 9, "credibility": 7, "score": 8.0}``.

        Returns:
            True when a row was updated, False when no item carries the key
            (caller decides whether that is worth a warning).

        Raises:
            ValueError: empty ``dedup_key`` or a non-mapping ``scores``.
        """
        if not dedup_key:
            raise ValueError("字段校验失败: items.dedup_key 不能为空")
        if not isinstance(scores, Mapping):
            raise ValueError(
                f"字段校验失败: scores 必须是键值映射,得到 {type(scores).__name__}"
            )
        cursor = self._write(
            "UPDATE items SET scores = ? WHERE dedup_key = ?",
            (_json_dumps(dict(scores)), dedup_key),
        )
        updated = cursor.rowcount > 0
        if updated:
            logger.debug("条目评分回填 dedup_key=%s dims=%s", dedup_key, sorted(scores))
        return updated

    def merge_item_metadata(self, dedup_key: str, metadata: Mapping[str, object]) -> bool:
        """Merge keys into one item's ``raw`` JSON column(分析 lane 装饰回填).

        定位语义与 :meth:`update_item_scores` 同门(dedup_key 稳定身份);读改写
        在同一把写锁内完成,防并发 run 丢更新。合并语义 = 现有 ``raw`` 键保留、
        同名新键覆盖(lane 装饰是 run 级重算,最新一轮为准);``raw`` 原值不是
        对象(损坏行)时以本次合并值为准整体重建——装饰不因行坏而丢,行坏由
        retention/doctor 面另行暴露。

        Raises:
            ValueError: empty ``dedup_key`` or a non-mapping ``metadata``.
        """
        if not dedup_key:
            raise ValueError("字段校验失败: items.dedup_key 不能为空")
        if not isinstance(metadata, Mapping):
            raise ValueError(
                f"字段校验失败: metadata 必须是键值映射,得到 {type(metadata).__name__}"
            )
        with self._lock:
            row = self.conn.execute(
                "SELECT raw FROM items WHERE dedup_key = ? ORDER BY id DESC LIMIT 1",
                (dedup_key,),
            ).fetchone()
            if row is None:
                return False
            current = _json_loads(row["raw"]) if isinstance(row["raw"], str) else None
            merged: dict[str, object] = dict(current) if isinstance(current, dict) else {}
            merged.update(dict(metadata))
            cursor = self.conn.execute(
                "UPDATE items SET raw = ? WHERE dedup_key = ?",
                (_json_dumps(merged), dedup_key),
            )
            self.conn.commit()
        if cursor.rowcount:
            logger.debug("条目装饰回填 dedup_key=%s fields=%s", dedup_key, sorted(metadata))
        return bool(cursor.rowcount)

    # ---------------------------------------------------------- dedup_registry

    def get_dedup_entry(self, key: str) -> DedupEntry | None:
        row = self._query_one("SELECT * FROM dedup_registry WHERE key = ?", (key,))
        if row is None:
            return None
        return DedupEntry(
            key=row["key"],
            first_seen=_from_iso(row["first_seen"]),
            last_pushed_at=_from_iso(row["last_pushed_at"]),
            last_push_slot=row["last_push_slot"],
        )

    def mark_dedup_seen(self, key: str, first_seen: datetime) -> None:
        if not key:
            raise ValueError("字段校验失败: dedup_registry.key 不能为空")
        self._write(
            "INSERT OR IGNORE INTO dedup_registry (key, first_seen) VALUES (?, ?)",
            (key, _to_iso(first_seen)),
        )

    def record_dedup_push(self, key: str, pushed_at: datetime, slot: str) -> None:
        if not key:
            raise ValueError("字段校验失败: dedup_registry.key 不能为空")
        if slot not in PUSH_SLOTS:
            raise ValueError(
                f"字段校验失败: push_slot 必须是 {sorted(PUSH_SLOTS)} 之一,得到 {slot!r}"
            )
        self._write(
            """
            INSERT INTO dedup_registry (key, first_seen, last_pushed_at, last_push_slot)
            VALUES (?, ?, ?, ?)
            ON CONFLICT(key) DO UPDATE SET
                last_pushed_at = excluded.last_pushed_at,
                last_push_slot = excluded.last_push_slot
            """,
            (key, _to_iso(pushed_at), _to_iso(pushed_at), slot),
        )
        logger.debug("去重推送登记 key=%s slot=%s", key, slot)

    # ---------------------------------------------------------- change_baseline

    def get_baseline(self, url: str) -> ChangeBaseline | None:
        row = self._query_one("SELECT * FROM change_baseline WHERE url = ?", (url,))
        if row is None:
            return None
        return ChangeBaseline(
            url=row["url"],
            etag=row["etag"],
            last_modified=row["last_modified"],
            content_hash=row["content_hash"],
            last_changed=_from_iso(row["last_changed"]),
        )

    def set_baseline(
        self,
        url: str,
        *,
        etag: str | None = None,
        last_modified: str | None = None,
        content_hash: str | None = None,
        last_changed: datetime | None = None,
    ) -> None:
        if not url:
            raise ValueError("字段校验失败: change_baseline.url 不能为空")
        self._write(
            """
            INSERT INTO change_baseline (url, etag, last_modified, content_hash, last_changed)
            VALUES (?, ?, ?, ?, ?)
            ON CONFLICT(url) DO UPDATE SET
                etag = excluded.etag,
                last_modified = excluded.last_modified,
                content_hash = excluded.content_hash,
                last_changed = excluded.last_changed
            """,
            (url, etag, last_modified, content_hash, _to_iso(last_changed)),
        )
        logger.debug("变更基线更新 url=%s etag=%s", url, bool(etag))

    # ------------------------------------------------------------- engine_hints

    def get_engine_hint(self, source_key: str) -> str | None:
        row = self._query_one(
            "SELECT engine FROM engine_hints WHERE source_key = ?", (source_key,)
        )
        return row["engine"] if row is not None else None

    def set_engine_hint(self, source_key: str, engine: str) -> None:
        if not source_key:
            raise ValueError("字段校验失败: engine_hints.source_key 不能为空")
        if not engine:
            raise ValueError("字段校验失败: engine_hints.engine 不能为空")
        self._write(
            """
            INSERT INTO engine_hints (source_key, engine, updated_at)
            VALUES (?, ?, ?)
            ON CONFLICT(source_key) DO UPDATE SET
                engine = excluded.engine,
                updated_at = excluded.updated_at
            """,
            (source_key, engine, _to_iso(datetime.now(timezone.utc))),
        )
        logger.debug("引擎提示回写 source_key=%s engine=%s", source_key, engine)

    def clear_engine_hint(self, source_key: str) -> None:
        self._write("DELETE FROM engine_hints WHERE source_key = ?", (source_key,))
        logger.debug("引擎提示清除 source_key=%s", source_key)

    # ----------------------------------------------------------- enrich_cache

    def get_enrich_cache(self, url: str, model: str, scores_key: str) -> dict | None:
        """Return the cached score result for one URL, or None on a miss.

        Cache identity is ``(url, model, scores_key)``: switching the model or
        the score dimensions / prompt version (both fingerprinted into
        ``scores_key``) invalidates old entries — schema 变更才重评 semantics.

        Raises:
            ValueError: any key component is empty.
        """
        if not url or not model or not scores_key:
            raise ValueError("字段校验失败: enrich_cache 查询键(url/model/scores_key)不能为空")
        row = self._query_one(
            "SELECT result FROM enrich_cache "
            "WHERE url = ? AND model = ? AND scores_key = ?",
            (url, model, scores_key),
        )
        if row is None:
            return None
        try:
            result = _json_loads(row["result"])
        except (TypeError, ValueError) as exc:
            logger.warning("enrich_cache 行损坏(按未命中处理) url=%s: %s", url, exc)
            return None
        return result if isinstance(result, dict) else None

    def set_enrich_cache(
        self,
        url: str,
        model: str,
        scores_key: str,
        result: Mapping[str, object],
        created_at: datetime | None = None,
    ) -> None:
        """Upsert one cached score result (same URL re-score overwrites).

        Raises:
            ValueError: empty key component or a non-mapping ``result``.
        """
        if not url or not model or not scores_key:
            raise ValueError("字段校验失败: enrich_cache 写入键(url/model/scores_key)不能为空")
        if not isinstance(result, Mapping):
            raise ValueError(
                f"字段校验失败: enrich_cache.result 必须是键值映射,得到 {type(result).__name__}"
            )
        self._write(
            """
            INSERT INTO enrich_cache (url, model, scores_key, result, created_at)
            VALUES (?, ?, ?, ?, ?)
            ON CONFLICT(url, model, scores_key) DO UPDATE SET
                result = excluded.result,
                created_at = excluded.created_at
            """,
            (
                url,
                model,
                scores_key,
                _json_dumps(dict(result)),
                _to_iso(created_at or datetime.now(timezone.utc)),
            ),
        )
        logger.debug("enrich 缓存写入 url=%s model=%s", url, model)

    def clear_enrich_cache(self, url: str | None = None) -> int:
        """Drop cached scores — manual invalidation (手动失效才重评).

        Args:
            url: drop only this URL's entries; ``None`` clears the whole table.

        Returns:
            Number of rows deleted.
        """
        if url is None:
            with self._lock:
                cursor = self.conn.execute("DELETE FROM enrich_cache")
                self.conn.commit()
        else:
            cursor = self._write("DELETE FROM enrich_cache WHERE url = ?", (url,))
        logger.info("enrich 缓存失效 url=%s deleted=%s", url or "(全部)", cursor.rowcount)
        return cursor.rowcount

    # ---------------------------------------------------------------- feedback

    def save_feedback(self, feedback: FeedbackRecord) -> int | None:
        """Insert one good/bad verdict; return its row id, ``None`` on duplicate.

        ``title`` / ``category`` snapshots travel on the record; the caller
        resolves them from the item (feedback package). Append-only: verdicts
        are never updated (同一卡片改判 = 新增一行,历史可追溯). Idempotent on
        the provider event identity: 同一 ``(channel, external_id)`` 只记一次
        —— 双击/平台重试/重启重放不再凑出第二条 bad(护栏「one angry click
        must not mute a word forever」不被一次双击击穿);``external_id`` 为
        NULL(CLI 手动路径)不受约束,恒插入。

        Returns:
            New row id, or ``None`` when a row with the same
            ``(channel, external_id)`` already exists (duplicate skipped).

        Raises:
            ValueError: empty ``dedup_key`` / ``channel``, or ``verdict``
                outside :data:`myssia.store.models.FEEDBACK_VERDICTS`.
        """
        if not feedback.dedup_key:
            raise ValueError("字段校验失败: feedback.dedup_key 不能为空")
        if feedback.verdict not in FEEDBACK_VERDICTS:
            raise ValueError(
                f"字段校验失败: feedback.verdict 必须是 {sorted(FEEDBACK_VERDICTS)} 之一,"
                f"得到 {feedback.verdict!r}"
            )
        if not feedback.channel:
            raise ValueError("字段校验失败: feedback.channel 不能为空")
        with self._lock:
            cursor = self.conn.execute(
                """
                INSERT INTO feedback (
                    item_id, dedup_key, verdict, channel, title, category,
                    external_id, created_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(channel, external_id) DO NOTHING
                """,
                (
                    feedback.item_id,
                    feedback.dedup_key,
                    feedback.verdict,
                    feedback.channel,
                    feedback.title,
                    feedback.category,
                    feedback.external_id,
                    _to_iso(feedback.created_at or datetime.now(timezone.utc)),
                ),
            )
            inserted = cursor.rowcount > 0
            feedback_id = int(cursor.lastrowid) if inserted else None
            self.conn.commit()
        if inserted:
            logger.debug(
                "反馈入库 feedback_id=%s verdict=%s channel=%s dedup_key=%s",
                feedback_id, feedback.verdict, feedback.channel, feedback.dedup_key,
            )
        else:
            logger.info(
                "重复反馈已忽略(幂等) channel=%s external_id=%s dedup_key=%s",
                feedback.channel, feedback.external_id, feedback.dedup_key,
            )
        return feedback_id

    def list_feedback(
        self,
        *,
        verdict: str | None = None,
        channel: str | None = None,
        since: datetime | None = None,
        limit: int | None = None,
    ) -> list[FeedbackRecord]:
        """List feedback rows, newest first, with optional filters.

        Raises:
            ValueError: ``verdict`` given but outside the vocabulary, negative
                ``limit``.
        """
        if verdict is not None and verdict not in FEEDBACK_VERDICTS:
            raise ValueError(
                f"字段校验失败: verdict 必须是 {sorted(FEEDBACK_VERDICTS)} 之一,得到 {verdict!r}"
            )
        if limit is not None and limit < 0:
            raise ValueError(f"字段校验失败: limit 不能为负数,得到 {limit}")
        sql = "SELECT * FROM feedback"
        conditions: list[str] = []
        params: list[object] = []
        if verdict is not None:
            conditions.append("verdict = ?")
            params.append(verdict)
        if channel is not None:
            conditions.append("channel = ?")
            params.append(channel)
        if since is not None:
            conditions.append("created_at >= ?")
            params.append(_to_iso(since))
        if conditions:
            sql += " WHERE " + " AND ".join(conditions)
        sql += " ORDER BY id DESC"
        if limit is not None:
            sql += " LIMIT ?"
            params.append(limit)
        return [_row_to_feedback(row) for row in self._query_all(sql, tuple(params))]

    def save_tuning(self, adjustment: TuningRecord) -> int:
        """Append one tuning-adjustment row and return its id (append-only).

        Raises:
            ValueError: empty ``kind`` or a non-mapping ``payload``.
        """
        if not adjustment.kind:
            raise ValueError("字段校验失败: feedback_tuning.kind 不能为空")
        if not isinstance(adjustment.payload, Mapping):
            raise ValueError(
                f"字段校验失败: feedback_tuning.payload 必须是键值映射,"
                f"得到 {type(adjustment.payload).__name__}"
            )
        with self._lock:
            cursor = self.conn.execute(
                "INSERT INTO feedback_tuning (kind, payload, created_at) VALUES (?, ?, ?)",
                (
                    adjustment.kind,
                    _json_dumps(dict(adjustment.payload)),
                    _to_iso(adjustment.created_at or datetime.now(timezone.utc)),
                ),
            )
            adjustment_id = int(cursor.lastrowid)
            self.conn.commit()
        logger.debug(
            "调参历史入库 tuning_id=%s kind=%s payload_keys=%s",
            adjustment_id, adjustment.kind, sorted(adjustment.payload),
        )
        return adjustment_id

    def list_tuning(
        self, *, kind: str | None = None, limit: int | None = None
    ) -> list[TuningRecord]:
        """List tuning rows, newest first (调整历史), optionally by kind."""
        if limit is not None and limit < 0:
            raise ValueError(f"字段校验失败: limit 不能为负数,得到 {limit}")
        sql = "SELECT * FROM feedback_tuning"
        params: list[object] = []
        if kind is not None:
            sql += " WHERE kind = ?"
            params.append(kind)
        sql += " ORDER BY id DESC"
        if limit is not None:
            sql += " LIMIT ?"
            params.append(limit)
        return [_row_to_tuning(row) for row in self._query_all(sql, tuple(params))]

    # ---------------------------------------------------------- metric_history
    # Consumed by the v0.4 trend baseline (PRD 10-01-v04-trend-baseline):
    # numeric snapshots per (category, metric_key, field) power the
    # 「vs 昨日 / vs 上周」 template functions and keyword week-over-week.
    # Retention keeps this table longer than items (基线期长于条目期).

    def save_metric(
        self,
        category: str,
        metric_key: str,
        field: str,
        value: float,
        *,
        recorded_at: datetime | None = None,
    ) -> int:
        """Append one numeric snapshot and return its row id (append-only 历史).

        Raises:
            ValueError: empty ``category`` / ``metric_key`` / ``field``, or a
                non-numeric / non-finite ``value`` (bool 也不是数值).
        """
        if not category:
            raise ValueError("字段校验失败: metric_history.category 不能为空")
        if not metric_key:
            raise ValueError("字段校验失败: metric_history.metric_key 不能为空")
        if not field:
            raise ValueError("字段校验失败: metric_history.field 不能为空")
        number = _require_finite_number(value, "metric_history.value")
        with self._lock:
            cursor = self.conn.execute(
                "INSERT INTO metric_history (category, metric_key, field, value, recorded_at) "
                "VALUES (?, ?, ?, ?, ?)",
                (
                    category,
                    metric_key,
                    field,
                    number,
                    _to_iso(recorded_at or datetime.now(timezone.utc)),
                ),
            )
            self.conn.commit()
            metric_id = int(cursor.lastrowid)
        logger.debug(
            "数值快照入库 category=%s key=%s field=%s value=%s", category, metric_key, field, number
        )
        return metric_id

    def latest_metric(
        self, category: str, metric_key: str, field: str
    ) -> MetricRecord | None:
        """Return the newest snapshot for the key, or None when never recorded."""
        row = self._query_one(
            "SELECT * FROM metric_history "
            "WHERE category = ? AND metric_key = ? AND field = ? "
            "ORDER BY recorded_at DESC, id DESC LIMIT 1",
            (category, metric_key, field),
        )
        return _row_to_metric(row) if row is not None else None

    def get_metric_baseline(
        self,
        category: str,
        metric_key: str,
        field: str,
        *,
        now: datetime,
        window: str,
        tz: tzinfo | None = None,
    ) -> MetricRecord | None:
        """Newest snapshot recorded strictly before the window start (窗口对比).

        ``window='day'`` → vs 昨日:the newest snapshot before 当地零点
        (today's own snapshots never answer as their own baseline);
        ``window='week'`` → vs 上周:the newest before 本 ISO 周周一零点.
        ``tz`` is the category schedule timezone (slot-boundary semantics
        follow the same zone); None means UTC. Naive ``now`` is read as UTC.

        Returns:
            The baseline snapshot, or None when the key has no history before
            the window start (first observation — callers render no
            comparison rather than inventing one).

        Raises:
            ValueError: ``window`` outside
                :data:`myssia.store.models.METRIC_WINDOWS`.
        """
        start = metric_window_start(now, window, tz)
        row = self._query_one(
            "SELECT * FROM metric_history "
            "WHERE category = ? AND metric_key = ? AND field = ? AND recorded_at < ? "
            "ORDER BY recorded_at DESC, id DESC LIMIT 1",
            (category, metric_key, field, _to_iso(start)),
        )
        return _row_to_metric(row) if row is not None else None

    def sum_metrics(
        self,
        category: str,
        metric_key: str,
        field: str,
        *,
        since: datetime,
        until: datetime,
    ) -> float:
        """Sum snapshots recorded in the half-open ``[since, until)`` window.

        周环比的品类级聚合:per-run 关键词命中数逐 run 入库后,本周累计 =
        ``sum_metrics(week_start, next_week_start)``,上周累计同理(半开区间
        保证两次调用恰好铺满相邻两周、无重叠无遗漏)。

        Raises:
            ValueError: empty key components, or ``since >= until``.
        """
        if not category or not metric_key or not field:
            raise ValueError("字段校验失败: sum_metrics 查询键(category/metric_key/field)不能为空")
        if since >= until:
            raise ValueError(
                f"字段校验失败: sum_metrics 窗口为空(since={_to_iso(since)} >= until={_to_iso(until)})"
            )
        row = self._query_one(
            "SELECT COALESCE(SUM(value), 0.0) AS total FROM metric_history "
            "WHERE category = ? AND metric_key = ? AND field = ? "
            "AND recorded_at >= ? AND recorded_at < ?",
            (category, metric_key, field, _to_iso(since), _to_iso(until)),
        )
        return float(row["total"]) if row is not None else 0.0

    # ------------------------------------------------------------------ alerts
    # Consumed by the alert rules engine (PRD 10-04-alert-rules): rules are
    # written by the desktop sidecar (alerts.save 全量替换在此之上 diff 编排),
    # fired rows are the 命中历史 — snapshots survive rule deletion and item
    # retention. scope/when 语法/action_config 形状的构造期拒在
    # myssia.alerts.rule.compile_rule(读库坏行 WARNING 跳过、写库拒整批共用)。

    def save_alert_rule(self, rule: AlertRule) -> AlertRule:
        """Insert or update one alert rule; return the persisted row.

        带 ``id`` = UPDATE(未知 id 抛值错);无 ``id`` = INSERT。
        ``updated_at`` 落库侧每次刷新;``created_at`` 仅 INSERT 时落(缺省 now)。

        Raises:
            ValueError: empty ``name`` / ``when``, ``action`` outside
                :data:`myssia.store.models.ALERT_ACTIONS`, or an unknown
                ``rule.id`` on update.
        """
        if not rule.name:
            raise ValueError("字段校验失败: alert_rules.name 不能为空")
        if not rule.when or not rule.when.strip():
            raise ValueError("字段校验失败: alert_rules.when_expr 不能为空")
        if rule.action not in ALERT_ACTIONS:
            raise ValueError(
                f"字段校验失败: alert_rules.action 必须是 {sorted(ALERT_ACTIONS)} 之一,"
                f"得到 {rule.action!r}"
            )
        now = datetime.now(timezone.utc)
        if rule.id is not None:
            cursor = self._write(
                "UPDATE alert_rules SET name = ?, enabled = ?, scope = ?, when_expr = ?, "
                "action = ?, action_config = ?, kind = ?, params = ?, updated_at = ? WHERE id = ?",
                (
                    rule.name,
                    1 if rule.enabled else 0,
                    rule.scope,
                    rule.when,
                    rule.action,
                    _json_dumps(rule.action_config),
                    rule.kind,
                    _json_dumps(rule.params) if rule.params is not None else None,
                    _to_iso(now),
                    rule.id,
                ),
            )
            if cursor.rowcount == 0:
                raise ValueError(f"alert_rules 记录不存在: id={rule.id}")
            row = self._query_one("SELECT * FROM alert_rules WHERE id = ?", (rule.id,))
        else:
            with self._lock:
                cursor = self.conn.execute(
                    "INSERT INTO alert_rules (name, enabled, scope, when_expr, action, "
                    "action_config, kind, params, created_at, updated_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                    (
                        rule.name,
                        1 if rule.enabled else 0,
                        rule.scope,
                        rule.when,
                        rule.action,
                        _json_dumps(rule.action_config),
                        rule.kind,
                        _json_dumps(rule.params) if rule.params is not None else None,
                        _to_iso(rule.created_at or now),
                        _to_iso(now),
                    ),
                )
                new_id = int(cursor.lastrowid)
                self.conn.commit()
            row = self._query_one("SELECT * FROM alert_rules WHERE id = ?", (new_id,))
        persisted = _row_to_alert_rule(row)
        logger.debug("告警规则落库 rule_id=%s name=%s action=%s", persisted.id, persisted.name, persisted.action)
        return persisted

    def list_alert_rules(self, *, enabled: bool | None = None) -> list[AlertRule]:
        """List alert rules, id ascending; ``enabled=None`` applies no filter."""
        if enabled is None:
            rows = self._query_all("SELECT * FROM alert_rules ORDER BY id ASC")
        else:
            rows = self._query_all(
                "SELECT * FROM alert_rules WHERE enabled = ? ORDER BY id ASC",
                (1 if enabled else 0,),
            )
        return [_row_to_alert_rule(row) for row in rows]

    def delete_alert_rule(self, rule_id: int) -> bool:
        """Drop one rule definition row; fired history stays (命中历史是事实).

        Returns True when a row was deleted, False when the id matches nothing.
        """
        cursor = self._write("DELETE FROM alert_rules WHERE id = ?", (rule_id,))
        deleted = cursor.rowcount > 0
        if deleted:
            logger.info("告警规则删除 rule_id=%s(fired 历史照留)", rule_id)
        return deleted

    def record_fired(self, fired: AlertFired) -> AlertFired | None:
        """Insert one fired row as the 占坑门闩; return it, or None on duplicate.

        ``UNIQUE (rule_id, dedup_key)`` 冲突 → None(调用方跳过动作,
        at-most-once;send_immediate 的 registry 槽位哲学同源)。成功返回落库行
        (含 id,``action_status`` 起始为 ``pending``)。

        Raises:
            ValueError: empty ``dedup_key``, ``action`` outside
                :data:`myssia.store.models.ALERT_ACTIONS`, or ``action_status``
                outside :data:`myssia.store.models.ALERT_ACTION_STATUSES`.
        """
        if not fired.dedup_key:
            raise ValueError("字段校验失败: alert_fired.dedup_key 不能为空")
        if fired.action not in ALERT_ACTIONS:
            raise ValueError(
                f"字段校验失败: alert_fired.action 必须是 {sorted(ALERT_ACTIONS)} 之一,"
                f"得到 {fired.action!r}"
            )
        if fired.action_status not in ALERT_ACTION_STATUSES:
            raise ValueError(
                f"字段校验失败: alert_fired.action_status 必须是 "
                f"{sorted(ALERT_ACTION_STATUSES)} 之一,得到 {fired.action_status!r}"
            )
        with self._lock:
            cursor = self.conn.execute(
                "INSERT INTO alert_fired (rule_id, rule_name, item_id, dedup_key, title, "
                "category, action, action_status, created_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?) "
                "ON CONFLICT(rule_id, dedup_key) DO NOTHING",
                (
                    fired.rule_id,
                    fired.rule_name,
                    fired.item_id,
                    fired.dedup_key,
                    fired.title,
                    fired.category,
                    fired.action,
                    fired.action_status,
                    _to_iso(fired.created_at or datetime.now(timezone.utc)),
                ),
            )
            inserted = cursor.rowcount > 0
            new_id = int(cursor.lastrowid) if inserted else None
            self.conn.commit()
        if not inserted:
            logger.info(
                "告警命中占坑冲突(UNIQUE 拦截,跳过动作) rule_id=%s dedup_key=%s",
                fired.rule_id, fired.dedup_key,
            )
            return None
        row = self._query_one("SELECT * FROM alert_fired WHERE id = ?", (new_id,))
        persisted = _row_to_alert_fired(row)
        logger.debug(
            "告警命中入库 fired_id=%s rule_id=%s dedup_key=%s action=%s",
            persisted.id, persisted.rule_id, persisted.dedup_key, persisted.action,
        )
        return persisted

    def mark_alert_fired_status(self, fired_id: int, status: str) -> None:
        """Backfill one fired row's terminal ``action_status`` (动作结果回填).

        Raises:
            ValueError: ``status`` outside
                :data:`myssia.store.models.ALERT_ACTION_STATUSES`, or no fired
                row with ``fired_id``.
        """
        if status not in ALERT_ACTION_STATUSES:
            raise ValueError(
                f"字段校验失败: alert_fired.action_status 必须是 "
                f"{sorted(ALERT_ACTION_STATUSES)} 之一,得到 {status!r}"
            )
        cursor = self._write(
            "UPDATE alert_fired SET action_status = ? WHERE id = ?", (status, fired_id)
        )
        if cursor.rowcount == 0:
            raise ValueError(f"alert_fired 记录不存在: id={fired_id}")

    def has_fired(self, rule_id: int, dedup_key: str) -> bool:
        """Whether ``(rule_id, dedup_key)`` already fired(命中预查,alerts.test).

        Raises:
            ValueError: empty ``dedup_key``.
        """
        if not dedup_key:
            raise ValueError("字段校验失败: alert_fired.dedup_key 不能为空")
        return (
            self._query_one(
                "SELECT 1 FROM alert_fired WHERE rule_id = ? AND dedup_key = ? LIMIT 1",
                (rule_id, dedup_key),
            )
            is not None
        )

    def list_fired(
        self,
        *,
        rule_id: int | None = None,
        since: datetime | None = None,
        limit: int = 100,
    ) -> list[AlertFired]:
        """List fired rows, newest first(``limit`` 钳制 [1, 200]).

        ``since`` filters on ``created_at``(sidecar run 终态回放取新命中);
        ``rule_id`` 过滤(CLI ``alerts list --rule`` / alerts.list 载荷)。
        """
        clamped = max(1, min(200, int(limit)))
        sql = "SELECT * FROM alert_fired"
        conditions: list[str] = []
        params: list[object] = []
        if rule_id is not None:
            conditions.append("rule_id = ?")
            params.append(rule_id)
        if since is not None:
            conditions.append("created_at >= ?")
            params.append(_to_iso(since))
        if conditions:
            sql += " WHERE " + " AND ".join(conditions)
        sql += " ORDER BY id DESC LIMIT ?"
        params.append(clamped)
        return [_row_to_alert_fired(row) for row in self._query_all(sql, tuple(params))]

    def fired_counts(self) -> dict[int, int]:
        """Per-rule hit counts, derived from ``alert_fired`` (GROUP BY COUNT).

        命中计数不落 rules 行(save 全量替换会清计数,grill Q1)——派生即真相。
        """
        rows = self._query_all(
            "SELECT rule_id, COUNT(*) AS count FROM alert_fired GROUP BY rule_id"
        )
        return {int(row["rule_id"]): int(row["count"]) for row in rows}

    def update_item_tags(self, *, dedup_key: str, tags: Sequence[str]) -> bool:
        """Write back one item's ``tags`` JSON column by ``dedup_key``(tag 动作第 2 步).

        定位语义与 :meth:`get_item_by_dedup_key` 同门(dedup_key 是 dedup 阶段
        落的稳定身份);行不存在(如已被 retention 剪枝)返回 False,由调用方
        WARNING 说破,不视为错误。

        Raises:
            ValueError: empty ``dedup_key``.
        """
        if not dedup_key:
            raise ValueError("字段校验失败: items.dedup_key 不能为空")
        cursor = self._write(
            "UPDATE items SET tags = ? WHERE dedup_key = ?",
            (_json_dumps(list(tags)), dedup_key),
        )
        return cursor.rowcount > 0

    # -------------------------------------------------------------------- runs

    def start_run(self, category: str) -> int:
        if not category:
            raise ValueError("字段校验失败: runs.category 不能为空")
        with self._lock:
            cursor = self.conn.execute(
                "INSERT INTO runs (category, started_at, status) VALUES (?, ?, ?)",
                (category, _to_iso(datetime.now(timezone.utc)), RUN_STATUS_RUNNING),
            )
            run_id = int(cursor.lastrowid)
            self.conn.commit()
        logger.debug("run 开始 run_id=%s category=%s", run_id, category)
        return run_id

    def finish_run(
        self,
        run_id: int,
        *,
        status: str,
        stats: dict | None = None,
        error: str | None = None,
    ) -> None:
        if status not in RUN_STATUSES:
            raise ValueError(
                f"字段校验失败: runs.status 必须是 {sorted(RUN_STATUSES)} 之一,得到 {status!r}"
            )
        cursor = self._write(
            "UPDATE runs SET finished_at = ?, status = ?, stats = ?, error = ? WHERE id = ?",
            (_to_iso(datetime.now(timezone.utc)), status, _json_dumps(stats), error, run_id),
        )
        if cursor.rowcount == 0:
            raise ValueError(f"runs 记录不存在: id={run_id}")
        logger.debug("run 结束 run_id=%s status=%s", run_id, status)

    def set_run_log_run_id(self, run_id: int, log_run_id: int) -> None:
        """回填 run 的会话级日志身份(10-07-logs-restart-visibility R1)。

        sidecar 在 run 收口处调用:把「本会话注册表 run_id」落到 runs 行——
        JSONL 日志行按此值打 run_id,跨重启后历史行展开 ``logs.tail`` 用它
        对齐(裸 runs.id 与会话号是两个编号空间,不能混用)。旧库行保持
        NULL(会话号已不可考,不伪造);重复回填以末次为准(同 run 重跑
        收口幂等覆盖)。
        """
        if not isinstance(log_run_id, int) or isinstance(log_run_id, bool) or log_run_id < 1:
            raise ValueError(f"字段校验失败: runs.log_run_id 必须为正整数,得到 {log_run_id!r}")
        cursor = self._write(
            "UPDATE runs SET log_run_id = ? WHERE id = ?",
            (log_run_id, run_id),
        )
        if cursor.rowcount == 0:
            raise ValueError(f"runs 记录不存在: id={run_id}")
        logger.debug("run 日志身份回填 run_id=%s log_run_id=%s", run_id, log_run_id)

    def _row_to_run(self, row: sqlite3.Row) -> RunRecord:
        # sqlite3.Row 不是 dict:`in` 走 __iter__(值而非键),必须用 row.keys()。
        keys = row.keys()
        steps = _json_loads(row["steps"]) if "steps" in keys else None  # noqa: SIM118
        # log_run_id:v10 起在场;防御式读(旧连接/异构行不炸,v2 steps 同款)。
        log_run_id = row["log_run_id"] if "log_run_id" in keys else None  # noqa: SIM118
        return RunRecord(
            id=int(row["id"]),
            category=row["category"],
            started_at=_from_iso(row["started_at"]),
            status=row["status"],
            finished_at=_from_iso(row["finished_at"]),
            stats=_json_loads(row["stats"]),
            error=row["error"],
            steps=steps if isinstance(steps, dict) else None,
            log_run_id=int(log_run_id) if log_run_id is not None else None,
        )

    def list_runs(self, *, category: str | None = None, limit: int = 50) -> list[RunRecord]:
        """List persisted runs, newest first(桌面 runs.list 直读,C3).

        与内存注册表(entry.py ``_RUNS``)互补:重启后历史 run 由此可达。
        ``limit`` 负数即拒(照 :meth:`list_feedback` 口径)。
        """
        if limit < 0:
            raise ValueError(f"字段校验失败: limit 不能为负数,得到 {limit}")
        if category is not None:
            rows = self._query_all(
                "SELECT * FROM runs WHERE category = ? ORDER BY id DESC LIMIT ?",
                (category, limit),
            )
        else:
            rows = self._query_all("SELECT * FROM runs ORDER BY id DESC LIMIT ?", (limit,))
        return [self._row_to_run(row) for row in rows]

    def get_run(self, run_id: int) -> RunRecord | None:
        row = self._query_one("SELECT * FROM runs WHERE id = ?", (run_id,))
        return self._row_to_run(row) if row is not None else None

    def previous_run(self, category: str, *, before_run_id: int) -> RunRecord | None:
        """Return the most recent run of ``category`` with ``id < before_run_id``.

        The 断点续跑 lookup anchor: the pipeline asks "what did the run right
        before mine leave behind?" — a crashed (status ``running``) or
        failed/partial predecessor with recorded step checkpoints.
        """
        if not category:
            raise ValueError("字段校验失败: runs.category 不能为空")
        row = self._query_one(
            "SELECT * FROM runs WHERE category = ? AND id < ? ORDER BY id DESC LIMIT 1",
            (category, before_run_id),
        )
        return self._row_to_run(row) if row is not None else None

    def update_run_step(
        self,
        run_id: int,
        step: str,
        *,
        status: str,
        payload: Mapping[str, object] | None = None,
    ) -> None:
        """Record one pipeline step's progress on the ``runs.steps`` JSON column.

        Existing entries for other steps are preserved (read-modify-write
        under the connection lock). ``payload`` is the resumable checkpoint
        (e.g. ``{"items": [...]}``) — it must be JSON-serializable.

        Raises:
            ValueError: unknown ``run_id``, empty ``step``, ``status`` outside
                :data:`myssia.store.models.STEP_STATUSES`, or a non-mapping
                payload.
        """
        if not step:
            raise ValueError("字段校验失败: runs.steps.step 不能为空")
        if status not in STEP_STATUSES:
            raise ValueError(
                f"字段校验失败: 步骤状态必须是 {sorted(STEP_STATUSES)} 之一,得到 {status!r}"
            )
        if payload is not None and not isinstance(payload, Mapping):
            raise ValueError(
                f"字段校验失败: 步骤 payload 必须是键值映射或 None,得到 {type(payload).__name__}"
            )
        with self._lock:
            row = self.conn.execute("SELECT steps FROM runs WHERE id = ?", (run_id,)).fetchone()
            if row is None:
                raise ValueError(f"runs 记录不存在: id={run_id}")
            try:
                steps: dict[str, object] = dict(_json_loads(row["steps"]) or {})
            except (TypeError, ValueError) as exc:
                raise ValueError(f"runs.steps 已有数据无法解析 run_id={run_id}: {exc}") from exc
            entry: dict[str, object] = {
                "status": status,
                "completed_at": _to_iso(datetime.now(timezone.utc)),
            }
            if payload is not None:
                entry["payload"] = dict(payload)
            steps[step] = entry
            self.conn.execute(
                "UPDATE runs SET steps = ? WHERE id = ?",
                (json.dumps(steps, ensure_ascii=False), run_id),
            )
            self.conn.commit()
        logger.debug("run 步骤进度 run_id=%s step=%s status=%s", run_id, step, status)

    def latest_run(self, category: str | None = None) -> RunRecord | None:
        if category is None:
            row = self._query_one("SELECT * FROM runs ORDER BY id DESC LIMIT 1")
        else:
            row = self._query_one(
                "SELECT * FROM runs WHERE category = ? ORDER BY id DESC LIMIT 1",
                (category,),
            )
        return self._row_to_run(row) if row is not None else None

    # ------------------------------------------------------- retention/vacuum

    def cleanup_expired(
        self,
        retention_days: int,
        *,
        now: datetime | None = None,
        active_urls: Collection[str] | None = None,
        metrics_retention_days: int | None = None,
    ) -> dict[str, int]:
        """Delete retention-expired rows; return per-table deletion counts.

        Policy (区分已推送与未推送条目):

        - pushed items — anchored at ``pushed_at``, dropped after
          ``retention_days`` (delivered content has served its purpose);
        - never-pushed items — anchored at ``first_seen``, kept for
          ``UNPUSHED_RETENTION_MULTIPLIER × retention_days`` (undelivered
          content stays one extra window for diagnosis/recovery);
        - change baselines + engine hints — per-URL caches, pruned ONLY via an
          explicit ``active_urls`` set (the caller must own the whole DB
          namespace: one shared ``myssia.db`` serves every category, so a single
          category's source list is NOT authoritative for "stale URL").
          Without ``active_urls`` they are left untouched: rows are tiny (one
          per source URL ever seen), and both wrong kinds of deletion are
          catastrophic — cross-category pruning kills other categories'
          fingerprints / engine learning, and age-pruning by ``last_changed``
          kills quiet sources (the stamp only moves when content actually
          changes);
        - runs — finished rows and stale ``running`` rows (crashed processes)
          after ``retention_days`` (checkpoint payloads are the bulk);
        - metric_history (数值基线) — after
          ``BASELINE_RETENTION_MULTIPLIER × retention_days`` anchored at
          ``recorded_at``: 基线期长于条目期 — week-over-week (and day-over-day)
          comparisons need at least two full windows of history to survive
          (PRD 10-01-v04-trend-baseline retention 协同).

        All timestamps compared as normalized ISO-8601 UTC strings.

        Args:
            retention_days: retention window in days; must be >= 1.
            now: evaluation instant; defaults to the current UTC time.
            active_urls: currently configured source URLs across the WHOLE
                database (baselines/hints outside the set are stale); None —
                the safe default for the shared multi-category DB — leaves
                both URL-keyed caches alone.

            metrics_retention_days: ``metric_history`` retention override;
                ``None`` keeps the ``BASELINE_RETENTION_MULTIPLIER ×
                retention_days`` default. Pipeline 传入声明窗口下限
                (两个完整窗口 + 余量),短 retention + week 窗口时防基线被清空.

        Returns:
            Counts: ``items_pushed`` / ``items_unpushed`` / ``baselines`` /
            ``engine_hints`` / ``runs`` / ``enrich_cache`` / ``metrics``.

        Raises:
            ValueError: ``retention_days`` < 1.
        """
        if retention_days < 1:
            raise ValueError(f"字段校验失败: retention_days 必须为正整数,得到 {retention_days}")
        now = now or datetime.now(timezone.utc)
        pushed_cutoff = _to_iso(now - timedelta(days=retention_days))
        unpushed_cutoff = _to_iso(
            now - timedelta(days=retention_days * UNPUSHED_RETENTION_MULTIPLIER)
        )
        counts: dict[str, int] = {}
        with self._lock:
            counts["items_pushed"] = self.conn.execute(
                "DELETE FROM items WHERE pushed_at IS NOT NULL AND pushed_at < ?",
                (pushed_cutoff,),
            ).rowcount
            counts["items_unpushed"] = self.conn.execute(
                "DELETE FROM items WHERE pushed_at IS NULL AND first_seen < ?",
                (unpushed_cutoff,),
            ).rowcount
            if active_urls is not None:
                counts["baselines"] = self._delete_stale_urls(
                    "change_baseline", "url", active_urls
                )
                counts["engine_hints"] = self._delete_stale_urls(
                    "engine_hints", "source_key", active_urls
                )
            else:
                # 共享库安全缺省:同一 myssia.db 服务所有品类,单品类的源清单
                # 无权判定「别的 URL 已失效」;而 last_changed 只在内容真变时
                # 刷新,按龄删会误杀安静源的指纹 skip。URL 缓存行极小(每源
                # 一行)、误删代价是两套核心缓存机制失效,故只在调用方显式给
                # 出全库 active_urls 时才修剪。
                counts["baselines"] = 0
                counts["engine_hints"] = 0
            counts["runs"] = self.conn.execute(
                "DELETE FROM runs WHERE "
                "(finished_at IS NOT NULL AND finished_at < ?) OR "
                f"(status = '{RUN_STATUS_RUNNING}' AND started_at < ?)",
                (pushed_cutoff, pushed_cutoff),
            ).rowcount
            # enrich_cache 是纯缓存(命中省 token,未命中重评即可):随 retention
            # 老化清除,防长期桌面运行无界膨胀(2026-10 复盘:该表此前无任何
            # 过期路径,clear_enrich_cache 只能手动调用)。
            counts["enrich_cache"] = self.conn.execute(
                "DELETE FROM enrich_cache WHERE created_at < ?",
                (pushed_cutoff,),
            ).rowcount
            # metric_history(趋势基线)保留期 = max(2× retention, 调用方给的
            # 声明窗口下限):基线期长于条目期,且必须覆盖「两个完整声明窗口 +
            # 余量」—— 否则 retention: 3d + windows: [week] 时,周中后段的
            # 「窗口开始前最新快照」被清空,vs 上周结构性失效且无告警。纯数值
            # 行极小,老化上界仍需存在(防长期运行无界膨胀)。
            metrics_days = (
                metrics_retention_days
                if metrics_retention_days is not None
                else retention_days * BASELINE_RETENTION_MULTIPLIER
            )
            baseline_cutoff = _to_iso(now - timedelta(days=metrics_days))
            counts["metrics"] = self.conn.execute(
                "DELETE FROM metric_history WHERE recorded_at < ?",
                (baseline_cutoff,),
            ).rowcount
            # 注意:dedup_registry 不做自动按龄删除——它是 all-time dedup
            # (is_seen)与同槽位防重发的底座,删行会让重新出现的旧条目被再次
            # 推送。手动治理走 :meth:`prune_dedup_registry`。
            self.conn.commit()
        total = sum(counts.values())
        log = logger.info if total else logger.debug
        log(
            "过期清理完成 retention_days=%s deleted=%s(items_pushed=%s items_unpushed=%s "
            "baselines=%s engine_hints=%s runs=%s enrich_cache=%s metrics=%s)",
            retention_days, total, counts["items_pushed"], counts["items_unpushed"],
            counts["baselines"], counts["engine_hints"], counts["runs"],
            counts["enrich_cache"], counts["metrics"],
        )
        return counts

    def _delete_stale_urls(
        self, table: str, column: str, active_urls: Collection[str]
    ) -> int:
        """Delete ``table`` rows whose key URL is not in ``active_urls``."""
        active = sorted(set(active_urls))
        if not active:  # 无活跃源 → 全部按过期处理
            return self.conn.execute(f"DELETE FROM {table}").rowcount
        placeholders = ", ".join("?" for _ in active)
        return self.conn.execute(
            f"DELETE FROM {table} WHERE {column} NOT IN ({placeholders})",
            tuple(active),
        ).rowcount

    def prune_dedup_registry(self, *, before: datetime) -> int:
        """Manually delete dedup_registry rows older than ``before``; return count.

        ⚠️ dedup_registry 承载两层语义:all-time dedup(:meth:`DedupRegistry.is_seen`,
        防同一 item 反复入库/推送)与同槽位防重发(should_send)。自动按龄删除会
        让「重新出现的旧条目」再次通过 dedup 被推送——防重发兜底失效(storage PRD
        明言依赖该表兜底)。因此**不挂自动策略**,只提供这个显式手动治理通道:
        调用方须确认 ``before`` 之前的条目确无重现风险(如 before 距今 < 1 天,
        槽位窗口之外的行)。

        Age anchor: ``COALESCE(last_pushed_at, first_seen)`` — a row last pushed
        (or first seen) before ``before`` is pruned.
        """
        cutoff = _to_iso(before)
        with self._lock:
            deleted = self.conn.execute(
                "DELETE FROM dedup_registry WHERE COALESCE(last_pushed_at, first_seen) < ?",
                (cutoff,),
            ).rowcount
            self.conn.commit()
        if deleted:
            logger.info("dedup_registry 手动修剪 before=%s deleted=%s", cutoff, deleted)
        return deleted

    def vacuum(self) -> None:
        """Rebuild the database file, reclaiming free pages (anti-bloat).

        VACUUM cannot run inside a transaction; pending writes are committed
        first. Page counts before/after land in the log (膨胀观测).
        """
        with self._lock:
            self.conn.commit()
            before = self.conn.execute("PRAGMA page_count").fetchone()[0]
            self.conn.execute("VACUUM")
            after = self.conn.execute("PRAGMA page_count").fetchone()[0]
        logger.info(
            "数据库 VACUUM 完成 path=%s page_count %s → %s",
            self.sqlite_path, before, after,
        )

    def maybe_vacuum(self, cadence: str, *, now: datetime | None = None) -> bool:
        """Run :meth:`vacuum` when the configured cadence is due.

        The ``last_vacuum_at`` stamp lives in ``store_meta``; cadence is
        calendar-based in UTC (daily = another date, weekly = another ISO
        week, monthly = another month), so "monthly" fires once per month no
        matter how often runs execute.

        Args:
            cadence: ``daily`` / ``weekly`` / ``monthly`` / ``never``
                (schema ``storage.vacuum`` vocabulary).
            now: evaluation instant; defaults to the current UTC time.

        Returns:
            True when a VACUUM ran, False when skipped (never / not yet due).

        Raises:
            ValueError: unknown cadence.
        """
        if cadence not in VACUUM_CADENCES:
            raise ValueError(
                f"字段校验失败: vacuum 周期必须是 {sorted(VACUUM_CADENCES)} 之一,得到 {cadence!r}"
            )
        now = now or datetime.now(timezone.utc)
        if cadence == "never":
            return False
        last_raw = self.get_meta(_META_LAST_VACUUM_AT)
        last = _from_iso(last_raw) if last_raw else None
        if last is not None and not _cadence_elapsed(cadence, last, now):
            logger.debug("VACUUM 未到周期 cadence=%s last=%s", cadence, last_raw)
            return False
        self.vacuum()
        self.set_meta(_META_LAST_VACUUM_AT, _to_iso(now) or "")
        logger.info("定时 VACUUM 已执行 cadence=%s", cadence)
        return True

    # --------------------------------------------------------------- lifecycle

    def close(self) -> None:
        self.conn.close()

    def __enter__(self) -> "SQLiteStore":
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        self.close()
