"""TG 网页线常驻宿主 —— Watcher/哨兵/多账号治理(10-08-tg-web-line W3).

「每时每刻过滤」的 web 线常驻档(serve 第三线,与 bot 长轮询线/telethon
事件线并跑):每**账号键**一个无头 Chromium persistent context(design D1
「每键一 Host」),每**(账号×群)**一个 Watcher 页 —— ``page.evaluate``
注入 ``MutationObserver``(``web_dom.install_observer_js``)盯消息容器,
新消息节点到达 → ``data-mid`` 入页内事件队列 → 宿主轮询取走 → 单条
抽取(``extract_message_js``)→ ``dom_message_to_update`` → Bot API update
同形 → **bot 线 ``TelegramServeHost.dispatch_once`` 全语义复用**(分拣/
过滤/出口/账本/媒体组记忆;telethon 用户线同款判例)。

哨兵(design D3,绝不装死):

- ``tg_web_logged_out`` —— 登录态丢失(被踢/会话过期:登录表单重新
  出现或会话列表消失):该账号全部 Watcher 停 + 结构化告警(账本
  ``error`` 行 + 宿主内存态 + 日志),其他账号不受累(design D5 失效
  隔离);重登指引 ``myssia telegram web-login --account <键> --force``;
- ``tg_web_dom_stale`` —— DOM 选择器失配(会话列表/消息容器/观察器
  面全不中):同上停+告警,指引 = 重标定 ``web_dom`` 选择器表(跟修)。

多账号治理(design D5):

- 失效隔离:单键宿主死亡只停该键,manager 记告警不复活不退出 ——
  「serve 重启全量拉起各键」,重启由人决定;
- 资源帽:``max_accounts``(缺省 :data:`DEFAULT_MAX_ACCOUNTS` = 3,
  ``engine_options.tg_web.max_accounts`` 任一源声明即取最大):超帽的键
  结构化拒(装配期,带资源披露 ~150-300MB/键);
- 审计:每键独立 web 事件账本(``web-events-<sha8>.db``,指纹
  ``tg-web:<账号键>``,与 bot/telethon 线互不可见,F8 判例)。

依赖方向红线(serve.py 同款):本模块零 ``myssia.pipeline`` 依赖,出口
sink(``push_high_value``/``store_item``)注入;装配工厂
:func:`assemble_web_manager` 是 CLI serve 与桌面 entry 的同门面。
"""

from __future__ import annotations

import asyncio
import logging
from collections import OrderedDict
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Awaitable, Callable, Mapping

from myssia.telegram.serve import (
    TelegramServeHost,
    TelegramSourceBinding,
)
from myssia.telegram.web_line import (
    TelegramWebError,
    default_data_root,
    profile_dir,
    require_playwright,
)

logger = logging.getLogger(__name__)

#: Watcher 事件队列轮询步长(秒;MutationObserver 实时入队,宿主取走节奏)。
WATCH_POLL_INTERVAL_SECONDS = 2.0

#: 哨兵健康探测间隔(秒;登录态 + 观察器面巡检)。
HEALTH_PROBE_INTERVAL_SECONDS = 60.0

#: 多账号并发帽缺省(PRD 多账号决议 ⑤:建议 ≤3,资源 ~150-300MB/键)。
DEFAULT_MAX_ACCOUNTS = 3

#: 哨兵告警类型词表(封闭;UI 账号行翻红消费)。
SENTINEL_LOGGED_OUT = "tg_web_logged_out"
SENTINEL_DOM_STALE = "tg_web_dom_stale"

#: 媒体组跨事件记忆帽(telethon 用户线同值;F13 语义)。
MEDIA_GROUP_MEMORY_CAP = 1000

#: 空闲宿主心跳秒(manager 巡检死任务用;telethon 线同款)。
IDLE_TICK_SECONDS = 1.0

