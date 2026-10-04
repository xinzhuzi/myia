"""Slack 通道:Bot Token ``chat.postMessage``(Bearer + channel id + JSON POST)。

蓝本归属(10-03-messaging-w3-longtail 组一):出站形态移植自 Hermes
``plugins/platforms/slack/adapter.py`` 的 ``_standalone_send`` /
``_slack_json_post`` / ``_resolve_slack_user_dm``(NousResearch/Hermes-Agent,
MIT;上游路径 ``~/.hermes/hermes-agent/plugins/platforms/slack/adapter.py``)。
MYIA 按本档语义重写,不整块复制:

- **chat.postMessage**:``POST https://slack.com/api/chat.postMessage`` +
  ``Authorization: Bearer <bot token>`` + JSON body;HTTP 200 且 ``ok=true``
  即成功——Slack 的 API 错误几乎恒为 **HTTP 200 + ``ok=false`` + ``error``**
  (blueprint ``data.get("ok")`` 同判据),错误文案保留原厂 ``error`` 值
  (``channel_not_found`` / ``invalid_auth`` / ``not_in_channel`` / …)。
- **分段**:text 上限官方 40000,蓝本 ``MAX_MESSAGE_LENGTH = 39000`` 留余量
  (:data:`MESSAGE_LIMIT`);长文按行边界自动拆多条(:func:`telegram.split_message`
  复用,逐块顺序发送,中途失败整通道报错——telegram 同款取舍)。
- **U/W 用户直达**::func:`parse_direct_ref` 收 ``U…``/``W…``(bot 不能直发
  裸用户 id,蓝本 ``channel_not_found`` 事实注释),发送期先
  ``conversations.open``(需 ``im:write`` scope)换 DM 会话 id ``D…`` 再投递;
  解析失败如实报 ``slack_api_error``(原厂 error 进文案)。**与蓝本的偏离**:
  Hermes ``_resolve_slack_user_dm`` 按 ``(token, user)`` 缓存会话 id(进程级
  ``_slack_dm_cache``);MYIA 每次发送重新 ``conversations.open``——多一次
  API 往返与限频暴露面,换取零跨 run 缓存态(通道实例不长寿,缓存收益小)。

寻址(design D1/D4):``supports_targeting=True``;``context.target.chat_id``
优先,退回 legacy ``target`` 引用(**须显式配置,无运行期 env 缺省回退**;
推荐引用名 ``env:SLACK_CHANNEL``——蓝本 cron delivery 同名先例
``SLACK_HOME_CHANNEL``,MYIA 按通道名取 ``SLACK_CHANNEL``,schema 层
target/targets 二选一强制)。直达形态 ``C/G/D/U/W`` 系 id(Hermes setup 指南:「频道
ID 以 C 开头」)。

目录自动发现(10-05-push-reliability-batch R4):``discover_directory`` 实装。
蓝本锚:Hermes ``gateway/channel_directory.py`` 的 ``_slack_team_channels``
与 ``_slack_resolve_raw_names``(上游 235-317 行,NousResearch/Hermes-Agent,
MIT)——``users.conversations``(types=public+private、exclude_archived、
limit=200、游标翻页 20 页保底)逐页聚合,再对无名单的条目
``conversations.info``/``users.info`` 补名。载体偏离:蓝本多工作空间
(``_team_clients`` 按 team 迭代)与 session DM 回填是 gateway 入站专属,
MYIA 单 bot token 单工作空间、零入站——DM 不在 types 枚举面内(蓝本同值),
靠别名手工登记(feishu 私聊同款组内约定);补名判据从「name 以 C/G/D
原始 id 前缀开头」(session 占名条目)退化为「name 缺失/空」,补名失败
保留 id 占位仍可寻址(蓝本 info 不 ok 时条目保留原名同语义);蓝本
``asyncio.gather`` 并发补名改为顺序循环(无 session 大批量,简单优先)。
私有频道落 ``type="group"``、公开频道 ``type="channel"``(蓝本 private/
channel 语汇对位 :data:`myssia.push.directory.ENTRY_TYPES` 仓内约定)。

凭据安全基线同其余通道:token 引用直到发送期才解析,错误只带引用名;全部
HTTP 经注入的 ``httpx.AsyncClient``(测试 ``httpx.MockTransport``,零真发)。
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
    "DISCOVER_MAX_PAGES",
    "DISCOVER_PAGE_SIZE",
    "DISCOVER_TYPES",
    "MESSAGE_LIMIT",
    "SlackChannel",
]

logger = logging.getLogger(__name__)

#: Slack Web API 基址(方法拼在 ``/api/<method>`` 后)。
API_BASE = "https://slack.com/api"
#: Bot token 凭据引用缺省(``xoxb-`` 系;发送期解析,值永不入日志)。
DEFAULT_TOKEN_ENV_REF = "env:SLACK_BOT_TOKEN"
#: 接收频道 id 的推荐引用名(显式配置 ``target`` 用;运行期不自动回退,
#: 两路全缺报 missing_target)。
DEFAULT_TARGET_ENV_REF = "env:SLACK_CHANNEL"
#: chat.postMessage text 上限(官方 40000;蓝本 39000 余量同款)。
MESSAGE_LIMIT = 39000
#: 直达 id 形态:``C`` 频道 / ``G`` 私有群 / ``D`` DM 会话 / ``U``/``W`` 用户
#: (U/W 发送期先 conversations.open 换 D…,蓝本 #17444 同款);9-12 位大写
#: 字母数字(Slack id 官方字符集)。
CHANNEL_ID_RE = re.compile(r"^[CGDUW][A-Z0-9]{8,20}$")
#: 目录发现 types 枚举面(蓝本 ``_slack_team_channels`` 同值:公开 + 私有
#: 成员频道;im/mpim 不入——DM 靠别名手工登记,蓝本 session 回填不适用)。
DISCOVER_TYPES = "public_channel,private_channel"
#: 目录发现页大小(蓝本同值 limit=200,官方上限)。
DISCOVER_PAGE_SIZE = 200
#: 目录发现翻页保底上限(蓝本 ``range(20)`` 护栏同款:20 页 × 200 = 4000 频道)。
DISCOVER_MAX_PAGES = 20


class SlackChannel(TrendAwareChannel):
    """``slack`` channel:每 ≤39000 字符块一次 ``chat.postMessage``。

    Args:
        target: 频道 id 的凭据引用(``env:SLACK_CHANNEL`` style,发送期解析);
            与 ``targets`` 定向配置互斥可省,此时频道由 ``context.target`` 给出。
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
            ``ok != true``(原厂 ``error`` 进文案),或模板渲染失败。
    """

    name = "slack"
    #: 目录寻址已开(context.target 优先,legacy target 兜底);协议判定见
    #: base.Channel docstring。
    supports_targeting = True
    #: 目录发现 429 退避兜底秒数(响应 Retry-After 头在场时以其为准;测试钉 0)。
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
        """Render + 逐块 ``chat.postMessage``;定向优先(``context.target.chat_id``)。

        Raises:
            PushSendError: on any credential/transport/API failure (callers
                isolate per channel; nothing is raised on success).
        """
        token = self._resolve_token()
        channel = await self._resolve_channel(token, context)
        for text in split_message(self._compose(items, context), limit=MESSAGE_LIMIT):
            await self._post_message(token, channel, text)
        logger.debug(
            "slack 发送完成: slot=%s kind=%s count=%d channel_ref=%s",
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
            raise PushSendError(exc.code, f"slack bot 凭据解析失败: {exc}") from exc

    async def _resolve_channel(self, token: str, context: SendContext) -> str:
        """定向(``context.target.chat_id``)优先,退回 legacy target 引用。

        ``U…``/``W…`` 裸用户 id 不可直发(蓝本 #17444:chat.postMessage 报
        ``channel_not_found``),先 ``conversations.open`` 换 DM 会话 id;
        其余 id(C/G/D)原样投递。解析值先过 :data:`CHANNEL_ID_RE` 形态校验
        (discord/line/mattermost 同位置同款:目录别名登记错/引用配置笔误
        → ``invalid_credential_ref`` 配置类错误,绝不原样打到 Slack API——
        那会以 200+``ok=false`` ``channel_not_found`` 回来,被死信分类按
        瞬态每轮重试)。两条寻址路径全缺 → ``missing_target``。
        """
        if context.target is not None:
            channel = context.target.chat_id.strip()
        elif self._target is not None:
            channel = self._resolve_ref(self._target, "slack target")
        else:
            raise PushSendError(
                "missing_target",
                "slack 两条寻址路径均缺席:未配置 legacy target(频道 id 引用),"
                "本次发送也未携带 context.target",
            )
        if not CHANNEL_ID_RE.fullmatch(channel):
            # 解析值不回显(死信分类误判暴露面收敛,discord/line/mattermost 同款)。
            raise PushSendError(
                "invalid_credential_ref",
                f"slack 频道/用户 id 形态非法(须为 C/G/D/U/W 前缀 + 8-20 位"
                f"大写字母数字):得到 {len(channel)} 字符的值,不匹配该形态"
                "(解析值不回显)",
            )
        if channel[:1] in ("U", "W"):
            return await self._open_dm(token, channel)
        return channel

    def _resolve_ref(self, reference: str, label: str) -> str:
        try:
            value = resolve_credential(reference).strip()
        except CredentialResolveError as exc:
            raise PushSendError(exc.code, f"{label} 解析失败: {exc}") from exc
        if not value:
            raise PushSendError(
                "invalid_credential_ref",
                f"{label} 引用 {reference!r} 解析结果为空",
            )
        return value

    async def _open_dm(self, token: str, user_id: str) -> str:
        """``conversations.open`` 换 DM 会话 id(蓝本 ``_resolve_slack_user_dm`` 同形态)。

        需应用具备 ``im:write`` scope;``ok=false``(如 ``user_not_found`` /
        ``not_authed``)原厂 error 进文案如实上抛。蓝本按 ``(token, user)``
        缓存会话 id,MYIA 每次发送重开(模块 docstring 偏离注记)。
        """
        body = {"users": user_id}
        data = await self._api_call(token, "conversations.open", body)
        channel = data.get("channel")
        dm_id = channel.get("id") if isinstance(channel, dict) else None
        if not isinstance(dm_id, str) or not dm_id.strip():
            raise PushSendError(
                "invalid_response",
                f"slack conversations.open 响应缺 channel.id(用户 {user_id[:4]}…):"
                f" {str(data)[:200]!r}",
            )
        return dm_id.strip()

    # ------------------------------------------------------------- send

    async def _post_message(self, token: str, channel: str, text: str) -> None:
        """一块正文:``chat.postMessage``(纯文本,不 unfurl 预览)。"""
        await self._api_call(token, "chat.postMessage", {"channel": channel, "text": text})

    async def _api_call(self, token: str, method: str, body: dict[str, Any]) -> dict[str, Any]:
        """``POST {API_BASE}/{method}``;HTTP 非 2xx / 非 JSON / ``ok != true`` 报错。

        错误文案保留 ``HTTP <status>`` 与原厂 ``error`` 描述片段,供死信分类
        (:func:`myssia.push.delivery.classify_dead_error`)。
        """
        url = f"{API_BASE}/{method}"
        headers = {"Authorization": f"Bearer {token}"}
        try:
            if self._client is not None:
                response = await self._client.post(url, headers=headers, json=body)
            else:
                async with httpx.AsyncClient(timeout=self._timeout) as client:
                    response = await client.post(url, headers=headers, json=body)
        except httpx.HTTPError as exc:
            raise PushSendError(
                "http_error", f"slack 请求失败: {type(exc).__name__}: {exc}"
            ) from exc
        return self._parse_api_response(response, method)

    @staticmethod
    def _parse_api_response(response: httpx.Response, method: str) -> dict[str, Any]:
        """Slack 应答公共判据:HTTP 层 → JSON → ``ok``(POST/GET 读路径共用)。"""
        if response.status_code >= 400:
            # HTTP 层错误(429 限频 / 5xx / 方法不存在):状态码先于 JSON 解析
            # 进文案,死信分类按 429/5xx → 瞬态、403/404 → 硬失败命中。
            raise PushSendError(
                "slack_api_error",
                f"slack HTTP {response.status_code}({method}): {response.text[:200]!r}",
            )
        try:
            data = response.json()
        except ValueError as exc:
            raise PushSendError(
                "invalid_response",
                f"slack 响应不是 JSON(HTTP {response.status_code}): {response.text[:200]!r}",
            ) from exc
        if not isinstance(data, dict) or data.get("ok") is not True:
            error = data.get("error") if isinstance(data, dict) else None
            raise PushSendError(
                "slack_api_error",
                f"slack API 返回错误({method}): error={error}",
            )
        return data

    # ------------------------------------------------- 目录发现(R4)+ 直达

    async def discover_directory(self) -> list[ChannelEntry]:
        """列出 bot 已加入的公开 + 私有频道(目录发现,R4 实装)。

        蓝本 ``_slack_team_channels`` + ``_slack_resolve_raw_names``
        (channel_directory.py:235-317,MIT)的 MYIA 移植:
        ``users.conversations``(types/:data:`DISCOVER_TYPES`、
        exclude_archived、limit=200、``response_metadata.next_cursor``
        游标翻页,保底 :data:`DISCOVER_MAX_PAGES` 页)逐页聚合;name
        缺失的条目再经 ``conversations.info`` 补名(im 形态经
        ``users.info`` 取 display_name,蓝本同分支)。``last_seen`` 不在
        此填——目录合并口统一盖刷新戳(feishu 同款约定)。

        Raises:
            PushSendError: 凭据缺失、HTTP 传输失败、非 JSON 响应、
                ``ok != true`` 或 429 退避一次仍失败(调用方 refresh 按发现
                失败隔离:告警 + 保留旧桶)。补名单条失败**不**上抛——保留
                id 占位仍可寻址(蓝本 info 不 ok 条目保留原名同语义)。
        """
        token = self._resolve_token()
        entries: list[ChannelEntry] = []
        seen: set[str] = set()
        cursor: str | None = None
        for _page_index in range(DISCOVER_MAX_PAGES):
            params: dict[str, Any] = {
                "types": DISCOVER_TYPES,
                "exclude_archived": "true",
                "limit": DISCOVER_PAGE_SIZE,
            }
            if cursor:
                params["cursor"] = cursor
            data = await self._api_get(token, "users.conversations", params)
            for raw in data.get("channels") or []:
                entry = self._entry_from_conversation(raw)
                if entry is not None and entry.chat_id not in seen:
                    seen.add(entry.chat_id)
                    entries.append(entry)
            metadata = data.get("response_metadata")
            cursor = (
                str(metadata.get("next_cursor") or "").strip()
                if isinstance(metadata, Mapping)
                else ""
            )
            if not cursor:
                break
        else:
            logger.warning(
                "slack 频道列表翻页达保底上限 %d 页,目录可能不完整(服务端游标未收敛)",
                DISCOVER_MAX_PAGES,
            )
        await self._resolve_raw_names(token, entries)
        return entries

    @staticmethod
    def _entry_from_conversation(raw: Any) -> ChannelEntry | None:
        """One ``channels[]`` → :class:`ChannelEntry`;形态坏 → None。

        公开频道 ``type="channel"``、私有频道 ``type="group"``(蓝本
        private/channel 语汇对位仓内 ENTRY_TYPES);``name`` 缺失先以 id
        占位(补名 pass 兜底),仍可按 id 寻址。archived 由请求参数
        exclude_archived 排除(蓝本同值),响应内不重复判。
        """
        if not isinstance(raw, Mapping):
            return None
        chat_id = str(raw.get("id") or "").strip()
        if not chat_id:
            return None
        name = str(raw.get("name") or "").strip() or chat_id
        return ChannelEntry(
            platform="slack",
            chat_id=chat_id,
            name=name,
            type="group" if raw.get("is_private") else "channel",
        )

    async def _resolve_raw_names(self, token: str, entries: list[ChannelEntry]) -> None:
        """补名 pass:name 仍是 id 占位的条目经 info 调用取名(蓝本移植)。

        ``conversations.info`` 非 im → name/name_normalized;is_im 且带
        user → ``users.info`` 取 profile.display_name → real_name → name,
        并把 type 改判 ``dm``(蓝本同分支;MYIA types 枚举面不含 im,该
        分支为形态防御)。单条失败(含 ``ok=false``)仅 debug 日志、条目
        保留 id 占位——补名是尽力而为,不阻发现(蓝本同语义)。
        """
        for entry in entries:
            if entry.name != entry.chat_id:
                continue
            try:
                info = await self._api_get(
                    token, "conversations.info", {"channel": entry.chat_id}
                )
            except PushSendError as exc:
                logger.debug(
                    "slack 目录补名失败(保留 id 占位): channel=%s error=%s",
                    entry.chat_id,
                    exc,
                )
                continue
            channel = info.get("channel")
            if not isinstance(channel, Mapping):
                continue
            resolved: str | None = None
            if not channel.get("is_im"):
                resolved = str(
                    channel.get("name") or channel.get("name_normalized") or ""
                ).strip() or None
            else:
                user_id = str(channel.get("user") or "").strip()
                if not user_id:
                    continue
                try:
                    user_info = await self._api_get(
                        token, "users.info", {"user": user_id}
                    )
                except PushSendError as exc:
                    logger.debug(
                        "slack 目录 DM 补名失败(保留 id 占位): user=%s error=%s",
                        user_id,
                        exc,
                    )
                    continue
                user = user_info.get("user")
                if isinstance(user, Mapping):
                    profile = user.get("profile")
                    resolved = (
                        str(
                            (profile.get("display_name") if isinstance(profile, Mapping) else None)
                            or user.get("real_name")
                            or user.get("name")
                            or ""
                        ).strip()
                        or None
                    )
                if resolved:
                    entry.type = "dm"
            if resolved:
                entry.name = resolved

    async def _api_get(
        self, token: str, method: str, params: dict[str, Any]
    ) -> dict[str, Any]:
        """``GET {API_BASE}/{method}``(目录发现读路径;429 退避一次再试)。

        Slack 读方法走 GET + 查询参;限频 = HTTP 429 + ``Retry-After`` 头
        (秒),退避时长以其为准、缺省 :attr:`discover_backoff_seconds`,
        经 :attr:`discover_sleeper` 注入(测试免真睡)。二次 429 不再退避,
        按 HTTP 层错误结构化报错(feishu D2 同款取舍)。应答判据与 POST 路
        径共用(:meth:`_parse_api_response`)。
        """
        url = f"{API_BASE}/{method}"
        headers = {"Authorization": f"Bearer {token}"}
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
                    "http_error", f"slack 请求失败: {type(exc).__name__}: {exc}"
                ) from exc
            if response.status_code != 429 or attempt == 2:
                break
            await self._discover_backoff(response)
        assert response is not None  # 循环体至少执行一次
        return self._parse_api_response(response, method)

    async def _discover_backoff(self, response: httpx.Response) -> None:
        """429 退避:``Retry-After`` 头优先,缺省类级兜底秒数。"""
        delay = self.discover_backoff_seconds
        header = response.headers.get("Retry-After")
        if header is not None:
            with contextlib.suppress(ValueError):
                delay = max(float(header), 0.0)
        logger.warning("slack 目录发现 429 限频,退避 %.1fs 重试一次", delay)
        # 经类取值调用:实例访问会把普通函数绑成方法(self 混入首参)。
        await self.__class__.discover_sleeper(delay)

    @classmethod
    def parse_direct_ref(cls, ref: str) -> ChannelTarget | None:
        """直达:``C/G/D/U/W`` 系 id 不经目录。

        U/W 形态发送期先 conversations.open 换 D…(蓝本 #17444);非 id 形态
        (名称等)返回 None,调用方回落目录四路径解析。
        """
        value = ref.strip()
        if CHANNEL_ID_RE.fullmatch(value):
            return ChannelTarget(
                platform="slack", chat_id=value, resolved_from=RESOLVED_DIRECT
            )
        return None
