"""vision/table 表格还原单测(task 10-05-table-restore 执行清单①)。

全量 mock、零外网(真引擎路径除外):引擎单测注入假 ``rapid_table`` /
``rapidocr_onnxruntime`` 模块(``sys.modules``,与 ``tests/vision/test_vision.py``
假引擎同款纪律)+ 引擎单例逐例重置(``table._reset_engines``);图片环分支
monkeypatch ``collect.run_table``(与 ``fake_ocr`` 同款);schema 侧验
``images.table`` sidecar(``$.images`` 前缀错误路径)。真引擎端到端
(``TestRealEngineFixture``)显式 skip 守卫——dev/CI 未装 extras
``myssia[table]`` 时留给装后沙箱(AC6),与 e2e package smoke 的 SKIP
纪律同款;夹具 = PIL 生成的 4×3 带框行情表(真跑逐格已验,探针记录见
任务档 implement.jsonl)。
"""

from __future__ import annotations

import asyncio
import ipaddress
import sys
from pathlib import Path
from types import SimpleNamespace
from typing import Any

import httpx
import pytest

import myssia.vision.collect as collect
import myssia.vision.table as vision_table
from myssia.schema import ImagesConfig, LoadError, load_category
from myssia.vision.ocr import OcrLine
from myssia.vision.settings import VisionConfig
from myssia.vision.table import (
    INSTALL_COMMAND,
    TableError,
    TableResult,
    html_table_to_markdown,
    run_table,
)

PUBLIC_IPS = ["93.184.216.34"]
PNG_HEAD = b"\x89PNG\r\n\x1a\n"
FIXTURE = Path(__file__).parent / "fixtures" / "table_sample.png"

SIMPLE_HTML = (
    "<html><body><table>"
    "<tr><td>a</td><td>b</td></tr>"
    "<tr><td>1</td><td>2</td></tr>"
    "</table></body></html>"
)
#: 真引擎探针(2026-10-05,rapid-table 3.0.2 + rapidocr-onnxruntime 实跑)
#: 对 fixtures/table_sample.png 的逐格还原输出——端到端断言的事实源。
FIXTURE_MARKDOWN = (
    "|品种|价格|涨跌幅|\n"
    "|---|---|---|\n"
    "|BTC|65000|+2.3%|\n"
    "|ETH|3200|-1.2%|\n"
    "|SOL|150|+5.6%|"
)


# ---------------------------------------------------------------------------
# HTML → GFM Markdown(纯函数)
# ---------------------------------------------------------------------------


class TestHtmlToMarkdown:
    def test_simple_table_gfm_shape(self):
        result = html_table_to_markdown(SIMPLE_HTML)
        assert result == TableResult(markdown="|a|b|\n|---|---|\n|1|2|", rows=2, cols=2)

    def test_single_row_is_header_plus_separator_only(self):
        result = html_table_to_markdown("<table><tr><td>a</td><td>b</td></tr></table>")
        assert result == TableResult(markdown="|a|b|\n|---|---|", rows=1, cols=2)

    def test_th_counts_as_cell(self):
        result = html_table_to_markdown(
            "<table><tr><th>h1</th><th>h2</th></tr><tr><td>1</td><td>2</td></tr></table>"
        )
        assert result is not None and result.rows == 2 and result.cols == 2
        assert result.markdown.startswith("|h1|h2|")

    def test_colspan_keeps_content_once_and_widens_cols(self):
        result = html_table_to_markdown(
            "<table><tr><td colspan=\"2\">wide</td><td>c</td></tr>"
            "<tr><td>1</td><td>2</td><td>3</td></tr></table>"
        )
        assert result is not None
        assert result.cols == 3, "colspan=2 占两列,后续格顺延"
        assert result.markdown.splitlines()[0] == "|wide||c|", "colspan 内容留原格,影子列补空"

    def test_rowspan_shadow_cells_fill_empty(self):
        result = html_table_to_markdown(
            "<table><tr><td rowspan=\"2\">tall</td><td>b</td></tr>"
            "<tr><td>d</td></tr></table>"
        )
        assert result is not None
        lines = result.markdown.splitlines()
        assert lines[0] == "|tall|b|"
        assert lines[2] == "||d|", "rowspan 影子格补空(GFM 无跨行语义),行内后续格对齐"

    def test_pipe_escaped_and_whitespace_collapsed(self):
        result = html_table_to_markdown(
            "<table><tr><td>a|b</td><td>x\ny</td></tr></table>"
        )
        assert result is not None
        assert result.markdown.splitlines()[0] == r"|a\|b|x y|"

    def test_malformed_span_attribute_degrades_to_one(self):
        result = html_table_to_markdown(
            '<table><tr><td colspan="abc">a</td><td>b</td></tr></table>'
        )
        assert result is not None and result.cols == 2

    def test_no_tr_or_no_cell_is_none(self):
        assert html_table_to_markdown("<html><body></body></html>") is None
        assert html_table_to_markdown("<table><tr></tr></table>") is None

    def test_all_empty_cells_is_none(self):
        assert html_table_to_markdown("<table><tr><td></td><td></td></tr></table>") is None


