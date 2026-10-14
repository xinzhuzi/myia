"""像素读层(task 10-11-wechat-ui-bridge Phase C1/C2;D2 定论后的唯一 UI 读源)。

A1 定论(prd D2;证据 research/ax-probe-4.1.15.md):微信 4.1.15 聊天内容层
对 AX 完全零暴露 → UI 读唯一路径 = 像素链::

    截窗(screencapture -l -o,零激活零抢焦)
      → VisionOCR(pyobjc/Vision 直调,一级,毫秒级+逐行置信度)
      → VL 校对(127.0.0.1:8080 qwen3-vl-8b-mlx,二级,置信度门触发,
                 显式降采样路径:长边 >2048 先 LANCZOS 降采样再 base64)
      → 结构化解析(会话名+未读数 / 最近 K 条消息文本)

静默铁律(prd 红线 4):screencapture -l 对后台窗口零交互零合成;
2026-10-11 实测(macOS 26.4 + 微信 4.1.15)ordered-off(托盘/未 ordered-on)
主窗可出**完整合成帧**(出图/黑图/失败三态判定的「出图」,见
research/pixel-chain-e2e.md),但内容为窗口服务器持有的**最后渲染帧**——
新鲜度限制如实标注在载荷 ``window.note``。

私有数据红线(prd 红线 6):截图与裁剪件含聊天内容 → 全部落 tempfile
(0700)私有目录、用后即清;OCR 行文本只进 stdout 契约载荷,不进日志、
不进异常消息。

几何解析不硬编码本机像素:以**时间锚**(会话列表右缘的 HH:MM/昨天/周X 列)
做数据驱动定位——名字=同行左侧线、预览=名字下方同 x 线、未读徽标=时间右侧
短线;聊天区=时间锚右缘之右。全部阈值取 2026-10-11 实测形状的宽容带。

错误码纪律(对齐 ax.py 过渡码先例):像素链专属故障不谎报 §6 具名族——
exit 1(通用失败段)+ 显式过渡码(``screen_capture_failed`` /
``screen_capture_black`` / ``ocr_unavailable``);§6 码表封闭,扩码须先改
design §6(主会话裁决项,见 research/pixel-chain-e2e.md §建议)。
"""

from __future__ import annotations

import base64
import json
import re
import shutil
import subprocess
import tempfile
import time
import urllib.request
from dataclasses import dataclass, replace
from pathlib import Path
from typing import Any, Callable

from .codes import EXIT_GENERIC_FAILURE, TIMEOUT, BridgeError
from .config import BridgeConfig
from .system_checks import WECHAT_OWNER_NAMES

__all__ = [
    "CONF_GATE",
    "VL_BASE_URL",
    "OcrLine",
    "SessionRow",
    "MessageRow",
    "WindowInfo",
    "find_main_window",
    "capture_window",
    "vision_ocr",
    "vl_available",
    "vl_correct_lines",
    "parse_sessions",
    "parse_messages",
    "list_sessions",
    "read_messages",
]

# —— 一级→二级升级门(local-ocr 技能机械规则:任一使用的行 conf≤0.5 即升)——
CONF_GATE = 0.5

# —— VL 二级(本机 mlx-vlm 服务;组件内常量,不进 §7 配置面)——
VL_BASE_URL = "http://127.0.0.1:8080"
VL_TIMEOUT_SECONDS = 120.0
VL_MAX_DIM = 2048  # 显式降采样路径:长边超过先降采样(2130×2x 全窗 → 2048)

# —— 截窗三态判定 ——
#: 黑图判定:64×36 降采样 luma 均值与极差都低于此 → 无有效内容
#: (TCC 屏幕录制权限缺失/未渲染窗口的典型形状)。
BLACK_MEAN_MAX = 8.0
BLACK_SPAN_MAX = 10.0

# —— 会话列表几何(2026-10-11 实测形状的宽容带;全部为窗口内容归一化坐标)——
#: 名字列 x 下限(图标栏右缘,实测亮带 0–0.052;名字列实测 x≈0.059)。
NAME_MIN_X = 0.045
#: 同行(名字↔时间)y 容差。
NAME_Y_TOL = 0.009
#: 时间锚聚集带宽(会话时间列 x 跨度;实测 0.185–0.20)。
TIME_CLUSTER_SPAN = 0.08
#: 预览行相对名字行的 y 偏移带(实测 ≈0.018)。
PREVIEW_DY = (0.006, 0.038)
#: 趟 2 名字+预览对组的 y 偏移带(与 PREVIEW_DY 同源,收窄防误配)。
PAIR_DY = (0.012, 0.028)
#: 徽标带相对行右缘的回退宽度(徽标与时间同右对齐,带宽=时间文本宽度级)。
BADGE_ZONE_WIDTH = 0.045
#: 未读徽标带左缘的余量(徽标与时间同右对齐,时间文本右缘≈行右缘)。
BADGE_GAP = 0.004
#: 徽标↔时间行 y 偏移带(徽标在时间行同高略偏下:行中垂直居中;相对时间行)。
BADGE_DY = (-0.005, 0.026)
#: 行去重最小间距。
ROW_DEDUPE_Y = 0.004
#: 聊天标题带(窗口顶部;实测标题 y≈0.041)。
TITLE_MAX_Y = 0.06
#: 消息体起点(标题带之下)。
MSG_TOP_Y = 0.075
#: 居中时间标记的 x 中心带宽(聊天区横向中部 ±0.18)。
CENTER_TIME_SPAN = 0.18
#: 右侧(自己发的)气泡 x 下限。
RIGHT_BUBBLE_MIN_X = 0.55
#: 发送者名行:位于气泡文本上方 0.012–0.034(实测名→气泡 dy≈0.030;
#: 消息块间距 ≈0.042 在带外,压窄上限防把上一条消息末行误判为发送者)。
SENDER_DY = (0.012, 0.034)
SENDER_MAX_LEN = 24
#: 换行合并:同行消息的连续行 dy 上限。
WRAP_MERGE_DY = 0.036

