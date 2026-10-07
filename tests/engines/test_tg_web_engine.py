"""Tests for the TG web-session window engine (10-08-tg-web-line W2).

四态矩阵(照 telegram 引擎判例;design D4 引擎面):

- **配置档缺失**(未 web-login)→ ``session_missing`` 显式空态(items=[],
  last_skip_reason 置位、**零浏览器启动**、web-login 人话指引留痕);
- **配置错误**:account/chat/lookback_limit 形状错、源 URL 不符契约、
  pagination 配置 → 结构化 FetchError;
- **哨兵错误面**:登出页在 → ``tg_web_logged_out``(重登指引);选择器
  全不中 → ``tg_web_dom_stale``(跟修指引);群定位失败 → 结构化拒;
- **开启态**:mock persistent context 往返(goto → 登录态探针 → 开群 →
  窗口读取)→ items 形状:#tg- 锚(与 bot 线同命名空间)/ 粗筛复用
  (keywords 配置面 → 命中出仓、未命中零痕迹);
- **注册表**:ENGINE_REGISTRY 在册、AUTO_CHAIN 七层原样、auto_degrade
  单级链、schema ENGINES/EngineName 词表收录。

零真实网络零真浏览器(launch_persistent_context/require_playwright 全
monkeypatch web_line 模块面)。
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import pytest

from myssia import schema
from myssia.engines.fetch_base import FetchContext, FetchError
from myssia.engines.registry import (
    AUTO_CHAIN,
    ENGINE_REGISTRY,
    auto_degrade,
    resolve_engine,
)
from myssia.engines.tg_web import TelegramWebEngine
from myssia.schema import SourceConfig
from myssia.telegram import web_line

from conftest import make_client, make_context, make_source, run

SOURCE_URL = "https://web.telegram.org"
ACCOUNT = "telegram-alt1"
CHAT = "mihomo_party_group"


class FakePage:
    """evaluate 按 JS 体内容分发的 fake(登录探针/开群/窗口读取三面)."""

    def __init__(
        self,
        *,
        login_state: str = "logged_in",
        open_outcome: dict[str, Any] | None = None,
        window: list[dict[str, Any]] | None = None,
    ) -> None:
        self.login_state = login_state
        self.open_outcome = open_outcome or {"ok": True, "reason": "opened", "title": "mihomo 群"}
        self.window = window if window is not None else []
        self.goto_calls: list[str] = []

    async def goto(self, url: str, **_: Any) -> None:
        self.goto_calls.append(url)

    async def evaluate(self, script: Any, arg: Any = None) -> Any:
        js = script if isinstance(script, str) else ""
        if "has-auth-pages" in js:  # login_state_probe_js(W5 标定口径)
            return {"state": self.login_state}
        if "search_box_missing" in js:
            return self.open_outcome
        if "querySelectorAll" in js:
            return self.window
        raise AssertionError(f"意外 evaluate 面:{js[:80]}")


class FakeContext:
    def __init__(self, page: FakePage) -> None:
        self.pages = [page]
        self.closed = False

    async def new_page(self) -> FakePage:
        return self.pages[0]

    def set_default_timeout(self, ms: int) -> None:
        self.timeout_ms = ms

    async def close(self) -> None:
        self.closed = True


class FakeHandle:
    def __init__(self, context: FakeContext) -> None:
        self._context = context
        self.stopped = False

    async def start(self) -> Any:
        class _Started:
            chromium = None

        started = _Started()

        class _Chromium:
            async def launch_persistent_context(_self, directory: str, **kw: Any) -> FakeContext:  # noqa: N805
                _self.last_launch = {"directory": directory, **kw}  # type: ignore[attr-defined]
                return self._context

        started.chromium = _Chromium()
        return started

    async def stop(self) -> None:
        self.stopped = True


def patch_browser(
    monkeypatch: pytest.MonkeyPatch,
    page: FakePage,
) -> tuple[FakeHandle, FakeContext]:
    """把 web_line 的浏览器面换成 fake;返回 (handle, context) 供断言."""
    context = FakeContext(page)
    handle = FakeHandle(context)

    async def fake_launch(directory, *, headless, page_timeout_seconds=60.0, playwright_factory=None):
        return handle, context, None

    monkeypatch.setattr(web_line, "launch_persistent_context", fake_launch)
    monkeypatch.setattr(web_line, "require_playwright", lambda: object())
    return handle, context


def make_tg_web_source(**overrides: Any) -> SourceConfig:
    data: dict[str, Any] = {
        "name": f"telegram-{CHAT}",
        "engine": "tg_web",
        "url": SOURCE_URL,
        "engine_options": {
            "tg_web": {
                "account": ACCOUNT,
                "chat": CHAT,
                "lookback_limit": 50,
                # 粗筛口径钉死(免费情报词表之外的确定性面)
                "keywords": ["mihomo"],
            }
        },
    }
    data.update(overrides)
    return SourceConfig.model_validate(data)


def tg_web_context() -> FetchContext:
    context, _ = make_context(make_client(lambda request: None))
    return context


# ------------------------------------------------------------- registration


def test_registry_and_schema_vocabulary() -> None:
    assert "tg_web" in ENGINE_REGISTRY
    assert "tg_web" not in AUTO_CHAIN  # 链外:显式选择才生效
    assert resolve_engine("tg_web") is TelegramWebEngine
    assert auto_degrade("tg_web") == ["tg_web"]  # 单级链
    assert "tg_web" in schema.ENGINES
    typing_hints = schema.EngineName.__annotations__ if hasattr(schema.EngineName, "__annotations__") else ""
    assert "tg_web" in str(typing_hints) or "tg_web" in getattr(
        schema.EngineName, "__args__", ()
    )


# ------------------------------------------------------------ config errors


@pytest.mark.parametrize(
    "options",
    [
        {},  # 缺 account
        {"account": "bad-key", "chat": CHAT},  # 键违全称律
        {"account": ACCOUNT},  # 缺 chat
        {"account": ACCOUNT, "chat": True},  # chat 布尔
        {"account": ACCOUNT, "chat": CHAT, "lookback_limit": 0},
        {"account": ACCOUNT, "chat": CHAT, "lookback_limit": 101},
        {"account": ACCOUNT, "chat": CHAT, "lookback_limit": "50"},
    ],
)
def test_options_shape_errors(options: dict) -> None:
    source = make_tg_web_source(engine_options={"tg_web": options})
    engine = TelegramWebEngine(source, tg_web_context())
    with pytest.raises(FetchError) as exc_info:
        run(engine.fetch())
    assert exc_info.value.error_type == "invalid_engine_options"


def test_source_url_contract() -> None:
    engine = TelegramWebEngine(
        make_tg_web_source(url="https://evil.example.com"), tg_web_context()
    )
    with pytest.raises(FetchError) as exc_info:
        run(engine.fetch())
    assert exc_info.value.error_type == "invalid_tg_web_source_url"


def test_pagination_unsupported() -> None:
    # selector 模式(schema 合法形态,template 模式会被 {page} 占位符校验先拒)
    engine = TelegramWebEngine(
        make_tg_web_source(
            pagination={"mode": "selector", "selector": "a.next"}
        ),
        tg_web_context(),
    )
    with pytest.raises(FetchError) as exc_info:
        run(engine.fetch())
    assert exc_info.value.error_type == "pagination_unsupported"


# ---------------------------------------------------------- explicit states


def test_session_missing_is_explicit_empty(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    monkeypatch.setenv("MYIA_HOME", str(tmp_path))
    launched = []

    async def fake_launch(*args: Any, **kw: Any) -> Any:
        launched.append(args)
        raise AssertionError("session_missing 空态不得启动浏览器")

    monkeypatch.setattr(web_line, "launch_persistent_context", fake_launch)
    monkeypatch.setattr(web_line, "require_playwright", lambda: object())
    engine = TelegramWebEngine(make_tg_web_source(), tg_web_context())
    items = run(engine.fetch())
    assert items == []
    assert engine.last_skip_reason == "session_missing"
    assert launched == []


def test_dependency_missing_structured(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    monkeypatch.setenv("MYIA_HOME", str(tmp_path))
    profile = tmp_path / "telegram-web" / ACCOUNT
    profile.mkdir(parents=True)

    def fake_require() -> Any:
        raise web_line.TelegramWebError(
            "TG 网页线依赖 playwright 未安装:请先执行 "
            "pip install 'myssia[crawl4ai]'(组件轨)",
            reason="dependency_missing",
            fatal=True,
        )

    monkeypatch.setattr(web_line, "require_playwright", fake_require)
    engine = TelegramWebEngine(make_tg_web_source(), tg_web_context())
    with pytest.raises(FetchError) as exc_info:
        run(engine.fetch())
    assert exc_info.value.error_type == "dependency_missing"
    assert "myssia[crawl4ai]" in str(exc_info.value)


def test_logged_out_sentinel(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    monkeypatch.setenv("MYIA_HOME", str(tmp_path))
    (tmp_path / "telegram-web" / ACCOUNT).mkdir(parents=True)
    page = FakePage(login_state="logged_out")
    handle, context = patch_browser(monkeypatch, page)
    engine = TelegramWebEngine(make_tg_web_source(), tg_web_context())
    with pytest.raises(FetchError) as exc_info:
        run(engine.fetch())
    assert exc_info.value.error_type == "tg_web_logged_out"
    assert "web-login" in str(exc_info.value)
    assert "--force" in str(exc_info.value)
    assert context.closed and handle.stopped


def test_dom_stale_sentinel(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    monkeypatch.setenv("MYIA_HOME", str(tmp_path))
    (tmp_path / "telegram-web" / ACCOUNT).mkdir(parents=True)
    page = FakePage(login_state="unknown")
    patch_browser(monkeypatch, page)
    engine = TelegramWebEngine(make_tg_web_source(), tg_web_context())
    with pytest.raises(FetchError) as exc_info:
        run(engine.fetch())
    assert exc_info.value.error_type == "tg_web_dom_stale"
    assert "web_dom" in str(exc_info.value)  # 跟修指引


@pytest.mark.parametrize(
    ("open_outcome", "expected_type"),
    [
        ({"ok": False, "reason": "chat_not_found"}, "tg_web_chat_not_found"),
        ({"ok": False, "reason": "search_box_missing"}, "tg_web_dom_stale"),
        ({"ok": False, "reason": "open_timeout"}, "tg_web_dom_stale"),
    ],
)
def test_chat_open_failures_structured(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
    open_outcome: dict,
    expected_type: str,
) -> None:
    monkeypatch.setenv("MYIA_HOME", str(tmp_path))
    (tmp_path / "telegram-web" / ACCOUNT).mkdir(parents=True)
    page = FakePage(open_outcome=open_outcome)
    patch_browser(monkeypatch, page)
    engine = TelegramWebEngine(make_tg_web_source(), tg_web_context())
    with pytest.raises(FetchError) as exc_info:
        run(engine.fetch())
    assert exc_info.value.error_type == expected_type


# ---------------------------------------------------------------- open state


def test_window_fetch_maps_updates_with_anchor_and_filter(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    monkeypatch.setenv("MYIA_HOME", str(tmp_path))
    (tmp_path / "telegram-web" / ACCOUNT).mkdir(parents=True)
    page = FakePage(
        window=[
            {"mid": "11", "text": "mihomo v1.19 发布", "timestamp": 1761000000.0},
            {"mid": "12", "text": "今天天气不错", "timestamp": 1761000060.0},
            {"mid": "13", "text": None, "has_media": True},  # 纯媒体跳过
            {"mid": "14", "text": "mihomo 配置分享", "timestamp": 1761000120.0},
        ]
    )
    patch_browser(monkeypatch, page)
    engine = TelegramWebEngine(make_tg_web_source(), tg_web_context())
    items = run(engine.fetch())
    # 粗筛(keywords=[mihomo])只放行命中词的条目;锚 = 源url#tg-<chat>-<mid>
    urls = [item["url"] for item in items]
    assert f"{SOURCE_URL}#tg-{CHAT}-11" in urls
    assert f"{SOURCE_URL}#tg-{CHAT}-14" in urls
    assert len(items) == 2
    hit = items[0]
    assert hit["title"] == "mihomo v1.19 发布"
    assert hit["content"] == "mihomo v1.19 发布"
    assert page.goto_calls == ["https://web.telegram.org/k/"]


def test_window_zero_messages_is_legal_empty(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    monkeypatch.setenv("MYIA_HOME", str(tmp_path))
    (tmp_path / "telegram-web" / ACCOUNT).mkdir(parents=True)
    page = FakePage(window=[])
    patch_browser(monkeypatch, page)
    engine = TelegramWebEngine(make_tg_web_source(), tg_web_context())
    assert run(engine.fetch()) == []
    assert engine.last_skip_reason is None  # 安静群 ≠ skip


def test_filter_options_merge_telegram_compatible_keys(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    """tg_web 源过滤键与 bot 线同面:engine_options.telegram 的 keywords 也生效."""
    monkeypatch.setenv("MYIA_HOME", str(tmp_path))
    (tmp_path / "telegram-web" / ACCOUNT).mkdir(parents=True)
    source = make_tg_web_source(
        engine_options={"telegram": {"keywords": ["mihomo"]}, "tg_web": {"account": ACCOUNT, "chat": CHAT}}
    )
    page = FakePage(
        window=[{"mid": "1", "text": "mihomo 更新"}]
    )
    patch_browser(monkeypatch, page)
    engine = TelegramWebEngine(source, tg_web_context())
    items = run(engine.fetch())
    assert len(items) == 1


def test_source_validates_in_schema() -> None:
    """schema 全装载面:engine: tg_web 源过 SourceConfig 校验(词表在册)."""
    source = make_tg_web_source()
    assert source.engine == "tg_web"
    assert source.extra_params["engine_options"]["tg_web"]["account"] == ACCOUNT
