# Implement:10-04-proxy-pool(2026-10-04 定稿)

> 查改分家:动笔前重读 design.md(§编号下文引用)与 prd「已拍板决议」;
> 行号锚以 2026-10-04 工作树为准。热点纪律:pipeline.py / cli.py /
> docs/*/schema.md 有并行会话在飞——每处先读现状、追加式、不重排他人改动。

## Stage 0:基线

- [x] 0.1 `uv run --no-sync python -m pytest tests/test_proxy_transport.py -q`
  → **33 passed**(实现会话 2026-10-04 真跑,与建档基线一致);外来未提交
  改动清单见工作树 git status(24 项,含 desktop/ 与 docs/ 批量改动,
  归属并行会话,验收豁免)
- [x] 0.2 `rg -n '_active_client|_active_proxy_url' src/myia` 逐文件单跑:
  `_active_client` 消费只在 fetch_base.py(:1564/:1621/:1638/:1641/:1775,
  即基座内部);`_active_proxy_url` 三读者坐实——crawl4ai.py:226/275/316/321、
  stealth_browser.py:727-728、scrapling.py:327/410-411(grill round 2 修正③
  无漂移)。**图片环消费面补充实读**:collect.py:444/:552 的 `client.stream(...)
  timeout=... follow_redirects=False` 与 :344 `_client_egress_is_proxied`
  经 `_mounts` 内部面观测 —— facade 因此补 `stream` 方法与
  `is_proxy_egress` 标记(design §3「未知调用面」风险项的实锤,改动注记见 C1)

## Stage A:声明层(纯数据,独立可测)

- [x] A1 `PoolSpec` dataclass + `ProxyPools.spec/upstream_urls/resolve_upstreams`
  (design §2);`raw_url`/`resolve` 保留单上游语义(多上游池取第一个);
  构造函数兼容 v0.2 `{name: url}` 字符串映射(测试/内建直接构造面)
- [x] A2 `load_proxy_pools` 混形分支 + `_pool_spec_from_mapping`(新 code
  `invalid_pool_upstreams` / `invalid_pool_policy` / `unknown_pool_field`,
  布尔冒充数值一并拒);`load_proxy_pools_file` 零改动
- [x] A3 混形加载测试 10 项入 tests/test_proxy_transport.py(字符串等价/
  两形态并存/空列表/缺键/逐上游错误路径 `$.pools.<name>.upstreams[i]`/
  策略越界/布尔与字符串拒/未知键/列表形态池拒/映射上游明文拒)

## Stage B:运行时(核心)

- [x] B1 `UpstreamHealth` + `ProxyPoolTransport`(fetch_base.py):request/get/
  **stream**/aclose 四面显式 `**kwargs` 透传(D9;stream 是图片环实读补充,
  见 0.2)、懒建 per-upstream client(构建失败不计数直接冒 ProxyConfigError,
  D10)、`_scan_admissible` 选择圈(healthy / 到期半开单飞 take_trial / 跳过)、
  `peek_admissible`/`ensure_operable`(mount 期零状态变更 + 熔断零 I/O 拒绝)、
  masked_current、upstreams_tried/total(错误消息口径)、注入 clock;
  `trial_in_flight` 清位 finally 全终态覆盖(成功/transport 失败/非
  TransportError/CancelledError)
- [x] B2 `FetchContext.pool_transports` + `pool_transport_for(name)`(D9 统一
  命名;凭据在首次创建时 `resolve_upstreams` 一次性解析)+ `pool_clients`
  property / `client_for_pool` / `aclose_pool_clients` deprecated alias
  (一个版本周期)+ `aclose_pool_transports`
- [x] B3 引擎接线:`_prepare_proxy_transport` 走 facade(熔断 mount 期
  `ensure_operable` 零 I/O 拒绝;`_active_proxy_url` = mount 时刻可 admit
  上游,会话内不轮换入 docstring);`_send_with_retry` 零改动(facade 每
  request 自身选择 = per-attempt 选上游,transport 失败即换下游由游标
  语义自动成立);`_wrap_proxy_transport_failure` 消息带「已试 N/M 上游」
  + masked_current
- [x] B4 `ProxyPoolExhaustedError`(error_type=proxy_pool_exhausted,pool +
  recovery_in_seconds)入 `__all__`;classify_exception 零改动验证(FetchError
  子类自带 error_type)
- [x] B5 `tests/test_proxy_pool.py` 27 项:顺序轮换/单上游退化/失败跳过
  (引擎级)/未到期跳过/连续计数摘除(时戳=注入 clock)/成功复位/HTTP 状态
  不计数不清零/半开到期再入/半开失败立即重摘除/半开单飞(async 传输层事件
  控制)/取消路径清位(task.cancel 后 slot 复位、再入成功)/池熔断零网络
  (transport 计数为证 + recovery 可解释)/mount 期熔断拒绝/registry 短路
  不清 hint/字符串池语义变化(3 连败熔断,retry 未烧完零网络收场)/
  kwargs 透传(extensions 观测 per-request timeout)/stream 健康口径/
  is_proxy_egress 标记/AClose 全关/mount URL/错误消息掩码/alias 同物/
  pools 未声明零影响/doctor 逐上游 index 字段与单上游形态等价/解析失败隔离/
  映射上游非字符串拒载。全部 FakeClock 零真等 + mock 传输层零外网
