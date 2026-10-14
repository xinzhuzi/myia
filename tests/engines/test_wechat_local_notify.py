"""Tests for 10-14-wechat-notify-revoke R4 — wechat_local 引擎 notify 通道件。

覆盖(AC4):sessions 白名单透传(stdin 载荷契约)/显示名白名单二查解析/
锚 #wxn-/#wxnr- 强幂等(重读同锚沉默)/水位 kv 读写(仅成功轮回写)/
key_unavailable 结构化 skip/sessions 空清单拒/交叉键拒/条目 metadata 平铺。

实现件在 :mod:`myssia.wechat.notify`(新文件);通道词表与
_fetch_impl 分发接线在引擎本体(集成统一落笔,integrationSpec)——本文件
直调实现件,接线落地后零改动继续有效。零真机零真桥
(bin_path/run_bridge_command_sync 全 monkeypatch;fixture 全合成)。
"""

from __future__ import annotations

import json
import time
from typing import Any

import httpx
import pytest

import myssia.wechat.engine as wx_engine
import myssia.wechat.notify as wx_notify
from myssia.engines.fetch_base import FetchError
from myssia.wechat.engine import WechatLocalEngine
from myssia.wechat.notify import (
    notify_anchor,
    revoke_anchor,
    validate_options,
)

from conftest import make_client, make_context, make_source, run

SOURCE_URL = "https://weixin.qq.com"
CHAT = "00000000000000000000@chatroom"  # 合成会话 id(形状真实;非真实会话)
SOURCE_NAME = "weixin-通知"


def make_bridge_bin(tmp_path):
    fake_bin = tmp_path / "wechat-bridge"
    fake_bin.write_text("#!/bin/sh\n", encoding="utf-8")
    fake_bin.chmod(0o755)
    return fake_bin


def make_notify_engine(
    *,
    sessions: Any = None,  # → engine_options.wechat_local.chat_whitelist
    notify_self: Any = None,
    store: Any = None,
    url: str = SOURCE_URL,
    options_extra: dict[str, Any] | None = None,
) -> WechatLocalEngine:
    options: dict[str, Any] = {"channel": "notify"}
    if sessions is not None:
        options["chat_whitelist"] = sessions
    if notify_self is not None:
        options["notify_self"] = notify_self
    options.update(options_extra or {})
    source = make_source(
        name=SOURCE_NAME,
        engine="wechat_local",
        url=url,
        engine_options={"wechat_local": options},
    )
    context, _clock = make_context(
        make_client(lambda request: httpx.Response(404)), store=store
    )
    return WechatLocalEngine(source, context)


class FakeRunner:
    """桥子进程 fake:按序回放应答;记录 (argv, input_text)。"""

    def __init__(self, responses: list[dict[str, Any]]) -> None:
        self.responses = list(responses)
        self.calls: list[tuple[list[str], str]] = []

    def __call__(self, argv: Any, input_text: str, timeout: float):
        self.calls.append((list(argv), input_text))
        if not self.responses:
            raise AssertionError("桥调用次数超出回放清单")
        response = self.responses.pop(0)
        if "payload" in response:
            body = response["payload"]
        elif "error" in response:
            body = {"error": response["error"]}
        else:
            body = response
        payload = json.dumps(body, ensure_ascii=False)
        return response.get("exit_code", 0), payload, ""


def scan_payload(events: list[dict[str, Any]], baseline: dict[str, Any] | None = None) -> dict[str, Any]:
    """桥 notify-scan 成功载荷(契约形;全合成)。"""
    return {
        "notify_scan": {
            "events": events,
            "baseline": baseline if baseline is not None else {},
            "stats": {
                "sessions_scanned": 1, "whitelist_sessions": 1, "candidates": 1,
                "msg_rows_read": len(events), "self_filtered": 0,
                "revoke_events": sum(1 for e in events if e["event"] == "message.revoke"),
                "db_busy": False, "duration_ms": 3,
            },
        }
    }


def new_event(**overrides: Any) -> dict[str, Any]:
    event: dict[str, Any] = {
        "event": "message.new",
        "session_id": CHAT,
        "session_display": "合成群聊",
        "sender_display": "合成张三",
        "is_self": False,
        "content_preview": "合成新消息预览",
        "ts": 1760000000,
        "server_id": 1234567890,
        "local_type": 1,
    }
    event.update(overrides)
    return event


