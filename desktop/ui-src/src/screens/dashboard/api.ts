/**
 * 仪表盘数据装配(本屏私有 api 模块;共享客户端 @/lib/api 只读不动)。
 *
 * 数据面 = sidecar 协议三方法(entry.py `_HANDLERS`):
 *   doctor     → myssia doctor --json 等价(品类/源健康度/findings);
 *   runs.list  → runs 表直读(新→旧;重启 .app 后历史仍可达,C3);
 *   run.status → 内存注册表(活跃 run 叠加;进行中 run 的实时态)。
 * 纯函数聚合出三块视图模型:品类状态卡 / 源健康度汇总 / 近期 run 成功率。
 * 结构化错误不在此吞:SidecarRequestError 原样上抛,由组件渲染 code/message。
 */
import { api } from "@/lib/api";
import type {
  DoctorPluginReport,
  DoctorResult,
  Finding,
  RunEntry,
  RunOutcomeDay,
  RunRecord,
  RunStatsPushEntry,
  SourceHealthState,
  StoreTrendResult,
  TrendDay,
} from "@/lib/api";

/** 本屏组件从 ./api 统一取类型(趋势窗视图模型的日行形状与 @/lib/api 同源) */
export type { TrendDay, RunOutcomeDay };

/**
 * 仪表盘 run 行视图模型:历史行(runs.list)+ 活跃叠加(run.status 内存态)。
 * active = 当前会话内进行中(run.status state=running);history 行里
 * status="running" 但非 active = sidecar 中断遗留的僵尸行(如实标「中断」)。
 */
export interface DashboardRun {
  runId: number;
  /** 品类 id;活跃 dry run 无表行,取 yaml 文件名 */
  category: string;
  /** runs 表 status(success/partial/failed/config_error/running/…;活跃且无表行 = null) */
  status: string | null;
  startedAt: string | null;
  finishedAt: string | null;
  stats: Record<string, unknown> | null;
  active: boolean;
  dry: boolean;
  /** 毫秒;历史行由 finishedAt-startedAt 推导,活跃行取注册表实时值 */
  durationMs: number | null;
}

/** 分区失败条目:局部降级不整屏报废(主人 2026-10-04 目验判例「报错你也不处理」)。 */
export interface DashboardSectionError {
  /** 失败的数据分区 */
  section: "doctor" | "runs" | "registry";
  error: { code: string; message: string };
}

/** 一次仪表盘刷新的原始快照(分区可缺,失败进 sectionErrors) */
export interface DashboardData {
  /** doctor 失败时为 null(品类状态/源健康度/告警格降级) */
  doctor: DoctorResult | null;
  /** 合并后的 run 行(新→旧);runs.list 失败时仅注册表活跃行,双败为空数组 */
  runs: DashboardRun[];
  /** 失败分区清单;三区全败时调用方按整屏错误处理 */
  sectionErrors: DashboardSectionError[];
}

function toSectionError(reason: unknown, section: DashboardSectionError["section"]): DashboardSectionError {
  const err =
    reason && typeof reason === "object" && "code" in reason
      ? (reason as { code: string; message?: string })
      : { code: "transport_error", message: String(reason) };
  return { section, error: { code: err.code ?? "transport_error", message: String(err.message ?? reason) } };
}

/** 历史 20 条 + 内存活跃叠加;并发拉三方法,allSettled 分区降级(单区失败不再拖垮整屏)。 */
export async function loadDashboardData(): Promise<DashboardData> {
  const [doctorR, historyR, registryR] = await Promise.allSettled([
    api.doctor(),
    api.runsList({ limit: 20 }),
    api.runStatus(),
  ]);
  const sectionErrors: DashboardSectionError[] = [];
  const doctor = doctorR.status === "fulfilled" ? doctorR.value : (sectionErrors.push(toSectionError(doctorR.reason, "doctor")), null);
  const history = historyR.status === "fulfilled" ? historyR.value : (sectionErrors.push(toSectionError(historyR.reason, "runs")), null);
  const registry = registryR.status === "fulfilled" ? registryR.value : (sectionErrors.push(toSectionError(registryR.reason, "registry")), null);
  if (history === null && registry !== null) {
    return { doctor, runs: mergeDashboardRuns([], registry.runs), sectionErrors };
  }
  if (history !== null && registry !== null) {
    return { doctor, runs: mergeDashboardRuns(history.runs, registry.runs), sectionErrors };
  }
  return { doctor, runs: [], sectionErrors };
}

