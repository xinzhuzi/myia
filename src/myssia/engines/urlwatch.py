"""urlwatch 变更监控引擎 —— 官网页面快照对比,链外(10-06-ai-news-sources S2).

``engine: urlwatch`` 显式选择才生效(链外注册,credhunter/reddit 先例):
``ENGINE_REGISTRY`` 在册、``AUTO_CHAIN`` 不在,auto 永不路过;显式选择 =
单级链,失败/空态都是源级结构化结果,品类内其余源不受影响(铁律)。

监控语义(蓝本 ``plugins/myssia-urlwatch/adapter.py``,thp/urlwatch BSD 封装):

- 引擎把**源 URL 当监控目标**(单页语义,``pagination`` 配置即结构化拒);
  快照对比由场景件 adapter 完成(子进程 ``uv run --with urlwatch``,缓存落
  ``~/.myia/urlwatch/cache.db`` 跨 run 持久);引擎只消费结构化事件。
- 事件四态 → 管线映射:
  - ``changed`` → 条目(官网有更新;diff 进 content 供 enrich 精评);
  - ``new`` → 上游语义=该目标首次入快照(冷启动基线);``announce_new``
    开(缺省)时产一条「已纳入监控」条目,关时纯建基线零条目
    (ai-news 示范源取关:首跑零打扰,后续只报变更);
  - ``unchanged`` → 合法空态(零变更不是错误,上游已钉):零条目 +
    ``last_skip_reason=watch_unchanged``;
  - ``error`` → 源级结构化失败(目标页抓取坏;不废品类)。
- **去重键适配**:品类级 ``dedup.key: {url}`` 对 watch 目标会「同一页面
  第二次变更被全期吞掉」,故引擎给条目 URL 铸变更指纹锚点
  ``<页面>#watch-<sha1(diff)[:10]>``——不同变更=不同 url=不同去重键,
  点击仍落原页面(锚点不改变落点)。
- 代理边界:子进程直连抓取(场景件零第三方铁律),源 ``proxy`` 非
  ``direct`` 即结构化拒(不做「配了代理池却悄悄直连」的出口错配)。
- **渲染通道**(10-06-ai-news-sources §12):``engine_options.urlwatch.render:
  crawl4ai`` 时监控目标交给渲染 helper(场景件 ``render_crawl4ai.py``,
  crawl4ai 无头渲染取归一化纯文本),job 换上游 ShellJob 形态
  ``{name, command, user_visible_url}``——命令 stdout 即快照对象,快照
  对比/diff/重试语义全在上游原样复用;``user_visible_url`` 锚住事件
  location 与 guid,引擎事件匹配零改动。渲染 helper 以 ``sys.executable``
  运行(crawl4ai 装在哪个环境就由哪个环境跑;uv 临时 urlwatch 环境不背
  浏览器重依赖),后端缺失/件缺失都是结构化失败(``dependency_missing``
  /``render_helper_missing``)。纯客户端渲染页(ai.meta.com/blog 实证,
  静态通道六选择器全零)是本通道的目标面;``render`` 与 ``selector``
  互斥(前者快照是归一化纯文本,CSS 过滤只适用于静态 HTML 快照)。
- robots:目标页抓取不经引擎 HTTP 栈,但礼貌面照走 —— fetch 前经
  ``_ensure_robots_allowed`` 查一次目标 URL(``respect_robots`` 缺省真,
  官网监控属授权目标的礼貌自查,robots 全禁页面如实结构化拒)。

引擎零凭据、零新依赖(adapter 在场景件目录里,缺失/``uv`` 缺失 =
``dependency_missing`` / ``urlwatch_adapter_missing`` 结构化失败,
「装不上不拦核心」铁律)。

Raises:
    FetchError: 源 URL 非 http/https、proxy 非 direct、pagination 配置、
        engine_options 类型错、adapter 缺失、子进程失败/超时、目标页
        error 事件、robots 全禁、渲染通道的 helper 件缺失
        (``render_helper_missing``)、渲染后端未安装
        (``dependency_missing``)或渲染命令段含双引号
        (``invalid_render_command``)。
"""

