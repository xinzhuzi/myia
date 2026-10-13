"""三态探针单测(design §2 判据矩阵逐行;检查器全 mock,零真实系统调用)。"""

from __future__ import annotations

import pytest

from wechat_bridge.config import load_config
from wechat_bridge.probe import run_probe

from bridge_testkit import CheckMocks, green_mocks, tray_mocks


@pytest.fixture(autouse=True)
def _isolate_home(tmp_path, monkeypatch):
    """数据根隔离:load_config() 缺省路径落 tmp,不读宿主真实配置(本机若
    配了桥配置会把断言带偏;单测环境要确定性)。"""
    monkeypatch.setenv("MYIA_HOME", str(tmp_path))


class TestMatrixRows:
    def test_process_not_running_is_bridge_unavailable(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """矩阵行 2:微信进程未运行 → bridge_unavailable。"""
        tray_mocks(monkeypatch, CheckMocks(process=False))
        result = run_probe(bridge_version="t")
        assert result.state == "bridge_unavailable"
        assert result.ok is False
        assert [r.code for r in result.reasons] == ["wechat_not_running"]
        # 短路语义:进程不在就不再评窗口/本地库(checks 如实留短)。
        assert "main_window" not in result.checks

    def test_screen_recording_missing_is_bridge_unavailable(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """矩阵行 3(2026-10-12 勘误):屏幕录制缺失 → bridge_unavailable(像素链前置)。"""
        tray_mocks(monkeypatch, CheckMocks(screen_granted=False))
        result = run_probe(bridge_version="t")
        assert result.state == "bridge_unavailable"
        assert [r.code for r in result.reasons] == ["screen_recording_denied"]
        assert result.checks["screen_recording"] == "fail"

    def test_screen_recording_unknown_is_not_unavailable(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """权限判定不可及(None)= unknown 如实,不据此判死(托盘降级照走)。"""
        tray_mocks(monkeypatch, CheckMocks(screen_granted=None))
        result = run_probe(bridge_version="t")
        assert result.state == "degraded"
        assert result.checks["screen_recording"] == "unknown"

    def test_ax_denied_no_longer_drives_state(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """2026-10-12 勘误回归:AX 缺失(A1 死路后不再前置)不驱动态,仅保留报告。"""
        tray_mocks(monkeypatch, CheckMocks(ax_trusted=False, screen_granted=True))
        result = run_probe(bridge_version="t")
        assert result.state != "bridge_unavailable"
        assert result.checks["ax_permission"] == "fail"
        assert all(r.code != "ax_permission_denied" for r in result.reasons)

    def test_tray_state_is_degraded_window_closed(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """矩阵行 4(2026-10-11 实况形状):托盘态 → degraded(window_closed)。"""
        tray_mocks(monkeypatch)
        result = run_probe(bridge_version="t")
        assert result.state == "degraded"
        codes = [r.code for r in result.reasons]
        assert "window_closed" in codes
        assert result.checks["main_window"] == "fail"
        assert result.checks["wechat_process"] == "ok"
        assert result.wechat_version == "4.1.15"

    def test_key_unavailable_adds_degraded_reason(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """矩阵行 6:本地库密钥不可得 → degraded(key_unavailable;D4 语义)。"""
        tray_mocks(monkeypatch, CheckMocks(window=True))  # 窗口开,只剩密钥缺
        result = run_probe(bridge_version="t")
        assert result.state == "degraded"
        assert [r.code for r in result.reasons] == ["key_unavailable"]
        assert result.checks["localdb_key"] == "unavailable"

    def test_db_storage_missing_is_degraded_db_not_found(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """矩阵行 6 近亲:本地库定位失败 → degraded(db_not_found);密钥缺
        依据实并报(两项独立事实,理由清单不互相吞并)。"""
        tray_mocks(monkeypatch, CheckMocks(window=True, accounts=None))
        result = run_probe(bridge_version="t")
        assert result.state == "degraded"
        codes = [r.code for r in result.reasons]
        assert "db_not_found" in codes and "key_unavailable" in codes
        assert result.checks["localdb_storage"] == "fail"

    def test_all_green_is_ok(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """矩阵行 7:全部通过 → ok(窗口开 + 密钥可得)。"""
        green_mocks(monkeypatch)
        result = run_probe(bridge_version="t")
        assert result.state == "ok"
        assert result.ok is True
        assert result.reasons == []
        assert result.checks["main_window"] == "ok"
        assert result.checks["localdb_key"] == "ok"

    def test_ax_tree_unknown_in_skeleton(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """矩阵行 5(AX 树空/残缺)属 Phase C 判据;骨架态如实 unknown。"""
        tray_mocks(monkeypatch)
        result = run_probe(bridge_version="t")
        assert result.checks["ax_tree"] == "unknown"


class TestContractShape:
    def test_payload_carries_config_and_versions(self, monkeypatch: pytest.MonkeyPatch, tmp_path) -> None:
        """§6 契约四键(ok/state/checks/wechat_version)在场 + 诊断附加键。"""
        tray_mocks(monkeypatch)
        config = load_config()
        result = run_probe(config=config, bridge_version="0.1.0")
        payload = result.to_payload()
        for key in ("ok", "state", "checks", "wechat_version"):
            assert key in payload
        assert payload["bridge_version"] == "0.1.0"
        assert payload["config"]["domains"] == config.domains

    def test_reasons_carry_fix_hints(self, monkeypatch: pytest.MonkeyPatch) -> None:
        tray_mocks(monkeypatch)
        result = run_probe(bridge_version="t")
        assert result.reasons, "托盘态必有降级原因"
        for reason in result.reasons:
            assert reason.fix_hint



# ---------------------------------------------------------------------------
# doctor(task 10-14-wechat-send-text design §E-2;--probe 超集 + AX 门态)
# ---------------------------------------------------------------------------

import wechat_bridge.system_checks as sc  # noqa: E402
from wechat_bridge.probe import run_doctor  # noqa: E402


class TestRunDoctor:
    def test_doctor_reuses_probe_payload_and_ax_gate_open(self, monkeypatch: pytest.MonkeyPatch) -> None:
        tray_mocks(monkeypatch)
        monkeypatch.setattr(sc, "wechat_ax_node_count", lambda: 122)
        import wechat_bridge.axui as axui

        monkeypatch.setattr(axui, "read_input_value", lambda: "")
        payload = run_doctor(bridge_version="t")
        doctor = payload["doctor"]
        assert doctor["probe"]["state"] == "degraded"  # 复用 run_probe 全量
        assert doctor["probe"]["bridge_version"] == "t"
        assert doctor["ax_gate"] == {
            "nodes": 122, "state": "open", "input_field": "ok",
            "note": None, "fix_hint": None,
        }

    def test_doctor_closed_and_unknown_states(self, monkeypatch: pytest.MonkeyPatch) -> None:
        tray_mocks(monkeypatch)
        import wechat_bridge.axui as axui

        monkeypatch.setattr(axui, "read_input_value", lambda: None)
        monkeypatch.setattr(sc, "wechat_ax_node_count", lambda: 5)  # ≤5 = closed
        gate = run_doctor()["doctor"]["ax_gate"]
        assert gate["state"] == "closed" and gate["input_field"] == "missing"
        assert "LLDB" in gate["fix_hint"]
        monkeypatch.setattr(sc, "wechat_ax_node_count", lambda: None)
        gate2 = run_doctor()["doctor"]["ax_gate"]
        assert gate2["state"] == "unknown" and gate2["nodes"] is None

    def test_doctor_cgevent_channel_note(self, monkeypatch: pytest.MonkeyPatch) -> None:
        tray_mocks(monkeypatch)
        monkeypatch.setattr(sc, "wechat_ax_node_count", lambda: 122)
        monkeypatch.setattr(sc, "ax_permission_trusted", lambda: False)
        import wechat_bridge.axui as axui

        monkeypatch.setattr(axui, "read_input_value", lambda: "")
        channel = run_doctor()["doctor"]["cgevent_channel"]
        assert channel["post_key"] == "unverified"
        assert channel["host_ax_trusted"] is False  # 宿主授权实锤信号(0.8.1)
        assert "不合成事件" in channel["note"]
        assert "keystroke" in channel["note"]


class TestAxNodeCount:
    """wechat_ax_node_count:全部窗口最大 UI elements 数(不绑 window 1,
    design §J-22——多窗时 z-order 首窗未必主窗)。"""

    def test_script_deep_walks_all_windows_and_takes_max(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """0.8.1(真机实证直查第一层恒 ~4):计数 = 全窗子树 BFS 深度枚举
        取最大,不绑 window 1。"""
        seen: dict = {}

        def fake_run(argv: list) -> object:
            seen["script"] = argv[2]
            import subprocess

            return subprocess.CompletedProcess(
                args=[], returncode=0, stdout=b"122\n", stderr=b""
            )

        monkeypatch.setattr(sc, "_run_command", fake_run)
        assert sc.wechat_ax_node_count() == 122
        script = seen["script"]
        assert "repeat with w in windows" in script  # 遍历全部窗口
        assert "maxCount" in script  # 取最大,不绑 window 1
        assert "window 1" not in script
        assert "theQueue" in script and "budget" in script  # BFS 队列 + 预算
        assert "UI elements of elem" in script  # 逐层展开(非直查 count)

    def test_failures_return_none(self, monkeypatch: pytest.MonkeyPatch) -> None:
        import subprocess

        monkeypatch.setattr(
            sc, "_run_command",
            lambda argv: subprocess.CompletedProcess(args=[], returncode=1, stdout=b"", stderr=b"x"),
        )
        assert sc.wechat_ax_node_count() is None
        monkeypatch.setattr(
            sc, "_run_command",
            lambda argv: subprocess.CompletedProcess(args=[], returncode=0, stdout=b"not-a-number\n", stderr=b""),
        )
        assert sc.wechat_ax_node_count() is None