__all__ = [
    "DEFAULT_MAX_ACCOUNTS",
    "HEALTH_PROBE_INTERVAL_SECONDS",
    "IDLE_TICK_SECONDS",
    "MEDIA_GROUP_MEMORY_CAP",
    "SENTINEL_DOM_STALE",
    "SENTINEL_LOGGED_OUT",
    "WATCH_POLL_INTERVAL_SECONDS",
    "TelegramWebAccountHost",
    "TelegramWebManager",
    "TelegramWebSentinel",
    "TelegramWebWatcher",
    "assemble_web_manager",
    "web_source_binding",
]


class _NeverPoller:
    """web 线内嵌 bot 分派器的占位 poller(永不调用,telethon 线同款)."""

    async def poll(self, offset: int) -> list[dict]:  # pragma: no cover - 防御
        raise AssertionError("TG 网页线不得触发 bot 长轮询")


@dataclass
class TelegramWebSentinel:
    """一条哨兵告警(结构化;manager 内存态 + 账本 error 行 + 日志)."""

    type: str  # SENTINEL_LOGGED_OUT / SENTINEL_DOM_STALE
    account: str
    chat: str | None
    detail: str
    created_at: str

    def to_payload(self) -> dict[str, Any]:
        return {
            "type": self.type,
            "account": self.account,
            "chat": self.chat,
            "detail": self.detail,
            "created_at": self.created_at,
        }


def _now_iso() -> str:
    from datetime import datetime, timezone

    return datetime.now(timezone.utc).isoformat()


