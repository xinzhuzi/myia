"""Tests for bluebubbles 适配器(10-05-push-reliability-batch R3 出壳)。

壳沿革:10-03-messaging-w3-longtail R3 曾按「外部服务端不进核心」立
extras 壳(``send()`` 恒抛 ``dependency_missing``);本批出壳——真发送路
为自建 BlueBubbles 服务端的 REST(蓝本 Hermes
``gateway/platforms/bluebubbles.py``,MIT)。覆盖:``message/text`` 出站
形态(password 查询串鉴权 + chatGuid/tempGuid/message)、裸 GUID 直通与
手机号经 ``chat/query`` 解析(严格 identifier 匹配)、邮箱/手机号地址直开
新会话(chat/new)、GUID 解析不到 = chat 级 not_found 死信锚、分段(4000)、
鉴权失败 401 文案明示核对凭据且 password 永不进错误文案、传输不可达 =
瞬态、凭据 env→钥匙链回退(10-05-push-credential-journey 口径)、URL
规范化(补 scheme)、定向(context.target)优先与 legacy 兜底、
missing_target fail-fast、直达 chat GUID/手机号与目录名寻址、无自动发现
语义、Channel 协议面。

No pytest-asyncio: async calls run through ``asyncio.run``(同
test_push.py 约定)。All network I/O goes through ``httpx.MockTransport``;
钥匙链一律 ``InMemoryKeychainBackend`` 注入,零真实钥匙串、零外网。
"""

from __future__ import annotations

import asyncio
import json
from dataclasses import replace
from typing import Any
from urllib.parse import parse_qs

import httpx
import pytest

from myssia import secrets as secrets_store
from myssia.push import SendContext
from myssia.push.base import Channel, PushSendError, TrendAwareChannel
from myssia.push.bluebubbles import (
    MESSAGE_LIMIT,
    BlueBubblesChannel,
    normalize_server_url,
)
from myssia.push.delivery import classify_dead_error
from myssia.push.directory import ChannelDirectory, ChannelEntry, DirectoryDiscoverUnsupported
from myssia.push.targets import RESOLVED_DIRECT, RESOLVED_DIRECTORY_NAME, ChannelTarget, resolve_target

CONTEXT = SendContext(slot="am", date="2026-10-03", category="羊毛", kind="digest")
SERVER = "http://127.0.0.1:1234"
PASSWORD = "bb-pass-123"
DM_GUID = "iMessage;-;+15551234567"
GROUP_GUID = "iMessage;chatC3E4B9A1-2F3D-4E5A"
SMS_GUID = "SMS;-;+15551234567"
PHONE = "+15551234567"
EMAIL = "alice@icloud.com"

#: 真实 PLATFORMS 登记 is 集成步(push/__init__);本文件用显式注册表钉
#: 直达语义,登记后零改动生效。
PLATFORMS: dict[str, type] = {"bluebubbles": BlueBubblesChannel}

_BLUEBUBBLES_ENV_KEYS = ("BLUEBUBBLES_SERVER_URL", "BLUEBUBBLES_PASSWORD", "BLUEBUBBLES_CHAT")


@pytest.fixture(autouse=True)
def _in_memory_keychain(monkeypatch):
    """每用例独立 InMemory 钥匙链 + bluebubbles 推送 env 清零;用毕复位。"""
    secrets_store.set_backend(secrets_store.InMemoryKeychainBackend())
    for var in _BLUEBUBBLES_ENV_KEYS:
        monkeypatch.delenv(var, raising=False)
    yield
    secrets_store.reset_backend()


def _run(coro: Any) -> Any:
    return asyncio.run(coro)


def _target(chat_id: str) -> ChannelTarget:
    return ChannelTarget(platform="bluebubbles", chat_id=chat_id, resolved_from=RESOLVED_DIRECT)


def _capture(request: httpx.Request) -> dict[str, Any]:
    return {
        "path": request.url.path,
        "query": parse_qs(request.url.query.decode("utf-8")),
        "body": json.loads(request.content.decode("utf-8")) if request.content else {},
    }