#: 会话时间形态(HH:MM / 昨天 / 前天 / 周X / 星期X / M月D日 / M/D)。
TIME_RE = re.compile(
    r"^(?:\d{1,2}[:：]\d{2}|\d{1,2}[:：]\d{2}:\d{2}|昨天|前天|今[天日]|"
    r"周[一二三四五六日天]|星期[一二三四五六日天]|\d{1,2}月\d{1,2}[日号]|\d{1,2}/\d{1,2})$"
)
#: 未读徽标形态(纯数字 / 999+)。
BADGE_RE = re.compile(r"^(?:\d{1,3}|999\+)$")


@dataclass(frozen=True)
class WindowInfo:
    """微信主窗快照(CGWindowList;零激活零枚举 AX)。

    x/y = 窗口左上角的屏幕绝对像素(kCGWindowBounds 同系:原点主屏左上、
    Y 向下;2026-10-14 task 10-14-wechat-send-text 加,供 CGEvent 点击的
    window→screen 坐标换算;缺省 0 向后兼容旧构造)。
    """

    window_id: int
    onscreen: bool
    width: float
    height: float
    pid: int | None = None
    x: float = 0.0
    y: float = 0.0

    def to_payload(self) -> dict[str, Any]:
        note = None
        if not self.onscreen:
            note = (
                "窗口在册但未 ordered-on(托盘/后台态):截窗取窗口服务器持有的"
                "最后渲染帧,可能非实时内容(2026-10-11 实测可出完整帧)"
            )
        return {
            "window_id": self.window_id,
            "onscreen": self.onscreen,
            "width": self.width,
            "height": self.height,
            "x": self.x,
            "y": self.y,
            "note": note,
        }


@dataclass(frozen=True)
class OcrLine:
    """单行 OCR 结果(坐标为图像归一化 0–1,原点左上)。"""

    text: str
    conf: float
    x: float
    y: float
    w: float
    h: float


@dataclass(frozen=True)
class SessionRow:
    """会话行(C1 结构化解析产物;unread 不可见时 None 如实)。"""

    name: str
    unread: int | None
    time_text: str | None
    preview: str | None
    conf: float

    def to_payload(self) -> dict[str, Any]:
        return {
            "id": self.name,
            "name": self.name,
            "unread": self.unread,
            "time": self.time_text,
            "preview": self.preview,
            "conf": self.conf,
        }


@dataclass(frozen=True)
class MessageRow:
    """消息行(C2 结构化解析产物;ts=最近居中时间标记原文,无绝对日期)。"""

    ts: str | None
    sender: str | None
    text: str
    side: str  # left=对方 / right=自己 / center=时间或系统行
    conf: float

    def to_payload(self) -> dict[str, Any]:
        return {
            "ts": self.ts,
            "sender": self.sender,
            "type": "text",
            "text": self.text,
            "side": self.side,
            "conf": self.conf,
        }


# ---------------------------------------------------------------- 截窗 ----

def _read_window_list() -> list[dict[str, Any]]:
    """CGWindowList 全量快照(零激活;pyobjc 缺位/非 darwin → 空表如实)。"""
    if not _sys_darwin():
        return []
    try:
        import Quartz
    except ImportError:
        return []
    raw = Quartz.CGWindowListCopyWindowInfo(
        Quartz.kCGWindowListOptionAll, Quartz.kCGNullWindowID
    )
    return [dict(w) for w in (raw or [])]


def find_main_window(
    *,
    window_list_reader: Callable[[], list[dict[str, Any]]] | None = None,
) -> WindowInfo | None:
    """定位微信主窗(属主 微信/WeChat,layer 0,面积最大;在场窗优先)。

    ordered-off 窗口同样在册且可截(2026-10-11 实测),故不做 onscreen 过滤,
    只在并列时优先在场窗;零窗口 → None(上层前置门给 §6 exit 12)。
    """
    reader = window_list_reader if window_list_reader is not None else _read_window_list
    best: WindowInfo | None = None
    for entry in reader():
        owner = entry.get("kCGWindowOwnerName") or ""
        if owner not in WECHAT_OWNER_NAMES:
            continue
        if entry.get("kCGWindowLayer") != 0:
            continue
        bounds = entry.get("kCGWindowBounds") or {}
        width = float(bounds.get("Width") or 0)
        height = float(bounds.get("Height") or 0)
        if width <= 0 or height <= 0:
            continue
        info = WindowInfo(
            window_id=int(entry.get("kCGWindowNumber") or 0),
            onscreen=bool(entry.get("kCGWindowIsOnscreen")),
            width=width,
            height=height,
            pid=entry.get("kCGWindowOwnerPID"),
            x=float(bounds.get("X") or 0),
            y=float(bounds.get("Y") or 0),
        )
        if best is None or (info.onscreen, info.width * info.height) > (
            best.onscreen,
            best.width * best.height,
        ):
            best = info
    return best


def _sys_darwin() -> bool:
    import sys

    return sys.platform == "darwin"


def _looks_black(path: Path) -> bool:
    """黑图/空帧判定(64×36 降采样 luma;纯统计,零内容读出)。"""
    try:
        from PIL import Image
    except ImportError:
        return False  # 判不了 → 不判黑(宁可给出图也不误杀)
    with Image.open(path) as img:
        small = img.convert("L").resize((64, 36))
        pixels = list(small.getdata())
    mean = sum(pixels) / len(pixels)
    return mean < BLACK_MEAN_MAX and (max(pixels) - min(pixels)) < BLACK_SPAN_MAX


