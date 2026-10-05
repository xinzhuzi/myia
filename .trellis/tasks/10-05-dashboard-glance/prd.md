# 仪表盘一眼看懂:状态句先行+告警升格+口径收悬停+文案人话

## Goal

打开仪表盘第一眼即得一句结论——「系统还好吗 / 今天有什么新东西 / 有没有要我处理的」,
不再让用户从四格数字+源网格+品类徽标里自己拼答案。扫读面只剩「标签+大数字+状态色」,
复核性口径注记收进悬停;可见文案清零 run 行话(→采集)。

## 背景与现状(锚点)

- 2026-10-05 主人问「仪表盘的展示内容,如何让人一眼看懂」,AI 评估出七条;
  主人令「具体落入到 trellis 任务文档里面」。低风险四条+文案件入本档,
  交互语义两件(双时间窗收敛/源健康度默认折叠)记边界待翻案(见下)。
- 屏现状:`desktop/ui-src/src/screens/dashboard/dashboard-screen.tsx`(约 1038 行):
  概览四格(StatCell,note 明文挂口径小字)→ 采集量趋势+成功率 → 源健康度
  网格 → 品类状态 → 近期 run 成功率+反馈统计。数据装配
  `dashboard/api.ts` 全齐:`OverviewStats`(windowItems/activeSources/
  totalSources/alerts)、`summarizeSourceHealth` 四态计数、
  `buildSourceHealthCards`(坏者靠前排序已做)、`runSummary.running`——
  **verdict 句零新拉数、零协议改动**,纯前端装配。
- 无头范式:PageHeader 渲染 null(2026-10-04 主人「无头」指令),屏首块即
  内容——verdict 句做成**屏内第一块**,不复活页头。
- 行话判例:cron-ui 主人抓过 ticker/job/裸路径;弹窗判例=行话 trace 收
  技术小字。仪表盘可见文案同标准;title/aria 属性里的 run.start 类技术注
  可留(即「技术小字」落点)。

## Requirements

1. **R1 状态句先行(verdict)**:屏内第一块渲染一句话总状态:headline 只
   承载最坏态定性(失效/告警/正常/数据不全,grill Q2),facts 次段拼收获
   与动态(随概览窗的采集 X 条 · M/K 源在线 · 推送成功 Y · N 个采集中;
   逐项缺数省略不虚构、不显 0,grill Q1/Q3);数据全来自既有装配。
   整屏错误态不渲染(错误卡已负责),doctor 分区失败显「数据不全」级。
2. **R2 告警升格清单**:触发 = 告警(findings)>0 **或** 坏源(state≠ok)
   >0(深化轮修——两数据面不重合:findings 可只打品类级、退化可无
   finding);概览区下方渲染异常清单前三条(坏源行优先:状态点+源名+
   原因+相对时间;坏源不足且存在品类级 findings 时补品类行),点行跳
   源管理(#/sources);溢出口「还有 N 个异常 · 查看全部 →」(grill
   Q4:3 条封顶);两者皆零时零占位。
3. **R3 口径注记收悬停**:StatCell 的口径型 note(UTC 口径/20 条上限/
   快照不随窗)收进 ⓘ 提示(grill Q5:走 `ui/tooltip` 基件,
   `settings/label-hint.tsx` 先例上提共享,弃原生 title),扫读面只剩
   标签+大数字;**错误/降级型 note(趋势不可达等)保留明文**——错误
   不藏 hover。
4. **R4 数字带分母**:「活跃源 12」→「12/14」(totalSources 已有);
   告警格照旧纯数(分母无意义)。
5. **R5 文案人话**:可见文案全量换词(近期 run→最近采集、全部 run→→
   全部采集→、dry 徽标→试跑(grill Q6,**logs 屏同徽标一并换**)、
   坏者(dead → degraded → unknown)靠前→异常优先、SECTION_LABELS 的
   历史 run/进行中 run→采集、品类节注动态三态(grill Q8));aria-label
   同步人话(grill Q7:读屏行话也是行话);完整映射表见 design.md D6;
   注释与 title 技术注不动。

