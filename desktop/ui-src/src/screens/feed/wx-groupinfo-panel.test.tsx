// @vitest-environment jsdom
/**
 * 群信息面板测试(10-13-wechat-groupinfo R2;R3 导出态机同文件扩展)——
 * mock 壳侧 IPC(invoke 按命令名分发;载荷 = 任务档 prd「group-info 应答
 * 契约 v1」钉死形状)。覆盖:面板渲染(群名大字/群主/成员 N 人)/ 成员列表
 * (显示名为主 + wxid 次要灰字 + 备注)/ 群主标记 / 公告折叠展开 / 加载与
 * 错误态(重试真重发)/ 导出态机(R3:idle 可点 → 导出中禁用 → 成功行内
 * 两件路径 / 失败人话可重试 / 取消壳回 null 静默)/ Esc 关闭;api 纯函数
 * parseWechatGroupInfo 守门(契约全量 / 缺表缺行降级 / 形状漂移大声失败 /
 * 单行残缺丢弃)、wxGroupInfoChatKey 前缀剥除与导出回执守门
 * parseWechatGroupExportResult(三字段严校 + null 取消直通)。
 */
import { cleanup, fireEvent, render, screen, waitFor, within } from "@testing-library/react";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";

import { SidecarRequestError } from "@/lib/api";

import {
  parseWechatGroupExportResult,
  wechatGroupExport,
} from "./wechat-group-export-api";
import {
  parseWechatGroupInfo,
  wechatGroupInfo,
  wxGroupInfoChatKey,
  type WechatGroupInfo,
} from "./wechat-groupinfo-api";
import { WxGroupInfoPanel } from "./wx-groupinfo-panel";

vi.mock("@tauri-apps/api/core", () => ({ invoke: vi.fn() }));

const invokeMock = (await import("@tauri-apps/api/core")).invoke as unknown as import("vitest").Mock;

/** 契约夹具(prd「group-info 应答契约 v1」全量形状;TMS 群实名同款) */
function groupInfoPayload(overrides: Record<string, unknown> = {}): Record<string, unknown> {
  return {
    chat_id: "50438708676@chatroom",
    display_name: "TMS 中转站交流1️⃣",
    member_count: 97,
    owner: { username: "wxid_owner", display: "老王" },
    announcement: {
      text: "本群仅供技术交流,禁止广告。",
      editor_display: "老王",
      published_at: "2026-10-13T09:30:00",
    },
    status: null,
    members: [
      { username: "wxid_owner", display: "老王", remark: null, is_owner: true },
      { username: "wxid_a", display: "花开相随", remark: "备注名", is_owner: false },
      { username: "wxid_b", display: null, remark: null, is_owner: false },
    ],
    ...overrides,
  };
}

function renderPanel(props: { source?: string; onClose?: () => void } = {}) {
  const onClose = props.onClose ?? vi.fn();
  render(<WxGroupInfoPanel source={props.source ?? "weixin-TMS 中转站交流"} onClose={onClose} />);
  return { onClose };
}

beforeEach(() => {
  invokeMock.mockReset();
});

afterEach(() => {
  cleanup();
});

