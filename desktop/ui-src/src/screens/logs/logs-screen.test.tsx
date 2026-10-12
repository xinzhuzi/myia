// @vitest-environment jsdom
/**
 * 采集日志组件测试(10-12-logs-two-level-ui:两级 IA 重写)—— mock sidecar
 * (vi.mock "@/lib/api":run.status / logs.tail / run.start 返回夹具;
 * onSidecarEvent 捕获处理器以注入 log/progress/completed 事件)。
 * 断言面随信息架构重写(design §8;jsdom 无真实布局,布局断言归无头冒烟):
 * L1 摘要行派生(summarizeRun 分状态段/accordion 退役哨兵)/ 切级动线(点行
 * 惰性拉 tail · 返回钮 · Esc 全局链 · 缓存不重拉)/ 默认不自动跳级 / 过滤态
 * 穿越保持 / 失败原因区(三源合成四象限 + 无据如实文案 + 永假在途态拦下)/
 * L2 元信息头(绝对起止/exit 语义映射/会话对齐号/行数-错误行数)/ 日志体
 * (错误行 dead 高亮与级别着色/搜索过滤高亮计数/框内 Esc 清词)/ 流式续播
 * (事件归组缓冲-进 L2 合并/completed 刷新)/ 重跑(L1/L2 双可达,triggered
 * 词面去「展开跟随」)/ 结构化错误横幅两级可见 / 空态 / 「上一程」历史行全家族。
 * 夹具层复用现状(run2Running/run1Success/histRun5/tail 五行/事件夹具),仅按
 * wire 真形增补:pipeline.py:592 stats.sources 数组(success 行全健康;
 * failed 注册表行内造一例 failed:true 成员)——喂摘要源段/失败段。
 */
import { act, cleanup, fireEvent, render, screen, waitFor, within } from "@testing-library/react";
import { afterEach, beforeAll, describe, expect, it, vi } from "vitest";

import { SidecarRequestError } from "@/lib/api";
import type {
  AlertsFiredEvent,
  CronCompletedEvent,
  CronSkippedEvent,
  RunEntry,
  SidecarEvent,
} from "@/lib/api";

const harness = vi.hoisted(() => ({
  handler: null as null | ((event: SidecarEvent) => void),
  unlisten: vi.fn(),
}));

vi.mock("@/lib/api", async (importOriginal) => {
  const actual = await importOriginal<typeof import("@/lib/api")>();
  return {
    ...actual,
    api: {
      ...actual.api,
      runStatus: vi.fn(),
      logsTail: vi.fn(),
      runStart: vi.fn(),
      storeItems: vi.fn(),
    },
    onSidecarEvent: vi.fn((handler: (event: SidecarEvent) => void) => {
      harness.handler = handler;
      return Promise.resolve(harness.unlisten);
    }),
  };
});

const { api } = await import("@/lib/api");
const runStatusMock = vi.mocked(api.runStatus);
const logsTailMock = vi.mocked(api.logsTail);
const storeItemsMock = vi.mocked(api.storeItems);
const runStartMock = vi.mocked(api.runStart);

import { LogsScreen } from "./logs-screen";
import { buildRunRows, eventToRow, formatAbsolute, splitTextOnQuery, summarizeRun, synthesizeFailure, tailToRows } from "./api";
import type { LogsRunEntry, RunHistoryEntry } from "./api";

// ---------------------------------------------------------------------------
// 夹具(形状严格对齐 types.ts:RunEntry / LogsTailResult / 三类事件)
// ---------------------------------------------------------------------------

/** SourceReport.to_dict 形状(pipeline.py:399-412)的最小 wire 真形;摘要源段
 *  只消费 source/failed/error,健康成员全键在场 */
function sourceDict(name: string, overrides: { failed?: boolean; error?: string | null } = {}) {
  return {
    source: name,
    engine: "httpx",
    url: `https://example.com/${name}`,
    item_count: 2,
    attempts: 1,
    duration_seconds: 0.42,
    skipped: false,
    skip_reason: null,
    failures: [],
    error: overrides.error ?? null,
    failed: overrides.failed ?? false,
  };
}

const run2Running: RunEntry = {
  run_id: 2,
  yaml: "/config/daily-tech.yaml",
  db: "myssia.db",
  dry: false,
  state: "running",
  exit_code: null,
  status: null,
  started_at: "2026-10-02T12:00:00+00:00",
  finished_at: null,
  duration_ms: null,
  record: null,
};

const run1Success: RunEntry = {
  run_id: 1,
  yaml: "/config/tech.yaml",
  db: "myssia.db",
  dry: false,
  state: "done",
  exit_code: 0,
  status: "success",
  started_at: "2026-10-02T08:00:00+00:00",
  finished_at: "2026-10-02T08:00:01+00:00",
  duration_ms: 1200,
  record: {
    run_id: 1,
    category: "科技资讯",
    status: "success",
    started_at: null,
    finished_at: null,
    stats: { items_retained: 5, sources: [sourceDict("example")] },
    steps: null,
    error: null,
  },
};

/** failed 注册表行(wire 真形:注册表行 exit_code 0/1/2/3 有契约语义;
 *  record.error 落库真句 + stats.sources 造一例 failed 成员)——失败区/exit
 *  语义映射/摘要错误段共用 */
const run3Failed: RunEntry = {
  run_id: 3,
  yaml: "/config/social.yaml",
  db: "myssia.db",
  dry: false,
  state: "done",
  exit_code: 2,
  status: "failed",
  started_at: "2026-10-02T06:00:00+00:00",
  finished_at: "2026-10-02T06:00:02+00:00",
  duration_ms: 2000,
  record: {
    run_id: 3,
    category: "社媒动态",
    status: "failed",
    started_at: null,
    finished_at: null,
    stats: {
      items_retained: 2,
      sources: [sourceDict("weibo", { failed: true, error: "engine chain exhausted: timeout" }), sourceDict("rss")],
    },
    steps: null,
    error: "RuntimeError: source fetch failed: timeout after 3 attempts",
  },
};

