// @vitest-environment jsdom
//
// 「装机组件」分区卡契约测试(10-05-bundled-plugins-install + 批二
// 10-05-bundled-plugins-batch2):mock Tauri IPC(sidecar_request 通道),覆盖:
// - plugins.bundled.list 渲染:逐包行(名称/版本/tier·gate 徽章/已装态徽章/
//   findings 行内展示)+ 已装版本落后随包 →「可重装更新」;
// - 安装/重装按钮两态:未装件发 {id}(零 force 键)、已装件发 {id, force:true};
//   装后回读 list(拉取是真相源);
// - 卸载钮(批二 R2):已装行普通确认后发 {id};取消零调用;未装行零卸载钮;
// - 品类分区(批二 R3):名称/排程/已存在徽章;未存在发 {id}、已存在确认后
//   发 {id, force:true}(覆盖是知情操作);
// - 装卸错误结构化上屏(PluginStoreError code 透传,如 already_installed);
// - 空态如实:dir=null(dev/旧包未注入)→ 提示块,零虚构清单零按钮。
import { cleanup, fireEvent, render, screen, waitFor } from "@testing-library/react";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";

const mocks = vi.hoisted(() => ({ invoke: vi.fn() }));
vi.mock("@tauri-apps/api/core", () => ({ invoke: mocks.invoke }));

import { BundledPluginsCard } from "./bundled-plugins-card";
import {
  parseBundledCategoryInstall,
  parseBundledPluginsInstall,
  parseBundledPluginsList,
  parseBundledPluginsUninstall,
  parseRemoteDoctorSection,
  parseRemotePluginConfig,
  parseRemotePluginSave,
} from "./bundled-plugins-api";

// ---------------------------------------------------------------------------
// 夹具(wire 形 = entry.py _m_plugins_bundled_list 应答的原样 JSON)
// ---------------------------------------------------------------------------

interface WirePlugin {
  dir_name: string;
  path?: string;
  id: string | null;
  name: string | null;
  version: string | null;
  tier?: string | null;
  gate?: string | null;
  compatible?: string | null;
  compatible_current?: boolean | null;
  requires?: string[];
  provides?: string[];
  installed?: boolean;
  installed_version?: string | null;
  findings?: unknown[];
}

function wirePlugin(overrides: Partial<WirePlugin> & { dir_name: string }): Record<string, unknown> {
  return {
    path: `/app/Contents/Resources/plugins/${overrides.dir_name}`,
    version: "1.0.0",
    tier: "desktop",
    gate: null,
    compatible: ">=0.0.1,<0.1",
    compatible_current: true,
    requires: [],
    provides: [],
    installed: false,
    installed_version: null,
    findings: [],
    ...overrides,
  };
}

function wireList(
  plugins: Record<string, unknown>[],
  dir: string | null = "/app/Contents/Resources/plugins",
  categories: unknown[] = [],
) {
  return { dir, count: plugins.length, plugins, categories };
}

/** 记账式 IPC 桩:list 内存态 + install 翻态回读(壳桩行为 = entry.py 语义);
 * 批二扩 uninstall/category_install(品类翻态回读同源)。 */
function installBundledIpc(
  initial: Record<string, unknown>[],
  dir: string | null = "/app/Contents/Resources/plugins",
  installImpl?: (params: { id: string; force?: boolean }) => unknown,
  initialCategories: Record<string, unknown>[] = [],
) {  const seen: { method: string; params: unknown }[] = [];
  let current = initial;
  let currentCategories = initialCategories;
  mocks.invoke.mockImplementation(async (_command: string, args?: { method?: string; params?: unknown }) => {
    seen.push({ method: args?.method ?? "", params: args?.params });
    if (args?.method === "plugins.bundled.list") return wireList(current, dir, currentCategories);
    if (args?.method === "plugins.bundled.install") {
      if (installImpl) {
        const outcome = installImpl(args.params as { id: string; force?: boolean });
        if (outcome !== undefined) return outcome; // 可编程拒绝(throw JSON 由用例自带)
      }
      const { id, force } = args.params as { id: string; force?: boolean };
      if (force !== true) {
        // 已装未 force → already_installed 结构化拒(与 InstalledPluginStore 同门)
        throw JSON.stringify({
          code: "already_installed",
          path: "params.id",
          message: `插件 ${id} 已安装;覆盖安装请加 --force`,
        });
      }
      current = current.map((plugin) =>
        (plugin as unknown as WirePlugin).dir_name === id
          ? { ...plugin, installed: true, installed_version: (plugin as unknown as WirePlugin).version }
          : plugin,
      );
      return {
        ok: true,
        dir: `/home/myia/plugins/${id}`,
        version: (current.find((p) => (p as unknown as WirePlugin).dir_name === id) as unknown as WirePlugin).version,
      };
    }
    if (args?.method === "plugins.bundled.uninstall") {
      const { id } = args.params as { id: string };
      current = current.map((plugin) =>
        (plugin as unknown as WirePlugin).dir_name === id ? { ...plugin, installed: false, installed_version: null } : plugin,
      );
      return { ok: true, id, path: `/home/myia/plugins/${id}` };
    }
    if (args?.method === "plugins.bundled.category_install") {
      const { id, force } = args.params as { id: string; force?: boolean };
      const target = currentCategories.find((cat) => (cat as { id?: string | null }).id === id);
      if (target && (target as { exists?: boolean }).exists && force !== true) {
        // 该件已存在未 force → category_exists 结构化拒(与补种「绝不覆盖」语义对齐)
        throw JSON.stringify({
          code: "category_exists",
          path: "params.id",
          message: `数据根已有同名品类文件;确认覆盖请加 force`,
        });
      }
      currentCategories = currentCategories.map((cat) =>
        (cat as { id?: string | null }).id === id ? { ...cat, exists: true } : cat,
      );
      return { ok: true, file: `${id}.yaml`, path: `/home/myia/plugins/${id}.yaml` };
    }
    throw JSON.stringify({ code: "method_not_found", path: "method", message: `未知方法 ${args?.method}` });
  });
  return { seen };
}

