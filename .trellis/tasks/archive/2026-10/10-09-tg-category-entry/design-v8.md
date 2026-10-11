# 情报流 v8 设计稿 · 三级界面(1 类型卡瀑布流 / 2 全渠道列表 / 3 渠道详情)

> 主人最终定调(2026-10-10 晨,v8 追加):此前 v7 把 3 级做进了 1 级(双栏监控台 = 选中即数据)= 做错。正确层级:**1 级 = 渠道类型卡瀑布流(竖版卡,只有卡片+搜索)→ 2 级 = 该类型下全渠道列表 → 3 级 = 该渠道详情(消息时间线/条目;TG 含监控台)**。深度测试以 3 级为重点。本稿替代 design-v7.md 的双栏方案;v7 已落地的机件(双缓冲/监控台 phase/能力门/行组件)按 §6 逐项收编,不推倒重来。
>
> 事实底座(2026-10-10 实查,写定不再摸底;引注 = 本会话实读):
> - 现状 = v7 双栏已落地:`scope {source, history}`(`feed-screen.tsx:1552-1557`)、双缓冲 catalogItems/streamItems(`:1575-1576`)、右栏 aside 搜索+ChannelRow+脚注(`:3290-3385`)、左栏工具条+监控台条+时间线(`:2662-3287`)、双环键盘 navPane/Shift 层(`:2237-2239, 2470-2646`)。
> - 查询通路:`fetchFeedPage` 现仅收 `cursor/cursorId/pageSize/source/withTotal`(`api.ts:23-35, 50-69`);**category/source_kind/query 三参在 v5/v6 信息架构退役时从本封装摘除**(`api.ts:28-31` 注记)——但**共享客户端与后端三参全在**:`StoreItemsParams` 仍带 `source_kind/query/with_total`(`lib/api/types.ts:416-430`),`_m_store_items` 照收(`entry.py:1655-1742`,`source_kind` 校验 `:1704-1708`,`with_total` `:1712-1734`)。重挂 = 封装层一行透传,零后端动。
> - store 层过滤单点 `_items_filter_sql`(`src/myssia/store/sqlite.py:866-931`):`source` 精确等值;`source_kind` **"im" = `source LIKE 'telegram-%' OR 'tg-%'`,"web" = 其余含 source NULL**(`:904-909`);`query` = title/content/source 三列 LIKE NOCASE(`:920-929`);`count_items` 同 WHERE(`:972-999`)。
> - 能力门:READ_STATE_PROTOCOL=10(`api.ts:313`)/ COUNT_PROTOCOL=13(`api.ts:323`);后端 `PROTOCOL_VERSION = 13`(`entry.py:511`)。读态列 read/starred/later 0/1 在库(`sqlite.py:142-144`)。
> - 类型判定两套并存:**五档呈现档** channelKindOf(telegram/watch/document/deal/news,`api.ts:599, 620-638`,**前缀优先** `:624-625`)与**三档渠道卡档** channelCardKindOf(tg/site/daily,`api.ts:753, 768-774`,**engine 优先**)。TG 词表 TG_ENGINES = tg_web/telegram/telethon/bot(`:757`);日报 DAILY_ENGINES = prompt/store_report(`:760`);前缀规约 TELEGRAM_SOURCE_RE(`:602`)。
> - **判定矛盾实锤**:同一源可挂不同 engine——`telegram-mihomo_party_group` 在 telegram-groups.yaml engine=telegram、telegram-web.yaml engine=tg_web;`telegram-durov` 在 telegram-channels.yaml engine=static_html(本会话逐文件 grep 实证)。health 插件遍历 = 路径字典序(`cli.py:2854` sorted glob),engineMapFromHealth 首遇即胜(`api.ts:643-649`)→ mihomo 恰好落 groups.yaml 判 tg,durov 判 **site**(按媒介应属 TG)。v8 必须改前缀优先(§4.2)。
> - health 结构:`plugins[] = {file,id,name,loaded,sources:[{name,url,engine,engine_hint,health,fingerprint_skips}]}`(`cli.py:3341-3373`);渠道全集 = health sources ∪ 条目 source 去重、零条目渠道也在(`feedChannelCards`,`api.ts:801-845`)。
> - telegram.status 三线快照(`entry.py:5836`)/ browser.open 单入口(`:5793-5818`);UI 侧 `telegramGetStatus/telegramWebLogin` 来自 `@/screens/settings/telegram-api`(`feed-screen.tsx:108`);监控台 phase 机件(idle/loading/ok/error)与预览推导(openTgPreview,`feed-screen.tsx:2182-2204, 2415-2468`)v7 已修 R2。
> - 活库实测(只读 SQL,本会话执行;条数为实查时点值,活库日增漂移无涉——拷问 R1 复跑 1463,同性质):`~/Library/Application Support/MYIA/myssia.db` 1461 条 / 21 个具名源 / **0 条 NULL source**;类型归位 = TG 1 源(telegram-mihomo_party_group)+ 网站 17 源(openai-news / cocoloop / cheapshark / steam-specials / epic-free / github-new-stars / aihot / 博客族 / *-watch(urlwatch)等)+ **日报 3 源(daily-digest=store_report;ai-token-deals、ai-vendor-watch=engine prompt,`plugins/ai-token-deals.yaml:19`、`plugins/ai-vendor-watch.yaml:35` 实读——拷问 R1-Q1 裁定词表权威,首稿「日报 1 源」系归并笔误,已改)**。
> - 测试/冒烟资产:`feed-screen.test.tsx` **145 例**(`grep -c` 实测);冒烟 `desktop/scripts/feed-card-smoke.py`(381 行,锚 v7 双栏:`feed-channel-list`/`feed-channel-row-*`/`feed-chat-timeline`/`feed-stream-list`,行 208-359);`tg-card-smoke.py` 锚设置页 telegram-card(不受影响);v7 注记的 `e2e/feed_channels_smoke.py` 已不存在(ui-src/e2e/ 实查仅 package_smoke)。
> - 待吸收 P2:无遗留(R1/R2 已随 v7 关闭;v7 N1 一条在打磨册,与本批无涉,不吸收)。

## 0. 定调与总骨架

三级页面切换,屏内 state 驱动(沿用 v6/v7「作用域不进路由」先例,`feed-screen.tsx:1551` 注记):

