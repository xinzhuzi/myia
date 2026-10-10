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
import type { FeedItem, HealthResult, SidecarErrorShape, SourceStatsRow } from "@/lib/api";

export type { SourceStatsRow };

/** 单页条数(与卡片瀑布一屏量级匹配) */
export const FEED_PAGE_SIZE = 50;

/** 翻页请求:cursor = 上页最旧条目的 (first_seen, id) 对(首页两键皆 null) */
export interface FeedPageRequest {
  cursor: string | null;
  /** 复合游标第二键(与 cursor 同源:同刻条目翻页不跳不重) */
  cursorId: number | null;
  pageSize?: number;
  /** 源名过滤(null = 不传参;v6 渠道详情作用域,store.items source 精确
   *  等值。category/source_kind 两参随 v5 chips/源大类信息架构退役不重挂
   *  ——三级 IA 无「按类型查条目」动线;后端两参保留不删) */
  source?: string | null;
  /** 渠道内检索(v8 3 级,重挂):store.items query 参透传(title/content/
   *  source 三列 LIKE;共享客户端 types.ts 与后端全在,封装层一行)。检索态
   *  语义 = 显式全量,绕读态过滤由 UI 裁;翻页游标与 query 同 WHERE */
  query?: string | null;
  /** 同条件全量计数(F2 计数口径根治,仅过 COUNT_PROTOCOL 门时传):
   *  true = store.items 带 with_total → 应答 total 透出 FeedPage.total */
  withTotal?: boolean;
}

export interface FeedPage {
  /** 服务端原始返回(新→旧;边界条目由 appendFeedPage 去重兜底) */
  items: FeedItem[];
  /** 服务端返回数达到 limit → 可能还有更旧条目(判停 = 返回数 < limit) */
  hasMore: boolean;
  /** 下页游标 = 本页最旧条目的 (first_seen, id)(空页为 null) */
  nextCursor: string | null;
  nextCursorId: number | null;
  /** 同条件全量计数(F2;仅 withTotal 且 sidecar 回带 total 键时非 null,
   *  形状坏/缺键 = null → UI 回落「已加载 N 条」词面,不猜不报错) */
  total: number | null;
}

export async function fetchFeedPage(request: FeedPageRequest): Promise<FeedPage> {
  const pageSize = request.pageSize ?? FEED_PAGE_SIZE;
  const result = await api.storeItems({
    limit: pageSize,
    ...(request.cursor
      ? { before: request.cursor, ...(request.cursorId !== null ? { before_id: request.cursorId } : {}) }
      : {}),
    ...(request.source ? { source: request.source } : {}),
    ...(request.query ? { query: request.query } : {}),
    ...(request.withTotal ? { with_total: true } : {}),
  });
  const items = result.items;
  const oldest = items.length > 0 ? items[items.length - 1] : null;
  return {
    items,
    hasMore: items.length >= pageSize,
    nextCursor: oldest?.first_seen ?? null,
    nextCursorId: oldest?.id ?? null,
    total: typeof result.total === "number" ? result.total : null,
  };
}

// ---------------------------------------------------------------------------
// 屏内品类下拉(10-04-topbar-cleanup:品类过滤从全局顶栏拆下归位 feed 屏;
// 词汇源沿用顶栏旧路 = health().plugins,与 store.items 的 category 精确
// 等值同口径 —— 入库时条目记 config.id(pipeline.py `category=self.config.id`),
// 选项 value 即 plugin.id,label 显名称)
// ---------------------------------------------------------------------------

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
  // v6:全库直出(category/source_kind/query 随信息架构退役,已摘除)
  const result = await api.feedExport({ format: options.format, path });
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

/**
 * 计数口径能力门(10-09-tg-category-entry F2 计数口径根治,READ_STATE 同款
 * 模式):protocol ≥ 13 = store.items 支持可选 `with_total` → 应答带 `total`
 * (同 WHERE 不分页全量计数)→ 工具条/墙卡词面「已加载 X · 共 T 条」;
 * 未过门 / 应答无 total 字段(旧 sidecar 忽略未知参数属预期,不报错)=
 * 回落「已加载 N 条」词面(F2 半程:如实不说满话,但 T 缺位)。取值与
 * entry.py `PROTOCOL_VERSION` 同笔维护:本批 = 13,后端 bump 时此处同批跟改。
 */
export const COUNT_PROTOCOL = 13;

