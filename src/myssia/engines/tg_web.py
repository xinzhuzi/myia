"""TG 网页会话引擎(tg_web)—— 自管 Chromium 读群消息窗口(10-08-tg-web-line W2).

``engine: tg_web`` 显式选择才生效(链外注册,reddit/urlwatch/telegram 判例):
``ENGINE_REGISTRY`` 在册、``AUTO_CHAIN`` 不在,auto 永不路过;显式选择 =
单级链,失败/空态都是源级结构化结果,品类内其余源不受影响(铁律)。

通道形态(C 线,PRD 10-08-tg-web-line):零外部凭据(bot token/api_id/
api_hash 全不需要)—— 登录态在 Playwright persistent 配置档
(``<数据根>/telegram-web/<账号键>/``,``myssia telegram web-login`` 的一次
性产物)。批量档(fetch)开该账号配置档的无头 Chromium → 打开目标群 →
读**当前窗口**现存消息(不滚动翻历史;深历史是 TG 客户端滚动加载面)
→ DOM 消息 → Bot API update 同形(``web_dom.dom_message_to_update``)→
**全复用 bot 线消息面**(:func:`engines.telegram.updates_to_items` 群分拣/
媒体面/``#tg-<chat>-<mid>`` 锚全期幂等 + :class:`telegram.filter.
TelegramFilterPipeline` 粗筛/LLM 精筛/高价值合并单条出口)。常驻实时档
是 ``myssia telegram serve`` 的 web 线(telegram/web_host.py,MutationObserver
逐新消息推送),两档同一份消息面语义。

源 YAML 形态(design D4):

.. code-block:: yaml

    - name: telegram-mihomo_party_group   # 源名全称律
      engine: tg_web
      url: "https://web.telegram.org"     # 锚(请求 URL 引擎全权构造)
      engine_options:
        tg_web:
          account: telegram-alt1          # 账号键(归属声明,全称律)
          chat: mihomo_party_group        # 群用户名或 -100 数字 id
          lookback_limit: 50              # 窗口帽 1-100(缺省 50)

凭据零(登录态在档;配置档缺 = ``session_missing`` 显式空态零浏览器,
指引 ``myssia telegram web-login --account <键>``);playwright 缺装 =
结构化 ``dependency_missing``(``myssia[crawl4ai]`` 组件轨,浏览器二进制
复用既有 playwright-browsers,零新下载);登录态失效(登出页在) =
结构化 ``tg_web_logged_out``(重登指引 ``--force``);DOM 选择器失配
(选择器表全不中) = 结构化 ``tg_web_dom_stale``(跟修指引:重标定
web_dom 选择器表)—— 两个哨兵词表与常驻档一致,绝不装死。

robots 论证(telegram 引擎同口径的钉端点豁免):本引擎驱动的是**已
授权用户会话**的自家消息面(web.telegram.org 登录后 UI),不是对目标
站点的爬取;robots.txt 语义对认证第一方应用面无意义。合规面走 PRD
诚实披露(ToS 灰色同 userbot、只读、建议小号、api_id 到手切正统线),
不经 ``_ensure_robots_allowed``;该豁免只属本模块钉死的 web.telegram.org
常量。

其余边界:单轮窗口语义(pagination 配置即结构化拒,urlwatch 判例);
浏览器无头(登录流才 headed);资源面 = 每源每轮一 context(开-读-关),
常驻多 Watcher 共用 context 是 serve 档形态(design D1);多账号 = 每
账号独立配置档独立 context(PRD 多账号决议 ①),批量档源级声明 ``account``
即归属,失效隔离天然(单键空态/失败不涉他键)。

Raises:
    FetchError: engine_options 形状错 / 源 URL 不符契约 / 依赖缺 /
        登录态失效 / DOM 失配 / 群定位失败 / pagination 配置。
"""

from __future__ import annotations

import logging
from typing import Any

from myssia.engines.fetch_base import BaseEngine, FetchContext, FetchError
from myssia.engines.telegram import updates_to_items
from myssia.schema import SourceConfig
from myssia.telegram.filter import (
    TelegramFilterPipeline,
    merge_high_value,
)
from myssia.telegram.web_dom import (
    MAX_DOM_MESSAGES,
    SELECTOR_REVISION,
    chat_url,
    collect_window_updates,
    login_state_probe_js,
    open_chat_js,
)

logger = logging.getLogger(__name__)

#: 引擎名(schema ``EngineName`` 词表一员;链外源引擎,不进 AUTO_CHAIN)。
LAYER = "TG_WEB_SESSION"

#: web.telegram.org 宿主(源 URL 锚契约)。
WEB_HOST = "web.telegram.org"

#: 窗口帽缺省(批量档读当前窗口,50 条常识帽;锚去重兜底重复面)。
DEFAULT_LOOKBACK_LIMIT = 50

#: 群打开与登录检查的页面预算(秒)。
PAGE_BUDGET_SECONDS = 60.0

