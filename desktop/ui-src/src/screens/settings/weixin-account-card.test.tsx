// @vitest-environment jsdom
//
// 「微信账号」卡组件测试(10-11-platform-account-config;渠道本名制拆卡,
// 受限形态):桥三布尔状态灯 + 登录指引复制 + 单活诚实披露。
// 10-13-wechat-keyprovider B5:卡底「取钥器」配置行(三态徽标/未配置引导
// 文案指向 docs/wechat-keyprovider.md/保存/清除;IPC = 壳侧 Tauri 命令
// wechat_key_provider,mock 按命令名分派)。
// 10-13-wechat-monitor-ui A 线:密钥状态行(wechat_key_status 三态)+ 卡内
// 三步获取面板(confirm→running→result;progress = wechat-key-acquire 事件,
// mock listen 捕获 handler 后由用例派发;acquire 命令回包 = 手动 deferred,
// 终态时机由用例控制)。
import { act, cleanup, fireEvent, render, screen, waitFor } from "@testing-library/react";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";

const mocks = vi.hoisted(() => ({ invoke: vi.fn(), listen: vi.fn() }));
vi.mock("@tauri-apps/api/core", () => ({ invoke: mocks.invoke }));
vi.mock("@tauri-apps/api/event", () => ({ listen: mocks.listen }));

import { WeixinAccountCard } from "./weixin-account-card";
import type { PlatformAccountsStatus } from "./platform-accounts-api";
import { KEY_ACQUIRE_EVENT_NAME, type KeyProviderState, type WechatKeyStatus } from "./wechat-keyprovider-api";

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

/** 密钥三态缺省(ready;§B.1 wire 形)。 */
function keyStatusPayload(override: Partial<WechatKeyStatus>): WechatKeyStatus {
  return {
    state: "ready",
    db_count: 20,
    acquired_at: new Date().toISOString(),
    wechat_version: "4.1.15",
    verdict_note: "抽样 3 库验真通过",
    ...override,
  };
}

/** invoke 记录(命令名 + 参数),供保存/清除断言。 */
const invokeCalls: Array<[string, Record<string, unknown>]> = [];

/** wechat-key-acquire 事件派发器(listen mock 捕获的 handler)。 */
let dispatchKeyEvent: ((payload: unknown) => void) | null = null;

/**
 * 按命令名分派 mock(sidecar_request → 桥状态;wechat_key_provider → 取钥器
 * 配置态,状态可变——set/clear 变更后 get 反映新值,模拟桥配置落盘回读;
 * wechat_key_status → 密钥三态;wechat_key_acquire → 挂起 deferred(用例
 * 显式 resolve 控制终态时机);wechat_key_acquire_cancel → {ok})。
 */
