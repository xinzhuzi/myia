/**
 * 微信统计报告 IPC 封装(10-14-wechat-stats-reports R6;消费方 = 微信
 * 工作台「统计报告」分区 wx-stats-panel.tsx)。两通道:
 *
 * - 桥统计:invoke 直连壳命令 `sidecar_request` {method:"wechat_local.stats"}
 *   → 桥 `localdb stats <mode> …`(密钥链与 query 同族;查询层降级 =
 *   空结构恒 exit 0,错误族 20/21/22 结构化直显);
 * - AI 报告:`wechat_local.stats_report`(桥不重查,前端已持 stats 载荷
 *   原样回传;隐私缺省 = 聚合数字+短语,零逐条原文);
 * - 导出:壳命令 `wechat_stats_export {default_name, json_payload,
 *   markdown_payload?}`(保存对话框一次 → 同名 .json+.md 两件;
 *   wechat_group_export 判例,两侧成对注释互指)。
 *
 * wire 守门判例 wechat-groupinfo-api.ts:核心判别字段严校,展示字段宽容
 * (缺键 = null,不拦面板);`asSidecarError` 归一化(screens/settings/api)。
 */
import { invoke } from "@tauri-apps/api/core";

import { asSidecarError } from "@/screens/settings/api";

/** 时间窗(近 N 天 | 全时间;annual 用 year|"all" 另走) */
export type StatsWindow = { kind: "since"; days: number } | { kind: "all" };

/** 会话行(stats chats;chats 契约 v1) */
export interface StatsChatEntry {
  chat_id: string;
  display_name: string | null;
  kind: "group" | "official" | "private" | "system";
  message_count: number;
  first_ts: number | null;
  last_ts: number | null;
}

export interface StatsChatsView {
  chats: StatsChatEntry[];
  unattributed_tables: number;
}

/** 类型分布桶(契约十桶固定键) */
export type StatsTypeCounts = Partial<
  Record<
    "text" | "image" | "voice" | "video" | "sticker" | "file_or_link" | "location" | "other" | "system" | "revoke",
    number
  >
>;

/** 连续聊天段({days, from, to};空 = days 0) */
export interface StatsStreak {
  days: number;
  from: string | null;
  to: string | null;
}

export interface StatsPhrase {
  phrase: string;
  count: number;
}

/** stats chat 聚合树(契约 v1) */
export interface StatsChatView {
  chat_id: string;
  display_name: string | null;
  kind: StatsChatEntry["kind"];
  window: { mode: "since" | "all"; from_ts: number; to_ts: number };
  total: number;
  sent: number;
  received: number;
  human_total: number;
  type_counts: StatsTypeCounts;
  hourly: number[];
  weekday: number[];
  monthly: number[];
  daily: Array<{ date: string; count: number }>;
  active_days: number;
  longest_streak: StatsStreak;
  top_phrases: StatsPhrase[];
  senders: Array<{ sender_id: string; display: string; count: number }>;
  sessions: { threshold_minutes: number; total: number; me_initiated: number; other_initiated: number };
  response: {
    avg_seconds: number | null;
    median_seconds: number | null;
    fastest_seconds: number | null;
    pairs: number;
  };
  self_id: string | null;
  first_ts: number | null;
  last_ts: number | null;
  cache: StatsCacheInfo;
}

/** stats annual(契约 v1;子集视图,消费面只读要渲染的字段) */
export interface StatsAnnualView {
  year: number | "all";
  years_available: number[];
  total: number;
  sent: number;
  received: number;
  human_total: number;
  type_counts: StatsTypeCounts;
  hourly: number[];
  weekday: number[];
  monthly: number[];
  active_days: number;
  longest_streak: StatsStreak;
  chats_count: number;
  top_chats: Array<{ chat_id: string; display_name: string | null; count: number }>;
  top_phrases: StatsPhrase[];
  midnight: { count: number; top_chat: { chat_id: string; display_name: string | null; count: number } | null };
  friend_contrast: Array<{ chat_id: string; display_name: string | null; early_count: number; late_count: number }>;
  cache: StatsCacheInfo;
}

/** 双人报告一侧列 */
export interface StatsDualSide {
  count: number;
  initiated: number;
  avg_response_seconds: number | null;
  top_phrases: StatsPhrase[];
}

