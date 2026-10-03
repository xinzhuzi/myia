// @vitest-environment jsdom
//
// 消息屏组件测试:mock sidecar(壳命令 sidecar_request 的 JS 假实现,
// 内存态模拟 channel_directory/aliases/ledger/rules),覆盖:目录渲染
// (平台分组/类型徽标/死信徽标/别名徽标)、别名行内编辑(调用 channels.alias
// set/delete)、targets 多选产出 platform:名称 spec 与 push.write 全量保存、
// 平台刷新按钮、空态(先配平台凭据指引)、断连态(结构化错误 + 重试)。
// 平台总览(10-03-messaging-hermes-look):左平台卡网格 + 右详情面板双栏 ——
// 三态(已连接绿/需要设置黄/即将支持灰,secret.list 凭据探测 + channels.list
// 目录信号派生)、全部/已连接/未启用筛选(tone 呼应 + 切筛选带动选中)、
// 28 平台头像芯片(见 platform-icons.test.tsx)、详情面板(描述/状态说明/
// 出站凭据指南唯一入口/目录速览)、底部状态条(sidecar 健康 + 已连接平台
// 计数)、入站项零出现(扫码/允许的用户 ID/webhook secret 不渲染)。
// 告警规则子面板(10-04-alert-rules design §9/§11):列表行(启停 Switch =
// 全量提交/when 摘要/动作徽章/命中 N/最近触发)、新建编辑表单(when 校验
// 反馈 = alerts.save 构造期错直显 + 前端预检)、测试按钮(alerts.test 真调,
// rule_id/草稿两形态)、删除二次确认、alerts.fired 事件(onSidecarEvent →
// toast + 命中数刷新)、旧版 sidecar(method_not_found)降级不挡整屏。
// 协议契约权威:desktop/entry.py `_m_channels_*` / `_m_push_write` +
// 任务 design.md §4(alerts 四方法契约;协议落地前按契约 mock)。
import { act, cleanup, fireEvent, render, screen, waitFor, within } from "@testing-library/react";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import { MemoryRouter } from "react-router-dom";

const mocks = vi.hoisted(() => ({ invoke: vi.fn(), listen: vi.fn() }));
vi.mock("@tauri-apps/api/core", () => ({ invoke: mocks.invoke }));
// 事件通道:onSidecarEvent → listen("sidecar://event", handler);捕获 handler
// 供测试注入 alerts.fired(dashboard/logs 屏同款 mock 形态)
vi.mock("@tauri-apps/api/event", () => ({ listen: mocks.listen }));

import { MessagingScreen } from "./messaging-screen";
import type { AlertRuleInput, AlertRuleView, BridgeStatusView, ChannelsView } from "./api";
import {
  buildPlatformCards,
  deriveImplementedStatus,
  matchSecretNames,
  matchesFilter,
} from "./platform-overview";

const FILE = "plugins/messaging-demo.yaml";

/** 已注册的 sidecar 事件 handler(供 emitSidecarEvent 注入事件)。 */
const eventHandlers: Array<(payload: unknown) => void> = [];

/** 向所有已注册 handler 注入一条 sidecar 事件(alerts.fired 测试用)。
 *  client.ts 的 listen 回调解包 event.payload 后才进屏内 handler ——
 *  注入须按 Tauri 事件形态({event, id, payload})包装。 */
function emitSidecarEvent(payload: unknown): void {
  for (const handler of [...eventHandlers]) {
    act(() => handler({ event: "sidecar://event", id: 1, payload }));
  }
}

// ---------------------------------------------------------------------------
// 协议夹具(形状逐字段对照 ./api.ts / desktop/entry.py 应答载荷)
// ---------------------------------------------------------------------------

function channelEntry(
  platform: string,
  chatId: string,
  name: string,
  extra: Partial<{ type: string; last_seen: number | null }> = {},
) {
  return {
    platform,
    chat_id: chatId,
    name,
    type: extra.type ?? "group",
    thread_id: null,
    last_seen: extra.last_seen ?? null,
  };
}

function channelsViewFixture(): ChannelsView {
  return {
    data_root: "/tmp/home",
    updated_at: "2026-10-03T08:00:00",
    platforms: {
      feishu: [
        channelEntry("feishu", "oc_1", "AI中转站合伙人群", { last_seen: 1760000000 }),
        channelEntry("feishu", "oc_2", "羊毛反馈群", { type: "dm" }),
      ],
      telegram: [channelEntry("telegram", "12345", "测试私聊", { type: "dm" })],
    },
    aliases: {} as Record<string, Record<string, string>>,
    dead: ["feishu:oc_2"],
    rules: [
      {
        file: FILE,
        category_id: "messaging-demo",
        category_name: "消息屏夹具",
        parse_ok: true,
        error: null,
        entries: [
          {
            index: 0,
            channel: "feishu_card",
            platform: "feishu",
            targets: ["feishu:AI中转站合伙人群"],
            has_template: false,
            route_count: 1,
            raw: {
              channel: "feishu_card",
              targets: ["feishu:AI中转站合伙人群"],
              route: [{ when: "category == 'freebie'", mode: "immediate" }],
            },
          },
          {
            index: 1,
            channel: "stdout",
            platform: null,
            targets: [],
            has_template: false,
            route_count: 0,
            raw: { channel: "stdout" },
          },
        ],
      },
    ],
  };
}

/** 告警规则视图夹具(design §4.1 AlertRuleView = 规则全字段 + 派生两列)。 */
function alertRuleViewFixture(): AlertRuleView {
  return {
    id: 1,
    name: "竞对融资",
    enabled: true,
    scope: "global",
    when: "'融资' in title",
    action: "push",
    action_config: { channel: "feishu_card" },
    created_at: "2026-10-04T00:00:00",
    updated_at: "2026-10-04T00:00:00",
    fired_count: 2,
    last_fired_at: "2026-10-04T01:23:45",
  };
}

// ---------------------------------------------------------------------------
// mock sidecar:内存态 = channels.list 四视图 + alerts 规则表 + yaml.list;
// 写方法只记账(不真改状态;alerts.save 按「全量替换保 id」语义维护内存态)
// ---------------------------------------------------------------------------

type Handler = (params: never) => unknown;
type SidecarMap = Record<string, Handler>;

function okSidecar() {
  const view = channelsViewFixture();
  // 告警规则内存态(10-04-alert-rules;服务端 = alert_rules/alert_fired 两表)
  const alertRules = { rules: [alertRuleViewFixture()] as AlertRuleView[] };
  // secret.list 名单(平台总览凭据探测用;只有名字,值永不可读)
  const secrets = { names: [] as string[] };
  // health 是否应答失败(false = R4 状态条「sidecar 不可达」路径;缺省 true)
  const health = { ok: true };
  const calls: { method: string; params: unknown }[] = [];
  const map: SidecarMap = {
    "channels.list": () => JSON.parse(JSON.stringify(view)) as unknown,
    "channels.refresh": (params: never) => {
      const { platform } = params as { platform: string };
      const bucket = view.platforms[platform] ?? [];
      return { platform, merged: bucket.length, entries: bucket };
    },
    "channels.alias": (params: never) => {
      const { platform, chat_id, name } = params as {
        platform: string;
        chat_id: string;
        name: string | null;
      };
      if (name === null) {
        delete view.aliases[platform]?.[chat_id];
      } else {
        (view.aliases[platform] ??= {})[chat_id] = name;
      }
      return { platform, chat_id: chat_id, deleted: name === null, name };
    },
    "push.write": (params: never) => {
      const { file, push } = params as { file: string; push: unknown[] };
      return { file, written: true as const, changed: true, push };
    },
    "secret.list": () => ({ names: [...secrets.names] }),
    // health 应答形状只需支撑「一来一回成功 = 存活」判定(R4 状态条)
    health: () => {
      if (!health.ok) {
        throw JSON.stringify({
          code: "sidecar_not_running",
          path: "$",
          message: "sidecar 进程未运行",
        });
      }
      return { healthy: true };
    },
    // ---- 告警规则族(design §4.1 契约;协议落地前按契约 mock)----
    "alerts.list": () => ({ rules: JSON.parse(JSON.stringify(alertRules.rules)) }),
    "alerts.save": (params: never) => {
      const { rules } = params as { rules: AlertRuleInput[] };
      // 全量替换:带 id = 更新保 id(派生列保留),不带 = 新建分配 id
      let nextId = Math.max(0, ...alertRules.rules.map((rule) => rule.id)) + 1;
      const next = rules.map((input) => {
        const existing = alertRules.rules.find((rule) => rule.id === input.id);
        if (existing && input.id !== undefined) {
          return { ...existing, ...input, updated_at: "2026-10-04T02:00:00" };
        }
        return {
          ...input,
          id: nextId++,
          created_at: "2026-10-04T02:00:00",
          updated_at: "2026-10-04T02:00:00",
          fired_count: 0,
          last_fired_at: null,
        };
      });
      alertRules.rules = next as AlertRuleView[];
      return { ok: true as const, rules: JSON.parse(JSON.stringify(alertRules.rules)) };
    },
    "alerts.delete": (params: never) => {
      const { id } = params as { id: number };
      if (!alertRules.rules.some((rule) => rule.id === id)) {
        throw JSON.stringify({
          code: "alert_not_found",
          path: "params.id",
          message: `告警规则不存在: ${id}`,
          data: { id },
        });
      }
      alertRules.rules = alertRules.rules.filter((rule) => rule.id !== id);
      return { ok: true as const };
    },
    "alerts.test": (params: never) => {
      const { rule_id: ruleId } = params as { rule_id?: number };
      if (ruleId !== undefined && !alertRules.rules.some((rule) => rule.id === ruleId)) {
        throw JSON.stringify({
          code: "alert_not_found",
          path: "params.rule_id",
          message: `告警规则不存在: ${ruleId}`,
          data: { id: ruleId },
        });
      }
      return {
        matched: true,
        muted: false,
        actions: [
          {
            action: "push" as const,
            channel: "feishu_card",
            resolved: true,
            resolved_target: "messaging-demo push[0]",
            targets: null,
            template: null,
            degrade_reason: null,
          },
        ],
        already_fired: ruleId === 1,
      };
    },
    "yaml.list": () => ({
      plugins_dir: "/tmp/plugins",
      files: [
        {
          file: FILE,
          name: "messaging-demo.yaml",
          parse_ok: true,
          category_id: "messaging-demo",
          category_name: "消息屏夹具",
          sources: 1,
          error: null,
        },
      ],
    }),
  };
  const record = (method: string, params: unknown) => {
    calls.push({ method, params });
  };
  return { map, view, alertRules, secrets, health, calls, record };
}