# ---------------------------------------------------------------------------
# 引擎封装:惰性 import / 缺装结构化报错 / ocr_results 喂入 / 单例
# ---------------------------------------------------------------------------


class FakeRapidTable:
    """rapid_table 桩:记录构造与调用;按调用序吐 pred_htmls(或抛错)。"""

    instances: list["FakeRapidTable"] = []

    def __init__(self, cfg: Any = None) -> None:
        self.cfg = cfg
        self.calls: list[dict[str, Any]] = []
        self.call_error: Exception | None = None
        self.htmls: list[str | None] = [SIMPLE_HTML]
        FakeRapidTable.instances.append(self)

    def __call__(self, img: Any, *, ocr_results: Any = None, **_: Any) -> Any:
        self.calls.append({"img": img, "ocr_results": ocr_results})
        if self.call_error is not None:
            raise self.call_error
        html = self.htmls[min(len(self.calls) - 1, len(self.htmls) - 1)]
        return SimpleNamespace(pred_htmls=[html] if html else [])


class FakeRapidOCR:
    """rapidocr_onnxruntime 桩:RapidOCR()(无参)→ (result, elapse)。"""

    instances: list["FakeRapidOCR"] = []

    def __init__(self, params: Any = None) -> None:
        self.calls: list[str] = []
        self.result: list[Any] | None = [
            [[[0, 0], [10, 0], [10, 10], [0, 10]], "a", 0.99],
            [[[20, 0], [30, 0], [30, 10], [20, 10]], "b", 0.98],
        ]
        self.error: Exception | None = None
        FakeRapidOCR.instances.append(self)

    def __call__(self, img: str) -> tuple[list[Any] | None, list[float]]:
        self.calls.append(img)
        if self.error is not None:
            raise self.error
        return self.result, [0.1]


class _FakeNumpyArray(list):
    """numpy.ndarray 最小桩:仅 ``shape``(按嵌套深度递推),供 ocr_results 契约断言。"""

    @property
    def shape(self) -> tuple[int, ...]:
        dims: list[int] = [len(self)]
        first = self[0] if self else None
        while isinstance(first, list):
            dims.append(len(first))
            first = first[0] if first else None
        return tuple(dims)


#: 假 numpy 模块(table.py:178 惰性 import 的全部触面:array/float32 两件;
#: src 若演进用更多 numpy API,桩即 AttributeError 响亮失败,不静默吞)。
_FAKE_NUMPY = SimpleNamespace(
    array=lambda items, dtype=None: _FakeNumpyArray(items),
    float32="float32",
)


@pytest.fixture(autouse=True)
def reset_engines():
    """引擎单例逐例重置(sys.modules 假引擎注入后,缓存必须清防串台)。"""
    vision_table._reset_engines()
    FakeRapidTable.instances.clear()
    FakeRapidOCR.instances.clear()
    yield
    vision_table._reset_engines()