class TelegramWebWatcher:
    """一个(账号×群)的常驻监听页:MutationObserver → dispatch_once.

    Args:
        page: 已开到目标群的页(账号宿主准备;测试注 fake)。
        account: 账号键(告警/账本归属)。
        binding: 该群的源绑定(chat_id=群标识,source_name/source_url/
            pipeline 与 bot 线同形)。
        ledger: 本键 web 事件账本(装配方按 ``tg-web:<键>`` 指纹分键)。
        push_high_value / store_item: 出口 sink(bot 线装配同源同语义)。
        sleep: 异步 sleep 注入(测试 fake)。
        should_stop: 停止判定(装配方注入)。
    """

    def __init__(
        self,
        *,
        page: Any,
        account: str,
        binding: TelegramSourceBinding,
        ledger: Any,
        push_high_value: Callable[[dict[str, Any]], Awaitable[bool]],
        store_item: Callable[[dict[str, Any]], bool],
        sleep: Callable[[float], Awaitable[None]] = asyncio.sleep,
        should_stop: Callable[[], bool] | None = None,
    ) -> None:
        self._page = page
        self._account = account
        self._binding = binding
        self._sleep = sleep
        self._should_stop = should_stop
        from myssia.telegram.offsets import OffsetStore

        self._dispatcher = TelegramServeHost(
            poller=_NeverPoller(),
            bindings={binding.chat_id: binding},
            offsets=OffsetStore(Path("telegram-web") / "offsets-placeholder.json"),
            ledger=ledger,
            push_high_value=push_high_value,
            store_item=store_item,
            sleep=sleep,
            should_stop=should_stop,
        )
        #: 媒体组跨事件记忆(``chat:grouped_id``;telethon 线同款永久记忆
        #: + FIFO 裁剪 —— DOM 面无相册分组键,本记忆只兜 dispatch_once
        #: 的滚动窗口语义)。
        self._anchored_groups: OrderedDict[str, None] = OrderedDict()
        #: 生命周期观测。
        self.events = 0
        self._last_health_at = 0.0

    def _stopped(self) -> bool:
        return self._should_stop is not None and self._should_stop()

    async def run_forever(self) -> None:
        """主循环:注入观察器 → 轮询取事件 → 同形分派;哨兵异常上抛.

        Raises:
            TelegramWebError: ``tg_web_logged_out`` / ``tg_web_dom_stale``
                (fatal —— 单键失效是凭据态/DOM 态,重试无意义;账号宿主
                收到后停该键全部 Watcher 并告警,design D5 失效隔离)。
        """
        from myssia.telegram.web_dom import (
            CHAT_OPEN_SELECTORS,
            MESSAGE_SELECTORS,
            drain_observer_js,
            install_observer_js,
        )

        installed = await self._page.evaluate(
            install_observer_js(),
            {
                "messageSelectors": list(MESSAGE_SELECTORS),
                "containerSelectors": list(CHAT_OPEN_SELECTORS),
            },
        )
        if not (isinstance(installed, dict) and installed.get("ok")):
            reason = (
                installed.get("reason")
                if isinstance(installed, dict)
                else type(installed).__name__
            )
            raise TelegramWebError(
                f"TG 网页线观察器安装失败 chat={self._binding.chat_id}"
                f" reason={reason}(消息容器选择器失配);跟修:重标定"
                " myssia/telegram/web_dom.py 选择器表",
                reason=SENTINEL_DOM_STALE,
                fatal=True,
            )
        logger.info(
            "TG 网页线 Watcher 启动 account=%s chat=%s source=%s(观察器已注入)",
            self._account,
            self._binding.chat_id,
            self._binding.source_name,
        )
        loop = asyncio.get_event_loop()
        self._last_health_at = loop.time()
        try:
            while not self._stopped():
                await self._drain_once()
                if loop.time() - self._last_health_at >= HEALTH_PROBE_INTERVAL_SECONDS:
                    await self._health_probe()
                    self._last_health_at = loop.time()
                await self._sleep(WATCH_POLL_INTERVAL_SECONDS)
        except asyncio.CancelledError:
            logger.info(
                "TG 网页线 Watcher 收到取消,退出 account=%s chat=%s",
                self._account,
                self._binding.chat_id,
            )
            raise

    async def _drain_once(self) -> None:
        """取走页内事件队列 → 逐 mid 抽取 → 同形 update 批量分派."""
        from myssia.telegram.web_dom import (
            dom_message_to_update,
            drain_observer_js,
            extract_message_js,
        )

        mids = await self._page.evaluate(drain_observer_js())
        if not isinstance(mids, list) or not mids:
            return
        seen: set[str] = set()
        updates: list[dict[str, Any]] = []
        for entry in mids:
            mid = entry.get("mid") if isinstance(entry, dict) else None
            if not isinstance(mid, str) or not mid or mid in seen:
                continue
            seen.add(mid)
            raw = await self._page.evaluate(extract_message_js(), mid)
            update = dom_message_to_update(
                raw if isinstance(raw, dict) else {},
                chat_id=self._binding.chat_id,
            )
            if update is not None:
                updates.append(update)
        if not updates:
            return
        self.events += len(updates)
        anchored = await self._dispatcher.dispatch_once(
            updates, skip_groups=set(self._anchored_groups)
        )
        for key in anchored:
            self._anchored_groups[key] = None
        while len(self._anchored_groups) > MEDIA_GROUP_MEMORY_CAP:
            self._anchored_groups.popitem(last=False)

    async def _health_probe(self) -> None:
        """周期哨兵:登录表单重现 = 登出;会话列表+观察器全失 = DOM 失配."""
        from myssia.telegram.web_dom import (
            CHAT_LIST_SELECTORS,
            LOGGED_OUT_SELECTORS,
        )

        state = await self._page.evaluate(
            """(selectors) => {
                const out = selectors.logged_out.find(
                    (s) => document.querySelector(s) !== null);
                if (out) return {state: 'logged_out'};
                const chat = selectors.chat_list.find(
                    (s) => document.querySelector(s) !== null);
                const observer = Boolean(window.__myssiaTgWebObserver);
                return {state: chat ? 'logged_in' : 'unknown', observer};
            }""",
            {
                "chat_list": list(CHAT_LIST_SELECTORS),
                "logged_out": list(LOGGED_OUT_SELECTORS),
            },
        )
        if not isinstance(state, dict):
            state = {"state": "unknown"}
        if state.get("state") == "logged_out":
            raise TelegramWebError(
                f"TG 网页线账号 {self._account} 登录态丢失(登录表单重现 —— "
                "常见于被 Telegram 侧吊销或账号在别处登出);重登:"
                f"myssia telegram web-login --account {self._account} --force",
                reason=SENTINEL_LOGGED_OUT,
                fatal=True,
            )
        if state.get("state") == "unknown" or not state.get("observer"):
            raise TelegramWebError(
                f"TG 网页线页面健康面失配 account={self._account}"
                f" chat={self._binding.chat_id}(会话列表/观察器全不中);"
                "跟修:重标定 myssia/telegram/web_dom.py 选择器表",
                reason=SENTINEL_DOM_STALE,
                fatal=True,
            )


