"""SearXNG 自托管元搜索引擎 —— 关键词日报,链外,零凭据(10-05-source-searxng).

``engine: searxng`` 显式选择才生效(链外注册,credhunter/reddit/urlwatch
先例):``ENGINE_REGISTRY`` 在册、``AUTO_CHAIN`` 不在,auto 永不路过;显式
选择 = 单级链,失败/空态都是源级结构化结果,品类内其余源不受影响(铁律)。
搜索型源没有「降级链」语义——实例坏了就是本源结构化失败,不是换浏览器
引擎能救的(同 reddit 论证形态)。

请求形状(探查实测定案,research §9-1;蓝本 ``.trellis/tasks/
10-05-source-searxng/``,实测实例 2026.10.4+d48c4b555)::

    GET {base}/search?q=<关键词>&format=json&language=zh-CN
        &safesearch=1&pageno=1&categories=web

- ``categories=web`` 是实测定案:缺省 general 类只挂 9 个小引擎,弱网出口
  可全灭;web 是大类池(google cse/naver/qwant 系/bing/ddg/brave…)。
- 每词固定 ``pageno=1`` 一页(实测评判:web 池一页 20-65 条,对关键词日报
  足够;深页对上游放大请求且质量陡降)—— 因此 ``pagination`` 配置即结构化
  拒(reddit/urlwatch 单页语义同款)。
- 常发 ``Accept-Language: zh-CN,zh;q=0.9``:limiter-on 实例一行头即过
  (实测拦截面只认缺 Accept-Language 这一件),limiter-off 无害。

``base`` 三级解析(firecrawl ``ENV_FIRECRAWL_URL`` 先例,firecrawl.py:46-48):
源级扩展参数 ``searxng_base_url`` > env ``MYIA_SEARXNG_URL`` > 内置缺省
``http://127.0.0.1:8888``。base_url 是自家实例地址,明文非凭据(prd 红线:
queries/base_url 均明文可落 YAML,零 env/keychain 引用面)。

条目映射(research §9-2):只收 ``template == "default.html"`` 的行(实测
images.html 卡会混入 web 池);缺 url/title 的坏行跳过(不废整源,rss 逐
条目语义);``content`` 摘要可空串;``publishedDate`` 非空字符串透传
(实测 web 池多为 null)。去重走 feed 层既有 url metric 键(实测同 URL
不同标题会重复出现,必要;零新机制)。

礼貌口径(research §5-3/§9-3,实测背书):自托管也设——逐词串行 + 词间
``query_delay``(缺省 3s,探查纪律同款)+ 既有 per-host 限速;上游元搜索
的礼貌由 SearXNG 聚合层承担(其自带 ``ban_time_on_fail``/
``suspended_times`` 熔断),MYIA 不放大。run 级间隔建议 ≥1800s(文档/
示例 YAML 面,不属引擎强制)。robots 面不适用自家实例(自授权通道,
research §6 结案;实例内置 robots 禁的是第三方爬虫的 ``/*?*q=*``,
MYIA 采集的是主人自己部署的实例;上游搜索源的礼貌由聚合层统一承担)
—— 引擎不查 robots.txt(reddit「robots 面不适用钉死端点」同款论证,
本引擎的请求只发往三级解析出的自家 base)。

错误面(research §4/§7,实测对账;+ 轨B 就绪探测,10-06 G-Q5):

- **就绪探测先行**(``/healthz`` 一发即定,不走重试预算):loopback base
  探测 transport 失败 → ``searxng_service_not_running``「服务组件未启动」
  结构化失败,文案引导设置页「Python 运行环境 → 关键词日报(SearXNG)」行
  「启动」;**不隐式拉起**(启停是管控面显式动作,G-Q5)。远端 base 保持
  「实例未起」network 分类;任何 HTTP 应答(含 404/5xx)= 实例在,放行
  /search(健康语义归设置卡绿点);
- HTTP 403 → 实例未开 json format(部署侧:settings.yml 的
  ``search.formats`` 加 ``json`` 后重启容器;实测未激活时 Flask 路由层
  即拒,零上游成本);
- HTTP 429 → limiter 拦截(客户端已常发 Accept-Language;仍拦则核对实例
  limiter/ip_lists 口径);
- HTTP 400/5xx → 透传响应体 ``error`` 字段(实测 ``{"error": "No query"}``
  等形态);
- 连接拒绝等 transport 失败(就绪探测已放行后的运行中死亡)→ 「实例未起」
  结构化失败(同 firecrawl 自托管死服务优雅降级口径,不挂死管线);
- 响应非 JSON / ``results`` 非数组 → ``json_decode`` /
  ``searxng_payload_malformed``。

零结果(引擎全灭,``unresponsive_engines`` 非空但 HTTP 200)是**合法空
产出**:items=[] 正常返回,不设 skip、不报错(搜索没结果是常态,不是
源坏)。

Raises:
    FetchError: engine_options 类型错、源配置缺 queries、HTTP 失败
        (403/429/400/5xx 专属文案)、transport 失败(实例未起)、响应
        形状坏、pagination/extract 配置错配。
"""

