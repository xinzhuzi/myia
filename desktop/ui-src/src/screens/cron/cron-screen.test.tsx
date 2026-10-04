// @vitest-environment jsdom
//
// 定时任务屏测试(10-04-cron-ui):mock 传输层(@tauri-apps/api/core invoke +
// api/event listen,messaging 形态;emitSidecarEvent 注入 cron.* 事件)。
// 用例 = research/screen-spec.md §5 #1-#27 全集(编号对应 AC;#18 logs 涟漪
// 落 logs-screen.test.tsx;#20-#27 = Stage 6 蓝本对排缺口修复,G8 reload
// generation 守卫为代码审查项不设用例)+ Stage 1 骨架基线(空态/错误态/
// 路由可达)。协议契约权威:desktop/entry.py `_m_cron_*` + @/lib/api types.ts。
import { act, cleanup, fireEvent, render, screen, waitFor, within } from "@testing-library/react";
import { afterEach, beforeAll, beforeEach, describe, expect, it, vi } from "vitest";
import { MemoryRouter } from "react-router-dom";

const mocks = vi.hoisted(() => ({ invoke: vi.fn(), listen: vi.fn() }));
vi.mock("@tauri-apps/api/core", () => ({ invoke: mocks.invoke }));
vi.mock("@tauri-apps/api/event", () => ({ listen: mocks.listen }));

// jsdom 缺指针捕获/滚动 API(Radix Select trigger 的 onPointerDown 依赖
// hasPointerCapture;item 聚焦路径依赖 scrollIntoView)——最小 polyfill
beforeAll(() => {
  if (typeof Element.prototype.hasPointerCapture !== "function") {
    Element.prototype.hasPointerCapture = () => false;
  }
  if (typeof Element.prototype.releasePointerCapture !== "function") {
    Element.prototype.releasePointerCapture = () => undefined;
  }
  if (typeof Element.prototype.scrollIntoView !== "function") {
    Element.prototype.scrollIntoView = () => undefined;
  }
});

import App from "@/App";
import type {
  CronExecutionRow,
  CronJobRecord,
  CronListResult,
  CronStatusResult,
  HealthResult,
  PluginReport,
  YamlListResult,
} from "@/lib/api";
import { CronScreen } from "./cron-screen";

// ---------------------------------------------------------------------------
// 传输层假实现(invoke 按方法分发 + 事件捕获)
// ---------------------------------------------------------------------------

/** 已注册的 sidecar 事件 handler(供 emitSidecarEvent 注入;messaging 形态) */
const eventHandlers: Array<(payload: unknown) => void> = [];

/** 注入一条 sidecar 事件(client.ts listen 回调解包 event.payload 后进屏内
 *  handler —— 注入须按 Tauri 事件形态 {event, id, payload} 包装)。 */
function emitSidecarEvent(payload: unknown): void {
  for (const handler of [...eventHandlers]) {
    act(() => handler({ event: "sidecar://event", id: 1, payload }));
  }
}

/** invoke 按方法分发;handler 收 (params) 可带副作用(如排队后改内存 store) */
function mockSidecar(handlers: Record<string, (params: Record<string, unknown>) => unknown>): void {
  mocks.invoke.mockImplementation((_cmd: string, args: { method?: string; params?: Record<string, unknown> }) => {
    const handler = handlers[args?.method ?? ""];
    if (handler === undefined) {
      if (args?.method === "version") {
        return Promise.resolve({ name: "myssia", version: "1.0.0", protocol: 10 });
      }
      return Promise.reject(new Error(`测试未 mock 的方法:${args?.method}`));
    }
    return Promise.resolve(handler(args.params ?? {}));
  });
}

/** 取某方法已被 invoke 的 params 序列(断言调用形状) */
function invokedParams(method: string): Record<string, unknown>[] {
  return mocks.invoke.mock.calls
    .filter((call) => (call[1] as { method?: string }).method === method)
    .map((call) => ((call[1] as { params?: Record<string, unknown> }).params ?? {}));
}

/** Radix Select 交互配方(v2.1.4 实核):trigger 以 pointerType=mouse 的
 *  pointerDown 打开;item 上普通 click 即选择(handleSelect 有 disabled 守卫)。 */
function openSelect(trigger: HTMLElement): void {
  fireEvent.pointerDown(trigger, { button: 0, ctrlKey: false, pointerType: "mouse" });
}

// ---------------------------------------------------------------------------
// 协议夹具(形状逐字段对照 types.ts / entry.py `_m_cron_*` 应答载荷)
// ---------------------------------------------------------------------------

function cronJob(overrides: Partial<CronJobRecord> = {}): CronJobRecord {
  return {
    id: "a1b2c3d4e5f6",
    name: "早晚情报流",
    category: "/p/news.yaml",
    schedule: { kind: "cron", expr: "0 9 * * *", display: "every day 9am" },
    schedule_display: "every day 9am",
    repeat: { times: null, completed: 0 },
    enabled: true,
    state: "scheduled",
    paused_at: null,
    paused_reason: null,
    created_at: "2026-10-04T09:00:00+08:00",
    next_run_at: "2026-10-05T09:00:00+08:00",
    last_run_at: null,
    last_status: null,
    last_error: null,
    last_delivery_error: null,
    failure_streak: 0,
    deliver: "local",
    origin: { source: "desktop" },
    timezone: null,
    ...overrides,
  };
}

const STATUS_OK: CronStatusResult = {
  db: "/h/myssia.db",
  data_root: "/h",
  ticker_alive: true,
  heartbeat_age_seconds: 3,
  last_success_age_seconds: 60,
  last_error: null,
  estopped: false,
  jobs_total: 0,
  jobs_enabled: 0,
  next_due_at: "2026-10-05T09:00:00+08:00",
};

const STATUS_STALE: CronStatusResult = {
  ...STATUS_OK,
  ticker_alive: false,
  heartbeat_age_seconds: 900,
};

const STATUS_ESTOPPED: CronStatusResult = {
  ...STATUS_OK,
  estopped: true,
};

function listResult(jobs: CronJobRecord[]): CronListResult {
  return { db: "/h/myssia.db", data_root: "/h", count: jobs.length, jobs };
}

const YAML_LIST: YamlListResult = {
  plugins_dir: "/p",
  files: [
    {
      file: "/p/news.yaml",
      name: "news.yaml",
      parse_ok: true,
      category_id: "news",
      category_name: "新闻",
      sources: 3,
      error: null,
    },
    {
      file: "/p/broken.yaml",
      name: "broken.yaml",
      parse_ok: false,
      category_id: null,
      category_name: null,
      sources: null,
      error: { path: "$.sources[0]", code: "invalid_source", message: "源缺 url" },
    },
  ],
};

let confirmSpy: ReturnType<typeof vi.spyOn>;

beforeEach(() => {
  mocks.invoke.mockReset();
  mocks.listen.mockReset();
  eventHandlers.length = 0;
  mocks.listen.mockImplementation((name: string, handler: (event: unknown) => void) => {
    if (name === "sidecar://event") eventHandlers.push(handler);
    return Promise.resolve(() => {});
  });
  confirmSpy = vi.spyOn(window, "confirm").mockReturnValue(true);
});

afterEach(() => {
  cleanup();
  confirmSpy.mockRestore();
});

function renderScreen(): ReturnType<typeof render> {
  return render(
    <MemoryRouter>
      <CronScreen />
    </MemoryRouter>,
  );
}

/** 打开创建 Dialog 并等选择器清单就绪——必须等 trigger 解除 disabled
 *  (yaml.list 的 promise 落地渲染后)才返回:抢先 openSelect 会点在禁用
 *  trigger 上,下拉永不打开(#9 门禁首轮实炸的竞态面) */
