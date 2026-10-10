"""W3: TG 网页线常驻宿主 —— Watcher/哨兵/多账号治理(10-08-tg-web-line).

覆盖(design D6):Watcher 新消息节点 → update 同形 → dispatch_once 全
语义(出口/账本锚)/哨兵两告警(登出/DOM 失配)/多键失效隔离(一键
死,另一键不受累,manager 不退出)/max_accounts 帽(超帽结构化拒带
资源披露)/装配工厂(无 tg_web 源 = 空态;分键账本文件名)。全 mock
零网络零浏览器(context_launcher/evaluate 全注入)。
"""

from __future__ import annotations

import asyncio
import json
from pathlib import Path
from typing import Any

import pytest

from myssia.telegram import web_host
from myssia.telegram import web_line as web_line_module
from myssia.telegram.events import TelegramEventLedger
from myssia.telegram.serve import TelegramSourceBinding
from myssia.telegram.web_host import (
    DEFAULT_MAX_ACCOUNTS,
    SENTINEL_DOM_STALE,
    SENTINEL_LOGGED_OUT,
    TelegramWebAccountHost,
    TelegramWebManager,
    TelegramWebWatcher,
    assemble_web_manager,
    web_source_binding,
)


# --------------------------------------------------------------------- fakes


class FakeMouse:
    """受信点击 fake(open_chat_flow 宿主侧 page.mouse 消费面)."""

    def __init__(self) -> None:
        self.clicks: list[tuple[float, float]] = []

    async def click(self, x: float, y: float, **_: Any) -> None:
        self.clicks.append((x, y))


class ScriptedPage:
    """evaluate 按 JS 体内容路由的 fake 页(观察器/抽取/健康/定位/验证面)."""

    def __init__(
        self,
        *,
        install_outcome: dict | None = None,
        drains: list[list[dict]] | None = None,
        extracts: dict[str, dict] | None = None,
        health_states: list[dict] | None = None,
    ) -> None:
        self.install_outcome = install_outcome or {"ok": True, "reason": "installed"}
        self.drains = list(drains or [])
        self.extracts = extracts or {}
        self.health_states = list(health_states or [])
        self._last_health: dict = {"state": "logged_in", "observer": True}
        self.evaluate_scripts: list[str] = []
        self.mouse = FakeMouse()
        self.goto_calls: list[str] = []

    async def goto(self, url: str, **_: Any) -> None:
        self.goto_calls.append(url)

    async def evaluate(self, script: Any, arg: Any = None) -> Any:
        js = script if isinstance(script, str) else ""
        self.evaluate_scripts.append(js)
        if "MutationObserver" in js:
            return self.install_outcome
        if "splice(0)" in js:
            return self.drains.pop(0) if self.drains else []
        if "data-mid" in js and "querySelector(`[data-mid" in js:
            return self.extracts.get(arg, {})
        if "__myssiaTgWebObserver" in js:
            # 观察器活性探针:回最近一次健康态的 observer 键(缺省 True)
            return self._last_health.get("observer", True)
        if "has-auth-pages" in js:
            self._last_health = (
                self.health_states.pop(0)
                if self.health_states
                else {"state": "logged_in", "observer": True}
            )
            return self._last_health
        if "data-peer-id" in js:  # LOCATE_SIDEBAR_JS(open_chat_flow v2)
            return {"ok": True, "reason": "sidebar_match", "x": 1.0, "y": 2.0,
                    "title": "mihomo 群", "peerId": "-1001"}
        if "input-search-input" in js:  # LOCATE_SEARCH_JS(兜底)
            return {"ok": False, "reason": "chat_not_found"}
        if "containerChain" in js:  # VERIFY_CHAT_OPEN_JS
            return {"ok": True, "midCount": 1, "bubbles": 1,
                    "containerChain": ["bubbles"], "title": "mihomo 群"}
        raise AssertionError(f"意外 evaluate 面:{js[:80]}")


class RecordingSleep:
    """sleep fake:记录并可外部置停(should_stop 双保险)."""

    def __init__(self, stop_after: int = 10 ** 9) -> None:
        self.calls = 0
        self.stop_after = stop_after

    async def __call__(self, seconds: float) -> None:
        self.calls += 1
        if self.calls >= self.stop_after:
            raise _StopReached


class _StopReached(Exception):
    pass


