// @vitest-environment jsdom
//
// 定时任务屏测试(10-04-cron-ui):mock 传输层(@tauri-apps/api/core invoke +
// api/event listen,messaging 形态;emitSidecarEvent 注入 cron.* 事件)。
// 用例 = research/screen-spec.md §5 #1-#19 全集(编号对应 AC;#18 logs 涟漪
// 落 logs-screen.test.tsx)+ Stage 1 骨架基线(空态/错误态/路由可达)。
// 协议契约权威:desktop/entry.py `_m_cron_*` + @/lib/api types.ts。
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
  it("/cron 路由可达:页头「定时任务」+ 侧栏导航项同屏可见", async () => {
    mockSidecar({ "cron.list": () => listResult([]), "cron.status": () => STATUS_OK });
    render(
      <MemoryRouter initialEntries={["/cron"]}>
        <App />
      </MemoryRouter>,
    );

    await waitFor(() => {
      expect(screen.getByRole("heading", { name: "定时任务" })).toBeTruthy();
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
    expect(normal.textContent).toContain("ticker 活跃");
    expect(normal.textContent).toContain("/h"); // Q3 数据根可见
    first.unmount();

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