beforeEach(() => {
  mocks.invoke.mockReset();
});
afterEach(() => {
  cleanup();
  vi.clearAllMocks();
});

// ---------------------------------------------------------------------------

describe("装机组件:发现面渲染", () => {
  it("逐包行:名称/版本/tier·gate 徽章/已装态徽章/能力名;已装版本落后随包 → 可重装更新", async () => {
    installBundledIpc([
      wirePlugin({
        dir_name: "myssia-proxy",
        id: "myssia-proxy",
        name: "代理池(proxy)",
        provides: ["proxy_pool"],
        installed: true,
        installed_version: "0.9.0", // 落后随包 1.0.0
      }),
      wirePlugin({
        dir_name: "myssia-crawlab",
        id: "myssia-crawlab",
        name: "Crawlab",
        tier: "remote",
        gate: "platform",
        provides: ["crawlab"],
      }),
    ]);
    render(<BundledPluginsCard />);

    await screen.findByTestId("bundled-plugin-myssia-proxy");
    expect(screen.getByTestId("bundled-plugins-dir").textContent).toBe("/app/Contents/Resources/plugins");
    // 已装件:徽章「已装」+ 版本对照(随包 1.0.0 / 已装 0.9.0 可重装更新)+「重装」按钮
    expect(screen.getByTestId("bundled-plugin-myssia-proxy-state").textContent).toBe("已装");
    expect(screen.getByTestId("bundled-version-myssia-proxy").textContent).toContain("随包 1.0.0");
    expect(screen.getByTestId("bundled-version-myssia-proxy").textContent).toContain("已装 0.9.0");
    expect(screen.getByTestId("bundled-version-myssia-proxy").textContent).toContain("可重装更新");
    expect(screen.getByTestId("bundled-plugin-myssia-proxy-reinstall")).toBeDefined();
    // 未装件:「未装」徽章 +「安装」按钮;tier/gate 徽章如实(tier=remote gate=platform)
    expect(screen.getByTestId("bundled-plugin-myssia-crawlab-state").textContent).toBe("未装");
    expect(screen.getByTestId("bundled-plugin-myssia-crawlab-install")).toBeDefined();
    expect(screen.getByTestId("bundled-tier-remote").textContent).toBe("remote");
    expect(screen.getByTestId("bundled-gate-platform").textContent).toBe("platform");
    // 能力名与卸载面文案在卡内(批二:本屏可卸载,已装行有卸载钮)
    expect(screen.getByTestId("bundled-plugins-rows").textContent).toContain("proxy_pool");
    expect(screen.getByTestId("bundled-plugin-myssia-proxy-uninstall")).toBeDefined();
    expect(screen.queryByTestId("bundled-plugin-myssia-crawlab-uninstall")).toBeNull(); // 未装行零卸载钮
    expect(screen.getByTestId("bundled-plugins-card").textContent).toContain("vendor_missing");
  });

  it("条目级 findings 行内展示(坏 manifest 件如实透出,manifest 坏件安装钮禁用)", async () => {
    installBundledIpc([
      wirePlugin({
        dir_name: "myssia-broken",
        id: null,
        name: null,
        version: null,
        installed: false,
        findings: [
          {
            severity: "error",
            scope: "plugin:myssia-broken",
            code: "manifest_invalid",
            message: "随包插件 manifest 校验失败:id 必须为小写字母或数字开头",
          },
        ],
      }),
    ]);
    render(<BundledPluginsCard />);

    const findings = await screen.findByTestId("bundled-plugin-myssia-broken-findings");
    expect(findings.textContent).toContain("manifest_invalid");
    expect(findings.textContent).toContain("id 必须为小写字母或数字开头");
    const button = screen.getByTestId("bundled-plugin-myssia-broken-install") as HTMLButtonElement;
    expect(button.disabled).toBe(true);
  });

  it("空态如实:dir=null(dev 形态/旧包未注入)→ 提示块 + 零虚构清单", async () => {
    installBundledIpc([], null);
    render(<BundledPluginsCard />);

    await screen.findByTestId("bundled-plugins-empty");
    expect(screen.getByTestId("bundled-plugins-empty").textContent).toContain("未发现随包插件目录");
    expect(screen.getByTestId("bundled-plugins-empty").textContent).toContain("dev");
    expect(screen.queryByTestId("bundled-plugins-rows")).toBeNull();
    expect(screen.queryByTestId("bundled-plugins-dir")).toBeNull();
  });
});

