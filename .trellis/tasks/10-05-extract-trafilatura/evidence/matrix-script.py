"""10-05-extract-trafilatura 行为矩阵取证脚本 v2(离线,零外网)。

trafilatura 2.3.0 bare_extraction 返回 Document 对象(非 dict,脚本 v1 实证),
改走稳定 API:trafilatura.extract(output_format="json", with_metadata=True)→
JSON 字符串 → json.loads 拿字段面。这也是实现期兜底应钉的 API 形态。
"""
import json
import trafilatura
from trafilatura import extract as traf_extract
from myssia.engines.fetch_base import extract_html
from myssia.schema import ExtractConfig

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
<footer><p>© 2026 EXAMPLE 新闻网 | 隐私政策 | 服务条款 | 网站地图</p></footer>
</body></html>"""

REVAMPED = """<!DOCTYPE html><html lang="zh"><head><title>最新资讯 - EXAMPLE</title></head><body>
<nav><a href="/">首页</a> | <a href="/news">新闻</a></nav><h1>最新资讯</h1>
<div class="card"><h3><a href="/items/2001">台风路径最新预报:明日登陆</a></h3></div>
<div class="card"><h3><a href="/items/2002">量子计算原型机误差率创新低</a></h3></div>
<div class="card"><h3><a href="/items/2003">城市轨道交通新线开通</a></h3></div>
<footer><p>© 2026 EXAMPLE 新闻网</p></footer>
</body></html>"""

# 改版后的文章页(旧 .story-title/.story-body 选择器失效,新结构 .headline/.post-content)
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

def rules_result(label, html, cfg, base):
    try:
        return {"label": label, "outcome": extract_html(html, cfg, base_url=base)}
    except Exception as exc:
        return {"label": label, "outcome": f"EXCEPTION {type(exc).__name__}: {exc}"}

def traf_result(label, html, url):
    """trafilatura 稳定 API:extract(output_format='json')。产出 None = 启发式判定无正文。"""
    try:
        raw = traf_extract(html, url=url, output_format="json", with_metadata=True)
        if raw is None:
            return {"label": label, "outcome": None, "note": "启发式判定无正文,返回 None"}
        doc = json.loads(raw)
        keep = {}
        for k in ("title", "author", "date", "description", "sitename", "categories", "tags", "source"):
            v = doc.get(k)
            if v not in (None, "", []):
                keep[k] = v
        text = doc.get("text") or doc.get("raw_text") or ""
        keep["text_chars"] = len(text)
        keep["text_head_150"] = text[:150].replace("\n", "⏎")
        return {"label": label, "outcome": keep, "note": f"JSON 键面={sorted(doc.keys())}"}
    except Exception as exc:
        return {"label": label, "outcome": f"EXCEPTION {type(exc).__name__}: {exc}"}

results = {
    "trafilatura_version": trafilatura.__version__,
    "api_note": "bare_extraction 返回 Document 对象(v1 实测);钉 extract(output_format='json') 稳定面",
    "matrix": {
        "A_文章页": {
            "有规则源_现状": rules_result("A1:手写 item 规则命中旧版结构(精确字段)", ARTICLE_OLD, RULES_ITEM_OLD, PAGE_URL),
            "无规则源_加trafilatura后": traf_result("A2:文章页零配置兜底(导航/广告/页脚剥除取证)", ARTICLE, PAGE_URL),
        },
        "B_列表页": {
            "有规则源_现状": rules_result("B1:手写 list 规则命中(3 条结构化条目)", LISTING, RULES_LIST, LIST_URL),
            "无规则源_加trafilatura后": traf_result("B2:列表页喂启发式(退化噪声形态取证)", LISTING, LIST_URL),
        },
        "C_改版失效源": {
            "有规则源_跑空": rules_result("C1:改版后旧规则零命中(整页 0 条=现状静默失效)", REVAMPED, RULES_LIST, LIST_URL),
            "改版文章页_规则跑空加trafilatura后": traf_result("C2:改版文章页兜底(正文仍在,启发式可救)", REVAMPED_ARTICLE, PAGE_URL),
            "改版列表页_规则跑空加trafilatura后": traf_result("C3:改版列表页兜底(列表形态,启发式退化取证)", REVAMPED, LIST_URL),
        },
    },
}
print(json.dumps(results, ensure_ascii=False, indent=2, default=str))
