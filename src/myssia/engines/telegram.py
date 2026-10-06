"""Telegram Bot API 窗口引擎 —— getUpdates 批量拉取,链外,凭据可选(10-06).

``engine: telegram`` 显式选择才生效(链外注册,reddit/urlwatch/prompt 判例):
``ENGINE_REGISTRY`` 在册、``AUTO_CHAIN`` 不在,auto 永不路过;显式选择 =
单级链,失败/空态都是源级结构化结果,品类内其余源不受影响(铁律)。

通道形态(阶段一 bot 线,PRD 10-06-telegram-telethon;httpx 直调零依赖,
**不引 PTB/aiogram** —— 调研 §1:python-telegram-bot 29.5k★ 只借其分层思
想,MYIA 手搓同 Hermes 网关手法):

1. GET ``https://api.telegram.org/bot<token>/getUpdates?limit=N&timeout=0``
   (不带 offset = 未确认窗口从头拉;批量档不做长轮询 —— 25s 挂起属 serve
   档(``myssia telegram serve``,另文件)的常驻语义);
2. 客户端按 ``engine_options.telegram.chat_id`` 过滤(serve 级单 bot 多群
   各配一源,更新流按群分拣),消息文本 = 条目,锚点幂等见下;
3. 成功解析后跟一发**确认请求**(``offset=<max_update_id>+1``,best-effort):
   服务器据此丢弃 ≤ max 的已处理更新,窗口不随时间滚雪球;确认失败只告警
   —— 锚点去重兜底正确性,下一轮重拉被管线拦掉。⚠ 多群共用同一 bot 时
   确认是**全 bot 语义**(A 群源的确认会把 B 群未处理更新一并丢弃)——
   单 bot 单群(Grill Q2:首批仅 mihomo_party_group)或全部走 serve 档
   (offset 持久 + 逐条分拣)即可规避,扩群时再议。

**锚点幂等**(prompt ``#prompt-`` 判例):条目 URL = ``<源url>#tg-<chat_id>-
<message_id>`` —— 消息 id 群内单调递增,锚全期唯一,品类 ``dedup.key:
{url}`` 同条消息只进一次(编辑消息重投同 id → 同锚 → 天然吞掉;锚不改变
落点)。**媒体组聚合**:同 ``media_group_id`` 的多条消息(相册/多图)聚合
为一条 —— 取组内首条有 text/caption 的消息铸锚,纯媒体无文本整组跳过
(零文本无可筛面)。

**凭据三态**(reddit 判例,核心决议:凭据可选,绝不拦核心):

- **未配置**(``bot_token`` 引用缺)→ 结构化 ``credential_missing`` 显式
  空态:零请求、:attr:`last_skip_reason` 置位、日志人话指引(主人四步:
  BotFather 建 bot → ``/setprivacy`` 关隐私模式 → ``myssia secret set
  myia/telegram/bot-token`` → 拉进目标群);
- **引用在而解析失败**(钥匙串键未写等)→ 同空态 + warning 留痕;
- **解析成功** → 正常拉取。token 坏(401)→ 结构化 ``http_401``(不重试
  无意义值,提示 token 失效/被 revoke)。

**凭据零外显**(saas/reddit 同款纪律):token 走 URL path
(``/bot<token>/getUpdates``)—— 一切落日志/错误消息的 URL 一律过
:func:`mask_bot_url`(``/bot***/``);httpx 异常 str 自带完整 URL,包装
FetchError 前先净化(错误分类不净化,消息净化)。

robots 论证(reddit 同口径):api.telegram.org 的 robots 面对授权 Bot API
通道无意义 —— 合规面在 Bot API 条款(bot token 即授权凭证),引擎只保留
通用礼貌(限速 + 重试退避),不经 ``_ensure_robots_allowed``;该豁免只属
本模块钉死的官方端点常量。

其余边界:单轮窗口语义(``lookback_limit`` 1-100 缺省 100,getUpdates 硬
顶;无翻页 —— 长轮询/offset 持久是 serve 档的形态);409 冲突(serve 档
同 bot 在线长轮询互斥)→ 结构化 ``telegram_conflict`` 带指引;代理骑共
享 HTTP 栈(direct/pool 语义原样)。

Raises:
    FetchError: engine_options 形状错 / 源 URL 不符契约、getUpdates HTTP
        失败(消息净化)、响应形状不符、pagination 配置(单轮窗口语义拒)。
"""

