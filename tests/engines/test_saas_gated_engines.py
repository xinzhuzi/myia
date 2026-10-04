"""Tests for the gated paid-SaaS engines (zenrows / scraperapi, R6, 批二第 12 步).

三态矩阵(design §6.7 / AC7):

- **关闭态**:gates.yaml 缺失 / 总开关关 / 件开关关 / 坏文件(fail-closed)
  → ``FetchError(class="gate_closed")`` 结构化失败,且**零上游请求**(关闭态
  不烧钱是本引擎类的存在理由;handler 挂 pytest.fail 钉死);
- **开启态**:``MYIA_HOME`` 指 tmp gates.yaml + InMemoryKeychainBackend →
  httpx.MockTransport 往返(上游 URL/查询参数/键值直进查询串/条目提取/
  css_extractor JSON 模式/timeout 透传);
- **注册表**:ENGINE_REGISTRY 在册、AUTO_CHAIN 不在(七层原样不动)、
  ``auto_degrade`` 给单级链、schema ``ENGINES``/``EngineName`` 词表收录。

零真实网络(MockTransport)、零真实钥匙串(InMemoryKeychainBackend)、
零真实扣费(全部门槛态与上游调用均 mock)。
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
from myssia.engines.scraperapi import ScraperAPIEngine
from myssia.engines.zenrows import ZenrowsEngine
from myssia.schema import CredentialResolveError, SourceConfig
from myssia.secrets import SECRET_SERVICE, InMemoryKeychainBackend

from conftest import make_client, make_context, make_handler, make_source, run

TARGET_URL = "https://js-heavy.example.com/hot"

# gates.yaml 文档片段(§6.1 形状):开启 = 总开关 ∧ 件开关,api_key 只收
# keychain 引用(明文/env: 由 myssia.gates 构造校验拒载,这里只写合法形态)。
GATES_ZENROWS_ON = """\
version: 1
paid_engines: true
saas:
  zenrows:
    enabled: true
    api_key: keychain:myia/saas/zenrows-key
"""
GATES_TOTAL_OFF_ENGINE_ON = """\
version: 1
paid_engines: false
saas:
  zenrows:
    enabled: true
    api_key: keychain:myia/saas/zenrows-key
"""
GATES_TOTAL_ON_ENGINE_OFF = """\
version: 1
paid_engines: true
saas:
  zenrows:
    enabled: false
    api_key: keychain:myia/saas/zenrows-key
"""
GATES_ENGINE_ON_NO_KEY = """\
version: 1
paid_engines: true
saas:
  zenrows:
    enabled: true
"""
GATES_BOTH_ON = """\
version: 1
paid_engines: true
saas:
  zenrows:
    enabled: true
    api_key: keychain:myia/saas/zenrows-key
  scraperapi:
    enabled: true
    api_key: keychain:myia/saas/scraperapi-key
