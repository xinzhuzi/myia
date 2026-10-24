"""Tests for value-gate 品类开关落地(价值判断脚手架 WS4,config-rollout).

覆盖验收口径(三配置真实件,零网络零钥匙串——``load_category_file`` 只做
schema 校验,``keychain:`` 引用在装载期是字符串不解析):

- 三配置 ``load_category_file`` 装载成功:value_gate 是第 6 个顶层 sidecar
  节(schema.py 先例 plugin/baseline/aggregate/images/timeouts),装载入口
  pop/校验/挂载,不破 12 节公开契约;
- ``config/ai-news.yaml`` 与 ``config/ai-token-deals.yaml`` 的
  ``value_gate`` 两开关(``first_run_quiet`` / ``repush_on_change``)为真
  ——首跑建档不打扰 + 内容变了再报,在两个 AI 品类真开;
- ``config/daily-digest.yaml`` 装载成功且 value_gate 缺省为 None(sidecar
  未声明 = 合常态);「AI 资讯」与「AI 白嫖与优惠」两个分区
  ``first_run == "fold"``(首轮建档条目折叠,分区键在 engine_options 里,
  分区级校验在 store_report 引擎运行时——本面从 YAML 侧断言键值);
- 其余分区不带 first_run 键(缺省 show = 照常编号进正文):对应品类没开
  first_run_quiet,折叠面不扩散。
"""

from __future__ import annotations

from pathlib import Path

import yaml

from myssia.schema import load_category_file

REPO_ROOT = Path(__file__).resolve().parents[1]
AI_NEWS = REPO_ROOT / "config" / "ai-news.yaml"
AI_TOKEN_DEALS = REPO_ROOT / "config" / "ai-token-deals.yaml"
DAILY_DIGEST = REPO_ROOT / "config" / "daily-digest.yaml"

#: 开了 first_run_quiet 的两个品类对应的日报分区(折叠面,不多不少)
FOLD_SECTIONS = ("AI 日报", "AI 白嫖与优惠")


def test_ai_news_value_gate_armed() -> None:
    """ai-news.yaml 装载成功,value_gate 两开关真(首跑静默+变化重推)."""
    config = load_category_file(AI_NEWS)
    assert config.value_gate is not None, "value_gate 节应已声明并挂载"
    assert config.value_gate.first_run_quiet is True
    assert config.value_gate.repush_on_change is True


def test_ai_token_deals_value_gate_armed() -> None:
    """ai-token-deals.yaml 装载成功,value_gate 两开关真(纯 archive 品类)."""
    config = load_category_file(AI_TOKEN_DEALS)
    assert config.value_gate is not None, "value_gate 节应已声明并挂载"
    assert config.value_gate.first_run_quiet is True
    assert config.value_gate.repush_on_change is True


def test_daily_digest_target_sections_fold_first_run() -> None:
    """daily-digest.yaml 装载成功;目标分区 first_run=折叠,其余保持缺省.

    分区键活在 engine_options.store_report.sections 里(SourceConfig 对
    engine_options 宽松透传),分区级键值校验属 store_report 引擎运行时
    (FIRST_RUN_MODES 白名单);本面从 YAML 侧钉住目标分区的取值。
    """
    config = load_category_file(DAILY_DIGEST)
    assert config.id == "daily-digest"
    assert config.value_gate is None, "daily-digest 未声明 value_gate(缺省态)"

    document = yaml.safe_load(DAILY_DIGEST.read_text(encoding="utf-8"))
    source = next(s for s in document["sources"] if s["name"] == "daily-digest")
    sections = source["engine_options"]["store_report"]["sections"]
    by_title = {section["title"]: section for section in sections}

    for title in FOLD_SECTIONS:
        assert title in by_title, f"分区「{title}」应在 sections 清单内"
        assert by_title[title].get("first_run") == "fold", (
            f"分区「{title}」应 first_run: fold(首轮建档条目折叠)"
        )

    others = [title for title in by_title if title not in FOLD_SECTIONS]
    for title in others:
        assert "first_run" not in by_title[title], (
            f"分区「{title}」未开首跑抑制,不应配 first_run(缺省 show 不动)"
        )
