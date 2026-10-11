"""UI 通道 AX 层骨架(task 10-11-wechat-ui-bridge Phase C/D 落点位)。

本模块当前只承载**前置检查门**(:func:`ensure_ui_preconditions`)——进程
在、AX 权限在、主窗口开,按 §6 码序 fail-fast;真正的 AX 树遍历/动作驱动
归 Phase C(读)与 Phase D(写),到位于本文件扩展,**不另起模块路径**
(MYIA 侧按 CLI 契约调用,内部模块布局是桥自己的事)。

实现层未落地时的应答纪律:结构化 :class:`BridgeError`(exit 1,通用失败
段,``code="not_implemented"``)——**绝不谎报为任何 §6 具名族**(把「还没
实现」伪装成 ax_tree_empty/window_closed 之类会把 MYIA 侧三态与修复指引
带偏)。

静默铁律(prd 红线 4)对本模块的约束,落地 Phase C/D 时同样生效:
只走 AX 属性读 + AXPress/AXConfirm 类动作;禁合成鼠标事件、禁激活窗口、
禁抢前台焦点。像素链兜底(AX 空树 → 截屏 + local-ocr)属 Phase C3,同样
不得违反静默铁律(screencapture 不需要窗口在前台)。
"""

from __future__ import annotations

from typing import Callable

from .codes import (
    AX_PERMISSION_DENIED,
    WECHAT_NOT_RUNNING,
    WINDOW_CLOSED,
    EXIT_GENERIC_FAILURE,
    BridgeError,
)
from .config import BridgeConfig

__all__ = ["ensure_ui_preconditions", "not_implemented"]

#: 骨架过渡码(design §6 表外唯一过渡态;Phase C/D 落地即消亡)。
NOT_IMPLEMENTED_CODE = "not_implemented"


def ensure_ui_preconditions(
    *,
    process_running: Callable[[], bool] | None = None,
    ax_trusted: Callable[[], bool | None] | None = None,
    window_open: Callable[[], bool | None] = None,
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

    if not process():
        raise BridgeError(
            WECHAT_NOT_RUNNING,
            "微信进程不在运行,UI 通道无对象可驱",
            fix_hint="启动微信客户端后重试",
        )
    if trusted() is False:
        raise BridgeError(
            AX_PERMISSION_DENIED,
            "辅助功能权限缺失:桥宿主进程未被授权读取/驱动 AX 树",
            fix_hint="系统设置 → 隐私与安全性 → 辅助功能,给 MYIA(或桥宿主进程)授权",
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
    """``sessions list`` 实现位(Phase C1:AX 读会话列表,名称+未读数)。"""
    raise not_implemented("sessions list", "Phase C1")


def read_messages(config: BridgeConfig, chat_id: str, k: int | None = None) -> dict[str, object]:
    """``messages read`` 实现位(Phase C2:AX 读最近 K 条文本;媒体落类型占位)。"""
    raise not_implemented("messages read", "Phase C2")


def send_text(config: BridgeConfig, chat_id: str, body: str) -> dict[str, object]:
    """``send_text`` 实现位(Phase D1/D2:AX 定位发送框 → AXConfirm/AXPress +
    回执验证;调用方已过频控门,本函数只在真发送成功后经 SendRateState.record_send
    落时间戳)。"""
    raise not_implemented("send_text", "Phase D1")