class TelegramWebAccountHost:
    """一个账号键的常驻宿主:一 context 多 Watcher 页(失效隔离单元).

    骨架(TelethonUserHost 同款):宿主本体 asyncio 协程,由装配方在独立
    线程以 ``asyncio.run`` 拉起(CLI serve / desktop entry 判例)。启动序:
    配置档门(缺 = 结构化留痕,web-login 指引)→ 依赖门 → 无头 context →
    登录态探针(登出 = ``tg_web_logged_out`` 上抛)→ 逐群开页 + 起 Watcher
    → ``gather`` 并跑。单 Watcher 哨兵异常 = 停**该账号**全部 Watcher
    (登录态是账号级面;DOM 失配按当前实现同停 —— 保守取向,告警带全键
    上下文),异常经 :class:`TelegramWebManager` 记哨兵告警,其他键不受累。
    """

    def __init__(
        self,
        *,
        account: str,
        bindings: Mapping[str, TelegramSourceBinding],
        ledger: Any,
        push_high_value: Callable[[dict[str, Any]], Awaitable[bool]],
        store_item: Callable[[dict[str, Any]], bool],
        data_root: str | Path | None = None,
        sleep: Callable[[float], Awaitable[None]] = asyncio.sleep,
        should_stop: Callable[[], bool] | None = None,
        context_launcher: Callable[..., Awaitable[tuple[Any, Any, Any]]] | None = None,
    ) -> None:
        self.account = account
        self._bindings = dict(bindings)
        self._ledger = ledger
        self._push = push_high_value
        self._store = store_item
        self._data_root = Path(data_root) if data_root is not None else default_data_root()
        self._sleep = sleep
        self._should_stop = should_stop
        self._context_launcher = context_launcher
        #: 生命周期观测(CLI 横幅/doctor 消费)。
        self.watchers: list[TelegramWebWatcher] = []

    def _stopped(self) -> bool:
        return self._should_stop is not None and self._should_stop()

    async def _launch(self) -> tuple[Any, Any]:
        """起本键无头 persistent context(注入面 context_launcher = 测试缝)."""
        from myssia.telegram.web_line import launch_persistent_context

        directory = profile_dir(self._data_root, self.account)
        launcher = self._context_launcher or launch_persistent_context
        handle, context, _ = await launcher(
            directory, headless=True, page_timeout_seconds=60.0
        )
        return handle, context

    async def run_forever(self) -> None:
        """主循环:context → 登录探针 → 开群起 Watcher → 并跑至停止.

        Raises:
            TelegramWebError: ``session_missing``(配置档缺)/依赖缺/
                ``tg_web_logged_out``/``tg_web_dom_stale``/开群失败 ——
                全 fatal,manager 收到即记哨兵并隔离本键。
        """
        directory = profile_dir(self._data_root, self.account)
        if not directory.is_dir():
            raise TelegramWebError(
                f"TG 网页线账号 {self.account} 未首登(配置档缺 {directory});"
                f"一次性前置:myssia telegram web-login --account {self.account}"
                "(页面内输手机号+验证码,建议挂小号)",
                reason="session_missing",
                fatal=True,
            )
        try:
            require_playwright()
        except TelegramWebError:
            raise
        from myssia.telegram.web_dom import (
            CHAT_LIST_SELECTORS,
            LOGGED_OUT_SELECTORS,
            chat_url,
        )

        handle, context = await self._launch()
        try:
            page = context.pages[0] if context.pages else await context.new_page()
            await page.goto(chat_url(""), wait_until="domcontentloaded")
            state = await page.evaluate(
                """(selectors) => {
                    const hit = selectors.chat_list.find(
                        (s) => document.querySelector(s) !== null);
                    if (hit) return {state: 'logged_in'};
                    const out = selectors.logged_out.find(
                        (s) => document.querySelector(s) !== null);
                    return {state: out ? 'logged_out' : 'unknown'};
                }""",
                {
                    "chat_list": list(CHAT_LIST_SELECTORS),
                    "logged_out": list(LOGGED_OUT_SELECTORS),
                },
            )
            login_state = (
                state.get("state") if isinstance(state, dict) else "unknown"
            )
            if login_state == "logged_out":
                raise TelegramWebError(
                    f"TG 网页线账号 {self.account} 登录态失效(登出页在);重登:"
                    f"myssia telegram web-login --account {self.account} --force",
                    reason=SENTINEL_LOGGED_OUT,
                    fatal=True,
                )
            if login_state == "unknown":
                raise TelegramWebError(
                    f"TG 网页线账号 {self.account} 页面标志面失配(既无会话列表"
                    "也无登录表单);跟修:重标定 myssia/telegram/web_dom.py 选择器表",
                    reason=SENTINEL_DOM_STALE,
                    fatal=True,
                )
            for chat_id, binding in self._bindings.items():
                await self._open_chat_page(context, chat_id, binding)
            tasks = [
                asyncio.ensure_future(w.run_forever()) for w in self.watchers
            ]
            try:
                while not self._stopped() and any(not t.done() for t in tasks):
                    await self._sleep(IDLE_TICK_SECONDS)
            finally:
                for task in tasks:
                    if not task.done():
                        task.cancel()
                await asyncio.gather(*tasks, return_exceptions=True)
        finally:
            for closer in (context.close, handle.stop):
                try:
                    result = closer()
                    if hasattr(result, "__await__"):
                        await result
                except Exception:  # noqa: BLE001 - 收尾失败不污染主结果
                    logger.warning(
                        "TG 网页线账号宿主收尾失败(忽略)account=%s", self.account
                    )
            from myssia.telegram.web_line import harden_profile_permissions

            harden_profile_permissions(directory)
        logger.info(
            "TG 网页线账号宿主退出 account=%s watchers=%s",
            self.account,
            len(self.watchers),
        )

    async def _open_chat_page(
        self, context: Any, chat_id: str, binding: TelegramSourceBinding
    ) -> None:
        """开一页到目标群并挂 Watcher(开群失败 = 本键 fatal 上抛)."""
        from myssia.telegram.web_dom import chat_url, open_chat_js

        page = await context.new_page()
        await page.goto(chat_url(chat_id), wait_until="domcontentloaded")
        opened = await page.evaluate(
            open_chat_js(),
            {
                "chat": chat_id,
                "chatOpenSelectors": [".bubbles", ".messages-container"],
                "pollStepMs": 250,
            },
        )
        if not (isinstance(opened, dict) and opened.get("ok")):
            reason = (
                opened.get("reason")
                if isinstance(opened, dict)
                else type(opened).__name__
            )
            raise TelegramWebError(
                f"TG 网页线打开群失败 account={self.account} chat={chat_id}"
                f" reason={reason}(未加入该群/DOM 改版面);源"
                f" {binding.source_name} 本键停(其他键不受累)",
                reason=SENTINEL_DOM_STALE,
                fatal=True,
            )
        watcher = TelegramWebWatcher(
            page=page,
            account=self.account,
            binding=binding,
            ledger=self._ledger,
            push_high_value=self._push,
            store_item=self._store,
            sleep=self._sleep,
            should_stop=self._should_stop,
        )
        self.watchers.append(watcher)