const tailFixture = {
  lines: [
    { seq: 1, ts: "t1", run_id: 2, stream: "stdout" as const, line: "fetch https://example.com" },
    // INFO 级 stderr 行(本仓采集管线日志全走 stderr):正常运行日志,不染警示色
    { seq: 2, ts: "t2", run_id: 2, stream: "stderr" as const, line: "2026-10-02 12:00:00,001 INFO myssia.pipeline: 运行开始 category=tech run_id=2 sources=1" },
    { seq: 3, ts: "t3", run_id: 2, stream: "stderr" as const, line: "ERROR source fetch failed: timeout" },
    { seq: 4, ts: "t4", run_id: 2, stream: "stderr" as const, line: "2026-10-02 12:00:01,002 WARNING 源限速 backoff 2s" },
    { seq: 5, ts: "t5", run_id: 2, stream: "stderr" as const, line: "2026-10-02 12:00:02,003 INFO myssia.pipeline: 采集步骤完成 sources=1 items=5 source_failures=0" },
  ],
  total: 5,
  truncated: false,
};

// 「上一程」历史行夹具(形状严格对齐 run.status 合流后的 DB 历史行:entry.py
// _history_run_rows——yaml/exit_code 无库源置 null(wire 真形恒 null)、
// dry 恒 false、state=done、history=true、log_run_id=会话对齐号;run_id 是
// DB 自增号,与会话号两空间)
const histRun5: RunHistoryEntry = {
  run_id: 5,
  yaml: null,
  db: "myssia.db",
  dry: false,
  state: "done",
  exit_code: null,
  status: "success",
  started_at: "2026-10-01T09:00:00+00:00",
  finished_at: "2026-10-01T09:00:03+00:00",
  duration_ms: 3000,
  record: {
    run_id: 5,
    category: "科技早报",
    status: "success",
    started_at: "2026-10-01T09:00:00+00:00",
    finished_at: "2026-10-01T09:00:03+00:00",
    stats: { items_retained: 8, sources: [sourceDict("arxiv"), sourceDict("hackernews")] },
    steps: null,
    error: null,
  },
  history: true,
  log_run_id: 9,
};

function mockSidecar(runs: LogsRunEntry[]) {
  // wire 真形已含「上一程」历史行(RunEntry 超集);共享 RunStatusResult 仍
  // 建模注册表行契约(不 widen 的决策见 ./api.ts RunHistoryEntry 注),测试
  // 边界处一次性收窄断言,屏内 loadRuns 按联合类型消费
  runStatusMock.mockResolvedValue({ runs: runs as RunEntry[] });
  logsTailMock.mockResolvedValue(tailFixture);
}

function emit(event: SidecarEvent) {
  act(() => {
    harness.handler?.(event);
  });
}

// alerts.fired 夹具(形状严格对齐 types.ts AlertsFiredEvent;fe-gap-census R2 入联合)
const alertsFiredFixture: AlertsFiredEvent = {
  type: "alerts.fired",
  rule_id: 3,
  rule_name: "GLM 快讯",
  item_id: 42,
  dedup_key: "dk-42",
  title: "GLM-5 发布",
  action: "push",
  action_status: "sent",
  ts: "t9",
};

// cron 域两事件夹具(10-04-cron-ui 涟漪;形状对齐 types.ts,协议 v9 实装)
const cronSkippedFixture: CronSkippedEvent = {
  type: "cron.skipped",
  job_id: "a1b2c3d4e5f6",
  name: "早晚情报流",
  reason: "run_busy",
  active_run_id: 7,
  ts: "t10",
};

const cronCompletedFixture: CronCompletedEvent = {
  type: "cron.completed",
  job_id: "a1b2c3d4e5f6",
  name: "早晚情报流",
  ok: true,
  status: "ok",
  delivery_error: null,
  summary: null,
  ts: "t11",
};

afterEach(() => {
  cleanup(); // vitest globals 关闭,RTL 自动清理不生效,须显式清理
  harness.handler = null;
  vi.resetAllMocks();
});

// Radix Select 2.x 在 jsdom 里开下拉需要的指针捕获/滚动桩(品类·状态过滤用例;
// 同款见 dashboard-screen.test.tsx beforeAll)
beforeAll(() => {
  window.HTMLElement.prototype.hasPointerCapture = () => false;
  window.HTMLElement.prototype.releasePointerCapture = () => {};
  window.HTMLElement.prototype.scrollIntoView = () => {};
});

// Radix Select 2.x:mouse 型 pointerDown 才开下拉(品类·状态过滤用例)
function openSelect(name: string) {
  fireEvent.pointerDown(screen.getByRole("combobox", { name }), { button: 0, pointerType: "mouse" });
}

// ---------------------------------------------------------------------------
// L1 摘要行(两级 IA:每 run 一行直出,accordion 退役)
// ---------------------------------------------------------------------------

describe("LogsScreen L1 摘要行(10-12 两级 IA)", () => {
  it("摘要派生:success 行含成果+源段;running 行如实「采集中…」;行按钮无 aria-expanded(accordion 退役哨兵)", async () => {
    mockSidecar([run2Running, run1Success]);
    render(<LogsScreen />);

    const row1 = await screen.findByTestId("run-row-1");
    expect(row1.getAttribute("aria-expanded")).toBeNull(); // 折叠语义终结
    expect(row1.textContent).toContain("科技资讯");
    expect(row1.textContent).toContain("1.2s");
    const summary1 = screen.getByTestId("run-summary-1");
    expect(summary1.textContent).toContain("保留 5 条");
    expect(summary1.textContent).toContain("1 源");
    expect(summary1.textContent).not.toContain("失败");

    // running 行 record=null(record 为 running 常态)→ 如实兜底,不造假
    expect(screen.getByTestId("run-summary-2").textContent).toBe("采集中…");
  });

  it("摘要派生:failed 行错误段 error 原文 + 失败源计数,dead 片段着色(#ff6b70 实算档)", async () => {
    mockSidecar([run3Failed]);
    render(<LogsScreen />);

    const summary = await screen.findByTestId("run-summary-3");
    expect(summary.textContent).toContain("保留 2 条");
    expect(summary.textContent).toContain("2 源");
    expect(summary.textContent).toContain("失败 1 源");
    expect(summary.textContent).toContain("RuntimeError: source fetch failed: timeout after 3 attempts");
    expect(summary.innerHTML).toContain("text-[#ff6b70]");
  });

  it("摘要派生:终态 record/stats 全缺 → 「无统计记录」(如实,不造假)", async () => {
    mockSidecar([{ ...run1Success, run_id: 4, record: null }]);
    render(<LogsScreen />);
    expect(await screen.findByTestId("run-summary-4").then((el) => el.textContent)).toBe("无统计记录");
  });
});

// ---------------------------------------------------------------------------
// 切级动线(L1 点行 → L2;返回钮 / Esc → L1;缓存不重拉)
// ---------------------------------------------------------------------------

