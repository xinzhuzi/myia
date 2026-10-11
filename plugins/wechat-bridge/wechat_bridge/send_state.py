"""发送频控的跨进程落盘状态(G6 红线级;design §2 实现修正节)。

桥为一次性子进程,进程退出内存状态即失——频控时间戳**必须落盘**
``<数据根>/wechat-localdb/send_state.json``(上次发送时刻,flock 防并发,
非敏感元数据);每次发送前检查 + 原子更新,间隔不足 10s 直接拒发并返回
剩余等待秒数。

红线参数(G6,design §7 刻意无配置键):

- 单次调用只发一条;
- 两次发送硬间隔 ≥10 秒(:data:`SEND_MIN_INTERVAL_SECONDS`,硬编码);
- 不提供批量接口、不做配置面。

并发纪律:flock 独立锁文件(``.lock``)守护「读-判-写」临界区,状态本体
走临时文件 + ``os.replace`` 原子写(与壳侧组件戳 write_stamp 同款)——
锁文件锁的是临界区,不是状态文件本身(避免截断竞态)。时间全部经参数
注入(单测不真等 10 秒,design §8)。
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


class SendRateState:
    """频控状态文件的家(send_state.json + .lock;路径可注入 = 单测隔离)。"""

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

    # ------------------------------------------------------------- 读/写

    def load_last_send_epoch(self) -> float | None:
        """上次发送时刻(epoch 秒);缺文件/坏文件 = 从未发过(None 如实,
        坏行不拦发送——状态丢失只会放行首发,不会错拒)。"""
        def read(_: Any) -> float | None:
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

        return self._locked(read)

    def check_send_allowed(self, now: float) -> None:
        """发送前检查:间隔不足 → :class:`BridgeError`(exit 14,含剩余秒)。

        剩余秒 = ``interval - (now - last)``;上限取两位小数(UI 倒计时
        够用,不泄露时钟精度),最小 0.01 防 0 值歧义。
        """
        last = self.load_last_send_epoch()
        if last is None:
            return
        elapsed = now - last
        if elapsed >= SEND_MIN_INTERVAL_SECONDS:
            return
        retry_after = round(SEND_MIN_INTERVAL_SECONDS - elapsed, 2) or 0.01
        raise BridgeError(
            SEND_RATE_LIMITED,
            f"频控拒发(G6 硬间隔 {SEND_MIN_INTERVAL_SECONDS:.0f}s):"
            f"距上次发送尚差 {retry_after:.2f}s",
            fix_hint="等待剩余秒数后重试;桥不提供批量接口与频控配置(G6)",
            retry_after_seconds=retry_after,
        )

    def record_send(self, now: float) -> None:
        """记录一次成功发送(原子写;仅在 AX 发送回执确认后调用——失败的
        尝试不落时间戳,不吞掉重试窗口)。"""
        def write(_: Any) -> None:
            path = self.state_path()
            tmp = path.with_name(f".{path.name}.tmp")
            payload = json.dumps(
                {"last_send_epoch": float(now)}, ensure_ascii=False, indent=1
            )
            tmp.write_text(payload, encoding="utf-8")
            os.replace(tmp, path)

        self._locked(write)


def default_send_state_path() -> Path:
    """缺省状态文件路径(诊断面用;逻辑态经 :class:`SendRateState`)。"""
    return SendRateState().state_path()


def load_last_send_epoch(state_path: Path | None = None) -> float | None:
    """模块级便捷读(单测/诊断;发送路径走 :class:`SendRateState` 临界区)。"""
    return SendRateState(state_path).load_last_send_epoch()


# 静态对账:exit 14 的码值与 codes 表一致(改码先改 design §6)。
assert SEND_RATE_LIMITED == 14 and EXIT_OK == 0