@dataclass
class _AccountRuntime:
    """manager 的单键运行态(任务句柄 + 告警面)."""

    host: TelegramWebAccountHost
    task: asyncio.Task | None = None
    alert: TelegramWebSentinel | None = None


class TelegramWebManager:
    """web 线总管:多键并跑 + 失效隔离 + 哨兵告警面(design D5).

    Args:
        hosts: 账号键 → 账号宿主(装配期已过 max_accounts 帽)。
        alert_sink: 哨兵告警的旁路 sink(``Callable[[TelegramWebSentinel],
            None]``;缺省只走内存态+日志+账本 —— 桌面接线可挂 sidecar 流)。
        sleep: 异步 sleep 注入(测试 fake)。
        should_stop: 停止判定(装配方注入线程 Event)。
    """

    def __init__(
        self,
        *,
        hosts: Mapping[str, TelegramWebAccountHost],
        alert_sink: Callable[[TelegramWebSentinel], None] | None = None,
        sleep: Callable[[float], Awaitable[None]] = asyncio.sleep,
        should_stop: Callable[[], bool] | None = None,
    ) -> None:
        self._hosts: dict[str, _AccountRuntime] = {
            account: _AccountRuntime(host=host)
            for account, host in hosts.items()
        }
        self._alert_sink = alert_sink
        self._sleep = sleep
        self._should_stop = should_stop
        #: 观测面(CLI 横幅/doctor/设置卡消费)。
        self.started_at: str | None = None

    # -------------------------------------------------------------- status

    def status(self) -> dict[str, Any]:
        """web 线运行态快照(账号行:运行中/已停/最近告警)."""
        accounts: list[dict[str, Any]] = []
        for account, runtime in sorted(self._hosts.items()):
            task = runtime.task
            running = task is not None and not task.done()
            accounts.append(
                {
                    "account": account,
                    "running": running,
                    "chats": sorted(
                        chat for chat in runtime.host._bindings  # noqa: SLF001 - 观测面
                    ),
                    "alert": runtime.alert.to_payload()
                    if runtime.alert is not None
                    else None,
                }
            )
        return {"line": "tg_web", "started_at": self.started_at, "accounts": accounts}

    # ---------------------------------------------------------------- loop

    async def run_forever(self) -> None:
        """总管循环:全键拉起 → 巡检死键记告警(design D5 失效隔离).

        单键 fatal(登出/DOM 失配/开群失败)= 记哨兵告警 + 停该键,**不
        复活不退出**(「serve 重启全量拉起各键」,重启由人决定)。manager
        自身只在停止位/取消时退出 —— 一键失效绝不带走其他键与 serve。
        """
        self.started_at = _now_iso()
        for account, runtime in self._hosts.items():
            runtime.task = asyncio.ensure_future(self._run_account(account, runtime))
        logger.info(
            "TG 网页线 manager 启动 accounts=%s(多账号失效隔离;帽已过)",
            sorted(self._hosts),
        )
        try:
            while not (
                self._should_stop is not None and self._should_stop()
            ):
                await self._sleep(IDLE_TICK_SECONDS)
        except asyncio.CancelledError:
            logger.info("TG 网页线 manager 收到取消,正在退出")
            raise
        finally:
            for runtime in self._hosts.values():
                if runtime.task is not None and not runtime.task.done():
                    runtime.task.cancel()
            await asyncio.gather(
                *(r.task for r in self._hosts.values() if r.task is not None),
                return_exceptions=True,
            )
        logger.info("TG 网页线 manager 已退出")

    def close(self) -> None:
        """装配面收尾:各键账本连接关闭(失败只留痕;观测面此后不可读)."""
        for runtime in self._hosts.values():
            ledger = getattr(runtime.host, "_ledger", None)
            if ledger is not None:
                try:
                    ledger.close()
                except Exception:  # noqa: BLE001
                    logger.warning(
                        "TG 网页线账本关闭失败(忽略)account=%s",
                        runtime.host.account,
                    )

    async def _run_account(self, account: str, runtime: _AccountRuntime) -> None:
        """单键拉起面:fatal 统一收口为哨兵告警(隔离语义的实现点)."""
        try:
            await runtime.host.run_forever()
        except asyncio.CancelledError:
            raise
        except TelegramWebError as exc:
            # 哨兵词表(tg_web_logged_out/tg_web_dom_stale)直传;配置态
            # reason(session_missing/dependency_missing)同面告警(账号行
            # 翻红 + 修复指引在 detail 里)。
            self._record_alert(
                TelegramWebSentinel(
                    type=exc.reason,
                    account=account,
                    chat=None,
                    detail=str(exc),
                    created_at=_now_iso(),
                )
            )
        except Exception as exc:  # noqa: BLE001 - 未知异常同记告警,不带走向管
            self._record_alert(
                TelegramWebSentinel(
                    type="tg_web_error",
                    account=account,
                    chat=None,
                    detail=f"{type(exc).__name__}: {exc}",
                    created_at=_now_iso(),
                )
            )

    def _record_alert(self, sentinel: TelegramWebSentinel) -> None:
        """哨兵告警三面:内存态 + 日志 + 账本 error 行(+可选旁路 sink)."""
        runtime = self._hosts.get(sentinel.account)
        if runtime is not None:
            runtime.alert = sentinel
        logger.error(
            "TG 网页线哨兵告警 type=%s account=%s chat=%s: %s",
            sentinel.type,
            sentinel.account,
            sentinel.chat,
            sentinel.detail,
        )
        host = runtime.host if runtime is not None else None
        ledger = getattr(host, "_ledger", None) if host is not None else None
        if ledger is not None:
            try:
                ledger.record(
                    update_id=-1,
                    chat_id=sentinel.chat,
                    outcome="error",
                    detail=f"{sentinel.type}: {sentinel.detail}"[:500],
                )
            except Exception:  # noqa: BLE001 - 账本失败不带走告警面
                logger.warning("TG 网页线哨兵账本写入失败(忽略)", exc_info=True)
        if self._alert_sink is not None:
            try:
                self._alert_sink(sentinel)
            except Exception:  # noqa: BLE001
                logger.warning("TG 网页线告警旁路 sink 失败(忽略)", exc_info=True)


