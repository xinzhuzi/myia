"""BlueBubbles 通道:自建 BlueBubbles 服务端的 REST 出站(iMessage 桥)。

出壳沿革:10-03-messaging-w3-longtail R3 曾按「需要外部服务端不进核心」立
**extras 壳**(发送恒报 ``dependency_missing``);10-05-push-reliability-batch
R3 出壳——发送路纯 ``httpx`` 可达(无额外 pip 依赖,extras 门就此退役),
BlueBubbles 服务端(常驻 macOS 并接管 Messages.app 的自建 iMessage 桥)
仍是**外部系统级部署前提**(如实写进凭据指南,不再是结构化报错壳)。

蓝本锚注记:出站形态对照 Hermes ``gateway/platforms/bluebubbles.py``
(NousResearch/Hermes-Agent,MIT)——``POST {server}/api/v1/message/text``,
鉴权 ``?password=`` 查询参数(BlueBubbles 不能发自定义头,查询串是唯一
通道,蓝本 ``_api_url`` 同款),body ``{"chatGuid", "tempGuid", "message"}``;
chat 目标先经 ``POST /api/v1/chat/query`` 解析成 GUID(裸 GUID——含
``;`` 分段——直通,蓝本 ``_resolve_chat_guid`` 同款按 ``chatIdentifier``/
``identifier`` 严格匹配,参与者成员故意不做回退:同一联系人同时挂在
1:1 与任意多群里,按参与者匹配会把 DM 回复漏进群会话);邮箱/``+`` 手机
号形地址可 ``POST /api/v1/chat/new`` 直开新会话(蓝本
``_create_chat_for_handle``;蓝本以 server-info 的 private_api 开关为门,
MYIA one-shot 不先探 info,直开交服务端裁决——private API 未开时服务端
拒绝,结构化错误如实呈现)。URL 规范化(无 scheme 补 ``http://``、去尾
``/``)移植蓝本 ``_normalize_server_url``。MYIA 按本仓通道形态重写
(one-shot 出站、无常驻 webhook 监听、无跨发送 GUID LRU 缓存),不整块复制。

- **凭据**(env 名对齐蓝本):``BLUEBUBBLES_SERVER_URL`` +
  ``BLUEBUBBLES_PASSWORD`` 经
  :func:`~myssia.push.base.resolve_channel_credential`(env → 钥匙链规范名
  ``myia/push/<ENV_KEY>`` 回退,10-05-push-credential-journey 口径,双缺
  指引设置→推送)。
- **寻址**:``supports_targeting=True``;``context.target.chat_id`` 优先,
  退回 legacy ``target`` 引用;两路全缺报 ``missing_target``。直达解析
  ``iMessage;…``/``SMS;…`` chat GUID 形态与 ``+`` 手机号(蓝本
  ``chatGuid``/``_ADDRESS_RE`` 形态)。
- **分段**:蓝本 ``MAX_TEXT_LENGTH = 4000`` 同款上限;蓝本按段落拆独立
  iMessage 泡,MYIA 用仓内共享 ``split_message`` 整体切(通知卡不续聊,
  偏离已注记)。
- **目录**:无自动发现——蓝本 ``chat/query`` 在 MYIA 仅作发送前 GUID
  解析(一次性,无缓存);目录发现未实装,条目来源 = 直达 + 别名登记。

错误语义(结构化 code + 中文原因):服务端不可达/传输失败 →
``http_error``(瞬态);HTTP 非 2xx(含 401 密码错)→
``bluebubbles_api_error``(鉴权失败是配置级根因,文案明示核对
``BLUEBUBBLES_PASSWORD``;重试分类面归 delivery 分类表,通道不私设);
GUID 解析不到且非地址形 → ``bluebubbles_api_error``,文案带 chat 级
``chat not found`` 锚(该会话确认不可达,死信语义成立,蓝本同款错误);
应答坏形 → ``invalid_response``。凭据/模板解析失败照常走配置类码。

凭据安全基线同其余通道:password 走 URL 查询串——错误文案与日志**绝不**
带完整 URL(只带路径与引用名),凭据永不落盘。All HTTP I/O goes through
an injectable ``httpx.AsyncClient`` — tests use ``httpx.MockTransport``.
"""

