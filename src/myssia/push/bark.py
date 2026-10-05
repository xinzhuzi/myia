"""Bark 通道(iOS 即时推送):one-shot ``POST {endpoint}/{device_key}`` JSON。

蓝本 = :mod:`myssia.push.telegram` 的最薄面(10-05-push-bark:零第三方
依赖、十行级 HTTP 出站)——无分段、无发送期重试环、无目录寻址(Bark 无
目录语义,schema 配 ``targets`` 即拒,同 webhook):

- **one-shot POST**:``POST {endpoint}/{device_key}``,JSON 体
  ``{title, body, group}``;``group`` 固定 :data:`BARK_GROUP`(``"MYIA"``)
  ——iOS 通知按组聚合,信息流不刷屏(PRD 定案);``sound``/``icon``/
  ``level`` 留池不实现(YAGNI,需要时加可选字段)。
- **成功 = 2xx**;4xx/超时结构化 :class:`PushSendError` 透传(消息含
  ``HTTP <status>`` 供 delivery 死信分类按状态码文本命中;重试走既有
  delivery/retry 账本,零新配置,bark 自身不设发送期重试环)。
- **端点非密**:官方服务 ``https://api.day.app`` 或自建主机地址
  (docker ``finb/bark-server``,自建部署不在本仓范围)——可落 YAML
  (``bark_endpoint`` 字段);schema 已做 http(s) scheme 门,构造期再做
  一次形态门兜直构路径(fail-fast 于程序员错误)。
- **凭据安全基线同其余通道**:device key 是 ``target`` 凭据引用(缺省
  :data:`DEFAULT_DEVICE_KEY_REF`,env 缺失回退钥匙链规范名
  ``myia/push/BARK_DEVICE_KEY``——设置→推送 表单存入位),发送期才解析,
  错误只带引用名,永不带值;日志只记端点,永不记拼好 key 的完整 URL。

All HTTP I/O goes through an injectable ``httpx.AsyncClient`` — tests use
``httpx.MockTransport`` and never touch the real Bark server.
"""

from __future__ import annotations

import logging
from typing import Any, Sequence
from urllib.parse import urlsplit

import httpx

from myssia.push.base import (
    DEFAULT_SEND_TIMEOUT_SECONDS,
    PushSendError,
    SendContext,
    TrendAwareChannel,
    clip_text,
    item_view,
    resolve_channel_credential,
)
from myssia.push.feishu_card import card_title
from myssia.push.templates import TemplateRenderError, TemplateRenderer
from myssia.schema import CredentialResolveError

__all__ = [
    "BARK_GROUP",
    "BODY_LIMIT",
    "BarkChannel",
    "DEFAULT_BARK_ENDPOINT",
    "DEFAULT_DEVICE_KEY_REF",
    "build_body",
]

logger = logging.getLogger(__name__)

#: Bark 官方服务端点;自建填 ``bark_endpoint``(如 ``http://<host>:8080``)。
DEFAULT_BARK_ENDPOINT = "https://api.day.app"
#: device key 凭据引用缺省(发送期解析;明文启动拒,同全通道铁律)。
DEFAULT_DEVICE_KEY_REF = "env:BARK_DEVICE_KEY"
#: iOS 通知分组固定名:MYIA 的通知聚成一组,信息流不刷屏(PRD 定案)。
BARK_GROUP = "MYIA"
#: 正文字符上限:APNs 整包载荷 4KB,CJK 最宽 3 字节/字符,1024 字符稳收
#: (计入 title+JSON 开销仍在限内);超长截断并告警(通知场景一条即达,
#: 尾巴丢弃是显式取舍,ntfy 通道同款纪律)。
BODY_LIMIT = 1024


def build_body(items: Sequence[Any]) -> str:
    """内置纯文本正文:每条目一行「标题 · URL」(ntfy 同款版式,无 HTML)。

    标题不进 body——:func:`myssia.push.feishu_card.card_title` 走 JSON 的
    ``title`` 字段(跨通道标题一致);iOS 锁屏先显 title,body 点开才读。
    """
    lines: list[str] = []
    for item in items:
        view = item_view(item)
        title = str(view.get("title") or "(无标题)")
        url = view.get("url")
        lines.append(f"▸ {title} · {url}" if url else f"▸ {title}")
    return "\n".join(lines)


