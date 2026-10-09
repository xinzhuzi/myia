# 情报流 v7 设计稿 · 双栏监控台(右群组列表 / 左数据主区)

> 主人定调(2026-10-10 凌晨):**右侧 = 群组/渠道列表,左侧 = 选中群组的数据**;镜像 Telegram 桌面但**群组列表在右是主人明确指定,勿镜像回常规侧**。v6 渠道详情整页单列 + 大片空白(主人截图点名)不对,双栏收编全部导航面。
>
> 事实底座(2026-10-10 实查,写定不再摸底):
> - 应用壳 = 左侧全局 Sidebar(展开 224px / 折叠 56px,`sidebar.tsx:87-90`)+ 主内容区(`app-layout.tsx:24-34`);**PageHeader 已死**(`page-header.tsx:1-4` 返回 null,feed-screen.tsx:2320 的调用是死代码)——v7 顺删。
> - 窗口默认 1920×1080,**无 minWidth/minHeight 约束**(`desktop/src-tauri/tauri.conf.json:14-22`)。
> - 选中驱动查询的既有通路:`fetchFeedPage` 带 `source` 精确等值参数(`api.ts:23-35, 50-69`),v6 渠道详情已在用(`feed-screen.tsx:1613-1655`)。
> - 渠道全集聚合 `feedChannelCards`(`api.ts:801-845`,health sources ∪ 条目 source 去重)、搜索过滤 `filterChannelsByQuery`(`api.ts:863-875`,类型别名 `api.ts:851-855`)、展示词 `channelDisplayName`(`api.ts:662-666`)、类型三档 `channelCardKindOf`(`api.ts:768-774`)**全部原样复用,api.ts 零改**。
> - 键盘 effect(j-k-U-Enter + Mod+F + 守卫)`feed-screen.tsx:2228-2311`;TG 监控台(状态 effect `1951-1965`、扫码 `2169-2182`、预览推导 `2190-2198`、开窗 `2199-2217`、渲染 `2719-2804`);详情弹窗 `1196-1364`。
> - 能力门:READ_STATE_PROTOCOL=10(`api.ts:313`)/ COUNT_PROTOCOL=13(`api.ts:323`),探测 `feed-screen.tsx:1583-1603`。
> - 待吸收 P2:**R1** 渠道详情计数 tooltip 词面残留当日窗(「已加载 N 条为当日窗视图首页」,`feed-screen.tsx:2409`);**R2** TG 监控台首拉在途时「状态未知」卡闪现(「状态未知」空态以 `tgWebline === null` 为门,首拉在途同显,`feed-screen.tsx:2888-2904`)。
> - 测试规模:`feed-screen.test.tsx` 137 用例,渠道卡/墙选择器引用 `grep -oE "feed-channel[a-z-]*"` = 109 处 + `feed-back-to-wall` 9 处(复审轮实测口径);冒烟资产 `desktop/scripts/feed-card-smoke.py`(引 `feed-channel-wall` 点卡动线)、`ui-src/e2e/feed_channels_smoke.py`(10-06 旧三级 IA 的 feed-l1/l2/l3,早已过期,随本批重写或退役)。

## 0. 定调与总骨架

双栏监控台 = **右栏渠道列表(导航本体,常驻)+ 左栏数据主区(时间线/引导,常驻)**。没有「落地页 → 详情页」的页面切换,只有「选中 → 载入数据」:点右栏行,左栏换数据,右栏原地不动。瀑布流落地页、渠道行导航页、详情页返回动线全部收编进这一屏。

```
┌─App──────────────────────────────────────────────────────────────────────┐
│ Sidebar │ FeedScreen(main 内容区,flex h-full)                                   │
│ (全局)  │ ┌─ 左栏:数据主区 section(flex-1 min-w-0)────┐┌─ 右栏:渠道列表 aside ─┐│
│         │ │ 工具条(词面/读态分段/计数/历史/显示/刷新)      ││ 搜索框(贴顶)        ││
│         │ │ TG 监控台条(仅 TG 渠道选中时;不随流滚走)     ││ ──────────────────  ││
│         │ │ ┌────────────────────────────┐ ││ 渠道行(滚动)         ││
│         │ │ │ 时间线滚动区(TG 气泡/条目卡)     │ ││  ▣ 频道名   12:01    ││
│         │ │ │ 日期胶囊 / 加载更早              │ ││    最新预览    (3)    ││
│         │ │ └────────────────────────────┘ ││  ▣ …                ││
│         │ │ [未选中 = 引导空态/统计/首跑 CTA]     ││ …                  ││
│         │ └────────────────────────────────────┘└─ 脚注:N 个渠道 ──────┘│
└──────────────────────────────────────────────────────────────────────────┘
```