describe("LogsScreen 切级动线", () => {
  it("点行进 L2 惰性拉 tail(L1 零拉取);返回钮回 L1 卸载 detail;再进同 run 缓存不重拉", async () => {
    mockSidecar([run2Running, run1Success]);
    render(<LogsScreen />);
    await screen.findByTestId("run-row-2");
    expect(logsTailMock).not.toHaveBeenCalled(); // 1 级严禁逐行拉日志(数据真源边界)

    fireEvent.click(screen.getByTestId("run-row-2"));
    expect(screen.getByTestId("run-detail")).toBeTruthy();
    await waitFor(() => expect(logsTailMock).toHaveBeenCalledTimes(1));
    expect(logsTailMock).toHaveBeenLastCalledWith({ lines: 400, run_id: 2 });

    fireEvent.click(screen.getByTestId("run-back"));
    expect(screen.queryByTestId("run-detail")).toBeNull();
    expect(screen.getByTestId("run-row-2")).toBeTruthy();

    // 再进同 run:loadedRunsRef 缓存命中,总调用数不变
    fireEvent.click(screen.getByTestId("run-row-2"));
    expect(await screen.findByTestId("run-detail")).toBeTruthy();
    expect(logsTailMock).toHaveBeenCalledTimes(1);
  });

  it("Esc 全局链:2 级按 Esc 回 L1(1 级 no-op);搜索框内 Esc 归清词自身语义不切级", async () => {
    mockSidecar([run2Running, run1Success]);
    render(<LogsScreen />);
    await screen.findByTestId("run-row-2");

    // 1 级 Esc = no-op(仍留列表)
    fireEvent.keyDown(window, { key: "Escape" });
    expect(screen.getByTestId("run-row-2")).toBeTruthy();
    expect(screen.queryByTestId("run-detail")).toBeNull();

    fireEvent.click(screen.getByTestId("run-row-2"));
    await screen.findByTestId("run-detail");
    fireEvent.keyDown(window, { key: "Escape" });
    expect(screen.queryByTestId("run-detail")).toBeNull();

    // 再进;焦点在搜索框时 Esc → 框内清词(守卫①),不触发回退
    fireEvent.click(screen.getByTestId("run-row-2"));
    await screen.findByTestId("run-detail");
    const input = screen.getByTestId("log-search-input");
    fireEvent.change(input, { target: { value: "error" } });
    fireEvent.keyDown(input, { key: "Escape" });
    expect((input as HTMLInputElement).value).toBe("");
    expect(screen.getByTestId("run-detail")).toBeTruthy();
  });
});

// ---------------------------------------------------------------------------
// 默认不自动跳级(design §4.3 定稿:跟随策略退役的哨兵)
// ---------------------------------------------------------------------------

describe("LogsScreen 默认不自动跳级", () => {
  it("进屏素列表;新 running run 到达(completed 触发刷新)仍不跳级、不拉 tail", async () => {
    mockSidecar([run1Success]);
    render(<LogsScreen />);
    await screen.findByTestId("run-row-1");
    expect(screen.queryByTestId("run-detail")).toBeNull();
    expect(logsTailMock).not.toHaveBeenCalled();

    runStatusMock.mockResolvedValue({ runs: [run2Running, run1Success] as RunEntry[] });
    emit({ type: "completed", run_id: 99, exit_code: 0, status: "success", dry: false, ts: "t20" });
    await screen.findByTestId("run-row-2");
    expect(screen.queryByTestId("run-detail")).toBeNull();
    expect(logsTailMock).not.toHaveBeenCalled();
  });
});

// ---------------------------------------------------------------------------
// 过滤态穿越保持(AC3 的 jsdom 半边;滚动位置归无头冒烟)
// ---------------------------------------------------------------------------

describe("LogsScreen 过滤态穿越保持", () => {
  it("品类过滤 → 进 L2 → Esc 回:计数与行集仍是被过滤态", async () => {
    mockSidecar([run2Running, run1Success]);
    render(<LogsScreen />);
    await screen.findByTestId("run-row-2");
    expect(screen.getByTestId("logs-filter-count").textContent).toBe("2 / 2 轮");

    openSelect("品类过滤");
    fireEvent.click(await screen.findByRole("option", { name: "科技资讯" }));
    await waitFor(() => expect(screen.queryByTestId("run-row-2")).toBeNull());
    expect(screen.getByTestId("logs-filter-count").textContent).toBe("1 / 2 轮");

    fireEvent.click(screen.getByTestId("run-row-1"));
    await screen.findByTestId("run-detail");
    fireEvent.keyDown(window, { key: "Escape" });
    expect(screen.queryByTestId("run-detail")).toBeNull();
    // 过滤态挂编排层,切级天然不重置
    expect(screen.getByTestId("logs-filter-count").textContent).toBe("1 / 2 轮");
    expect(screen.queryByTestId("run-row-2")).toBeNull();
    expect(screen.getByTestId("run-row-1")).toBeTruthy();
  });

  it("状态过滤 + 清除过滤(L1 既有工具面零回归)", async () => {
    mockSidecar([run2Running, run1Success]);
    render(<LogsScreen />);
    await screen.findByTestId("run-row-2");

    openSelect("状态过滤");
    fireEvent.click(await screen.findByRole("option", { name: "运行中" }));
    await waitFor(() => expect(screen.queryByTestId("run-row-1")).toBeNull());
    expect(screen.getByTestId("run-row-2")).toBeTruthy();

    fireEvent.click(screen.getByRole("button", { name: /清除过滤/ }));
    await waitFor(() => expect(screen.getByTestId("run-row-1")).toBeTruthy());
    expect(screen.getByTestId("logs-filter-count").textContent).toBe("2 / 2 轮");
  });
});

// ---------------------------------------------------------------------------
// 失败原因区(L2;PRD AC2「成功轮不显示」)
// ---------------------------------------------------------------------------

