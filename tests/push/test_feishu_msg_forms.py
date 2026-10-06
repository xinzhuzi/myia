"""Tests for 10-06-hermes-align 批次1/2 + 组合优先铁律 — 飞书投递面。

覆盖三面:

- **组合铁律**(主人 10-06 令,最高优先):同轮 immediate 多条命中恰发
  **一条**(头=类目+条数,正文=逐条标题+链接);digest N 条恰一条文本
  消息;定向 specs 分组不跨对象串台;合并组失败不 record_push。
- **文本消息形态**(批次1,``msg_form: text``):post md rows 蓝本直译
  (无 fence 单 row / fence 切 row);阈值内单条无段指示;真超
  ``POST_SPLIT_THRESHOLD`` 按行边界续条且每段头尾 ``(i/N)`` 标注
  (蓝本 ``truncate_message`` ``(1/3)`` 指示同款,gateway/platforms/
  base.py:4874);footer 只随末段。
- **双机器人**(批次2,``bot: analyst``):FEISHU2_* 凭据 mint(缓存按
  app_id 分键);凭据缺结构化指引;chat id 沿用主群 target 不随 bot 切换;
  构造期词表纵深防御。

No pytest-asyncio in dev deps: async calls run through ``asyncio.run``
(同 test_push_credential_journey.py 约定)。All network I/O goes through
``httpx.MockTransport``,钥匙链走 InMemoryKeychainBackend 注入——零真实
网络、零真实钥匙链触碰。
"""

from __future__ import annotations

import asyncio
import json
from datetime import datetime
from typing import Any

import httpx
import pytest

from myssia import secrets as secrets_store
from myssia.dedup import DedupRegistry
from myssia.push import FeishuCardChannel, PushSendError, SendContext
from myssia.push.digest import DigestAggregator, send_immediate
from myssia.push.feishu_card import (
    API_URL,
    BOT_APP_CREDENTIAL_KEYS,
    TENANT_TOKEN_CACHE,
    TOKEN_API_URL,
    build_post_rows,
    card_title,
)
from myssia.schema import LoadError, load_category
from myssia.store import SQLiteStore

_PUSH_ENV_KEYS = (
    "FEISHU_BOT_TOKEN",
    "FEISHU_CHAT_ID",
    "FEISHU_APP_ID",
    "FEISHU_APP_SECRET",
    "FEISHU2_APP_ID",
    "FEISHU2_APP_SECRET",
    "MYIA_TEST_CHAT_ID",
)

NOW = datetime(2026, 10, 6, 10, 0)


@pytest.fixture(autouse=True)
def _in_memory_keychain(monkeypatch):
    """每用例独立 InMemory 钥匙链 + 推送 env 清零 + mint 缓存清零;用毕复位。"""
    secrets_store.set_backend(secrets_store.InMemoryKeychainBackend())
    for var in _PUSH_ENV_KEYS:
        monkeypatch.delenv(var, raising=False)
    TENANT_TOKEN_CACHE.clear()
    yield
    secrets_store.reset_backend()
    TENANT_TOKEN_CACHE.clear()


def _capture(request: httpx.Request) -> dict[str, Any]:
    return {
        "url": str(request.url),
        "auth": request.headers.get("authorization", ""),
        "body": json.loads(request.content.decode("utf-8")) if request.content else {},
    }


def _mock(calls: list[dict], *, token: str = "t-tenant") -> httpx.MockTransport:
    """token mint + 消息端点双路由 mock;两端口都记入 calls。"""

    def handler(request: httpx.Request) -> httpx.Response:
        calls.append(_capture(request))
        if str(request.url) == TOKEN_API_URL:
            return httpx.Response(
                200, json={"code": 0, "tenant_access_token": token, "expire": 7200}
            )
        return httpx.Response(200, json={"code": 0, "msg": "success", "data": {}})

    return httpx.MockTransport(handler)


def _channel(
    calls: list[dict],
    *,
    msg_form: str = "text",
    bot: str | None = None,
    token: str | None = "t-injected",
    template: str | None = None,
    token_value: str = "t-tenant",
) -> FeishuCardChannel:
    return FeishuCardChannel(
        target="env:MYIA_TEST_CHAT_ID",
        token=token,
        msg_form=msg_form,
        bot=bot,
        template=template,
        client=httpx.AsyncClient(transport=_mock(calls, token=token_value)),
    )


