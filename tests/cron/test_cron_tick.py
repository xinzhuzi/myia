"""tick 调度与监督 ticker(tests 冻结命名,10-04-hermes-cron implement A6)。

覆盖面(implement.md A6 六项 + 邻接语义):

- **文件锁单飞**:他者持锁 → 静默 return 0;并发双 tick 恰一个派发;
- **先推进后派发**(at-most-once):runner 运行时存储的 ``next_run_at``
  已是未来射点、occurrence 身份仍取派发快照;处理失败也消耗槽(二次
  tick 不重发);
- **并行池 / D13 分组**:不同 db 的 job 并行(Barrier 实证重叠)、同 db
  串行(组内活跃数恒 1);
- **单 job 失败不拖垮**:同组兄弟照跑,失败侧 streak/账本/last_error 落全;
- **ticker respawn**:SupervisedTickerThread 崩溃复活 + restart 计数、
  stop 后不复活、健康线程不复活;常驻循环冒烟(发 job、写心跳、干净停);
- 邻接:空转心跳、estop 让路、宿主互斥钩子(skipped_busy,Q2)、在途
  守卫跳过 + 槽恢复重发恰一次(#107485)、死属主回收(300s 节流)、
  超龄 fire_claim 清扫、fire 认领心跳保活、delivery_failed 三态透传、
  A6 占位执行体契约。

上游对照:``~/.hermes/hermes-agent/cron/scheduler_tick.py``(全时序)+
``cron/scheduler.py`` 派发段(H:4100-4330、H:2706)+
``cron/scheduler_thread.py`` + ``cron/scheduler_provider.py`` 循环段。
控时纪律(ground-truth B16):无 freezegun,注入 ``now_fn`` 显式 aware
datetime;心跳节奏断言只做存在性/先后性,不做精确时距。
"""

from __future__ import annotations

import fcntl
import subprocess
import sys
import threading
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Callable, Optional
from zoneinfo import ZoneInfo

import pytest

from myssia.cron import tick as tick_module
from myssia.cron.jobs import CronJobs, release_running_job, try_register_running_job
from myssia.cron.occurrences import scheduled_instant
from myssia.cron.tick import (
    TICK_LOCK_NAME,
    _sweep_stale_fire_claims,
    tick,
)
from myssia.cron.ticker import SupervisedTickerThread, run_ticker_loop

TZ = ZoneInfo("Asia/Shanghai")
BASE = datetime(2026, 10, 4, 9, 0, tzinfo=TZ)  # 周日 09:00,固定控时基准


class Clock:
    """可拨动的注入时钟(now_fn 形态,test_cron_jobs 同款)。"""

    def __init__(self, at: datetime) -> None:
        self.now = at

    def __call__(self) -> datetime:
        return self.now

    def tick(self, **delta: float) -> None:
        self.now = self.now + timedelta(**delta)


@pytest.fixture()
def clock() -> Clock:
    return Clock(BASE)


@pytest.fixture()
def cron(tmp_path: Path, clock: Clock) -> CronJobs:
    return CronJobs(tmp_path, now_fn=clock)


@pytest.fixture(autouse=True)
def reset_reap_throttle() -> None:
    """死属主回收节流是按 cron 目录的模块态;逐例清零强制下一轮可回收
    (上游对 ``_last_dead_owner_reap_at`` 的同款测试处置)。"""
    tick_module._last_dead_owner_reap_at.clear()


@pytest.fixture()
def dead_pid() -> int:
    """确定已死且已收尸的 pid(死属主回收用,test_cron_jobs 同款)。"""
    child = subprocess.Popen([sys.executable, "-c", "import time; time.sleep(60)"])
    child.kill()
    child.wait()
    return child.pid


