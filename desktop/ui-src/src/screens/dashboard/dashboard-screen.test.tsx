// @vitest-environment jsdom
/**
 * 仪表盘组件测试 —— mock sidecar(vi.mock "@/lib/api" 的 api 门面,
 * doctor / runs.list / run.status / store.trend 返回夹具;错误用真实
 * SidecarRequestError 注入)。覆盖:状态句(D1 verdict 四态)+ 告警清单
 * (D3 双口径触发)/ 概览条(D4 四格,口径 note 收 ⓘ 悬停 R3)/ 采集量趋势
 * (Select 时间范围 + 自绘 sparkline,窗口切换重查)/ 源健康度卡网格(四态 +
 * 异常优先 + 相对时间锚)/ 品类状态卡(含载入失败)/ 源健康度四态计数 /
 * 最近采集成功率(runs.list 历史行 + run.status 活跃叠加,C3)/ 错误与空态。
 */
import { cleanup, fireEvent, render, screen, waitFor, act } from "@testing-library/react";
import { afterEach, beforeAll, describe, expect, it, vi } from "vitest";

import { SidecarRequestError } from "@/lib/api";
import type {
  DoctorResult,
  RunEntry,
  RunOutcomeDay,
  RunRecord,
  SourceHealthState,
  TrendDay,
} from "@/lib/api";

vi.mock("@/lib/api", async (importOriginal) => {
  const actual = await importOriginal<typeof import("@/lib/api")>();
  return {
    ...actual,
    api: {
      ...actual.api,
      doctor: vi.fn(),
      runsList: vi.fn(),
      runStatus: vi.fn(),
      runStart: vi.fn(),
      storeTrend: vi.fn(),
      runsTrend: vi.fn(),
      feedbackStats: vi.fn(),
    },
    onSidecarEvent: vi.fn(),
  };
});

const { api, onSidecarEvent } = await import("@/lib/api");
const doctorMock = vi.mocked(api.doctor);
const runsListMock = vi.mocked(api.runsList);
const runStatusMock = vi.mocked(api.runStatus);
const runStartMock = vi.mocked(api.runStart);
const storeTrendMock = vi.mocked(api.storeTrend);
const runsTrendMock = vi.mocked(api.runsTrend);
const feedbackStatsMock = vi.mocked(api.feedbackStats);
const onSidecarEventMock = vi.mocked(onSidecarEvent);

import { DashboardScreen } from "./dashboard-screen";
import { Sparkline } from "./sparkline";
import {
  buildOverviewStats,
  buildVerdict,
  cumulativeOutcomeSummary,
  fillDailyCounts,
  fillDailyOutcomes,
  overviewTrendDays,
  shiftUtcDate,
  successRateSeries,
  toSparklinePoints,
} from "./api";
import type {
  CategoryCardModel,
  CategoryTone,
  DashboardRun,
  OverviewStats,
  RunSuccessSummary,
  SourceHealthCounts,
} from "./api";

// ---------------------------------------------------------------------------
// 夹具(形状严格对齐 types.ts:DoctorResult / RunEntry)
// ---------------------------------------------------------------------------

function fixtureSource(
  name: string,
  state: SourceHealthState,
  latest: DoctorResult["plugins"][number]["sources"][number]["health"]["latest"] = null,
) {
  return {
    name,
    url: `https://example.com/${name}`,
    engine: "static_html",
    engine_hint: null,
    health: { state, reason: state === "dead" ? "连续无产出" : "", observed: 5, latest, baseline: 2 },
    fingerprint_skips: { observed: 0, skipped: 0 },
  };
}

function fixturePlugin(overrides: Partial<DoctorResult["plugins"][number]>) {
  return {
    file: "tech.yaml",
    id: "tech",
    name: "科技资讯",
    schedule: "0 9 * * *",
    timezone: "Asia/Shanghai",
    push_channels: [],
    loaded: true,
    load_errors: null,
    sources: [],
    next_fire_at: "2026-10-03T09:00:00+08:00",
    enrich: null,
    ...overrides,
  };
}

function fixtureDoctor(overrides: Partial<DoctorResult> = {}): DoctorResult {
  return {
    command: "doctor",
    generated_at: "2026-10-02T12:00:00+00:00",
    db: "myssia.db",
    healthy: true,
    plugins: [
      fixturePlugin({
        sources: [fixtureSource("hn", "ok"), fixtureSource("gh", "ok"), fixtureSource("blog", "degraded")],
      }),
    ],
    credentials: { backend_available: true, backend_error: null, entries: [] },
    proxy: { config: null, pools: [] },
    findings: [],
    summary: { plugins: 1, sources: 3, errors: 0, warnings: 0 },
    ...overrides,
  };
}

let nextRunId = 0;
/** runs.list 历史行(runs 表直读形状,types.ts RunRecord) */
function fixtureHistoryRun(overrides: Partial<RunRecord> = {}): RunRecord {
  nextRunId += 1;
  return {
    run_id: nextRunId,
    category: "tech",
    status: "success",
    started_at: "2026-10-02T08:00:00+00:00",
    finished_at: "2026-10-02T08:00:01+00:00",
    stats: { items_retained: 5 },
    steps: null,
    error: null,
    ...overrides,
  };
}

/** run.status 内存注册表条目(仅活跃叠加用;entry.py `_m_run_status`) */
function fixtureRegistryRun(overrides: Partial<RunEntry> = {}): RunEntry {
  return {
    run_id: 9000,
    yaml: "/plugins/tech.yaml",
    db: "myssia.db",
    dry: false,
    state: "running",
    exit_code: null,
    status: null,
    started_at: "2026-10-03T08:00:00+00:00",
    finished_at: null,
    duration_ms: null,
    record: null,
    ...overrides,
  };
}

function mockSidecar(
  doctor: Promise<DoctorResult>,
  history: Promise<{ runs: RunRecord[] }>,
  registry: Promise<{ runs: RunEntry[] }> = Promise.resolve({ runs: [] }),
) {
  doctorMock.mockReturnValue(doctor);
  // runs.list 应答形 = RunsListResult(db/count/runs);夹具只给 runs,补外层
  runsListMock.mockReturnValue(history.then((payload) => ({ db: "myssia.db", count: payload.runs.length, ...payload })));
  runStatusMock.mockReturnValue(registry);
  // B2/B4/G6 三自取数卡:默认空态,不搅既有用例;专项用例自行覆写
  storeTrendMock.mockResolvedValue({ days: [] });
  runsTrendMock.mockResolvedValue({ days: [] });
  feedbackStatsMock.mockResolvedValue({
    window_days: 14,
    stats: {
      total: 0,
      good: 0,
      bad: 0,
      bad_ratio: 0,
      by_channel: {},
      top_bad_categories: [],
      top_bad_words: [],
    },
    active_tuning: {},
    tuning_history: [],
  });
}

afterEach(() => {
  cleanup(); // vitest globals 关闭,RTL 自动清理不生效,须显式清理
  vi.resetAllMocks();
  nextRunId = 0;
});

// Radix Select 2.x 在 jsdom 里开下拉需要的指针捕获/滚动桩(趋势时间范围切换用例)
beforeAll(() => {
  window.HTMLElement.prototype.hasPointerCapture = () => false;
  window.HTMLElement.prototype.releasePointerCapture = () => {};
  window.HTMLElement.prototype.scrollIntoView = () => {};
});

/**
 * ⓘ 悬停后取 tooltip 文案(R3 口径注记收悬停;触发方式照 ui-base.test.tsx
 * 基件自测先例:mouseEnter + 假时钟推进 300ms 开延迟,再查 role=tooltip;
 * 读完即 mouseLeave 关闭并两次推进卸载——离场卸载定时器在关闭拍 flush 后
 * 才排上,须再推进一拍;保证同用例多次悬停不残留多个 tooltip)。
 */
