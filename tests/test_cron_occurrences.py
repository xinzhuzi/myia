"""Cron occurrences:到期身份去重 + pending_slot(tests 冻结命名,
10-04-hermes-cron implement A5)。

覆盖 :mod:`myia.cron.occurrences` 全函数面(上游 ``cron/occurrences.py``
102 行全文对照):

- ``scheduled_instant``:aware ISO → UTC 规范化;naive/非串/垃圾 → None
  (无精确身份;复用 executions.canonical_scheduled_instant,A3 注);
- ``completed_occurrence``:completed 行 → True(含日志);failed/unknown 行
  → False(证不了完成);毒行(完成时刻早于所认领 occurrence 减偏斜窗)→
  忽略;账本异常 → False;跳过的告警是唯一痕迹(#111414);
- ``pending_slot_stamp``:存储形状(scheduled_at/at/by=machine_id);
- ``unclaimed_pending_slot``:非 recurring → None;残缺戳/坏 ISO → None;
  本进程在跑 → None;他进程戳且租约内 → None;属主可证死/租约过/本机戳
  → 恢复恰一次(#107485 的读取侧)。

上游对照:`~/.hermes/hermes-agent/cron/occurrences.py`。控时纪律(ground-
truth B16):显式 aware datetime 注入,时区显式 ZoneInfo。
"""

from __future__ import annotations

import socket
import subprocess
import sys
from datetime import datetime, timedelta, timezone
from typing import Any, Optional
from zoneinfo import ZoneInfo

import pytest

from myia.cron import occurrences
from myia.cron.executions import ExecutionLedger
from myia.cron.jobs import machine_id, try_register_running_job, release_running_job

TZ = ZoneInfo("Asia/Shanghai")
NOW = datetime(2026, 10, 4, 9, 6, tzinfo=TZ)
FIRE_TTL_OVER = 301  # 恰过 FIRE_CLAIM_TTL_SECONDS(300s)的窗


@pytest.fixture()
def ledger(tmp_path: Any) -> ExecutionLedger:
    return ExecutionLedger.for_db(tmp_path / "myia.db")


def make_job(job_id: str = "job-1", **overrides: Any) -> dict[str, Any]:
    base: dict[str, Any] = {
        "id": job_id,
        "name": f"job {job_id}",
        "schedule": {"kind": "interval", "minutes": 5, "display": "every 5m"},
        "next_run_at": "2026-10-04T09:05:00+08:00",
    }
    base.update(overrides)
    return base


def seed_execution(
    ledger: ExecutionLedger,
    *,
    status: str,
    scheduled_instant: Optional[str],
    finished_at: Optional[str] = None,
    claimed_at: Optional[str] = None,
) -> str:
    """绕过状态机直插一行(任意 status/时刻,模拟前任宿主留下的账本)。"""
    execution_id = (
        f"exec-{status}-{abs(hash((status, scheduled_instant, finished_at))) % 10**8}"
    )
    with ledger.transaction() as conn:
        conn.execute(
            """INSERT INTO executions
               (id, job_id, source, status, scheduled_instant, pid, process_start_time,
                claimed_at, started_at, finished_at)
               VALUES (?, 'job-1', 'tick', ?, ?, ?, ?, ?, ?, ?)""",
            (
                execution_id,
                status,
                scheduled_instant,
                0,
                None,
                claimed_at or "2026-10-04T01:00:00+00:00",
                None,
                finished_at,
            ),
        )
    return execution_id


# --- scheduled_instant ----------------------------------------------------------


@pytest.mark.parametrize(
    "value,expected",
    [
        ("2026-10-04T09:05:00+08:00", "2026-10-04T01:05:00+00:00"),  # 偏移换 UTC
        ("2026-10-04T01:05:00+00:00", "2026-10-04T01:05:00+00:00"),  # 幂等
        ("2026-10-04T09:05:00", None),  # naive:无精确身份
        (None, None),
        (123, None),
        (["x"], None),
        ("garbage", None),
        ("", None),
    ],
)
def test_scheduled_instant_canonicalizes(value: Any, expected: Optional[str]) -> None:
    assert occurrences.scheduled_instant(value) == expected


# --- completed_occurrence --------------------------------------------------------


