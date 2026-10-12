"""UI 通道实现层(task 10-11-wechat-ui-bridge Phase C/D 落点位)。

**Phase C 读通道已按 D2 定论改写为像素链**(A1 实测微信 4.1.15 聊天内容层
对 AX 完全零暴露,证据 research/ax-probe-4.1.15.md):``sessions list`` /
``messages read`` 委托 :mod:`.pixel`(截窗 → VisionOCR → VL 校对 → 结构化
解析;静默铁律全套:零激活、零合成点击、零抢焦点)。原「AX 树遍历」实现
整体作废,本模块保留前置检查门与写通道占位。

实现层未落地时的应答纪律(现仅剩 Phase D 写通道):结构化
:class:`BridgeError`(exit 1,通用失败段,``code="not_implemented"``)——
**绝不谎报为任何 §6 具名族**。

静默铁律(prd 红线 4)对本模块的约束:
读=像素链(screencapture -l 对后台窗口零交互,ordered-off 窗可截,
2026-10-11 实测);写=AX 动作(AXPress/AXConfirm 类),禁合成鼠标事件、
禁激活窗口、禁抢前台焦点——A1 实测 AX 写通道整体不可达,Phase D1 按
「官方 iLink 桥独任」第三案收口,UI 写如实报不可用。
"""

from __future__ import annotations

from typing import Callable

from .codes import (
    AX_PERMISSION_DENIED,
    SCREEN_RECORDING_DENIED,
    WECHAT_NOT_RUNNING,
    WINDOW_CLOSED,
    EXIT_GENERIC_FAILURE,
    BridgeError,
)
from .config import BridgeConfig

__all__ = ["ensure_ui_preconditions", "not_implemented", "list_sessions", "read_messages", "send_text"]

#: 骨架过渡码(design §6 表外唯一过渡态;Phase C/D 落地即消亡)。
NOT_IMPLEMENTED_CODE = "not_implemented"


def ensure_ui_preconditions(
    *,
    process_running: Callable[[], bool] | None = None,
    ax_trusted: Callable[[], bool | None] | None = None,
    window_open: Callable[[], bool | None] | None = None,
    screen_granted: Callable[[], bool | None] | None = None,
) -> None:
    """UI 通道前置检查门(§6 码序:10 → 11 → 12;全绿放行)。

    检查器与探针共用 :mod:`.system_checks` 注入点;窗口态 ``None``
    (判定不可及)不拦截——探测不到窗口不等于窗口没开,误拦会把可用态
    报死;真窗口态由 AX 树探测(Phase C)给出终局结论。
    """
    from . import system_checks as sc

    process = process_running if process_running is not None else sc.wechat_process_running
    trusted = ax_trusted if ax_trusted is not None else sc.ax_permission_trusted
    window = window_open if window_open is not None else sc.wechat_main_window_open
    screen = screen_granted if screen_granted is not None else sc.screen_recording_granted

    if not process():
        raise BridgeError(
            WECHAT_NOT_RUNNING,
            "微信进程不在运行,UI 通道无对象可驱",
            fix_hint="启动微信客户端后重试",
        )
    # 2026-10-13 勘误(0.3.1 残留收口):AX 通道 A1 定论死路后,像素链是唯一
    # UI 读路,其真实 TCC 前置=屏幕录制(截窗),不是辅助功能——生产宿主缺 AX
    # 权限把像素链拦死在码 11(run 108 实锤)。AX 检查退出前置门(probe 保留
    # 报告位);本门码序改为 10 → 11(screen_recording_denied) → 12。
    if screen() is False:
        raise BridgeError(
            SCREEN_RECORDING_DENIED,
            "屏幕录制权限缺失:像素链截窗需要 TCC 屏幕录制授权",
            fix_hint="系统设置 → 隐私与安全性 → 屏幕录制,给 MYIA(或桥宿主进程)授权",
        )
    if window() is False:
        raise BridgeError(
            WINDOW_CLOSED,
            "微信主窗口未开(托盘态):UI 通道无窗口可读",
            fix_hint="打开微信主窗口;本地库只读通道(localdb)不受此限",
        )


def not_implemented(operation: str, landing_phase: str) -> BridgeError:
    """骨架过渡应答(exit 1 + not_implemented;不谎报 §6 具名族)。"""
    return BridgeError(
        EXIT_GENERIC_FAILURE,
        f"{operation} 的实现层尚未落地({landing_phase});当前为 Phase B 桥骨架,"
        "前置检查通过但无实现可执行",
        code=NOT_IMPLEMENTED_CODE,
        fix_hint=f"等待 {landing_phase} 落地;期间可用通道:probe(三态)/ localdb(按 D4)",
    )


def list_sessions(config: BridgeConfig, limit: int | None = None) -> dict[str, object]:
    """``sessions list`` 实现(Phase C1:D2 定论后 = 像素链,委托 :mod:`.pixel`)。

    Returns:
        §6 契约 ``{"sessions":[{"id","name","unread",…}]}`` + 附加诊断键
        (window/capture/ocr;unread 在像素链下可为 None——徽标不可见时如实)。
    """
    from . import pixel

    return pixel.list_sessions(config, limit)


def read_messages(config: BridgeConfig, chat_id: str, k: int | None = None) -> dict[str, object]:
    """``messages read`` 实现(Phase C2:D2 定论后 = 像素链,委托 :mod:`.pixel`)。

    静默硬边界(像素链不能点击切换会话):读到的是**当前打开会话**,载荷
    ``chat.match`` 如实回报请求 id 与可见标题匹配结果。
    """
    from . import pixel

    return pixel.read_messages(config, chat_id, k)


def send_text(config: BridgeConfig, chat_id: str, body: str) -> dict[str, object]:
    """``send_text`` 实现位(Phase D1/D2:AX 定位发送框 → AXConfirm/AXPress +
    回执验证;调用方已过频控占位门——``SendRateState.reserve_send`` 检查+落戳
    同临界区,并发封闭。本函数契约 = **只在未发出时**抛 BridgeError(调用方
    据此 rollback_reserve 还原占位),发出即成功返回,失败不得发生在真实
    AX 发送之后——否则还原占位会放开 10s 内的第二发,踩 G6 红线)。"""
    raise not_implemented("send_text", "Phase D1")
