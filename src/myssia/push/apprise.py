"""Apprise 统一推送通道(extras 可选依赖,一库通吃长尾目标)。

一个 pip 依赖(caronc/apprise,MIT;extras ``myssia[apprise]``)解锁 ~160
个推送目标(Pushover/Gotify/Bark/discord-webhook 变体等长尾)——**不替代**
既有 31 通道,只为长尾目标服务(10-05-push-apprise PRD 定案)。蓝本 =
:mod:`myssia.push.bark` 的最薄面 + :mod:`myssia.push.simplex` 的依赖门:

- **target = 凭据引用**:Apprise 原生 URL 串内含 token(schema.py 明文凭据
  启动即拒的红线在 apprise 上更紧——**整串都是凭据**),只能写
  ``env:``/``keychain:`` 引用;发送期解析,解析值 = Apprise 原生目标串,
  **逗号/换行分隔多目标**(Apprise 原生语法,一引用多目标,如
  ``bark://…,pushover://…`` 两行三目标)。缺省引用 :data:`DEFAULT_TARGET_ENV_REF`
  (``env:APPRISE_URL``;env 缺失回退钥匙链规范名 ``myia/push/APPRISE_URL``
  ——设置→推送 表单存入位)。
- **依赖门(simplex 先例)**:``apprise`` 库惰性 import,**只在 send 期触发**
  ——未装且未配置 = 永不 import 零感知(不惊扰未配置用户);配了未装 =
  结构化 :class:`PushSendError` ``apprise_unavailable`` 带安装命令
  (:data:`INSTALL_COMMAND`),doctor 侧另有 ``apprise_not_installed``
  warning finding 提前披露(cli.py)。
- **发送面**::meth:`AppriseChannel.send` 每次 ``apprise.Apprise()`` 新单例,
  逐目标 ``add``(单个目标不被接受即结构化 ``apprise_target_invalid``
  fail-fast——错误只报目标**序号**不报内容,目标串含凭据永不进错误文案/
  日志),一次 ``notify(title=…, body=…)`` 广播到全部目标;``notify``
  返回 False(任一目标拒绝/不可达)= 结构化 ``apprise_notify_failed`` 透传
  不吞(重试走既有 delivery/retry 账本,本通道零发送期重试环,同 bark)。
- **无目录寻址**:目标 = URL 串,无 ``platform:名称或id`` 语义,不进
  :data:`myssia.push.PLATFORMS`(schema 配 ``targets`` 即拒,同 webhook/bark)。

All Apprise I/O goes through the injected ``apprise`` module surface
(``Apprise`` class) — tests inject a fake module via ``sys.modules``
(tests/push/test_apprise.py,crawl4ai/trafilatura 同款纪律),零真外发。
"""

from __future__ import annotations

import importlib
import logging
import re
from typing import Any, Sequence

from myssia.push.base import (
    PushSendError,
    SendContext,
    TrendAwareChannel,
    clip_text,
    resolve_channel_credential,
)
from myssia.push.bark import BODY_LIMIT, build_body
from myssia.push.feishu_card import card_title
from myssia.push.templates import TemplateRenderError, TemplateRenderer
from myssia.schema import CredentialResolveError

__all__ = [
    "APPRISE_PACKAGE",
    "AppriseChannel",
    "DEFAULT_TARGET_ENV_REF",
    "INSTALL_COMMAND",
    "parse_targets",
]

logger = logging.getLogger(__name__)

#: Apprise 库的 import 名(pip 发行名同名;extras ``myssia[apprise]``)。
APPRISE_PACKAGE = "apprise"
#: 未装时的安装命令(错误文案与 doctor finding 共用;pyproject extras 同源)。
INSTALL_COMMAND = 'pip install "myssia[apprise]"'
#: 目标串凭据引用缺省(发送期解析;明文目标串启动即拒,同全通道铁律)。
DEFAULT_TARGET_ENV_REF = "env:APPRISE_URL"


#: 目标分隔符:逗号 / 回车 / 换行(Apprise 原生聚合语法,PRD:逗号/换行
#: 多目标;连续分隔与空白片段跳过)。
_TARGET_SEPARATOR_RE = re.compile(r"[,\r\n]+")


def parse_targets(raw: str) -> list[str]:
    """Apprise 原生目标串 → 目标列表(逗号/换行分隔;保序去空)。

    Apprise 自家配置即以逗号/换行聚合多目标(原生语法);空片段跳过,
    全空由调用方按 ``invalid_credential_ref`` 拒。**不做**逐目标 URL 形态
    校验——形态对错由 Apprise ``add`` 判定(错误只报序号,内容不进日志)。
    """
    return [part for part in (piece.strip() for piece in _TARGET_SEPARATOR_RE.split(raw)) if part]