## 测试

- `buildVerdict` 纯函数单测(vitest,api 层):四态(失效/告警/正常/数据不全)
  + 缺数省略 + 整屏错误不渲染。
- 组件测试同步:`dashboard-screen.test.tsx` 断言旧文案/note 明文的用例
  同笔更新(「即时快照不随窗」等明文 note 断言随 R3 改为 tooltip 触发
  后查内容);新增 verdict 行(facts 随概览窗)、告警清单(>0 三条可点/
  =0 零占位/溢出口)、ⓘ tooltip、分母格式断言。
- 跨屏:logs dry→试跑断言;label-hint 上提后 settings 屏 scoped 回归
  (引用改路径,行为零变化)。
- scoped 自跑:`npx vitest run src/screens/dashboard`;tsc 见门禁。

## 验证

- 离线:vitest+tsc 全绿(测试矩阵上列)。
- 视觉:无头冒烟(Playwright+bridge.mjs+`__TAURI_INTERNALS__` shim 先例)
  或装机包刷新后 `MYIA_SHOW_ON_START=1` 直跑二进制+screencapture+local-ocr;
  按判例(交付完成判定含装机包)AI 自己验到像素级,回执贴档 evidence/,
  留主人只余审美。

## Acceptance Criteria

- [x] AC1 verdict:四态快照断言+像素回执;facts 随概览窗、缺数省略;零新拉数。
- [x] AC2 告警清单:告警或坏源非零时渲染前三行(坏源优先、品类 findings 补位)可点跳源管理;皆零时零占位(触发双口径各有用例)。
- [x] AC3 口径悬停:口径 note 移入 ⓘ tooltip(ui/tooltip 基件,label-hint 上提共享),错误型 note 仍明文。
- [x] AC4 分母+文案:活跃源 12/14;两屏(dashboard+logs)可见文案 run 清零、dry→试跑、aria 人话(测试断言新文案)。
- [x] AC5 门禁:`cd desktop/ui-src && npm run test` + `npm run build`(含
  tsc -b)全绿;根 `uv run pytest` 全量兜底零新红。
- [x] AC6 装机包:刷新+像素级验证(截屏+OCR 证据入 evidence/)。
  ——已销号(主会话 2026-10-05 夜补):tauri build 重打包(世事.app
  17.07MiB,adhoc)静默换装 /Applications/世事.app(优雅退出+清 WKWebView
  缓存)+MYIA_SHOW_ON_START=1 直跑+screencapture -l 窗取证+local-ocr 两级链
  (Vision 一级+本机 VL 二级校对五关键行全对):warning 态 verdict「8 项告警 ·
  今日采集 0 条 · 1/21 源在线」、活跃源 1/21、异常优先节注、溢出口逐字在屏
  (evidence/10-installed-app-verdict.png+installed-ocr.txt);无头冒烟另存
  9 帧(mock-bridge 双场景+DOM 探针,见尾部回执注记)。

## 收口回执(2026-10-05)

- evidence/ 产出:无头冒烟(mock-bridge.py 注入 ok/dead 双场景 + bridge.mjs
  +shim 先例)9 帧截图 + probe.json(DOM 探针:verdict ok/dead、四格分母
  5/5、tooltip 文本、告警清单三行+溢出口、品类节注「1 品类异常」、零重叠
  零溢出)+ ocr-level2.json(校对回执)+ harness/(冒烟基建 5 件可复跑)。
- 收口员亲跑门禁四件套全绿:scoped vitest(dashboard+settings+logs)
  185/185;全量 `npm run test` 507/507;`npm run build`(tsc -b+vite)✓;
  根 `uv run pytest -q` 4384 passed 40 skipped 零新红。
- label-hint 上提件(components/label-hint.tsx+field-input/pyenv-card/
  settings-screen 三引用)已随 38acd34 收编提交,本笔不再含。

## 边界与红线

