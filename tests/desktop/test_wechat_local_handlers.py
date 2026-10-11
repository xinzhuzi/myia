"""Tests for 10-11-wechat-ui-bridge Phase F2 — 微信本机桥 sidecar 协议面。

覆盖:四动作(probe/sessions/messages/query)的参数校验、桥应答透传、
桥具名错误族原样上抛(码名 + fix_hint/retry_after_seconds 走 data)、
组件缺席/超时/非契约应答三兜底、封闭动作词表。桥子进程全 mock
(monkeypatch 模块注入点),零真跑;真桥本体由 tests/wechat-bridge 专测。
"""

from __future__ import annotations

import json
from typing import Any

import pytest

from myssia import wechat_local_sidecar as wls
from myssia.push.weixin_local import LocalBridgeTimeoutError

PROBE_OK = {
    "ok": True,
    "state": "ok",
    "checks": {"bridge_component": "ok", "wechat_process": "ok"},
    "wechat_version": "4.1.15",
    "bridge_version": "0.2.0",
    "reasons": [],
}

SESSIONS_PAYLOAD = {
    "sessions": [
        {"id": "filehelper", "name": "文件传输助手", "unread": 0},
        {"id": "123@chatroom", "name": "测试群", "unread": 3},
    ]
}

QUERY_PAYLOAD = {
    "chat_id": "filehelper",
    "since_days": 7,
    "messages": [{"ts": 1760000000, "sender": "me", "type": "text", "text": "…"}],
    "display_name": "文件传输助手",
    "sessions": [],
    "domains": {"message": "ok", "session": "ok", "contact": "ok"},
    "copy": {"dir": "/tmp/copies"},
}


@pytest.fixture()
def fake_bridge(tmp_path, monkeypatch):
    """fake bridge:真可执行占位文件(过 bin 存在性门)+ 换 _BASE + 捕获
    argv;应答按注册表逐命令给出。"""
    calls: list[dict[str, Any]] = []
    responses: dict[str, tuple[int, str]] = {}
    bridge_bin = tmp_path / "fake-wechat-bridge"
    bridge_bin.write_text("#!/bin/sh\nexit 0\n", encoding="utf-8")
    bridge_bin.chmod(0o755)

    def fake_run(argv, input_text, timeout):
        calls.append({"argv": list(argv), "timeout": timeout})
        key = "probe" if len(argv) < 3 else " ".join(argv[1:3])
        if argv[1:2] == ["--probe"]:
            key = "probe"
        exit_code, stdout = responses.get(key, (0, json.dumps(SESSIONS_PAYLOAD)))
        return exit_code, stdout, ""

    monkeypatch.setattr(wls, "_BASE", str(bridge_bin))
    monkeypatch.setattr(wls, "run_bridge_command_sync", fake_run)
    return calls, responses


@pytest.fixture()
def fake_probe(monkeypatch):
    """探针注入:probe_local_bridge 换可编程假件。"""
    holder: dict[str, Any] = {"payload": dict(PROBE_OK)}

    def fake_probe(bridge_bin, *, timeout):
        return holder["payload"]

    monkeypatch.setattr(wls, "probe_local_bridge", fake_probe)
    return holder


# ---------------------------------------------------------------------------
# probe
# ---------------------------------------------------------------------------


class TestProbe:
    def test_probe_passthrough_payload(self, fake_probe):
        payload = wls.handle_wechat_local("probe", {})
        assert payload == PROBE_OK

    def test_probe_extra_params_tolerated(self, fake_probe):
        """地基路纯加法纪律:多余键宽容,不拒。"""
        assert wls.handle_wechat_local("probe", {"future_key": 1}) == PROBE_OK

    def test_probe_none_params(self, fake_probe):
        assert wls.handle_wechat_local("probe", None) == PROBE_OK

    def test_probe_never_raises_on_degraded(self, fake_probe):
        """健康面自健康:合成载荷透传,不抛。"""
        fake_probe["payload"] = {
            "ok": False,
            "state": "bridge_unavailable",
            "checks": {"bridge_component": "missing"},
            "wechat_version": None,
            "bridge_version": None,
            "reasons": [{"code": "component_missing", "fix_hint": "装组件"}],
        }
        payload = wls.handle_wechat_local("probe", {})
        assert payload["state"] == "bridge_unavailable"
        assert payload["reasons"][0]["code"] == "component_missing"


# ---------------------------------------------------------------------------
# sessions / messages / query:argv 形状 + 透传
# ---------------------------------------------------------------------------


