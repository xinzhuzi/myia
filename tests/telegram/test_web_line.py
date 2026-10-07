"""W1: TG 网页线登录器与配置档(10-08-tg-web-line)—— 全 mock 零网络零浏览器.

覆盖:账号键校验/配置档路径与权限硬化/账号列表/list 登录标记复用/force 删档/
成功登录落标记/超时结构化/依赖门(缺 playwright)/DOM 面映射(dom_message_to_update
与 JS 件形态)。Fake playwright 经 ``playwright_factory`` 注入(web_line 全注入面)。
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest

from myssia.telegram.web_line import (
    ACCOUNT_KEY_RE,
    PROFILE_DIR_MODE,
    PROFILE_FILE_MODE,
    PROFILE_ROOT_DIR,
    TelegramWebError,
    TelegramWebLoginFlow,
    check_logged_in,
    harden_profile_permissions,
    list_accounts,
    login_marker_path,
    profile_dir,
    profile_root,
    read_login_marker,
    require_playwright,
    validate_account_key,
)


# --------------------------------------------------------------------- fakes


class FakePage:
    """登录轮询面 fake:evaluate(script, arg) 按队列吐登录态."""

    def __init__(self, states: list[dict[str, Any]]) -> None:
        self._states = list(states)
        self.goto_calls: list[str] = []

    async def goto(self, url: str, **_: Any) -> None:
        self.goto_calls.append(url)

    async def evaluate(self, script: Any, arg: Any = None) -> Any:
        if callable(script):  # 注入件是 callable 形态时真执行(JS fake 面)
            return script(arg)
        return self._states.pop(0) if self._states else {"state": "unknown"}


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


class FakeChromium:
    def __init__(self, context: FakeContext) -> None:
        self._context = context
        self.launch_args: dict[str, Any] | None = None

    async def launch_persistent_context(
        self, directory: str, **kwargs: Any
    ) -> FakeContext:
        self.launch_args = {"directory": directory, **kwargs}
        return self._context


class FakeStarted:
    def __init__(self, chromium: FakeChromium) -> None:
        self.chromium = chromium


class FakeHandle:
    def __init__(self, context: FakeContext) -> None:
        self._started = FakeStarted(FakeChromium(context))
        self.stopped = False

    async def start(self) -> FakeStarted:
        return self._started

    async def stop(self) -> None:
        self.stopped = True


def make_factory(
    states: list[dict[str, Any]],
) -> tuple[Any, FakeHandle, FakeContext, FakePage]:
    page = FakePage(states)
    context = FakeContext(page)
    handle = FakeHandle(context)
    return (lambda: handle), handle, context, page


# ------------------------------------------------------------- 账号键与路径


@pytest.mark.parametrize(
    "key",
    ["telegram-alt1", "telegram-a", "telegram-main_01", "telegram-x9"],
)
def test_account_key_valid_shapes(key: str) -> None:
    assert validate_account_key(key) == key
    assert ACCOUNT_KEY_RE.match(key)


@pytest.mark.parametrize(
    "bad",
    [
        "",
        "alt1",  # 缺 telegram- 前缀(全称律)
        "Telegram-Alt",  # 大写
        "telegram--x",  # 连字符起头
        "telegram-工具",  # 非 ASCII
        "../escape",  # 目录穿越面
        "telegram-a" * 30,  # 超长
        None,
    ],
)
def test_account_key_invalid_structured(bad: Any) -> None:
    with pytest.raises(TelegramWebError) as exc_info:
        validate_account_key(bad)
    assert exc_info.value.reason == "invalid_account"
    assert exc_info.value.fatal is True


def test_profile_dir_shape_and_root(tmp_path: Path) -> None:
    directory = profile_dir(tmp_path, "telegram-alt1")
    assert directory == tmp_path / PROFILE_ROOT_DIR / "telegram-alt1"
    assert profile_root(tmp_path) == tmp_path / "telegram-web"


def test_profile_dir_rejects_traversal(tmp_path: Path) -> None:
    with pytest.raises(TelegramWebError):
        profile_dir(tmp_path, "../../etc")


def test_list_accounts_missing_root_and_sorted(tmp_path: Path) -> None:
    assert list_accounts(tmp_path) == []
    for key in ("telegram-b", "telegram-a"):
        profile_dir(tmp_path, key).mkdir(parents=True)
    (profile_root(tmp_path) / "not-a-key").mkdir()
    assert list_accounts(tmp_path) == ["telegram-a", "telegram-b"]


def test_harden_profile_permissions(tmp_path: Path) -> None:
    directory = profile_dir(tmp_path, "telegram-alt1")
    sub = directory / "Default"
    sub.mkdir(parents=True)
    cookie = sub / "Cookies"
    cookie.write_text("{}")
    cookie.chmod(0o644)
    harden_profile_permissions(directory)
    assert (directory.stat().st_mode & 0o777) == PROFILE_DIR_MODE
    assert (sub.stat().st_mode & 0o777) == PROFILE_DIR_MODE
    assert (cookie.stat().st_mode & 0o777) == PROFILE_FILE_MODE


# --------------------------------------------------------------- 登录流


def test_login_reuses_marker_without_browser(tmp_path: Path) -> None:
    directory = profile_dir(tmp_path, "telegram-alt1")
    directory.mkdir(parents=True)
    marker = login_marker_path(directory)
    marker.write_text(
        json.dumps({"logged_in_at": "2026-10-08T00:00:00+00:00"}),
        encoding="utf-8",
    )
    lines: list[str] = []
    flow = TelegramWebLoginFlow(
        print_fn=lines.append,
        playwright_factory=lambda: pytest.fail("复用路径不得启动浏览器"),
    )
    import asyncio

    result = asyncio.run(flow.run(tmp_path, "telegram-alt1"))
    assert result == directory
    assert any("直接复用" in line for line in lines)


def test_login_success_flow_writes_marker_and_hardens(
    tmp_path: Path,
) -> None:
    factory, handle, context, page = make_factory(
        [{"state": "logged_out"}, {"state": "logged_in", "hit": ".chatlist-container"}]
    )
    lines: list[str] = []
    flow = TelegramWebLoginFlow(
        print_fn=lines.append, playwright_factory=factory, timeout_seconds=5
    )
    import asyncio

    directory = asyncio.run(flow.run(tmp_path, "telegram-alt1"))
    assert page.goto_calls == ["https://web.telegram.org"]
    assert handle.stopped and context.closed
    marker = read_login_marker(directory)
    assert marker is not None and marker.get("line") == "tg_web"
    assert (directory.stat().st_mode & 0o777) == PROFILE_DIR_MODE
    assert any("披露" in line for line in lines)  # 诚实披露在成功回执
    # chromium 以非无头形态启动(headed 登录窗)
    launched = handle._started.chromium.launch_args
    assert launched is not None and launched["headless"] is False
    assert launched["directory"] == str(directory)


def test_login_force_deletes_stale_profile(tmp_path: Path) -> None:
    directory = profile_dir(tmp_path, "telegram-alt1")
    stale = directory / "Default" / "Cookies"
    stale.parent.mkdir(parents=True)
    stale.write_text("stale")
    login_marker_path(directory).write_text("{}", encoding="utf-8")
    factory, _, _, _ = make_factory([{"state": "logged_in", "hit": ".chatlist-container"}])
    lines: list[str] = []
    flow = TelegramWebLoginFlow(print_fn=lines.append, playwright_factory=factory)
    import asyncio

    asyncio.run(flow.run(tmp_path, "telegram-alt1", force=True))
    assert not stale.exists()  # 旧 cookies 已随整档删除
    assert any("--force" in line or "已删除旧配置档" in line for line in lines)


def test_login_timeout_is_structured(tmp_path: Path) -> None:
    factory, handle, _, _ = make_factory(
        [{"state": "logged_out"}] * 50
    )
    flow = TelegramWebLoginFlow(print_fn=lambda _: None, playwright_factory=factory, timeout_seconds=0.1)
    import asyncio

    with pytest.raises(TelegramWebError) as exc_info:
        asyncio.run(flow.run(tmp_path, "telegram-alt1"))
    assert exc_info.value.reason == "login_timeout"
    assert exc_info.value.fatal is True
    assert handle.stopped  # 超时路径资源也收尾


def test_login_invalid_account_never_launches(tmp_path: Path) -> None:
    flow = TelegramWebLoginFlow(
        print_fn=lambda _: None,
        playwright_factory=lambda: pytest.fail("键校验先于浏览器"),
    )
    import asyncio

    with pytest.raises(TelegramWebError) as exc_info:
        asyncio.run(flow.run(tmp_path, "bad-key"))
    assert exc_info.value.reason == "invalid_account"


def test_require_playwright_missing_is_structured(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    import builtins

    real_import = builtins.__import__

    def fake_import(name: str, *args: Any, **kw: Any) -> Any:
        if name.startswith("playwright"):
            raise ImportError("no playwright")
        return real_import(name, *args, **kw)

    monkeypatch.setattr(builtins, "__import__", fake_import)
    with pytest.raises(TelegramWebError) as exc_info:
        require_playwright()
    assert exc_info.value.reason == "dependency_missing"
    assert "myssia[crawl4ai]" in str(exc_info.value)


# --------------------------------------------------------------- 探针


def test_check_logged_in_missing_profile_is_explicit_empty(
    tmp_path: Path,
) -> None:
    import asyncio

    logged_in, note = asyncio.run(check_logged_in(tmp_path, "telegram-alt1"))
    assert logged_in is False
    assert note == "profile_missing"


def test_check_logged_in_ok_and_logged_out(
    tmp_path: Path,
) -> None:
    import asyncio

    directory = profile_dir(tmp_path, "telegram-alt1")
    directory.mkdir(parents=True)
    factory, _, _, page = make_factory(
        [{"state": "logged_in", "hit": ".chatlist-container"}]
    )
    logged_in, note = asyncio.run(
        check_logged_in(tmp_path, "telegram-alt1", playwright_factory=factory)
    )
    assert (logged_in, note) == (True, "ok")
    assert page.goto_calls == ["https://web.telegram.org"]

    factory2, _, _, _ = make_factory([{"state": "logged_out"}] * 30)
    logged_in2, note2 = asyncio.run(
        check_logged_in(
            tmp_path, "telegram-alt1", timeout_seconds=0.2, playwright_factory=factory2
        )
    )
    assert logged_in2 is False
    assert note2 == "logged_out_or_dom_stale"


# --------------------------------------------------------------- DOM 面


def test_dom_message_to_update_full_mapping() -> None:
    from myssia.telegram.web_dom import dom_message_to_update

    update = dom_message_to_update(
        {
            "mid": "12345",
            "text": "mihomo 新版本 v1.19 发布",
            "sender": "翦翦风",
            "timestamp": 1760000000.0,
            "has_media": False,
        },
        chat_id="-1001234567890",
        chat_title="mihomo_party_group",
    )
    message = update["message"]
    assert update["update_id"] == 12345
    assert message["message_id"] == 12345
    assert message["chat"]["id"] == "-1001234567890"
    assert message["chat"]["title"] == "mihomo_party_group"
    assert message["text"] == "mihomo 新版本 v1.19 发布"
    assert message["date"] == 1760000000.0
    assert message["from"] == {"first_name": "翦翦风"}


def test_dom_message_to_update_media_only_and_bad_mid_skipped() -> None:
    from myssia.telegram.web_dom import dom_message_to_update

    assert (
        dom_message_to_update(
            {"mid": "1", "text": None, "has_media": True}, chat_id="c"
        )
        is None
    )
    assert (
        dom_message_to_update(
            {"mid": "not-a-number", "text": "hi"}, chat_id="c"
        )
        is None
    )
    assert dom_message_to_update({"text": "无 mid"}, chat_id="c") is None


def test_dom_update_feeds_bot_line_updates_to_items() -> None:
    """同形复用铁证:网页线 update 直接进 bot 线分拣/锚(零改动)."""
    from myssia.engines.telegram import updates_to_items
    from myssia.telegram.web_dom import dom_message_to_update

    update = dom_message_to_update(
        {"mid": "77", "text": "关键词 mihomo", "timestamp": 1760000000.0},
        chat_id="-1001234567890",
    )
    items = updates_to_items([update], "-1001234567890", source_url="https://web.telegram.org")
    assert len(items) == 1
    assert items[0]["url"] == "https://web.telegram.org#tg--1001234567890-77"
    assert items[0]["title"] == "关键词 mihomo"


def test_observer_js_shapes() -> None:
    from myssia.telegram.web_dom import (
        drain_observer_js,
        extract_message_js,
        install_observer_js,
        open_chat_js,
    )

    install_js = install_observer_js()
    assert "MutationObserver" in install_js
    assert "already_installed" in install_js  # 幂等面
    assert "container_missing" in install_js  # DOM 失配如实报
    drain = drain_observer_js()
    assert "splice(0)" in drain
    extract = extract_message_js()
    assert "data-mid" in extract
    assert "has_media" in extract
    assert "TEXT_SELECTORS" in extract  # 选择器表烙进 JS 体
    opened = open_chat_js()
    assert "search_box_missing" in opened
    assert "chat_not_found" in opened


def test_collect_window_updates_via_fake_evaluate(tmp_path: Path) -> None:
    """批量档窗口读取:page.evaluate(fake callable 形态)→ update 列表."""
    import asyncio

    from myssia.telegram.web_dom import collect_window_updates, collect_messages_js

    class CollectPage:
        async def evaluate(self, script: Any, arg: Any = None) -> Any:
            js = script if isinstance(script, str) else script()
            assert "querySelectorAll" in js
            return [
                {"mid": "1", "text": "第一条", "timestamp": 10.0},
                {"mid": "2", "text": None, "has_media": True},  # 纯媒体跳过
                {"mid": "3", "text": "第三条", "timestamp": 30.0},
            ]

    updates = asyncio.run(
        collect_window_updates(
            CollectPage(), chat_id="-100", chat_title="群", limit=50
        )
    )
    assert [u["message"]["message_id"] for u in updates] == [1, 3]
    assert collect_messages_js(limit=5).startswith("const LIMIT = 5;")
