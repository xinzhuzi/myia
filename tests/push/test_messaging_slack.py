"""Tests for 10-03-messaging-w3-longtail 组一 — slack 适配器。

覆盖:chat.postMessage 形态(Bearer + JSON + ok 判据)、U/W 用户先
conversations.open 换 DM(蓝本 #17444)、39000 分段、定向/legacy 两路寻址
与直达解析、错误分类(HTTP 403 → forbidden、404 → not_found、429/5xx →
瞬态、ok=false 原厂 error 进文案)、目录发现(R4:users.conversations
翻页聚合/429 退避/补名/空结果/目录合并)。

蓝本对照:Hermes ``plugins/platforms/slack/adapter.py`` 的
``_standalone_send``/``_slack_json_post``/``_resolve_slack_user_dm``
(NousResearch/Hermes-Agent,MIT)——此处测 MYIA 重写;目录发现蓝本 =
Hermes ``gateway/channel_directory.py`` ``_slack_team_channels`` /
``_slack_resolve_raw_names``(上游 235-317 行,MIT)。

No pytest-asyncio in dev deps: async calls run through ``asyncio.run``
(同 test_push.py 约定)。All network I/O goes through ``httpx.MockTransport``.
"""

from __future__ import annotations

import asyncio
import json
from dataclasses import replace
from typing import Any

import httpx
import pytest

from myssia.push.base import PushSendError
from myssia.push.delivery import classify_dead_error
from myssia.push.directory import ChannelDirectory
from myssia.push.slack import MESSAGE_LIMIT, SlackChannel
from myssia.push.targets import (
    RESOLVED_DIRECT,
    RESOLVED_DIRECTORY_NAME,
    ChannelTarget,
    resolve_target,
)
from myssia.push.base import SendContext

CONTEXT = SendContext(slot="am", date="2026-10-03", category="羊毛", kind="digest")

PLATFORMS = {"slack": SlackChannel}  # 注册表钉死前的注入形态(集成后随 PLATFORMS)


def _capture(request: httpx.Request) -> dict:
    return {
        "url": str(request.url),
        "headers": dict(request.headers),
        "body": json.loads(request.content.decode("utf-8")),
    }


def _mock(calls: list[dict], response: httpx.Response | None = None) -> httpx.MockTransport:
    def handler(request: httpx.Request) -> httpx.Response:
        calls.append(_capture(request))
        return response or httpx.Response(200, json={"ok": True, "ts": "1234.5678"})

    return httpx.MockTransport(handler)


def _channel(calls: list[dict], *, response: httpx.Response | None = None, **kwargs: Any) -> SlackChannel:
    kwargs.setdefault("target", "env:MYIA_TEST_SLACK_CHANNEL")
    client = kwargs.pop("client", None) or httpx.AsyncClient(transport=_mock(calls, response=response))
    return SlackChannel(client=client, **kwargs)


def _run(coro: Any) -> Any:
    return asyncio.run(coro)


def _target(chat_id: str) -> ChannelTarget:
    return ChannelTarget(platform="slack", chat_id=chat_id, resolved_from=RESOLVED_DIRECT)


@pytest.fixture()
def channel_env(monkeypatch):
    monkeypatch.setenv("MYIA_TEST_SLACK_CHANNEL", "C0123ABCDEF")
    monkeypatch.setenv("SLACK_BOT_TOKEN", "xoxb-fixture-token")


# ---------------------------------------------------------------------------
# chat.postMessage 形态 + ok 判据
# ---------------------------------------------------------------------------