def _router(
    calls: list[dict[str, Any]],
    *,
    query_data: list[dict[str, Any]] | None = None,
    message_status: int = 200,
    message_text: str = "",
) -> httpx.MockTransport:
    """path 分发的 MockTransport:chat/query、chat/new、message/text 三端点。"""

    def handler(request: httpx.Request) -> httpx.Response:
        calls.append(_capture(request))
        path = request.url.path
        if path == "/api/v1/chat/query":
            return httpx.Response(200, json={"status": 200, "data": query_data or []})
        if path == "/api/v1/chat/new":
            return httpx.Response(200, json={"status": 200, "data": {"guid": "new-chat"}})
        if path == "/api/v1/message/text":
            if message_status != 200:
                return httpx.Response(message_status, text=message_text)
            return httpx.Response(200, json={"status": 200, "data": {"guid": "MSG-1"}})
        return httpx.Response(404, text="unknown path")

    return httpx.MockTransport(handler)


def _channel(calls: list[dict[str, Any]], *, env: bool = True, monkeypatch: Any = None, **kwargs: Any) -> BlueBubblesChannel:
    if env and monkeypatch is not None:
        monkeypatch.setenv("BLUEBUBBLES_SERVER_URL", SERVER)
        monkeypatch.setenv("BLUEBUBBLES_PASSWORD", PASSWORD)
    client = kwargs.pop("client", None) or httpx.AsyncClient(transport=_router(calls))
    return BlueBubblesChannel(client=client, **kwargs)


def _query_hit(identifier: str, guid: str) -> list[dict[str, Any]]:
    return [{"chatIdentifier": identifier, "guid": guid}]


# ---------------------------------------------------------------------------
# 真发送:REST 出站形态(蓝本 _api_url/_resolve_chat_guid/send 移植)
# ---------------------------------------------------------------------------


class TestRestSend:
    def test_raw_guid_posts_message_text_with_password_query(self, monkeypatch):
        """裸 chat GUID(含 ``;``)直通:不查 chat/query,直接 ``message/text``。"""
        calls: list[dict[str, Any]] = []
        channel = _channel(calls, monkeypatch=monkeypatch)

        _run(channel.send([{"title": "羊毛", "url": "https://x/1"}], replace(CONTEXT, target=_target(DM_GUID))))

        assert [call["path"] for call in calls] == ["/api/v1/message/text"]
        call = calls[0]
        # 鉴权走查询串(蓝本 _api_url 同款:BlueBubbles 不能发自定义头)。
        assert call["query"].get("password") == [PASSWORD]
        assert set(call["body"]) == {"chatGuid", "tempGuid", "message"}
        assert call["body"]["chatGuid"] == DM_GUID
        assert call["body"]["tempGuid"].startswith("temp-")
        assert "羊毛" in call["body"]["message"] and "https://x/1" in call["body"]["message"]

    def test_phone_target_resolves_guid_via_chat_query(self, monkeypatch):
        """手机号 target → ``chat/query`` 严格匹配 ``chatIdentifier`` 后按 GUID 发。"""
        calls: list[dict[str, Any]] = []
        channel = _channel(
            calls,
            monkeypatch=monkeypatch,
            client=httpx.AsyncClient(
                transport=_router(calls, query_data=_query_hit(PHONE, DM_GUID))
            ),
        )

        _run(channel.send([{"title": "t"}], replace(CONTEXT, target=_target(PHONE))))

        assert [call["path"] for call in calls] == ["/api/v1/chat/query", "/api/v1/message/text"]
        assert calls[0]["body"] == {"limit": 100, "offset": 0}
        assert calls[1]["body"]["chatGuid"] == DM_GUID

    def test_query_strict_identifier_no_participant_fallback(self, monkeypatch):
        """参与者成员不做回退(蓝本防 DM 回复漏进群会话):identifier 不匹配即视为未解析。"""
        calls: list[dict[str, Any]] = []
        channel = _channel(
            calls,
            monkeypatch=monkeypatch,
            client=httpx.AsyncClient(
                transport=_router(
                    calls,
                    query_data=[{"chatIdentifier": "+15559990000", "guid": "iMessage;-;+15559990000"}],
                )
            ),
        )

        with pytest.raises(PushSendError) as excinfo:
            _run(channel.send([{"title": "t"}], replace(CONTEXT, target=_target("unknown-handle"))))
        assert excinfo.value.code == "bluebubbles_api_error"

    def test_context_target_overrides_legacy(self, monkeypatch):
        """定向优先:context.target 的 GUID 覆盖 legacy target。"""
        calls: list[dict[str, Any]] = []
        channel = _channel(calls, monkeypatch=monkeypatch, target="env:BLUEBUBBLES_CHAT")
        monkeypatch.setenv("BLUEBUBBLES_CHAT", SMS_GUID)

        _run(channel.send([{"title": "t"}], replace(CONTEXT, target=_target(GROUP_GUID))))

        assert [call["path"] for call in calls] == ["/api/v1/message/text"]
        assert calls[0]["body"]["chatGuid"] == GROUP_GUID

    def test_long_message_splits_per_chunk(self, monkeypatch):
        """超 :data:`MESSAGE_LIMIT`(4000)自动分段,逐块独立 ``message/text``。"""
        calls: list[dict[str, Any]] = []
        channel = _channel(calls, monkeypatch=monkeypatch)
        long_title = "长" * (MESSAGE_LIMIT + 500)

        _run(channel.send([{"title": long_title}], replace(CONTEXT, target=_target(DM_GUID))))

        assert len(calls) >= 2
        messages = [call["body"]["message"] for call in calls]
        assert all(len(text) <= MESSAGE_LIMIT for text in messages)
        assert "".join(messages).count("长") == MESSAGE_LIMIT + 500
        # 各块独立 tempGuid(蓝本 _temp_guid 同构)。
        assert len({call["body"]["tempGuid"] for call in calls}) == len(calls)


