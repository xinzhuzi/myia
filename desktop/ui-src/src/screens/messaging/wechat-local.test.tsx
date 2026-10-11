// @vitest-environment jsdom
//
// 「微信本机」工作区组件测试(task 10-11-wechat-ui-bridge F3/F4):
// AX 权限引导卡常驻(授权主体 = MYIA app 本体)/ 探针三态胶囊(ok 可用绿 /
// degraded 降级黄带原因逐条 / 不可用灰)/ sidecar 未接线降级说明(method_
// not_found,alerts unsupported 判例同款)/ 只读会话入口(G2 选会话 → 拉最近
// 消息展示;G3 读回不入情报管线)/ 本地库查询行(E 段三域,key_unavailable
// 结构化直显)。桥命令族全走 mock sidecar,零真跑。
import { cleanup, fireEvent, render, screen, waitFor, within } from "@testing-library/react";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";

const mocks = vi.hoisted(() => ({ invoke: vi.fn() }));
vi.mock("@tauri-apps/api/core", () => ({ invoke: mocks.invoke }));

import { WechatLocalSection } from "./wechat-local";
import { SidecarRequestError } from "@/lib/api";
import type { WechatLocalProbeView } from "./api";

type Handler = (params: never) => unknown;
type SidecarMap = Record<string, Handler>;

function probeFixture(overrides: Partial<WechatLocalProbeView> = {}): WechatLocalProbeView {
  return {
    ok: true,
    state: "ok",
    checks: { bridge_component: "ok", wechat_process: "ok", ax_permission: "ok" },
    wechat_version: "4.1.15",
    bridge_version: "0.2.0",
    reasons: [],
    ...overrides,
  };
}

function installSidecar(map: SidecarMap): void {
  mocks.invoke.mockImplementation(
    async (_command: string, args: { method: string; params?: unknown }) => {
      const handler = map[args.method];
      if (!handler) {
        throw JSON.stringify({
          code: "method_not_found",
          path: "method",
          message: `未知方法 ${args.method}`,
          data: { allowed: Object.keys(map).sort() },
        });
      }
      return handler(args.params as never);
    },
  );
}

/** 结构化 SidecarRequestError 直构(错误路径不用 mock,直传组件)。 */
function sidecarError(code: string, message: string, fixHint?: string): SidecarRequestError {
  return new SidecarRequestError({
    code,
    path: "$",
    message,
    data: fixHint ? { fix_hint: fixHint } : undefined,
  });
}

function renderSection(props: Partial<Parameters<typeof WechatLocalSection>[0]> = {}) {
  return render(
    <WechatLocalSection
      probe={props.probe ?? null}
      probeError={props.probeError ?? null}
      refreshing={props.refreshing ?? false}
      onRefresh={props.onRefresh ?? (() => {})}
    />,
  );
}

beforeEach(() => {
  mocks.invoke.mockReset();
  installSidecar({});
});

afterEach(() => {
  cleanup();
});

// ---------------------------------------------------------------------------
// F3:状态头 + AX 权限引导卡
// ---------------------------------------------------------------------------