def _ctx(kind: str = "immediate", category: str | None = "羊毛") -> SendContext:
    return SendContext(slot="am", date="2026-10-06", category=category, kind=kind)


def _items(n: int, *, prefix: str = "示例") -> list[dict[str, Any]]:
    return [
        {"title": f"{prefix}{i}", "url": f"https://example.com/{i}", "category": "羊毛"}
        for i in range(1, n + 1)
    ]


def _message_calls(calls: list[dict]) -> list[dict]:
    """过滤出 im/v1/messages 消息请求(mint 端点剔除)。"""
    return [c for c in calls if str(c["url"]).startswith(API_URL)]


def _rows_text(body: dict[str, Any]) -> str:
    """post 载荷全部 md row 文本拼回单串(断言用)。"""
    content = json.loads(body["content"])["zh_cn"]["content"]
    return "\n".join(element.get("text", "") for row in content for element in row)


# ---------------------------------------------------------------------------
# 组合铁律 ①:同轮 immediate 多条 → 恰一条消息
# ---------------------------------------------------------------------------


class TestImmediateCombination:
    def test_same_round_items_merge_into_single_message(self, monkeypatch, tmp_path):
        """组合铁律(主人令):同轮 N 条命中恰发**一条**,头=类目+条数。"""
        monkeypatch.setenv("MYIA_TEST_CHAT_ID", "oc_main_group")
        calls: list[dict] = []
        channel = _channel(calls)
        store = SQLiteStore(tmp_path / "imm.db")
        try:
            registry = DedupRegistry(store)
            reports = asyncio.run(
                send_immediate(
                    _items(3),
                    channels=[channel],
                    registry=registry,
                    now=NOW,
                    category="羊毛",
                )
            )
        finally:
            store.close()
        messages = _message_calls(calls)
        assert len(messages) == 1  # 恰一条(逐条单发已消灭)
        assert len(reports) == 1 and reports[0].ok and reports[0].item_count == 3
        body = messages[0]["body"]
        assert body["msg_type"] == "post"
        text = _rows_text(body)
        assert "羊毛" in text and "3条" in text  # 消息头=类目+条数
        for i in (1, 2, 3):
            # 正文=逐条标题+链接
            assert f"示例{i}" in text and f"https://example.com/{i}" in text

    def test_card_form_also_merges_with_count_header(self, monkeypatch):
        """卡片形态同守铁律:同轮 3 条一张卡,标题带「3条」。"""
        monkeypatch.setenv("MYIA_TEST_CHAT_ID", "oc_main_group")
        calls: list[dict] = []
        channel = _channel(calls, msg_form="card")
        asyncio.run(
            send_immediate(
                _items(3),
                channels=[channel],
                now=NOW,
                category="羊毛",
            )
        )
        messages = _message_calls(calls)
        assert len(messages) == 1
        card = json.loads(messages[0]["body"]["content"])
        title = card["header"]["title"]["content"]
        assert title.startswith("🔔 羊毛") and title.endswith("· 3条")

    def test_targeted_groups_do_not_cross(self, tmp_path):
        """定向 specs 分组:同 specs 合一组、不同 specs 各组,不跨对象串台。"""

        class Recording:
            name = "recording"

            def __init__(self) -> None:
                self.calls: list[dict] = []

            async def send(self, items, context) -> None:
                self.calls.append({"items": list(items), "context": context})

        channel = Recording()
        items = _items(5)
        # 条目 0/1 无 specs(legacy 合一组);2/3 → spec 甲(一组);4 → spec 乙(一组)。
        specs: list[list[str] | None] = [
            None,
            None,
            ["feishu:甲"],
            ["feishu:甲"],
            ["feishu:乙"],
        ]
        reports = asyncio.run(
            send_immediate(
                items,
                channels=[channel],
                item_specs=specs,
                directory=None,  # 未接线目录:定向组按失败报告,legacy 组照发
                now=NOW,
            )
        )
        assert len(channel.calls) == 1  # 仅 legacy 组真正到达通道,且整组一条
        assert len(channel.calls[0]["items"]) == 2
        # 1 legacy 成功报告 + 2 定向组失败报告(组粒度,不再逐条 ×5)
        assert len(reports) == 3
        assert reports[0].ok and reports[0].item_count == 2
        assert all(not r.ok for r in reports[1:])

    def test_merged_group_failure_records_nothing(self, tmp_path):
        """合并组同进退:发送失败 → 组内任何 key 都不 record_push。"""
        store = SQLiteStore(tmp_path / "imm-fail.db")
        try:
            registry = DedupRegistry(store)

            class Bad:
                name = "bad"

                async def send(self, items, context) -> None:
                    raise PushSendError("http_error", "模拟故障")

            reports = asyncio.run(
                send_immediate(
                    _items(2),
                    channels=[Bad()],
                    registry=registry,
                    now=NOW,
                )
            )
            assert len(reports) == 1 and not reports[0].ok
            assert reports[0].item_count == 2
            for i in (1, 2):
                assert registry.get_entry(f"https://example.com/{i}") is None
        finally:
            store.close()


