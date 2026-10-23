"""羊毛质量治理(task 10-19-wool-quality-gate → 10-24 词表 v2 上收):
drop 否决机制 + 源级同主体合成。

案发线(2026-10-19 主人报障):
- sb.sb 提问帖「甲骨文账号升级后…可以再免费开一台 2c12g100g 的实例吗」因标题
  含「免费」被 FREE_KW 判 freebie 混进羊毛流(items.id=8547;同型 7616/8060);
- TapNow 活动列表整页 8+ 行同主体,逐条进情报流=刷屏,须合成一条。

2026-10-24 演进(10-24-huawei-ai-news-absorb Step 1.5):wool.yaml 的三条
品类级 drop 规则(10-19 试错版)已删——提问帖/广告帖否决上收进
myssia-classifier 词表 v2(builtin noise 五刀求助族+`吗$|呢$` 尾缀、fake
假信号、付费/拉客砍),全局生效。本文件钉三件事:
1. 品类级 drop 规则机制本身照旧可用且先于内置裁决(合成配置单测,
   classify_rule_drop ≠ classify_unmatched 分开计数);
2. 词表 v2 对真实案发标题的否决(经 builtin,不经品类规则)与真羊毛放行;
3. 源级 aggregate 把整页条目合成单条(标题/正文/metadata/URL 身份契约)。
"""

from __future__ import annotations

import asyncio
from pathlib import Path
from typing import Any

import httpx
import pytest

from conftest import FakeClock
from myssia.classify import classify_item, load_rules
from myssia.pipeline import Pipeline
from myssia.schema import load_category
from myssia.store import SQLiteStore

REPO_ROOT = Path(__file__).resolve().parents[2]
WOOL_YAML = REPO_ROOT / "config" / "wool.yaml"

# 真实案发标题(装机库 items 实录,2026-10-19)
QUESTION_TITLE = "甲骨文账号升级后，需要做些什么呢？另外升级后可以再免费开一台 2c12g100g 的实例吗"
QUESTION_TITLE_2 = "听说这个论坛可以获得免费域名啊 冲着 edu.ax 这个后缀来的 什么时候开放呀"
# 促销广告案发标题:词表 v2/生产 v3.1 实测均归 proxy-node(「Proxy」先命中主循环,
# 付费砍只杀主循环零命中的标题——生产同款语义,cat_of 实测在案)。10-19 的
# 品类级促销 drop 规则已按 10-24 裁决删除;品类要再收紧可按本文件下方合成
# 配置单测的机制自行声明 drop 规则(机制保留,语义上收)。
AD_TITLE = "🔥 B2Proxy 超值大促 | 限时特惠 3GB 仅 $2.99 | 最高 25%OFF + 免费"
# 真羊毛(同库同源实录;v2 硬门槛语义下仍须放行)
LEGIT_TITLES = [
    "腾讯地图打车无门槛 10 元",
    "免费送 NAS 券",
]
# 10-19 旧判「真羊毛」中的宽松形态:标题光带「免费」无量化/动作信号,
# v2 硬门槛(生产 10-20 主人令)下按设计收紧为丢弃——主人 10-20 生产令,
# 收量下降是预期,不算误杀(交付汇报说明)。
LOOSE_FREEBIE_NOW_DROPPED = "京东 plus 的免费家政清洁还不错"


# ---------------------------------------------------------------------------
# unit level: 词表 v2 builtin 否决案发标题(品类 drop 规则已上收,10-24)
# ---------------------------------------------------------------------------


def _wool_rules():
    return load_rules(str(WOOL_YAML))


def test_wool_yaml_loads_through_schema_with_new_fields():
    """整份 wool.yaml 过 load_category:三条品类级 drop 规则已删(否决上收
    进词表 v2 builtin,10-24 Step 1.5),两条打标规则(免费AI端点/合成条目)
    留守;占位注释里的 aggregate 形态照旧在 schema 白名单内。"""
    from myssia.schema import load_category_file

    config = load_category_file(WOOL_YAML)
    drops = [rule for rule in config.classify.rules if rule.drop]
    assert drops == [], "品类级 drop 规则应已上收进词表 v2(wool.yaml 不再叠床架屋)"
    assert [rule.name for rule in config.classify.rules] == ["免费AI端点", "同主体合成条目"]


