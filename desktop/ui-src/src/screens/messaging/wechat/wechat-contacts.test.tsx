// @vitest-environment jsdom
//
// 联系人工作台浏览器组件测试(task 10-14-wechat-contacts R6b):五 chip 计数
// 呈现与切换 / 搜索 debounce 200ms / 加载更多 cursor 续拉 / 考古声明与证据
// 徽标 / 导出三格式与回执(取消 = 静默)/ 错误族结构化直显。桥命令与壳命令
// 全走 mock invoke,零真跑(判例 wechat-local.test.tsx)。
import { cleanup, fireEvent, render, screen, waitFor } from "@testing-library/react";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";

const mocks = vi.hoisted(() => ({ invoke: vi.fn() }));
vi.mock("@tauri-apps/api/core", () => ({ invoke: mocks.invoke }));

import { ContactsBrowser } from "./wechat-contacts";
import type { WechatContactsView } from "./wechat-contacts-api";

type Params = Record<string, unknown> | undefined;

/** 全字段契约夹具(桥 R1 应答内层对象同形;内容全合成)。 */
function contactsView(overrides: Partial<WechatContactsView> = {}): WechatContactsView {
  return {
    counts: { friend: 731, group: 105, official: 346, former: 20310, other: 594, system: 4 },
    former_tiers: null,
    residue_checked: false,
    strict_residual_count: 1,
    labels: [
      { id: 4, name: "同事" },
      { id: 5, name: "家人" },
    ],
    stranger: [],
    room_verify: { present: true, rows: 0 },
    rows: [
      {
        username: "wxid_friend_a",
        display_name: "好友A",
        remark: "备注A",
        nickname: "好友A",
        alias: "",
        type: "friend",
        local_type: 1,
        evidence: [],
        description: null,
      },
      {
        username: "wxid_friend_b",
        display_name: "好友B",
        remark: "",
        nickname: "好友B",
        alias: "alias_b",
        type: "friend",
        local_type: 1,
        evidence: [],
        description: null,
      },
    ],
    next_cursor: "CUR1",
    has_more: true,
    filter: { type: "friend", keyword: null, with_residue: false, include_stranger: true },
    page_size: 100,
    degraded: [],
    ...overrides,
  };
}

/** sidecar + 壳命令双通道 mock:wechat_local.contacts 按 params 分发;
 * wechat_contacts_export 由用例即时覆写。 */
function installBridge(handler: (params: Params) => WechatContactsView): void {
  mocks.invoke.mockImplementation(
    async (command: string, args: { method?: string; params?: Params } | Record<string, unknown>) => {
      if (command === "wechat_contacts_export") {
        // 导出应答由用例经 mockReturnValueOnce 覆写;缺省 = 取消(null)
        return null;
      }
      if (command === "sidecar_request" && (args as { method?: string }).method === "wechat_local.contacts") {
        return handler((args as { params?: Params }).params);
      }
      throw JSON.stringify({
        code: "method_not_found",
        path: "method",
        message: `未知调用 ${command}`,
      });
    },
  );
}

/** 最近一次 contacts 调用的 params(断言 wire 形状)。 */
function lastContactsParams(): Params {
  const call = [...mocks.invoke.mock.calls]
    .reverse()
    .find((entry) => {
      const [command, args] = entry as [string, { method?: string }];
      return command === "sidecar_request" && args?.method === "wechat_local.contacts";
    });
  return (call?.[1] as { params?: Params } | undefined)?.params;
}

beforeEach(() => {
  mocks.invoke.mockReset();
});

afterEach(() => {
  cleanup();
});

