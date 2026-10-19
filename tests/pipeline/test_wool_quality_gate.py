"""羊毛质量治理(task 10-19-wool-quality-gate):drop 否决 + 源级同主体合成。

案发线(2026-10-19 主人报障):
- sb.sb 提问帖「甲骨文账号升级后…可以再免费开一台 2c12g100g 的实例吗」因标题
  含「免费」被 FREE_KW 判 freebie 混进羊毛流(items.id=8547;同型 7616/8060);
- TapNow 活动列表整页 8+ 行同主体,逐条进情报流=刷屏,须合成一条。

本文件钉三件事:
1. drop 规则先于内置免费信号否决提问/广告帖,且丢弃路径单独计数
   (classify_rule_drop ≠ classify_unmatched);
2. 仓库真实 config/wool.yaml 的规则装载后否决真实案发标题、放行真羊毛;
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
AD_TITLE = "🔥 B2Proxy 超值大促 | 限时特惠 3GB 仅 $2.99 | 最高 25%OFF + 免费"
# 真羊毛(同库同源实录,不该被误杀)
LEGIT_TITLES = [
    "腾讯地图打车无门槛 10 元",
    "京东 plus 的免费家政清洁还不错",
    "免费送 NAS 券",
]


# ---------------------------------------------------------------------------
# drop veto: unit level (classifier) against the real wool.yaml rules
# ---------------------------------------------------------------------------


def _wool_rules():
    return load_rules(str(WOOL_YAML))


def test_wool_yaml_loads_through_schema_with_new_fields():
    """整份 wool.yaml 过 load_category:drop 规则字段与占位注释里的 aggregate
    形态都要在 schema 白名单内(drop 在 ClassifyRuleConfig,aggregate 在
    SourceConfig——后者由占位注释承载,装载面只验证 drop 生效)。"""
    from myssia.schema import load_category_file

    config = load_category_file(WOOL_YAML)
    drops = [rule for rule in config.classify.rules if rule.drop]
    assert [rule.name for rule in drops] == [
        "提问帖过滤",
        "提问帖过滤·怎么如何",
        "促销广告帖过滤",
    ]


def test_wool_yaml_rules_veto_real_offenders():
    rules = _wool_rules()
    for title in (QUESTION_TITLE, QUESTION_TITLE_2, AD_TITLE):
        result = classify_item({"title": title, "url": "https://sb.sb/t/x"}, rules=rules)
        assert result.category is None, f"案发标题应被否决: {title}"
        assert result.dropped_by, "否决须留 dropped_by 规则名(观测面)"


def test_wool_yaml_rules_keep_real_freebies():
    rules = _wool_rules()
    for title in LEGIT_TITLES:
        result = classify_item({"title": title, "url": "https://sb.sb/t/y"}, rules=rules)
        assert result.category == "freebie", f"真羊毛不该被误杀: {title}"
        assert result.dropped_by == ""


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
