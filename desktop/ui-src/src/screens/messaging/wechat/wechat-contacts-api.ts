/**
 * 微信联系人工作台 IPC 封装(10-14-wechat-contacts R4;消费方 =
 * wechat-contacts.tsx ContactsBrowser)。
 *
 * 两条通道:
 * - `wechatLocalContacts(params)` → invoke `sidecar_request` method
 *   `wechat_local.contacts`(sidecar 动作族;方法名与 entry.py 薄壳双侧同步),
 *   应答 = 桥 `localdb contacts --json` 的 `contacts` 内层对象(wire
 *   snake_case 零改形;契约 = 任务档 prd R1 应答契约)。parse 守门判例
 *   parseWechatGroupExportResult:核心判别字段严校,漂移即抛大声失败。
 * - `wechatContactsExport(opts)` → invoke 壳命令 `wechat_contacts_export`
 *   (三格式导出;壳不收大载荷——壳侧 spawn 桥 `--limit 0` 全量取数落盘)。
 *   应答三态:`null` = 用户取消保存对话框(静默语义,面板态机回 idle);
 *   对象 = `{files: [{name, path, rows}], total_rows}`;throw = 失败
 *   (asSidecarError 归一,面板原样上屏)。
 *
 * wire 键注记:壳命令参数名 Rust 侧为 `type_filter`(`type` 是 Rust 关键字),
 * Tauri camelCase 映射后前端键 = `typeFilter`/`withResidue`——两侧文件头注
 * 互指,改任一侧须两侧同步(壳侧 = wechat_contacts_export.rs)。
 */
import { invoke } from "@tauri-apps/api/core";

import { asSidecarError } from "../api";

/** 六桶计数(counts 恒全量,与 filter 无关;system 是诊断桶不呈现行)。 */
export interface WechatContactsCounts {
  friend: number;
  group: number;
  official: number;
  former: number;
  other: number;
  system: number;
}

/** 一行联系人(行形状 = 桥契约;群聊行另带 member_count)。 */
export interface WechatContactRow {
  username: string;
  display_name: string;
  remark: string;
  nickname: string;
  alias: string;
  /** 六桶名(friend/group/official/former/other;system 恒不出行)。 */
  type: string;
  local_type: number | null;
  /** 考古证据(msg_residue=会话痕迹 / identity_fields=身份字段残留)。 */
  evidence: string[];
  description: string | null;
  member_count?: number;
}

/** stranger 表原样行(「非好友联系人缓存」独立子卡,不混入 former 计数)。 */
export interface WechatStrangerRow {
  username: string;
  display_name: string;
  local_type: number | null;
  remark: string;
}

/** `wechat_local.contacts` 应答(桥 R1 契约内层对象)。 */
export interface WechatContactsView {
  counts: WechatContactsCounts;
  /** 仅 with_residue 时非 null(Tier A/B 计数);message 副本缺 = null 如实。 */
  former_tiers: { msg_residue: number; table_only: number } | null;
  residue_checked: boolean;
  /** WeFlow 严判据对照诊断(不出 UI;校准字段)。 */
  strict_residual_count: number;
  labels: Array<{ id: number; name: string }>;
  stranger: WechatStrangerRow[];
  room_verify: { present: boolean; rows: number; sample?: unknown[] };
  rows: WechatContactRow[];
  next_cursor: string | null;
  has_more: boolean;
  filter: {
    type: string | null;
    keyword: string | null;
    with_residue: boolean;
    include_stranger: boolean;
  };
  /** 0 = 全量导出态(帽豁免);正数 = 页大小。 */
  page_size: number;
  /** 缺表/缺列诊断标注(健康时空数组)。 */
  degraded: string[];
}

/** `wechat_local.contacts` 请求参数(全可选;缺省 = 好友桶首页 100 行)。 */
export interface WechatContactsParams {
  type?: string;
  keyword?: string;
  limit?: number;
  cursor?: string;
  with_residue?: boolean;
  include_stranger?: boolean;
}

/** 导出回执单件(路径 + 数据行数)。 */
export interface WechatContactsExportedFile {
  name: string;
  path: string;
  rows: number;
}

/** `wechat_contacts_export` 成功应答(三件成套落盘回执)。 */
export interface WechatContactsExportResult {
  files: WechatContactsExportedFile[];
  total_rows: number;
}

