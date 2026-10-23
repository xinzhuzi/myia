"""发送频控 + 防重指纹的跨进程落盘状态(G6 红线级;design §2 实现修正节;
2026-10-14 task 10-14-wechat-send-text 扩展为「间隔门 + 多槽指纹门」双原语)。

桥为一次性子进程,进程退出内存状态即失——频控时间戳与防重指纹**必须落盘**
``<数据根>/wechat-localdb/send_state.json``(flock 防并发,非敏感元数据)。

红线参数(G6,design §7 刻意无配置键):

- 单次调用只发一条;
- 两次发送硬间隔 ≥10 秒(:data:`SEND_MIN_INTERVAL_SECONDS`,硬编码);
- 同指纹(sha256(username+"\\0"+body))120 秒内防重
  (:data:`DEDUP_WINDOW_SECONDS`,硬编码);
- 不提供批量接口、不做配置面。

状态文件形状(两键;旧格式仅 ``last_send_epoch`` 一键,可读兼容——缺
``send_fingerprints`` 键 = 无指纹态)::

    {"last_send_epoch": 1730000000.0,
     "send_fingerprints": {"<sha256hex>": {"status": "pending|sent", "ts": …}}}

**门序论证(design §C-3/§J-5)**:发送路径专用原语
:meth:`SendRateState.reserve_send_dedup` 在同一 flock 临界区内三步,
**指纹门在前、间隔门在后**——幂等命中(指纹 sent,窗内)不占位、不该
再被间隔门拦:立即重复同指纹得幂等 exit 0 而非 exit 14;指纹 pending
命中 → exit 17(uncertain-never-retry,绝不自动重试);两门同临界区,
无 TOCTOU 缝。

**多槽并发论证(design §C-3/§J-10)**:``send_fingerprints`` 是 dict
(键=指纹,值={status,ts})而非单槽——单槽会被并发异指纹覆盖,A 的
pending 保护失效。写入时顺手清扫:删过期条目(ts 距 now >
:data:`DEDUP_WINDOW_SECONDS`)+ 容量上限 :data:`FINGERPRINT_CAPACITY`
(超限按 ts 淘汰最旧)。A 的 pending 档不会被 B 的异指纹发送挤掉——
120s 窗内 A 的同指纹重发仍被拒(exit 17)。

**写路径保全论证(design §C-3/§J-16,硬指令)**:本模块**任何**落盘都
经 :meth:`SendRateState._write_unlocked` 的**读-改-写**实现——临界区内
先读现文件、原样保留 ``send_fingerprints`` 键、只更新目标键再原子落盘
(tmp+``os.replace``)。若按旧实现整写 ``{"last_send_epoch": …}``,任何
一次占位/还原都会整抹指纹档:B 异指纹失败 rollback 即抹 A 的 pending
(实洞,已修)。既有公共原语(reserve_send/check_send_allowed/
record_send/load_last_send_epoch)的外部可观测行为零改动。

**rollback 两分支纪律(design §C-3/§J-16)**::

    rollback_reserve          只动 last_send_epoch(经读-改-写保指纹);
      无指纹档(previous=None)→ unlink 文件(旧行为,既有断言锁死);
      有指纹档(previous=None)→ 移除 last_send_epoch 键、保留指纹档
        (unlink 会把 A 的 pending 一起删);
      previous 有值           → 精确写回占位前时刻(读-改-写)。
    rollback 只在未发出路径(on_armed 之前)可及;on_armed 之后 sendui
    恒不抛(design §C-5),rollback 天然不触发——指纹 pending 不随
    rollback 还原,「armed 过即视同 uncertain」(design §C-4)。

**pending 时点 = on_armed(回车 down 前;design §C-4/WZ:270-271 同序)**:
回车事件被系统丢弃的尝试也会被锁 120s——宁可误锁,不开「已发出却无
指纹」的双发窗。

并发纪律:flock 独立锁文件(``.lock``)守护临界区,状态本体走临时文件 +
``os.replace`` 原子写(与壳侧组件戳 write_stamp 同款)——锁文件锁的是
临界区,不是状态文件本身(避免截断竞态)。时间全部经参数注入(单测不真
等 10 秒,design §8)。
"""

from __future__ import annotations

import json
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .codes import EXIT_OK, SEND_RATE_LIMITED, SEND_UNCERTAIN_DEDUP, BridgeError
from .config import myssia_home

__all__ = [
    "DEDUP_WINDOW_SECONDS",
    "FINGERPRINT_CAPACITY",
    "ReserveOutcome",
    "SEND_MIN_INTERVAL_SECONDS",
    "SendRateState",
    "default_send_state_path",
    "load_last_send_epoch",
]

