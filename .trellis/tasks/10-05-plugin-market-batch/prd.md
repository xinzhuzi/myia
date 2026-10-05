# 插件市场批量收录:市面有名爬虫/分析工具(先定引擎层 vs 插件层分工)

## Goal

把市面有名的爬虫/分析工具成批收录进 `plugins/` 市场。**第一阶段先定案引擎链(L1-L6)与插件层的分工**(主人 2026-10-05 指令:「先把这个问题讨论清楚了」),再全量盘点+分批落地。铁律不变:装不上不拦核心。

## 背景:现状两层各自是什么(事实,非提案)

### 引擎层(核心,`src/myssia/engines/`)

- 自动降级链 `direct_api → static_html → crawl4ai ⇄ firecrawl → scrapling → stealth_browser → llm_browser`(`registry.py` 模块文档):回答的问题是「**这个 URL 的结构化内容,用最低成本怎么拿**」。
- crawl4ai/firecrawl/scrapling/隐身浏览器进核心而非插件,机制原因:
  1. 抓取是流水线第一步,**每个源的每次 run 都要用**——若做成插件,「装不上不拦核心」铁律立即被核心自身依赖击穿;
  2. 降级链要做进程内控制流(逐档尝试/失败记账/`engine_hints` 胜者持久化/预算与取消),引擎必须是被调度的库,不是外部进程;
  3. 上游以「库/API」形态被嵌入(pip 装或 BYO endpoint),MYIA **只借其执行机构,不保留其产品形态**;调度/降级/记账是 MYIA 自研。
- 可选依赖纪律:后端缺失=结构化失败(`dependency_missing`)继续降级,不拦链。

### 插件层(`plugins/` + `~/.myia/plugins` 安装根 + manifest 规范)

- 回答的问题是「**给核心加一个它不该自有、可整体失效的能力**」:代理出口池、凭证猎取、OSINT 侦察(Photon 子进程)、变更监控(changedetection.io remote)、无代码平台(Maxun server-only)、抖音采集、aipocket 聚合。
- 已有正规通道先例:**链外源引擎**——`engine: credhunter` 注册进 `ENGINE_REGISTRY` 但刻意不进 `AUTO_CHAIN`,`engines/credhunter.py` 的实现就是「加载 `plugins/myssia-credhunter/adapter.py` 进程内执行」(`engines/credhunter.py` 模块文档)。即**架构上已经允许「插件发行新抓取能力」**:显式选用、单档链、失败=源级结构化失败、不参与自动降级。
- 市场治理:manifest 分级(desktop/remote/server-only)+ 许可红线(AGPL 只桩不抄、GPL 走 submodule 样板=Photon、BSD/MIT 可直借)+ 版本矩阵 + community/ 收录规范。

## 待主人定案的分层裁决(Phase 1 出口)

**问题:引擎层已覆盖「有名的爬虫库」,插件层还承载什么?**

建议答案(待质询/主人裁决):

1. **两层不是竞争,是两问**:引擎=「URL→结构化内容」的通用抓取调度(每个源都路过);插件=「场景能力+生态接入」(特定品类/任务才用,可整体失效,带上游生态与部署形态)。已有的 7 件全部落在这一定义内,无一与引擎链重叠。
2. **逐工具归位判定框**(批量收录时每个工具过一遍,顺序裁):
   - a. 它是「库/API,能把 URL 变结构化内容」且比现有档更强 → 候选**核心链新档**(如 scrapy/crawlee 型库;进链须回答「比 scrapling 强在哪、降级序插哪」);
   - b. 它是「采集能力但非浏览器降级语义」(API 猎取/侦察/平台代抓) → **插件+链外引擎**(照 credhunter 先例);
   - c. 它是「独立平台/服务」(自带编排与 UI) → **remote/server-only 桩+compose**(照 maxun/monitor 先例);
   - d. 它与 MYIA 同物种(本身就是情报/采集编排台,如 Crawlab) → **默认不收**——把竞品包进来当数据源语义牵强,除非用户已有部署实例要接(c 形态);
   - e. 许可/免费路径不过关(connector-selection 硬规则) → 不立项,记档。
3. **桌面优先纪律不变**:desktop 分级=进程内/子进程零 docker;要 docker 的进 server-only。

## 主人 2026-10-05 追问:云 API 花钱 + 第三方留痕 + 自研 vs 借(Phase 1 裁决输入)

