"""Tests for 10-03-messaging-w3-longtail 组一 — discord 适配器。

覆盖:REST 形态(Bot 头 + /channels/{id}/messages + content)、2000 硬拆、
thread_id 话题改投、定向/legacy 两路寻址与雪花 id 直达、错误分类(403 →
forbidden、404 Unknown Channel → not_found、429/5xx → 瞬态)、目录发现
(R4:guild 两跳 REST 翻页聚合/429 退避/type 过滤/空结果/目录合并)。

蓝本对照:Hermes ``plugins/platforms/discord/adapter.py`` 的
``_standalone_send``(NousResearch/Hermes-Agent,MIT)——此处测 MYIA 重写;
目录发现蓝本 = Hermes ``gateway/channel_directory.py`` ``_build_discord``
(上游 174-197 行,MIT)。

No pytest-asyncio in dev deps: async calls run through ``asyncio.run``.
All network I/O goes through ``httpx.MockTransport``.
"""

from __future__ import annotations

import asyncio
import json
from dataclasses import replace
from typing import Any

import httpx
import pytest

from myssia.push.base import PushSendError, SendContext
from myssia.push.delivery import classify_dead_error
from myssia.push.directory import ChannelDirectory
from myssia.push.discord import MESSAGE_LIMIT, DiscordChannel
from myssia.push.targets import (
    RESOLVED_DIRECT,
    RESOLVED_DIRECTORY_NAME,
    ChannelTarget,
    resolve_target,
)

CONTEXT = SendContext(slot="am", date="2026-10-03", category="羊毛", kind="digest")
CHANNEL_ID = "123456789012345678"
PLATFORMS = {"discord": DiscordChannel}


def _capture(request: httpx.Request) -> dict:
    return {
        "url": str(request.url),
        "headers": dict(request.headers),
        "body": json.loads(request.content.decode("utf-8")),
    }


def _mock(calls: list[dict], response: httpx.Response | None = None) -> httpx.MockTransport:
    def handler(request: httpx.Request) -> httpx.Response:
        calls.append(_capture(request))
        return response or httpx.Response(200, json={"id": "998877", "content": "x"})

    return httpx.MockTransport(handler)


def _channel(calls: list[dict], *, response: httpx.Response | None = None, **kwargs: Any) -> DiscordChannel:
    kwargs.setdefault("target", "env:MYIA_TEST_DISCORD_CHANNEL")
    client = kwargs.pop("client", None) or httpx.AsyncClient(transport=_mock(calls, response=response))
    return DiscordChannel(client=client, **kwargs)


def _run(coro: Any) -> Any:
    return asyncio.run(coro)


def _target(chat_id: str, thread_id: str | None = None) -> ChannelTarget:
    return ChannelTarget(
        platform="discord", chat_id=chat_id, thread_id=thread_id, resolved_from=RESOLVED_DIRECT
    )


@pytest.fixture()
def channel_env(monkeypatch):
    monkeypatch.setenv("MYIA_TEST_DISCORD_CHANNEL", CHANNEL_ID)
    monkeypatch.setenv("DISCORD_BOT_TOKEN", "MTIz-bot-token")


# ---------------------------------------------------------------------------
# REST 形态 + 2000 硬拆
# ---------------------------------------------------------------------------


class TestPostShape:
    def test_post_message_shape(self, channel_env):
        calls: list[dict] = []
        channel = _channel(calls, token="MTIz-direct-token")

        _run(channel.send([{"title": "羊毛", "url": "https://x/1"}], CONTEXT))

        assert calls[0]["url"] == f"https://discord.com/api/v10/channels/{CHANNEL_ID}/messages"
        assert calls[0]["headers"]["authorization"] == "Bot MTIz-direct-token"
        assert "羊毛" in calls[0]["body"]["content"] and "https://x/1" in calls[0]["body"]["content"]

    def test_long_content_hard_splits_at_2000(self, channel_env):
        calls: list[dict] = []
        channel = _channel(calls, token="MTIz-t")

        _run(channel.send([{"title": "长" * 1500}, {"title": "另" * 1500}], CONTEXT))

        assert len(calls) == 2
        assert all(len(call["body"]["content"]) <= MESSAGE_LIMIT for call in calls)

    def test_response_without_id_is_invalid(self, channel_env):
        calls: list[dict] = []
        channel = _channel(calls, response=httpx.Response(200, json={"content": "no id"}))

        with pytest.raises(PushSendError) as excinfo:
            _run(channel.send([{"title": "t"}], CONTEXT))
        assert excinfo.value.code == "invalid_response"

    def test_default_token_ref_resolved_at_send_time(self, channel_env):
        calls: list[dict] = []
        channel = _channel(calls)

        _run(channel.send([{"title": "t"}], CONTEXT))

        assert calls[0]["headers"]["authorization"] == "Bot MTIz-bot-token"

    def test_missing_token_env_is_env_var_missing(self, channel_env, monkeypatch):
        monkeypatch.delenv("DISCORD_BOT_TOKEN", raising=False)
        calls: list[dict] = []
        channel = _channel(calls)

        with pytest.raises(PushSendError) as excinfo:
            _run(channel.send([{"title": "t"}], CONTEXT))
        assert excinfo.value.code == "env_var_missing"
        assert calls == []


