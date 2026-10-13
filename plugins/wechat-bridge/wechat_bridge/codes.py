"""桥 CLI 错误码表(task 10-11-wechat-ui-bridge design §6;执行者零设计,照表实现)。

exit 三段语义对齐 ``src/myssia/push/weixin.py`` 桥接 Hermes 的惯例:0 成功 /
1 通用失败(结构化 error 载荷)/ 2 用法错;§6 把失败段细化为具名错误族
(10-30),MYIA 侧按码映射 UI 文案与三态。**本表封闭**:新错误族须先改
design §6 再进这里,不许执行侧顺手加码。

骨架态的过渡码:四子命令的 AX/本地库实现层归 Phase C/D/E(design §9 依赖
图,B 与之并行),前置检查全绿但实现层未落地时,以 exit 1 + ``code=
"not_implemented"`` 如实应答(不谎报为任何 §6 具名族);Phase C/D/E 落地
后该过渡码随之消亡。
"""

from __future__ import annotations

from dataclasses import dataclass

__all__ = [
    "AX_PERMISSION_DENIED",
    "SCREEN_RECORDING_DENIED",
    "AX_TREE_EMPTY",
    "DB_NOT_FOUND",
    "DECRYPT_FAILED",
    "KEY_UNAVAILABLE",
    "SEND_AX_FOCUS_REQUIRED",
    "SEND_RATE_LIMITED",
    "SEND_UNCERTAIN_DEDUP",
    "MEDIA_UNAVAILABLE",
    "TIMEOUT",
    "USAGE",
    "WECHAT_NOT_RUNNING",
    "WINDOW_CLOSED",
    "EXIT_OK",
    "EXIT_GENERIC_FAILURE",
    "EXIT_USAGE",
    "BridgeError",
]

# —— 成功与三段骨架(design §6 调用形态:exit 三段语义)——
EXIT_OK = 0
#: 通用失败段(结构化 error 载荷在 stdout JSON;weixin.py 桥接惯例 0/1/2)。
EXIT_GENERIC_FAILURE = 1
#: 参数/用法错(§6 表;含配置文件 schema 拒载——fail-fast 于配置的家规)。
EXIT_USAGE = 2

# —— §6 具名错误族(exit == 码值;名字即表中码名列)——
USAGE = 2
WECHAT_NOT_RUNNING = 10
AX_PERMISSION_DENIED = 11
#: 屏幕录制权限缺失(2026-10-13 勘误:像素链前置门真实权限;与 AX 同属权限族复用码值 11,通道侧 screen_recording_denied 已映射 11)
SCREEN_RECORDING_DENIED = 16
WINDOW_CLOSED = 12
AX_TREE_EMPTY = 13
SEND_RATE_LIMITED = 14
SEND_AX_FOCUS_REQUIRED = 15
#: §6 修订 2026-10-14(task 10-14-wechat-send-text design §E-4):17 = 指纹
#: pending 命中,上次同指纹发送状态不确定,**绝不自动重试**
#: (uncertain-never-retry;与 14「可等后重试」语义分开编程)。
SEND_UNCERTAIN_DEDUP = 17
DB_NOT_FOUND = 20
KEY_UNAVAILABLE = 21
DECRYPT_FAILED = 22
#: 媒体解密件未配置/不可用(design §6 修订 2026-10-14,task
#: 10-14-wechat-media-sns:媒体面结构化降级,文本链零影响)。media.py 的
#: try-import fallback 同值 23,键落位后接线前后行为一致。
MEDIA_UNAVAILABLE = 23
TIMEOUT = 30

#: exit 码 → 码名(§6 表的程序化形态;MYIA 侧/UI 文案映射与单测对账用)。
CODE_NAMES: dict[int, str] = {
    USAGE: "usage",
    WECHAT_NOT_RUNNING: "wechat_not_running",
    AX_PERMISSION_DENIED: "ax_permission_denied",
    SCREEN_RECORDING_DENIED: "screen_recording_denied",  # 16(独立码;11 复用会顶名字,实测教训)
    WINDOW_CLOSED: "window_closed",
    AX_TREE_EMPTY: "ax_tree_empty",
    SEND_RATE_LIMITED: "send_rate_limited",
    SEND_AX_FOCUS_REQUIRED: "send_ax_focus_required",
    SEND_UNCERTAIN_DEDUP: "send_uncertain_dedup",
    DB_NOT_FOUND: "db_not_found",
    KEY_UNAVAILABLE: "key_unavailable",
    DECRYPT_FAILED: "decrypt_failed",
    MEDIA_UNAVAILABLE: "media_unavailable",  # 23(2026-10-14 design §6 修订)
    TIMEOUT: "timeout",
}


@dataclass(frozen=True)
class BridgeError(Exception):
    """桥内结构化错误:exit 码 + 码名 + 人读原因 + 修复指引。

    ``code`` 缺省由 exit 码查 :data:`CODE_NAMES`;骨架过渡码
    ``not_implemented`` 显式传入(exit=1 通用失败段)。所有字段均可直接
    进 stdout JSON 的 ``error`` 节;**消息只承载形状与指引,永不承载聊天
    内容/密钥材料**(prd 红线 6)。
    """

    exit_code: int
    message: str
    code: str | None = None
    fix_hint: str | None = None
    #: 频控拒发专属(§6:应答含 retry_after_seconds);其余族恒 None。
    retry_after_seconds: float | None = None

    def __post_init__(self) -> None:
        # Exception 的 args 需非空才有像样的 str();放消息本身。
        super().__init__(self.message)

    @property
    def name(self) -> str:
        """码名:具名族查表,过渡/未知码用显式 ``code``(缺省字面量)。"""
        if self.code is not None:
            return self.code
        return CODE_NAMES.get(self.exit_code, f"exit_{self.exit_code}")

    def to_payload(self) -> dict[str, object]:
        """stdout JSON 的 ``error`` 节(键序稳定,golden 基件对账用)。"""
        payload: dict[str, object] = {"code": self.name, "message": self.message}
        if self.fix_hint is not None:
            payload["fix_hint"] = self.fix_hint
        if self.retry_after_seconds is not None:
            payload["retry_after_seconds"] = self.retry_after_seconds
        return payload
