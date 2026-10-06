"""Tests for the Telegram filter pipeline (10-06-telegram-telethon B2).

覆盖面(design D5 过滤面;grill Q5 决议):

- **粗筛**:默认词表命中/未命中、ASCII 大小写不敏感、显式空词表=关闭、
  自定义词表覆盖(口味配置化);
- **精筛**:LLM 端点未配 = 降级纯粗筛(零 token、条目照常出仓)、注入
  completer 的批量打分解析(id 匹配/夹逼 0-10/坏条目宽容)、端点失败与
  空输出降级、阈值可配(score_threshold=9);
- **出口(组合铁律)**:同轮 N 条高价值 → :func:`merge_high_value` 恰
  1 条(score=组内最高、title 带 N 与阈值、逐条 markdown 明细、合并锚
  随消息 id 区间稳定 → 重拉幂等);
- **引擎集成**:mock getUpdates + fake completer → 最终 items = 1 条
  合并高价值 + 普通条目;无 LLM 配置 → 全部普通出仓。

零真实网络、零真实钥匙串;completer 一律注入 fake(prompt 引擎判例)。
"""

from __future__ import annotations

import json

import httpx
import pytest

from myssia.engines.fetch_base import FetchError
from myssia.engines.telegram import TelegramEngine
from myssia.schema import SourceConfig
from myssia.secrets import SECRET_SERVICE, InMemoryKeychainBackend
from myssia.telegram.filter import (
    DEFAULT_COARSE_KEYWORDS,
    DEFAULT_SCORE_THRESHOLD,
    TelegramFilterConfig,
    TelegramFilterPipeline,
    coarse_hit,
    merge_high_value,
)

from conftest import make_client, make_context, run

CHAT_ID = -1001234567890
SOURCE_URL = "https://api.telegram.org"
BOT_TOKEN = "8000000001:AA_test-token-do-not-leak"


# ---------------------------------------------------------------------------
# fakes
# ---------------------------------------------------------------------------


class FakeCompletion:
    def __init__(self, text: str, total_tokens: int = 120) -> None:
        self.text = text
        self.total_tokens = total_tokens


class FakeCompleter:
    """记录调用的 fake 完成层;可编程返回文本或抛错."""

    def __init__(self, text: str | None = None, error: Exception | None = None) -> None:
        self.text = text
        self.error = error
        self.calls: list[dict] = []

    async def __call__(self, *, model: str, system: str, user: str) -> FakeCompletion:
        self.calls.append({"model": model, "system": system, "user": user})
        if self.error is not None:
            raise self.error
        assert self.text is not None
        return FakeCompletion(self.text)


def make_item(message_id: int, text: str, *, score: int | None = None) -> dict:
    item = {
        "url": f"{SOURCE_URL}#tg-{CHAT_ID}-{message_id}",
        "title": text[:100],
        "content": text,
        "author": "@alice",
        "chat_id": CHAT_ID,
        "message_id": message_id,
    }
    if score is not None:
        item["score"] = score
    return item


def scores_answer(*pairs: tuple[int, int]) -> str:
    """LLM 应答 fake JSON:[{"id": n, "score": s, "reason": …}, …]."""
    return json.dumps(
        [{"id": item_id, "score": score, "reason": "fake"} for item_id, score in pairs],
        ensure_ascii=False,
    )


# ---------------------------------------------------------------------------
# 粗筛
# ---------------------------------------------------------------------------


def test_default_keywords_cover_freebie_appetite():
    """内置缺省词表覆盖免费/token/额度/优惠/白嫖(任务口径)."""
    for word in ("免费", "白嫖", "羊毛", "token", "额度", "优惠", "coupon", "free"):
        assert word in DEFAULT_COARSE_KEYWORDS


def test_coarse_hit_case_insensitive_and_miss():
    assert coarse_hit("FREE tier 扩容", ["free"]) == "free"
    assert coarse_hit("捡到 Coupon 一枚", ["coupon"]) == "coupon"
    assert coarse_hit("今天天气不错", DEFAULT_COARSE_KEYWORDS) is None
    assert coarse_hit("任意文本", []) is None  # 空词表 = 关闭粗筛面
    assert coarse_hit("  ", ["免费"]) is None


def test_pipeline_coarse_split():
    pipeline = TelegramFilterPipeline(TelegramFilterConfig())
    outcome = run(
        pipeline.process(
            [
                make_item(1, "OpenAI 免费额度来了"),
                make_item(2, "今天午饭吃什么"),
                make_item(3, "无关灌水"),
            ]
        )
    )
    assert outcome.coarse_hits == 1
    assert outcome.coarse_misses == 2
    assert [item["message_id"] for item in outcome.normal] == [1]
    assert outcome.high_value == []
    assert outcome.degraded and outcome.degrade_reason == "llm_not_configured"


