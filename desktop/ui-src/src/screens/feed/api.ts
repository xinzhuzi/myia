/**
 * 情报流数据装配(本屏私有 api 模块;共享客户端 @/lib/api 只读不动)。
 *
 * 数据面 = sidecar 协议 store.items(SQLiteStore.list_items 直读,新→旧,
 * 见 entry.py `_m_store_items` / store/sqlite.py `list_items`);服务端搜索
 * query(G1,10-03-feed-ux)随游标全程透传 —— 搜索覆盖已加载页之外的
 * 全库数据,协议级而非本地过滤。
 *
 * 翻页游标(v1.1.2 桌面对齐批 C1,与 feed-ux G1 合流形状):复合游标
 * `(before, before_id)` = 上页最旧条目的 `(first_seen, id)` —— 同刻条目
 * 超单页 limit 也能推进直至取尽(旧「since 复用 + 客户端去重 + added==0
 * 判停」的卡死边界已修)。客户端 dedup 与 added==0 防御判停保留为兜底。
 */
import { invoke } from "@tauri-apps/api/core";

import { api, SidecarRequestError } from "@/lib/api";
import type { FeedItem, HealthResult, SidecarErrorShape } from "@/lib/api";

/** 单页条数(与卡片瀑布一屏量级匹配) */
export const FEED_PAGE_SIZE = 50;

/** 翻页请求:cursor = 上页最旧条目的 (first_seen, id) 对(首页两键皆 null) */
export interface FeedPageRequest {
  cursor: string | null;
  /** 复合游标第二键(与 cursor 同源:同刻条目翻页不跳不重) */
  cursorId: number | null;
  pageSize?: number;
  /** 品类过滤(null = 不传参 = 全部品类;10-06 三级下钻:L3 品类作用域) */
  category?: string | null;
  /** 源名过滤(null = 不传参;10-06-feed-channel-groups:L3 渠道作用域,
   *  store.items source 精确等值) */
  source?: string | null;
  /** 源大类过滤(null = 不传参;10-08-tg-channel-card v2 卡片墙第二层,
   *  仅过 SOURCE_KIND_PROTOCOL 门才传) */
  sourceKind?: "web" | "im" | null;
  /** 服务端搜索词(G1:title/content/source 三列 LIKE NOCASE,随游标透传) */
  query?: string | null;
}

export interface FeedPage {
  /** 服务端原始返回(新→旧;边界条目由 appendFeedPage 去重兜底) */
  items: FeedItem[];
  /** 服务端返回数达到 limit → 可能还有更旧条目(判停 = 返回数 < limit) */
  hasMore: boolean;
  /** 下页游标 = 本页最旧条目的 (first_seen, id)(空页为 null) */
  nextCursor: string | null;
  nextCursorId: number | null;
}

export async function fetchFeedPage(request: FeedPageRequest): Promise<FeedPage> {
  const pageSize = request.pageSize ?? FEED_PAGE_SIZE;
  const result = await api.storeItems({
    limit: pageSize,
    ...(request.cursor
      ? { before: request.cursor, ...(request.cursorId !== null ? { before_id: request.cursorId } : {}) }
      : {}),
    ...(request.category ? { category: request.category } : {}),
    ...(request.source ? { source: request.source } : {}),
    ...(request.sourceKind ? { source_kind: request.sourceKind } : {}),
    ...(request.query ? { query: request.query } : {}),
  });
  const items = result.items;
  const oldest = items.length > 0 ? items[items.length - 1] : null;
  return {
    items,
    hasMore: items.length >= pageSize,
    nextCursor: oldest?.first_seen ?? null,
    nextCursorId: oldest?.id ?? null,
  };
}

// ---------------------------------------------------------------------------
// 屏内品类下拉(10-04-topbar-cleanup:品类过滤从全局顶栏拆下归位 feed 屏;
// 词汇源沿用顶栏旧路 = health().plugins,与 store.items 的 category 精确
// 等值同口径 —— 入库时条目记 config.id(pipeline.py `category=self.config.id`),
// 选项 value 即 plugin.id,label 显名称)
// ---------------------------------------------------------------------------

/** 品类下拉选项(id = 服务端过滤词;label = 回显名) */
export interface FeedCategoryOption {
  id: string;
  label: string;
}

/**
 * health().plugins → 品类下拉选项:id 去重(目录内同 id 多文件时首现优先)
 * + 名称回显(name 缺省回 id);装不上的插件 id=null 不入选项(选了也无数据
 * 可滤);排序稳定(id localeCompare)。与旧顶栏下拉同构(拆下归位零语义变化)。
 */
export function categoryOptionsFromHealth(plugins: HealthResult["plugins"]): FeedCategoryOption[] {
  const seen = new Map<string, string>();
  for (const plugin of plugins) {
    if (plugin.id && !seen.has(plugin.id)) {
      seen.set(plugin.id, plugin.name ?? plugin.id);
    }
  }
  return [...seen.entries()]
    .map(([id, label]) => ({ id, label }))
    .sort((a, b) => a.id.localeCompare(b.id));
}

// ---------------------------------------------------------------------------
// 导出当前视图(G3,10-03-feed-ux):dialog.save 选路径 → sidecar 直写;
// 打开原文的 URL 门(G2):仅 http(s) 走 plugin-shell open
// ---------------------------------------------------------------------------

/** 打开原文的 URL 门(G2):仅 http(s) 渲染「打开原文」(capabilities 同门) */
export function isOpenableUrl(url: string | null | undefined): boolean {
  if (!url) return false;
  try {
    const parsed = new URL(url);
    return parsed.protocol === "https:" || parsed.protocol === "http:";
  } catch {
    return false;
  }
}

/** 导出格式选择(与 feed.export params.format 同词表) */
export type ExportFormat = "jsonl" | "csv";

/** 默认文件名:myssia-feed-YYYYMMDD.<ext>(本地日期,与导出按钮同日可见) */
export function defaultExportName(format: ExportFormat, now: Date = new Date()): string {
  const pad = (value: number) => String(value).padStart(2, "0");
  const date = `${now.getFullYear()}${pad(now.getMonth() + 1)}${pad(now.getDate())}`;
  return `myssia-feed-${date}.${format}`;
}

/** 保存对话框形状(= @tauri-apps/plugin-dialog save 的参数;注入以便测试) */
export interface SaveDialogFn {
  (opts: {
    defaultPath: string;
    filters: { name: string; extensions: string[] }[];
  }): Promise<string | null>;
}

export interface ExportOutcome {
  /** 用户在系统保存对话框取消 = null(不是错误) */
  path: string | null;
  count: number;
  bytes: number;
}

/**
 * 导出当前过滤视图:``dialog.save()`` 选路径(默认名带日期,覆盖确认归
 * 对话框)→ ``feed.export`` sidecar 直写(数据不经 webview)。
 * 对话框函数注入以便测试;生产缺省 = @tauri-apps/plugin-dialog 的 save。
 */