describe("LogsScreen 失败原因区", () => {
  it("failed 注册表行三源齐呈:exit 语义/error 原文/stderr 错误行摘;success 行不渲染", async () => {
    mockSidecar([run3Failed, run1Success]);
    render(<LogsScreen />);

    fireEvent.click(await screen.findByTestId("run-row-3"));
    const panel = await screen.findByTestId("run-failure-3");
    expect(panel.textContent).toContain("exit=2 · 运行失败"); // cli.py:212-215 契约语义词
    expect(panel.textContent).toContain("RuntimeError: source fetch failed: timeout after 3 attempts");
    expect(panel.textContent).toContain("ERROR source fetch failed: timeout"); // stderr 错误行摘
    expect(screen.getByTestId("run-failure-line-3-0").textContent).toContain("ERROR");

    // success 轮:失败区一行都不渲染
    fireEvent.click(screen.getByTestId("run-back"));
    fireEvent.click(screen.getByTestId("run-row-1"));
    await screen.findByTestId("run-detail");
    expect(screen.queryByTestId("run-failure-1")).toBeNull();
  });

  it("三源全空 → 无据如实文案;旧行无对齐号(log_run_id=null)不挂「日志拉取中」且零请求(永假在途态拦下)", async () => {
    const histNoAlignFailed: RunHistoryEntry = {
      ...histRun5,
      run_id: 8,
      status: "failed",
      record: {
        run_id: 8,
        category: "科技早报",
        status: "failed",
        started_at: null,
        finished_at: null,
        stats: null,
        steps: null,
        error: null,
      },
      log_run_id: null,
    };
    mockSidecar([histNoAlignFailed]);
    render(<LogsScreen />);

    fireEvent.click(await screen.findByTestId("run-row-h8"));
    await screen.findByTestId("run-detail");
    const panel = await screen.findByTestId("run-failure-h8");
    expect(panel.textContent).toContain("exit=—"); // 历史行 wire 真形(entry.py 恒 None),不编语义
    expect(screen.getByTestId("run-failure-none-h8").textContent).toContain("暂无结构化失败记录");
    expect(panel.textContent).not.toContain("日志拉取中");
    expect(logsTailMock).not.toHaveBeenCalled(); // ensureTail 对 null 号早退
  });

  it("tail 真在途(对齐号在场)挂「日志拉取中」,到位后错误行摘补上", async () => {
    let resolveTail: (value: typeof tailFixture) => void = () => {};
    const failedHist: RunHistoryEntry = {
      ...histRun5,
      status: "failed",
      record: { ...histRun5.record!, error: "source chain collapsed" },
    };
    runStatusMock.mockResolvedValue({ runs: [failedHist as unknown as RunEntry] });
    logsTailMock.mockImplementation(
      () => new Promise<typeof tailFixture>((resolve) => { resolveTail = resolve; }),
    );
    render(<LogsScreen />);

    fireEvent.click(await screen.findByTestId("run-row-h5"));
    await screen.findByTestId("run-detail");
    expect(screen.getByTestId("run-failure-h5").textContent).toContain("日志拉取中");

    await act(async () => {
      resolveTail(tailFixture);
    });
    await screen.findByTestId("run-failure-line-h5-0");
    expect(screen.getByTestId("run-failure-h5").textContent).not.toContain("日志拉取中");
    expect(screen.getByTestId("run-failure-h5").textContent).toContain("exit=—");
  });
});

// ---------------------------------------------------------------------------
// L2 元信息头(绝对起止/耗时/exit/来源号/行数-错误行数)
// ---------------------------------------------------------------------------

describe("LogsScreen L2 元信息头", () => {
  it("历史行:绝对起止/耗时/exit=—/会话对齐号 run_id=9/行数-错误行数", async () => {
    mockSidecar([histRun5]);
    render(<LogsScreen />);
    fireEvent.click(await screen.findByTestId("run-row-h5"));
    await screen.findByTestId("run-detail");

    const meta = screen.getByTestId("run-detail-meta-h5");
    expect(meta.textContent).toMatch(/^\D*\d{4}-\d{2}-\d{2} \d{2}:\d{2}/); // formatAbsolute(本地时区)
    expect(meta.textContent).toContain("结束");
    expect(meta.textContent).toContain("3.0s");
    expect(meta.textContent).toContain("exit=—");
    expect(meta.textContent).toContain("logs.tail run_id=9"); // 会话对齐号,非 DB 号 5
    await waitFor(() => expect(meta.textContent).toContain("5 行"));
    expect(meta.textContent).toContain("1 错误行");
  });

  it("exit 语义映射用注册表行:failed exit_code=2 → 元信息头 exit=2 + 失败区「运行失败」", async () => {
    mockSidecar([run3Failed]);
    render(<LogsScreen />);
    fireEvent.click(await screen.findByTestId("run-row-3"));
    await screen.findByTestId("run-detail");
    expect(screen.getByTestId("run-detail-meta-3").textContent).toContain("exit=2");
    expect(screen.getByTestId("run-failure-3").textContent).toContain("运行失败");
  });
});

// ---------------------------------------------------------------------------
// L2 日志体(内滚帽解除/错误行着色/搜索三件套迁 L2/自动滚底随迁)
// ---------------------------------------------------------------------------

describe("LogsScreen L2 日志体", () => {
  it("错误行 dead 高亮(bg-dead/10)/ WARNING 级警示 / INFO 级不染;行子项 shrink-0(塌缩律)", async () => {
    mockSidecar([run2Running, run1Success]);
    render(<LogsScreen />);
    fireEvent.click(await screen.findByTestId("run-row-2"));
    const rows = await screen.findAllByTestId("log-row");
    expect(rows).toHaveLength(5);
    for (const row of rows) {
      expect(row.className).toContain("shrink-0"); // 直接 flex 子项塌缩律(67546cd 不回归)
    }
    const errorRow = rows.find((row) => row.textContent?.includes("ERROR"));
    expect(errorRow?.getAttribute("data-error")).toBe("true");
    expect(errorRow?.className).toContain("text-dead");
    // P2(G7 附带):对比公式实算 text-dead #e5484d 叠 bg-dead/10 于 bg-sidebar
    // #080b13 上 ≈ 4.67:1(原 /15 ≈ 4.43:1 不达 WCAG AA 正文 4.5)
    expect(errorRow?.className).toContain("bg-dead/10");
    const warnRow = rows.find((row) => row.textContent?.includes("源限速"));
    expect(warnRow?.getAttribute("data-warn")).toBe("true");
    expect(warnRow?.getAttribute("data-error")).toBeNull();
    const infoRow = rows.find((row) => row.textContent?.includes("运行开始"));
    expect(infoRow?.getAttribute("data-error")).toBeNull();
    expect(infoRow?.getAttribute("data-warn")).toBeNull(); // INFO 级 stderr 不再全染警示
    const progressSignal = rows.find((row) => row.textContent?.includes("采集步骤完成"));
    expect(progressSignal?.getAttribute("data-error")).toBeNull();
    const normalRow = rows.find((row) => row.textContent?.includes("fetch https://"));
    expect(normalRow?.getAttribute("data-error")).toBeNull();
    expect(normalRow?.getAttribute("data-warn")).toBeNull();
    // 内滚帽解除:accordion 时代 max-h-[26rem] → 页面级 flex-1
    expect(screen.getByTestId("run-log-2").className).toContain("flex-1");
    expect(screen.getByTestId("run-log-2").className).not.toContain("max-h-");
  });

  it("搜索(迁 L2 挂载点):输入即过滤 + mark 高亮 + 命中计数;无命中文案;清空恢复", async () => {
    mockSidecar([run2Running, run1Success]);
    render(<LogsScreen />);
    fireEvent.click(await screen.findByTestId("run-row-2"));
    await screen.findAllByTestId("log-row");
    expect(screen.getAllByTestId("log-row")).toHaveLength(5);

    // 小写 "error" 命中大写 ERROR 行(stdout/WARNING/INFO 行全部滤除)
    fireEvent.change(screen.getByTestId("log-search-input"), { target: { value: "error" } });
    const rows = await screen.findAllByTestId("log-row");
    expect(rows).toHaveLength(1);
    expect(rows[0].textContent).toContain("ERROR source fetch failed");
    expect(screen.getByTestId("run-log-hits-2").textContent).toContain("命中 1 / 5 行");

    const marks = screen.getAllByTestId("log-search-hit");
    expect(marks).toHaveLength(1);
    expect(marks[0].textContent).toBe("ERROR");

    fireEvent.change(screen.getByTestId("log-search-input"), { target: { value: "zzz-不存在" } });
    expect(await screen.findByText(/无命中行/)).toBeTruthy();
    expect(screen.queryAllByTestId("log-row")).toHaveLength(0);
    expect(screen.getByTestId("run-log-hits-2").textContent).toContain("命中 0 / 5 行");

    fireEvent.change(screen.getByTestId("log-search-input"), { target: { value: "" } });
    await waitFor(() => expect(screen.getAllByTestId("log-row")).toHaveLength(5));
  });
});

