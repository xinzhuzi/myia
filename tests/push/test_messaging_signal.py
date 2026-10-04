"""Tests for signal 适配器(10-05-push-reliability-batch R3 出壳)。

壳沿革:10-03-messaging-w3-longtail R3 曾按「外部守护进程不进核心」立
extras 壳(``send()`` 恒抛 ``dependency_missing``);本批出壳——真发送路
为 signal-cli 守护进程 HTTP 模式的 JSON-RPC 2.0(蓝本 Hermes
``gateway/platforms/signal.py``,MIT)。覆盖:JSON-RPC ``send`` 出站形态
(recipient/groupId 双分支路由)、分段(8000)、错误信封(版本差异两形态:
typed code 与旧版文本子串均原样透传)、逐收件人失败 type 透传、传输
不可达 = 瞬态、凭据 env→钥匙链回退(10-05-push-credential-journey 口径)、
定向(context.target)优先与 legacy 兜底、missing_target fail-fast、
直达 ``+手机号``(E.164)与目录名寻址、无自动发现语义、Channel 协议面。

No pytest-asyncio: async calls run through ``asyncio.run``(同
test_push.py 约定)。All network I/O goes through ``httpx.MockTransport``;
钥匙链一律 ``InMemoryKeychainBackend`` 注入,零真实钥匙串、零外网。
"""

from __future__ import annotations

import asyncio
import json
from dataclasses import replace
from typing import Any

import httpx
import pytest

from myssia import secrets as secrets_store
from myssia.push import SendContext
from myssia.push.base import Channel, PushSendError, TrendAwareChannel
from myssia.push.delivery import classify_dead_error
from myssia.push.directory import ChannelDirectory, DirectoryDiscoverUnsupported
from myssia.push.signal import (
    MESSAGE_LIMIT,
    RPC_PATH,
    SignalChannel,
)
from myssia.push.targets import RESOLVED_DIRECT, RESOLVED_DIRECTORY_NAME, ChannelTarget, resolve_target

CONTEXT = SendContext(slot="am", date="2026-10-03", category="羊毛", kind="digest")
DAEMON_URL = "http://127.0.0.1:8080"
ACCOUNT = "+8613800138000"
RECIPIENT = "+8613900139000"
GROUP_ID = "a2V5Z3JvdXBpZA=="

#: 真实 PLATFORMS 登记 is 集成步(push/__init__);本文件用显式注册表钉
#: 直达语义,登记后零改动生效。
PLATFORMS: dict[str, type] = {"signal": SignalChannel}

_SIGNAL_ENV_KEYS = ("SIGNAL_HTTP_URL", "SIGNAL_ACCOUNT", "SIGNAL_CHAT")


@pytest.fixture(autouse=True)
def _in_memory_keychain(monkeypatch):
    """每用例独立 InMemory 钥匙链 + signal 推送 env 清零;用毕复位。"""
    secrets_store.set_backend(secrets_store.InMemoryKeychainBackend())
    for var in _SIGNAL_ENV_KEYS:
        monkeypatch.delenv(var, raising=False)
    yield
    secrets_store.reset_backend()


def _run(coro: Any) -> Any:
    return asyncio.run(coro)


def _target(chat_id: str) -> ChannelTarget:
    return ChannelTarget(platform="signal", chat_id=chat_id, resolved_from=RESOLVED_DIRECT)


def _ok_response(request: httpx.Request) -> httpx.Response:
    """蓝本成功应答形态:result.timestamp + results[*].type=SUCCESS。"""
    return httpx.Response(
        200,
        json={
            "jsonrpc": "2.0",
            "id": json.loads(request.content.decode("utf-8")).get("id"),
            "result": {"timestamp": 1760000000000, "results": [{"type": "SUCCESS"}]},
        },
    )


def _channel(
    handler: Any | None = None, *, env: bool = True, monkeypatch: Any = None, **kwargs: Any
) -> SignalChannel:
    if env and monkeypatch is not None:
        monkeypatch.setenv("SIGNAL_HTTP_URL", DAEMON_URL)
        monkeypatch.setenv("SIGNAL_ACCOUNT", ACCOUNT)
    client = kwargs.pop("client", None) or httpx.AsyncClient(
        transport=httpx.MockTransport(handler or _ok_response)
    )
    return SignalChannel(client=client, **kwargs)


