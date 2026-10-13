# design — 采集日志两级界面(L1 摘要行 → L2 详情)

> 任务档:10-12-logs-two-level-ui · 设计轮 R1 · 依据:prd.md + 库内判例实读
> **修订 R2**(新眼终审四缺口):①§9 断言 6 选择器补 `h` 前缀(夹具全 history:true);②§3.2 第三源增「log_run_id=null = 无据」可用性门(永假在途态);③§9 夹具 exit_code 改 wire 真形(null,历史行恒 None)并把 exit 语义断言迁组件测试;④logs-error 横幅显式挂编排层两级可见。
> 参考面(全部本会话实读,只读):`desktop/ui-src/src/screens/logs/logs-screen.tsx`(922 行,accordion 现状)、`logs/api.ts`(394 行,数据层)、`logs-screen.test.tsx`(677 行)、`desktop/scripts/logs-screen-smoke.py`(218 行,50 轮夹具)、`feed/feed-screen.tsx`(4416 行,v8 三级切级先例:`FeedView` 判别联合 175-178、返回钮 3457-3467、Esc 链 3038-3046、输入框守卫 3024-3031)、`lib/api/types.ts:312-401`(RunState/RunExitStatus/RunRecord/RunEntry/LogLine/LogsTailResult 契约)、`src/myssia/pipeline.py:586-612`(`stats_dict` 键全集)、`src/index.css`(token 表)。

---

## 0. 定位与判例对齐

- **物种锚(铁律)**:Kestra Executions 表列 → Execution 详情页。借结构改语义:L1 = Executions 表行(定宽槽位列对齐 + 状态小芯片,现状已锚,L1 保留其列解剖并升格摘要槽);L2 = Execution 详情页(页面级视图,**非弹窗**——PRD 判例 5:详情弹窗判例只管动作反馈类提示)。L2 头区解剖借 feed v8 2 级工具条(返回钮 + 词面 + 搜索,feed-screen.tsx:3454-3515)。
- **切级机制**:照抄 feed v8 `FeedView` 先例——屏内 `useState` 判别联合驱动互斥分支渲染,**作用域不进路由**(App.tsx 的 `Route path="logs"` 零改动,红线内)。
- **布局纪律**:满高列表容器内滚(现状 `flex h-full min-h-0` 骨架保留);67546cd shrink-0 塌缩律在 L1 行列表与 L2 日志体内滚容器**双双显式落地**(§7)。
- **数据真源边界(不可妥协)**:1 级只吃 `run.status` 行;`logs.tail` 只在 L2 进入时惰性拉取(既有 `ensureTail` 缓存语义原样保留)。1 级**严禁**逐行拉日志——这正是把日志搜索从 1 级迁到 2 级的根因(§2.3)。

---

## 1. 信息架构总览

```
LogsScreen(编排层:数据 hooks + 事件订阅 + view state + Esc 全局链
│          + logs-error 结构化错误横幅挂此层,L1/L2 两级可见)
├─ L1 运行历史(RunListView)                    ← 默认落点,50 轮一行直出
│   ├─ PageHeader(标题/描述/刷新钮)
│   ├─ 过滤条:品类 select · 状态 select · 清除过滤 · 「N / M 轮」计数
│   ├─ 节头 + run 状态分布条(既有,纯视图派生)
│   └─ run 行瀑布(run-list 内滚容器,新→旧)
│       └─ RunSummaryRow:#id · 品类 · 徽标 · 「采集了什么」摘要 · 相对时间 · 耗时 · 状态芯片 ‖ 重跑钮
└─ L2 轮详情(RunDetailView)                    ← 点行进入,页面级替换渲染
    ├─ 元信息头(固定):返回钮 · #id · 品类 · 徽标 · 绝对起止/耗时 · exit_code · 来源号 · 状态芯片 · 重跑 · 复制 · 实时徽标
    ├─ 失败原因区(固定,仅终态非 success):exit_code 语义词 + record/run.error 一句话 + stderr 错误行摘
    └─ 日志体(主滚动区,flex-1):搜索框(迁自 L1)· 摘要行 · 全量日志行(错误行高亮/自动滚底/截断徽标)
```

动线一句话:**L1 点行 → L2;返回钮 / Esc → L1;过滤态与滚动位置在返回后原样;新 running run 不自动跳级,只在 L1 行内以状态芯片呼吸。**