from __future__ import annotations

import logging
import os
from typing import Any
from urllib.parse import urlencode, urlsplit

import httpx

from myssia.engines.fetch_base import (
    BaseEngine,
    FetchContext,
    FetchError,
    classify_exception,
)
from myssia.schema import SourceConfig

logger = logging.getLogger(__name__)

#: 引擎层标签(schema 引擎词表一员;链外源引擎,不进 AUTO_CHAIN)。
LAYER = "SELFHOST_SEARCH"

#: env 覆盖通道(firecrawl ``ENV_FIRECRAWL_URL`` 先例)。
ENV_SEARXNG_URL = "MYIA_SEARXNG_URL"

#: 内置缺省 base(本机探查栈口径:searxng-core 0.0.0.0:8888)。
DEFAULT_SEARXNG_BASE_URL = "http://127.0.0.1:8888"

#: 就绪探测端点(10-06-native-plugin-components 轨B/G-Q5:本机服务组件
#: 未启动 → 结构化失败并给设置页引导,**不隐式拉起**——启停是管控面显式
#: 动作,状态须在设置卡可见)。上游 /healthz 是纯文本 200,零上游搜索成本。
HEALTHZ_PATH = "healthz"

#: loopback 主机名集合(就绪探测失败文案分岔:loopback base = 本机壳服务
#: 组件实例(设置页可启);远端 base = 外部实例未起,引导部署侧)。
_LOOPBACK_HOSTS = frozenset({"127.0.0.1", "localhost", "::1"})

#: 请求参数常量(探查实测定案,research §9-1;不做配置面)。
SEARCH_CATEGORIES = "web"
SEARCH_LANGUAGE = "zh-CN"
SEARCH_SAFESEARCH = 1
SEARCH_PAGENO = 1

#: limiter-on 实例的一行头过闸(实测:拦截面只认缺 Accept-Language)。
ACCEPT_LANGUAGE = "zh-CN,zh;q=0.9"

#: 词间短延时缺省秒(逐词串行之外的礼貌垫层;探查纪律同款 3s)。
DEFAULT_QUERY_DELAY_SECONDS = 3.0

__all__ = [
    "ACCEPT_LANGUAGE",
    "DEFAULT_QUERY_DELAY_SECONDS",
    "DEFAULT_SEARXNG_BASE_URL",
    "ENV_SEARXNG_URL",
    "HEALTHZ_PATH",
    "LAYER",
    "SEARCH_CATEGORIES",
    "SEARCH_LANGUAGE",
    "SEARCH_SAFESEARCH",
    "SEARCH_PAGENO",
    "SearxngEngine",
]


