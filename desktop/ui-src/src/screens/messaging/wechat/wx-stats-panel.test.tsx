// @vitest-environment jsdom
/**
 * 统计报告面板测试(10-14-wechat-stats-reports R6/AC6)——mock 壳侧
 * IPC(invoke 按命令分发;载荷 = 任务档 prd「stats 应答契约 v1」形状的
 * 合成夹具,与桥侧 pytest 夹具同源语义)。覆盖:报告类型四选与会话过滤
 * (群聊只列 @chatroom,私聊/双人只列好友)/ 生成态机(数字卡 + 纯 CSS
 * 条形 + 排行)/ 年度(最常聊 + 深夜)/ 双人(两列对照 + 7×24 热度格)/
 * AI 报告生成与 markdown-lite 渲染 / 导出两件落盘回执 / 错误族(20/21/22)
 * 结构化直显 / 缓存耗时提示。api 纯函数守门(契约全量 / 形状漂移大声失败)。
 */
import { cleanup, fireEvent, render, screen, waitFor } from "@testing-library/react";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";

import { SidecarRequestError } from "@/lib/api";

import { parseStatsChat, yearsFromChats } from "./wechat-stats-api";
import { WechatStatsPanel } from "./wx-stats-panel";

vi.mock("@tauri-apps/api/core", () => ({ invoke: vi.fn() }));

const invokeMock = (await import("@tauri-apps/api/core")).invoke as unknown as import("vitest").Mock;

/** stats chats 契约夹具(群 + 私聊 + 官号混居) */
function chatsPayload() {
  return {
    stats_chats: {
      chats: [
        { chat_id: "50438708676@chatroom", display_name: "TMS 群", kind: "group" as const, message_count: 111048, first_ts: 1750000000, last_ts: 1760000000 },
        { chat_id: "wxid_friend", display_name: "好友甲", kind: "private" as const, message_count: 3525, first_ts: 1740000000, last_ts: 1760000000 },
        { chat_id: "wxid_friend2", display_name: "好友乙", kind: "private" as const, message_count: 900, first_ts: 1740000000, last_ts: 1760000000 },
        { chat_id: "gh_official", display_name: "官号", kind: "official" as const, message_count: 42, first_ts: 1740000000, last_ts: 1760000000 },
      ],
      unattributed_tables: 0,
      copy: { dir: "/private" },
    },
  };
}

/** stats chat 契约夹具(私聊形态;群聊分析复用同形) */
function chatPayload(overrides: Record<string, unknown> = {}) {
  return {
    stats_chat: {
      chat_id: "wxid_friend",
      display_name: "好友甲",
      kind: "private",
      window: { mode: "since", from_ts: 1757000000, to_ts: 1760000000 },
      total: 120,
      sent: 50,
      received: 66,
      human_total: 116,
      type_counts: { text: 100, image: 8, voice: 2, video: 0, sticker: 4, file_or_link: 1, location: 0, other: 0, system: 3, revoke: 1 },
      hourly: Array.from({ length: 24 }, (_, h) => (h === 22 ? 30 : h === 9 ? 12 : 1)),
      weekday: [3, 4, 5, 6, 7, 8, 9],
      monthly: Array.from({ length: 12 }, () => 10),
      daily: [{ date: "2026-10-01", count: 5 }, { date: "2026-10-02", count: 8 }],
      active_days: 90,
      longest_streak: { days: 12, from: "2026-09-20", to: "2026-10-01" },
      top_phrases: [{ phrase: "好的", count: 9 }, { phrase: "周末", count: 5 }],
      senders: [
        { sender_id: "wxid_me", display: "wxid_me", count: 50 },
        { sender_id: "wxid_friend", display: "好友甲", count: 66 },
      ],
      sessions: { threshold_minutes: 30, total: 40, me_initiated: 18, other_initiated: 22 },
      response: { avg_seconds: 300, median_seconds: 120, fastest_seconds: 5, pairs: 80 },
      self_id: "wxid_me",
      first_ts: 1757000000,
      last_ts: 1760000000,
      cache: { hit: false, computed_ms: 4200 },
      ...overrides,
    },
  };
}

function annualPayload() {
  return {
    stats_annual: {
      year: 2026,
      years_available: [2025, 2026],
      total: 20961,
      sent: 10533,
      received: 10173,
      human_total: 20706,
      type_counts: { text: 17940, image: 1135 },
      hourly: Array.from({ length: 24 }, (_, h) => (h === 23 ? 2000 : 100)),
      weekday: [1, 2, 3, 4, 5, 6, 7],
      monthly: Array.from({ length: 12 }, () => 1700),
      active_days: 90,
      longest_streak: { days: 90, from: "2026-07-07", to: "2026-10-04" },
      chats_count: 162,
      top_chats: [{ chat_id: "wxid_friend", display_name: "好友甲", count: 3525 }],
      top_phrases: [{ phrase: "这个", count: 1283 }],
      midnight: { count: 2155, top_chat: { chat_id: "wxid_friend", display_name: "好友甲", count: 400 } },
      friend_contrast: [],
      cache: { hit: true, computed_ms: 12 },
    },
  };
}

