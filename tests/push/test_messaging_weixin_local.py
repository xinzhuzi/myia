"""Tests for 10-11-wechat-ui-bridge Phase F1 — 微信本机通道(weixin-local)。

覆盖:发送四态(mock runner:成功 / 桥组件缺失 / 频控拒发 / UI 通道降级)、
design §6 错误映射表全行(每行断言 ``classify_dead_error`` 为 None——零死信:
桥错误族全环境态)、超时 kill、exit 2 用法漂移、寻址(legacy target 引用,
无目录寻址)、``probe_local_bridge`` 三形态(fake bridge 回显预录 JSON)、
schema 门(weixin_local_enabled 缺省拒 + 字段宿主 + pipeline kwargs 下传)。

蓝本对照::mod:`myssia.push.weixin`(官方 Hermes 桥,出站主口)——此处测
MYIA 侧重写;桥本体(plugins/wechat-bridge)由 tests/wechat-bridge 专测。
真实子进程冒烟仅两条(fake bridge 回显 / sleep 超时 kill),对齐蓝本克制口径。
"""

from __future__ import annotations

import asyncio
import json
import os
import stat
from dataclasses import replace
from typing import Any

import pytest

from myssia.pipeline import _W2_CHANNEL_FIELD_KWARGS, _build_push_channel
from myssia.push import SendContext, WeixinLocalChannel
from myssia.push.base import PushSendError
from myssia.push.delivery import classify_dead_error, is_config_send_error
from myssia.push.directory import DirectoryDiscoverUnsupported
from myssia.wechat.push_local import (
    DEFAULT_BRIDGE_BIN,
    DEFAULT_BRIDGE_TIMEOUT_SECONDS,
    DEFAULT_PROBE_TIMEOUT_SECONDS,
    LocalBridgeTimeoutError,
    probe_local_bridge,
    run_bridge_command_sync,
)
from myssia.schema import (
    CHANNEL_PLATFORMS,
    PUSH_CHANNELS,
    LoadError,
    load_category_file,
)

CONTEXT = SendContext(slot="am", date="2026-10-11", category="羊毛", kind="digest")

CHAT = "filehelper"

ITEMS = [{"title": "羊毛", "url": "https://x/1"}, {"title": "另一条"}]

#: 预录桥应答(fake bridge 回显用;形状对照 wechat_bridge/codes.py 契约)。
BRIDGE_SUCCESS_STDOUT = '{"ok": true}\n'
BRIDGE_RATE_LIMITED_STDOUT = json.dumps(
    {
        "error": {
            "code": "send_rate_limited",
            "message": "距上次发送不足 10 秒(桥内硬编码频控)",
            "fix_hint": "稍候重试",
            "retry_after_seconds": 6.5,
        }
    },
    ensure_ascii=False,
) + "\n"


def _run(coro: Any) -> Any:
    return asyncio.run(coro)


def _mock_runner(result: tuple[int, str, str], calls: list[dict] | None = None):
    """固定应答的 runner:记录 (argv, input, timeout) 供断言。"""

    async def run(argv, input_text, timeout):
        if calls is not None:
            calls.append({"argv": list(argv), "input": input_text, "timeout": timeout})
        return result

    return run


def _raising_runner(exc: BaseException, calls: list[dict] | None = None):
    async def run(argv, input_text, timeout):
        if calls is not None:
            calls.append({"argv": list(argv), "input": input_text, "timeout": timeout})
        raise exc

    return run


def _channel(**kwargs: Any) -> WeixinLocalChannel:
    kwargs.setdefault("target", "env:MYIA_TEST_WEIXIN_LOCAL_CHAT")
    return WeixinLocalChannel(**kwargs)


def _write_executable(path, body: str) -> None:
    path.write_text(body, encoding="utf-8")
    path.chmod(path.stat().st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)


@pytest.fixture()
def chat_env(monkeypatch):
    monkeypatch.setenv("MYIA_TEST_WEIXIN_LOCAL_CHAT", CHAT)


# ---------------------------------------------------------------------------
# 发送四态:成功 / 组件缺失 / 频控拒发 / UI 通道降级
# ---------------------------------------------------------------------------


