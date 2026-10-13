// @vitest-environment jsdom
//
// 聊天记录导出 IPC 契约测试(task 10-14-wechat-chat-export R6;mock Tauri
// IPC 零真壳),与壳侧 src-tauri/src/wechat_chat_export.rs / 桥 R5 契约
// 逐字段对齐:命令回包三形(null 取消 / export 回执 / error 信封)、进度
// 事件订阅(job_id 寻址 + 宽容解析)、取消透传、回执守门抛 TypeError。
import { afterEach, describe, expect, it, vi } from "vitest";

const mocks = vi.hoisted(() => ({
  invoke: vi.fn(),
  listen: vi.fn(),
}));

vi.mock("@tauri-apps/api/core", () => ({ invoke: mocks.invoke }));
vi.mock("@tauri-apps/api/event", () => ({ listen: mocks.listen }));

import { SidecarRequestError } from "@/lib/api";
import {
  WECHAT_CHAT_EXPORT_EVENT_NAME,
  WECHAT_CHAT_EXPORT_FORMATS,
  parseWechatChatExportEvent,
  parseWechatChatExportReceipt,
  subscribeWechatChatExportProgress,
  wechatChatExport,
  wechatChatExportCancel,
} from "./wechat-chat-export-api";

afterEach(() => {
  mocks.invoke.mockReset();
  mocks.listen.mockReset();
});

/** 桥 R5 成功回执夹具(wire snake_case 原样)。 */
function receiptFixture(): Record<string, unknown> {
  return {
    chat_id: "50438708676@chatroom",
    display_name: "TMS 中转站交流1️⃣",
    format: "json",
    files: [
      {
        name: "聊天记录-TMS 中转站交流1️⃣-20261014-120000.json",
        path: "/Users/dev/Exports/聊天记录-TMS 中转站交流1️⃣-20261014-120000.json",
        rows: 1200,
        sha256: "a".repeat(64),
      },
    ],
    manifest_path: "/Users/dev/Exports/manifest.json",
    total_rows: 1200,
    time_range: { from_ts: 1_740_000_000, to_ts: 1_760_000_000 },
    elapsed_ms: 8421,
  };
}

describe("wechatChatExport 命令封装", () => {
  it("camelCase 参数透传壳命令;export 回执守门解析", async () => {
    mocks.invoke.mockResolvedValue({ export: receiptFixture() });
    const receipt = await wechatChatExport({
      chatId: "50438708676@chatroom",
      format: "json",
      outDir: "/Users/dev/Exports",
      fromTs: 1_740_000_000,
      displayNamePref: "nickname-first",
      types: ["text", "file"],
    });
    expect(mocks.invoke).toHaveBeenCalledWith("wechat_chat_export", {
      chatId: "50438708676@chatroom",
      format: "json",
      outDir: "/Users/dev/Exports",
      fromTs: 1_740_000_000,
      types: ["text", "file"],
      displayNamePref: "nickname-first",
    });
    expect(receipt?.total_rows).toBe(1200);
    expect(receipt?.files[0].sha256).toBe("a".repeat(64));
    expect(receipt?.time_range?.to_ts).toBe(1_760_000_000);
  });

  it("null 回包 = 用户取消目录选择,静默返回 null(不抛)", async () => {
    mocks.invoke.mockResolvedValue(null);
    await expect(wechatChatExport({ chatId: "c", format: "txt" })).resolves.toBeNull();
  });

  it("error 信封回包 → SidecarRequestError(桥错误族原样)", async () => {
    mocks.invoke.mockResolvedValue({
      error: { code: "export_cancelled", message: "导出已取消" },
    });
    const thrown = await wechatChatExport({ chatId: "c", format: "txt" }).catch((e) => e);
    expect(thrown).toBeInstanceOf(SidecarRequestError);
    expect((thrown as SidecarRequestError).code).toBe("export_cancelled");
  });

  it("invoke 抛出的信封字符串 → asSidecarError 归一化", async () => {
    mocks.invoke.mockRejectedValue(
      JSON.stringify({ code: "component_missing", path: "$", message: "桥组件未安装" }),
    );
    const thrown = await wechatChatExport({ chatId: "c", format: "csv" }).catch((e) => e);
    expect((thrown as SidecarRequestError).code).toBe("component_missing");
  });

  it("回执形状漂移(缺 manifest_path)→ TypeError 大声失败", () => {
    expect(() => parseWechatChatExportReceipt({ total_rows: 1 })).toThrow(TypeError);
    expect(() => parseWechatChatExportReceipt("不是对象")).toThrow(TypeError);
    // files 元素残缺:丢弃该条不拦整单
    const base = receiptFixture();
    const goodFile = (base.files as unknown[])[0];
    const parsed = parseWechatChatExportReceipt({
      ...base,
      files: [goodFile, { name: 42 }, null],
    });
    expect(parsed.files).toHaveLength(1);
  });
});