describe("装机组件:一键装/重装两态", () => {
  it("未装件「安装」发 {id} 零 force 键;装后回读 list(已装徽章随新)", async () => {
    const { seen } = installBundledIpc([wirePlugin({ dir_name: "myssia-media", id: "myssia-media", name: "视频情报" })], undefined, () => {
      // 可编程成功路径(桩默认 force-only 翻态,这里未装件直接成功)
      return { ok: true, dir: "/home/myia/plugins/myssia-media", version: "1.0.0" };
    });
    render(<BundledPluginsCard />);
    fireEvent.click(await screen.findByTestId("bundled-plugin-myssia-media-install"));

    await screen.findByTestId("bundled-install-note");
    const installCall = seen.find((call) => call.method === "plugins.bundled.install");
    expect(installCall?.params).toEqual({ id: "myssia-media" }); // 零 force 键(force=false 省略)
    expect(screen.getByTestId("bundled-install-note").textContent).toContain("myssia-media@1.0.0 已安装");
    // 装后回读:list 至少两次(挂载初始 + 装后回读)
    const listCalls = seen.filter((call) => call.method === "plugins.bundled.list");
    expect(listCalls.length).toBeGreaterThanOrEqual(2);
  });

  it("已装件「重装」发 {id, force:true}(覆盖重装 = force 通道)", async () => {
    const { seen } = installBundledIpc([
      wirePlugin({ dir_name: "myssia-proxy", id: "myssia-proxy", name: "代理池", installed: true, installed_version: "1.0.0" }),
    ]);
    render(<BundledPluginsCard />);
    fireEvent.click(await screen.findByTestId("bundled-plugin-myssia-proxy-reinstall"));

    await screen.findByTestId("bundled-install-note");
    const installCall = seen.find((call) => call.method === "plugins.bundled.install");
    expect(installCall?.params).toEqual({ id: "myssia-proxy", force: true });
    expect(screen.getByTestId("bundled-install-note").textContent).toContain("已重装");
  });

  it("装卸错误结构化上屏(already_installed 透传;安装钮零成功回执)", async () => {
    installBundledIpc([wirePlugin({ dir_name: "myssia-yake", id: "myssia-yake", name: "关键词抽取" })], undefined, (params) => {
      if (params.force !== true) {
        throw JSON.stringify({
          code: "incompatible_version",
          path: "params.id",
          message: `插件 ${params.id} 要求 myssia >=999.0.0,当前不兼容;确认风险后可 --force 强制安装`,
        });
      }
      return undefined;
    });
    render(<BundledPluginsCard />);
    fireEvent.click(await screen.findByTestId("bundled-plugin-myssia-yake-install"));

    await waitFor(() => {
      expect(screen.getByRole("alert").textContent).toContain("incompatible_version");
    });
    expect(screen.queryByTestId("bundled-install-note")).toBeNull();
  });
});

describe("装机组件:卸载钮(批二 R2)", () => {
  it("已装行「卸载」:普通确认 → 发 {id};回执「已卸载」+ 回读 list(已装徽章随新)", async () => {
    const confirmSpy = vi.spyOn(window, "confirm").mockReturnValue(true);
    const { seen } = installBundledIpc([
      wirePlugin({ dir_name: "myssia-proxy", id: "myssia-proxy", name: "代理池", installed: true, installed_version: "1.0.0" }),
    ]);
    render(<BundledPluginsCard />);
    fireEvent.click(await screen.findByTestId("bundled-plugin-myssia-proxy-uninstall"));

    await screen.findByTestId("bundled-install-note");
    expect(confirmSpy).toHaveBeenCalledTimes(1); // 普通一次确认(非危险操作,不循钥匙链二次确认判例)
    expect(confirmSpy.mock.calls[0][0]).toContain("myssia-proxy");
    const uninstallCall = seen.find((call) => call.method === "plugins.bundled.uninstall");
    expect(uninstallCall?.params).toEqual({ id: "myssia-proxy" });
    expect(screen.getByTestId("bundled-install-note").textContent).toContain("已卸载");
    expect(screen.getByTestId("bundled-install-note").textContent).toContain("可随时重装");
    // 卸载后回读:list ≥ 2 次(挂载 + 卸后),已装态翻「未装」
    const listCalls = seen.filter((call) => call.method === "plugins.bundled.list");
    expect(listCalls.length).toBeGreaterThanOrEqual(2);
    await waitFor(() => {
      expect(screen.getByTestId("bundled-plugin-myssia-proxy-state").textContent).toBe("未装");
    });
    confirmSpy.mockRestore();
  });

  it("确认取消 → 零卸载调用(不误删)", async () => {
    const confirmSpy = vi.spyOn(window, "confirm").mockReturnValue(false);
    const { seen } = installBundledIpc([
      wirePlugin({ dir_name: "myssia-proxy", id: "myssia-proxy", name: "代理池", installed: true, installed_version: "1.0.0" }),
    ]);
    render(<BundledPluginsCard />);
    fireEvent.click(await screen.findByTestId("bundled-plugin-myssia-proxy-uninstall"));

    await waitFor(() => expect(confirmSpy).toHaveBeenCalledTimes(1));
    expect(seen.find((call) => call.method === "plugins.bundled.uninstall")).toBeUndefined();
    expect(screen.queryByTestId("bundled-install-note")).toBeNull();
    confirmSpy.mockRestore();
  });

  it("not_installed 结构化上屏(未装件被并发卸载的如实态)", async () => {
    const confirmSpy = vi.spyOn(window, "confirm").mockReturnValue(true);
    mocks.invoke.mockImplementation(async (_command: string, args?: { method?: string; params?: unknown }) => {
      if (args?.method === "plugins.bundled.list") {
        return wireList([
          wirePlugin({ dir_name: "myssia-proxy", id: "myssia-proxy", name: "代理池", installed: true, installed_version: "1.0.0" }),
        ]);
      }
      if (args?.method === "plugins.bundled.uninstall") {
        throw JSON.stringify({
          code: "not_installed",
          path: "params.id",
          message: "插件 myssia-proxy 未安装于 /home/myia/plugins,无法移除",
        });
      }
      throw JSON.stringify({ code: "method_not_found", path: "method", message: "未知方法" });
    });
    render(<BundledPluginsCard />);
    fireEvent.click(await screen.findByTestId("bundled-plugin-myssia-proxy-uninstall"));

    await waitFor(() => {
      expect(screen.getByRole("alert").textContent).toContain("not_installed");
    });
    expect(screen.queryByTestId("bundled-install-note")).toBeNull();
    confirmSpy.mockRestore();
  });
});

