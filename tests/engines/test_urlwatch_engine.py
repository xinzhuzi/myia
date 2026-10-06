"""Tests for the urlwatch change-monitor engine (10-06-ai-news-sources S2).

状态矩阵(同 reddit 引擎四态法):

- **形状守卫**:extract/pagination 配置即结构化拒(单页监控语义)、源 URL
  非 http/https 拒、proxy 非 direct 拒(子进程直连铁律)、engine_options
  类型错拒(timeout/announce_new/content_max_chars/label);
- **robots 面**:目标页(虽由子进程抓)robots 全禁 → RobotsDisallowedError;
- **事件映射**:changed→条目(锚点指纹 url/label 标题/diff 截断进 content)、
  unchanged→合法空态 skip、new×announce_new 三态、error 事件→源级失败、
  deferred→显式空态;
- **adapter 错误码**:uv_missing→dependency_missing、其余→urlwatch_<code>、
  adapter 文件缺失→urlwatch_adapter_missing;
- **注册表**:ENGINE_REGISTRY 在册、AUTO_CHAIN 七层原样、auto_degrade 单级
  链、schema ENGINES/EngineName 词表收录;
- **registry 集成**:unchanged=skipped 源(非 failures)、changed=items
  正常流转(engine 名回填)。

零真实网络(MockTransport)、零真实子进程(fake adapter module)、零真实
快照缓存。
"""

from __future__ import annotations

import types

import httpx
import pytest

from myssia import schema
from myssia.engines import urlwatch as urlwatch_engine_module
from myssia.engines.fetch_base import FetchContext, FetchError, RobotsDisallowedError
from myssia.engines.registry import (
    AUTO_CHAIN,
    ENGINE_REGISTRY,
    auto_degrade,
    fetch_source,
    resolve_engine,
)
from myssia.engines.urlwatch import UrlwatchEngine, import_urlwatch_adapter
from myssia.schema import SourceConfig

from conftest import make_client, make_context, make_handler, run

PAGE_URL = "https://www.anthropic.com/news"


# ---------------------------------------------------------------------------
# 夹具:fake adapter 模块(compile+exec 加载面被 monkeypatch 替换)
# ---------------------------------------------------------------------------


class FakeAdapterError(RuntimeError):
    def __init__(self, code: str, message: str) -> None:
        super().__init__(message)
        self.code = code


def fake_adapter(
    *,
    events: list[dict] | None = None,
    counts: dict | None = None,
    checked: int = 1,
    raise_exc: Exception | None = None,
    calls: list | None = None,
    raise_sequence: list[Exception | None] | None = None,
) -> types.SimpleNamespace:
    """与 plugins/myssia-urlwatch/adapter.py 的 run() 同形的假件(零子进程).

    ``raise_sequence``:逐次调用弹出一项(None=按 events 正常返回),用于
    「先败后成」的重试路径;与 ``raise_exc`` 互斥(后者恒抛)。
    """
    if events is None:
        events = []
    if counts is None:
        counts = {
            "new": 0,
            "changed": 0,
            "unchanged": 0,
            "error": 0,
            "deferred": 0,
        }

    def fake_run(urls, *, cache_file=None, timeout=None, **_kw):  # noqa: ANN001, ANN202
        if calls is not None:
            calls.append({"urls": urls, "cache_file": cache_file, "timeout": timeout})
        if raise_sequence is not None:
            outcome = raise_sequence.pop(0) if raise_sequence else None
            if isinstance(outcome, Exception):
                raise outcome
        elif raise_exc is not None:
            raise raise_exc
        return {
            "plugin": "myssia-urlwatch",
            "status": "success",
            "checked": checked,
            "counts": counts,
            "events": events,
            "cache_file": str(cache_file or "~/.myia/urlwatch/cache.db"),
        }

    return types.SimpleNamespace(run=fake_run)


def changed_event(diff: str = "+ Qwen4 发布公告", url: str = PAGE_URL) -> dict:
    return {
        "event": "changed",
        "name": "demo",
        "location": url,
        "timestamp": "2026-10-05T08:00:00+00:00",
        "diff": diff,
    }


def urlwatch_source(**overrides: object) -> SourceConfig:
    data: dict = {"name": "demo", "engine": "urlwatch", "url": PAGE_URL}
    data.update(overrides)
    return SourceConfig.model_validate(data)


