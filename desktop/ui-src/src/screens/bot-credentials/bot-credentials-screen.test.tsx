// @vitest-environment jsdom
//
// 「机器人凭据」屏测试(10-11-bot-credentials-screen;自 settings.test 推送块
// 随屏搬迁+发送测试新用例):mock sidecar(secret.set 内存态 + push.test 可
// 编程)。覆盖:预设位逐字段入钥匙链 / 空字段跳过+全空 note / 自定义凭据位 /
// scope 非法拦截 / bark、apprise 通道提示 / 发送测试(push.test 真发)。
import { cleanup, fireEvent, render, screen, within } from "@testing-library/react";
import { MemoryRouter } from "react-router-dom";
import { afterAll, afterEach, beforeAll, beforeEach, describe, expect, it, vi } from "vitest";

const mocks = vi.hoisted(() => ({ invoke: vi.fn() }));
vi.mock("@tauri-apps/api/core", () => ({ invoke: mocks.invoke }));

import { BotCredentialsScreen } from "./bot-credentials-screen";

type SecretCalls = { name: string; value: string }[];

function installSidecar(options: {
  secrets?: Map<string, string>;
  pushTest?: (params: { channel: string; target?: string }) => unknown;
  calls?: SecretCalls;
} = {}): { secrets: Map<string, string> } {
  const secrets = options.secrets ?? new Map<string, string>();
  const calls = options.calls ?? [];
  mocks.invoke.mockImplementation(async (_command: string, args: { method: string; params?: unknown }) => {
    if (args.method === "secret.set") {
      const { name, value } = args.params as { name: string; value: string };
      calls.push({ name, value });
      secrets.set(name, value);
      return { name, stored: true };
    }
    if (args.method === "push.test") {
      return options.pushTest
        ? options.pushTest(args.params as { channel: string; target?: string })
        : { ok: true, channel: (args.params as { channel: string }).channel };
    }
    throw JSON.stringify({ code: "method_not_found", path: "method", message: `未知方法 ${args.method}` });
  });
  return { secrets };
}

function callsOf(method: string): SecretCalls {
  return mocks.invoke.mock.calls
    .filter(([c]) => c === "sidecar_request")
    .map(([, args]) => args as unknown as { method: string; params: unknown })
    .filter((args) => args.method === method)
    .map((args) => args.params as { name: string; value: string });
}

async function typeByLabel(label: string, value: string): Promise<void> {
  const input = await screen.findByLabelText(label);
  fireEvent.change(input, { target: { value } });
}

beforeEach(() => {
  mocks.invoke.mockReset();
  vi.spyOn(window, "confirm").mockReturnValue(true);
});
// Radix Select 在 jsdom 打开下拉需指针捕获 + 选中项滚入桩(settings.test 同款;
// 退出还原防外溢到同 worker 其他测试文件)
beforeAll(() => {
  window.HTMLElement.prototype.hasPointerCapture = () => false;
  window.HTMLElement.prototype.releasePointerCapture = () => {};
  Element.prototype.scrollIntoView = () => {};
});
afterAll(() => {
  delete (window.HTMLElement.prototype as Partial<HTMLElement>).hasPointerCapture;
  delete (window.HTMLElement.prototype as Partial<HTMLElement>).releasePointerCapture;
  delete (Element.prototype as Partial<Element>).scrollIntoView;
});
afterEach(() => {
  cleanup();
  vi.restoreAllMocks();
});

