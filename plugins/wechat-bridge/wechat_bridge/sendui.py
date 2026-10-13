"""send_text 真身:三源合体 UI 驱动层(task 10-14-wechat-send-text;
0.7.0 wxauto 三支柱 → 0.8.0 升级)。

三源合体(design §0;蓝本 = 任务档 research/ 三份):

- **tonyshield**(ref_search_click.sh):搜索结果面板**分区过滤导航**
  (本地结果分区头锚定 + 垃圾分区排除 + 评分选行)——**零盲回车**:
  旧「Cmd+F → ↓ → Return」键序已删除,``KEY_RETURN`` 全链唯一出现点 =
  发送段 j2 的回车;无候选行 → exit 15 拒发,绝不猜(选行纯逻辑在
  :mod:`.navfilter`)。
- **wechatctl**(wuziyong_wechatctl.swift):**验证五件套**——
  ①标题校验(AX label 直读优先/OCR 标题带兜底/emoji 间接证据链);
  ②composer 哨兵探测(:func:`read_composer_via_clipboard`,只读协议);
  ③发送后清空轮询(12×80ms);④SHA256 指纹防重 120s + uncertain-
  never-retry(落 :mod:`.send_state`,on_armed 落 pending);⑤旧剪贴板
  保存恢复(finally 兜底,哨兵/搜索词的中间覆写全在 try 内)。
- **REV**(FINDINGS.md):AX 主链元素(``chat_input_field``/
  ``current_chat_name_label``/``session_item_*``,经 :mod:`.axui`)。

**通道分层(design §D-1)**:每次尝试开头 ``axui.probe_wechat_ax()``
双判据(全窗最大节点数>5 AND 输入区可读)判定 ``ax`` |
``cgevent_ocr``,单尝试内通道固定;**跨尝试降级**——本尝试失败原语为
AX 能力缺失(返回 False)→ 下一尝试 forced_fallback 直走降级链。降级链
= 剪贴板粘搜索词 + 分区过滤 OCR 选行 + CGEvent 点击(坐标三段换算:
裁剪系 → 全窗 → 屏幕,navfilter)。

**发送前聚焦断言(两通道对称,design §D-2/§J-17)**:AX 路
focus_input + 复读 value==body + focused_is_input 尽力断言;降级链
click_at(COMPOSER_POINT) + 哨兵读一致性(回 None 或 ==body 才算聚焦
成立,回异值 = 焦点落别处)——哨兵协议本身即断言,不是裸点击。聚焦
终败 → exit 15 error 载荷(stage=focus,message 注明「未回车;指纹已
pending,120s 内同指纹重发将 exit 17」,design §J-20,不破
exit 0 ⇒ sent:true 旧契约)。

**fail-closed 门与 armed 段隔离(design §C-5,硬结构)**::

    on_armed() 失败(落指纹 pending 失败)→ 正常上抛(armed 仍 False →
        CLI rollback → 未回车,可安全重试)——指纹没落就绝不进入发送段,
        宁可不发也不开「无指纹却发出」的双发窗;
    armed = True 之后 → 对外恒不抛:聚焦断言失败计入重试/终败 error
        载荷(不上抛 BridgeError 诱发 rollback);发出后一切异常(回执/
        升级 sent/清空轮询)吞掉 + ``fingerprint_note``/``post_send_note``
        如实——上抛会诱发 CLI rollback 放开 10s 内第二发(G6 红线)。

**点击范围收窄(design §B-4 纪律)**:本模块的合成鼠标点击仅
①搜索结果行(导航)、②composer 聚焦点(``COMPOSER_POINT_NORM``)、
③无。不点发送按钮(发送=回车)、不点任何其他 UI。

CGEvent 事件源隔离(0.8.0,WZ:25-41):键盘/鼠标事件均带
kCGEventSourceStateCombinedSessionState 源句柄(模块级缓存;创建失败
回退 None 源如实,不拦发送)。

**0.8.1 真机 dry-run 修正(证据 /tmp/wxsend-e2e/,2026-10-14)**:首测
两目标 dry-run 均止于 navigate 零候选——(a) System Events ``entire
contents`` 在 4.1.15 动态树上返回空(元素重建竞态,-1719),axui 全部
元素原语改 BFS 逐层遍历;(b) 降级链 CGEvent Cmd+F/Cmd+V 未把搜索词带
进 UI(静默丢不可检测)——搜索词改 **AXFocusedUIElement 直写优先**
(REF 同路线)+ 剪贴板 Cmd+V 兜底;非发送键一律走 ``_post_key_dual``
(**System Events keystroke 优先,失败可检测**,宿主缺辅助功能授权时
报错回落 CGEvent 而非静默)。发送回车保持 :func:`post_key` CGEvent
单路(唯一发送动作,零歧义)。

回执终验(红线 4):``receipt_query`` 闭包由 CLI 注入(sendui 零
localdb 依赖,design §A);``RECEIPT_POLL_SCHEDULE`` 退避轮询,累计
~30s 保守覆盖冷重建(design §J-18);``since_epoch`` 取 on_armed 时刻
(wall_clock 注入点);判定含 ``ts > since_epoch - 2`` 防同正文历史
消息假绿(design §C-6)。

错误码映射(§6 封闭表):激活/定位/导航/回读/聚焦断言失败 → 15
send_ax_focus_required;子进程挂起 → 30 timeout;指纹 pending 命中 →
17(CLI 层 reserve_send_dedup)。OCR 长正文局限:输入带 OCR 对超长正文
按首尾段对账(:data:`READBACK_EDGE_CHARS`),AX value 路径恒全量精确。

静默铁律豁免如实记录:本模块**会**激活微信并抢前台焦点、**会**合成
键盘事件与(收窄范围内的)鼠标点击——PRD 2026-10-14 翻案(design
§I-1),读通道(pixel)静默铁律不变。组件戳 redlines 已同步披露。

单测纪律(design §G):平台原语(子进程/ctypes/时钟/AX/OCR)全部是
模块级注入点,tests/wechat-bridge/test_send_ui.py 全 mock;真机矩阵走
``--dry-run`` 与 P10 门控。
"""