from __future__ import annotations

import asyncio
import hashlib
import importlib.util
import logging
import os
import shlex
import sys
import types
from pathlib import Path
from typing import Any
from urllib.parse import urlsplit

from myssia.engines.crawl4ai import ensure_playwright_browsers_env
from myssia.engines.fetch_base import BaseEngine, FetchContext, FetchError
from myssia.schema import SourceConfig

logger = logging.getLogger(__name__)

#: 引擎层标签(schema 引擎词表一员;链外源引擎,不进 AUTO_CHAIN)。
LAYER = "PLUGIN_WATCH"

#: 场景插件目录内定位(与 CLI ``--plugins-dir`` / credhunter 引擎同一约定)。
DEFAULT_PLUGINS_DIR = "plugins"

#: 单页子进程 wall-clock 缺省(上游单 job 请求超时 60s,单页 120s 留足重试)。
DEFAULT_TIMEOUT_SECONDS = 120.0

#: content 里 diff 的截断上限(上游事件已截 4000,引擎层再收窄到人读量级)。
DEFAULT_CONTENT_MAX_CHARS = 1500

#: 选择器失效哨兵阈值(发现 C):过滤后快照字节数低于此值即告警——正常
#: 正文区快照为千字节级(anthropic 实证 15K),近零=选择器选空。
TINY_SNAPSHOT_BYTES = 200

#: 渲染通道后端词表(``engine_options.urlwatch.render`` 合法值;词表式收窄,
#: 新后端=改这里+helper 件,不是自由字符串)。
RENDER_BACKENDS = ("crawl4ai",)

#: 渲染 helper 件名(场景件目录内,与 adapter.py 同分发面)。
RENDER_HELPER_FILENAME = "render_crawl4ai.py"

__all__ = [
    "DEFAULT_CONTENT_MAX_CHARS",
    "DEFAULT_PLUGINS_DIR",
    "DEFAULT_TIMEOUT_SECONDS",
    "LAYER",
    "RENDER_BACKENDS",
    "RENDER_HELPER_FILENAME",
    "TINY_SNAPSHOT_BYTES",
    "UrlwatchEngine",
    "build_render_command",
    "import_urlwatch_adapter",
    "render_backend_available",
    "render_helper_path",
]


def import_urlwatch_adapter(
    plugins_dir: str | Path = DEFAULT_PLUGINS_DIR,
) -> types.ModuleType:
    """动态加载 ``<plugins_dir>/myssia-urlwatch/adapter.py``(compile+exec).

    与 credhunter 引擎 / CLI ``_import_plugin_adapter`` 同一手法与同一理由
    (场景件不入核心 import 面)。候选装载路径按序:

    1. ``plugins_dir``(缺省 cwd 相对 ``plugins``,CLI/桌面 home 模式同约定
       ——桌面 sidecar home 模式 cwd 即数据根,``<home>/plugins`` 命中
       已安装件);
    2. ``MYIA_BUNDLED_PLUGINS`` 环境变量(桌面壳 release 态注入的
       Resources/plugins 锚点,tauri resources 恒随包本件 adapter——
       引擎消费免「先在 UI 一键安装」前置);
    3. 源码树布局兜底(包文件 ``src/myssia/engines/`` → 仓库根 ``plugins/``)。

    三处都缺 → 结构化 ``urlwatch_adapter_missing``。
    """
    candidates = [Path(plugins_dir) / "myssia-urlwatch" / "adapter.py"]
    bundled = os.environ.get("MYIA_BUNDLED_PLUGINS")
    if bundled:
        candidates.append(Path(bundled) / "myssia-urlwatch" / "adapter.py")
    here = Path(__file__).resolve()
    if len(here.parents) > 3:  # 源码树布局 src/myssia/engines/urlwatch.py
        candidates.append(
            here.parents[3] / "plugins" / "myssia-urlwatch" / "adapter.py"
        )
    for adapter_file in candidates:
        if adapter_file.is_file():
            module = types.ModuleType("myssia_myssia_urlwatch_adapter")
            module.__file__ = str(adapter_file)
            executable = compile(
                adapter_file.read_text(encoding="utf-8"), str(adapter_file), "exec"
            )
            exec(executable, module.__dict__)  # noqa: S102 - 场景件白名单装载,credhunter 同手法
            return module
    raise FileNotFoundError(
        f"urlwatch 适配器不存在:{candidates[0]}(场景件应随仓库 plugins/ 分发;"
        "桌面端=myssia plugin install plugins/myssia-urlwatch)"
    )


