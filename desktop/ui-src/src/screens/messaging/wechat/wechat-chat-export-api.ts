/**
 * 微信聊天记录导出 IPC 封装(task 10-14-wechat-chat-export R6;消费方 =
 * 「微信本机」只读会话入口导出行)。invoke 直连壳命令 `wechat_chat_export`
 * (壳 spawn 桥 `localdb export`,NDJSON 进度转事件);错误归一化走 ./api
 * 的 asSidecarError(惯例同 wechat-keyprovider-api.ts)。
 *
 * 契约(与 src-tauri/src/wechat_chat_export.rs 对齐):
 * - command `wechat_chat_export {chatId, format, outDir?, fromTs?, toTs?,
 *   types?, sender?, displayNamePref?, nameMode?, all?}`(camelCase → 壳侧
 *   snake_case 自动换轨)→ 回包 = 桥终态行**原样**:`{"export": …}` 成功
 *   / `{"error": …}` 桥侧失败;`null` = 用户取消目录选择(静默,不报错)
 * - event `wechat-chat-export-progress`:载荷 `{job_id, seq, body}`,body =
 *   桥行原样(`{"progress":…}` 流 / start 合成行 seq=0 携 job_id 寻址键)
 * - command `wechat_chat_export_cancel {jobId}` → `{ok: boolean}`
 * - 错误 = 信封 `{code, path, message}` JSON 字符串
 */
import { invoke } from "@tauri-apps/api/core";
import { listen, type UnlistenFn } from "@tauri-apps/api/event";

import { asSidecarError } from "../api";

/** 导出进度事件名(与壳侧 WECHAT_CHAT_EXPORT_EVENT 常量同值成对,改值须两侧同步)。 */
export const WECHAT_CHAT_EXPORT_EVENT_NAME = "wechat-chat-export-progress";

/** 六格式封闭词表(桥 CLI --format 同源;label = UI 人话,文案判例 AC-P5)。 */
export const WECHAT_CHAT_EXPORT_FORMATS: ReadonlyArray<{ value: WechatChatExportFormat; label: string }> = [
  { value: "json", label: "JSON 文件" },
  { value: "txt", label: "纯文本" },
  { value: "csv", label: "CSV 表格" },
  { value: "md", label: "Markdown" },
  { value: "html", label: "网页" },
  { value: "xlsx", label: "Excel 表格" },
];

export type WechatChatExportFormat = "json" | "txt" | "csv" | "md" | "html" | "xlsx";

/** 导出请求参数(wire camelCase;outDir 缺省 = 壳内目录对话框)。 */
export interface WechatChatExportParams {
  chatId: string;
  format: WechatChatExportFormat;
  outDir?: string;
  fromTs?: number;
  toTs?: number;
  types?: string[];
  sender?: string;
  displayNamePref?: "remark-first" | "nickname-first";
  nameMode?: "classic" | "date-range";
  all?: boolean;
}

/** 导出件清单条目(manifest 同形)。 */
export interface WechatChatExportFile {
  name: string;
  path: string;
  rows: number;
  sha256: string;
}

/** 成功回执(桥 R5 契约的 `export` 对象,wire snake_case 原样)。 */
export interface WechatChatExportReceipt {
  chat_id: string | null;
  display_name: string | null;
  format: WechatChatExportFormat;
  files: WechatChatExportFile[];
  manifest_path: string;
  total_rows: number;
  time_range: { from_ts: number; to_ts: number } | null;
  elapsed_ms: number;
}

/** 进度行(progress 对象;phase ∈ scan|write|chat|starting,rows 单调)。 */
export interface WechatChatExportProgress {
  phase: string;
  rows: number;
  current_chat?: string;
  pct_est?: number;
}

/** 进度事件载荷(壳侧拼装:桥行原样 + job_id/seq 寻址)。 */
export interface WechatChatExportEvent {
  job_id: number;
  seq: number;
  body: { progress?: WechatChatExportProgress } & Record<string, unknown>;
}

/**
 * wire 载荷 → 回执(TS 侧守门,惯例同 parseKeyProviderState:关键字段形状
 * 漂移即抛 TypeError 大声失败,不静默装成功);files 元素残缺(非对象/
 * 缺 path)丢弃该条不拦整单(单件漂移判例同壳侧 member 行)。
 */
