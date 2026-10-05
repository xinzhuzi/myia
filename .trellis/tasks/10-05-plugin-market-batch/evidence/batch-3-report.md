# 批三交付报告:分析 lane(D10)+AC5 装机包+4low/D9 小修(2026-10-05)

> 回填会话:文档收口者(2026-10-05 午,HEAD=0349930)。本文档只陈述事实与可溯源证据;执行回执引自批三各分路/落账/复审会话的原始汇报,标注「引自回执」;收口指令计数(归档清单/全量门禁/复审 10 项 4 修)标注「引自收口指令」;本次回填会话亲跑/亲读的检查标注「本次实测」。

## 一、批三时序与并行拓扑

批三在同一条 main 工作树上多会话并行(table-restore 线、pyenv 线、journal 归档轮同刻在场),全程靠「快照外科+单件单提交+外来脏树零触碰」纪律防混线:

1. **质询定案**(D8 悬案闭):批三前置质询出 D10 决议(挂点/执法关系/三件形态),prd.md 决议节+design.md §7 设计节落档=**854f3c7**(docs)。
2. **三路落地**(执行会话,工作树在途):批三收录(analysis lane+三件)/AC5 装机包/4low+D9 小修,零 commit 留树;两引擎任务建档另立两新档(task.py create --no-start)。
3. **落账**:五笔按序入 main=854f3c7→c43144b→60fff33→ead33f7→4b66cad;每笔 `git diff --cached --name-only` 核对暂存集零外来;cli.py 单文件混两笔按 hunk 拆(lane 9 hunks→c43144b、D9 3 hunks→ead33f7,拆后 `git diff cli.py`=0 行确认全量归位)(引自回执)。gitnexus detect-changes(`-r shishi --scope staged`)三笔代码提交=c43144b 17 文件/34 符号/0 流程/low、60fff33 5 文件/8 符号/5 流程/medium(serve 启动路径,AC5 语义换代本义)、ead33f7 6 文件/19 符号/0 流程/low,无 HIGH/CRITICAL;两笔 docs 依 AGENTS.md 豁免(引自回执)。
4. **复审**:10 项 4 修(引自收口指令);修复载体=**119f57f**(ac5 域 medium)+**0349930**(批三域两缺陷),详见 §六。
5. **归档轮**:9 档任务归档+全量门禁绿(引自收口指令),详见 §五。
6. **收口回填(本步)**:implement.md 勾选注记+批三新节(步骤 17-22)、prd.md AC5/AC9 回标、research.md TikTokDownloader 核毕(已在案)、本报告。

## 二、每路落地与提交哈希

