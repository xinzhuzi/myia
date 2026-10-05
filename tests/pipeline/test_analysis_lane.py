"""Tests for the analysis lane hook — ``_stage_analyze`` 内的本地装饰件通道.

批三 D10(task 10-05-plugin-market-batch,2026-10-05 定案)钉住的契约:

- **执法(D10-2:真执法,fail-closed)**:gates.yaml 缺失/损坏 = 全关 = lane
  不跑;gate 关 = 字面零开销(适配器零触碰,mock 断言零调用);逐件键 =
  ``plugin_gate_key`` 派生(``myssia-snownlp`` → ``analysis.snownlp``);
- **挂点(D10-1:enrich 平行)**:enrich 启用分支与直通分支都必须经过 lane
  (与 ``enrich.enabled`` 正交);lane 输出落 ``item.metadata`` 经
  ``Item.view()`` 可见,**装饰不过滤**;
- **失败容器**:适配器失败 = ``report.warnings`` + ``analysis_lane_degraded_*``
  skip 计数,**绝不进 ``report.failures``**(run 状态不翻 partial);
- **items 表回填** best-effort(``store.merge_item_metadata``,照 enricher
  ``update_item_scores`` 先例:现有 raw 键保留、同名新键覆盖)。

测试纪律:适配器全 mock(零子进程零网络);gates.yaml 每测独立 tmp_path;
store 为 tmp_path 下的 SQLiteStore。
"""

from __future__ import annotations

import asyncio
from typing import Any

import httpx
import pytest

import myssia.pipeline as pipeline_module
from myssia.analysis_lane import ANALYSIS_LANE_MEMBERS, lane_degrade_token
from myssia.pipeline import Pipeline
from myssia.schema import load_category
from myssia.store import SQLiteStore, ItemRecord


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def make_config(**overrides: Any):
    """A minimal valid CategoryConfig(含 enrich 节可开,供两分支测试)。"""
    data: dict[str, Any] = {
        "id": "lane-demo",
        "name": "分析 lane 演示",
        "schedule": "0 9 * * *",
        "sources": [
            {
                "name": "api",
                "engine": "direct_api",
                "url": "https://api.demo.local/list",
                "extract": {
                    "type": "json_path",
                    "fields": {"title": "$[*].title", "url": "$[*].url"},
                },
            }
        ],
        "push": [{"channel": "stdout"}],
    }
    data.update(overrides)
    return load_category(data)


def make_handler(payloads: list[dict[str, Any]]):
    """MockTransport handler:robots.txt -> 404(fail open),列表一次性回。"""

    def handler(request: httpx.Request) -> httpx.Response:
        if request.url.path == "/robots.txt":
            return httpx.Response(404, text="")
        return httpx.Response(200, json=payloads)

    return handler


def write_gates(data_root, text: str):
    (data_root / "gates.yaml").write_text(text, encoding="utf-8")


class FakeAdapter:
    """测试注入的假分析适配器(记录调用;可注入失败)。"""

    def __init__(self, *, decorations: dict[str, dict[str, Any]] | None = None,
                 error: Exception | None = None) -> None:
        self.calls: list[list[dict[str, str]]] = []
        self.decorations = decorations
        self.error = error

    def decorate(self, texts: list[dict[str, str]]) -> dict[str, Any]:
        self.calls.append(list(texts))
        if self.error is not None:
            raise self.error
        if self.decorations is not None:
            return {"decorations": dict(self.decorations)}
        return {
            "decorations": {
                entry["url"]: {"sentiment_score": 0.87, "sentiment_label": "正面"}
                for entry in texts
            }
        }


