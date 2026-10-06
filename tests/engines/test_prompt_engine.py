"""Tests for the prompt-task engine (10-06-hermes-align 批次3).

MYIA 版 ``hermes chat -Q`` 的最小等价物:一个源 = 一个自然语言监控任务
(instructions + URL 清单)→ 逐 URL 礼貌抓取 + trafilatura 抽正文 → 一轮
OpenAI 兼容 LLM → markdown 摘要条目。测试全 mock(MockTransport HTTP、
fake trafilatura、fake completer、env 引用凭据),零真网零真 LLM。

用例面(蓝本 ``plugins/ai-vendor-watch.yaml`` 示范件的形状):

1. registry/链外语义与 schema 词表(prompt 在册、AUTO_CHAIN 不在、
   auto_degrade 单级链);
2. options 校验:instructions 必填、urls 元素/上限/scheme、数值越界、
   端点凭据引用缺失/明文拒(credential_invalid);
3. 凭据解析失败结构化(credential_unresolved);
4. 正常路径:三目标 → 一条目,日期锚点 #prompt-<YYYYMMDD>、
   content=prompt_summary=LLM markdown、观测键 prompt_urls_ok/failed、
   user 消息含 instructions 与各正文段、限速按 host 生效;
5. 部分目标失败降级继续(prompt_urls_failed=1 照出条目);6. 全部目标失败 → prompt_fetch_failed;
7. LLM 失败/空输出 → prompt_llm_failed;
8. trafilatura 缺装 → dependency_missing;
9. pagination / extract 配置结构化拒;
10. robots 禁止目标 → RobotsDisallowedError(礼貌红线不降级)。
"""

from __future__ import annotations

from types import SimpleNamespace
from typing import Any

import httpx
import pytest

from conftest import FakeClock, make_client, make_context, make_source, run

from myssia.engines.fetch_base import FetchContext, FetchError, RobotsDisallowedError
from myssia.engines.prompt import (
    MAX_URLS_PER_SOURCE,
    SYSTEM_PROMPT,
    PromptEngine,
)
from myssia.engines.registry import (
    AUTO_CHAIN,
    ENGINE_REGISTRY,
    auto_degrade,
    resolve_engine,
)
from myssia.schema import PaginationConfig, RateLimitConfig, SourceConfig

PAGE_HTML = "<html><body><main>OpenAI 新闻列表正文。</main></body></html>"
MARKDOWN = "## AI 厂商官网日报\n\n- OpenAI:发布新模型\n- Anthropic:无明显动态"

ENV_URL = "MYIA_TEST_PROMPT_LLM_URL"
ENV_KEY = "MYIA_TEST_PROMPT_LLM_KEY"


class FakeCompleter:
    """LLM 完成层替身:记录调用、返回固定 markdown(CompletionResult 同形)."""

    def __init__(self, text: str = MARKDOWN, exc: Exception | None = None) -> None:
        self.text = text
        self.exc = exc
        self.calls: list[dict[str, Any]] = []

    async def complete(self, *, model: str, system: str, user: str) -> Any:
        self.calls.append({"model": model, "system": system, "user": user})
        if self.exc is not None:
            raise self.exc
        return SimpleNamespace(text=self.text, total_tokens=42)


def fake_trafilatura(text_by_html: dict[str, str] | None = None) -> Any:
    """trafilatura 替身模块:extract() 返回 JSON 串(static_html 钉版 API)."""
    import json

    def extract(html: str, url: str, output_format: str, with_metadata: bool) -> str | None:
        assert output_format == "json" and with_metadata
        text = (text_by_html or {}).get(html, "默认正文" * 30)
        if text is None:
            return None
        return json.dumps({"text": text, "title": "页面标题", "url": url}, ensure_ascii=False)

    return SimpleNamespace(extract=extract)


def prompt_options(**overrides: Any) -> dict[str, Any]:
    base: dict[str, Any] = {
        "instructions": "找出新发布/重大更新,中文摘要",
        "base_url": f"env:{ENV_URL}",
        "api_key": f"env:{ENV_KEY}",
    }
    base.update(overrides)
    return base


def prompt_source(**overrides: Any):
    data: dict[str, Any] = {
        "name": "ai-vendor-watch",
        "url": "https://openai.com/news",
        "engine": "prompt",
        "engine_options": {"prompt": prompt_options()},
    }
    data.update(overrides)
    return make_source(**data)