class TestBridgeFourStates:
    def test_success_invokes_bridge_send_text_with_stdin_body(self, chat_env):
        """exit 0 → 放行;argv 形状(send_text <chat> --file -)+ 正文走 stdin。"""
        calls: list[dict] = []
        channel = _channel(
            bridge_bin="/bin/sh",
            timeout=7.5,
            runner=_mock_runner((0, BRIDGE_SUCCESS_STDOUT, ""), calls),
        )

        _run(channel.send(ITEMS, CONTEXT))

        assert calls[0]["argv"] == ["/bin/sh", "send_text", CHAT, "--file", "-"]
        assert calls[0]["timeout"] == 7.5
        # 正文经 stdin:内置版式 = card_title 行 + 每条「▸ 标题 · URL」行
        assert "羊毛" in calls[0]["input"] and "https://x/1" in calls[0]["input"]

    def test_bridge_bin_missing_is_structured_unavailable(self, chat_env):
        """bin 不存在:发送期预检 → ``bridge_unavailable`` 带修复指引,
        不触 runner(显式可选:无桥环境的如实结构化错误)。"""
        calls: list[dict] = []
        channel = _channel(
            bridge_bin="/nonexistent/wechat-bridge", runner=_mock_runner((0, "{}", ""), calls)
        )

        with pytest.raises(PushSendError) as excinfo:
            _run(channel.send(ITEMS, CONTEXT))
        assert excinfo.value.code == "bridge_unavailable"
        assert "wechat_bridge_bin" in str(excinfo.value)
        assert calls == []  # 预检先于子进程,零调用
        assert classify_dead_error(excinfo.value) is None

    def test_rate_limited_maps_transient_with_retry_seconds(self, chat_env):
        """exit 14(G6 频控拒发)→ ``send_rate_limited`` + 剩余秒数入文案;
        频控是桥内硬门,MYIA 侧零复制。"""
        channel = _channel(
            bridge_bin="/bin/sh",
            runner=_mock_runner((14, BRIDGE_RATE_LIMITED_STDOUT, "")),
        )

        with pytest.raises(PushSendError) as excinfo:
            _run(channel.send(ITEMS, CONTEXT))
        assert excinfo.value.code == "send_rate_limited"
        assert "6.5" in str(excinfo.value)
        assert "G6" in str(excinfo.value)
        assert classify_dead_error(excinfo.value) is None

    def test_window_closed_maps_degraded(self, chat_env):
        """exit 12(主窗口未开,UI 通道降级态)→ ``bridge_degraded`` 带桥内
        修复指引;localdb 只读不受窗口态影响是桥内语义,MYIA 不复述。"""
        channel = _channel(
            bridge_bin="/bin/sh",
            runner=_mock_runner(
                (
                    12,
                    json.dumps(
                        {
                            "error": {
                                "code": "window_closed",
                                "message": "微信主窗口未开(托盘态)",
                                "fix_hint": "打开微信主窗口",
                            }
                        },
                        ensure_ascii=False,
                    ),
                    "",
                )
            ),
        )

        with pytest.raises(PushSendError) as excinfo:
            _run(channel.send(ITEMS, CONTEXT))
        assert excinfo.value.code == "bridge_degraded"
        assert "打开微信主窗口" in str(excinfo.value)
        assert classify_dead_error(excinfo.value) is None


# ---------------------------------------------------------------------------
# design §6 错误映射表全行(零死信 + 配置类码短路断言)
# ---------------------------------------------------------------------------


