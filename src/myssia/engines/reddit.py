"""Reddit 官方 Data API 引擎 —— OAuth2 授权通道,链外,凭据可选(10-05).

``engine: reddit`` 显式选择才生效(链外注册,credhunter/zenrows 先例):
``ENGINE_REGISTRY`` 在册、``AUTO_CHAIN`` 不在,auto 永不路过;显式选择 =
单级链,失败/空态都是源级结构化结果,品类内其余源不受影响(铁律)。

通道形态(官方 Data API,蓝本 ``.trellis/tasks/10-05-reddit-source/``):

1. OAuth2 **client_credentials**(userless):POST
   ``https://www.reddit.com/api/v1/access_token``(Basic auth =
   client_id:client_secret,body ``grant_type=client_credentials``)→
   ``access_token``(bearer,~1h);
2. 列表:GET ``https://oauth.reddit.com/r/<sub>/<listing>?limit=N&raw_json=1``
   (``Authorization: Bearer <token>``)→ ``data.children[].data`` → items。

凭据三态(核心决议:凭据可选,绝不拦核心):

- **未配置**(`client_id`/`client_secret` 引用均缺)→ 结构化
  ``credential_missing`` **显式空态**(credhunter 先例):零请求、
  :attr:`last_skip_reason` 置位、日志给人话指引(``myssia secret set
  myia/reddit/client-id`` / ``client-secret``);
- **引用在而解析失败**(钥匙串键未写等)→ 同空态 + warning 留痕
  (配置问题可见,不静默;credhunter ``_resolve_lane_key`` 同口径);
- **半配置**(只配了一只)→ 结构化 ``invalid_engine_options`` 拒绝
  (不是空态:漏写一半是配置错误,报错优于静默不启用)。

robots 论证(为何本引擎不查两宿主 robots.txt):www.reddit.com 与
oauth.reddit.com 的 robots 均全站 ``Disallow: /``,但官方一手口径
(蓝本证据 B6,Data API Wiki):"Our robots.txt is for search engines, not
Data API users." —— robots.txt 是搜索引擎爬虫礼貌面,OAuth 授权 Data API
的合规面在 Developer Terms(条款面:OAuth 强制/UA 硬格式/非商业口径)。
故本引擎的请求只保留**通用礼貌**(qps 限速 + 重试退避),不经
``_ensure_robots_allowed``(不拉 robots.txt,少两次无意义请求);该豁免
只属于本模块钉死的两个官方端点常量,引擎不提供任何通用绕 robots 能力,
通用引擎的 ``.rss``/``.json`` 直抓路线零改动(robots 全禁照旧拦它)。

UA 政策(Reddit 开发者条款硬格式 ``<platform>:<app ID>:<version>
(by /u/<username>)``,禁谎报):优先级 = 源级 ``headers.User-Agent``(完整
覆盖)> ``engine_options.reddit.ua_username``(拼 `` (by /u/<name>)`` 段)>
缺省 ``desktop:com.myia.app:1.0``。缺省**不带用户名** —— Reddit 建议带
账号身份但非强制,把账号钉进每个请求日志是隐私让步,缺省取隐私侧
(蓝本 §8.5 张力记录,design.md §6)。

其余边界:单页语义(``limit`` 1-100 缺省 25,无翻页/滚动 —— 循环间隔交
既有 run loop);token 实例内取一次即弃(**不做跨 run 缓存**:每 run 每源
2 请求,100 QPM 免费层下无压力);token 请求**无重试**(4xx = 凭据坏,
重试无意义,立即结构化失败);变更指纹不协商(Reddit /new 是时间流,条目
级去重靠管线 ``{url}`` 键,304/ETag 对列表端点无意义);凭据与 token 值
不落日志/错误消息(saas 同款纪律)。

Raises:
    FetchError: 源 URL 不符 oauth.reddit.com/r/<sub>/<listing> 契约、
        engine_options 类型错/半配置、OAuth/列表请求 HTTP 失败、响应
        形状不符。
"""

from __future__ import annotations

import base64
import logging
import re
from datetime import datetime, timezone
from typing import Any
from urllib.parse import urlencode, urlsplit

import httpx

from myssia.engines.fetch_base import (
    BaseEngine,
    FetchContext,
    FetchError,
    classify_exception,
)
from myssia.schema import CredentialResolveError, SourceConfig, resolve_credential

logger = logging.getLogger(__name__)

#: 引擎名(schema ``EngineName`` 词表一员;链外源引擎,不进 AUTO_CHAIN)。
LAYER = "OFFICIAL_API"

#: OAuth2 token 端点(公开文档常量,可入日志;凭据只进 Basic 头,不落日志)。
TOKEN_ENDPOINT = "https://www.reddit.com/api/v1/access_token"