function hoverTooltip(trigger: HTMLElement): string {
  vi.useFakeTimers();
  try {
    fireEvent.mouseEnter(trigger);
    act(() => {
      vi.advanceTimersByTime(300); // openDelay 300
    });
    const content = screen.getByRole("tooltip").textContent ?? "";
    fireEvent.mouseLeave(trigger);
    act(() => {
      vi.advanceTimersByTime(300); // closeDelay 80 → state=closed
    });
    act(() => {
      vi.advanceTimersByTime(300); // EXIT_UNMOUNT_MS 120 卸载(上一拍 flush 时才排上)
    });
    return content;
  } finally {
    vi.useRealTimers();
  }
}

// ---------------------------------------------------------------------------
// 用例
// ---------------------------------------------------------------------------

describe("DashboardScreen", () => {
  it("渲染品类状态卡:健康品类=正常,载入失败品类=异常", async () => {
    mockSidecar(
      Promise.resolve(
        fixtureDoctor({
          plugins: [
            fixturePlugin({ file: "tech.yaml", sources: [fixtureSource("hn", "ok")] }),
            fixturePlugin({
              file: "broken.yaml",
              name: "坏品类",
              loaded: false,
              load_errors: [{ error_type: "config_error", path: "$", message: "schema 拒载" }],
            }),
          ],
          findings: [
            {
              severity: "error",
              scope: "plugin:broken.yaml",
              code: "config_error",
              message: "schema 拒载",
            },
          ],
          healthy: false,
          summary: { plugins: 2, sources: 1, errors: 1, warnings: 0 },
        }),
      ),
      Promise.resolve({ runs: [] }),
    );
    render(<DashboardScreen />);

    await screen.findByTestId("category-tech.yaml");
    // 「坏品类」现两处(品类卡 + 告警清单补位行),按卡断言不全局取
    expect(screen.getByTestId("category-broken.yaml").textContent).toContain("坏品类");
    const healthy = screen.getByTestId("category-tech.yaml");
    expect(healthy.textContent).toContain("正常");
    const broken = screen.getByTestId("category-broken.yaml");
    expect(broken.textContent).toContain("异常");
    expect(broken.textContent).toContain("未载入");
    expect(screen.getByTestId("dashboard-screen-root")).toBeTruthy();
  });

  it("源健康度汇总按四态计数(ok/degraded/dead/unknown)", async () => {
    mockSidecar(
      Promise.resolve(
        fixtureDoctor({
          plugins: [
            fixturePlugin({
              sources: [
                fixtureSource("a", "ok"),
                fixtureSource("b", "ok"),
                fixtureSource("c", "degraded"),
                fixtureSource("d", "dead"),
                fixtureSource("e", "unknown"),
              ],
            }),
          ],
        }),
      ),
      Promise.resolve({ runs: [] }),
    );
    render(<DashboardScreen />);

    await screen.findByTestId("category-tech.yaml");
    expect(screen.getByTestId("health-ok").textContent).toContain("2");
    expect(screen.getByTestId("health-degraded").textContent).toContain("1");
    expect(screen.getByTestId("health-dead").textContent).toContain("1");
    expect(screen.getByTestId("health-unknown").textContent).toContain("1");
  });

  it("最近采集成功率:8/10 成功 = 80%,活跃(run.status 叠加)不计入且单独标注", async () => {
    const history: RunRecord[] = [];
    for (let i = 0; i < 8; i += 1) history.push(fixtureHistoryRun({}));
    history.push(fixtureHistoryRun({ status: "partial" }));
    history.push(fixtureHistoryRun({ status: "failed" }));
    history.push(fixtureHistoryRun({ status: "running" })); // pipeline start_run 即写表
    // 协议契约:runs.list 新→旧(entry.py `_m_runs_list`),夹具反转为真实顺序;
    // 注册表活跃条目与之合并 → running 表行标 active(mergeDashboardRuns ①)
    mockSidecar(
      Promise.resolve(fixtureDoctor()),
      Promise.resolve({ runs: history.reverse() }),
      Promise.resolve({ runs: [fixtureRegistryRun()] }),
    );
    render(<DashboardScreen />);

    await screen.findByTestId("category-tech.yaml");
    expect(screen.getByTestId("run-success-rate").textContent).toBe("80%");
    expect(screen.getByTestId("run-success-rate").parentElement?.textContent).toContain("8/10 次成功");
    expect(screen.getByTestId("run-success-rate").parentElement?.textContent).toContain("1 个运行中");
    // 最近列表最多 10 条,且含最新(运行中)那条
    expect(screen.getByTestId(`recent-run-${nextRunId}`)).toBeTruthy();
    expect(screen.getAllByTestId(/^recent-run-/)).toHaveLength(10);
  });

  it("runs.list 历史可达:注册表空(sidecar 重启后)历史行仍上屏", async () => {
    // C3 验收的组件级形态:run.status 空(内存态随重启蒸发),仪表盘吃 runs.list
    mockSidecar(
      Promise.resolve(fixtureDoctor()),
      Promise.resolve({
        runs: [fixtureHistoryRun(), fixtureHistoryRun({ status: "cancelled" })], // 新→旧
      }),
      Promise.resolve({ runs: [] }),
    );
    render(<DashboardScreen />);

    await screen.findByTestId("category-tech.yaml");
    expect(screen.getByTestId("run-success-rate").textContent).toBe("50%");
    expect(screen.getByTestId(`recent-run-${nextRunId}`).textContent).toContain("已取消");
  });

  it("分区失败降级:doctor 挂而 runs 活 → 降级横幅(码+原因+重试指引)+ 其余分区照常渲染,不整屏报废", async () => {
    mockSidecar(
      Promise.reject(
        new SidecarRequestError({
          code: "config",
          path: "params.yamls",
          message: "品类 YAML 校验失败",
        }),
      ),
      Promise.resolve({ runs: [] }),
    );
    render(<DashboardScreen />);

    const banner = await screen.findByTestId("dashboard-section-errors");
    expect(banner.textContent).toContain("config");
    expect(banner.textContent).toContain("品类 YAML 校验失败");
    expect(banner.textContent).toContain("降级");
    expect(banner.textContent).toContain("刷新");
    expect(screen.getByTestId("dashboard-overview")).toBeTruthy();
    expect(screen.queryByTestId("dashboard-error")).toBeNull();
  });

  it("internal_error 单区失败 → 人话文案 + mono 码,不裸放 raw code", async () => {
    mockSidecar(
      Promise.reject(
        new SidecarRequestError({
          code: "internal_error",
          path: "$",
          message: "Traceback …",
        }),
      ),
      Promise.resolve({ runs: [] }),
    );
    render(<DashboardScreen />);

    const banner = await screen.findByTestId("dashboard-section-errors");
    expect(banner.textContent).toContain("核心内部错误");
    expect(banner.textContent).toContain("internal_error");
    expect(banner.textContent).not.toContain("Traceback");
  });

  it("空态:无品类、无 run 时给引导文案,成功率为 —(不虚构 0%)", async () => {
    mockSidecar(Promise.resolve(fixtureDoctor({ plugins: [] })), Promise.resolve({ runs: [] }));
    render(<DashboardScreen />);

    await screen.findByText("暂无品类");
    expect(screen.getByText(/还没有采集记录/)).toBeTruthy();
    expect(screen.getByTestId("run-success-rate").textContent).toBe("—");
  });

  // -------------------------------------------------------------------------
  // 10-05-dashboard-glance:D1 状态句(verdict)+ D3 告警清单 + dry→试跑
  // -------------------------------------------------------------------------

  it("verdict ok 态:屏首一行「一切正常 · 今日采集 X 条 · M/K 源在线」,ok 态纯文本", async () => {
    const today = new Date().toISOString().slice(0, 10);
    mockSidecar(
      Promise.resolve(
        fixtureDoctor({
          plugins: [
            fixturePlugin({
              sources: [fixtureSource("a", "ok"), fixtureSource("b", "ok"), fixtureSource("c", "ok")],
            }),
          ],
          findings: [],
        }),
      ),
      Promise.resolve({ runs: [] }),
    );
    storeTrendMock.mockResolvedValue({ days: [{ date: today, count: 128 }] });
    render(<DashboardScreen />);

    const verdict = await screen.findByTestId("dashboard-verdict");
    expect(verdict.textContent).toContain("一切正常");
    expect(verdict.textContent).toContain("今日采集 128 条");
    expect(verdict.textContent).toContain("3/3 源在线");
    expect(verdict.getAttribute("role")).toBe("status");
    expect(verdict.getAttribute("aria-label")).toContain("一切正常 · 今日采集 128 条");
    expect(verdict.tagName).toBe("DIV"); // ok 态纯文本,非链接
    // 屏首块:先于概览 section(无头范式首块)
    expect(
      verdict.compareDocumentPosition(screen.getByTestId("dashboard-overview")) &
        Node.DOCUMENT_POSITION_FOLLOWING,
    ).toBeTruthy();
  });

  it("verdict dead 态:dead 源升「N 个源失效」,整行可点跳源管理", async () => {
    mockSidecar(
      Promise.resolve(
        fixtureDoctor({
          plugins: [
            fixturePlugin({
              sources: [fixtureSource("a", "ok"), fixtureSource("b", "ok"), fixtureSource("deadone", "dead")],
            }),
          ],
          findings: [],
        }),
      ),
      Promise.resolve({ runs: [] }),
    );
    render(<DashboardScreen />);

    const verdict = await screen.findByTestId("dashboard-verdict");
    expect(verdict.textContent).toContain("1 个源失效");
    expect(verdict.textContent).toContain("2/3 源在线");
    expect(verdict.tagName).toBe("A");
    expect(verdict.getAttribute("href")).toBe("#/sources");
  });

  it("verdict warning 态:告警/退化拼段缺段省略,facts 随概览窗切 7 天换窗文案(grill Q1)", async () => {
    const today = new Date().toISOString().slice(0, 10);
    mockSidecar(
      Promise.resolve(
        fixtureDoctor({
          plugins: [fixturePlugin({ sources: [fixtureSource("a", "ok"), fixtureSource("b", "degraded")] })],
          findings: [
            { severity: "warning", scope: "plugin:tech.yaml", code: "env_ref_missing", message: "缺环境变量" },
          ],
        }),
      ),
      Promise.resolve({ runs: [] }),
    );
    storeTrendMock.mockResolvedValue({ days: [{ date: today, count: 4 }] });
    render(<DashboardScreen />);

    const verdict = await screen.findByTestId("dashboard-verdict");
    expect(verdict.textContent).toContain("1 项告警 · 1 个源退化");
    expect(verdict.getAttribute("href")).toBe("#/sources");

    // 概览窗切 7 天 → facts 采集段换「近 7 天采集 …」(与四格同窗同数)
    storeTrendMock.mockResolvedValue({ days: [{ date: today, count: 9 }] });
    fireEvent.pointerDown(screen.getByRole("combobox", { name: "概览时间范围" }), {
      button: 0,
      ctrlKey: false,
      pointerType: "mouse",
    });
    fireEvent.click(await screen.findByRole("option", { name: "7 天" }));
    await waitFor(() =>
      expect(screen.getByTestId("dashboard-verdict").textContent).toContain("近 7 天采集 9 条"),
    );
    expect(screen.getByTestId("dashboard-verdict").textContent).not.toContain("今日采集");
  });

  it("verdict unknown 态:doctor 分区失败 → 「部分数据不可达,状态未知 · 其余分区已降级显示」", async () => {
    mockSidecar(
      Promise.reject(
        new SidecarRequestError({ code: "internal_error", path: "$", message: "Traceback …" }),
      ),
      Promise.resolve({ runs: [] }),
    );
    render(<DashboardScreen />);

    const verdict = await screen.findByTestId("dashboard-verdict");
    expect(verdict.textContent).toContain("部分数据不可达,状态未知");
    expect(verdict.textContent).toContain("其余分区已降级显示");
    expect(verdict.textContent).not.toContain("源在线"); // doctor 挂 → 缺数省略,不虚构
    expect(verdict.tagName).toBe("DIV"); // unknown 态纯文本
  });

  it("verdict 不抢跑:数据整体未到(加载态/整屏错误)不渲染,零双报", () => {
    const never = <T,>() => new Promise<T>(() => {});
    mockSidecar(never<DoctorResult>(), never<{ runs: RunRecord[] }>());
    render(<DashboardScreen />);

    expect(screen.queryByTestId("dashboard-verdict")).toBeNull();
  });

  it("告警清单(仅坏源口径):坏源行优先前三条可点跳源管理,溢出口如实计", async () => {
    mockSidecar(
      Promise.resolve(
        fixtureDoctor({
          plugins: [
            fixturePlugin({
              sources: [
                fixtureSource("a", "ok"),
                fixtureSource("deadone", "dead"),
                fixtureSource("degradedone", "degraded"),
                fixtureSource("unknownone", "unknown"),
                fixtureSource("deadtwo", "dead"),
              ],
            }),
          ],
          findings: [],
        }),
      ),
      Promise.resolve({ runs: [] }),
    );
    render(<DashboardScreen />);

    const list = await screen.findByTestId("dashboard-alert-list");
    const rows = screen.getAllByTestId(/^alert-row-/);
    expect(rows).toHaveLength(3); // grill Q4:三条封顶
    for (const row of rows) expect(row.getAttribute("href")).toBe("#/sources");
    // 异常优先排序:dead 两行居前(buildSourceHealthCards dead→degraded→unknown)
    expect(rows[0].textContent).toContain("失效");
    expect(rows[1].textContent).toContain("失效");
    expect(rows[2].textContent).toContain("退化");
    // 行内容:状态点+词 / 源名 / 品类名 / reason 原文直用 / 相对时间右置
    expect(rows[0].textContent).toContain("deadone");
    expect(rows[0].textContent).toContain("科技资讯");
    expect(rows[0].textContent).toContain("连续无产出"); // reason 原文直用,零映射
    expect(rows[0].textContent).toContain("—"); // 「品类名 — reason」分隔形态
    // 溢出口:4 坏源 − 3 行 = 1(如实计)
    const overflow = screen.getByTestId("dashboard-alert-overflow");
    expect(overflow.textContent).toContain("还有 1 个异常 · 查看全部 →");
    expect(overflow.getAttribute("href")).toBe("#/sources");
    expect(list).toBeTruthy();
  });

  it("告警清单(仅 findings 口径,零坏源):品类级 finding 补位行(品类名+message 原文)", async () => {
    mockSidecar(
      Promise.resolve(
        fixtureDoctor({
          plugins: [fixturePlugin({ sources: [fixtureSource("a", "ok")] })],
          findings: [
            { severity: "error", scope: "plugin:tech.yaml", code: "credentials", message: "缺凭据" },
          ],
        }),
      ),
      Promise.resolve({ runs: [] }),
    );
    render(<DashboardScreen />);

    const rows = await screen.findAllByTestId(/^alert-row-/);
    expect(screen.getByTestId("dashboard-alert-list")).toBeTruthy();
    expect(rows).toHaveLength(1);
    expect(rows[0].textContent).toContain("异常"); // error → 异常词(不只靠色)
    expect(rows[0].textContent).toContain("科技资讯"); // 品类名
    expect(rows[0].textContent).toContain("缺凭据"); // finding.message 原文
    expect(rows[0].getAttribute("title")).toBe("缺凭据"); // title=全文
    expect(screen.queryByTestId("dashboard-alert-overflow")).toBeNull(); // 无溢出
  });

  it("告警清单补位:坏源不足 3 行时品类级 findings 补满(坏源行优先,source 级 finding 不入清单)", async () => {
    mockSidecar(
      Promise.resolve(
        fixtureDoctor({
          plugins: [fixturePlugin({ sources: [fixtureSource("deadone", "dead"), fixtureSource("a", "ok")] })],
          findings: [
            { severity: "error", scope: "plugin:tech.yaml", code: "credentials", message: "缺凭据" },
            { severity: "warning", scope: "plugin:tech.yaml/source:a", code: "env_ref_missing", message: "缺环境变量" },
          ],
        }),
      ),
      Promise.resolve({ runs: [] }),
    );
    render(<DashboardScreen />);

    const rows = await screen.findAllByTestId(/^alert-row-/);
    expect(rows).toHaveLength(2); // 1 坏源行 + 1 品类级补位行
    expect(rows[0].textContent).toContain("deadone"); // 坏源行优先
    expect(rows[0].getAttribute("href")).toBe("#/sources");
    expect(rows[1].textContent).toContain("科技资讯");
    expect(rows[1].textContent).toContain("异常");
    expect(rows[1].textContent).toContain("缺凭据");
    expect(screen.queryByTestId("dashboard-alert-overflow")).toBeNull();
  });

  it("告警清单零占位:告警与坏源皆零时不渲染", async () => {
    mockSidecar(
      Promise.resolve(
        fixtureDoctor({
          plugins: [fixturePlugin({ sources: [fixtureSource("a", "ok")] })],
          findings: [],
        }),
      ),
      Promise.resolve({ runs: [] }),
    );
    render(<DashboardScreen />);

    await screen.findByTestId("category-tech.yaml");
    expect(screen.queryByTestId("dashboard-alert-list")).toBeNull();
  });

  it("试跑徽标:dry 活跃行标「试跑」,title 留 dry run 技术注(dry→试跑,10-05-dashboard-glance)", async () => {
    mockSidecar(
      Promise.resolve(fixtureDoctor()),
      Promise.resolve({ runs: [] }), // 无表行 → 注册表活跃 dry run 前插合成行
      Promise.resolve({ runs: [fixtureRegistryRun({ dry: true })] }),
    );
    render(<DashboardScreen />);

    const row = await screen.findByTestId("recent-run-9000");
    expect(row.textContent).toContain("试跑");
    const badge = row.querySelector('[data-slot="badge"]');
    expect(badge?.getAttribute("title")).toBe("dry run(不落库)");
  });

  it("刷新数据钮:嵌概览卡头(不占独立行),点击重拉 doctor/run.status/趋势,loading 期自转", async () => {
    mockSidecar(Promise.resolve(fixtureDoctor()), Promise.resolve({ runs: [] }));
    // 第二次 doctor 应答挂起(手放行),冻结 loading 态供自转/禁用断言
    let release: ((value: DoctorResult) => void) | undefined;
    doctorMock.mockImplementationOnce(() => Promise.resolve(fixtureDoctor()));
    doctorMock.mockImplementationOnce(
      () => new Promise<DoctorResult>((resolve) => {
        release = resolve;
      }),
    );
    render(<DashboardScreen />);
    await screen.findByTestId("category-tech.yaml");
    expect(doctorMock).toHaveBeenCalledTimes(1);

    const refreshBtn = screen.getByRole("button", { name: "刷新数据" });
    // 嵌在概览条卡头右上(不占独立行);独立刷新行已撤
    expect(refreshBtn.closest("section")?.getAttribute("data-testid")).toBe("dashboard-overview");
    expect(screen.queryByTestId("dashboard-toolbar")).toBeNull();
    expect((refreshBtn as HTMLButtonElement).disabled).toBe(false);

    const trendCallsBefore = storeTrendMock.mock.calls.length;
    fireEvent.click(refreshBtn);
    // loading 期:禁用 + RefreshCw 自转
    await waitFor(() =>
      expect((screen.getByRole("button", { name: "刷新数据" }) as HTMLButtonElement).disabled).toBe(true),
    );
    expect(
      screen.getByRole("button", { name: "刷新数据" }).querySelector("svg")?.getAttribute("class"),
    ).toContain("animate-spin");
    // 趋势同窗重查(refreshTrend + 概览窗各一笔)
    await waitFor(() => expect(storeTrendMock.mock.calls.length).toBe(trendCallsBefore + 2));

    act(() => release?.(fixtureDoctor()));
    await waitFor(() => expect(doctorMock).toHaveBeenCalledTimes(2));
    expect(runStatusMock).toHaveBeenCalledTimes(2);
    await waitFor(() =>
      expect((screen.getByRole("button", { name: "刷新数据" }) as HTMLButtonElement).disabled).toBe(false),
    );
    expect(
      screen.getByRole("button", { name: "刷新数据" }).querySelector("svg")?.getAttribute("class"),
    ).not.toContain("animate-spin");
  });

  // -------------------------------------------------------------------------
  // D4/D5(10-03-ui-deep-imitation):概览条 / 趋势 sparkline / 源健康卡网格
  // (对照 teardown-vercel-dashboard #2/#3/#4/#6)
  // -------------------------------------------------------------------------

  it("概览条(D4):今日采集=trend 右端 / 活跃源=ok+degraded / 推送成功=今日 run 的 push ok / 告警=findings", async () => {
    const today = new Date().toISOString().slice(0, 10);
    mockSidecar(
      Promise.resolve(
        fixtureDoctor({
          plugins: [
            fixturePlugin({
              sources: [
                fixtureSource("a", "ok"),
                fixtureSource("b", "degraded"),
                fixtureSource("c", "dead"),
                fixtureSource("d", "unknown"),
              ],
            }),
          ],
          findings: [
            { severity: "error", scope: "plugin:tech.yaml", code: "credentials", message: "缺凭据" },
            { severity: "warning", scope: "plugin:tech.yaml", code: "env_ref_missing", message: "缺环境变量" },
          ],
        }),
      ),
      Promise.resolve({
        runs: [
          fixtureHistoryRun({
            started_at: `${today}T08:00:00+00:00`,
            stats: {
              items_retained: 5,
              push: [
                { channel: "tg", ok: true },
                { channel: "feishu", ok: false },
                { channel: "mail", ok: true },
              ],
            },
          }),
        ],
      }),
    );
    storeTrendMock.mockResolvedValue({ days: [{ date: today, count: 5 }] });
    render(<DashboardScreen />);

    await screen.findByTestId("category-tech.yaml");
    await waitFor(() => expect(screen.getByTestId("stat-window-items").textContent).toContain("5"));
    expect(screen.getByText("今日采集")).toBeTruthy(); // 默认今日档,口径不动
    // R4 数字带分母:活跃源 2/4(ok+degraded / 总数;tnum 全局已开)
    expect(screen.getByTestId("stat-active-sources").textContent).toContain("2/4");
    // R3 口径注记收 ⓘ 悬停:扫读面无口径明文,悬停后可查
    expect(screen.getByTestId("stat-active-sources").textContent).not.toContain("共 4 源");
    expect(hoverTooltip(screen.getByRole("button", { name: "活跃源说明" }))).toContain(
      "共 4 源 · ok+degraded",
    );
    expect(screen.getByTestId("stat-window-items").textContent).not.toContain("UTC 日口径");
    expect(hoverTooltip(screen.getByRole("button", { name: "今日采集说明" }))).toContain(
      "UTC 日口径 · items 入库",
    );
    // hover note 人话化(D9):「各轮采集的推送成功数 · 受最近 20 轮上限(runs.list)」
    expect(hoverTooltip(screen.getByRole("button", { name: "推送成功说明" }))).toContain(
      "受最近 20 轮上限(runs.list)",
    );
    expect(screen.getByTestId("stat-window-push").textContent).toContain("2"); // 2 次 ok 推送
    expect(screen.getByTestId("stat-alerts").textContent).toContain("2"); // error+warning 各一
    expect(screen.getByTestId("dashboard-overview")).toBeTruthy();
    expect(storeTrendMock).toHaveBeenCalledWith({ days: 1 }); // A-dash:概览独立 1 天窗
  });

  it("A-dash 概览窗口:Select 切 7 天 → 采集格=窗口求和、推送格吃窗口内 run;活跃源/告警保持快照并注记", async () => {
    const today = new Date().toISOString().slice(0, 10);
    const yesterday = new Date(Date.now() - 86_400_000).toISOString().slice(0, 10);
    const twoDaysAgo = new Date(Date.now() - 2 * 86_400_000).toISOString().slice(0, 10);
    mockSidecar(
      Promise.resolve(
        fixtureDoctor({
          plugins: [
            fixturePlugin({
              sources: [fixtureSource("a", "ok"), fixtureSource("b", "ok"), fixtureSource("c", "degraded")],
            }),
          ],
          findings: [
            { severity: "warning", scope: "plugin:tech.yaml", code: "env_ref_missing", message: "缺环境变量" },
          ],
        }),
      ),
      Promise.resolve({
        runs: [
          // 昨日 run:2 次 ok 推送(今日档不入窗,7 天档入窗)
          fixtureHistoryRun({
            started_at: `${yesterday}T08:00:00+00:00`,
            stats: {
              items_retained: 3,
              push: [
                { channel: "tg", ok: true },
                { channel: "tg", ok: true },
                { channel: "mail", ok: false },
              ],
            },
          }),
          // 前日 run:0 次 ok 推送
          fixtureHistoryRun({
            started_at: `${twoDaysAgo}T08:00:00+00:00`,
            stats: { items_retained: 2, push: [{ channel: "mail", ok: false }] },
          }),
        ],
      }),
    );
    storeTrendMock.mockResolvedValue({
      days: [
        { date: twoDaysAgo, count: 2 },
        { date: yesterday, count: 3 },
        { date: today, count: 4 },
      ],
    });
    render(<DashboardScreen />);

    // 默认今日档:采集=当日 4;推送=—(今日无 run,不虚构 0)
    await waitFor(() => expect(screen.getByTestId("stat-window-items").textContent).toContain("4"));
    expect(screen.getByTestId("stat-window-push").textContent).toContain("—");

    // 概览 Select 切 7 天(与趋势卡 Select 同款交互;Radix 需 mouse 型 pointerDown)
    fireEvent.pointerDown(screen.getByRole("combobox", { name: "概览时间范围" }), {
      button: 0,
      ctrlKey: false,
      pointerType: "mouse",
    });
    const option = await screen.findByRole("option", { name: "7 天" });
    fireEvent.click(option);
    await waitFor(() => expect(storeTrendMock).toHaveBeenCalledWith({ days: 7 })); // 独立重查

    // 采集格 = 窗口求和 2+3+4=9;推送格 = 窗口内 run 的 ok 计数 2
    await waitFor(() => expect(screen.getByTestId("stat-window-items").textContent).toContain("9"));
    expect(screen.getByText("近 7 天采集")).toBeTruthy();
    await waitFor(() => expect(screen.getByTestId("stat-window-push").textContent).toContain("2"));

    // 两格快照:活跃源(ok 2 + degraded 1 → 活跃 3/3)、告警(findings 1)不随窗;
    // 「即时快照不随窗」口径注记收 ⓘ 悬停(R3),textContent 不再明文
    expect(screen.getByTestId("stat-active-sources").textContent).toContain("3/3");
    expect(screen.getByTestId("stat-active-sources").textContent).not.toContain("即时快照不随窗");
    expect(hoverTooltip(screen.getByRole("button", { name: "活跃源说明" }))).toContain(
      "即时快照不随窗",
    );
    expect(screen.getByTestId("stat-alerts").textContent).toContain("1");
    expect(hoverTooltip(screen.getByRole("button", { name: "告警说明" }))).toContain(
      "即时快照不随窗",
    );
  });

  it("趋势(D4/D5):sparkline 画补零等长窗口(默认 14 点),Select 切 7 天重查 store.trend", async () => {
    const today = new Date().toISOString().slice(0, 10);
    mockSidecar(Promise.resolve(fixtureDoctor()), Promise.resolve({ runs: [] }));
    storeTrendMock.mockResolvedValue({ days: [{ date: today, count: 3 }] });
    render(<DashboardScreen />);

    const spark = await screen.findByTestId("dashboard-sparkline");
    const polyline = spark.querySelector("polyline");
    expect(polyline).toBeTruthy();
    expect(polyline?.getAttribute("points")?.trim().split(/\s+/)).toHaveLength(14); // 补零 = 等长序列
    expect(screen.getByTestId("trend-total").textContent).toContain("共 3 条");
    expect(storeTrendMock).toHaveBeenCalledWith({ days: 14 }); // 默认窗口

    // Select 时间范围切换(teardown #6):Radix 下拉仅对 mouse 型 pointerDown 开
    // (react-select dist index.mjs:214 的 pointerType==="mouse" 门)→ 显式带 pointerType
    fireEvent.pointerDown(screen.getByRole("combobox", { name: "趋势时间范围" }), {
      button: 0,
      ctrlKey: false,
      pointerType: "mouse",
    });
    const option = await screen.findByRole("option", { name: "7 天" });
    fireEvent.click(option);
    await waitFor(() => expect(storeTrendMock).toHaveBeenCalledWith({ days: 7 }));
  });

  it("趋势独立降级:store.trend 拒绝 → 趋势卡显错、概览采集格如实 — 且注记错误码,doctor 区块照常", async () => {
    mockSidecar(Promise.resolve(fixtureDoctor()), Promise.resolve({ runs: [] }));
    storeTrendMock.mockRejectedValue(
      new SidecarRequestError({ code: "db_locked", path: "$", message: "数据库被锁" }),
    );
    render(<DashboardScreen />);

    const trendError = await screen.findByTestId("dashboard-trend-error");
    expect(trendError.textContent).toContain("db_locked");
    await waitFor(() => expect(screen.getByTestId("stat-window-items").textContent).toContain("—"));
    expect(screen.getByTestId("stat-window-items").textContent).toContain("db_locked"); // A-dash 降级注记
    expect(screen.getByTestId("category-tech.yaml")).toBeTruthy();
  });

  it("源健康度卡网格(D4):四态卡 + 异常源(dead)排前 + 观测时间锚回 runs.list + 无观测显 —", async () => {
    // 90 分钟前启动的 run(留 ~30 分钟余量,相对时间稳定落「1 小时前」)
    const observedRunStarted = new Date(Date.now() - 90 * 60_000).toISOString();
    const observedRun = fixtureHistoryRun({
      started_at: observedRunStarted,
      finished_at: new Date().toISOString(),
    });
    const plugin = fixturePlugin({
      sources: [
        fixtureSource("hn", "ok", {
          run_id: observedRun.run_id,
          run_status: "success",
          item_count: 5,
          skip_reason: null,
          failed: false,
        }),
        fixtureSource("deadone", "dead"),
        fixtureSource("fresh", "unknown"),
      ],
    });
    mockSidecar(
      Promise.resolve(fixtureDoctor({ plugins: [plugin] })),
      Promise.resolve({ runs: [observedRun] }),
    );
    render(<DashboardScreen />);

    const okCard = await screen.findByTestId("source-card-tech.yaml#hn");
    expect(okCard.textContent).toContain("正常");
    expect(okCard.textContent).toContain("1 小时前"); // latest.run_id → runs.list startedAt
    expect(okCard.textContent).toContain("最近 5 条");
    expect(screen.getByTestId("source-health-grid")).toBeTruthy();

    // 异常优先:dead 卡排在 ok 卡之前(buildSourceHealthCards 状态序)
    const deadCard = screen.getByTestId("source-card-tech.yaml#deadone");
    expect(deadCard.textContent).toContain("失效");
    expect(deadCard.compareDocumentPosition(okCard) & Node.DOCUMENT_POSITION_FOLLOWING).toBeTruthy();

    // 无观测(latest=null)→ 相对时间如实 —
    expect(screen.getByTestId("source-card-tech.yaml#fresh").textContent).toContain("—");
  });

  // -------------------------------------------------------------------------
  // G4(10-03-feed-ux):品类卡「跑一次」状态机(照抄 feed 空态 CTA)
  // -------------------------------------------------------------------------

  it("跑一次:run.start(yaml)→ completed 事件 → 刷新;busy 期按钮禁用", async () => {
    mockSidecar(Promise.resolve(fixtureDoctor()), Promise.resolve({ runs: [] }));
    runStartMock.mockResolvedValue({
      run_id: 7, state: "running", yaml: "tech.yaml", dry: false, db: "myssia.db",
    });
    let emitEvent: ((event: { type: string; run_id: number }) => void) | undefined;
    onSidecarEventMock.mockImplementation((handler: (event: never) => void) => {
      emitEvent = handler as (event: { type: string; run_id: number }) => void;
      return Promise.resolve(() => {});
    });
    render(<DashboardScreen />);
    await screen.findByTestId("category-tech.yaml");

    const runOnce = screen.getByRole("button", { name: "跑一次:科技资讯" });
    fireEvent.click(runOnce);
    await waitFor(() => expect(runStartMock).toHaveBeenCalledWith({ yaml: "tech.yaml" }));
    // busy(collecting)期按钮禁用,防重复发起
    await waitFor(() =>
      expect((screen.getByRole("button", { name: "跑一次:科技资讯" }) as HTMLButtonElement).disabled).toBe(true),
    );

    const doctorCallsBefore = doctorMock.mock.calls.length;
    act(() => emitEvent?.({ type: "completed", run_id: 7 }));
    await waitFor(() => expect(doctorMock.mock.calls.length).toBeGreaterThan(doctorCallsBefore));
    await waitFor(() =>
      expect((screen.getByRole("button", { name: "跑一次:科技资讯" }) as HTMLButtonElement).disabled).toBe(false),
    );
  });

  it("跑一次错误路径:run_busy 结构化拒绝行内回显,按钮回可用", async () => {
    mockSidecar(Promise.resolve(fixtureDoctor()), Promise.resolve({ runs: [] }));
    runStartMock.mockRejectedValue(
      new SidecarRequestError({ code: "run_busy", path: "$", message: "已有 run 在执行" }),
    );
    onSidecarEventMock.mockResolvedValue(() => {});
    render(<DashboardScreen />);
    await screen.findByTestId("category-tech.yaml");

    fireEvent.click(screen.getByRole("button", { name: "跑一次:科技资讯" }));
    const errorLine = await screen.findByTestId("run-once-error-tech.yaml");
    expect(errorLine.textContent).toContain("run_busy");
    expect((screen.getByRole("button", { name: "跑一次:科技资讯" }) as HTMLButtonElement).disabled).toBe(false);
  });

  // -------------------------------------------------------------------------
  // G6(10-04-desktop-b234):成功率趋势第二序列(runs.trend)
  // -------------------------------------------------------------------------

  it("G6 成功率折线:running 不入分母、零完结日不入线、max=1 固定 [0,1] 刻度,摘要 = 累计口径", async () => {
    const today = new Date().toISOString().slice(0, 10);
    const yesterday = new Date(Date.now() - 86_400_000).toISOString().slice(0, 10);
    const beforeYesterday = new Date(Date.now() - 2 * 86_400_000).toISOString().slice(0, 10);
    mockSidecar(Promise.resolve(fixtureDoctor()), Promise.resolve({ runs: [] }));
    runsTrendMock.mockResolvedValue({
      days: [
        // 前天:3 个 run 全 running(零完结)→ 不入线
        { date: beforeYesterday, total: 3, statuses: { running: 3 } },
        // 昨天:2/5 成功 = 0.4
        { date: yesterday, total: 5, statuses: { success: 2, partial: 3 } },
        // 今天:12 run 含 running 2 → finished 10、success 8 = 0.8(running 不入分母)
        { date: today, total: 12, statuses: { success: 8, running: 2, failed: 2 } },
      ],
    });
    render(<DashboardScreen />);

    const rate = await screen.findByTestId("dashboard-rate-sparkline");
    const polyline = rate.querySelector("polyline");
    expect(polyline).toBeTruthy();
    // 固定 [0,1] 刻度(max=1):0.4 → y=3+42*0.6=28.2;0.8 → y=3+42*0.2=11.4。
    // max 归一会让 0.8 贴顶(3.0)、0.4 半程(24.0)—— 本断言即真刻度护栏。
    expect(polyline?.getAttribute("points")).toBe("3.0,28.2 257.0,11.4");
    // 摘要 = 累计口径(非均值):finished 15(10+5)、success 10 → 67%
    const summary = screen.getByTestId("rate-summary");
    expect(summary.textContent).toContain("近 14 天累计成功率 67%(10/15 次成功)");
    expect(rate.getAttribute("aria-label")).toContain("无完结采集的日子不入线");
    expect(runsTrendMock).toHaveBeenCalledWith({ days: 14 }); // 与采集量同默认窗口
  });

  it("G6 窗口切换:Select 切 7 天 → runs.trend 与 store.trend 同窗重查", async () => {
    const today = new Date().toISOString().slice(0, 10);
    mockSidecar(Promise.resolve(fixtureDoctor()), Promise.resolve({ runs: [] }));
    storeTrendMock.mockResolvedValue({ days: [{ date: today, count: 3 }] });
    runsTrendMock.mockResolvedValue({
      days: [{ date: today, total: 4, statuses: { success: 4 } }],
    });
    render(<DashboardScreen />);
    await screen.findByTestId("dashboard-rate-sparkline");

    fireEvent.pointerDown(screen.getByRole("combobox", { name: "趋势时间范围" }), {
      button: 0,
      ctrlKey: false,
      pointerType: "mouse",
    });
    const option = await screen.findByRole("option", { name: "7 天" });
    fireEvent.click(option);
    await waitFor(() => expect(runsTrendMock).toHaveBeenCalledWith({ days: 7 }));
    await waitFor(() => expect(storeTrendMock).toHaveBeenCalledWith({ days: 7 }));
  });

  it("G6 独立降级(双向):runs.trend 挂 → 成功率区人话错误、采集量照画;store.trend 挂 → 采集量显错、成功率照画", async () => {
    const today = new Date().toISOString().slice(0, 10);
    // 正向:runs.trend 拒
    mockSidecar(Promise.resolve(fixtureDoctor()), Promise.resolve({ runs: [] }));
    storeTrendMock.mockResolvedValue({ days: [{ date: today, count: 3 }] });
    runsTrendMock.mockRejectedValue(
      new SidecarRequestError({ code: "transport_error", path: "$", message: "与核心的连接异常" }),
    );
    const { unmount } = render(<DashboardScreen />);

    const rateError = await screen.findByTestId("dashboard-rate-error");
    expect(rateError.textContent).toContain("与核心的连接异常"); // 人话文案(fbbaaa7 判例)
    expect(rateError.textContent).toContain("[transport_error]"); // mono 码如实,不裸放 raw
    await waitFor(() => expect(screen.getByTestId("dashboard-sparkline").querySelector("polyline")).toBeTruthy());
    unmount();

    // 反向:store.trend 拒、runs.trend 活
    mockSidecar(Promise.resolve(fixtureDoctor()), Promise.resolve({ runs: [] }));
    storeTrendMock.mockRejectedValue(
      new SidecarRequestError({ code: "db_locked", path: "$", message: "数据库被锁" }),
    );
    runsTrendMock.mockResolvedValue({
      days: [{ date: today, total: 2, statuses: { success: 1, failed: 1 } }],
    });
    render(<DashboardScreen />);

    await screen.findByTestId("dashboard-trend-error");
    const rateSpark = await screen.findByTestId("dashboard-rate-sparkline");
    expect(rateSpark.querySelector("polyline")).toBeTruthy(); // allSettled 分流,互不连带
  });

  it("G6 空态:全窗口零完结 run → 如实提示,不画 0% 平线", async () => {
    mockSidecar(Promise.resolve(fixtureDoctor()), Promise.resolve({ runs: [] }));
    runsTrendMock.mockResolvedValue({ days: [] }); // 全窗口零 run(含缺省空库)
    render(<DashboardScreen />);

    const empty = await screen.findByTestId("dashboard-rate-empty");
    expect(empty.textContent).toContain("无已完结采集");
    expect(screen.queryByTestId("dashboard-rate-sparkline")).toBeNull(); // 不虚构 0%/100%
    expect(screen.queryByTestId("dashboard-rate-error")).toBeNull();
  });
});

