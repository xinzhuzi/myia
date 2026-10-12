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
from myssia.telegram import web_line, web_thread

from conftest import make_client, make_context, make_source, run

SOURCE_URL = "https://web.telegram.org"
ACCOUNT = "telegram-alt1"
CHAT = "mihomo_party_group"

#: 线程档 fake 坐标/常量(r6 判例:close-btn 504,40;hash 形 clashv8/xoxo8868)。
THREAD_FOOTER_XY = (10.0, 20.0)
THREAD_CLOSE_XY = (504.0, 40.0)
CHANNEL_HASH = "#@clashv8"
THREAD_HASH = "#@xoxo8868"
THREAD_PEER = "-4373866046"


class FakeMouse:
    """受信点击 fake:记录坐标并驱动线程页片状态翻转(真点语义)."""

    def __init__(self, page: "FakePage | None" = None) -> None:
        self.clicks: list[tuple[float, float]] = []
        self._page = page

    async def click(self, x: float, y: float, **_: Any) -> None:
        self.clicks.append((x, y))
        if self._page is not None:
            self._page.apply_click(x, y)


class FakePage:
    """evaluate 按 JS 体内容分发的 fake.

    基础面:登录探针/侧栏定位/搜索兜底/验证/窗口读取;线程档面
    (10-12-tg-comments-reach):频道帖扫描/评论钮定位/线程读取/状态件/
    close 钮定位 —— 真点坐标翻转 ``in_thread`` 页片状态。
    """

    def __init__(
        self,
        *,
        login_state: str = "logged_in",
        login_state_sequence: list[str] | None = None,
        open_outcome: dict[str, Any] | None = None,
        window: list[dict[str, Any]] | None = None,
        posts: list[dict[str, Any]] | None = None,
        thread: list[dict[str, Any]] | None = None,
        threads: dict[str, list[dict[str, Any]]] | None = None,
        footer_ok: bool = True,
        stuck_in_thread: bool = False,
    ) -> None:
        self.login_state = login_state
        # 稳态复探回归件(2026-10-08 真跑:冷启动 0.4s logged_out → 2.9s
        # logged_in):非空时逐探弹出,弹尽回落 login_state
        self.login_state_sequence = list(login_state_sequence or [])
        # None = 开群全链成功面;{ok:False,...} = 定位/验证失败注入口
        self.open_outcome = open_outcome
        self.window = window if window is not None else []
        # 线程档注入口:posts = collect_channel_posts 的 JS 形载荷;
        # thread = 线程回泡载荷(JS 形);footer_ok=False = 评论钮缺;
        # stuck_in_thread=True = 线程开得进回不来(状态基中断面)。
        self.posts = posts
        self.thread = thread
        # 每帖独立线程载荷(键 = 帖 mid;缺省走 thread 全量,任帖同载)
        self.threads = threads
        self.located_post: str | None = None
        self.footer_ok = footer_ok
        self.stuck_in_thread = stuck_in_thread
        self.in_thread = False
        self.footer_locates: list[tuple[str, bool]] = []
        self.goto_calls: list[str] = []
        self.probe_count = 0
        self.mouse = FakeMouse(self)

    def apply_click(self, x: float, y: float) -> None:
        if (x, y) == THREAD_FOOTER_XY and self.footer_ok:
            self.in_thread = True  # stuck 面:开得进
        elif (x, y) == THREAD_CLOSE_XY and not self.stuck_in_thread:
            self.in_thread = False  # stuck 面:close 点击无效

    def _channel_posts_payload(self) -> list[dict[str, Any]]:
        if self.in_thread:
            return []  # 线程页片无评论钮(扫描只在频道面发生)
        return list(self.posts or [])

    async def goto(self, url: str, **_: Any) -> None:
        self.goto_calls.append(url)

    async def evaluate(self, script: Any, arg: Any = None) -> Any:
        js = script if isinstance(script, str) else ""
        if "has-auth-pages" in js:  # login_state_probe_js(W5 标定口径)
            self.probe_count += 1
            if self.login_state_sequence:
                state = self.login_state_sequence.pop(0)
                return {"state": state}
            return {"state": self.login_state}
        if "replies-footer-text" in js:  # collect_channel_posts_js
            return self._channel_posts_payload()
        if "data-reply-to-mid" in js:  # collect_thread_messages_js
            if not self.in_thread:
                return []
            if self.threads is not None:
                return list(self.threads.get(self.located_post or "", []))
            return list(self.thread or [])
        if "replies-element" in js:  # LOCATE_REPLY_FOOTER_JS
            self.located_post = str(arg.get("mid"))
            self.footer_locates.append(
                (str(arg.get("mid")), bool(arg.get("scroll")))
            )
            if not self.footer_ok or self.in_thread:
                return {"ok": False, "reason": "no_footer"}
            if arg.get("scroll"):
                return {"ok": True, "reason": "scrolled"}
            return {"ok": True, "reason": "located", "x": 10.0, "y": 20.0}
        if "sidebar-close-button" in js:  # LOCATE_CLOSE_BTN_JS
            return {"ok": True, "x": 504.0, "y": 40.0, "hit": "btn-icon",
                    "badge": True}
        if "tabs-tab" in js:  # THREAD_STATE_JS
            if self.stuck_in_thread:
                return {"hash": THREAD_HASH, "tabCount": 2,
                        "chanTabActive": False}
            return {"hash": THREAD_HASH if self.in_thread else CHANNEL_HASH,
                    "tabCount": 2 if self.in_thread else 1,
                    "chanTabActive": not self.in_thread}
        if js.strip() == web_thread.HASH_PROBE_JS:
            return THREAD_HASH if self.in_thread else CHANNEL_HASH
        if "data-peer-id" in js:  # LOCATE_SIDEBAR_JS
            if self.open_outcome is not None:
                return dict(self.open_outcome)
            return {"ok": True, "reason": "sidebar_match", "x": 1.0, "y": 2.0,
                    "title": "mihomo 群", "peerId": "-1001"}
        if "input-search-input" in js:  # LOCATE_SEARCH_JS(兜底)
            if self.open_outcome is not None:
                return dict(self.open_outcome)
            return {"ok": True, "reason": "search_match", "x": 3.0, "y": 4.0,
                    "title": "mihomo 群"}
        if "containerChain" in js:  # VERIFY_CHAT_OPEN_JS
            if self.open_outcome is not None and not self.open_outcome.get("ok"):
                return {"ok": False, "midCount": 0}
            return {"ok": True, "midCount": max(len(self.window), 1),
                    "bubbles": 1, "containerChain": ["bubbles"],
                    "title": "mihomo 群"}
        if "bubble[data-mid]" in js:
            return self.window
        raise AssertionError(f"意外 evaluate 面:{js[:80]}")


