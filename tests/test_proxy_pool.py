"""Tests for the v1.2 proxy pool(轮换 / 被动健康 / 摘除恢复 / 每池熔断).

PRD 10-04-proxy-pool acceptance:

- AC2 轮换/摘除/半开:顺序轮换、失败跳过、单上游退化、连续计数摘除、
  成功复位、半开到期再入、半开单飞(并发只一骑试炼上游)、**取消路径
  清位**(sidecar 120s 壳超时取消在飞试炼后 trial_in_flight 复位、下一
  请求可再入)、未到期跳过、clock 注入零真等;
- AC3 池熔断:全摘除后**零网络快速失败**(transport mock 计数为证)、
  ``proxy_pool_exhausted`` 进 proxy_* 家族、registry「短路链 + 不清 hint」
  不变量;
- 字符串池失败语义变化披露(D5 附注):逐源各自重试 → 3 连败摘除 → 池
  熔断快速失败。

All I/O runs on mock transports injected through a per-upstream ``httpx
.AsyncClient`` recorder(零真实网络);all waiting is FakeClock(零真等)。
真机双上游(一坏)验证是 [manual] AC6,不在 CI。
"""

from __future__ import annotations

import asyncio
import sys
from typing import Any, Callable

import httpx
import pytest

from myia.engines.direct_api import DirectAPIEngine
from myia.engines.fetch_base import (
    ProxyConfigError,
    ProxyPoolExhaustedError,
    ProxyPoolTransport,
    ProxyTransportError,
    classify_exception,
    load_proxy_pools,
    mask_proxy_url,
)
from myia.engines.registry import fetch_source
from myia.schema import LoadError
from myia.store import SQLiteStore
from myia.vision.collect import _client_egress_is_proxied

from conftest import FakeClock, make_client, make_context, make_source, run


# ----------------------------------------------------------------- helpers


UPSTREAM_A = "http://10.0.0.1:8080"
UPSTREAM_B = "http://10.0.0.2:8080"
DATA_URL = "https://target.example/list"


class _AsyncTransport(httpx.AsyncBaseTransport):
    """Async mock transport — responder 可以是 async callable.

    httpx.MockTransport 只收同步 handler;半开单飞/取消路径需要「先进门、
    等事件再应答」的异步 responder 来精确控制在飞时刻。
    """

    def __init__(self, responder: Callable[[httpx.Request], Any]) -> None:
        self._responder = responder

    async def handle_async_request(self, request: httpx.Request) -> httpx.Response:
        outcome = self._responder(request)
        if asyncio.iscoroutine(outcome):
            outcome = await outcome
        return outcome  # type: ignore[return-value]


def ok_responder(sink: list[str] | None = None) -> Callable[[httpx.Request], httpx.Response]:
    """200 JSON 应答(可选记录被请求的 path)."""

    def responder(request: httpx.Request) -> httpx.Response:
        if sink is not None:
            sink.append(request.url.path)
        return httpx.Response(200, json=[{"u": "https://a.example/1"}])

    return responder


def fail_with(
    exc: Exception, sink: list[str] | None = None
) -> Callable[[httpx.Request], httpx.Response]:
    """恒抛 transport 异常(可选记录)."""

    def responder(request: httpx.Request) -> httpx.Response:
        if sink is not None:
            sink.append(request.url.path)
        raise exc

    return responder


def scripted_responder(
    outcomes: list[httpx.Response | Exception], sink: list[str] | None = None
) -> Callable[[httpx.Request], httpx.Response]:
    """按脚本逐次应答;脚本耗尽后重复最后一项."""
    calls = {"i": 0}

    def responder(request: httpx.Request) -> httpx.Response:
        if sink is not None:
            sink.append(request.url.path)
        outcome = outcomes[min(calls["i"], len(outcomes) - 1)]
        calls["i"] += 1
        if isinstance(outcome, Exception):
            raise outcome
        return outcome

    return responder


def upstream_recorder(monkeypatch, responders: dict[str, Any]) -> list[str]:
    """替身 ``httpx.AsyncClient``:按解析后的上游 URL 分发 responder.

    每个上游 URL 懒建一个 client(返回值记录构建顺序 = 轮换证据);responder
    为 async 时用 :class:`_AsyncTransport`(单飞/取消控制),否则 MockTransport。
    """
    built: list[str] = []
    real_client = httpx.AsyncClient

    def factory(**kwargs: Any) -> httpx.AsyncClient:
        proxy = kwargs.pop("proxy", None)  # mock 传输层与 proxy= 参数互斥
        built.append(proxy)
        responder = responders[proxy]
        if asyncio.iscoroutinefunction(responder):
            kwargs.setdefault("transport", _AsyncTransport(responder))
        else:
            kwargs.setdefault("transport", httpx.MockTransport(responder))
        return real_client(**kwargs)

    monkeypatch.setattr("myia.engines.fetch_base.httpx.AsyncClient", factory)
    return built


