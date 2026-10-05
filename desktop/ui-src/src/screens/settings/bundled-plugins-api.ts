/**
 * 随包插件组件包发现/一键装 IPC 封装(10-05-bundled-plugins-install)。
 *
 * 数据面 = sidecar 协议两新方法(entry.py `_HANDLERS` 63/64):
 *   plugins.bundled.list   → 枚举 env MYIA_BUNDLED_PLUGINS 目录下含 plugin.yaml
 *                             的子目录(env 未设/目录不存在 = 合法空表,dir=null 如实)
 *   plugins.bundled.install → {id, force?} → {ok, dir, version}
 *                             (装卸门零新增 = 直调 InstalledPluginStore.install
 *                              与 CLI myssia plugin install 同门;装卸错误码
 *                              already_installed/incompatible_version 等经
 *                              SidecarRequestError.code 原文透传)
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

/** plugins.bundled.list 应答({dir:null, count:0, plugins:[]} = dev/旧包合法空态)。 */
export interface BundledPluginsListResult {
  /** 随包目录锚点(env 未设/目录不存在 = null 如实,不虚构) */
  dir: string | null;
  count: number;
  plugins: BundledPluginView[];
}

/** plugins.bundled.install 应答(契约三键钉死)。 */
export interface BundledPluginsInstallResult {
  ok: boolean;
  /** 安装落点(安装根 <install_root>/<id>) */
  dir: string;
  version: string;
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
  return { dir: asStringOrNone(record.dir), count: record.count, plugins };
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
