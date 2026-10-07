"""Telegram serve 常驻宿主 —— 长轮询/退避/事件账本(10-06-telegram-telethon B3).

「每时每刻过滤」的常驻档(design D1 双宿主):getUpdates **长轮询**
(timeout=25s 挂起,空窗也不忙轮)→ 每轮新消息过过滤管线(粗筛 → LLM 精筛,
B2 同一份)→ 高价值合并单条即时推(组合铁律)/ 普通入库(合并日报
「Telegram 群」分区承载)→ offset 持久断点续拉 → 事件账本逐条记账。

骨架照 cron serve 判例(``myssia cron serve`` / SupervisedTickerThread):

- **宿主互斥**:与批量档同 token 互斥(Telegram 409),与 cron 的 tick 文件
  锁不共用(各管各的域);
- **断线指数退避**:transport/5xx → 1s 起步翻倍,帽 :data:`BACKOFF_MAX_SECONDS`
  (300s);成功即归零重计;
- **致命错误不蒙头退避**:401(token 失效)/ 409(互斥)是配置态错误,
  退避只会推迟必然的失败 —— 结构化上抛让宿主退出给人看(重启由监督者/
  人决定),设计 D4「不静默」纪律;
- **sink 注入**:推送/入库都是注入面(``push_high_value``/``store_item``),
  CLI 装配真实通道与 store,测试装 fake —— 宿主本体零 myssia.pipeline 依赖
  (依赖方向红线:telegram 包不反向依赖管线大件)。

桌面接线(design D1 双宿主;grill Q6 桌面为主)已落(10-06 桌面接线批):
``desktop/entry.py`` 照 ``_CRON_TICKER`` 判例持本类于常驻 daemon 线程
(asyncio.run + stop Event 注入 ``should_stop``),装配与 CLI 同门
(``_assemble_telegram_host``);凭据缺失 = graceful 不启动仅留痕。sidecar
观测方法位(``telegram.serve.status`` 等)仍留待后续批实装。

telethon 用户线(B4)::meth:`TelegramServeHost.dispatch_once` 把单批分派
语义(分拣/过滤/出口/账本/F14)开放给
:class:`~myssia.telegram.telethon_line.TelethonUserHost` 逐事件消费 ——
bot 线与用户线的消息面是同一份实现(design D1「两档共用」)。
"""

from __future__ import annotations

import asyncio
import logging
from dataclasses import dataclass
from typing import Any, Awaitable, Callable, Mapping
from urllib.parse import urlencode

import httpx

from myssia.engines.telegram import (
    API_ORIGIN,
    mask_bot_url,
    mask_token_text,
    message_text,
    updates_to_items,
)
from myssia.telegram.events import TelegramEventLedger
from myssia.telegram.filter import TelegramFilterPipeline, merge_high_value
from myssia.telegram.offsets import OffsetStore

logger = logging.getLogger(__name__)

#: 长轮询挂起秒(Bot API 上限 30s,取 25s 留裕量 —— PRD 阶段一口径)。
LONG_POLL_SECONDS = 25.0

#: 长轮询请求的 httpx 超时(> 挂起窗,否则客户端先掐死服务端挂起)。
REQUEST_TIMEOUT_SECONDS = LONG_POLL_SECONDS + 10.0

#: 断线退避起步秒与帽(指数翻倍)。
BACKOFF_BASE_SECONDS = 1.0
BACKOFF_MAX_SECONDS = 300.0

#: 长轮询单轮消息帽(getUpdates limit 硬顶;serve 档每轮即清,一般到不了)。
POLL_LIMIT = 100

#: token path 段净化错误消息用(engines.telegram 同形;错误不携带凭据)。
_MASKED_ENDPOINT = f"{API_ORIGIN}/bot***/getUpdates"

__all__ = [
    "BACKOFF_BASE_SECONDS",
    "BACKOFF_MAX_SECONDS",
    "LONG_POLL_SECONDS",
    "POLL_LIMIT",
    "REQUEST_TIMEOUT_SECONDS",
    "TelegramPollError",
    "TelegramPoller",
    "TelegramServeHost",
    "TelegramSourceBinding",
]


