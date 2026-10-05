"""10-05-trafilatura-impl 真跑取证(离线 MockTransport,零外网零 robots 负担)。

夹具=母任务评估档 matrix-script.py 同款(ARTICLE/LISTING/REVAMPED/REVAMPED_ARTICLE),
引擎级真跑 StaticHTMLEngine:真 trafilatura 2.3.0 + 真开关 env,覆盖矩阵
A2/C2(应出条)与 B2/C3(质量门应拦)+ 开关关两态零行为差。
"""
from __future__ import annotations

import asyncio
import json
import os

import httpx

from myssia.engines.fetch_base import FetchError
from myssia.engines.static_html import StaticHTMLEngine
from myssia.schema import ExtractConfig, SourceConfig

PAGE_URL = "https://example.org/news/2026-10-05/story"
LIST_URL = "https://example.org/news"

ARTICLE = """<!DOCTYPE html><html lang="zh"><head><title>机库起火事故调查报告发布</title>
<meta name="author" content="张三"><meta name="date" content="2026-10-05T08:00:00+08:00"></head>
<body>
<nav><a href="/">首页</a> | <a href="/news">新闻</a> | <a href="/about">关于</a> | <a href="/login">登录</a> | <a href="/contact">联系</a></nav>
<header><h1 class="site-title">EXAMPLE 新闻网</h1><div class="banner-ad">广告:全场五折 点击查看</div></header>
<article>
<h1>机库起火事故调查报告发布</h1>
<p>事故调查组周五发布了最终调查报告,指出起火原因与配电线路老化有关。报告全文共 87 页,涵盖了事发经过、责任认定与整改建议三个部分。</p>
<p>调查组负责人在发布会上表示,涉事机库的配电线路自 2014 年以来未进行过大修,线路绝缘层多处破损,最终在持续高负载下短路起火。</p>
<p>报告同时建议对同类机库进行全面电气安全排查,并在两年内完成整改。相关部门表示将采纳该建议,首批排查工作将于下月启动。</p>
</article>
<footer><p>© 2026 EXAMPLE 新闻网 | 地址 | 隐私政策 | 服务条款 | 网站地图 | 招聘信息 | RSS 订阅</p></footer>
</body></html>"""

LISTING = """<!DOCTYPE html><html lang="zh"><head><title>最新资讯 - EXAMPLE</title></head><body>
<nav><a href="/">首页</a> | <a href="/news">新闻</a> | <a href="/tech">科技</a> | <a href="/finance">财经</a> | <a href="/sports">体育</a> | <a href="/login">登录</a></nav>
<h1>最新资讯</h1>
<article data-item-id="1001"><h3><a href="/items/1001">调查报告发布:机库起火原因查明</a></h3><img src="/img/1001.jpg"></article>
<article data-item-id="1002"><h3><a href="/items/1002">新款 AI 芯片发布,算力翻倍</a></h3><img src="/img/1002.jpg"></article>
<article data-item-id="1003"><h3><a href="/items/1003">开源社区宣布合并两大基金会</a></h3><img src="/img/1003.jpg"></article>
<footer><p>© 2026 EXAMPLE 新闻网 | 隐私政策 | 服务条款 | 网站地图 | 招聘信息</p></footer>
</body></html>"""

REVAMPED = """<!DOCTYPE html><html lang="zh"><head><title>最新资讯 - EXAMPLE</title></head><body>
<nav><a href="/">首页</a> | <a href="/news">新闻</a></nav><h1>最新资讯</h1>
<div class="card"><h3><a href="/items/2001">台风路径最新预报:明日登陆</a></h3></div>
<div class="card"><h3><a href="/items/2002">量子计算原型机误差率创新低</a></h3></div>
<div class="card"><h3><a href="/items/2003">城市轨道交通新线开通</a></h3></div>
<footer><p>© 2026 EXAMPLE 新闻网</p></footer>
</body></html>"""

REVAMPED_ARTICLE = ARTICLE.replace("<h1>机库起火事故调查报告发布</h1>",
    '<h1 class="headline">机库起火事故调查报告发布</h1>').replace("<article>", '<div class="post-content">').replace("</article>", "</div>")

RULES_LIST = ExtractConfig(
    type="list", item="article[data-item-id]",
    fields={"title": "h3", "url": "h3 a@href", "image": "img@src"},
)
RULES_ITEM_OLD = ExtractConfig(
    type="item", fields={"title": ".story-title", "content": ".story-body p"},
)
ARTICLE_OLD = ARTICLE.replace("<h1>机库起火事故调查报告发布</h1>",
    '<div class="story-title">机库起火事故调查报告发布</div>').replace(
    "<article>", '<div class="story-body">').replace("</article>", "</div>")


def make_source(url, extract=None):
    data = {"name": "demo", "engine": "static_html", "url": url}
    if extract is not None:
        data["extract"] = {
            "type": extract.type, "item": extract.item, "fields": extract.fields,
        }
    return SourceConfig.model_validate(data)


from myssia.engines.fetch_base import FetchContext


def Ctx(html):  # tests/conftest.make_context 同构(client 注入,robots 404 fail-open)
    return FetchContext(client=httpx.AsyncClient(transport=httpx.MockTransport(
        lambda req: httpx.Response(404, text="") if req.url.path == "/robots.txt"
        else httpx.Response(200, headers={"content-type": "text/html"}, text=html))))


async def run_case(label, html, url, extract, *, env_on):
    os.environ.pop("MYIA_EXTRACT_FALLBACK", None)
    if env_on:
        os.environ["MYIA_EXTRACT_FALLBACK"] = "1"
    try:
        engine = StaticHTMLEngine(make_source(url, extract), Ctx(html))
        items = await engine.fetch()
        return {"case": label, "items": items}
    except FetchError as exc:
        return {"case": label, "fetch_error": exc.error_type, "message": str(exc)}
    finally:
        os.environ.pop("MYIA_EXTRACT_FALLBACK", None)


async def main():
    import trafilatura
    cases = [
        ("A1 手写规则命中(开关开也永不触达兜底)", ARTICLE_OLD, PAGE_URL, RULES_ITEM_OLD, True),
        ("A2 无规则文章页(①触发,应出条)", ARTICLE, PAGE_URL, None, True),
        ("B2 无规则列表页(①触发,质量门应拦)", LISTING, LIST_URL, None, True),
        ("C1 改版列表页规则跑空(②触发,质量门应拦)", REVAMPED, LIST_URL, RULES_LIST, True),
        ("C2 改版文章页规则跑空(②触发,应出条)", REVAMPED_ARTICLE, PAGE_URL, RULES_ITEM_OLD, True),
        ("A2-开关关 无规则文章页(①照旧拒载)", ARTICLE, PAGE_URL, None, False),
        ("C1-开关关 改版列表页(②照旧零条)", REVAMPED, LIST_URL, RULES_LIST, False),
    ]
    results = []
    for label, html, url, extract, env_on in cases:
        out = await run_case(label, html, url, extract, env_on=env_on)
        # 附正文量取证
        if "items" in out and out["items"]:
            for it in out["items"]:
                if it.get("extract_provenance") == "trafilatura":
                    it["_content_chars"] = len(it.get("content", ""))
        results.append(out)
    print(json.dumps({
        "trafilatura_version": trafilatura.__version__,
        "quality_gate_min_chars": 120,
        "results": results,
    }, ensure_ascii=False, indent=1))


asyncio.run(main())