describe("微信本机:状态头与 AX 引导卡", () => {
  it("AX 权限引导卡常驻渲染(探针缺位也在);步骤含授权路径与静默铁律", () => {
    renderSection();
    const guide = screen.getByTestId("wechat-local-ax-guide");
    expect(guide.textContent).toContain("辅助功能");
    expect(guide.textContent).toContain("隐私与安全性");
    expect(guide.textContent).toContain("MYIA");
    expect(guide.textContent).toContain("不激活微信窗口");
  });

  it("探针 ok:胶囊「可用」;版本行携带微信/桥组件版本;无降级原因列表", () => {
    renderSection({ probe: probeFixture() });
    expect(screen.getByTestId("wechat-local-state-pill").textContent).toBe("可用");
    const summary = screen.getByTestId("wechat-local-probe-summary");
    expect(summary.textContent).toContain("4.1.15");
    expect(summary.textContent).toContain("0.2.0");
    expect(screen.queryByTestId("wechat-local-reasons")).toBeNull();
  });

  it("探针 degraded:胶囊「降级」+ 原因逐条(码名 + 修复指引)", () => {
    renderSection({
      probe: probeFixture({
        ok: false,
        state: "degraded",
        checks: { wechat_process: "ok", main_window: "fail", ax_permission: "ok" },
        reasons: [{ code: "window_closed", fix_hint: "打开微信主窗口" }],
      }),
    });
    expect(screen.getByTestId("wechat-local-state-pill").textContent).toBe("降级");
    const reasons = screen.getByTestId("wechat-local-reasons");
    expect(reasons.textContent).toContain("window_closed");
    expect(reasons.textContent).toContain("打开微信主窗口");
  });

  it("探针 bridge_unavailable:胶囊「不可用」;探针缺位(null)同灰态", () => {
    const { rerender } = renderSection({
      probe: probeFixture({ ok: false, state: "bridge_unavailable", reasons: [{ code: "component_missing", fix_hint: "装组件" }] }),
    });
    expect(screen.getByTestId("wechat-local-state-pill").textContent).toBe("不可用");
    rerender(
      <WechatLocalSection probe={null} probeError={null} refreshing={false} onRefresh={() => {}} />,
    );
    expect(screen.getByTestId("wechat-local-state-pill").textContent).toBe("不可用");
  });

  it("探针 checks.ax_permission=fail:引导卡 warning 强调 + 未授权徽标", () => {
    renderSection({
      probe: probeFixture({
        ok: false,
        state: "bridge_unavailable",
        checks: { ax_permission: "fail" },
        reasons: [{ code: "ax_permission_denied", fix_hint: "系统设置授权" }],
      }),
    });
    const guide = screen.getByTestId("wechat-local-ax-guide");
    expect(guide.className).toContain("border-warning/40");
    expect(within(guide).getByText("未授权").className).toContain("border-destructive");
  });

  it("sidecar 未接线(method_not_found):降级说明 + 其余面板不挡", () => {
    renderSection({ probeError: sidecarError("method_not_found", "未知方法 wechat_local.probe") });
    expect(screen.getByTestId("wechat-local-unsupported").textContent).toContain("wechat_local.*");
    expect(screen.getByTestId("wechat-local-state-pill").textContent).toContain("sidecar 未接线");
  });

  it("探针传输层错误(非 method_not_found):结构化错误直显", () => {
    renderSection({ probeError: sidecarError("sidecar_unavailable", "Tauri IPC 不可用") });
    const box = screen.getByTestId("wechat-local-probe-error");
    expect(box.textContent).toContain("sidecar_unavailable");
  });

  it("刷新状态按钮触发 onRefresh", () => {
    const onRefresh = vi.fn();
    renderSection({ onRefresh });
    fireEvent.click(screen.getByTestId("wechat-local-refresh"));
    expect(onRefresh).toHaveBeenCalledTimes(1);
  });
});

// ---------------------------------------------------------------------------
// F4:只读会话入口(G2/G3)
// ---------------------------------------------------------------------------