/**
 * contacts 应答守门(判例 parseWechatGroupExportResult 的核心判别字段严校):
 * counts 六键非负整数 / rows 数组 / has_more 布尔 / next_cursor 串或 null,
 * 漂移即抛(桥侧契约已钉死,出现即对齐破了,大声失败)。
 */
export function parseWechatContactsResult(raw: unknown): WechatContactsView {
  if (typeof raw !== "object" || raw === null) {
    throw new TypeError(`contacts 应答不是对象: ${String(raw)}`);
  }
  const record = raw as Record<string, unknown>;
  const counts = record.counts;
  if (typeof counts !== "object" || counts === null) {
    throw new TypeError(`contacts 应答 counts 非对象: ${String(counts)}`);
  }
  for (const key of ["friend", "group", "official", "former", "other", "system"]) {
    const value = (counts as Record<string, unknown>)[key];
    if (typeof value !== "number" || !Number.isInteger(value) || value < 0) {
      throw new TypeError(`contacts 应答 counts.${key} 非非负整数: ${String(value)}`);
    }
  }
  if (!Array.isArray(record.rows)) {
    throw new TypeError(`contacts 应答 rows 非数组: ${String(record.rows)}`);
  }
  if (typeof record.has_more !== "boolean") {
    throw new TypeError(`contacts 应答 has_more 非布尔: ${String(record.has_more)}`);
  }
  if (record.next_cursor !== null && typeof record.next_cursor !== "string") {
    throw new TypeError(`contacts 应答 next_cursor 非串或 null: ${String(record.next_cursor)}`);
  }
  return raw as WechatContactsView;
}

/**
 * 导出回执守门:files 非空数组(元素带非空 path 串 + 非负整数 rows)、
 * total_rows 非负整数;漂移即抛(壳侧 serde 已钉死,出现即对齐破了)。
 */
export function parseWechatContactsExportResult(raw: unknown): WechatContactsExportResult {
  if (typeof raw !== "object" || raw === null) {
    throw new TypeError(`导出回执不是对象: ${String(raw)}`);
  }
  const record = raw as Record<string, unknown>;
  if (!Array.isArray(record.files) || record.files.length === 0) {
    throw new TypeError(`导出回执 files 非非空数组: ${String(record.files)}`);
  }
  for (const file of record.files) {
    if (typeof file !== "object" || file === null) {
      throw new TypeError(`导出回执 files 元素非对象: ${String(file)}`);
    }
    const entry = file as Record<string, unknown>;
    if (typeof entry.path !== "string" || entry.path === "") {
      throw new TypeError(`导出回执 files[].path 非非空串: ${String(entry.path)}`);
    }
    if (typeof entry.rows !== "number" || !Number.isInteger(entry.rows) || entry.rows < 0) {
      throw new TypeError(`导出回执 files[].rows 非非负整数: ${String(entry.rows)}`);
    }
  }
  if (typeof record.total_rows !== "number" || !Number.isInteger(record.total_rows) || record.total_rows < 0) {
    throw new TypeError(`导出回执 total_rows 非非负整数: ${String(record.total_rows)}`);
  }
  return raw as WechatContactsExportResult;
}

/**
 * 联系人查询(工作台浏览面唯一数据通道;throw = 结构化失败经
 * asSidecarError 归一,面板 ReadOnlyError 直显不重试)。
 */
export async function wechatLocalContacts(params: WechatContactsParams): Promise<WechatContactsView> {
  try {
    const raw = await invoke<unknown>("sidecar_request", {
      method: "wechat_local.contacts",
      params,
    });
    return parseWechatContactsResult(raw);
  } catch (raw) {
    throw asSidecarError(raw);
  }
}

/**
 * 导出当前筛选(三格式成套;`null` = 用户取消保存对话框,静默返回面板
 * 不提示;对象 = 落盘回执;throw = 失败人话)。formats ⊆ ["json","csv","vcf"]。
 */
export async function wechatContactsExport(options: {
  type: string;
  keyword?: string;
  withResidue?: boolean;
  formats: string[];
}): Promise<WechatContactsExportResult | null> {
  try {
    const raw = await invoke<unknown>("wechat_contacts_export", {
      typeFilter: options.type,
      keyword: options.keyword || null,
      withResidue: options.withResidue ?? false,
      formats: options.formats,
    });
    return raw === null ? null : parseWechatContactsExportResult(raw);
  } catch (raw) {
    throw asSidecarError(raw);
  }
}