def make_job(
    job_id: str,
    *,
    due_minutes_ago: float = 1.0,
    interval_minutes: int = 30,
    db_path: Optional[str] = None,
    **overrides: Any,
) -> dict[str, Any]:
    """最小合法 interval job(design §2.1 字段面常用子集;直落库用)。
    ``due_minutes_ago=0` 表示 next_run_at 恰在 BASE(仍算到期)。"""
    base: dict[str, Any] = {
        "id": job_id,
        "name": f"job {job_id}",
        "category": "plugins/news.yaml",
        "db_path": db_path,
        "schedule": {
            "kind": "interval",
            "minutes": interval_minutes,
            "display": f"every {interval_minutes}m",
        },
        "schedule_display": f"every {interval_minutes}m",
        "repeat": {"times": None, "completed": 0},
        "enabled": True,
        "state": "scheduled",
        "paused_at": None,
        "paused_reason": None,
        "manual_run_at": None,
        "created_at": (BASE - timedelta(days=1)).isoformat(),
        "next_run_at": (BASE - timedelta(minutes=due_minutes_ago)).isoformat(),
        "last_run_at": None,
        "last_status": None,
        "last_error": None,
        "last_delivery_error": None,
        "failure_streak": 0,
        "deliver": "local",
        "failure_deliver": None,
        "origin": {"source": "cli"},
        "timezone": None,
    }
    base.update(overrides)
    return base


def seed(cron: CronJobs, *records: dict[str, Any]) -> None:
    """绕过生命周期 API 直落库(模拟已建好的 jobs.json)。"""
    with cron.store.jobs_lock():
        cron.store.save_jobs(list(records), replace=True)


def raw_of(cron: CronJobs, job_id: str) -> dict[str, Any]:
    return next(j for j in cron.store.load_jobs() if j.get("id") == job_id)


def ok_runner(job: dict[str, Any]) -> tuple[bool, None, None]:
    """共享的成功执行体桩。"""
    return True, None, None


def wait_until(cond: Callable[[], bool], timeout: float = 5.0) -> bool:
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        if cond():
            return True
        time.sleep(0.01)
    return cond()


# --- 文件锁单飞 ----------------------------------------------------------------


def test_tick_lock_held_by_other_returns_zero(cron: CronJobs) -> None:
    """他者持 tick.lock:静默 return 0、不派发;释放后正常派发。"""
    seed(cron, make_job("j1"))
    cron.store.ensure_dirs()
    lock_path = cron.store.cron_dir / TICK_LOCK_NAME
    calls: list[str] = []
    with open(lock_path, "w", encoding="utf-8") as held:
        fcntl.flock(held, fcntl.LOCK_EX | fcntl.LOCK_NB)
        try:
            assert (
                tick(
                    cron,
                    execute_job=lambda job: (
                        calls.append(job["id"]) or (True, None, None)
                    ),
                )
                == 0
            )
        finally:
            fcntl.flock(held, fcntl.LOCK_UN)
    assert calls == []
    assert tick(cron, execute_job=ok_runner) == 1  # 释放后正常派发


def test_tick_lock_single_flight_concurrent(cron: CronJobs) -> None:
    """并发双 tick 恰一个派发:先入场者的 runner 阻塞期间,后来者拿不到锁。"""
    seed(cron, make_job("j1"))
    entered = threading.Event()
    release_runner = threading.Event()

    def blocking_runner(job: dict[str, Any]) -> tuple[bool, None, None]:
        entered.set()
        release_runner.wait(timeout=10.0)
        return True, None, None

    result: list[int] = []
    first = threading.Thread(
        target=lambda: result.append(tick(cron, execute_job=blocking_runner))
    )
    first.start()
    try:
        assert wait_until(entered.is_set), "runner never started"
        # 先入场线程持锁派发中:本线程的 tick 必须静默让路。
        assert tick(cron, execute_job=ok_runner) == 0
    finally:
        release_runner.set()
        first.join(timeout=10.0)
    assert not first.is_alive()
    assert result == [1]


# --- 先推进后派发(at-most-once)-----------------------------------------------