describe("装机组件:品类分区(批二 R3)", () => {
  const CATEGORIES = [
    { file: "ai-news.yaml", path: "/app/Contents/Resources/plugins/ai-news.yaml", id: "ai-news", name: "AI资讯", schedule: "0 9 * * *", exists: true, findings: [] },
    { file: "monitor.yaml", path: "/app/Contents/Resources/plugins/monitor.yaml", id: "monitor", name: "变更监控", schedule: "*/15 * * * *", exists: false, findings: [] },
  ];

  it("品类行渲染:名称/排程/已存在徽章(已存在 ok/未装 outline)", async () => {
    installBundledIpc([wirePlugin({ dir_name: "myssia-proxy", id: "myssia-proxy", name: "代理池" })], undefined, undefined, CATEGORIES);
    render(<BundledPluginsCard />);

    await screen.findByTestId("bundled-categories");
    expect(screen.getByTestId("bundled-category-ai-news.yaml-state").textContent).toBe("已存在");
    expect(screen.getByTestId("bundled-category-monitor.yaml-state").textContent).toBe("未装");
    expect(screen.getByTestId("bundled-category-monitor.yaml").textContent).toContain("*/15 * * * *");
    expect(screen.getByTestId("bundled-category-monitor.yaml").textContent).toContain("变更监控");
    // 与补种语义对齐的说明文案在分区(section 含标题)
    expect(screen.getByTestId("bundled-categories-section").textContent).toContain("补种");
  });

  it("未存在品类「安装」发 {id} 零 force 键(零确认弹窗);装后回读 exists 翻真", async () => {
    const confirmSpy = vi.spyOn(window, "confirm").mockReturnValue(true);
    const { seen } = installBundledIpc([wirePlugin({ dir_name: "myssia-proxy", id: "myssia-proxy", name: "代理池" })], undefined, undefined, CATEGORIES);
    render(<BundledPluginsCard />);
    fireEvent.click(await screen.findByTestId("bundled-category-monitor.yaml-install"));

    await screen.findByTestId("bundled-install-note");
    expect(confirmSpy).not.toHaveBeenCalled(); // 未存在零确认(不是覆盖操作)
    const call = seen.find((item) => item.method === "plugins.bundled.category_install");
    expect(call?.params).toEqual({ id: "monitor" }); // 零 force 键
    expect(screen.getByTestId("bundled-install-note").textContent).toContain("monitor.yaml 已安装");
    await waitFor(() => {
      expect(screen.getByTestId("bundled-category-monitor.yaml-state").textContent).toBe("已存在");
    });
    confirmSpy.mockRestore();
  });

  it("已存在品类「覆盖」:普通确认后发 {id, force:true};取消零调用(与补种「绝不覆盖」对齐)", async () => {
    const confirmSpy = vi.spyOn(window, "confirm").mockReturnValueOnce(true);
    const { seen } = installBundledIpc([wirePlugin({ dir_name: "myssia-proxy", id: "myssia-proxy", name: "代理池" })], undefined, undefined, CATEGORIES);
    render(<BundledPluginsCard />);
    fireEvent.click(await screen.findByTestId("bundled-category-ai-news.yaml-overwrite"));

    await screen.findByTestId("bundled-install-note");
    expect(confirmSpy).toHaveBeenCalledTimes(1);
    expect(confirmSpy.mock.calls[0][0]).toContain("ai-news.yaml");
    const call = seen.find((item) => item.method === "plugins.bundled.category_install");
    expect(call?.params).toEqual({ id: "ai-news", force: true });
    expect(screen.getByTestId("bundled-install-note").textContent).toContain("已覆盖");
    // 取消路径:再点一次但 confirm 返回 false → 零新增调用
    confirmSpy.mockReturnValueOnce(false);
    fireEvent.click(screen.getByTestId("bundled-category-ai-news.yaml-overwrite"));
    await waitFor(() => expect(confirmSpy).toHaveBeenCalledTimes(2));
    expect(seen.filter((item) => item.method === "plugins.bundled.category_install")).toHaveLength(1);
    confirmSpy.mockRestore();
  });

  it("坏品类 YAML 件:findings 行内 + 安装钮禁用;category_exists 结构化上屏", async () => {
    const confirmSpy = vi.spyOn(window, "confirm").mockReturnValue(true);
    const badCategories = [
      {
        file: "broken.yaml",
        path: "/app/Contents/Resources/plugins/broken.yaml",
        id: null,
        name: null,
        schedule: null,
        exists: false,
        findings: [{ severity: "error", scope: "category:broken.yaml", code: "category_invalid", message: "随包品类 YAML 校验失败:schedule 不是合法的 5 段 cron" }],
      },
    ];
    mocks.invoke.mockImplementation(async (_command: string, args?: { method?: string; params?: unknown }) => {
      if (args?.method === "plugins.bundled.list") {
        return wireList([wirePlugin({ dir_name: "myssia-proxy", id: "myssia-proxy", name: "代理池" })], undefined, badCategories);
      }
      if (args?.method === "plugins.bundled.category_install") {
        throw JSON.stringify({
          code: "category_exists",
          path: "params.id",
          message: "数据根已有同名品类文件 /home/myia/plugins/ai-news.yaml;确认覆盖请加 force",
        });
      }
      throw JSON.stringify({ code: "method_not_found", path: "method", message: "未知方法" });
    });
    render(<BundledPluginsCard />);

    const findings = await screen.findByTestId("bundled-category-broken.yaml-findings");
    expect(findings.textContent).toContain("category_invalid");
    const button = screen.getByTestId("bundled-category-broken.yaml-install") as HTMLButtonElement;
    expect(button.disabled).toBe(true);
    confirmSpy.mockRestore();
  });
});

// ---------------------------------------------------------------------------
// 轨D remote 配置面板(阶段3,10-06-native-plugin-components R7/G-Q1)
// ---------------------------------------------------------------------------

