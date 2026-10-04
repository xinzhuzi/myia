"""Shared SaaS fetch skeleton for the gated paid engines (R6/D4, 批二第 12 步).

Zenrows 与 ScraperAPI 同为「GET + key + url」薄形态(API 形态已核,research
第五波:``GET api.zenrows.com/v1/?apikey=&url=`` / ``GET api.scraperapi.com/
?api_key=&url=``),共用本骨架 —— fetch 前置查 gates → keychain 解 api_key →
httpx GET 上游代抓;两引擎模块(:mod:`myssia.engines.zenrows` /
:mod:`myssia.engines.scraperapi`)只映射各自的参数面与响应语义。

门槛契约(D4/design §6.3,R6):

- **fail-closed 前置检查**(fetch 时,零网络):``gates.yaml`` 经
  :func:`myssia.gates.load_gates_fail_closed` 装载 —— 文件缺失/损坏 = 全关;
  ``paid_engines`` 总开关 ∧ ``saas.<name>.enabled`` 件开关任一未开 → 结构化
  失败 ``gate_closed``(**新失败类**,与 ``dependency_missing`` 分列:门槛关着
  不是故障,是用户未知情开启 —— doctor 文案据此区分「关着」与「缺依赖」)。
  关闭态**零上游请求**:不烧钱是本类的存在理由;
- **永不进 AUTO_CHAIN**(链外引擎,credhunter 先例):显式 ``engine:`` 选择
  才生效,单级链,失败即源级结构化失败,不降级、不拦品类(铁律);
- **api_key 只走钥匙串**:引用来自 gates.yaml ``saas.<name>.api_key``
  (:mod:`myssia.gates` 构造期已强制 ``keychain:`` 引用形态,零明文),fetch
  时经 :func:`myssia.schema.resolve_credential` + ``context.keychain_backend``
  解析(测试注 mock backend);门槛开着但引用缺位 = ``gate_key_missing``
  结构化失败,解析失败 :class:`CredentialResolveError` 原样上抛(既有凭据
  分类通道);
- **凭据不落日志**:上游请求 URL 内嵌 apikey 查询参数 —— 重试/HTTP 错误
  路径的 URL 展示一律过 :func:`mask_endpoint_url`(firecrawl 同款纪律;
  端点常量本身是公开文档值,可入日志)。

礼貌约束(robots/限速)作用于**目标站点**(由上游代抓),不是我们自己的
后端(firecrawl 镜像先例)。变更指纹不协商:SaaS 后端不透传目标站的
ETag/Last-Modified,304 协商对代抓响应无意义,每次 fetch 都是全量取回。
"""

from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Any

import httpx
from selectolax.parser import HTMLParser

from myssia.engines.fetch_base import (
    BaseEngine,
    FetchError,
    decode_response,
    extract_html,
    extract_json,
    mask_endpoint_url,
)
from myssia.gates import (
    GatesConfig,
    SaaSGate,
    default_gates_path,
    gate_open,
    load_gates_fail_closed,
)
from myssia.schema import resolve_credential

logger = logging.getLogger(__name__)

#: 上游预算缺省(秒):JS 渲染/代理链路比直连慢,取 firecrawl 后端预算量级;
#: ``engine_options.<name>.timeout`` 可调(HTTP 客户端超时取 max(上游预算,
#: 管线默认),客户端不得早于上游预算掐断)。
DEFAULT_SAAS_TIMEOUT_SECONDS = 60.0

#: 门槛未开的结构化失败类 —— 与 ``dependency_missing``/``mcp_server_missing``
#: 分列的新失败类(D4:doctor 文案区分「门槛关着」与「缺依赖」)。
GATE_CLOSED_ERROR_TYPE = "gate_closed"

#: 门槛开着但钥匙串引用缺位(手写 gates.yaml 漏 ``api_key``)的失败类。
GATE_KEY_MISSING_ERROR_TYPE = "gate_key_missing"

__all__ = [
    "DEFAULT_SAAS_TIMEOUT_SECONDS",
    "GATE_CLOSED_ERROR_TYPE",
    "GATE_KEY_MISSING_ERROR_TYPE",
    "SaasEngineBase",
    "gates_path",
]


def gates_path() -> Path:
    """引擎侧 gates.yaml 解析口(fetch 时逐次解析,不缓存)。

    与 CLI 缺省同一位序(:func:`myssia.gates.default_gates_path`):
    ``MYIA_HOME`` env > ``~/.myia/gates.yaml`` —— 桌面启动器 spawn sidecar 时
    注入 ``MYIA_HOME``(main.rs v1.1.1 规则),桌面/CLI/引擎读到同一文件。
    逐次解析让用户改门槛后下一个 run 立即生效(改 gates.yaml 不需要重启)。
    """
    return default_gates_path()