// ---------------------------------------------------------------------------
// 流式续播(事件按 run_id 归组;未进 L2 先缓冲,进 L2 时 tail 打底合并)
// ---------------------------------------------------------------------------

describe("LogsScreen 流式续播", () => {
  it("事件归组缓冲;进 L2 时 tail 打底、缓冲行殿后;错误行实时高亮;completed 刷新列表", async () => {
    mockSidecar([run2Running, run1Success]);
    render(<LogsScreen />);
    await screen.findByTestId("run-row-2");
    expect(harness.handler).not.toBeNull();

    // 他 run 的 log 事件:不入任何可见体(runs 列表也没有该组)
    emit({ type: "log", run_id: 99, stream: "stdout", line: "他 run 的行", ts: "t5" });

    // 未进 L2:run 2 的实时事件缓冲不可见(L1 无日志体)
    emit({ type: "log", run_id: 2, stream: "stdout", line: "实时输出行", ts: "t6" });
    expect(screen.queryByText("实时输出行")).toBeNull();

    // 进 L2:tail 打底 + 缓冲行合并到 tail 历史之后(事件比快照新)
    fireEvent.click(screen.getByTestId("run-row-2"));
    await screen.findAllByTestId("log-row");
    expect(screen.getByText("实时输出行")).toBeTruthy();
    const body = screen.getByTestId("run-log-2");
    const texts = Array.from(body.querySelectorAll('[data-testid="log-row"]')).map((el) => el.textContent);
    const bufferedIndex = texts.findIndex((t) => t?.includes("实时输出行"));
    expect(bufferedIndex).toBe(texts.length - 1);

    // stderr 错误行实时高亮(dead)
    emit({ type: "log", run_id: 2, stream: "stderr", line: "ERROR 实时错误", ts: "t7" });
    await waitFor(() =>
      expect(screen.getByText(/实时错误/).getAttribute("data-error")).toBe("true"),
    );

    // progress 事件 → system 合成行(▸ 源完成 source=… items=…)
    emit({
      type: "progress",
      run_id: 2,
      phase: "source_done",
      source: "example",
      engine: "httpx",
      items: "3",
      ts: "t8",
    });
    const systemRow = await screen.findByTestId("log-system-row");
    expect(systemRow.textContent).toContain("源完成");
    expect(systemRow.textContent).toContain("source=example");

    // completed(选中 run)→ 摘要行 + 列表刷新(runStatus 第二次调用)
    emit({
      type: "completed",
      run_id: 2,
      exit_code: 0,
      status: "success",
      dry: false,
      duration_ms: 900,
      ts: "t9",
    });
    expect(await screen.findByText(/run 2 结束/).then((el) => el.textContent)).toContain("status=success");
    await waitFor(() => expect(runStatusMock.mock.calls.length).toBeGreaterThanOrEqual(2));

    // 他 run 的 completed:只刷新列表,不落摘要行
    emit({ type: "completed", run_id: 99, exit_code: 2, status: "failed", dry: false, ts: "t10" });
    await waitFor(() => expect(runStatusMock.mock.calls.length).toBeGreaterThanOrEqual(3));
    expect(screen.queryByText(/run 99 结束/)).toBeNull();
  });
});

// ---------------------------------------------------------------------------
// 重跑(L1/L2 双可达;triggered 词面去「展开跟随」)
// ---------------------------------------------------------------------------