/** 面板可编程 IPC 桩:list + plugins.remote.get/save + secret.set + doctor。 */
function installRemoteIpc(options: {
  plugins: Record<string, unknown>[];
  /** plugins.remote.get 应答(null = 结构化拒 remote_config_unavailable,dev 形态) */
  remoteConfig?: { endpoint: string | null; token: string | null; known: boolean } | null;
  /** doctor 应答的 firecrawl 键(undefined = 键缺失,旧 sidecar;null = 方法拒) */
  doctorFirecrawl?: Record<string, unknown> | undefined | null;
  /** secret.set 可编程失败 */
  secretSetError?: Record<string, unknown>;
  /** plugins.remote.save 可编程失败(secret.set 已成功的部分成功场景) */
  remoteSaveError?: Record<string, unknown>;
}) {
  const seen: { method: string; params: unknown }[] = [];
  const state = {
    remoteConfig: options.remoteConfig ?? { endpoint: null, token: null, known: false },
  };
  mocks.invoke.mockImplementation(async (_command: string, args?: { method?: string; params?: unknown }) => {
    seen.push({ method: args?.method ?? "", params: args?.params });
    const method = args?.method ?? "";
    const params = (args?.params ?? {}) as Record<string, unknown>;
    if (method === "plugins.bundled.list") return wireList(options.plugins);
    if (method === "plugins.remote.get") {
      if (options.remoteConfig === null) {
        throw JSON.stringify({
          code: "remote_config_unavailable",
          path: "params.id",
          message: "remote 插件配置属桌面数据根(dev 形态无 MYIA_HOME);开发后门 = 显式 env(如 MYIA_FIRECRAWL_URL)",
        });
      }
      return { id: params.id, ...state.remoteConfig };
    }
    if (method === "plugins.remote.save") {
      if (options.remoteSaveError) throw JSON.stringify(options.remoteSaveError);
      const endpoint = params.endpoint as string;
      state.remoteConfig = { endpoint, token: (params.token as string | undefined) ?? state.remoteConfig.token, known: true };
      return { ok: true, id: params.id, path: "/home/MYIA/remote-plugins.json", endpoint };
    }
    if (method === "secret.set") {
      if (options.secretSetError) throw JSON.stringify(options.secretSetError);
      return { name: params.name, stored: true };
    }
    if (method === "doctor") {
      if (options.doctorFirecrawl === null) {
        throw JSON.stringify({ code: "method_not_found", path: "method", message: "未知方法 doctor" });
      }
      return { healthy: true, firecrawl: options.doctorFirecrawl };
    }
    throw JSON.stringify({ code: "method_not_found", path: "method", message: `未知方法 ${method}` });
  });
  return { seen, state };
}

const FIRECRAWL_ENTRY = () =>
  wirePlugin({
    dir_name: "myssia-firecrawl",
    id: "myssia-firecrawl",
    name: "渲染抓取后端(Firecrawl)",
    tier: "remote",
    provides: ["render_fetch"],
  });