def render_helper_path(plugins_dir: str | Path = DEFAULT_PLUGINS_DIR) -> Path:
    """定位渲染 helper 件(候选装载路径与 :func:`import_urlwatch_adapter` 同序).

    1. ``plugins_dir``(缺省 cwd 相对 ``plugins``,CLI/桌面 home 模式同约定);
    2. ``MYIA_BUNDLED_PLUGINS`` 环境变量(桌面壳 release 态 Resources/plugins);
    3. 源码树布局兜底(包文件 → 仓库根 ``plugins/``)。

    Raises:
        FileNotFoundError: 三处都缺(渲染通道场景件分发不完整)。
    """
    candidates = [
        Path(plugins_dir) / "myssia-urlwatch" / RENDER_HELPER_FILENAME,
    ]
    bundled = os.environ.get("MYIA_BUNDLED_PLUGINS")
    if bundled:
        candidates.append(Path(bundled) / "myssia-urlwatch" / RENDER_HELPER_FILENAME)
    here = Path(__file__).resolve()
    if len(here.parents) > 3:
        candidates.append(
            here.parents[3] / "plugins" / "myssia-urlwatch" / RENDER_HELPER_FILENAME
        )
    for helper_file in candidates:
        if helper_file.is_file():
            return helper_file
    raise FileNotFoundError(
        f"urlwatch 渲染 helper 不存在:{candidates[0]}"
        "(场景件应随仓库 plugins/ 分发,与 adapter.py 同分发面)"
    )


def render_backend_available(backend: str) -> bool:
    """渲染后端可导入性(find_spec 探测,不执行包导入;测试注入口)."""
    try:
        return importlib.util.find_spec(backend) is not None
    except (ImportError, ValueError):  # 残缺发行版/命名空间边缘:按不可用处理
        return False


def build_render_command(python_executable: str, helper: Path | str, url: str) -> str:
    """装配渲染 shell job 命令串:``<python> <helper> <url>``(三段各自引号包裹).

    上游 ShellJob 以 ``shell=True`` 执行命令串,路径/URL 里的空格与壳元字符
    必须引号隔离(POSIX 走 shlex)。win32 走 cmd.exe,其命令分隔符 ``&``/
    ``|``/``<``/``>`` 在双引号内失效——而 ``subprocess.list2cmdline`` 只对
    含空格参数加引号,带查询串的 URL(``?page=2&lang=zh``,无空格)不被
    包裹即被 ``&`` 切断(复核轮实证),故 win32 分支对三段**无条件**双引号
    包裹(% 变量展开属 cmd 既有语义,URL 百分号编码残片不在已定义变量表,
    如实留痕不额外转义)。

    引号包裹的安全前提是**被入口强制**而非口头声明(复核二轮:adapter 的
    URL 校验不拒 ``"``——ord 34 非空白非控制字符,且引擎构命令先于 adapter
    校验):三段任一含双引号即结构化拒 ``invalid_render_command``,不让
    win32 的三段引号被闭合破坏(darwin 的 shlex.quote 本可安全处理,统一
    拒是为了契约单口径)。

    Raises:
        FetchError: 任一段含双引号(``invalid_render_command``)。
    """
    parts = [python_executable, str(helper), url]
    for part in parts:
        if '"' in part:
            raise FetchError(
                f"渲染命令段含双引号(win32 三段引号包裹会被闭合破坏):{part[:80]!r}",
                error_type="invalid_render_command",
            )
    if sys.platform == "win32":
        return " ".join(f'"{part}"' for part in parts)
    return " ".join(shlex.quote(part) for part in parts)


