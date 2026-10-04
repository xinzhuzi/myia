"""Signal 通道:signal-cli 守护进程 HTTP 模式的 JSON-RPC 出站。

出壳沿革:10-03-messaging-w3-longtail R3 曾按「外部守护进程不进核心」立
**extras 壳**(发送恒报 ``dependency_missing``);10-05-push-reliability-batch
R3 出壳——发送路纯 ``httpx`` 可达(无额外 pip 依赖,extras 门就此退役),
守护进程(signal-cli daemon ``--http`` 模式)仍是**外部系统级部署前提**
(如实写进凭据指南,不再是结构化报错壳)。

蓝本锚注记:出站形态对照 Hermes ``gateway/platforms/signal.py``
(NousResearch/Hermes-Agent,MIT)——``POST {SIGNAL_HTTP_URL}/api/v1/rpc``
的 JSON-RPC 2.0 ``send`` 方法,参数 ``{"account", "message",
"recipient": [<E.164>]" | "groupId": <id>}``;应答校验移植
``_validate_send_result``(``results[*].type != "SUCCESS"`` 或
``success=false`` 即失败,原厂 type 透传供分类)。**上游对 JSON-RPC
版本差异的处理**(移植口径,见蓝本 ``signal_rate_limit.py:25`` 与
``_is_signal_rate_limit_error``):signal-cli ≥ v0.14.3 对限流等错误给
typed JSON-RPC 错误码(如 ``-5`` RATELIMIT),旧版只在 error message
文本里漏 ``[429]``/``RateLimitException`` 子串——MYIA 不解析分版本
结构,错误 dict 的 code+message 原样透传进结构化错误文案(瞬态分类
交给 delivery 分类表,不在通道私设)。MYIA 按本仓通道形态重写
(one-shot 出站、无常驻 SSE、逐块独立请求),不整块复制。

- **凭据**(env 名对齐蓝本):``SIGNAL_HTTP_URL``(守护进程地址)+
  ``SIGNAL_ACCOUNT``(发送账号 E.164;蓝本 ``validate_signal_config``
  双必填同款)经 :func:`~myssia.push.base.resolve_channel_credential`
  (env → 钥匙链规范名 ``myia/push/<ENV_KEY>`` 回退,10-05-push-
  credential-journey 口径,双缺指引设置→推送)。**与蓝本的偏离**:
  Hermes 对 http_url 缺省 ``http://127.0.0.1:8080``(守护进程同机假设);
  MYIA 不猜地址,缺省即 ``env_var_missing`` 明示去设置→推送填。
- **寻址**:``supports_targeting=True``;``context.target.chat_id`` 优先,
  退回 legacy ``target`` 引用;两路全缺报 ``missing_target``。直达解析
  ``+手机号``(E.164,可选 ``+``;蓝本 recipient 形态——蓝本无
  @username 寻址,mention 只渲染 @号码/@UUID,不虚设)。发送路由照蓝本
  ``_with_target`` 双分支:号码形 → ``recipient`` 列表;其余(目录别名
  登记的群 id,base64)→ ``groupId``。
- **分段**:蓝本 ``MAX_MESSAGE_LENGTH = 8000`` 同款上限逐块发送。
- **目录**:无自动发现——蓝本 ``listContacts`` 只用作发送前号码→UUID
  升级(常驻会话的收件人缓存),不是目录发现;条目来源 = 直达号码 +
  别名手工登记。

错误语义(结构化 code + 中文原因):守护进程不可达/传输失败 →
``http_error``(瞬态);JSON-RPC error 应答/HTTP 非 2xx/应答坏形 →
``signal_api_error``(瞬态;daemon 级 404 是地址配错不是会话级丢失,
文案刻意用「HTTP 状态 N」措辞,不误触分类表的 chat 级 not_found 锚);
逐收件人失败(原厂 type 如 ``UNREGISTERED_FAILURE``)→
``signal_api_error`` 原样透传。凭据/模板解析失败照常走配置类码。

凭据安全基线同其余通道:YAML 只写 ``env:``/``keychain:`` 引用,发送期
才解析;错误文案只带引用名与 HTTP 状态,绝不带解析值。All HTTP I/O
goes through an injectable ``httpx.AsyncClient`` — tests use
``httpx.MockTransport``.
"""