def revoke_event(**overrides: Any) -> dict[str, Any]:
    event: dict[str, Any] = {
        "event": "message.revoke",
        "session_id": CHAT,
        "session_display": "合成群聊",
        "revoker_display": "合成李四",
        "is_self_revoke": False,
        "ts": 1760000100,
        "server_id": 1234567891,
        "local_type": 10002,
        "original": {
            "server_id": 1234567890,
            "ts": 1760000000,
            "sender_display": "合成张三",
            "content_preview": "被撤回的合成原文",
            "recovery": "server_id",
        },
        "replacemsg_text": None,
    }
    event.update(overrides)
    return event


# ---------------------------------------------------------------------------
# 1. 配置错误面(结构化 FetchError;零子进程)
# ---------------------------------------------------------------------------


class TestOptionsValidation:
    @pytest.mark.parametrize(
        "sessions",
        [None, [], [""], ["a", 3], ["a", True], "a@chatroom", {"a": 1}],
    )
    def test_bad_sessions_rejected(self, sessions: Any) -> None:
        with pytest.raises(FetchError) as excinfo:
            validate_options({"channel": "notify", "chat_whitelist": sessions})
        assert excinfo.value.error_type == "invalid_engine_options"
        assert "chat_whitelist" in str(excinfo.value)

    def test_empty_sessions_is_rejected_not_silent(self) -> None:
        """sessions 空清单 = 白名单空 = 功能空转:构造期即拒(R4)。"""
        with pytest.raises(FetchError) as excinfo:
            validate_options({"channel": "notify", "chat_whitelist": []})
        assert "功能空转" in str(excinfo.value)

    def test_defaults_and_pass_through(self) -> None:
        options = validate_options({"channel": "notify", "chat_whitelist": [CHAT, "显示名"]})
        assert options == {
            "channel": "notify",
            "chat_whitelist": [CHAT, "显示名"],
            "notify_self": False,
            "read_timeout_seconds": wx_notify.DEFAULT_NOTIFY_TIMEOUT_SECONDS,
        }
        assert validate_options(
            {"channel": "notify", "chat_whitelist": [" a@chatroom "], "notify_self": True}
        )["chat_whitelist"] == ["a@chatroom"]

    @pytest.mark.parametrize("notify_self", ["yes", 1, None])
    def test_bad_notify_self_rejected(self, notify_self: Any) -> None:
        with pytest.raises(FetchError) as excinfo:
            validate_options(
                {"channel": "notify", "chat_whitelist": ["a"], "notify_self": notify_self}
            )
        assert excinfo.value.error_type == "invalid_engine_options"

    def test_bad_timeout_rejected(self) -> None:
        with pytest.raises(FetchError) as excinfo:
            validate_options(
                {"channel": "notify", "chat_whitelist": ["a"], "read_timeout_seconds": 0}
            )
        assert excinfo.value.error_type == "invalid_engine_options"

    @pytest.mark.parametrize(
        "cross_key", ["chat", "sides", "count", "since_days", "feed_kind"]
    )
    def test_cross_channel_keys_rejected(self, cross_key: str) -> None:
        """会话/朋友圈通道专属键交叉声明即拒(消费面不同,不静默忽略)。"""
        with pytest.raises(FetchError) as excinfo:
            validate_options(
                {"channel": "notify", "chat_whitelist": ["a"], cross_key: "x"}
            )
        assert excinfo.value.error_type == "invalid_engine_options"
        assert cross_key in str(excinfo.value)


# ---------------------------------------------------------------------------
# 2. 取数全链:stdin 载荷契约 / argv / 白名单透传 / 二查解析
# ---------------------------------------------------------------------------


