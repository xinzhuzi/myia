// @vitest-environment jsdom
//
// 浏览器专用模块页 IPC 契约测试(10-08-browser-module 案甲;PRD AC4)。
// 契约四方法(desktop/entry.py v11 对齐,全量 mock Tauri IPC 不触真实壳):
// - sidecar_request {method: "browser.list"} → {operations: […], kinds}
// - sidecar_request {method: "browser.open", params:{kind, session_key,
//   force?}} → {started, op_id}(失败 = 结构化 error,见错误态用例)
// - sidecar_request {method: "browser.focus"/"browser.close", params:{op_id}}
// 组件面:操作台账(登录中/完成/失败+重试)+ 窗口管理(聚焦/关闭)+
// 日志尾巴 + 单入口铁律文案 + 修复指引(AC2:静默失败=反模式)。
// 本项目无 jest-dom:DOM 断言走原生(queryByText/non-null/disabled)。
import { cleanup, fireEvent, render, screen, waitFor } from "@testing-library/react";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";

const mocks = vi.hoisted(() => ({
  invoke: vi.fn(),
}));

vi.mock("@tauri-apps/api/core", () => ({ invoke: mocks.invoke }));

import { BrowserModuleCard } from "./browser-module";
import type { BrowserListResult, BrowserOperation } from "./browser-api";

function opFixture(overrides?: Partial<BrowserOperation>): BrowserOperation {
  return {
    op_id: "telegram-alt1",
    kind: "tg_web_login",
    session_key: "telegram-alt1",
    url: "https://web.telegram.org",
    phase: "done",
    note: "登录完成(登录态已落配置档,0700/0600)",
    fix_hint: null,
    started_at: "2026-10-08T05:00:00+00:00",
    finished_at: "2026-10-08T05:03:00+00:00",
    log_tail: ["2026-10-08T05:00:00+00:00 操作登记:tg_web_login 会话 telegram-alt1(force=false)"],
    ...overrides,
  };
}

function ledgerFixture(operations: BrowserOperation[]): BrowserListResult {
  return {
    operations,
    kinds: { tg_web_login: "TG 网页线登录(web.telegram.org;复用 web_line 登录器)" },
  };
}

function installIpc(initial: BrowserListResult = ledgerFixture([])) {
  let current = initial;
  mocks.invoke.mockImplementation(async (command: string, args?: unknown) => {
    if (command !== "sidecar_request") {
      throw new Error(`未预期的 IPC 命令: ${command}`);
    }
    const { method, params } = (args ?? {}) as { method: string; params?: Record<string, unknown> };
    if (method === "browser.list") return current;
    if (method === "browser.open") {
      const sessionKey = String(params?.session_key ?? "");
      current = {
        ...current,
        operations: [
          opFixture({
            op_id: sessionKey,
            session_key: sessionKey,
            phase: "running",
            note: "登录窗拉起中(浏览器窗口即将弹出)",
            finished_at: null,
          }),
          ...current.operations.filter((row) => row.op_id !== sessionKey),
        ],
      };
      return { started: true, op_id: sessionKey, kind: params?.kind };
    }
    if (method === "browser.focus") return { focused: true, op_id: params?.op_id };
    if (method === "browser.close") return { closed: true, op_id: params?.op_id, note: "已请求关闭" };
    if (method === "version") return { version: "test" };
    if (method === "health") return { ok: true };
    throw new Error(`未预期的 sidecar 方法: ${method}`);
  });
  return {
    get current() {
      return current;
    },
  };
}

function callsOf(method: string) {
  return mocks.invoke.mock.calls.filter(
    ([, args]) => (args as { method: string }).method === method,
  );
}

beforeEach(() => {
  mocks.invoke.mockReset();
});

afterEach(() => {
  cleanup();
});

