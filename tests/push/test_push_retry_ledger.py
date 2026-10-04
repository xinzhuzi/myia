"""Tests for myssia.push.retry_ledger — R1 投递重试账本(10-05-push-reliability-batch)。

蓝本对照:NousResearch/Hermes-Agent ``gateway/delivery_ledger.py``(MIT)。
覆盖 AC1 全项(fake clock):瞬态失败入队 → 到期重投 → 3 次耗尽 abandoned
→ 24h 过期清理 → 成功出队 → 死信不入队 → 原子写容错;外加 send_immediate
集成(legacy/定向/意外异常/digest 留池不掺和)与 pipeline 接线(每轮 run
推送阶段先 flush 到期条目)。全程零外网零真发零真实钥匙串(fake 通道注入)。
"""

from __future__ import annotations

import asyncio
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import httpx
import pytest

import myssia.pipeline as pipeline_module
from myssia.pipeline import Pipeline
from myssia.push.base import PushSendError
from myssia.push.delivery import DeliveryLedger
from myssia.push.digest import DigestAggregator, send_immediate
from myssia.push.directory import ChannelDirectory, ChannelEntry
from myssia.push.retry_ledger import (
    MAX_ATTEMPTS,
    RETRY_BACKOFF_SECONDS,
    RETRY_LEDGER_FILENAME,
    STALE_AFTER_SECONDS,
    PushRetryLedger,
)
from myssia.schema import load_category
from myssia.store import SQLiteStore

#: 瞬态错误样本(分类器判 None,不标死信)。
TRANSIENT = PushSendError("http_error", "ConnectError: connection refused")

#: 现场发送用的条目(纯 dict,通道渲染只读 view)。
ITEM = {"title": "免费送 NAS 券", "url": "https://demo.local/1", "dedup_key": "k1"}

#: send_immediate 的 now 参数(槽位推导用,与账本时钟独立)。
NOW = datetime(2026, 10, 5, 10, 0, tzinfo=timezone.utc)


class ManualClock:
    """可手动推进的秒级时钟(fake clock):退避/过期断言不真等。"""

    def __init__(self, start: float = 1_700_000_000.0) -> None:
        self.now = start

    def __call__(self) -> float:
        return self.now

    def advance(self, seconds: float) -> None:
        self.now += seconds


async def _no_sleep(seconds: float) -> None:
    """不真睡的注入 sleep(隔离管线退避)。"""


class FlakyChannel:
    """legacy fake 通道:前 ``fail_next`` 次抛瞬态错误,之后成功。"""

    name = "flaky"
    supports_targeting = False

    def __init__(self, fail_next: int = 0) -> None:
        self.fail_next = fail_next
        self.calls: list[dict[str, Any]] = []

    async def send(self, items, context) -> None:
        self.calls.append({"items": list(items), "context": context})
        if self.fail_next > 0:
            self.fail_next -= 1
            raise TRANSIENT


class FakeTargetingChannel:
    """支持寻址的 fake 通道:按 chat_id 抛指定错误(定向路径集成用)。"""

    name = "flaky_targeting"
    supports_targeting = True

    def __init__(self, failures: dict[str, BaseException] | None = None) -> None:
        self.failures = failures or {}
        self.calls: list[dict[str, Any]] = []

    async def send(self, items, context) -> None:
        self.calls.append({"items": list(items), "context": context})
        failure = self.failures.get(context.target.chat_id)
        if failure is not None:
            raise failure


class FlakyStdout:
    """管线接线用 stdout 假体:类级剩余失败次数跨实例(run 间)共享。"""

    name = "stdout"
    fail_remaining = 0
    instances: list["FlakyStdout"] = []

    def __init__(self, **kwargs: Any) -> None:
        self.calls: list[dict[str, Any]] = []
        FlakyStdout.instances.append(self)

    async def send(self, items, context) -> None:
        self.calls.append({"items": list(items), "context": context})
        if FlakyStdout.fail_remaining > 0:
            FlakyStdout.fail_remaining -= 1
            raise TRANSIENT

    @classmethod
    def total_calls(cls) -> int:
        return sum(len(instance.calls) for instance in cls.instances)

    @classmethod
    def reset(cls, fail_remaining: int = 0) -> None:
        cls.fail_remaining = fail_remaining
        cls.instances = []


