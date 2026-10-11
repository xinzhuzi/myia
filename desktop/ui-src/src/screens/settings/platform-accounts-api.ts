/**
 * 平台账号 IPC 封装(10-11-platform-account-config;消费方 = 「平台账号」
 * 独立屏)。invoke 直连 sidecar 协议方法(协议 v15),错误归一化走 ./api
 * 的 asSidecarError(惯例同 telegram-api.ts)。裁定语义:本面管「本身账号」
 * (用户对自建应用的 OAuth 授权态),推送机器人凭据归设置→推送,两不相混。
 *
 * 契约(与 desktop/entry.py v15 对齐):
 * - `platform_accounts.status` → `{feishu: {accounts: [{account, label,
 *   authorized_at, refresh_ok, refreshed_at}], authorize_in_progress},
 *   weixin: probe_bridge 七键}`(feishu 静态快照;weixin 零新契约桥三布尔)
 * - `platform_accounts.feishu.authorize {account, label?}` → `{authorize_url,
 *   redirect_uri, account}`(系统浏览器开授权页 + 本地回调端点接 code)
 * - `platform_accounts.feishu.delete {account}` → `{deleted, account}`
 * - `platform_accounts.feishu.probe {account}` → `{account, refresh_ok,
 *   refreshed_at?, reason?}`(刷新闭环探针;失败是状态不是异常)
 */
import { invoke } from "@tauri-apps/api/core";

import { asSidecarError } from "./api";
import type { SidecarRequestError } from "@/lib/api";

/** 飞书账号行(platform_accounts.status 的 feishu.accounts[] 形态,wire snake_case) */
export interface FeishuAccount {
  account: string;
  /** 人读备注名(添加授权时起;主显示面) */
  label: string | null;
  /** 首次授权完成时间(ISO;标记缺省 null) */
  authorized_at: string | null;
  /** 探针状态:true=refresh 闭环通过(绿)/ false=失效(灰,指引重授权)/ null=未探 */
  refresh_ok: boolean | null;
  refreshed_at: string | null;
}

/** 微信桥接段(probe_bridge 七键直传;红线:MYIA 不读 Hermes 私有内容) */
export interface WeixinBridgeStatus {
  available: boolean;
  reason?: string | null;
  fix_hint?: string | null;
  bin_found?: boolean;
  weixin_configured?: boolean;
  gateway_alive?: boolean;
  bin_path?: string | null;
}

/** platform_accounts.status 载荷 */
export interface PlatformAccountsStatus {
  feishu: {
    accounts: FeishuAccount[];
    authorize_in_progress: boolean;
  };
  weixin: WeixinBridgeStatus;
}

async function platformRequest<R>(method: string, params: unknown): Promise<R> {
  try {
    return await invoke<R>("sidecar_request", { method, params });
  } catch (raw) {
    throw asSidecarError(raw);
  }
}

/** 平台账号快照(拉取是真相源;授权完成态由轮询/手动刷新对账) */
export function platformAccountsGetStatus(): Promise<PlatformAccountsStatus> {
  return platformRequest<PlatformAccountsStatus>("platform_accounts.status", {});
}

/**
 * 发起飞书账号授权:返回授权页 URL,调用方用系统浏览器打开(window.open);
 * 本地回调端点接 code 换 token,完成后 platform_accounts.status 即见新账号。
 * App 凭据缺失等失败同步结构化拒(人话指引)。
 */
export function feishuAccountAuthorize(
  account: string,
  label?: string,
): Promise<{ authorize_url: string; redirect_uri: string; account: string }> {
  return platformRequest("platform_accounts.feishu.authorize", {
    account,
    ...(label !== undefined && label !== "" ? { label } : {}),
  });
}

/** 删除飞书账号(钥匙链 token + 账号目录;授权进行中被侧拒) */
export function feishuAccountDelete(
  account: string,
): Promise<{ deleted: boolean; account: string }> {
  return platformRequest("platform_accounts.feishu.delete", { account });
}

/** 刷新闭环探针(「重新检查」钮;refresh_ok=false 时带 reason 置灰) */
export function feishuAccountProbe(
  account: string,
): Promise<{ account: string; refresh_ok: boolean; refreshed_at?: string; reason?: string }> {
  return platformRequest("platform_accounts.feishu.probe", { account });
}

export type { SidecarRequestError };
