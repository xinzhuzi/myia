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
import { act, cleanup, fireEvent, render, screen, waitFor } from "@testing-library/react";
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
  parseServiceStatus,
  pyenvInstallComponent,
  serviceStart,
  serviceStatus,
  serviceStop,
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

// ---------------------------------------------------------------------------
// 轨B 壳服务组件(10-06-native-plugin-components 阶段2;design §2/G-Q5):
// components[].kind="service" 三键透传 + 启停按钮/健康绿点/服务态对账。
// ---------------------------------------------------------------------------

function serviceStatusFixture(
  id = "searxng",
  state: "running" | "stopped" = "stopped",
  healthy = false,
): Record<string, unknown> {
  return {
    id,
    state,
    healthy,
    pid: state === "running" ? 4242 : null,
    started_at: state === "running" ? 1730000000 : null,
    last_exit: state === "stopped" ? 0 : null,
  };
}

/**
 * IPC mock:轨B 服务组件面。initial.components 决定渲染面;service_status
 * 按 serviceOutcomes[id] 应答(缺省 stopped);service_start/stop 记账并翻
 * serviceOutcomes(模拟壳侧状态戳+对账)。
 */
function installServiceIpc(
  initial: Record<string, unknown>,
  serviceOutcomes: Record<string, Record<string, unknown>> = {},
) {
  let current = initial;
  const services = { ...serviceOutcomes };
  const outcomesAfter = {
    start: (id: string) => ({ ...services[id], state: "running", healthy: true, pid: 9999, started_at: 1730000100, last_exit: null }),
    stop: (id: string) => ({ id, state: "stopped", healthy: false, pid: null, started_at: null, last_exit: 0 }),
  };
  mocks.invoke.mockImplementation(async (command: string, args?: unknown) => {
    const { id } = (args ?? {}) as { id?: string };
    if (command === "pyenv_get_status") return current;
    if (command === "service_status") return services[id ?? ""] ?? serviceStatusFixture(id ?? "searxng");
    if (command === "service_start") {
      const outcome = id !== undefined && id in services ? outcomesAfter.start(id) : services[id ?? ""];
      services[id ?? ""] = outcome;
      return outcome;
    }
    if (command === "service_stop") {
      const outcome = outcomesAfter.stop(id ?? "");
      services[id ?? ""] = outcome;
      return outcome;
    }
    if (command === "pyenv_install_component") throw new Error("本测试面不应触发装组件");
    throw new Error(`未预期的 IPC 命令: ${command}`);
  });
  return {
    emitStatus: (payload: Record<string, unknown>) => {
      current = payload;
    },
  };
}

describe("pyenv-api:服务组件契约(与壳侧 service_start/stop/status 对齐)", () => {
  it("serviceStart/Stop/Status:命令名与参数键 id;载荷六键守门透传", async () => {
    mocks.invoke
      .mockResolvedValueOnce(serviceStatusFixture("searxng", "running", true))
      .mockResolvedValueOnce(serviceStatusFixture())
      .mockResolvedValueOnce(serviceStatusFixture());
    await serviceStart("searxng");
    await serviceStop("searxng");
    await serviceStatus("searxng");
    expect(mocks.invoke).toHaveBeenNthCalledWith(1, "service_start", { id: "searxng" });
    expect(mocks.invoke).toHaveBeenNthCalledWith(2, "service_stop", { id: "searxng" });
    expect(mocks.invoke).toHaveBeenNthCalledWith(3, "service_status", { id: "searxng" });
  });

  it("parseServiceStatus:六键透传(number|null 宽容);非契约形态即抛", () => {
    const parsed = parseServiceStatus(serviceStatusFixture("searxng", "running", true));
    expect(parsed).toEqual({
      id: "searxng",
      state: "running",
      healthy: true,
      pid: 4242,
      started_at: 1730000000,
      last_exit: null,
    });
    // 观测三键缺键 → null(宽容,不拦渲染);id/state/healthy 非契约即抛
    expect(parseServiceStatus({ id: "searxng", state: "stopped", healthy: false })).toEqual({
      id: "searxng",
      state: "stopped",
      healthy: false,
      pid: null,
      started_at: null,
      last_exit: null,
    });
    expect(() => parseServiceStatus("not-an-object")).toThrow(TypeError);
    expect(() => parseServiceStatus({ id: "searxng", state: "bogus", healthy: false })).toThrow(TypeError);
    expect(() => parseServiceStatus({ id: "searxng", state: "running", healthy: "yes" })).toThrow(TypeError);
  });

  it("parsePyenvStatus:kind=service 透传,未知/缺省 kind → 库组件形态", () => {
    const parsed = parsePyenvStatus(
      wireFixture({
        components: [
          { id: "searxng", installed: true, kind: "service" },
          { id: "table", installed: false },
          { id: "weird", installed: false, kind: "daemon" },
        ],
      }),
    );
    expect(parsed.components).toEqual([
      { id: "searxng", installed: true, kind: "service" },
      { id: "table", installed: false, kind: undefined },
      { id: "weird", installed: false, kind: undefined },
    ]);
  });
});

