"""Discord 通道:Bot REST ``POST /channels/{id}/messages``(Bot token + JSON)。

蓝本归属(10-03-messaging-w3-longtail 组一):出站形态移植自 Hermes
``plugins/platforms/discord/adapter.py`` 的 ``_standalone_send``(NousResearch/
Hermes-Agent,MIT;上游路径
``~/.hermes/hermes-agent/plugins/platforms/discord/adapter.py``——文本路径
``POST https://discord.com/api/v10/channels/{id}/messages`` + ``Authorization:
Bot <token>`` + ``{"content": …}``)。MYIA 按本档语义重写,不整块复制:

- **REST 直发**:无网关 WebSocket(那是蓝本入站的另一半,MYIA 零入站);
  2xx(200/201)即成功,响应 JSON 含 ``id``(消息 snowflake)。
- **2000 硬上限**:官方 content 上限 2000 字符,蓝本
  ``MAX_MESSAGE_LENGTH = 2000`` 同值(:data:`MESSAGE_LIMIT`);长文按行边界
  拆多条(:func:`telegram.split_message` 复用,逐块顺序发送)。
- **话题定向**::class:`~myssia.push.targets.ChannelTarget.thread_id` 在场时改投
  ``/channels/{thread_id}/messages``(蓝本 thread_id 分支同形态;蓝本的论坛
  建帖分支(type 15 探测)是入站元数据依赖,MYIA 不做——出站直投普通频道/
  已存在话题)。

寻址(design D1/D4):``supports_targeting=True``;``context.target.chat_id``
优先,退回 legacy ``target`` 引用(**须显式配置,无运行期 env 缺省回退**;
推荐引用名 ``env:DISCORD_CHANNEL_ID``,蓝本同名 env 先例)。直达形态:雪花 id(17-20 位数字,
Discord snowflake 官方形态)。

目录自动发现(10-05-push-reliability-batch R4):``discover_directory`` 实装。
蓝本锚:Hermes ``gateway/channel_directory.py`` 的 ``_build_discord``(上游
174-197 行,NousResearch/Hermes-Agent,MIT)——枚举 bot 可见服务器内的
text + forum 频道。载体偏离:蓝本读 discord.py SDK 的网关缓存
(``client.guilds``,需 WebSocket 在场),MYIA 出站-only 无网关,REST 等价
两跳 = ``GET /users/@me/guilds``(``after`` 游标翻页,20 页 × 200 保底,
对位蓝本 slack 侧同款翻页护栏)→ 每服务器 ``GET /guilds/{id}/channels``
过滤 type 0(GUILD_TEXT)/15(GUILD_FORUM,发消息自动开帖,蓝本注释同义)。
forum 在 MYIA 目录语汇里落 ``type="topic"``(:data:`myssia.push.directory.
ENTRY_TYPES` 对齐 Hermes channel/dm/forum 语汇的第四槽)。两处不适用蓝本
分支:obfuscated 占位过滤(#90154 是 SDK 缓存侧问题,REST 列表本就按 bot
视野返回)与 session DM 回填(gateway 入站专属,MYIA 零入站——DM 靠别名
手工登记,feishu 私聊同款组内约定)。``ChannelEntry`` 无 guild 位:跨服务器
同名频道以雪花 id 直达消歧(蓝本 entry 的 guild 字段在此裁剪)。

错误文案保留 ``HTTP <status>`` 与原厂响应片段(Discord 错误体
``{"message": "Unknown Channel", "code": 10003}``)供死信分类:
403 → forbidden、404 → not_found、429(``retry_after`` 限频)/5xx → 瞬态;
401 是 token 级配置错(非会话级不可达),分类器不标死信、按瞬态透传
(:func:`myssia.push.delivery.classify_dead_error` 无 ``http 401`` 锚点)。

凭据安全基线同其余通道;全部 HTTP 经注入的 ``httpx.AsyncClient``。
"""

from __future__ import annotations

import asyncio
import contextlib
import logging
import re
from typing import Any, Awaitable, Callable, Mapping, Sequence

import httpx