def make_facade(
    monkeypatch,
    responders: dict[str, Any],
    *,
    clock: FakeClock | None = None,
    max_failures: int = 3,
    probe_interval: float = 300.0,
) -> tuple[ProxyPoolTransport, list[str], FakeClock]:
    clock = clock or FakeClock()
    built = upstream_recorder(monkeypatch, responders)
    facade = ProxyPoolTransport(
        "main",
        list(responders),
        max_failures=max_failures,
        probe_interval=probe_interval,
        clock=clock.time,
    )
    return facade, built, clock


def pool_context(
    monkeypatch,
    responders: dict[str, Any],
    *,
    pools: dict[str, Any] | None = None,
    store: SQLiteStore | None = None,
) -> tuple[Any, FakeClock, list[str]]:
    """Context + 上游 recorder 双件套(引擎级用例;pools 声明走真加载器)."""
    client = make_client(lambda request: httpx.Response(200, json=[]))
    context, clock = make_context(client, store=store)
    if pools is not None:
        context.proxy_pools = load_proxy_pools({"pools": pools})
    built = upstream_recorder(monkeypatch, responders)
    return context, clock, built


def json_source(**overrides: Any):
    overrides.setdefault("extract", {"type": "json_path", "fields": {"url": "$[*].u"}})
    # robots 关闭:robots GET 也骑 facade 会污染逐上游计数,引擎级用例聚焦数据面
    overrides.setdefault("rate_limit", {"respect_robots": False})
    return make_source(**overrides)


# ------------------------------------------------------------- AC2 轮换


def test_rotation_rides_upstreams_in_declaration_order(monkeypatch):
    """顺序游标轮换(D1):全健康时请求按声明序环形分布,上游 client 懒建一次."""
    facade, built, _clock = make_facade(
        monkeypatch, {UPSTREAM_A: ok_responder(), UPSTREAM_B: ok_responder()}
    )
    ridden = [facade.current_url]
    for _ in range(4):
        run(facade.get(DATA_URL))
        ridden.append(facade.current_url)
    assert ridden == [UPSTREAM_A, UPSTREAM_A, UPSTREAM_B, UPSTREAM_A, UPSTREAM_B]
    assert built == [UPSTREAM_A, UPSTREAM_B]  # 每上游懒建一次,复用不重建


def test_single_upstream_pool_degenerates_to_sticky(monkeypatch):
    """单上游池退化:无可轮换,全部请求骑同一上游(v0.2 语义基座)."""
    hits: list[str] = []
    facade, built, _clock = make_facade(monkeypatch, {UPSTREAM_A: ok_responder(hits)})
    for _ in range(3):
        run(facade.get(DATA_URL))
    assert len(hits) == 3
    assert built == [UPSTREAM_A]
    assert facade.current_url == UPSTREAM_A


def test_transport_failure_rotates_to_next_upstream_within_retry(monkeypatch):
    """失败跳过(质询修正④):transport 失败后下一次尝试不连续复骑同一上游,
    重试预算花在其余健康上游上 —— 引擎 retry 循环零改动即得轮换."""
    a_hits: list[str] = []
    b_hits: list[str] = []
    context, _clock, built = pool_context(
        monkeypatch,
        {
            UPSTREAM_A: fail_with(httpx.ConnectError("a down"), a_hits),
            UPSTREAM_B: ok_responder(b_hits),
        },
        pools={"main": {"upstreams": [UPSTREAM_A, UPSTREAM_B]}},
    )
    engine = DirectAPIEngine(json_source(proxy="pool:main", retry=2), context)
    items = run(engine.fetch())
    assert items == [{"url": "https://a.example/1"}]  # B 接住了
    assert a_hits == ["/list"]  # A 只吃了一次尝试(不连续吃两次)
    assert b_hits == ["/list"]
    assert built == [UPSTREAM_A, UPSTREAM_B]
    assert context.pool_transports["main"]._health[UPSTREAM_A].consec_failures == 1