describe("进度事件订阅", () => {
  it("订阅事件名常量与壳侧成对;载荷宽容解析(坏行丢弃不炸)", async () => {
    expect(WECHAT_CHAT_EXPORT_EVENT_NAME).toBe("wechat-chat-export-progress");
    const holder: { emit: ((payload: unknown) => void) | null } = { emit: null };
    mocks.listen.mockImplementation(
      async (_name: string, cb: (event: { payload: unknown }) => void) => {
        holder.emit = (payload: unknown) => cb({ payload });
        return () => undefined;
      },
    );
    const seen: number[] = [];
    const unlisten = await subscribeWechatChatExportProgress((event) => {
      seen.push(event.job_id);
    });
    expect(mocks.listen).toHaveBeenCalledWith(
      WECHAT_CHAT_EXPORT_EVENT_NAME,
      expect.any(Function),
    );
    holder.emit?.({
      job_id: 7,
      seq: 0,
      body: { progress: { phase: "starting", rows: 0 } },
    });
    holder.emit?.({ job_id: 7, seq: 1, body: { progress: { phase: "write", rows: 500 } } });
    holder.emit?.("坏行");
    holder.emit?.({ job_id: 7, seq: 2, body: { export: {} } }); // 终态行非 progress → 丢
    expect(seen).toEqual([7, 7]);
    expect(typeof unlisten).toBe("function");
  });

  it("事件守门:缺 job_id/seq/progress 均为 null", () => {
    expect(parseWechatChatExportEvent(null)).toBeNull();
    expect(parseWechatChatExportEvent({ seq: 1, body: { progress: {} } })).toBeNull();
    expect(parseWechatChatExportEvent({ job_id: 1, seq: 1, body: {} })).toBeNull();
    expect(
      parseWechatChatExportEvent({ job_id: 1, seq: 1, body: { progress: { phase: "chat" } } }),
    ).toMatchObject({ job_id: 1, seq: 1 });
  });
});

describe("取消与格式词表", () => {
  it("cancel 透传 jobId;{ok:false} 如实返回", async () => {
    mocks.invoke.mockResolvedValue({ ok: false });
    await expect(wechatChatExportCancel(9)).resolves.toEqual({ ok: false });
    expect(mocks.invoke).toHaveBeenCalledWith("wechat_chat_export_cancel", { jobId: 9 });
  });

  it("六格式人话词表 = 桥 CLI 封闭词表(顺序即下拉序)", () => {
    expect(WECHAT_CHAT_EXPORT_FORMATS.map((f) => f.value)).toEqual([
      "json", "txt", "csv", "md", "html", "xlsx",
    ]);
    expect(WECHAT_CHAT_EXPORT_FORMATS.map((f) => f.label)).toEqual([
      "JSON 文件", "纯文本", "CSV 表格", "Markdown", "网页", "Excel 表格",
    ]);
  });
});
