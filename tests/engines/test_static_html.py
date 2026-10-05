"""Tests for the L2 static_html engine (PRD 10-01-v01-engine-l1-l2).

Covers: list extraction with @href/@src attribute fields + relative-URL
resolution / item single-page mode / gb18030 decoding (meta charset, no HTTP
charset) / template pagination with max_pages cap and empty-page stop /
selector pagination (follow, stop without next, loop guard) / change
fingerprint skip / unsupported extract type / trafilatura 正文兜底
(10-05-trafilatura-impl:三分触发①② + 质量门 + 开关缺省关零行为差)/
源级开关矩阵(10-05-trafilatura-source-scope:engine_options.static_html.
extract_fallback 三态 × 全局 env 两态)。

All I/O runs on httpx.MockTransport; all waiting is recorded by FakeClock.
trafilatura 全程 mock(sys.modules 注入,同 rapid_table/rapidocr 先例)——
主套件不依赖真包,已装/未装环境都绿。
"""

from __future__ import annotations

import httpx
import json
import sys
from typing import Any

import pytest

from myssia.engines.fetch_base import FetchError
from myssia.engines.static_html import StaticHTMLEngine

from conftest import make_client, make_context, make_handler, make_source, run

PAGE_TEMPLATE = """
<html><head><meta charset="utf-8"><title>示例列表页</title></head><body>
<div class="list">
  <div class="item"><h3><a class="title" href="/t/{n}">公开帖子 {n}</a></h3>
  <img class="thumb" src="/img/{n}.png"><span class="price">¥{price}</span></div>
  <div class="item"><h3><a class="title" href="/t/{n1}">AI 资讯 {n1}</a></h3>
  <img class="thumb" src="/img/{n1}.png"><span class="price">¥{price1}</span></div>
</div>
</body></html>
"""


def build_site(pages: dict[int, str | bytes], *, next_pages: set[int] | None = None):
    """Serve /list?page=N from ``pages``; append a next-link for pages in the set."""
    next_pages = next_pages or set()
    calls: list[int] = []

    def responder(request: httpx.Request) -> httpx.Response:
        page = int(request.url.params.get("page", "1"))
        calls.append(page)
        body = pages[page]
        if page in next_pages and isinstance(body, str):
            body = body.replace(
                "</body>", '<a class="next" href="/list?page={}">下一页</a></body>'.format(page + 1)
            )
        headers = {"content-type": "text/html"}
        return httpx.Response(200, headers=headers, content=body)

    return responder, calls


LIST_FIELDS = {
    "title": "a.title",
    "url": "a.title@href",
    "image": "img.thumb@src",
    "price": "span.price",
}


def html_source(url: str, **overrides):
    return make_source(url=url, extract={"type": "list", "item": "div.item", "fields": LIST_FIELDS}, **overrides)


def test_list_extract_attrs_and_relative_url_resolution():
    responder, _ = build_site({1: PAGE_TEMPLATE.format(n=1, n1=2, price=100, price1=200)})
    client = make_client(make_handler(responder))
    source = html_source("https://example.com/list")
    context, _ = make_context(client)
    engine = StaticHTMLEngine(source, context)

    items = run(engine.fetch())
    # price 文本经 coerce_numeric_text 规整为数值(¥ 前缀剥离):基线快照与
    # 阈值路由(price >= 10000)消费数值语义,字符串形态会双双静默失效。
    assert items == [
        {"title": "公开帖子 1", "url": "https://example.com/t/1", "image": "https://example.com/img/1.png", "price": 100},
        {"title": "AI 资讯 2", "url": "https://example.com/t/2", "image": "https://example.com/img/2.png", "price": 200},
    ]


def test_item_extract_single_page_mode():
    responder, _ = build_site({1: PAGE_TEMPLATE.format(n=1, n1=2, price=100, price1=200)})
    client = make_client(make_handler(responder))
    source = make_source(
        url="https://example.com/detail",
        extract={
            "type": "item",
            "fields": {"title": "h3 a.title", "image": "img.thumb@src"},
        },
    )
    context, _ = make_context(client)
    engine = StaticHTMLEngine(source, context)

    items = run(engine.fetch())
    assert items == [{"title": "公开帖子 1", "image": "https://example.com/img/1.png"}]


