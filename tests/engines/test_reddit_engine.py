"""Tests for the Reddit official Data API engine (10-05-reddit-official-engine).

四态矩阵(design §5/AC6):

- **凭据缺失**:未配引用 / 引用在而钥匙串未写 → ``credential_missing``
  显式空态(items=[]、last_skip_reason 置位、**零请求**、人话指引留痕;
  registry 面 = skipped 源,不拦品类);
- **配置错误**:半配置 / 引用类型错 / limit 类型错 / ua_username 类型错 /
  源 URL 不符契约 / payload 形状坏 → 结构化 FetchError;
- **开启态**:MockTransport 往返(OAuth Basic+form body → Bearer 列表 GET →
  items 形状:url=permalink 绝对化 / published=ISO UTC / content=selftext);
- **注册表**:ENGINE_REGISTRY 在册、AUTO_CHAIN 七层原样、auto_degrade 单级
  链、schema ENGINES/EngineName 词表收录。

零真实网络(MockTransport)、零真实钥匙串(InMemoryKeychainBackend)、
零 robots 拉取(授权 API 通道,官方口径 "robots.txt is for search engines,
not Data API users";测试钉死请求序列里无 /robots.txt)。
"""

from __future__ import annotations

import base64
from datetime import datetime, timezone

import httpx
import pytest

from myssia import schema
from myssia.engines.fetch_base import FetchContext, FetchError
from myssia.engines.registry import (
    AUTO_CHAIN,
    ENGINE_REGISTRY,
    auto_degrade,
    fetch_source,
    resolve_engine,
)
from myssia.engines.reddit import DEFAULT_LIMIT, DEFAULT_UA, LISTINGS, RedditEngine
from myssia.schema import SourceConfig
from myssia.secrets import SECRET_SERVICE, InMemoryKeychainBackend

from conftest import make_client, make_context, make_source, run

SOURCE_URL = "https://oauth.reddit.com/r/MachineLearning/new"

TOKEN_OK = {"access_token": "tok-1", "token_type": "bearer", "expires_in": 3600}


def listing_payload(*datas: dict) -> dict:
    return {
        "kind": "Listing",
        "data": {"children": [{"kind": "t3", "data": d} for d in datas]},
    }


POST_DATA = {
    "title": "新模型发布:开源权重",
    "permalink": "/r/MachineLearning/comments/abc123/new_model/",
    "created_utc": 1761000000.0,
    "author": "alice",
    "score": 42,
    "num_comments": 7,
    "url": "https://example.com/paper.pdf",
    "selftext": "正文摘要,介绍模型结构。",
}
LINK_ONLY_DATA = {
    "title": "讨论:Scaling laws",
    "permalink": "/r/MachineLearning/comments/def456/scaling/",
    "created_utc": 1761000600.0,
    "url": "https://example.com/discussion",
    # 无 author/score/num_comments/selftext —— 缺字段逐条目省略(rss 同语义)
}


def reddit_client(
    captured: list,
    *,
    token_response: httpx.Response | None = None,
    listing_response: httpx.Response | None = None,
) -> httpx.AsyncClient:
    """双宿主 mock:www 宿主应答 token,oauth 宿主应答列表;其余一律失败.

    不经 ``make_handler`` 包装(它会自动应答 /robots.txt 掩盖零 robots 断言)。
    """

    def handler(request: httpx.Request) -> httpx.Response:
        captured.append(request)
        if (
            request.url.host == "www.reddit.com"
            and request.url.path == "/api/v1/access_token"
        ):
            if token_response is not None:
                return token_response
            return httpx.Response(200, json=TOKEN_OK)
        if request.url.host == "oauth.reddit.com":
            if listing_response is not None:
                return listing_response
            return httpx.Response(200, json=listing_payload(POST_DATA, LINK_ONLY_DATA))
        pytest.fail(f"意外请求(非官方端点):{request.url}")

    return make_client(handler)


def reddit_context(
    client: httpx.AsyncClient, *, with_credentials: bool = True
) -> FetchContext:
    """上下文 + 已写好 reddit 键的 mock 钥匙串(零真实 keychain 触碰)."""
    context, _ = make_context(client)
    if with_credentials:
        backend = InMemoryKeychainBackend()
        backend.set_password(SECRET_SERVICE, "myia/reddit/client-id", "cid-1")
        backend.set_password(SECRET_SERVICE, "myia/reddit/client-secret", "cs-1")
        context.keychain_backend = backend
    return context


def credential_refs() -> dict:
    return {
        "client_id": "keychain:myia/reddit/client-id",
        "client_secret": "keychain:myia/reddit/client-secret",
    }


