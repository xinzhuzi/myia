# implement — 执行计划

> 前置阅读顺序:implement.jsonl 所列 spec → [prd.md](./prd.md) → [design.md](./design.md) → 本档。
> 铁律:frontend-ui.md 检查单 #5(测试同步同笔)、#6(协议红线零变更);改动全部限定 `desktop/ui-src/src/screens/dashboard/` 三文件。

## 批0 基线(不动码)

- [x] `cd desktop/ui-src && npx vitest run src/screens/dashboard` —— 全绿基线,记 passed 数(翻新前后对照用)
  - 回执(脚本跑,04:20:27):exit 0,Duration 1.51s(transform 142ms / import 250ms / tests 914ms / environment 256ms);回执未带 passed 数,批1 后同文件 73 passed − 新增 2 例 ⇒ 基线 71
- [x] `npx tsc --noEmit -p tsconfig.app.json` 零错基线(实现代理自跑:EXIT=0)

## 批1 api.ts 纯函数层(提交点①,可独立 revert)

- [x] `CHART_WINDOW_MIN_DAYS = 7` + `chartWindowDays(window)`(组合 `overviewTrendDays`,勿复制其逻辑)
- [x] `buildOverviewStats` 采集格概览窗切片:输入 `trend` 先过滤 `[windowStart..today]` 再求和;`trend` 为 null → `windowItems` 仍 null(拉取失败显「—」语义不变);切片空(理论不发生,fillDailyCounts 保证右端=today)→ 和 0 如实
- [x] api.ts `:431-435` 统一时间窗注释块更新(概览窗 vs 图窗两词分立)
- [x] 新增纯函数断言(design §4 矩阵 AC2/AC4 行):
  - `chartWindowDays` 四档:today→7、7→7、14→14、30→30
  - `buildOverviewStats`:7 日 trend 输入 + today 档 → `windowItems` = 当日行数(非 7 日和);7 日档 → 整窗和;trend null → null
- 验证(亲跑双绿):`npx vitest run src/screens/dashboard` = 73 passed(1 file,EXIT=0)+ `npx tsc --noEmit -p tsconfig.app.json` EXIT=0
- **提交点①**(此时 screen 仍传 `overviewTrendDays`,今日档行为未变,纯函数已就位——中间态自洽可过全量)

## 批2 screen 消费层 + 既有断言翻新(提交点②)

- [x] `refreshTrend` 两调用点换 `chartWindowDays`(`dashboard-screen.tsx:817` effect、`:947` 刷新钮)
- [x] 图窗标签 `chartWindowLabel = \`近 ${chartWindowDays(overviewWindow)} 天\``;替换面**仅限趋势卡内**:aria `:1064`、卡脚 `:1078`、成功率空态 `:1110`、成功率 aria `:1122`/`:1124`、成功率摘要 `:1135`。概览四格 note 与 verdict 文案**一字不动**(注:屏内 `windowLabel` 变量原本只被趋势卡五处消费,五处换 `chartWindowLabel` 后失去消费方遂删——概览面「今日/近 N 天」一直是各自内联三元与 `buildVerdict` 拼词,零文案变化;`overviewTrendDays` 屏内 import 同步移除,api 导出面不动)
- [x] D8 全零刻度守卫:趋势卡 `yLabels={trendPeak === 0 ? undefined : [\`${trendPeak}\`, \`${Math.round(trendPeak / 2)}\`, "0"]}`(`TrendChart` 元组类型硬取三位,不可传部分数组;缺省=刻度列不渲染)
- [x] D6 同窗切换守卫:Select `onValueChange` 仅 `chartWindowDays(next) !== chartWindowDays(overviewWindow)` 时 `setTrend(null)`/`setOutcomes(null)`(effect 同参重拉保留兜底;14/30 切换照旧弃旧窗)
- [x] 注释改写:screen `:759-762` 头注、`:783-791` refreshTrend 注、`:914-915` Select 注(「今日档 = 1 天趋势窗(单点…如实画)」句作废,改图窗下限语义)
- [x] 既有断言翻新:design §4 清单七行逐条落(含 verdict 四档「预期零改动」行——只核对,不碰:verdict 用例 :409-494 稀疏单日 mock,切片后仍取当日行,零改动亲核)
- [x] 新增 AC1/AC3 组件断言:默认渲染 mock 多日 trend → 轴行首末日不同、`trend-total`「近 7 天共 N 条」、aria 含「近 7 天」;rate 区序列随 7 天 mock;全零窗(7 日皆 0)无 y 刻度列 + 「共 0 条 · 峰值 0 条/日」;今日↔7 天切换后 `trend-total` 仍在文档(无骨架屏闪)且 `storeTrend` 同参重发
- 验证(亲跑双绿):`npx vitest run src/screens/dashboard` = 75 passed(1 file,EXIT=0;批1 后 73 + 新增 2 例:全零窗 D8 / D6 同窗切换)+ `npx tsc --noEmit -p tsconfig.app.json` EXIT=0
- **提交点②**

