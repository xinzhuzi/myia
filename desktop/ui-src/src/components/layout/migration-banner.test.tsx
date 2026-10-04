// @vitest-environment jsdom
//
// 存量迁移一次性引导(10-05-desktop-managed-py-env 第 6 步,D5/design §6;
// implement.md 门:vitest 契约测试 + 壳侧夹具零丢失单测在 pyenv_migration.rs)。
// 全量 mock Tauri IPC(不触真实壳):
// - command pyenv_migration_banner → {show: boolean}(查询即消费:壳侧标记
//   落盘,同一数据根 show=true 至多一次 —— 组件只如实渲染,一次性由壳钉死)
// 组件面:挂载只查一次(StrictMode 双效应)/ show 才现 / 跳设置深链
// (#/settings?section=python-env,第 4 步落点)/ 关闭仅本会话 / 失败静默。
// 集成面:AppLayout 挂载接线(全局横幅位唯一)。
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

import { AppLayout } from "@/components/layout/app-layout";
import { MigrationBanner } from "@/components/layout/migration-banner";
import {
  parseMigrationBannerDecision,
  pyenvMigrationBanner,
} from "@/screens/settings/pyenv-api";

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

/** 横幅渲染容器:StrictMode 包裹(证挂载效应只查一次)+ 路由含设置哨兵。 */
function renderBanner() {
  return render(
    <StrictMode>
      <MemoryRouter initialEntries={["/"]}>
        <Routes>
          <Route path="/" element={<MigrationBanner />} />
          <Route path="/settings" element={<LocationProbe />} />
        </Routes>
      </MemoryRouter>
    </StrictMode>,
  );
}

/** 内存 Storage:jsdom 下 window.localStorage 被 Node 实验性全局遮蔽
 * (app-layout.test.tsx 同款惯例;AppLayout 集成用例渲染 Sidebar 需要)。 */
function memoryStorage(): Storage {
  const map = new Map<string, string>();
  return {
    get length() {
      return map.size;
    },
    clear: () => map.clear(),
    getItem: (key: string) => (map.has(key) ? (map.get(key) as string) : null),
    key: (index: number) => Array.from(map.keys())[index] ?? null,
    removeItem: (key: string) => void map.delete(key),
    setItem: (key: string, value: string) => void map.set(key, String(value)),
  };
}

beforeEach(() => {
  mocks.invoke.mockReset();
  mocks.listen.mockReset();
});

afterEach(() => {
  cleanup();
  vi.unstubAllGlobals();
  vi.clearAllMocks();
});

// ---------------------------------------------------------------------------
// api 层契约(命令名 / 无参 / 载荷守门)
// ---------------------------------------------------------------------------

describe("pyenv-api:pyenv_migration_banner 契约(与壳侧 pyenv_migration.rs 对齐)", () => {
  it("命令名 pyenv_migration_banner、无参;{show:boolean} 原样消费", async () => {
    mocks.invoke.mockResolvedValue({ show: true });
    const decision = await pyenvMigrationBanner();
    expect(mocks.invoke).toHaveBeenCalledTimes(1);
    expect(mocks.invoke).toHaveBeenCalledWith("pyenv_migration_banner");
    expect(decision.show).toBe(true);
  });

  it("parseMigrationBannerDecision:show 非布尔即抛(对齐破了要大声失败)", () => {
    expect(parseMigrationBannerDecision({ show: false })).toEqual({ show: false });
    expect(() => parseMigrationBannerDecision({ show: "yes" })).toThrow(TypeError);
    expect(() => parseMigrationBannerDecision({})).toThrow(TypeError);
    expect(() => parseMigrationBannerDecision("not-an-object")).toThrow(TypeError);
  });
});

// ---------------------------------------------------------------------------
// 组件面(一次性语义 / 深链跳转 / 会话内关闭 / 失败静默)
// ---------------------------------------------------------------------------

describe("MigrationBanner:存量迁移一次性引导", () => {
  it("show=true → 横幅出现(文案含自管环境/一次性配置/数据沿用);StrictMode 双效应仍只查一次", async () => {
    mocks.invoke.mockResolvedValue({ show: true });
    renderBanner();

    const banner = await screen.findByTestId("migration-banner");
    expect(banner.textContent).toContain("自管 Python 环境");
    expect(banner.textContent).toContain("一次性配置");
    expect(banner.textContent).toContain("原样沿用");
    expect(screen.getByTestId("migration-banner-goto-settings")).toBeTruthy();
    expect(screen.getByTestId("migration-banner-close")).toBeTruthy();
    await waitFor(() => expect(mocks.invoke).toHaveBeenCalledTimes(1));
  });

  it("show=false → 不渲染任何横幅(壳侧一次性消费后/全新装机)", async () => {
    mocks.invoke.mockResolvedValue({ show: false });
    renderBanner();

    await waitFor(() => expect(mocks.invoke).toHaveBeenCalledTimes(1));
    expect(screen.queryByTestId("migration-banner")).toBeNull();
  });

  it("「前往设置」→ 跳设置 python-env 分区深链 + 横幅卸载(引导只跳设置,不改数据)", async () => {
    mocks.invoke.mockResolvedValue({ show: true });
    renderBanner();
    await screen.findByTestId("migration-banner");

    fireEvent.click(screen.getByTestId("migration-banner-goto-settings"));

    expect((await screen.findByTestId("location-probe")).textContent).toBe(
      "/settings?section=python-env",
    );
    expect(screen.queryByTestId("migration-banner")).toBeNull();
  });

  it("关闭 → 本会话内隐藏,不再查询(一次性已由壳侧消费,重启后亦不现)", async () => {
    mocks.invoke.mockResolvedValue({ show: true });
    renderBanner();
    await screen.findByTestId("migration-banner");

    fireEvent.click(screen.getByTestId("migration-banner-close"));

    expect(screen.queryByTestId("migration-banner")).toBeNull();
    expect(mocks.invoke).toHaveBeenCalledTimes(1);
  });

  it("查询失败 → 静默不渲染不抛(辅助引导;环境态真相源在设置屏)", async () => {
    const consoleError = vi.spyOn(console, "error").mockImplementation(() => undefined);
    mocks.invoke.mockRejectedValue(JSON.stringify({ code: "data_root_unreadable", path: "$", message: "数据根不可读" }));
    renderBanner();

    await waitFor(() => expect(mocks.invoke).toHaveBeenCalledTimes(1));
    await waitFor(() => expect(consoleError).toHaveBeenCalledTimes(1));
    expect(screen.queryByTestId("migration-banner")).toBeNull();
  });
});

// ---------------------------------------------------------------------------
// 集成面:AppLayout 全局横幅位接线
// ---------------------------------------------------------------------------

describe("AppLayout 集成:全局横幅位", () => {
  it("AppLayout 挂载 MigrationBanner(存量根首启经布局呈现,不依赖具体屏)", async () => {
    vi.stubGlobal("localStorage", memoryStorage());
    mocks.invoke.mockImplementation(async (command: string) => {
      if (command === "pyenv_migration_banner") return { show: true };
      throw new Error(`未预期的 IPC 命令: ${command}`);
    });

    render(
      <MemoryRouter initialEntries={["/"]}>
        <AppLayout />
      </MemoryRouter>,
    );

    expect(await screen.findByTestId("migration-banner")).toBeTruthy();
    expect(mocks.invoke).toHaveBeenCalledWith("pyenv_migration_banner");
  });
});