def urlwatch_context(
    handler_responder=None, *, robots: str | None = None
) -> FetchContext:
    if handler_responder is None:

        def handler_responder(request):  # noqa: ANN001, ANN202
            return httpx.Response(404, text="")

    client = make_client(make_handler(handler_responder, robots=robots))
    context, _ = make_context(client)
    return context


@pytest.fixture
def patched_adapter(monkeypatch):
    """替换 compile+exec 装载面:engine._adapter() 拿到 fake 模块."""

    def _install(adapter: types.SimpleNamespace) -> None:
        monkeypatch.setattr(
            urlwatch_engine_module, "import_urlwatch_adapter", lambda: adapter
        )

    return _install


# ---------------------------------------------------------------------------
# 注册表与 schema 词表
# ---------------------------------------------------------------------------


def test_registry_membership_and_chain_untouched():
    assert "urlwatch" in ENGINE_REGISTRY
    assert resolve_engine("urlwatch") is UrlwatchEngine
    assert "urlwatch" not in AUTO_CHAIN  # 链外:auto 永不路过
    assert len(AUTO_CHAIN) == 7
    assert auto_degrade("urlwatch") == ["urlwatch"]


def test_schema_vocabulary_accepts_urlwatch():
    assert "urlwatch" in schema.ENGINES
    source = urlwatch_source()  # SourceConfig.model_validate 即 schema 面
    assert source.engine == "urlwatch"


# ---------------------------------------------------------------------------
# 形状守卫(零 I/O 拒绝)
# ---------------------------------------------------------------------------


def test_extract_config_is_rejected():
    engine = UrlwatchEngine(
        urlwatch_source(
            extract={
                "type": "list",
                "item": "a",
                "fields": {"title": "h3", "url": "a@href"},
            }
        ),
        urlwatch_context(),
    )
    with pytest.raises(FetchError, match="extract") as excinfo:
        run(engine.fetch())
    assert excinfo.value.error_type == "extract_unsupported"


def test_pagination_config_is_rejected():
    engine = UrlwatchEngine(
        urlwatch_source(
            url="https://www.anthropic.com/news?page={page}",
            pagination={"mode": "template", "max_pages": 2},
        ),
        urlwatch_context(),
    )
    with pytest.raises(FetchError, match="单页监控") as excinfo:
        run(engine.fetch())
    assert excinfo.value.error_type == "pagination_unsupported"


def test_non_http_source_url_rejected():
    """纵深防御:schema 已拦非 http(s);引擎守卫兜 model_construct 旁路形态."""
    raw = SourceConfig.model_construct(
        name="raw", engine="urlwatch", url="ftp://example.com/page"
    )
    engine = UrlwatchEngine(raw, urlwatch_context())
    with pytest.raises(FetchError, match="http/https") as excinfo:
        run(engine._fetch_impl())
    assert excinfo.value.error_type == "invalid_urlwatch_source_url"


def test_non_direct_proxy_rejected_in_fetch_impl():
    engine = UrlwatchEngine(
        urlwatch_source(proxy="pool:demo"),
        urlwatch_context(),
    )
    with pytest.raises(FetchError, match="direct") as excinfo:
        run(engine._fetch_impl())  # 直接打 _fetch_impl:pool 挂载面另属 fetch() 门架
    assert excinfo.value.error_type == "proxy_unsupported"


@pytest.mark.parametrize(
    "options",
    [
        {"timeout": "90"},
        {"timeout": -1},
        {"announce_new": "yes"},
        {"content_max_chars": 5},
        {"content_max_chars": 99999},
        {"cache_file": 123},
        {"label": "  "},
        {"selector": 123},
        {"selector": " "},
        {"render": "playwright"},
        {"render": 123},
        {"render": "crawl4ai", "selector": "main"},
    ],
)
def test_engine_options_type_guard(options):
    engine = UrlwatchEngine(
        urlwatch_source(engine_options={"urlwatch": options}),
        urlwatch_context(),
    )
    with pytest.raises(FetchError, match="engine_options") as excinfo:
        run(engine.fetch())
    assert excinfo.value.error_type == "invalid_engine_options"


# ---------------------------------------------------------------------------
# robots 面
# ---------------------------------------------------------------------------