def test_advance_next_runs_before_dispatch(cron: CronJobs, clock: Clock) -> None:
    """runner 运行时,存储的 next_run_at 已被推进到未来射点(at-most-once);
    派发快照的 occurrence 身份不受 advance 影响;claim 已清 pending_slot。"""
    due_iso = (BASE - timedelta(minutes=1)).isoformat()
    seed(cron, make_job("j1"))
    seen: dict[str, Any] = {}

    def inspect_runner(job: dict[str, Any]) -> tuple[bool, None, None]:
        seen["instant"] = job.get("_scheduled_instant")
        seen["stored_next"] = raw_of(cron, "j1").get("next_run_at")
        seen["pending_slot"] = raw_of(cron, "j1").get("pending_slot")
        return True, None, None

    assert tick(cron, execute_job=inspect_runner) == 1
    assert seen["instant"] == scheduled_instant(due_iso)  # 身份 = 到期射点
    stored_next = datetime.fromisoformat(str(seen["stored_next"]))
    assert stored_next > BASE  # 推进先于派发:已是未来射点
    assert seen["pending_slot"] is None  # fire claim 已清槽


def test_failed_run_still_consumes_slot(cron: CronJobs, clock: Clock) -> None:
    """处理失败的 fire 也消耗槽:同刻二次 tick 不重发(崩溃不重放)。"""
    seed(cron, make_job("j1"))
    calls: list[str] = []

    def failing_runner(job: dict[str, Any]) -> tuple[bool, None, None]:
        calls.append(job["id"])
        raise RuntimeError("boom")

    assert tick(cron, execute_job=failing_runner) == 0  # 处理了但失败 → 0
    assert tick(cron, execute_job=ok_runner) == 0  # 槽已消耗:不再 due
    assert calls == ["j1"]
    job = raw_of(cron, "j1")
    assert job["last_status"] == "failed"
    assert "RuntimeError" in str(job["last_error"])
    assert job["failure_streak"] == 1


# --- 派发主线 ------------------------------------------------------------------


def test_happy_path_bookkeeping(cron: CronJobs) -> None:
    """单 job 全链:执行体 → mark_job_run(ok + repeat 计数 + 重锚)→ 账本
    completed(到期身份 = due 射点)。"""
    due_iso = (BASE - timedelta(minutes=1)).isoformat()
    seed(cron, make_job("j1"))
    assert tick(cron, execute_job=ok_runner) == 1
    job = raw_of(cron, "j1")
    assert job["last_status"] == "ok"
    assert job["last_error"] is None
    assert job["failure_streak"] == 0
    assert job["repeat"]["completed"] == 1
    assert job["fire_claim"] is None
    assert datetime.fromisoformat(job["next_run_at"]) > BASE  # 锚完成时刻
    row = cron.ledger.latest_execution("j1")
    assert row is not None and row["status"] == "completed"
    assert row["scheduled_instant"] == scheduled_instant(due_iso)
    assert row["error"] is None


def test_delivery_failed_status_flows_through(cron: CronJobs) -> None:
    """运行成功 + 投递失败 → last_status=delivery_failed 且 streak 不动
    (F1.7 三态经执行体 seam 透传)。"""

    def deliver_fails(job: dict[str, Any]) -> tuple[bool, None, str]:
        return True, None, "feishu: channel down"

    seed(cron, make_job("j1"))
    assert tick(cron, execute_job=deliver_fails) == 1
    job = raw_of(cron, "j1")
    assert job["last_status"] == "delivery_failed"
    assert job["last_delivery_error"] == "feishu: channel down"
    assert job["failure_streak"] == 0


def test_missing_runner_raises_instead_of_fake_success(cron: CronJobs) -> None:
    """缺陷 7:缺 execute_job 的 tick() 一律 ValueError——Stage A 的 no-op 桩
    (记假成功:completed/ok + repeat 消耗)已移除;派发零副作用、账本零行。"""
    seed(cron, make_job("j1"))
    with pytest.raises(ValueError, match="execute_job"):
        tick(cron)
    job = raw_of(cron, "j1")
    assert job["last_status"] is None  # 没有假成功
    assert job["repeat"]["completed"] == 0  # 预算未消耗
    assert job["next_run_at"] == (BASE - timedelta(minutes=1)).isoformat()  # 槽未吞
    assert cron.ledger.list_executions() == []  # 账本零行


