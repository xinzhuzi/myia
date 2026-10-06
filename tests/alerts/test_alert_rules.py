"""Alert rules core(10-04-alert-rules design §11 的 store/引擎/管线行).

一个文件收拢本批 Python 侧核心的测试面:

- store:v6→v7 迁移(旧库自动升级/幂等重放/新库基线/降级打开拒);两表
  CRUD;record_fired UNIQUE 占坑冲突;fired_counts 派生;update_item_tags
  回写;delete_rule 不删 fired;
- 引擎:构造期拒全形态(属性访问/下标/lambda/超长/bad action/scope/
  config 形状);``9**9**9`` 资源护栏;alert_view 含 content(view 零波及
  回归);score=None 隔离;mute 硬规则;scope 钉品类;push 动作三态
  (sent/send_failed/degraded_no_channel);tag 两步回写;双向压制两方向;
  占坑 at-most-once;
- 管线:零规则零惊扰;dry-run 短路;broken(result.items=[])跳过;真发/
  降级/tag 回写全链;反馈 0.0 权重词并入 mute;附加步失败不改 run 终态。

全部零真实网络(httpx.MockTransport)与零真实等待;发送路径注入假件或
RecordingChannel 同款通道替身。
"""

from __future__ import annotations

import asyncio
import sqlite3
from datetime import datetime, timedelta, timezone
from typing import Any

import httpx
import pytest

import myssia.pipeline as pipeline_module
from myssia.alerts import (
    ALERT_SCOPES,
    AlertConfigError,
    AlertEngine,
    alert_view,
    compile_rule,
    compile_rules,
)
from myssia.dedup import DedupRegistry
from myssia.pipeline import Item, Pipeline
from myssia.push.base import SendReport
from myssia.push.digest import DigestAggregator
from myssia.schema import load_category
from myssia.store import (
    SCHEMA_VERSION,
    AlertFired,
    AlertRule,
    SQLiteStore,
    StoreSchemaError,
)

TIMEZONE = "Asia/Shanghai"


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def make_store(tmp_path) -> SQLiteStore:
    return SQLiteStore(tmp_path / "alerts.db")


def push_rule(name: str = "告警", when: str = "title", **overrides: Any) -> AlertRule:
    data: dict[str, Any] = dict(
        name=name, when=when, action="push", action_config={"channel": "stdout"}
    )
    data.update(overrides)
    return AlertRule(**data)


def tag_rule(name: str = "打标", when: str = "title", **overrides: Any) -> AlertRule:
    data: dict[str, Any] = dict(
        name=name, when=when, action="tag", action_config={"tags": ["watch"]}
    )
    data.update(overrides)
    return AlertRule(**data)


def make_item(title: str = "X公司完成新一轮融资", **overrides: Any) -> Item:
    data: dict[str, Any] = dict(
        url="https://api.demo.local/a",
        title=title,
        source="demo",
        category="freebie",
        dedup_key="key-a",
        metadata={},
    )
    data.update(overrides)
    return Item(**data)


class FakeChannel:
    """send_immediate 的通道假件:记录调用,可脚本化失败."""

    def __init__(self, name: str = "stdout", fail: bool = False) -> None:
        self.name = name
        self.fail = fail
        self.calls: list[dict[str, Any]] = []

    async def send(self, items, context) -> None:
        self.calls.append({"items": list(items), "context": context})
        if self.fail:
            from myssia.push import PushSendError

            raise PushSendError("http_error", "模拟通道故障")


def ok_send(calls: list[Any]):
    """假发送函数:记录调用并返回一份成功报告(send_immediate 同形)."""

    async def _send(*args: Any, **kwargs: Any) -> list[SendReport]:
        calls.append({"args": args, "kwargs": kwargs})
        return [SendReport("stdout", ok=True, item_count=1)]

    return _send


def failing_send(calls: list[Any]):
    """假发送函数:返回一份失败报告."""

    async def _send(*args: Any, **kwargs: Any) -> list[SendReport]:
        calls.append({"args": args, "kwargs": kwargs})
        return [SendReport("stdout", ok=False, item_count=1, error="[http_error] 模拟")]

    return _send


# ---------------------------------------------------------------------------
# Store:迁移与两表契约(design §2 / §11 store 行)
# ---------------------------------------------------------------------------


def test_fresh_database_baseline_has_both_tables_unseeded(tmp_path):
    """新库基线:两表两索引齐、不 seed(零惊扰:空表即合法态)."""
    store = make_store(tmp_path)
    names = {
        row[0]
        for row in store.conn.execute(
            "SELECT name FROM sqlite_master WHERE type IN ('table', 'index')"
        )
    }
    assert {"alert_rules", "alert_fired", "idx_alert_fired_created"} <= names
    assert store.list_alert_rules() == []
    assert store.list_fired() == []
    # 版本钉死跟随符号:字面 "9" 已随 v10(runs.log_run_id;
    # 10-07-logs-restart-visibility)过期,不再双等字面量。
    assert store.get_meta("schema_version") == str(SCHEMA_VERSION)
    store.close()


