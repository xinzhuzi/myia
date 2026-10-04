"""投递重试账本:immediate 推送瞬态失败的 at-least-once 兜底(R1)。

蓝本:NousResearch/Hermes-Agent ``gateway/delivery_ledger.py``(MIT;上游
路径 ``~/.hermes/hermes-agent/gateway/delivery_ledger.py``)——持久投递
义务账本:``pending → attempting → delivered/failed → abandoned`` 状态机、
``MAX_ATTEMPTS=3``、退避 30s/120s(每档一次)、24h 过期、启动 sweep、
重试留最后一击给 boot sweep、一切 best-effort(账本故障绝不阻塞投递)。
本模块按 MYIA 形态移植,不整块抄;design 决策与蓝本的偏离如下:

1. **入账时机**:蓝本在发送**前**记 obligation(崩溃语义:pending=从未
   开始,attempting=await 中崩溃,平台可能已收到);MYIA 在 immediate
   发送**失败后**入队——条目=已确认失败的批次,at-least-once 语义靠
   重投实现。``attempting`` 仅用于重投途中崩溃的恢复标记:下一轮
   claim 即刻再认领(平台可能已收到上一击,可能重复——蓝本同款取舍;
   MYIA 无 ♻️ 恢复标记前缀基础设施,卡片模板不在本层,重复可能以日志
   说破)。
2. **存储**:数据根 JSON 文件(:data:`RETRY_LEDGER_FILENAME`,照
   :mod:`myssia.push.delivery` ``LEDGER_FILENAME`` 惯例:db 父目录、
   原子写 tmp+rename、损坏/不可写退化内存态),非蓝本的 SQLite
   state.db——MYIA 无多进程共享网关形态,JSON 是死信账本/通道目录的
   既定惯例。
3. **入队门槛**:仅 ``kind="immediate"`` 且 :func:`~myssia.push.delivery.classify_dead_error`
   无值(非死信)且非配置级错误码。digest 全通道失败有留池机制
   (:mod:`myssia.push.digest` 契约),immediate 原先瞬态失败即丢——本
   账本只补这个缺口;死信由 :class:`~myssia.push.delivery.DeliveryLedger`
   接管(重投无意义);配置级错误修配置才是出路,重试无解。
4. **通道构造参数不入账**:重投挂在 ``pipeline._push_channel`` 当轮构建
   的通道实例上(按通道名匹配)——配置即真相,通道参数变更后按新配置
   重投;通道从配置移除则条目按 24h 过期自然清退。同名多 push 条目时
   按当轮首个同名列的实例重投(v1 取舍,同通道类型仅 target/template
   差异)。
5. **目标 spec 入账**:定向条目存**源 spec**(由
   :func:`~myssia.push.delivery.send_batch_to_targets` 的目标↔spec 对齐
   提供),重投经 :func:`~myssia.push.digest.send_immediate` 走完整链路
   (解析/死信过滤/成功自愈),不绕过派发层语义;同槽位防重发闸门
   **跳过**(``slot_dedup=False``,换眼复审修复)——防重发键是条目级、
   不分子通道/子目标(:func:`myssia.dedup.DedupRegistry.should_send`),
   多通道/多目标部分成功即 record_push,失败侧的到期重投再过闸门会被
   拦成零报告而被冲账侧误记成功(消息静默丢失);重投条目本身即防重
   单元(认领即计次、投出即出队),罕见重复由 at-least-once 承担(蓝本
   「may be a duplicate」同款取舍)。
6. **蓝本的 flood_control 专用退避与重连专用错误族不移植**:MYIA 通道层
   尚无对应错误形态(飞书/TG 瞬态护栏由 R2 另行落地)。

调度语义(MYIA 的「boot sweep」):管线是周期 run 形态,每轮 run 推送
阶段开头 flush 到期条目(``pipeline._push_channel``),等价于蓝本「启动
sweep + 运行时重试 timer」的合体;退避的最后一击不设额外等待(立即
到期)——正是蓝本「留最后一击给 boot sweep」的 MYIA 形态,run 间隔
天然兜底。abandoned 记录保留 24h 观察窗后清退(蓝本 retention 的精简)。
"""