class TestReadCommands:
    def test_sessions_default_argv(self, fake_bridge):
        calls, responses = fake_bridge
        responses["sessions list"] = (0, json.dumps(SESSIONS_PAYLOAD))

        payload = wls.handle_wechat_local("sessions", {})

        assert payload == SESSIONS_PAYLOAD
        assert calls[0]["argv"][1:] == ["sessions", "list", "--json"]

    def test_sessions_limit_forwarded(self, fake_bridge):
        calls, responses = fake_bridge
        responses["sessions list"] = (0, json.dumps(SESSIONS_PAYLOAD))

        wls.handle_wechat_local("sessions", {"limit": 5})

        assert calls[0]["argv"][1:] == ["sessions", "list", "--json", "-n", "5"]

    def test_messages_argv_with_count(self, fake_bridge, monkeypatch):
        calls, _ = fake_bridge
        messages = {"messages": [{"ts": 1, "type": "text", "text": "…"}]}

        def fake_run(argv, input_text, timeout):
            calls.append({"argv": list(argv), "timeout": timeout})
            return 0, json.dumps(messages), ""

        monkeypatch.setattr(wls, "run_bridge_command_sync", fake_run)

        payload = wls.handle_wechat_local(
            "messages", {"chat_id": "filehelper", "count": 10}
        )

        assert payload == messages
        assert calls[-1]["argv"][1:] == ["messages", "read", "filehelper", "--json", "-k", "10"]

    def test_query_default_since_30d(self, fake_bridge):
        calls, responses = fake_bridge
        responses["localdb query"] = (0, json.dumps(QUERY_PAYLOAD))

        payload = wls.handle_wechat_local("query", {"chat_id": "filehelper"})

        assert payload == QUERY_PAYLOAD
        assert calls[0]["argv"][1:] == ["localdb", "query", "filehelper", "--since", "30d", "--json"]

    def test_query_since_days_forwarded(self, fake_bridge):
        calls, responses = fake_bridge
        responses["localdb query"] = (0, json.dumps(QUERY_PAYLOAD))

        wls.handle_wechat_local("query", {"chat_id": "x@chatroom", "since_days": 7})

        assert "--since" in calls[0]["argv"]
        assert calls[0]["argv"][calls[0]["argv"].index("--since") + 1] == "7d"

    def test_command_timeout_bound(self, fake_bridge):
        """读命令超时 = 发送同款 60s 模块常量。"""
        calls, responses = fake_bridge
        responses["sessions list"] = (0, json.dumps(SESSIONS_PAYLOAD))
        wls.handle_wechat_local("sessions", {})
        assert calls[0]["timeout"] == wls._COMMAND_TIMEOUT_SECONDS

    def test_query_timeout_bound_covers_first_copy_build(self, fake_bridge):
        """query 超时独立于 60s 命令族:桥侧 sqlcipher 单库解密上界 300s,
        多域副本首建累计可超 60s → 600s(2×单库上界)盖住,首查不被误杀。"""
        calls, responses = fake_bridge
        responses["localdb query"] = (0, json.dumps(QUERY_PAYLOAD))
        wls.handle_wechat_local("query", {"chat_id": "filehelper"})
        assert calls[0]["timeout"] == wls._QUERY_TIMEOUT_SECONDS == 600.0
        assert wls._QUERY_TIMEOUT_SECONDS > wls._COMMAND_TIMEOUT_SECONDS


# ---------------------------------------------------------------------------
# 参数校验
# ---------------------------------------------------------------------------


class TestParamValidation:
    @pytest.mark.parametrize(
        "action,params",
        [
            ("messages", {}),
            ("messages", {"chat_id": ""}),
            ("messages", {"chat_id": "   "}),
            ("messages", {"chat_id": 123}),
            ("query", {}),
            ("query", {"chat_id": "x", "since_days": 0}),
            ("query", {"chat_id": "x", "since_days": 4000}),
            ("query", {"chat_id": "x", "since_days": "7"}),
            ("sessions", {"limit": 0}),
            ("sessions", {"limit": 101}),
            ("sessions", {"limit": True}),
        ],
    )
    def test_invalid_params_structured(self, fake_bridge, action, params):
        with pytest.raises(wls.WechatLocalSidecarError) as excinfo:
            wls.handle_wechat_local(action, params)
        assert excinfo.value.code == "invalid_params"
        assert excinfo.value.path.startswith("params.")

    def test_messages_count_over_max_rejected(self, fake_bridge):
        with pytest.raises(wls.WechatLocalSidecarError) as excinfo:
            wls.handle_wechat_local("messages", {"chat_id": "x", "count": 201})
        assert excinfo.value.code == "invalid_params"

    def test_params_not_object(self, fake_bridge):
        with pytest.raises(wls.WechatLocalSidecarError) as excinfo:
            wls.handle_wechat_local("sessions", ["not", "a", "dict"])  # type: ignore[arg-type]
        assert excinfo.value.code == "invalid_params"

    def test_unknown_action_closed_vocabulary(self, fake_bridge):
        with pytest.raises(wls.WechatLocalSidecarError) as excinfo:
            wls.handle_wechat_local("send_text", {})
        assert excinfo.value.code == "invalid_params"
        assert "query" in str(excinfo.value)  # 合法词表在文案里


