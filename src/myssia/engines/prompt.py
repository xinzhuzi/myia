"""prompt 任务引擎 —— 一句话监控:抓正文 → 一轮 LLM → 摘要条目,链外.

``engine: prompt`` 显式选择才生效(链外注册,urlwatch/reddit 先例):
``ENGINE_REGISTRY`` 在册、``AUTO_CHAIN`` 不在,auto 永不路过;显式选择 =
单级链,失败/空态都是源级结构化结果,品类内其余源不受影响(铁律)。

语义(Hermes ``hermes chat -Q`` cron job 的最小等价物,蓝本
``.trellis/tasks/10-06-hermes-align/research.md`` §2/§3 批次 3):一个源 =
一个自然语言监控任务 —— ``engine_options.prompt.instructions`` 是任务
指令,``urls`` 是监控目标清单;引擎对每个 URL 走既有礼貌面(robots +
per-host 限速 + 重试退避,全部复用 :class:`BaseEngine`)抓页面,正文抽取
双通路 —— HTML 页走 trafilatura(extras ``myssia[trafilatura]``),XML
feed(``/rss.xml`` 等官网发布通道)走 feedparser 核心依赖 —— 把全部正文
喂**一轮** OpenAI 兼容 LLM(enrich 同款
:class:`~myssia.enrich.client.OpenAICompatClient`,凭据同 enrich 契约:
``env:``/``keychain:`` 引用,明文拒),LLM 的回答(markdown)直接作为
条目 ``content`` 进 push —— 无选择器工程,一句话定义监控。

配置形状(``engine_options.prompt``):

- ``instructions``(必填):任务指令,如「找出新发布/重大更新,中文摘要」;
- ``urls``(可选):监控 URL 清单(缺省 = ``[源 url]``;上限
  :data:`MAX_URLS_PER_SOURCE`);
- ``title``(可选):条目标题(缺省 = 源名);
- ``model``(可选):LLM 模型名(缺省 = schema :data:`DEFAULT_ENRICH_MODEL`);
- ``base_url`` / ``api_key``(必填):OpenAI 兼容端点凭据引用
  (enrich 节同款语法;明文/缺失 = 结构化拒);
- ``max_chars_per_url``(可选):每 URL 正文截断(缺省 6000,100-40000);
- ``timeout``(可选):LLM 单轮超时秒(缺省 180)。

completion 输出上限钉 :data:`DEFAULT_MAX_OUTPUT_TOKENS`(4096),刻意不设
YAML 键 —— ``max_output_tokens`` 键名会被 schema 的凭据子串扫描
(:func:`myssia.schema.is_credential_key`,``token`` 子串)当成疑似凭据键
要求 ``env:``/``keychain:`` 引用形态,数值配不进去;日报量级 4096 足够。

去重键适配(urlwatch 判例):品类级 ``dedup.key: {url}`` 会把「明天的日报」
全期吞掉,引擎给条目 URL 铸**日期锚点** ``<源url>#prompt-<YYYYMMDD>``
(本地日期,日报语义)—— 每天一个新 URL = 新去重键,同日重跑幂等去重,
点击仍落源页面(锚点不改变落点)。

失败模型(全部结构化 :class:`FetchError`,源级隔离,绝不炸品类/调度):

- ``invalid_engine_options``   配置形状错(instructions 缺/urls 坏/数值越界)
- ``credential_invalid``       base_url/api_key 缺失或非引用(明文拒载)
- ``credential_unresolved``    引用解析失败(env 缺/钥匙串未写)
- ``dependency_missing``       trafilatura / openai extras 未装(带安装命令)
- ``prompt_fetch_failed``      **全部** URL 抓取失败(部分失败降级继续,
  摘要标注哪些 URL 没看着)
- ``prompt_llm_failed``        LLM 端点失败/超时/空输出

代理:走引擎共享 HTTP 栈(``_send_with_retry`` 骑 ``_active_client``),
``direct`` / ``pool:<名称>`` 语义原样(pool 挂载/熔断由 BaseEngine 统一处理),
不限 direct。robots:每个目标 URL 逐个 ``_ensure_robots_allowed``
(``respect_robots`` 缺省真;官网监控属授权目标的礼貌自查)。

Raises:
    FetchError: 见上表;``pagination`` 配置结构化拒(单轮任务语义,
    翻页游走会让「任务」的对象漂移)。
"""

