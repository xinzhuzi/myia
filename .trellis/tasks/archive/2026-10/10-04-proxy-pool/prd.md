# proxy_pool 池化:代理轮换与健康检查

## 需求源

主人批(2026-10-04 /workflow 做软件三连,task.json description):v0.2 已毕单上游
transport(归档 `10-01-v02-proxy-transport`),补池化——轮换策略/被动失败计数/
摘除恢复/每池熔断,全局 pools YAML schema 扩展;探查→grill→实现全流程。
上游池档:`10-03-v12-backlog` prd 节 3(「proxy_pool 对接」)。

**授权口径**:grill 决议一律「按推荐」定稿(主人 7 连全按推荐的既有授权口径,
事后可翻案);本档「已拍板决议」节即定稿形态。

## 现状(2026-10-04 探查,证据 file:line)

> **路径基准注记**:建档期间并行会话将 `src/shishi/` 整包改名 `src/myia/`
> (staged renames 在飞);本档路径与行号锚已对改名后工作树逐一直核
> (fetch_base.py 538/1475/1607/1750/1802、registry.py 278-287、cli.py 1184、
  pipeline.py 1596、crawl4ai.py 223-227、schema.py 288、entry.py 2251——
  行号除 pipeline +1 外零漂移)。若改名回滚,路径前缀同步换回即可。

- **单上游通路已毕**:池声明 `ProxyPools`(name → 单条 URL 字符串)与加载器
  `load_proxy_pools`/`load_proxy_pools_file`(`src/myia/engines/fetch_base.py:538-738`);
  引擎挂载点 `BaseEngine._prepare_proxy_transport`(fetch_base.py:1607-1649);
  每池一个共享 `httpx.AsyncClient`(`FetchContext.client_for_pool`,
  fetch_base.py:1475-1511)+ 同出口 robots 视角(`robots_for_pool`,
  fetch_base.py:1513-1519)。
- **代理失败分类已立**:transport 级失败在代理链上包装为
  `ProxyTransportError`(error_type ∈ proxy_error / proxy_timeout / proxy_network,
  fetch_base.py:224-240、276-290、1802-1819);direct 失败原样透传。
- **降级链短路不变量**:`proxy_*` error_type(1)不清引擎 hint、(2)中止降级链
  (`src/myia/engines/registry.py:277-295`——「链上其余引擎骑同一条池
  transport,必然同错:短路并保留 hint」)。本任务不得破此不变量。
- **消费面五路**:引擎 fetch 挂载(fetch_base.py:1607);图片下载环
  `pipeline.py:_ring_proxy_for_source`(pipeline.py:1596-1630,池 client 以
  IMAGE_DOWNLOAD_TIMEOUT 超时共享;环内请求带 `follow_redirects=False`
  kwargs,collect.py:445——facade 方法面必须 **kwargs 透传,见 D9);doctor
  逐池并行探测(`cli.py:_probe_proxy_pools`,cli.py:1184-1215);浏览器/重型
  引擎直读 `_active_proxy_url` **三处读者**(crawl4ai.py:226、
  stealth_browser.py:727-728、scrapling.py:410-411,grill round 2 修正③);
  桌面 sidecar 经 run 的 `config` 参数(全局 pools YAML 路径)注入
  (desktop/entry.py:2251)。
- **schema 不涉**:`pool:<名称>` 语法(`schema.py:288 _PROXY_RE`)不变;
  pools 节的加载校验全在 fetch_base.py。
- **测试基线**:`uv run --no-sync python -m pytest tests/test_proxy_transport.py -q`
  → **33 passed**(2026-10-04 本会话真跑)。
- **前档遗留**:v02-proxy-transport 的 manual AC(真机本地代理验证一次)仍未
  销账(归档 prd 验收记录节);本任务 AC6 真机项可顺带覆盖单上游形态。

## Requirements

- **R1 池化 YAML 扩展(向后兼容)**:全局配置 `pools` 节每池从「单 URL 字符串」
  扩展为「`upstreams` URL 列表 + 可选策略字段」;v0.2 字符串形态原样合法
  (等价于单上游池)。名称语法、凭据只走 `env:`/`keychain:` 引用、明文拒载、
  scheme 白名单、结构化 LoadError——全部沿用现有加载器规则。
- **R2 轮换策略**:多上游按声明顺序游标轮换,transport 失败即跳过该上游换
  下一个健康上游重试(消耗源 retry 预算);不做加权随机。