describe("LogsScreen 重跑", () => {
  it("L1 行操作按原 run 的 yaml/dry/db 调 run.start,反馈新 run_id 并刷新列表", async () => {
    runStartMock.mockResolvedValue({
      run_id: 3,
      state: "running",
      yaml: "/config/tech.yaml",
      dry: false,
      db: "myssia.db",
    });
    mockSidecar([run2Running, run1Success]);
    render(<LogsScreen />);
    await screen.findByTestId("run-row-1");
    const runStatusCalls = runStatusMock.mock.calls.length;

    fireEvent.click(screen.getByTestId("run-rerun-1"));
    // 回放原 run 三参数(dry/db 原样),不新增协议方法
    await waitFor(() =>
      expect(runStartMock).toHaveBeenCalledWith({ yaml: "/config/tech.yaml", dry: false, db: "myssia.db" }),
    );
    const ok = await screen.findByTestId("run-rerun-ok-1");
    expect(ok.textContent).toContain("已触发 #3");
    // 词面(design §2.3):不再有「展开跟随」,两级 IA 下新 run 落列表
    expect(ok.getAttribute("title")).toContain("运行历史列表已刷新");
    expect(ok.getAttribute("title")).not.toContain("展开跟随");
    await waitFor(() => expect(runStatusMock.mock.calls.length).toBe(runStatusCalls + 1));
  });

  it("L2 元信息头重跑钮双可达,反馈同挂 detail", async () => {
    runStartMock.mockResolvedValue({
      run_id: 3,
      state: "running",
      yaml: "/config/tech.yaml",
      dry: false,
      db: "myssia.db",
    });
    mockSidecar([run2Running, run1Success]);
    render(<LogsScreen />);
    fireEvent.click(await screen.findByTestId("run-row-1"));
    await screen.findByTestId("run-detail");

    fireEvent.click(screen.getByTestId("run-rerun-1"));
    await waitFor(() =>
      expect(runStartMock).toHaveBeenCalledWith({ yaml: "/config/tech.yaml", dry: false, db: "myssia.db" }),
    );
    expect(await screen.findByTestId("run-rerun-ok-1").then((el) => el.textContent)).toContain("已触发 #3");
  });

  it("重跑失败:sidecar 结构化错误如实上屏(run_busy)", async () => {
    runStartMock.mockRejectedValue(
      new SidecarRequestError({ code: "run_busy", path: "$", message: "已有 run 在跑" }),
    );
    mockSidecar([run2Running, run1Success]);
    render(<LogsScreen />);
    await screen.findByTestId("run-row-1");

    fireEvent.click(screen.getByTestId("run-rerun-1"));
    const feedback = await screen.findByTestId("run-rerun-err-1");
    expect(feedback.textContent).toContain("run_busy");
    expect(feedback.textContent).toContain("已有 run 在跑");
  });
});

// ---------------------------------------------------------------------------
// 结构化错误横幅(挂编排层,L1/L2 两级可见)与空态
// ---------------------------------------------------------------------------

describe("LogsScreen 结构化错误与空态", () => {
  it("sidecar 结构化错误上屏(sidecar_not_running)", async () => {
    runStatusMock.mockRejectedValue(
      new SidecarRequestError({ code: "sidecar_not_running", path: "$", message: "sidecar 未运行" }),
    );
    logsTailMock.mockResolvedValue({ lines: [], total: 0, truncated: false });
    render(<LogsScreen />);

    const banner = await screen.findByTestId("logs-error");
    expect(banner.textContent).toContain("sidecar_not_running");
    expect(banner.textContent).toContain("sidecar 未运行");
  });

  it("横幅两级可见:进 L2 后 run.status 刷新失败,横幅仍在场且 L2 不被顶掉(design §2.3 R2)", async () => {
    mockSidecar([run1Success]);
    render(<LogsScreen />);
    fireEvent.click(await screen.findByTestId("run-row-1"));
    await screen.findByTestId("run-detail");

    runStatusMock.mockRejectedValue(
      new SidecarRequestError({ code: "sidecar_not_running", path: "$", message: "sidecar 未运行" }),
    );
    emit({ type: "completed", run_id: 1, exit_code: 0, status: "success", dry: false, ts: "t20" });
    const banner = await screen.findByTestId("logs-error");
    expect(banner.textContent).toContain("sidecar_not_running");
    expect(screen.getByTestId("run-detail")).toBeTruthy();
  });

  it("空态:无 run 记录给引导文案,不渲染任何行", async () => {
    mockSidecar([]);
    render(<LogsScreen />);

    expect(await screen.findByText(/还没有采集记录/)).toBeTruthy();
    expect(screen.queryByTestId("run-row-1")).toBeNull();
    expect(screen.queryByTestId("run-row-2")).toBeNull();
  });

  it("试跑徽标:dry run 行标「试跑」,title 留 dry run 技术注(dry→试跑,10-05-dashboard-glance)", async () => {
    mockSidecar([{ ...run1Success, run_id: 7, dry: true }]);
    render(<LogsScreen />);

    const row = await screen.findByTestId("run-row-7");
    expect(row.textContent).toContain("试跑");
    const badge = row.querySelector('[data-slot="badge"]');
    expect(badge?.getAttribute("title")).toBe("dry run(不落库)");
  });
});

// ---------------------------------------------------------------------------
// 「上一程」历史行全家族(10-07-logs-restart-visibility R1 语义平移新挂点)
// ---------------------------------------------------------------------------

