// @vitest-environment jsdom
//
// 可选组件机制 IPC 契约测试(10-05-table-restore 桌面侧;mock Tauri IPC,
// 不触真实壳),与壳侧 src-tauri/src/pyenv_components.rs / pyenv.rs 逐字段对齐:
// - command `pyenv_install_component(id)` → `{id, installed, error}`
//   (error 恒在场,无错为 null;安装失败也走 Ok 回包,如实呈现)
// - `pyenv_get_status` 扩展 `components: [{id, installed}]`(两键钉死;
//   注册表缺位回空表,前端不渲染组件行)
// 组件面(R4):「表格还原」开关 = 装/状态回读;卸载本期不做(on→off 只提示,
// 不发卸载调用);主链未配置/安装中开关禁用(壳侧同门)。
import { cleanup, fireEvent, render, screen, waitFor } from "@testing-library/react";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";

const mocks = vi.hoisted(() => ({
  invoke: vi.fn(),
  listen: vi.fn(),
}));

vi.mock("@tauri-apps/api/core", () => ({ invoke: mocks.invoke }));
vi.mock("@tauri-apps/api/event", () => ({ listen: mocks.listen }));

import {
  parseComponentInstallOutcome,
  parsePyenvStatus,
  pyenvInstallComponent,
} from "./pyenv-api";
import { PyenvCard } from "./pyenv-card";
import { PYENV_STATUS_EVENT_NAME } from "./pyenv-api";

// ---------------------------------------------------------------------------
// 夹具(wire 形 = 壳侧 serde 序列化 PyenvStatus 的原样 JSON;components 两键)
// ---------------------------------------------------------------------------

function wireFixture(overrides?: Partial<Record<string, unknown>>): Record<string, unknown> {
  return {
    state: "ready",
    install_path: "/Users/dev/Library/Application Support/MYIA/python",
    python_path: "/Users/dev/Library/Application Support/MYIA/python/bin/python3",
    mirror_runtime: null,
    mirror_pypi: null,
    steps: [],
    components: [],
    ...overrides,
  };
}

function installOutcomeFixture(
  id = "table",
  installed = true,
  error: string | null = null,
): Record<string, unknown> {
  return { id, installed, error };
}

beforeEach(() => {
  mocks.invoke.mockReset();
  mocks.listen.mockReset();
});

afterEach(() => {
  cleanup();
  vi.clearAllMocks();
});

function callsOf(command: string): unknown[] {
  return mocks.invoke.mock.calls
    .filter(([called]) => called === command)
    .map(([, args]) => args)
    .map((args) => args ?? {});
}

// ---------------------------------------------------------------------------
// api 层契约(命令名 / 参数键 / 载荷守门)
// ---------------------------------------------------------------------------

describe("pyenv-api:组件契约(与壳侧 pyenv_components.rs 对齐)", () => {
  it("pyenvInstallComponent:命令名 pyenv_install_component、参数键 id;三键结果原样消费", async () => {
    mocks.invoke.mockResolvedValue(installOutcomeFixture());
    const outcome = await pyenvInstallComponent("table");
    expect(mocks.invoke).toHaveBeenCalledTimes(1);
    expect(mocks.invoke).toHaveBeenCalledWith("pyenv_install_component", { id: "table" });
    expect(outcome).toEqual({ id: "table", installed: true, error: null });
  });

  it("parseComponentInstallOutcome:非契约形态即抛(对齐破了要大声失败);error 恒在场", () => {
    expect(parseComponentInstallOutcome(installOutcomeFixture("table", false, "pip_failed: boom")))
      .toEqual({ id: "table", installed: false, error: "pip_failed: boom" });
    expect(() => parseComponentInstallOutcome("not-an-object")).toThrow(TypeError);
    expect(() => parseComponentInstallOutcome({ id: "table" })).toThrow(TypeError);
    expect(() => parseComponentInstallOutcome({ id: 1, installed: true, error: null })).toThrow(TypeError);
    expect(() => parseComponentInstallOutcome({ id: "table", installed: "yes", error: null })).toThrow(TypeError);
  });

  it("parsePyenvStatus:components 两键透传;缺键回空表(旧壳兼容);坏条目丢弃", () => {
    // 缺 components 键 → [](旧壳中间态,不拦状态展示)
    const { components: missing } = parsePyenvStatus(wireFixture({ components: undefined }));
    expect(missing).toEqual([]);
    const parsed = parsePyenvStatus(
      wireFixture({
        components: [
          { id: "table", installed: true },
          { id: "future", installed: false },
          { id: "bad-shape", installed: "yes" },
          { no: "keys" },
          "not-an-entry",
        ],
      }),
    );
    expect(parsed.components).toEqual([
      { id: "table", installed: true },
      { id: "future", installed: false },
    ]);
  });
});

