"""value_gate 裁决层测试(value-gate-dedup):schema 装载 + 首跑抑制 + 变化重推.

覆盖 acceptance 三块:

- schema:``value_gate:`` sidecar 装载/未声明 None/非法结构 ``$.value_gate``
  前缀/字段校验;两开关缺省 false 即现状。
- 首跑抑制(first_run_quiet):archive 路由首跑条目入库+登记+不进 kept+skip
  计数;immediate 路由首跑条目豁免照常进 kept(F1 双断言);开关假时现状。
- 变化重推(repush_on_change):内容变放行且同 key 两行、新行 read/starred
  继承旧行(F4)、内容同拦截、存量旧指纹 NULL 拦截;ItemRecord.content_hash
  无条件铸值非 None。

全部走 httpx.MockTransport + monkeypatch 的 fetch_source(条目内容完全受控),
零真实网络;存储 tmp_path / :memory:。风格同 tests/pipeline/test_pipeline.py。
"""

from __future__ import annotations

import asyncio
from datetime import datetime, timezone
from typing import Any

import httpx
import pytest

import myssia.pipeline as pipeline_module
from conftest import FakeClock
from myssia.pipeline import Pipeline
from myssia.schema import ValueGateConfig, load_category
from myssia.store import ItemRecord, SQLiteStore

TIMEZONE = "Asia/Shanghai"
URL_A = "https://api.demo.local/a"


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def make_config(**overrides: Any):
    """最小合法品类 + 覆写(value_gate/push/dedup 都从这进,schema 真校验)。"""
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
        "classify": {"builtin": False, "rules": []},
        "push": [{"channel": "stdout"}],
    }
    data.update(overrides)
    return load_category(data)


def make_pipeline(config, *, store: SQLiteStore) -> tuple[Pipeline, FakeClock]:
    """注入 MockTransport 的 Pipeline(fetch 会被 monkeypatch 掉,handler 只兜底)。"""
    clock = FakeClock()

    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(404, text="")

    client = httpx.AsyncClient(transport=httpx.MockTransport(handler))
    return (
        Pipeline(config, store=store, client=client, clock=clock.time, sleep=clock.sleep),
        clock,
    )


def fetch_returning(monkeypatch, items: list[dict[str, Any]]) -> None:
    """把 fetch_source 换成返回固定条目的假件(内容/fetch_change_reason 受控)。"""

    async def fake_fetch(source, context):
        return pipeline_module.FetchOutcome(
            source=source.name, engine="direct_api", items=[dict(item) for item in items]
        )

    monkeypatch.setattr(pipeline_module, "fetch_source", fake_fetch)


def first_fetch_item(*, title: str = "免费送 NAS 券", content: str | None = None) -> dict[str, Any]:
    """一条带 fetch_change_reason=first_fetch 的首跑条目(static_html 铸键同形)。"""
    item: dict[str, Any] = {
        "title": title,
        "url": URL_A,
        "fetch_change_reason": "first_fetch",
    }
    if content is not None:
        item["content"] = content
    return item


# ---------------------------------------------------------------------------
# schema:value_gate 节装载与校验
# ---------------------------------------------------------------------------


def base_data(**overrides: Any) -> dict[str, Any]:
    data: dict[str, Any] = {
        "id": "demo",
        "name": "演示品类",
        "schedule": "0 9 * * *",
        "sources": [{"name": "api", "url": "https://api.demo.local/list"}],
    }
    data.update(overrides)
    return data


def test_value_gate_section_loads_and_attaches():
    """声明即装载:两开关为真挂到 CategoryConfig.value_gate 属性。"""
    config = load_category(
        base_data(value_gate={"first_run_quiet": True, "repush_on_change": True})
    )
    assert config.value_gate is not None
    assert config.value_gate.first_run_quiet is True
    assert config.value_gate.repush_on_change is True


def test_value_gate_absent_and_null_are_none():
    """未声明与 value_gate: null 都视为未声明(sidecar 先例,占位写法不拒载)。"""
    assert load_category(base_data()).value_gate is None
    assert load_category(base_data(value_gate=None)).value_gate is None


def test_value_gate_rejects_non_mapping_with_dollar_prefix():
    """非映射结构:LoadError 且错误路径恰为 $.value_gate 前缀。"""
    with pytest.raises(Exception) as exc_info:
        load_category(base_data(value_gate="nope"))
    details = exc_info.value.errors
    assert [(d.path, d.error_type) for d in details] == [
        ("$.value_gate", "invalid_value_gate_section")
    ]