```
1 级(落地)              2 级                     3 级
┌──────────────────┐   ┌──────────────────┐   ┌──────────────────────────┐
│ 头:搜索+刷新+⋯   │   │ 头:返回+类型名    │   │ 头:返回+渠道名+读态分段    │
│                  │   │    +搜索+刷新     │   │    +计数+检索+显示+刷新    │
│  ┌────┐ ┌────┐   │   │ ┌──────────────┐ │   │ [TG 监控台条,仅 kind=tg]  │
│  │ TG │ │网站 │ … │→  │ │ ▣ 渠道行      │ │→  │ ┌──────────────────────┐ │
│  │竖版 │ │竖版 │   │   │ │ ▣ 渠道行      │ │   │ │ 时间线(TG 气泡/单列)  │ │
│  └────┘ └────┘   │   │ │ …(j/k 环)   │ │   │ │ 日期胶囊/加载更早      │ │
│  columns 瀑布流   │   │ └──────────────┘ │   │ └──────────────────────┘ │
└──────────────────┘   └──────────────────┘   └──────────────────────────┘
        └── Esc/返回钮 逐级回退:3 → 2 → 1;详情弹窗 Esc 只关弹窗 ──┘
```

- 视图态(替代 v7 `scope`):

```ts
type FeedView =
  | { level: 1 }
  | { level: 2; kind: ChannelCardKind }            // ChannelCardKind = "tg"|"site"|"daily"(api.ts:753)
  | { level: 3; source: string; history: boolean }; // history 语义 = v7 scope.history 原样
```

- 迁移函数:`openKind(kind)`(1→2)/ `openChannel(key)`(2→3;v7 既有,`feed-screen.tsx:2379`,改置 level:3)/ `backLevel()`(3→2→1;kind 在 3→2 时由 `channelCardKindOf(source, engineBySource.get(source))` 重派生,v7 `activeChannelKind` 同式 `:2168-2169`)/ `openHistory()/exitHistory()` 原样(`:2399-2406`)。**不跳级**:单渠道类型(如今日 TG 仅 1 渠道)也走 1→2→3 全程,层级一致性优先(主人三层定调是结构性的;「单渠道直达」不做,留档防翻案)。
- 双缓冲**原样保留**(§5.3):catalogItems 喂 1/2 级聚合,streamItems 仅 3 级拉取(v7 §3.2 拆分动机在三级下同样成立,且更甚——2 级列表不能被 3 级流饿死)。
- 满高内滚沿用:每级根容器 `h-full min-h-0`,滚动区各自内滚(Kestra 惯例,v7 §0 已定);1 级卡墙外层可滚(卡片少,单屏通常容纳)。

## 1. 1 级:类型卡瀑布流(落地页)

### 1.1 布局

- 根:`<div className="flex h-full min-h-0 flex-col">`;头部工具条(1.4)贴顶,主体滚动区 `flex-1 overflow-y-auto`。
- 卡墙容器:`mx-auto w-full max-w-6xl px-6 py-6` 内 `columns-[260px] gap-4`(CSS 多列瀑布流,列宽理想 260px,视口自适应列数;v6 墙同门先例,Tailwind 任意值列宽);卡 `mb-4 break-inside-avoid min-h-[340px]`——**高 > 宽由 min-h 兜底 + 内容自然流**(260 宽 × ≥340 高;纯内容自然高约 280-320,340 下限保证竖版比例,主人「卡片高度 > 宽度」钉死)。
- 容器 `data-testid="feed-types-wall"`;卡片逐张 `data-testid="feed-type-card-<kind>"`。

### 1.2 类型卡内容(TypeCard,新组件)

竖版卡自上而下四段,数据全来 §5.1 聚合(诚实口径):

```
┌─────────────────────┐
│ [头像 chip]  类型名   │  ← CHANNEL_CARD_META 同门(feed-screen.tsx:141):tg=Send 品牌紫/
│  TG · 2 个渠道       │    site=Rss 灰 / daily=FileText 淡紫;size-10 rounded-md
│                     │
│   今日 128 条        │  ← 大号 mono tabular-nums(text-2xl);今日 = 当日窗 03:00 起
│   未读 46            │    (api.ts:958 窗锚);未读 = 未标已读全库(不限今日)
│                     │
│  ───────────────────│
│  ▸ mihomo_party_group│  ← 最新预览 2-3 条:成员渠道按 latest_first_seen 降序取前 3
│    消息预览…  12:01  │    (渠道名 + latest_title 一行 truncate + 相对时间);
│  ▸ durov             │    零条目类型 = 知会词「暂无入库条目」
│    预览…    3 小时前  │
└─────────────────────┘
```

- 卡根:`div role="button" tabIndex={0}` `aria-label="打开类型:<名>"`;Space/Enter 激活语义(v7 ChannelRow 同门 `feed-screen.tsx:1145-1156`);hover `ring-1 ring-primary/40` + 抬升 shadow;键盘巡游环 `ring-1 ring-primary/60`(§7 环机件)。点击/Enter = `openKind(kind)`。
- 计数 title 双口径如实:过 STATS 门 = 「全库口径(store.source_stats 分源聚合)」;未过门 = 「已加载口径:全库首页 50 条铺底,更早未计入」(沿用 v7 行徽标 title 词面,`feed-screen.tsx:1197`)。
- 卡序固定词表序 tg → site → daily(稳定心智模型,不按计数跳动);**零渠道类型不出卡**(类型以仓内现存源划分,主人定调;health 词表外类型不猜)。
- memo 化(FeedCard/ChannelRow 同模式)。

### 1.3 搜索(1 级)

- 头部搜索框 `data-testid="feed-type-search"`:客户端过滤类型卡,匹配 = **类型名 + 别名词表**(复用 `CHANNEL_KIND_ALIASES` 语义,`api.ts:851-855`:tg→"tg"/"telegram"、site→"web"/"网站"/"网址"、daily→"daily"/"日报";新增纯函数 `filterTypesByQuery`,query 为类型别名或其前缀即命中——搜「Tg」仅 TG 卡直出,v6.1 主人实测路径同门)。空串 = 全量。
- 零命中:卡墙位行内小空态「没有匹配的类型」(词面沿 `feed-search-empty` 基调);搜索词不进服务端查询。

### 1.4 头部工具条(1 级;「只有卡片+搜索」的最小例外面)

