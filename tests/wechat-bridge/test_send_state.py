"""G6 频控落盘单测(design §8:直接测状态文件读写与 flock,不真等 10 秒
——时间注入)。"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from wechat_bridge.codes import SEND_RATE_LIMITED, BridgeError
from wechat_bridge.send_state import (
    SEND_MIN_INTERVAL_SECONDS,
    SendRateState,
    load_last_send_epoch,
)

assert SEND_MIN_INTERVAL_SECONDS == 10.0  # G6 红线值钉死;改动=改 design+prd


def test_no_state_file_allows_first_send(tmp_path: Path) -> None:
    """从未发过(缺文件)→ 放行首发。"""
    state = SendRateState(tmp_path / "wechat-localdb" / "send_state.json")
    state.check_send_allowed(now=1000.0)  # 不抛即放行
    assert load_last_send_epoch(state.state_path()) is None


def test_interval_shorter_than_10s_rejected_with_retry_after(tmp_path: Path) -> None:
    """间隔不足 10s → exit 14 + retry_after_seconds(§6 表)。"""
    state = SendRateState(tmp_path / "wechat-localdb" / "send_state.json")
    state.record_send(now=1000.0)
    with pytest.raises(BridgeError) as excinfo:
        state.check_send_allowed(now=1003.5)
    err = excinfo.value
    assert err.exit_code == SEND_RATE_LIMITED == 14
    assert err.retry_after_seconds == pytest.approx(6.5)
    assert err.name == "send_rate_limited"


def test_interval_at_and_beyond_10s_allowed(tmp_path: Path) -> None:
    state = SendRateState(tmp_path / "send_state.json")
    state.record_send(now=1000.0)
    state.check_send_allowed(now=1010.0)  # 恰好 10s:放行(≥10s 硬间隔语义)
    state.check_send_allowed(now=2000.0)  # 远超:放行


def test_record_send_writes_state_file(tmp_path: Path) -> None:
    path = tmp_path / "wechat-localdb" / "send_state.json"
    state = SendRateState(path)
    state.record_send(now=1728600000.0)
    data = json.loads(path.read_text(encoding="utf-8"))
    assert data["last_send_epoch"] == 1728600000.0
    assert load_last_send_epoch(path) == 1728600000.0


def test_record_send_leaves_no_tmp_residue(tmp_path: Path) -> None:
    """原子写(临时文件 + replace)不留 .tmp 残余。"""
    path = tmp_path / "send_state.json"
    SendRateState(path).record_send(now=1.0)
    assert list(tmp_path.glob(".*tmp")) == []
    assert path.is_file()


def test_corrupt_state_file_reads_as_never_sent(tmp_path: Path) -> None:
    """坏状态文件 = 从未发过(状态丢失只会放行首发,不会错拒,也不会炸)。"""
    path = tmp_path / "send_state.json"
    path.write_text("{broken", encoding="utf-8")
    assert load_last_send_epoch(path) is None
    SendRateState(path).check_send_allowed(now=42.0)  # 不抛


def test_wrong_typed_state_file_reads_as_never_sent(tmp_path: Path) -> None:
    path = tmp_path / "send_state.json"
    path.write_text(json.dumps({"last_send_epoch": "not-a-number"}), encoding="utf-8")
    assert load_last_send_epoch(path) is None


def test_lock_file_created_alongside_state(tmp_path: Path) -> None:
    """flock 防并发:锁文件与状态文件同目录(design §2)。"""
    path = tmp_path / "wechat-localdb" / "send_state.json"
    state = SendRateState(path)
    state.record_send(now=1.0)
    assert state.lock_path.name == "send_state.lock"
    assert state.lock_path.parent == path.parent


def test_record_then_check_roundtrip(tmp_path: Path) -> None:
    """记录 → 间隔内拒 → 间隔外放(临界区行为闭环)。"""
    state = SendRateState(tmp_path / "send_state.json")
    state.record_send(now=100.0)
    with pytest.raises(BridgeError):
        state.check_send_allowed(now=105.0)
    state.record_send(now=200.0)
    with pytest.raises(BridgeError):
        state.check_send_allowed(now=205.0)
    state.check_send_allowed(now=210.5)


# ---------------------------------------------------------------------------
# 占位原语(reserve/rollback):G6 红线间隔在并发下封闭
# ---------------------------------------------------------------------------


def test_reserve_send_stamps_and_returns_previous(tmp_path: Path) -> None:
    """首次占位:检查+落戳同临界区,返回占位前值(None=从未发过)。"""
    path = tmp_path / "wechat-localdb" / "send_state.json"
    state = SendRateState(path)
    assert state.reserve_send(now=1000.0) is None
    assert load_last_send_epoch(path) == 1000.0
    # 间隔内再次占位 → exit 14,状态零副作用(未被第二进程改写)。
    with pytest.raises(BridgeError) as excinfo:
        state.reserve_send(now=1005.0)
    assert excinfo.value.exit_code == 14
    assert excinfo.value.retry_after_seconds == pytest.approx(5.0)
    assert load_last_send_epoch(path) == 1000.0
    # 间隔外(≥10s)→ 过检占位成功。
    assert state.reserve_send(now=1010.0) == 1000.0


def test_rollback_reserve_restores_never_sent(tmp_path: Path) -> None:
    """占位前从未发过:失败还原 = 删状态文件(重试窗口不被吞)。"""
    path = tmp_path / "send_state.json"
    state = SendRateState(path)
    previous = state.reserve_send(now=100.0)
    assert previous is None
    assert state.rollback_reserve(100.0, previous) is True
    assert load_last_send_epoch(path) is None
    assert not path.exists()


def test_rollback_reserve_restores_previous_epoch(tmp_path: Path) -> None:
    """占位前已有更早发送:失败还原 = 精确写回占位前时刻。"""
    path = tmp_path / "send_state.json"
    state = SendRateState(path)
    state.record_send(now=90.0)
    previous = state.reserve_send(now=100.0)
    assert previous == 90.0
    assert state.rollback_reserve(100.0, previous) is True
    assert load_last_send_epoch(path) == 90.0


def test_rollback_reserve_noop_when_other_process_advanced(tmp_path: Path) -> None:
    """他进程已更新状态(占位后真发成功)→ 不动、返回 False。"""
    path = tmp_path / "send_state.json"
    state = SendRateState(path)
    state.reserve_send(now=100.0)
    state.record_send(now=200.0)  # 模拟他进程的更新
    assert state.rollback_reserve(100.0, None) is False
    assert load_last_send_epoch(path) == 200.0


def test_concurrent_reserve_only_one_passes(tmp_path: Path) -> None:
    """并发两个 send_text 子进程占位:flock 串行化,只有一个过检(G6 红线
    在并发下封闭——两段式 check/record 在此场景会双双过检)。"""
    pytest.importorskip("fcntl")  # flock 并发语义是 posix 面;Windows 备胎另启
    import threading

    path = tmp_path / "wechat-localdb" / "send_state.json"
    state = SendRateState(path)
    start = threading.Barrier(2)
    results: list[str] = []
    lock = threading.Lock()

    def worker() -> None:
        start.wait()
        try:
            state.reserve_send(now=1000.0)
            outcome = "reserved"
        except BridgeError as exc:
            outcome = f"rejected:{exc.exit_code}"
        with lock:
            results.append(outcome)

    threads = [threading.Thread(target=worker) for _ in range(2)]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
    # 恰好一个占位成功,另一个被 exit 14 拒(实际间隔 <10s 不可能出现)。
    assert sorted(results) == ["rejected:14", "reserved"]
    assert load_last_send_epoch(path) == 1000.0
