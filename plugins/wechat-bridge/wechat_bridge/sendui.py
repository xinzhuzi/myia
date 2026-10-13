"""send_text 真身:热激活 UI 驱动层(wxauto 三支柱;task 10-13,0.7.0)。

历史定位:Phase D1 原按 A1 第三案收口(官方 iLink 桥独任,UI 写如实报
不可用)。**2026-10-13 主人令翻案**:热激活实验范围已批(本 workflow 使命;
红线=不注入 dylib、不重签名、不 hook 拦截),mac 4.1.15 无 iLink 等价物,
send_text 按 wxauto 三支柱在本层实装——激活微信 + Cmd+F 定位会话 + 剪贴板
粘正文 + 回车,键盘事件全走 CGEvent(ctypes 直调 CoreGraphics,零新增依赖)。

wxauto 三支柱(一条不可少):

① 焦点/状态断言 —— 前台断言(osascript System Events frontmost)、会话
   定位断言(截窗 OCR 标题带与请求 id 空白不敏感互含,pixel._chat_match
   同款)、粘贴前输入区就位经支柱②回读事后证实;
② 粘后回读确认 —— 先 pbpaste 对账剪贴板本体,再读输入区:AX 焦点元素
   value(osascript;灯亮时精确)优先,OCR 输入带(截窗+裁剪+VisionOCR,
   0.14s 级)兜底;两路都取不到正文 → 断言失败;
③ 超时报错绝不假成功 —— 全部等待有硬超时(模块常量);断言失败整尝试
   重试上限 :data:`MAX_ATTEMPTS`(3),仍败抛 BridgeError(exit 15/30,
   阶段与原因如实入 message)。回车(key flags=0)**只在回读确认后按下、
   全程至多一次**;发出后不再抛错(ax.py 契约:BridgeError 只在未发出时
   抛——发出后抛错会诱发 rollback_reserve 放开 10s 内第二发,踩 G6 红线),
   发送后消息区 OCR 回读结果如实入载荷 ``post_send_verified``。

G6 频控不在本层(调用方 cli.py 已接 ``SendRateState.reserve_send`` 占位
原语:检查+落戳同临界区,失败 rollback);本层的本份=**只在未发出时抛错**。

错误码映射(§6 封闭表,不新增码):激活/定位/回读断言失败 → 15
send_ax_focus_required(message 带阶段);子进程挂起(osascript/pbcopy)
→ 30 timeout。OCR 长正文局限:输入带 OCR 对超长正文按首尾段对账
(:data:`READBACK_EDGE_CHARS`),AX value 路径恒全量精确。

静默铁律豁免如实记录:本模块**会**激活微信并抢前台焦点、**会**合成键盘
事件(合成鼠标仍禁)——主人 2026-10-13 热激活批令,读通道(pixel)静默
铁律不变。组件戳 redlines 已同步披露。

单测纪律(design §8):平台原语全部是模块级小函数 = 注入点,
tests/wechat-bridge/test_send_ui.py 全 mock;真机冒烟走
``MYIA_WECHAT_E2E=1`` 门控(下一阶段)。
"""

from __future__ import annotations

import re
import shutil
import subprocess
import tempfile
import time
from pathlib import Path
from typing import Any, Callable

from .codes import SEND_AX_FOCUS_REQUIRED, TIMEOUT, BridgeError
from .config import BridgeConfig

__all__ = ["MAX_ATTEMPTS", "send_text"]

# ------------------------------------------------------------- 节流参数 ----
#: 单次 send_text 的总尝试上限(断言失败整尝试重试;回车只在尝试内确认后)。
MAX_ATTEMPTS = 3

# ------------------------------------------------------------- 等待上限 ----
ACTIVATE_TIMEOUT_S = 6.0
ACTIVATE_POLL_S = 0.25
SEARCH_SETTLE_S = 0.8
KEY_PRESS_GAP_S = 0.05
CLIPBOARD_SETTLE_S = 0.2
TITLE_MATCH_TIMEOUT_S = 8.0
TITLE_POLL_S = 0.6
CLEAR_SETTLE_S = 0.2
PASTE_SETTLE_S = 0.4
READBACK_TIMEOUT_S = 4.0
READBACK_POLL_S = 0.4
POST_SEND_SETTLE_S = 1.2
POST_SEND_TIMEOUT_S = 6.0
POST_SEND_POLL_S = 0.8
#: 平台子进程超时上限(osascript/pbcopy;挂起 → exit 30,同 system_checks 惯例)。
SUBPROC_TIMEOUT_S = 10.0
#: 断言失败后的整尝试重试退避(窗口态/剪贴板稳定窗;末次失败后不等)。
RETRY_BACKOFF_S = 1.0

