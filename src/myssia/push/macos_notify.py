"""macOS 通知中心通道(``macos_notify``;10-14-wechat-notify-revoke R3)。

本机零网络新通道:``/usr/bin/osascript -e 'display notification …'`` 子进程
弹系统通知——零凭据零端点零出网(正文不出现在日志/网络面;AC 审计点)。

- **寻址**:``supports_targeting = False``(无目录语义;schema 层
  ``targets``/``target`` 配置即拒,stdout 同款判例——通知中心不是地址簿)。
- **平台门**:非 darwin = 结构化 ``PushSendError(platform_unsupported)``
  (构造期零检查,发送期如实拒;同 weixin-local 的「无桥环境配置照常加载」
  纪律——配置面可加载,发送面才判平台)。
- **发送**:/usr/bin/osascript 字面量 argv,10s 超时 kill;字符串转义
  (反斜杠/引号/换行,AppleScript 双引号串形态)。
- **合并纪律(组合优先铁律)**:同轮同 ``session_display`` 的
  ``message.new`` 条目并成**每会话一条**——title=会话名,subtitle=
  ``N 条新消息``,body=最新一条「发送者: 预览」(200 字帽);``message.
  revoke`` 事件**独立成条**:body=「<撤回者>撤回了一条消息」+ 三态
  (恢复原文/兜底文本/未能恢复)。条目元数据缺 ``event``/``session_
  display``(其他品类借用本通道)= 并成一条通用通知,body 取最新条目标题
  (如实降级,不臆造微信语义)。
- **日志只记形状**(通知条数/会话数),永不记正文(私有数据红线);
  osascript 失败载荷只带 exit 码不带 stderr(stderr 可能回显脚本正文)。

已知形态限制(如实落档不修):通知归组显示为 osascript;系统通知中心
会留通知历史(本机态,与 WeFlow 弹窗同级)。

纯 stdlib(subprocess);测试经 ``runner``/``platform`` 注入点 mock,不触
真通知(AC7 端到端弹窗归主人实测,截图证据)。
"""

from __future__ import annotations

import logging
import subprocess
import sys
from typing import Any, Callable, Sequence

from myssia.push.base import (
    PushSendError,
    SendContext,
    TrendAwareChannel,
    clip_text,
    item_view,
)

__all__ = [
    "BODY_MAX_CHARS",
    "DEFAULT_NOTIFY_TIMEOUT_SECONDS",
    "OSASCRIPT_BIN",
    "MacosNotifyChannel",
    "applescript_escape",
    "build_notification_script",
    "plan_notifications",
]

logger = logging.getLogger(__name__)

#: osascript 字面量路径(绝不走 PATH 查找——argv 注入面收敛到零)。
OSASCRIPT_BIN = "/usr/bin/osascript"

#: 单次 osascript 超时(秒;超时 kill 兜底,R3 契约值)。
DEFAULT_NOTIFY_TIMEOUT_SECONDS = 10.0

#: 通知正文帽(R3:通知正文 200 字帽;与桥侧预览 80 字帽分工——200 是
#: 撤回兜底/长会话名的余量,不放大到全文)。
BODY_MAX_CHARS = 200

#: 通知标题帽(title 过长会被系统截断,主动收口;引擎标题同 80 帽惯例)。
TITLE_MAX_CHARS = 80

#: runner 契约:``(argv, timeout) -> (exit_code, stdout, stderr)``。
#: 测试注入点;缺省 :func:`_default_runner`(subprocess.run 超时自带 kill)。
NotifyRunner = Callable[[Sequence[str], float], "tuple[int, str, str]"]


def _default_runner(argv: Sequence[str], timeout: float) -> tuple[int, str, str]:
    """缺省 runner:字面量 argv 子进程;超时 kill(subprocess.run 自带)。"""
    proc = subprocess.run(  # noqa: S603 - 字面量 bin + 构造脚本,无外壳
        list(argv),
        capture_output=True,
        timeout=timeout,
        check=False,
    )
    return (
        proc.returncode,
        proc.stdout.decode("utf-8", "replace"),
        proc.stderr.decode("utf-8", "replace"),
    )


def applescript_escape(text: str) -> str:
    """AppleScript 双引号串转义:反斜杠/引号/换行/回车/制表。

    换行映射为 ``\\n`` 字面转义(AppleScript 双引号串内裸换行非法);
    其余控制字符拍平为空(通知正文不承载不可见噪声)。
    """
    text = text.replace("\\", "\\\\").replace('"', '\\"')
    text = text.replace("\n", "\\n").replace("\r", "\\r").replace("\t", "\\t")
    return "".join(ch for ch in text if ch >= " ")


def build_notification_script(
    *, title: str, subtitle: str | None, body: str
) -> str:
    """一条通知的 osascript 脚本(``display notification … with title …``)。"""
    parts = [
        f'display notification "{applescript_escape(body)}"',
        f'with title "{applescript_escape(title)}"',
    ]
    if subtitle:
        parts.append(f'subtitle "{applescript_escape(subtitle)}"')
    return " ".join(parts)


def _clip(text: str, limit: int) -> str:
    """截断帽(clip_text 同语义的本地别名;空值安全)。"""
    return clip_text(text, limit) if text else ""