from __future__ import annotations

import hashlib
import json
import logging
import threading
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable, Mapping, Sequence

from myssia.push.base import item_view
from myssia.push.delivery import classify_dead_error, is_config_send_error

__all__ = [
    "MAX_ATTEMPTS",
    "RETRY_BACKOFF_SECONDS",
    "STALE_AFTER_SECONDS",
    "RETRY_LEDGER_FILENAME",
    "RetryEntry",
    "PushRetryLedger",
]

logger = logging.getLogger(__name__)

#: 重试账本文件名(数据根下;与死信账本 ``delivery_ledger.json`` 同目录惯例)。
RETRY_LEDGER_FILENAME = "push_retry_ledger.json"

#: 重投预算上限(蓝本 ``MAX_ATTEMPTS`` 同款):重投认领即计 1 次,≥3 次即弃置。
MAX_ATTEMPTS = 3

#: 退避档位(蓝本 ``_RETRY_BACKOFF_SECONDS`` 同款:每档一次,档数=预算-1;
#: 最后一击不设等待,留给下一轮 run 的 flush——蓝本「留最后一击给 boot sweep」)。
RETRY_BACKOFF_SECONDS: tuple[float, ...] = (30.0, 120.0)
assert len(RETRY_BACKOFF_SECONDS) == MAX_ATTEMPTS - 1

#: 条目时效(蓝本 ``STALE_AFTER_SECONDS`` 同款):超龄无条件弃置。
STALE_AFTER_SECONDS = 24 * 60 * 60.0

#: 活跃状态(等待重投/重投途中);终态 ``abandoned`` 留观察窗后清退。
_ACTIVE_STATES = frozenset({"pending", "attempting"})
_KNOWN_STATES = frozenset({"pending", "attempting", "abandoned"})


@dataclass(frozen=True)
class RetryEntry:
    """一条待重投的 immediate 批次(claim 返回/快照用只读形态)。

    ``items`` 是 :func:`~myssia.push.base.item_view` 序列化后的纯 dict 列表
    (通道渲染只读 view,重投经 send_immediate 原路消费);``attempts`` 为
    已花费的重投次数(认领即 +1,蓝本同款——崩溃不退款);``next_retry_at``
    为 None 表示 attempting 中(重投途中)。
    """

    entry_id: str
    channel: str
    items: list[dict[str, Any]]
    target_spec: str | None
    dedup_key: str | None
    state: str
    attempts: int
    created_at: float
    updated_at: float
    next_retry_at: float | None
    last_error: str


def _entry_id(channel: str, target_spec: str | None, views: Sequence[Mapping[str, Any]]) -> str:
    """稳定条目 id:同通道+同对象+同条目集合的重复失败幂等命中(蓝本
    ``compute_obligation_id`` 的 MYIA 对位——sha256 截断 24 位十六进制)。"""
    identity = "|".join(
        [
            str(channel).strip().lower(),
            (target_spec or "").strip(),
            *[str(view.get("dedup_key") or view.get("url") or "") for view in views],
        ]
    )
    return hashlib.sha256(identity.encode("utf-8", "replace")).hexdigest()[:24]


def _dedup_key_of(views: Sequence[Mapping[str, Any]]) -> str | None:
    """条目 dedup 键(可观测性;缺省回落 url,与 send_immediate 同口径)。"""
    if not views:
        return None
    key = views[0].get("dedup_key") or views[0].get("url")
    return str(key) if key else None


def _float_or_none(value: Any) -> float | None:
    if value is None:
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


