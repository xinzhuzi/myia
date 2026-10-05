// @vitest-environment jsdom
//
// Python 环境门禁横幅(10-05-desktop-managed-py-env D2「各屏引导空态卡」,
// AC2 收尾)。全量 mock Tauri IPC(不触真实壳):
// - command pyenv_get_status → status 形态(初拉真相源)
// - event pyenv-status-changed → 同形态随动(安装完成自动消失)
// 组件面:未就绪三态各自文案 / ready 与 deps_stale 不出现 / 就绪事件即隐 /
// 跳设置深链(#/settings?section=python-env)/ 关闭仅本会话、状态事件复现 /
// 拉取失败静默。集成面:AppLayout 挂载接线。
import { cleanup, fireEvent, render, screen, waitFor } from "@testing-library/react";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import { StrictMode } from "react";
import { MemoryRouter, Route, Routes, useLocation } from "react-router-dom";

const mocks = vi.hoisted(() => ({
  invoke: vi.fn(),
  listen: vi.fn(),
}));

vi.mock("@tauri-apps/api/core", () => ({ invoke: mocks.invoke }));
vi.mock("@tauri-apps/api/event", () => ({ listen: mocks.listen }));

import { PyenvGateBanner } from "@/components/layout/pyenv-gate-banner";
import { PYENV_STATUS_EVENT_NAME } from "@/screens/settings/pyenv-api";

function wireFixture(overrides?: Partial<Record<string, unknown>>): Record<string, unknown> {
  return {
    state: "not_configured",
    install_path: "/Users/dev/Library/Application Support/MYIA/python",
    python_path: "/Users/dev/Library/Application Support/MYIA/python/bin/python3",
    mirror_runtime: null,
    mirror_pypi: null,
    steps: [],
    ...overrides,
  };
}

/** 记录当前路由(深链断言哨兵:path + search)。 */
function LocationProbe() {
  const location = useLocation();
  return (
    <div data-testid="location-probe">
      {location.pathname}
      {location.search}
    </div>
  );
}

let currentChannel: ((event: { payload: unknown }) => void) | null = null;

/** 经当前订阅发一枚状态事件(防直线窄化的稳定调用面)。 */
function emitStatus(payload: Record<string, unknown>) {
  currentChannel?.({ payload });
}

function renderBanner(initial: Record<string, unknown> = wireFixture()) {
  mocks.invoke.mockImplementation(async (command: string) => {
    if (command === "pyenv_get_status") return initial;
    if (command === "pyenv_migration_banner") return { show: false };
    throw new Error(`未预期的 IPC 命令: ${command}`);
  });
  mocks.listen.mockImplementation(
    async (name: string, handler: (event: { payload: unknown }) => void) => {
      if (name === PYENV_STATUS_EVENT_NAME) currentChannel = handler;
      return () => undefined;
    },
  );
  return render(
    <StrictMode>
      <MemoryRouter initialEntries={["/"]}>
        <Routes>
          <Route path="/" element={<PyenvGateBanner />} />
          <Route path="/settings" element={<LocationProbe />} />
        </Routes>
      </MemoryRouter>
    </StrictMode>,
  );
}

beforeEach(() => {
  mocks.invoke.mockReset();
  mocks.listen.mockReset();
  currentChannel = null;
});

afterEach(() => {
  cleanup();
  vi.clearAllMocks();
  currentChannel = null;
});

describe("PyenvGateBanner:D2 各屏引导空态卡(AC2 收尾)", () => {
  it("not_configured → 横幅出现(人话文案+前往设置);ready/deps_stale 不出现", async () => {
    renderBanner(wireFixture({ state: "not_configured" }));
    const banner = await screen.findByTestId("pyenv-gate-banner");
    expect(banner.textContent).toContain("未配置");
    expect(banner.textContent).toContain("开始配置");

    cleanup();
    renderBanner(wireFixture({ state: "ready" }));
    await waitFor(() => expect(mocks.invoke).toHaveBeenCalled());
    expect(screen.queryByTestId("pyenv-gate-banner")).toBeNull();

    cleanup();
    renderBanner(wireFixture({ state: "deps_stale" }));
    await waitFor(() => expect(mocks.invoke).toHaveBeenCalled());
    expect(screen.queryByTestId("pyenv-gate-banner")).toBeNull();
  });

  it("error 态文案引导重装;installing 态文案见进度;状态事件就绪即隐", async () => {
    renderBanner(wireFixture({ state: "error" }));
    expect((await screen.findByTestId("pyenv-gate-banner")).textContent).toContain("异常");
    expect(screen.getByTestId("pyenv-gate-banner").textContent).toContain("重新安装");

    // 事件随动:error → installing → ready(安装完成自动消失)
    emitStatus(wireFixture({ state: "installing" }));
    await waitFor(() =>
      expect(screen.getByTestId("pyenv-gate-banner").textContent).toContain("安装中"),
    );
    emitStatus(wireFixture({ state: "ready" }));
    await waitFor(() => expect(screen.queryByTestId("pyenv-gate-banner")).toBeNull());
  });

  it("「前往设置」深链 #/settings?section=python-env;关闭仅隐本会话,状态事件复现", async () => {
    renderBanner(wireFixture({ state: "not_configured" }));
    await screen.findByTestId("pyenv-gate-banner");

    fireEvent.click(screen.getByTestId("pyenv-gate-goto-settings"));
    expect((await screen.findByTestId("location-probe")).textContent).toBe(
      "/settings?section=python-env",
    );

    cleanup();
    currentChannel = null;
    renderBanner(wireFixture({ state: "not_configured" }));
    await screen.findByTestId("pyenv-gate-banner");
    fireEvent.click(screen.getByTestId("pyenv-gate-close"));
    expect(screen.queryByTestId("pyenv-gate-banner")).toBeNull();
    // 关闭是会话级:下一个状态事件(仍未就绪)如实复现引导
    emitStatus(wireFixture({ state: "error" }));
    await waitFor(() => expect(screen.getByTestId("pyenv-gate-banner").textContent).toContain("异常"));
  });

  it("拉取失败(浏览器直开/致命盘况)→ 静默不渲染不炸", async () => {
    mocks.invoke.mockRejectedValue(new Error("IPC 不可达"));
    mocks.listen.mockImplementation(async () => () => undefined);
    render(
      <MemoryRouter>
        <PyenvGateBanner />
      </MemoryRouter>,
    );
    await waitFor(() => expect(mocks.invoke).toHaveBeenCalled());
    expect(screen.queryByTestId("pyenv-gate-banner")).toBeNull();
  });
});