**顾虑原文**:「这些 API 会花费钱,还会在别人的服务器上面留下问题吧?很多内容这样方便,还是你自己自研方便呢?」

事实澄清(避免误伤现有架构):

- 引擎链四件全是**本地开源库**(crawl4ai/scrapling pip 装本机跑;隐身浏览器本机 playwright;firecrawl 开源可自部署,云端是可选 BYO-key)——**不是云 API**;项目书面宪法本就排序「本地/自托管 > 多年稳定免费层 > 聚合器只做可选后端,永不默认」(connector-selection spec)。
- 真正会「花钱+第三方留痕」的是**厂商反爬 SaaS**(Zenrows/ScraperAPI/Crawlbase 型):按页计费,且你监控的全部目标 URL 集中经过对方服务器、与你的账号(API key)绑定——对情报工具这是最坏的留痕形态(目标侧留痕是采集固有,厂商侧聚合留痕是我们主动送出去的)。

**✅ 主人已批(2026-10-05「优先使用零成本的爬虫手段」)——以下升级为定案,判定框以此为准**:

- **P0 本地执行硬规则**:收录的每个工具必须「本地跑」(进程内/子进程,开源上游)或「指向自部署实例」(remote 桩指用户自己的部署);厂商 SaaS 型收录=默认不立项(e 路),特殊需要时至多做文档级可选后端,永不成为插件 lane 缺省。
- **自研 vs 借的分工线**:能力是 MYIA 核心回路(采集调度/去重/分类/精评/推送/凭证猎取)→ 自研(credhunter 先例);能力是通用轮子且上游开源健康(浏览器/指纹/反检测/代理测活)→ 借库嵌入,不自研(自研 playwright 级轮子是输局);无开源上游又是核心需要 → 才评估自研或付费。
- 该规则与本仓既有门禁(免费路径/许可红线)叠加生效,不改写。

## 2026-10-05 grill 决议(主人按建议全批 D1-D3;Phase 1 出口达成)

| # | 决议点 | 定案(2026-10-05 主人批) |
| --- | --- | --- |
| D1 | 两层分工定义 + 判定框 a-e(引擎=「URL→结构化内容」通用调度,插件=「可整体失效的场景能力+生态接入」) | **按上文建议答案定案**——7 件现有插件全部落在该定义内,无一与引擎链重叠;判定框作为 Phase 2 盘点表唯一归位依据 |
| D2 | P0 本地执行硬规则(对主人「花钱+第三方留痕」顾虑的回应) | **批准为硬规则**:收录件必须本地跑(进程内/子进程开源上游)或指向自部署实例;厂商反爬 SaaS(Zenrows/ScraperAPI 型)默认不立项(e 路),至多文档级可选后端、永不做缺省 |
| D3 | 自研 vs 借的分工线 | **按建议定案**:核心回路(调度/去重/分类/精评/推送/凭证猎取)自研;通用轮子(浏览器/指纹/反检测/代理测活)借开源库嵌入不自研;无开源上游且核心需要才评估自研或付费 |

> 依据事实(已在档):引擎链四件全是本地开源库非云 API;厂商 SaaS 的「目标 URL 集+账号绑定」是最坏留痕形态;connector-selection spec 宪法排序「本地/自托管 > 稳定免费层 > 聚合器只做可选后端」。

## 2026-10-05 晚主人裁决 D4:e 路不是「不做」,是「门槛化地做」(+设置面配置)

**原文**:「e 路砍掉的不是不做,是要做,但是有门槛的去做,设置里面要加配置的。」

**D4 定案(细化,对 D2 的演进不是推翻)**:

- e 路语义从「不立项记档」改为「**门槛立项**」:除「被覆盖/无增量」类(Selenium/urlwatch 重复件等,门槛无意义)外,e 路各项全部转为门槛件,门槛类型五类:
  1. **付费知情门槛**(Zenrows/ScraperAPI/Crawlbase 型 SaaS):收录为 gated 引擎/插件,激活需设置面显式开关(知情确认:花钱+目标清单经第三方)+ keychain 键;**永不缺省、永不进 AUTO_CHAIN**;
  2. **第三方留痕门槛**(公共 RSSHub 实例等):激活需留痕知情开关;
  3. **自有实例门槛**(同物种例外通道:Crawlab/worldmonitor 等):收录为 remote 桩,门槛=用户自部署实例 endpoint,非物种本身拒绝;
  4. **许可核验门槛**(MediaCrawler/yake):法律门槛,核验通过前不进仓库(设置面无关),核验动作进待办;
  5. **停更知情门槛**(snownlp 型):激活需接受「上游冻结,pin 版自担维护」的知情开关。