class TestPostShape:
    def test_post_message_shape(self, channel_env):
        calls: list[dict] = []
        channel = _channel(calls, token="xoxb-test-token")

        _run(channel.send([{"title": "羊毛", "url": "https://x/1"}], CONTEXT))

        assert calls[0]["url"] == "https://slack.com/api/chat.postMessage"
        assert calls[0]["headers"]["authorization"] == "Bearer xoxb-test-token"
        assert calls[0]["body"]["channel"] == "C0123ABCDEF"
        assert "羊毛" in calls[0]["body"]["text"] and "https://x/1" in calls[0]["body"]["text"]

    def test_ok_false_is_structured_api_error(self, channel_env):
        """Slack API 错误恒为 HTTP 200 + ok=false:原厂 error 进文案。"""
        calls: list[dict] = []
        channel = _channel(
            calls,
            response=httpx.Response(200, json={"ok": False, "error": "channel_not_found"}),
        )

        with pytest.raises(PushSendError) as excinfo:
            _run(channel.send([{"title": "t"}], CONTEXT))
        assert excinfo.value.code == "slack_api_error"
        assert "error=channel_not_found" in str(excinfo.value)

    def test_long_message_splits_at_limit(self, channel_env):
        calls: list[dict] = []
        channel = _channel(calls, token="xoxb-t")
        items = [
            {"title": "行" * 20000, "url": "https://x/1"},
            {"title": "另" * 20000},
        ]

        _run(channel.send(items, CONTEXT))

        assert len(calls) == 2
        assert all(len(call["body"]["text"]) <= MESSAGE_LIMIT for call in calls)

    def test_default_token_ref_resolved_at_send_time(self, channel_env, monkeypatch):
        """缺省 token 走 env:SLACK_BOT_TOKEN 引用(发送期才解析)。"""
        monkeypatch.setenv("SLACK_BOT_TOKEN", "xoxb-default-ref-token")
        calls: list[dict] = []
        channel = _channel(calls)

        _run(channel.send([{"title": "t"}], CONTEXT))

        assert calls[0]["headers"]["authorization"] == "Bearer xoxb-default-ref-token"

    def test_missing_token_env_is_env_var_missing(self, channel_env, monkeypatch):
        monkeypatch.delenv("SLACK_BOT_TOKEN", raising=False)
        calls: list[dict] = []
        channel = _channel(calls)

        with pytest.raises(PushSendError) as excinfo:
            _run(channel.send([{"title": "t"}], CONTEXT))
        assert excinfo.value.code == "env_var_missing"
        assert calls == []


# ---------------------------------------------------------------------------
# U/W 用户直达:conversations.open 先行(蓝本 #17444)
# ---------------------------------------------------------------------------


class TestUserDirectDM:
    def test_user_id_resolved_via_conversations_open(self, channel_env):
        """U/W 裸用户 id 不可直发:先 conversations.open 换 D… 再 postMessage。"""
        calls: list[dict] = []
        responses = [
            httpx.Response(200, json={"ok": True, "channel": {"id": "D0123DMID"}}),
            httpx.Response(200, json={"ok": True, "ts": "1.2"}),
        ]

        def handler(request: httpx.Request) -> httpx.Response:
            calls.append(_capture(request))
            return responses[len(calls) - 1]

        channel = SlackChannel(
            target="env:MYIA_TEST_SLACK_CHANNEL",
            token="xoxb-t",
            client=httpx.AsyncClient(transport=httpx.MockTransport(handler)),
        )

        _run(channel.send([{"title": "t"}], replace(CONTEXT, target=_target("U0456USERID"))))

        assert calls[0]["url"] == "https://slack.com/api/conversations.open"
        assert calls[0]["body"] == {"users": "U0456USERID"}
        assert calls[1]["url"] == "https://slack.com/api/chat.postMessage"
        assert calls[1]["body"]["channel"] == "D0123DMID"

    def test_conversations_open_failure_surfaces_vendor_error(self, channel_env):
        calls: list[dict] = []
        channel = _channel(
            calls,
            response=httpx.Response(200, json={"ok": False, "error": "user_not_found"}),
        )

        with pytest.raises(PushSendError) as excinfo:
            _run(channel.send([{"title": "t"}], replace(CONTEXT, target=_target("U0456USERID"))))
        assert excinfo.value.code == "slack_api_error"
        assert "error=user_not_found" in str(excinfo.value)
        assert len(calls) == 1  # postMessage 未发出


# ---------------------------------------------------------------------------
# 寻址:定向(context.target)优先 / legacy 兜底 / 直达与目录
# ---------------------------------------------------------------------------