async function openCreateDialog(): Promise<void> {
  fireEvent.click(await screen.findByTestId("cron-create-open"));
  await waitFor(() => {
    expect(invokedParams("yaml.list")).toHaveLength(1);
    expect((screen.getByTestId("cron-form-category") as HTMLButtonElement).disabled).toBe(false);
  });
}

/** 按名称单元格定位行(动作按钮作用域) */
function getByRowName(rows: HTMLElement, name: string): HTMLElement {
  const cell = within(rows).getByText(name);
  const row = cell.closest("tr");
  if (row === null) throw new Error(`找不到含「${name}」的行`);
  return row;
}

// ---------------------------------------------------------------------------
// Stage 1 基线:空态 / 错误态 / 路由可达
// ---------------------------------------------------------------------------

describe("CronScreen 基线(Stage 1)", () => {
  it("空库:挂载双拉 cron.list + cron.status,空态引导卡含 CLI 对照", async () => {
    mockSidecar({ "cron.list": () => listResult([]), "cron.status": () => STATUS_OK });
    renderScreen();

    expect(await screen.findByText("创建第一个定时任务")).toBeTruthy();
    expect(screen.getByText(/myssia cron list/)).toBeTruthy();
    const methods = mocks.invoke.mock.calls.map((call) => (call[1] as { method: string }).method);
    expect(methods).toContain("cron.list");
    expect(methods).toContain("cron.status");
  });

  it("拉取失败:ErrorBox 结构化错误(code 原文)+ 重试按钮", async () => {
    mockSidecar({ "cron.status": () => STATUS_OK });
    mocks.invoke.mockImplementation((_cmd: string, args: { method?: string }) => {
      if (args?.method === "cron.list") {
        return Promise.reject(
          JSON.stringify({ code: "store_corrupt", path: "$", message: "cron 账本不可读" }),
        );
      }
      return Promise.resolve(STATUS_OK);
    });
    renderScreen();

    const alertBox = await screen.findByRole("alert");
    expect(alertBox.textContent).toContain("cron 账本不可读");
    expect(alertBox.textContent).toContain("code=store_corrupt");
    expect(within(alertBox).getByRole("button", { name: /重试/ })).toBeTruthy();
  });
});

describe("路由接线(App.tsx /cron)", () => {
  it("/cron 路由可达(无头布局:PageHeader 返 null,以活性条为锚)", async () => {
    mockSidecar({ "cron.list": () => listResult([]), "cron.status": () => STATUS_OK });
    render(
      <MemoryRouter initialEntries={["/cron"]}>
        <App />
      </MemoryRouter>,
    );

    // 页头已删(d9ae353 无头):屏内首个可见锚 = 活性条 cron-vitality
    await waitFor(() => {
      expect(screen.getByTestId("cron-vitality")).toBeTruthy();
    });
    const nav = screen.getByRole("navigation", { name: "主导航" });
    expect(within(nav).getByRole("link", { name: "定时任务" })).toBeTruthy();
    expect(within(nav).getByRole("link", { name: "源管理" })).toBeTruthy();
  });
});

// ---------------------------------------------------------------------------
// screen-spec §5 #1-#12(编号对应 AC)
// ---------------------------------------------------------------------------

describe("#1 列表渲染:全字段(AC3)", () => {
  it("name/schedule_display/deliver/repeat 渲染;times null 显示 ∞", async () => {
    mockSidecar({
      "cron.list": () =>
        listResult([
          cronJob({
            name: "早晚情报流",
            schedule_display: "every day 9am",
            deliver: "feishu:ops群",
            repeat: { times: 5, completed: 2 },
          }),
          cronJob({
            id: "b2c3d4e5f6a7",
            name: "周报",
            schedule: { kind: "interval", minutes: 10080, display: "every 10080m" },
            schedule_display: "every 10080m",
            repeat: { times: null, completed: 0 },
          }),
        ]),
      "cron.status": () => STATUS_OK,
    });
    renderScreen();

    const rows = await screen.findByTestId("cron-job-rows");
    expect(within(rows).getByText("早晚情报流")).toBeTruthy();
    expect(within(rows).getByText("every day 9am")).toBeTruthy();
    expect(within(rows).getByText("feishu:ops群")).toBeTruthy();
    expect(within(rows).getByText("2/5")).toBeTruthy();
    expect(within(rows).getByText("0/∞")).toBeTruthy();
  });
});

describe("#2 四态 badge 色(AC3)", () => {
  it("ok→ok 类/failed→destructive/delivery_failed→warning/paused→中性", async () => {
    mockSidecar({
      "cron.list": () =>
        listResult([
          cronJob({ id: "j1", name: "甲", last_status: "ok" }),
          cronJob({ id: "j2", name: "乙", last_status: "failed", last_error: "boom" }),
          cronJob({ id: "j3", name: "丙", last_status: "delivery_failed" }),
          cronJob({ id: "j4", name: "丁", state: "paused", paused_at: "2026-10-04T09:00:00+08:00" }),
        ]),
      "cron.status": () => STATUS_OK,
    });
    renderScreen();

    await screen.findByTestId("cron-job-rows");
    expect(screen.getByText("成功").className).toContain("text-ok");
    expect(screen.getByText("失败").className).toContain("destructive");
    expect(screen.getByText("投递失败").className).toContain("text-warning");
    expect(screen.getByText("已暂停").className).toContain("bg-secondary");
  });
});

describe("#3 逾期红标边界(AC3)", () => {
  it("next=now-16min 红 / now-14min 不红 / paused 无标", async () => {
    const minutesAgo = (m: number) => new Date(Date.now() - m * 60_000).toISOString();
    mockSidecar({
      "cron.list": () =>
        listResult([
          cronJob({ id: "late16", name: "迟到十六", next_run_at: minutesAgo(16) }),
          cronJob({ id: "late14", name: "迟到十四", next_run_at: minutesAgo(14) }),
          cronJob({ id: "paused", name: "已暂停的", state: "paused", next_run_at: minutesAgo(30) }),
        ]),
      "cron.status": () => STATUS_OK,
    });
    renderScreen();

    await screen.findByTestId("cron-job-rows");
    const overdueMarks = screen.getAllByText("逾期");
    expect(overdueMarks).toHaveLength(1); // 16min 红、14min 宽限内、paused 无
    // 「逾期」标记 span 本体无类;红色在父级时间 span 上
    expect(overdueMarks[0]?.parentElement?.className).toContain("text-destructive");
    expect(screen.getByText("已暂停的").closest("tr")?.textContent).not.toContain("逾期");
  });
});

describe("#4 all 切换(AC3)", () => {
  it("开关打开后 list 携 all:true;终态行出现「已完结」", async () => {
    mockSidecar({
      "cron.list": (params) =>
        listResult(params.all === true ? [cronJob({ id: "done", name: "已完成的", state: "completed" })] : []),
      "cron.status": () => STATUS_OK,
    });
    renderScreen();

    await screen.findByText("创建第一个定时任务"); // 默认仅活跃 = 空
    fireEvent.click(screen.getByTestId("cron-all-switch"));

    await screen.findByText("已完结");
    const listCalls = invokedParams("cron.list");
    expect(listCalls[listCalls.length - 1]).toEqual({ all: true });
  });
});