def test_robots_disallowed_target_rejected(patched_adapter):
    patched_adapter(fake_adapter(events=[changed_event()]))
    engine = UrlwatchEngine(
        urlwatch_source(),
        urlwatch_context(robots="User-agent: *\nDisallow: /"),
    )
    with pytest.raises(RobotsDisallowedError):
        run(engine.fetch())


def test_robots_allowed_target_passes(patched_adapter):
    patched_adapter(fake_adapter(events=[changed_event()]))
    engine = UrlwatchEngine(
        urlwatch_source(),
        urlwatch_context(robots="User-agent: *\nAllow: /"),
    )
    items = run(engine.fetch())
    assert len(items) == 1


# ---------------------------------------------------------------------------
# adapter 装载与错误码
# ---------------------------------------------------------------------------


def test_adapter_missing_is_structured(monkeypatch):
    def missing():
        raise FileNotFoundError(
            "urlwatch 适配器不存在:plugins/myssia-urlwatch/adapter.py"
        )

    monkeypatch.setattr(urlwatch_engine_module, "import_urlwatch_adapter", missing)
    engine = UrlwatchEngine(urlwatch_source(), urlwatch_context())
    with pytest.raises(FetchError, match="适配器不存在") as excinfo:
        run(engine.fetch())
    assert excinfo.value.error_type == "urlwatch_adapter_missing"


def test_uv_missing_maps_to_dependency_missing(patched_adapter):
    patched_adapter(fake_adapter(raise_exc=FakeAdapterError("uv_missing", "宿主无 uv")))
    engine = UrlwatchEngine(urlwatch_source(), urlwatch_context())
    with pytest.raises(FetchError, match="uv") as excinfo:
        run(engine.fetch())
    assert excinfo.value.error_type == "dependency_missing"


def test_adapter_failure_code_passthrough(patched_adapter):
    patched_adapter(
        fake_adapter(raise_exc=FakeAdapterError("urlwatch_timeout", "超时 120s"))
    )
    engine = UrlwatchEngine(urlwatch_source(), urlwatch_context())
    with pytest.raises(FetchError, match="超时") as excinfo:
        run(engine.fetch())
    assert excinfo.value.error_type == "urlwatch_timeout"


# ---------------------------------------------------------------------------
# 并发首装竞态重试(urlwatch_failed 一次错峰重试)
# ---------------------------------------------------------------------------


def clocked_context() -> tuple[FetchContext, object]:
    """带 FakeClock 的上下文夹具:重试 sleep 走假钟,零真实等待."""
    client = make_client(make_handler(lambda request: httpx.Response(404, text="")))
    return make_context(client)


def test_subprocess_failure_retries_once_then_succeeds(patched_adapter, caplog):
    """dry-run 实录的并发竞态形态:第 1 次 urlwatch_failed → 4s 错峰 → 第 2 次成功."""
    calls: list[dict] = []
    patched_adapter(
        fake_adapter(
            events=[changed_event()],
            calls=calls,
            raise_sequence=[
                FakeAdapterError("urlwatch_failed", "urlwatch 子进程非零退出(code=1)"),
                None,
            ],
        )
    )
    context, clock = clocked_context()
    engine = UrlwatchEngine(urlwatch_source(), context)
    with caplog.at_level("WARNING", logger="myssia.engines.urlwatch"):
        items = run(engine.fetch())
    assert len(items) == 1  # 重试后正常产出
    assert len(calls) == 2  # 恰好两进
    assert clock.sleeps == [4.0]  # 错峰 4s 走假钟
    assert any("错峰重试" in r.message for r in caplog.records)


def test_subprocess_failure_twice_is_terminal_with_stderr_tail(patched_adapter):
    """两连败=终态结构化失败;adapter 的 stderr 尾巴随行进消息(可诊断)."""

    class TailedError(RuntimeError):
        code = "urlwatch_failed"
        stderr_tail = "uv: error: failed to acquire lock"

    patched_adapter(
        fake_adapter(raise_exc=TailedError("urlwatch 子进程非零退出(code=1)"))
    )
    context, clock = clocked_context()
    engine = UrlwatchEngine(urlwatch_source(), context)
    with pytest.raises(FetchError, match="failed to acquire lock") as excinfo:
        run(engine.fetch())
    assert excinfo.value.error_type == "urlwatch_failed"
    assert clock.sleeps == [4.0]  # 只重试了一次


