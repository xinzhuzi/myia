"""10-04-proxy-pool 冒烟:多上游池 fixture 端到端矩阵(轮换/摘除/恢复/熔断)
+ pool 未声明零影响对照。零外网:全部 I/O 骑注入的 mock 传输层,全部等待是
FakeClock(零真等)。跑法(仓库根):

    uv run --no-sync python .trellis/tasks/10-04-proxy-pool/evidence/e2e_matrix_smoke.py

任何断言失败 → 非零退出。矩阵时线(t=0 起,max_failures=2, probe_interval=300):

    M1 轮换     A,B 全健康 → 声明序环形 A,B,A,B(client 懒建各一次)
    M2 摘除     A 烧死 → 连续 2 败摘除@t0;失败即跳过(B 接住,A 不连吃两次)
    M3 未到期   t0+299 → A 零复骑,流量全落 B
    M4 恢复     t0+300 → 半开试炼 A 成功 → 复位归队
    M5 熔断     A,B 全摘除@t400 → 下一请求零网络 ProxyPoolExhaustedError
    M6 熔断解除 最早摘除者到期半开成功 → 池恢复可运营
    E1 引擎级   真加载器 YAML(混形)→ DirectAPIEngine.fetch()(A 死 B 活,retry=2)
    C1 对照     pools 未声明(proxy_pools=None)→ direct 源零 facade/零新 client
    C2 兼容     v0.2 字符串池原样合法 = 单上游池;空 upstreams 结构化拒载
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "tests"))

import httpx  # noqa: E402
import yaml  # noqa: E402

from conftest import FakeClock, make_client, make_context, make_source, run  # noqa: E402
from myia.engines.direct_api import DirectAPIEngine  # noqa: E402
from myia.engines.fetch_base import (  # noqa: E402
    ProxyPoolExhaustedError,
    ProxyPoolTransport,
    load_proxy_pools,
)
from myia.schema import LoadError  # noqa: E402

UPSTREAM_A = "http://10.0.0.1:8080"
UPSTREAM_B = "http://10.0.0.2:8080"
DATA_URL = "https://target.example/list"

fails = 0


def check(label: str, ok: bool, detail: str = "") -> None:
    global fails
    mark = "PASS" if ok else "FAIL"
    print(f"  [{mark}] {label}" + (f" — {detail}" if detail else ""))
    if not ok:
        fails += 1


class Recorder:
    """替身 httpx.AsyncClient 工厂:按上游 URL 分发可控 responder 并记命中."""

    def __init__(self) -> None:
        self.built: list[str] = []
        self.hits: dict[str, list[str]] = {UPSTREAM_A: [], UPSTREAM_B: []}
        self.dead: set[str] = set()  # 当前处于「烧死」态的上游
        self._orig = httpx.AsyncClient

    def install(self) -> None:
        recorder = self

        def factory(**kwargs):
            proxy = kwargs.pop("proxy", None)
            recorder.built.append(proxy)

            def responder(request: httpx.Request) -> httpx.Response:
                sink = recorder.hits[proxy]
                sink.append(request.url.path)
                if proxy in recorder.dead:
                    raise httpx.ConnectError(f"{proxy} down")
                return httpx.Response(200, json=[{"u": "https://a.example/1"}])

            kwargs.setdefault("transport", httpx.MockTransport(responder))
            return recorder._orig(**kwargs)

        httpx.AsyncClient = factory  # 全局补丁(脚本进程内;脚本结束即销毁)

    def restore(self) -> None:
        httpx.AsyncClient = self._orig

    def n(self, url: str) -> int:
        return len(self.hits[url])


def health_line(facade: ProxyPoolTransport, url: str) -> str:
    h = facade._health[url]
    return f"{url}: consec={h.consec_failures} removed_at={h.removed_at} trial={h.trial_in_flight}"


async def matrix() -> None:  # M1–M6:facade 级端到端矩阵
    clock = FakeClock()
    recorder = Recorder()
    recorder.install()
    try:
        facade = ProxyPoolTransport(
            "main", [UPSTREAM_A, UPSTREAM_B], max_failures=2, probe_interval=300.0, clock=clock.time
        )

        print("== M1 轮换(声明序环形)==")
        ridden = []
        for _ in range(4):
            await facade.get(DATA_URL)
            ridden.append(facade.current_url)
        check("4 请求骑乘序 = A,B,A,B", ridden == [UPSTREAM_A, UPSTREAM_B] * 2, str(ridden))
        check("上游 client 懒建各一次", recorder.built == [UPSTREAM_A, UPSTREAM_B], str(recorder.built))
        check("M1 命中 A=2 B=2", recorder.n(UPSTREAM_A) == 2 and recorder.n(UPSTREAM_B) == 2,
              f"A={recorder.n(UPSTREAM_A)} B={recorder.n(UPSTREAM_B)}")

        print("== M2 摘除(A 烧死:连续 2 败即摘除;失败即跳过)==")
        recorder.dead.add(UPSTREAM_A)
        # 游标在 B(index1):下一请求扫到 A(index0)→ 败 1;再下一请求扫到 B → 接住;
        # 再下一请求扫到 A → 败 2 → 摘除@t=0
        try:
            await facade.get(DATA_URL)
            check("A 第 1 败透传 ConnectError", False, "竟然成功")
        except httpx.ConnectError:
            check("A 第 1 败透传 ConnectError", True)
        await facade.get(DATA_URL)  # 失败即跳过 → B 接住
        try:
            await facade.get(DATA_URL)
            check("A 第 2 败透传 ConnectError", False, "竟然成功")
        except httpx.ConnectError:
            check("A 第 2 败透传 ConnectError", True)
        h = facade._health[UPSTREAM_A]
        check("A 连续 2 败 → 摘除@t=0", h.consec_failures == 2 and h.removed_at == 0.0,
              health_line(facade, UPSTREAM_A))
        check("失败即跳过:A 不连吃两次(命中 A=4/B=3)",
              recorder.n(UPSTREAM_A) == 4 and recorder.n(UPSTREAM_B) == 3,
              f"A={recorder.n(UPSTREAM_A)} B={recorder.n(UPSTREAM_B)}")
        check("B 健康未受牵连", facade._health[UPSTREAM_B].removed_at is None)

        print("== M3 未到期跳过(t0+299,A 零复骑)==")
        clock.now = 299.0
        for _ in range(3):
            await facade.get(DATA_URL)
        check("A 摘除后零复骑(命中仍 4)", recorder.n(UPSTREAM_A) == 4, f"A={recorder.n(UPSTREAM_A)}")
        check("流量全落 B(命中 B=6)", recorder.n(UPSTREAM_B) == 6, f"B={recorder.n(UPSTREAM_B)}")

        print("== M4 恢复(t0+300 半开试炼成功 → 复位归队)==")
        recorder.dead.discard(UPSTREAM_A)
        clock.now = 300.0
        response = await facade.get(DATA_URL)  # 游标在 B → 扫描从 A 起 → 试炼 A → 成功
        check("半开试炼 A 成功(200 返回)", response.status_code == 200)
        h = facade._health[UPSTREAM_A]
        check("A 复位归队(consec=0, removed=None, trial 已清)",
              h.consec_failures == 0 and h.removed_at is None and h.trial_in_flight is False,
              health_line(facade, UPSTREAM_A))
        check("零后台探活:恢复由本次真流量触发(A 命中 5)", recorder.n(UPSTREAM_A) == 5)

        print("== M5 池熔断(A,B 全摘除@t400 → 零网络快速失败)==")
        clock.now = 400.0
        recorder.dead.update({UPSTREAM_A, UPSTREAM_B})
        drained = 0
        for _ in range(12):  # 安全上界:两上游各 2 败即全摘除(≤5 请求)
            if (
                facade._health[UPSTREAM_A].removed_at is not None
                and facade._health[UPSTREAM_B].removed_at is not None
            ):
                break
            drained += 1
            try:
                await facade.get(DATA_URL)
            except (httpx.ConnectError, ProxyPoolExhaustedError):
                continue
        check("全摘除达成(≤5 请求烧红两上游)", drained <= 5, f"drained={drained}")
        check("A 重新摘除@400", facade._health[UPSTREAM_A].removed_at == 400.0,
              health_line(facade, UPSTREAM_A))
        check("B 摘除@400 → 全摘除 = 池熔断", facade._health[UPSTREAM_B].removed_at == 400.0,
              health_line(facade, UPSTREAM_B))
        a_before, b_before = recorder.n(UPSTREAM_A), recorder.n(UPSTREAM_B)
        try:
            await facade.get(DATA_URL)
            check("熔断请求应抛 ProxyPoolExhaustedError", False, "竟然成功")
        except ProxyPoolExhaustedError as error:
            check("ProxyPoolExhaustedError(error_type=proxy_pool_exhausted)",
                  error.error_type == "proxy_pool_exhausted")
            check("进 proxy_* 家族(R5)", error.error_type.startswith("proxy_"))
            check("pool 字段可解释", error.pool == "main")
            check("recovery_in_seconds=300(最早摘除@400,now=400)",
                  error.recovery_in_seconds == 300.0, f"recovery={error.recovery_in_seconds}s")
        check("零网络:熔断请求未触传输层(命中不变)",
              recorder.n(UPSTREAM_A) == a_before and recorder.n(UPSTREAM_B) == b_before,
              f"A:{recorder.n(UPSTREAM_A) - a_before} 次, B:{recorder.n(UPSTREAM_B) - b_before} 次")

        print("== M6 熔断解除(最早摘除者到期半开成功)==")
        recorder.dead.clear()
        clock.now = 700.0  # 400 + probe_interval
        response = await facade.get(DATA_URL)
        check("到期半开试炼成功 → 池恢复运营", response.status_code == 200)
        check("ensure_operable 通过", facade.ensure_operable() in (UPSTREAM_A, UPSTREAM_B))
        await facade.aclose()
        check("aclose 关全部上游 client", all(c.is_closed for c in facade._clients.values()))
    finally:
        recorder.restore()


def engine_level() -> None:
    """E1 引擎级端到端:真加载器 YAML(混形)→ DirectAPIEngine.fetch()."""
    recorder = Recorder()
    try:
        text = """