def make_reddit_source(**overrides: object) -> SourceConfig:
    data: dict = {
        "name": "reddit-ml",
        "engine": "reddit",
        "url": SOURCE_URL,
        "engine_options": {"reddit": credential_refs()},
    }
    data.update(overrides)
    return SourceConfig.model_validate(data)


# ---------------------------------------------------------------------------
# 状态一:凭据缺失 = 显式空态(零请求)
# ---------------------------------------------------------------------------


def test_no_credentials_is_explicit_empty_state_zero_requests(caplog):
    """未配引用 → credential_missing 空态:零请求 + 人话指引 + skip 语义."""
    captured: list = []
    client = reddit_client(captured)
    context = reddit_context(client, with_credentials=False)
    source = SourceConfig.model_validate(
        {"name": "reddit-ml", "engine": "reddit", "url": SOURCE_URL}
    )

    engine = RedditEngine(source, context)
    with caplog.at_level("INFO", logger="myssia.engines.reddit"):
        items = run(engine.fetch())
    assert items == []
    assert engine.last_skip_reason == "credential_missing"
    assert captured == []  # 零请求:空态先于一切 I/O
    assert any(
        "myssia secret set myia/reddit/client-id" in r.getMessage()
        for r in caplog.records
    )


def test_unresolvable_keychain_ref_degrades_to_empty_state_with_warning(caplog):
    """引用在、钥匙串键未写 → 同空态 + warning 留痕(不静默吞配置问题)."""
    captured: list = []
    client = reddit_client(captured)
    context = reddit_context(client, with_credentials=False)  # 引用在,键没写
    context.keychain_backend = InMemoryKeychainBackend()
    engine = RedditEngine(make_reddit_source(), context)

    with caplog.at_level("WARNING", logger="myssia.engines.reddit"):
        items = run(engine.fetch())
    assert items == []
    assert engine.last_skip_reason == "credential_missing"
    assert captured == []
    assert any("解析失败" in r.getMessage() for r in caplog.records)


def test_env_reference_credentials_roundtrip(monkeypatch):
    """env: 引用形态同链可用(客户端_id 走 env、secret 走钥匙串的混合)."""
    monkeypatch.setenv("MYIA_REDDIT_CLIENT_ID", "cid-env")
    captured: list = []
    client = reddit_client(captured)
    context = reddit_context(client)
    source = make_reddit_source(
        engine_options={
            "reddit": {
                "client_id": "env:MYIA_REDDIT_CLIENT_ID",
                "client_secret": "keychain:myia/reddit/client-secret",
            }
        }
    )

    items = run(RedditEngine(source, context).fetch())
    assert len(items) == 2
    auth = captured[0].headers["Authorization"]
    assert auth == f"Basic {base64.b64encode(b'cid-env:cs-1').decode()}"


# ---------------------------------------------------------------------------
# 状态二:开启态 MockTransport 全链往返
# ---------------------------------------------------------------------------


def test_oauth_flow_and_listing_roundtrip():
    """OAuth client_credentials 全链:Basic+form body → Bearer 列表 GET → items."""
    captured: list = []
    client = reddit_client(captured)
    context = reddit_context(client)

    items = run(RedditEngine(make_reddit_source(), context).fetch())

    assert [request.method for request in captured] == ["POST", "GET"]
    token_req, list_req = captured
    # token 请求:官方端点 + Basic 凭据 + client_credentials form body
    assert str(token_req.url) == "https://www.reddit.com/api/v1/access_token"
    assert token_req.headers["Authorization"] == (
        f"Basic {base64.b64encode(b'cid-1:cs-1').decode()}"
    )
    assert token_req.headers["Content-Type"] == "application/x-www-form-urlencoded"
    assert "grant_type=client_credentials" in token_req.content.decode()
    assert "device_id=" in token_req.content.decode()
    # 列表请求:oauth 宿主 + Bearer + limit/raw_json 参数 + UA 硬格式
    assert str(list_req.url) == (
        f"https://oauth.reddit.com/r/MachineLearning/new?limit={DEFAULT_LIMIT}&raw_json=1"
    )
    assert list_req.headers["Authorization"] == "Bearer tok-1"
    assert list_req.headers["User-Agent"] == DEFAULT_UA
    # items:管线契约(url/title/content 管线键,其余 metadata)
    assert items[0] == {
        "url": "https://www.reddit.com/r/MachineLearning/comments/abc123/new_model/",
        "title": "新模型发布:开源权重",
        "published": datetime.fromtimestamp(
            POST_DATA["created_utc"], tz=timezone.utc
        ).isoformat(),
        "author": "alice",
        "score": 42,
        "num_comments": 7,
        "link": "https://example.com/paper.pdf",
        "content": "正文摘要,介绍模型结构。",
    }
    # 缺字段条目逐项省略(rss 逐条目语义),url/title 恒在
    assert items[1] == {
        "url": "https://www.reddit.com/r/MachineLearning/comments/def456/scaling/",
        "title": "讨论:Scaling laws",
        "published": datetime.fromtimestamp(
            LINK_ONLY_DATA["created_utc"], tz=timezone.utc
        ).isoformat(),
        "link": "https://example.com/discussion",
    }