class TelegramPollError(RuntimeError):
    """长轮询一轮的结构化失败(fatal 区分退避与上抛)."""

    def __init__(self, message: str, *, reason: str, fatal: bool = False) -> None:
        super().__init__(message)
        self.reason = reason  # transport / http_401 / http_409 / http_<n> / malformed
        self.fatal = fatal  # True = 配置态错误,退避无意义,上抛给宿主


class TelegramPoller:
    """getUpdates 长轮询面(httpx 注入;token 零外显)."""

    def __init__(
        self,
        client: httpx.AsyncClient,
        bot_token: str,
        *,
        long_poll_seconds: float = LONG_POLL_SECONDS,
        request_timeout_seconds: float = REQUEST_TIMEOUT_SECONDS,
    ) -> None:
        self._client = client
        self._token = bot_token
        self._long_poll = long_poll_seconds
        self._request_timeout = request_timeout_seconds

    async def poll(self, offset: int) -> list[dict[str, Any]]:
        """拉一轮(挂起至多 long_poll 秒);返回 result 数组(可空)."""
        query = urlencode(
            {
                "offset": offset,
                "limit": POLL_LIMIT,
                "timeout": int(self._long_poll),
                "allowed_updates": '["message", "edited_message"]',
            }
        )
        url = f"{API_ORIGIN}/bot{self._token}/getUpdates?{query}"
        try:
            response = await self._client.get(
                url, timeout=self._request_timeout
            )
        except httpx.TransportError as exc:
            # 深审 F10:httpx 异常 str 自带完整 URL(含 token path 段),拼进
            # 错误消息前过 mask_token_text(engines.telegram 同款纪律)。
            raise TelegramPollError(
                f"telegram 长轮询网络失败 endpoint={_MASKED_ENDPOINT}: "
                f"{mask_token_text(str(exc))}",
                reason="transport",
            ) from exc
        if response.status_code == 401:
            raise TelegramPollError(
                "telegram 长轮询 401:bot token 失效/被 revoke"
                "(重新找 BotFather 取,myssia secret set myia/telegram/bot-token)",
                reason="http_401",
                fatal=True,
            )
        if response.status_code == 409:
            raise TelegramPollError(
                "telegram 长轮询 409:同 token 的其他 getUpdates 消费者在跑"
                "(批量档/另一 serve/webhook)—— 同 bot 只能有一个长轮询宿主",
                reason="http_409",
                fatal=True,
            )
        if response.status_code >= 400:
            raise TelegramPollError(
                f"telegram 长轮询 HTTP {response.status_code}"
                f" endpoint={_MASKED_ENDPOINT}: {response.reason_phrase}",
                reason=f"http_{response.status_code}",
            )
        try:
            payload = response.json()
        except ValueError as exc:
            raise TelegramPollError(
                f"telegram 长轮询响应不是 JSON endpoint={_MASKED_ENDPOINT}: "
                f"{mask_token_text(str(exc))}",
                reason="malformed",
            ) from exc
        result = payload.get("result") if isinstance(payload, dict) else None
        if not isinstance(result, list) or not payload.get("ok"):
            raise TelegramPollError(
                "telegram 长轮询响应形状不符(缺 ok/result)",
                reason="malformed",
            )
        return [update for update in result if isinstance(update, dict)]

    async def aclose(self) -> None:
        """关闭所持 HTTP 客户端(深审 F14:CLI/desktop 装配的专属客户端由
        poller 持有并在宿主退出路径统一收尾;httpx aclose 幂等,二次关闭
        无害)。测试注入的 fake poller 无本方法,宿主收尾走 getattr 软探。
        """
        await self._client.aclose()


@dataclass
class TelegramSourceBinding:
    """serve 档的一个群绑定:chat_id → 源(名/锚 URL/过滤管线)."""

    chat_id: str
    source_name: str
    source_url: str
    pipeline: TelegramFilterPipeline