def test_removed_upstream_not_readmitted_before_probe_interval(monkeypatch):
    """未到期跳过:摘除后、probe_interval 内,流量全部让位其余上游."""
    a_hits: list[str] = []
    b_hits: list[str] = []
    facade, _built, clock = make_facade(
        monkeypatch,
        {
            UPSTREAM_A: fail_with(httpx.ConnectError("a dead"), a_hits),
            UPSTREAM_B: ok_responder(b_hits),
        },
        max_failures=2,
        probe_interval=300.0,
    )
    with pytest.raises(httpx.ConnectError):  # r1:A 连败第 1 次
        run(facade.get(DATA_URL))
    run(facade.get(DATA_URL))  # r2:B
    with pytest.raises(httpx.ConnectError):  # r3:A 连败第 2 次 → 摘除@t=0
        run(facade.get(DATA_URL))
    assert facade._health[UPSTREAM_A].removed_at == 0.0
    clock.now = 299.9  # 未到期
    for _ in range(4):
        run(facade.get(DATA_URL))
    assert a_hits == ["/list"] * 2  # 摘除后 A 零复骑
    assert len(b_hits) == 5  # r2 + 摘除后的 4 次全落 B


# ------------------------------------------------- AC2 健康模型(D4 口径)


def test_consecutive_failures_reach_threshold_removes(monkeypatch):
    """连续计数摘除:达 max_failures 置 removed_at(时戳 = 注入 clock,零真等)."""
    facade, _built, _clock = make_facade(
        monkeypatch, {UPSTREAM_A: fail_with(httpx.ConnectError("dead"))}, max_failures=3
    )
    for expected_consec in (1, 2, 3):
        with pytest.raises(httpx.ConnectError):
            run(facade.get(DATA_URL))
        health = facade._health[UPSTREAM_A]
        assert health.consec_failures == expected_consec
        assert health.removed_at == (0.0 if expected_consec == 3 else None)  # clock 恒 0


def test_success_resets_consecutive_counter(monkeypatch):
    """成功复位:一次送达清零连续计数(D4 交错复位防御)."""
    script = [
        httpx.ConnectError("flap"),
        httpx.Response(200, json=[]),
        httpx.ConnectError("flap"),
    ]
    facade, _built, _clock = make_facade(
        monkeypatch, {UPSTREAM_A: scripted_responder(script)}, max_failures=2
    )
    with pytest.raises(httpx.ConnectError):
        run(facade.get(DATA_URL))
    assert facade._health[UPSTREAM_A].consec_failures == 1
    run(facade.get(DATA_URL))  # 成功 → 清零
    assert facade._health[UPSTREAM_A].consec_failures == 0
    with pytest.raises(httpx.ConnectError):  # 再败一次仍 < 阈值 → 不摘除
        run(facade.get(DATA_URL))
    assert facade._health[UPSTREAM_A].consec_failures == 1
    assert facade._health[UPSTREAM_A].removed_at is None


def test_http_status_failures_do_not_count(monkeypatch):
    """HTTP 状态失败不计数也不清零(D4:代理已送达,锅是源的)."""
    script = [
        httpx.Response(500, text="boom"),
        httpx.ConnectError("real transport failure"),
        httpx.Response(502, text="still source's fault"),
        httpx.ConnectError("another transport failure"),
    ]
    facade, _built, _clock = make_facade(
        monkeypatch, {UPSTREAM_A: scripted_responder(script)}, max_failures=2
    )
    run(facade.get(DATA_URL))  # 500:不计数
    assert facade._health[UPSTREAM_A].consec_failures == 0
    with pytest.raises(httpx.ConnectError):
        run(facade.get(DATA_URL))  # transport 失败:计 1
    assert facade._health[UPSTREAM_A].consec_failures == 1
    run(facade.get(DATA_URL))  # 502:不计数也不清零(计数保持 1)
    assert facade._health[UPSTREAM_A].consec_failures == 1
    with pytest.raises(httpx.ConnectError):  # 再一次 transport 失败 → 计 2 → 摘除
        run(facade.get(DATA_URL))
    assert facade._health[UPSTREAM_A].removed_at == 0.0


# ------------------------------------------------- AC2 半开(恢复/单飞/取消)


def test_half_open_readmits_after_probe_interval(monkeypatch):
    """半开到期再入:摘除上游过 probe_interval 后由流量自然触发试炼,成功复位归队."""
    script = [httpx.ConnectError("dead"), httpx.Response(200, json=[])]
    a_hits: list[str] = []
    facade, _built, clock = make_facade(
        monkeypatch,
        {UPSTREAM_A: scripted_responder(script, a_hits), UPSTREAM_B: ok_responder()},
        max_failures=1,
        probe_interval=300.0,
    )
    with pytest.raises(httpx.ConnectError):
        run(facade.get(DATA_URL))  # t=0 A 摘除
    run(facade.get(DATA_URL))  # B 接住,cursor 落 B
    clock.now = 300.0  # 到期
    assert run(facade.get(DATA_URL)) is not None  # 试炼 A → 成功
    assert facade.current_url == UPSTREAM_A
    health = facade._health[UPSTREAM_A]
    assert health.removed_at is None and health.consec_failures == 0  # 复位归队
    assert health.trial_in_flight is False
    assert a_hits == ["/list", "/list"]  # 零后台探活:恢复由这两次真流量完成


