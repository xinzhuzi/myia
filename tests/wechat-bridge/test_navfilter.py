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

    def test_function_headers_are_local_not_junk(self) -> None:
        """勘误回归(真机实证):功能/功能分类=本地功能分区,曾在 JUNK。"""
        assert "功能" in LOCAL_HEADERS and "功能" not in JUNK_HEADERS
        assert "功能分类" in LOCAL_HEADERS and "功能分类" not in JUNK_HEADERS
        for name in ("最常使用", "常用"):
            assert name in LOCAL_HEADERS

    def test_network_tokens_cover_real_header_render(self) -> None:
        """网络区锚(主人抓障 2026-10-14:「每次都搜索网络结果」)。"""
        for token in ("搜索网络结果", "搜一搜", "网络结果"):
            assert token in navfilter.NETWORK_TOKENS


class TestSelectResultRow:
    def test_real_layout_network_top_local_band(self) -> None:
        """真机布局回归(/tmp/wxsend-e2e/r3/float-evidence.png 位置化取证,
        2026-10-14):网络区置顶 + Q 联想 + 功能带内目标行 + 深区同名行——
        必须选功能带内那行,网络行/回显/深区同名行永不中。"""
        lines = [
            line("大 搜索网络结果", 0.10, 0.028),
            line("Q", 0.10, 0.081, w=0.03),
            line("文件传输助手", 0.139, 0.081, w=0.2),  # 输入回显(网络区下、功能带上)
            line("Q 文件传输助手打开", 0.103, 0.135),
            line("Q 文件传输助手恢复数据", 0.103, 0.190),
            line("功能", 0.098, 0.351),
            line("文件传输助手", 0.212, 0.421),  # ★目标行(功能带内)
            line("聊天记录", 0.095, 0.499),
            line("文件传输助手", 0.209, 0.728),  # 深区同名行(聊天记录带)
        ]
        pick = select_result_row(lines, ["文件传输助手"])
        assert pick is not None and pick.rule == "text_match"
        assert pick.cy == approx(0.421 + 0.015)  # 功能带内行,非深区同名

    def test_no_local_header_never_guesses(self) -> None:
        """无本地分区锚 → None 绝不猜——网络联想行/回显永不入候选
        (旧版 limit=None 时全行候选的洞,主人抓障根因)。"""
        lines = [
            line("搜索网络结果", 0.10, 0.028),
            line("文件传输助手", 0.139, 0.081),
            line("Q 文件传输助手打开", 0.103, 0.135),
        ]
        assert select_result_row(lines, ["文件传输助手"]) is None

    def test_band_bottom_excludes_deeper_sections(self) -> None:
        """候选带止于下一个分区头:更深分区的行(哪怕全等)不入带。"""
        lines = [
            line("功能", 0.098, 0.35),
            line("目标会话", 0.21, 0.42),
            line("文章", 0.095, 0.50),  # junk 分区头=带底
            line("目标会话", 0.21, 0.60),  # 带外
        ]
        pick = select_result_row(lines, ["目标会话"])
        assert pick is not None and pick.cy == approx(0.42 + 0.015)

    def test_tie_break_prefers_topmost_in_band(self) -> None:
        """并列(同 term 同分)取带内最上(y 最小)——旧版取 y 最大的
        平局规则会把同名深区行点错(勘误)。"""
        lines = [
            line("联系人", 0.02, 0.10),
            line("同名群", 0.05, 0.30),
            line("同名群", 0.10, 0.50),
        ]
        pick = select_result_row(lines, ["同名群"])
        assert pick is not None and pick.cy == approx(0.30 + 0.015)

    def test_exact_beats_prefix_beats_contains_in_band(self) -> None:
        """评分序:全等 0 / 前缀 1 / 包含 2;term 序即优先级(带内)。"""
        lines = [
            line("联系人", 0.02, 0.10),
            line("目标会话(工作)", 0.03, 0.30),  # 前缀
            line("目标会话", 0.03, 0.20),  # 全等
            line("讨论目标会话", 0.03, 0.25),  # 包含
        ]
        pick = select_result_row(lines, ["目标会话"])
        assert pick is not None and pick.cy == approx(0.20 + 0.015)
        pick2 = select_result_row(lines, ["无关词", "讨论目标会话"])
        assert pick2 is not None and pick2.cy == approx(0.25 + 0.015)

    def test_unique_row_adopted_for_garbled_single_candidate(self) -> None:
        """unique-row 兜底:emoji 行 OCR 乱码、带内恰 1 行且本地头在场。"""
        lines = [
            line("联系人", 0.02, 0.10),
            line(".cert.=:)", 0.03, 0.42),
        ]
        pick = select_result_row(lines, ["🐳", "jiangliushi666"])
        assert pick is not None and pick.rule == "unique_row" and pick.term == ""

    def test_unique_row_rejected_when_zero_candidates(self) -> None:
        """OCR 零文本行(候选 0)→ None 拒发,绝不猜。"""
        lines = [line("联系人", 0.02, 0.30)]
        assert select_result_row(lines, ["🐳"]) is None

    def test_unique_row_rejected_when_multiple_candidates(self) -> None:
        """带内候选 ≥2 且无命中 → 不触发兜底。"""
        lines = [
            line("联系人", 0.02, 0.10),
            line(".cert.=:)", 0.03, 0.42),
            line("::..~", 0.03, 0.52),
        ]
        assert select_result_row(lines, ["🐳"]) is None

    def test_click_point_is_text_center_avoiding_avatar(self) -> None:
        """点击点 = 行文本本体中心(cx = x + w/2 避头像)。"""
        lines = [
            line("功能", 0.02, 0.10),
            line("目标会话", x=0.10, y=0.40, w=0.20, h=0.04),
        ]
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

