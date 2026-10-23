"""定向优惠监控量化门槛(task 10-24-huawei-ai-news-absorb Step 3 / D3):
watch-deals 品类 + urlwatch 引擎 watch_diff_head + DEAL_SPECIFIC_KW drop 规则。

生产语义(watch_deals.py:23-27,2026-10-20 主人令):优惠条目必须带量化信号
(¥$数额/N元块刀credits积分额度天次张/折/%/送N/领N/首N/兑换码/CDK/coupon/
promo),纯话术(赢现金大奖/邀新争霸赛)不发。MYIA 承载链:

    urlwatch 引擎 changed 条目 metadata.watch_diff_head(added 行摘要,
    grill 修正 F4:content 不在 when 求值面,Item.view 含 metadata)
    → 品类 classify drop 规则(正则逐字移植,经 classifier 白名单
      match() 求值)→ 话术变更零产出、量化变更放行
    → daily-digest 分区四「AI 白嫖与优惠」按源名合并承载。

本文件钉四件事(镜像 test_wool_quality_gate.py 归组):
1. 品类装载:watch-deals.yaml 过 schema;三源 announce_new 全关(首跑建
   基线零条目,生产「首跑不推」语义);drop 规则在位。
2. 正则语义:生产案发样本逐条裁决(话术 drop / 量化放行)——规则从
   watch-deals.yaml 真实装载,不复制正则(单一事实源)。
3. 求值链路:引擎 fake adapter changed 事件 → Pipeline 全链 →
   classify_rule_drop 计数与放行条目 category/metadata 断言。
4. 分区同步:watch-deals 三源名在 daily-digest 分区四清单(场景件注释
   铁律的测试化:新源名不同步=分区静默丢条)。
"""

from __future__ import annotations

import asyncio
import types
from pathlib import Path

import httpx
import pytest

from conftest import FakeClock, make_client, make_handler
from myssia.classify import classify_item, load_rules
from myssia.engines import urlwatch as urlwatch_engine_module
from myssia.pipeline import Item, Pipeline
from myssia.schema import load_category, load_category_file
from myssia.store import SQLiteStore

REPO_ROOT = Path(__file__).resolve().parents[2]
WATCH_DEALS_YAML = REPO_ROOT / "config" / "watch-deals.yaml"
DAILY_DIGEST_YAML = REPO_ROOT / "config" / "daily-digest.yaml"

# 生产案发样本(watch_deals.py 注释与 10-24 实抓横幅文案)
# —— 话术(无量化信号,期望 drop)
MARKETING_HEADS = [
    "邀新争霸赛 · 邀请好友赢千元现金大奖",
    "邀请好友注册 RunningHub,冲击邀新排行榜赢取现金大奖!",
    "VibeX —— 百亿 Token 补贴已到账",
    "全新支持 Agent、Skill,从快捷生成到智能协作,开启 AI 创作新体验!",
    "",  # 纯删行/无 added 行摘要
]
# —— 量化(期望放行)
QUANTIFIED_HEADS = [
    "新用户送 30 元额度",
    "首单额外 20% off first order",
    "限时 8 折",
    "月订阅价: $14.99/$54.99/$94.99",
    "limited-time offer at $7.99",
    "200 Free Tapies per $1 兑换码见公告",
    "H3 会员 3 days free trial 1000 credits",
]


def _watch_deals_rules():
    return load_rules(str(WATCH_DEALS_YAML))


# ---------------------------------------------------------------------------
# 1. 品类装载
# ---------------------------------------------------------------------------


def test_watch_deals_yaml_loads_three_urlwatch_sources_baseline_quiet():
    """整份 watch-deals.yaml 过 load_category:三源全 urlwatch、announce_new
    全 false(首跑建基线零条目 = 生产「首跑只建基线不推」)、drop 规则在位。"""
    config = load_category_file(WATCH_DEALS_YAML)
    assert config.id == "watch-deals"
    assert [source.name for source in config.sources] == [
        "runninghub",
        "hailuo",
        "tapnow",
    ]
    assert all(source.engine == "urlwatch" for source in config.sources)
    for source in config.sources:
        options = source.extra_params["engine_options"]["urlwatch"]
        assert options["announce_new"] is False, f"{source.name} 首跑必须静默建基线"
        assert source.proxy == "direct", "urlwatch 引擎只支持 direct"
    assert config.classify.builtin is True, "drop 否决只在 builtin 路生效(管线分支实证)"
    assert [rule.name for rule in config.classify.rules] == ["优惠话术无量化信号"]
    assert config.classify.rules[0].drop is True
    assert config.dedup.key == "{url}"
    assert config.enrich.enabled is False


