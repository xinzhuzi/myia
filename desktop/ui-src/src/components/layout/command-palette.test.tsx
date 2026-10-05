// @vitest-environment jsdom
//
// ⌘K 命令面板自检(10-04-interaction-batch A-cmd;10-05 复活后口径):
// ①唤起/关闭(⌘K·Ctrl+K 自含监听 preventDefault、Esc、遮罩点击;挂载级
// 回归在 app-layout.test);②输入过滤(中文标签/英文 keywords/空态);
// ③键盘巡游(↑↓ 环回、aria-activedescendant 同步、Enter 执行、过滤词变化
// 重置回首项);④动作(导航八屏、跑一次 = 第一个可加载插件、刷新 =
// window.location.reload)。品类组已随 TopBar 全球过滤退役(7152ff9 归
// 情报流屏),挂载直连 AppLayout(10-05 复活注记见组件头)。
import { cleanup, fireEvent, render, screen, waitFor } from "@testing-library/react";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import { MemoryRouter, useLocation } from "react-router-dom";

const mocks = vi.hoisted(() => ({
  invoke: vi.fn(),
  listen: vi.fn(),
  health: vi.fn(),
  runStart: vi.fn(),
  version: vi.fn(),
}));

vi.mock("@tauri-apps/api/core", () => ({ invoke: mocks.invoke }));
vi.mock("@tauri-apps/api/event", () => ({ listen: mocks.listen }));
vi.mock("@/lib/api", async (importOriginal) => {
  const actual = await importOriginal<typeof import("@/lib/api")>();
  return {
    ...actual,
    api: { ...actual.api, health: mocks.health, runStart: mocks.runStart, version: mocks.version },
  };
});

import { CommandPalette } from "@/components/layout/command-palette";
import type { CommandPaletteProps } from "@/components/layout/command-palette";
import type { HealthResult } from "@/lib/api";

function healthOf(
  plugins: { id: string | null; name: string | null; loaded?: boolean }[],
): HealthResult {
  return {
    command: "list",
    plugins_dir: "/home/plugins",
    db: "/home/myssia.db",
    store_error: null,
    plugins: plugins.map((entry, index) => ({
      file: `/home/plugins/${entry.id ?? `broken-${index}`}.yaml`,
      id: entry.id,
      name: entry.name,
      schedule: null,
      timezone: null,
      push_channels: [],
      loaded: entry.loaded ?? true,
      load_errors: null,
      sources: [],
    })),
    summary: { plugins: plugins.length, sources: 0, ok: 0, degraded: 0, dead: 0, unknown: 0 },
    healthy: true,
    first_run: false,
    exit_code: 0,
  } as HealthResult;
}

beforeEach(() => {
  mocks.version.mockResolvedValue({ name: "myssia", version: "1.1.1", protocol: 3 });
  mocks.listen.mockResolvedValue(() => undefined);
  mocks.invoke.mockResolvedValue({ restarted: true });
  mocks.health.mockResolvedValue(
    healthOf([
      { id: "ai-news", name: "AI资讯" },
      { id: "stocks", name: "股票" },
    ]),
  );
  mocks.runStart.mockResolvedValue({ run_id: 7, state: "running", yaml: "", dry: false, db: "" });
  // jsdom 未实现 scrollIntoView(面板巡游跟随/Radix 高亮滚动),补 stub(真实浏览器原生)
  Element.prototype.scrollIntoView = vi.fn();
});

afterEach(() => {
  cleanup();
  vi.clearAllMocks();
});

/** 路由探针:Enter 导航后读当前 pathname */
function LocationProbe() {
  const location = useLocation();
  return <div data-testid="location-probe">{location.pathname}</div>;
}

function renderPalette(overrides: Partial<CommandPaletteProps> = {}) {
  const onOpenChange = vi.fn();
  render(
    <MemoryRouter initialEntries={["/"]}>
      <LocationProbe />
      <CommandPalette open onOpenChange={onOpenChange} {...overrides} />
    </MemoryRouter>,
  );
  return { onOpenChange };
}

function getInput() {
  return screen.getByRole("combobox", { name: "搜索命令" }) as HTMLInputElement;
}

function getOptions() {
  return screen.getAllByRole("option");
}

function selectedOptionText() {
  return getOptions().find((node) => node.getAttribute("aria-selected") === "true")?.textContent;
}

