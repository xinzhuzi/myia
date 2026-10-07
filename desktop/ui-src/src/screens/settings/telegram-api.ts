/**
 * Telegram 监控 IPC 封装(10-08-tg-web-line W4;消费方 = 设置屏 Telegram
 * 总卡)。invoke 直连 sidecar 协议方法,错误归一化走 ./api 的 asSidecarError
 * (惯例同 pyenv-api.ts);契约三方法(与 desktop/entry.py 对齐):
 *
 * - `telegram.status` → `{bot: {configured, error}, session: {exists},
 *   web: {accounts: [{account, logged_in, logged_in_at, login_in_progress,
 *   login_note}]}}`(只读零副作用;bot = keychain token 在册探查,值零回显)
 * - `telegram.web.login {account, force?}` → `{started, account?}`(后台
 *   headed 登录窗;手机号+验证码全在页面内,sidecar 零读取零落日志)
 * - `telegram.web.delete {account}` → `{deleted, account}`(配置档整档删除)
 */
import { invoke } from "@tauri-apps/api/core";

import { asSidecarError } from "./api";
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

/** 拉起 headed 登录窗(后台线程;同键在跑 = started:false 幂等回执) */
export function telegramWebLogin(
  account: string,
  force = false,
): Promise<{ started: boolean; account?: string; note?: string }> {
  return telegramRequest("telegram.web.login", { account, force });
}

/** 删除账号配置档(登录态随档消失;登录窗在跑会被侧拒 login_in_progress) */
export function telegramWebDelete(
  account: string,
): Promise<{ deleted: boolean; account: string }> {
  return telegramRequest("telegram.web.delete", { account });
}

export type { SidecarRequestError };