class TestFetchContract:
    def _patch(self, monkeypatch, tmp_path, runner: FakeRunner) -> None:
        # 两处引用都打桩:fetch_notify/bin_path 走 wx_notify 自己的 import
        # 引用,显示名二查解析走引擎方法(wx_engine 引用)。
        monkeypatch.setattr(wx_engine, "bin_path", lambda _: make_bridge_bin(tmp_path))
        monkeypatch.setattr(wx_notify, "bin_path", lambda _: make_bridge_bin(tmp_path))
        monkeypatch.setattr(wx_engine, "run_bridge_command_sync", runner)
        monkeypatch.setattr(wx_notify, "run_bridge_command_sync", runner)

    def test_argv_and_stdin_payload_contract(self, tmp_path, monkeypatch) -> None:
        runner = FakeRunner([scan_payload([])])
        self._patch(monkeypatch, tmp_path, runner)
        engine = make_notify_engine(sessions=[CHAT], notify_self=True)
        items = run(wx_notify.fetch_notify(engine, validate_options(
            {"channel": "notify", "chat_whitelist": [CHAT], "notify_self": True}
        )))
        assert items == []
        argv, input_text = runner.calls[0]
        assert argv == [
            str(make_bridge_bin(tmp_path)), "localdb", "notify-scan",
            "--file", "-", "--json",
        ]
        payload = json.loads(input_text)
        assert payload == {
            "whitelist": [CHAT],
            "baseline": None,  # 首轮:无水位 → null(桥只建基线零事件)
            "notify_self": True,
        }

    def test_id_like_session_skips_resolution_single_call(self, tmp_path, monkeypatch) -> None:
        """id 形态直通:整轮仅一次桥调用(显示名解析零二查)。"""
        runner = FakeRunner([scan_payload([])])
        self._patch(monkeypatch, tmp_path, runner)
        engine = make_notify_engine(sessions=[CHAT])
        run(wx_notify.fetch_notify(engine, validate_options(
            {"channel": "notify", "chat_whitelist": [CHAT]}
        )))
        assert len(runner.calls) == 1

    def test_display_name_resolved_via_sessions_second_query(self, tmp_path, monkeypatch) -> None:
        """显示名白名单二查解析:localdb query 应答 sessions 按名精确实 Parse。"""
        resolution = {
            "chat_id": "合成显示名",
            "since_days": 1,
            "messages": [],
            "display_name": None,
            "sessions": [{"id": CHAT, "name": "合成显示名", "unread": 0}],
            "domains": {},
        }
        runner = FakeRunner([resolution, scan_payload([])])
        self._patch(monkeypatch, tmp_path, runner)
        engine = make_notify_engine(sessions=["合成显示名"])
        run(wx_notify.fetch_notify(engine, validate_options(
            {"channel": "notify", "chat_whitelist": ["合成显示名"]}
        )))
        assert len(runner.calls) == 2
        assert runner.calls[0][0][1:4] == ["localdb", "query", "合成显示名"]
        scan_payload_json = json.loads(runner.calls[1][1])
        assert scan_payload_json["whitelist"] == [CHAT]

    def test_display_name_unresolvable_keeps_declared(self, tmp_path, monkeypatch) -> None:
        resolution = {
            "chat_id": "不在列表的名", "messages": [], "display_name": None,
            "sessions": [{"id": "other@chatroom", "name": "别的会话", "unread": 0}],
        }
        runner = FakeRunner([resolution, scan_payload([])])
        self._patch(monkeypatch, tmp_path, runner)
        engine = make_notify_engine(sessions=["不在列表的名"])
        run(wx_notify.fetch_notify(engine, validate_options(
            {"channel": "notify", "chat_whitelist": ["不在列表的名"]}
        )))
        assert json.loads(runner.calls[1][1])["whitelist"] == ["不在列表的名"]

    def test_component_missing_without_bin(self, tmp_path, monkeypatch) -> None:
        monkeypatch.setattr(
            wx_engine, "bin_path", lambda _: tmp_path / "absent-bridge"
        )
        monkeypatch.setattr(
            wx_notify, "bin_path", lambda _: tmp_path / "absent-bridge"
        )
        engine = make_notify_engine(sessions=[CHAT])
        with pytest.raises(FetchError) as excinfo:
            run(wx_notify.fetch_notify(engine, validate_options(
                {"channel": "notify", "chat_whitelist": [CHAT]}
            )))
        assert excinfo.value.error_type == "component_missing"

    def test_bridge_timeout_is_structured(self, tmp_path, monkeypatch) -> None:
        def timeout_runner(argv, input_text, timeout):
            raise wx_engine.LocalBridgeTimeoutError("wechat-bridge 超时")

        monkeypatch.setattr(wx_engine, "bin_path", lambda _: make_bridge_bin(tmp_path))
        monkeypatch.setattr(wx_notify, "bin_path", lambda _: make_bridge_bin(tmp_path))
        monkeypatch.setattr(wx_engine, "run_bridge_command_sync", timeout_runner)
        monkeypatch.setattr(wx_notify, "run_bridge_command_sync", timeout_runner)
        engine = make_notify_engine(sessions=[CHAT])
        with pytest.raises(FetchError) as excinfo:
            run(wx_notify.fetch_notify(engine, validate_options(
                {"channel": "notify", "chat_whitelist": [CHAT]}
            )))
        assert excinfo.value.error_type == "bridge_timeout"

    def test_missing_notify_scan_node_is_bridge_error(self, tmp_path, monkeypatch) -> None:
        runner = FakeRunner([{"chat_id": CHAT}])
        self._patch(monkeypatch, tmp_path, runner)
        engine = make_notify_engine(sessions=[CHAT])
        with pytest.raises(FetchError) as excinfo:
            run(wx_notify.fetch_notify(engine, validate_options(
                {"channel": "notify", "chat_whitelist": [CHAT]}
            )))
        assert excinfo.value.error_type == "bridge_error"
        assert "0.8.0" in str(excinfo.value)