- **设置面配置是硬要求**:门槛开关不落在品类 YAML(那会让 AI 生成配置时无意开启),落在**全局配置文件**(gates.yaml,照 vision.yaml 先例)+ **桌面设置屏新分区**(门槛件:开关/警示文案/凭据录入/endpoint 填写)。
- **fail-closed**:gates.yaml 缺失/损坏 = 全部门槛件关闭 + doctor 结构化提示;铁律不变(门槛件永不拦核心)。
- D2 硬规则的存活部分:门槛件**永不缺省**——本地/自托管优先序不变,门槛只是让「用户知情后的选择」有正规的落地通道。

## 2026-10-05 深夜 grill 决议 D5-D9(主人「按推荐」全批;批二动工前最后钉口)

| # | 决议点 | 定案 |
| --- | --- | --- |
| D5 | gated 的 manifest 形态 | **独立字段** `gate: paid \| trace \| platform \| stale`(缺省不声明=无门槛);`TIER_TOKENS` 三元组不动——tier=传输形态、gate=激活策略,正交组合(crawlab=`tier: remote`+`gate: platform`;zenrows 引擎配置=`gate: paid`)。修正 §6.2 早稿「tier 加 gated 词表」(单值枚举装不下组合) |
| D6 | 平台门槛运行时语义 | **组织性不执法**:platforms 开关=设置面知情确认+plugin list「已启用」徽标+doctor info→ok;真执法只属付费引擎(gate_closed)与未来 analysis lane;**不拦用户 direct_api 源**(用户自有 endpoint 自主) |
| D7 | 门槛 CLI 通道 | `myssia gates show --json` / `myssia gates set <kind>.<name> <on|off>`(照 secret 命令族形状;键值经既有 secret 通道);BYO-agent 无桌面可配;技能清单同步一行 |
| D8 | 批二分析件裁剪 | gates.analysis **只立 schema+设置面占位,零分析件落地**(snownlp/recon-ng 留批三,且须先独立质询「分析 lane 挂点:classify 后处理还是 enrich 平行」);AC9 缩为 web-check/social-analyzer 两桩+trafilatura 结案 |
| D9 | 公共实例检测 | 本轮不做,记 backlog;third_party_trace **当前无执法点**,留痕保护=README 知情文案(如实注记,不装作有执法) |

## 2026-10-05 批三前置质询决议 D10:分析 lane 挂点定案(D8 悬案闭)

> 主人令「按照你的建议做完它」授权按推荐直接定案;**翻案权保留(记档,翻案即改)**。质询依据:pipeline.py 实况(fetch→classify→dedup→analyze→push,`EXECUTED_STAGES` pipeline.py:233)+ gates.py 实况 + design §6(D4-D9);上游许可/活跃度本日 gh api 复核(snownlp=MIT/最后推送 2020-01-19;yake=AGPL 文件(NOASSERTION)/最后推送 2026-02-11=**活跃**;MediaCrawler=非商业学习许可 1.1/最后推送 2026-10-04=活跃)。设计细则见 design §7。