class BarkChannel(TrendAwareChannel):
    """``bark`` channel:每条消息一次 ``POST {endpoint}/{device_key}`` JSON。

    Args:
        target: device key 凭据引用(``env:BARK_DEVICE_KEY`` style,发送期
            解析);省略 → :data:`DEFAULT_DEVICE_KEY_REF`。明文 device key
            在此拒(``invalid_credential_ref``,零请求发出)。
        bark_endpoint: Bark 服务端端点(官方公共服务或自建主机地址;
            省略 → :data:`DEFAULT_BARK_ENDPOINT`)。**非凭据**,构造期做
            http(s) 形态门(schema 已拒 YAML 侧花样新 scheme,此处兜
            直构路径)。
        template: 可选用户模板(Jinja2);渲染输出为整条 body;省略 →
            内置纯文本版式。
        renderer: 模板渲染器;缺省共享沙箱实例。
        client: 注入用 ``httpx.AsyncClient``(测试 mock 点);省略则每次
            发送自建带 ``timeout`` 的 client。
        timeout: 自管 client 的发送超时秒数。

    Raises:
        ValueError: ``bark_endpoint`` 不是 http(s) 形态(构造期 fail-fast
            于程序员错误,同 webhook 对负 retries 的先例)。
        PushSendError: 凭据解析失败、HTTP 传输失败(含超时)、非 2xx 应答
            (消息含 ``HTTP <status>`` 供死信分类)、或模板渲染失败。
    """

    name = "bark"
    #: bark 无目录语义:不支持目录寻址(schema 配 targets 即拒,同 webhook);
    #: 显式声明保住 isinstance(Channel) 判定。
    supports_targeting = False

    def __init__(
        self,
        *,
        target: str | None = None,
        bark_endpoint: str | None = None,
        template: str | None = None,
        renderer: TemplateRenderer | None = None,
        client: httpx.AsyncClient | None = None,
        timeout: float = DEFAULT_SEND_TIMEOUT_SECONDS,
    ) -> None:
        endpoint = (bark_endpoint or DEFAULT_BARK_ENDPOINT).strip().rstrip("/")
        parts = urlsplit(endpoint)
        if parts.scheme not in ("http", "https") or not parts.netloc:
            raise ValueError(
                f"字段校验失败: bark bark_endpoint 须为 http(s)://<host>[:port] 形态"
                f"(官方服务留空即可),当前为 {bark_endpoint!r}"
            )
        self._target = target
        self._endpoint = endpoint
        self._template = template
        self._renderer = renderer or TemplateRenderer()
        self._client = client
        self._timeout = timeout

    async def send(self, items: Sequence[Any], context: SendContext) -> None:
        """Render + one-shot POST 到 ``{endpoint}/{device_key}``。

        Raises:
            PushSendError: on any credential/transport/endpoint failure
                (callers isolate per channel; nothing is raised on success).
        """
        key = self._resolve_device_key()
        payload = self._compose(items, context)
        # URL 内嵌 device key(凭据):永不进日志——logger 只记端点。
        await self._post(f"{self._endpoint}/{key}", payload)
        logger.debug(
            "bark 已推送: slot=%s kind=%s count=%d endpoint=%s",
            context.slot,
            context.kind,
            len(items),
            self._endpoint,
        )

    # ------------------------------------------------------------- compose

    def _compose(self, items: Sequence[Any], context: SendContext) -> dict[str, Any]:
        """JSON 载荷:{title, body, group=MYIA};超长 body 截断告警。"""
        if self._template is not None:
            # 契约:send 只抛 PushSendError —— 渲染失败包装为结构化的
            # template_render_error(语法错误已在加载期被 schema 拒绝)。
            try:
                body = self._renderer.render(
                    self._template, items, context, **self.trend_render_kwargs()
                )
            except TemplateRenderError as exc:
                raise PushSendError(
                    "template_render_error", f"push[].template 渲染失败: {exc}"
                ) from exc
        else:
            body = build_body(items)
        if len(body) > BODY_LIMIT:
            logger.warning("bark 消息超限,截断 %d → %d 字符", len(body), BODY_LIMIT)
            body = clip_text(body, BODY_LIMIT)
        return {"title": card_title(context), "body": body, "group": BARK_GROUP}

    def _resolve_device_key(self) -> str:
        """device key 引用 → 值(发送期;env 缺失回退 myia/push/BARK_DEVICE_KEY)。"""
        reference = self._target or DEFAULT_DEVICE_KEY_REF
        try:
            return resolve_channel_credential(
                reference, env_key="BARK_DEVICE_KEY", label="bark device key"
            )
        except CredentialResolveError as exc:
            raise PushSendError(exc.code, f"bark device key 解析失败: {exc}") from exc

    async def _post(self, url: str, payload: dict[str, Any]) -> None:
        """One-shot POST;2xx 即成功,否则结构化报错(状态码+体片段透传)。"""
        try:
            if self._client is not None:
                response = await self._client.post(url, json=payload)
            else:
                async with httpx.AsyncClient(timeout=self._timeout) as client:
                    response = await client.post(url, json=payload)
        except httpx.HTTPError as exc:
            raise PushSendError(
                "http_error", f"bark 请求失败: {type(exc).__name__}: {exc}"
            ) from exc
        if not response.is_success:
            # 状态码与响应体片段进错误文案:死信分类按「HTTP 404」命中
            # (坏 device key),原厂 message 文本一并透传(delivery 消费)。
            raise PushSendError(
                "bark_api_error",
                f"bark HTTP {response.status_code}: {response.text[:200]!r}",
            )
