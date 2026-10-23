"""UI 通道实现层(task 10-11-wechat-ui-bridge Phase C/D 落点位)。

**Phase C 读通道已按 D2 定论改写为像素链**(A1 实测微信 4.1.15 聊天内容层
对 AX 完全零暴露,证据 research/ax-probe-4.1.15.md):``sessions list`` /
``messages read`` 委托 :mod:`.pixel`(截窗 → VisionOCR → VL 校对 → 结构化
解析;静默铁律全套:零激活、零合成点击、零抢焦点)。原「AX 树遍历」实现
整体作废。

**Phase D1 写通道已落(0.7.0;0.8.0 三源合体升级)**:``send_text`` 委托
:mod:`.sendui`(分区过滤导航零盲回车 + 验证五件套 + AX 主链/CGEvent+OCR
降级 + localdb 回执终验;详见 sendui 模块 docstring);
``not_implemented`` 过渡应答仅作 API 兼容保留(C/D 全落,过渡码消亡)。

静默铁律(prd 红线 4)对本模块的约束:
读=像素链(screencapture -l 对后台窗口零交互,ordered-off 窗可截,
2026-10-11 实测)——**不变**;写=**2026-10-13 主人令翻案**:热激活实验
范围已批(不注入 dylib、不重签名、不 hook 拦截),send_text 按 wxauto
三支柱实装(激活+Cmd+F 定位+剪贴板粘+回读确认才回车),落
:mod:`.sendui`;原「官方 iLink 桥独任」第三案与「UI 写如实报不可用」
的旧 D1 收口自此作废(合成鼠标仍禁)。
"""

from __future__ import annotations

from typing import Any, Callable

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


def send_text(
    config: BridgeConfig,
    target: Any,
    body: str,
    *,
    dry_run: bool = False,
    on_armed: Callable[[], None] | None = None,
    on_receipt_green: Callable[[], None] | None = None,
    receipt_query: Callable[[str, str, float], bool | None] | None = None,
) -> dict[str, object]:
    """``send_text`` 实现(0.8.0 三源合体,委托 :mod:`.sendui`)。

    契约 = **只在未发出时**抛 BridgeError(调用方据此 rollback_reserve
    还原占位);发出即成功返回,失败不得发生在真实回车之后——否则还原
    占位会放开 10s 内的第二发,踩 G6 红线。

    on_armed 边界条款(design §C-4/§C-5):on_armed(= 落指纹 pending,
    回车 down 前回调)**失败 = fail-closed 上抛**(未回车,调用方可
    rollback 重试);armed 之后的一切异常在 sendui 内吞掉(聚焦终败的
    exit 15 error 载荷除外——已 pending 不该 rollback,调用方以 armed
    闭包标志区分,cli.py 同款)。

    Args:
        target: :class:`.sendtarget.SendTarget`(DB 侧解析产物)。
        dry_run: 走到粘贴回读即收尾,零发送零频控副作用。
        on_armed / on_receipt_green / receipt_query: 见 :func:`.sendui.
            send_text`(指纹状态机回调与回执判定闭包,CLI 注入)。
    """
    from . import sendui

    return sendui.send_text(
        config,
        target,
        body,
        dry_run=dry_run,
        on_armed=on_armed,
        on_receipt_green=on_receipt_green,
        receipt_query=receipt_query,
    )
