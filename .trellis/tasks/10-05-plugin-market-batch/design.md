# 技术设计:插件市场批量收录(Phase 2 盘点 → Phase 3 分批落地)

> 前提:D1-D3 已批(prd.md 决议表)。铁律:装不上不拦核心;裁决前不开收录工的闸门已过。
> 本设计只定方法与结构,不预填候选结论(盘点表逐行核实是 Phase 2 的活)。

## 1. Phase 2 盘点方法论

**产出物**:`research/inventory.md`(盘点表,照 supplier-map 惯例:○=待核实/●=已核实)。

每行字段:工具名 | 上游 repo | license | 免费路径 | 形态(库/CLI/服务/平台) | 桌面分级可行性(零 docker?) | 建议归位(a-e) | 一句话理由 | 核实标记。

**核实纪律**(避免静态罗列翻车,教训在册「选池档任务前先对归档验前提」):

- license 以上游 LICENSE 文件原文为准(AGPL=只桩不抄;GPL=submodule 样板照 Photon;BSD/MIT 可直借);
- 免费路径按 connector-selection 硬规则四问(免费层是什么/限多少/自托管可否/留痕在哪),SaaS 型直接走 e 路记档;
- 活跃度看最近提交/发布(>1 年停滞记档,不自动出局但标注);
- 每行结论必须给「归位理由」引用判定框字母,不允许无字母入表。

**归位判定框执行细则**(D1 定案):

- **a 路(进引擎链新档)**必须回答两问:比 scrapling/crawl4ai 强在哪(成本/成功率/反检测维度);降级序插哪一档(答不出=不入链,落 b 或记档);
- **b 路(插件+链外引擎)**照 credhunter 先例:`engine: <name>` 注册 `ENGINE_REGISTRY` 不进 `AUTO_CHAIN`,实现=进程内加载 `plugins/<name>/adapter.py`;显式选用、失败=源级 `dependency_missing` 结构化失败;
- **c 路(remote/server-only 桩)**照 maxun/monitor 先例:manifest 分级+compose 文件+README 自部署指引,核心零依赖;
- **d 路(同物种不收)** Crawlab 型——除非接用户既有部署(仍走 c);
- **e 路(不过关不立项)**仅记档一行,不进市场目录。

**D2 硬规则执行点**:盘点表新增「本地可跑?」列——厂商 SaaS/仅云 API 的候选此列必为 ✗,归位自动落 e(或「文档级可选后端」注记,永不进插件 lane 缺省)。

## 2. Phase 3 收录物结构(每件)

- `plugins/<name>/`:plugin.yaml(manifest:分级/版本/许可摘要)+ README.md(上游署名+装法+限制)+ adapter.py(b/c 路)或桩(c 路);
- 服务端件:`docker/` 增 compose 片段(c 路);
- doctor 集成:`dependency_missing` 降级 warning 验证用例;
- `OFFICIAL_PLUGINS` 清单 + `tests/test_plugins.py` 参数化 + golden 快照同步(教训:改官方插件声明面必同步 golden 基件);
- README「6 official categories」口径修正(AC4,与 tests 权威清单 7 个对齐,顺手在首批批内做)。

## 3. 批次划分原则

- 每批 2-4 件、独立可验、独立提交(禁大爆炸,R4);
- 首批选 **零 docker、BSD/MIT、adapter 形态**的最小风险件(打样收录流水线);平台型(c 路)与引擎链候选(a 路,须降级链设计)靠后,各自单独成批;
- a 路候选单独拆任务(涉引擎链与降级序,复杂度高于收录)。

## 4. 风险与回滚

- 收录件全部 additive(plugins/ 目录新增+清单/golden 同步),单件回滚=删目录+还原清单与 golden;
- 引擎链不动(a 路另拆任务),本任务主线零核心改动;
- 并行会话在场:状态走 task.json 直改,不用 start/finish。

## 5. 首批收录设计(2026-10-05 主人批「按照你的建议去做,尽量都弄上」)

> §1-§4 的首批具体化。盘点表=本档 `research.md`(与 §1 所称 inventory.md 同物,文件名从简);§3 首批选件原则(零 docker/MIT·公域/adapter 打样)在本批兑现,§3 尾句「a 路单独拆任务」兑现为 curl_cffi 留独立任务不动。

### 收录清单与形态裁定