/**
 * 合并 runs.list 历史行与 run.status 内存活跃条目:
 * ① 活跃 run 若已写表(pipeline start_run 即写,status="running"),给最新
 *   running 行打 active 并带上注册表实时 duration;
 * ② 活跃 run 无表行(dry run 不落库/表行写入滞后)→ 前插合成行;
 * ③ 其余 history 行原样;表内 status="running" 且无内存活跃 = 中断遗留。
 */
export function mergeDashboardRuns(history: RunRecord[], registry: RunEntry[]): DashboardRun[] {
  const actives = registry.filter((entry) => entry.state === "running");
  const rows: DashboardRun[] = history.map((record) => ({
    runId: record.run_id,
    category: record.category,
    status: record.status,
    startedAt: record.started_at,
    finishedAt: record.finished_at,
    stats: record.stats,
    active: false,
    dry: false,
    durationMs: elapsedMs(record.started_at, record.finished_at),
  }));
  for (const active of actives) {
    const tableRow = rows.find((row) => !row.active && row.status === "running");
    if (tableRow) {
      tableRow.active = true;
      tableRow.dry = active.dry;
      tableRow.durationMs = active.duration_ms ?? tableRow.durationMs;
    } else {
      rows.unshift({
        runId: active.run_id,
        category: active.yaml.split("/").pop() ?? active.yaml,
        status: null,
        startedAt: active.started_at,
        finishedAt: null,
        stats: null,
        active: true,
        dry: active.dry,
        durationMs: active.duration_ms,
      });
    }
  }
  return rows;
}

/** ISO 对差值(毫秒);任一缺失/不可解析 = null(不虚构时长)。 */
export function elapsedMs(startedAt: string | null, finishedAt: string | null): number | null {
  if (!startedAt || !finishedAt) return null;
  const start = Date.parse(startedAt);
  const end = Date.parse(finishedAt);
  if (Number.isNaN(start) || Number.isNaN(end) || end < start) return null;
  return end - start;
}

// ---------------------------------------------------------------------------
// 源健康度汇总(ok / degraded / dead / unknown 四态计数)
// ---------------------------------------------------------------------------

export type SourceHealthCounts = Record<SourceHealthState, number>;

export function emptyHealthCounts(): SourceHealthCounts {
  return { ok: 0, degraded: 0, dead: 0, unknown: 0 };
}

/** 遍历 doctor.plugins[].sources[].health.state 计数(与 health.summary 同口径) */
export function summarizeSourceHealth(doctor: DoctorResult): SourceHealthCounts {
  const counts = emptyHealthCounts();
  for (const plugin of doctor.plugins) {
    for (const source of plugin.sources) {
      counts[source.health.state] += 1;
    }
  }
  return counts;
}

// ---------------------------------------------------------------------------
// 近期 run 成功率(state=done 的 run 中 status==="success" 占比)
// ---------------------------------------------------------------------------

export interface RunSuccessSummary {
  total: number;
  running: number;
  finished: number;
  /** status==="success" 的完成 run 数(exit_code 0 语义,见 types.ts RunRecord.status) */
  success: number;
  /** success / finished;无完成 run 时 null(不虚构成 0%) */
  successRate: number | null;
  /** 最近 N 个 run(保持新→旧原序) */
  recent: DashboardRun[];
}

/** 近期列表长度(仪表盘只展示最近 10 条) */
export const RECENT_RUNS_COUNT = 10;

/**
 * 成功率聚合(吃 runs.list 合并行):active = 运行中不计入;其余全算已完结
 * (含中断遗留的 status="running" 僵尸行 —— 拖低成功率是如实的)。
 */