function dualPayload() {
  return {
    stats_dual: {
      chat_id: "wxid_friend",
      display_name: "好友甲",
      window: { mode: "all", from_ts: 0, to_ts: 1760000000 },
      first_chat: { ts: 1740000000, sender: "other", text: "在吗" },
      me: { count: 1720, initiated: 158, avg_response_seconds: 1793, top_phrases: [{ phrase: "okok", count: 6 }] },
      other: { count: 1787, initiated: 35, avg_response_seconds: 454, top_phrases: [{ phrase: "机器", count: 7 }] },
      heatmap: Array.from({ length: 7 }, (_, w) => Array.from({ length: 24 }, (_, h) => (w === 5 && h === 22 ? 99 : 1))),
      longest_streak: { days: 28, from: "2026-09-01", to: "2026-09-28" },
      active_days: 74,
      cache: { hit: false, computed_ms: 50 },
    },
  };
}

function sidecarOk(payload: unknown) {
  return Promise.resolve(payload);
}

/** 按方法名分发的 invoke mock(侧车 wechat_local.* + 壳命令导出) */
function mockSidecar(routes: Record<string, unknown>) {
  invokeMock.mockImplementation((method: string, args: Record<string, unknown>) => {
    if (method === "sidecar_request") {
      const m = args.method as string;
      if (m in routes) {
        const handler = routes[m];
        if (typeof handler === "function") return handler(args.params as Record<string, unknown>);
        return sidecarOk(handler);
      }
    }
    if (method in routes) {
      const handler = routes[method];
      if (typeof handler === "function") return Promise.resolve(handler(args));
      return Promise.resolve(handler);
    }
    return Promise.reject(new Error(`unexpected invoke: ${method}`));
  });
}

beforeEach(() => {
  invokeMock.mockReset();
});

afterEach(() => {
  cleanup();
});