describe("#5 活性条三态(AC2)", () => {
  it("正常灰字含 data_root;僵死黄条 cron-stale;急停红条 cron-estopped+恢复全部+注记", async () => {
    // 正常
    mockSidecar({ "cron.list": () => listResult([]), "cron.status": () => STATUS_OK });
    const first = renderScreen();
    const normal = await first.findByTestId("cron-vitality");
    expect(normal.textContent).toContain("调度器运行中");
    expect(normal.textContent).toContain("下次运行"); // 人话文案(r2:去 ticker/job 行话)
    expect(normal.textContent).toContain("数据目录 /h"); // Q3 数据根可见+带标签
    first.unmount();

    // 部分暂停:启用数/总数 形态(0/0 之外的 1/2 分数钉住)
    mockSidecar({
      "cron.list": () => listResult([]),
      "cron.status": () => ({ ...STATUS_OK, jobs_total: 2, jobs_enabled: 1 }),
    });
    const partial = renderScreen();
    const partialBar = await partial.findByTestId("cron-vitality");
    expect(partialBar.textContent).toContain("1/2 个任务启用");
    partial.unmount();

    // 僵死(heartbeat_age_seconds > 180 / ticker 不活)
    mockSidecar({ "cron.list": () => listResult([]), "cron.status": () => STATUS_STALE });
    const second = renderScreen();
    expect(await second.findByTestId("cron-stale")).toBeTruthy();
    second.unmount();

    // 急停
    mockSidecar({
      "cron.list": () => listResult([]),
      "cron.status": () => STATUS_ESTOPPED,
      "cron.resume": () => ({ estopped: false, cleared: true }),
    });
    const third = renderScreen();
    const estopBar = await third.findByTestId("cron-estopped");
    expect(estopBar.textContent).toContain("已急停");
    expect(estopBar.textContent).toContain("仅暂停调度"); // Q4 注记
    expect(within(estopBar).getByTestId("cron-resume-all")).toBeTruthy();
    // AC5 恢复全部调用形状:点击 → cron.resume {all:true}
    fireEvent.click(within(estopBar).getByTestId("cron-resume-all"));
    await waitFor(() => {
      expect(invokedParams("cron.resume")).toContainEqual({ all: true });
    });
    third.unmount();

    // 僵死判据第二支独立钉:ticker_alive:true 且 heartbeat_age_seconds=900
    // (>180)——防 cronTickerStale 退化成仅 !ticker_alive 也照绿
    mockSidecar({
      "cron.list": () => listResult([]),
      "cron.status": () => ({ ...STATUS_OK, ticker_alive: true, heartbeat_age_seconds: 900 }),
    });
    const fourth = renderScreen();
    expect(await fourth.findByTestId("cron-stale")).toBeTruthy();
    fourth.unmount();
  });
});

describe("#6 急停全部(AC5)", () => {
  it("红钮→确认 Dialog→invoke cron.pause {all:true}", async () => {
    mockSidecar({
      "cron.list": () => listResult([]),
      "cron.status": () => STATUS_OK,
      "cron.pause": () => ({ estopped: true, marker: "2026-10-04T10:00:00+08:00" }),
    });
    renderScreen();

    fireEvent.click(await screen.findByTestId("cron-estop-all"));
    expect(await screen.findByText("急停全部定时任务?")).toBeTruthy();
    fireEvent.click(screen.getByTestId("cron-estop-confirm"));

    await waitFor(() => {
      expect(invokedParams("cron.pause")).toContainEqual({ all: true });
    });
    expect((await screen.findByTestId("cron-notice")).textContent).toContain("已急停");
  });
});

describe("#7 创建提交形状(AC4)", () => {
  it("chips 点击→schedule;选择器选 parse_ok 项→category 绝对路径;全字段 payload", async () => {
    mockSidecar({
      "cron.list": () => listResult([]),
      "cron.status": () => STATUS_OK,
      "yaml.list": () => YAML_LIST,
      "cron.create": () => ({ job: cronJob() }),
    });
    renderScreen();
    await openCreateDialog();

    // chips 行:点击填 schedule 输入框
    fireEvent.click(screen.getByTestId("cron-chip-every monday 9am"));
    expect((screen.getByTestId("cron-form-schedule") as HTMLInputElement).value).toBe("every monday 9am");

    // 选择器:parse_ok 项 → category 绝对路径
    openSelect(screen.getByTestId("cron-form-category"));
    fireEvent.click(await screen.findByRole("option", { name: "新闻" }));

    // 高级折叠展开后补全字段
    fireEvent.click(screen.getByText(/高级选项/));
    fireEvent.change(screen.getByTestId("cron-form-deliver"), { target: { value: "feishu:ops" } });
    fireEvent.change(screen.getByTestId("cron-form-failureDeliver"), { target: { value: "feishu:alert" } });
    fireEvent.change(screen.getByTestId("cron-form-repeat"), { target: { value: "5" } });
    fireEvent.change(screen.getByTestId("cron-form-timezone"), { target: { value: "Asia/Shanghai" } });
    fireEvent.change(screen.getByTestId("cron-form-config"), { target: { value: "/p/pools.yaml" } });
    fireEvent.change(screen.getByTestId("cron-form-runTimeout"), { target: { value: "600" } });
    fireEvent.click(within(screen.getByText("dry-run(零持久化试跑)").parentElement!).getByRole("switch"));

    fireEvent.click(screen.getByTestId("cron-form-submit"));

    await waitFor(() => {
      expect(invokedParams("cron.create")).toEqual([
        {
          schedule: "every monday 9am",
          category: "/p/news.yaml",
          deliver: "feishu:ops",
          failure_deliver: "feishu:alert",
          timezone: "Asia/Shanghai",
          config: "/p/pools.yaml",
          repeat: 5,
          run_timeout: 600,
          dry_run: true,
        },
      ]);
    });
  });
});

describe("#8 创建错误回显(AC4)", () => {
  it("create 报 parse 错误→错误行含原文,Dialog 不关", async () => {
    mockSidecar({
      "cron.list": () => listResult([]),
      "cron.status": () => STATUS_OK,
      "yaml.list": () => YAML_LIST,
      "cron.create": () =>
        Promise.reject(
          JSON.stringify({
            code: "cron_create_failed",
            path: "params",
            message: "schedule 解析失败:未知形态「foo」",
          }),
        ),
    });
    renderScreen();
    await openCreateDialog();

    fireEvent.click(screen.getByTestId("cron-chip-0 9 * * *"));
    openSelect(screen.getByTestId("cron-form-category"));
    fireEvent.click(await screen.findByRole("option", { name: "新闻" }));
    fireEvent.click(screen.getByTestId("cron-form-submit"));

    const errorLine = await screen.findByTestId("cron-form-error");
    expect(errorLine.textContent).toContain("schedule 解析失败:未知形态「foo」");
    expect(screen.getByTestId("cron-form-schedule")).toBeTruthy(); // Dialog 未关
  });
});

describe("#9 选择器坏文件禁选(AC4)", () => {
  it("parse_ok:false 项 aria-disabled+「解析失败」;手输兜底可提交", async () => {
    mockSidecar({
      "cron.list": () => listResult([]),
      "cron.status": () => STATUS_OK,
      "yaml.list": () => YAML_LIST,
      "cron.create": () => ({ job: cronJob() }),
    });
    renderScreen();
    await openCreateDialog();

    openSelect(screen.getByTestId("cron-form-category"));
    const badOption = await screen.findByRole("option", { name: /解析失败/ });
    expect(badOption.getAttribute("aria-disabled")).toBe("true");
    expect(badOption.textContent).toContain("解析失败");

    // 手输兜底:末项「手输路径…」切换 input,提交带手输绝对路径
    fireEvent.click(screen.getByRole("option", { name: "手输路径…" }));
    fireEvent.change(await screen.findByTestId("cron-form-category-input"), {
      target: { value: "/p/manual.yaml" },
    });
    fireEvent.click(screen.getByTestId("cron-chip-30m"));
    fireEvent.click(screen.getByTestId("cron-form-submit"));

    await waitFor(() => {
      const created = invokedParams("cron.create");
      expect(created).toHaveLength(1);
      expect(created[0]).toMatchObject({ schedule: "30m", category: "/p/manual.yaml" });
    });
  });
});