def capture_window(
    window: WindowInfo,
    out_path: Path,
    *,
    runner: Callable[..., subprocess.CompletedProcess[bytes]] | None = None,
) -> dict[str, Any]:
    """截窗(screencapture -x -o -l;静默、零交互、无阴影)。

    Returns:
        ``{"state": "ok"|"black"|"failed", "path", "width", "height",
        "mean_luma"}``——三态判定(ask 判例:出图/黑图/失败)。

    Raises:
        BridgeError: exit 30(子进程超时)/ exit 1(失败或黑图)。
    """
    run = runner if runner is not None else subprocess.run
    try:
        result = run(
            [
                "screencapture",
                "-x",  # 静默(不出快门声)
                "-o",  # 无阴影(坐标=窗口内容原点)
                "-l",
                str(window.window_id),
                str(out_path),
            ],
            capture_output=True,
            timeout=15,
            check=False,
        )
    except subprocess.TimeoutExpired as exc:
        raise BridgeError(
            TIMEOUT,
            "截窗子进程超时(screencapture 15s 未退出,已 kill)",
            fix_hint="重试;持续超时说明窗口服务器层挂起",
        ) from exc
    if result.returncode != 0 or not out_path.is_file():
        raise BridgeError(
            EXIT_GENERIC_FAILURE,
            "截窗失败:screencapture 退出码 {}、产物缺失={}".format(
                result.returncode, not out_path.is_file()
            ),
            code="screen_capture_failed",
            fix_hint="确认微信主窗在册(CGWindowList);重试一次;持续失败查系统日志",
        )
    try:
        from PIL import Image

        with Image.open(out_path) as img:
            width, height = img.size
            small = img.convert("L").resize((64, 36))
            pixels = list(small.tobytes())  # L 模式 → 每像素 1 字节灰度
    except Exception as exc:  # noqa: BLE001 - 产物损坏按失败态
        raise BridgeError(
            EXIT_GENERIC_FAILURE,
            f"截窗产物不可读:{type(exc).__name__}",
            code="screen_capture_failed",
            fix_hint="重试;持续失败说明窗口服务器态异常",
        ) from exc
    mean = sum(pixels) / len(pixels)
    black = mean < BLACK_MEAN_MAX and (max(pixels) - min(pixels)) < BLACK_SPAN_MAX
    if black:
        raise BridgeError(
            EXIT_GENERIC_FAILURE,
            f"截窗得黑图/空帧(64×36 采样 luma 均值 {mean:.1f})",
            code="screen_capture_black",
            fix_hint=(
                "典型原因=宿主进程缺「屏幕录制」TCC 授权:系统设置 → 隐私与安全性 → "
                "屏幕录制,给 MYIA(或桥宿主进程)授权后重试"
            ),
        )
    return {
        "state": "ok",
        "path": str(out_path),
        "width": width,
        "height": height,
        "mean_luma": round(mean, 1),
    }


# ------------------------------------------------------------- VisionOCR ----

_VISION_LANGS = ("zh-Hans", "en-US")


def vision_ocr(image_path: Path) -> tuple[str, list[OcrLine], float]:
    """一级 OCR:pyobjc/Vision 框架组件内直调(毫秒级,逐行置信度)。

    Returns:
        (engine 名, 行列表[按 y→x 排序], 耗时秒)。

    Raises:
        BridgeError: Vision/pyobjc 不可用(exit 1 + ``ocr_unavailable``,
        上层可据此降级 VL 直读)或识别执行失败。
    """
    try:
        import Vision
        from Foundation import NSURL
    except ImportError as exc:
        raise BridgeError(
            EXIT_GENERIC_FAILURE,
            "VisionOCR 不可用:pyobjc-framework-Vision 未安装",
            code="ocr_unavailable",
            fix_hint="组件运行环境需 pyobjc(含 Vision);或等待 VL 二级接管",
        ) from exc
    url = NSURL.fileURLWithPath_(str(image_path))
    handler = Vision.VNImageRequestHandler.alloc().initWithURL_options_(url, None)
    request = Vision.VNRecognizeTextRequest.alloc().init()
    request.setRecognitionLevel_(Vision.VNRequestTextRecognitionLevelAccurate)
    request.setRecognitionLanguages_(list(_VISION_LANGS))
    request.setUsesLanguageCorrection_(False)  # 报错码/ID 保真惯例(local-ocr 技能)
    started = time.monotonic()
    ok, error = handler.performRequests_error_([request], None)
    elapsed = time.monotonic() - started
    if not ok:
        raise BridgeError(
            EXIT_GENERIC_FAILURE,
            f"VisionOCR 执行失败:{type(error).__name__ if error else 'unknown'}",
            code="ocr_unavailable",
            fix_hint="重试;持续失败改走 VL 二级",
        )
    lines: list[OcrLine] = []
    for observation in request.results() or []:
        candidates = observation.topCandidates_(1)
        if not candidates:
            continue
        candidate = candidates[0]
        box = observation.boundingBox()  # 原点左下 → 翻成左上
        text = candidate.string()
        if not text or not text.strip():
            continue
        lines.append(
            OcrLine(
                text=text,
                conf=round(float(candidate.confidence()), 3),
                x=round(box.origin.x, 4),
                y=round(1.0 - box.origin.y - box.size.height, 4),
                w=round(box.size.width, 4),
                h=round(box.size.height, 4),
            )
        )
    lines.sort(key=lambda line: (line.y, line.x))
    return "vision", lines, round(elapsed, 3)


# --------------------------------------------------------------- VL 二级 ----

