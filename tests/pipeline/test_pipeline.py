"""Tests for myssia.pipeline — orchestration, isolation, timeout/retry, scheduler.

Covers PRD 10-01-v01-pipeline-orchestrator acceptance criteria:

- 步骤顺序与产物传递(stage chain: fetch -> classify -> dedup -> analyze -> push,
  stage reports carry in/out counts and skips);
- 单源失败隔离(one dead source never breaks siblings or downstream stages);
- 超时与重试(per-source timeout isolation, step-level retry with recorded
  exponential backoff, upstream_failed skipping);
- cron+timezone 解析(build_cron_trigger next-fire computation);
- 多源并发(4-source asyncio.Barrier rendezvous proves overlap, serial would
  time out);
- 常驻模式(run_forever with a per-second cron fires on schedule; a failing
  run never kills the scheduler).

All I/O runs on httpx.MockTransport via injected clients; all waiting is
recorded by FakeClock (except the loop-mode test, which uses a real 1-second
cron). No real network, no real filesystem (stores are tmp_path / :memory:).
"""

from __future__ import annotations

import asyncio
import json
import sys
import time
from datetime import datetime
from typing import Any

import httpx
import pytest
from apscheduler.triggers.cron import CronTrigger

import myssia.pipeline as pipeline_module
from conftest import FakeClock
from myssia.pipeline import (
    EXECUTED_STAGES,
    STAGES,
    ChannelPushReport,
    Item,
    Pipeline,
    RunResult,
    SourceReport,
    StageOptions,
    StageReport,
    build_cron_trigger,
)
from myssia.schema import load_category
from myssia.store import SQLiteStore

TIMEZONE = "Asia/Shanghai"


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def make_config(**overrides: Any):
    """A minimal valid CategoryConfig (schema-validated) with overrides."""
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


def json_source(name: str, host: str) -> dict[str, Any]:
    """One direct_api source spec on its own host (per-host limiter isolation)."""
    return {
        "name": name,
        "engine": "direct_api",
        "url": f"https://{host}/list",
        "extract": {
            "type": "json_path",
            "fields": {"title": "$[*].title", "url": "$[*].url"},
        },
    }


def make_handler(payloads: dict[str, Any]):
    """MockTransport handler: robots.txt -> 404 (fail open), path-keyed payloads."""

    def handler(request: httpx.Request) -> httpx.Response:
        if request.url.path == "/robots.txt":
            return httpx.Response(404, text="")
        return httpx.Response(200, json=payloads)

    return handler


def make_pipeline(
    config,
    *,
    handler: Any,
    store: SQLiteStore,
    clock: FakeClock | None = None,
    **kwargs: Any,
) -> tuple[Pipeline, FakeClock]:
    """Pipeline on an injected mock client + FakeClock (no real I/O or waiting)."""
    clock = clock or FakeClock()
    client = httpx.AsyncClient(transport=httpx.MockTransport(handler))
    pipeline = Pipeline(
        config,
        store=store,
        client=client,
        clock=clock.time,
        sleep=clock.sleep,
        **kwargs,
    )
    return pipeline, clock


class RecordingChannel:
    """Test double capturing channel sends (构造注入 into CHANNELS registry)."""

    name = "stdout"

    def __init__(self, **kwargs: Any) -> None:
        self.kwargs = kwargs
        self.calls: list[dict[str, Any]] = []

    async def send(self, items, context) -> None:
        self.calls.append({"items": list(items), "context": context})


class FlakyOnceChannel(RecordingChannel):
    """First send fails with a structured PushSendError, later sends succeed."""

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.attempts = 0

    async def send(self, items, context) -> None:
        self.attempts += 1
        if self.attempts == 1:
            from myssia.push import PushSendError

            raise PushSendError("http_error", "模拟瞬时网络故障")
        await super().send(items, context)


# ---------------------------------------------------------------------------
# Stage order & artifact handoff
# ---------------------------------------------------------------------------


def test_pipeline_stage_order_and_item_handoff(tmp_path):
    """fetch(3) -> classify(2 留存,1 丢弃) -> dedup(2 新) -> analyze -> push."""
    store = SQLiteStore(tmp_path / "p.db")
    config = make_config(
        sources=[json_source("api", "api.demo.local")],
        push=[{"channel": "stdout"}],
    )
    handler = make_handler(
        [
            {"title": "免费送 NAS 券", "url": "https://api.demo.local/a"},
            {"title": "白嫖机场体验", "url": "https://api.demo.local/b"},
            {"title": "广告贴不要点", "url": "https://api.demo.local/c"},
        ]
    )
    pipeline, _clock = make_pipeline(config, handler=handler, store=store)
    result = asyncio.run(pipeline.run())

    assert [stage.name for stage in result.stages] == list(EXECUTED_STAGES)
    assert all(stage.status == "ok" for stage in result.stages)
    assert (result.stage("fetch").items_in, result.stage("fetch").items_out) == (1, 3)
    assert result.stage("classify").items_out == 2
    assert result.stage("classify").skips["classify_unmatched"] == 1
    assert result.stage("dedup").items_out == 2
    assert result.stage("analyze").items_out == 2
    assert result.status == "success"
    assert [(item.url, item.category) for item in result.items] == [
        ("https://api.demo.local/a", "freebie"),
        ("https://api.demo.local/b", "freebie"),
    ]
    assert all(item.dedup_key for item in result.items)
    assert len(store.list_items()) == 2
    # stdout 通道真正收到 immediate 桶(freebie -> 大类缺省 immediate);
    # send_immediate 每条目一张卡 → 2 条报告
    assert result.pushes[0].channel == "stdout"
    assert result.pushes[0].immediate == 2
    assert result.pushes[0].ok is True
    assert [report.ok for report in result.pushes[0].reports] == [True, True]
    store.close()