#: 两次发送硬间隔(秒;G6 红线,硬编码——design §7 刻意无配置键)。
SEND_MIN_INTERVAL_SECONDS = 10.0
#: 同指纹防重窗(秒;WZ:143-158 同参数,硬编码——G6 同风格无配置键)。
DEDUP_WINDOW_SECONDS = 120.0
#: 多槽指纹容量上限(清扫用;防状态文件无限膨胀,design §C-3)。
FINGERPRINT_CAPACITY = 8


@dataclass(frozen=True)
class ReserveOutcome:
    """占位原语结果(design §C-3)。

    ``previous``:占位前时间戳(rollback 用;dedup 命中未占位时 None)。
    ``dedup``:None = 正常占位;"sent_recently" = 指纹命中且已发
    (幂等,未占位,调用方 exit 0 载荷)。
    """

    previous: float | None
    dedup: str | None


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


def _uncertain_dedup_error(remaining: float) -> BridgeError:
    """exit 17 载荷(指纹 pending 命中;uncertain-never-retry,design §E-3)。"""
    return BridgeError(
        SEND_UNCERTAIN_DEDUP,
        f"上次同指纹发送状态不确定(pending,{DEDUP_WINDOW_SECONDS:.0f}s 窗内,"
        f"剩 {remaining:.0f}s):绝不自动重试",
        fix_hint="等待窗口过期或更换正文;人工确认上次发送结果后再操作",
    )


def _sweep_fingerprints(
    entries: dict[str, dict[str, Any]], now: float
) -> dict[str, dict[str, Any]]:
    """指纹档清扫(**临界区内调用**):删过期(> :data:`DEDUP_WINDOW_SECONDS`)
    + 容量上限(超限按 ts 淘汰最旧)。形状非法条目一并剔除(坏行不拦发送)。"""
    cleaned: dict[str, dict[str, Any]] = {}
    for key, entry in entries.items():
        if not isinstance(key, str) or not isinstance(entry, dict):
            continue
        status = entry.get("status")
        ts = entry.get("ts")
        if status not in ("pending", "sent"):
            continue
        if isinstance(ts, bool) or not isinstance(ts, (int, float)):
            continue
        cleaned[key] = {"status": status, "ts": float(ts)}
    live = {
        key: entry
        for key, entry in cleaned.items()
        if (now - entry["ts"]) < DEDUP_WINDOW_SECONDS
    }
    if len(live) > FINGERPRINT_CAPACITY:
        oldest = sorted(live.items(), key=lambda kv: kv[1]["ts"])
        for key, _entry in oldest[: len(live) - FINGERPRINT_CAPACITY]:
            del live[key]
    return live