def test_half_open_failure_reamoves_immediately(monkeypatch):
    """半开试炼失败 = 上游仍死:立即重摘除(removed_at 刷新,不另攒 N 次)."""
    facade, _built, clock = make_facade(
        monkeypatch,
        {UPSTREAM_A: fail_with(httpx.ConnectError("still dead")), UPSTREAM_B: ok_responder()},
        max_failures=2,
        probe_interval=300.0,
    )
    with pytest.raises(httpx.ConnectError):  # A 连败第 1 次
        run(facade.get(DATA_URL))
    run(facade.get(DATA_URL))  # B
    with pytest.raises(httpx.ConnectError):  # A 连败第 2 次 → 摘除@t=0
        run(facade.get(DATA_URL))
    run(facade.get(DATA_URL))  # B,cursor 落 B
    clock.now = 300.0  # A 到期
    with pytest.raises(httpx.ConnectError):  # 试炼 A(扫描从 A 起)→ 失败
        run(facade.get(DATA_URL))
    health = facade._health[UPSTREAM_A]
    assert health.removed_at == 300.0  # 立即重摘除(时戳刷新)
    assert health.consec_failures == 3
    assert health.trial_in_flight is False
    clock.now = 599.0  # 距新摘除 299s:未到期
    run(facade.get(DATA_URL))  # cursor 落 B
    run(facade.get(DATA_URL))  # 扫描从 A 起:A 未到期被跳过 → B
    assert facade.current_url == UPSTREAM_B  # A 未到期继续让位


def test_half_open_trial_is_single_flight(monkeypatch):
    """半开单飞(修正②):到期上游同一时刻只承载一个试炼请求,并发者让位健康上游."""
    a_entered = asyncio.Event()
    release_a = asyncio.Event()
    a_calls = {"n": 0}

    async def a_responder(request: httpx.Request) -> httpx.Response:
        a_calls["n"] += 1
        if a_calls["n"] == 1:
            raise httpx.ConnectError("dead")  # 第 1 次:烧红摘除
        a_entered.set()
        await release_a.wait()  # 之后:进门占位,等放行
        return httpx.Response(200, json=[])

    facade, _built, clock = make_facade(
        monkeypatch,
        {UPSTREAM_A: a_responder, UPSTREAM_B: ok_responder()},
        max_failures=1,
        probe_interval=300.0,
    )

    async def scenario() -> None:
        with pytest.raises(httpx.ConnectError):
            await facade.get(DATA_URL)  # t=0 A 摘除
        await facade.get(DATA_URL)  # B 接住,cursor 落 B
        clock.now = 300.0  # A 到期
        trial = asyncio.create_task(facade.get(DATA_URL))  # 扫描从 A 起 → 骑 A 试炼
        await a_entered.wait()  # 试炼已进门并占位
        assert facade._health[UPSTREAM_A].trial_in_flight is True
        bystander = await asyncio.wait_for(facade.get(DATA_URL), timeout=1.0)
        assert bystander is not None  # 并发者不堵:让位 B(A 试炼位被占)
        assert facade._current is UPSTREAM_B
        release_a.set()
        assert await trial is not None
        assert facade._health[UPSTREAM_A].removed_at is None  # 试炼成功复位

    run(scenario())
    assert a_calls["n"] == 2  # A 只承载了烧红 + 单飞试炼两次


