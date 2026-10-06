"""Tests for the SearXNG self-hosted metasearch engine (10-05-source-searxng).

八用例(夹具蓝本 = 探查实快照 ``.trellis/tasks/10-05-source-searxng/
evidence/2026-10-06-search-web-zhcn.json``:55 条 / 35 default.html +
20 images.html / 七顶层键 / 23 键骨架):

1. 正常解析 55 条形状:template 过滤后 35 条,字段映射 + 请求形状
   (format=json&language=zh-CN&safesearch=1&pageno=1&categories=web,
   常发 Accept-Language);
2. 空态:零结果(unresponsive 全灭)→ items=[] 不炸不 skip;
3. 分页:每词固定 pageno=1 一发;pagination 配置结构化拒;
4. 坏 JSON / 坏形状:HTML 403 页 → http_403 文案指 settings.yml;
   200 非 JSON → json_decode;results 非数组 → searxng_payload_malformed;
5. base_url 三级解析:缺省 127.0.0.1:8888 / env MYIA_SEARXNG_URL 覆盖 /
   源级 searxng_base_url 最高优先;
6. 礼貌参数:逐词串行 + 词间 query_delay(缺省 3s)+ per-host 限速;
7. (10-06 轨B/G-Q5)就绪探测:loopback 未启动 → searxng_service_not_running
   「服务组件未启动」+设置页引导,零 /search 流量,不隐式拉起;远端未起 →
   network「实例未起」;探测放行(200/404 皆可)= 实例在;
8. schema 装载校验(engine=searxng 时 queries 必填)。

零真实网络(MockTransport)。robots 不查(自家实例自授权通道,模块文档
论证;测试钉死请求序列里无 /robots.txt)。
"""

from __future__ import annotations

import httpx
import pytest

from myssia import schema
from myssia.engines.fetch_base import FetchContext, FetchError
from myssia.engines.registry import (
    AUTO_CHAIN,
    ENGINE_REGISTRY,
    auto_degrade,
    resolve_engine,
)
from myssia.engines.searxng import (
    DEFAULT_QUERY_DELAY_SECONDS,
    DEFAULT_SEARXNG_BASE_URL,
    ENV_SEARXNG_URL,
    HEALTHZ_PATH,
    SearxngEngine,
)
from myssia.schema import LoadError, SourceConfig, load_category

from conftest import make_client, make_context, make_source, run

QUERIES = ["人工智能 监管", "数据泄露 事件 通报"]


def searxng_result(url: str, title: str, *, template: str = "default.html") -> dict:
    """一条 results[] 元素 —— 字段集对齐实快照 23 键骨架(research §2.3)."""
    return {
        "template": template,
        "title": title,
        "content": f"{title}的摘要文本,可空串。",
        "img_src": "",
        "iframe_src": "",
        "audio_src": "",
        "thumbnail": "",
        "publishedDate": None,
        "pubdate": "",
        "length": None,
        "views": "",
        "author": "",
        "metadata": "",
        "priority": "",
        "engines": ["naver"],
        "open_group": False,
        "close_group": False,
        "positions": [1],
        "score": 1.0,
        "category": "general",
        "url": url,
        "engine": "naver",
        "parsed_url": ["https", "example.org", "/p", "", "", ""],
    }


def web_payload(n_default: int = 35, n_images: int = 20) -> dict:
    """实快照形状的响应体:55 条 = 35 default.html + 20 images.html."""
    results = [
        searxng_result(
            f"https://example.org/p/{index}",
            f"第 {index} 条:人工智能安全监管制度的现实路径",
        )
        for index in range(n_default)
    ]
    results += [
        searxng_result(
            f"https://example.org/img/{index}.png",
            f"图片行 {index}",
            template="images.html",
        )
        for index in range(n_images)
    ]
    return {
        "query": "人工智能 监管",
        "results": results,
        "answers": [],
        "corrections": [],
        "infoboxes": [],
        "suggestions": [],
        "unresponsive_engines": [["brave", "Suspended: too many requests"]],
    }


