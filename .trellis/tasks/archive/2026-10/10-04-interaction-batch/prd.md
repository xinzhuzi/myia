# 对标交互小批:j/k 导航+命令面板+卡片时间范围+右键菜单+显示选项+侧栏折叠

## Goal

10-04-fe-gap-census 缺口一层六件一次做掉:①feed j/k 键盘导航(focus 环);②⌘K 命令面板本体(导航+全局动作);③仪表盘卡片级时间范围;④feed 右键上下文菜单(复制链接/标已读/沉淀入口);⑤列表显示选项下拉(未读优先/分组切换);⑥侧栏折叠(含最小快捷键底座)。对标 Linear/Vercel 拆解表,主人 2026-10-04 批「按照你的建议做完剩下的任务」

## Requirements

- TBD

## Acceptance Criteria

- [ ] TBD

## Notes

- Keep `prd.md` focused on requirements, constraints, and acceptance criteria.
- Lightweight tasks can remain PRD-only.
- For complex tasks, add `design.md` for technical design and `implement.md` for execution planning before `task.py start`.

## implement(2026-10-04 A-分诊:四组互斥白名单)

分诊依据 = gap-matrix.md 缺口一层 #1/#2/#3/#4/#5/#8;现状为本轮实读(feed-screen.tsx、feed/api.ts、top-bar.tsx、dashboard-screen.tsx、dashboard/api.ts、layout/sidebar.tsx、layout/app-layout.tsx、App.tsx、global-run.tsx、ui/dropdown-menu.tsx、ui/dialog.tsx、package.json、ui-src 全树 find)。基线:`cd desktop/ui-src && npm test` = **19 文件 295 测试全绿**(2026-10-04 实跑)。

事实底座(分诊时实况,逐条有出处):

- `components/ui/` **无 ContextMenu、无 Command 基件**(find 实核,现有=badge/button/card/dialog/dropdown-menu/input/scroll-area/select/separator/skeleton/switch/table/tabs/tooltip);自建范式 = 零新依赖(`ui/dropdown-menu.tsx:8-9`「无 @radix-ui/react-dropdown-menu 依赖(任务红线不装包)」;package.json 亦无 cmdk/react-hotkeys-hook)
- `top-bar.tsx:130-144` CommandSlot 是 aria-hidden 占位(注释明示「命令面板属后续任务」)
- `feed-screen.tsx:829-846` 已有 U 键本地 keydown effect,守卫 = INPUT/TEXTAREA/contentEditable 跳过 + meta/ctrl/alt 修饰键跳过——j/k 扩此惯例,不引外部 hook
- feed 分组固定时间四桶(`feed/api.ts:337-356` groupFeedItems),无分组切换、无未读优先排序;G12 沉淀面板在 FeedCard 内(`feed-screen.tsx:573-658`,openPin 在 `:205`)
- dashboard 趋势卡已有窗口 Select(`dashboard-screen.tsx:497-511`);概览条/源健康卡无范围;概览「今日采集」格 = trend 补零窗口右端(`dashboard/api.ts:477-479`),runs 面 = runs.list limit 20(`dashboard/api.ts:76`)
- 侧栏 w-56 固定宽(`sidebar.tsx:109`),NAV_GROUPS 模块私有未导出(`sidebar.tsx:30`)
- 快捷键现状:仅 feed 屏 U 键一处本地监听,无全局 hook;⌘K 文案已在 top-bar(`top-bar.tsx:23-24`)

### A-shell(最小快捷键底座 + 侧栏折叠)——缺口 #2

白名单(4 文件,2 改 2 新):