- DOM 顺序:左栏 `<section>` 先、右栏 `<aside aria-label="渠道列表">` 后(flex 行内自然落右,视觉即右,符合主人指定)。
- 根容器:`<div className="flex h-full min-h-0">`(双栏行);**去 v6 顶层 `px-6` 大留白与外层滚动**——双栏各自内滚:左栏时间线区 `flex-1 min-h-0 overflow-y-auto`,右栏行列表 `flex-1 min-h-0 overflow-y-auto`。沿用 Kestra「满高内滚」惯例(feed-screen.tsx:2318-2319 注记)。
- 两栏之间 `border-l`(右栏左缘描边)+ 右栏底色 `bg-muted/20` 微差(列表区与内容区的质感分层,TG 桌面同构)。

## 1. 右栏:渠道列表栏(群组列表)

### 1.1 宽度与容器

- 固定宽 **`w-72`(288px)`shrink-0`**;视口 <1280px 降 `w-64`(256px,`max-lg:w-64` 一档即可)。不做折叠钮、不做拖拽调宽(桌面主窗口 1920,右栏 288px 后左栏仍有 ~1400px;复杂度不值)。
- 结构自上而下:搜索框(贴顶,sticky 语义由容器布局天然保证)→ 行列表(内滚)→ 脚注(渠道数词面)。

### 1.2 搜索框(置顶过滤)

- 即 v6 工具条搜索位整体迁址(`feed-screen.tsx:2577-2600`):`searchInput/query` 双态、300ms 防抖 + Enter 即时 + Esc 即时清空(`feed-screen.tsx:162, 1606-1611`)、`filterChannelsByQuery` 客户端过滤(渠道名/源 id 包含匹配 + 类型别名,搜「Tg」直出全部 TG 行)——**语义零改,只挪位置**。
- 占位词改右栏语境:「搜索群组/渠道(名称 / 源 id,如 Tg)」;`searchInputRef` 随迁且**搜索框随右栏常驻 = ref 恒挂载**——Mod+F 直聚焦直选(`feed-screen.tsx:2229-2235` 主路径),v6 的 `backToWall + searchFocusPending` 补焦分支(`feed-screen.tsx:2236-2241`)**永不可达,连 `searchFocusPending` 态一并退役**(§6)。Mod+F 新增让位守卫:`detailKey !== null` 时让位(详情弹窗焦点陷阱内把焦点打到遮罩后行为未定义)——并入既有弹窗守卫 `feed-screen.tsx:2245`,详见 §4。
- 搜索只过滤右栏行,不发服务端查询(v6 AC21 语义不变);搜索词**跨选中保留**(选中/清选中不清词)。

### 1.3 渠道行(ChannelRow,新组件)

- 数据源 = `feedChannelCards(catalogItems, states, engineBySource, windowStart)` ∩ `filterChannelsByQuery(cards, query)`(既有纯函数,排序 = 最新新→旧、零条目沉底,`api.ts:840-844`)。
- 行形态(TG 桌面聊天列表的两行密度,借形不改语义):

```
[类型头像 chip]  渠道名(channelDisplayName)        12:01(相对时间,mono)
 size-8 rounded-md   最新一条预览(cardDigest,截一行)      ❸(未读徽标)
```

- **类型头像 chip**:圆角方 `size-8 rounded-md flex items-center justify-center`,内置类型图标 + 色调按 `CHANNEL_CARD_META`(`feed-screen.tsx:142-146`:tg=Send 品牌紫 / site=Rss 灰 / daily=FileText 淡紫),底色同色系淡档(如 tg=`bg-primary/10 text-primary`,site=`bg-muted text-muted-foreground`,daily=`bg-primary/5 text-primary/80`)——头像位即类型徽标,不再另挂 Badge 词标(行宽省给名字;类型以图标+色承载)。
- **行 1**:渠道名(`text-sm font-medium truncate`)+ 右侧最新相对时间(`formatRelativeTime`,mono `text-2xs` muted;零条目不显)。
- **行 2**:最新预览(`cardDigest(latest)`,F6 同文回退 `latest.title`,零条目 = 知会词「今日暂无新条目」;`text-xs text-muted-foreground truncate` 一行)+ 右侧未读徽标(`unread > 0` 才渲染:`min-w-5 rounded-full bg-primary px-1.5 text-center text-2xs font-medium text-primary-foreground tabular-nums`,数字 9+ 截断)。
- **选中高亮**:选中行 = `bg-accent` 填充 + 渠道名转 `text-link`(Kestra NavRow「填充 + 文字色」范式,`sidebar.tsx:169-176` 同门);hover = `bg-accent/50`;键盘巡游环 = `ring-1 ring-primary/60`(仅 `navByKeyboard` 时,与条目卡同门)。
- 行根:`div role="button" tabIndex={0}` `data-testid="feed-channel-row-<key>"` `data-item-key=<key>` `data-channel-kind` `data-selected` `data-unread`;`aria-current="true"` 标选中行;Space/Enter 双键激活语义(深检 F5 同门,`feed-screen.tsx:1134-1141`);点击/Enter = `openChannel(key)`。memo 化(同 ChannelCard/FeedCard 模式,hover onCurrent 只改 key)。
- 未读徽标与行内计数 title 沿用「已加载口径」真话(`feed-screen.tsx:1175` 的 title 文案收编进行组件,title 注「全库首页 50 条铺底口径」)。

