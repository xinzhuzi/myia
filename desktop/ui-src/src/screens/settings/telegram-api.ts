/**
 * Telegram 监控 IPC 封装(10-08-tg-web-line W4;消费方 = 设置屏 Telegram
 * 总卡)。invoke 直连 sidecar 协议方法,错误归一化走 ./api 的 asSidecarError
 * (惯例同 pyenv-api.ts)。契约(与 desktop/entry.py v11 对齐):
 *
 * - `telegram.status` → `{bot: {configured, error}, session: {exists},
 *   web: {accounts: [{account, logged_in, logged_in_at, login_in_progress,
 *   login_note}]}}`(只读零副作用;web 段登录中/失败态真源 = 浏览器模块
 *   操作台账,卡面 ↔ 模块同源联动)
 * - `telegram.web.delete {account}` → `{deleted, account}`(配置档整档删除)
 *
 * 登录动作自 10-08-browser-module 起改调浏览器模块统一入口
 * `browser.open {kind: "tg_web_login", session_key, force}`(单入口铁律:
 * 一切浏览器操作必经浏览器模块,禁止旁路直启 Chromium;原
 * telegram.web.login 方法已随协议 v11 移除)——封装见 ./browser-api.ts。
 */
import { invoke } from "@tauri-apps/api/core";

import { asSidecarError } from "./api";
import { browserOpen, type BrowserOpenResult } from "./browser-api";
import type { SidecarRequestError } from "@/lib/api";

/** 网页线账号行(telegram.status 的 web.accounts[] 形态,wire snake_case) */
export interface TelegramWebAccount {
  account: string;
  logged_in: boolean;
  logged_in_at: string | null;
  login_in_progress: boolean;
  login_note: string | null;
}

/** telegram.status 载荷(bot/telethon/web 三线快照) */
export interface TelegramStatus {
  bot: { configured: boolean; error: string | null };
  session: { exists: boolean };
  web: { accounts: TelegramWebAccount[] };
}

async function telegramRequest<R>(method: string, params: unknown): Promise<R> {
  try {
    return await invoke<R>("sidecar_request", { method, params });
  } catch (raw) {
    throw asSidecarError(raw);
  }
}

/** 三线状态快照(拉取是真相源;登录窗完成态由轮询/手动刷新对账) */
export function telegramGetStatus(): Promise<TelegramStatus> {
  return telegramRequest<TelegramStatus>("telegram.status", {});
}

/**
 * 拉起 headed 登录窗(浏览器模块统一入口;单入口铁律)。同操作在跑 =
 * started:false 幂等回执;依赖缺失等失败同步结构化拒(人话+修复指引)。
 */
export function telegramWebLogin(
  account: string,
  force = false,
): Promise<BrowserOpenResult> {
  return browserOpen("tg_web_login", account, { force });
}

/** 删除账号配置档(登录态随档消失;登录窗在跑会被侧拒 login_in_progress) */
export function telegramWebDelete(
  account: string,
): Promise<{ deleted: boolean; account: string }> {
  return telegramRequest("telegram.web.delete", { account });
}

export type { SidecarRequestError };