# ------------------------------------------------------------- OCR 区域 ----
#: 会话标题带(窗口顶部;pixel.TITLE_MAX_Y 放宽一档,搜索态标题在顶栏)。
TITLE_BAND_BOX = (0.0, 0.0, 1.0, 0.10)
#: 输入带(窗口底部;微信 4.x 输入区约在下 1/4,上缘放至 0.72 兜多行回绕)。
INPUT_STRIP_BOX = (0.0, 0.72, 1.0, 0.94)
#: 消息区(发送后回读;不含标题带与输入带)。
MESSAGE_AREA_BOX = (0.0, 0.12, 1.0, 0.70)
#: OCR 长正文对账:超过此长度的正文只验首尾段(输入框内回绕滚动,中段可能
#: 不可见;AX value 路径不受此限恒全量)。
READBACK_EDGE_CHARS = 80

# --------------------------------------------------------- CGEvent 键码 ----
KEY_RETURN = 0x24
KEY_A = 0x00
KEY_F = 0x03
KEY_V = 0x09
KEY_DELETE = 0x33
KEY_DOWN_ARROW = 0x7D
#: kCGEventFlagCommand(NX_COMMANDMASK)。
FLAG_COMMAND = 0x00000100
#: kCGHIDEventTap(会话级注入点;wxauto 同层)。
HID_EVENT_TAP = 0

_WECHAT_BUNDLE_ID = "com.tencent.xinWeChat"
#: frontmost 判定名(System Events 进程名两形态;system_checks 同款)。
_FRONTMOST_NAMES = ("微信", "WeChat")

# ------------------------------------------------------------ 注入点 --------
#: 时钟/睡眠注入(单测不真等;golden 确定性也靠它)。
monotonic: Callable[[], float] = time.monotonic
sleep: Callable[[float], None] = time.sleep

_CG_LIB: Any = None
_CF_LIB: Any = None


def _coregraphics() -> Any:
    """CoreGraphics 句柄(懒加载缓存;ctypes 直调,零 pyobjc 依赖)。"""
    global _CG_LIB
    if _CG_LIB is None:
        import ctypes

        lib = ctypes.CDLL(
            "/System/Library/Frameworks/CoreGraphics.framework/CoreGraphics"
        )
        lib.CGEventCreateKeyboardEvent.restype = ctypes.c_void_p
        lib.CGEventCreateKeyboardEvent.argtypes = [
            ctypes.c_void_p,
            ctypes.c_uint16,
            ctypes.c_bool,
        ]
        lib.CGEventSetFlags.argtypes = [ctypes.c_void_p, ctypes.c_uint64]
        lib.CGEventPost.argtypes = [ctypes.c_uint32, ctypes.c_void_p]
        _CG_LIB = lib
    return _CG_LIB


def _release(event: int | None) -> None:
    """CFRelease 事件对象(best-effort;失败不拦发送路径)。"""
    if not event:
        return
    global _CF_LIB
    try:
        import ctypes

        if _CF_LIB is None:
            _CF_LIB = ctypes.CDLL(
                "/System/Library/Frameworks/CoreFoundation.framework/"
                "CoreFoundation"
            )
            _CF_LIB.CFRelease.argtypes = [ctypes.c_void_p]
        _CF_LIB.CFRelease(ctypes.c_void_p(event))
    except Exception:  # noqa: BLE001 - 释放失败=微小泄漏,进程即退
        pass


def post_key(key_code: int, flags: int = 0) -> None:
    """合成单键(down+up 各一,flags 同设;CGEvent → HID tap)。

    权限事实:宿主进程缺辅助功能/输入监控授权时 CGEventPost 对他 app 无效
    ——本函数不报错(事件被丢),由上层断言(前台/标题/回读)兜住并以
    exit 15 如实失败,绝不假成功。
    """
    lib = _coregraphics()
    down = lib.CGEventCreateKeyboardEvent(None, key_code, True)
    up = lib.CGEventCreateKeyboardEvent(None, key_code, False)
    try:
        lib.CGEventSetFlags(down, flags)
        lib.CGEventSetFlags(up, flags)
        lib.CGEventPost(HID_EVENT_TAP, down)
        sleep(KEY_PRESS_GAP_S)
        lib.CGEventPost(HID_EVENT_TAP, up)
    finally:
        _release(down)
        _release(up)


