# Design:proxy_pool 池化(轮换 + 被动健康 + 每池熔断)

> 决议依据:prd「已拍板决议」D1-D10(grill round 1 七问 + round 2 质询
> 修正/补拍,全按推荐)。行号基准 2026-10-04 工作树(fetch_base.py 1889 行版);
> 建档期间并行会话将 `src/shishi/` 改名 `src/myia/`,本文锚点已对新路径逐一
> 直核(零漂移,见 prd 路径基准注记)。

## 1. 架构总览

```
v0.2(现状)                                 v1.2 池化(目标)
──────────────────────────                 ──────────────────────────
pools: {name: "url"}                        pools: {name: "url" | {upstreams: [...], ...}}
ProxyPools: name -> raw_url:str             ProxyPools: name -> PoolSpec(urls, max_failures, probe_interval)
FetchContext.pool_clients                   FetchContext.pool_transports(池运行态,facade)
  : dict[name, httpx.AsyncClient]             : dict[name, ProxyPoolTransport]
client_for_pool(name, url)                  pool_transport_for(name) -> ProxyPoolTransport
                                              (client_for_pool 留 deprecated alias,D9)
BaseEngine._active_client = 池 client       = 池 facade(duck-type request/get/aclose)
transport 失败 -> ProxyTransportError       池内轮换耗尽才冒 ProxyTransportError;
                                            全池摘除 -> ProxyPoolExhaustedError
```

改动集中在 `src/myia/engines/fetch_base.py` 一处(声明模型 + 运行时 + 引擎
接线),消费点(`pipeline.py` 图片环、`cli.py` doctor、`engines/crawl4ai.py`)
做适配性小改;`schema.py` 零改动(pool:<名称> 语法不变)。

## 2. YAML 声明层(prd D5 混形兼容)

```yaml
pools:
  main: "http://env:MYIA_PROXY_MAIN@proxy.example.com:8080"   # v0.2 字符串,原样合法
  rotating:                                                    # v1.2 池化形态
    upstreams:
      - "http://env:MYIA_PROXY_A@p1.example.com:8080"
      - "socks5://keychain:myia/proxy/b@p2.example.com:1080"
    max_failures: 3          # 可选;连续失败摘除阈值,默认 3;须 ≥1
    probe_interval: 300      # 可选;半开恢复间隔(秒),默认 300;须 ≥1
```

**数据模型**(fetch_base.py 内新增,`ProxyPools` 对外方法保持向后可用):

```python
@dataclass(frozen=True)
class PoolSpec:
    upstreams: tuple[str, ...]     # 声明序原始 URL(凭据仍为引用)
    max_failures: int = 3
    probe_interval: float = 300.0

class ProxyPools:
    def spec(self, name) -> PoolSpec              # 新:整池规格
    def upstream_urls(self, name) -> list[str]    # 新:声明序 URL 列表(doctor 用)
    def raw_url(self, name) -> str                # 保留:单上游池=唯一 URL;多上游池=第一个
                                                   # (仅 doctor 错误展示兜底用,逐步边缘化)
    def resolve(self, name, *, backend) -> str    # 保留:解析第一个上游(兼容既有调用
                                                   # 语义);运行态一律走 resolve_upstreams
    def resolve_upstreams(self, name, *, backend) -> list[str]  # 新:逐上游凭据解析
```

**加载校验**(全部挂现有 `load_proxy_pools` 的 LoadErrorDetail 通道,零第二套
规则):映射形态必须含非空 `upstreams` 列表(`invalid_pools` / 新 code
`invalid_pool_upstreams`);每条 URL 过既有 `_validate_pool_url`(scheme 白名单/
host/凭据引用);`max_failures`/`probe_interval` 非法(非正数/非数值)逐条
结构化拒载(code `invalid_pool_policy`);**混形歧义**(同时给字符串语义的键
如 `upstreams` 与未知键)——未知键拒载(code `unknown_pool_field`,防拼写错误
静默吞策略)。名称语法/重复键拒载/明文凭据拒载红线全部沿用。

## 3. 运行时:ProxyPoolTransport(每池每 run 一个,挂在 FetchContext)

```python
class ProxyPoolTransport:
    """池 facade:引擎持它当 _active_client,请求委派当前健康上游的 client。

    duck-type 面(D9:显式 **kwargs 透传——collect.py:445 现网调用已传
    follow_redirects=False,固定签名会打挂图片环):
      async def request(self, method: str, url: str, **kwargs) -> httpx.Response
      async def get(self, url: str, **kwargs) -> httpx.Response
      async def aclose(self) -> None
    引擎与 RobotsCache 的既有调用形态零改动。
    """
    # 构造:(pool 名, resolved_urls, policy, timeout, clock)
    #   clock 注入自 FetchContext.clock(测试零真等,同 RateLimiter 范式)
    # 状态:
    #   _clients: dict[url, httpx.AsyncClient]     # 懒建,凭据只解析一次/上游
    #   _health:  dict[url, UpstreamHealth]        # 见 §4
    #   _cursor:  int                              # 顺序游标(声明序环形)
    #   _current: str | None                       # 当前骑乘上游 URL
    # 对外:
    #   current_url -> str | None                  # crawl4ai 直读(_active_proxy_url 来源)
    #   masked_current() -> str                    # 日志形态(mask_proxy_url)
```