def _directory(tmp_path: Path, entries: list[ChannelEntry]) -> ChannelDirectory:
    directory = ChannelDirectory(tmp_path)
    directory.replace_platform("fake", entries, now=1.0)
    return directory


def _run(coro):
    return asyncio.run(coro)


def _enqueue(ledger: PushRetryLedger, *, channel: str = "flaky", **overrides) -> bool:
    kwargs: dict[str, Any] = {
        "channel": channel,
        "items": [ITEM],
        "error": TRANSIENT,
        "kind": "immediate",
    }
    kwargs.update(overrides)
    return ledger.enqueue_failure(**kwargs)


# ---------------------------------------------------------------------------
# 入队门槛(瞬态入队 / 死信不入队 / 配置级不入队 / digest 不入队)
# ---------------------------------------------------------------------------


class TestEnqueueFailure:
    def test_transient_immediate_failure_enqueues_with_first_backoff(self, tmp_path: Path):
        clock = ManualClock()
        ledger = PushRetryLedger(tmp_path, clock=clock)

        assert _enqueue(ledger) is True

        entry = ledger.snapshot()[0]
        assert entry.state == "pending"
        assert entry.attempts == 0
        assert entry.next_retry_at == clock.now + RETRY_BACKOFF_SECONDS[0]  # 30s 档
        assert entry.channel == "flaky"
        assert entry.dedup_key == "k1"
        assert entry.items == [ITEM]  # item_view 序列化原样可重投
        assert entry.last_error == str(TRANSIENT)
        # 持久化往返 + 惰性建文件(构造不落盘,首次变更才写)
        assert (tmp_path / RETRY_LEDGER_FILENAME).exists()
        assert PushRetryLedger(tmp_path, clock=clock).pending_count() == 1

    def test_construction_never_creates_file(self, tmp_path: Path):
        PushRetryLedger(tmp_path)

        assert not (tmp_path / RETRY_LEDGER_FILENAME).exists()

    def test_dead_error_never_enqueues(self, tmp_path: Path):
        ledger = PushRetryLedger(tmp_path, clock=ManualClock())
        dead = PushSendError("feishu_api_error", "code=403 msg=forbidden: bot was blocked")

        assert (
            ledger.enqueue_failure(
                channel="flaky", items=[ITEM], error=dead, kind="immediate"
            )
            is False
        )
        assert ledger.pending_count() == 0
        assert ledger.snapshot() == []

    def test_config_error_never_enqueues(self, tmp_path: Path):
        ledger = PushRetryLedger(tmp_path, clock=ManualClock())
        config_error = PushSendError("env_var_missing", "环境变量未设置")

        assert (
            ledger.enqueue_failure(
                channel="flaky", items=[ITEM], error=config_error, kind="immediate"
            )
            is False
        )
        assert ledger.pending_count() == 0

    def test_digest_kind_never_enqueues(self, tmp_path: Path):
        ledger = PushRetryLedger(tmp_path, clock=ManualClock())

        assert _enqueue(ledger, kind="digest") is False
        assert ledger.pending_count() == 0

    def test_reenqueue_same_identity_preserves_budget(self, tmp_path: Path):
        clock = ManualClock()
        ledger = PushRetryLedger(tmp_path, clock=clock)

        assert _enqueue(ledger) is True
        clock.advance(RETRY_BACKOFF_SECONDS[0])
        due = ledger.claim_due(now=clock.now)
        assert len(due) == 1
        assert ledger.mark_failed(due[0].entry_id, TRANSIENT, now=clock.now) is True

        # 同一条目下一轮 run 现场又失败:预算不重置(不为反复失败续命),
        # 只刷新 last_error。
        assert _enqueue(ledger) is False
        entry = [e for e in ledger.snapshot() if e.state != "abandoned"][0]
        assert entry.attempts == 1
        assert entry.next_retry_at == clock.now + RETRY_BACKOFF_SECONDS[1]  # 120s 档

    def test_different_target_spec_is_distinct_entry(self, tmp_path: Path):
        ledger = PushRetryLedger(tmp_path, clock=ManualClock())

        assert _enqueue(ledger, target_spec="fake:群一") is True
        assert _enqueue(ledger, target_spec="fake:群二") is True

        assert ledger.pending_count() == 2