---

## 2. 1 级:行列拆解与「采集了什么」字段派生映射

### 2.1 行槽位表(RunSummaryRow,Kestra Executions 行解剖延续)

行根仍是「按钮区 + 兄弟重跑钮」两节点(现状 button 不可嵌套纪律保留),`role="button"` 语义归按钮区;行高 `min-h-11`(44px,≥40px 哨兵档不变)。槽位左→右:

| # | 槽位 | 视觉(token) | 数据源(仅 run.status 行) | 现状差异 |
|---|------|------------|------------------------|---------|
| 1 | 展开箭头 | — | — | **退役**(accordion 语义终结) |
| 2 | `#id` | `w-9 shrink-0 font-mono text-xs text-muted-foreground` | `run_id`(DOM id/testid 加 `h` 前缀防撞号,`domIdOf` 原样) | 保留 |
| 3 | 品类 | `w-40 shrink-0 truncate text-[13px] font-medium text-foreground`,title 全文 | `record.category` → yaml 基名 → `未知品类`(`runCategory` 原样) | 由 `flex-1` 改**定宽槽**——摘要槽接管弹性位 |
| 4 | 徽标簇 | `Badge variant="outline"` ×N | `dry`→试跑;`history`→上一程(互斥不并存,现状纪律) | 保留 |
| 5 | **「采集了什么」摘要** | `min-w-0 flex-1 truncate text-2xs text-muted-foreground`,title 全文;失败语义片段着色(见 2.2) | `summarizeRun(run)`,派生映射见 2.2 | **新增(本档主升级)** |
| 6 | 相对开始时间 | `w-[68px] shrink-0 text-right tabular-nums`,title 绝对时间 | `started_at`(`formatRelative`,历史行可空 → `—`) | 保留 |
| 7 | 耗时 | `w-[56px] shrink-0 text-right font-mono` | `duration_ms`(`formatDuration`) | 保留 |
| 8 | 状态芯片 | `StatusChip`(24px 高/xs 12px/描边圆图标/状态色淡底) | `status` + `state`(`runBadge` 原样) | 保留 |
| 9 | 重跑钮(兄弟节点) | ghost icon `size-6` | `yaml !== null` 才渲染(`rerunRun` 骑 run.start,零新协议) | 保留 |

### 2.2 摘要合成规则 `summarizeRun` — 字段派生映射(PRD「只能用 run.status 行派生」的逐槽落实)

新纯函数落 `logs/api.ts`(PRD 边界明示「logs/api.ts 可加视图派生」),签名 `summarizeRun(run: LogsRunEntry): RunSummaryModel`,返回 `{ segments: Array<{ text; tone: "muted"|"dead" }>, empty: string | null }`。**每个 segment 的字段来源**(wire 类型 `Record<string, unknown>` 处一律 typeof/Array.isArray 守卫,不信任形状):

| segment | 条件 | wire 字段(真源) | 文案 |
|---------|------|----------------|------|
| 成果段 | `record.stats.items_retained` 为 number | `record.stats.items_retained`(pipeline.py:606 `len(self.items)`) | `保留 N 条` |
| 源段 | `record.stats.sources` 为数组 | `record.stats.sources`(pipeline.py:592,元素含 `failed`/`error`/`skipped`,pipeline.py:399-412) | `M 源`;其中 `s.failed === true || typeof s.error === "string"` 计 K,K>0 追加失败段 `失败 K 源`(tone=dead) |
| 错误段 | 终态非 success 且有 error 原文 | `record.error`(RunRecord,types.ts:326)**优先**;否则 `run.error`(RunEntry 工作线程兜底,types.ts:342;历史行同键) | error 原文一句话(tone=dead,CSS truncate 兜行) |
| 空档兜底 | record 为 null(running 行常态)或 stats 全缺 | — | running:`采集中…`;终态:`无统计记录`(如实,不造假) |

分状态拼装示例:`保留 25 条 · 5 源 · 失败 1 源 · RuntimeError: source fetch failed: timeout`。成功轮只有成果+源段。**边界自查**:以上全部字段都在 `run.status` 应答行内,零 `logs.tail` 依赖;`itemCount`(现 `RunRowModel.itemCount`)即成果段同源,行尾独立「N 条」槽(现状 w-11)并入摘要段后**退役**,避免同屏读两遍。