describe("装机组件:轨D remote 配置面板(阶段3)", () => {
  it("tier=remote 条目渲染面板(get 预填端点 + 已配置/未配置徽章);desktop 条目零面板", async () => {
    installRemoteIpc({
      plugins: [FIRECRAWL_ENTRY(), wirePlugin({ dir_name: "myssia-proxy", id: "myssia-proxy", name: "代理池" })],
      remoteConfig: { endpoint: "https://fc.mine.example.org", token: "keychain:myia/firecrawl/api-key", known: true },
    });
    render(<BundledPluginsCard />);

    const panel = await screen.findByTestId("bundled-remote-panel-myssia-firecrawl");
    await waitFor(() => {
      expect((screen.getByTestId("bundled-remote-panel-myssia-firecrawl-endpoint") as HTMLInputElement).value).toBe(
        "https://fc.mine.example.org",
      );
    });
    await waitFor(() => {
      expect(screen.getByTestId("bundled-remote-panel-myssia-firecrawl-state").textContent).toBe("已配置");
    });
    // 凭据引用名提示在面板(keychain-only:配置只存引用);探活钮在(轨道D doctor 连通项件)
    expect(panel.textContent).toContain("keychain:myia/firecrawl/api-key");
    expect(screen.getByTestId("bundled-remote-panel-myssia-firecrawl-probe")).toBeDefined();
    // desktop 条目零面板
    expect(screen.queryByTestId("bundled-remote-panel-myssia-proxy")).toBeNull();
  });

  it("未配置件:徽章「未配置」+ 输入空(dev 后门提示文案在)", async () => {
    installRemoteIpc({ plugins: [FIRECRAWL_ENTRY()] });
    render(<BundledPluginsCard />);

    await waitFor(() => {
      expect(screen.getByTestId("bundled-remote-panel-myssia-firecrawl-state").textContent).toBe("未配置");
    });
    expect((screen.getByTestId("bundled-remote-panel-myssia-firecrawl-endpoint") as HTMLInputElement).value).toBe("");
    expect(screen.getByTestId("bundled-remote-panel-myssia-firecrawl").textContent).toContain("MYIA_FIRECRAWL_URL");
  });

  it("保存流(带凭据):secret.set 先行(myssia secret set 同门)→ remote.save 只存 keychain 引用;明文零进配置;保存即清输入", async () => {
    const { seen } = installRemoteIpc({ plugins: [FIRECRAWL_ENTRY()] });
    render(<BundledPluginsCard />);

    await screen.findByTestId("bundled-remote-panel-myssia-firecrawl");
    fireEvent.change(screen.getByTestId("bundled-remote-panel-myssia-firecrawl-endpoint"), {
      target: { value: "https://fc.mine.example.org" },
    });
    fireEvent.change(screen.getByTestId("bundled-remote-panel-myssia-firecrawl-token"), {
      target: { value: "fc-plain-secret" },
    });
    fireEvent.click(screen.getByTestId("bundled-remote-panel-myssia-firecrawl-save"));
    await waitFor(() => {
      expect(screen.getByRole("status").textContent).toContain("已保存");
    });

    const secretCall = seen.find((call) => call.method === "secret.set");
    expect(secretCall?.params).toEqual({ name: "myia/firecrawl/api-key", value: "fc-plain-secret" });
    const saveCall = seen.find((call) => call.method === "plugins.remote.save");
    // keychain-only 联动:配置里只有 keychain: 引用,明文只在 secret.set 通道
    expect(saveCall?.params).toEqual({
      id: "myssia-firecrawl",
      endpoint: "https://fc.mine.example.org",
      token: "keychain:myia/firecrawl/api-key",
    });
    expect(JSON.stringify(seen.find((call) => call.method === "plugins.remote.save")?.params)).not.toContain("fc-plain-secret");
    // 保存即清(明文不留输入态);get 回读翻「已配置」
    expect((screen.getByTestId("bundled-remote-panel-myssia-firecrawl-token") as HTMLInputElement).value).toBe("");
    await waitFor(() => {
      expect(screen.getByTestId("bundled-remote-panel-myssia-firecrawl-state").textContent).toBe("已配置");
    });
  });

  it("保存流(凭据留空):只发 remote.save 无 token 键(保持现值),零 secret.set", async () => {
    const { seen } = installRemoteIpc({
      plugins: [FIRECRAWL_ENTRY()],
      remoteConfig: { endpoint: "https://old.example.org", token: "keychain:myia/firecrawl/api-key", known: true },
    });
    render(<BundledPluginsCard />);

    await screen.findByTestId("bundled-remote-panel-myssia-firecrawl");
    fireEvent.change(screen.getByTestId("bundled-remote-panel-myssia-firecrawl-endpoint"), {
      target: { value: "https://new.example.org" },
    });
    fireEvent.click(screen.getByTestId("bundled-remote-panel-myssia-firecrawl-save"));
    await waitFor(() => {
      expect(screen.getByRole("status").textContent).toContain("已保存");
    });

    const saveCall = seen.find((call) => call.method === "plugins.remote.save");
    expect(saveCall?.params).toEqual({ id: "myssia-firecrawl", endpoint: "https://new.example.org" });
    expect(seen.find((call) => call.method === "secret.set")).toBeUndefined();
  });

  it("校验错误态:非 http(s)(env:/keychain: 引用、裸串)→ 前端同口径先挡,零保存 IPC", async () => {
    const { seen } = installRemoteIpc({ plugins: [FIRECRAWL_ENTRY()] });
    render(<BundledPluginsCard />);

    await screen.findByTestId("bundled-remote-panel-myssia-firecrawl");
    for (const bad of ["env:MYIA_FIRECRAWL_URL", "keychain:myia/firecrawl/api-key", "not-a-url", " ", "https://"]) {
      fireEvent.change(screen.getByTestId("bundled-remote-panel-myssia-firecrawl-endpoint"), { target: { value: bad } });
      fireEvent.click(screen.getByTestId("bundled-remote-panel-myssia-firecrawl-save"));
      expect(await screen.findByTestId("bundled-remote-panel-myssia-firecrawl-endpoint-error")).toBeDefined();
    }
    expect(seen.find((call) => call.method === "plugins.remote.save")).toBeUndefined();
    expect(seen.find((call) => call.method === "secret.set")).toBeUndefined();
    // env:/keychain: 引用有专门文案(引用不走本面板)
    fireEvent.change(screen.getByTestId("bundled-remote-panel-myssia-firecrawl-endpoint"), {
      target: { value: "env:MYIA_FIRECRAWL_URL" },
    });
    fireEvent.click(screen.getByTestId("bundled-remote-panel-myssia-firecrawl-save"));
    expect((await screen.findByTestId("bundled-remote-panel-myssia-firecrawl-endpoint-error")).textContent).toContain("引用");
  });

  it("secret.set 失败结构化上屏(invalid_secret_name 透传,零 remote.save)", async () => {
    const { seen } = installRemoteIpc({
      plugins: [FIRECRAWL_ENTRY()],
      secretSetError: { code: "invalid_secret_name", path: "params.name", message: "凭据名不合规范" },
    });
    render(<BundledPluginsCard />);

    await screen.findByTestId("bundled-remote-panel-myssia-firecrawl");
    fireEvent.change(screen.getByTestId("bundled-remote-panel-myssia-firecrawl-endpoint"), {
      target: { value: "https://fc.example.org" },
    });
    fireEvent.change(screen.getByTestId("bundled-remote-panel-myssia-firecrawl-token"), {
      target: { value: "some-secret" },
    });
    fireEvent.click(screen.getByTestId("bundled-remote-panel-myssia-firecrawl-save"));

    await waitFor(() => {
      expect(screen.getByRole("alert").textContent).toContain("invalid_secret_name");
    });
    expect(seen.find((call) => call.method === "plugins.remote.save")).toBeUndefined();
  });

  it("部分成功披露(复审修复):secret.set 已入钥匙串后 remote.save 被拒 → 孤立凭据如实可见", async () => {
    const { seen } = installRemoteIpc({
      plugins: [FIRECRAWL_ENTRY()],
      remoteSaveError: { code: "remote_config_unavailable", path: "$", message: "remote 插件配置属桌面数据根(dev 形态无 MYIA_HOME)" },
    });
    render(<BundledPluginsCard />);

    await screen.findByTestId("bundled-remote-panel-myssia-firecrawl");
    fireEvent.change(screen.getByTestId("bundled-remote-panel-myssia-firecrawl-endpoint"), {
      target: { value: "https://fc.example.org" },
    });
    fireEvent.change(screen.getByTestId("bundled-remote-panel-myssia-firecrawl-token"), {
      target: { value: "some-secret" },
    });
    fireEvent.click(screen.getByTestId("bundled-remote-panel-myssia-firecrawl-save"));

    // 保存错误 + 「键已入钥匙串」披露双上屏(部分成功不留暗账)
    await waitFor(() => {
      const alerts = screen.getAllByRole("alert");
      expect(alerts.some((el) => el.textContent?.includes("remote_config_unavailable"))).toBe(true);
    });
    await waitFor(() => {
      const alerts = screen.getAllByRole("alert");
      expect(alerts.some((el) => el.textContent?.includes("已先行写入系统钥匙串"))).toBe(true);
    });
    // secret.set 先行执行过(顺序如实:凭据先行,save 后拒)
    expect(seen.find((call) => call.method === "secret.set")).toBeDefined();
  });

  it("dev 形态(remote.get 拒 remote_config_unavailable)→ 保存预判禁用,secret.set 零触达", async () => {
    const { seen } = installRemoteIpc({ plugins: [FIRECRAWL_ENTRY()], remoteConfig: null });
    render(<BundledPluginsCard />);

    await screen.findByTestId("bundled-remote-panel-myssia-firecrawl");
    const save = await screen.findByTestId("bundled-remote-panel-myssia-firecrawl-save");
    await waitFor(() => expect((save as HTMLButtonElement).disabled).toBe(true));
    // 禁存使「secret.set 已入钥匙串而 save 恒拒」的部分成功在 dev 形态不发生
    expect(seen.find((call) => call.method === "secret.set")).toBeUndefined();
    expect(seen.find((call) => call.method === "plugins.remote.save")).toBeUndefined();
  });

  it("端点草稿防覆写(复审修复):载入应答晚于用户输入时不覆写已改草稿", async () => {
    let resolveGet: ((value: unknown) => void) | null = null;
    mocks.invoke.mockImplementation(async (_command: string, args?: { method?: string; params?: unknown }) => {
      const method = args?.method ?? "";
      if (method === "plugins.bundled.list") return wireList([FIRECRAWL_ENTRY()]);
      if (method === "plugins.remote.get") {
        return await new Promise((resolve) => {
          resolveGet = () => resolve({ id: "myssia-firecrawl", endpoint: "https://old.example.org", token: null, known: true });
        });
      }
      throw JSON.stringify({ code: "method_not_found", path: "method", message: `未知方法 ${method}` });
    });
    render(<BundledPluginsCard />);

    const input = (await screen.findByTestId(
      "bundled-remote-panel-myssia-firecrawl-endpoint",
    )) as HTMLInputElement;
    // 载入应答未达(mount→IPC 窗口)用户已开始输入
    fireEvent.change(input, { target: { value: "https://draft.example.org" } });
    // 类型面:闭包内赋值不被 CFA 追踪,显式还原可空调用形态(运行时语义不变)
    (resolveGet as ((value: unknown) => void) | null)?.({});
    // 应答到达:草稿不被旧配置覆写;徽章如实翻「已配置」
    await waitFor(() =>
      expect(screen.getByTestId("bundled-remote-panel-myssia-firecrawl-state").textContent).toBe("已配置"),
    );
    expect(input.value).toBe("https://draft.example.org");
  });

  it("探活三态:连通 / 不可达 / 未配置(未配置不红)", async () => {
    const probe = async (firecrawl: Record<string, unknown> | undefined, expected: string) => {
      mocks.invoke.mockReset();
      installRemoteIpc({
        plugins: [FIRECRAWL_ENTRY()],
        remoteConfig: { endpoint: "https://fc.example.org", token: null, known: true },
        doctorFirecrawl: firecrawl,
      });
      render(<BundledPluginsCard />);
      fireEvent.click(await screen.findByTestId("bundled-remote-panel-myssia-firecrawl-probe"));
      const result = await screen.findByTestId("bundled-remote-panel-myssia-firecrawl-probe-result");
      expect(result.textContent).toContain(expected);
      cleanup();
    };

    await probe(
      {
        configured: true,
        endpoint_display: "env:MYIA_FIRECRAWL_URL",
        api_key_configured: true,
        probe: { ok: true, http_status: 200, message: "HTTP 200", error_type: null },
      },
      "连通",
    );
    await probe(
      {
        configured: true,
        endpoint_display: "env:MYIA_FIRECRAWL_URL",
        api_key_configured: false,
        probe: { ok: false, http_status: null, message: "连接失败(network)", error_type: "network" },
      },
      "不可达",
    );
    await probe(
      { configured: false, endpoint_display: null, api_key_configured: false, probe: null },
      "未配置",
    );
    await probe(undefined, "诊断无 firecrawl 连通项");
  });

  it("dev 形态:plugins.remote.get 结构化拒 → 提示行如实(开发后门=env),输入仍可渲染", async () => {
    installRemoteIpc({ plugins: [FIRECRAWL_ENTRY()], remoteConfig: null });
    render(<BundledPluginsCard />);

    const panel = await screen.findByTestId("bundled-remote-panel-myssia-firecrawl");
    // loadHint = 结构化错误 message 原文(dev 形态无数据根 + 开发后门指引)
    await waitFor(() => {
      expect(panel.textContent).toContain("dev 形态无 MYIA_HOME");
    });
    expect(panel.textContent).toContain("MYIA_FIRECRAWL_URL");
    await waitFor(() => {
      expect(screen.getByTestId("bundled-remote-panel-myssia-firecrawl-state").textContent).toBe("读取失败");
    });
  });
});