- **新** `src/hooks/use-hotkeys.ts` + `src/hooks/use-hotkeys.test.tsx`:最小快捷键 hook——声明式绑 window keydown,输入框/可编辑目标跳过、修饰键判定(守卫逻辑与 feed U 键同源);单键与 ⌘/Ctrl 组合两形态;**不装 react-hotkeys-hook**(红线不装包)
- `src/components/layout/sidebar.tsx`:collapsed 受控 prop → 折叠态 w-14 图标态(NavRow 隐文字留图标+title 悬浮、组标题隐、品牌区只留 MyiaMark、底部状态区精简);顺手 `export NAV_GROUPS`(一行,供后续复用)
- `src/components/layout/app-layout.tsx`:collapsed state + localStorage 持久化(键 `myia.sidebar.collapsed.v1`,损坏即弃 = loadFeedStates 同纪律;不做拖拽调宽,teardown 只要折叠)+ `[` 键切换(useHotkeys 首个消费者)
- **新** `src/components/layout/app-layout.test.tsx`:[ 键切换 / 折叠态持久往返 / 损坏键弃用

要点:不碰 top-bar.tsx(归 A-cmd);⌘K **不走**本 hook(A-cmd 面板自含监听,免跨批文件依赖)。

### A-cmd(⌘K 命令面板本体 + 两个新基件)——缺口 #3

白名单(5 文件,3 新 2 改):

- **新** `src/components/ui/command.tsx`:命令面板基件,自建零依赖(dialog.tsx 范式 = portal+遮罩+焦点圈禁+Esc 还焦+120ms 离场;增输入过滤/↑↓巡游/Enter 执行;shadcn Command API 子集)
- **新** `src/components/ui/context-menu.tsx`:右键菜单基件,自建零依赖(dropdown-menu.tsx 范式;定位锚 pointer 坐标;↑↓/Esc/120ms 离场)——**A-feed 右键件的依赖,须先行落**
- **新** `src/components/layout/command-palette.tsx` + `command-palette.test.tsx`:⌘K 本体。命令面 = 导航七屏(App.tsx 路由表;命令清单**自含**约 8 行数据,不复用 sidebar 的 NAV_GROUPS——避免与 A-shell 的 sidebar.tsx 跨批耦合,重复属有意取舍)+ 全局动作:跑一次(health→plugin 定位→run.start,复刻 `global-run.tsx:29-52` 口径;GlobalRun 组件本身不动)/刷新(window.location.reload,自含,不逐屏发刷新事件)/切换品类(TopBar 既有 options 清单 + onCategoryChange 透传即可)。⌘K 开/关监听在面板组件内自含
- `src/components/layout/top-bar.tsx` + `top-bar.test.tsx`:CommandSlot 占位换真触发器(button + aria-haspopup,挂载 palette;品类 options 下传)

要点:不碰 app-layout.tsx / global-run.tsx / App.tsx。

### A-feed(j/k 导航 + 显示选项下拉 + 右键上下文菜单)——缺口 #1/#5/#8

白名单(3 文件,全改既有):

- `src/screens/feed/api.ts`:新增纯函数——sortUnreadFirst(未读优先,稳定保序)、groupFeedItemsByCategory(按品类分组,品类色同 categoryColor 源)、显示选项 load/save(键 `myia.feed.display.v1`,loadFeedStates 同纪律)
- `src/screens/feed/feed-screen.tsx`:① j/k 扩既有 U 键 effect(`:829-846` 同守卫;currentKey 上/下移 + scrollIntoView({block:"nearest"}));② 过滤区右侧显示选项下拉(**复用既有 ui/dropdown-menu.tsx**,不新建基件):未读优先 toggle + 分组切换 = 时间四桶(默认)/按品类/不分组;③ FeedCard 包 ui/context-menu.tsx(A-cmd 基件):复制链接(navigator.clipboard,仅 isOpenableUrl)/标已读未读(既有 toggle)/沉淀为关键词(直调卡内既有 openPin `:205`,G12 面板本尊零改)
- `src/screens/feed/feed-screen.test.tsx`:j/k 巡游含边界、未读优先+分组切换、右键菜单三动作;新纯函数测试并入本文件

要点:j/k 用 feed 本地 keydown 惯例(**不 import** A-shell 的 use-hotkeys,免跨批依赖,守卫同源);右键菜单件依赖 A-cmd 的 context-menu.tsx 先落。

### A-dash(仪表盘卡片级时间范围——落位判断)——缺口 #4

白名单(3 文件,全改既有):

- `src/screens/dashboard/api.ts`:buildOverviewStats 扩窗口参数(今日→窗口):窗口内采集 = 既有 fillDailyCounts 窗口求和(零新协议);推送 = runs 窗口内过滤;新纯函数伴测试
- `src/screens/dashboard/dashboard-screen.tsx`:概览条加独立窗口 Select(今日(UTC)/7/14/30 天,与趋势卡同款形态;独立 state + 独立 fetchTrendWindow,allSettled 降级,不与趋势卡共用窗口)。**落位判断(以 Vercel 拆解 #2 为准,不过度)**:
  1. 概览条 = **可切**,但只两格随窗:「今日采集」→「近 N 天采集」(trend 窗口求和)、「推送成功」→窗口内过滤(note 如实注记 runs.list 20 条上限口径,`dashboard/api.ts:76`);「活跃源」「告警」= doctor 点快照,**不随窗**(快照无时间序列,硬切 = 伪窗口,只注记口径)
  2. 源健康度卡 = **不加范围切换**——doctor 是点快照(state/reason/latest 单值),无逐日序列可切,卡面已有相对时间锚;给快照卡加 range 属过度,明确不做
  3. 趋势卡已有 Select(`dashboard-screen.tsx:497`)不动
- `src/screens/dashboard/dashboard-screen.test.tsx`:窗口切换重查 / 两格随窗两格快照 / 降级注记

要点:零协议改动;不动 sparkline / feedback-stats-card。

### 批次序与互斥核验

- 四组文件两两无交集;共享文件只读消费无人改:App.tsx、lib/api/*、ui/dropdown-menu.tsx、ui/dialog.tsx、global-run.tsx
- 唯一跨批依赖:A-feed 右键菜单 ← A-cmd 的 ui/context-menu.tsx。建议序:**A-shell 与 A-dash 可并行;A-cmd 先于 A-feed**(若 A-feed 先行,j/k 与显示选项先落,右键件待 A-cmd 后补)
- 各批收口检查:`cd desktop/ui-src && npm test`(基线 295 绿)+ `npx tsc -b`(与 build script 同门类型检查)