### 1.4 脚注

- 一行词面:「`N 个渠道`」;搜索时「`命中 M / N 个渠道`」(v6 墙态计数词面迁此)。**testid 独占 `feed-count`**(复审 R1-1 消歧:全屏唯一,常驻栏挂它;选中态工具条计数词面另挂 `feed-stream-count`,见 §2.1——双挂 `feed-count` 会让 `getByTestId` 多匹配抛错)。

## 2. 左栏:数据主区

### 2.1 工具条(读态工具条,按选中态分叉)

单行 `flex flex-wrap items-center gap-2 px-5 py-2.5 border-b`,内容按「未选中(总览)/选中渠道」两态取件,**全部是既有控件归位,零新控件**:

| 件 | 未选中(总览) | 选中渠道 | 出处 |
|---|---|---|---|
| 作用域词面 | 「全部情报」 | 渠道名(channelDisplayName) | `feed-stream-title` 保留 |
| 总览钮 | 不出 | 出(ChevronDown rotate-180 + 「总览」;清选中,testid 改 `feed-back-to-overview`) | 替代 v6 `feed-back-to-wall` |
| 读态分段 未读/星标/稍后读/全部 | 不出 | 出(历史态隐藏,既有) | `feed-screen.tsx:2354-2386` |
| 计数词面 | 渠道数已归右栏脚注,此处不出 | 「已加载 X · 共 T 条」/ 回落词面(既有 F2 口径);**testid 改挂 `feed-stream-count`**(原 `feed-count`,复审 R1-1:让位右栏脚注,防双挂) | `feed-screen.tsx:2403-2425`(:2406 现 `data-testid="feed-count"`) |
| 知会词 | 不出(统计在引导空态) | 「全量 · 新→旧 · 实时滚动」/ 历史态「全部历史 · 已读未读全显」 | `feed-screen.tsx:2429-2445` |
| 退出历史钮 | 不出 | 仅历史态出 | `feed-screen.tsx:2446-2457` |
| 全部标已读/未读(二次确认) | **出**(全库语义与总览语境相符) | 不出(既有 `bulkHidden` 原样) | `feed-screen.tsx:2463-2523` |
| 显示选项(未读优先/分组) | 不出 | 出 | `feed-screen.tsx:2527-2574` |
| 搜索框 | **不出(已迁右栏)** | 不出 | 迁址 §1.2 |
| 刷新 | 出(刷 catalog) | 出(刷当前流) | `feed-screen.tsx:2603-2613` |
| 导出 JSONL/CSV + 导出全库 | **出**(全库语义) | 不出(既有「范围不实不出钮」原则) | `feed-screen.tsx:2616-2655` |

- R1 吸收:选中态计数 title 删「当日窗视图首页」残词,统一「共 T 条 = 当前过滤条件全量计数,含未翻页;已加载 X 条为已加载口径」(`feed-screen.tsx:2409`)。
- **计数 testid 消歧(复审 R1-1,blocker)**:`feed-count` = 右栏脚注独占(两态都在场);`feed-stream-count` = 选中态工具条条目计数(仅选中态在场)。两 testid 任意时刻至多各一个实例,`getByTestId` 恒单匹配;测试迁移时 :521/:3306/:3321/:3335 的详情态断言改 `feed-stream-count`,:664/:723 的渠道数断言改打右栏脚注 `feed-count`(实测 `feed-screen.test.tsx` 六处引用已核对)。
- 错误/回执行(`exportNote/openError/markError`)保留在时间线区顶部(既有位置语义,随滚动区走)。

### 2.2 TG 监控台条(仅选中渠道 kind=tg)