def test_builtin_table_vetoes_real_offenders():
    """案发标题经词表 v2 builtin 否决(不再依赖品类 drop 规则):提问帖走
    noise 五刀(需要做些什么),听说帖走 fake(听说)。促销广告案发标题例外:
    「Proxy」先命中主循环 → proxy-node(生产 v3.1 cat_of 实测同判,五刀只砍
    主循环零命中的标题),单列断言留档——品类要拦可自行声明 drop 规则。"""
    for title in (QUESTION_TITLE, QUESTION_TITLE_2):
        result = classify_item({"title": title, "url": "https://sb.sb/t/x"})
        assert result.category is None, f"案发标题应被词表 v2 否决: {title}"
        assert result.matched, f"否决须有命中追溯(观测面): {title}"
    ad_result = classify_item({"title": AD_TITLE, "url": "https://sb.sb/t/x"})
    assert ad_result.category == "proxy-node", (
        "促销广告案发标题:主循环 Proxy 命中在付费砍之前(生产 v3.1 实测同判)"
    )


def test_builtin_table_keeps_hard_threshold_freebies():
    """真羊毛(带硬门槛量化/动作信号)不被误杀;宽松「免费」形态按 v2 收紧丢弃。"""
    for title in LEGIT_TITLES:
        result = classify_item({"title": title, "url": "https://sb.sb/t/y"})
        assert result.category == "freebie", f"真羊毛不该被误杀: {title}"
    assert classify_item({"title": LOOSE_FREEBIE_NOW_DROPPED}).category is None, (
        "宽松免费形态按 10-20 硬门槛收紧为丢弃(预期行为,非回归)"
    )


def test_wool_yaml_g4f_rule_still_tags_without_veto():
    rules = _wool_rules()
    result = classify_item(
        {"title": "https://g4f.dev/api/x", "url": "https://g4f.dev/api/x"}, rules=rules
    )
    assert result.dropped_by == ""
    assert "freebie" in result.tags


# ---------------------------------------------------------------------------
# drop veto: pipeline stage level (separate skip counter)
# ---------------------------------------------------------------------------


def _html_handler(pages: dict[str, str]):
    def handler(request: httpx.Request) -> httpx.Response:
        if request.url.path == "/robots.txt":
            return httpx.Response(404, text="")
        return httpx.Response(
            200, headers={"content-type": "text/html"}, text=pages.get(request.url.path, "")
        )

    return handler


_PAGE = """
<html><body>
<div class="ev"><a class="t" href="/t/1">甲骨文升级后可以再免费开一台吗</a></div>
<div class="ev"><a class="t" href="/t/2">免费送 NAS 券</a></div>
<div class="ev"><a class="t" href="/t/3">超值大促限时免费领</a></div>
</body></html>
"""


def _make_pipeline(config, handler, store):
    client = httpx.AsyncClient(transport=httpx.MockTransport(handler))
    return Pipeline(
        config,
        store=store,
        client=client,
        clock=FakeClock().time,
        sleep=FakeClock().sleep,
    )


def test_pipeline_drop_rules_counted_separately_from_unmatched(tmp_path):
    """3 行:1 提问(吗)+1 广告(超值大促)+1 真羊毛 → 2 条 drop 否决、1 条留存,
    classify_rule_drop 与 classify_unmatched 分开计数。"""
    store = SQLiteStore(tmp_path / "p.db")
    config = load_category(
        {
            "id": "demo",
            "name": "演示品类",
            "schedule": "0 9 * * *",
            "timezone": "Asia/Shanghai",
            "sources": [
                {
                    "name": "sbsb",
                    "engine": "static_html",
                    "url": "https://demo.local/list",
                    "extract": {
                        "type": "list",
                        "item": "div.ev",
                        "fields": {"title": "a.t", "url": "a.t@href"},
                    },
                }
            ],
            "push": [{"channel": "stdout"}],
            "classify": {
                "builtin": True,
                "rules": [
                    {
                        "name": "提问帖过滤",
                        "drop": True,
                        "when": "'吗' in title or '什么时候' in title",
                    },
                    {
                        "name": "促销广告帖过滤",
                        "drop": True,
                        "when": "'超值' in title or '大促' in title",
                    },
                ],
            },
        }
    )
    pipeline = _make_pipeline(config, _html_handler({"/list": _PAGE}), store)
    result = asyncio.run(pipeline.run())

    classify = result.stage("classify")
    assert classify.items_out == 1
    assert classify.skips["classify_rule_drop"] == 2
    assert classify.skips.get("classify_unmatched", 0) == 0
    assert [(item.title, item.category) for item in result.items] == [
        ("免费送 NAS 券", "freebie")
    ]
    store.close()


# ---------------------------------------------------------------------------
# source-level aggregate: page -> one item
# ---------------------------------------------------------------------------