# ---------------------------------------------------------------------------
# 组合铁律 ②:digest N 条 → 恰一条文本消息(超限才续条)
# ---------------------------------------------------------------------------


class TestDigestCombination:
    def test_flush_n_items_single_text_message(self, monkeypatch):
        monkeypatch.setenv("MYIA_TEST_CHAT_ID", "oc_main_group")
        calls: list[dict] = []
        channel = _channel(calls)
        aggregator = DigestAggregator(channels=[channel])
        for item in _items(6):
            aggregator.add(item, dedup_key=item["url"])
        reports = asyncio.run(aggregator.flush(now=NOW, category="羊毛"))
        messages = _message_calls(calls)
        assert len(messages) == 1  # 摘要 N 条恰一条(阈值内绝不拆)
        assert reports and reports[0].ok and reports[0].item_count == 6
        text = _rows_text(messages[0]["body"])
        assert "示例6" in text and "MYIA 自动聚合推送" in text  # 全条目 + footer
        assert "(1/" not in text  # 单条无段指示


# ---------------------------------------------------------------------------
# 批次1:文本消息形态(蓝本 md rows 直译 + 4000 拆分 + (i/N) 标注)
# ---------------------------------------------------------------------------


class TestPostRows:
    def test_plain_markdown_single_row(self):
        rows = build_post_rows("第一行\n第二行")
        assert rows == [[{"tag": "md", "text": "第一行\n第二行"}]]

    def test_empty_content_single_empty_row(self):
        assert build_post_rows("") == [[{"tag": "md", "text": ""}]]

    def test_code_fence_gets_own_rows(self):
        """fence 切 row(上游 _build_markdown_post_rows 直译):prose/fence/prose。"""
        md = "前文\n```python\nprint(1)\n```\n后文"
        rows = build_post_rows(md)
        texts = [row[0]["text"] for row in rows]
        assert texts == ["前文", "```python\nprint(1)\n```", "后文"]


class TestTextFormSplit:
    def test_under_threshold_single_message_with_footer(self, monkeypatch):
        monkeypatch.setenv("MYIA_TEST_CHAT_ID", "oc_main_group")
        calls: list[dict] = []
        channel = _channel(calls)
        asyncio.run(channel.send(_items(3), _ctx("digest")))
        messages = _message_calls(calls)
        assert len(messages) == 1
        text = _rows_text(messages[0]["body"])
        assert "(1/" not in text
        assert text.rstrip().endswith(
            "MYIA 自动聚合推送 · 条目来自公开论坛分享,注意甄别风险。"
        )

    def test_over_threshold_splits_with_head_tail_markers(self, monkeypatch):
        """真超 4000 才续条;每段头尾 ``(i/N)`` 标注,footer 只随末段,段间不丢条目。"""
        monkeypatch.setenv("MYIA_TEST_CHAT_ID", "oc_main_group")
        calls: list[dict] = []
        channel = _channel(calls)
        items = [
            {"title": f"长文{i} " + "字" * 900, "url": f"https://example.com/big/{i}"}
            for i in range(1, 10)
        ]
        asyncio.run(channel.send(items, _ctx("digest")))
        messages = _message_calls(calls)
        assert len(messages) >= 2  # 拆条是不得已(真超阈值)
        total = len(messages)
        for index, call in enumerate(messages):
            text = _rows_text(call["body"])
            marker = f"({index + 1}/{total})"
            lines = text.splitlines()
            assert lines[0] == marker  # 头标注(独立首行)
            assert text.count(marker) >= 2  # 尾标注(末行再出现一次)
        footers = [
            i
            for i, call in enumerate(messages)
            if "MYIA 自动聚合推送" in _rows_text(call["body"])
        ]
        assert footers == [total - 1]  # footer 只随末段
        all_text = "\n".join(_rows_text(c["body"]) for c in messages)
        for i in range(1, 10):
            assert f"https://example.com/big/{i}" in all_text  # 段间不丢条目

    def test_template_rendered_into_post_payload(self, monkeypatch):
        monkeypatch.setenv("MYIA_TEST_CHAT_ID", "oc_main_group")
        calls: list[dict] = []
        channel = _channel(
            calls, template="{% for i in items %}· {{ i.title }}\n{% endfor %}"
        )
        asyncio.run(channel.send(_items(2), _ctx("digest")))
        text = _rows_text(_message_calls(calls)[0]["body"])
        assert "· 示例1" in text and "· 示例2" in text


