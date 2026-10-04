"""Tests for FeishuCardChannel 定向发送 + 直达解析 — 10-03-messaging-feishu 步骤 2。

覆盖:``supports_targeting`` 翻 True;``context.target.chat_id`` 优先于
通道自带 legacy target;两路都缺席 → ``missing_target`` 结构化错误
(schema 放宽「targets 在场时 target 可省」的发送侧对应物);``ou_``
前缀按 receive_id_type=open_id 投递(Hermes 发送路由同款);
``parse_direct_ref`` 对 oc_/ou_/on_/chat_/open_ 前缀直达(含 ``:thread``
部分),非 id 形态返回 None 走目录;经 core ``resolve_target`` 真钩子
打通直达/目录两条解析路。话题定向(10-04-feishu-thread-send):
``context.target.thread_id`` 在场改投 ``{thread_id}/reply`` 话题回复
端点(root_id 锚定),三段 spec ``feishu:<名或id>:<thread_id>`` 经 core
解析接线。全部 httpx.MockTransport,零真实网络。
"""

from __future__ import annotations

import asyncio
import json
from dataclasses import replace

import httpx
import pytest

from myssia.push import FeishuCardChannel, PushSendError, SendContext
from myssia.push.directory import ChannelDirectory, ChannelEntry
from myssia.push.feishu_card import API_URL, thread_reply_url
from myssia.push.targets import ChannelTarget, TargetResolveError, resolve_target


def _capture_client(capture: dict) -> httpx.AsyncClient:
    def handler(request: httpx.Request) -> httpx.Response:
        capture["url"] = str(request.url)
        capture["auth"] = request.headers.get("Authorization")
        capture["body"] = json.loads(request.content)
        return httpx.Response(200, json={"code": 0, "msg": "success", "data": {}})

    return httpx.AsyncClient(transport=httpx.MockTransport(handler))


def _ctx(target: ChannelTarget | None = None) -> SendContext:
    return replace(
        SendContext(slot="am", date="2026-10-03", category="羊毛", kind="immediate"),
        target=target,
    )


class TestTargetedSend:
    def test_supports_targeting_is_true(self):
        assert FeishuCardChannel.supports_targeting is True

    def test_context_target_overrides_channel_legacy_target(self, monkeypatch):
        """定向优先:context.target.chat_id 胜过通道自带 env 引用。"""
        monkeypatch.setenv("MYIA_TEST_CHAT_ID", "oc_legacy")
        capture: dict = {}
        client = _capture_client(capture)
        channel = FeishuCardChannel(
            target="env:MYIA_TEST_CHAT_ID", token="t", client=client
        )
        target = ChannelTarget(
            platform="feishu", chat_id="oc_direct_1", name="AI中转站合伙人群"
        )

        asyncio.run(
            channel.send([{"title": "条目", "url": "https://e/1"}], _ctx(target))
        )
        asyncio.run(client.aclose())

        assert capture["body"]["receive_id"] == "oc_direct_1"
        assert "receive_id_type=chat_id" in capture["url"]

    def test_legacy_target_used_when_no_context_target(self, monkeypatch):
        monkeypatch.setenv("MYIA_TEST_CHAT_ID", "oc_legacy")
        capture: dict = {}
        client = _capture_client(capture)
        channel = FeishuCardChannel(
            target="env:MYIA_TEST_CHAT_ID", token="t", client=client
        )

        asyncio.run(channel.send([{"title": "条目"}], _ctx(None)))
        asyncio.run(client.aclose())

        assert capture["body"]["receive_id"] == "oc_legacy"

    def test_targets_only_config_sends_via_context_target(self):
        """schema 放宽:targets 在场时 target 可省——构造与发送都成立。"""
        capture: dict = {}
        client = _capture_client(capture)
        channel = FeishuCardChannel(token="t", client=client)  # 无 legacy target

        target = ChannelTarget(platform="feishu", chat_id="oc_from_targets")
        asyncio.run(channel.send([{"title": "条目"}], _ctx(target)))
        asyncio.run(client.aclose())

        assert capture["body"]["receive_id"] == "oc_from_targets"

    def test_no_target_no_context_raises_missing_target(self):
        capture: dict = {}
        client = _capture_client(capture)
        channel = FeishuCardChannel(token="t", client=client)

        with pytest.raises(PushSendError) as excinfo:
            asyncio.run(channel.send([{"title": "条目"}], _ctx(None)))
        asyncio.run(client.aclose())

        assert excinfo.value.code == "missing_target"

    def test_ou_prefix_routes_as_open_id(self):
        """ou_(用户 open_id)按 receive_id_type=open_id 投递(Hermes 同款)。"""
        capture: dict = {}
        client = _capture_client(capture)
        channel = FeishuCardChannel(token="t", client=client)

        target = ChannelTarget(platform="feishu", chat_id="ou_user123")
        asyncio.run(channel.send([{"title": "条目"}], _ctx(target)))
        asyncio.run(client.aclose())

        assert capture["body"]["receive_id"] == "ou_user123"
        assert "receive_id_type=open_id" in capture["url"]