- **不做(记档翻案)**:
  - 双时间窗收敛(概览窗与趋势窗语义不一致,「不随窗」注记即症状)——
    联动合一 or 快照格退窗属交互语义变更,翻案条件=主人点名或下批 UI 档;
  - 源健康度默认折叠正常源(信息架构变更,同上翻案);
  - verdict 句 i18n(单语中文现状)。
  ——前两项已于 2026-10-05 夜随主人令「剩下的问题全部做完」翻案落地
  (补批四/五,见下方「补批」段);i18n 维持不做。
- **红线**:
  - 零 sidecar 协议改动(要新方法=停止回 PRD 重新裁定);
  - 不动共享 `@/lib/api`(装配留屏私有 api.ts);
  - 诚实原则不破坏:null 显 —、错误明文、无数据不虚构 0;
  - 状态不只靠颜色传达(点/图标+文字,spec 可达性约定)。

## 放行回执(2026-10-05 grill 八问,主人令「都按推荐」)

- Q1 verdict 随概览窗(与四格同窗同数,默认态即满足「今日」直觉)。
- Q2 headline 只留最坏态定性;「采集中 · N 个」进 facts。
- Q3 facts 逐项缺数省略,不显 0。
- Q4 告警清单 take 3 + 溢出口「还有 N 个异常 · 查看全部 →」。
- Q5 ⓘ 走 `ui/tooltip` 基件:`label-hint.tsx` 上提 `src/components/`
  共享,settings 引用同步改(原生 title 弃,不走回头路)。
- Q6 dry→「试跑」(title 留 dry run 技术注);logs 屏同徽标一并换。
- Q7 词表按 design D6 放行;aria-label 一并人话;注释/title 技术注不动。
- Q8 品类节注动态三态(无异常 / X 品类异常 / Y 品类有提醒)。
- grill 事实修正:D3 的 reason 人话映射小表删除(cli reason 已是人话,
  原文直用);测试断言面 11 处旧文案在案(含 note 明文断言改形态)。
- 改动面扩大:pathspec = dashboard 三件 + logs-screen(+测试)+
  label-hint 上提 + settings 引用处(执行时 grep 定位)。

## 低危处置回执(2026-10-06,review 三条 low 收口)

- ① 品类补位行 React key 可撞:同品类两条同 code(error_type)的 load_errors
  finding(cli.py `_plugin_findings` 每条 detail 产一条)在旧 key 形
  `category-${file}-${code}` 下会重 key。修复 = 装配循环加品类内序号
  (`${code}-${seq}`,dashboard-screen.tsx `buildAlertRows`),测试 = 同品类
  两条同 code finding 双行均渲染且行 testid(=key)互异。本笔处置时该修复与
  测试已由同窗并行「补批一」落工作树(定向 vitest 亲验 58 用例全绿),不重复
  造件,注记收口。
- ② alert 型 note 明文零护栏:noteKind="alert" 分支(「趋势不可达(code)」
  「诊断不可达 · doctor 分区失败」明文直显、不走 ⓘ 悬停,R3「错误不藏
  hover」)此前零断言。补双护栏:「趋势不可达」半边由并行「补批二」用例
  (store.trend 拒绝 → 采集格明文 + meta 态反向断言)覆盖;「诊断不可达」
  半边由本笔新用例(dashboard-screen.test.tsx「错误不藏 hover(低危②
  护栏)」:doctor 分区拒绝 + 趋势拒绝双错同屏 → 两类明文均在扫读面、alert
  态无 ⓘ 说明钮)覆盖——正向断言,与 meta 态「textContent 不含口径明文」
  反向断言先例互补。实现零改动,定向 vitest 亲验 59/59 绿。