export function summarizeRuns(runs: DashboardRun[], recentCount = RECENT_RUNS_COUNT): RunSuccessSummary {
  const activeRuns = runs.filter((run) => run.active);
  const finishedRuns = runs.filter((run) => !run.active);
  const success = finishedRuns.filter((run) => run.status === "success").length;
  return {
    total: runs.length,
    running: activeRuns.length,
    finished: finishedRuns.length,
    success,
    successRate: finishedRuns.length > 0 ? success / finishedRuns.length : null,
    recent: runs.slice(0, recentCount),
  };
}

/** 0.8 → "80%";null → "—"(无完成 run) */
export function formatSuccessRate(rate: number | null): string {
  if (rate === null) return "—";
  return `${Math.round(rate * 100)}%`;
}

// ---------------------------------------------------------------------------
// 品类状态卡(doctor.plugins 一品类一卡;findings 按 scope 归属回品类)
// ---------------------------------------------------------------------------

export type CategoryTone = "ok" | "warning" | "dead";

export interface CategoryCardModel {
  /** 品类 YAML 文件名(doctor findings 的 scope 锚点) */
  file: string;
  name: string;
  loaded: boolean;
  schedule: string | null;
  /** 调度下次触发时间(ISO;计算失败为 null) */
  nextFireAt: string | null;
  sourceCount: number;
  errorCount: number;
  warningCount: number;
  tone: CategoryTone;
}

/**
 * 归属本品类的 findings:cli.py `_plugin_findings` 的 scope 形态为
 * `plugin:<file>` 与 `plugin:<file>/source:<name>`,前缀匹配即可。
 */
export function pluginFindings(doctor: DoctorResult, file: string): Finding[] {
  const prefix = `plugin:${file}`;
  return doctor.findings.filter(
    (finding) => finding.scope === prefix || finding.scope.startsWith(`${prefix}/`),
  );
}

export function buildCategoryCards(doctor: DoctorResult): CategoryCardModel[] {
  return doctor.plugins.map((plugin: DoctorPluginReport) => {
    const findings = pluginFindings(doctor, plugin.file);
    const errorCount = findings.filter((finding) => finding.severity === "error").length;
    const warningCount = findings.filter((finding) => finding.severity === "warning").length;
    const tone: CategoryTone =
      !plugin.loaded || errorCount > 0 ? "dead" : warningCount > 0 ? "warning" : "ok";
    return {
      file: plugin.file,
      name: plugin.name ?? plugin.file,
      loaded: plugin.loaded,
      schedule: plugin.schedule,
      nextFireAt: plugin.next_fire_at,
      sourceCount: plugin.sources.length,
      errorCount,
      warningCount,
      tone,
    };
  });
}

// ---------------------------------------------------------------------------
// 采集量趋势(B4,10-03-v112-desktop-parity:store.trend 纯函数装配)
// ---------------------------------------------------------------------------

/** 趋势窗口档位(卡头切换;服务端钳制 [1,90]) */
export const TREND_WINDOW_DAYS = [7, 14, 30] as const;
export type TrendWindowDays = (typeof TREND_WINDOW_DAYS)[number];

/** UTC「今天」的 YYYY-MM-DD(趋势窗口右端;口径 = UTC 逐日,卡面如实注记)。 */
export function utcToday(): string {
  return new Date().toISOString().slice(0, 10);
}

/** UTC 日期串加减天数(纯字符串日历运算,不经本地时区)。 */
export function shiftUtcDate(date: string, deltaDays: number): string {
  const ms = Date.parse(`${date}T00:00:00Z`);
  if (Number.isNaN(ms)) return date; // 防御:非法入参原样返回,调用侧对齐失败可见
  return new Date(ms + deltaDays * 86_400_000).toISOString().slice(0, 10);
}

/**
 * 补零对齐:把 store.trend 的稀疏逐日计数铺满「截至 today 的 days 天窗口」——
 * 缺数日补 0、窗口外行丢弃、旧→新稳定输出(空态 = 全零窗口,不是空数组:
 * sparkline 需要等长序列)。today 显式传入(纯函数可测)。
 */