from __future__ import annotations

import ctypes
import re
import shutil
import subprocess
import tempfile
import time
import uuid
from pathlib import Path
from typing import Any, Callable

from . import axui, navfilter
from .codes import SEND_AX_FOCUS_REQUIRED, TIMEOUT, BridgeError
from .config import BridgeConfig
from .sendtarget import SendTarget, row_match_terms

__all__ = [
    "MAX_ATTEMPTS",
    "RECEIPT_POLL_SCHEDULE",
    "click_at",
    "post_key",
    "read_composer_via_clipboard",
    "send_text",
    "squash",
]

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

# ----------------------------------------------------- 导航/五件套参数 ----
#: 搜索结果渲染等待上限(两通道共用;轮询 SEARCH_POLL_S)。
SEARCH_RENDER_TIMEOUT_S = 5.0
SEARCH_POLL_S = 0.5
#: 粘搜索词后的渲染静置(降级链)。
SEARCH_RENDER_S = 1.2
#: 结果行点击后的会话切换静置。
CLICK_SETTLE_S = 0.3
#: 哨兵协议各步间隙(WZ:190-197 同参数)。
SENTINEL_GAP_S = 0.06
#: 发送后清空轮询(五件套件 3;WZ:271-277 同参数 12×80ms)。
CLEAR_POLL_TIMES = 12
CLEAR_POLL_GAP_S = 0.08
#: localdb 回执轮询退避表(累计 ~30s,保守覆盖 E2 副本冷重建;design §J-18)。
RECEIPT_POLL_SCHEDULE = (5.0, 10.0, 15.0)
#: composer 聚焦点(窗口内容归一化;INPUT_STRIP_BOX 中心;P9 预验校准项)。
COMPOSER_POINT_NORM = (0.50, 0.83)

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
KEY_C = 0x08  # WZ:194 同键码(哨兵读 Cmd+C 全量复制)
KEY_F = 0x03
KEY_V = 0x09
KEY_DELETE = 0x33
KEY_ESCAPE = 0x35  # dry-run 降级链退出搜索态(design §B-5)
#: kCGEventFlagCommand(NX_COMMANDMASK)。
FLAG_COMMAND = 0x00000100
#: kCGHIDEventTap(会话级注入点;wxauto 同层)。
HID_EVENT_TAP = 0
#: kCGEventSourceStateCombinedSessionState(事件源隔离,WZ:25-41;0.8.0)。
EVENT_SOURCE_COMBINED = 0
#: CGEvent 鼠标事件类型(CoreGraphics 枚举值)。
_MOUSE_MOVED = 5
_MOUSE_LEFT_DOWN = 1
_MOUSE_LEFT_UP = 2

_WECHAT_BUNDLE_ID = "com.tencent.xinWeChat"
#: frontmost 判定名(System Events 进程名两形态;system_checks 同款)。
_FRONTMOST_NAMES = ("微信", "WeChat")

# ------------------------------------------------------------ 注入点 --------
#: 时钟/睡眠注入(单测不真等;golden 确定性也靠它)。
monotonic: Callable[[], float] = time.monotonic
sleep: Callable[[float], None] = time.sleep
#: 墙钟注入(回执 since_epoch 取 on_armed 时刻;单测换假钟,design §C-6)。
wall_clock: Callable[[], float] = time.time

_CG_LIB: Any = None
_CF_LIB: Any = None
_EVENT_SOURCE: Any = None
_event_source_tried = False


class _CGPoint(ctypes.Structure):
    """CGPoint(ctypes 形态;CGEventCreateMouseEvent 坐标参数)。"""

    _fields_ = [("x", ctypes.c_double), ("y", ctypes.c_double)]


def _coregraphics() -> Any:
    """CoreGraphics 句柄(懒加载缓存;ctypes 直调,零 pyobjc 依赖)。"""
    global _CG_LIB
    if _CG_LIB is None:
        lib = ctypes.CDLL(
            "/System/Library/Frameworks/CoreGraphics.framework/CoreGraphics"
        )
        lib.CGEventCreateKeyboardEvent.restype = ctypes.c_void_p
        lib.CGEventCreateKeyboardEvent.argtypes = [
            ctypes.c_void_p,
            ctypes.c_uint16,
            ctypes.c_bool,
        ]
        lib.CGEventSourceCreate.restype = ctypes.c_void_p
        lib.CGEventSourceCreate.argtypes = [ctypes.c_uint32]
        lib.CGEventCreateMouseEvent.restype = ctypes.c_void_p
        lib.CGEventCreateMouseEvent.argtypes = [
            ctypes.c_void_p,
            ctypes.c_uint32,
            _CGPoint,
            ctypes.c_uint32,
        ]
        lib.CGEventSetFlags.argtypes = [ctypes.c_void_p, ctypes.c_uint64]
        lib.CGEventPost.argtypes = [ctypes.c_uint32, ctypes.c_void_p]
        _CG_LIB = lib
    return _CG_LIB


def _event_source() -> Any:
    """CGEventSourceCreate(combinedSessionState) 模块级缓存句柄(WZ:25-31
    事件源隔离;hardened:0.7.0 现状 source=None)。

    失败回退 None 源(事件仍发,不带源隔离)并在 docstring 如实——
    不拦发送。
    """
    global _EVENT_SOURCE, _event_source_tried
    if _event_source_tried:
        return _EVENT_SOURCE
    _event_source_tried = True
    try:
        lib = _coregraphics()
        _EVENT_SOURCE = lib.CGEventSourceCreate(EVENT_SOURCE_COMBINED) or None
    except Exception:  # noqa: BLE001 - 创建失败回退 None 源,如实不拦发送
        _EVENT_SOURCE = None
    return _EVENT_SOURCE


