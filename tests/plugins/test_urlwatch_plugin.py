"""myssia-urlwatch 场景件契约测试(10-05-plugin-market-batch 首批).

被钉住的契约:

1. **manifest**:声明 adapter(subprocess)且无 vendor(BSD-3-Clause 上游
   不 vendor);tier=desktop、modes 走 local 安装命令(上游是 CLI 库,无
   remote endpoint);
2. **适配器 mock 子进程**:输入校验(仅 http/https、上限 64、去重保序)、
   jobs 文件是上游 UrlsYaml 多文档 YAML、命令形状(uv 隔离环境跑 MYIA
   shim)、成功装配结构化事件 JSON(new/changed/unchanged/error + deferred
   计数 + diff 截尾)、零变更=合法空态、非零退出/超时/输出不可解析/
   uv 缺失/URL 非法 —— 每种失败都是结构化 :class:`UrlwatchAdapterError`;
3. **铁律**:适配器任何失败形态下核心品类加载与 Pipeline 构造完全无感
   (装不上不拦核心;本批无 CLI 面,失败面=适配器异常)。

测试纪律:子进程一律注入 fake runner(mock,stdout 喂事件 JSON),零真实
网络、零真实 uv、零上游采集(真网冒烟留主人);每测独立 tmp_path。
"""

from __future__ import annotations

import json
import subprocess
from pathlib import Path
from typing import Any

import pytest
import yaml

from myssia.pipeline import Pipeline
from myssia.plugins.manifest import load_manifest_file
from myssia.schema import load_category_file

REPO_ROOT = Path(__file__).resolve().parents[2]
PLUGINS_DIR = REPO_ROOT / "plugins"
PLUGIN_DIR = PLUGINS_DIR / "myssia-urlwatch"
PLUGIN_ADAPTER = PLUGIN_DIR / "adapter.py"


def load_adapter() -> Any:
    import types

    module = types.ModuleType("myssia_urlwatch_adapter_test")
    module.__file__ = str(PLUGIN_ADAPTER)
    exec(  # noqa: S102 - 仓库内受控代码
        compile(
            PLUGIN_ADAPTER.read_text(encoding="utf-8"), str(PLUGIN_ADAPTER), "exec"
        ),
        module.__dict__,
    )
    return module


def _stdout(payload: dict[str, Any]) -> str:
    return json.dumps(payload, ensure_ascii=False)


def _runner_with_stdout(stdout: str, *, returncode: int = 0) -> Any:
    """fake runner:stdout/退出码可配,绝不触网、绝不开真子进程."""

    def _run(command: list[str], **kwargs: Any) -> subprocess.CompletedProcess[str]:
        return subprocess.CompletedProcess(command, returncode, stdout, "")

    return _run


def _sample_events() -> list[dict[str, Any]]:
    """shim 事件形状(2026-10-05 对 urlwatch 2.29 源码亲核的 collector 面)."""
    return [
        {
            "event": "new",
            "name": "example.com/a",
            "location": "https://example.com/a",
            "timestamp": 1759700000.0,
        },
        {
            "event": "changed",
            "name": "示例",
            "location": "https://example.com/b",
            "timestamp": 1759600000.0,
            "diff": "@@ -1 +1 @@\n-old\n+new" + "x" * 5000,
        },
        {
            "event": "unchanged",
            "name": "example.com/c",
            "location": "https://example.com/c",
        },
        {
            "event": "error",
            "name": "example.com/d",
            "location": "https://example.com/d",
            "error": "ConnectionError: boom",
            "traceback_tail": "Traceback (most recent call last): …",
        },
    ]


def _sample_payload(
    events: list[dict[str, Any]] | None = None, *, checked: int | None = None
) -> dict:
    events = _sample_events() if events is None else events
    return {
        "urlwatch_version": "2.29",
        "checked": len(events) if checked is None else checked,
        "events": events,
    }


class TestUrlwatchManifest:
    def test_manifest_declares_subprocess_adapter_without_vendor(self):
        manifest = load_manifest_file(PLUGIN_DIR / "plugin.yaml")
        assert manifest.id == "myssia-urlwatch"
        assert manifest.tier == "desktop"
        assert manifest.vendor is None, "BSD-3-Clause 上游不 vendor(pip 依赖隔离调用)"
        assert manifest.adapter is not None
        assert manifest.adapter.mode == "subprocess"
        assert manifest.modes.remote is None
        assert manifest.modes.local is not None
        assert manifest.modes.local.install.startswith("myssia plugin install")
        assert manifest.provides == ["change_monitor"]


