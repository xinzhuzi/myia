"""发送频控的跨进程落盘状态(G6 红线级;design §2 实现修正节)。

桥为一次性子进程,进程退出内存状态即失——频控时间戳**必须落盘**
``<数据根>/wechat-localdb/send_state.json``(上次发送时刻,flock 防并发,
非敏感元数据);两次发送硬间隔不足 10s 直接拒发并返回剩余等待秒数。

红线参数(G6,design §7 刻意无配置键):

- 单次调用只发一条;
- 两次发送硬间隔 ≥10 秒(:data:`SEND_MIN_INTERVAL_SECONDS`,硬编码);
- 不提供批量接口、不做配置面。

并发纪律:flock 独立锁文件(``.lock``)守护临界区,状态本体走临时文件 +
``os.replace`` 原子写(与壳侧组件戳 write_stamp 同款)——锁文件锁的是
临界区,不是状态文件本身(避免截断竞态)。时间全部经参数注入(单测不真
等 10 秒,design §8)。

**并发封闭(G6 实现层闭环)**:发送路径用 :meth:`SendRateState.reserve_send`
把「检查间隔 + 落时间戳」收进**同一** flock 临界区——「先检查、发送后再
落戳」的两段式在并发下有 TOCTOU 缝(两个 send_text 子进程可同时过检、
实际间隔 <10s,红线间隔不封闭),故发送一律走占位原语:过检即占位,
真发送成功无须再记;失败调 :meth:`rollback_reserve` 精确还原为占位前值
(失败尝试不吞重试窗口;他进程已更新状态则不动)。两段式的
``check_send_allowed`` / ``record_send`` 保留为单步原语(诊断/测试用),
发送路径不再使用。
"""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any

from .codes import EXIT_OK, SEND_RATE_LIMITED, BridgeError
from .config import myssia_home

__all__ = [
    "SEND_MIN_INTERVAL_SECONDS",
    "SendRateState",
    "default_send_state_path",
    "load_last_send_epoch",
]

#: 两次发送硬间隔(秒;G6 红线,硬编码——design §7 刻意无配置键)。
SEND_MIN_INTERVAL_SECONDS = 10.0


def _rate_limit_error(remaining: float) -> BridgeError:
    """exit 14 载荷(检查与占位共用同一文案形状,golden 基件对账)。

    剩余秒 = ``remaining``;上限取两位小数(UI 倒计时够用,不泄露时钟
    精度),最小 0.01 防 0 值歧义。
    """
    retry_after = round(remaining, 2) or 0.01
    return BridgeError(
        SEND_RATE_LIMITED,
        f"频控拒发(G6 硬间隔 {SEND_MIN_INTERVAL_SECONDS:.0f}s):"
        f"距上次发送尚差 {retry_after:.2f}s",
        fix_hint="等待剩余秒数后重试;桥不提供批量接口与频控配置(G6)",
        retry_after_seconds=retry_after,
    )