from __future__ import annotations

import logging
import re
import time
from typing import Any, Mapping, Sequence
from urllib.parse import quote

import httpx

from myssia.push.base import (
    DEFAULT_SEND_TIMEOUT_SECONDS,
    PushSendError,
    SendContext,
    TrendAwareChannel,
    resolve_channel_credential,
)
from myssia.push.directory import DirectoryDiscoverUnsupported
from myssia.push.ntfy import build_message
from myssia.push.targets import RESOLVED_DIRECT, ChannelTarget
from myssia.push.telegram import split_message
from myssia.push.templates import TemplateRenderError, TemplateRenderer
from myssia.schema import CredentialResolveError

__all__ = [
    "CHAT_GUID_RE",
    "DEFAULT_PASSWORD_ENV_REF",
    "DEFAULT_SERVER_ENV_REF",
    "DEFAULT_TARGET_ENV_REF",
    "MESSAGE_LIMIT",
    "PHONE_RE",
    "BlueBubblesChannel",
    "normalize_server_url",
]

logger = logging.getLogger(__name__)

#: 服务端 base URL 引用(蓝本 ``BLUEBUBBLES_SERVER_URL`` 同名;发送期解析)。
DEFAULT_SERVER_ENV_REF = "env:BLUEBUBBLES_SERVER_URL"
#: 服务端 password 引用(蓝本 ``BLUEBUBBLES_PASSWORD`` 同名;查询串鉴权)。
DEFAULT_PASSWORD_ENV_REF = "env:BLUEBUBBLES_PASSWORD"
#: legacy target 引用(chat GUID 或手机号;群/邮箱走目录别名登记)。
DEFAULT_TARGET_ENV_REF = "env:BLUEBUBBLES_CHAT"
#: 单条消息上限(蓝本 ``MAX_TEXT_LENGTH = 4000`` 同款)。
MESSAGE_LIMIT = 4000
#: 直达 chat GUID 形态(蓝本 chatGuid:``iMessage;…``/``SMS;…`` sigil 起头,
#: 分号分段;群 GUID 含 ``chat…``、DM 为服务格式 + 地址段)。
CHAT_GUID_RE = re.compile(r"^(iMessage|SMS);[-A-Za-z0-9.;+]+$")
#: 直达手机号形态(蓝本 ``_ADDRESS_RE = ^\+\d+``;新会话可按地址直开)。
PHONE_RE = re.compile(r"^\+[0-9]{7,15}$")
#: 地址形判定(邮箱含 ``@`` 或 ``+`` 起头号码;蓝本 chat/new 触发条件同款)。
_EMAIL_MARK = "@"


def normalize_server_url(raw: str) -> str:
    """URL 规范化(蓝本 ``_normalize_server_url`` 移植):补 scheme、去尾斜杠。"""
    value = (raw or "").strip()
    if value and not re.match(r"^https?://", value, flags=re.I):
        value = f"http://{value}"
    return value.rstrip("/")


def _temp_guid() -> str:
    """tempGuid(蓝本 ``_temp_guid`` 同构:temp- + 时间戳)。"""
    return f"temp-{time.time()}"