class TestAddressing:
    def test_context_target_overrides_legacy(self, channel_env):
        calls: list[dict] = []
        channel = _channel(calls, token="xoxb-t")

        _run(channel.send([{"title": "t"}], replace(CONTEXT, target=_target("G089GROUP1"))))

        assert calls[0]["body"]["channel"] == "G089GROUP1"

    def test_no_target_and_no_context_target_fails_fast(self, monkeypatch):
        monkeypatch.delenv("MYIA_TEST_SLACK_CHANNEL", raising=False)
        calls: list[dict] = []
        channel = SlackChannel(client=httpx.AsyncClient(transport=_mock(calls)), token="xoxb-t")

        with pytest.raises(PushSendError) as excinfo:
            _run(channel.send([{"title": "t"}], CONTEXT))
        assert excinfo.value.code == "missing_target"
        assert calls == []

    def test_malformed_channel_id_rejected(self, channel_env, monkeypatch):
        """畸形 chat_id(目录别名登记错/引用配置笔误)→ invalid_credential_ref。

        与 discord/line/mattermost 同位置同款:形态校验先于任何 API 调用,
        绝不原样打到 Slack API——那会以 200+ok=false channel_not_found 回来,
        被死信分类按瞬态每轮重试(复核 D1)。两条寻址路(context.target /
        legacy target 引用)都过同一校验。
        """
        calls: list[dict] = []
        channel = _channel(calls, token="xoxb-t")

        # 定向路:别名名当 id 用(非 C/G/D/U/W 形态)
        with pytest.raises(PushSendError) as excinfo:
            _run(channel.send([{"title": "t"}], replace(CONTEXT, target=_target("羊毛群"))))
        assert excinfo.value.code == "invalid_credential_ref"
        assert "形态非法" in str(excinfo.value)

        # legacy 引用路:env 解析值非 id 形态(值不回显,只有长度与形态描述)
        monkeypatch.setenv("MYIA_TEST_SLACK_CHANNEL", "#general")
        with pytest.raises(PushSendError) as excinfo:
            _run(channel.send([{"title": "t"}], CONTEXT))
        assert excinfo.value.code == "invalid_credential_ref"
        assert calls == []

    def test_direct_ref_parse(self):
        for ref in ["C0123ABCDEF", "G0123456AB", "D0123456AB", "U0456USERID", "W0123ENTUSER"]:
            target = SlackChannel.parse_direct_ref(ref)
            assert target is not None
            assert (target.platform, target.chat_id, target.resolved_from) == (
                "slack",
                ref,
                RESOLVED_DIRECT,
            )
        for ref in ["羊毛群", "c0123abcdef", "#general", "", "X0123ABCDEF"]:
            assert SlackChannel.parse_direct_ref(ref) is None

    def test_resolve_direct_bypasses_directory(self, tmp_path):
        target = resolve_target("slack:C0123ABCDEF", ChannelDirectory(tmp_path), platforms=PLATFORMS)

        assert (target.platform, target.chat_id) == ("slack", "C0123ABCDEF")
        assert target.resolved_from == RESOLVED_DIRECT

    def test_resolve_via_alias_name_and_prefix(self, tmp_path):
        """目录精确名 + 唯一前缀两路径(注入注册表;集成后随 PLATFORMS)。"""
        from myssia.push.directory import ChannelEntry

        directory = ChannelDirectory(tmp_path)
        directory.merge_entries(
            "slack",
            [
                ChannelEntry(platform="slack", chat_id="C0AAA999999", name="羊毛群"),
                ChannelEntry(platform="slack", chat_id="C0BBB888888", name="节点群"),
            ],
            now=1.0,
        )
        by_name = resolve_target("slack:羊毛群", directory, platforms=PLATFORMS)
        assert (by_name.chat_id, by_name.resolved_from) == ("C0AAA999999", RESOLVED_DIRECTORY_NAME)
        by_prefix = resolve_target("slack:节点", directory, platforms=PLATFORMS)
        assert by_prefix.chat_id == "C0BBB888888"

    def test_template_render(self, channel_env):
        calls: list[dict] = []
        channel = _channel(calls, token="xoxb-t", template="{{ date }} 共 {{ items|length }} 条")

        _run(channel.send([{"title": "t"}], CONTEXT))

        assert calls[0]["body"]["text"] == "2026-10-03 共 1 条"

    def test_template_render_failure_is_structured(self, channel_env):
        calls: list[dict] = []
        channel = _channel(calls, token="xoxb-t", template="{{ no_such_helper() }}")

        with pytest.raises(PushSendError) as excinfo:
            _run(channel.send([{"title": "t"}], CONTEXT))
        assert excinfo.value.code == "template_render_error"


# ---------------------------------------------------------------------------
# 错误分类(prd:HTTP 403/404 硬失败,429/5xx/超时瞬态;ok=false 原样透传)
# ---------------------------------------------------------------------------


