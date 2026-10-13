"""navfilter 单测(design §B-3/§G;纯逻辑,零平台调用)。

坐标契约钉死:lines 与 RowPick 一律为 SEARCH_PANE_BOX 裁剪图归一化 0-1;
三段换算链端到端 = 裁剪系 fixture → pane_to_window → row_box_to_screen
(design §J-3:直接当全窗用会系统性偏左上)。
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

COMPONENT_SRC = Path(__file__).resolve().parents[2] / "plugins" / "wechat-bridge"
if str(COMPONENT_SRC) not in sys.path:
    sys.path.insert(0, str(COMPONENT_SRC))

import wechat_bridge.navfilter as navfilter  # noqa: E402
from wechat_bridge.navfilter import (  # noqa: E402
    JUNK_HEADERS,
    LOCAL_HEADERS,
    SEARCH_PANE_BOX,
    RowPick,
    compact,
    pane_to_window,
    row_box_to_screen,
    select_result_row,
)
from wechat_bridge.pixel import OcrLine, WindowInfo  # noqa: E402

approx = pytest.approx


def line(text: str, x: float, y: float, w: float = 0.2, h: float = 0.03, conf: float = 0.9) -> OcrLine:
    return OcrLine(text=text, conf=conf, x=x, y=y, w=w, h=h)


class TestCompact:
    def test_strips_whitespace_and_casefolds(self) -> None:
        assert compact("  File Helper\n\t") == "filehelper"
        assert compact("文件 传输助手") == "文件传输助手"

    def test_empty_is_empty(self) -> None:
        assert compact("") == ""
        assert compact("   ") == ""


class TestHeaderSets:
    def test_local_headers_cover_ref_six_plus_moments(self) -> None:
        for name in ("群聊", "联系人", "聊天记录", "公众号", "服务号", "小程序", "朋友圈"):
            assert name in LOCAL_HEADERS

    def test_junk_headers_cover_fenced_groups(self) -> None:
        for name in ("搜一搜", "功能", "功能分类", "文章", "智能工具", "朋友圈动态"):
            assert name in JUNK_HEADERS


class TestSelectResultRow:
    def test_text_match_below_junk_excluded(self) -> None:
        """命中行在锚(limit)之上被选中;junk 头之下的行被排除。

        坐标语义(design §B-3 步骤 2):候选 = y < limit - 0.003——
        limit = y_junk(在场时),即垃圾分区头之上的行才可点。
        """
        lines = [
            line("文件传输助手", 0.03, 0.25),  # 锚之上:可选
            line("搜一搜", 0.02, 0.60),
            line("文件传输助手广告", 0.03, 0.75),  # junk 分区之下,必须排除
        ]
        pick = select_result_row(lines, ["文件传输助手"])
        assert pick is not None
        assert pick.rule == "text_match"
        assert pick.term == "文件传输助手"
        assert pick.cy == approx(0.25 + 0.03 / 2)

    def test_junk_anchor_wins_over_local_anchor(self) -> None:
        """junk 头在场时以 junk 头为排除锚(比最下本地头更紧)。"""
        lines = [
            line("聊天记录", 0.02, 0.05),  # local 头(锚更松)
            line("目标会话", 0.03, 0.25),
            line("搜一搜", 0.02, 0.50),  # junk 头(锚更紧,优先)
            line("目标会话", 0.03, 0.55),  # junk 之下,排除
        ]
        pick = select_result_row(lines, ["目标会话"])
        assert pick is not None
        assert pick.cy == approx(0.25 + 0.015)

    def test_no_headers_all_rows_are_candidates(self) -> None:
        """分区头全没 OCR 出来(limit None)→ 全部有文本行为候选。"""
        lines = [line("目标会话", 0.03, 0.90)]
        pick = select_result_row(lines, ["目标会话"])
        assert pick is not None and pick.rule == "text_match"

    def test_tie_break_prefers_lowest_y_then_smallest_x(self) -> None:
        """并列(同 term 同分)取 y 最大、再 x 最小(REF:80-97)。"""
        lines = [
            line("同名群", 0.10, 0.30),
            line("同名群", 0.05, 0.50),  # y 更大 → 胜
        ]
        pick = select_result_row(lines, ["同名群"])
        assert pick is not None
        assert pick.cy == approx(0.50 + 0.015)

    def test_exact_beats_prefix_beats_contains(self) -> None:
        """评分序:全等 0 / 前缀 1 / 包含 2;term 序即优先级。"""
        lines = [
            line("目标会话(工作)", 0.03, 0.60),  # 前缀(term1)
            line("目标会话", 0.03, 0.40),  # 全等(term1)
            line("讨论目标会话", 0.03, 0.50),  # 包含(term1)
        ]
        pick = select_result_row(lines, ["目标会话"])
        assert pick is not None and pick.cy == approx(0.40 + 0.015)
        # term_rank 优先:低 rank 的包含胜过高 rank 的全等
        pick2 = select_result_row(lines, ["无关词", "讨论目标会话"])
        assert pick2 is not None and pick2.cy == approx(0.50 + 0.015)

    def test_unique_row_adopted_for_garbled_single_candidate(self) -> None:
        """unique-row 兜底:emoji 行被 OCR 读成乱码(与 terms 全不匹配)、
        候选恰 1 行且分区头在场 → 采纳(design §J-9「行在名读不出」)。"""
        lines = [
            line("联系人", 0.02, 0.60),  # 分区头(锚)
            line(".cert.=:)", 0.03, 0.42),  # 🐳 行乱码(锚之上,唯一候选)
        ]
        pick = select_result_row(lines, ["🐳", "jiangliushi666"])
        assert pick is not None
        assert pick.rule == "unique_row"
        assert pick.term == ""

    def test_unique_row_rejected_when_zero_candidates(self) -> None:
        """OCR 零文本行(行完全没读出,候选 0)→ None 拒发,绝不猜。"""
        lines = [line("联系人", 0.02, 0.30)]  # 只有分区头
        assert select_result_row(lines, ["🐳"]) is None

    def test_unique_row_rejected_when_multiple_candidates(self) -> None:
        """候选 ≥2 且无命中 → 不触发兜底(猜哪个都是赌)。"""
        lines = [
            line("联系人", 0.02, 0.60),
            line(".cert.=:)", 0.03, 0.42),
            line("::..~", 0.03, 0.52),
        ]
        assert select_result_row(lines, ["🐳"]) is None

    def test_click_point_is_text_center_avoiding_avatar(self) -> None:
        """点击点 = 行文本本体中心(cx = x + w/2 避头像)。"""
        lines = [line("目标会话", x=0.10, y=0.40, w=0.20, h=0.04)]
        pick = select_result_row(lines, ["目标会话"])
        assert pick is not None
        assert pick.cx == approx(0.10 + 0.10)
        assert pick.cy == approx(0.40 + 0.02)


class TestCoordinateChain:
    """三段换算链端到端(design §J-3):裁剪系 → 全窗 → 屏幕像素。"""

    def test_pane_to_window(self) -> None:
        wx, wy = pane_to_window(SEARCH_PANE_BOX, 0.5, 0.5)
        assert wx == approx(SEARCH_PANE_BOX[0] + 0.5 * SEARCH_PANE_BOX[2])
        assert wy == approx(SEARCH_PANE_BOX[1] + 0.5 * SEARCH_PANE_BOX[3])

    def test_row_box_to_screen_uses_window_origin(self) -> None:
        window = WindowInfo(window_id=1, onscreen=True, width=800, height=600, x=100, y=200)
        sx, sy = row_box_to_screen(window, 0.5, 0.25)
        assert (sx, sy) == (round(100 + 0.5 * 800), round(200 + 0.25 * 600))
        assert (sx, sy) == (500, 350)

    def test_end_to_end_cropped_fixture_to_screen(self) -> None:
        """裁剪系 fixture(全左栏内一行)→ 屏幕绝对像素:直接当全窗用会
        系统性偏左上(反例断言换算链确实生效)。"""
        window = WindowInfo(window_id=1, onscreen=True, width=800, height=600, x=100, y=200)
        pick = RowPick(cx=0.5, cy=0.5, rule="text_match", term="x")
        wx, wy = pane_to_window(SEARCH_PANE_BOX, pick.cx, pick.cy)
        sx, sy = row_box_to_screen(window, wx, wy)
        # pane 原点 (0, 0.10)、尺寸 (0.32, 0.88):中心 → 全窗 (0.16, 0.54)
        assert (sx, sy) == (round(100 + 0.16 * 800), round(200 + 0.54 * 600))
        assert (sx, sy) == (228, 524)
        # 反例:裸当全窗换算会得到 (500, 500) —— 偏右下,系统性错位。
        naive = (round(100 + pick.cx * 800), round(200 + pick.cy * 600))
        assert naive != (sx, sy)

    def test_window_xy_defaults_zero(self) -> None:
        """旧构造(无 x/y)缺省 0 —— 向后兼容。"""
        window = WindowInfo(window_id=1, onscreen=True, width=100, height=100)
        assert (window.x, window.y) == (0.0, 0.0)
        assert row_box_to_screen(window, 0.5, 0.5) == (50, 50)