ZERO_PAYLOAD = {  # evidence/2026-10-06-search-default-general-zero.json 原样形状
    "query": "人工智能 监管",
    "results": [],
    "answers": [],
    "corrections": [],
    "infoboxes": [],
    "suggestions": [],
    "unresponsive_engines": [
        ["brave", "timeout"],
        ["duckduckgo", "CAPTCHA"],
        ["google cse", "timeout"],
        ["wikidata", "timeout"],
        ["wikipedia", "timeout"],
    ],
}


def searxng_handler(
    captured: list[httpx.Request],
    responder=None,
    probes: list[httpx.Request] | None = None,
) -> httpx.AsyncClient:
    """单宿主 mock:一切 /search 走 responder;/healthz 就绪探测恒 200(计入
    probes 独立记账,不混入搜索流量断言);其余请求一律失败(零 robots)."""

    def handler(request: httpx.Request) -> httpx.Response:
        if request.url.path == f"/{HEALTHZ_PATH}":
            if probes is not None:
                probes.append(request)
            return httpx.Response(200, text="OK")
        captured.append(request)
        if request.url.path == "/search":
            if responder is not None:
                return responder(request)
            return httpx.Response(200, json=web_payload())
        pytest.fail(
            f"意外请求(引擎只应打 /search 与 /healthz,且不查 robots):{request.url}"
        )

    return make_client(handler)


def searxng_context(client: httpx.AsyncClient) -> tuple[FetchContext, object]:
    """silent limiter 上下文:clock.sleeps 只记引擎的词间 delay."""
    return make_context(client, silent_limiter=True)


def make_searxng_source(**overrides: object) -> SourceConfig:
    data: dict = {
        "name": "searxng-watch",
        "engine": "searxng",
        "url": "http://127.0.0.1:8888",
        "queries": list(QUERIES),
        "retry": 0,
    }
    data.update(overrides)
    return SourceConfig.model_validate(data)


# ---------------------------------------------------------------------------
# 用例一:正常解析 55 条形状(实快照蓝本)
# ---------------------------------------------------------------------------


def test_parses_snapshot_shape_55_results_filters_images():
    """55 条实快照形状 → 35 条 default.html 条目;字段映射与请求形状对账."""
    captured: list[httpx.Request] = []
    client = searxng_handler(captured)
    context, _clock = searxng_context(client)
    source = make_searxng_source()

    engine = SearxngEngine(source, context)
    items = run(engine.fetch())

    assert len(items) == 70  # 2 词 × 35 条 default.html(55-20 images,实测定案过滤)
    assert all(item["query"] == QUERIES[0] for item in items[:35])
    assert all(item["query"] == QUERIES[1] for item in items[35:])
    first = items[0]
    assert first["url"] == "https://example.org/p/0"
    assert first["title"] == "第 0 条:人工智能安全监管制度的现实路径"
    assert first["content"].startswith("第 0 条")
    assert first["query"] == QUERIES[0]
    assert "published" not in first  # publishedDate=null(实测 web 池常态)
    assert engine.last_skip_reason is None

    # 请求形状:逐词两发,参数集对 research §9-1 定案逐项对账。
    assert len(captured) == 2
    for request, query in zip(captured, QUERIES):
        assert request.url.host == "127.0.0.1" and request.url.port == 8888
        assert request.url.params["q"] == query
        assert request.url.params["format"] == "json"
        assert request.url.params["language"] == "zh-CN"
        assert request.url.params["safesearch"] == "1"
        assert request.url.params["pageno"] == "1"
        assert request.url.params["categories"] == "web"
        # 常发 Accept-Language(limiter-on 实例一行头即过;limiter-off 无害)
        assert request.headers["accept-language"] == "zh-CN,zh;q=0.9"
    # 查询词间串行:两词按声明序各自一发。
    assert [request.url.params["q"] for request in captured] == QUERIES