describe("微信群信息面板(渲染/成员/群主/公告/态)", () => {
  it("面板渲染主链:加载词 → 群名大字 / 群主(名+wxid 灰字)/ 成员 N 人 / 短公告全文;invoke 寻址键剥 weixin- 前缀", async () => {
    invokeMock.mockResolvedValue(groupInfoPayload());
    renderPanel();
    // 载入在途占位词(不空窗一拍)
    expect(screen.getByTestId("wx-groupinfo-loading").textContent).toContain("正在读取群信息");
    // 完成态:群名大字(display_name 优先)+ chat_id 只作 title 悬浮不上屏
    expect(await screen.findByTestId("wx-groupinfo-name").then((node) => node.textContent)).toBe(
      "TMS 中转站交流1️⃣",
    );
    const name = screen.getByTestId("wx-groupinfo-name");
    expect(name.getAttribute("title")).toBe("50438708676@chatroom");
    expect(name.textContent).not.toContain("@chatroom");
    // 群主行:显示名为主 + wxid 次要灰字
    const owner = screen.getByTestId("wx-groupinfo-owner");
    expect(owner.textContent).toContain("老王");
    expect(owner.textContent).toContain("wxid_owner");
    // 成员 N 人(人话判例)
    expect(screen.getByTestId("wx-groupinfo-member-count").textContent).toBe("成员 97 人");
    // 短公告:全文直出,零折叠钮(阈内不折)
    const announcement = screen.getByTestId("wx-groupinfo-announcement");
    expect(announcement.textContent).toContain("本群仅供技术交流,禁止广告。");
    expect(announcement.textContent).toContain("老王 编辑");
    expect(within(announcement).getByRole("time").getAttribute("datetime")).toBe("2026-10-13T09:30:00");
    expect(screen.queryByTestId("wx-groupinfo-announcement-toggle")).toBeNull();
    // 寻址键:源名剥 weixin- 前缀(名→id 解析在壳侧命令内,api 模块头注「寻址」节)
    expect(invokeMock).toHaveBeenCalledWith("wechat_group_info", { chat: "TMS 中转站交流" });
  });

  it("成员列表:显示名为主,wxid 次要灰字,备注带「备注」词面;无显示名成员如实「—」", async () => {
    invokeMock.mockResolvedValue(groupInfoPayload());
    renderPanel();
    await screen.findByTestId("wx-groupinfo-name");
    const members = screen.getByTestId("wx-groupinfo-members");
    const ownerRow = within(members).getByTestId("wx-groupinfo-member-wxid_owner");
    expect(within(ownerRow).getByText("老王")).toBeTruthy();
    expect(ownerRow.textContent).toContain("wxid_owner");
    const remarkedRow = within(members).getByTestId("wx-groupinfo-member-wxid_a");
    expect(remarkedRow.textContent).toContain("花开相随");
    expect(remarkedRow.textContent).toContain("备注 备注名");
    // 无显示名成员:名位「—」(不猜),wxid 灰字仍在
    const bareRow = within(members).getByTestId("wx-groupinfo-member-wxid_b");
    expect(bareRow.textContent).toContain("—");
    expect(bareRow.textContent).toContain("wxid_b");
  });

  it("群主标记:is_owner 成员行带「群主」徽标,普通成员零徽标", async () => {
    invokeMock.mockResolvedValue(groupInfoPayload());
    renderPanel();
    await screen.findByTestId("wx-groupinfo-name");
    const members = screen.getByTestId("wx-groupinfo-members");
    expect(within(members).getAllByTestId("wx-groupinfo-owner-badge")).toHaveLength(1);
    expect(
      within(members).getByTestId("wx-groupinfo-member-wxid_owner").textContent,
    ).toContain("群主");
    expect(
      within(members).getByTestId("wx-groupinfo-member-wxid_a").textContent,
    ).not.toContain("群主");
  });

  it("公告折叠:长文(>160 字符)默认截断 + 省略号,展开全文后全文在屏,title 留全文;收起回折叠", async () => {
    const longText = "公".repeat(200);
    invokeMock.mockResolvedValue(groupInfoPayload({ announcement: { text: longText, editor_display: null, published_at: null } }));
    renderPanel();
    await screen.findByTestId("wx-groupinfo-name");
    const announcement = screen.getByTestId("wx-groupinfo-announcement");
    const toggle = within(announcement).getByTestId("wx-groupinfo-announcement-toggle");
    // 折叠态:前 160 字符 + 省略号;全文不入 DOM
    expect(announcement.textContent).toContain("公".repeat(160));
    expect(announcement.textContent).not.toContain("公".repeat(161));
    expect(announcement.textContent).toContain("…");
    expect(toggle.getAttribute("aria-expanded")).toBe("false");
    // 展开:全文在屏 + aria-expanded 翻真 + 词面转「收起」
    fireEvent.click(toggle);
    expect(announcement.textContent).toContain("公".repeat(200));
    expect(screen.getByTestId("wx-groupinfo-announcement-toggle").getAttribute("aria-expanded")).toBe("true");
    expect(screen.getByTestId("wx-groupinfo-announcement-toggle").textContent).toBe("收起");
    // 收起:回折叠态
    fireEvent.click(screen.getByTestId("wx-groupinfo-announcement-toggle"));
    expect(screen.getByTestId("wx-groupinfo-announcement").textContent).not.toContain("公".repeat(161));
  });

  it("缺库缺表如实降级:owner/announcement 缺行显「—」,成员数缺表显「成员数未知」,成员空表给知会词;群名回落源剥前缀", async () => {
    invokeMock.mockResolvedValue(
      groupInfoPayload({
        display_name: null,
        member_count: null,
        owner: null,
        announcement: null,
        members: [],
      }),
    );
    renderPanel({ source: "weixin-AI中转站-♾️ AI Token" });
    expect(await screen.findByTestId("wx-groupinfo-name").then((node) => node.textContent)).toBe(
      "AI中转站-♾️ AI Token",
    );
    expect(screen.getByTestId("wx-groupinfo-owner").textContent).toBe("—");
    expect(screen.getByTestId("wx-groupinfo-announcement").textContent).toContain("—");
    expect(screen.getByTestId("wx-groupinfo-member-count").textContent).toBe("成员数未知");
    expect(screen.getByTestId("wx-groupinfo-members-empty").textContent).toContain("暂无成员数据");
  });

  it("导出态机(R3):idle 可点 → 导出中禁用 → 成功行内两件路径(含成员行数),按钮回「导出」可点", async () => {
    let resolveExport!: (value: Record<string, unknown> | null) => void;
    invokeMock.mockImplementation((command: string) => {
      if (command === "wechat_group_info") return Promise.resolve(groupInfoPayload());
      if (command === "wechat_group_export") {
        return new Promise<Record<string, unknown> | null>((resolve) => {
          resolveExport = resolve;
        });
      }
      return Promise.reject(new Error(`unexpected command: ${command}`));
    });
    renderPanel();
    const exportButton = (await screen.findByTestId("wx-groupinfo-export")) as HTMLButtonElement;
    // idle:可点,词面「导出」
    expect(exportButton.disabled).toBe(false);
    expect(exportButton.textContent).toBe("导出");
    // 点导出:前端已持应答原样交壳(chat_id + 全量载荷),壳零重查
    fireEvent.click(exportButton);
    // 导出中:禁用 + 人话词面
    expect((screen.getByTestId("wx-groupinfo-export") as HTMLButtonElement).disabled).toBe(true);
    expect(screen.getByTestId("wx-groupinfo-export").textContent).toBe("导出中…");
    expect(invokeMock).toHaveBeenCalledWith("wechat_group_export", {
      chatId: "50438708676@chatroom",
      jsonPayload: groupInfoPayload(),
    });
    // 放行成功回执:行内两件路径 + 成员行数(人话),按钮回可点
    resolveExport({
      json_path: "/Users/me/Desktop/群信息-TMS 中转站交流1️⃣-2026-10-13.json",
      csv_path: "/Users/me/Desktop/群信息-TMS 中转站交流1️⃣-2026-10-13.csv",
      member_rows: 3,
    });
    const success = await screen.findByTestId("wx-groupinfo-export-success");
    expect(success.textContent).toContain("已导出:");
    expect(success.textContent).toContain("群信息-TMS 中转站交流1️⃣-2026-10-13.json");
    expect(success.textContent).toContain("成员表 3 行");
    expect(success.getAttribute("role")).toBe("status");
    expect((screen.getByTestId("wx-groupinfo-export") as HTMLButtonElement).disabled).toBe(false);
    expect(screen.getByTestId("wx-groupinfo-export").textContent).toBe("导出");
  });

  it("导出取消(R3):壳回 null = 静默 —— 无成功/失败提示,按钮回「导出」可点", async () => {
    let resolveExport!: (value: Record<string, unknown> | null) => void;
    invokeMock.mockImplementation((command: string) => {
      if (command === "wechat_group_info") return Promise.resolve(groupInfoPayload());
      if (command === "wechat_group_export") {
        return new Promise<Record<string, unknown> | null>((resolve) => {
          resolveExport = resolve;
        });
      }
      return Promise.reject(new Error(`unexpected command: ${command}`));
    });
    renderPanel();
    const exportButton = (await screen.findByTestId("wx-groupinfo-export")) as HTMLButtonElement;
    fireEvent.click(exportButton);
    expect(exportButton.textContent).toBe("导出中…");
    resolveExport(null); // 用户关掉保存对话框,壳静默回 null
    await waitFor(() => {
      expect((screen.getByTestId("wx-groupinfo-export") as HTMLButtonElement).disabled).toBe(false);
    });
    expect(screen.queryByTestId("wx-groupinfo-export-success")).toBeNull();
    expect(screen.queryByTestId("wx-groupinfo-export-failed")).toBeNull();
    expect(screen.getByTestId("wx-groupinfo-export").textContent).toBe("导出");
  });

  it("导出失败(R3):壳侧人话 message 行内上屏,按钮回可点即重试(真再发一次)", async () => {
    let rejectExport!: (error: unknown) => void;
    invokeMock.mockImplementation((command: string) => {
      if (command === "wechat_group_info") return Promise.resolve(groupInfoPayload());
      if (command === "wechat_group_export") {
        return new Promise<Record<string, unknown> | null>((_resolve, reject) => {
          rejectExport = reject;
        });
      }
      return Promise.reject(new Error(`unexpected command: ${command}`));
    });
    renderPanel();
    const exportButton = (await screen.findByTestId("wx-groupinfo-export")) as HTMLButtonElement;
    fireEvent.click(exportButton);
    rejectExport(
      JSON.stringify({
        code: "export_failed",
        path: "$",
        message: "成员表写入失败(/tmp/x.csv): 权限不够",
      }),
    );
    const failed = await screen.findByTestId("wx-groupinfo-export-failed");
    expect(failed.textContent).toContain("导出失败:成员表写入失败(/tmp/x.csv): 权限不够");
    expect(failed.getAttribute("role")).toBe("status");
    expect(screen.queryByTestId("wx-groupinfo-export-success")).toBeNull();
    // 按钮回可点:再点真重发(invoke 第二次到 wechat_group_export)
    const retryButton = screen.getByTestId("wx-groupinfo-export") as HTMLButtonElement;
    expect(retryButton.disabled).toBe(false);
    fireEvent.click(retryButton);
    expect(retryButton.textContent).toBe("导出中…");
    const exportCalls = invokeMock.mock.calls.filter(([command]) => command === "wechat_group_export");
    expect(exportCalls).toHaveLength(2);
  });

  it("错误态与重试:桥结构化错误如实上屏(code/message),重试真重发并恢复渲染", async () => {
    invokeMock.mockRejectedValueOnce(
      new SidecarRequestError({
        code: "bridge_error",
        path: "$",
        message: "群不存在或未入库",
      }),
    );
    renderPanel();
    const errorArea = await screen.findByTestId("wx-groupinfo-error");
    expect(errorArea.textContent).toContain("群不存在或未入库");
    expect(errorArea.textContent).toContain("bridge_error");
    expect(screen.queryByTestId("wx-groupinfo-name")).toBeNull();
    // 重试:第二次应答在场 → 面板恢复
    invokeMock.mockResolvedValue(groupInfoPayload());
    fireEvent.click(within(errorArea).getByRole("button", { name: "重试" }));
    expect(await screen.findByTestId("wx-groupinfo-name")).toBeTruthy();
    expect(invokeMock).toHaveBeenCalledTimes(2);
  });

  it("解析失败与真 0 人分层(评审 10-13):壳侧 group_not_resolved → 错误态词面「未能定位该群(不在最近会话)」,绝不渲染「成员 0 人」冒充", async () => {
    invokeMock.mockRejectedValueOnce(
      JSON.stringify({
        code: "group_not_resolved",
        path: "$",
        message: "未能定位该群(不在最近会话)",
      }),
    );
    renderPanel();
    const errorArea = await screen.findByTestId("wx-groupinfo-error");
    expect(errorArea.textContent).toContain("未能定位该群(不在最近会话)");
    expect(errorArea.textContent).toContain("group_not_resolved");
    // 关键分层断言:数据面零渲染 —— 0 人/空表降级词面不冒充解析失败
    expect(screen.queryByTestId("wx-groupinfo-member-count")).toBeNull();
    expect(screen.queryByTestId("wx-groupinfo-members-empty")).toBeNull();
    // 重试可达(解析失败可能是群暂不在最近会话,稍后重试可救)
    invokeMock.mockResolvedValue(groupInfoPayload());
    fireEvent.click(within(errorArea).getByRole("button", { name: "重试" }));
    expect(await screen.findByTestId("wx-groupinfo-name")).toBeTruthy();
    expect(screen.getByTestId("wx-groupinfo-member-count").textContent).toBe("成员 97 人");
  });

  it("Esc 关闭(onOpenChange false → onClose)", async () => {
    invokeMock.mockResolvedValue(groupInfoPayload());
    const { onClose } = renderPanel();
    await screen.findByTestId("wx-groupinfo-name");
    fireEvent.keyDown(screen.getByRole("dialog"), { key: "Escape" });
    expect(onClose).toHaveBeenCalledTimes(1);
  });
});