describe("#10 编辑预填+部分更新(AC4)", () => {
  it("fromJob 预填;只改 deliver→edit 仅含 job+deliver", async () => {
    mockSidecar({
      "cron.list": () =>
        listResult([cronJob({ repeat: { times: 5, completed: 1 }, deliver: "local", timezone: null })]),
      "cron.status": () => STATUS_OK,
      "yaml.list": () => YAML_LIST,
      "cron.edit": () => ({ job: cronJob() }),
    });
    renderScreen();

    const rows = await screen.findByTestId("cron-job-rows");
    fireEvent.click(within(getByRowName(rows, "早晚情报流")).getByRole("button", { name: "编辑" }));
    await waitFor(() => {
      expect(invokedParams("yaml.list")).toHaveLength(1);
    });

    // 预填:schedule=expr 直读、deliver=local(高级折叠内)
    expect((screen.getByTestId("cron-form-schedule") as HTMLInputElement).value).toBe("0 9 * * *");
    fireEvent.click(screen.getByText(/高级选项/));
    expect((screen.getByTestId("cron-form-deliver") as HTMLInputElement).value).toBe("local");
    // dry_run 开关编辑态禁用(cron.edit 更新键集无此键——entry.py 4620-4637,
    // 可切不可交 = 误导 affordance;禁用后载荷必不含该键)
    const dryRunSwitch = within(screen.getByText("dry-run(零持久化试跑)", { exact: false }).parentElement!).getByRole("switch");
    expect((dryRunSwitch as HTMLButtonElement).disabled).toBe(true);

    // 只改 deliver → 部分更新载荷仅 job + deliver
    fireEvent.change(screen.getByTestId("cron-form-deliver"), { target: { value: "feishu:ops" } });
    fireEvent.click(screen.getByTestId("cron-form-submit"));

    await waitFor(() => {
      expect(invokedParams("cron.edit")).toEqual([{ job: "a1b2c3d4e5f6", deliver: "feishu:ops" }]);
    });
    expect(await screen.findByTestId("cron-notice")).toBeTruthy();
  });
});

describe("#11 动作四件(AC5)", () => {
  it("run/pause/resume invoke 形状;remove 先 window.confirm", async () => {
    mockSidecar({
      "cron.list": () =>
        listResult([cronJob({ id: "ja", name: "甲" }), cronJob({ id: "jb", name: "乙", state: "paused" })]),
      "cron.status": () => STATUS_OK,
      "cron.run": () => ({ job: cronJob() }),
      "cron.pause": () => ({ job: cronJob() }),
      "cron.resume": () => ({ job: cronJob() }),
      "cron.remove": () => ({ removed: true, job_id: "ja", name: "甲" }),
    });
    renderScreen();

    const rows = await screen.findByTestId("cron-job-rows");
    const rowA = getByRowName(rows, "甲");
    const rowB = getByRowName(rows, "乙");

    fireEvent.click(within(rowA).getByRole("button", { name: "运行" }));
    await waitFor(() => expect(invokedParams("cron.run")).toContainEqual({ job: "ja" }));

    fireEvent.click(within(rowA).getByRole("button", { name: "暂停" }));
    await waitFor(() =>
      expect(invokedParams("cron.pause")).toContainEqual({ job: "ja", reason: "桌面端手动暂停" }),
    );

    fireEvent.click(within(rowB).getByRole("button", { name: "恢复" }));
    await waitFor(() => expect(invokedParams("cron.resume")).toContainEqual({ job: "jb" }));

    // remove 先 window.confirm:拒绝 → 不发请求;同意 → cron.remove
    confirmSpy.mockReturnValue(false);
    fireEvent.click(within(rowA).getByRole("button", { name: "删除" }));
    expect(confirmSpy).toHaveBeenCalled();
    expect(invokedParams("cron.remove")).toHaveLength(0);

    confirmSpy.mockReturnValue(true);
    fireEvent.click(within(rowA).getByRole("button", { name: "删除" }));
    await waitFor(() => expect(invokedParams("cron.remove")).toContainEqual({ job: "ja" }));
  });
});

describe("#12 run 排队语义(AC5,grill 二 Q1)", () => {
  it("run 后 notice「已排队/≤60 秒」+行「已排队」态;completed 事件到刷新", async () => {
    let storeJob = cronJob();
    let listCallCount = 0;
    mockSidecar({
      "cron.list": () => {
        listCallCount += 1;
        return listResult([storeJob]);
      },
      "cron.status": () => STATUS_OK,
      "cron.run": () => {
        storeJob = { ...storeJob, manual_run_at: "2026-10-04T10:00:10+08:00" };
        return { job: storeJob };
      },
    });
    renderScreen();

    const rows = await screen.findByTestId("cron-job-rows");
    expect(screen.queryByText("已排队")).toBeNull();

    fireEvent.click(within(getByRowName(rows, "早晚情报流")).getByRole("button", { name: "运行" }));

    const notice = await screen.findByTestId("cron-notice");
    expect(notice.textContent).toContain("已排队");
    expect(notice.textContent).toContain("60 秒");
    expect(await screen.findByText("已排队")).toBeTruthy(); // 行短时排队态(manual_run_at 派生)

    // completed 事件到 → notice 翻新 + list 重拉
    const listCallsAtRun = listCallCount;
    emitSidecarEvent({
      type: "cron.completed",
      job_id: storeJob.id,
      name: storeJob.name,
      ok: true,
      status: "ok",
      delivery_error: null,
      summary: null,
      ts: "2026-10-04T10:00:40+08:00",
    });
    await waitFor(() => {
      expect(screen.getByTestId("cron-notice").textContent).toContain("完成");
    });
    // 「已排队」态随 completed 收讫清除——本 mock 的 store 刻意不 pop
    // manual_run_at(事件发射先于后端 mark_job_run,tick.py `_process_due_job`
    // 顺序),证明清态来自客户端收讫集合而非数据派生
    await waitFor(() => {
      expect(screen.queryByText("已排队")).toBeNull();
    });
    expect(listCallCount).toBeGreaterThan(listCallsAtRun);
  });
});

// ---------------------------------------------------------------------------
// screen-spec §5 #13-#17 + #19(Stage 4;#18 logs 涟漪在 logs-screen.test.tsx)
// ---------------------------------------------------------------------------

/** 执行账本行夹具(D10 摘要快照;形状对齐 CronExecutionRow/CronRunSummary;
 *  默认 partial 跑:退出码 3=部分成功 + 失败行,F6 全字段可见) */
function executionRow(overrides: Partial<CronExecutionRow> = {}): CronExecutionRow {
  return {
    id: "e1b2c3d4e5f6",
    job_id: "jx",
    source: "tick",
    status: "completed",
    scheduled_instant: "2026-10-04T09:00:00+08:00",
    pid: 12345,
    process_start_time: 1728000000.5,
    claimed_at: "2026-10-04T09:00:01+08:00",
    started_at: "2026-10-04T09:00:02+08:00",
    finished_at: "2026-10-04T09:05:15+08:00",
    error: null,
    run_summary: {
      job: { id: "jx", name: "有历史的", category: "/p/news.yaml" },
      run: {
        status: "partial",
        exit_code: 3,
        timed_out: false,
        run_id: 7,
        dry_run: false,
        duration_seconds: 12.3,
        error: null,
      },
      sources: { total: 3, ok: 2, failed: 1, items: 40 },
      items_retained: 12,
      push: [],
      failures: ["src-a · http_error · 连接超时"],
      failure_count: 1,
    },
    ...overrides,
  };
}