"""

PAGE_HTML = (
    "<html><head><title>JS 渲染标题</title></head><body>"
    '<div class="item"><a class="title" href="/t/1">条目一</a></div>'
    '<div class="item"><a class="title" href="/t/2">条目二</a></div>'
    "</body></html>"
)


def set_home(monkeypatch: pytest.MonkeyPatch, tmp_path, text: str | None) -> None:
    """MYIA_HOME → tmp 目录;``text`` 非 None 时落 gates.yaml(None = 缺文件态)。

    引擎在 fetch 时经 ``default_gates_path()`` 逐次解析(MYIA_HOME env >
    ``~/.myia/gates.yaml``),monkeypatch 环境即完成隔离 —— 开发机的
    ``~/.myia/gates.yaml`` 永不影响测试。
    """
    monkeypatch.setenv("MYIA_HOME", str(tmp_path))
    if text is not None:
        (tmp_path / "gates.yaml").write_text(text, encoding="utf-8")


def gated_context(
    client: httpx.AsyncClient,
) -> tuple[FetchContext, InMemoryKeychainBackend]:
    """上下文 + 已写好 saas 键的 mock 钥匙串(零真实 keychain 触碰)。"""
    context, _ = make_context(client)
    backend = InMemoryKeychainBackend()
    backend.set_password(SECRET_SERVICE, "myia/saas/zenrows-key", "zr-secret-1")
    backend.set_password(SECRET_SERVICE, "myia/saas/scraperapi-key", "sa-secret-9")
    context.keychain_backend = backend
    return context, backend


def failing_handler():
    """任何非 robots 请求即失败的 handler(关闭态零请求断言)。"""
    return make_handler(lambda request: pytest.fail(f"不应发起任何请求:{request.url}"))


# ---------------------------------------------------------------------------
# 状态一:关闭态 gate_closed(零上游请求)
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    ("gates_text", "label"),
    [
        (None, "缺文件=全关"),
        (GATES_TOTAL_OFF_ENGINE_ON, "总开关关"),
        (GATES_TOTAL_ON_ENGINE_OFF, "件开关关"),
        ("version: 1\nunknown_key: true\n", "未知字段=fail-closed 全关"),
        ("version: 1\nsaas: {zenrows: {enabled: true\n", "坏 YAML=fail-closed 全关"),
    ],
)
def test_closed_gate_is_structured_gate_closed_zero_requests(
    monkeypatch, tmp_path, gates_text, label
):
    """五路关闭态(含 fail-closed 两路)→ gate_closed,零上游请求。"""
    set_home(monkeypatch, tmp_path, gates_text)
    client = make_client(failing_handler())
    context, _ = make_context(client)
    engine = ZenrowsEngine(make_source(engine="zenrows", url=TARGET_URL), context)

    with pytest.raises(FetchError) as excinfo:
        run(engine.fetch())
    assert excinfo.value.error_type == "gate_closed", label
    # doctor 文案语义:门槛失败自带开闸指引,与 dependency_missing(缺依赖)
    # 分列 —— 消息说的是「知情开启」,不是「装依赖」。
    message = str(excinfo.value)
    assert "myssia gates set" in message
    assert "saas.zenrows" in message
    assert "dependency" not in message


def test_bad_gates_file_logs_warning_but_stays_fail_closed(monkeypatch, tmp_path, caplog):
    """坏 gates.yaml:全关继续跑 + warning 留痕(fail-closed 不是静默吞)。"""
    set_home(monkeypatch, tmp_path, "version: 1\nunknown_key: true\n")
    client = make_client(failing_handler())
    context, _ = make_context(client)
    engine = ZenrowsEngine(make_source(engine="zenrows", url=TARGET_URL), context)

    with caplog.at_level("WARNING", logger="myssia.engines.saas"):
        with pytest.raises(FetchError) as excinfo:
            run(engine.fetch())
    assert excinfo.value.error_type == "gate_closed"
    assert any("全关" in record.getMessage() for record in caplog.records)


# ---------------------------------------------------------------------------
# 状态二:开启态 MockTransport 往返
# ---------------------------------------------------------------------------


def test_open_gate_zenrows_roundtrip_query_params_and_item(monkeypatch, tmp_path):
    """开启态:apikey(钥匙串解析值)+ url 直进上游查询串;HTML 原文回退条目。"""
    set_home(monkeypatch, tmp_path, GATES_ZENROWS_ON)
    captured: dict = {}

    def responder(request: httpx.Request) -> httpx.Response:
        captured["url"] = str(request.url)
        captured["params"] = dict(request.url.params)
        return httpx.Response(200, text=PAGE_HTML)

    client = make_client(make_handler(responder))
    context, _ = gated_context(client)
    source = make_source(
        engine="zenrows",
        url=TARGET_URL,
        engine_options={"zenrows": {"js_render": True, "premium_proxy": True}},
    )
    engine = ZenrowsEngine(source, context)

    items = run(engine.fetch())
    assert captured["url"].startswith("https://api.zenrows.com/v1/")
    assert captured["params"]["apikey"] == "zr-secret-1"  # 钥匙串值直进查询串
    assert captured["params"]["url"] == TARGET_URL
    assert captured["params"]["js_render"] == "true"  # 布尔序列化 true/false
    assert captured["params"]["premium_proxy"] == "true"
    assert items == [
        {"url": TARGET_URL, "title": "JS 渲染标题", "content": PAGE_HTML}
    ]


def test_open_gate_zenrows_extract_over_html(monkeypatch, tmp_path):
    """extract list/item 在上游返回的目标页 HTML 上照常 CSS 抽取。"""
    set_home(monkeypatch, tmp_path, GATES_ZENROWS_ON)
    client = make_client(
        make_handler(lambda request: httpx.Response(200, text=PAGE_HTML))
    )
    context, _ = gated_context(client)
    source = make_source(
        engine="zenrows",
        url=TARGET_URL,
        extract={
            "type": "list",
            "item": "div.item",
            "fields": {"title": "a.title", "url": "a.title@href"},
        },
    )

    items = run(ZenrowsEngine(source, context).fetch())
    assert items == [
        {"title": "条目一", "url": "https://js-heavy.example.com/t/1"},
        {"title": "条目二", "url": "https://js-heavy.example.com/t/2"},
    ]


def test_zenrows_css_extractor_json_mode(monkeypatch, tmp_path):
    """css_extractor:映射序列化进查询串,上游响应按 JSON 消费(json_path 抽取)。"""
    set_home(monkeypatch, tmp_path, GATES_ZENROWS_ON)
    captured: dict = {}

    def responder(request: httpx.Request) -> httpx.Response:
        captured["css_extractor"] = request.url.params.get("css_extractor")
        return httpx.Response(
            200,
            json={
                "title": "上游抽取标题",
                "price": "42",
                "url": "https://js-heavy.example.com/t/1",
            },
        )

    client = make_client(make_handler(responder))
    context, _ = gated_context(client)
    source = make_source(
        engine="zenrows",
        url=TARGET_URL,
        engine_options={"zenrows": {"css_extractor": {"title": "h1", "price": ".price"}}},
        extract={
            "type": "json_path",
            "fields": {"title": "$.title", "price": "$.price", "url": "$.url"},
        },
    )

    items = run(ZenrowsEngine(source, context).fetch())
    assert captured["css_extractor"] == '{"title":"h1","price":".price"}'
    assert items == [
        {
            "title": "上游抽取标题",
            "price": "42",
            "url": "https://js-heavy.example.com/t/1",
        }
    ]


def test_open_gate_scraperapi_roundtrip_country_render_timeout(monkeypatch, tmp_path):
    """ScraperAPI 参数面:api_key/url/country/render;timeout 透传到 HTTP 客户端。"""
    set_home(monkeypatch, tmp_path, GATES_ZENROWS_ON.replace("zenrows", "scraperapi"))
    captured: dict = {}

    def responder(request: httpx.Request) -> httpx.Response:
        captured["params"] = dict(request.url.params)
        captured["extensions"] = request.extensions
        return httpx.Response(200, text=PAGE_HTML)

    client = make_client(make_handler(responder))
    context, _ = gated_context(client)
    source = make_source(
        engine="scraperapi",
        url=TARGET_URL,
        engine_options={"scraperapi": {"country": "US", "render": True, "timeout": 45}},
    )

    items = run(ScraperAPIEngine(source, context).fetch())
    assert captured["params"]["api_key"] == "sa-secret-9"
    assert captured["params"]["url"] == TARGET_URL
    assert captured["params"]["country"] == "us"  # ISO alpha-2 小写化
    assert captured["params"]["render"] == "true"
    # HTTP 客户端超时 = max(上游预算 45, 管线默认 30):客户端不早于上游预算掐断。
    assert captured["extensions"]["timeout"]["read"] == 45.0
    assert items and items[0]["url"] == TARGET_URL


# ---------------------------------------------------------------------------
# 门槛半开两态:开着但钥匙串缺位 / 引用在而键未写
# ---------------------------------------------------------------------------


def test_gate_open_without_api_key_ref_is_gate_key_missing(monkeypatch, tmp_path):
    """门槛开着但 api_key 引用缺位(手写 gates.yaml 漏键)→ gate_key_missing,零请求。"""
    set_home(monkeypatch, tmp_path, GATES_ENGINE_ON_NO_KEY)
    client = make_client(failing_handler())
    context, _ = make_context(client)
    engine = ZenrowsEngine(make_source(engine="zenrows", url=TARGET_URL), context)

    with pytest.raises(FetchError) as excinfo:
        run(engine.fetch())
    assert excinfo.value.error_type == "gate_key_missing"
    assert "myssia secret set myia/saas/zenrows-key" in str(excinfo.value)


def test_keychain_ref_unresolvable_propagates_credential_error(monkeypatch, tmp_path):
    """引用在、钥匙串键未写 → 既有凭据失败通道(CredentialResolveError),零请求。"""
    set_home(monkeypatch, tmp_path, GATES_ZENROWS_ON)
    client = make_client(failing_handler())
    context, _ = make_context(client)  # 未写任何键的 mock 钥匙串
    context.keychain_backend = InMemoryKeychainBackend()
    engine = ZenrowsEngine(make_source(engine="zenrows", url=TARGET_URL), context)

    with pytest.raises(CredentialResolveError) as excinfo:
        run(engine.fetch())
    assert excinfo.value.code == "secret_not_found"


# ---------------------------------------------------------------------------
# 上游错误:结构化 + 凭据不落错误消息
# ---------------------------------------------------------------------------


def test_upstream_http_error_is_structured_and_leaks_no_api_key(monkeypatch, tmp_path):
    """上游 401 → http_401 结构化失败;消息零 apikey 值(日志安全纪律)。"""
    set_home(monkeypatch, tmp_path, GATES_ZENROWS_ON)
    client = make_client(
        make_handler(lambda request: httpx.Response(401, text="invalid apikey"))
    )
    context, _ = gated_context(client)
    engine = ZenrowsEngine(make_source(engine="zenrows", url=TARGET_URL), context)

    with pytest.raises(FetchError) as excinfo:
        run(engine.fetch())
    assert excinfo.value.error_type == "http_401"
    message = str(excinfo.value)
    assert "zr-secret-1" not in message  # 凭据零外流
    assert "https://api.zenrows.com/v1/" in message  # 端点常量可入消息(公开文档值)


# ---------------------------------------------------------------------------
# 状态三:注册表与词表(链外三锁)
# ---------------------------------------------------------------------------


def test_registry_contains_both_but_auto_chain_untouched():
    """在册 + 不在链 + AUTO_CHAIN 七层原样(AC7:永不进 AUTO_CHAIN)。"""
    assert "zenrows" in ENGINE_REGISTRY and "scraperapi" in ENGINE_REGISTRY
    assert "zenrows" not in AUTO_CHAIN and "scraperapi" not in AUTO_CHAIN
    assert AUTO_CHAIN == (
        "direct_api",
        "static_html",
        "crawl4ai",
        "firecrawl",
        "scrapling",
        "stealth_browser",
        "llm_browser",
    )
    assert resolve_engine("zenrows") is ZenrowsEngine
    assert resolve_engine("scraperapi") is ScraperAPIEngine
    assert auto_degrade("zenrows") == ["zenrows"]  # 链外:显式选择=单级链
    assert auto_degrade("scraperapi") == ["scraperapi"]


def test_schema_vocabulary_accepts_both_engines():
    """schema 双锁:ENGINES 词表 + SourceConfig 可显式选用(test_credhunter_wiring 同款)。"""
    assert "zenrows" in schema.ENGINES and "scraperapi" in schema.ENGINES
    for name in ("zenrows", "scraperapi"):
        source = SourceConfig.model_validate({"name": "demo", "url": TARGET_URL, "engine": name})
        assert source.engine == name


def test_option_type_errors_are_structured(monkeypatch, tmp_path):
    """参数面类型错(布尔位给了字符串/国家码三位)→ 结构化拒,零上游请求。

    gates 用 BOTH_ON:门槛检查先于参数校验,两引擎都得开着才测得到参数面。
    """
    set_home(monkeypatch, tmp_path, GATES_BOTH_ON)
    zenrows_client = make_client(failing_handler())
    context, _ = gated_context(zenrows_client)
    bad_bool = make_source(
        engine="zenrows", url=TARGET_URL, engine_options={"zenrows": {"js_render": "yes"}}
    )
    with pytest.raises(FetchError) as excinfo:
        run(ZenrowsEngine(bad_bool, context).fetch())
    assert excinfo.value.error_type == "invalid_engine_options"

    bad_country = make_source(
        engine="scraperapi", url=TARGET_URL, engine_options={"scraperapi": {"country": "usa"}}
    )
    with pytest.raises(FetchError) as excinfo:
        run(ScraperAPIEngine(bad_country, context).fetch())
    assert excinfo.value.error_type == "invalid_engine_options"