# ---------------------------------------------------------------------------
# 到期重投(退避/通道过滤/崩溃残留再认领/退避档位)
# ---------------------------------------------------------------------------


class TestClaimDue:
    def test_claim_waits_for_backoff_then_persists_attempting(self, tmp_path: Path):
        clock = ManualClock()
        ledger = PushRetryLedger(tmp_path, clock=clock)
        _enqueue(ledger)

        clock.advance(RETRY_BACKOFF_SECONDS[0] - 1)
        assert ledger.claim_due(now=clock.now) == []  # 差 1 秒未到期

        clock.advance(1)
        due = ledger.claim_due(now=clock.now)
        assert len(due) == 1
        assert due[0].attempts == 1  # 认领即计(蓝本同款,崩溃不退款)
        assert due[0].state == "attempting"
        # 认领先落盘再发送:崩溃在重投途中也留下 attempting 证据
        reloaded = PushRetryLedger(tmp_path, clock=clock)
        assert [e.state for e in reloaded.snapshot()] == ["attempting"]
        assert [e.attempts for e in reloaded.snapshot()] == [1]

    def test_channel_filter_scopes_claims(self, tmp_path: Path):
        clock = ManualClock()
        ledger = PushRetryLedger(tmp_path, clock=clock)
        _enqueue(ledger, channel="feishu_card")
        _enqueue(ledger, channel="telegram")

        clock.advance(RETRY_BACKOFF_SECONDS[0])
        due = ledger.claim_due(channel="feishu_card", now=clock.now)

        assert [e.channel for e in due] == ["feishu_card"]
        # feishu_card 已认领(attempting=在途重投),telegram 原封不动
        states = {e.channel: e.state for e in ledger.snapshot()}
        assert states == {"feishu_card": "attempting", "telegram": "pending"}
        assert ledger.pending_count(channel="telegram") == 1

    def test_crashed_attempting_entry_is_reclaimed_immediately(self, tmp_path: Path):
        """蓝本 boot-sweep 语义:认领后进程崩溃(无结转),下一轮 run 的新
        实例即刻再认领——at-least-once(平台可能已收到上一击,可能重复)。"""
        clock = ManualClock()
        ledger = PushRetryLedger(tmp_path, clock=clock)
        _enqueue(ledger)
        clock.advance(RETRY_BACKOFF_SECONDS[0])
        assert len(ledger.claim_due(now=clock.now)) == 1
        # 「崩溃」:不 mark_delivered/mark_failed,后继实例从盘上接手
        successor = PushRetryLedger(tmp_path, clock=clock)

        due = successor.claim_due(now=clock.now)

        assert len(due) == 1
        assert due[0].attempts == 2

    def test_backoff_tiers_30_120_then_final_strike(self, tmp_path: Path):
        """退避档位对齐蓝本 retry_not_before:30s → 120s → 最后一击不设
        等待(立即到期,交给下一轮 run 的 flush——蓝本「留最后一击给
        boot sweep」的 MYIA 形态)。"""
        clock = ManualClock()
        ledger = PushRetryLedger(tmp_path, clock=clock)
        _enqueue(ledger)
        entry_id = ledger.snapshot()[0].entry_id
        assert ledger.snapshot()[0].next_retry_at == clock.now + RETRY_BACKOFF_SECONDS[0]

        clock.advance(RETRY_BACKOFF_SECONDS[0])  # 第 1 击到期
        assert len(ledger.claim_due(now=clock.now)) == 1
        ledger.mark_failed(entry_id, TRANSIENT, now=clock.now)
        assert ledger.snapshot()[0].next_retry_at == clock.now + RETRY_BACKOFF_SECONDS[1]

        clock.advance(RETRY_BACKOFF_SECONDS[1])  # 第 2 击到期
        due = ledger.claim_due(now=clock.now)
        assert [e.attempts for e in due] == [2]
        ledger.mark_failed(entry_id, TRANSIENT, now=clock.now)
        assert ledger.snapshot()[0].next_retry_at == clock.now  # 最后一击:立即到期

        due = ledger.claim_due(now=clock.now)  # 下一轮 flush 即刻认领
        assert [e.attempts for e in due] == [MAX_ATTEMPTS]


