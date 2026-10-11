// @vitest-environment jsdom
//
// 「平台账号」卡组件测试(10-11-platform-account-config):mock sidecar
// (shell 命令 sidecar_request 假实现)+ mock @tauri-apps/plugin-shell
// (记录 authorize_url 打开)。覆盖:两段渲染三态 / 键规约预拦 / 添加授权流
// (系统浏览器打开 + note)/ App 凭据缺失结构化错 / 删除(confirm)/
// 微信段(桥可用/不可用 + 诚实披露)。
import { cleanup, fireEvent, render, screen, waitFor, within } from "@testing-library/react";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";

const mocks = vi.hoisted(() => ({ invoke: vi.fn(), shellOpen: vi.fn() }));
vi.mock("@tauri-apps/api/core", () => ({ invoke: mocks.invoke }));
vi.mock("@tauri-apps/plugin-shell", () => ({ open: mocks.shellOpen }));

import { PlatformAccountsCard } from "./platform-accounts-card";
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
    weixin?: Partial<PlatformAccountsStatus["weixin"]>;
  } = {},
): PlatformAccountsStatus {
  return {
    feishu: {
      accounts: overrides.feishuAccounts ?? [feishuEntry()],
      authorize_in_progress: overrides.authorizeInProgress ?? false,
    },
    weixin: {
      available: true,
      bin_found: true,
      weixin_configured: true,
      gateway_alive: true,
      ...(overrides.weixin ?? {}),
    },
  };
}

/** 安装 status 分发(其余方法按 handlers 增补) */
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

describe("平台账号卡:两段渲染", () => {
  it("飞书段:账号行(绿态/label/授权时间)+ 计数徽标;微信段:桥可用三布尔", async () => {
    installSidecar(statusPayload());
    render(<PlatformAccountsCard />);
    await waitFor(() => expect(screen.getByTestId("platform-accounts-card")).toBeTruthy());
    expect(screen.getByText("1 个已授权")).toBeTruthy();
    const row = screen.getByTestId("feishu-account-feishu-work");
    expect(within(row).getByText("工作号")).toBeTruthy();
    expect(within(row).getByText(/授权于 2026-10-11/)).toBeTruthy();
    expect(screen.getByTestId("platform-dot-feishu-feishu-work").className).toContain("bg-ok");
    // 微信段:三布尔全绿 + 可用徽标 + 诚实披露
    expect(screen.getByText("桥可用")).toBeTruthy();
    expect(screen.getByTestId("platform-dot-weixin-bin").className).toContain("bg-ok");
    expect(screen.getByTestId("platform-dot-weixin-configured").className).toContain("bg-ok");
    expect(screen.getByTestId("platform-dot-weixin-gateway").className).toContain("bg-ok");
    expect(screen.getByTestId("weixin-disclosure").textContent).toContain("单活");
  });

  it("灰态:refresh_ok=false 账号行带「授权态失效」;微信桥不可用三布尔全灰", async () => {
    installSidecar(
      statusPayload({
        feishuAccounts: [feishuEntry({ refresh_ok: false })],
        weixin: { available: false, bin_found: false, weixin_configured: false, gateway_alive: false },
      }),
    );
    render(<PlatformAccountsCard />);
    await waitFor(() => expect(screen.getByTestId("platform-accounts-card")).toBeTruthy());
    expect(screen.getByText(/授权态失效/)).toBeTruthy();
    expect(screen.getByText("桥不可用")).toBeTruthy();
    expect(screen.getByTestId("platform-dot-weixin-bin").className).toContain("bg-muted-foreground");
    expect(screen.getByText(/Hermes CLI 未找到/)).toBeTruthy();
  });
});

describe("平台账号卡:添加授权流", () => {
  it("键规约预拦:不合规键名 → 发起授权禁用 + 内联报因,不发请求", async () => {
    installSidecar(statusPayload());
    render(<PlatformAccountsCard />);
    await waitFor(() => expect(screen.getByTestId("platform-accounts-card")).toBeTruthy());
    fireEvent.change(screen.getByLabelText("飞书账号键名"), { target: { value: "bad-key!" } });
    expect(screen.getByRole("alert").textContent).toContain("键名不合规");
    expect(isDisabled(screen.getByRole("button", { name: /发起授权/ }))).toBe(true);
    const statusCalls = mocks.invoke.mock.calls.filter(([, args]) => (args as { method: string }).method === "platform_accounts.feishu.authorize");
    expect(statusCalls).toHaveLength(0);
  });

  it("合规键名发起授权:authorize 调用 + 系统浏览器打开授权页 + note 提示", async () => {
    installSidecar(statusPayload(), {
      "platform_accounts.feishu.authorize": ((params: { account: string; label?: string }) => {
        expect(params.account).toBe("feishu-alt2");
        expect(params.label).toBe("小号");
        return { authorize_url: "https://accounts.feishu.cn/open-apis/authen/v1/authorize?state=x", redirect_uri: "http://127.0.0.1:8731/callback", account: params.account };
      }) as never,
    });
    render(<PlatformAccountsCard />);
    await waitFor(() => expect(screen.getByTestId("platform-accounts-card")).toBeTruthy());
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
    render(<PlatformAccountsCard />);
    await waitFor(() => expect(screen.getByTestId("platform-accounts-card")).toBeTruthy());
    fireEvent.change(screen.getByLabelText("飞书账号键名"), { target: { value: "feishu-alt2" } });
    fireEvent.click(screen.getByRole("button", { name: /发起授权/ }));
    const alert = await screen.findByRole("alert");
    expect(alert.textContent).toContain("feishu_account_app_credential_missing");
    expect(alert.textContent).toContain("设置→推送");
  });
});

describe("平台账号卡:删除与探针", () => {
  it("删除:confirm 文案含 label,确认后调 delete 并刷新列表(删后空态)", async () => {
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
    render(<PlatformAccountsCard />);
    await waitFor(() => expect(screen.getByTestId("feishu-account-feishu-work")).toBeTruthy());
    fireEvent.click(within(screen.getByTestId("feishu-account-feishu-work")).getByRole("button", { name: /删除/ }));
    expect(window.confirm).toHaveBeenCalledWith(expect.stringContaining("工作号"));
    // delete 后卡面 reload:账号已清,列表回到空态
    await waitFor(() => expect(screen.queryByTestId("feishu-account-feishu-work")).toBeNull());
    expect(screen.getByText("0 个已授权")).toBeTruthy();
  });

  it("重新检查:探针返回失效 → probeNote 带原因指引重授权", async () => {
    installSidecar(statusPayload(), {
      "platform_accounts.feishu.probe": (() => ({ account: "feishu-work", refresh_ok: false, reason: "feishu_refresh_failed" })) as never,
    });
    render(<PlatformAccountsCard />);
    await waitFor(() => expect(screen.getByTestId("feishu-account-feishu-work")).toBeTruthy());
    fireEvent.click(within(screen.getByTestId("feishu-account-feishu-work")).getByRole("button", { name: /重新检查/ }));
    const note = await screen.findByTestId("probe-note");
    expect(note.textContent).toContain("授权态失效");
    expect(note.textContent).toContain("feishu_refresh_failed");
  });
});