def test_v6_database_upgrades_to_current_idempotent_zero_data_migration(tmp_path):
    """旧 v6 库打开自动升级;幂等重放;既有表与行零触碰."""
    path = tmp_path / "v6.db"
    store = SQLiteStore(path)
    marker = store.save_item(
        __import__("myssia.store", fromlist=["ItemRecord"]).ItemRecord(
            url="https://x/m", dedup_key="marker", title="既有行零触碰"
        )
    )
    # 伪造 v6 形态:版本戳回拨 + 摘除两表(等效于 v6 库从未有过它们)。
    store.conn.execute("DROP INDEX IF EXISTS idx_alert_fired_created")
    store.conn.execute("DROP TABLE IF EXISTS alert_fired")
    store.conn.execute("DROP TABLE IF EXISTS alert_rules")
    store.conn.execute("UPDATE store_meta SET value = '6' WHERE key = 'schema_version'")
    store.conn.commit()
    store.close()

    reopened = SQLiteStore(path)  # 打开即自动迁移
    assert reopened.get_meta("schema_version") == str(SCHEMA_VERSION)  # v10 起非字面 "9"
    tables = {
        row[0]
        for row in reopened.conn.execute(
            "SELECT name FROM sqlite_master WHERE type = 'table'"
        )
    }
    assert {"alert_rules", "alert_fired"} <= tables
    assert reopened.get_item(marker).title == "既有行零触碰"  # 零数据迁移
    rule = reopened.save_alert_rule(push_rule())
    assert rule.id is not None

    reopened.conn.execute(
        "UPDATE store_meta SET value = '6' WHERE key = 'schema_version'"
    )
    reopened.conn.commit()
    reopened.close()
    again = SQLiteStore(path)  # 幂等重放:已有形状上再放一遍迁移
    assert again.get_meta("schema_version") == str(SCHEMA_VERSION)  # v10 起非字面 "9"
    assert [r.name for r in again.list_alert_rules()] == ["告警"]  # 数据存活
    again.close()


def test_newer_schema_version_refused(tmp_path):
    """v8 库被旧版本打开 → 既有「不要降级打开新库」护栏直拦."""
    path = tmp_path / "future.db"
    store = SQLiteStore(path)
    store.conn.execute(
        "UPDATE store_meta SET value = ? WHERE key = 'schema_version'",
        (str(SCHEMA_VERSION + 1),),
    )
    store.conn.commit()
    store.close()
    with pytest.raises(StoreSchemaError) as excinfo:
        SQLiteStore(path)
    assert excinfo.value.code == "schema_version_newer"
    assert "不要降级打开新库" in str(excinfo.value)


def test_save_list_delete_alert_rule_roundtrip(tmp_path):
    store = make_store(tmp_path)
    first = store.save_alert_rule(push_rule(name="一"))
    second = store.save_alert_rule(tag_rule(name="二", enabled=False))
    assert (first.id, second.id) == (1, 2)
    assert first.created_at is not None and first.updated_at is not None

    renamed = store.save_alert_rule(
        push_rule(name="一改", id=first.id)  # 带 id = UPDATE 保 id
    )
    assert renamed.id == first.id and renamed.name == "一改"
    assert renamed.updated_at >= first.updated_at  # 落库侧刷新
    assert renamed.created_at == first.created_at  # created_at 不随 UPDATE 改

    assert [(r.id, r.name, r.enabled) for r in store.list_alert_rules()] == [
        (1, "一改", True),
        (2, "二", False),
    ]
    assert [r.id for r in store.list_alert_rules(enabled=True)] == [1]
    assert [r.id for r in store.list_alert_rules(enabled=False)] == [2]

    assert store.delete_alert_rule(second.id) is True
    assert store.delete_alert_rule(second.id) is False  # 不存在返回 False
    assert [r.id for r in store.list_alert_rules()] == [1]

    with pytest.raises(ValueError, match="alert_rules 记录不存在"):
        store.save_alert_rule(push_rule(id=999))
    with pytest.raises(ValueError, match="name 不能为空"):
        store.save_alert_rule(push_rule(name=""))
    with pytest.raises(ValueError, match="action 必须是"):
        store.save_alert_rule(push_rule(action="sms", action_config={}))
    store.close()


def test_record_fired_unique_gate_and_status_backfill(tmp_path):
    """占坑门闩:UNIQUE(rule_id, dedup_key) 冲突返 None;状态回填契约."""
    store = make_store(tmp_path)
    rule = store.save_alert_rule(push_rule())

    fired = store.record_fired(
        AlertFired(
            rule_id=rule.id,
            rule_name=rule.name,
            dedup_key="k1",
            action="push",
            item_id=7,
            title="快照标题",
            category="freebie",
        )
    )
    assert fired is not None and fired.id is not None
    assert fired.action_status == "pending"

    dup = store.record_fired(
        AlertFired(rule_id=rule.id, rule_name=rule.name, dedup_key="k1", action="push")
    )
    assert dup is None  # 同规则同 key:UNIQUE 拦截
    other_key = store.record_fired(
        AlertFired(rule_id=rule.id, rule_name=rule.name, dedup_key="k2", action="push")
    )
    assert other_key is not None  # 同规则不同 key:放行

    store.mark_alert_fired_status(fired.id, "sent")
    assert store.list_fired(limit=10)[1].action_status == "sent"  # k1 行(id 小)
    with pytest.raises(ValueError, match="action_status 必须是"):
        store.mark_alert_fired_status(fired.id, "exploded")
    with pytest.raises(ValueError, match="alert_fired 记录不存在"):
        store.mark_alert_fired_status(999, "sent")

    assert store.has_fired(rule.id, "k1") is True
    assert store.has_fired(rule.id, "missing") is False
    with pytest.raises(ValueError, match="dedup_key 不能为空"):
        store.has_fired(rule.id, "")
    with pytest.raises(ValueError, match="dedup_key 不能为空"):
        store.record_fired(
            AlertFired(rule_id=1, rule_name="x", dedup_key="", action="push")
        )
    store.close()