- v6 监控台卡(`feed-screen.tsx:2719-2804`)**降高为条**:单行 flex-wrap——「Telegram 监控台」词 + 状态段(● 监控中 · 账号 · 自 时间 / 未登录知会词)+ 右侧钮簇(扫码登录|登录中…、内置浏览器预览、管理)+ 第二行「看全部历史消息(含已读)」文字钮 + 预览失败注记行(`tgPreviewNote`)。内容零增删,只重排;样式沿用现状卡原值 `rounded-md border border-primary/30 bg-primary/5 px-3 py-2.5`(`feed-screen.tsx:2722`,复审注:padding 与现状逐字对齐,免无谓 diff)。
- **落位 = 工具条之下、时间线滚动区之外**(兄弟节点,不随流滚走):监控状态常驻可见,这正是「监控台条」的意义;不再像 v6 埋在滚动流内随内容上滚。
- 逻辑零改:状态快照 effect(`isTgChannel` 派生自选中渠道的 kind;deps 含它,保 v2.1 教训)、`retryTgStatus`、`startWebLogin`、`tgPreviewUrl` 推导(遍历域改 streamItems)、`openTgPreview`、`sanitizeTelegramStatus` 全保留。
- **R2 吸收**:状态态拆三层——`tgStatusPhase: "idle" | "loading" | "ok" | "error"`(替换 `tgWebline === null` 的双态):loading(首拉在途)监控台条与空态卡**都不出**(时间线骨架已在转,不闪「状态未知」);error 才出「监控状态未知 + 重试拉取状态」(既有文案保留);ok 出监控台条。旧 `tgWebline` 数据态保留在 phase=ok 内。已知的残余一拍空白(流查询已回空、状态快照仍在途 = phase=loading 时左栏零呈现)**设计接受不收**:单 RPC 在途窗极短,为它加「状态拉取中」细条是常驻 UI 为瞬态买单(复审注采纳「可接受」项,不加新 UI)。
- 切到非 TG 渠道:监控台条卸载(条件渲染即得);切回 TG:phase 走 loading→ok/error 重拉(账号级状态,两 TG 渠道间切换不重拉,可接受)。

### 2.3 时间线主体(选中渠道)

- **TG 渠道 = 聊天气泡时间线**(既有 chatView 全套):气泡卡 w-fit 左对齐、未读亮泡/已读降档、日期居中胶囊分组(今天/昨天/7 天内/更早)、不分组平铺——`feed-screen.tsx:2985-3007` 原样迁入左栏滚动区。气泡 `max-w-[min(100%,640px)]`(`feed-screen.tsx:430`)随左栏宽自适应,零改。
- **网站/日报渠道 = 条目卡单列列表**:v6 详情的 columns 多列瀑布流(`feed-screen.tsx:3008-3022`)**降为单列纵向列表**(Kestra 行密度;左栏 ~900-1400px 下双列挤,单列读性最优;FeedCard 五档差异化头区/价格行/diff 块不因列数受影响)。容器 `data-testid="feed-waterfall"` 改名 `feed-stream-list`(名实相符),`mb-3 break-inside-avoid` 包装层撤除。
- 分组/平铺由显示选项驱动(既有 `groups` memo,`feed-screen.tsx:1977-1994`,分组仅聊天视图生效——语义不变)。
- **加载更早**:列表尾部按钮(既有 `feed-screen.tsx:3024-3028`),仅选中态;hasMore 语义/复合游标/判停零改。

### 2.4 未选中 = 引导空态(总览态)

- 左栏主体位置出引导空态(EmptyState 容器 + 总览统计行):
  - 统计行(数据全从 channelCards 派生,零新 RPC):「N 个渠道 · 今日 Σtoday 条 · 未读 Σunread」(mono 数字,三段 inline)。
  - 主词面:「从右侧选择一个群组或渠道,这里显示它的消息流」——引导动线指向右栏。
  - **承接 v6 墙空态三兄弟**(语义迁址,判定条件原样):`firstRun` → 首跑空态(去源管理,`feed-screen.tsx:2838-2852`);空流 → 运行第一个插件 CTA(idle→starting→collecting→done/error 状态机,`feed-screen.tsx:2853-2887`);搜索零命中**不在此**(搜索空态归右栏行列表内的小空态,§1.3 列表尾,「没有匹配的渠道」词面保留)。**冷启动防闪(复审注)**:v6 判定链以「loading 先出骨架」打底(`feed-screen.tsx:2806`),总览态不搬骨架则 catalog 在途一拍会闪「运行第一个插件」——故 firstRun/CTA 两分支以 **`catalogLoaded` 门**(catalog 首拉应答已落,boolean 新态)为前置;在途时统计行与空态主体都不出,左栏留白一拍(与右栏行骨架同期,无 CTA 闪现)。
- 总览态左栏不出大骨架(catalog 在拉时右栏出行骨架;左栏仅统计行位留白,catalogLoaded 翻转后统计与空态一次落位)。

## 3. 状态与数据接线

### 3.1 选中态(scope 改名不改形)

```
const [scope, setScope] = useState<{ source: string | null; history: boolean }>({ source: null, history: false });
```
- 形状沿用 v6(`feed-screen.tsx:1471-1476`),仅语义重述:`source = null` 不再是「渠道墙」而是「总览态」;`history` 仍是「该渠道历史态(读态豁免)」。
- `openChannel(key)`:置 `{source: key, history: false}` + 清左栏键盘环;`clearSelection()`(替代 `backToWall`):置 `{source: null, history: false}`;`openHistory()/exitHistory()` 原样。**无路由变化**(与 v6 同,作用域是屏内 state,不进 URL)。

### 3.2 双缓冲(本稿最关键的结构改动)

