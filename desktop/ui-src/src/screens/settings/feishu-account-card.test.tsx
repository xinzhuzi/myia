// @vitest-environment jsdom
//
// 「飞书账号」卡组件测试(10-11-platform-account-config;渠道本名制拆卡):
// mock sidecar(sidecar_request 假实现)+ mock @tauri-apps/plugin-shell
// (记录 authorize_url 打开)。覆盖:渲染三态 / 键规约预拦 / 添加授权流 /
// App 凭据缺失结构化错 / 删除 / 重新检查探针。
import { cleanup, fireEvent, render, screen, waitFor, within } from "@testing-library/react";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";

const mocks = vi.hoisted(() => ({ invoke: vi.fn(), shellOpen: vi.fn() }));
vi.mock("@tauri-apps/api/core", () => ({ invoke: mocks.invoke }));
vi.mock("@tauri-apps/plugin-shell", () => ({ open: mocks.shellOpen }));

import { FeishuAccountCard } from "./feishu-account-card";
import type { PlatformAccountsStatus } from "./platform-accounts-api";

function feishuEntry(overrides: Partial<PlatformAccountsStatus["feishu"]["accounts"][number]> = {}) {
  return {
    account: "feishu-work",
    label: "工作号",
    authorized_at: "2026-10-11T12:00:00+08:00",
    refresh_ok: true,
    refreshed_at: "2026-10-11T12:30:00+08:00",
    ...overrides,
  };
}

function statusPayload(
  overrides: {
    feishuAccounts?: PlatformAccountsStatus["feishu"]["accounts"];
    authorizeInProgress?: boolean;
  } = {},
): PlatformAccountsStatus {
  return {
    feishu: {
      accounts: overrides.feishuAccounts ?? [feishuEntry()],
      authorize_in_progress: overrides.authorizeInProgress ?? false,
    },
    weixin: { available: true, bin_found: true, weixin_configured: true, gateway_alive: true },
  };
}

function installSidecar(
  status: PlatformAccountsStatus,
  handlers: Record<string, (params: never) => unknown> = {},
): void {
  mocks.invoke.mockImplementation(async (_command: string, args: { method: string; params?: unknown }) => {
    const handler = handlers[args.method];
    if (handler) return handler(args.params as never);
    if (args.method === "platform_accounts.status") return status;
    throw JSON.stringify({ code: "method_not_found", path: "method", message: `未知方法 ${args.method}` });
  });
}

function errJson(code: string, message: string): string {
  return JSON.stringify({ code, path: "params", message });
}

beforeEach(() => {
  mocks.invoke.mockReset();
  mocks.shellOpen.mockReset();
  vi.spyOn(window, "confirm").mockReturnValue(true);
});
afterEach(() => {
  cleanup();
  vi.restoreAllMocks();
});

function isDisabled(button: HTMLElement): boolean {
  return (button as HTMLButtonElement).disabled;
}

describe("飞书账号卡:渲染", () => {
  it("账号行:绿态灯 + label 主显示 + 键与授权时间 + 计数徽标", async () => {
    installSidecar(statusPayload());
    render(<FeishuAccountCard />);
    await waitFor(() => expect(screen.getByTestId("feishu-account-card")).toBeTruthy());
    expect(screen.getByText("1 个")).toBeTruthy();
    const row = screen.getByTestId("feishu-account-feishu-work");
    expect(within(row).getByText("工作号")).toBeTruthy();
    expect(within(row).getByText(/授权于 2026-10-11/)).toBeTruthy();
    expect(screen.getByTestId("feishu-dot-feishu-work").className).toContain("bg-ok");
  });

  it("灰态:refresh_ok=false 行带「授权态失效」;授权进行中徽标", async () => {
    installSidecar(
      statusPayload({ feishuAccounts: [feishuEntry({ refresh_ok: false })], authorizeInProgress: true }),
    );
    render(<FeishuAccountCard />);
    await waitFor(() => expect(screen.getByTestId("feishu-account-card")).toBeTruthy());
    expect(screen.getByText(/授权态失效/)).toBeTruthy();
    expect(screen.getByText("授权进行中")).toBeTruthy();
  });
});