def vl_available(
    *,
    opener: Callable[[urllib.request.Request], Any] | None = None,
    base_url: str = VL_BASE_URL,
) -> str | None:
    """VL 服务在场性(GET /v1/models;返回可用 model id,缺位 → None)。"""
    fetch = opener if opener is not None else _http_get_json
    try:
        payload = fetch(urllib.request.Request(f"{base_url}/v1/models"))
    except Exception:  # noqa: BLE001 - 服务不在/超时一律如实 None
        return None
    models = (payload or {}).get("data") or []
    ids = [str(item.get("id")) for item in models if item.get("id")]
    if not ids:
        return None
    for model_id in ids:
        if "qwen3-vl" in model_id.lower():
            return model_id
    return ids[0]


def _http_get_json(request: urllib.request.Request) -> Any:
    with urllib.request.urlopen(request, timeout=5) as response:  # noqa: S310 - 本机定址
        return json.loads(response.read().decode("utf-8"))


def downsample_for_vl(image_path: Path, out_path: Path) -> tuple[Path, bool]:
    """显式降采样路径:长边 > :data:`VL_MAX_DIM` → LANCZOS 缩到上限。

    Returns:
        (送检图路径, 是否降采样过)。
    """
    from PIL import Image

    with Image.open(image_path) as img:
        width, height = img.size
        if max(width, height) <= VL_MAX_DIM:
            return image_path, False
        scale = VL_MAX_DIM / max(width, height)
        resized = img.resize(
            (max(1, round(width * scale)), max(1, round(height * scale))),
            Image.LANCZOS,
        )
        resized.save(out_path, format="PNG")
    return out_path, True


def vl_correct_lines(
    image_path: Path,
    lines: list[OcrLine],
    workdir: Path,
    *,
    model_id: str | None = None,
    opener: Callable[..., Any] | None = None,
    base_url: str = VL_BASE_URL,
) -> tuple[list[OcrLine], dict[str, Any]]:
    """二级 VL 校对:对照降采样图修正初稿行(禁增删行,只改字)。

    Returns:
        (修正后行列表[行数/顺序/坐标/置信度保持], meta)——meta 带是否降
        采样、是否解析成功;VL 不可用或应答不可解析时原样返回初稿(如实)。
    """
    meta: dict[str, Any] = {"model": model_id, "downsampled": False, "parsed": False}
    model = model_id or vl_available(base_url=base_url, opener=opener)
    if not model:
        meta["error"] = "vl_unavailable"
        return lines, meta
    meta["model"] = model
    send_path = image_path
    from PIL import Image as _pil  # 尺寸探测(降采样判据)

    with _pil.open(image_path) as probe:
        need_downsample = max(probe.size) > VL_MAX_DIM
    if need_downsample:
        send_path, meta["downsampled"] = downsample_for_vl(
            image_path, workdir / "vl_input.png"
        )
    draft = [{"i": index, "text": line.text} for index, line in enumerate(lines)]
    content = [
        {
            "type": "image_url",
            "image_url": {
                "url": "data:image/png;base64,"
                + base64.b64encode(send_path.read_bytes()).decode("ascii")
            },
        },
        {
            "type": "text",
            "text": (
                "这是 OCR 初稿的行列表(JSON)。请对照图片逐行校对,只修正确有"
                "出入的字;禁止增删行、禁止改顺序、禁止输出任何解释。输出 JSON "
                '数组,每项 {"i": 行号, "text": "校对后文本"},覆盖全部 '
                f"{len(lines)} 行。初稿:{json.dumps(draft, ensure_ascii=False)}"
            ),
        },
    ]
    body = json.dumps(
        {"model": model, "max_tokens": 8192, "messages": [{"role": "user", "content": content}]}
    ).encode("utf-8")
    request = urllib.request.Request(  # noqa: S310 - 本机定址
        f"{base_url}/v1/chat/completions",
        data=body,
        headers={"Content-Type": "application/json"},
    )
    post = opener if opener is not None else _http_post_json
    try:
        payload = post(request)
    except Exception as exc:  # noqa: BLE001 - VL 故障不拖垮一级结果
        meta["error"] = f"{type(exc).__name__}"
        return lines, meta
    meta["parsed"], corrected = _apply_vl_answer(payload, lines)
    return corrected, meta


def _http_post_json(request: urllib.request.Request) -> Any:
    with urllib.request.urlopen(request, timeout=VL_TIMEOUT_SECONDS) as response:  # noqa: S310
        return json.loads(response.read().decode("utf-8"))


def _apply_vl_answer(
    payload: Any, lines: list[OcrLine]
) -> tuple[bool, list[OcrLine]]:
    """解析 VL 应答 → 逐行替换文本(行数/顺序/坐标/置信度全保持)。"""
    try:
        content = payload["choices"][0]["message"]["content"]
    except (KeyError, IndexError, TypeError):
        return False, lines
    match = re.search(r"\[.*\]", str(content), re.DOTALL)
    if not match:
        return False, lines
    try:
        items = json.loads(match.group(0))
    except ValueError:
        return False, lines
    if not isinstance(items, list):
        return False, lines
    out: list[OcrLine] = list(lines)
    hits = 0
    for item in items:
        try:
            index = int(item["i"])
            text = str(item["text"])
        except (KeyError, TypeError, ValueError):
            continue
        if 0 <= index < len(out) and text.strip():
            out[index] = replace(out[index], text=text)
            hits += 1
    return hits > 0, out


# --------------------------------------------------------- 结构化解析 ----

def _is_time_text(text: str) -> bool:
    return bool(TIME_RE.match(text.strip()))


