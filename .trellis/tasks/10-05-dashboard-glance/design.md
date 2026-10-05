# 技术设计:仪表盘一眼看懂

## 0. 边界与不变量

- 改动面(grill 后扩大):dashboard 三件 + `screens/logs/logs-screen.tsx`
  (dry 徽标,及其测试)+ `settings/label-hint.tsx` 上提
  `src/components/label-hint.tsx` + settings 引用处改 import;
  **零 sidecar 协议改动、零共享基件改动**(`@/lib/api` 与 `ui/tooltip`
  基件只消费不动;上提的是业务消费入口组件,基件本体不碰)。
- spec 遵守(frontend-ui.md):token 单源(语义四色/字号阶梯/间距 scale);
  **零新样式家族**——verdict 行与告警清单复用 StatusDot 解剖、现阶字号,
  无新 arbitrary 值;新结构带出处注释(规范 #4)。
- 诚实原则贯穿:null 显 —/省略,错误明文,无数据不虚构 0。

## D1 `buildVerdict` 纯函数(api.ts)

```ts
export type VerdictTone = "dead" | "warning" | "ok" | "unknown";
export interface DashboardVerdict {
  tone: VerdictTone;
  /** 主句:选词与着色依据 */
  headline: string;
  /** 次段短语(今日收获),逐项可缺 */
  facts: string[];
}
export function buildVerdict(input: {
  overview: OverviewStats | null;
  health: SourceHealthCounts | null;
  categories: CategoryCardModel[];
  runSummary: RunSuccessSummary | null;
  doctorFailed: boolean; // sectionErrors 含 doctor 或整屏 error
}): DashboardVerdict | null;
```

- 返回 null = 不渲染(整屏 error 态,错误卡已负责,不双报)。
- 语气阶梯(最坏优先,纯函数可测):
  1. `doctorFailed` → unknown「部分数据不可达,状态未知」;
  2. `health.dead > 0` → dead「{dead} 个源失效」;
  3. `alerts > 0 || health.degraded > 0 || categories 含 dead tone` →
     warning「{alerts} 项告警 · {degraded} 个源退化」(缺段省略);
  4. 否则 ok「一切正常」。
  (grill Q2:「采集中」不占 headline——headline 只留最坏态定性,
  运行中属动态信息进 facts,与失效/告警并存时不互相顶。)
- facts 次段(所有态都拼,逐项可缺,缺数省略不显 0——grill Q3):
  采集(grill Q1:随概览窗文案「今日 X 条 / 近 N 天 X 条」,与四格
  同窗同数)· {active}/{total} 源在线 · 推送成功 X · {running} 个
  采集中(>0 才拼)。

## D2 verdict 行组件与位置

- 位置:屏 root **首块**(无头范式,PageHeader=null 不复活;先于概览
  section),`px-6` 常驻内容行——不是 toast、不做大横幅(主人弹窗判例:
  屏顶横幅慎用;此为内容不是提示)。
- 解剖(零新样式):StatusDot 家族「状态点+词」(点色复用 SOURCE_STATE
  四色 token)+ headline(text-base medium)+ facts(text-xs muted,
  `·` 分隔)。状态不只靠色:headline 文字本身达意(可达性约定)。
- 交互:dead/warning 态整行包 `<a href="#/sources">` 跳源管理(与 R2 清单
  同目的地);ok/unknown 态纯文本。
- `role="status"` + `aria-label` 汇总句;`data-testid="dashboard-verdict"`。
- pyenv 未就绪走既有错误卡/门禁横幅路径(`SIDECAR_ERROR_HINTS` 已人话),
  verdict 不另起炉灶不双报;verdict 句不带 UTC 括注(口径注记由 ⓘ 承载)。

## D3 告警清单(AlertList;深化轮修触发口径)

- 位置:概览 section 内、四格 grid 之下。
- **触发与内容口径(两数据面不重合,双向都要兜)**:`alerts` = doctor
  findings 计数——可只打品类级(scope `plugin:<file>`,零坏源);坏源 =
  源健康 state≠ok——基线退化可无 finding。故:
  - 触发 = `alerts > 0 || badSourceCount > 0`;两者皆零 = 零占位。
    (badSourceCount = dead+degraded+unknown;unknown 源入清单但 verdict
    不升态——观测缺失非故障,灰点+「未知」词已自释。)
  - 内容 = 坏源行优先;坏源不足 3 行且存在品类级 error/warning
    findings 时,补品类行(品类名 + `finding.message` 截断,
    `title`=全文;Finding 形状 `{severity, scope, code, message}`
    已实核 lib/api/types.ts:254)。
  - 溢出口 N = 清单外剩余异常数(坏源 + 品类级 findings,如实计)。
- 坏源行解剖复用 SourceCard 首行语言:StatusDot(title=完整 reason)+
  源名(text-sm medium)+ 品类名 muted + 相对时间 muted 右置。
- reason 直用原文(grill 事实核:`evaluate_source_health` 的 reason 已是
  人话——「连续 3 轮采集失败(引擎链耗尽/超时)」「本轮产出 N 条」等,
  技术括注属可接受小字,零映射表);行内截断,`title`=完整 reason。
- 溢出口:「还有 N 个异常 · 查看全部 →」`<a href="#/sources">`。
- `data-testid="dashboard-alert-list"`。

## D4 StatCell 口径悬停(grill Q5:ui/tooltip 基件,弃原生 title)

- 前置:`settings/label-hint.tsx` 上提 `src/components/label-hint.tsx`
  (10-05-ui-chore-batch ① 先例的组件共享化;settings 引用处 grep 改
  import,行为零变化,scoped 回归)。
- 消费方实核(3 文件,均只改 import 行):`field-input.tsx` /
  `pyenv-card.tsx` / `settings-screen.tsx`。
- 并行风险:`pyenv-card.tsx` 有并行会话在途改动(git status 在案)——
  import 行冲突面极小;若真撞车,退「dashboard 屏内私有复制」案,
  上提挪后续批次,不阻塞本档主件。
- StatCell 增 `noteKind?: "meta" | "alert"`(缺省 meta):
  - meta → note 文本进 ⓘ 提示(HintButton 形态:CircleHelp +
    `ui/tooltip`,a11y 契约=基件自测同口径,键盘 focus 可达);扫读面
    只剩标签+大数字。
  - alert(趋势不可达/诊断不可达/pyenv)→ 明文照旧,**错误不藏 hover**。
- 判据不嗅探字符串:调用处显式传参(错误分支自己知道自己是 alert)。

## D5 活跃源分母

- value={`${active}/${total}`}(tnum 全局已开);note 仍走 hover。
- 采集/推送/告警格不变(分母无意义;告警格 destructive 着色照旧)。

## D6 文案映射表(可见文案,旧 → 新)

| 旧 | 新 |
|---|---|
| 近期 run 成功率 | 最近采集成功率 |
| 全部 run → | 全部采集 → |
| 还没有 run 记录;跑一次采集后… | 还没有采集记录;跑一次后… |
| `dry` outline 徽标 | 试跑(title 留「dry run(不落库)」;grill Q6 **两屏同改**:dashboard-screen.tsx:274 + logs-screen.tsx:245) |
| {n} 个源 · 坏者(dead → degraded → unknown)靠前 | {n} 个源 · 异常优先 |
| 已载品类、调度与诊断评级(0 error / N warning)(**静态残留,原就未模板化**) | 已载品类、调度与诊断评级(grill Q8 动态三态:{d} 品类异常 / {w} 品类有提醒 / 无异常) |
| SECTION_LABELS:历史 run / 进行中 run | 历史采集 / 进行中采集 |

- aria 同步人话(grill Q7:读屏念出来的行话也是行话):趋势/成功率
  aria-label、概览区 aria-label 等随可见文案换词。
- 不动(title/注释=技术小字判例):「手动触发该品类采集一次(run.start)」
  title、#id mono、状态芯片词(成功/失败已人话)。
- 审计:`grep -n "run" dashboard-screen.tsx` 逐条过,可见层清零、注释层
  不动;再全 ui-src grep 复核无别屏引用(SECTION_LABELS/「全部 run」均
  屏内私有)。

## D7 测试策略

- 纯函数:`buildVerdict` 单测进 `dashboard-screen.test.tsx`(单屏单测文件
  的既有组织,不另开新文件惯例)——四态 + facts 逐项缺省 + null 分支。
- 组件:verdict 四态渲染/错误态零渲染 + facts 随概览窗(grill Q1);
  清单 >0 三条可点 /=0 零占位 / 溢出口;ⓘ tooltip 内容断言(明文 note
  断言改触发后查 TooltipContent——「即时快照不随窗」等 11 处旧文案
  断言同笔换形态);分母 `12/14` 文本;旧文案断言全量换新。
- 跨屏:logs dry→试跑断言;label-hint 上提后 settings 屏 scoped 回归
  (引用改路径,行为零变化)。
- 门禁:`cd desktop/ui-src && npm run test`(全量 vitest)+
  `npm run build`(tsc -b + vite);根 `uv run pytest` 全量兜底。

## D8 风险与回滚

- 单屏文件+屏私有 api.ts,单提交制;revert 即回滚,无数据/协议迁移。
- 文案改动牵动测试面大(旧断言多)——S5 一次清完不留半新半旧。
- 并行会话:dashboard/logs/settings 路径当前无在途改动;提交纪律照
  共享暂存区判例(pathspec 限定本档文件集:dashboard 三件+logs 两件+
  label-hint 上提与 settings 引用处)。

## D9 文案全稿(执行直抄;深化轮实核定稿)

- verdict 例句矩阵(headline · facts,缺段直接省略):
  - ok 静态:「一切正常 · 今日采集 128 条 · 12/14 源在线」
  - ok+运行:「一切正常 · 今日采集 128 条 · 12/14 源在线 · 2 个采集中」
  - warning:「3 项告警 · 2 个源退化 · 今日采集 128 条 · 12/14 源在线」
  - dead(行可点跳源管理):「2 个源失效 · 今日采集 128 条 · 12/14 源在线」
  - unknown:「部分数据不可达,状态未知 · 其余分区已降级显示」
  - 窗口档随概览窗(grill Q1):「近 7 天采集 900 条」替换「今日…」段。
- 告警清单行:「● 源名 · 品类名 — 连续 3 轮采集失败(引擎链耗尽/超时) ·
  3 小时前」(reason 原文直用);溢出口:「还有 N 个异常 · 查看全部 →」。
- 品类节注三态:「无异常」/「{d} 品类异常」/「{w} 品类有提醒」(组合取
  最坏优先:d>0 只报异常数,否则 w>0 报提醒数)。
- aria 改点实核(全屏 grep 后仅一处带 run):成功率趋势 aria
  「…无完结 run 的日子不入线」→「…无完结采集的日子不入线」;其余 aria
  (今日概览/采集量趋势/源健康度/品类状态/刷新数据/概览与趋势时间范围)
  已人话,不动。
- hover note 人话化规则(深化轮补):note 进 ⓘ 时顺手换人话——
  「今日(UTC)run 的 ok 推送 · 受 runs.list 20 条上限」→「今日(UTC)
  各轮采集的推送成功数 · 受最近 20 轮上限(runs.list)」;技术标识
  留括注,hover 小字允许 trace 但不裸放。