def test_published_date_passthrough_when_present():
    """publishedDate 非空 isoformat 透传(实测 web 池多 null,有则带上)."""
    payload = web_payload(n_default=1, n_images=0)
    payload["results"][0]["publishedDate"] = "2026-10-01T08:00:00+00:00"

    captured: list[httpx.Request] = []
    client = searxng_handler(
        captured, responder=lambda _r: httpx.Response(200, json=payload)
    )
    context, _clock = searxng_context(client)
    source = make_searxng_source(queries=["单词"])

    items = run(SearxngEngine(source, context).fetch())
    assert len(items) == 1
    assert items[0]["published"] == "2026-10-01T08:00:00+00:00"


def test_bad_rows_skipped_not_fatal():
    """坏行(缺 url / 空 title / 非字典)逐条跳过,不废整源(rss 同语义)."""
    payload = {
        "query": "q",
        "results": [
            searxng_result("https://example.org/ok", "正常条目"),
            {"title": "缺 url 的行"},
            searxng_result("", "url 为空串"),
            searxng_result("https://example.org/no-title", "  "),
            "not-a-dict",
            searxng_result("https://example.org/none-template", "无 template 键"),
        ],
        "answers": [],
        "corrections": [],
        "infoboxes": [],
        "suggestions": [],
        "unresponsive_engines": [],
    }
    captured: list[httpx.Request] = []
    client = searxng_handler(
        captured, responder=lambda _r: httpx.Response(200, json=payload)
    )
    context, _clock = searxng_context(client)
    source = make_searxng_source(queries=["q"])

    items = run(SearxngEngine(source, context).fetch())
    assert [item["url"] for item in items] == [
        "https://example.org/ok",
        "https://example.org/none-template",  # template 缺失 = 容忍(default 语义)
    ]


# ---------------------------------------------------------------------------
# 用例二:空态(零结果不炸)
# ---------------------------------------------------------------------------


def test_zero_results_is_legitimate_empty_not_skip():
    """引擎全灭(unresponsive 非空)→ 200 + results:[] → items=[] 正常空态."""
    captured: list[httpx.Request] = []
    client = searxng_handler(
        captured, responder=lambda _r: httpx.Response(200, json=ZERO_PAYLOAD)
    )
    context, _clock = searxng_context(client)
    source = make_searxng_source()

    engine = SearxngEngine(source, context)
    items = run(engine.fetch())
    assert items == []
    assert engine.last_skip_reason is None  # 搜索没结果是常态,不是 skip/错误


# ---------------------------------------------------------------------------
# 用例三:分页语义(固定 pageno=1;pagination 配置拒)
# ---------------------------------------------------------------------------


def test_fixed_pageno_one_page_per_query():
    """每词固定 pageno=1 一发(research §3/§9-3 定案:深页放大上游)."""
    captured: list[httpx.Request] = []
    client = searxng_handler(captured)
    context, _clock = searxng_context(client)
    source = make_searxng_source(queries=["词一", "词二", "词三"])

    run(SearxngEngine(source, context).fetch())
    assert len(captured) == 3
    assert all(request.url.params["pageno"] == "1" for request in captured)


def test_pagination_config_structurally_rejected():
    """单页语义:任何 pagination 配置结构化拒(reddit/urlwatch 先例)."""
    client = searxng_handler([])
    context, _clock = searxng_context(client)
    source = SourceConfig.model_validate(
        {
            "name": "searxng-watch",
            "engine": "searxng",
            "url": "http://127.0.0.1:8888/search?q=x&page={page}",
            "queries": list(QUERIES),
            "pagination": {"mode": "template", "max_pages": 2},
        }
    )

    with pytest.raises(FetchError) as excinfo:
        run(SearxngEngine(source, context).fetch())
    assert excinfo.value.error_type == "pagination_unsupported"


# ---------------------------------------------------------------------------
# 用例四:坏 JSON / 坏形状的结构化错误面
# ---------------------------------------------------------------------------