def test_timeout_is_not_retried(patched_adapter):
    """超时重试无意义(重跑只会再超时一遍):单进即抛,零 sleep."""
    calls: list[dict] = []
    patched_adapter(
        fake_adapter(
            calls=calls,
            raise_exc=FakeAdapterError("urlwatch_timeout", "超时 120s"),
        )
    )
    context, clock = clocked_context()
    engine = UrlwatchEngine(urlwatch_source(), context)
    with pytest.raises(FetchError, match="超时"):
        run(engine.fetch())
    assert len(calls) == 1
    assert clock.sleeps == []


def test_real_adapter_file_loads_from_repo_tree():
    """compile+exec 装载面在源码树布局真实可用(cwd 无关兜底路径)."""
    module = import_urlwatch_adapter()
    assert hasattr(module, "run")
    assert hasattr(module, "UrlwatchAdapterError")


def test_bundled_plugins_env_is_candidate_path(tmp_path, monkeypatch):
    """MYIA_BUNDLED_PLUGINS(桌面壳 Resources/plugins 锚点)是第二候选:
    cwd 无件时从随包锚点装载,装机态免「先 UI 安装」前置."""
    bundled_root = tmp_path / "Resources" / "plugins"
    plugin_dir = bundled_root / "myssia-urlwatch"
    plugin_dir.mkdir(parents=True)
    (plugin_dir / "adapter.py").write_text(
        "SENTINEL = 'bundled-adapter'\n", encoding="utf-8"
    )
    monkeypatch.chdir(tmp_path)  # cwd 相对 plugins/ 不存在 → 候选 1 落空
    monkeypatch.setenv("MYIA_BUNDLED_PLUGINS", str(bundled_root))
    module = import_urlwatch_adapter()
    assert getattr(module, "SENTINEL", None) == "bundled-adapter"


def test_bundled_plugins_env_ignored_when_not_a_dir(tmp_path, monkeypatch):
    """锚点环境变量指向不存在的目录时静默跳过(源码树兜底照走)."""
    monkeypatch.chdir(tmp_path)
    monkeypatch.setenv("MYIA_BUNDLED_PLUGINS", str(tmp_path / "nope"))
    module = import_urlwatch_adapter()  # 源码树兜底命中
    assert hasattr(module, "run")


# ---------------------------------------------------------------------------
# 事件映射
# ---------------------------------------------------------------------------


def test_selector_option_builds_content_filter_job(patched_adapter):
    """selector 选项 → job 携带上游实证形状的 css 内容过滤链.

    框架噪声根治(10-06 二段):main 选区 + exclude 剔 script/style
    + method html;背靠背实证 anthropic/cohere 过滤后快照稳定 unchanged。
    """
    calls: list[dict] = []
    patched_adapter(fake_adapter(events=[changed_event()], calls=calls))
    engine = UrlwatchEngine(
        urlwatch_source(engine_options={"urlwatch": {"selector": "main"}}),
        urlwatch_context(),
    )
    items = run(engine.fetch())
    assert len(items) == 1
    job = calls[0]["urls"][0]
    assert job["name"] == "demo"
    assert job["url"] == PAGE_URL
    assert job["filter"] == [
        {
            "css": {
                "selector": "main",
                "exclude": "script, style, noscript, template, svg",
                "method": "html",
            }
        }
    ]


def test_no_selector_means_raw_watch(patched_adapter):
    """不配 selector = 整页原始监控(向后兼容,过滤器键不出现)."""
    calls: list[dict] = []
    patched_adapter(fake_adapter(events=[changed_event()], calls=calls))
    engine = UrlwatchEngine(urlwatch_source(), urlwatch_context())
    run(engine.fetch())
    assert calls[0]["urls"][0] == {"name": "demo", "url": PAGE_URL}


def test_changed_event_maps_to_item_with_fingerprint_anchor(patched_adapter):
    patched_adapter(fake_adapter(events=[changed_event(diff="+ GPT-5 发布")]))
    engine = UrlwatchEngine(
        urlwatch_source(engine_options={"urlwatch": {"label": "OpenAI 新闻页"}}),
        urlwatch_context(),
    )
    items = run(engine.fetch())
    assert len(items) == 1
    item = items[0]
    assert item["url"].startswith(PAGE_URL + "#watch-")
    assert item["title"] == "OpenAI 新闻页 官网有更新"
    assert item["content"] == "+ GPT-5 发布"
    assert item["watch_event"] == "changed"
    assert item["watch_page"] == PAGE_URL
    assert item["published"] == "2026-10-05T08:00:00+00:00"


