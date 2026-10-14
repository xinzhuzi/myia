// @vitest-environment jsdom
//
// 「磁盘占用」分区卡 IPC 契约测试(10-14-leftover-sweep-install storage 域;
// mock Tauri IPC,不触真实壳),与壳侧 src-tauri/src/pyenv_components.rs
// pyenv_storage_usage / pyenv_reclaim_storage 对齐:
// - 分项渲染(策展目录 + 顶层文件聚合 + 其余)与总占用
// - 加载态 / 错误态(结构化错误上屏 + 重试)
// - 回收按钮条件显隐(reclaimable && bytes>0;不可回收分项无入口)
// - 回收动作:invoke target 白名单取值(playwright-browsers / 服务 id),
//   成功后重拉占用与组件状态(crawl4ai 行转「未装」的真相源链路)
// - 回收后卡态:bytes=0 → 按钮消失;服务回收后服务行消失
import { cleanup, fireEvent, render, screen, waitFor } from "@testing-library/react";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import { MemoryRouter } from "react-router-dom";

const mocks = vi.hoisted(() => ({
  invoke: vi.fn(),
  listen: vi.fn(),
}));

vi.mock("@tauri-apps/api/core", () => ({ invoke: mocks.invoke }));
vi.mock("@tauri-apps/api/event", () => ({ listen: mocks.listen }));

import { StorageCard } from "./storage-card";

// ---------------------------------------------------------------------------
// 夹具(wire 形 = 壳侧 serde 序列化 StorageUsage / PyenvStatus 的原样 JSON)
// ---------------------------------------------------------------------------

const MB = 1024 * 1024;

function usageFixture(browsersBytes: number): Record<string, unknown> {
  return {
    total: 16 * 1024 * MB + browsersBytes + 7000,
    items: [
      {
        id: "models",
        label: "模型(models/)",
        bytes: 16 * 1024 * MB,
        reclaimable: false,
        hint: "视觉模型本地权重(qwen3-vl-8b-mlx 等);删除与管理在「视觉 → 模型管理」",
      },
      {
        id: "python",
        label: "Python 运行环境(python/)",
        bytes: 1.1 * 1024 * MB,
        reclaimable: false,
        hint: "自管 Python 运行时 + 依赖;pip 件随 Python 环境重建回收",
      },
      {
        id: "playwright-browsers",
        label: "抓取浏览器(playwright-browsers/)",
        bytes: browsersBytes,
        reclaimable: true,
        hint: "回收后重装幂等:pip 件秒级跳过,浏览器需重下约 300MB 级、耗时数分钟",
      },
      {
        id: "wechat-localdb",
        label: "微信本地库解密副本(wechat-localdb/)",
        bytes: 428 * MB,
        reclaimable: false,
        hint: "TTL 默认 24h 自清(可配永不过期);随查询自动重建",
      },
      {
        id: "telegram",
        label: "Telegram 登录态(telegram/)",
        bytes: 56 * 1024,
        reclaimable: false,
        hint: "telethon session 登录态(权限 0600);不可回收——删除即掉登录态",
      },
      {
        id: "services",
        label: "壳服务数据(services/)",
        bytes: 8 * 1024,
        reclaimable: false,
        hint: "壳服务组件数据目录;按服务整目录回收",
      },
      {
        id: "top-files",
        label: "顶层文件(含隐藏)",
        bytes: 120 * MB,
        reclaimable: false,
        hint: "数据根顶层文件:配置 JSON / 数据库(myia.db、myssia.db 及 .bak 系列)",
      },
      { id: "other", label: "其余(未策展目录)", bytes: 0, reclaimable: false, hint: "未策展的一层目录自动归并" },
    ],
  };
}

function statusFixture(crawl4aiInstalled: boolean, searxngInstalled: boolean): Record<string, unknown> {
  return {
    state: "ready",
    install_path: "/Users/dev/Library/Application Support/MYIA/python",
    python_path: "/Users/dev/Library/Application Support/MYIA/python/bin/python3",
    mirror_runtime: null,
    mirror_pypi: null,
    steps: [],
    components: [
      { id: "table", installed: true },
      { id: "crawl4ai", installed: crawl4aiInstalled },
      { id: "searxng", installed: searxngInstalled, kind: "service" },
    ],
  };
}