def test_run_ticker_loop_requires_runner(cron: CronJobs) -> None:
    """常驻循环同款 fail fast(缺陷 7):缺 runner 的宿主装配错误当场暴露,
    不是每轮吞错写假成功。"""
    with pytest.raises(ValueError, match="execute_job"):
        run_ticker_loop(cron, threading.Event())


def test_idle_tick_records_heartbeat(cron: CronJobs) -> None:
    """空转 tick:更新心跳标记(design §3.1 步骤 6),return 0。"""
    seed(cron, make_job("j1", due_minutes_ago=-30))  # next_run_at 在未来
    assert tick(cron, execute_job=ok_runner) == 0
    assert (cron.store.cron_dir / "ticker_heartbeat").exists()
    assert cron.get_ticker_heartbeat_age() is not None
    assert cron.get_ticker_success_age() is not None


def test_estop_skips_dispatch(cron: CronJobs) -> None:
    """全局急停(marker):跳过派发、绝不动 job;解除后恢复。"""
    seed(cron, make_job("j1"))
    cron.engage_estop(reason="test")
    calls: list[str] = []
    try:
        assert (
            tick(
                cron,
                execute_job=lambda job: calls.append(job["id"]) or (True, None, None),
            )
            == 0
        )
        assert calls == []
        assert (
            raw_of(cron, "j1")["next_run_at"]
            == (BASE - timedelta(minutes=1)).isoformat()
        )
    finally:
        assert cron.disengage_estop()
    assert tick(cron, execute_job=ok_runner) == 1


def test_dispatch_gate_skips_busy(cron: CronJobs) -> None:
    """宿主互斥钩子(Q2):gate=False → 不跑执行体,last_status=skipped_busy
    (streak 不动)、槽消耗、账本行按未启动记失败。"""
    seed(cron, make_job("j1"))
    calls: list[str] = []

    def gate(job: dict[str, Any]) -> bool:
        return False

    assert (
        tick(
            cron,
            execute_job=lambda job: calls.append(job["id"]) or (True, None, None),
            dispatch_gate=gate,
        )
        == 1
    )
    assert calls == []
    job = raw_of(cron, "j1")
    assert job["last_status"] == "skipped_busy"
    assert job["last_error"] is None
    assert job["failure_streak"] == 0
    assert datetime.fromisoformat(job["next_run_at"]) > BASE  # 槽已消耗
    row = cron.ledger.latest_execution("j1")
    assert row is not None and row["status"] == "failed"
    assert "skipped_busy" in str(row["error"])
    # gate 放行时正常派发(trigger 重建 due 槽:下次 tick 立即跑)
    cron.trigger_job("j1")
    assert (
        tick(
            cron,
            execute_job=lambda job: calls.append(job["id"]) or (True, None, None),
            dispatch_gate=lambda job: True,
        )
        == 1
    )
    assert calls == ["j1"]
    assert raw_of(cron, "j1")["last_status"] == "ok"


def test_inflight_guard_skips_and_slot_recovers_once(cron: CronJobs) -> None:
    """在途守卫:本进程已在跑的 job 派发跳过;守卫释放后 pending_slot 恢复
    恰一次重发(#107485)。"""
    seed(cron, make_job("j1"))
    calls: list[str] = []
    assert try_register_running_job("j1")
    try:
        assert (
            tick(
                cron,
                execute_job=lambda job: calls.append(job["id"]) or (True, None, None),
            )
            == 0
        )
        assert calls == []
    finally:
        release_running_job("j1")
    assert (
        tick(
            cron, execute_job=lambda job: calls.append(job["id"]) or (True, None, None)
        )
        == 1
    )
    assert calls == ["j1"]  # 恢复恰一次,不是跳过


# --- D13:同 db 串行 / 不同 db 并行 ---------------------------------------------