class SendRateState:
    """频控状态文件的家(send_state.json + .lock;路径可注入 = 单测隔离)。

    发送路径一律走 :meth:`reserve_send_dedup`(指纹门+间隔门同临界区);
    旧 :meth:`reserve_send` 保留原样公共行为(诊断/兼容;docstring 注明
    发送路径走新原语)。两段式 ``check_send_allowed`` / ``record_send``
    是单步原语,供诊断与测试,不承载「检查→发送→落戳」链。
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

    def _read_full_unlocked(self) -> dict[str, Any]:
        """读整份状态(**临界区内调用**)。缺文件/坏文件/非 dict = 空态
        (如实,坏行不拦发送——状态丢失只会放行首发,不会错拒)。"""
        path = self.state_path()
        if not path.is_file():
            return {}
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            return {}
        return data if isinstance(data, dict) else {}

    def _fingerprints_unlocked(self, full: dict[str, Any]) -> dict[str, dict[str, Any]]:
        """从整份状态取指纹档(形状非法 → 空 dict;不重写文件)。"""
        raw = full.get("send_fingerprints")
        if not isinstance(raw, dict):
            return {}
        cleaned = _sweep_fingerprints(raw, now=self._now_for_sweep(raw))
        return cleaned

    @staticmethod
    def _now_for_sweep(raw: dict[str, Any]) -> float:
        """清扫基准时刻:取档内最新 ts(单调方向近似;调用方带 now 的
        原语不走本函数,只读路径用它避免臆造时钟)。"""
        best = 0.0
        for entry in raw.values():
            if isinstance(entry, dict):
                ts = entry.get("ts")
                if isinstance(ts, (int, float)) and not isinstance(ts, bool):
                    best = max(best, float(ts))
        return best

    def _dump_unlocked(self, full: dict[str, Any]) -> None:
        """原子落盘整份状态(**临界区内调用**;tmp + os.replace,不留残余)。"""
        path = self.state_path()
        tmp = path.with_name(f".{path.name}.tmp")
        tmp.write_text(
            json.dumps(full, ensure_ascii=False, indent=1), encoding="utf-8"
        )
        os.replace(tmp, path)

    def _read_unlocked(self) -> float | None:
        """读上次发送时刻(**临界区内调用**)。缺键/坏值 = 从未发过(None)。"""
        value = self._read_full_unlocked().get("last_send_epoch")
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            return None
        return float(value)

    def _write_unlocked(self, epoch: float) -> None:
        """写上次发送时刻(**临界区内调用**)。

        **读-改-写保指纹键**(design §J-16 硬指令):先读现文件原样保留
        ``send_fingerprints``,只更新 ``last_send_epoch`` 再原子落盘——
        单键整写会整抹指纹档(B 异指纹 rollback 抹 A pending,实洞)。
        私有实现升级,公共原语外部可观测行为不变。
        """
        full = self._read_full_unlocked()
        full["last_send_epoch"] = float(epoch)
        full.setdefault("send_fingerprints", {})
        self._dump_unlocked(full)

    # ------------------------------------------------- 占位原语(发送路径)

    def reserve_send(self, now: float) -> float | None:
        """原子「检查 + 占位」:同一 flock 临界区内先验间隔再落时间戳。

        并发两个 send_text 子进程只有一个能过检占位——G6 红线 ≥10s 硬间隔
        在并发下封闭(两段式的 TOCTOU 缝在此闭合)。时间戳即占位:真发送
        成功无须再记;发送失败调 :meth:`rollback_reserve` 还原占位。

        **发送路径走 :meth:`reserve_send_dedup`**(间隔门+指纹门合成;
        本原语保留给诊断/兼容)。

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

    def reserve_send_dedup(self, now: float, fingerprint: str) -> ReserveOutcome:
        """发送路径专用:同一 flock 临界区内「指纹门 → 间隔门 → 占位」。

        门序 = **指纹门在前、间隔门在后**(design §C-3/§J-5:幂等命中
        不占位不该被间隔拦;立即重复同指纹 → 幂等而非 exit 14):

        1. 指纹门(只读,不预落):档内 fingerprint 命中且窗内
           (:data:`DEDUP_WINDOW_SECONDS`)——
           status=sent → :class:`ReserveOutcome`\\ ``(None,
           "sent_recently")``(幂等,**未占位**);
           status=pending → BridgeError(17,绝不自动重试);
        2. 间隔门(判据不变):previous 在且 now-previous <10s → exit 14;
        3. 占位:写 ``last_send_epoch=now``(经读-改-写保指纹键)+ 顺手
           清扫指纹档;指纹条目不写(只在 on_armed 落 pending)。

        Args:
            now: 本次发送时刻(epoch 秒;注入)。
            fingerprint: sha256(username + "\\0" + body) hex——键用解析后
                username,同一人 alias/wxid/展示名三种叫法指纹相同,防重闭合。

        Raises:
            BridgeError: exit 17(指纹 pending 命中,未占位)/ exit 14
                (间隔不足,未占位)——两者状态零副作用。
        """

        def op(_: Any) -> ReserveOutcome:
            full = self._read_full_unlocked()
            entries = self._fingerprints_unlocked(full)
            entry = entries.get(fingerprint)
            if entry is not None and (now - entry["ts"]) < DEDUP_WINDOW_SECONDS:
                if entry["status"] == "sent":
                    return ReserveOutcome(previous=None, dedup="sent_recently")
                raise _uncertain_dedup_error(DEDUP_WINDOW_SECONDS - (now - entry["ts"]))
            value = full.get("last_send_epoch")
            previous = (
                float(value)
                if isinstance(value, (int, float)) and not isinstance(value, bool)
                else None
            )
            if (
                previous is not None
                and (now - previous) < SEND_MIN_INTERVAL_SECONDS
            ):
                raise _rate_limit_error(SEND_MIN_INTERVAL_SECONDS - (now - previous))
            full["last_send_epoch"] = float(now)
            full["send_fingerprints"] = _sweep_fingerprints(entries, now=now)
            self._dump_unlocked(full)
            return ReserveOutcome(previous=previous, dedup=None)

        return self._locked(op)

    def rollback_reserve(self, reserved_epoch: float, previous_epoch: float | None) -> bool:
        """撤销占位(发送失败时调用):仅当状态仍是本次占位值时还原。

        状态被并发他进程更新过(占位后他进程真发成功)→ 不动并返回 False
        (不吞他进程的频控事实);还原成功返回 True——失败尝试由此不吞
        重试窗口。还原语义(design §J-16 两分支):

        - **无指纹档**(现文件无 ``send_fingerprints`` 或空 dict):
          previous None → 删状态文件(旧行为完全不变,既有断言锁死);
          previous 有值 → 精确写回占位前时刻;
        - **有指纹档**:previous None 时**不再 unlink**,改为移除
          ``last_send_epoch`` 键、保留指纹档(unlink 会把 A 的 pending
          一起删);previous 有值 → 写回(经读-改-写保指纹)。
        """

        def op(_: Any) -> bool:
            full = self._read_full_unlocked()
            value = full.get("last_send_epoch")
            current = (
                float(value)
                if isinstance(value, (int, float)) and not isinstance(value, bool)
                else None
            )
            if current is None or current != float(reserved_epoch):
                return False
            has_fingerprints = bool(self._fingerprints_unlocked(full))
            if previous_epoch is None:
                if has_fingerprints:
                    full.pop("last_send_epoch", None)
                    self._dump_unlocked(full)
                else:
                    self.state_path().unlink(missing_ok=True)
                return True
            full["last_send_epoch"] = float(previous_epoch)
            if has_fingerprints:
                self._dump_unlocked(full)
            else:
                self._write_unlocked(float(previous_epoch))
            return True

        return self._locked(op)

    # --------------------------------------------- 指纹原语(on_armed/回执)

    def mark_fingerprint_pending(self, key: str, now: float) -> None:
        """落指纹 pending(on_armed 调 = 回车 down 前;design §C-4)。

        只写自己的 key 不覆盖他档(多槽);顺手清扫(过期 + 容量)。
        原子性:tmp+os.replace,失败 = 未写或已写——已写后仍抛的窗口下,
        重试路径会发现指纹已 pending → exit 17(保守方向,docstring 注明)。
        """

        def op(_: Any) -> None:
            full = self._read_full_unlocked()
            entries = _sweep_fingerprints(
                full.get("send_fingerprints")
                if isinstance(full.get("send_fingerprints"), dict)
                else {},
                now=now,
            )
            entries[key] = {"status": "pending", "ts": float(now)}
            entries = _sweep_fingerprints(entries, now=now)  # 含新档再清容量
            full["last_send_epoch"] = full.get("last_send_epoch", float(now))
            full["send_fingerprints"] = entries
            self._dump_unlocked(full)

        self._locked(op)

    def mark_fingerprint_sent(self, key: str, now: float) -> None:
        """回执全绿后升级指纹 pending → sent(on_receipt_green 调)。

        仅当档内 key 存在且 status=pending 才升级(不同/缺档 = 他进程的
        后发占了自己档,不覆盖——该次发送的防重窗以 pending 态继续有效,
        保守方向;design §C-3)。
        """

        def op(_: Any) -> None:
            full = self._read_full_unlocked()
            raw = full.get("send_fingerprints")
            if not isinstance(raw, dict):
                return
            entry = raw.get(key)
            if not isinstance(entry, dict) or entry.get("status") != "pending":
                return
            entry["status"] = "sent"
            entry["ts"] = float(now)
            full["send_fingerprints"] = _sweep_fingerprints(raw, now=now)
            self._dump_unlocked(full)

        self._locked(op)

    # --------------------------------------------- 单步原语(诊断/测试用)

    def load_last_send_epoch(self) -> float | None:
        """上次发送时刻(epoch 秒);缺文件/坏文件 = 从未发过(None 如实)。"""
        return self._locked(lambda _: self._read_unlocked())

    def check_send_allowed(self, now: float) -> None:
        """发送前检查(只读零副作用;诊断/测试用——**发送路径走
        :meth:`reserve_send_dedup`**,两段式在并发下有 TOCTOU 缝)。

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
        还原见 :meth:`reserve_send_dedup` / :meth:`rollback_reserve`)。"""
        self._locked(lambda _: self._write_unlocked(float(now)))


def default_send_state_path() -> Path:
    """缺省状态文件路径(诊断面用;逻辑态经 :class:`SendRateState`)。"""
    return SendRateState().state_path()


def load_last_send_epoch(state_path: Path | None = None) -> float | None:
    """模块级便捷读(单测/诊断;发送路径走 :class:`SendRateState` 占位原语)。"""
    return SendRateState(state_path).load_last_send_epoch()


# 静态对账:exit 14/17 的码值与 codes 表一致(改码先改 design §6)。
assert SEND_RATE_LIMITED == 14 and EXIT_OK == 0 and SEND_UNCERTAIN_DEDUP == 17