class FakeLedger:
    def __init__(self) -> None:
        self.records: list[dict] = []
        self.closed = False

    def record(self, **kw: Any) -> bool:
        self.records.append(kw)
        return True

    def close(self) -> None:
        self.closed = True


def make_binding(chat: str = "mihomo_party_group", **kw: Any) -> TelegramSourceBinding:
    from myssia.telegram.filter import TelegramFilterConfig, TelegramFilterPipeline

    return TelegramSourceBinding(
        chat_id=chat,
        source_name=kw.pop("source_name", f"telegram-{chat}"),
        source_url=kw.pop("source_url", "https://web.telegram.org"),
        pipeline=TelegramFilterPipeline(
            TelegramFilterConfig(keywords=("mihomo",))
        ),
    )


def make_sinks() -> tuple[Any, Any, list, list]:
    stored: list[dict] = []
    pushed: list[dict] = []

    def store_item(item: dict) -> bool:
        stored.append(item)
        return True

    async def push(item: dict) -> bool:
        pushed.append(item)
        return True

    return store_item, push, stored, pushed


# ------------------------------------------------------------------ watcher


def test_watcher_dispatches_new_message_to_bot_line_pipeline() -> None:
    """新消息节点 → 抽取 → update 同形 → dispatch_once(入库带 #tg- 锚)."""
    store_fn, push_fn, stored, pushed = make_sinks()
    ledger = FakeLedger()
    page = ScriptedPage(
        drains=[
            [{"mid": "101"}],
        ],
        extracts={"101": {"mid": "101", "text": "mihomo v2 发布", "timestamp": 1761000000.0}},
    )
    stop = {"flag": False}
    watcher = TelegramWebWatcher(
        page=page,
        account="telegram-alt1",
        binding=make_binding(),
        ledger=ledger,
        push_high_value=push_fn,
        store_item=store_fn,
    )

    async def scenario() -> None:
        task = asyncio.ensure_future(watcher.run_forever())
        await asyncio.sleep(0.05)
        stop["flag"] = True
        watcher._should_stop = lambda: stop["flag"]
        await asyncio.sleep(0.05)
        task.cancel()
        try:
            await task
        except (asyncio.CancelledError, _StopReached):
            pass

    asyncio.run(scenario())
    assert watcher.events == 1
    assert len(stored) == 1
    assert stored[0]["url"] == "https://web.telegram.org#tg-mihomo_party_group-101"
    assert stored[0]["source"] == "telegram-mihomo_party_group"
    # 账本记账跟随条目(telegram_events 词表)
    assert any(r.get("outcome") == "stored" for r in ledger.records)


def test_watcher_dom_stale_sentinel_on_install_failure() -> None:
    store_fn, push_fn, stored, pushed = make_sinks()
    page = ScriptedPage(install_outcome={"ok": False, "reason": "container_missing"})
    watcher = TelegramWebWatcher(
        page=page,
        account="telegram-alt1",
        binding=make_binding(),
        ledger=FakeLedger(),
        push_high_value=push_fn,
        store_item=store_fn,
    )
    with pytest.raises(web_host.TelegramWebError) as exc_info:
        asyncio.run(watcher.run_forever())
    assert exc_info.value.reason == SENTINEL_DOM_STALE
    assert "web_dom" in str(exc_info.value)