describe("wechat-groupinfo-api 守门(parse/寻址)", () => {
  it("契约全量解析:逐字段照 prd v1(status 原样透传)", () => {
    const payload = groupInfoPayload({ status: 2 });
    const parsed = parseWechatGroupInfo(payload) as WechatGroupInfo;
    expect(parsed.chat_id).toBe("50438708676@chatroom");
    expect(parsed.display_name).toBe("TMS 中转站交流1️⃣");
    expect(parsed.member_count).toBe(97);
    expect(parsed.owner).toEqual({ username: "wxid_owner", display: "老王" });
    expect(parsed.announcement).toEqual({
      text: "本群仅供技术交流,禁止广告。",
      editor_display: "老王",
      published_at: "2026-10-13T09:30:00",
    });
    expect(parsed.status).toBe(2);
    expect(parsed.members).toEqual([
      { username: "wxid_owner", display: "老王", remark: null, is_owner: true },
      { username: "wxid_a", display: "花开相随", remark: "备注名", is_owner: false },
      { username: "wxid_b", display: null, remark: null, is_owner: false },
    ]);
  });

  it("缺表缺行降级:owner/announcement/member_count null 与 members 空表原样通过", () => {
    const parsed = parseWechatGroupInfo(
      groupInfoPayload({ owner: null, announcement: null, member_count: null, members: [] }),
    );
    expect(parsed.owner).toBeNull();
    expect(parsed.announcement).toBeNull();
    expect(parsed.member_count).toBeNull();
    expect(parsed.members).toEqual([]);
  });

  it("形状漂移大声失败:非对象 / chat_id 缺 / members 非数组 / owner.username 缺 均抛", () => {
    expect(() => parseWechatGroupInfo(null)).toThrow(TypeError);
    expect(() => parseWechatGroupInfo("oops")).toThrow(TypeError);
    expect(() => parseWechatGroupInfo(groupInfoPayload({ chat_id: 42 }))).toThrow(TypeError);
    expect(() => parseWechatGroupInfo(groupInfoPayload({ members: "[]" }))).toThrow(TypeError);
    expect(() => parseWechatGroupInfo(groupInfoPayload({ owner: { display: "无名" } }))).toThrow(TypeError);
  });

  it("成员单行残缺丢弃不抛(无 username 行滤除,其余保留);is_owner 缺键 = false", () => {
    const parsed = parseWechatGroupInfo(
      groupInfoPayload({
        members: [
          { display: "无 id 行" },
          { username: "wxid_ok", display: "完整行", is_owner: true },
          { username: "wxid_quiet" },
          "junk",
        ],
      }),
    );
    expect(parsed.members).toEqual([
      { username: "wxid_ok", display: "完整行", remark: null, is_owner: true },
      { username: "wxid_quiet", display: null, remark: null, is_owner: false },
    ]);
  });

  it("wxGroupInfoChatKey 剥 weixin- 前缀;非前缀源名原样(不猜)", () => {
    expect(wxGroupInfoChatKey("weixin-TMS 中转站交流")).toBe("TMS 中转站交流");
    expect(wxGroupInfoChatKey("wx-旧缩写群")).toBe("旧缩写群");
    expect(wxGroupInfoChatKey("50438708676@chatroom")).toBe("50438708676@chatroom");
  });

  it("wechatGroupInfo:寻址键剥前缀传壳侧;bridge 错误族经 asSidecarError 结构化上抛", async () => {
    invokeMock.mockResolvedValueOnce(groupInfoPayload());
    const info = await wechatGroupInfo("weixin-TMS 中转站交流");
    expect(info.chat_id).toBe("50438708676@chatroom");
    expect(invokeMock).toHaveBeenCalledWith("wechat_group_info", { chat: "TMS 中转站交流" });

    invokeMock.mockRejectedValueOnce(
      JSON.stringify({ code: "db_not_found", path: "$", message: "本地库缺席", data: { fix_hint: "先装组件" } }),
    );
    const error = await wechatGroupInfo("weixin-X").catch((thrown: unknown) => thrown);
    expect(error).toBeInstanceOf(SidecarRequestError);
    expect((error as SidecarRequestError).code).toBe("db_not_found");
    expect((error as SidecarRequestError).message).toContain("本地库缺席");
  });
});

