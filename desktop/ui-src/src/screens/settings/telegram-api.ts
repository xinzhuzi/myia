/**
 * Telegram 监控 IPC 封装(10-08-tg-web-line W4;消费方 = 设置屏 Telegram
 * 总卡)。invoke 直连 sidecar 协议方法,错误归一化走 ./api 的 asSidecarError
 * (惯例同 pyenv-api.ts)。契约(与 desktop/entry.py 对齐):
 *
 * - `telegram.status` → `{bot: {configured, error}, session: {exists},
 *   web: {accounts: [{account, logged_in, logged_in_at, label?, user_id?,
 *   last_verified_at?, alive?, login_in_progress, login_note,
 *   check_in_progress?, check_note?}]}}`(只读零副作用;web 段登录中/
 *   失败态真源 = 浏览器模块操作台账,体检中/结果 note 真源 = 体检台账,
 *   体检结论 last_verified_at/alive 从登录标记透传 —— 双键语义:alive 不
 *   覆盖 logged_in;10-11-tg-manage-absorb 批新键全可选,旧壳忽略照跑)
 * - `telegram.web.delete {account}` → `{deleted, account}`(配置档整档删除)
 * - `telegram.web.check {account}` → `{started, account, note}`(账号体检:
 *   同键在跑 started:false 幂等回执;常态读常驻哨兵真源秒回,无常驻占用
 *   走无头探针后台线程,结果经 telegram.status 行小字回读)
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
  /** 人读备注名(登录时起;主显示面——内部键名认不出是哪个号,2026-10-11) */
  label?: string | null;
  /** 登录会话捕获的 TG user id(观测键,best-effort) */
  user_id?: string | null;
  /** 最近一次体检时刻(登录标记透传;null/缺 = 从未体检) */
  last_verified_at?: string | null;
  /** 最近一次体检结论(null/缺 = 从未体检;与 logged_in 并存不覆盖) */
  alive?: boolean | null;
  login_in_progress: boolean;
  login_note: string | null;
  /** 体检进行中/结果 note 真源 = 体检台账(10-11-tg-manage-absorb) */
  check_in_progress?: boolean;
  check_note?: string | null;
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
 * label = 可选账号备注名(随登录标记落盘,卡面主显示)。
 */
export function telegramWebLogin(
  account: string,
  force = false,
  label?: string,
): Promise<BrowserOpenResult> {
  return browserOpen("tg_web_login", account, {
    force,
    ...(label !== undefined ? { label } : {}),
  });
}

/** 删除账号配置档(登录态随档消失;登录窗在跑会被侧拒 login_in_progress) */
export function telegramWebDelete(
  account: string,
): Promise<{ deleted: boolean; account: string }> {
  return telegramRequest("telegram.web.delete", { account });
}

/**
 * 账号体检(10-11-tg-manage-absorb):常驻监控在跑时读哨兵真源秒回
 * (零浏览器零锁冲突);无常驻占用走无头探针后台线程(≤45s),被占用时
 * failed note 人话引导先停占用。结果经 telegram.status 的行小字回读
 * (last_verified_at/alive/check_note),本回执只报发起。
 */
export function telegramWebCheck(
  account: string,
): Promise<{ started: boolean; account: string; note?: string | null }> {
  return telegramRequest("telegram.web.check", { account });
}

export type { SidecarRequestError };