describe("统计报告面板(流/渲染/错误/导出)", () => {
  it("主链:私聊分析 → 拉会话(只列好友)→ 生成 → 数字卡/条形/短语/缓存耗时", async () => {
    const paramsSeen: Array<Record<string, unknown>> = [];
    mockSidecar({
      "wechat_local.stats": (params: Record<string, unknown>) => {
        paramsSeen.push(params);
        if (params.mode === "chats") return sidecarOk(chatsPayload());
        return sidecarOk(chatPayload());
      },
    });
    render(<WechatStatsPanel />);
    // 切到私聊分析触发拉取会话
    fireEvent.click(screen.getByTestId("wx-stats-kind-chat"));
    const select = await screen.findByTestId("wx-stats-chat-select");
    await waitFor(() => {
      expect((select as HTMLSelectElement).options.length).toBe(3); // 占位 + 2 好友(官号/群不列)
    });
    fireEvent.change(select, { target: { value: "wxid_friend" } });
    fireEvent.change(screen.getByTestId("wx-stats-window-select"), { target: { value: "365" } });
    fireEvent.click(screen.getByTestId("wx-stats-generate"));
    expect(await screen.findByTestId("wx-stats-card-total").then((n) => n.textContent)).toContain("120");
    expect(screen.getByTestId("wx-stats-card-sent").textContent).toContain("50");
    expect(screen.getByTestId("wx-stats-card-received").textContent).toContain("66");
    expect(screen.getByTestId("wx-stats-card-streak").textContent).toContain("12");
    // 时段条形 + 短语徽标 + 缓存提示(未命中带「首次统计较慢」文案)
    expect(screen.getByTestId("wx-stats-hourly-22")).toBeTruthy();
    expect(screen.getByTestId("wx-stats-phrases").textContent).toContain("好的");
    expect(screen.getByTestId("wx-stats-cache").textContent).toContain("首次统计较慢");
    // 生成参数:mode/chat_id/365 天窗
    expect(paramsSeen[1]).toMatchObject({ mode: "chat", chat_id: "wxid_friend", since_days: 365 });
  });

  it("群聊分析:会话清单只列 @chatroom;发言排行渲染", async () => {
    mockSidecar({
      "wechat_local.stats": (params: Record<string, unknown>) => {
        if (params.mode === "chats") return sidecarOk(chatsPayload());
        return sidecarOk(chatPayload({ chat_id: "50438708676@chatroom", kind: "group", display_name: "TMS 群" }));
      },
    });
    render(<WechatStatsPanel />);
    fireEvent.click(screen.getByTestId("wx-stats-kind-group"));
    const select = await screen.findByTestId("wx-stats-chat-select");
    await waitFor(() => {
      expect((select as HTMLSelectElement).options.length).toBe(2); // 占位 + 群
    });
    fireEvent.change(select, { target: { value: "50438708676@chatroom" } });
    fireEvent.click(screen.getByTestId("wx-stats-generate"));
    expect(await screen.findByTestId("wx-stats-senders").then((n) => n.textContent)).toContain("好友甲");
  });

  it("年度报告:免会话选择;年份下拉来自 chats 推导;最常聊/深夜/缓存命中态", async () => {
    mockSidecar({
      "wechat_local.stats": (params: Record<string, unknown>) => {
        if (params.mode === "chats") return sidecarOk(chatsPayload());
        return sidecarOk(annualPayload());
      },
    });
    render(<WechatStatsPanel />);
    fireEvent.click(screen.getByTestId("wx-stats-kind-annual"));
    // 年度不渲染会话选择,渲染年份下拉(含「全部年份」)
    expect(screen.queryByTestId("wx-stats-chat-select")).toBeNull();
    const yearSelect = screen.getByTestId("wx-stats-year-select");
    await waitFor(() => {
      const values = Array.from((yearSelect as HTMLSelectElement).options).map((o) => o.value);
      expect(values).toContain("2025"); // chats 拉回后年份推导到位
    });
    const optionValues = Array.from((yearSelect as HTMLSelectElement).options).map((o) => o.value);
    expect(optionValues).toContain("all");
    expect(optionValues).toContain("2025"); // first_ts 1740000000 → 2025
    expect(optionValues).toContain("2026");
    fireEvent.click(screen.getByTestId("wx-stats-generate"));
    expect(await screen.findByTestId("wx-stats-card-chats").then((n) => n.textContent)).toContain("162");
    expect(screen.getByTestId("wx-stats-top-chats").textContent).toContain("好友甲");
    expect(screen.getByTestId("wx-stats-result").textContent).toContain("深夜");
    expect(screen.getByTestId("wx-stats-cache").textContent).toContain("缓存命中");
  });

  it("双人报告:两列对照 + 7×24 热度格 + 最初一条", async () => {
    mockSidecar({
      "wechat_local.stats": (params: Record<string, unknown>) => {
        if (params.mode === "chats") return sidecarOk(chatsPayload());
        return sidecarOk(dualPayload());
      },
    });
    render(<WechatStatsPanel />);
    fireEvent.click(screen.getByTestId("wx-stats-kind-dual"));
    const select = await screen.findByTestId("wx-stats-chat-select");
    await waitFor(() => expect((select as HTMLSelectElement).options.length).toBe(3));
    fireEvent.change(select, { target: { value: "wxid_friend" } });
    fireEvent.click(screen.getByTestId("wx-stats-generate"));
    expect(await screen.findByTestId("wx-stats-card-me").then((n) => n.textContent)).toContain("1720");
    expect(screen.getByTestId("wx-stats-card-other").textContent).toContain("1787");
    expect(screen.getByTestId("wx-stats-dual-me").textContent).toContain("开启话题 158 次");
    expect(screen.getByTestId("wx-stats-dual-other").textContent).toContain("平均回复");
    expect(screen.getByTestId("wx-stats-result").textContent).toContain("最初一条");
    const heatmap = screen.getByTestId("wx-stats-heatmap");
    expect(heatmap.querySelectorAll("span.bg-primary").length).toBeGreaterThan(7 * 24 - 1);
  });

  it("AI 报告:生成 → markdown-lite 渲染章节;载荷回传前端已持 stats 应答", async () => {
    const reportCalls: Array<Record<string, unknown>> = [];
    mockSidecar({
      "wechat_local.stats": (params: Record<string, unknown>) =>
        params.mode === "chats" ? sidecarOk(chatsPayload()) : sidecarOk(chatPayload()),
      "wechat_local.stats_report": (params: Record<string, unknown>) => {
        reportCalls.push(params);
        return sidecarOk({
          report_markdown: "## 总览\n\n全年聊了不少。\n\n## 结语\n\n祝好。",
          model: "glm-5.3-flash",
          total_tokens: 321,
        });
      },
    });
    render(<WechatStatsPanel />);
    fireEvent.click(screen.getByTestId("wx-stats-kind-chat"));
    const select = await screen.findByTestId("wx-stats-chat-select");
    await waitFor(() => expect((select as HTMLSelectElement).options.length).toBe(3));
    fireEvent.change(select, { target: { value: "wxid_friend" } });
    fireEvent.click(screen.getByTestId("wx-stats-generate"));
    await screen.findByTestId("wx-stats-result");
    fireEvent.click(screen.getByTestId("wx-stats-ai"));
    expect(await screen.findByTestId("wx-stats-ai-report").then((n) => n.textContent)).toContain("glm-5.3-flash");
    expect(screen.getByTestId("wx-stats-ai-markdown").textContent).toContain("总览");
    // 载荷 = 前端已持应答原样回传(桥不重查),mode 同步
    expect(reportCalls[0].mode).toBe("chat");
    const payload = reportCalls[0].stats_payload as Record<string, unknown>;
    expect(payload).toHaveProperty("stats_chat");
  });

  it("导出:AI 报告在场 → 两件落盘回执直显", async () => {
    mockSidecar({
      "wechat_local.stats": (params: Record<string, unknown>) =>
        params.mode === "chats" ? sidecarOk(chatsPayload()) : sidecarOk(chatPayload()),
      "wechat_local.stats_report": () =>
        sidecarOk({ report_markdown: "## 总览\n\n导出用。", model: "glm-5.3-flash", total_tokens: 9 }),
      wechat_stats_export: (args: Record<string, unknown>) =>
        Promise.resolve(
          args.markdownPayload
            ? { json_path: "/tmp/私聊分析-好友甲.json", markdown_path: "/tmp/私聊分析-好友甲.md" }
            : { json_path: "/tmp/私聊分析-好友甲.json" },
        ),
    });
    render(<WechatStatsPanel />);
    fireEvent.click(screen.getByTestId("wx-stats-kind-chat"));
    const select = await screen.findByTestId("wx-stats-chat-select");
    await waitFor(() => expect((select as HTMLSelectElement).options.length).toBe(3));
    fireEvent.change(select, { target: { value: "wxid_friend" } });
    fireEvent.click(screen.getByTestId("wx-stats-generate"));
    await screen.findByTestId("wx-stats-result");
    // 先生成 AI 报告 → 导出两件(json + md)
    fireEvent.click(screen.getByTestId("wx-stats-ai"));
    await screen.findByTestId("wx-stats-ai-report");
    fireEvent.click(screen.getByTestId("wx-stats-export"));
    expect(await screen.findByTestId("wx-stats-export-receipt").then((n) => n.textContent)).toContain(
      "私聊分析-好友甲.md",
    );
  });

  it("错误族:桥 key_unavailable(21)结构化直显,重试真重发", async () => {
    let attempts = 0;
    invokeMock.mockImplementation((method: string) => {
      if (method !== "sidecar_request") return Promise.resolve(null);
      attempts += 1;
      return Promise.reject(
        new SidecarRequestError({
          code: "key_unavailable",
          path: "$",
          message: "本地库密钥不可得",
          data: { fix_hint: "先在设置里完成取钥" },
        }),
      );
    });
    render(<WechatStatsPanel />);
    fireEvent.click(screen.getByTestId("wx-stats-kind-chat"));
    await screen.findByTestId("wx-stats-chats-error");
    expect(screen.getByTestId("wx-stats-chats-error").textContent).toContain("key_unavailable");
    expect(screen.getByTestId("wx-stats-chats-error").textContent).toContain("修复指引");
    expect(attempts).toBe(1);
  });

  it("未选会话点生成 = 本地校验提示(invalid_params,零 IPC)", async () => {
    mockSidecar({ "wechat_local.stats": (p: Record<string, unknown>) => sidecarOk(p.mode === "chats" ? chatsPayload() : chatPayload()) });
    render(<WechatStatsPanel />);
    fireEvent.click(screen.getByTestId("wx-stats-kind-chat"));
    // 不拉取/不选择,直接点年度以外的生成
    const generate = screen.getByTestId("wx-stats-generate");
    invokeMock.mockClear();
    fireEvent.click(generate);
    expect(await screen.findByTestId("wx-stats-error").then((n) => n.textContent)).toContain("请先选择一个会话");
    expect(invokeMock.mock.calls.filter((c) => c[0] === "sidecar_request").length).toBe(0);
  });
});

describe("api 守门纯函数", () => {
  it("parseStatsChat:契约全量解析;形状漂移(chat_id 缺)大声失败", () => {
    const view = parseStatsChat(chatPayload().stats_chat);
    expect(view.total).toBe(120);
    expect(view.hourly).toHaveLength(24);
    expect(view.response.avg_seconds).toBe(300);
    expect(view.cache).toEqual({ hit: false, computed_ms: 4200 });
    expect(() => parseStatsChat({ chat_id: 42 })).toThrow(TypeError);
    expect(() => parseStatsChat({ hourly: [1, 2] })).toThrow(/chat_id/);
  });

  it("yearsFromChats:首末时间戳推导年份(含当年);空清单 = 仅当年", () => {
    const years = yearsFromChats(chatsPayload().stats_chats.chats);
    expect(years).toContain(2025);
    expect(years).toContain(new Date().getFullYear());
    expect(yearsFromChats([])).toEqual([new Date().getFullYear()]);
  });
});