describe("LogsScreen 上一程历史行", () => {
  it("渲染:徽标 + 同款摘要面;注册表在前/历史接后顺序直渲;历史行无重跑钮", async () => {
    mockSidecar([run2Running, run1Success, histRun5]);
    render(<LogsScreen />);

    const histRow = await screen.findByTestId("run-row-h5");
    expect(histRow.textContent).toContain("科技早报");
    expect(histRow.textContent).toContain("3.0s");
    expect(histRow.textContent).toContain("保留 8 条");
    expect(screen.getByTestId("run-status-chip-h5").textContent).toContain("成功");

    const badge = histRow.querySelector('[data-testid="run-history-badge-h5"]');
    expect(badge?.textContent).toContain("上一程");
    expect(badge?.getAttribute("title")).toContain("重启前");

    expect(
      screen.getByTestId("run-row-2").querySelector('[data-testid^="run-history-badge-"]'),
    ).toBeNull();

    // 新→旧:协议回包顺序直渲(注册表在前、DB 历史接后),前端不重排
    const order = screen.getAllByTestId(/^run-row-/).map((el) => el.getAttribute("data-testid"));
    expect(order).toEqual(["run-row-2", "run-row-1", "run-row-h5"]);

    expect(screen.queryByTestId("run-rerun-h5")).toBeNull();
    expect(screen.getByTestId("run-rerun-2")).toBeTruthy();
  });

  it("进历史行详情:logs.tail 按 log_run_id 会话对齐号拉取(非 DB 号);返回再进缓存不重拉", async () => {
    mockSidecar([histRun5]); // 重启后注册表空 → 历史行接管列表
    render(<LogsScreen />);

    fireEvent.click(await screen.findByTestId("run-row-h5"));
    // 惰性 tail:run_id=log_run_id(9,会话号),不是 DB 号 5——两编号空间不混用
    await waitFor(() => expect(logsTailMock).toHaveBeenLastCalledWith({ lines: 400, run_id: 9 }));
    expect(screen.getByTestId("run-detail-meta-h5").textContent).toContain("run_id=9");
    expect(await within(screen.getByTestId("run-log-h5")).findAllByTestId("log-row")).toHaveLength(5);

    fireEvent.click(screen.getByTestId("run-back"));
    expect(screen.queryByTestId("run-detail")).toBeNull();
    fireEvent.click(screen.getByTestId("run-row-h5"));
    expect(await within(screen.getByTestId("run-log-h5")).findAllByTestId("log-row")).toHaveLength(5);
    expect(logsTailMock).toHaveBeenCalledTimes(1);
  });

  it("旧行无对齐号(log_run_id=null):不拉取,日志体如实降级;来源标记如实报「未对齐」", async () => {
    mockSidecar([{ ...histRun5, log_run_id: null }]);
    render(<LogsScreen />);

    fireEvent.click(await screen.findByTestId("run-row-h5"));
    await screen.findByTestId("run-detail");
    expect(screen.getByTestId("run-log-h5").textContent).toContain("未记录日志会话号");
    expect(screen.getByTestId("run-log-h5").textContent).toContain("无可回看的日志");
    expect(logsTailMock).not.toHaveBeenCalled();
    expect(screen.getByTestId("run-detail-meta-h5").textContent).toContain("run_id=—");
  });

  it("L2 采集成果区:保留 N 条 + 每源行 + 条目预览(finishedAt 截窗);running 行不渲染", async () => {
    storeItemsMock.mockResolvedValue({
      db: "myssia.db",
      count: 2,
      items: [
        {
          id: 1, url: "https://example.com/a", dedup_key: "dk-a", title: "标题甲(本轮新入库)",
          source: "arxiv", content: null, tags: [], category: "科技早报", scores: null,
          pushed_at: null, push_slot: null,
          first_seen: "2026-10-01T09:00:02+00:00", read: false, starred: false, later: false,
        },
        {
          id: 2, url: "https://example.com/b", dedup_key: "dk-b", title: "后继轮条目(截窗应剔)",
          source: "arxiv", content: null, tags: [], category: "科技早报", scores: null,
          pushed_at: null, push_slot: null,
          first_seen: "2026-10-02T09:00:00+00:00", read: false, starred: false, later: false,
        },
      ],
    });
    mockSidecar([{ ...histRun5, record: { ...histRun5.record!, stats: {
      ...histRun5.record!.stats,
      push: [{ channel: "feishu_card", ok: true, immediate: 0, digest: 8, archive: 0, failures: [] }],
    } } }]);
    render(<LogsScreen />);

    fireEvent.click(await screen.findByTestId("run-row-h5"));
    await screen.findByTestId("run-detail");
    const outcome = await screen.findByTestId("run-outcome-h5");
    expect(outcome.textContent).toContain("保留");
    expect(outcome.textContent).toContain("8");
    expect(outcome.textContent).toContain("feishu_card");
    expect(outcome.textContent).toContain("日报 8");
    const sources = screen.getByTestId("run-outcome-sources-h5");
    expect(sources.textContent).toContain("arxiv");
    expect(sources.textContent).toContain("hackernews");
    expect(sources.textContent).toContain("2 条");
    const preview = await screen.findByTestId("run-outcome-preview-h5");
    expect(preview.textContent).toContain("标题甲");
    expect(preview.textContent).not.toContain("后继轮条目"); // finishedAt 截窗
    expect(storeItemsMock).toHaveBeenCalledWith(
      expect.objectContaining({ category: "科技早报", since: "2026-10-01T09:00:00+00:00" }),
    );
    cleanup();
  });

  it("L2 采集成果区:running 行(record=null)一行不渲染", async () => {
    mockSidecar([run2Running]);
    render(<LogsScreen />);

    fireEvent.click(await screen.findByTestId("run-row-2"));
    await screen.findByTestId("run-detail");
    expect(screen.queryByTestId("run-outcome-2")).toBeNull();
    expect(storeItemsMock).not.toHaveBeenCalled();
    cleanup();
  });

  it("撞号防混:注册表会话 5 与历史 DB 5 同屏分立;实时事件只进注册表行,历史行按对齐号拉取", async () => {
    const run5Running: RunEntry = { ...run2Running, run_id: 5 };
    const histDb5: RunHistoryEntry = { ...histRun5, run_id: 5 }; // DB 号同 5,log_run_id=9
    mockSidecar([run5Running, histDb5]);
    render(<LogsScreen />);

    // 同号两行并存(会话号与 DB 号两编号空间),DOM id/testid 靠 h 前缀分立
    expect(await screen.findByTestId("run-row-5")).toBeTruthy();
    expect(screen.getByTestId("run-row-h5")).toBeTruthy();

    fireEvent.click(screen.getByTestId("run-row-5"));
    await waitFor(() => expect(logsTailMock).toHaveBeenLastCalledWith({ lines: 400, run_id: 5 }));
    emit({ type: "log", run_id: 5, stream: "stdout", line: "实时行-注册表5", ts: "t6" });
    expect(await within(screen.getByTestId("run-log-5")).findByText(/实时行-注册表5/)).toBeTruthy();

    // 返回后进历史行 → 按对齐号 9 拉取;两体内容互不串
    fireEvent.click(screen.getByTestId("run-back"));
    fireEvent.click(screen.getByTestId("run-row-h5"));
    await waitFor(() => expect(logsTailMock).toHaveBeenLastCalledWith({ lines: 400, run_id: 9 }));
    const histText = screen.getByTestId("run-log-h5").textContent ?? "";
    expect(histText).not.toContain("实时行-注册表5");
  });
});

// ---------------------------------------------------------------------------
// api.ts 纯函数(10-12 两级视图派生,直测)
// ---------------------------------------------------------------------------

/** LogsRunEntry → RunRowModel(buildRunRows 首行;synthesizeFailure 直测用) */
function rowOf(run: LogsRunEntry) {
  return buildRunRows([run])[0];
}

