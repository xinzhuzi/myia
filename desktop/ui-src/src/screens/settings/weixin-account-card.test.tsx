// @vitest-environment jsdom
//
// 「微信账号」卡组件测试(10-11-platform-account-config;渠道本名制拆卡,
// 受限形态):桥三布尔状态灯 + 登录指引复制 + 单活诚实披露;零动作面。
import { cleanup, fireEvent, render, screen, waitFor } from "@testing-library/react";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";

const mocks = vi.hoisted(() => ({ invoke: vi.fn() }));
vi.mock("@tauri-apps/api/core", () => ({ invoke: mocks.invoke }));

import { WeixinAccountCard } from "./weixin-account-card";
import type { PlatformAccountsStatus } from "./platform-accounts-api";

function statusPayload(weixin: Partial<PlatformAccountsStatus["weixin"]>): PlatformAccountsStatus {
  return {
    feishu: { accounts: [], authorize_in_progress: false },
    weixin: { available: true, bin_found: true, weixin_configured: true, gateway_alive: true, ...weixin },
  };
}

beforeEach(() => {
  mocks.invoke.mockReset();
});
afterEach(() => {
  cleanup();
});

describe("微信账号卡:受限形态渲染", () => {
  it("桥可用:三布尔全绿 + 可用徽标 + 登录指引 + 单活诚实披露", async () => {
    mocks.invoke.mockImplementation(async (_c: string, _args: { method: string }) => {
      return statusPayload({});
    });
    render(<WeixinAccountCard />);
    await waitFor(() => expect(screen.getByTestId("weixin-account-card")).toBeTruthy());
    expect(screen.getByText("可用")).toBeTruthy();
    expect(screen.getByTestId("weixin-dot-bin").className).toContain("bg-ok");
    expect(screen.getByTestId("weixin-dot-configured").className).toContain("bg-ok");
    expect(screen.getByTestId("weixin-dot-gateway").className).toContain("bg-ok");
    expect(screen.getByText(/已配置\(扫码登录过\)/)).toBeTruthy();
    expect(screen.getByTestId("weixin-disclosure").textContent).toContain("单活");
    expect(screen.getByLabelText("复制微信登录指引命令")).toBeTruthy();
  });

  it("桥不可用:三布尔灰 + 不可用徽标 + 缺失文案", async () => {
    mocks.invoke.mockImplementation(async (_c: string, _args: { method: string }) => {
      return statusPayload({ available: false, bin_found: false, weixin_configured: false, gateway_alive: false });
    });
    render(<WeixinAccountCard />);
    await waitFor(() => expect(screen.getByTestId("weixin-account-card")).toBeTruthy());
    expect(screen.getByText("不可用")).toBeTruthy();
    expect(screen.getByTestId("weixin-dot-bin").className).toContain("bg-muted-foreground");
    expect(screen.getByText(/Hermes CLI 未找到/)).toBeTruthy();
    expect(screen.getByText(/微信账号档缺失/)).toBeTruthy();
  });

  it("复制指引:写入剪贴板 + note 回执", async () => {
    const writeText = vi.fn().mockResolvedValue(undefined);
    Object.defineProperty(navigator, "clipboard", { value: { writeText }, configurable: true });
    mocks.invoke.mockImplementation(async (_c: string) => statusPayload({}));
    render(<WeixinAccountCard />);
    await waitFor(() => expect(screen.getByTestId("weixin-account-card")).toBeTruthy());
    fireEvent.click(screen.getByLabelText("复制微信登录指引命令"));
    expect(writeText).toHaveBeenCalledWith("hermes gateway setup");
    expect(await screen.findByTestId("weixin-note")).toBeTruthy();
  });
});