class TestErrorClassification:
    def test_403_classifies_forbidden(self, channel_env):
        calls: list[dict] = []
        channel = _channel(calls, response=httpx.Response(403, text=" Forbidden"))

        with pytest.raises(PushSendError) as excinfo:
            _run(channel.send([{"title": "t"}], CONTEXT))
        # 非 JSON 的 403 body:HTTP 状态先于 JSON 解析 → slack_api_error(非
        # invalid_response),死信分类照常命中 forbidden。
        assert excinfo.value.code == "slack_api_error"
        assert "HTTP 403" in str(excinfo.value)
        assert classify_dead_error(excinfo.value) == "forbidden"

    def test_429_classifies_transient(self, channel_env):
        calls: list[dict] = []
        channel = _channel(calls, response=httpx.Response(429, text="Too many requests"))

        with pytest.raises(PushSendError) as excinfo:
            _run(channel.send([{"title": "t"}], CONTEXT))
        assert classify_dead_error(excinfo.value) is None

    def test_ok_false_not_found_like_error_is_transient(self, channel_env):
        """ok=false + channel_not_found 无 HTTP 404:不判死信(诚实文案面)。

        Slack 的 chat 级不存在以 200+error 形态返回,死信分类器按 HTTP 状态
        命中;该错误如实透传、分类为瞬态(下轮重试)。
        """
        calls: list[dict] = []
        channel = _channel(
            calls, response=httpx.Response(200, json={"ok": False, "error": "channel_not_found"})
        )

        with pytest.raises(PushSendError) as excinfo:
            _run(channel.send([{"title": "t"}], CONTEXT))
        assert classify_dead_error(excinfo.value) is None

    def test_non_json_response_is_invalid_response(self, channel_env):
        calls: list[dict] = []
        channel = _channel(calls, response=httpx.Response(200, text="<html>not json</html>"))

        with pytest.raises(PushSendError) as excinfo:
            _run(channel.send([{"title": "t"}], CONTEXT))
        assert excinfo.value.code == "invalid_response"

    def test_transport_error_reports_http_error(self, channel_env):
        def handler(request: httpx.Request) -> httpx.Response:
            raise httpx.ConnectError("connection refused")

        channel = SlackChannel(
            target="env:MYIA_TEST_SLACK_CHANNEL",
            token="xoxb-t",
            client=httpx.AsyncClient(transport=httpx.MockTransport(handler)),
        )

        with pytest.raises(PushSendError) as excinfo:
            _run(channel.send([{"title": "t"}], CONTEXT))
        assert excinfo.value.code == "http_error"
        assert classify_dead_error(excinfo.value) is None


# ---------------------------------------------------------------------------
# 目录发现(R4:users.conversations 20×200 + info 补名,蓝本 235-317 移植)
# ---------------------------------------------------------------------------


def _convo(cid: str, name: str | None = "频道", **extra: Any) -> dict[str, Any]:
    raw: dict[str, Any] = {"id": cid}
    if name is not None:
        raw["name"] = name
    raw.update(extra)
    return raw


def _page(channels: list[dict[str, Any]], next_cursor: str | None = None) -> dict[str, Any]:
    body: dict[str, Any] = {"ok": True, "channels": channels}
    if next_cursor:
        body["response_metadata"] = {"next_cursor": next_cursor}
    return body


def _discovery_channel(handler) -> SlackChannel:
    client = httpx.AsyncClient(transport=httpx.MockTransport(handler))
    return SlackChannel(token="xoxb-t", client=client)


