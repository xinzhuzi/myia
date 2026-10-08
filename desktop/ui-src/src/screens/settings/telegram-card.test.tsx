// @vitest-environment jsdom
//
// 「Telegram 监控」总卡 IPC 契约测试(10-08-tg-web-line W4;PRD AC2;
// 10-08-browser-module 接线:登录动作改调浏览器模块统一入口)。
// 契约方法(desktop/entry.py v11 对齐,全量 mock Tauri IPC 不触真实壳):
// - sidecar_request {method: "telegram.status"} → {bot:{configured,error},
//   session:{exists}, web:{accounts:[…]}}
// - sidecar_request {method: "browser.open", params:{kind:"tg_web_login",
//   session_key, force?}} → {started, op_id}(单入口铁律:登录必经浏览器
//   模块;依赖缺失 = 结构化 dependency_missing,卡面人话+修复指引可见)
// - sidecar_request {method: "telegram.web.delete", params:{account}}
// 组件面:三段状态(bot/session/web)+ 账号列表行(状态灯/重登/删除)+
// 添加账号(键名校验前置)+ 披露三条文案在卡面可见(AC5)。
// 本项目无 jest-dom:DOM 断言走原生(queryByText/non-null/disabled)。
import { cleanup, fireEvent, render, screen, waitFor } from "@testing-library/react";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";

const mocks = vi.hoisted(() => ({
  invoke: vi.fn(),
}));

vi.mock("@tauri-apps/api/core", () => ({ invoke: mocks.invoke }));

import { TelegramCard } from "./telegram-card";

function statusFixture(overrides?: {
  bot?: { configured: boolean; error?: string | null };
  session?: { exists: boolean };
  accounts?: Array<Record<string, unknown>>;
}) {
  return {
    bot: overrides?.bot ?? { configured: false, error: null },
    session: overrides?.session ?? { exists: false },
    web: { accounts: overrides?.accounts ?? [] },
  };
}