| # | 决议点 | 定案 |
| --- | --- | --- |
| D10-1 | 分析件 lane 挂点 | **enrich 平行:挂 `_stage_analyze` 阶段内(dedup 之后、push 之前),与 LLM 精评同位互补;不是 classify 后处理**。理由(代码实况):(a) 开销位置——dedup(pipeline.py:1794)先杀 `dedup_seen` 再持久化幸存者,classify 后处理会把 snownlp 子进程/yake 抽取烧在即将被去重丢弃的条目上,每轮重复浪费;(b) 阶段契约——classify 是过滤器(未命中即丢,pipeline.py:1770),analyze 是装饰器(「scoring decorates, it does not filter」pipeline.py:1864),情感/关键词是装饰不是过滤,挂进过滤器阶段会诱使分析结果参与丢弃决策→分类结果依赖插件在位性→击穿「装不上不拦核心」铁律;(c) 失败容器——classify 条目失败走 `report.failures` 翻 partial(pipeline.py:546),分析件失败(uv_missing/超时/dependency_missing)是常态降级,必须走 warnings 通道(enrich 先例 pipeline.py:1898);(d) 执法先例——`_stage_analyze` 已有「开关关=零开销直通」形状(pipeline.py:1872),classify 零配置面;(e) D6 措辞本就把真执法预留給「付费引擎(gate_closed)与未来 analysis lane」。爆炸半径已跑:`gitnexus impact -r shishi _stage_analyze --direction upstream --kind Method --summary-only`=0 直接调用方/LOW(run() 内 flow 字典派发是唯一生产引用,pipeline.py:1082),钩子封闭在阶段方法内部 |
| D10-2 | lane ↔ gates.analysis 执法关系 | **真执法(dispatch 级),非组织性**:每轮 run 在 lane 入口 `load_gates_fail_closed`(gates.py:432,照 vision ring 每轮装载先例 pipeline.py:1658——设置面改动下一轮即生效)→ 逐件 `gate_open(config, "analysis", <key>)`(gates.py:492);**gate 关=零开销 skip**:不 import adapter、不 spawn 子进程、条目零触碰,仅一次字典查找——与 SaaS 引擎的 `gate_closed` 结构化失败(saas.py:70,引擎「被品类请求后被拒」)刻意不同:lane 关=正常未启用态=doctor info+debug 日志,无 run 可见痕迹。fail-closed:gates.yaml 缺失/损坏=全关=lane 不跑(D2 永不缺省存活)。**逐件键名以 `plugin_gate_key`(gates.py:499)为准**:myssia-snownlp→`snownlp`、myssia-yake→`yake`;design §6.1 样例键 `snownlp_sentiment` 与 gates.py:494 docstring 例键是实现前早稿,批三一律用 plugin 派生键(docstring 例键为示意串,无需改码) |
| D10-3 | 三件形态 | **snownlp**(MIT/2020 停更●):`plugins/myssia-snownlp/`,tier: desktop+**gate: stale**(停更知情名副其实)+ adapter 子进程**钉版** `uv run --no-project --with snownlp==<pin>`(urlwatch 先例 plugins/myssia-urlwatch/adapter.py 的 uv 隔离手法;pin 版本号收录时以 PyPI 末版核)+**每轮单次 spawn 批处理**(stdin JSON——snownlp import 即载训练模型,逐条 spawn 会反复载模)+情感分装饰 metadata+错误码照 urlwatch 词表(uv_missing/`*_failed`/`*_timeout`/`*_output_invalid`)+测试 mock 子进程零网络。**yake**(AGPL-3.0 免费档+商业双轨●/活跃●):`plugins/myssia-yake/`,tier: desktop+**不声明 gate**(许可核验已过=D4 类型4 设置面无关;上游 2026-02 仍活跃=stale 徽标失实,本日 gh api 实况定此判)+**lane 激活仍走 gates.analysis.yake**(lane 级纪律:analysis lane 件一律显式开启才跑——缺省关闭来自 D2,不依赖 manifest 徽标;市场面批三把 plugin list/doctor 启用徽标按 lane 成员派生自 analysis 开关,D5 词表不动前提下的最小扩展)+**pip 注入进程内**:adapter 惰性 `import yake`(credhunter 进程内先例 engines/credhunter.py:67),未装=dependency_missing 条目级降级 warning;AGPL 纪律=只声明依赖零复制(pip 运行时自装不构成分发,research 第五波已裁)。**MediaCrawler**(非商业学习许可 1.1●/无 API 无 pip):**最薄=警示型文档桩** `plugins/myssia-mediacrawler/`——manifest(tier: desktop,无 adapter,modes.local.install=用户自行 clone 上游,**不声明 gate**——无程序面即无开关可执法)+README(非商业学习许可醒目警示+零复制声明+「MYIA 不调用不集成不捆绑,收录=市场知识面,用户自装自负边界」);零 adapter/零 compose/零 CLI/零 lane 接线,license 门=D4 类型4(README 级,设置面无关) |

> 附注(如实记):(1) 续跑边界——`_item_checkpoint`(pipeline.py:612)不序列化 `content`,断点续跑条目分析输入退化为 title-only(降级记 warning,不阻);lane 装饰是 run 级重算,不进 checkpoint 载荷。(2) D9 公共实例检测维持 backlog,D10 不解锁。(3) 装饰落 `metadata`(route 规则/模板经 `Item.view()` 可见,pipeline.py:467);items 表回填 best-effort 照 enricher `update_item_scores` 先例(enrich/__init__.py:486),列面批三实现时定。