class TestCardTitleCount:
    def test_immediate_branch_appends_count(self):
        assert card_title(_ctx("immediate", "羊毛"), count=3).endswith("· 3条")

    def test_count_omitted_keeps_legacy_shape(self):
        """既有调用方(ntfy/telegram/bark/email/apprise/HA 单参调用)零感知。"""
        assert card_title(_ctx("immediate", "羊毛")) == "🔔 羊毛 · 10-06"

    def test_non_immediate_ignores_count(self):
        # digest/cron_summary 支不受 count 影响(组合头形态只属 immediate)。
        assert card_title(_ctx("digest", "羊毛"), count=3) == card_title(
            _ctx("digest", "羊毛")
        )
        ctx = SendContext(slot="am", date="2026-10-06", kind="cron_summary")
        assert card_title(ctx, count=3) == card_title(ctx)


# ---------------------------------------------------------------------------
# 批次2:双机器人(bot: analyst → FEISHU2_* 凭据)
# ---------------------------------------------------------------------------


class TestDualBot:
    def test_analyst_mints_token_with_feishu2_and_keeps_main_chat(self, monkeypatch):
        """二号机器人:FEISHU2_* mint + chat id 沿用主群 target(不随 bot 切换)。"""
        monkeypatch.setenv("FEISHU2_APP_ID", "cli_analyst_app")
        monkeypatch.setenv("FEISHU2_APP_SECRET", "sec_analyst")
        monkeypatch.setenv("MYIA_TEST_CHAT_ID", "oc_main_group")
        calls: list[dict] = []
        channel = _channel(calls, bot="analyst", token=None, token_value="t-analyst")
        asyncio.run(channel.send(_items(1), _ctx()))
        mints = [c for c in calls if str(c["url"]) == TOKEN_API_URL]
        assert mints and mints[0]["body"] == {
            "app_id": "cli_analyst_app",
            "app_secret": "sec_analyst",
        }
        messages = _message_calls(calls)
        assert messages[0]["auth"] == "Bearer t-analyst"  # 消息走二号 token
        assert messages[0]["body"]["receive_id"] == "oc_main_group"  # 主群不切换

    def test_analyst_missing_credentials_structured_error(self):
        calls: list[dict] = []
        channel = _channel(calls, bot="analyst", token=None)
        with pytest.raises(PushSendError) as excinfo:
            asyncio.run(channel.send(_items(1), _ctx()))
        assert excinfo.value.code == "env_var_missing"
        assert "FEISHU2_APP_ID" in str(excinfo.value)
        assert "FEISHU2_APP_SECRET" in str(excinfo.value)
        assert calls == []  # 零请求发出(fail-fast)

    def test_token_cache_keyed_by_app_id(self, monkeypatch):
        """缓存按 app_id 分键:二号 token 不误写主机器人位。"""
        monkeypatch.setenv("FEISHU2_APP_ID", "cli_analyst_app")
        monkeypatch.setenv("FEISHU2_APP_SECRET", "sec_analyst")
        monkeypatch.setenv("MYIA_TEST_CHAT_ID", "oc_main_group")
        calls: list[dict] = []
        channel = _channel(calls, bot="analyst", token=None, token_value="t-analyst")
        asyncio.run(channel.send(_items(1), _ctx()))
        assert TENANT_TOKEN_CACHE["cli_analyst_app"][0] == "t-analyst"

    def test_analyst_via_keychain_fallback(self, monkeypatch):
        """env 缺 → 钥匙链规范名 myia/push/FEISHU2_* 回退(同主机器人链)。"""
        secrets_store.set_secret("myia/push/FEISHU2_APP_ID", "kc_app")
        secrets_store.set_secret("myia/push/FEISHU2_APP_SECRET", "kc_sec")
        monkeypatch.setenv("MYIA_TEST_CHAT_ID", "oc_main_group")
        calls: list[dict] = []
        channel = _channel(calls, bot="analyst", token=None)
        asyncio.run(channel.send(_items(1), _ctx()))
        mints = [c for c in calls if str(c["url"]) == TOKEN_API_URL]
        assert mints[0]["body"]["app_id"] == "kc_app"

    def test_constructor_vocabulary_defense(self):
        with pytest.raises(ValueError, match="msg_form"):
            FeishuCardChannel(msg_form="voice")  # type: ignore[arg-type]
        with pytest.raises(ValueError, match="bot"):
            FeishuCardChannel(bot="intern")  # type: ignore[arg-type]

    def test_bot_keys_registry_shape(self):
        assert BOT_APP_CREDENTIAL_KEYS == {
            "analyst": ("FEISHU2_APP_ID", "FEISHU2_APP_SECRET")
        }


