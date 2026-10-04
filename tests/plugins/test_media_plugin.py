"""myssia-media 场景件契约测试(10-05-plugin-market-batch 首批).

被钉住的契约:

1. **manifest**:声明 adapter(subprocess)且无 vendor(公域上游不 vendor);
   tier=desktop、modes 走 local 安装命令(上游是 CLI 库,无 remote endpoint);
2. **适配器 mock 子进程**:命令形状(uv 隔离环境+扁平快扫旗标+预算前置)、
   成功装配结构化 JSON(单视频/频道列表/截断)、非零退出/超时/输出损坏/
   目标非法/uv 缺失 —— 每种失败都是结构化 :class:`MediaAdapterError`;
3. **CLI ``myssia media`` + 铁律**:成功退 0、采集失败退 2、适配器缺失退 1;
   任何失败形态下核心品类加载与 Pipeline 构造完全无感(装不上不拦核心)。

测试纪律:子进程一律注入 fake runner(mock),零真实网络、零真实 uv;
每测独立 tmp_path。
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
    MEDIA_FETCH_FAILURE_CODES,
    _import_plugin_adapter,
    main,
)
from myssia.pipeline import Pipeline
from myssia.plugins.manifest import load_manifest_file
from myssia.schema import load_category_file

REPO_ROOT = Path(__file__).resolve().parents[2]
PLUGINS_DIR = REPO_ROOT / "plugins"
PLUGIN_DIR = PLUGINS_DIR / "myssia-media"
PLUGIN_ADAPTER = PLUGIN_DIR / "adapter.py"

#: CLI 级测试用的桩适配器(与 CLI 的调用合同同形:run(target, **kw))。
STUB_ADAPTER = '''\
"""stub media adapter(CLI 接线测试专用;不触网)."""
RAISE = None
PAYLOAD = {
    "plugin": "myssia-media",
    "target": "stub://unset",
    "status": "success",
    "entries": [],
}
def run(target, **kwargs):
    if RAISE is not None:
        class Err(Exception):
            def __init__(self, code, message, **details):
                super().__init__(message)
                self.code, self.message, self.details = code, message, details
            def to_dict(self):
                return {"code": self.code, "message": self.message, **self.details}
        raise Err(RAISE, RAISE, exit_code=1)
    payload = dict(PAYLOAD)
    payload["target"] = target
    return payload
'''


def load_adapter() -> Any:
    """真适配器(compile+exec 加载,与 CLI 同路;仓库内受控代码)."""
    import types

    module = types.ModuleType("myssia_media_adapter_test")
    module.__file__ = str(PLUGIN_ADAPTER)
    exec(  # noqa: S102 - 仓库内受控代码
        compile(PLUGIN_ADAPTER.read_text(encoding="utf-8"), str(PLUGIN_ADAPTER), "exec"),
        module.__dict__,
    )
    return module


def make_stub_plugin(tmp_path: Path, *, raise_code: str | None = None) -> Path:
    plugins = tmp_path / "plugins"
    plugin = plugins / "myssia-media"
    plugin.mkdir(parents=True)
    source = STUB_ADAPTER
    if raise_code:
        source = source.replace("RAISE = None", f"RAISE = {raise_code!r}")
    (plugin / "adapter.py").write_text(source, encoding="utf-8")
    return plugins


def _fake_runner(
    *, returncode: int = 0, stdout: str = "", stderr: str = ""
) -> Any:
    def _run(command: list[str], **kwargs: Any) -> subprocess.CompletedProcess[str]:
        return subprocess.CompletedProcess(command, returncode, stdout, stderr)

    return _run


class TestMediaManifest:
    def test_manifest_declares_subprocess_adapter_without_vendor(self):
        manifest = load_manifest_file(PLUGIN_DIR / "plugin.yaml")
        assert manifest.id == "myssia-media"
        assert manifest.tier == "desktop"
        assert manifest.vendor is None, "公域上游不 vendor(yt-dlp 以 pip 依赖隔离调用)"
        assert manifest.adapter is not None
        assert manifest.adapter.mode == "subprocess"
        assert manifest.adapter.entry == "adapter.py"
        # 上游是 CLI 库:无 remote endpoint,market 面走 local 安装命令。
        assert manifest.modes.remote is None
        assert manifest.modes.local is not None
        assert manifest.modes.local.compose is None
        assert manifest.modes.local.install.startswith("myssia plugin install")


class TestMediaAdapter:
    def test_build_command_is_isolated_uv_flat_scan(self):
        adapter = load_adapter()
        command = adapter.build_command("https://example.com/video")
        assert command[:3] == ["uv", "run", "--no-project"]
        assert "--with" in command and "yt-dlp" in command
        assert "--dump-single-json" in command and "--flat-playlist" in command
        assert command[-1] == "https://example.com/video"
        assert "--playlist-end" not in command, "无 max_items 不加预算旗标"

    def test_build_command_prepends_playlist_end_budget(self):
        adapter = load_adapter()
        command = adapter.build_command("https://example.com/c", max_items=25)
        assert command[command.index("--playlist-end") + 1] == "25"

    def test_run_single_video_assembles_payload(self):
        adapter = load_adapter()
        upstream = json.dumps(
            {
                "id": "abc123",
                "title": "示例视频",
                "uploader": "示例频道",
                "view_count": 1024,
                "duration": 61,
                "upload_date": "20261001",
                "entries": None,
                # 白名单外的字段必须被丢弃(输出有界)
                "description": "x" * 10_000,
            }
        )
        payload = adapter.run(
            "https://example.com/watch?v=abc123", runner=_fake_runner(stdout=upstream)
        )
        assert payload["status"] == "success"
        assert payload["plugin"] == "myssia-media"
        assert payload["entry_count"] == 1 and payload["entry_total"] == 1
        entry = payload["entries"][0]
        assert entry["id"] == "abc123" and entry["view_count"] == 1024
        assert all(key in adapter.ENTRY_FIELDS for key in entry)
        assert payload["meta"]["uploader"] == "示例频道"

    def test_run_channel_truncates_entries_and_reports_total(self):
        adapter = load_adapter()
        entries = [
            {"id": f"v{i}", "url": f"https://example.com/v{i}", "title": f"第 {i} 期"}
            for i in range(120)
        ]
        upstream = json.dumps({"title": "频道", "channel": "频道", "entries": entries})
        payload = adapter.run(
            "https://example.com/@c", max_items=50, runner=_fake_runner(stdout=upstream)
        )
        assert payload["entry_total"] == 120
        assert payload["entry_count"] == 50
        assert payload["entries"][-1]["id"] == "v49"

    @pytest.mark.parametrize("target", ["", "example.com", "ftp://x/y", "not a url"])
    def test_invalid_target_rejected_before_any_process(self, target):
        adapter = load_adapter()
        with pytest.raises(adapter.MediaAdapterError) as exc_info:
            adapter.run(target)
        assert exc_info.value.code == "url_invalid"

    def test_nonzero_exit_maps_to_media_failed(self):
        adapter = load_adapter()
        with pytest.raises(adapter.MediaAdapterError) as exc_info:
            adapter.run(
                "https://example.com/x",
                runner=_fake_runner(returncode=1, stderr="ERROR: Unsupported URL"),
            )
        assert exc_info.value.code == "media_failed"
        assert "Unsupported URL" in exc_info.value.details["stderr_tail"]

    def test_timeout_maps_to_media_timeout(self):
        adapter = load_adapter()

        def _hang(command: list[str], **kwargs: Any) -> Any:
            raise subprocess.TimeoutExpired(command, kwargs.get("timeout", 1))

        with pytest.raises(adapter.MediaAdapterError) as exc_info:
            adapter.run("https://example.com/x", timeout=0.5, runner=_hang)
        assert exc_info.value.code == "media_timeout"
        assert exc_info.value.details["timeout_seconds"] == 0.5

    @pytest.mark.parametrize("stdout", ["", "not-json", '["array", "not", "object"]'])
    def test_bad_stdout_maps_to_media_output_invalid(self, stdout):
        adapter = load_adapter()
        with pytest.raises(adapter.MediaAdapterError) as exc_info:
            adapter.run("https://example.com/x", runner=_fake_runner(stdout=stdout))
        assert exc_info.value.code == "media_output_invalid"

    def test_entries_not_dicts_maps_to_media_output_invalid(self):
        adapter = load_adapter()
        upstream = json.dumps({"entries": ["flat-string"]})
        with pytest.raises(adapter.MediaAdapterError) as exc_info:
            adapter.run("https://example.com/x", runner=_fake_runner(stdout=upstream))
        assert exc_info.value.code == "media_output_invalid"

    def test_uv_missing_is_structured(self, monkeypatch):
        adapter = load_adapter()
        monkeypatch.setattr(adapter.shutil, "which", lambda name: None)
        with pytest.raises(adapter.MediaAdapterError) as exc_info:
            adapter.run("https://example.com/x")
        assert exc_info.value.code == "uv_missing"


class TestCliMedia:
    def test_success_json_contract(self, tmp_path, capsys):
        plugins = make_stub_plugin(tmp_path)
        code = main(
            ["media", "https://example.com/v", "--plugins-dir", str(plugins), "--json"]
        )
        assert code == EXIT_OK
        payload = json.loads(capsys.readouterr().out)
        assert payload["plugin"] == "myssia-media"
        assert payload["target"] == "https://example.com/v"
        assert payload["status"] == "success"

    def test_media_failure_exits_2(self, tmp_path, capsys):
        plugins = make_stub_plugin(tmp_path, raise_code="media_failed")
        code = main(
            ["media", "https://example.com/v", "--plugins-dir", str(plugins), "--json"]
        )
        assert code == EXIT_FETCH_ALL_FAILED
        payload = json.loads(capsys.readouterr().out)
        assert payload["error"] == "media_failed"

    def test_config_failure_exits_1(self, tmp_path, capsys):
        plugins = make_stub_plugin(tmp_path, raise_code="uv_missing")
        code = main(
            ["media", "https://example.com/v", "--plugins-dir", str(plugins), "--json"]
        )
        assert code == EXIT_CONFIG_ERROR
        assert json.loads(capsys.readouterr().out)["error"] == "uv_missing"

    def test_adapter_file_missing_exits_1(self, tmp_path, capsys):
        plugins = tmp_path / "plugins"
        plugins.mkdir()
        code = main(
            ["media", "https://example.com/v", "--plugins-dir", str(plugins), "--json"]
        )
        assert code == EXIT_CONFIG_ERROR
        assert json.loads(capsys.readouterr().out)["error"] == "media_adapter_missing"

    def test_broken_adapter_source_exits_1_not_crash(self, tmp_path, capsys):
        plugins = tmp_path / "plugins"
        (plugins / "myssia-media").mkdir(parents=True)
        (plugins / "myssia-media" / "adapter.py").write_text(
            "def run(: broken", encoding="utf-8"
        )
        code = main(
            ["media", "https://example.com/v", "--plugins-dir", str(plugins), "--json"]
        )
        assert code == EXIT_CONFIG_ERROR
        assert json.loads(capsys.readouterr().out)["error"] == "media_adapter_missing"

    def test_import_adapter_from_repo_plugins_dir(self):
        module = _import_plugin_adapter(PLUGINS_DIR, "myssia-media")
        assert module.PLUGIN_DIR.name == "myssia-media"

    def test_fetch_failure_codes_are_the_collection_family(self):
        assert MEDIA_FETCH_FAILURE_CODES == frozenset(
            {"media_failed", "media_timeout", "media_output_invalid"}
        )


class TestIronLawAdapterNeverBlocksCore:
    """铁律回归:适配器任何装不上/失败形态,核心品类流水线完全无感。"""

    @staticmethod
    def _assert_core_unblocked() -> None:
        category_files = sorted(PLUGINS_DIR.glob("*.yaml"))
        assert category_files, "顶层品类示例不应为空"
        for path in category_files:
            config = load_category_file(path)
            assert config.sources, f"{path.name} 必须可加载且有源"
        Pipeline(load_category_file(PLUGINS_DIR / "wool.yaml"))

    def test_adapter_missing_keeps_core_unblocked(self, tmp_path):
        plugins = tmp_path / "plugins"
        plugins.mkdir()
        assert (
            main(
                ["media", "https://example.com/v", "--plugins-dir", str(plugins), "--json"]
            )
            == EXIT_CONFIG_ERROR
        )
        self._assert_core_unblocked()

    def test_adapter_failure_keeps_core_unblocked(self, tmp_path):
        plugins = make_stub_plugin(tmp_path, raise_code="media_failed")
        assert (
            main(
                ["media", "https://example.com/v", "--plugins-dir", str(plugins), "--json"]
            )
            == EXIT_FETCH_ALL_FAILED
        )
        self._assert_core_unblocked()