class TestErrorMappingTable:
    """上表每一行:期望 code + ``classify_dead_error`` 必得 None。"""

    ROWS = [
        ("wechat_not_running", 10, '{"error": {"code": "wechat_not_running", "message": "微信进程不在运行"}}', "bridge_unavailable"),
        ("ax_permission_denied", 11, '{"error": {"code": "ax_permission_denied", "message": "辅助功能权限缺失"}}', "bridge_unavailable"),
        ("window_closed", 12, '{"error": {"code": "window_closed", "message": "微信主窗口未开"}}', "bridge_degraded"),
        ("ax_tree_empty", 13, '{"error": {"code": "ax_tree_empty", "message": "AX 树空"}}', "bridge_degraded"),
        ("send_ax_focus_required", 15, '{"error": {"code": "send_ax_focus_required", "message": "AX 静默发送不可行"}}', "bridge_degraded"),
        ("db_not_found", 20, '{"error": {"code": "db_not_found", "message": "db_storage 定位失败"}}', "weixin_local_send_error"),
        ("key_unavailable", 21, '{"error": {"code": "key_unavailable", "message": "密钥不可得"}}', "weixin_local_send_error"),
        ("decrypt_failed", 22, '{"error": {"code": "decrypt_failed", "message": "解密失败"}}', "weixin_local_send_error"),
        ("not_implemented", 1, '{"error": {"code": "not_implemented", "message": "实现层尚未落地"}}', "weixin_local_send_error"),
        ("invalid_json_stdout", 1, "not-json-at-all", "weixin_local_send_error"),
        ("empty_stdout", 1, "", "weixin_local_send_error"),
        ("bridge_timeout_exit_30", 30, '{"error": {"code": "timeout", "message": "子进程超时"}}', "bridge_timeout"),
        ("usage_exit_2", 2, "", "bridge_usage_error"),
    ]

    @pytest.mark.parametrize(
        "label,exit_code,stdout,expected", ROWS, ids=[r[0] for r in ROWS]
    )
    def test_row_maps_to_expected_code_and_never_dead(
        self, chat_env, label, exit_code, stdout, expected
    ):
        stderr = "wechat-bridge: usage error" if exit_code == 2 else ""
        channel = _channel(
            bridge_bin="/bin/sh", runner=_mock_runner((exit_code, stdout, stderr))
        )

        with pytest.raises(PushSendError) as excinfo:
            _run(channel.send(ITEMS, CONTEXT))
        assert excinfo.value.code == expected
        assert classify_dead_error(excinfo.value) is None  # 零死信:全表无一 dead

    def test_invalid_json_carries_stderr_fragment(self, chat_env):
        """stdout 非法 JSON:错误文案带原始片段。"""
        channel = _channel(
            bridge_bin="/bin/sh", runner=_mock_runner((1, "{{broken", "bridge boom detail"))
        )

        with pytest.raises(PushSendError) as excinfo:
            _run(channel.send(ITEMS, CONTEXT))
        assert excinfo.value.code == "weixin_local_send_error"
        assert "boom detail" in str(excinfo.value)

    def test_bridge_error_messages_never_hit_dead_markers(self, chat_env):
        """静态对账:桥具名族的消息/指引文案全中文,与 core 死信分类器的
        ASCII marker 表无 forbidden/not_found 交集(零死信闭口)。"""
        from myssia.push.delivery import (
            _CHAT_LEVEL_NOT_FOUND_MARKERS,
            _FORBIDDEN_MARKERS,
        )

        bridge_texts = [
            "微信进程不在运行,UI 通道无对象可驱",
            "辅助功能权限缺失:桥宿主进程未被授权",
            "微信主窗口未开(托盘态)",
            "AX 树空/残缺",
            "AX 静默发送不可行",
            "距上次发送不足 10 秒(桥内硬编码频控)",
            "db_storage 定位失败",
            "本地库密钥不可得",
            "解密失败",
        ]
        for text in bridge_texts:
            blob = text.lower()
            assert not any(m in blob for m in _FORBIDDEN_MARKERS), text
            assert not any(m in blob for m in _CHAT_LEVEL_NOT_FOUND_MARKERS), text

    def test_exit_0_with_error_payload_still_maps(self, chat_env):
        """防御:exit 0 但 payload 带 error(契约不该出现)→ 按错误表映射。"""
        channel = _channel(
            bridge_bin="/bin/sh",
            runner=_mock_runner(
                (0, '{"error": {"code": "wechat_not_running", "message": "微信不在"}}', "")
            ),
        )

        with pytest.raises(PushSendError) as excinfo:
            _run(channel.send(ITEMS, CONTEXT))
        assert excinfo.value.code == "bridge_unavailable"