export function fillDailyCounts(rows: TrendDay[], days: number, today: string): TrendDay[] {
  if (!Number.isInteger(days) || days <= 0) return [];
  const byDate = new Map<string, number>();
  for (const row of rows) {
    if (/^\d{4}-\d{2}-\d{2}$/.test(row.date)) byDate.set(row.date, row.count);
  }
  const out: TrendDay[] = [];
  for (let offset = days - 1; offset >= 0; offset -= 1) {
    const date = shiftUtcDate(today, -offset);
    out.push({ date, count: byDate.get(date) ?? 0 });
  }
  return out;
}

/** SVG polyline 坐标:等距 x + 按 max 归一 y(全零 = 居中平线,不除零)。 */
export function toSparklinePoints(
  counts: number[],
  width: number,
  height: number,
  pad = 3,
): string {
  if (counts.length === 0 || width <= pad * 2 || height <= pad * 2) return "";
  const max = Math.max(...counts, 0);
  const spanX = width - pad * 2;
  const spanY = height - pad * 2;
  return counts
    .map((count, index) => {
      const x = counts.length === 1 ? width / 2 : pad + (spanX * index) / (counts.length - 1);
      const y = max === 0 ? height / 2 : pad + spanY * (1 - count / max);
      return `${x.toFixed(1)},${y.toFixed(1)}`;
    })
    .join(" ");
}

/** 趋势行 → sparkline 数据(拉平 count;补零由 fillDailyCounts 负责)。 */
export function trendCounts(filled: TrendDay[]): number[] {
  return filled.map((day) => day.count);
}

/** store.trend 应答 → 补零窗口(独立小装配,卡组件直用)。 */
export function toTrendWindow(result: StoreTrendResult, days: number, today: string): TrendDay[] {
  return fillDailyCounts(result.days, days, today);
}

/**
 * 拉一个补零趋势窗口(统一时间窗,补批四:概览采集格与趋势卡同窗一拉,
 * 窗口右端即今天)。失败上抛,由调用侧降级 —— 趋势不可用时概览格显 —,
 * 不拖垮 doctor/runs 驱动的其余区块。
 */
export async function fetchTrendWindow(days: number): Promise<TrendDay[]> {
  const result = await api.storeTrend({ days });
  return toTrendWindow(result, days, utcToday());
}

// ---------------------------------------------------------------------------
// 成功率趋势(G6,10-04-desktop-b234:runs.trend 纯函数装配;口径 = 每日
// success/(total−running),running 不入分母,零完结日不入线不虚构 0%/100%)
// ---------------------------------------------------------------------------

/** 补零对齐(镜像 fillDailyCounts):缺数日补 total 0,旧→新稳定输出。 */
export function fillDailyOutcomes(rows: RunOutcomeDay[], days: number, today: string): RunOutcomeDay[] {
  if (!Number.isInteger(days) || days <= 0) return [];
  const byDate = new Map<string, RunOutcomeDay>();
  for (const row of rows) {
    if (/^\d{4}-\d{2}-\d{2}$/.test(row.date)) byDate.set(row.date, row);
  }
  const out: RunOutcomeDay[] = [];
  for (let offset = days - 1; offset >= 0; offset -= 1) {
    const date = shiftUtcDate(today, -offset);
    out.push(byDate.get(date) ?? { date, total: 0, statuses: {} });
  }
  return out;
}

/** 单日成功率:success/(total−running);零完结日 = null(不入线,不虚构)。 */
export function dayOutcomeRate(day: RunOutcomeDay): number | null {
  const running = day.statuses.running ?? 0;
  const finished = day.total - running;
  if (finished <= 0) return null;
  const success = day.statuses.success ?? 0;
  return success / finished;
}

/**
 * 逐日成功率序列(有完结 run 的日子才入序,旧→新;x 轴与采集量折线不对齐
 * 属如实取舍 —— 压缩画法,卡面注记说明,见任务档 design §3)。
 */
export interface OutcomeRatePoint {
  date: string;
  rate: number;
}

