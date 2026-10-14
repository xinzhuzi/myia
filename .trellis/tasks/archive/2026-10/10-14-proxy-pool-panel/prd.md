# 代理池管理面板(V1 只读)

## Goal

独立「代理池」屏(路由 `/proxy-pool`,侧栏「配置」组):**出口列表 / 按需测活 / 探测成功率统计**,V1 严控为**只读面板**——零引擎改动、零写回、零后台探活、零图表库。数据面全部骑既有链路:doctor 逐上游探测(引擎 10-04 归档 f759c87)+ G10 一键化通道(`doctor` config_auto);唯一新增后端面 = 桌面层「探测快照历史」持久化(2 个新 sidecar 方法),补齐成功率统计的数据缺口。

母任务口径:`10-03-v12-backlog` prd 第 6 项远期形态(出口列表/测活/成功率统计,对标 jhao104/proxy_pool;与 proxy_pool 后端、G10 测试按钮同族)。本件是该形态的**第一档(只读)**,先窄后宽。

## 红线(踩任一条 = 设计返工)

1. **零后台探活**:探测只由用户点按钮触发;挂载/切屏零网络。jhao104 的 apscheduler 定时采集/复检与 10-04 归档 D2 决议直接冲突(「被动失败计数摘除 + 半开单飞恢复,否决主动后台探活」,archive/2026-10/10-04-proxy-pool/prd.md 决议表 D2 行 + 非目标「主动后台探活/心跳(D2 否决)」),只借它的数据字段形状,不借调度器。
2. **零引擎改动**:不在引擎侧加累计计数/落库——D7「健康状态生命周期 = run 内,不落库不跨 run」是归档决议,翻案不属本件。`UpstreamHealth` run 内即焚(engines/fetch_base.py:954-966);pipeline 运行统计也不带代理计数(`rg "proxy.*stat|proxy.*count|proxy.*fail" src/myssia/pipeline.py` 零命中,本机亲验)。
3. **成功率口径必须明写**:面板能给的只有「**探测成功率**」(doctor `check_proxy_connectivity` 语义),**不是**真实流量成功率。屏内文案与本文档同款声明,不得写成「成功率」裸词误导。
4. **凭据打码到底**:上游永远只以 `mask_proxy_url` 形态出现(engines/fetch_base.py:471;「凭据永不入结果」:1250);持久化文件同理只存打码行。`exit_ip` 非凭据可显示。凭据值编辑继续只走钥匙串(settings-screen.tsx:1284-1290 代理池卡「池凭据入钥匙串」),URL 与凭据两分离面不在 UI 合并明文。
5. **不写回 pools.yaml**:上游增删改/结构写回 = G10 prd.md:7 明记的协议缺口(「属远期代理池面板族」),且 yaml-editor 待拍板 3 未定(archive/2026-10/10-03-yaml-editor/prd.md:17;v112 design.md:229 顺延回标;settings-screen.tsx:230-231 现行注记)。V1 只读,V2 再收口(见「留待 V2」节)。写回将来必须过 `load_proxy_pools` 同一校验器(engines/fetch_base.py:800:凭据引用规则 env:/keychain: 明文拒载 + 结构化 LoadError),否则面板写出坏 YAML 打挂全部 run。
6. **不整搬库存表 UX**:jhao104 是上千动态 IP 的免费采集池;MYIA 是手写静态池(典型 2-5 上游,顺序轮换)。面板做成「**每声明上游的健康卡**」+ 按池分组,不做代理库存大表格/评分。
7. **许可面**:jhao104 与本仓同为 MIT(其 LICENSE 亲读,Copyright (c) 2017 J_hao104),且本仓纪律 = 只借设计不抄码;若未来逐字抄片段须保留其版权声明。

## 既有交付(全部本机亲验,不重做)