def _run(argv: list[str], *, input_bytes: bytes | None = None) -> subprocess.CompletedProcess[bytes]:
    """平台子进程(osascript/pbcopy/pbpaste;超时 kill → exit 30)。"""
    try:
        return subprocess.run(  # noqa: S603 - argv 白名单字面量,无外壳
            argv,
            input=input_bytes,
            capture_output=True,
            timeout=SUBPROC_TIMEOUT_S,
            check=False,
        )
    except subprocess.TimeoutExpired as exc:
        raise BridgeError(
            TIMEOUT,
            f"平台子进程超时({' '.join(argv[:2])}…,{SUBPROC_TIMEOUT_S:.0f}s 未退出,已 kill)",
            fix_hint="重试;持续超时说明 osascript/pbcopy 层挂起,查系统日志",
        ) from exc


def activate_wechat() -> None:
    """激活微信(osascript activate;热激活批令内的显式抢焦点)。"""
    result = _run(
        ["osascript", "-e", f'tell application id "{_WECHAT_BUNDLE_ID}" to activate']
    )
    if result.returncode != 0:
        raise BridgeError(
            SEND_AX_FOCUS_REQUIRED,
            "激活微信失败(osascript 非零退出)",
            fix_hint="确认 /Applications/WeChat.app 在位且可启动;重试",
        )


def frontmost_is_wechat() -> bool:
    """前台断言:System Events frontmost 进程名 ∈ {微信, WeChat}。

    查询失败(权限/无进程)→ False 如实——测不了不等于在前台。
    """
    result = _run(
        [
            "osascript",
            "-e",
            'tell application "System Events" to get name of first '
            "application process whose frontmost is true",
        ]
    )
    if result.returncode != 0:
        return False
    name = result.stdout.decode("utf-8", "replace").strip()
    return name in _FRONTMOST_NAMES


def set_clipboard_text(text: str) -> None:
    """剪贴板写入(pbcopy;UTF-8 直传,零转义面)。"""
    result = _run(["pbcopy"], input_bytes=text.encode("utf-8"))
    if result.returncode != 0:
        raise BridgeError(
            SEND_AX_FOCUS_REQUIRED,
            "剪贴板写入失败(pbcopy 非零退出)",
            fix_hint="重试;持续失败查 pbcopy 在位(标配工具)",
        )


def clipboard_text() -> str | None:
    """剪贴板读回(pbpaste;非文本内容/失败 → None 如实,不臆测)。"""
    result = _run(["pbpaste"])
    if result.returncode != 0:
        return None
    return result.stdout.decode("utf-8", "replace")


def ax_focused_value() -> str | None:
    """AX 焦点元素 value(osascript System Events;微信 4.1.15 聊天输入区
    对 AX 基本零暴露——本原语可用时是精确回读,不可用 → None 走 OCR 兜底)。"""
    script = (
        "on run\n"
        '  tell application "System Events"\n'
        '    repeat with pname in {"微信", "WeChat"}\n'
        "      try\n"
        "        tell process (pname as text)\n"
        "          try\n"
        "            return (value of focused element) as text\n"
        "          on error\n"
        '            return ""\n'
        "          end try\n"
        "        end tell\n"
        "      end try\n"
        "    end repeat\n"
        "  end tell\n"
        '  return ""\n'
        "end run"
    )
    result = _run(["osascript", "-e", script])
    if result.returncode != 0:
        return None
    return result.stdout.decode("utf-8", "replace")


# --------------------------------------------------------------- 文本对账 ----


def _squash(text: str) -> str:
    """空白不敏感形态(OCR 行距/换行/全半角空格噪声全压掉)。"""
    return re.sub(r"\s+", "", text)


def text_confirmed(haystack: str, body: str) -> bool:
    """回读对账:正文(空白不敏感)在 haystack 内。

    长正文(> :data:`READBACK_EDGE_CHARS` 压缩后)只验首尾段——输入框
    内部滚动会让中段不可见;首尾两段都在场=粘贴完整的最小诚实证据。
    空正文恒 False(调用方 usage 门已拒空,防御性兜底)。
    """
    want = _squash(body)
    if not want:
        return False
    have = _squash(haystack)
    if not have:
        return False
    if len(want) <= READBACK_EDGE_CHARS:
        return want in have
    head, tail = want[:READBACK_EDGE_CHARS], want[-READBACK_EDGE_CHARS:]
    return head in have and tail in have


def _title_matches(visible: str, chat_id: str) -> bool:
    """定位断言:标题带 OCR 文本与请求 id 互含(pixel._chat_match 同款语义,
    本层自持实现避免私符号跨模块引用)。"""
    from .pixel import _chat_match

    return bool(_chat_match(chat_id, visible or None))


# --------------------------------------------------------------- 截窗 OCR ----