### 2.3 既有面退役/迁移清单(PRD「工具面不丢」的逐项交待)

| 既有面 | 去向 | 依据 |
|--------|------|------|
| 折叠组头/`aria-expanded`/ChevronDown | **退役**(两级下钻取代内嵌折叠) | PRD Requirements 3 |
| 「N 错误行」槽(64px,组头) | **L1 退役**;错误行计数迁 L2 元信息头 | 其数据源是 `rowsByRun`(logs.tail 行过滤 `isRowError`)——1 级不拉日志,该槽在 L1 无真源;L1 失败信号由摘要错误段+状态芯片承担 |
| 日志搜索框(`log-search-input`) | **迁 L2** 日志体工具位 | 搜索对象是日志行,行只在 L2 在场;留在 L1 = 50 行 × tail 协议风暴,违反数据真源边界。词面改「搜索该轮日志(输入即过滤,命中高亮)」 |
| 状态分布条 + 图例 | **L1 保留** | 纯视图派生(run.status 聚档),现状零改 |
| 品类/状态过滤 + 清除 + 计数 | **L1 保留** | state 挂编排层,切级不重置(§4.2) |
| 结构化错误横幅(`logs-error`) | **挂编排层,L1/L2 两级可见** | 现状横幅在屏根全态可见(logs-screen.tsx:797-808);按分支拆分后若误钉 L1,则 L2 在途的 run.status 结构化错误静默不可见——渲染位置在 L1/L2 互斥分支**之上**(R2 修正) |
| 重跑钮 + starting/triggered/error 反馈 | **L1/L2 双可达**(L2 挂元信息头) | PRD 交互动线「重跑钮 1/2 级都可达」;triggered 的 title 文案改「新 run #N 已启动,运行历史列表已刷新」(不再有「展开跟随」) |
| 「缓冲截断」「实时跟踪中/未跟踪」徽标、复制日志、自动滚底、无对齐号降级、加载失败面 | **L2 保留**(§3.3) | PRD 交互动线 3 |
| 初次进屏自动展开最新 run(现状 refreshRuns follow 策略) | **退役** | accordion 时代的跟随遗产;两级 IA 下「自动展开」=「进屏自动跳 L2」,违反 PRD 默认不自动跳级(§4.3)。`knownRowKeysRef`/follow 分支整体删除 |

---

## 3. 2 级:三分区

L2 根 `flex h-full min-h-0 flex-col`(与 L1 互斥分支替换渲染);三区自上而下,头两区固定、日志体独占滚动——feed 详情整屏化判例(头/动作簇常驻 + 中段主滚动区)同门。

### 3.1 元信息头(固定区)

- **返回钮**(槽位第一):`Button variant="outline" size="sm"`,ChevronLeft + 「运行历史」,`title="返回运行历史(Esc 同门)"`——feed 返回钮(feed-screen.tsx:3457-3467)同款解剖,词面随本屏物种。
- **身份簇**:`#{run_id}` mono · 品类 · 试跑/上一程徽标 · 状态芯片。
- **事实簇**(text-2xs muted,`·` 分隔):开始 `YYYY-MM-DD HH:mm`(新 `formatAbsolute`,title 挂相对时间对偶)· 耗时 mono · `exit={n}` mono(可空 → `exit=—`)· `logs.tail run_id={logRunId ?? "—"}`(来源号如实报,历史行=会话对齐号,旧行=未对齐;现状 `run-log-meta` 的来源标记升格到此)· 日志行数/错误行数(tail 到位后)。
- **动作簇**(右缘):实时跟踪徽标(running 时)· 复制日志 link 钮(现状 copyLogs 原样,不受搜索过滤影响)· 重跑钮(yaml 在场)。

### 3.2 失败原因区(固定区,`FailurePanel`)

**渲染门槛(PRD AC2「成功轮不显示」)**:`state === "done" && status !== "success"`(即 failed / partial / config_error / cancelled 四终态);success 与 running 一行都不渲染。

**合成规则 `synthesizeFailure(run, rows | undefined) → FailureModel`**(纯函数落 api.ts,三证据源 + 如实判空):