class TestParseDirectRef:
    @pytest.mark.parametrize(
        "ref,chat_id,thread_id",
        [
            ("oc_9a79abc123", "oc_9a79abc123", None),
            ("ou_2f4c5d6e", "ou_2f4c5d6e", None),
            ("on_union0id", "on_union0id", None),
            ("chat_legacy99", "chat_legacy99", None),
            ("open_scoped42", "open_scoped42", None),
            ("oc_group1:mt_topic2", "oc_group1", "mt_topic2"),
        ],
    )
    def test_id_prefixes_resolve_direct(
        self, ref: str, chat_id: str, thread_id: str | None
    ):
        target = FeishuCardChannel.parse_direct_ref(ref)
        assert target is not None
        assert target.platform == "feishu"
        assert target.chat_id == chat_id
        assert target.thread_id == thread_id
        assert target.resolved_from == "direct"

    @pytest.mark.parametrize(
        "ref", ["AI中转站合伙人群", "oc_", "#群名", "mt_topic_only", "oc_a:b:c"]
    )
    def test_non_id_refs_return_none(self, ref: str):
        """非 id 形态 → None:调用方回落目录四路径解析(名称/前缀匹配)。

        注:``oc_-``(裸连字符)按 Hermes 原正则 ``[-A-Za-z0-9]+`` 同样
        放行——保真上游,不做额外收紧。
        """
        assert FeishuCardChannel.parse_direct_ref(ref) is None


class TestResolveTargetWiring:
    """真钩子接线:core resolve_target 经 PLATFORMS 表吃到 feishu 直达钩子。"""

    PLATFORMS = {"feishu": FeishuCardChannel}

    def _directory(self, tmp_path) -> ChannelDirectory:
        directory = ChannelDirectory(tmp_path)
        directory.replace_platform(
            "feishu",
            [ChannelEntry(platform="feishu", chat_id="g1", name="AI中转站合伙人群")],
            now=1.0,
        )
        return directory

    def test_direct_ref_bypasses_directory(self, tmp_path):
        target = resolve_target(
            "feishu:oc_9a79notindir",
            self._directory(tmp_path),
            platforms=self.PLATFORMS,
        )
        assert (target.chat_id, target.resolved_from) == ("oc_9a79notindir", "direct")

    def test_name_resolution_still_reaches_directory(self, tmp_path):
        """非 id spec 不被钩子拦截,照常目录精确名路径。"""
        target = resolve_target(
            "feishu:AI中转站合伙人群",
            self._directory(tmp_path),
            platforms=self.PLATFORMS,
        )
        assert (target.chat_id, target.resolved_from) == ("g1", "directory_name")


class TestThreadSend:
    """话题定向发送(10-04-feishu-thread-send):root_id 话题回复路径。"""

    def test_thread_target_posts_to_reply_endpoint(self):
        """thread_id 在场 → POST {API_URL}/{thread_id}/reply,体只带 msg_type/content。"""
        capture: dict = {}
        client = _capture_client(capture)
        channel = FeishuCardChannel(token="t", client=client)

        target = ChannelTarget(
            platform="feishu", chat_id="oc_g", thread_id="om_topic_root1"
        )
        asyncio.run(
            channel.send([{"title": "条目", "url": "https://e/1"}], _ctx(target))
        )
        asyncio.run(client.aclose())

        assert capture["url"] == f"{API_URL}/om_topic_root1/reply"
        assert capture["url"] == thread_reply_url("om_topic_root1")
        assert "receive_id_type" not in capture["url"]  # 回复端点无该查询参
        assert set(capture["body"]) == {"msg_type", "content"}
        assert capture["body"]["msg_type"] == "interactive"

    def test_thread_reply_carries_card_content(self):
        """回复体 content 是完整互动卡(header/elements 在场),非裸文本。"""
        capture: dict = {}
        client = _capture_client(capture)
        channel = FeishuCardChannel(token="t", client=client)

        target = ChannelTarget(platform="feishu", chat_id="oc_g", thread_id="om_root2")
        asyncio.run(
            channel.send([{"title": "标题A", "url": "https://e/2"}], _ctx(target))
        )
        asyncio.run(client.aclose())

        content = json.loads(capture["body"]["content"])
        assert content["config"] == {"wide_screen_mode": True}
        assert content["header"]["template"] == "blue"
        assert any("标题A" in str(element) for element in content["elements"])

    def test_blank_thread_falls_back_to_create(self):
        """thread_id 空白串按缺席处理(.strip() or None)→ create 路径不变。"""
        capture: dict = {}
        client = _capture_client(capture)
        channel = FeishuCardChannel(token="t", client=client)

        target = ChannelTarget(platform="feishu", chat_id="oc_g", thread_id="  ")
        asyncio.run(channel.send([{"title": "条目"}], _ctx(target)))
        asyncio.run(client.aclose())

        assert capture["url"].split("?")[0] == API_URL
        assert "receive_id_type=chat_id" in capture["url"]
        assert capture["body"]["receive_id"] == "oc_g"

    def test_invalid_thread_shape_raises_structured_error(self):
        """话题 id 形态非法:结构化报错 + 解析值不回显(discord 同款纪律)。"""
        capture: dict = {}
        client = _capture_client(capture)
        channel = FeishuCardChannel(token="t", client=client)

        target = ChannelTarget(
            platform="feishu", chat_id="oc_g", thread_id="om_x/evil path"
        )
        with pytest.raises(PushSendError) as excinfo:
            asyncio.run(channel.send([{"title": "条目"}], _ctx(target)))
        asyncio.run(client.aclose())

        assert excinfo.value.code == "invalid_thread_ref"
        assert "om_x" not in str(excinfo.value)  # 解析值不回显
        assert "url" not in capture  # 校验先于任何 HTTP(零请求发出)

    def test_supports_threads_flag_is_true(self):
        """supports_threads 声明:core targets 三段拆分的平台 opt-in 旗标。"""
        assert FeishuCardChannel.supports_threads is True