/**
 * 分源统计能力门(v8 三级界面批,1 级类型卡统计的全库真值源):protocol ≥ 14
 * = sidecar 有 `store.source_stats` 分源聚合(每源 total/today/unread/latest
 * 一答直出)→ 类型卡/2 级行计数覆写为全库值;未过门(旧 sidecar 无此方法 /
 * protocol<14)= 客户端 catalog 已加载口径 + title 词面如实,**不发 RPC
 * 试错**(门先行,COUNT_PROTOCOL 同模式)。取值与 entry.py
 * `PROTOCOL_VERSION` 同笔维护:本批 = 14,后端 bump 时此处同批跟改。
 */
export const STATS_PROTOCOL = 14;

/** 分源统计拉取(v8 1 级类型卡统计底座;since = 当日窗锚 Date,省略 =
 *  today 恒 0「无窗无今日」。应答 rows 原样透出,归并/覆写在纯函数侧) */
export async function fetchSourceStats(since: Date | null): Promise<SourceStatsRow[]> {
  const result = await api.storeSourceStats({
    ...(since ? { since: since.toISOString() } : {}),
  });
  return result.rows;
}

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

/** 品类色板:8 色邻位环(暗面可读、饱和度同档;Linear label 式)。
 *  10-08 审计 F8:色板避开语义色(ok 绿 #43f6b6 / warning 橙 #ff8b61 /
 *  dead 红 #ff6a6c)的色相带 —— 品类徽章不再与「限免」琥珀、OCR 高置信绿、
 *  源健康度互相污染语义;被替三档旧值与实测对比(卡底 #1e202a,WCAG):
 *  #8b5cf6 3.83 ✗ → #cdb6fb 9.02(primary-200,--link 同源);
 *  #3dd68c(ok 绿系)→ #818cf8 5.44(indigo-400);#f5b544(琥珀系)→
 *  #94a3b8 6.32(slate-400)。全表现档 ≥4.5:1,11px 徽章文字过筛。 */