# ---------------------------------------------------------------------------
# 真发送:JSON-RPC 出站形态(蓝本 _rpc/send/_with_target 移植)
# ---------------------------------------------------------------------------


class TestJsonRpcSend:
    def test_send_posts_rpc_send_with_recipient(self, monkeypatch):
        """手机号 target → ``POST {url}/api/v1/rpc`` JSON-RPC ``send``,recipient 列表。"""
        calls: list[httpx.Request] = []

        def handler(request: httpx.Request) -> httpx.Response:
            calls.append(request)
            return _ok_response(request)

        channel = _channel(handler, monkeypatch=monkeypatch, target="env:SIGNAL_CHAT")
        monkeypatch.setenv("SIGNAL_CHAT", RECIPIENT)

        _run(channel.send([{"title": "羊毛", "url": "https://x/1"}], CONTEXT))

        assert len(calls) == 1
        assert str(calls[0].url) == f"{DAEMON_URL}{RPC_PATH}"
        payload = json.loads(calls[0].content.decode("utf-8"))
        assert payload["jsonrpc"] == "2.0"
        assert payload["method"] == "send"
        assert payload["id"]
        params = payload["params"]
        assert set(params) == {"account", "message", "recipient"}
        assert params["account"] == ACCOUNT
        assert params["recipient"] == [RECIPIENT]
        assert "羊毛" in params["message"] and "https://x/1" in params["message"]

    def test_group_chat_id_routes_group_id_param(self, monkeypatch):
        """非号码形 chat_id(目录登记的群 id,base64)→ ``groupId`` 参数(蓝本双分支)。"""
        calls: list[httpx.Request] = []

        def handler(request: httpx.Request) -> httpx.Response:
            calls.append(request)
            return _ok_response(request)

        channel = _channel(handler, monkeypatch=monkeypatch)

        _run(channel.send([{"title": "t"}], replace(CONTEXT, target=_target(GROUP_ID))))

        payload = json.loads(calls[0].content.decode("utf-8"))
        assert payload["params"]["groupId"] == GROUP_ID
        assert "recipient" not in payload["params"]

    def test_context_target_overrides_legacy(self, monkeypatch):
        """定向优先:context.target 的手机号覆盖 legacy target。"""
        calls: list[httpx.Request] = []

        def handler(request: httpx.Request) -> httpx.Response:
            calls.append(request)
            return _ok_response(request)

        channel = _channel(handler, monkeypatch=monkeypatch, target="env:SIGNAL_CHAT")
        monkeypatch.setenv("SIGNAL_CHAT", "+8613700137000")

        _run(channel.send([{"title": "t"}], replace(CONTEXT, target=_target(RECIPIENT))))

        payload = json.loads(calls[0].content.decode("utf-8"))
        assert payload["params"]["recipient"] == [RECIPIENT]

    def test_long_message_splits_per_chunk(self, monkeypatch):
        """超 :data:`MESSAGE_LIMIT`(8000)自动分段,逐块独立 JSON-RPC 请求。"""
        calls: list[httpx.Request] = []

        def handler(request: httpx.Request) -> httpx.Response:
            calls.append(request)
            return _ok_response(request)

        channel = _channel(handler, monkeypatch=monkeypatch)
        long_title = "长" * (MESSAGE_LIMIT + 500)

        _run(channel.send([{"title": long_title}], replace(CONTEXT, target=_target(RECIPIENT))))

        # 标题行先在行边界切,长行再按上限硬切——块数 ≥2 即分段生效。
        assert len(calls) >= 2
        messages = [
            json.loads(request.content.decode("utf-8"))["params"]["message"]
            for request in calls
        ]
        assert all(len(text) <= MESSAGE_LIMIT for text in messages)
        assert "".join(messages).count("长") == MESSAGE_LIMIT + 500
        # 蓝本同款:rpc id 每请求唯一(计数器 + 毫秒)。
        ids = [json.loads(request.content.decode("utf-8"))["id"] for request in calls]
        assert len(set(ids)) == len(calls)