describe("联系人工作台:chip 计数与切换", () => {
  it("挂载即拉取:五 chip 人话 + 实值计数;缺省好友桶首页", async () => {
    installBridge(() => contactsView());
    render(<ContactsBrowser />);
    await waitFor(() => {
      expect(screen.getByTestId("wechat-contacts-chip-friend").textContent).toBe("好友731");
    });
    expect(screen.getByTestId("wechat-contacts-chip-group").textContent).toBe("群聊105");
    expect(screen.getByTestId("wechat-contacts-chip-official").textContent).toBe("公众号346");
    expect(screen.getByTestId("wechat-contacts-chip-former").textContent).toBe("曾经的好友20,310");
    expect(screen.getByTestId("wechat-contacts-chip-other").textContent).toBe("其他594");
    // 缺省请求:好友桶 + with_residue 关(AC9 域收缩:常规浏览不触 message 副本)
    await waitFor(() => {
      expect(lastContactsParams()).toMatchObject({ type: "friend", with_residue: false, limit: 100 });
    });
    // 行渲染:显示名 + 类型徽标
    expect(screen.getAllByTestId("wechat-contacts-row").length).toBe(2);
    expect(screen.getByText("好友A")).toBeTruthy();
  });

  it("点击群聊 chip:type=group 首页拉取 + chip 选中态", async () => {
    installBridge((_params) =>
      contactsView({
        rows: [
          {
            username: "91000000001@chatroom",
            display_name: "合成群A",
            remark: "",
            nickname: "合成群A",
            alias: "",
            type: "group",
            local_type: 2,
            evidence: [],
            description: null,
            member_count: 3,
          },
        ],
        filter: { type: "group", keyword: null, with_residue: false, include_stranger: true },
      }),
    );
    render(<ContactsBrowser />);
    await waitFor(() => expect(screen.getByTestId("wechat-contacts-chip-group").textContent).toContain("105"));
    fireEvent.click(screen.getByTestId("wechat-contacts-chip-group"));
    await waitFor(() => {
      expect(lastContactsParams()).toMatchObject({ type: "group", with_residue: false });
    });
    // 群行成员数徽标
    await waitFor(() => expect(screen.getByText("成员 3")).toBeTruthy());
  });
});

describe("联系人工作台:搜索与翻页", () => {
  it("搜索 debounce 200ms:立即不触发,200ms 后带 keyword 首页拉取", async () => {
    installBridge(() => contactsView());
    render(<ContactsBrowser />);
    await waitFor(() => expect(screen.getByTestId("wechat-contacts-chip-friend").textContent).toContain("731"));
    const before = mocks.invoke.mock.calls.length;
    fireEvent.change(screen.getByTestId("wechat-contacts-search"), { target: { value: "张" } });
    // 立即不触发(debounce 窗内)
    await new Promise((resolve) => setTimeout(resolve, 60));
    expect(mocks.invoke.mock.calls.length).toBe(before);
    // 200ms 后触发
    await waitFor(
      () => {
        expect(lastContactsParams()).toMatchObject({ type: "friend", keyword: "张" });
      },
      { timeout: 1500 },
    );
  });

  it("加载更多:cursor 续拉追加行(零清空)", async () => {
    installBridge((params) =>
      (params?.cursor as string | undefined) === "CUR1"
        ? contactsView({
            rows: [
              {
                username: "wxid_friend_c",
                display_name: "好友C",
                remark: "",
                nickname: "好友C",
                alias: "",
                type: "friend",
                local_type: 1,
                evidence: [],
                description: null,
              },
            ],
            next_cursor: null,
            has_more: false,
          })
        : contactsView(),
    );
    render(<ContactsBrowser />);
    await waitFor(() => expect(screen.getAllByTestId("wechat-contacts-row").length).toBe(2));
    fireEvent.click(screen.getByTestId("wechat-contacts-load-more"));
    await waitFor(() => {
      expect(lastContactsParams()).toMatchObject({ cursor: "CUR1" });
    });
    await waitFor(() => expect(screen.getAllByTestId("wechat-contacts-row").length).toBe(3));
    // 尾页后「加载更多」退场
    await waitFor(() => expect(screen.queryByTestId("wechat-contacts-load-more")).toBeNull());
  });
});