class TestTimeoutAndUsage:
    def test_bridge_timeout_is_transient(self, chat_env):
        """runner 抛 :class:`LocalBridgeTimeoutError` → ``bridge_timeout`` 瞬态。"""
        channel = _channel(
            bridge_bin="/bin/sh",
            runner=_raising_runner(
                LocalBridgeTimeoutError("wechat-bridge 超过 60s 未退出,子进程已终止")
            ),
        )

        with pytest.raises(PushSendError) as excinfo:
            _run(channel.send(ITEMS, CONTEXT))
        assert excinfo.value.code == "bridge_timeout"
        assert classify_dead_error(excinfo.value) is None

    def test_default_timeout_is_60s_module_constant(self):
        """60s 模块常量(与蓝本 120s 的差异是刻意事实:无上游重试嵌套)。"""
        assert DEFAULT_BRIDGE_TIMEOUT_SECONDS == 60.0
        assert DEFAULT_PROBE_TIMEOUT_SECONDS == 30.0
        assert _channel()._timeout == DEFAULT_BRIDGE_TIMEOUT_SECONDS

    def test_usage_exit_2_logs_error(self, chat_env, caplog):
        """exit 2 = MYIA argv 契约漂移(自家 bug):ERROR 级日志 + stderr 原文。"""
        channel = _channel(
            bridge_bin="/bin/sh",
            runner=_mock_runner((2, "", "wechat-bridge: send_text is required\n")),
        )

        with pytest.raises(PushSendError) as excinfo, caplog.at_level("ERROR"):
            _run(channel.send(ITEMS, CONTEXT))
        assert excinfo.value.code == "bridge_usage_error"
        assert "send_text is required" in str(excinfo.value)
        assert any(r.levelname == "ERROR" for r in caplog.records)

    def test_runner_file_not_found_maps_unavailable(self, chat_env):
        """预检放过后子进程仍 FileNotFoundError(竞态)→ 同归
        ``bridge_unavailable`` 带指引。"""
        channel = _channel(
            bridge_bin="/bin/sh",
            runner=_raising_runner(FileNotFoundError(2, "No such file", "/fake/bridge")),
        )

        with pytest.raises(PushSendError) as excinfo:
            _run(channel.send(ITEMS, CONTEXT))
        assert excinfo.value.code == "bridge_unavailable"
        assert classify_dead_error(excinfo.value) is None
        # 频控在桥内,MYIA 不复制:发送错误都不是「配置类」(修配置无解的
        # 环境态走瞬态账本;target 解析类才是配置类,下一节单独断言)。
        assert is_config_send_error(excinfo.value) is False


# ---------------------------------------------------------------------------
# 真实子进程冒烟(缺省 runner:fake bridge 二进制回显预录 JSON,克制口径)
# ---------------------------------------------------------------------------


class TestRealSubprocess:
    def test_default_runner_success_with_fake_bridge_echo(self, tmp_path, chat_env):
        """真子进程端到端:回显预录成功 JSON 的 fake bridge → 送达。"""
        script = tmp_path / "wechat-bridge-fake"
        _write_executable(script, f"#!/bin/sh\ncat >/dev/null\necho '{BRIDGE_SUCCESS_STDOUT}'\n")
        channel = _channel(bridge_bin=str(script))

        _run(channel.send(ITEMS, CONTEXT))  # 不抛即成功

    def test_default_runner_timeout_kills_subprocess(self, tmp_path, chat_env):
        """真子进程超时:sleep 脚本 + 0.25s 超时 → kill + ``bridge_timeout``。"""
        script = tmp_path / "wechat-bridge-slow"
        _write_executable(script, "#!/bin/sh\nsleep 5\n")
        channel = _channel(bridge_bin=str(script), timeout=0.25)

        with pytest.raises(PushSendError) as excinfo:
            _run(channel.send(ITEMS, CONTEXT))
        assert excinfo.value.code == "bridge_timeout"
        assert classify_dead_error(excinfo.value) is None

    def test_default_runner_missing_bin_raises_unavailable(self, chat_env):
        """预检捕获缺 bin 场景;不可执行 bin(无 X 位)同样预检拒。"""
        channel = _channel(bridge_bin="/definitely/not/here/wechat-bridge")

        with pytest.raises(PushSendError) as excinfo:
            _run(channel.send(ITEMS, CONTEXT))
        assert excinfo.value.code == "bridge_unavailable"

    def test_sync_runner_roundtrip(self, tmp_path):
        """同步 runner(sidecar handler 宿主):回显脚本 exit/stdout 原样;
        超时路径抛 :class:`LocalBridgeTimeoutError`。"""
        script = tmp_path / "wechat-bridge-sync"
        _write_executable(script, "#!/bin/sh\necho '{\"state\": \"ok\"}'\n")

        exit_code, stdout, _ = run_bridge_command_sync([str(script)])
        assert (exit_code, json.loads(stdout)["state"]) == (0, "ok")

        slow = tmp_path / "wechat-bridge-sync-slow"
        _write_executable(slow, "#!/bin/sh\nsleep 5\n")
        with pytest.raises(LocalBridgeTimeoutError):
            run_bridge_command_sync([str(slow)], timeout=0.25)


