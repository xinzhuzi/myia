"""myssia-maigret 场景件契约测试(10-05-plugin-market-batch 首批).

被钉住的契约:

1. **manifest**:声明 adapter(subprocess)且无 vendor(MIT 上游不 vendor);
   tier=desktop、modes 走 local 安装命令(上游是 CLI 库,无 remote endpoint);
2. **适配器 mock 子进程**:命令形状(uv 隔离环境+``-J simple``+folderoutput+
   top-sites 预算)、成功装配结构化 JSON(含零命中空态)、报告解析契约
   (命中对象在条目 ``status`` 键下——2026-10-05 对 v0.6.6 实测)、非零退出/
   超时/报告缺失或损坏/用户名非法/uv 缺失 —— 每种失败都是结构化
   :class:`MaigretAdapterError`;
3. **CLI ``myssia maigret`` + 铁律**:成功退 0、采集失败退 2、适配器缺失退 1;
   任何失败形态下核心品类加载与 Pipeline 构造完全无感(装不上不拦核心)。

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
    MAIGRET_FETCH_FAILURE_CODES,
    _import_plugin_adapter,
    main,
)
from myssia.pipeline import Pipeline
from myssia.plugins.manifest import load_manifest_file
from myssia.schema import load_category_file

REPO_ROOT = Path(__file__).resolve().parents[2]
PLUGINS_DIR = REPO_ROOT / "plugins"
PLUGIN_DIR = PLUGINS_DIR / "myssia-maigret"
PLUGIN_ADAPTER = PLUGIN_DIR / "adapter.py"

STUB_ADAPTER = '''\
"""stub maigret adapter(CLI 接线测试专用;不触网)."""
RAISE = None
PAYLOAD = {
    "plugin": "myssia-maigret",
    "target": "unset",
    "status": "success",
    "hit_count": 0,
    "hits": [],
}
def run(username, **kwargs):
    if RAISE is not None:
        class Err(Exception):
            def __init__(self, code, message, **details):
                super().__init__(message)
                self.code, self.message, self.details = code, message, details
            def to_dict(self):
                return {"code": self.code, "message": self.message, **self.details}
        raise Err(RAISE, RAISE, exit_code=1)
    payload = dict(PAYLOAD)
    payload["target"] = username
    return payload
'''


def load_adapter() -> Any:
    import types

    module = types.ModuleType("myssia_maigret_adapter_test")
    module.__file__ = str(PLUGIN_ADAPTER)
    exec(  # noqa: S102 - 仓库内受控代码
        compile(PLUGIN_ADAPTER.read_text(encoding="utf-8"), str(PLUGIN_ADAPTER), "exec"),
        module.__dict__,
    )
    return module


def make_stub_plugin(tmp_path: Path, *, raise_code: str | None = None) -> Path:
    plugins = tmp_path / "plugins"
    plugin = plugins / "myssia-maigret"
    plugin.mkdir(parents=True)
    source = STUB_ADAPTER
    if raise_code:
        source = source.replace("RAISE = None", f"RAISE = {raise_code!r}")
    (plugin / "adapter.py").write_text(source, encoding="utf-8")
    return plugins


def _report_path(command: list[str]) -> Path:
    """从命令行参数里取 --folderoutput 目录(mock runner 写报告的目标)."""
    return Path(command[command.index("--folderoutput") + 1])


def _runner_writing_report(report: dict[str, Any], *, returncode: int = 0) -> Any:
    """fake runner:退出码可配;成功时把报告 JSON 写进 folderoutput."""

    def _run(command: list[str], **kwargs: Any) -> subprocess.CompletedProcess[str]:
        if returncode == 0:
            output_dir = _report_path(command)
            output_dir.mkdir(parents=True, exist_ok=True)
            (output_dir / "report_x_simple.json").write_text(
                json.dumps(report), encoding="utf-8"
            )
        return subprocess.CompletedProcess(command, returncode, "", "")

    return _run


def _sample_report() -> dict[str, Any]:
    """实测形状(v0.6.6):命中对象在条目 status 键下,未命中为 None."""
    return {
        "WordPress": {
            "username": "torvalds",
            "rank": 34,
            "is_similar": False,
            "http_status": 200,
            "status": {
                "username": "torvalds",
                "site_name": "WordPress",
                "url": "https://torvalds.wordpress.com/",
                "status": "Claimed",
                "ids": {"uid": "123", "follower_count": "18", "blob": {"nested": 1}},
                "tags": ["blog", "tech"],
            },
        },
        "NoSuchSite": {
            "username": "torvalds",
            "rank": 99999,
            "status": None,
        },
    }


class TestMaigretManifest:
    def test_manifest_declares_subprocess_adapter_without_vendor(self):
        manifest = load_manifest_file(PLUGIN_DIR / "plugin.yaml")
        assert manifest.id == "myssia-maigret"
        assert manifest.tier == "desktop"
        assert manifest.vendor is None, "MIT 上游不 vendor(pip 依赖隔离调用)"
        assert manifest.adapter is not None
        assert manifest.adapter.mode == "subprocess"
        assert manifest.modes.remote is None
        assert manifest.modes.local is not None
        assert manifest.modes.local.install.startswith("myssia plugin install")


class TestMaigretAdapter:
    def test_build_command_is_isolated_uv_with_simple_report(self, tmp_path):
        adapter = load_adapter()
        command = adapter.build_command("torvalds", tmp_path)
        assert command[:3] == ["uv", "run", "--no-project"]
        assert "--with" in command and "maigret" in command
        assert command[command.index("-J") + 1] == "simple"
        assert command[command.index("--folderoutput") + 1] == str(tmp_path)
        assert "--no-color" in command and "--no-progressbar" in command
        assert command[command.index("--top-sites") + 1] == "100"
        assert command[command.index("--timeout") + 1] == "15.0"
        assert "torvalds" in command

    def test_build_command_drops_top_sites_when_none(self, tmp_path):
        adapter = load_adapter()
        command = adapter.build_command("torvalds", tmp_path, top_sites=None)
        assert "--top-sites" not in command

    def test_run_success_parses_hits_from_status_key(self):
        adapter = load_adapter()
        payload = adapter.run(
            "torvalds", runner=_runner_writing_report(_sample_report())
        )
        assert payload["status"] == "success"
        assert payload["plugin"] == "myssia-maigret"
        assert payload["hit_count"] == 1
        hit = payload["hits"][0]
        assert hit["site"] == "WordPress"
        assert hit["url"] == "https://torvalds.wordpress.com/"
        assert hit["status"] == "Claimed"
        assert hit["rank"] == 34
        # ids 只保留标量值(嵌套 blob 剔除)
        assert hit["ids"] == {"uid": "123", "follower_count": "18"}

    def test_run_zero_hits_is_success_empty_state(self):
        adapter = load_adapter()
        payload = adapter.run(
            "nobody", runner=_runner_writing_report({"SiteA": {"status": None}})
        )
        assert payload["status"] == "success"
        assert payload["hit_count"] == 0 and payload["hits"] == []

    @pytest.mark.parametrize("username", ["", "-x", "a b", "okay;rm", "x" * 65])
    def test_invalid_username_rejected_before_any_process(self, username):
        adapter = load_adapter()
        with pytest.raises(adapter.MaigretAdapterError) as exc_info:
            adapter.run(username)
        assert exc_info.value.code == "username_invalid"

    def test_nonzero_exit_maps_to_maigret_failed(self):
        adapter = load_adapter()
        with pytest.raises(adapter.MaigretAdapterError) as exc_info:
            adapter.run(
                "torvalds",
                runner=_runner_writing_report({}, returncode=1),
            )
        assert exc_info.value.code == "maigret_failed"

    def test_timeout_maps_to_maigret_timeout(self):
        adapter = load_adapter()

        def _hang(command: list[str], **kwargs: Any) -> Any:
            raise subprocess.TimeoutExpired(command, kwargs.get("timeout", 1))

        with pytest.raises(adapter.MaigretAdapterError) as exc_info:
            adapter.run("torvalds", timeout=0.5, runner=_hang)
        assert exc_info.value.code == "maigret_timeout"

    def test_missing_report_maps_to_report_missing(self):
        adapter = load_adapter()

        def _silent(command: list[str], **kwargs: Any) -> Any:
            return subprocess.CompletedProcess(command, 0, "", "")

        with pytest.raises(adapter.MaigretAdapterError) as exc_info:
            adapter.run("torvalds", runner=_silent)
        assert exc_info.value.code == "maigret_report_missing"

    def test_corrupt_report_maps_to_report_invalid(self):
        adapter = load_adapter()

        def _corrupt(command: list[str], **kwargs: Any) -> Any:
            output_dir = _report_path(command)
            output_dir.mkdir(parents=True, exist_ok=True)
            (output_dir / "report_x_simple.json").write_text("not-json", encoding="utf-8")
            return subprocess.CompletedProcess(command, 0, "", "")

        with pytest.raises(adapter.MaigretAdapterError) as exc_info:
            adapter.run("torvalds", runner=_corrupt)
        assert exc_info.value.code == "maigret_report_invalid"

    def test_uv_missing_is_structured(self, monkeypatch):
        adapter = load_adapter()
        monkeypatch.setattr(adapter.shutil, "which", lambda name: None)
        with pytest.raises(adapter.MaigretAdapterError) as exc_info:
            adapter.run("torvalds")
        assert exc_info.value.code == "uv_missing"


class TestCliMaigret:
    def test_success_json_contract(self, tmp_path, capsys):
        plugins = make_stub_plugin(tmp_path)
        code = main(["maigret", "torvalds", "--plugins-dir", str(plugins), "--json"])
        assert code == EXIT_OK
        payload = json.loads(capsys.readouterr().out)
        assert payload["plugin"] == "myssia-maigret"
        assert payload["target"] == "torvalds"
        assert payload["status"] == "success"

    def test_maigret_failure_exits_2(self, tmp_path, capsys):
        plugins = make_stub_plugin(tmp_path, raise_code="maigret_failed")
        code = main(["maigret", "torvalds", "--plugins-dir", str(plugins), "--json"])
        assert code == EXIT_FETCH_ALL_FAILED
        assert json.loads(capsys.readouterr().out)["error"] == "maigret_failed"

    def test_config_failure_exits_1(self, tmp_path, capsys):
        plugins = make_stub_plugin(tmp_path, raise_code="username_invalid")
        # 带空格的用户名:argparse 收作位置参数,适配器侧校验拒(username_invalid)。
        code = main(
            ["maigret", "a b", "--plugins-dir", str(plugins), "--json"]
        )
        assert code == EXIT_CONFIG_ERROR
        assert json.loads(capsys.readouterr().out)["error"] == "username_invalid"

    def test_adapter_file_missing_exits_1(self, tmp_path, capsys):
        plugins = tmp_path / "plugins"
        plugins.mkdir()
        code = main(["maigret", "torvalds", "--plugins-dir", str(plugins), "--json"])
        assert code == EXIT_CONFIG_ERROR
        assert (
            json.loads(capsys.readouterr().out)["error"] == "maigret_adapter_missing"
        )

    def test_import_adapter_from_repo_plugins_dir(self):
        module = _import_plugin_adapter(PLUGINS_DIR, "myssia-maigret")
        assert module.PLUGIN_DIR.name == "myssia-maigret"

    def test_fetch_failure_codes_are_the_collection_family(self):
        assert MAIGRET_FETCH_FAILURE_CODES == frozenset(
            {
                "maigret_failed",
                "maigret_timeout",
                "maigret_report_missing",
                "maigret_report_invalid",
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
            main(["maigret", "torvalds", "--plugins-dir", str(plugins), "--json"])
            == EXIT_CONFIG_ERROR
        )
        self._assert_core_unblocked()

    def test_adapter_failure_keeps_core_unblocked(self, tmp_path):
        plugins = make_stub_plugin(tmp_path, raise_code="maigret_failed")
        assert (
            main(["maigret", "torvalds", "--plugins-dir", str(plugins), "--json"])
            == EXIT_FETCH_ALL_FAILED
        )
        self._assert_core_unblocked()
