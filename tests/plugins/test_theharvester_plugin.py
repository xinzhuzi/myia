"""myssia-theharvester 场景件契约测试(10-05-plugin-market-batch 首批).

被钉住的契约:

1. **manifest**:声明 vendor(GPL-2.0 submodule pin=4.9.2)+ adapter(subprocess);
   tier=desktop;pin 选型记录(master 49a38f8d 含 Python2 语法残留不可运行);
2. **submodule 形状**:vendor/theHarvester 以 gitlink(160000)入库并等于
   manifest 的 pin —— GPL 上游零代码复制的仓库级证据;依赖钉版清单与
   4.9.2 pyproject 逐条同源;
3. **适配器 mock 子进程**:命令形状(uv --no-config 隔离+-c 唤起上游入口+
   -f JSON 落盘)、成功装配(列表分桶+totals)、零命中空态、非零退出/超时/
   报告缺失或损坏/目标与源清单非法/vendor 缺失/uv 缺失 —— 每种失败都是
   结构化 :class:`HarvesterAdapterError`;
4. **CLI ``myssia harvester`` + 铁律**:成功退 0、采集失败退 2、适配器
   缺失退 1;任何失败形态下核心品类加载与 Pipeline 构造完全无感。

测试纪律:子进程一律注入 fake runner(mock,fake 自写报告文件),零真实
网络、零真实 uv;每测独立 tmp_path。
"""

from __future__ import annotations

import json
import subprocess
from pathlib import Path
from typing import Any

import pytest

from myssia.cli import (
    EXIT_CONFIG_ERROR,
    EXIT_FETCH_ALL_FAILED,
    EXIT_OK,
    HARVESTER_FETCH_FAILURE_CODES,
    _import_plugin_adapter,
    main,
)
from myssia.pipeline import Pipeline
from myssia.plugins.manifest import load_manifest_file
from myssia.schema import load_category_file

REPO_ROOT = Path(__file__).resolve().parents[2]
PLUGINS_DIR = REPO_ROOT / "plugins"
PLUGIN_DIR = PLUGINS_DIR / "myssia-theharvester"
PLUGIN_ADAPTER = PLUGIN_DIR / "adapter.py"
#: pin 选型:release 4.9.2(master 49a38f8d 语法坏,见 plugin.yaml 注记)。
EXPECTED_PIN = "ba85366644131d5f170cc7016d4ed99b9817889a"

STUB_ADAPTER = '''\
"""stub theharvester adapter(CLI 接线测试专用;不触网)."""
RAISE = None
PAYLOAD = {
    "plugin": "myssia-theharvester",
    "target": "unset",
    "status": "success",
    "results": {},
    "result_totals": {},
}
def run(domain, **kwargs):
    if RAISE is not None:
        class Err(Exception):
            def __init__(self, code, message, **details):
                super().__init__(message)
                self.code, self.message, self.details = code, message, details
            def to_dict(self):
                return {"code": self.code, "message": self.message, **self.details}
        raise Err(RAISE, RAISE, exit_code=1)
    payload = dict(PAYLOAD)
    payload["target"] = domain
    return payload
'''


def load_adapter() -> Any:
    import types

    module = types.ModuleType("myssia_theharvester_adapter_test")
    module.__file__ = str(PLUGIN_ADAPTER)
    exec(  # noqa: S102 - 仓库内受控代码
        compile(PLUGIN_ADAPTER.read_text(encoding="utf-8"), str(PLUGIN_ADAPTER), "exec"),
        module.__dict__,
    )
    return module


def make_stub_plugin(tmp_path: Path, *, raise_code: str | None = None) -> Path:
    plugins = tmp_path / "plugins"
    plugin = plugins / "myssia-theharvester"
    plugin.mkdir(parents=True)
    source = STUB_ADAPTER
    if raise_code:
        source = source.replace("RAISE = None", f"RAISE = {raise_code!r}")
    (plugin / "adapter.py").write_text(source, encoding="utf-8")
    return plugins