describe("机器人凭据:预设位", () => {
  it("feishu 三字段逐条写 myia/push/<ENV_KEY>;保存即清值零回显", async () => {
    const state = installSidecar();
    render(<MemoryRouter><BotCredentialsScreen /></MemoryRouter>);
    await typeByLabel("feishu_card App ID", "cli_test_app");
    await typeByLabel("feishu_card App Secret", "sec_private_value");
    await typeByLabel("feishu_card 群 chat_id", "oc_room123");
    fireEvent.click(screen.getByRole("button", { name: "保存推送凭据" }));

    await screen.findByTestId("save-status");
    expect(callsOf("secret.set")).toContainEqual({ name: "myia/push/FEISHU_APP_ID", value: "cli_test_app" });
    expect(callsOf("secret.set")).toContainEqual({ name: "myia/push/FEISHU_APP_SECRET", value: "sec_private_value" });
    expect(callsOf("secret.set")).toContainEqual({ name: "myia/push/FEISHU_CHAT_ID", value: "oc_room123" });
    expect(document.body.textContent).not.toContain("sec_private_value");
    expect((screen.getByLabelText("feishu_card App Secret") as HTMLInputElement).value).toBe("");
    expect(state.secrets.get("myia/push/FEISHU_APP_SECRET")).toBe("sec_private_value");
  });

  it("空字段跳过;全空 → note 拦截零协议调用", async () => {
    installSidecar();
    render(<MemoryRouter><BotCredentialsScreen /></MemoryRouter>);
    await typeByLabel("feishu_card App Secret", "only_secret");
    fireEvent.click(screen.getByRole("button", { name: "保存推送凭据" }));
    await screen.findByTestId("save-status");
    expect(callsOf("secret.set")).toEqual([{ name: "myia/push/FEISHU_APP_SECRET", value: "only_secret" }]);

    fireEvent.click(screen.getByRole("button", { name: "保存推送凭据" }));
    expect(await screen.findByText(/至少填一个字段/)).toBeTruthy();
    expect(callsOf("secret.set")).toHaveLength(1);
  });
});

describe("机器人凭据:自定义凭据位", () => {
  it("按 scope+名字写 myia/<scope>/<name>", async () => {
    const state = installSidecar();
    render(<MemoryRouter><BotCredentialsScreen /></MemoryRouter>);
    await typeByLabel("品类 scope", "stocks");
    await typeByLabel("推送凭据名", "chat_id");
    await typeByLabel("推送凭据值", "oc_abc123private");
    fireEvent.click(screen.getByRole("button", { name: "保存自定义凭据位" }));

    await screen.findByTestId("save-status");
    expect(callsOf("secret.set")).toContainEqual({ name: "myia/stocks/chat_id", value: "oc_abc123private" });
    expect(document.body.textContent).not.toContain("oc_abc123private");
    expect(state.secrets.get("myia/stocks/chat_id")).toBe("oc_abc123private");
  });

  it("scope 非法 → 前端校验拦截,零协议调用", async () => {
    installSidecar();
    render(<MemoryRouter><BotCredentialsScreen /></MemoryRouter>);
    await typeByLabel("品类 scope", "Stocks!");
    await typeByLabel("推送凭据值", "whatever");
    fireEvent.click(screen.getByRole("button", { name: "保存自定义凭据位" }));

    expect(await screen.findByText(/scope 须为品类 id 规则/)).toBeTruthy();
    expect(callsOf("secret.set")).toEqual([]);
  });
});

describe("机器人凭据:通道下拉与提示", () => {
  it("bark(iOS 推送):下拉可选;device key 入钥匙链 + 两处提示文案在位", async () => {
    const state = installSidecar();
    render(<MemoryRouter><BotCredentialsScreen /></MemoryRouter>);
    await screen.findByRole("combobox", { name: "推送通道" });

    // Radix Select(mouse 型 pointerDown 才开下拉,惯例同 feed 屏)
    fireEvent.pointerDown(screen.getByRole("combobox", { name: "推送通道" }), { button: 0, pointerType: "mouse" });
    fireEvent.click(await screen.findByRole("option", { name: "Bark(iOS 推送)" }));

    expect(screen.getByText(/在 iPhone 的 Bark App 里复制/)).toBeTruthy();
    await typeByLabel("bark Device Key", "devkey_from_app");
    fireEvent.click(screen.getByRole("button", { name: "保存推送凭据" }));
    await screen.findByTestId("save-status");
    expect(callsOf("secret.set")).toContainEqual({ name: "myia/push/BARK_DEVICE_KEY", value: "devkey_from_app" });
    expect(state.secrets.get("myia/push/BARK_DEVICE_KEY")).toBe("devkey_from_app");

    const endpointHint = screen.getByTestId("bark-endpoint-hint").textContent ?? "";
    expect(endpointHint).toContain("留空 = 官方服务");
    expect(endpointHint).toContain("自建");
  });

  it("apprise(统一推送):目标串入钥匙链 + 目标引用提示在位", async () => {
    const state = installSidecar();
    render(<MemoryRouter><BotCredentialsScreen /></MemoryRouter>);

    fireEvent.pointerDown(screen.getByRole("combobox", { name: "推送通道" }), { button: 0, pointerType: "mouse" });
    fireEvent.click(await screen.findByRole("option", { name: "Apprise(统一推送)" }));

    const targetHint = screen.getByTestId("apprise-target-hint").textContent ?? "";
    expect(targetHint).toContain("env:/keychain: 引用");
    expect(targetHint).toContain("bark://");
    expect(targetHint).toContain("逗号");

    await typeByLabel("apprise Apprise 推送目标", "json://sink/a,bark://key/DEFAULT");
    fireEvent.click(screen.getByRole("button", { name: "保存推送凭据" }));
    await screen.findByTestId("save-status");
    expect(callsOf("secret.set")).toContainEqual({
      name: "myia/push/APPRISE_URL",
      value: "json://sink/a,bark://key/DEFAULT",
    });
    expect(state.secrets.get("myia/push/APPRISE_URL")).toBe("json://sink/a,bark://key/DEFAULT");
  });
});