v6 单一 `items` 同时喂「墙聚合」与「详情流」,双栏下选中渠道会把右栏其他行的数据饿死——**拆双缓冲**:

- **`catalogItems`**(全库铺底):`refreshCatalog()` = `fetchFeedPage({ cursor:null, cursorId:null, source:null, withTotal:countReady })`(首页 50);`liveRefreshCatalog()` = 同参静默拉 + `mergeFreshItems` 前插。**只喂右栏**:channelCards 聚合、总览统计。挂载即拉;completed/cron.completed 事件 + 30s 可见性轮询保活(既有两 effect `feed-screen.tsx:1686-1714` 改挂 catalog 域)。
- **`streamItems`**(+cursor/cursorId/hasMore/total/loading/loadingMore/error,即 v6 `items` 全套游标机件):查询带 `source: scope.source`(fetchFeedPage source= 既有,`api.ts:57`);**仅选中态拉取**(`scope.source === null` 时不拉、切总览即清流态);loadMore/refresh 既有对票守卫(`feedSeqRef` 拆 `catalogSeqRef`/`streamSeqRef` 两票,防旧域包互踩,机制同 `feed-screen.tsx:1536-1544`)。事件/轮询在选中态时**双刷**(catalog + stream 各自静默 merge)。
- **读态 states**:服务端通路 = `statesFromItems([...catalogItems, ...streamItems])`(两缓冲并集投影,`api.ts:330` 纯函数零改);未过门通路 = localStorage `localStates` 原样(`feed-screen.tsx:1719-1722` 改并集源)。这样选中渠道内标读,右栏该行未读徽标即时降——**右栏与左栏读态同源联动**。
- **缓冲写路面枚举(复审注补全,写者一个不漏)**:两缓冲的全部本地写者与归属——
  - `flipItem`(新 helper,替换 `markItemState` 的裸 `setItems` 翻转,`feed-screen.tsx:1790-1795`):**双写**两缓冲;其 previous 真值查找(`feed-screen.tsx:1788` 的 `items.find`)**改查双缓冲并集**——条目可能只在 catalog(选中前看过的行)或只在 stream(选中后加载),漏一边则 rollback-to-previous 语义破。
  - `onEnriched` 精评回写(`feed-screen.tsx:1837-1843` `setItems` 回写 scores):**只写 streamItems**(精评钮在左栏时间线卡上,条目必在当前流;catalog 不需要分数)——漏改则精评后分数徽标不即时刷新。
  - `markAllRead` 乐观翻转(`feed-screen.tsx:1874-1888`):只在总览态有入口 → 只翻 catalogItems(选中态无批量钮,零歧义);失败回滚同门。
  - `mergeFreshItems`/`appendFeedPage`:各自归属域(catalog 收静默首页合流,stream 收翻页追加与合流)。
  - 服务端通路态源不变:`statesFromItems([...catalogItems, ...streamItems])` 并集投影(上文);未过门通路 `localStates` 原样。

### 3.3 渠道全集 / stats / 搜索 / 历史归位

- 渠道全集:`feedChannelCards(catalogItems, …)`——health sources ∪ catalog source 去重,零条目渠道也出行(`api.ts:808-811` 原样);`engineBySource` 挂载一次 effect 原样(`feed-screen.tsx:1555-1568`)。
- 总览统计:Σtoday/Σunread 由 channelCards reduce(纯派生)。
- 搜索:只过右栏(§1.2);`query` 不进任何服务端查询(v6 语义)。
- 历史态:流查询仍 `source` 作用域,`visible` 在 history 时豁免读态过滤(`feed-screen.tsx:1905-1914` 原样);当日窗只作用于右栏「今日 N」计数(渠道详情无当日窗,深检 F1 定案不动);60s `windowStart` 滴答原样(`feed-screen.tsx:1574-1578`)。
- 详情弹窗:`detailKey` 命中域 = streamItems(总览态无条目,弹窗天然不出);`openDetail` 弹开记已读、`FeedItemDetail` 本体零改(`feed-screen.tsx:1850-1863, 1196-1364`)。
- 能力门:READ_STATE/COUNT 两门探测与回退语义原样(`feed-screen.tsx:1583-1603`);`withTotal` 只进 catalog 首拉与 stream 首拉(游标页不带,既有)。

### 3.4 显示选项 / 分组 / 键盘环派生

- `display`(unreadFirst/groupMode,本地持久)只作用于 streamItems 展示序——原样。
- `chatView = channelCardKindOf(scope.source, engineBySource.get(scope.source)) === "tg"`(派生式原样,`feed-screen.tsx:1940-1944`);总览态 `scope.source === null` 时 chatView 恒 false。

## 4. 键盘语义(终案)