export function parseWechatChatExportReceipt(raw: unknown): WechatChatExportReceipt {
  if (typeof raw !== "object" || raw === null) {
    throw new TypeError(`导出回执不是对象: ${String(raw)}`);
  }
  const record = raw as Record<string, unknown>;
  if (typeof record.total_rows !== "number" || typeof record.manifest_path !== "string") {
    throw new TypeError(
      `导出回执缺 total_rows/manifest_path(壳桥契约漂移): ${JSON.stringify(record).slice(0, 120)}`,
    );
  }
  const files = Array.isArray(record.files)
    ? record.files.filter(
        (file): file is WechatChatExportFile =>
          typeof file === "object" &&
          file !== null &&
          typeof (file as WechatChatExportFile).name === "string" &&
          typeof (file as WechatChatExportFile).path === "string" &&
          typeof (file as WechatChatExportFile).rows === "number",
      )
    : [];
  const timeRange =
    typeof record.time_range === "object" && record.time_range !== null
      ? record.time_range as { from_ts: number; to_ts: number }
      : null;
  return {
    chat_id: typeof record.chat_id === "string" ? record.chat_id : null,
    display_name: typeof record.display_name === "string" ? record.display_name : null,
    format: (typeof record.format === "string" ? record.format : "json") as WechatChatExportFormat,
    files,
    manifest_path: record.manifest_path,
    total_rows: record.total_rows,
    time_range: timeRange,
    elapsed_ms: typeof record.elapsed_ms === "number" ? record.elapsed_ms : 0,
  };
}

/**
 * 发起导出:`null` = 用户取消目录选择(静默);`{"export":…}` → 回执;
 * `{"error":…}` → SidecarRequestError(壳桥错误族原样上屏)。
 */
export async function wechatChatExport(
  params: WechatChatExportParams,
): Promise<WechatChatExportReceipt | null> {
  const wire: Record<string, unknown> = {
    chatId: params.chatId,
    format: params.format,
  };
  if (params.outDir !== undefined) wire.outDir = params.outDir;
  if (params.fromTs !== undefined) wire.fromTs = params.fromTs;
  if (params.toTs !== undefined) wire.toTs = params.toTs;
  if (params.types !== undefined && params.types.length > 0) wire.types = params.types;
  if (params.sender !== undefined) wire.sender = params.sender;
  if (params.displayNamePref !== undefined) wire.displayNamePref = params.displayNamePref;
  if (params.nameMode !== undefined) wire.nameMode = params.nameMode;
  if (params.all !== undefined) wire.all = params.all;
  let raw: unknown;
  try {
    raw = await invoke("wechat_chat_export", wire);
  } catch (thrown) {
    throw asSidecarError(thrown);
  }
  if (raw === null || raw === undefined) return null; // 用户取消目录选择
  if (typeof raw === "object" && raw !== null && "export" in raw) {
    return parseWechatChatExportReceipt((raw as Record<string, unknown>).export);
  }
  if (typeof raw === "object" && raw !== null && "error" in raw) {
    throw asSidecarError(JSON.stringify((raw as Record<string, unknown>).error));
  }
  throw new TypeError(`导出回包形状不可识别: ${JSON.stringify(raw).slice(0, 120)}`);
}

/**
 * 订阅导出进度事件(返回退订函数;handler 收宽容解析:形状异常行丢弃不炸,
 * 判例同 parse 事件流)。job_id 从事件捕获,供取消寻址。
 */
export async function subscribeWechatChatExportProgress(
  handler: (event: WechatChatExportEvent) => void,
): Promise<UnlistenFn> {
  return listen<unknown>(WECHAT_CHAT_EXPORT_EVENT_NAME, (event) => {
    const parsed = parseWechatChatExportEvent(event.payload);
    if (parsed !== null) handler(parsed);
  });
}

/** 事件载荷守门:`{job_id, seq, body{progress}}` 齐备才算导出进度事件。 */
export function parseWechatChatExportEvent(raw: unknown): WechatChatExportEvent | null {
  if (typeof raw !== "object" || raw === null) return null;
  const record = raw as Record<string, unknown>;
  if (typeof record.job_id !== "number" || typeof record.seq !== "number") return null;
  const body = record.body;
  if (typeof body !== "object" || body === null || !("progress" in body)) return null;
  return raw as WechatChatExportEvent;
}

/** 取消进行中的导出(job_id = 进度事件捕获);无在途 = {ok:false} 如实。 */
export async function wechatChatExportCancel(jobId: number): Promise<{ ok: boolean }> {
  try {
    return await invoke<{ ok: boolean }>("wechat_chat_export_cancel", { jobId });
  } catch (thrown) {
    throw asSidecarError(thrown);
  }
}

export type { UnlistenFn };