def test_gb18030_decoding_without_http_charset():
    gb_page = (
        "<html><head><meta charset=\"gb18030\"></head><body>"
        "<div class=\"item\"><h3><a class=\"title\" href=\"/t/9\">显卡降价</a></h3></div>"
        "</body></html>"
    ).encode("gb18030")
    responder, _ = build_site({1: gb_page})
    client = make_client(make_handler(responder))
    source = html_source("https://example.com/list")
    context, _ = make_context(client)
    engine = StaticHTMLEngine(source, context)

    items = run(engine.fetch())
    assert items[0]["title"] == "显卡降价"  # 生产源痛点:gb18030 自动识别


def test_pagination_template_respects_max_pages():
    pages = {p: PAGE_TEMPLATE.format(n=p, n1=p + 1, price=p, price1=p + 1) for p in (1, 2, 3)}
    responder, calls = build_site(pages)
    client = make_client(make_handler(responder))
    source = html_source(
        "https://example.com/list?page={page}",
        pagination={"mode": "template", "max_pages": 2},
        rate_limit={"qps": 1000.0},
    )
    context, _ = make_context(client)
    engine = StaticHTMLEngine(source, context)

    items = run(engine.fetch())
    assert calls == [1, 2]  # max_pages 封顶,第 3 页不抓
    assert len(items) == 4


def test_pagination_template_stops_on_empty_page():
    pages = {
        1: PAGE_TEMPLATE.format(n=1, n1=2, price=1, price1=2),
        2: "<html><body><div class=\"list\"></div></body></html>",  # 空页
        3: PAGE_TEMPLATE.format(n=5, n1=6, price=5, price1=6),
    }
    responder, calls = build_site(pages)
    client = make_client(make_handler(responder))
    source = html_source(
        "https://example.com/list?page={page}",
        pagination={"mode": "template", "max_pages": 5},
        rate_limit={"qps": 1000.0},
    )
    context, _ = make_context(client)
    engine = StaticHTMLEngine(source, context)

    items = run(engine.fetch())
    assert calls == [1, 2]  # 空页提前收尾,礼貌不空翻
    assert len(items) == 2


def test_pagination_selector_follows_next_links():
    pages = {p: PAGE_TEMPLATE.format(n=p, n1=p + 1, price=p, price1=p + 1) for p in (1, 2, 3)}
    responder, calls = build_site(pages, next_pages={1, 2})  # 第 3 页无下一页
    client = make_client(make_handler(responder))
    source = html_source(
        "https://example.com/list",
        pagination={"mode": "selector", "selector": "a.next@href", "max_pages": 5},
        rate_limit={"qps": 1000.0},
    )
    context, _ = make_context(client)
    engine = StaticHTMLEngine(source, context)

    items = run(engine.fetch())
    assert calls == [1, 2, 3]  # 跟随 a.next@href,无下一页自然收尾
    assert len(items) == 6


def test_pagination_selector_stops_at_max_pages():
    pages = {p: PAGE_TEMPLATE.format(n=p, n1=p + 1, price=p, price1=p + 1) for p in (1, 2, 3, 4, 5)}
    responder, calls = build_site(pages, next_pages={1, 2, 3, 4, 5})
    client = make_client(make_handler(responder))
    source = html_source(
        "https://example.com/list",
        pagination={"mode": "selector", "selector": "a.next@href", "max_pages": 2},
        rate_limit={"qps": 1000.0},
    )
    context, _ = make_context(client)
    engine = StaticHTMLEngine(source, context)

    run(engine.fetch())
    assert calls == [1, 2]  # max_pages 封顶