def test_runninghub_selector_narrows_banner_region():
    """runninghub 源 selector 收窄横幅区(全页监控的定向化:首页其余区块
    日常轮换不进 diff);hailuo 整页(定价文案在 script 内,css 过滤会空心);
    tapnow 走 render 渲染通道(JS 壳)。"""
    config = load_category_file(WATCH_DEALS_YAML)
    by_name = {source.name: source for source in config.sources}
    runninghub = by_name["runninghub"].extra_params["engine_options"]["urlwatch"]
    assert "new-home-npc3-banner" in runninghub["selector"]
    hailuo = by_name["hailuo"].extra_params["engine_options"]["urlwatch"]
    assert "selector" not in hailuo
    tapnow = by_name["tapnow"].extra_params["engine_options"]["urlwatch"]
    assert tapnow["render"] == "crawl4ai"


# ---------------------------------------------------------------------------
# 2. 正则语义(规则从 watch-deals.yaml 真实装载,单一事实源)
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("head", MARKETING_HEADS)
def test_marketing_only_diff_head_is_dropped(head):
    """话术样本(生产 10-20 主人令点名形态)→ drop 零产出。"""
    result = classify_item(
        {
            "title": "RunningHub 横幅 官网有更新",
            "url": "https://www.runninghub.cn/#watch-x",
            "watch_diff_head": head,
        },
        rules=_watch_deals_rules(),
    )
    assert result.category is None
    assert result.dropped_by == "优惠话术无量化信号"


@pytest.mark.parametrize("head", QUANTIFIED_HEADS)
def test_quantified_diff_head_passes(head):
    """量化样本(数额/折扣率/天数/额度/兑换码)→ 放行(词表「更新」键落
    ai-news 存活,标签进观测面)。"""
    result = classify_item(
        {
            "title": "MiniMax 海螺定价 官网有更新",
            "url": "https://hailuoai.video/pricing#watch-x",
            "watch_diff_head": head,
        },
        rules=_watch_deals_rules(),
    )
    assert result.category == "ai-news"
    assert result.dropped_by == ""


def test_missing_watch_diff_head_field_drops_safely():
    """缺 watch_diff_head 字段(非 urlwatch 变更来源的条目混入时)→ `or ''`
    兜底判 drop(宁缺勿滥;量化信号不可证 = 不推)。"""
    result = classify_item(
        {"title": "任意 官网有更新", "url": "https://x.example/#watch-y"},
        rules=_watch_deals_rules(),
    )
    assert result.category is None
    assert result.dropped_by == "优惠话术无量化信号"


# ---------------------------------------------------------------------------
# 3. watch_diff_head 求值链路(引擎 changed 事件 → Pipeline 全链)
# ---------------------------------------------------------------------------


def _fake_adapter(events: list[dict]) -> types.SimpleNamespace:
    def fake_run(urls, *, cache_file=None, timeout=None, **_kw):  # noqa: ANN001, ANN202
        return {
            "plugin": "myssia-urlwatch",
            "status": "success",
            "checked": 1,
            "counts": {"new": 0, "changed": len(events), "unchanged": 0, "error": 0, "deferred": 0},
            "events": events,
            "cache_file": str(cache_file or "~/.myia/urlwatch/cache.db"),
        }

    return types.SimpleNamespace(run=fake_run)


def _changed_event(diff: str) -> dict:
    return {
        "event": "changed",
        "name": "runninghub",
        "location": "https://www.runninghub.cn/",
        "timestamp": "2026-10-24T08:00:00+00:00",
        "diff": diff,
    }


def _handler(request: httpx.Request) -> httpx.Response:
    if request.url.path == "/robots.txt":
        return httpx.Response(404, text="")
    return httpx.Response(200, text="")