def prompt_engine(
    source: Any = None,
    *,
    handler: Any = None,
    completer: FakeCompleter | None = None,
    trafilatura: Any = "unset",
    monkeypatch: Any = None,
    clock: FakeClock | None = None,
) -> tuple[PromptEngine, FakeCompleter, FakeClock]:
    """组装被测引擎:mock HTTP + fake trafilatura + fake completer."""
    if monkeypatch is not None:
        monkeypatch.setenv(ENV_URL, "https://llm.example.com/v4")
        monkeypatch.setenv(ENV_KEY, "sk-test-not-a-real-key")
        if trafilatura == "unset":
            trafilatura = fake_trafilatura()
        monkeypatch.setattr(
            "myssia.engines.prompt.load_trafilatura", lambda: trafilatura
        )
    completer = completer or FakeCompleter()
    if handler is None:
        handler = lambda request: httpx.Response(  # noqa: E731 - 测试局部handler
            200, text=PAGE_HTML
        )
    client = make_client(handler)
    context, clock = make_context(client, clock=clock, silent_limiter=True)
    engine = PromptEngine(source or prompt_source(), context, completer=completer.complete)
    return engine, completer, clock


# ---------------------------------------------------------------------- 1


def test_registry_membership_and_chain_untouched():
    assert "prompt" in ENGINE_REGISTRY
    assert resolve_engine("prompt") is PromptEngine
    assert "prompt" not in AUTO_CHAIN  # 链外:auto 永不路过
    assert auto_degrade("prompt") == ["prompt"]  # 显式选择=单级链


def test_schema_vocabulary_accepts_prompt():
    source = prompt_source()  # SourceConfig.model_validate 即 schema 面
    assert source.engine == "prompt"


# ---------------------------------------------------------------------- 2


@pytest.mark.parametrize(
    "overrides",
    [
        {"instructions": None},
        {"instructions": "   "},
        {"urls": "not-a-list"},
        {"urls": []},
        {"urls": [123]},
        {"urls": ["ftp://bad.example/"]},
        {"urls": ["https://a.example/", "https://b.example/", "no-scheme"]},
        {"title": "  "},
        {"model": 42},
        {"max_chars_per_url": 10},
        {"timeout": -1},
        {"base_url": None},
    ],
)
def test_engine_options_type_guard(overrides, monkeypatch):
    monkeypatch.setenv(ENV_URL, "https://llm.example.com/v4")
    monkeypatch.setenv(ENV_KEY, "sk-test-not-a-real-key")
    source = prompt_source(
        engine_options={"prompt": prompt_options(**overrides)},
    )
    engine, _, _ = prompt_engine(source)
    with pytest.raises(FetchError) as excinfo:
        run(engine.fetch())
    # base_url 缺失=credential_invalid,其余形状错=invalid_engine_options
    assert excinfo.value.error_type in ("invalid_engine_options", "credential_invalid")


def test_plaintext_endpoint_refused_at_load():
    """明文端点在 schema 装载期即拒(engine_options 凭据键子串扫描红线)."""
    import pydantic

    with pytest.raises(pydantic.ValidationError):
        prompt_source(
            engine_options={
                "prompt": prompt_options(api_key="sk-plaintext-not-a-real-key")
            }
        )


def test_urls_over_limit_rejected(monkeypatch):
    many = [f"https://host{i}.example.com/" for i in range(MAX_URLS_PER_SOURCE + 1)]
    source = prompt_source(engine_options={"prompt": prompt_options(urls=many)})
    engine, _, _ = prompt_engine(source, monkeypatch=monkeypatch)
    with pytest.raises(FetchError) as excinfo:
        run(engine.fetch())
    assert excinfo.value.error_type == "invalid_engine_options"
    assert f"最多 {MAX_URLS_PER_SOURCE}" in str(excinfo.value)


# ---------------------------------------------------------------------- 3


def test_credential_reference_unresolved(monkeypatch):
    # helper 先把两个 env 都设好,再撤掉 KEY:解析期才失败(装载期只看引用形态)
    engine, _, _ = prompt_engine(
        trafilatura=fake_trafilatura(), monkeypatch=monkeypatch
    )
    monkeypatch.delenv(ENV_KEY, raising=False)  # api_key 的 env 引用解析不到
    with pytest.raises(FetchError) as excinfo:
        run(engine.fetch())
    assert excinfo.value.error_type == "credential_unresolved"


# ---------------------------------------------------------------------- 4