def test_token_fetched_once_per_fetch():
    """单源单次 fetch 只取一次 token(实例内复用,无重复 OAuth)."""
    captured: list = []
    client = reddit_client(captured)
    context = reddit_context(client)

    items = run(RedditEngine(make_reddit_source(), context).fetch())
    assert len(items) == 2
    assert sum(1 for r in captured if r.url.path == "/api/v1/access_token") == 1


def test_listing_and_limit_options_apply():
    """listing 取自 URL 路径;limit 选项透传进查询串."""
    captured: list = []
    client = reddit_client(captured)
    context = reddit_context(client)
    source = make_reddit_source(
        url="https://oauth.reddit.com/r/Games/hot",
        engine_options={"reddit": {**credential_refs(), "limit": 50}},
    )

    run(RedditEngine(source, context).fetch())
    assert (
        str(captured[1].url)
        == "https://oauth.reddit.com/r/Games/hot?limit=50&raw_json=1"
    )


@pytest.mark.parametrize("limit", [0, 500])
def test_limit_out_of_range_is_clamped(limit):
    """limit 超出 1-100 → 钳制到边界(上游本会截断,先钳可见)."""
    captured: list = []
    client = reddit_client(captured)
    context = reddit_context(client)
    source = make_reddit_source(
        engine_options={"reddit": {**credential_refs(), "limit": limit}}
    )

    run(RedditEngine(source, context).fetch())
    expected = 1 if limit == 0 else 100
    assert captured[1].url.params["limit"] == str(expected)


def test_source_url_query_is_ignored():
    """源 URL 手拼的 query 被忽略(limit/raw_json 由引擎全权构造)."""
    captured: list = []
    client = reddit_client(captured)
    context = reddit_context(client)
    source = make_reddit_source(url="https://oauth.reddit.com/r/x/new?limit=99&foo=bar")

    run(RedditEngine(source, context).fetch())
    assert str(captured[1].url) == (
        f"https://oauth.reddit.com/r/x/new?limit={DEFAULT_LIMIT}&raw_json=1"
    )


def test_multi_subreddit_path_passes_through():
    """r/a+b 多 sub 形态原样放行(Reddit 官方支持)."""
    captured: list = []
    client = reddit_client(captured)
    context = reddit_context(client)
    source = make_reddit_source(url="https://oauth.reddit.com/r/foo+bar/new")

    run(RedditEngine(source, context).fetch())
    assert captured[1].url.path == "/r/foo+bar/new"


# ---------------------------------------------------------------------------
# UA 政策(Reddit 条款硬格式)
# ---------------------------------------------------------------------------


def test_ua_username_appends_by_segment():
    """ua_username 配置 → UA 拼 (by /u/<name>) 段;不带则缺省无段."""
    captured: list = []
    client = reddit_client(captured)
    context = reddit_context(client)
    source = make_reddit_source(
        engine_options={"reddit": {**credential_refs(), "ua_username": "somebody"}}
    )

    run(RedditEngine(source, context).fetch())
    assert captured[1].headers["User-Agent"] == f"{DEFAULT_UA} (by /u/somebody)"


def test_source_level_user_agent_header_wins():
    """源级 headers.User-Agent 显式配置 = 最高优先级(完整覆盖)."""
    captured: list = []
    client = reddit_client(captured)
    context = reddit_context(client)
    source = make_reddit_source(
        headers={"User-Agent": "web:my-custom-app:2.0 (by /u/custom)"}
    )

    run(RedditEngine(source, context).fetch())
    assert captured[1].headers["User-Agent"] == "web:my-custom-app:2.0 (by /u/custom)"