# ---------------------------------------------------------------------------
# 新会话(chat/new)与 chat 级丢失
# ---------------------------------------------------------------------------


class TestNewChatAndNotFound:
    def test_email_address_opens_new_chat(self, monkeypatch):
        """邮箱地址(legacy target 解析产物)→ ``chat/new`` 直开新会话(蓝本
        ``_create_chat_for_handle``;首块即 chat/new 正文)。"""
        calls: list[dict[str, Any]] = []
        channel = _channel(calls, monkeypatch=monkeypatch, target="env:BLUEBUBBLES_CHAT")
        monkeypatch.setenv("BLUEBUBBLES_CHAT", EMAIL)

        _run(channel.send([{"title": "t"}], CONTEXT))

        assert [call["path"] for call in calls] == ["/api/v1/chat/query", "/api/v1/chat/new"]
        assert calls[1]["body"]["addresses"] == [EMAIL]
        assert "message" in calls[1]["body"] and calls[1]["body"]["tempGuid"].startswith("temp-")

    def test_new_chat_multi_part_resolves_guid_for_rest(self, monkeypatch):
        """新会话多块:首块 chat/new,余块重解析 GUID 后走常规路(MYIA 补齐,蓝本只发首块)。"""
        calls: list[dict[str, Any]] = []
        long_title = "长" * (MESSAGE_LIMIT + 500)
        # 首次 query 空(触发 new),chat/new 后第二次 query 命中。
        state = {"queried": 0}

        def handler(request: httpx.Request) -> httpx.Response:
            calls.append(_capture(request))
            path = request.url.path
            if path == "/api/v1/chat/query":
                state["queried"] += 1
                data = _query_hit(EMAIL, DM_GUID) if state["queried"] >= 2 else []
                return httpx.Response(200, json={"status": 200, "data": data})
            if path == "/api/v1/chat/new":
                return httpx.Response(200, json={"status": 200, "data": {"guid": "new-chat"}})
            return httpx.Response(200, json={"status": 200, "data": {"guid": "MSG-1"}})

        channel = _channel(
            calls,
            monkeypatch=monkeypatch,
            target="env:BLUEBUBBLES_CHAT",
            client=httpx.AsyncClient(transport=httpx.MockTransport(handler)),
        )
        monkeypatch.setenv("BLUEBUBBLES_CHAT", EMAIL)

        _run(channel.send([{"title": long_title}], CONTEXT))

        # 序列:首查(空)→ chat/new 首块 → 重查(命中)→ 余块逐发 message/text。
        assert [call["path"] for call in calls][:3] == [
            "/api/v1/chat/query",
            "/api/v1/chat/new",
            "/api/v1/chat/query",
        ]
        rest = calls[3:]
        assert rest and {call["path"] for call in rest} == {"/api/v1/message/text"}
        assert all(call["body"]["chatGuid"] == DM_GUID for call in rest)

    def test_chat_not_found_is_chat_level_dead_letter(self, monkeypatch):
        """非地址形且解析不到 → chat 级 ``chat not found`` 锚 → 死信 not_found(会话确认不可达)。"""
        calls: list[dict[str, Any]] = []
        channel = _channel(calls, monkeypatch=monkeypatch)

        with pytest.raises(PushSendError) as excinfo:
            _run(channel.send([{"title": "t"}], replace(CONTEXT, target=_target("unknown-handle"))))
        assert excinfo.value.code == "bluebubbles_api_error"
        assert "chat not found" in str(excinfo.value)
        assert classify_dead_error(excinfo.value) == "not_found"