def test_different_db_groups_run_in_parallel(cron: CronJobs, tmp_path: Path) -> None:
    """不同 db 的 job 并行派发:两组首 job 用 Barrier 会合(串行则超时破裂)。"""
    seed(
        cron,
        make_job("ja", db_path=str(tmp_path / "a" / "myssia.db")),
        make_job("jb", db_path=str(tmp_path / "b" / "myssia.db")),
    )
    barrier = threading.Barrier(2, timeout=10.0)
    passed: set[str] = set()
    lock = threading.Lock()

    def barrier_runner(job: dict[str, Any]) -> tuple[bool, None, None]:
        try:
            barrier.wait()
        except threading.BrokenBarrierError:
            return False, "serialized: barrier timed out", None
        with lock:
            passed.add(job["id"])
        return True, None, None

    assert tick(cron, execute_job=barrier_runner) == 2
    assert passed == {"ja", "jb"}  # 两组确曾同时在跑


def test_same_db_jobs_run_serially(cron: CronJobs, tmp_path: Path) -> None:
    """同 db 的 job 组内串行:全程组内活跃数恒 1(若并行则重叠 ≥ 2)。"""
    db = str(tmp_path / "one" / "myssia.db")
    seed(cron, make_job("j1", db_path=db), make_job("j2", db_path=db))
    lock = threading.Lock()
    state = {"active": 0, "max_active": 0, "order": []}

    def serial_runner(job: dict[str, Any]) -> tuple[bool, None, None]:
        with lock:
            state["order"].append(job["id"])
            state["active"] += 1
            state["max_active"] = max(state["max_active"], state["active"])
        time.sleep(0.06)  # 留出可观测的重叠窗口
        with lock:
            state["active"] -= 1
        return True, None, None

    assert tick(cron, execute_job=serial_runner) == 2
    assert state["order"] == ["j1", "j2"]  # due 顺序保序
    assert state["max_active"] == 1  # 从未重叠


def test_same_db_serial_and_cross_db_parallel_combined(
    cron: CronJobs, tmp_path: Path
) -> None:
    """D13 组合场景:两组各两 job——组间并行(Barrier 会合),组内串行
    (第二 job 必等第一 job 让位)。"""
    db_a = str(tmp_path / "a" / "myssia.db")
    db_b = str(tmp_path / "b" / "myssia.db")
    seed(
        cron,
        make_job("a1", db_path=db_a),
        make_job("a2", db_path=db_a),
        make_job("b1", db_path=db_b),
        make_job("b2", db_path=db_b),
    )
    barrier = threading.Barrier(2, timeout=10.0)
    lock = threading.Lock()
    events: dict[str, dict[str, float]] = {}
    barrier_passed: list[str] = []

    def recording_runner(job: dict[str, Any]) -> tuple[bool, None, None]:
        jid = job["id"]
        if jid in {"a1", "b1"}:  # 各组首 job:组间会合点
            try:
                barrier.wait()
            except threading.BrokenBarrierError:
                return False, "serialized across db groups: barrier timed out", None
            with lock:
                barrier_passed.append(jid)
        with lock:
            events[jid] = {"start": time.monotonic(), "end": 0.0}
        time.sleep(0.03)
        with lock:
            events[jid]["end"] = time.monotonic()
        return True, None, None

    assert tick(cron, execute_job=recording_runner) == 4
    assert sorted(barrier_passed) == ["a1", "b1"]  # 组间并行实证
    # 组内串行:第二 job 的开始不早于同组第一 job 的结束。
    assert events["a2"]["start"] >= events["a1"]["end"]
    assert events["b2"]["start"] >= events["b1"]["end"]


