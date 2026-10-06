// @vitest-environment jsdom
//
// UI 日志面测试(10-07-unified-logging 批2;AC10):console 劫持转发
// (forwardConsole 模式 → @tauri-apps/plugin-log JS API)、onerror/
// unhandledrejection 兜底注册与前缀化、非 tauri 容器跳过、幂等不翻倍。
// 全量 mock plugin-log 模块(返回 Promise,同真实 invoke 契约),不触真实
// IPC;__TAURI_INTERNALS__ 按 webview 注入形态模拟。模块是单例——用
// __uninstallForTests 逐例撤装(console 原函数还原 + 兜底 handler 摘除)
// 防污染后续用例。
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";

const mocks = vi.hoisted(() => ({
  // 签名带 message: string(同真实 plugin fn 契约),mock.calls 才是有参元组
  info: vi.fn(async (_message: string) => {}),
  warn: vi.fn(async (_message: string) => {}),
  error: vi.fn(async (_message: string) => {}),
}));
vi.mock("@tauri-apps/plugin-log", () => ({
  info: mocks.info,
  warn: mocks.warn,
  error: mocks.error,
}));

import { installConsoleForward, installGlobalErrorHandlers, installUiLogging, __uninstallForTests } from "./log";

describe("lib/log · UI 日志面", () => {
  beforeEach(() => {
    mocks.info.mockClear();
    mocks.warn.mockClear();
    mocks.error.mockClear();
    // webview 注入形态(生产前提);非 tauri 用例自行摘除
    (window as unknown as Record<string, unknown>).__TAURI_INTERNALS__ = {};
  });

  afterEach(() => {
    __uninstallForTests();
    delete (window as unknown as Record<string, unknown>).__TAURI_INTERNALS__;
    vi.restoreAllMocks();
  });

  it("console 四档劫持:原函数仍执行 + 按级转发 plugin JS API(对象/Error 格式化)", () => {
    const logSpy = vi.spyOn(console, "log");
    const warnSpy = vi.spyOn(console, "warn");
    installConsoleForward();

    console.log("纯文本", 42);
    console.info({ key: "值" });
    console.warn("警告行");
    console.error(new Error("崩了"));

    // 原函数仍执行(devtools 展示语义不变)
    expect(logSpy).toHaveBeenCalledWith("纯文本", 42);
    expect(warnSpy).toHaveBeenCalledWith("警告行");
    // 按级转发:log/info→info、warn→warn、error→error(Error 带 name: message)
    expect(mocks.info).toHaveBeenCalledWith("纯文本 42");
    expect(mocks.info).toHaveBeenCalledWith('{"key":"值"}');
    expect(mocks.warn).toHaveBeenCalledWith("警告行");
    expect(mocks.error).toHaveBeenCalledTimes(1);
    expect(mocks.error.mock.calls[0][0]).toContain("Error: 崩了");
  });

  it("幂等:重复安装不重挂(同一条 console.log 恰转发一次)", () => {
    const logSpy = vi.spyOn(console, "log");
    installConsoleForward();
    installConsoleForward(); // 二次安装应零行为
    installUiLogging(); // 聚合入口重复调也零行为

    console.log("只此一份");
    expect(logSpy).toHaveBeenCalledTimes(1);
    expect(mocks.info).toHaveBeenCalledTimes(1);
    expect(mocks.info).toHaveBeenCalledWith("只此一份");
  });

  it("非 tauri 容器(浏览器 dev):console 原样执行,零转发零 invoke", () => {
    delete (window as unknown as Record<string, unknown>).__TAURI_INTERNALS__;
    const logSpy = vi.spyOn(console, "log");
    installConsoleForward();

    console.log("浏览器里的一行");
    expect(logSpy).toHaveBeenCalledWith("浏览器里的一行");
    expect(mocks.info).not.toHaveBeenCalled();
  });

  it("onerror 兜底:window error 事件 → 前缀 window.onerror 落 error 级恰一份", () => {
    installGlobalErrorHandlers();

    window.dispatchEvent(
      new ErrorEvent("error", {
        message: "脚本炸了",
        filename: "http://localhost/app.js",
        lineno: 10,
        colno: 5,
      }),
    );

    expect(mocks.error).toHaveBeenCalledTimes(1);
    const message = mocks.error.mock.calls[0][0] as string;
    expect(message).toContain("window.onerror: 脚本炸了");
    expect(message).toContain("app.js:10:5");
  });

  it("unhandledrejection 兜底:Promise 拒绝 → 前缀 unhandledrejection 落 error 级恰一份", () => {
    installGlobalErrorHandlers();

    window.dispatchEvent(
      new PromiseRejectionEvent("unhandledrejection", {
        promise: Promise.resolve(), // 已决 promise:不制造真实未捕获拒绝
        reason: new Error("没人接的拒绝"),
      }),
    );

    expect(mocks.error).toHaveBeenCalledTimes(1);
    expect(mocks.error.mock.calls[0][0]).toContain("unhandledrejection: Error: 没人接的拒绝");
  });

  it("installUiLogging 聚合入口:console 劫持 + 双兜底一次装齐", () => {
    installUiLogging();

    console.info("经聚合入口的行");
    window.dispatchEvent(
      new ErrorEvent("error", { message: "聚合后崩溃", filename: "", lineno: 0, colno: 0 }),
    );

    expect(mocks.info).toHaveBeenCalledWith("经聚合入口的行");
    expect(mocks.error).toHaveBeenCalledWith(
      expect.stringContaining("window.onerror: 聚合后崩溃"),
    );
  });

  it("撤装(测试隔离契约):console 还原 + 兜底 handler 摘除 + 可重装", () => {
    const logSpy = vi.spyOn(console, "log");
    installUiLogging();
    __uninstallForTests();

    console.log("撤装后的行");
    window.dispatchEvent(new ErrorEvent("error", { message: "撤装后崩溃" }));
    expect(logSpy).toHaveBeenCalledWith("撤装后的行");
    expect(mocks.info).not.toHaveBeenCalled();
    expect(mocks.error).not.toHaveBeenCalled();

    // 重装可用(安装旗已复位)
    installUiLogging();
    console.warn("重装后的行");
    expect(mocks.warn).toHaveBeenCalledWith("重装后的行");
  });
});