from myssia.push.base import (
    DEFAULT_SEND_TIMEOUT_SECONDS,
    PushSendError,
    SendContext,
    TrendAwareChannel,
)
from myssia.push.directory import ChannelEntry
from myssia.push.ntfy import build_message
from myssia.push.targets import RESOLVED_DIRECT, ChannelTarget
from myssia.push.telegram import split_message
from myssia.push.templates import TemplateRenderError, TemplateRenderer
from myssia.schema import CredentialResolveError, resolve_credential

__all__ = [
    "API_BASE",
    "CHANNEL_ID_RE",
    "DEFAULT_TARGET_ENV_REF",
    "DEFAULT_TOKEN_ENV_REF",
    "DISCOVER_CHANNEL_TYPES",
    "DISCOVER_MAX_PAGES",
    "DISCOVER_PAGE_SIZE",
    "DiscordChannel",
    "GUILDS_API_URL",
    "MESSAGE_LIMIT",
]

logger = logging.getLogger(__name__)

#: Discord Bot REST 基址(v10,蓝本同版)。
API_BASE = "https://discord.com/api/v10"
#: Bot token 凭据引用缺省(蓝本同名 env ``DISCORD_BOT_TOKEN``)。
DEFAULT_TOKEN_ENV_REF = "env:DISCORD_BOT_TOKEN"
#: 接收频道 id 的推荐引用名(显式配置 ``target`` 用;运行期不自动回退)。
DEFAULT_TARGET_ENV_REF = "env:DISCORD_CHANNEL_ID"
#: content 官方硬上限 2000(蓝本同值);按字符拆,行边界优先。
MESSAGE_LIMIT = 2000
#: 直达 id 形态:Discord snowflake(17-20 位数字,官方 Twitter 雪花同源)。
CHANNEL_ID_RE = re.compile(r"^\d{16,20}$")
#: 目录发现第一跳:bot 已加入服务器列表(蓝本 ``client.guilds`` 的 REST 等价)。
GUILDS_API_URL = f"{API_BASE}/users/@me/guilds"
#: 目录发现 guild 翻页页大小(官方 limit 上限 200;取上限减少往返)。
DISCOVER_PAGE_SIZE = 200
#: 目录发现翻页保底上限(20 页 × 200 = 4000 服务器;服务端游标不收敛时防死循环,
#: 蓝本 slack ``_slack_team_channels`` 的 range(20) 护栏同款)。
DISCOVER_MAX_PAGES = 20
#: guild 频道 type → 目录 entry type 过滤表(蓝本 text+forum 枚举面同款):
#: 0 = GUILD_TEXT → "channel";15 = GUILD_FORUM → "topic"(发消息自动开帖,
#: MYIA 目录语汇第四槽;其余 type——语音/分类/公告等——蓝本未枚举,跳过)。
DISCOVER_CHANNEL_TYPES: Mapping[int, str] = {0: "channel", 15: "topic"}