describe("wechat-group-export-api 守门(R3 导出 IPC)", () => {
  it("成功回执守门:两路径非空串 + 行数非负整数;漂移大声失败", () => {
    const ok = parseWechatGroupExportResult({
      json_path: "/tmp/群信息-x-2026-10-13.json",
      csv_path: "/tmp/群信息-x-2026-10-13.csv",
      member_rows: 3,
    });
    expect(ok.member_rows).toBe(3);
    expect(() => parseWechatGroupExportResult(null)).toThrow(TypeError);
    expect(() =>
      parseWechatGroupExportResult({ json_path: "", csv_path: "/tmp/x.csv", member_rows: 1 }),
    ).toThrow(TypeError);
    expect(() =>
      parseWechatGroupExportResult({ json_path: "/tmp/x.json", csv_path: 42, member_rows: 1 }),
    ).toThrow(TypeError);
    expect(() =>
      parseWechatGroupExportResult({ json_path: "/tmp/x.json", csv_path: "/tmp/x.csv", member_rows: 1.5 }),
    ).toThrow(TypeError);
    expect(() =>
      parseWechatGroupExportResult({ json_path: "/tmp/x.json", csv_path: "/tmp/x.csv", member_rows: -1 }),
    ).toThrow(TypeError);
  });

  it("wechatGroupExport:回执对象透传 / null 直通(取消静默语义)/ 错误串归一化;参数键 chatId+jsonPayload", async () => {
    const payload = { chat_id: "50438708676@chatroom", members: [] };
    invokeMock.mockResolvedValueOnce({
      json_path: "/tmp/群信息-x.json",
      csv_path: "/tmp/群信息-x.csv",
      member_rows: 0,
    });
    const result = await wechatGroupExport("50438708676@chatroom", payload);
    expect(result?.json_path).toBe("/tmp/群信息-x.json");
    expect(invokeMock).toHaveBeenCalledWith("wechat_group_export", {
      chatId: "50438708676@chatroom",
      jsonPayload: payload,
    });

    invokeMock.mockResolvedValueOnce(null);
    expect(await wechatGroupExport("x@chatroom", payload)).toBeNull();

    invokeMock.mockRejectedValueOnce(
      JSON.stringify({ code: "export_failed", path: "$", message: "群信息写入失败(/tmp/x.json): 磁盘已满" }),
    );
    const error = await wechatGroupExport("x@chatroom", payload).catch((thrown: unknown) => thrown);
    expect(error).toBeInstanceOf(SidecarRequestError);
    expect((error as SidecarRequestError).code).toBe("export_failed");
    expect((error as SidecarRequestError).message).toContain("磁盘已满");
  });
});
