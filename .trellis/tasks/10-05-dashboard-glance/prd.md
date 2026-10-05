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
- [ ] AC6 装机包:刷新+像素级验证(截屏+OCR 证据入 evidence/)。
  ——无头冒烟已取证,装机包刷新待办(mock-bridge 双场景 9 帧截图+DOM 探针
  +OCR 存 evidence/,见尾部回执注记)。

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