def test_list_fired_newest_first_since_filter_limit_clamp(tmp_path):
    store = make_store(tmp_path)
    rule = store.save_alert_rule(push_rule())
    base = datetime(2026, 10, 4, 12, 0, tzinfo=timezone.utc)
    for index in range(205):
        store.record_fired(
            AlertFired(
                rule_id=rule.id,
                rule_name=rule.name,
                dedup_key=f"k{index:03d}",
                action="push",
                created_at=base + timedelta(seconds=index),
            )
        )
    newest = store.list_fired()
    assert len(newest) == 100  # 缺省 100
    assert newest[0].dedup_key == "k204"  # 新→旧
    assert newest[-1].dedup_key == "k105"

    assert len(store.list_fired(limit=0)) == 1  # 钳制下界 [1, 200]
    assert len(store.list_fired(limit=999)) == 200  # 钳制上界

    since = base + timedelta(seconds=203)
    fresh = store.list_fired(since=since, limit=10)
    assert [row.dedup_key for row in fresh] == ["k204", "k203"]  # >= 语义含边界

    only_first = store.list_fired(rule_id=rule.id, limit=5)
    assert len(only_first) == 5
    assert store.list_fired(rule_id=4242) == []  # 无命中规则过滤为空
    store.close()


def test_fired_counts_derivation_and_delete_keeps_history(tmp_path):
    """计数由 alert_fired COUNT 派生;删规则不删 fired(命中历史是事实)."""
    store = make_store(tmp_path)
    rule_a = store.save_alert_rule(push_rule(name="A"))
    rule_b = store.save_alert_rule(tag_rule(name="B"))
    for key in ("k1", "k2"):
        store.record_fired(
            AlertFired(rule_id=rule_a.id, rule_name="A", dedup_key=key, action="push")
        )
    store.record_fired(
        AlertFired(rule_id=rule_b.id, rule_name="B", dedup_key="k1", action="tag")
    )
    assert store.fired_counts() == {rule_a.id: 2, rule_b.id: 1}

    assert store.delete_alert_rule(rule_a.id) is True
    assert store.fired_counts() == {rule_a.id: 2, rule_b.id: 1}  # 历史照留
    survivors = store.list_fired(rule_id=rule_a.id)
    assert len(survivors) == 2 and survivors[0].rule_name == "A"  # 快照可读
    store.close()


def test_update_item_tags_writeback(tmp_path):
    store = make_store(tmp_path)
    from myssia.store import ItemRecord

    store.save_item(
        ItemRecord(url="https://x/a", dedup_key="k1", title="T", tags=["old"])
    )
    assert store.update_item_tags(dedup_key="k1", tags=["old", "watch"]) is True
    row = store.get_item_by_dedup_key("k1")
    assert row.tags == ["old", "watch"]  # JSON 数组列回写
    assert store.update_item_tags(dedup_key="gone", tags=["x"]) is False  # 行不存在
    with pytest.raises(ValueError, match="dedup_key 不能为空"):
        store.update_item_tags(dedup_key="", tags=[])
    store.close()


# ---------------------------------------------------------------------------
# 引擎:构造期拒 / 求值上下文 / 护栏(design §5 / §11 引擎行)
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    ("rule", "fragment"),
    [
        (push_rule(name="  "), "name 不能为空"),
        (push_rule(scope="unknown-scope"), "scope 必须是"),
        (push_rule(action="sms", action_config={}), "action 必须是"),
        (push_rule(when="title.lower"), "when_expr 无效"),  # 属性访问
        (push_rule(when="scores['x'] >= 1"), "when_expr 无效"),  # 下标
        (push_rule(when="(lambda: True)()"), "when_expr 无效"),  # lambda
        (push_rule(when="a" * 1001), "when_expr 无效"),  # 超 1000 字符
        (push_rule(when=""), "when_expr 无效"),
        (push_rule(action_config={}), "channel 必须是"),  # push 缺 channel
        (push_rule(action_config={"channel": "nope"}), "channel 必须是"),
        (
            push_rule(action_config={"channel": "stdout", "targets": "feishu:x"}),
            "targets",
        ),
        (push_rule(action_config={"channel": "stdout", "extra": 1}), "未知键"),
        (tag_rule(action_config={}), "tags 必须"),  # tag 缺 tags
        (tag_rule(action_config={"tags": []}), "tags 必须"),  # 空列表
        (tag_rule(action_config={"tags": ["a", 2]}), "tags 必须"),
        (tag_rule(action_config={"tags": ["a"], "channel": "stdout"}), "未知键"),
    ],
)
def test_compile_rejects_all_invalid_shapes(rule: AlertRule, fragment: str):
    with pytest.raises(AlertConfigError) as excinfo:
        compile_rule(rule)
    assert "字段校验失败" in str(excinfo.value)
    assert fragment in str(excinfo.value)