| 路 | 交付 | 提交 | 增补事实(引自回执;代码锚点=本次实测亲读) |
|---|---|---|---|
| 批三质询定案(D10) | prd「批三 grill 决议 D10」节(+12 行)+design §7 lane 设计(+39 行),均标注主人令按建议执行、翻案即改 | **854f3c7** | 挂点=enrich 平行(`_stage_analyze` 阶段内 dedup 后/push 前),非 classify 后处理(三处违规:重复开销/过滤语义混淆/partial 翻转);爆炸半径 gitnexus impact `_stage_analyze`=0 直接调用方/LOW;执法关系=D6 措辞闭合(lane 关=正常态非 gate_closed 失败);yake 活跃实况修正(2026-02-11 推送,stale 徽标失实→不声明 gate) |
| 批三收录(分析件) | `src/myssia/analysis_lane.py`(成员注册表 {snownlp,yake})+`Pipeline._analysis_lane_pass`+`store.merge_item_metadata` 回填+三件+snownlp(tier:desktop+gate:stale,子进程钉版 snownlp==0.12.3 单 spawn stdin JSON 批,真跑冒烟正面 0.9635/负面 0.0006)/yake(不声明 gate,进程内惰性 import,未装=dependency_missing 降级,真跑 yake 0.7.3)/mediacrawler(警示文档桩:plugin.yaml+README 零 adapter)+cli 市场面 lane 徽标+测试 43 新例 | **c43144b** | 本次实测锚点:pipeline.py:1895/:1934 两分支都过 `_analysis_lane_pass`(def :1946,design §7.1「与 enrich.enabled 正交」形状落实);store/base.py:110 merge_item_metadata;cli.py:145 ANALYSIS_LANE_MEMBERS、:3313/:3381-3411 gates.analysis_lane 分组+doctor analysis_lane_disabled=info;plugins/myssia-snownlp|yake(含 adapter.py)/myssia-mediacrawler(仅 plugin.yaml+README)三目录在位;门禁 842 passed/31 skipped+全树 4199 passed;TikTokDownloader gh api 核毕=终态不收(research.md 盘点表行+未核项节随笔入库);复审修复 0349930 见 §六 |
| AC5 装机包 | ①`_seed_first_run` 幂等补缺(缺哪补哪绝不覆盖、`.seeded`=补种记录、零缺件零写入,种子用例 2 修 2 增)②tauri resources 品类 7/7(games/news/exposure)+desktop tier 件逐文件映射(排除 vendor/docker/__pycache__;credhunter/ 自有子包整目录例外)③市场面包裁决入 prd(vendor/ GPL 不随包、vendor_missing 零新码)+守卫 tests/desktop/test_installer_resources.py+spec python/index.md 同步 | **60fff33** | 三处裁量记档 prd AC5(credhunter 子包超字面三件套/逐文件映射排除需要/真包安装冒烟归 CI);tests/desktop=206 passed 含守卫 27 例;复审修复 119f57f 见 §六;本次实测:tauri.conf.json snownlp/yake/mediacrawler 映射行 :70-77 在位 |
| 4low+D9 小修 | zenrows.py:77 判键改判值(css_extractor:~ HTML 直通+null 测试)/robots 守卫盲区 2 例/sidecar-protocol.md:282 半句按代码实况修正(entry.py:3094 忽略 params)/D9=cli doctor KNOWN_PUBLIC_INSTANCE_HOSTS(rsshub.app)+platforms endpoint 命中 third_party_trace info(4 例);crawlab install.source=gh api 双向核验远端实名 myia 无错→不采纳修,YAML 注记重定向(全仓 20 件统一切 shishi 留批末专项) | **ead33f7** | 修 4 如实记档不采纳(重定向回 full_name=xinzhuzi/myia 与 git remote 一致);gitnexus 索引先 analyze --index-only 刷新(30.2s);门禁 tests/engines tests/test_gates.py=429 passed/8 skipped+邻接 773 passed/22 skipped |
| 两引擎任务建档 | 10-05-engine-curl-cffi(L2.5 档,定案问题=AUTO_CHAIN vs 链外显式选用)+10-05-extract-trafilatura(补手写规则两盲区,定案问题=共存边界+挂点档位),均 planning、implement.jsonl 各 curated 2 条 | **4b66cad** | 有意不用 --parent(防改母档 children 列表);check.jsonl 空=planning 设计态,validate 1 error 属预期;零现存档改动,git 足迹=仅两新 untracked 目录(引自回执;本次实测:两目录仍在 .trellis/tasks/ 活区) |

## 三、质询决议 D10 要点(详见 prd 决议表+design §7)

- **D10-1 挂点**:enrich 平行,`_stage_analyze` 阶段内(dedup 之后、push 之前),与 LLM 精评同位互补;不是 classify 后处理——classify 后处理在三处违规(重复开销烧在将被去重丢弃的条目上/装饰挂过滤器阶段诱使分析结果参与丢弃决策→击穿铁律/失败误翻 partial)。
- **D10-2 执法**:gates.analysis 是真执法(dispatch 级)非组织性——每轮 `load_gates_fail_closed`(照 vision ring 每轮装载先例)+逐件 `gate_open` 在任何 adapter 加载之前;gate 关=不 import/不 spawn/条目零触碰的字面零开销;坏 gates.yaml=全关=lane 不跑;lane 关=正常未启用态(doctor info+debug),刻意不是 SaaS 的 gate_closed 结构化失败(语义=被品类请求后被拒,lane 无此调用方);逐件键名以 `plugin_gate_key` 派生(§6.1 样例键系实现前早稿)。
- **D10-3 三件形态**:snownlp 钉版子进程件 gate:stale / yake 进程内惰性 import 无 gate(活跃实况修正)/ mediacrawler 警示文档桩(零 adapter/零 lane 接线)。

## 四、验证命令与结果

**本次回填会话亲跑(2026-10-05,工作树=HEAD 0349930+外来在途脏树)**:

| 命令 | 结果 |
|---|---|
| `uv run --no-sync python -m pytest tests/plugins tests/pipeline tests/desktop tests/engines tests/test_gates.py -q` | **1 failed, 1408 passed, 39 skipped**(53.04s)——失败=tests/desktop/test_pyenv_resources.py::test_components_registry_shape(:151 AssertionError),该文件系并行 pyenv 线在途改动(git status:M 该文件+untracked desktop/resources/components.json、desktop/src-tauri/src/pyenv_components.rs),**外来域红非本批文件**;本批全部文件(tests/pipeline/test_analysis_lane.py、tests/desktop/test_installer_resources.py、tests/plugins、tests/engines、tests/test_gates.py)在同跑中全绿。与复审修提交前亲跑 1409 passed/39 skipped(引自回执)对照:总数同 1409,恰为该 pyenv 件随并行线推进翻红 |
| 代码锚点亲读 | pipeline.py:1895/:1934/:1946;store/base.py:110;cli.py:145/:3313/:3381-3411;tauri.conf.json:70-77;plugins/ 三新件目录清单;tests/pipeline/test_analysis_lane.py(20 test 函数)/tests/desktop/test_installer_resources.py(7 test 函数,参数化 40 例引自回执) |
| `ls plugins/`(myssia-* 计数) | **官方场景件 20**(批一 13→批二 17→批三 +3:snownlp/yake/mediacrawler) |

**引自回执(非本次亲跑,如实注记)**:

- 批三收录:门禁 `pytest tests/pipeline tests/plugins tests/test_gates.py -q`=842 passed/31 skipped;全树 4199 passed 零回归;snownlp/yake 两 adapter 各真跑冒烟一次 exit 0。
- AC5:`pytest tests/desktop -q`=206 passed(含守卫 27 例);gitnexus impact `_seed_first_run`=LOW 单调用方。
- 小修:`pytest tests/engines tests/test_gates.py -q`=429 passed/8 skipped;邻接 tests/plugins tests/desktop=773 passed/22 skipped;ruff 四文件净。
- 落账复核:`pytest tests/plugins tests/pipeline tests/desktop tests/engines tests/test_gates.py -q`=1394 passed/39 skipped(首轮绿零修复轮);ruff 全部已提交 py 文件 All checks passed。
- 复审修两笔:同命令=1409 passed/39 skipped(提交前亲跑);detect-changes 119f57f=No changes detected(配置+文档+测试)/0349930=3 文件/5 符号/0 流程/low。
- 归档轮:全量门禁绿(引自收口指令,本会话未重跑全量)。

## 五、归档清单(引自收口指令;归档提交哈希=本次实测 git log 逐档核)

归档主体=**10-05-messaging-heading-levels**(连带 held 8 档),共 9 档全部已在 `archive/2026-10/`,活区仅余 10-03-v12-backlog(池,永不归档)+10-05-plugin-market-batch+10-05-table-restore(并行线)+两新引擎档:

| 档 | 归档提交 |
|---|---|
| 10-05-messaging-heading-levels | 2c9a65c |
| 10-04-unified-dev-entry | 3d486e8(随 e2e 架构自适应笔移入) |
| 10-04-wrapup-checklist | 0fffda7 |
| 10-04-yaml-editor-no-scroll | e2dbbaa |
| 10-05-keychain-silent-listing | 3608d1d |
| 10-05-push-credential-journey | 9652610 |
| 10-05-push-reliability-batch | 8b809a6 |
| 10-05-run-once-result-dialog | 5d5a6f8 |
| 10-05-test-result-dialog | 11b622c |

## 六、复审处置(10 项 4 修,计数引自收口指令)

10 项逐条清单未随指令下发至本会话,无法逐项对号——如实记;已落地的修复以两笔 fix(review) 提交为证(提交信息=本次实测 git show 亲读):