# ---------------------------------------------------------------------------
# schema 面:msg_form/bot 仅 feishu_card 可配 + Literal 值域
# ---------------------------------------------------------------------------


def _data(**overrides: Any) -> dict[str, Any]:
    base = {
        "id": "demo",
        "name": "Demo",
        "schedule": "0 9 * * *",
        "sources": [{"name": "example", "url": "https://example.com/list?page={page}"}],
    }
    base.update(overrides)
    return base


class TestSchemaFields:
    def test_msg_form_and_bot_load_on_feishu_card(self):
        cfg = load_category(
            _data(
                push=[
                    {
                        "channel": "feishu_card",
                        "target": "env:FEISHU_CHAT_ID",
                        "msg_form": "text",
                        "bot": "analyst",
                    },
                    {"channel": "feishu_card", "target": "env:FEISHU_CHAT_ID"},
                ]
            )
        )
        text_entry, default_entry = cfg.push
        assert (text_entry.msg_form, text_entry.bot) == ("text", "analyst")
        assert (default_entry.msg_form, default_entry.bot) == (
            None,
            None,
        )  # 缺省 card/主机器人

    def test_msg_form_on_wrong_channel_rejected(self):
        with pytest.raises(LoadError) as excinfo:
            load_category(
                _data(
                    push=[
                        {
                            "channel": "bark",
                            "target": "env:BARK_DEVICE_KEY",
                            "msg_form": "text",
                        }
                    ]
                )
            )
        assert any(
            d.error_type == "unexpected_platform_field" for d in excinfo.value.errors
        )

    def test_bot_on_wrong_channel_rejected(self):
        with pytest.raises(LoadError) as excinfo:
            load_category(
                _data(
                    push=[
                        {
                            "channel": "ntfy",
                            "target": "env:NTFY_TARGET",
                            "bot": "analyst",
                        }
                    ]
                )
            )
        assert any(
            d.error_type == "unexpected_platform_field" for d in excinfo.value.errors
        )

    def test_msg_form_literal_values(self):
        with pytest.raises(LoadError) as excinfo:
            load_category(
                _data(
                    push=[
                        {
                            "channel": "feishu_card",
                            "target": "env:FEISHU_CHAT_ID",
                            "msg_form": "voice",
                        }
                    ]
                )
            )
        assert excinfo.value.errors  # Literal 值域拒绝(text|card 之外)


# ---------------------------------------------------------------------------
# 管线下传接线:schema 可选字段经真实 _build_channel 到达通道构造参数
# ---------------------------------------------------------------------------


def test_build_channel_wires_msg_form_and_bot(tmp_path):
    from myssia.pipeline import Pipeline

    cfg = load_category(
        _data(
            push=[
                {
                    "channel": "feishu_card",
                    "target": "env:FEISHU_CHAT_ID",
                    "msg_form": "text",
                    "bot": "analyst",
                }
            ]
        )
    )
    pipeline = Pipeline(
        cfg,
        db_path=tmp_path / "p.db",
        store=SQLiteStore(tmp_path / "p.db"),
        client=httpx.AsyncClient(
            transport=httpx.MockTransport(lambda request: httpx.Response(404, text=""))
        ),
    )
    try:
        channel = pipeline._build_channel(pipeline.config.push[0])
        assert isinstance(channel, FeishuCardChannel)
        assert channel._msg_form == "text"
        assert channel._bot == "analyst"
    finally:
        pipeline.close()