export function successRateSeries(filled: RunOutcomeDay[]): OutcomeRatePoint[] {
  const out: OutcomeRatePoint[] = [];
  for (const day of filled) {
    const rate = dayOutcomeRate(day);
    if (rate !== null) out.push({ date: day.date, rate });
  }
  return out;
}

/** 窗口累计(摘要行/aria 用,累计口径非均值):{finished, success, rate}。 */
export function cumulativeOutcomeSummary(filled: RunOutcomeDay[]): {
  finished: number;
  success: number;
  rate: number | null;
} {
  let finished = 0;
  let success = 0;
  for (const day of filled) {
    const running = day.statuses.running ?? 0;
    finished += day.total - running;
    success += day.statuses.success ?? 0;
  }
  return { finished, success, rate: finished > 0 ? success / finished : null };
}

/** runs.trend 应答 → 补零窗口;失败上抛由调用侧降级(allSettled 分流)。 */
export async function fetchOutcomeWindow(days: number): Promise<RunOutcomeDay[]> {
  const result = await api.runsTrend({ days });
  return fillDailyOutcomes(result.days, days, utcToday());
}

// ---------------------------------------------------------------------------
// 小格式化(本屏私有;跨屏抽取属共享层,不在本任务边界)
// ---------------------------------------------------------------------------

/** 毫秒 → "830ms" / "1.2s" / "2m3s";null/非法 → "—" */
export function formatDuration(ms: number | null): string {
  if (ms === null || !Number.isFinite(ms) || ms < 0) return "—";
  if (ms < 1000) return `${Math.round(ms)}ms`;
  const seconds = ms / 1000;
  if (seconds < 60) return `${seconds.toFixed(1)}s`;
  return `${Math.floor(seconds / 60)}m${Math.round(seconds % 60)}s`;
}

/** run 记录 stats 的条目数(pipeline.py `stats_dict` 的 items_retained) */
export function runItemCount(run: DashboardRun): number | null {
  const raw = run.stats?.["items_retained"];
  return typeof raw === "number" ? raw : null;
}

// ---------------------------------------------------------------------------
// D4 概览条(10-03-ui-deep-imitation;teardown-vercel-dashboard #2:一行四格
// = 小标签(大写+弱色)+ 大数字(tnum)):采集 / 活跃源 / 推送成功 / 告警。
// 统一时间窗(10-05 补批四,联动合一):概览头 Select(今日(UTC)/7/14/30 天)
// = 全屏唯一时间窗,驱动概览四格与采集量/成功率两折线(趋势卡自有 Select 已
// 删);今日档 = 1 天趋势窗。活跃源/告警 = doctor 点快照,无时间序列,不随窗
// (硬切 = 伪窗口),卡面注记口径。
// ---------------------------------------------------------------------------

/** 概览窗口档位:今日(UTC)单日,或近 N 天(档位与趋势卡同门;默认今日) */
export type OverviewWindow = "today" | TrendWindowDays;
export const OVERVIEW_WINDOW_DEFAULT: OverviewWindow = "today";

/** 概览窗口 → store.trend days 参数(今日 = 1 天补零窗口,右端即今天;零新协议) */
export function overviewTrendDays(window: OverviewWindow): number {
  return window === "today" ? 1 : window;
}

/** 概览条四格视图模型(全部零协议改动:既有 doctor/runs.list/store.trend 装配) */
export interface OverviewStats {
  /** 装配窗口(口径回显;今日 = UTC 单日) */
  window: OverviewWindow;
  /** 采集格:窗口内入库条目数(今日档 = 当日;窗口档 = 窗口求和);趋势不可达 = null */
  windowItems: number | null;
  /** 活跃源 = 健康度活着(ok + degraded;dead/unknown 不计);doctor 分区失败 = null(点快照,不随窗) */
  activeSources: number | null;
  /** doctor 分区失败 = null(点快照,不随窗) */
  totalSources: number | null;
  /** 推送格:窗口内(UTC)启动 run 的 stats.push[].ok=true 计数;窗口内无 run = null(不虚构 0) */
  windowPushOk: number | null;
  /** 窗口内任一 run 的 stats.push 存在失败通道(ok!==true 即计,与 windowPushOk 同源
   *  互补;verdict 升态输入,全通道失败不再报「一切正常」);窗口内无 run = null */
  windowPushFailed: boolean | null;
  /** 告警:doctor findings 的 error+warning 计数(info 级不入告警——cli 实况
   *  gate_disabled/analysis_lane_disabled/third_party_trace 等 info 明写「正常态,
   *  不是故障」且默认装机即有,计入会把正常态播报成告警;doctor 分区失败 =
   *  null(点快照,不随窗)) */
  alerts: number | null;
}