单行 `flex items-center gap-2 border-b px-5 py-2.5`:左 = 搜索框(flex-1 max-w-sm);右 = 刷新钮(重拉 catalog + sourceStats)+ **溢出菜单 ⋯**(DropdownMenu 收纳全库级动作,防「杂项」铺面):导出 JSONL / 导出 CSV / 全部标已读 / 全部标未读(导出词面 = 全库直出语义不变,`feed-screen.tsx:2301-2318`)。词面「全部情报」保留为屏级 sr-only 播报,不占视觉位。
- 承接 v7 总览态工具条全部职责(`feed-screen.tsx:2662-2944` 的 overviewMode 分支),件件有去处、零能力丢失。
- **二次确认簇落位(拷问 R1-Q3 裁定:不能「原样迁入菜单内」)**:Radix DropdownMenuItem 点击默认关菜单,而确认簇 autoFocus + onBlur 失焦即取消(`feed-screen.tsx:2802-2812` 实读)——簇渲染在已卸载的 menu content 里不可见且立即被 onBlur 取消,「迁入菜单内」物理不成立。方案 = **菜单项发起、确认簇渲染在头部(菜单外兄弟位)**:菜单项点击 = `setConfirmAllMark("read"/"unread")` → 菜单按默认行为关闭 → 头部右侧渲染既有确认簇(`feed-confirm-all-group` testid/确认钮 autoFocus/onBlur 失焦取消/「取消」钮,全部代码原样,仅渲染宿主从工具条改为 1 级头部);Esc 全局收口(`:2261-2279`)在 1 级可达,零新互斥守卫。R2 语义(一次点击进入确认态,再点「确认」才执行)完整。
- **AC29 边界追认注(拷问 R1-Q6,待主人点头后方进 §10 第 0 步)**:AC29 写死「只有卡片+搜索,无任何列表/杂项」,本稿 1 级头部仍放刷新钮 + ⋯ 菜单(共 2 个视觉位,5 个动作收纳其中)。**推荐追认现稿**,理由:①v6 AC23(主人已验收)「读态/刷新/导出/键盘等工具性能力保留并随新 IA 归位」——工具能力不能凭空消失,1 级是唯一全库语境宿主(3 级渠道语境下全库钮范围不实);②主人历轮否的是「展示性内容」(消息卡/分类行/chips),两个图标位的工具入口非展示性杂项;③让步案(若主人砍):1 级头砍到只剩搜索+刷新,批量标读/导出在 v8 缺席,待点名再加——不擅自塞进 2/3 级。

### 1.5 空态 / 加载态 / 错误态(1 级)

- 加载:catalog 在途 = 3 张类型卡形骨架(`feed-channel-loading` 同门骨架改卡形;`catalogLoaded` 门沿用,`feed-screen.tsx:1579`)。
- 空态判定链(拷问 R1-Q5 裁定,三态写死优先级,health/catalog 竞速下唯一解释):
  1. **零源**(`catalogLoaded && channelCards.length === 0`,health 亦无源):卡墙不出,落位出 `firstRun` 首跑卡(去源管理)或空流 CTA 卡(`feed-first-run`/`feed-run-cta` testid 保留,idle→starting→collecting→done/error 状态机 `feed-screen.tsx:2320-2341` 原样)——v7 总览分叉原样(`:3082-3131`)。
  2. **有源零条目**(`catalogLoaded && channelCards.length > 0 && catalogItems.length === 0`,插件在、cron 未跑/刚清库):**卡墙照出**(三张零值卡,渠道结构如实,卡内落「暂无入库条目」知会词,§1.2)+ **卡墙之下并置空流 CTA 卡**(同 `feed-run-cta` 件,词面区分:「插件已就绪,还没有任何入库条目——先运行一个插件」)。卡与 CTA 并存不互斥:卡回答「有什么渠道」,CTA 回答「怎么让数据来」;不做「零值卡被 CTA 顶替」(渠道面缺席)也不做「只出卡无 CTA」(动作引导丢失)。
- `catalogLoaded` 防闪门原样(`:3073`);活库常态 = 有源有条目,两态均不显。
- 错误:catalog 域错 → `FeedErrorCard`(`feed-error` 保留,`catalogSeqRef` 对票原样 `:1739`)。

## 2. 2 级:类型下全渠道列表

### 2.1 布局

- 根同 1 级满高列;头部工具条贴顶,主体 = 渠道行列表内滚。
- **v7 右栏 aside 整体升格为本级页面本体**(`feed-screen.tsx:3290-3385`):行列表容器 `max-w-3xl mx-auto w-full`(桌面 1920 下行长约 768px,Telegram 桌面列表密度;不再 288px 窄栏),`flex-1 min-h-0 overflow-y-auto py-1`(`feed-channel-list` testid 保留)。ChannelRow 组件复用,**渲染结构/交互零动**(`:1102-1204`:类型头像/两行形/未读徽标/选中高亮/Space 激活全保留);**唯一新增 prop = `statsScope: "loaded" | "full"`**(拷问 R1-Q4 裁定,见 §2.3——不加 prop 则徽标 title 词面在全库口径下撒谎,违 F2/R1 铁律;故「零改」承诺在此一处让步,components 其余面不动)。
- 脚注(列表尾,sticky 域外):「N 个渠道」/ 搜索时「命中 M / N 个渠道」——`feed-count` testid **随迁本级**(全屏恒单实例纪律不变,v7 R1-1 消歧延续:1 级无 feed-count,3 级条目计数独占 `feed-stream-count`)。

### 2.2 头部工具条(2 级)

`返回钮 + 类型词面 + 搜索框 + 刷新`:
- 返回钮 `data-testid="feed-back-to-types"`(ChevronLeft + 「类型」词;`onClick={backLevel}`;title「返回类型卡(Esc 同门)」)。
- 类型词面 `data-testid="feed-type-title"`:`TG 监控 · N 个渠道`(CHANNEL_CARD_META label)。
- 搜索框 = v7 右栏搜索位整体迁址(`feed-screen.tsx:3298-3327`),`feed-channel-search` testid 保留,`filterChannelsByQuery` 语义零改——**作用域 = 该类型成员集**(§4)。`searchInputRef` 随迁(Mod+F 落点,§7)。

### 2.3 数据与行为

- 行集 = `feedChannelCards(catalogItems, …)`(既有,枚举/排序零改)按 `card.kind === view.kind` 过滤 ∩ `filterChannelsByQuery`。**零条目渠道也出行**(health 枚举半边,`api.ts:808-811`);行统计 today/unread 优先取 sourceStats 行(全库诚实,§5.2),无行(零条目)= 0。
- **口径词面双面(拷问 R1-Q4 裁定)**:行内未读徽标 title 现为组件内硬编码「已加载口径:…更早条目未计入」(`feed-screen.tsx:1197` 实读)——sourceStats 覆写后数字已是全库真值,词面必须随行,否则同徽标数字与 title 互相拆台。方案 = ChannelRow 新增 `statsScope` prop:`"loaded"`(缺省,现词面,存量断言不破)/ `"full"`(「全库口径:未读 = 未标已读(store.source_stats 分源聚合),不限今日」)。L2 行集 stats 在场传 `"full"`,未过门回退传 `"loaded"`。**同根顺手补**:行预览 `card.latest` 只来自 catalog 首页 50,50 条外的活跃源(如 openai-news)会落「今日暂无新条目」假知会——`applySourceStats` 覆写时一并回填 `latestTitle/latestSeen`(§5.2),行预览在 card.latest 缺席时用 stats 的 latest_title + latest_first_seen 显一行(title 词,无 digest),消灭第二个假 0 面。
- 点击/Enter/Space = `openChannel(key)` → 3 级;行高亮 `selected` 语义 = 「上次从这里进入的渠道」改为**本级无持久选中**(进入 3 级即页面切换,回退不高亮;`data-selected` 属性保留恒 false,组件零改)。
- 空态:该类型零渠道(理论不达,类型卡以成员存在为前提)→ 行内知会词;搜索零命中 → `feed-search-empty` 行内小空态(v7 保留件,`feed-screen.tsx:3354-3359`)。