__all__ = [
    "DEFAULT_LOOKBACK_LIMIT",
    "LAYER",
    "PAGE_BUDGET_SECONDS",
    "WEB_HOST",
    "TelegramWebEngine",
]


class TelegramWebEngine(BaseEngine):
    """TG 网页会话窗口源(显式 ``engine: tg_web``;凭据零,登录态在档).

    items 出口对齐 ``Item.from_extracted`` 契约(经 bot 线
    ``updates_to_items`` 同一实现):url(``#tg-`` 锚)/title(截断)/
    content(全文),观测键进 metadata。过滤面 = bot 线同一份
    (粗筛/LLM 精筛/高价值合并单条,``TelegramFilterPipeline``)。
    """

    LAYER = "TG_WEB_SESSION"
    ENGINE_NAME = "tg_web"
    REQUIRES_EXTRACT = False
    SUPPORTED_EXTRACT_TYPES = ()

    def __init__(
        self,
        source: SourceConfig,
        context: FetchContext,
        *,
        completer: Any | None = None,
    ) -> None:
        super().__init__(source, context)
        #: LLM 精筛完成层注入口(测试 fake;telegram 引擎同款判例)。
        self._completer = completer

    # -------------------------------------------------------------- options

    def _options(self) -> dict[str, Any]:
        """engine_options.tg_web 校验与缺省化(错型即结构化拒)."""
        from myssia.telegram.web_line import validate_account_key

        options = self.engine_options()
        account = options.get("account")
        if not isinstance(account, str) or not account.strip():
            raise FetchError(
                "engine_options.tg_web.account 应为账号键(全称律"
                " telegram-<标识>,如 telegram-alt1;多账号各键各配置档)",
                error_type="invalid_engine_options",
            )
        try:
            account_key = validate_account_key(account)
        except Exception as exc:  # noqa: BLE001 - TelegramWebError 统一翻译
            raise FetchError(str(exc), error_type="invalid_engine_options") from exc
        chat = options.get("chat")
        if isinstance(chat, bool) or not isinstance(chat, (str, int)):
            raise FetchError(
                "engine_options.tg_web.chat 应为群用户名(字符串)或超级群"
                "数字 id(形如 -100xxxxxxxxxx),当前为 "
                f"{chat!r}",
                error_type="invalid_engine_options",
            )
        lookback = options.get("lookback_limit", DEFAULT_LOOKBACK_LIMIT)
        if (
            isinstance(lookback, bool)
            or not isinstance(lookback, int)
            or not 1 <= lookback <= MAX_DOM_MESSAGES
        ):
            raise FetchError(
                f"engine_options.tg_web.lookback_limit 应为 "
                f"1-{MAX_DOM_MESSAGES} 整数(当前窗口读取帽),当前为 {lookback!r}",
                error_type="invalid_engine_options",
            )
        return {
            "account": account_key,
            "chat": str(chat).strip(),
            "lookback_limit": lookback,
        }

    def _filter_options(self):
        """过滤面配置(engine_options 过滤键;bot 线 ``filter_config_from_options``)."""
        from myssia.engines.telegram import filter_config_from_options

        # tg_web 源的过滤键与 bot 线同面(keywords/score_threshold/llm_*),
        # 读 engine_options.telegram 兼容面 + tg_web 键并集(tg_web 优先)。
        merged: dict[str, Any] = {}
        raw = self.source.extra_params.get("engine_options") or {}
        if isinstance(raw, dict):
            telegram_options = raw.get("telegram")
            if isinstance(telegram_options, dict):
                merged.update(telegram_options)
            web_options = raw.get("tg_web")
            if isinstance(web_options, dict):
                merged.update(web_options)
        return filter_config_from_options(merged)

    # ------------------------------------------------------- url & profile

    def _parse_source_url(self) -> None:
        """源 URL 契约校验(零 I/O):``https://web.telegram.org`` 锚形态."""
        from urllib.parse import urlsplit

        parsed = urlsplit(self.source.url)
        host = (parsed.hostname or "").lower()
        if parsed.scheme != "https" or host != WEB_HOST or parsed.path not in ("", "/"):
            raise FetchError(
                f"tg_web 引擎源 url 应为 https://{WEB_HOST} 锚形态"
                f"(路径留空;群配置在 engine_options.tg_web.chat),"
                f"当前为 {self.source.url!r}",
                error_type="invalid_tg_web_source_url",
            )

    def _profile_dir(self, account: str):
        """账号配置档目录(web_line 同源派生)."""
        from myssia.telegram.web_line import default_data_root, profile_dir

        return profile_dir(default_data_root(), account)

    # ----------------------------------------------------------------- fetch

    async def _fetch_impl(self) -> list[dict]:
        from myssia.telegram.web_line import (
            TelegramWebError,
            launch_persistent_context,
            require_playwright,
        )

        self._parse_source_url()
        options = self._options()
        filter_config = self._filter_options()  # 零 I/O 校验先于任何浏览器
        try:
            require_playwright()
        except TelegramWebError as exc:
            raise FetchError(str(exc), error_type="dependency_missing") from exc
        directory = self._profile_dir(options["account"])
        if not directory.is_dir():
            self.last_skip_reason = "session_missing"
            logger.info(
                "tg_web 引擎账号 %s 未首登,显式空态 source=%s(本轮零浏览器;"
                "一次性前置:myssia telegram web-login --account %s,"
                "页面内输手机号+验证码,建议挂小号)",
                options["account"],
                self.source.name,
                options["account"],
            )
            return []
        handle = None
        context = None
        try:
            handle, context, _ = await launch_persistent_context(
                directory,
                headless=True,
                page_timeout_seconds=PAGE_BUDGET_SECONDS,
            )
            page = context.pages[0] if context.pages else await context.new_page()
            await page.goto(chat_url(options["chat"]), wait_until="domcontentloaded")
            from myssia.telegram.web_dom import login_state_probe_js

            login_state = await page.evaluate(login_state_probe_js())
            state = (
                login_state.get("state")
                if isinstance(login_state, dict)
                else "unknown"
            )
            if state == "logged_out":
                raise FetchError(
                    f"tg_web 账号 {options['account']} 登录态失效(登出页在 —— "
                    "常见于配置档被TG 侧吊销或账号在别处登出);重登:"
                    f"myssia telegram web-login --account {options['account']} --force",
                    error_type="tg_web_logged_out",
                )
            if state == "unknown":
                raise FetchError(
                    "tg_web 页面既无会话列表也无登录表单(选择器表失配或网络"
                    "受限);跟修:重标定 myssia/telegram/web_dom.py 选择器表"
                    f"(当前标定 {SELECTOR_REVISION})",
                    error_type="tg_web_dom_stale",
                )
            opened = await page.evaluate(
                open_chat_js(),
                {
                    "chat": options["chat"],
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
                hint = {
                    "chat_not_found": "账号未加入该群或群名不符(先在 TG 客户端加入)",
                    "search_box_missing": "搜索框选择器失配(DOM 改版面)",
                    "open_timeout": "点击后消息列未出现(DOM 改版面)",
                }.get(str(reason), "群定位失败")
                error_type = (
                    "tg_web_dom_stale"
                    if str(reason)
                    in ("search_box_missing", "open_timeout")
                    else "tg_web_chat_not_found"
                )
                raise FetchError(
                    f"tg_web 打开群失败 chat={options['chat']} reason={reason}:{hint}"
                    f"(账号 {options['account']})",
                    error_type=error_type,
                )
            updates = await collect_window_updates(
                page,
                chat_id=options["chat"],
                chat_title=(
                    opened.get("title")
                    if isinstance(opened.get("title"), str)
                    else None
                ),
                limit=options["lookback_limit"],
            )
            if not updates:
                # 零消息两种面:群真安静(DOM 在,消息零)vs 选择器失配
                # (消息列开成功但零节点)。opened.ok 已证消息列容器在,
                # 此处零节点 = 安静群/纯媒体,合法空态。
                logger.info(
                    "tg_web 窗口零消息 source=%s chat=%s(安静群或纯媒体面)",
                    self.source.name,
                    options["chat"],
                )
                return []
            items = updates_to_items(
                updates, options["chat"], source_url=self.source.url
            )
            final_items = await self._apply_filter(items, filter_config)
            logger.info(
                "tg_web 窗口取得 source=%s account=%s chat=%s messages=%s"
                " items=%s (过滤后出仓 %s)",
                self.source.name,
                options["account"],
                options["chat"],
                len(updates),
                len(items),
                len(final_items),
            )
            return final_items
        finally:
            for closer in (
                lambda: context.close() if context is not None else None,
                lambda: handle.stop() if handle is not None else None,
            ):
                try:
                    result = closer()
                    if hasattr(result, "__await__"):
                        await result
                except Exception:  # noqa: BLE001 - 收尾失败不污染主结果
                    logger.warning(
                        "tg_web 引擎浏览器收尾失败(忽略)", exc_info=True
                    )

    async def _apply_filter(self, items: list[dict], filter_config) -> list[dict]:
        """过滤管线挂点(bot 线同一份:粗筛→LLM 精筛→高价值合并单条)."""
        if not items:
            return []
        pipeline = TelegramFilterPipeline(
            filter_config,
            completer=self._completer,
            keychain_backend=self.context.keychain_backend,
        )
        outcome = await pipeline.process(items)
        merged = merge_high_value(
            outcome.high_value, threshold=pipeline.config.score_threshold
        )
        return ([merged] if merged is not None else []) + outcome.normal

    # ------------------------------------------------------- shape overrides

    def _check_pagination_support(self) -> None:
        """单轮窗口语义:任何 pagination 配置都结构化拒(urlwatch 判例)."""
        if self.source.pagination is not None:
            raise FetchError(
                "tg_web 引擎是单轮窗口语义(lookback_limit 即窗口帽,"
                "常驻实时监控走 myssia telegram serve web 线),"
                "不支持 pagination 配置",
                error_type="pagination_unsupported",
            )