def test_cancelled_trial_releases_slot(monkeypatch):
    """取消路径清位(修正②核心):壳超时取消在飞试炼后 trial_in_flight 复位
    —— 该上游本 run 不永久占坑、不永久摘除(最坏情形 = 池提前永久熔断)."""
    a_entered = asyncio.Event()
    release_a = asyncio.Event()
    a_calls = {"n": 0}

    async def a_responder(request: httpx.Request) -> httpx.Response:
        a_calls["n"] += 1
        if a_calls["n"] == 1:
            raise httpx.ConnectError("dead")  # 第 1 次:烧红摘除
        a_entered.set()
        await release_a.wait()  # 试炼:进门后挂起,等放行(模拟 sidecar 壳超时窗)
        return httpx.Response(200, json=[])

    facade, _built, clock = make_facade(
        monkeypatch,
        {UPSTREAM_A: a_responder, UPSTREAM_B: ok_responder()},
        max_failures=1,
        probe_interval=300.0,
    )

    async def scenario() -> None:
        with pytest.raises(httpx.ConnectError):
            await facade.get(DATA_URL)  # t=0 A 摘除(removed_at=0)
        await facade.get(DATA_URL)  # B,cursor 落 B
        clock.now = 300.0  # A 到期
        trial = asyncio.create_task(facade.get(DATA_URL))  # 骑 A 试炼并挂起
        await a_entered.wait()
        assert facade._health[UPSTREAM_A].trial_in_flight is True
        trial.cancel()  # 桌面 sidecar 的 asyncio.wait_for 壳超时即这样取消在飞请求
        with pytest.raises(asyncio.CancelledError):
            await trial
        assert facade._health[UPSTREAM_A].trial_in_flight is False  # 取消也清位
        assert facade._health[UPSTREAM_A].removed_at == 0.0  # 未被误记失败/误复位
        release_a.set()  # 后续对 A 的请求即刻应答
        await facade.get(DATA_URL)  # cursor 落 B
        clock.now = 600.0  # A 再次到期(removed_at 仍为 0)
        await facade.get(DATA_URL)  # 扫描从 A 起 → A 可再入(占坑被清的证明)
        assert facade._current is UPSTREAM_A

    run(scenario())
    assert a_calls["n"] == 3  # 烧红 + 被取消的试炼 + 再入成功


# ------------------------------------------------------------- AC3 池熔断


def test_exhausted_pool_fails_fast_without_network(monkeypatch):
    """全摘除 → 池熔断:后续请求零网络快速失败(transport 计数为证)."""
    a_hits: list[str] = []
    facade, _built, _clock = make_facade(
        monkeypatch, {UPSTREAM_A: fail_with(httpx.ConnectError("dead"), a_hits)}, max_failures=1
    )
    with pytest.raises(httpx.ConnectError):
        run(facade.get(DATA_URL))  # 唯一上游摘除
    with pytest.raises(ProxyPoolExhaustedError) as excinfo:
        run(facade.get(DATA_URL))  # 熔断:零网络
    error = excinfo.value
    assert a_hits == ["/list"]  # 第二次请求根本没到传输层
    assert error.error_type == "proxy_pool_exhausted"
    assert error.error_type.startswith("proxy_")  # 进 proxy_* 家族(R5)
    assert error.pool == "main"
    assert error.recovery_in_seconds == 300.0  # 何时自愈可解释(clock 恒 0)
    assert classify_exception(error) == "proxy_pool_exhausted"
    assert mask_proxy_url(UPSTREAM_A) in str(error)  # 上游只以掩码形态出现


def test_engine_mount_fails_fast_when_pool_exhausted(monkeypatch):
    """mount 期熔断拒绝:同 run 内前一源烧红全池后,下一源 fetch 前零 I/O 报错."""
    hits: list[str] = []
    context, _clock, _built = pool_context(
        monkeypatch,
        {UPSTREAM_A: fail_with(httpx.ConnectError("dead"), hits)},
        pools={"main": {"upstreams": [UPSTREAM_A], "max_failures": 1}},
    )
    first = DirectAPIEngine(json_source(name="s1", proxy="pool:main", retry=0), context)
    with pytest.raises(ProxyTransportError):  # 单上游烧红:transport 失败包装
        run(first.fetch())
    second = DirectAPIEngine(json_source(name="s2", proxy="pool:main", retry=3), context)
    with pytest.raises(ProxyPoolExhaustedError):
        run(second.fetch())  # mount 期即拒,秒回不烧 retry 预算
    assert hits == ["/list"]  # s2 的 robots/数据零 I/O