`FetchContext.pool_clients: dict[str, httpx.AsyncClient]` 更名为
`pool_transports: dict[str, ProxyPoolTransport]`(`aclose_pool_clients` 同步
改名 `aclose_pool_transports`,内部逐池 `transport.aclose()` 关全部上游
client;旧名保留 alias 一个版本周期,标注 deprecated)。工厂方法**统一命名
`pool_transport_for(name) -> ProxyPoolTransport`**(D9:round 1 草稿 §1/§3 写
`client_for_pool(name)`、§5.3 写 `pool_transport_for(pool_name)`,同物两名,
定稿统一后者;`client_for_pool` 留 deprecated alias 一个版本周期)——spec/
解析都从 `self.proxy_pools` 取;timeout 参数移除——池内统一用
`context.timeout`,图片环的短超时改在 request 调用点传(**kwargs 透传面),
httpx 支持 per-request timeout,`_send_with_retry` 已有该先例
fetch_base.py:1772。

**身份兼容**:`pool_transports[name] is engine._active_client`(facade 同一
对象)与「同池多源共享一个对象」(test_proxy_transport.py:219-242 断言形态)
原样存活。

## 4. 健康模型(prd D2/D3/D4/D6)

### 4.1 UpstreamHealth 状态

```python
@dataclass
class UpstreamHealth:
    consec_failures: int = 0     # 连续失败计数(成功清零)
    removed_at: float | None     # monotonic 时戳;非 None = 摘除态
    trial_in_flight: bool        # 半开单飞占位
```

状态 = healthy(consec < max_failures)| removed(removed_at 非 None)。
**无独立 state 枚举**——池熔断是派生态(len(healthy∪到期半开)== 0)。

### 4.2 计数与轮换(retry 循环内)

失败计数口径(D4):facade.request 捕获的 transport 级异常(`httpx.TransportError`
含 Timeout 族,即 classify_proxy_transport 会归 proxy_* 的同一集合)→ 当前上游
`consec_failures += 1`,达 `max_failures` 置 `removed_at = clock()`;HTTP 状态
失败(4xx/5xx)不计数——代理已送达。成功(2xx/3xx/304)→ `consec = 0`、
`removed_at = None`、`trial_in_flight = False`。

轮换节奏(质询修正④):transport 失败后下一次尝试**立即换下一个可 admit 的
上游**(同一上游不连续吃两次尝试,池大小 >1 时);backoff 仍按源 retry 策略
照睡(既有 `_send_with_retry` fetch_base.py:1750-1800 骨架不动,attempt 循环
内把 `self._active_client.request` 换成经 facade 的 per-attempt 选择)。

上游选择(admit 规则,从 cursor+1 环形扫):
1. healthy → admit,游标落位;
2. removed 且 `clock() - removed_at >= probe_interval` 且 `trial_in_flight`
   为 False → admit 并置 `trial_in_flight = True`(**半开单飞**,质询修正②);
3. 其余跳过。扫描一整圈无 admit → 池熔断路径(§4.4)。

### 4.3 半开单飞

试炼上游成功 → 复位归队(consec=0/removed_at=None);失败 → `consec+1`,
若仍 < max_failures 也**立即重摘除**(removed_at 刷新——半开失败不等待再攒
N 次,试炼失败=上游仍死)。`trial_in_flight` 清位必须 **try/finally 且覆盖
全部终态:成功 / transport 失败 / 非 TransportError 异常 / CancelledError**
(grill round 2 修正②)——桌面 sidecar 120s 壳超时经 `asyncio.wait_for`
取消在飞请求,取消路径若不清位,该上游本 run 永久占坑=永久摘除,最坏情形
池提前永久熔断。单线程 asyncio 下占位/清位都发生在 await 前后的同步段,
无锁安全。

### 4.4 池熔断(派生态,D6)

选择圈空 → facade 抛 `ProxyPoolExhaustedError`:

```python
class ProxyPoolExhaustedError(FetchError):
    """全部上游摘除且无到期半开——池熔断,零网络快速失败。"""
    error_type = "proxy_pool_exhausted"      # startswith("proxy_") ✓
    # 携带:pool 名、上游数、最早 removed_at + probe_interval 的到期时刻(日志/
    #       doctor 可解释「何时自愈」,mask 形态)
```

