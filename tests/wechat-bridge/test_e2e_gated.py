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


def _run_localdb_query(chat: str = "filehelper") -> tuple[int, dict]:
    result = subprocess.run(
        [sys.executable, "-m", "wechat_bridge", "localdb", "query", chat, "--since", "7d", "--json"],
        capture_output=True,
        text=True,
        timeout=600,
        cwd=COMPONENT_SRC,
        env={**os.environ},
    )
    return result.returncode, json.loads(result.stdout)


class TestRealLocaldbNegative:
    """真机 E1 负结论回归(2026-10-11 E1 实测:零内存途径不可推导)。

    门控语义:真跑 E1 全链(读真 key_info.db + 真 db_storage page1 离线
    HMAC 校验,数十秒级)——**零微信进程交互、零出网、零密钥材料落盘**;
    期望 exit 21 + key_unavailable + D4 指引。若某天真命中(D4 已闭合/微信
    改了密钥落盘),此测试如实失败,提醒刷新本档结论。
    """

    def test_query_reports_honest_key_unavailable(self) -> None:
        exit_code, payload = _run_localdb_query()
        if exit_code == 0:
            pytest.fail("E1 零内存途径真机命中了密钥——刷新 research/localdb-e2e.md 与本测试")
        err = payload["error"]
        assert exit_code in (20, 21), f"非预期错误族: {err}"
        if exit_code == 21:
            assert err["code"] == "key_unavailable"
            assert "D4" in (err.get("fix_hint") or "")