def test_registry_short_circuits_and_keeps_hint_on_exhausted(monkeypatch, tmp_path):
    """R5 不变量:proxy_pool_exhausted 与既有 proxy_* 同族 —— registry 短路
    降级链 + 不清 hint(链上其余引擎骑同一池 facade,熔断对所有引擎同效)."""
    store = SQLiteStore(tmp_path / "registry.db")
    try:
        store.set_engine_hint(DATA_URL, "static_html")
        firecrawl_calls = {"count": 0}

        def firecrawl_factory():
            firecrawl_calls["count"] += 1
            from myia.engines.firecrawl import FirecrawlEngine

            return FirecrawlEngine

        from myia.engines import registry

        monkeypatch.setitem(registry.ENGINE_REGISTRY, "firecrawl", firecrawl_factory)
        monkeypatch.setitem(sys.modules, "crawl4ai", None)

        hits: list[str] = []
        context, _clock, _built = pool_context(
            monkeypatch,
            {UPSTREAM_A: fail_with(httpx.ConnectError("dead"), hits)},
            pools={"main": {"upstreams": [UPSTREAM_A], "max_failures": 1}},
            store=store,
        )
        source = make_source(
            engine="auto",
            url=DATA_URL,
            extract={"type": "list", "item": "a", "fields": {"url": "a@href"}},
            retry=1,
            proxy="pool:main",
            rate_limit={"respect_robots": False},
        )
        outcome = run(fetch_source(source, context))
        # attempt1 → proxy_network(摘除);attempt2 → 池熔断;链立即短路,
        # direct_api / crawl4ai / firecrawl 都不再被尝试。
        assert [(f.engine, f.error_type) for f in outcome.failures] == [
            ("static_html", "proxy_pool_exhausted")
        ]
        assert firecrawl_calls["count"] == 0
        assert store.get_engine_hint(DATA_URL) == "static_html"  # hint 保留
        assert hits == ["/list"]  # retry=1 但第 2 次尝试零网络(熔断)
    finally:
        store.close()


def test_string_pool_failure_semantics_changed_to_circuit_break(monkeypatch):
    """D5 附注(行为变化披露):字符串池从「逐源各自重试」变为「3 连败摘除 →
    池熔断快速失败」—— retry 预算没烧完就零网络收场,这是文档明写的改进."""
    hits: list[str] = []
    context, _clock, _built = pool_context(
        monkeypatch,
        {UPSTREAM_A: fail_with(httpx.ConnectError("dead"), hits)},
        pools={"main": UPSTREAM_A},  # v0.2 字符串形态,原样合法
    )
    engine = DirectAPIEngine(json_source(proxy="pool:main", retry=3), context)
    with pytest.raises(ProxyPoolExhaustedError):
        run(engine.fetch())
    assert hits == ["/list"] * 3  # 默认 max_failures=3:第 4 次尝试零网络
    assert context.pool_transports["main"]._health[UPSTREAM_A].removed_at is not None


# ---------------------------------------------------- facade 契约面与兼容


def test_facade_request_get_stream_pass_kwargs_through(monkeypatch):
    """D9 方法面:request/get/stream 显式 **kwargs 透传(per-request timeout、
    follow_redirects=False —— 图片环现网调用形态)."""
    seen: dict[str, Any] = {}

    def responder(request: httpx.Request) -> httpx.Response:
        seen["timeout"] = request.extensions.get("timeout")
        return httpx.Response(200, text="body")

    async def read_stream(facade: ProxyPoolTransport, url: str) -> bytes:
        async with facade.stream("GET", url, timeout=7.5, follow_redirects=False) as resp:
            return await resp.aread()

    facade, _built, _clock = make_facade(monkeypatch, {UPSTREAM_A: responder})
    # follow_redirects / timeout 若不透传,固定签名在这里即 TypeError(httpx
    # 原生支持 per-request 覆写);timeout 在传输层可观测,断言其到达。
    response = run(facade.request("GET", DATA_URL, timeout=7.5, follow_redirects=False))
    assert response.text == "body"
    assert float(seen["timeout"]["connect"]) == 7.5  # per-request timeout 覆写生效
    run(facade.get(DATA_URL, timeout=7.5))
    assert run(read_stream(facade, DATA_URL)) == b"body"


def test_facade_stream_records_health_outcomes(monkeypatch):
    """stream 的健康口径与 request 同源:transport 失败计数、4xx 不计数不清零、
    成功复位."""
    script = [
        httpx.ConnectError("stream flap"),
        httpx.Response(404, text="gone"),
        httpx.Response(200, text="ok"),
    ]
    facade, _built, _clock = make_facade(
        monkeypatch, {UPSTREAM_A: scripted_responder(script)}, max_failures=2
    )

    async def scenario() -> None:
        with pytest.raises(httpx.ConnectError):
            async with facade.stream("GET", DATA_URL):
                pass
        assert facade._health[UPSTREAM_A].consec_failures == 1
        async with facade.stream("GET", DATA_URL) as resp:
            await resp.aread()
        assert facade._health[UPSTREAM_A].consec_failures == 1  # 404 不计数不清零
        async with facade.stream("GET", DATA_URL) as resp:
            await resp.aread()
        assert facade._health[UPSTREAM_A].consec_failures == 0  # 成功复位

    run(scenario())