/** 可翻转的壳侧状态(回收成功后戳已删 → installed 翻 false)。 */
const state = {
  browsersBytes: 557 * MB,
  crawl4aiInstalled: true,
  searxngInstalled: true,
  failUsage: false,
  failReclaim: false,
  reclaimTargets: [] as string[],
  usageCalls: 0,
  statusCalls: 0,
};

function renderCard(): ReturnType<typeof render> {
  return render(
    <MemoryRouter>
      <StorageCard />
    </MemoryRouter>,
  );
}

beforeEach(() => {
  state.browsersBytes = 557 * MB;
  state.crawl4aiInstalled = true;
  state.searxngInstalled = true;
  state.failUsage = false;
  state.failReclaim = false;
  state.reclaimTargets = [];
  state.usageCalls = 0;
  state.statusCalls = 0;
  mocks.listen.mockResolvedValue(() => undefined);
  mocks.invoke.mockImplementation(async (command: string, args?: Record<string, unknown>) => {
    if (command === "pyenv_storage_usage") {
      state.usageCalls += 1;
      if (state.failUsage) throw new Error("setup_failed: 数据根不可访问(/nope)");
      return usageFixture(state.browsersBytes);
    }
    if (command === "pyenv_get_status") {
      state.statusCalls += 1;
      return statusFixture(state.crawl4aiInstalled, state.searxngInstalled);
    }
    if (command === "pyenv_reclaim_storage") {
      const target = String(args?.target);
      state.reclaimTargets.push(target);
      if (state.failReclaim) {
        throw new Error(`非法回收目标: '${target}'(白名单: ["playwright-browsers", "searxng"])`);
      }
      // 壳侧回收语义:浏览器回收连带删 crawl4ai 戳;服务回收删双戳
      if (target === "playwright-browsers") {
        state.crawl4aiInstalled = false;
        state.browsersBytes = 0;
      }
      if (target === "searxng") state.searxngInstalled = false;
      return { target, reclaimed_bytes: 557 * MB };
    }
    throw new Error(`unexpected command: ${command}`);
  });
});

afterEach(() => {
  cleanup();
  vi.clearAllMocks();
});