# ---------------------------------------------------------------------------
# 错误语义:结构化 code + 瞬态/配置级如实分类
# ---------------------------------------------------------------------------


class TestErrorSemantics:
    def test_transport_unreachable_is_transient(self, monkeypatch):
        """服务端不可达 → ``http_error``(瞬态,不标死信)。"""
        def handler(request: httpx.Request) -> httpx.Response:
            raise httpx.ConnectError("connection refused")

        channel = _channel(
            [],
            monkeypatch=monkeypatch,
            client=httpx.AsyncClient(transport=httpx.MockTransport(handler)),
        )

        with pytest.raises(PushSendError) as excinfo:
            _run(channel.send([{"title": "t"}], replace(CONTEXT, target=_target(DM_GUID))))
        assert excinfo.value.code == "http_error"
        assert "BlueBubbles" in str(excinfo.value)
        assert classify_dead_error(excinfo.value) is None

    def test_auth_failure_hint_and_password_never_leaks(self, monkeypatch):
        """401 鉴权失败(配置级根因)→ 文案明示核对 BLUEBUBBLES_PASSWORD;password 永不进文案。"""
        calls: list[dict[str, Any]] = []
        channel = _channel(
            calls,
            monkeypatch=monkeypatch,
            client=httpx.AsyncClient(
                transport=_router(calls, message_status=401, message_text="Unauthorized")
            ),
        )

        with pytest.raises(PushSendError) as excinfo:
            _run(channel.send([{"title": "t"}], replace(CONTEXT, target=_target(DM_GUID))))
        assert excinfo.value.code == "bluebubbles_api_error"
        assert "鉴权失败" in str(excinfo.value)
        assert "BLUEBUBBLES_PASSWORD" in str(excinfo.value)
        assert PASSWORD not in str(excinfo.value)
        assert classify_dead_error(excinfo.value) is None

    def test_http_500_is_transient(self, monkeypatch):
        calls: list[dict[str, Any]] = []
        channel = _channel(
            calls,
            monkeypatch=monkeypatch,
            client=httpx.AsyncClient(
                transport=_router(calls, message_status=500, message_text="boom")
            ),
        )

        with pytest.raises(PushSendError) as excinfo:
            _run(channel.send([{"title": "t"}], replace(CONTEXT, target=_target(DM_GUID))))
        assert excinfo.value.code == "bluebubbles_api_error"
        assert "HTTP 状态 500" in str(excinfo.value)
        assert classify_dead_error(excinfo.value) is None

    def test_non_json_response_invalid(self, monkeypatch):
        def handler(request: httpx.Request) -> httpx.Response:
            return httpx.Response(200, text="<html>not json</html>")

        channel = _channel(
            [],
            monkeypatch=monkeypatch,
            client=httpx.AsyncClient(transport=httpx.MockTransport(handler)),
        )

        with pytest.raises(PushSendError) as excinfo:
            _run(channel.send([{"title": "t"}], replace(CONTEXT, target=_target(DM_GUID))))
        assert excinfo.value.code == "invalid_response"

    def test_missing_target_is_config_error(self, monkeypatch):
        """两路寻址全缺 → ``missing_target``(配置类码,不标死信)。"""
        channel = _channel([], monkeypatch=monkeypatch)

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
        channel = _channel([], env=False, target="env:BLUEBUBBLES_CHAT")

        with pytest.raises(PushSendError) as excinfo:
            _run(channel.send([{"title": "t"}], CONTEXT))
        assert excinfo.value.code == "env_var_missing"
        assert "设置→推送" in str(excinfo.value)
        assert "BLUEBUBBLES_SERVER_URL" in str(excinfo.value)

    def test_keychain_fallback_drives_real_send(self, monkeypatch):
        """GUI 桌面路径:三凭据全走钥匙链规范名 ``myia/push/<ENV_KEY>`` 照发不误。"""
        calls: list[dict[str, Any]] = []
        channel = _channel(calls, env=False, target="env:BLUEBUBBLES_CHAT")
        secrets_store.set_secret("myia/push/BLUEBUBBLES_SERVER_URL", SERVER)
        secrets_store.set_secret("myia/push/BLUEBUBBLES_PASSWORD", PASSWORD)
        secrets_store.set_secret("myia/push/BLUEBUBBLES_CHAT", DM_GUID)

        _run(channel.send([{"title": "t"}], CONTEXT))

        assert [call["path"] for call in calls] == ["/api/v1/message/text"]
        assert calls[0]["query"].get("password") == [PASSWORD]

    def test_server_url_normalization(self, monkeypatch):
        """无 scheme 地址自动补 ``http://``(蓝本 ``_normalize_server_url`` 移植)。"""
        assert normalize_server_url("bluebubbles.local:1234/") == "http://bluebubbles.local:1234"
        assert normalize_server_url("https://bb.example.com/") == "https://bb.example.com"

        calls: list[dict[str, Any]] = []
        channel = _channel(calls, env=False, target="env:BLUEBUBBLES_CHAT")
        secrets_store.set_secret("myia/push/BLUEBUBBLES_SERVER_URL", "bluebubbles.local:1234")
        secrets_store.set_secret("myia/push/BLUEBUBBLES_PASSWORD", PASSWORD)
        monkeypatch.setenv("BLUEBUBBLES_CHAT", DM_GUID)

        _run(channel.send([{"title": "t"}], CONTEXT))

        # 请求确实打向规范化后的地址(MockTransport 按 path 分发,URL host 侧
        # 由 httpx 客户端解析;此处钉 path 与查询串已足)。
        assert calls[0]["path"] == "/api/v1/message/text"