def _release(event: int | None) -> None:
    """CFRelease 事件对象(best-effort;失败不拦发送路径)。"""
    if not event:
        return
    global _CF_LIB
    try:
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
    """合成单键(down+up 各一,flags 同设;CGEvent → HID tap;事件带
    combinedSessionState 源句柄,WZ:25-31 配方)。

    权限事实:宿主进程缺辅助功能/输入监控授权时 CGEventPost 对他 app 无效
    ——本函数不报错(事件被丢),由上层断言(前台/标题/回读)兜住并以
    exit 15 如实失败,绝不假成功。**非发送键一律走 :func:`_post_key_dual`
    (System Events keystroke 优先,失败可检测);本函数保留为发送回车的
    唯一通道与兜底引擎**。
    """
    lib = _coregraphics()
    src = _event_source()
    down = lib.CGEventCreateKeyboardEvent(src, key_code, True)
    up = lib.CGEventCreateKeyboardEvent(src, key_code, False)
    try:
        lib.CGEventSetFlags(down, flags)
        lib.CGEventSetFlags(up, flags)
        lib.CGEventPost(HID_EVENT_TAP, down)
        sleep(KEY_PRESS_GAP_S)
        lib.CGEventPost(HID_EVENT_TAP, up)
    finally:
        _release(down)
        _release(up)


def post_key_stevents(key_code: int, flags: int = 0) -> bool:
    """System Events keystroke 键注入(REF 同路线;0.8.1 引入)。

    与 CGEvent 的差异(真机 dry-run 实证,/tmp/wxsend-e2e/):keystroke
    走 osascript System Events——**宿主缺辅助功能授权时报错可检测**
    (returncode ≠ 0 → 本函数返回 False),而 CGEventPost 是静默丢弃
    (不可检测,搜索词进不了 UI 也无任何错误信号)。仅支持 flags=0 与
    FLAG_COMMAND 两形态,其余旗标组合返回 False(调用方回落 CGEvent)。
    """
    if flags == 0:
        using = ""
    elif flags == FLAG_COMMAND:
        using = " using command down"
    else:
        return False
    result = _run(
        ["osascript", "-e", f'tell application "System Events" to key code {key_code}{using}']
    )
    return result.returncode == 0


def _post_key_dual(key_code: int, flags: int = 0) -> None:
    """非发送键双引擎:keystroke(System Events,REF 对齐,失败可检测)
    优先 → CGEvent 兜底(旧路)。**发送回车不走本函数**(KEY_RETURN
    唯一性:发送动作恒 :func:`post_key` CGEvent 单路,零歧义)。"""
    if not post_key_stevents(key_code, flags):
        post_key(key_code, flags)


def click_at(x: int, y: int) -> None:
    """合成鼠标点击(moved 60ms → down 35ms → up;WZ:33-41 配方,事件带
    combinedSessionState 源,post 到 HID tap)。

    **点击范围收窄纪律(design §B-4,红线)**:仅 ①搜索结果行(导航)、
    ②composer 聚焦点、③无。不点发送按钮(发送=回车)、不点其他 UI。
    """
    lib = _coregraphics()
    src = _event_source()
    point = _CGPoint(float(x), float(y))
    for event_type, gap in ((_MOUSE_MOVED, 0.06), (_MOUSE_LEFT_DOWN, 0.035), (_MOUSE_LEFT_UP, 0.035)):
        event = lib.CGEventCreateMouseEvent(src, event_type, point, 0)
        try:
            lib.CGEventPost(HID_EVENT_TAP, event)
        finally:
            _release(event)
        sleep(gap)


def _composer_point(window: Any) -> tuple[int, int]:
    """composer 聚焦点的屏幕绝对像素(全窗归一化 COMPOSER_POINT_NORM)。"""
    return (
        round(float(window.x) + COMPOSER_POINT_NORM[0] * float(window.width)),
        round(float(window.y) + COMPOSER_POINT_NORM[1] * float(window.height)),
    )


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


# --------------------------------------------------------------- 文本对账 ----


def squash(text: str) -> str:
    """空白不敏感形态(OCR 行距/换行/全半角空格噪声全压掉)。

    回读/回执对账共用(:mod:`.cli` 的 receipt_query 同款);与
    :func:`navfilter.compact`(另加 casefold,用于展示名/行文比对)语义
    分层——对账不折叠大小写,比对折叠。
    """
    return re.sub(r"\s+", "", text)


def text_confirmed(haystack: str, body: str) -> bool:
    """回读对账:正文(空白不敏感)在 haystack 内。

    长正文(> :data:`READBACK_EDGE_CHARS` 压缩后)只验首尾段——输入框
    内部滚动会让中段不可见;首尾两段都在场=粘贴完整的最小诚实证据。
    空正文恒 False(调用方 usage 门已拒空,防御性兜底)。
    """
    want = squash(body)
    if not want:
        return False
    have = squash(haystack)
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


def _has_emoji(text: str) -> bool:
    """display_name 是否含 BMP 之外字符(emoji;中文恒 False)——
    emoji 目标的 OCR 不可读处置走 indirect 证据链(design §D-3)。"""
    return any(ord(ch) > 0xFFFF for ch in text)


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


def _ocr_region_lines(
    window: Any, box: tuple[float, float, float, float], workdir: Path, tag: str
) -> list[Any]:
    """截窗 → 裁剪 → VisionOCR → **OcrLine 列表**(0.8.0 新原语,design
    §J-3:分区过滤选行需要行级坐标;坐标 = 裁剪图归一化 0-1)。"""
    from . import pixel

    shot = workdir / f"{tag}.png"
    pixel.capture_window(window, shot)
    cropped = workdir / f"{tag}-crop.png"
    pixel._crop(shot, box, cropped)
    _engine, lines, _elapsed = pixel.vision_ocr(cropped)
    return list(lines)


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


# ------------------------------------------------------- 内部信号(异常) ----


class _AxCapabilityMissing(Exception):
    """AX 原语返回 False(能力缺失)→ 下一尝试 forced_fallback 直走降级链
    (design §D-1;write_search_value/press_session_item/write_input_value/
    focus_input/read_input_value 族)。内部信号,不上抛出层。"""

    def __init__(self, primitive: str) -> None:
        super().__init__(primitive)
        self.primitive = primitive