class SearxngEngine(BaseEngine):
    """SearXNG 关键词搜索源(显式 ``engine: searxng``;零凭据).

    源配置:``queries: [关键词列表]``(源级扩展参数,schema 装载期对
    engine=searxng 强制非空字符串列表);``searxng_base_url`` 可选覆盖。
    内置 JSON 形状解析,``extract`` 节必是错配(配置即结构化拒,reddit
    先例);单页语义,``pagination`` 节同理拒。items 出口对齐
    ``Item.from_extracted`` 契约:url/title/content 管线键。
    """

    LAYER = "SELFHOST_SEARCH"
    ENGINE_NAME = "searxng"
    REQUIRES_EXTRACT = False
    SUPPORTED_EXTRACT_TYPES = ()

    # -------------------------------------------------------------- options

    def _base_url(self) -> str:
        """三级解析请求 base:源级 ``searxng_base_url`` > env > 内置缺省.

        base 是自家实例地址(明文非凭据,prd 红线),直接进日志无碍;
        env 覆盖态记 env 名(research §9-5:部署迁移只改 env/源级键,
        YAML 其余不动)。
        """
        configured = self.source.extra_params.get("searxng_base_url")
        if configured is not None:
            base = self._validate_base(str(configured), "源级 searxng_base_url")
            logger.info("searxng base 就绪 source=%s base=%s", self.source.name, base)
            return base
        from_env = os.environ.get(ENV_SEARXNG_URL, "").strip()
        if from_env:
            base = self._validate_base(from_env, f"env:{ENV_SEARXNG_URL}")
            logger.info(
                "searxng base 就绪 source=%s base=%s(env:%s 覆盖缺省)",
                self.source.name,
                base,
                ENV_SEARXNG_URL,
            )
            return base
        logger.info(
            "searxng base 就绪 source=%s base=%s(内置缺省)",
            self.source.name,
            DEFAULT_SEARXNG_BASE_URL,
        )
        return DEFAULT_SEARXNG_BASE_URL

    @staticmethod
    def _validate_base(raw: str, label: str) -> str:
        """base 形态校验:http(s) + host;尾斜杠剥掉(拼接面统一)."""
        value = raw.strip().rstrip("/")
        parts = urlsplit(value)
        if parts.scheme not in ("http", "https") or not parts.netloc:
            raise FetchError(
                f"{label} 应为 http(s) 实例地址(如 {DEFAULT_SEARXNG_BASE_URL}),"
                f"当前为 {raw!r}",
                error_type="invalid_searxng_base_url",
            )
        return value

    def _queries(self) -> list[str]:
        """搜索关键词列表(schema 装载期已校验必填;此处宽容复核)."""
        raw = self.source.extra_params.get("queries")
        if not isinstance(raw, list) or not raw:
            raise FetchError(
                "searxng 引擎需要源级 queries: [关键词列表](非空字符串列表),"
                "当前缺失或为空",
                error_type="missing_searxng_queries",
            )
        return [str(item).strip() for item in raw if str(item).strip()]

    def _query_delay(self) -> float:
        """词间短延时秒(research §9-3 礼貌垫层;0 = 显式关闭)."""
        value = self.engine_options().get("query_delay", DEFAULT_QUERY_DELAY_SECONDS)
        if isinstance(value, bool) or not isinstance(value, (int, float)) or value < 0:
            raise FetchError(
                f"engine_options.searxng.query_delay 应为 ≥0 的数值秒,当前为 {value!r}",
                error_type="invalid_engine_options",
            )
        return float(value)

    # ----------------------------------------------------------------- fetch

    async def _fetch_impl(self) -> list[dict]:
        base = self._base_url()
        queries = self._queries()
        delay = self._query_delay()
        # G-Q5 就绪探测先行:本机服务组件未启动 → 结构化失败引导设置页
        # (零 /search 流量——探测不过就不放查询,礼貌面同源)。
        await self._ensure_service_up(base)
        url = f"{base}/search"
        # 源级显式 Accept-Language 尊重用户配置(reddit UA 政策同款优先级)。
        headers = dict(self._headers)
        if "accept-language" not in {key.lower() for key in headers}:
            headers["Accept-Language"] = ACCEPT_LANGUAGE
        items: list[dict] = []
        for index, query in enumerate(queries):
            if index and delay > 0:
                # 词间短延时:逐词串行之外的礼貌垫层(自托管也不放大)。
                await self.context.sleep(delay)
            payload = await self._search_once(url, headers, query)
            produced = self._parse_results(payload, query)
            logger.info(
                "searxng 搜索落地 source=%s query=%r results=%s items=%s",
                self.source.name,
                query,
                len(payload.get("results") or []),
                len(produced),
            )
            items.extend(produced)
        return items

    async def _ensure_service_up(self, base: str) -> None:
        """G-Q5 就绪探测(10-06-native-plugin-components 轨B):跑源先打一发
        ``/healthz``——**一发即定**(不走重试预算:服务态不会在毫秒级退避里
        翻转,重试只是白等;搜索请求自身的既有重试不受影响)。

        - 任何 HTTP 应答(2xx/404/5xx 皆可)= 实例在(健康语义归设置卡绿点,
          此处只判「有没有起来」;老实例无 /healthz 路由 → 404 也是「在」)。
        - transport 失败(连接拒绝/超时):
          - loopback base(=本机壳服务组件实例,缺省 ``127.0.0.1:8888`` 即
            此类)→ ``searxng_service_not_running`` 结构化失败,文案引导设置
            页「Python 运行环境 → 关键词日报(SearXNG)」行点「启动」;
            **不隐式拉起**(隐式拉起=状态不可见,违背管控面透明判例)。
          - 远端 base → 既有「实例未起」network 分类(firecrawl 死服务口径)。
        """
        probe_url = f"{base}/{HEALTHZ_PATH}"
        try:
            await self._active_client.request(
                "GET",
                probe_url,
                headers={"Accept-Language": ACCEPT_LANGUAGE},
                timeout=self.context.timeout,
            )
        except httpx.TransportError as exc:
            if urlsplit(base).hostname in _LOOPBACK_HOSTS:
                raise FetchError(
                    "searxng 服务组件未启动(就绪探测 /healthz 网络失败:"
                    f" {exc};本机实例请在 设置 → Python 运行环境 → 可选组件"
                    "「关键词日报(SearXNG)」行点「启动」后重跑;"
                    "引擎不隐式拉起服务,启停状态在设置卡可见)",
                    error_type="searxng_service_not_running",
                ) from exc
            raise FetchError(
                f"searxng 实例网络失败(常见=实例未起;base 见上文就绪行;"
                f"起栈指引见 plugins/searxng.yaml 头注): {exc}",
                error_type=classify_exception(exc),
            ) from exc
        logger.debug("searxng 就绪探测通过 base=%s(/healthz 有应答)", base)

    async def _search_once(
        self, url: str, headers: dict[str, str], query: str
    ) -> dict[str, Any]:
        """一发搜索请求:per-host 限速 + 既有重试退避 + 结构化错误面."""
        params = {
            "q": query,
            "format": "json",
            "language": SEARCH_LANGUAGE,
            "safesearch": SEARCH_SAFESEARCH,
            "pageno": SEARCH_PAGENO,
            "categories": SEARCH_CATEGORIES,
        }
        request_url = f"{url}?{urlencode(params)}"
        await self._acquire_rate_limit(url)
        try:
            response = await self._send_with_retry("GET", request_url, headers=headers)
        except httpx.HTTPStatusError as exc:
            raise self._status_failure(exc, query) from exc
        except httpx.TransportError as exc:
            # 自托管死服务优雅降级(firecrawl 口径):连接拒绝/超时 =
            # 「实例未起」,不挂死管线,源级结构化失败。
            raise FetchError(
                f"searxng 实例网络失败(常见=实例未起;base 见上文就绪行;"
                f"起栈指引见 plugins/searxng.yaml 头注): {exc}",
                error_type=classify_exception(exc),
            ) from exc
        try:
            payload = response.json()
        except ValueError as exc:
            raise FetchError(
                f"searxng 响应不是有效 JSON query={query!r}: {exc}",
                error_type="json_decode",
            ) from exc
        if not isinstance(payload, dict) or not isinstance(
            payload.get("results"), list
        ):
            raise FetchError(
                f"searxng 响应缺 results 数组 query={query!r}"
                f"(顶层键: {sorted(payload) if isinstance(payload, dict) else type(payload).__name__})",
                error_type="searxng_payload_malformed",
            )
        return payload

    def _status_failure(self, exc: httpx.HTTPStatusError, query: str) -> FetchError:
        """HTTP >= 400 → 结构化 FetchError(403/429/400/5xx 专属文案)."""
        status = exc.response.status_code
        detail = ""
        if status in (400, 422, 500):
            # 实测错误体形态 {"error": "..."};非 JSON 体给 reason_phrase 兜底。
            try:
                body = exc.response.json()
            except ValueError:
                body = None
            if isinstance(body, dict) and isinstance(body.get("error"), str):
                detail = f": {body['error']}"
        hints = {
            403: "(部署侧未开 json format:实例 settings.yml 的 search.formats "
            "加 json 后重启实例生效;本机壳服务组件实例的 settings.yml 已由壳"
            "生成开启 json,重启走设置卡「启动/停止」按钮)",
            429: "(limiter 拦截:客户端已常发 Accept-Language;仍拦请核对实例 "
            "limiter/ip_lists 口径或改走自托管专用实例)",
        }
        hint = hints.get(status, "")
        return FetchError(
            f"searxng 搜索 HTTP {status} query={query!r}{detail}{hint}",
            error_type=f"http_{status}",
        )

    # --------------------------------------------------------------- parsing

    def _parse_results(self, payload: dict[str, Any], query: str) -> list[dict]:
        """results[] → 管线 items(template 过滤 + 坏行跳过;零结果合法)."""
        items: list[dict] = []
        for result in payload["results"]:
            if not isinstance(result, dict):
                continue
            if result.get("template") not in (None, "default.html"):
                continue  # images.html 卡等特殊模板混入 web 池,实测定案过滤
            url = result.get("url")
            title = result.get("title")
            if not isinstance(url, str) or not url.strip():
                continue  # 坏行跳过(缺 url),不废整源
            if not isinstance(title, str) or not title.strip():
                continue
            item: dict[str, Any] = {
                "url": url,
                "title": title,
                "content": str(result.get("content") or ""),
                "query": query,
            }
            published = result.get("publishedDate")
            if isinstance(published, str) and published.strip():
                item["published"] = published
            items.append(item)
        return items

    # ------------------------------------------------------- shape overrides

    def _check_pagination_support(self) -> None:
        """单页语义:任何 pagination 配置都结构化拒(不是只拒 scroll).

        每词固定 pageno=1 是实测定案(research §3/§9-3):web 池一页
        20-65 条,深页对上游放大请求且质量陡降;翻页需求属「加词/调
        categories」的部署侧策展,不是本引擎的游走面。
        """
        if self.source.pagination is not None:
            raise FetchError(
                "searxng 引擎是单页语义(每词固定 pageno=1,web 池一页 20-65 "
                "条对关键词日报足够;深页放大上游请求,实测定案不翻页),"
                "不支持 pagination 配置",
                error_type="pagination_unsupported",
            )