# ---------------------------------------------------------------------------
# 预算耗尽 / 24h 过期 / 成功出队
# ---------------------------------------------------------------------------


class TestOutcome:
    def test_exhausted_entry_abandoned_and_kept_for_observation(self, tmp_path: Path):
        clock = ManualClock()
        ledger = PushRetryLedger(tmp_path, clock=clock)
        _enqueue(ledger)
        entry_id = ledger.snapshot()[0].entry_id

        for expected_attempts in range(1, MAX_ATTEMPTS + 1):
            clock.advance(
                max(0.0, (ledger.snapshot()[0].next_retry_at or clock.now) - clock.now)
            )
            due = ledger.claim_due(now=clock.now)
            assert [e.attempts for e in due] == [expected_attempts]
            ledger.mark_failed(entry_id, TRANSIENT, now=clock.now)

        entry = ledger.snapshot()[0]
        assert entry.state == "abandoned"
        assert "耗尽" in entry.last_error
        assert ledger.pending_count() == 0  # 不再认领
        assert ledger.claim_due(now=clock.now) == []
        # abandoned 记录留观察窗(盘上可查),不即删
        assert PushRetryLedger(tmp_path, clock=clock).snapshot()[0].state == "abandoned"

    def test_stale_entry_expired_after_24h(self, tmp_path: Path):
        clock = ManualClock()
        ledger = PushRetryLedger(tmp_path, clock=clock)
        _enqueue(ledger)

        clock.advance(STALE_AFTER_SECONDS + 1)

        assert ledger.claim_due(now=clock.now) == []
        entry = ledger.snapshot()[0]
        assert entry.state == "abandoned"
        assert "24h" in entry.last_error

    def test_abandoned_records_pruned_after_observation_window(self, tmp_path: Path):
        clock = ManualClock()
        ledger = PushRetryLedger(tmp_path, clock=clock)
        _enqueue(ledger)
        clock.advance(STALE_AFTER_SECONDS + 1)
        ledger.claim_due(now=clock.now)  # 触发 sweep → abandoned(updated_at=now)

        clock.advance(STALE_AFTER_SECONDS + 1)  # 观察窗也过
        ledger.claim_due(now=clock.now)

        assert ledger.snapshot() == []
        assert json.loads((tmp_path / RETRY_LEDGER_FILENAME).read_text(encoding="utf-8"))["entries"] == {}

    def test_delivered_entry_leaves_queue(self, tmp_path: Path):
        clock = ManualClock()
        ledger = PushRetryLedger(tmp_path, clock=clock)
        _enqueue(ledger)
        clock.advance(RETRY_BACKOFF_SECONDS[0])
        entry_id = ledger.claim_due(now=clock.now)[0].entry_id

        assert ledger.mark_delivered(entry_id, now=clock.now) is True

        assert ledger.pending_count() == 0
        assert ledger.snapshot() == []
        assert json.loads((tmp_path / RETRY_LEDGER_FILENAME).read_text(encoding="utf-8"))["entries"] == {}
        assert ledger.mark_delivered(entry_id, now=clock.now) is False  # 幂等

    def test_abandon_terminal_skip(self, tmp_path: Path):
        clock = ManualClock()
        ledger = PushRetryLedger(tmp_path, clock=clock)
        _enqueue(ledger)
        entry_id = ledger.snapshot()[0].entry_id

        assert ledger.abandon(entry_id, "重投被终态跳过(死信/对象未解析)", now=clock.now) is True

        entry = ledger.snapshot()[0]
        assert entry.state == "abandoned"
        assert "终态跳过" in entry.last_error
        assert ledger.abandon(entry_id, "again", now=clock.now) is False