发生时机两处,语义同一:引擎 mount 时(`_prepare_proxy_transport` 发现池
熔断,fetch 前零 I/O 拒绝,与既有 `proxy_pools_not_configured` 同层)与 retry
循环内换上游时。**等待不睡**:熔断期间不 sleep 到半开到期——快速失败把
决定权交还调用方(run 记失败,下一 run 自然重试;桌面场景 run 间隔分钟级,
300s 级自愈与之匹配)。

### 4.5 懒建 per-upstream client 构建失败(prd D10,grill round 2 补拍)

上游 client 懒建失败(socks 缺 `httpx[socks]`/socksio → ImportError,或代理
URL 协议非法 → ValueError)**不计数、不换上游,直接冒
`ProxyConfigError`**(error_type=proxy_config;复用现有构建错误映射,
fetch_base.py:1501-1508)。理由:计数换上游会把「依赖缺失」伪装成
proxy_network 连败摘除——socksio 缺失的池每上游都被烧红,真相(装 extras
就好)被健康模型吃掉。`proxy_config` 同样 startswith("proxy_"),registry
「不清 hint+短路链」行为与现状 mount 期 ProxyConfigError 完全一致,不变量
面零新增分叉。

## 5. 消费点接线

### 5.1 引擎挂载(fetch_base.py `_prepare_proxy_transport`)

- `proxy_pools.spec(pool_name)` 取规格 → `context.pool_transport_for(pool_name)`
  懒建 facade(内部 `resolve_upstreams` 一次性解析凭据;解析失败结构化报错
  语义与现状一致)。
- `self._active_client = facade`(duck-type,`_send_with_retry` 的
  `.request(...)` 调用形态不变);`self._active_pool = pool_name`;
  `self._active_proxy_url = facade.current_url`(crawl4ai 消费)。
- mount 即选上游:池熔断 → 直接抛 ProxyPoolExhaustedError(§4.4)。

### 5.2 robots(fetch_base.py `robots_for_pool`)

池级一个 RobotsCache,client 参数传 facade(质询修正①)——RobotsCache 只用
`.get(url, timeout=...)`(fetch_base.py:995),facade 委派当前上游,robots
视角随池轮换保持「活出口」。robots 拉取失败沿既有 fail-open 约定
(fetch_base.py:993-999),零新分支。

### 5.3 图片下载环(pipeline.py `_ring_proxy_for_source`)

`client_for_pool(pool_name, resolved, timeout=...)` 改 `pool_transport_for
(pool_name)`;返回 `(facade, facade.current_url, False)`。环内请求经 facade
骑当前健康上游;环的超时从 client 构造参数改为 per-request timeout
(IMAGE_DOWNLOAD_TIMEOUT_SECONDS 经 **kwargs 透传面传,collect.py:445 的
`follow_redirects=False` 同路)。降级 direct 兜底分支语义不变。

### 5.4 浏览器/重型引擎(crawl4ai / stealth_browser / scrapling)

`_active_proxy_url` 语义 = mount 时刻的当前健康上游(design §5.1)。读者
**三处**(grill round 2 修正③):crawl4ai.py:226、stealth_browser.py:727-728、
scrapling.py:410-411——基座 `_prepare_proxy_transport` 统一赋值,故
stealth_browser/scrapling **零代码改动**,行为自动同「会话内不轮换」。
**浏览器会话内不轮换**(BrowserConfig/浏览器参数建后代理固定;会话粘性本就是
浏览器形态的合理行为)——代理链失败照旧冒 ProxyTransportError,链短路
(不变量见 §6);下一个 run/源 mount 时自然选到健康上游。

### 5.5 doctor(cli.py `_probe_proxy_pools`)

逐池改逐**上游**:外层池名保序、内层 `resolve_upstreams` 展开后并入同一
`asyncio.gather` 并行集(cli.py:1184-1215 骨架不动);每条结果增
`upstream_index` 字段(单上游池恒 0,输出对现状是纯增字段);凭据解析失败
语义保留「单上游失败不拖垮其余」。`_proxy_findings`(cli.py:1670)按既有
字段(pool/ok/error_type)继续可消费;文本渲染补上游序号。cli.py 为并行
会话热点文件:实现时先读现状、追加式修改。

## 6. 与降级链的交互(不变量,prd R5)

不变量原文(registry.py:277-295):`proxy_*` 失败(a)不清 hint(b)短路链,
理由「链上其余引擎骑同一条池 transport」。池化后理由仍然成立——池 transport
(run 级共享)熔断对所有引擎同效。四类 error_type:
`proxy_error` / `proxy_timeout` / `proxy_network`(既有)/
`proxy_pool_exhausted`(新)——全部 startswith("proxy_"),registry 零改动。
轮换/健康完全收敛在引擎与 facade 内,**降级链不感知池内部**;引擎冒出的
失败要么是「轮换后仍失败」(ProxyTransportError,消息带尝试上游数与最后
上游 mask 形态)要么是「池熔断」(ProxyPoolExhaustedError)。