def web_source_binding(
    source: Any, backend: Any
) -> tuple[str, str, TelegramSourceBinding]:
    """tg_web 源 → ``(账号键, 群标识, 绑定)``(CLI serve 与桌面 entry 共用).

    过滤键与引擎面同口径(engine_options.telegram + tg_web 并集,
    tg_web 优先);群标识 = ``chat``(用户名或 -100 数字 id)。
    """
    from myssia.engines.fetch_base import FetchError
    from myssia.engines.telegram import filter_config_from_options
    from myssia.telegram.filter import TelegramFilterPipeline

    raw = (source.extra_params.get("engine_options") or {}) if hasattr(source, "extra_params") else {}
    web_options = raw.get("tg_web", {}) if isinstance(raw, dict) else {}
    if not isinstance(web_options, dict):
        web_options = {}
    account = web_options.get("account")
    chat = web_options.get("chat")
    from myssia.telegram.web_line import TelegramWebError, validate_account_key

    if not isinstance(account, str):
        raise FetchError(
            f"源 {source.name} 缺 engine_options.tg_web.account(账号键全称律"
            " telegram-<标识>)",
            error_type="invalid_engine_options",
        )
    try:
        account_key = validate_account_key(account)
    except TelegramWebError as exc:
        raise FetchError(str(exc), error_type="invalid_engine_options") from exc
    if isinstance(chat, bool) or not isinstance(chat, (str, int)):
        raise FetchError(
            f"源 {source.name} 缺 engine_options.tg_web.chat(群用户名或 -100 id)",
            error_type="invalid_engine_options",
        )
    merged: dict[str, Any] = {}
    telegram_options = raw.get("telegram") if isinstance(raw, dict) else None
    if isinstance(telegram_options, dict):
        merged.update(telegram_options)
    merged.update(web_options)
    binding = TelegramSourceBinding(
        chat_id=str(chat).strip(),
        source_name=source.name,
        source_url=source.url,
        pipeline=TelegramFilterPipeline(
            filter_config_from_options(merged), keychain_backend=backend
        ),
    )
    return account_key, binding.chat_id, binding


