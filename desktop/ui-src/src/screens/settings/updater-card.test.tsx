// @vitest-environment jsdom
//
// 软件更新卡片测试(v1.1.1 更新通道 UI 接线,design.md §3.3 三态):
// 无更新(回显当前版本)/ 有更新 → 下载安装 → relaunch / 检查失败 → ErrorBox。
// 附:安装失败 → ErrorBox 回退可重试。全量 mock 两个插件模块 + getVersion,
// 不触真实 Tauri IPC(Rust 侧注册与签名闭环见 desktop/UPDATER.md,不在此测)。
// 埋点断言(10-07-unified-logging 批2):检查/下载里程碑/安装/失败经
// `updater:` 前缀 console.info/warn/error 留痕(装机经 lib/log 劫持链落
// shell.log;本测试只钉 console 调用面)。
import { cleanup, fireEvent, render, screen, waitFor } from "@testing-library/react";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";

const mocks = vi.hoisted(() => ({
  check: vi.fn(),
  relaunch: vi.fn(),
  getVersion: vi.fn(),
  downloadAndInstall: vi.fn(),
}));
vi.mock("@tauri-apps/plugin-updater", () => ({ check: mocks.check }));
vi.mock("@tauri-apps/plugin-process", () => ({ relaunch: mocks.relaunch }));
vi.mock("@tauri-apps/api/app", () => ({ getVersion: mocks.getVersion }));

import type { Update } from "@tauri-apps/plugin-updater";

import { UpdaterCard } from "./updater-card";

/** 假 Update:只带卡片用到的字段(结构对照 plugin-updater dist-js 的 UpdateMetadata)。 */
function fakeUpdate(overrides?: Partial<{ version: string; currentVersion: string; body?: string }>) {
  return {
    version: "1.1.2",
    currentVersion: "1.1.1",
    body: "Fixed desktop data paths; bundled demo plugin.",
    downloadAndInstall: mocks.downloadAndInstall,
    close: vi.fn(),
    ...overrides,
  } as unknown as Update;
}

beforeEach(() => {
  mocks.check.mockReset();
  mocks.relaunch.mockReset();
  mocks.getVersion.mockReset();
  mocks.downloadAndInstall.mockReset();
  mocks.getVersion.mockResolvedValue("1.1.1");
});

afterEach(() => {
  cleanup();
  vi.clearAllMocks();
  // 埋点断言的 console spy 复原(否则 mockImplementation 会把 console.info
  // 静默到本文件后续用例);hoisted vi.fn 无原实现,restore≈reset,行为同前。
  vi.restoreAllMocks();
});