## Requirements(增补)

- R5(门槛机制,D5/D7 修订):gates.yaml 全局配置装载/校验(照 vision/settings.py 同款 fail-closed)+ manifest **独立字段 `gate`**(paid/trace/platform/stale,非 tier 词表)+ `myssia plugin list` 门槛件分组与启用徽标 + 未启用=doctor info finding + **CLI `myssia gates show/set`**;桌面设置屏新增「门槛件」分区(sidecar 协议 gates.get/save 两方法,照 yaml.save 先例)。
- R6(付费 SaaS 引擎化):Zenrows/ScraperAPI 收录为显式引擎词表新档(永不进 AUTO_CHAIN),fetch 前查 gates 总开关,关闭态=结构化失败 `gate_closed`(与 dependency_missing 语义区分);API key 走 keychain 引用。
- R7(同物种例外通道,D6 修订):Crawlab(BSD,可直借)/worldmonitor(AGPL 只桩)收录为 remote 桩件(`tier: remote`+`gate: platform`),门槛=自有实例 endpoint,**运行时组织性不执法**(list 徽标/doctor 状态面);EasySpider 形态核验(本地 GUI 无 API)如实记档——无服务形态则门槛条件不成立,维持不收并注记理由。

## Phase 2 盘点表骨架(D1 定案后填充;○=待核实,照 supplier-map 惯例)

| 形态类 | 候选(全部 ○ 待核实:上游/license/免费路径/活跃度) | 预期归位倾向 |
| --- | --- | --- |
| 平台/编排型 | Crawlab(BSD)、EasySpider(AGPL,只看不抄)、Huginn、(闭源参照:八爪鱼) | c/d:独立平台→remote/server-only 桩;同物种竞品默认不收 |
| 通用抓取库 | scrapy、crawlee(py)、selectolax/httpx 组合、selenium-wire 族 | a/b:逐个答「比 scrapling 强在哪、降级序插哪」,答不出不进链 |
| 采集专项/反检测 | curl_cffi(指纹模拟)、undetected-chromedriver、Zenrows/ScraperAPI 型 SaaS | 库→a/b 候选;SaaS→e(D2 硬规则) |
| OSINT/侦察 | theHarvester、SpiderFoot、maigret(Photon 已收先例) | b:插件+链外引擎(照 credhunter/Photon 先例) |
| 监控/变更 | changedetection.io(已收)、urlwatch、Huginn watch 型 | c/b:remote 桩或插件 |
| 分析/结构化 | trafilatura(正文抽取)、readability-lxml、newspaper3k 族 | a/b:正文抽取属「URL→结构化内容」语义,进链候选须答增量 |

> 填表纪律:每行须核实 license(AGPL 只桩不抄/GPL 走 submodule)、免费路径(connector-selection 硬规则)、桌面分级(desktop=零 docker;要 docker 的 server-only);≥4 形态类、≥15 工具为 AC2 口径。

## Requirements

- R1(Phase 1):分层定案——**已毕(2026-10-05 D1-D3 决议,见决议表)**;判定框 a-e 为 Phase 2 唯一归位依据。
- R2(Phase 2):全量盘点表——市面有名爬虫/分析工具清单(平台型/库型/采集专项型/分析侦察型/监控型),每行:上游、license、免费路径、形态、建议归位(a/b/c/d/e)、一句话理由;○/● 核实标记照 supplier-map 惯例。
- R3(Phase 3+):按批次落地收录——manifest+README+adapter(或桩)+compose(服务端)+doctor 集成+OFFICIAL_PLUGINS/golden 同步;每批独立可验。
- R4:收录一件动一件的验证(tests/test_plugins.py 官方件参数化+golden),禁止一次性大爆炸提交。

## Acceptance Criteria