| 既有件 | 锚点 | V1 用法 |
|---|---|---|
| 引擎池声明/加载/校验 | `PoolSpec`(max_failures=3/probe_interval=300)engines/fetch_base.py:576-587;`load_proxy_pools` :800;`load_proxy_pools_file` :899 | 零改动;doctor 应答即其投影 |
| 池运行时(轮换/被动健康/熔断) | `ProxyPoolTransport` engines/fetch_base.py:969-1243;`ProxyPoolExhaustedError` :252;`pool_transport_for` :1986 | 零改动(run 内自治,V1 不观测) |
| doctor 逐上游并行探测 | cli.py:3123-3183 `_probe_proxy_pools`(全上游同池并行 gather,总耗时≈最慢上游,120s 壳超时内回话;`upstream_index`/`upstreams` 纯增键;单池解析失败隔离);`_doctor_proxy` section={config,pools} cli.py:4154-4180 | 原样复用,数据源 |
| 探测应答行(打码) | `ProxyCheckResult.to_dict`:ok/message/proxy_url(打码)/latency_seconds/status_code/**exit_ip**/error_type,engines/fetch_base.py:1246-1271;exit_ip 产出 :1340-1354;`check_proxy_connectivity` :1274(doctor 专用,管线永不调) | exit_ip 已在应答、UI 未渲染——V1 补渲染即可 |
| sidecar doctor + G10 一键化 | entry.py:1543-1576 `_m_doctor`(config_auto 发现 `<home>/pools.yaml`,手填永远赢,非布尔 invalid_params);settings-screen.tsx:1000-1008 `handleProbe` 两态(有路径 {config}/留空 {config_auto:true});doctor-verify.tsx:140-174 三态 Badge(连通·延迟/不通/未探测)+ 已加载配置路径行 + auto-miss 提示行 | 探测交互范式照抄;设置屏本体零改动 |
| 池凭据入钥匙链 | settings-screen.tsx:985-998(`saveSecret`→`secret.set`);settings/api.ts:201-204 `proxySecretName`=`myia/proxy/<pool>` | 不动;空态指引链接过去 |
| 协议注册表与对账纪律 | `_HANDLERS` entry.py:7115(现 93 方法,sidecar-protocol.md:19 镜像一致);`test_method_registry_full_reconciliation` 动态对账例(G10 交付);PROTOCOL_VERSION 现值 15(entry.py:532,开工须实读) | 新方法走三件套(见 R1) |
| 屏族范式 | App.tsx:55-66(现 12 屏 react-router Route);sidebar.tsx NAV_GROUPS「配置」组(源管理/YAML配置/Telegram/飞书/微信/机器人凭据);screens/<name>/ 自带 api.ts+vitest(settings/yaml-editor 双例) | 新屏照此并入门族,不新造画布 |
| `<home>` 文件读写先例 | `gates.get`/`gates.save` 读写 `<home>/gates.yaml`(sidecar-protocol.md 注册表 61-62 行段) | 快照历史文件落 `<home>` 同判例 |
| 探测超时参数 | CLI `--probe-timeout` 缺省 10s(cli.py:947);sidecar 壳单请求硬超时 120s(entry.py:3305-3306 注记 main.rs REQUEST_TIMEOUT) | 透传不改缺省 |

## Requirements

### R1 sidecar 新方法族 `proxy.*`(2 个,entry.py)

1. **`proxy.probe`** — params `{config?: string, config_auto?: boolean, probe_timeout?: number}`(形状 = DoctorParams 子集,校验同门:config_auto 非布尔 → invalid_params):
   - 实现 = `payload = _m_doctor(params)`(字面内部复用,零逻辑分叉)→ 应答 = doctor 应答**原形状** + 纯增键 `snapshot: {persisted: boolean, reason?: string}`(persisted=false 时给原因,如 `no_home`/`write_failed`);随后把 `payload.proxy`(config + pools 打码行)作为一条快照追加落盘。落盘失败不 fail 探测(探测结果已到手,persisted=false 如实回)。
   - dev 无 home(ctx.home=None)→ 探测照跑、`persisted:false, reason:"no_home"`(G10 dev 回退同款降级)。
