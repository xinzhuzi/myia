// @vitest-environment jsdom
//
// 「微信账号」卡组件测试(10-11-platform-account-config;渠道本名制拆卡,
// 受限形态):桥三布尔状态灯 + 登录指引复制 + 单活诚实披露。
// 10-13-wechat-keyprovider B5:卡底「取钥器」配置行(三态徽标/未配置引导
// 文案指向 docs/wechat-keyprovider.md/保存/清除;IPC = 壳侧 Tauri 命令
// wechat_key_provider,mock 按命令名分派)。
import { cleanup, fireEvent, render, screen, waitFor } from "@testing-library/react";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";

const mocks = vi.hoisted(() => ({ invoke: vi.fn() }));
vi.mock("@tauri-apps/api/core", () => ({ invoke: mocks.invoke }));

import { WeixinAccountCard } from "./weixin-account-card";
import type { PlatformAccountsStatus } from "./platform-accounts-api";
import type { KeyProviderState } from "./wechat-keyprovider-api";

function statusPayload(weixin: Partial<PlatformAccountsStatus["weixin"]>): PlatformAccountsStatus {
  return {
    feishu: { accounts: [], authorize_in_progress: false },
    weixin: { available: true, bin_found: true, weixin_configured: true, gateway_alive: true, ...weixin },
  };
}

/** 取钥器配置态缺省(已配置且文件在场)。 */
function providerPayload(override: Partial<KeyProviderState>): KeyProviderState {
  return { configured: true, path: "/opt/tools/kp", file_exists: true, file_executable: true, ...override };
}

/** invoke 记录(命令名 + 参数),供保存/清除断言。 */
const invokeCalls: Array<[string, Record<string, unknown>]> = [];

/**
 * 按命令名分派 mock(sidecar_request → 桥状态;wechat_key_provider → 取钥器
 * 配置态,状态可变——set/clear 变更后 get 反映新值,模拟桥配置落盘回读)。
 */
function mockInvoke(weixin: Partial<PlatformAccountsStatus["weixin"]> = {}, keyProvider: Partial<KeyProviderState> = {}) {
  let provider = providerPayload(keyProvider);
  mocks.invoke.mockImplementation(async (cmd: string, args?: Record<string, unknown>) => {
    invokeCalls.push([cmd, args ?? {}]);
    if (cmd === "sidecar_request") return statusPayload(weixin);
    if (cmd === "wechat_key_provider") {
      const action = (args as { action?: string } | undefined)?.action;
      if (action === "get") return provider;
      if (action === "set") {
        provider = providerPayload({ path: (args as { path?: string }).path ?? null });
        return { ok: true };
      }
      if (action === "clear") {
        provider = providerPayload({ configured: false, path: null, file_exists: false, file_executable: false });
        return { ok: true };
      }
    }
    throw new Error(`测试未预期的 invoke:${cmd} ${JSON.stringify(args)}`);
  });
}

beforeEach(() => {
  mocks.invoke.mockReset();
  invokeCalls.length = 0;
});
afterEach(() => {
  cleanup();
});

describe("微信账号卡:受限形态渲染", () => {
  it("桥可用:三布尔全绿 + 可用徽标 + 登录指引 + 单活诚实披露", async () => {
    mockInvoke({});
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
    mockInvoke({ available: false, bin_found: false, weixin_configured: false, gateway_alive: false });
    render(<WeixinAccountCard />);
    await waitFor(() => expect(screen.getByTestId("weixin-account-card")).toBeTruthy());
    expect(screen.getByText("不可用")).toBeTruthy();
    expect(screen.getByTestId("weixin-dot-bin").className).toContain("bg-muted-foreground");
    expect(screen.getByText(/Hermes CLI 未找到/)).toBeTruthy();
    expect(screen.getByText(/微信账号缺失/)).toBeTruthy();
  });

  it("复制指引:写入剪贴板 + note 回执", async () => {
    const writeText = vi.fn().mockResolvedValue(undefined);
    Object.defineProperty(navigator, "clipboard", { value: { writeText }, configurable: true });
    mockInvoke({});
    render(<WeixinAccountCard />);
    await waitFor(() => expect(screen.getByTestId("weixin-account-card")).toBeTruthy());
    fireEvent.click(screen.getByLabelText("复制微信登录指引命令"));
    expect(writeText).toHaveBeenCalledWith("hermes gateway setup");
    expect(await screen.findByTestId("weixin-note")).toBeTruthy();
  });
});