# ---------------------------------------------------------------------------
# 状态三:结构化错误面(零凭据外泄)
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    ("url", "label"),
    [
        ("https://www.reddit.com/r/x/new", "宿主非 oauth API 宿主"),
        ("http://oauth.reddit.com/r/x/new", "非 https"),
        ("https://oauth.reddit.com/search?q=x", "路径非 r/<sub>/<listing>"),
        ("https://oauth.reddit.com/r/x/best", "listing 词表外"),
        ("https://oauth.reddit.com/r/x", "缺 listing 段"),
    ],
)
def test_bad_source_url_is_structured_rejection(url, label):
    """源 URL 不符契约 → invalid_reddit_source_url,零请求(先于凭据检查)."""
    captured: list = []
    client = reddit_client(captured)
    context = reddit_context(client)
    engine = RedditEngine(make_reddit_source(url=url), context)

    with pytest.raises(FetchError) as excinfo:
        run(engine.fetch())
    assert excinfo.value.error_type == "invalid_reddit_source_url", label
    assert captured == []


def test_half_configured_credentials_rejected():
    """半配置(只配一只)→ 结构化拒,不是空态(漏写一半是配置错误)."""
    captured: list = []
    client = reddit_client(captured)
    context = reddit_context(client)
    source = make_reddit_source(
        engine_options={"reddit": {"client_id": "keychain:myia/reddit/client-id"}}
    )

    with pytest.raises(FetchError) as excinfo:
        run(RedditEngine(source, context).fetch())
    assert excinfo.value.error_type == "invalid_engine_options"
    assert captured == []


@pytest.mark.parametrize(
    ("options", "label"),
    [
        ({"limit": "25"}, "limit 字符串"),
        ({"ua_username": 42}, "ua_username 非字符串"),
        (
            {"client_id": 123, "client_secret": "keychain:myia/reddit/client-secret"},
            "引用非字符串",
        ),
    ],
)
def test_option_type_errors_are_structured(options, label):
    """参数面类型错 → 结构化拒,零请求."""
    captured: list = []
    client = reddit_client(captured)
    context = reddit_context(client)
    source = make_reddit_source(
        engine_options={"reddit": {**credential_refs(), **options}}
    )

    with pytest.raises(FetchError) as excinfo:
        run(RedditEngine(source, context).fetch())
    assert excinfo.value.error_type == "invalid_engine_options", label
    assert captured == []


def test_oauth_http_401_is_structured_and_leaks_no_credentials():
    """OAuth 401(凭据被拒)→ http_401 结构化失败;消息零凭据值."""
    captured: list = []
    client = reddit_client(
        captured, token_response=httpx.Response(401, text="bad creds")
    )
    context = reddit_context(client)

    with pytest.raises(FetchError) as excinfo:
        run(RedditEngine(make_reddit_source(), context).fetch())
    assert excinfo.value.error_type == "http_401"
    message = str(excinfo.value)
    assert "cid-1" not in message and "cs-1" not in message
    assert "https://www.reddit.com/api/v1/access_token" in message  # 端点常量可入消息


def test_oauth_token_response_without_token_is_malformed():
    """token 200 但缺 access_token → reddit_oauth_malformed."""
    captured: list = []
    client = reddit_client(
        captured, token_response=httpx.Response(200, json={"error": "weird"})
    )
    context = reddit_context(client)

    with pytest.raises(FetchError) as excinfo:
        run(RedditEngine(make_reddit_source(), context).fetch())
    assert excinfo.value.error_type == "reddit_oauth_malformed"


def test_listing_http_403_is_structured():
    """列表 403(token 失效/无权)→ http_403 结构化失败."""
    captured: list = []
    client = reddit_client(
        captured, listing_response=httpx.Response(403, text="forbidden")
    )
    context = reddit_context(client)

    with pytest.raises(FetchError) as excinfo:
        run(RedditEngine(make_reddit_source(), context).fetch())
    assert excinfo.value.error_type == "http_403"
    assert "r/MachineLearning" in str(excinfo.value)


def test_listing_payload_without_children_is_malformed():
    """列表 JSON 缺 data.children → reddit_payload_malformed(形状错可见)."""
    captured: list = []
    client = reddit_client(
        captured, listing_response=httpx.Response(200, json={"error": 404})
    )
    context = reddit_context(client)

    with pytest.raises(FetchError) as excinfo:
        run(RedditEngine(make_reddit_source(), context).fetch())
    assert excinfo.value.error_type == "reddit_payload_malformed"


def test_listing_non_json_is_json_decode():
    """列表响应非 JSON → json_decode(direct_api 同款失败类)."""
    captured: list = []
    client = reddit_client(
        captured, listing_response=httpx.Response(200, text="<html>")
    )
    context = reddit_context(client)

    with pytest.raises(FetchError) as excinfo:
        run(RedditEngine(make_reddit_source(), context).fetch())
    assert excinfo.value.error_type == "json_decode"


