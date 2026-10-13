// @vitest-environment jsdom
//
// 「微信本机」工作区组件测试(task 10-11-wechat-ui-bridge F3/F4):
// AX 权限引导卡常驻(授权主体 = MYIA app 本体)/ 探针三态胶囊(ok 可用绿 /
// degraded 降级黄带原因逐条 / 不可用灰)/ sidecar 未接线降级说明(method_
// not_found,alerts unsupported 判例同款)/ 只读会话入口(G2 选会话 → 拉最近
// 消息展示;G3 读回不入情报管线)/ 本地库查询行(E 段三域,key_unavailable
// 结构化直显)。桥命令族全走 mock sidecar,零真跑。
//
// 六域接线批(0.8.0,10-14-wechat-chat-export R7)新增:分页浏览(首帧/
// 游标续拉/时间窗切换)与导出行(null 取消静默/回执路径/进度事件)。
import { cleanup, fireEvent, render, screen, waitFor, within } from "@testing-library/react";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";

const mocks = vi.hoisted(() => ({ invoke: vi.fn(), listen: vi.fn() }));
vi.mock("@tauri-apps/api/core", () => ({ invoke: mocks.invoke }));
vi.mock("@tauri-apps/api/event", () => ({ listen: mocks.listen }));

import { WechatLocalSection } from "./wechat-local";
import { SidecarRequestError } from "@/lib/api";
import type { WechatLocalProbeView } from "./api";

type Handler = (params: never) => unknown;
type SidecarMap = Record<string, Handler>;