export async function exportFeedView(
  options: {
    format: ExportFormat;
    category?: string | null;
    sourceKind?: "web" | "im" | null;
    query?: string | null;
  },
  saveDialog: SaveDialogFn = defaultSaveDialog,
): Promise<ExportOutcome> {
  const path = await saveDialog({
    defaultPath: defaultExportName(options.format),
    filters:
      options.format === "jsonl"
        ? [{ name: "JSON Lines", extensions: ["jsonl"] }]
        : [{ name: "CSV", extensions: ["csv"] }],
  });
  if (path === null) return { path: null, count: 0, bytes: 0 };
  const result = await api.feedExport({
    format: options.format,
    path,
    ...(options.category ? { category: options.category } : {}),
    ...(options.sourceKind ? { source_kind: options.sourceKind } : {}),
    ...(options.query ? { query: options.query } : {}),
  });
  return { path: result.path, count: result.count, bytes: result.bytes };
}

/** 生产保存对话框(延迟 import;浏览器直开时 save 不可用属预期错误路径) */
async function defaultSaveDialog(opts: {
  defaultPath: string;
  filters: { name: string; extensions: string[] }[];
}): Promise<string | null> {
  const dialog = await import("@tauri-apps/plugin-dialog");
  return dialog.save(opts);
}

/** 条目稳定 key:dedup_key 优先,id 兜底(防御 null id → url) */
export function itemKey(item: FeedItem): string {
  if (item.dedup_key) return item.dedup_key;
  return `id:${item.id ?? item.url}`;
}

/** 追加一页:滤除已加载条目后拼接(保持新→旧);返回新增数供判停 */
export function appendFeedPage(loaded: FeedItem[], page: FeedPage): { items: FeedItem[]; added: number } {
  const seen = new Set(loaded.map(itemKey));
  const fresh = page.items.filter((item) => !seen.has(itemKey(item)));
  return { items: [...loaded, ...fresh], added: fresh.length };
}

// ---------------------------------------------------------------------------
// 未读 / 星标 / 稍后读三态 —— 双通路(G9,10-04-read-state-server):
//   未过门(旧 sidecar)= 本地态:localStorage 持久,键 = itemKey(本节函数);
//   过门(protocol ≥ READ_STATE_PROTOCOL)= 服务端态:条目投影三键派生 +
//   store.state.* 置位(见本文件 G9 节 + feed-screen 能力门分流)。
// ---------------------------------------------------------------------------

export interface FeedItemState {
  read?: boolean;
  starred?: boolean;
  later?: boolean;
}

/** key(itemKey)→ 三态;未出现的 key 视为 全 false */
export type FeedStateMap = Record<string, FeedItemState>;

const STORAGE_KEY = "myssia.feed.states.v1";

export function loadFeedStates(storage: Storage | null = typeof window === "undefined" ? null : window.localStorage): FeedStateMap {
  if (storage === null) return {};
  try {
    const raw = storage.getItem(STORAGE_KEY);
    if (!raw) return {};
    const parsed: unknown = JSON.parse(raw);
    if (parsed === null || typeof parsed !== "object" || Array.isArray(parsed)) return {};
    return parsed as FeedStateMap;
  } catch {
    // 损坏即弃用本地态(不阻断情报流);下次切换标记时会重写
    return {};
  }
}

export function saveFeedStates(
  states: FeedStateMap,
  storage: Storage | null = typeof window === "undefined" ? null : window.localStorage,
): void {
  if (storage === null) return;
  try {
    storage.setItem(STORAGE_KEY, JSON.stringify(states));
  } catch {
    // 配额/隐私模式写失败不阻断界面(本地态尽力而为)
  }
}

/** 纯切换:read(未读⇄已读)/ starred / later;返回新 map 不改原对象 */
export function toggleMarker(states: FeedStateMap, key: string, marker: keyof FeedItemState): FeedStateMap {
  const current = states[key] ?? {};
  const next: FeedItemState = { ...current, [marker]: !current[marker] };
  const empty = !next.read && !next.starred && !next.later;
  const result: FeedStateMap = { ...states };
  if (empty) {
    delete result[key];
  } else {
    result[key] = next;
  }
  return result;
}

/**
 * 批量置位(G9,10-03-fe-small-batch):对 loaded 全部条目把 marker 置为
 * value;全 false 的键顺手剪除(与 toggleMarker 同存储纪律)。作用域 =
 * 已加载条目(本地态只能按 itemKey 置位,未翻页条目不在内)。
 * G9 后半(read-state-server):过门通路的批量已改走 store.state.mark_all
 * (全库语义),本函数仅未过门(旧 sidecar)通路调用 —— 过门后成死支,
 * 保留不删防未过门组合回归(design §5.4;引用面 grep 在案)。
 */
export function setMarkerBulk(
  items: FeedItem[],
  states: FeedStateMap,
  marker: keyof FeedItemState,
  value: boolean,
): FeedStateMap {
  const result: FeedStateMap = { ...states };
  for (const item of items) {
    const key = itemKey(item);
    const next: FeedItemState = { ...(result[key] ?? {}), [marker]: value };
    if (!next.read && !next.starred && !next.later) {
      delete result[key];
    } else {
      result[key] = next;
    }
  }
  return result;
}

export type FeedFilter = "unread" | "starred" | "later" | "all";

// ---------------------------------------------------------------------------
// later 到期重现(10-05-fe-gap-leftovers ①,池档「snooze 到期重现」项):
// 稍后读桶的提醒时效——放入超窗的条目「到期」,重新计入未读视图(Linear
// H 键 snooze 到期回 inbox 的最小对标;取消稍后读即离场)。锚点 =
// first_seen(入库时刻):later 置位时刻服务端(0/1 列,sqlite.py:144)与
// 本地态(map 无时间戳)均无落点,不为此时效扩存储;窗口取 7 天,与时间
// 分组「7 天内/更早」同界(groupFeedItems)——到期条目即落「更早」组,
// 词汇自洽。
// ---------------------------------------------------------------------------

/** later 提醒时效窗口(天):稍后读条目放入超过本窗口即到期重现于未读 */
export const LATER_RESURFACE_DAYS = 7;
const LATER_RESURFACE_MS = LATER_RESURFACE_DAYS * 86_400_000;

/**
 * 稍后读到期判定:条目带 later 态且 first_seen 早于 now−窗口(含边界)。
 * first_seen 缺失/无效 = 无法定龄,保守不起重现(不往未读流塞不可定龄的
 * 条目;与 groupFeedItems 把缺刻条目归「更早」不同判——那里只是展示桶,
 * 这里起重现会改未读集合,口径从紧)。
 */
export function isLaterResurface(
  item: FeedItem,
  state: FeedItemState | undefined,
  now: Date = new Date(),
): boolean {
  if (state?.later !== true || !item.first_seen) return false;
  const seen = new Date(item.first_seen).getTime();
  if (Number.isNaN(seen)) return false;
  return now.getTime() - seen >= LATER_RESURFACE_MS;
}

/**
 * 过滤视图:未读 = 未标记已读 + 到期稍后读(①:later 放入超窗重现,已读
 * 但未取消稍后读的到期条目回未读流);星标/稍后读按各自标记(稍后读桶
 * 不分到期与否全量可见);全部 = 不过滤。now 注入以便测试时效判定。
 */