def test_single_job_failure_does_not_kill_tick(cron: CronJobs) -> None:
    """单 job 失败不拖垮:同组兄弟照跑照记 ok,失败侧记账落全。"""
    seed(cron, make_job("j1"), make_job("j2"), make_job("j3"))
    ran: list[str] = []

    def flaky_runner(job: dict[str, Any]) -> tuple[bool, None, None]:
        ran.append(job["id"])
        if job["id"] == "j2":
            raise RuntimeError("kaboom")
        return True, None, None

    assert tick(cron, execute_job=flaky_runner) == 2  # ok + failed + ok
    assert ran == ["j1", "j2", "j3"]
    assert raw_of(cron, "j1")["last_status"] == "ok"
    bad = raw_of(cron, "j2")
    assert bad["last_status"] == "failed"
    assert "kaboom" in str(bad["last_error"])
    assert bad["failure_streak"] == 1
    assert datetime.fromisoformat(bad["next_run_at"]) > BASE  # 失败也重锚
    row = cron.ledger.latest_execution("j2")
    assert row is not None and row["status"] == "failed"
    assert raw_of(cron, "j3")["last_status"] == "ok"


# --- reap 与超龄 fire_claim 清扫 ----------------------------------------------


def test_reap_dead_owner_rows(cron: CronJobs, dead_pid: int) -> None:
    """属主已死的 claimed 行在 tick 内被终态化 unknown(#86721)。"""
    seed(cron, make_job("j1"))
    with cron.ledger.transaction() as conn:
        conn.execute(
            """INSERT INTO executions
                 (id, job_id, source, status, pid, process_start_time, claimed_at)
               VALUES ('deadrow', 'gone', 'tick', 'claimed', ?, 12345.0, ?)""",
            (dead_pid, datetime.now(timezone.utc).isoformat()),
        )
    assert tick(cron, execute_job=ok_runner) == 1
    row = cron.ledger.get_execution("deadrow")
    assert row is not None and row["status"] == "unknown"


def test_sweep_stale_fire_claims(cron: CronJobs) -> None:
    """超龄 fire_claim 清扫:due job 名下不活的清掉;活的与本进程在途的不动。"""
    stale = {"at": (BASE - timedelta(seconds=400)).isoformat(), "by": "otherhost:1:tok"}
    live = {"at": BASE.isoformat(), "by": "otherhost:2:tok"}
    seed(cron, make_job("j1", fire_claim=stale), make_job("j2", fire_claim=live))
    assert try_register_running_job("j2")
    try:
        cleared = _sweep_stale_fire_claims(
            cron, [raw_of(cron, "j1"), raw_of(cron, "j2")]
        )
    finally:
        release_running_job("j2")
    assert cleared == 1
    assert raw_of(cron, "j1")["fire_claim"] is None
    j2_claim = raw_of(cron, "j2")["fire_claim"]
    assert isinstance(j2_claim, dict) and j2_claim["by"] == "otherhost:2:tok"


# --- fire 认领心跳保活 ---------------------------------------------------------