describe("logs api 纯函数(10-12 两级视图派生)", () => {
  describe("summarizeRun", () => {
    it("分状态段拼装:成果+源+失败源+错误原文;running 兜「采集中…」;终态缺 stats 兜「无统计记录」", () => {
      const ok = summarizeRun(run1Success);
      expect(ok.empty).toBeNull();
      expect(ok.segments.map((s) => s.text)).toEqual(["保留 5 条", "1 源"]);
      expect(ok.segments.every((s) => s.tone === "muted")).toBe(true);

      const failed = summarizeRun(run3Failed);
      expect(failed.segments.map((s) => s.text)).toEqual([
        "保留 2 条",
        "2 源",
        "失败 1 源",
        "RuntimeError: source fetch failed: timeout after 3 attempts",
      ]);
      expect(failed.segments.filter((s) => s.tone === "dead").map((s) => s.text)).toEqual([
        "失败 1 源",
        "RuntimeError: source fetch failed: timeout after 3 attempts",
      ]);

      expect(summarizeRun(run2Running).empty).toBe("采集中…");
      expect(summarizeRun({ ...run1Success, run_id: 4, record: null }).empty).toBe("无统计记录");
    });

    it("wire 形状守卫:stats.sources 非数组不崩、元素缺键/异型成员按真形计数", () => {
      const nonArray = summarizeRun({
        ...run1Success,
        record: { ...run1Success.record!, stats: { items_retained: 5, sources: "not-an-array" } },
      });
      expect(nonArray.segments.map((s) => s.text)).toEqual(["保留 5 条"]); // 源段守卫跳过

      const mixed = summarizeRun({
        ...run1Success,
        record: { ...run1Success.record!, stats: { sources: [null, 42, {}, { failed: true }] } },
      });
      expect(mixed.segments.map((s) => s.text)).toEqual(["4 源", "失败 1 源"]);
    });
  });

  describe("synthesizeFailure", () => {
    it("渲染门槛:success / running / status 未知 → null(成功轮不显示失败区)", () => {
      expect(synthesizeFailure(rowOf(run1Success), undefined)).toBeNull();
      expect(synthesizeFailure(rowOf(run2Running), undefined)).toBeNull();
      expect(synthesizeFailure(rowOf({ ...run3Failed, status: null }), undefined)).toBeNull();
    });

    it("证据象限:三源齐 / exit 无据不编语义 / tail 在途挂等待 / 旧行无对齐号直接判无据", () => {
      const rows = tailToRows(tailFixture);

      const full = synthesizeFailure(rowOf(run3Failed), rows);
      expect(full).not.toBeNull();
      expect(full?.exitCode).toBe(2);
      expect(full?.exitLabel).toBe("运行失败");
      expect(full?.errorText).toContain("RuntimeError");
      expect(full?.errorRows).toHaveLength(1);
      expect(full?.errorRowsTotal).toBe(1);
      expect(full?.tailPending).toBe(false);
      expect(full?.logAligned).toBe(true);

      const noExit = synthesizeFailure(rowOf({ ...run3Failed, exit_code: null }), rows);
      expect(noExit?.exitCode).toBeNull();
      expect(noExit?.exitLabel).toBeNull(); // null 不编语义

      const pending = synthesizeFailure(
        rowOf({ ...histRun5, status: "failed", record: { ...histRun5.record!, error: "source chain collapsed" } }),
        undefined,
      ); // failed 历史行,logRunId=9 在场
      expect(pending?.tailPending).toBe(true);
      expect(pending?.errorRows).toHaveLength(0);

      const unaligned = synthesizeFailure(rowOf({ ...histRun5, status: "failed", log_run_id: null }), undefined);
      expect(unaligned?.logAligned).toBe(false);
      expect(unaligned?.tailPending).toBe(false); // 永假在途态在此拦下(design §3.2 R2)
      expect(unaligned?.errorRows).toHaveLength(0);
    });
  });

  describe("formatAbsolute", () => {
    it("YYYY-MM-DD HH:mm 本地时区;可空/非法 → 「—」", () => {
      expect(formatAbsolute("2026-10-01T09:00:00+00:00")).toMatch(/^\d{4}-\d{2}-\d{2} \d{2}:\d{2}$/);
      expect(formatAbsolute(null)).toBe("—");
      expect(formatAbsolute(undefined)).toBe("—");
      expect(formatAbsolute("not-a-date")).toBe("—");
    });
  });

  describe("splitTextOnQuery(搜索高亮切分,平移零改回归)", () => {
    it("大小写不敏感命中切分;空 needle 通配", () => {
      expect(splitTextOnQuery("a ERROR b", "error")).toEqual([
        { text: "a ", hit: false },
        { text: "ERROR", hit: true },
        { text: " b", hit: false },
      ]);
      expect(splitTextOnQuery("plain", "")).toEqual([{ text: "plain", hit: false }]);
    });
  });
});

// ---------------------------------------------------------------------------
// eventToRow(alerts.fired)—— fe-gap-census R2 穷尽守卫适配
// ---------------------------------------------------------------------------

describe("eventToRow(alerts.fired)—— fe-gap-census R2 穷尽守卫适配", () => {
  it("alerts.fired → 系统摘要行(runId=null 同试抓口径;规则名/标题/动作状态入文案;ts 透传)", () => {
    const row = eventToRow(alertsFiredFixture, 7);
    expect(row.key).toBe("event:7");
    expect(row.runId).toBeNull();
    expect(row.stream).toBe("system");
    expect(row.ts).toBe("t9");
    expect(row.text).toContain("告警命中");
    expect(row.text).toContain("GLM 快讯");
    expect(row.text).toContain("GLM-5 发布");
    expect(row.text).toContain("push:sent");
  });

  it("title=null 的 fired 快照:文案不残留空「」,动作状态仍如实", () => {
    const row = eventToRow({ ...alertsFiredFixture, title: null, action: "tag", action_status: "tagged" }, 8);
    expect(row.text).toContain("tag:tagged");
    expect(row.text).not.toContain("「」");
    expect(row.text).not.toContain("GLM-5 发布");
  });
});

describe("eventToRow(cron.*)—— 10-04-cron-ui 涟漪(穷尽守卫适配,协议 v9)", () => {
  it("cron.skipped → 系统行 runId=null:job 名/reason/占用 run id 入文案;ts 透传", () => {
    const row = eventToRow(cronSkippedFixture, 11);
    expect(row.key).toBe("event:11");
    expect(row.runId).toBeNull();
    expect(row.stream).toBe("system");
    expect(row.ts).toBe("t10");
    expect(row.text).toContain("定时任务跳过");
    expect(row.text).toContain("早晚情报流");
    expect(row.text).toContain("run_busy");
    expect(row.text).toContain("#7");
  });

  it("cron.completed → 系统行 runId=null:job 名/status;失败+投递错误附注", () => {
    const ok = eventToRow(cronCompletedFixture, 12);
    expect(ok.key).toBe("event:12");
    expect(ok.runId).toBeNull();
    expect(ok.stream).toBe("system");
    expect(ok.ts).toBe("t11");
    expect(ok.text).toContain("定时任务完成");
    expect(ok.text).toContain("早晚情报流");
    expect(ok.text).toContain("status=ok");
    expect(ok.text).not.toContain("投递失败");

    const failed = eventToRow(
      { ...cronCompletedFixture, ok: false, status: "failed", delivery_error: "feishu 429 限流" },
      13,
    );
    expect(failed.text).toContain("status=failed");
    expect(failed.text).toContain("投递失败");
    expect(failed.text).toContain("feishu 429 限流");
  });
});
