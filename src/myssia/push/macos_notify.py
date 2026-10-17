"""macOS 通知中心通道(``macos_notify``;10-14-wechat-notify-revoke R3)。

本机零网络新通道:``/usr/bin/osascript -e 'display notification …'`` 子进程
弹系统通知——零凭据零端点零出网(正文不出现在日志/网络面;AC 审计点)。

- **寻址**:``supports_targeting = False``(无目录语义;schema 层
  ``targets``/``target`` 配置即拒,stdout 同款判例——通知中心不是地址簿)。
- **平台门**:非 darwin = 结构化 ``PushSendError(platform_unsupported)``
  (构造期零检查,发送期如实拒;同 weixin-local 的「无桥环境配置照常加载」
  纪律——配置面可加载,发送面才判平台)。
- **发送**:桌面壳在跑 = ``MYIA_NOTIFY_FIFO`` 中继管道(serve 宿主
  ``start_notify_relay`` 注入环境,子进程自动继承)逐条送壳,壳经
  tauri-plugin-notification 以 app 身份代发(10-14-notify-app-icon:图标/
  归组/点击唤起 = 世事 app;osascript 直弹的脚本编辑器图标是主人报障);
  无管道/无读者(CLI 单跑/壳已死)= ``/usr/bin/osascript`` 字面量 argv,
  10s 超时 kill;字符串转义(反斜杠/引号/换行,AppleScript 双引号串形态)。
- **合并纪律(组合优先铁律)**:同轮同 ``session_display`` 的
  ``message.new`` 条目并成**每会话一条**——title=会话名,subtitle=
  ``N 条新消息``,body=最新一条「发送者: 预览」(200 字帽);``message.
  revoke`` 事件**独立成条**:body=「<撤回者>撤回了一条消息」+ 三态
  (恢复原文/兜底文本/未能恢复)。条目元数据缺 ``event``/``session_
  display``(其他品类借用本通道)= 并成一条通用通知,body 取最新条目标题
  (如实降级,不臆造微信语义)。
- **日志只记形状**(通知条数/会话数),永不记正文(私有数据红线);
  osascript 失败载荷只带 exit 码不带 stderr(stderr 可能回显脚本正文)。

已知形态限制(如实落档不修):CLI 无壳兜底的 osascript 通知归组显示为
osascript、图标为脚本编辑器(桌面壳在跑时已由壳代发根治);系统通知中心
会留通知历史(本机态,与 WeFlow 弹窗同级)。

纯 stdlib(subprocess);测试经 ``runner``/``platform`` 注入点 mock,不触
真通知(AC7 端到端弹窗归主人实测,截图证据)。
"""

from __future__ import annotations

import json
import logging
import os
import subprocess
import sys
import threading
from pathlib import Path
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
    "NOTIFY_FIFO_ENV",
    "OSASCRIPT_BIN",
    "MacosNotifyChannel",
    "applescript_escape",
    "build_notification_script",
    "plan_notifications",
    "start_notify_relay",
]

logger = logging.getLogger(__name__)

#: 中继管道路径环境变量(桌面 serve 宿主 ``start_notify_relay`` 注入;
#: 子进程经 ``os.environ.copy()`` 继承 → cron CLI run 等全部推送路径统一)。
NOTIFY_FIFO_ENV = "MYIA_NOTIFY_FIFO"


def _fifo_write(payload: dict[str, str | None]) -> bool:
    """经中继管道送一条横幅计划;无管道/无读者 = False(调用方回退 osascript)。

    ``O_NONBLOCK``:无读者(serve 未在跑/已死)立即 ENXIO,绝不挂起采集
    子进程;payload 远小于 PIPE_BUF(文案帽 80+200 字符)→ 原子写,
    多写者(并发 cron 子进程)安全。
    """
    path = os.environ.get(NOTIFY_FIFO_ENV)
    if not path:
        return False
    data = (json.dumps(payload, ensure_ascii=False) + "\n").encode("utf-8")
    try:
        fd = os.open(path, os.O_WRONLY | os.O_NONBLOCK)
    except OSError:
        return False
    try:
        os.write(fd, data)
    except OSError:
        os.close(fd)
        return False
    os.close(fd)
    return True


#: 中继自持常开写端(中继存活期 = 宿主进程期持有不关;None = 无中继)。
#: 持有它 → 读者读端永不 EOF →「写者#1 已 close/读者未重开」的无读者
#: 空窗不存在(门禁 flaky 根因:同轮第二条 ``_fifo_write`` 撞窗 ENXIO
#: 回退泄漏一次 osascript;2026-10-15 转交注记的最小修落地)。
_RELAY_KEEPALIVE_WFD: "int | None" = None