def test_pagination_selector_loop_guard():
    pages = {p: PAGE_TEMPLATE.format(n=p, n1=p + 1, price=p, price1=p + 1) for p in (1, 2)}
    responder, calls = build_site(pages, next_pages={1})  # 页 1 -> 页 2
    # 页 2 的"下一页"指向自己 -> 环路
    def responder_with_loop(request: httpx.Request) -> httpx.Response:
        response = responder(request)
        if int(request.url.params.get("page", "1")) == 2:
            return httpx.Response(
                200,
                headers={"content-type": "text/html"},
                content=str(response.content, "utf-8").replace(
                    "</body>", '<a class="next" href="/list?page=2">下一页</a></body>'
                ),
            )
        return response

    client = make_client(make_handler(responder_with_loop))
    source = html_source(
        "https://example.com/list",
        pagination={"mode": "selector", "selector": "a.next@href", "max_pages": 10},
        rate_limit={"qps": 1000.0},
    )
    context, _ = make_context(client)
    engine = StaticHTMLEngine(source, context)

    run(engine.fetch())
    assert calls == [1, 2]  # 环路检测:同一 URL 只抓一次


def test_change_unchanged_second_run_skips(engine_store):
    responder, calls = build_site({1: PAGE_TEMPLATE.format(n=1, n1=2, price=1, price1=2)})
    client = make_client(make_handler(responder))
    context, _ = make_context(client, store=engine_store)
    source = html_source("https://example.com/list")

    first = run(StaticHTMLEngine(source, context).fetch())
    assert len(first) == 2
    assert calls == [1]

    engine = StaticHTMLEngine(source, context)
    second = run(engine.fetch())
    assert second == []
    assert calls == [1, 1]  # 每轮各 1 次:请求先行,指纹命中后跳过的是提取
    assert engine.last_skip_reason == "hash_match"


def test_unsupported_extract_type_is_structured_error():
    source = make_source(
        engine="static_html",
        extract={"type": "json_path", "fields": {"url": "$[*].u"}},
    )
    client = make_client(make_handler(lambda r: httpx.Response(200, json={})))
    context, _ = make_context(client)
    engine = StaticHTMLEngine(source, context)

    with pytest.raises(FetchError) as excinfo:
        run(engine.fetch())
    assert excinfo.value.error_type == "extract_unsupported"


# ---------------------------------------------------------------------------
# trafilatura 正文兜底(10-05-trafilatura-impl;蓝本=评估档 research.md)
# ---------------------------------------------------------------------------


class _FakeTrafilatura:
    """mock trafilatura 模块(sys.modules 注入,同 rapid_table/rapidocr 先例)。

    ``extract`` 只回填固定 payload 与调用记录,不解析 HTML——契约面
    (output_format="json" → JSON 串)按实现钉版形态模拟。
    """

    def __init__(self, payload: dict | None):
        self.payload = payload
        self.calls: list[str] = []

    def extract(self, html, *, url=None, output_format=None, with_metadata=None):
        assert output_format == "json"  # API 钉版:bare_extraction 禁用
        assert with_metadata is True
        self.calls.append(url)
        if self.payload is None:
            return None
        return json.dumps(self.payload)


#: 文章页 payload(评估档夹具同源):text ≥ 质量门 120,description/sitename/
#: categories 等为「应被丢弃」的键面污染探针。
ARTICLE_DOC = {
    "title": "EXAMPLE 新闻网",
    "author": "张三",
    "date": "2026-10-05T08:00:00+08:00",
    "text": (
        "事故调查组周五发布了最终调查报告,指出起火原因与配电线路老化有关。"
        "报告全文共 87 页,涵盖了事发经过、责任认定与整改建议三个部分。"
        "调查组负责人在发布会上表示,涉事机库的配电线路自 2014 年以来未进行过"
        "大修,线路绝缘层多处破损,最终在持续高负载下短路起火。报告同时建议"
        "对同类机库进行全面电气安全排查,并在两年内完成整改。相关部门表示将"
        "采纳该建议,首批排查工作将于下月启动。"
    ),
    "description": "应被丢弃",
    "sitename": "应被丢弃",
    "categories": ["应被丢弃"],
    "fingerprint": "应被丢弃",
}

