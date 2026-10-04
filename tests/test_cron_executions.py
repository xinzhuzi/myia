"""Cron 执行账本(tests 冻结命名,10-04-hermes-cron implement A3)。

一个文件收拢 executions.db 账本的测试面:

- 全状态转移:claimed→running→completed/failed 恰一次;claimed 直达终态;
  run_summary_json 落列(D10);
- 死属主判定:PID 消失 → 死;同号进程换化身(指纹远漂)→ 死;指纹容差内
  漂移 ≠ 死(上游 #117505);指纹读不出 → 证不了死 → 不重写(fail-safe);
  NULL 指纹行只有本进程 pid 算活(上游照抄);
- 恢复:recover_interrupted_executions 只动可证死行、终态幂等;
  terminalize_dead_owner 带观察死因、活属主/本人行/已终态/缺失一律 False;
- 终态不可变:再 finish 返回 None、行原样;异属主行拒改;
- 裁剪:MAX_TERMINAL_EXECUTIONS=1000,finish 触发 newest-first 裁剪;
- 查询:list 游标分页(julianday 序)不跳行不重行、latest_executions 窗口化、
  live_inflight_execution 活属主判定;
- 契约面:DDL 列集 = design §2.3、三索引、status CHECK、事务回滚必放。

上游对照:`~/.hermes/hermes-agent/cron/executions.py`(模块 docstring 标注
裁/增偏离)。
"""

from __future__ import annotations

import json
import os
import sqlite3
import subprocess
import sys
from datetime import datetime, timedelta, timezone
from typing import Any, Optional

import pytest

from myia.cron import executions as cron_exec
from myia.cron.executions import ExecutionLedger

UTC = timezone.utc


@pytest.fixture()
def ledger(tmp_path: Any) -> ExecutionLedger:
    return ExecutionLedger.for_db(tmp_path / "myia.db")