原则:**j/k 巡游环 = 右栏行(主人方向钉死);左栏条目巡游整体上移 Shift 层;Enter/U 落点跟随「当前环」**。双环状态:`listCurrentKey`(右栏)/ `itemCurrentKey`(左栏)+ `navPane: "list" | "timeline"`;hover/focus 各自置本环 key 并切 navPane、清 `navByKeyboard`(既有 onCurrentCard 语义按栏复制)。

| 键 | 右栏环(navPane=list) | 左栏环(navPane=timeline) |
|---|---|---|
| `j` / `k` | 渠道行下/上移(边界钳制不回绕、未选中时 j 落首行 k 落末行、scrollIntoView 最近侧、环仅键盘巡游呈现)——机件全部沿用 `feed-screen.tsx:2282-2296` | —(让位) |
| `Shift+J` / `Shift+K` | —(让位;event.shiftKey 守卫分流) | 条目下/上移(同上机件) |
| `Enter` | 打开当前行渠道(=openChannel;行根 Space 同门) | 开当前条目详情弹窗 |
| `U` | **当前渠道已加载条目一键标已读**(triage 动作):单次 `api.storeStateMark({ keys: 该渠道已加载条目 keys, marker:"read", value:true })`(keys 数组协议既有,`feed-screen.tsx:1797-1799` 同门),乐观翻两缓冲、失败回滚;**范围 = 已加载口径**(与右栏未读徽标同门,title 如实注「已加载 X 条,未翻页不含」);已加载 0 条 = 无操作。未过门 = 本地态 `setMarkerBulk` 同构 | 当前条目已读/未读切换(既有 toggle) |
| `Esc` | 清选中回总览 | 清选中回总览 |
| `Mod+F` | 聚焦右栏搜索框并全选(搜索框常驻 = ref 恒挂载,直聚焦;详情弹窗开着 = 让位,§4 守卫) | 同左 |
| 详情弹窗开着 | 全部巡游/置位键让位(既有守卫 `feed-screen.tsx:2245`) | 同左 |

- 守卫不动:输入框/textarea/select/contentEditable 内敲键不触发;Enter 命中 button/a 归原生(`feed-screen.tsx:2248-2262`)。**Esc 分支落位铁律(复审注)**:`escape` 加入既有键过滤(`feed-screen.tsx:2246` 的 pressed 白名单),且分支必须放在弹窗守卫(`:2245` `if (detailKey !== null) return;`)**之后**——弹窗开着按 Esc 只关弹窗(Radix 自 handling),不清选中退总览;Esc 清选中仅在弹窗闭时可达。另注:批量二次确认的全局 Esc 收口(`feed-screen.tsx:2024-2042`)只在总览态可达(确认簇仅总览渲染,选中恒 null),与新 Esc 清选中天然无冲突(清 null = no-op),无需另设互斥守卫。Mod+F 同并入 `:2245` 弹窗守卫(§1.2)。
- 备选案(已否决,留档防复审翻案):↑/↓ 巡右栏 + j/k 保条目(零破坏变更)。否决因:主人明示「巡游=右栏行」以 j/k 计,且双套箭头/字母巡游并存语义解释成本更高;条目级旧键位 Shift 上移是一次性、可文档化的破坏。

## 5. 保留面(逐件清单,重构师对照勿丢)

| 面 | 保留内容 | v7 落位 |
|---|---|---|
| 详情弹窗 | FeedItemDetail 全件(标题全文/元信息簇/正文/图析/动作簇;Esc/遮罩关闭;弹开即记已读) | 零改,Portal 照旧 |
| 悬停操作簇 | FeedCard 内簇(👍👎/AI 摘要/沉淀关键词/打开原文/星标/稍后读/已读切换)+ focus-within 可达 | 零改(在卡内,随卡进左栏) |
| 右键菜单 | ContextMenu 四动作(打开原文/复制链接/标已读/沉淀为关键词) | 零改 |
| TG 监控台 | 扫码登录(browser.open 单入口)/● 监控中+账号+自时间/管理→设置·Telegram/内置浏览器预览(t.me/s 推导+置灰如实+失败注记)/看全部历史消息直达 | 降为左栏顶部常驻条(§2.2),逻辑零改 |
| 历史态 | history 豁免读态、退出历史钮、空态「看全部条目」入口、知会词 | 原样,入口/出口随工具条归位 |
| 加载更早 | 复合游标翻页 + 判停 + 按钮内联 loading | 时间线尾部原样 |
| 能力门与回退 | READ_STATE/COUNT 两门;未过门 localStorage 通路 + 一次性搬迁;旧 sidecar 无 total 回落词面 | 原样(状态源扩为双缓冲并集,§3.2) |
| 空流 CTA/首跑 | run.start 状态机、去源管理 | 总览引导空态承载(§2.4) |
| 实时滚动 | completed/cron.completed 即时 + 30s 可见性轮询 + mergeFreshItems | 挂双缓冲(§3.2) |
| sr-only aria-live | 作用域播报 | 保留,词面随 IA(「全部情报」/渠道名) |