class TestRunTableEngine:
    @pytest.fixture(autouse=True)
    def fake_numpy(self, monkeypatch: pytest.MonkeyPatch):
        """注入假 numpy(sys.modules,与假 rapid_table/rapidocr 同纪律)。

        根因(CI run 37268141209 连红):test 作业裸 ``uv sync`` 只装项目+dev
        组(dev=["pytest"]),numpy 仅经 extras ``myssia[table]`` 传递;而
        ``_ocr_feed`` 的惰性 ``import numpy``(table.py:178)先于一切引擎
        分支执行,本类 8 件在无 numpy 环境齐炸 ModuleNotFoundError。桩
        无条件注入——本地(有真 numpy)/CI(没有)同路径,确定性;真数值
        正确性归 TestRealEngineFixture 真引擎例(装后沙箱 -e '.[table]',
        importorskip 守卫),桩不越界。
        """
        monkeypatch.setitem(sys.modules, "numpy", _FAKE_NUMPY)

    def test_roundtrip_feeds_ocr_results_contract(self, monkeypatch, tmp_path):
        img = tmp_path / "t.png"
        img.write_bytes(PNG_HEAD + b"0" * 64)
        monkeypatch.setitem(sys.modules, "rapid_table", SimpleNamespace(RapidTable=FakeRapidTable))
        monkeypatch.setitem(
            sys.modules, "rapidocr_onnxruntime", SimpleNamespace(RapidOCR=FakeRapidOCR)
        )
        result = run_table(img)
        assert result == TableResult(markdown="|a|b|\n|---|---|\n|1|2|", rows=2, cols=2)
        engine = FakeRapidTable.instances[0]
        assert engine.calls[0]["img"] == str(img)
        boxes, txts, scores = engine.calls[0]["ocr_results"][0]
        assert txts == ("a", "b") and scores == (0.99, 0.98)
        assert boxes.shape == (2, 4, 2), "boxes 按 (N,4,2) polygon 堆叠喂入"

    def test_dependency_missing_rapid_table_structured(self, monkeypatch, tmp_path):
        img = tmp_path / "t.png"
        img.write_bytes(PNG_HEAD)
        monkeypatch.setitem(sys.modules, "rapid_table", None)
        monkeypatch.setitem(
            sys.modules, "rapidocr_onnxruntime", SimpleNamespace(RapidOCR=FakeRapidOCR)
        )
        with pytest.raises(TableError) as excinfo:
            run_table(img)
        assert excinfo.value.code == "dependency_missing"
        assert 'pip install "myssia[table]"' in str(excinfo.value)
        assert excinfo.value.details["install"] == INSTALL_COMMAND
        assert excinfo.value.details["package"] == "rapid-table"

    def test_dependency_missing_rapidocr_structured(self, monkeypatch, tmp_path):
        img = tmp_path / "t.png"
        img.write_bytes(PNG_HEAD)
        monkeypatch.setitem(sys.modules, "rapid_table", SimpleNamespace(RapidTable=FakeRapidTable))
        monkeypatch.setitem(sys.modules, "rapidocr_onnxruntime", None)
        with pytest.raises(TableError) as excinfo:
            run_table(img)
        assert excinfo.value.code == "dependency_missing"
        assert 'pip install "myssia[table]"' in str(excinfo.value)
        assert excinfo.value.details["package"] == "rapidocr-onnxruntime"

    def test_zero_ocr_text_short_circuits_to_none(self, monkeypatch, tmp_path):
        img = tmp_path / "t.png"
        img.write_bytes(PNG_HEAD)

        class EmptyOcr(FakeRapidOCR):
            def __init__(self, params: Any = None) -> None:
                super().__init__(params)
                self.result = None

        monkeypatch.setitem(sys.modules, "rapid_table", SimpleNamespace(RapidTable=FakeRapidTable))
        monkeypatch.setitem(sys.modules, "rapidocr_onnxruntime", SimpleNamespace(RapidOCR=EmptyOcr))
        assert run_table(img) is None, "图内零文字 = 未检出表格(合法,不触结构引擎)"
        assert FakeRapidTable.instances == []

    def test_engine_call_failure_wrapped(self, monkeypatch, tmp_path):
        img = tmp_path / "t.png"
        img.write_bytes(PNG_HEAD)

        class Boom(FakeRapidTable):
            def __init__(self, cfg: Any = None) -> None:
                super().__init__(cfg)
                self.call_error = RuntimeError("onnx session died")

        monkeypatch.setitem(sys.modules, "rapid_table", SimpleNamespace(RapidTable=Boom))
        monkeypatch.setitem(
            sys.modules, "rapidocr_onnxruntime", SimpleNamespace(RapidOCR=FakeRapidOCR)
        )
        with pytest.raises(TableError) as excinfo:
            run_table(img)
        assert excinfo.value.code == "engine_failed"
        assert "onnx session died" in str(excinfo.value)

    def test_engine_constructor_failure_wrapped(self, monkeypatch, tmp_path):
        img = tmp_path / "t.png"
        img.write_bytes(PNG_HEAD)

        class BoomInit(FakeRapidTable):
            def __init__(self, cfg: Any = None) -> None:
                raise OSError("model download refused")

        monkeypatch.setitem(sys.modules, "rapid_table", SimpleNamespace(RapidTable=BoomInit))
        monkeypatch.setitem(
            sys.modules, "rapidocr_onnxruntime", SimpleNamespace(RapidOCR=FakeRapidOCR)
        )
        with pytest.raises(TableError) as excinfo:
            run_table(img)
        assert excinfo.value.code == "engine_failed"
        assert "model download refused" in str(excinfo.value)

    def test_engines_are_singletons_across_calls(self, monkeypatch, tmp_path):
        img = tmp_path / "t.png"
        img.write_bytes(PNG_HEAD)
        monkeypatch.setitem(sys.modules, "rapid_table", SimpleNamespace(RapidTable=FakeRapidTable))
        monkeypatch.setitem(
            sys.modules, "rapidocr_onnxruntime", SimpleNamespace(RapidOCR=FakeRapidOCR)
        )
        assert run_table(img) is not None
        assert run_table(img) is not None
        assert len(FakeRapidTable.instances) == 1, "结构引擎只构造一次(模型只加载一次)"
        assert len(FakeRapidOCR.instances) == 1

    def test_empty_pred_htmls_is_none(self, monkeypatch, tmp_path):
        img = tmp_path / "t.png"
        img.write_bytes(PNG_HEAD)

        class NoHtml(FakeRapidTable):
            def __init__(self, cfg: Any = None) -> None:
                super().__init__(cfg)
                self.htmls = [None]

        monkeypatch.setitem(sys.modules, "rapid_table", SimpleNamespace(RapidTable=NoHtml))
        monkeypatch.setitem(
            sys.modules, "rapidocr_onnxruntime", SimpleNamespace(RapidOCR=FakeRapidOCR)
        )
        assert run_table(img) is None