function mockInvoke(weixin: Partial<PlatformAccountsStatus["weixin"]> = {}, keyProvider: Partial<KeyProviderState> = {}, keyStatus: Partial<WechatKeyStatus> = {}) {
  let provider = providerPayload(keyProvider);
  mocks.invoke.mockImplementation(async (cmd: string, args?: Record<string, unknown>) => {
    invokeCalls.push([cmd, args ?? {}]);
    if (cmd === "sidecar_request") return statusPayload(weixin);
    if (cmd === "wechat_key_status") return keyStatusPayload(keyStatus);
    if (cmd === "wechat_key_acquire") return new Promise(() => {});
    if (cmd === "wechat_key_acquire_cancel") return { ok: true };
    // E2 安装面缺省:源不在(引导文案形态,不掺和既有用例断言)
    if (cmd === "wechat_key_provider_install" && (args as { action?: string } | undefined)?.action === "inspect") {
      return { available: false, source_dir: null, installed: false, installed_path: null, files: [] };
    }
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

/**
 * 获取流专用 mock:wechat_key_acquire 回包挂起为手动 deferred,返回
 * resolve 函数(用例在派发若干 progress 事件后再收终态,全程可控)。
 */
function mockInvokeWithAcquire(keyStatus: Partial<WechatKeyStatus> = {}) {
  let resolveAcquire!: (value: unknown) => void;
  mocks.invoke.mockImplementation(async (cmd: string, args?: Record<string, unknown>) => {
    invokeCalls.push([cmd, args ?? {}]);
    if (cmd === "sidecar_request") return statusPayload({});
    if (cmd === "wechat_key_provider" && (args as { action?: string } | undefined)?.action === "get") {
      return providerPayload({});
    }
    if (
      cmd === "wechat_key_provider_install" &&
      (args as { action?: string } | undefined)?.action === "inspect"
    ) {
      return { available: false, source_dir: null, installed: false, installed_path: null, files: [] };
    }
    if (cmd === "wechat_key_status") return keyStatusPayload(keyStatus);
    if (cmd === "wechat_key_acquire") {
      return new Promise((resolve) => {
        resolveAcquire = resolve;
      });
    }
    if (cmd === "wechat_key_acquire_cancel") return { ok: true };
    throw new Error(`测试未预期的 invoke:${cmd} ${JSON.stringify(args)}`);
  });
  return (value: unknown) => resolveAcquire(value);
}

beforeEach(() => {
  mocks.invoke.mockReset();
  mocks.listen.mockReset();
  invokeCalls.length = 0;
  dispatchKeyEvent = null;
  mocks.listen.mockImplementation(
    async (name: string, handler: (event: { payload: unknown }) => void) => {
      if (name === KEY_ACQUIRE_EVENT_NAME) {
        dispatchKeyEvent = (payload: unknown) => handler({ payload });
      }
      return () => undefined;
    },
  );
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
      if (cmd === "wechat_key_status") {
        return keyStatusPayload({ state: "missing", db_count: 0, acquired_at: null, verdict_note: null });
      }
      if (cmd === "wechat_key_provider_install") {
        return { available: false, source_dir: null, installed: false, installed_path: null, files: [] };
      }
      throw new Error(`测试未预期的 invoke:${cmd}`);
    });
    render(<WeixinAccountCard />);
    await waitFor(() => expect(screen.getByTestId("weixin-keyprovider").textContent).toContain("component_missing"));
    expect(screen.getByTestId("weixin-keyprovider").textContent).toContain("微信本机桥组件未安装或不可执行");
  });
});