def _ocr_region(window: Any, box: tuple[float, float, float, float], workdir: Path, tag: str) -> str:
    """截窗 → 归一化框裁剪 → VisionOCR → 拼接文本(0.14s 级,OCR 链复用
    :mod:`.pixel`;截图件落 0700 工作目录,调用方统一清理——红线 6)。"""
    from . import pixel

    shot = workdir / f"{tag}.png"
    pixel.capture_window(window, shot)
    cropped = workdir / f"{tag}-crop.png"
    pixel._crop(shot, box, cropped)
    _engine, lines, _elapsed = pixel.vision_ocr(cropped)
    return "\n".join(line.text for line in lines)


def _find_window() -> Any:
    """主窗定位(pixel.find_main_window;None → 断言失败如实)。"""
    from . import pixel

    return pixel.find_main_window()


def _fresh_workdir() -> Path:
    """0700 私有工作目录(截图含聊天内容,用后即清——红线 6)。"""
    import os

    path = Path(tempfile.mkdtemp(prefix="wechat-bridge-send-"))
    os.chmod(path, 0o700)
    return path


# --------------------------------------------------------------- 轮询器 ----


def _wait_until(predicate: Callable[[], bool], *, timeout_s: float, poll_s: float, stage: str) -> None:
    """有界轮询(predicate True 返回;超时 → BridgeError 15 带 stage)。"""
    deadline = monotonic() + timeout_s
    while True:
        try:
            if predicate():
                return
        except BridgeError:
            if monotonic() >= deadline:
                raise
        else:
            if monotonic() >= deadline:
                break
        sleep(poll_s)
    raise BridgeError(
        SEND_AX_FOCUS_REQUIRED,
        f"发送断言超时(阶段={stage},{timeout_s:.0f}s 内未达成)",
        fix_hint="确认微信前台可见、目标会话存在且输入区可聚焦;辅助功能/输入监控授权给桥宿主后重试",
    )


# --------------------------------------------------------------- 单尝试 ----


def _attempt_send(chat_id: str, body: str, workdir: Path) -> str:
    """一次完整尝试:激活 → 定位 → 粘贴 → 回读(**不**回车)。

    Returns:
        回读通路(``"ax_value"`` / ``"ocr_strip"``)——外层据此回车。

    Raises:
        BridgeError: exit 15(激活/定位/回读断言失败,阶段入 message)/
        exit 30(子进程挂起)。**本函数绝不回车**,回车权在外层回读确认后。
    """

    def stage_fail(stage: str, detail: str) -> BridgeError:
        return BridgeError(
            SEND_AX_FOCUS_REQUIRED,
            f"发送断言失败(阶段={stage}):{detail}",
            fix_hint="重试由桥自动进行(上限 3 次);持续失败检查微信前台态/会话名/辅助功能授权",
        )

    # —— ① 激活 + 前台断言 ——
    activate_wechat()
    _wait_until(
        frontmost_is_wechat,
        timeout_s=ACTIVATE_TIMEOUT_S,
        poll_s=ACTIVATE_POLL_S,
        stage="activate",
    )

    window = _find_window()
    if window is None:
        raise stage_fail("window", "CGWindowList 无微信主窗(前置门放行后窗口消失)")

    # —— ② 定位会话:Cmd+F → 粘贴会话名 → ↓ → 回车 → 标题带断言 ——
    set_clipboard_text(chat_id)
    sleep(CLIPBOARD_SETTLE_S)
    post_key(KEY_F, FLAG_COMMAND)
    sleep(SEARCH_SETTLE_S)
    post_key(KEY_V, FLAG_COMMAND)
    sleep(SEARCH_SETTLE_S)
    post_key(KEY_DOWN_ARROW)
    sleep(KEY_PRESS_GAP_S)
    post_key(KEY_RETURN)
    _wait_until(
        lambda: _title_matches(_ocr_region(window, TITLE_BAND_BOX, workdir, "title"), chat_id),
        timeout_s=TITLE_MATCH_TIMEOUT_S,
        poll_s=TITLE_POLL_S,
        stage="locate",
    )

    # —— ③ 粘正文:先清残留(Cmd+A+Delete,best-effort)再粘 ——
    post_key(KEY_A, FLAG_COMMAND)
    sleep(KEY_PRESS_GAP_S)
    post_key(KEY_DELETE)
    sleep(CLEAR_SETTLE_S)
    set_clipboard_text(body)
    sleep(CLIPBOARD_SETTLE_S)
    post_key(KEY_V, FLAG_COMMAND)
    sleep(PASTE_SETTLE_S)

    # —— ④ 支柱②回读:剪贴板本体对账(pbpaste 有 clipboardd 延迟,短轮询)
    #    → AX value → OCR 输入带 ——
    def clipboard_ok() -> bool:
        current = clipboard_text()
        return current is not None and _squash(current) == _squash(body)

    for _probe in range(3):
        if clipboard_ok():
            break
        sleep(0.2)
    else:
        raise stage_fail("clipboard", "粘贴后剪贴板读回与正文不符(写入被夺/系统忙碌)")

    readback_path: list[str] = []

    def input_confirmed() -> bool:
        ax_value = ax_focused_value()
        if ax_value is not None and text_confirmed(ax_value, body):
            readback_path.append("ax_value")
            return True
        strip = _ocr_region(window, INPUT_STRIP_BOX, workdir, "input")
        if text_confirmed(strip, body):
            readback_path.append("ocr_strip")
            return True
        return False

    _wait_until(
        input_confirmed,
        timeout_s=READBACK_TIMEOUT_S,
        poll_s=READBACK_POLL_S,
        stage="readback",
    )
    return readback_path[-1]