/** stats dual(契约 v1) */
export interface StatsDualView {
  chat_id: string;
  display_name: string | null;
  window: { mode: "since" | "all"; from_ts: number; to_ts: number };
  first_chat: { ts: number; sender: "me" | "other"; text: string | null } | null;
  me: StatsDualSide;
  other: StatsDualSide;
  heatmap: number[][];
  longest_streak: StatsStreak;
  active_days: number;
  cache: StatsCacheInfo;
}

/** 缓存块(R3:载荷恒带) */
export interface StatsCacheInfo {
  hit: boolean;
  computed_ms: number;
}

/** AI 报告应答(R5) */
export interface StatsReportResult {
  report_markdown: string;
  model: string;
  total_tokens: number;
}

/** 导出回执(R7;markdown 缺席 = 只落 json) */
export interface StatsExportResult {
  json_path: string;
  markdown_path?: string;
}

// ---------------------------------------------------------------------------
// wire 守门(判例 parseWechatGroupInfo:核心判别严校,展示宽容)
// ---------------------------------------------------------------------------

function requireObject(raw: unknown, label: string): Record<string, unknown> {
  if (typeof raw !== "object" || raw === null) {
    throw new TypeError(`${label} 不是对象: ${String(raw)}`);
  }
  return raw as Record<string, unknown>;
}

function numArr(raw: unknown, len: number, label: string): number[] {
  if (!Array.isArray(raw) || raw.length !== len) {
    throw new TypeError(`${label} 须为 ${len} 桶数组: ${String(raw)}`);
  }
  return raw.map((v) => (typeof v === "number" ? v : 0));
}

function parseCache(raw: unknown): StatsCacheInfo {
  const rec = requireObject(raw ?? {}, "cache");
  return {
    hit: rec.hit === true,
    computed_ms: typeof rec.computed_ms === "number" ? rec.computed_ms : 0,
  };
}

function parseStreak(raw: unknown): StatsStreak {
  const rec = requireObject(raw ?? {}, "longest_streak");
  return {
    days: typeof rec.days === "number" ? rec.days : 0,
    from: typeof rec.from === "string" ? rec.from : null,
    to: typeof rec.to === "string" ? rec.to : null,
  };
}

function parsePhrases(raw: unknown): StatsPhrase[] {
  if (!Array.isArray(raw)) return [];
  return raw
    .filter((e): e is Record<string, unknown> => typeof e === "object" && e !== null)
    .filter((e) => typeof e.phrase === "string")
    .map((e) => ({ phrase: String(e.phrase), count: typeof e.count === "number" ? e.count : 0 }));
}

export function parseStatsChats(raw: unknown): StatsChatsView {
  const rec = requireObject(raw, "stats_chats");
  const chatsRaw = Array.isArray(rec.chats) ? rec.chats : [];
  const chats: StatsChatEntry[] = [];
  for (const entry of chatsRaw) {
    const item = requireObject(entry, "chats 行");
    if (typeof item.chat_id !== "string" || item.chat_id === "") continue;
    const kind = item.kind;
    chats.push({
      chat_id: item.chat_id,
      display_name: typeof item.display_name === "string" ? item.display_name : null,
      kind:
        kind === "group" || kind === "official" || kind === "private" || kind === "system"
          ? kind
          : "private",
      message_count: typeof item.message_count === "number" ? item.message_count : 0,
      first_ts: typeof item.first_ts === "number" ? item.first_ts : null,
      last_ts: typeof item.last_ts === "number" ? item.last_ts : null,
    });
  }
  return {
    chats,
    unattributed_tables: typeof rec.unattributed_tables === "number" ? rec.unattributed_tables : 0,
  };
}

