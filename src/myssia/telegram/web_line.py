"""TG 网页会话线(C 线)—— Playwright persistent 配置档登录器(10-08-tg-web-line W1).

零外部凭据(api_id/api_hash/bot token 全不需要)的第三条 Telegram 消息
通道:MYIA 自管 Chromium 打开 ``web.telegram.org``,用户(主人)**一次**
在页面里输手机号+验证码,登录态(cookies/localStorage)落 Playwright
persistent context 配置档 ``<数据根>/telegram-web/<账号键>/``(0700 目录/
内件 0600);之后引擎/常驻 Watcher 无头复用同一配置档读群消息 DOM。

三件套(本模块 = ①登录器;②DOM 面见 :mod:`myssia.telegram.web_dom`;
③常驻宿主见 :mod:`myssia.telegram.web_host`):

1. **配置档与账号键**(:func:`profile_dir` / :func:`list_accounts` /
   :func:`harden_profile_permissions`):账号键 = 用户起的全称标识,规约
   ``telegram-<标识>``(如 ``telegram-alt1``,PRD 多账号决议 ⑦);目录名即
   键,多账号互不相通(cookie/登录态零共享)。权限纪律同 telethon session
   判例:登录态 = 凭据面,目录 0700、内件 0600(best-effort 收紧,Playwright
   内部写文件不受控,登录完成/退出时统一硬化一遍)。
2. **登录流**(:class:`TelegramWebLoginFlow`,``myssia telegram web-login
   --account <键>`` 消费):headed 启动该键配置档 → 开 web.telegram.org →
   用户页面内输手机号+验证码(TG 发手机,2FA 如有也在页面内)→ 引擎轮询
   登录成功标志(左栏会话列表出现)→ 收紧权限 → CLI 退出留档。已有有效
   登录态(标记文件在场)→ 提示复用零浏览器;``--force`` 删档重登。
3. **登录态探针**(:func:`check_logged_in`):无头快查 —— 开配置档 goto
   后短窗内查会话列表选择器,返回 ``(logged_in, note)``;登出态/配置档
   缺如实报。设置页账号列表卡与本线哨兵共用。

浏览器二进制复用 crawl4ai 组件轨(:func:`ensure_playwright_browsers_env`
同源注入 ``PLAYWRIGHT_BROWSERS_PATH``,桌面数据根 ``playwright-browsers/``
在场即用,零新下载);playwright 库本体惰性 import(:func:`require_playwright`),
缺装 = 结构化 ``dependency_missing``(安装命令指 ``myssia[crawl4ai]``
组件轨 —— 该 extras 同时带 playwright 库与浏览器二进制,单装即可跑通)。

诚实披露(PRD 钉死,login 成功回执与设置卡文案同步):
- DOM 改版跟修风险:选择器失配哨兵(``tg_web_dom_stale``)在,不装死;
- ToS 灰色同 userbot:**建议小号**,同机同出口多账号可被 TG 关联(只读
  监控风险低,数量克制,缺省帽 3);
- 登录态 = 配置档文件(0600,非加密,同 telethon session 判例口径);
- api_id 到手切回 Telethon 正统线,本线退役或备份。

凭据纪律(AC5 同源):手机号/验证码/2FA 全在浏览器页面内由主人手输,
本模块**零读取零落日志**(登录流只轮询 DOM 登录标志,不碰输入框)。
"""

from __future__ import annotations

import asyncio
import json
import logging
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Awaitable, Callable

logger = logging.getLogger(__name__)

#: playwright 库(extras ``myssia[crawl4ai]`` 组件轨;缺装 → dependency_missing)。
PLAYWRIGHT_PACKAGE = "playwright"

#: 安装命令(dependency_missing 错误消息附带;组件轨单装即带库+浏览器二进制)。
INSTALL_COMMAND = "pip install 'myssia[crawl4ai]'  # 或 uv add 'myssia[crawl4ai]'(组件轨,含 playwright 库与浏览器二进制)"

#: 数据根下网页线配置档根目录(与 telethon 的 ``telegram/`` 并排,分根不混)。
PROFILE_ROOT_DIR = "telegram-web"

#: 账号键规约(PRD 多账号决议 ⑦:全称律 ``telegram-<标识>``;小写字母数字
#: 起头,允许连字符/下划线,2-64 字符 —— 目录名即键,守目录穿越)。
ACCOUNT_KEY_RE = re.compile(r"^telegram-[a-z0-9][a-z0-9_-]{0,62}$")