def test_403_html_page_gets_json_format_hint():
    """未开 json 的 403(Flask HTML 页)→ http_403,文案直指 settings.yml."""
    captured: list[httpx.Request] = []
    client = searxng_handler(
        captured,
        responder=lambda _r: httpx.Response(
            403,
            text="<html><body>Forbidden</body></html>",
            headers={"content-type": "text/html"},
        ),
    )
    context, _clock = searxng_context(client)
    source = make_searxng_source(queries=["q"])

    with pytest.raises(FetchError) as excinfo:
        run(SearxngEngine(source, context).fetch())
    assert excinfo.value.error_type == "http_403"
    assert "search.formats" in str(excinfo.value)


def test_429_gets_limiter_hint_and_400_passes_error_field():
    """429 → limiter 口径提示;400 → 透传响应体 error 字段(实测形态)."""
    for status, expected in ((429, "Accept-Language"), (400, "No query")):
        captured: list[httpx.Request] = []
        client = searxng_handler(
            captured,
            responder=lambda _r: httpx.Response(status, json={"error": "No query"}),
        )
        context, _clock = searxng_context(client)
        source = make_searxng_source(queries=["q"])

        with pytest.raises(FetchError) as excinfo:
            run(SearxngEngine(source, context).fetch())
        assert excinfo.value.error_type == f"http_{status}"
        assert expected in str(excinfo.value)


def test_non_json_body_structured_json_decode():
    """200 但非 JSON → json_decode 结构化错."""
    captured: list[httpx.Request] = []
    client = searxng_handler(
        captured, responder=lambda _r: httpx.Response(200, text="not json at all")
    )
    context, _clock = searxng_context(client)
    source = make_searxng_source(queries=["q"])

    with pytest.raises(FetchError) as excinfo:
        run(SearxngEngine(source, context).fetch())
    assert excinfo.value.error_type == "json_decode"


def test_payload_without_results_array_rejected():
    """200 JSON 但缺 results 数组 → searxng_payload_malformed."""
    captured: list[httpx.Request] = []
    client = searxng_handler(
        captured, responder=lambda _r: httpx.Response(200, json={"query": "q"})
    )
    context, _clock = searxng_context(client)
    source = make_searxng_source(queries=["q"])

    with pytest.raises(FetchError) as excinfo:
        run(SearxngEngine(source, context).fetch())
    assert excinfo.value.error_type == "searxng_payload_malformed"


def test_dead_instance_transport_error_structured(monkeypatch):
    """transport 失败分岔(轨B G-Q5 就绪探测先拦):

    - loopback base(=本机壳服务组件实例)→ ``searxng_service_not_running``
      「服务组件未启动」+ 设置页引导;零 /search 流量(探测不过不放查询)。
    - 远端 base → 既有 network「实例未起」分类(firecrawl 口径不变)。
    """

    # loopback:连接拒绝 → 服务组件未启动(引导设置页,不隐式拉起)
    def handler(request: httpx.Request) -> httpx.Response:
        raise httpx.ConnectError("[Errno 61] Connection refused", request=request)

    client = make_client(handler)
    context, _clock = searxng_context(client)
    source = make_searxng_source(queries=["q"], retry=0)

    with pytest.raises(FetchError) as excinfo:
        run(SearxngEngine(source, context).fetch())
    assert excinfo.value.error_type == "searxng_service_not_running"
    assert "服务组件未启动" in str(excinfo.value)
    assert "设置" in str(excinfo.value) and "启动" in str(excinfo.value)
    assert "不隐式拉起" in str(excinfo.value)

    # 远端实例:同样的连接拒绝 → network「实例未起」(部署侧引导)
    source = make_searxng_source(
        queries=["q"], retry=0, searxng_base_url="http://192.168.1.10:8888"
    )
    with pytest.raises(FetchError) as excinfo:
        run(SearxngEngine(source, context).fetch())
    assert excinfo.value.error_type == "network"
    assert "实例未起" in str(excinfo.value)