2. **`proxy.history`** — params `{limit?: number, pool?: string}`,零网络纯读:
   - limit 钳制 [1,100] 缺省 20;pool 给值时只回该池行;
   - 应答 `{snapshots: [{at: ISO8601, config: string|null, pools: [doctor proxy.pools 原行]}...], count, truncated:boolean}`,新→旧;
   - 读侧容错:坏行/不可解析行跳过计数如实(同 logs backfill 坏行跳过先例);文件不存在 = 合法空表 `{snapshots:[], count:0, truncated:false}`。
3. **持久化落点**:`<home>/proxy-probe-history.jsonl`——一行一条快照 `{at, config, pools}`(pools 行已打码,红线 4);append 后超 200 条裁最旧并原子重写(原子写先例 entry.py `_atomic_write_text`);无 home 不落盘。
4. **协议三件套**(alert-rules 先例,sidecar-protocol.md:146 段):① PROTOCOL_VERSION 开工实读后 +1(现 15)——**已作废(设计拷问修正①):纯加法不 bump**(循 entry.py:524-531 v15 后纯加法批先例;alert-rules 段是 bump 时代遗物已被取代);② sidecar-protocol.md 注册表补 2 行、计数 93→95;③ 对账例 `test_method_registry_full_reconciliation` 保持绿(动态断言,自动跟)。

### R2 前端类型与客户端(lib/api/)

- types.ts `ProxyPoolStatus`(现 :245-252)显式补 `exit_ip?: string | null`、`upstream_index?: number`、`upstreams?: number`(现在只靠 index signature 兜底,执行者不该靠猜);
- 新类型 `ProxyProbeResult`(= DoctorResult + snapshot 键)、`ProxyHistorySnapshot`/`ProxyHistoryResult`;
- client.ts 增 `proxyProbe(params)` / `proxyHistory(params)` 两方法(doctor 方法在 :198,同款封装)。

### R3 新屏「代理池」(desktop/ui-src/src/screens/proxy-pool/)

- **接线**:App.tsx:55-66 块增 `<Route path="proxy-pool">`;sidebar.tsx NAV_GROUPS「配置」组末尾增 `{to:"/proxy-pool", label:"代理池", icon: Globe}`(Globe = 设置屏代理池卡同款图标,settings-screen.tsx:1283);命名直白扁平,不造新词。
- **头部·配置与探测**:配置路径输入(placeholder「留空=自动探测 <数据根>/pools.yaml」)+「探测」按钮;两态逻辑照抄 G10 handleProbe(有路径 `{config}`/留空 `{config_auto:true}`),命中路径经应答 `proxy.config` 回显。探测进行中按钮禁用 + 人话等待文案。
- **总览卡**(借 jhao104 /count 的分组聚合形态,纯应答形状借用):池数 / 上游总数 / 最近探测时间 / 可用·不通·未探测三计数(按池分组小计)。
- **每池健康卡**(非库存表,红线 6):卡头 = 池名 + 上游数;逐上游行 = 打码 URL(`proxy_url`)、三态 Badge(连通·延迟秒 / 不通 / 未探测,doctor-verify.tsx:157-163 同款)、`exit_ip`(null 显「—」)、`message` 人话原文、`error_type` 短标签(行内 title 提示)。多上游池按 `upstream_index` 保序。
- **探测历史区**(只读):最近 N 次(缺省 20)快照;每池**探测成功率** = 该池 ok 行数 / 该池总行数(按取用快照窗计算),**口径文案明写「探测成功率,非流量成功率」**(红线 3);呈现 = 文本行 + 简单条形(div 宽度百分比),不引图表库;显示每条快照时间 + 当时配置路径。
- **空态**:无 pools.yaml 命中(auto-miss)→ 沿用 doctor-verify.tsx:169-171 人话提示 + 指引「去设置屏·代理池卡入凭据」;无历史 → 「尚无探测记录,点上方探测开始」;dev 无 home → 说明历史不落盘。
- **挂载零网络**:进屏只调 `proxy.history`(纯读);绝不挂载即探测。
- 屏内文案全人话(「出口 IP」「延迟」「不通原因」),零生造词。

### R4 设置屏零改动

G10 按钮/凭据入钥匙链/doctor-verify 三态行全部原样(settings-screen.tsx / doctor-verify.tsx 零 diff);设置屏探测不落历史(V2 再议统一走 `proxy.probe`)。既有 settings vitest 例必须原样绿(防手滑回归)。