ARTICLE_PAGE = (
    "<html><head><title>机库起火事故调查报告发布</title></head><body>"
    "<article><h1>机库起火事故调查报告发布</h1>"
    "<p>事故调查组周五发布了最终调查报告,指出起火原因与配电线路老化有关。</p>"
    "</article></body></html>"
)


def article_site():
    def responder(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, headers={"content-type": "text/html"}, text=ARTICLE_PAGE)

    return responder


def test_fallback_missing_rules_produces_single_item(monkeypatch):
    """① 规则缺失(extract=None)+开关开+mock 在:单页一条,键面=既有键。

    零新键契约:url/title/content=Item.from_extracted known 键;
    published/author=RSS_ENTRY_FIELDS 既有字段名;extract_provenance 落条目
    (from_extracted 归入 metadata);description/sitename/categories/
    fingerprint 不映射直接丢。
    """
    fake = _FakeTrafilatura(ARTICLE_DOC)
    monkeypatch.setitem(sys.modules, "trafilatura", fake)
    monkeypatch.setenv("MYIA_EXTRACT_FALLBACK", "1")
    client = make_client(make_handler(article_site()))
    source = make_source(engine="static_html", url="https://example.com/news/story")
    context, _ = make_context(client)
    engine = StaticHTMLEngine(source, context)

    items = run(engine.fetch())
    assert items == [
        {
            "url": "https://example.com/news/story",
            "title": "EXAMPLE 新闻网",
            "content": ARTICLE_DOC["text"],
            "published": "2026-10-05T08:00:00+08:00",
            "author": "张三",
            "extract_provenance": "trafilatura",
        }
    ]
    assert fake.calls == ["https://example.com/news/story"]

    # 管线消费契约:Item.from_extracted 真跑,published/author/provenance 落
    # metadata,content 落 Item.content(items.content 列回填)。
    from myssia.pipeline import Item

    item = Item.from_extracted(items[0], source="demo")
    assert item.url == "https://example.com/news/story"
    assert item.title == "EXAMPLE 新闻网"
    assert item.content == ARTICLE_DOC["text"]
    assert item.metadata == {
        "published": "2026-10-05T08:00:00+08:00",
        "author": "张三",
        "extract_provenance": "trafilatura",
    }


def test_fallback_missing_rules_disabled_by_default(monkeypatch):
    """① 开关缺省关=零行为差:照旧 extract_required 拒载(trafilatura 在也不进)。"""
    fake = _FakeTrafilatura(ARTICLE_DOC)
    monkeypatch.setitem(sys.modules, "trafilatura", fake)
    monkeypatch.delenv("MYIA_EXTRACT_FALLBACK", raising=False)
    client = make_client(make_handler(article_site()))
    source = make_source(engine="static_html", url="https://example.com/news/story")
    context, _ = make_context(client)
    engine = StaticHTMLEngine(source, context)

    with pytest.raises(FetchError) as excinfo:
        run(engine.fetch())
    assert excinfo.value.error_type == "extract_required"
    assert fake.calls == []  # 缺省关:兜底结构性不触达


def test_fallback_missing_rules_without_dependency(monkeypatch):
    """① 开关开+trafilatura 缺装(sys.modules 置 None 即 import 失败):装不上
    不拦核心——回落现状 extract_required 拒载(①语义逐字节同缺装前)。"""
    monkeypatch.setitem(sys.modules, "trafilatura", None)
    monkeypatch.setenv("MYIA_EXTRACT_FALLBACK", "1")
    client = make_client(make_handler(article_site()))
    source = make_source(engine="static_html", url="https://example.com/news/story")
    context, _ = make_context(client)
    engine = StaticHTMLEngine(source, context)

    with pytest.raises(FetchError) as excinfo:
        run(engine.fetch())
    assert excinfo.value.error_type == "extract_required"