# ------------------------------------------------------------- 发送后回读 ----


def _post_send_verify(body: str, workdir: Path) -> dict[str, Any]:
    """发送后回读(消息区 OCR):**绝不抛错**(ax.py 契约:发出后失败不得
    触发 rollback——G6);结果如实入载荷,末次中断原因不吞。"""
    deadline = monotonic() + POST_SEND_TIMEOUT_S
    last_error: BridgeError | None = None
    while True:
        try:
            window = _find_window()
            if window is not None:
                area = _ocr_region(window, MESSAGE_AREA_BOX, workdir, "sent")
                if text_confirmed(area, body):
                    return {"post_send_verified": True, "post_send_note": None}
        except BridgeError as exc:
            last_error = exc
        if monotonic() >= deadline:
            break
        sleep(POST_SEND_POLL_S)
    if last_error is not None:
        return {
            "post_send_verified": False,
            "post_send_note": f"消息区回读中断({last_error.name}):发送键已按下,未能复核",
        }
    return {
        "post_send_verified": False,
        "post_send_note": "消息区 OCR 未见正文(渲染延迟或区域裁剪误差):发送键已按下,输入带回读已确认",
    }


# ------------------------------------------------------------------ 主口 ----


def send_text(config: BridgeConfig, chat_id: str, body: str) -> dict[str, Any]:
    """``send_text`` 实现(热激活 UI 驱动;wxauto 三支柱,见模块 docstring)。

    Returns:
        ``{"send": {"chat", "sent": True, "attempts", "readback",
        "post_send_verified", "post_send_note", "elapsed_ms"}}``——载荷只
        载形状与通路,永不载正文(红线 6)。

    Raises:
        BridgeError: **只在未发出时**(exit 15 断言族 / 30 子进程超时);
        回车按下后不再抛(契约见 ax.py send_text docstring,G6 方向)。
    """
    started = monotonic()
    original_clipboard = clipboard_text()
    workdir = _fresh_workdir()
    attempts_used = 0
    readback = "ocr_strip"
    last_error: BridgeError | None = None
    try:
        for attempt_index in range(MAX_ATTEMPTS):
            attempts_used += 1
            try:
                readback = _attempt_send(chat_id, body, workdir)
                last_error = None
                break
            except BridgeError as exc:
                last_error = exc
                if attempt_index < MAX_ATTEMPTS - 1:
                    sleep(RETRY_BACKOFF_S)
        if last_error is not None:
            raise BridgeError(
                last_error.exit_code,
                f"发送未执行:{MAX_ATTEMPTS} 次尝试均未通过断言;"
                f"末次失败 {last_error.message}",
                fix_hint=last_error.fix_hint,
                retry_after_seconds=last_error.retry_after_seconds,
            )
        # —— 确认无误才回车(flags=0;全函数唯一的发送动作)——
        post_key(KEY_RETURN)
        sleep(POST_SEND_SETTLE_S)
        verdict = _post_send_verify(body, workdir)
    finally:
        # 剪贴板复原(best-effort:原内容非文本/空 → 清空,不留正文)。
        try:
            if original_clipboard:
                set_clipboard_text(original_clipboard)
            else:
                set_clipboard_text("")
        except BridgeError:
            pass  # 复原失败不拦发送结果(载荷如实,剪贴板残留正文可接受)
        shutil.rmtree(workdir, ignore_errors=True)  # 截图件即清(红线 6)
    return {
        "send": {
            "chat": chat_id,
            "sent": True,
            "attempts": attempts_used,
            "readback": readback,
            **verdict,
            "elapsed_ms": round((monotonic() - started) * 1000),
        }
    }