// ---------------------------------------------------------------------------
// api 纯函数(原 B4 死组件测试承载;10-04-desktop-b234 删死组件时迁此续命
// ——fillDailyCounts/shiftUtcDate/toSparklinePoints 仍是 api.ts 活函数)
// ---------------------------------------------------------------------------

describe("fillDailyCounts 聚合(B4 验收落点;死组件测试迁入)", () => {
  it("补零天:稀疏行铺满窗口,缺数日 count=0,旧→新稳定输出", () => {
    const rows: TrendDay[] = [
      { date: "2026-10-03", count: 4 },
      { date: "2026-09-30", count: 1 },
    ];
    const filled = fillDailyCounts(rows, 7, "2026-10-03");
    expect(filled).toHaveLength(7);
    expect(filled.map((day) => day.date)).toEqual([
      "2026-09-27",
      "2026-09-28",
      "2026-09-29",
      "2026-09-30",
      "2026-10-01",
      "2026-10-02",
      "2026-10-03",
    ]);
    expect(filled.map((day) => day.count)).toEqual([0, 0, 0, 1, 0, 0, 4]);
  });

  it("窗口裁剪:窗口外行丢弃(更早日期不带入);非法日期行防御性忽略", () => {
    const rows: TrendDay[] = [
      { date: "2020-01-01", count: 99 },
      { date: "2026-10-02", count: 2 },
      { date: "not-a-date", count: 7 },
    ];
    const filled = fillDailyCounts(rows, 3, "2026-10-03");
    expect(filled.map((day) => day.count)).toEqual([0, 2, 0]);
  });

  it("空态 = 全零窗口(不是空数组;sparkline 需等长序列)", () => {
    const filled = fillDailyCounts([], 14, "2026-10-03");
    expect(filled).toHaveLength(14);
    expect(filled.every((day) => day.count === 0)).toBe(true);
  });

  it("days 非法(0/负/小数)= 空数组(防御,不抛)", () => {
    expect(fillDailyCounts([], 0, "2026-10-03")).toEqual([]);
    expect(fillDailyCounts([], -3, "2026-10-03")).toEqual([]);
    expect(fillDailyCounts([], 2.5, "2026-10-03")).toEqual([]);
  });

  it("shiftUtcDate:UTC 字符历法加减(跨月/跨年正确,不经本地时区)", () => {
    expect(shiftUtcDate("2026-10-03", -1)).toBe("2026-10-02");
    expect(shiftUtcDate("2026-10-01", -1)).toBe("2026-09-30");
    expect(shiftUtcDate("2026-01-01", -1)).toBe("2025-12-31");
    expect(shiftUtcDate("2026-02-28", 1)).toBe("2026-03-01"); // 2026 非闰年
    expect(shiftUtcDate("bad", 1)).toBe("bad");
  });
});