## 6. 撤除面(逐件清单,收编去向)

| 撤除件 | 现位置 | 去向 |
|---|---|---|
| 渠道瀑布流落地页(ChannelCard + columns 容器 `feed-channel-wall`) | `feed-screen.tsx:1096-1187, 2964-2984` | ChannelCard 组件退役;信息收编为右栏 ChannelRow(§1.3) |
| 渠道详情返回钮(`feed-back-to-wall`)+ 墙⇄详情页面切换 | `feed-screen.tsx:2333-2345, 2145-2149` | 双栏无页面切换;替代 = 工具条「总览」钮(`feed-back-to-overview`)+ Esc(§4) |
| 监控台在渠道详情滚动流顶部的旧落位(整卡随滚) | `feed-screen.tsx:2719-2804` | 左栏工具条下常驻条,不随滚(§2.2) |
| 渠道详情条目 columns 瀑布流(`feed-waterfall`) | `feed-screen.tsx:3008-3022` | 单列列表(`feed-stream-list`) |
| 工具条搜索位 | `feed-screen.tsx:2577-2600` | 迁右栏顶(§1.2) |
| 渠道数词面在工具条 | `feed-screen.tsx:2393-2402` | 迁右栏脚注(§1.4) |
| PageHeader 死调用 | `feed-screen.tsx:2320-2325` | 删(组件本就渲染 null,零视觉变化) |
| 选中/清除时 `setCurrentKey` 单环清法 | `feed-screen.tsx:2140-2149` | 双环(§4);`currentKey` 单态退役 |
| `searchFocusPending` 补焦机制 | `feed-screen.tsx:1998-2007, 2236-2241` | 退役(复审注:搜索框随右栏常驻,ref 恒挂载,分支永不可达;Mod+F 改直聚焦 + 弹窗守卫让位,§1.2/§4) |
| 外层滚动容器(`feed-wall` testid) | `feed-screen.tsx:2662` | 退役(双栏各自内滚,§0;测试/冒烟零引用,已核) |
| 墙态分支的空态容器(`feed-search-empty` 整卡等) | `feed-screen.tsx:2828-2837` | 搜索空态降为右栏列表尾行内小空态;首跑/CTA 迁总览(§2.4) |

## 7. 边界:宽度 / 响应式 / 空态 / 加载态 / 错误态

- **宽度分档**:右栏 `w-72`(≥1280px)/ `max-lg:w-64`(<1280px);左栏 `flex-1 min-w-0`(气泡 w-fit、卡片 truncate、工具条 flex-wrap 均已自适应)。**建议(随 AC28 打包批落)**:`tauri.conf.json` 加 `"minWidth": 960, "minHeight": 640`——根除极窄窗挤压,与 256px 右栏 + 左栏 ~676px 的最坏布局自洽;不加亦不破(左栏可缩至气泡 min-w-[13rem] 仍可读)。
- **空态阶梯**(全部保留既有文案基调,落位更新):
  1. 右栏搜索零命中:行列表尾行内小空态「没有匹配的渠道…」(`feed-search-empty` testid 保留)。
  2. 总览 + firstRun / 空流:引导空态(§2.4,testid `feed-first-run` / `feed-run-cta` 保留)。
  3. TG 渠道流空:三态——状态未知(**仅拉取失败**,R2 吸收,`feed-tg-status-unknown` 保留)/ 未登录 / 监控在线(文案原样,`feed-screen.tsx:2888-2926`)。
  4. 零条目渠道:「该渠道暂无入库条目」+ CTA 改「回总览」(原「返回渠道墙」,`feed-channel-empty` 保留)。
  5. 读态过滤空:EMPTY_TEXT 词表 + 「看全部条目(含已读)」(原样)。
- **加载态**:catalog 首拉 = 右栏 4-6 行行形骨架(skeleton 贴 ChannelRow 两行形)+ 左栏引导空态照出;选中切换 = 左栏 4 卡既有骨架(`feed-loading` 保留)+ 右栏纹丝不动;loadMore = 按钮内联(既有)。
- **错误态**:sidecar 错误卡(pyenv_not_ready 引导 / 通用重试,`feed-error` 保留)出在**左栏主体位**(catalog 域错 = 总览态显示;stream 域错 = 选中态显示;对票守卫防旧域错误污染新域,`feed-screen.tsx:1641-1647` 机制复制到双票)。

## 8. testid 影响清单