def assemble_web_manager(
    sources: list[Any],
    *,
    telegram_dir: Path,
    data_root: Path,
    backend: Any,
    store_item: Callable[[dict[str, Any]], bool],
    push_high_value: Callable[[dict[str, Any]], Awaitable[bool]],
    max_accounts: int | None = None,
    should_stop: Callable[[], bool] | None = None,
) -> tuple[TelegramWebManager | None, str | None]:
    """web 线装配工厂(CLI serve 与桌面 entry 同门,W3).

    Returns:
        ``(manager, note)``:manager 为 None 时 note 说明未起原因(结构化
        留痕,不抛 —— web 线是增强线,绝不动摇 bot/telethon 线):无
        tg_web 源(常态)/键超 ``max_accounts`` 帽(结构化拒,带资源披露)。
        账本按键分文件:``web-events-<sha8(tg-web:<键>)>.db``(F8 判例)。
    """
    web_sources = [s for s in sources if s.engine == "tg_web"]
    if not web_sources:
        return None, None
    from myssia.telegram.events import TelegramEventLedger

    cap = max_accounts
    if cap is None:
        cap = DEFAULT_MAX_ACCOUNTS
        for source in web_sources:
            options = (
                source.extra_params.get("engine_options") or {}
            ).get("tg_web", {})
            declared = options.get("max_accounts") if isinstance(options, dict) else None
            if isinstance(declared, int) and not isinstance(declared, bool) and declared > 0:
                cap = max(cap, declared)
    grouped: dict[str, dict[str, TelegramSourceBinding]] = {}
    for source in web_sources:
        account, chat, binding = web_source_binding(source, backend)
        chats = grouped.setdefault(account, {})
        if chat in chats:
            from myssia.engines.fetch_base import FetchError

            raise FetchError(
                f"chat {chat} 被多源占用({chats[chat].source_name} / "
                f"{source.name},账号 {account})",
                error_type="invalid_engine_options",
            )
        chats[chat] = binding
    if len(grouped) > cap:
        accounts_list = ", ".join(sorted(grouped))
        return None, (
            f"TG 网页线未起:账号键数 {len(grouped)} 超 max_accounts 帽 {cap}"
            f"(键:{accounts_list})。资源披露:每键一 Chromium context 约"
            " 150-300MB 内存;同机同出口多账号可被 Telegram 关联(只读监控"
            "风险低,数量克制)。请减键或调 engine_options.tg_web.max_accounts"
        )
    hosts: dict[str, TelegramWebAccountHost] = {}
    for account, bindings in grouped.items():
        ledger = TelegramEventLedger(
            telegram_dir / "web-events.db", bot_token=f"tg-web:{account}"
        )
        hosts[account] = TelegramWebAccountHost(
            account=account,
            bindings=bindings,
            ledger=ledger,
            push_high_value=push_high_value,
            store_item=store_item,
            data_root=data_root,
            should_stop=should_stop,
        )
    manager = TelegramWebManager(hosts=hosts, should_stop=should_stop)
    return manager, None