def test_custom_keywords_override_default_appetite():
    """口味配置化:自定义词表替换缺省(游戏口味也能筛)."""
    pipeline = TelegramFilterPipeline(TelegramFilterConfig(keywords=("喜加一", "0元")))
    outcome = run(
        pipeline.process(
            [make_item(1, "Epic 喜加一速抢"), make_item(2, "免费 API 额度")]
        )
        # ↑ 免费命中缺省词表,但自定义词表下未命中 → 零痕迹跳过
    )
    assert outcome.coarse_hits == 1
    assert outcome.normal[0]["message_id"] == 1


# ---------------------------------------------------------------------------
# 精筛(LLM 挂点)
# ---------------------------------------------------------------------------


def test_fine_scoring_routes_high_and_normal():
    """打分分流:9 分高价值、6 分普通(带 score);7→缺答宽容普通."""
    completer = FakeCompleter(scores_answer((1, 9), (2, 6)))
    pipeline = TelegramFilterPipeline(
        TelegramFilterConfig(llm_base_url="env:X", llm_api_key="env:Y"),
        completer=completer,
    )
    outcome = run(
        pipeline.process(
            [
                make_item(1, "免费 token 双倍"),
                make_item(2, "常规优惠推送"),
                make_item(3, "免费但模型没答"),
            ]
        )
    )
    assert outcome.coarse_hits == 3
    assert outcome.scored == 2
    assert not outcome.degraded
    assert [item["message_id"] for item in outcome.high_value] == [1]
    assert [item["message_id"] for item in outcome.normal] == [2, 3]
    assert outcome.normal[0]["score"] == 6
    assert "score" not in outcome.normal[1]
    # user 消息带编号清单,system 是打分口径
    assert "[id 1]" in completer.calls[0]["user"]
    assert "0-10" in completer.calls[0]["system"]


def test_score_clamped_to_zero_ten_and_model_name_passthrough():
    completer = FakeCompleter(scores_answer((1, 15), (2, -3)))
    pipeline = TelegramFilterPipeline(
        TelegramFilterConfig(
            model="glm-4-flash", llm_base_url="env:X", llm_api_key="env:Y"
        ),
        completer=completer,
    )
    outcome = run(
        pipeline.process([make_item(1, "免费 a"), make_item(2, "免费 b")])
    )
    assert {item["message_id"]: item["score"] for item in outcome.high_value} == {1: 10}
    assert outcome.normal[0]["score"] == 0
    assert completer.calls[0]["model"] == "glm-4-flash"


def test_threshold_configurable():
    """阈值可配:score_threshold=9 时 8 分降为普通."""
    completer = FakeCompleter(scores_answer((1, 8)))
    pipeline = TelegramFilterPipeline(
        TelegramFilterConfig(
            score_threshold=9, llm_base_url="env:X", llm_api_key="env:Y"
        ),
        completer=completer,
    )
    outcome = run(pipeline.process([make_item(1, "免费 a")]))
    assert outcome.high_value == []
    assert outcome.normal[0]["score"] == 8


def test_llm_failure_degrades_to_coarse_only(caplog):
    """端点炸/空输出 → 降级纯粗筛:全部普通出仓,WARNING 留痕,不抛."""
    pipeline = TelegramFilterPipeline(
        TelegramFilterConfig(llm_base_url="env:X", llm_api_key="env:Y"),
        completer=FakeCompleter(error=RuntimeError("endpoint down")),
    )
    with caplog.at_level("WARNING", logger="myssia.telegram.filter"):
        outcome = run(pipeline.process([make_item(1, "免费 a")]))
    assert outcome.degraded and outcome.degrade_reason == "llm_failed"
    assert [item["message_id"] for item in outcome.normal] == [1]
    assert "降级" in caplog.text


def test_malformed_llm_output_degrades():
    pipeline = TelegramFilterPipeline(
        TelegramFilterConfig(llm_base_url="env:X", llm_api_key="env:Y"),
        completer=FakeCompleter(text="模型今天不想说话"),
    )
    outcome = run(pipeline.process([make_item(1, "免费 a")]))
    assert outcome.degraded and outcome.degrade_reason == "llm_failed"
    assert len(outcome.normal) == 1