1. **exit_code 证据**:`run.exit_code`(number | null)。展示 `exit={n}` mono 芯片 + 契约语义词(types.ts:314 / cli.py:212-215 `_EXIT_BY_STATUS`:0 正常退出 / 1 配置错误 / 2 运行失败 / 3 部分成功)。null → `exit=—`,不编语义;**历史行 wire 恒 null**(entry.py `_history_run_rows` 硬编码 `"exit_code": None`;0/1/2/3 只适用注册表行)——`exit=—` 是历史行的常态真形,不是降级。
2. **error 字段证据**:`record.error ?? run.error ?? null`,原文整句展示(wrap,不截断语义只 truncate 兜底+title 全文)。两键都空 = 此源无据,该段不渲染。
3. **stderr 错误行证据**:`rows?.filter(isRowError)`(双信号判定函数**原样复用**,stream+关键词);取**前 5 条**,等宽 dead 色单行 truncate(title 全文),尾注「另 N 条错误行在下方日志体(高亮)」。
   **第三源可用性门(R2 修正)**:`run.logRunId === null`(旧行未记会话号)→ 此源**直接判无据**——`ensureTail` 对 null 号早退不拉(logs-screen.tsx:505-506)、历史行收不到事件流(订阅按 `run:${runId}` 归组,logs-screen.tsx:585),rows 恒 undefined,「在途」是永假态,若挂「日志拉取中…」将与紧邻日志体的如实降级文案「无可回看的日志」(logs-screen.tsx:453-458)自相矛盾;只有 `logRunId !== null && rows === undefined`(tail 真在途)才挂「日志拉取中…」。`rows` 到位且零命中 → 无据不渲染。`FailureModel` 增 `logAligned: boolean` 字段承载此门(= `run.logRunId !== null`)。

**无据可查(PRD「如实无据就说无据」)**:三源全空且(rows 已到位**或** `logAligned=false`)→ 面板只保留状态芯片语义 + 一句 `data-testid` 挂点的如实文案:「暂无结构化失败记录(该轮未落 error 字段,日志缓冲中亦无错误行)」——不编造、不静默。

**布局帽**:面板 `max-h-40 shrink-0 overflow-y-auto`,行子项显式 `shrink-0`(§7 塌缩律);面板常驻固定不随日志体滚走——「为什么失败」是 L2 的答案位,不埋进 4000 行里。

### 3.3 日志体(主滚动区)

现状 `RunLogBody` 升格为页面主体,逐项交待:

- **内滚帽解除**:现状 `max-h-[26rem]`(accordion 时代的卡内帽)→ `flex-1 min-h-0`(页面级满高,feed 整屏化「去内滚帽、滚动交中段」同律)。
- **搜索**(迁自 L1):输入即过滤 `rowMatchesQuery` + `splitTextOnQuery` 命中 `<mark>` 高亮 + 「命中 X / Y 行」计数 + 无命中文案——三件套纯函数与组件**零语义改动**,只换挂载点;输入框 Esc 清词走**框内守卫**(feed L2 搜索同门,feed-screen.tsx:3485-3491),全局 Esc 链见 §4.1。
- **自动滚底**:行集变化贴底 effect 原样(running 续播时无条件贴底,Crawlab 同款)。
- **错误行高亮**:`isRowError` → `bg-dead/10 text-dead`(P2 对比实算档原样)、`isRowWarn` 弱警示原样。
- **降级面全保留**:tail 加载失败(结构化错误码)· 无对齐号(`log_run_id=null` 如实文案,零请求)· 环形缓冲截断徽标 · 空行集文案。
- **行子项 `shrink-0` 显式**(§7)。

---

## 4. 动线

### 4.1 进入与返回