describe("#13 历史展开(AC6)", () => {
  it("首次展开 invoke runs{job,limit:10};摘要字段渲染;空态;折叠再展开不重拉", async () => {
    mockSidecar({
      "cron.list": () =>
        listResult([cronJob({ id: "jx", name: "有历史的" }), cronJob({ id: "jy", name: "没历史的" })]),
      "cron.status": () => STATUS_OK,
      "cron.runs": (params) =>
        params.job === "jx"
          ? { db: "/h/myssia.db", count: 1, executions: [executionRow()] }
          : { db: "/h/myssia.db", count: 0, executions: [] },
    });
    renderScreen();

    const rows = await screen.findByTestId("cron-job-rows");
    const expandX = within(getByRowName(rows, "有历史的")).getByRole("button", {
      name: /展开「有历史的」/,
    });
    expect(expandX.getAttribute("aria-expanded")).toBe("false");

    fireEvent.click(expandX);
    await waitFor(() => {
      expect(invokedParams("cron.runs")).toContainEqual({ job: "jx", limit: 10 });
    });
    expect(expandX.getAttribute("aria-expanded")).toBe("true");
    // 展开钮 aria-controls 指向真实 id(logs 屏 163/261 成对先例)
    expect(document.getElementById("cron-runs-jx")).not.toBeNull();
    const list = await screen.findByTestId("cron-runs-jx-list");
    expect(list.textContent).toContain("源 2/3"); // D10 摘要:源 ok/total
    expect(list.textContent).toContain("12.3s"); // 时长
    expect(list.textContent).toContain("留存 12"); // 条目留存
    expect(list.textContent).toContain("排程"); // source=tick 人话
    // F6:run 语义状态(partial → 部分成功 warning)+ 失败行 + finished_at 时刻
    expect(list.textContent).toContain("部分成功");
    expect(list.textContent).toContain("src-a · http_error · 连接超时");
    expect(list.textContent).toContain("10/04 09:05"); // = finished_at(非 claimed_at 09:00)

    // 空态:无执行行的 job
    fireEvent.click(within(getByRowName(rows, "没历史的")).getByRole("button", { name: /展开「没历史的」/ }));
    expect(await screen.findByText("暂无运行历史")).toBeTruthy();

    // 折叠再展开:惰性缓存,不重拉(ensureRuns 只首发)
    fireEvent.click(expandX); // 收起
    fireEvent.click(expandX); // 再展开
    expect(invokedParams("cron.runs").filter((params) => params.job === "jx")).toHaveLength(1);
  });
});

describe("#14 事件驱动(AC7)", () => {
  it("emitSidecarEvent(completed)→notice(name/status)+list 重拉", async () => {
    let listCalls = 0;
    mockSidecar({
      "cron.list": () => {
        listCalls += 1;
        return listResult([]);
      },
      "cron.status": () => STATUS_OK,
    });
    renderScreen();
    await screen.findByText("创建第一个定时任务");
    const before = listCalls;

    emitSidecarEvent({
      type: "cron.completed",
      job_id: "a1b2c3d4e5f6",
      name: "早晚情报流",
      ok: true,
      status: "partial",
      delivery_error: null,
      summary: null,
      ts: "2026-10-04T10:00:40+08:00",
    });

    const notice = await screen.findByTestId("cron-notice");
    expect(notice.textContent).toContain("早晚情报流");
    expect(notice.textContent).toContain("status=partial");
    await waitFor(() => {
      expect(listCalls).toBeGreaterThan(before);
    });
  });
});

describe("#15 skipped 事件(AC7)", () => {
  it("文案含「跳过」;重拉列表", async () => {
    let listCalls = 0;
    mockSidecar({
      "cron.list": () => {
        listCalls += 1;
        return listResult([]);
      },
      "cron.status": () => STATUS_OK,
    });
    renderScreen();
    await screen.findByText("创建第一个定时任务");
    const before = listCalls;

    emitSidecarEvent({
      type: "cron.skipped",
      job_id: "a1b2c3d4e5f6",
      name: "早晚情报流",
      reason: "run_busy",
      active_run_id: 7,
      ts: "2026-10-04T10:00:00+08:00",
    });

    const notice = await screen.findByTestId("cron-notice");
    expect(notice.textContent).toContain("跳过");
    expect(notice.textContent).toContain("早晚情报流");
    await waitFor(() => {
      expect(listCalls).toBeGreaterThan(before);
    });
  });
});

describe("#16 手动刷新(AC7)", () => {
  it("刷新按钮→list+status 双拉", async () => {
    let listCalls = 0;
    let statusCalls = 0;
    mockSidecar({
      "cron.list": () => {
        listCalls += 1;
        return listResult([]);
      },
      "cron.status": () => {
        statusCalls += 1;
        return STATUS_OK;
      },
    });
    renderScreen();
    await screen.findByTestId("cron-vitality"); // 首拉落地
    const beforeList = listCalls;
    const beforeStatus = statusCalls;

    fireEvent.click(screen.getByTestId("cron-refresh"));

    await waitFor(() => {
      expect(listCalls).toBe(beforeList + 1);
      expect(statusCalls).toBe(beforeStatus + 1);
    });
  });
});

describe("#17 零轮询(AC7)", () => {
  it("listen 只一次;1min 时钟 tick 零取数且驱动逾期标跨宽限线翻红(删 setInterval 即红)", async () => {
    vi.useFakeTimers();
    try {
      // 14.5min 前(15min 宽限内):tick 60s 后跨线翻红——证明逾期标随
      // 本地走时重算,而非只在取数时刷新
      const now = Date.now();
      mockSidecar({
        "cron.list": () =>
          listResult([cronJob({ name: "常驻的", next_run_at: new Date(now - 14.5 * 60_000).toISOString() })]),
        "cron.status": () => STATUS_OK,
      });
      renderScreen();
      await act(async () => {}); // 冲微任务:首拉落地(不依赖定时器)

      expect(screen.getByTestId("cron-job-rows")).toBeTruthy();
      expect(mocks.listen).toHaveBeenCalledTimes(1); // 事件订阅只一条,零轮询通道
      expect(screen.queryByText("逾期")).toBeNull(); // 宽限内不红

      const invokeCount = mocks.invoke.mock.calls.length;
      act(() => {
        vi.advanceTimersByTime(60_000); // 1min 时钟 tick(fake Date 同步走)
      });
      expect(mocks.invoke.mock.calls.length).toBe(invokeCount); // tick 零取数
      expect(screen.getByText("逾期")).toBeTruthy(); // 14.5+1 > 15min:跨线翻红
    } finally {
      vi.useRealTimers();
    }
  });
});

