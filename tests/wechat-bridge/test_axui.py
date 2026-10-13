"""axui 单测(design §B-2/§G;osascript 全 mock——_run/_text 注入,
零真实 System Events 调用;脚本形状与双判据逻辑是受测面)。

真机可达性(元素名/AXPress 行为)= P9 预验项(design §I-7),
本文件只锁脚本形状与判定逻辑。
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest

COMPONENT_SRC = Path(__file__).resolve().parents[2] / "plugins" / "wechat-bridge"
if str(COMPONENT_SRC) not in sys.path:
    sys.path.insert(0, str(COMPONENT_SRC))

import wechat_bridge.axui as axui  # noqa: E402
from wechat_bridge.codes import TIMEOUT, BridgeError  # noqa: E402


def _proc_ok(stdout: str = "true\n") -> subprocess.CompletedProcess[bytes]:
    return subprocess.CompletedProcess(
        args=[], returncode=0, stdout=stdout.encode("utf-8"), stderr=b""
    )


def _proc_fail() -> subprocess.CompletedProcess[bytes]:
    return subprocess.CompletedProcess(
        args=[], returncode=1, stdout=b"", stderr=b"boom"
    )


class TestProbeDualGate:
    """probe_wechat_ax 双判据(design §D-1/§J-4/13):门开 + 输入区可读。"""

    def test_gate_open_and_input_readable_is_true(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setattr(axui, "read_input_value", lambda: "")
        assert axui.probe_wechat_ax(node_count=lambda: 122) is True

    def test_gate_open_without_input_field_is_false(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """「label 可读、输入区不可写」的半开态 → False(走降级链,§J-4)。"""
        monkeypatch.setattr(axui, "read_input_value", lambda: None)
        assert axui.probe_wechat_ax(node_count=lambda: 122) is False

    def test_gate_closed_is_false_even_with_input(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setattr(axui, "read_input_value", lambda: "内容")
        assert axui.probe_wechat_ax(node_count=lambda: 5) is False
        assert axui.probe_wechat_ax(node_count=lambda: 0) is False

    def test_node_count_unknown_is_false(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """探测不可及(None)→ 保守 False(不猜门态)。"""
        monkeypatch.setattr(axui, "read_input_value", lambda: "")
        assert axui.probe_wechat_ax(node_count=lambda: None) is False


class TestScriptShapes:
    """osascript 脚本形状(mock _run;参数经 argv 传递零转义面)。"""

    def test_write_search_value_script_sets_axvalue_of_focused(self, monkeypatch: pytest.MonkeyPatch) -> None:
        seen: dict = {}

        def fake_run(argv: list[str]) -> subprocess.CompletedProcess[bytes]:
            seen["argv"] = argv
            return _proc_ok()

        monkeypatch.setattr(axui, "_run", fake_run)
        assert axui.write_search_value("jiangliushi666") is True
        script = seen["argv"][2]
        assert "AXFocusedUIElement" in script and "AXValue" in script
        assert "jiangliushi666" not in script  # 正文/搜索词不进脚本拼接
        assert seen["argv"][-2:] == ["--", "jiangliushi666"]  # argv 传参

    def test_write_search_value_failure_returns_false(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setattr(axui, "_run", lambda argv: _proc_fail())
        assert axui.write_search_value("x") is False

    def test_press_session_item_matches_prefix_and_contains(self, monkeypatch: pytest.MonkeyPatch) -> None:
        seen: dict = {}

        def fake_run(argv: list[str]) -> subprocess.CompletedProcess[bytes]:
            seen["argv"] = argv
            return _proc_ok()

        monkeypatch.setattr(axui, "_run", fake_run)
        assert axui.press_session_item("🐳") is True
        script = seen["argv"][2]
        assert 'starts with "session_item_"' in script
        assert "contains theArg" in script
        assert "AXPress" in script
        assert seen["argv"][-1] == "🐳"

    def test_read_current_chat_name_none_on_missing(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setattr(axui, "_run", lambda argv: _proc_ok(""))  # missing value → 空输出
        assert axui.read_current_chat_name() is None
        monkeypatch.setattr(axui, "_run", lambda argv: _proc_ok("AI中转站\n"))
        assert axui.read_current_chat_name() == "AI中转站"

    def test_read_input_value_distinguishes_empty_from_missing(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """空输入框 ""(哨兵空断言判据面)与不可达 None 严格区分。"""
        monkeypatch.setattr(axui, "_run", lambda argv: _proc_ok("v:\n"))
        assert axui.read_input_value() == ""
        monkeypatch.setattr(axui, "_run", lambda argv: _proc_ok("v:正文内容\n"))
        assert axui.read_input_value() == "正文内容"
        monkeypatch.setattr(axui, "_run", lambda argv: _proc_ok(""))
        assert axui.read_input_value() is None

    def test_write_input_value_sets_axvalue(self, monkeypatch: pytest.MonkeyPatch) -> None:
        seen: dict = {}

        def fake_run(argv: list[str]) -> subprocess.CompletedProcess[bytes]:
            seen["argv"] = argv
            return _proc_ok()

        monkeypatch.setattr(axui, "_run", fake_run)
        assert axui.write_input_value("正文") is True
        script = seen["argv"][2]
        assert "chat_input_field" in script and "AXValue" in script
        assert seen["argv"][-1] == "正文"

    def test_focus_input_presses_axpress(self, monkeypatch: pytest.MonkeyPatch) -> None:
        seen: dict = {}

        def fake_run(argv: list[str]) -> subprocess.CompletedProcess[bytes]:
            seen["argv"] = argv
            return _proc_ok()

        monkeypatch.setattr(axui, "_run", fake_run)
        assert axui.focus_input() is True
        assert "AXPress" in seen["argv"][2] and "chat_input_field" in seen["argv"][2]

    def test_focused_is_input_three_states(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setattr(axui, "_run", lambda argv: _proc_ok("true\n"))
        assert axui.focused_is_input() is True
        monkeypatch.setattr(axui, "_run", lambda argv: _proc_ok("false\n"))
        assert axui.focused_is_input() is False
        monkeypatch.setattr(axui, "_run", lambda argv: _proc_ok(""))  # 取不到
        assert axui.focused_is_input() is None
        monkeypatch.setattr(axui, "_run", lambda argv: _proc_fail())
        assert axui.focused_is_input() is None

    def test_subprocess_timeout_raises_30(self, monkeypatch: pytest.MonkeyPatch) -> None:
        def hang(argv: list[str]) -> subprocess.CompletedProcess[bytes]:
            raise BridgeError(TIMEOUT, "平台子进程超时(osascript…)", fix_hint="重试")

        monkeypatch.setattr(axui, "_run", hang)
        with pytest.raises(BridgeError) as excinfo:
            axui.read_current_chat_name()
        assert excinfo.value.exit_code == TIMEOUT == 30

    def test_process_loop_covers_both_process_names(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """脚本遍历 {微信, WeChat} 两进程名(zh-CN/en 系统两形态)。"""
        seen: dict = {}

        def fake_run(argv: list[str]) -> subprocess.CompletedProcess[bytes]:
            seen["script"] = argv[2]
            return _proc_ok()

        monkeypatch.setattr(axui, "_run", fake_run)
        axui.read_input_value()
        assert '{"微信", "WeChat"}' in seen["script"]

    def test_element_walks_abandon_entire_contents(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """0.8.1(真机实证 -1719 竞态):元素原语弃 ``entire contents``,
        改 BFS 逐层遍历(队列 + 节点预算)。"""
        seen: dict = {}

        def fake_run(argv: list[str]) -> subprocess.CompletedProcess[bytes]:
            seen["script"] = argv[2]
            return _proc_ok()

        monkeypatch.setattr(axui, "_run", fake_run)
        for probe in (axui.read_input_value, axui.read_current_chat_name,
                      axui.write_input_value, axui.focus_input, axui.press_session_item):
            probe("目标") if probe is axui.press_session_item else (
                probe("x") if probe is axui.write_input_value else probe()
            )
            script = seen["script"]
            assert "entire contents" not in script, probe.__name__
            assert "set theQueue to {window 1}" in script  # BFS 队列起点
            assert "repeat while (count of theQueue) > 0 and budget > 0" in script
            assert f"set budget to {axui.WALK_BUDGET}" in script  # 节点预算上限
            assert "UI elements of elem" in script  # 逐层展开(非一次性拍平)

    def test_write_search_value_uses_focused_element_not_walk(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """write_search_value 保持 AXFocusedUIElement 直写(REF 路线,
        不依赖树遍历)。"""
        seen: dict = {}

        def fake_run(argv: list[str]) -> subprocess.CompletedProcess[bytes]:
            seen["script"] = argv[2]
            return _proc_ok()

        monkeypatch.setattr(axui, "_run", fake_run)
        assert axui.write_search_value("filehelper") is True
        script = seen["script"]
        assert "AXFocusedUIElement" in script and "AXValue" in script
        assert "theQueue" not in script