def test_compile_accepts_known_shapes_and_scope_vocabulary():
    compiled = compile_rule(push_rule(when="'融资' in title and score >= 4"))
    assert compiled.channel == "stdout" and compiled.evaluator is not None
    compiled_tag = compile_rule(tag_rule(action_config={"tags": ["a", "b"]}))
    assert compiled_tag.tags == ["a", "b"]
    assert ALERT_SCOPES == frozenset(
        {
            "global",
            "freebie",
            "proxy-node",
            "buying-agent",
            "ai-news",
            "server",
            "token",
            "credit-card",
            "channel",
        }
    )


def test_compile_rules_skips_bad_rows_isolated(caplog):
    """读库坏行 = 单行 WARNING 跳过,好行照常编译(不 break 批)."""
    good = push_rule(name="好")
    bad = push_rule(name="坏", when="title.lower")
    with caplog.at_level("WARNING", logger="myssia.alerts.rule"):
        compiled = compile_rules([good, bad])
    assert len(compiled) == 1 and compiled[0].name == "好"
    assert any("告警规则拒载" in record.message for record in caplog.records)


def test_alert_view_content_patch_and_view_zero_impact():
    """alert_view = view() + content;Item.view() 本体零波及(route 原样绿)."""
    item = make_item(content="正文提到融资", metadata={"score": 4, "symbol": "X"})
    view = alert_view(item)
    assert view["content"] == "正文提到融资"
    assert view["score"] == 4 and view["symbol"] == "X"  # metadata 平铺照旧
    assert view["url"] == item.url and view["category"] == "freebie"
    raw = item.view()
    assert "content" not in raw  # 补丁只在告警侧,route 共享 view 不变
    assert alert_view(item)["content"] == "正文提到融资"  # view() 每次新 dict


def test_resource_guard_pow_expression_never_hangs(tmp_path):
    """``9**9**9``:文法合法装载,求值被资源护栏拦截 → WARNING 未命中,不挂死."""
    store = make_store(tmp_path)
    rule = store.save_alert_rule(push_rule(name="炸药", when="9**9**9 or title"))
    engine = AlertEngine(store=store, channel_resolver=lambda _: None)
    fired = asyncio.run(engine.run_pass([make_item()], [rule]))
    assert fired == []  # 求值错 = 未命中(隔离),不落 fired
    assert store.list_fired() == []
    store.close()


def test_score_none_isolation(tmp_path):
    """enrich 未启用 score=None:``score >= 4`` 比较 TypeError → 未命中隔离."""
    store = make_store(tmp_path)
    rule = store.save_alert_rule(push_rule(name="阈值", when="score >= 4"))
    engine = AlertEngine(store=store)
    fired = asyncio.run(engine.run_pass([make_item(metadata={})], [rule]))
    assert fired == []
    with_score = make_item(metadata={"score": 4})
    fired2 = asyncio.run(AlertEngine(store=store).run_pass([with_score], [rule]))
    assert len(fired2) == 1  # 对照:有 score 时同一规则命中
    store.close()


def test_mute_hard_rule_skips_all_rules_without_fired(tmp_path):
    """mute 硬规则:title 子串命中 → 跳过全部规则求值,不落 fired(不读
    metadata['muted'],与品类 enrich 开关解耦)."""
    store = make_store(tmp_path)
    rules = [
        store.save_alert_rule(push_rule(name="一")),
        store.save_alert_rule(tag_rule(name="二")),
    ]
    engine = AlertEngine(store=store, mute_words=["广告"])
    muted_item = make_item(title="限时广告特价", metadata={"muted": False})
    fired = asyncio.run(engine.run_pass([muted_item], rules))
    assert fired == [] and store.list_fired() == []

    normal = make_item(title="无敏感词标题")
    fired2 = asyncio.run(engine.run_pass([normal], rules))
    assert len(fired2) == 2  # 两条规则都命中(不同 rule_id 各占一坑)
    store.close()


def test_scope_pins_category(tmp_path):
    store = make_store(tmp_path)
    scoped = store.save_alert_rule(tag_rule(name="只看羊毛", scope="freebie"))
    engine = AlertEngine(store=store)
    asyncio.run(engine.run_pass([make_item(category="server")], [scoped]))
    assert store.list_fired() == []  # 非本品类不求值
    asyncio.run(
        AlertEngine(store=store).run_pass(
            [
                make_item(
                    url="https://api.demo.local/b",
                    dedup_key="key-b",
                    category="freebie",
                )
            ],
            [scoped],
        )
    )
    assert len(store.list_fired()) == 1  # 本品类命中
    store.close()


def test_dedup_key_falls_back_to_url(tmp_path):
    store = make_store(tmp_path)
    rule = store.save_alert_rule(tag_rule())
    engine = AlertEngine(store=store)
    fired = asyncio.run(engine.run_pass([make_item(dedup_key=None)], [rule]))
    assert [row.dedup_key for row in fired] == ["https://api.demo.local/a"]
    store.close()


# ---------------------------------------------------------------------------
# 引擎:动作执行(push 三态 / tag 两步 / 双向压制 / at-most-once)
# ---------------------------------------------------------------------------