describe("PyenvCard:服务组件行(启停按钮 + 健康绿点 + 状态对账)", () => {
  it("已装服务行:渲染启停按钮(未运行=「启动」/已停止徽标/灰绿点),挂载即对账 service_status", async () => {
    installServiceIpc(
      wireFixture({ components: [{ id: "searxng", installed: true, kind: "service" }] }),
    );
    installListen();
    render(<PyenvCard />);

    await screen.findByTestId("pyenv-service-searxng-start");
    expect(screen.getByTestId("pyenv-component-searxng-state").textContent).toBe("已装");
    expect(screen.getByTestId("pyenv-service-searxng-run-state").textContent).toBe("已停止");
    await waitFor(() => expect(callsOf("service_status")).toEqual([{ id: "searxng" }]));
    // 未运行:无启动开关面(Switch 不渲染——服务形态替代库开关),无绿点
    expect(screen.queryByRole("switch", { name: "组件开关 searxng" })).toBeNull();
  });

  it("未装服务行:仍走装开关(Switch 渲染,无启停按钮/状态对账)", async () => {
    installServiceIpc(
      wireFixture({ components: [{ id: "searxng", installed: false, kind: "service" }] }),
    );
    installListen();
    render(<PyenvCard />);

    await screen.findByTestId("pyenv-component-searxng");
    expect(screen.getByRole("switch", { name: "组件开关 searxng" })).toBeTruthy();
    expect(screen.queryByTestId("pyenv-service-searxng-start")).toBeNull();
    expect(screen.queryByTestId("pyenv-service-searxng-run-state")).toBeNull();
    await waitFor(() => expect(screen.getByTestId("pyenv-state-badge")).toBeTruthy());
    expect(callsOf("service_status")).toEqual([]);
  });

  it("点「启动」→ service_start({id});回包 running+healthy → 按钮翻「停止」+绿点健康 + 绿色回执", async () => {
    installServiceIpc(
      wireFixture({ components: [{ id: "searxng", installed: true, kind: "service" }] }),
      { searxng: serviceStatusFixture() },
    );
    installListen();
    render(<PyenvCard />);
    await screen.findByTestId("pyenv-service-searxng-start");

    fireEvent.click(screen.getByTestId("pyenv-service-searxng-start"));

    await waitFor(() => expect(callsOf("service_start")).toEqual([{ id: "searxng" }]));
    await waitFor(() =>
      expect(screen.getByTestId("pyenv-service-searxng-run-state").textContent).toBe("运行中"),
    );
    expect(screen.getByTestId("pyenv-service-searxng-health").className).toContain("bg-ok");
    const stop = screen.getByTestId("pyenv-service-searxng-stop") as HTMLButtonElement;
    expect(stop.disabled).toBe(false);
    expect(screen.queryByTestId("pyenv-service-searxng-start")).toBeNull();
    const note = await screen.findByTestId("pyenv-service-note");
    expect(note.getAttribute("role")).toBe("status");
    expect(note.textContent).toContain("已启动且健康检查通过");
    expect(note.textContent).toContain("pid=9999");
  });

  it("点「停止」→ service_stop({id});回包 stopped → 按钮翻「启动」+绿点转灰 + 回执", async () => {
    installServiceIpc(
      wireFixture({ components: [{ id: "searxng", installed: true, kind: "service" }] }),
      { searxng: serviceStatusFixture("searxng", "running", true) },
    );
    installListen();
    render(<PyenvCard />);

    // 挂载即对账 → 运行中态呈现(绿点/停止按钮)
    await waitFor(() =>
      expect(screen.getByTestId("pyenv-service-searxng-run-state").textContent).toBe("运行中"),
    );
    fireEvent.click(screen.getByTestId("pyenv-service-searxng-stop"));

    await waitFor(() => expect(callsOf("service_stop")).toEqual([{ id: "searxng" }]));
    await waitFor(() =>
      expect(screen.getByTestId("pyenv-service-searxng-run-state").textContent).toBe("已停止"),
    );
    expect(screen.getByTestId("pyenv-service-searxng-health").className).not.toContain("bg-ok");
    expect(screen.getByTestId("pyenv-service-searxng-start")).toBeTruthy();
    expect(screen.getByTestId("pyenv-service-note").textContent).toContain("已停止");
  });

  it("启动回包 running+healthy=false(慢启动)→ 如实呈现黄点警示回执,不谎报健康", async () => {
    const slowStart = {
      ...serviceStatusFixture("searxng", "running", false),
      pid: 4242,
    };
    installServiceIpc(
      wireFixture({ components: [{ id: "searxng", installed: true, kind: "service" }] }),
      { searxng: serviceStatusFixture() },
    );
    // 覆写 start 应答为「已拉起未绿」;初态对账仍回 stopped(点击前是停态行)
    mocks.invoke.mockImplementation(async (command: string, args?: unknown) => {
      const { id } = (args ?? {}) as { id: string };
      if (command === "service_start" && id === "searxng") return slowStart;
      if (command === "service_status") return serviceStatusFixture();
      if (command === "pyenv_get_status")
        return wireFixture({ components: [{ id: "searxng", installed: true, kind: "service" }] });
      throw new Error(`未预期的 IPC 命令: ${command}`);
    });
    installListen();
    render(<PyenvCard />);
    await screen.findByTestId("pyenv-service-searxng-start");

    fireEvent.click(screen.getByTestId("pyenv-service-searxng-start"));

    const note = await screen.findByTestId("pyenv-service-note");
    expect(note.getAttribute("role")).toBe("alert");
    expect(note.textContent).toContain("健康端点尚未通过");
    expect(screen.getByTestId("pyenv-service-searxng-run-state").textContent).toBe("运行中");
    expect(screen.getByTestId("pyenv-service-searxng-health").className).toContain("bg-warning");
  });

  it("启动回包 healthy=false(慢启动)→ 起轮询对账,转绿即停——回执承诺自动兑现", async () => {
    // 复审修复 10-06-native-plugin-components:回执承诺「稍后以状态对账为准」
    // 原先无任何自动触发源(黄点滞留直到切屏重挂载);现每 5s 自动对账。
    // 确定性时序:纯假时钟 + act 冲刷 + 同步断言——waitFor 搭 shouldAdvanceTime
    // 在慢 CI 上会漂(黄点断言曾在 GitHub runner 翻车,本地绿属时序运气)。
    vi.useFakeTimers();
    try {
      const slowStart = {
        ...serviceStatusFixture("searxng", "running", false),
        pid: 4242,
      };
      let statusCalls = 0;
      mocks.invoke.mockImplementation(async (command: string, args?: unknown) => {
        const { id } = (args ?? {}) as { id: string };
        if (command === "service_start" && id === "searxng") return slowStart;
        if (command === "service_status") {
          statusCalls += 1;
          // 第 1 次 = 挂载对账(停态);轮询对账起回绿(慢启动转绿形态)
          return statusCalls <= 1
            ? serviceStatusFixture()
            : serviceStatusFixture("searxng", "running", true);
        }
        if (command === "pyenv_get_status")
          return wireFixture({ components: [{ id: "searxng", installed: true, kind: "service" }] });
        throw new Error(`未预期的 IPC 命令: ${command}`);
      });
      installListen();
      render(<PyenvCard />);
      // 冲刷挂载对账链(pyenv_get_status → service_status 第 1 次);两轮防微任务级联
      for (let i = 0; i < 2; i += 1) {
        await act(async () => {
          await vi.advanceTimersByTimeAsync(0);
        });
      }

      fireEvent.click(screen.getByTestId("pyenv-service-searxng-start"));
      // 冲刷 start 回包落态:运行中 + 黄点,同步断言(零 waitFor)
      await act(async () => {
        await vi.advanceTimersByTimeAsync(0);
      });
      expect(screen.getByTestId("pyenv-service-searxng-run-state").textContent).toBe("运行中");
      expect(screen.getByTestId("pyenv-service-searxng-health").className).toContain("bg-warning");
      const callsBeforePoll = statusCalls;

      // 5s 后第一次轮询对账 → 黄点转绿
      await act(async () => {
        await vi.advanceTimersByTimeAsync(5_000);
      });
      expect(screen.getByTestId("pyenv-service-searxng-health").className).toContain("bg-ok");
      const callsAtGreen = statusCalls;
      expect(callsAtGreen).toBe(callsBeforePoll + 1);

      // 绿即停:再推 20s 不再对账(轮询已终止)
      await act(async () => {
        await vi.advanceTimersByTimeAsync(20_000);
      });
      expect(statusCalls).toBe(callsAtGreen);
    } finally {
      vi.useRealTimers();
    }
  });

  it("启动失败(结构化错误:启动后即退出)→ ErrorBox 上屏,行保持已停止", async () => {
    installServiceIpc(
      wireFixture({ components: [{ id: "searxng", installed: true, kind: "service" }] }),
      { searxng: serviceStatusFixture() },
    );
    mocks.invoke.mockImplementation(async (command: string, args?: unknown) => {
      if (command === "service_start") {
        if ((args as { id: string }).id === "searxng") {
          throw JSON.stringify({
            code: "service_start_failed",
            path: "$",
            message: "服务进程启动后即退出(退出码 Some(78);日志尾部见 /data/services/searxng/service.log)",
          });
        }
      }
      if (command === "service_status") return serviceStatusFixture();
      if (command === "pyenv_get_status")
        return wireFixture({ components: [{ id: "searxng", installed: true, kind: "service" }] });
      throw new Error(`未预期的 IPC 命令: ${command}`);
    });
    installListen();
    render(<PyenvCard />);
    await screen.findByTestId("pyenv-service-searxng-start");

    fireEvent.click(screen.getByTestId("pyenv-service-searxng-start"));

    const alert = await screen.findByRole("alert");
    expect(alert.textContent).toContain("启动后即退出");
    expect(alert.textContent).toContain("code=service_start_failed");
    await waitFor(() =>
      expect(screen.getByTestId("pyenv-service-searxng-run-state").textContent).toBe("已停止"),
    );
  });
});
