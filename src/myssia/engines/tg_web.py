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
          comments_max_threads: 3         # 评论线程档帽(0=off;缺省 3)
          comments_max_replies: 50        # 单线程回复帽 1-100(缺省 50)
          fetch_timeout_seconds: 180      # 预算推导帽输入(与品类 timeouts.fetch 对齐)

评论线程档(V1,10-12-tg-comments-reach):基线窗口读后,对带评论钮的
频道帖**逐帖**展开线程(点开→读 active 页片回泡→关→下一帖;锚用讨论群
真实 peer id,与频道帖独立命名空间),线程回复与基线消息在**两次**
``updates_to_items``(频道标识/讨论群 id 各一调,must_fix2)后合并,同走
``_apply_filter`` 单出口。预算硬约束:总账(基线 + N×线程段 + 过滤储备)
须在每源 fetch 帽内 —— ``comments_budget = min(80, fetch 帽 − 基线实测 −
过滤储备)`` 动态推导,<18s/段自动跳过留痕;每段关闭后状态基验证(hash
回频道 + 频道页片 active),败则 ``open_chat_flow`` 兜底再验,仍败弃余帖
(基线 items 永不丢)。导航时序与 DOM 面见 :mod:`myssia.telegram.web_thread`
/ ``web_dom`` 线程 collect 变体(选择器表 ``2026-10-12.v3``)。

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

import asyncio
import logging
import time
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

# ---------------------------------------------------------------------------
# 评论线程档(10-12-tg-comments-reach V1;预算与帽常量)
# ---------------------------------------------------------------------------

#: 每轮展开的评论线程数帽缺省(0=off;预算不足时引擎自动跳过并留痕)。
DEFAULT_COMMENTS_MAX_THREADS = 3

#: comments_max_threads 域上界(展开段耗时线性涨,20 已远超缺省预算面)。
MAX_COMMENTS_MAX_THREADS = 20

#: 单线程回复读取帽缺省(1-100,与 lookback_limit 同词表)。
DEFAULT_COMMENTS_MAX_REPLIES = 50

#: 引擎侧预算推导帽输入缺省(秒;= 管线每源 asyncio.wait_for 的 fetch 帽
#: 缺省。品类声明 ``timeouts.fetch`` 时须与此键对齐 —— 引擎帽>管线帽会
#: 被外层 wait_for 掐,发现即超时留痕,漂移风险如实注记)。
DEFAULT_FETCH_TIMEOUT_SECONDS = 120.0

#: 评论线程总预算的安全帽(秒;comments_budget = min(本值, fetch 帽−基线
#: 实测−过滤储备),不静态拍 100s 也不放满 fetch 帽)。
COMMENTS_BUDGET_SAFETY_CAP = 80.0

#: 单线程段门槛(秒;总预算或逐帖剩余 < 此值即跳过/断,留痕)。
COMMENT_SEGMENT_THRESHOLD_SECONDS = 18.0

#: 过滤段储备:LLM 已配(端点成对)= 精筛 timeout 60s + 5s 余量;未配 = 5s
#: (粗筛零外呼)。判据同 filter.py 降级面(成对配置才精筛;60 出自
#: ``DEFAULT_LLM_TIMEOUT_SECONDS``)。
FILTER_RESERVE_LLM_SECONDS = 65.0
FILTER_RESERVE_COARSE_SECONDS = 5.0