def test_readiness_probe_passes_then_searches_run_and_tolerates_4xx_healthz():
    """就绪探测放行语义:① /healthz 200 → 放行 /search(既有流量断言的
    探测前提);② /healthz 404(老实例无该路由)= 实例在,照样放行——
    探测只判「有没有起来」,健康语义归设置卡绿点。"""

    probes: list[httpx.Request] = []
    captured: list[httpx.Request] = []
    client = searxng_handler(captured, probes=probes)
    context, _clock = searxng_context(client)
    source = make_searxng_source(queries=["q"])

    items = run(SearxngEngine(source, context).fetch())
    assert len(captured) == 1  # 一发 /search(流量断言不混探测)
    assert len(probes) == 1  # 探测恰一发,无重试预算放大
    assert probes[0].url.path == f"/{HEALTHZ_PATH}"
    assert items  # 放行后正常解析

    # 404 老实例形态:探测应答 404 → 仍在,放行
    def health_404(request: httpx.Request) -> httpx.Response:
        if request.url.path == f"/{HEALTHZ_PATH}":
            return httpx.Response(404, text="not found")
        if request.url.path == "/search":
            return httpx.Response(200, json=web_payload(n_default=2, n_images=0))
        pytest.fail(f"意外请求:{request.url}")

    client404 = make_client(health_404)
    context404, _clock = searxng_context(client404)
    items = run(SearxngEngine(source, context404).fetch())
    assert len(items) == 2  # 404 = 实例在,搜索照常


# ---------------------------------------------------------------------------
# 用例五:base_url 三级解析(缺省 / env / 源级)
# ---------------------------------------------------------------------------


def test_default_base_url_when_unconfigured(monkeypatch):
    """缺省态:无源级键、无 env → 内置 http://127.0.0.1:8888(firecrawl 先例)."""
    monkeypatch.delenv(ENV_SEARXNG_URL, raising=False)
    captured: list[httpx.Request] = []
    client = searxng_handler(captured)
    context, _clock = searxng_context(client)
    source = make_searxng_source(queries=["q"])

    run(SearxngEngine(source, context).fetch())
    assert captured[0].url.host == "127.0.0.1"
    assert captured[0].url.port == 8888


def test_env_overrides_default(monkeypatch):
    """env MYIA_SEARXNG_URL 覆盖内置缺省(部署迁移只改 env,research §9-5)."""
    monkeypatch.setenv(ENV_SEARXNG_URL, "http://192.168.1.10:8888")
    captured: list[httpx.Request] = []
    client = searxng_handler(captured)
    context, _clock = searxng_context(client)
    source = make_searxng_source(queries=["q"])

    run(SearxngEngine(source, context).fetch())
    assert captured[0].url.host == "192.168.1.10"
    assert captured[0].url.port == 8888


def test_source_level_base_url_wins_over_env(monkeypatch):
    """源级 searxng_base_url 最高优先;尾斜杠剥掉;坏形态结构化拒."""
    monkeypatch.setenv(ENV_SEARXNG_URL, "http://192.168.1.10:8888")
    captured: list[httpx.Request] = []
    client = searxng_handler(captured)
    context, _clock = searxng_context(client)
    source = make_searxng_source(
        queries=["q"], searxng_base_url="http://10.0.0.2:9999/"
    )

    run(SearxngEngine(source, context).fetch())
    assert captured[0].url.host == "10.0.0.2"
    assert captured[0].url.port == 9999

    bad = make_searxng_source(queries=["q"], searxng_base_url="not-a-url")
    with pytest.raises(FetchError) as excinfo:
        run(SearxngEngine(bad, searxng_context(client)[0]).fetch())
    assert excinfo.value.error_type == "invalid_searxng_base_url"


# ---------------------------------------------------------------------------
# 用例六:礼貌参数(逐词串行 + 词间延时 + 限速)
# ---------------------------------------------------------------------------


