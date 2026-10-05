"""myssia-snownlp / myssia-yake 场景件契约测试(10-05-plugin-market-batch 批三 D10).

被钉住的契约:

1. **manifest**:snownlp = desktop + ``gate: stale``(停更知情)+ adapter
   subprocess(上游 MIT,uv 隔离**钉版** 0.12.3,不 vendor);yake = desktop +
   **不声明 gate**(上游 AGPL 免费档+活跃,stale 徽标失实)+ adapter
   in_process(惰性 import,零 vendor);
2. **adapter 契约(analysis lane 的 decorate 面)**:``decorate(texts)`` 输出
   ``{"decorations": {url: {字段: 值}}}``;snownlp 单次 spawn stdin JSON 批处理
   (mock runner,零真实 uv 零网络);yake 进程内惰性 import(未装 =
   ``dependency_missing``,fake yake 模块注入 mock 抽取);错误码词表照
   urlwatch(``uv_missing``/``dependency_missing``/``*_failed``/``*_timeout``/
   ``*_output_invalid``);
3. **铁律**:适配器任何失败形态下核心品类加载与 Pipeline 构造完全无感
   (装不上不拦核心;lane 侧的降级注记钉在 tests/pipeline/test_analysis_lane.py)。

测试纪律:子进程一律 fake runner、上游 import 一律 fake 模块注入,零真实
网络、零真实 uv、零上游装载;每测独立 tmp_path。
"""

from __future__ import annotations

import json
import subprocess
import sys
import types
from pathlib import Path
from typing import Any

import pytest

from myssia.pipeline import Pipeline
from myssia.plugins.manifest import load_manifest_file
from myssia.schema import load_category_file

REPO_ROOT = Path(__file__).resolve().parents[2]
PLUGINS_DIR = REPO_ROOT / "plugins"
SNOWNLP_DIR = PLUGINS_DIR / "myssia-snownlp"
YAKE_DIR = PLUGINS_DIR / "myssia-yake"


def load_adapter(path: Path, module_name: str) -> Any:
    """compile+exec 加载一个插件 adapter(与 analysis_lane.import_analysis_adapter
    同手法;测试侧独立装载,互不污染)。"""
    module = types.ModuleType(module_name)
    module.__file__ = str(path)
    exec(  # noqa: S102 - 仓库内受控代码
        compile(path.read_text(encoding="utf-8"), str(path), "exec"),
        module.__dict__,
    )
    return module


def _stdout(payload: dict[str, Any]) -> str:
    return json.dumps(payload, ensure_ascii=False)


class _RunnerRecorder:
    """fake runner:记录命令与 stdin 载荷,回可配的 stdout/退出码(零子进程)。"""

    def __init__(self, stdout: str, *, returncode: int = 0) -> None:
        self.stdout = stdout
        self.returncode = returncode
        self.commands: list[list[str]] = []
        self.inputs: list[str] = []

    def __call__(self, command: list[str], **kwargs: Any) -> subprocess.CompletedProcess[str]:
        self.commands.append(list(command))
        self.inputs.append(str(kwargs.get("input") or ""))
        return subprocess.CompletedProcess(command, self.returncode, self.stdout, "")


def _hang(command: list[str], **kwargs: Any) -> subprocess.CompletedProcess[str]:
    raise subprocess.TimeoutExpired(command, timeout=0.01)


SAMPLE_TEXTS = [
    {"url": "https://example.com/a", "text": "这个优惠太棒了 白嫖成功"},
    {"url": "https://example.com/b", "text": "客服态度差劲 垃圾活动"},
]


# ---------------------------------------------------------------------------
# myssia-snownlp
# ---------------------------------------------------------------------------


class TestSnownlpManifest:
    def test_manifest_declares_stale_gate_and_pinned_subprocess_adapter(self):
        manifest = load_manifest_file(SNOWNLP_DIR / "plugin.yaml")
        assert manifest.id == "myssia-snownlp"
        assert manifest.tier == "desktop"
        assert manifest.gate == "stale", "停更知情门槛(上游 2020-01 冻结)"
        assert manifest.vendor is None, "MIT 上游不 vendor(pip 依赖隔离调用)"
        assert manifest.adapter is not None
        assert manifest.adapter.mode == "subprocess"
        assert manifest.modes.remote is None
        assert manifest.provides == ["sentiment"]

    def test_pin_matches_pypi_latest_at_collection(self):
        """钉版号 = 收录时 PyPI 末版亲核(2026-10-05):0.12.3(停更件永不漂移)。"""
        adapter = load_adapter(SNOWNLP_DIR / "adapter.py", "myssia_snownlp_adapter_test")
        assert adapter.SNOWNLP_PIN == "0.12.3"
        assert adapter.SNOWNLP_DEPENDENCIES == ("snownlp==0.12.3",)


