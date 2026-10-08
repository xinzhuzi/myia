# Design:TG 渠道卡(流内聚合 + 顶部渠道卡区)

## 0. 现状锚点

- 三级下钻(10-06-feed-channel-groups)已在:`FeedScreen.drill` = L1 品类列表 / L2 渠道列表 / L3 消息流;source 作用域 L3(渠道详情)**已存在**且呈现完好(面包屑 + telegram 气泡卡 + 分页)。
- 渠道判定:`channelKindOf(item, engineBySource)`(api.ts:657,telegram = 源名 `^(telegram|tg)[-_.]` 前缀);频道显示名:`channelDisplayName`(feed-screen.tsx:127)。
- 本特征 = 纯前端:**新增一层流内聚合呈现**,后端 `store.items` category/source 独立可选已支持跨品类渠道流(entry.py:1680-1689 已核)。

## 1. 数据层(api.ts 新增纯函数)

```ts
export interface TelegramChannelCard {
  key: string;            // 源名全称(items.source,drill 作用域键)
  label: string;          // 频道显示名(去 telegram- 前缀;与 channelDisplayName 同规约)
  count: number;          // 可见条数(当前过滤 ∪ 当日窗)
  unread: number;         // 其中未读数
  latest: FeedItem;       // 最新一条(first_seen 最大;预览与时间源)
}
export function telegramChannelCards(items: FeedItem[], states: FeedStateMap): TelegramChannelCard[]
```

- 聚合键 = `item.source`(telegram 判定复用 `channelKindOf(item).kind === "telegram"`,不重复写前缀正则)。
- 排序:latest.first_seen 降(聊天列表惯例;null first_seen 沉底),稳定同序 tiebreak。
- 纯函数零副作用,便于 vitest 直测。

## 2. 视图层(feed-screen.tsx)

- **派生**:`displayItems` 之后——
  - `kindByItem = useMemo`(streamItems 逐条 channelKindOf;与 renderCard 同源词表);
  - `tgCards = useMemo(telegramChannelCards(displayItems, states))`;
  - `streamItems = displayItems` 中 kind ≠ telegram 的条目(消息列表本体)。
- **渲染**(仅多渠道作用域 = `drill.level===3 && drill.source===null`;source 作用域即详情本身不聚合):
  - 列表区顶部新增「TG 频道」区(`data-testid="feed-tg-channels"`):小节头(N 个频道,样式对齐时间组头但非 sticky)+ 渠道卡列;
  - **TelegramChannelCard**(feed-screen 内新组件):左缘未读 accent 竖条(M>0)+ `Send` 图标 + 频道名 + 右侧最新相对时间;第二行最新一条预览(单行 truncate,`latest.title || latest.url`);第三行 `今日 N 条 · 未读 M`(title 注记「口径 = 当前视图 ∪ 当日窗可见条目」)+ chevron;hover 语言对齐 drillRow(border-primary/40 + bg-accent/40);
  - `data-testid="feed-tg-channel-card-<source>"`,点击 → `setDrill({level:3, category:<当前流品类>, source:key})`。
- **消息列表本体**改吃 `streamItems`:时间分组 `groups` 从 streamItems 派生(「今天 X 条」如实反映列表);空态门从 `visible.length===0` 改为 `streamItems.length===0 && tgCards.length===0`(AC4)。
- **工具条计数**:`{visible.length} / {items.length} 条`保持条目口径不变(渠道卡区自带计数,不重复)。
- **j/k 巡游**(AC5):keys 源从 `displayItems` 改为 `streamItems`(U 键 toggle 同源);TG 卡不渲染即不参与。
- **面包屑回流**(AC2):source 作用域且 category===null 时,插入中间层面包屑「全部条目」→ 回 `{level:3, category:null, source:null}`(现有 backToL2 在 category null 时落到 L1,不符本次动线)。

## 3. 兼容与风险

- **状态三通路**:server/local 读态经 `states` 传入聚合函数,两通路同语义;乐观翻转 → 未读数即时变化(markItemState 已改 items,派生自动)。
- **实时滚动**:liveRefresh 前插新条目 → tgCards 派生刷新(计数/预览/排序),零新订阅。
- **搜索/导出/批量**:不受影响(export 在 source 作用域照旧隐藏;mark_all 语义不变)。
- **回归面**:feed-screen.test.tsx 中给 L3 流播种 telegram 条目并断言内联气泡的用例需迁移——气泡断言改为在**渠道详情**(source 作用域)下成立;新增渠道卡区断言。
- **风险等级**:LOW-MEDIUM。单屏内改渲染管线派生链,不动 api 门面/sidecar 协议/其他屏;gitnexus impact 在实施前对 FeedScreen 跑一次留档。

## 4. 回滚

单 commit;回滚 = revert 该 commit(无数据迁移、无协议变化、无本地存储键变化)。