| # | 插件 | 上游/license | tier | 形态 | CLI |
|---|---|---|---|---|---|
| 1 | myssia-media | yt-dlp(Unlicense 公域) | desktop | adapter subprocess(`uv run --with yt-dlp yt-dlp --dump-single-json --flat-playlist`) | `myssia media <url> --json` |
| 2 | myssia-maigret | maigret(MIT) | desktop | adapter subprocess(`uv run --with maigret maigret <user> -J simple --folderoutput <tmp>`;v0.6.6 实测) | `myssia maigret <user> --json` |
| 3 | myssia-theharvester | theHarvester(GPL-2,**submodule**) | desktop | vendor submodule + adapter subprocess(照 Photon;pip 包为空壳不可用,2026-10-05 实测) | `myssia harvester <domain> --json` |
| 4 | myssia-rsshub | RSSHub(AGPL,**只桩不抄**) | remote | manifest remote 桩 + compose + README(自部署优先;公共实例=第三方留痕,P0 注记) | — |
| 5 | myssia-spiderfoot | SpiderFoot(MIT) | remote | **改判 b→c**:不在 PyPI(2026-10-05 实测 no solution)+Web 服务优先形态,进程内故事不成立;官方镜像自部署+REST | — |

### 关键裁定(Ruling)

- **R-1 版本策略**:yt-dlp/maigret 走 uv `--with` 不钉版(yt-dlp 抽取器时效即生命、maigret 站点库自更新;uv 缓存隔离零污染根依赖;测试全 mock 可复现);theHarvester 因 GPL 纪律 submodule 钉 commit。
- **R-2 CLI 接线**:只加 media/maigret/harvester 三个子命令(rsshub/spiderfoot 桩无 CLI);命令名直白用上游名;每命令 `_add_*_parser`+失败码→退出码照 osint 先例。
- **R-3 错误契约**:每 adapter 结构化异常(code+message+details.to_dict()),code 词表照 osint(`uv_missing`/`*_failed`/`*_timeout`/`*_output_invalid`);失败绝不拦核心。
- **R-4 引擎面**:首批零新引擎(不动 schema EngineName/registry/AUTO_CHAIN)——链外引擎化进情报流是后续批次按需另立;本批交付=市场包+一键 CLI。
- **R-5 测试**:adapter 单测照 test_osint_plugin(mock subprocess 零网络);包契约并入 test_plugin_packages.py(OFFICIAL_PACKAGES+EXPECTED_TIERS);新测试落 tests/plugins/。
- **R-6 compose**:rsshub/spiderfoot 部署件落 docker/plugins/<id>/compose.yml(插件目录零 compose)。

### 各件数据面

- **media**:items={title,url,channel,uploader,duration,view_count,upload_date,item_count(频道/列表)};url_invalid/media_failed/media_timeout/output_invalid。
- **maigret**(`-J simple`):items={site,username,url,status};top_sites/timeout 可调;无命中=空态成功。
- **harvester**(`-f json`):emails/hosts/ips 按 lane 聚合;vendor_missing 码照 osint。
- **rsshub**:endpoint 占位 example.com;README 教 RSS 路由→品类 `extract.type: rss`(news.yaml 同通路)。

### 改动面

新增 5 个 `plugins/myssia-*/`(plugin.yaml+README[+adapter.py][+vendor]);`src/myssia/cli.py` 加 3 组 parser/handler;`.gitmodules` +1;`tests/plugins/test_plugin_packages.py` 清单+3 个新测试文件;`docker/plugins/myssia-{rsshub,spiderfoot}/compose.yml`;README zh/en 品类数 6→7(AC4,顺批做)。


## 6. 门槛化融合设计(D4 裁决,2026-10-05 晚;深度探查已核实地基)

> 主人令:e 路改门槛立项+设置面配置。本节是落地设计;地基事实(2026-10-05 实读):`vision/settings.py` 是 `<MYIA_HOME>/vision.yaml` 全局配置先例(「MYIA_HOME 第一个全局配置文件」);桌面设置屏现有 4 分区(通用/推送/视觉/系统,`?section=` 深链模式);manifest tier 词表三元组(desktop/remote/server-only)。

### 6.1 gates.yaml(全局门槛配置,照 vision.yaml 先例)