#: Data API 宿主(源 URL 必须精确匹配;列表请求端点由引擎构造)。
API_HOST = "oauth.reddit.com"

#: 条目页 URL 的拼接前源(Reddit permalink 是站内绝对路径 ``/r/...``)。
PERMALINK_ORIGIN = "https://www.reddit.com"

#: client_credentials 通道的稳定 device 标识(≤30 位字母数字,不带用户身份)。
DEVICE_ID = "myssia01"

#: Reddit UA 硬格式的本引擎缺省(desktop:com.myia.app:1.0;不带用户名段,
#: 见模块文档「UA 政策」)。
DEFAULT_UA = "desktop:com.myia.app:1.0"

#: 单页条目上限(Reddit API 硬顶 100;缺省取「小 limit」礼貌决议)。
DEFAULT_LIMIT = 25
MAX_LIMIT = 100

#: 支持的 listing 词表(/r/<sub>/<listing>)。
LISTINGS = ("new", "hot", "rising", "top")

#: 源 URL 路径契约:/r/<sub>/<listing>,sub 允许多 sub 的 ``a+b`` 形态。
_SOURCE_PATH_RE = re.compile(r"^/r/(?P<sub>[A-Za-z0-9_+-]+)/(?P<listing>[a-z]+)/?$")

__all__ = [
    "API_HOST",
    "DEFAULT_LIMIT",
    "DEFAULT_UA",
    "LAYER",
    "LISTINGS",
    "TOKEN_ENDPOINT",
    "RedditEngine",
]


