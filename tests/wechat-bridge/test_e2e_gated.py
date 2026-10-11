"""真机探针测试(design §8 环境门控:``MYIA_WECHAT_E2E=1`` 才跑,CI 缺省
跳过——严禁把真客户端测试裸放进 pytest 全量)。

门控语义:只跑 ``--probe``(零成本只读:进程表/Info.plist/AXIsProcessTrusted/
CGWindowList 快照/目录计数)——**不读消息内容、不碰窗口前台、不触发任何
AX 写动作**(prd 红线 2/4)。断言按「如实三态」宽形状:机器上微信处于何种
实况(没装/托盘/开窗)都只要求载荷自洽,不预设结论。

形状基线:fixtures/probe_tray_state_20261011.json = 2026-10-11 本机托盘态
实跑录制(fixture 录制惯例,脱敏纪律红线 6——仅版本号与检查态,零内容)。
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

COMPONENT_SRC = Path(__file__).resolve().parents[2] / "plugins" / "wechat-bridge"
RECORDED_TRAY_PROBE = Path(__file__).resolve().parent / "fixtures" / "probe_tray_state_20261011.json"

pytestmark = pytest.mark.skipif(
    os.environ.get("MYIA_WECHAT_E2E") != "1",
    reason="真机探针默认跳过(design §8:MYIA_WECHAT_E2E=1 才跑,CI 无微信)",
)

VALID_STATES = {"ok", "degraded", "bridge_unavailable"}


def _run_probe() -> dict:
    result = subprocess.run(
        [sys.executable, "-m", "wechat_bridge", "--probe"],
        capture_output=True,
        text=True,
        timeout=60,
        cwd=COMPONENT_SRC,
        env={**os.environ},  # 环境原样继承(MYIA_HOME 尊重调用方)
    )
    assert result.returncode == 0, f"probe 非零退出 {result.returncode}: {result.stderr[:300]}"
    return json.loads(result.stdout)


class TestRealProbe:
    def test_probe_payload_is_wellformed_three_state(self) -> None:
        """真机实跑:载荷四键在场、state ∈ 三态、ok 与 state 自洽。"""
        payload = _run_probe()
        for key in ("ok", "state", "checks", "wechat_version"):
            assert key in payload
        assert payload["state"] in VALID_STATES
        assert payload["ok"] is (payload["state"] == "ok")
        assert isinstance(payload["checks"], dict) and payload["checks"]
        for reason in payload.get("reasons", []):
            assert {"code", "fix_hint"} <= set(reason)

    def test_probe_shape_matches_recorded_tray_baseline(self) -> None:
        """与托盘态录制基线同形(键集一致;值随实况,不比内容)。"""
        recorded = json.loads(RECORDED_TRAY_PROBE.read_text(encoding="utf-8"))
        payload = _run_probe()
        assert set(payload) == set(recorded), "probe 载荷键集漂移:先刷新录制基线再改契约"
        assert set(payload["checks"]) == set(recorded["checks"])

    def test_probe_consistency_with_process_reality(self) -> None:
        """状态与进程实况自洽:进程不在必须 bridge_unavailable(不静默装死)。"""
        import wechat_bridge.system_checks as sc

        payload = _run_probe()
        if not sc.wechat_process_running():
            assert payload["state"] == "bridge_unavailable"
            assert payload["reasons"][0]["code"] == "wechat_not_running"