describe("StorageCard(磁盘占用分区卡)", () => {
  it("分项渲染:策展目录 label/hint、总占用、顶层文件聚合项与文案边界(telegram 登录态/TTL 24h/重装幂等口径)", async () => {
    renderCard();
    expect(await screen.findByTestId("storage-item-models")).toBeTruthy();
    expect(screen.getByTestId("storage-total").textContent).toContain("16.5 GB");
    expect(screen.getByTestId("storage-item-telegram").textContent).toContain("不可回收");
    expect(screen.getByTestId("storage-item-wechat-localdb").textContent).toContain("TTL 默认 24h 自清(可配永不过期)");
    expect(screen.getByTestId("storage-item-playwright-browsers").textContent).toContain(
      "pip 件秒级跳过,浏览器需重下约 300MB 级、耗时数分钟",
    );
    expect(screen.getByTestId("storage-item-top-files").textContent).toContain("顶层文件(含隐藏)");
    // models 行挂「去模型管理」跳视觉屏(Q10:只展示 + 跳模型管理)
    expect(screen.getByTestId("storage-models-manage").textContent).toContain("去模型管理");
  });

  it("加载态:占用扫描未回前显示扫描中(du 级遍历秒级)", async () => {
    let releaseUsage!: (value: Record<string, unknown>) => void;
    const gate = new Promise<Record<string, unknown>>((resolve) => {
      releaseUsage = resolve;
    });
    mocks.invoke.mockImplementationOnce(() => gate);
    renderCard();
    expect(screen.getByTestId("storage-loading")).toBeTruthy();
    releaseUsage(usageFixture(state.browsersBytes));
    await screen.findByTestId("storage-total");
    expect(screen.queryByTestId("storage-loading")).toBeNull();
  });

  it("错误态:占用扫描结构化失败上屏 + 重试恢复(不 panic 不白屏)", async () => {
    state.failUsage = true;
    renderCard();
    const errorBox = await screen.findByTestId("storage-error");
    expect(errorBox.textContent).toContain("setup_failed: 数据根不可访问");
    expect(screen.getByTestId("storage-retry")).toBeTruthy();
    expect(screen.queryByTestId("storage-total")).toBeNull();
    state.failUsage = false;
    fireEvent.click(screen.getByTestId("storage-retry"));
    expect(await screen.findByTestId("storage-total")).toBeTruthy();
  });

  it("回收按钮条件显隐:仅 reclaimable 且 bytes>0 的分项有入口;bytes=0 消失", async () => {
    renderCard();
    await screen.findByTestId("storage-total");
    expect(screen.getByTestId("storage-reclaim-playwright-browsers")).toBeTruthy();
    // 不可回收分项(models 登录态 telegram 顶层文件)零回收入口
    expect(screen.queryByTestId("storage-reclaim-models")).toBeNull();
    expect(screen.queryByTestId("storage-reclaim-telegram")).toBeNull();
    expect(screen.queryByTestId("storage-reclaim-top-files")).toBeNull();
    // 回收后(bytes=0)按钮消失(mock 回收链路翻转 browsersBytes)
    fireEvent.click(screen.getByTestId("storage-reclaim-playwright-browsers"));
    await waitFor(() => {
      expect(screen.queryByTestId("storage-reclaim-playwright-browsers")).toBeNull();
    });
    expect(screen.getByTestId("storage-item-playwright-browsers").textContent).toContain("0 B");
  });

  it("浏览器回收:invoke target=playwright-browsers(白名单硬规格取值)→ 回执展示 + 重拉占用与组件状态(crawl4ai 行转「未装」的真相源链路)", async () => {
    renderCard();
    await screen.findByTestId("storage-total");
    const usageBefore = state.usageCalls;
    const statusBefore = state.statusCalls;
    fireEvent.click(screen.getByTestId("storage-reclaim-playwright-browsers"));
    await waitFor(() => {
      expect(state.reclaimTargets).toEqual(["playwright-browsers"]);
    });
    await screen.findByTestId("storage-reclaim-note");
    expect(screen.getByTestId("storage-reclaim-note").textContent).toContain("playwright-browsers");
    // 重拉链路:占用 + 组件状态都刷新(crawl4ai 戳已删 → 拉取后行转「未装」)
    await waitFor(() => {
      expect(state.usageCalls).toBeGreaterThanOrEqual(usageBefore + 1);
      expect(state.statusCalls).toBeGreaterThanOrEqual(statusBefore + 1);
    });
    expect(state.crawl4aiInstalled).toBe(false);
  });

  it("服务回收:已装 service 组件渲染服务行;点击 invoke target=searxng;回收后服务行随状态消失", async () => {
    renderCard();
    expect(await screen.findByTestId("storage-service-reclaim-searxng")).toBeTruthy();
    expect(screen.getByTestId("storage-service-reclaim-searxng").textContent).toContain("停止并回收");
    fireEvent.click(screen.getByTestId("storage-service-reclaim-searxng"));
    await waitFor(() => {
      expect(state.reclaimTargets).toEqual(["searxng"]);
    });
    // 双戳已删 → 组件状态重拉 installed=false → 服务回收行消失
    await waitFor(() => {
      expect(screen.queryByTestId("storage-service-reclaim-searxng")).toBeNull();
    });
  });

  it("回收失败:壳侧白名单拒(结构化错误)上屏,不吞", async () => {
    renderCard();
    await screen.findByTestId("storage-total");
    state.failReclaim = true;
    fireEvent.click(screen.getByTestId("storage-reclaim-playwright-browsers"));
    const alert = await screen.findByTestId("storage-reclaim-error");
    expect(alert.textContent).toContain("非法回收目标");
    expect(alert.textContent).toContain("白名单");
  });
});