- **R3 健康模型(被动)**:每上游连续失败计数,达阈值摘除;摘除经恢复间隔后
  半开单飞试炼,成功复位归队、失败重新摘除。**零后台探活线程/任务**——
  恢复由流量自然触发;doctor 的手动探测不参与运行态。
- **R4 每池熔断**:全部上游摘除时池处于熔断态,后续请求**零网络快速失败**
  (结构化错误 `proxy_pool_exhausted`);熔断解除 = 最早摘除的上游到期半开。
- **R5 降级链不变量保持**:`proxy_pool_exhausted` 与既有 `proxy_*` 三类同族
  (startswith("proxy_")),registry 的「不清 hint + 短路链」行为对四类一致;
  轮换发生在引擎 retry 循环内,降级链不感知。
- **R6 doctor 扩展**:逐池逐上游并行探测,输出逐上游条目(单上游池形态不变)。

## 已拍板决议(全按推荐;grill 记录见下节,事后可翻案)

| # | 议题 | 决议(= 推荐) |
|---|------|----------------|
| D1 | 轮换策略 | **顺序游标 + 失败跳过**(否决加权随机:静态池规模小,权重是用户负担且行为不可预测) |
| D2 | 健康模型 | **被动失败计数摘除 + 半开单飞恢复**(否决主动后台探活:零常驻开销) |
| D3 | 摘除阈值/恢复间隔 | 连续失败 **max_failures=3**(默认)、半开恢复 **probe_interval=300s**(默认);每池 YAML 可覆写 |
| D4 | 失败计数口径 | transport 级三类(proxy_error/proxy_timeout/proxy_network)全计,**连续**语义 + 成功一次清零;HTTP 状态失败(源 4xx/5xx)不计数——代理已送达,锅是源的 |
| D5 | YAML 形态 | **混形兼容**:字符串 = 单上游池;映射 = `upstreams` 列表 + `max_failures`/`probe_interval` 可选 |
| D6 | 熔断粒度 | 池级**派生态**(全摘除即熔断,不设独立熔断状态机/计时器);解除靠最早摘除上游到期半开 |
| D7 | 健康状态生命周期 | **run 内**(FetchContext 生命周期),不落库不跨 run——上次摘除不留幽灵 |
| D8 | 服务商边界 | 本任务=静态多上游池(v12-backlog「池化抽象」落地);**residential:/动态服务商池维持 not-implemented**(v0.3 myia-proxy 插件线,fetch_base.py:142-144 PROXY_SCHEDULE 不动) |
| D9 | facade 方法面与命名(grill round 2 修正①) | `request`/`get` 显式 **kwargs 透传(现网 collect.py:445 已传 `follow_redirects=False`,固定签名必打挂图片环);工厂方法**统一命名 `pool_transport_for(name)`**,`client_for_pool` 留 deprecated alias 一个版本周期 |
| D10 | 懒建 per-upstream client 构建失败归类(grill round 2 补拍) | **不计数、直接冒 ProxyConfigError**(error_type=proxy_config,startswith("proxy_") 落族,registry 行为与现状 mount 期报错一致);否决计数换上游——socks 缺 socksio 会被伪装成 proxy_network 摘除,依赖缺失真相被吃掉 |

## Grill 决议记录(2026-10-04,七问全按推荐)

- **Q1 轮换策略 = 顺序游标+失败跳过**:加权随机否决——池是手写静态清单
  (典型 2-5 上游),权重要求主人量化「上游好坏」实为负担;顺序天然均匀,
  失败跳过即事实降权,确定性可测。
- **Q2 健康模型 = 被动计数 + 半开**:主动探活(后台定时任务)否决——违背
  「管线无常驻服务」的既有形态,且静态上游池流量本身就持续供样;doctor 手动
  探测已覆盖「人主动想知道」的场景。
- **Q3 计数口径 = 三类全计 + 连续 + 成功清零**:「超时也计数」的慢源污染
  风险由交错复位防御——健康流量的成功会清零慢源叠的计数,只有失败主导时才
  摘除;池内仅慢源时全摘除 → proxy_pool_exhausted,与 v0.2 同场景的
  proxy_timeout 链上结局一致,非回归。仅计 proxy_error/proxy_network 的窄口径
  否决(与 `_wrap_proxy_transport_failure` 的分类口径分裂,两套真相)。
