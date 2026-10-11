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