__all__ = [
    "COMMENT_SEGMENT_THRESHOLD_SECONDS",
    "COMMENTS_BUDGET_SAFETY_CAP",
    "DEFAULT_COMMENTS_MAX_REPLIES",
    "DEFAULT_COMMENTS_MAX_THREADS",
    "DEFAULT_FETCH_TIMEOUT_SECONDS",
    "DEFAULT_LOOKBACK_LIMIT",
    "FILTER_RESERVE_COARSE_SECONDS",
    "FILTER_RESERVE_LLM_SECONDS",
    "LAYER",
    "MAX_COMMENTS_MAX_THREADS",
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
        # 评论线程档三钮(10-12-tg-comments-reach):0=off;预算不足(总账 =
        # fetch 帽 − 基线实测 − 过滤储备)时引擎自动跳过并留痕,不硬烧。
        max_threads = options.get(
            "comments_max_threads", DEFAULT_COMMENTS_MAX_THREADS
        )
        if (
            isinstance(max_threads, bool)
            or not isinstance(max_threads, int)
            or not 0 <= max_threads <= MAX_COMMENTS_MAX_THREADS
        ):
            raise FetchError(
                f"engine_options.tg_web.comments_max_threads 应为 "
                f"0-{MAX_COMMENTS_MAX_THREADS} 整数(每轮展开的评论线程数帽,"
                "0=off;需品类 timeouts.fetch 调大预算),当前为 "
                f"{max_threads!r}",
                error_type="invalid_engine_options",
            )
        max_replies = options.get(
            "comments_max_replies", DEFAULT_COMMENTS_MAX_REPLIES
        )
        if (
            isinstance(max_replies, bool)
            or not isinstance(max_replies, int)
            or not 1 <= max_replies <= MAX_DOM_MESSAGES
        ):
            raise FetchError(
                f"engine_options.tg_web.comments_max_replies 应为 "
                f"1-{MAX_DOM_MESSAGES} 整数(单线程回复读取帽),"
                f"当前为 {max_replies!r}",
                error_type="invalid_engine_options",
            )
        fetch_timeout = options.get(
            "fetch_timeout_seconds", DEFAULT_FETCH_TIMEOUT_SECONDS
        )
        if (
            isinstance(fetch_timeout, bool)
            or not isinstance(fetch_timeout, (int, float))
            or fetch_timeout <= 0
        ):
            raise FetchError(
                "engine_options.tg_web.fetch_timeout_seconds 应为正数秒"
                "(评论线程档预算推导帽输入,须与品类 timeouts.fetch 一致),"
                f"当前为 {fetch_timeout!r}",
                error_type="invalid_engine_options",
            )
        return {
            "account": account_key,
            "chat": str(chat).strip(),
            "lookback_limit": lookback,
            "comments_max_threads": max_threads,
            "comments_max_replies": max_replies,
            "fetch_timeout_seconds": float(fetch_timeout),
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
        baseline_clock = time.monotonic()  # 基线时钟(预算推导面:实测不静态代)
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
            from myssia.telegram.web_line import probe_login_state_settled

            # 稳态探测:/k/ 冷启动先渲染 auth 页再恢复会话(瞬态 logged_out,
            # 真跑实证 2026-10-08),单探误杀 → 宽窗复探,窗尽才定终态。
            state = await probe_login_state_settled(page)
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
            from myssia.telegram.web_line import open_chat_flow

            opened = await open_chat_flow(page, options["chat"])
            if not (isinstance(opened, dict) and opened.get("ok")):
                reason = (
                    opened.get("reason")
                    if isinstance(opened, dict)
                    else type(opened).__name__
                )
                hint = {
                    "dialogs_missing": "侧栏会话列表未渲染(网络受限或 DOM 改版面)",
                    "chat_not_found": "账号未加入该群或群名不符(先在 TG 客户端加入)",
                    "search_box_missing": "搜索框选择器失配(DOM 改版面)",
                    "open_timeout": "点击后消息列未出现(DOM 改版面)",
                }.get(str(reason), "群定位失败")
                error_type = (
                    "tg_web_dom_stale"
                    if str(reason)
                    in ("dialogs_missing", "search_box_missing", "open_timeout")
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
            baseline_elapsed = time.monotonic() - baseline_clock
            # 分拣缝第一调(must_fix2):基线窗口按频道标识 chat_id 分拣。
            items = updates_to_items(
                updates, options["chat"], source_url=self.source.url
            )
            # ── 评论线程扩展段(V1 批量档)── 整体 try 包裹:异常只留痕
            #    不抛,基线 items 永不丢;线程段内逐帖预算/状态基自守。
            thread_updates_count = 0
            try:
                thread_items, thread_updates_count = (
                    await self._expand_comment_threads(
                        page,
                        options,
                        filter_config,
                        baseline_elapsed=baseline_elapsed,
                    )
                )
                items = items + thread_items
            except Exception:  # noqa: BLE001 - 扩展段绝不拖垮基线出仓
                logger.warning(
                    "tg_web 评论线程扩展段异常(留痕不抛,基线 items 照常出仓)"
                    " source=%s",
                    self.source.name,
                    exc_info=True,
                )
            if not items:
                # 零消息两种面:群真安静(DOM 在,消息零)vs 选择器失配
                # (消息列开成功但零节点)。opened.ok 已证消息列容器在,
                # 此处零节点 = 安静群/纯媒体,合法空态。
                logger.info(
                    "tg_web 窗口零消息 source=%s chat=%s(安静群或纯媒体面;"
                    "基线 %s 条 + 线程 0 条)",
                    self.source.name,
                    options["chat"],
                    len(updates),
                )
                return []
            final_items = await self._apply_filter(items, filter_config)
            logger.info(
                "tg_web 窗口取得 source=%s account=%s chat=%s messages=%s"
                " items=%s 线程回复=%s(过滤后出仓 %s)",
                self.source.name,
                options["account"],
                options["chat"],
                len(updates),
                len(items),
                thread_updates_count,
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

    # --------------------------------------------------- comment threads (V1)

    async def _expand_comment_threads(
        self,
        page: Any,
        options: dict[str, Any],
        filter_config: Any,
        *,
        baseline_elapsed: float,
    ) -> tuple[list[dict], int]:
        """评论线程扩展段(批量档;预算推导 + 逐帖展开 + 状态基自守).

        预算硬要求(总账须在管线每源 asyncio.wait_for 的 fetch 帽内):
        ``comments_budget = min(80, fetch 帽 − 基线实测 elapsed − 过滤段储备)``
        (LLM 已配 = 精筛 timeout 60s+5s 余量,未配 = 5s);< 单段门槛 18s
        → 整档跳过留痕;逐帖 remaining = budget − 已耗线程 elapsed,<18s 即
        break;每段 = wait_for(开+读, remaining−CLOSE_RESERVE) + wait_for
        (关, CLOSE_RESERVE),开/读超时也必执行关闭段。

        Returns:
            ``(thread_items, thread_updates_count)`` —— 已铸锚条目(讨论群
            命名空间,must_fix2 第二调分拣)与回泡 update 计数(日志面)。
        """
        from myssia.telegram.web_dom import collect_channel_posts
        from myssia.telegram.web_line import open_chat_flow
        from myssia.telegram.web_thread import (
            CLOSE_RESERVE_SECONDS,
            read_page_hash,
        )

        max_threads = options["comments_max_threads"]
        if max_threads <= 0:
            return [], 0
        fetch_cap = float(options["fetch_timeout_seconds"])
        llm_ready = bool(filter_config.llm_base_url and filter_config.llm_api_key)
        t_filter_reserve = (
            FILTER_RESERVE_LLM_SECONDS if llm_ready else FILTER_RESERVE_COARSE_SECONDS
        )
        comments_budget = min(
            COMMENTS_BUDGET_SAFETY_CAP,
            fetch_cap - baseline_elapsed - t_filter_reserve,
        )
        if comments_budget < COMMENT_SEGMENT_THRESHOLD_SECONDS:
            logger.info(
                "tg_web 评论线程档跳过(预算不足,结构化留痕):budget=%.1fs"
                " < 单段门槛 %.0fs( fetch 帽 %.0fs − 基线实测 %.1fs − 过滤储备"
                " %.0fs );激活路径 = 品类声明 timeouts.fetch 调大帽并与"
                " engine_options.tg_web.fetch_timeout_seconds 对齐 source=%s",
                comments_budget,
                COMMENT_SEGMENT_THRESHOLD_SECONDS,
                fetch_cap,
                baseline_elapsed,
                t_filter_reserve,
                self.source.name,
            )
            return [], 0
        posts = await collect_channel_posts(page)
        if not posts:
            # 前置守卫(must_fix4):active 页片不是频道面(状态漂移)→
            # open_chat_flow 复活一次;不成即弃本轮(防对非 active 页片烧预算)。
            logger.info(
                "tg_web 评论钮重扫零帖(active 页片疑似非频道面),"
                "open_chat_flow 复活一次 source=%s",
                self.source.name,
            )
            reopened = await open_chat_flow(page, options["chat"])
            if not (isinstance(reopened, dict) and reopened.get("ok")):
                logger.warning(
                    "tg_web 评论线程档弃本轮(频道页片复活失败):%s source=%s",
                    reopened,
                    self.source.name,
                )
                return [], 0
            posts = await collect_channel_posts(page)
            if not posts:
                logger.warning(
                    "tg_web 评论线程档弃本轮(复活后重扫仍零帖,DOM 改版面"
                    " tg_web_dom_stale)source=%s",
                    self.source.name,
                )
                return [], 0
        candidates = [p for p in posts if p["comments_count"] > 0]

        def _mid_key(post: dict[str, Any]) -> int:
            try:
                return int(str(post["mid"]))
            except (TypeError, ValueError):
                return 0

        # 展开序:is_unread 优先(服务端新评论信号,v1 无状态)→ 帖 mid 大者
        # (新帖)→ count 降序;计数活变(697→704 实测)只影响优先序不扰去重。
        candidates.sort(
            key=lambda p: (not p["is_unread"], -_mid_key(p), -p["comments_count"])
        )
        selected = candidates[:max_threads]
        if not selected:
            logger.info(
                "tg_web 评论线程档零候选(窗口内帖全无评论钮)source=%s chat=%s",
                self.source.name,
                options["chat"],
            )
            return [], 0
        channel_hash = await read_page_hash(page)
        spent = 0.0
        collected: list[dict] = []
        updates_total = 0
        logger.info(
            "tg_web 评论线程档展开 source=%s chat=%s 候选=%s 选中=%s"
            " 预算=%.1fs",
            self.source.name,
            options["chat"],
            len(candidates),
            len(selected),
            comments_budget,
        )
        for index, post in enumerate(selected):
            remaining = comments_budget - spent
            if remaining < COMMENT_SEGMENT_THRESHOLD_SECONDS:
                logger.info(
                    "tg_web 评论线程档逐帖预算断(剩余 %.1fs < %.0fs,"
                    "弃余 %s 帖;基线 items 照常出仓)source=%s",
                    remaining,
                    COMMENT_SEGMENT_THRESHOLD_SECONDS,
                    len(selected) - index,
                    self.source.name,
                )
                break
            seg_started = time.monotonic()
            seg_updates: list[dict[str, Any]] = []
            seg_stats: dict[str, Any] = {}
            open_read_budget = max(0.1, remaining - CLOSE_RESERVE_SECONDS)
            try:
                seg_updates, seg_stats = await asyncio.wait_for(
                    self._open_and_read_thread(page, options, post),
                    timeout=open_read_budget,
                )
            except asyncio.TimeoutError:
                logger.warning(
                    "tg_web 评论线程段开/读超时(段预算 %.1fs;关闭段照常执行)"
                    " post_mid=%s source=%s",
                    open_read_budget,
                    post["mid"],
                    self.source.name,
                )
            except Exception:  # noqa: BLE001 - 单段异常只留痕,不弃整档
                logger.warning(
                    "tg_web 评论线程段开/读异常(留痕;关闭段照常执行)"
                    " post_mid=%s source=%s",
                    post["mid"],
                    self.source.name,
                    exc_info=True,
                )
            # 关闭段:开/读成败都必执行(线程页片不关会堆积;must_fix4)
            state_ok = await self._close_thread_segment(
                page, options, post, channel_hash
            )
            spent += time.monotonic() - seg_started
            # 半失配哨兵(must_fix5):text 命中率 <80% → tg_web_dom_stale
            # 半失配面留痕(不拦已读到的条目出仓)。
            reply_bubbles = seg_stats.get("reply_bubbles", 0)
            hit_rate = seg_stats.get("text_hit_rate", 1.0)
            if reply_bubbles and hit_rate < 0.8:
                logger.warning(
                    "tg_web_dom_stale 半失配面:线程回泡文本命中率 %.2f"
                    "(%s/%s)<0.80 —— 文本选择器半失配(选择器表 %s;"
                    "跟修 = 重标定 web_dom 线程档选择器)source=%s",
                    hit_rate,
                    seg_stats.get("text_hits", 0),
                    reply_bubbles,
                    SELECTOR_REVISION,
                    self.source.name,
                )
            if seg_updates:
                thread_chat_id = seg_stats.get("thread_chat_id")
                if not isinstance(thread_chat_id, str) or not thread_chat_id:
                    logger.warning(
                        "tg_web 线程读取缺讨论群 peer id(锚命名空间不可铸,"
                        "弃该段 %s 条)post_mid=%s",
                        len(seg_updates),
                        post["mid"],
                    )
                else:
                    # 分拣缝第二调(must_fix2):线程回复按讨论群真实 id 分拣
                    # —— 与第一调(频道标识)是两次独立调用,合并后才进
                    # _apply_filter;锚 = 讨论群独立命名空间。
                    collected.extend(
                        updates_to_items(
                            seg_updates,
                            thread_chat_id,
                            source_url=self.source.url,
                        )
                    )
                    updates_total += len(seg_updates)
            if not state_ok:
                # 状态基中断(非时间基):本轮剩余帖全弃,基线 items 照常出仓
                logger.warning(
                    "tg_web 评论线程档状态基中断(关闭+兜底后频道页片仍未"
                    "复原,弃本轮剩余 %s 帖;基线 items 照常出仓)source=%s",
                    len(selected) - index - 1,
                    self.source.name,
                )
                break
        return collected, updates_total

    async def _open_and_read_thread(
        self, page: Any, options: dict[str, Any], post: dict[str, Any]
    ) -> tuple[list[dict[str, Any]], dict[str, Any]]:
        """单段开+读(引擎 wait_for 面包着;超时由段预算掐)."""
        from myssia.telegram.web_dom import collect_thread_updates
        from myssia.telegram.web_thread import (
            THREAD_READ_SETTLE_SECONDS,
            open_thread_flow,
        )

        opened = await open_thread_flow(page, post["mid"])
        if not (isinstance(opened, dict) and opened.get("ok")):
            reason = (
                opened.get("reason")
                if isinstance(opened, dict)
                else type(opened).__name__
            )
            logger.info(
                "tg_web 评论线程开失败(留痕跳过该帖,关闭段仍执行)"
                " post_mid=%s reason=%s source=%s",
                post["mid"],
                reason,
                self.source.name,
            )
            return [], {}
        # 回复渲染稳态窗(服务端历史拉取后才出回泡,r5 实测)
        await asyncio.sleep(THREAD_READ_SETTLE_SECONDS)
        return await collect_thread_updates(
            page, limit=options["comments_max_replies"]
        )

    async def _close_thread_segment(
        self,
        page: Any,
        options: dict[str, Any],
        post: dict[str, Any],
        channel_hash: str,
    ) -> bool:
        """单段关闭(close-btn 真点→验→败则 open_chat_flow 兜底→再验).

        兜底走独立 wait_for(最坏 ≈ 侧栏 20s + 稳态 4s + 验证 20s + 余量),
        不挤 CLOSE_RESERVE;仍败由调用方按状态基中断弃余。
        """
        from myssia.telegram import web_line
        from myssia.telegram.web_thread import (
            CLOSE_RESERVE_SECONDS,
            close_thread_flow,
            read_thread_state,
        )

        try:
            closed = await asyncio.wait_for(
                close_thread_flow(page, post["mid"], channel_hash),
                timeout=CLOSE_RESERVE_SECONDS,
            )
        except asyncio.TimeoutError:
            closed = {"ok": False, "reason": "close_reserve_timeout"}
        if isinstance(closed, dict) and closed.get("ok"):
            return True
        logger.info(
            "tg_web 评论线程关闭验证未过(%s),open_chat_flow 兜底重开频道"
            " post_mid=%s source=%s",
            closed.get("reason") if isinstance(closed, dict) else closed,
            post["mid"],
            self.source.name,
        )
        fallback_budget = (
            web_line.OPEN_CHAT_DIALOGS_TIMEOUT_SECONDS
            + web_line.OPEN_CHAT_SETTLE_SECONDS
            + web_line.OPEN_CHAT_VERIFY_TIMEOUT_SECONDS
            + 4.0
        )
        try:
            reopened = await asyncio.wait_for(
                web_line.open_chat_flow(page, options["chat"]),
                timeout=fallback_budget,
            )
        except asyncio.TimeoutError:
            reopened = {"ok": False, "reason": "fallback_timeout"}
        if not (isinstance(reopened, dict) and reopened.get("ok")):
            logger.warning(
                "tg_web 评论线程兜底重开频道失败:%s source=%s",
                reopened,
                self.source.name,
            )
            return False
        state = await read_thread_state(page, post["mid"])
        return bool(state.get("chanTabActive")) and str(
            state.get("hash")
        ) == channel_hash

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
