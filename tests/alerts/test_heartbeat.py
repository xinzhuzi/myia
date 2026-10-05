"""cron 心跳告警(10-05-cron-heartbeat:kind=cron_stale 规则全链).

一个文件收拢本批测试面:

- store:v8→v9 迁移(旧库自动升级/既有行 kind 缺省 'item'/新库基线含两列)
  + kind/params 落库往返(INSERT/UPDATE 两路);
- 构造门:cron_stale 合法三形态(scope 钉品类/explicit/auto/job_id)与拒
  六形态(global/when≠true/params 形状/未知键/阈值二选一违例/item 带 params
  防误配/bad kind);
- 引擎 heartbeat_pass:久未成功触发 fire(文案含品类与时长)/同桶 UNIQUE
  冷却/新鲜静默/从未成功的规则年龄冷静期/恢复通知(同桶)+跨桶不重发/
  auto 阈值(2× 节奏+夹取)/auto 观测不足 WARNING 跳过/未落库规则跳过/
  push 动作按规则品类解析器(sent 与 degraded 两态,跨品类零借用)/
  item 规则不进心跳路径、cron_stale 规则不进条目路径(双向零漂移);
- 账本只读查询:last_completed_at(有/无成功/空 job 集)与
  completed_gap_hours(中位节奏/观测不足 None)。

全部零真实网络零真实等待;推送走注入假件。
"""

from __future__ import annotations

import asyncio
import sqlite3
from datetime import datetime, timedelta, timezone

import pytest

from myssia.alerts import AlertConfigError, AlertEngine, compile_rule
from myssia.alerts.engine import heartbeat_pass
from myssia.cron.executions import ExecutionLedger
from myssia.pipeline import Item
from myssia.push.base import SendReport
from myssia.store import AlertRule, SQLiteStore

NOW = datetime(2026, 10, 5, 12, 0, 0, tzinfo=timezone.utc)


def make_store(tmp_path) -> SQLiteStore:
    return SQLiteStore(tmp_path / "heartbeat.db")


def make_heartbeat_rule(**overrides) -> AlertRule:
    base = dict(
        name="ai-news 心跳", when="true", action="tag", action_config={"tags": ["hb"]},
        kind="cron_stale", params={"threshold_hours": 6}, scope="ai-news",
        created_at=NOW - timedelta(hours=30),
    )
    base.update(overrides)
    return AlertRule(**base)


def run(coro):
    return asyncio.run(coro)


# ---------------------------------------------------------------------------
# store:v8 → v9 迁移 + kind/params 往返
# ---------------------------------------------------------------------------

def _make_v8_database(path) -> None:
    """手工造一个 v8 形态的旧库(无 kind/params 列,schema_version=8)."""
    conn = sqlite3.connect(path)
    conn.execute("CREATE TABLE store_meta (key TEXT PRIMARY KEY, value TEXT NOT NULL)")
    conn.execute(
        """CREATE TABLE alert_rules (
             id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL,
             enabled INTEGER NOT NULL DEFAULT 1, scope TEXT NOT NULL DEFAULT 'global',
             when_expr TEXT NOT NULL, action TEXT NOT NULL, action_config TEXT NOT NULL,
             created_at TEXT NOT NULL, updated_at TEXT NOT NULL)"""
    )
    conn.execute(
        "INSERT INTO store_meta (key, value) VALUES ('schema_version', '8')"
    )
    conn.execute(
        "INSERT INTO alert_rules (name, when_expr, action, action_config,"
        " created_at, updated_at) VALUES ('旧规则', 'true', 'tag', '{\"tags\": [\"x\"]}',"
        " '2026-10-01T00:00:00+00:00', '2026-10-01T00:00:00+00:00')"
    )
    conn.commit()
    conn.close()


def test_migration_v8_to_v9_upgrades_existing_rules(tmp_path):
    db = tmp_path / "old.db"
    _make_v8_database(db)
    store = SQLiteStore(db)
    rules = store.list_alert_rules()
    assert len(rules) == 1
    assert rules[0].kind == "item"  # 既有行零漂移:缺省 kind
    assert rules[0].params is None
    columns = {
        row[1] for row in store.conn.execute("PRAGMA table_info(alert_rules)")
    }
    assert {"kind", "params"} <= columns


def test_heartbeat_rule_roundtrip_insert_and_update(tmp_path):
    store = make_store(tmp_path)
    saved = store.save_alert_rule(make_heartbeat_rule())
    assert saved.kind == "cron_stale" and saved.params == {"threshold_hours": 6}
    saved.params = {"auto": True}
    saved.scope = "freebie"
    updated = store.save_alert_rule(saved)  # UPDATE 路径
    assert updated.params == {"auto": True} and updated.scope == "freebie"
    assert updated.kind == "cron_stale"