def make_pipeline(tmp_path, *, analysis_adapters=None, handler_payloads=None,
                  enricher=None, config_overrides: dict[str, Any] | None = None) -> Pipeline:
    payloads = handler_payloads or [
        {"title": "免费送 NAS 券", "url": "https://api.demo.local/a"},
        {"title": "白嫖机场体验", "url": "https://api.demo.local/b"},
    ]
    config = make_config(**(config_overrides or {}))
    store = SQLiteStore(tmp_path / "p.db")
    client = httpx.AsyncClient(transport=httpx.MockTransport(make_handler(payloads)))
    return Pipeline(
        config,
        store=store,
        client=client,
        db_path=tmp_path / "p.db",
        analysis_adapters=analysis_adapters,
        enricher=enricher,
    )


def run(pipeline: Pipeline):
    return asyncio.run(pipeline.run())


# ---------------------------------------------------------------------------
# 执法:gate 关 = 字面零开销;fail-closed;键名派生
# ---------------------------------------------------------------------------


class TestLaneEnforcement:
    def test_gate_all_closed_adapter_never_touched(self, tmp_path):
        """gates.yaml 不存在 = 全关 = lane 直通:适配器零调用、零 skip 计数。"""
        adapter = FakeAdapter()
        pipeline = make_pipeline(tmp_path, analysis_adapters={"snownlp": adapter})
        result = run(pipeline)
        assert result.status == "success"
        assert adapter.calls == []
        analyze = result.stage("analyze")
        assert not [key for key in analyze.skips if key.startswith("analysis_lane")]

    def test_broken_gates_yaml_lane_stays_closed(self, tmp_path):
        """坏 gates.yaml = fail-closed 全关:lane 不跑,run 不失败(铁律)。"""
        write_gates(tmp_path, "oops: [\n")
        adapter = FakeAdapter()
        pipeline = make_pipeline(tmp_path, analysis_adapters={"snownlp": adapter})
        result = run(pipeline)
        assert result.status == "success"
        assert adapter.calls == []

    def test_per_plugin_gate_key_derivation(self, tmp_path):
        """逐件键按 plugin 派生:开 yake 不开 snownlp → 只跑 yake。"""
        write_gates(tmp_path, "analysis:\n  yake: true\n")
        snownlp = FakeAdapter()
        yake = FakeAdapter()
        pipeline = make_pipeline(
            tmp_path, analysis_adapters={"snownlp": snownlp, "yake": yake}
        )
        result = run(pipeline)
        assert result.status == "success"
        assert snownlp.calls == []
        assert len(yake.calls) == 1
        assert result.stage("analyze").skips["analysis_lane_yake_decorated"] == 2

    def test_lane_members_registry_pins_official_packages(self):
        """注册表 = 批三官方成员(键名与 gates.py 官方惯例一致)。"""
        assert ANALYSIS_LANE_MEMBERS == {"snownlp": "myssia-snownlp", "yake": "myssia-yake"}


# ---------------------------------------------------------------------------
# 挂点:两分支都经过;装饰不过滤;装饰落 metadata + items 表回填
# ---------------------------------------------------------------------------