@pytest.fixture(autouse=True)
def _fast_open_chat_windows(monkeypatch: pytest.MonkeyPatch) -> None:
    """稳态/轮询窗全归零(真值交互窗的单测零等待;真跑标定值在 web_line)."""
    monkeypatch.setattr(web_line, "LOGIN_SETTLE_SECONDS", 0.0)
    monkeypatch.setattr(web_line, "OPEN_CHAT_DIALOGS_TIMEOUT_SECONDS", 0.0)
    monkeypatch.setattr(web_line, "OPEN_CHAT_SETTLE_SECONDS", 0.0)
    monkeypatch.setattr(web_line, "OPEN_CHAT_VERIFY_TIMEOUT_SECONDS", 0.0)
    # 线程档时序窗同归零(真跑标定值在 web_thread;基线 elapsed≈0 →
    # 测试预算面 = fetch 帽 − 过滤储备,与真跑推导同式)
    monkeypatch.setattr(web_thread, "THREAD_FOOTER_READY_TIMEOUT_SECONDS", 0.0)
    monkeypatch.setattr(web_thread, "THREAD_FOOTER_POLL_SECONDS", 0.0)
    monkeypatch.setattr(web_thread, "THREAD_PREP_SETTLE_SECONDS", 0.0)
    monkeypatch.setattr(web_thread, "THREAD_OPEN_HASH_TIMEOUT_SECONDS", 0.0)
    monkeypatch.setattr(web_thread, "THREAD_HASH_POLL_SECONDS", 0.0)
    monkeypatch.setattr(web_thread, "THREAD_READ_SETTLE_SECONDS", 0.0)
    monkeypatch.setattr(web_thread, "THREAD_CLOSE_VERIFY_TIMEOUT_SECONDS", 0.0)
    monkeypatch.setattr(web_thread, "THREAD_STATE_POLL_SECONDS", 0.0)


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
        # 评论线程档三钮(10-12-tg-comments-reach)
        {"account": ACCOUNT, "chat": CHAT, "comments_max_threads": -1},
        {"account": ACCOUNT, "chat": CHAT, "comments_max_threads": 21},
        {"account": ACCOUNT, "chat": CHAT, "comments_max_threads": "3"},
        {"account": ACCOUNT, "chat": CHAT, "comments_max_threads": True},
        {"account": ACCOUNT, "chat": CHAT, "comments_max_replies": 0},
        {"account": ACCOUNT, "chat": CHAT, "comments_max_replies": 101},
        {"account": ACCOUNT, "chat": CHAT, "comments_max_replies": "50"},
        {"account": ACCOUNT, "chat": CHAT, "fetch_timeout_seconds": 0},
        {"account": ACCOUNT, "chat": CHAT, "fetch_timeout_seconds": -5},
        {"account": ACCOUNT, "chat": CHAT, "fetch_timeout_seconds": "120"},
        {"account": ACCOUNT, "chat": CHAT, "fetch_timeout_seconds": True},
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
    assert "页面加载异常" in str(exc_info.value)  # 排障细节在 error_type 与日志