# ---------------------------------------------------------------------------
# 错误语义:结构化 code + 瞬态/配置级如实分类
# ---------------------------------------------------------------------------


class TestErrorSemantics:
    def test_transport_unreachable_is_transient(self, monkeypatch):
        """守护进程不可达 → ``http_error``(瞬态,不标死信)。"""
        def handler(request: httpx.Request) -> httpx.Response:
            raise httpx.ConnectError("connection refused")

        channel = _channel(handler, monkeypatch=monkeypatch)

        with pytest.raises(PushSendError) as excinfo:
            _run(channel.send([{"title": "t"}], replace(CONTEXT, target=_target(RECIPIENT))))
        assert excinfo.value.code == "http_error"
        assert "signal-cli" in str(excinfo.value)  # 守护进程指引
        assert classify_dead_error(excinfo.value) is None

    def test_jsonrpc_error_envelope_typed_code_surfaced(self, monkeypatch):
        """JSON-RPC error 信封(signal-cli ≥0.14.3 typed code)→ code+message 透传。"""
        def handler(request: httpx.Request) -> httpx.Response:
            return httpx.Response(
                200, json={"jsonrpc": "2.0", "error": {"code": -5, "message": "RateLimitException"}}
            )

        channel = _channel(handler, monkeypatch=monkeypatch)

        with pytest.raises(PushSendError) as excinfo:
            _run(channel.send([{"title": "t"}], replace(CONTEXT, target=_target(RECIPIENT))))
        assert excinfo.value.code == "signal_api_error"
        assert "-5" in str(excinfo.value) and "RateLimitException" in str(excinfo.value)
        assert classify_dead_error(excinfo.value) is None  # 限流 = 瞬态

    def test_jsonrpc_error_legacy_text_only_shape(self, monkeypatch):
        """旧版 signal-cli 错误只在 message 文本漏 ``[429]`` 子串——同路透传(版本差异不分叉)。"""
        def handler(request: httpx.Request) -> httpx.Response:
            return httpx.Response(
                200, json={"jsonrpc": "2.0", "error": {"message": "RateLimitException: [429] retry later"}}
            )

        channel = _channel(handler, monkeypatch=monkeypatch)

        with pytest.raises(PushSendError) as excinfo:
            _run(channel.send([{"title": "t"}], replace(CONTEXT, target=_target(RECIPIENT))))
        assert excinfo.value.code == "signal_api_error"
        assert "[429]" in str(excinfo.value)

    def test_per_recipient_failure_type_surfaced(self, monkeypatch):
        """``results[*].type != SUCCESS``(蓝本 _validate_send_result)→ 原厂 type 透传。"""
        def handler(request: httpx.Request) -> httpx.Response:
            return httpx.Response(
                200,
                json={
                    "jsonrpc": "2.0",
                    "result": {"timestamp": 1, "results": [{"type": "UNREGISTERED_FAILURE"}]},
                },
            )

        channel = _channel(handler, monkeypatch=monkeypatch)

        with pytest.raises(PushSendError) as excinfo:
            _run(channel.send([{"title": "t"}], replace(CONTEXT, target=_target(RECIPIENT))))
        assert excinfo.value.code == "signal_api_error"
        assert "UNREGISTERED_FAILURE" in str(excinfo.value)

    def test_http_error_status_not_chat_level(self, monkeypatch):
        """daemon 级 HTTP 失败(地址/版本配错)→ 措辞「HTTP 状态 N」,不触 chat 级 not_found 锚。"""
        def handler(request: httpx.Request) -> httpx.Response:
            return httpx.Response(500, text="boom")

        channel = _channel(handler, monkeypatch=monkeypatch)

        with pytest.raises(PushSendError) as excinfo:
            _run(channel.send([{"title": "t"}], replace(CONTEXT, target=_target(RECIPIENT))))
        assert excinfo.value.code == "signal_api_error"
        assert "HTTP 状态 500" in str(excinfo.value)
        assert classify_dead_error(excinfo.value) is None

    def test_non_json_response_invalid(self, monkeypatch):
        def handler(request: httpx.Request) -> httpx.Response:
            return httpx.Response(200, text="<html>not json</html>")

        channel = _channel(handler, monkeypatch=monkeypatch)

        with pytest.raises(PushSendError) as excinfo:
            _run(channel.send([{"title": "t"}], replace(CONTEXT, target=_target(RECIPIENT))))
        assert excinfo.value.code == "invalid_response"

    def test_missing_result_envelope_fails_closed(self, monkeypatch):
        """200 + JSON 对象但无 result(反代/健康端点形态)→ 拒绝,绝不静默记成功。

        蓝本 ``_rpc_send``(上游 signal.py:694-697)对 ``result is None`` 判
        SendResult(success=False) fail-closed;MYIA 同款——放行会把推送吞掉且
        记成功,重试账本也无失败可入账。
        """
        def handler(request: httpx.Request) -> httpx.Response:
            return httpx.Response(200, json={"jsonrpc": "2.0", "id": "x"})

        channel = _channel(handler, monkeypatch=monkeypatch)

        with pytest.raises(PushSendError) as excinfo:
            _run(channel.send([{"title": "t"}], replace(CONTEXT, target=_target(RECIPIENT))))
        assert excinfo.value.code == "invalid_response"
        assert "SIGNAL_HTTP_URL" in str(excinfo.value)  # 指错端点的修复指引

    def test_non_object_result_fails_closed(self, monkeypatch):
        """result 在场但非对象(字符串等坏形)→ 同拒(MYIA 对蓝本的同向收紧)。"""
        def handler(request: httpx.Request) -> httpx.Response:
            return httpx.Response(200, json={"jsonrpc": "2.0", "id": "x", "result": "ok"})

        channel = _channel(handler, monkeypatch=monkeypatch)

        with pytest.raises(PushSendError) as excinfo:
            _run(channel.send([{"title": "t"}], replace(CONTEXT, target=_target(RECIPIENT))))
        assert excinfo.value.code == "invalid_response"

    def test_missing_target_is_config_error(self, monkeypatch):
        """两路寻址全缺 → ``missing_target``(配置类码,不标死信)。"""
        channel = _channel(monkeypatch=monkeypatch)

        with pytest.raises(PushSendError) as excinfo:
            _run(channel.send([{"title": "t"}], CONTEXT))
        assert excinfo.value.code == "missing_target"
        assert classify_dead_error(excinfo.value) is None