# ---------------------------------------------------------------------------
# 寻址:legacy target 引用;无目录寻址
# ---------------------------------------------------------------------------


class TestAddressing:
    def test_legacy_target_env_resolution(self, monkeypatch):
        """legacy target 引用发送期解析(env: 引用)。"""
        monkeypatch.setenv("MYIA_TEST_WEIXIN_LOCAL_CHAT", "filehelper")
        calls: list[dict] = []
        channel = _channel(
            bridge_bin="/bin/sh", runner=_mock_runner((0, BRIDGE_SUCCESS_STDOUT, ""), calls)
        )

        _run(channel.send(ITEMS, CONTEXT))

        assert calls[0]["argv"][2] == "filehelper"

    def test_legacy_target_resolution_failure_is_structured(self, monkeypatch):
        monkeypatch.delenv("MYIA_TEST_WEIXIN_LOCAL_CHAT", raising=False)
        channel = _channel(
            bridge_bin="/bin/sh", runner=_mock_runner((0, "{}", ""), [])
        )

        with pytest.raises(PushSendError) as excinfo:
            _run(channel.send(ITEMS, CONTEXT))
        assert excinfo.value.code == "env_var_missing"
        assert is_config_send_error(excinfo.value) is True

    def test_no_target_fails_fast(self):
        channel = WeixinLocalChannel(
            bridge_bin="/bin/sh", runner=_mock_runner((0, "{}", ""), [])
        )

        with pytest.raises(PushSendError) as excinfo:
            _run(channel.send(ITEMS, CONTEXT))
        assert excinfo.value.code == "missing_target"

    def test_blank_resolved_chat_rejected_before_subprocess(self, monkeypatch):
        """解析值空白 → invalid_credential_ref(argv 不携带空白会话 id)。"""
        monkeypatch.setenv("MYIA_TEST_WEIXIN_LOCAL_CHAT", "   ")
        calls: list[dict] = []
        channel = _channel(
            bridge_bin="/bin/sh", runner=_mock_runner((0, "{}", ""), calls)
        )

        with pytest.raises(PushSendError) as excinfo:
            _run(channel.send(ITEMS, CONTEXT))
        assert excinfo.value.code == "invalid_credential_ref"
        assert calls == []

    def test_context_target_is_ignored_by_design(self, monkeypatch):
        """无目录寻址:context.target 在场也不采用(defensive;寻址唯一路径
        = legacy target 引用)。"""
        monkeypatch.setenv("MYIA_TEST_WEIXIN_LOCAL_CHAT", "legacy-chat")
        calls: list[dict] = []
        channel = _channel(
            bridge_bin="/bin/sh", runner=_mock_runner((0, BRIDGE_SUCCESS_STDOUT, ""), calls)
        )

        _run(channel.send(ITEMS, replace(CONTEXT, target=None)))

        assert calls[0]["argv"][2] == "legacy-chat"

    def test_discover_directory_raises_unsupported(self):
        with pytest.raises(DirectoryDiscoverUnsupported) as excinfo:
            _run(WeixinLocalChannel().discover_directory())
        assert "无目录寻址" in str(excinfo.value)


# ---------------------------------------------------------------------------
# 模板(蓝本对齐)
# ---------------------------------------------------------------------------


class TestTemplate:
    def test_user_template_replaces_builtin_layout(self, chat_env):
        calls: list[dict] = []
        channel = _channel(
            bridge_bin="/bin/sh",
            template="{{ date }} 共 {{ items|length }} 条",
            runner=_mock_runner((0, BRIDGE_SUCCESS_STDOUT, ""), calls),
        )

        _run(channel.send(ITEMS, CONTEXT))

        assert calls[0]["input"] == "2026-10-11 共 2 条"

    def test_template_render_failure_is_structured(self, chat_env):
        channel = _channel(
            bridge_bin="/bin/sh", template="{{ no_such_helper() }}",
            runner=_mock_runner((0, "{}", ""), []),
        )

        with pytest.raises(PushSendError) as excinfo:
            _run(channel.send(ITEMS, CONTEXT))
        assert excinfo.value.code == "template_render_error"

    def test_long_body_not_prechunked(self, chat_env):
        """长文不预切(G6 单条契约:一条调用 = 一条消息)。"""
        calls: list[dict] = []
        channel = _channel(
            bridge_bin="/bin/sh",
            runner=_mock_runner((0, BRIDGE_SUCCESS_STDOUT, ""), calls),
        )
        items = [{"title": "长" * 6000, "url": "https://x/1"}]

        _run(channel.send(items, CONTEXT))

        assert len(calls[0]["input"]) > 6000  # 原样整条,不截不拆