## 3. 3 级:渠道详情(深度测试重点级)

### 3.1 布局

**v7 左栏整体升格为全页**(`feed-screen.tsx:2662-3287`),机件零逻辑改动,仅导航语义换血:

- 头部工具条(`feed-toolbar` 保留):返回钮(3.2)+ 渠道名(`feed-stream-title`,channelDisplayName)+ 读态分段(未读/星标/稍后读/全部;**隐藏条件 = 历史态 OR 检索态**,拷问 R1-Q2:`!view.history && !streamSearchActive`,检索态隐藏 = v7 深检 F4「不给死控件」纪律同门,`feed-screen.tsx:2682-2684` 先例)+ 计数词面(`feed-stream-count`,F2 口径与 R1 修正词面原样 `:2723-2745`;检索态词面见 §4.3)+ 知会词(`feed-day-window`:「全量 · 新→旧 · 实时滚动」/ 历史态词,`:2749-2761`)+ 退出历史钮(`:2762-2773`,与检索正交,检索态保持可见)+ **渠道内检索框(新,§4.3)**+ 显示选项(`:2840-2887`)+ 刷新(`:2890-2900`,刷当前流)。
- TG 监控台条(`feed-tg-console` 六件 testid 全保留):落位 = 工具条下、滚动区外,**与 v7 同构**(`:2952-3037`);条件 `kind==="tg" && tgStatusPhase==="ok" && tgWebline!==null`;phase 机件/R2 无闪现/startWebLogin/内置浏览器预览(tgPreviewUrl 遍历 streamItems)/看全部历史消息(→ `openHistory`)**逐行原样**(`:2182-2204, 2415-2468`)。
- 时间线滚动区:错误卡(`feed-error`,stream 域对票 `streamSeqRef` 原样)→ 骨架(`feed-loading`,`:3149-3165`)→ 空态阶梯(`:3166-3248`,TG 三态/零条目 `feed-channel-empty`/读态过滤空 `feed-empty-history`,原样)→ 聊天气泡时间线(`feed-chat-timeline` + `feed-group-*` 日期胶囊,chatView 判定 = `channelCardKindOf(source, engine) === "tg"`,`:2168-2170`)/ 单列条目列表(`feed-stream-list`,`:3277-3279`)→ 加载更早(复合游标 + 判停,`loadMore` `:1910-1937` 原样,query 在途时同 WHERE 翻页,§4.3)。
- 详情弹窗 FeedItemDetail 零改(Portal/Esc/遮罩/弹开记已读/动作簇;`detailKey` 命中域 = streamItems,3 级才有条目,天然不出现在 1/2 级)。

### 3.2 返回与历史

- 返回钮 `data-testid="feed-back-to-channels"`(ChevronLeft + 上级类型名;`backLevel()` → 2 级同类型列表;title「返回渠道列表(Esc 同门)」)。替代 v7 `feed-back-to-overview`。
- 历史态:`openHistory`(读态豁免)入口 = 监控台「看全部历史消息」+ 空态「看全部条目」;`feed-history-exit` 退出——全件原样,历史态只存在于 3 级(1/2 级无历史概念,2 级行计数不受历史态影响,天然成立)。

### 3.3 深度测试焦点面(3 级检查员/验收员清单,⑦ 的主体)

① 时间线双形态(TG 气泡含日期胶囊与未读亮泡 / 网站单列);② 监控台四态(loading 无卡不闪[R2]/ok·监控中/ok·未登录扫码/error 重试卡)+ 预览置灰与失败注记;③ 历史态进出与读态豁免;④ 读态分段 × 计数词面(total/hasMore/回退三词面);⑤ 渠道内检索(命中/零命中/清空恢复/翻页携带 query/读态豁免语义);⑥ 加载更早(复合游标/判停/内联 loading);⑦ 空态阶梯全支;⑧ 键盘全键位(§7);⑨ 弹窗(Esc/遮罩/动作簇/焦点陷阱让位);⑩ 实时滚动(completed 事件/30s 轮询/mergeFreshItems 前插);⑪ 能力门回退(READ_STATE/COUNT/STATS 三门);⑫ 错误卡对票(stream 旧票不污染新渠道)。

## 4. ② 类型划分 + ④ 搜索

### 4.1 类型映射表(判定权威 = UI,单一词表)

| 类型卡 | 判定词表(次序即优先级) | 后端对应 | 仓内现存源(活库+yaml 实测) |
|---|---|---|---|
| **TG** | ① 源名前缀 `telegram-`/`tg-`(TELEGRAM_SOURCE_RE,`api.ts:602`)→ tg;② engine ∈ TG_ENGINES{tg_web, telegram, telethon, bot}(`api.ts:757`)→ tg | `source_kind="im"`(纯前缀 LIKE,`sqlite.py:904-905`) | telegram-mihomo_party_group(engine=telegram);telegram-durov(engine=static_html,**前缀优先后归 TG**) |
| **网站** | ①② 均未命中 → site(涵盖 static_html/direct_api/urlwatch/rss/searxng/crawl4ai/auto/credhunter 等全部其余 engine) | `source_kind="web"`(含 source NULL 条目,`sqlite.py:906-909`) | openai-news、cocoloop、hf-blog、aihot、deepmind/qwen/google/mistral/microsoft-blog、github-new-stars、cheapshark、steam-specials、epic-free、*-watch(urlwatch)等 17 源 |
| **日报** | engine ∈ DAILY_ENGINES{prompt, store_report}(`api.ts:760`)→ daily | **无后端词表**(UI 判;后端不增设,理由见 §5.4) | daily-digest(store_report);**ai-token-deals、ai-vendor-watch(prompt,`plugins/ai-token-deals.yaml:19`、`plugins/ai-vendor-watch.yaml:35` 实读)——拷问 R1-Q1 裁定归日报** |

