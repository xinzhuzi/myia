"""Zenrows engine — 付费 SaaS gated 抓取(R6/D4,批二第 12 步;链外引擎).

API 形态已核(research 第五波,docs.zenrows.com/fetch/api-reference)::

    GET https://api.zenrows.com/v1/?apikey=<KEY>&url=<TARGET>
        &js_render=true            # 可选:JS 渲染
        &premium_proxy=true        # 可选:住宅代理
        &css_extractor={"price": ".price"}  # 可选:上游侧 CSS 抽取(响应转 JSON)

门槛与凭据纪律(前置查 gates / keychain 引用 / 凭据不落日志 / 永不进
AUTO_CHAIN)全部在共用骨架 :mod:`myssia.engines.saas`;本模块只映射参数面
与响应语义:

- 默认模式:响应 = 目标页 HTML 原文 → ``extract.type`` list/item CSS 抽取,
  无 extract 时回退单条目 {url, title, content}(firecrawl 形状);
- ``css_extractor`` 模式:上游按映射抽取,响应转 JSON → ``extract.type``
  json_path 或单条目(内容 = JSON 串)。

``engine_options.zenrows``:``js_render`` / ``premium_proxy``(布尔)、
``css_extractor``(``字段→CSS 选择器`` 映射或其 JSON 字符串)、``timeout``
(秒,缺省 60)。
"""

from __future__ import annotations

import json
from collections.abc import Mapping
from typing import Any

from myssia.engines.fetch_base import FetchError
from myssia.engines.saas import SaasEngineBase

__all__ = ["ZenrowsEngine"]


class ZenrowsEngine(SaasEngineBase):
    """Zenrows 上游代抓(显式 ``engine: zenrows``;门槛 saas.zenrows)。"""

    LAYER = "SAAS"
    ENGINE_NAME = "zenrows"
    GATE_NAME = "zenrows"
    API_ENDPOINT = "https://api.zenrows.com/v1/"
    API_KEY_PARAM = "apikey"
    REQUIRES_EXTRACT = False
    #: HTML 直通模式(list/item)+ css_extractor 上游抽取模式(json_path)。
    SUPPORTED_EXTRACT_TYPES = ("list", "item", "json_path")

    def _query_params(self) -> dict[str, str]:
        params: dict[str, str] = {}
        if self._bool_option("js_render"):
            params["js_render"] = "true"
        if self._bool_option("premium_proxy"):
            params["premium_proxy"] = "true"
        css_extractor = self.engine_options().get("css_extractor")
        if css_extractor is not None:
            params["css_extractor"] = self._css_extractor(css_extractor)
        return params

    def _css_extractor(self, value: Any) -> str:
        """``css_extractor`` 收「字段→CSS 选择器」映射或已序列化 JSON 字符串。

        映射形态序列化为紧凑 JSON(上游查询参数语义);空映射/其他类型结构化
        拒 —— 含糊值进了查询串只会换来上游 400,不如本地拒清楚。
        """
        if isinstance(value, str) and value.strip():
            return value
        if isinstance(value, Mapping) and value:
            return json.dumps(value, ensure_ascii=False, separators=(",", ":"))
        raise FetchError(
            "engine_options.zenrows.css_extractor 应为「字段→CSS 选择器」映射"
            f"或其 JSON 字符串,当前为 {value!r}(启用后上游响应转 JSON)",
            error_type="invalid_engine_options",
        )

    def _upstream_returns_json(self) -> bool:
        """css_extractor 一经配置,Zenrows 响应即 JSON(上游抽取语义)。"""
        return "css_extractor" in self.engine_options()