describe("唤起与关闭(⌘K 自含监听)", () => {
  it("open=false 时 ⌘K / Ctrl+K 唤起:onOpenChange(true) 且 preventDefault", () => {
    const { onOpenChange } = renderPalette({ open: false });

    const metaEvent = new KeyboardEvent("keydown", { key: "k", metaKey: true, cancelable: true });
    window.dispatchEvent(metaEvent);
    expect(metaEvent.defaultPrevented).toBe(true);
    expect(onOpenChange).toHaveBeenCalledWith(true);

    onOpenChange.mockClear();
    const ctrlEvent = new KeyboardEvent("keydown", { key: "k", ctrlKey: true, cancelable: true });
    window.dispatchEvent(ctrlEvent);
    expect(ctrlEvent.defaultPrevented).toBe(true);
    expect(onOpenChange).toHaveBeenCalledWith(true);
  });

  it("已开时 ⌘K 反向关闭(toggle,Linear 惯例)", () => {
    const { onOpenChange } = renderPalette({ open: true });
    window.dispatchEvent(new KeyboardEvent("keydown", { key: "k", metaKey: true }));
    expect(onOpenChange).toHaveBeenCalledWith(false);
  });

  it("Esc 与遮罩点击关闭", () => {
    const { onOpenChange } = renderPalette();
    fireEvent.keyDown(getInput(), { key: "Escape" });
    expect(onOpenChange).toHaveBeenCalledWith(false);

    onOpenChange.mockClear();
    const overlay = document.querySelector('[data-slot="command-palette-overlay"]');
    expect(overlay).toBeTruthy();
    fireEvent.mouseDown(overlay!);
    expect(onOpenChange).toHaveBeenCalledWith(false);
  });

  it("开启后焦点落输入框(dialog 范式:初始聚焦)", async () => {
    renderPalette();
    const input = getInput();
    await waitFor(() => expect(document.activeElement).toBe(input));
  });
});

describe("命令面与输入过滤", () => {
  it("默认命令面:导航八屏 + 跑一次/刷新(品类组已随 TopBar 退役)", () => {
    renderPalette();
    const labels = getOptions().map((node) => node.textContent);
    expect(labels).toEqual([
      "仪表盘",
      "情报流",
      "源管理",
      "定时任务",
      "配置编辑",
      "消息",
      "采集日志",
      "设置",
      "跑一次第一个可用品类", // label + hint 同节点文本
      "刷新重载界面",
    ]);
    // 分组标题(非 option)
    for (const group of ["导航", "动作"]) {
      expect(screen.getByText(group, { selector: "div" })).toBeTruthy();
    }
  });

  it("中文过滤:输入「设置」→ 仅「设置」一项", () => {
    renderPalette();
    fireEvent.change(getInput(), { target: { value: "设置" } });
    const options = getOptions();
    expect(options).toHaveLength(1);
    expect(options[0].textContent).toBe("设置");
  });

  it("英文 keywords 过滤:输入「feed」→ 情报流", () => {
    renderPalette();
    fireEvent.change(getInput(), { target: { value: "feed" } });
    expect(getOptions().map((node) => node.textContent)).toEqual(["情报流"]);
  });

  it("英文 keywords 过滤:输入「cron」→ 定时任务(10-05-palette-cron-entry)", () => {
    renderPalette();
    fireEvent.change(getInput(), { target: { value: "cron" } });
    expect(getOptions().map((node) => node.textContent)).toEqual(["定时任务"]);
  });

  it("无匹配:空态文案,Enter 不动作", () => {
    const { onOpenChange } = renderPalette();
    fireEvent.change(getInput(), { target: { value: "zzzz" } });
    expect(screen.queryAllByRole("option")).toHaveLength(0);
    expect(screen.getByText("无匹配命令")).toBeTruthy();
    fireEvent.keyDown(getInput(), { key: "Enter" });
    expect(onOpenChange).not.toHaveBeenCalled();
  });
});