def _pipeline_with_real_rules(monkeypatch, diff: str) -> tuple:
    """合成管线:源/规则照抄 watch-deals.yaml 装载件(drop 规则单一事实源),
    adapter 换假件零子进程,push 通道 stdout 避凭据解析。"""
    real = load_category_file(WATCH_DEALS_YAML)
    config = load_category(
        {
            "id": "watch-deals-test",
            "name": "定向优惠监控(测试)",
            "schedule": "30 6,18 * * *",
            "timezone": "Asia/Shanghai",
            "sources": [
                {
                    "name": "runninghub",
                    "engine": "urlwatch",
                    "url": "https://www.runninghub.cn/",
                    "proxy": "direct",
                    "engine_options": {
                        "urlwatch": {
                            "label": "RunningHub 横幅",
                            "announce_new": False,
                            "timeout": 30,
                        }
                    },
                }
            ],
            "push": [{"channel": "stdout"}],
            "classify": {
                "builtin": True,
                "rules": [rule.model_dump() for rule in real.classify.rules],
            },
            "value_gate": {"first_run_quiet": False},
        }
    )
    monkeypatch.setattr(
        urlwatch_engine_module, "import_urlwatch_adapter", lambda: _fake_adapter([_changed_event(diff)])
    )
    store = SQLiteStore(":memory:")
    client = make_client(make_handler(_handler))
    pipeline = Pipeline(
        config,
        store=store,
        client=client,
        clock=FakeClock().time,
        sleep=FakeClock().sleep,
    )
    return pipeline, store


def test_pipeline_drops_marketing_changed_event(monkeypatch):
    """话术变更 → 引擎出条目 → classify drop(classify_rule_drop 计数与
    classify_unmatched 分开观测)→ 零条目产出。"""
    pipeline, store = _pipeline_with_real_rules(
        monkeypatch, "+ 邀新争霸赛 · 邀请好友赢千元现金大奖"
    )
    result = asyncio.run(pipeline.run())
    classify = result.stage("classify")
    assert classify.skips["classify_rule_drop"] == 1
    assert classify.items_out == 0
    assert result.items == []
    store.close()


def test_pipeline_keeps_quantified_changed_event_with_metadata(monkeypatch):
    """量化变更 → 条目存活:category=ai-news(词表「更新」键)、
    metadata.watch_diff_head 随行(view 求值面实证)、#watch- 锚点去重键。"""
    pipeline, store = _pipeline_with_real_rules(
        monkeypatch,
        "+ 新用户送 30 元额度\n+ 限时 8 折\n- 旧套餐下架\n",
    )
    result = asyncio.run(pipeline.run())
    assert result.stage("classify").items_out == 1
    (item,) = result.items
    assert item.category == "ai-news"
    assert item.view()["watch_diff_head"] == "新用户送 30 元额度 限时 8 折"
    assert item.url.startswith("https://www.runninghub.cn/#watch-")
    assert item.source == "runninghub"  # daily-digest 分区四的源名锚
    store.close()


def test_engine_item_to_view_chain_exposes_diff_head():
    """链路最底段独立钉:引擎条目键 → Item.from_extracted → view() 可达
    (grill F4 的修正前提,不依赖管线其余段)。"""
    raw = {
        "url": "https://x.example/#watch-abc",
        "title": "X 官网有更新",
        "watch_event": "changed",
        "watch_page": "https://x.example/",
        "content": "+ 送 3 天",
        "watch_diff_head": "送 3 天",
    }
    view = Item.from_extracted(raw, "x").view()
    assert view["watch_diff_head"] == "送 3 天"


# ---------------------------------------------------------------------------
# 4. daily-digest 分区同步(场景件注释铁律的测试化)
# ---------------------------------------------------------------------------


def test_daily_digest_section_four_carries_watch_deals_sources():
    """分区四 sources 含 watch-deals 三源名——分区按 store items.source 匹配,
    源名不同步 = 条目入库却永远不进日报(静默丢条)。"""
    config = load_category_file(DAILY_DIGEST_YAML)
    sections = config.sources[0].extra_params["engine_options"]["store_report"][
        "sections"
    ]
    section_four = next(s for s in sections if s["title"] == "AI 白嫖与优惠")
    for name in ("runninghub", "hailuo", "tapnow"):
        assert name in section_four["sources"], (
            f"watch-deals 源 {name} 未同步进 daily-digest 分区四"
        )


def test_engine_diff_head_constant_and_pipeline_share_default():
    """引擎截断常量与 docstring 契约一致(200 字符 + 省略号留痕)。"""
    assert urlwatch_engine_module.DEFAULT_DIFF_HEAD_CHARS == 200
    assert urlwatch_engine_module.DIFF_HEAD_ELLIPSIS == "…"
