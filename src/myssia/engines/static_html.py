"""L2 engine: server-rendered static HTML via httpx + selectolax.

Contract (PRD 10-01-v01-engine-l1-l2):

- ``extract.type: list`` (item selector + per-field CSS selectors, ``@href`` /
  ``@src`` attribute values, relative URLs resolved against the page URL) and
  ``item`` (single-page, document-level selectors); ``json_path`` is rejected
  here so ``engine: auto`` degrades correctly. ``rss`` (10-03-news-rss) rides
  the same text path: the body goes to :func:`fetch_base.extract_rss`
  (feedparser) instead of CSS selectors — RSS 的 ``<link>`` void 元素拿不到
  条目 url,硬接 CSS = 静默零产出;``direct_api`` 保持 JSON-only(rss 配
  direct_api 在引擎层拒);
- non-UTF8 responses (gb18030/big5 legacy forums — 生产源痛点) are decoded by
  ``fetch_base.decode_response``: BOM > Content-Type charset > meta charset >
  utf-8/gb18030/big5 fallbacks;
- pagination walks ``template`` (``{page}`` in the URL, ``max_pages`` cap) and
  ``selector`` (``a.next@href`` next-link following, loop-guarded) modes;
  ``scroll`` is L4+ and never reached by this engine;
- per-URL change fingerprints skip pages whose content did not change;
- trafilatura 正文兜底(10-05-trafilatura-impl,opt-in):``MYIA_EXTRACT_FALLBACK=1``
  且 extras 已装时,①extract 缺失(覆写放行)与②规则跑空(rss 除外)走单页正文
  兜底;产出过最低正文量门才出条(键面全为管线既有键,条目带
  ``extract_provenance="trafilatura"``),不过门/启发式失败=维持零条语义。
  字段级失败(条目缺 url/部分字段 miss)不兜底;规则命中的源结构性永不触达。
  源级覆写(10-05-trafilatura-source-scope):``engine_options.static_html.
  extract_fallback: true/false`` 单源开/关,优先级=源级 > 全局 env > 缺省关。

Raises:
    FetchError: extract config missing/unsupported, template param missing.
    ExtractionError: malformed extract selector configuration.
"""

from __future__ import annotations

import json
import logging
import os
from typing import Any, Optional
from urllib.parse import urljoin

from selectolax.parser import HTMLParser

from myssia.engines.fetch_base import (
    BaseEngine,
    FetchError,
    decode_response,
    extract_html,
    extract_rss,
    split_attr_selector,
)

logger = logging.getLogger(__name__)

LAYER = "L2"

#: 兜底开关——全局态(缺省关=既有源零行为差);读点在引擎内,CLI 与 sidecar 同一
#: 代码路径自然同读(desktop/entry.py:563-567「env 可被测试逐例注入」同款形态)。
#: 源级覆写(10-05-trafilatura-source-scope):``engine_options.static_html.
#: extract_fallback`` 单源开/关,优先级=源级 > 全局 env > 缺省关。
FALLBACK_ENV = "MYIA_EXTRACT_FALLBACK"
#: 源级覆写键名(engine_options.<ENGINE_NAME> 旋钮命名空间,saas._bool_option 先例)。
FALLBACK_OPTION = "extract_fallback"
#: 最低正文量门(字符数):夹具标定——文章页 203 过 / 列表页退化 78 拦,120 居中
#: (评估档 §2.4 矩阵);不过门=视同启发式失败=维持零条语义,不产伪条目。
FALLBACK_MIN_TEXT_CHARS = 120

__all__ = ["LAYER", "StaticHTMLEngine"]


def _load_trafilatura() -> Any:
    """惰性 import trafilatura(extras 可选依赖,不进核心)。

    缺装不拦核心铁律:ImportError 只 WARNING 带安装命令后返回 None——①由
    ``_check_extract_support`` 覆写回落现状拒载,②维持零条语义,手写规则
    路径全程不受影响。
    """
    try:
        import trafilatura
    except ImportError:
        logger.warning(
            "trafilatura 兜底不可用(缺装,兜底能力降级不拦核心):"
            "pip install 'myssia[trafilatura]'"
        )
        return None
    return trafilatura


