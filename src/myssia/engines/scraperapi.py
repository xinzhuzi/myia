"""ScraperAPI engine — 付费 SaaS gated 抓取(R6/D4,批二第 12 步;链外引擎).

API 形态已核(research 第五波,docs.scraperapi.com)::

    GET https://api.scraperapi.com/?api_key=<KEY>&url=<TARGET>
        &country=us            # 可选:出口国家(ISO 3166-1 alpha-2)
        &render=true           # 可选:JS 渲染

门槛与凭据纪律(前置查 gates / keychain 引用 / 凭据不落日志 / 永不进
AUTO_CHAIN)全部在共用骨架 :mod:`myssia.engines.saas`;本模块只映射参数面:
响应恒为目标页 HTML 原文(无上游抽取模式),``extract.type`` list/item CSS
抽取,无 extract 时回退单条目 {url, title, content}(firecrawl 形状)。

``engine_options.scraperapi``:``country``(ISO 两字母)/``render``(布尔)/
``timeout``(秒,缺省 60)。
"""

from __future__ import annotations

import re

from myssia.engines.fetch_base import FetchError
from myssia.engines.saas import SaasEngineBase

__all__ = ["ScraperAPIEngine"]

#: ISO 3166-1 alpha-2(上游 country 参数语义;小写化后发上游)。
_COUNTRY_RE = re.compile(r"^[A-Za-z]{2}$")


class ScraperAPIEngine(SaasEngineBase):
    """ScraperAPI 上游代抓(显式 ``engine: scraperapi``;门槛 saas.scraperapi)。"""

    LAYER = "SAAS"
    ENGINE_NAME = "scraperapi"
    GATE_NAME = "scraperapi"
    API_ENDPOINT = "https://api.scraperapi.com/"
    API_KEY_PARAM = "api_key"
    REQUIRES_EXTRACT = False
    SUPPORTED_EXTRACT_TYPES = ("list", "item")

    def _query_params(self) -> dict[str, str]:
        params: dict[str, str] = {}
        if self._bool_option("render"):
            params["render"] = "true"
        country = self.engine_options().get("country")
        if country is not None:
            if not isinstance(country, str) or not _COUNTRY_RE.fullmatch(country):
                raise FetchError(
                    "engine_options.scraperapi.country 应为 ISO 3166-1 alpha-2"
                    f" 两字母国家码(如 us / jp),当前为 {country!r}",
                    error_type="invalid_engine_options",
                )
            params["country"] = country.lower()
        return params