def start_notify_relay(
    home: "str | Path",
    emit: Callable[[dict[str, "str | None"]], None],
) -> "Path | None":
    """桌面 serve 宿主启动横幅中继:创建 FIFO + 读者线程 + 注入环境变量。

    - FIFO = ``<home>/.notify.relay.fifo``(重建先 unlink,0600 私有);
    - 打开次序(零竞态关键,先读端后自持写端):``O_RDONLY|O_NONBLOCK``
      先开读端立即成(确立「有读者」),再 ``O_WRONLY|O_NONBLOCK`` 开
      自持常开写端(因读端在位必成,中继存活期持有不关)→ 读端永不
      EOF;读者线程持常开 fd 阻塞逐行读 → ``emit(plan)``(宿主:转协议
      事件 ``notify.banner`` 送壳代发);daemon,随宿主进程收尾;
    - ``os.environ`` 注入 → serve 进程内与 cron CLI 子进程(环境继承)
      的推送统一走壳;CLI 单跑(无注入)= osascript 直弹照旧。

    失败(只读文件系统/权限)只留痕返回 None = 不注入,推送自动落
    osascript 兜底,绝不拦 serve 启动。
    """
    global _RELAY_KEEPALIVE_WFD
    fifo = Path(home) / ".notify.relay.fifo"
    try:
        fifo.unlink()
    except OSError:
        pass
    try:
        os.mkfifo(fifo, 0o600)
    except OSError as exc:
        logger.warning("macos_notify 中继管道创建失败(%s);推送回退 osascript", exc)
        return None
    except AttributeError as exc:
        # 平台能力缺失(Windows 无 os.mkfifo;10-18-v0.0.5 Windows 装测
        # 实锤此路径):与创建失败同语义优雅回退,绝不把调用方拖崩——serve
        # 层已有 darwin 守卫,这里是纵深兜底(任何未来新调用点零伤)。
        logger.warning("macos_notify 中继管道不支持本平台(%s);推送回退", exc)
        return None

    # 零竞态握手:读端在位后写者们(并发 cron 子进程)的 O_WRONLY|
    # O_NONBLOCK 永不撞 ENXIO 空窗;任一步失败 = 清理已开 fd 回 None
    #(宿主进程死 = fd 全关 → 写者侧 ENXIO 回退契约不变)。
    try:
        rfd = os.open(fifo, os.O_RDONLY | os.O_NONBLOCK)
        try:
            wfd = os.open(fifo, os.O_WRONLY | os.O_NONBLOCK)
        except OSError:
            os.close(rfd)
            raise
        os.set_blocking(rfd, True)
    except OSError as exc:
        logger.warning("macos_notify 中继管道打开失败(%s);推送回退 osascript", exc)
        return None
    _RELAY_KEEPALIVE_WFD = wfd

    def _reader() -> None:
        try:
            with os.fdopen(rfd, "r", encoding="utf-8") as stream:
                for line in stream:  # 自持写端在 → 永不 EOF,阻塞候下一写者
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        plan = json.loads(line)
                    except ValueError:
                        continue
                    try:
                        emit(plan)
                    except Exception:  # noqa: BLE001 — 观测面失败不带走读者
                        logger.warning("macos_notify 中继转发失败", exc_info=True)
        except OSError:
            return  # FIFO 被删等致命态:读者退场(写者侧 ENXIO 自动回退)

    threading.Thread(
        target=_reader, name="macos-notify-relay", daemon=True
    ).start()
    os.environ[NOTIFY_FIFO_ENV] = str(fifo)
    return fifo

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
    - 元数据缺位(其他品类借用)= 单条通用通知,body 取最新条目标题;
    - 每条计划携带 ``source``(最新条目的条目源键;微信本机 = 会话名/feed
      渠道键)——壳侧横幅点击深链(10-15-notify-deeplink)据此直达该会话
      的 feed 3 级聊天工作台;缺 source(异常条目)= None,壳侧只弹不链。
    - 10-15 粒度细化:每条计划另携 ``item_key``(锚定条目的 ``dedup_key``,
      即 feed 屏 ``data-item-key`` 稳定键)——横幅点击后 3 级定位到该条
      消息(滚入视口 + 短暂高亮);合并通知锚 = 最新一条;缺 dedup_key
      (异常条目)= None,深链退回会话级。
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

    def _anchor_key(view: dict[str, Any]) -> str | None:
        """锚定条目的稳定键(dedup_key = feed 屏 data-item-key);缺 = None。"""
        key = view.get("dedup_key")
        return key if isinstance(key, str) and key.strip() else None

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
        source = view.get("source")
        plans.append({
            "title": _clip(title, TITLE_MAX_CHARS),
            "subtitle": None,
            "body": _clip(body, BODY_MAX_CHARS),
            "source": source if isinstance(source, str) and source.strip() else None,
            "item_key": _anchor_key(view),
        })
    for session, group in new_by_session.items():
        latest = max(
            group,
            key=lambda view: (view.get("ts") if isinstance(view.get("ts"), int) else 0),
        )
        sender = latest.get("sender_display") or "新消息"
        preview = latest.get("content") or latest.get("title") or ""
        body = _clip(f"{sender}: {preview}", BODY_MAX_CHARS)
        source = latest.get("source")
        plans.append({
            "title": _clip(session, TITLE_MAX_CHARS),
            "subtitle": f"{len(group)} 条新消息",
            "body": body,
            "source": source if isinstance(source, str) and source.strip() else None,
            "item_key": _anchor_key(latest),
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
            "source": latest.get("source") if isinstance(latest.get("source"), str) else None,
            "item_key": _anchor_key(latest),
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
            # 壳代发(10-14-notify-app-icon):中继管道在位先走壳(图标/归组 =
            # app 本体);管道缺失/无读者 = 该条回退 osascript,横幅不丢。
            if _fifo_write(dict(plan)):
                continue
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