def test_run_result_is_json_serializable_and_runs_row_written(tmp_path):
    """RunResult.to_dict() 可被 json 消费;runs 表落 status + stats。"""
    store = SQLiteStore(tmp_path / "p.db")
    config = make_config()
    pipeline, _clock = make_pipeline(
        config, handler=make_handler([{"title": "免费送 NAS 券", "url": "https://api.demo.local/a"}]), store=store
    )
    result = asyncio.run(pipeline.run())

    payload = json.dumps(result.to_dict(), ensure_ascii=False)
    assert json.loads(payload)["status"] == "success"
    run_row = store.get_run(result.run_id)
    assert run_row is not None and run_row.status == "success"
    assert run_row.stats["items_retained"] == 1
    store.close()


# ---------------------------------------------------------------------------
# Source failure isolation
# ---------------------------------------------------------------------------


def test_source_failure_isolated_siblings_proceed(tmp_path):
    """一个源 500 挂掉:结构化记录,兄弟源与后续步骤照常。"""
    store = SQLiteStore(tmp_path / "p.db")
    config = make_config(
        sources=[
            json_source("good", "good.demo.local"),
            {**json_source("dead", "dead.demo.local"), "retry": 0},
        ],
    )

    def handler(request: httpx.Request) -> httpx.Response:
        if request.url.path == "/robots.txt":
            return httpx.Response(404, text="")
        if request.url.host == "dead.demo.local":
            return httpx.Response(500, text="boom")
        return httpx.Response(
            200, json=[{"title": "免费送 NAS 券", "url": "https://good.demo.local/a"}]
        )

    pipeline, _clock = make_pipeline(config, handler=handler, store=store)
    result = asyncio.run(pipeline.run())

    by_name = {source.name: source for source in result.sources}
    assert by_name["good"].item_count == 1 and not by_name["good"].failed
    assert by_name["dead"].failed is True
    assert by_name["dead"].error is not None
    # 降级链全程尝试:direct_api 报 http_500,后继引擎报 extract_unsupported
    assert "http_500" in {f["error_type"] for f in by_name["dead"].failures}
    assert [item.url for item in result.items] == ["https://good.demo.local/a"]
    assert result.status == "partial"
    assert [stage.status for stage in result.stages if stage.name != "fetch"] == ["ok"] * 4
    assert store.get_run(result.run_id).status == "partial"
    store.close()


def test_all_sources_failed_maps_to_failed_status(tmp_path):
    """全部源挂掉:status=failed(CLI 退出码 2 的来源)。"""
    store = SQLiteStore(tmp_path / "p.db")
    config = make_config(
        sources=[
            {**json_source("a", "a.demo.local"), "retry": 0},
            {**json_source("b", "b.demo.local"), "retry": 0},
        ],
    )

    def handler(request: httpx.Request) -> httpx.Response:
        if request.url.path == "/robots.txt":
            return httpx.Response(404, text="")
        return httpx.Response(500, text="boom")

    pipeline, _clock = make_pipeline(config, handler=handler, store=store)
    result = asyncio.run(pipeline.run())

    assert all(source.failed for source in result.sources)
    assert result.status == "failed"
    assert result.items == []
    store.close()


def test_item_without_url_recorded_and_dropped(tmp_path):
    """缺 url 的条目:invalid_item 结构化记录,不影响其余条目。"""
    store = SQLiteStore(tmp_path / "p.db")
    config = make_config()
    handler = make_handler(
        [
            {"title": "免费送 NAS 券", "url": "https://api.demo.local/a"},
            {"title": "没有链接的条目"},
        ]
    )
    pipeline, _clock = make_pipeline(config, handler=handler, store=store)
    result = asyncio.run(pipeline.run())

    assert [f["error_type"] for f in result.stage("fetch").failures] == ["invalid_item"]
    assert [item.url for item in result.items] == ["https://api.demo.local/a"]
    assert result.status == "partial"
    store.close()


# ---------------------------------------------------------------------------
# Timeout & retry (per source / per stage)
# ---------------------------------------------------------------------------


def test_fetch_timeout_isolated_to_slow_source(tmp_path, monkeypatch):
    """慢源按源级超时单独失败,兄弟源不受影响(error_type=timeout)。"""
    store = SQLiteStore(tmp_path / "p.db")
    config = make_config(
        sources=[json_source("slow", "slow.demo.local"), json_source("fast", "fast.demo.local")],
        push=[{"channel": "stdout"}],
    )

    async def fake_fetch(source, context):
        if source.name == "slow":
            await asyncio.sleep(30)
        return pipeline_module.FetchOutcome(
            source=source.name,
            engine="direct_api",
            items=[{"title": "免费送 NAS 券", "url": f"https://{source.name}.demo.local/a"}],
        )

    monkeypatch.setattr(pipeline_module, "fetch_source", fake_fetch)
    pipeline, _clock = make_pipeline(
        config,
        handler=make_handler([]),
        store=store,
        stage_options={"fetch": StageOptions(timeout_seconds=0.1)},
    )
    result = asyncio.run(pipeline.run())

    by_name = {source.name: source for source in result.sources}
    assert by_name["slow"].failed and by_name["slow"].error["error_type"] == "timeout"
    assert by_name["fast"].item_count == 1 and not by_name["fast"].failed
    assert len(result.items) == 1
    assert result.status == "partial"
    store.close()


