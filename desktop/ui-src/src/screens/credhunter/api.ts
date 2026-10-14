/**
 * 凭证猎手数据装配(本屏私有 api 模块;共享客户端 @/lib/api 只读不动)。
 *
 * 数据面 = sidecar 协议方法 `credhunter.keys.list`(10-14-cred-hunter-panel
 * §3.1 冻结形状:纯文件读本地密钥库,零网络;应答只有服务端算好的
 * `masked_apikey`,全文 `apikey` 在 handler 投影时丢弃,协议流/UI 零全文
 * 密钥)。掩码与指纹都在服务端产出(规则源 = 插件 findings.py 的
 * mask_apikey:前 8 + `…MASKED…` + 后 4,短键 9-12 只前 8、≤8 只前 2;
 * 指纹 sha256 前 16 hex)——前端只显示不重算,本模块不含任何掩码逻辑。
 *
 * 协议类型已入共享映射 @/lib/api/types(SidecarProtocol
 * "credhunter.keys.list" 行,10-14-cred-hunter-panel AC7);本模块 re-export
 * 保持屏内引用点稳定,形状单一事实源 = types.ts(与 §3.1 冻结一致)。
 */
import { invoke } from "@tauri-apps/api/core";

import { SidecarRequestError } from "@/lib/api";
import type { SidecarErrorShape } from "@/lib/api";

// ---------------------------------------------------------------------------
// 协议类型(credhunter.keys.list 应答;已入共享映射 @/lib/api/types —— 本
// 模块 re-export 保持屏内引用点稳定,形状单一事实源 = types.ts)
// ---------------------------------------------------------------------------

import type {
  CredhunterCheckState,
  CredhunterKeyRecord,
  CredhunterKeysListResult,
} from "@/lib/api/types";

export type { CredhunterCheckState, CredhunterKeyRecord, CredhunterKeysListResult };

/** 任意抛出物 → SidecarRequestError(规则与 feed/api.ts G12 节 asSidecarError 相同)。 */
export function asSidecarError(raw: unknown): SidecarRequestError {
  if (raw instanceof SidecarRequestError) return raw;
  if (typeof raw === "string") {
    try {
      const parsed = JSON.parse(raw) as Partial<SidecarErrorShape>;
      if (parsed && typeof parsed.code === "string" && typeof parsed.message === "string") {
        return new SidecarRequestError({
          code: parsed.code,
          path: typeof parsed.path === "string" ? parsed.path : "$",
          message: parsed.message,
          data: parsed.data,
        });
      }
    } catch {
      // 非 JSON 文本:按裸消息包装
    }
    return new SidecarRequestError({ code: "transport_error", path: "$", message: raw });
  }
  return new SidecarRequestError({
    code: "sidecar_unavailable",
    path: "$",
    message: raw instanceof Error ? `Tauri IPC 不可用: ${raw.message}` : `Tauri IPC 不可用: ${String(raw)}`,
  });
}

/** 类型化往返:credhunter.keys.list 经壳命令 sidecar_request,失败归一化抛出。 */
async function sidecarRequest<R>(method: string, params: unknown): Promise<R> {
  try {
    return await invoke<R>("sidecar_request", { method, params });
  } catch (raw) {
    throw asSidecarError(raw);
  }
}

/** 拉取密钥库列表(空参;记录已按 last_seen 新→旧排序,服务端保证)。 */
export function fetchCredhunterKeys(): Promise<CredhunterKeysListResult> {
  return sidecarRequest<CredhunterKeysListResult>("credhunter.keys.list", {});
}

// ---------------------------------------------------------------------------
// 高危判据(单点常量:V2 调整余额阈值/hit_count 组合判据只动这里)
// ---------------------------------------------------------------------------

/**
 * 高危视图判据(PRD §3.3:check_state === final_verified = 已验证存活 =
 * 泄漏且有效,最高活险;rejected 已判死、transient 未定不入选)。
 */
export const HIGH_RISK_STATES: ReadonlySet<string> = new Set(["final_verified"]);

export function isHighRisk(record: CredhunterKeyRecord): boolean {
  return HIGH_RISK_STATES.has(record.check_state ?? "");
}

/** 高危视图行集(全部密钥视图由调用方直接用原 records) */
export function filterHighRisk(records: CredhunterKeyRecord[]): CredhunterKeyRecord[] {
  return records.filter(isHighRisk);
}

// ---------------------------------------------------------------------------
// 状态徽章词表(MYIA 自家三态 + 未验证;文案人话,变体映射 ui/badge 家族)
// ---------------------------------------------------------------------------

export interface CheckStateView {
  /** 徽章文案 */
  label: string;
  /** ui/badge 变体:final_verified→ok(存活)/ rejected→destructive(判死)/
   *  transient→warning(未定)/ 未验证→outline(muted 观感,不用彩色强调) */
  variant: "ok" | "destructive" | "warning" | "outline";
}

const CHECK_STATE_VIEWS: Record<CredhunterCheckState, CheckStateView> = {
  final_verified: { label: "已验证存活", variant: "ok" },
  rejected: { label: "已判死", variant: "destructive" },
  transient: { label: "暂不可判", variant: "warning" },
};

const UNCHECKED_VIEW: CheckStateView = { label: "未验证", variant: "outline" };

/** check_state → 徽章视图(null = 未验证;未知值如实显原值,不谎报为已验证) */
export function checkStateView(state: CredhunterCheckState | null | undefined): CheckStateView {
  if (state === null || state === undefined) return UNCHECKED_VIEW;
  return CHECK_STATE_VIEWS[state] ?? { label: state, variant: "outline" };
}