def test_push_action_sent(tmp_path):
    store = make_store(tmp_path)
    rule = store.save_alert_rule(push_rule())
    calls: list[Any] = []
    channel = FakeChannel()
    engine = AlertEngine(
        store=store,
        channel_resolver=lambda name: channel if name == "stdout" else None,
        send=ok_send(calls),
    )
    fired = asyncio.run(engine.run_pass([make_item()], [rule]))
    assert [row.action_status for row in fired] == ["sent"]
    assert store.list_fired()[0].action_status == "sent"  # 终态回填落库
    assert len(calls) == 1
    kwargs = calls[0]["kwargs"]
    assert kwargs["channels"] == [channel]
    assert kwargs["item_specs"] == [None]  # 无 targets → legacy 路径
    store.close()


def test_push_action_passes_rule_targets(tmp_path):
    store = make_store(tmp_path)
    rule = store.save_alert_rule(
        push_rule(action_config={"channel": "stdout", "targets": ["feishu:群A"]})
    )
    calls: list[Any] = []
    engine = AlertEngine(
        store=store, channel_resolver=lambda _: FakeChannel(), send=ok_send(calls)
    )
    asyncio.run(engine.run_pass([make_item()], [rule]))
    assert calls[0]["kwargs"]["item_specs"] == [["feishu:群A"]]
    store.close()


def test_push_action_send_failed(tmp_path):
    store = make_store(tmp_path)
    rule = store.save_alert_rule(push_rule())
    calls: list[Any] = []
    engine = AlertEngine(
        store=store, channel_resolver=lambda _: FakeChannel(), send=failing_send(calls)
    )
    fired = asyncio.run(engine.run_pass([make_item()], [rule]))
    assert [row.action_status for row in fired] == ["send_failed"]
    store.close()


def test_push_action_degraded_no_channel_without_resolver_call(tmp_path, caplog):
    """品类未配该类型 = 降级 WARNING + fired 记录不发,发送函数零调用."""
    store = make_store(tmp_path)
    rule = store.save_alert_rule(push_rule(action_config={"channel": "telegram"}))
    calls: list[Any] = []

    def resolver(name: str):
        assert name == "telegram"
        return None  # 当前品类 push[] 无 telegram

    engine = AlertEngine(store=store, channel_resolver=resolver, send=ok_send(calls))
    with caplog.at_level("WARNING", logger="myssia.alerts.engine"):
        fired = asyncio.run(engine.run_pass([make_item()], [rule]))
    assert [row.action_status for row in fired] == ["degraded_no_channel"]
    assert calls == []  # 未发送
    assert any("降级" in record.message for record in caplog.records)
    store.close()


def test_tag_action_two_step_writeback(tmp_path):
    """tag 两步:内存 add_tags(保序去重)+ items.tags 回写,状态 tagged."""
    from myssia.store import ItemRecord

    store = make_store(tmp_path)
    store.save_item(
        ItemRecord(
            url="https://api.demo.local/a", dedup_key="key-a", title="T", tags=["old"]
        )
    )
    rule = store.save_alert_rule(
        tag_rule(action_config={"tags": ["watch", "old", "fin"]})  # old 已在 → 去重
    )
    engine = AlertEngine(store=store)
    fired = asyncio.run(
        engine.run_pass([make_item(metadata={"tags": ["old"]})], [rule])
    )
    assert [row.action_status for row in fired] == ["tagged"]
    assert store.get_item_by_dedup_key("key-a").tags == ["old", "watch", "fin"]
    store.close()


def test_tag_writeback_missing_row_warns_but_statuses_tagged(tmp_path, caplog):
    """items 行已被剪枝:回写 False → WARNING;动作已执行,状态如实 tagged."""
    store = make_store(tmp_path)
    rule = store.save_alert_rule(tag_rule())
    with caplog.at_level("WARNING", logger="myssia.alerts.engine"):
        fired = asyncio.run(
            AlertEngine(store=store).run_pass([make_item(dedup_key="pruned")], [rule])
        )
    assert [row.action_status for row in fired] == ["tagged"]
    assert any("回写未命中" in record.message for record in caplog.records)
    store.close()


def test_at_most_once_second_pass_skips_action(tmp_path):
    """重跑再评估同批条目:UNIQUE 占坑拦住,动作只执行一次(崩溃窗口同款)."""
    store = make_store(tmp_path)
    rule = store.save_alert_rule(push_rule())
    calls: list[Any] = []
    engine = AlertEngine(
        store=store, channel_resolver=lambda _: FakeChannel(), send=ok_send(calls)
    )
    first = asyncio.run(engine.run_pass([make_item()], [rule]))
    second = asyncio.run(engine.run_pass([make_item()], [rule]))
    assert len(first) == 1 and second == []
    assert len(calls) == 1  # 第二轮占坑失败,不重发
    assert store.fired_counts() == {rule.id: 1}
    store.close()


def test_bidirectional_suppression_route_first(tmp_path):
    """方向①:route immediate 先发(占住槽位)→ 告警 send_immediate 被拦."""
    store = make_store(tmp_path)
    rule = store.save_alert_rule(push_rule())
    channel = FakeChannel()
    registry = DedupRegistry(store)
    item = make_item()
    registry.record_push("key-a")  # route immediate 已在本槽位发过
    engine = AlertEngine(
        store=store,
        channel_resolver=lambda _: channel,
        registry=registry,
    )
    fired = asyncio.run(engine.run_pass([item], [rule]))
    assert [row.action_status for row in fired] == ["send_failed"]  # 未送达(§7.1 字面)
    assert channel.calls == []  # send_immediate 内部 should_send 拦截,通道零调用
    store.close()