class _FocusFail(Exception):
    """聚焦断言失败(发送前;design §1-j1)。内部信号。"""

    def __init__(self, error: BridgeError, ax_missing: bool = False) -> None:
        super().__init__(error.message)
        self.error = error
        self.ax_missing = ax_missing


class _ArmedFailure(Exception):
    """armed(= on_armed 已成功)之后的聚焦断言失败(design §C-4/§1-j1)。

    重试次数内 → 下一尝试(armed 状态已落,不 rollback);耗尽 → 上抛
    exit 15 error 载荷(stage=focus;CLI 层 armed 闭包标志保证不 rollback)。
    """

    def __init__(self, error: BridgeError, ax_missing: bool) -> None:
        super().__init__(error.message)
        self.error = error
        self.ax_missing = ax_missing


# ------------------------------------------------------- 五件套件 2:哨兵 ----


def read_composer_via_clipboard(window: Any) -> str | None:
    """降级链读输入框内容(哨兵探测协议;WZ:190-197 原样移植)。

    只读协议:click_at(composer 点)→ Cmd+A 全选 → 置哨兵 → Cmd+C 复制
    (不改输入框内容)→ 读剪贴板:回哨兵本体 = 输入框空(None);否则 =
    输入框内容(精确全量)。KEY_C = 0x08(WZ:194 同键码)。

    哨兵读会把哨兵留在剪贴板 → 调用方 finally 复原兜底;异常向上抛
    (exit 15/30 族;仅 on_armed 前调用,armed 后由隔离段兜住,§C-5)。
    """
    click_at(*_composer_point(window))
    sleep(SENTINEL_GAP_S)
    _post_key_dual(KEY_A, FLAG_COMMAND)
    sleep(0.03)
    sentinel = f"__MYIA_PROBE_{uuid.uuid4().hex[:8]}__"
    set_clipboard_text(sentinel)
    sleep(0.04)
    _post_key_dual(KEY_C, FLAG_COMMAND)
    sleep(SENTINEL_GAP_S)
    got = clipboard_text()
    return None if got == sentinel else got


# ------------------------------------------------------------ 导航(§B-5) ----


def _navigate(target: SendTarget, window: Any, channel: str, workdir: Path) -> dict[str, Any]:
    """两通道导航(**零盲回车**;旧 ↓+Return 键序已删除)。

    ax 通道:Cmd+F → AXValue 直写搜索词(零剪贴板)→ 轮询找
    session_item_<display_name> 并 AXPress(零坐标)。
    cgevent_ocr 通道:剪贴板粘搜索词 → Cmd+F → Cmd+V → 轮询
    _ocr_region_lines(SEARCH_PANE_BOX) → navfilter.select_result_row
    分区过滤选行 → 坐标三段换算 → click_at(目标行)。

    Returns:
        nav_debug(坐标与规则名,零内容;dry-run 载荷用,P9 预验校准依据)。

    Raises:
        _AxCapabilityMissing: AX 原语 False(降级信号)。
        BridgeError: stage=navigate(超时/零候选——emoji 目标降级链不可达
            是设计内行为,exit 15 拒发,绝不盲回车)。
    """

    def stage_fail(detail: str) -> BridgeError:
        return BridgeError(
            SEND_AX_FOCUS_REQUIRED,
            f"发送断言失败(阶段=navigate):{detail}",
            fix_hint="重试由桥自动进行(上限 3 次);emoji 目标在降级链不可定位时,先修 AX 门(doctor 看配方)后以 AX 主链发送",
        )

    if channel == "ax":
        _post_key_dual(KEY_F, FLAG_COMMAND)
        sleep(SEARCH_SETTLE_S)
        if not axui.write_search_value(target.search_term):
            raise _AxCapabilityMissing("write_search_value")
        deadline = monotonic() + SEARCH_RENDER_TIMEOUT_S
        while True:
            if axui.press_session_item(target.display_name):
                return {
                    "pick_rule": "ax_session_item",
                    "pick_cx": None,
                    "pick_cy": None,
                    "terms_hit": target.display_name,
                }
            if monotonic() >= deadline:
                raise _AxCapabilityMissing("press_session_item")
            sleep(SEARCH_POLL_S)
    terms = row_match_terms(target)
    # 搜索词双路写入(0.8.1,真机 dry-run 实证 CGEvent Cmd+V 可能静默丢:
    # /tmp/wxsend-e2e/ 搜索框恒空、无搜索弹窗):**AXFocusedUIElement 直写
    # 优先**(REF:26-28 同路线,系统级焦点查询,不依赖树遍历与键事件)
    # → 失败回落剪贴板 + Cmd+V(纯 CGEvent 路,keystroke 双引擎)。
    _post_key_dual(KEY_F, FLAG_COMMAND)
    sleep(SEARCH_SETTLE_S)
    if not axui.write_search_value(target.search_term):
        set_clipboard_text(target.search_term)
        sleep(CLIPBOARD_SETTLE_S)
        _post_key_dual(KEY_V, FLAG_COMMAND)
    sleep(SEARCH_RENDER_S)
    deadline = monotonic() + SEARCH_RENDER_TIMEOUT_S
    pick = None
    while True:
        lines = _ocr_region_lines(
            window, navfilter.SEARCH_PANE_BOX, workdir, "search"
        )
        pick = navfilter.select_result_row(lines, terms)
        if pick is not None:
            break
        if monotonic() >= deadline:
            raise stage_fail("搜索结果面板无可定位行(分区过滤零候选)")
        sleep(SEARCH_POLL_S)
    wx, wy = navfilter.pane_to_window(navfilter.SEARCH_PANE_BOX, pick.cx, pick.cy)
    click_at(*navfilter.row_box_to_screen(window, wx, wy))
    sleep(CLICK_SETTLE_S)
    return {
        "pick_rule": pick.rule,
        "pick_cx": pick.cx,
        "pick_cy": pick.cy,
        "terms_hit": pick.term,
    }


# --------------------------------------------------- 标题双验证(五件套①) ----