# ---------------------------------------------------------------------------
# 构造门:cron_stale 形态
# ---------------------------------------------------------------------------

def test_compile_accepts_three_legal_forms():
    compile_rule(make_heartbeat_rule())  # explicit
    compile_rule(make_heartbeat_rule(params={"auto": True}))  # auto
    compile_rule(make_heartbeat_rule(params={"threshold_hours": 4, "job_id": "j-1"}))


@pytest.mark.parametrize(
    "overrides",
    [
        dict(scope="global"),                                   # 心跳必须钉品类
        dict(when="score > 3"),                                 # when 恒占位 true
        dict(params=None),                                      # params 必须是映射
        dict(params={"threshold_hours": 6, "nope": 1}),         # 未知键
        dict(params={"threshold_hours": 6, "auto": True}),      # 阈值二选一
        dict(params={}),                                        # 阈值必须给一个
        dict(params={"threshold_hours": -1}),                   # 正数
        dict(params={"threshold_hours": True}),                 # bool 非数
        dict(params={"auto": True, "job_id": ""}),              # job_id 非空
    ],
)
def test_compile_rejects_bad_cron_stale_shapes(overrides):
    with pytest.raises(AlertConfigError):
        compile_rule(make_heartbeat_rule(**overrides))


def test_compile_rejects_item_rule_with_params_and_bad_kind():
    with pytest.raises(AlertConfigError, match="params 仅 cron_stale"):
        compile_rule(AlertRule(
            name="x", when="true", action="tag", action_config={"tags": ["t"]},
            params={"auto": True},
        ))
    with pytest.raises(AlertConfigError, match="kind"):
        compile_rule(AlertRule(
            name="x", when="true", action="tag", action_config={"tags": ["t"]},
            kind="webhook",
        ))


# ---------------------------------------------------------------------------
# heartbeat_pass 语义
# ---------------------------------------------------------------------------

def test_fires_when_never_succeeded_past_grace_period(tmp_path):
    store = make_store(tmp_path)
    rule = store.save_alert_rule(make_heartbeat_rule())  # 规则年龄 30h > 6h
    fired = run(heartbeat_pass(store, [rule], last_success_at=lambda c: None, now=NOW))
    assert len(fired) == 1
    assert "ai-news" in fired[0].title and "30" in fired[0].title
    assert fired[0].action_status == "tagged"
    assert fired[0].dedup_key.startswith("cron-stale:ai-news:")


def test_cooldown_same_bucket_is_at_most_once(tmp_path):
    store = make_store(tmp_path)
    rule = store.save_alert_rule(make_heartbeat_rule())
    run(heartbeat_pass(store, [rule], last_success_at=lambda c: None, now=NOW))
    fired_again = run(heartbeat_pass(store, [rule], last_success_at=lambda c: None, now=NOW))
    assert fired_again == []  # UNIQUE 门闩 = 每桶一条


def test_fresh_category_stays_silent(tmp_path):
    store = make_store(tmp_path)
    rule = store.save_alert_rule(make_heartbeat_rule())
    fired = run(heartbeat_pass(store, [rule], last_success_at=lambda c: NOW, now=NOW))
    assert fired == []


def test_young_rule_without_history_waitGrace(tmp_path):
    store = make_store(tmp_path)
    rule = store.save_alert_rule(make_heartbeat_rule(created_at=NOW - timedelta(hours=2)))
    fired = run(heartbeat_pass(store, [rule], last_success_at=lambda c: None, now=NOW))
    assert fired == []  # 冷静期:规则年龄 2h < 阈值 6h


def test_stale_then_recovered_notifies_once_per_incident(tmp_path):
    store = make_store(tmp_path)
    rule = store.save_alert_rule(make_heartbeat_rule())
    run(heartbeat_pass(store, [rule], last_success_at=lambda c: None, now=NOW))
    recovered = run(heartbeat_pass(store, [rule], last_success_at=lambda c: NOW, now=NOW))
    assert len(recovered) == 1 and "恢复" in recovered[0].title
    again = run(heartbeat_pass(store, [rule], last_success_at=lambda c: NOW, now=NOW + timedelta(hours=1)))
    assert again == []  # 同事故不重发(近两桶恢复行在场即压制)