from __future__ import annotations

import asyncio
import json
import logging
from datetime import datetime
from typing import Any, Sequence
from urllib.parse import urlsplit

import httpx

from myssia.engines.fetch_base import (
    BaseEngine,
    FetchContext,
    FetchError,
    decode_response,
)
from myssia.enrich.client import INSTALL_COMMAND, CompletionResult, OpenAICompatClient
from myssia.enrich.errors import EnrichConfigError
from myssia.schema import (
    DEFAULT_ENRICH_MODEL,
    CredentialResolveError,
    SourceConfig,
    parse_secret_value,
    resolve_credential,
)

logger = logging.getLogger(__name__)

#: 引擎层标签(schema 引擎词表一员;链外源引擎,不进 AUTO_CHAIN)。
LAYER = "PROMPT_TASK"

#: 单源监控 URL 上限(一轮 LLM 的正文预算护栏;更多目标拆多源/多品类)。
MAX_URLS_PER_SOURCE = 8

#: 每 URL 正文进 prompt 的截断上限缺省(字符;token 成本护栏的一部分)。
DEFAULT_MAX_CHARS_PER_URL = 6000

#: LLM 单轮完成超时缺省(秒;长于 enrich 缺省 60 —— 摘要任务输出长)。
DEFAULT_TIMEOUT_SECONDS = 180.0

#: completion 输出上限缺省(token;日报 markdown 量级)。
DEFAULT_MAX_OUTPUT_TOKENS = 4096

#: 条目侧 metadata 里 instructions 的截断(档案/模板可见性,防 YAML 巨文)。
INSTRUCTIONS_SNIPPET_CHARS = 300

#: 固定 system 指令:任务人格与输出形态(用户 instructions 只描述任务本身)。
SYSTEM_PROMPT = (
    "你是 MYIA 的监控摘要助手。根据提供的网页正文完成用户的监控任务,"
    "直接输出 markdown 摘要(除非任务另有要求,用中文),不要寒暄、"
    "不要复述任务、不要输出与摘要无关的元信息。"
)

#: 抓取失败 URL 在 prompt 里的标注(让 LLM 知道哪些目标本轮没看着)。
_FAILED_URL_NOTE = "(本轮抓取失败,无正文)"

#: XML feed 通路取的条目上限(条目标题+摘要拼文本,有界)。
FEED_MAX_ENTRIES = 40

#: feed 条目摘要截断(字符;feed summary 常是整段 HTML 转文本,防膨胀)。
FEED_SUMMARY_CHARS = 400

__all__ = [
    "DEFAULT_MAX_CHARS_PER_URL",
    "DEFAULT_MAX_OUTPUT_TOKENS",
    "DEFAULT_TIMEOUT_SECONDS",
    "FEED_MAX_ENTRIES",
    "FEED_SUMMARY_CHARS",
    "INSTRUCTIONS_SNIPPET_CHARS",
    "LAYER",
    "MAX_URLS_PER_SOURCE",
    "SYSTEM_PROMPT",
    "PromptEngine",
    "load_trafilatura",
]


def load_trafilatura() -> Any:
    """惰性 import trafilatura(extras 可选依赖,不进核心;static_html 同款)。

    缺装返回 None(调用方结构化 ``dependency_missing``,带安装命令)。
    """
    try:
        import trafilatura
    except ImportError:
        return None
    return trafilatura