def _verify_title(
    target: SendTarget,
    window: Any,
    channel: str,
    baseline_title: str | None,
    workdir: Path,
    nav_debug: dict[str, Any],
) -> str:
    """标题双验证(红线 2 第二验)→ 返回 ``"ax_label"|"ocr"|"indirect"``。

    ax 通道:label 直读(emoji 精确;label 缺位不拦通道走 OCR 兜底)。
    降级:OCR 标题带轮询;emoji display_name OCR 核不出 → 间接证据链
    放行(导航级采纳记录在案 + 点击后标题带 ≠ 导航前基线)——零证据
    → exit 15 拒发(design §D-3)。
    """
    display = target.display_name

    def stage_fail(detail: str) -> BridgeError:
        return BridgeError(
            SEND_AX_FOCUS_REQUIRED,
            f"发送断言失败(阶段=locate):{detail}",
            fix_hint="重试由桥自动进行(上限 3 次);确认目标会话存在且搜索词可命中",
        )

    if channel == "ax":
        label = axui.read_current_chat_name()
        if label is not None:
            if _title_matches(label, display):
                return "ax_label"
            raise stage_fail("AX 标题与目标不符(label 可读但非目标会话)")
    deadline = monotonic() + TITLE_MATCH_TIMEOUT_S
    while True:
        visible = _ocr_region(window, TITLE_BAND_BOX, workdir, "title")
        if _title_matches(visible, display):
            return "ocr"
        if monotonic() >= deadline:
            break
        sleep(TITLE_POLL_S)
    if (
        _has_emoji(display)
        and nav_debug.get("pick_rule") in ("text_match", "unique_row")
        and baseline_title is not None
    ):
        current = _ocr_region(window, TITLE_BAND_BOX, workdir, "title")
        if squash(current or "") != squash(baseline_title):
            return "indirect"
    raise stage_fail("标题带与目标不符(导航后未切换到目标会话)")


# ------------------------------------------------- 哨兵空断言(五件套②前半) ----


def _assert_composer_empty(window: Any, channel: str) -> None:
    """发送前空断言:composer 非空 → 清 → 复探仍非空 →
    exit 15(composer_not_empty;WZ:250-252 同语义)。

    清的通道纪律(质询修正 2026-10-14:无焦点断言不合成 Cmd+A+Delete——
    焦点若落在会话列表,Delete 是 IM 的破坏性键):
    - ax 路:``axui.write_input_value("")`` AXValue 直写空串,**零键盘
      事件、焦点无关**(cgevent 路的 Cmd+A+Delete 安全性来自哨兵读自身
      先 click composer——哨兵读协议把焦点带到了输入区,键序才允许);
    - cgevent 路:哨兵读(含 composer 点击)已确保焦点在输入区,键序安全。
    """
    if channel == "ax":
        value = axui.read_input_value()
        if value is None:
            raise _AxCapabilityMissing("read_input_value")
        if not value.strip():
            return
        if not axui.write_input_value(""):
            raise _AxCapabilityMissing("write_input_value")
        sleep(CLEAR_SETTLE_S)
        again = axui.read_input_value()
        if again is None:
            raise _AxCapabilityMissing("read_input_value")
        if again.strip():
            raise BridgeError(
                SEND_AX_FOCUS_REQUIRED,
                "发送断言失败(阶段=composer_not_empty):清空后复探输入框仍非空",
                fix_hint="人工打开微信清理输入框残留草稿后重试",
            )
        return
    got = read_composer_via_clipboard(window)
    if got is None or not got.strip():
        return
    # 焦点已在 composer(上方哨兵读已点击聚焦),Cmd+A+Delete 安全。
    _post_key_dual(KEY_A, FLAG_COMMAND)
    _post_key_dual(KEY_DELETE)
    sleep(CLEAR_SETTLE_S)
    again = read_composer_via_clipboard(window)
    if again is not None and again.strip():
        raise BridgeError(
            SEND_AX_FOCUS_REQUIRED,
            "发送断言失败(阶段=composer_not_empty):清空后复探输入框仍非空(哨兵读)",
            fix_hint="人工打开微信清理输入框残留草稿后重试",
        )


# ------------------------------------------------------------- 写入与回读 ----


def _write_body(body: str, window: Any, channel: str) -> None:
    """写入正文:ax 通道 AXValue 直写(零剪贴板);降级链剪贴板 + Cmd+V。"""
    if channel == "ax":
        if not axui.write_input_value(body):
            raise _AxCapabilityMissing("write_input_value")
        sleep(PASTE_SETTLE_S)
        return
    set_clipboard_text(body)
    sleep(CLIPBOARD_SETTLE_S)
    click_at(*_composer_point(window))
    sleep(SENTINEL_GAP_S)
    _post_key_dual(KEY_V, FLAG_COMMAND)
    sleep(PASTE_SETTLE_S)


def _copy_all_readback(body: str, window: Any, channel: str) -> bool:
    """回读路 3:Cmd+A+Cmd+C 全量复制回读(KEY_C;长正文精确全量,
    design §1-h)。失败(False)→ 调用方走 OCR 输入带兜底。"""
    try:
        if channel == "cgevent_ocr":
            click_at(*_composer_point(window))
        else:
            if not axui.focus_input():
                return False  # 回读是断言不是能力门:跳过本路走 OCR 兜底
        sleep(SENTINEL_GAP_S)
        _post_key_dual(KEY_A, FLAG_COMMAND)
        sleep(0.03)
        _post_key_dual(KEY_C, FLAG_COMMAND)
        sleep(SENTINEL_GAP_S)
        got = clipboard_text()
        return got is not None and text_confirmed(got, body)
    except BridgeError:
        return False