// ---------------------------------------------------------------------------
// 组件面(「表格还原」开关;R4 字段全覆盖)
// ---------------------------------------------------------------------------

/**
 * IPC mock:get_status 回 current;install_component 记账并按 outcome 应答
 * (可选副作用:成功后 current 的该组件翻 installed=true,模拟壳侧指纹戳+回读)。
 */
function installIpc(
  initial: Record<string, unknown>,
  installOutcome: Record<string, unknown> = installOutcomeFixture(),
) {
  let current = initial;
  mocks.invoke.mockImplementation(async (command: string, args?: unknown) => {
    if (command === "pyenv_get_status") return current;
    if (command === "pyenv_install_component") {
      const { id } = (args ?? {}) as { id: string };
      if ((installOutcome.id as string) === id && installOutcome.installed === true) {
        current = {
          ...current,
          components: (current.components as Record<string, unknown>[]).map((entry) =>
            entry.id === id ? { ...entry, installed: true } : entry,
          ),
        };
      }
      return installOutcome;
    }
    throw new Error(`未预期的 IPC 命令: ${command}`);
  });
}

function installListen() {
  mocks.listen.mockResolvedValue(() => undefined);
}

describe("PyenvCard:设置屏「表格还原」组件开关", () => {
  it("ready 态渲染组件行:文案/未装徽标/开关 off;components 空表时不渲染组件块", async () => {
    installIpc(wireFixture({ components: [{ id: "table", installed: false }] }));
    installListen();
    render(<PyenvCard />);

    const row = await screen.findByTestId("pyenv-component-table");
    expect(row.textContent).toContain("表格还原");
    expect(row.textContent).toContain("rapid_table");
    expect(screen.getByTestId("pyenv-component-table-state").textContent).toBe("未装");
    const toggle = screen.getByRole("switch", { name: "组件开关 table" });
    expect(toggle.getAttribute("aria-checked")).toBe("false");

    // 注册表缺位(旧包)→ components 空 → 组件块整段不渲染
    expect(screen.queryByTestId("pyenv-components")).not.toBeNull();
    cleanup();
    installIpc(wireFixture());
    render(<PyenvCard />);
    await screen.findByTestId("pyenv-state-badge");
    expect(screen.queryByTestId("pyenv-components")).toBeNull();
  });

  it("未装点击开 → pyenv_install_component({id:'table'});回读翻已装(徽标/开关随新)", async () => {
    installIpc(wireFixture({ components: [{ id: "table", installed: false }] }));
    installListen();
    render(<PyenvCard />);
    await screen.findByTestId("pyenv-component-table");

    fireEvent.click(screen.getByRole("switch", { name: "组件开关 table" }));

    await waitFor(() => expect(callsOf("pyenv_install_component")).toEqual([{ id: "table" }]));
    await waitFor(() =>
      expect(screen.getByTestId("pyenv-component-table-state").textContent).toBe("已装"),
    );
    expect(screen.getByRole("switch", { name: "组件开关 table" }).getAttribute("aria-checked")).toBe("true");
    expect(screen.getByTestId("pyenv-component-note").textContent).toContain("已装进自管环境");
  });

  it("安装失败回包(outcome.error=pip_failed):alert 如实呈现,开关保持 off(回读未翻)", async () => {
    installIpc(
      wireFixture({ components: [{ id: "table", installed: false }] }),
      installOutcomeFixture("table", false, "pip_failed: 退出码 1,输出尾部: no matching distribution"),
    );
    installListen();
    render(<PyenvCard />);
    await screen.findByTestId("pyenv-component-table");

    fireEvent.click(screen.getByRole("switch", { name: "组件开关 table" }));

    const alert = await screen.findByTestId("pyenv-component-note");
    expect(alert.getAttribute("role")).toBe("alert");
    expect(alert.textContent).toContain("pip_failed");
    expect(screen.getByTestId("pyenv-component-table-state").textContent).toBe("未装");
    expect(screen.getByRole("switch", { name: "组件开关 table" }).getAttribute("aria-checked")).toBe("false");
  });

  it("已装点击关 → 零卸载调用;如实提示卸载本期未提供(档记后续)", async () => {
    installIpc(wireFixture({ components: [{ id: "table", installed: true }] }));
    installListen();
    render(<PyenvCard />);
    await screen.findByTestId("pyenv-component-table");

    fireEvent.click(screen.getByRole("switch", { name: "组件开关 table" }));

    await screen.findByTestId("pyenv-component-note");
    expect(callsOf("pyenv_install_component")).toEqual([]);
    expect(screen.getByTestId("pyenv-component-note").textContent).toContain("卸载本期未提供");
    expect(screen.getByRole("switch", { name: "组件开关 table" }).getAttribute("aria-checked")).toBe("true");
  });

  it("IPC 护栏拒绝(结构化错误)→ ErrorBox 上屏,开关保持现状", async () => {
    mocks.invoke.mockImplementation(async (command: string) => {
      if (command === "pyenv_get_status")
        return wireFixture({ components: [{ id: "table", installed: false }] });
      if (command === "pyenv_install_component")
        throw JSON.stringify({
          code: "component_env_missing",
          path: "$",
          message: "Python 运行环境未就位:请先在设置页「开始配置」完成环境安装,再装组件",
        });
      throw new Error(`未预期的 IPC 命令: ${command}`);
    });
    installListen();
    render(<PyenvCard />);
    await screen.findByTestId("pyenv-component-table");

    fireEvent.click(screen.getByRole("switch", { name: "组件开关 table" }));

    const alert = await screen.findByRole("alert");
    expect(alert.textContent).toContain("Python 运行环境未就位");
    expect(alert.textContent).toContain("code=component_env_missing");
    expect(screen.getByRole("switch", { name: "组件开关 table" }).getAttribute("aria-checked")).toBe("false");
  });

  it("环境未配置/主链安装中 → 开关禁用(壳侧同门,前端先拦)", async () => {
    for (const state of ["not_configured", "installing"]) {
      cleanup();
      installIpc(wireFixture({ state, components: [{ id: "table", installed: false }] }));
      installListen();
      render(<PyenvCard />);
      await screen.findByTestId(`pyenv-component-table`);
      const toggle = screen.getByRole("switch", { name: "组件开关 table" }) as HTMLButtonElement;
      expect(toggle.disabled, `state=${state} 应禁用`).toBe(true);
      fireEvent.click(toggle);
      expect(callsOf("pyenv_install_component")).toEqual([]);
    }
  });
});

// 事件名守门(载荷同 status 形态 → components 随事件到达,与拉取同源)。
describe("pyenv-components:状态事件载荷同源", () => {
  it("pyenv-status-changed 订阅名不变;载荷经 parsePyenvStatus 带 components", async () => {
    const handler = vi.fn();
    mocks.listen.mockResolvedValue(() => undefined);
    const { onPyenvStatusChanged } = await import("./pyenv-api");
    await onPyenvStatusChanged(handler);
    expect(mocks.listen.mock.calls[0][0]).toBe(PYENV_STATUS_EVENT_NAME);
    const dispatch = mocks.listen.mock.calls[0][1] as (event: { payload: unknown }) => void;
    dispatch({ payload: wireFixture({ components: [{ id: "table", installed: true }] }) });
    expect(handler).toHaveBeenLastCalledWith(
      expect.objectContaining({ components: [{ id: "table", installed: true }] }),
    );
  });
});