def _trafilatura_fallback(html: str, url: str) -> list[dict] | None:
    """单页正文兜底(评估档 §2.2 契约);None=不可用/失败/不过质量门。

    钉版 API:``extract(output_format="json", with_metadata=True)`` 返回 JSON
    串(``bare_extraction`` 2.3.0 返回 Document 非 dict,评估档实测,禁用)。
    产出=单页一条,键面全为管线/白名单既有键:url/title/content =
    ``Item.from_extracted`` known 键,published/author = RSS_ENTRY_FIELDS 既有
    字段名(缺则省略),``extract_provenance`` 落条目 metadata;其余 JSON 键
    (description/sitename/categories/fingerprint/…)不映射直接丢。
    """
    trafilatura = _load_trafilatura()
    if trafilatura is None:
        return None
    try:
        raw = trafilatura.extract(
            html, url=url, output_format="json", with_metadata=True
        )
    except Exception as exc:  # 启发式内部崩溃不外溢:视同兜底失败
        logger.warning("trafilatura 兜底异常(视同兜底失败) url=%s: %s", url, exc)
        return None
    if not raw:
        return None  # 启发式判定无正文(trafilatura 自判阈值过宽,门在自己手里)
    try:
        doc = json.loads(raw)
    except (TypeError, ValueError):
        logger.warning("trafilatura 兜底输出非 JSON url=%s", url)
        return None
    if not isinstance(doc, dict):
        logger.warning("trafilatura 兜底输出形状异常 url=%s type=%s", url, type(doc).__name__)
        return None
    content = (doc.get("text") or doc.get("raw_text") or "").strip()
    if len(content) < FALLBACK_MIN_TEXT_CHARS:
        logger.info(
            "trafilatura 兜底正文量不足门(%s<%s),维持零条语义 url=%s",
            len(content), FALLBACK_MIN_TEXT_CHARS, url,
        )
        return None
    item: dict[str, Any] = {
        "url": url,
        "title": doc.get("title") or "",  # 可退化(title 空由既有容错消化)
        "content": content,
    }
    if doc.get("date"):
        item["published"] = doc["date"]
    if doc.get("author"):
        item["author"] = doc["author"]
    item["extract_provenance"] = "trafilatura"
    return [item]