def test_fetch_retries_with_recorded_backoff_then_succeeds(tmp_path, monkeypatch):
    """源级重试:两次失败后第三次成功,退避节奏 1s/2s 记录在 FakeClock。"""
    store = SQLiteStore(tmp_path / "p.db")
    config = make_config()
    calls = {"count": 0}

    async def flaky_fetch(source, context):
        calls["count"] += 1
        if calls["count"] < 3:
            raise RuntimeError(f"瞬时故障 #{calls['count']}")
        return pipeline_module.FetchOutcome(
            source=source.name,
            engine="direct_api",
            items=[{"title": "免费送 NAS 券", "url": "https://api.demo.local/a"}],
        )

    monkeypatch.setattr(pipeline_module, "fetch_source", flaky_fetch)
    pipeline, clock = make_pipeline(
        config,
        handler=make_handler([]),
        store=store,
        stage_options={"fetch": StageOptions(timeout_seconds=5, retries=2)},
    )
    result = asyncio.run(pipeline.run())

    assert calls["count"] == 3  # 重试 2 次:共 3 次尝试
    assert clock.sleeps == [1.0, 2.0]  # 指数退避 2**0 / 2**1
    assert result.sources[0].attempts == 3  # 重试记在源级,步骤级本身只跑一轮
    assert result.status == "success"
    store.close()


def test_stage_failure_skips_downstream_stages(tmp_path, monkeypatch):
    """分类步骤失败:下游 dedup/analyze/push 标记 upstream_failed,不推半成品。"""
    store = SQLiteStore(tmp_path / "p.db")
    config = make_config()

    def boom(*args, **kwargs):
        raise RuntimeError("分类器崩了")

    monkeypatch.setattr(pipeline_module, "classify_item", boom)
    pipeline, _clock = make_pipeline(
        config, handler=make_handler([{"title": "免费送 NAS 券", "url": "https://api.demo.local/a"}]), store=store
    )
    result = asyncio.run(pipeline.run())

    assert result.stage("fetch").status == "ok"
    assert result.stage("classify").status == "failed"
    assert result.stage("classify").error is not None
    assert result.stage("dedup").status == "skipped"
    assert result.stage("dedup").skip_reason == "upstream_failed"
    assert result.stage("analyze").status == "skipped"
    assert result.stage("push").status == "skipped"
    assert result.items == []
    assert result.status == "partial"
    assert store.list_items() == []  # 没有条目走到入库
    store.close()


def test_stage_options_rejects_unknown_stage(tmp_path):
    """stage_options 含未知阶段名 → ValueError(fail fast)。"""
    config = make_config()
    with pytest.raises(ValueError, match="未知阶段"):
        Pipeline(config, store=SQLiteStore(tmp_path / "p.db"), stage_options={"nope": StageOptions(timeout_seconds=1)})


# ---------------------------------------------------------------------------
# Concurrency (multi-source asyncio)
# ---------------------------------------------------------------------------


def test_sources_fetch_concurrently_barrier_rendezvous(tmp_path, monkeypatch):
    """4 源并发:屏障会合证明同时在飞;串行会合不上(超时)。"""
    store = SQLiteStore(tmp_path / "p.db")
    config = make_config(
        sources=[json_source(f"s{i}", f"h{i}.demo.local") for i in range(4)],
        push=[{"channel": "stdout"}],
    )
    barrier = asyncio.Barrier(4)

    async def rendezvous_fetch(source, context):
        await asyncio.wait_for(barrier.wait(), timeout=2.0)  # 串行执行会在此超时
        await asyncio.sleep(0.05)  # 每源 50ms:并发总耗时远小于 4×50ms
        return pipeline_module.FetchOutcome(
            source=source.name,
            engine="direct_api",
            items=[{"title": "免费送 NAS 券", "url": f"https://{source.name}.demo.local/a"}],
        )

    monkeypatch.setattr(pipeline_module, "fetch_source", rendezvous_fetch)
    pipeline, _clock = make_pipeline(
        config,
        handler=make_handler([]),
        store=store,
        stage_options={"fetch": StageOptions(timeout_seconds=5)},
    )
    started = time.monotonic()
    result = asyncio.run(pipeline.run())
    elapsed = time.monotonic() - started

    assert all(source.item_count == 1 for source in result.sources)
    assert len(result.items) == 4
    assert elapsed < 0.35, f"并发采集应明显快于串行(实测 {elapsed:.2f}s)"
    assert result.status == "success"
    store.close()


# ---------------------------------------------------------------------------
# Dedup across runs & key errors
# ---------------------------------------------------------------------------


def test_dedup_skips_seen_keys_across_runs(tmp_path):
    """同一 URL 第二轮(fetch 内容变了、指纹放行)被去重拦截。"""
    store = SQLiteStore(tmp_path / "p.db")
    config = make_config(dedup={"key": "{url}"})
    counter = {"n": 0}

    def handler(request: httpx.Request) -> httpx.Response:
        if request.url.path == "/robots.txt":
            return httpx.Response(404, text="")
        counter["n"] += 1
        return httpx.Response(
            200,
            json=[{"title": f"免费送 NAS 券 v{counter['n']}", "url": "https://api.demo.local/a"}],
        )

    pipeline, _clock = make_pipeline(config, handler=handler, store=store)
    first = asyncio.run(pipeline.run())
    second = asyncio.run(pipeline.run())

    assert len(first.items) == 1
    assert second.stage("dedup").skips["dedup_seen"] == 1
    assert second.items == []
    assert len(store.list_items()) == 1  # 第二轮未重复入库
    assert second.status == "success"  # dedup skip 是正常路径
    store.close()