def test_value_gate_unknown_field_and_bad_type_paths():
    """未知字段/类型错:错误路径带 $.value_gate.<字段> 前缀(fail-fast)。"""
    with pytest.raises(Exception) as unknown:
        load_category(base_data(value_gate={"nope": True}))
    assert [(d.path, d.error_type) for d in unknown.value.errors] == [
        ("$.value_gate.nope", "unknown_field")
    ]
    with pytest.raises(Exception) as bad_type:
        load_category(base_data(value_gate={"first_run_quiet": [1]}))
    assert [(d.path, d.error_type) for d in bad_type.value.errors] == [
        ("$.value_gate.first_run_quiet", "bool_type")
    ]


def test_value_gate_defaults_are_current_behavior():
    """缺省即现状:两开关默认 false(节不存在时行为逐字段一致)。"""
    defaults = ValueGateConfig()
    assert defaults.first_run_quiet is False
    assert defaults.repush_on_change is False


# ---------------------------------------------------------------------------
# 首跑抑制(first_run_quiet)
# ---------------------------------------------------------------------------


def test_first_run_quiet_archive_route_persists_registers_and_holds_back(tmp_path, monkeypatch):
    """archive 路由首跑条目:入库+登记+不进 kept+skip 计数(照常 save+mark_seen)。"""
    store = SQLiteStore(tmp_path / "p.db")
    config = make_config(
        value_gate={"first_run_quiet": True},
        push=[{"channel": "stdout", "route": [{"when": "title", "mode": "archive"}]}],
    )
    fetch_returning(monkeypatch, [first_fetch_item(content="正文第一版")])
    pipeline, _clock = make_pipeline(config, store=store)
    result = asyncio.run(pipeline.run())

    # 入库:一行,且指纹无条件铸值(content_hash 非 None)
    rows = store.list_items()
    assert len(rows) == 1
    assert rows[0].content_hash is not None
    # 登记:dedup 注册表有键(下一轮同键会被 dedup_seen 拦)
    assert store.get_dedup_entry(URL_A) is not None
    # 不进 kept:当轮推送流零条目,skip 计数可见
    assert result.items == []
    assert result.stage("dedup").skips["first_run_quiet"] == 1
    assert result.stage("dedup").skips.get("dedup_seen", 0) == 0
    store.close()


def test_first_run_quiet_immediate_route_exempt_f1(tmp_path, monkeypatch):
    """immediate 路由首跑条目豁免(F1 双断言):照常进 kept 且零 first_run_quiet 抑制。"""
    store = SQLiteStore(tmp_path / "p.db")
    config = make_config(
        value_gate={"first_run_quiet": True},
        push=[{"channel": "stdout", "route": [{"when": "title", "mode": "immediate"}]}],
    )
    fetch_returning(monkeypatch, [first_fetch_item()])
    pipeline, _clock = make_pipeline(config, store=store)
    result = asyncio.run(pipeline.run())

    # 断言一:首跑条目照常进 kept(羊毛/优惠类不折叠)
    assert len(result.items) == 1 and result.items[0].url == URL_A
    # 断言二:零抑制计数、零拦截
    assert result.stage("dedup").skips.get("first_run_quiet", 0) == 0
    assert result.stage("dedup").skips.get("dedup_seen", 0) == 0
    assert len(store.list_items()) == 1
    store.close()


def test_first_run_quiet_false_keeps_current_behavior(tmp_path, monkeypatch):
    """开关假(显式声明 false):首跑条目照常进 kept(与本节不存在时现状一致)。"""
    store = SQLiteStore(tmp_path / "p.db")
    config = make_config(
        value_gate={"first_run_quiet": False, "repush_on_change": False},
        push=[{"channel": "stdout", "route": [{"when": "title", "mode": "archive"}]}],
    )
    fetch_returning(monkeypatch, [first_fetch_item()])
    pipeline, _clock = make_pipeline(config, store=store)
    result = asyncio.run(pipeline.run())

    assert len(result.items) == 1  # 现状:首跑条目进推送流(archive 桶入库不发送)
    assert result.stage("dedup").skips.get("first_run_quiet", 0) == 0
    assert len(store.list_items()) == 1
    store.close()


# ---------------------------------------------------------------------------
# 变化重推(repush_on_change)
# ---------------------------------------------------------------------------


def test_repush_on_change_same_content_blocked(tmp_path, monkeypatch):
    """内容同:照常拦截(dedup_seen),不重复入库。"""
    store = SQLiteStore(tmp_path / "p.db")
    config = make_config(value_gate={"repush_on_change": True})
    item = first_fetch_item(title="同一个标题", content="一模一样的正文")
    fetch_returning(monkeypatch, [item])
    pipeline, _clock = make_pipeline(config, store=store)
    first = asyncio.run(pipeline.run())
    second = asyncio.run(pipeline.run())

    assert len(first.items) == 1
    assert second.stage("dedup").skips["dedup_seen"] == 1
    assert second.items == []
    assert len(store.list_items()) == 1  # 只有第一轮那行
    store.close()


