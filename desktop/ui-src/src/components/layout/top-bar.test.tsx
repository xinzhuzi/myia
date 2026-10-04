// @vitest-environment jsdom
//
// 顶栏接线测试(壳层清理后极简形态):①屏标题 = 当前路由在侧栏导航口径
// 下的页面名;②拆除断言:品牌字/面包屑/品类下拉/全局跑一次/假搜索框
// 均不再出现(侧栏已有品牌+导航;品类与跑一次由 feed/sources 屏自放
// 上下文版);③⌘K 命令面板触发器收为图标钮(button + aria-haspopup=
// dialog,点击唤起面板且 aria-expanded 翻转;面板本体细测在
// command-palette.test.tsx,此处测触发器件本身的可达语义);④health
// 仍拉取(品类清单供命令面板「切换品类」透传),失败静默不拦顶栏。
// TopBar 现消费 useLocation(屏标题),须在 MemoryRouter 下渲染。
import { cleanup, fireEvent, render, screen, waitFor } from "@testing-library/react";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import { MemoryRouter } from "react-router-dom";

const mocks = vi.hoisted(() => ({ invoke: vi.fn(), listen: vi.fn(), health: vi.fn(), version: vi.fn() }));

vi.mock("@tauri-apps/api/core", () => ({ invoke: mocks.invoke }));
vi.mock("@tauri-apps/api/event", () => ({ listen: mocks.listen }));
vi.mock("@/lib/api", async (importOriginal) => {
  const actual = await importOriginal<typeof import("@/lib/api")>();
  return { ...actual, api: { ...actual.api, health: mocks.health, version: mocks.version } };
});

import { TopBar } from "@/components/layout/top-bar";

beforeEach(() => {
  mocks.version.mockResolvedValue({ name: "myssia", version: "1.1.1", protocol: 3 });
  mocks.listen.mockResolvedValue(() => undefined);
  mocks.invoke.mockResolvedValue({ restarted: true });
  mocks.health.mockResolvedValue({ plugins: [] });
  // Radix 巡游高亮滚动 jsdom 未实现,补 stub(真实浏览器原生)
  Element.prototype.scrollIntoView = vi.fn();
});

afterEach(() => {
  cleanup();
  vi.clearAllMocks();
});

function renderTopBar(initialEntry = "/") {
  return render(
    <MemoryRouter initialEntries={[initialEntry]}>
      <TopBar category={null} onCategoryChange={vi.fn()} />
    </MemoryRouter>,
  );
}

describe("TopBar 屏标题(极简形态)", () => {
  it("标题 = 当前路由在侧栏导航口径下的页面名(分组路由)", () => {
    renderTopBar("/sources");
    expect(screen.getByText("源管理")).toBeTruthy();
  });

  it("主入口区路由同样只有页面名(根路由 = 仪表盘)", () => {
    renderTopBar("/");
    expect(screen.getByText("仪表盘")).toBeTruthy();
  });

  it("底部设置路由也在口径内(设置)", () => {
    renderTopBar("/settings");
    expect(screen.getByText("设置")).toBeTruthy();
  });
});

describe("TopBar 拆除断言(壳层清理)", () => {
  it("无面包屑、无品牌字「世事」(侧栏已有品牌+导航)", () => {
    renderTopBar("/sources");
    expect(screen.queryByRole("navigation", { name: "面包屑" })).toBeNull();
    expect(screen.queryByRole("link", { name: "世事" })).toBeNull();
    expect(screen.queryByText("世事")).toBeNull();
    expect(screen.queryByText("采集")).toBeNull(); // 分组段不出现
  });

  it("无品类下拉、无全局跑一次(由 feed/sources 屏自放上下文版)", () => {
    renderTopBar("/feed");
    expect(screen.queryByLabelText("品类选择")).toBeNull();
    expect(screen.queryByRole("button", { name: /^跑一次/ })).toBeNull();
  });

  it("无假搜索框(触发器收为图标钮,不占宽)", () => {
    renderTopBar();
    expect(screen.queryByText("搜索或跳转…")).toBeNull();
    expect(screen.queryByRole("combobox")).toBeNull();
  });
});

describe("TopBar ⌘K 命令面板触发器", () => {
  it("图标钮 = button + aria-haspopup=dialog,点击唤起面板且 aria-expanded 翻转", async () => {
    renderTopBar();
    const trigger = screen.getByRole("button", { name: "打开命令面板" });
    expect(trigger.getAttribute("aria-haspopup")).toBe("dialog");
    expect(trigger.getAttribute("aria-expanded")).toBe("false");

    fireEvent.click(trigger);
    expect(await screen.findByRole("dialog", { name: "命令面板" })).toBeTruthy();
    expect(trigger.getAttribute("aria-expanded")).toBe("true");
  });
});

describe("TopBar health 拉取(品类清单供命令面板透传)", () => {
  it("挂载即拉取一次;失败静默不拦顶栏", async () => {
    mocks.health.mockRejectedValue(new Error("sidecar 未连接"));
    renderTopBar();

    await waitFor(() => expect(mocks.health).toHaveBeenCalledTimes(1));
    // 顶栏本体仍完整:屏标题与触发器俱在
    expect(screen.getByText("仪表盘")).toBeTruthy();
    expect(screen.getByRole("button", { name: "打开命令面板" })).toBeTruthy();
  });
});