describe("#19 estopped 下单 job 操作(Q4;AC2/AC5)", () => {
  it("急停态仍可暂停/编辑单 job;红条含注记文案", async () => {
    mockSidecar({
      "cron.list": () => listResult([cronJob({ id: "jz", name: "急停中的" })]),
      "cron.status": () => STATUS_ESTOPPED,
      "cron.pause": () => ({ job: cronJob() }),
      "cron.edit": () => ({ job: cronJob() }),
    });
    renderScreen();

    const bar = await screen.findByTestId("cron-estopped");
    expect(bar.textContent).toContain("仅暂停调度"); // Q4 注记

    const rows = await screen.findByTestId("cron-job-rows");
    fireEvent.click(within(getByRowName(rows, "急停中的")).getByRole("button", { name: "暂停" }));
    await waitFor(() => {
      expect(invokedParams("cron.pause")).toContainEqual({ job: "jz", reason: "桌面端手动暂停" });
    });

    fireEvent.click(within(getByRowName(rows, "急停中的")).getByRole("button", { name: "编辑" }));
    expect(await screen.findByTestId("cron-form-schedule")).toBeTruthy(); // 编辑 Dialog 可开
  });
});

// ---------------------------------------------------------------------------
// screen-spec §5 #20-#27(Stage 6 蓝本对排缺口修复;G8 = 代码审查项不设用例)
// ---------------------------------------------------------------------------

describe("#20 error 态 badge(G1;AC3)", () => {
  it("state=error → destructive「已停摆」+ title 含 last_error;优先于 last_status 派生", async () => {
    mockSidecar({
      "cron.list": () =>
        listResult([
          // last_status=ok 若不被抢占会渲染「成功」(ok 色)——抢占序证明
          cronJob({
            id: "jer",
            name: "停摆的",
            state: "error",
            last_status: "ok",
            last_error: "recurring 算不出下次运行时刻",
          }),
        ]),
      "cron.status": () => STATUS_OK,
    });
    renderScreen();

    const rows = await screen.findByTestId("cron-job-rows");
    const stopped = within(rows).getByText("已停摆");
    expect(stopped.className).toContain("destructive"); // H530 error→destructive 对位
    expect(stopped.title).toContain("recurring 算不出下次运行时刻"); // H1158-1166 title 悬浮细节
    expect(within(rows).queryByText("成功")).toBeNull(); // 优先于 last_status 派生
  });
});

describe("#21 错误红行(G2b;AC3)", () => {
  it("last_error/last_delivery_error 有值→行下红字两行且截 120;无值不渲染行", async () => {
    const longError = "连".repeat(200);
    mockSidecar({
      "cron.list": () =>
        listResult([
          cronJob({
            id: "jerr",
            name: "带错的",
            last_error: longError,
            last_delivery_error: "feishu 410 gone",
          }),
          cronJob({ id: "jok", name: "干净的" }),
        ]),
      "cron.status": () => STATUS_OK,
    });
    renderScreen();

    const rows = await screen.findByTestId("cron-job-rows");
    const lastErr = within(rows).getByText(/上次错误:/);
    expect(lastErr.textContent).toBe(`上次错误:${"连".repeat(120)}...`); // 截 120 + ...
    expect(lastErr.closest("td")?.className).toContain("text-destructive");
    const deliveryErr = within(rows).getByText(/投递错误:/);
    expect(deliveryErr.textContent).toBe("投递错误:feishu 410 gone"); // 短文原样
    expect(deliveryErr.closest("td")?.getAttribute("colspan")).toBe("9"); // 九列契约

    // 无值不渲染:干净行(末行)之后无错误行
    const cleanRow = getByRowName(rows, "干净的");
    expect(cleanRow.nextElementSibling?.textContent ?? "").not.toContain("错误:");
  });
});

describe("#22 上次运行列(G2a;AC3)", () => {
  it("last_run_at 有值本地化渲染 / 空 = 「—」;列位在「下次运行」后", async () => {
    mockSidecar({
      "cron.list": () =>
        listResult([
          cronJob({ id: "jran", name: "跑过的", last_run_at: "2026-10-04T09:05:15+08:00" }),
          cronJob({ id: "jnew", name: "没跑过的", last_run_at: null }),
        ]),
      "cron.status": () => STATUS_OK,
    });
    renderScreen();

    const rows = await screen.findByTestId("cron-job-rows");
    expect(screen.getByRole("columnheader", { name: "上次运行" })).toBeTruthy();
    const ranRow = getByRowName(rows, "跑过的");
    expect(within(ranRow).getByText("10/04 09:05")).toBeTruthy(); // 本地化 MM-DD HH:mm
    // 列位:cells[3]=下次运行(10/05 09:00)、cells[4]=上次运行(10/04 09:05)
    const ranCells = (ranRow as HTMLTableRowElement).cells;
    expect(ranCells[3]?.textContent).toContain("10/05 09:00");
    expect(ranCells[4]?.textContent).toContain("10/04 09:05");
    const newRow = getByRowName(rows, "没跑过的") as HTMLTableRowElement;
    expect(newRow.cells[4]?.textContent).toBe("—"); // 空 = 「—」
  });
});

describe("#23 name 表单(G3;AC4)", () => {
  it("创建可命名(payload 含 name);留空不带键;编辑改名入 diff", async () => {
    mockSidecar({
      "cron.list": () => listResult([cronJob()]),
      "cron.status": () => STATUS_OK,
      "yaml.list": () => YAML_LIST,
      "cron.create": () => ({ job: cronJob() }),
      "cron.edit": () => ({ job: cronJob() }),
    });
    renderScreen();
    await screen.findByTestId("cron-job-rows");

    // 创建可命名:name 输入(主字段组最上)+ chips + 选择器 → payload 含 name
    await openCreateDialog();
    fireEvent.change(screen.getByTestId("cron-form-name"), { target: { value: "我的任务" } });
    fireEvent.click(screen.getByTestId("cron-chip-30m"));
    openSelect(screen.getByTestId("cron-form-category"));
    fireEvent.click(await screen.findByRole("option", { name: "新闻" }));
    fireEvent.click(screen.getByTestId("cron-form-submit"));
    await waitFor(() => {
      expect(invokedParams("cron.create")[0]).toMatchObject({ name: "我的任务" });
    });
    await waitFor(() => {
      expect(screen.queryByTestId("cron-form-submit")).toBeNull(); // Dialog 关闭收口
    });

    // 留空不带键(optionalParam = undefined;后端 _cron_opt_str 空串即拒)
    await openCreateDialog();
    fireEvent.click(screen.getByTestId("cron-chip-30m"));
    openSelect(screen.getByTestId("cron-form-category"));
    fireEvent.click(await screen.findByRole("option", { name: "新闻" }));
    fireEvent.click(screen.getByTestId("cron-form-submit"));
    await waitFor(() => {
      expect(invokedParams("cron.create")).toHaveLength(2);
    });
    expect(invokedParams("cron.create")[1]?.name).toBeUndefined();
    await waitFor(() => {
      expect(screen.queryByTestId("cron-form-submit")).toBeNull(); // Dialog 关闭收口
    });

    // 编辑改名入 diff:预填旧名,只改 name → 载荷仅 job+name
    fireEvent.click(within(getByRowName(screen.getByTestId("cron-job-rows"), "早晚情报流")).getByRole("button", { name: "编辑" }));
    await waitFor(() => {
      expect(invokedParams("yaml.list")).toHaveLength(2);
    });
    expect((screen.getByTestId("cron-form-name") as HTMLInputElement).value).toBe("早晚情报流"); // fromJob 预填
    fireEvent.change(screen.getByTestId("cron-form-name"), { target: { value: "新名字" } });
    fireEvent.click(screen.getByTestId("cron-form-submit"));
    await waitFor(() => {
      expect(invokedParams("cron.edit")).toEqual([{ job: "a1b2c3d4e5f6", name: "新名字" }]);
    });
  });
});