def test_fire_claim_heartbeat_refreshes_during_run(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """执行体运行期间 fire 认领被周期刷新(长执行活过 TTL 不被他宿主回收);
    真实时钟 + 缩短心跳节奏(monkeypatch 模块常量)。写节流阈值
    (CLAIM_REFRESH_MIN_AGE_SECONDS,缺陷 3)同步压到 0:本用例验的是
    「每跳可刷新」的机制面,节流行为另见 test_heartbeat_fire_claim_write_throttled。"""
    monkeypatch.setattr(tick_module, "FIRE_CLAIM_HEARTBEAT_SECONDS", 0.05)
    monkeypatch.setattr(tick_module, "FIRE_CLAIM_MISS_CONFIRM_SECONDS", 0.01)
    from myssia.cron import jobs as jobs_module

    monkeypatch.setattr(jobs_module, "CLAIM_REFRESH_MIN_AGE_SECONDS", 0.0)
    cron = CronJobs(tmp_path)  # 无注入时钟:真实 now,at 戳可分辨先后
    seed(
        cron,
        make_job(
            "j1",
            next_run_at=(
                datetime.now().astimezone() - timedelta(minutes=1)
            ).isoformat(),
        ),
    )
    samples: list[str] = []

    def slow_runner(job: dict[str, Any]) -> tuple[bool, None, None]:
        samples.append(str(raw_of(cron, "j1").get("fire_claim", {}).get("at")))
        time.sleep(0.2)  # ≥ 3 个心跳周期
        samples.append(str(raw_of(cron, "j1").get("fire_claim", {}).get("at")))
        return True, None, None

    assert tick(cron, execute_job=slow_runner) == 1
    first, last = samples
    assert first and last and first != last
    assert datetime.fromisoformat(last) > datetime.fromisoformat(first)
    assert raw_of(cron, "j1")["last_status"] == "ok"  # owner fence 未拒收


# --- SupervisedTickerThread 与常驻循环 -----------------------------------------


@pytest.mark.filterwarnings("ignore::pytest.PytestUnhandledThreadExceptionWarning")
def test_supervised_ticker_respawns_after_crash() -> None:
    """崩了 respawn + restart 计数;复活后的目标真被再执行,且可反复复活。"""
    starts: list[int] = []
    stop = threading.Event()

    def dying_ticker() -> None:
        starts.append(1)
        raise RuntimeError("ticker died")

    ticker = SupervisedTickerThread(dying_ticker, stop_event=stop, name="cron-test")
    ticker.start()
    ticker.join(timeout=5.0)
    assert not ticker.is_alive()
    assert starts == [1]
    assert ticker.restart_if_dead() is True
    assert ticker.restarts == 1
    ticker.join(timeout=5.0)
    assert starts == [1, 1]  # 复活后真跑了一遍(又崩,常态)
    assert ticker.restart_if_dead() is True  # 可反复复活
    assert ticker.restarts == 2
    ticker.join(timeout=5.0)
    assert starts == [1, 1, 1]


@pytest.mark.filterwarnings("ignore::pytest.PytestUnhandledThreadExceptionWarning")
def test_supervised_ticker_no_respawn_when_stopped_or_healthy() -> None:
    """stop 已请求或线程健在 → 不复活;正常返回的目标不是死 ticker。"""

    def die() -> None:
        raise RuntimeError("die")

    # stop 已请求:即便崩过也不复活。
    stop = threading.Event()
    stop.set()
    ticker = SupervisedTickerThread(die, stop_event=stop)
    ticker.start()
    ticker.join(timeout=5.0)
    assert ticker.restart_if_dead() is False
    assert ticker.restarts == 0
    # 健康线程:活着,不复活。
    healthy_stop = threading.Event()
    ran = threading.Event()

    def healthy_ticker() -> None:
        ran.set()
        healthy_stop.wait(timeout=10.0)

    healthy = SupervisedTickerThread(
        healthy_ticker, stop_event=healthy_stop, name="cron-healthy"
    )
    healthy.start()
    try:
        assert wait_until(ran.is_set)
        assert healthy.is_alive()
        assert healthy.restart_if_dead() is False
    finally:
        healthy_stop.set()
        healthy.join(timeout=5.0)
    # 有意返回的目标(无异常逃逸)不是死 ticker。
    returned = SupervisedTickerThread(lambda: None, stop_event=threading.Event())
    returned.start()
    returned.join(timeout=5.0)
    assert returned.restart_if_dead() is False


def test_run_ticker_loop_fires_and_stops_cleanly(cron: CronJobs, clock: Clock) -> None:
    """常驻循环冒烟:发 job → 心跳在册 → stop_event 干净退出、无错误标记。"""
    seed(cron, make_job("j1"))
    calls: list[str] = []

    def counting_runner(job: dict[str, Any]) -> tuple[bool, None, None]:
        calls.append(job["id"])
        return True, None, None

    stop = threading.Event()
    loop = threading.Thread(
        target=run_ticker_loop,
        args=(cron, stop),
        kwargs={"interval": 0.05, "execute_job": counting_runner},
        daemon=True,
    )
    loop.start()
    try:
        assert wait_until(lambda: len(calls) >= 1, timeout=5.0), "job never fired"
        assert wait_until(
            lambda: (cron.store.cron_dir / "ticker_heartbeat").exists(), timeout=5.0
        )
    finally:
        stop.set()
        loop.join(timeout=5.0)
    assert not loop.is_alive()
    assert calls == ["j1"]  # 发过恰一次(后续循环空转)
    assert cron.get_ticker_heartbeat_age() is not None
    assert cron.get_ticker_last_error() is None
    assert raw_of(cron, "j1")["last_status"] == "ok"


def test_run_ticker_loop_heartbeat_scan_fires_and_gates(cron: CronJobs) -> None:
    """低频扫描钩子(10-05-cron-heartbeat 收尾件):注入即被调——首轮即扫
    (停摆检测宁早勿晚),且间隔门独立于 tick 密集度(tick 远快于扫描间隔的
    观察窗内,恰只扫一次;节奏断言沿控时纪律:存在性+计数,不做精确时距)。
    成功一扫不留扫描错误 marker(缺陷 9 的清面)。"""
    seed(cron, make_job("j1"))
    scans: list[float] = []

    def counting_scan() -> None:
        scans.append(time.monotonic())

    stop = threading.Event()
    loop = threading.Thread(
        target=run_ticker_loop,
        args=(cron, stop),
        kwargs={
            "interval": 0.05,
            "execute_job": lambda job: (True, None, None),  # 缺 runner 即 raise(缺陷 7)
            "heartbeat_scan": counting_scan,
            "heartbeat_scan_interval": 10.0,  # 观察窗(亚秒)<< 间隔:只该有首轮一扫
        },
        daemon=True,
    )
    loop.start()
    try:
        assert wait_until(lambda: len(scans) >= 1, timeout=5.0), "scan never fired"
        time.sleep(0.4)  # ≥ 8 个 tick 空转:证间隔门不随 tick 连扫
        assert len(scans) == 1
    finally:
        stop.set()
        loop.join(timeout=5.0)
    assert not loop.is_alive()
    assert cron.get_heartbeat_scan_last_error() is None  # 成功扫描:marker 不在场


def test_run_ticker_loop_heartbeat_scan_error_isolated(cron: CronJobs) -> None:
    """扫描钩子自身异常绝不带走 ticker 线程(_guarded 惯例):反复炸的扫描
    后循环照常 tick/发 job/写心跳;ERROR 留痕 + **专用** heartbeat_scan
    错误 marker(缺陷 9:操作者可见,此前只留日志);不写 ticker 错误 marker
    (marker 面 = ticker 自身死活,不被评估侧失败污染);stop 干净退出。"""
    seed(cron, make_job("j1"))
    calls: list[str] = []
    attempts: list[int] = []

    def counting_runner(job: dict[str, Any]) -> tuple[bool, None, None]:
        calls.append(job["id"])
        return True, None, None

    def exploding_scan() -> None:
        attempts.append(1)
        raise RuntimeError("scan blew up")

    stop = threading.Event()
    loop = threading.Thread(
        target=run_ticker_loop,
        args=(cron, stop),
        kwargs={
            "interval": 0.05,
            "execute_job": counting_runner,
            "heartbeat_scan": exploding_scan,
            "heartbeat_scan_interval": 0.05,
        },
        daemon=True,
    )
    loop.start()
    try:
        # 第 3 次扫描尝试 = 线程已扛过前两次异常仍在循环。
        assert wait_until(lambda: len(attempts) >= 3, timeout=5.0), "loop died with the scan"
        assert wait_until(
            lambda: (cron.store.cron_dir / "ticker_heartbeat").exists(), timeout=5.0
        )
    finally:
        stop.set()
        loop.join(timeout=5.0)
    assert not loop.is_alive()
    assert calls == ["j1"]  # job 照发恰一次(扫描异常不拖累派发)
    assert cron.get_ticker_last_error() is None  # 扫描失败不染指 ticker 错误面
    assert "scan blew up" in (cron.get_heartbeat_scan_last_error() or "")  # 缺陷 9