# ---------------------------------------------------------------------------
# 寻址:定向优先 / thread 话题 / 直达 + 目录
# ---------------------------------------------------------------------------


class TestAddressing:
    def test_context_target_overrides_legacy(self, channel_env):
        calls: list[dict] = []
        channel = _channel(calls, token="MTIz-t")

        _run(channel.send([{"title": "t"}], replace(CONTEXT, target=_target("987654321098765432"))))

        assert calls[0]["url"].endswith("/channels/987654321098765432/messages")

    def test_thread_id_reroutes_to_thread_endpoint(self, channel_env):
        """thread_id 在场 → 改投话题端点(蓝本 thread_id 分支同形态)。"""
        calls: list[dict] = []
        channel = _channel(calls, token="MTIz-t")

        _run(
            channel.send(
                [{"title": "t"}],
                replace(CONTEXT, target=_target(CHANNEL_ID, thread_id="111222333444555666")),
            )
        )

        assert calls[0]["url"].endswith("/channels/111222333444555666/messages")

    def test_no_target_and_no_context_target_fails_fast(self, monkeypatch):
        monkeypatch.delenv("MYIA_TEST_DISCORD_CHANNEL", raising=False)
        calls: list[dict] = []
        channel = DiscordChannel(client=httpx.AsyncClient(transport=_mock(calls)), token="t")

        with pytest.raises(PushSendError) as excinfo:
            _run(channel.send([{"title": "t"}], CONTEXT))
        assert excinfo.value.code == "missing_target"
        assert calls == []

    def test_malformed_channel_id_rejected(self, channel_env):
        calls: list[dict] = []
        channel = _channel(calls, token="t")

        with pytest.raises(PushSendError) as excinfo:
            _run(channel.send([{"title": "t"}], replace(CONTEXT, target=_target("general"))))
        assert excinfo.value.code == "invalid_credential_ref"
        assert calls == []

    def test_direct_ref_parse(self):
        for ref in ["123456789012345678", "998877665544332211"]:
            target = DiscordChannel.parse_direct_ref(ref)
            assert target is not None
            assert (target.platform, target.chat_id, target.resolved_from) == (
                "discord",
                ref,
                RESOLVED_DIRECT,
            )
        for ref in ["羊毛频道", "123", "123456789012345678901", "c0123"]:
            assert DiscordChannel.parse_direct_ref(ref) is None

    def test_resolve_direct_bypasses_directory(self, tmp_path):
        target = resolve_target(
            "discord:123456789012345678", ChannelDirectory(tmp_path), platforms=PLATFORMS
        )
        assert (target.platform, target.chat_id) == ("discord", "123456789012345678")

    def test_resolve_via_directory_name(self, tmp_path):
        from myssia.push.directory import ChannelEntry

        directory = ChannelDirectory(tmp_path)
        directory.merge_entries(
            "discord",
            [ChannelEntry(platform="discord", chat_id="123456789012345678", name="羊毛频道")],
            now=1.0,
        )
        by_name = resolve_target("discord:羊毛频道", directory, platforms=PLATFORMS)
        assert (by_name.chat_id, by_name.resolved_from) == (
            "123456789012345678",
            RESOLVED_DIRECTORY_NAME,
        )

    def test_template_render(self, channel_env):
        calls: list[dict] = []
        channel = _channel(calls, token="t", template="{{ date }} 共 {{ items|length }} 条")

        _run(channel.send([{"title": "t"}], CONTEXT))

        assert calls[0]["body"]["content"] == "2026-10-03 共 1 条"

    def test_template_render_failure_is_structured(self, channel_env):
        calls: list[dict] = []
        channel = _channel(calls, token="t", template="{{ no_such_helper() }}")

        with pytest.raises(PushSendError) as excinfo:
            _run(channel.send([{"title": "t"}], CONTEXT))
        assert excinfo.value.code == "template_render_error"