- [x] B6 迁移 4 项(全列名,AC1):
  1. `test_fetch_with_pool_proxy_mounts_shared_proxied_client`
     —— `pool_clients["main"]` → `pool_transports["main"]`(facade 身份)
     + 追加 alias 同物断言;recorder 断言零改动
  2. `test_fetch_direct_keeps_context_client` —— 原断言不动 + 追加
     `context.pool_transports == {}` 加固行(grill round 2 采纳)
  3. `test_client_for_pool_bad_scheme_is_structured` →
     `test_upstream_client_build_failure_is_structured_config_error`
     (旧签名直传 URL 已 deprecated,等价面 = facade 懒建期构建失败,
     断言 invalid_proxy_url + 不计数)
  4. `test_doctor_pool_probes_run_concurrently_in_declared_order` ——
     duck 型 `_Pools` 补 `resolve_upstreams`(断言零改动)
  其余 29 项零改动;`pytest tests/test_proxy_transport.py
  tests/test_proxy_pool.py -q` → **71 passed**
- [x] 门禁 G1(池化核心):71 passed + 邻域 `pytest -q tests/test_proxy_pool.py
  tests/test_proxy_transport.py tests/test_proxy_plugin.py tests/test_fetch_base.py
  tests/test_registry.py tests/test_pipeline.py tests/test_vision_collect.py
  tests/test_vision.py tests/test_crawl4ai.py tests/test_scrapling.py
  tests/test_stealth.py tests/test_firecrawl.py tests/test_cli_full.py`
  → **463 passed, 6 skipped 零新红**(全量 tests/ 留 G2 脚本统一跑)

## Stage C:消费面适配

- [x] C1 图片环(pipeline.py `_ring_proxy_for_source`):`pool_transport_for`
  + `ensure_operable`(熔断/解析失败照旧降级 direct 不炸环),返回
  (facade, mount 上游 URL, False);per-request 超时由 collect.py 现网
  `timeout=DOWNLOAD_TIMEOUT_SECONDS` 显式传(facade kwargs 透传面);
  pipeline.py:1150 `aclose_pool_clients` → `aclose_pool_transports`;
  **追加改动**:collect.py `_client_egress_is_proxied` 首查
  `is_proxy_egress` 标记(4 行,含 rationale)——facade 无 `_mounts`
  内部面,懒建 client 未建时若判直连,经代理图片会全灭 ssrf_rebind
  (collect.py:429-433 实测判例同宗);`_proxy_findings` 兼容(pool/ok/
  error_type 键不变)
- [x] C2 浏览器/重型引擎:基座统一赋值 `_active_proxy_url =
  transport.ensure_operable()`,三读者(crawl4ai/stealth_browser/scrapling)
  零代码改动(rg 逐文件复核);「会话内不轮换」写入 `_prepare_proxy_transport`
  docstring
- [x] C3 doctor(cli.py `_probe_proxy_pools`):逐池 `resolve_upstreams` 展开、
  池内并入同一 asyncio.gather(并行集 = 外层 gather × 内层 gather,同一事件
  循环拍内全量在飞);每行 `upstream_index`/`upstreams`;文本渲染多上游池
  补 `#N` 序号(单上游池输出与既往等价,AC4);解析失败行保持单条 +
  mask 打码
- [x] C4 测试:doctor 逐上游两用例(真 ProxyPools 混形 + fake_check;
  单上游行键集 = 既有键 + 纯增两键等价断言)+ 图片环 egress 标记用例
  (is_proxy_egress / 未建 client 也判代理 / 直连判定不变);既有
  test_vision_collect.py 池用例经 alias 零改动通过
- [x] 门禁 G2(消费面):邻域 463 passed(上述清单)零新红;全量 tests/ 与
  detect-changes 由收口脚本统一跑(本会话不提交,无 staged 面;改动面
  核验 = `git diff --stat` 十文件清单,见下)

## Stage D:文档与收尾

- [x] D1 docs/zh + docs/en schema.md 各追加「全局配置 pools」节(字符串
  样例保留 + upstreams 形态样例 + 运行语义 + **失败语义变化披露**);
  en 侧同款双语同步
- [x] D2 spec:`.trellis/spec/python/index.md` 末尾追加「代理池池化」节
  (声明形态/运行时/熔断/不变量四类 error_type + registry、schema 零改动
  红线/行为变化披露/回滚注记)
- [x] D3 回滚注记:已写入 spec 小节与 design §10;commit message 由收口
  会话带上(本会话不提交)
- [x] D4 AC6 [manual] 登记遗留:真机双上游(一坏)验证 + 顺带销
  v02-proxy-transport 单上游真机欠账——留主人,凭据不进仓库
  → 登记完成(2026-10-04 终检):prd AC6 如实标 manual + 收口 leftovers 在案;
  真机验证本体留主人
- [ ] D5 v12-backlog 节 3 回标建议(留主人收口时定,不在本任务内改档)
  → 终检时点 v12-backlog prd 树上仅 G6 消号注记(b234 批),节 3 池化回标
  仍未落——按本档原口径留主人

## 实现会话改动面(2026-10-04,未提交,供收口核验)

src/myia/engines/fetch_base.py、src/myia/pipeline.py(两处)、src/myia/cli.py
(两处)、src/myia/vision/collect.py(一处)、tests/test_proxy_transport.py、
tests/test_proxy_pool.py(新)、tests/test_docs.py(pools 顶层块按形态路由到
load_proxy_pools,反漂移保障不放松)、docs/zh/schema.md、docs/en/schema.md、
.trellis/spec/python/index.md —— schema.py / registry.py / desktop/ 零改动。

**定向自测终值(2026-10-04 实跑)**:`pytest -q tests/test_proxy_pool.py
tests/test_proxy_transport.py` → 71 passed;proxy/engines 邻域 13 文件 →
463 passed 6 skipped;全量 `pytest -q tests/` → **3478 passed, 19 skipped,
零失败**;ruff 全过。