export function parseStatsChat(raw: unknown): StatsChatView {
  const rec = requireObject(raw, "stats_chat");
  if (typeof rec.chat_id !== "string" || rec.chat_id === "") {
    throw new TypeError(`stats_chat.chat_id 非字符串: ${String(rec.chat_id)}`);
  }
  const response = requireObject(rec.response ?? {}, "response");
  const sessions = requireObject(rec.sessions ?? {}, "sessions");
  return {
    chat_id: rec.chat_id,
    display_name: typeof rec.display_name === "string" ? rec.display_name : null,
    kind: (rec.kind as StatsChatEntry["kind"]) ?? "private",
    window: (() => {
      const w = requireObject(rec.window ?? {}, "window");
      return {
        mode: w.mode === "all" ? "all" : "since",
        from_ts: typeof w.from_ts === "number" ? w.from_ts : 0,
        to_ts: typeof w.to_ts === "number" ? w.to_ts : 0,
      };
    })(),
    total: typeof rec.total === "number" ? rec.total : 0,
    sent: typeof rec.sent === "number" ? rec.sent : 0,
    received: typeof rec.received === "number" ? rec.received : 0,
    human_total: typeof rec.human_total === "number" ? rec.human_total : 0,
    type_counts: requireObject(rec.type_counts ?? {}, "type_counts") as StatsTypeCounts,
    hourly: numArr(rec.hourly, 24, "hourly"),
    weekday: numArr(rec.weekday, 7, "weekday"),
    monthly: numArr(rec.monthly, 12, "monthly"),
    daily: Array.isArray(rec.daily)
      ? rec.daily
          .filter((d): d is Record<string, unknown> => typeof d === "object" && d !== null)
          .map((d) => ({ date: String(d.date ?? ""), count: typeof d.count === "number" ? d.count : 0 }))
      : [],
    active_days: typeof rec.active_days === "number" ? rec.active_days : 0,
    longest_streak: parseStreak(rec.longest_streak),
    top_phrases: parsePhrases(rec.top_phrases),
    senders: Array.isArray(rec.senders)
      ? rec.senders
          .filter((s): s is Record<string, unknown> => typeof s === "object" && s !== null)
          .filter((s) => typeof s.sender_id === "string")
          .map((s) => ({
            sender_id: String(s.sender_id),
            display: typeof s.display === "string" ? s.display : String(s.sender_id),
            count: typeof s.count === "number" ? s.count : 0,
          }))
      : [],
    sessions: {
      threshold_minutes: typeof sessions.threshold_minutes === "number" ? sessions.threshold_minutes : 30,
      total: typeof sessions.total === "number" ? sessions.total : 0,
      me_initiated: typeof sessions.me_initiated === "number" ? sessions.me_initiated : 0,
      other_initiated: typeof sessions.other_initiated === "number" ? sessions.other_initiated : 0,
    },
    response: {
      avg_seconds: typeof response.avg_seconds === "number" ? response.avg_seconds : null,
      median_seconds: typeof response.median_seconds === "number" ? response.median_seconds : null,
      fastest_seconds: typeof response.fastest_seconds === "number" ? response.fastest_seconds : null,
      pairs: typeof response.pairs === "number" ? response.pairs : 0,
    },
    self_id: typeof rec.self_id === "string" ? rec.self_id : null,
    first_ts: typeof rec.first_ts === "number" ? rec.first_ts : null,
    last_ts: typeof rec.last_ts === "number" ? rec.last_ts : null,
    cache: parseCache(rec.cache),
  };
}

export function parseStatsAnnual(raw: unknown): StatsAnnualView {
  const rec = requireObject(raw, "stats_annual");
  const midnight = requireObject(rec.midnight ?? {}, "midnight");
  const topChat = midnight.top_chat;
  return {
    year: typeof rec.year === "number" ? rec.year : "all",
    years_available: Array.isArray(rec.years_available)
      ? rec.years_available.filter((y): y is number => typeof y === "number")
      : [],
    total: typeof rec.total === "number" ? rec.total : 0,
    sent: typeof rec.sent === "number" ? rec.sent : 0,
    received: typeof rec.received === "number" ? rec.received : 0,
    human_total: typeof rec.human_total === "number" ? rec.human_total : 0,
    type_counts: requireObject(rec.type_counts ?? {}, "type_counts") as StatsTypeCounts,
    hourly: numArr(rec.hourly, 24, "hourly"),
    weekday: numArr(rec.weekday, 7, "weekday"),
    monthly: numArr(rec.monthly, 12, "monthly"),
    active_days: typeof rec.active_days === "number" ? rec.active_days : 0,
    longest_streak: parseStreak(rec.longest_streak),
    chats_count: typeof rec.chats_count === "number" ? rec.chats_count : 0,
    top_chats: Array.isArray(rec.top_chats)
      ? rec.top_chats
          .filter((c): c is Record<string, unknown> => typeof c === "object" && c !== null)
          .map((c) => ({
            chat_id: String(c.chat_id ?? ""),
            display_name: typeof c.display_name === "string" ? c.display_name : null,
            count: typeof c.count === "number" ? c.count : 0,
          }))
      : [],
    top_phrases: parsePhrases(rec.top_phrases),
    midnight: {
      count: typeof midnight.count === "number" ? midnight.count : 0,
      top_chat:
        typeof topChat === "object" && topChat !== null
          ? {
              chat_id: String((topChat as Record<string, unknown>).chat_id ?? ""),
              display_name:
                typeof (topChat as Record<string, unknown>).display_name === "string"
                  ? ((topChat as Record<string, unknown>).display_name as string)
                  : null,
              count: typeof (topChat as Record<string, unknown>).count === "number"
                ? ((topChat as Record<string, unknown>).count as number)
                : 0,
            }
          : null,
    },
    friend_contrast: Array.isArray(rec.friend_contrast)
      ? rec.friend_contrast
          .filter((c): c is Record<string, unknown> => typeof c === "object" && c !== null)
          .map((c) => ({
            chat_id: String(c.chat_id ?? ""),
            display_name: typeof c.display_name === "string" ? c.display_name : null,
            early_count: typeof c.early_count === "number" ? c.early_count : 0,
            late_count: typeof c.late_count === "number" ? c.late_count : 0,
          }))
      : [],
    cache: parseCache(rec.cache),
  };
}