describe("#24 错误保留旧列表(G4;AC3/AC7)", () => {
  it("reload 失败→ErrorBox 出现且旧表行仍在(错误条+旧表共存)", async () => {
    let failList = false;
    mockSidecar({
      "cron.list": () => {
        if (failList) {
          return Promise.reject(
            JSON.stringify({ code: "internal_error", path: "$", message: "重拉失败 boom" }),
          );
        }
        return listResult([cronJob({ id: "jkeep", name: "旧表还在的" })]);
      },
      "cron.status": () => STATUS_OK,
    });
    renderScreen();
    await screen.findByText("旧表还在的");

    failList = true;
    fireEvent.click(screen.getByTestId("cron-refresh"));

    const alertBox = await screen.findByRole("alert"); // ErrorBox(H629 错误条)
    expect(alertBox.textContent).toContain("重拉失败 boom");
    expect(screen.getByText("旧表还在的")).toBeTruthy(); // 旧表共存,未被清空
  });
});

describe("#25 列表计数(G5;AC3)", () => {
  it("工具行「共 N 个」=当前行数;all 开关联动", async () => {
    const active = [cronJob({ id: "ja", name: "甲" }), cronJob({ id: "jb", name: "乙" })];
    const withPaused = [...active, cronJob({ id: "jc", name: "丙", state: "paused" })];
    mockSidecar({
      "cron.list": (params) => listResult(params.all === true ? withPaused : active),
      "cron.status": () => STATUS_OK,
    });
    renderScreen();

    await screen.findByTestId("cron-job-rows");
    expect(screen.getByTestId("cron-job-count").textContent).toBe("共 2 个");

    fireEvent.click(screen.getByTestId("cron-all-switch"));
    await waitFor(() => {
      expect(screen.getByTestId("cron-job-count").textContent).toBe("共 3 个"); // H1092 ({jobs.length}) 对位
    });
  });
});

describe("#26 校验聚焦(G6;AC4)", () => {
  it("缺 schedule→对应 input 获焦;错误字段在高级折叠→先展开再聚焦", async () => {
    mockSidecar({
      "cron.list": () => listResult([]),
      "cron.status": () => STATUS_OK,
      "yaml.list": () => YAML_LIST,
      "cron.create": () => ({ job: cronJob() }),
    });
    renderScreen();
    await openCreateDialog();

    // 缺 schedule:错误行 + schedule input 获焦(HJ 77-85 focusCronField)
    fireEvent.click(screen.getByTestId("cron-form-submit"));
    expect(screen.getByTestId("cron-form-error").textContent).toContain("排程必填");
    await waitFor(() => {
      expect(document.activeElement?.id).toBe("cron-create-schedule");
    });

    // 高级折叠内字段(repeat 非整数):填坏后收起折叠再提交 → 先展开再聚焦
    fireEvent.click(screen.getByTestId("cron-chip-30m"));
    openSelect(screen.getByTestId("cron-form-category"));
    fireEvent.click(await screen.findByRole("option", { name: "新闻" }));
    const advancedToggle = screen.getByText(/高级选项/).closest("button")!;
    fireEvent.click(advancedToggle); // 展开
    fireEvent.change(screen.getByTestId("cron-form-repeat"), { target: { value: "abc" } });
    fireEvent.click(advancedToggle); // 收起
    expect(advancedToggle.getAttribute("aria-expanded")).toBe("false");

    fireEvent.click(screen.getByTestId("cron-form-submit"));
    expect(screen.getByTestId("cron-form-error").textContent).toContain("repeat 必须为整数");
    await waitFor(() => {
      expect(advancedToggle.getAttribute("aria-expanded")).toBe("true"); // 先展开
      expect(document.activeElement?.id).toBe("cron-create-repeat"); // 再聚焦
    });
  });
});

describe("#27 编辑示 id(G7;AC4)", () => {
  it("编辑 Dialog footer 含 font-mono job.id;create 不示", async () => {
    mockSidecar({
      "cron.list": () => listResult([cronJob()]),
      "cron.status": () => STATUS_OK,
      "yaml.list": () => YAML_LIST,
    });
    renderScreen();

    const rows = await screen.findByTestId("cron-job-rows");
    fireEvent.click(within(getByRowName(rows, "早晚情报流")).getByRole("button", { name: "编辑" }));
    const idSpan = await screen.findByTestId("cron-edit-job-id"); // H1065-1068 对位
    expect(idSpan.textContent).toBe("a1b2c3d4e5f6");
    expect(idSpan.className).toContain("font-mono");
  });
});

// ---------------------------------------------------------------------------
// 排程一览 + 品类行「跑一次」(2026-10-05 自源管理屏迁入;主人质疑
// 「排程一览是什么意思?没在定时任务里面?」——排程语义归位 cron 屏):
// 逐品类 schedule.preview 并发预览(单品类失败只塌该行)+ 行尾 run.start
// 单飞(completed 事件按 run_id 对账收尾)。用例自 sources.test.tsx 迁移,
// 适配点:数据面经 health 取品类清单;终态不 reload(本屏无健康度面)。
// ---------------------------------------------------------------------------

const SCHED_FILE = "plugins/ai-news.yaml";

/** 品类夹具(排程一览只吃 plugins 层,sources 一律空) */
function schedPlugin(file: string, id: string, schedule: string | null): PluginReport {
  return {
    file,
    id,
    name: `品类 ${id}`,
    schedule,
    timezone: "Asia/Shanghai",
    push_channels: [],
    loaded: true,
    load_errors: null,
    sources: [],
  };
}

function schedHealth(plugins: PluginReport[]): HealthResult {
  return {
    command: "list",
    plugins_dir: "plugins",
    db: "myssia.db",
    store_error: null,
    plugins,
    summary: { plugins: plugins.length, sources: 0, ok: 0, degraded: 0, dead: 0, unknown: 0 },
    healthy: true,
    exit_code: 0,
  };
}