/** 安装 mock sidecar:所有 invoke("sidecar_request") 走此分派;未知方法=结构化 404 */
function installSidecar(map: SidecarMap, record?: (method: string, params: unknown) => void): void {
  mocks.invoke.mockImplementation(
    async (_command: string, args: { method: string; params?: unknown }) => {
      const handler = map[args.method];
      if (record) record(args.method, args.params);
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

function lastParams(calls: { method: string; params: unknown }[], method: string): unknown {
  return calls.filter((call) => call.method === method).at(-1)?.params;
}

beforeEach(() => {
  mocks.invoke.mockReset();
  // 事件通道缺省实现:捕获 handler(emitSidecarEvent 注入用),unlisten 恒可用
  // (sources.test.tsx 注释同款:undefined unlisten 会让屏内 .then 炸)
  mocks.listen.mockReset();
  eventHandlers.length = 0;
  mocks.listen.mockImplementation(
    async (_name: string, handler: (payload: unknown) => void) => {
      eventHandlers.push(handler);
      return () => undefined;
    },
  );
});
afterEach(() => {
  cleanup(); // vitest 非 globals 模式下 RTL 不自动清理,防 DOM 跨测试污染
  vi.clearAllMocks();
});

// ---------------------------------------------------------------------------

describe("消息:通道目录渲染", () => {
  it("平台分组渲染:名称/类型徽标/最后发现/死信徽标;死信只标在对应行", async () => {
    const sidecar = okSidecar();
    installSidecar(sidecar.map, sidecar.record);
    render(
      <MemoryRouter>
        <MessagingScreen />
      </MemoryRouter>,
    );

    const feishu = within(await screen.findByTestId("platform-feishu"));
    expect(feishu.getByText("AI中转站合伙人群")).toBeTruthy();
    // 类型徽标:group(群)/dm(私聊)如实呈现
    expect(feishu.getByText("group")).toBeTruthy();
    expect(feishu.getByText("dm")).toBeTruthy();
    // 死信徽标只在 oc_2 行;别名徽标此时不存在
    const deadRow = feishu.getByTestId("entry-oc_2");
    expect(within(deadRow).getByText("死信")).toBeTruthy();
    expect(within(feishu.getByTestId("entry-oc_1")).queryByText("死信")).toBeNull();
    expect(screen.queryByText("别名")).toBeNull();
    // telegram 平台分组同样渲染
    expect(within(screen.getByTestId("platform-telegram")).getByText("测试私聊")).toBeTruthy();
  });
});

describe("消息:别名行内编辑", () => {
  it("改名:输入新名保存 → channels.alias(set)参数正确,成功提示呈现", async () => {
    const sidecar = okSidecar();
    installSidecar(sidecar.map, sidecar.record);
    render(
      <MemoryRouter>
        <MessagingScreen />
      </MemoryRouter>,
    );
    const feishu = within(await screen.findByTestId("platform-feishu"));
    fireEvent.click(within(feishu.getByTestId("entry-oc_1")).getByRole("button", { name: "改名" }));

    const input = feishu.getByLabelText("别名 oc_1") as HTMLInputElement;
    expect(input.value).toBe("AI中转站合伙人群"); // 预填当前名
    fireEvent.change(input, { target: { value: "重点群" } });
    fireEvent.click(feishu.getByRole("button", { name: "保存" }));

    expect(lastParams(sidecar.calls, "channels.alias")).toEqual({
      platform: "feishu",
      chat_id: "oc_1",
      name: "重点群",
    });
    await waitFor(() => {
      expect(screen.getByTestId("messaging-notice").textContent).toContain("已命名 feishu:重点群");
    });
  });

  it("已命名条目出「别名」徽标与「取消别名」;点击 → channels.alias(name:null)", async () => {
    const sidecar = okSidecar();
    sidecar.view.aliases = { feishu: { oc_1: "手工名" } };
    installSidecar(sidecar.map, sidecar.record);
    render(
      <MemoryRouter>
        <MessagingScreen />
      </MemoryRouter>,
    );
    const feishu = within(await screen.findByTestId("platform-feishu"));
    const row = feishu.getByTestId("entry-oc_1");
    expect(within(row).getByText("别名")).toBeTruthy();

    fireEvent.click(within(row).getByRole("button", { name: "取消别名" }));
    expect(lastParams(sidecar.calls, "channels.alias")).toEqual({
      platform: "feishu",
      chat_id: "oc_1",
      name: null,
    });
    await waitFor(() => {
      expect(screen.getByTestId("messaging-notice").textContent).toContain("已取消");
    });
  });
});

describe("消息:targets 多选与 push.write 保存", () => {
  it("勾选产出 platform:名称 spec;保存提交完整 push 数组(仅 targets 变)", async () => {
    const sidecar = okSidecar();
    installSidecar(sidecar.map, sidecar.record);
    render(
      <MemoryRouter>
        <MessagingScreen />
      </MemoryRouter>,
    );

    const group = await screen.findByTestId("rule-file-messaging-demo");
    // 初始态:已选 AI中转站合伙人群(spec 文本直接可见)
    expect(group.textContent).toContain("feishu:AI中转站合伙人群");

    // 取消 AI中转站合伙人群,勾上 羊毛反馈群(spec = feishu:羊毛反馈群)
    fireEvent.click(within(group).getByLabelText("对象 AI中转站合伙人群"));
    fireEvent.click(within(group).getByLabelText("对象 羊毛反馈群"));

    fireEvent.click(within(group).getByRole("button", { name: "保存推送对象" }));

    expect(lastParams(sidecar.calls, "push.write")).toEqual({
      file: FILE,
      push: [
        {
          channel: "feishu_card",
          targets: ["feishu:羊毛反馈群"],
          route: [{ when: "category == 'freebie'", mode: "immediate" }],
        },
        { channel: "stdout" },
      ],
    });
    await waitFor(() => {
      expect(screen.getByTestId("messaging-notice").textContent).toContain("已保存");
    });
  });

  it("不支持寻址的条目(stdout/webhook)不出选择器,如实说明", async () => {
    const sidecar = okSidecar();
    installSidecar(sidecar.map, sidecar.record);
    render(
      <MemoryRouter>
        <MessagingScreen />
      </MemoryRouter>,
    );
    const group = await screen.findByTestId("rule-file-messaging-demo");
    expect(group.textContent).toContain("该通道不支持目录寻址");
  });
});

describe("消息:平台刷新", () => {
  it("点平台组内「刷新」→ channels.refresh({platform});失败 toast 结构化错误", async () => {
    const sidecar = okSidecar();
    installSidecar(sidecar.map, sidecar.record);
    render(
      <MemoryRouter>
        <MessagingScreen />
      </MemoryRouter>,
    );
    fireEvent.click(
      within(await screen.findByTestId("platform-feishu")).getByRole("button", { name: "刷新" }),
    );
    expect(lastParams(sidecar.calls, "channels.refresh")).toEqual({ platform: "feishu" });
    await waitFor(() => {
      expect(screen.getByTestId("messaging-notice").textContent).toContain("feishu 目录已刷新");
    });

    // 失败路径:凭据缺失族错误如实带回,目录不清空
    sidecar.map["channels.refresh"] = () => {
      throw JSON.stringify({
        code: "channel_refresh_failed",
        path: "params.platform",
        message: "feishu 目录发现失败,旧目录不动: [credential_not_found] 飞书 bot 凭据未配置",
        data: { platform: "feishu", code: "credential_not_found" },
      });
    };
    fireEvent.click(
      within(screen.getByTestId("platform-feishu")).getByRole("button", { name: "刷新" }),
    );
    await waitFor(() => {
      expect(screen.getByTestId("messaging-notice").textContent).toContain("credential_not_found");
    });
    // 旧目录仍在(作用域钉在目录区,规则区的同名选项不参与匹配)
    expect(within(screen.getByTestId("platform-feishu")).getByText("AI中转站合伙人群")).toBeTruthy();
  });
});

describe("消息:空态与断连态", () => {
  it("目录为空 → 「先配平台凭据」指引空态", async () => {
    const sidecar = okSidecar();
    sidecar.view.platforms = {};
    sidecar.view.rules = [];
    installSidecar(sidecar.map);
    render(
      <MemoryRouter>
        <MessagingScreen />
      </MemoryRouter>,
    );
    expect(await screen.findByText("通道目录还是空的")).toBeTruthy();
    expect(screen.getByText(/先到「设置」录入平台凭据/)).toBeTruthy();
    expect(screen.getByText(/还没有品类 YAML/)).toBeTruthy();
    // 状态条:目录空 = 已连接 0(28 张在册卡),sidecar 本身存活
    const bar = await screen.findByTestId("messaging-statusbar");
    await waitFor(() => {
      expect(bar.textContent).toContain("sidecar 正常");
    });
    expect(bar.textContent).toContain("已连接平台 0/28");
  });

  it("sidecar 不可达 → 结构化错误(code/path)+ 重试;状态条同步转红", async () => {
    mocks.invoke.mockImplementation(async () => {
      throw JSON.stringify({ code: "sidecar_not_running", path: "$", message: "sidecar 进程未运行" });
    });
    render(
      <MemoryRouter>
        <MessagingScreen />
      </MemoryRouter>,
    );
    const alert = await screen.findByRole("alert");
    expect(alert.textContent).toContain("sidecar 进程未运行");
    expect(alert.textContent).toContain("code=sidecar_not_running");
    expect(alert.textContent).toContain("path=$");
    // R4 状态条如实反映 sidecar 不可达(channels.list/health 全失败)
    await waitFor(() => {
      expect(screen.getByTestId("messaging-statusbar").textContent).toContain("sidecar 不可达");
    });
    // 屏级重试(同屏还有告警子面板的局部重试,断言限定 ErrorBox 作用域)
    fireEvent.click(within(screen.getByRole("alert")).getByRole("button", { name: "重试" }));
    await waitFor(() => {
      expect(mocks.invoke.mock.calls.length).toBeGreaterThanOrEqual(2);
    });
  });
});

// ---------------------------------------------------------------------------
// 平台总览(10-03-messaging-hermes-look R1-R4:左网格 + 右详情面板)
// ---------------------------------------------------------------------------

describe("消息:平台总览三态与头像卡", () => {
  it("左卡网格 28 张全带头像;缺省选中 feishu,详情面板出已连接 + 目录速览(死信徽标)", async () => {
    const sidecar = okSidecar();
    installSidecar(sidecar.map, sidecar.record);
    render(
      <MemoryRouter>
        <MessagingScreen />
      </MemoryRouter>,
    );

    const overview = await screen.findByTestId("platform-overview");
    const list = within(overview).getByTestId("platform-card-list");
    // R1 验收:28 张平台卡全部带头像芯片(2 精确标 + 26 通用标)
    expect(within(list).getAllByRole("listitem")).toHaveLength(28);
    expect(list.querySelectorAll("[data-testid^='platform-avatar-']")).toHaveLength(28);
    expect(within(list).getByTestId("platform-avatar-feishu")).toBeTruthy();
    expect(within(list).getByTestId("platform-avatar-telegram")).toBeTruthy();

    // 缺省选中第一张已实装卡:详情面板已连接 + 目录速览只读镜像
    const detail = within(overview).getByTestId("platform-detail");
    expect(within(detail).getByText("已连接")).toBeTruthy();
    expect(detail.textContent).toContain("目录非空(2 个会话)");
    expect(within(detail).getByText("AI中转站合伙人群")).toBeTruthy();
    expect(within(detail).getByText("羊毛反馈群")).toBeTruthy();
    // 死信徽标在详情速览的 oc_2 行上;速览标注只读(编辑入口仍在下方通道目录)
    expect(detail.textContent).toContain("oc_2");
    expect(within(detail).getAllByText("死信")).toHaveLength(1);
    expect(detail.textContent).toContain("只读速览");
  });

  it("点击 telegram 卡 → 详情切换(Telegram 头 + 目录速览 1 个会话);左卡网格不动", async () => {
    const sidecar = okSidecar();
    installSidecar(sidecar.map, sidecar.record);
    render(
      <MemoryRouter>
        <MessagingScreen />
      </MemoryRouter>,
    );
    const overview = await screen.findByTestId("platform-overview");
    fireEvent.click(within(overview).getByTestId("platform-card-telegram"));

    const detail = within(overview).getByTestId("platform-detail");
    expect(within(detail).getByText("Telegram")).toBeTruthy();
    expect(within(detail).getByText("已连接")).toBeTruthy();
    expect(within(detail).getByText("测试私聊")).toBeTruthy();
    expect(within(detail).queryByText("AI中转站合伙人群")).toBeNull();
    // 卡网格仍完整(选中只影响右栏)
    expect(within(overview).getByTestId("platform-card-list").querySelectorAll("[data-testid^='platform-avatar-']")).toHaveLength(28);
  });

  it("凭据缺失(目录空且钥匙链无命中)→ 详情面板需要设置(说明含下一步动作)", async () => {
    const sidecar = okSidecar();
    sidecar.view.platforms = {};
    installSidecar(sidecar.map, sidecar.record);
    render(
      <MemoryRouter>
        <MessagingScreen />
      </MemoryRouter>,
    );
    const overview = await screen.findByTestId("platform-overview");
    const detail = within(overview).getByTestId("platform-detail");
    expect(within(detail).getByText("需要设置")).toBeTruthy();
    expect(detail.textContent).toContain("目录为空");
    expect(detail.textContent).toContain("出站凭据指南"); // 需要设置时指南仍在(唯一入口)
  });

  it("钥匙链探测命中(secret.list:scope 或叶子名)→ 目录空也判已连接", async () => {
    const sidecar = okSidecar();
    sidecar.view.platforms = {};
    sidecar.secrets.names = [
      "myia/feishu/bot_token", // scope = 平台 id 命中
      "myia/push/TELEGRAM_BOT_TOKEN", // 叶子名 = 凭据 key 命中
      "myia/llm/api_key", // 无关凭据,不参与
    ];
    installSidecar(sidecar.map, sidecar.record);
    render(
      <MemoryRouter>
        <MessagingScreen />
      </MemoryRouter>,
    );
    const overview = await screen.findByTestId("platform-overview");
    // 缺省选中 feishu → 详情栏说明钥匙链命中;切 telegram 同样命中
    const detail = within(overview).getByTestId("platform-detail");
    expect(within(detail).getByText("已连接")).toBeTruthy();
    expect(detail.textContent).toContain("钥匙链命中 1 项凭据名");
    fireEvent.click(within(overview).getByTestId("platform-card-telegram"));
    expect(within(overview).getByTestId("platform-detail").textContent).toContain(
      "钥匙链命中 1 项凭据名",
    );
  });

  it("灰卡(slack,未实装代表)点击选中 → 详情即将支持 + W3 排期说明;无凭据指南、无目录速览", async () => {
    // 微信已随 10-03-messaging-weixin-bridge 转实装(桥接灰卡另测),
    // coming_soon 行为以 W3 未实装平台代表覆盖。
    const sidecar = okSidecar();
    installSidecar(sidecar.map, sidecar.record);
    render(
      <MemoryRouter>
        <MessagingScreen />
      </MemoryRouter>,
    );
    const overview = await screen.findByTestId("platform-overview");
    fireEvent.click(within(overview).getByTestId("platform-card-slack"));

    const detail = within(overview).getByTestId("platform-detail");
    expect(within(detail).getByText("Slack")).toBeTruthy();
    expect(within(detail).getByText("即将支持")).toBeTruthy();
    expect(detail.textContent).toContain("W3");
    expect(detail.textContent).toContain("尚未实装");
    expect(within(detail).queryByTestId("platform-guide-slack")).toBeNull();
    expect(within(detail).queryByText("目录速览")).toBeNull();
  });
});

describe("消息:平台总览筛选 tabs", () => {
  it("全部(28)/已连接/未启用 正确分组;tab 文案带计数;已连接档隐藏灰卡且选中不动", async () => {
    const sidecar = okSidecar();
    installSidecar(sidecar.map, sidecar.record);
    render(
      <MemoryRouter>
        <MessagingScreen />
      </MemoryRouter>,
    );
    const overview = await screen.findByTestId("platform-overview");

    // 缺省 = 全部:已实装 2 + 未实装 26 = 28 张卡
    expect(within(overview).getByTestId("platform-filter-all").textContent).toBe("全部(28)");
    expect(within(overview).getByTestId("platform-filter-connected").textContent).toBe("已连接(2)");
    expect(within(overview).getByTestId("platform-filter-disabled").textContent).toBe("未启用(26)");
    expect(within(overview).getByTestId("platform-card-weixin")).toBeTruthy();

    // 已连接:只剩已实装且已连接的卡;选中(feishu)仍匹配筛选 → 详情栏不动
    fireEvent.click(within(overview).getByTestId("platform-filter-connected"));
    expect(within(overview).getByTestId("platform-card-feishu")).toBeTruthy();
    expect(within(overview).queryByTestId("platform-card-weixin")).toBeNull();
    expect(within(overview).getByTestId("platform-detail").textContent).toContain("飞书");

    // 未启用:需要设置 + 即将支持(此处 fixture 全已连接 → 只剩灰卡)
    fireEvent.click(within(overview).getByTestId("platform-filter-disabled"));
    expect(within(overview).queryByTestId("platform-card-feishu")).toBeNull();
    expect(within(overview).queryByTestId("platform-card-telegram")).toBeNull();
    expect(within(overview).getByTestId("platform-card-weixin")).toBeTruthy();
    expect(within(overview).getByTestId("platform-card-homeassistant")).toBeTruthy();
  });

  it("切「未启用」带动选中(上游交互流):选中平台不再匹配 → 详情栏切入该筛选下第一张卡", async () => {
    const sidecar = okSidecar();
    installSidecar(sidecar.map, sidecar.record);
    render(
      <MemoryRouter>
        <MessagingScreen />
      </MemoryRouter>,
    );
    const overview = await screen.findByTestId("platform-overview");
    // 缺省选中 feishu(已连接);切到「未启用」后选中不再匹配 → 自动选中该筛选
    // 下第一张卡。fixture 只有 feishu/telegram 已连接 → 第一张未启用 = W2 转实装
    // 但凭据缺失的 ntfy(需要设置,不是灰卡)。
    fireEvent.click(within(overview).getByTestId("platform-filter-disabled"));
    const detail = within(overview).getByTestId("platform-detail");
    // 名称与 id 行都写着 ntfy(h3 + font-mono id),用文本包含断言选中对象
    expect(detail.textContent).toContain("ntfy");
    expect(within(detail).getByText("需要设置")).toBeTruthy();
    expect(detail.textContent).toContain("无自动发现"); // manual 平台的需要设置说明
  });

  it("已实装但凭据缺失 → 归入「未启用」而非「已连接」;切档后详情栏保持在 feishu(需要设置)", async () => {
    const sidecar = okSidecar();
    sidecar.view.platforms = {};
    installSidecar(sidecar.map, sidecar.record);
    render(
      <MemoryRouter>
        <MessagingScreen />
      </MemoryRouter>,
    );
    const overview = await screen.findByTestId("platform-overview");
    expect(within(overview).getByTestId("platform-filter-connected").textContent).toBe("已连接(0)");
    expect(within(overview).getByTestId("platform-filter-disabled").textContent).toBe("未启用(28)");
    fireEvent.click(within(overview).getByTestId("platform-filter-disabled"));
    expect(within(overview).getByTestId("platform-card-feishu")).toBeTruthy();
    const detail = within(overview).getByTestId("platform-detail");
    expect(within(detail).getByText("飞书")).toBeTruthy();
    expect(within(detail).getByText("需要设置")).toBeTruthy();
  });
});

describe("消息:详情栏出站凭据指南(唯一入口)", () => {
  it("选中 feishu 即见指南(零点击,卡片上无展开按钮):tenant token 手工换 + curl 命令", async () => {
    const sidecar = okSidecar();
    installSidecar(sidecar.map, sidecar.record);
    render(
      <MemoryRouter>
        <MessagingScreen />
      </MemoryRouter>,
    );
    const overview = await screen.findByTestId("platform-overview");
    // 缺省选中 feishu:指南直接在详情栏,不再需要「点开卡片」
    const guide = within(overview).getByTestId("platform-guide-feishu");
    expect(guide.textContent).toContain("FEISHU_BOT_TOKEN");
    expect(guide.textContent).toContain("tenant_access_token");
    expect(guide.textContent).toContain("im:message:send_as_bot");
    expect(guide.textContent).toContain(
      "curl -X POST https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal",
    );
    // R2:左卡上不再有指南展开交互(无 aria-expanded 的按钮)
    const feishuCard = within(overview).getByTestId("platform-card-feishu");
    expect(feishuCard.getAttribute("aria-expanded")).toBeNull();
    expect(feishuCard.tagName).toBe("BUTTON"); // 卡即选中按钮,无二级展开
  });

  it("点击 telegram 卡 → 指南切到 telegram(@BotFather + @userinfobot + 两个凭据 key)", async () => {
    const sidecar = okSidecar();
    installSidecar(sidecar.map, sidecar.record);
    render(
      <MemoryRouter>
        <MessagingScreen />
      </MemoryRouter>,
    );
    const overview = await screen.findByTestId("platform-overview");
    fireEvent.click(within(overview).getByTestId("platform-card-telegram"));

    const guide = within(overview).getByTestId("platform-guide-telegram");
    expect(guide.textContent).toContain("TELEGRAM_BOT_TOKEN");
    expect(guide.textContent).toContain("TELEGRAM_CHAT_ID");
    expect(guide.textContent).toContain("@BotFather");
    expect(guide.textContent).toContain("@userinfobot");
    // 详情栏一次只展示一个平台:feishu 指南随选中切换离开
    expect(within(overview).queryByTestId("platform-guide-feishu")).toBeNull();
  });

  it("入站项零出现:详情栏先后选中 feishu/telegram,两份整屏文本不渲染扫码/允许的用户 ID/webhook secret", async () => {
    const sidecar = okSidecar();
    installSidecar(sidecar.map, sidecar.record);
    render(
      <MemoryRouter>
        <MessagingScreen />
      </MemoryRouter>,
    );
    const overview = await screen.findByTestId("platform-overview");
    // 缺省选中 feishu → 指南已在;再切 telegram,两份选中态的整屏文本都收进来断言
    await within(overview).findByTestId("platform-guide-feishu");
    const feishuOpenText = document.body.textContent ?? "";

    fireEvent.click(within(overview).getByTestId("platform-card-telegram"));
    await within(overview).findByTestId("platform-guide-telegram");
    const telegramOpenText = document.body.textContent ?? "";

    for (const text of [feishuOpenText, telegramOpenText]) {
      expect(text).not.toMatch(/扫码/);
      expect(text).not.toMatch(/允许的用户/);
      expect(text).not.toMatch(/webhook\s*secret/i);
    }
  });

  it("W2 三平台指南各就位(ntfy 自建/公共 topic、钉钉群设置→自定义机器人、企微管理后台自建应用)", async () => {
    const sidecar = okSidecar();
    installSidecar(sidecar.map, sidecar.record);
    render(
      <MemoryRouter>
        <MessagingScreen />
      </MemoryRouter>,
    );
    const overview = await screen.findByTestId("platform-overview");

    // ntfy:凭据 key + curl 冒烟 + 直达寻址指引;指南文案只覆盖出站
    fireEvent.click(within(overview).getByTestId("platform-card-ntfy"));
    const ntfyGuide = within(overview).getByTestId("platform-guide-ntfy");
    expect(ntfyGuide.textContent).toContain("NTFY_TARGET");
    expect(ntfyGuide.textContent).toContain("NTFY_TOKEN");
    expect(ntfyGuide.textContent).toContain("docs.ntfy.sh");
    expect(ntfyGuide.textContent).toContain("curl -d");
    expect(ntfyGuide.textContent).toContain("ntfy:my-games-alerts");
    expect(ntfyGuide.textContent).toContain("无自动发现");

    // 钉钉:群设置 → 机器人 → 自定义机器人;加签密钥可配;直达 = 完整 webhook
    fireEvent.click(within(overview).getByTestId("platform-card-dingtalk"));
    const dingGuide = within(overview).getByTestId("platform-guide-dingtalk");
    expect(dingGuide.textContent).toContain("DINGTALK_WEBHOOK_URL");
    expect(dingGuide.textContent).toContain("群设置");
    expect(dingGuide.textContent).toContain("自定义");
    expect(dingGuide.textContent).toContain("dingtalk_secret");
    expect(dingGuide.textContent).toContain("oapi.dingtalk.com/robot/send");

    // 企微:管理后台建自建应用 → corpid/secret/agentid 三凭据 + touser
    fireEvent.click(within(overview).getByTestId("platform-card-wecom"));
    const wecomGuide = within(overview).getByTestId("platform-guide-wecom");
    expect(wecomGuide.textContent).toContain("WECOM_CORPID");
    expect(wecomGuide.textContent).toContain("WECOM_CORPSECRET");
    expect(wecomGuide.textContent).toContain("WECOM_AGENTID");
    expect(wecomGuide.textContent).toContain("work.weixin.qq.com");
    expect(wecomGuide.textContent).toContain("wecom:ZhangSan");
    // 群聊/markdown 是蓝本外能力:描述如实声明只做 text 私聊
    expect(within(overview).getByTestId("platform-detail").textContent).toContain("text 私聊");
  });
});

describe("消息:底部状态条(R4)", () => {
  it("sidecar 健康(health 一来一回成功)+ 已连接平台计数(已连接/在册总数)", async () => {
    const sidecar = okSidecar();
    installSidecar(sidecar.map, sidecar.record);
    render(
      <MemoryRouter>
        <MessagingScreen />
      </MemoryRouter>,
    );
    const bar = await screen.findByTestId("messaging-statusbar");
    await waitFor(() => {
      expect(bar.textContent).toContain("sidecar 正常");
    });
    expect(bar.textContent).toContain("已连接平台 2/28");
  });

  it("health 失败但目录视图可用 → 状态条如实转「sidecar 不可达」,计数照常派生", async () => {
    const sidecar = okSidecar();
    sidecar.health.ok = false;
    installSidecar(sidecar.map, sidecar.record);
    render(
      <MemoryRouter>
        <MessagingScreen />
      </MemoryRouter>,
    );
    // 目录照常(channels.list 成功);状态条只反映 health 信号
    expect(await screen.findByTestId("platform-feishu")).toBeTruthy();
    const bar = screen.getByTestId("messaging-statusbar");
    await waitFor(() => {
      expect(bar.textContent).toContain("sidecar 不可达");
    });
    expect(bar.textContent).toContain("已连接平台 2/28");
  });
});

describe("消息:平台总览派生纯函数", () => {
  it("matchSecretNames:scope=平台 id 或叶子名=凭据 key 命中;其余忽略", () => {
    const names = [
      "myia/feishu/bot_token",
      "myia/push/FEISHU_BOT_TOKEN",
      "myia/llm/api_key",
      "feishu/裸名",
      "myia/feishu", // 无 name 段
    ];
    expect(matchSecretNames("feishu", ["FEISHU_BOT_TOKEN"], names)).toEqual([
      "myia/feishu/bot_token",
      "myia/push/FEISHU_BOT_TOKEN",
    ]);
    expect(matchSecretNames("telegram", ["TELEGRAM_BOT_TOKEN", "TELEGRAM_CHAT_ID"], names)).toEqual([]);
  });

  it("deriveImplementedStatus:目录非空或钥匙链命中 = 已连接;双缺 = 需要设置", () => {
    const bucket = [channelEntry("feishu", "oc_1", "群")];
    expect(deriveImplementedStatus(bucket, [])).toBe("connected");
    expect(deriveImplementedStatus([], ["myia/feishu/bot_token"])).toBe("connected");
    expect(deriveImplementedStatus([], [])).toBe("needs_setup");
  });

  it("buildPlatformCards:6 已实装(5 缺凭据=需要设置 + 微信桥接灰态)+ 22 未实装;灰卡无指南、id 唯一", () => {
    const cards = buildPlatformCards({}, []);
    expect(cards).toHaveLength(28);
    expect(cards.filter((card) => card.status === "needs_setup")).toHaveLength(5);
    expect(cards.filter((card) => card.status === "coming_soon")).toHaveLength(22);
    // 微信桥接(10-03-messaging-weixin-bridge):不传 bridgeStatus = 灰态
    // 「需本机 Hermes」,永黄不了(凭据不在 MYIA 侧,needs_setup 是误导)
    expect(cards.find((c) => c.id === "weixin")!.status).toBe("bridge_unavailable");
    expect(new Set(cards.map((card) => card.id)).size).toBe(28);
    // W2 四平台已转实装:有指南、discovery=manual(无自动发现,蓝本事实)
    for (const id of ["ntfy", "dingtalk", "wecom", "weixin"]) {
      const card = cards.find((c) => c.id === id)!;
      expect(card.guide).not.toBeNull();
      expect(card.wave).toBe("W2");
      expect(card.discovery).toBe("manual");
    }
    // 微信指南 keys 为空是刻意事实:MYIA 侧零凭据(R2「不装可用」如实披露)
    expect(cards.find((c) => c.id === "weixin")!.guide!.keys).toEqual([]);
    expect(cards.find((c) => c.id === "feishu")!.discovery).toBe("auto");
    expect(cards.find((c) => c.id === "telegram")!.discovery).toBe("passive");
    for (const card of cards.filter((c) => c.status === "coming_soon")) {
      expect(card.guide).toBeNull();
      expect(card.directoryCount).toBe(0);
    }
  });

  it("matchesFilter:未启用 = 需要设置 + 即将支持;已连接只收 connected", () => {
    const cards = buildPlatformCards(
      { feishu: [channelEntry("feishu", "oc_1", "群")] },
      ["myia/telegram/bot_token"],
    );
    const byId = Object.fromEntries(cards.map((card) => [card.id, card]));
    expect(byId.feishu.status).toBe("connected"); // 目录非空
    expect(byId.telegram.status).toBe("connected"); // 钥匙链命中
    expect(matchesFilter(byId.feishu, "connected")).toBe(true);
    expect(matchesFilter(byId.weixin, "connected")).toBe(false);
    expect(matchesFilter(byId.feishu, "disabled")).toBe(false);
    expect(matchesFilter(byId.weixin, "disabled")).toBe(true); // 即将支持 → 未启用
    const emptyCards = buildPlatformCards({}, []);
    const needsSetup = emptyCards.find((card) => card.status === "needs_setup")!;
    expect(needsSetup).toBeTruthy();
    expect(matchesFilter(needsSetup, "disabled")).toBe(true); // 需要设置 → 未启用
  });
});

// ---------------------------------------------------------------------------
// 微信桥接灰卡(10-03-messaging-weixin-bridge D4):bridge.status 四态接线
// ---------------------------------------------------------------------------

/** bridge.status 应答夹具(形状对照 ./api.ts BridgeStatusView / entry.py probe_bridge)。 */
function bridgeFixture(overrides: Partial<BridgeStatusView> = {}): BridgeStatusView {
  return {
    available: false,
    reason: "hermes_missing",
    fix_hint:
      "安装 Hermes-Agent,或在本品类 push[].weixin_hermes_bin 配置其 hermes bin 的路径(缺省 ~/.hermes/hermes-agent/.hermes/bin/hermes)",
    bin_found: false,
    weixin_configured: false,
    gateway_alive: false,
    bin_path: "/Users/demo/.hermes/hermes-agent/.hermes/bin/hermes",
    ...overrides,
  };
}

describe("微信桥接:纯函数派生", () => {
  it("不传 bridgeStatus:微信灰态、其余平台卡逐字段不变(向后兼容)", () => {
    const without = buildPlatformCards(
      { feishu: [channelEntry("feishu", "oc_1", "群")] },
      ["myia/telegram/bot_token"],
    );
    const withProbe = buildPlatformCards(
      { feishu: [channelEntry("feishu", "oc_1", "群")] },
      ["myia/telegram/bot_token"],
      bridgeFixture({ available: true }),
    );
    // 其余平台卡与传不传探测无关(快照不变:向后兼容)
    for (const card of without.filter((c) => c.id !== "weixin")) {
      const twin = withProbe.find((c) => c.id === card.id)!;
      expect({ ...twin, bridge: null }).toEqual({ ...card, bridge: null });
    }
    // 微信:不传 = 灰;探测可用 = 绿——两态都不落 needs_setup(永黄不了)
    expect(without.find((c) => c.id === "weixin")!.status).toBe("bridge_unavailable");
    expect(withProbe.find((c) => c.id === "weixin")!.status).toBe("connected");
  });

  it("探测不可用两种原因都归灰态(修复指引随卡携带)", () => {
    for (const reason of ["hermes_missing", "weixin_not_configured"]) {
      const cards = buildPlatformCards({}, [], bridgeFixture({ reason, available: false }));
      const weixin = cards.find((c) => c.id === "weixin")!;
      expect(weixin.status).toBe("bridge_unavailable");
      expect(weixin.bridge?.reason).toBe(reason);
      expect(weixin.bridge?.fix_hint).toBeTruthy();
    }
  });
});

describe("微信桥接:屏级灰卡披露(AC2 UI 侧)", () => {
  function renderScreenWithBridge(bridge: BridgeStatusView | null) {
    const sidecar = okSidecar();
    if (bridge) {
      sidecar.map["bridge.status"] = () => ({ ...bridge });
    }
    installSidecar(sidecar.map, sidecar.record);
    render(
      <MemoryRouter>
        <MessagingScreen />
      </MemoryRouter>,
    );
    return sidecar;
  }

  it("探测不可用:微信卡灰态「需本机 Hermes」+ 详情披露桥接/Hermes + 指南含自查命令", async () => {
    renderScreenWithBridge(bridgeFixture());

    const weixinCard = await screen.findByTestId("platform-card-weixin");
    // 卡面 tone:灰描边(复用 coming_soon 灰值;卡上无文字状态,文案在详情 pill)
    expect(weixinCard.className).toContain("border-border/60");
    expect(weixinCard.className).not.toContain("border-ok/30");
    // 点选微信卡 → 详情面板:状态胶囊「需本机 Hermes」+ 披露文案含「桥接」「Hermes」
    fireEvent.click(weixinCard);
    const detail = await screen.findByTestId("platform-detail");
    expect(within(detail).getByText("需本机 Hermes")).toBeTruthy();
    const detailText = detail.textContent ?? "";
    expect(detailText).toContain("桥接");
    expect(detailText).toContain("Hermes");
    expect(detailText).toContain("如实披露");
    // 凭据指南:peer id 自查步骤(send --list weixin)在列
    expect(detailText).toContain("send --list weixin");
    // 灰态不出目录速览(coming_soon/bridge_unavailable 均无目录区)
    expect(detail.textContent ?? "").not.toContain("目录速览");
  });

  it("探测可用:微信卡绿态「已连接」+ 目录速览走 manual 空桶文案", async () => {
    renderScreenWithBridge(
      bridgeFixture({
        available: true,
        reason: null,
        fix_hint: null,
        bin_found: true,
        weixin_configured: true,
        gateway_alive: true,
      }),
    );

    const weixinCard = await screen.findByTestId("platform-card-weixin");
    expect(weixinCard.className).toContain("border-ok/30"); // 绿描边(桥接探测通过)
    fireEvent.click(weixinCard);
    const detail = await screen.findByTestId("platform-detail");
    expect(within(detail).getByText("已连接")).toBeTruthy();
    const detailText = detail.textContent ?? "";
    // 已连接 → 目录速览出现,且 manual 平台空桶如实说明「无自动发现」
    expect(detailText).toContain("目录速览");
    expect(detailText).toContain("无自动发现");
    expect(detailText).toContain("channel_aliases.json");
  });

  it("bridge.status 失败(旧版 sidecar):降级灰态,不挡整屏目录视图", async () => {
    const sidecar = okSidecar(); // 无 bridge.status 处理器 → method_not_found
    installSidecar(sidecar.map, sidecar.record);
    render(
      <MemoryRouter>
        <MessagingScreen />
      </MemoryRouter>,
    );

    // 目录视图照常(通道目录区渲染 = 整屏未被探测失败拖挂)
    const feishu = await screen.findByTestId("platform-feishu");
    expect(within(feishu).getByText("AI中转站合伙人群")).toBeTruthy();
    const weixinCard = screen.getByTestId("platform-card-weixin");
    expect(weixinCard.className).toContain("border-border/60"); // 降级灰态
  });
});

// ---------------------------------------------------------------------------
// 告警规则子面板(10-04-alert-rules design §9/§11;契约 = design §4)
// ---------------------------------------------------------------------------

describe("告警规则:列表渲染与空态", () => {
  it("规则行:启停 Switch/名称/scope 徽章/when 等宽摘要/动作徽章(push→通道)/命中 N/最近触发", async () => {
    const sidecar = okSidecar();
    installSidecar(sidecar.map, sidecar.record);
    render(
      <MemoryRouter>
        <MessagingScreen />
      </MemoryRouter>,
    );

    const row = await screen.findByTestId("alert-rule-1");
    expect(within(row).getByText("竞对融资")).toBeTruthy();
    expect(within(row).getByText("全局")).toBeTruthy();
    expect(row.textContent).toContain("when '融资' in title"); // 等宽摘要含 when 前缀
    expect(within(row).getByText("推送 → feishu_card")).toBeTruthy(); // 动作徽章
    expect(row.textContent).toContain("命中 2");
    // 最近触发已本地化(不为 "—";格式随宿主 locale,只锚定年份)
    expect(row.textContent).toMatch(/最近触发 .*2026/);
    const toggle = within(row).getByRole("switch", { name: "启停 竞对融资" });
    expect(toggle.getAttribute("aria-checked")).toBe("true");
    // 未停用:无「已停用」徽标
    expect(within(row).queryByText("已停用")).toBeNull();
  });

  it("空表 = 合法零惊扰态:「还没有告警规则」空态 + 说明文案", async () => {
    const sidecar = okSidecar();
    sidecar.alertRules.rules = [];
    installSidecar(sidecar.map, sidecar.record);
    render(
      <MemoryRouter>
        <MessagingScreen />
      </MemoryRouter>,
    );
    expect(await screen.findByText("还没有告警规则")).toBeTruthy();
    expect(screen.getByText(/零惊扰/)).toBeTruthy();
  });
});

describe("告警规则:启停 = 全量提交(design §4.1 钉死①)", () => {
  it("点行内 Switch → alerts.save 提交完整数组(id 保稳,该行 enabled 翻转)", async () => {
    const sidecar = okSidecar();
    installSidecar(sidecar.map, sidecar.record);
    render(
      <MemoryRouter>
        <MessagingScreen />
      </MemoryRouter>,
    );

    const row = await screen.findByTestId("alert-rule-1");
    fireEvent.click(within(row).getByRole("switch", { name: "启停 竞对融资" }));

    // 载荷 = 完整规则数组,唯一变化 = 该行 enabled: true→false(无独立启停方法)
    expect(lastParams(sidecar.calls, "alerts.save")).toEqual({
      rules: [
        {
          id: 1,
          name: "竞对融资",
          enabled: false,
          scope: "global",
          when: "'融资' in title",
          action: "push",
          action_config: { channel: "feishu_card" },
        },
      ],
    });
    // 应答回传后:Switch 翻转 + 「已停用」徽标
    const toggled = await screen.findByTestId("alert-rule-1");
    await waitFor(() => {
      expect(within(toggled).getByRole("switch", { name: "启停 竞对融资" }).getAttribute("aria-checked")).toBe("false");
    });
    expect(within(toggled).getByText("已停用")).toBeTruthy();
  });

  it("启停失败(构造期错)→ 结构化错误如实呈现,不假装成功", async () => {
    const sidecar = okSidecar();
    sidecar.map["alerts.save"] = () => {
      throw JSON.stringify({
        code: "alert_rule_invalid",
        path: "params.rules[0].when",
        message: "字段校验失败: when 表达式不允许属性访问",
        data: { index: 0, field: "when", reason: "attribute_access" },
      });
    };
    installSidecar(sidecar.map, sidecar.record);
    render(
      <MemoryRouter>
        <MessagingScreen />
      </MemoryRouter>,
    );

    fireEvent.click(
      within(await screen.findByTestId("alert-rule-1")).getByRole("switch", { name: "启停 竞对融资" }),
    );
    await waitFor(() => {
      expect(screen.getByTestId("alert-rules-notice").textContent).toContain("alert_rule_invalid");
    });
    expect(screen.getByTestId("alert-rules-notice").textContent).toContain("字段校验失败");
  });
});

describe("告警规则:新建/编辑表单", () => {
  it("新建 push 规则:填表保存 → alerts.save 追加无 id 新条目;品类下拉 = yaml.list 派生", async () => {
    const sidecar = okSidecar();
    installSidecar(sidecar.map, sidecar.record);
    render(
      <MemoryRouter>
        <MessagingScreen />
      </MemoryRouter>,
    );

    await screen.findByTestId("alert-rule-1");
    fireEvent.click(screen.getByRole("button", { name: "新建规则" }));

    const form = screen.getByTestId("alert-rule-form");
    // scope 下拉:全局 + yaml.list 的品类(design §9:品类下拉 = yaml.list)
    const scopeSelect = within(form).getByLabelText("规则作用域") as HTMLSelectElement;
    const options = Array.from(scopeSelect.querySelectorAll("option")).map((option) => option.textContent);
    expect(options).toContain("全局(所有品类)");
    expect(options).toContain("消息屏夹具(messaging-demo)");

    fireEvent.change(within(form).getByLabelText("规则名称"), { target: { value: "高分项目" } });
    fireEvent.change(scopeSelect, { target: { value: "messaging-demo" } });
    fireEvent.change(within(form).getByLabelText("when 表达式"), {
      target: { value: "score >= 4" },
    });
    fireEvent.change(within(form).getByLabelText("推送通道"), { target: { value: "telegram" } });
    fireEvent.change(within(form).getByLabelText("推送对象"), { target: { value: "telegram:测试私聊" } });
    fireEvent.click(within(form).getByRole("button", { name: "保存规则" }));

    // 载荷:既有规则原样(id=1 保稳)+ 新条目(无 id,可选 targets 携带)
    expect(lastParams(sidecar.calls, "alerts.save")).toEqual({
      rules: [
        {
          id: 1,
          name: "竞对融资",
          enabled: true,
          scope: "global",
          when: "'融资' in title",
          action: "push",
          action_config: { channel: "feishu_card" },
        },
        {
          name: "高分项目",
          enabled: true,
          scope: "messaging-demo",
          when: "score >= 4",
          action: "push",
          action_config: { channel: "telegram", targets: ["telegram:测试私聊"] },
        },
      ],
    });
    // 保存成功:表单收起 + 新行入列(mock 全量替换语义回传)
    await waitFor(() => {
      expect(screen.getByTestId("alert-rules-notice").textContent).toContain("已保存");
    });
    expect(screen.queryByTestId("alert-rule-form")).toBeNull();
    expect(screen.getByTestId("alert-rule-2").textContent).toContain("高分项目");
  });

  it("新建 tag 规则:标签逗号分隔解析;targets/template 空则不携带", async () => {
    const sidecar = okSidecar();
    sidecar.alertRules.rules = [];
    installSidecar(sidecar.map, sidecar.record);
    render(
      <MemoryRouter>
        <MessagingScreen />
      </MemoryRouter>,
    );

    await screen.findByText("还没有告警规则");
    fireEvent.click(screen.getByRole("button", { name: "新建规则" }));
    const form = screen.getByTestId("alert-rule-form");
    fireEvent.change(within(form).getByLabelText("规则名称"), { target: { value: "免费羊毛" } });
    fireEvent.change(within(form).getByLabelText("when 表达式"), {
      target: { value: "'免费' in content" },
    });
    fireEvent.click(within(form).getByLabelText("打标"));
    fireEvent.change(within(form).getByLabelText("标签列表"), { target: { value: "羊毛, 限时, 白嫖" } });
    fireEvent.click(within(form).getByRole("button", { name: "保存规则" }));

    expect(lastParams(sidecar.calls, "alerts.save")).toEqual({
      rules: [
        {
          name: "免费羊毛",
          enabled: true,
          scope: "global",
          when: "'免费' in content",
          action: "tag",
          action_config: { tags: ["羊毛", "限时", "白嫖"] },
        },
      ],
    });
  });

  it("编辑预填原值;改 when 保存 → 全量提交该行 id 保留", async () => {
    const sidecar = okSidecar();
    installSidecar(sidecar.map, sidecar.record);
    render(
      <MemoryRouter>
        <MessagingScreen />
      </MemoryRouter>,
    );

    fireEvent.click(
      within(await screen.findByTestId("alert-rule-1")).getByRole("button", { name: "编辑" }),
    );
    const form = screen.getByTestId("alert-rule-form");
    expect(within(form).getByText("编辑规则(id=1)")).toBeTruthy();
    expect((within(form).getByLabelText("规则名称") as HTMLInputElement).value).toBe("竞对融资");
    expect((within(form).getByLabelText("when 表达式") as HTMLTextAreaElement).value).toBe("'融资' in title");
    expect((within(form).getByLabelText("推送通道") as HTMLSelectElement).value).toBe("feishu_card");

    fireEvent.change(within(form).getByLabelText("when 表达式"), {
      target: { value: "'融资' in title or 'financing' in content" },
    });
    fireEvent.click(within(form).getByRole("button", { name: "保存规则" }));

    const saved = lastParams(sidecar.calls, "alerts.save") as { rules: AlertRuleInput[] };
    expect(saved.rules).toHaveLength(1); // 编辑 = 替换该行,数组仍是全量
    expect(saved.rules[0]).toMatchObject({ id: 1, when: "'融资' in title or 'financing' in content" });
  });

  it("前端预检:名称/when/通道/标签缺省零提交,提示就地呈现", async () => {
    const sidecar = okSidecar();
    installSidecar(sidecar.map, sidecar.record);
    render(
      <MemoryRouter>
        <MessagingScreen />
      </MemoryRouter>,
    );

    await screen.findByTestId("alert-rule-1");
    fireEvent.click(screen.getByRole("button", { name: "新建规则" }));
    const form = screen.getByTestId("alert-rule-form");

    // 全空直接保存 → 名称预检拦截,零 alerts.save 调用
    fireEvent.click(within(form).getByRole("button", { name: "保存规则" }));
    expect(screen.getByTestId("alert-rules-notice").textContent).toContain("规则名称不能为空");
    expect(sidecar.calls.filter((call) => call.method === "alerts.save")).toHaveLength(0);

    // 名称有、when 空 → when 预检
    fireEvent.change(within(form).getByLabelText("规则名称"), { target: { value: "X" } });
    fireEvent.click(within(form).getByRole("button", { name: "保存规则" }));
    expect(screen.getByTestId("alert-rules-notice").textContent).toContain("when 表达式不能为空");

    // push 无通道 → 通道预检
    fireEvent.change(within(form).getByLabelText("when 表达式"), { target: { value: "score >= 4" } });
    fireEvent.click(within(form).getByRole("button", { name: "保存规则" }));
    expect(screen.getByTestId("alert-rules-notice").textContent).toContain("推送动作需选择通道");

    // tag 无标签 → 标签预检
    fireEvent.click(within(form).getByLabelText("打标"));
    fireEvent.click(within(form).getByRole("button", { name: "保存规则" }));
    expect(screen.getByTestId("alert-rules-notice").textContent).toContain("打标动作需至少一个标签");
    expect(sidecar.calls.filter((call) => call.method === "alerts.save")).toHaveLength(0);
  });

  it("坏 when 构造期拒(alerts.save)→ 结构化错直显(code/message),表单不收起", async () => {
    const sidecar = okSidecar();
    sidecar.map["alerts.save"] = () => {
      throw JSON.stringify({
        code: "alert_rule_invalid",
        path: "params.rules[1].when",
        message: "字段校验失败: when 表达式语法错误(title. 不允许属性访问)",
        data: { index: 1, field: "when", reason: "syntax" },
      });
    };
    installSidecar(sidecar.map, sidecar.record);
    render(
      <MemoryRouter>
        <MessagingScreen />
      </MemoryRouter>,
    );

    await screen.findByTestId("alert-rule-1");
    fireEvent.click(screen.getByRole("button", { name: "新建规则" }));
    const form = screen.getByTestId("alert-rule-form");
    fireEvent.change(within(form).getByLabelText("规则名称"), { target: { value: "坏表达式" } });
    fireEvent.change(within(form).getByLabelText("when 表达式"), {
      target: { value: "title.startswith('x')" },
    });
    fireEvent.change(within(form).getByLabelText("推送通道"), { target: { value: "stdout" } });
    fireEvent.click(within(form).getByRole("button", { name: "保存规则" }));

    // 构造期错直显(design §9:坏 when 结构化错误直显),整批零写入由服务端保证
    const notice = await screen.findByTestId("alert-rules-notice");
    expect(notice.textContent).toContain("alert_rule_invalid");
    expect(notice.textContent).toContain("属性访问");
    // 表单保持展开(草稿不丢)
    expect(screen.getByTestId("alert-rule-form")).toBeTruthy();
  });
});

describe("告警规则:测试按钮(alerts.test 真调,dry 求值)", () => {
  it("行内「测试」→ alerts.test({rule_id});结果面板:命中/actions 展开/already_fired", async () => {
    const sidecar = okSidecar();
    installSidecar(sidecar.map, sidecar.record);
    render(
      <MemoryRouter>
        <MessagingScreen />
      </MemoryRouter>,
    );

    fireEvent.click(
      within(await screen.findByTestId("alert-rule-1")).getByRole("button", { name: "测试" }),
    );
    expect(lastParams(sidecar.calls, "alerts.test")).toEqual({ rule_id: 1 });

    const panel = await screen.findByTestId("alert-test-result");
    await waitFor(() => {
      expect(panel.textContent).toContain("✓ 命中");
    });
    expect(panel.textContent).toContain("推送 → feishu_card");
    expect(panel.textContent).toContain("解析:messaging-demo push[0]"); // 通道解析结果
    expect(panel.textContent).toContain("已触发过"); // already_fired(该条已占坑去重)
  });

  it("表单草稿「测试(dry)」→ alerts.test({rule: 草稿});eval_error / muted 如实呈现", async () => {
    const sidecar = okSidecar();
    sidecar.map["alerts.test"] = () => ({
      matched: false,
      muted: true,
      actions: [],
      eval_error: "比较类型错: score 是 None(enrich 未启用)",
    });
    installSidecar(sidecar.map, sidecar.record);
    render(
      <MemoryRouter>
        <MessagingScreen />
      </MemoryRouter>,
    );

    await screen.findByTestId("alert-rule-1");
    fireEvent.click(screen.getByRole("button", { name: "新建规则" }));
    const form = screen.getByTestId("alert-rule-form");
    fireEvent.change(within(form).getByLabelText("规则名称"), { target: { value: "草稿" } });
    fireEvent.change(within(form).getByLabelText("when 表达式"), {
      target: { value: "score >= 4" },
    });
    fireEvent.change(within(form).getByLabelText("推送通道"), { target: { value: "stdout" } });
    fireEvent.click(within(form).getByRole("button", { name: "测试(dry)" }));

    // 草稿形态:rule 无 id,未保存即可测(design §4.1)
    const saved = lastParams(sidecar.calls, "alerts.test") as { rule?: { name: string; when: string } };
    expect(saved.rule).toMatchObject({ name: "草稿", when: "score >= 4" });

    const panel = await screen.findByTestId("alert-test-result");
    await waitFor(() => {
      expect(panel.textContent).toContain("when 求值错"); // eval_error 直显
    });
    expect(panel.textContent).toContain("mute 词表压制"); // muted 提示
    expect(panel.textContent).toContain("草稿"); // 面板标明草稿形态
  });

  it("测试失败(alert_test_no_item 空库)→ 结构化错误直显", async () => {
    const sidecar = okSidecar();
    sidecar.map["alerts.test"] = () => {
      throw JSON.stringify({
        code: "alert_test_no_item",
        path: "$",
        message: "没有可测条目:未提供 item/item_id 且条目库为空",
        data: {},
      });
    };
    installSidecar(sidecar.map, sidecar.record);
    render(
      <MemoryRouter>
        <MessagingScreen />
      </MemoryRouter>,
    );

    fireEvent.click(
      within(await screen.findByTestId("alert-rule-1")).getByRole("button", { name: "测试" }),
    );
    const panel = await screen.findByTestId("alert-test-result");
    await waitFor(() => {
      expect(panel.textContent).toContain("alert_test_no_item");
    });
    expect(panel.textContent).toContain("条目库为空");
  });
});

describe("告警规则:删除二次确认", () => {
  it("点删除出「确认删除」;取消零调用;确认 → alerts.delete({id}) 行消失", async () => {
    const sidecar = okSidecar();
    installSidecar(sidecar.map, sidecar.record);
    render(
      <MemoryRouter>
        <MessagingScreen />
      </MemoryRouter>,
    );

    const row = await screen.findByTestId("alert-rule-1");
    // 第一步:点删除只出二次确认,零调用
    fireEvent.click(within(row).getByRole("button", { name: "删除" }));
    expect(within(row).getByRole("button", { name: "确认删除" })).toBeTruthy();
    expect(sidecar.calls.filter((call) => call.method === "alerts.delete")).toHaveLength(0);

    // 取消:回到常规按钮,仍零调用
    fireEvent.click(within(row).getByRole("button", { name: "取消" }));
    expect(within(row).queryByRole("button", { name: "确认删除" })).toBeNull();
    expect(sidecar.calls.filter((call) => call.method === "alerts.delete")).toHaveLength(0);

    // 确认:alerts.delete({id:1}),行消失,notice 说明命中历史照留
    fireEvent.click(within(row).getByRole("button", { name: "删除" }));
    fireEvent.click(within(row).getByRole("button", { name: "确认删除" }));
    expect(lastParams(sidecar.calls, "alerts.delete")).toEqual({ id: 1 });
    await waitFor(() => {
      expect(screen.queryByTestId("alert-rule-1")).toBeNull();
    });
    expect(screen.getByTestId("alert-rules-notice").textContent).toContain("命中历史照留");
  });
});

describe("告警规则:alerts.fired 事件(事件流既有通道)", () => {
  it("fired 事件 → toast(notice)+ 规则行命中数 +1、最近触发刷新", async () => {
    const sidecar = okSidecar();
    installSidecar(sidecar.map, sidecar.record);
    render(
      <MemoryRouter>
        <MessagingScreen />
      </MemoryRouter>,
    );

    const row = await screen.findByTestId("alert-rule-1");
    expect(row.textContent).toContain("命中 2");

    emitSidecarEvent({
      type: "alerts.fired",
      rule_id: 1,
      rule_name: "竞对融资",
      item_id: 42,
      dedup_key: "https://example.com/a",
      title: "某公司完成 B 轮融资",
      action: "push",
      action_status: "sent",
      ts: "2026-10-04T03:00:00",
    });

    // toast:规则名 + 条目标题 + 动作终态(design §4.2 v1 消费)
    const notice = screen.getByTestId("alert-rules-notice");
    expect(notice.textContent).toContain("竞对融资");
    expect(notice.textContent).toContain("某公司完成 B 轮融资");
    expect(notice.textContent).toContain("sent");
    // 命中数刷新(本地增量,不整表重拉)+ 最近触发更新到事件 ts
    // (03:00 两种 12/24 小时制 locale 都含;原值 01:23 已被替换)
    const updated = screen.getByTestId("alert-rule-1");
    expect(updated.textContent).toContain("命中 3");
    expect(updated.textContent).toContain("03:00");
    // 零额外协议往返:命中刷新纯本地
    expect(sidecar.calls.filter((call) => call.method === "alerts.list").length).toBe(1);
  });

  it("非 alerts.fired 事件(如 completed)零影响", async () => {
    const sidecar = okSidecar();
    installSidecar(sidecar.map, sidecar.record);
    render(
      <MemoryRouter>
        <MessagingScreen />
      </MemoryRouter>,
    );

    const row = await screen.findByTestId("alert-rule-1");
    emitSidecarEvent({ type: "completed", run_id: 9, exit_code: 0, status: "ok", dry: false, ts: "2026-10-04T03:00:00" });
    expect(screen.queryByTestId("alert-rules-notice")).toBeNull();
    expect(screen.getByTestId("alert-rule-1").textContent).toContain("命中 2");
    expect(row).toBeTruthy();
  });
});

describe("告警规则:协议未实装降级与错误态", () => {
  it("旧版 sidecar(method_not_found)→ 子面板降级说明,不挡整屏目录视图", async () => {
    const sidecar = okSidecar();
    delete sidecar.map["alerts.list"]; // 旧版 sidecar 无 alerts.* → 结构化 404
    installSidecar(sidecar.map, sidecar.record);
    render(
      <MemoryRouter>
        <MessagingScreen />
      </MemoryRouter>,
    );

    // 目录视图照常(整屏未被拖挂)
    expect(await screen.findByTestId("platform-feishu")).toBeTruthy();
    const panel = await screen.findByTestId("alert-rules-unsupported");
    expect(panel.textContent).toContain("还没有告警规则方法");
    // 降级态不出新建按钮与列表
    expect(screen.queryByRole("button", { name: "新建规则" })).toBeNull();
    expect(screen.queryByTestId("alert-rule-1")).toBeNull();
  });

  it("alerts.list 真错误 → 局部错误 + 重试可用(不吞)", async () => {
    const sidecar = okSidecar();
    sidecar.map["alerts.list"] = () => {
      throw JSON.stringify({ code: "sidecar_not_running", path: "$", message: "sidecar 进程未运行" });
    };
    installSidecar(sidecar.map, sidecar.record);
    render(
      <MemoryRouter>
        <MessagingScreen />
      </MemoryRouter>,
    );

    const error = await screen.findByTestId("alert-rules-error");
    expect(error.textContent).toContain("sidecar_not_running");
    // 修好后再点重试 → 规则列表恢复
    sidecar.map["alerts.list"] = () => ({ rules: JSON.parse(JSON.stringify(sidecar.alertRules.rules)) });
    fireEvent.click(within(error).getByRole("button", { name: "重试" }));
    expect(await screen.findByTestId("alert-rule-1")).toBeTruthy();
  });
});