def parse_sessions(
    lines: list[OcrLine], *, limit: int = 20
) -> tuple[list[SessionRow], dict[str, Any]]:
    """C1:全窗 OCR 行 → 会话行(两趟组装,数据驱动定位,零本机像素硬编码)。

    趟 1(高置信):**时间锚**——列表时间列(HH:MM/昨天/周X…)所在行即会话
    行;名字=同行左侧最靠左线,预览=名字下方同 x 线,未读徽标=行右缘徽标带
    内的数字/999+ 短线。
    趟 2(兜底):Vision 偶发漏读时间行(2026-10-11 合成面板实测 8 行漏 5)
    → 名字+预览**对组**恢复(左列同名 x、dy∈PAIR_DY 的上下两线;时间/未读
    尽可能从徽标带回捞,捞不到如实 None)。

    Returns:
        (会话行列表[按窗口自上而下], 命中率 meta)——meta 只含计数(红线 6)。
    """
    time_lines = [line for line in lines if _is_time_text(line.text)]
    row_right = _list_right_edge(lines)
    name_zone_right = row_right - 0.10
    placed: set[int] = set()  # 已消费行的 id()(名字/预览/徽标)
    scored: list[tuple[float, SessionRow]] = []

    if time_lines:
        leftmost = min(line.x for line in time_lines)
        for time_line in sorted(
            (line for line in time_lines if line.x <= leftmost + TIME_CLUSTER_SPAN),
            key=lambda line: line.y,
        ):
            same_row = [
                line
                for line in lines
                if id(line) not in placed
                and abs(line.y - time_line.y) <= NAME_Y_TOL
                and NAME_MIN_X <= line.x < min(time_line.x, name_zone_right)
                and len(line.text.strip()) >= 2
            ]
            if not same_row:
                continue
            name_line = min(same_row, key=lambda line: line.x)
            preview, preview_line = _find_preview(lines, name_line, placed)
            badge, badge_line = _find_badge(lines, row_right, time_line.y, placed)
            placed.update((id(name_line), id(time_line)))
            if preview_line:
                placed.add(id(preview_line))
            if badge_line:
                placed.add(id(badge_line))
            scored.append(
                (
                    name_line.y,
                    SessionRow(
                        name=name_line.text.strip(),
                        unread=badge,
                        time_text=time_line.text.strip(),
                        preview=preview,
                        # conf 取名字行(VL 修字门按名字质量;时间为结构文本,
                        # 误读只丢 time 字段不影响名字)
                        conf=round(name_line.conf, 3),
                    ),
                )
            )

    # 趟 2:名字+预览对组(时间行被漏读的会话行;时间/徽标尽力回捞)
    for line in sorted(lines, key=lambda item: item.y):
        if id(line) in placed or not (
            NAME_MIN_X <= line.x < name_zone_right and len(line.text.strip()) >= 2
        ):
            continue
        pair = next(
            (
                candidate
                for candidate in lines
                if candidate is not line
                and id(candidate) not in placed
                and abs(candidate.x - line.x) <= 0.014
                and PAIR_DY[0] <= candidate.y - line.y <= PAIR_DY[1]
            ),
            None,
        )
        if pair is None:
            continue
        badge, badge_line = _find_badge(
            lines, row_right, line.y, placed, dy_band=(0.005, 0.032)
        )
        placed.update((id(line), id(pair)))
        if badge_line:
            placed.add(id(badge_line))
        scored.append(
            (
                line.y,
                SessionRow(
                    name=line.text.strip(),
                    unread=badge,
                    time_text=None,
                    preview=pair.text.strip(),
                    conf=round(line.conf, 3),
                ),
            )
        )

    scored.sort(key=lambda item: item[0])
    deduped: list[SessionRow] = []
    for _, row in scored:
        if deduped and deduped[-1].name == row.name:
            continue
        deduped.append(row)
        if len(deduped) >= limit:
            break
    meta = {
        "rows": len(deduped),
        "time_anchors": len(time_lines),
        "with_preview": sum(1 for row in deduped if row.preview),
        "with_time": sum(1 for row in deduped if row.time_text),
        "with_unread": sum(1 for row in deduped if row.unread is not None),
        "low_conf_names": sum(1 for row in deduped if row.conf <= CONF_GATE),
    }
    return deduped, meta


def _find_badge(
    lines: list[OcrLine],
    row_right: float,
    row_y: float,
    placed: set[int],
    *,
    dy_band: tuple[float, float] = BADGE_DY,
) -> tuple[int | None, OcrLine | None]:
    """未读徽标:行右缘徽标带([row_right-BADGE_ZONE_WIDTH, row_right+余量])
    内、y 偏移带中的数字/999+ 短线;取最靠右命中(徽标与时间同右对齐)。

    Returns:
        (未读数或 None, 命中行[供消费标记];未命中 → (None, None))。
    """
    hit: tuple[int, OcrLine] | None = None
    for line in lines:
        if id(line) in placed:
            continue
        if not (dy_band[0] <= line.y - row_y <= dy_band[1]):
            continue
        if not (row_right - BADGE_ZONE_WIDTH - BADGE_GAP <= line.x <= row_right + 0.008):
            continue
        if BADGE_RE.match(line.text.strip()):
            text = line.text.strip()
            value = 999 if text == "999+" else int(text)
            if hit is None or line.x > hit[1].x:
                hit = (value, line)
    return hit if hit else (None, None)


def _find_preview(
    lines: list[OcrLine], name_line: OcrLine, placed: set[int]
) -> tuple[str | None, OcrLine | None]:
    """预览行:名字正下方 PREVIEW_DY 带内、同 x 的最近一行。

    Returns:
        (预览文本或 None, 命中行)。
    """
    candidates = [
        line
        for line in lines
        if line is not name_line
        and id(line) not in placed
        and abs(line.x - name_line.x) <= 0.014
        and PREVIEW_DY[0] < line.y - name_line.y <= PREVIEW_DY[1]
    ]
    if not candidates:
        return None, None
    best = min(candidates, key=lambda line: line.y)
    return best.text.strip(), best