def seed_row(
    ledger: ExecutionLedger, execution_id: str, *,
    job_id: str = "job-1", source: str = "tick", status: str = "claimed",
    pid: Optional[int] = None, start: Optional[float] = None,
    claimed_at: Optional[str] = None,
) -> None:
    """绕过状态机直插一行(模拟他进程/前任宿主留下的账本行)。"""
    with ledger.transaction() as conn:
        conn.execute(
            """INSERT INTO executions
               (id, job_id, source, status, pid, process_start_time, claimed_at)
               VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (execution_id, job_id, source, status,
             os.getpid() if pid is None else pid, start,
             claimed_at or datetime.now(UTC).isoformat()),
        )


@pytest.fixture()
def dead_pid() -> int:
    """一个确定已死且已被回收的 pid(杀掉并 wait 收尸,防僵尸误判存活)。"""
    child = subprocess.Popen([sys.executable, "-c", "import time; time.sleep(60)"])
    child.kill()
    child.wait()
    return child.pid


@pytest.fixture()
def live_child() -> Any:
    """一个确定存活的子进程(异地属主替身)。"""
    child = subprocess.Popen([sys.executable, "-c", "import time; time.sleep(60)"])
    try:
        yield child
    finally:
        child.kill()
        child.wait()


# --- 定位与 schema ------------------------------------------------------------


def test_for_db_derives_db_path_and_bootstraps(tmp_path: Any) -> None:
    ledger = ExecutionLedger.for_db(tmp_path / "myia.db")
    assert ledger.data_root == tmp_path
    assert ledger.db_path == tmp_path / "cron" / "executions.db"
    assert not ledger.db_path.exists()
    ledger.create_execution("job-1", source="tick")  # 首事务自建目录与库
    assert ledger.db_path.is_file()
    # 账本与 job 注册表同一数据根(A6)。
    assert ledger.db_path.parent == tmp_path / "cron"


def test_schema_columns_indexes_and_status_check(ledger: ExecutionLedger) -> None:
    ledger.create_execution("job-s", source="tick")
    with ledger.transaction() as conn:
        columns = {row["name"] for row in conn.execute("PRAGMA table_info(executions)")}
        indexes = {row["name"] for row in conn.execute("PRAGMA index_list(executions)")}
    assert columns == {
        "id", "job_id", "source", "status", "scheduled_instant",
        "pid", "process_start_time", "claimed_at", "started_at",
        "finished_at", "error", "run_summary_json",
    }
    assert indexes >= {
        "idx_executions_job_claimed",
        "idx_executions_status_claimed",
        "idx_executions_occurrence",
    }
    with pytest.raises(sqlite3.IntegrityError):
        with ledger.transaction() as conn:
            conn.execute(
                "INSERT INTO executions (id, job_id, source, status, pid, claimed_at) "
                "VALUES ('bad', 'j', 'tick', 'bogus', 1, 'x')")


def test_transaction_rolls_back_and_releases(ledger: ExecutionLedger) -> None:
    with pytest.raises(RuntimeError):
        with ledger.transaction() as conn:
            conn.execute(
                "INSERT INTO executions (id, job_id, source, status, pid, claimed_at) "
                "VALUES ('rb', 'j', 'tick', 'claimed', 1, 'x')")
            raise RuntimeError("boom")
    assert ledger.get_execution("rb") is None
    ledger.create_execution("after", source="tick")  # 连接已关、库未锁


# --- 全状态转移 ---------------------------------------------------------------


def test_full_transition_success_with_summary(ledger: ExecutionLedger) -> None:
    record = ledger.create_execution(
        "job-1", source="tick", scheduled_instant="2026-10-04T09:00:00+08:00")
    assert record["status"] == "claimed"
    assert record["pid"] == os.getpid()
    assert record["claimed_at"]
    if os.name == "posix":
        assert record["process_start_time"] is not None
    # 到期身份规范化为 UTC(occurrence 去重键)。
    assert record["scheduled_instant"] == "2026-10-04T01:00:00+00:00"

    running = ledger.mark_execution_running(record["id"])
    assert running is not None
    assert running["status"] == "running"
    assert running["started_at"]

    finished = ledger.finish_execution(
        record["id"], success=True,
        run_summary={"status": "success", "items_retained": 3})
    assert finished is not None
    assert finished["status"] == "completed"
    assert finished["error"] is None
    assert finished["finished_at"]
    assert json.loads(finished["run_summary_json"]) == {
        "status": "success", "items_retained": 3}


def test_failure_paths_record_error(ledger: ExecutionLedger) -> None:
    rec_a = ledger.create_execution("job-a", source="manual")
    finished = ledger.finish_execution(rec_a["id"], success=False, error="boom")
    assert finished is not None
    assert finished["status"] == "failed"
    assert finished["error"] == "boom"
    # claimed 不经 running 直达终态同样合法(快失败路径)。
    rec_b = ledger.create_execution("job-b", source="tick")
    no_detail = ledger.finish_execution(rec_b["id"], success=False)
    assert no_detail is not None
    assert no_detail["error"] == "unknown failure"


def test_mark_running_exactly_once(ledger: ExecutionLedger) -> None:
    record = ledger.create_execution("job-1", source="tick")
    assert ledger.mark_execution_running(record["id"]) is not None
    assert ledger.mark_execution_running(record["id"]) is None  # running ≠ claimed


# --- 终态不可变 + 属主护栏 -----------------------------------------------------


def test_terminal_state_immutable(ledger: ExecutionLedger) -> None:
    record = ledger.create_execution("job-1", source="tick")
    ledger.mark_execution_running(record["id"])
    finished = ledger.finish_execution(record["id"], success=True)
    assert finished is not None
    # 终态后再写:一律 None,行原样。
    assert ledger.finish_execution(record["id"], success=False, error="late") is None
    assert ledger.mark_execution_running(record["id"]) is None
    row = ledger.get_execution(record["id"])
    assert row is not None
    assert row["status"] == "completed"
    assert row["error"] is None
    assert row["run_summary_json"] is None


def test_foreign_rows_rejected(ledger: ExecutionLedger) -> None:
    seed_row(ledger, "foreign", pid=os.getpid() + 10000, start=12345.0)
    assert ledger.mark_execution_running("foreign") is None
    assert ledger.finish_execution("foreign", success=True) is None
    row = ledger.get_execution("foreign")
    assert row is not None and row["status"] == "claimed"


def test_own_null_fingerprint_row_is_self(ledger: ExecutionLedger) -> None:
    # 本人 pid + NULL 指纹(指纹源读不出的平台上 create 的产物)按己方行,
    # 恢复绝不碰自己。
    seed_row(ledger, "own-null", pid=os.getpid(), start=None)
    assert ledger.recover_interrupted_executions() == 0
    assert ledger.get_execution("own-null") is not None
    assert ledger.get_execution("own-null")["status"] == "claimed"


# --- 死属主判定与恢复 ---------------------------------------------------------


def test_recover_dead_owner_rows(ledger: ExecutionLedger, dead_pid: int) -> None:
    seed_row(ledger, "dead-claimed", pid=dead_pid, start=12345.0, status="claimed")
    seed_row(ledger, "dead-running", pid=dead_pid, start=12345.0, status="running")
    assert ledger.recover_interrupted_executions() == 2
    for row_id in ("dead-claimed", "dead-running"):
        row = ledger.get_execution(row_id)
        assert row is not None
        assert row["status"] == "unknown"
        assert "owner exited" in row["error"]
        assert row["finished_at"]
    # 终态行幂等:再扫零改动。
    assert ledger.recover_interrupted_executions() == 0


def test_recover_skips_live_foreign_owner(ledger: ExecutionLedger, live_child: Any) -> None:
    started = cron_exec.process_start_time(live_child.pid)
    assert started is not None  # POSIX 上指纹可读
    seed_row(ledger, "live-row", job_id="job-live", pid=live_child.pid,
             start=started, status="running")
    assert ledger.recover_interrupted_executions() == 0
    row = ledger.get_execution("live-row")
    assert row is not None and row["status"] == "running"
    # 所有权判定(只读):活属主的 in-flight 行可见。
    inflight = ledger.live_inflight_execution("job-live")
    assert inflight is not None and inflight["id"] == "live-row"


def test_recycled_pid_fingerprint_mismatch_is_dead(ledger: ExecutionLedger) -> None:
    own = cron_exec.process_start_time(os.getpid())
    assert own is not None  # POSIX
    # 行 pid=本进程号,但指纹远离 → 同号前任宿主 → 可证死 → 恢复。
    seed_row(ledger, "recycled", pid=os.getpid(),
             start=own + 10 * cron_exec.START_TIME_DRIFT_TOLERANCE + 100.0)
    assert ledger.recover_interrupted_executions() == 1
    row = ledger.get_execution("recycled")
    assert row is not None and row["status"] == "unknown"


def test_fingerprint_drift_within_tolerance_is_not_death(ledger: ExecutionLedger) -> None:
    own = cron_exec.process_start_time(os.getpid())
    assert own is not None
    # 同机两次读数漂移(上游 #117505 ±2s 论证)不是死亡证明:不恢复。
    seed_row(ledger, "drift", pid=os.getpid(),
             start=own + cron_exec.START_TIME_DRIFT_TOLERANCE / 2)
    assert ledger.recover_interrupted_executions() == 0
    row = ledger.get_execution("drift")
    assert row is not None and row["status"] == "claimed"


def test_unreadable_fingerprint_cannot_prove_death(
    ledger: ExecutionLedger, live_child: Any, monkeypatch: pytest.MonkeyPatch,
) -> None:
    seed_row(ledger, "opaque", pid=live_child.pid, start=999.0, status="running")
    monkeypatch.setattr(cron_exec, "process_start_time", lambda pid: None)
    # 读不出 → 证不了死 → 行不动(fail-safe);所有权判定同样按活处理。
    assert ledger.recover_interrupted_executions() == 0
    assert ledger.live_inflight_execution("job-1") is not None


def test_null_start_foreign_pid_treated_dead(
    ledger: ExecutionLedger, dead_pid: int,
) -> None:
    # 照抄上游:started_at 为 None 时只有本进程 pid 算活。
    seed_row(ledger, "null-foreign", pid=dead_pid, start=None)
    assert ledger.recover_interrupted_executions() == 1
    assert ledger.get_execution("null-foreign") is not None
    assert ledger.get_execution("null-foreign")["status"] == "unknown"


def test_terminalize_dead_owner_with_reason(
    ledger: ExecutionLedger, dead_pid: int, live_child: Any,
) -> None:
    seed_row(ledger, "term-dead", pid=dead_pid, start=12345.0, status="running")
    assert ledger.terminalize_dead_owner(
        "term-dead", reason="runner killed orphan process group (D14)") is True
    row = ledger.get_execution("term-dead")
    assert row is not None
    assert row["status"] == "unknown"
    assert row["error"] == "runner killed orphan process group (D14)"
    # 已终态 → False(回落给调用方)。
    assert ledger.terminalize_dead_owner("term-dead", reason="again") is False
    # 活属主绝不许从脚下被终态化。
    started = cron_exec.process_start_time(live_child.pid)
    assert started is not None
    seed_row(ledger, "term-live", pid=live_child.pid, start=started)
    assert ledger.terminalize_dead_owner("term-live", reason="x") is False
    # 缺失行 → False。
    assert ledger.terminalize_dead_owner("missing", reason="x") is False
    # 本人行 → False。
    seed_row(ledger, "term-own", pid=os.getpid(),
             start=cron_exec.process_start_time(os.getpid()))
    assert ledger.terminalize_dead_owner("term-own", reason="x") is False


# --- 裁剪 ---------------------------------------------------------------------


def test_prune_terminal_rows_at_threshold(ledger: ExecutionLedger) -> None:
    assert cron_exec.MAX_TERMINAL_EXECUTIONS == 1000
    base = datetime(2026, 1, 1, tzinfo=UTC)
    rows = []
    for i in range(1005):
        stamp = (base + timedelta(seconds=i)).isoformat()
        rows.append((f"old-{i}", "job-p", "tick", "completed", 1, 1.0, stamp, stamp))
    with ledger.transaction() as conn:
        conn.executemany(
            """INSERT INTO executions
               (id, job_id, source, status, pid, process_start_time,
                claimed_at, finished_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
            rows,
        )
    # 一次终态写入触发裁剪:1005 旧 + 1 新 = 1006 → 留最新 1000。
    record = ledger.create_execution("job-p", source="tick")
    finished = ledger.finish_execution(record["id"], success=True)
    assert finished is not None
    with ledger.transaction() as conn:
        terminal = conn.execute(
            "SELECT COUNT(*) FROM executions WHERE status IN ('completed','failed','unknown')"
        ).fetchone()[0]
        inflight = conn.execute(
            "SELECT COUNT(*) FROM executions WHERE status IN ('claimed','running')"
        ).fetchone()[0]
    assert terminal == 1000
    assert inflight == 0
    # newest-first:最旧的 6 条被裁,新写入与尾部旧行都在。
    assert ledger.get_execution("old-5") is None
    assert ledger.get_execution("old-6") is not None
    assert ledger.get_execution(record["id"]) is not None


# --- 查询 ---------------------------------------------------------------------


def test_list_executions_order_filter_and_cursor(ledger: ExecutionLedger) -> None:
    base = datetime(2026, 1, 1, tzinfo=UTC)
    for i in range(5):
        stamp = (base + timedelta(minutes=i)).isoformat()
        seed_row(ledger, f"a-{i}", job_id="job-a", claimed_at=stamp)
    for i in range(2):
        seed_row(ledger, f"b-{i}", job_id="job-b",
                 claimed_at=(base + timedelta(hours=10 + i)).isoformat())

    page1 = ledger.list_executions(job_id="job-a", limit=3)
    assert [r["id"] for r in page1] == ["a-4", "a-3", "a-2"]  # 最新优先
    page2 = ledger.list_executions(
        job_id="job-a", limit=3, before_claimed_at=page1[-1]["claimed_at"])
    assert [r["id"] for r in page2] == ["a-1", "a-0"]  # 游标不跳行不重行
    # 无过滤全量最新优先;limit 下限钳到 1。
    everything = ledger.list_executions(limit=500)
    assert [r["id"] for r in everything][:2] == ["b-1", "b-0"]
    assert len(ledger.list_executions(limit=0)) == 1


def test_latest_execution_and_windowed_latest(ledger: ExecutionLedger) -> None:
    base = datetime(2026, 1, 1, tzinfo=UTC)
    for i in range(3):
        seed_row(ledger, f"a-{i}", job_id="job-a",
                 claimed_at=(base + timedelta(minutes=i)).isoformat())
    seed_row(ledger, "b-0", job_id="job-b", claimed_at=base.isoformat())

    latest_a = ledger.latest_execution("job-a")
    assert latest_a is not None and latest_a["id"] == "a-2"
    assert ledger.latest_execution("job-none") is None

    windowed = ledger.latest_executions(["job-a", "job-b", "", "job-a"])
    assert set(windowed) == {"job-a", "job-b"}
    assert windowed["job-a"]["id"] == "a-2"
    assert ledger.latest_executions([]) == {}


def test_live_inflight_requires_live_owner(
    ledger: ExecutionLedger, dead_pid: int,
) -> None:
    seed_row(ledger, "dead-row", job_id="job-d", pid=dead_pid, start=12345.0,
             status="running")
    assert ledger.live_inflight_execution("job-d") is None  # 属主已死
    seed_row(ledger, "done-row", job_id="job-e", pid=os.getpid(),
             start=cron_exec.process_start_time(os.getpid()), status="completed")
    assert ledger.live_inflight_execution("job-e") is None  # 已终态


def test_canonical_scheduled_instant_shapes() -> None:
    canonical = cron_exec.canonical_scheduled_instant
    assert canonical("2026-10-04T09:00:00+08:00") == "2026-10-04T01:00:00+00:00"
    assert canonical("2026-10-04T01:00:00+00:00") == "2026-10-04T01:00:00+00:00"
    assert canonical("2026-10-04T09:00:00") is None   # naive:无精确身份
    assert canonical(12345) is None                    # 非字符串
    assert canonical("not-a-time") is None             # 解析失败