# ---------------------------------------------------------------------------
# 错误分类(401/403 → forbidden、404 → not_found、429/5xx → 瞬态)
# ---------------------------------------------------------------------------


class TestErrorClassification:
    def test_403_classifies_forbidden(self, channel_env):
        calls: list[dict] = []
        channel = _channel(
            calls, response=httpx.Response(403, json={"message": "Missing Permissions", "code": 50013})
        )

        with pytest.raises(PushSendError) as excinfo:
            _run(channel.send([{"title": "t"}], CONTEXT))
        assert "HTTP 403" in str(excinfo.value)
        assert classify_dead_error(excinfo.value) == "forbidden"

    def test_404_unknown_channel_classifies_not_found(self, channel_env):
        calls: list[dict] = []
        channel = _channel(
            calls, response=httpx.Response(404, json={"message": "Unknown Channel", "code": 10003})
        )

        with pytest.raises(PushSendError) as excinfo:
            _run(channel.send([{"title": "t"}], CONTEXT))
        assert "Unknown Channel" in str(excinfo.value)
        assert classify_dead_error(excinfo.value) == "not_found"

    @pytest.mark.parametrize("status", [429, 500, 503])
    def test_transient_statuses_do_not_mark_dead(self, channel_env, status):
        calls: list[dict] = []
        channel = _channel(calls, response=httpx.Response(status, text="busy"))

        with pytest.raises(PushSendError) as excinfo:
            _run(channel.send([{"title": "t"}], CONTEXT))
        assert classify_dead_error(excinfo.value) is None

    def test_transport_error_reports_http_error(self, channel_env):
        def handler(request: httpx.Request) -> httpx.Response:
            raise httpx.ConnectError("connection refused")

        channel = DiscordChannel(
            target="env:MYIA_TEST_DISCORD_CHANNEL",
            token="t",
            client=httpx.AsyncClient(transport=httpx.MockTransport(handler)),
        )

        with pytest.raises(PushSendError) as excinfo:
            _run(channel.send([{"title": "t"}], CONTEXT))
        assert excinfo.value.code == "http_error"
        assert classify_dead_error(excinfo.value) is None


# ---------------------------------------------------------------------------
# 目录发现(R4:guild 两跳 REST,蓝本 channel_directory.py:174-197 移植)
# ---------------------------------------------------------------------------


def _guild(gid: str, name: str = "服务器") -> dict[str, Any]:
    return {"id": gid, "name": name}


def _chan(cid: str, ctype: int, name: str | None = "频道") -> dict[str, Any]:
    raw: dict[str, Any] = {"id": cid, "type": ctype}
    if name is not None:
        raw["name"] = name
    return raw


def _discovery_channel(handler) -> DiscordChannel:
    client = httpx.AsyncClient(transport=httpx.MockTransport(handler))
    return DiscordChannel(token="MTIz-t", client=client)