from __future__ import annotations

import logging
import re
from datetime import datetime, timezone
from typing import Any
from urllib.parse import urlencode, urlsplit

import httpx

from myssia.engines.fetch_base import (
    BaseEngine,
    FetchContext,
    FetchError,
    classify_exception,
)
from myssia.schema import CredentialResolveError, SourceConfig, resolve_credential

logger = logging.getLogger(__name__)

#: 引擎名(schema ``EngineName`` 词表一员;链外源引擎,不进 AUTO_CHAIN)。
LAYER = "OFFICIAL_BOT_API"

#: Bot API 宿主(源 URL 必须精确匹配;端点由引擎构造,token 在 path)。
API_HOST = "api.telegram.org"

#: Bot API 端点 scheme(源 URL 契约与请求构造共用)。
API_ORIGIN = "https://api.telegram.org"

#: 钥匙串缺省键(与 PRD/示范件一致;``myssia secret set`` 的落点)。
DEFAULT_TOKEN_KEY = "keychain:myia/telegram/bot-token"

#: 单轮窗口帽(getUpdates limit 硬顶 100;缺省即顶 —— 群消息窗口宁可多拉
#: 靠锚点去重,不可漏)。
DEFAULT_LOOKBACK_LIMIT = 100
MAX_LOOKBACK_LIMIT = 100

#: 条目标题截断(消息文本可 4096 字,标题面给列表/日报用,全文在 content)。
TITLE_SNIPPET_CHARS = 100

#: token path 段的净化形态(URL 日志/错误消息统一过这个)。
_MASKED_TOKEN_PATH = "/bot***/"

#: ``/bot<token>/`` 路径段的捕获(净化用;token 形如 ``<数字>:<字母数字_-]>``,
#: 含冒号 —— 官方 token 语法,非 URL scheme 段)。
_TOKEN_PATH_RE = re.compile(r"/bot[A-Za-z0-9:_-]+/")

#: 纯文本消息之外可作 content 的字段(媒体组判例:文本缺失取 caption)。
_TEXT_FIELDS = ("text", "caption")

__all__ = [
    "API_HOST",
    "API_ORIGIN",
    "DEFAULT_LOOKBACK_LIMIT",
    "DEFAULT_TOKEN_KEY",
    "LAYER",
    "MAX_LOOKBACK_LIMIT",
    "TITLE_SNIPPET_CHARS",
    "TelegramEngine",
    "mask_bot_url",
]


def mask_bot_url(url: str) -> str:
    """把 URL 里的 ``/bot<token>/`` 段净化为 ``/bot***/``(凭据零外显)."""
    return _TOKEN_PATH_RE.sub("/bot***/", url)


def _mask_text(value: Any) -> str:
    """异常/消息文本净化:字符串里的 bot token path 段一律打码."""
    if not isinstance(value, str):
        return str(value)
    return _TOKEN_PATH_RE.sub("/bot***/", value)


def message_text(message: dict[str, Any]) -> str | None:
    """消息可筛文本:text 优先、caption 兜底(媒体组判例),双缺 = None."""
    for field in _TEXT_FIELDS:
        value = message.get(field)
        if isinstance(value, str) and value.strip():
            return value
    return None