def test_fingerprint_anchor_stable_per_diff_and_distinct_across_diffs(patched_adapter):
    engine = UrlwatchEngine(urlwatch_source(), urlwatch_context())
    first = engine._events_to_items(
        {"events": [changed_event(diff="+ A")]},
        PAGE_URL,
        {"label": "x", "announce_new": True, "content_max_chars": 1500},
    )[0]["url"]
    same = engine._events_to_items(
        {"events": [changed_event(diff="+ A")]},
        PAGE_URL,
        {"label": "x", "announce_new": True, "content_max_chars": 1500},
    )[0]["url"]
    other = engine._events_to_items(
        {"events": [changed_event(diff="+ B")]},
        PAGE_URL,
        {"label": "x", "announce_new": True, "content_max_chars": 1500},
    )[0]["url"]
    assert first == same  # 同 diff = 同锚点(dedup {url} 拦重复告警)
    assert first != other  # 新变更 = 新锚点(第二次变更不被 {url} 全期吞)


def test_diff_truncated_to_content_max_chars(patched_adapter):
    patched_adapter(fake_adapter(events=[changed_event(diff="+" + "x" * 5000)]))
    engine = UrlwatchEngine(
        urlwatch_source(engine_options={"urlwatch": {"content_max_chars": 200}}),
        urlwatch_context(),
    )
    items = run(engine.fetch())
    assert len(items[0]["content"]) == 200


@pytest.mark.parametrize("noise_diff", ["", "   "])
def test_changed_event_with_empty_diff_is_noise_skip(patched_adapter, noise_diff):
    """噪声闸(装机真跑两轮实证):changed 但 diff 空/纯空白 = 页面漂移噪声.

    CDN/出口轮换使大页快照逐次漂移,上游判 changed 而 diff 渲染为空——
    「有更新」标题+空 content 的条目零信息量,降级显式 skip 不产条目。
    """
    patched_adapter(fake_adapter(events=[changed_event(diff=noise_diff)]))
    engine = UrlwatchEngine(urlwatch_source(), urlwatch_context())
    items = run(engine.fetch())
    assert items == []
    assert engine.last_skip_reason == "watch_noise_empty_diff"


def test_unchanged_is_legal_empty_state(patched_adapter):
    patched_adapter(
        fake_adapter(
            events=[
                {
                    "event": "unchanged",
                    "name": "demo",
                    "location": PAGE_URL,
                    "timestamp": "t",
                }
            ],
            counts={"new": 0, "changed": 0, "unchanged": 1, "error": 0, "deferred": 0},
        )
    )
    engine = UrlwatchEngine(urlwatch_source(), urlwatch_context())
    items = run(engine.fetch())
    assert items == []
    assert engine.last_skip_reason == "watch_unchanged"


def test_new_event_announces_by_default(patched_adapter):
    patched_adapter(
        fake_adapter(
            events=[
                {
                    "event": "new",
                    "name": "demo",
                    "location": PAGE_URL,
                    "timestamp": "t1",
                }
            ],
            counts={"new": 1, "changed": 0, "unchanged": 0, "error": 0, "deferred": 0},
        )
    )
    engine = UrlwatchEngine(urlwatch_source(), urlwatch_context())
    items = run(engine.fetch())
    assert len(items) == 1
    assert "已纳入监控" in items[0]["title"]


def test_new_event_baseline_only_when_announce_new_off(patched_adapter):
    patched_adapter(
        fake_adapter(
            events=[
                {
                    "event": "new",
                    "name": "demo",
                    "location": PAGE_URL,
                    "timestamp": "t1",
                }
            ],
            counts={"new": 1, "changed": 0, "unchanged": 0, "error": 0, "deferred": 0},
        )
    )
    engine = UrlwatchEngine(
        urlwatch_source(engine_options={"urlwatch": {"announce_new": False}}),
        urlwatch_context(),
    )
    items = run(engine.fetch())
    assert items == []
    assert engine.last_skip_reason == "watch_baseline_seeded"