- [x] AC1:Phase 1 分层定案回写本档(判定框 a-e 主人过目);裁决前不开任何收录工。**(2026-10-05 回标:D1-D3 主人按建议全批,见上决议表;Phase 2 盘点解锁)**
- [x] AC2:盘点表覆盖 ≥4 形态类、≥15 个有名工具,每行有核实标记。**(2026-10-05 回标:`research.md` 27 行/6 形态类,gh api 快照逐行 ●/○;首批 4 件建议已列,主人过目=当轮汇报,翻案即改;2026-10-05 收录开工令=主人令按档执行:b 路首批 maigret+urlwatch,design §1/§3 与 inventory §三)**
- [x] AC3:首批收录全绿(2026-10-05 首批 5 件:media/maigret/theharvester/rsshub/spiderfoot;tests/plugins 518 绿、`plugin install+list` 沙箱冒烟可见、doctor 降级 warning=包契约既有钉;官方件 golden 无涉——首批零品类 YAML 变更,OFFICIAL_PLUGINS 品类清单不动;**全量 pytest 门禁:批末跑毕,红项归因见下注**)。注:首批期间并行会话同树在做 secrets 修复与 urlwatch 件,全量若有红先归因并行域再回本档。
- [x] AC4:README「6 official categories」→7(并行会话顺手完成,265b7a9 双语两处)。
- [x] AC5(挂账,另任务):装机包 tauri resources 只捆 4/7 官方品类(games/news/exposure 缺)与 `.seeded` 全有或全无补种语义——本任务不动,已单独记录。**首批追加注记:官方场景件已达 12 件(7 桌面+3 remote+2 server-only),装机包市场面是否随包分发 plugins/<pkg> 是 AC5 任务一并裁。**(2026-10-05 批三回标:三件事落码、commit pending)①**补种语义改毕**——`_seed_first_run` 从「全有或全无」改为**幂等补缺**:bundle 官方品类 YAML 缺哪件补哪件、绝不覆盖已存在文件;`.seeded` 标志语义改为「已做过一次补种」的记录(首次补种时刻定格,不再抑制复种),零缺件启动零写入;tests/desktop 种子用例 2 修 2 增(删件重启补回且标志不刷新/用户自建件零覆盖/games 手改件逐字节原样/缺 news 只补 news+全量在位首启零标志),gitnexus impact=_startup_seed→serve 单链 LOW。②**resources 补齐 7/7 官方品类**:games/news/exposure 三 YAML 并入(官方 7=ai-news/wool/stocks/gpu-prices/games/news/exposure;demo 件维持,README「7 official categories」口径)。③**市场面包裁决按推荐落地**:desktop tier 全件 7 件(proxy/osint/credhunter/media/maigret/theharvester/urlwatch)源码面随包——每件 manifest+README+adapter.py **逐文件**映射进 `plugins/<pkg>/`(精确排除 vendor/、docker/、__pycache__,整目录映射做不到排除故弃);**credhunter/ 自有子包例外随包**(adapter compile+exec 自举依赖其 *.py 与 data/,MYIA 自有零上游复制、可随包,漏捆即交付坏件)。**理由**:装机用户无仓库 checkout,desktop 件(零 docker、进程内/子进程)的安装来源必须在包内,三件套即完整可安装件(`plugin install`=整目录拷贝过 manifest 校验);vendor/ 外来 submodule(GPL Photon/theHarvester)随包分发越许可红线,装机上 vendor 缺失走 adapter **既有结构化 `vendor_missing` 指引**(tests/plugins/test_osint_plugin.py、test_theharvester_plugin.py 已钉,零新码);remote/server-only 件的 docker/ 属服务端部署面不入装机包。守卫=tests/desktop/test_installer_resources.py(27 例:品类 7/7+demo、桌面件 3×7+credhunter 子包、vendor/docker/__pycache__ 排除断言);真包安装冒烟(发布前必跑项)本批未跑,归 CI desktop-release 出包与发布流程;spec python/index.md 种子行为行已同步。**装机安装接线(Resources/plugins/<pkg> 作市场安装来源的发现/一键通道)不在本件范围,后续件另立。****(2026-10-05 批二收口审计注记:本步审计时点 AC5 系「挂账另任务」未勾;上列批三回标与勾选系并行批三会话在途所为且 commit pending——工作树未提交面含 tauri.conf.json/tests/desktop/test_installer_resources.py 等,本步对其未提交代码面未核验、不背书亦不推翻,留批三提交与收口核验;官方场景件时点数=17(批二 +4)。)**
- [x] AC6(D4/D5/D7 门槛机制):gates.yaml fail-closed 装载+manifest `gate` 字段校验+`myssia gates show/set` CLI+桌面设置屏门槛件分区+plugin list 门槛件分组全绿;未启用门槛件 doctor=info(非 warning)且核心无感(铁律测试)。**(2026-10-05 批二回标:主体随 d613310 收编+本批 fa10443/84533ee 落齐;doctor info 非 warning=tests/test_gates.py:850(test_disabled_gate_is_info_not_warning),坏 gates.yaml=warning+全关=:883,普通件零 finding=:896;核心无感=品类 YAML 全可加载+Pipeline 可构造铁律(tests/plugins/test_plugin_packages.py:515)叠加 gates 坏文件三态全关;门禁 `uv run --no-sync python -m pytest tests/plugins tests/engines tests/desktop tests/test_gates.py -q` 本次回填实测 1182 passed/30 skipped;证据 evidence/batch-2-report.md)**
  - **(2026-10-05 批二收口审计复核:met)** gates.py:63/:432+manifest.py:206-258+cli.py:874-953/:3085-3093+settings-screen.tsx:132 亲读;MYIA_HOME=$(mktemp -d) myssia gates show --json=exists:false 全关 exit 0(fail-closed 亲证);tests/test_gates.py:850/883/896 三测亲读在位;G1(tests/plugins+tests/test_gates.py,收口脚本统一跑)退出码 0。**