describe("微信账号卡:取钥器配置行(10-13-wechat-keyprovider B5)", () => {
  it("已配置态:ok 徽标 + 当前路径 + 清除入口", async () => {
    mockInvoke({}, {});
    render(<WeixinAccountCard />);
    await waitFor(() => expect(screen.getByTestId("weixin-keyprovider-badge")).toBeTruthy());
    expect(screen.getByTestId("weixin-keyprovider-badge").textContent).toBe("已配置");
    expect(screen.getByTestId("weixin-keyprovider-current").textContent).toContain("/opt/tools/kp");
    expect(screen.getByLabelText("清除取钥器配置")).toBeTruthy();
    // 引导文案是未配置态专属,此处不出场
    expect(screen.queryByTestId("weixin-keyprovider-guidance")).toBeNull();
  });

  it("未配置态:outline 徽标 + 引导文案指向 docs/wechat-keyprovider.md", async () => {
    mockInvoke({}, { configured: false, path: null, file_exists: false, file_executable: false });
    render(<WeixinAccountCard />);
    await waitFor(() => expect(screen.getByTestId("weixin-keyprovider-badge")).toBeTruthy());
    expect(screen.getByTestId("weixin-keyprovider-badge").textContent).toBe("未配置");
    const guidance = screen.getByTestId("weixin-keyprovider-guidance");
    expect(guidance.textContent).toContain("未配置取钥器");
    expect(guidance.textContent).toContain("不静默降级");
    expect(guidance.textContent).toContain("docs/wechat-keyprovider.md");
    expect(screen.queryByLabelText("清除取钥器配置")).toBeNull();
  });

  it("文件缺失态:warning 徽标 + 路径回显 + 重存指引", async () => {
    mockInvoke({}, { configured: true, path: "/gone/kp", file_exists: false, file_executable: false });
    render(<WeixinAccountCard />);
    await waitFor(() => expect(screen.getByTestId("weixin-keyprovider-badge")).toBeTruthy());
    expect(screen.getByTestId("weixin-keyprovider-badge").textContent).toBe("文件缺失");
    expect(screen.getByTestId("weixin-keyprovider-missing").textContent).toContain("/gone/kp");
    expect(screen.getByTestId("weixin-keyprovider-missing").textContent).toContain("重新保存");
  });

  it("保存:输入新路径 → invoke set(绝对路径)→ 刷新 get → 已配置回显新路径", async () => {
    mockInvoke({}, { configured: false, path: null, file_exists: false, file_executable: false });
    render(<WeixinAccountCard />);
    await waitFor(() => expect(screen.getByTestId("weixin-keyprovider-badge")).toBeTruthy());
    // 未配置态:与现值不同才算 dirty,保存钮才亮
    const save = screen.getByLabelText("保存取钥器路径") as HTMLButtonElement;
    expect(save.disabled).toBe(true);
    fireEvent.change(screen.getByLabelText("取钥器路径"), { target: { value: "/opt/new-kp" } });
    expect(save.disabled).toBe(false);
    fireEvent.click(save);
    await waitFor(() => expect(screen.getByTestId("weixin-keyprovider-note")).toBeTruthy());
    expect(invokeCalls).toContainEqual(["wechat_key_provider", { action: "set", path: "/opt/new-kp" }]);
    expect(screen.getByTestId("weixin-keyprovider-note").textContent).toContain("/opt/new-kp");
    // mock 的 set 落盘回读:刷新后三态翻到已配置、新路径在「当前取钥器」
    await waitFor(() => expect(screen.getByTestId("weixin-keyprovider-badge").textContent).toBe("已配置"));
    expect(screen.getByTestId("weixin-keyprovider-current").textContent).toContain("/opt/new-kp");
  });

  it("清除:invoke clear → 刷新 get → 未配置态 + 引导文案", async () => {
    mockInvoke({}, {});
    render(<WeixinAccountCard />);
    await waitFor(() => expect(screen.getByTestId("weixin-keyprovider-badge").textContent).toBe("已配置"));
    fireEvent.click(screen.getByLabelText("清除取钥器配置"));
    await waitFor(() => expect(screen.getByTestId("weixin-keyprovider-badge").textContent).toBe("未配置"));
    expect(invokeCalls).toContainEqual(["wechat_key_provider", { action: "clear" }]);
    expect(screen.getByTestId("weixin-keyprovider-guidance").textContent).toContain("docs/wechat-keyprovider.md");
  });

  it("配置读取失败:结构化错误上屏 + 重试入口", async () => {
    mocks.invoke.mockImplementation(async (cmd: string, _args?: Record<string, unknown>) => {
      if (cmd === "sidecar_request") return statusPayload({});
      if (cmd === "wechat_key_provider") {
        throw JSON.stringify({ code: "component_missing", path: "$", message: "微信本机桥组件未安装或不可执行" });
      }
      throw new Error(`测试未预期的 invoke:${cmd}`);
    });
    render(<WeixinAccountCard />);
    await waitFor(() => expect(screen.getByTestId("weixin-keyprovider").textContent).toContain("component_missing"));
    expect(screen.getByTestId("weixin-keyprovider").textContent).toContain("微信本机桥组件未安装或不可执行");
  });
});