@dataclass
class _DispatchStats:
    """一轮分派的可观测计数(日志/账本对照)."""

    updates: int = 0
    items: int = 0
    stored: int = 0
    pushed: int = 0
    ledger_failed: int = 0


class TelegramServeHost:
    """常驻宿主:长轮询 → 过滤 → 出口(推/入库)→ offset/账本.

    Args:
        poller: 长轮询面(:class:`TelegramPoller`;测试注 fake)。
        bindings: chat_id → 绑定(一 bot 多群,每群一条目源)。
        offsets: 确认游标持久化(:class:`OffsetStore`)。
        ledger: 事件账本(:class:`TelegramEventLedger`)。
        push_high_value: 高价值合并单条的推送 sink(async;一轮至多一次)。
            返回 **bool**:True = 真实送达;False = 通道未配(深审 F14:
            虚账修正 —— 未配通道不再计 pushed、账本记 ``no_channel``,
            条目已入库由日报兜底)。
        store_item: 条目入库 sink(sync;返回 True = 新入库,False = 去重
            跳过;批量档管线 ``_stage_dedup`` 同语义由 CLI 装配)。
        sleep: 异步 sleep 注入(测试 fake 记录退避)。
        should_stop: 停止判定(注入;None = 只靠取消/致命错误)。
    """

    def __init__(
        self,
        *,
        poller: TelegramPoller,
        bindings: Mapping[str, TelegramSourceBinding],
        offsets: OffsetStore,
        ledger: TelegramEventLedger,
        push_high_value: Callable[[dict[str, Any]], Awaitable[bool]],
        store_item: Callable[[dict[str, Any]], bool],
        sleep: Callable[[float], Awaitable[None]] = asyncio.sleep,
        should_stop: Callable[[], bool] | None = None,
    ) -> None:
        self._poller = poller
        self._bindings = dict(bindings)
        self._offsets = offsets
        self._ledger = ledger
        self._push = push_high_value
        self._store = store_item
        self._sleep = sleep
        self._should_stop = should_stop
        #: 媒体组跨轮记忆(深审 F13):上一轮铸锚的 ``chat:media_group_id``
        #: 复合键 —— 跨轮保留一轮,后到的同组带 caption 成员按并入吞掉,
        #: 不再重复出条(每轮分派完滚动更新)。
        self._media_group_memory: set[str] = set()
        #: 宿主生命周期观测(CLI 横幅/doctor 消费)。
        self.rounds = 0
        self.backoff_seconds = BACKOFF_BASE_SECONDS

    # ------------------------------------------------------------------ loop

    async def run_forever(self) -> None:
        """主循环:阻塞至 should_stop/取消;致命 poll 错误上抛(Ctrl-C 干净停).

        退出路径收尾(深审 F14):poller 的 HTTP 客户端 aclose(fake poller
        无 aclose 时软探跳过;httpx aclose 幂等,与装配侧收尾双关闭无害)。
        账本连接的关闭归**装配方**(CLI finally / desktop bundle close)——
        宿主退出后观测面(host._ledger.counts 等)仍可读,资源纪律不与
        可观测性打架。
        """
        logger.info(
            "telegram serve 已启动 chats=%s long_poll=%.0fs backoff=%.0f-%.0fs",
            sorted(self._bindings),
            LONG_POLL_SECONDS,
            BACKOFF_BASE_SECONDS,
            BACKOFF_MAX_SECONDS,
        )
        try:
            while not (self._should_stop is not None and self._should_stop()):
                try:
                    updates = await self._poller.poll(self._offsets.load())
                except TelegramPollError as exc:
                    if exc.fatal:
                        logger.error("telegram serve 致命错误,宿主退出: %s", exc)
                        raise
                    self.backoff_seconds = await self._backoff(exc)
                    continue
                self.backoff_seconds = BACKOFF_BASE_SECONDS
                self.rounds += 1
                if updates:
                    await self._dispatch(updates)
                    self._persist_offset(updates)
        except asyncio.CancelledError:
            logger.info("telegram serve 收到取消,正在退出")
            raise
        finally:
            await self._shutdown_resources()
        logger.info("telegram serve 已退出 rounds=%s", self.rounds)

    async def _shutdown_resources(self) -> None:
        """宿主退出路径的资源收尾(poller 客户端;失败只留痕)."""
        poller_aclose = getattr(self._poller, "aclose", None)
        if callable(poller_aclose):
            try:
                await poller_aclose()
            except Exception:  # noqa: BLE001
                logger.warning(
                    "telegram serve poller 客户端关闭失败(忽略)", exc_info=True
                )

    async def _backoff(self, exc: TelegramPollError) -> float:
        """指数退避一步(返回下一档;帽后恒定重试 —— 常驻不放弃)."""
        delay = self.backoff_seconds
        logger.warning(
            "telegram 长轮询失败 reason=%s,%.1fs 后重试(当前退避档 %.1fs): %s",
            exc.reason,
            delay,
            delay,
            exc,
        )
        await self._sleep(delay)
        return min(delay * 2, BACKOFF_MAX_SECONDS)

    # -------------------------------------------------------------- dispatch

    async def dispatch_once(
        self,
        updates: list[dict[str, Any]],
        *,
        skip_groups: set[str] | None = None,
    ) -> set[str]:
        """单批分派的公开入口(telethon 用户线消费面,B4).

        bot 线走 :meth:`run_forever` 主循环(长轮询自驱);用户线的事件
        到达是**逐条推送**,由 :class:`~myssia.telegram.telethon_line.
        TelethonUserHost` 每事件调本方法一次 —— 分拣/过滤/出口/账本语义
        与 bot 线完全同一份(``_dispatch`` 单实现)。

        ``skip_groups``:调用方持有的额外「已铸锚媒体组」(``chat:gid``
        复合键;用户线的跨事件相册记忆 —— 分派器自身滚动记忆只保上一批,
        单条批会在无锚定成员处清空,长记忆归调用方)。返回本轮铸锚的
        ``chat:gid`` 键集(调用方滚动自己的记忆)。
        """
        return await self._dispatch(updates, extra_skip_groups=skip_groups)

    def _persist_offset(self, updates: list[dict[str, Any]]) -> None:
        max_update_id = max(
            (
                update.get("update_id")
                for update in updates
                if isinstance(update.get("update_id"), int)
            ),
            default=0,
        )
        if max_update_id > 0:
            self._offsets.save(max_update_id + 1)

    async def _dispatch(
        self,
        updates: list[dict[str, Any]],
        *,
        extra_skip_groups: set[str] | None = None,
    ) -> set[str]:
        """一轮新消息:分拣到绑定 → 过滤 → 入库/推送 → 记账.

        返回本轮铸锚的媒体组键集(``chat:gid``;B4 起 dispatch_once 消费)。
        """
        stats = _DispatchStats(updates=len(updates))
        # 本轮铸锚的媒体组(F13 跨轮记忆滚动面:分派完替换上一轮记忆)。
        anchored_now: set[str] = set()
        # 先按绑定分拣(消息面共用 engines.telegram 的分拣/聚合/锚语义)。
        buckets: dict[str, list[dict[str, Any]]] = {
            chat_id: [] for chat_id in self._bindings
        }
        for update in updates:
            update_id = update.get("update_id")
            if not isinstance(update_id, int):
                continue
            message = update.get("message") or update.get("edited_message")
            if not isinstance(message, dict):
                self._record(stats, update_id, outcome="dropped_other")
                continue
            chat = message.get("chat") if isinstance(message.get("chat"), dict) else {}
            chat_id = str(chat.get("id", ""))
            binding = self._bindings.get(chat_id)
            if binding is None:
                self._record(stats, update_id, chat_id=chat_id, outcome="dropped_chat")
                continue
            if message_text(message) is None:
                self._record(
                    stats,
                    update_id,
                    chat_id=chat_id,
                    message_id=message.get("message_id"),
                    outcome="dropped_textless",
                )
                continue
            buckets[chat_id].append(update)

        for chat_id, chat_updates in buckets.items():
            if not chat_updates:
                continue
            binding = self._bindings[chat_id]
            # 深审 F13:上一轮铸锚的媒体组前缀跨轮保留一轮 —— 后到的同组
            # 成员(相册被长轮询分批切开)按并入吞掉,不再重复出条。
            # B4:extra_skip_groups = 调用方(telethon 用户线)的跨事件长
            # 记忆,与自身滚动记忆并集(键同 ``chat:gid`` 复合形)。
            prefix = f"{chat_id}:"
            skip_groups = {
                key[len(prefix):]
                for key in (*self._media_group_memory, *(extra_skip_groups or ()))
                if key.startswith(prefix)
            }
            items = updates_to_items(
                chat_updates,
                chat_id,
                source_url=binding.source_url,
                skip_groups=skip_groups,
            )
            stats.items += len(items)
            anchored_now.update(
                f"{chat_id}:{item['media_group_id']}"
                for item in items
                if isinstance(item, dict)
                and isinstance(item.get("media_group_id"), str)
            )
            # update_id ↔ message_id 映射(条目级记账回填主键面)。
            update_id_by_mid: dict[int, int] = {}
            for update in chat_updates:
                message = update.get("message") or update.get("edited_message")
                mid = message.get("message_id") if isinstance(message, dict) else None
                if isinstance(mid, int) and isinstance(update.get("update_id"), int):
                    update_id_by_mid[mid] = update["update_id"]
            # 账本口径:未产出条目的更新(媒体组并入/文本缺失经聚合口)按
            # dropped_textless 记;产出条目的记账跟随条目(见下)。
            produced_ids = {
                item.get("message_id") for item in items if isinstance(item, dict)
            }
            for update in chat_updates:
                message = update.get("message") or update.get("edited_message")
                mid = message.get("message_id") if isinstance(message, dict) else None
                if mid not in produced_ids:
                    self._record(
                        stats,
                        update.get("update_id"),
                        chat_id=chat_id,
                        message_id=mid,
                        outcome="dropped_textless",
                    )
            await self._filter_and_emit(binding, items, update_id_by_mid, stats)
        # F13 跨轮记忆滚动:只保留本轮铸锚的组(上一轮记忆本轮已消费即弃)。
        self._media_group_memory = anchored_now
        logger.info(
            "telegram serve 分派完成 updates=%s items=%s stored=%s pushed=%s"
            " ledger_failed=%s",
            stats.updates,
            stats.items,
            stats.stored,
            stats.pushed,
            stats.ledger_failed,
        )
        return anchored_now

    async def _filter_and_emit(
        self,
        binding: TelegramSourceBinding,
        items: list[dict[str, Any]],
        update_id_by_mid: Mapping[int, int],
        stats: _DispatchStats,
    ) -> None:
        """一组条目:过滤管线 → 普通入库/高价值合并推送(B2 同一份语义)."""
        for item in items:
            item["source"] = binding.source_name  # 日报分区匹配键(源名锚)
        try:
            outcome = await binding.pipeline.process(items)
        except Exception as exc:  # noqa: BLE001 - 过滤面炸不带走循环:全量入库降级
            logger.error(
                "telegram serve 过滤管线异常(本轮按入库降级) source=%s: %s",
                binding.source_name,
                exc,
                exc_info=True,
            )
            outcome = None
        if outcome is None:
            for item in items:
                if self._safe_store(item):
                    stats.stored += 1
                self._record_for_item(
                    stats, item, update_id_by_mid, outcome="error", detail="filter_failed"
                )
            return
        # 粗筛未命中的条目:管线内零痕迹跳过,账本按 update_id 回记来过。
        survived = {
            self._item_key(item) for item in (*outcome.normal, *outcome.high_value)
        }
        for item in items:
            if self._item_key(item) not in survived:
                self._record_for_item(
                    stats, item, update_id_by_mid, outcome="dropped_coarse"
                )
        for item in outcome.normal:
            if self._safe_store(item):
                stats.stored += 1
            self._record_for_item(
                stats, item, update_id_by_mid, outcome="stored", score=item.get("score")
            )
        merged = (
            merge_high_value(
                outcome.high_value, threshold=binding.pipeline.config.score_threshold
            )
            if outcome.high_value
            else None
        )
        if merged is None:
            return
        # 先入库再推(管线先入库后推送同序:推失败条目已在库,日报兜底可见)。
        merged["source"] = binding.source_name
        if self._safe_store(merged):
            stats.stored += 1
        first = outcome.high_value[0] if outcome.high_value else None
        try:
            pushed = bool(await self._push(merged))
        except Exception as exc:  # noqa: BLE001 - 推送失败:条目已入库,账本记 error
            logger.error(
                "telegram serve 高价值推送失败(条目已入库,日报兜底) url=%s: %s",
                merged.get("url"),
                exc,
            )
            self._record_for_item(
                stats,
                outcome.high_value[0] if outcome.high_value else merged,
                update_id_by_mid,
                outcome="error",
                detail=str(exc)[:200],
            )
            return
        if not pushed:
            # 深审 F14 虚账修正:推送 sink 返回 False = 通道未配 —— 条目已
            # 入库(日报兜底),但不再计 pushed/记 pushed 账;首条记
            # no_channel,同轮并入的其余条目按 stored(同「一轮一推」口径)。
            logger.info(
                "telegram serve 高价值条目仅入库(品类未配 push 通道) url=%s",
                merged.get("url"),
            )
            for item in outcome.high_value:
                self._record_for_item(
                    stats,
                    item,
                    update_id_by_mid,
                    outcome="no_channel" if item is first else "stored",
                    score=item.get("score"),
                )
            return
        stats.pushed += 1
        # 账本口径:同轮并入合并的条目里,首条记 pushed(一轮一推),其余 stored。
        for item in outcome.high_value:
            self._record_for_item(
                stats,
                item,
                update_id_by_mid,
                outcome="pushed" if item is first else "stored",
                score=item.get("score"),
            )

    @staticmethod
    def _item_key(item: Mapping[str, Any]) -> str:
        """条目唯一键(url 锚;过滤管线同口径)."""
        return str(item.get("url") or "")

    def _safe_store(self, item: Mapping[str, Any]) -> bool:
        """入库 sink 防炸(失败记 error,不带走循环)."""
        try:
            return bool(self._store(dict(item)))
        except Exception as exc:  # noqa: BLE001
            logger.error(
                "telegram serve 入库失败 url=%s: %s", item.get("url"), exc
            )
            return False

    # --------------------------------------------------------------- ledger

    def _record(
        self,
        stats: _DispatchStats,
        update_id: int,
        *,
        chat_id: str | None = None,
        message_id: int | None = None,
        outcome: str,
        score: int | None = None,
        detail: str | None = None,
    ) -> None:
        if not self._ledger.record(
            update_id=update_id,
            chat_id=chat_id,
            message_id=message_id,
            outcome=outcome,
            score=score,
            detail=detail,
        ):
            stats.ledger_failed += 1

    def _record_for_item(
        self,
        stats: _DispatchStats,
        item: Mapping[str, Any],
        update_id_by_mid: Mapping[int, int],
        *,
        outcome: str,
        score: Any = None,
        detail: str | None = None,
    ) -> None:
        """条目级记账:message_id → update_id 回填(锚语义与账本主键面衔接)."""
        mid = item.get("message_id")
        update_id = (
            update_id_by_mid.get(mid)
            if isinstance(mid, int)
            else None
        )
        self._record(
            stats,
            update_id=update_id if isinstance(update_id, int) else -1,
            chat_id=str(item.get("chat_id") or "") or None,
            message_id=mid if isinstance(mid, int) else None,
            outcome=outcome,
            score=score
            if isinstance(score, (int, float)) and not isinstance(score, bool)
            else None,
            detail=detail,
        )