describe("BrowserModuleCard 台账渲染", () => {
  it("空台账:空态指引可见(指向 Telegram 卡添加账号,单入口文案在卡面)", async () => {
    installIpc(ledgerFixture([]));
    render(<BrowserModuleCard />);
    expect(await screen.findByTestId("browser-module-card")).not.toBeNull();
    expect(screen.getByTestId("browser-operations-empty")).not.toBeNull();
    const text = screen.getByTestId("browser-module-card").textContent ?? "";
    expect(text).toContain("统一入口");
    expect(text).toContain("单入口");
  });

  it("完成态操作行:徽标 + 会话键 + 日志尾巴", async () => {
    installIpc(ledgerFixture([opFixture()]));
    render(<BrowserModuleCard />);
    expect(await screen.findByTestId("browser-op-telegram-alt1")).not.toBeNull();
    expect(screen.getByTestId("browser-op-telegram-alt1-phase").textContent).toContain("完成");
    expect(screen.getByTestId("browser-op-telegram-alt1-log")).not.toBeNull();
    // 终态行无聚焦/关闭/重试按钮
    expect(screen.queryByTestId("browser-op-telegram-alt1-focus")).toBeNull();
    expect(screen.queryByTestId("browser-op-telegram-alt1-close")).toBeNull();
    expect(screen.queryByTestId("browser-op-telegram-alt1-retry")).toBeNull();
  });

  it("进行中操作行:聚焦/关闭按钮在,重试不在", async () => {
    installIpc(
      ledgerFixture([
        opFixture({ phase: "running", note: "登录窗拉起中(浏览器窗口即将弹出)", finished_at: null }),
      ]),
    );
    render(<BrowserModuleCard />);
    expect(await screen.findByTestId("browser-op-telegram-alt1-phase")).not.toBeNull();
    expect(screen.getByTestId("browser-op-telegram-alt1-focus")).not.toBeNull();
    expect(screen.getByTestId("browser-op-telegram-alt1-close")).not.toBeNull();
    expect(screen.queryByTestId("browser-op-telegram-alt1-retry")).toBeNull();
  });

  it("失败操作行:人话错误(alert)+ 修复指引 + 重试按钮(AC2:静默失败=反模式)", async () => {
    installIpc(
      ledgerFixture([
        opFixture({
          phase: "failed",
          note: "浏览器二进制缺失(Chromium 未下载):Executable doesn't exist at …",
          fix_hint: "设置 →「Python 环境」→ 安装「JS 渲染抓取(crawl4ai)」组件(含 Chromium 下载)",
        }),
      ]),
    );
    render(<BrowserModuleCard />);
    expect(await screen.findByTestId("browser-op-telegram-alt1-phase")).not.toBeNull();
    expect(screen.getByRole("alert").textContent).toContain("浏览器二进制缺失");
    expect(screen.getByTestId("browser-op-telegram-alt1-fix").textContent).toContain("修复指引");
    expect(screen.getByTestId("browser-op-telegram-alt1-fix").textContent).toContain("crawl4ai");
    expect(screen.getByTestId("browser-op-telegram-alt1-retry")).not.toBeNull();
  });

  it("台账拉取失败:错误面 + 重试", async () => {
    mocks.invoke.mockRejectedValue(new Error("sidecar 未连"));
    render(<BrowserModuleCard />);
    expect(await screen.findByText(/sidecar 未连/)).not.toBeNull();
  });
});

describe("BrowserModuleCard 窗口管理与重试动作", () => {
  it("聚焦走 browser.focus {op_id}", async () => {
    installIpc(
      ledgerFixture([
        opFixture({ phase: "running", note: null, finished_at: null }),
      ]),
    );
    render(<BrowserModuleCard />);
    await screen.findByTestId("browser-op-telegram-alt1");
    fireEvent.click(screen.getByTestId("browser-op-telegram-alt1-focus"));
    await waitFor(() => {
      expect(callsOf("browser.focus")).toHaveLength(1);
    });
    expect(
      (callsOf("browser.focus")[0]?.[1] as { params: { op_id: string } }).params.op_id,
    ).toBe("telegram-alt1");
  });

  it("关闭走 browser.close {op_id}", async () => {
    installIpc(
      ledgerFixture([
        opFixture({ phase: "running", note: null, finished_at: null }),
      ]),
    );
    render(<BrowserModuleCard />);
    await screen.findByTestId("browser-op-telegram-alt1");
    fireEvent.click(screen.getByTestId("browser-op-telegram-alt1-close"));
    await waitFor(() => {
      expect(callsOf("browser.close")).toHaveLength(1);
    });
  });

  it("失败重试走 browser.open 同 kind+会话键 force:true(单入口铁律)", async () => {
    const state = installIpc(
      ledgerFixture([
        opFixture({ phase: "failed", note: "登录等待超时", fix_hint: "重新点「添加账号 / 重新登录」再试" }),
      ]),
    );
    render(<BrowserModuleCard />);
    await screen.findByTestId("browser-op-telegram-alt1-retry");
    fireEvent.click(screen.getByTestId("browser-op-telegram-alt1-retry"));
    await waitFor(() => {
      expect(callsOf("browser.open")).toHaveLength(1);
    });
    expect(
      (callsOf("browser.open")[0]?.[1] as { params: Record<string, unknown> }).params,
    ).toEqual({ kind: "tg_web_login", session_key: "telegram-alt1", force: true });
    // 重试后回执 note 可见 + 台账刷新(行转 running)
    expect(await screen.findByTestId("browser-action-note")).not.toBeNull();
    expect(
      state.current.operations.some((row) => row.phase === "running"),
    ).toBe(true);
  });
});