def test_bidirectional_suppression_alert_first_blocks_digest(tmp_path):
    """方向②:告警先发(登记槽位)→ 同注册表的 digest flush 被拦."""
    store = make_store(tmp_path)
    rule = store.save_alert_rule(push_rule())
    channel = FakeChannel()
    registry = DedupRegistry(store)
    engine = AlertEngine(
        store=store,
        channel_resolver=lambda _: channel,
        registry=registry,
    )
    fired = asyncio.run(engine.run_pass([make_item()], [rule]))
    assert [row.action_status for row in fired] == ["sent"]
    assert len(channel.calls) == 1  # 告警真实发出并 record_push

    aggregator = DigestAggregator(channels=[channel], registry=registry)
    aggregator.add(make_item(), dedup_key="key-a")
    reports = asyncio.run(aggregator.flush())
    assert reports == []  # 同槽位拦截:摘要零发送
    store.close()


# ---------------------------------------------------------------------------
# 管线挂点(design §6 / §11 管线行)
# ---------------------------------------------------------------------------


def make_config(**overrides: Any):
    data: dict[str, Any] = {
        "id": "demo",
        "name": "演示品类",
        "schedule": "0 9 * * *",
        "timezone": TIMEZONE,
        "sources": [
            {
                "name": "api",
                "engine": "direct_api",
                "url": "https://api.demo.local/list",
                "extract": {
                    "type": "json_path",
                    "fields": {"title": "$[*].title", "url": "$[*].url"},
                },
            }
        ],
        "push": [{"channel": "stdout"}],
    }
    data.update(overrides)
    return load_category(data)


def make_handler(payloads: Any):
    def handler(request: httpx.Request) -> httpx.Response:
        if request.url.path == "/robots.txt":
            return httpx.Response(404, text="")
        return httpx.Response(200, json=payloads)

    return handler


def make_pipeline(config, *, handler: Any, store: SQLiteStore, **kwargs: Any):
    client = httpx.AsyncClient(transport=httpx.MockTransport(handler))
    return Pipeline(config, store=store, client=client, **kwargs)


class EngineSpy:
    """AlertEngine 替身:记录构造与 run_pass 载荷,行为同真件(薄包装)."""

    instances: list["EngineSpy"] = []
    real_cls = AlertEngine

    def __init__(self, **kwargs: Any) -> None:
        self.kwargs = kwargs
        self.passes: list[list[Any]] = []
        EngineSpy.instances.append(self)
        self._real = AlertEngine(**kwargs)

    async def run_pass(self, items, rules):
        self.passes.append(list(items))
        return await self._real.run_pass(items, rules)


@pytest.fixture()
def engine_spy(monkeypatch):
    EngineSpy.instances = []
    monkeypatch.setattr(pipeline_module, "AlertEngine", EngineSpy)
    yield EngineSpy
    EngineSpy.instances = []


def test_pipeline_zero_rules_zero_surprise(tmp_path, engine_spy):
    """零惊扰第一用例:不配规则 → 一次空表 SELECT 后短路,引擎不构造."""
    store = make_store(tmp_path)
    pipeline = make_pipeline(
        make_config(),
        handler=make_handler(
            [{"title": "免费送 NAS 券", "url": "https://api.demo.local/a"}]
        ),
        store=store,
    )
    result = asyncio.run(pipeline.run())
    assert result.status == "success"
    assert engine_spy.instances == []  # 规则表空 → 引擎零构造
    assert store.list_fired() == []
    store.close()


def test_pipeline_dry_run_short_circuits_alert_pass(tmp_path, engine_spy):
    """dry-run 最强零告警:不评估、不占坑、不发(短排在引擎构造之前)."""
    store = make_store(tmp_path)
    store.save_alert_rule(push_rule(when="'免费送' in title"))
    pipeline = make_pipeline(
        make_config(),
        handler=make_handler(
            [{"title": "免费送 NAS 券", "url": "https://api.demo.local/a"}]
        ),
        store=store,
    )
    result = asyncio.run(pipeline.run(dry_run=True))
    assert result.status == "success"
    assert engine_spy.instances == []  # dry 短路
    assert store.list_fired() == []  # 持久库零落(dry 用内存库,更无痕迹)
    store.close()


def test_pipeline_broken_fetch_skips_alert_items(tmp_path, engine_spy):
    """上游 broken(result.items=[])→ 附加步收到空集,零命中(同哲学)."""

    def dead_handler(request: httpx.Request) -> httpx.Response:
        if request.url.path == "/robots.txt":
            return httpx.Response(404, text="")
        return httpx.Response(500, text="dead")

    store = make_store(tmp_path)
    store.save_alert_rule(push_rule())
    pipeline = make_pipeline(make_config(), handler=dead_handler, store=store)
    result = asyncio.run(pipeline.run())
    assert result.items == [] and result.status == "failed"
    assert len(engine_spy.instances) == 1  # 引擎被构造(规则在)
    assert engine_spy.instances[0].passes == [[]]  # 但输入是空集
    assert store.list_fired() == []
    store.close()