class TestDirectoryDiscovery:
    def test_request_contract_and_single_page(self):
        """guild 两跳形态:Bot 头 + limit=200 + 每服务器频道列表路径。"""
        requests: list[httpx.Request] = []

        def handler(request: httpx.Request) -> httpx.Response:
            requests.append(request)
            if request.url.path == "/api/v10/users/@me/guilds":
                return httpx.Response(200, json=[_guild("100000000000000001", "羊毛服")])
            return httpx.Response(200, json=[_chan("123456789012345678", 0, "线报台")])

        channel = _discovery_channel(handler)
        entries = _run(channel.discover_directory())
        _run(channel._client.aclose())

        assert [(e.platform, e.chat_id, e.name, e.type) for e in entries] == [
            ("discord", "123456789012345678", "线报台", "channel")
        ]
        assert [str(r.url.path) for r in requests] == [
            "/api/v10/users/@me/guilds",
            "/api/v10/guilds/100000000000000001/channels",
        ]
        assert requests[0].url.params["limit"] == "200"
        assert "after" not in requests[0].url.params
        assert requests[0].headers["Authorization"] == "Bot MTIz-t"

    def test_guild_pagination_threads_after_cursor(self, monkeypatch):
        """翻页契约:整页 → after=尾 guild id 续拉;不足一页即止;跨页聚合。"""
        monkeypatch.setattr("myssia.push.discord.DISCOVER_PAGE_SIZE", 2)
        requests: list[httpx.Request] = []
        page_one = [_guild("100000000000000001"), _guild("100000000000000002")]
        page_two = [_guild("100000000000000003")]

        def handler(request: httpx.Request) -> httpx.Response:
            requests.append(request)
            if request.url.path == "/api/v10/users/@me/guilds":
                if "after" in request.url.params:
                    assert request.url.params["after"] == "100000000000000002"
                    return httpx.Response(200, json=page_two)
                return httpx.Response(200, json=page_one)
            gid = request.url.path.split("/")[-2]
            return httpx.Response(
                200, json=[_chan(f"55500000000000000{gid[-1]}", 0, f"频道{gid[-1]}")]
            )

        channel = _discovery_channel(handler)
        entries = _run(channel.discover_directory())
        _run(channel._client.aclose())

        assert [e.chat_id for e in entries] == [
            "555000000000000001",
            "555000000000000002",
            "555000000000000003",
        ]
        guild_pages = [r for r in requests if r.url.path == "/api/v10/users/@me/guilds"]
        assert len(guild_pages) == 2  # 尾页(1 < 2)即止,无第三拉

    def test_page_cap_20_when_cursor_never_converges(self, monkeypatch):
        """服务端整页永不收敛 → 保底 20 页止步(防死循环,蓝本护栏同款)。"""
        monkeypatch.setattr("myssia.push.discord.DISCOVER_PAGE_SIZE", 1)
        calls = {"guilds": 0, "channels": 0}

        def handler(request: httpx.Request) -> httpx.Response:
            if request.url.path == "/api/v10/users/@me/guilds":
                calls["guilds"] += 1
                return httpx.Response(200, json=[_guild(str(10**17 + calls["guilds"]))])
            calls["channels"] += 1
            return httpx.Response(
                200, json=[_chan(str(5 * 10**18 + calls["channels"]), 0, "频道")]
            )

        channel = _discovery_channel(handler)
        entries = _run(channel.discover_directory())
        _run(channel._client.aclose())

        assert calls["guilds"] == 20  # DISCOVER_MAX_PAGES 保底
        assert len(entries) == 20

    def test_channel_type_filter_and_entry_mapping(self):
        """仅 text(0)/forum(15) 进目录(蓝本枚举面);forum 落 type=topic;
        其余 type(语音/分类/公告)跳过;无名频道退 id 占位仍可寻址。"""

        def handler(request: httpx.Request) -> httpx.Response:
            if request.url.path == "/api/v10/users/@me/guilds":
                return httpx.Response(200, json=[_guild("100000000000000001")])
            return httpx.Response(
                200,
                json=[
                    _chan("111111111111111111", 0, "公告板"),
                    _chan("222222222222222222", 15, "论坛台"),
                    _chan("333333333333333333", 2, "语音房"),
                    _chan("444444444444444444", 4, "分类"),
                    _chan("555555555555555555", 5, "公告频道"),
                    _chan("666666666666666666", 0, None),
                ],
            )

        channel = _discovery_channel(handler)
        entries = _run(channel.discover_directory())
        _run(channel._client.aclose())

        assert [(e.chat_id, e.name, e.type) for e in entries] == [
            ("111111111111111111", "公告板", "channel"),
            ("222222222222222222", "论坛台", "topic"),
            ("666666666666666666", "666666666666666666", "channel"),
        ]

    def test_duplicate_channel_ids_deduped_across_guilds(self):
        """同频道 id 跨服务器只留一条(频道 id 全局唯一,防御重复枚举)。"""

        def handler(request: httpx.Request) -> httpx.Response:
            if request.url.path == "/api/v10/users/@me/guilds":
                return httpx.Response(
                    200, json=[_guild("100000000000000001"), _guild("100000000000000002")]
                )
            return httpx.Response(200, json=[_chan("777777777777777777", 0, "同名频道")])

        channel = _discovery_channel(handler)
        entries = _run(channel.discover_directory())
        _run(channel._client.aclose())

        assert [e.chat_id for e in entries] == ["777777777777777777"]

    def test_429_backoff_once_then_succeeds(self, monkeypatch):
        """429 退避一次再试:retry_after 优先(响应体官方字段),sleeper 注入免真睡。"""
        sleeps: list[float] = []

        async def fake_sleep(seconds: float) -> None:
            sleeps.append(seconds)

        monkeypatch.setattr(DiscordChannel, "discover_sleeper", fake_sleep)
        seen = {"guilds": 0}

        def handler(request: httpx.Request) -> httpx.Response:
            if request.url.path == "/api/v10/users/@me/guilds":
                seen["guilds"] += 1
                if seen["guilds"] == 1:
                    return httpx.Response(
                        429,
                        json={"message": "You are being rate limited.", "retry_after": 0.25},
                    )
                return httpx.Response(200, json=[_guild("100000000000000001")])
            return httpx.Response(200, json=[_chan("123456789012345678", 0, "限频后频道")])

        channel = _discovery_channel(handler)
        entries = _run(channel.discover_directory())
        _run(channel._client.aclose())

        assert sleeps == [0.25]  # retry_after 优先于类级兜底秒数
        assert [e.name for e in entries] == ["限频后频道"]

    def test_429_twice_raises_structured_error(self, monkeypatch):
        """二次 429 不再退避:按发现失败如实上抛(诚实失败,feishu D2 同款)。"""
        sleeps: list[float] = []

        async def fake_sleep(seconds: float) -> None:
            sleeps.append(seconds)

        monkeypatch.setattr(DiscordChannel, "discover_sleeper", fake_sleep)
        calls = {"guilds": 0, "channels": 0}

        def handler(request: httpx.Request) -> httpx.Response:
            if request.url.path == "/api/v10/users/@me/guilds":
                calls["guilds"] += 1
                return httpx.Response(429, json={"message": "You are being rate limited."})
            calls["channels"] += 1
            return httpx.Response(200, json=[])

        channel = _discovery_channel(handler)
        with pytest.raises(PushSendError) as excinfo:
            _run(channel.discover_directory())
        _run(channel._client.aclose())

        assert excinfo.value.code == "discord_api_error"
        assert calls == {"guilds": 2, "channels": 0}  # 退避一次,频道列表未发出
        assert len(sleeps) == 1

    def test_empty_guild_list_returns_empty_list(self):
        def handler(request: httpx.Request) -> httpx.Response:
            assert request.url.path == "/api/v10/users/@me/guilds"
            return httpx.Response(200, json=[])

        channel = _discovery_channel(handler)
        entries = _run(channel.discover_directory())
        _run(channel._client.aclose())
        assert entries == []

    def test_non_json_success_response_is_invalid_response(self):
        """2xx 但非 JSON → invalid_response(502 等非 2xx 先走 discord_api_error,
        与发送路径 _post_message 的判定顺序一致)。"""

        def handler(request: httpx.Request) -> httpx.Response:
            return httpx.Response(200, text="<html>not json</html>")

        channel = _discovery_channel(handler)
        with pytest.raises(PushSendError) as excinfo:
            _run(channel.discover_directory())
        _run(channel._client.aclose())
        assert excinfo.value.code == "invalid_response"

    def test_http_error_status_raises_api_error(self):
        def handler(request: httpx.Request) -> httpx.Response:
            return httpx.Response(502, text="<html>bad gateway</html>")

        channel = _discovery_channel(handler)
        with pytest.raises(PushSendError) as excinfo:
            _run(channel.discover_directory())
        _run(channel._client.aclose())
        assert excinfo.value.code == "discord_api_error"
        assert "HTTP 502" in str(excinfo.value)

    def test_missing_token_env_is_credential_error(self, monkeypatch):
        monkeypatch.delenv("DISCORD_BOT_TOKEN", raising=False)
        calls: list[dict] = []
        channel = DiscordChannel(client=httpx.AsyncClient(transport=_mock(calls)))

        with pytest.raises(PushSendError) as excinfo:
            _run(channel.discover_directory())
        _run(channel._client.aclose())

        assert excinfo.value.code == "env_var_missing"
        assert calls == []

    def test_discovery_merges_into_directory_refresh(self, tmp_path):
        """acceptance:发现结果经 directory.refresh 桶替换 + last_seen 盖戳 + 落盘。"""

        def handler(request: httpx.Request) -> httpx.Response:
            if request.url.path == "/api/v10/users/@me/guilds":
                return httpx.Response(200, json=[_guild("100000000000000001", "羊毛服")])
            return httpx.Response(
                200,
                json=[
                    _chan("123456789012345678", 0, "线报台"),
                    _chan("234567890123456789", 15, "论坛台"),
                ],
            )

        channel = _discovery_channel(handler)
        directory = ChannelDirectory(tmp_path)
        counts = _run(directory.refresh({"discord": channel}, now=100.0))
        _run(channel._client.aclose())

        assert counts == {"discord": 2}
        assert [(e.chat_id, e.type, e.last_seen) for e in directory.entries("discord")] == [
            ("123456789012345678", "channel", 100.0),
            ("234567890123456789", "topic", 100.0),
        ]
        saved = json.loads((tmp_path / "channel_directory.json").read_text(encoding="utf-8"))
        assert [e["chat_id"] for e in saved["platforms"]["discord"]] == [
            "123456789012345678",
            "234567890123456789",
        ]
