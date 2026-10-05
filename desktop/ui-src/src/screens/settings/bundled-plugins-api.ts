/**
 * 随包插件组件包发现/一键装/卸载 + 品类 YAML 平铺装 IPC 封装
 * (10-05-bundled-plugins-install + 批二 10-05-bundled-plugins-batch2)。
 *
 * 数据面 = sidecar 协议方法(entry.py `_HANDLERS` 63-66):
 *   plugins.bundled.list   → 枚举 env MYIA_BUNDLED_PLUGINS 目录下含 plugin.yaml
 *                             的子目录(env 未设/目录不存在 = 合法空表,dir=null 如实)
 *                             + 平铺品类 YAML 发现视图(categories,批二 R3)
 *   plugins.bundled.install → {id, force?} → {ok, dir, version}
 *                             (装卸门零新增 = 直调 InstalledPluginStore.install
 *                              与 CLI myssia plugin install 同门;装卸错误码
 *                              already_installed/incompatible_version 等经
 *                              SidecarRequestError.code 原文透传)
 *   plugins.bundled.uninstall → {id} → {ok, id, path}(批二 R2:直调
 *                             InstalledPluginStore.remove 与 CLI
 *                             myssia plugin remove 同门;随包原件只读永不删,
 *                             not_installed/io_error 透传)
 *   plugins.bundled.category_install → {id, force?} → {ok, file, path}
 *                             (批二 R3:品类 YAML 单文件平铺拷到数据根
 *                              plugins/,与补种同落点;已存在未 force →
 *                              category_exists 拒,force 才覆盖)
 *
 * 屏私有封装面(spec 变更纪律第 3 条):invoke("sidecar_request") 直连 +
 * 错误归一化走 ./api 的 asSidecarError(与 yaml-editor/api.ts、settings/api.ts
 * 的 settingsYamlRequest 同款惯例;types+invoke 封装沿 ./pyenv-api.ts 先例,
 * 共享客户端 @/lib/api 只读不动——单屏单消费方,不进共享门面)。
 */
import { invoke } from "@tauri-apps/api/core";

import type { Finding } from "@/lib/api";
import { asSidecarError } from "./api";

/** 发现条目(协议注册表 #63 行契约;属性名保持 wire 形 snake_case,惯例同 types.ts)。 */
export interface BundledPluginView {
  /** 随包目录名(发现枚举键;与 manifest id 约定一致,id_mismatch 时如实不一致) */
  dir_name: string;
  /** 随包件路径(Resources/plugins/<pkg> 装机态绝对路径) */
  path: string;
  id: string | null;
  name: string | null;
  version: string | null;
  tier: string | null;
  gate: string | null;
  compatible: string | null;
  compatible_current: boolean | null;
  requires: string[];
  provides: string[];
  /** 已装态(对齐安装根 InstalledPluginStore 的 plugin_id) */
  installed: boolean;
  /** 已装版本(已装但已装 manifest 坏 → null,如实;与随包 version 不同 = 可重装更新) */
  installed_version: string | null;
  /** 条目级 findings(坏 manifest manifest_invalid/id_mismatch/已装不兼容警示等) */
  findings: Finding[];
}

/** 品类发现条目(批二 R3;注册表 #63 行 categories 键契约)。 */
export interface BundledCategoryView {
  /** 随包文件名(安装落点 = 数据根 plugins/ 下同名平铺文件) */
  file: string;
  path: string;
  id: string | null;
  name: string | null;
  /** 品类 cron 排程(坏 YAML → null 如实) */
  schedule: string | null;
  /** 数据根 plugins/ 下同名文件已在(补种/自建/本面已装,文件级冲突口径) */
  exists: boolean;
  findings: Finding[];
}

/** plugins.bundled.list 应答(dev/旧包合法空态:categories 同空)。 */
export interface BundledPluginsListResult {
  /** 随包目录锚点(env 未设/目录不存在 = null 如实,不虚构) */
  dir: string | null;
  count: number;
  plugins: BundledPluginView[];
  /** 随包品类 YAML 发现面(批二 R3;与组件包并列,count 不含品类) */
  categories: BundledCategoryView[];
}

