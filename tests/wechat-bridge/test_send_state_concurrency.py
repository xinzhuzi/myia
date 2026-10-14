"""send_state 真子进程并发测试(S3;10-14 followups)。

r3 留档疑点:「检查+占位」的 flock 封闭在**真跨进程并发**下是否成立
(既有单测全是单进程 mock 注入时间)。本文件用 multiprocessing 真
spawn 两个进程同一时刻打同一状态文件,验证 G6 红线:并发下恰一个
占位、另一个被间隔门拒(exit 14,状态零副作用);同指纹 pending
命中 exit 17 绝不自动重试。零微信交互、零真实发送。
"""

from __future__ import annotations

import multiprocessing as mp
import sys
from pathlib import Path

import pytest

COMPONENT_SRC = Path(__file__).resolve().parents[2] / "plugins" / "wechat-bridge"
if str(COMPONENT_SRC) not in sys.path:
    sys.path.insert(0, str(COMPONENT_SRC))


def _child_attempt(state_path: str, now: float, fingerprint: str, out_q: mp.Queue) -> None:  # type: ignore[type-arg]
    """子进程:对共享状态文件做一次「占位」尝试,把结局塞回队列。"""
    from wechat_bridge.codes import SEND_RATE_LIMITED, SEND_UNCERTAIN_DEDUP, BridgeError
    from wechat_bridge.send_state import SendRateState

    st = SendRateState(Path(state_path))
    try:
        outcome = st.reserve_send_dedup(now, fingerprint)
        out_q.put(("reserved", outcome.dedup))
    except BridgeError as exc:
        out_q.put(("rejected", exc.exit_code, SEND_RATE_LIMITED == exc.exit_code, SEND_UNCERTAIN_DEDUP == exc.exit_code))


class TestCrossProcessConcurrency:
    def test_concurrent_different_fingerprints_exactly_one_wins(self, tmp_path: Path) -> None:
        """异指纹并发(同一注入时刻):flock 临界区内串行化——恰一个
        占位成功,另一个过指纹门后撞间隔门 exit 14 且零副作用。"""
        ctx = mp.get_context("spawn")
        state = tmp_path / "send_state.json"
        q: mp.Queue = ctx.Queue()  # type: ignore[type-arg]
        procs = [
            ctx.Process(target=_child_attempt, args=(str(state), 1000.0, fp, q))
            for fp in ("fp-alpha", "fp-beta")
        ]
        for p in procs:
            p.start()
        results = [q.get(timeout=10) for _ in procs]
        for p in procs:
            p.join(timeout=10)
        winners = [r for r in results if r[0] == "reserved"]
        losers = [r for r in results if r[0] == "rejected"]
        assert len(winners) == 1, f"并发占位必须恰一个,实得 {results}"
        assert len(losers) == 1, f"另一个必须被拒,实得 {results}"
        assert losers[0][1] == 14 and losers[0][2], "落败方应撞间隔门 exit 14"

    def test_pending_fingerprint_blocks_second_process_exit_17(self, tmp_path: Path) -> None:
        """同指纹 pending 命中:第二个进程 exit 17(绝不自动重试),零占位。"""
        from wechat_bridge.send_state import SendRateState

        state = tmp_path / "send_state.json"
        st = SendRateState(state)
        st.mark_fingerprint_pending("fp-x", 1000.0)
        ctx = mp.get_context("spawn")
        q: mp.Queue = ctx.Queue()  # type: ignore[type-arg]
        p = ctx.Process(target=_child_attempt, args=(str(state), 1000.5, "fp-x", q))
        p.start()
        result = q.get(timeout=10)
        p.join(timeout=10)
        assert result[0] == "rejected" and result[1] == 17 and result[3], f"应 exit 17,实得 {result}"

    def test_interval_lock_holds_across_processes_after_reservation(self, tmp_path: Path) -> None:
        """占位后的 9 秒内,新进程(新指纹)也被间隔门拒——跨进程读得到
        刚落的占位时间戳(flock+原子写联合语义)。"""
        ctx = mp.get_context("spawn")
        state = tmp_path / "send_state.json"
        q: mp.Queue = ctx.Queue()  # type: ignore[type-arg]
        p1 = ctx.Process(target=_child_attempt, args=(str(state), 2000.0, "fp-a", q))
        p1.start()
        assert q.get(timeout=10)[0] == "reserved"
        p1.join(timeout=10)
        p2 = ctx.Process(target=_child_attempt, args=(str(state), 2000.0 + 9.0, "fp-b", q))
        p2.start()
        result = q.get(timeout=10)
        p2.join(timeout=10)
        assert result[0] == "rejected" and result[1] == 14, f"9s<10s 应拒,实得 {result}"
