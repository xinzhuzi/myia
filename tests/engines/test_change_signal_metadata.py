"""Tests for change-signal metadata stamping (change-signal-metadata).

契约:``static_html`` 引擎 ``_fetch_page`` verdict 判定后,所有出条出口统一
铸 ``fetch_change_reason=verdict.reason`` 进每条条目 dict——经
``Item.from_extracted`` 非 known 键自动落条目 metadata,dedup key 模板/
classify ``when``/push route ``when`` 零新语法可读。

覆盖验收五点 + 值域补全:
① 空库首跑(CSS list)每条 first_fetch,含管线 from_extracted metadata 断言;
② ``extract.type: rss`` 提取子模式同样带信号(F2 补:厂商 RSS+reddit-ml 全
   走此路径);
③ 规则缺失与规则跑空两路 trafilatura 兜底出条同样带信号(F8 补);
④ 基线存在且内容变 → 每条 hash_differ(含 metadata 断言);
⑤ unchanged 页维持现有整页跳过零条目(零信号,行为零变化);
⑥ 值域补全:etag 变 → validators_differ。

All I/O runs on httpx.MockTransport;trafilatura 全程 mock(sys.modules 注入,
同 test_static_html 先例)。
"""

from __future__ import annotations

import json
import sys
from typing import Any

import httpx

from myssia.engines.static_html import StaticHTMLEngine
from myssia.pipeline import Item

from conftest import make_client, make_context, make_handler, make_source, run

PAGE_TEMPLATE = """
<html><head><meta charset="utf-8"><title>示例列表页</title></head><body>
<div class="list">
  <div class="item"><h3><a class="title" href="/t/{n}">公开帖子 {n}</a></h3></div>
  <div class="item"><h3><a class="title" href="/t/{n1}">AI 资讯 {n1}</a></h3></div>
</div>
</body></html>
"""

RSS_FEED = """<rss version="2.0"><channel><title>示例 feed</title>
<item><title>文章甲</title><link>https://example.com/a</link>
  <published>2026-10-18T08:00:00+08:00</published></item>
<item><title>文章乙</title><link>https://example.com/b</link></item>
</channel></rss>"""

#: 文章页 payload(text ≥ 质量门 120,test_static_html 同源夹具)。
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
}

ARTICLE_PAGE = (
    "<html><head><title>机库起火事故调查报告发布</title></head><body>"
    "<article><h1>机库起火事故调查报告发布</h1>"
    "<p>事故调查组周五发布了最终调查报告,指出起火原因与配电线路老化有关。</p>"
    "</article></body></html>"
)

LIST_FIELDS = {"title": "a.title", "url": "a.title@href"}


def list_source(url: str = "https://example.com/list", **overrides: Any):
    return make_source(
        url=url, extract={"type": "list", "item": "div.item", "fields": LIST_FIELDS}, **overrides
    )


class _FakeTrafilatura:
    """mock trafilatura 模块(sys.modules 注入,同 test_static_html 先例)。"""

    def __init__(self, payload: dict | None):
        self.payload = payload

    def extract(self, html, *, url=None, output_format=None, with_metadata=None):
        assert output_format == "json"
        assert with_metadata is True
        if self.payload is None:
            return None
        return json.dumps(self.payload)


def html_site(body_by_call: list[str], *, etags: list[str | None] | None = None):
    """按调用序返回 body(第 N 次抓取吃第 N 份);etags 同序(None=不带)。"""
    calls: list[str] = []
    etags = etags or [None] * len(body_by_call)

    def responder(request: httpx.Request) -> httpx.Response:
        index = len(calls)
        calls.append(request.url.path)
        headers = {"content-type": "text/html"}
        if etags[index] is not None:
            headers["etag"] = etags[index]
        return httpx.Response(200, headers=headers, text=body_by_call[index])

    return responder, calls


def rss_site(feed: str = RSS_FEED):
    def responder(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, headers={"content-type": "application/xml"}, text=feed)

    return responder


def article_site():
    def responder(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, headers={"content-type": "text/html"}, text=ARTICLE_PAGE)

    return responder


# ---------------------------------------------------------------------------
# ① 空库首跑:CSS list 每条 first_fetch(raw dict + 管线 metadata 双层断言)
# ---------------------------------------------------------------------------


def test_first_fetch_css_list_items_carry_first_fetch(engine_store):
    page = PAGE_TEMPLATE.format(n=1, n1=2)
    responder, calls = html_site([page])
    client = make_client(make_handler(responder))
    context, _ = make_context(client, store=engine_store)
    source = list_source()

    items = run(StaticHTMLEngine(source, context).fetch())
    assert len(items) == 2
    assert [item["fetch_change_reason"] for item in items] == ["first_fetch", "first_fetch"]

    # 管线消费契约:Item.from_extracted 非 known 键自动落 metadata——dedup
    # key 模板/classify when/push route when 零新语法可读。
    built = [Item.from_extracted(item, source="demo") for item in items]
    assert all(item.metadata["fetch_change_reason"] == "first_fetch" for item in built)


# ---------------------------------------------------------------------------
# ② rss 提取子模式同样带信号(F2 补)
# ---------------------------------------------------------------------------