def plan_notifications(items: Sequence[Any]) -> list[dict[str, str | None]]:
    """一轮条目 → 通知计划(每会话一条 + 撤回独立成条;R3 合并纪律)。

    - ``event == "message.revoke"``:独立一条,body=引擎侧组装好的三态
      文案(「<撤回者>撤回了一条消息」+ 原内容:"预览"/replacemsg 兜底
      文本/原内容未能恢复;取条目 content 现成 body,缺则兜底);
    - ``event == "message.new"`` 或无 event:按 ``session_display`` 分组,
      每会话一条,subtitle=N 条新消息,body=最新一条(ts 最大,序稳定)
      「发送者: 预览」;
    - 元数据缺位(其他品类借用)= 单条通用通知,body 取最新条目标题。
    """
    new_by_session: dict[str, list[dict[str, Any]]] = {}
    revokes: list[dict[str, Any]] = []
    generic: list[dict[str, Any]] = []
    for item in items:
        view = item_view(item)
        event = view.get("event")
        if event == "message.revoke":
            revokes.append(view)
        elif event == "message.new":
            session = view.get("session_display")
            key = session if isinstance(session, str) and session.strip() else "微信消息"
            new_by_session.setdefault(key, []).append(view)
        else:
            generic.append(view)

    plans: list[dict[str, str | None]] = []
    for view in revokes:
        session = view.get("session_display")
        title = session if isinstance(session, str) and session.strip() else "微信消息"
        # 撤回文案三态(恢复原文/兜底文本/未能恢复)由引擎侧组装进条目
        # content——本层取现成 body,不二次臆造;缺 content = 未能恢复兜底。
        content = view.get("content")
        body = (
            content
            if isinstance(content, str) and content.strip()
            else "撤回了一条消息(原内容未能恢复)"
        )
        plans.append({
            "title": _clip(title, TITLE_MAX_CHARS),
            "subtitle": None,
            "body": _clip(body, BODY_MAX_CHARS),
        })
    for session, group in new_by_session.items():
        latest = max(
            group,
            key=lambda view: (view.get("ts") if isinstance(view.get("ts"), int) else 0),
        )
        sender = latest.get("sender_display") or "新消息"
        preview = latest.get("content") or latest.get("title") or ""
        body = _clip(f"{sender}: {preview}", BODY_MAX_CHARS)
        plans.append({
            "title": _clip(session, TITLE_MAX_CHARS),
            "subtitle": f"{len(group)} 条新消息",
            "body": body,
        })
    if generic:
        latest = max(
            generic,
            key=lambda view: (view.get("ts") if isinstance(view.get("ts"), int) else 0),
        )
        title = latest.get("source") or "MYIA 通知"
        preview = latest.get("title") or ""
        plans.append({
            "title": _clip(str(title), TITLE_MAX_CHARS),
            "subtitle": f"{len(generic)} 条更新",
            "body": _clip(str(preview), BODY_MAX_CHARS),
        })
    return plans


class MacosNotifyChannel(TrendAwareChannel):
    """``macos_notify`` 通道:本机通知中心弹窗(零网络;同轮每会话一条)。

    Args:
        runner: 子进程 runner 注入点(测试);缺省真 osascript。
        platform: 平台覆写(测试);缺省 ``sys.platform``。
        timeout: 单次 osascript 超时秒;缺省 10(R3 契约)。
    """

    name = "macos_notify"
    #: 通知中心无目录寻址;schema 配 targets/targets 即拒(stdout 同款)。
    supports_targeting = False

    def __init__(
        self,
        *,
        runner: NotifyRunner | None = None,
        platform: str | None = None,
        timeout: float = DEFAULT_NOTIFY_TIMEOUT_SECONDS,
    ) -> None:
        self._runner = runner or _default_runner
        self._platform = platform if platform is not None else sys.platform
        self._timeout = timeout

    async def send(self, items: Sequence[Any], context: SendContext) -> None:
        """按 R3 合并纪律弹通知;平台不符/发送失败 = 结构化 PushSendError。"""
        if self._platform != "darwin":
            raise PushSendError(
                "platform_unsupported",
                "macos_notify 通道仅在 macOS 上可用(通知中心弹窗是本机"
                "形态;当前平台不是 darwin)",
            )
        plans = plan_notifications(items)
        if not plans:
            return  # 空条目组由调用方前置跳过;防御形状零弹零错
        for plan in plans:
            script = build_notification_script(
                title=str(plan["title"] or ""),
                subtitle=plan["subtitle"],
                body=str(plan["body"] or ""),
            )
            argv = [OSASCRIPT_BIN, "-e", script]
            try:
                exit_code, _stdout, _stderr = self._runner(argv, self._timeout)
            except subprocess.TimeoutExpired as exc:
                raise PushSendError(
                    "notify_timeout",
                    f"osascript 超过 {self._timeout:.0f}s 未退出,通知可能未弹出"
                    "(系统通知服务繁忙;稍后重试)",
                ) from exc
            except OSError as exc:
                raise PushSendError(
                    "osascript_failed",
                    f"osascript 启动失败({type(exc).__name__});确认 macOS 系统完整性",
                ) from exc
            if exit_code != 0:
                # 失败载荷只带 exit 码:stderr 可能回显脚本(含正文),不入错文。
                raise PushSendError(
                    "osascript_failed",
                    f"osascript exit={exit_code}(通知未弹出;检查系统通知权限:"
                    "系统设置 → 通知 → 脚本编辑器/osascript)",
                )
        # 日志只记形状:条数/会话数/槽位——永不记正文(私有数据红线)。
        logger.info(
            "macos_notify 通知已发送: kind=%s slot=%s items=%d notifications=%d",
            context.kind,
            context.slot,
            len(items),
            len(plans),
        )