export function applyFeedFilter(
  items: FeedItem[],
  states: FeedStateMap,
  filter: FeedFilter,
  now: Date = new Date(),
): FeedItem[] {
  if (filter === "all") return items;
  return items.filter((item) => {
    const state = states[itemKey(item)] ?? {};
    if (filter === "unread") return !state.read || isLaterResurface(item, state, now);
    if (filter === "starred") return state.starred === true;
    return state.later === true;
  });
}

// ---------------------------------------------------------------------------
// G9 服务端读态(read-state-server):能力门常量 + 条目派生状态源 + 一次性搬迁
// ---------------------------------------------------------------------------

/**
 * 服务端读态能力门版本:sidecar `version().protocol ≥ 本值` → 服务端通路;
 * 低版本 / 探测失败 → 旧 localStorage 通路原样保留(旧 sidecar + 新 UI 组合
 * 可用,AC7)。取值与 entry.py `PROTOCOL_VERSION` 同笔维护:read-state-server
 * 批 = 10(含 hermes-cron 竞速顺延,开工实读;后端 bump 时此处同批跟改)。
 */
export const READ_STATE_PROTOCOL = 10;

/** 源大类能力门(10-08-tg-channel-card v2,read-state-server 同款模式):
 *  protocol ≥ 12 = store.items / store.state.mark_all / feed.export 三方法
 *  支持 source_kind(web/im)→ 情报流 L3 走卡片墙(网页一张 + 每通讯软件
 *  一张,点卡进第二层详情);未过门 = v1 形态原样(TG 频道卡区 + 消息列表)。 */
export const SOURCE_KIND_PROTOCOL = 12;

/**
 * 条目 → FeedStateMap(过门后的状态源):read/starred/later 投影三键按
 * itemKey 直配;三态全缺省/false 不产键 —— 与 loadFeedStates 的缺省语义
 * 对齐,喂既有 applyFeedFilter / sortUnreadFirst / 渲染管线零改动。
 */
export function statesFromItems(items: FeedItem[]): FeedStateMap {
  const states: FeedStateMap = {};
  for (const item of items) {
    const state: FeedItemState = {};
    if (item.read === true) state.read = true;
    if (item.starred === true) state.starred = true;
    if (item.later === true) state.later = true;
    if (state.read || state.starred || state.later) states[itemKey(item)] = state;
  }
  return states;
}

/** 一次性搬迁会话哨位:模块级布尔防 React StrictMode 双挂载双调(每会话至多
 *  一次;不做 localStorage 旗标 —— webview 数据可被独立清掉,服务端
 *  store_meta `feed_state_imported_at` 才是幂等真相,Q2.2)。 */
let feedStatesImportAttempted = false;

/**
 * 一次性搬迁 localStorage 读态快照(G9 Q2;过门后由 feed 屏挂载触发):
 * 旧 map 非空 → 单请求 `store.state.import` 整 map 搬完(逐键 RPC = N 往返,
 * 否);应答仅记日志不弹窗(搬迁对用户透明,skipped = id:<url> 形态如实
 * 计数);旧键保留不删(降级回旧 build 读旧快照照常,回滚路径 Q2.3)。
 * 失败不重试(本会话):服务端旗标未落,下会话自然再试。
 *
 * Returns: 实际发起导入的应答 `{imported, skipped}`;null = 未发起
 * (本会话已发起过 / 旧 map 为空 / 搬迁失败)。
 */
export async function importLocalFeedStates(): Promise<{ imported: number; skipped: number } | null> {
  if (feedStatesImportAttempted) return null;
  feedStatesImportAttempted = true;
  const states = loadFeedStates();
  if (Object.keys(states).length === 0) return null;
  try {
    const result = await api.storeStateImport({ states });
    console.info(
      `[feed] 读态一次性搬迁:imported=${result.imported} skipped=${result.skipped}` +
        "(旧键 myssia.feed.states.v1 保留不删)",
    );
    return result;
  } catch (err) {
    console.warn(
      `[feed] 读态一次性搬迁失败(本会话不再重试,下会话再搬):${
        err instanceof Error ? err.message : String(err)
      }`,
    );
    return null;
  }
}

// ---------------------------------------------------------------------------
// 展示辅助:精评分数徽标 / 相对时间 / 品类色(D4)/ 时间分组(D4)
// ---------------------------------------------------------------------------

/**
 * 主分数:enrich scores 形如 {维度: 分值}(schema enrich.scores 命名维度),
 * 取最大数值;无 scores 或全非数值 → null(不显示徽标)。
 */
export function primaryScore(item: FeedItem): number | null {
  if (item.scores === null || item.scores === undefined) return null;
  const values = Object.values(item.scores).filter((value): value is number => typeof value === "number");
  if (values.length === 0) return null;
  return Math.max(...values);
}

/** 相对时间:刚刚 / N 分钟前 / N 小时前 / N 天前;超过 7 天落 YYYY-MM-DD HH:mm */
export function formatRelativeTime(iso: string | null, now: Date = new Date()): string {
  if (!iso) return "—";
  const then = new Date(iso);
  if (Number.isNaN(then.getTime())) return iso;
  const diffMs = now.getTime() - then.getTime();
  const minutes = Math.floor(diffMs / 60_000);
  if (minutes < 1) return "刚刚";
  if (minutes < 60) return `${minutes} 分钟前`;
  const hours = Math.floor(minutes / 60);
  if (hours < 24) return `${hours} 小时前`;
  const days = Math.floor(hours / 24);
  if (days < 7) return `${days} 天前`;
  const pad = (value: number) => String(value).padStart(2, "0");
  return (
    `${then.getFullYear()}-${pad(then.getMonth() + 1)}-${pad(then.getDate())} ` +
    `${pad(then.getHours())}:${pad(then.getMinutes())}`
  );
}

// ---- D4(10-03-ui-deep-imitation):品类色 + 分组时间轴 ----

/** 品类色板:品牌青/紫领衔的 8 色邻位环(暗面可读、饱和度同档;Linear label 式) */
const CATEGORY_PALETTE = [
  "#22d3ee", // 品牌青
  "#8b5cf6", // 品牌紫
  "#3dd68c", // ok 绿
  "#f5b544", // warning 琥珀
  "#60a5fa", // 蓝
  "#f472b6", // 粉
  "#2dd4bf", // 青绿
  "#fb7185", // 玫红
] as const;

/** djb2 字符串散列(稳定无依赖:同品类恒同色,跨会话/跨端不变) */
function hashString(text: string): number {
  let hash = 5381;
  for (let index = 0; index < text.length; index += 1) {
    hash = ((hash << 5) + hash + text.charCodeAt(index)) >>> 0;
  }
  return hash;
}

/**
 * 品类色:卡片左侧品类色条与品类徽标同源取色;无品类 → null(不渲染色件)。
 * 色值是 6 位 hex,透明度由消费侧拼 8 位 hex(hex+alpha)或 opacity 控制。
 */
export function categoryColor(category: string | null | undefined): string | null {
  if (!category) return null;
  return CATEGORY_PALETTE[hashString(category) % CATEGORY_PALETTE.length];
}

/** 时间分组桶 key(新→旧) */
export type FeedGroupKey = "today" | "yesterday" | "week" | "earlier";

