import { afterEach, describe, expect, it, vi } from "vitest";

import { systemConfirm } from "./system-confirm";

const pluginConfirm = vi.hoisted(() => vi.fn());

vi.mock("@tauri-apps/plugin-dialog", () => ({
  confirm: pluginConfirm,
}));

/** 模拟 Tauri webview 标记(生产由 Tauri 注入;defineProperty 走 configurable 便于清理) */
function stubTauriInternals() {
  Object.defineProperty(window, "__TAURI_INTERNALS__", { value: {}, configurable: true });
}

function clearTauriInternals() {
  delete (window as { __TAURI_INTERNALS__?: unknown }).__TAURI_INTERNALS__;
}

describe("systemConfirm(系统级确认弹窗)", () => {
  afterEach(() => {
    vi.restoreAllMocks();
    pluginConfirm.mockReset();
    clearTauriInternals();
  });

  it("Tauri 环境:走插件原生 confirm,title/kind/按钮文案齐备,默认 warning+确定/取消", async () => {
    stubTauriInternals();
    pluginConfirm.mockResolvedValue(true);

    const ok = await systemConfirm({
      title: "删除定时任务",
      message: "删除定时任务「每日情报」?任务记录将删除;运行历史与输出目录保留。",
      okLabel: "删除",
    });

    expect(ok).toBe(true);
    expect(pluginConfirm).toHaveBeenCalledTimes(1);
    expect(pluginConfirm).toHaveBeenCalledWith("删除定时任务「每日情报」?任务记录将删除;运行历史与输出目录保留。", {
      title: "删除定时任务",
      kind: "warning",
      okLabel: "删除",
      cancelLabel: "取消",
    });
  });

  it("Tauri 环境:kind 直传 info;用户取消 = false 原样返回", async () => {
    stubTauriInternals();
    pluginConfirm.mockResolvedValue(false);

    const ok = await systemConfirm({ title: "继续?", message: "正文", kind: "info", okLabel: "继续", cancelLabel: "返回" });

    expect(ok).toBe(false);
    expect(pluginConfirm).toHaveBeenCalledWith("正文", {
      title: "继续?",
      kind: "info",
      okLabel: "继续",
      cancelLabel: "返回",
    });
  });

  it("非 Tauri 环境:回退 window.confirm,正文原样透传,返回值透传", async () => {
    const spy = vi.spyOn(window, "confirm").mockReturnValue(false);

    const ok = await systemConfirm({ title: "删除账号", message: "确定删除账号?", okLabel: "删除" });

    expect(ok).toBe(false);
    expect(spy).toHaveBeenCalledTimes(1);
    expect(spy).toHaveBeenCalledWith("确定删除账号?");
    expect(pluginConfirm).not.toHaveBeenCalled();
  });
});