class TestLaneDecoration:
    def test_pass_through_branch_runs_lane_when_open(self, tmp_path):
        """enrich 未启用(直通分支):lane 照跑——开关正交,gates 才是唯一开关。"""
        write_gates(tmp_path, "analysis:\n  snownlp: true\n")
        adapter = FakeAdapter()
        pipeline = make_pipeline(tmp_path, analysis_adapters={"snownlp": adapter})
        result = run(pipeline)
        assert result.status == "success"
        assert len(adapter.calls) == 1
        analyze = result.stage("analyze")
        assert analyze.skips["analysis_lane_snownlp_decorated"] == 2
        # 装饰落 metadata 且经 view() 可见(route 规则/模板消费面)
        for item in result.items:
            view = item.view()
            assert view["sentiment_score"] == 0.87
            assert view["sentiment_label"] == "正面"

    def test_enrich_branch_runs_lane_after_scoring(self, tmp_path):
        """enrich 启用分支:精评之后 lane 照跑(同位互补,装饰不冲突)。"""
        write_gates(tmp_path, "analysis:\n  snownlp: true\n")

        class ScoreAllEnricher:
            async def enrich(self, items, *, watchlist, store):  # noqa: ANN001, ARG002
                from myssia.enrich import EnrichOutcome

                for item in items:
                    item.scores = {"value": 9}
                    item.metadata["score"] = 9.0
                return EnrichOutcome(model="fake", requested=len(items), scored=len(items))

        adapter = FakeAdapter()
        pipeline = make_pipeline(
            tmp_path,
            analysis_adapters={"snownlp": adapter},
            enricher=ScoreAllEnricher(),
            config_overrides={"enrich": {"enabled": True, "model": "fake"}},
        )
        result = run(pipeline)
        assert result.status == "success"
        assert len(adapter.calls) == 1
        for item in result.items:
            assert item.metadata["score"] == 9.0  # 精评装饰仍在
            assert item.metadata["sentiment_score"] == 0.87  # lane 装饰并存

    def test_decoration_does_not_filter_items(self, tmp_path):
        """装饰不过滤:适配器只装饰一条,另一条原样存活。"""
        write_gates(tmp_path, "analysis:\n  snownlp: true\n")
        adapter = FakeAdapter(
            decorations={"https://api.demo.local/a": {"sentiment_score": 0.1}}
        )
        pipeline = make_pipeline(tmp_path, analysis_adapters={"snownlp": adapter})
        result = run(pipeline)
        assert result.status == "success"
        assert len(result.items) == 2  # 未装饰的条目不丢
        assert result.stage("analyze").skips["analysis_lane_snownlp_decorated"] == 1

    def test_store_backfill_merges_into_raw(self, tmp_path):
        """items 表回填:raw 列合并(先并的装饰键保留,后并的不覆盖前者)。"""
        write_gates(tmp_path, "analysis:\n  yake: true\n")
        adapter = FakeAdapter(
            decorations={"https://api.demo.local/a": {"keywords": ["NAS", "白嫖"]}}
        )
        store = SQLiteStore(tmp_path / "p.db")
        client = httpx.AsyncClient(
            transport=httpx.MockTransport(
                make_handler([{"title": "免费送 NAS 券", "url": "https://api.demo.local/a"}])
            )
        )
        config = make_config()
        pipeline = Pipeline(
            config,
            store=store,
            client=client,
            db_path=tmp_path / "p.db",
            analysis_adapters={"yake": adapter},
        )
        result = run(pipeline)
        assert result.status == "success"
        row = store.get_item_by_dedup_key(result.items[0].dedup_key)
        assert row is not None and row.raw is not None
        assert row.raw["keywords"] == ["NAS", "白嫖"]
        # 同条目再并一个键:既有装饰键保留(合并语义,非整列覆写)
        assert store.merge_item_metadata(row.dedup_key, {"sentiment_score": 0.9}) is True
        merged = store.get_item_by_dedup_key(row.dedup_key)
        assert merged.raw["keywords"] == ["NAS", "白嫖"]
        assert merged.raw["sentiment_score"] == 0.9

    def test_title_only_items_counted(self, tmp_path):
        """content 缺失条目(源无 content/续跑退化)按 title-only 计数,不阻。"""
        write_gates(tmp_path, "analysis:\n  snownlp: true\n")
        adapter = FakeAdapter()
        pipeline = make_pipeline(tmp_path, analysis_adapters={"snownlp": adapter})
        result = run(pipeline)
        # 本测试源不带 content 字段 → 全部 title-only
        assert result.stage("analyze").skips["analysis_lane_title_only"] == 2


# ---------------------------------------------------------------------------
# 失败容器:降级注记不翻 partial;适配器缺失;token 归一
# ---------------------------------------------------------------------------