export interface FeedGroup {
  key: FeedGroupKey;
  /** 分组头文案(中文界面) */
  label: string;
  items: FeedItem[];
}

const GROUP_LABELS: Record<FeedGroupKey, string> = {
  today: "今天",
  yesterday: "昨天(上一窗口)",
  week: "7 天内",
  earlier: "更早",
};

const DAY_MS = 86_400_000;

/**
 * 分组时间轴(D4):按 first_seen 落 今天 / 昨天(上一窗口)/ 7 天内 /
 * 更早 四桶,保持传入顺序(新→旧),空桶不出组;first_seen 缺失/无效归
 * 「更早」。`now` 注入以便测试。
 *
 * 桶口径与当日窗对齐(深审 F7):边界取 03:00 窗锚(= dayWindowStart),
 * 非日历 0 点 —— 00:00-03:00 的条目属**上一窗**(03:00 清零语义下它们
 * 是昨窗尾段),组头如实标「昨天(上一窗口)」;UI 所见(滚动窗)与
 * 组头口径一致。DST 注记:上一窗起点用本地日历构造(月/日进位,DST 区
 * 跨夏令时边界 ±1h;7 天界用毫秒算术同注)—— 运行时区 Shanghai 无
 * DST,零影响(如实注记,不为不存在的影响加码)。
 */
export function groupFeedItems(
  items: FeedItem[],
  now: Date = new Date(),
  anchorHour: number = DAY_WINDOW_ANCHOR_HOUR,
): FeedGroup[] {
  const startOfWindow = dayWindowStart(now, anchorHour).getTime();
  const prevAnchor = dayWindowStart(now, anchorHour);
  prevAnchor.setDate(prevAnchor.getDate() - 1);
  const startOfPrevWindow = prevAnchor.getTime();
  const buckets: Record<FeedGroupKey, FeedItem[]> = { today: [], yesterday: [], week: [], earlier: [] };
  for (const item of items) {
    const seen = item.first_seen ? new Date(item.first_seen).getTime() : Number.NaN;
    if (Number.isNaN(seen) || seen < startOfWindow - 7 * DAY_MS) {
      buckets.earlier.push(item);
    } else if (seen >= startOfWindow) {
      buckets.today.push(item);
    } else if (seen >= startOfPrevWindow) {
      buckets.yesterday.push(item);
    } else {
      buckets.week.push(item);
    }
  }
  const order: FeedGroupKey[] = ["today", "yesterday", "week", "earlier"];
  return order
    .filter((key) => buckets[key].length > 0)
    .map((key) => ({ key, label: GROUP_LABELS[key], items: buckets[key] }));
}

// ---------------------------------------------------------------------------
// 显示选项(10-04-interaction-batch A-feed):未读优先 + 分组维度,本地持久
// (loadFeedStates 同纪律:损坏/字段非法即弃回缺省;storage 缺席 = 缺省)。
// ---------------------------------------------------------------------------

/** 分组维度:时间四桶(缺省)/ 按品类 / 不分组 */
export type FeedGroupMode = "time" | "category" | "none";

export interface FeedDisplayOptions {
  /** 未读优先:未读浮前、已读沉底(两类各自稳定保序) */
  unreadFirst: boolean;
  /** 分组维度切换 */
  groupMode: FeedGroupMode;
}

/** 缺省显示选项 = 既有行为(时间四桶分组、原序) */
export const DEFAULT_FEED_DISPLAY: FeedDisplayOptions = { unreadFirst: false, groupMode: "time" };

const DISPLAY_STORAGE_KEY = "myssia.feed.display.v1";

/**
 * 读取显示选项:JSON 损坏/非对象 → 整体缺省;单字段类型非法 → 逐字段回
 * 缺省(部分合法仍保留),纪律同 loadFeedStates(不阻断情报流)。
 */
export function loadFeedDisplay(
  storage: Storage | null = typeof window === "undefined" ? null : window.localStorage,
): FeedDisplayOptions {
  if (storage === null) return { ...DEFAULT_FEED_DISPLAY };
  try {
    const raw = storage.getItem(DISPLAY_STORAGE_KEY);
    if (!raw) return { ...DEFAULT_FEED_DISPLAY };
    const parsed: unknown = JSON.parse(raw);
    if (parsed === null || typeof parsed !== "object" || Array.isArray(parsed)) {
      return { ...DEFAULT_FEED_DISPLAY };
    }
    const record = parsed as Record<string, unknown>;
    return {
      unreadFirst:
        typeof record.unreadFirst === "boolean" ? record.unreadFirst : DEFAULT_FEED_DISPLAY.unreadFirst,
      groupMode:
        record.groupMode === "time" || record.groupMode === "category" || record.groupMode === "none"
          ? record.groupMode
          : DEFAULT_FEED_DISPLAY.groupMode,
    };
  } catch {
    return { ...DEFAULT_FEED_DISPLAY };
  }
}

export function saveFeedDisplay(
  options: FeedDisplayOptions,
  storage: Storage | null = typeof window === "undefined" ? null : window.localStorage,
): void {
  if (storage === null) return;
  try {
    storage.setItem(DISPLAY_STORAGE_KEY, JSON.stringify(options));
  } catch {
    // 配额/隐私模式写失败不阻断界面(本地态尽力而为)
  }
}

/**
 * 未读优先(A-feed):未读浮前、已读沉底;两类各自保持传入原序(ES2019+
 * sort 稳定保证,不引显式索引兜底)。不改原数组(返回新序)。
 */
export function sortUnreadFirst(items: FeedItem[], states: FeedStateMap): FeedItem[] {
  return [...items].sort(
    (a, b) => Number(states[itemKey(a)]?.read === true) - Number(states[itemKey(b)]?.read === true),
  );
}

/** 品类分组(A-feed):组头色点与卡片品类色条同源(categoryColor) */
export interface FeedCategoryGroup {
  /** 品类值(无品类 = null,作 React key 时由消费侧兜底) */
  key: string | null;
  /** 组头文案(中文界面;无品类 = 未分类) */
  label: string;
  /** 品类色(categoryColor 同源;无品类 = null 不渲色点) */
  color: string | null;
  items: FeedItem[];
}

/**
 * 按品类分组(A-feed):品类按首次出现顺序出组(稳定、可预期),组内保持
 * 传入顺序;无品类条目归「未分类」组(排在首次出现处,不强制沉底)。
 */
export function groupFeedItemsByCategory(items: FeedItem[]): FeedCategoryGroup[] {
  const groups: FeedCategoryGroup[] = [];
  const byCategory = new Map<string | null, FeedCategoryGroup>();
  for (const item of items) {
    const key = item.category ?? null;
    let group = byCategory.get(key);
    if (!group) {
      group = { key, label: key ?? "未分类", color: categoryColor(key), items: [] };
      byCategory.set(key, group);
      groups.push(group);
    }
    group.items.push(item);
  }
  return groups;
}