def test_pipeline_alert_push_sends_when_route_archives(tmp_path, monkeypatch):
    """route archive 不发送 → 告警 push 真发(status=sent;通道唯一调用来自告警)."""
    store = make_store(tmp_path)
    store.save_alert_rule(push_rule(when="'免费送' in title"))

    channel = FakeChannel()
    monkeypatch.setattr(
        pipeline_module, "CHANNELS", {**pipeline_module.CHANNELS, "stdout": FakeChannel}
    )
    # 通道实例由 _build_channel 构造;此处直接捕获其调用:改用 registry 替代法
    # ——更直接:让 stdout 通道类记录到共享列表。
    shared: list[FakeChannel] = []

    class Capturing(FakeChannel):
        def __init__(self, **kwargs: Any) -> None:
            super().__init__(**kwargs)
            shared.append(self)

    monkeypatch.setattr(pipeline_module, "CHANNELS", {"stdout": Capturing})
    config = make_config(
        classify={"builtin": False, "rules": []},
        push=[{"channel": "stdout", "route": [{"when": "title", "mode": "archive"}]}],
    )
    pipeline = make_pipeline(
        config,
        handler=make_handler(
            [{"title": "免费送 NAS 券", "url": "https://api.demo.local/a"}]
        ),
        store=store,
    )
    result = asyncio.run(pipeline.run())
    assert result.status == "success"
    fired = store.list_fired()
    assert len(fired) == 1 and fired[0].action_status == "sent"  # 告警送达
    assert fired[0].item_id == store.list_items(limit=1)[0].id  # item 关联可解析
    # route(archive)与告警各自 _build_channel:全链通道只被真正调用一次,
    # 且那一次来自告警的 immediate 发送。
    all_calls = [call for channel in shared for call in channel.calls]
    assert len(all_calls) == 1 and all_calls[0]["context"].kind == "immediate"
    store.close()


def test_pipeline_route_immediate_first_suppresses_alert(tmp_path, monkeypatch):
    """双向压制·管线方向:route immediate 先发 → 告警同注册表被拦(不重发)."""
    store = make_store(tmp_path)
    store.save_alert_rule(push_rule(when="'免费送' in title"))
    shared: list[FakeChannel] = []

    class Capturing(FakeChannel):
        def __init__(self, **kwargs: Any) -> None:
            super().__init__(**kwargs)
            shared.append(self)

    monkeypatch.setattr(pipeline_module, "CHANNELS", {"stdout": Capturing})
    pipeline = make_pipeline(
        make_config(),
        handler=make_handler(
            [{"title": "免费送 NAS 券", "url": "https://api.demo.local/a"}]
        ),
        store=store,
    )
    result = asyncio.run(pipeline.run())
    assert result.status == "success"
    fired = store.list_fired()
    assert len(fired) == 1
    assert fired[0].action_status == "send_failed"  # 同槽位拦截 → 未送达
    # 全链通道只被 route 的 immediate 真正调用一次;告警实例零调用(被拦)。
    all_calls = [call for channel in shared for call in channel.calls]
    assert len(all_calls) == 1 and all_calls[0]["context"].kind == "immediate"
    store.close()


def test_pipeline_tag_rule_two_step_writeback_without_push_channels(tmp_path):
    """品类未配 push 通道:tag-only 规则照常命中(独立附加步,不并入 push 收尾)."""
    store = make_store(tmp_path)
    store.save_alert_rule(
        tag_rule(when="'融资' in title", action_config={"tags": ["fin"]})
    )
    pipeline = make_pipeline(
        make_config(classify={"builtin": False, "rules": []}, push=[]),
        handler=make_handler(
            [{"title": "X公司完成融资", "url": "https://api.demo.local/a"}]
        ),
        store=store,
    )
    result = asyncio.run(pipeline.run())
    assert result.status == "success"
    item_row = store.list_items(limit=1)[0]
    assert item_row.tags == ["fin"]  # items.tags 回写
    fired = store.list_fired()
    assert len(fired) == 1 and fired[0].action_status == "tagged"
    assert fired[0].dedup_key == item_row.dedup_key
    store.close()


def test_pipeline_feedback_mute_word_joins_suppression(tmp_path):
    """反馈 0.0 权重词并入 effective mute → 告警同门被压制(mute 词表同源).

    seeding 说明:调参器在 run 起点按窗口反馈重算权重,「无反馈支撑的 0.0」
    会被 release(恢复语义,调整历史可追溯)。因此种 2 条 bad 反馈
    (ratio=1.0 → 重算权重恰为 0.0,与活跃值相等 = 幂等不写),0.0 得以
    存活到 _alert_pass 读词表——这正是真实反馈环到达该态的路径。
    """
    from myssia.store import FeedbackRecord, TuningRecord

    store = make_store(tmp_path)
    for index in range(2):  # DEFAULT_MIN_BAD_COUNT=2, ratio=1.0 ≥ 0.5
        store.save_feedback(
            FeedbackRecord(
                dedup_key=f"fb-{index}",
                verdict="bad",
                channel="cli",
                title="X公司完成融资",
            )
        )
    store.save_tuning(
        TuningRecord(kind="mute_weight", payload={"word": "融资", "weight": 0.0})
    )
    store.save_alert_rule(tag_rule(when="title"))
    pipeline = make_pipeline(
        make_config(classify={"builtin": False, "rules": []}, push=[]),
        handler=make_handler(
            [{"title": "X公司完成融资", "url": "https://api.demo.local/a"}]
        ),
        store=store,
    )
    result = asyncio.run(pipeline.run())
    assert result.status == "success"
    assert store.list_fired() == []  # mute 命中:跳过全部规则
    assert store.list_items(limit=1)[0].tags == []  # 未打标
    store.close()