- ③ credentials 级 finding 不触发告警清单的口径缝隙:告警格计数吃 findings
  全量(scope=credentials/store/db 等全局 finding 也计数),而 design D3 的
  清单行口径只定义了坏源行 + 品类级(scope=`plugin:<file>`)finding 补位行
  ——全局 finding 独存时「格>0 清单空」两面不齐,属 D3 档内缝隙。原处置 =
  注记收口不实现(渲染空清单更差);本笔处置时同窗并行「补批三」已在工作树
  以「全局 finding 行」实现收口(findingScopeLabel 人话主体名 + 非 plugin:*
  scope 的 error/warning 行入清单,配测试「格=2 清单=2 行」),两案并存如实
  记档。**残留缝(2026-10-06 复审必改,已收)**:补批三只消除了 error/warning
  半边——计数仍吃 findings 全量而清单行滤 info,cli 实况三处 severity="info"
  (third_party_trace / gate_disabled / analysis_lane_disabled,后两者 message
  明写「正常态,不是故障」)且 gates 未配置即关 → 默认装机态「格>0 清单空」
  复现、正常态被播报成「N 项告警」;修向取「告警格/状态句只计 error+warning」:
  api.ts alerts 过滤 + buildAlertRows 品类行同滤(全局行原有滤)+ 双护栏用例
  (仅 info 默认装机态=格 0/清单空/verdict「一切正常」;info+warning 混合=
  格与清单只吃 error/warning),三面口径同源,本段处置注记以收官树为准。

## 补批(2026-10-05 夜,主人令「剩下的问题全部做完」)

主人 2026-10-05 夜令把剩下的问题全部做完:边界两项翻案放行 + review 在途件
收编,计五件。归属如实记:一~五的实现+测试由同窗并行补批会话落树、随
f795033 收编提交(与 review 三条 low 收口同笔,共享工作树同路径无法拆分);
残留缝复审修 + 补批冒烟取证 + 本段记档随本笔。

- [x] 补批一 key 去重:同品类两条同 code(error_type)load_errors finding 旧
  key 形 `category-file-code` 撞 React key → buildAlertRows 装配循环加品类内
  序号 `${code}-${seq}`(dashboard-screen.tsx:445-450);测试 test:624 同 code
  双条均渲染且行 testid(=key)互异。
- [x] 补批二 明文断言:alert 型 note「错误不藏 hover」(R3)补齐断言——
  「趋势不可达(code)」半边 test:737(store.trend 拒绝→采集格明文+meta 态
  反向断言);「诊断不可达 · doctor 分区失败」半边 test:761(review 批补:
  doctor 分区拒绝双错同屏→两类明文均在扫读面、alert 态无 ⓘ 说明钮)。实现
  零改动,护栏补在测试面。
- [x] 补批三 凭据行型:全局 findings(非 plugin:* scope,如 credentials/store)
  入告警清单——findingScopeLabel 人话主体名(dashboard-screen.tsx:410/473),
  test:647「格=2 清单=2 行」。**残留缝复审修(本笔收口)**:cli 实况三处
  severity="info"(third_party_trace/gate_disabled/analysis_lane_disabled,后
  两者 message 明写「正常态,不是故障」)且 gates 未配置即关 → 默认装机即有,
  计数吃全量会把正常态播报成「N 项告警」、清单滤行则「格>0 清单空」复现;
  修向=告警三面(格/清单/verdict)同源只计 error+warning:api.ts:510 alerts
  过滤 + dashboard-screen.tsx:450 品类行同滤(全局行原有滤)+ 双护栏用例
  test:677(仅 info 默认装机态=格 0/清单空/verdict「一切正常」)/test:713
  (info+warning 混合=格与清单只吃 error/warning);types.ts Finding.severity
  漏声明 info 档的契约修正归共享层批次(红线:不动 @/lib/api),测试以窄
  断言夹具先行,不虚构宽契约。
- [x] 补批四 统一时间窗联动合一(边界翻案第一项,翻案条件「主人点名」即
  告成立):概览头 Select(aria「概览时间范围」,dashboard-screen.tsx:907)
  驱动四格+两折线,趋势卡自有 Select 删除(tsx:1013 注记;今日档=1 天窗
  overviewTrendDays 换算 tsx:801,buildOverviewStats 吃 overviewWindow
  tsx:812);测试 test:913/993/1232(切窗双趋势同窗重查+趋势卡无自有
  Select)。「不随窗」注记随快照格保留(活跃源/告警仍是点快照)。
