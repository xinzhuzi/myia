// @vitest-environment jsdom
//
// 「装机组件」分区卡契约测试(10-05-bundled-plugins-install):mock Tauri IPC
// (sidecar_request 通道),覆盖:
// - plugins.bundled.list 渲染:逐包行(名称/版本/tier·gate 徽章/已装态徽章/
//   findings 行内展示)+ 已装版本落后随包 →「可重装更新」;
// - 安装/重装按钮两态:未装件发 {id}(零 force 键)、已装件发 {id, force:true};
//   装后回读 list(拉取是真相源);
// - 装卸错误结构化上屏(PluginStoreError code 透传,如 already_installed);
// - 空态如实:dir=null(dev/旧包未注入)→ 提示块,零虚构清单零按钮。
import { cleanup, fireEvent, render, screen, waitFor } from "@testing-library/react";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";

const mocks = vi.hoisted(() => ({ invoke: vi.fn() }));
vi.mock("@tauri-apps/api/core", () => ({ invoke: mocks.invoke }));

import { BundledPluginsCard } from "./bundled-plugins-card";
import { parseBundledPluginsInstall, parseBundledPluginsList } from "./bundled-plugins-api";

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

function wireList(plugins: Record<string, unknown>[], dir: string | null = "/app/Contents/Resources/plugins") {
  return { dir, count: plugins.length, plugins };
}

/** 记账式 IPC 桩:list 内存态 + install 翻态回读(壳桩行为 = entry.py 语义)。 */
function installBundledIpc(
  initial: Record<string, unknown>[],
  dir: string | null = "/app/Contents/Resources/plugins",
  installImpl?: (params: { id: string; force?: boolean }) => unknown,
) {
  const seen: { method: string; params: unknown }[] = [];
  let current = initial;
  mocks.invoke.mockImplementation(async (_command: string, args?: { method?: string; params?: unknown }) => {
    seen.push({ method: args?.method ?? "", params: args?.params });
    if (args?.method === "plugins.bundled.list") return wireList(current, dir);
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
    // 能力名与卸载指引文案在卡内
    expect(screen.getByTestId("bundled-plugins-rows").textContent).toContain("proxy_pool");
    expect(screen.getByTestId("bundled-plugins-card").textContent).toContain("myssia plugin remove");
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
    // dev 空态契约:dir=null 合法
    expect(parseBundledPluginsList({ dir: null, count: 0, plugins: [] })).toEqual({
      dir: null,
      count: 0,
      plugins: [],
    });
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
});