```yaml
# <MYIA_HOME>/gates.yaml —— 门槛件知情启用(fail-closed:本文件缺失/损坏=全关)
version: 1
paid_engines: false            # 付费 SaaS 采集通道总开关(知情:按页计费)
third_party_trace: false       # 第三方留痕通道(公共 RSSHub 实例等)
saas:                          # 付费引擎逐件(key 走钥匙串引用,零明文)
  zenrows:    {enabled: false, api_key: keychain:myia/saas/zenrows-key}
  scraperapi: {enabled: false, api_key: keychain:myia/saas/scraperapi-key}
platforms:                     # 同物种/自有实例接入(门槛=自部署 endpoint)
  crawlab:     {enabled: false, endpoint: https://crawlab.example.com, token: keychain:myia/platforms/crawlab-token}
  worldmonitor:{enabled: false, endpoint: https://worldmonitor.example.com}
analysis:                      # 停更/许可核验后启用的分析件
  snownlp_sentiment: false     # 知情:上游 2020 停更,pin 版自担维护
```

- 装载:新模块 `src/myssia/gates.py`(照 vision/settings.py 的「构造即校验+非法拒构造+LoadError 结构化」);坏文件=**全关+doctor warning**(fail-closed,不是 fail-open);
- **刻意不落品类 YAML**:门槛开关只在这里——AI/模板生成品类配置时不可能无意开启付费通道(主人裁决的「设置里加配置」落地位置)。

### 6.2 manifest `gate` 字段与市场面(D5 定案:独立字段,非 tier 词表)

- manifest 新增可选字段 **`gate: paid | trace | platform | stale`**(缺省不声明=无门槛件);`TIER_TOKENS` 三元组(desktop/remote/server-only)不动——tier 表传输形态、gate 表激活策略,正交组合(crawlab=`tier: remote`+`gate: platform`);
- `plugin list` 对声明 gate 的件独立分组+「未启用/已启用」徽标(状态派生自 gates.yaml);**platform 类门槛组织性不执法**(D6:不拦用户 direct_api 源,开关=知情确认+状态面);
- 未启用门槛件 = doctor **info** finding(不是 warning:用户没开是正常态,不是故障);启用后 doctor 转 ok;
- 带 gate 的插件包 README 必须含门槛类型+知情文案(成本/留痕/停更三态文案模板);
- `third_party_trace` 开关当前无执法点(D9):公共实例(rsshub.app 等)检测提示记 backlog,留痕保护现阶段=README 知情文案。

### 6.3 付费 SaaS 引擎化(Zenrows/ScraperAPI,R6)

- `EngineName` 词表新增 `zenrows`/`scraperapi`,注册 `ENGINE_REGISTRY` **永不进 AUTO_CHAIN**(链外引擎,credhunter 先例);
- fetch 前置检查:总开关或件开关未开 → 结构化失败 `gate_closed`(新失败类,与 `dependency_missing`/`mcp_server_missing` 并列;doctor 文案区分「关着」与「缺依赖」);
- 开启后:engine_options 收 `api_key: keychain:myia/saas/<name>-key` 引用(凭据解析走既有 secret 通道);测试全 MockTransport(零真实扣费)。
- **API 形态已核 ●(research 第五波)**:Zenrows `GET api.zenrows.com/v1/?apikey=&url=&js_render=true`(可选 premium_proxy/css_extractor);ScraperAPI `GET api.scraperapi.com/?api_key=&url=`(可选 country/render);同薄形态 → 共用一个 SaaS fetch 骨架模块,两引擎各映射参数面。

### 6.4 桌面设置屏「门槛件」分区

- `SECTIONS` 增第 5 分区 `{id: "gates", label: "门槛件"}`(照现有 4 分区与 `?section=` 深链模式);
- 区内三卡:付费通道(总开关+逐件开关+钥匙串键录入)/自有实例(endpoint+token 表单)/分析件(**D8:仅占位**——显示「批三解锁」禁用态,不发分析件);保存走 sidecar 新方法 `gates.get`/`gates.save`(照 yaml.save 先例;**协议权威=entry.py `_HANDLERS` 注册表,main.rs 通用路由无方法级白名单,rust 侧零改动**——2026-10-05 深夜实读 main.rs 核实,修正早稿「白名单同步」错述);
- 文案铁律:每开关旁挂知情警示(「按页计费,你的采集目标清单将经对方服务器」等)。

### 6.5 e 路逐件门槛表(盘点表回写索引)