def test_dedup_key_missing_field_recorded(tmp_path):
    """条目缺失 dedup.key 字段(json_path 未命中):dedup_key_error 记录,条目不入库。

    extract.fields 与 dedup.key 的静态一致性由 schema 加载期校验(invalid_dedup_key);
    这里覆盖运行期兜底:字段虽已声明,单条记录的 json_path 未命中时键缺席。
    """
    store = SQLiteStore(tmp_path / "p.db")
    config = make_config(
        sources=[
            {
                "name": "api",
                "engine": "direct_api",
                "url": "https://api.demo.local/list",
                "extract": {
                    "type": "json_path",
                    "fields": {
                        "title": "$[*].title",
                        "url": "$[*].url",
                        "symbol": "$[*].symbol",
                    },
                },
            }
        ],
        dedup={"key": "{symbol}"},
    )
    pipeline, _clock = make_pipeline(
        config,
        handler=make_handler([{"title": "免费送 NAS 券", "url": "https://api.demo.local/a"}]),
        store=store,
    )
    result = asyncio.run(pipeline.run())

    assert [f["error_type"] for f in result.stage("dedup").failures] == ["dedup_key_error"]
    assert result.items == []
    assert result.status == "partial"
    assert store.list_items() == []
    store.close()


# ---------------------------------------------------------------------------
# Dry-run & routing decisions
# ---------------------------------------------------------------------------


def test_dry_run_full_chain_without_side_effects(tmp_path):
    """dry-run:全链执行、路由判定产出,但零持久化副作用、零发送。"""
    real_store = SQLiteStore(tmp_path / "p.db")
    config = make_config(
        push=[
            {
                "channel": "feishu_card",
                "target": "env:FEISHU_CHAT_ID",
            }
        ]
    )
    pipeline, _clock = make_pipeline(
        config,
        handler=make_handler([{"title": "免费送 NAS 券", "url": "https://api.demo.local/a"}]),
        store=real_store,
    )
    result = asyncio.run(pipeline.run(dry_run=True))

    assert result.dry_run is True
    assert result.pushes[0].dry_run is True
    assert result.pushes[0].reports == []  # 未发送
    assert result.pushes[0].immediate == 1  # 路由判定照常产出
    assert result.items and result.items[0].category == "freebie"
    # 副作用全部隔离在内存库:注入的 store 未被写入
    assert real_store.list_items() == []
    assert real_store.get_run(result.run_id) is None  # run_id 来自内存库
    real_store.close()


def test_route_decisions_captured_per_channel(tmp_path):
    """route 判定结构化输出(mode/reason/rule_when),archive 桶不发送。"""
    real_store = SQLiteStore(tmp_path / "p.db")
    config = make_config(
        classify={"builtin": False},
        push=[{"channel": "stdout", "route": [{"when": "title", "mode": "archive"}]}],
    )
    pipeline, _clock = make_pipeline(
        config,
        handler=make_handler([{"title": "任意标题都能存档", "url": "https://api.demo.local/a"}]),
        store=real_store,
    )
    result = asyncio.run(pipeline.run())

    decisions = result.pushes[0].decisions
    assert decisions[0]["mode"] == "archive"
    assert decisions[0]["reason"] == "rule"
    assert decisions[0]["rule_when"] == "title"
    assert result.pushes[0].archive == 1
    assert result.pushes[0].reports == []  # archive 仅入库,不发送
    real_store.close()


def test_immediate_send_reaches_channel(tmp_path, monkeypatch):
    """非 dry-run:immediate 条目经注册通道真正发出。"""
    real_store = SQLiteStore(tmp_path / "p.db")
    config = make_config(push=[{"channel": "stdout"}])
    sent: list[dict[str, Any]] = []

    class CapturingChannel(RecordingChannel):
        async def send(self, items, context) -> None:
            await super().send(items, context)
            sent.append({"count": len(items), "kind": context.kind})

    monkeypatch.setattr(pipeline_module, "CHANNELS", {"stdout": CapturingChannel})
    pipeline, _clock = make_pipeline(
        config,
        handler=make_handler([{"title": "免费送 NAS 券", "url": "https://api.demo.local/a"}]),
        store=real_store,
    )
    result = asyncio.run(pipeline.run())

    assert len(sent) == 1 and sent[0]["count"] == 1 and sent[0]["kind"] == "immediate"
    assert result.pushes[0].ok is True
    real_store.close()


def test_stdout_stream_injection_reroutes_channel_output(tmp_path, capsys):
    """stdout_stream 注入:stdout 通道的卡片行写进注入流,进程 stdout 零输出。

    CLI 契约(SKILL.md §0):``myssia run --json`` 的 stdout 恰好一份 JSON——
    stdout 通道卡片行经此注入改写 stderr,不再与 run 报告同流(两份 JSON
    会让 AI 消费面 json.load 直接失败)。
    """
    import io

    real_store = SQLiteStore(tmp_path / "p.db")
    config = make_config(push=[{"channel": "stdout"}])
    card = io.StringIO()
    pipeline, _clock = make_pipeline(
        config,
        handler=make_handler([{"title": "免费送 NAS 券", "url": "https://api.demo.local/a"}]),
        store=real_store,
        stdout_stream=card,
    )
    result = asyncio.run(pipeline.run())

    assert result.pushes[0].ok is True
    card.seek(0)
    import json as _json

    payload = _json.loads(card.read())  # 卡片行落进注入流且本身是合法 JSON
    assert payload["channel"] == "stdout" and payload["count"] == 1
    assert capsys.readouterr().out == ""  # 进程 stdout 干净(run 报告独占它)
    real_store.close()