class BlueBubblesChannel(TrendAwareChannel):
    """``bluebubbles`` channel:REST one-shot 出站到自建 BlueBubbles 服务端。

    Args:
        target: legacy target 引用(chat GUID / ``+`` 手机号 / 邮箱;存储不
            解析);定向(``targets``)在场时可省——两条寻址路径至少一条,
            否则发送期报 ``missing_target``。
        server_ref: 服务端 base URL 引用;省略 → :data:`DEFAULT_SERVER_ENV_REF`。
        password_ref: 服务端 password 引用;省略 →
            :data:`DEFAULT_PASSWORD_ENV_REF`。
        template: 可选用户模板(Jinja2);省略 → 内置纯文本版式(ntfy 同款)。
        renderer: 模板渲染器;缺省共享沙箱实例。
        client: 注入用 ``httpx.AsyncClient``(测试 mock 点);省略则每次发送
            自建带 ``timeout`` 的 client。
        timeout: 自管 client 的发送超时秒数。

    Raises:
        PushSendError: 凭据解析失败、传输失败(服务端不可达,瞬态)、HTTP
            错误应答(401 鉴权失败文案明示核对 password)、GUID 解析不到
            (chat 级 not_found 锚)或应答坏形。
    """

    name = "bluebubbles"
    #: 目录寻址面:context.target 优先,legacy target 兜底;协议判定见
    #: base.Channel docstring。
    supports_targeting = True

    def __init__(
        self,
        *,
        target: str | None = None,
        server_ref: str | None = None,
        password_ref: str | None = None,
        template: str | None = None,
        renderer: TemplateRenderer | None = None,
        client: httpx.AsyncClient | None = None,
        timeout: float = DEFAULT_SEND_TIMEOUT_SECONDS,
    ) -> None:
        self._target = target
        self._server_ref = server_ref
        self._password_ref = password_ref
        self._template = template
        self._renderer = renderer or TemplateRenderer()
        self._client = client
        self._timeout = timeout

    async def send(self, items: Sequence[Any], context: SendContext) -> None:
        """Render + GUID 解析 + 逐块 ``message/text``;定向优先。

        Raises:
            PushSendError: on any credential/transport/API failure (callers
                isolate per channel; nothing is raised on success).
        """
        server = self._resolve_server()
        password = self._resolve_password()
        chat_id = (
            context.target.chat_id
            if context.target is not None
            else self._resolve_target()
        )
        parts = self._compose(items, context)
        guid = await self._resolve_chat_guid(server, password, chat_id)
        via_new_chat = False
        if guid is None:
            # 地址形(邮箱/+手机号)按蓝本 chat/new 直开新会话:首块即
            # chat/new 正文(蓝本同款);余块重解析一次 GUID 再走常规路
            # (蓝本对新会话只发首块即返回,MYIA 补齐余块——偏离已注记)。
            if _EMAIL_MARK in chat_id or PHONE_RE.fullmatch(chat_id):
                await self._post_new_chat(server, password, chat_id, parts[0])
                via_new_chat = True
                if len(parts) > 1:
                    guid = await self._resolve_chat_guid(server, password, chat_id)
                    if guid is None:
                        raise PushSendError(
                            "bluebubbles_api_error",
                            f"bluebubbles 新会话已发首块,但余 {len(parts) - 1} 块"
                            f"仍解析不到 chat GUID(target {chat_id[:120]!r}):"
                            "(部分投递;到该会话产生一条真实消息后重推)",
                        )
            else:
                raise PushSendError(
                    "bluebubbles_api_error",
                    f"BlueBubbles chat not found for target: {chat_id[:120]!r}"
                    "(chat 级丢失:核对 chat GUID/手机号,或先在该会话里产生一条"
                    "真实消息再推)",
                )
        remainder = parts[1:] if via_new_chat else parts
        for text in remainder:
            payload = {"chatGuid": guid, "tempGuid": _temp_guid(), "message": text}
            await self._post_json(server, password, "/api/v1/message/text", payload)
        logger.debug(
            "bluebubbles 已发送: slot=%s kind=%s count=%d parts=%d guid=%s",
            context.slot,
            context.kind,
            len(items),
            len(parts),
            "new-chat" if via_new_chat else "resolved",
        )

    # ------------------------------------------------------------- compose

    def _compose(self, items: Sequence[Any], context: SendContext) -> list[str]:
        """消息分段:模板渲染输出或内置版式,均按 :data:`MESSAGE_LIMIT` 切。

        蓝本按段落拆独立 iMessage 泡(``re.split(r'\\n\\s*\\n', …)``);MYIA
        用仓内共享 ``split_message`` 换行边界整体切——通知卡不续聊,泡边界
        无业务语义(偏离已注记,蓝本锚见模块 docstring)。
        """
        if self._template is not None:
            # 契约:send 只抛 PushSendError —— 渲染失败包装为结构化的
            # template_render_error(语法错误已在加载期被 schema 拒绝)。
            try:
                text = self._renderer.render(
                    self._template, items, context, **self.trend_render_kwargs()
                )
            except TemplateRenderError as exc:
                raise PushSendError(
                    "template_render_error", f"push[].template 渲染失败: {exc}"
                ) from exc
            return split_message(text, limit=MESSAGE_LIMIT)
        return split_message(build_message(items, context), limit=MESSAGE_LIMIT)

    # ------------------------------------------------------------- resolve

    def _resolve_credential(self, reference: str, *, env_key: str, label: str) -> str:
        """凭据解析(env → 钥匙链规范名回退;双缺指引设置→推送)。"""
        try:
            return resolve_channel_credential(
                reference, env_key=env_key, label=label
            ).strip()
        except CredentialResolveError as exc:
            raise PushSendError(exc.code, f"bluebubbles {label}解析失败: {exc}") from exc

    def _resolve_server(self) -> str:
        value = normalize_server_url(
            self._resolve_credential(
                self._server_ref or DEFAULT_SERVER_ENV_REF,
                env_key="BLUEBUBBLES_SERVER_URL",
                label="服务端地址(BLUEBUBBLES_SERVER_URL)",
            )
        )
        if not value:
            raise PushSendError(
                "invalid_credential_ref",
                f"bluebubbles 服务端地址引用 {self._server_ref or DEFAULT_SERVER_ENV_REF!r}"
                " 解析结果为空",
            )
        return value

    def _resolve_password(self) -> str:
        value = self._resolve_credential(
            self._password_ref or DEFAULT_PASSWORD_ENV_REF,
            env_key="BLUEBUBBLES_PASSWORD",
            label="服务端密码(BLUEBUBBLES_PASSWORD)",
        )
        if not value:
            raise PushSendError(
                "invalid_credential_ref",
                f"bluebubbles 服务端密码引用 {self._password_ref or DEFAULT_PASSWORD_ENV_REF!r}"
                " 解析结果为空",
            )
        return value

    def _resolve_target(self) -> str:
        if self._target is None:
            raise PushSendError(
                "missing_target",
                "bluebubbles 未配置 legacy target(env:/keychain: 引用,chat GUID/"
                "手机号/邮箱),本次发送也未携带 context.target——两条寻址路径"
                "至少一条在场",
            )
        try:
            value = resolve_channel_credential(
                self._target, env_key="BLUEBUBBLES_CHAT", label="bluebubbles 推送对象"
            ).strip()
        except CredentialResolveError as exc:
            raise PushSendError(exc.code, f"bluebubbles target 解析失败: {exc}") from exc
        if not value:
            raise PushSendError(
                "invalid_credential_ref",
                f"bluebubbles target 引用 {self._target!r} 解析结果为空",
            )
        return value

    # ---------------------------------------------------------- REST plumbing

    def _api_url(self, server: str, password: str, path: str) -> str:
        """鉴权 URL(蓝本 ``_api_url`` 同款:password 走查询串)。

        产物只进 httpx 请求,绝不进日志/错误文案(password 内嵌其中)。
        """
        suffix = f"{'&' if '?' in path else '?'}password={quote(password, safe='')}"
        return f"{server}{path}{suffix}"

    async def _request(
        self, server: str, password: str, path: str, payload: Mapping[str, Any]
    ) -> dict[str, Any]:
        """POST one JSON 请求并解包校验;错误文案只带路径/状态/响应片段。

        Raises:
            PushSendError: 传输失败(http_error,瞬态)、HTTP 非 2xx
                (bluebubbles_api_error;401 明示鉴权失败核对 password)、
                非 JSON/非对象应答(invalid_response)。
        """
        url = self._api_url(server, password, path)
        try:
            if self._client is not None:
                response = await self._client.post(url, json=dict(payload))
            else:
                async with httpx.AsyncClient(timeout=self._timeout) as client:
                    response = await client.post(url, json=dict(payload))
        except httpx.HTTPError as exc:
            raise PushSendError(
                "http_error",
                f"bluebubbles 请求失败(服务端不可达,瞬态;地址引用 "
                f"{self._server_ref or DEFAULT_SERVER_ENV_REF!r},路径 {path}): "
                f"{type(exc).__name__}: {exc}(确认 BlueBubbles 服务端在跑、地址正确)",
            ) from exc
        if response.status_code == 401:
            # 鉴权失败是配置级根因(重试无解):文案明示核对凭据;分类面归
            # delivery 分类表(码不在配置码表内,按瞬态有界重试,如实注记)。
            raise PushSendError(
                "bluebubbles_api_error",
                f"bluebubbles 鉴权失败(HTTP 状态 401,路径 {path}): "
                f"{response.text[:200]!r}(核对 BLUEBUBBLES_PASSWORD 与服务端"
                "设置的密码一致)",
            )
        if response.status_code >= 300:
            raise PushSendError(
                "bluebubbles_api_error",
                f"bluebubbles HTTP 状态 {response.status_code}(路径 {path}): "
                f"{response.text[:200]!r}",
            )
        try:
            data = response.json()
        except ValueError as exc:
            raise PushSendError(
                "invalid_response",
                f"bluebubbles 应答不是 JSON(HTTP 状态 {response.status_code},"
                f"路径 {path}): {response.text[:200]!r}",
            ) from exc
        if not isinstance(data, Mapping):
            raise PushSendError(
                "invalid_response",
                f"bluebubbles 2xx 应答不是 JSON 对象(路径 {path}): {str(data)[:200]!r}",
            )
        return dict(data)

    async def _resolve_chat_guid(
        self, server: str, password: str, chat_id: str
    ) -> str | None:
        """chat 目标 → GUID(蓝本 ``_resolve_chat_guid`` 一次性版)。

        裸 GUID(含 ``;``)直通;其余经 ``chat/query`` 按
        ``chatIdentifier``/``identifier`` 严格匹配(参与者成员不做回退,
        蓝本同款:防 DM 回复漏进群会话)。查不到返回 None 由调用方分派
        (地址形直开新会话/其余报 chat 级丢失)。跨发送不缓存(one-shot
        纪律;蓝本 LRU 属常驻适配器形态,不移植)。
        """
        if ";" in chat_id:
            return chat_id
        data = await self._request(
            server, password, "/api/v1/chat/query", {"limit": 100, "offset": 0}
        )
        for chat in data.get("data") or []:
            if not isinstance(chat, Mapping):
                continue
            if (chat.get("chatIdentifier") or chat.get("identifier")) != chat_id:
                continue
            if guid := chat.get("guid") or chat.get("chatGuid"):
                return str(guid)
        return None

    async def _post_new_chat(
        self, server: str, password: str, address: str, message: str
    ) -> None:
        """按地址直开新会话并发首块(蓝本 ``_create_chat_for_handle`` 移植)。

        蓝本以 server-info 的 private_api 开关为门;MYIA one-shot 不先探
        info——直开交服务端裁决,private API 未开时结构化错误如实呈现。
        """
        await self._request(
            server,
            password,
            "/api/v1/chat/new",
            {"addresses": [address], "message": message, "tempGuid": _temp_guid()},
        )

    async def _post_json(
        self, server: str, password: str, path: str, payload: Mapping[str, Any]
    ) -> dict[str, Any]:
        """POST + 2xx 即成功(蓝本 ``_post_message`` 同款成功口径)。"""
        return await self._request(server, password, path, payload)

    # ------------------------------------------------- 目录(无自动发现)+ 直达

    async def discover_directory(self) -> list[Any]:
        """bluebubbles 无目录发现:结构化说明,而非假装刷新。

        蓝本的 ``chat/query`` 在 MYIA 仅作发送前 GUID 解析(一次性);目录
        发现未实装(条目来源 = 直达 + 别名手工登记)。
        """
        raise DirectoryDiscoverUnsupported(
            "bluebubbles 无自动发现(chat/query 仅作发送前 GUID 解析,不作出站"
            "目录):直达写 bluebubbles:iMessage;… / SMS;… 或 +手机号,"
            "常用地名可用别名文件登记"
        )

    @classmethod
    def parse_direct_ref(cls, ref: str) -> ChannelTarget | None:
        """直达:chat GUID(``iMessage;…``/``SMS;…``)与 ``+`` 手机号不经目录。

        邮箱/显示名不设直达——与目录别名撞形,经别名登记;其余形态返回
        None,调用方回落目录四路径解析。
        """
        value = ref.strip()
        if CHAT_GUID_RE.fullmatch(value) or PHONE_RE.fullmatch(value):
            return ChannelTarget(
                platform="bluebubbles", chat_id=value, resolved_from=RESOLVED_DIRECT
            )
        return None
