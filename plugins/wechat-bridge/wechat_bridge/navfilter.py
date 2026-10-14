"""搜索结果面板的分区过滤选行纯逻辑 + 三段坐标换算链(task
10-14-wechat-send-text design §B-3;tonyshield ref_search_click.sh 算法
根型 + 2026-10-14 按真机布局重写)。

纯逻辑模块:**零平台调用、零桥内其它模块 import(仅 stdlib)**——单测
主战场(design §A)。

真机布局实证(2026-10-14 /tmp/wxsend-e2e/r3/float-evidence.png 位置化
OCR,主人抓障「每次都搜索网络结果」后取证)::

    y=0.028  搜索网络结果        ← 网络区(顶部!)
    y=0.081  Q / <输入回显>      ← 搜索框回显
    y=0.135+ Q <词>+<联想尾>     ← 网络联想行(Q 前缀族)
    y=0.351  功能                ← 本地分区头(★曾在 JUNK,勘误:本地!)
    y=0.421  <目标行>            ← 要点的行
    y=0.499  聊天记录            ← 更深本地分区
    y=0.560+ 聊天记录行…

即 4.1.15 的浮窗是「网络区在上、本地分区在下」——tonyshield 原算法的
「垃圾在底、取锚上方行」假设整体不成立,旧实现靠 OCR 漏读分区头 +
``y 最大`` 平局侥幸点对过。本版语义:

1. 网络区锚:文本**包含** :data:`NETWORK_TOKENS` 任一词(OCR 会带图标
   前缀,如「大 搜索网络结果」→ containment 匹配)或 Q 联想行形态;
2. 本地分区头锚:精确命中 :data:`LOCAL_HEADERS`(功能/功能分类勘误
   归本地;补最常使用/常用);
3. 候选带 = 首个位于网络区之下的本地头 → 下一个任意分区头(开区间);
   **无本地头 → None 拒发绝不猜**(网络联想行永不入候选);
4. 评分全等=0/前缀=1/包含=2(terms 按序即 rank);并列取带内最上
   (y 最小)再 x 最小——同名行常在更深聊天记录区再现,取带内首段;
5. unique-row 兜底:带内恰 1 行且本地头在场才采(救「名读不出」)。

坐标契约(design §B-3,docstring 写死)::

    select_result_row(lines, terms) 的 lines 与返回的 RowPick.cx/cy
    一律为裁剪图内归一化 0-1(原点左上);pane_to_window → 全窗归一化;
    row_box_to_screen → 屏幕绝对像素(kCGWindowBounds 同系:原点主屏
    左上、Y 向下,与 CGEvent 鼠标坐标一致)。
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import TYPE_CHECKING, Sequence

if TYPE_CHECKING:  # 仅类型引用;运行时零桥内依赖(鸭子类型,OcrLine 同形)
    from .pixel import OcrLine, WindowInfo

__all__ = [
    "JUNK_HEADERS",
    "LOCAL_HEADERS",
    "NETWORK_TOKENS",
    "SEARCH_PANE_BOX",
    "RowPick",
    "compact",
    "pane_to_window",
    "row_box_to_screen",
    "select_result_row",
]

#: 本地结果分区头(真机实证:功能/功能分类=本地功能分区,勘误自 JUNK;
#: 最常使用/常用=搜索首段常见头)。
LOCAL_HEADERS = frozenset(
    {
        "群聊",
        "联系人",
        "聊天记录",
        "公众号",
        "服务号",
        "小程序",
        "朋友圈",
        "功能",
        "功能分类",
        "最常使用",
        "常用",
    }
)
#: 兜底垃圾分区头(其下整段排除;真机布局下网络区靠 NETWORK_TOKENS
#: containment 锚,此处仅兜更深的非目标分区)。
JUNK_HEADERS = frozenset(
    {
        "文章",
        "智能工具",
        "朋友圈动态",
        "表情",
        "视频号",
        "直播",
        "新闻",
        "购物",
        "小程序码",
    }
)
#: 网络区锚( containment 匹配——OCR 常带图标前缀,如「大 搜索网络结果」;
#: 主人抓障 2026-10-14:此区每次搜索都置顶出现,永不点击)。
NETWORK_TOKENS = ("搜索网络结果", "搜一搜", "网络结果")
#: 搜索结果面板 OCR 区(窗口内容归一化;全左栏,分区头逻辑做主裁;
#: P9 预验校准注记:design §I-7,几何漂移先改本常量再进 P10)。
SEARCH_PANE_BOX = (0.0, 0.10, 0.32, 0.88)


@dataclass(frozen=True)
class RowPick:
    """选中行(坐标 = 裁剪图归一化,design §J-3)。"""

    cx: float
    cy: float
    rule: str  # "text_match" | "unique_row"
    term: str  # 命中的匹配词(unique_row = "")


def compact(text: str) -> str:
    """NFKC 全半角归一 + 去全部空白 + casefold(展示名/行文比对形态)。

    全半角归一(2026-10-14 真机实证:备注「竹海晨金(分身)」半角括号,
    微信界面渲染全角「竹海晨金（分身）」,不归一则三连匹配全空;
    WZ:127-129 widthInsensitive 同味)。
    """
    import unicodedata

    return re.sub(r"\s+", "", unicodedata.normalize("NFKC", text or "")).casefold()


def _line_y(line: "OcrLine") -> float:
    return float(getattr(line, "y", 0.0))


def _line_text(line: "OcrLine") -> str:
    return str(getattr(line, "text", "") or "")


def _is_network_row(text_compact: str) -> bool:
    """网络区行(头行 containment + Q 联想行形态)。"""
    if any(token in text_compact for token in NETWORK_TOKENS):
        return True
    return text_compact.startswith("q") and len(text_compact) > 1


def select_result_row(
    lines: Sequence["OcrLine"], terms: Sequence[str]
) -> RowPick | None:
    """分区带过滤 + 评分选行(零平台调用;真机布局语义,模块 docstring)。

    步骤:

    1. 锚定:网络区头 y(最上 containment/Q 行);全部本地头 y(升序);
    2. 候选带 = (网络区之下首个本地头, 下一个任意分区头);无本地头 →
       None(绝不猜,网络联想行永不入候选);
    3. 带内候选 = 有文本、非任何分区头、非网络行;
    4. 评分(全等=0/前缀=1/包含=2,terms 序=rank),并列取带内最上
       (y 最小)再 x 最小;
    5. unique-row 兜底:带内恰 1 行才采;
    6. 无命中 → None(调用方 exit 15 拒,绝不盲回车)。

    点击点 = 行文本本体中心(cx = x + w/2 避头像,cy = y + h/2)。
    """
    # —— 1. 锚 ——
    y_network: float | None = None
    local_ys: list[float] = []
    header_rows: list[tuple[float, str]] = []  # (y, compact) 全部分区头
    for line in lines:
        text = compact(_line_text(line))
        if not text:
            continue
        y = _line_y(line)
        if _is_network_row(text):
            y_network = y if y_network is None else min(y_network, y)
            continue
        if text in LOCAL_HEADERS:
            local_ys.append(y)
            header_rows.append((y, text))
        elif text in JUNK_HEADERS:
            header_rows.append((y, text))
    if not local_ys:
        return None  # 无本地分区锚:绝不猜(网络联想行永不点)

    # —— 2. 候选带:网络区之下首个本地头 → 下一个任意分区头 ——
    band_top = min(
        (y for y in local_ys if y_network is None or y > y_network),
        default=min(local_ys),
    )
    header_ys = sorted({y for y, _ in header_rows})
    nexts = [y for y in header_ys if y > band_top + 1e-4]
    band_bottom = min(nexts) if nexts else 1.0

    # —— 3. 带内候选 ——
    network_texts = {id(l) for l in lines if _is_network_row(compact(_line_text(l)))}
    all_header_y = {y for y, _ in header_rows} | set(local_ys)
    candidates = []
    for line in lines:
        text = compact(_line_text(line))
        if not text or id(line) in network_texts:
            continue
        y = _line_y(line)
        if any(abs(y - hy) < 1e-4 for hy in all_header_y):
            continue
        if not (band_top + 1e-4 < y < band_bottom - 1e-4):
            continue
        candidates.append(line)
    if not candidates:
        return None

    # —— 4. 评分 + 并列取带内最上(y 最小)再 x 最小 ——
    best: tuple[tuple[int, int], float, float, "OcrLine", str] | None = None
    for line in candidates:
        line_text = compact(_line_text(line))
        for rank, term in enumerate(terms):
            term_text = compact(term)
            if not term_text:
                continue
            if line_text == term_text:
                score = 0
            elif line_text.startswith(term_text):
                score = 1
            elif term_text in line_text:
                score = 2
            else:
                continue
            key = ((rank, score), _line_y(line), float(getattr(line, "x", 0.0)), line, term)
            if best is None or key[:3] < best[:3]:
                best = key
    if best is not None:
        line = best[3]
        return RowPick(
            cx=float(getattr(line, "x", 0.0)) + float(getattr(line, "w", 0.0)) / 2,
            cy=_line_y(line) + float(getattr(line, "h", 0.0)) / 2,
            rule="text_match",
            term=best[4],
        )

    # —— 5. unique-row 兜底 ——
    if len(candidates) == 1:
        line = candidates[0]
        return RowPick(
            cx=float(getattr(line, "x", 0.0)) + float(getattr(line, "w", 0.0)) / 2,
            cy=_line_y(line) + float(getattr(line, "h", 0.0)) / 2,
            rule="unique_row",
            term="",
        )
    return None


def pane_to_window(
    pane_box: tuple[float, float, float, float],
    cx: float,
    cy: float,
) -> tuple[float, float]:
    """第二段换算:裁剪系归一化 → 全窗归一化。

    ``wx = pane_box[0] + cx * pane_box[2]``;``wy = pane_box[1] + cy *
    pane_box[3]``。
    """
    return (
        pane_box[0] + cx * pane_box[2],
        pane_box[1] + cy * pane_box[3],
    )


def row_box_to_screen(
    window: "WindowInfo", wx: float, wy: float
) -> tuple[int, int]:
    """第三段换算:全窗归一化 → 屏幕绝对像素。

    ``round(window.x + wx * window.width)`` / ``round(window.y + wy *
    window.height)``(依赖 WindowInfo 的 x/y 字段,kCGWindowBounds 同系:
    原点主屏左上、Y 向下 = CGEvent 鼠标坐标系)。
    """
    return (
        round(float(window.x) + wx * float(window.width)),
        round(float(window.y) + wy * float(window.height)),
    )