| testid | 处置 |
|---|---|
| `feed-count` | **右栏脚注独占**(§1.4;渠道数词面;任意时刻全屏唯一实例——复审 R1-1 blocker 消歧) |
| 选中态工具条条目计数(原 `feed-count`,`feed-screen.tsx:2406`) | **改名 `feed-stream-count`**(仅选中态在场;测试 :521/:3306/:3321/:3335 随改) |
| `feed-channel-wall` / `feed-channel-<key>` / `feed-channel-strip-<key>` / `feed-channel-count-<key>` | 退役(墙撤);行新挂 `feed-channel-row-<key>`(strip/count 收进行内属性或随迁子 testid) |
| `feed-back-to-wall` | 改名 `feed-back-to-overview`(语义=清选中) |
| `feed-waterfall` | 改名 `feed-stream-list`(单列) |
| `feed-wall` | 退役(外层滚动容器撤,§6;测试/冒烟零引用已核) |
| `feed-chat-timeline` / `feed-flat-list` | **保留**(聊天视图原样迁入左栏;`feed-chat-timeline` 测试 :3464 有 1 处引用,勿误删) |
| `feed-toolbar` / `feed-stream-title` / `feed-day-window` / `feed-history-exit` / `feed-search-scope` / `feed-confirm-all-group` / `feed-loading` / `feed-error` / `feed-search-empty` / `feed-first-run` / `feed-run-cta` / `feed-tg-console*`(6 件)/ `feed-tg-status-unknown` / `feed-channel-empty` / `feed-empty-history` / `feed-item-*` / `feed-tg-bubble-*` / `feed-group-*` / `feed-detail-*` / `feed-export-result` / `feed-open-error` / `feed-mark-error` | 保留,落位随 §1/§2 |
| FeedCard 内部件(`feed-strip-*` / `feed-watch-badge-*` / `feed-watch-target-*` / `feed-deal-price-*` / `feed-enrich-*` / `feed-keyword-*` / `feed-image-*` / `feed-doc-body-*` / `feed-expanded-*`) | 随「FeedCard 零改」自然保留,勿动 |
| 新增 | `feed-channel-list`(右栏行列表容器)/ `feed-channel-search`(右栏搜索框)/ `feed-overview`(总览引导空态)/ `feed-stream-list` / `feed-stream-count` |

## 9. 测试与门禁迁移

- **api.ts 纯函数零改**:`feedChannelCards` / `filterChannelsByQuery` / `channelDisplayName` / `channelCardKindOf` / `statesFromItems` 等既有用例(含「渠道卡纯函数」describe)不动。
- **feed-screen.test.tsx**(137 例):①挂载/动线类用例——「点渠道卡」改「点渠道行」(`feed-channel-row-*`),「返回渠道墙」改「总览」;②墙断言类(v6 渠道瀑布流/零条目出卡/监控台落点/聊天形态锚/深审 F2/F4/F5/F6 五个 describe,约 40-50 例)改断言对象为行/左栏落位;③**计数断言消歧**(R1-1):详情态 `feed-count` 六处引用中 :521/:3306/:3321/:3335(条目计数)改 `feed-stream-count`,:664/:723(渠道数)改打右栏脚注 `feed-count`;④新增面:双缓冲联动(选中渠道标读 → 右栏行徽标降)、U-渠道已加载标已读(过门/未过门/空集三态)、Shift+J/K 巡游、Esc 清选中(含弹窗开着让位)、R2(首拉在途无「状态未知」闪现)、R1(词面无当日窗残词)。目标全量 feed 文件 ≥ 137 例且全绿。(引用量口径,复审注:`grep -oE "feed-channel[a-z-]*"` = 109 处,加 `feed-back-to-wall` 9 处 ≈ 118 处,对账以此为准。)
- **冒烟**:`scripts/feed-card-smoke.py` 点卡动线改点行;`e2e/feed_channels_smoke.py` 仍指 10-06 三级 IA(feed-l1/l2/l3)早已过期——随本批重写为双栏五动线(右栏行→TG 时间线→详情弹窗→总览→搜 Tg)或声明退役(v6 五动线截图脚本若为 ad-hoc 则以新脚本替代)。执行口令与基线由重构/验收阶段定,设计只钉「动线锚 = 行点击,非卡点击」。
- **门禁照旧**:build / feed vitest / pytest desktop+store(store 零改动,跑存量防回归)/ 无头冒烟 + 换装双实锤 + app 还原(AC28)。

## 10. 实施顺序建议(给重构师)

1. **双缓冲地基**:`items` → `catalogItems` + `streamItems` 拆分、双票守卫、states 并集源、flipItem 双写(§3.2)——此步不动 UI,先让既有断言在等价行为下绿。
2. **右栏 ChannelRow + aside**:搜索框迁址、行列表、脚注;`feed-channel-wall` 撤。
3. **左栏重组**:工具条分叉、监控台降条(+R2 phase 态)、时间线落位、单列列表、总览引导空态。
4. **键盘双环**(§4)+ Esc/Mod+F 落点。
5. **测试/冒烟迁移**(§9)→ 门禁全绿 → 换装入库。

每步独立可绿,重构师按步提交;AC25/AC26 验收动线 = 「进屏见右栏列表 → 点行左栏出流 → TG 行出监控台条 → 点条目出弹窗 → Esc 回总览」。