- **归并理由(媒介优先,主人「从哪种渠道获取信息」口径)**:五档 channelKindOf 的 watch/deal/news 是**卡面呈现分档**(变更徽标/价格行/新闻列表),载体全是网页——L1 类型回答媒介问题,故 watch/deal/news 归并进「网站」;**L3 条目卡呈现仍用五档**(`renderCard` 的 `kind=channelKindOf`,v7 `feed-screen.tsx:2292` 原样)——两层词表各司其职,类型管导航,呈现档管卡面,互不替代。
- **prompt 源归日报的裁定(拷问 R1-Q1,词表是权威)**:`engine: prompt` = LLM 生成引擎(prompt.yaml `engine_options.prompt.instructions` 驱动生成),非采集引擎——ai-token-deals(linux.sb 优惠 AI 汇总)与 ai-vendor-watch(厂商动态 AI 日报)本质是**生成型汇报**,与 daily-digest 同档;既有断言已锁定此语义(`feed-screen.test.tsx:3812` `channelCardKindOf("ai-vendor-watch","prompt") → "daily"` 实读,五档 channelKindOf document 档同门 `api.ts:628`)。首稿事实底座「日报 1 源」系归并笔误,以词表为准改 3 源,**DAILY_ENGINES 词表与既有断言零改动**。后果如实接受:日报卡渠道数 = 3,首条预览可能是 ai-token-deals(成员源 latest 最新者)——卡面预览行自带渠道名(§1.2),不构成误导;若主人验收时观感不适,处置是词表细分(如 prompt 优惠汇总另立档)而非本批拍脑袋归网站,留档不预设。
- **微信/飞书**:仓内零源,不设卡不预占位(类型以现存源划分,主人定调)。扩展路径预留:ChannelCardKind 增档 + 同款 engine 集合 + CHANNEL_KIND_ALIASES 词条 +(可选)后端 source_kind 词表扩展;扩展前 UI 不猜。
- 零条目渠道归属:health 枚举半边(engineBySource)给 engine → 词表判型;纯条目侧发现(health 失败/插件已卸)退化前缀判定(engine 空 = 前缀判,`api.ts:772` 原样)。health 整体失败:daily 档不可判,类型退化二分(TG/网站),日报卡缺席如实(与 v7 同退化面)。

### 4.2 判定次序修正(本批必改,防类型漏判)

现 `channelCardKindOf` **engine 先于前缀**(`api.ts:768-774`):telegram-durov(engine=static_html,t.me 公开镜像采集线)被判 site——与后端 `source_kind="im"` 纯前缀词表矛盾,2 级列表里 TG 频道混进网站。改为**前缀优先**:`TELEGRAM_SOURCE_RE.test(source)` 先判 → tg;再 DAILY_ENGINES → daily;再 TG_ENGINES;其余 → site(与五档 channelKindOf 前缀优先同门,`api.ts:624-625`)。波及面:2 级行头像/3 级 chatView/监控台判定(isTgChannel)对 durov 类源翻正(聊天时间线 + 监控台条,媒介正确);api 纯函数用例补「telegram-durov + static_html → tg」断言,存量断言逐条核(既有 engine 命中 TG 的用例不变绿→绿)。

### 4.3 搜索矩阵(④:在哪几级、匹配什么)

| 级 | 载体 | 匹配什么 | 通路 |
|---|---|---|---|
| 1 级 | `feed-type-search` | 类型名 + 别名(含前缀命中:搜「Tg」直出 TG 卡) | 客户端 `filterTypesByQuery`(新纯函数,词表同 CHANNEL_KIND_ALIASES) |
| 2 级 | `feed-channel-search` | 渠道名(label)/源 id(key)包含匹配 + 类型别名,v6 AC21/v7 语义 | 客户端 `filterChannelsByQuery`(`api.ts:863-875` 零改),作用域 = 该类型成员 |
| 3 级 | `feed-stream-search`(新) | 该渠道内 title/content 全文(服务端 LIKE 三列,source 精确等值同 WHERE) | **服务端**:`fetchFeedPage` 重挂 `query` 参透传(共享客户端 `types.ts:425` 与后端 `sqlite.py:920-929` 全在,封装层一行);检索态 = 显式全量——绕过读态过滤(v6.1 全库检索语义平移,新→旧全量直出),词面「检索中 · 渠道内全量(不限读态)」;清空恢复读态视图;翻页游标与 query 同 WHERE(`loadMore` 传 query),检索态下「加载更早」照常 |

- **检索态 × 读态分段并存形态(拷问 R1-Q2 裁定 = 隐藏,不失效不叠加)**:检索态下读态分段**整体隐藏**(§3.1),`visible` 计算的读态豁免与历史态同门(`streamSearchActive` 加入豁免位)。理由:①(b) 可见但失效违反 v7 深检 F4「不给死控件」纪律(`feed-screen.tsx:2682-2684` 历史态先例);②(c) 叠加生效则词面「不限读态」撒谎,且 total(source+query 同 WHERE,无读态变量)与分段过滤口径互斥。历史退出钮与检索正交(历史态中检索合法:两者都是全量豁免,无冲突);清空检索词 → 分段即时恢复。深度测试预期(§3.3⑤)据此可判定:检索态断言「分段不存在」+「未读条目在检索命中中可见」+「清空后分段回归且未读过滤生效」。

- 1/2 级搜索词各自独立(不跨级携带);3 级检索词随渠道切换清空。Esc 在输入框内 = 清词(v7 既有守卫,`feed-screen.tsx:3313-3319` 同门)。
- 检索零命中:3 级滚动区行内空态 `feed-stream-search-empty`(独立 testid,防与 2 级 `feed-search-empty` 混)。

## 5. ③ 数据接线(每级查询 / 统计诚实方案 / 后端动不动)

### 5.1 每级查询一览

| 级 | 查询 | RPC | 时机 |
|---|---|---|---|
| 1 级 | 全库铺底首页 50(withTotal) | store.items(既有 fetchFeedPage 零 source) | 挂载即拉;completed/cron.completed + 30s 可见性轮询保活(v7 双域事件挂载 `:1703-1839` 改挂 catalog 域,原样) |
| 1 级 | 分源统计(新) | **store.source_stats**(新 RPC,§5.4) | 挂载即拉;与 catalog 同触发面双刷;windowStart 60s 滴答跨窗重拉(今日数随窗翻面) |
| 1 级 | engine 词表 | health() | 挂载一次(v7 `:1652-1665` 原样) |
| 2 级 | **零新查询** | —(catalog + sourceStats + health 复用,纯客户端过滤) | — |
| 3 级 | 渠道条目流(source=) | store.items(既有 refreshStream/loadMore,`feed-screen.tsx:1751-1782, 1910-1937` 原样) | 进入 3 级即拉;实时双刷(catalog + stream)原样 |
| 3 级 | TG 状态(TG 渠道) | telegram.status | isTgChannel 翻转时(v7 phase effect `:2185-2204` 原样,deps 含 isTgChannel——v2.1 教训不破) |
| 3 级 | 渠道内检索 | store.items(source= + query=) | 防抖 300ms/Enter(v7 防抖机件同门) |