describe("微信本机:只读会话入口", () => {
  it("拉取会话列表 → 渲染(名称/未读/id);点会话 → 拉最近消息展示", async () => {
    const calls: Array<{ method: string; params: unknown }> = [];
    installSidecar({
      "wechat_local.sessions": (params: never) => {
        calls.push({ method: "wechat_local.sessions", params });
        return {
          sessions: [
            { id: "filehelper", name: "文件传输助手", unread: 0 },
            { id: "123@chatroom", name: "测试群", unread: 3 },
          ],
        };
      },
      "wechat_local.messages": (params: never) => {
        calls.push({ method: "wechat_local.messages", params });
        return {
          messages: [
            { ts: 1760000000, sender: "me", type: "text", text: "你好" },
            { ts: 1760000100, sender: "peer", type: "image", media_placeholder: "非文本消息,内容未导出(占位)" },
          ],
        };
      },
    });
    renderSection();

    fireEvent.click(screen.getByTestId("wechat-local-load-sessions"));
    const list = await screen.findByTestId("wechat-local-session-list");
    expect(within(list).getByText("文件传输助手")).toBeTruthy();
    expect(within(list).getByText("未读 3")).toBeTruthy();

    fireEvent.click(within(list).getByTestId("wechat-local-session-filehelper"));
    const messages = await screen.findByTestId("wechat-local-messages");
    expect(messages.textContent).toContain("你好");
    expect(messages.textContent).toContain("非文本消息,内容未导出(占位)");
    // G2 契约:messages 带会话 id;count 未传(桥用配置缺省 50)
    const messageCall = calls.find((call) => call.method === "wechat_local.messages");
    expect(messageCall?.params).toEqual({ chat_id: "filehelper" });
  });

  it("拉取失败:结构化错误直显(码名 + 修复指引),不重试不静默", async () => {
    installSidecar({
      "wechat_local.sessions": () => {
        throw JSON.stringify({
          code: "not_implemented",
          path: "$",
          message: "sessions list 的实现层尚未落地(Phase C1)",
          data: { fix_hint: "等待 Phase C1 落地;期间可用通道:probe/localdb" },
        });
      },
    });
    renderSection();

    fireEvent.click(screen.getByTestId("wechat-local-load-sessions"));
    const box = await screen.findByTestId("wechat-local-sessions-error");
    expect(box.textContent).toContain("not_implemented");
    expect(box.textContent).toContain("Phase C1");
    expect(box.textContent).toContain("等待 Phase C1 落地");
  });

  it("空会话列表:合法空态提示(确认窗口已开)", async () => {
    installSidecar({ "wechat_local.sessions": () => ({ sessions: [] }) });
    renderSection();
    fireEvent.click(screen.getByTestId("wechat-local-load-sessions"));
    await waitFor(() => expect(screen.getByTestId("wechat-local-readonly").textContent).toContain("会话列表为空"));
  });
});

// ---------------------------------------------------------------------------
// 本地库查询行(E 段产出消费面)
// ---------------------------------------------------------------------------

describe("微信本机:本地库查询", () => {
  it("填会话 id 查询 → 结果渲染(展示名/域徽标/消息);since_days 透传", async () => {
    const calls: Array<{ method: string; params: unknown }> = [];
    installSidecar({
      "wechat_local.query": (params: never) => {
        calls.push({ method: "wechat_local.query", params });
        return {
          chat_id: "filehelper",
          since_days: 7,
          messages: [{ ts: 1760000000, sender: "me", type: "text", text: "历史消息" }],
          display_name: "文件传输助手",
          sessions: [],
          domains: { message: "ok", session: "ok", contact: "ok" },
          copy: {},
        };
      },
    });
    renderSection();

    fireEvent.change(screen.getByLabelText("本地库会话 id"), { target: { value: "filehelper" } });
    fireEvent.change(screen.getByLabelText("历史天数"), { target: { value: "7" } });
    fireEvent.click(screen.getByTestId("wechat-local-db-run"));

    const result = await screen.findByTestId("wechat-local-db-result");
    expect(result.textContent).toContain("文件传输助手");
    expect(result.textContent).toContain("历史消息");
    expect(result.textContent).toContain("message:ok");
    expect(calls[0]?.params).toEqual({ chat_id: "filehelper", since_days: 7 });
  });

  it("密钥不可得(key_unavailable):结构化错误 + D4 修复指引直显", async () => {
    installSidecar({
      "wechat_local.query": () => {
        throw JSON.stringify({
          code: "key_unavailable",
          path: "$",
          message: "本地库密钥不可得:零内存途径实测未闭合",
          data: { fix_hint: "D4 待主人裁决:豁免内存搜索或引入外部密钥" },
        });
      },
    });
    renderSection();

    fireEvent.change(screen.getByLabelText("本地库会话 id"), { target: { value: "filehelper" } });
    fireEvent.click(screen.getByTestId("wechat-local-db-run"));

    const box = await screen.findByTestId("wechat-local-db-error");
    expect(box.textContent).toContain("key_unavailable");
    expect(box.textContent).toContain("D4 待主人裁决");
  });

  it("空会话 id:前端轻预检拒(不发协议调用)", async () => {
    const calls: Array<{ method: string }> = [];
    installSidecar({
      "wechat_local.query": (params: never) => {
        calls.push({ method: "wechat_local.query" });
        return {};
      },
    });
    renderSection();
    fireEvent.click(screen.getByTestId("wechat-local-db-run"));
    await waitFor(() => expect(screen.getByTestId("wechat-local-db-error").textContent).toContain("不能为空"));
    expect(calls).toHaveLength(0);
  });
});