- **Q4 默认值 = max_failures 3 / probe_interval 300s**:3 与典型源 retry=2 的
  三次尝试对齐(单上游池一个源烧完重试预算即摘除该上游);300s 半开=5 分钟
  自愈粒度,桌面 run 频率下足够。YAML 可覆写留给真实异质池。
- **Q5 YAML = 混形兼容**:全量改列表否决——v0.2 存量 YAML(含文档样例)零
  迁移成本是硬约束;两形态共用同一校验器,不产生第二套规则。
- **Q6 熔断 = 池级派生态**:独立熔断器(failure-rate 型状态机)否决——静态
  小池上失败率统计无意义,「全摘除」这个派生条件已充分;恢复探活间隔即
  每上游的 probe_interval,不另设池级计时器。
- **Q7 服务商边界 = 静态池 now,动态池留 v0.3**:v12-backlog 主人侧前置
  (「服务商与预算:有」)指向的**服务商 API 动态取 IP**形态归 residential/
  myia-proxy 插件线(PROXY_SCHEDULE 既有排期);本任务交付的「池化抽象」=
  多上游声明+轮换+健康,服务商实装在其上叠加而非其中。

### 质询修正(起草→定稿被 grill 改掉的部分)

1. **robots 视角**:初稿拟「每上游一个 RobotsCache」→ 修正为**池级一个
   RobotsCache 骑池 facade**(robots.txt 是目标站属性非出口属性,按上游复制
   只会翻倍探测;facade 委派当前健康上游,见 design §5.2)。
2. **半开并发**:初稿拟「半开上游临时全量再入」→ 修正为**严格单飞试炼**
   (试炼位一个,避免死上游复联瞬间吃满流量;见 design §4.3)。
3. **pool_clients 容器形态**:初稿拟保留 `dict[str, AsyncClient]` 键加后缀
   → 修正为**值统一为池 transport facade**(单上游池也走 facade,`is`
   身份断言与「同池多源共享一个对象」的既有测试语义原样存活;见 design §5.1)。
4. **轮换节奏**:初稿拟「同上游吃满 backoff 重试再换」→ 修正为**transport
   失败即换下一个健康上游**(同一上游不连续吃两次尝试,池大小 >1 时;死上游
   立即让位,重试预算花在活上游上;见 design §4.2)。

## Grill 决议记录 round 2(2026-10-04,质询 21 项:17 ok / 3 change / 1 missing;修正与补拍全按推荐采纳)

ok 17 项(D1-D8、facade 身份兼容、RobotsCache 池级、doctor 逐上游、熔断不睡、
迁移表 33→2、CI 零外网测法、pools 缺省零影响、proxy_* 家族/registry 零改动、
门禁纪律、回滚形态)关键依据已由质询方实读复核(契约断言 tests:223/:240、
context 每 run 新建 pipeline.py:898/1011/1150、ci.yml:23、loader 缺节空声明
fetch_base.py:654-655 等),本侧抽查直核一致(stealth_browser 读者、collect
kwargs 调用点、ci.yml:23)。

- **修正①(facade 方法面与命名,→D9)**:request/get 必须显式 **kwargs 透传
  ——collect.py:445 现网传 `follow_redirects=False`,固定签名图片环直接打挂;
  `client_for_pool` 与 `pool_transport_for` 同物两名,定稿统一后者,前者留
  deprecated alias。
- **修正②(半开单飞清位语义)**:`trial_in_flight` 清位必须 try/finally 且
  覆盖非 TransportError 异常与 **CancelledError**——桌面 sidecar 120s 壳超时
  会 `asyncio.wait_for` 取消在飞请求,取消路径不清位 = 该上游本 run 永久占坑
  =永久摘除,最坏池提前永久熔断。
- **修正③(浏览器消费面补 scrapling)**:`_active_proxy_url` 读者实为三处
  (crawl4ai.py:226、stealth_browser.py:727-728、scrapling.py:410-411);基座
  统一赋值使 scrapling/stealth_browser 零代码改动,行为同「会话内不轮换」;
  现状节与 design §5.4、implement 0.2/C2 已同步补齐。
- **补拍④(懒建 client 构建失败归类,→D10)**:不计数、直接冒
  ProxyConfigError;计数换上游会把 socks 缺 socksio 伪装成 proxy_network
  摘除,依赖缺失真相被吃掉。
- **附注落实(D5)**:字符串池失败语义会从「逐源各自重试」变为「3 连败摘除
  →池熔断快速失败」——是改进且属 R4 题中之义,但 spec 小节与 docs 必须
  **明写该行为变化**,否则用户观感是「号称兼容却变了行为」(AC7 增此披露项)。