// ---------------------------------------------------------------------------
// 渠道级分组与渠道类型判定(10-06-feed-channel-groups:主人令「情报流也要
// 分渠道」+「不同渠道表现的方式不一样」)。品类分组下再按渠道(items.source
// = 源名全称,规约 telegram-<频道原名> 等)细分;渠道类型五档:
//   telegram = 消息卡(聊天感:正文气泡+时间+频道名;源名前缀判定)
//   watch    = 变更事件(engine urlwatch 或条目带 watch_event;「有更新」
//              徽标+时间+目标页链接 watch_page)
//   document = 日报文档(engine prompt / store_report;markdown 可折叠正文)
//   deal     = 价格优惠行(品类 games/wool 或价格键在场;价格字段突出)
//   news     = 新闻列表卡(缺省,现状 RSS 形态)
// engine 判定的词表源 = health().plugins[].sources[].name→engine 映射
// (本屏品类下拉同一次 health 调用顺带装配,零新 RPC);health 失败/旧
// sidecar 无映射时退化为前缀+品类+字段三级判定(watch_event/价格键由
// _item_dict 白名单投影,见 entry.py)。
// ---------------------------------------------------------------------------

/** 渠道类型五档(呈现档位;判定优先级 telegram > watch > document > deal) */
export type ChannelKind = "telegram" | "watch" | "document" | "deal" | "news";

/** telegram 源名前缀(命名规约 telegram-<渠道原名>;tg- 旧缩写同收防漏) */
const TELEGRAM_SOURCE_RE = /^(telegram|tg)[-_.]/i;

/** 优惠渠道品类集(games 游戏情报 / wool 羊毛情报;config.id 词表) */
const DEAL_CATEGORIES = new Set(["games", "wool"]);

/** 渠道类型判定输入(item 的渠道相关字段子集;便于纯函数测试窄化) */
export type ChannelKindInput = Pick<
  FeedItem,
  "source" | "category" | "watch_event" | "price_text" | "final_price" | "sale_price"
>;

/**
 * 渠道类型判定:源名前缀(telegram- 或 tg- 前缀)→ 消息卡;engine=urlwatch
 * 或条目带 watch_event(旧 sidecar 无 engine 映射时的字段级兜底)→ 变更
 * 事件;engine=prompt/store_report → 日报文档;品类 games/wool 或任一
 * 价格键在场 → 价格优惠行;其余 → 新闻列表卡(现状缺省)。
 * engineOfSource 缺席(health 失败)= 空映射,纯靠前缀+品类+字段。
 */
export function channelKindOf(
  item: ChannelKindInput,
  engineOfSource?: ReadonlyMap<string, string>,
): ChannelKind {
  const source = item.source ?? "";
  if (TELEGRAM_SOURCE_RE.test(source)) return "telegram";
  const engine = engineOfSource?.get(source);
  if (engine === "urlwatch" || (item.watch_event ?? null) !== null) return "watch";
  if (engine === "prompt" || engine === "store_report") return "document";
  if (
    (item.category !== null && DEAL_CATEGORIES.has(item.category)) ||
    item.price_text != null ||
    item.final_price != null ||
    item.sale_price != null
  ) {
    return "deal";
  }
  return "news";
}

/** health().plugins → 源名→engine 映射(渠道类型判定的词表源;同一次调用) */
export function engineMapFromHealth(plugins: HealthResult["plugins"]): Map<string, string> {
  const engines = new Map<string, string>();
  for (const plugin of plugins) {
    for (const source of plugin.sources) {
      if (source.name && source.engine && !engines.has(source.name)) {
        engines.set(source.name, source.engine);
      }
    }
  }
  return engines;
}

/** 渠道分组(品类分组下的二级分组):渠道按首次出现顺序出组(与品类分组
 *  同纪律:稳定、可预期),组内保持传入顺序;无源名条目归「未知来源」组。 */
export interface FeedChannelGroup {
  /** 源名(items.source;无源名 = null,React key 由消费侧兜底) */
  key: string | null;
  /** 组头文案(源名全称;无源名 = 未知来源) */
  label: string;
  /** 渠道类型(组内首条判定;同源同渠道,组内一致) */
  kind: ChannelKind;
  items: FeedItem[];
}

export function groupFeedItemsByChannel(
  items: FeedItem[],
  engineOfSource?: ReadonlyMap<string, string>,
): FeedChannelGroup[] {
  const groups: FeedChannelGroup[] = [];
  const bySource = new Map<string | null, FeedChannelGroup>();
  for (const item of items) {
    const key = item.source ?? null;
    let group = bySource.get(key);
    if (!group) {
      group = {
        key,
        label: key ?? "未知来源",
        kind: channelKindOf(item, engineOfSource),
        items: [],
      };
      bySource.set(key, group);
      groups.push(group);
    }
    group.items.push(item);
  }
  return groups;
}

/** 源名展示词(telegram-<频道> 规约:去平台前缀显频道本名;其余源名全称直出。
 *  10-08-tg-channel-card 自 feed-screen 收编入 api —— 渠道卡视图模型与卡面
 *  头区共用同一词表,聚合函数返回的 label 即成品词)。 */
export function channelDisplayName(source: string | null): string {
  if (source === null) return "未知来源";
  const stripped = source.replace(/^(telegram|tg)[-_.]/i, "");
  return stripped === "" ? source : stripped;
}

/** TG 渠道卡(10-08-tg-channel-card,主人令「渠道单独一个卡片,点击进去才是
 *  详情」):把可见集里的 telegram 条目按渠道聚合为渠道卡视图模型 —— 每渠道
 *  一卡(频道名/条数/未读/最新一条),消息卡不再逐条进流,点卡进该渠道
 *  source 作用域消息流(详情)。
 *
 *  口径:输入 = 调用方过滤后的可见条目(当前读态过滤 ∪ 当日窗),计数即
 *  视图诚实计数;排序 = 最新消息新→旧(聊天列表惯例),first_seen 缺失/
 *  非法沉底,同刻按源名稳定 tiebreak。telegram 判定复用 channelKindOf
 *  (源名前缀档,engine 词表无关该档,零依赖)。 */
export interface TelegramChannelCardData {
  /** 源名全称(items.source;下钻作用域键) */
  key: string;
  /** 频道显示名(去 telegram- 前缀本名) */
  label: string;
  /** 可见条数 */
  count: number;
  /** 其中未读数(states 读态;server/local 两通路同语义) */
  unread: number;
  /** 最新一条(first_seen 最大;预览与相对时间源) */
  latest: FeedItem;
}

function firstSeenValue(iso: string | null | undefined): number {
  if (!iso) return Number.NEGATIVE_INFINITY;
  const value = new Date(iso).getTime();
  return Number.isNaN(value) ? Number.NEGATIVE_INFINITY : value;
}

/** 卡片摘要字符上限(v3,主人令「精炼,不能过长,也不能展示不出来特殊
 *  之处」):一行摘要的硬截断位,CSS truncate 再兜底视觉一行。 */
export const CARD_DIGEST_MAX_CHARS = 72;

/** 卡片摘要(v3):为卡片描述行产出「内容里的特殊之处」,精炼一行 ——
 *  ① 优惠:价格片段即特殊之处(dealPriceView:限免/现价/原价/折扣);
 *  ② 其余:正文压平取头,且**先去掉与标题重复的开头**(TG 消息正文常
 *     复述标题,不去重则摘要行空转、版本号等独有信息被挤出);
 *  ③ 无正文回事件词(watch 首纳/有更新);全空 = null(消费侧不渲染
 *     空行)。超长 `…` 收尾。 */