def test_happy_path_one_summary_item(monkeypatch):
    seen: list[str] = []

    def handler(request: httpx.Request) -> httpx.Response:
        seen.append(str(request.url))
        if request.url.path == "/robots.txt":
            return httpx.Response(404)  # fail-open:无规则=允许
        return httpx.Response(200, text=PAGE_HTML)

    source = prompt_source(
        engine_options={
            "prompt": prompt_options(
                urls=[
                    "https://openai.com/news",
                    "https://www.anthropic.com/news",
                    "https://deepmind.google/discover",
                ],
            )
        },
    )
    engine, completer, _clock = prompt_engine(
        source, handler=handler, monkeypatch=monkeypatch
    )
    items = run(engine.fetch())
    assert len(items) == 1
    item = items[0]
    # 日期锚点:urlwatch #watch- 判例 —— 每天新条目、同日幂等
    import re

    assert re.search(r"#prompt-\d{8}$", item["url"])
    assert item["url"].startswith("https://openai.com/news")
    assert item["title"] == "ai-vendor-watch"  # 缺省 title=源名
    assert item["content"] == MARKDOWN
    assert item["prompt_summary"] == MARKDOWN  # 模板渲染键(metadata 面)
    assert item["prompt_urls_ok"] == 3
    assert item["prompt_urls_failed"] == 0
    assert item["prompt_model"] == "glm-4-flash"
    assert item["prompt_instructions"].startswith("找出新发布")
    # LLM 调用形状:一轮、system 固定、user 含 instructions 与三正文段
    assert len(completer.calls) == 1
    call = completer.calls[0]
    assert call["system"] == SYSTEM_PROMPT
    assert "找出新发布/重大更新" in call["user"]
    assert call["user"].count("## 目标页面") == 3
    assert "https://www.anthropic.com/news" in call["user"]
    # 礼貌面:每目标 robots 查询 + 页面抓取都发生了
    robots = [url for url in seen if url.endswith("/robots.txt")]
    pages = [url for url in seen if not url.endswith("/robots.txt")]
    assert len(robots) == 3 and len(pages) == 3


def test_per_host_rate_limit_applies(monkeypatch):
    """同域多目标共享 per-host 限速(源内串行礼貌)。"""
    sleeps: list[float] = []

    async def fake_sleep(seconds: float) -> None:
        sleeps.append(seconds)

    from myssia.engines.fetch_base import FetchContext

    source = prompt_source(
        engine_options={
            "prompt": prompt_options(
                urls=[
                    "https://openai.com/news",
                    "https://openai.com/index",
                ],
            )
        },
    )
    handler = lambda request: httpx.Response(200, text=PAGE_HTML)  # noqa: E731
    client = make_client(handler)
    clock = FakeClock()
    # 手工构造:limiter registry 的 sleeper 绑 fake_sleep(make_context 的
    # silent_limiter 绑静默 sleep,限速等待不可观测)。
    context = FetchContext(client=client, clock=clock.time, sleep=fake_sleep)
    monkeypatch.setenv(ENV_URL, "https://llm.example.com/v4")
    monkeypatch.setenv(ENV_KEY, "sk-test-not-a-real-key")
    monkeypatch.setattr(
        "myssia.engines.prompt.load_trafilatura", lambda: fake_trafilatura()
    )
    engine = PromptEngine(source, context, completer=FakeCompleter().complete)
    items = run(engine.fetch())
    assert len(items) == 1
    # qps=0.5 → 同域第二请求至少等 ~2s(1/qps 主导,jitter 只增不减)
    assert sleeps and max(sleeps) >= 1.5


# ---------------------------------------------------------------------- 5


def test_partial_target_failure_degrades(monkeypatch):
    def handler(request: httpx.Request) -> httpx.Response:
        if request.url.host == "www.anthropic.com":
            return httpx.Response(500, text="boom")  # 重试耗尽后 raise_for_status
        if request.url.path == "/robots.txt":
            return httpx.Response(404)
        return httpx.Response(200, text=PAGE_HTML)

    source = prompt_source(
        engine_options={
            "prompt": prompt_options(
                urls=[
                    "https://openai.com/news",
                    "https://www.anthropic.com/news",
                ],
            )
        },
    )
    # retry=0 让 500 立即失败(不退避),加快测试
    source = make_source(
        name="ai-vendor-watch",
        url="https://openai.com/news",
        engine="prompt",
        retry=0,
        engine_options={
            "prompt": prompt_options(
                urls=["https://openai.com/news", "https://www.anthropic.com/news"]
            )
        },
    )
    engine, completer, _ = prompt_engine(source, handler=handler, monkeypatch=monkeypatch)
    items = run(engine.fetch())
    assert len(items) == 1
    assert items[0]["prompt_urls_ok"] == 1
    assert items[0]["prompt_urls_failed"] == 1
    # 抓取失败的目标在 user 消息里留名(LLM 知道哪些没看着)
    assert "https://www.anthropic.com/news" in completer.calls[0]["user"]