def test_digest_all_failed_retries_on_next_run(tmp_path, monkeypatch):
    """摘要全通道失败:条目留池,同一 Pipeline 下一次 run 的 flush 重试成功。

    Regression: the aggregator was created fresh inside every _push_channel,
    so digest.py's 「全通道失败留池待重试」 never took effect across runs —
    the failed item was dedup-marked and silently never pushed.
    """
    real_store = SQLiteStore(tmp_path / "digest.db")
    config = make_config(push=[{"channel": "stdout"}], classify={"builtin": False, "rules": []})
    payloads = [
        [{"title": "第一条", "url": "https://api.demo.local/a"}],
        [{"title": "第二条", "url": "https://api.demo.local/b"}],
    ]
    fetch_calls = {"n": 0}

    def handler(request: httpx.Request) -> httpx.Response:
        if request.url.path == "/robots.txt":
            return httpx.Response(404, text="")
        payload = payloads[min(fetch_calls["n"], 1)]
        fetch_calls["n"] += 1
        return httpx.Response(200, json=payload)

    sent_batches: list[list[str]] = []

    class TrackedChannel(FlakyOnceChannel):
        async def send(self, items, context) -> None:
            sent_batches.append([str(getattr(item, "title", item)) for item in items])
            await super().send(items, context)

    monkeypatch.setattr(pipeline_module, "CHANNELS", {"stdout": TrackedChannel})
    clock = FakeClock()
    client = httpx.AsyncClient(transport=httpx.MockTransport(handler))
    pipeline = Pipeline(
        config, store=real_store, client=client, clock=clock.time, sleep=clock.sleep
    )

    result1 = asyncio.run(pipeline.run())
    assert result1.pushes[0].ok is False
    assert result1.status == "partial"
    assert result1.pushes[0].reports[0].error.startswith("[http_error]")

    result2 = asyncio.run(pipeline.run())
    reports = result2.pushes[0].reports
    assert result2.pushes[0].ok is True
    assert result2.status == "success"
    assert len(reports) == 1
    # 第二次 flush 把上一轮失败条目和本轮新条目合并成一张卡发出(留池重试生效)
    assert sent_batches == [["第一条"], ["第一条", "第二条"]]
    real_store.close()


def test_stats_push_failures_dedup_cap_and_clip(tmp_path, monkeypatch, caplog):
    """stats_dict push 段失败明细:同错去重计数、封顶 3 条、超长截断、
    ok 通道空列表;真失败文案进 ERROR 日志;failures 经 finish_run 落库
    → list_runs 回读全链存活(仪表盘失败徽章的数据面)。
    """
    from myssia.push.base import clip_text

    real_store = SQLiteStore(tmp_path / "push-failures.db")
    # 通道名必须在 schema 字面量白名单内;CHANNELS 注册表整体换测试替身
    config = make_config(push=[{"channel": "stdout"}, {"channel": "ntfy", "target": "env:NTFY_TOPIC"}])
    items = [
        {"title": f"免费送 第{i}期", "url": f"https://api.demo.local/{i}"} for i in range(5)
    ]
    # 一次 send = 一条 immediate 卡 = 一条报告;长文案 ×2(去重计 2)+
    # 三条不同短文案(封顶后仅前两条入桶)
    long_detail = "凭据解析失败: 环境变量 X 未设置,到 设置→推送 填一次即可" + "补" * 400
    errors = [long_detail, "短错二", long_detail, "短错三", "短错四"]

    class SequencedFailureChannel(RecordingChannel):
        name = "stdout"

        async def send(self, items, context) -> None:
            from myssia.push import PushSendError

            raise PushSendError("env_var_missing", errors.pop(0))

    class SilentOkChannel(RecordingChannel):
        name = "ntfy"

    monkeypatch.setattr(
        pipeline_module,
        "CHANNELS",
        {"stdout": SequencedFailureChannel, "ntfy": SilentOkChannel},
    )
    pipeline, _clock = make_pipeline(config, handler=make_handler(items), store=real_store)

    with caplog.at_level("WARNING", logger="myssia.pipeline"):
        result = asyncio.run(pipeline.run())

    assert result.pushes[0].ok is False
    assert result.status == "partial"
    push_stats = result.stats_dict()["push"]
    # 既有五字段一字不动,failures 为加法第六键
    failing, ok_channel = push_stats
    assert set(failing) == {
        "channel",
        "ok",
        "immediate",
        "digest",
        "archive",
        "failures",
    }
    assert failing["channel"] == "stdout" and failing["immediate"] == 5
    long_error = f"[env_var_missing] {long_detail}"
    assert failing["failures"] == [
        {"error": clip_text(long_error, 300), "count": 2},  # 同错两报告去重计 2
        {"error": "[env_var_missing] 短错二", "count": 1},
        {"error": "[env_var_missing] 短错三", "count": 1},  # 封顶 3,短错四出局
    ]
    clipped = failing["failures"][0]["error"]
    assert (
        len(clipped) == 300
        and clipped.endswith("…")
        and clipped.startswith("[env_var_missing] 凭据")
    )
    # ok 通道恒带 failures 键(空列表,旧消费方按可选字段读)
    assert ok_channel["ok"] is True and ok_channel["failures"] == []
    # ERROR 日志含首条真失败文案(采集日志屏的指引露出面)
    error_logs = [
        r for r in caplog.records
        if r.levelname == "ERROR" and "推送失败原因" in r.message
    ]
    assert len(error_logs) == 1
    assert "channel=stdout" in error_logs[0].message and clipped in error_logs[0].message
    # store 往返:finish_run 落库 → list_runs 回读,失败明细原样存活
    stored_stats = real_store.list_runs()[0].stats
    assert stored_stats["push"][0]["failures"] == failing["failures"]
    real_store.close()