from __future__ import annotations

import logging
import re
import time
from typing import Any, Mapping, Sequence

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
    "DEFAULT_ACCOUNT_ENV_REF",
    "DEFAULT_HTTP_URL_ENV_REF",
    "DEFAULT_TARGET_ENV_REF",
    "MESSAGE_LIMIT",
    "PHONE_RE",
    "RPC_PATH",
    "SignalChannel",
]

logger = logging.getLogger(__name__)

#: signal-cli 守护进程地址引用(蓝本 ``SIGNAL_HTTP_URL`` 同名;发送期解析)。
DEFAULT_HTTP_URL_ENV_REF = "env:SIGNAL_HTTP_URL"
#: 发送账号引用(蓝本 ``SIGNAL_ACCOUNT`` 同名,E.164 手机号;蓝本双必填同款)。
DEFAULT_ACCOUNT_ENV_REF = "env:SIGNAL_ACCOUNT"
#: legacy target 引用(``+8613…`` 手机号;群 id 走目录别名登记)。
DEFAULT_TARGET_ENV_REF = "env:SIGNAL_CHAT"
#: 单块文本上限(蓝本 ``MAX_MESSAGE_LENGTH = 8000`` 同款)。
MESSAGE_LIMIT = 8000
#: JSON-RPC 端点路径(拼在守护进程地址之后;蓝本 ``/api/v1/rpc`` 同款)。
RPC_PATH = "/api/v1/rpc"
#: 直达 recipient 形态:E.164 手机号(可选 ``+`` 前缀,7-15 位数字;蓝本
#: ``recipient`` 参数即手机号/groupId,groupId 为 base64 不设直达——
#: 蓝本无 @username 寻址,不虚设)。
PHONE_RE = re.compile(r"^\+?[0-9]{7,15}$")


def _validate_send_result(result: Any) -> str | None:
    """校验 ``send`` 应答(蓝本 ``_validate_send_result`` 移植)。

    ``results[*].type`` 非 ``SUCCESS`` → 透传该 type;``success=false`` →
    透传 ``failure`` 原因(缺省占位文案)。全部通过返回 None。
    """
    results = result.get("results") if isinstance(result, Mapping) else None
    for entry in results if isinstance(results, list) else ():
        if not isinstance(entry, Mapping):
            continue
        entry_type = entry.get("type")
        if entry_type and entry_type != "SUCCESS":
            return str(entry_type)
        if "success" in entry and not entry.get("success"):
            return str(entry.get("failure") or "Recipient delivery failed")
    return None