def _report_prefix(command: list[str]) -> Path:
    return Path(command[command.index("-f") + 1])


def _runner_writing_report(report: dict[str, Any], *, returncode: int = 0) -> Any:
    def _run(command: list[str], **kwargs: Any) -> subprocess.CompletedProcess[str]:
        if returncode == 0:
            _report_prefix(command).with_suffix(".json").write_text(
                json.dumps(report), encoding="utf-8"
            )
        return subprocess.CompletedProcess(command, returncode, "", "")

    return _run


class TestHarvesterManifest:
    def test_manifest_declares_vendor_and_subprocess_adapter(self):
        manifest = load_manifest_file(PLUGIN_DIR / "plugin.yaml")
        assert manifest.id == "myssia-theharvester"
        assert manifest.tier == "desktop"
        assert manifest.vendor is not None
        assert manifest.vendor.license == "GPL-2.0"
        assert manifest.vendor.pin == EXPECTED_PIN
        assert manifest.adapter is not None
        assert manifest.adapter.mode == "subprocess"
        assert manifest.modes.remote is None
        assert manifest.modes.local is not None


class TestSubmoduleShape:
    def test_vendor_is_gitlink_pinned_to_manifest_pin(self):
        """gitlink(160000)入库且等于 manifest pin —— GPL 零复制的仓库级证据."""
        completed = subprocess.run(
            ["git", "ls-files", "-s", "plugins/myssia-theharvester/vendor/theHarvester"],
            capture_output=True,
            text=True,
            check=True,
            cwd=REPO_ROOT,
        )
        fields = completed.stdout.split()
        assert fields[0] == "160000", "vendor 必须以 gitlink(submodule)入库"
        assert fields[1] == EXPECTED_PIN

    def test_gitmodules_declares_theharvester_submodule(self):
        content = (REPO_ROOT / ".gitmodules").read_text(encoding="utf-8")
        assert "plugins/myssia-theharvester/vendor/theHarvester" in content
        assert "https://github.com/laramies/theHarvester" in content

    def test_pinned_dependencies_match_vendor_pyproject(self):
        """适配器钉版清单与 4.9.2 vendor pyproject 的 dependencies 逐条同源."""
        adapter = load_adapter()
        pyproject = PLUGIN_DIR / "vendor/theHarvester/pyproject.toml"
        if not pyproject.is_file():  # CI 未 init submodule:形状断言在上一测钉住
            pytest.skip("vendor submodule 未初始化(CI)")
        import tomllib

        expected = {
            dep for dep in tomllib.load(open(pyproject, "rb"))["project"]["dependencies"]
            if ";" not in dep
        }
        got = {
            dep
            for dep in adapter.THEHARVESTER_DEPENDENCIES
            if ";" not in dep
        }
        assert got == expected, "钉版依赖漂移(vendor pyproject 改了?重钉)"