def test_stats_push_failures_skipped_report_not_polluting_guidance(
    tmp_path, monkeypatch, caplog
):
    """skipped「未尝试」报告(死信)不入 failures、不顶掉真失败指引文案:
    dead_target 在前时,stats failures 与 ERROR 日志仍显凭据指引。
    """
    from myssia.push import SendReport

    real_store = SQLiteStore(tmp_path / "skipped-mix.db")
    config = make_config(push=[{"channel": "stdout"}])
    guidance = "[env_var_missing] 飞书 bot 凭据解析失败: 到 设置→推送 填一次即可"

    async def fake_send_immediate(items, **kwargs):
        return [
            SendReport(
                channel="stdout", ok=False, item_count=1,
                error="[dead_target] 跳过此前确认不可达的对象", skipped=True,
            ),
            SendReport(channel="stdout", ok=False, item_count=1, error=guidance),
        ]

    monkeypatch.setattr(pipeline_module, "send_immediate", fake_send_immediate)
    pipeline, _clock = make_pipeline(
        config,
        handler=make_handler([{"title": "免费送 NAS 券", "url": "https://api.demo.local/a"}]),
        store=real_store,
    )

    with caplog.at_level("WARNING", logger="myssia.pipeline"):
        result = asyncio.run(pipeline.run())

    assert result.pushes[0].ok is False  # ok 口径含 skipped,既有行为不动
    failures = result.stats_dict()["push"][0]["failures"]
    assert failures == [{"error": guidance, "count": 1}]  # dead_target 未入桶
    error_logs = [
        r for r in caplog.records
        if r.levelname == "ERROR" and "推送失败原因" in r.message
    ]
    assert len(error_logs) == 1 and guidance in error_logs[0].message
    assert "dead_target" not in error_logs[0].message
    real_store.close()


def test_stats_push_all_skipped_failures_empty_and_no_error_log(
    tmp_path, monkeypatch, caplog
):
    """全 skipped 通道:ok=False 如实呈现,但 failures 为空、不打 ERROR
    (无「发送失败文案」可指,只保留既有计数 warning)——文档别把空
    failures 读成 ok。"""
    from myssia.push import SendReport

    real_store = SQLiteStore(tmp_path / "all-skipped.db")
    config = make_config(push=[{"channel": "stdout"}])

    async def fake_send_immediate(items, **kwargs):
        return [
            SendReport(
                channel="stdout", ok=False, item_count=1,
                error="[targeting_not_configured] 定向条目缺少通道目录(管线未接线)",
                skipped=True,
            ),
        ]

    monkeypatch.setattr(pipeline_module, "send_immediate", fake_send_immediate)
    pipeline, _clock = make_pipeline(
        config,
        handler=make_handler([{"title": "免费送 NAS 券", "url": "https://api.demo.local/a"}]),
        store=real_store,
    )

    with caplog.at_level("WARNING", logger="myssia.pipeline"):
        result = asyncio.run(pipeline.run())

    assert result.pushes[0].ok is False
    assert result.stats_dict()["push"][0]["failures"] == []
    assert not any(
        "推送失败原因" in r.message for r in caplog.records
    )  # 无 ERROR 文案行
    assert any(
        r.levelname == "WARNING" and "通道存在发送失败" in r.message for r in caplog.records
    )  # 既有计数 warning 照打
    real_store.close()


# ---------------------------------------------------------------------------
# Cron + timezone
# ---------------------------------------------------------------------------


def test_build_cron_trigger_resolves_timezone_next_fire():
    """cron+timezone:周三 10:00(上海)→ 当天 15:00 触发。"""
    trigger = build_cron_trigger("0 9,15 * * 1-5", TIMEZONE)
    now = datetime(2026, 10, 7, 10, 0, tzinfo=__import__("zoneinfo").ZoneInfo(TIMEZONE))
    next_fire = trigger.get_next_fire_time(None, now)
    assert next_fire is not None
    assert (next_fire.year, next_fire.month, next_fire.day, next_fire.hour) == (2026, 10, 7, 15)


def test_build_cron_trigger_defaults_and_rejects():
    """无 timezone 用系统本地;非法 cron / 非法 timezone 结构化报错。"""
    assert build_cron_trigger("0 9 * * *") is not None
    with pytest.raises(ValueError, match="cron"):
        build_cron_trigger("not-a-cron")
    with pytest.raises(ValueError, match="timezone"):
        build_cron_trigger("0 9 * * *", "Mars/Olympus_Mons")


# ---------------------------------------------------------------------------
# Resident mode (APScheduler)
# ---------------------------------------------------------------------------


def test_run_forever_fires_on_schedule(tmp_path):
    """常驻模式:秒级 cron 到点自动触发 2 次(runs 表落 2 行)。"""
    store = SQLiteStore(tmp_path / "p.db")
    config = make_config()
    counter = {"n": 0}

    def handler(request: httpx.Request) -> httpx.Response:
        if request.url.path == "/robots.txt":
            return httpx.Response(404, text="")
        counter["n"] += 1
        return httpx.Response(
            200,
            json=[{"title": f"免费送 NAS 券 v{counter['n']}", "url": "https://api.demo.local/a"}],
        )

    pipeline, _clock = make_pipeline(config, handler=handler, store=store)
    fires = asyncio.run(
        pipeline.run_forever(trigger=CronTrigger(second="*/1"), max_fires=2)
    )

    assert fires == 2
    assert len(store.list_items()) >= 1  # 至少一次真实运行入库
    store.close()