#: 登录成功标记文件名(配置档内;内容 = JSON 时间戳,零凭据面)。
LOGIN_MARKER_NAME = "myssia-login.json"

#: web.telegram.org 锚(引擎源 URL 契约与登录流共用)。
WEB_ORIGIN = "https://web.telegram.org"

#: 登录窗轮询帽(秒):手机号+验证码+2FA 的人速窗,超时结构化收(可重跑)。
LOGIN_TIMEOUT_SECONDS = 600.0

#: 登录成功标志轮询步长(秒)。
LOGIN_POLL_INTERVAL_SECONDS = 2.0

#: 无头登录态探针的页面预算(秒;探针只看会话列表在不在,不读消息)。
CHECK_TIMEOUT_SECONDS = 45.0

#: 配置档目录/内件权限(登录态 = 凭据面;telethon session 判例)。
PROFILE_DIR_MODE = 0o700
PROFILE_FILE_MODE = 0o600

__all__ = [
    "ACCOUNT_KEY_RE",
    "CHECK_TIMEOUT_SECONDS",
    "INSTALL_COMMAND",
    "LOGIN_MARKER_NAME",
    "LOGIN_POLL_INTERVAL_SECONDS",
    "LOGIN_TIMEOUT_SECONDS",
    "PLAYWRIGHT_PACKAGE",
    "PROFILE_DIR_MODE",
    "PROFILE_FILE_MODE",
    "PROFILE_ROOT_DIR",
    "TelegramWebError",
    "TelegramWebLoginFlow",
    "WEB_ORIGIN",
    "check_logged_in",
    "default_data_root",
    "harden_profile_permissions",
    "list_accounts",
    "login_marker_path",
    "profile_dir",
    "profile_root",
    "read_login_marker",
    "require_playwright",
    "validate_account_key",
]


class TelegramWebError(RuntimeError):
    """TG 网页线的结构化失败(reason 词表见各构造点).

    Attributes:
        reason: ``invalid_account`` / ``dependency_missing`` /
            ``login_timeout`` / ``login_failed`` / ``profile_unavailable``。
        fatal: True = 配置态/凭据态错误,重试无意义(CLI 退码 1)。
    """

    def __init__(self, message: str, *, reason: str, fatal: bool = False) -> None:
        super().__init__(message)
        self.reason = reason
        self.fatal = fatal


def require_playwright() -> Any:
    """惰性 import playwright;缺装 → 结构化 ``dependency_missing``(组件轨判例).

    Returns:
        ``playwright.async_api`` 模块对象(``async_playwright`` 消费面由此取)。
    """
    try:
        from playwright.async_api import async_playwright
    except ImportError as exc:
        raise TelegramWebError(
            f"TG 网页线依赖 {PLAYWRIGHT_PACKAGE} 未安装:"
            f"请先执行 {INSTALL_COMMAND}(浏览器二进制复用 crawl4ai 组件轨,"
            "已装过 crawl4ai 组件则零新下载;不影响 bot/telethon 线)",
            reason="dependency_missing",
            fatal=True,
        ) from exc
    import playwright.async_api as api

    return api


def validate_account_key(account: str) -> str:
    """账号键校验(全称律 ``telegram-<标识>``;违例结构化拒).

    Raises:
        TelegramWebError: ``invalid_account``(形状不符/目录穿越面)。
    """
    key = str(account or "").strip()
    if not ACCOUNT_KEY_RE.match(key):
        raise TelegramWebError(
            f"账号键应为全称律 telegram-<标识>(小写字母数字起头,如"
            f" telegram-alt1;目录名即键),当前为 {account!r}",
            reason="invalid_account",
            fatal=True,
        )
    return key


def default_data_root() -> Path:
    """引擎/登录流的数据根缺省(``$MYIA_HOME`` 或 cwd;telethon 线与 CLI
    ``_cron_default_db`` 同口径 —— serve 装配的数据根 = ``--db`` 父目录,
    两口径在桌面/沙箱一致)。"""
    import os

    home = os.environ.get("MYIA_HOME")
    return Path(home) if home else Path.cwd()


def profile_root(data_root: str | Path) -> Path:
    """网页线配置档根目录(``<数据根>/telegram-web/``;与 telethon 分根)."""
    return Path(data_root) / PROFILE_ROOT_DIR