class TestUrlwatchAdapter:
    # ---------------------------------------------------------- 输入校验

    def test_normalize_urls_accepts_strings_and_mappings(self):
        adapter = load_adapter()
        jobs = adapter.normalize_urls(
            [
                "https://example.com/a",
                {"name": "示例", "url": "https://example.com/b"},
                "https://example.com/a",  # 重复:去重保序
            ]
        )
        assert jobs == [
            {"name": "example.com/a", "url": "https://example.com/a"},
            {"name": "示例", "url": "https://example.com/b"},
        ]

    def test_normalize_urls_passes_through_filter_chain(self):
        """内容过滤链透传(10-06-ai-news-sources 框架噪声根治):上游 UrlsYaml
        原生 filter 形态,如 css 选择器圈正文;浅层形状校验,坏形拒绝."""
        adapter = load_adapter()
        flt = [
            {
                "css": {
                    "selector": "main",
                    "exclude": "script, style",
                    "method": "html",
                }
            }
        ]
        jobs = adapter.normalize_urls(
            [{"name": "带过滤", "url": "https://example.com/c", "filter": flt}]
        )
        assert jobs == [
            {"name": "带过滤", "url": "https://example.com/c", "filter": flt}
        ]
        for bad in ("main", [], [None], [["x"]], "css: main"):
            with pytest.raises(adapter.UrlwatchAdapterError):
                adapter.normalize_urls(
                    [{"url": "https://example.com/c", "filter": bad}]
                )

    def test_normalize_urls_wraps_single_string(self):
        adapter = load_adapter()
        assert adapter.normalize_urls("https://example.com/x") == [
            {"name": "example.com/x", "url": "https://example.com/x"}
        ]

    # ------------------------------------------------- shell 型 job(§12)

    def test_normalize_urls_accepts_shell_command_jobs(self):
        """shell 型 job(渲染通道):{name, command, user_visible_url} 透传;

        user_visible_url 锚住上游 get_location()/guid(2.29 装包实测),
        缺它事件 location 会变成命令串、调用方按 URL 匹配静默失配——必填。
        """
        adapter = load_adapter()
        jobs = adapter.normalize_urls(
            [
                {
                    "name": "meta 渲染",
                    "command": "python render_crawl4ai.py 'https://ai.meta.com/blog'",
                    "user_visible_url": "https://ai.meta.com/blog",
                }
            ]
        )
        assert jobs == [
            {
                "name": "meta 渲染",
                "command": "python render_crawl4ai.py 'https://ai.meta.com/blog'",
                "user_visible_url": "https://ai.meta.com/blog",
            }
        ]

    def test_normalize_urls_shell_job_derives_name_from_user_visible_url(self):
        adapter = load_adapter()
        jobs = adapter.normalize_urls(
            [
                {
                    "command": "python h.py u",
                    "user_visible_url": "https://ai.meta.com/blog",
                }
            ]
        )
        assert jobs[0]["name"] == "ai.meta.com/blog"

    def test_normalize_urls_shell_job_dedupes_by_user_visible_url(self):
        adapter = load_adapter()
        jobs = adapter.normalize_urls(
            [
                {
                    "command": "python h.py u",
                    "user_visible_url": "https://ai.meta.com/blog",
                },
                {
                    "command": "python other.py u",
                    "user_visible_url": "https://ai.meta.com/blog",
                },
                # 同目标 url 型与 shell 型互斥形态:同 location 只留首个
                "https://ai.meta.com/blog",
            ]
        )
        assert len(jobs) == 1
        assert "command" in jobs[0]

    @pytest.mark.parametrize(
        "item",
        [
            {"command": "echo hi"},  # 缺 user_visible_url
            {
                "command": "echo hi",
                "user_visible_url": "ftp://example.com/x",
            },  # 非 http/https
            {
                "command": "echo hi",
                "user_visible_url": "https://example.com/ oops",
            },  # 含空白
            {"command": "", "user_visible_url": "https://example.com/x"},
            {"command": 42, "user_visible_url": "https://example.com/x"},
            {
                "command": "echo 'a'\necho 'b'",
                "user_visible_url": "https://example.com/x",
            },  # 控制字符(换行)
            {
                "command": "x" * 5000,
                "user_visible_url": "https://example.com/x",
            },  # 超上限
        ],
    )
    def test_normalize_urls_rejects_invalid_shell_jobs(self, item):
        adapter = load_adapter()
        with pytest.raises(adapter.UrlwatchAdapterError) as exc_info:
            adapter.normalize_urls([item])
        assert exc_info.value.code == "url_invalid"

    def test_normalize_urls_shell_job_passes_through_filter_chain(self):
        adapter = load_adapter()
        flt = [{"css": {"selector": "main", "method": "html"}}]
        jobs = adapter.normalize_urls(
            [
                {
                    "command": "python h.py u",
                    "user_visible_url": "https://example.com/s",
                    "filter": flt,
                }
            ]
        )
        assert jobs[0]["filter"] == flt

    @pytest.mark.parametrize(
        "urls",
        [
            [],
            "ftp://example.com/f",  # 仅 http/https
            "not-a-url",  # 无 scheme
            "https://example.com/ oops",  # 含空白
            42,  # 非法类型
            [42],
            [{"name": "无 url 键"}],
            [""],
        ],
    )
    def test_normalize_urls_rejects_invalid_input(self, urls):
        adapter = load_adapter()
        with pytest.raises(adapter.UrlwatchAdapterError) as exc_info:
            adapter.normalize_urls(urls)
        assert exc_info.value.code == "url_invalid"

    def test_normalize_urls_caps_at_sixty_four(self):
        adapter = load_adapter()
        urls = [f"https://example.com/{i}" for i in range(adapter.MAX_URLS_PER_RUN + 1)]
        with pytest.raises(adapter.UrlwatchAdapterError) as exc_info:
            adapter.normalize_urls(urls)
        assert exc_info.value.code == "url_invalid"

    # ---------------------------------------------------------- jobs 文件

    def test_write_jobs_yaml_is_upstream_multi_doc_yaml(self, tmp_path):
        """上游 UrlsYaml 用 yaml.load_all 装载:每 doc 一个 {name,url} 映射
        (JSON 即合法 YAML 流映射,适配器不引 PyYAML 也能写)."""
        adapter = load_adapter()
        jobs_path = tmp_path / "urls.yaml"
        adapter.write_jobs_yaml(
            [
                {"name": "a", "url": "https://example.com/a"},
                {"name": "b", "url": "https://example.com/b"},
            ],
            jobs_path,
        )
        docs = list(yaml.safe_load_all(jobs_path.read_text(encoding="utf-8")))
        assert docs == [
            {"name": "a", "url": "https://example.com/a"},
            {"name": "b", "url": "https://example.com/b"},
        ]

    # ---------------------------------------------------------- 命令形状

    def test_build_command_is_isolated_uv_running_myia_shim(self, tmp_path):
        adapter = load_adapter()
        command = adapter.build_command(
            tmp_path / "shim.py", tmp_path / "urls.yaml", tmp_path / "cache.db"
        )
        assert command[:3] == ["uv", "run", "--no-project"]
        assert "--with" in command and "urlwatch" in command
        assert command[command.index("python") + 1] == str(tmp_path / "shim.py")
        assert command[command.index("--jobs") + 1] == str(tmp_path / "urls.yaml")
        assert command[command.index("--cache") + 1] == str(tmp_path / "cache.db")

    def test_shim_source_compiles_and_rides_upstream_loop(self):
        """shim 是 MYIA 代码但活在 uv 临时环境里:静态面钉住——可编译,
        且复用上游 worker.run_jobs 主循环 + UrlsYaml/CacheMiniDBStorage."""
        adapter = load_adapter()
        compile(adapter.SHIM_SOURCE, "<shim>", "exec")
        for anchor in ("run_jobs", "UrlsYaml", "CacheMiniDBStorage"):
            assert anchor in adapter.SHIM_SOURCE

    # ---------------------------------------------------------- run 面

    def test_run_success_counts_events(self, tmp_path):
        adapter = load_adapter()
        payload = adapter.run(
            [
                "https://example.com/a",
                "https://example.com/b",
                "https://example.com/c",
                "https://example.com/d",
            ],
            cache_file=tmp_path / "cache.db",
            runner=_runner_with_stdout(_stdout(_sample_payload())),
        )
        assert payload["status"] == "success"
        assert payload["plugin"] == "myssia-urlwatch"
        assert payload["checked"] == 4
        assert payload["counts"] == {
            "new": 1,
            "changed": 1,
            "unchanged": 1,
            "error": 1,
            "deferred": 0,
        }
        assert payload["cache_file"] == str(tmp_path / "cache.db")
        assert payload["urlwatch_version"] == "2.29"
        changed = next(e for e in payload["events"] if e["event"] == "changed")
        assert changed["name"] == "示例"
        errored = next(e for e in payload["events"] if e["event"] == "error")
        assert errored["error"] == "ConnectionError: boom"
        assert "traceback_tail" not in errored, (
            "shim 内部字段不上透(adapter 只留有界面)"
        )

    def test_run_bounds_diff_tail(self, tmp_path):
        adapter = load_adapter()
        payload = adapter.run(
            ["https://example.com/b"],
            cache_file=tmp_path / "cache.db",
            runner=_runner_with_stdout(_stdout(_sample_payload())),
        )
        changed = next(e for e in payload["events"] if e["event"] == "changed")
        assert len(changed["diff"]) == 4000, "diff 截尾 4000 字(结构化输出有界)"
        assert changed["diff"].endswith("x" * 10)

    def test_run_zero_change_is_success_empty_state(self, tmp_path):
        adapter = load_adapter()
        events = [
            {
                "event": "unchanged",
                "name": "example.com/a",
                "location": "https://example.com/a",
            }
        ]
        payload = adapter.run(
            ["https://example.com/a"],
            cache_file=tmp_path / "cache.db",
            runner=_runner_with_stdout(_stdout(_sample_payload(events))),
        )
        assert payload["status"] == "success"
        assert payload["counts"]["changed"] == 0 and payload["counts"]["unchanged"] == 1

    def test_run_counts_deferred_retry_jobs(self, tmp_path):
        """checked - 事件数 = deferred(上游 max_tries 重试未到阈值,本轮不判定)."""
        adapter = load_adapter()
        events = [
            {
                "event": "unchanged",
                "name": "example.com/a",
                "location": "https://example.com/a",
            },
        ]
        payload = adapter.run(
            ["https://example.com/a", "https://example.com/b"],
            cache_file=tmp_path / "cache.db",
            runner=_runner_with_stdout(_stdout(_sample_payload(events, checked=2))),
        )
        assert payload["counts"]["deferred"] == 1

    def test_nonzero_exit_maps_to_urlwatch_failed(self, tmp_path):
        adapter = load_adapter()
        with pytest.raises(adapter.UrlwatchAdapterError) as exc_info:
            adapter.run(
                ["https://example.com/a"],
                cache_file=tmp_path / "cache.db",
                runner=_runner_with_stdout(_stdout(_sample_payload()), returncode=1),
            )
        assert exc_info.value.code == "urlwatch_failed"
        assert exc_info.value.details["exit_code"] == 1

    def test_timeout_maps_to_urlwatch_timeout(self, tmp_path):
        adapter = load_adapter()

        def _hang(command: list[str], **kwargs: Any) -> Any:
            raise subprocess.TimeoutExpired(command, kwargs.get("timeout", 1))

        with pytest.raises(adapter.UrlwatchAdapterError) as exc_info:
            adapter.run(
                ["https://example.com/a"],
                cache_file=tmp_path / "cache.db",
                timeout=0.5,
                runner=_hang,
            )
        assert exc_info.value.code == "urlwatch_timeout"

    def test_invalid_stdout_maps_to_output_invalid(self, tmp_path):
        adapter = load_adapter()
        for stdout in ("not-json", json.dumps({"checked": 1})):
            with pytest.raises(adapter.UrlwatchAdapterError) as exc_info:
                adapter.run(
                    ["https://example.com/a"],
                    cache_file=tmp_path / "cache.db",
                    runner=_runner_with_stdout(stdout),
                )
            assert exc_info.value.code == "urlwatch_output_invalid"

    def test_uv_missing_is_structured(self, tmp_path, monkeypatch):
        adapter = load_adapter()
        monkeypatch.setattr(adapter.shutil, "which", lambda name: None)
        # 兜底已知落位一并空置(PATH 与已知落位全缺才是 uv_missing)
        monkeypatch.setattr(adapter, "_KNOWN_UV_PATHS", ())
        with pytest.raises(adapter.UrlwatchAdapterError) as exc_info:
            adapter.run(
                ["https://example.com/a"],
                cache_file=tmp_path / "cache.db",
                runner=_runner_with_stdout(_stdout(_sample_payload())),
            )
        assert exc_info.value.code == "uv_missing"

    def test_uv_falls_back_to_known_paths_when_path_lacks_it(
        self, tmp_path, monkeypatch
    ):
        """GUI 态 PATH 缺 uv(Finder/Dock 启动)→ 已知落位兜底可用.

        10-06-ai-news-sources:桌面壳 spawn 只注入 PYTHONPATH 不补 PATH,
        which 未命中时按 ~/.local/bin/uv 等绝对路径解析;本测以假 HOME
        造一个可执行 uv,断言解析与命令装配都吃到绝对路径。
        """
        adapter = load_adapter()
        fake_home = tmp_path / "home"
        fake_uv = fake_home / ".local" / "bin" / "uv"
        fake_uv.parent.mkdir(parents=True)
        fake_uv.write_text("#!/bin/sh\n", encoding="utf-8")
        fake_uv.chmod(0o755)
        monkeypatch.setattr(adapter.shutil, "which", lambda name: None)
        monkeypatch.setattr(adapter.Path, "home", staticmethod(lambda: fake_home))
        monkeypatch.setattr(
            adapter,
            "_KNOWN_UV_PATHS",
            (fake_home / ".local" / "bin" / "uv",),
        )
        assert adapter.uv_executable() == str(fake_uv)
        assert adapter.is_available() is True
        captured: dict[str, Any] = {}

        def _capture_runner(command: list[str], **kwargs: Any) -> Any:
            captured["command"] = command
            return _runner_with_stdout(_stdout(_sample_payload()))(command, **kwargs)

        result = adapter.run(
            ["https://example.com/a"],
            cache_file=tmp_path / "cache.db",
            runner=_capture_runner,
        )
        assert captured["command"][0] == str(fake_uv)
        assert result["status"] == "success"

    def test_uv_fallback_paths_win32_variant(self, monkeypatch):
        """Windows 官方落位是 uv.exe(复查轮补):win32 下首候选名带后缀;
        /opt/homebrew 专属位在非 darwin 平台退不存在路径,不误命中。"""
        import sys as _sys

        monkeypatch.setattr(_sys, "platform", "win32")
        adapter = load_adapter()  # load_adapter 每次重装载,元组按 platform 重建
        first = adapter._KNOWN_UV_PATHS[0]
        assert first.name == "uv.exe"
        assert first.parent == Path.home() / ".local" / "bin"
        assert all("/opt/homebrew" not in str(p) for p in adapter._KNOWN_UV_PATHS)

        monkeypatch.setattr(_sys, "platform", "darwin")
        adapter = load_adapter()
        assert adapter._KNOWN_UV_PATHS[0].name == "uv"
        assert adapter._KNOWN_UV_PATHS[1] == Path("/opt/homebrew/bin/uv")

    def test_url_invalid_raises_before_any_process(self, tmp_path):
        adapter = load_adapter()

        def _must_not_run(command: list[str], **kwargs: Any) -> Any:
            raise AssertionError("URL 校验失败时绝不开子进程")

        with pytest.raises(adapter.UrlwatchAdapterError) as exc_info:
            adapter.run(
                "ftp://example.com/f",
                cache_file=tmp_path / "cache.db",
                runner=_must_not_run,
            )
        assert exc_info.value.code == "url_invalid"
        assert exc_info.value.to_dict()["code"] == "url_invalid"


class TestIronLawAdapterNeverBlocksCore:
    """铁律回归:适配器任何装不上/失败形态,核心品类流水线完全无感."""

    @staticmethod
    def _assert_core_unblocked() -> None:
        for path in sorted(PLUGINS_DIR.glob("*.yaml")):
            config = load_category_file(path)
            assert config.sources, f"{path.name} 必须可加载且有源"
        Pipeline(load_category_file(PLUGINS_DIR / "wool.yaml"))

    def test_adapter_failures_keep_core_unblocked(self, tmp_path, monkeypatch):
        adapter = load_adapter()
        monkeypatch.setattr(adapter.shutil, "which", lambda name: None)
        monkeypatch.setattr(adapter, "_KNOWN_UV_PATHS", ())
        for bad_call in (
            lambda: adapter.run("ftp://example.com/f", cache_file=tmp_path / "c.db"),
            lambda: adapter.run(
                ["https://example.com/a"], cache_file=tmp_path / "c.db"
            ),
        ):
            with pytest.raises(adapter.UrlwatchAdapterError):
                bad_call()
        self._assert_core_unblocked()
