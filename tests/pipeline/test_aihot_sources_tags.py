"""aihot 深挖两源 + 公司/大V 标签库(10-24-huawei-ai-news-absorb Step 5)。

钉住四件事(镜像 ``test_watch_deals_gate.py`` 的 Step 3 同款分层):

1. ``config/ai-news.yaml`` 的 aihot-daily(/daily 站方昨日回顾,X 原文直链
   进条目 metadata)与 aihot-hot(/hot 48h 热榜)两源形状——条目卡锚/字段/
   引擎层;
2. 改版哨兵(条目数):两源**不设** ``empty_ok`` → 健康度对「指纹未跳过却
   产出 0 条」判 degraded(aihot 09-30 改版静默归零判例的 MYIA 兜底,巡检
   口径=看条目数);
3. 标签库迁入:华为云关停前快照 companies(20)/influencers(22) 生成的
   42 条 custom rules——装载零错 + 抽验求值(含跨字距正则形态与双 tag
   并存)+ region 旗标 cn→🇨🇳/global→🌍;
4. daily-digest 分区一 sources 同步两源名(场景件注释铁律的测试化:源名
   不同步 = 条目入库却永远不进日报)。

X 直链渲染优先另由 ``tests/plugins/test_plugins.py`` 的 ai-news 配置断言
钉住(template 带 ``origin_url or item.url``);抽取形状由同文件
``_SNIPPETS`` 的 aihot-daily/aihot-hot snippet 钉住(无网络)。
"""

from __future__ import annotations

from pathlib import Path

from myssia.classify import rules_from_config
from myssia.schema import load_category_file

REPO_ROOT = Path(__file__).resolve().parents[2]
AI_NEWS_YAML = REPO_ROOT / "config" / "ai-news.yaml"
DAILY_DIGEST_YAML = REPO_ROOT / "config" / "daily-digest.yaml"


def _sources_by_name():
    config = load_category_file(AI_NEWS_YAML)
    return config, {source.name: source for source in config.sources}


# ---------------------------------------------------------------------------
# 1+2. 两源形状 + 条目数哨兵
# ---------------------------------------------------------------------------


def test_aihot_daily_source_shape():
    """aihot-daily:/daily 条目卡锚 article[id^=r-] + X 直链/摘要/来源名字段
    (非保留 extract 字段经 Item.from_extracted 落 metadata,供渲染优先)。"""
    _, by_name = _sources_by_name()
    daily = by_name["aihot-daily"]
    assert daily.engine == "static_html"
    assert daily.url == "https://aihot.news/daily"
    assert daily.extract is not None and daily.extract.type == "list"
    assert daily.extract.item == "article[id^='r-']", (
        "条目卡锚=报告条目数据模型 id(r-<items slug>),2026-10-24 实测 11/11"
    )
    fields = daily.extract.fields
    assert fields["title"] == "h3 a"
    assert fields["url"] == "h3 a@href"
    assert fields["origin_url"] == "div.mt-auto a@href", (
        "X 原文直链字段(x.com/status 或厂商官网 [原文] 链)是本源差异价值"
    )
    assert fields["summary"] == "p"
    assert fields["source_label"] == "span.truncate"


def test_aihot_hot_source_shape():
    """aihot-hot:/hot 双链接形态锚(story uuid|items id)镜像生产 parse_hot
    正则;item 即锚,title 空选择器=锚自身文本。"""
    _, by_name = _sources_by_name()
    hot = by_name["aihot-hot"]
    assert hot.engine == "static_html"
    assert hot.url == "https://aihot.news/hot"
    assert hot.extract is not None and hot.extract.type == "list"
    assert hot.extract.item == "a[href^='/story/'], a[href^='/items/']", (
        "生产 parse_hot 正则的 CSS 形态:story/<uuid36> 与 items/<id> 并收"
    )
    assert hot.extract.fields["url"] == "@href"
    assert hot.extract.fields["title"] == "", "空 css=锚自身文本(extract_html 语义)"