# ---------------------------------------------------------------------------
# 寻址面(壳期已接线,出壳后语义不变)
# ---------------------------------------------------------------------------


class TestAddressing:
    def test_direct_ref_parse(self):
        """chat GUID(iMessage;/SMS; sigil)与 ``+`` 手机号直达;邮箱/显示名回落目录。"""
        for ref in [DM_GUID, GROUP_GUID, SMS_GUID, "+15551234567"]:
            target = BlueBubblesChannel.parse_direct_ref(ref)
            assert target is not None
            assert (target.platform, target.chat_id, target.resolved_from) == (
                "bluebubbles",
                ref,
                RESOLVED_DIRECT,
            )
        for ref in ["iMessage", "alice@icloud.com", "15551234567", "imessage;-;+1555", "", "羊毛群"]:
            assert BlueBubblesChannel.parse_direct_ref(ref) is None

    def test_resolve_direct_via_explicit_registry(self, tmp_path):
        target = resolve_target(
            f"bluebubbles:{GROUP_GUID}", ChannelDirectory(tmp_path), platforms=PLATFORMS
        )

        assert (target.chat_id, target.resolved_from) == (GROUP_GUID, RESOLVED_DIRECT)

    def test_resolve_via_directory_name(self, tmp_path):
        directory = ChannelDirectory(tmp_path)
        directory.replace_platform(
            "bluebubbles",
            [ChannelEntry(platform="bluebubbles", chat_id=GROUP_GUID, name="家人群", type="group")],
        )

        target = resolve_target("bluebubbles:家人群", directory, platforms=PLATFORMS)
        assert (target.chat_id, target.resolved_from) == (GROUP_GUID, RESOLVED_DIRECTORY_NAME)


# ---------------------------------------------------------------------------
# 目录语义(无自动发现,不是失败)+ 协议面
# ---------------------------------------------------------------------------


class TestDirectorySemantics:
    def test_discover_directory_raises_unsupported(self):
        with pytest.raises(DirectoryDiscoverUnsupported) as excinfo:
            _run(BlueBubblesChannel().discover_directory())
        assert "无自动发现" in str(excinfo.value)

    def test_directory_refresh_skips_unsupported_quietly(self, tmp_path):
        directory = ChannelDirectory(tmp_path)
        directory.merge_entries("bluebubbles", [], now=1.0)

        counts = _run(directory.refresh({"bluebubbles": BlueBubblesChannel()}, now=100.0))

        assert counts == {}


class TestProtocolSurface:
    def test_channel_protocol_surface(self):
        """Channel 协议面:name/supports_targeting/TrendAwareChannel 基类。"""
        channel = BlueBubblesChannel()
        assert channel.name == "bluebubbles"
        assert channel.supports_targeting is True
        assert isinstance(channel, TrendAwareChannel)
        assert isinstance(channel, Channel)

    def test_registered_in_channel_registry(self):
        """集成注册面:CHANNELS/PLATFORMS 均登记本通道(壳期已注册,出壳零变化)。"""
        from myssia.push import CHANNELS, PLATFORMS

        assert CHANNELS["bluebubbles"] is BlueBubblesChannel
        assert PLATFORMS["bluebubbles"] is BlueBubblesChannel