class TestSnownlpAdapter:
    def test_build_command_is_isolated_uv_with_pinned_snownlp(self, tmp_path):
        adapter = load_adapter(SNOWNLP_DIR / "adapter.py", "myssia_snownlp_adapter_test")
        command = adapter.build_command(tmp_path / "shim.py")
        assert command[:3] == ["uv", "run", "--no-project"]
        assert "--with" in command and "snownlp==0.12.3" in command
        assert command[-2:] == ["python", str(tmp_path / "shim.py")]

    def test_decorate_success_single_spawn_stdin_batch(self, tmp_path, monkeypatch):
        """成功路径:单次 spawn;stdin 携带全批 JSON;decorations 结构化。"""
        monkeypatch.setattr("shutil.which", lambda name: "/usr/local/bin/uv")
        adapter = load_adapter(SNOWNLP_DIR / "adapter.py", "myssia_snownlp_adapter_test")
        decorations = {
            "https://example.com/a": {"sentiment_score": 0.92, "sentiment_label": "正面"},
            "https://example.com/b": {"sentiment_score": 0.08, "sentiment_label": "负面"},
        }
        runner = _RunnerRecorder(_stdout({"decorations": decorations}))
        result = adapter.decorate(SAMPLE_TEXTS, runner=runner)
        assert len(runner.commands) == 1, "每轮单次 spawn(import 即载训练模型,禁逐条)"
        sent = json.loads(runner.inputs[0])
        assert sent == {"texts": SAMPLE_TEXTS}
        assert result["decorations"] == decorations
        assert result["decorated"] == 2
        assert result["snownlp_pin"] == "0.12.3"

    def test_decorate_empty_texts_is_legal_empty_state(self, tmp_path, monkeypatch):
        """零装饰(全跳过)= 合法空态:decorations 空映射,不是错误。"""
        monkeypatch.setattr("shutil.which", lambda name: "/usr/local/bin/uv")
        adapter = load_adapter(SNOWNLP_DIR / "adapter.py", "myssia_snownlp_adapter_test")
        runner = _RunnerRecorder(_stdout({"decorations": {}}))
        result = adapter.decorate(
            [{"url": "https://example.com/a", "text": ""}], runner=runner
        )
        assert result["decorations"] == {}
        assert result["skipped"] == 1

    def test_nonzero_exit_maps_to_failed(self, tmp_path, monkeypatch):
        monkeypatch.setattr("shutil.which", lambda name: "/usr/local/bin/uv")
        adapter = load_adapter(SNOWNLP_DIR / "adapter.py", "myssia_snownlp_adapter_test")
        runner = _RunnerRecorder("", returncode=1)
        with pytest.raises(Exception) as excinfo:
            adapter.decorate(SAMPLE_TEXTS, runner=runner)
        assert excinfo.value.code == "snownlp_failed"

    def test_timeout_maps_to_timeout(self, tmp_path, monkeypatch):
        monkeypatch.setattr("shutil.which", lambda name: "/usr/local/bin/uv")
        adapter = load_adapter(SNOWNLP_DIR / "adapter.py", "myssia_snownlp_adapter_test")
        with pytest.raises(Exception) as excinfo:
            adapter.decorate(SAMPLE_TEXTS, runner=_hang, timeout=0.01)
        assert excinfo.value.code == "snownlp_timeout"

    @pytest.mark.parametrize("stdout", ["not json", '{"nope": true}'])
    def test_invalid_stdout_maps_to_output_invalid(self, tmp_path, monkeypatch, stdout):
        monkeypatch.setattr("shutil.which", lambda name: "/usr/local/bin/uv")
        adapter = load_adapter(SNOWNLP_DIR / "adapter.py", "myssia_snownlp_adapter_test")
        runner = _RunnerRecorder(stdout)
        with pytest.raises(Exception) as excinfo:
            adapter.decorate(SAMPLE_TEXTS, runner=runner)
        assert excinfo.value.code == "snownlp_output_invalid"

    def test_uv_missing_is_structured(self, tmp_path, monkeypatch):
        monkeypatch.setattr("shutil.which", lambda name: None)
        adapter = load_adapter(SNOWNLP_DIR / "adapter.py", "myssia_snownlp_adapter_test")
        with pytest.raises(Exception) as excinfo:
            adapter.decorate(SAMPLE_TEXTS)
        assert excinfo.value.code == "uv_missing"

    def test_input_validation_rejects_bad_shapes(self):
        adapter = load_adapter(SNOWNLP_DIR / "adapter.py", "myssia_snownlp_adapter_test")
        for bad in ("not-a-list", [{"no_url": 1}], [{"url": "", "text": "x"}]):
            with pytest.raises(Exception) as excinfo:
                adapter.decorate(bad)
            assert excinfo.value.code == "texts_invalid"

    def test_input_validation_caps_batch_size(self):
        adapter = load_adapter(SNOWNLP_DIR / "adapter.py", "myssia_snownlp_adapter_test")
        batch = [{"url": f"https://example.com/{i}", "text": "x"} for i in range(300)]
        with pytest.raises(Exception) as excinfo:
            adapter.decorate(batch)
        assert excinfo.value.code == "texts_invalid"

    def test_shim_source_compiles(self):
        adapter = load_adapter(SNOWNLP_DIR / "adapter.py", "myssia_snownlp_adapter_test")
        compile(adapter.SHIM_SOURCE, "<snownlp-shim>", "exec")