def test_fenced_json_output_parsed():
    """markdown 围栏包裹的 JSON 也认(extract_json_entries 宽容契约)."""
    completer = FakeCompleter("```json\n" + scores_answer((1, 10)) + "\n```")
    pipeline = TelegramFilterPipeline(
        TelegramFilterConfig(llm_base_url="env:X", llm_api_key="env:Y"),
        completer=completer,
    )
    outcome = run(pipeline.process([make_item(1, "免费 a")]))
    assert len(outcome.high_value) == 1


def test_unresolvable_endpoint_refs_degrade(caplog):
    """引用在而钥匙串未写 → llm_failed 降级(不是空态:精筛是增强件)."""
    backend = InMemoryKeychainBackend()  # 空:未写 llm 键
    pipeline = TelegramFilterPipeline(
        TelegramFilterConfig(
            llm_base_url="keychain:myia/llm/base_url",
            llm_api_key="keychain:myia/llm/api_key",
        ),
        keychain_backend=backend,
    )
    with caplog.at_level("WARNING", logger="myssia.telegram.filter"):
        outcome = run(pipeline.process([make_item(1, "免费 a")]))
    assert outcome.degraded and outcome.degrade_reason == "llm_failed"
    assert len(outcome.normal) == 1


# ---------------------------------------------------------------------------
# 出口:同轮多条高价值合并单条(组合铁律)
# ---------------------------------------------------------------------------


def test_merge_high_value_n_items_into_exactly_one():
    """同轮 N 条高价值 → 恰 1 条:title/content/score/锚区间."""
    merged = merge_high_value(
        [
            make_item(101, "免费 token 500w", score=8),
            make_item(102, "白嫖 GPT-5 一年", score=10),
            make_item(103, "优惠码 MOLI", score=9),
        ]
    )
    assert merged is not None
    assert merged["merged_count"] == 3
    assert merged["score"] == 10  # 组内最高(route score>=8 直接过)
    assert merged["title"] == "Telegram 高价值 3 条(score≥8)"
    assert merged["merged_message_ids"] == [101, 102, 103]
    assert merged["url"] == f"{SOURCE_URL}#tg-{CHAT_ID}-101-hv3-103"
    # content:逐条明细(分数/作者/文本)
    assert "[10分] @alice: 白嫖 GPT-5 一年" in merged["content"]
    assert merged["content"].count("\n") == 2


def test_merge_high_value_anchor_is_idempotent_per_window():
    """合并锚随消息 id 区间稳定:同窗口重拉同批 → 同 URL → dedup 幂等."""
    batch = [make_item(201, "免费 a", score=9), make_item(205, "免费 b", score=8)]
    first = merge_high_value(batch)
    second = merge_high_value(list(reversed(batch)))  # 顺序不稳也不怕(按 url 排序)
    assert first is not None and second is not None
    assert first["url"] == second["url"]


def test_merge_high_value_empty_is_none():
    assert merge_high_value([]) is None


def test_pipeline_to_merged_flow_same_round_n_items_one_output():
    """端到端口径:同轮 5 条(2 高 + 1 低分普通 + 1 缺答普通 + 1 未命中)
    → 出仓恰 3 条,其中高价值面**恰 1 条**合并条目(组合铁律)。"""
    completer = FakeCompleter(scores_answer((1, 9), (2, 10), (3, 7)))
    pipeline = TelegramFilterPipeline(
        TelegramFilterConfig(llm_base_url="env:X", llm_api_key="env:Y"),
        completer=completer,
    )
    outcome = run(
        pipeline.process(
            [
                make_item(1, "免费 token"),
                make_item(2, "白嫖额度"),
                make_item(3, "优惠小件"),
                make_item(4, "免费常规"),
                make_item(5, "纯闲聊"),
            ]
        )
    )
    merged = merge_high_value(outcome.high_value)
    final = ([merged] if merged else []) + outcome.normal
    assert len(final) == 3  # 1 合并 + 2 普通(7 分/缺答)
    assert final[0]["score"] == 10
    assert final[0]["merged_count"] == 2
    assert final[1]["message_id"] == 3
    assert final[1]["score"] == 7
    assert final[2]["message_id"] == 4
    assert "score" not in final[2]


# ---------------------------------------------------------------------------
# 引擎集成(mock getUpdates + fake completer)
# ---------------------------------------------------------------------------