// ---------------------------------------------------------------------------
// 排序 / 过滤 / 聚合(纯函数,便于测试)
// ---------------------------------------------------------------------------

/** 排序档:hit_count 高→低(缺省)/ last_seen 新→旧 */
export type KeySortMode = "hits" | "recency";

export const KEY_SORT_MODES: { value: KeySortMode; label: string }[] = [
  { value: "hits", label: "按命中数" },
  { value: "recency", label: "按最近发现" },
];

/** last_seen 数值化(缺失/非法 = 负无穷,排序沉底) */
function lastSeenValue(iso: string | null | undefined): number {
  if (!iso) return Number.NEGATIVE_INFINITY;
  const value = new Date(iso).getTime();
  return Number.isNaN(value) ? Number.NEGATIVE_INFINITY : value;
}

/**
 * 排序键记录:hits = hit_count 降序;recency = last_seen 新→旧。各自以
 * fingerprint 稳定 tiebreak(不随数据序抖动);不改原数组(返回新序)。
 */
export function sortKeyRecords(
  records: CredhunterKeyRecord[],
  mode: KeySortMode = "hits",
): CredhunterKeyRecord[] {
  return [...records].sort((a, b) => {
    if (mode === "recency") {
      const delta = lastSeenValue(b.last_seen) - lastSeenValue(a.last_seen);
      return delta !== 0 ? delta : a.fingerprint.localeCompare(b.fingerprint);
    }
    const delta = (b.hit_count ?? 0) - (a.hit_count ?? 0);
    return delta !== 0 ? delta : a.fingerprint.localeCompare(b.fingerprint);
  });
}

/**
 * 掩码域子串搜索:masked_apikey + provider 匹配,大小写不敏感;空串/纯
 * 空白 = 全量原样。客户端过滤,不发服务端查询。
 */
export function filterKeyRecords(records: CredhunterKeyRecord[], query: string): CredhunterKeyRecord[] {
  const q = query.trim().toLowerCase();
  if (q === "") return records;
  return records.filter(
    (record) =>
      record.masked_apikey.toLowerCase().includes(q) || String(record.provider ?? "").toLowerCase().includes(q),
  );
}

/** 供应商聚合计数行(chips 数据源;计数降序,tiebreak 字典序稳定) */
export interface ProviderCount {
  provider: string;
  count: number;
}

export function providerCounts(records: CredhunterKeyRecord[]): ProviderCount[] {
  const byProvider = new Map<string, number>();
  for (const record of records) {
    const provider = String(record.provider ?? "");
    byProvider.set(provider, (byProvider.get(provider) ?? 0) + 1);
  }
  return [...byProvider.entries()]
    .map(([provider, count]) => ({ provider, count }))
    .sort((a, b) => b.count - a.count || a.provider.localeCompare(b.provider, "zh-Hans-CN"));
}

// ---------------------------------------------------------------------------
// 列宽持久化(PRD §3.3:localStorage key credhunter.key-table-columns.v1;
// loadFeedDisplay 同纪律:损坏/非法即弃回缺省,写失败不阻断)
// ---------------------------------------------------------------------------

/** 列宽持久化键(Record<列id, px>) */
export const COLUMN_SIZES_STORAGE_KEY = "credhunter.key-table-columns.v1";

export type ColumnSizes = Record<string, number>;

/** 读取列宽:JSON 损坏/非对象/值非有限正数 → 整体弃用回缺省({}) */
export function loadColumnSizes(
  storage: Storage | null = typeof window === "undefined" ? null : window.localStorage,
): ColumnSizes {
  if (storage === null) return {};
  try {
    const raw = storage.getItem(COLUMN_SIZES_STORAGE_KEY);
    if (!raw) return {};
    const parsed: unknown = JSON.parse(raw);
    if (parsed === null || typeof parsed !== "object" || Array.isArray(parsed)) return {};
    const result: ColumnSizes = {};
    for (const [id, value] of Object.entries(parsed as Record<string, unknown>)) {
      if (typeof value === "number" && Number.isFinite(value) && value > 0) result[id] = value;
    }
    return result;
  } catch {
    return {};
  }
}

/** 写入列宽(尽力而为:配额/隐私模式写失败不阻断界面) */
export function saveColumnSizes(
  sizes: ColumnSizes,
  storage: Storage | null = typeof window === "undefined" ? null : window.localStorage,
): void {
  if (storage === null) return;
  try {
    storage.setItem(COLUMN_SIZES_STORAGE_KEY, JSON.stringify(sizes));
  } catch {
    // 本地态尽力而为,不阻断
  }
}

// ---------------------------------------------------------------------------
// 展示辅助:日期词面(密钥记录用绝对时刻,不做相对时间)
// ---------------------------------------------------------------------------

const pad = (value: number) => String(value).padStart(2, "0");

/** 短日期 YYYY-MM-DD(命中列副行);null = 「—」 */
export function formatDay(iso: string | null | undefined): string {
  if (!iso) return "—";
  const date = new Date(iso);
  if (Number.isNaN(date.getTime())) return iso;
  return `${date.getFullYear()}-${pad(date.getMonth() + 1)}-${pad(date.getDate())}`;
}

/** 完整时刻 YYYY-MM-DD HH:mm(行展开的 first_seen/last_check 明细) */
export function formatDateTime(iso: string | null | undefined): string {
  if (!iso) return "—";
  const date = new Date(iso);
  if (Number.isNaN(date.getTime())) return iso;
  return `${formatDay(iso)} ${pad(date.getHours())}:${pad(date.getMinutes())}`;
}