class DiscordChannel(TrendAwareChannel):
    """``discord`` channel:每 ≤2000 字符块一次频道消息 POST。

    Args:
        target: 频道 id 的凭据引用(``env:DISCORD_CHANNEL_ID`` style,发送期
            解析);与 ``targets`` 定向配置互斥可省,此时频道由
            ``context.target`` 给出。
        template: 可选用户模板(Jinja2);在场时渲染输出为整条消息文本;
            省略 → 内置纯文本版式(ntfy ``build_message`` 同款复用)。
        token: 预解析 bot token(构造注入,测试用);省略 → 发送期从
            :data:`DEFAULT_TOKEN_ENV_REF` 解析。
        renderer: 模板渲染器;缺省共享沙箱实例。
        client: 注入用 ``httpx.AsyncClient``(测试 mock 点);省略则每次
            发送自建带 ``timeout`` 的 client。
        timeout: 自管 client 的发送超时秒数。

    Raises:
        PushSendError: 凭据解析失败、HTTP 传输失败、非 JSON 响应、
            非 2xx(原厂 ``message``/``code`` 进文案),或模板渲染失败。
    """

    name = "discord"
    #: 目录寻址已开(context.target 优先,legacy target 兜底);协议判定见
    #: base.Channel docstring。
    supports_targeting = True
    #: 目录发现 429 退避兜底秒数(响应体带 retry_after 时以其为准;测试钉 0)。
    discover_backoff_seconds = 1.0
    #: 退避 sleeper 注入点(测试记录时长 + 免真睡;缺省 asyncio.sleep)。
    discover_sleeper: Callable[[float], Awaitable[None]] = asyncio.sleep

    def __init__(
        self,
        *,
        target: str | None = None,
        template: str | None = None,
        token: str | None = None,
        renderer: TemplateRenderer | None = None,
        client: httpx.AsyncClient | None = None,
        timeout: float = DEFAULT_SEND_TIMEOUT_SECONDS,
    ) -> None:
        self._target = target
        self._template = template
        self._token = token
        self._renderer = renderer or TemplateRenderer()
        self._client = client
        self._timeout = timeout

    async def send(self, items: Sequence[Any], context: SendContext) -> None:
        """Render + 逐块 POST;定向优先(``context.target.chat_id``/``thread_id``)。

        Raises:
            PushSendError: on any credential/transport/API failure (callers
                isolate per channel; nothing is raised on success). 块序发送,
                中途失败整通道报错(telegram 同款取舍)。
        """
        token = self._resolve_token()
        channel, thread_id = self._resolve_channel(context)
        # thread_id 在场 = 话题内投递(蓝本 thread_id 分支:改投话题端点)。
        endpoint_id = thread_id or channel
        for text in split_message(self._compose(items, context), limit=MESSAGE_LIMIT):
            await self._post_message(token, endpoint_id, text)
        logger.debug(
            "discord 发送完成: slot=%s kind=%s count=%d channel_ref=%s",
            context.slot,
            context.kind,
            len(items),
            context.target or self._target,
        )

    # ------------------------------------------------------------- compose

    def _compose(self, items: Sequence[Any], context: SendContext) -> str:
        """消息文本:用户模板优先,缺省内置纯文本版式(ntfy 同款复用)。"""
        if self._template is None:
            return build_message(items, context)
        # 契约:send 只抛 PushSendError —— 渲染失败包装为结构化的
        # template_render_error(语法错误已在加载期被 schema 拒绝)。
        try:
            return self._renderer.render(
                self._template, items, context, **self.trend_render_kwargs()
            )
        except TemplateRenderError as exc:
            raise PushSendError(
                "template_render_error", f"push[].template 渲染失败: {exc}"
            ) from exc

    # ------------------------------------------------------------ credentials

    def _resolve_token(self) -> str:
        if self._token is not None:
            return self._token
        try:
            return resolve_credential(DEFAULT_TOKEN_ENV_REF)
        except CredentialResolveError as exc:
            raise PushSendError(exc.code, f"discord bot 凭据解析失败: {exc}") from exc

    def _resolve_channel(self, context: SendContext) -> tuple[str, str | None]:
        """定向优先 → ``(channel_id, thread_id)``;两路全缺 → missing_target。"""
        if context.target is not None:
            channel = context.target.chat_id.strip()
            thread_id = (context.target.thread_id or "").strip() or None
        elif self._target is not None:
            channel = self._resolve_ref(self._target, "discord target")
            thread_id = None
        else:
            raise PushSendError(
                "missing_target",
                "discord 两条寻址路径均缺席:未配置 legacy target(频道 id 引用),"
                "本次发送也未携带 context.target",
            )
        if not CHANNEL_ID_RE.fullmatch(channel):
            # 解析值不回显(死信分类误判暴露面收敛,10-03-messaging-w3-longtail D1)。
            raise PushSendError(
                "invalid_credential_ref",
                f"discord 频道 id 形态非法(须为 17-20 位数字 snowflake):"
                f"得到 {len(channel)} 字符的值,不匹配该形态(解析值不回显)",
            )
        if thread_id is not None and not CHANNEL_ID_RE.fullmatch(thread_id):
            raise PushSendError(
                "invalid_credential_ref",
                f"discord 话题 id 形态非法(须为 17-20 位数字 snowflake):"
                f"得到 {len(thread_id)} 字符的值,不匹配该形态(解析值不回显)",
            )
        return channel, thread_id

    def _resolve_ref(self, reference: str, label: str) -> str:
        try:
            value = resolve_credential(reference).strip()
        except CredentialResolveError as exc:
            raise PushSendError(exc.code, f"{label} 解析失败: {exc}") from exc
        return value

    # ------------------------------------------------------------- send

    async def _post_message(self, token: str, channel_id: str, text: str) -> None:
        """一块正文:``POST /channels/{id}/messages``;2xx 即成功。"""
        url = f"{API_BASE}/channels/{channel_id}/messages"
        headers = {"Authorization": f"Bot {token}"}
        try:
            if self._client is not None:
                response = await self._client.post(url, headers=headers, json={"content": text})
            else:
                async with httpx.AsyncClient(timeout=self._timeout) as client:
                    response = await client.post(url, headers=headers, json={"content": text})
        except httpx.HTTPError as exc:
            raise PushSendError(
                "http_error", f"discord 请求失败: {type(exc).__name__}: {exc}"
            ) from exc
        if not response.is_success:
            # HTTP <status> + 原厂 body 片段进文案:403 → forbidden、
            # 404(Unknown Channel)→ not_found、429(限频)/5xx → 瞬态;
            # 401(token 级配置错)不标死信,按瞬态透传(模块 docstring 注记)。
            raise PushSendError(
                "discord_api_error",
                f"discord HTTP {response.status_code}: {response.text[:200]!r}",
            )
        try:
            data = response.json()
        except ValueError as exc:
            raise PushSendError(
                "invalid_response",
                f"discord 响应不是 JSON(HTTP {response.status_code}): {response.text[:200]!r}",
            ) from exc
        if not isinstance(data, dict) or not data.get("id"):
            raise PushSendError(
                "invalid_response",
                f"discord 响应缺消息 id: {str(data)[:200]!r}",
            )

    # ------------------------------------------------- 目录发现(R4)+ 直达

    async def discover_directory(self) -> list[ChannelEntry]:
        """枚举 bot 可见服务器的 text + forum 频道(目录发现,R4 实装)。

        蓝本 ``_build_discord``(channel_directory.py:174-197,MIT)的 REST
        移植:``GET /users/@me/guilds`` 翻页(after 游标,保底
        :data:`DISCOVER_MAX_PAGES` 页)→ 每服务器 ``GET /guilds/{id}/channels``
        过滤 :data:`DISCOVER_CHANNEL_TYPES`(text/forum,蓝本枚举面同款);
        跨服务器按频道雪花 id 去重。``last_seen`` 不在此填——目录合并口
        (:meth:`myssia.push.directory.ChannelDirectory.replace_platform`)
        统一盖刷新戳(feishu 同款约定)。

        Raises:
            PushSendError: 凭据缺失、HTTP 传输失败、非 JSON 响应或非 2xx
                (429 退避一次仍失败也走这里;调用方 refresh 按发现失败隔离:
                告警 + 保留旧桶)。
        """
        token = self._resolve_token()
        entries: list[ChannelEntry] = []
        seen: set[str] = set()
        after: str | None = None
        for _page_index in range(DISCOVER_MAX_PAGES):
            guilds = await self._fetch_guilds_page(token, after)
            for raw in guilds:
                if not isinstance(raw, Mapping):
                    continue
                guild_id = str(raw.get("id") or "").strip()
                if not guild_id:
                    continue
                for channel in await self._fetch_guild_channels(token, guild_id):
                    entry = self._entry_from_channel(channel)
                    if entry is not None and entry.chat_id not in seen:
                        seen.add(entry.chat_id)
                        entries.append(entry)
            if len(guilds) < DISCOVER_PAGE_SIZE:
                return entries  # 尾页(Discord 翻页契约:不足一页即尽)
            after = str(guilds[-1].get("id") or "").strip() if isinstance(guilds[-1], Mapping) else ""
            if not after:
                # 整页却取不到游标:防御性止步(不依赖服务端守约,feishu 同款)。
                logger.warning("discord 服务器列表整页但缺 after 游标,目录发现提前止步")
                return entries
        logger.warning(
            "discord 服务器列表翻页达保底上限 %d 页,目录可能不完整(服务端游标未收敛)",
            DISCOVER_MAX_PAGES,
        )
        return entries

    @staticmethod
    def _entry_from_channel(raw: Any) -> ChannelEntry | None:
        """One guild channel → :class:`ChannelEntry`;非枚举面/形态坏 → None。

        仅 text(0)/forum(15) 进目录(蓝本枚举面);id 过雪花形态校验;
        ``name`` 缺失退回频道 id 占位(条目仍可按 id 寻址,feishu 同款)。
        """
        if not isinstance(raw, Mapping):
            return None
        channel_id = str(raw.get("id") or "").strip()
        if not CHANNEL_ID_RE.fullmatch(channel_id):
            return None
        entry_type = DISCOVER_CHANNEL_TYPES.get(raw.get("type"))
        if entry_type is None:
            return None
        name = str(raw.get("name") or "").strip() or channel_id
        return ChannelEntry(platform="discord", chat_id=channel_id, name=name, type=entry_type)

    async def _fetch_guilds_page(self, token: str, after: str | None) -> list[Any]:
        """One ``GET /users/@me/guilds`` page(after 游标翻页)。"""
        params: dict[str, Any] = {"limit": DISCOVER_PAGE_SIZE}
        if after:
            params["after"] = after
        data = await self._discover_get(token, GUILDS_API_URL, params)
        if not isinstance(data, list):
            raise PushSendError(
                "invalid_response",
                f"discord 服务器列表响应不是数组: {str(data)[:200]!r}",
            )
        return data

    async def _fetch_guild_channels(self, token: str, guild_id: str) -> list[Any]:
        """One ``GET /guilds/{id}/channels``(单服务器全量频道,无翻页)。"""
        data = await self._discover_get(
            token, f"{API_BASE}/guilds/{guild_id}/channels", None
        )
        if not isinstance(data, list):
            raise PushSendError(
                "invalid_response",
                f"discord 服务器频道列表响应不是数组(guild {guild_id[:4]}…):"
                f" {str(data)[:200]!r}",
            )
        return data

    async def _discover_get(
        self, token: str, url: str, params: dict[str, Any] | None
    ) -> Any:
        """目录发现 GET(429 退避一次再试;retry_after 优先,feishu D2 同款)。

        退避时长取响应体 ``retry_after``(Discord 429 官方字段,秒)缺省
        :attr:`discover_backoff_seconds`;经 :attr:`discover_sleeper` 注入,
        测试免真睡。二次 429 不再退避,按非 2xx 结构化报错(诚实失败)。
        """
        headers = {"Authorization": f"Bot {token}"}
        response: httpx.Response | None = None
        for attempt in (1, 2):
            try:
                if self._client is not None:
                    response = await self._client.get(url, params=params, headers=headers)
                else:
                    async with httpx.AsyncClient(timeout=self._timeout) as client:
                        response = await client.get(url, params=params, headers=headers)
            except httpx.HTTPError as exc:
                raise PushSendError(
                    "http_error", f"discord 目录发现请求失败: {type(exc).__name__}: {exc}"
                ) from exc
            if response.status_code != 429 or attempt == 2:
                break
            await self._discover_backoff(response)
        assert response is not None  # 循环体至少执行一次
        if not response.is_success:
            # 文案形态与 _post_message 同款:HTTP <status> + 原厂 body 片段。
            raise PushSendError(
                "discord_api_error",
                f"discord HTTP {response.status_code}: {response.text[:200]!r}",
            )
        try:
            return response.json()
        except ValueError as exc:
            raise PushSendError(
                "invalid_response",
                f"discord 响应不是 JSON(HTTP {response.status_code}): {response.text[:200]!r}",
            ) from exc

    async def _discover_backoff(self, response: httpx.Response) -> None:
        """429 退避:响应体 ``retry_after`` 优先,缺省类级兜底秒数。"""
        delay = self.discover_backoff_seconds
        with contextlib.suppress(ValueError):
            body = response.json()
            if isinstance(body, Mapping):
                value = body.get("retry_after")
                if isinstance(value, (int, float)) and value >= 0:
                    delay = float(value)
        logger.warning("discord 目录发现 429 限频,退避 %.1fs 重试一次", delay)
        # 经类取值调用:实例访问会把普通函数绑成方法(self 混入首参)。
        await self.__class__.discover_sleeper(delay)

    @classmethod
    def parse_direct_ref(cls, ref: str) -> ChannelTarget | None:
        """直达:雪花 id(17-20 位数字)不经目录。

        非数字形态(名称等)返回 None,调用方回落目录四路径解析。
        """
        value = ref.strip()
        if CHANNEL_ID_RE.fullmatch(value):
            return ChannelTarget(
                platform="discord", chat_id=value, resolved_from=RESOLVED_DIRECT
            )
        return None