class StaticHTMLEngine(BaseEngine):
    """Fetch static pages and apply the CSS ``extract`` selectors."""

    LAYER = "L2"
    ENGINE_NAME = "static_html"
    SUPPORTED_EXTRACT_TYPES = ("list", "item", "rss")

    def _fallback_enabled(self) -> bool:
        """兜底开关取值链(10-05-trafilatura-source-scope):源级 > 全局 env > 缺省关。

        源级 = ``engine_options.static_html.extract_fallback: true/false``
        (引擎旋钮命名空间,schema 开放参数直通;布尔类型错即结构化拒,
        saas ``_bool_option`` 先例——含糊值不开不关静默失效才是坑);
        未设 → 全局 ``MYIA_EXTRACT_FALLBACK == "1"``(现状语义逐字节不变)。
        """
        value = self.engine_options().get(FALLBACK_OPTION)
        if value is not None:
            if not isinstance(value, bool):
                raise FetchError(
                    f"engine_options.{self.ENGINE_NAME}.{FALLBACK_OPTION} 应为布尔,当前为 {value!r}",
                    error_type="invalid_engine_options",
                )
            return value
        return os.environ.get(FALLBACK_ENV) == "1"

    def _check_extract_support(self) -> None:
        """①extract=None 的兜底放行面(10-05-trafilatura-impl)。

        开关开且 trafilatura 可用才放行(extract 走 ``_fetch_page`` 兜底分流);
        其余一切情况(开关关/缺装/extract 非 None 的类型检查)逐字节走父类
        现状——开关缺省关 = ``extract_required`` 拒载语义零行为差。
        """
        if (
            self.source.extract is None
            and self._fallback_enabled()
            and _load_trafilatura() is not None
        ):
            return
        super()._check_extract_support()

    async def _fetch_impl(self) -> list[dict]:
        items: list[dict] = []
        pagination = self.source.pagination
        mode = pagination.mode if pagination else "template"
        if mode == "selector":
            await self._walk_selector(items)
        else:
            await self._walk_template(items)
        return items

    async def _walk_template(self, items: list[dict]) -> None:
        """``?page={n}`` walks capped by ``max_pages``; stops on unchanged/empty."""
        for url in self._template_urls():
            page_items, _, stop = await self._fetch_page(url)
            items.extend(page_items)
            if stop:
                break

    async def _walk_selector(self, items: list[dict]) -> None:
        """Follow the next-page link, ``max_pages``-capped and loop-guarded."""
        pagination = self.source.pagination
        assert pagination is not None and pagination.selector  # schema-enforced
        url = self.source.url
        visited = {url}
        for _ in range(pagination.max_pages):
            page_items, next_url, stop = await self._fetch_page(url)
            items.extend(page_items)
            if stop or not next_url:
                break
            if next_url in visited:
                logger.warning("翻页检测到环路,提前收尾 url=%s", next_url)
                break
            visited.add(next_url)
            url = next_url

    async def _fetch_page(self, url: str) -> tuple[list[dict], Optional[str], bool]:
        """Fetch+extract one page; returns (items, next_url, stop_walk)."""
        response = await self.request(url)
        if response.status_code == 304:
            self.last_skip_reason = "not_modified"
            logger.info("变更指纹协商命中(304),跳过 url=%s", url)
            return [], None, True
        text = decode_response(response)
        verdict = self.check_change(url, response, decoded_text=text)
        if not verdict.changed:
            self.last_skip_reason = verdict.reason
            logger.info("变更指纹未变(%s),跳过 url=%s", verdict.reason, url)
            return [], None, True
        # 提取出口分流(10-03-news-rss):rss 走 feedparser 条目映射(fields
        # 值=entry 属性白名单),其余类型走 CSS 选择器。
        extract = self.source.extract
        if extract is None:
            # ① 规则缺失兜底(10-05-trafilatura-impl):_check_extract_support
            # 覆写已保证走到这里=开关开+trafilatura 可用。兜底失败/不过门=
            # 维持零条语义(auto 链 L3 探测信号「static_html 真零结果」保真)。
            page_items = _trafilatura_fallback(text, url)
            if page_items:
                return page_items, self._next_page_url(text, url), False
            return [], None, True
        if extract.type == "rss":
            page_items = extract_rss(text, extract)
        else:
            page_items = extract_html(text, extract, base_url=url)
        if not page_items:
            # ② 规则跑空兜底(rss 除外:feedparser 白名单路径结构性不挂);
            # ③字段级失败不进——extract_html 内部语义(条目缺 url→管线
            # invalid_item 记账),本引擎零新代码。
            if extract.type != "rss" and self._fallback_enabled():
                page_items = _trafilatura_fallback(text, url)
                if page_items:
                    logger.info("规则跑空,trafilatura 兜底出条 url=%s", url)
                    return page_items, self._next_page_url(text, url), False
            logger.debug("本页提取 0 条,提前收尾 url=%s", url)
            return [], None, True
        next_url = self._next_page_url(text, url)
        return page_items, next_url, False

    def _next_page_url(self, html: str, base_url: str) -> Optional[str]:
        """Resolve the ``pagination.selector`` next-link (absolute URL), or None."""
        pagination = self.source.pagination
        if pagination is None or not pagination.selector:
            return None
        css, attr = split_attr_selector(pagination.selector)
        if not css:
            return None
        nodes = HTMLParser(html).css(css)
        if not nodes:
            return None
        node = nodes[0]
        value = node.attributes.get(attr) if attr else node.text(separator=" ", strip=True)
        if not value:
            return None
        return urljoin(base_url, value)
