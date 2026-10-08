/**
 * 浏览器专用模块 IPC 封装(10-08-browser-module 案甲;消费方 = 设置屏
 * 「浏览器」分区模块页 + Telegram 总卡的登录动作)。
 *
 * PRD 单入口铁律:一切浏览器操作(tg_web 登录打头)必经本模块 API,
 * 禁止任何功能旁路直启 Chromium。契约四方法(与 desktop/entry.py 对齐,
 * v11):
 * - `browser.open {kind, session_key, url?, force?}` → `{started, op_id,
 *   kind, url?}`(后台线程拉起 headed 登录窗;依赖缺失等失败同步结构化
 *   拒——错误人话+修复指引,静默失败=反模式)
 * - `browser.list {}` → `{operations: [{op_id, kind, session_key, url,
 *   phase, note, fix_hint, started_at, finished_at, log_tail[]}]}`(操作
 *   台账,最新在前;phase = running/done/failed/closed)
 * - `browser.focus {op_id}` → `{focused}`(进行中窗口带到前台)
 * - `browser.close {op_id}` → `{closed}`(请求关窗,台账转 closed)
 */
import { invoke } from "@tauri-apps/api/core";

import { asSidecarError } from "./api";
import type { SidecarRequestError } from "@/lib/api";

/** 浏览器操作台账行(wire snake_case;phase 词表 = running/done/failed/closed) */
export interface BrowserOperation {
  op_id: string;
  kind: string;
  session_key: string;
  url: string | null;
  phase: "running" | "done" | "failed" | "closed";
  note: string | null;
  fix_hint: string | null;
  started_at: string | null;
  finished_at: string | null;
  log_tail: string[];
}

/** browser.list 载荷(台账 + 已登记操作类别) */
export interface BrowserListResult {
  operations: BrowserOperation[];
  kinds: Record<string, string>;
}

/** browser.open 回执(started=false = 同操作窗口已在跑) */
export interface BrowserOpenResult {
  started: boolean;
  op_id: string;
  kind?: string;
  url?: string | null;
  note?: string;
}

async function browserRequest<R>(method: string, params: unknown): Promise<R> {
  try {
    return await invoke<R>("sidecar_request", { method, params });
  } catch (raw) {
    throw asSidecarError(raw);
  }
}

/** 统一入口:拉起浏览器操作窗口(首役 kind=tg_web_login;单入口铁律) */
export function browserOpen(
  kind: string,
  sessionKey: string,
  options: { url?: string; force?: boolean } = {},
): Promise<BrowserOpenResult> {
  return browserRequest("browser.open", {
    kind,
    session_key: sessionKey,
    ...(options.url !== undefined ? { url: options.url } : {}),
    ...(options.force !== undefined ? { force: options.force } : {}),
  });
}

/** 操作台账(最新在前;含日志尾巴与修复指引) */
export function browserList(): Promise<BrowserListResult> {
  return browserRequest<BrowserListResult>("browser.list", {});
}

/** 聚焦进行中操作的浏览器窗口(带到前台) */
export function browserFocus(opId: string): Promise<{ focused: boolean; op_id: string }> {
  return browserRequest("browser.focus", { op_id: opId });
}

/** 请求关闭进行中操作的浏览器窗口(台账转 closed) */
export function browserClose(opId: string): Promise<{ closed: boolean; op_id: string; note?: string }> {
  return browserRequest("browser.close", { op_id: opId });
}

export type { SidecarRequestError };