def test_completed_row_proves_completion(
    ledger: ExecutionLedger,
    caplog: Any,
) -> None:
    instant = "2026-10-04T01:05:00+00:00"
    seed_execution(
        ledger,
        status="completed",
        scheduled_instant=instant,
        finished_at="2026-10-04T01:05:30+00:00",
    )
    with caplog.at_level("WARNING", logger="myia.cron.occurrences"):
        assert (
            occurrences.completed_occurrence(make_job(), instant, ledger=ledger) is True
        )
    # 跳过不落 run/账本行——告警是唯一痕迹(#111414)。
    assert any("already completed" in r.message for r in caplog.records)


def test_no_rows_or_unfinished_rows_do_not_prove(ledger: ExecutionLedger) -> None:
    instant = "2026-10-04T01:05:00+00:00"
    assert occurrences.completed_occurrence(make_job(), instant, ledger=ledger) is False
    # failed / unknown 尝试证明不了完成:槽保持可发。
    seed_execution(
        ledger,
        status="failed",
        scheduled_instant=instant,
        finished_at="2026-10-04T01:05:30+00:00",
    )
    seed_execution(
        ledger,
        status="unknown",
        scheduled_instant=instant,
        finished_at="2026-10-04T01:05:30+00:00",
    )
    assert occurrences.completed_occurrence(make_job(), instant, ledger=ledger) is False


def test_noncompleted_status_rows_are_invisible(ledger: ExecutionLedger) -> None:
    # 索引只取 status='completed' 的行:其余状态的 scheduled_instant 匹配不上。
    instant = "2026-10-04T01:05:00+00:00"
    seed_execution(ledger, status="running", scheduled_instant=instant)
    assert occurrences.completed_occurrence(make_job(), instant, ledger=ledger) is False


def test_other_instant_or_job_rows_do_not_match(ledger: ExecutionLedger) -> None:
    seed_execution(
        ledger,
        status="completed",
        scheduled_instant="2026-10-04T01:10:00+00:00",
        finished_at="2026-10-04T01:10:30+00:00",
    )
    assert (
        occurrences.completed_occurrence(
            make_job(), "2026-10-04T01:05:00+00:00", ledger=ledger
        )
        is False
    )
    # 同 instant 不同 job:按 (job_id, instant) 精确匹配。
    other = make_job("job-2")
    seed_execution(
        ledger,
        status="completed",
        scheduled_instant="2026-10-04T01:05:00+00:00",
        finished_at="2026-10-04T01:05:30+00:00",
    )
    # job-1 也有了(上一行 seed 是 job-1)——换 job-2 验证不串。
    assert (
        occurrences.completed_occurrence(
            other, "2026-10-04T01:05:00+00:00", ledger=ledger
        )
        is False
    )


def test_poison_row_ignored(ledger: ExecutionLedger) -> None:
    # 完成时刻早于「所认领 occurrence − 偏斜窗」= 确诊毒行(早到的完成证明
    # 不可能属于该槽),忽略之。
    instant = "2026-10-04T01:05:00+00:00"
    seed_execution(
        ledger,
        status="completed",
        scheduled_instant=instant,
        finished_at="2026-10-04T01:00:00+00:00",
    )  # 早 5 分钟 > SKEW(60s)
    assert occurrences.completed_occurrence(make_job(), instant, ledger=ledger) is False


def test_malformed_timestamps_remain_proof(ledger: ExecutionLedger) -> None:
    # 遗留/残缺时间戳仍是完成证明(只有确诊毒行才忽略)。
    instant = "2026-10-04T01:05:00+00:00"
    seed_execution(
        ledger,
        status="completed",
        scheduled_instant=instant,
        finished_at=None,
        claimed_at="not-a-date",
    )
    assert occurrences.completed_occurrence(make_job(), instant, ledger=ledger) is True


def test_naive_instant_has_no_identity(ledger: ExecutionLedger) -> None:
    seed_execution(
        ledger,
        status="completed",
        scheduled_instant="2026-10-04T01:05:00+00:00",
        finished_at="2026-10-04T01:05:30+00:00",
    )
    assert (
        occurrences.completed_occurrence(
            make_job(), "2026-10-04T01:05:00", ledger=ledger
        )
        is False
    )


def test_ledger_failure_fails_open(tmp_path: Any) -> None:
    class ExplodingLedger(ExecutionLedger):
        def transaction(self) -> Any:
            raise RuntimeError("ledger unavailable")

    assert (
        occurrences.completed_occurrence(
            make_job(), "2026-10-04T01:05:00+00:00", ledger=ExplodingLedger(tmp_path)
        )
        is False
    )