def test_aihot_sources_keep_zero_item_sentinel():
    """改版哨兵(条目数):两源不设 empty_ok(缺省 False)→ 健康度把
    「指纹未跳过却产出 0 条」判 degraded、doctor 可见——aihot 09-30 改版
    静默归零判例的兜底;设了 empty_ok 会把哨兵废掉(0 条被判合法空集)。"""
    _, by_name = _sources_by_name()
    for name in ("aihot-daily", "aihot-hot"):
        assert by_name[name].empty_ok is False, f"{name} 不得声明 empty_ok"


def test_push_template_prefers_origin_url():
    """X 直链渲染优先:immediate 模板按 origin_url is defined 分流链接
    (StrictUndefined 下 or 短路不可用,games.yaml is defined 判例同款;
    design §6:X 直抓全死判例下的唯一路径;其余源无该字段回退 url)。"""
    config, _ = _sources_by_name()
    template = config.push[0].template
    assert "item.origin_url is defined" in template
    assert "{{ item.origin_url }}" in template and "{{ item.url }}" in template


# ---------------------------------------------------------------------------
# 3. 公司/大V 标签库(custom rules)
# ---------------------------------------------------------------------------


def _tag_rules():
    import yaml

    document = yaml.safe_load(AI_NEWS_YAML.read_text(encoding="utf-8"))
    return rules_from_config(
        document["classify"]["rules"], source="config/ai-news.yaml"
    )


def test_tag_library_counts_20_companies_22_people():
    """42 条 tag 规则(20 公司+22 大V)全部装载零错——生成自华为云快照
    cloud-snapshot-20261017/{companies,influencers}.json(version 2026-09-24),
    一次性生成产物固化进 YAML(自包含)。"""
    rules = _tag_rules()
    companies = [r for r in rules if r.name.startswith("tag-company-")]
    people = [r for r in rules if r.name.startswith("tag-person-")]
    assert len(companies) == 20, f"公司规则应 20 条,当前 {len(companies)}"
    assert len(people) == 22, f"大V规则应 22 条,当前 {len(people)}"


def test_tag_rules_evaluate_on_sample_titles():
    """抽验求值:普通词命中/跨字距正则形态(微软.*AI)/cn 与 global 旗标/
    公司+人物双 tag 并存/无关标题零命中(生产 load_matches 语义:match()
    单正则 = '|'.join(keywords) 逐字形态,大小写敏感)。"""
    rules = _tag_rules()

    def tags_of(title: str) -> list[str]:
        return sorted(rule.tag for rule in rules if rule.evaluate({"title": title}))

    assert tags_of("OpenAI 正式发布 Decisions API") == ["OpenAI·🌍"]
    assert tags_of("Claude 网页端默认启用 auto mode") == ["Anthropic·🌍"]
    assert tags_of("月之暗面发布 Kimi K3.1 Pro") == ["月之暗面Kimi·🇨🇳"], (
        "region cn → 🇨🇳 旗标"
    )
    assert tags_of("梁文锋谈 DeepSeek 下一阶段") == [
        "DeepSeek·🇨🇳",
        "梁文锋·🇨🇳",
    ], "公司+人物双 tag 并存(生产 max_labels=2 上限未移植,记档)"
    assert tags_of("微软将 AI 基础设施支出追加百亿") == ["Microsoft·🌍"], (
        "跨字距正则形态 微软.*AI 逐字移植可命中"
    )
    assert tags_of("本地菜市场价格波动") == [], "无关标题零命中"


# ---------------------------------------------------------------------------
# 4. daily-digest 分区同步
# ---------------------------------------------------------------------------


def test_daily_digest_section_one_carries_aihot_sources():
    """分区一 sources 含 aihot-daily/aihot-hot——分区按 store items.source
    匹配,源名不同步 = 条目入库却永远不进日报(静默丢条)。"""
    config = load_category_file(DAILY_DIGEST_YAML)
    sections = config.sources[0].extra_params["engine_options"]["store_report"][
        "sections"
    ]
    section_one = next(s for s in sections if s["title"] == "AI 日报")
    for name in ("aihot-daily", "aihot-hot"):
        assert name in section_one["sources"], (
            f"aihot 新源 {name} 未同步进 daily-digest 分区一"
        )