def test_auto_threshold_uses_doubled_cadence_and_skips_without_observation(tmp_path, caplog):
    store = make_store(tmp_path)
    rule = store.save_alert_rule(make_heartbeat_rule(params={"auto": True}, scope="server"))
    fired = run(heartbeat_pass(
        store, [rule], last_success_at=lambda c: None, now=NOW,
        cadence_hours=lambda c: 10 if c == "server" else None,
    ))
    assert len(fired) == 1  # 2×10=20h,规则年龄 30h > 20h
    with caplog.at_level("WARNING"):
        skipped = run(heartbeat_pass(
            store, [rule], last_success_at=lambda c: None, now=NOW, cadence_hours=lambda c: None,
        ))
    assert skipped == [] and any("观测不足" in r.message for r in caplog.records)


def test_unsaved_rule_is_skipped_with_warning(tmp_path):
    store = make_store(tmp_path)
    fired = run(heartbeat_pass(store, [make_heartbeat_rule()], last_success_at=lambda c: None, now=NOW))
    assert fired == []  # 无 id 无法占坑:跳过不猜


def test_push_action_resolves_channel_for_rule_category(tmp_path):
    store = make_store(tmp_path)
    rule = store.save_alert_rule(make_heartbeat_rule(
        action="push", action_config={"channel": "stdout"},
    ))
    seen: list[str] = []

    async def fake_send(items, **kwargs):
        seen.append(kwargs.get("category"))
        return [SendReport(channel="stdout", ok=True, item_count=1)]

    fired = run(heartbeat_pass(
        store, [rule], last_success_at=lambda c: None, now=NOW,
        channel_resolver_for=lambda category: (seen.append(f"resolve:{category}") or object()),
        send=fake_send,
    ))
    assert len(fired) == 1 and fired[0].action_status == "sent"
    assert "resolve:ai-news" in seen and seen[-1] == "ai-news"  # 按规则品类解析


def test_push_action_degrades_without_channel_for_rule_category(tmp_path):
    store = make_store(tmp_path)
    rule = store.save_alert_rule(make_heartbeat_rule(
        action="push", action_config={"channel": "telegram"},
    ))
    fired = run(heartbeat_pass(
        store, [rule], last_success_at=lambda c: None, now=NOW,
        channel_resolver_for=lambda category: None,
    ))
    assert fired[0].action_status == "degraded_no_channel"


def test_item_rules_ignored_by_heartbeat_and_cron_stale_ignored_by_item_pass(tmp_path):
    store = make_store(tmp_path)
    heartbeat_rule = store.save_alert_rule(make_heartbeat_rule())
    item_rule = store.save_alert_rule(AlertRule(
        name="条目规则", when="'快讯' in title", action="tag",
        action_config={"tags": ["flash"]}, scope="ai-news",
    ))
    # 心跳路径只吃 cron_stale
    fired = run(heartbeat_pass(
        store, [heartbeat_rule, item_rule], last_success_at=lambda c: NOW, now=NOW,
    ))
    assert fired == []
    # 条目路径只吃 item(run_pass 对 cron_stale 零求值)
    item = Item(url="https://example.org/a", title="快讯:某事", category="ai-news")
    item.dedup_key = "k-1"
    engine = AlertEngine(store=store)
    rows = run(engine.run_pass([item], [heartbeat_rule, item_rule]))
    assert len(rows) == 1 and rows[0].rule_name == "条目规则"


# ---------------------------------------------------------------------------
# 账本只读查询
# ---------------------------------------------------------------------------

def _seed_ledger(tmp_path, completions: list[int]) -> ExecutionLedger:
    ledger = ExecutionLedger(tmp_path / "cron-root")
    for hours_ago in completions:
        record = ledger.create_execution("job-1", source="tick")
        ledger.finish_execution(record["id"], success=True)
        # 把 finished_at 回拨到目标时刻(账本 API 不接受自定义时刻,测试直改)
        with ledger.transaction() as conn:
            conn.execute(
                "UPDATE executions SET finished_at = ? WHERE id = ?",
                ((NOW - timedelta(hours=hours_ago)).isoformat(), record["id"]),
            )
    return ledger


def test_ledger_last_completed_and_gap(tmp_path):
    ledger = _seed_ledger(tmp_path, completions=[1, 5, 9, 13])  # 等距 4h × 3 段
    assert ledger.last_completed_at(["job-1"]) is not None
    assert ledger.completed_gap_hours(["job-1"]) == pytest.approx(4.0)
    assert ledger.last_completed_at(["job-other"]) is None
    assert ledger.completed_gap_hours([]) is None


def test_ledger_gap_needs_two_completions(tmp_path):
    ledger = _seed_ledger(tmp_path, completions=[2])
    assert ledger.completed_gap_hours(["job-1"]) is None