def _feed_text(html: str) -> str | None:
    """XML feed 正文通路:feedparser 条目(标题+摘要截断)拼文本.

    feedparser 是 :mod:`myssia.engines.fetch_base` 的既有核心依赖
    (``extract_rss`` 同源),bozo 容错同款 —— 坏 feed 不抛,能活几条算
    几条,空条目返回 None(调用方按该目标失败降级)。
    """
    import feedparser

    parsed = feedparser.parse(html)
    if parsed.bozo:
        logger.warning(
            "prompt 目标 feed 解析带 bozo(容错继续,entries=%s): %s",
            len(parsed.entries),
            parsed.get("bozo_exception", ""),
        )
    lines: list[str] = []
    for entry in parsed.entries[:FEED_MAX_ENTRIES]:
        title = (getattr(entry, "title", None) or "").strip()
        summary = (getattr(entry, "summary", None) or "").strip()
        line = f"- {title}" if title else "- (无标题条目)"
        if summary:
            line = f"{line}:{summary[:FEED_SUMMARY_CHARS]}"
        lines.append(line)
    return "\n".join(lines) if lines else None


class PromptEngine(BaseEngine):
    """自然语言监控任务源(显式 ``engine: prompt``;一轮 LLM 产摘要条目).

    items 出口对齐 ``Item.from_extracted`` 契约:url/title/content 管线键
    (content = LLM markdown 全文,入 items 表档案),``prompt_summary``
    (同一 markdown)与其余观测键进 metadata —— push 模板经 item_view 的
    metadata 合并直接可渲染(``{{ item.prompt_summary }}``),零 push 层改动。
    """

    LAYER = "PROMPT_TASK"
    ENGINE_NAME = "prompt"
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
        #: LLM 完成层注入口(测试 fake;缺省一轮一建 :class:`OpenAICompatClient`,
        #: 其 openai 惰性 import 语义见 enrich.client)。签名同
        #: ``OpenAICompatClient.complete(model=…, system=…, user=…)``。
        self._completer = completer

    # -------------------------------------------------------------- options

    def _options(self) -> dict[str, Any]:
        """engine_options.prompt 校验与缺省化(错型即结构化拒,不静默吞)."""
        options = self.engine_options()
        instructions = options.get("instructions")
        if not isinstance(instructions, str) or not instructions.strip():
            raise FetchError(
                f"engine_options.prompt.instructions 应为非空字符串(任务指令,"
                f"如「找出新发布/重大更新,中文摘要」),当前为 {instructions!r}",
                error_type="invalid_engine_options",
            )
        urls_option = options.get("urls")
        if urls_option is None:
            urls: list[str] = [self.source.url]
        elif isinstance(urls_option, (list, tuple)) and urls_option:
            urls = []
            for item in urls_option:
                if not isinstance(item, str) or not item.strip():
                    raise FetchError(
                        f"engine_options.prompt.urls 元素应为 URL 字符串,"
                        f"当前为 {item!r}",
                        error_type="invalid_engine_options",
                    )
                urls.append(item.strip())
        else:
            raise FetchError(
                f"engine_options.prompt.urls 应为非空 URL 列表(缺省 = [源 url]),"
                f"当前为 {urls_option!r}",
                error_type="invalid_engine_options",
            )
        if len(urls) > MAX_URLS_PER_SOURCE:
            raise FetchError(
                f"单源最多 {MAX_URLS_PER_SOURCE} 个监控 URL(当前 {len(urls)}),"
                "更多目标请拆多源(每源一轮独立摘要)",
                error_type="invalid_engine_options",
            )
        for url in urls:
            parsed = urlsplit(url)
            if parsed.scheme not in ("http", "https") or not parsed.netloc:
                raise FetchError(
                    f"engine_options.prompt.urls 元素应为 http/https 地址,"
                    f"当前为 {url!r}",
                    error_type="invalid_engine_options",
                )
        title = options.get("title")
        if title is not None and (not isinstance(title, str) or not title.strip()):
            raise FetchError(
                f"engine_options.prompt.title 应为非空字符串,当前为 {title!r}",
                error_type="invalid_engine_options",
            )
        model = options.get("model", DEFAULT_ENRICH_MODEL)
        if not isinstance(model, str) or not model.strip():
            raise FetchError(
                f"engine_options.prompt.model 应为非空模型名,当前为 {model!r}",
                error_type="invalid_engine_options",
            )
        max_chars = options.get("max_chars_per_url", DEFAULT_MAX_CHARS_PER_URL)
        if (
            isinstance(max_chars, bool)
            or not isinstance(max_chars, int)
            or not 100 <= max_chars <= 40000
        ):
            raise FetchError(
                f"engine_options.prompt.max_chars_per_url 应为 100-40000 整数,"
                f"当前为 {max_chars!r}",
                error_type="invalid_engine_options",
            )
        max_output = DEFAULT_MAX_OUTPUT_TOKENS
        timeout = options.get("timeout", DEFAULT_TIMEOUT_SECONDS)
        if (
            isinstance(timeout, bool)
            or not isinstance(timeout, (int, float))
            or timeout <= 0
        ):
            raise FetchError(
                f"engine_options.prompt.timeout 应为正数秒,当前为 {timeout!r}",
                error_type="invalid_engine_options",
            )
        return {
            "instructions": instructions.strip(),
            "urls": urls,
            "title": (title or self.source.name).strip(),
            "model": model.strip(),
            "base_url": self._require_ref("base_url", options.get("base_url")),
            "api_key": self._require_ref("api_key", options.get("api_key")),
            "max_chars_per_url": max_chars,
            "max_output_tokens": max_output,
            "timeout": float(timeout),
        }

    @staticmethod
    def _require_ref(field: str, value: Any) -> str:
        """LLM 端点凭据引用校验(enrich 契约:纯 ``env:``/``keychain:``,明文拒).

        Raises:
            FetchError: ``credential_invalid``(缺失/非字符串/非引用形态)。
        """
        if not isinstance(value, str) or not value.strip():
            raise FetchError(
                f"engine_options.prompt.{field} 必须配置为 env:/keychain: 凭据引用"
                "(prompt 引擎与 enrich 节同一契约:MYIA 无内置端点、无默认 key;"
                "如 keychain:myia/llm/base_url)",
                error_type="credential_invalid",
            )
        try:
            parse_secret_value(value, label=f"engine_options.prompt.{field}")
        except Exception as exc:
            raise FetchError(
                f"engine_options.prompt.{field} 必须是纯 env:/keychain: 凭据引用"
                f"(明文拒绝):{exc}",
                error_type="credential_invalid",
            ) from exc
        return value.strip()

    def _resolve_credentials(self, options: dict[str, Any]) -> tuple[str, str]:
        """解析端点引用为具体 ``(base_url, api_key)``(值不落日志).

        Raises:
            FetchError: ``credential_unresolved`` / ``invalid_base_url``
                (resolve_credential / http(s) 校验的结构化包装)。
        """
        try:
            base_url = resolve_credential(
                options["base_url"], backend=self.context.keychain_backend
            )
            api_key = resolve_credential(
                options["api_key"], backend=self.context.keychain_backend
            )
        except CredentialResolveError as exc:
            raise FetchError(
                f"prompt 引擎 LLM 端点凭据引用解析失败"
                f"({options['base_url']} / {options['api_key']}): {exc}",
                error_type="credential_unresolved",
            ) from exc
        if not base_url.startswith(("http://", "https://")):
            raise FetchError(
                f"engine_options.prompt.base_url 解析结果不是 http(s) 地址"
                f"(当前以 {base_url[:8]!r} 开头)",
                error_type="invalid_base_url",
            )
        return base_url, api_key

    # ----------------------------------------------------------------- fetch

    async def _fetch_impl(self) -> list[dict]:
        options = self._options()
        base_url, api_key = self._resolve_credentials(options)
        trafilatura = load_trafilatura()
        if trafilatura is None:
            raise FetchError(
                "trafilatura 未安装(prompt 引擎以它抽正文;extras 可选依赖,"
                "不进核心):pip install 'myssia[trafilatura]' 或 uv add",
                error_type="dependency_missing",
            )

        # 逐 URL 抓正文:单目标失败记录在案继续(部分降级),全灭才拒。
        documents: list[tuple[str, str]] = []
        failures: list[str] = []
        for url in options["urls"]:
            text = await self._fetch_page_text(url, trafilatura)
            if text is None:
                failures.append(url)
                logger.warning(
                    "prompt 任务目标抓取失败(降级继续)source=%s url=%s",
                    self.source.name,
                    url,
                )
            else:
                documents.append((url, text))
        if not documents:
            raise FetchError(
                f"prompt 任务全部 {len(options['urls'])} 个监控 URL 抓取失败"
                f" source={self.source.name}(逐个失败原因见上文日志;"
                f"目标清单: {', '.join(options['urls'])})",
                error_type="prompt_fetch_failed",
            )

        markdown = await self._run_llm(
            options, (base_url, api_key), documents, failures
        )
        return [self._build_item(options, markdown, len(documents), len(failures))]

    async def _fetch_page_text(self, url: str, trafilatura: Any) -> str | None:
        """一个监控目标的正文:robots + 限速 + 重试抓取 → 正文抽取.

        两条抽取通路(目标「官网 URL」常是 RSS 发布通道,openai 官网 HTML
        对非浏览器流量 403 而 ``/news/rss.xml`` 放行 —— 仓库 ai-news 对其
        的既有判例同款):

        - 内容是 XML feed(``<?xml``/``<rss``/``<feed`` 开头)→ feedparser
          (:mod:`myssia.engines.fetch_base` 同款核心依赖)取条目标题+摘要
          拼文本(前 :data:`FEED_MAX_ENTRIES` 条);
        - 其余 → trafilatura 抽正文(static_html 兜底同款钉版 API)。

        抓取/抽取/正文量任一失败返回 None(调用方降级);robots 禁止直接
        抛 :class:`RobotsDisallowedError`(礼貌红线,不降级绕过)。HTTP
        状态/网络失败经 ``_send_with_retry`` 重试耗尽后在这里降级为单目标
        失败(:class:`httpx.HTTPError` 家族;:class:`FetchError` 家族
        robots/proxy 结构化错误照旧冒泡)。
        """
        await self._ensure_robots_allowed(url)
        await self._acquire_rate_limit(url)
        try:
            response = await self._send_with_retry("GET", url)
        except httpx.HTTPError:
            return None
        html = decode_response(response)
        head = html.lstrip()[:200]
        if head.startswith("<?xml") or "<rss" in head or "<feed" in head:
            return _feed_text(html)
        try:
            raw = trafilatura.extract(
                html, url=url, output_format="json", with_metadata=True
            )
        except Exception as exc:  # noqa: BLE001 - 启发式崩溃按该目标失败处理
            logger.warning("trafilatura 抽取异常 url=%s: %s", url, exc)
            return None
        if not raw:
            return None
        try:
            doc = json.loads(raw)
        except (TypeError, ValueError):
            return None
        if not isinstance(doc, dict):
            return None
        text = (doc.get("text") or doc.get("raw_text") or "").strip()
        return text or None

    async def _run_llm(
        self,
        options: dict[str, Any],
        endpoint: tuple[str, str],
        documents: Sequence[tuple[str, str]],
        failures: Sequence[str],
    ) -> str:
        """一轮 LLM:instructions + 全部正文 → markdown 摘要.

        Raises:
            FetchError: ``dependency_missing``(openai extras)/
                ``prompt_llm_failed``(端点失败/超时/空输出)。
        """
        sections = [f"# 监控任务\n\n{options['instructions']}"]
        for url, text in documents:
            clipped = text[: options["max_chars_per_url"]]
            note = (
                f"(正文超长,已截断至 {options['max_chars_per_url']} 字符)"
                if len(text) > options["max_chars_per_url"]
                else ""
            )
            sections.append(f"## 目标页面 {url}{note}\n\n{clipped}")
        for url in failures:
            sections.append(f"## 目标页面 {url}\n\n{_FAILED_URL_NOTE}")
        user_message = "\n\n".join(sections)

        own_client: OpenAICompatClient | None = None
        if self._completer is not None:
            completer = self._completer
        else:
            own_client = OpenAICompatClient(
                endpoint[0],
                endpoint[1],
                timeout_seconds=options["timeout"],
                max_output_tokens=options["max_output_tokens"],
            )
            completer = own_client.complete
            try:
                own_client._ensure_async_client()  # noqa: SLF001 - 提前触发 openai 惰性 import
            except EnrichConfigError as exc:
                raise FetchError(
                    f"openai 依赖未安装(prompt 引擎 LLM 调用需要):{INSTALL_COMMAND}",
                    error_type="dependency_missing",
                ) from exc
        try:
            completion: CompletionResult = await asyncio.wait_for(
                completer(
                    model=options["model"],
                    system=SYSTEM_PROMPT,
                    user=user_message,
                ),
                timeout=options["timeout"],
            )
        except asyncio.CancelledError:
            raise
        except Exception as exc:  # noqa: BLE001 - 端点/网络/超时:源级结构化失败
            raise FetchError(
                f"prompt 任务 LLM 调用失败 source={self.source.name}"
                f" model={options['model']}: {type(exc).__name__}: {exc}",
                error_type="prompt_llm_failed",
            ) from exc
        finally:
            # 资源卫生(复核条目④:每轮自建的 AsyncOpenAI/httpx 连接必关)——
            # 长驻宿主(cron ticker/sidecar)每日多源运行不再累积待 GC 客户端;
            # 关闭失败只告警,绝不顶掉真实结果/异常。
            if own_client is not None:
                try:
                    await own_client.aclose()
                except Exception:  # noqa: BLE001 - 清理失败不污染真实结果
                    logger.warning(
                        "prompt 引擎 LLM 客户端关闭失败(忽略) source=%s",
                        self.source.name,
                        exc_info=True,
                    )
        markdown = str(getattr(completion, "text", "") or "").strip()
        if not markdown:
            raise FetchError(
                f"prompt 任务 LLM 返回空摘要 source={self.source.name}"
                f" model={options['model']}(端点异常或 max_output_tokens 过小)",
                error_type="prompt_llm_failed",
            )
        logger.info(
            "prompt 任务摘要完成 source=%s model=%s targets=%s failed=%s "
            "tokens=%s markdown_chars=%s",
            self.source.name,
            options["model"],
            len(documents),
            len(failures),
            getattr(completion, "total_tokens", 0),
            len(markdown),
        )
        return markdown

    # --------------------------------------------------------------- mapping

    def _build_item(
        self,
        options: dict[str, Any],
        markdown: str,
        urls_ok: int,
        urls_failed: int,
    ) -> dict[str, Any]:
        """LLM 摘要 → 管线条目(日期锚点防全期去重;观测键进 metadata)."""
        stamp = datetime.now().strftime("%Y%m%d")  # 本地日期 = 日报语义
        item: dict[str, Any] = {
            "url": f"{self.source.url}#prompt-{stamp}",
            "title": options["title"],
            "content": markdown,
            "prompt_summary": markdown,
            "prompt_instructions": options["instructions"][:INSTRUCTIONS_SNIPPET_CHARS],
            "prompt_model": options["model"],
            "prompt_urls_ok": urls_ok,
            "prompt_urls_failed": urls_failed,
        }
        return item

    # ------------------------------------------------------- shape overrides

    def _check_pagination_support(self) -> None:
        """单轮任务语义:任何 pagination 配置都结构化拒(urlwatch 判例).

        监控对象就是固定 URL 清单;翻页游走会让「任务」的对象漂移。
        """
        if self.source.pagination is not None:
            raise FetchError(
                "prompt 引擎是单轮任务语义(urls 清单即监控对象,每轮一轮摘要),"
                "不支持 pagination 配置",
                error_type="pagination_unsupported",
            )