describe("联系人工作台:考古面(曾经的好友)", () => {
  it("former chip:声明行常驻 + with_residue=true + 分层计数 + 证据徽标 + 子卡", async () => {
    installBridge((params) =>
      (params?.type as string) === "former"
        ? contactsView({
            counts: { friend: 731, group: 105, official: 346, former: 20310, other: 594, system: 4 },
            former_tiers: { msg_residue: 6386, table_only: 13924 },
            residue_checked: true,
            stranger: [
              {
                username: "v3_stranger_1@stranger",
                display_name: "陌生人甲",
                local_type: 4,
                remark: "",
              },
            ],
            room_verify: { present: true, rows: 0 },
            rows: [
              {
                username: "wxid_former_a",
                display_name: "旧友A",
                remark: "",
                nickname: "旧友A",
                alias: "",
                type: "former",
                local_type: 3,
                evidence: ["msg_residue"],
                description: null,
              },
              {
                username: "wxid_former_b",
                display_name: "旧友B",
                remark: "",
                nickname: "旧友B",
                alias: "alias_b",
                type: "former",
                local_type: 3,
                evidence: ["msg_residue", "identity_fields"],
                description: null,
              },
              {
                username: "wxid_former_c",
                display_name: "旧友C",
                remark: "",
                nickname: "旧友C",
                alias: "",
                type: "former",
                local_type: 3,
                evidence: [],
                description: null,
              },
            ],
            filter: { type: "former", keyword: null, with_residue: true, include_stranger: true },
          })
        : contactsView(),
    );
    render(<ContactsBrowser />);
    await waitFor(() => expect(screen.getByTestId("wechat-contacts-chip-former").textContent).toContain("20,310"));
    fireEvent.click(screen.getByTestId("wechat-contacts-chip-former"));
    // with_residue 仅考古 chip 触发(AC9)
    await waitFor(() => {
      expect(lastContactsParams()).toMatchObject({ type: "former", with_residue: true });
    });
    // 声明行(人话,非保证如实)
    const declaration = await waitFor(() => screen.getByTestId("wechat-contacts-declaration"));
    expect(declaration.textContent).toContain("考古呈现");
    expect(declaration.textContent).toContain("不保证完整与准确");
    // 分层计数
    expect(screen.getByTestId("wechat-contacts-tiers").textContent).toContain("6,386");
    expect(screen.getByTestId("wechat-contacts-tiers").textContent).toContain("13,924");
    // 证据徽标:会话痕迹 / 身份字段残留;无徽标 = 仅残留低置信
    expect(screen.getAllByTestId("wechat-contacts-evidence").length).toBe(3); // A 行 1 + B 行 2
    expect(screen.getAllByText("会话痕迹").length).toBe(2);
    expect(screen.getAllByText("身份字段残留").length).toBe(1);
    // 子卡:stranger(非好友联系人缓存)+ room_verify(本机无记录)
    const stranger = await screen.findByTestId("wechat-contacts-stranger");
    expect(stranger.textContent).toContain("陌生人甲");
    expect(screen.getByTestId("wechat-contacts-room-verify").textContent).toContain("本机无记录");
    // 标签尾注(清单计数,不做逐人关联)
    expect(screen.getByTestId("wechat-contacts-labels").textContent).toContain("库内标签:2 个");
  });

  it("非 former chip 不触考古面:无声明行、with_residue 恒 false", async () => {
    installBridge(() => contactsView());
    render(<ContactsBrowser />);
    await waitFor(() => expect(screen.getByTestId("wechat-contacts-chip-friend").textContent).toContain("731"));
    expect(screen.queryByTestId("wechat-contacts-declaration")).toBeNull();
    expect(screen.queryByTestId("wechat-contacts-archaeology")).toBeNull();
    expect(lastContactsParams()).toMatchObject({ with_residue: false });
  });
});