export function parseStatsDual(raw: unknown): StatsDualView {
  const rec = requireObject(raw, "stats_dual");
  if (typeof rec.chat_id !== "string" || rec.chat_id === "") {
    throw new TypeError(`stats_dual.chat_id 非字符串: ${String(rec.chat_id)}`);
  }
  const parseSide = (rawSide: unknown): StatsDualSide => {
    const side = requireObject(rawSide ?? {}, "dual 侧列");
    return {
      count: typeof side.count === "number" ? side.count : 0,
      initiated: typeof side.initiated === "number" ? side.initiated : 0,
      avg_response_seconds: typeof side.avg_response_seconds === "number" ? side.avg_response_seconds : null,
      top_phrases: parsePhrases(side.top_phrases),
    };
  };
  const first = rec.first_chat;
  return {
    chat_id: rec.chat_id,
    display_name: typeof rec.display_name === "string" ? rec.display_name : null,
    window: (() => {
      const w = requireObject(rec.window ?? {}, "window");
      return {
        mode: w.mode === "all" ? "all" : "since",
        from_ts: typeof w.from_ts === "number" ? w.from_ts : 0,
        to_ts: typeof w.to_ts === "number" ? w.to_ts : 0,
      };
    })(),
    first_chat:
      typeof first === "object" && first !== null
        ? {
            ts: typeof (first as Record<string, unknown>).ts === "number"
              ? ((first as Record<string, unknown>).ts as number)
              : 0,
            sender: (first as Record<string, unknown>).sender === "me" ? "me" : "other",
            text: typeof (first as Record<string, unknown>).text === "string"
              ? ((first as Record<string, unknown>).text as string)
              : null,
          }
        : null,
    me: parseSide(rec.me),
    other: parseSide(rec.other),
    heatmap: Array.isArray(rec.heatmap)
      ? rec.heatmap.map((row) => (Array.isArray(row) ? row.map((v) => (typeof v === "number" ? v : 0)) : []))
      : [],
    longest_streak: parseStreak(rec.longest_streak),
    active_days: typeof rec.active_days === "number" ? rec.active_days : 0,
    cache: parseCache(rec.cache),
  };
}

// ---------------------------------------------------------------------------
// 协议封装(sidecar_request;方法名与 entry.py 双侧同步)
// ---------------------------------------------------------------------------