class TelegramEngine(BaseEngine):
    """Telegram Bot API 群消息窗口源(显式 ``engine: telegram``;凭据可选).

    内置 Telegram updates 形状解析,``extract`` 节必是错配(配置即结构化
    拒);单轮窗口语义,``pagination`` 节同理拒;items 出口对齐
    ``Item.from_extracted`` 契约:url(#tg- 锚,管线去重键)/title(文本截
    断)/content(全文),其余观测键(published/author/chat_id/…)进
    metadata。
    """

    LAYER = "OFFICIAL_BOT_API"
    ENGINE_NAME = "telegram"
    REQUIRES_EXTRACT = False
    SUPPORTED_EXTRACT_TYPES = ()

    # -------------------------------------------------------------- options

    def _options(self) -> dict[str, Any]:
        """engine_options.telegram 校验与缺省化(错型即结构化拒)."""
        options = self.engine_options()
        chat_id = options.get("chat_id")
        if isinstance(chat_id, bool) or not isinstance(chat_id, (str, int)):
            raise FetchError(
                "engine_options.telegram.chat_id 应为群/频道数字 id(字符串或"
                f"整数,超级群形如 -100xxxx),当前为 {chat_id!r}",
                error_type="invalid_engine_options",
            )
        lookback = options.get("lookback_limit", DEFAULT_LOOKBACK_LIMIT)
        if (
            isinstance(lookback, bool)
            or not isinstance(lookback, int)
            or not 1 <= lookback <= MAX_LOOKBACK_LIMIT
        ):
            raise FetchError(
                f"engine_options.telegram.lookback_limit 应为 "
                f"1-{MAX_LOOKBACK_LIMIT} 整数(getUpdates 硬顶),当前为 {lookback!r}",
                error_type="invalid_engine_options",
            )
        bot_token = options.get("bot_token", DEFAULT_TOKEN_KEY)
        if not isinstance(bot_token, str) or not bot_token.strip():
            raise FetchError(
                "engine_options.telegram.bot_token 应为 env:/keychain: 凭据引用"
                f"(缺省 {DEFAULT_TOKEN_KEY}),当前为 {bot_token!r}",
                error_type="invalid_engine_options",
            )
        return {
            "chat_id": str(chat_id).strip(),
            "lookback_limit": lookback,
            "bot_token": bot_token.strip(),
        }

    # ------------------------------------------------------- url & credentials

    def _parse_source_url(self) -> None:
        """源 URL 契约校验(零 I/O):``https://api.telegram.org`` 锚形态.

        源 URL 只是引擎锚(铸 #tg- 去重键 + 排障定位);请求端点由引擎全权
        构造,host 必须精确匹配 —— 把引擎指到别站只会换来误导性错误。
        """
        parsed = urlsplit(self.source.url)
        host = (parsed.hostname or "").lower()
        if parsed.scheme != "https" or host != API_HOST or parsed.path not in ("", "/"):
            raise FetchError(
                f"telegram 引擎源 url 应为 https://{API_HOST} 锚形态"
                f"(路径留空;chat 配置在 engine_options.telegram.chat_id),"
                f"当前为 {self.source.url!r}",
                error_type="invalid_telegram_source_url",
            )

    def _bot_token(self) -> str | None:
        """解析 bot token 三态(见模块文档;None = 显式空态,由调用方落 skip)."""
        options = self._options()
        ref = options["bot_token"]
        try:
            token = resolve_credential(ref, backend=self.context.keychain_backend)
        except CredentialResolveError as exc:
            # 引用在而钥匙串未写/解析坏:空态 + warning 留痕(reddit 同口径)。
            logger.warning(
                "telegram 凭据引用解析失败,源降级为显式空态 source=%s ref=%s: %s",
                self.source.name,
                ref,
                exc,
            )
            return None
        if not token.strip() or token.strip() in {"token", "changeme"}:
            # 占位值视同未配置:零请求显式空态,不拿坏 token 去撞端点。
            logger.warning(
                "telegram bot token 引用 %s 解析为占位值,源降级为显式空态 source=%s",
                ref,
                self.source.name,
            )
            return None
        return token.strip()

    # ----------------------------------------------------------------- fetch

    async def _fetch_impl(self) -> list[dict]:
        self._parse_source_url()
        options = self._options()
        token = self._bot_token()
        if token is None:
            self.last_skip_reason = "credential_missing"
            logger.info(
                "telegram 引擎未配凭据,显式空态 source=%s(本轮零请求;"
                "主人四步:BotFather 建 bot → /setprivacy 关隐私模式(否则看不到"
                "普通消息)→ myssia secret set myia/telegram/bot-token → 拉进目标群;"
                "chat_id=%s)",
                self.source.name,
                options["chat_id"],
            )
            return []
        payload = await self._fetch_updates(token, options["lookback_limit"])
        updates = self._extract_updates(payload)
        items = self._updates_to_items(updates, options["chat_id"])
        await self._confirm_updates(token, updates)
        logger.info(
            "telegram 窗口取得 source=%s chat_id=%s updates=%s items=%s",
            self.source.name,
            options["chat_id"],
            len(updates),
            len(items),
        )
        return items

    async def _fetch_updates(self, token: str, lookback_limit: int) -> dict[str, Any]:
        """GET getUpdates(未确认窗口,零长轮询;限速 + 重试 + 消息净化).

        Raises:
            FetchError: ``http_4xx``(401 = token 失效 / 409 = serve 档冲突)、
                网络类(transport 净化)、``telegram_payload_malformed``。
        """
        query = urlencode(
            {
                "limit": lookback_limit,
                "timeout": 0,
                "allowed_updates": '["message"]',
            }
        )
        url = f"{API_ORIGIN}/bot{token}/getUpdates?{query}"
        await self._acquire_rate_limit(API_ORIGIN)
        try:
            response = await self._send_with_retry(
                "GET", url, headers={**self._headers}, log_url=mask_bot_url(url)
            )
        except httpx.HTTPStatusError as exc:
            status = exc.response.status_code
            if status == 401:
                hint = "(bot token 被拒:常见于 token 失效/revoke,重新找 BotFather 取)"
            elif status == 409:
                hint = (
                    "(getUpdates 冲突:同 token 的常驻宿主(myssia telegram serve"
                    "/webhook)在跑,批量档与其互斥 —— 常驻开着就不必排程采集)"
                )
            else:
                hint = ""
            raise FetchError(
                f"telegram getUpdates HTTP {status} endpoint={mask_bot_url(url)}"
                f": {exc.response.reason_phrase}{hint}",
                error_type=f"http_{status}",
            ) from exc
        except httpx.TransportError as exc:
            raise FetchError(
                f"telegram getUpdates 网络失败 endpoint={_MASKED_TOKEN_PATH}getUpdates: "
                f"{_mask_text(str(exc))}",
                error_type=classify_exception(exc),
            ) from self._wrap_proxy_transport_failure(exc)
        try:
            payload = response.json()
        except ValueError as exc:
            raise FetchError(
                f"telegram getUpdates 响应不是有效 JSON endpoint="
                f"{_MASKED_TOKEN_PATH}getUpdates: {exc}",
                error_type="json_decode",
            ) from exc
        if not isinstance(payload, dict) or not isinstance(payload.get("ok"), bool):
            raise FetchError(
                "telegram getUpdates 响应缺 ok 字段或形状不符(端点应答非 Bot API "
                "契约形态)",
                error_type="telegram_payload_malformed",
            )
        if not payload["ok"]:
            # Bot API 错误应答:{"ok": false, "error_code": …, "description": …}
            error_code = payload.get("error_code")
            description = _mask_text(payload.get("description"))
            raise FetchError(
                f"telegram getUpdates 应答错误 error_code={error_code}: {description}"
                "(401 = token 失效;409 = 常驻宿主冲突)",
                error_type=f"telegram_api_{error_code if isinstance(error_code, int) else 'error'}",
            )
        if not isinstance(payload.get("result"), list):
            raise FetchError(
                "telegram getUpdates 响应缺 result 数组",
                error_type="telegram_payload_malformed",
            )
        return payload

    def _extract_updates(self, payload: dict[str, Any]) -> list[dict[str, Any]]:
        """result 数组 → message/edited_message 更新(其余类型跳过)."""
        updates: list[dict[str, Any]] = []
        for update in payload["result"]:
            if not isinstance(update, dict):
                continue
            for kind in ("message", "edited_message"):
                message = update.get(kind)
                if isinstance(message, dict):
                    updates.append(update)
                    break
        return updates

    async def _confirm_updates(
        self, token: str, updates: list[dict[str, Any]]
    ) -> None:
        """确认请求(offset=max+1;best-effort:失败只告警,锚点去重兜底)."""
        if not updates:
            return
        max_update_id = max(
            update.get("update_id", 0) for update in updates if isinstance(update, dict)
        )
        if not isinstance(max_update_id, int) or max_update_id <= 0:
            return
        url = (
            f"{API_ORIGIN}/bot{token}/getUpdates"
            f"?{urlencode({'offset': max_update_id + 1, 'limit': 1, 'timeout': 0})}"
        )
        await self._acquire_rate_limit(API_ORIGIN)
        try:
            await self._send_with_retry(
                "GET", url, headers={**self._headers}, log_url=mask_bot_url(url)
            )
        except Exception as exc:  # noqa: BLE001 - 确认是窗口卫生动作,失败不废源
            logger.warning(
                "telegram 窗口确认失败(忽略;锚点去重兜底正确性) source=%s: %s",
                self.source.name,
                _mask_text(str(exc)),
            )

    # --------------------------------------------------------------- mapping

    def _updates_to_items(
        self, updates: list[dict[str, Any]], chat_id: str
    ) -> list[dict]:
        """更新流 → 管线 items(群分拣/媒体组聚合/#tg- 锚;逐条目宽容)."""
        # 群分拣:只留目标 chat 的消息(单 bot 多群 = 每群一源,各配 chat_id)。
        messages: list[dict[str, Any]] = []
        for update in updates:
            message = update.get("message") or update.get("edited_message")
            if not isinstance(message, dict):
                continue
            chat = message.get("chat")
            if not isinstance(chat, dict) or str(chat.get("id", "")) != chat_id:
                continue
            messages.append(message)
        # 媒体组聚合:同 media_group_id 取首条有文本的铸锚,整组出一条。
        seen_groups: set[str] = set()
        items: list[dict] = []
        for message in messages:
            media_group_id = message.get("media_group_id")
            text = message_text(message)
            if isinstance(media_group_id, str) and media_group_id:
                if media_group_id in seen_groups:
                    continue  # 组内后续消息(纯图/重复 caption)并入首条
                if text is None:
                    continue  # 组首无文本:不锁组,组内后续带文本的仍有机会
                seen_groups.add(media_group_id)
            if text is None:
                continue  # 无文本无 caption 的单发消息(贴纸/纯图):零可筛面,跳过
            items.append(self._message_to_item(message, text))
        return items

    def _message_to_item(self, message: dict[str, Any], text: str) -> dict[str, Any]:
        """一条消息 → 管线条目(#tg- 锚 + 观测键;Item.from_extracted 契约)."""
        chat = message.get("chat") if isinstance(message.get("chat"), dict) else {}
        message_id = message.get("message_id")
        item: dict[str, Any] = {
            "url": f"{self.source.url}#tg-{chat.get('id')}-{message_id}",
            "title": text[:TITLE_SNIPPET_CHARS],
            "content": text,
        }
        date = message.get("date")
        if isinstance(date, (int, float)) and not isinstance(date, bool):
            item["published"] = datetime.fromtimestamp(date, tz=timezone.utc).isoformat()
        author = self._author_label(message.get("from"))
        if author:
            item["author"] = author
        chat_title = chat.get("title")
        if isinstance(chat_title, str) and chat_title.strip():
            item["chat_title"] = chat_title.strip()
        if isinstance(message.get("media_group_id"), str):
            item["media_group_id"] = message["media_group_id"]
        return item

    @staticmethod
    def _author_label(sender: Any) -> str | None:
        """发送者可读标识:@username 优先,实名拼接兜底,双缺 = None."""
        if not isinstance(sender, dict):
            return None
        username = sender.get("username")
        if isinstance(username, str) and username.strip():
            return f"@{username.strip()}"
        parts = [
            part
            for part in (sender.get("first_name"), sender.get("last_name"))
            if isinstance(part, str) and part.strip()
        ]
        if parts:
            return " ".join(parts)
        return None

    # ------------------------------------------------------- shape overrides

    def _check_pagination_support(self) -> None:
        """单轮窗口语义:任何 pagination 配置都结构化拒(urlwatch 判例).

        窗口即 lookback_limit 帽;长轮询/offset 游标是 serve 档的常驻形态,
        翻页模板/滚动对本引擎无意义。
        """
        if self.source.pagination is not None:
            raise FetchError(
                "telegram 引擎是单轮窗口语义(lookback_limit 即窗口帽,"
                "常驻长轮询走 myssia telegram serve),不支持 pagination 配置",
                error_type="pagination_unsupported",
            )