def test_repush_on_change_content_change_repushes_new_row_with_state(tmp_path, monkeypatch):
    """内容变:放行且同 key 两行;新行 read/starred 继承旧行(F4 状态迁移)。"""
    store = SQLiteStore(tmp_path / "p.db")
    config = make_config(value_gate={"repush_on_change": True})
    fetch_returning(monkeypatch, [first_fetch_item(title="降价播报", content="价格 199 元")])
    pipeline, _clock = make_pipeline(config, store=store)
    first = asyncio.run(pipeline.run())
    assert len(first.items) == 1
    old_row = store.get_item_by_dedup_key(URL_A)
    assert old_row is not None and old_row.content_hash is not None

    # 两轮之间:用户读了旧行并加了星标(置位按 dedup_key)
    store.set_item_states([URL_A], "read", True)
    store.set_item_states([URL_A], "starred", True)

    # 第二轮:同键内容变了(指纹不同)→ 放行
    fetch_returning(
        monkeypatch,
        [{**first_fetch_item(title="降价播报", content="价格 99 元"), "fetch_change_reason": "hash_differ"}],
    )
    second = asyncio.run(pipeline.run())
    assert len(second.items) == 1  # 放行进 kept
    assert second.stage("dedup").skips.get("dedup_seen", 0) == 0

    # 同 key 两行;新行(取最新)继承读态,指纹更新
    rows = store.list_items()
    assert len(rows) == 2
    assert {row.dedup_key for row in rows} == {URL_A}
    newest = store.get_item_by_dedup_key(URL_A)  # newest wins
    assert newest.id != old_row.id
    assert newest.read is True and newest.starred is True  # F4 继承
    assert newest.later is False
    assert newest.content_hash is not None and newest.content_hash != old_row.content_hash
    store.close()


def test_repush_legacy_null_hash_never_repushes(tmp_path, monkeypatch):
    """存量旧指纹 NULL(本节上线前的老行):内容再不同也拦截,永不误重推(F9)。"""
    store = SQLiteStore(tmp_path / "p.db")
    # 预置一行无指纹的老条目 + 已登记键(模拟存量库)
    store.save_item(
        ItemRecord(url=URL_A, dedup_key=URL_A, title="旧标题", content="旧正文", content_hash=None)
    )
    store.mark_dedup_seen(URL_A, datetime.now(timezone.utc))

    config = make_config(value_gate={"repush_on_change": True})
    fetch_returning(monkeypatch, [first_fetch_item(title="新标题", content="全新正文")])
    pipeline, _clock = make_pipeline(config, store=store)
    result = asyncio.run(pipeline.run())

    assert result.stage("dedup").skips["dedup_seen"] == 1
    assert result.items == []
    rows = store.list_items()
    assert len(rows) == 1 and rows[0].title == "旧标题"  # 仍是老行,未添新行
    store.close()


def test_dedup_stamps_content_hash_unconditionally(tmp_path, monkeypatch):
    """指纹无条件铸:连 value_gate 节都不配(现状配置)也铸 content_hash 非 None。"""
    store = SQLiteStore(tmp_path / "p.db")
    config = make_config()  # 无 value_gate 节
    fetch_returning(monkeypatch, [first_fetch_item(content="任何正文")])
    pipeline, _clock = make_pipeline(config, store=store)
    asyncio.run(pipeline.run())

    row = store.get_item_by_dedup_key(URL_A)
    assert row is not None and row.content_hash is not None
    store.close()


# ---------------------------------------------------------------------------
# store:状态迁移小方法
# ---------------------------------------------------------------------------


def test_carry_item_states_copies_three_columns_and_false_on_missing():
    """carry_item_states:三列拷贝;旧行/新行不在返回 False(best-effort)。"""
    store = SQLiteStore(":memory:")
    old_id = store.save_item(
        ItemRecord(url=URL_A, dedup_key=URL_A, title="旧行", content="v1", content_hash="h1")
    )
    # 旧行先置位(此时同键只有旧行)
    store.set_item_states([URL_A], "read", True)
    store.set_item_states([URL_A], "starred", True)
    new_id = store.save_item(
        ItemRecord(url=URL_A, dedup_key=URL_A, title="新行", content="v2", content_hash="h2")
    )
    assert store.get_item(new_id).read is False  # 新行缺省未读

    assert store.carry_item_states(from_item_id=old_id, to_item_id=new_id) is True
    migrated = store.get_item(new_id)
    assert migrated.read is True and migrated.starred is True and migrated.later is False

    # 旧行不在(retention 剪枝)或新行不在 → False,不抛
    assert store.carry_item_states(from_item_id=999_999, to_item_id=new_id) is False
    assert store.carry_item_states(from_item_id=old_id, to_item_id=999_999) is False
    store.close()