class TestThreadSpecWiring:
    """真钩子接线:三段 spec ``feishu:<名或id>:<thread_id>`` 经 core 解析。"""

    PLATFORMS = {"feishu": FeishuCardChannel}

    def _directory(self, tmp_path, thread_id: str | None = None) -> ChannelDirectory:
        directory = ChannelDirectory(tmp_path)
        directory.replace_platform(
            "feishu",
            [
                ChannelEntry(
                    platform="feishu",
                    chat_id="g1",
                    name="AI中转站合伙人群",
                    thread_id=thread_id,
                )
            ],
            now=1.0,
        )
        return directory

    def test_three_segment_via_directory_name(self, tmp_path):
        target = resolve_target(
            "feishu:AI中转站合伙人群:om_t1",
            self._directory(tmp_path),
            platforms=self.PLATFORMS,
        )
        assert (target.chat_id, target.thread_id, target.resolved_from) == (
            "g1",
            "om_t1",
            "directory_name",
        )

    def test_three_segment_via_directory_chat_id(self, tmp_path):
        target = resolve_target(
            "feishu:g1:om_t2", self._directory(tmp_path), platforms=self.PLATFORMS
        )
        assert (target.chat_id, target.thread_id, target.resolved_from) == (
            "g1",
            "om_t2",
            "directory_id",
        )

    def test_directory_entry_thread_flows_without_segment(self, tmp_path):
        """无显式段:目录条目存量 thread_id 照旧透传(10-03 承诺的兑现口)。"""
        target = resolve_target(
            "feishu:AI中转站合伙人群",
            self._directory(tmp_path, thread_id="om_stored"),
            platforms=self.PLATFORMS,
        )
        assert (target.chat_id, target.thread_id) == ("g1", "om_stored")

    def test_explicit_segment_overrides_entry_thread(self, tmp_path):
        """显式话题段比目录存量新:spec 段覆盖 entry.thread_id。"""
        target = resolve_target(
            "feishu:AI中转站合伙人群:om_fresh",
            self._directory(tmp_path, thread_id="om_stale"),
            platforms=self.PLATFORMS,
        )
        assert (target.chat_id, target.thread_id) == ("g1", "om_fresh")

    def test_direct_id_base_with_thread_segment(self, tmp_path):
        """base 是直达 id 形态(钩子吃 bare id)→ direct + 话题段。"""
        target = resolve_target(
            "feishu:oc_9a79:om_t3", self._directory(tmp_path), platforms=self.PLATFORMS
        )
        assert (target.chat_id, target.thread_id, target.resolved_from) == (
            "oc_9a79",
            "om_t3",
            "direct",
        )

    def test_non_id_thread_segment_not_split(self, tmp_path):
        """话题段中文(不匹配保守 id 字符集)不拆 → 按整体未命中报错。"""
        with pytest.raises(TargetResolveError) as excinfo:
            resolve_target(
                "feishu:AI中转站合伙人群:话题甲",
                self._directory(tmp_path),
                platforms=self.PLATFORMS,
            )
        assert excinfo.value.reason == "unresolvable"
