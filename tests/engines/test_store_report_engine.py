"""Tests for the store-report engine(10-06-hermes-align 批次4).

跨品类合并日报(Hermes 版式):store 本槽位窗查询 → 分区渲染 → 单条目
出仓;全分区无新内容 = 零条目静默(skip 哨兵留痕)。测试全 mock(内存
SQLiteStore 种子数据 + now_fn 控时 + MockTransport 飞书通道),零真网。

用例面:

1. registry/链外语义与 schema 词表(store_report 在册、AUTO_CHAIN 不在、
   auto_degrade 单级链、EngineName 词表收词);
2. options 校验:sections 形状/未知字段/style 词表/labels/suffix_fields/
   数值区间/timezone;
3. slot_window:AM/PM 边界(本地 12:00 界,dedup 同界);
4. 版式渲染快照:头行/分区/编号/--分隔线/缩进明细/省略留痕/尾戳原文;
   空分区跳过、全空返回空串;
5. normalize_detail_line:markdown 结构符剥除(防飞书 md 把缩进行渲染成
   标题/列表);
6. 引擎 fetch:store 缺席结构化拒;空窗静默(skip 哨兵);正常路径单条目
   (锚点 #report-<日期>-<槽位>、content=report_markdown、标签/句尾链接/
   suffix 价格);截断帽;detail 分区行帽;
7. pagination/extract 配置结构化拒(单报表语义);
8. 超长报表过 feishu msg_form text:行边界续段头尾 (i/N)(通道层护栏,
   组合铁律不在引擎层重做);
9. 既有品类路由降噪:ai-news/games/ai-vendor-watch 的 YAML 路由对代表
   条目落 archive/immediate,grep 面无 mode: digest 残留(daily-digest
   成为唯一日报出口)。
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from zoneinfo import ZoneInfo

import httpx
import pytest

from conftest import make_client, make_context, make_source, run

from myssia.engines.fetch_base import FetchContext, FetchError
from myssia.engines.registry import (
    AUTO_CHAIN,
    ENGINE_REGISTRY,
    auto_degrade,
    resolve_engine,
)
from myssia.engines.store_report import (
    DEFAULT_MAX_ENTRIES,
    FOOTER_TEMPLATE,
    SKIP_WINDOW_EMPTY,
    DigestEntry,
    DigestSection,
    StoreReportEngine,
    clip_title,
    normalize_detail_line,
    render_report,
    slot_window,
)
from myssia.push import SendContext
from myssia.push.route import resolve_route, routes_from_config
from myssia.schema import ENGINES, load_category_file
from myssia.store import SQLiteStore
from myssia.store.models import ItemRecord

PLUGINS = Path(__file__).resolve().parents[2] / "plugins"
TZ_SHANGHAI = ZoneInfo("Asia/Shanghai")
NOW_PM = datetime(2026, 10, 6, 20, 30, tzinfo=TZ_SHANGHAI)  # PM 槽,窗口起 12:00
NOW_AM = datetime(2026, 10, 6, 8, 5, tzinfo=TZ_SHANGHAI)  # AM 槽,窗口起 00:00

SECTIONS: list[dict[str, Any]] = [
    {
        "title": "AI 资讯",
        "sources": ["aihot", "openai-news"],
        "labels": {"openai-news": "OpenAI"},
        "max_entries": 5,
    },
    {
        "title": "AI 厂商官网",
        "sources": ["ai-vendor-watch"],
        "style": "detail",
        "max_lines": 3,
    },
    {"title": "游戏喜加一与折扣", "sources": ["epic-free"], "suffix_fields": ["price_text"]},
]


def report_options(**overrides: Any) -> dict[str, Any]:
    base: dict[str, Any] = {
        "title": "情报日报",
        "timezone": "Asia/Shanghai",
        "sections": SECTIONS,
    }
    base.update(overrides)
    return base


def report_source(**overrides: Any) -> Any:
    data: dict[str, Any] = {
        "name": "daily-digest",
        "engine": "store_report",
        "url": "https://myia.local/daily-digest",
        "engine_options": {"store_report": report_options()},
    }
    data.update(overrides)
    return make_source(**data)


def make_engine(
    store: SQLiteStore | None,
    *,
    now: datetime = NOW_PM,
    options: dict[str, Any] | None = None,
) -> StoreReportEngine:
    """直构引擎(store 注入 + 墙钟钉死;零 HTTP——MockTransport 兜 robots 缺省)."""
    data: dict[str, Any] = {
        "name": "daily-digest",
        "engine": "store_report",
        "url": "https://myia.local/daily-digest",
    }
    if options is None:
        options = report_options()
    data["engine_options"] = {"store_report": options}
    source = make_source(**data)
    context, _clock = make_context(make_client(lambda request: httpx.Response(404)), store=store)
    return StoreReportEngine(source, context, now_fn=lambda: now)


def seed(
    store: SQLiteStore,
    *,
    source: str,
    title: str,
    url: str,
    first_seen: datetime,
    content: str | None = None,
    raw: dict[str, Any] | None = None,
) -> None:
    store.save_item(
        ItemRecord(
            url=url,
            dedup_key=f"{url}#k",
            title=title,
            source=source,
            content=content,
            raw=raw or {},
            first_seen=first_seen,
        )
    )


IN_WINDOW_PM = datetime(2026, 10, 6, 6, 0, tzinfo=timezone.utc)  # 14:00 +08 = PM 窗内
OUT_WINDOW = datetime(2026, 10, 5, 6, 0, tzinfo=timezone.utc)  # 昨日 = 窗外


@pytest.fixture()
def store(tmp_path):
    return SQLiteStore(tmp_path / "report.db")


# --------------------------------------------------------------- 词表与链外


def test_registered_off_chain_and_schema_vocab():
    """store_report 在册、AUTO_CHAIN 不在、auto 单级链、schema 词表收词."""
    assert "store_report" in ENGINE_REGISTRY
    assert "store_report" not in AUTO_CHAIN
    assert auto_degrade("store_report") == ["store_report"]
    assert resolve_engine("store_report") is StoreReportEngine
    assert "store_report" in ENGINES
    report_source()  # schema 接受显式 engine: store_report


# ----------------------------------------------------------------- options


@pytest.mark.parametrize(
    ("overrides", "fragment"),
    [
        ({"sections": None}, "sections"),
        ({"sections": []}, "sections"),
        ({"sections": [{"title": "x"}]}, "sources"),
        ({"sections": [{"sources": ["a"]}]}, "title"),
        ({"sections": [{"title": "x", "sources": ["a"], "style": "table"}]}, "style"),
        ({"sections": [{"title": "x", "sources": ["a"], "labels": ["OpenAI"]}]}, "labels"),
        (
            {"sections": [{"title": "x", "sources": ["a"], "suffix_fields": [1]}]},
            "suffix_fields",
        ),
        (
            {"sections": [{"title": "x", "sources": ["a"], "max_entries": 0}]},
            "max_entries",
        ),
        ({"sections": [{"title": "x", "sources": ["a"], "max_lines": 999}]}, "max_lines"),
        (
            {"sections": [{"title": "x", "sources": ["a"], "unknown": 1}]},
            "未知字段",
        ),
        ({"timezone": "Mars/Olympus"}, "IANA 时区名"),
        ({"max_chars_per_title": 3}, "max_chars_per_title"),
    ],
)
def test_options_rejected(store, overrides, fragment):
    engine = make_engine(store, options=report_options(**overrides))
    with pytest.raises(FetchError, match=fragment) as excinfo:
        run(engine.fetch())
    assert excinfo.value.error_type == "invalid_engine_options"


def test_options_reject_bad_section_type(store):
    engine = make_engine(store, options=report_options(sections=["nope"]))
    with pytest.raises(FetchError, match="sections\\[0\\]"):
        run(engine.fetch())


# ---------------------------------------------------------------- 槽位窗口


def test_slot_window_am_pm_boundary():
    slot, start, date = slot_window(NOW_AM, TZ_SHANGHAI)
    assert (slot, date) == ("am", "2026-10-06")
    assert start == datetime(2026, 10, 6, 0, 0, tzinfo=TZ_SHANGHAI)

    slot, start, date = slot_window(NOW_PM, TZ_SHANGHAI)
    assert (slot, date) == ("pm", "2026-10-06")
    assert start == datetime(2026, 10, 6, 12, 0, tzinfo=TZ_SHANGHAI)

    # 12:00 整 = PM(dedup SLOT_BOUNDARY_HOUR 同界:hour < 12 才是 AM)
    slot, start, _ = slot_window(datetime(2026, 10, 6, 12, 0, tzinfo=TZ_SHANGHAI), TZ_SHANGHAI)
    assert slot == "pm"
    assert start.hour == 12


# ----------------------------------------------------------------- 版式渲染


def test_render_report_layout_snapshot():
    """版式快照:头行/分区/编号/--/缩进明细/尾戳;空分区整段跳过."""
    sections = [
        DigestSection(
            title="AI 资讯",
            entries=[
                DigestEntry(
                    head="OpenAI 发布 GPT-5.5",
                    url="https://openai.com/blog/x",
                    label="OpenAI",
                ),
                DigestEntry(head="智谱开源 CogAgent"),
            ],
        ),
        DigestSection(
            title="AI 厂商官网",
            style="detail",
            entries=[
                DigestEntry(
                    head="AI 厂商官网日报",
                    details=["OpenAI 发布新模型", "Anthropic 无明显动态"],
                )
            ],
        ),
        DigestSection(title="空分区", entries=[]),
    ]
    rendered = render_report(
        sections,
        title="情报日报",
        date="2026-10-06",
        slot="pm",
        generated_at=NOW_PM,
    )
    assert rendered == "\n".join(
        [
            "情报日报 · 2026-10-06 · PM",
            "AI 资讯",
            "1. [OpenAI] OpenAI 发布 GPT-5.5 [原文](https://openai.com/blog/x)",
            "2. 智谱开源 CogAgent",
            "--",
            "AI 厂商官网",
            "1. AI 厂商官网日报",
            "   · OpenAI 发布新模型",
            "   · Anthropic 无明显动态",
            "20:30 实时爬取生成 · 全条目指纹去重 · 无新内容自动静默",
        ]
    )


def test_render_report_suffix_and_omitted():
    sections = [
        DigestSection(
            title="游戏",
            entries=[DigestEntry(head="Control", url="https://epic/x", suffix="¥0.00")],
            omitted=7,
        )
    ]
    rendered = render_report(
        sections, title="情报日报", date="2026-10-06", slot="am", generated_at=NOW_AM
    )
    assert "1. Control · ¥0.00 [原文](https://epic/x)" in rendered
    assert "   ……(另有 7 条省略)" in rendered
    assert FOOTER_TEMPLATE.format(time="08:05") in rendered


def test_render_report_all_empty_returns_empty_string():
    sections = [DigestSection(title="A", entries=[]), DigestSection(title="B", entries=[])]
    assert render_report(
        sections, title="t", date="d", slot="am", generated_at=NOW_AM
    ) == ""


def test_normalize_detail_line_strips_markdown_structure():
    assert normalize_detail_line("## 厂商要闻") == "厂商要闻"
    assert normalize_detail_line("- OpenAI 发布新模型") == "OpenAI 发布新模型"
    assert normalize_detail_line("**加粗**条目") == "加粗条目"
    assert normalize_detail_line("   ") is None
    assert normalize_detail_line("  ") is None


def test_clip_title_single_line_and_ellipsis():
    assert clip_title("  多行\n标题  ", 80) == "多行 标题"
    assert clip_title("长" * 100, 10) == "长" * 9 + "…"


# -------------------------------------------------------------------- fetch


def test_fetch_requires_store():
    engine = make_engine(None, options=report_options())
    with pytest.raises(FetchError, match="store") as excinfo:
        run(engine.fetch())
    assert excinfo.value.error_type == "store_not_available"


def test_fetch_silent_when_window_empty(store):
    seed(store, source="aihot", title="旧条目", url="https://old/x", first_seen=OUT_WINDOW)
    engine = make_engine(store)
    items = run(engine.fetch())
    assert items == []
    assert engine.last_skip_reason == SKIP_WINDOW_EMPTY


def test_fetch_renders_one_item_with_hermes_layout(store):
    seed(
        store,
        source="aihot",
        title="热点:多模态新模型刷屏",
        url="https://aihot/x",
        first_seen=IN_WINDOW_PM,
    )
    seed(
        store,
        source="openai-news",
        title="OpenAI announces GPT-5.5",
        url="https://openai/x",
        first_seen=IN_WINDOW_PM,
    )
    seed(  # 窗外旧条目不得混入
        store, source="openai-news", title="旧闻", url="https://openai/old", first_seen=OUT_WINDOW
    )
    seed(  # 不在任何分区的源不得混入
        store,
        source="wool-forum",
        title="羊毛闲聊",
        url="https://wool/x",
        first_seen=IN_WINDOW_PM,
    )
    seed(  # detail 分区:LLM 摘要 markdown 归一缩进
        store,
        source="ai-vendor-watch",
        title="AI 厂商官网日报",
        url="https://vendor/x",
        first_seen=IN_WINDOW_PM,
        content="## 厂商要闻\n\n- OpenAI:发布新模型\n- Anthropic:无明显动态",
    )
    seed(  # suffix 分区:游戏价格附注
        store,
        source="epic-free",
        title="Control 终极版",
        url="https://epic/control",
        first_seen=IN_WINDOW_PM,
        raw={"price_text": "¥0.00"},
    )
    engine = make_engine(store)
    items = run(engine.fetch())
    assert len(items) == 1
    item = items[0]
    # 锚点 = 日期+槽位(#prompt- 判例):同槽幂等、跨槽必新。
    assert item["url"] == "https://myia.local/daily-digest#report-20261006-pm"
    assert item["title"] == "情报日报"
    assert item["content"] == item["report_markdown"]
    assert item["report_slot"] == "pm"
    assert item["report_entries"] == 4
    lines = item["report_markdown"].splitlines()
    assert lines[0] == "情报日报 · 2026-10-06 · PM"
    # aihot 在测试 SECTIONS 里没配 label → 无前缀;openai-news 配了 OpenAI 前缀。
    assert "热点:多模态新模型刷屏 [原文](https://aihot/x)" in item["report_markdown"]
    assert "[OpenAI] OpenAI announces GPT-5.5 [原文](https://openai/x)" in item["report_markdown"]
    assert "旧闻" not in item["report_markdown"]
    assert "羊毛闲聊" not in item["report_markdown"]
    # detail 分区:markdown 结构符剥除 + 三空格缩进 + · 前缀。
    assert "1. AI 厂商官网日报" in item["report_markdown"]
    assert "   · 厂商要闻" in item["report_markdown"]
    assert "   · OpenAI:发布新模型" in item["report_markdown"]
    assert "   · Anthropic:无明显动态" in item["report_markdown"]
    # suffix 分区:price_text 首个非空值作句尾附注。
    assert "Control 终极版 · ¥0.00 [原文](https://epic/control)" in item["report_markdown"]
    # 分区之间 -- 分隔线。
    assert "--" in item["report_markdown"]
    # 尾戳原文(生成时间来自注入墙钟)。
    assert FOOTER_TEMPLATE.format(time="20:30") in item["report_markdown"]


def test_fetch_detail_line_cap(store):
    content = "\n".join(f"- 厂商{i}:更新" for i in range(10))
    seed(
        store,
        source="ai-vendor-watch",
        title="日报",
        url="https://vendor/x",
        first_seen=IN_WINDOW_PM,
        content=content,
    )
    engine = make_engine(store)
    items = run(engine.fetch())
    details = [
        line
        for line in items[0]["report_markdown"].splitlines()
        if line.startswith("   · ")
    ]
    assert len(details) == 4  # max_lines=3 + 省略行
    assert details[-1] == "   · ……(明细超长省略)"


def test_fetch_section_entry_cap(store):
    for index in range(DEFAULT_MAX_ENTRIES + 3):
        seed(
            store,
            source="aihot",
            title=f"条目{index}",
            url=f"https://aihot/{index}",
            first_seen=IN_WINDOW_PM,
        )
    engine = make_engine(store)  # AI 资讯分区 max_entries=5(SECTIONS 钉值)
    items = run(engine.fetch())
    markdown = items[0]["report_markdown"]
    numbered = [line for line in markdown.splitlines() if line[:2] in {"1.", "2.", "3.", "4.", "5."}]
    assert len(numbered) == 5
    assert f"   ……(另有 {DEFAULT_MAX_ENTRIES + 3 - 5} 条省略)" in markdown


def test_fetch_am_window_excludes_pm_items(store):
    """AM 窗只看 00:00 起:昨日 PM 条目(12:00 后入库)不进今晨报表."""
    yesterday_pm = datetime(2026, 10, 5, 14, 0, tzinfo=timezone.utc)  # 22:00 +08 昨日
    seed(
        store, source="aihot", title="昨夜条目", url="https://old/pm", first_seen=yesterday_pm
    )
    engine = make_engine(store, now=NOW_AM)
    items = run(engine.fetch())
    assert items == []
    assert engine.last_skip_reason == SKIP_WINDOW_EMPTY


def test_fetch_rejects_pagination_and_extract(store):
    paginated = make_source(
        name="daily-digest",
        engine="store_report",
        url="https://myia.local/daily-digest/{page}",
        engine_options={"store_report": report_options()},
        pagination={"mode": "template", "max_pages": 2},
    )
    context, _clock = make_context(
        make_client(lambda request: httpx.Response(404)), store=store
    )
    engine = StoreReportEngine(paginated, context, now_fn=lambda: NOW_PM)
    with pytest.raises(FetchError, match="pagination"):
        run(engine.fetch())


# ------------------------------------------- 超长报表:feishu text 续段 (i/N)


def _feishu_mock(calls: list[dict[str, Any]]) -> httpx.MockTransport:
    def handler(request: httpx.Request) -> httpx.Response:
        body = json.loads(request.content.decode("utf-8")) if request.content else {}
        calls.append({"url": str(request.url), "body": body})
        return httpx.Response(200, json={"code": 0, "msg": "success", "data": {}})

    return httpx.MockTransport(handler)


def test_long_report_splits_into_marker_segments(store, monkeypatch):
    """超 4000 字报表过 msg_form text:行边界续段,头尾 (i/N)(通道层护栏)."""
    from myssia.push.feishu_card import POST_SPLIT_THRESHOLD, FeishuCardChannel

    monkeypatch.setenv("MYIA_TEST_CHAT_ID", "oc_test")
    # 60 条长标题条目 + 分区帽放开 → 渲染必然超 POST_SPLIT_THRESHOLD。
    long_options = report_options(
        sections=[
            {
                "title": "AI 资讯",
                "sources": ["aihot"],
                "max_entries": 100,
            }
        ]
    )
    for index in range(60):
        seed(
            store,
            source="aihot",
            title=f"超长报表第 {index} 条:标题占位 " + "字" * 60,
            url=f"https://aihot/long/{index}",
            first_seen=IN_WINDOW_PM,
        )
    engine = make_engine(store, options=long_options)
    items = run(engine.fetch())
    assert len(items) == 1
    assert len(items[0]["report_markdown"]) > POST_SPLIT_THRESHOLD

    calls: list[dict[str, Any]] = []
    channel = FeishuCardChannel(
        target="env:MYIA_TEST_CHAT_ID",
        token="t-injected",
        msg_form="text",
        template="{{ items[0].report_markdown }}",
        client=httpx.AsyncClient(transport=_feishu_mock(calls)),
    )

    async def _send() -> None:
        await channel.send(
            items,
            SendContext(slot="pm", date="2026-10-06", category="每日合并日报", kind="immediate"),
        )

    run(_send())
    posts = [c for c in calls if c["url"].startswith("https://open.feishu.cn")]
    assert len(posts) >= 2
    total = len(posts)
    for index, post in enumerate(posts, start=1):
        assert post["body"]["msg_type"] == "post"
        content = json.loads(post["body"]["content"])
        rows = content["zh_cn"]["content"]
        text = rows[0][0]["text"]
        marker = f"({index}/{total})"
        assert text.startswith(marker), "段头指示"
        # 段尾指示:末段尾戳之后还有通道层 CARD_FOOTER 注记,按出现次数断言
        # (头尾各一处 = 2)。
        assert text.count(marker) == 2, "段尾指示"
    # 首段含头行,末段含尾戳(报表自身 footer 行)。
    first_text = json.loads(posts[0]["body"]["content"])["zh_cn"]["content"][0][0]["text"]
    last_text = json.loads(posts[-1]["body"]["content"])["zh_cn"]["content"][0][0]["text"]
    assert "情报日报 · 2026-10-06 · PM" in first_text
    assert "实时爬取生成" in last_text


# ------------------------------------------------- 既有品类路由降噪(批次4)


def _routes_of(yaml_name: str, push_index: int = 0) -> list[Any]:
    config = load_category_file(PLUGINS / f"{yaml_name}.yaml")
    return routes_from_config(config.push[push_index].route)


@pytest.mark.parametrize(
    ("item", "mode"),
    [
        ({"url": "https://x/1", "title": "t", "category": "ai-news"}, "archive"),
        (
            {"url": "https://x/2", "title": "t", "category": "ai-news", "score": 9.2},
            "immediate",
        ),
        (
            {"url": "https://x/3", "title": "t", "category": "freebie"},
            "immediate",
        ),
    ],
)
def test_ai_news_route_noise_reduction(item, mode):
    """ai-news:普通条目落 archive(合并日报收口),score≥9/白给保留 immediate."""
    assert resolve_route(item, _routes_of("ai-news")).mode == mode


@pytest.mark.parametrize(
    ("item", "mode"),
    [
        ({"url": "https://s/1", "title": "t", "final_price": 0}, "immediate"),
        ({"url": "https://s/2", "title": "t", "final_price": 1360}, "archive"),
        ({"url": "https://s/3", "title": "t", "sale_price": "0.50"}, "archive"),
    ],
)
def test_games_route_noise_reduction(item, mode):
    """games 双通道:限免保留 immediate,付费折扣落 archive(双条目同构)."""
    for push_index in (0, 1):
        assert resolve_route(item, _routes_of("games", push_index)).mode == mode


def test_vendor_watch_route_noise_reduction():
    """ai-vendor-watch:整条 archive(日报由合并日报分区承担,原 immediate 退役)."""
    rules = _routes_of("ai-vendor-watch")
    assert resolve_route({"url": "https://v/1", "title": "t"}, rules).mode == "archive"


def test_no_digest_mode_left_in_daily_outlet_categories():
    """grep 面:三品类路由无 mode: digest 残留(daily-digest 是唯一日报出口)."""
    for name in ("ai-news", "games", "ai-vendor-watch"):
        text = (PLUGINS / f"{name}.yaml").read_text(encoding="utf-8")
        assert "mode: digest" not in text, f"{name}.yaml 仍有 digest 路由残留"
        config = load_category_file(PLUGINS / f"{name}.yaml")
        for push in config.push:
            assert all(rule.mode != "digest" for rule in routes_from_config(push.route))


def test_daily_digest_plugin_loads_with_store_report():
    config = load_category_file(PLUGINS / "daily-digest.yaml")
    assert config.id == "daily-digest"
    assert config.sources[0].engine == "store_report"
    assert config.push[0].msg_form == "text"
    options = config.sources[0].extra_params["engine_options"]["store_report"]
    assert {section["title"] for section in options["sections"]} >= {
        "AI 资讯",
        "AI 厂商官网",
        "游戏喜加一与折扣",
    }