```
type LogsView = { level: 1 } | { level: 2; rowKey: string }
```
- **进**:`RunSummaryRow` 按钮区 onClick → `setView({ level: 2, rowKey })` + `ensureTail(run)`(惰性拉取;`loadedRunsRef` 缓存驻屏,返回再进不重拉——现状缓存语义零改)。进 L2 后事件流照旧按 run_id 归组缓冲/续播(订阅挂屏级,不随切级变)。
- **返回**:`backLevel = () => setView({ level: 1 })`(feed `backLevel` 同名同构,feed-screen.tsx:2776-2779;本屏只有两级,无 3→2 重派生分支)。
- **Esc 全局链**:window keydown,`view.level === 2` 时 `backLevel()`;守卫两道随迁 feed 先例——①焦点在 INPUT/TEXTAREA/SELECT/contentEditable 不抢(输入框 Esc 归清词自身语义);②`event.metaKey/ctrlKey/altKey/shiftKey` 修饰键不抢。本屏无菜单/浮层,feed 的 `[role="menu"]` 第三道守卫不需要(如实注明差异: Select 下拉开着时 Esc 归 Radix 自身,先关下拉不切级——正好落在守卫①)。1 级 Esc = no-op。

### 4.2 过滤态与列表位置保持(AC3 落点)

- **过滤态**:categoryFilter/statusFilter/query 全部挂编排层 `LogsScreen` state,L1/L2 分支只消费不持有 → 切级天然不重置(React state 生命周期 = 屏生命周期)。组件测试断言:设过滤 → 进 L2 → 返回 → 计数文案与行集仍是被过滤态。
- **列表滚动位置**:L1 内滚容器分支卸载后 scrollTop 归零——feed v8 三级**没有**做恢复(其验收无此条),本档 AC3 明示「列表位置保持」,故**加两行机制**(对 feed 先例的唯一偏离,特此留档):`openRun` 时把 `run-list` 容器 `scrollTop` 存 `l1ScrollTopRef`;返回 L1 的 effect 里回写。无头冒烟断言(scrollTop 写 400 → 进 → 返回 → ≥300,§9);jsdom 无真实布局不测此条(PRD 判例 6)。

### 4.3 跟随策略定稿(默认不自动跳级,**接受 PRD 默认,不翻案**)

理由四条:
1. **阅读连续性**:L2 是逐轮诊断视图,新 run 把主人从正在读的失败详情里拽走 = 打断诊断;feed 整屏化判例的主人语义是「一眼看出所有数据」,拽走与之相反。
2. **信息不丢**:新 running run 的活性在 L1 有双承载体——该行状态芯片(running 档)+ 状态分布条(completed 事件已触发 `refreshRuns`,现状通路);要看细节,主人点行即达,一次点击的成本低于被拽走后的找回成本。
3. **返回链心理模型**:自动跳级会破坏「Esc 回到刚才的列表」的稳定预期(返回后又被顶走);Kestra 物种锚亦无此行为(Execution 详情页不会被新 Execution 顶掉)。
4. **run 级跟随仍然在**:若主人正在 L2 看的就是那个 running run,日志体自动滚底续播照旧——「跟随」发生在日志体,不发生在层级。

**退役件**:现状「初次进屏自动展开最新 run」+「新 running run 自动展开」(refreshRuns follow 分支、`knownRowKeysRef`)整体删除——初见即 L1 素列表,冒烟「首组自动展开」断言随 IA 重写为「默认无 run-detail(不自动跳级)」(§9)。

---

## 5. 组件/文件拆分计划(全部在允许改动区内)

| 文件 | 动作 | 内容 |
|------|------|------|
| `screens/logs/logs-screen.tsx` | 重写(缩) | 编排层:`LogsView` state · runs/rowsByRun/truncatedByRun/loadErrors 数据 hooks(现状逻辑原样)· 事件订阅(原样)· Esc 全局链 · 过滤 state · 滚动位置 ref · 互斥渲染 L1/L2 |
| `screens/logs/run-list-view.tsx` | 新增 | L1 页:PageHeader/过滤条/分布条/`run-list` 内滚容器 + `RunSummaryRow`(槽位表 §2.1) |
| `screens/logs/run-detail-view.tsx` | 新增 | L2 页:元信息头 + 日志体(`LogRowView`/`HighlightedText`/copyLogs/自动滚底/搜索三件套随迁) |
| `screens/logs/failure-panel.tsx` | 新增 | 失败原因区渲染器(消费 `FailureModel`) |
| `screens/logs/run-status-chip.tsx` | 新增 | `runBadge`/`STATUS_CHIP_TONE`/`StatusChip`/`STATUS_FILTER_OPTIONS`(L1/L2 共用,现状代码平移) |
| `screens/logs/api.ts` | 增量 | `summarizeRun`/`synthesizeFailure` 纯函数 + `RunSummaryModel`/`FailureModel` 类型 + `formatRelative`/`formatAbsolute` 平移收口(纯函数可直测;wire 类型与 `@/lib/api` client **零改动**,PRD 边界) |
| `screens/logs/logs-screen.test.tsx` | 重写 | §8 |
| `desktop/scripts/logs-screen-smoke.py` | 重写 | §9 |