def _readback(body: str, window: Any, workdir: Path, channel: str) -> str:
    """粘后回读(四路,顺序降级;失败 → exit 15 stage=readback)。

    降级链:剪贴板对账 → axui.read_input_value(门关时 None 跳过)→
    Cmd+A+Cmd+C 全量("clipboard_copy")→ OCR 输入带("ocr_strip")。
    ax 通道:read_input_value("ax_value")→ clipboard_copy → ocr_strip。
    """

    def stage_fail() -> BridgeError:
        return BridgeError(
            SEND_AX_FOCUS_REQUIRED,
            "发送断言失败(阶段=readback):四路回读均未确认正文在输入框",
            fix_hint="重试由桥自动进行(上限 3 次);持续失败检查输入区可聚焦性",
        )

    if channel == "cgevent_ocr":
        for _probe in range(3):
            current = clipboard_text()
            if current is not None and squash(current) == squash(body):
                break
            sleep(0.2)
        else:
            raise BridgeError(
                SEND_AX_FOCUS_REQUIRED,
                "发送断言失败(阶段=clipboard):粘贴后剪贴板读回与正文不符(写入被夺/系统忙碌)",
                fix_hint="重试;持续失败检查剪贴板被夺(pbpaste 读回对账)",
            )
    ax_value = axui.read_input_value()
    if ax_value is not None and text_confirmed(ax_value, body):
        return "ax_value"
    if _copy_all_readback(body, window, channel):
        return "clipboard_copy"
    deadline = monotonic() + READBACK_TIMEOUT_S
    while True:
        strip = _ocr_region(window, INPUT_STRIP_BOX, workdir, "input")
        if text_confirmed(strip, body):
            return "ocr_strip"
        if monotonic() >= deadline:
            break
        sleep(READBACK_POLL_S)
    raise stage_fail()


# ------------------------------------------------- 发送前聚焦断言(§D-2) ----


def _assert_focused(body: str, window: Any, channel: str) -> None:
    """发送前聚焦断言(两通道对称;防回车落搜索框)。失败抛 _FocusFail /
    _AxCapabilityMissing(focus_input False),不抛 = 聚焦成立。

    ax 通道:focus_input(AXPress)→ 复读 value==body(聚焦未丢正文)→
    focused_is_input 尽力断言(取 None 如实降为前两条)。
    降级链:哨兵读一致性——click_at(COMPOSER_POINT) + read_composer 回
    **==body(正文在框)** 才算聚焦成立;回异值 = 焦点落别处、回 None/
    空 = 正文已丢失(此时回读已确认过,空即异常态)——两者都 focus 失败
    (哨兵协议本身即聚焦断言,不是裸点击;design §J-17。质询修正
    2026-10-14:发送前「空」不等于聚焦成立——空 composer 上回车 = 发空
    消息/错发,与 ax 路对空值 fail 对称)。
    """

    def focus_fail(detail: str, ax_missing: bool = False) -> _FocusFail:
        return _FocusFail(
            BridgeError(
                SEND_AX_FOCUS_REQUIRED,
                f"发送断言失败(阶段=focus):{detail}",
                fix_hint="重试由桥自动进行;持续失败检查输入区聚焦与辅助功能授权",
            ),
            ax_missing,
        )

    if channel == "ax":
        if not axui.focus_input():
            raise _AxCapabilityMissing("focus_input")
        value = axui.read_input_value()
        if value is None or not text_confirmed(value, body):
            raise focus_fail("AX 聚焦后复读正文丢失(输入框内容与正文不符)")
        focused = axui.focused_is_input()
        if focused is False:
            raise focus_fail("AXFocusedUIElement 非输入区")
        return
    click_at(*_composer_point(window))
    sleep(SENTINEL_GAP_S)
    got = read_composer_via_clipboard(window)
    if text_confirmed(got or "", body):
        return  # 正文在框 = 焦点在 composer 且正文未丢
    if got is None or not got.strip():
        raise focus_fail("composer 哨兵读回空(正文已丢失;发送前空 ≠ 聚焦成立)")
    raise focus_fail("composer 点击后哨兵读回异值(焦点不在输入框)")


# --------------------------------------------- 发送后验证(五件套③/回执) ----


def _wait_composer_cleared(window: Any, channel: str) -> bool:
    """发送后清空轮询(五件套件 3;12×80ms,WZ:271-277):AX 通道
    read_input_value 直读(零点击),降级链哨兵读。转空 = 发出强证据;
    超时 → False 如实(uncertain note 由调用方组装)。"""
    for _ in range(CLEAR_POLL_TIMES):
        if channel == "ax":
            value = axui.read_input_value()
            if value is not None and not value.strip():
                return True
        else:
            if read_composer_via_clipboard(window) is None:
                return True
        sleep(CLEAR_POLL_GAP_S)
    return False


def _poll_receipt(
    receipt_query: Callable[[str, str, float], bool | None] | None,
    username: str,
    body: str,
    since_epoch: float,
) -> bool | None:
    """localdb 回执终验轮询(红线 4;RECEIPT_POLL_SCHEDULE 退避,累计 ~30s)。

    Returns:
        True = 见到落库;False = 查询可执行但超窗未见;None = 链失败
        (localdb BridgeError → None 如实,不算失败也不算成功,§C-6)。
        回执判定(含 ts > since_epoch - 2 防同正文历史假绿)在 CLI 注入
        的闭包内。
    """
    if receipt_query is None:
        return None
    executed = False
    for gap in (0.0,) + tuple(RECEIPT_POLL_SCHEDULE):
        if gap:
            sleep(gap)
        try:
            if receipt_query(username, body, since_epoch) is True:
                return True
            executed = True
        except Exception:  # noqa: BLE001 - 链失败如实 None/继续轮询
            continue
    return False if executed else None


def _post_send_verify(body: str, workdir: Path) -> dict[str, Any]:
    """发送后回读(消息区 OCR,辅助证据;降级为五件套之外的过程证据):
    **绝不抛错**;结果如实入载荷,末次中断原因不吞。"""
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


# --------------------------------------------------------------- 单尝试 ----