### 5.2 1 级类型卡统计怎么来才诚实(核心问题)

**现状口径的不诚实点**:今日/未读若从 catalogItems(全库首页 50)聚合,openai-news 单源日增百条即可把首页吃满——TG/日报类型的「今日 0 条」是**截断假象**而非事实(v7 ChannelRow/总览统计 title 自认「已加载口径」,但那是流明细可翻页的口径;类型卡是聚合终值,没有「再翻页」动线,假 0 不可接受)。渠道数无此问题(health 枚举完整)。

**为何 with_total(协议 13)不够**:`with_total` = 同 WHERE 全量计数(`count_items`,`sqlite.py:972-999`),要凑出类型卡的今日/未读得按「类型 × 指标」发多次查询(since=窗锚 × source_kind=im/web …)——且**日报类型无后端词表**(§4.1),source_kind 路线对 daily 根本无参可传;N 次 RPC 换一个仍不完整的答案,不如一次分源聚合直答。

**方案(动后端,一 RPC 直答)**:新增 `store.source_stats` 分源聚合,一条 SQL 出全库真值,UI 按类型归并:

```sql
SELECT source,
       COUNT(*)                                          AS total,
       SUM(CASE WHEN first_seen >= :since THEN 1 ELSE 0 END) AS today,
       SUM(CASE WHEN COALESCE(read,0) = 0 THEN 1 ELSE 0 END) AS unread,
       MAX(first_seen)                                   AS latest_first_seen
FROM items GROUP BY source
-- latest_title 二遍取每源最新一条 title(关联子查询;仅 21 行,成本可忽略)
```

- 参数 `{since?: ISO, db?}`:since = UI 传当日窗锚 `dayWindowStart().toISOString()`(03:00 窗锚与视图同源,`api.ts:958-970`;省略 = today 全 0,「无窗无今日」如实);应答 `{rows: [{source: string|null, total, today, unread, latest_first_seen, latest_title}]}`。
- 语义对齐:unread = 未标已读(与 feedChannelCards 既有 unread `api.ts:829` 同义,不含 later 到期重现加成);today = 窗内条数(不含 isLaterResurface 加成——重现条目极少数且多为已读,偏差面如实注记在 api 纯函数测试注释)。source NULL 行(活库 0 条,schema 允许)计数**归入「网站」卡的 today/unread,不计渠道数**(它不是渠道);卡 title 注明含无源条目。
- UI 消费:新纯函数 `aggregateTypeCards(channelCards, statsRows, …) → TypeCardData[]`({kind, label, channels, today, unread, previews[3]};previews = 成员源按 latest_first_seen 降序取 3 的 {channelLabel, latestTitle, firstSeen})+ `applySourceStats(cards, statsMap)` 把 2 级行的 today/unread 覆写为全库值,**并回填 `latestTitle/latestSeen`**(拷问 R1-Q4 同根面:catalog 首页 50 外的活跃源,行预览在 `card.latest` 缺席时用 stats 值显一行,消灭「今日暂无新条目」假知会,§2.3);未过门/应答缺失 → 回退 catalog 已加载口径(现 v7 行为)+ title 词面如实(1.2,ChannelRow `statsScope="loaded"` 缺省档)。

### 5.3 双缓冲与读态(v7 机件原样保留)

- catalogItems(1/2 级聚合)/ streamItems(3 级流)拆分、双票守卫(catalogSeqRef/streamSeqRef)、statesFromItems 双缓冲并集投影 + localStorage 回退、flipItem 双写、markAllRead 只翻 catalog、onEnriched 只写 stream——**全部原样**(`feed-screen.tsx:1632-1641, 1956-1998` 等,§6 不逐条重列)。
- 唯一增量:markChannelRead(U 键渠道级标读,v7 `:2087`)在 2 级行环继续可用(§7);其乐观翻写已走 flipItem 双写,零改。

### 5.4 能力门与后端改动清单(允许动,逐件给方案)

| 件 | 改动 | 文件 |
|---|---|---|
| `store.source_stats` RPC | 新方法 + 方法表注册;`since` 非法 ISO → `invalid_params`(同 `_parse_iso` 门,`entry.py:1672-1679`);SQL 见 §5.2 | `src/myssia/store/sqlite.py`(新方法 source_stats)、`desktop/entry.py`(`_m_store_source_stats` + `"store.source_stats": …`) |
| 协议版本 | `PROTOCOL_VERSION = 13 → 14`(注释行 v14 注记,先例 `entry.py:506-510`);UI 常量 `STATS_PROTOCOL = 14` + 探测(v7 `:1680-1700` 同一次 version 应答顺带置门,零新 RPC) | `entry.py:511`、`feed/api.ts` |
| 回退语义 | 未过门(旧 sidecar 无此方法 / protocol<14)= 客户端 catalog 口径 + title 如实;**不发 RPC 试错**(门先行,COUNT_PROTOCOL 同模式) | `feed/api.ts` + `feed-screen.tsx` |
| fetchFeedPage 重挂 query | `FeedPageRequest + query?: string|null` → `api.storeItems({query})` 透传 | `feed/api.ts:23-59` |
| 共享客户端 | `client.ts + storeSourceStats`;`types.ts + SourceStatsParams/SourceStatsResult`(storeStateMarkAll 先例 `client.ts:220`) | `lib/api/client.ts, types.ts` |
| **不动** | fetchFeedPage 的 source_kind/category 参**不重挂**——三级 IA 无「按类型查条目」动线(L1 聚合走 source_stats 一次直答,L2 是渠道枚举非条目查询);后端两参保留不删(协议面既存,词表漂移风险零) | — |
| **不动** | daily 类型无后端词表:后端不做类型过滤(两套词表必漂移),类型归并唯一权威 = UI engineMap + 前缀(§4.1) | — |

## 6. ⑥ 撤除面:v7 双栏逐项收编清单