/** run 的 stats.push[] 里 ok=true 的个数(pipeline.py `stats_dict` 的 push 段) */
export function countPushOk(run: DashboardRun): number {
  const push = run.stats?.["push"];
  if (!Array.isArray(push)) return 0;
  return push.filter(
    (entry) => typeof entry === "object" && entry !== null && (entry as { ok?: unknown }).ok === true,
  ).length;
}

/** run 的 stats.push[] 是否存在失败通道(ok!==true;与 ok 字段同源口径,skipped
 *  未尝试的报告也算——是否「有失败」与「失败文案是什么」两层分离,见下) */
export function hasPushFailure(run: DashboardRun): boolean {
  const push = run.stats?.["push"];
  if (!Array.isArray(push)) return false;
  return push.some(
    (entry) => typeof entry === "object" && entry !== null && (entry as { ok?: unknown }).ok !== true,
  );
}

/**
 * run 的首个推送失败文案(stats.push[].failures[0].error,后端已按错误原文
 * 去重封顶 3 条):逐条扫描失败通道(ok!==true),首个带非空 failures[].error
 * 的条目即返回其文案;首个失败条目无 failures 键(旧 run 行 / 全 skipped
 * 未尝试)时继续找后续失败条目;无 → null(调用方不渲染徽章,不虚构)。
 */
export function runPushFailureText(run: DashboardRun): string | null {
  const push = run.stats?.["push"];
  if (!Array.isArray(push)) return null;
  for (const entry of push) {
    if (typeof entry !== "object" || entry === null) continue;
    if ((entry as { ok?: unknown }).ok === true) continue;
    const error = (entry as RunStatsPushEntry).failures?.[0]?.error;
    if (typeof error === "string" && error !== "") return error;
  }
  return null;
}

/** ISO 串的 UTC 日(YYYY-MM-DD);缺失/不可解析 = null */
export function utcDateOf(iso: string | null): string | null {
  if (!iso) return null;
  const date = iso.slice(0, 10);
  return /^\d{4}-\d{2}-\d{2}$/.test(date) ? date : null;
}

/**
 * 概览条装配:doctor(源/告警快照)+ runs(窗口内推送)+ trend 窗口(采集)。
 * trend 即趋势卡同份数据(统一时间窗,一窗一拉;补批四前概览另拉一份,已并)。
 * trend 不可达 = null → 采集格显 —,不拖垮整屏;today 显式传入(纯函数可测)。
 * 窗口内推送 = startedAt 的 UTC 日落在 [today−(N−1), today](今日档即单日);
 * runs 为 runs.list 上限 20 条的快照,窗口口径如实注记由卡面负责。
 */
export function buildOverviewStats(
  doctor: DoctorResult | null,
  runs: DashboardRun[],
  trend: TrendDay[] | null,
  today: string = utcToday(),
  window: OverviewWindow = OVERVIEW_WINDOW_DEFAULT,
): OverviewStats {
  const health = doctor !== null ? summarizeSourceHealth(doctor) : null;
  const windowStart = window === "today" ? today : shiftUtcDate(today, -(window - 1));
  const windowRuns = runs.filter((run) => {
    const date = utcDateOf(run.startedAt);
    return date !== null && date >= windowStart && date <= today;
  });
  const trendKnown = trend !== null && trend.length > 0;
  return {
    window,
    windowItems: trendKnown ? trend.reduce((sum, day) => sum + day.count, 0) : null,
    activeSources: health ? health.ok + health.degraded : null,
    totalSources: health ? health.ok + health.degraded + health.dead + health.unknown : null,
    windowPushOk: windowRuns.length > 0 ? windowRuns.reduce((sum, run) => sum + countPushOk(run), 0) : null,
    windowPushFailed: windowRuns.length > 0 ? windowRuns.some(hasPushFailure) : null,
    // 告警只计 error+warning(info 级 = cli 明示的正常态注记,默认装机即有,
    // 不入告警——与 AlertList 行口径/verdict 升态三面同源,不留「格>0 清单空」缝)
    alerts:
      doctor !== null
        ? doctor.findings.filter(
            (finding) => finding.severity === "error" || finding.severity === "warning",
          ).length
        : null,
  };
}