def _attempt_send(
    target: SendTarget,
    body: str,
    workdir: Path,
    *,
    dry_run: bool,
    forced_fallback: bool,
    on_armed: Callable[[], None] | None,
    on_receipt_green: Callable[[], None] | None,
    receipt_query: Callable[[str, str, float], bool | None] | None,
    ctx: dict[str, bool],
) -> dict[str, Any]:
    """一次完整尝试(设计 §1 序列 a-k;**绝不盲回车**)。

    Returns:
        载荷素材 dict(dry-run 收尾或发送后验证结果;成功/uncertain 形态)。

    Raises:
        BridgeError: on_armed 之前(含 on_armed 自身 fail-closed)的断言
            失败(exit 15/30 族)→ 调用方重试/上抛(可 rollback)。
        _ArmedFailure: armed 后聚焦断言失败(未回车)→ 调用方重试/终败
            上抛(CLI 不 rollback,指纹 pending 在档)。
        _AxCapabilityMissing: AX 原语 False → 下一尝试 forced_fallback。
    """
    # —— a. 激活 + 前台断言 ——
    activate_wechat()
    _wait_until(
        frontmost_is_wechat,
        timeout_s=ACTIVATE_TIMEOUT_S,
        poll_s=ACTIVATE_POLL_S,
        stage="activate",
    )
    window = _find_window()
    if window is None:
        raise BridgeError(
            SEND_AX_FOCUS_REQUIRED,
            "发送断言失败(阶段=window):CGWindowList 无微信主窗(前置门放行后窗口消失)",
            fix_hint="重试;持续失败检查微信窗口态",
        )

    # —— b. 通道判定(双判据;单尝试内固定,跨尝试降级见调用方)——
    channel = "cgevent_ocr" if forced_fallback else (
        "ax" if axui.probe_wechat_ax() else "cgevent_ocr"
    )

    # —— c. 导航前基线(仅降级链;emoji indirect 证据链比较基准)——
    baseline_title: str | None = None
    if channel == "cgevent_ocr":
        baseline_title = _ocr_region(window, TITLE_BAND_BOX, workdir, "title")

    # —— d. 导航(分区过滤/AXPress;零盲回车)——
    nav_debug = _navigate(target, window, channel, workdir)

    # —— e. 标题双验证 ——
    title_verify = _verify_title(target, window, channel, baseline_title, workdir, nav_debug)

    # —— f. 发送前哨兵空断言(五件套②)——
    _assert_composer_empty(window, channel)

    # —— g. 写入正文 ——
    _write_body(body, window, channel)

    # —— h. 粘后回读(四路)——
    readback = _readback(body, window, workdir, channel)

    # —— i. dry-run 收尾(不回车不 on_armed,零频控副作用)——
    if dry_run:
        # 清草稿的通道纪律(同 _assert_composer_empty:无焦点断言不合成
        # Cmd+A+Delete)——ax 路 AXValue 直写空串零键盘;cgevent 路先
        # click composer 确保焦点再走键序。
        if channel == "ax":
            if not axui.write_input_value(""):
                raise _AxCapabilityMissing("write_input_value")
        else:
            click_at(*_composer_point(window))
            sleep(SENTINEL_GAP_S)
            _post_key_dual(KEY_A, FLAG_COMMAND)
            _post_key_dual(KEY_DELETE)
            _post_key_dual(KEY_ESCAPE)  # 退出搜索态
        return {
            "channel": channel,
            "sent": False,
            "dry_run": True,
            "navigated": True,
            "pasted": True,
            "readback": readback,
            "title_verify": title_verify,
            "nav_debug": nav_debug,
        }

    # —— j0. on_armed = fail-closed 门(design §C-5)——
    since_epoch = wall_clock()
    if on_armed is not None:
        try:
            on_armed()  # 落指纹 pending;失败上抛(armed 仍 False → 可 rollback)
        except BridgeError:
            raise
        except Exception:
            raise BridgeError(
                SEND_AX_FOCUS_REQUIRED,
                "on_armed 回调失败(指纹 pending 未落;未回车,fail-closed 拒发)",
                fix_hint="重试可安全进行(未发出);持续失败检查数据根可写性",
            ) from None
    ctx["armed"] = True

    # —— 以下(armed=True)对外恒不抛(§C-5)——
    try:
        # j1. 发送前聚焦断言(两通道对称)
        try:
            _assert_focused(body, window, channel)
        except _FocusFail as ff:
            raise _ArmedFailure(ff.error, ff.ax_missing)
        except _AxCapabilityMissing as exc:
            raise _ArmedFailure(
                BridgeError(
                    SEND_AX_FOCUS_REQUIRED,
                    f"发送断言失败(阶段=focus):AX 能力缺失({exc.primitive})",
                    fix_hint="下一尝试转降级链;持续失败检查辅助功能授权",
                ),
                True,
            )
        # j2. 唯一一次回车(全函数唯一发送动作;flags=0)
        post_key(KEY_RETURN)
        sleep(POST_SEND_SETTLE_S)
        # k1. 清空轮询(五件套③)
        cleared = _wait_composer_cleared(window, channel)
        # k2. localdb 回执终验(红线 4;失败→指纹保持 pending)
        receipt = _poll_receipt(receipt_query, target.username, body, since_epoch)
        fingerprint_note = None
        # 全绿(清空轮询 + 回执)才升 sent(design §C-4「回车后验证全绿
        # → sent;否则保持 pending」);回执 True 是 DB 侧铁证但轮询超时
        # = 过程不确定,保守 pending(uncertain-never-retry 方向)。
        if cleared and receipt is True and on_receipt_green is not None:
            try:
                on_receipt_green()
            except Exception:  # noqa: BLE001 - armed 后吞,如实注记
                fingerprint_note = "回执全绿但指纹升级 sent 失败(防重窗仍以 pending 有效)"
        # k3. 消息区 OCR(辅助证据,既有原语保留)
        verdict = _post_send_verify(body, workdir)
    except _ArmedFailure:
        raise  # 聚焦终败信号原样上抛(内部处理路径)
    except Exception as exc:  # noqa: BLE001 - armed 后兜底吞(§C-5)
        return {
            "channel": channel,
            "sent": True,
            "readback": readback,
            "title_verify": title_verify,
            "composer_cleared": False,
            "localdb_receipt": None,
            "post_send_verified": False,
            "post_send_note": f"发出后内部异常({type(exc).__name__}),结果不确定",
            "fingerprint_note": None,
        }
    return {
        "channel": channel,
        "sent": True,
        "readback": readback,
        "title_verify": title_verify,
        "composer_cleared": cleared,
        "localdb_receipt": receipt,
        "fingerprint_note": fingerprint_note,
        **verdict,
    }