export function cardDigest(item: FeedItem): string | null {
  const title = (item.title ?? "").trim();
  if (item.price_text != null || item.final_price != null || item.sale_price != null) {
    const deal = dealPriceView(item);
    const bits: string[] = [];
    if (deal.free) bits.push("限免");
    if (deal.current !== null) bits.push(deal.current);
    if (deal.original !== null) bits.push(`原价 ${deal.original}`);
    if (deal.discount !== null && !deal.free) bits.push(`-${deal.discount}%`);
    if (bits.length > 0) return bits.join(" · ");
  }
  const body = (item.content ?? "").replace(/\s+/g, " ").trim();
  const deduped = title !== "" && body.startsWith(title) ? body.slice(title.length).trim() : body;
  const text =
    deduped ||
    (item.watch_event != null
      ? item.watch_event === "new"
        ? "首次纳入监控"
        : "目标页有更新"
      : "");
  if (text === "") return null;
  if (text.length <= CARD_DIGEST_MAX_CHARS) return text;
  return `${text.slice(0, CARD_DIGEST_MAX_CHARS)}…`;
}

export function telegramChannelCards(
  items: FeedItem[],
  states: FeedStateMap,
): TelegramChannelCardData[] {
  const bySource = new Map<string, { count: number; unread: number; latest: FeedItem }>();
  for (const item of items) {
    if (channelKindOf(item) !== "telegram") continue;
    const key = item.source ?? "";
    if (key === "") continue;
    const read = states[itemKey(item)]?.read === true;
    const row = bySource.get(key);
    if (row) {
      row.count += 1;
      if (!read) row.unread += 1;
      if (firstSeenValue(item.first_seen) > firstSeenValue(row.latest.first_seen)) row.latest = item;
    } else {
      bySource.set(key, { count: 1, unread: read ? 0 : 1, latest: item });
    }
  }
  return [...bySource.entries()]
    .map(([key, row]) => ({ key, label: channelDisplayName(key), ...row }))
    .sort((a, b) => {
      const diff = firstSeenValue(b.latest.first_seen) - firstSeenValue(a.latest.first_seen);
      return diff !== 0 ? diff : a.key.localeCompare(b.key);
    });
}

/** 源名 → 通讯软件应用标识(10-08-tg-channel-card v2 卡片墙「每通讯软件
 *  一张卡」;与 channelKindOf 同一词表 —— telegram-/tg- 前缀 = telegram。
 *  今后新接入的通讯软件在此扩一词,卡片墙自动多一张软件卡)。 */
export function imAppOf(source: string | null | undefined): "telegram" | null {
  if (!source) return null;
  return /^(telegram|tg)[-_.]/i.test(source) ? "telegram" : null;
}

/** 卡片墙视图模型(10-08-tg-channel-card v2,主人令「网页集中在一起,其他
 *  通讯软件一个通讯软件一个卡片,点击进入第二层才是详情展示」):L3 多渠道
 *  作用域的第一层只有大类卡 —— 网页一张(一切非通讯软件源)+ 每通讯软件
 *  应用一张(Telegram 等),散条目卡不再出现在第一层。
 *
 *  口径与 telegramChannelCards 相同:输入 = 调用方过滤后的可见条目,计数即
 *  视图诚实计数;排序 = 最新消息新→旧(网页/软件卡同榜竞争),first_seen
 *  缺失/非法沉底,同刻按 key 稳定 tiebreak。 */
export interface StreamKindCardData {
  /** 卡片作用域键 = 源大类(drill.kind 同词表):"web" = 网页卡(详情查询
   *  source_kind=web);"im" = 通讯软件卡(详情查询 source_kind=im) */
  key: "web" | "im";
  /** 卡面词(网页 / Telegram;新 IM 应用在此补词) */
  label: string;
  /** 可见条数 */
  count: number;
  /** 其中未读数 */
  unread: number;
  /** 最新一条(预览与相对时间源) */
  latest: FeedItem;
}

export function streamKindCards(
  items: FeedItem[],
  states: FeedStateMap,
): StreamKindCardData[] {
  const byKey = new Map<"web" | "im", { count: number; unread: number; latest: FeedItem }>();
  for (const item of items) {
    const key: "web" | "im" = imAppOf(item.source) !== null ? "im" : "web";
    const read = states[itemKey(item)]?.read === true;
    const row = byKey.get(key);
    if (row) {
      row.count += 1;
      if (!read) row.unread += 1;
      if (firstSeenValue(item.first_seen) > firstSeenValue(row.latest.first_seen)) row.latest = item;
    } else {
      byKey.set(key, { count: 1, unread: read ? 0 : 1, latest: item });
    }
  }
  const labels: Record<StreamKindCardData["key"], string> = { web: "网页", im: "Telegram" };
  return [...byKey.entries()]
    .map(([key, row]) => ({ key, label: labels[key], ...row }))
    .sort((a, b) => {
      const diff = firstSeenValue(b.latest.first_seen) - firstSeenValue(a.latest.first_seen);
      return diff !== 0 ? diff : a.key.localeCompare(b.key);
    });
}

/** 价格/优惠行的展示视图(games 四源字段形态并存,push 模板 elif 链同款
 *  优先序:price_text(Epic 直出)→ sale_price(CS·GOG 美元串,配
 *  normal_price 原价)→ final_price 数值分 ÷100(Steam/Epic);折扣徽标
 *  取 discount_pct(int)或 savings_pct(字符串 % 解析);限免判定镜像
 *  games.yaml classify「限免」析取(final_price==0 / discount≥100 /
 *  sale 0 且 normal>0)。 */
export interface DealPriceView {
  /** 现价词面(直出或换算;无任何价格键 = null,消费侧不渲价格块) */
  current: string | null;
  /** 原价词面(划线呈现;无 = null) */
  original: string | null;
  /** 折扣百分比(整数;无 = null) */
  discount: number | null;
  /** 限免(true = 「限免」徽标) */
  free: boolean;
}

/**
 * 数值键宽容解析(深审 F5):store 投影/旧 sidecar 可把数值键以字符串形态
 * 送达(final_price: "1360")—— Number() 宽容解析;null/undefined/空串/
 * 布尔/NaN → null(形态坏不猜,原 null 语义不变)。sale_price/normal_price/
 * savings_pct 本就是字符串键,保持 parseFloat 既有路径。
 */
function lenientNumber(value: unknown): number | null {
  if (value === null || value === undefined || typeof value === "boolean" || value === "") {
    return null;
  }
  const parsed = typeof value === "number" ? value : Number(value);
  return Number.isFinite(parsed) ? parsed : null;
}