class RedditEngine(BaseEngine):
    """Reddit 官方 Data API 列表源(显式 ``engine: reddit``;凭据可选)。

    内置 Reddit JSON 形状解析,``extract`` 节必是错配(配置即结构化拒);
    单页语义,``pagination`` 节同理拒;items 出口对齐
    ``Item.from_extracted`` 契约:url(title/content 为管线键,其余进
    metadata)。
    """

    LAYER = "OFFICIAL_API"
    ENGINE_NAME = "reddit"
    REQUIRES_EXTRACT = False
    SUPPORTED_EXTRACT_TYPES = ()

    def __init__(self, source: SourceConfig, context: FetchContext) -> None:
        super().__init__(source, context)
        self._apply_user_agent()

    # -------------------------------------------------------------- options

    def _apply_user_agent(self) -> None:
        """Reddit 开发者条款 UA 覆盖(优先级见模块文档「UA 政策」).

        源级 ``headers.User-Agent`` 显式配置 = 最高优先级,原样保留
        (BaseEngine 已解析并注入 self._headers);否则用本引擎的 Reddit
        硬格式缺省(可拼 ``ua_username`` 段)。BaseEngine 填的通用
        ``DEFAULT_USER_AGENT`` 对 Reddit 条款是「无 App 标识」,必须换掉。
        """
        if "user-agent" in {key.lower() for key in self.source.headers}:
            return  # 源级显式 UA:完整覆盖,尊重用户
        username = self.engine_options().get("ua_username")
        if username is None:
            ua = DEFAULT_UA
        elif isinstance(username, str) and username.strip():
            ua = f"{DEFAULT_UA} (by /u/{username.strip()})"
        else:
            raise FetchError(
                f"engine_options.reddit.ua_username 应为 Reddit 用户名字符串,"
                f"当前为 {username!r}",
                error_type="invalid_engine_options",
            )
        self._headers["User-Agent"] = ua

    def _limit(self) -> int:
        """单页条目数:整数、1-100 钳制(超顶会被上游截断,先钳可见)."""
        value = self.engine_options().get("limit", DEFAULT_LIMIT)
        if isinstance(value, bool) or not isinstance(value, int):
            raise FetchError(
                f"engine_options.reddit.limit 应为整数(1-{MAX_LIMIT}),当前为 {value!r}",
                error_type="invalid_engine_options",
            )
        clamped = max(1, min(MAX_LIMIT, value))
        if clamped != value:
            logger.debug(
                "reddit limit=%s 超出 1-%s,钳制为 %s source=%s",
                value,
                MAX_LIMIT,
                clamped,
                self.source.name,
            )
        return clamped

    # ------------------------------------------------------- url & credentials

    def _parse_source_url(self) -> tuple[str, str]:
        """源 URL 契约校验(零 I/O):``https://oauth.reddit.com/r/<sub>/<listing>``.

        源 URL 的 query 一律忽略(limit/raw_json 由引擎全权构造,防止与
        engine_options 打架);host 必须精确匹配 API 宿主 —— 本引擎的解析器
        只认 Reddit JSON 形状,把引擎指到别站只会换来误导性解析错误。
        """
        parsed = urlsplit(self.source.url)
        host = (parsed.hostname or "").lower()
        if parsed.scheme != "https" or host != API_HOST:
            raise FetchError(
                f"reddit 引擎源 url 应为 https://{API_HOST}/r/<sub>/<listing> 形态,"
                f"当前为 {self.source.url!r}",
                error_type="invalid_reddit_source_url",
            )
        match = _SOURCE_PATH_RE.match(parsed.path)
        if match is None or match.group("listing") not in LISTINGS:
            raise FetchError(
                f"reddit 引擎源 url 路径应为 /r/<sub>/<listing>"
                f"(listing 取值 {'/'.join(LISTINGS)}),当前为 {parsed.path!r}",
                error_type="invalid_reddit_source_url",
            )
        return match.group("sub"), match.group("listing")

    def _credentials(self) -> tuple[str, str] | None:
        """解析 OAuth 凭据三态(见模块文档;None = 显式空态,由调用方落 skip)."""
        options = self.engine_options()
        id_ref = options.get("client_id")
        secret_ref = options.get("client_secret")
        if id_ref is None and secret_ref is None:
            return None
        if id_ref is None or secret_ref is None:
            raise FetchError(
                "engine_options.reddit.client_id 与 client_secret 须成对配置"
                "(env:/keychain: 引用):当前 "
                f"client_id={'已配' if id_ref is not None else '缺'} / "
                f"client_secret={'已配' if secret_ref is not None else '缺'}",
                error_type="invalid_engine_options",
            )
        for label, ref in (("client_id", id_ref), ("client_secret", secret_ref)):
            if not isinstance(ref, str):
                raise FetchError(
                    f"engine_options.reddit.{label} 应为 env:/keychain: 凭据引用"
                    f"字符串,当前为 {ref!r}",
                    error_type="invalid_engine_options",
                )
        try:
            client_id = resolve_credential(
                id_ref, backend=self.context.keychain_backend
            )
            client_secret = resolve_credential(
                secret_ref, backend=self.context.keychain_backend
            )
        except CredentialResolveError as exc:
            # 引用在而钥匙串未写/解析坏:空态 + warning 留痕(不静默;
            # credhunter lane 键同口径)。
            logger.warning(
                "reddit 凭据引用解析失败,源降级为显式空态 source=%s: %s",
                self.source.name,
                exc,
            )
            return None
        return client_id, client_secret

    # ----------------------------------------------------------------- fetch

    async def _fetch_impl(self) -> list[dict]:
        subreddit, listing = self._parse_source_url()
        limit = self._limit()
        credentials = self._credentials()
        if credentials is None:
            self.last_skip_reason = "credential_missing"
            logger.info(
                "reddit 引擎未配凭据,显式空态 source=%s(本轮零请求;"
                "myssia secret set myia/reddit/client-id 与"
                " myssia secret set myia/reddit/client-secret 写入钥匙串,"
                "再在 engine_options.reddit 配 client_id/client_secret 引用;"
                "app 注册:reddit.com/prefs/apps,script 型)",
                self.source.name,
            )
            return []
        client_id, client_secret = credentials
        token = await self._fetch_token(client_id, client_secret)
        response = await self._fetch_listing(token, subreddit, listing, limit)
        items = self._parse_listing(response, subreddit)
        logger.info(
            "reddit 列表取得 source=%s subreddit=r/%s listing=%s limit=%s items=%s",
            self.source.name,
            subreddit,
            listing,
            limit,
            len(items),
        )
        return items

    async def _fetch_token(self, client_id: str, client_secret: str) -> str:
        """OAuth2 client_credentials(userless)取 bearer token;无重试.

        单发直达(不骑 ``_send_with_retry``):form body 通道 + 「凭据坏
        重试无意义」—— 4xx 立即结构化失败,transport 抖动按结构化网络错误
        上报(每 run 每源一次的请求,重试收益不抵共享面的扩张)。
        Basic 头只在请求里;异常消息不含凭据(httpx 异常 str 只带 URL,
        token 端点无查询参数)。
        """
        basic = base64.b64encode(f"{client_id}:{client_secret}".encode()).decode()
        body = urlencode({"grant_type": "client_credentials", "device_id": DEVICE_ID})
        # 通用礼貌:限速照做(robots 面不适用 —— 授权 API 通道,见模块文档)。
        await self._acquire_rate_limit(TOKEN_ENDPOINT)
        try:
            response = await self._active_client.request(
                "POST",
                TOKEN_ENDPOINT,
                headers={
                    **self._headers,
                    "Authorization": f"Basic {basic}",
                    "Content-Type": "application/x-www-form-urlencoded",
                },
                content=body,
                timeout=self.context.timeout,
            )
        except httpx.TransportError as exc:
            raise FetchError(
                f"reddit OAuth token 请求网络失败 endpoint={TOKEN_ENDPOINT}: {exc}",
                error_type=classify_exception(exc),
            ) from self._wrap_proxy_transport_failure(exc)
        if response.status_code >= 400:
            raise FetchError(
                f"reddit OAuth token 请求 HTTP {response.status_code}"
                f" endpoint={TOKEN_ENDPOINT}: {response.reason_phrase}"
                "(凭据被拒常见于 client_id/secret 不符或 app 未注册)",
                error_type=f"http_{response.status_code}",
            )
        try:
            payload = response.json()
        except ValueError as exc:
            raise FetchError(
                f"reddit OAuth token 响应不是有效 JSON endpoint={TOKEN_ENDPOINT}: {exc}",
                error_type="json_decode",
            ) from exc
        token = payload.get("access_token") if isinstance(payload, dict) else None
        if not isinstance(token, str) or not token.strip():
            raise FetchError(
                f"reddit OAuth token 响应缺 access_token endpoint={TOKEN_ENDPOINT}",
                error_type="reddit_oauth_malformed",
            )
        return token

    async def _fetch_listing(
        self, token: str, subreddit: str, listing: str, limit: int
    ) -> httpx.Response:
        """GET 列表端点(Bearer;限速 + 既有重试退避;错误结构化脱敏)."""
        url = (
            f"https://{API_HOST}/r/{subreddit}/{listing}"
            f"?{urlencode({'limit': limit, 'raw_json': 1})}"
        )
        await self._acquire_rate_limit(url)
        try:
            return await self._send_with_retry(
                "GET",
                url,
                headers={**self._headers, "Authorization": f"Bearer {token}"},
            )
        except httpx.HTTPStatusError as exc:
            status = exc.response.status_code
            raise FetchError(
                f"reddit 列表请求 HTTP {status} endpoint=https://{API_HOST}"
                f" subreddit=r/{subreddit} listing={listing}: {exc.response.reason_phrase}"
                "(401 常见于 token 过期,本轮即弃即报,下一 run 重新取)",
                error_type=f"http_{status}",
            ) from exc

    # --------------------------------------------------------------- parsing

    def _parse_listing(self, response: httpx.Response, subreddit: str) -> list[dict]:
        """Reddit Listing JSON → 管线 items(url 必需;title/content 管线键).

        逐条目宽容:缺 permalink 的畸形 child 跳过(不废整源,同 rss 逐条目
        语义);published = ``created_utc``(epoch)转 ISO 8601 UTC;content =
        ``selftext``(非空才带,enrich credibility 消费)。
        """
        try:
            payload = response.json()
        except ValueError as exc:
            raise FetchError(
                f"reddit 列表响应不是有效 JSON subreddit=r/{subreddit}: {exc}",
                error_type="json_decode",
            ) from exc
        children = (
            payload.get("data", {}).get("children")
            if isinstance(payload, dict)
            else None
        )
        if not isinstance(children, list):
            raise FetchError(
                f"reddit 列表响应缺 data.children 数组 subreddit=r/{subreddit}",
                error_type="reddit_payload_malformed",
            )
        items: list[dict] = []
        for child in children:
            data = child.get("data") if isinstance(child, dict) else None
            if not isinstance(data, dict):
                continue
            permalink = data.get("permalink")
            if not isinstance(permalink, str) or not permalink.strip():
                continue
            item: dict[str, Any] = {
                "url": f"{PERMALINK_ORIGIN}{permalink}",
                "title": str(data.get("title") or ""),
            }
            created = data.get("created_utc")
            if isinstance(created, (int, float)) and not isinstance(created, bool):
                item["published"] = datetime.fromtimestamp(
                    created, tz=timezone.utc
                ).isoformat()
            author = data.get("author")
            if isinstance(author, str) and author:
                item["author"] = author
            for field in ("score", "num_comments"):
                value = data.get(field)
                if isinstance(value, (int, float)) and not isinstance(value, bool):
                    item[field] = value
            link = data.get("url")
            if isinstance(link, str) and link.startswith(("http://", "https://")):
                item["link"] = link
            selftext = data.get("selftext")
            if isinstance(selftext, str) and selftext.strip():
                item["content"] = selftext
            items.append(item)
        return items

    # ------------------------------------------------------- shape overrides

    def _check_pagination_support(self) -> None:
        """单页语义:任何 pagination 配置都结构化拒(不是只拒 scroll).

        Reddit 列表翻页是 cursor 语义(after/before),与模板/选择器/滚动
        三模式都不对应;单页 ``limit`` + 既有 run loop 的循环间隔是本引擎
        的定案形态(蓝本决议「单页小 limit、无重试风暴」)。
        """
        if self.source.pagination is not None:
            raise FetchError(
                "reddit 引擎是单页语义(limit 即条目帽,循环间隔由 run loop "
                "调度),不支持 pagination 配置",
                error_type="pagination_unsupported",
            )