# ---------------------------------------------------------------------------
# 图片环表格分支(collect.process_item_images)
# ---------------------------------------------------------------------------


class Item:
    def __init__(self, url: str = "https://example.com/item", title: str = "示例条目") -> None:
        self.url = url
        self.title = title
        self.metadata: dict[str, Any] = {}


@pytest.fixture(autouse=True)
def public_dns(monkeypatch: pytest.MonkeyPatch):
    def _resolve(host: str) -> list[str]:
        try:
            ipaddress.ip_address(host)
        except ValueError:
            return list(PUBLIC_IPS)
        return [host]

    monkeypatch.setattr(collect, "_resolve_host", _resolve)


def png_bytes(size: int = 4096) -> bytes:
    return PNG_HEAD + b"0" * (size - len(PNG_HEAD))


def serve(routes: dict[str, bytes]) -> httpx.AsyncClient:
    def handler(request: httpx.Request) -> httpx.Response:
        target = routes.get(request.url.path)
        if target is None:
            return httpx.Response(404, text="missing")
        return httpx.Response(200, content=target)

    return httpx.AsyncClient(transport=httpx.MockTransport(handler), follow_redirects=False)


def fake_ocr(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(
        collect, "run_ocr", lambda path, engine: [OcrLine(text="第一行", conf=0.99)]
    )


def run(coro):
    return asyncio.run(coro)


class TestCollectTableBranch:
    def cfg(self, **overrides: Any) -> ImagesConfig:
        return ImagesConfig(**{"enabled": True, "min_bytes": 1, **overrides})

    def test_table_true_lands_tables_contract_in_metadata(self, monkeypatch):
        fake_ocr(monkeypatch)
        monkeypatch.setattr(
            collect,
            "run_table",
            lambda path: TableResult(markdown="|a|b|\n|---|---|\n|1|2|", rows=2, cols=2),
        )
        item = Item()
        item.metadata["image"] = "https://example.com/pic.png"
        client = serve({"/pic.png": png_bytes()})
        status = run(collect.process_item_images(
            item, images_cfg=self.cfg(table=True), vision_cfg=VisionConfig(), client=client,
        ))
        assert status == "ok"
        assert item.metadata["tables"] == [
            {"markdown": "|a|b|\n|---|---|\n|1|2|", "rows": 2, "cols": 2}
        ], "R6 产出契约:恰好 {markdown, rows, cols} 三键"
        assert "table_status" not in item.metadata, "零失败不写降级标记"
        assert item.metadata["image_ocr"] == "第一行", "表格分支不挤占既有 OCR 产物"

    def test_table_on_no_table_found_writes_nothing(self, monkeypatch):
        fake_ocr(monkeypatch)
        monkeypatch.setattr(collect, "run_table", lambda path: None)
        item = Item()
        item.metadata["image"] = "https://example.com/pic.png"
        client = serve({"/pic.png": png_bytes()})
        run(collect.process_item_images(
            item, images_cfg=self.cfg(table=True), vision_cfg=VisionConfig(), client=client,
        ))
        assert "tables" not in item.metadata
        assert "table_status" not in item.metadata, "未检出表格 ≠ 失败,零降级标记"

    def test_table_error_marks_provider_error_without_blocking(self, monkeypatch):
        fake_ocr(monkeypatch)
        monkeypatch.setattr(
            collect,
            "run_table",
            lambda path: (_ for _ in ()).throw(TableError("dependency_missing", "rapid-table 未安装")),
        )
        item = Item()
        item.metadata["image"] = "https://example.com/pic.png"
        client = serve({"/pic.png": png_bytes()})
        status = run(collect.process_item_images(
            item, images_cfg=self.cfg(table=True), vision_cfg=VisionConfig(), client=client,
        ))
        assert status == "ok", "R6 红线:表格失败绝不阻管线,图片环本体照常收口"
        assert item.metadata["table_status"] == "table_provider_error"
        assert "tables" not in item.metadata
        assert item.metadata["image_ocr"] == "第一行"

    def test_unexpected_exception_degrades_not_raises(self, monkeypatch):
        fake_ocr(monkeypatch)
        monkeypatch.setattr(collect, "run_table", lambda path: (_ for _ in ()).throw(ValueError("boom")))
        item = Item()
        item.metadata["image"] = "https://example.com/pic.png"
        client = serve({"/pic.png": png_bytes()})
        status = run(collect.process_item_images(
            item, images_cfg=self.cfg(table=True), vision_cfg=VisionConfig(), client=client,
        ))
        assert status == "ok"
        assert item.metadata["table_status"] == "table_provider_error"

    def test_mixed_outcome_lands_tables_and_marks_partial_failure(self, monkeypatch):
        fake_ocr(monkeypatch)
        table = TableResult(markdown="|x|\n|---|\n|1|", rows=2, cols=1)

        def flaky(path: Path) -> TableResult:
            if b"good" in path.read_bytes():
                return table
            raise TableError("engine_failed", "半路失败")

        monkeypatch.setattr(collect, "run_table", flaky)
        item = Item()
        item.metadata["images"] = [
            "https://example.com/good.png",
            "https://example.com/bad.png",
        ]
        client = serve({
            "/good.png": png_bytes()[:8] + b"good" + png_bytes()[12:],
            "/bad.png": png_bytes(),
        })
        status = run(collect.process_item_images(
            item, images_cfg=self.cfg(table=True, max_images=2),
            vision_cfg=VisionConfig(), client=client,
        ))
        assert status == "ok"
        assert item.metadata["tables"] == [table.to_dict()], "成功图照常落表,失败图不连坐"
        assert item.metadata["table_status"] == "table_provider_error"

    def test_table_default_off_is_zero_change_golden(self, monkeypatch):
        fake_ocr(monkeypatch)
        monkeypatch.setattr(
            collect, "run_table",
            lambda path: pytest.fail("table 缺省关 = 分支零进入,run_table 不得被调"),
        )
        item = Item()
        item.metadata["image"] = "https://example.com/pic.png"
        client = serve({"/pic.png": png_bytes()})
        status = run(collect.process_item_images(
            item, images_cfg=self.cfg(), vision_cfg=VisionConfig(), client=client,
        ))
        assert status == "ok"
        assert "tables" not in item.metadata and "table_status" not in item.metadata
        assert item.metadata["image_ocr"] == "第一行", "AC2:缺省时表格面零写入,既有产物逐键不变"

    def test_table_false_explicit_same_as_default(self, monkeypatch):
        fake_ocr(monkeypatch)
        monkeypatch.setattr(collect, "run_table", lambda path: pytest.fail("不得进入"))
        item = Item()
        item.metadata["image"] = "https://example.com/pic.png"
        client = serve({"/pic.png": png_bytes()})
        run(collect.process_item_images(
            item, images_cfg=self.cfg(table=False), vision_cfg=VisionConfig(), client=client,
        ))
        assert "tables" not in item.metadata and "table_status" not in item.metadata

    def test_no_usable_images_skips_table_too(self, monkeypatch):
        fake_ocr(monkeypatch)
        monkeypatch.setattr(collect, "run_table", lambda path: pytest.fail("无可用图不得进表格分支"))
        item = Item()
        item.metadata["image"] = "https://example.com/none.png"
        client = serve({"/none.png": b"\x00\x01not-an-image"})
        status = run(collect.process_item_images(
            item, images_cfg=self.cfg(table=True), vision_cfg=VisionConfig(), client=client,
        ))
        assert status == "none", "下载关全灭 → 图片环既有语义不变,表格分支同零进入"


# ---------------------------------------------------------------------------
# schema:images sidecar table 字段($.images 前缀错误路径)
# ---------------------------------------------------------------------------


def _minimal_data() -> dict[str, Any]:
    """最小合法品类(与 tests/test_schema.py 同形状;sidecar 缺省全不带)。"""
    return {
        "id": "demo",
        "name": "Demo",
        "schedule": "0 9 * * *",
        "sources": [{"name": "example", "url": "https://example.com/list?page={page}"}],
    }


class TestSchemaImagesTable:
    def test_table_true_accepted_and_default_off(self):
        data = _minimal_data()
        data["images"] = {"enabled": True, "table": True}
        images = load_category(data).images
        assert images is not None and images.table is True

        data2 = _minimal_data()
        data2["images"] = {"enabled": True}
        images2 = load_category(data2).images
        assert images2 is not None and images2.table is False, "R2 默认关(零影响默认)"

    def test_invalid_table_type_reported_under_images_prefix(self):
        data = _minimal_data()
        data["images"] = {"enabled": True, "table": "maybe"}
        with pytest.raises(LoadError) as excinfo:
            load_category(data)
        paths = [detail.path for detail in excinfo.value.errors]
        assert "$.images.table" in paths, "sidecar 错误路径统一 $.images 前缀"

    def test_coercible_bool_strings_accepted_like_sibling_fields(self):
        """pydantic 宽松布尔词表("yes"/"on" 等)与 enabled 等既有布尔字段同待遇。"""
        data = _minimal_data()
        data["images"] = {"enabled": True, "table": "yes"}
        images = load_category(data).images
        assert images is not None and images.table is True

    def test_twelve_section_contract_untouched_by_table_sidecar(self):
        data = _minimal_data()
        data["images"] = {"enabled": True, "table": True}
        config = load_category(data)
        assert [source.name for source in config.sources] == ["example"]
        assert config.images is not None and config.images.table is True


# ---------------------------------------------------------------------------
# 真引擎端到端(装后跑;dev/CI 缺装显式 SKIP —— 与 e2e smoke 纪律同款)
# ---------------------------------------------------------------------------


class TestRealEngineFixture:
    def test_real_table_fixture_cell_by_cell(self):
        rapid_table = pytest.importorskip(
            "rapid_table",
            reason="extras myssia[table] 未装:缺装路径另有专测;本测留给装后沙箱(AC6)",
        )
        assert rapid_table is not None
        assert FIXTURE.exists(), "PIL 生成的 4×3 带框行情表夹具应随仓提交"
        vision_table._reset_engines()
        result = run_table(FIXTURE)
        assert result is not None, "真表夹具必须还原出表(AC1:装后真图还原)"
        assert (result.rows, result.cols) == (4, 3)
        assert result.markdown == FIXTURE_MARKDOWN, "逐格对照(真引擎探针 2026-10-05 校准)"
        assert set(result.to_dict()) == {"markdown", "rows", "cols"}
