"""AX 层前置检查门单测(§6 码序 10 → 11 → 12;全 mock,零真实系统调用)。"""

from __future__ import annotations

import pytest

import wechat_bridge.system_checks as sc
from wechat_bridge.ax import ensure_ui_preconditions, not_implemented
from wechat_bridge.codes import (
    AX_PERMISSION_DENIED,
    SCREEN_RECORDING_DENIED,
    WECHAT_NOT_RUNNING,
    WINDOW_CLOSED,
    BridgeError,
)


def _gate(monkeypatch: pytest.MonkeyPatch, *, process=True, ax=True, window=False, screen=True) -> None:
    monkeypatch.setattr(sc, "wechat_process_running", lambda: process)
    monkeypatch.setattr(sc, "ax_permission_trusted", lambda: ax)
    monkeypatch.setattr(sc, "wechat_main_window_open", lambda: window)
    monkeypatch.setattr(sc, "screen_recording_granted", lambda: screen)


class TestPreconditionGate:
    def test_process_not_running_exits_10_first(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """码序:进程不在 → 10(不再评权限/窗口)。"""
        _gate(monkeypatch, process=False, ax=False, window=False)
        with pytest.raises(BridgeError) as excinfo:
            ensure_ui_preconditions()
        assert excinfo.value.exit_code == WECHAT_NOT_RUNNING == 10

    def test_screen_denied_exits_11(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """2026-10-13 勘误:像素链前置门真实权限=屏幕录制(非 AX);缺失 → 码 16(独立码)。"""
        _gate(monkeypatch, process=True, window=False, screen=False)
        with pytest.raises(BridgeError) as excinfo:
            ensure_ui_preconditions()
        assert excinfo.value.exit_code == SCREEN_RECORDING_DENIED == 16

    def test_ax_denied_no_longer_blocks_gate(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """2026-10-13 勘误回归:AX 缺失不再拦门(码 11 归屏幕录制;run 108 实锤收口)。"""
        _gate(monkeypatch, process=True, ax=False, window=True, screen=True)
        assert ensure_ui_preconditions() is None

    def test_window_closed_exits_12(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """托盘态:窗口未开 → 12(UI 通道专属;localdb 不受影响)。"""
        _gate(monkeypatch, process=True, ax=True, window=False)
        with pytest.raises(BridgeError) as excinfo:
            ensure_ui_preconditions()
        assert excinfo.value.exit_code == WINDOW_CLOSED == 12
        assert "localdb" in excinfo.value.fix_hint

    def test_window_unknown_does_not_block(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """窗口态判定不可及(None)不拦——探测不到 ≠ 没开,不误杀可用态。"""
        _gate(monkeypatch, process=True, ax=True)
        monkeypatch.setattr(sc, "wechat_main_window_open", lambda: None)
        assert ensure_ui_preconditions() is None  # 过窗门放行(门只挡 10/11/12)

    def test_all_green_gate_passes_and_send_delegates(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """前置全绿 = 门放行(None);send_text 委托 sendui 真身(此处桩验证
        委托面——0.8.0 三源合体新签名 target/dry_run/on_armed 全参透传;
        全链本体见 test_send_ui.py)。"""
        _gate(monkeypatch, process=True, ax=True, window=True)
        assert ensure_ui_preconditions() is None
        from wechat_bridge.ax import send_text
        from wechat_bridge.config import BridgeConfig
        from wechat_bridge.sendtarget import SendTarget

        target = SendTarget(
            username="filehelper", alias=None, display_name="文件传输助手",
            search_term="filehelper",
        )
        seen: dict = {}

        def stub(config, tgt, body, *, dry_run=False, on_armed=None,
                 on_receipt_green=None, receipt_query=None):
            seen.update(target=tgt, dry_run=dry_run)
            return {"send": {"sent": True}}

        monkeypatch.setattr("wechat_bridge.sendui.send_text", stub)
        payload = send_text(BridgeConfig(), target, "正文")
        assert payload["send"]["sent"] is True
        assert seen["target"] is target  # 委托面:target 原样透传
        assert seen["dry_run"] is False


class TestNotImplementedDiscipline:
    def test_not_implemented_never_fakes_a_named_family(self) -> None:
        """过渡码纪律:「没实现」绝不谎报 §6 具名族(码表封闭,过渡码显式)。"""
        err = not_implemented("sessions list", "Phase C1")
        assert err.exit_code == 1
        assert err.name == "not_implemented"
        assert err.name not in codes_named()
        assert "Phase C1" in err.message


def codes_named() -> set[str]:
    import wechat_bridge.codes as codes_mod

    return set(codes_mod.CODE_NAMES.values())