class UrlwatchEngine(BaseEngine):
    """官网页面变更监控源(显式 ``engine: urlwatch``;零凭据).

    单页语义:源 URL 即监控目标;``extract`` 节必是错配(配置即结构化拒,
    reddit 先例),``pagination`` 同理拒。items 出口对齐
    ``Item.from_extracted`` 契约(url/title/content 管线键,其余进 metadata)。
    """

    LAYER = "PLUGIN_WATCH"
    ENGINE_NAME = "urlwatch"
    REQUIRES_EXTRACT = False
    SUPPORTED_EXTRACT_TYPES = ()

    def __init__(self, source: SourceConfig, context: FetchContext) -> None:
        super().__init__(source, context)
        self._adapter_module: types.ModuleType | None = None

    # -------------------------------------------------------------- options

    def _adapter(self) -> Any:
        if self._adapter_module is None:
            try:
                self._adapter_module = import_urlwatch_adapter()
            except FileNotFoundError as exc:
                raise FetchError(
                    str(exc), error_type="urlwatch_adapter_missing"
                ) from exc
        return self._adapter_module

    def _options(self) -> dict[str, Any]:
        """engine_options.urlwatch 的类型校验(错型即结构化拒,不静默吞)."""
        options = self.engine_options()
        timeout = options.get("timeout", DEFAULT_TIMEOUT_SECONDS)
        if (
            isinstance(timeout, bool)
            or not isinstance(timeout, (int, float))
            or timeout <= 0
        ):
            raise FetchError(
                f"engine_options.urlwatch.timeout 应为正数秒,当前为 {timeout!r}",
                error_type="invalid_engine_options",
            )
        announce_new = options.get("announce_new", True)
        if not isinstance(announce_new, bool):
            raise FetchError(
                f"engine_options.urlwatch.announce_new 应为布尔,当前为 {announce_new!r}",
                error_type="invalid_engine_options",
            )
        content_max = options.get("content_max_chars", DEFAULT_CONTENT_MAX_CHARS)
        if (
            isinstance(content_max, bool)
            or not isinstance(content_max, int)
            or not 100 <= content_max <= 4000
        ):
            raise FetchError(
                f"engine_options.urlwatch.content_max_chars 应为 100-4000 整数,"
                f"当前为 {content_max!r}",
                error_type="invalid_engine_options",
            )
        cache_file = options.get("cache_file")
        if cache_file is not None and not isinstance(cache_file, (str, Path)):
            raise FetchError(
                f"engine_options.urlwatch.cache_file 应为路径字符串,当前为 {cache_file!r}",
                error_type="invalid_engine_options",
            )
        label = options.get("label")
        if label is not None and (not isinstance(label, str) or not label.strip()):
            raise FetchError(
                f"engine_options.urlwatch.label 应为非空字符串,当前为 {label!r}",
                error_type="invalid_engine_options",
            )
        selector = options.get("selector")
        if selector is not None and (
            not isinstance(selector, str) or not selector.strip()
        ):
            raise FetchError(
                f"engine_options.urlwatch.selector 应为非空 CSS 选择器字符串,"
                f"当前为 {selector!r}",
                error_type="invalid_engine_options",
            )
        render = options.get("render")
        if render is not None and (
            not isinstance(render, str) or render.strip() not in RENDER_BACKENDS
        ):
            raise FetchError(
                f"engine_options.urlwatch.render 应为渲染后端名"
                f"{list(RENDER_BACKENDS)} 之一,当前为 {render!r}",
                error_type="invalid_engine_options",
            )
        if isinstance(render, str):
            render = render.strip() or None
        if render and selector:
            raise FetchError(
                "engine_options.urlwatch.render 与 selector 互斥:渲染通道的"
                "快照是 helper 归一化后的纯文本(CDN 签名噪声已出局),CSS 选择器"
                "过滤只适用于静态通道的 HTML 快照(纯客户端渲染页选不出正文,"
                "正是 render 通道存在的理由)",
                error_type="invalid_engine_options",
            )
        return {
            "timeout": float(timeout),
            "announce_new": announce_new,
            "content_max_chars": content_max,
            "cache_file": cache_file,
            "label": (label or self.source.name).strip(),
            "selector": selector.strip() if isinstance(selector, str) else None,
            "render": render,
        }

    def _render_helper(self, backend: str) -> Path:
        """渲染通道前置:helper 件在位 + 渲染后端可导入,缺一即结构化拒.

        Raises:
            FetchError: ``render_helper_missing``(场景件分发不完整)或
                ``dependency_missing``(运行环境无渲染后端;装机 python 缺
                crawl4ai 属依赖面,归主人 lock 收编,同 llm extras 先例)。
        """
        try:
            helper = render_helper_path()
        except FileNotFoundError as exc:
            raise FetchError(str(exc), error_type="render_helper_missing") from exc
        if not render_backend_available(backend):
            raise FetchError(
                f"渲染后端 {backend} 未安装(渲染通道由运行 myssia 的解释器"
                f"({sys.executable or 'python3'})执行 helper 取正文):"
                f"pip install myssia[{backend}];装机端待 desktop lock 收编该"
                f"extras 后设置页一键重装",
                error_type="dependency_missing",
            )
        return helper

    # ----------------------------------------------------------------- fetch

    async def _fetch_impl(self) -> list[dict]:
        url = self.source.url
        parsed = urlsplit(url)
        if parsed.scheme not in ("http", "https") or not parsed.netloc:
            raise FetchError(
                f"urlwatch 引擎源 url 应为 http/https 页面地址,当前为 {url!r}",
                error_type="invalid_urlwatch_source_url",
            )
        if self.source.proxy != "direct":
            raise FetchError(
                f"urlwatch 引擎只支持 proxy: direct(子进程直连抓取,场景件零"
                f"第三方铁律;监控目标应直连可达),当前 proxy={self.source.proxy!r}",
                error_type="proxy_unsupported",
            )
        options = self._options()
        # 礼貌自查:目标页抓取虽在子进程,robots 面照查(缺省 respect_robots 真)。
        await self._ensure_robots_allowed(url)

        job: dict[str, Any]
        if options["render"]:
            # 渲染通道(§12):shell 型 job,命令 stdout(渲染 helper 的归一化
            # 纯文本)即快照对象;user_visible_url 锚住事件 location/guid,
            # 事件映射零改动。helper 以 sys.executable 运行——crawl4ai 装在
            # 哪个环境就由哪个环境跑(装机 python 缺后端=结构化
            # dependency_missing,同 llm extras 先例归主人收编)。
            helper = self._render_helper(options["render"])
            # 桌面组件浏览器目录自解析(复审修复,与 crawl4ai 引擎同源):
            # 渲染 helper 子进程经 ShellJob(shell=True)继承本进程 env——
            # 装完组件后常驻 sidecar 无需重启,起子进程前即时对齐
            # PLAYWRIGHT_BROWSERS_PATH(已设原样尊重,目录在场才注)。
            ensure_playwright_browsers_env()
            job = {
                "name": self.source.name,
                "user_visible_url": url,
                "command": build_render_command(
                    sys.executable or "python3", helper, url
                ),
            }
            logger.info(
                "urlwatch 渲染通道就绪 source=%s url=%s backend=%s helper=%s",
                self.source.name,
                url,
                options["render"],
                helper,
            )
        else:
            job = {"name": self.source.name, "url": url}
            if options["selector"]:
                # 内容过滤(框架噪声根治):CSS 选择器圈正文区并剔除 script/
                # style 等噪声节点,快照与 diff 只看正文 HTML 而非整页 ——
                # meta/cohere 实证的全页 diff 全是 React/Next 构建产物漂移
                # (research §8/§9)。上游 css 过滤器实证形状:method 仅 html/
                # xml、exclude 剔除选区内子树(10-06 探针亲验 anthropic 425KB
                # →main 20KB 正文)。注意:纯客户端渲染页(meta 实证)选不出
                # 正文 —— 那是 render 渲染通道的目标面,本过滤不适用。
                job["filter"] = [
                    {
                        "css": {
                            "selector": options["selector"],
                            "exclude": "script, style, noscript, template, svg",
                            "method": "html",
                        }
                    }
                ]
        jobs = [job]
        adapter = self._adapter()
        result: dict | None = None
        last_exc: Exception | None = None
        for attempt in (1, 2):
            try:
                result = await asyncio.to_thread(
                    adapter.run,
                    jobs,
                    cache_file=options["cache_file"],
                    timeout=options["timeout"],
                )
                break
            except Exception as exc:  # noqa: BLE001 - adapter 统一结构化错误码词表
                if getattr(exc, "code", None) == "uv_missing":
                    raise FetchError(
                        f"宿主缺 uv,urlwatch 上游依赖不可用: {exc}",
                        error_type="dependency_missing",
                    ) from exc
                last_exc = exc
                # urlwatch_failed(子进程非零退出)重试一次:品类内源是
                # asyncio.gather 并发抓取(pipeline._fetch_sources),多个
                # urlwatch 源同轮首跑会并发触发 uv 临时环境首装,竞态形态
                # 在案(dry-run 实录:三源并发,两败一成;缓存热后单跑即通)。
                # 4s 错峰后二进;其余错误码(超时/输出坏)重试无意义即抛。
                if getattr(exc, "code", None) == "urlwatch_failed" and attempt == 1:
                    logger.warning(
                        "urlwatch 子进程非零退出(第 1 次),4s 错峰重试一次"
                        " source=%s url=%s: %s",
                        self.source.name,
                        url,
                        exc,
                    )
                    await self.context.sleep(4)
                    continue
                raise self._adapter_failure(url, exc) from exc
        if result is None:
            # 两次 urlwatch_failed(重试路径终态):last_exc 必在
            raise self._adapter_failure(url, last_exc)  # type: ignore[arg-type]
        return self._events_to_items(result, url, options)

    def _adapter_failure(self, url: str, exc: Exception) -> FetchError:
        """adapter 结构化异常 → FetchError;stderr/stdout 尾巴随行(可诊断)."""
        code = getattr(exc, "code", None)
        tail = str(
            getattr(exc, "stderr_tail", "") or getattr(exc, "stdout_tail", "") or ""
        )[:300]
        message = f"urlwatch 监控失败 source={self.source.name} url={url}: {exc}"
        if tail:
            message = f"{message} | 子进程输出尾: {tail}"
        return FetchError(
            message,
            error_type=code if isinstance(code, str) else "urlwatch_failed",
        )

    # --------------------------------------------------------------- mapping

    def _events_to_items(
        self, result: dict[str, Any], url: str, options: dict[str, Any]
    ) -> list[dict]:
        """adapter 结构化结果 → 管线 items(单目标:至多一条有意义事件).

        counts.checked==0 且 deferred>0 = 上游重试未到报错阈值,本轮不判定
        (显式空态);events 里只认本源 URL 的事件(防御性过滤,同名跨源不串)。
        """
        events = [
            event
            for event in result.get("events", [])
            if isinstance(event, dict) and event.get("location") == url
        ]
        if not events:
            counts = result.get("counts", {})
            if counts.get("deferred"):
                self.last_skip_reason = "watch_deferred"
                logger.info(
                    "urlwatch 目标本轮重试未达阈值不判定 source=%s url=%s",
                    self.source.name,
                    url,
                )
            else:
                self.last_skip_reason = "watch_unchanged"
                logger.info(
                    "urlwatch 目标零变更(合法空态)source=%s url=%s counts=%s",
                    self.source.name,
                    url,
                    counts,
                )
            return []
        event = events[0]
        kind = event.get("event")
        label = options["label"]
        if kind == "error":
            raise FetchError(
                f"urlwatch 目标页抓取失败 source={self.source.name} url={url}: "
                f"{event.get('error', '未知错误')}",
                error_type="urlwatch_job_failed",
            )
        if kind == "unchanged":
            self.last_skip_reason = "watch_unchanged"
            self._warn_if_tiny_snapshot(event, url)
            return []
        if kind == "new":
            self._warn_if_tiny_snapshot(event, url)
            if not options["announce_new"]:
                self.last_skip_reason = "watch_baseline_seeded"
                logger.info(
                    "urlwatch 冷启动基线已建(announce_new 关,零条目)source=%s url=%s",
                    self.source.name,
                    url,
                )
                return []
            title = f"{label} 已纳入监控(首次快照)"
            fingerprint = str(event.get("timestamp") or self.source.name)
            diff_text = ""
        else:  # changed
            title = f"{label} 官网有更新"
            diff_text = event.get("diff") or ""
            # 噪声闸(装机真跑两轮实证,10-06-ai-news-sources §8/§9):CDN/
            # 出口轮换使大页快照逐次漂移,上游判 changed 但 diff 渲染为空
            # ——「有更新」标题 + 空 content = 零信息量假阳性,降级为显式
            # skip 不产条目;diff 正常渲染的真变更照常出条目。
            if not diff_text.strip():
                self.last_skip_reason = "watch_noise_empty_diff"
                logger.info(
                    "urlwatch 变更事件 diff 为空(页面漂移噪声,不产条目)"
                    " source=%s url=%s",
                    self.source.name,
                    url,
                )
                return []
            fingerprint = diff_text
        anchor = hashlib.sha1(fingerprint.encode("utf-8", "replace")).hexdigest()[:10]
        item: dict[str, Any] = {
            "url": f"{url}#watch-{anchor}",
            "title": title,
            "watch_event": kind,
            "watch_page": url,
        }
        if diff_text:
            item["content"] = diff_text[: options["content_max_chars"]]
        timestamp = event.get("timestamp")
        if isinstance(timestamp, str) and timestamp:
            item["published"] = timestamp
        logger.info(
            "urlwatch 事件落地 source=%s url=%s event=%s anchor=%s",
            self.source.name,
            url,
            kind,
            anchor,
        )
        return [item]

    # ------------------------------------------------------- shape overrides

    def _warn_if_tiny_snapshot(self, event: dict[str, Any], url: str) -> None:
        """选择器失效哨兵(10-06 发现 C,两跑实证):过滤后快照近零字节而上游
        仍判 unchanged/new——css 选择器选不中正文的结构信号(站点改版即触发,
        此前形态是恒 unchanged 零告警的静默死亡)。出 WARNING 可见,不翻失败。
        """
        snapshot_bytes = event.get("bytes")
        if isinstance(snapshot_bytes, int) and snapshot_bytes < TINY_SNAPSHOT_BYTES:
            logger.warning(
                "urlwatch 快照仅 %s 字节(<%s),选择器疑似失效——目标页可能已"
                "改版,selector 选不中正文;请到配置编辑核对 %s 的 "
                "engine_options.urlwatch.selector source=%s",
                snapshot_bytes,
                TINY_SNAPSHOT_BYTES,
                url,
                self.source.name,
            )

    def _check_pagination_support(self) -> None:
        """单页语义:任何 pagination 配置都结构化拒(不是只拒 scroll).

        监控目标就是一个固定页面;翻页游走会让快照基线漂移(每次比对对象
        都不同),语义上就不是变更监控了。
        """
        if self.source.pagination is not None:
            raise FetchError(
                "urlwatch 引擎是单页监控语义(源 url 即监控目标,快照基线"
                "要求比对对象恒定),不支持 pagination 配置",
                error_type="pagination_unsupported",
            )