# ---------------------------------------------------------------------------
# probe_local_bridge(fake bridge 回显预录 probe JSON;三态合成兜底)
# ---------------------------------------------------------------------------

PROBE_OK_STDOUT = json.dumps(
    {
        "ok": True,
        "state": "ok",
        "checks": {"bridge_component": "ok", "wechat_process": "ok"},
        "wechat_version": "4.1.15",
        "bridge_version": "0.2.0",
        "reasons": [],
    }
) + "\n"


class TestProbeLocalBridge:
    def test_probe_passthrough_bridge_payload(self, tmp_path):
        """桥在场:``--probe`` 应答原样透传(键序即组件 to_payload)。"""
        script = tmp_path / "wechat-bridge-probe"
        _write_executable(script, f"#!/bin/sh\necho '{PROBE_OK_STDOUT}'\n")

        payload = probe_local_bridge(str(script))

        assert payload["ok"] is True
        assert payload["state"] == "ok"
        assert payload["wechat_version"] == "4.1.15"
        assert payload["bridge_version"] == "0.2.0"

    def test_probe_missing_bin_synthesizes_unavailable(self, tmp_path):
        """组件缺席:同形合成载荷(state=bridge_unavailable),不裸抛——
        探针是健康面,健康面自己必须先健康。"""
        payload = probe_local_bridge(str(tmp_path / "absent"))

        assert payload["ok"] is False
        assert payload["state"] == "bridge_unavailable"
        assert payload["checks"] == {"bridge_component": "missing"}
        assert payload["reasons"][0]["code"] == "component_missing"

    def test_probe_timeout_synthesizes_unavailable(self, tmp_path):
        """探针挂死:kill + 合成 probe_timeout 载荷。"""
        script = tmp_path / "wechat-bridge-probe-slow"
        _write_executable(script, "#!/bin/sh\nsleep 5\n")

        payload = probe_local_bridge(str(script), timeout=0.25)

        assert payload["state"] == "bridge_unavailable"
        assert payload["reasons"][0]["code"] == "probe_timeout"

    def test_probe_unparseable_stdout_synthesizes_unavailable(self, tmp_path):
        """应答非契约 JSON(exit 非 0):合成 probe_unparseable(f-string 内插
        真实 exit 码,不字面输出占位符)。"""
        script = tmp_path / "wechat-bridge-probe-bad"
        _write_executable(script, "#!/bin/sh\necho 'not-json'\nexit 3\n")

        payload = probe_local_bridge(str(script))

        assert payload["state"] == "bridge_unavailable"
        assert payload["reasons"][0]["code"] == "probe_unparseable"
        assert "无法识别的结果" in payload["reasons"][0]["fix_hint"]
        assert "{exit_code}" not in payload["reasons"][0]["fix_hint"]

    def test_default_bin_path_constant(self):
        """缺省 bin 常量 = design §7 缺省(受管组件落点;B3 安装链路对齐)。"""
        assert DEFAULT_BRIDGE_BIN == "~/.myia/plugins/wechat-bridge/bin/wechat-bridge"
        assert os.path.isabs(os.path.expanduser(DEFAULT_BRIDGE_BIN))


# ---------------------------------------------------------------------------
# 注册表 + schema 门(enabled 显式开关 / 字段宿主 / pipeline 下传)
# ---------------------------------------------------------------------------