# ---------------------------------------------------------------------------
# 原子写容错(不可写根/损坏文件/坏条目/无 tmp 残留)
# ---------------------------------------------------------------------------


class TestAtomicWriteTolerance:
    def test_unwritable_root_keeps_memory_state(self, tmp_path: Path):
        root = tmp_path / "ro"
        root.mkdir()
        root.chmod(0o500)
        try:
            clock = ManualClock()
            ledger = PushRetryLedger(root, clock=clock)

            assert _enqueue(ledger) is True  # 不抛,内存态继续
            assert ledger.pending_count() == 1
            clock.advance(RETRY_BACKOFF_SECONDS[0])
            due = ledger.claim_due(now=clock.now)
            assert len(due) == 1
            assert ledger.mark_delivered(due[0].entry_id, now=clock.now) is True
            assert ledger.pending_count() == 0
        finally:
            root.chmod(0o700)

    def test_corrupt_file_degrades_to_empty_then_rewrites(self, tmp_path: Path):
        (tmp_path / RETRY_LEDGER_FILENAME).write_text("{broken", encoding="utf-8")

        ledger = PushRetryLedger(tmp_path, clock=ManualClock())

        assert ledger.snapshot() == []
        assert _enqueue(ledger) is True
        # 恢复写路径后文件重新成为合法 JSON
        raw = json.loads((tmp_path / RETRY_LEDGER_FILENAME).read_text(encoding="utf-8"))
        assert len(raw["entries"]) == 1

    def test_malformed_entries_dropped_on_load(self, tmp_path: Path):
        ledger = PushRetryLedger(tmp_path, clock=ManualClock())
        _enqueue(ledger)
        good_id = ledger.snapshot()[0].entry_id
        raw = json.loads((tmp_path / RETRY_LEDGER_FILENAME).read_text(encoding="utf-8"))
        raw["entries"]["bad"] = "not-a-dict"
        raw["entries"]["worse"] = {"channel": 123, "items": []}
        (tmp_path / RETRY_LEDGER_FILENAME).write_text(json.dumps(raw), encoding="utf-8")

        reloaded = PushRetryLedger(tmp_path, clock=ManualClock())

        assert [e.entry_id for e in reloaded.snapshot()] == [good_id]

    def test_atomic_write_leaves_no_tmp_and_file_always_parseable(self, tmp_path: Path):
        clock = ManualClock()
        ledger = PushRetryLedger(tmp_path, clock=clock)
        _enqueue(ledger)

        def assert_clean_state() -> None:
            assert list(tmp_path.glob("*.tmp")) == []
            json.loads((tmp_path / RETRY_LEDGER_FILENAME).read_text(encoding="utf-8"))

        assert_clean_state()
        clock.advance(RETRY_BACKOFF_SECONDS[0])
        entry_id = ledger.claim_due(now=clock.now)[0].entry_id
        assert_clean_state()
        ledger.mark_failed(entry_id, TRANSIENT, now=clock.now)
        assert_clean_state()
        ledger.mark_delivered(entry_id, now=clock.now)
        assert_clean_state()


# ---------------------------------------------------------------------------
# send_immediate 集成(fake clock;legacy/定向/意外异常/digest 留池)
# ---------------------------------------------------------------------------