def test_pipeline_alert_pass_failure_isolated_from_run_status(
    tmp_path, monkeypatch, caplog
):
    """附加步自身失败 = WARNING 隔离,不影响 run 终态(design §6.1)."""
    store = make_store(tmp_path)
    store.save_alert_rule(push_rule())

    class ExplodingEngine:
        def __init__(self, **kwargs: Any) -> None:
            pass

        async def run_pass(self, items, rules):
            raise RuntimeError("模拟附加步基础设施故障")

    monkeypatch.setattr(pipeline_module, "AlertEngine", ExplodingEngine)
    pipeline = make_pipeline(
        make_config(),
        handler=make_handler(
            [{"title": "免费送 NAS 券", "url": "https://api.demo.local/a"}]
        ),
        store=store,
    )
    with caplog.at_level("WARNING", logger="myssia.pipeline"):
        result = asyncio.run(pipeline.run())
    assert result.status == "success"  # run 终态不被附加步拖垮
    assert any("告警附加步失败" in record.message for record in caplog.records)
    store.close()


# ---------------------------------------------------------------------------
# 组合投递(10-06-hermes-align 复核条目③):同轮 push 命中按通道合并一条
# ---------------------------------------------------------------------------


def test_push_hits_same_channel_merge_into_single_send(tmp_path):
    """组合铁律:同轮 2 条命中同通道 → send 恰 1 次载 2 条,全员 sent。

    事件语义零变化锚:UNIQUE 占坑仍逐规则(两行 fired 各自入库)。
    """
    store = make_store(tmp_path)
    rules = [
        store.save_alert_rule(push_rule(name="规则甲", when="'甲' in title")),
        store.save_alert_rule(push_rule(name="规则乙", when="'乙' in title")),
    ]
    channel = FakeChannel()
    calls: list[Any] = []
    engine = AlertEngine(
        store=store,
        channel_resolver=lambda name: channel if name == "stdout" else None,
        send=ok_send(calls),
    )
    items = [
        make_item(title="甲事件命中", dedup_key="key-a"),
        make_item(title="乙事件命中", dedup_key="key-b"),
    ]
    fired = asyncio.run(engine.run_pass(items, rules))
    assert len(calls) == 1  # 同通道一轮恰一条(逐条单发已消灭)
    assert len(calls[0]["args"][0]) == 2  # 两条目同载一条消息
    assert calls[0]["kwargs"]["item_specs"] == [None, None]
    assert [row.action_status for row in fired] == ["sent", "sent"]  # 桶内同进退
    assert len(store.list_fired()) == 2  # 占坑仍逐规则
    store.close()


def test_push_hits_different_channels_stay_isolated(tmp_path):
    """跨通道不合桶:不同通道各自一条(凭据/投递面隔离)。"""
    store = make_store(tmp_path)
    stdout = FakeChannel(name="stdout")
    tg = FakeChannel(name="telegram")
    rules = [
        store.save_alert_rule(
            push_rule(
                name="规则甲", when="'甲' in title", action_config={"channel": "stdout"}
            )
        ),
        store.save_alert_rule(
            push_rule(
                name="规则乙",
                when="'乙' in title",
                action_config={"channel": "telegram"},
            )
        ),
    ]
    calls: list[Any] = []

    async def send(items, **kwargs):
        calls.append(
            {"args": list(items), "kwargs": kwargs, "channels": kwargs["channels"]}
        )
        return [SendReport(kwargs["channels"][0].name, ok=True, item_count=len(items))]

    engine = AlertEngine(
        store=store,
        channel_resolver=lambda name: {"stdout": stdout, "telegram": tg}[name],
        send=send,
    )
    items = [
        make_item(title="甲事件命中", dedup_key="key-a"),
        make_item(title="乙事件命中", dedup_key="key-b"),
    ]
    asyncio.run(engine.run_pass(items, rules))
    assert len(calls) == 2  # 两通道各一条
    assert [c["channels"][0].name for c in calls] == ["stdout", "telegram"]
    store.close()


def test_push_merged_batch_failure_marks_all_send_failed(tmp_path):
    """桶内同进退:合并批失败 → 组内全员 send_failed(合并消息原子性)。"""
    store = make_store(tmp_path)
    rules = [
        store.save_alert_rule(push_rule(name="规则甲", when="'甲' in title")),
        store.save_alert_rule(push_rule(name="规则乙", when="'乙' in title")),
    ]
    calls: list[Any] = []
    engine = AlertEngine(
        store=store,
        channel_resolver=lambda _: FakeChannel(),
        send=failing_send(calls),
    )
    items = [
        make_item(title="甲事件命中", dedup_key="key-a"),
        make_item(title="乙事件命中", dedup_key="key-b"),
    ]
    fired = asyncio.run(engine.run_pass(items, rules))
    assert len(calls) == 1
    assert [row.action_status for row in fired] == ["send_failed", "send_failed"]
    store.close()