describe("键盘巡游(↑↓ 环回 + aria 同步)", () => {
  it("↓ 下移、↑ 从首项环回末项;aria-selected 与 aria-activedescendant 同步", () => {
    renderPalette();
    const input = getInput();

    expect(selectedOptionText()).toBe("仪表盘");
    fireEvent.keyDown(input, { key: "ArrowDown" });
    expect(selectedOptionText()).toBe("情报流");
    expect(input.getAttribute("aria-activedescendant")).toBe(getOptions()[1].id);

    fireEvent.keyDown(input, { key: "ArrowUp" });
    expect(selectedOptionText()).toBe("仪表盘");
    fireEvent.keyDown(input, { key: "ArrowUp" }); // 首项 ↑ 环回末项(刷新)
    expect(selectedOptionText()).toContain("刷新");
  });

  it("过滤词变化后巡游重置回首项", () => {
    renderPalette();
    const input = getInput();
    fireEvent.keyDown(input, { key: "ArrowDown" });
    fireEvent.keyDown(input, { key: "ArrowDown" });
    expect(selectedOptionText()).toBe("源管理");

    fireEvent.change(input, { target: { value: "日志" } });
    expect(selectedOptionText()).toBe("采集日志");
  });
});

describe("动作:导航 / 跑一次 / 刷新 / 切品类", () => {
  it("Enter 执行导航:过滤「日志」→ 路由 /logs 且面板关闭", () => {
    const { onOpenChange } = renderPalette();
    fireEvent.change(getInput(), { target: { value: "日志" } });
    fireEvent.keyDown(getInput(), { key: "Enter" });
    expect(screen.getByTestId("location-probe").textContent).toBe("/logs");
    expect(onOpenChange).toHaveBeenCalledWith(false);
  });

  it("Enter 执行导航:过滤「定时」→ 路由 /cron 且面板关闭(10-05-palette-cron-entry)", () => {
    const { onOpenChange } = renderPalette();
    fireEvent.change(getInput(), { target: { value: "定时" } });
    fireEvent.keyDown(getInput(), { key: "Enter" });
    expect(screen.getByTestId("location-probe").textContent).toBe("/cron");
    expect(onOpenChange).toHaveBeenCalledWith(false);
  });

  it("跑一次(全部品类口径 = 第一个可加载插件,global-run 同源)", async () => {
    const { onOpenChange } = renderPalette();
    fireEvent.change(getInput(), { target: { value: "跑一次" } });
    fireEvent.keyDown(getInput(), { key: "Enter" });
    await waitFor(() =>
      expect(mocks.runStart).toHaveBeenCalledWith({ yaml: "/home/plugins/ai-news.yaml" }),
    );
    expect(onOpenChange).toHaveBeenCalledWith(false);
  });

  it("跑一次(第一个可加载插件口径;前面有未加载插件时跳过)", async () => {
    mocks.health.mockResolvedValue(
      healthOf([{ id: "broken", name: null, loaded: false }, { id: "ai-news", name: "AI资讯" }]),
    );
    renderPalette();
    fireEvent.change(getInput(), { target: { value: "跑一次" } });
    fireEvent.keyDown(getInput(), { key: "Enter" });
    await waitFor(() =>
      expect(mocks.runStart).toHaveBeenCalledWith({ yaml: "/home/plugins/ai-news.yaml" }),
    );
  });

  it("跑一次失败:面板保持打开,错误脚注可见(health 异常如实入态)", async () => {
    mocks.health.mockRejectedValue(new Error("sidecar 未连接"));
    const { onOpenChange } = renderPalette();
    fireEvent.change(getInput(), { target: { value: "跑一次" } });
    fireEvent.keyDown(getInput(), { key: "Enter" });
    await waitFor(() =>
      expect(screen.getByTestId("palette-run-error").textContent).toContain("sidecar 未连接"),
    );
    expect(onOpenChange).not.toHaveBeenCalledWith(false);
  });

  it("刷新 = window.location.reload(自含,不逐屏发刷新事件)", () => {
    const original = Object.getOwnPropertyDescriptor(window, "location");
    const reload = vi.fn();
    Object.defineProperty(window, "location", {
      value: { ...(original?.value ?? {}), reload },
      writable: true,
      configurable: true,
    });
    try {
      const { onOpenChange } = renderPalette();
      fireEvent.change(getInput(), { target: { value: "刷新" } });
      fireEvent.keyDown(getInput(), { key: "Enter" });
      expect(reload).toHaveBeenCalledTimes(1);
      expect(onOpenChange).toHaveBeenCalledWith(false);
    } finally {
      if (original) Object.defineProperty(window, "location", original);
    }
  });


});
