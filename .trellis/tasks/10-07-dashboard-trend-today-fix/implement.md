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

- [ ] `refreshTrend` 两调用点换 `chartWindowDays`(`dashboard-screen.tsx:817` effect、`:947` 刷新钮)
- [ ] 图窗标签 `chartWindowLabel = \`近 ${chartWindowDays(overviewWindow)} 天\``;替换面**仅限趋势卡内**:aria `:1064`、卡脚 `:1078`、成功率空态 `:1110`、成功率 aria `:1122`/`:1124`、成功率摘要 `:1135`。概览四格 note 与 verdict 文案**一字不动**
- [ ] D8 全零刻度守卫:趋势卡 `yLabels={trendPeak === 0 ? undefined : [`${trendPeak}`, `${Math.round(trendPeak / 2)}`, "0"]}`(`TrendChart` 元组类型硬取三位,不可传部分数组;缺省=刻度列不渲染)
- [ ] D6 同窗切换守卫:Select `onValueChange` 仅 `chartWindowDays(next) !== chartWindowDays(overviewWindow)` 时 `setTrend(null)`/`setOutcomes(null)`(effect 同参重拉保留兜底;14/30 切换照旧弃旧窗)
- [ ] 注释改写:screen `:759-762` 头注、`:783-791` refreshTrend 注、`:914-915` Select 注(「今日档 = 1 天趋势窗(单点…如实画)」句作废,改图窗下限语义)
- [ ] 既有断言翻新:design §4 清单七行逐条落(含 verdict 四档「预期零改动」行——只核对,不碰)
- [ ] 新增 AC1/AC3 组件断言:默认渲染 mock 多日 trend → 轴行首末日不同、`trend-total`「近 7 天共 N 条」、aria 含「近 7 天」;rate 区序列随 7 天 mock;全零窗(7 日皆 0)无 y 刻度列 + 「共 0 条 · 峰值 0 条/日」;今日↔7 天切换后 `trend-total` 仍在文档(无骨架屏闪)且 `storeTrend` 同参重发
- 验证:`npx vitest run src/screens/dashboard` + `npx tsc --noEmit -p tsconfig.app.json`
- **提交点②**

## 批3 全量门禁 + 像素验收(提交点③)

- [ ] `cd desktop/ui-src && npx vitest run` 全量(对照批0 基线:仅 dashboard 文件内预期变动,其余文件 passed 数不变)
- [ ] `npx tsc -b` 零错(repo 门禁口径)
- [ ] 像素验收(AI 亲验,不留给主人;grill Q6 批:**devUrl 为准**——本档纯文案/数据装配,零 CSP/打包敏感面;装机包刷新归 tag 驱动发布流,不绑本档):按仓库既有无头 GUI 冒烟链(Playwright + bridge / devUrl,见 memory「装机包 CSP 与 devUrl 三陷阱」——**必须外链 devUrl,裸 cargo build 是 devUrl 模式不代表装机**):
  - 默认(今日档)截屏:趋势图 ≥2 点有折线、轴行两端日期不同、卡脚「近 7 天」、概览四格仍「今日」口径
  - 切 14 天对比:文案/数据与修复前同形(回归目验)
  - 证据(截屏+度量)存 `evidence/`
- [ ] `gitnexus detect-changes -r shishi --scope staged` —— 预期仅 dashboard 屏内符号(纯前端,零协议面)
- **提交点③**

## 复查门(review gate)

- [ ] trellis-check 全量:AC1-AC5 逐条 + design §4 矩阵逐行 + 反 AI 审美红线(纯文案不触发,仍核)
- [ ] 结果回填本档勾选与 review 记录

## 回滚

- 任一批红 → revert 对应提交点(批1/批2 分离设计保证纯函数层可独占回退);全档 revert = 回到现状,无数据/协议残留。