function installIpc(initial: Record<string, unknown> = statusFixture()) {
  let current = initial;
  mocks.invoke.mockImplementation(async (command: string, args?: unknown) => {
    if (command !== "sidecar_request") {
      throw new Error(`未预期的 IPC 命令: ${command}`);
    }
    const { method, params } = (args ?? {}) as { method: string; params?: Record<string, unknown> };
    if (method === "telegram.status") return current;
    if (method === "browser.open") {
      const account = String(params?.session_key ?? "");
      const accounts = (current.web as { accounts: Array<Record<string, unknown>> }).accounts.map(
        (row) => (row.account === account ? { ...row, login_in_progress: true } : row),
      );
      if (!accounts.some((row) => row.account === account)) {
        accounts.push({
          account,
          logged_in: false,
          logged_in_at: null,
          login_in_progress: true,
          login_note: null,
        });
      }
      current = { ...current, web: { accounts } };
      return { started: true, op_id: account, kind: params?.kind };
    }
    if (method === "telegram.web.delete") {
      const account = String(params?.account ?? "");
      const accounts = (current.web as { accounts: Array<Record<string, unknown>> }).accounts.filter(
        (row) => row.account !== account,
      );
      current = { ...current, web: { accounts } };
      return { deleted: true, account };
    }
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

function loginCalls() {
  return mocks.invoke.mock.calls.filter(
    ([, args]) => (args as { method: string }).method === "browser.open",
  );
}

function deleteCalls() {
  return mocks.invoke.mock.calls.filter(
    ([, args]) => (args as { method: string }).method === "telegram.web.delete",
  );
}

beforeEach(() => {
  mocks.invoke.mockReset();
});

afterEach(() => {
  cleanup();
});

describe("TelegramCard 三段状态", () => {
  it("初拉渲染 bot/session/web 三段与空账号态", async () => {
    installIpc(
      statusFixture({
        bot: { configured: true },
        session: { exists: true },
        accounts: [],
      }),
    );
    render(<TelegramCard />);
    expect(await screen.findByTestId("telegram-card")).not.toBeNull();
    expect(screen.getByText("bot 线(Bot API)")).not.toBeNull();
    expect(screen.getByText("token 已录")).not.toBeNull();
    expect(screen.getByText("用户 session(Telethon)")).not.toBeNull();
    expect(screen.getByText("session 在")).not.toBeNull();
    expect(screen.getByText("网页登录(tg_web)")).not.toBeNull();
    expect(screen.getByTestId("telegram-web-empty")).not.toBeNull();
  });

  it("未配置面给指引(bot 四步/session 首登)", async () => {
    installIpc(statusFixture());
    render(<TelegramCard />);
    await screen.findByTestId("telegram-card");
    expect(screen.getByText(/BotFather/)).not.toBeNull();
    expect(screen.getByText(/myssia telegram login/)).not.toBeNull();
  });

  it("披露三条在卡面文案可见(AC5)", async () => {
    installIpc(statusFixture());
    render(<TelegramCard />);
    await screen.findByTestId("telegram-card");
    const cardText = screen.getByTestId("telegram-card").textContent ?? "";
    expect(cardText).toContain("跟修哨兵");
    expect(cardText).toContain("建议各键专用小号");
    expect(cardText).toContain("切回 Telethon 正统线");
  });

  it("status 拉取失败给错误与重试面", async () => {
    mocks.invoke.mockRejectedValue(new Error("sidecar 未连"));
    render(<TelegramCard />);
    expect(await screen.findByText(/sidecar 未连/)).not.toBeNull();
  });
});

describe("TelegramCard 账号列表与动作", () => {
  it("账号行:状态灯 + 重登 + 删除 + 登录时间", async () => {
    installIpc(
      statusFixture({
        accounts: [
          {
            account: "telegram-alt1",
            logged_in: true,
            logged_in_at: "2026-10-08T03:00:00+00:00",
            login_in_progress: false,
            login_note: null,
          },
        ],
      }),
    );
    render(<TelegramCard />);
    expect(
      await screen.findByTestId("telegram-web-account-telegram-alt1"),
    ).not.toBeNull();
    expect(screen.getByTestId("telegram-dot-telegram-alt1")).not.toBeNull();
    expect(screen.getByTestId("telegram-web-telegram-alt1-relogin")).not.toBeNull();
    expect(screen.getByTestId("telegram-web-telegram-alt1-delete")).not.toBeNull();
    expect(screen.getByText(/登录于 2026-10-08T03:00:00\+00:00/)).not.toBeNull();
  });

  it("添加账号:键名合法 → browser.open(模块统一入口)+ 回执指引(验证码在你手机 TG 里)", async () => {
    installIpc();
    render(<TelegramCard />);
    await screen.findByTestId("telegram-card");
    const input = await screen.findByLabelText("新账号键名");
    fireEvent.change(input, { target: { value: "telegram-alt1" } });
    fireEvent.click(screen.getByTestId("telegram-web-add"));
    await waitFor(() => {
      expect(loginCalls()).toHaveLength(1);
    });
    expect(
      (loginCalls()[0]?.[1] as { params: { kind: string; session_key: string; force: boolean } })
        .params,
    ).toEqual({ kind: "tg_web_login", session_key: "telegram-alt1", force: false });
    const note = await screen.findByTestId("telegram-action-note");
    expect(note.textContent ?? "").toContain("验证码在你手机 TG 里");
    expect(note.textContent ?? "").toContain("经浏览器模块");
  });

  it("添加账号:拉起失败(拔依赖)→ 卡面人话错误+修复指引可见,零静默(AC2 钉死)", async () => {
    installIpc();
    render(<TelegramCard />);
    await screen.findByTestId("telegram-card");
    // 服务侧拔依赖形态:browser.open 同步结构化拒(playwright 缺装;
    // 消息自带人话修复指引 —— 静默失败=反模式)
    mocks.invoke.mockImplementation(async (command: string, args?: unknown) => {
      const { method } = (args ?? {}) as { method: string };
      if (method === "browser.open") {
        throw JSON.stringify({
          code: "dependency_missing",
          path: "params.kind",
          message:
            "登录窗拉不起来:playwright 库未安装。修复:设置 →「Python 环境」→ 同步依赖" +
            "(桌面锁已收录 playwright),或终端执行 pip install 'myssia[browser]'",
          data: null,
        });
      }
      if (method === "telegram.status") return statusFixture();
      if (command !== "sidecar_request") throw new Error("只应答 sidecar_request");
      throw new Error(`未预期方法 ${method}`);
    });
    const input = await screen.findByLabelText("新账号键名");
    fireEvent.change(input, { target: { value: "telegram-alt1" } });
    fireEvent.click(screen.getByTestId("telegram-web-add"));
    expect(await screen.findByTestId("error-box-dependency-missing")).not.toBeNull();
    expect(screen.getAllByText(/同步依赖/).length).toBeGreaterThan(0);
    expect(screen.getByText(/playwright 库未安装/)).not.toBeNull();
    // 失败不冒充成功:成功回执 note 不出现
    expect(screen.queryByTestId("telegram-action-note")).toBeNull();
  });

  it("添加账号:键名违全称律 → 前端先拦(零 IPC 往返)", async () => {
    installIpc();
    render(<TelegramCard />);
    await screen.findByTestId("telegram-card");
    const input = await screen.findByLabelText("新账号键名");
    fireEvent.change(input, { target: { value: "bad-key" } });
    fireEvent.click(screen.getByTestId("telegram-web-add"));
    expect(loginCalls()).toHaveLength(0);
    expect(await screen.findByText(/全称律 telegram-/)).not.toBeNull();
  });

  it("重登按钮走 force:true(拉起后行进入登录中态)", async () => {
    installIpc(
      statusFixture({
        accounts: [
          {
            account: "telegram-alt1",
            logged_in: true,
            logged_in_at: null,
            login_in_progress: false,
            login_note: null,
          },
        ],
      }),
    );
    render(<TelegramCard />);
    await screen.findByTestId("telegram-web-account-telegram-alt1");
    fireEvent.click(screen.getByTestId("telegram-web-telegram-alt1-relogin"));
    await waitFor(() => {
      expect(loginCalls()).toHaveLength(1);
    });
    expect(
      (loginCalls()[0]?.[1] as { params: { force: boolean } }).params.force,
    ).toBe(true);
    // 登录窗进行中态(mock 置 login_in_progress)回读后行翻 busy
    await screen.findByTestId("telegram-web-telegram-alt1-busy");
  });

  it("删除走 delete 方法并刷新列表", async () => {
    installIpc(
      statusFixture({
        accounts: [
          {
            account: "telegram-alt1",
            logged_in: true,
            logged_in_at: null,
            login_in_progress: false,
            login_note: null,
          },
        ],
      }),
    );
    render(<TelegramCard />);
    await screen.findByTestId("telegram-web-account-telegram-alt1");
    fireEvent.click(screen.getByTestId("telegram-web-telegram-alt1-delete"));
    await waitFor(() => {
      expect(deleteCalls()).toHaveLength(1);
    });
    expect(
      (deleteCalls()[0]?.[1] as { params: { account: string } }).params.account,
    ).toBe("telegram-alt1");
    await waitFor(() => {
      expect(
        screen.queryByTestId("telegram-web-account-telegram-alt1"),
      ).toBeNull();
    });
  });

  it("登录中行:重登/删除禁用 + busy 指示", async () => {
    installIpc(
      statusFixture({
        accounts: [
          {
            account: "telegram-alt1",
            logged_in: false,
            logged_in_at: null,
            login_in_progress: true,
            login_note: null,
          },
        ],
      }),
    );
    render(<TelegramCard />);
    expect(await screen.findByTestId("telegram-web-telegram-alt1-busy")).not.toBeNull();
    expect(
      (screen.getByTestId("telegram-web-telegram-alt1-relogin") as HTMLButtonElement).disabled,
    ).toBe(true);
    expect(
      (screen.getByTestId("telegram-web-telegram-alt1-delete") as HTMLButtonElement).disabled,
    ).toBe(true);
  });
});