# ------------------------------------------------------------------ 主口 ----


def send_text(
    config: BridgeConfig,
    target: SendTarget,
    body: str,
    *,
    dry_run: bool = False,
    on_armed: Callable[[], None] | None = None,
    on_receipt_green: Callable[[], None] | None = None,
    receipt_query: Callable[[str, str, float], bool | None] | None = None,
) -> dict[str, Any]:
    """``send_text`` 实现(三源合体,见模块 docstring)。

    Args:
        target: DB 侧解析产物(:func:`.sendtarget.resolve_target`)。
        dry_run: 走到「正文已粘贴 + 回读确认」收尾——不回车、不 on_armed、
            零频控副作用,可无限重跑(design §E-1)。
        on_armed: 回车 down 前回调(= 落指纹 pending)。**fail-closed**:
            失败上抛(未回车,CLI 可 rollback 重试);armed 之后的一切异常
            在本函数内吞掉(design §C-5)。
        on_receipt_green: 回执全绿回调(= 指纹升 sent;armed 段内吞异常)。
        receipt_query: CLI 注入的 localdb 回执判定闭包(username, body,
            since_epoch)→ bool | None(sendui 零 localdb 依赖)。

    Returns:
        ``{"send": {target, channel, sent, dry_run?, navigated?, pasted?,
        readback, title_verify, nav_debug?, attempts, composer_cleared?,
        localdb_receipt?, post_send_verified?, post_send_note?,
        fingerprint_note?, elapsed_ms}}``——``chat`` 键由 CLI 补(原样
        入参);载荷只载形状与通路,永不载正文(红线 6)。

    Raises:
        BridgeError: **只在未发出时**(exit 15 断言族——含聚焦终败的
        error 载荷,stage=focus 且 message 注明 pending 已落 / 30 子进程
        超时);回车按下后不再抛(契约见 ax.py send_text docstring,G6)。
    """
    started = monotonic()
    original_clipboard = clipboard_text()
    workdir = _fresh_workdir()
    attempts_used = 0
    forced_fallback = False
    armed_ever = False
    last_error: BridgeError | None = None
    result: dict[str, Any] | None = None
    ctx: dict[str, bool] = {"armed": False}
    try:
        for attempt_index in range(MAX_ATTEMPTS):
            attempts_used += 1
            ctx["armed"] = False
            try:
                result = _attempt_send(
                    target,
                    body,
                    workdir,
                    dry_run=dry_run,
                    forced_fallback=forced_fallback,
                    on_armed=None if dry_run else on_armed,
                    on_receipt_green=on_receipt_green,
                    receipt_query=receipt_query,
                    ctx=ctx,
                )
                last_error = None
                break
            except _AxCapabilityMissing as exc:
                forced_fallback = True
                last_error = BridgeError(
                    SEND_AX_FOCUS_REQUIRED,
                    f"AX 能力缺失({exc.primitive}),下一尝试转降级链",
                    fix_hint="降级链自动接管;持续失败检查辅助功能授权与 AX 门(doctor)",
                )
            except _ArmedFailure as exc:
                forced_fallback = forced_fallback or exc.ax_missing
                last_error = exc.error
            except BridgeError as exc:
                last_error = exc
            # 任一尝试 armed 过即视同 uncertain(质询修正 2026-10-14:
            # 在循环内即时并集,终败报文不再只反映末次尝试——尝试1 armed
            # 后失败 + 尝试2 未及 armed 失败的混合场景,message 也带
            # pending 注记,与状态文件/CLI armed 闭包的保守方向一致)。
            armed_ever = armed_ever or ctx["armed"]
            if result is None and attempt_index < MAX_ATTEMPTS - 1:
                sleep(RETRY_BACKOFF_S)
        if result is None:
            if last_error is None:  # pragma: no cover - 防御(循环必设其一)
                last_error = BridgeError(
                    SEND_AX_FOCUS_REQUIRED, "发送未执行(未知失败形态)"
                )
            if armed_ever:
                # 聚焦终败(armed 后未回车):exit 15 error 载荷,message
                # 注明 pending 已落(design §1-j1/§J-20)——不破
                # 「exit 0 ⇒ sent:true」旧契约;CLI 层 armed 闭包保证不 rollback。
                raise BridgeError(
                    last_error.exit_code,
                    f"发送前聚焦断言未过(未回车;指纹已 pending,120s 内同指纹"
                    f"重发将 exit 17):{MAX_ATTEMPTS} 次尝试均未通过;"
                    f"末次失败 {last_error.message}",
                    fix_hint="重试须换正文或等 120s(uncertain-never-retry);"
                    "持续失败检查输入区聚焦与辅助功能授权",
                    retry_after_seconds=last_error.retry_after_seconds,
                )
            raise BridgeError(
                last_error.exit_code,
                f"发送未执行:{MAX_ATTEMPTS} 次尝试均未通过断言;"
                f"末次失败 {last_error.message}",
                fix_hint=last_error.fix_hint,
                retry_after_seconds=last_error.retry_after_seconds,
            )
    finally:
        # 剪贴板复原(best-effort;五件套⑤)。已知局限如实(与 WZ 原版
        # 同限):复原仅文本面——原内容为非文本(图片/富文本)时 pbpaste
        # 读不回,**清空即销毁**;哨兵/搜索词/正文对剪贴板的中间覆写都在
        # 本 try 块内,finally 必达,文本原内容精确复原、空原内容清空不留正文。
        try:
            if original_clipboard:
                set_clipboard_text(original_clipboard)
            else:
                set_clipboard_text("")
        except BridgeError:
            pass  # 复原失败不拦发送结果(载荷如实,剪贴板残留正文可接受)
        shutil.rmtree(workdir, ignore_errors=True)  # 截图件即清(红线 6)
    assert result is not None  # 循环正常出口必已赋值
    return {
        "send": {
            "target": {"username": target.username, "display_name": target.display_name},
            "attempts": attempts_used,
            "elapsed_ms": round((monotonic() - started) * 1000),
            **result,
        }
    }