# ---------------------------------------------------------------------------
# 凭据:env → 钥匙链规范名回退(10-05-push-credential-journey 口径)
# ---------------------------------------------------------------------------


class TestCredentials:
    def test_missing_credentials_guide_to_settings(self, monkeypatch):
        """env 与钥匙链双缺 → ``env_var_missing`` 指引设置→推送(壳期 dependency_missing 已退役)。"""
        channel = _channel(None, env=False, target="env:SIGNAL_CHAT")

        with pytest.raises(PushSendError) as excinfo:
            _run(channel.send([{"title": "t"}], CONTEXT))
        assert excinfo.value.code == "env_var_missing"
        assert "设置→推送" in str(excinfo.value)
        assert "SIGNAL_HTTP_URL" in str(excinfo.value)

    def test_keychain_fallback_drives_real_send(self, monkeypatch):
        """GUI 桌面路径:三凭据全走钥匙链规范名 ``myia/push/<ENV_KEY>`` 照发不误。"""
        calls: list[httpx.Request] = []

        def handler(request: httpx.Request) -> httpx.Response:
            calls.append(request)
            return _ok_response(request)

        channel = _channel(handler, env=False, target="env:SIGNAL_CHAT")
        secrets_store.set_secret("myia/push/SIGNAL_HTTP_URL", DAEMON_URL)
        secrets_store.set_secret("myia/push/SIGNAL_ACCOUNT", ACCOUNT)
        secrets_store.set_secret("myia/push/SIGNAL_CHAT", RECIPIENT)

        _run(channel.send([{"title": "t"}], CONTEXT))

        assert str(calls[0].url) == f"{DAEMON_URL}{RPC_PATH}"
        payload = json.loads(calls[0].content.decode("utf-8"))
        assert payload["params"]["account"] == ACCOUNT
        assert payload["params"]["recipient"] == [RECIPIENT]

    def test_env_takes_priority_over_keychain(self, monkeypatch):
        calls: list[httpx.Request] = []

        def handler(request: httpx.Request) -> httpx.Response:
            calls.append(request)
            return _ok_response(request)

        monkeypatch.setenv("SIGNAL_HTTP_URL", "http://env.example:9090")
        monkeypatch.setenv("SIGNAL_ACCOUNT", "+8611100110000")
        secrets_store.set_secret("myia/push/SIGNAL_HTTP_URL", "http://kc.example:8080")
        channel = _channel(handler, env=False, target="env:SIGNAL_CHAT")
        monkeypatch.setenv("SIGNAL_CHAT", RECIPIENT)

        _run(channel.send([{"title": "t"}], CONTEXT))

        assert str(calls[0].url).startswith("http://env.example:9090/api/v1/rpc")
        payload = json.loads(calls[0].content.decode("utf-8"))
        assert payload["params"]["account"] == "+8611100110000"