describe("机器人凭据:发送测试", () => {
  it("push.test 真发:target=预设凭据位键,成功回显通道连通", async () => {
    const seen: Array<{ channel: string; target?: string }> = [];
    installSidecar({
      pushTest: (params) => {
        seen.push(params);
        return { ok: true, channel: params.channel };
      },
    });
    render(<MemoryRouter><BotCredentialsScreen /></MemoryRouter>);
    await typeByLabel("feishu_card 群 chat_id", "oc_room123");
    fireEvent.click(screen.getByRole("button", { name: "发送测试" }));

    const note = await screen.findByTestId("push-test-result");
    expect(note.textContent).toContain("测试消息已发");
    expect(seen[0]).toEqual({ channel: "feishu_card", target: "keychain:myia/push/FEISHU_CHAT_ID" });
    expect(screen.getByText("通道连通")).toBeTruthy();
  });

  it("发送失败:结构化错误置灰徽标 + alert", async () => {
    installSidecar({
      pushTest: () => {
        throw JSON.stringify({ code: "env_var_missing", path: "$", message: "通道凭据缺失" });
      },
    });
    render(<MemoryRouter><BotCredentialsScreen /></MemoryRouter>);
    fireEvent.click(screen.getByRole("button", { name: "发送测试" }));
    const note = await screen.findByTestId("push-test-result");
    expect(note.textContent).toContain("发送失败(env_var_missing)");
    expect(screen.getByText("通道失败")).toBeTruthy();
  });
});

// ---------------------------------------------------------------------------
// 推送最后一公里(push-last-mile):B 派逐键引用清单 + 保存成功反馈 A/B 分流
// ---------------------------------------------------------------------------

describe("机器人凭据:B 派 keychain 引用清单(push-last-mile)", () => {
  it("wecom 4 键 / email 6 键:逐键一行「label → keychain:myia/push/<键>」+ 复制钮", async () => {
    installSidecar();
    render(<MemoryRouter><BotCredentialsScreen /></MemoryRouter>);
    fireEvent.pointerDown(screen.getByRole("combobox", { name: "推送通道" }), { button: 0, pointerType: "mouse" });
    fireEvent.click(await screen.findByRole("option", { name: "企业微信" }));

    const wecomList = screen.getByTestId("keychain-ref-list");
    expect(within(wecomList).getAllByTestId(/^keychain-ref-row-/)).toHaveLength(4);
    const corpidRow = within(wecomList).getByTestId("keychain-ref-row-WECOM_CORPID");
    expect(corpidRow.textContent).toContain("企业 ID(corpid)");
    expect(corpidRow.textContent).toContain("keychain:myia/push/WECOM_CORPID");
    expect(within(corpidRow).getByTestId("keychain-ref-copy-WECOM_CORPID")).toBeTruthy();
    expect(within(wecomList).getByTestId("keychain-ref-row-WECOM_TUSER")).toBeTruthy();

    // 切 email:6 键清单随之切换
    fireEvent.pointerDown(screen.getByRole("combobox", { name: "推送通道" }), { button: 0, pointerType: "mouse" });
    fireEvent.click(await screen.findByRole("option", { name: "Email(SMTP)" }));
    const emailList = screen.getByTestId("keychain-ref-list");
    expect(within(emailList).getAllByTestId(/^keychain-ref-row-/)).toHaveLength(6);
    expect(within(emailList).getByTestId("keychain-ref-row-EMAIL_TO")).toBeTruthy();
  });

  it("A 派通道(feishu)不渲染引用清单", async () => {
    installSidecar();
    render(<MemoryRouter><BotCredentialsScreen /></MemoryRouter>);
    await screen.findByRole("combobox", { name: "推送通道" });
    expect(screen.queryByTestId("keychain-ref-list")).toBeNull();
  });

  it("复制钮:写入剪贴板(navigator.clipboard.writeText;jsdom 缺席注入 stub,测后还原)", async () => {
    const writeText = vi.fn().mockResolvedValue(undefined);
    Object.defineProperty(navigator, "clipboard", { value: { writeText }, configurable: true });
    installSidecar();
    render(<MemoryRouter><BotCredentialsScreen /></MemoryRouter>);
    fireEvent.pointerDown(screen.getByRole("combobox", { name: "推送通道" }), { button: 0, pointerType: "mouse" });
    fireEvent.click(await screen.findByRole("option", { name: "企业微信" }));
    fireEvent.click(screen.getByTestId("keychain-ref-copy-WECOM_CORPSECRET"));
    expect(writeText).toHaveBeenCalledWith("keychain:myia/push/WECOM_CORPSECRET");
    Reflect.deleteProperty(navigator, "clipboard");
  });
});