# ---------------------------------------------------------------------------
# myssia-yake
# ---------------------------------------------------------------------------


class TestYakeManifest:
    def test_manifest_declares_no_gate_and_in_process_adapter(self):
        manifest = load_manifest_file(YAKE_DIR / "plugin.yaml")
        assert manifest.id == "myssia-yake"
        assert manifest.tier == "desktop"
        assert manifest.gate is None, "上游活跃(2026-02 推送),stale 徽标失实;许可核验已过=设置面无关"
        assert manifest.vendor is None, "AGPL 上游零 vendor(只声明依赖,pip 运行时装包不构成分发)"
        assert manifest.adapter is not None
        assert manifest.adapter.mode == "in_process"
        assert manifest.modes.remote is None
        assert manifest.provides == ["keywords"]


class TestYakeAdapter:
    @pytest.fixture()
    def no_yake(self, monkeypatch):
        """宿主未装 yake:sys.modules['yake']=None 使 import yake 抛 ImportError。"""
        monkeypatch.setitem(sys.modules, "yake", None)

    @pytest.fixture()
    def fake_yake(self, monkeypatch) -> list[str]:
        """注入 fake yake 模块(零真实装载);记录喂给抽取器的文本。"""
        fed: list[str] = []

        class KeywordExtractor:
            def __init__(self, *, lan: str, n: int, top: int) -> None:
                self.ranked = [("关键词甲", 0.01), ("keyword-b", 0.02), ("噪声", 0.03)]
                self.lan = lan
                self.top = top

            def extract_keywords(self, text: str) -> list[tuple[str, float]]:
                fed.append(text)
                return self.ranked[: self.top]

        module = types.SimpleNamespace(KeywordExtractor=KeywordExtractor)
        monkeypatch.setitem(sys.modules, "yake", module)
        return fed

    def test_dependency_missing_when_not_installed(self, no_yake):
        adapter = load_adapter(YAKE_DIR / "adapter.py", "myssia_yake_adapter_test")
        with pytest.raises(Exception) as excinfo:
            adapter.decorate(SAMPLE_TEXTS)
        assert excinfo.value.code == "dependency_missing"
        assert "uv pip install yake" in excinfo.value.message

    def test_decorate_success_emits_keywords(self, fake_yake):
        adapter = load_adapter(YAKE_DIR / "adapter.py", "myssia_yake_adapter_test")
        result = adapter.decorate(SAMPLE_TEXTS)
        assert result["decorations"]["https://example.com/a"]["keywords"] == [
            "关键词甲", "keyword-b", "噪声",
        ]
        assert result["decorated"] == 2
        assert len(fake_yake) == 2, "逐条喂给抽取器(同一次构造,零重复装载)"

    def test_cjk_text_is_char_segmented_before_extraction(self, fake_yake):
        """中文连续段落先做 CJK 逐字切分(否则 segtok 把整段当单 token)。"""
        adapter = load_adapter(YAKE_DIR / "adapter.py", "myssia_yake_adapter_test")
        adapter.decorate([{"url": "https://example.com/c", "text": "白嫖攻略"}])
        assert fake_yake[0] == "白 嫖 攻 略"

    def test_normalize_text_keeps_ascii_words_intact(self):
        adapter = load_adapter(YAKE_DIR / "adapter.py", "myssia_yake_adapter_test")
        assert adapter.normalize_text("NAS 白嫖 GPU") == "NAS 白 嫖 GPU"

    def test_top_bounds_keyword_count(self, fake_yake):
        adapter = load_adapter(YAKE_DIR / "adapter.py", "myssia_yake_adapter_test")
        result = adapter.decorate(SAMPLE_TEXTS, top=1)
        assert result["decorations"]["https://example.com/a"]["keywords"] == ["关键词甲"]

    def test_empty_text_skipped_not_error(self, fake_yake):
        adapter = load_adapter(YAKE_DIR / "adapter.py", "myssia_yake_adapter_test")
        result = adapter.decorate([{"url": "https://example.com/e", "text": ""}])
        assert result["decorations"] == {}
        assert result["skipped"] == 1

    def test_input_validation_rejects_bad_shapes(self, fake_yake):
        adapter = load_adapter(YAKE_DIR / "adapter.py", "myssia_yake_adapter_test")
        for bad in ("not-a-list", [{"no_url": 1}], [{"url": "", "text": "x"}]):
            with pytest.raises(Exception) as excinfo:
                adapter.decorate(bad)
            assert excinfo.value.code == "texts_invalid"

    def test_input_validation_caps_batch_size(self, fake_yake):
        adapter = load_adapter(YAKE_DIR / "adapter.py", "myssia_yake_adapter_test")
        batch = [{"url": f"https://example.com/{i}", "text": "x"} for i in range(300)]
        with pytest.raises(Exception) as excinfo:
            adapter.decorate(batch)
        assert excinfo.value.code == "texts_invalid"