describe("排程一览(自源管理迁入)", () => {
  it("屏底逐品类出 schedule/timezone 原文 + 未来时刻行;无排程品类明示「无排程」", async () => {
    mockSidecar({
      "cron.list": () => listResult([]),
      "cron.status": () => STATUS_OK,
      health: () =>
        schedHealth([
          schedPlugin(SCHED_FILE, "ai-news", "*/15 * * * *"),
          schedPlugin("plugins/nosched.yaml", "nosched", null),
        ]),
      "schedule.preview": (params) => {
        const { file } = params as { file: string };
        if (file.endsWith("nosched.yaml")) {
          return { file, schedule: null, timezone: null, runs: [] };
        }
        return {
          file,
          schedule: "*/15 * * * *",
          timezone: "Asia/Shanghai",
          runs: ["2026-10-03T09:00:00+08:00", "2026-10-03T09:15:00+08:00"],
        };
      },
    });
    renderScreen();

    const overview = await screen.findByTestId("schedule-overview");
    expect(overview.textContent).toContain("排程一览");
    // schedule 原文 + 时区 + 本地化时刻
    const row = screen.getByTestId(`schedule-row-${SCHED_FILE}`);
    expect(row.textContent).toContain("*/15 * * * *");
    expect(row.textContent).toContain("Asia/Shanghai");
    expect(row.textContent).toContain("09:00");
    // 无排程品类明示,不是错误
    const nosched = screen.getByTestId("schedule-row-plugins/nosched.yaml");
    expect(nosched.textContent).toContain("无排程");
    // 预览请求逐品类发出,且带 count(缺省 5)
    expect(invokedParams("schedule.preview")).toContainEqual({ file: SCHED_FILE, count: 5 });
    expect(invokedParams("schedule.preview")).toContainEqual({ file: "plugins/nosched.yaml", count: 5 });
  });

  it("单品类预览失败只塌该行(预览失败徽标 + code),整区仍出", async () => {
    mockSidecar({
      "cron.list": () => listResult([]),
      "cron.status": () => STATUS_OK,
      health: () =>
        schedHealth([schedPlugin(SCHED_FILE, "ai-news", "0 9 * * *"), schedPlugin("plugins/bad.yaml", "bad", null)]),
      "schedule.preview": (params) => {
        const { file } = params as { file: string };
        if (file.endsWith("bad.yaml")) {
          throw JSON.stringify({
            code: "source_file_unreadable",
            path: "params.file",
            message: "品类 YAML 装不上: invalid_cron",
          });
        }
        return { file, schedule: "0 9 * * *", timezone: null, runs: ["2026-10-04T09:00:00+08:00"] };
      },
    });
    renderScreen();

    const badRow = await screen.findByTestId("schedule-row-plugins/bad.yaml");
    expect(badRow.textContent).toContain("预览失败");
    expect(badRow.textContent).toContain("source_file_unreadable");
    // 好品类照常出(allSettled 不塌整区)
    expect(screen.getByTestId(`schedule-row-${SCHED_FILE}`).textContent).toContain("0 9 * * *");
  });

  it("空品类目录:排程一栏给空态引导文案", async () => {
    mockSidecar({
      "cron.list": () => listResult([]),
      "cron.status": () => STATUS_OK,
      health: () => schedHealth([]),
    });
    renderScreen();

    const overview = await screen.findByTestId("schedule-overview");
    expect(overview.textContent).toContain("没有品类 YAML");
  });

  it("排程行 Trigger 钮发起 run.start(yaml=品类文件)→ completed 按 run_id 对账收尾", async () => {
    mockSidecar({
      "cron.list": () => listResult([]),
      "cron.status": () => STATUS_OK,
      health: () =>
        schedHealth([schedPlugin(SCHED_FILE, "ai-news", "*/15 * * * *"), schedPlugin("plugins/weekly.yaml", "weekly", null)]),
      "schedule.preview": (params) => {
        const { file } = params as { file: string };
        return { file, schedule: "*/15 * * * *", timezone: "Asia/Shanghai", runs: ["2026-10-04T09:00:00+08:00"] };
      },
      "run.start": (params) => {
        const { yaml } = params as { yaml: string };
        return { run_id: 31, state: "running", yaml, dry: false, db: "myssia.db" };
      },
    });
    renderScreen();

    // 每行品类(含无源品类)行尾各有 Trigger 钮
    const trigger = await screen.findByRole("button", { name: "跑一次:品类 ai-news" });
    expect(screen.getByRole("button", { name: "跑一次:品类 weekly" })).toBeTruthy();

    fireEvent.click(trigger);
    await waitFor(() => expect(invokedParams("run.start")).toContainEqual({ yaml: SCHED_FILE }));
    // 进行中横幅(人话+日志屏深链;run_id 类行话不上活性面)+ run 单飞:全区品类行 Trigger 禁点
    const running = await screen.findByTestId("run-once-running");
    expect(running.textContent).toContain("品类 ai-news");
    expect(running.textContent).not.toContain("run #");
    expect(running.querySelector("a")?.getAttribute("href")).toBe("#/logs");
    expect((screen.getByRole("button", { name: "跑一次:品类 ai-news" }) as HTMLButtonElement).disabled).toBe(true);
    expect((screen.getByRole("button", { name: "跑一次:品类 weekly" }) as HTMLButtonElement).disabled).toBe(true);

    // 串台防护:别的入口发起的 run(run_id=99)completed 不抢收
    emitSidecarEvent({ type: "completed", run_id: 99, exit_code: 0, status: "success", dry: false, ts: "2026-10-04T09:00:00+00:00" });
    expect(screen.getByTestId("run-once-running")).toBeTruthy();

    emitSidecarEvent({ type: "completed", run_id: 31, exit_code: 0, status: "success", dry: false, ts: "2026-10-04T09:01:00+00:00" });
    // 终态 → 模态详情弹窗(10-05-run-once-result-dialog;贴顶终态横幅已撤)
    const done = await screen.findByTestId("run-once-dialog");
    expect(done.getAttribute("role")).toBe("dialog");
    expect(done.getAttribute("aria-modal")).toBe("true");
    expect(done.textContent).toContain("跑一次结果 · 品类 ai-news");
    expect(screen.getByTestId("run-once-status").textContent).toBe("成功");
    // trace 值收技术小字(弹窗内可见,活性面无)
    expect(done.textContent).toContain("status=success");
    expect(done.textContent).toContain("run_id=31");
    expect(screen.getByRole("link", { name: "查看采集日志" }).getAttribute("href")).toBe("#/logs");
    expect(screen.queryByTestId("run-once-running")).toBeNull();
    // 单飞解除:按钮回可用
    expect((screen.getByRole("button", { name: "跑一次:品类 ai-news" }) as HTMLButtonElement).disabled).toBe(false);

    // 关闭弹窗 → 终态清除,不残留
    fireEvent.click(screen.getByRole("button", { name: "关闭" }));
    await waitFor(() => {
      expect(screen.queryByTestId("run-once-dialog")).toBeNull();
    });
  });

  it("发起被拒(run_busy)→ 弹窗失败形按钮回可用;failed 终态如实失败分级不伪装成功", async () => {
    let reject = true;
    mockSidecar({
      "cron.list": () => listResult([]),
      "cron.status": () => STATUS_OK,
      health: () => schedHealth([schedPlugin(SCHED_FILE, "ai-news", "*/15 * * * *")]),
      "schedule.preview": (params) => {
        const { file } = params as { file: string };
        return { file, schedule: "*/15 * * * *", timezone: "Asia/Shanghai", runs: ["2026-10-04T09:00:00+08:00"] };
      },
      "run.start": () => {
        if (reject) {
          throw JSON.stringify({
            code: "run_busy",
            path: "$",
            message: "已有 run 在执行 run_id=8(单飞)",
            data: { active_run_id: 8 },
          });
        }
        return { run_id: 32, state: "running", yaml: SCHED_FILE, dry: false, db: "myssia.db" };
      },
    });
    renderScreen();

    fireEvent.click(await screen.findByRole("button", { name: "跑一次:品类 ai-news" }));
    const busy = await screen.findByTestId("run-once-dialog");
    expect(busy.textContent).toContain("发起失败:run_busy");
    expect(busy.textContent).toContain("已有 run 在执行");
    expect(screen.getByTestId("run-once-status").textContent).toBe("发起失败");
    // 拒绝不滞留:关闭弹窗即可重试,按钮始终可用
    expect((screen.getByRole("button", { name: "跑一次:品类 ai-news" }) as HTMLButtonElement).disabled).toBe(false);

    // 关闭失败弹窗 → 重试发起成功;failed 终态(exit=2)弹窗如实分级
    fireEvent.click(screen.getByRole("button", { name: "关闭" }));
    await waitFor(() => {
      expect(screen.queryByTestId("run-once-dialog")).toBeNull();
    });
    reject = false;
    fireEvent.click(screen.getByRole("button", { name: "跑一次:品类 ai-news" }));
    await screen.findByTestId("run-once-running");
    emitSidecarEvent({ type: "completed", run_id: 32, exit_code: 2, status: "failed", dry: false, ts: "2026-10-04T09:02:00+00:00" });
    const fail = await screen.findByTestId("run-once-dialog");
    expect(screen.getByTestId("run-once-status").textContent).toBe("失败");
    expect(fail.textContent).toContain("status=failed");
    expect(fail.textContent).toContain("exit 2");
  });
});