describe("装机组件:轨D wire 解析守门(阶段3)", () => {
  it("parseRemotePluginConfig:四键契约;id/known 非契约即抛,endpoint/token 宽容 null", () => {
    expect(parseRemotePluginConfig({ id: "myssia-firecrawl", endpoint: "https://x.example.org", token: null, known: true })).toEqual({
      id: "myssia-firecrawl",
      endpoint: "https://x.example.org",
      token: null,
      known: true,
    });
    expect(parseRemotePluginConfig({ id: "x", endpoint: null, token: null, known: false })).toEqual({
      id: "x",
      endpoint: null,
      token: null,
      known: false,
    });
    expect(() => parseRemotePluginConfig({ endpoint: null, token: null, known: false })).toThrow();
    expect(() => parseRemotePluginConfig({ id: "x", endpoint: null, token: null, known: "yes" })).toThrow();
    expect(() => parseRemotePluginConfig("not-an-object")).toThrow();
  });

  it("parseRemotePluginSave:四键契约(ok 非 true/缺键即抛)", () => {
    expect(parseRemotePluginSave({ ok: true, id: "x", path: "/h/remote-plugins.json", endpoint: "https://x" })).toEqual({
      ok: true,
      id: "x",
      path: "/h/remote-plugins.json",
      endpoint: "https://x",
    });
    expect(() => parseRemotePluginSave({ ok: true, id: "x", path: "/h" })).toThrow();
    expect(() => parseRemotePluginSave({ ok: false, id: "x", path: "/h", endpoint: "https://x" })).toThrow();
  });

  it("parseRemoteDoctorSection:宽容守门——firecrawl 键缺失/非对象/缺 configured = null(旧 sidecar 降级)", () => {
    expect(parseRemoteDoctorSection(null)).toBeNull();
    expect(parseRemoteDoctorSection("nope")).toBeNull();
    expect(parseRemoteDoctorSection({ probe: { ok: true } })).toBeNull();
    const section = parseRemoteDoctorSection({
      configured: true,
      endpoint_display: "env:MYIA_FIRECRAWL_URL",
      api_key_configured: true,
      probe: { ok: false, http_status: null, message: "连接失败(network)", error_type: "network" },
    });
    expect(section).toEqual({
      configured: true,
      endpoint_display: "env:MYIA_FIRECRAWL_URL",
      api_key_configured: true,
      probe: { ok: false, http_status: null, message: "连接失败(network)", error_type: "network" },
    });
    expect(parseRemoteDoctorSection({ configured: false, endpoint_display: null, api_key_configured: false, probe: null })).toEqual({
      configured: false,
      endpoint_display: null,
      api_key_configured: false,
      probe: null,
    });
  });
});