- [x] AC7(D4 付费 SaaS):Zenrows/ScraperAPI gated 引擎收录——gate_closed 语义测试(总开关关=结构化失败不降级不烧钱)+ 开启后 MockTransport 往返;永不进 AUTO_CHAIN 的注册表断言。**(2026-10-05 批二回标:60e2f52——tests/engines/test_saas_gated_engines.py 16 例(关闭态 gate_closed 零上游请求/开启态 MockTransport 往返/注册表三锁/AUTO_CHAIN 不含),本次回填实测绿(门禁 1182 passed 内);遗留低危(css_extractor 显式 null 判键/robots 守卫盲区)见 evidence/batch-2-report.md)**
  - **(2026-10-05 批二收口审计复核:met)** AUTO_CHAIN(registry.py:79-88)七档不含两件亲核;亲跑 `pytest tests/engines/test_saas_gated_engines.py -q`=16 passed;`ruff check`(gates.py+zenrows/scraperapi/saas)All checks passed;遗留低危 2 条亲证原样未修,记 evidence 待批三或顺手修。**
- [x] AC8(D4 同物种/门槛桩):Crawlab+worldmonitor remote 桩收录(compose/README 门槛说明);EasySpider 形态核验结论记档(可接/不可接+理由);MediaCrawler/yake 许可核验动作完成或如实挂起。**(2026-10-05 批二回标:7df322b(crawlab)/0195806(worldmonitor),`tier: remote`+`gate: platform`,README 指设置面表单+规范键名;EasySpider=Electron GUI 无 API 门槛条件不成立,维持不收终态(research.md 第五波);MediaCrawler=非商业学习许可(警示型批三)/yake=AGPL-3.0 双许可(批三候选)核验毕(步骤 15,research.md 第五波);golden 同步事故与闭环见 evidence/batch-2-report.md)**
  - **(2026-10-05 批二收口审计复核:met)** crawlab/worldmonitor plugin.yaml 亲读(tier: remote+gate: platform,D5 正交);沙箱 MYIA_PLUGIN_DIR=$(mktemp -d) 逐件 install 四件全过、list 门槛件分组与 {platform:未启用} 徽标正确(findings 0/0);EasySpider/MediaCrawler/yake 核验=research.md 第五波;EXPECTED_GATES(test_plugin_packages.py:108-111)+aa89aa5 闭环(git log -S _gate_ref_errors 亲证)。**
- [x] AC9(分析件二批,D8 裁剪):web-check+social-analyzer 桩收录;trafilatura extract 增强评估结案(独立引擎任务或并入,须回答「比手写 extract 规则强在哪」);**gates.analysis 仅 schema+设置面占位,零分析件**(分析 lane 挂点=批三独立质询)。**(2026-10-05 批二回标:66ace59(webcheck,MIT 官方镜像 compose)/cd29e0f(socialanalyzer,AGPL 只桩不携 compose);trafilatura 结案=research.md 第六波(增量=零配置正文抽取补「无规则长尾源」「改版后规则失效」两盲区,与手写规则互补非替代,另立引擎任务);D8 照办——分析件卡设置面禁用占位「批三解锁」,gates.analysis 零分析件)**
  - **(2026-10-05 批二收口审计复核:met)** webcheck/socialanalyzer plugin.yaml 亲读(均 tier: remote 无 gate;socialanalyzer 只桩不携 compose——docker/plugins 亲列 10 目录确无其目录);gates.analysis 仅 schema(gates.py:135)+设置面禁用占位(settings-screen.tsx:774-796 亲读);trafilatura 结案=research.md 第六波。**