| 提交 | 域/严重度 | 发现 | 修复 |
|---|---|---|---|
| **119f57f** | ac5 域 medium | AC5 ③「desktop tier 全件 7 件」与 c43144b 同批分析件漂移——snownlp/yake(EXPECTED_TIERS test_plugin_packages.py:110-111)与 mediacrawler 桩(:112)未入随包面,「装机包=官方件全集」措辞失真 | 补齐而非改口径:snownlp/yake 并入三件套面(9 件)+mediacrawler 桩形两件(plugin.yaml+README.md);tauri.conf.json 外科 +8 行(快照外科:pyenv 并行 hunk 一行字节未动);守卫 32→40 例;prd AC5 追加复审修复注记;门禁 1409 passed/39 skipped |
| **0349930**(两缺陷) | 批三域 | ①装载段失败容器缺口:import_analysis_adapter 装载失败(OSError/SyntaxError/exec 顶层抛,含依赖缺失)不是 AnalysisLaneError,原 except 接不住→analyze 阶段被打翻→push 连坐跳过→run 翻 partial,违反铁律;②无 content 条目拼串:content=None 时 f-string 拼出字面 'None' 发给 adapter,与 title-only 注记语义自相矛盾 | ①捕获面放宽为 Exception,统一归 analysis_lane_degraded_load_failed 降级(warnings+skip 计数,绝不进 failures),+3 参数化例;②`item.content or ''` 归空,+2 例;门禁 1409 passed/39 skipped |

计数口径说明:两笔提交具名缺陷 3 个,其中 AC5 修复含「三件套面并入」与「mediacrawler 桩形映射」两个子项——与「4 修」计数吻合的拆法=①三件套面②桩形③装载段④None 归空;此拆法系本会话推断,具名清单以提交信息为准。

## 七、遗留与如实记档

1. **桌面设置屏分析件卡仍为 D8 禁用占位**(UI 面不在本批清单;激活通道=CLI `myssia gates set analysis.<key> on`,设置面卡待后续批解锁)。
2. **title-only 续跑条目按 skip 计数+DEBUG 处理**,D10 附注「记 warning」未逐字执行——lane 内无法区分「续跑 content 退化」与「源本来无 content」,防 title-only 源常态误报;裁量已记档(prd AC9 批三回标②)。
3. **真包安装冒烟未跑**(发布前必跑项),需 tauri build 出包,归 CI desktop-release/发布流程(prd AC5 记档)。
4. **装机安装接线**(Resources/plugins/<pkg> 作市场安装来源的发现/一键通道)不在 AC5 三件事内,后续件另立(prd AC5 记档)。
5. **gates.py:494 docstring 例键早稿未改**——D10-2 明示为示意串无需改码,键名一律 plugin 派生。
6. **install.source 全仓 20 件旧仓名**:gh api 双向核验(repos/xinzhuzi/shishi 重定向回 full_name=xinzhuzi/myia,与 git remote 一致)证明远端实名=myia 无错,AGENTS.md shishi 注记系历史漂移;ead33f7 对 crawlab YAML 注记重定向策略,统一切 shishi 留批末专项。
7. **yake `__version__` 自报 0.7.1 属上游忘 bump**,安装指引按 PyPI 0.7.3(README 记档)。
8. **task.json 维持 in_progress**:批三域全部落地+回标,但整体转 review/归档未获指令,留主人裁(批二收口段先例:转 review 与后批处置一并)。
9. **外来脏树全程零触碰且仍在树**:table-restore 线(.trellis/tasks/10-05-table-restore/、schema.py、vision/{__init__,collect,table}.py、tests/vision/*、pyproject.toml)、pyenv 线(main.rs/pyenv*.rs/components.json/pyenv-card.tsx/pyenv-api.ts/test_pyenv_resources.py;tauri.conf.json 的 components.json hunk 系该线追加,本批捆齐内容经 60fff33+119f57f 核对在位)、journal-1.md(批三 ask 无 journal 笔,循既有留树惯例);本次实测五组门禁的 1 例红即 pyenv 线在途件(test_pyenv_resources.py:151),外来红不代修。
10. **implement.md 回标曾缺席**:批三收录会话因该文件被并行会话改写中而放弃回标(别人半成品不碰),其执行记录以回执为准——本步(批三收口)补齐勾选注记与批三新节(步骤 17-22)。

## 八、本步回填动作

implement.md(步骤 8/9 勾选注记+批三新节 17-22)、prd.md(AC5 回标 commit pending→60fff33/119f57f 实哈希;AC9 批三回标段)、evidence/batch-3-report.md(本文)三文件一笔提交 `docs(task): 批三+AC5+归档清理回填`;research.md TikTokDownloader 结论核毕无需改(盘点表行+未核项节双落在案);task.json 零改动;未 push 未打 tag。