_AGG_PAGE = """
<html><body>
<div class="ev"><a class="t" href="/event/19">TapNow | 1500 Tapies</a></div>
<div class="ev"><a class="t" href="/event/20">TapNow | 100 Tapies</a></div>
<div class="ev"><a class="t" href="/event/21">TapNow | 6000 Tapies</a></div>
<div class="ev"><a class="t" href="/event/22">TapNow | 107 Tapies</a></div>
<div class="ev"><a class="t" href="/event/23">TapNow | 36000 Tapies</a></div>
<div class="ev"><a class="t" href="/event/24">TapNow | 120 Tapies</a></div>
<div class="ev"><a class="t" href="/event/25">TapNow | 72000 Tapies</a></div>
<div class="ev"><a class="t" href="/event/26">TapNow | 20 Tapies/sec</a></div>
</body></html>
"""


def test_source_aggregate_collapses_page_to_one_item(tmp_path):
    """整页 8 行同主体 → fetch 出 1 条:标题=主体+条数+最高值(千分位)、
    url=页面 URL(稳定身份)、明细进 content、原始行进 metadata.aggregated_from。"""
    store = SQLiteStore(tmp_path / "p.db")
    config = load_category(
        {
            "id": "demo",
            "name": "演示品类",
            "schedule": "0 9 * * *",
            "timezone": "Asia/Shanghai",
            "sources": [
                {
                    "name": "tapnow",
                    "engine": "static_html",
                    "url": "https://demo.local/events",
                    "aggregate": {"subject": "TapNow 活动"},
                    "extract": {
                        "type": "list",
                        "item": "div.ev",
                        "fields": {"title": "a.t", "url": "a.t@href"},
                    },
                }
            ],
            "push": [{"channel": "stdout"}],
            "classify": {"builtin": False, "rules": []},
        }
    )
    pipeline = _make_pipeline(config, _html_handler({"/events": _AGG_PAGE}), store)
    result = asyncio.run(pipeline.run())

    fetch = result.stage("fetch")
    assert fetch.status == "ok"
    assert fetch.items_out == 1  # 8 行合成 1 条
    assert len(result.items) == 1
    item = result.items[0]
    assert item.title == "TapNow 活动 · 8 条(最高 72,000)"
    assert item.url == "https://demo.local/events"  # 页面即身份
    assert item.dedup_key  # url 模板可用
    assert "TapNow | 1500 Tapies" in (item.content or "")
    assert "TapNow | 72000 Tapies" in (item.content or "")
    rows = item.view()["aggregated_from"]
    assert len(rows) == 8
    assert rows[0]["url"].endswith("/event/19")
    assert item.view()["aggregate_subject"] == "TapNow 活动"
    store.close()


def test_source_aggregate_zero_rows_stays_zero(tmp_path):
    """空页不合成(0 条 → 0 条,不产「· 0 条」占位)。"""
    store = SQLiteStore(tmp_path / "p.db")
    config = load_category(
        {
            "id": "demo",
            "name": "演示品类",
            "schedule": "0 9 * * *",
            "timezone": "Asia/Shanghai",
            "sources": [
                {
                    "name": "tapnow",
                    "engine": "static_html",
                    "url": "https://demo.local/events",
                    "aggregate": {"subject": "TapNow 活动"},
                    "extract": {
                        "type": "list",
                        "item": "div.ev",
                        "fields": {"title": "a.t", "url": "a.t@href"},
                    },
                }
            ],
            "push": [{"channel": "stdout"}],
            "classify": {"builtin": False, "rules": []},
        }
    )
    pipeline = _make_pipeline(config, _html_handler({"/events": "<html></html>"}), store)
    result = asyncio.run(pipeline.run())
    assert result.stage("fetch").items_out == 0
    assert result.items == []
    store.close()


def test_source_aggregate_requires_list_extract():
    """aggregate 只对 extract.type=list 开放:json_path 源装载即拒(结构化合成
    的前提是列表行;单页 item 源合成无意义)。"""
    with pytest.raises(Exception) as excinfo:
        load_category(
            {
                "id": "demo",
                "name": "演示品类",
                "schedule": "0 9 * * *",
                "timezone": "Asia/Shanghai",
                "sources": [
                    {
                        "name": "api",
                        "engine": "direct_api",
                        "url": "https://api.demo.local/list",
                        "aggregate": {"subject": "X"},
                        "extract": {
                            "type": "json_path",
                            "fields": {"title": "$[*].title", "url": "$[*].url"},
                        },
                    }
                ],
                "push": [{"channel": "stdout"}],
            }
        )
    assert "invalid_source_aggregate" in str(excinfo.value) or any(
        "invalid_source_aggregate" in str(detail)
        for detail in getattr(excinfo.value, "errors", [])
    )