## Constraints

- 装不上不拦核心(市场铁律);AGPL 不抄码;GPL 走 submodule;凭据零明文;免费路径门禁(connector-selection spec)。
- 并行会话在场:本任务状态改动直接改 task.json,不用 start/finish 命令(记忆:踩踏在案)。

## Notes

- 2026-10-05 建档。来源:主人「我想的是你把市面上面所有有名的爬虫工具,分析工具塞入这个下面」+「crawl4ai/firecrawl/scrapling/隐身浏览器 为啥走了引擎降级链,如果已经做了,plugins 还有什么作用?建这个 Trellis 任务,先把这个问题讨论清楚了」。
- 现有 7 件官方件明细与形态见 2026-10-05 会话盘点(plugins/ 目录实况)。

## 收口(2026-10-05,批二域:审计+回填步)

- **核验方法**:只读审计(档四件全读+git log/show 逐笔+代码/测试亲读)+域内门禁:G1 `pytest tests/plugins tests/test_gates.py`(收口脚本统一跑,退出码 0)、G2 `myssia plugin list`(退出码 0);审计 scoped 亲跑:`pytest tests/engines/test_saas_gated_engines.py -q`=16 passed、`ruff check`(gates.py+zenrows/scraperapi/saas 四文件)绿、MYIA_HOME 沙箱 `gates show --json` 冒烟 exit 0。G1 绿无红项,无需归因。
- **G2 注记(缺件如实,不略过)**:G2 输出仅 myssia-maigret+myssia-urlwatch 两件——本机 `~/.myia/plugins` 已装清单(皆批一 desktop 件);批二四件未装本机故不在 G2 输出,plugin list 语义=已装清单(cli.py plugin list help「列出已安装插件」)。沙箱复核(MYIA_PLUGIN_DIR=$(mktemp -d) 逐件 install):四件全过,list 输出「共 4 个,可用 4 个;门槛件(2):myssia-crawlab[platform]未启用, myssia-worldmonitor[platform]未启用」+逐件 {platform:未启用} 徽标,findings 0 错误/0 警告——市场可装+门槛分组/徽标实证正确,判定非缺口。
- **批二收录四件(plugin.yaml id,供 plugin list 断言)**:myssia-crawlab、myssia-worldmonitor(gate: platform)、myssia-webcheck、myssia-socialanalyzer(无 gate);官方场景件 13→17,docker/plugins compose 集 10 件(亲列:crawlab/douyin/maxun/monitor/osint/proxy/rsshub/spiderfoot/webcheck/worldmonitor)。
- **task.json 维持 in_progress(本步未转 review)的理由**:批二域 AC6-AC9 审计全 met 已回标;但 AC5 之 [x] 系并行批三会话在途回标且 commit pending(未提交面:tauri.conf.json/tests/desktop/test_installer_resources.py/spec 两件等),批三(D10 分析件,本档 §D10)同刻已动工——本步不核验未提交面,整体转 review 留批三提交+收口一并处置(先例:批一收口 ce9878d 置 review 后因后批回 in_progress)。
- **背景口径漂移(如实记)**:收口指令背景称「批三(分析件挂点质询)明确另议,不属本档收口范围」;档实况=D10 决议+AC5 批三回标已落本档且代码在途——本步按「批二域收口」处理,不吞并批三;批三是否独立立档由主人/提交员裁。
- **遗留(低危,记档待批三或顺手修,详见 evidence/batch-2-report.md §四)**:zenrows.py:77 css_extractor 显式 null 判键不判值;「零上游请求」守卫 robots 盲区;sidecar-protocol.md:282「gates.get 非法参数」半句超前于代码;四新件 install.source 旧仓库名 xinzhuzi/myia.git(全仓 17 件同惯例,重定向兜底)。
- **全量门禁注记**:批二回填会话任务书门禁 1182 passed/30 skipped(evidence 报告);aa89aa5 收编回执全量 4074 过;本收口步未重跑全量(职责域外),域内 G1 绿。
- **真机验收留主人(如有需)**:设置屏「门槛件」分区与 gated 引擎在桌面壳/装机包的实机表现无真机记录(代码侧由 vitest settings+协议测试+MockTransport 测试覆盖)。