- **可选加固采纳**:迁移 direct 零构建用例(tests:243)时补一行
  `context.pool_transports == {}` 断言,钉死「facade 也零构建」(一行成本)。

探查方法教训入档:rg 多文件参数下输出乱序(线程并行),truncated 输出的
「未见命中」不可当零命中判据——stealth_browser 读者首轮漏看即此因,单文件
复跑才坐实。

## Acceptance Criteria

- [x] AC1 兼容:v0.2 单上游字符串 YAML 原样可跑;`tests/test_proxy_transport.py`
  既有 33 项语义保持(允许等价断言迁移,迁移项逐一列名于 implement.md)
  → 终检冒烟(2026-10-04)passed:44 passed(基线 33+加载器新增零失败);B6 迁移
  4 项逐名跑 PASS;e2e C2 字符串池=单上游池+默认策略 3/300 PASS
- [x] AC2 轮换/摘除/半开:新测试文件 `tests/test_proxy_pool.py` 覆盖——顺序
  轮换、失败跳过、连续计数摘除、成功复位、半开到期再入、半开单飞、未到期
  跳过、clock 注入零真等
  → 终检冒烟 passed:全套 27 项 PASS + e2e 矩阵 M1-M4(轮换 A,B,A,B/摘除@t0/
  未到期零复骑/半开复位归队)38 PASS exit 0;引擎级 E1(A 死 B 活 retry=2,A 只吃
  一次尝试)PASS
- [x] AC3 池熔断:全摘除后零网络快速失败(transport mock 计数为证)、
  `proxy_pool_exhausted` 进 proxy_* 家族、registry 短路+不清 hint 不变量测试
  → 终检冒烟 passed:e2e M5 传输层计数零增量+error_type=proxy_pool_exhausted+
  startswith("proxy_")+recovery_in_seconds=300;具名单测两件 PASS
- [x] AC4 doctor:多上游池逐上游并行探测,单上游池输出形态与现状等价
  → 终检冒烟 passed:test_doctor_probes_every_upstream_with_index_fields(逐上游
  各探一次+纯增两键+单上游行=既有键集)与解析失败隔离用例逐名跑 PASS
- [x] AC5 回归:全量 `uv run --no-sync python -m pytest -q` 零新红(并行会话
  在场的预存红按归属豁免,列名)
  → 终检冒烟 passed:3495 passed, 19 skipped, 0 failed(66.74s,full-pytest.log);
  零红故无需豁免列名
- [ ] AC6 **[manual]** 真机:本地起两个代理上游(一个故意坏)跑多源品类,
  观察轮换/摘除/恢复日志(顺带销 v02-proxy-transport 遗留的单上游真机验证;
  凭据不进仓库,结果记任务日志)
  → 终检冒烟 manual(未跑):真机代理冒烟属主人侧,CI/本地零外网口径不可替代,
  如实标 manual;已登记收口 leftovers
- [x] AC7 文档:docs/zh + docs/en 的全局配置/pools 节双语同步(spec:
  python/index.md 增池化小节);**须明写字符串池失败语义变化**(逐源各自
  重试 → 3 连败摘除→池熔断快速失败,grill round 2 D5 附注)
  → 终检冒烟 passed:docs/zh/schema.md 与 docs/en/schema.md pools 节双语在位
  且均明写 v1.2 行为变化披露;spec python/index.md:53-60 池化小节在位;
  pytest tests/test_docs.py -q → 92 passed

## 非目标

- residential: 及服务商 API 动态住宅池(v0.3 myia-proxy 插件线;PROXY_SCHEDULE
  的结构化 not-implemented 报错维持)
- 跨 run 持久化健康状态/摘除记忆(留池议:D7)
- 代理池管理 UI 面板与 G10 连通性按钮的 UI 侧改造(v12-backlog 第 6 项,
  另拆任务;本任务只保证 doctor 数据面就绪)
- 主动后台探活/心跳(D2 否决)
- 按上游分别配 robots/限速策略(限速仍按目标 host,与出口无关)

## 衔接

- v12-backlog 节 3 的「池化抽象」→ 本任务;「服务商实装」→ Q7 划归插件线,
  池档该节回标由主人收口时定。
- 完成后 `10-03-v12-backlog` prd 节 3 现状行「池化未写」应回标(留主人)。