pools:
  main:
    upstreams:
      - http://10.0.0.1:8080
      - http://10.0.0.2:8080
    max_failures: 2
    probe_interval: 300
        """
        pools = load_proxy_pools(yaml.safe_load(text))
        spec = pools.spec("main")
        check("YAML 混形加载:upstreams 声明序", list(spec.upstreams) == [UPSTREAM_A, UPSTREAM_B])
        check("YAML 池策略覆写生效", spec.max_failures == 2 and spec.probe_interval == 300.0)
        check("resolve_upstreams 展开(无凭据引用=原样)",
              pools.resolve_upstreams("main") == [UPSTREAM_A, UPSTREAM_B])

        client = make_client(lambda request: httpx.Response(200, json=[]))  # 补丁装前先建(直连对照 client)
        context, _clock = make_context(client)
        recorder.install()
        context.proxy_pools = pools
        recorder.dead.add(UPSTREAM_A)  # A 死 B 活
        source = make_source(
            name="e2e",
            url=DATA_URL,
            extract={"type": "json_path", "fields": {"url": "$[*].u"}},
            rate_limit={"respect_robots": False},
            proxy="pool:main",
            retry=2,
        )
        items = run(DirectAPIEngine(source, context).fetch())
        check("引擎级轮换:A 死 B 接住,拿到真 items", items == [{"url": "https://a.example/1"}], str(items))
        check("A 只吃一次尝试(失败即换,不连续复骑)", recorder.n(UPSTREAM_A) == 1,
              f"A={recorder.n(UPSTREAM_A)} B={recorder.n(UPSTREAM_B)}")
        check("B 接住一次", recorder.n(UPSTREAM_B) == 1, f"B={recorder.n(UPSTREAM_B)}")
        check("facade 已挂载", isinstance(context.pool_transports["main"], ProxyPoolTransport))
        run(context.aclose_pool_transports())
    finally:
        recorder.restore()


def control_no_pools() -> None:
    """C1 对照:pools 未声明 → direct 源零 facade 构建、零新 client,语义原样."""
    # 直连对照 client 先建(recorder 补丁作用于共享的 httpx 模块属性,后建会混入 built)
    client = make_client(lambda request: httpx.Response(200, json=[{"u": "https://a.example/1"}]))
    recorder = Recorder()
    recorder.install()
    try:
        context, _clock = make_context(client)
        context.proxy_pools = None  # pools 未声明(对照态)
        source = make_source(
            name="ctl",
            url=DATA_URL,
            extract={"type": "json_path", "fields": {"url": "$[*].u"}},
            rate_limit={"respect_robots": False},
            proxy="direct",
            retry=0,
        )
        engine = DirectAPIEngine(source, context)
        items = run(engine.fetch())
        check("direct 源语义原样(items 到手)", items == [{"url": "https://a.example/1"}], str(items))
        check("零 facade 构建(pool_transports 空)", context.pool_transports == {})
        check("零新上游 client(recorder 空)", recorder.built == [], str(recorder.built))
        check("引擎骑 context 既有 client", engine._active_client is context.client)
    finally:
        recorder.restore()


def string_form_compat() -> None:
    """C2 v0.2 字符串形态兼容(AC1 冒烟面):原样合法 = 单上游池."""
    pools = load_proxy_pools({"pools": {"legacy": UPSTREAM_A}})
    spec = pools.spec("legacy")
    check("字符串池 = 单上游池", list(spec.upstreams) == [UPSTREAM_A])
    check("字符串池默认策略(3/300)", spec.max_failures == 3 and spec.probe_interval == 300.0)
    try:
        load_proxy_pools({"pools": {"bad": {"upstreams": []}}})
        check("空 upstreams 拒载(structured LoadError)", False, "竟然载入")
    except LoadError as error:
        check("空 upstreams 拒载(structured LoadError)",
              error.errors[0].error_type == "invalid_pool_upstreams")


if __name__ == "__main__":
    print(f"e2e_matrix_smoke @ {ROOT}(全部 mock 传输层 + FakeClock,零外网零真等)\n")
    run(matrix())
    print("\n== E1 引擎级端到端(真加载器 + DirectAPIEngine)==")
    engine_level()
    print("\n== C1 对照:pools 未声明零影响 ==")
    control_no_pools()
    print("\n== C2 v0.2 字符串形态兼容 ==")
    string_form_compat()
    print(f"\n== 结果:{'ALL PASS' if fails == 0 else f'{fails} 项 FAIL'} ==")
    sys.exit(1 if fails else 0)