# ---------------------------------------------------------------------------
# 3. 结构化空态 + 水位 kv(仅成功轮回写;AC4 主诉)
# ---------------------------------------------------------------------------


class TestSkipAndWatermark:
    def _patch(self, monkeypatch, tmp_path, runner: FakeRunner) -> None:
        # 两处引用都打桩:fetch_notify/bin_path 走 wx_notify 自己的 import
        # 引用,显示名二查解析走引擎方法(wx_engine 引用)。
        monkeypatch.setattr(wx_engine, "bin_path", lambda _: make_bridge_bin(tmp_path))
        monkeypatch.setattr(wx_notify, "bin_path", lambda _: make_bridge_bin(tmp_path))
        monkeypatch.setattr(wx_engine, "run_bridge_command_sync", runner)
        monkeypatch.setattr(wx_notify, "run_bridge_command_sync", runner)

    def test_key_unavailable_is_structured_skip_no_watermark(
        self, tmp_path, monkeypatch, engine_store
    ) -> None:
        runner = FakeRunner([{
            "error": {"code": "key_unavailable", "message": "合成:密钥未就绪",
                      "fix_hint": "合成指引"},
            "exit_code": 21,
        }])
        self._patch(monkeypatch, tmp_path, runner)
        engine = make_notify_engine(sessions=[CHAT], store=engine_store)
        options = validate_options({"channel": "notify", "chat_whitelist": [CHAT]})
        assert run(wx_notify.fetch_notify(engine, options)) == []
        assert engine.last_skip_reason == "key_unavailable"
        assert engine_store.get_baseline(wx_engine.watermark_key(SOURCE_NAME)) is None

    def test_watermark_round_trip_only_on_success(
        self, tmp_path, monkeypatch, engine_store
    ) -> None:
        """成功轮回写 JSON 基线;skip 轮不推进(下轮仍传 null/旧值)。"""
        events = [new_event()]
        baseline_out = {CHAT: {"ts": 1760000100, "unread": 5}}
        runner = FakeRunner([
            scan_payload(events, baseline_out),
            {"error": {"code": "key_unavailable", "message": "合成"}, "exit_code": 21},
            scan_payload([], {CHAT: {"ts": 1760000200, "unread": 5}}),
        ])
        self._patch(monkeypatch, tmp_path, runner)
        options = validate_options({"channel": "notify", "chat_whitelist": [CHAT]})
        engine = make_notify_engine(sessions=[CHAT], store=engine_store)
        assert len(run(wx_notify.fetch_notify(engine, options))) == 1
        stored = engine_store.get_baseline(wx_engine.watermark_key(SOURCE_NAME))
        assert stored is not None and json.loads(stored.etag) == baseline_out
        # 第二轮(skip):水位不推进,stdin 仍带旧基线
        engine2 = make_notify_engine(sessions=[CHAT], store=engine_store)
        assert run(wx_notify.fetch_notify(engine2, options)) == []
        assert json.loads(runner.calls[1][1])["baseline"] == baseline_out
        # 第三轮(成功零事件):推进到新基线
        engine3 = make_notify_engine(sessions=[CHAT], store=engine_store)
        assert run(wx_notify.fetch_notify(engine3, options)) == []
        stored3 = engine_store.get_baseline(wx_engine.watermark_key(SOURCE_NAME))
        assert json.loads(stored3.etag) == {CHAT: {"ts": 1760000200, "unread": 5}}

    def test_corrupt_watermark_falls_back_to_first_round(
        self, tmp_path, monkeypatch, engine_store
    ) -> None:
        engine_store.set_baseline(
            wx_engine.watermark_key(SOURCE_NAME), etag="not-json"
        )
        runner = FakeRunner([scan_payload([])])
        self._patch(monkeypatch, tmp_path, runner)
        engine = make_notify_engine(sessions=[CHAT], store=engine_store)
        options = validate_options({"channel": "notify", "chat_whitelist": [CHAT]})
        run(wx_notify.fetch_notify(engine, options))
        assert json.loads(runner.calls[0][1])["baseline"] is None

    def test_no_store_degrades_to_first_round_stdin(
        self, tmp_path, monkeypatch
    ) -> None:
        runner = FakeRunner([scan_payload([])])
        self._patch(monkeypatch, tmp_path, runner)
        engine = make_notify_engine(sessions=[CHAT], store=None)
        options = validate_options({"channel": "notify", "chat_whitelist": [CHAT]})
        run(wx_notify.fetch_notify(engine, options))
        assert json.loads(runner.calls[0][1])["baseline"] is None