def test_logged_out_transient_settled_passes(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    """/k/ 冷启动瞬态回归(2026-10-08 真跑实证):前两探 logged_out →
    logged_in,稳态复探后采集照常,不误杀 tg_web_logged_out。"""
    monkeypatch.setenv("MYIA_HOME", str(tmp_path))
    # 瞬态回归需要真实稳态窗(覆盖 autouse 归零;序列推进靠 0.5s 复探步长)
    monkeypatch.setattr(web_line, "LOGIN_SETTLE_SECONDS", 2.0)
    (tmp_path / "telegram-web" / ACCOUNT).mkdir(parents=True)
    page = FakePage(
        login_state="logged_in",
        login_state_sequence=["logged_out", "logged_out", "logged_in"],
        window=[],
    )
    patch_browser(monkeypatch, page)
    engine = TelegramWebEngine(make_tg_web_source(), tg_web_context())
    items = run(engine.fetch())
    assert items == []
    assert engine.last_skip_reason is None
    assert page.probe_count == 3


@pytest.mark.parametrize(
    ("open_outcome", "expected_type"),
    [
        ({"ok": False, "reason": "chat_not_found"}, "tg_web_chat_not_found"),
        ({"ok": False, "reason": "dialogs_missing"}, "tg_web_dom_stale"),
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


def test_sample_plugin_yaml_ships_valid_tg_web_source() -> None:
    """示范件把守(G9,质询回改):config/telegram-web.yaml 过 schema 全装载,
    源形态与 D4 对齐(account 全称律/chat/lookback 窗口帽);首源=生产正户
    clashv8(2026-10-11 主人令换源;G9 同名复用对 mihomo_party 的 web 侧源
    停订为注释块可回切,bot 线同名示范件仍在册);**锚命名空间独立**——
    #tg- 锚含源 url 前缀+chat.id,两线 url 必不同(web vs api)且 tg_web
    chat 按源配置原样注入(标题包含形≠bot 线数字形),双线同跑同群同消息
    双条;断言两线示范件同消息锚串不等(未来若做锚归一改动,此断言红=提示
    同步四处文档口径)."""
    from myssia.schema import load_category_file

    repo_root = Path(__file__).resolve().parents[2]
    cfg = load_category_file(repo_root / "config" / "telegram-web.yaml")
    assert cfg.id == "telegram"  # 10-09 AC6 归一:三件同 id,文件名区分三线
    src = cfg.sources[0]
    assert src.name == "telegram-clashv8"  # 生产正户钉名(示范件换源/重排须有意过此关)
    assert src.engine == "tg_web"
    opts = src.extra_params["engine_options"]["tg_web"]
    assert opts["account"].startswith("telegram-")  # 账号键全称律
    # 2026-10-11 主人令换源:mihomo_party 停订(注释块可回切),首源=clashv8
    # 频道「免费VPN|机场|节点」,chat 落标题包含形(数字形 -3770098404 备选,
    # 见 config/telegram-web.yaml 源注记)
    assert opts["chat"] == "免费VPN"
    assert 1 <= opts["lookback_limit"] <= 100  # 窗口帽域
    # 评论线程档示范(10-12-tg-comments-reach):帽与预算键在档,且品类
    # timeouts.fetch 与引擎 fetch_timeout_seconds 对齐(漂移 = 超帽被掐面)
    assert 0 <= opts["comments_max_threads"] <= 20
    assert 1 <= opts["comments_max_replies"] <= 100
    assert cfg.timeouts is not None
    assert opts["fetch_timeout_seconds"] == cfg.timeouts.fetch
    groups = load_category_file(repo_root / "config" / "telegram-groups.yaml")
    # 同名复用对的 web 侧已停订(注释块),按名找 bot 对位会扑空——取 bot 线
    # 示范件首源(mihomo_party,占位 chat_id)作锚对照;回切同名对时改回按名找。
    bot_src = groups.sources[0]
    # 锚命名空间独立把守(质询实证):两线示范件铸的锚必不同——
    # url 前缀(web.telegram.org vs api.telegram.org)+chat 形(标题包含 vs
    # 数字)双差异;若有人改配置成 url 同值+同数字 id(互去重理论成立条件),
    # 此断言红 = 逼同步文档口径,防「互去重」失真声明再溜入。
    web_anchor = f"{src.url}#tg-{opts['chat']}-123"
    bot_opts = bot_src.extra_params["engine_options"]["telegram"]
    bot_anchor = f"{bot_src.url}#tg-{bot_opts['chat_id']}-123"
    assert web_anchor != bot_anchor


# ------------------------------------------------- comment threads (V1 批量档)


def _thread_reply(mid: str, text: str, sender: str = "李某人 .") -> dict[str, Any]:
    """r7_2 钉死形态的回泡载荷(JS 形;must_fix5 文本叶干净)."""
    return {
        "mid": mid,
        "peerId": THREAD_PEER,
        "replyTo": "4295090508",
        "text": text,
        "sender": sender,
        "timestamp": 1791724777.0,
        "has_media": False,
        "has_inner_text": True,
    }


def test_comment_threads_two_sorting_calls_ship_both_namespaces(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    """must_fix2 真出仓断言:fake 更新流含频道 update(chat.id=频道标识)+
    回帖 update(chat.id=讨论群 peer),两次 updates_to_items 后合并进过滤,
    输出两类锚各 ≥1(防单调用实现「形状绿/线上零评论条目」)。"""
    monkeypatch.setenv("MYIA_HOME", str(tmp_path))
    (tmp_path / "telegram-web" / ACCOUNT).mkdir(parents=True)
    page = FakePage(
        window=[
            {"mid": "11", "text": "mihomo v1.19 发布", "timestamp": 1761000000.0},
            {"mid": "12", "text": "今天天气不错", "timestamp": 1761000060.0},
        ],
        posts=[
            {"mid": "4294967709", "peerId": "-3770098404",
             "commentsCount": 704, "isUnread": False},
            {"mid": "4294967708", "peerId": "-3770098404",
             "commentsCount": 1128, "isUnread": True},
            {"mid": "4294967702", "peerId": "-3770098404",
             "commentsCount": 1128, "isUnread": False},
            {"mid": "4294967633", "peerId": "-3770098404",
             "commentsCount": 0, "isUnread": False},  # 无评论钮帖
        ],
        threads={
            "4294967708": [_thread_reply("4295090517", "mihomo 线程福利")],
            "4294967709": [
                _thread_reply("4295090521", "mihomo 第二帖回复", sender="OO OO"),
                _thread_reply("4295090523", "订阅(不含关键词)"),
            ],
        },
    )
    patch_browser(monkeypatch, page)
    engine = TelegramWebEngine(
        make_tg_web_source(
            engine_options={"tg_web": {
                "account": ACCOUNT, "chat": CHAT, "keywords": ["mihomo"],
                "comments_max_threads": 2,  # 帽 2:三候选只展开两帖
            }}
        ),
        tg_web_context(),
    )
    items = run(engine.fetch())
    urls = [item["url"] for item in items]
    # 频道命名空间锚(第一次分拣:频道标识 chat_id)
    assert f"{SOURCE_URL}#tg-{CHAT}-11" in urls
    # 讨论群命名空间锚(第二次分拣:讨论群真实 peer;-负 peer 连写双横线)
    assert f"{SOURCE_URL}#tg-{THREAD_PEER}-4295090517" in urls
    assert f"{SOURCE_URL}#tg-{THREAD_PEER}-4295090521" in urls
    # 粗筛同源:不含关键词的回帖零痕迹
    assert len(items) == 3
    # 展开序与帽:is_unread 优先(4294967708)→ mid 大者(4294967709);
    # 每帖两调(scroll + 新鲜 rect),4294967702 因帽 2 未展开
    assert [mid for mid, _ in page.footer_locates] == [
        "4294967708", "4294967708", "4294967709", "4294967709",
    ]
    # 每段关一次线程页片(真点 close-btn 判例坐标)
    assert page.mouse.clicks.count(THREAD_CLOSE_XY) == 2
    assert page.mouse.clicks.count(THREAD_FOOTER_XY) == 2
    assert page.in_thread is False  # 收尾回频道面


def test_comment_threads_off_zero_interaction(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    """comments_max_threads=0 = 整档 off:零评论钮交互,行为与 V1 前一致."""
    monkeypatch.setenv("MYIA_HOME", str(tmp_path))
    (tmp_path / "telegram-web" / ACCOUNT).mkdir(parents=True)
    page = FakePage(
        window=[{"mid": "11", "text": "mihomo v1.19 发布",
                 "timestamp": 1761000000.0}],
        posts=[{"mid": "4294967708", "peerId": "-3770098404",
                "commentsCount": 1128, "isUnread": True}],
        thread=[_thread_reply("4295090517", "mihomo 线程福利")],
    )
    patch_browser(monkeypatch, page)
    engine = TelegramWebEngine(
        make_tg_web_source(
            engine_options={"tg_web": {
                "account": ACCOUNT, "chat": CHAT, "keywords": ["mihomo"],
                "comments_max_threads": 0,
            }}
        ),
        tg_web_context(),
    )
    items = run(engine.fetch())
    assert [item["url"] for item in items] == [f"{SOURCE_URL}#tg-{CHAT}-11"]
    assert page.footer_locates == []
    assert THREAD_FOOTER_XY not in page.mouse.clicks


def test_comment_threads_budget_skip_structured(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path, caplog: pytest.LogCaptureFixture
) -> None:
    """预算推导跳过(留痕不硬烧):fetch 帽 80s + LLM 已配(储备 65s)→
    budget=80−基线≈0−65≈15s < 18s 门槛 → 整档跳过,零评论钮交互."""
    import logging

    monkeypatch.setenv("MYIA_HOME", str(tmp_path))
    (tmp_path / "telegram-web" / ACCOUNT).mkdir(parents=True)
    page = FakePage(
        window=[{"mid": "11", "text": "mihomo v1.19 发布",
                 "timestamp": 1761000000.0}],
        posts=[{"mid": "4294967708", "peerId": "-3770098404",
                "commentsCount": 1128, "isUnread": True}],
        thread=[_thread_reply("4295090517", "mihomo 线程福利")],
    )
    patch_browser(monkeypatch, page)

    async def fake_completer(**_: Any) -> Any:
        from types import SimpleNamespace

        return SimpleNamespace(text='[{"id": 1, "score": 5, "reason": "ok"}]')

    engine = TelegramWebEngine(
        make_tg_web_source(
            engine_options={"tg_web": {
                "account": ACCOUNT, "chat": CHAT, "keywords": ["mihomo"],
                "comments_max_threads": 3,
                "fetch_timeout_seconds": 80,
                "llm_base_url": "env:MYIA_TEST_LLM_URL",
                "llm_api_key": "env:MYIA_TEST_LLM_KEY",
            }}
        ),
        tg_web_context(),
        completer=fake_completer,
    )
    with caplog.at_level(logging.INFO, logger="myssia.engines.tg_web"):
        items = run(engine.fetch())
    # 基线条目照常出仓(精筛面 completer 注入,零真网络)
    assert [item["url"] for item in items] == [f"{SOURCE_URL}#tg-{CHAT}-11"]
    assert page.footer_locates == []  # 零评论钮交互
    assert any("预算不足" in message for message in caplog.messages)


def test_comment_threads_state_interrupt_abandons_remaining(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path, caplog: pytest.LogCaptureFixture
) -> None:
    """must_fix4 状态基中断:线程开得进回不来(close 失效 + 兜底后仍未复原)
    → 第一段后弃本轮剩余帖,基线 items 照常出仓(已读到的线程条目保留)."""
    import logging

    monkeypatch.setenv("MYIA_HOME", str(tmp_path))
    (tmp_path / "telegram-web" / ACCOUNT).mkdir(parents=True)
    page = FakePage(
        window=[{"mid": "11", "text": "mihomo v1.19 发布",
                 "timestamp": 1761000000.0}],
        posts=[
            {"mid": "4294967708", "peerId": "-3770098404",
             "commentsCount": 1128, "isUnread": True},
            {"mid": "4294967709", "peerId": "-3770098404",
             "commentsCount": 704, "isUnread": False},
        ],
        thread=[_thread_reply("4295090517", "mihomo 线程福利")],
        stuck_in_thread=True,  # close 点击无效 + 状态件恒报未复原
    )
    patch_browser(monkeypatch, page)
    engine = TelegramWebEngine(
        make_tg_web_source(
            engine_options={"tg_web": {
                "account": ACCOUNT, "chat": CHAT, "keywords": ["mihomo"],
                "comments_max_threads": 3,
            }}
        ),
        tg_web_context(),
    )
    with caplog.at_level(logging.WARNING, logger="myssia.engines.tg_web"):
        items = run(engine.fetch())
    urls = [item["url"] for item in items]
    # 基线 + 第一段线程条目都在(状态中断不丢已出仓数据)
    assert f"{SOURCE_URL}#tg-{CHAT}-11" in urls
    assert f"{SOURCE_URL}#tg-{THREAD_PEER}-4295090517" in urls
    # 只展开了第一帖(unread 优先),第二帖按状态基弃
    assert [mid for mid, _ in page.footer_locates] == ["4294967708", "4294967708"]
    assert any("状态基中断" in message for message in caplog.messages)
    # 兜底路径走过了(open_chat_flow 的侧栏定位 → 真点复活)
    assert page.mouse.clicks.count((1.0, 2.0)) >= 1


def test_comment_threads_open_failure_continues_next_post(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    """开失败留痕不弃档:第一帖评论钮缺 → 跳过;第二帖照常展开."""
    monkeypatch.setenv("MYIA_HOME", str(tmp_path))
    (tmp_path / "telegram-web" / ACCOUNT).mkdir(parents=True)
    page = FakePage(
        window=[{"mid": "11", "text": "mihomo v1.19 发布",
                 "timestamp": 1761000000.0}],
        posts=[
            {"mid": "4294967708", "peerId": "-3770098404",
             "commentsCount": 1128, "isUnread": True},
            {"mid": "4294967709", "peerId": "-3770098404",
             "commentsCount": 704, "isUnread": False},
        ],
        thread=[_thread_reply("4295090517", "mihomo 线程福利")],
    )
    patch_browser(monkeypatch, page)
    # 第一帖的评论钮定位失败(post_missing 面:泡不在窗)
    real_evaluate = page.evaluate

    async def evaluate_with_missing_first(script: Any, arg: Any = None) -> Any:
        js = script if isinstance(script, str) else ""
        if "replies-element" in js and arg and arg.get("mid") == "4294967708":
            return {"ok": False, "reason": "post_missing"}
        return await real_evaluate(script, arg)

    page.evaluate = evaluate_with_missing_first  # type: ignore[method-assign]
    engine = TelegramWebEngine(
        make_tg_web_source(
            engine_options={"tg_web": {
                "account": ACCOUNT, "chat": CHAT, "keywords": ["mihomo"],
                "comments_max_threads": 3,
            }}
        ),
        tg_web_context(),
    )
    items = run(engine.fetch())
    urls = [item["url"] for item in items]
    assert f"{SOURCE_URL}#tg-{CHAT}-11" in urls
    assert f"{SOURCE_URL}#tg-{THREAD_PEER}-4295090517" in urls
    # 第二帖完整展开(2 次定位);第一帖零点击
    assert [mid for mid, _ in page.footer_locates] == [
        "4294967709", "4294967709",
    ]
    assert page.mouse.clicks.count(THREAD_FOOTER_XY) == 1


def test_comment_threads_half_mismatch_sentinel(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path, caplog: pytest.LogCaptureFixture
) -> None:
    """must_fix5 半失配哨兵:回泡 text 命中率 <80% → tg_web_dom_stale 词面
    留痕(不拦已读条目出仓)。"""
    import logging

    monkeypatch.setenv("MYIA_HOME", str(tmp_path))
    (tmp_path / "telegram-web" / ACCOUNT).mkdir(parents=True)
    thread = [_thread_reply("4295090517", "mihomo 线程福利")]
    thread += [
        _thread_reply(str(4295090520 + i), "") for i in range(1, 5)
    ]  # 4/5 回泡 text 空 → 命中率 0.2
    for entry in thread[1:]:
        entry["text"] = None
    page = FakePage(
        window=[{"mid": "11", "text": "mihomo v1.19 发布",
                 "timestamp": 1761000000.0}],
        posts=[{"mid": "4295090517", "peerId": THREAD_PEER,
                "commentsCount": 5, "isUnread": False}],
        thread=thread,
    )
    patch_browser(monkeypatch, page)
    engine = TelegramWebEngine(
        make_tg_web_source(
            engine_options={"tg_web": {
                "account": ACCOUNT, "chat": CHAT, "keywords": ["mihomo"],
                "comments_max_threads": 3,
            }}
        ),
        tg_web_context(),
    )
    with caplog.at_level(logging.WARNING, logger="myssia.engines.tg_web"):
        items = run(engine.fetch())
    assert any(
        "tg_web_dom_stale" in message and "命中率" in message
        for message in caplog.messages
    )
    urls = [item["url"] for item in items]
    assert f"{SOURCE_URL}#tg-{THREAD_PEER}-4295090517" in urls  # 已读照常出仓


def test_comment_threads_zero_candidates_is_noop(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    """窗口内帖全无评论钮 → 零候选留痕,零交互零错误."""
    monkeypatch.setenv("MYIA_HOME", str(tmp_path))
    (tmp_path / "telegram-web" / ACCOUNT).mkdir(parents=True)
    page = FakePage(
        window=[{"mid": "11", "text": "mihomo v1.19 发布",
                 "timestamp": 1761000000.0}],
        posts=[{"mid": "4294967633", "peerId": "-3770098404",
                "commentsCount": 0, "isUnread": False}],
    )
    patch_browser(monkeypatch, page)
    engine = TelegramWebEngine(
        make_tg_web_source(
            engine_options={"tg_web": {
                "account": ACCOUNT, "chat": CHAT, "keywords": ["mihomo"],
                "comments_max_threads": 3,
            }}
        ),
        tg_web_context(),
    )
    items = run(engine.fetch())
    assert [item["url"] for item in items] == [f"{SOURCE_URL}#tg-{CHAT}-11"]
    assert page.footer_locates == []
    assert engine.last_skip_reason is None