class TestRegistryAndSchema:
    def test_channel_registered_not_in_platforms(self):
        """CHANNELS 注册(通道 id weixin-local,G7);不入 PLATFORMS /
        CHANNEL_PLATFORMS(无目录寻址,targets 配即拒,同 webhook)。"""
        from myssia.push import CHANNELS, PLATFORMS

        assert CHANNELS["weixin-local"] is WeixinLocalChannel
        assert "weixin-local" not in PLATFORMS
        assert "weixin-local" not in CHANNEL_PLATFORMS
        assert "weixin-local" in PUSH_CHANNELS
        assert WeixinLocalChannel.name == "weixin-local"
        assert WeixinLocalChannel.supports_targeting is False

    def _write_category(self, tmp_path, push_entry: str) -> Any:
        yaml_text = f"""
id: weixin-local-demo
name: 微信本机通道夹具
schedule: "0 9 * * *"
sources:
  - name: local-api
    engine: direct_api
    url: "http://127.0.0.1:9/x"
    rate_limit:
      qps: 1000.0
      respect_robots: false
    retry: 0
    extract:
      type: json_path
      fields:
        title: "$.a"
        url: "$.b"
classify:
  builtin: false
push:
{push_entry}
"""
        path = tmp_path / "weixin-local-demo.yaml"
        path.write_text(yaml_text, encoding="utf-8")
        return load_category_file(path)

    def test_enabled_entry_loads_and_pipeline_passes_bin(self, tmp_path):
        """显式开启 + target + bin 覆写:加载通过;pipeline 构造下传
        wechat_bridge_bin → bridge_bin。"""
        config = self._write_category(
            tmp_path,
            (
                "  - channel: weixin-local\n"
                "    target: env:WEIXIN_LOCAL_CHAT_ID\n"
                "    weixin_local_enabled: true\n"
                "    wechat_bridge_bin: /opt/bridge/bin/wechat-bridge\n"
            ),
        )
        entry = config.push[0]
        assert entry.channel == "weixin-local"
        assert entry.weixin_local_enabled is True
        assert entry.wechat_bridge_bin == "/opt/bridge/bin/wechat-bridge"

        channel = _build_push_channel(entry, data_root=tmp_path)
        assert isinstance(channel, WeixinLocalChannel)
        assert channel._bridge_bin == "/opt/bridge/bin/wechat-bridge"

    def test_disabled_entry_fails_fast_at_load(self, tmp_path):
        """缺省关:不带 weixin_local_enabled 的条目加载期拒
        (weixin_local_disabled;不留「配了却不发」的静默忽略)。"""
        with pytest.raises(LoadError) as excinfo:
            self._write_category(
                tmp_path,
                "  - channel: weixin-local\n    target: env:WEIXIN_LOCAL_CHAT_ID\n",
            )
        assert "weixin_local_disabled" in str(excinfo.value)

    def test_enabled_false_fails_fast_too(self, tmp_path):
        """显式 false 同拒(缺省关 = false,写条目就必须真开)。"""
        with pytest.raises(LoadError) as excinfo:
            self._write_category(
                tmp_path,
                (
                    "  - channel: weixin-local\n"
                    "    target: env:WEIXIN_LOCAL_CHAT_ID\n"
                    "    weixin_local_enabled: false\n"
                ),
            )
        assert "weixin_local_disabled" in str(excinfo.value)

    def test_targets_rejected_like_webhook(self, tmp_path):
        """无目录寻址:targets 配即拒(targeting_not_supported,webhook 同款)。"""
        with pytest.raises(LoadError) as excinfo:
            self._write_category(
                tmp_path,
                (
                    "  - channel: weixin-local\n"
                    "    targets: [\"weixin:某群\"]\n"
                    "    weixin_local_enabled: true\n"
                ),
            )
        assert "targeting_not_supported" in str(excinfo.value)

    def test_field_hosting(self, tmp_path):
        """字段宿主门:wechat_bridge_bin/weixin_local_enabled 仅 weixin-local
        可配(别处出现 = unexpected_platform_field)。"""
        with pytest.raises(LoadError) as excinfo:
            self._write_category(
                tmp_path,
                (
                    "  - channel: weixin\n"
                    "    target: env:WEIXIN_PEER_ID\n"
                    "    weixin_local_enabled: true\n"
                ),
            )
        assert "unexpected_platform_field" in str(excinfo.value)

    def test_w2_kwargs_mapping_registered(self):
        """pipeline kwargs 下传映射在册(字段名 → 构造参数名)。"""
        assert _W2_CHANNEL_FIELD_KWARGS["weixin-local"] == (
            ("wechat_bridge_bin", "bridge_bin"),
        )