// ---------------------------------------------------------------------------
// D1 状态句(10-05-dashboard-glance):一句话总状态纯装配——headline 只承载
// 最坏态定性(grill Q2),facts 次段拼收获与动态(逐项可缺,缺数省略不显 0,
// grill Q3);零新拉数,全吃既有装配(overview/health/categories/runSummary)。
// ---------------------------------------------------------------------------

export type VerdictTone = "dead" | "warning" | "ok" | "unknown";

export interface DashboardVerdict {
  tone: VerdictTone;
  /** 主句:选词与着色依据 */
  headline: string;
  /** 次段短语(今日收获/动态),逐项可缺;「·」分隔由消费方拼 */
  facts: string[];
}

/**
 * 语气阶梯(最坏优先,纯函数可测):doctorFailed → unknown「数据不全」级;
 * dead>0 → dead 失效;alerts>0 / degraded>0 / 推送失败(windowPushFailed)/
 * 品类 dead tone → warning(缺段省略;推送全挂不再报「一切正常」与行内失败
 * 徽章自相矛盾);否则 ok。返回 null = 不渲染(overview 与 runSummary 同源
 * 于 data,任一 null 即数据整体不可达——整屏错误卡已负责,不双报;加载态同)。
 * facts 所有态都拼(grill Q1:采集随概览窗与四格同窗同数;running>0 才拼)。
 */
export function buildVerdict(input: {
  overview: OverviewStats | null;
  health: SourceHealthCounts | null;
  categories: CategoryCardModel[];
  runSummary: RunSuccessSummary | null;
  /** doctor 分区失败(sectionErrors 含 doctor)或整屏 error */
  doctorFailed: boolean;
}): DashboardVerdict | null {
  const { overview, health, categories, runSummary, doctorFailed } = input;
  if (overview === null || runSummary === null) return null;

  const facts: string[] = [];
  if (doctorFailed) facts.push("其余分区已降级显示");
  if (overview.windowItems !== null) {
    facts.push(
      overview.window === "today"
        ? `今日采集 ${overview.windowItems} 条`
        : `近 ${overview.window} 天采集 ${overview.windowItems} 条`,
    );
  }
  if (
    overview.activeSources !== null &&
    overview.totalSources !== null &&
    overview.totalSources > 0
  ) {
    // totalSources=0(未配置任何源)省略本段:0/0 是空配置不是健康度事实
    facts.push(`${overview.activeSources}/${overview.totalSources} 源在线`);
  }
  if (overview.windowPushOk !== null) facts.push(`推送成功 ${overview.windowPushOk}`);
  if (runSummary !== null && runSummary.running > 0) facts.push(`${runSummary.running} 个采集中`);

  if (doctorFailed) {
    return { tone: "unknown", headline: "部分数据不可达,状态未知", facts };
  }
  const dead = health?.dead ?? 0;
  if (dead > 0) {
    return { tone: "dead", headline: `${dead} 个源失效`, facts };
  }
  const alerts = overview.alerts ?? 0;
  const degraded = health?.degraded ?? 0;
  if (
    alerts > 0 ||
    degraded > 0 ||
    overview.windowPushFailed === true ||
    categories.some((category) => category.tone === "dead")
  ) {
    const segments: string[] = [];
    if (alerts > 0) segments.push(`${alerts} 项告警`);
    if (degraded > 0) segments.push(`${degraded} 个源退化`);
    if (overview.windowPushFailed === true) segments.push("推送失败");
    // 兜底段仅在 alerts/degraded/推送失败皆零而品类 dead tone 触发时出现(理论
    // 缺口:品类载入失败未产 finding;词表取品类节注三态同源,不自造)
    if (segments.length === 0) {
      segments.push(`${categories.filter((category) => category.tone === "dead").length} 品类异常`);
    }
    return { tone: "warning", headline: segments.join(" · "), facts };
  }
  return { tone: "ok", headline: "一切正常", facts };
}