def test_facade_marks_proxy_egress_for_image_ring(monkeypatch):
    """图片环 SSRF 复核的出网判定:facade 自述 is_proxy_egress(懒建 client
    未建时也必须成立,否则经代理图片全灭 ssrf_rebind —— collect.py rationale)."""
    # recorder 补丁作用于共享的 httpx 模块属性,直连对照 client 须先建
    plain = make_client(lambda request: httpx.Response(200))
    facade, _built, _clock = make_facade(monkeypatch, {UPSTREAM_A: ok_responder()})
    assert facade.is_proxy_egress is True
    assert _client_egress_is_proxied(facade) is True  # 尚未构建任何上游 client
    run(facade.get(DATA_URL))
    assert _client_egress_is_proxied(facade) is True  # 构建后同样成立
    assert _client_egress_is_proxied(plain) is False  # 直连 client 判定不变


def test_facade_aclose_closes_all_upstream_clients(monkeypatch):
    """aclose 关全部上游 client(run 收尾由 aclose_pool_transports 统一调用)."""
    facade, _built, _clock = make_facade(
        monkeypatch, {UPSTREAM_A: ok_responder(), UPSTREAM_B: ok_responder()}
    )
    run(facade.get(DATA_URL))
    run(facade.get(DATA_URL))  # 轮换到 B,两上游 client 都已懒建
    clients = list(facade._clients.values())
    assert len(clients) == 2 and not any(client.is_closed for client in clients)
    run(facade.aclose())
    assert all(client.is_closed for client in clients)


def test_engine_mount_sets_active_proxy_url_to_first_admissible(monkeypatch):
    """mount 即选上游(design §5.1):``_active_proxy_url`` = mount 时刻第一个
    可 admit 上游(浏览器三读者消费;会话内不轮换)."""
    context, _clock, built = pool_context(
        monkeypatch,
        {UPSTREAM_A: ok_responder(), UPSTREAM_B: ok_responder()},
        pools={"main": {"upstreams": [UPSTREAM_A, UPSTREAM_B]}},
    )
    engine = DirectAPIEngine(json_source(proxy="pool:main", retry=0), context)
    run(engine.fetch())
    assert engine._active_proxy_url == UPSTREAM_A
    assert built[0] == UPSTREAM_A
    transport = context.pool_transports["main"]
    assert transport.current_url in (UPSTREAM_A, UPSTREAM_B)  # 数据请求后可轮换
    assert context.pool_robots["main"] is engine._active_robots  # robots 骑 facade


def test_transport_failure_message_carries_tried_upstreams_and_mask(monkeypatch):
    """错误消息带尝试上游数 + 最后上游掩码(B3;凭据不落错误信息)."""
    monkeypatch.setenv("MYIA_T_POOL_CRED", "alice:hunter2")
    resolved = "http://alice:hunter2@10.0.0.1:8080"
    context, _clock, _built = pool_context(
        monkeypatch,
        {resolved: fail_with(httpx.ProxyError("auth rejected"))},
        pools={"main": {"upstreams": ["http://env:MYIA_T_POOL_CRED@10.0.0.1:8080"]}},
    )
    engine = DirectAPIEngine(json_source(proxy="pool:main", retry=2), context)
    with pytest.raises(ProxyTransportError) as excinfo:
        run(engine.fetch())
    message = str(excinfo.value)
    assert "pool=main" in message
    assert "已试 1/1 上游" in message
    assert "http://***@10.0.0.1:8080" in message
    assert "hunter2" not in message


def test_client_build_failure_raises_config_error_not_health():
    """D10:懒建 client 构建失败不计数、直接冒 ProxyConfigError(依赖缺失的
    真相不被健康模型吃掉;与 test_proxy_transport 迁移用例互为佐证)."""
    facade = ProxyPoolTransport("bad", ["ftp://10.0.0.1:21"], clock=FakeClock().time)
    with pytest.raises(ProxyConfigError) as excinfo:
        run(facade.get(DATA_URL))
    assert excinfo.value.code == "invalid_proxy_url"
    assert facade._health["ftp://10.0.0.1:21"].consec_failures == 0


def test_context_deprecated_aliases_return_same_objects(monkeypatch):
    """D9 兼容:client_for_pool/pool_clients/aclose_pool_clients deprecated
    alias 与新名同物(留一个版本周期)."""
    context, _clock, _built = pool_context(
        monkeypatch,
        {UPSTREAM_A: ok_responder()},
        pools={"main": UPSTREAM_A},
    )
    engine = DirectAPIEngine(json_source(proxy="pool:main", retry=0), context)
    run(engine.fetch())
    facade = context.pool_transports["main"]
    assert context.client_for_pool("main") is facade
    assert context.pool_clients is context.pool_transports
    assert context.pool_clients["main"] is facade
    run(context.aclose_pool_clients())  # alias 关闭同样生效
    assert context.pool_transports == {}