describe("微信账号卡:密钥状态行与获取流(10-13-wechat-monitor-ui A 线)", () => {
  it("密钥状态行三态渲染:ready=已就绪 N 库+取得时间 / stale=已失效 / missing=未获取", async () => {
    const missing = { state: "missing" as const, db_count: 0, acquired_at: null, verdict_note: null };
    mockInvoke({}, {}, { state: "ready", db_count: 20 });
    const first = render(<WeixinAccountCard />);
    await waitFor(() => expect(screen.getByTestId("weixin-keystatus-badge").textContent).toBe("已就绪 20 库"));
    // acquired_at = now(同日)→ 「今天 HH:MM」相对词面;ready 态按钮 = 重新获取
    expect(screen.getByTestId("weixin-keystatus-time").textContent).toContain("今天");
    expect(screen.getByTestId("weixin-keystatus-refresh").textContent).toBe("重新获取");
    expect(screen.getByText("抽样 3 库验真通过")).toBeTruthy();
    first.unmount();

    mockInvoke({}, {}, { state: "stale", db_count: 20, verdict_note: "抽样验真失败:1/3" });
    const second = render(<WeixinAccountCard />);
    await waitFor(() => expect(screen.getByTestId("weixin-keystatus-badge").textContent).toBe("已失效"));
    expect(screen.getByText("抽样验真失败:1/3")).toBeTruthy();
    second.unmount();

    mockInvoke({}, {}, missing);
    render(<WeixinAccountCard />);
    await waitFor(() => expect(screen.getByTestId("weixin-keystatus-badge").textContent).toBe("未获取"));
    // missing:无取得时间,按钮回「获取密钥」
    expect(screen.queryByTestId("weixin-keystatus-time")).toBeNull();
    expect(screen.getByTestId("weixin-keystatus-refresh").textContent).toBe("获取密钥");
  });

  it("获取流全程 confirm 到 result:双文案 → 开始(force:false)→ 步进词表+detail+乱序丢弃 → 成功形+重拉 status", async () => {
    const resolveAcquire = mockInvokeWithAcquire({
      state: "missing",
      db_count: 0,
      acquired_at: null,
      verdict_note: null,
    });
    render(<WeixinAccountCard />);
    await waitFor(() => expect(screen.getByTestId("weixin-keystatus-badge").textContent).toBe("未获取"));
    const statusCallsBefore = invokeCalls.filter(([cmd]) => cmd === "wechat_key_status").length;

    // ① confirm:两行文案逐字(§4 文案表);missing 态入口无覆盖语义行
    fireEvent.click(screen.getByTestId("weixin-keystatus-refresh"));
    const confirm = screen.getByTestId("weixin-keyacquire-confirm");
    expect(confirm.textContent).toContain("接下来会弹出系统密码框;请在微信里退出登录并重新扫码一次。");
    expect(confirm.textContent).toContain("全程只读,微信数据不会被修改。");
    expect(confirm.textContent).not.toContain("当前密钥将在新密钥验证通过后覆盖");

    // ② 开始 → running;force:false(missing 场景不走缓存短路)
    fireEvent.click(screen.getByTestId("weixin-keyacquire-start"));
    expect(invokeCalls).toContainEqual(["wechat_key_acquire", { force: false }]);
    await waitFor(() => expect(screen.getByTestId("weixin-keyacquire-running")).toBeTruthy());
    // 首事件前:第一步高亮;四阶段词表逐字(§D.3)
    expect(screen.getByText("等待输入密码").getAttribute("aria-current")).toBe("step");
    expect(screen.getByText("正在连接微信")).toBeTruthy();
    expect(screen.getByText("等待重新登录")).toBeTruthy();
    expect(screen.getByText("正在验证数据库")).toBeTruthy();

    // ③ progress 事件:步进推进 + detail 原文(mono 行,只显最新一条)
    await act(async () => {
      dispatchKeyEvent?.({ seq: 1, phase: "password", detail: "等待输入管理员密码" });
    });
    expect(screen.getByText("等待输入管理员密码")).toBeTruthy();
    await act(async () => {
      dispatchKeyEvent?.({ seq: 2, phase: "attach", detail: "连接建立" });
    });
    expect(screen.getByText("连接建立")).toBeTruthy();
    expect(screen.queryByText("等待输入管理员密码")).toBeNull();
    // password 已完成(打勾形=text-ok),attach 当前
    expect(screen.getByText("等待输入密码").className).toContain("text-ok");
    expect(screen.getByText("正在连接微信").getAttribute("aria-current")).toBe("step");

    // ④ 乱序旧包丢弃:seq=1 旧包不改写当前阶段/不进 detail
    await act(async () => {
      dispatchKeyEvent?.({ seq: 1, phase: "password", detail: "过期旧包" });
    });
    expect(screen.getByText("正在连接微信").getAttribute("aria-current")).toBe("step");
    expect(screen.queryByText("过期旧包")).toBeNull();

    // ⑤ 终态回包:ok + db_count → result 成功形 + 重拉三态
    await act(async () => {
      resolveAcquire({ result: "ok", db_count: 20 });
    });
    await waitFor(() => expect(screen.getByTestId("weixin-keyacquire-result")).toBeTruthy());
    expect(screen.getByTestId("weixin-keyacquire-result").textContent).toContain("密钥就绪,20 个数据库已可解密");
    await waitFor(() =>
      expect(invokeCalls.filter(([cmd]) => cmd === "wechat_key_status").length).toBeGreaterThan(statusCallsBefore),
    );
  });

  it("取消触发 cancel 并收 cancelled 事件:正在取消… → 事件收敛回 idle(回包后到被吞)", async () => {
    const resolveAcquire = mockInvokeWithAcquire({
      state: "missing",
      db_count: 0,
      acquired_at: null,
      verdict_note: null,
    });
    render(<WeixinAccountCard />);
    await waitFor(() => expect(screen.getByTestId("weixin-keystatus-badge").textContent).toBe("未获取"));
    fireEvent.click(screen.getByTestId("weixin-keystatus-refresh"));
    fireEvent.click(screen.getByTestId("weixin-keyacquire-start"));
    await waitFor(() => expect(screen.getByTestId("weixin-keyacquire-running")).toBeTruthy());

    // 取消:调命令 + 按钮翻「正在取消…」禁用
    fireEvent.click(screen.getByTestId("weixin-keyacquire-cancel"));
    await waitFor(() => expect(invokeCalls).toContainEqual(["wechat_key_acquire_cancel", {}]));
    const cancelButton = screen.getByTestId("weixin-keyacquire-cancel") as HTMLButtonElement;
    expect(cancelButton.textContent).toBe("正在取消…");
    expect(cancelButton.disabled).toBe(true);

    // cancelled 事件收敛:回 idle,状态行按钮复出
    await act(async () => {
      dispatchKeyEvent?.({ seq: 1, phase: "cancelled", detail: "已取消" });
    });
    await waitFor(() => expect(screen.queryByTestId("weixin-keyacquire-running")).toBeNull());
    expect(screen.getByTestId("weixin-keystatus-refresh").textContent).toBe("获取密钥");

    // 回包后到:settled 守卫吞掉,不二次转换(不落结果页)
    await act(async () => {
      resolveAcquire({ result: "cancelled" });
    });
    expect(screen.queryByTestId("weixin-keyacquire-result")).toBeNull();
  });

  it("ready 态重新获取带确认文案:覆盖语义行 + 开始 force:true", async () => {
    mockInvokeWithAcquire({ state: "ready", db_count: 20 });
    render(<WeixinAccountCard />);
    await waitFor(() => expect(screen.getByTestId("weixin-keystatus-refresh").textContent).toBe("重新获取"));
    fireEvent.click(screen.getByTestId("weixin-keystatus-refresh"));
    expect(screen.getByTestId("weixin-keyacquire-confirm").textContent).toContain("当前密钥将在新密钥验证通过后覆盖");
    fireEvent.click(screen.getByTestId("weixin-keyacquire-start"));
    // ready 场景必须 force(缓存短路会让重取永远空转,grill 决议②)
    expect(invokeCalls).toContainEqual(["wechat_key_acquire", { force: true }]);
  });

  it("未配取钥器按钮置灰:disabled + title/引导「先配置取钥器」", async () => {
    mockInvoke(
      {},
      { configured: false, path: null, file_exists: false, file_executable: false },
      { state: "missing", db_count: 0, acquired_at: null, verdict_note: null },
    );
    render(<WeixinAccountCard />);
    await waitFor(() => expect(screen.getByTestId("weixin-keystatus-badge").textContent).toBe("未获取"));
    const refresh = screen.getByTestId("weixin-keystatus-refresh") as HTMLButtonElement;
    expect(refresh.disabled).toBe(true);
    expect(refresh.title).toBe("先配置取钥器");
    expect(screen.getByText(/先配置取钥器/)).toBeTruthy();
  });

  it("失败形:错误人话上屏 + 重试回 confirm(补 §D.2 失败形覆盖)", async () => {
    const resolveAcquire = mockInvokeWithAcquire({
      state: "stale",
      db_count: 20,
      verdict_note: "抽样验真失败:1/3",
    });
    render(<WeixinAccountCard />);
    await waitFor(() => expect(screen.getByTestId("weixin-keystatus-badge").textContent).toBe("已失效"));
    fireEvent.click(screen.getByTestId("weixin-keystatus-refresh"));
    fireEvent.click(screen.getByTestId("weixin-keyacquire-start"));
    await waitFor(() => expect(screen.getByTestId("weixin-keyacquire-running")).toBeTruthy());
    await act(async () => {
      resolveAcquire({ result: "failed", error: "取钥失败:未在超时时间内检测到重新登录" });
    });
    await waitFor(() => expect(screen.getByTestId("weixin-keyacquire-result")).toBeTruthy());
    const result = screen.getByTestId("weixin-keyacquire-result");
    expect(result.textContent).toContain("取钥失败:未在超时时间内检测到重新登录");
    fireEvent.click(screen.getByTestId("weixin-keyacquire-retry"));
    // 重试回 confirm(覆盖语义沿用:stale 入口无该行)
    await waitFor(() => expect(screen.getByTestId("weixin-keyacquire-confirm")).toBeTruthy());
    expect(screen.queryByTestId("weixin-keyacquire-result")).toBeNull();
  });

  it("跨轮事件水位:上一轮迟到的低 seq 终态事件不污染新一轮(startAcquire 不清零 lastSeqRef)", async () => {
    const resolveAcquire = mockInvokeWithAcquire({
      state: "missing",
      db_count: 0,
      acquired_at: null,
      verdict_note: null,
    });
    render(<WeixinAccountCard />);
    await waitFor(() => expect(screen.getByTestId("weixin-keystatus-badge").textContent).toBe("未获取"));
    // 第一轮:见 seq=5 progress,回包收 failed(结果页)
    fireEvent.click(screen.getByTestId("weixin-keystatus-refresh"));
    fireEvent.click(screen.getByTestId("weixin-keyacquire-start"));
    await waitFor(() => expect(screen.getByTestId("weixin-keyacquire-running")).toBeTruthy());
    await act(async () => {
      dispatchKeyEvent?.({ seq: 5, phase: "password", detail: "第一轮进度" });
    });
    await act(async () => {
      resolveAcquire({ result: "failed", error: "第一轮失败" });
    });
    await waitFor(() => expect(screen.getByTestId("weixin-keyacquire-result")).toBeTruthy());

    // 第二轮:重试 → 开始(settle 重新武装;lastSeqRef 跨 run 保留最大值)
    fireEvent.click(screen.getByTestId("weixin-keyacquire-retry"));
    await waitFor(() => expect(screen.getByTestId("weixin-keyacquire-confirm")).toBeTruthy());
    fireEvent.click(screen.getByTestId("weixin-keyacquire-start"));
    await waitFor(() => expect(screen.getByTestId("weixin-keyacquire-running")).toBeTruthy());

    // 上一轮迟到的终态事件(seq=4 ≤ 已见水位 5)被挡:不收敛、不落结果页
    await act(async () => {
      dispatchKeyEvent?.({ seq: 4, phase: "failed", detail: "上一轮迟到的失败" });
    });
    expect(screen.getByTestId("weixin-keyacquire-running")).toBeTruthy();
    expect(screen.queryByTestId("weixin-keyacquire-result")).toBeNull();

    // 新一轮真事件(seq=6 > 水位)正常生效
    await act(async () => {
      dispatchKeyEvent?.({ seq: 6, phase: "password", detail: "第二轮进度" });
    });
    expect(screen.getByText("第二轮进度")).toBeTruthy();
  });
});