- [x] 补批五 折叠正常源(边界翻案第二项):源健康度 ok 卡收折叠组默认收起
  (okSourcesExpanded useState(false) tsx:754;原生 button+aria-expanded
  tsx:1185-1193,spec 折叠组惯例),「N 个源正常 · 展开/收起」;零 ok 不
  渲染折叠组;测试 test:1085(默认收起/展开/收起+零 ok)+test:1038(点开
  后正常卡可见)。

复审与门禁(收口员本笔亲跑):

- `cd desktop/ui-src && npx vitest run src/screens/dashboard` = **61 passed/61**
  (f795033 提交态 59 用例 + 复审双护栏 2 新例全绿);
- `npm run build`(= `tsc -b && vite build`,desktop/ui-src/package.json:12)
  ✓,仅既有 chunk 体积警示零新错。

冒烟结论(补批会话无头冒烟跑,回执件在档,收口员逐件核对):

- 8 帧 failures=0(harness/shoot11.log 尾行「S7 补批 11- 取证:shots=8
  failures=0」,log 按 .gitignore:41 不入库);11-probe.json 全帧
  overlaps/overflows 空、docHorizontalOverflow=false;两级 OCR(Vision 一级+
  本机 VL 二级)关键行全部一致(vl_check11.exit=0;17/18 帧形近字符如
  「一/—」「~/)」系 OCR 误读,VL 二级已纠正,屏文以 probe DOM 文本为准
  一致)。
- 帧映射:11/12=统一时间窗 7 天/今日双档(shim params 入痕实证 store.trend/
  runs.trend 的 days 随窗 [1,1,7]→追加 1、趋势卡自有 Select=0、卡头随窗
  「近 7 天概览(UTC)」/「今日概览(UTC)」);13=verdict dead 可点 A;
  14/15=折叠组默认收起(aria-expanded=false「2 个源正常 · 展开」)/展开
  两态;16=cred 场景 verdict「2 项告警」可点;17=凭据行型双行(「异常/
  提醒」前缀+「凭据」主体,告警格=2=清单 2 行、零溢出口);18=doctorfail
  verdict unknown 不可点 DIV+分区降级明文(「诊断不可达 · doctor 分区失败」
  明文在屏,与补批二护栏互证)。
- 如实记:info 过滤半边无冒烟场景(cred 夹具只载 error+warning),该面由
  vitest 双护栏用例(test:677/713)覆盖;补批一 key 去重同为纯单测面。

evidence/ 11- 前缀产出(一行说明):11~18 帧 + 11-probe.json(DOM 探针)+
11-ocr-level1.txt/11-ocr-level2.json(两级校对)+ harness/(shoot11.py/
vl_check11.py 可复跑件+vl_check11.exit 回执;mock-bridge.py 增 cred/doctorfail
场景、shim.js params 入痕)= 补批五件+残留缝复审的无头冒烟回执,编号接
10 号装机帧续排。

## 低危三件回执(2026-10-06 凌晨,主会话顺手清;主人「全部做完」口径)

复审补批三 low 全数销号,主会话直改+门禁亲跑:

- ①TREND_WINDOW_DEFAULT 死导出删除(统一窗后全 src 零消费,grep 实核)。
- ②findingScopeLabel:db 死分支删(cli 无 db scope),真实数据库相关
  scope=store 改映射「数据库」(cli.py:3190);测试断言随改
  (toContain("数据库")+not.toContain("store"))。
- ③refreshTrend 迟响应护栏:trendSeq 序号过期整笔丢弃(旧窗慢回不再
  冒充新窗);新增竞态用例(7 天 deferred 挂起→今日先回→7 天迟回 128 条
  被丢弃,格值稳 5)。
- 门禁:全量 vitest 517/517(26 文件)+npm run build(tsc -b && vite)绿;
  pytest 未重跑(本笔纯 UI 零 python 触碰,如实注记)。