def test_run_forever_survives_run_failure(tmp_path, monkeypatch):
    """单次运行异常不拖垮调度:异常被结构化记录,后续触发继续。"""
    store = SQLiteStore(tmp_path / "p.db")
    config = make_config()
    pipeline, _clock = make_pipeline(config, handler=make_handler([]), store=store)

    async def broken_run(*, dry_run: bool = False):
        raise RuntimeError("存储炸了")

    monkeypatch.setattr(pipeline, "run", broken_run)
    fires = asyncio.run(pipeline.run_forever(trigger=CronTrigger(second="*/1"), max_fires=2))
    assert fires == 2  # 调度继续
    store.close()


# ---------------------------------------------------------------------------
# Unit-level: data structures
# ---------------------------------------------------------------------------


def test_item_from_extracted_rejects_missing_url():
    """缺 url 的提取记录 → ValueError(去重键依赖 URL)。"""
    with pytest.raises(ValueError, match="url"):
        Item.from_extracted({"title": "没有链接"}, "api")


def test_item_view_top_level_wins_over_metadata():
    """view():顶层字段优先于 metadata 同名字段。"""
    item = Item(url="https://a.local/1", title="标题", source="api", metadata={"title": "旧标题", "symbol": "NVDA"})
    view = item.view()
    assert view["title"] == "标题"
    assert view["symbol"] == "NVDA"


def test_stage_options_validation():
    """StageOptions 参数校验(正数超时、非负重试)。"""
    with pytest.raises(ValueError, match="超时"):
        StageOptions(timeout_seconds=0)
    with pytest.raises(ValueError, match="重试"):
        StageOptions(timeout_seconds=1, retries=-1)


# ---------------------------------------------------------------------------
# Channel wiring (v0.2 push-telegram:target/template/transport 可配且必达)
# ---------------------------------------------------------------------------


def test_build_channel_wires_target_and_template_for_telegram_and_webhook():
    """回归:v0.1 壳分支曾静默丢弃 telegram/webhook 的 target/template(裸构造
    改走默认 env 引用——假失败或误投)。v0.2 实装后必须原样到达通道。"""
    store = SQLiteStore(":memory:")
    pipeline, _ = make_pipeline(make_config(), handler=make_handler({}), store=store)

    from myssia.push import CHANNELS
    from myssia.push.telegram import TelegramChannel
    from myssia.push.webhook import WebhookChannel
    from myssia.schema import PushConfig

    assert set(CHANNELS) >= {"telegram", "webhook"}

    telegram = pipeline._build_channel(
        PushConfig(channel="telegram", target="env:MYIA_TG_CHAT", template="{{ slot }} {{ count }}")
    )
    assert isinstance(telegram, TelegramChannel)
    assert telegram._target == "env:MYIA_TG_CHAT"
    assert telegram._template == "{{ slot }} {{ count }}"

    webhook = pipeline._build_channel(
        PushConfig(
            channel="webhook",
            target="env:MYIA_HOOK",
            timeout=5.0,
            retries=3,
            retry_backoff_seconds=0.5,
        )
    )
    assert isinstance(webhook, WebhookChannel)
    assert webhook._target == "env:MYIA_HOOK"
    assert webhook._timeout == 5.0
    assert webhook._retries == 3
    assert webhook._retry_backoff_seconds == 0.5
    store.close()


def test_push_config_rejects_transport_fields_outside_webhook():
    """超时/重试仅 webhook 生效;其他通道显式配置即拒(不留静默忽略)。"""
    with pytest.raises(Exception, match="timeout"):
        make_config(push=[{"channel": "stdout", "timeout": 5.0}])
    with pytest.raises(Exception, match="retries"):
        make_config(push=[{"channel": "telegram", "target": "env:MYIA_TG_CHAT", "retries": 3}])
    with pytest.raises(Exception, match="timeout"):
        make_config(push=[{"channel": "webhook", "target": "env:MYIA_HOOK", "timeout": 0}])


# ---------------------------------------------------------------------------
# 2026-10 复盘修复回归:content 接线(enrich prompt + items.content 列)
# ---------------------------------------------------------------------------


def test_item_from_extracted_keeps_content_on_field():
    """content 是 Item 的字段(不进 metadata):enrich prompt 与 items.content
    列的数据来源——此前 content 在 from_extracted 被剔除,LLM 只见 url/title。"""
    item = Item.from_extracted(
        {"url": "https://a.local/1", "title": "t", "content": "正文内容" * 50, "symbol": "NVDA"},
        "api",
    )
    assert item.content == "正文内容" * 50
    assert "content" not in item.metadata
    assert item.metadata == {"symbol": "NVDA"}


def test_item_from_extracted_blank_content_is_none():
    item = Item.from_extracted({"url": "https://a.local/1", "title": "t", "content": "  "}, "api")
    assert item.content is None