## 7. 并发与时钟

- 单线程 asyncio:health/cursor/trial 位的读写都在 await 间同步段,无锁。
  多协程同时到达选择圈:游标环形扫描天然分散;同池并发摘除竞态无害
  (幂等置 removed_at,时戳取后到者,自愈粒度不变)。
- clock 全部走注入的 monotonic(FetchContext.clock);probe_interval 比较、
  removed_at、日志时戳渲染同源。测试注入假时钟,零真等。
- 生命周期:pool_transports 随 FetchContext(= 随 run);`aclose` 关全部上游
  client。D7:不落库、不跨 run。

## 8. 兼容与测试迁移

| 既有测试(test_proxy_transport.py) | 迁移 |
|---|---|
| test_fetch_with_pool_proxy_mounts_shared_proxied_client(:200) | 断言 `context.pool_clients["main"] is engine._active_client` → `pool_transports["main"] is engine._active_client`(facade 身份);recorder 断言不变(facade 内建 client 仍经 monkeypatch 过的构造器) |
| test_fetch_with_pool_proxy_reuses_one_client_across_sources(:227) | 同上,「共享一个对象」语义原样 |
| test_fetch_direct_keeps_context_client(:243) | 断言不动 + **可选加固一行**(grill round 2 采纳):`context.pool_transports == {}` 钉死「direct 路径 facade 也零构建」 |
| 其余 31 项(loader/分类/doctor/mask/residential) | 零改动预期;`raw_url`/`resolve` 保留使 loader 族直接兼容 |

新测试文件 `tests/test_proxy_pool.py`(AC2/AC3 清单见 prd;transport mock
计数证明「熔断零网络」「摘除跳过」,假时钟证明「半开到期/未到期」)。

## 9. 取舍与风险记录

- **字符串池失败语义变化须披露**(grill round 2 D5 附注):混形兼容指
  「YAML 可原样加载、请求照跑」,**不指失败路径逐字节等价**——字符串池从
  「逐源各自重试」变为「3 连败摘除→池熔断快速失败」(R4 题中之义的改进,
  死上游不再被每源反复烧)。spec 小节与 docs 必须明写此行为变化,否则用户
  观感是「号称兼容却变了行为」。AC7 已挂披露项。
- **run 内状态冷启代价**(D7 已核 pipeline.py:898/1011/1150:context 每 run
  新建):每 run 游标回声明序、摘除态清零——死上游每 run 至多浪费一次尝试,
  有界(游标 facade 级共享自限),可接受;换来的是零跨 run 幽灵摘除。
- **超时计入摘除的慢源污染**(D4 采纳):防御=连续语义下健康流量成功清零
  (交错复位)+ 半开 300s 自愈;残余风险场景(池内全部源都慢)结局与 v0.2
  proxy_timeout 链上等价,非回归。已否决窄口径(只计 proxy_error/proxy_network):
  与 `_wrap_proxy_transport_failure` 分类真相分裂。
- **熔断不睡到半开**(§4.4):快速失败 + 下一 run 重试;代价=熔断窗口内首个
  run 必失败一次。桌面手动 run 场景可接受;定时高频 run 场景 300s 内损失
  ≤ 一轮 run。否决「熔断期 sleep 等半开」:管线内不可预期挂起,违背
  「run 有界时长」直觉。
- **浏览器引擎不轮换**(§5.4):crawl4ai 会话粘性;代理挂时该源当轮失败,
  链短路(与现状同),下轮自愈。否决「会话中途重建浏览器」:冷启开销远大于
  一轮等待,且半开会话状态复杂。
- **facade duck-type 而非继承 AsyncClient**:引擎/RobotsCache/图片环三个
  调用面(request/get)全覆盖;风险=未知调用面假设完整 AsyncClient API
  (rg 全树核验过仅这三处消费 `_active_client`,design §1;实现期 C2
  detect-changes 复核)。
- **doctor 输出增字段**:单上游池 upstream_index=0,下游(UI G10 按钮、
  `_proxy_findings`)向后兼容;JSON 消费方按纯增字段容忍(仓内 golden
  回归先例:纯增字段容忍断言形态)。

## 10. 发布/回滚形态

- 单 commit 交付(fetch_base + pipeline/cli/crawl4ai 适配 + 测试 + docs);
  无数据迁移、无协议变更、无配置破坏(字符串形态原样)。
- 回滚 = revert 单 commit;v0.2 形态 YAML 在新代码上继续可跑,回滚后
  upstreams 形态 YAML 会被旧加载器以 `invalid_pools` 拒载(结构化报错,
  非静默)——回滚前需将池化 YAML 还原为字符串形态,此点写入 implement
  收尾注记。