class TestHarvesterAdapter:
    def test_build_command_is_isolated_uv_c_entry(self):
        adapter = load_adapter()
        command = adapter.build_command(
            "example.com", "crtsh,dnsdumpster", "/tmp/harvest"
        )
        assert command[:4] == ["uv", "run", "--no-config", "--no-project"]
        assert command.count("--with") == len(adapter.THEHARVESTER_DEPENDENCIES)
        assert command[command.index("-c") + 1] == adapter.ENTRY_SNIPPET
        assert command[command.index("-d") + 1] == "example.com"
        assert command[command.index("-b") + 1] == "crtsh,dnsdumpster"
        assert command[command.index("-f") + 1] == "/tmp/harvest"
        assert "-q" in command

    def test_run_success_buckets_list_fields(self, tmp_path):
        adapter = load_adapter()
        report = {
            "cmd": "theHarvester -d example.com",
            "emails": ["admin@example.com"],
            "hosts": ["www.example.com", "example.com"],
            "shodan": [],
        }
        payload = adapter.run(
            "example.com", plugin_dir=_plugin_with_vendor(tmp_path),
            runner=_runner_writing_report(report),
        )
        assert payload["status"] == "success"
        assert payload["results"]["emails"] == ["admin@example.com"]
        assert payload["result_totals"] == {"emails": 1, "hosts": 2, "shodan": 0}
        assert "cmd" not in payload["results"], "非列表字段(cmd)不进分桶"

    def test_run_zero_hits_is_success_empty_state(self, tmp_path):
        adapter = load_adapter()
        payload = adapter.run(
            "example.com",
            plugin_dir=_plugin_with_vendor(tmp_path),
            runner=_runner_writing_report({"cmd": "x", "hosts": []}),
        )
        assert payload["status"] == "success"
        assert payload["result_totals"] == {"hosts": 0}

    @pytest.mark.parametrize("domain", ["", "-d", "a b", "x;y", "例.com"])
    def test_invalid_domain_rejected_before_any_process(self, domain):
        adapter = load_adapter()
        with pytest.raises(adapter.HarvesterAdapterError) as exc_info:
            adapter.run(domain)
        assert exc_info.value.code == "domain_invalid"

    def test_invalid_sources_rejected(self, tmp_path):
        adapter = load_adapter()
        with pytest.raises(adapter.HarvesterAdapterError) as exc_info:
            adapter.run(
                "example.com",
                sources="--evil",
                plugin_dir=_plugin_with_vendor(tmp_path),
            )
        assert exc_info.value.code == "domain_invalid"

    def test_vendor_missing_is_structured(self, tmp_path):
        adapter = load_adapter()
        empty = tmp_path / "plugins/myssia-theharvester"
        empty.mkdir(parents=True)
        with pytest.raises(adapter.HarvesterAdapterError) as exc_info:
            adapter.run("example.com", plugin_dir=empty)
        assert exc_info.value.code == "vendor_missing"
        assert "git submodule update --init" in exc_info.value.message

    def test_uv_missing_is_structured(self, tmp_path, monkeypatch):
        adapter = load_adapter()
        monkeypatch.setattr(adapter.shutil, "which", lambda name: None)
        with pytest.raises(adapter.HarvesterAdapterError) as exc_info:
            adapter.run(
                "example.com", plugin_dir=_plugin_with_vendor(tmp_path)
            )
        assert exc_info.value.code == "uv_missing"

    def test_nonzero_exit_maps_to_harvester_failed(self, tmp_path):
        adapter = load_adapter()
        with pytest.raises(adapter.HarvesterAdapterError) as exc_info:
            adapter.run(
                "example.com",
                plugin_dir=_plugin_with_vendor(tmp_path),
                runner=_runner_writing_report({}, returncode=1),
            )
        assert exc_info.value.code == "harvester_failed"

    def test_timeout_maps_to_harvester_timeout(self, tmp_path):
        adapter = load_adapter()

        def _hang(command: list[str], **kwargs: Any) -> Any:
            raise subprocess.TimeoutExpired(command, kwargs.get("timeout", 1))

        with pytest.raises(adapter.HarvesterAdapterError) as exc_info:
            adapter.run(
                "example.com",
                timeout=0.5,
                plugin_dir=_plugin_with_vendor(tmp_path),
                runner=_hang,
            )
        assert exc_info.value.code == "harvester_timeout"

    def test_missing_report_maps_to_report_missing(self, tmp_path):
        adapter = load_adapter()

        def _silent(command: list[str], **kwargs: Any) -> Any:
            return subprocess.CompletedProcess(command, 0, "", "")

        with pytest.raises(adapter.HarvesterAdapterError) as exc_info:
            adapter.run(
                "example.com",
                plugin_dir=_plugin_with_vendor(tmp_path),
                runner=_silent,
            )
        assert exc_info.value.code == "harvester_report_missing"

    def test_corrupt_report_maps_to_report_invalid(self, tmp_path):
        adapter = load_adapter()

        def _corrupt(command: list[str], **kwargs: Any) -> Any:
            _report_prefix(command).with_suffix(".json").write_text(
                "not-json", encoding="utf-8"
            )
            return subprocess.CompletedProcess(command, 0, "", "")

        with pytest.raises(adapter.HarvesterAdapterError) as exc_info:
            adapter.run(
                "example.com",
                plugin_dir=_plugin_with_vendor(tmp_path),
                runner=_corrupt,
            )
        assert exc_info.value.code == "harvester_report_invalid"