/** plugins.bundled.install 应答(契约三键钉死)。 */
export interface BundledPluginsInstallResult {
  ok: boolean;
  /** 安装落点(安装根 <install_root>/<id>) */
  dir: string;
  version: string;
}

/** plugins.bundled.uninstall 应答(批二 R2;契约三键钉死)。 */
export interface BundledPluginsUninstallResult {
  ok: boolean;
  id: string;
  /** 被删的安装根拷贝路径(随包原件只读,可随时重装) */
  path: string;
}

/** plugins.bundled.category_install 应答(批二 R3;契约三键钉死)。 */
export interface BundledCategoryInstallResult {
  ok: boolean;
  file: string;
  /** 落点(数据根 plugins/<file> 平铺,与补种同落点) */
  path: string;
}

// ---------------------------------------------------------------------------
// wire → 类型化(守门;坏形态大声失败,与 parsePyenvStatus 同口径)
// ---------------------------------------------------------------------------

function asStringOrNone(value: unknown): string | null {
  return typeof value === "string" ? value : null;
}

function asStringArray(value: unknown): string[] {
  return Array.isArray(value) ? value.filter((item): item is string => typeof item === "string") : [];
}

function asFindings(value: unknown): Finding[] {
  return Array.isArray(value) ? value.filter((item): item is Finding => typeof item === "object" && item !== null) : [];
}

/**
 * wire 载荷 → BundledPluginsListResult(TS 侧守门):dir/count 非契约类型即抛
 * (壳侧/协议侧已钉死,出现即对齐破了,大声失败);条目附加字段宽容忽略、
 * 条目非对象形态丢弃(条目级坏件不拦整表渲染,与后端条目级 finding 同口径)。
 * categories(批二 R3)缺键宽容为空数组——旧 sidecar + 新 UI 组合
 * (method_not_found 结构化降级之外的第二种旧壳态:list 在但无 categories 键)
 * 零炸,分区静默空。
 */
export function parseBundledPluginsList(raw: unknown): BundledPluginsListResult {
  if (typeof raw !== "object" || raw === null) {
    throw new TypeError(`随包插件清单载荷不是对象: ${String(raw)}`);
  }
  const record = raw as Record<string, unknown>;
  if (typeof record.count !== "number" || !(record.dir === null || typeof record.dir === "string")) {
    throw new TypeError(`随包插件清单非契约形态({dir, count, plugins}): ${String(raw)}`);
  }
  const plugins = Array.isArray(record.plugins)
    ? record.plugins.flatMap((item): BundledPluginView[] => {
        if (typeof item !== "object" || item === null) return [];
        const plugin = item as Record<string, unknown>;
        return [
          {
            dir_name: typeof plugin.dir_name === "string" ? plugin.dir_name : "",
            path: typeof plugin.path === "string" ? plugin.path : "",
            id: asStringOrNone(plugin.id),
            name: asStringOrNone(plugin.name),
            version: asStringOrNone(plugin.version),
            tier: asStringOrNone(plugin.tier),
            gate: asStringOrNone(plugin.gate),
            compatible: asStringOrNone(plugin.compatible),
            compatible_current: typeof plugin.compatible_current === "boolean" ? plugin.compatible_current : null,
            requires: asStringArray(plugin.requires),
            provides: asStringArray(plugin.provides),
            installed: plugin.installed === true,
            installed_version: asStringOrNone(plugin.installed_version),
            findings: asFindings(plugin.findings),
          },
        ];
      })
    : [];
  const categories = Array.isArray(record.categories)
    ? record.categories.flatMap((item): BundledCategoryView[] => {
        if (typeof item !== "object" || item === null) return [];
        const category = item as Record<string, unknown>;
        return [
          {
            file: typeof category.file === "string" ? category.file : "",
            path: typeof category.path === "string" ? category.path : "",
            id: asStringOrNone(category.id),
            name: asStringOrNone(category.name),
            schedule: asStringOrNone(category.schedule),
            exists: category.exists === true,
            findings: asFindings(category.findings),
          },
        ];
      })
    : [];
  return { dir: asStringOrNone(record.dir), count: record.count, plugins, categories };
}