describe("联系人工作台:导出", () => {
  it("勾选三格式导出:typeFilter/formats wire 正确,回执路径呈现", async () => {
    installBridge(() => contactsView());
    mocks.invoke.mockImplementation(async (command: string) => {
      if (command === "wechat_contacts_export") {
        return {
          files: [
            { name: "联系人-好友-2026-10-14.json", path: "/tmp/联系人-好友.json", rows: 731 },
            { name: "联系人-好友-2026-10-14.csv", path: "/tmp/联系人-好友.csv", rows: 731 },
            { name: "联系人-好友-2026-10-14.vcf", path: "/tmp/联系人-好友.vcf", rows: 731 },
          ],
          total_rows: 731,
        };
      }
      return contactsView();
    });
    render(<ContactsBrowser />);
    await waitFor(() => expect(screen.getByTestId("wechat-contacts-chip-friend").textContent).toContain("731"));
    fireEvent.click(screen.getByTestId("wechat-contacts-export-csv"));
    fireEvent.click(screen.getByTestId("wechat-contacts-export-vcf"));
    fireEvent.click(screen.getByTestId("wechat-contacts-export"));
    const call = await waitFor(() => {
      const found = mocks.invoke.mock.calls.find(([command]) => command === "wechat_contacts_export");
      expect(found).toBeTruthy();
      return found;
    });
    expect(call![1]).toEqual({
      typeFilter: "friend",
      keyword: null,
      withResidue: false,
      formats: ["json", "csv", "vcf"],
    });
    // 回执:路径列表(title 悬浮全路径)
    const receipt = await screen.findByTestId("wechat-contacts-receipt");
    expect(receipt.textContent).toContain("已导出 731 行");
    expect(receipt.textContent).toContain("/tmp/联系人-好友.json");
  });

  it("取消保存对话框(应答 null):静默回 idle,零回执零错误", async () => {
    installBridge(() => contactsView());
    render(<ContactsBrowser />);
    await waitFor(() => expect(screen.getByTestId("wechat-contacts-chip-friend").textContent).toContain("731"));
    fireEvent.click(screen.getByTestId("wechat-contacts-export"));
    await waitFor(() => {
      expect(mocks.invoke.mock.calls.some(([command]) => command === "wechat_contacts_export")).toBe(true);
    });
    await new Promise((resolve) => setTimeout(resolve, 50));
    expect(screen.queryByTestId("wechat-contacts-receipt")).toBeNull();
    expect(screen.queryByTestId("wechat-contacts-export-error")).toBeNull();
  });

  it("零格式勾选:面板内 invalid_params 提示,不 invoke 壳命令", async () => {
    installBridge(() => contactsView());
    render(<ContactsBrowser />);
    await waitFor(() => expect(screen.getByTestId("wechat-contacts-chip-friend").textContent).toContain("731"));
    fireEvent.click(screen.getByTestId("wechat-contacts-export-json")); // 取消唯一勾选
    fireEvent.click(screen.getByTestId("wechat-contacts-export"));
    await new Promise((resolve) => setTimeout(resolve, 50));
    expect(mocks.invoke.mock.calls.some(([command]) => command === "wechat_contacts_export")).toBe(false);
    expect(screen.getByTestId("wechat-contacts-export-error").textContent).toContain("至少勾选一种导出格式");
  });
});

describe("联系人工作台:错误族", () => {
  it("桥 key_unavailable(21):结构化直显(code + 修复指引),不重试", async () => {
    mocks.invoke.mockImplementation(async (command: string, args: { method?: string }) => {
      if (command === "sidecar_request" && args.method === "wechat_local.contacts") {
        throw JSON.stringify({
          code: "key_unavailable",
          path: "$",
          message: "密钥缺位:本地库钥匙未就绪",
          data: { fix_hint: "到设置页完成取钥后重试" },
        });
      }
      throw JSON.stringify({ code: "method_not_found", path: "method", message: "未知调用" });
    });
    render(<ContactsBrowser />);
    const error = await screen.findByTestId("wechat-contacts-error");
    expect(error.textContent).toContain("key_unavailable");
    expect(error.textContent).toContain("密钥缺位");
    expect(error.textContent).toContain("到设置页完成取钥后重试");
  });
});