def test_fallback_rules_empty_produces_single_item(monkeypatch):
    """② 规则跑空(list 型整页 0 条)+开关开:兜底出条(改版失效源可救)。"""
    fake = _FakeTrafilatura(ARTICLE_DOC)
    monkeypatch.setitem(sys.modules, "trafilatura", fake)
    monkeypatch.setenv("MYIA_EXTRACT_FALLBACK", "1")
    client = make_client(make_handler(article_site()))
    # 规则在但选择器零命中(页面是 article 结构,规则找 div.list)
    source = html_source("https://example.com/news/story")
    context, _ = make_context(client)
    engine = StaticHTMLEngine(source, context)

    items = run(engine.fetch())
    assert [item["extract_provenance"] for item in items] == ["trafilatura"]
    assert items[0]["url"] == "https://example.com/news/story"
    assert items[0]["content"] == ARTICLE_DOC["text"]


def test_fallback_rules_hit_never_touches_trafilatura(monkeypatch):
    """结构性「兜底非首选」:规则命中的源 trafilatura 永不触达(含③字段级
    失败面——部分字段 miss 的条目照常省略,不进兜底)。"""
    fake = _FakeTrafilatura(ARTICLE_DOC)
    monkeypatch.setitem(sys.modules, "trafilatura", fake)
    monkeypatch.setenv("MYIA_EXTRACT_FALLBACK", "1")
    responder, _ = build_site({1: PAGE_TEMPLATE.format(n=1, n1=2, price=100, price1=200)})
    client = make_client(make_handler(responder))
    source = html_source("https://example.com/list")
    context, _ = make_context(client)
    engine = StaticHTMLEngine(source, context)

    items = run(engine.fetch())
    assert len(items) == 2  # 规则产出,键面与现状零差
    assert all("extract_provenance" not in item for item in items)
    assert fake.calls == []  # 规则命中:兜底零调用


def test_fallback_quality_gate_blocks_degenerate_text(monkeypatch):
    """质量门:正文量不足(50<120,列表页退化形态)→ 视同启发式失败=零条。"""
    short_doc = dict(ARTICLE_DOC, text="导航与标题拼接的退化正文,共五十个字符左右,不过门。")
    fake = _FakeTrafilatura(short_doc)
    monkeypatch.setitem(sys.modules, "trafilatura", fake)
    monkeypatch.setenv("MYIA_EXTRACT_FALLBACK", "1")
    client = make_client(make_handler(article_site()))
    source = make_source(engine="static_html", url="https://example.com/news/story")
    context, _ = make_context(client)
    engine = StaticHTMLEngine(source, context)

    items = run(engine.fetch())
    assert items == []  # 零条保真:不产伪条目
    assert fake.calls == ["https://example.com/news/story"]  # 启发式跑了,门拦住


def test_fallback_heuristic_none_keeps_zero_items(monkeypatch):
    """启发式判定无正文(extract 返回 None):维持零条语义(JS 空壳页同路径)。"""
    fake = _FakeTrafilatura(None)
    monkeypatch.setitem(sys.modules, "trafilatura", fake)
    monkeypatch.setenv("MYIA_EXTRACT_FALLBACK", "1")
    client = make_client(make_handler(article_site()))
    source = make_source(engine="static_html", url="https://example.com/news/story")
    context, _ = make_context(client)
    engine = StaticHTMLEngine(source, context)

    items = run(engine.fetch())
    assert items == []


def test_fallback_rss_empty_not_touched(monkeypatch):
    """负向边界:rss 源走 feedparser 白名单路径,跑空也不挂兜底。"""
    fake = _FakeTrafilatura(ARTICLE_DOC)
    monkeypatch.setitem(sys.modules, "trafilatura", fake)
    monkeypatch.setenv("MYIA_EXTRACT_FALLBACK", "1")
    empty_feed = "<rss version='2.0'><channel><title>空 feed</title></channel></rss>"

    def responder(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, headers={"content-type": "application/xml"}, text=empty_feed)

    client = make_client(make_handler(responder))
    source = make_source(
        engine="static_html",
        url="https://example.com/feed.xml",
        extract={"type": "rss", "fields": {"title": "title", "url": "link"}},
    )
    context, _ = make_context(client)
    engine = StaticHTMLEngine(source, context)

    items = run(engine.fetch())
    assert items == []
    assert fake.calls == []  # rss 结构性不触达