const CATEGORY_PALETTE = [
  "#22d3ee", // 品牌青(8.97)
  "#cdb6fb", // 淡紫(primary-200;替旧品牌紫 #8b5cf6 不达 AA)
  "#818cf8", // 靛蓝(替旧 ok 绿 #3dd68c)
  "#94a3b8", // 冷灰(替旧 warning 琥珀 #f5b544)
  "#60a5fa", // 蓝(6.38)
  "#f472b6", // 粉(6.12)
  "#2dd4bf", // 青绿(8.71;色相独立于 --ok)
  "#fb7185", // 玫红(6.02)
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

/** 源名前缀展示词表(10-08 审计 F9 一屏一词:卡面与 L2 渠道行共用本函数;
 *  telegram-<频道> 去 platform 前缀显本名,rss-/hnrss-/urlwatch-/engine-
 *  同为「协议载体前缀」一并剥除;其余源名全称直出,不猜)。 */
const SOURCE_DISPLAY_PREFIX_RE = /^(telegram|tg|rss|hnrss|urlwatch|engine)[-_.]/i;

/** 源名展示词(去协议载体前缀显可读本名;未匹配词表 = 源名全称原样;
 *  前缀后空残余回源名,不猜。10-08-tg-channel-card 自 feed-screen 收编入
 *  api —— 渠道卡视图模型与卡面头区共用同一词表,聚合函数返回的 label 即
 *  成品词;F9 起网页卡源名行与 L2 渠道行同门)。 */
export function channelDisplayName(source: string | null): string {
  if (source === null) return "未知来源";
  const stripped = source.replace(SOURCE_DISPLAY_PREFIX_RE, "");
  return stripped === "" ? source : stripped;
}

/** first_seen 数值化(缺失/非法 = 负无穷,排序沉底;feedChannelCards 消费) */
function firstSeenValue(iso: string | null | undefined): number {
  if (!iso) return Number.NEGATIVE_INFINITY;
  const value = new Date(iso).getTime();
  return Number.isNaN(value) ? Number.NEGATIVE_INFINITY : value;
}

/** 卡片摘要字符上限(v3,主人令「精炼,不能过长,也不能展示不出来特殊
 *  之处」):一行摘要的硬截断位,CSS truncate 再兜底视觉一行。 */
export const CARD_DIGEST_MAX_CHARS = 72;

/**
 * 正文去标题重复开头(10-08 验收:标题行下正文复述标题,同屏读两遍)。
 * TG 消息 title=首行、content=全文,正文常逐字复述标题 —— 四处消费同一
 * 去重门:条目卡收起摘要 / 详情弹窗正文 / TG 气泡收起正文行 / 墙卡
 * cardDigest。返回**原格式**(保换行,消费侧 whitespace-pre-wrap/行钳);
 * 正文整段与标题相同 = null(无独有信息,不渲染重复行);无标题/不以
 * 标题开头 = 原文原样。 */
export function bodyWithoutTitleDup(item: Pick<FeedItem, "title" | "content">): string | null {
  const content = item.content ?? "";
  if (content.trim() === "") return null;
  const title = (item.title ?? "").trim();
  if (title === "") return content;
  const body = content.replace(/^\s+/, "");
  if (!body.startsWith(title)) return content;
  const rest = body.slice(title.length).replace(/^[\s:：]+/, "");
  return rest === "" ? null : rest;
}

/** 卡片摘要(v3):为卡片描述行产出「内容里的特殊之处」,精炼一行 ——
 *  ① 优惠:价格片段即特殊之处(dealPriceView:限免/现价/原价/折扣);
 *  ② 其余:正文压平取头,且**先经 bodyWithoutTitleDup 去掉与标题重复的
 *     开头**(TG 消息正文常复述标题,不去重则摘要行空转、版本号等独有
 *     信息被挤出;10-08 验收起与条目卡/弹窗/气泡正文行同一去重门);
 *  ③ 无正文回事件词(watch 首纳/有更新);全空 = null(消费侧不渲染
 *     空行)。超长 `…` 收尾。 */
export function cardDigest(item: FeedItem): string | null {
  if (item.price_text != null || item.final_price != null || item.sale_price != null) {
    const deal = dealPriceView(item);
    const bits: string[] = [];
    if (deal.free) bits.push("限免");
    if (deal.current !== null) bits.push(deal.current);
    if (deal.original !== null) bits.push(`原价 ${deal.original}`);
    if (deal.discount !== null && !deal.free) bits.push(`-${deal.discount}%`);
    if (bits.length > 0) return bits.join(" · ");
  }
  const deduped = bodyWithoutTitleDup(item);
  const text =
    deduped !== null
      ? deduped.replace(/\s+/g, " ").trim()
      : item.watch_event != null
        ? item.watch_event === "new"
          ? "首次纳入监控"
          : "目标页有更新"
        : "";
  if (text === "") return null;
  if (text.length <= CARD_DIGEST_MAX_CHARS) return text;
  return `${text.slice(0, CARD_DIGEST_MAX_CHARS)}…`;
}

/** TG 频道公开镜像推导(10-09-tg-category-entry v3 AC11 内置浏览器预览):
 *  从该品类最新条目 url 还原 `https://t.me/s/<频道名>` 公开预览页 ——
 *  t.me 的 /s/ 路径 = 无需登录的消息流网页版(telegram-channels.yaml
 *  采集线同款入口),应用内 WebviewWindow 直开即看。
 *
 *  认得三种形态:`https://t.me/<频道>/<消息id>`(bot/网页线消息锚)、
 *  `https://t.me/s/<频道>(/<id>)`(已是预览链)、`https://t.me/<频道>`(纯频道链)。
 *  不猜(一律 null,按钮置灰如实):`t.me/+邀请链`(私有,无公开镜像)、
 *  非 t.me 域、空 url。频道名口径 = t.me 用户名(字母开头,字母/数字/下划线)。
 */
export function telegramMirrorUrlOf(url: string | null | undefined): string | null {
  if (!url) return null;
  const match = /^https?:\/\/t\.me\/(?:s\/)?([A-Za-z][A-Za-z0-9_]{2,})(?:\/\d+)?\/?(?:[?#].*)?$/.exec(
    url.trim(),
  );
  return match ? `https://t.me/s/${match[1]}` : null;
}

// ---------------------------------------------------------------------------
// 渠道卡(v6 渠道瀑布流,10-09 主人三次纠偏后的最终定调:「卡片 = 信息获取
// 渠道」——一个网站/一个 TG 频道/一个日报源,不是单条消息也不是分类):
// 类型三档判定 + 渠道全集聚合 + 搜索过滤,三件纯函数收编 api 与卡面同源。
// ---------------------------------------------------------------------------

/** 渠道卡类型三档(v6 AC20 类型徽标;engine 词表映射) */
export type ChannelCardKind = "tg" | "site" | "daily";

/** TG 线引擎词表:tg_web(网页线)/ telegram(bot·telethon 线仓内实名);
 *  telethon/bot 为同族别名预留。 */
const TG_ENGINES = new Set(["tg_web", "telegram", "telethon", "bot"]);

/** 日报引擎词表(prompt 生成日报 / store_report 链外日报) */
const DAILY_ENGINES = new Set(["prompt", "store_report"]);

/**
 * 渠道卡类型判定(v8 §4.2 判定次序修正:**前缀优先**):源名前缀
 * (telegram-/tg- 命名规约)先判 → tg;再 engine 词表(prompt/store_report
 * → 日报;tg_web/telegram/telethon/bot → TG);其余 → 网站。与后端
 * `source_kind="im"` 纯前缀词表和五档 channelKindOf 的前缀优先同门 ——
 * v6 版 engine 先于前缀,telegram-durov(engine=static_html,t.me 公开
 * 镜像采集线)被误判 site,2 级列表里 TG 频道混进网站(设计稿实锤),
 * 本批翻正;api 纯函数用例钉「telegram-durov + static_html → tg」。health
 * 词表外的源(engine 缺席)同样走前缀判定,词表漂移零风险。
 */
export function channelCardKindOf(source: string, engine?: string | null): ChannelCardKind {
  if (TELEGRAM_SOURCE_RE.test(source)) return "tg";
  const normalized = (engine ?? "").trim().toLowerCase();
  if (DAILY_ENGINES.has(normalized)) return "daily";
  if (TG_ENGINES.has(normalized)) return "tg";
  return "site";
}

/** 渠道卡视图模型(v6 AC20):渠道全集一卡一渠道 */
export interface FeedChannelCardData {
  /** 源名全称(items.source / health sources[].name;渠道详情作用域键) */
  key: string;
  /** 展示名(channelDisplayName 词表) */
  label: string;
  /** 类型三档(类型徽标;TG 详情 = 聊天时间线,其余 = 条目卡列表) */
  kind: ChannelCardKind;
  /** 今日条数(当日窗 03:00 起;已加载口径,过 STATS 门被 applySourceStats
   *  覆写为全库真值) */
  today: number;
  /** 未读数(已加载条目中的未读,不限今日;过 STATS 门同上覆写) */
  unread: number;
  /** 最新一条(first_seen 最大;cardDigest 预览与相对时间源;零条目 = null) */
  latest: FeedItem | null;
  /** stats 回填(v8 §2.3,applySourceStats 落):该源最新标题/时刻全库真值
   *  —— catalog 首页 50 外的活跃源行预览在 card.latest 缺席时用此显一行,
   *  消灭「今日暂无新条目」假知会;未过 STATS 门 = 字段缺省 undefined */
  statsLatestTitle?: string | null;
  statsLatestSeen?: string | null;
}

/**
 * 渠道全集 → 渠道卡(v6 AC20):全集 = health 词表源(engineBySource 的键,
 * **零条目渠道也出卡**显今日 0)∪ 已加载条目 source,去重。计数从已加载
 * 条目聚合(首屏铺底 = store.items 首页 50,消费侧 title 注明「已加载口径」):
 * today 按 当日窗(03:00 窗锚;later 到期重现视同显式留存计回),unread
 * 不限窗。latest = first_seen 最大者(缺失/非法刻沉底)。排序 = 有最新
 * 条目的渠道按最新新→旧,零条目渠道沉底(按 key 稳定 tiebreak)。now 注入
 * 以便测试(later 到期判定)。
 */
export function feedChannelCards(
  items: FeedItem[],
  states: FeedStateMap,
  engineOfSource: ReadonlyMap<string, string>,
  windowStart: Date,
  now: Date = new Date(),
): FeedChannelCardData[] {
  const keys = new Set<string>(engineOfSource.keys());
  for (const item of items) {
    if (item.source) keys.add(item.source);
  }
  const rows: FeedChannelCardData[] = [];
  for (const key of keys) {
    if (key === "") continue;
    let latest: FeedItem | null = null;
    let today = 0;
    let unread = 0;
    for (const item of items) {
      if (item.source !== key) continue;
      if (latest === null || firstSeenValue(item.first_seen) > firstSeenValue(latest.first_seen)) {
        latest = item;
      }
      if (
        inDayWindow(item.first_seen, windowStart) ||
        isLaterResurface(item, states[itemKey(item)], now)
      ) {
        today += 1;
      }
      if (!(states[itemKey(item)]?.read === true)) unread += 1;
    }
    rows.push({
      key,
      label: channelDisplayName(key),
      kind: channelCardKindOf(key, engineOfSource.get(key)),
      today,
      unread,
      latest,
    });
  }
  return rows.sort((a, b) => {
    const diff =
      firstSeenValue(b.latest?.first_seen ?? null) - firstSeenValue(a.latest?.first_seen ?? null);
    return diff !== 0 ? diff : a.key.localeCompare(b.key);
  });
}

/** 渠道类型别名词表(TG 是平台俗名:搜「Tg」须直出全部 TG 渠道卡 ——
 *  字面包含匹配碰不到 "telegram"(t、g 不相邻),v6.1 服务端全文检索靠的
 *  是条目正文里的 TG 字样,渠道卡过滤没有正文可搜,类型别名补上这条主人
 *  实测主路径;网站/日报同构一词)。 */
const CHANNEL_KIND_ALIASES: Record<ChannelCardKind, string[]> = {
  tg: ["tg", "telegram"],
  site: ["web", "网站", "网址"],
  daily: ["daily", "日报"],
};

/**
 * 渠道卡搜索过滤(v6 AC21,主人实测「搜 Tg 出不来 telegram 卡片」的渠道版
 * 直答):query 按渠道名(label)/源 id(key)**包含匹配**,大小写不敏感;
 * 渠道类型别名同认(query 是该渠道类型的别名或其前缀也算命中,「Tg」直出
 * 全部 TG 渠道卡)。空串 = 全量原样。客户端过滤,不发服务端查询。
 */
export function filterChannelsByQuery(
  cards: FeedChannelCardData[],
  query: string,
): FeedChannelCardData[] {
  const q = query.trim().toLowerCase();
  if (q === "") return cards;
  return cards.filter((card) => {
    if (`${card.key} ${card.label}`.toLowerCase().includes(q)) return true;
    return (CHANNEL_KIND_ALIASES[card.kind] ?? []).some(
      (alias) => alias === q || alias.startsWith(q),
    );
  });
}

// ---------------------------------------------------------------------------
// 类型卡(v8 三级界面 1 级):类型 = 渠道类型三档(tg/site/daily)的归并视图
// —— 1 级回答媒介问题(从哪种渠道获取信息),渠道成员集合由 2 级展开;
// 统计走 store.source_stats 分源聚合(全库真值,无首页 50 截断假象)。
// ---------------------------------------------------------------------------

/** 类型卡展示名(api 自持词表:类型管导航;feed-screen 的 CHANNEL_CARD_META
 *  图标/色调随此 label,聚合层自持防 api↔screen 循环导入) */
export const CHANNEL_CARD_LABELS: Record<ChannelCardKind, string> = {
  tg: "TG",
  site: "网站",
  daily: "日报",
};

/** 类型卡固定序(词表序 tg → site → daily,稳定心智模型,不按计数跳动) */
export const CHANNEL_CARD_ORDER: readonly ChannelCardKind[] = ["tg", "site", "daily"];

/** 类型卡最新预览行(成员渠道按 latest_first_seen 降序取前 3) */
export interface TypeCardPreview {
  /** 成员渠道展示名(channelDisplayName 词表) */
  channelLabel: string;
  /** 该渠道最新一条标题(stats 全库真值优先,catalog 铺底回退;零条目 = null) */
  latestTitle: string | null;
  /** 该渠道最新入库时刻(排序键 + 相对时间源) */
  firstSeen: string | null;
}

/** 类型卡视图模型(v8 1 级):一类型一卡 */
export interface TypeCardData {
  kind: ChannelCardKind;
  /** 展示名(CHANNEL_CARD_LABELS) */
  label: string;
  /** 成员渠道数(health 枚举完整,无截断面) */
  channels: number;
  /** 今日条数(当日窗 03:00 起;过 STATS 门 = 全库真值,未过 = catalog 已加载口径) */
  today: number;
  /** 未读数(同上双口径) */
  unread: number;
  /** 最新预览 2-3 条(§1.2;零条目类型 = 空数组,卡内出知会词) */
  previews: TypeCardPreview[];
  /** stats 覆写是否在场(过 STATS 门且应答已落;计数 title 双口径词面用:
   *  过门 = 「全库口径(store.source_stats 分源聚合)」,未过 = 「已加载口径」) */
  statsApplied: boolean;
}

/**
 * 渠道卡全集 + 分源统计 → 类型卡(v8 §5.2 聚合,诚实口径):
 * - 类型以仓内现存源划分,零渠道类型不出卡(health 词表外类型不猜);
 * - 计数优先取 sourceStats 行归并(全库真值);statsRows = null(未过门/
 *   应答缺失)回退 catalog 已加载口径(statsApplied=false,title 如实);
 * - NULL source 行(schema 允许,活库 0 条)计入「网站」卡的 today/unread、
 *   **不计渠道数**(它不是渠道)——只把 site 档计入,null 行对 tg/daily 不沾;
 * - previews = 成员源按 latest_first_seen 降序取 3(stats 的 latest_title/
 *   latest_first_seen 优先,catalog 最新条目回退;两者皆缺 = 行不产)。
 */
export function aggregateTypeCards(
  cards: FeedChannelCardData[],
  statsRows: SourceStatsRow[] | null,
): TypeCardData[] {
  const result: TypeCardData[] = [];
  for (const kind of CHANNEL_CARD_ORDER) {
    const members = cards.filter((card) => card.kind === kind);
    if (members.length === 0) continue;
    const memberKeys = new Set(members.map((member) => member.key));
    let today = 0;
    let unread = 0;
    if (statsRows !== null) {
      for (const row of statsRows) {
        // NULL source 行归「网站」(site 档),不计渠道数也不进 tg/daily
        if (row.source === null) {
          if (kind === "site") {
            today += row.today;
            unread += row.unread;
          }
          continue;
        }
        if (!memberKeys.has(row.source)) continue;
        today += row.today;
        unread += row.unread;
      }
    } else {
      for (const member of members) {
        today += member.today;
        unread += member.unread;
      }
    }
    const statsBySource = new Map(
      (statsRows ?? []).filter((row) => row.source !== null).map((row) => [row.source as string, row]),
    );
    const previews = members
      .map((member) => {
        const row = statsBySource.get(member.key) ?? null;
        const firstSeen = row?.latest_first_seen ?? member.latest?.first_seen ?? null;
        const latestTitle = row?.latest_title ?? member.latest?.title ?? null;
        return { channelLabel: member.label, latestTitle, firstSeen };
      })
      .filter((preview) => preview.firstSeen !== null || preview.latestTitle !== null)
      .sort((a, b) => firstSeenValue(b.firstSeen) - firstSeenValue(a.firstSeen))
      .slice(0, 3);
    result.push({
      kind,
      label: CHANNEL_CARD_LABELS[kind],
      channels: members.length,
      today,
      unread,
      previews,
      statsApplied: statsRows !== null,
    });
  }
  return result;
}

/**
 * 分源统计覆写(v8 §2.3/§5.2):2 级行集的 today/unread 覆写为全库真值,
 * 并回填 statsLatestTitle/statsLatestSeen(catalog 首页 50 外的活跃源,
 * card.latest 缺席时行预览用 stats 值显一行,消灭「今日暂无新条目」假知会)。
 * 该源无 stats 行(零条目渠道)= 原样返回(0 值已是事实,无假知会面)。
 * 未过 STATS 门时消费侧不调用本函数(catalog 口径原样)。
 */
export function applySourceStats(
  cards: FeedChannelCardData[],
  statsRows: SourceStatsRow[],
): FeedChannelCardData[] {
  const statsBySource = new Map(
    statsRows.filter((row) => row.source !== null).map((row) => [row.source as string, row]),
  );
  return cards.map((card) => {
    const row = statsBySource.get(card.key);
    if (!row) return card;
    return {
      ...card,
      today: row.today,
      unread: row.unread,
      statsLatestTitle: row.latest_title,
      statsLatestSeen: row.latest_first_seen,
    };
  });
}

/**
 * 类型卡搜索过滤(v8 1 级,§1.3):query 按类型名 + 别名词表**前缀命中**
 * (搜「Tg」仅 TG 卡直出,v6.1 主人实测路径同门;词表 = CHANNEL_KIND_ALIASES
 * 同源)。空串 = 全量原样。客户端过滤,不发服务端查询。
 */
export function filterTypesByQuery(types: TypeCardData[], query: string): TypeCardData[] {
  const q = query.trim().toLowerCase();
  if (q === "") return types;
  return types.filter((type) => {
    if (type.label.toLowerCase().includes(q)) return true;
    return (CHANNEL_KIND_ALIASES[type.kind] ?? []).some(
      (alias) => alias === q || alias.startsWith(q),
    );
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