def test_error_event_is_source_level_failure(patched_adapter):
    patched_adapter(
        fake_adapter(
            events=[
                {
                    "event": "error",
                    "name": "demo",
                    "location": PAGE_URL,
                    "timestamp": "t",
                    "error": "HTTP 503",
                }
            ],
            counts={"new": 0, "changed": 0, "unchanged": 0, "error": 1, "deferred": 0},
        )
    )
    engine = UrlwatchEngine(urlwatch_source(), urlwatch_context())
    with pytest.raises(FetchError, match="HTTP 503") as excinfo:
        run(engine.fetch())
    assert excinfo.value.error_type == "urlwatch_job_failed"


def test_deferred_event_is_explicit_empty_state(patched_adapter):
    patched_adapter(
        fake_adapter(
            events=[],
            counts={"new": 0, "changed": 0, "unchanged": 0, "error": 0, "deferred": 1},
            checked=0,
        )
    )
    engine = UrlwatchEngine(urlwatch_source(), urlwatch_context())
    items = run(engine.fetch())
    assert items == []
    assert engine.last_skip_reason == "watch_deferred"


def test_foreign_url_events_are_ignored(patched_adapter):
    """防御性过滤:同名跨源/异 URL 事件不串进本源条目."""
    patched_adapter(fake_adapter(events=[changed_event(url="https://other.example/x")]))
    engine = UrlwatchEngine(urlwatch_source(), urlwatch_context())
    items = run(engine.fetch())
    assert items == []
    assert engine.last_skip_reason == "watch_unchanged"


# ---------------------------------------------------------------------------
# registry 集成
# ---------------------------------------------------------------------------


def test_fetch_source_unchanged_is_skip_not_failure(patched_adapter):
    patched_adapter(
        fake_adapter(
            events=[
                {
                    "event": "unchanged",
                    "name": "demo",
                    "location": PAGE_URL,
                    "timestamp": "t",
                }
            ],
            counts={"new": 0, "changed": 0, "unchanged": 1, "error": 0, "deferred": 0},
        )
    )
    outcome = run(fetch_source(urlwatch_source(), urlwatch_context()))
    assert outcome.engine == "urlwatch"
    assert outcome.skipped is True
    assert outcome.skip_reason == "watch_unchanged"
    assert outcome.items == []
    assert outcome.failures == []


def test_fetch_source_changed_flows_items(patched_adapter):
    patched_adapter(fake_adapter(events=[changed_event()]))
    outcome = run(fetch_source(urlwatch_source(), urlwatch_context()))
    assert outcome.skipped is False
    assert len(outcome.items) == 1
    assert outcome.items[0]["url"].startswith(PAGE_URL + "#watch-")


# ---------------------------------------------------------------------------
# 渲染通道(10-06-ai-news-sources §12:纯客户端渲染页经 crawl4ai 取正文)
# ---------------------------------------------------------------------------


@pytest.fixture
def render_seams(monkeypatch, tmp_path):
    """渲染通道两注入口:helper 路径与后端可导入性(测试不依赖本机依赖)."""
    helper = tmp_path / "render_crawl4ai.py"
    helper.write_text("# fake helper\n", encoding="utf-8")
    monkeypatch.setattr(urlwatch_engine_module, "render_helper_path", lambda: helper)
    monkeypatch.setattr(
        urlwatch_engine_module, "render_backend_available", lambda backend: True
    )
    return helper


def test_render_builds_shell_job(patched_adapter, render_seams):
    """render: crawl4ai → job 换 ShellJob 形态(user_visible_url 锚事件定位)."""
    calls: list[dict] = []
    patched_adapter(
        fake_adapter(events=[changed_event(diff="+ Muse Spark 1.2")], calls=calls)
    )
    engine = UrlwatchEngine(
        urlwatch_source(engine_options={"urlwatch": {"render": "crawl4ai"}}),
        urlwatch_context(),
    )
    items = run(engine.fetch())
    assert len(items) == 1  # 事件映射零改动:location 仍=页面 URL
    assert items[0]["url"].startswith(PAGE_URL + "#watch-")
    job = calls[0]["urls"][0]
    assert job["name"] == "demo"
    assert job["user_visible_url"] == PAGE_URL
    assert "url" not in job and "filter" not in job  # shell 型,非 url 型
    assert str(render_seams) in job["command"]
    assert PAGE_URL in job["command"]