### R5 测试

- **tests/desktop/test_desktop_sidecar_protocol.py**(proxy.* 新例,零外网手法同 G10 AC1——tmp MYIA_HOME 沙箱置 pools.yaml,env 缺失凭据上游 → 解析失败行,不触网):
  1. `proxy.probe` 落盘:探测后 `<home>/proxy-probe-history.jsonl` 恰一行、行内 pools 含打码 proxy_url 与 at/config;应答含 `snapshot.persisted=true`;
  2. `proxy.history` 读回/limit 钳制/pool 过滤/坏行跳过/文件不存在空表;
  3. dev 无 home → `persisted:false reason:"no_home"`,探测应答形状不坏;
  4. 对账例绿(93→95 后动态断言自恰)。
- **ui-src vitest(screens/proxy-pool/)**:挂载只发 proxy.history 零探测(零网络断言 seen 调用表)/探测两态分流/exit_ip 渲染与「—」/每池分组与总览计数/成功率口径文案在/空态三分支/设置屏既有例零回归。
- **门禁**:`uv run --no-sync pytest tests/desktop -q` 全绿;ui-src `npx vitest run` + `npx tsc -b` 零错;`uv run --no-sync ruff check .` 零新红;`gitnexus detect-changes -r shishi --scope unstaged` 亲跑对账。

## Acceptance Criteria

- [x] AC1 sidecar:`proxy.probe` = doctor 原形状 + snapshot 纯增键,落盘打码快照;dev 无 home 降级 `persisted:false/no_home` 不 fail。
- [x] AC2 sidecar:`proxy.history` limit 钳制 [1,100]/pool 过滤/坏行跳过/空文件空表,零网络。
- [x] AC3 协议:sidecar-protocol.md 注册表 95 行与计数注记更新;`test_method_registry_full_reconciliation` 绿。PROTOCOL_VERSION 不 bump(设计拷问修正①,纯加法先例;原 bump 指令作废)。
- [x] AC4 屏:路由 + 侧栏「配置」组可达;挂载零探测;探测两态;exit_ip/逐上游分组/总览卡/历史区(口径文案「探测成功率,非流量成功率」)全渲染;三分支空态人话。
- [x] AC5 设置屏零回归:settings/doctor-verify 相关 vitest 原样绿。
- [x] AC6 门禁:R5 末条全量亲跑过。

## 留待 V2(本件不做,登记防丢)

- 池/上游增删改 + pools.yaml 写回收口(落本面板族还是 yaml-editor = 待拍板 3,需主人拍板;写回过 `load_proxy_pools` 同一校验器 + `.bak` + mtime 乐观锁,yaml.save 先例)。
- 上游摘除即时生效(写回后须想清「run 内摘除态」与「声明态」的关系,不新造常驻)。
- http/https 双端点能力探测(jhao104 validator 双端点思想,doctor 探测参数扩展,不动引擎运行时)。
- 设置屏 G10 按钮统一走 `proxy.probe`(历史全量归一)。
- 历史趋势图(若做,控制拉取量,120s 壳超时约束)。

## Notes

- 调研对标仓库 = github.com/jhao104/proxy_pool(zread 免 clone 取证):仓内「面板」实为 Flask JSON API(六端点 /get /pop /all /count /delete /refresh),无图形 UI;/delete→写回、/refresh→重探、/count→聚合形态、Proxy 对象字段(check_count/fail_count/last_status/last_time/source)→ 快照历史的字段形状蓝本;/pop //get 取用语义对 MYIA 无意义(引擎轮换自治)。
- 引擎侧事实核验(避免执行者再翻):`resolve_upstreams`/`raw_url`(cli.py:3158/3161 调用面)已存在;doctor 应答 `proxy.pools` 行 = cli.py:3149-3154 形状。
- 本档不另立 design.md(改动面窄:1 个屏 + 2 个方法 + 协议三件套,PRD 已到文件级);执行中若写回相关出现新事实,回本档「留待 V2」节登记。