| 原判 | 工具 | 门槛类型 | 落地形态 |
|---|---|---|---|
| e(SaaS) | Zenrows/ScraperAPI/Crawlbase | 付费知情 | gated 引擎+gates.yaml(§6.3) |
| e(被覆盖) | Selenium/undetected-chromedriver/you-get/urlwatch | —(维持不收) | 无门槛可设,纯冗余;裁决适用范围不含此类 |
| e(同物种) | Crawlab/worldmonitor | 自有实例 | remote 桩+gates.platforms(§6.1) |
| e(同物种) | EasySpider | 形态核验 | 本地 GUI 无 API:门槛条件不成立→维持不收+理由记档(R7) |
| e(许可) | MediaCrawler/yake/weibo-search/SpiderKeeper | 许可核验 | 法律门槛,核验前不进仓;核验动作入 implement 清单 |
| e(停更) | snownlp/recon-ng/ScrapydWeb | 停更知情 | gates.analysis 开关+pin 版 |
| e(免费路径) | — | — | 免费路径门禁是 connector-selection spec 硬规则,D4 不改写 |

### 6.6 与既有判例的一致性

- D2「永不缺省」存活且加强:门槛件=显式知情后的选择,缺省关闭进 gates.yaml fail-closed;
- 铁律不变:门槛件任何失败(含 gate_closed)不拦核心品类;
- connector-selection spec 的免费路径门禁不放宽——付费 SaaS 收录的是「用户自带钥匙的通道」,不进官方文档推荐路径(zero-cost.md 不列)。

### 6.7 接口契约与测试矩阵(2026-10-05 深夜深化)

**gates.py 公开面**(照 vision/settings.py 形状):

```
GATES_FILE_NAME = "gates.yaml"
class GatesConfig:        # 构造即校验,未知字段拒(LoadError 结构化明细)
    paid_engines: bool    # 缺省 False;任何缺失/坏文件路径→全 False(fail-closed)
    third_party_trace: bool
    saas: dict[str, SaaSGate]        # {enabled: bool, api_key: keychain 引用|None}
    platforms: dict[str, PlatformGate]  # {enabled, endpoint(https 占位校验), token(钥匙串引用|None)}
    analysis: dict[str, bool]
def load_gates_config(path) -> GatesConfig   # 坏文件→LoadError;调用侧(CLI/sidecar)捕获后以全关态继续+doctor warning
def gate_open(config, kind, name) -> bool    # 引擎/插件侧唯一查询口
```

**sidecar 协议**:`gates.get {params:{}} → {config: {...}, path}`;`gates.save {params:{config}} → {ok:true, path}`(tmp+rename 原子写;校验失败→结构化 error 不落盘)。

**CLI 面**(D7,照 secret 命令族):`myssia gates show --json`(整份配置+路径)/ `myssia gates set <kind>.<name> <on|off>`(kind∈{paid_engines,third_party_trace,saas,platforms,analysis};saas/platforms 逐件 on 需要 keychain 键在位,缺键=结构化拒);`myssia gates` 退出码族与全家桶对齐(0/1)。

**测试矩阵**(批二新增件一览):

| 层 | 文件 | 钉什么 |
|---|---|---|
| gates 装载 | tests/test_gates.py | 缺失/坏文件=全关;未知字段拒;每开关往返;keychain 引用形态校验 |
| manifest | tests/plugins/test_plugin_packages.py | gated 档清单/分级/README 门槛文案必含 |
| 市场/doctor | tests/plugins+tests/cli | plugin list 分组与 enabled 派生;未启用=info 非 warning |
| 引擎 | tests/engines/test_saas_gated_engines.py | 关闭态 gate_closed;开启态 MockTransport 往返;AUTO_CHAIN 不含断言 |
| 桩件 | tests/plugins/test_plugin_packages.py | crawlab/worldmonitor `tier: remote`+`gate: platform`(D5 正交组合);compose 集 10 件(7+crawlab/worldmonitor/webcheck,social-analyzer 只桩不携;批二回填修正:本行原 D5 前早稿「tier=gated;9 件」与 prd.md D5 定案及实际交付均不符,复审 low 抓出) |
| 设置屏 | desktop ui settings 测试+tests/desktop | gates.get/save 协议往返;分区渲染;知情文案在位 |
| 铁律 | 各新件 | gate_closed/桩不可达/坏 gates.yaml 三态下核心品类与 Pipeline 构造无感 |