describe("toSparklinePoints(死组件测试迁入)", () => {
  it("按 max 归一:峰值贴上边、零贴下边,点数 = 输入长度", () => {
    const points = toSparklinePoints([0, 5, 10], 100, 50, 5).split(" ");
    expect(points).toHaveLength(3);
    const [, mid, top] = points.map((point) => point.split(",").map(Number));
    expect(mid[1]).toBe(30 - 5); // (5/10) 半程:pad + span*(1-0.5) = 5+40*0.5=25
    expect(top[1]).toBe(5); // 峰值贴 pad
  });

  it("全零 = 居中平线(不除零);空输入/过小画布 = 空串", () => {
    const flat = toSparklinePoints([0, 0, 0], 100, 50, 5).split(" ");
    expect(flat.every((point) => point.split(",")[1] === "25.0")).toBe(true);
    expect(toSparklinePoints([], 100, 50)).toBe("");
    expect(toSparklinePoints([1], 4, 4)).toBe("");
  });

  it("单点居中(x = width/2,不除零)", () => {
    expect(toSparklinePoints([7], 100, 50, 5)).toBe("50.0,5.0");
  });
});

describe("G6 成功率装配纯函数(10-04-desktop-b234)", () => {
  const rows: RunOutcomeDay[] = [
    { date: "2026-10-01", total: 3, statuses: { running: 3 } }, // 零完结 → 不入序
    { date: "2026-10-02", total: 5, statuses: { success: 2, partial: 3 } }, // 0.4
    { date: "2026-10-03", total: 12, statuses: { success: 8, running: 2, failed: 2 } }, // running 不入分母 → 0.8
  ];

  it("fillDailyOutcomes:补零对齐镜像 fillDailyCounts,缺数日 total 0", () => {
    const filled = fillDailyOutcomes([rows[1]], 3, "2026-10-03");
    expect(filled.map((day) => day.date)).toEqual(["2026-10-01", "2026-10-02", "2026-10-03"]);
    expect(filled[0]).toEqual({ date: "2026-10-01", total: 0, statuses: {} });
    expect(filled[2]).toEqual({ date: "2026-10-03", total: 0, statuses: {} });
    expect(fillDailyOutcomes([], 0, "2026-10-03")).toEqual([]); // 非法 days 防御
  });

  it("successRateSeries:running 不入分母、零完结日不入序(不虚构 0%/100%)", () => {
    const series = successRateSeries(rows);
    expect(series).toEqual([
      { date: "2026-10-02", rate: 0.4 },
      { date: "2026-10-03", rate: 0.8 },
    ]);
    // 若 running 入分母,今天会是 8/12≈0.667 —— 0.8 即分母剔除的数值断言
    expect(successRateSeries([{ date: "2026-10-01", total: 4, statuses: { running: 4 } }])).toEqual([]);
  });

  it("cumulativeOutcomeSummary:窗口累计口径(finished=Σ(total−running))", () => {
    expect(cumulativeOutcomeSummary(rows)).toEqual({ finished: 15, success: 10, rate: 10 / 15 });
    expect(cumulativeOutcomeSummary([])).toEqual({ finished: 0, success: 0, rate: null });
  });
});