不新增依赖、不改 `App.tsx`/路由/全局 CSS/`@/lib/api`。

---

## 6. testid 约定(新 IA 关键锚点;`{domId}` = `h` 前缀规则原样)

**L1**
| testid | 挂点 | 沿革 |
|--------|------|------|
| `run-list` | L1 内滚容器 | 新(取代 `run-waterfall`,IA 语义改名,冒烟同步) |
| `run-row-{domId}` | 行按钮区(点击进 L2 的语义 owner) | 新(取代 `run-group-header-*`,去 aria-expanded) |
| `run-summary-{domId}` | 摘要槽 | 新(AC1 断言锚) |
| `run-status-chip-{domId}` / `run-history-badge-{domId}` / `run-rerun-{domId}` / `run-rerun-ok-{domId}` / `run-rerun-err-{domId}` | 原样 | 沿用 |
| `logs-filter-bar` / `filter-category` / `filter-status` / `logs-filter-count` / `run-status-distribution` | 原样 | 沿用(L1) |
| `logs-error` | 结构化错误横幅(**挂编排层,L1/L2 两级可见**——渲染在互斥分支之上,切级不使其静默) | 沿用 |

**L2**
| testid | 挂点 |
|--------|------|
| `run-detail` | L2 页根(冒烟「是否在 2 级」判据) |
| `run-back` | 返回钮(对齐 `feed-back-to-types` 命名式) |
| `run-detail-meta-{domId}` | 元信息头事实簇 |
| `run-failure-{domId}` | 失败原因区根;`run-failure-none-{domId}` = 无据文案;错误行摘条目 `run-failure-line-{domId}-{n}` |
| `run-log-{domId}` / `run-log-hits-{domId}` / `run-log-copy-{domId}` / `log-row` / `log-system-row` / `log-search-hit` | 日志体(全部沿用,词面/语义零改) |
| `log-search-input` | 搜索框(沿用 id,**挂载点迁 L2**) |

---

## 7. 视觉规范(现有 token 复用,不改全局 CSS)

- **token 清单(全部已在 `src/index.css` 实读核验)**:`text-2xs`(11px/16px/500)· `gap-grid`(12px)· `min-h-11` 行高档 · `StatusChip` 四态+unknown(`border-ok|warning|destructive|unknown/30 bg-*/15` 淡底实算档)· Kestra 紫 `primary`/`text-link` · dead 色族(`text-dead`/`bg-dead/10`,P2 对比档)· `--duration-fast`(120ms)hover 过渡 · `animate-fade-in` 行入场。
- **新增视觉面只用既有 token 组合**:L2 工具条 = feed 2 级工具条解剖(`flex flex-wrap items-center gap-2 border-b px-5 py-2.5`);失败面板底 `bg-muted/20` + `border-border/60` 圆角条(feed 沉淀面板同族);摘要槽失败片段 `text-[#ff6b70]`(组头 hover 底对比实算档,现状注释在案)。
- **塌缩律显式落地(67546cd 不回归,判例 3)**:两个内滚容器——L1 `run-list` 与 L2 日志体——其**直接 flex 子项一律显式 `shrink-0`**(行/日志行/降级文案行;子项无 overflow-hidden,双保险)。冒烟双哨兵:两容器各自 `scrollHeight > clientHeight` 且行高 ≥40px(§9)。
- L2 日志体宽度:满宽不设 max-w(终端块惯例,现状 accordion 体同款);L1 行满宽。

---

## 8. 组件测试改写要点(`logs-screen.test.tsx`,jsdom,管渲染语义/交互/过滤搜索)

夹具层不动(`run2Running`/`run1Success`/`histRun5`/tail 五行/事件夹具全复用),断言面随 IA 重写:

1. **L1 摘要行派生**(新):success 行摘要含「保留 5 条」+ 源段;failed 行(造 record.error)摘要含 error 原文且片段 dead 色 class;record=null 的 running 行摘要 =「采集中…」;record/stats 全缺终态行 =「无统计记录」;`run-row-*` 无 aria-expanded(accordion 退役哨兵)。
2. **切级动线**(新):点 `run-row-2` → `run-detail` 在场 + tail 以 run_id=2 拉取(一次);点 `run-back` → 回 L1 且 `run-detail` 卸载;`fireEvent.keyDown(window, {key:"Escape"})` 同效;再进同 run **不重拉**(缓存,总调用数不变)。
3. **默认不自动跳级**(新):render 后 `run-detail` 不在场;refreshRuns 注入新 running run 后仍不在场(§4.3 哨兵)。
4. **过滤态穿越保持**(新,AC3 的 jsdom 半边):品类过滤 → 计数「1 / 2 轮」→ 进 L2 → 返回 → 计数与行集仍被过滤。
5. **失败原因区**(新):failed + record.error + stderr ERROR 行 → 面板同时呈现 exit 语义/error 原文/错误行摘;success 行 `run-failure` 不在场;三源全空 → `run-failure-none` 如实文案;tail 在途(logRunId 在场)错误行摘段挂「日志拉取中」;**旧行无对齐号(log_run_id=null)的 failed 历史行 → 面板不出现「日志拉取中」,第三源走无据分支**(R2 修正——logs-screen.tsx:505-506 早退/:585 事件不达历史行,永假在途态在此象限拦下)。
6. **元信息头**(新):绝对起止/耗时/`exit` mono+语义词/`logs.tail run_id=9`(历史行对齐号)/行数-错误行数。exit 语义映射断言**用注册表行夹具**(histRun5 是 wire 真形 `exit_code: null` → 断言 `exit=—`;另造 failed 注册表行 `exit_code: 2` → `exit=2 · 运行失败`——0/1/2/3 映射只适用注册表行,历史行恒 None,R2 修正)。
7. **存量语义平移改挂点**:流式续播(缓冲-展开合并 → 改为「进 L2 时合并」,emit 顺序断言同构)/ 错误行 dead 高亮与 INFO 不染 / completed 刷新列表 / 结构化错误横幅 / 空态 / 试跑徽标 / 重跑(触发参数面+反馈+失败如实;triggered 文案去「展开跟随」)/ 日志搜索(过滤+高亮+计数+无命中;输入框现在 L2)/ 上一程历史行全家族(徽标/序/log_run_id 拉取/无号降级/撞号防混)/ 空态零回归。
8. **api.ts 纯函数新 describe**:`summarizeRun`(分状态段拼装 + wire 形状守卫:stats.sources 非数组/元素缺键不崩)、`synthesizeFailure`(三源有无的四象限)、`formatAbsolute`。

---

## 9. 冒烟脚本改写要点(`desktop/scripts/logs-screen-smoke.py`,保留「布局哨兵」性质)