def telegram_bot_client(responses: list[httpx.Response]) -> httpx.AsyncClient:
    """单宿主 mock:依次应答(窗口/确认),offset 请求应答空窗口."""
    queue = list(responses)

    def handler(request: httpx.Request) -> httpx.Response:
        if "offset=" in str(request.url):
            return httpx.Response(200, json={"ok": True, "result": []})
        return queue.pop(0) if queue else httpx.Response(200, json={"ok": True, "result": []})

    return make_client(handler)


def build_engine(completer, options: dict) -> tuple[TelegramEngine, object]:
    payload = {
        "ok": True,
        "result": [
            {
                "update_id": 11,
                "message": {
                    "message_id": 101,
                    "date": 1761000000.0,
                    "chat": {"id": CHAT_ID, "type": "supergroup", "title": "g"},
                    "text": "OpenAI 免费额度翻倍速领",
                    "from": {"id": 1, "username": "alice"},
                },
            },
            {
                "update_id": 12,
                "message": {
                    "message_id": 102,
                    "date": 1761000060.0,
                    "chat": {"id": CHAT_ID, "type": "supergroup", "title": "g"},
                    "text": "白嫖 Claude Pro 一年 速抢",
                    "from": {"id": 2, "username": "bob"},
                },
            },
            {
                "update_id": 13,
                "message": {
                    "message_id": 103,
                    "date": 1761000120.0,
                    "chat": {"id": CHAT_ID, "type": "supergroup", "title": "g"},
                    "text": "常规优惠推送一枚",
                    "from": {"id": 3, "username": "carol"},
                },
            },
        ],
    }
    client = telegram_bot_client([httpx.Response(200, json=payload)])
    context, _ = make_context(client)
    backend = InMemoryKeychainBackend()
    backend.set_password(SECRET_SERVICE, "myia/telegram/bot-token", BOT_TOKEN)
    context.keychain_backend = backend
    source = SourceConfig.model_validate(
        {
            "name": "telegram-g",
            "engine": "telegram",
            "url": SOURCE_URL,
            "engine_options": {"telegram": {"chat_id": str(CHAT_ID), **options}},
        }
    )
    return TelegramEngine(source, context, completer=completer), backend


def test_engine_end_to_end_merged_single_item_with_scores():
    """引擎集成:同轮 3 命中(2 高 1 普)→ items 恰 2 条,高价值恰 1 条."""
    completer = FakeCompleter(scores_answer((1, 9), (2, 10), (3, 6)))
    engine, _ = build_engine(
        completer,
        {
            "llm_base_url": "keychain:myia/llm/base_url",
            "llm_api_key": "keychain:myia/llm/api_key",
        },
    )
    # LLM 端点引用在(成对)但走注入 completer —— 真端点不会被触碰
    items = run(engine.fetch())
    assert len(items) == 2
    merged = items[0]
    assert merged["score"] == 10
    assert merged["merged_count"] == 2
    assert merged["url"] == f"{SOURCE_URL}#tg-{CHAT_ID}-101-hv2-102"
    assert "9分" in merged["content"] and "10分" in merged["content"]
    normal = items[1]
    assert normal["message_id"] == 103
    assert normal["score"] == 6


def test_engine_without_llm_refs_degrades_to_all_normal(caplog):
    """精筛端点未配 → 降级纯粗筛:命中全部普通出仓(route archive 入库)."""
    engine, _ = build_engine(FakeCompleter(), {})
    with caplog.at_level("INFO", logger="myssia.telegram.filter"):
        items = run(engine.fetch())
    assert len(items) == 3
    assert all("score" not in item for item in items)
    assert "降级纯粗筛" in caplog.text


@pytest.mark.parametrize(
    ("options", "fragment"),
    [
        ({"keywords": "免费"}, "keywords"),
        ({"keywords": [1, 2]}, "keywords"),
        ({"score_threshold": 0}, "score_threshold"),
        ({"score_threshold": 11}, "score_threshold"),
        ({"model": ""}, "model"),
        ({"llm_base_url": "keychain:myia/llm/base_url"}, "成对"),
        ({"llm_api_key": "keychain:myia/llm/api_key"}, "成对"),
        ({"llm_base_url": "https://plain.example/v1", "llm_api_key": "env:LLM_KEY"}, "明文"),
        ({"timeout": -1}, "timeout"),
    ],
)
def test_engine_filter_options_structural_rejection(options, fragment):
    """过滤面配置错误 = invalid_engine_options(半配/明文/越界全拒)."""
    engine, _ = build_engine(FakeCompleter(), options)
    with pytest.raises(FetchError) as excinfo:
        run(engine.fetch())
    assert excinfo.value.error_type == "invalid_engine_options"
    assert fragment in str(excinfo.value)