export function dealPriceView(
  item: Pick<FeedItem, "price_text" | "sale_price" | "normal_price" | "final_price" | "original_price" | "discount_pct" | "savings_pct">,
): DealPriceView {
  const numericFinal = lenientNumber(item.final_price);
  const numericOriginal = lenientNumber(item.original_price);
  const numericDiscount = lenientNumber(item.discount_pct);
  const current =
    item.price_text != null && item.price_text !== ""
      ? item.price_text
      : item.sale_price != null && item.sale_price !== ""
        ? `$${item.sale_price}`
        : numericFinal !== null
          ? `¥${(numericFinal / 100).toFixed(2)}`
          : null;
  const original =
    item.normal_price != null && item.normal_price !== ""
      ? `$${item.normal_price}`
      : numericOriginal !== null
        ? `¥${(numericOriginal / 100).toFixed(2)}`
        : null;
  const savings = item.savings_pct != null ? Number.parseFloat(item.savings_pct) : Number.NaN;
  const discount =
    numericDiscount !== null
      ? Math.round(numericDiscount)
      : Number.isFinite(savings)
        ? Math.round(savings)
        : null;
  const sale = item.sale_price != null ? Number.parseFloat(item.sale_price) : Number.NaN;
  const normal = item.normal_price != null ? Number.parseFloat(item.normal_price) : Number.NaN;
  const free =
    numericFinal === 0 ||
    (discount !== null && discount >= 100) ||
    (Number.isFinite(sale) && sale === 0 && Number.isFinite(normal) && normal > 0);
  return { current, original, discount, free };
}

// ---------------------------------------------------------------------------
// 当日窗滚动 + 实时滚动(10-06-feed-channel-groups 追加:主人令「情报流要
// 不停地过信息日志,每天凌晨 3 点清零,继续过滤」)。语义:
//   · 「清零」是**视图层当日窗滚动**——store 数据不动(retention 照旧),
//     过了 03:00 视图重新从零累计当日流;窗口锚写死 03:00(配置位预留
//     anchorHour 参数,缺省 DAY_WINDOW_ANCHOR_HOUR)。
//   · 窗口只作用于滚动流(未读/全部两档);星标/稍后读是用户显式留存,
//     不随窗清零(跨窗可见)。
//   · 实时滚动 = completed / cron.completed 事件驱动即时刷新(采集一落地
//     就进流)+ 可见性感知的定时轮询兜底(CLI 独立跑的采集无事件;隐藏
//     时暂停,不打 sidecar)。
// ---------------------------------------------------------------------------

/** 当日窗锚点小时(凌晨 3 点清零;配置位预留,缺省即写死值) */
export const DAY_WINDOW_ANCHOR_HOUR = 3;

/**
 * 当日窗起点:now 所在「03:00 → 次日 03:00」窗口的 03:00 时刻。
 * 例:05-01 14:00 → 05-01 03:00;05-01 02:59 → 04-30 03:00。
 * `now` 注入以便测试(边界:整点、点前一分钟)。
 */
export function dayWindowStart(now: Date = new Date(), anchorHour: number = DAY_WINDOW_ANCHOR_HOUR): Date {
  const start = new Date(now.getFullYear(), now.getMonth(), now.getDate(), anchorHour, 0, 0, 0);
  if (now.getTime() >= start.getTime()) return start;
  start.setDate(start.getDate() - 1);
  return start;
}

/**
 * 条目是否在当日窗内:first_seen ≥ start 即在窗。缺失/无法解析的
 * first_seen **保守放行**(进窗可见)—— 与 isLaterResurface 的从紧口径
 * 相反:这里排除会静默藏数据,宁可多显。items.first_seen 列 NOT NULL,
 * 异常形态罕见,防御而已。
 */
export function inDayWindow(firstSeen: string | null | undefined, start: Date): boolean {
  if (!firstSeen) return true;
  const seen = new Date(firstSeen).getTime();
  if (Number.isNaN(seen)) return true;
  return seen >= start.getTime();
}

/** 滚动流窗内过滤(unread/all 两档用;starred/later 不走此门) */
export function filterDayWindow(items: FeedItem[], start: Date): FeedItem[] {
  return items.filter((item) => inDayWindow(item.first_seen, start));
}

/** 轮询合并:首页(新→旧)里已加载集合没有的键 **前插**(实时进流),
 *  已加载行一条不丢(与翻页 appendFeedPage 的追加语义互补;去重同键)。 */
export function mergeFreshItems(loaded: FeedItem[], fresh: FeedItem[]): { items: FeedItem[]; added: number } {
  const seen = new Set(loaded.map(itemKey));
  const incoming = fresh.filter((item) => !seen.has(itemKey(item)));
  return { items: [...incoming, ...loaded], added: incoming.length };
}

/** 实时滚动轮询间隔(毫秒):可见时 30s 一发 store.items 首页查询(SQLite
 *  读,轻);隐藏暂停(visibilitychange 恢复即刷)。 */
export const LIVE_POLL_INTERVAL_MS = 30_000;

// ---------------------------------------------------------------------------
// G12 沉淀为关键词(10-03-fe-small-batch):yaml.* 屏私有封装 + 原文文本手术。
// 写通道语义复用 yaml-editor(yaml.read → 文本手术 → yaml.save:mtime 乐观
// 锁 + 服务端同门校验 + 跨文件 id 查重 duplicate_category_id——改词不动 id,
// 查重天然不破);契约权威 = entry.py `_m_yaml_*`,错误码族由后端结构化
// 抛出,这里只归一化为 SidecarRequestError(惯例同 sources/yaml-editor 屏
// 私有封装:invoke 直连 + asSidecarError 同规则归一)。
// ---------------------------------------------------------------------------

/** yaml.list 单项(G12 只需选择面字段;权威形状 entry.py `_m_yaml_list`) */
export interface YamlTargetFile {
  /** 品类 YAML 绝对路径(yaml.read/save 同口径) */
  file: string;
  /** 文件名(如 ai-news.yaml) */
  name: string;
  parse_ok: boolean;
  category_id: string | null;
  category_name: string | null;
}

export interface YamlTargetList {
  plugins_dir: string;
  files: YamlTargetFile[];
}

/** yaml.read 应答(mtime = save 乐观锁基线) */
export interface YamlRawRead {
  file: string;
  /** UTF-8 原文(注释/顺序逐字节原样;手术只动 keywords 一处) */
  content: string;
  mtime: number;
}

/** yaml.save 应答(写入面字段;warnings 原样透传不展开) */
export interface YamlRawSave {
  file: string;
  written: true;
  created: boolean;
  backed_up: string | null;
  mtime: number;
  warnings: unknown[];
}

/** 任意抛出物 → SidecarRequestError(规则与 yaml-editor/api.ts asSidecarError 相同)。 */
function asSidecarError(raw: unknown): SidecarRequestError {
  if (raw instanceof SidecarRequestError) return raw;
  if (typeof raw === "string") {
    try {
      const parsed = JSON.parse(raw) as Partial<SidecarErrorShape>;
      if (parsed && typeof parsed.code === "string" && typeof parsed.message === "string") {
        return new SidecarRequestError({
          code: parsed.code,
          path: typeof parsed.path === "string" ? parsed.path : "$",
          message: parsed.message,
          data: parsed.data,
        });
      }
    } catch {
      // 非 JSON 文本:按裸消息包装
    }
    return new SidecarRequestError({ code: "transport_error", path: "$", message: raw });
  }
  return new SidecarRequestError({
    code: "sidecar_unavailable",
    path: "$",
    message: raw instanceof Error ? `Tauri IPC 不可用: ${raw.message}` : `Tauri IPC 不可用: ${String(raw)}`,
  });
}