- **骨架不动**:静态服务 `desktop/ui` 产物 · 无头 Chromium 1685×1057 · `add_init_script` IPC 注入 · HashRouter `#/logs` · 截图落 /tmp · 退出码语义。
- **夹具修正(R2 终审修正,如实向 wire 真形对齐)**:①历史行 `exit_code` **保持 null**——entry.py `_history_run_rows` 的 wire 真形恒 `"exit_code": None`,0/1/2/3 CLI 映射(cli.py:212-215)只适用注册表行;现状夹具的 1/0 本就是 wire 上不存在的形状(屏内 `RunHistoryEntry` 类型亦建模 `exit_code: null`,api.ts:47),**不得**改成 2/3/0 假装「对齐契约」;exit 语义词断言随夹具修正**移出冒烟、落组件测试**(注册表行夹具,§8-6)。②全部夹具行 `record.stats` 补 `sources` 数组(pipeline.py:592 形状:`source/failed/error`;success 行全健康,partial/failed 行内各造一例 `failed:true` 成员——stats 来自 `_run_record_dict` 落库 record,wire 真,喂摘要源段/失败段)。③failed 行(i=45..49,run_id 855..851)`record.error` 置真句 + `logs.tail` 对这些 run_id 回一行 stderr `ERROR …`(喂失败合成第二/三源;夹具行 `log_run_id` 在场,第三源可达)。
- **断言面(编号即脚本顺序)**:
  1. L1 直出:`run-list` 在场;`[data-testid^="run-row-"]` 计数 == 50;
  2. **行高哨兵**:行高 min ≥ 40px(44px 档,塌缩回归一票否决);
  3. **可滚哨兵**:`run-list` scrollHeight > clientHeight + 100;
  4. **不自动跳级哨兵**:`run-detail` 计数 == 0;`run-summary-h900` 文本非空且含「保留」与「源」(摘要可读,AC1);
  5. 截图 L1 → `/tmp/myssia-logs-screen-smoke-l1.png`(AC4 双图之一);
  6. **进 2 级**:滚动容器置 scrollTop=400(为断言 9 铺垫)→ 点 `run-row-h855`(failed 历史行——夹具全 `history:true`,domIdOf 规则带 `h` 前缀,与断言 4 的 `run-summary-h900` 同律;R2 修正,裸号 `run-row-855` 必空匹配)→ `run-detail` 在场;`run-failure-h855` 在场且文本含 record.error 句与 `exit=—`(历史行 wire 真形)、**不**含「无据」文案(此轮有据);日志行在场且 ERROR 行 `data-error="true"`;截图 L2 → `/tmp/myssia-logs-screen-smoke-l2.png`(AC4 双图之二);
  7. **返回钮**:点 `run-back` → `run-detail` 卸载;
  8. **过滤态保持**:开 `filter-category` 选一品类 → 计数文本读数 → 进 L2 → `Escape` 回 → 计数文本同读数(Radix select 无头可点,feed/源管理既有用例同法);
  9. **滚动位置保持**:返回后 `run-list` scrollTop ≥ 300(§4.2 机制的无头验证);
  10. 失败清单非空 → 退出码 1,全绿 → 0(原样)。

---

## 10. AC 逐条落点

| AC | 落点 |
|----|------|
| **AC1** 1 级 50 行直出、摘要可读、accordion 退役、工具面不丢 | §2.1 槽位表(行直出定宽对齐)· §2.2 派生映射(摘要只用 run.status 行)· §2.3 退役/迁移清单(accordion/错误行槽/搜索迁移/分布条保留)· 冒烟断言 1-4 · 组件测试 1 |
| **AC2** 2 级详情:日志体(自动滚底/错误行高亮/复制)+ 失败原因区;成功轮无失败区 | §3.1 元信息头 · §3.2 合成规则三源 + 无据如实文案 + 成功轮门槛 · §3.3 日志体四件保留 · 组件测试 5/6 · 冒烟断言 6 |
| **AC3** 返回钮 + Esc 回 1 级,过滤态与列表位置保持 | §4.1 Esc 链与守卫(feed 先例随迁)· §4.2 过滤 state 挂编排层 + scrollTop 捕存回写(对 feed 先例唯一偏离,已留档理由)· 组件测试 2/4 · 冒烟断言 7-9 |
| **AC4** 门禁三件绿 + 双截图 | `npm --prefix desktop/ui-src run build` / `npm --prefix desktop/ui-src run test`(基线 35 文件 744 绿,共享树)· `.venv/bin/python desktop/scripts/logs-screen-smoke.py`(重写后 §9)· `/tmp/myssia-logs-screen-smoke-l1.png` + `-l2.png`。(本设计轮未跑门禁——实现轮在 workflow 内 world.run 执行,此处只认领落点。) |
| AC5 装机换装 | 主会话 workflow 后,非本 design 范围(PRD 已划界) |

---

## 11. 红线自查(设计承诺)

- 并行在途文件(`App.tsx`/`sidebar.tsx`/`feed/**`/`browser-module.tsx`/`settings-screen.tsx`/`tg-account/**`)**零修改**;feed 只作判例引用。改动面 = `screens/logs/**` + `desktop/scripts/logs-screen-smoke.py`,与 PRD 边界逐字对齐。
- 零新协议、零 `@/lib/api` 改动;视图派生按 PRD 授权落 `logs/api.ts` 纯函数。
- 不造假数据:摘要/失败区每个字段的 wire 真源在 §2.2/§3.2 表格中可追溯;无据即「无统计记录」「暂无结构化失败记录」如实文案。
- 不 git commit;实现改动留工作树主会话收口。