def test_pipeline_persists_content_column(tmp_path):
    """回归:extract 显式映射 content 字段,items.content 列必须真的有数据。"""
    payloads = [
        {"title": "甲", "url": "https://api.demo.local/1", "body": "正文甲" * 50},
        {"title": "乙", "url": "https://api.demo.local/2", "body": "正文乙" * 50},
    ]
    config = make_config(
        sources=[
            {
                "name": "api",
                "engine": "direct_api",
                "url": "https://api.demo.local/list",
                "extract": {
                    "type": "json_path",
                    "fields": {
                        "title": "$[*].title",
                        "url": "$[*].url",
                        "content": "$[*].body",
                    },
                },
                "rate_limit": {"qps": 1000.0},
                "retry": 0,
            }
        ],
        classify={"builtin": False, "rules": []},  # 内置分类不命中会丢弃条目,本测只看 content 落库
    )
    store = SQLiteStore(tmp_path / "content.db")
    client = httpx.AsyncClient(transport=httpx.MockTransport(make_handler(payloads)))
    pipeline = Pipeline(config, store=store, client=client)
    try:
        result = asyncio.run(pipeline.run(dry_run=False))
        assert result.status == "success"
        rows = {r.url: r for r in store.list_items()}
        assert rows["https://api.demo.local/1"].content and "正文甲" in rows["https://api.demo.local/1"].content
        assert rows["https://api.demo.local/2"].content and "正文乙" in rows["https://api.demo.local/2"].content
    finally:
        store.close()


# ---------------------------------------------------------------------------
# trafilatura 兜底软信号(10-05-trafilatura-impl ②;research §3.1/§7-4)
# ---------------------------------------------------------------------------


class _FakeTrafilatura:
    """mock trafilatura(sys.modules 注入,同 tests/engines/test_static_html.py)。"""

    def __init__(self, payload: dict):
        self.payload = payload
        self.calls: list[str] = []

    def extract(self, html, *, url=None, output_format=None, with_metadata=None):
        self.calls.append(url)
        return json.dumps(self.payload)


_TRAF_DOC = {
    "title": "EXAMPLE 新闻网",
    "author": "张三",
    "date": "2026-10-05T08:00:00+08:00",
    "text": (
        "事故调查组周五发布了最终调查报告,指出起火原因与配电线路老化有关。"
        "报告全文共 87 页,涵盖了事发经过、责任认定与整改建议三个部分。"
        "调查组负责人在发布会上表示,涉事机库的配电线路自 2014 年以来未进行过"
        "大修,线路绝缘层多处破损,最终在持续高负载下短路起火。报告同时建议"
        "对同类机库进行全面电气安全排查,并在两年内完成整改。相关部门表示将"
        "采纳该建议,首批排查工作将于下月启动。"
    ),
    "description": "应被丢弃",
    "sitename": "应被丢弃",
}

_REVAMPED_PAGE = (
    "<html><head><title>最新资讯</title></head><body>"
    "<div class='card'><h3><a href='/items/2001'>台风路径最新预报</a></h3></div>"
    "</body></html>"
)


def _html_handler(payloads: dict[str, str]):
    """path-keyed HTML handler:robots 404 fail-open,页面按 path 返回。"""

    def handler(request: httpx.Request) -> httpx.Response:
        if request.url.path == "/robots.txt":
            return httpx.Response(404, text="")
        return httpx.Response(
            200,
            headers={"content-type": "text/html"},
            text=payloads.get(request.url.path, _REVAMPED_PAGE),
        )

    return handler


def test_rules_empty_fallback_records_warning_not_failure(tmp_path, monkeypatch):
    """② 软信号:规则跑空+兜底出条 → fetch 阶段 warnings 出
    extract_rules_empty_fallback(降级注记通道,不翻 run 状态、不计 partial)。"""
    monkeypatch.setitem(sys.modules, "trafilatura", _FakeTrafilatura(_TRAF_DOC))
    monkeypatch.setenv("MYIA_EXTRACT_FALLBACK", "1")
    store = SQLiteStore(tmp_path / "p.db")
    config = make_config(
        sources=[
            {
                "name": "revamped",
                "engine": "static_html",
                "url": "https://revamped.demo.local/news",
                # 规则在(旧结构 div.list),页面已改版(.card)→ 整页跑空
                "extract": {
                    "type": "list",
                    "item": "div.list div.item",
                    "fields": {"title": "h3 a", "url": "h3 a@href"},
                },
            }
        ],
        classify={"builtin": False, "rules": []},
        push=[{"channel": "stdout"}],
    )
    pipeline, _clock = make_pipeline(config, handler=_html_handler({}), store=store)
    result = asyncio.run(pipeline.run())

    fetch = result.stage("fetch")
    assert fetch.status == "ok"
    assert fetch.warnings == [
        {
            "source": "revamped",
            "engine": "static_html",
            "error_type": "extract_rules_empty_fallback",
            "message": "规则跑空(整页 0 条),trafilatura 兜底出条;规则选择器疑已失效",
            "fallback_items": 1,
        }
    ]
    assert fetch.failures == []  # 降级注记不并 failures(resolve_status 不计 partial)
    assert result.status == "success"  # 自动恢复,不翻 run 状态
    assert fetch.items_out == 1
    store.close()


def test_missing_rules_fallback_no_rules_empty_warning(tmp_path, monkeypatch):
    """① 无规则兜底出条:不挂 rules_empty 注记(源没配规则无所谓「已烂」),
    doctor 由源配置即可分辨①②。"""
    monkeypatch.setitem(sys.modules, "trafilatura", _FakeTrafilatura(_TRAF_DOC))
    monkeypatch.setenv("MYIA_EXTRACT_FALLBACK", "1")
    store = SQLiteStore(tmp_path / "p.db")
    config = make_config(
        sources=[
            {
                "name": "norules",
                "engine": "static_html",
                "url": "https://norules.demo.local/story",
            }
        ],
        classify={"builtin": False, "rules": []},
        push=[{"channel": "stdout"}],
    )
    pipeline, _clock = make_pipeline(config, handler=_html_handler({}), store=store)
    result = asyncio.run(pipeline.run())

    fetch = result.stage("fetch")
    assert fetch.status == "ok"
    assert fetch.warnings == []
    assert fetch.items_out == 1  # ①兜底出条,零软信号
    store.close()