| v7 现件(位置) | v8 去向 |
|---|---|
| 右栏 aside 整体:搜索框+ChannelRow 列表+脚注(`feed-screen.tsx:3290-3385`) | **= 2 级页面本体**;ChannelRow 复用(渲染结构/交互零动,唯一 prop 让步 `statsScope`,拷问 R1-Q4,§2.1),搜索迁 2 级头(`feed-channel-search` 保留),脚注 `feed-count` 迁列表尾 |
| 左栏工具条(`:2662-2944`) | **= 3 级工具条**;总览钮→返回钮(3.2);读态分段/计数/知会词/历史退出/显示/刷新全件随迁 |
| 批量标已读/未读 + 导出组(总览态分支 `:2774-2836, 2901-2942`) | **迁 1 级头部**:导出与批量入口进 ⋯ 溢出菜单,二次确认簇渲染在头部菜单外兄弟位(拷问 R1-Q3 裁定,§1.4——Radix 菜单项点击默认关菜单 × 簇 onBlur 失焦取消 `:2802-2812`,「迁入菜单内」物理不成立);全库语义在 1 级语境更实 |
| 总览引导空态统计行/首跑/CTA(`:3068-3145`) | **迁 1 级卡墙落地位**(1.5);统计行退役(数字由类型卡承载),`feed-overview`/`feed-overview-stats` testid 退役,`feed-first-run`/`feed-run-cta` 保留迁位 |
| TG 监控台条(`:2952-3037`) | **= 3 级专属**(工具条下同构落位);1/2 级不出(登录态是账号级,入口归 3 级 TG 渠道详情,主人 v8 定调「3 级…TG 含监控台」);phase/R2/预览逻辑逐行原样 |
| 双环键盘 navPane/list+item 环/Shift+J·K 层(`:2237-2239, 2609-2635`) | **退役**;三级互斥页面 = 三层单环(§7),Shift 层语义消亡(3 级 j/k 直属条目,恢复 v7 前 v6 旧语义) |
| `feed-back-to-overview`(`:2665-2677`) | 改名两件:2 级 `feed-back-to-types` / 3 级 `feed-back-to-channels` |
| Esc 清选中回总览(`:2558-2568`) | 改为 **Esc 回上一级**(3→2→1);弹窗守卫(`:2532`)+ 浮层 defaultPrevented 收口(`:2520`)+ menu-in-place 守卫(`:2564` `[role="menu"]` 探测)三道原样随迁——Esc 分支仍在弹窗守卫**之后**(复审铁律延续) |
| scope {source, history}(`:1552-1557`) | 替换为 FeedView 三态(§0);overviewMode 派生量退役,各级以 view.level 分叉 |
| keyStateRef 实时状态镜(`:2484-2513`) | **保留模式**,镜像面改三层(view/typeCurrent/listCurrent/itemCurrent/detailKey/各环可见集/各动作);mount-once effect 写法原样(真机 4ms 键序实证教训,勿回退) |
| R1(计数词面)/R2(监控台 phase)修复成果 | 随工具条/监控台条迁移保留,回归用例不撤 |

## 7. ⑤ 返回链与键盘语义(终案)

返回链:**3 →(Esc/返回钮)→ 2 →(Esc/返回钮)→ 1**;详情弹窗开着 Esc 只关弹窗(Radix 自 handling,守卫在先);浮层(菜单/下拉)在场 Esc 归浮层(三道守卫随迁,§6)。无路由,浏览器侧无历史栈语义(与 v6/v7 一致,屏内 state)。

| 键 | 1 级 | 2 级 | 3 级 |
|---|---|---|---|
| `j`/`k`(↑/↓ 同效) | 类型卡环(typeCurrentKey;3 卡边界钳制不回绕) | 渠道行环(listCurrentKey;v7 机件原样:`:2609-2641` 边界钳制/未选中 j 落首 k 落末/scrollIntoView 最近侧/环仅键盘巡游呈现) | 条目环(itemCurrentKey;同机件,集合 = displayItems) |
| `Enter` | 开当前类型卡 → 2 级 | 开当前行渠道 → 3 级 | 开当前条目详情弹窗 |
| `U` | 无操作 | 当前行渠道已加载条目一键标已读(v7 markChannelRead + 在场校验 `:2579-2591` 原样;range = 已加载口径 title 如实) | 当前条目已读/未读切换(toggle 原样) |
| `Esc` | 清搜索词(焦点在框内,框守卫);其余 no-op | 回 1 级 | 回 2 级 |
| `Mod+F` | 聚焦类型搜索并全选 | 聚焦渠道搜索 | 聚焦渠道内检索框(三级各自 ref,keyStateRef 镜 view.level 取落点;弹窗开着让位 `:2524-2526`) |
| `Space` | 卡根按钮激活(ARIA) | 行激活(v7 既有 `:1145-1156`) | — |
| 弹窗/浮层开着 | 全部让位(守卫三道,§6) | 同左 | 同左 |

- 守卫白名单键集:`u/j/k/enter/escape` + Mod+F(`:2533-2541`);输入框/textarea/select/contentEditable 不触发;Enter 命中 button/a 归原生——全部原样。
- hover/focus 置环 + 清 navByKeyboard(v7 onCurrentRow/onCurrentCard `:2243-2255` 按级复制为三件)。

## 8. testid 影响清单

| testid | 处置 |
|---|---|
| `feed-types-wall` / `feed-type-card-<kind>` / `feed-type-search` / `feed-type-title` / `feed-back-to-types` / `feed-back-to-channels` / `feed-stream-search` / `feed-stream-search-empty` | **新增** |
| `feed-channel-list` / `feed-channel-row-<key>` / `feed-channel-unread-<key>` / `feed-channel-search` / `feed-count`(2 级脚注)/ `feed-search-empty` / `feed-channel-loading` | **保留迁 2 级**(组件/容器原样,落位换页) |
| `feed-toolbar` / `feed-stream-title` / `feed-stream-count` / `feed-day-window` / `feed-history-exit` / `feed-confirm-all-group`(迁 1 级菜单)/ `feed-loading` / `feed-error` / `feed-tg-console*` 六件 / `feed-tg-status-unknown` / `feed-channel-empty` / `feed-empty-history` / `feed-chat-timeline` / `feed-group-*` / `feed-flat-list` / `feed-stream-list` / `feed-item-*` / `feed-tg-bubble-*` / `feed-detail-*` / `feed-export-result` / `feed-open-error` / `feed-mark-error` / `feed-first-run` / `feed-run-cta` / FeedCard 内部件全套 | **保留**,落位随 §1/§2/§3 |
| `feed-back-to-overview` / `feed-overview` / `feed-overview-stats` / `feed-search-scope`(词面拆入 2 级搜索注与 3 级检索注,单 testid 退役) | **退役** |

## 9. ⑦ 测试与冒烟随动清单