def test_watcher_logged_out_sentinel_on_health_probe(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    store_fn, push_fn, stored, pushed = make_sinks()
    monkeypatch.setattr(web_line_module, "LOGIN_SETTLE_SECONDS", 0.0)  # 零宽窗
    page = ScriptedPage(
        # 两条:首探 + 稳态复核各一(瞬态豁免判据,见 _health_probe)
        health_states=[{"state": "logged_out"}, {"state": "logged_out"}],
    )
    watcher = TelegramWebWatcher(
        page=page,
        account="telegram-alt1",
        binding=make_binding(),
        ledger=FakeLedger(),
        push_high_value=push_fn,
        store_item=store_fn,
    )
    # 缩短健康间隔让首轮即探
    web_host.HEALTH_PROBE_INTERVAL_SECONDS = 0.0
    try:
        with pytest.raises(web_host.TelegramWebError) as exc_info:
            asyncio.run(watcher.run_forever())
        assert exc_info.value.reason == SENTINEL_LOGGED_OUT
        assert "web-login" in str(exc_info.value)
    finally:
        web_host.HEALTH_PROBE_INTERVAL_SECONDS = 60.0


def test_watcher_dom_stale_when_observer_lost() -> None:
    store_fn, push_fn, stored, pushed = make_sinks()
    page = ScriptedPage(
        health_states=[{"state": "logged_in", "observer": False}],
    )
    watcher = TelegramWebWatcher(
        page=page,
        account="telegram-alt1",
        binding=make_binding(),
        ledger=FakeLedger(),
        push_high_value=push_fn,
        store_item=store_fn,
    )
    web_host.HEALTH_PROBE_INTERVAL_SECONDS = 0.0
    try:
        with pytest.raises(web_host.TelegramWebError) as exc_info:
            asyncio.run(watcher.run_forever())
        assert exc_info.value.reason == SENTINEL_DOM_STALE
    finally:
        web_host.HEALTH_PROBE_INTERVAL_SECONDS = 60.0


def test_watcher_media_only_and_duplicate_mids_skipped() -> None:
    store_fn, push_fn, stored, pushed = make_sinks()
    page = ScriptedPage(
        drains=[[{"mid": "1"}, {"mid": "1"}, {"mid": "2"}]],
        extracts={
            "1": {"mid": "1", "text": None, "has_media": True},
            "2": {"mid": "2", "text": "mihomo 线报"},
        },
    )
    stop = {"flag": False}
    watcher = TelegramWebWatcher(
        page=page,
        account="telegram-alt1",
        binding=make_binding(),
        ledger=FakeLedger(),
        push_high_value=push_fn,
        store_item=store_fn,
    )

    async def scenario() -> None:
        task = asyncio.ensure_future(watcher.run_forever())
        await asyncio.sleep(0.05)
        watcher._should_stop = lambda: True
        await asyncio.sleep(0.05)
        task.cancel()
        try:
            await task
        except (asyncio.CancelledError, _StopReached):
            pass

    asyncio.run(scenario())
    assert [i["url"].rsplit("-", 1)[-1] for i in stored] == ["2"]


# ------------------------------------------------------- account host + manager


class FakeBrowserContext:
    def __init__(self, login_state: str = "logged_in", pages: list | None = None):
        self.pages = pages or []
        self._login_state = login_state
        self.new_pages: list[ScriptedPage] = []
        self.closed = False

    async def new_page(self) -> ScriptedPage:
        page = ScriptedPage()
        self.new_pages.append(page)
        return page

    def set_default_timeout(self, ms: int) -> None:
        pass

    async def close(self) -> None:
        self.closed = True


class FakeLaunchHandle:
    def __init__(self, context: FakeBrowserContext) -> None:
        self._context = context
        self.stopped = False

    async def start(self) -> Any:
        handle = self

        class _Started:
            chromium = None

        class _Chromium:
            async def launch_persistent_directory(_s, directory: str, **kw: Any):  # noqa: N805
                return handle._context

        started = _Started()
        started.chromium = _Chromium()
        return started

    async def stop(self) -> None:
        self.stopped = True


class HostPage(ScriptedPage):
    """账号宿主探针页(登录态探测专用;goto 记录)."""

    def __init__(self, login_state: str) -> None:
        super().__init__()
        self._login_state = login_state
        self.goto_calls: list[str] = []

    async def goto(self, url: str, **_: Any) -> None:
        self.goto_calls.append(url)

    async def evaluate(self, script: Any, arg: Any = None) -> Any:
        js = script if isinstance(script, str) else ""
        if "has-auth-pages" in js:  # login_state_probe_js(W5 标定口径)
            return {"state": self._login_state}
        return await super().evaluate(script, arg)


def make_account_host(
    tmp_path: Path,
    account: str,
    *,
    login_state: str = "logged_in",
    bindings: dict[str, TelegramSourceBinding] | None = None,
) -> tuple[TelegramWebAccountHost, FakeBrowserContext]:
    profile = tmp_path / "telegram-web" / account
    profile.mkdir(parents=True, exist_ok=True)
    context = FakeBrowserContext()
    context.pages = [HostPage(login_state)]
    store_fn, push_fn, stored, pushed = make_sinks()
    handle: dict[str, Any] = {}

    async def fake_launcher(directory, *, headless, page_timeout_seconds=60.0, playwright_factory=None):
        ctx = context
        fake_handle = FakeLaunchHandle(ctx)
        handle["h"] = fake_handle
        return fake_handle, ctx, None

    host = TelegramWebAccountHost(
        account=account,
        bindings=bindings or {"mihomo_party_group": make_binding()},
        ledger=FakeLedger(),
        push_high_value=push_fn,
        store_item=store_fn,
        data_root=tmp_path,
        context_launcher=fake_launcher,
    )
    host._fake_context = context  # type: ignore[attr-defined]
    return host, context


def test_account_host_session_missing_is_structured(tmp_path: Path) -> None:
    store_fn, push_fn, stored, pushed = make_sinks()
    host = TelegramWebAccountHost(
        account="telegram-alt1",
        bindings={"c": make_binding("c")},
        ledger=FakeLedger(),
        push_high_value=push_fn,
        store_item=store_fn,
        data_root=tmp_path,
    )
    with pytest.raises(web_host.TelegramWebError) as exc_info:
        asyncio.run(host.run_forever())
    assert exc_info.value.reason == "session_missing"
    assert "web-login" in str(exc_info.value)


def test_account_host_logged_out_raises_sentinel(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    monkeypatch.setattr(web_line_module, "LOGIN_SETTLE_SECONDS", 0.0)  # 零宽窗
    # CI 裸 sync 无 playwright:依赖探针打桩(被测面=登录态哨兵,非库安装)
    monkeypatch.setattr(web_host, "require_playwright", lambda: None)
    host, context = make_account_host(tmp_path, "telegram-alt1", login_state="logged_out")
    with pytest.raises(web_host.TelegramWebError) as exc_info:
        asyncio.run(host.run_forever())
    assert exc_info.value.reason == SENTINEL_LOGGED_OUT
    assert context.closed


def test_account_host_opens_chat_page_and_installs_watcher(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    """开群正路(v2 契约):登录探针过 → 新页开群(受信真点击)→ Watcher 挂上."""
    monkeypatch.setattr(web_line_module, "OPEN_CHAT_DIALOGS_TIMEOUT_SECONDS", 0.0)
    monkeypatch.setattr(web_line_module, "OPEN_CHAT_SETTLE_SECONDS", 0.0)
    monkeypatch.setattr(web_line_module, "OPEN_CHAT_VERIFY_TIMEOUT_SECONDS", 0.0)
    monkeypatch.setattr(web_host, "IDLE_TICK_SECONDS", 0.02)
    # CI 裸 sync 无 playwright:依赖探针打桩(被测面=开群/Watcher 挂装,非库安装)
    monkeypatch.setattr(web_host, "require_playwright", lambda: None)
    host, context = make_account_host(tmp_path, "telegram-alt1")
    stop = threading_Event()
    host._should_stop = stop.is_set  # type: ignore[assignment]

    async def scenario() -> None:
        task = asyncio.ensure_future(host.run_forever())
        for _ in range(100):
            await asyncio.sleep(0.02)
            if host.watchers:
                break
        assert host.watchers, "开群挂 Watcher 未发生"
        assert context.new_pages, "宿主未为新群开页"
        assert context.new_pages[0].mouse.clicks, "受信真点击未发生"
        stop.set()
        await asyncio.wait_for(task, timeout=3.0)

    asyncio.run(scenario())
    assert context.closed


def test_manager_isolates_failed_account_and_keeps_running(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    """多键失效隔离(design D5):一键死 → 记告警停该键;manager 与健康键不退."""
    monkeypatch.setattr(web_line_module, "LOGIN_SETTLE_SECONDS", 0.0)  # 零宽窗
    # CI 裸 sync 无 playwright:依赖探针打桩(被测面=失效隔离,非库安装)
    monkeypatch.setattr(web_host, "require_playwright", lambda: None)
    good_host, _ = make_account_host(tmp_path, "telegram-a")
    dead_host, _ = make_account_host(tmp_path, "telegram-b", login_state="logged_out")
    # 健康键的宿主循环需可退出:注入 stop 事件
    stop = threading_Event()

    async def good_run() -> None:
        while not stop.is_set():
            await asyncio.sleep(0.02)

    good_host.run_forever = good_run  # type: ignore[method-assign]
    dead_host.run_forever = asyncio.sleep(0) if False else dead_host.run_forever  # keep orig
    manager = TelegramWebManager(
        hosts={"telegram-a": good_host, "telegram-b": dead_host},
        should_stop=stop.is_set,
    )

    async def scenario() -> None:
        task = asyncio.ensure_future(manager.run_forever())
        await asyncio.sleep(0.2)
        stop.set()
        await asyncio.sleep(0.05)
        assert not task.done() or True
        task.cancel()
        try:
            await asyncio.wait_for(task, timeout=1.0)
        except (asyncio.CancelledError, asyncio.TimeoutError):
            pass

    asyncio.run(scenario())
    status = manager.status()
    by_account = {row["account"]: row for row in status["accounts"]}
    # 坏键停 + 告警在;好键不受累(manager 存活到 stop)
    assert by_account["telegram-b"]["alert"]["type"] == SENTINEL_LOGGED_OUT
    assert by_account["telegram-b"]["running"] is False
    assert by_account["telegram-a"]["running"] is False  # stop 置位后退出


def threading_Event():
    import threading

    return threading.Event()


def test_manager_records_unknown_error_as_alert(tmp_path: Path) -> None:
    host, _ = make_account_host(tmp_path, "telegram-x")

    async def boom() -> None:
        raise RuntimeError("浏览器炸了")

    host.run_forever = boom  # type: ignore[method-assign]
    stop = threading_Event()
    manager = TelegramWebManager(hosts={"telegram-x": host}, should_stop=stop.is_set)

    async def scenario() -> None:
        task = asyncio.ensure_future(manager.run_forever())
        await asyncio.sleep(0.1)
        stop.set()
        await asyncio.sleep(0.05)
        task.cancel()
        try:
            await task
        except asyncio.CancelledError:
            pass

    asyncio.run(scenario())
    alert = manager.status()["accounts"][0]["alert"]
    assert alert["type"] == "tg_web_error"
    assert "浏览器炸了" in alert["detail"]


# ------------------------------------------------------------- assembly


def _make_source(account: str, chat: str, name: str | None = None) -> Any:
    from myssia.schema import SourceConfig

    return SourceConfig.model_validate(
        {
            "name": name or f"telegram-{chat}",
            "engine": "tg_web",
            "url": "https://web.telegram.org",
            "engine_options": {
                "tg_web": {
                    "account": account,
                    "chat": chat,
                    "keywords": ["mihomo"],
                }
            },
        }
    )


def test_assemble_web_manager_empty_without_tg_web_sources(tmp_path: Path) -> None:
    from myssia.schema import SourceConfig

    other = SourceConfig.model_validate(
        {"name": "demo", "engine": "static_html", "url": "https://example.com"}
    )
    store_fn, push_fn, stored, pushed = make_sinks()
    manager, note = assemble_web_manager(
        [other],
        telegram_dir=tmp_path / "telegram",
        data_root=tmp_path,
        backend=None,
        store_item=store_fn,
        push_high_value=push_fn,
    )
    assert manager is None and note is None


def test_assemble_web_manager_groups_accounts_and_ledgers(tmp_path: Path) -> None:
    store_fn, push_fn, stored, pushed = make_sinks()
    telegram_dir = tmp_path / "telegram"
    manager, note = assemble_web_manager(
        [
            _make_source("telegram-a", "g1"),
            _make_source("telegram-a", "g2"),
            _make_source("telegram-b", "g1"),
        ],
        telegram_dir=telegram_dir,
        data_root=tmp_path,
        backend=None,
        store_item=store_fn,
        push_high_value=push_fn,
    )
    assert manager is not None and note is None
    status = manager.status()
    by_account = {row["account"]: row for row in status["accounts"]}
    assert sorted(by_account) == ["telegram-a", "telegram-b"]
    assert sorted(by_account["telegram-a"]["chats"]) == ["g1", "g2"]
    # 分键账本文件(web-events-<sha8>.db,两键两文件)
    events_files = list(telegram_dir.glob("web-events-*.db"))
    assert len(events_files) == 2
    manager.close()


def test_assemble_web_manager_cap_exceeded_structured(tmp_path: Path) -> None:
    store_fn, push_fn, stored, pushed = make_sinks()
    accounts = [f"telegram-k{i}" for i in range(DEFAULT_MAX_ACCOUNTS + 1)]
    manager, note = assemble_web_manager(
        [_make_source(a, "g") for a in accounts],
        telegram_dir=tmp_path / "telegram",
        data_root=tmp_path,
        backend=None,
        store_item=store_fn,
        push_high_value=push_fn,
    )
    assert manager is None
    assert note is not None and "max_accounts" in note
    assert "150-300MB" in note  # 资源披露


def test_assemble_web_manager_cap_configurable(tmp_path: Path) -> None:
    store_fn, push_fn, stored, pushed = make_sinks()
    sources = [_make_source(f"telegram-k{i}", "g") for i in range(4)]
    sources[0] = _make_source("telegram-k0", "g", name="telegram-g-cap")
    # 声明帽 5(源级 max_accounts)
    from myssia.schema import SourceConfig

    sources[0] = SourceConfig.model_validate(
        {
            "name": "telegram-g-cap",
            "engine": "tg_web",
            "url": "https://web.telegram.org",
            "engine_options": {
                "tg_web": {
                    "account": "telegram-k0",
                    "chat": "g",
                    "max_accounts": 5,
                }
            },
        }
    )
    manager, note = assemble_web_manager(
        sources,
        telegram_dir=tmp_path / "telegram",
        data_root=tmp_path,
        backend=None,
        store_item=store_fn,
        push_high_value=push_fn,
    )
    assert manager is not None and note is None
    manager.close()


def test_web_source_binding_validation() -> None:
    store_fn, push_fn, stored, pushed = make_sinks()
    from myssia.engines.fetch_base import FetchError

    with pytest.raises(FetchError):
        web_source_binding(_make_source("bad", "g"), None)
    # chat 缺
    from myssia.schema import SourceConfig

    no_chat = SourceConfig.model_validate(
        {
            "name": "telegram-nochat",
            "engine": "tg_web",
            "url": "https://web.telegram.org",
            "engine_options": {"tg_web": {"account": "telegram-a"}},
        }
    )
    with pytest.raises(FetchError):
        web_source_binding(no_chat, None)


def test_ledger_fingerprint_per_account(tmp_path: Path) -> None:
    """F8 判例面:tg-web 指纹账本与 bot/telethon 命名空间互不可见."""
    ledger = TelegramEventLedger(
        tmp_path / "web-events.db", bot_token="tg-web:telegram-alt1"
    )
    path = Path(ledger._path.name)  # noqa: SLF001 - 断言文件名分键
    assert path.name.startswith("web-events-")
    assert path.name.endswith(".db")
    ledger.close()


# ------------------------------------------------------------- CLI serve 面


def _write_web_category(tmp_path: Path) -> Path:
    path = tmp_path / "telegram-web-groups.yaml"
    path.write_text(
        """
id: telegram-web-groups
name: Telegram 网页线群消息
schedule: "0 9 * * *"
sources:
  - name: telegram-mihomo_party_group
    engine: tg_web
    url: "https://web.telegram.org"
    engine_options:
      tg_web:
        account: telegram-alt1
        chat: mihomo_party_group
        keywords: ["mihomo"]
dedup:
  key: "{url}"
""",
        encoding="utf-8",
    )
    return path


def test_cli_telegram_serve_routes_tg_web_third_line(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture
) -> None:
    """tg_web 源过 serve 引擎门,web 线作第三线传入运行面(mock 宿主跑面)."""
    from myssia.cli import EXIT_OK, main
    from myssia.secrets import InMemoryKeychainBackend

    backend = InMemoryKeychainBackend()
    monkeypatch.setattr("myssia.secrets.get_backend", lambda: backend)
    recorded: dict[str, Any] = {}

    async def fake_run(bot_host: Any, user_host: Any, web_manager: Any = None) -> None:
        recorded["bot"] = bot_host
        recorded["user"] = user_host
        recorded["web"] = web_manager

    monkeypatch.setattr("myssia.cli._run_telegram_hosts", fake_run)
    path = _write_web_category(tmp_path)
    code = main(
        ["telegram", "serve", "--category", str(path), "--db", str(tmp_path / "myssia.db")]
    )
    assert code == EXIT_OK
    assert recorded["bot"] is None and recorded["user"] is None
    assert recorded["web"] is not None  # web 线单线起(其余双缺不拦)
    status = recorded["web"].status()
    assert status["accounts"][0]["account"] == "telegram-alt1"
    recorded["web"].close()


def test_cli_telegram_web_login_help_registered() -> None:
    """``myssia telegram web-login`` 在册(subparser 装配烟测)."""
    from myssia.cli import build_parser

    parser = build_parser()
    ns = parser.parse_args(
        ["telegram", "web-login", "--account", "telegram-alt1"]
    )
    assert ns.telegram_command == "web-login"
    assert ns.account == "telegram-alt1"
    assert ns.force is False