describe("装机组件:wire 解析守门", () => {
  it("parseBundledPluginsList:契约形态过;dir/count 非契约即抛;条目附加字段宽容", () => {
    // 附加未知字段 extra:1(wire 侧宽容忽略——与后端条目级坏件不拦整表同口径)
    const wire = wirePlugin({ dir_name: "x", id: "x" });
    (wire as Record<string, unknown>).extra = 1;
    const parsed = parseBundledPluginsList(wireList([wire]));
    expect(parsed.dir).toBe("/app/Contents/Resources/plugins");
    expect(parsed.count).toBe(1);
    expect(parsed.plugins[0]).toMatchObject({ dir_name: "x", id: "x", installed: false });
    expect(() => parseBundledPluginsList({ count: 1 })).toThrow();
    expect(() => parseBundledPluginsList({ dir: "/x", count: "1", plugins: [] })).toThrow();
    // dev 空态契约:dir=null 合法(categories 同空)
    expect(parseBundledPluginsList({ dir: null, count: 0, plugins: [] })).toEqual({
      dir: null,
      count: 0,
      plugins: [],
      categories: [],
    });
    // categories 缺键宽容为空(旧 sidecar + 新 UI 的第二种旧壳态,list 在但无键)
    const legacyParsed = parseBundledPluginsList({ dir: "/x", count: 1, plugins: [wire] });
    expect(legacyParsed.categories).toEqual([]);
  });

  it("parseBundledPluginsInstall:三键契约;ok 非 true / 缺键即抛", () => {
    expect(parseBundledPluginsInstall({ ok: true, dir: "/x", version: "1.0.0" })).toEqual({
      ok: true,
      dir: "/x",
      version: "1.0.0",
    });
    expect(() => parseBundledPluginsInstall({ ok: false, dir: "/x", version: "1.0.0" })).toThrow();
    expect(() => parseBundledPluginsInstall({ ok: true, dir: "/x" })).toThrow();
  });

  it("parseBundledPluginsUninstall / parseBundledCategoryInstall:批二两应答守门(缺键即抛)", () => {
    expect(parseBundledPluginsUninstall({ ok: true, id: "myssia-proxy", path: "/x" })).toEqual({
      ok: true,
      id: "myssia-proxy",
      path: "/x",
    });
    expect(() => parseBundledPluginsUninstall({ ok: true, id: "x" })).toThrow();
    expect(parseBundledCategoryInstall({ ok: true, file: "ai-news.yaml", path: "/x" })).toEqual({
      ok: true,
      file: "ai-news.yaml",
      path: "/x",
    });
    expect(() => parseBundledCategoryInstall({ ok: true, file: "x" })).toThrow();
    // 品类条目 wire 守门:file/path 宽容降级空串、exists 仅 true 认定;
    // 非对象条目丢弃(对象条目缺键降级默认值——与 plugins 条目同口径)
    const parsed = parseBundledPluginsList(
      wireList([], "/x", [
        { file: "ai-news.yaml", path: "/x/ai-news.yaml", id: "ai-news", name: "AI资讯", schedule: "0 9 * * *", exists: true, findings: [] },
        { id: "broken" },
        "not-an-object",
      ]),
    );
    expect(parsed.categories).toHaveLength(2);
    expect(parsed.categories[0]).toMatchObject({ file: "ai-news.yaml", id: "ai-news", exists: true });
    expect(parsed.categories[1]).toMatchObject({ file: "", id: "broken", exists: false });
  });
});