- **api 纯函数(feed/api.ts 用例)**:① channelCardKindOf 前缀优先(telegram-durov+static_html→tg;mihomo+telegram→tg;daily-digest+store_report→daily;**ai-token-deals/ai-vendor-watch+prompt→daily,拷问 R1-Q1 词表权威,与既有断言 `feed-screen.test.tsx:3812` 同门**;无名源+无 engine→site);② aggregateTypeCards/applySourceStats(stats 覆写/缺失回退/NULL source 行归网站不计渠道数/**latestTitle·latestSeen 回填与行预览回退**);③ filterTypesByQuery(别名/前缀/空串);④ fetchFeedPage query 透传。
- **feed-screen.test.tsx(145 例迁移)**:①1 级——类型卡渲染(渠道数/今日/未读/预览/竖版 min-h 锚)/卡点击→2 级/搜索过滤/溢出菜单导出与批量/**确认簇兄弟层动线(菜单项点击→菜单关→头部确认簇在场→确认执行;失焦取消,拷问 R1-Q3)**/空态三支判定链(零源首跑/CTA、**有源零条目 = 零值卡 + CTA 卡并存**,拷问 R1-Q5)/catalogLoaded 防闪;②2 级——原右栏行断言改落点(行形/徽标/选中高亮/零条目行/搜索零命中/脚注计数)/**statsScope 双词面(full 真值词/loaded 缺省词,拷问 R1-Q4)+ 50 条外源行预览 stats 回退**/返回钮→1 级;③3 级——原左栏断言改落点(时间线双形态/监控台四态含 R2/历史态/计数词面 R1/加载更早/空态阶梯/弹窗);④返回链 3→2→1 双跳与 Esc 链(含弹窗让位/浮层守卫);⑤stats 门过/未过双口径词面;⑥键盘三层(j/k 各级环/Enter/U/Esc/Mod+F 落点);⑦3 级检索(命中/零命中/清空/翻页携带/**检索态读态分段隐藏 + 未读命中可见 + 清空恢复过滤**,拷问 R1-Q2)。目标:全量 ≥145 例且全绿,存量断言只改落点不删语义。
- **pytest**:①新 `tests/store/test_store_source_stats.py`(分组聚合/today 窗锚/unread read=0/NULL source 行/空库/since 非法);②`tests/desktop/test_desktop_sidecar_protocol.py` 加 source_stats 参数校验与 PROTOCOL_VERSION=14 断言(存量 13 断言随 bump 核改);③存量 store/desktop 套件防回归全跑。
- **冒烟**:`desktop/scripts/feed-card-smoke.py`(381 行,v7 双栏锚)重写三级动线:L1 三卡直出 → 搜「Tg」TG 卡独显 → 点 TG 卡 → 2 级行列(mihomo 行在场,openai/daily 不在)→ 点行 → 3 级聊天气泡(`feed-chat-timeline`)+ 监控台/`feed-stream-count` → 点条目弹窗 → Esc→2→Esc→1;退役 testid 零命中清单随 v7 先例(`:238`)更新。`tg-card-smoke.py`(设置页)不受影响。
- **门禁照旧**:build / feed vitest / pytest desktop+store / 无头冒烟 + 换装双实锤(新 chunk 旧件零命中)+ WKWebView 缓存清 + app 还常驻 + 入库。

## 10. 实施顺序建议(给重构师)

0. **前置门(拷问 R1-Q6)**:Q6 的 1 级头部例外面(刷新+⋯菜单)经主人追认后方可动工;追认砍则按 §1.4 让步案执行,后续步骤不变。
1. **后端地基**:sqlite.source_stats + entry.py 注册 + PROTOCOL_VERSION 14 + pytest——不动 UI 先绿。
2. **api 层**:STATS_PROTOCOL/SourceStats/fetchSourceStats/aggregateTypeCards/applySourceStats/channelCardKindOf 前缀优先/fetchFeedPage query——纯函数用例随写。
3. **视图态换血**:FeedView 三态 + 三级根骨架(先全量平铺旧件:1 级空墙 + 2 级行列表 + 3 级左栏件升格),测试落点迁移到「位置正确」。
4. **1 级 TypeCard + 头部件**:卡形/聚合/搜索/溢出菜单/空态。
5. **2 级**:返回钮/类型词面/搜索迁址/脚注。
6. **3 级**:工具条改血(返回/检索框)/监控台与时间线落位复核。
7. **键盘三层** + Esc 链(守卫三道随迁)。
8. **测试/冒烟重写**(§9)→ 门禁全绿 → 换装入库。

每步独立可绿;AC29-32 验收动线 = 「进情报流见类型卡瀑布流 → 搜 Tg 直出 TG 卡 → 点卡见渠道列表 → 点渠道见时间线(TG 带监控台)→ 点条目出弹窗 → Esc Esc Esc 回 1 级」。

## 11. 拷问第 1 轮裁决记录(v8.1 修订,2026-10-10)

| 问 | 裁决 | 落点 |
|---|---|---|
| Q1 类型划分矛盾(ai-token-deals/ai-vendor-watch engine=prompt) | **词表是权威**:prompt = 生成引擎,两源归「日报」档;首稿事实底座「日报 1 源」系归并笔误。DAILY_ENGINES 与既有断言(`feed-screen.test.tsx:3812`)零改动;活库口径改 = TG 1 / 网站 17 / 日报 3;日报卡预览可能首现 ai-token-deals,预览行自带渠道名不误导(词表细分留档不预设) | 事实底座、§4.1 表+裁定注、§9 用例 |
| Q2 检索态 × 读态分段 | **(a) 检索态隐藏分段**(v7 深检 F4「不给死控件」同门);分段隐藏条件 = 历史态 OR 检索态;历史退出钮与检索正交;深度测试预期三断言写死 | §3.1、§4.3、§9⑦ |
| Q3 确认簇迁入菜单物理不成立 | **菜单项发起、确认簇渲染在头部菜单外兄弟位**(簇代码原样,渲染宿主换位;Radix 关菜单 × onBlur 取消 `:2802-2812` 实锤);Esc 全局收口在 1 级可达零新守卫 | §1.4、§6 |
| Q4 ChannelRow「零改」× 词面如实 | **加唯一 prop `statsScope: "loaded"|"full"`**(徽标 title 双词面);同根补 stats 的 latestTitle/latestSeen 回填(50 条外源行预览假知会消灭);「零改」承诺收敛为「渲染结构/交互零动」 | §2.1、§2.3、§5.2、§9 |
| Q5 有源零条目态优先级 | **三态判定链写死**:零源 → 首跑/CTA 替代卡墙(v7 分叉原样);**有源零条目 → 零值卡墙 + CTA 卡并存**(卡答「有什么渠道」,CTA 答「怎么让数据来」) | §1.5、§9① |
| Q6 1 级头部 5 控件 vs AC29 | **推荐追认现稿**(刷新+⋯菜单共 2 视觉位;v6 AC23 工具能力归位是主人已验收;3 级渠道语境下全库钮范围不实);**待主人点头后方进 §10 第 0 步**;让步案 = 头砍到只剩搜索+刷新,批量/导出 v8 缺席待点名 | §1.4 追认注、§10 前置门 |
