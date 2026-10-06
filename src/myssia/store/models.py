"""Data models and vocabulary shared by all storage implementations.

Store methods accept and return these typed records; serialization
(JSON columns, ISO-8601 UTC timestamps) stays inside each implementation.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime

# AM/PM push slots (grill Q3, PRD v01-store-dedup): the local day splits at
# 12:00 — AM = 00:00-11:59, PM = 12:00-23:59. digest and immediate pushes
# share one registry; this layer answers "发没发过", push route answers
# "推不推".
SLOT_AM = "am"
SLOT_PM = "pm"
PUSH_SLOTS = frozenset({SLOT_AM, SLOT_PM})

# Feedback verdicts (feedback table, PRD 10-01-v03-feedback-loop): the
# push-card 回写 is a binary judgement — 有价值 / 没价值.
FEEDBACK_GOOD = "good"
FEEDBACK_BAD = "bad"
FEEDBACK_VERDICTS = frozenset({FEEDBACK_GOOD, FEEDBACK_BAD})

# Receiving channels of one feedback (feedback.channel): CLI manual marking
# and the two channel-specific callback paths (grill Q7 分形态接收).
# desktop = 桌面 app 卡片 👍/👎(v1.1.2 桌面对齐批 B2;channel 为自由串无词表
# 校验,此常数只作常量家与 CLI/桌面互认锚点 —— `myssia feedback list` 无过滤即见)。
FEEDBACK_CHANNEL_CLI = "cli"
FEEDBACK_CHANNEL_TELEGRAM = "telegram"
FEEDBACK_CHANNEL_FEISHU = "feishu"
FEEDBACK_CHANNEL_DESKTOP = "desktop"

# Tuning adjustment kinds (feedback_tuning table). The feedback loop's
# periodic task appends rows here; the LATEST row per key (word / category)
# is the active adjustment, so history stays fully traceable (可追溯).
TUNING_MUTE_WEIGHT = "mute_weight"  # payload: {word, weight, bad_count, ratio}
TUNING_CATEGORY_PENALTY = "category_penalty"  # payload: {category, weight, ...}
TUNING_PROMPT_NOTE = "prompt_note"  # payload: {note, categories, words}

# Pipeline run statuses (runs table). Exit-code mapping (0/1/2/3) lives in
# the CLI layer, not here.
RUN_STATUS_RUNNING = "running"
RUN_STATUS_SUCCESS = "success"
RUN_STATUS_PARTIAL = "partial"
RUN_STATUS_FAILED = "failed"
RUN_STATUSES = frozenset(
    {RUN_STATUS_RUNNING, RUN_STATUS_SUCCESS, RUN_STATUS_PARTIAL, RUN_STATUS_FAILED}
)

# Trend-baseline compare windows (metric_history, PRD 10-01-v04-trend-baseline):
# ``day`` compares against the newest snapshot recorded before today's local
# midnight (vs 昨日), ``week`` against the newest before this ISO week's
# Monday 00:00 (vs 上周).
METRIC_WINDOW_DAY = "day"
METRIC_WINDOW_WEEK = "week"
METRIC_WINDOWS = frozenset({METRIC_WINDOW_DAY, METRIC_WINDOW_WEEK})

# Per-step progress recorded in ``runs.steps`` (JSON column, v0.2 storage
# hardening). ``ok``/``failed`` are written when a stage completes or exhausts
# its retries; ``skipped`` marks stages bypassed (upstream failed); ``resumed``
# marks steps inherited from an interrupted predecessor run (断点续跑) -- the
# payload travels with the entry so the resumed row stays self-sufficient.
STEP_STATUS_OK = "ok"
STEP_STATUS_FAILED = "failed"
STEP_STATUS_SKIPPED = "skipped"
STEP_STATUS_RESUMED = "resumed"
STEP_STATUSES = frozenset(
    {STEP_STATUS_OK, STEP_STATUS_FAILED, STEP_STATUS_SKIPPED, STEP_STATUS_RESUMED}
)

# Alert actions (alert_rules.action, PRD 10-04-alert-rules grill Q4): one
# rule = one action; push = send_immediate 同门 immediate push, tag =
# Item.add_tags + items.tags 回写. 沉淀为关键词 / digest 汇总留 v2.
ALERT_ACTION_PUSH = "push"
ALERT_ACTION_TAG = "tag"
ALERT_ACTIONS = frozenset({ALERT_ACTION_PUSH, ALERT_ACTION_TAG})

# Alert rule scope (alert_rules.scope): ``global`` applies to every
# category's ingest; any other value is a category id (七品类+channel 词表,
# myssia.push.route.CATEGORY_DEFAULT_ROUTES) and the rule only evaluates
# against that category's items.
ALERT_SCOPE_GLOBAL = "global"

# Fired-row action statuses (alert_fired.action_status): written ``pending``
# at the 占坑 INSERT, backfilled with the terminal outcome once the action
# executes (mark_alert_fired_status). ``skipped_dry_run`` is reserved for the
# dry evaluation path (alerts.test, sidecar Stage D) which never sends.
ALERT_STATUS_PENDING = "pending"
ALERT_STATUS_SENT = "sent"
ALERT_STATUS_SEND_FAILED = "send_failed"
ALERT_STATUS_TAGGED = "tagged"
ALERT_STATUS_DEGRADED_NO_CHANNEL = "degraded_no_channel"
ALERT_STATUS_SKIPPED_DRY_RUN = "skipped_dry_run"
ALERT_ACTION_STATUSES = frozenset(
    {
        ALERT_STATUS_PENDING,
        ALERT_STATUS_SENT,
        ALERT_STATUS_SEND_FAILED,
        ALERT_STATUS_TAGGED,
        ALERT_STATUS_DEGRADED_NO_CHANNEL,
        ALERT_STATUS_SKIPPED_DRY_RUN,
    }
)

# Alert rule kind (alert_rules.kind, 10-05-cron-heartbeat): ``item`` = 条目
# 驱动规则(when 表达式求值于 ingest 条目,10-04-alert-rules 原语义);
# ``cron_stale`` = 时间驱动心跳规则(品类久未成功触发即告警,executions
# 账本只读评估,不进条目求值路径)。cron_stale 参数落 ``params`` JSON:
# {threshold_hours>0} 或 {auto: true}(阈值 = 2× 账本观测节奏,夹
# [1,168]h;观测不足由评估侧 WARNING 跳过,fail-fast 不猜)。
ALERT_RULE_KIND_ITEM = "item"
ALERT_RULE_KIND_CRON_STALE = "cron_stale"
ALERT_RULE_KINDS = frozenset({ALERT_RULE_KIND_ITEM, ALERT_RULE_KIND_CRON_STALE})


@dataclass(slots=True)
class ItemRecord:
    """One intelligence entry persisted in the ``items`` table."""

    url: str
    dedup_key: str
    title: str
    source: str | None = None
    content: str | None = None  # sanitized digest of the body, not the full text
    content_hash: str | None = None
    tags: list[str] = field(default_factory=list)
    category: str | None = None
    scores: dict | None = None  # reserved column for v0.1 score backfill
    pushed_at: datetime | None = None
    push_slot: str | None = None
    first_seen: datetime | None = None  # filled by the store on save when absent
    raw: dict | None = None  # optional JSON payload
    read: bool = False       # G9 服务端读态(库列 0/1;新条目缺省 False)
    starred: bool = False    # 星标(策展;retention 剪枝不豁免,PRD Q4.2)
    later: bool = False      # 稍后读(同上)
    id: int | None = None


@dataclass(slots=True)
class DedupEntry:
    """One ``dedup_registry`` row: a seen key plus its last push info."""

    key: str
    first_seen: datetime
    last_pushed_at: datetime | None = None
    last_push_slot: str | None = None


@dataclass(slots=True)
class ChangeBaseline:
    """One ``change_baseline`` row: per-URL change fingerprint for fetch_base."""

    url: str
    etag: str | None = None
    last_modified: str | None = None
    content_hash: str | None = None
    last_changed: datetime | None = None


@dataclass(slots=True)
class EngineHint:
    """One ``engine_hints`` row: the engine that last succeeded for a source."""

    source_key: str
    engine: str
    updated_at: datetime


@dataclass(slots=True)
class MetricRecord:
    """One ``metric_history`` row: a category-level numeric snapshot.

    趋势基线的历史底座(PRD 10-01-v04-trend-baseline):条目级数值字段(如
    显卡 ``price``)按 ``(category, metric_key, field)`` 逐 run 存快照;品类
    级统计(关键词提及量)也走同一张表,约定 ``metric_key = "keyword:<词>"``、
    ``field = "mentions"``、值为该 run 的命中条目数。窗口对比
    (vs 昨日/上周)在查询时按 ``recorded_at`` 与本地日/ISO 周边界计算。
    """

    category: str
    metric_key: str  # 条目 dedup_key / url,或品类级约定键 keyword:<词>
    field: str  # 数值字段名(baseline.fields),或品类级 "mentions"
    value: float
    recorded_at: datetime | None = None  # filled by the store on save when absent
    id: int | None = None


@dataclass(slots=True)
class FeedbackRecord:
    """One ``feedback`` row: a good/bad verdict on a pushed item.

    ``item_id`` is the ``items.id`` association; ``dedup_key`` is stored
    redundantly (plus ``title`` / ``category`` snapshots) so per-word and
    per-category statistics keep working after retention prunes the item row
    itself. ``channel`` records which receiving path delivered the verdict
    (cli / telegram / feishu).
    """

    dedup_key: str
    verdict: str  # good | bad (FEEDBACK_VERDICTS)
    channel: str  # cli | telegram | feishu
    item_id: int | None = None
    title: str | None = None  # snapshot at feedback time (word stats)
    category: str | None = None  # snapshot at feedback time (category stats)
    #: provider event identity (TG update_id / Feishu event_id; NULL for CLI).
    #: Unique per (channel, external_id): 双击/平台重试/进程重启重放只记一次
    #: (幂等去重,防「一次点击凑满 min_bad_count」击穿护栏)。
    external_id: str | None = None
    created_at: datetime | None = None  # filled by the store on save when absent
    id: int | None = None


@dataclass(slots=True)
class TuningRecord:
    """One ``feedback_tuning`` row: an append-only parameter adjustment.

    Rows are never updated or deleted (调整历史可追溯); the active adjustment
    for a word/category is the newest matching row. ``payload`` is a
    JSON-serializable dict whose shape depends on ``kind``.
    """

    kind: str  # mute_weight | category_penalty | prompt_note
    payload: dict
    created_at: datetime | None = None  # filled by the store on save when absent
    id: int | None = None


@dataclass(slots=True)
class RunRecord:
    """One ``runs`` row: a pipeline execution record.

    ``steps`` carries per-step progress (断点续跑, v0.2 storage hardening):
    ``{step_name: {"status": ..., "completed_at": ..., "payload": ...}}``.
    Checkpoint payloads (fetched/classified/deduped items) let a rerun skip
    already-completed stages instead of re-fetching and re-classifying.
    """

    category: str
    started_at: datetime
    status: str
    finished_at: datetime | None = None
    stats: dict | None = None
    error: str | None = None
    steps: dict | None = None
    id: int | None = None
    #: 侧写日志身份(10-07-logs-restart-visibility R1):sidecar 会话级 run_id——
    #: JSONL 日志行的 run_id 即此值,跨重启「上一程」行展开 logs.tail 的对齐键。
    #: 旧行/独立 CLI 跑次 NULL(无法对齐,展示侧如实降级)。
    log_run_id: int | None = None


@dataclass(slots=True)
class AlertRule:
    """One ``alert_rules`` row: 情报流告警规则(条件 → 动作).

    纯存储记录(行 ↔ 对象互转,零校验):scope/when 白名单语法/action_config
    形状的构造期拒由 ``myssia.alerts.rule.compile_rule`` 统一承担——读库坏行
    WARNING 跳过(隔离)、写库(alerts.save)结构化拒整批,两路共用同一道门。
    ``when`` 字段名与 ``RouteRuleConfig.when`` 对齐;存储列名为 ``when_expr``
    (SQL 保留字规避)。``action_config`` 为 JSON 形态:push ``{channel,
    targets?, template?}`` / tag ``{tags: [..]}``。
    """

    name: str
    when: str
    action: str  # push | tag (ALERT_ACTIONS)
    action_config: dict = field(default_factory=dict)
    kind: str = ALERT_RULE_KIND_ITEM  # item | cron_stale (ALERT_RULE_KINDS)
    #: cron_stale 专属参数(JSON 列):{threshold_hours} 或 {auto: true};
    #: item 规则恒 None(构造门拒非 None,防误配)。
    params: dict | None = None
    scope: str = ALERT_SCOPE_GLOBAL  # 'global' | 品类 id(cron_stale 必须品类)
    enabled: bool = True
    created_at: datetime | None = None  # filled by the store on save when absent
    updated_at: datetime | None = None  # 落库侧每次 save 刷新
    id: int | None = None


@dataclass(slots=True)
class AlertFired:
    """One ``alert_fired`` row: one rule hit on one item (命中历史).

    ``rule_name`` / ``title`` / ``category`` / ``action`` are snapshots at
    fire time so the history stays readable after the rule is deleted or the
    item row is pruned by retention (FeedbackRecord 同款快照先例).
    ``dedup_key`` 是引擎侧已兜底的非空身份(item.dedup_key or item.url,
    digest.py 同款);``UNIQUE (rule_id, dedup_key)`` 是 fired 去重的
    at-most-once 门闩(record_fired 冲突返回 None)。
    """

    rule_id: int
    rule_name: str
    dedup_key: str
    action: str  # push | tag(命中时规则的动作快照)
    action_status: str = ALERT_STATUS_PENDING
    item_id: int | None = None
    title: str | None = None  # snapshot at fire time
    category: str | None = None  # snapshot at fire time
    created_at: datetime | None = None  # filled by the store on save when absent
    id: int | None = None