describe("buildOverviewStats 窗口语义(A-dash 纯函数;两格随窗两格快照)", () => {
  const today = "2026-10-04";
  const doctor = fixtureDoctor(); // 3 源:2 ok + 1 degraded;findings 空
  const trendToday: TrendDay[] = [{ date: today, count: 5 }];
  const trend7: TrendDay[] = [
    { date: "2026-09-28", count: 1 },
    { date: today, count: 5 },
  ];

  /** DashboardRun 最小行(pushOk>0 时带 push 数组) */
  function dashRun(runId: number, startedAt: string, pushOk = 0): DashboardRun {
    return {
      runId,
      category: "tech",
      status: "success",
      startedAt,
      finishedAt: startedAt,
      stats:
        pushOk > 0
          ? { push: Array.from({ length: pushOk }, () => ({ channel: "tg", ok: true })) }
          : null,
      active: false,
      dry: false,
      durationMs: 0,
    };
  }

  it("今日档(默认):采集=单日 count;推送=今日 run 的 ok 计数;今日无 run = null 不虚构 0", () => {
    const stats = buildOverviewStats(doctor, [dashRun(1, "2026-10-04T08:00:00+00:00", 2)], trendToday, today);
    expect(stats.window).toBe("today");
    expect(stats.windowItems).toBe(5);
    expect(stats.windowPushOk).toBe(2);
    const noTodayRun = buildOverviewStats(doctor, [dashRun(2, "2026-10-03T08:00:00+00:00", 3)], trendToday, today);
    expect(noTodayRun.windowPushOk).toBeNull();
  });

  it("7 天档:采集=窗口求和(非右端单值);推送吃窗口内 run,窗口外(8 天前)不入", () => {
    const inWindow = [dashRun(3, "2026-10-01T08:00:00+00:00", 1), dashRun(4, "2026-10-04T09:00:00+00:00", 1)];
    const outOfWindow = dashRun(5, "2026-09-26T08:00:00+00:00", 9); // today−8 = 窗外
    const stats = buildOverviewStats(doctor, [...inWindow, outOfWindow], trend7, today, 7);
    expect(stats.windowItems).toBe(6); // 1+5
    expect(stats.windowPushOk).toBe(2); // 窗外 9 次不入
  });

  it("快照格不随窗:activeSources/totalSources/alerts 两档一致;trend=null → 采集格 null", () => {
    const todayStats = buildOverviewStats(doctor, [], trendToday, today);
    const weekStats = buildOverviewStats(doctor, [], trend7, today, 7);
    expect(weekStats.activeSources).toBe(todayStats.activeSources); // 2
    expect(weekStats.totalSources).toBe(todayStats.totalSources); // 3
    expect(weekStats.alerts).toBe(todayStats.alerts); // 0
    expect(buildOverviewStats(doctor, [], null, today, 7).windowItems).toBeNull();
  });

  it("overviewTrendDays:今日→1(1 天补零窗右端即今天),窗口档原样", () => {
    expect(overviewTrendDays("today")).toBe(1);
    expect(overviewTrendDays(7)).toBe(7);
    expect(overviewTrendDays(30)).toBe(30);
  });
});

