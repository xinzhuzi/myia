# 批二交付报告:D4 门槛机制+门槛件+分析件(2026-10-05)

> 回填会话:文档收口者(2026-10-05,HEAD=123f597)。本文档只陈述事实与可溯源证据;执行回执引自批二各分路/落账会话的原始汇报,标注「引自回执」;本次回填会话亲跑的检查标注「本次实测」。

## 一、并行拓扑说明

批二在同一条 main 工作树上多会话并行,全程无独家锁,靠「快照外科+单件单提交+跨路只读」纪律防混线:

1. **执行期(四路并行)**:10 门槛机制地基路 / 11 设置屏门槛件分区路 / 12 付费 SaaS 引擎路 / 13+14 桩件路(gates=地基,engines/桩件可即时自验因地基主体已先在树)。
2. **前置事实**:地基主体(gates.py/manifest.py/cli.py/skill/SKILL.md)在批二执行会话开工前,已由更早的并行协调收编提交 **d613310** 入库(引自地基路回执:工作树对账确认);四路在剩余缺口上作业。
3. **落账期**:落账会话按逻辑单元七笔单件单提交(fa10443→60e2f52→84533ee→7df322b→0195806→66ace59→cd29e0f,git reflog 实证按此序);提交前后各跑一次任务书门禁命令,两次均 1144 passed/30 skipped(引自落账回执)。
4. **批末复审**:换眼复审报 14 条发现(2 high/5 medium/7 low),其中两条 high 同根(tests/plugins/test_plugin_packages.py golden 未随批提交,HEAD 态红)。
5. **收编闭环**:复审修复在工作树在途期间,同树另有 desktop-managed-py-env 批与 push 批活跃;**aa89aa5**(「收编并行批三波在途件」)把复审修复(golden 同步/gates 构造期引用校验/gate 声明钉子/两份 README 指引/SKILL.md 枚举同步)与 engines/desktop 在途件一并收编入库,附「全量 4074 过+vitest 433 绿+tsc 0」回执(引自提交信息)。
6. **批后**:push 批收口链(b965753/adf3da5/123f597)至本回填会话取证的 HEAD **123f597**;七笔批二提交均为 HEAD 祖先且已在 origin/main(`git branch -a --contains fa10443` 实证)。

## 二、每步落地与提交哈希(implement.md 步骤 10-14)