def test_render_helper_missing_is_structured(patched_adapter, monkeypatch):
    def missing():
        raise FileNotFoundError("urlwatch 渲染 helper 不存在:plugins/…")

    monkeypatch.setattr(urlwatch_engine_module, "render_helper_path", missing)
    engine = UrlwatchEngine(
        urlwatch_source(engine_options={"urlwatch": {"render": "crawl4ai"}}),
        urlwatch_context(),
    )
    with pytest.raises(FetchError, match="渲染 helper 不存在") as excinfo:
        run(engine.fetch())
    assert excinfo.value.error_type == "render_helper_missing"


def test_render_backend_missing_is_dependency_missing(
    patched_adapter, monkeypatch, tmp_path
):
    helper = tmp_path / "render_crawl4ai.py"
    helper.write_text("# fake helper\n", encoding="utf-8")
    monkeypatch.setattr(urlwatch_engine_module, "render_helper_path", lambda: helper)
    monkeypatch.setattr(
        urlwatch_engine_module, "render_backend_available", lambda backend: False
    )
    engine = UrlwatchEngine(
        urlwatch_source(engine_options={"urlwatch": {"render": "crawl4ai"}}),
        urlwatch_context(),
    )
    with pytest.raises(FetchError, match="crawl4ai") as excinfo:
        run(engine.fetch())
    assert excinfo.value.error_type == "dependency_missing"


def test_render_helper_path_reads_bundled_plugins_env(tmp_path, monkeypatch):
    """MYIA_BUNDLED_PLUGINS(桌面壳 Resources/plugins)是 helper 候选路径."""
    bundled_root = tmp_path / "Resources" / "plugins"
    plugin_dir = bundled_root / "myssia-urlwatch"
    plugin_dir.mkdir(parents=True)
    (plugin_dir / "render_crawl4ai.py").write_text("# bundled\n", encoding="utf-8")
    monkeypatch.chdir(tmp_path)  # cwd 相对 plugins/ 落空
    monkeypatch.setenv("MYIA_BUNDLED_PLUGINS", str(bundled_root))
    resolved = urlwatch_engine_module.render_helper_path()
    assert resolved == plugin_dir / "render_crawl4ai.py"


def test_render_helper_path_source_tree_fallback(tmp_path, monkeypatch):
    """cwd 无件、锚点环境变量缺省 → 源码树兜底命中真实 helper(cwd 无关)."""
    monkeypatch.chdir(tmp_path)
    monkeypatch.delenv("MYIA_BUNDLED_PLUGINS", raising=False)
    resolved = urlwatch_engine_module.render_helper_path()
    assert resolved.name == "render_crawl4ai.py"
    assert resolved.is_file()  # 仓库树内场景件真实在位


def test_build_render_command_quotes_shell_metacharacters():
    """命令串三段各自引号隔离(上游 ShellJob shell=True;路径空格/URL 元字符)."""
    command = urlwatch_engine_module.build_render_command(
        "/opt/tools/my python",
        "/tmp/some dir/render_crawl4ai.py",
        "https://ai.meta.com/blog?a=1&b=2",
    )
    assert "'/opt/tools/my python'" in command
    assert "'/tmp/some dir/render_crawl4ai.py'" in command
    assert "'https://ai.meta.com/blog?a=1&b=2'" in command  # & 在引号内,无裸露


def test_build_render_command_win32_variant(monkeypatch):
    """win32 走 cmd.exe:三段无条件双引号包裹(list2cmdline 只引含空格参数,
    带查询串 URL 的 ``&`` 不被包裹即被 cmd 切断——复核轮实证,故强制引号)."""
    monkeypatch.setattr(urlwatch_engine_module.sys, "platform", "win32")
    command = urlwatch_engine_module.build_render_command(
        r"C:\Python312\python.exe",
        r"C:\Program Files\helper.py",
        "https://example.com/blog?page=2&lang=zh",
    )
    assert command == (
        '"C:\\Python312\\python.exe"'
        ' "C:\\Program Files\\helper.py"'
        ' "https://example.com/blog?page=2&lang=zh"'
    )
    assert command.count('"') == 6  # 三段×首尾,无裸露元字符