@dataclass(frozen=True)
class _MsgBlock:
    """消息流中间块(时间标记/左右气泡原始行)。"""

    side: str
    text: str
    y: float
    x: float
    conf: float


def parse_messages(
    lines: list[OcrLine],
    *,
    k: int = 50,
    title_band_max_y: float = TITLE_MAX_Y,
    body_min_y: float | None = None,
) -> tuple[str | None, list[MessageRow], dict[str, Any]]:
    """C2:聊天区 OCR 行 → (可见标题, 最近 K 条消息行, 命中率 meta)。

    解析规则(误差如实标注,质量上限低于 AX——prd R1a/Phase C 注记):
    居中时间行 = 分段标记(ts 沿用);x > RIGHT_BUBBLE_MIN_X = 自己的气泡;
    左侧短行紧邻下方气泡行 = 发送者名(群聊形态);其余左侧连续行 = 消息
    文本(换行按 WRAP_MERGE_DY 合并)。发送者判定是启发式,可能误标——
    meta.caveat 如实声明。

    ``body_min_y``:消息体 y 下限(全窗传参时默认标题带之下;聊天区裁剪件
    传 0.0——裁剪坐标原点已在消息区顶,无标题带)。
    """
    title: str | None = None
    if title_band_max_y > 0:
        titled = [
            line
            for line in lines
            if line.y <= title_band_max_y and len(line.text.strip()) >= 2
        ]
        if titled:
            top = min(line.y for line in titled)
            title = " ".join(
                line.text.strip()
                for line in sorted(titled, key=lambda l: l.x)
                if abs(line.y - top) <= 0.012
            )
    floor = body_min_y if body_min_y is not None else MSG_TOP_Y - 0.01
    body = [line for line in lines if line.y > floor]
    blocks: list[_MsgBlock] = []
    for line in body:
        text = line.text.strip()
        if not text:
            continue
        center = line.x + line.w / 2
        if _is_time_text(text) and abs(center - 0.5) <= CENTER_TIME_SPAN:
            blocks.append(_MsgBlock("center", text, line.y, line.x, line.conf))
        elif line.x >= RIGHT_BUBBLE_MIN_X:
            blocks.append(_MsgBlock("right", text, line.y, line.x, line.conf))
        else:
            blocks.append(_MsgBlock("left", text, line.y, line.x, line.conf))
    rows = _blocks_to_messages(blocks)
    meta = {
        "blocks": len(blocks),
        "markers": sum(1 for block in blocks if block.side == "center"),
        "left": sum(1 for block in blocks if block.side == "left"),
        "right": sum(1 for block in blocks if block.side == "right"),
        "with_sender": sum(1 for row in rows if row.sender),
        "low_conf_lines": sum(1 for block in blocks if block.conf <= CONF_GATE),
        "caveat": (
            "OCR 逐行读出:发送者名为启发式判定可能误标;换行合并可能并错行;"
            "置信度≤0.5 的行已经/尝试 VL 校对;图片/文件类消息读不出文本"
            "(落「类型+占位」的语义在像素链不可判,缺行即如实缺)"
        ),
    }
    visible_title = title
    return visible_title, rows[-k:] if k else rows, meta


def _blocks_to_messages(blocks: list[_MsgBlock]) -> list[MessageRow]:
    rows: list[MessageRow] = []
    current_ts: str | None = None
    index = 0
    while index < len(blocks):
        block = blocks[index]
        if block.side == "center":
            current_ts = block.text
            index += 1
            continue
        if block.side == "right":
            merged, index = _merge_forward(blocks, index, "right")
            rows.append(MessageRow(current_ts, None, merged.text, "right", merged.conf))
            continue
        # left:先看是否「发送者名 + 下方气泡」形态
        sender: str | None = None
        nxt = blocks[index + 1] if index + 1 < len(blocks) else None
        if (
            nxt is not None
            and nxt.side == "left"
            and SENDER_DY[0] <= nxt.y - block.y <= SENDER_DY[1]
            and len(block.text) <= SENDER_MAX_LEN
            and not _looks_like_wrap(block, _prev_left(blocks, index))
        ):
            sender = block.text
            index += 1
            block = blocks[index]
        merged, index = _merge_forward(blocks, index, "left")
        rows.append(MessageRow(current_ts, sender, merged.text, "left", merged.conf))
    return rows


def _prev_left(blocks: list[_MsgBlock], index: int) -> _MsgBlock | None:
    for candidate in reversed(blocks[:index]):
        if candidate.side == "left":
            return candidate
    return None


def _looks_like_wrap(block: _MsgBlock, prev: _MsgBlock | None) -> bool:
    """与上一左侧行构成换行连续(同消息折行)→ 不当发送者名。"""
    return prev is not None and 0 < block.y - prev.y <= WRAP_MERGE_DY


def _merge_forward(blocks: list[_MsgBlock], index: int, side: str) -> tuple[_MsgBlock, int]:
    """换行合并:同侧、y 紧邻、x 相近的连续行并为一条(中文直连,空格分隔拉丁)。"""
    merged = blocks[index]
    cursor = index + 1
    while cursor < len(blocks):
        nxt = blocks[cursor]
        if nxt.side != side or not (0 < nxt.y - merged.y <= WRAP_MERGE_DY):
            break
        if abs(nxt.x - merged.x) > 0.05:
            break
        joiner = "" if _ends_cjk(merged.text) or not _starts_ascii(nxt.text) else " "
        merged = _MsgBlock(
            side,
            merged.text + joiner + nxt.text,
            merged.y,
            merged.x,
            min(merged.conf, nxt.conf),
        )
        cursor += 1
    return merged, cursor