| 步 | 交付 | 提交 | 增补事实 |
|---|---|---|---|
| 10 门槛机制地基(R5) | gates.py fail-closed 装载(GatesConfig 构造即校验/未知字段拒/keychain 引用形态校验/load_gates_fail_closed);manifest `gate` 独立字段(D5,TIER_TOKENS 不动);cli.py gates show/set 命令族+plugin list 门槛件分组 enabled 徽标+doctor gate_disabled=info;sidecar gates.get(坏文件 fail-closed=全关+error 带回)/gates.save(同门校验失败零写入,tmp+rename);tests/test_gates.py | **d613310**(主体,前置收编)+ **fa10443**(本批补 entry.py 两方法+测试) | 地基路回执:执行卡裁给本路的唯一缺口=entry.py 两方法;SKILL.md 清单同步一行在地基主体内 |
| 11 设置屏门槛件分区(R5 尾) | settings-screen.tsx 第 5 分区三卡(付费通道/自有实例/分析件 D8 禁用占位)+知情警示+拒载 fail-closed 警示卡+保存覆写修复;types.ts/client.ts GatesView 族+gatesGet/gatesSave;sidecar-protocol.md 方法表 61/62 行;settings.test.tsx +5 例、sidecar 协议测试 +5 例 | **84533ee**(rust 零改动——main.rs 实无方法级白名单) | 协议版本**定案不随批 bump**(维持 v10,两方法在 v10 内交付,测试 docstring 记因 tests/desktop/test_desktop_sidecar_protocol.py:2308);执行中报过的「版本钉 11 vs 实际 10」契约红随定案消解(本次实测 tests/desktop 全绿);gates.get 应答实为 {config,path,exists,error} 超集(设计 §6.7 早稿 {config,path} 的偏差已按「代码为准」记入 spec——引自设置屏路回执) |
| 12 付费 SaaS gated 引擎(R6) | schema.py EngineName +zenrows/scraperapi;engines/saas.py 共用骨架(fetch 前置查 gates→关闭态 FetchError class=gate_closed 零上游请求;开启态 keychain 解引用;apikey mask 不落日志);zenrows.py/scraperapi.py;registry.py 链外注册(credhunter 先例位);tests/engines/test_saas_gated_engines.py 16 例(关闭态/开启态往返/注册表三锁/AUTO_CHAIN 不含) | **60e2f52** | 执行中报过的 SKILL.md 枚举表连锁红已闭:SKILL.md:57 ENGINES 行现含 scraperapi/zenrows,test_skill_doc 24 passed(本次实测) |
| 13 同物种门槛桩(R7) | myssia-crawlab(tier:remote+gate:platform,BSD-3 官方镜像 compose,127.0.0.1:8080 回环)+myssia-worldmonitor(AGPL 只桩,compose 四服务构建上下文钉上游 tag v2.10.0,必设密钥 ${VAR} 注入,127.0.0.1:3001 回环避开 web-check 的 3000);README 门槛说明(自有实例例外通道,组织性不执法) | **7df322b**(crawlab)/ **0195806**(worldmonitor) | EasySpider 终态不收(Electron GUI 无 API,门槛条件不成立;research.md 第五波);compose 集**实为 10 件**——卡面「7→9」系步骤 13 单步语言,文件清单同时给 webcheck 配 compose、socialanalyzer 只桩,自洽总数=10(桩件路如实报偏离);docker/plugins 目录本次实测恰 10 个 |
| 14 分析件二批(AC9,D8 裁剪) | myssia-webcheck(MIT 官方镜像单服务零凭据 compose)+myssia-socialanalyzer(AGPL 只桩不携 compose);research.md 第六波 trafilatura 结案 | **66ace59**(webcheck)/ **cd29e0f**(socialanalyzer+第六波) | trafilatura 结论:零配置正文抽取补手写规则两盲区(无规则长尾源/改版后规则失效兜底),互补非替代,另立引擎任务;gates.analysis 仅 schema+设置面禁用占位「批三解锁」,零分析件(D8 照办);D9 公共实例检测照记 backlog |
| 15 许可核验批 | —(先行完成) | 步骤 15 已 [x] | MediaCrawler=非商业学习许可(警示型批三)/yake=AGPL-3.0 双许可(批三候选)/weibo-search+SpiderKeeper=无 LICENSE 维持不收终态(research.md 第五波) |
| golden 同步(OFFICIAL_PACKAGES/EXPECTED_TIERS/EXPECTED_GATES/compose 集/README 门槛文案断言) | tests/plugins/test_plugin_packages.py 批二钉子 | **aa89aa5**(收编,非七笔之内) | 落账会话因该文件同时出现在任务书文件清单与「外来脏树禁入」清单、两规冲突取强令未提交(引自落账回执),造成 HEAD 态红(复审 high)——详见下节 |

## 三、验证命令与结果

**本次回填会话亲跑(2026-10-05,工作树=HEAD 123f597,批二相关文件零未提交改动)**:

| 命令 | 结果 |
|---|---|
| `uv run --no-sync python -m pytest tests/plugins tests/engines tests/desktop tests/test_gates.py -q` | **1182 passed, 30 skipped**(34s)——任务书门禁命令(落账会话当时=1144 passed/30 skipped;差额系 aa89aa5 收编后新增测试,引自各自回执) |
| `uv run --no-sync python -m pytest tests/test_skill_doc.py -q` | **24 passed**(SKILL.md 枚举表含 zenrows/scraperapi,SKILL.md:57) |
| SidecarProtocol 方法键清点(python 逐行解析 desktop/ui-src/src/lib/api/types.ts:1283-1336,排除注释行,含带引号键) | **47 个方法键**(含 gates.get/gates.save);另与逐行手数(35+9+1+2=47)互证一致 |
| entry.py `_HANDLERS` 清点(python 正则) | **62 方法** |
| `ls docker/plugins/` | **10 个 compose 目录**(crawlab/douyin/maxun/monitor/osint/proxy/rsshub/spiderfoot/webcheck/worldmonitor),与 golden 断言集一致 |

**引自分路/落账/收编回执(非本次亲跑,如实注记)**:

- 地基路:`pytest tests/test_gates.py tests/plugins -q`=594 passed/22 skipped;+tests/desktop=729 passed/22 skipped;`MYIA_HOME=$(mktemp -d) myssia gates show --json` 冒烟 exit 0。
- 引擎路:`pytest tests/engines/test_saas_gated_engines.py -q`=16 passed;邻接面 468 passed/8 skipped;ruff 六文件净。
- 设置屏路:`npx tsc --noEmit` exit 0;vitest settings.test.tsx 38/38。
- 桩件路:四 manifest 过 load_manifest_file、三 compose yaml.safe_load+凭据形键全 ${VAR}、私网 IP/Bearer 裸字面量扫描零命中(冒烟脚本)。
- 落账会话:门禁命令提交前后各一次=1144 passed/30 skipped。
- 复审:detached worktree(f64c0ef)跑 tests/plugin_packages=**1 failed/153 passed**(golden 未提交态,即两条 high 的实证);工作区改动态=198 passed。
- aa89aa5 收编回执:全量 4074 过+vitest 433 绿+tsc 0。

## 四、受阻与遗留

**受阻:无。**批二十五路(10/11/12/13+14)全部落地,无 blocked 项;批二全量门禁绿(ask 陈述+aa89aa5 回执+本次实测门禁命令绿)。

**遗留(低危,未处置,记档待批三或顺手修)**:

1. **zenrows css_extractor 显式 null 判键不判值**(src/myssia/engines/zenrows.py:77 `_upstream_returns_json` 按「键在」判;`_query_params` 按值非 None 发参)——`css_extractor: ~` 时不发参却按 JSON 解析,上游回 HTML 得误导性 json_decode 且白发一次付费请求。本次实测代码原样未修。
2. **「零上游请求」守卫 robots 盲区**(tests/engines/test_saas_gated_engines.py:117-118)——failing_handler 经 make_handler 自动应答 /robots.txt,断言强度弱于「任何请求」字面;实现侧门槛检查先于 robots,无现役洞。未修。
3. **sidecar-protocol.md:282 半句超前于代码**——「gates.get 带非法参数=invalid_params」,而 entry.py `_m_gates_get`(3094-3114)忽略 params 不校验。文档与代码不一致,未修(择一:删半句或补形状校验)。
4. **四新 manifest install.source 沿用 `https://github.com/xinzhuzi/myia.git` 旧仓库名**(如 plugins/myssia-crawlab/plugin.yaml:29)——沿袭全仓既有 17 件惯例非本批引入,fresh install 靠 GitHub 改名重定向;建议批末全仓统一切 shishi 或注记重定向策略。
5. **备忘**:cli.py 复审范围内含 push 域 hunk(channels refresh 帮助文案,d556bb7),与门槛域同文件混载属多任务同树预期;按域拆提交/回滚时该 hunk 归 push 域。

**结构性教训(记档,供后续同形批次)**:golden 基件(tests/plugins/test_plugin_packages.py)同时出现在任务书某笔的文件清单与「外来脏树禁入」清单时,两规冲突取禁入令的代价=提交态 HEAD 红(本批复审 high 实证)。后续同形冲突应即时上报裁决,或 golden 增量随所属件同笔提交;本批由 aa89aa5 收编闭环。

## 五、复审发现与处置(14 条;2 high/5 medium/7 low)

处置状态以本次回填会话在 HEAD 123f597 的逐项实测为准:

| # | 位置 | 严重度 | 发现 | 处置(实测依据) |
|---|---|---|---|---|
| 1 | tests/plugins/test_plugin_packages.py:191 | high | 批二四件已提交但 OFFICIAL_PACKAGES/EXPECTED_TIERS/compose 钉子只在未提交工作区,HEAD(f64c0ef)实测 1 failed/153 passed | **已解(aa89aa5 收编)**:`git log cd29e0f..HEAD -- tests/plugins/test_plugin_packages.py` 仅 aa89aa5 一笔;当前 HEAD 含四件清单+EXPECTED_TIERS+compose 10 件集;本次实测门禁 1182 passed |
| 2 | 同上(第二视角:各提交 git show grep 四包名=0,单件单提交纪律未覆盖 golden) | high | 同根 | **已解(同上)**;教训记档见上节 |
| 3 | src/myssia/gates.py:130 | medium | docstring 称凭据引用形态「构造期同门校验」但 __post_init__ 不校验,save 可写出 load 拒收的文件 | **已解(aa89aa5)**:本次实测 __post_init__ 对 saas.*.api_key_ref 与 platforms.*.token_ref 走 `_gate_ref_errors` 构造期同门(代码注释「复审补」;`git log -S _gate_ref_errors` 锁定 aa89aa5);回归测试 test_direct_construction_plaintext_api_key_rejected(tests/test_gates.py:334)/test_direct_construction_env_ref_rejected_both_kinds(:341)/test_replace_gate_with_plaintext_ref_rejected(:373)在位 |
| 4 | src/myssia/gates.py:140 | medium | 同根 3(直接构造不校验 api_key_ref 形态) | **已解(同 3)** |
| 5 | tests/plugins/test_plugin_packages.py:82 | medium | gate 声明面无钉:删 plugin.yaml 的 gate 行测试仍绿 | **已解(aa89aa5)**:本次实测 EXPECTED_GATES(crawlab/worldmonitor=platform)+ test_gate_declaration_matches_expected_table(:169)+ test_gated_readme_documents_gate_type_and_informed_consent(:243)俱在 |
| 6 | plugins/myssia-crawlab/README.md:19 | medium | 凭据键名两路互斥(README 教 myia/crawlab/api-token vs 设置面 myia/platforms/crawlab-token) | **已解(aa89aa5)**:本次实测 README 步骤 2 已改指「设置→门槛件→自有实例 表单」+规范名 `myia/platforms/crawlab-token`(README:19-23) |
| 7 | plugins/myssia-worldmonitor/README.md:19 | medium | endpoint 指引错位(指向 manifest 占位字段而非设置面表单/gates.yaml) | **已解(aa89aa5)**:本次实测步骤 2 已改写为「实例地址填进桌面 设置→门槛件→自有实例 表单——落点…gates.yaml platforms.worldmonitor.endpoint」(README:20-23) |
| 8 | src/myssia/engines/zenrows.py:77 | low | css_extractor 显式 null 判键不判值(见遗留 1) | **遗留未修**(本次实测代码原样) |
| 9 | tests/engines/test_saas_gated_engines.py:119 | low | robots 守卫盲区(见遗留 2) | **遗留未修** |
| 10 | .trellis/spec/desktop/sidecar-protocol.md:282 | low | 「gates.get 带非法参数=invalid_params」与代码不符 | **遗留未修**(见遗留 3) |
| 11 | .trellis/spec/desktop/sidecar-protocol.md:305 + client.ts:4 | low | 「SidecarProtocol 现盖 47 方法」注记虚报,建议改 44 | **不采纳(复审清点疑误)**:本次两种独立清点(types.ts:1283-1336 interface 体逐行解析=47;手数 35+9+1+2=47)一致得 **47**(含 gates.get/save 两键);47 注记与代码实况相符。复审「实有 44」疑漏数带引号键(如 "plugins.list"/"run.start" 等)。后续对账以代码键数为准——此点采纳 |
| 12 | .trellis/tasks/10-05-plugin-market-batch/design.md:175 | low | §6.7 桩件行 D5 前早稿口径(tier=gated;compose 集 9 件) | **本次文档收口修正**:该行改「tier: remote+gate: platform(D5 正交组合);compose 集 10 件(含 webcheck;social-analyzer 只桩不携)」并留修正注记 |
| 13 | plugins/myssia-crawlab/plugin.yaml:28 | low | install.source 沿用旧仓库名(见遗留 4) | **遗留备忘**(全仓性,非本批引入) |
| 14 | src/myssia/cli.py:1011 | low | 复审范围内混入 push 域 hunk(d556bb7) | **备忘,无需修复动作**(见遗留 5) |

**收尾说明**:本报告与 implement.md 步骤 10-14 勾选、prd.md AC6-AC9 回标、design.md §6.7 桩件行修正同笔提交;task.json 状态未动(仍 in_progress,批三未启)。工作树残留脏件(desktop/pyenv 相关 9 件+Cargo 两件)系 desktop-managed-py-env 并行批在途,不属本批二,未触碰。