def profile_dir(data_root: str | Path, account: str) -> Path:
    """账号配置档目录(``<数据根>/telegram-web/<账号键>/``;目录名即键).

    Raises:
        TelegramWebError: ``invalid_account``(先校验再拼路径,守目录穿越)。
    """
    key = validate_account_key(account)
    return profile_root(data_root) / key


def login_marker_path(directory: str | Path) -> Path:
    """登录成功标记文件路径(配置档内;零凭据面,只有时间戳)。"""
    return Path(directory) / LOGIN_MARKER_NAME


def list_accounts(data_root: str | Path) -> list[str]:
    """列出数据根下已有账号键(目录名即键;排序稳定供 UI 列表).

    宽容面:根目录缺 = 空表(未首登常态);不合键规约的目录(手工放置/
    中间态)如实跳过并留痕,不装死也不误显示。
    """
    root = profile_root(data_root)
    if not root.is_dir():
        return []
    accounts: list[str] = []
    for entry in sorted(root.iterdir()):
        if not entry.is_dir() or not ACCOUNT_KEY_RE.match(entry.name):
            continue
        accounts.append(entry.name)
    return accounts


def read_login_marker(directory: str | Path) -> dict[str, Any] | None:
    """读登录标记(缺/坏 = None;宽容不抛 —— 标记只是复用快捷面)."""
    marker = login_marker_path(directory)
    try:
        payload = json.loads(marker.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None
    return payload if isinstance(payload, dict) else None


def harden_profile_permissions(directory: str | Path) -> None:
    """收紧配置档权限:目录 0700、内件 0600(best-effort,失败只留痕).

    Playwright 在会话期持续写配置档(IndexedDB/Local Storage 等),权限
    收紧是退出路径的一次性硬化 + 登录成功即硬化一遍;不能保证会话中途
    新文件恒 0600 —— 如实注记(配置档根 0700 已挡外读,同 session 判例
    口径的非加密披露)。
    """
    root = Path(directory)
    try:
        if root.is_dir():
            root.chmod(PROFILE_DIR_MODE)
        for path in root.rglob("*"):
            if path.is_dir():
                path.chmod(PROFILE_DIR_MODE)
            elif path.is_file():
                path.chmod(PROFILE_FILE_MODE)
    except OSError as exc:
        logger.warning(
            "TG 网页线配置档权限收紧失败 path=%s: %s", root, exc
        )


async def launch_persistent_context(
    directory: str | Path,
    *,
    headless: bool,
    page_timeout_seconds: float = 60.0,
    playwright_factory: Callable[[], Any] | None = None,
) -> tuple[Any, Any, Any]:
    """启动账号配置档的 persistent Chromium(登录流/引擎/探针共用).

    Returns:
        ``(playwright_handle, context, ensure_env_value)`` —— 调用方负责
        ``await playwright_handle.stop()`` 与 ``await context.close()``
        (本函数不持有资源;测试经 ``playwright_factory`` 注入 fake)。
    """
    from myssia.engines.crawl4ai import ensure_playwright_browsers_env

    ensure_playwright_browsers_env()
    if playwright_factory is not None:
        handle = playwright_factory()
    else:
        api = require_playwright()
        handle = api.async_playwright()
    # ⚠ 返回 handle.start() 的产物(Playwright 实例,带 .stop())而非上下文
    # 管理器本体 —— PlaywrightContextManager 只有 start(),stop 在实例上;
    # 返回错对象会让一切收尾路径 AttributeError(playwright node 进程泄漏,
    # W5 真跑标定在案实证)。
    started = await handle.start()
    context = await started.chromium.launch_persistent_context(
        str(directory),
        headless=headless,
        viewport={"width": 1280, "height": 900},
        args=["--disable-blink-features=AutomationControlled"],
    )
    context.set_default_timeout(int(page_timeout_seconds * 1000))
    return started, context, None


async def _wait_for_login(
    page: Any,
    *,
    timeout_seconds: float,
    poll_interval: float = LOGIN_POLL_INTERVAL_SECONDS,
    sleep: Callable[[float], Awaitable[None]] = asyncio.sleep,
    **_legacy: Any,
) -> str:
    """轮询登录成功标志到会话列表出现;返回命中态.

    探测件 = ``web_dom.login_state_probe_js``(可见性口径,W5 真跑标定);
    登录表单重现/会话列表可见由同一份判据序裁决(登录流/引擎/哨兵共用)。

    Raises:
        TelegramWebError: ``login_timeout``(超时,人速窗内没等到会话列表)。
    """
    from myssia.telegram.web_dom import login_state_probe_js

    deadline = asyncio.get_event_loop().time() + timeout_seconds
    last_state = "unknown"
    while asyncio.get_event_loop().time() < deadline:
        try:
            found = await page.evaluate(login_state_probe_js())
        except Exception:  # noqa: BLE001 - 页面导航间隙的 evaluate 异常按 unknown 重试
            found = {"state": "unknown"}
        state = found.get("state") if isinstance(found, dict) else "unknown"
        if state == "logged_in":
            return state
        last_state = state
        await sleep(poll_interval)
    hint = (
        "页面停在登录表单(手机号/验证码未完成或被刷新)"
        if last_state == "logged_out"
        else "页面未出现会话列表(DOM 改版或网络受限,哨兵面见 web_dom 模块)"
    )
    raise TelegramWebError(
        f"TG 网页线登录等待超时({timeout_seconds:.0f}s):{hint};"
        "重新执行 myssia telegram web-login --account <键>(--force 可清档重登)",
        reason="login_timeout",
        fatal=True,
    )


def _write_login_marker(directory: Path) -> None:
    """落登录成功标记(时间戳;零凭据面)。"""
    marker = login_marker_path(directory)
    try:
        marker.write_text(
            json.dumps(
                {
                    "logged_in_at": datetime.now(timezone.utc).isoformat(),
                    "line": "tg_web",
                },
                ensure_ascii=False,
            ),
            encoding="utf-8",
        )
        marker.chmod(PROFILE_FILE_MODE)
    except OSError as exc:  # 标记写失败不废登录(复用检查退化为探针)
        logger.warning(
            "TG 网页线登录标记写入失败(复用检查将走无头探针) path=%s: %s",
            marker,
            exc,
        )


async def check_logged_in(
    data_root: str | Path,
    account: str,
    *,
    timeout_seconds: float = CHECK_TIMEOUT_SECONDS,
    playwright_factory: Callable[[], Any] | None = None,
) -> tuple[bool, str]:
    """无头快查账号登录态;返回 ``(logged_in, note)``.

    配置档缺 = ``(False, "profile_missing")`` 显式空态(零浏览器);
    配置档在 = 无头开档 goto → 短窗查会话列表 → 在 = 登录态活。探针
    不读消息只看标志;DOM 失配(选择器全不中)如实报 ``dom_stale`` note
    (哨兵同词表),不装死。
    """
    directory = profile_dir(data_root, account)
    if not directory.is_dir():
        return False, "profile_missing"
    handle = None
    context = None
    try:
        handle, context, _ = await launch_persistent_context(
            directory,
            headless=True,
            page_timeout_seconds=timeout_seconds,
            playwright_factory=playwright_factory,
        )
        page = context.pages[0] if context.pages else await context.new_page()
        await page.goto(WEB_ORIGIN, wait_until="domcontentloaded")
        try:
            await _wait_for_login(
                page,
                timeout_seconds=timeout_seconds,
                poll_interval=1.0,
            )
        except TelegramWebError:
            # 超时 = 会话列表未出现:登出页在 = 真登出;全不中 = DOM 失配面。
            return False, "logged_out_or_dom_stale"
        return True, "ok"
    except TelegramWebError:
        raise
    except Exception as exc:  # noqa: BLE001 - 探针异常如实报,不装死
        return False, f"probe_failed:{type(exc).__name__}"
    finally:
        for closer in (
            lambda: context.close() if context is not None else None,
            lambda: handle.stop() if handle is not None else None,
        ):
            try:
                result = closer()
                if hasattr(result, "__await__"):
                    await result
            except Exception:  # noqa: BLE001 - 探针收尾失败不掩盖主结果
                logger.debug("TG 网页线探针收尾失败(忽略)", exc_info=True)
    return False, "unknown"


class TelegramWebLoginFlow:
    """网页线一次性登录流(``myssia telegram web-login``;headed).

    全依赖面注入(``playwright_factory``/``print_fn``/``sleep``/``on_page_opened``)
    —— 测试零交互零网络零真 playwright。流程:

    1. 账号键校验 + 配置档目录就位(0700);
    2. 登录标记在(且未 ``--force``)→ 复用提示退出零浏览器;
       ``--force`` 删档重来(标记与 cookies 一并清);
    3. headed 启动 persistent Chromium → 开 web.telegram.org →
       **用户页面内**输手机号+验证码(+2FA;本流零读取零落日志);
    4. 轮询会话列表出现(LOGIN_TIMEOUT 秒人速窗)→ 落标记 + 权限硬化
       → 成功回执(含披露三条:DOM 跟修哨兵/建议小号/api_id 到手切正统)。

    ``on_page_opened``(10-08-browser-module 案甲):页面取得后、goto 前的
    同步回调(注入缝 = 浏览器模块的窗口管理面:聚焦经 page.bring_to_front);
    缺省 None 零行为差,既有调用方(CLI/引擎/宿主/测试)不受影响。

    Raises:
        TelegramWebError: ``invalid_account``/``dependency_missing``/
            ``login_timeout``/``profile_unavailable``(结构化,CLI 退码 1)。
    """

    def __init__(
        self,
        *,
        print_fn: Callable[[str], None] = print,
        playwright_factory: Callable[[], Any] | None = None,
        sleep: Callable[[float], Awaitable[None]] = asyncio.sleep,
        timeout_seconds: float = LOGIN_TIMEOUT_SECONDS,
        on_page_opened: Callable[[Any], None] | None = None,
    ) -> None:
        self._print = print_fn
        self._playwright_factory = playwright_factory
        self._sleep = sleep
        self._timeout = timeout_seconds
        self._on_page_opened = on_page_opened

    async def run(
        self, data_root: str | Path, account: str, *, force: bool = False
    ) -> Path:
        """执行登录;成功返回配置档目录(已 0700/0600 硬化 + 标记在)."""
        key = validate_account_key(account)
        directory = profile_dir(data_root, key)
        if force and directory.exists():
            import shutil

            shutil.rmtree(directory)
            self._print(f"已删除旧配置档(--force):{directory}")
        directory.mkdir(parents=True, exist_ok=True)
        directory.chmod(PROFILE_DIR_MODE)
        marker = read_login_marker(directory)
        if marker is not None and not force:
            self._print(
                f"账号 {key} 已有登录标记({marker.get('logged_in_at')}),"
                "直接复用;失效重登:myssia telegram web-login "
                f"--account {key} --force"
            )
            return directory
        handle, context, _ = await launch_persistent_context(
            directory,
            headless=False,
            page_timeout_seconds=max(60.0, self._timeout),
            playwright_factory=self._playwright_factory,
        )
        try:
            page = (
                context.pages[0]
                if context.pages
                else await context.new_page()
            )
            if self._on_page_opened is not None:
                # 同步回调(goto 前注入页面句柄;浏览器模块窗口管理面消费)
                self._on_page_opened(page)
            await page.goto(WEB_ORIGIN, wait_until="domcontentloaded")
            self._print(
                f"登录窗口已打开({WEB_ORIGIN};账号 {key})。\n"
                "请在页面里输入手机号 → 验证码(TG 发手机 App 内信或短信;"
                "如有两步验证再输密码)。本窗全程不读你的输入,只等会话列表出现;"
                f"{self._timeout:.0f} 秒内未完成将超时退出(可随时重跑)。"
            )
            await _wait_for_login(
                page,
                timeout_seconds=self._timeout,
                sleep=self._sleep,
            )
        finally:
            for closer in (context.close, handle.stop):
                try:
                    result = closer()
                    if hasattr(result, "__await__"):
                        await result
                except Exception:  # noqa: BLE001 - 收尾失败不污染主结果
                    logger.warning(
                        "TG 网页线登录窗收尾失败(忽略;登录态已落配置档)",
                        exc_info=True,
                    )
        harden_profile_permissions(directory)
        if not directory.is_dir():  # pragma: no cover - 异型删除面防御
            raise TelegramWebError(
                f"登录完成但配置档目录消失(预期 {directory})",
                reason="profile_unavailable",
                fatal=True,
            )
        _write_login_marker(directory)
        self._print(
            f"TG 网页线登录完成,登录态已落配置档(0700/0600):{directory}\n"
            "下一步:myssia telegram serve(web 线常驻读群;bot/telethon/web "
            "三线共用过滤出口),或品类源 engine: tg_web 批量采集。\n"
            "披露:①DOM 改版跟修风险 —— 哨兵 tg_web_dom_stale 在,失配即结构化"
            "告警不装死;②ToS 灰色同 userbot,建议专用小号(同机同出口多账号"
            "可被关联,只读监控风险低,数量克制);③api_id 到手建议切回 "
            "Telethon 正统线,本线退役或备份;④登录态=配置档文件(0600,非加密)。"
        )
        return directory
