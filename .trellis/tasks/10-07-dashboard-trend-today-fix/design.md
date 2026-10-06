# design — 仪表盘趋势卡「今日」档退化修复

> 需求与根因证据矩阵见 [prd.md](./prd.md)(§1 机制链五环,每环行号亲核);本档只做技术设计,不重复举证。
> 方向 = PRD 方向 A:两图图窗设 7 天下限与概览窗解耦,概览四格与 verdict 口径不动。
> grill 六问全批按推荐(2026-10-07):Q1 下限 7 / Q2 标签如实不加解释 / Q3 摘要跟图窗 / Q4 全零刻度纳入(→D8)/ Q5 同窗切换不弃旧窗(D6 修订)/ Q6 像素验收 devUrl(implement 批3)。

## §0 改动面总览

三个文件,全部在 `desktop/ui-src/src/screens/dashboard/` 屏内(api.ts 消费方唯一性已核:`rg overviewTrendDays|buildOverviewStats|fetchTrendWindow` 与跨屏 `import .../dashboard/api` 在 dashboard 目录外零命中):

| 文件 | 改动 |
|---|---|
| `api.ts` | +`CHART_WINDOW_MIN_DAYS` / +`chartWindowDays()`;`buildOverviewStats` 采集格改概览窗切片;注释更新 |
| `dashboard-screen.tsx` | 两处 `refreshTrend` 调用点换 `chartWindowDays`;趋势卡内文案/aria 换图窗标签;注释更新 |
| `dashboard-screen.test.tsx` | 既有断言翻新(design §5 清单)+ 新增 AC 断言 |

UI 零 token/零样式改动(纯数据装配与文案),frontend-ui.md 检查单 #1/#4 不触发;#5 测试同步见 implement 批2;#6 协议红线 = 零方法增删零版本 bump。

## §1 决议