def _ends_cjk(text: str) -> bool:
    return bool(text) and "\u4e00" <= text[-1] <= "\u9fff"


def _starts_ascii(text: str) -> bool:
    return bool(text) and text[0].isascii() and text[0].isalnum()


# ------------------------------------------------------------ 编排入口 ----

def _fresh_workdir() -> Path:
    """0700 私有工作目录(截图/裁剪件落此,用后即清——红线 6)。"""
    return Path(tempfile.mkdtemp(prefix="wechat-bridge-pixel-"))


def _crop(image_path: Path, box: tuple[float, float, float, float], out_path: Path) -> Path:
    """按归一化框裁剪(窗口内容坐标;产物落私有工作目录)。"""
    from PIL import Image

    with Image.open(image_path) as img:
        width, height = img.size
        left, top, right, bottom = box
        img.crop(
            (
                max(0, round(left * width)),
                max(0, round(top * height)),
                min(width, round(right * width)),
                min(height, round(bottom * height)),
            )
        ).save(out_path, format="PNG")
    return out_path


def _ocr_with_gate(
    image_path: Path,
    workdir: Path,
    *,
    vision_fn: Callable[[Path], tuple[str, list[OcrLine], float]] | None = None,
) -> tuple[list[OcrLine], dict[str, Any]]:
    """一级 OCR(定位/解析用原始几何;VL 校对在**解析后**按行修正)。"""
    vision = vision_fn if vision_fn is not None else vision_ocr
    engine, lines, elapsed = vision(image_path)
    low = sum(1 for line in lines if line.conf <= CONF_GATE)
    meta = {
        "engine": engine,
        "elapsed_s": elapsed,
        "n_lines": len(lines),
        "low_conf_lines": low,
        "conf_gate": CONF_GATE,
    }
    return lines, meta


def _vl_correct_rows(
    image_path: Path,
    workdir: Path,
    fields: list[tuple[int, int, OcrLine]],
    apply: Callable[[int, int, str], None],
    *,
    model_id: str | None = None,
    vl_fn: Callable[..., tuple[list[OcrLine], dict[str, Any]]] | None = None,
) -> dict[str, Any]:
    """二级 VL 校对(解析后按行):低置信行文本送 VL 对照原图修字。

    几何/行序/行数全部以一级 Vision 为准(2026-10-11 实测教训:对全量行做
    VL 校对后再解析,文本改写会让时间锚/名字配对失稳——校对只应改字,不应
    参与定位)。``fields`` = (容器下标, 字段标记, 行);``apply`` 回填修正文本。

    Returns:
        vl meta(used/model/downsampled/error;零内容)。
    """
    if not fields:
        return {"used": False}
    vl = vl_fn if vl_fn is not None else vl_correct_lines
    corrected, info = vl(image_path, [line for _, _, line in fields], workdir, model_id=model_id)
    if not info.get("parsed"):
        return {
            "used": False,
            "attempted": True,
            **{key: info[key] for key in ("model", "downsampled", "error") if key in info},
        }
    hits = 0
    for (container, slot, _), new_line in zip(fields, corrected):
        text = new_line.text.strip()
        if text:
            apply(container, slot, text)
            hits += 1
    return {
        "used": True,
        "corrected_lines": hits,
        **{key: info[key] for key in ("model", "downsampled") if key in info},
    }


def list_sessions(
    config: BridgeConfig,
    limit: int | None = None,
    *,
    window_finder: Callable[[], WindowInfo | None] | None = None,
    capturer: Callable[[WindowInfo, Path], dict[str, Any]] | None = None,
    vision_fn: Callable[[Path], tuple[str, list[OcrLine], float]] | None = None,
    vl_fn: Callable[..., tuple[list[OcrLine], dict[str, Any]]] | None = None,
    model_id: str | None = None,
) -> dict[str, Any]:
    """C1 编排:截主窗 → Vision → 结构化解析 → 低置信行 VL 修字。

    三级链次序=「解析用原始几何,VL 只改字」(全量校对后再解析会让时间锚
    配对失稳,2026-10-11 实测);调用方(cli)已过前置门。
    """
    effective_limit = limit if limit is not None else config.sessions
    find_window = window_finder if window_finder is not None else find_main_window
    window = find_window()
    if window is None:
        raise BridgeError(
            EXIT_GENERIC_FAILURE,
            "CGWindowList 未定位到微信主窗(layer 0)",
            code="screen_capture_failed",
            fix_hint="打开微信主窗口后重试;本地库只读通道(localdb)不受此限",
        )
    capture = capturer if capturer is not None else capture_window
    workdir = _fresh_workdir()
    try:
        capture_result = capture(window, workdir / "window.png")
        lines, ocr_meta = _ocr_with_gate(
            workdir / "window.png", workdir, vision_fn=vision_fn
        )
        sessions, parse_meta = parse_sessions(lines, limit=effective_limit)
        # VL 二级:名字低置信的行(名字+预览成对送检,几何不动只回填文本)
        fields: list[tuple[int, int, OcrLine]] = []
        for index, row in enumerate(sessions):
            if row.conf > CONF_GATE:
                continue
            fields.append((index, 0, OcrLine(row.name, row.conf, 0, 0, 0, 0)))
            if row.preview:
                fields.append((index, 1, OcrLine(row.preview, row.conf, 0, 0, 0, 0)))
        if fields:
            def apply(index: int, slot: int, text: str) -> None:
                row = sessions[index]
                sessions[index] = (
                    replace(row, name=text) if slot == 0 else replace(row, preview=text)
                )

            vl_meta = _vl_correct_rows(
                workdir / "window.png", workdir, fields, apply,
                model_id=model_id, vl_fn=vl_fn,
            )
        else:
            vl_meta = {"used": False}
    finally:
        shutil.rmtree(workdir, ignore_errors=True)
    ocr_meta["vl"] = vl_meta
    return {
        "sessions": [row.to_payload() for row in sessions],
        "count": len(sessions),
        "window": window.to_payload(),
        "capture": {
            key: capture_result[key]
            for key in ("state", "width", "height", "mean_luma")
        },
        "ocr": {**ocr_meta, "parse": parse_meta},
    }


