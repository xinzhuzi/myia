/**
 * 微信本机桥「取钥器」配置 IPC 封装(10-13-wechat-keyprovider B5;消费方 =
 * 「微信账号」卡取钥器配置行)。invoke 直连壳侧 Tauri 命令 `wechat_key_provider`
 * (壳 spawn 安装态桥可执行文件执行 `localdb key-provider set/get/clear`,
 * 配置落桥自有 `<数据根>/wechat-bridge/config.json` 经桥管理命令——前端与壳
 * 都不直写桥配置文件)。错误归一化走 ./api 的 asSidecarError(惯例同
 * platform-accounts-api.ts);桥具名错误族码名/人话/fix_hint 原样上屏。
 *
 * 契约(与 src-tauri/src/wechat_keyprovider.rs 对齐):
 * - `wechat_key_provider {action:"get"}` → `{configured, path, file_exists,
 *   file_executable}`(三态派生唯一真源;path 回存桥配置原字面,可为 null)
 * - `wechat_key_provider {action:"set", path}` → `{ok}`(桥侧校验文件存在
 *   +可执行后才落盘;成功后前端重拉 get 刷新)
 * - `wechat_key_provider {action:"clear"}` → `{ok}`
 * - 错误 = 信封 `{code, path, message[, data.fix_hint]}` JSON 字符串
 */
import { invoke } from "@tauri-apps/api/core";

import { asSidecarError } from "./api";

/** 取钥器配置态(wechat_key_provider get 应答;wire snake_case) */
export interface KeyProviderState {
  /** 桥 config.json 的 key_provider_path 非空 = true */
  configured: boolean;
  /** 已配置的取钥器路径原字面(未配置 = null) */
  path: string | null;
  /** 配置路径的文件存在性(壳侧如实重探;set 后文件可能被删) */
  file_exists: boolean;
  /** 配置路径的可执行性(unix 执行位;非 unix 家族 = 存在即 true) */
  file_executable: boolean;
}

/** 三态视图(设置页「已配置/未配置/文件缺失」的派生口径) */
export type KeyProviderView = "configured" | "unset" | "missing";

/** 配置态 → 三态视图:未配置优先;已配置但文件缺席/不可执行 = 文件缺失。 */
export function keyProviderView(state: KeyProviderState): KeyProviderView {
  if (!state.configured || !state.path) return "unset";
  return state.file_exists && state.file_executable ? "configured" : "missing";
}

/**
 * wire 载荷 → KeyProviderState(TS 侧守门,惯例同 parsePyenvStatus):
 * configured 非布尔即抛(壳侧 serde 已钉死,出现即对齐破了,大声失败);
 * path 宽容 string|null(缺键 = null);两文件键宽容布尔(缺键 = false,
 * 与「文件缺失」三态同形,不拦状态展示)。
 */
export function parseKeyProviderState(raw: unknown): KeyProviderState {
  if (typeof raw !== "object" || raw === null) {
    throw new TypeError(`取钥器配置态载荷不是对象: ${String(raw)}`);
  }
  const record = raw as Record<string, unknown>;
  if (typeof record.configured !== "boolean") {
    throw new TypeError(`取钥器配置态 configured 非布尔: ${String(record.configured)}`);
  }
  return {
    configured: record.configured,
    path: typeof record.path === "string" ? record.path : null,
    file_exists: record.file_exists === true,
    file_executable: record.file_executable === true,
  };
}

async function callKeyProvider(action: string, path?: string): Promise<unknown> {
  try {
    return await invoke("wechat_key_provider", path !== undefined ? { action, path } : { action });
  } catch (raw) {
    throw asSidecarError(raw);
  }
}

/** 读取钥器配置态(设置行初始/保存后刷新的真相源)。 */
export async function wechatKeyProviderGet(): Promise<KeyProviderState> {
  return parseKeyProviderState(await callKeyProvider("get"));
}

/** 保存取钥器路径(桥侧校验存在+可执行;绝对路径,~ 前缀可用)。 */
export async function wechatKeyProviderSet(path: string): Promise<{ ok: boolean }> {
  return (await callKeyProvider("set", path)) as { ok: boolean };
}

/** 清除取钥器配置(回到未配置态;解密时桥会明确报错,不静默降级)。 */
export async function wechatKeyProviderClear(): Promise<{ ok: boolean }> {
  return (await callKeyProvider("clear")) as { ok: boolean };
}