- **D1 拉数形态:一窗拉宽 + 客户端切片(弃「今日档双拉」)**。今日档把两图的拉数窗直接放宽到 7 天,概览四格所需当日数由纯函数从 7 天窗内切片取得。理由:①少一次 sidecar 往返;②切片落在 `buildOverviewStats` 纯函数层,可单测;③「一窗一拉」架构(补批四决议,trend 由趋势卡与概览四格共享)与迟响应护栏(`trendSeq` 序号整笔丢弃)原样保留,不引入第二份 trend 状态。
- **D2 图窗下限 = 7 天**(`CHART_WINDOW_MIN_DAYS = 7`)。取 `TREND_WINDOW_DAYS [7,14,30]` 最小档:与概览 Select 档位族对齐、与既有「近 14 天」文案同构;≥2 点即成线,7 天保证有基线语境(「今天 vs 近几天」),不是只为消单点的最小修补。(grill Q1 批;14 落选=今日/7 天两档图完全同窗,Select 档位感知变糊)
- **D3 图窗换算:`chartWindowDays(window) = max(overviewTrendDays(window), 7)`**。契约:图窗 ⊇ 概览窗恒成立(今日 7≥1;7/14/30 相等)。保留 `overviewTrendDays` 不删——它仍是「概览窗语义」的编码,`chartWindowDays` 组合它;`buildOverviewStats` 的切片边界也由概览窗决定,两者职责分离。
- **D4 概览窗切片(采集格/verdict 口径不虚增)**:`buildOverviewStats` 的 `windowItems` 由 trend 整窗求和(`api.ts:535`)改为先按 `[windowStart..today]` 切片再求和。`windowStart` 现算已有(今日档=today);YYYY-MM-DD 字符串字典序比较即日历序。输入契约放宽为「trend 窗 ⊇ 概览窗、右端=today」(fillDailyCounts 保证)。trend 拉取失败 → null → 格显「—」语义不变。verdict 消费 `overview.window/windowItems`(`api.ts:589-594`),自动保持概览口径,**零改动**。
- **D5 标签归属两分法(PRD R2 修案)**:概览四格 + verdict = 概览窗 `windowLabel`(今日/近 N 天,不变);趋势卡内一切(两图 aria、卡脚合计、峰值、轴行、成功率区摘要与空态文案)= 图窗标签,取 `近 ${chartWindowDays(overviewWindow)} 天`——7/14/30 档与现 `windowLabel` 逐字相同,今日档为「近 7 天」。`cumulativeOutcomeSummary(outcomes)` 吃的就是拉数窗,数字天然跟图窗,**不切片、仅换标签**(数字-标签同窗,不撒谎)。今日档图示「近 7 天」**不加解释文案**(grill Q2 批:标签如实即够,解释是给设计者的噪音;「UTC 逐日」徽章已是口径注记位)。摘要跟图窗经 grill Q3 终裁——与「最近采集成功率」卡双口径并存系既有形态(卡面已注「不同源,不冒充同源」),各自如实注记。
- **D6 today↔7 天同窗切换:不弃旧窗,重拉保留(grill Q5 修订,原「冗余重拉保留不改」作废)**。两档 `chartWindowDays` 同为 7,沿用「切窗即 `setTrend(null)`/`setOutcomes(null)`」会让今日↔7 天切换闪一下骨架屏再显出一模一样的图——可见退化。修法=Select `onValueChange` 仅当 `chartWindowDays(next) !== chartWindowDays(overviewWindow)` 时才弃旧窗(一行守卫);effect 同参重拉保留兜底刷新(冗余往返无正确性影响)。白闪消除原理=骨架屏仅在 `trend === null` 时渲染(`dashboard-screen.tsx:1044`),不弃旧窗则旧图原地保留、新数据无声替换;四格靠 D4 切片立即正确(同一份 7 天数组,今日档取当日行/7 天档整窗和皆对)。14/30 天切换照旧真实弃旧窗(竞态护栏本体零改动)。
- **D7 不改面(红线)**:`sparkline.tsx` 单点渲染语义(其他消费面在);`store.trend`/`runs.trend` 协议与 `fetchTrendWindow`/`fetchOutcomeWindow` 签名;`OVERVIEW_WINDOW_DEFAULT`(今日仍是默认概览档);Select 选项族;`fillDailyCounts` 补零语义;`trendSeq` 迟响应护栏;概览四格 note 文案与 verdict 词表。
- **D8 全零窗 y 轴刻度守卫(grill Q4 纳入)**:趋势卡 `yLabels` 在 `trendPeak === 0` 时传 `undefined`(`TrendChart` 的 `yLabels?: [string, string, string]` 元组类型硬取三位,不可传部分数组,`dashboard-screen.tsx:616`;缺省=刻度列整体不渲染,属组件已认可态)。理由:现状全零窗渲染「0/0/0」三零叠刻度——今日档默认 7 天窗后,装机首屏必经全零态,属同类退化,不修即漏。折线全零居中平线、卡脚「共 0 条 · 峰值 0 条/日」已把语义说尽,刻度列冗余。rate 图定刻度 `["100%","50%","0"]` 不受影响(零完结走空态文案分支不画图,`:1108-1111`)。

## §2 契约(公开面变更,全部屏内)

```ts
// api.ts 新增
export const CHART_WINDOW_MIN_DAYS = 7;
/** 两图(采集量/成功率)图窗天数:概览窗下限 7(图窗 ⊇ 概览窗恒成立) */
export function chartWindowDays(window: OverviewWindow): number;

// api.ts 语义变更(签名零变化)
buildOverviewStats(...)  // windowItems: trend 整窗和 → 概览窗切片和
                        // (输入契约放宽:trend 窗 ⊇ 概览窗、右端=today)

// dashboard-screen.tsx(屏内私有,不进 api 公开面)
const chartWindowLabel = `近 ${chartWindowDays(overviewWindow)} 天`;  // 今日档=近 7 天
```

调用点切换:`dashboard-screen.tsx:817`(effect)与 `:947`(刷新钮)`overviewTrendDays(overviewWindow)` → `chartWindowDays(overviewWindow)`。
屏内新增两处守卫(不进 api 公开面):
- 趋势卡 `yLabels={trendPeak === 0 ? undefined : [...]}`(D8;元组类型不可传部分数组);
- Select `onValueChange` 弃旧窗条件化:`chartWindowDays(next) !== chartWindowDays(overviewWindow)` 才 `setTrend(null)`/`setOutcomes(null)`(D6)。

注释四处随语义改写:screen `:759-762`(头注「今日档 = 1 天趋势窗(单点…如实画)」)、`:783-791`(refreshTrend 注)、`:914-915`(Select 注,含弃旧窗条件化);api.ts `:431-435`(统一时间窗注释块)。

## §3 数据流(改后)