## 批3 全量门禁 + 像素验收(提交点③)

- [x] `cd desktop/ui-src && npx vitest run` 全量(对照批0 基线:仅 dashboard 文件内预期变动,其余文件 passed 数不变)——脚本统一实跑 `npm --prefix desktop/ui-src run test` exit=0(28 files passed;批0 基线 71→批2 后 scoped 75,新增 4 例)
- [x] `npx tsc -b` 零错(repo 门禁口径)——`npm --prefix desktop/ui-src run build`(tsc -b && vite build)exit=0
- [x] 像素验收(AI 亲验,不留给主人;grill Q6 批:**devUrl 为准**——本档纯文案/数据装配,零 CSP/打包敏感面;装机包刷新归 tag 驱动发布流,不绑本档):按仓库既有无头 GUI 冒烟链(Playwright + bridge / devUrl,见 memory「装机包 CSP 与 devUrl 三陷阱」——**必须外链 devUrl,裸 cargo build 是 devUrl 模式不代表装机**):
  - 默认(今日档)截屏:趋势图 ≥2 点有折线、轴行两端日期不同、卡脚「近 7 天」、概览四格仍「今日」口径
  - 切 14 天对比:文案/数据与修复前同形(回归目验)
  - 证据(截屏+度量)存 `evidence/`
  ——像素代理(evidence/harness/pixel_verify.py,devUrl+受控 mock)三场景 27/27 断言过,截图三张落 evidence/;主会话 local-ocr 补验两张关键截图(今日档:近7天共22条·峰值5条/日+轴行 2026-09-30/2026-10-06 两端不同+verdict 今日采集5条;全零窗:无 y 刻度列+近7天共0条)——180d707「无图像输入代理像素主张须补位」教训已偿
- [x] `gitnexus detect-changes -r shishi --scope staged` —— 预期仅 dashboard 屏内符号(纯前端,零协议面)——批1=3 files 3 symbols 0 processes risk low;批2=3 files 2 symbols(DashboardScreen/refreshTrend 屏内)7 affected flows 皆 DashboardScreen 根系(risk=high 系枢纽流程计数,波及面屏内,符合 design §5)
- **提交点③**(批3 全为验证步,零代码改动,无独立提交;验证回执入本档+run-report)

## 复查门(review gate)

- [x] trellis-check 全量:AC1-AC5 逐条 + design §4 矩阵逐行 + 反 AI 审美红线(纯文案不触发,仍核)——独立复查门(工作流「复查门」代理,零实现参与)pass:AC1-AC5 全过;改动面 git diff 亲核限三文件(并行任务 d4bb295 零混淆);scoped 亲跑复验双绿(75 passed+tsc EXIT=0);§4 翻新清单七行逐行对照 diff 全落地、verdict 段零 hunk;D6 不闪机制亲核(骨架屏条件 trendLoading&&trend===null);协议零变更/sparkline 语义零改/反 AI 审美不触发
- [x] 结果回填本档勾选与 review 记录——勾选随收尾提交;复查唯一 low(evidence/harness/__pycache__ 留档)已清

## 回滚

- 任一批红 → revert 对应提交点(批1/批2 分离设计保证纯函数层可独占回退);全档 revert = 回到现状,无数据/协议残留。