describe("buildVerdict 状态句(D1 纯函数;10-05-dashboard-glance)", () => {
  const stats = (over: Partial<OverviewStats> = {}): OverviewStats => ({
    window: "today",
    windowItems: 128,
    activeSources: 12,
    totalSources: 14,
    windowPushOk: 3,
    alerts: 0,
    ...over,
  });
  const health = (over: Partial<SourceHealthCounts> = {}): SourceHealthCounts => ({
    ok: 12,
    degraded: 0,
    dead: 0,
    unknown: 2,
    ...over,
  });
  const category = (tone: CategoryTone): CategoryCardModel => ({
    file: "tech.yaml",
    name: "科技资讯",
    loaded: true,
    schedule: "0 9 * * *",
    nextFireAt: null,
    sourceCount: 3,
    errorCount: 0,
    warningCount: 0,
    tone,
  });
  const runs = (running = 0): RunSuccessSummary => ({
    total: 10,
    running,
    finished: 10 - running,
    success: 8,
    successRate: 0.8,
    recent: [],
  });

  it("ok 静态:「一切正常」+ 采集/源在线/推送 三段 facts", () => {
    expect(
      buildVerdict({
        overview: stats(),
        health: health(),
        categories: [category("ok")],
        runSummary: runs(),
        doctorFailed: false,
      }),
    ).toEqual({
      tone: "ok",
      headline: "一切正常",
      facts: ["今日采集 128 条", "12/14 源在线", "推送成功 3"],
    });
  });

  it("ok+运行:running>0 才拼「N 个采集中」(grill Q2:动态进 facts 不占 headline)", () => {
    const verdict = buildVerdict({
      overview: stats(),
      health: health(),
      categories: [category("ok")],
      runSummary: runs(2),
      doctorFailed: false,
    });
    expect(verdict?.headline).toBe("一切正常");
    expect(verdict?.facts).toEqual(["今日采集 128 条", "12/14 源在线", "推送成功 3", "2 个采集中"]);
  });

  it("warning:alerts/degraded 拼段、缺段省略;仅品类 dead tone 触发时兜底「N 品类异常」", () => {
    expect(
      buildVerdict({
        overview: stats({ alerts: 3 }),
        health: health({ degraded: 2 }),
        categories: [category("warning")],
        runSummary: runs(),
        doctorFailed: false,
      })?.headline,
    ).toBe("3 项告警 · 2 个源退化");
    expect(
      buildVerdict({
        overview: stats(),
        health: health({ degraded: 1 }),
        categories: [category("ok")],
        runSummary: runs(),
        doctorFailed: false,
      })?.headline,
    ).toBe("1 个源退化");
    expect(
      buildVerdict({
        overview: stats(),
        health: health(),
        categories: [category("dead"), category("dead")],
        runSummary: runs(),
        doctorFailed: false,
      })?.headline,
    ).toBe("2 品类异常");
  });

  it("dead:dead>0 最坏优先(压过告警/退化)", () => {
    expect(
      buildVerdict({
        overview: stats({ alerts: 3 }),
        health: health({ dead: 2, degraded: 1 }),
        categories: [],
        runSummary: runs(),
        doctorFailed: false,
      })?.headline,
    ).toBe("2 个源失效");
  });

  it("unknown:doctorFailed 最坏优先;health 缺 → 源在线缺数省略,首段「其余分区已降级显示」", () => {
    const verdict = buildVerdict({
      overview: stats({ activeSources: null, totalSources: null, alerts: null }),
      health: null,
      categories: [],
      runSummary: runs(),
      doctorFailed: true,
    });
    expect(verdict?.tone).toBe("unknown");
    expect(verdict?.headline).toBe("部分数据不可达,状态未知");
    expect(verdict?.facts).toEqual(["其余分区已降级显示", "今日采集 128 条", "推送成功 3"]);
  });

  it("null 分支:overview/runSummary 任一 null(整屏错误/加载态)不渲染", () => {
    expect(
      buildVerdict({ overview: null, health: null, categories: [], runSummary: null, doctorFailed: true }),
    ).toBeNull();
    expect(
      buildVerdict({ overview: null, health: health(), categories: [], runSummary: runs(), doctorFailed: false }),
    ).toBeNull();
  });

  it("facts 随概览窗(grill Q1):7 天档换「近 7 天采集」;缺数逐项省略不显 0(grill Q3)", () => {
    const windowed = buildVerdict({
      overview: stats({ window: 7, windowItems: 900 }),
      health: health(),
      categories: [category("ok")],
      runSummary: runs(),
      doctorFailed: false,
    });
    expect(windowed?.facts[0]).toBe("近 7 天采集 900 条");
    const missing = buildVerdict({
      overview: stats({ windowItems: null, activeSources: null, totalSources: null, windowPushOk: null }),
      health: health(),
      categories: [category("ok")],
      runSummary: runs(),
      doctorFailed: false,
    });
    expect(missing?.facts).toEqual([]); // 趋势不可达/无 run → 逐项省略,不虚构 0
  });

  it("零源配置:totalSources=0 省略源在线段(0/0 不是健康度事实)", () => {
    const verdict = buildVerdict({
      overview: stats({ activeSources: 0, totalSources: 0 }),
      health: health({ ok: 0, unknown: 0 }),
      categories: [],
      runSummary: runs(),
      doctorFailed: false,
    });
    expect(verdict?.facts).toEqual(["今日采集 128 条", "推送成功 3"]);
  });
});

describe("Sparkline max prop(G6 固定刻度;向后兼容回归护栏)", () => {
  it("max=1:固定 [0,1] 真刻度,0.4/0.8 不被拉成满格差", () => {
    const { container } = render(
      <Sparkline values={[0.4, 0.8]} max={1} aria-label="固定刻度" />,
    );
    // 0.4 → y=3+42*0.6=28.2;0.8 → y=3+42*0.2=11.4(距顶还有余量 = 真刻度)
    expect(container.querySelector("polyline")?.getAttribute("points")).toBe("3.0,28.2 257.0,11.4");
  });

  it("不传 max:现行为 max 归一不变(存量采集量序列零感知)", () => {
    const { container } = render(<Sparkline values={[0.4, 0.8]} aria-label="归一" />);
    // max=0.8:0.4 → y=3+42*0.5=24.0;0.8 → 贴顶 3.0
    expect(container.querySelector("polyline")?.getAttribute("points")).toBe("3.0,24.0 257.0,3.0");
  });
});
