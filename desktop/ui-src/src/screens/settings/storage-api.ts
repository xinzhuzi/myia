/**
 * 磁盘占用 IPC 封装(10-14-leftover-sweep-install storage 域;壳侧
 * src-tauri/src/pyenv_components.rs 的 pyenv_storage_usage /
 * pyenv_reclaim_storage 对齐源,类型先例 = ./pyenv-api.ts):
 * - command `pyenv_storage_usage` → `{total, items:[{id,label,bytes,
 *   reclaimable,hint}]}`。口径钉死(壳侧 Q6):metadata().len() 逻辑字节、
 *   含隐藏文件全量;全部顶层文件(含隐藏)聚合为「顶层文件」项,未知一层
 *   目录归「其余」——枚举仅示例不设限,视图不漏面;total 与分项之和恒等。
 *   hint 文案钉在壳侧(与 components.json 已发布契约一致),前端只渲染。
 * - command `pyenv_reclaim_storage(target)` → `{target, reclaimed_bytes}`。
 *   target **白名单硬规格**(壳侧 Q9):仅接受 {"playwright-browsers"} ∪
 *   {components.json 中 kind=service 的 id}(当前 = searxng);其余一切
 *   取值(路径分隔符/raw path/`../` 穿越/白名单外 id)壳侧结构化拒,
 *   绝不接受原始路径参数。回收后壳侧广播 pyenv-status-changed
 *   (crawl4ai / searxng 组件行即时转「未装」)。
 */
import { invoke } from "@tauri-apps/api/core";

/** 占用分项(wire 形 snake_case 无附加键;id 稳定供测试/交互定位)。 */
export interface StorageItem {
  id: string;
  label: string;
  bytes: number;
  reclaimable: boolean;
  hint: string;
}

/** `pyenv_storage_usage` 载荷(total = 全根逻辑字节总和)。 */
export interface StorageUsage {
  total: number;
  items: StorageItem[];
}

/** `pyenv_reclaim_storage` 回执(reclaimed_bytes = 删除前实测逻辑字节)。 */
export interface ReclaimOutcome {
  target: string;
  reclaimed_bytes: number;
}

/** wire 载荷 → StorageUsage(TS 侧守门,同 parsePyenvStatus 口径):
 * total/items 非契约类型即抛(壳侧 serde 已钉死,出现即对齐破了,大声
 * 失败);条目宽容五键形态(缺键/错型丢弃,坏行不拦占用展示)。 */
export function parseStorageUsage(raw: unknown): StorageUsage {
  if (typeof raw !== "object" || raw === null) {
    throw new TypeError(`storage usage 载荷不是对象: ${String(raw)}`);
  }
  const record = raw as Record<string, unknown>;
  if (typeof record.total !== "number" || !Array.isArray(record.items)) {
    throw new TypeError(
      `storage usage 非契约形态({total, items}): ${String(raw)}`,
    );
  }
  const items = record.items.flatMap((entry): StorageItem[] => {
    if (typeof entry !== "object" || entry === null) return [];
    const item = entry as Record<string, unknown>;
    if (
      typeof item.id !== "string" ||
      typeof item.label !== "string" ||
      typeof item.bytes !== "number" ||
      typeof item.reclaimable !== "boolean" ||
      typeof item.hint !== "string"
    ) {
      return [];
    }
    return [
      {
        id: item.id,
        label: item.label,
        bytes: item.bytes,
        reclaimable: item.reclaimable,
        hint: item.hint,
      },
    ];
  });
  return { total: record.total, items };
}

/** wire 载荷 → ReclaimOutcome(同上守门口径)。 */
export function parseReclaimOutcome(raw: unknown): ReclaimOutcome {
  if (typeof raw !== "object" || raw === null) {
    throw new TypeError(`reclaim 载荷不是对象: ${String(raw)}`);
  }
  const record = raw as Record<string, unknown>;
  if (
    typeof record.target !== "string" ||
    typeof record.reclaimed_bytes !== "number"
  ) {
    throw new TypeError(
      `reclaim 非契约形态({target, reclaimed_bytes}): ${String(raw)}`,
    );
  }
  return { target: record.target, reclaimed_bytes: record.reclaimed_bytes };
}

/** 占用扫描(du 级遍历秒级返回;加载态由消费方渲染)。 */
export async function storageUsage(): Promise<StorageUsage> {
  return parseStorageUsage(await invoke("pyenv_storage_usage"));
}

/**
 * 整目录回收(第一批白名单目标)。成功后壳侧广播 pyenv-status-changed,
 * 消费方应重拉占用与组件状态(组件行转「未装」的真相源是拉取)。
 */
export async function reclaimStorage(target: string): Promise<ReclaimOutcome> {
  return parseReclaimOutcome(await invoke("pyenv_reclaim_storage", { target }));
}