/** 类型化往返:yaml.* 经壳命令 sidecar_request,失败归一化抛出。 */
async function sidecarRequest<R>(method: string, params: unknown): Promise<R> {
  try {
    return await invoke<R>("sidecar_request", { method, params });
  } catch (raw) {
    throw asSidecarError(raw);
  }
}

/** 品类 YAML 清单(G12 目标选择;坏文件 parse_ok=false 由 UI 过滤不选)。 */
export function listYamlTargets(): Promise<YamlTargetList> {
  return sidecarRequest<YamlTargetList>("yaml.list", {});
}

/** 原文直读(手术基底 + mtime 乐观锁基线)。 */
export function readYamlRaw(file: string): Promise<YamlRawRead> {
  return sidecarRequest<YamlRawRead>("yaml.read", { file });
}

/** 编辑写回:服务端同门校验(零容忍 error 级)+ 跨文件 id 查重 + .bak 留底。 */
export function saveYamlRaw(file: string, content: string, expected_mtime: number): Promise<YamlRawSave> {
  return sidecarRequest<YamlRawSave>("yaml.save", { file, content, expected_mtime });
}

/** 关键词长度上限(schema ShortStr = 1..64;前端预检,后端仍是守门) */
export const KEYWORD_MAX_CHARS = 64;

/** 手术结果:ok=false 的 reason 驱动 UI 文案(空/超长/已在/不可解析) */
export type KeywordAppendOutcome =
  | { ok: true; content: string }
  | { ok: false; reason: "empty_keyword" | "keyword_too_long" | "already_present" | "keywords_unparsed" };

/** 流式/块式列表里安全的关键词形态:纯词原样,含 YAML 特殊字符则双引号转义 */
function yamlSafeKeyword(keyword: string): string {
  if (/^[A-Za-z0-9_\-\u4e00-\u9fff][A-Za-z0-9_\-\u4e00-\u9fff ]*$/.test(keyword)) return keyword;
  return JSON.stringify(keyword); // 双引号 + 反斜杠转义(YAML 双引号串兼容)
}

/** 列表项词面值(已存在比对用;单/双引号包裹剥壳,其余原样) */
function keywordLiteral(entry: string): string {
  const trimmed = entry.trim();
  if (
    (trimmed.startsWith('"') && trimmed.endsWith('"') && trimmed.length >= 2) ||
    (trimmed.startsWith("'") && trimmed.endsWith("'") && trimmed.length >= 2)
  ) {
    return trimmed.slice(1, -1);
  }
  return trimmed;
}

/**
 * watchlist.keywords 文本手术(G12):把关键词追加进 YAML **原文**(注释/
 * 顺序/其余节点逐字节不动,只动 keywords 一处;id 行原样 → 服务端跨文件
 * id 查重不破)。支持四种现实形态:
 *   ① 流式 `keywords: [a, b]`(含空 `[]`)→ 闭括号前插入 `, 新词`
 *   ② 块式 `keywords:` + 深缩进 `- 项` 行列表 → 末项后追加同缩进 `- 新词`
 *   ③ `keywords:` 空值 / null / ~ → 键行后起块式首项
 *   ④ 无 keywords 键:有 `watchlist:` 顶层键 → 其下补 `keywords:` 块;
 *      连 watchlist 都没有 → 文件末尾追加整个 watchlist 节(缺省即空表,
 *      补节不改变其余语义)
 * 词已在列表 → `already_present`(零写入);非常规排版(标量值等)→
 * `keywords_unparsed`(UI 引导去配置编辑,不硬猜)。最终守门仍是
 * yaml.save 的 load_category 同门校验(坏结果结构化拒,零落盘)。
 */
export function appendWatchlistKeyword(content: string, rawKeyword: string): KeywordAppendOutcome {
  const keyword = rawKeyword.trim();
  if (!keyword) return { ok: false, reason: "empty_keyword" };
  if (keyword.length > KEYWORD_MAX_CHARS) return { ok: false, reason: "keyword_too_long" };
  const safe = yamlSafeKeyword(keyword);
  const lines = content.split("\n");

  const keywordsIndex = lines.findIndex((line) => /^(\s*)keywords:/.test(line));
  if (keywordsIndex >= 0) {
    const match = lines[keywordsIndex].match(/^(\s*)keywords:\s*(.*)$/);
    const indent = match?.[1] ?? "";
    const rest = (match?.[2] ?? "").trim();
    // ① 流式单行列表(允许尾随注释)
    const flow = lines[keywordsIndex].match(/^(\s*keywords:\s*\[)(.*?)(\].*)$/);
    if (flow) {
      const inner = flow[2].trim();
      const entries = inner === "" ? [] : inner.split(",").map(keywordLiteral);
      if (entries.includes(keyword)) return { ok: false, reason: "already_present" };
      const nextInner = inner === "" ? safe : `${inner}, ${safe}`;
      lines[keywordsIndex] = `${flow[1]}${nextInner}${flow[3]}`;
      return { ok: true, content: lines.join("\n") };
    }
    // ② 块式 / ③ 空值(null/~ 需先落定键行):键行后连续的(更深缩进)- 项行
    if (rest === "" || rest === "null" || rest === "~") {
      if (rest !== "") lines[keywordsIndex] = `${indent}keywords:`;
      let lastItemIndex = -1;
      let itemIndent = "";
      for (let index = keywordsIndex + 1; index < lines.length; index += 1) {
        const line = lines[index];
        if (line.trim() === "") continue;
        const itemMatch = line.match(/^(\s+)-\s?(.*)$/);
        if (!itemMatch || itemMatch[1].length <= indent.length) break;
        lastItemIndex = index;
        itemIndent = itemMatch[1];
        if (keywordLiteral(itemMatch[2]) === keyword) return { ok: false, reason: "already_present" };
      }
      if (lastItemIndex >= 0) {
        lines.splice(lastItemIndex + 1, 0, `${itemIndent}- ${safe}`);
      } else {
        lines.splice(keywordsIndex + 1, 0, `${indent}  - ${safe}`);
      }
      return { ok: true, content: lines.join("\n") };
    }
    // 标量值等非常规排版:不硬猜,引导去配置编辑
    return { ok: false, reason: "keywords_unparsed" };
  }

  // ④a 无 keywords 键:顶层 watchlist: 键下补块(顺序无关,YAML 语义等价)
  const watchlistIndex = lines.findIndex((candidate) => /^watchlist:\s*(#.*)?$/.test(candidate));
  if (watchlistIndex >= 0) {
    lines.splice(watchlistIndex + 1, 0, "  keywords:", `    - ${safe}`);
    return { ok: true, content: lines.join("\n") };
  }

  // ④b 连 watchlist 节都没有:文件末尾整节追加(schema 缺省即空表,补节安全)
  const base = content.length === 0 ? "" : content.endsWith("\n") ? content : `${content}\n`;
  return { ok: true, content: `${base}watchlist:\n  keywords:\n    - ${safe}\n` };
}