# ---------------------------------------------------------------------------
# 桥错误归一
# ---------------------------------------------------------------------------


class TestBridgeErrorMapping:
    def test_bridge_named_error_passthrough_with_fix_hint(self, fake_bridge):
        """桥具名错误族原样上抛:码名 = code,message = 人话,指引进 data。"""
        calls, responses = fake_bridge
        responses["sessions list"] = (
            13,
            json.dumps(
                {
                    "error": {
                        "code": "ax_tree_empty",
                        "message": "AX 树空/残缺",
                        "fix_hint": "像素链兜底或降级",
                    }
                },
                ensure_ascii=False,
            ),
        )

        with pytest.raises(wls.WechatLocalSidecarError) as excinfo:
            wls.handle_wechat_local("sessions", {})
        assert excinfo.value.code == "ax_tree_empty"
        assert "AX 树空" in excinfo.value.message
        assert excinfo.value.data == {"fix_hint": "像素链兜底或降级"}

    def test_rate_limited_carries_retry_seconds_in_data(self, fake_bridge):
        calls, responses = fake_bridge
        responses["localdb query"] = (
            14,
            json.dumps(
                {
                    "error": {
                        "code": "send_rate_limited",
                        "message": "距上次发送不足 10 秒",
                        "retry_after_seconds": 6.5,
                    }
                }
            ),
        )

        with pytest.raises(wls.WechatLocalSidecarError) as excinfo:
            wls.handle_wechat_local("query", {"chat_id": "x"})
        assert excinfo.value.code == "send_rate_limited"
        assert excinfo.value.data == {"retry_after_seconds": 6.5}

    def test_not_implemented_passthrough(self, fake_bridge):
        """Phase C 骨架过渡码如实透传(不谎报为任何具名族——桥内纪律)。"""
        calls, responses = fake_bridge
        responses["messages read"] = (
            1,
            json.dumps(
                {
                    "error": {
                        "code": "not_implemented",
                        "message": "messages read 的实现层尚未落地(Phase C2)",
                    }
                },
                ensure_ascii=False,
            ),
        )

        with pytest.raises(wls.WechatLocalSidecarError) as excinfo:
            wls.handle_wechat_local("messages", {"chat_id": "x"})
        assert excinfo.value.code == "not_implemented"

    def test_timeout_maps_bridge_timeout(self, fake_bridge, monkeypatch):
        calls, _responses = fake_bridge

        def fake_run(argv, input_text, timeout):
            raise LocalBridgeTimeoutError("wechat-bridge 超过 60s 未退出,子进程已终止")

        monkeypatch.setattr(wls, "run_bridge_command_sync", fake_run)

        with pytest.raises(wls.WechatLocalSidecarError) as excinfo:
            wls.handle_wechat_local("sessions", {})
        assert excinfo.value.code == "bridge_timeout"

    def test_unparseable_stdout_maps_bridge_error(self, fake_bridge, monkeypatch):
        monkeypatch.setattr(
            wls, "run_bridge_command_sync", lambda *a, **k: (1, "not-json", "")
        )

        with pytest.raises(wls.WechatLocalSidecarError) as excinfo:
            wls.handle_wechat_local("sessions", {})
        assert excinfo.value.code == "bridge_error"

    def test_exit_0_with_error_payload_maps_error(self, fake_bridge, monkeypatch):
        """防御:exit 0 却带 error 载荷 → 仍按错误族映射。"""
        monkeypatch.setattr(
            wls,
            "run_bridge_command_sync",
            lambda *a, **k: (
                0,
                json.dumps({"error": {"code": "wechat_not_running", "message": "微信不在"}}),
                "",
            ),
        )

        with pytest.raises(wls.WechatLocalSidecarError) as excinfo:
            wls.handle_wechat_local("sessions", {})
        assert excinfo.value.code == "wechat_not_running"

    def test_error_message_never_enters_log_by_default(self, fake_bridge, caplog):
        """红线 6:聊天内容只在应答载荷;本层默认零日志输出。"""
        calls, responses = fake_bridge
        responses["sessions list"] = (0, json.dumps(SESSIONS_PAYLOAD))

        with caplog.at_level("DEBUG"):
            wls.handle_wechat_local("sessions", {})
        assert caplog.records == []
