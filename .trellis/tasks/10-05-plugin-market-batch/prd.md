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
- [ ] AC5(挂账,另任务):装机包 tauri resources 只捆 4/7 官方品类(games/news/exposure 缺)与 `.seeded` 全有或全无补种语义——本任务不动,已单独记录。**首批追加注记:官方场景件已达 12 件(7 桌面+3 remote+2 server-only),装机包市场面是否随包分发 plugins/<pkg> 是 AC5 任务一并裁。**
- [x] AC6(D4/D5/D7 门槛机制):gates.yaml fail-closed 装载+manifest `gate` 字段校验+`myssia gates show/set` CLI+桌面设置屏门槛件分区+plugin list 门槛件分组全绿;未启用门槛件 doctor=info(非 warning)且核心无感(铁律测试)。**(2026-10-05 批二回标:主体随 d613310 收编+本批 fa10443/84533ee 落齐;doctor info 非 warning=tests/test_gates.py:850(test_disabled_gate_is_info_not_warning),坏 gates.yaml=warning+全关=:883,普通件零 finding=:896;核心无感=品类 YAML 全可加载+Pipeline 可构造铁律(tests/plugins/test_plugin_packages.py:515)叠加 gates 坏文件三态全关;门禁 `uv run --no-sync python -m pytest tests/plugins tests/engines tests/desktop tests/test_gates.py -q` 本次回填实测 1182 passed/30 skipped;证据 evidence/batch-2-report.md)**
- [x] AC7(D4 付费 SaaS):Zenrows/ScraperAPI gated 引擎收录——gate_closed 语义测试(总开关关=结构化失败不降级不烧钱)+ 开启后 MockTransport 往返;永不进 AUTO_CHAIN 的注册表断言。**(2026-10-05 批二回标:60e2f52——tests/engines/test_saas_gated_engines.py 16 例(关闭态 gate_closed 零上游请求/开启态 MockTransport 往返/注册表三锁/AUTO_CHAIN 不含),本次回填实测绿(门禁 1182 passed 内);遗留低危(css_extractor 显式 null 判键/robots 守卫盲区)见 evidence/batch-2-report.md)**
- [x] AC8(D4 同物种/门槛桩):Crawlab+worldmonitor remote 桩收录(compose/README 门槛说明);EasySpider 形态核验结论记档(可接/不可接+理由);MediaCrawler/yake 许可核验动作完成或如实挂起。**(2026-10-05 批二回标:7df322b(crawlab)/0195806(worldmonitor),`tier: remote`+`gate: platform`,README 指设置面表单+规范键名;EasySpider=Electron GUI 无 API 门槛条件不成立,维持不收终态(research.md 第五波);MediaCrawler=非商业学习许可(警示型批三)/yake=AGPL-3.0 双许可(批三候选)核验毕(步骤 15,research.md 第五波);golden 同步事故与闭环见 evidence/batch-2-report.md)**
- [x] AC9(分析件二批,D8 裁剪):web-check+social-analyzer 桩收录;trafilatura extract 增强评估结案(独立引擎任务或并入,须回答「比手写 extract 规则强在哪」);**gates.analysis 仅 schema+设置面占位,零分析件**(分析 lane 挂点=批三独立质询)。**(2026-10-05 批二回标:66ace59(webcheck,MIT 官方镜像 compose)/cd29e0f(socialanalyzer,AGPL 只桩不携 compose);trafilatura 结案=research.md 第六波(增量=零配置正文抽取补「无规则长尾源」「改版后规则失效」两盲区,与手写规则互补非替代,另立引擎任务);D8 照办——分析件卡设置面禁用占位「批三解锁」,gates.analysis 零分析件)**

## Constraints

- 装不上不拦核心(市场铁律);AGPL 不抄码;GPL 走 submodule;凭据零明文;免费路径门禁(connector-selection spec)。
- 并行会话在场:本任务状态改动直接改 task.json,不用 start/finish 命令(记忆:踩踏在案)。

## Notes

- 2026-10-05 建档。来源:主人「我想的是你把市面上面所有有名的爬虫工具,分析工具塞入这个下面」+「crawl4ai/firecrawl/scrapling/隐身浏览器 为啥走了引擎降级链,如果已经做了,plugins 还有什么作用?建这个 Trellis 任务,先把这个问题讨论清楚了」。
- 现有 7 件官方件明细与形态见 2026-10-05 会话盘点(plugins/ 目录实况)。