describe("飞书账号卡:添加授权流", () => {
  it("键规约预拦:不合规键名 → 发起授权禁用 + 内联报因,零请求", async () => {
    installSidecar(statusPayload());
    render(<FeishuAccountCard />);
    await waitFor(() => expect(screen.getByTestId("feishu-account-card")).toBeTruthy());
    fireEvent.change(screen.getByLabelText("飞书账号键名"), { target: { value: "bad-key!" } });
    expect(screen.getByRole("alert").textContent).toContain("键名不合规");
    expect(isDisabled(screen.getByRole("button", { name: /发起授权/ }))).toBe(true);
    const calls = mocks.invoke.mock.calls.filter(([, args]) => (args as { method: string }).method === "platform_accounts.feishu.authorize");
    expect(calls).toHaveLength(0);
  });

  it("合规键名:authorize 调用(带备注)+ 系统浏览器打开授权页 + note", async () => {
    installSidecar(statusPayload(), {
      "platform_accounts.feishu.authorize": ((params: { account: string; label?: string }) => {
        expect(params.account).toBe("feishu-alt2");
        expect(params.label).toBe("小号");
        return { authorize_url: "https://accounts.feishu.cn/open-apis/authen/v1/authorize?state=x", redirect_uri: "http://127.0.0.1:8731/callback", account: params.account };
      }) as never,
    });
    render(<FeishuAccountCard />);
    await waitFor(() => expect(screen.getByTestId("feishu-account-card")).toBeTruthy());
    fireEvent.change(screen.getByLabelText("飞书账号键名"), { target: { value: "feishu-alt2" } });
    fireEvent.change(screen.getByLabelText("飞书账号备注"), { target: { value: "小号" } });
    fireEvent.click(screen.getByRole("button", { name: /发起授权/ }));
    await waitFor(() => expect(mocks.shellOpen).toHaveBeenCalledWith(expect.stringContaining("accounts.feishu.cn")));
    expect(await screen.findByTestId("platform-note")).toBeTruthy();
    expect(screen.getByTestId("platform-note").textContent).toContain("feishu-alt2");
  });

  it("App 凭据缺失:结构化错进 ErrorBox(指引设置→推送)", async () => {
    installSidecar(statusPayload(), {
      "platform_accounts.feishu.authorize": (() => {
        throw errJson("feishu_account_app_credential_missing", "飞书应用凭据缺失:先到 设置→推送 选 feishu_card 录入");
      }) as never,
    });
    render(<FeishuAccountCard />);
    await waitFor(() => expect(screen.getByTestId("feishu-account-card")).toBeTruthy());
    fireEvent.change(screen.getByLabelText("飞书账号键名"), { target: { value: "feishu-alt2" } });
    fireEvent.click(screen.getByRole("button", { name: /发起授权/ }));
    const alert = await screen.findByRole("alert");
    expect(alert.textContent).toContain("feishu_account_app_credential_missing");
  });
});

describe("飞书账号卡:删除与探针", () => {
  it("删除:confirm 文案含 label,确认后调 delete,删后空态", async () => {
    let deleted = false;
    mocks.invoke.mockImplementation(async (_command: string, args: { method: string; params?: unknown }) => {
      if (args.method === "platform_accounts.status") {
        return deleted ? statusPayload({ feishuAccounts: [] }) : statusPayload();
      }
      if (args.method === "platform_accounts.feishu.delete") {
        deleted = true;
        expect((args.params as { account: string }).account).toBe("feishu-work");
        return { deleted: true, account: "feishu-work" };
      }
      throw JSON.stringify({ code: "method_not_found", path: "method", message: `未知方法 ${args.method}` });
    });
    render(<FeishuAccountCard />);
    await waitFor(() => expect(screen.getByTestId("feishu-account-feishu-work")).toBeTruthy());
    fireEvent.click(within(screen.getByTestId("feishu-account-feishu-work")).getByRole("button", { name: /删除/ }));
    expect(window.confirm).toHaveBeenCalledWith(expect.stringContaining("工作号"));
    await waitFor(() => expect(screen.queryByTestId("feishu-account-feishu-work")).toBeNull());
  });

  it("重新检查:探针失效 → probeNote 带原因指引重授权", async () => {
    installSidecar(statusPayload(), {
      "platform_accounts.feishu.probe": (() => ({ account: "feishu-work", refresh_ok: false, reason: "feishu_refresh_failed" })) as never,
    });
    render(<FeishuAccountCard />);
    await waitFor(() => expect(screen.getByTestId("feishu-account-feishu-work")).toBeTruthy());
    fireEvent.click(within(screen.getByTestId("feishu-account-feishu-work")).getByRole("button", { name: /重新检查/ }));
    const note = await screen.findByTestId("probe-note");
    expect(note.textContent).toContain("授权态失效");
    expect(note.textContent).toContain("feishu_refresh_failed");
  });
});