describe("微信账号卡:取钥器一键安装(E2;D3 装机后首用引导)", () => {
  const UNSET: Partial<KeyProviderState> = {
    configured: false,
    path: null,
    file_exists: false,
    file_executable: false,
  };
  const BUNDLE_FILES = [
    "keyprovider-lldb.sh",
    "keyprovider_wrap.py",
    "keyprovider_root.sh",
    "wcdb_key_tool_macos.py",
  ];

  /** 未配置态 + 安装面可编程 mock(inspect/install 形状可控;provider set 落盘回读)。 */
  function mockInvokeWithInstall(
    inspect: Record<string, unknown>,
    install?: Record<string, unknown> | Error,
  ) {
    let provider = providerPayload(UNSET);
    mocks.invoke.mockImplementation(async (cmd: string, args?: Record<string, unknown>) => {
      invokeCalls.push([cmd, args ?? {}]);
      if (cmd === "sidecar_request") return statusPayload({});
      if (cmd === "wechat_key_provider") {
        const action = (args as { action?: string } | undefined)?.action;
        if (action === "get") return provider;
        if (action === "set") {
          provider = providerPayload({ path: (args as { path?: string }).path ?? null });
          return { ok: true };
        }
      }
      if (cmd === "wechat_key_status") {
        return keyStatusPayload({ state: "missing", db_count: 0, acquired_at: null, verdict_note: null });
      }
      if (cmd === "wechat_key_acquire") return new Promise(() => {});
      if (cmd === "wechat_key_acquire_cancel") return { ok: true };
      if (cmd === "wechat_key_provider_install") {
        const action = (args as { action?: string } | undefined)?.action;
        if (action === "inspect") return inspect;
        if (action === "install") {
          if (install instanceof Error) throw JSON.stringify({ code: "install_source_missing", path: "$", message: install.message });
          return install;
        }
      }
      throw new Error(`测试未预期的 invoke:${cmd} ${JSON.stringify(args)}`);
    });
  }

  it("源不在:引导文案(束暂存目录指引)在场,无安装按钮", async () => {
    mockInvokeWithInstall({
      available: false,
      source_dir: null,
      installed: false,
      installed_path: null,
      files: [],
    });
    render(<WeixinAccountCard />);
    await waitFor(() => expect(screen.getByTestId("weixin-keyprovider-install-guidance")).toBeTruthy());
    const guidance = screen.getByTestId("weixin-keyprovider-install-guidance");
    expect(guidance.textContent).toContain("未检测到可安装的取钥器部署件");
    expect(guidance.textContent).toContain("keyprovider-lldb.sh");
    expect(guidance.textContent).toContain("/tmp/wxkey-deploy");
    expect(screen.queryByTestId("weixin-keyprovider-install-button")).toBeNull();
  });

  it("源在场但属主校验未过:unsafe 拒因警示在场,无安装按钮(评审修③)", async () => {
    mockInvokeWithInstall({
      available: false,
      source_unsafe_reason: "目录 /tmp/wxkey-deploy 属主 uid=4242 非当前用户(uid=501)亦非可信 root 形态",
      source_dir: null,
      installed: false,
      installed_path: null,
      files: [],
    });
    render(<WeixinAccountCard />);
    const unsafe = await screen.findByTestId("weixin-keyprovider-install-unsafe");
    expect(unsafe.textContent).toContain("属主校验未通过,已拒绝一键安装");
    expect(unsafe.textContent).toContain("uid=4242");
    expect(unsafe.textContent).toContain("由本人重新放置");
    // 互斥形态:无安装按钮;标准引导仍在(unsafe 是叠加披露,不替换指引)
    expect(screen.queryByTestId("weixin-keyprovider-install-button")).toBeNull();
    expect(screen.getByTestId("weixin-keyprovider-install-guidance")).toBeTruthy();
  });

  it("源在场未装:一键安装 → invoke install + set(落点路径)→ 回执含路径 + 配置态翻已配置", async () => {
    const installedPath = "/data-root/wechat-localdb/bin/keyprovider-lldb.sh";
    mockInvokeWithInstall(
      { available: true, source_dir: "/tmp/wxkey-deploy", installed: false, installed_path: null, files: BUNDLE_FILES },
      { ok: true, installed_path: installedPath, copied: BUNDLE_FILES },
    );
    render(<WeixinAccountCard />);
    const button = await screen.findByTestId("weixin-keyprovider-install-button");
    expect(button.textContent).toBe("一键安装取钥器");
    // 源不在引导是互斥形态
    expect(screen.queryByTestId("weixin-keyprovider-install-guidance")).toBeNull();
    fireEvent.click(button);
    await waitFor(() => expect(screen.getByTestId("weixin-keyprovider-install-note")).toBeTruthy());
    expect(screen.getByTestId("weixin-keyprovider-install-note").textContent).toContain(installedPath);
    expect(invokeCalls).toContainEqual(["wechat_key_provider_install", { action: "install" }]);
    expect(invokeCalls).toContainEqual(["wechat_key_provider", { action: "set", path: installedPath }]);
    // mock set 落盘回读:安装+配置后翻「已配置」(安装行随未配置门退场)
    await waitFor(() => expect(screen.getByTestId("weixin-keyprovider-badge").textContent).toBe("已配置"));
    expect(screen.queryByTestId("weixin-keyprovider-install-button")).toBeNull();
  });

  it("安装失败:错误人话上屏 + 无成功回执 + 按钮可重试", async () => {
    mockInvokeWithInstall(
      { available: true, source_dir: "/tmp/wxkey-deploy", installed: false, installed_path: null, files: BUNDLE_FILES },
      new Error("未检测到可安装的取钥器部署件(束暂存目录缺入口文件)"),
    );
    render(<WeixinAccountCard />);
    fireEvent.click(await screen.findByTestId("weixin-keyprovider-install-button"));
    await waitFor(() =>
      expect(screen.getByTestId("weixin-keyprovider").textContent).toContain("束暂存目录缺入口文件"),
    );
    expect(screen.queryByTestId("weixin-keyprovider-install-note")).toBeNull();
    // 失败后按钮仍在场可重试
    expect((screen.getByTestId("weixin-keyprovider-install-button") as HTMLButtonElement).disabled).toBe(false);
  });
});