/** wire 载荷 → BundledPluginsInstallResult(TS 侧守门,同上口径)。 */
export function parseBundledPluginsInstall(raw: unknown): BundledPluginsInstallResult {
  if (typeof raw !== "object" || raw === null) {
    throw new TypeError(`随包插件安装结果载荷不是对象: ${String(raw)}`);
  }
  const record = raw as Record<string, unknown>;
  if (record.ok !== true || typeof record.dir !== "string" || typeof record.version !== "string") {
    throw new TypeError(`随包插件安装结果非契约形态({ok, dir, version}): ${String(raw)}`);
  }
  return { ok: true, dir: record.dir, version: record.version };
}

/** wire 载荷 → BundledPluginsUninstallResult(批二 R2;TS 侧守门,同上口径)。 */
export function parseBundledPluginsUninstall(raw: unknown): BundledPluginsUninstallResult {
  if (typeof raw !== "object" || raw === null) {
    throw new TypeError(`随包插件卸载结果载荷不是对象: ${String(raw)}`);
  }
  const record = raw as Record<string, unknown>;
  if (record.ok !== true || typeof record.id !== "string" || typeof record.path !== "string") {
    throw new TypeError(`随包插件卸载结果非契约形态({ok, id, path}): ${String(raw)}`);
  }
  return { ok: true, id: record.id, path: record.path };
}

/** wire 载荷 → BundledCategoryInstallResult(批二 R3;TS 侧守门,同上口径)。 */
export function parseBundledCategoryInstall(raw: unknown): BundledCategoryInstallResult {
  if (typeof raw !== "object" || raw === null) {
    throw new TypeError(`随包品类安装结果载荷不是对象: ${String(raw)}`);
  }
  const record = raw as Record<string, unknown>;
  if (record.ok !== true || typeof record.file !== "string" || typeof record.path !== "string") {
    throw new TypeError(`随包品类安装结果非契约形态({ok, file, path}): ${String(raw)}`);
  }
  return { ok: true, file: record.file, path: record.path };
}

// ---------------------------------------------------------------------------
// 封装(invoke sidecar_request 直连;错误归一化 SidecarRequestError)
// ---------------------------------------------------------------------------

/** 屏私有类型化往返(与 settings/api.ts 的 settingsYamlRequest 同款)。 */
async function bundledRequest<R>(method: string, params: unknown): Promise<R> {
  try {
    return await invoke<R>("sidecar_request", { method, params });
  } catch (raw) {
    throw asSidecarError(raw);
  }
}

/** 随包插件组件包发现(dev/旧包/未注入 = 合法空态,不抛)。 */
export async function bundledPluginsList(): Promise<BundledPluginsListResult> {
  return parseBundledPluginsList(await bundledRequest("plugins.bundled.list", {}));
}

/**
 * 一键装/重装(id 必须出自 plugins.bundled.list 的条目;装卸错误
 * already_installed/incompatible_version 等经 SidecarRequestError 结构化上屏)。
 */
export async function bundledPluginsInstall(params: {
  id: string;
  force?: boolean;
}): Promise<BundledPluginsInstallResult> {
  return parseBundledPluginsInstall(
    await bundledRequest("plugins.bundled.install", {
      id: params.id,
      ...(params.force ? { force: true } : {}),
    }),
  );
}

/**
 * 卸载(批二 R2):删安装根拷贝(随包原件只读,可随时重装);未装件经
 * SidecarRequestError(not_installed)结构化上屏。
 */
export async function bundledPluginsUninstall(params: { id: string }): Promise<BundledPluginsUninstallResult> {
  return parseBundledPluginsUninstall(
    await bundledRequest("plugins.bundled.uninstall", { id: params.id }),
  );
}

/**
 * 品类 YAML 平铺装(批二 R3):已存在未 force → category_exists 结构化上屏
 * (与补种「绝不覆盖」语义对齐;覆盖是知情操作,UI 侧确认后才发 force)。
 */
export async function bundledCategoryInstall(params: {
  id: string;
  force?: boolean;
}): Promise<BundledCategoryInstallResult> {
  return parseBundledCategoryInstall(
    await bundledRequest("plugins.bundled.category_install", {
      id: params.id,
      ...(params.force ? { force: true } : {}),
    }),
  );
}