class TestSendImmediateIntegration:
    def test_transient_failure_via_send_immediate_enqueues(self, tmp_path: Path):
        ledger = PushRetryLedger(tmp_path, clock=ManualClock())
        channel = FlakyChannel(fail_next=1)

        reports = _run(
            send_immediate([ITEM], channels=[channel], retry_ledger=ledger, now=NOW)
        )

        assert reports[0].ok is False
        assert ledger.pending_count() == 1
        entry = ledger.snapshot()[0]
        assert entry.channel == "flaky"
        assert entry.items == [ITEM]
        assert entry.target_spec is None

    def test_dead_error_via_send_immediate_not_enqueued(self, tmp_path: Path):
        ledger = PushRetryLedger(tmp_path, clock=ManualClock())

        class DeadChannel:
            name = "flaky"
            supports_targeting = False

            async def send(self, items, context):
                raise PushSendError(
                    "feishu_api_error", "code=403 msg=forbidden: bot was blocked"
                )

        reports = _run(
            send_immediate([ITEM], channels=[DeadChannel()], retry_ledger=ledger, now=NOW)
        )

        assert reports[0].ok is False
        assert ledger.pending_count() == 0

    def test_config_error_via_send_immediate_not_enqueued(self, tmp_path: Path):
        ledger = PushRetryLedger(tmp_path, clock=ManualClock())

        class ConfigBroken:
            name = "flaky"
            supports_targeting = False

            async def send(self, items, context):
                raise PushSendError("env_var_missing", "环境变量 FEISHU_TOKEN 未设置")

        reports = _run(
            send_immediate([ITEM], channels=[ConfigBroken()], retry_ledger=ledger, now=NOW)
        )

        assert reports[0].ok is False
        assert "[env_var_missing]" in reports[0].error
        assert ledger.pending_count() == 0

    def test_unexpected_exception_enqueues_with_bounded_budget(self, tmp_path: Path):
        ledger = PushRetryLedger(tmp_path, clock=ManualClock())

        class Buggy:
            name = "flaky"
            supports_targeting = False

            async def send(self, items, context):
                raise RuntimeError("模板渲染意外崩溃")

        reports = _run(
            send_immediate([ITEM], channels=[Buggy()], retry_ledger=ledger, now=NOW)
        )

        assert reports[0].ok is False
        assert "[unexpected]" in reports[0].error
        assert ledger.pending_count() == 1  # 未知异常也入账(at-least-once,预算封顶)

    def test_targeted_transient_failure_enqueues_with_source_spec(self, tmp_path: Path):
        directory = _directory(
            tmp_path,
            [
                ChannelEntry(platform="fake", chat_id="c1", name="群一"),
                ChannelEntry(platform="fake", chat_id="c2", name="群二"),
            ],
        )
        ledger = PushRetryLedger(tmp_path, clock=ManualClock())
        channel = FakeTargetingChannel(failures={"c2": TRANSIENT})

        reports = _run(
            send_immediate(
                [ITEM],
                channels=[channel],
                item_specs=[["fake:群一", "fake:群二"]],
                directory=directory,
                ledger=DeliveryLedger(tmp_path),
                retry_ledger=ledger,
                now=NOW,
            )
        )

        assert [r.ok for r in reports] == [True, False]  # 群一成功,群二瞬态失败
        assert ledger.pending_count() == 1
        entry = ledger.snapshot()[0]
        assert entry.target_spec == "fake:群二"  # 源 spec 入账,重投走原路
        assert entry.items == [ITEM]
        # 瞬态不标死信(与既有 delivery 语义一致)
        assert DeliveryLedger(tmp_path).dead_keys() == []

    def test_digest_flush_failure_not_enqueued(self, tmp_path: Path):
        """digest 全通道失败有留池机制(digest.py 契约),不掺和重试账本。"""
        ledger = PushRetryLedger(tmp_path, clock=ManualClock())
        aggregator = DigestAggregator(channels=[FlakyChannel(fail_next=99)])
        aggregator.add(ITEM)

        reports = _run(aggregator.flush())

        assert reports and reports[0].ok is False
        assert len(aggregator) == 1  # 留池待下轮 flush
        assert ledger.pending_count() == 0

    def test_full_heal_loop_with_fake_clock(self, tmp_path: Path):
        """端到端 at-least-once:现场失败 → 到期认领 → 重投成功 → 出队。"""
        clock = ManualClock()
        ledger = PushRetryLedger(tmp_path, clock=clock)
        channel = FlakyChannel(fail_next=1)

        reports = _run(
            send_immediate([ITEM], channels=[channel], retry_ledger=ledger, now=NOW)
        )
        assert reports[0].ok is False
        assert ledger.pending_count() == 1

        clock.advance(RETRY_BACKOFF_SECONDS[0])  # 退避到点(通道已自愈)
        due = ledger.claim_due(now=clock.now)
        assert [e.attempts for e in due] == [1]

        retry_reports = _run(
            send_immediate(
                due[0].items,
                channels=[channel],
                item_specs=[[due[0].target_spec]] if due[0].target_spec else None,
                now=NOW,
            )
        )
        assert retry_reports[0].ok is True
        assert ledger.mark_delivered(due[0].entry_id, now=clock.now) is True
        assert ledger.pending_count() == 0
        assert channel.calls[1]["items"] == [ITEM]  # 重投携带原条目
        assert channel.calls[1]["context"].kind == "immediate"