class AppriseChannel(TrendAwareChannel):
    """``apprise`` channel:一次 ``notify`` 广播到引用解析出的全部目标。

    Args:
        target: Apprise 目标串凭据引用(``env:APPRISE_URL`` style,发送期
            解析;解析值 = 逗号/换行分隔的 Apprise 原生 URL 串);省略 →
            :data:`DEFAULT_TARGET_ENV_REF`。明文目标串在此拒
            (``invalid_credential_ref``,零发送——schema 加载期已拒,此处
            兜直构路径)。
        template: 可选用户模板(Jinja2);渲染输出为整条 body;省略 →
            内置纯文本版式(bark 同款一行一条)。
        renderer: 模板渲染器;缺省共享沙箱实例。

    Raises:
        PushSendError: apprise 库未装(``apprise_unavailable``,文案带安装
            命令)、凭据解析失败、目标串为空、某目标不被 Apprise 接受
            (``apprise_target_invalid``,只报序号)、``notify`` 广播失败
            (``apprise_notify_failed``),或模板渲染失败。
    """

    name = "apprise"
    #: apprise 无目录语义:不支持目录寻址(schema 配 targets 即拒,同
    #: webhook/bark);显式声明保住 isinstance(Channel) 判定。
    supports_targeting = False

    def __init__(
        self,
        *,
        target: str | None = None,
        template: str | None = None,
        renderer: TemplateRenderer | None = None,
    ) -> None:
        self._target = target
        self._template = template
        self._renderer = renderer or TemplateRenderer()

    async def send(self, items: Sequence[Any], context: SendContext) -> None:
        """Render + 一次 ``notify(title, body)`` 广播到全部目标。

        依赖门在此触发(构造/加载期零 import——没配该通道的用户永不感知);
        单个目标 ``add`` 失败即 fail-fast,不半推(部分目标坏 = 整次结构化
        拒,交给上层按通道隔离重试)。

        Raises:
            PushSendError: on any dependency/credential/target/notify failure
                (callers isolate per channel; nothing is raised on success).
        """
        apprise = _require_apprise()
        targets = self._resolve_targets()
        title, body = self._compose(items, context)
        notifier = apprise.Apprise()
        for index, url in enumerate(targets, start=1):
            try:
                accepted = notifier.add(url)
            except Exception as exc:  # noqa: BLE001 - Apprise 解析异常面未成文,结构化兜住
                raise PushSendError(
                    "apprise_target_invalid",
                    f"apprise 第 {index}/{len(targets)} 个目标解析异常:"
                    f" {type(exc).__name__}: {exc}(错误只报序号,目标串含凭据不进文案)",
                ) from exc
            if accepted is False:
                raise PushSendError(
                    "apprise_target_invalid",
                    f"apprise 第 {index}/{len(targets)} 个目标未被接受"
                    "(检查 URL 形态是否为 Apprise 支持的目标;错误只报序号,"
                    "目标串含凭据不进文案)",
                )
        try:
            delivered = notifier.notify(title=title, body=body)
        except Exception as exc:  # noqa: BLE001 - 广播异常面未成文,结构化兜住
            raise PushSendError(
                "apprise_notify_failed",
                f"apprise 通知广播异常: {type(exc).__name__}: {exc}",
            ) from exc
        if not delivered:
            raise PushSendError(
                "apprise_notify_failed",
                "apprise 通知发送失败(notify 返回 False:某目标拒绝或不可达;"
                "重试由推送账本按通道统一调度)",
            )
        logger.debug(
            "apprise 已推送: slot=%s kind=%s count=%d targets=%d title_chars=%d",
            context.slot,
            context.kind,
            len(items),
            len(targets),
            len(title),
        )

    # ------------------------------------------------------------- compose

    def _compose(self, items: Sequence[Any], context: SendContext) -> tuple[str, str]:
        """(title, body):标题走 ``card_title`` 跨通道一致;body=bark 同款版式。

        body 上限同 bark :data:`BODY_LIMIT`(1024):Apprise 目标家族上限差异
        极大(SMS 极短 / Discord 2000),取通知场景最保守公共预算,超长截断
        并告警(一条即达的通知,尾巴丢弃是显式取舍;bark/ntfy 同款纪律)。
        """
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
            logger.warning(
                "apprise 消息超限,截断 %d → %d 字符", len(body), BODY_LIMIT
            )
            body = clip_text(body, BODY_LIMIT)
        return card_title(context), body

    # ------------------------------------------------------------- resolve

    def _resolve_targets(self) -> list[str]:
        """目标串引用 → 目标列表(发送期;env 缺失回退 myia/push/APPRISE_URL)。"""
        reference = self._target or DEFAULT_TARGET_ENV_REF
        try:
            value = resolve_channel_credential(
                reference, env_key="APPRISE_URL", label="apprise 推送目标串"
            )
        except CredentialResolveError as exc:
            raise PushSendError(exc.code, f"apprise target 解析失败: {exc}") from exc
        targets = parse_targets(value)
        if not targets:
            raise PushSendError(
                "invalid_credential_ref",
                f"apprise target 引用 {reference!r} 解析结果为空串(应为逗号/"
                "换行分隔的 Apprise 目标 URL 串)",
            )
        return targets


def _require_apprise() -> Any:
    """惰性 import ``apprise``;缺装 → ``apprise_unavailable``(simplex 先例)。

    只在 send 期调用:未配置该通道的用户永不触发(import 面零扩大),
    doctor 侧用 find_spec 预检(cli.py ``apprise_not_installed``)。
    """
    try:
        return importlib.import_module(APPRISE_PACKAGE)
    except ImportError as exc:
        raise PushSendError(
            "apprise_unavailable",
            f"apprise 通道依赖 {APPRISE_PACKAGE} 库未安装(统一推送:"
            f"~160 个长尾目标一个依赖通吃):请先执行 {INSTALL_COMMAND}"
            f"(或 uv sync --extra apprise);未配置 apprise 通道的品类不受影响",
        ) from exc