class TestLaneDegradation:
    def test_adapter_failure_degrades_to_warning_not_partial(self, tmp_path):
        """适配器抛错 → warnings + degraded 计数;状态仍 success、条目照常。"""

        class CodedError(Exception):
            code = "dependency_missing"

        adapter = FakeAdapter(error=CodedError("yake 未安装"))
        write_gates(tmp_path, "analysis:\n  yake: true\n")
        pipeline = make_pipeline(tmp_path, analysis_adapters={"yake": adapter})
        result = run(pipeline)
        analyze = result.stage("analyze")
        assert result.status == "success"
        assert result.item_failures == []
        assert analyze.skips["analysis_lane_degraded_dependency_missing"] == 2
        assert [w["error_type"] for w in analyze.warnings] == ["analysis_lane_dependency_missing"]
        assert len(result.items) == 2  # 条目零丢失

    def test_adapter_missing_degrades(self, tmp_path, monkeypatch):
        """gate 开但适配器文件不存在 → adapter_missing 降级,不拦管线。"""
        write_gates(tmp_path, "analysis:\n  snownlp: true\n")
        monkeypatch.setattr(pipeline_module, "default_plugins_roots", lambda data_root: [])
        pipeline = make_pipeline(tmp_path)  # 不注入:走默认发现(被 mock 成空根)
        result = run(pipeline)
        analyze = result.stage("analyze")
        assert result.status == "success"
        assert analyze.skips["analysis_lane_degraded_adapter_missing"] == 2
        assert analyze.warnings and analyze.warnings[0]["plugin"] == "myssia-snownlp"

    def test_bad_output_shape_degrades(self, tmp_path):
        """适配器输出形状不对(缺 decorations)→ output_invalid 降级。"""
        write_gates(tmp_path, "analysis:\n  yake: true\n")

        class BadAdapter:
            def decorate(self, texts):  # noqa: ANN001, ARG001
                return {"nope": True}

        pipeline = make_pipeline(tmp_path, analysis_adapters={"yake": BadAdapter()})
        result = run(pipeline)
        analyze = result.stage("analyze")
        assert result.status == "success"
        assert analyze.skips["analysis_lane_degraded_output_invalid"] == 2

    def test_degrade_token_normalizes_adaptor_codes(self):
        """错误码归一:非词形字符折叠为下划线,空/None → adapter_error。"""
        assert lane_degrade_token("uv_missing") == "uv_missing"
        assert lane_degrade_token("Subprocess FAILED!") == "subprocess_failed"
        assert lane_degrade_token(None) == "adapter_error"


# ---------------------------------------------------------------------------
# store.merge_item_metadata 单元(items 表回填的合并语义)
# ---------------------------------------------------------------------------


class TestMergeItemMetadata:
    def _saved_store(self, tmp_path) -> SQLiteStore:
        store = SQLiteStore(tmp_path / "s.db")
        store.save_item(
            ItemRecord(
                url="https://x.local/a",
                dedup_key="k1",
                title="标题",
                raw={"tags": ["freebie"], "keep": "me"},
            )
        )
        return store

    def test_merge_preserves_existing_keys(self, tmp_path):
        store = self._saved_store(tmp_path)
        assert store.merge_item_metadata("k1", {"sentiment_score": 0.9}) is True
        row = store.get_item_by_dedup_key("k1")
        assert row.raw == {"tags": ["freebie"], "keep": "me", "sentiment_score": 0.9}
        store.close()

    def test_merge_overwrites_same_name_key(self, tmp_path):
        """同名新键覆盖(lane 装饰是 run 级重算,最新一轮为准)。"""
        store = self._saved_store(tmp_path)
        store.merge_item_metadata("k1", {"keep": "new"})
        assert store.get_item_by_dedup_key("k1").raw["keep"] == "new"
        store.close()

    def test_merge_missing_key_returns_false(self, tmp_path):
        store = self._saved_store(tmp_path)
        assert store.merge_item_metadata("nope", {"a": 1}) is False
        store.close()

    def test_merge_rejects_empty_key_and_non_mapping(self, tmp_path):
        store = self._saved_store(tmp_path)
        with pytest.raises(ValueError):
            store.merge_item_metadata("", {"a": 1})
        with pytest.raises(ValueError):
            store.merge_item_metadata("k1", ["not", "a", "mapping"])
        store.close()