def test_first_fetch_rss_items_carry_first_fetch(engine_store):
    client = make_client(make_handler(rss_site()))
    context, _ = make_context(client, store=engine_store)
    source = make_source(
        url="https://example.com/feed.xml",
        extract={"type": "rss", "fields": {"title": "title", "url": "link", "published": "published"}},
    )

    items = run(StaticHTMLEngine(source, context).fetch())
    assert len(items) == 2
    assert [item["fetch_change_reason"] for item in items] == ["first_fetch", "first_fetch"]

    built = [Item.from_extracted(item, source="demo") for item in items]
    assert all(item.metadata["fetch_change_reason"] == "first_fetch" for item in built)


# ---------------------------------------------------------------------------
# ③ 两路 trafilatura 兜底出条同样带信号(F8 补)
# ---------------------------------------------------------------------------


def test_first_fetch_fallback_missing_rules_carries_signal(monkeypatch, engine_store):
    """规则缺失(extract=None)+开关开+mock 在:兜底出条同样铸 first_fetch。"""
    monkeypatch.setitem(sys.modules, "trafilatura", _FakeTrafilatura(ARTICLE_DOC))
    monkeypatch.setenv("MYIA_EXTRACT_FALLBACK", "1")
    client = make_client(make_handler(article_site()))
    context, _ = make_context(client, store=engine_store)
    source = make_source(engine="static_html", url="https://example.com/news/story")

    items = run(StaticHTMLEngine(source, context).fetch())
    assert len(items) == 1
    assert items[0]["fetch_change_reason"] == "first_fetch"
    built = Item.from_extracted(items[0], source="demo")
    assert built.metadata["fetch_change_reason"] == "first_fetch"


def test_first_fetch_fallback_rules_empty_carries_signal(monkeypatch, engine_store):
    """规则跑空(list 型整页 0 条)+开关开:兜底出条同样铸 first_fetch。"""
    monkeypatch.setitem(sys.modules, "trafilatura", _FakeTrafilatura(ARTICLE_DOC))
    monkeypatch.setenv("MYIA_EXTRACT_FALLBACK", "1")
    client = make_client(make_handler(article_site()))
    context, _ = make_context(client, store=engine_store)
    source = list_source("https://example.com/news/story")  # 规则在但零命中

    items = run(StaticHTMLEngine(source, context).fetch())
    assert len(items) == 1
    assert items[0]["fetch_change_reason"] == "first_fetch"


# ---------------------------------------------------------------------------
# ④ 基线存在且内容变 → hash_differ;⑥ 值域补全:etag 变 → validators_differ
# ---------------------------------------------------------------------------


def test_changed_page_items_carry_hash_differ(engine_store):
    """第二轮页面内容变(无 etag/last-modified 头,纯 body hash 比对)。"""
    first_page = PAGE_TEMPLATE.format(n=1, n1=2)
    changed_page = PAGE_TEMPLATE.format(n=9, n1=10)
    responder, calls = html_site([first_page, changed_page])
    client = make_client(make_handler(responder))
    context, _ = make_context(client, store=engine_store)
    source = list_source()

    first = run(StaticHTMLEngine(source, context).fetch())
    assert [item["fetch_change_reason"] for item in first] == ["first_fetch"] * 2

    engine = StaticHTMLEngine(source, context)
    second = run(engine.fetch())
    assert [item["url"] for item in second] == [
        "https://example.com/t/9",
        "https://example.com/t/10",
    ]
    assert [item["fetch_change_reason"] for item in second] == ["hash_differ"] * 2

    built = [Item.from_extracted(item, source="demo") for item in second]
    assert all(item.metadata["fetch_change_reason"] == "hash_differ" for item in built)
    assert calls == ["/list", "/list"]


def test_changed_etag_items_carry_validators_differ(engine_store):
    """值域补全:基线带 etag 且下一轮 etag 变 → validators_differ(比对优先级
    etag > hash,body 不变也以 etag 为准)。"""
    same_body = PAGE_TEMPLATE.format(n=1, n1=2)
    responder, _ = html_site([same_body, same_body], etags=['"v1"', '"v2"'])
    client = make_client(make_handler(responder))
    context, _ = make_context(client, store=engine_store)
    source = list_source()

    first = run(StaticHTMLEngine(source, context).fetch())
    assert [item["fetch_change_reason"] for item in first] == ["first_fetch"] * 2

    second = run(StaticHTMLEngine(source, context).fetch())
    assert [item["fetch_change_reason"] for item in second] == ["validators_differ"] * 2


# ---------------------------------------------------------------------------
# ⑤ unchanged 页维持现有整页跳过零条目(行为零变化)
# ---------------------------------------------------------------------------


def test_unchanged_page_keeps_whole_page_skip_zero_items(engine_store):
    page = PAGE_TEMPLATE.format(n=1, n1=2)
    responder, calls = html_site([page, page])
    client = make_client(make_handler(responder))
    context, _ = make_context(client, store=engine_store)
    source = list_source()

    first = run(StaticHTMLEngine(source, context).fetch())
    assert len(first) == 2

    engine = StaticHTMLEngine(source, context)
    second = run(engine.fetch())
    assert second == []  # 整页跳过零条目:现状语义逐字节不变
    assert calls == ["/list", "/list"]  # 请求先行,指纹命中后跳过的是提取
    assert engine.last_skip_reason == "hash_match"