class TestDirectoryDiscovery:
    def test_request_contract_and_type_mapping(self):
        """users.conversations 契约:types/exclude_archived/limit=200 + Bearer;
        公开频道 type=channel、私有频道 type=group(仓内 ENTRY_TYPES 语汇)。"""
        requests: list[httpx.Request] = []

        def handler(request: httpx.Request) -> httpx.Response:
            requests.append(request)
            return httpx.Response(
                200,
                json=_page([_convo("C0AAA999999", "羊毛台"), _convo("G0BBB88888", "私人群", is_private=True)]),
            )

        channel = _discovery_channel(handler)
        entries = _run(channel.discover_directory())
        _run(channel._client.aclose())

        assert [(e.platform, e.chat_id, e.name, e.type) for e in entries] == [
            ("slack", "C0AAA999999", "羊毛台", "channel"),
            ("slack", "G0BBB88888", "私人群", "group"),
        ]
        assert len(requests) == 1  # 具名条目不触发补名
        assert str(requests[0].url.path) == "/api/users.conversations"
        assert requests[0].url.params["types"] == "public_channel,private_channel"
        assert requests[0].url.params["exclude_archived"] == "true"
        assert requests[0].url.params["limit"] == "200"
        assert "cursor" not in requests[0].url.params
        assert requests[0].headers["Authorization"] == "Bearer xoxb-t"

    def test_pagination_aggregates_and_threads_cursor(self):
        requests: list[httpx.Request] = []

        def handler(request: httpx.Request) -> httpx.Response:
            requests.append(request)
            if "cursor" not in request.url.params:
                return httpx.Response(
                    200,
                    json=_page(
                        [_convo("C0AAA999999", "羊毛台"), _convo("C0BBB888888", "节点台")],
                        next_cursor="cur-2",
                    ),
                )
            assert request.url.params["cursor"] == "cur-2"
            return httpx.Response(200, json=_page([_convo("C0CCC777777", "信用卡台")]))

        channel = _discovery_channel(handler)
        entries = _run(channel.discover_directory())
        _run(channel._client.aclose())

        assert [e.chat_id for e in entries] == ["C0AAA999999", "C0BBB888888", "C0CCC777777"]
        assert len(requests) == 2  # 无 next_cursor 即止,无第三拉

    def test_page_cap_20_when_cursor_never_converges(self):
        """服务端游标永不收敛 → 保底 20 页止步(蓝本 range(20) 护栏同款)。"""
        calls = {"count": 0}

        def handler(request: httpx.Request) -> httpx.Response:
            calls["count"] += 1
            return httpx.Response(
                200, json=_page([_convo(f"C0CAP00{calls['count']:03d}", f"频道{calls['count']}")], next_cursor="more")
            )

        channel = _discovery_channel(handler)
        entries = _run(channel.discover_directory())
        _run(channel._client.aclose())

        assert calls["count"] == 20  # DISCOVER_MAX_PAGES 保底
        assert len(entries) == 20

    def test_429_backoff_once_then_succeeds(self, monkeypatch):
        """429 退避一次再试:Retry-After 头优先(Slack 限频官方字段),免真睡。"""
        sleeps: list[float] = []

        async def fake_sleep(seconds: float) -> None:
            sleeps.append(seconds)

        monkeypatch.setattr(SlackChannel, "discover_sleeper", fake_sleep)
        seen = {"count": 0}

        def handler(request: httpx.Request) -> httpx.Response:
            seen["count"] += 1
            if seen["count"] == 1:
                return httpx.Response(
                    429, headers={"Retry-After": "0.5"}, text="Too many requests"
                )
            return httpx.Response(200, json=_page([_convo("C0AAA999999", "限频后台")]))

        channel = _discovery_channel(handler)
        entries = _run(channel.discover_directory())
        _run(channel._client.aclose())

        assert sleeps == [0.5]  # Retry-After 头优先于类级兜底秒数
        assert [e.name for e in entries] == ["限频后台"]

    def test_429_twice_raises_structured_error(self, monkeypatch):
        """二次 429 不再退避:按发现失败如实上抛(诚实失败,feishu D2 同款)。"""
        sleeps: list[float] = []

        async def fake_sleep(seconds: float) -> None:
            sleeps.append(seconds)

        monkeypatch.setattr(SlackChannel, "discover_sleeper", fake_sleep)

        def handler(request: httpx.Request) -> httpx.Response:
            return httpx.Response(429, text="Too many requests")

        channel = _discovery_channel(handler)
        with pytest.raises(PushSendError) as excinfo:
            _run(channel.discover_directory())
        _run(channel._client.aclose())

        assert excinfo.value.code == "slack_api_error"
        assert "HTTP 429" in str(excinfo.value)
        assert len(sleeps) == 1

    def test_ok_false_raises_structured_error(self):
        def handler(request: httpx.Request) -> httpx.Response:
            return httpx.Response(200, json={"ok": False, "error": "missing_scope"})

        channel = _discovery_channel(handler)
        with pytest.raises(PushSendError) as excinfo:
            _run(channel.discover_directory())
        _run(channel._client.aclose())

        assert excinfo.value.code == "slack_api_error"
        assert "error=missing_scope" in str(excinfo.value)

    def test_nameless_channel_resolved_via_conversations_info(self):
        """补名 pass(蓝本 _slack_resolve_raw_names):无名条目经
        conversations.info 取 name,失败/具名条目零补名往返。"""
        requests: list[httpx.Request] = []

        def handler(request: httpx.Request) -> httpx.Response:
            requests.append(request)
            if request.url.path == "/api/users.conversations":
                return httpx.Response(200, json=_page([_convo("C0NONAME99", None), _convo("C0OKNAME999", "已具名")]))
            assert str(request.url).startswith("https://slack.com/api/conversations.info")
            assert request.url.params["channel"] == "C0NONAME99"
            return httpx.Response(
                200, json={"ok": True, "channel": {"id": "C0NONAME99", "name": "补名台"}}
            )

        channel = _discovery_channel(handler)
        entries = _run(channel.discover_directory())
        _run(channel._client.aclose())

        assert [(e.chat_id, e.name) for e in entries] == [
            ("C0NONAME99", "补名台"),
            ("C0OKNAME999", "已具名"),
        ]
        assert [str(r.url.path).rsplit("/", 1)[-1] for r in requests] == [
            "users.conversations",
            "conversations.info",
        ]

    def test_im_entry_resolved_via_users_info(self):
        """补名 im 分支(蓝本:is_im → users.info 取 display_name,改判 dm)。

        MYIA 的 types 枚举面不含 im(蓝本同值),该入口以形态防御身份
        保留——mock 强喂 D… 条目走通整条补名链。
        """
        requests: list[httpx.Request] = []

        def handler(request: httpx.Request) -> httpx.Response:
            requests.append(request)
            if request.url.path == "/api/users.conversations":
                return httpx.Response(200, json=_page([{"id": "D0IMENTRY9"}]))
            if request.url.path == "/api/conversations.info":
                return httpx.Response(
                    200,
                    json={"ok": True, "channel": {"id": "D0IMENTRY9", "is_im": True, "user": "U0OWNER999"}},
                )
            assert request.url.path == "/api/users.info"
            assert request.url.params["user"] == "U0OWNER999"
            return httpx.Response(
                200,
                json={
                    "ok": True,
                    "user": {"profile": {"display_name": "台主"}, "real_name": "张三", "name": "zhangsan"},
                },
            )

        channel = _discovery_channel(handler)
        entries = _run(channel.discover_directory())
        _run(channel._client.aclose())

        assert (entries[0].name, entries[0].type) == ("台主", "dm")
        assert [str(r.url.path).rsplit("/", 1)[-1] for r in requests] == [
            "users.conversations",
            "conversations.info",
            "users.info",
        ]

    def test_info_failure_keeps_id_placeholder(self):
        """补名失败(ok=false)不阻发现:条目保留 id 占位仍可寻址(蓝本同语义)。"""
        requests: list[httpx.Request] = []

        def handler(request: httpx.Request) -> httpx.Response:
            requests.append(request)
            if request.url.path == "/api/users.conversations":
                return httpx.Response(200, json=_page([_convo("C0DEAD9999", None)]))
            return httpx.Response(200, json={"ok": False, "error": "channel_not_found"})

        channel = _discovery_channel(handler)
        entries = _run(channel.discover_directory())
        _run(channel._client.aclose())

        assert [(e.chat_id, e.name) for e in entries] == [("C0DEAD9999", "C0DEAD9999")]
        assert len(requests) == 2

    def test_empty_channel_list_returns_empty_list(self):
        def handler(request: httpx.Request) -> httpx.Response:
            return httpx.Response(200, json=_page([]))

        channel = _discovery_channel(handler)
        entries = _run(channel.discover_directory())
        _run(channel._client.aclose())
        assert entries == []

    def test_missing_token_env_is_credential_error(self, monkeypatch):
        monkeypatch.delenv("SLACK_BOT_TOKEN", raising=False)
        calls: list[dict] = []
        channel = SlackChannel(client=httpx.AsyncClient(transport=_mock(calls)))

        with pytest.raises(PushSendError) as excinfo:
            _run(channel.discover_directory())
        _run(channel._client.aclose())

        assert excinfo.value.code == "env_var_missing"
        assert calls == []

    def test_discovery_merges_into_directory_refresh(self, tmp_path):
        """acceptance:发现结果经 directory.refresh 桶替换 + last_seen 盖戳 + 落盘。"""

        def handler(request: httpx.Request) -> httpx.Response:
            return httpx.Response(
                200,
                json=_page([_convo("C0AAA999999", "羊毛台"), _convo("G0BBB88888", "私人群", is_private=True)]),
            )

        channel = _discovery_channel(handler)
        directory = ChannelDirectory(tmp_path)
        counts = _run(directory.refresh({"slack": channel}, now=100.0))
        _run(channel._client.aclose())

        assert counts == {"slack": 2}
        assert [(e.chat_id, e.type, e.last_seen) for e in directory.entries("slack")] == [
            ("C0AAA999999", "channel", 100.0),
            ("G0BBB88888", "group", 100.0),
        ]
        saved = json.loads((tmp_path / "channel_directory.json").read_text(encoding="utf-8"))
        assert [e["chat_id"] for e in saved["platforms"]["slack"]] == ["C0AAA999999", "G0BBB88888"]