def read_messages(
    config: BridgeConfig,
    chat_id: str,
    k: int | None = None,
    *,
    window_finder: Callable[[], WindowInfo | None] | None = None,
    capturer: Callable[[WindowInfo, Path], dict[str, Any]] | None = None,
    vision_fn: Callable[[Path], tuple[str, list[OcrLine], float]] | None = None,
    vl_fn: Callable[..., tuple[list[OcrLine], dict[str, Any]]] | None = None,
    model_id: str | None = None,
) -> dict[str, Any]:
    """C2 编排:截主窗 → 定位聊天区裁剪 → 三级链 → 最近 K 条。

    静默铁律约束下的**硬边界**:桥不能点击会话切换(合成点击被禁),故读到的
    是**当前打开会话**的消息区;``chat.match`` 如实回报请求 id 与可见标题的
    匹配结果(None=标题不可读),不匹配时载荷照实返回 + ``match=false``,
    消费方自行取舍——绝不静默张冠李戴。
    """
    effective_k = k if k is not None else config.messages
    find_window = window_finder if window_finder is not None else find_main_window
    window = find_window()
    if window is None:
        raise BridgeError(
            EXIT_GENERIC_FAILURE,
            "CGWindowList 未定位到微信主窗(layer 0)",
            code="screen_capture_failed",
            fix_hint="打开微信主窗口后重试;本地库只读通道(localdb)不受此限",
        )
    capture = capturer if capturer is not None else capture_window
    workdir = _fresh_workdir()
    try:
        capture_result = capture(window, workdir / "window.png")
        full_path = workdir / "window.png"
        # 第一遍:全窗 OCR——拿时间锚(列表右缘,裁剪 x)与可见标题
        # (定位趟不接 VL:VL 只校字不挪几何,不花分钟级时延)
        anchor_lines, anchor_meta = _ocr_with_gate(
            full_path, workdir, vision_fn=vision_fn
        )
        list_right = _list_right_edge(anchor_lines)
        title, _, _ = parse_messages(anchor_lines, k=1)
        # 第二遍:聊天区裁剪 OCR(密文本,裁剪后识别质量更高;裁剪件坐标
        # 原点=消息区顶,无标题带 → title_band 关、body 下限 0)
        crop_path = _crop(
            full_path, (list_right, MSG_TOP_Y, 1.0, 1.0), workdir / "messages.png"
        )
        lines, ocr_meta = _ocr_with_gate(crop_path, workdir, vision_fn=vision_fn)
        visible_title, rows, parse_meta = parse_messages(
            lines, k=effective_k, title_band_max_y=-1.0, body_min_y=0.0
        )
        # VL 二级:文本低置信的消息行送检修字(几何不动只回填文本)
        fields = [
            (index, 0, OcrLine(row.text, row.conf, 0, 0, 0, 0))
            for index, row in enumerate(rows)
            if row.conf <= CONF_GATE
        ]
        if fields:
            def apply(index: int, slot: int, text: str) -> None:
                rows[index] = replace(rows[index], text=text)

            vl_meta = _vl_correct_rows(
                crop_path, workdir, fields, apply, model_id=model_id, vl_fn=vl_fn
            )
        else:
            vl_meta = {"used": False}
    finally:
        shutil.rmtree(workdir, ignore_errors=True)
    ocr_meta["vl"] = vl_meta
    match = _chat_match(chat_id, visible_title or title)
    return {
        "messages": [row.to_payload() for row in rows],
        "count": len(rows),
        "chat": {
            "requested_id": chat_id,
            "visible_title": visible_title or title,
            "match": match,
            "note": (
                "像素链静默硬边界:不能点击切换会话(合成点击被禁),读到的是"
                "当前打开会话的消息区;match=false 时请忽略本载荷"
                if match is not True
                else None
            ),
        },
        "window": window.to_payload(),
        "capture": {
            key: capture_result[key]
            for key in ("state", "width", "height", "mean_luma")
        },
        "ocr": {
            **ocr_meta,
            "anchor": {
                "n_lines": anchor_meta["n_lines"],
                "engine": anchor_meta["engine"],
            },
            "parse": parse_meta,
        },
    }


def _list_right_edge(lines: list[OcrLine]) -> float:
    """会话列表右缘(时间锚右缘最大 x + 余量;无锚回落实测缺省 0.215)。"""
    time_lines = [line for line in lines if _is_time_text(line.text)]
    if not time_lines:
        return 0.215
    leftmost = min(line.x for line in time_lines)
    anchored = [line for line in time_lines if line.x <= leftmost + TIME_CLUSTER_SPAN]
    return min(0.35, max(line.x + line.w for line in anchored) + 0.01)


def _chat_match(requested: str, visible_title: str | None) -> bool | None:
    """请求 id 与可见标题匹配判定(True/False;标题不可读 → None 如实)。

    NFKC 全半角归一(2026-10-14 真机实证:备注半角括号 vs 标题带全角
    括号,不归一恒不匹配;navfilter.compact 同味)。"""
    import unicodedata

    if not visible_title:
        return None
    want = re.sub(r"\s+", "", unicodedata.normalize("NFKC", requested))
    have = re.sub(r"\s+", "", unicodedata.normalize("NFKC", visible_title))
    if not want:
        return None
    return want in have or have in want