def _plugin_with_vendor(tmp_path: Path) -> Path:
    """带 vendor 判据的插件目录(只造 theHarvester/theHarvester.py 存在性,
    不需要真 submodule —— 子进程本身是 mock)。"""
    plugin = tmp_path / "plugins/myssia-theharvester"
    (plugin / "vendor/theHarvester/theHarvester").mkdir(parents=True, exist_ok=True)
    (plugin / "vendor/theHarvester/theHarvester/theHarvester.py").write_text(
        "# stub vendor marker\n", encoding="utf-8"
    )
    return plugin


class TestCliHarvester:
    def test_success_json_contract(self, tmp_path, capsys):
        plugins = make_stub_plugin(tmp_path)
        code = main(["harvester", "example.com", "--plugins-dir", str(plugins), "--json"])
        assert code == EXIT_OK
        payload = json.loads(capsys.readouterr().out)
        assert payload["plugin"] == "myssia-theharvester"
        assert payload["target"] == "example.com"

    def test_harvester_failure_exits_2(self, tmp_path, capsys):
        plugins = make_stub_plugin(tmp_path, raise_code="harvester_failed")
        code = main(["harvester", "example.com", "--plugins-dir", str(plugins), "--json"])
        assert code == EXIT_FETCH_ALL_FAILED
        assert json.loads(capsys.readouterr().out)["error"] == "harvester_failed"

    def test_config_failure_exits_1(self, tmp_path, capsys):
        plugins = make_stub_plugin(tmp_path, raise_code="vendor_missing")
        code = main(["harvester", "example.com", "--plugins-dir", str(plugins), "--json"])
        assert code == EXIT_CONFIG_ERROR
        assert json.loads(capsys.readouterr().out)["error"] == "vendor_missing"

    def test_adapter_file_missing_exits_1(self, tmp_path, capsys):
        plugins = tmp_path / "plugins"
        plugins.mkdir()
        code = main(["harvester", "example.com", "--plugins-dir", str(plugins), "--json"])
        assert code == EXIT_CONFIG_ERROR
        assert (
            json.loads(capsys.readouterr().out)["error"] == "harvester_adapter_missing"
        )

    def test_fetch_failure_codes_are_the_collection_family(self):
        assert HARVESTER_FETCH_FAILURE_CODES == frozenset(
            {
                "harvester_failed",
                "harvester_timeout",
                "harvester_report_missing",
                "harvester_report_invalid",
            }
        )


class TestIronLawAdapterNeverBlocksCore:
    """铁律回归:适配器任何装不上/失败形态,核心品类流水线完全无感。"""

    @staticmethod
    def _assert_core_unblocked() -> None:
        for path in sorted(PLUGINS_DIR.glob("*.yaml")):
            config = load_category_file(path)
            assert config.sources, f"{path.name} 必须可加载且有源"
        Pipeline(load_category_file(PLUGINS_DIR / "wool.yaml"))

    def test_adapter_missing_keeps_core_unblocked(self, tmp_path):
        plugins = tmp_path / "plugins"
        plugins.mkdir()
        assert (
            main(["harvester", "example.com", "--plugins-dir", str(plugins), "--json"])
            == EXIT_CONFIG_ERROR
        )
        self._assert_core_unblocked()

    def test_adapter_failure_keeps_core_unblocked(self, tmp_path):
        plugins = make_stub_plugin(tmp_path, raise_code="harvester_failed")
        assert (
            main(["harvester", "example.com", "--plugins-dir", str(plugins), "--json"])
            == EXIT_FETCH_ALL_FAILED
        )
        self._assert_core_unblocked()