def test_extract_config_is_rejected():
    """内置解析引擎,extract 配置 = 错配可见(credhunter 同款)."""
    captured: list = []
    client = reddit_client(captured)
    context = reddit_context(client)
    source = make_reddit_source(
        extract={"type": "json_path", "fields": {"url": "$.url"}}
    )

    with pytest.raises(FetchError) as excinfo:
        run(RedditEngine(source, context).fetch())
    assert excinfo.value.error_type == "extract_unsupported"
    assert captured == []


def test_pagination_config_is_rejected():
    """单页语义:任何 pagination 配置拒(不是只拒 scroll)."""
    captured: list = []
    client = reddit_client(captured)
    context = reddit_context(client)
    source = make_reddit_source(pagination={"mode": "scroll"})

    with pytest.raises(FetchError) as excinfo:
        run(RedditEngine(source, context).fetch())
    assert excinfo.value.error_type == "pagination_unsupported"
    assert captured == []


def test_malformed_children_entries_are_skipped_not_fatal():
    """畸形 child(非 dict/缺 permalink)逐条跳过,不废整源."""
    payload = {
        "kind": "Listing",
        "data": {
            "children": [{"kind": "t3", "data": POST_DATA}, "junk", {"no": "data"}]
        },
    }
    captured: list = []
    client = reddit_client(captured, listing_response=httpx.Response(200, json=payload))
    context = reddit_context(client)

    items = run(RedditEngine(make_reddit_source(), context).fetch())
    assert len(items) == 1
    assert items[0]["title"] == POST_DATA["title"]


# ---------------------------------------------------------------------------
# robots 面:授权 API 通道零 robots 拉取(官方口径,B6 为据)
# ---------------------------------------------------------------------------


def test_no_robots_txt_fetch_on_any_host():
    """全链请求序列里零 /robots.txt(引擎不经 _ensure_robots_allowed)."""
    captured: list = []
    client = reddit_client(captured)
    context = reddit_context(client)

    run(RedditEngine(make_reddit_source(), context).fetch())
    assert all(request.url.path != "/robots.txt" for request in captured)
    assert len(captured) == 2  # 恰好 token + 列表两次


# ---------------------------------------------------------------------------
# 状态四:注册表与词表(链外三锁 + schema 双锁)+ registry 集成
# ---------------------------------------------------------------------------


def test_registry_offchain_locks():
    """在册 + 不在链 + AUTO_CHAIN 七层原样 + 单级链 + resolve."""
    assert "reddit" in ENGINE_REGISTRY
    assert "reddit" not in AUTO_CHAIN
    assert AUTO_CHAIN == (
        "direct_api",
        "static_html",
        "crawl4ai",
        "firecrawl",
        "scrapling",
        "stealth_browser",
        "llm_browser",
    )
    assert resolve_engine("reddit") is RedditEngine
    assert auto_degrade("reddit") == ["reddit"]


def test_schema_vocabulary_accepts_reddit():
    """schema 双锁:ENGINES 词表 + SourceConfig 可显式选用."""
    assert "reddit" in schema.ENGINES
    source = SourceConfig.model_validate(
        {"name": "demo", "url": SOURCE_URL, "engine": "reddit"}
    )
    assert source.engine == "reddit"


def test_fetch_source_registry_empty_state_is_skip_not_failure():
    """registry 集成:credential_missing = skipped 源(非 failures),不拦品类."""
    client = reddit_client([])
    context = reddit_context(client, with_credentials=False)
    source = SourceConfig.model_validate(
        {"name": "demo", "url": SOURCE_URL, "engine": "reddit"}
    )

    outcome = run(fetch_source(source, context))
    assert outcome.engine == "reddit"
    assert outcome.skipped is True
    assert outcome.skip_reason == "credential_missing"
    assert outcome.items == []
    assert outcome.failures == []  # 空态不是引擎失败


def test_fetch_source_registry_happy_path_records_engine():
    """registry 集成:开启态经 hint 回写引擎名、items 正常流转."""
    client = reddit_client([])
    context = reddit_context(client)

    outcome = run(fetch_source(make_reddit_source(), context))
    assert outcome.engine == "reddit"
    assert outcome.skipped is False
    assert len(outcome.items) == 2


def test_listing_vocabulary_constant():
    """listing 词表钉死(new/hot/rising/top)——防未来漂移的锚."""
    assert LISTINGS == ("new", "hot", "rising", "top")