# --- pending_slot_stamp ----------------------------------------------------------


def test_pending_slot_stamp_shape() -> None:
    stamp = occurrences.pending_slot_stamp("2026-10-04T09:05:00+08:00", NOW)
    assert stamp == {
        "scheduled_at": "2026-10-04T09:05:00+08:00",
        "at": NOW.isoformat(),
        "by": machine_id(),
    }


# --- unclaimed_pending_slot ------------------------------------------------------


def own_stamp(slot: str, *, at: Optional[datetime] = None) -> dict[str, Any]:
    return {"scheduled_at": slot, "at": (at or NOW).isoformat(), "by": machine_id()}


def test_non_recurring_and_malformed_return_none() -> None:
    slot = "2026-10-04T09:05:00+08:00"
    # once job 不参与 pending_slot(一次性走 run_claim)。
    assert (
        occurrences.unclaimed_pending_slot(
            make_job(
                schedule={"kind": "once", "run_at": slot}, pending_slot=own_stamp(slot)
            ),
            NOW,
        )
        is None
    )
    # 戳不是 dict / 缺 scheduled_at / 坏 ISO → None(绝不当作 fire 信号)。
    assert occurrences.unclaimed_pending_slot(make_job(pending_slot="x"), NOW) is None
    assert (
        occurrences.unclaimed_pending_slot(
            make_job(pending_slot={"at": NOW.isoformat()}), NOW
        )
        is None
    )
    assert (
        occurrences.unclaimed_pending_slot(
            make_job(pending_slot=own_stamp("garbage")), NOW
        )
        is None
    )
    assert occurrences.unclaimed_pending_slot(make_job(), NOW) is None  # 无戳


def test_running_in_this_process_returns_none() -> None:
    slot = "2026-10-04T09:05:00+08:00"
    job = make_job(pending_slot=own_stamp(slot))
    try:
        assert try_register_running_job("job-1") is True
        # 排队 worker 会自行认领并清槽——扫描侧不得抢跑恢复。
        assert occurrences.unclaimed_pending_slot(job, NOW) is None
    finally:
        release_running_job("job-1")


def test_own_orphan_stamp_restores() -> None:
    # 本机戳 + job 不在本进程跑 = 孤儿戳(派发被拒)→ 恢复。
    slot = "2026-10-04T09:05:00+08:00"
    assert (
        occurrences.unclaimed_pending_slot(make_job(pending_slot=own_stamp(slot)), NOW)
        == slot
    )


def test_foreign_live_stamp_honoured() -> None:
    # 他进程戳、租约内(at 距 NOW < FIRE_CLAIM_TTL_SECONDS=300)→ 视为正在派发。
    slot = "2026-10-04T09:05:00+08:00"
    foreign = {
        "scheduled_at": slot,
        "at": (NOW - timedelta(seconds=60)).isoformat(),
        "by": f"other-host:{NOW.second}:tok",
    }
    assert (
        occurrences.unclaimed_pending_slot(make_job(pending_slot=foreign), NOW) is None
    )


def test_foreign_stamp_with_local_dead_owner_restores() -> None:
    # 他进程戳但属主是本机可证死进程 → 恢复(同机属主退出立即放行,不等 TTL)。
    child = subprocess.Popen([sys.executable, "-c", "import time; time.sleep(60)"])
    child.kill()
    child.wait()
    slot = "2026-10-04T09:05:00+08:00"
    dead = {
        "scheduled_at": slot,
        "at": (NOW - timedelta(seconds=60)).isoformat(),
        "by": f"{socket.gethostname()}:{child.pid}",
    }
    assert occurrences.unclaimed_pending_slot(make_job(pending_slot=dead), NOW) == slot


def test_expired_stamp_restores_regardless_of_owner() -> None:
    # 租约已过(at 距 NOW ≥ 300s)→ 属主死活都恢复恰一次。
    slot = "2026-10-04T09:05:00+08:00"
    expired = {
        "scheduled_at": slot,
        "at": (NOW - timedelta(seconds=FIRE_TTL_OVER)).isoformat(),
        "by": f"other-host:{NOW.second}:tok",
    }
    assert (
        occurrences.unclaimed_pending_slot(make_job(pending_slot=expired), NOW) == slot
    )