def test_pools_undeclared_zero_impact_keeps_direct_path(monkeypatch):
    """pool 未声明的零影响断言:pools=None 时 direct 源零 facade 构建、零
    新 client(recorder 空),direct 请求语义原样."""
    calls: list[str] = []

    def responder(request: httpx.Request) -> httpx.Response:
        calls.append(request.url.path)
        return httpx.Response(200, json=[{"u": "https://a.example/1"}])

    client = make_client(responder)
    context, _clock = make_context(client)
    context.proxy_pools = None  # pools 未声明
    built = upstream_recorder(monkeypatch, {UPSTREAM_A: responder})
    engine = DirectAPIEngine(json_source(proxy="direct", retry=0), context)
    items = run(engine.fetch())
    assert items == [{"url": "https://a.example/1"}]
    assert built == []  # 零 facade/零新 client
    assert context.pool_transports == {}
    assert engine._active_client is context.client


# ------------------------------------------------- doctor 逐上游(C4/AC4)


def _fake_check_shape(ok: bool = True) -> dict[str, Any]:
    """与 ProxyCheckResult.to_dict 同键集的假探测结果(AC4 形态等价断言用)."""
    return {
        "ok": ok,
        "message": "代理连通" if ok else "失败",
        "proxy_url": "http://***@masked",
        "latency_seconds": 0.01,
        "status_code": 200 if ok else None,
        "exit_ip": "203.0.113.7" if ok else None,
        "error_type": None if ok else "proxy_network",
    }


def test_doctor_probes_every_upstream_with_index_fields(monkeypatch):
    """doctor 逐池逐上游:展开 resolve_upstreams 并行探测,行带
    upstream_index/upstreams;单上游池输出 = 既有字段集 + 纯增字段(AC4)."""
    from myia import cli

    probed: list[str] = []

    async def fake_check(proxy_url, *, client=None, timeout=10.0, **kwargs):
        probed.append(proxy_url)
        return type("Check", (), {"to_dict": staticmethod(lambda: _fake_check_shape())})()

    monkeypatch.setattr(cli, "check_proxy_connectivity", fake_check)
    pools = load_proxy_pools(
        {
            "pools": {
                "multi": {"upstreams": [UPSTREAM_A, UPSTREAM_B]},
                "solo": UPSTREAM_A,
            }
        }
    )
    rows = run(cli._probe_proxy_pools(pools, timeout=1.0, backend=None))
    assert probed == [UPSTREAM_A, UPSTREAM_B, UPSTREAM_A]  # 每上游各探一次
    assert [(row["pool"], row["upstream_index"], row["upstreams"]) for row in rows] == [
        ("multi", 0, 2),
        ("multi", 1, 2),
        ("solo", 0, 1),
    ]
    # 单上游池行形态 = 既有键集合 + 纯增的 upstream_index/upstreams(AC4 等价)
    assert set(rows[-1]) == set(_fake_check_shape()) | {"pool", "upstream_index", "upstreams"}


def test_doctor_multi_upstream_resolution_failure_isolated(monkeypatch):
    """单池凭据解析失败不拖垮其余池(部分失败语义,mask 打码不变)."""
    from myia import cli

    async def fake_check(proxy_url, *, client=None, timeout=10.0, **kwargs):  # pragma: no cover
        raise AssertionError("探测不应发生:唯一池解析失败")

    monkeypatch.setattr(cli, "check_proxy_connectivity", fake_check)
    monkeypatch.delenv("MYIA_T_MISSING", raising=False)
    pools = load_proxy_pools(
        {"pools": {"broken": {"upstreams": ["http://env:MYIA_T_MISSING@10.0.0.1:8080"]}}}
    )
    rows = run(cli._probe_proxy_pools(pools, timeout=1.0, backend=None))
    assert len(rows) == 1
    row = rows[0]
    assert row["ok"] is False
    assert "无法解析" in row["message"]
    assert row["proxy_url"] == "http://***@10.0.0.1:8080"


# ------------------------------------------------- 加载器错误面(补 A3)


def test_mapping_pool_upstream_not_string_refused():
    with pytest.raises(LoadError) as excinfo:
        load_proxy_pools({"pools": {"rot": {"upstreams": [42]}}})
    detail = excinfo.value.errors[0]
    assert detail.error_type == "invalid_pool_upstreams"
    assert detail.path == "$.pools.rot.upstreams[0]"