# ---------------------------------------------------------------------- 6


def test_all_targets_failed_is_structured(monkeypatch):
    def handler(request: httpx.Request) -> httpx.Response:
        if request.url.path == "/robots.txt":
            return httpx.Response(404)
        return httpx.Response(503, text="down")

    source = prompt_source(retry=0)
    engine, completer, _ = prompt_engine(source, handler=handler, monkeypatch=monkeypatch)
    with pytest.raises(FetchError) as excinfo:
        run(engine.fetch())
    assert excinfo.value.error_type == "prompt_fetch_failed"
    assert completer.calls == []  # 零 LLM 调用


# ---------------------------------------------------------------------- 7


def test_llm_failure_is_structured(monkeypatch):
    completer = FakeCompleter(exc=RuntimeError("endpoint 500"))
    engine, _, _ = prompt_engine(completer=completer, monkeypatch=monkeypatch)
    with pytest.raises(FetchError) as excinfo:
        run(engine.fetch())
    assert excinfo.value.error_type == "prompt_llm_failed"
    assert "endpoint 500" in str(excinfo.value)


def test_llm_empty_output_is_structured(monkeypatch):
    completer = FakeCompleter(text="   ")
    engine, _, _ = prompt_engine(completer=completer, monkeypatch=monkeypatch)
    with pytest.raises(FetchError) as excinfo:
        run(engine.fetch())
    assert excinfo.value.error_type == "prompt_llm_failed"


class FakeLLMClient:
    """OpenAICompatClient 替身(自建路径用):记录 complete/aclose 调用."""

    instances: list["FakeLLMClient"] = []

    def __init__(self, base_url: str, api_key: str, **_kw: Any) -> None:
        self.base_url = base_url
        self.closed = False
        self.completed = False
        FakeLLMClient.instances.append(self)

    def _ensure_async_client(self) -> None:  # openai 惰性 import 的替身(恒可用)
        pass

    async def complete(self, *, model: str, system: str, user: str) -> Any:
        self.completed = True
        return SimpleNamespace(text=MARKDOWN, total_tokens=7)

    async def aclose(self) -> None:
        self.closed = True


def test_own_client_closed_after_completion(monkeypatch):
    """资源卫生(复核条目④):completer 未注入时每轮自建 LLM 客户端,完成即 aclose."""
    FakeLLMClient.instances = []
    monkeypatch.setattr(
        "myssia.engines.prompt.OpenAICompatClient", FakeLLMClient
    )
    engine, _, _ = prompt_engine(monkeypatch=monkeypatch)
    engine._completer = None  # 强制走自建路径(helper 默认注入 fake completer)
    items = run(engine.fetch())
    assert len(items) == 1
    assert len(FakeLLMClient.instances) == 1
    client = FakeLLMClient.instances[0]
    assert client.completed and client.closed


def test_own_client_closed_on_llm_failure(monkeypatch):
    """LLM 失败路径同样关闭客户端(清理绝不顶掉真实异常)."""

    class FailingClient(FakeLLMClient):
        async def complete(self, *, model: str, system: str, user: str) -> Any:
            self.completed = True
            raise RuntimeError("endpoint boom")

    FakeLLMClient.instances = []
    monkeypatch.setattr("myssia.engines.prompt.OpenAICompatClient", FailingClient)
    engine, _, _ = prompt_engine(monkeypatch=monkeypatch)
    engine._completer = None
    with pytest.raises(FetchError) as excinfo:
        run(engine.fetch())
    assert excinfo.value.error_type == "prompt_llm_failed"
    assert "endpoint boom" in str(excinfo.value)
    assert FakeLLMClient.instances[0].closed


# ---------------------------------------------------------------------- 8


def test_trafilatura_missing_is_structured(monkeypatch):
    engine, _, _ = prompt_engine(trafilatura=None, monkeypatch=monkeypatch)
    with pytest.raises(FetchError) as excinfo:
        run(engine.fetch())
    assert excinfo.value.error_type == "dependency_missing"
    assert "myssia[trafilatura]" in str(excinfo.value)


# ---------------------------------------------------------------------- 9


