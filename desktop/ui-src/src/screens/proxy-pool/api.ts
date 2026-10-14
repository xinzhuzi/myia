/**
 * 「代理池」屏 IPC 封装(task 10-14-proxy-pool-panel R2/R3;消费方 = 独立屏
 * /proxy-pool)。invoke 直连 sidecar 协议方法,错误归一化走 settings/api 的
 * asSidecarError(惯例同 platform-accounts-api.ts;共享门面接线见任务档
 * integrationSpec,切门面只动本文件内部实现,屏组件零感知)。
 *
 * 契约(与 src/myssia/proxy_panel.py 对齐;注册接线前 sidecar 回
 * method_not_found 结构化错误,不白屏):
 * - `proxy.probe` `{config?, config_auto?, probe_timeout?}` → doctor 应答
 *   原形状 + 纯增键 `snapshot:{persisted, reason?}`(探测照跑,落盘失败
 *   只降级不 fail;dev 无 home → reason="no_home")。
 * - `proxy.history` `{limit?, pool?}` → `{snapshots:[{at,config,pools}…],
 *   count, truncated, home_available, skipped?}`(新→旧,零网络纯读;
 *   limit 钳制 [1,100] 缺省 20;pool 过滤只回该池行;坏行跳过 skipped 如实)。
 *
 * 类型纪律(PRD R2):`ProxyPoolRow` 显式声明 exit_ip/upstream_index/upstreams
 * 三键(解析失败兜底行只有 7 键,exit_ip 可 undefined——渲染侧 undefined
 * 同 null 显「—」),不靠 index signature 兜底猜。
 */
import { invoke } from "@tauri-apps/api/core";

import { asSidecarError } from "@/screens/settings/api";
import type { DoctorResult, SidecarRequestError } from "@/lib/api";

/** 探测应答的池行(doctor proxy.pools 原行;engine ProxyCheckResult.to_dict
 *  + pool/upstream_index/upstreams 三纯增键;凭据永不入行,proxy_url 已打码) */
export interface ProxyPoolRow {
  pool?: string;
  ok?: boolean;
  /** 打码上游 URL(http://***@host:port;红线 4:凭据只此形态出现) */
  proxy_url?: string;
  message?: string;
  latency_seconds?: number | null;
  status_code?: number | null;
  /** 探测端点回的出口 IP;成功但端点未回 IP / 解析失败兜底行 = 缺键或 null */
  exit_ip?: string | null;
  error_type?: string;
  /** 池内序号 / 该池应答行数(兜底行 upstreams=1 是兜底值非声明数) */
  upstream_index?: number;
  upstreams?: number;
}

/** doctor 应答的 proxy 节 */
export interface ProxySection {
  config: string | null;
  pools: ProxyPoolRow[];
  error?: unknown[];
}

/** proxy.probe 应答 = DoctorResult 原形状 + snapshot 纯增键 */
export interface ProxyProbeResult extends Omit<DoctorResult, "proxy"> {
  proxy: ProxySection;
  snapshot: { persisted: boolean; reason?: string };
}

/** 一条探测快照(历史文件一行的投影;pools 行已打码) */
export interface ProxyHistorySnapshot {
  at: string;
  config: string | null;
  pools: ProxyPoolRow[];
}

/** proxy.history 应答(新→旧;home_available=false = dev 无数据根,历史不落盘) */
export interface ProxyHistoryResult {
  snapshots: ProxyHistorySnapshot[];
  count: number;
  truncated: boolean;
  home_available: boolean;
  /** 坏行跳过计数(如实回,前端可忽略) */
  skipped?: number;
  /** pool 过滤给值时回带(应答自描述) */
  pool?: string;
}

/** proxy.probe 参数(DoctorParams 子集:探测两态 + 超时透传) */
export interface ProxyProbeParams {
  config?: string;
  config_auto?: boolean;
  probe_timeout?: number;
}

async function proxyRequest<R>(method: string, params: unknown): Promise<R> {
  try {
    return await invoke<R>("sidecar_request", { method, params });
  } catch (raw) {
    throw asSidecarError(raw);
  }
}

/** 按需探测(唯一网络动作;挂载零调用——进屏只读历史) */
export function proxyProbe(params: ProxyProbeParams): Promise<ProxyProbeResult> {
  return proxyRequest<ProxyProbeResult>("proxy.probe", params);
}

/** 探测历史纯读(缺省最近 20 条;新→旧) */
export function proxyHistory(params: { limit?: number; pool?: string } = {}): Promise<ProxyHistoryResult> {
  return proxyRequest<ProxyHistoryResult>("proxy.history", params);
}

export type { SidecarRequestError };