class SendRateState:
    """频控状态文件的家(send_state.json + .lock;路径可注入 = 单测隔离)。

    发送路径一律走 :meth:`reserve_send` 占位原语(并发封闭);两段式
    ``check_send_allowed`` / ``record_send`` 是单步原语,供诊断与测试,
    不再承载「检查→发送→落戳」链(并发下不封闭,见模块 docstring)。
    """

    def __init__(self, state_path: Path | None = None) -> None:
        self._override = state_path

    def state_path(self) -> Path:
        """状态文件绝对路径(数据根 wechat-localdb/send_state.json)。"""
        if self._override is not None:
            return self._override
        return myssia_home() / "wechat-localdb" / "send_state.json"

    @property
    def lock_path(self) -> Path:
        return self.state_path().with_suffix(".lock")

    def _ensure_dir(self) -> Path:
        directory = self.state_path().parent
        directory.mkdir(parents=True, exist_ok=True)
        return directory

    # ------------------------------------------------------------- 临界区

    def _locked(self, action: Any) -> Any:
        """在 flock 临界区内执行 ``action(lock_fd)``(posix fcntl;非 posix
        平台退化为无锁直跑——桥 macOS 先行,Windows 备胎另启,注释如实)。"""
        self._ensure_dir()
        try:
            import fcntl  # posix
        except ImportError:  # pragma: no cover - Windows 备胎线另启
            return action(None)
        with open(self.lock_path, "w", encoding="utf-8") as lock_fd:
            fcntl.flock(lock_fd.fileno(), fcntl.LOCK_EX)
            try:
                return action(lock_fd)
            finally:
                fcntl.flock(lock_fd.fileno(), fcntl.LOCK_UN)

    # --------------------------------------------------- 临界区内读/写原语

    def _read_unlocked(self) -> float | None:
        """读上次发送时刻(**临界区内调用**)。缺文件/坏文件 = 从未发过
        (None 如实,坏行不拦发送——状态丢失只会放行首发,不会错拒)。"""
        path = self.state_path()
        if not path.is_file():
            return None
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            return None
        value = data.get("last_send_epoch") if isinstance(data, dict) else None
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            return None
        return float(value)

    def _write_unlocked(self, epoch: float) -> None:
        """写上次发送时刻(**临界区内调用**;临时文件 + os.replace 原子写,
        不留 .tmp 残余)。"""
        path = self.state_path()
        tmp = path.with_name(f".{path.name}.tmp")
        payload = json.dumps(
            {"last_send_epoch": float(epoch)}, ensure_ascii=False, indent=1
        )
        tmp.write_text(payload, encoding="utf-8")
        os.replace(tmp, path)

    # ------------------------------------------------- 占位原语(发送路径)

    def reserve_send(self, now: float) -> float | None:
        """原子「检查 + 占位」:同一 flock 临界区内先验间隔再落时间戳。

        并发两个 send_text 子进程只有一个能过检占位——G6 红线 ≥10s 硬间隔
        在并发下封闭(两段式的 TOCTOU 缝在此闭合)。时间戳即占位:真发送
        成功无须再记;发送失败调 :meth:`rollback_reserve` 还原占位。

        Args:
            now: 本次发送时刻(epoch 秒;调用方注入,单测不真等)。

        Returns:
            占位前的上次发送时刻(None = 此前从未发过)——供
            :meth:`rollback_reserve` 精确还原。

        Raises:
            BridgeError: exit 14(间隔不足;**未占位**,状态零副作用)。
        """

        def op(_: Any) -> float | None:
            previous = self._read_unlocked()
            if previous is not None and (now - previous) < SEND_MIN_INTERVAL_SECONDS:
                raise _rate_limit_error(SEND_MIN_INTERVAL_SECONDS - (now - previous))
            self._write_unlocked(float(now))
            return previous

        return self._locked(op)

    def rollback_reserve(self, reserved_epoch: float, previous_epoch: float | None) -> bool:
        """撤销占位(发送失败时调用):仅当状态仍是本次占位值时还原。

        状态被并发他进程更新过(占位后他进程真发成功)→ 不动并返回 False
        (不吞他进程的频控事实);还原成功返回 True——失败尝试由此不吞
        重试窗口。还原语义:占位前从未发过(previous None)→ 删状态文件;
        否则精确写回占位前时刻。
        """

        def op(_: Any) -> bool:
            current = self._read_unlocked()
            if current is None or current != float(reserved_epoch):
                return False
            if previous_epoch is None:
                self.state_path().unlink(missing_ok=True)
            else:
                self._write_unlocked(float(previous_epoch))
            return True

        return self._locked(op)

    # --------------------------------------------- 单步原语(诊断/测试用)

    def load_last_send_epoch(self) -> float | None:
        """上次发送时刻(epoch 秒);缺文件/坏文件 = 从未发过(None 如实)。"""
        return self._locked(lambda _: self._read_unlocked())

    def check_send_allowed(self, now: float) -> None:
        """发送前检查(只读零副作用;诊断/测试用——**发送路径走
        :meth:`reserve_send`**,两段式在并发下有 TOCTOU 缝)。

        间隔不足 → :class:`BridgeError`(exit 14,含剩余秒)。
        """
        last = self.load_last_send_epoch()
        if last is None:
            return
        elapsed = now - last
        if elapsed >= SEND_MIN_INTERVAL_SECONDS:
            return
        raise _rate_limit_error(SEND_MIN_INTERVAL_SECONDS - elapsed)

    def record_send(self, now: float) -> None:
        """记录一次发送时刻(单步原子写;诊断/测试用——发送路径的占位与
        还原见 :meth:`reserve_send` / :meth:`rollback_reserve`)。"""
        self._locked(lambda _: self._write_unlocked(float(now)))


def default_send_state_path() -> Path:
    """缺省状态文件路径(诊断面用;逻辑态经 :class:`SendRateState`)。"""
    return SendRateState().state_path()


def load_last_send_epoch(state_path: Path | None = None) -> float | None:
    """模块级便捷读(单测/诊断;发送路径走 :class:`SendRateState` 占位原语)。"""
    return SendRateState(state_path).load_last_send_epoch()


# 静态对账:exit 14 的码值与 codes 表一致(改码先改 design §6)。
assert SEND_RATE_LIMITED == 14 and EXIT_OK == 0