function probeFixture(overrides: Partial<WechatLocalProbeView> = {}): WechatLocalProbeView {
  return {
    ok: true,
    state: "ok",
    checks: { bridge_component: "ok", wechat_process: "ok", screen_recording: "ok" },
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
  mocks.listen.mockReset();
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
    expect(guide.textContent).toContain("屏幕录制");
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
        checks: { wechat_process: "ok", main_window: "fail", screen_recording: "ok" },
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

  it("探针 checks.screen_recording=fail:引导卡 warning 强调 + 未授权徽标(2026-10-12 勘误换轨)", () => {
    renderSection({
      probe: probeFixture({
        ok: false,
        state: "bridge_unavailable",
        checks: { screen_recording: "fail" },
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
      "wechat_local.query": (_params: never) => {
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

// ---------------------------------------------------------------------------
// C1 分页浏览与导出行(10-14-wechat-chat-export R7;mock sidecar + mock 壳命令)
// ---------------------------------------------------------------------------

/** 分页应答夹具(desc 最新在前;两条消息 ts 新旧可辨)。 */
function pagePayload(overrides: Partial<{ next_cursor: string | null; has_more: boolean; messages: unknown[] }> = {}) {
  return {
    page: {
      chat_id: "filehelper",
      display_name: "文件传输助手",
      messages:
        overrides.messages ??
        [
          { seq: 2, ts: 1760000200, sender: "wxid_a", sender_id: "wxid_a", type: "text", local_type: 1, text: "较新的消息" },
          { seq: 1, ts: 1760000100, sender: "wxid_a", sender_id: "wxid_a", type: "text", local_type: 1, text: "较旧的消息" },
        ],
      next_cursor: overrides.next_cursor ?? null,
      has_more: overrides.has_more ?? false,
      filter: { from_ts: null, to_ts: null, types: [], sender: null, order: "desc" },
      page_size: 200,
    },
  };
}

describe("微信本机:分页浏览与导出(C1)", () => {
  it("拉取最新一页 → 倒转上屏(旧在上新在下);加载更早 = 游标续拉头部续接", async () => {
    const calls: Array<{ method: string; params: unknown }> = [];
    installSidecar({
      "wechat_local.page": (params: never) => {
        calls.push({ method: "wechat_local.page", params });
        const record = params as { cursor?: string };
        if (!record.cursor) return pagePayload({ next_cursor: "next-cursor-1", has_more: true });
        // 续拉页:更早的一条
        return pagePayload({
          next_cursor: null,
          has_more: false,
          messages: [
            { seq: 4, ts: 1759999200, sender: "wxid_a", sender_id: "wxid_a", type: "text", local_type: 1, text: "更早的消息" },
          ],
        });
      },
    });
    renderSection();

    fireEvent.change(screen.getByLabelText("本地库会话 id"), { target: { value: "filehelper" } });
    fireEvent.click(screen.getByTestId("wechat-local-page-run"));

    const result = await screen.findByTestId("wechat-local-page-messages");
    // 首帧倒转:旧在上新在下(聊天阅读序)
    const items = within(result).getAllByRole("listitem");
    expect(items[0].textContent).toContain("较旧的消息");
    expect(items[items.length - 1].textContent).toContain("较新的消息");
    // 缺省窗口 30 天 → from_ts 透传
    const first = calls[0]?.params as { from_ts?: number };
    expect(typeof first.from_ts).toBe("number");

    // 加载更早:游标续拉,新批 prepend 在头部
    fireEvent.click(screen.getByTestId("wechat-local-page-more"));
    await waitFor(() => {
      const merged = screen.getByTestId("wechat-local-page-messages");
      const mergedItems = within(merged).getAllByRole("listitem");
      expect(mergedItems[0].textContent).toContain("更早的消息");
      expect(mergedItems).toHaveLength(3);
    });
    const second = calls[1]?.params as { cursor?: string };
    expect(second.cursor).toBe("next-cursor-1");
  });

  it("时间窗切换:全部 → from_ts 不传;7 天 → 按天换算", async () => {
    const calls: Array<unknown> = [];
    installSidecar({
      "wechat_local.page": (params: never) => {
        calls.push(params);
        return pagePayload();
      },
    });
    renderSection();

    fireEvent.change(screen.getByLabelText("本地库会话 id"), { target: { value: "filehelper" } });
    fireEvent.click(screen.getByTestId("wechat-local-window-all"));
    fireEvent.click(screen.getByTestId("wechat-local-page-run"));
    await screen.findByTestId("wechat-local-page-messages");
    expect((calls[0] as { from_ts?: number }).from_ts).toBeUndefined();

    fireEvent.click(screen.getByTestId("wechat-local-window-7d"));
    fireEvent.click(screen.getByTestId("wechat-local-page-run"));
    await waitFor(() => expect(calls.length).toBeGreaterThanOrEqual(2));
    const fromTs = (calls[calls.length - 1] as { from_ts?: number }).from_ts;
    expect(typeof fromTs).toBe("number");
    expect(fromTs!).toBeGreaterThan(Math.floor(Date.now() / 1000) - 8 * 86400);
  });

  it("导出:null 回包(用户取消目录选择)静默回 idle 零提示", async () => {
    const exportCalls: Array<unknown> = [];
    mocks.listen.mockResolvedValue(() => undefined);
    mocks.invoke.mockImplementation(async (command: string, args: unknown) => {
      if (command === "wechat_chat_export") {
        exportCalls.push(args);
        return null; // 用户取消
      }
      throw JSON.stringify({ code: "method_not_found", path: "method", message: "未知调用" });
    });
    renderSection();

    fireEvent.change(screen.getByLabelText("本地库会话 id"), { target: { value: "filehelper" } });
    fireEvent.change(screen.getByTestId("wechat-local-export-format"), { target: { value: "xlsx" } });
    fireEvent.click(screen.getByTestId("wechat-local-export-run"));

    await waitFor(() => expect(exportCalls).toHaveLength(1));
    const args = exportCalls[0] as { chatId: string; format: string };
    expect(args.chatId).toBe("filehelper");
    expect(args.format).toBe("xlsx");
    // 取消 = 静默:无错误无回执列表
    await waitFor(() => expect(screen.queryByTestId("wechat-local-export-error")).toBeNull());
    expect(screen.queryByTestId("wechat-local-export-files")).toBeNull();
  });

  it("导出:回执路径列表上屏;进度事件驱动进度条并携带取消", async () => {
    const holder: { emit: ((payload: unknown) => void) | null } = { emit: null };
    mocks.listen.mockImplementation(
      async (_name: string, cb: (event: { payload: unknown }) => void) => {
        holder.emit = (payload: unknown) => cb({ payload });
        return () => undefined;
      },
    );
    const cancelCalls: Array<unknown> = [];
    let resolveExport: ((value: unknown) => void) | null = null;
    mocks.invoke.mockImplementation(async (command: string, args: unknown) => {
      if (command === "wechat_chat_export") {
        return await new Promise((resolve) => {
          resolveExport = resolve;
        });
      }
      if (command === "wechat_chat_export_cancel") {
        cancelCalls.push(args);
        return { ok: true };
      }
      throw JSON.stringify({ code: "method_not_found", path: "method", message: "未知调用" });
    });
    renderSection();

    fireEvent.change(screen.getByLabelText("本地库会话 id"), { target: { value: "filehelper" } });
    fireEvent.click(screen.getByTestId("wechat-local-export-run"));
    await waitFor(() => expect(mocks.listen).toHaveBeenCalled());

    // 进度事件:job_id 捕获 → 取消按钮在场;pct_est 上屏
    holder.emit?.({ job_id: 9, seq: 1, body: { progress: { phase: "write", rows: 500, pct_est: 42.5 } } });
    const progress = await screen.findByTestId("wechat-local-export-progress");
    expect(progress.textContent).toContain("43"); // Math.round(42.5)
    fireEvent.click(screen.getByTestId("wechat-local-export-cancel"));
    await waitFor(() => expect(cancelCalls).toHaveLength(1));
    expect((cancelCalls[0] as { jobId: number }).jobId).toBe(9);

    // 终态回执:产物路径列表。先等 invoke 真正进场(resolve 落位)再放行
    // 终态——waitFor(listen) 只保证订阅完成,invoke 是其后的独立微步,
    // 高负载下抢先 resolve 会被 null 静默吞掉(files 永不出现→findBy 超时,
    // 本文件曾 1/13 复现的竞态);局部 let 在回调内赋值会被 CFA 钉成
    // null,读出侧显式还原可空签名再调。
    await waitFor(() => {
      expect(resolveExport as unknown).not.toBeNull();
    });
    (resolveExport as unknown as (value: unknown) => void)({
      export: {
        chat_id: "filehelper",
        display_name: "文件传输助手",
        format: "html",
        files: [
          { name: "a.html", path: "/tmp/exports/a.html", rows: 10, sha256: "0".repeat(64) },
          { name: "manifest.json", path: "/tmp/exports/manifest.json", rows: 10, sha256: "1".repeat(64) },
        ],
        manifest_path: "/tmp/exports/manifest.json",
        total_rows: 10,
        time_range: null,
        elapsed_ms: 5,
      },
    });
    const files = await screen.findByTestId("wechat-local-export-files");
    expect(files.textContent).toContain("/tmp/exports/a.html");
    expect(files.textContent).toContain("/tmp/exports/manifest.json");
  });
});