// ---------------------------------------------------------------------------
// 源健康度卡网格(teardown-vercel-dashboard #3/#4:StatusDot 8px 圆点+13px
// 标签四色映射;Card = 名称 14 medium + muted 次行 + 相对时间;网格 gap-6)
// ---------------------------------------------------------------------------

/** 健康度四态展示序:坏者优先(dead → degraded → unknown → ok),同态稳定原序 */
const SOURCE_STATE_RANK: Record<SourceHealthState, number> = { dead: 0, degraded: 1, unknown: 2, ok: 3 };

export interface SourceHealthCardModel {
  /** `${pluginFile}#${sourceName}`(跨品类同名源不撞 key) */
  key: string;
  name: string;
  /** 所属品类显示名 */
  pluginName: string;
  state: SourceHealthState;
  /** 健康度评判原因(cli.py evaluate_source_health 的 reason) */
  reason: string;
  engine: string;
  /** 最近观测 run 的启动时刻(ISO;latest.run_id 在 runs.list 窗口内可查,否则 null) */
  lastObservedAt: string | null;
  /** 最近观测轮产出条数(latest.item_count;无观测 = null) */
  latestItemCount: number | null;
}

/**
 * 源健康卡模型:doctor.plugins[].sources[] 摊平 + 最近观测时间锚。
 * 时间锚如实处理:health.latest 只带 run_id 不带时刻,时刻要回 runs.list
 * 历史行查;窗口(20 条)外查不到 = null → 卡面显「—」,不虚构。
 */
export function buildSourceHealthCards(doctor: DoctorResult, runs: DashboardRun[]): SourceHealthCardModel[] {
  const startedAtByRunId = new Map(runs.map((run) => [run.runId, run.startedAt] as const));
  const cards: SourceHealthCardModel[] = [];
  for (const plugin of doctor.plugins) {
    for (const source of plugin.sources) {
      const latest = source.health.latest;
      cards.push({
        key: `${plugin.file}#${source.name}`,
        name: source.name,
        pluginName: plugin.name ?? plugin.file,
        state: source.health.state,
        reason: source.health.reason,
        engine: source.engine,
        lastObservedAt: latest ? (startedAtByRunId.get(Number(latest.run_id)) ?? null) : null,
        latestItemCount: latest && typeof latest.item_count === "number" ? latest.item_count : null,
      });
    }
  }
  return cards.sort((a, b) => SOURCE_STATE_RANK[a.state] - SOURCE_STATE_RANK[b.state]);
}

/** 相对时间:刚刚 / N 分钟前 / N 小时前 / N 天前;超 7 天或无效 = 原文/—(本屏私有,语义与 feed/api 同源) */
export function formatRelativeTime(iso: string | null, now: Date = new Date()): string {
  if (!iso) return "—";
  const then = new Date(iso);
  if (Number.isNaN(then.getTime())) return iso;
  const minutes = Math.floor((now.getTime() - then.getTime()) / 60_000);
  if (minutes < 1) return "刚刚";
  if (minutes < 60) return `${minutes} 分钟前`;
  const hours = Math.floor(minutes / 60);
  if (hours < 24) return `${hours} 小时前`;
  const days = Math.floor(hours / 24);
  if (days < 7) return `${days} 天前`;
  const pad = (value: number) => String(value).padStart(2, "0");
  return (
    `${then.getFullYear()}-${pad(then.getMonth() + 1)}-${pad(then.getDate())} ` +
    `${pad(then.getHours())}:${pad(then.getMinutes())}`
  );
}