# ---------------------------------------------------------------------------
# pipeline 接线(每轮 run 推送阶段先 flush 到期条目)
# ---------------------------------------------------------------------------


def _make_handler():
    def handler(request: httpx.Request) -> httpx.Response:
        if request.url.path == "/robots.txt":
            return httpx.Response(404, text="")
        return httpx.Response(
            200,
            json=[{"title": "免费送 NAS 券", "url": "https://api.demo.local/0"}],
        )

    return handler


def _make_config():
    return load_category(
        {
            "id": "demo",
            "name": "演示品类",
            "schedule": "0 9 * * *",
            "timezone": "Asia/Shanghai",
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
    )


def _run_once(tmp_path: Path, config, manual: ManualClock):
    store = SQLiteStore(tmp_path / "p.db")
    client = httpx.AsyncClient(transport=httpx.MockTransport(_make_handler()))
    pipeline = Pipeline(
        config,
        db_path=tmp_path / "p.db",
        store=store,
        client=client,
        clock=lambda: manual.now,
        sleep=_no_sleep,
        wall_clock=lambda: datetime.fromtimestamp(manual.now, tz=timezone.utc),
    )
    try:
        return asyncio.run(pipeline.run())
    finally:
        store.close()


@pytest.fixture(autouse=True)
def _reset_flaky_stdout():
    FlakyStdout.reset()
    yield
    FlakyStdout.reset()


class TestPipelineWiring:
    def test_run_flushes_due_retry_at_push_stage(self, tmp_path: Path, monkeypatch):
        monkeypatch.setattr(
            pipeline_module, "CHANNELS", {**pipeline_module.CHANNELS, "stdout": FlakyStdout}
        )
        monkeypatch.setattr(pipeline_module, "PLATFORMS", {})
        FlakyStdout.reset(fail_remaining=1)
        manual = ManualClock()
        config = _make_config()

        result1 = _run_once(tmp_path, config, manual)

        # 现场发送瞬态失败 → 入账(at-least-once;原先失败即丢)
        assert result1.pushes[0].ok is False
        ledger = PushRetryLedger(tmp_path)
        assert ledger.pending_count(channel="stdout") == 1
        assert ledger.snapshot()[0].next_retry_at > manual.now  # 未到期,本轮不冲

        manual.advance(RETRY_BACKOFF_SECONDS[0] + 1)  # 退避到点(通道已自愈)
        result2 = _run_once(tmp_path, config, manual)

        assert PushRetryLedger(tmp_path).pending_count() == 0  # 重投成功出队
        assert result2.pushes[0].ok is True
        # 全程恰好两击:run1 现场失败一击 + run2 推送阶段开头重投成功一击
        assert FlakyStdout.total_calls() == 2
        kinds = [c["context"].kind for i in FlakyStdout.instances for c in i.calls]
        assert kinds == ["immediate", "immediate"]

    def test_undue_entry_not_flushed_early(self, tmp_path: Path, monkeypatch):
        monkeypatch.setattr(
            pipeline_module, "CHANNELS", {**pipeline_module.CHANNELS, "stdout": FlakyStdout}
        )
        monkeypatch.setattr(pipeline_module, "PLATFORMS", {})
        FlakyStdout.reset(fail_remaining=1)
        manual = ManualClock()
        config = _make_config()

        _run_once(tmp_path, config, manual)  # 失败入账
        manual.advance(RETRY_BACKOFF_SECONDS[0] - 1)  # 差 1 秒未到期
        result2 = _run_once(tmp_path, config, manual)

        assert PushRetryLedger(tmp_path).pending_count() == 1  # 未到期不冲账
        assert FlakyStdout.total_calls() == 1  # 无重投击发
        assert result2.pushes[0].ok is True  # 本轮无新失败

    def test_targeted_retry_resends_to_resolved_target_not_exploded(
        self, tmp_path: Path
    ):
        """定向重投按源 spec 解析到原对象(换眼复审 R1-high 回归)。

        修复前:``item_specs=[entry.target_spec]`` 把单字符串当「每条目的
        spec 列表」传给 send_immediate,内部 ``list(specs)`` 逐字符炸开
        ('f','a','k','e',':','群','二'),全部单字符 spec 解析失败 →
        7×skipped 报告 → 冲账侧误判「死信/对象未解析」终态放弃——瞬态
        失败一次认领即灭,at-least-once 对所有定向 immediate 失效且日志
        归因错误。修复后:spec 包成列表,经目录解析回原对象、成功出队。
        """
        manual = ManualClock()
        store = SQLiteStore(tmp_path / "p.db")
        client = httpx.AsyncClient(transport=httpx.MockTransport(_make_handler()))
        pipeline = Pipeline(
            _make_config(),
            db_path=tmp_path / "p.db",
            store=store,
            client=client,
            clock=lambda: manual.now,
            sleep=_no_sleep,
            wall_clock=lambda: datetime.fromtimestamp(manual.now, tz=timezone.utc),
        )
        try:
            # 预置通道目录(replace_platform 为内存桶替换,directory.py:347;
            # 持久化走 refresh 流程,与本测试无关)——对 Pipeline 自持的
            # directory 实例预置,重投解析走真目录。
            pipeline._channel_directory.replace_platform(
                "fake", [ChannelEntry(platform="fake", chat_id="c2", name="群二")], now=1.0
            )
            assert pipeline._retry_ledger.enqueue_failure(
                channel="flaky_targeting",
                items=[ITEM],
                target_spec="fake:群二",
                error=TRANSIENT,
                kind="immediate",
            )
            manual.advance(RETRY_BACKOFF_SECONDS[0] + 1)  # 到期

            channel = FakeTargetingChannel()  # 通道已自愈,重投应成功

            async def scenario():
                registry = pipeline._ensure_registry(store)
                return await pipeline._flush_push_retries(
                    channel, registry, datetime.fromtimestamp(manual.now, tz=timezone.utc)
                )

            reports = asyncio.run(scenario())

            assert [r.ok for r in reports] == [True]  # 修复前:7×skipped 全 False
            # 重投按源 spec 解析回原对象(修复前:单字符 spec 全解析失败,零发送)
            assert len(channel.calls) == 1
            assert channel.calls[0]["context"].target.chat_id == "c2"
            assert channel.calls[0]["items"] == [ITEM]
            assert channel.calls[0]["context"].kind == "immediate"
            # 成功出队,而非误判终态放弃(修复前:abandoned 记录带错归因文案)
            assert pipeline._retry_ledger.snapshot() == []
            assert PushRetryLedger(tmp_path).snapshot() == []
        finally:
            store.close()