# ---------------------------------------------------------------------------
# 4. 条目铸形:强锚幂等 + metadata 平铺 + 撤回三态
# ---------------------------------------------------------------------------


class TestItems:
    def test_new_message_item_shape_and_strong_anchor(self) -> None:
        items = wx_notify.items_from_events([new_event()])
        assert len(items) == 1
        item = items[0]
        assert item["url"] == notify_anchor(CHAT, 1234567890)
        assert item["url"] == (
            f"wechat-local://notify/{CHAT.replace('@', '%40')}#wxn-1234567890"
        )
        assert item["title"] == "合成群聊 · 合成张三"
        assert item["content"] == "合成新消息预览"
        assert item["event"] == "message.new"
        assert item["revoke"] is False
        assert item["side"] == "left"
        assert item["server_id"] == 1234567890
        assert item["local_type"] == 1

    def test_revoke_item_shape_and_recovery_metadata(self) -> None:
        items = wx_notify.items_from_events([revoke_event()])
        item = items[0]
        assert item["url"] == revoke_anchor(CHAT, 1234567891)
        assert "#wxnr-1234567891" in item["url"]
        assert item["revoke"] is True
        assert item["revoke_recovery"] == "server_id"
        assert item["revoke_original_preview"] == "被撤回的合成原文"
        assert item["content"] == '合成李四撤回了一条消息:原内容:"被撤回的合成原文"'

    @pytest.mark.parametrize(
        ("event", "expected_body"),
        [
            (revoke_event(), '合成李四撤回了一条消息:原内容:"被撤回的合成原文"'),
            (
                revoke_event(original=None, replacemsg_text='"合成王五"撤回了一条消息'),
                '合成李四撤回了一条消息:"合成王五"撤回了一条消息',
            ),
            (revoke_event(original=None), "合成李四撤回了一条消息:原内容未能恢复"),
        ],
    )
    def test_revoke_three_state_bodies(self, event: dict, expected_body: str) -> None:
        items = wx_notify.items_from_events([event])
        assert items[0]["content"] == expected_body

    def test_anchor_strong_idempotency_on_rescan(self) -> None:
        """同事件重扫恒同锚(AC4:重读同锚沉默,dedup 消化重叠)。"""
        first = wx_notify.items_from_events([new_event(), revoke_event()])
        second = wx_notify.items_from_events([new_event(), revoke_event()])
        assert [item["url"] for item in first] == [item["url"] for item in second]

    def test_self_message_side_is_right(self) -> None:
        items = wx_notify.items_from_events([new_event(is_self=True)])
        assert items[0]["side"] == "right"

    def test_unknown_event_shape_skipped(self) -> None:
        assert wx_notify.items_from_events([{"event": "future.kind"}, "junk"]) == []

    def test_title_clipped_to_engine_limit(self) -> None:
        long_name = "超" * 200
        items = wx_notify.items_from_events(
            [new_event(session_display=long_name)]
        )
        assert len(items[0]["title"]) <= wx_engine.TITLE_MAX_CHARS + 1