# ---------------------------------------------------------------------------
# 源级开关矩阵(10-05-trafilatura-source-scope)
# engine_options.static_html.extract_fallback 三态 × 全局 env 两态,①场景断言。
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    ("source_flag", "env_value", "expect_fallback"),
    [
        pytest.param(True, "1", True, id="src-on-env-on"),
        pytest.param(True, None, True, id="src-on-env-off"),
        pytest.param(False, "1", False, id="src-off-env-on"),
        pytest.param(False, None, False, id="src-off-env-off"),
        pytest.param(None, "1", True, id="src-unset-env-on"),
        pytest.param(None, None, False, id="src-unset-env-off"),
    ],
)
def test_fallback_source_scoped_switch_matrix(
    monkeypatch, source_flag, env_value, expect_fallback
):
    """优先级=源级 > 全局 env > 缺省关。

    源级开两格(全局开/关)均兜底;源级关两格均拒载(含全局开被单源压掉);
    未设两格=母任务现状逐字节复现(env 开→出条 / env 关→extract_required)。
    """
    fake = _FakeTrafilatura(ARTICLE_DOC)
    monkeypatch.setitem(sys.modules, "trafilatura", fake)
    if env_value is None:
        monkeypatch.delenv("MYIA_EXTRACT_FALLBACK", raising=False)
    else:
        monkeypatch.setenv("MYIA_EXTRACT_FALLBACK", env_value)
    overrides: dict[str, Any] = {}
    if source_flag is not None:
        overrides["engine_options"] = {"static_html": {"extract_fallback": source_flag}}
    client = make_client(make_handler(article_site()))
    source = make_source(engine="static_html", url="https://example.com/news/story", **overrides)
    context, _ = make_context(client)
    engine = StaticHTMLEngine(source, context)

    if expect_fallback:
        items = run(engine.fetch())
        assert [item.get("extract_provenance") for item in items] == ["trafilatura"]
        assert fake.calls == ["https://example.com/news/story"]
    else:
        with pytest.raises(FetchError) as excinfo:
            run(engine.fetch())
        assert excinfo.value.error_type == "extract_required"
        assert fake.calls == []  # 关态:兜底结构性不触达


def test_fallback_source_scoped_type_error(monkeypatch):
    """类型错即结构化拒(saas._bool_option 先例):含糊值不开不关静默失效才是坑。"""
    fake = _FakeTrafilatura(ARTICLE_DOC)
    monkeypatch.setitem(sys.modules, "trafilatura", fake)
    monkeypatch.setenv("MYIA_EXTRACT_FALLBACK", "1")
    client = make_client(make_handler(article_site()))
    source = make_source(
        engine="static_html",
        url="https://example.com/news/story",
        engine_options={"static_html": {"extract_fallback": "yes"}},
    )
    context, _ = make_context(client)
    engine = StaticHTMLEngine(source, context)

    with pytest.raises(FetchError) as excinfo:
        run(engine.fetch())
    assert excinfo.value.error_type == "invalid_engine_options"
    assert fake.calls == []


def test_fallback_source_scoped_covers_rules_empty(monkeypatch):
    """②规则跑空走同一取值链:源级开 + 全局 env 关 → 兜底出条(改版失效源单源可救)。"""
    fake = _FakeTrafilatura(ARTICLE_DOC)
    monkeypatch.setitem(sys.modules, "trafilatura", fake)
    monkeypatch.delenv("MYIA_EXTRACT_FALLBACK", raising=False)
    client = make_client(make_handler(article_site()))
    source = html_source(
        "https://example.com/news/story",
        engine_options={"static_html": {"extract_fallback": True}},
    )
    context, _ = make_context(client)
    engine = StaticHTMLEngine(source, context)

    items = run(engine.fetch())
    assert [item["extract_provenance"] for item in items] == ["trafilatura"]
    assert fake.calls == ["https://example.com/news/story"]