def test_pagination_config_rejected(monkeypatch):
    # model_construct 绕开 schema 的 template/{page} 交叉校验(urlwatch 测试
    # 同款):这里钉的是引擎层单轮任务语义的拒,不是 schema 层。
    source = SourceConfig.model_construct(
        name="ai-vendor-watch",
        url="https://openai.com/news",
        engine="prompt",
        headers={},
        proxy="direct",
        retry=0,
        rate_limit=RateLimitConfig(),
        pagination=PaginationConfig.model_construct(mode="template", max_pages=2),
        engine_options={"prompt": prompt_options()},
    )
    engine, _, _ = prompt_engine(source, monkeypatch=monkeypatch)
    with pytest.raises(FetchError) as excinfo:
        run(engine.fetch())
    assert excinfo.value.error_type == "pagination_unsupported"


def test_extract_config_rejected():
    source = prompt_source(
        extract={
            "type": "list",
            "item": "article",
            "fields": {"title": "h3", "url": "a@href"},
        },
    )
    engine, _, _ = prompt_engine(source)
    with pytest.raises(FetchError) as excinfo:
        run(engine.fetch())
    assert excinfo.value.error_type == "extract_unsupported"


# --------------------------------------------------------------------- 10


def test_xml_feed_target_uses_feedparser_path(monkeypatch):
    """XML feed 目标走 feedparser 通路(openai RSS 判例:HTML 页 CF 403)。"""
    rss = (
        '<?xml version="1.0"?><rss version="2.0"><channel>'
        "<item><title>OpenAI 发布新模型</title>"
        "<description>正文摘要一段。</description></item>"
        "<item><title>另一条更新</title></item>"
        "</channel></rss>"
    )

    def handler(request: httpx.Request) -> httpx.Response:
        if request.url.path == "/robots.txt":
            return httpx.Response(404)
        if request.url.path.endswith(".xml"):
            return httpx.Response(200, text=rss)
        return httpx.Response(200, text=PAGE_HTML)

    source = prompt_source(
        engine_options={
            "prompt": prompt_options(
                urls=["https://www.anthropic.com/news", "https://openai.com/news/rss.xml"],
            )
        },
    )
    engine, completer, _ = prompt_engine(
        source, handler=handler, monkeypatch=monkeypatch
    )
    items = run(engine.fetch())
    assert len(items) == 1
    assert items[0]["prompt_urls_ok"] == 2
    user = completer.calls[0]["user"]
    assert "OpenAI 发布新模型" in user  # feed 条目标题进了 prompt
    assert "正文摘要一段" in user


def test_robots_disallowed_target_rejected(monkeypatch):
    def handler(request: httpx.Request) -> httpx.Response:
        if request.url.path == "/robots.txt":
            return httpx.Response(
                200, text="User-agent: *\nDisallow: /\n"  # 全禁
            )
        return httpx.Response(200, text=PAGE_HTML)

    engine, completer, _ = prompt_engine(handler=handler, monkeypatch=monkeypatch)
    with pytest.raises(RobotsDisallowedError):
        run(engine.fetch())
    assert completer.calls == []


# --------------------------------------------------------------------- 11


def test_push_template_renders_prompt_summary(monkeypatch):
    """「LLM 输出直接作为条目内容进 push」:示范件模板渲染链(prompt_summary
    经 item_view 的 metadata 合并进模板上下文 → feishu markdown 卡分片)。"""
    from myssia.pipeline import Item
    from myssia.push.base import SendContext
    from myssia.push.feishu_card import _split_markdown_cards
    from myssia.push.templates import TemplateRenderer

    engine, _, _ = prompt_engine(monkeypatch=monkeypatch)
    raw_items = run(engine.fetch())
    items = [Item.from_extracted(raw, source="ai-vendor-watch") for raw in raw_items]
    # content 进 Item.content(档案),prompt_summary 进 metadata(模板键)
    assert items[0].content == MARKDOWN
    assert items[0].metadata["prompt_summary"] == MARKDOWN

    template = (
        "**AI 厂商官网日报 · {{ date }}**\n"
        "{% if items %}{{ items[0].prompt_summary }}{% endif %}"
    )
    context = SendContext(
        category="ai-vendor-watch", date="2026-10-06", slot="am", kind="immediate"
    )
    rendered = TemplateRenderer().render(template, items, context)
    assert "AI 厂商官网日报 · 2026-10-06" in rendered
    assert MARKDOWN in rendered  # LLM markdown 全文进推送载荷
    cards = _split_markdown_cards(rendered, title="AI 厂商官网日报", threshold=28000)
    assert cards and MARKDOWN[:40] in cards[0]["elements"][0]["text"]["content"]