def test_politeness_serial_queries_with_inter_query_delay():
    """逐词串行 + 词间 query_delay(缺省 3s,silent limiter 下 clock 只记它)."""
    captured: list[httpx.Request] = []
    client = searxng_handler(captured)
    context, clock = searxng_context(client)
    source = make_searxng_source(queries=["词一", "词二", "词三"])

    run(SearxngEngine(source, context).fetch())
    # 词间断言:3 词 = 2 次 delay,每次缺省 3s(探查纪律同款)。
    assert clock.sleeps == [DEFAULT_QUERY_DELAY_SECONDS, DEFAULT_QUERY_DELAY_SECONDS]


def test_query_delay_zero_disables_but_type_checked():
    """query_delay=0 显式关(测试/自家专用实例);类型错结构化拒."""
    captured: list[httpx.Request] = []
    client = searxng_handler(captured)
    context, clock = searxng_context(client)
    source = make_searxng_source(
        queries=["词一", "词二"],
        engine_options={"searxng": {"query_delay": 0}},
    )
    run(SearxngEngine(source, context).fetch())
    assert clock.sleeps == []

    bad = make_searxng_source(
        queries=["q"], engine_options={"searxng": {"query_delay": "3"}}
    )
    with pytest.raises(FetchError) as excinfo:
        run(SearxngEngine(bad, searxng_context(client)[0]).fetch())
    assert excinfo.value.error_type == "invalid_engine_options"


# ---------------------------------------------------------------------------
# 配置错配与注册表/schema 面
# ---------------------------------------------------------------------------


def test_extract_config_is_structural_mismatch():
    """内置 JSON 解析:extract 节配置即结构化拒(reddit 先例)."""
    client = searxng_handler([])
    context, _clock = searxng_context(client)
    source = SourceConfig.model_validate(
        {
            "name": "searxng-watch",
            "engine": "searxng",
            "url": "http://127.0.0.1:8888",
            "queries": ["q"],
            "extract": {"type": "json_path", "fields": {"url": "$.results[*].url"}},
        }
    )
    with pytest.raises(FetchError) as excinfo:
        run(SearxngEngine(source, context).fetch())
    assert excinfo.value.error_type == "extract_unsupported"


def test_registry_off_chain_and_schema_vocabulary():
    """链外注册:ENGINE_REGISTRY 在册、AUTO_CHAIN 原样、auto_degrade 单级链;
    schema ENGINES/EngineName 词表收录(anti-drift 面)。"""
    assert "searxng" in ENGINE_REGISTRY
    assert "searxng" not in AUTO_CHAIN  # 搜索型源没有降级链语义
    assert resolve_engine("searxng") is SearxngEngine
    assert auto_degrade("searxng") == ["searxng"]
    assert "searxng" in schema.ENGINES
    import typing

    assert "searxng" in typing.get_args(schema.EngineName)


def test_schema_requires_queries_for_searxng_engine():
    """schema 装载期:engine=searxng 时 queries 必填且逐词非空(prd 用例⑥).

    断言走 :func:`load_category` 的 LoadError 通道(既有 _error_of_type
    形态):code 必须机器可读,doctor/agent 自修复才消费得了。
    """
    from myssia.schema import load_category

    def category(queries: object) -> dict:
        source: dict = {
            "name": "s",
            "engine": "searxng",
            "url": "http://127.0.0.1:8888",
        }
        if queries is not None:
            source["queries"] = queries
        return {"id": "t", "name": "t", "schedule": "0 8 * * *", "sources": [source]}

    with pytest.raises(LoadError) as excinfo:
        load_category(category(None))
    assert excinfo.value.errors[0].error_type == "missing_searxng_queries"
    assert "queries" in excinfo.value.errors[0].path

    with pytest.raises(LoadError) as excinfo:
        load_category(category(["正常词", "  "]))
    assert excinfo.value.errors[0].error_type == "invalid_searxng_query"
    assert excinfo.value.errors[0].path.endswith("queries[1]")

    # 正常形态装载通过;其余引擎不受影响(queries 是开放扩展命名空间)。
    loaded = load_category(category(["词一", "词二"]))
    assert loaded.sources[0].extra_params["queries"] == ["词一", "词二"]
    assert make_source(queries=["x"]).extra_params["queries"] == ["x"]
