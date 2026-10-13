"""搜索结果面板的分区过滤选行纯逻辑 + 三段坐标换算链(task
10-14-wechat-send-text design §B-3;tonyshield ref_search_click.sh 算法
+ 三处增强;降级通道 CGEvent+OCR 导航的选行器)。

纯逻辑模块:**零平台调用、零桥内其它模块 import(仅 stdlib)**——单测
主战场(design §A)。

来源与增强(REF = research/ref_search_click.sh 内嵌 python):

- 分区头定位(REF:53-59 最下本地头)——增强①:补「功能分类」族垃圾
  分区头集合,``y_junk`` 排除锚优先于 ``y_local``;
- 评分选行(REF:69-74 全等/前缀/包含)与并列取 y 最大再 x 最小
  (REF:80-97);
- 增强②:unique-row 兜底——emoji 行 OCR 名乱/不匹配时的「行在但名读
  不出」救援(候选恰 1 行且分区头在场才采;**不救**「行完全没读出」,
  0 候选 → None 拒发绝不猜,design §J-9);
- 增强③:**三段坐标换算链**——OcrLine 坐标是 ``SEARCH_PANE_BOX`` 裁剪图
  归一化 0-1(pixel.vision_ocr 输出坐标系),必须先 pane→window 再
  window→screen,直接当全窗用会系统性偏左上(design §J-3)。

坐标契约(design §B-3,docstring 写死)::

    select_result_row(lines, terms) 的 lines 与返回的 RowPick.cx/cy
    一律为 SEARCH_PANE_BOX 裁剪图内归一化 0-1(原点左上);
    pane_to_window → 全窗归一化;row_box_to_screen → 屏幕绝对像素
    (kCGWindowBounds 同系:原点主屏左上、Y 向下,与 CGEvent 鼠标坐标
    一致)。
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
    "SEARCH_PANE_BOX",
    "RowPick",
    "compact",
    "pane_to_window",
    "row_box_to_screen",
    "select_result_row",
]

#: 本地结果分区头(REF:53 六项 + 朋友圈)。
LOCAL_HEADERS = frozenset({"群聊", "联系人", "聊天记录", "公众号", "服务号", "小程序", "朋友圈"})
#: 非本地/功能分类分区头(其下候选一律排除;★补 REF 缺的「功能分类」族)。
JUNK_HEADERS = frozenset(
    {
        "搜一搜",
        "功能",
        "功能分类",
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
#: 搜索结果面板 OCR 区(窗口内容归一化;全左栏,分区头逻辑做主裁;
#: P9 预验校准注记:design §I-7,几何漂移先改本常量再进 P10)。
SEARCH_PANE_BOX = (0.0, 0.10, 0.32, 0.88)

#: 候选行必须落在分区头锚之上的容差(REF:83 同款 -0.003)。
_LIMIT_TOLERANCE = 0.003


@dataclass(frozen=True)
class RowPick:
    """选中行(坐标 = SEARCH_PANE_BOX 裁剪图归一化,design §J-3)。"""

    cx: float
    cy: float
    rule: str  # "text_match" | "unique_row"
    term: str  # 命中的匹配词(unique_row = "")


def compact(text: str) -> str:
    """去全部空白 + casefold(展示名/行文比对形态)。"""
    return re.sub(r"\s+", "", text or "").casefold()


def _line_y(line: "OcrLine") -> float:
    return float(getattr(line, "y", 0.0))


def _line_text(line: "OcrLine") -> str:
    return str(getattr(line, "text", "") or "")


def select_result_row(
    lines: Sequence["OcrLine"], terms: Sequence[str]
) -> RowPick | None:
    """分区过滤 + 评分选行(零平台调用;REF 算法 + 增强项)。

    **坐标契约:lines 的 x/y/w/h 一律为 SEARCH_PANE_BOX 裁剪图内归一化
    0-1**(与 pixel.vision_ocr 的输出坐标系一致);返回的 RowPick 同系。

    步骤(design §B-3):

    1. 分区头定位:y_local = 最下本地头 y;junk 头取最上(``min``)——
       ``limit = y_junk if 在场 else y_local if 在场 else None``;
    2. 候选 = 有文本(OcrLine.text 去空白非空;OCR 吐出的行哪怕乱码也算
       ——unique-row 的可达前提)、非分区头、y < limit - 0.003 的行;
       limit None(分区头全没 OCR 出来)→ 候选 = 全部非分区头有文本行;
    3. 文本评分:每候选取最优 (term_rank, score),score:全等=0 / 前缀=1 /
       包含=2;terms 按序即 rank;
    4. 并列取 y 最大、再 x 最小(sorted key=(score_tuple, -y, x) 取首);
    5. unique_row 兜底:无任何文本命中 且 候选恰 1 行 且 limit 在场 →
       采纳该行(rule="unique_row")——救「行在但名读不出」,不救
       「行完全没读出」(0 候选 → None 拒发,绝不猜);
    6. 无命中 → None(调用方 exit 15 拒,绝不盲回车)。

    点击点 = 行文本本体中心(cx = x + w/2 避头像,cy = y + h/2)。
    """
    # —— 1. 分区头锚 ——
    y_local: float | None = None
    y_junk: float | None = None
    for line in lines:
        key = compact(_line_text(line))
        if not key:
            continue
        if key in LOCAL_HEADERS:
            y = _line_y(line)
            y_local = y if y_local is None else max(y_local, y)
        elif key in JUNK_HEADERS:
            y = _line_y(line)
            y_junk = y if y_junk is None else min(y_junk, y)
    limit = y_junk if y_junk is not None else y_local

    # —— 2. 候选行 ——
    header_keys = LOCAL_HEADERS | JUNK_HEADERS
    candidates = []
    for line in lines:
        text = compact(_line_text(line))
        if not text or text in header_keys:
            continue
        if limit is not None and _line_y(line) >= limit - _LIMIT_TOLERANCE:
            continue
        candidates.append(line)
    if not candidates:
        return None

    # —— 3/4. 文本评分 + 并列取 y 最大再 x 最小 ——
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
            key = ((rank, score), -_line_y(line), float(getattr(line, "x", 0.0)), line, term)
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
    if limit is not None and len(candidates) == 1:
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