# ---------------------------------------------------------------------------
# 寻址面(壳期已接线,出壳后语义不变)
# ---------------------------------------------------------------------------


class TestAddressing:
    def test_direct_ref_parse(self):
        """E.164 手机号(可选 ``+``,7-15 位)直达;群 id/显示名/@username 回落目录(蓝本无 @username 寻址)。"""
        for ref in ["+8613800138000", "13800138000", "+15551234567"]:
            target = SignalChannel.parse_direct_ref(ref)
            assert target is not None
            assert (target.platform, target.chat_id, target.resolved_from) == (
                "signal",
                ref,
                RESOLVED_DIRECT,
            )
        for ref in ["group", "张三", "@someone", "+86-138-0013", "+abc", "", "1555123456789016"]:
            assert SignalChannel.parse_direct_ref(ref) is None

    def test_resolve_direct_via_explicit_registry(self, tmp_path):
        target = resolve_target("signal:+8613800138000", ChannelDirectory(tmp_path), platforms=PLATFORMS)

        assert (target.chat_id, target.resolved_from) == ("+8613800138000", RESOLVED_DIRECT)

    def test_resolve_via_directory_name(self, tmp_path):
        from myssia.push.directory import ChannelEntry

        directory = ChannelDirectory(tmp_path)
        directory.replace_platform(
            "signal",
            [
                ChannelEntry(platform="signal", chat_id="+8613800138000", name="张三", type="dm"),
                ChannelEntry(platform="signal", chat_id=GROUP_ID, name="行情群", type="group"),
            ],
        )

        target = resolve_target("signal:张三", directory, platforms=PLATFORMS)
        assert (target.chat_id, target.resolved_from) == ("+8613800138000", RESOLVED_DIRECTORY_NAME)


# ---------------------------------------------------------------------------
# 目录语义(无自动发现,不是失败)+ 协议面
# ---------------------------------------------------------------------------


class TestDirectorySemantics:
    def test_discover_directory_raises_unsupported(self):
        with pytest.raises(DirectoryDiscoverUnsupported) as excinfo:
            _run(SignalChannel().discover_directory())
        assert "无自动发现" in str(excinfo.value)

    def test_directory_refresh_skips_unsupported_quietly(self, tmp_path):
        directory = ChannelDirectory(tmp_path)
        directory.merge_entries("signal", [], now=1.0)

        counts = _run(directory.refresh({"signal": SignalChannel()}, now=100.0))

        assert counts == {}


class TestProtocolSurface:
    def test_channel_protocol_surface(self):
        """Channel 协议面:name/supports_targeting/TrendAwareChannel 基类。"""
        channel = SignalChannel()
        assert channel.name == "signal"
        assert channel.supports_targeting is True
        assert isinstance(channel, TrendAwareChannel)
        assert isinstance(channel, Channel)

    def test_registered_in_channel_registry(self):
        """集成注册面:CHANNELS/PLATFORMS 均登记本通道(壳期已注册,出壳零变化)。"""
        from myssia.push import CHANNELS, PLATFORMS

        assert CHANNELS["signal"] is SignalChannel
        assert PLATFORMS["signal"] is SignalChannel