def _html_title(html: str) -> str:
    """HTML 回退条目的 title(无 extract 时;selectolax 已是核心依赖)。"""
    try:
        node = HTMLParser(html).css_first("title")
    except Exception:  # noqa: BLE001 — 病态 HTML 的 title 是尽力而为,不拦条目
        return ""
    return node.text(strip=True) if node is not None else ""


class SaasEngineBase(BaseEngine):
    """付费 SaaS 引擎骨架:gates 前置 → 钥匙串 api_key → GET 上游代抓。

    子类只声明参数面(``API_ENDPOINT``/``API_KEY_PARAM``/``_query_params``)
    与响应语义(``_upstream_returns_json``);门槛、凭据、日志脱敏、礼貌约束
    全部在本层一次落死。链外注册(``ENGINE_REGISTRY`` 在册、``AUTO_CHAIN``
    不在)由 registry 层保证,本类不感知链。
    """

    LAYER = "SAAS"
    ENGINE_NAME = "saas"
    REQUIRES_EXTRACT = False
    #: gates.yaml ``saas`` 节的逐件键名(官方惯例 = 引擎名同形)。
    GATE_NAME = ""
    #: 上游 REST 端点(公开文档常量,可入日志;查询参数才含凭据)。
    API_ENDPOINT = ""
    #: api key 的查询参数名(Zenrows ``apikey`` / ScraperAPI ``api_key``)。
    API_KEY_PARAM = "apikey"

    # ------------------------------------------------------ gate & credentials

    def _load_gates(self) -> GatesConfig:
        """装载 gates.yaml(fail-closed:坏文件 = 全关态继续,warning 留痕)。"""
        path = gates_path()
        config, error = load_gates_fail_closed(path)
        if error is not None:
            logger.warning(
                "gates.yaml 不可载,门槛件按全关处理 path=%s: %s",
                path, error.get("message") or error,
            )
        return config

    def _gate(self) -> SaaSGate:
        """前置门槛检查(零网络):总开关 ∧ 件开关,任一未开即 ``gate_closed``。

        消息带齐开闸三步(写钥匙串键 → 总开关 → 件开关)—— 门槛失败的
        self-service 文案,doctor/日志可直接消费。
        """
        config = self._load_gates()
        if not gate_open(config, "saas", self.GATE_NAME):
            raise FetchError(
                f"{self.ENGINE_NAME} 付费通道门槛未开,本轮零请求零扣费"
                f"(paid_engines 总开关与 saas.{self.GATE_NAME} 件开关需都知情开启;"
                f"关闭不是故障,是未启用 —— 与缺依赖不同类):"
                f"先 myssia secret set myia/saas/{self.GATE_NAME}-key 写入钥匙串,"
                f"再 myssia gates set paid_engines on 与 myssia gates set"
                f" saas.{self.GATE_NAME} on",
                error_type=GATE_CLOSED_ERROR_TYPE,
            )
        return config.saas[self.GATE_NAME]

    def _api_key(self, gate: SaaSGate) -> str:
        """解 saas 逐件的 api_key(引用 → 值;解析值只进查询参数,不落日志)。"""
        if gate.api_key_ref is None:
            raise FetchError(
                f"saas.{self.GATE_NAME} 门槛已开但 api_key 引用缺位:"
                f"myssia secret set myia/saas/{self.GATE_NAME}-key 写入钥匙串,"
                f"并在 gates.yaml saas.{self.GATE_NAME}.api_key 引用"
                f"(keychain:myia/saas/{self.GATE_NAME}-key)",
                error_type=GATE_KEY_MISSING_ERROR_TYPE,
            )
        return resolve_credential(gate.api_key_ref, backend=self.context.keychain_backend)

    # ------------------------------------------------------------- options

    def _timeout(self) -> float:
        value = self.engine_options().get("timeout")
        if value is None:
            return DEFAULT_SAAS_TIMEOUT_SECONDS
        if isinstance(value, bool) or not isinstance(value, (int, float)) or value <= 0:
            raise FetchError(
                f"engine_options.{self.ENGINE_NAME}.timeout 应为正数秒,当前为 {value!r}",
                error_type="invalid_timeout",
            )
        return float(value)

    def _bool_option(self, name: str, *, default: bool = False) -> bool:
        """布尔选项(类型错即结构化拒;SaaS 参数面容不下含糊值)。"""
        value = self.engine_options().get(name, default)
        if not isinstance(value, bool):
            raise FetchError(
                f"engine_options.{self.ENGINE_NAME}.{name} 应为布尔,当前为 {value!r}",
                error_type="invalid_engine_options",
            )
        return value

    def _query_params(self) -> dict[str, str]:
        """上游额外查询参数(子类按参数面映射;布尔须序列化为 true/false)。"""
        return {}

    # --------------------------------------------------------------- fetch

    async def _fetch_impl(self) -> list[dict]:
        gate = self._gate()
        api_key = self._api_key(gate)
        timeout = self._timeout()
        logger.info(
            "%s 付费通道门槛已开 gate=saas.%s api_key=%s timeout=%ss",
            self.ENGINE_NAME, self.GATE_NAME, "已配置", timeout,
        )
        items: list[dict] = []
        for target_url in self._template_urls():
            # 礼貌约束作用于目标站点(由上游代抓),不是我们自己的后端。
            await self._ensure_robots_allowed(target_url)
            await self._acquire_rate_limit(target_url)
            response = await self._upstream_get(target_url, api_key, timeout)
            items.extend(self._parse_response(response, target_url))
        return items

    async def _upstream_get(
        self, target_url: str, api_key: str, timeout: float
    ) -> httpx.Response:
        """GET 上游(key+url 进查询参数);HTTP 错误包装成脱敏结构化失败。

        httpx 异常的 str 内嵌完整解析 URL(含 apikey 查询参数)—— 透传会把
        凭据带进 failures[] 与日志,故 ``http_<status>`` 的消息只记端点常量与
        目标 URL(均公开),重试 WARNING 的 URL 展示走 :func:`mask_endpoint_url`
        (firecrawl 同款纪律)。
        """
        params = {self.API_KEY_PARAM: api_key, "url": target_url, **self._query_params()}
        url = str(httpx.URL(self.API_ENDPOINT, params=params))
        try:
            return await self._send_with_retry(
                "GET",
                url,
                timeout=max(timeout, self.context.timeout),
                log_url=mask_endpoint_url(url),
            )
        except httpx.HTTPStatusError as exc:
            status = exc.response.status_code
            raise FetchError(
                f"{self.ENGINE_NAME} 上游 HTTP {status} endpoint={self.API_ENDPOINT}"
                f" url={target_url}: {exc.response.reason_phrase}",
                error_type=f"http_{status}",
            ) from exc

    # -------------------------------------------------------------- parsing

    def _upstream_returns_json(self) -> bool:
        """上游响应是否为 JSON(默认 HTML 直通;Zenrows css_extractor 模式覆写)。"""
        return False

    def _parse_response(self, response: httpx.Response, target_url: str) -> list[dict]:
        if self._upstream_returns_json():
            return self._parse_json_response(response, target_url)
        return self._parse_html_response(response, target_url)

    def _parse_html_response(
        self, response: httpx.Response, target_url: str
    ) -> list[dict]:
        extract = self.source.extract
        if extract is not None:
            if extract.type == "json_path":
                raise FetchError(
                    f"{self.ENGINE_NAME} 默认模式响应是 HTML(目标页原文),"
                    f"extract.type=json_path 需要 Zenrows css_extractor 上游抽取模式"
                    f"(engine_options.zenrows.css_extractor)或改用 list/item",
                    error_type="extract_unsupported",
                )
            return extract_html(decode_response(response), extract, base_url=target_url)
        html = decode_response(response)
        return [{"url": target_url, "title": _html_title(html), "content": html}]

    def _parse_json_response(
        self, response: httpx.Response, target_url: str
    ) -> list[dict]:
        extract = self.source.extract
        if extract is not None and extract.type != "json_path":
            raise FetchError(
                f"{self.ENGINE_NAME} 上游抽取模式(css_extractor)的响应是 JSON,"
                f"extract.type={extract.type!r} 不适用,应为 json_path",
                error_type="extract_unsupported",
            )
        try:
            payload: Any = response.json()
        except ValueError as exc:
            raise FetchError(
                f"{self.ENGINE_NAME} 上游响应不是有效 JSON url={target_url}: {exc}",
                error_type="json_decode",
            ) from exc
        if extract is not None:
            return extract_json(payload, extract)
        return [
            {
                "url": target_url,
                "title": "",
                "content": json.dumps(payload, ensure_ascii=False),
            }
        ]