# ---------------------------------------------------------------------------
# 铁律:适配器任何失败形态不拦核心
# ---------------------------------------------------------------------------


class TestIronLaw:
    def test_core_pipeline_builds_regardless_of_analysis_plugins(self):
        """装不上不拦核心:两件失败态(uv 缺失/依赖缺失)下品类照常加载、
        Pipeline 可构造(lane 的降级注记钉在 tests/pipeline/test_analysis_lane.py)。"""
        config = load_category_file(PLUGINS_DIR / "wool.yaml")
        Pipeline(config)


# ---------------------------------------------------------------------------
# 市场面:lane 成员资格 → analysis 开关派生徽标(D10-2 最小扩展)
# ---------------------------------------------------------------------------

#: 假市场里的 lane 成员对(snownlp 带 stale gate / yake 无 gate)与对照件。
SNOWNLP_MANIFEST_YAML = """
id: myssia-snownlp
name: 中文情感装饰(snownlp)
version: 1.0.0
compatible: ">=0.0.1,<0.1"
tier: desktop
gate: stale
provides: [sentiment]
modes:
  local:
    install: myssia plugin install plugins/myssia-snownlp
install:
  source: https://github.com/xinzhuzi/myia.git
"""

YAKE_MANIFEST_YAML = """
id: myssia-yake
name: 关键词装饰(yake)
version: 1.0.0
compatible: ">=0.0.1,<0.1"
tier: desktop
provides: [keywords]
modes:
  local:
    install: myssia plugin install plugins/myssia-yake
install:
  source: https://github.com/xinzhuzi/myia.git
"""


def _make_market(tmp_path: Path, *manifests: str) -> Path:
    import yaml

    market = tmp_path / "market"
    for text in manifests:
        data = yaml.safe_load(text)
        plugin_dir = market / str(data["id"])
        plugin_dir.mkdir(parents=True)
        (plugin_dir / "plugin.yaml").write_text(text, encoding="utf-8")
    return market