async function callStats(mode: "chats", params: { refresh?: boolean }): Promise<StatsChatsView>;
async function callStats(
  mode: "chat" | "dual",
  params: { chat_id: string; since_days?: number; all?: boolean; refresh?: boolean },
): Promise<StatsChatView | StatsDualView>;
async function callStats(
  mode: "annual",
  params: { year?: number; all?: boolean; refresh?: boolean },
): Promise<StatsAnnualView>;
async function callStats(
  mode: "chats" | "chat" | "annual" | "dual",
  params: Record<string, unknown>,
): Promise<StatsChatsView | StatsChatView | StatsAnnualView | StatsDualView> {
  try {
    const raw = await invoke<Record<string, unknown>>("sidecar_request", {
      method: "wechat_local.stats",
      params: { mode, ...params },
    });
    const inner =
      raw && typeof raw === "object" && `stats_${mode}` in raw
        ? ((raw as Record<string, unknown>)[`stats_${mode}` as string] as unknown)
        : raw;
    switch (mode) {
      case "chats":
        return parseStatsChats(inner);
      case "chat":
        return parseStatsChat(inner);
      case "annual":
        return parseStatsAnnual(inner);
      default:
        return parseStatsDual(inner);
    }
  } catch (raw) {
    throw asSidecarError(raw);
  }
}

/** 会话枚举(报告类型选择的会话清单真源) */
export function wechatStatsChats(refresh = false): Promise<StatsChatsView> {
  return callStats("chats", { refresh });
}

/** 单会话聚合树(私聊/群聊通用) */
export function wechatStatsChat(
  chatId: string,
  window: StatsWindow,
  refresh = false,
): Promise<StatsChatView> {
  return callStats("chat", {
    chat_id: chatId,
    ...(window.kind === "since" ? { since_days: window.days } : { all: true }),
    refresh,
  }) as Promise<StatsChatView>;
}

/** 年度报告(单年或全时间) */
export function wechatStatsAnnual(
  year: number | "all",
  refresh = false,
): Promise<StatsAnnualView> {
  return callStats("annual", {
    ...(year === "all" ? { all: true } : { year }),
    refresh,
  }) as Promise<StatsAnnualView>;
}

/** 双人对照(私聊) */
export function wechatStatsDual(
  chatId: string,
  window: StatsWindow,
  refresh = false,
): Promise<StatsDualView> {
  return callStats("dual", {
    chat_id: chatId,
    ...(window.kind === "since" ? { since_days: window.days } : { all: true }),
    refresh,
  }) as Promise<StatsDualView>;
}

/** AI 叙事报告(桥不重查;statsPayload = 前端已持的桥 stats 应答) */
export async function wechatStatsReport(
  mode: "chat" | "annual" | "dual",
  statsPayload: unknown,
  tone?: string,
): Promise<StatsReportResult> {
  try {
    const raw = await invoke<unknown>("sidecar_request", {
      method: "wechat_local.stats_report",
      params: { mode, stats_payload: statsPayload, ...(tone ? { tone } : {}) },
    });
    const rec = requireObject(raw, "stats_report");
    return {
      report_markdown: typeof rec.report_markdown === "string" ? rec.report_markdown : "",
      model: typeof rec.model === "string" ? rec.model : "",
      total_tokens: typeof rec.total_tokens === "number" ? rec.total_tokens : 0,
    };
  } catch (raw) {
    throw asSidecarError(raw);
  }
}

/** 导出统计树(+ AI 报告)两件落盘;null = 用户取消(静默) */
export async function wechatStatsExport(
  defaultName: string,
  jsonPayload: unknown,
  markdownPayload?: string,
): Promise<StatsExportResult | null> {
  try {
    const raw = await invoke<unknown>("wechat_stats_export", {
      defaultName,
      jsonPayload,
      markdownPayload: markdownPayload ?? null,
    });
    if (raw === null) return null;
    const rec = requireObject(raw, "导出回执");
    if (typeof rec.json_path !== "string" || rec.json_path === "") {
      throw new TypeError(`导出回执 json_path 非字符串: ${String(rec.json_path)}`);
    }
    return {
      json_path: rec.json_path,
      ...(typeof rec.markdown_path === "string" && rec.markdown_path
        ? { markdown_path: rec.markdown_path }
        : {}),
    };
  } catch (raw) {
    throw asSidecarError(raw);
  }
}

/** 年份清单推导(chats 契约的 first_ts/last_ts → 年份;免独立命令) */
export function yearsFromChats(chats: StatsChatEntry[]): number[] {
  const years = new Set<number>();
  const now = new Date().getFullYear();
  for (const chat of chats) {
    for (const ts of [chat.first_ts, chat.last_ts]) {
      if (typeof ts === "number" && ts > 0) years.add(new Date(ts * 1000).getFullYear());
    }
  }
  years.add(now); // 当年恒在(空会话/刚起步也有「年度报告」可选)
  return [...years].sort((a, b) => b - a);
}