class PushRetryLedger:
    """持久化 JSON 重试队列(蓝本 delivery ledger 的 MYIA 形态,见模块 docstring)。

    线程安全(RLock);读写 best-effort:损坏/不可写退化内存态,绝不阻塞
    投递(上游同款)。时钟可注入(``clock`` 返回 epoch 秒;各方法 ``now``
    参数可显式覆盖,管线侧统一用注入时钟取值)。
    """

    def __init__(self, data_root: str | Path, *, clock: Callable[[], float] | None = None) -> None:
        self._lock = threading.RLock()
        self._clock = clock or time.time
        self._path = Path(data_root) / RETRY_LEDGER_FILENAME
        self._entries: dict[str, dict[str, Any]] = {}
        try:
            raw = json.loads(self._path.read_text(encoding="utf-8-sig"))
        except (OSError, ValueError) as exc:
            if self._path.exists():
                logger.warning("重试账本读取失败,按空态处理: path=%s error=%s", self._path, exc)
            return
        container = raw.get("entries") if isinstance(raw, dict) else None
        if not isinstance(container, Mapping):
            return
        for key, value in container.items():
            record = self._sanitize(str(key), value)
            if record is not None:
                self._entries[record["entry_id"]] = record

    @staticmethod
    def _sanitize(entry_id: str, value: Any) -> dict[str, Any] | None:
        """只留形态良好的条目(上游同款防御:坏条目丢弃,不连坐整账)。"""
        if not isinstance(value, Mapping) or not isinstance(value.get("channel"), str):
            return None
        if not isinstance(value.get("items"), list) or not value["items"]:
            return None
        state = value.get("state")
        if state not in _KNOWN_STATES:
            state = "pending"  # 未知状态按待重投处理(at-least-once 偏置)
        spec = value.get("target_spec")
        try:
            attempts = max(0, int(value.get("attempts") or 0))
        except (TypeError, ValueError):
            attempts = 0
        return {
            "entry_id": entry_id,
            "channel": value["channel"],
            "items": list(value["items"]),
            "target_spec": spec if isinstance(spec, str) and spec else None,
            "dedup_key": _dedup_key_of(value["items"]),
            "state": state,
            "attempts": attempts,
            "created_at": _float_or_none(value.get("created_at")) or 0.0,
            "updated_at": _float_or_none(value.get("updated_at")) or 0.0,
            "next_retry_at": _float_or_none(value.get("next_retry_at")),
            "last_error": str(value.get("last_error") or "")[:500],
        }

    @property
    def path(self) -> Path:
        return self._path

    # ------------------------------------------------------------------ internals

    def _now(self, now: float | None) -> float:
        return float(now) if now is not None else float(self._clock())

    def _flush_locked(self) -> None:
        """原子写(tmp+rename);失败保内存态(best-effort,绝不抛给投递链)。"""
        try:
            self._path.parent.mkdir(parents=True, exist_ok=True)
            tmp = self._path.with_suffix(self._path.suffix + ".tmp")
            payload = {"version": 1, "entries": self._entries}
            tmp.write_text(json.dumps(payload, ensure_ascii=False, indent=1, default=str), encoding="utf-8")
            tmp.replace(self._path)
        except OSError as exc:
            logger.warning("重试账本写入失败(继续内存态): path=%s error=%s", self._path, exc)

    def _sweep_locked(self, now: float) -> bool:
        """过期清理(蓝本 sweep 的 MYIA 形态):超预算/超龄 → abandoned;
        abandoned 记录过观察窗 → 删除。只在本锁内调用;返回是否发生变更
        (无认领也要把 sweep 结果落盘,否则下轮重读会回退)。"""
        mutated = False
        for entry_id, record in list(self._entries.items()):
            if record["state"] == "abandoned":
                if now - record["updated_at"] > STALE_AFTER_SECONDS:
                    del self._entries[entry_id]  # 观察窗已过,弃置记录清退
                    mutated = True
                continue
            reason = ""
            if record["attempts"] >= MAX_ATTEMPTS:
                reason = f"{MAX_ATTEMPTS} 次重投耗尽"
            elif now - record["created_at"] > STALE_AFTER_SECONDS:
                reason = "24h 过期"
            if reason:
                record["state"] = "abandoned"
                record["updated_at"] = now
                record["last_error"] = f"{record['last_error']}（{reason}弃置）".strip()
                mutated = True
                logger.warning(
                    "投递重试条目弃置(%s): id=%s channel=%s attempts=%s",
                    reason, entry_id, record["channel"], record["attempts"],
                )
        return mutated

    @staticmethod
    def _as_entry(record: Mapping[str, Any]) -> RetryEntry:
        return RetryEntry(
            entry_id=str(record["entry_id"]),
            channel=str(record["channel"]),
            items=[dict(item) if isinstance(item, Mapping) else {"value": item} for item in record["items"]],
            target_spec=record.get("target_spec"),
            dedup_key=record.get("dedup_key"),
            state=str(record["state"]),
            attempts=int(record["attempts"]),
            created_at=float(record["created_at"]),
            updated_at=float(record["updated_at"]),
            next_retry_at=record.get("next_retry_at"),
            last_error=str(record.get("last_error") or ""),
        )

    # -------------------------------------------------------------------- public

    def enqueue_failure(
        self,
        *,
        channel: str,
        items: Sequence[Any],
        error: BaseException | str,
        kind: str,
        target_spec: str | None = None,
        now: float | None = None,
    ) -> bool:
        """一次 immediate 发送失败入队;返回是否**新建**了条目。

        门槛(模块 docstring 决策 3):非 immediate(digest 有留池)/死信
        (``classify_dead_error`` 有值)/配置级错误码一律不入队返回 False。
        同 id 活跃条目已存在时不重置预算(重复失败按同一走向耗尽,不为
        反复失败续命),只刷新 last_error;abandoned 记录在册则重开新预算
        (隔轮复发视为新一轮故障,24h 时效仍兜底)。
        """
        ts = self._now(now)
        if kind != "immediate":
            return False
        if classify_dead_error(error) is not None:
            return False  # 死信不入队:对象确认不可达,重投无意义(死信账本接管)
        if is_config_send_error(error):
            return False  # 配置级错误:修配置才是出路,重试无解
        if not items:
            return False
        views = [item_view(item) for item in items]
        entry_id = _entry_id(channel, target_spec, views)
        record: dict[str, Any] = {
            "entry_id": entry_id,
            "channel": str(channel),
            "items": views,
            "target_spec": target_spec,
            "dedup_key": _dedup_key_of(views),
            "state": "pending",
            "attempts": 0,
            "created_at": ts,
            "updated_at": ts,
            "next_retry_at": ts + RETRY_BACKOFF_SECONDS[0],
            "last_error": str(error)[:200],
        }
        with self._lock:
            existing = self._entries.get(entry_id)
            if existing is not None and existing["state"] in _ACTIVE_STATES:
                existing["last_error"] = record["last_error"]
                existing["updated_at"] = ts
                self._flush_locked()
                return False
            self._entries[entry_id] = record
            self._sweep_locked(ts)
            self._flush_locked()
        logger.info(
            "投递重试入队(at-least-once): id=%s channel=%s spec=%s 重投时刻=%s error=%s",
            entry_id, channel, target_spec or "—", record["next_retry_at"], record["last_error"],
        )
        return True

    def claim_due(
        self, *, channel: str | None = None, now: float | None = None
    ) -> list[RetryEntry]:
        """认领到期条目(重投前调用):``pending`` 且过 ``next_retry_at``,或
        ``attempting``(上一进程崩在重投途中——即刻再认领,可能重复,蓝本
        boot-sweep 同款);认领即 ``attempts += 1`` 且持久化(崩溃不退款)。
        ``channel`` 过滤只认领该通道的条目(管线按 push 条目逐通道冲账)。
        认领前先做过期 sweep。"""
        ts = self._now(now)
        claimed: list[RetryEntry] = []
        with self._lock:
            mutated = self._sweep_locked(ts)
            for entry_id, record in self._entries.items():
                if record["state"] == "abandoned":
                    continue
                if channel is not None and record["channel"] != channel:
                    continue
                if record["attempts"] >= MAX_ATTEMPTS:
                    continue  # sweep 刚清过的兜底(不新增认领)
                if record["state"] == "pending":
                    due_at = record.get("next_retry_at")
                    if due_at is None or due_at > ts:
                        continue
                # attempting(崩溃残留)直接再认领
                record["state"] = "attempting"
                record["attempts"] += 1
                record["updated_at"] = ts
                record["next_retry_at"] = None
                claimed.append(self._as_entry(record))
            if claimed or mutated:
                self._flush_locked()
        if claimed:
            logger.info(
                "投递重试认领: count=%d channel=%s ids=%s",
                len(claimed), channel or "—", [entry.entry_id for entry in claimed],
            )
        return claimed

    def mark_delivered(self, entry_id: str, *, now: float | None = None) -> bool:
        """重投成功出队(条目移除;蓝本 delivered → prune 的 JSON 等价)。"""
        ts = self._now(now)
        with self._lock:
            record = self._entries.get(entry_id)
            if record is None or record["state"] not in _ACTIVE_STATES:
                return False
            del self._entries[entry_id]
            self._flush_locked()
        logger.info("投递重试成功出队: id=%s attempts=%s", entry_id, record["attempts"])
        return True

    def mark_failed(self, entry_id: str, error: BaseException | str, *, now: float | None = None) -> bool:
        """重投失败结转:按已花次数排下一档退避;耗尽预算 → abandoned。

        退避对齐蓝本 ``retry_not_before``:第 1 次失败后 +30s、第 2 次后
        +120s、第 3 次(最后一击)不设等待——立即到期,交给下一轮 run 的
        flush(run 间隔天然兜底)。"""
        ts = self._now(now)
        with self._lock:
            record = self._entries.get(entry_id)
            if record is None or record["state"] not in _ACTIVE_STATES:
                return False
            record["last_error"] = str(error)[:200]
            record["updated_at"] = ts
            if record["attempts"] >= MAX_ATTEMPTS:
                record["state"] = "abandoned"
                record["last_error"] = f"{record['last_error']}（{MAX_ATTEMPTS} 次重投耗尽弃置）"
                logger.warning(
                    "投递重试耗尽弃置: id=%s channel=%s attempts=%s", entry_id, record["channel"], record["attempts"]
                )
            else:
                record["state"] = "pending"
                if record["attempts"] >= MAX_ATTEMPTS - 1:
                    # 最后一击:立即到期,留给下一轮 run 的 flush(蓝本语义)。
                    record["next_retry_at"] = ts
                    logger.info(
                        "投递重试进入最后一击(下一轮 flush 即认领): id=%s attempts=%s", entry_id, record["attempts"]
                    )
                else:
                    record["next_retry_at"] = ts + RETRY_BACKOFF_SECONDS[record["attempts"]]
                    logger.info(
                        "投递重试退避再排: id=%s attempts=%s 重投时刻=%s",
                        entry_id, record["attempts"], record["next_retry_at"],
                    )
            self._flush_locked()
        return True

    def abandon(self, entry_id: str, reason: str, *, now: float | None = None) -> bool:
        """终态放弃(不死信、不重试的结局,如重投被死信/未解析终态跳过)。"""
        ts = self._now(now)
        with self._lock:
            record = self._entries.get(entry_id)
            if record is None or record["state"] not in _ACTIVE_STATES:
                return False
            record["state"] = "abandoned"
            record["updated_at"] = ts
            record["last_error"] = f"{record['last_error']}（{reason}）".strip()
            self._flush_locked()
        logger.warning("投递重试终态放弃: id=%s reason=%s", entry_id, reason)
        return True

    def pending_count(self, *, channel: str | None = None) -> int:
        """活跃条目数(pending+attempting;测试/UI 可见性)。"""
        with self._lock:
            return sum(
                1
                for record in self._entries.values()
                if record["state"] in _ACTIVE_STATES and (channel is None or record["channel"] == channel)
            )

    def snapshot(self) -> list[RetryEntry]:
        """全部条目快照(含 abandoned 观察窗记录;测试/UI 可见性)。"""
        with self._lock:
            return [self._as_entry(record) for record in self._entries.values()]