class SignalChannel(TrendAwareChannel):
    """``signal`` channel:JSON-RPC 2.0 one-shot 出站到 signal-cli 守护进程。

    Args:
        target: legacy target 引用(存储不解析;定向(``targets``)在场时可省
            ——两条寻址路径至少一条,否则发送期报 ``missing_target``)。
        http_url_ref: 守护进程地址引用;省略 → :data:`DEFAULT_HTTP_URL_ENV_REF`。
        account_ref: 发送账号引用;省略 → :data:`DEFAULT_ACCOUNT_ENV_REF`。
        template: 可选用户模板(Jinja2);省略 → 内置纯文本版式(ntfy 同款)。
        renderer: 模板渲染器;缺省共享沙箱实例。
        client: 注入用 ``httpx.AsyncClient``(测试 mock 点);省略则每次发送
            自建带 ``timeout`` 的 client。
        timeout: 自管 client 的发送超时秒数。

    Raises:
        PushSendError: 凭据解析失败、传输失败(守护进程不可达,瞬态)、
            JSON-RPC 错误应答或逐收件人投递失败(原厂 type 透传)。
    """

    name = "signal"
    #: 目录寻址面:context.target 优先,legacy target 兜底;协议判定见
    #: base.Channel docstring。
    supports_targeting = True

    def __init__(
        self,
        *,
        target: str | None = None,
        http_url_ref: str | None = None,
        account_ref: str | None = None,
        template: str | None = None,
        renderer: TemplateRenderer | None = None,
        client: httpx.AsyncClient | None = None,
        timeout: float = DEFAULT_SEND_TIMEOUT_SECONDS,
    ) -> None:
        self._target = target
        self._http_url_ref = http_url_ref
        self._account_ref = account_ref
        self._template = template
        self._renderer = renderer or TemplateRenderer()
        self._client = client
        self._timeout = timeout
        self._rpc_counter = 0

    async def send(self, items: Sequence[Any], context: SendContext) -> None:
        """Render + 逐块 JSON-RPC ``send``;定向优先(``context.target``)。

        Raises:
            PushSendError: on any credential/transport/API failure (callers
                isolate per channel; nothing is raised on success).
        """
        http_url = self._resolve_http_url()
        account = self._resolve_account()
        chat_id = (
            context.target.chat_id
            if context.target is not None
            else self._resolve_target()
        )
        params_base = self._routing_params(account, chat_id)
        parts = self._compose(items, context)
        for text in parts:
            await self._rpc_send(http_url, params_base, text)
        logger.debug(
            "signal 已发送: slot=%s kind=%s count=%d parts=%d",
            context.slot,
            context.kind,
            len(items),
            len(parts),
        )

    # ------------------------------------------------------------- compose

    def _compose(self, items: Sequence[Any], context: SendContext) -> list[str]:
        """消息分段:模板渲染输出或内置版式,均按 :data:`MESSAGE_LIMIT` 切。"""
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
            raise PushSendError(exc.code, f"signal {label}解析失败: {exc}") from exc

    def _resolve_http_url(self) -> str:
        value = self._resolve_credential(
            self._http_url_ref or DEFAULT_HTTP_URL_ENV_REF,
            env_key="SIGNAL_HTTP_URL",
            label="守护进程地址(SIGNAL_HTTP_URL)",
        ).rstrip("/")
        if not value:
            raise PushSendError(
                "invalid_credential_ref",
                f"signal 守护进程地址引用 {self._http_url_ref or DEFAULT_HTTP_URL_ENV_REF!r}"
                " 解析结果为空",
            )
        return value

    def _resolve_account(self) -> str:
        value = self._resolve_credential(
            self._account_ref or DEFAULT_ACCOUNT_ENV_REF,
            env_key="SIGNAL_ACCOUNT",
            label="发送账号(SIGNAL_ACCOUNT)",
        )
        if not value:
            raise PushSendError(
                "invalid_credential_ref",
                f"signal 发送账号引用 {self._account_ref or DEFAULT_ACCOUNT_ENV_REF!r}"
                " 解析结果为空",
            )
        return value

    def _resolve_target(self) -> str:
        if self._target is None:
            raise PushSendError(
                "missing_target",
                "signal 未配置 legacy target(env:/keychain: 引用,+手机号),"
                "本次发送也未携带 context.target——两条寻址路径至少一条在场",
            )
        try:
            value = resolve_channel_credential(
                self._target, env_key="SIGNAL_CHAT", label="signal 推送对象"
            ).strip()
        except CredentialResolveError as exc:
            raise PushSendError(exc.code, f"signal target 解析失败: {exc}") from exc
        if not value:
            raise PushSendError(
                "invalid_credential_ref",
                f"signal target 引用 {self._target!r} 解析结果为空",
            )
        return value

    # --------------------------------------------------------------- send

    def _routing_params(self, account: str, chat_id: str) -> dict[str, Any]:
        """蓝本 ``_with_target`` 双分支:号码形 → recipient 列表;其余 → groupId。

        蓝本以 ``group:`` 前缀显式分流;MYIA 目录登记的群 chat_id 是裸
        base64(与号码形不撞,字母/+/= 不匹配 PHONE_RE),按形态分流等价。
        """
        params: dict[str, Any] = {"account": account}
        if PHONE_RE.fullmatch(chat_id):
            params["recipient"] = [chat_id]
        else:
            params["groupId"] = chat_id
        return params

    def _next_rpc_id(self) -> str:
        """mint JSON-RPC 关联 id(蓝本 ``f"{method}_{ms}"`` 同构 + 计数器)。"""
        self._rpc_counter += 1
        return f"myssia-send-{self._rpc_counter}-{int(time.time() * 1000)}"

    async def _rpc_send(self, http_url: str, params_base: dict[str, Any], text: str) -> None:
        """一块文本一发:JSON-RPC 2.0 ``send`` + 蓝本同款应答校验。

        错误文案只带引用名与 HTTP 状态/原厂错误,绝不带解析出的地址/账号值
        (账号虽非密钥,同为解析产物不回显)。
        """
        payload = {
            "jsonrpc": "2.0",
            "method": "send",
            "params": dict(params_base, message=text),
            "id": self._next_rpc_id(),
        }
        url = f"{http_url}{RPC_PATH}"
        try:
            if self._client is not None:
                response = await self._client.post(url, json=payload)
            else:
                async with httpx.AsyncClient(timeout=self._timeout) as client:
                    response = await client.post(url, json=payload)
        except httpx.HTTPError as exc:
            raise PushSendError(
                "http_error",
                f"signal 请求失败(守护进程不可达,瞬态;地址引用 "
                f"{self._http_url_ref or DEFAULT_HTTP_URL_ENV_REF!r}): "
                f"{type(exc).__name__}: {exc}(确认本机 signal-cli daemon --http 在跑、"
                "地址与端口正确)",
            ) from exc
        if response.status_code >= 300:
            # daemon 级失败(地址/版本配错)不是会话级丢失:措辞用「HTTP 状态 N」,
            # 刻意不落「HTTP 404」锚形,避免误触 delivery 分类表的 chat 级
            # not_found(蓝本对 daemon 层失败同按瞬态处理)。
            raise PushSendError(
                "signal_api_error",
                f"signal 守护进程 HTTP 状态 {response.status_code}: {response.text[:200]!r}",
            )
        try:
            data = response.json()
        except ValueError as exc:
            raise PushSendError(
                "invalid_response",
                f"signal 应答不是 JSON(HTTP 状态 {response.status_code}): {response.text[:200]!r}",
            ) from exc
        if not isinstance(data, Mapping):
            raise PushSendError(
                "invalid_response",
                f"signal 2xx 应答不是 JSON 对象: {str(data)[:200]!r}",
            )
        if "error" in data:
            # JSON-RPC error 信封:版本差异(signal-cli ≥0.14.3 typed code 如 -5,
            # 旧版文本漏 [429]/RateLimitException)不在此分叉,code+message
            # 原样透传(蓝本 _is_signal_rate_limit_error 的分版本识别属附件
            # 限流调度器,出站文本推送不移植)。
            error = data["error"]
            error_code = error.get("code") if isinstance(error, Mapping) else None
            error_message = (
                error.get("message") if isinstance(error, Mapping) else str(error)
            )
            raise PushSendError(
                "signal_api_error",
                f"signal JSON-RPC 错误(code={error_code!r}): {str(error_message)[:200]}"
                "(瞬态;核对守护进程地址/账号与收件人)",
            )
        failure = _validate_send_result(data.get("result"))
        if failure is not None:
            raise PushSendError(
                "signal_api_error",
                f"signal 收件人投递失败(原厂结果 type): {failure}",
            )

    # ------------------------------------------------- 目录(无自动发现)+ 直达

    async def discover_directory(self) -> list[Any]:
        """signal 无目录发现:结构化说明,而非假装刷新。

        蓝本 ``listContacts`` RPC 只用作发送前号码→UUID 升级(常驻会话的
        收件人缓存),不是目录发现;MYIA 出站-only 不含。条目唯一来源 =
        直达 ``+手机号`` + 别名文件手工登记(群 id base64)。
        """
        raise DirectoryDiscoverUnsupported(
            "signal 无自动发现(蓝本 listContacts 仅作发送前号码→UUID 升级,"
            "非常驻目录发现):直达写 signal:+手机号,群可用别名文件登记"
        )

    @classmethod
    def parse_direct_ref(cls, ref: str) -> ChannelTarget | None:
        """直达:``+8613…`` 手机号(E.164,可选 ``+``)不经目录。

        蓝本无 @username 寻址(mention 只渲染 @号码/@UUID),不虚设;群 id
        (base64)与显示名不设直达——与目录别名撞形,经别名登记。其余形态
        返回 None,调用方回落目录四路径解析。
        """
        value = ref.strip()
        if PHONE_RE.fullmatch(value):
            return ChannelTarget(
                platform="signal", chat_id=value, resolved_from=RESOLVED_DIRECT
            )
        return None