describe("机器人凭据:保存成功反馈 A/B 分流(push-last-mile)", () => {
  it("A 派(feishu):note 原文 + 下一步锚点 #/messaging(飞书先刷新 / Telegram 先发条消息)", async () => {
    installSidecar();
    render(<MemoryRouter><BotCredentialsScreen /></MemoryRouter>);
    await typeByLabel("feishu_card App ID", "cli_test_app");
    fireEvent.click(screen.getByRole("button", { name: "保存推送凭据" }));

    const status = await screen.findByTestId("save-status");
    expect(status.textContent).toContain("运行时 env 缺失会自动用这些值");
    expect(status.textContent).not.toContain("真实推送要品类 YAML 写");
    const nextStep = within(status).getByTestId("save-next-step");
    expect(nextStep.textContent).toContain("勾推送对象");
    expect(nextStep.textContent).toContain("飞书先点刷新");
    expect(nextStep.textContent).toContain("Telegram 先给机器人发条消息");
    const anchor = within(nextStep).getByRole("link", { name: "消息屏" });
    expect(anchor.getAttribute("href")).toBe("#/messaging");
    expect(within(nextStep).queryByRole("link", { name: "YAML配置" })).toBeNull();
  });

  it("B 派(wecom):note 指向引用清单 + 下一步双锚点 #/yaml-editor 与 #/messaging", async () => {
    installSidecar();
    render(<MemoryRouter><BotCredentialsScreen /></MemoryRouter>);
    fireEvent.pointerDown(screen.getByRole("combobox", { name: "推送通道" }), { button: 0, pointerType: "mouse" });
    fireEvent.click(await screen.findByRole("option", { name: "企业微信" }));
    await typeByLabel("wecom 企业 ID(corpid)", "ww_demo_corp");
    fireEvent.click(screen.getByRole("button", { name: "保存推送凭据" }));

    const status = await screen.findByTestId("save-status");
    expect(callsOf("secret.set")).toContainEqual({ name: "myia/push/WECOM_CORPID", value: "ww_demo_corp" });
    expect(status.textContent).toContain("真实推送要品类 YAML 写 keychain:myia/push/<键> 引用");
    expect(status.textContent).toContain("可先点「发送测试」验连通");
    const nextStep = within(status).getByTestId("save-next-step");
    expect(nextStep.textContent).toContain("贴 keychain: 引用");
    expect(nextStep.textContent).toContain("勾对象");
    const yamlAnchor = within(nextStep).getByRole("link", { name: "YAML配置" });
    expect(yamlAnchor.getAttribute("href")).toBe("#/yaml-editor");
    const msgAnchor = within(nextStep).getByRole("link", { name: "消息屏" });
    expect(msgAnchor.getAttribute("href")).toBe("#/messaging");
  });
});