describe("设置 · 软件更新", () => {
  it("无更新:回显「已是最新(当前 v1.1.1)」,不出安装按钮", async () => {
    mocks.check.mockResolvedValue(null);
    render(<UpdaterCard />);

    fireEvent.click(screen.getByRole("button", { name: "检查更新" }));

    const status = await screen.findByTestId("updater-status");
    expect(status.textContent).toContain("已是最新");
    expect(status.textContent).toContain("v1.1.1");
    expect(screen.queryByRole("button", { name: "下载并安装" })).toBeNull();
    expect(mocks.relaunch).not.toHaveBeenCalled();
  });

  it("有更新:展示版本与 notes → 下载并安装 → relaunch", async () => {
    mocks.check.mockResolvedValue(fakeUpdate());
    render(<UpdaterCard />);

    fireEvent.click(screen.getByRole("button", { name: "检查更新" }));

    const status = await screen.findByTestId("updater-status");
    expect(status.textContent).toContain("发现新版本");
    expect(status.textContent).toContain("v1.1.2");
    expect(status.textContent).toContain("v1.1.1"); // 当前版本对照
    expect(status.textContent).toContain("Fixed desktop data paths"); // notes(body)如实展示

    fireEvent.click(screen.getByRole("button", { name: "下载并安装" }));
    await waitFor(() => {
      expect(mocks.downloadAndInstall).toHaveBeenCalledTimes(1);
      expect(mocks.relaunch).toHaveBeenCalledTimes(1);
    });
    expect(screen.getByTestId("updater-status").textContent).toContain("正在重启");
  });

  it("检查失败 → ErrorBox 结构化回显(code=updater_check_failed),可重试", async () => {
    mocks.check
      .mockRejectedValueOnce(new Error("endpoint unreachable"))
      .mockResolvedValueOnce(null);
    render(<UpdaterCard />);

    fireEvent.click(screen.getByRole("button", { name: "检查更新" }));

    const alert = await screen.findByRole("alert");
    expect(alert.textContent).toContain("endpoint unreachable");
    expect(alert.textContent).toContain("code=updater_check_failed");
    expect(screen.queryByTestId("updater-status")?.textContent).not.toContain("已是最新");

    // 重试按钮走同一条检查路径:第二次成功 → 已是最新
    fireEvent.click(screen.getByRole("button", { name: "重试" }));
    await waitFor(() => {
      expect(mocks.check).toHaveBeenCalledTimes(2);
    });
    expect(await screen.findByText(/已是最新/)).toBeTruthy();
  });

  it("安装失败 → ErrorBox(code=updater_install_failed),回到可重装态", async () => {
    mocks.check.mockResolvedValue(fakeUpdate());
    mocks.downloadAndInstall.mockRejectedValue(new Error("signature verification failed"));
    render(<UpdaterCard />);

    fireEvent.click(screen.getByRole("button", { name: "检查更新" }));
    await screen.findByText(/发现新版本/);
    fireEvent.click(screen.getByRole("button", { name: "下载并安装" }));

    const alert = await screen.findByRole("alert");
    expect(alert.textContent).toContain("signature verification failed");
    expect(alert.textContent).toContain("code=updater_install_failed");
    expect(mocks.relaunch).not.toHaveBeenCalled();
    // 失败回退 available:可再次安装
    expect(screen.getByRole("button", { name: "下载并安装" })).toBeTruthy();
  });

  // —— 埋点断言(批2;console 经 lib/log 劫持后落 shell.log)——

  /** 收集某 console 档的 updater: 前缀消息。 */
  function updaterMessages(calls: unknown[][]): string[] {
    return calls
      .map((args) => String(args[0]))
      .filter((message) => message.startsWith("updater:"));
  }

  it("埋点:检查开始/结果(发现新版)→ 下载里程碑(25/50/75%)→ 安装/重启全程留痕", async () => {
    const infoSpy = vi.spyOn(console, "info").mockImplementation(() => {});
    mocks.check.mockResolvedValue(fakeUpdate());
    // 模拟下载流:总量 1000B,四个 250B chunk(恰触发 25/50/75% 三档里程碑)
    type FakeDownloadEvent = {
      event: "Started" | "Progress" | "Finished";
      data?: { contentLength?: number; chunkLength?: number };
    };
    mocks.downloadAndInstall.mockImplementation(async (onEvent?: (event: FakeDownloadEvent) => void) => {
      onEvent?.({ event: "Started", data: { contentLength: 1000 } });
      for (let chunk = 1; chunk <= 4; chunk++) {
        onEvent?.({ event: "Progress", data: { chunkLength: 250 } });
      }
      onEvent?.({ event: "Finished" });
    });
    render(<UpdaterCard />);

    fireEvent.click(screen.getByRole("button", { name: "检查更新" }));
    await screen.findByText(/发现新版本/);
    fireEvent.click(screen.getByRole("button", { name: "下载并安装" }));
    await waitFor(() => {
      expect(mocks.relaunch).toHaveBeenCalledTimes(1);
    });

    const messages = updaterMessages(infoSpy.mock.calls);
    expect(messages).toContain("updater: 检查更新开始");
    expect(messages).toContainEqual(expect.stringContaining("updater: 检查完成: 发现新版本 v1.1.2"));
    expect(messages).toContainEqual(expect.stringContaining("updater: 开始下载并安装 v1.1.2"));
    expect(messages).toContain("updater: 下载开始(总量 1000 B)");
    expect(messages).toContain("updater: 下载进度 25%(250/1000 B)");
    expect(messages).toContain("updater: 下载进度 50%(500/1000 B)");
    expect(messages).toContain("updater: 下载进度 75%(750/1000 B)");
    expect(messages).toContain("updater: 下载完成(1000 B),请求安装");
    expect(messages).toContain("updater: 安装完成,已请求重启");
    // 100% 不另记一档(75% 后恰到顶,Finished 才收尾):里程碑档数钉死
    expect(messages.filter((m) => m.includes("下载进度")).length).toBe(3);
  });

  it("埋点:已是最新与检查失败两态各自留痕(info/warn 分级)", async () => {
    const infoSpy = vi.spyOn(console, "info").mockImplementation(() => {});
    const warnSpy = vi.spyOn(console, "warn").mockImplementation(() => {});
    mocks.check
      .mockResolvedValueOnce(null)
      .mockRejectedValueOnce(new Error("endpoint unreachable"));
    render(<UpdaterCard />);

    fireEvent.click(screen.getByRole("button", { name: "检查更新" }));
    await screen.findByText(/已是最新/);
    expect(updaterMessages(infoSpy.mock.calls)).toContainEqual(
      expect.stringContaining("updater: 检查完成: 已是最新(v1.1.1)"),
    );

    fireEvent.click(screen.getByRole("button", { name: "检查更新" }));
    const alert = await screen.findByRole("alert");
    expect(alert.textContent).toContain("endpoint unreachable");
    expect(updaterMessages(warnSpy.mock.calls)).toContainEqual(
      expect.stringContaining("updater: 检查失败: endpoint unreachable"),
    );
  });
});