def _run_cli(capsys, *argv: str):
    import json as json_module

    from myssia.cli import main

    code = main(list(argv))
    out = capsys.readouterr().out
    return code, json_module.loads(out) if out.strip() else None


class TestMarketLaneBadges:
    def test_lane_badges_derived_from_analysis_switches(self, tmp_path, capsys):
        """lane 成员徽标按 lane 成员资格派生自 analysis.<key>(yake 无 gate 也有徽标)。"""
        market = _make_market(
            tmp_path, SNOWNLP_MANIFEST_YAML, YAKE_MANIFEST_YAML, """
id: myssia-plain
name: 普通件
version: 1.0.0
compatible: ">=0.0.1,<0.1"
tier: desktop
provides: [plain]
modes:
  local:
    install: echo ok
install:
  source: https://github.com/xinzhuzi/myia.git
""")
        gates_file = tmp_path / "gates.yaml"
        gates_file.write_text("analysis:\n  yake: true\n", encoding="utf-8")
        code, payload = _run_cli(
            capsys, "plugin", "list", "--dir", str(market), "--gates-file", str(gates_file), "--json"
        )
        assert code == 0
        lane = {item["id"]: item for item in payload["gates"]["analysis_lane"]}
        assert set(lane) == {"myssia-snownlp", "myssia-yake"}
        assert lane["myssia-yake"] == {"id": "myssia-yake", "key": "yake", "enabled": True}
        assert lane["myssia-snownlp"]["enabled"] is False  # gate 关 = 徽标未启用
        by_id = {plugin["id"]: plugin for plugin in payload["plugins"]}
        assert by_id["myssia-yake"]["analysis_lane"]["enabled"] is True
        assert by_id["myssia-plain"]["analysis_lane"] is None, "非 lane 成员无徽标"

    def test_doctor_lane_disabled_is_info_and_gate_member_not_doubled(self, tmp_path, capsys):
        """doctor:yake 未启用 = info(yake 无 gate 也要可见);snownlp 只报 gate_disabled 不双报。"""
        market = _make_market(tmp_path, SNOWNLP_MANIFEST_YAML, YAKE_MANIFEST_YAML)
        gates_file = tmp_path / "gates.yaml"  # 不存在 = 全关
        plugins_dir = tmp_path / "plugins"
        plugins_dir.mkdir()
        code, payload = _run_cli(
            capsys,
            "doctor",
            "--plugins-dir", str(plugins_dir),
            "--db", str(tmp_path / "myssia.db"),
            "--dir", str(market),
            "--gates-file", str(gates_file),
            "--json",
        )
        assert code == 0
        lane_disabled = [f for f in payload["findings"] if f["code"] == "analysis_lane_disabled"]
        assert [f["scope"] for f in lane_disabled] == ["plugin:myssia-yake"]
        assert lane_disabled[0]["severity"] == "info"
        # snownlp(声明 gate: stale)只走 gate_disabled,不双报
        gate_disabled = [f for f in payload["findings"] if f["code"] == "gate_disabled"]
        assert [f["scope"] for f in gate_disabled] == ["plugin:myssia-snownlp"]
        lane_section = payload["gates"]["analysis_lane"]
        assert {item["id"]: item["enabled"] for item in lane_section} == {
            "myssia-snownlp": False,
            "myssia-yake": False,
        }

    def test_doctor_lane_enabled_no_finding(self, tmp_path, capsys):
        """lane 件启用后不再产 info(与 gate_disabled 同纪律)。"""
        market = _make_market(tmp_path, YAKE_MANIFEST_YAML)
        gates_file = tmp_path / "gates.yaml"
        gates_file.write_text("analysis:\n  yake: true\n", encoding="utf-8")
        plugins_dir = tmp_path / "plugins"
        plugins_dir.mkdir()
        code, payload = _run_cli(
            capsys,
            "doctor",
            "--plugins-dir", str(plugins_dir),
            "--db", str(tmp_path / "myssia.db"),
            "--dir", str(market),
            "--gates-file", str(gates_file),
            "--json",
        )
        assert code == 0
        assert not [f for f in payload["findings"] if f["code"] == "analysis_lane_disabled"]