```
今日档:  Select(today) → chartWindowDays=7 → refreshTrend(7)
          → store.trend/runs.trend({days:7}) → fillDailyCounts(7) → trend[7 天]
          → 图+卡脚+成功率摘要(标「近 7 天」)
          → buildOverviewStats(trend, window=today):切片 [today..today] → 采集格=当日数
          → verdict facts「今日采集 X 条」(不变)
7/14/30: chartWindowDays=window → 与现状逐字节相同(拉参/数据/标签/aria 全等)。
今日↔7 天切换(D6):图窗同参 → 不弃旧窗、effect 同参重拉兜底 → 无骨架屏白闪,四格即时重算。
全零窗(D8):7 日皆 0 → 平线、y 刻度列不渲染、卡脚「共 0 条 · 峰值 0 条/日」。
```

## §4 测试矩阵(AC 映射)

| AC | 断言(落 `dashboard-screen.test.tsx`,纯函数与组件混排沿用本文件既有模式) |
|---|---|
| AC1 | 默认渲染(今日档)mock 多日 trend:`trend-axis` 首末日不同;`trend-total` 含「近 7 天共 N 条」;sparkline 序列 ≥2 点(rate 区同断言序列长度);全零窗(7 日皆 0)→ 无 y 刻度列 + 平线 + 「共 0 条 · 峰值 0 条/日」 |
| AC2 | `buildOverviewStats`:7 日 trend 输入 + today 档 → `windowItems`=当日行(非 7 日和);verdict 文本仍「今日采集 X 条」;7 日档 → 整窗和(既有行为回归锚,防切片误伤) |
| AC3 | 趋势卡 aria 含「近 7 天」;7/14/30 档全部文案与现状逐字一致(既有断言 `:1144`「近 14 天共 3 条」原样过) |
| AC4 | 见下「既有断言翻新清单」+ D3 契约断言(`chartWindowDays` 四档取值)+ D6/D8 守卫断言:今日↔7 天切换不闪(切后 `trend-total` 仍在文档、无骨架屏)且 `storeTrend` 同参重发;14 天切换仍弃旧窗(既有竞态测试) |
| AC5 | implement 批3 门禁与像素验收 |

**既有断言翻新清单**(`dashboard-screen.test.tsx`,逐条):

| 位置 | 现断言 | 改为 |
|---|---|---|
| `:933-994` 概览条 | `storeTrend` 以 `{days:1}` 调用 | `{days:7}`;采集格值断言不动(mock 单日行,切片后仍 5) |
| `:994` 注 | 「统一时间窗:默认今日 = 1 天窗」 | 图窗下限语义 |
| `:1083-1107` 迟响应竞态 | today↔7 天对做挂起/迟回 | 改 today↔**14 天**对(两档图窗不同参才测得出弃旧;护栏逻辑零改动) |
| `:1116-1144` 趋势统一窗 | 测试名「默认今日 = 1 天窗单点如实画」;`今日共 3 条`;`{days:1}` | 名改「默认今日 = 图窗下限 7 天补零窗」;`近 7 天共 3 条`;`{days:7}`;补「轴行首末日不同」断言;切 14 天段不动 |
| `:1333-1352` rate 区 | 「默认今日 = 1 天窗」;`runsTrend` 后断 14 天 | 默认断 `{days:7}` + 序列断言随 7 天 mock 重算;切 14 天段不动 |
| `:1355-1375` 统一窗 | 两处 `{days:1}` | 两处 `{days:7}` |
| `:408-494` verdict | (稀疏单日 mock) | **预期零改动**——切片后仍取当日行;列此防误改 |

## §5 兼容 / 回滚

- 分两个提交点(批1 纯函数层、批2 消费层+测试),任一批独立可 revert;全档 revert 即回到现状。
- 协议零新面(前端单侧改动,sidecar 零触碰);golden 与其余七屏零波及(dashboard/api 无跨屏消费方,§0 已核)。
- 风险点:`buildOverviewStats` 切片改变了「trend 窗 ≡ 概览窗」的隐含前提——已核消费方唯一(screen 本地),测试矩阵 AC2 行为锚双侧(今日切片 + 7 日整窗)钉死。
- `今日↔7 天` 切换(D6 修订后):同参重拉保留、无正确性影响;不弃旧窗守卫有断言钉死(不闪);14/30 弃旧窗行为由既有竞态测试锚定。
