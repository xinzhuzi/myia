/**
 * 采集日志数据装配(本屏私有 api 模块;共享客户端 @/lib/api 只读不动)。
 *
 * 数据面 = sidecar 协议三通道:
 *   run.status    → run 列表(新→旧;状态/耗时/条目数,entry.py `_m_run_status`;
 *                   10-07-logs-restart-visibility R1 起合流 DB runs 历史——
 *                   重启后「上一程」行可达,展开走 logs.tail 惰性回填);
 *   logs.tail     → 环形缓冲历史(可按 run_id 过滤,`_m_logs_tail`);
 *   sidecar://event → log/progress/completed 流式事件(壳转发,`_pump_stream`)。
 * 流式渲染 = tail 打底 + 事件续播;错误行按 stderr 通道 + 关键词双信号高亮。
 */
import { api, onSidecarEvent } from "@/lib/api";
import type {
  LogLine,
  LogsTailResult,
  ProgressEvent,
  RunEntry,
  RunExitStatus,
  RunRecord,
  RunStartResult,
  SidecarEvent,
  UnlistenFn,
} from "@/lib/api";

// ---------------------------------------------------------------------------
// run 列表(注册表行 + 「上一程」历史行)
// ---------------------------------------------------------------------------

/**
 * 「上一程」历史行(run.status 合流 DB runs 表;entry.py `_history_run_rows`
 * 是 wire 真源):RunEntry 键全在场的超集——yaml/exit_code 无库源置 null、
 * dry 恒 false(dry run 不落库)、state 恒 done、started_at 沿库可空、
 * `history: true` 徽标、`log_run_id` = 会话注册表号(JSONL 日志行打的号,
 * 展开 `logs.tail?run_id=` 的对齐键;旧库行 null = 不可回看,如实降级)。
 *
 * 共享类型 `RunEntry` 不 widen(yaml: string 仍是注册表行契约;dashboard 域
 * 同吃该类型且并行任务在途,`active.yaml.split` 撞 null 崩编译)——历史行
 * 形状在本屏私有类型收口,dashboard/yaml-editor 侧只按 state=running 过滤
 * 消费注册表行,历史行(state=done)天然不进其路径。
 */
export interface RunHistoryEntry {
  run_id: number;
  yaml: null;
  db: string;
  dry: false;
  state: "done";
  exit_code: null;
  status: RunExitStatus | null;
  started_at: string | null;
  finished_at: string | null;
  duration_ms: number | null;
  record: RunRecord | null;
  error?: string;
  history: true;
  log_run_id: number | null;
}

/** 本屏消费的 run.status 行:会话注册表行(RunEntry)或 DB 历史行 */
export type LogsRunEntry = RunEntry | RunHistoryEntry;

/** wire 上历史行携带的增补键(共享 RunEntry 未建模;见 RunHistoryEntry 注) */
interface RunHistoryMarks {
  history?: boolean;
  log_run_id?: number | null;
}

/** 历史行判别:history === true(一次性结构收窄,后续访问走 RunHistoryEntry 面) */
export function isHistoryRun(run: LogsRunEntry): run is RunHistoryEntry {
  return (run as RunHistoryMarks).history === true;
}

/** 行唯一键:会话注册表号与 DB 自增号是两个编号空间,裸 run_id 必撞号
 *  (同屏双 #N);React key 与屏内 Set/Map 一律用此键防串 */
export function runRowKey(run: { run_id: number; history?: boolean }): string {
  return run.history === true ? `hist:${run.run_id}` : `run:${run.run_id}`;
}

export interface RunRowModel {
  runId: number;
  /** 品类名:record.category 优先,缺省取 yaml 文件名(去目录与扩展名) */
  category: string;
  status: RunExitStatus | null;
  state: RunEntry["state"];
  /** 重跑参数面(G7):run.start 需要的 yaml/dry/db 三件,原样回放该 run;
   *  历史行无库源 yaml=null → 重跑钮不渲染(无从回放) */
  yaml: string | null;
  db: string;
  dry: boolean;
  durationText: string;
  /** 「上一程」行(run.status 合流 DB runs 历史;重启后跨会话可见) */
  history: boolean;
  /** logs.tail 的 run_id:历史行 = log_run_id 会话对齐号(旧行 null=不可回看),
   *  注册表行 = 自身 run_id */
  logRunId: number | null;
  /** 退出码(注册表行 0/1/2/3 有契约语义;历史行 wire 恒 null——entry.py
   *  `_history_run_rows` 硬编码 None,0/1/2/3 只适用注册表行) */
  exitCode: number | null;
  /** error 原文整句(record.error 落库记录优先,run.error 工作线程兜底;
   *  两键皆空 = null,如实不编) */
  errorText: string | null;
  /** 行唯一键(run:N / hist:N,见 runRowKey) */
  rowKey: string;
  /** wire 原始行(run.status 应答行原样;视图派生 summarizeRun 的签名声源
   *  = LogsRunEntry,行模型随身携带免二次查表) */
  entry: LogsRunEntry;
}

/** 毫秒 → "830ms" / "1.2s" / "2m3s";null/非法 → "—"(本屏私有格式化) */
export function formatDuration(ms: number | null): string {
  if (ms === null || !Number.isFinite(ms) || ms < 0) return "—";
  if (ms < 1000) return `${Math.round(ms)}ms`;
  const seconds = ms / 1000;
  if (seconds < 60) return `${seconds.toFixed(1)}s`;
  return `${Math.floor(seconds / 60)}m${Math.round(seconds % 60)}s`;
}

export function runCategory(run: LogsRunEntry): string {
  if (run.record?.category) return run.record.category;
  if (run.yaml === null) return "未知品类"; // 历史行 yaml 无库源且 record 缺品类:如实兜底
  const file = run.yaml.split(/[\\/]/).pop() ?? run.yaml;
  return file.replace(/\.ya?ml$/i, "");
}

export function buildRunRows(runs: LogsRunEntry[]): RunRowModel[] {
  return runs.map((run) => {
    const history = isHistoryRun(run);
    return {
      runId: run.run_id,
      category: runCategory(run),
      status: run.status,
      state: run.state,
      yaml: run.yaml,
      db: run.db,
      dry: run.dry,
      durationText: formatDuration(run.duration_ms),
      history,
      logRunId: history ? (run.log_run_id ?? null) : run.run_id,
      exitCode: run.exit_code ?? null,
      errorText: run.record?.error ?? run.error ?? null,
      rowKey: runRowKey(run),
      entry: run,
    };
  });
}

export async function loadRuns(): Promise<LogsRunEntry[]> {
  // wire 上历史行(yaml=null 等)超出共享 RunEntry 契约(注册表行),本屏按
  // 合流视图消费——联合类型在此收口(见 RunHistoryEntry 注)
  return (await api.runStatus()).runs;
}

/**
 * 重跑(G7):骑 G4 手动触发通道 run.start,不新增协议方法——把该 run 的
 * yaml/dry/db 原样回放(dry run 重跑仍是 dry);成功返回新 run_id,终态与
 * 日志经既有 completed 事件 + run.status 列表刷新可见。
 * 历史行 yaml=null 无从回放,调用方不渲染重跑钮(签名收窄 yaml: string)。
 */
export function rerunRun(run: { yaml: string; dry: boolean; db: string }): Promise<RunStartResult> {
  return api.runStart({ yaml: run.yaml, dry: run.dry, db: run.db });
}

/** 重跑反馈(10-12 两级界面:重跑钮 L1 行 / L2 元信息头双可达,反馈态挂编排层):
 *  starting 打转 → triggered 报新 run_id → 8s 后自动隐去 */
export type RerunState =
  | { phase: "starting" }
  | { phase: "triggered"; runId: number }
  | { phase: "error"; message: string };

// ---------------------------------------------------------------------------
// 两级界面视图派生(10-12-logs-two-level-ui;PRD 授权「logs/api.ts 可加视图
// 派生」)。数据真源边界(PRD 不可妥协):L1 摘要 / L2 失败合成的每个字段都
// 出自 run.status 应答行(record + stats + error + exit_code),零 logs.tail
// 依赖;wire 形状一律守卫,不信任形状、不造假数据。
// ---------------------------------------------------------------------------

/** testid/DOM id 后缀:历史行加 h 前缀(原 logs-screen.tsx domIdOf 平移收口,
 *  L1 行/L2 详情共用)——会话号与 DB 号两编号空间撞号(同屏双 #N)时保
 *  DOM id/testid 唯一(行语义区分交给「上一程」徽标) */
export function domIdOf(run: Pick<RunRowModel, "runId" | "history">): string {
  return run.history ? `h${run.runId}` : `${run.runId}`;
}

/** 相对开始时间(Kestra KsDateAgo inverted 同义:列表里读「多久前」比绝对时间快;
 *  title 挂绝对时间补全语义;历史行 started_at 沿库可空 → 「—」)
 *  (原 logs-screen.tsx formatRelative 平移收口,纯函数可直测) */
export function formatRelative(iso: string | null | undefined): string {
  if (!iso) return "—";
  const ms = Date.now() - new Date(iso).getTime();
  if (!Number.isFinite(ms) || ms < 0) return "—";
  const sec = Math.floor(ms / 1000);
  if (sec < 10) return "刚刚";
  if (sec < 60) return `${sec} 秒前`;
  const min = Math.floor(sec / 60);
  if (min < 60) return `${min} 分钟前`;
  const hour = Math.floor(min / 60);
  if (hour < 24) return `${hour} 小时前`;
  return `${Math.floor(hour / 24)} 天前`;
}

/** 绝对时间(L2 元信息头「开始/结束」槽,新派生):YYYY-MM-DD HH:mm 本地时区;
 *  title 挂相对时间对偶(与 formatRelative 互补)。可空/非法 → 「—」 */
export function formatAbsolute(iso: string | null | undefined): string {
  if (!iso) return "—";
  const date = new Date(iso);
  if (Number.isNaN(date.getTime())) return "—";
  const pad = (value: number) => String(value).padStart(2, "0");
  return `${date.getFullYear()}-${pad(date.getMonth() + 1)}-${pad(date.getDate())} ${pad(date.getHours())}:${pad(date.getMinutes())}`;
}

/** 摘要段:dead = 失败语义片段(渲染 #ff6b70,组头 hover 底对比实算档,
 *  WCAG 5.5+ 不降级);muted = 常规派生段 */
export interface RunSummarySegment {
  text: string;
  tone: "muted" | "dead";
}

export interface RunSummaryModel {
  segments: RunSummarySegment[];
  /** 全空兜底文案(record 缺失或 stats 全缺;null = 有段可渲染)。
   *  如实档:running = 「采集中…」;终态 = 「无统计记录」(不造假) */
  empty: string | null;
}

/**
 * L1「采集了什么」摘要合成(design §2.2 字段派生映射,只吃 run.status 行):
 * 段序 = 成果(保留 N 条)· 源(M 源)· 失败源(失败 K 源,dead)· 错误原文
 * (dead,终态非 success 才有)。stats 是 wire 上的 Record<string, unknown>
 * (pipeline.py:586-609 stats_dict 键全集),一律 typeof/Array.isArray 守卫。
 */
export function summarizeRun(run: LogsRunEntry): RunSummaryModel {
  const segments: RunSummarySegment[] = [];
  const stats: Record<string, unknown> | null = run.record?.stats ?? null;
  // 成果段:record.stats.items_retained(pipeline.py:606 len(self.items))
  const retained = stats ? stats["items_retained"] : undefined;
  if (typeof retained === "number") {
    segments.push({ text: `保留 ${retained} 条`, tone: "muted" });
  }
  // 源段:record.stats.sources(pipeline.py:592;元素 SourceReport.to_dict
  // 带 failed/error,pipeline.py:399-412;failed 或 error 为串 = 该源失败链耗尽)
  const sources = stats ? stats["sources"] : undefined;
  if (Array.isArray(sources)) {
    segments.push({ text: `${sources.length} 源`, tone: "muted" });
    const failedCount = sources.filter(
      (source) =>
        source !== null &&
        typeof source === "object" &&
        ((source as Record<string, unknown>).failed === true ||
          typeof (source as Record<string, unknown>).error === "string"),
    ).length;
    if (failedCount > 0) segments.push({ text: `失败 ${failedCount} 源`, tone: "dead" });
  }
  if (segments.length === 0) {
    return { segments, empty: run.state === "running" ? "采集中…" : "无统计记录" };
  }
  // 错误段:终态非 success 且有 error 原文(record.error 落库记录优先,
  // run.error 工作线程兜底,历史行同键);status 未知(null)不声称失败
  if (run.state === "done" && run.status !== null && run.status !== "success") {
    const errorText = run.record?.error ?? run.error ?? null;
    if (errorText !== null && errorText !== "") segments.push({ text: errorText, tone: "dead" });
  }
  return { segments, empty: null };
}

/** exit_code → 契约语义词(cli.py:212-215 `_EXIT_BY_STATUS`:0=success /
 *  1=config_error / 2=failed / 3=partial)。只适用注册表行——历史行 wire
 *  恒 null(entry.py `_history_run_rows`),exit=— 是历史行常态真形非降级 */
const EXIT_CODE_LABEL: Record<number, string> = {
  0: "正常退出",
  1: "配置错误",
  2: "运行失败",
  3: "部分成功",
};

/** L2 失败原因区模型(design §3.2):三证据源 + 如实判空 */
export interface FailureModel {
  /** exit_code 证据:null = 无据(exit=— 不编语义) */
  exitCode: number | null;
  /** exit 契约语义词(仅注册表行 0/1/2/3 有义;null 不编) */
  exitLabel: string | null;
  /** error 字段证据整句(record.error ?? run.error;两键皆空 = null 无据) */
  errorText: string | null;
  /** stderr 错误行摘(前 5 条,等宽 dead 单行;旧行无对齐号 = 恒空) */
  errorRows: LogRow[];
  /** stderr 错误行总数(摘 5 条外的余量在日志体高亮可见) */
  errorRowsTotal: number;
  /** tail 在途(日志对齐号在场且 rows 未到位)→ 面板挂「日志拉取中」 */
  tailPending: boolean;
  /** 日志对齐号在场(= logRunId !== null):旧行 stderr 源直接判无据——
   *  ensureTail 对 null 号早退、事件流按 run_id 归组也收不到,「在途」永假 */
  logAligned: boolean;
}

/**
 * L2「为什么失败」三源合成(design §3.2):exit_code + error 字段 + stderr
 * 错误行(isRowError 双信号原样复用)。渲染门槛(PRD AC2「成功轮不显示」):
 * failed / partial / config_error / cancelled 四终态才进合成,success /
 * running / status 未知一律 null(面板一行都不渲染)。
 */
export function synthesizeFailure(run: RunRowModel, rows: LogRow[] | undefined): FailureModel | null {
  if (run.state !== "done" || run.status === null || run.status === "success") return null;
  const logAligned = run.logRunId !== null;
  const matched = logAligned && rows !== undefined ? rows.filter(isRowError) : [];
  return {
    exitCode: run.exitCode,
    exitLabel: run.exitCode !== null ? (EXIT_CODE_LABEL[run.exitCode] ?? null) : null,
    errorText: run.errorText,
    errorRows: matched.slice(0, 5),
    errorRowsTotal: matched.length,
    tailPending: logAligned && rows === undefined,
    logAligned,
  };
}

// ---------------------------------------------------------------------------
// 过滤与搜索(G7 纯函数,供组件与测试直接消费)
// ---------------------------------------------------------------------------

/** 状态过滤键:"running" 活跃态 + 五档终态(与 runBadge 同口径) */
export type RunFilterStatus = "running" | RunExitStatus;

/** run → 状态过滤键:state=running(或 status 未知)归 running,其余按终态 */
export function runFilterStatus(run: Pick<RunRowModel, "status" | "state">): RunFilterStatus {
  if (run.state === "running" || run.status === null) return "running";
  return run.status;
}

/** 品类/状态双过滤:"all" 为通配(单选项直选,不做多选) */
export function filterRunRows(
  rows: RunRowModel[],
  category: string,
  status: RunFilterStatus | "all",
): RunRowModel[] {
  return rows.filter(
    (row) =>
      (category === "all" || row.category === category) &&
      (status === "all" || runFilterStatus(row) === status),
  );
}

/** 搜索命中(大小写不敏感子串);needle 已 trim+lower,空串通配一切行 */
export function rowMatchesQuery(row: LogRow, needle: string): boolean {
  return needle === "" || row.text.toLowerCase().includes(needle);
}

/**
 * 搜索高亮切分:把 text 按 needle(已 trim+lower)切成片段序列,命中片段
 * hit=true。手写 indexOf 循环而非 RegExp——免正则元字符转义坑,任意输入安全。
 */
export function splitTextOnQuery(text: string, needle: string): Array<{ text: string; hit: boolean }> {
  if (needle === "") return [{ text, hit: false }];
  const parts: Array<{ text: string; hit: boolean }> = [];
  const haystack = text.toLowerCase();
  let cursor = 0;
  let index = haystack.indexOf(needle);
  while (index !== -1) {
    if (index > cursor) parts.push({ text: text.slice(cursor, index), hit: false });
    parts.push({ text: text.slice(index, index + needle.length), hit: true });
    cursor = index + needle.length;
    index = haystack.indexOf(needle, cursor);
  }
  if (cursor < text.length) parts.push({ text: text.slice(cursor), hit: false });
  return parts;
}

/** run_id 为 null = 不过滤(全 run 的最近日志) */
export async function loadRunLogs(runId: number | null, lines = 400): Promise<LogsTailResult> {
  return api.logsTail(runId === null ? { lines } : { lines, run_id: runId });
}

/** 订阅壳转发的 sidecar 事件流;返回取消订阅函数。 */
export function subscribeRunEvents(handler: (event: SidecarEvent) => void): Promise<UnlistenFn> {
  return onSidecarEvent(handler);
}

// ---------------------------------------------------------------------------
// 日志行视图模型:tail 历史打底 + 事件续播
// ---------------------------------------------------------------------------

export interface LogRow {
  /** 渲染 key:tail 行用 seq,事件行用自增序号(前缀区分防碰撞) */
  key: string;
  runId: number | null;
  /** system = 进度/完成事件的合成行(非子进程原行) */
  stream: "stdout" | "stderr" | "system";
  text: string;
  ts: string;
}

export function tailToRows(result: LogsTailResult): LogRow[] {
  return result.lines.map((line: LogLine) => ({
    key: `seq:${line.seq}`,
    runId: line.run_id,
    stream: line.stream,
    text: line.line,
    ts: line.ts,
  }));
}

const PROGRESS_LABEL: Record<ProgressEvent["phase"], string> = {
  run_start: "运行开始",
  source_done: "源完成",
  fetch_done: "采集步骤完成",
  run_end: "运行结束",
};

function progressText(event: ProgressEvent): string {
  const fields: string[] = [];
  if (event.category !== undefined) fields.push(`category=${event.category}`);
  if (event.source !== undefined) fields.push(`source=${event.source}`);
  if (event.engine !== undefined) fields.push(`engine=${event.engine}`);
  if (event.items !== undefined) fields.push(`items=${event.items}`);
  if (event.sources !== undefined) fields.push(`sources=${event.sources}`);
  if (event.source_failures !== undefined) fields.push(`source_failures=${event.source_failures}`);
  if (event.run_status !== undefined) fields.push(`status=${event.run_status}`);
  const joined = fields.length > 0 ? ` ${fields.join(" ")}` : "";
  return `▸ ${PROGRESS_LABEL[event.phase] ?? event.phase}${joined}`;
}

function completedText(event: SidecarEvent & { type: "completed" }): string {
  if (event.error !== undefined) {
    return `● run ${event.run_id} 异常终止:${event.error}`;
  }
  const status = event.status ?? "未知";
  const exit = event.exit_code === null ? "—" : String(event.exit_code);
  const duration = formatDuration(event.duration_ms ?? null);
  return `● run ${event.run_id} 结束 · status=${status} · exit=${exit} · 耗时 ${duration}`;
}

/** 事件 → 日志行;seq 由调用方自增(保证 key 稳定且不与 tail seq 碰撞) */
export function eventToRow(event: SidecarEvent, seq: number): LogRow {
  if (event.type === "log") {
    return { key: `event:${seq}`, runId: event.run_id, stream: event.stream, text: event.line, ts: event.ts };
  }
  if (event.type === "progress") {
    return { key: `event:${seq}`, runId: event.run_id, stream: "system", text: progressText(event), ts: event.ts };
  }
  if (event.type === "completed") {
    return { key: `event:${seq}`, runId: event.run_id, stream: "system", text: completedText(event), ts: event.ts };
  }
  if (event.type === "test.completed") {
    // 试抓 job 结果(C13,v1.1.2 桌面对齐批):一行系统摘要(run_id=null,
    // 与 sources.test 的环形缓冲 run_id=null 同口径;详情在源管理屏回显)
    const outcome = event.ok
      ? `▸ 试抓完成(job #${event.job_id})`
      : `▸ 试抓失败(job #${event.job_id}:${event.error ?? "error"})`;
    return { key: `event:${seq}`, runId: null, stream: "system", text: outcome, ts: event.ts };
  }
  if (event.type === "alerts.fired") {
    // 告警命中回放(10-04-alert-rules,协议 v7):一行系统摘要(runId=null 同
    // 试抓口径;采集日志屏订阅处按 run 域过滤不续播本事件,命中详情在消息屏
    // 告警面板 —— 本分支为穷尽守卫的类型适配,fe-gap-census R2)
    const detail = [event.title, `${event.action}:${event.action_status}`].filter(Boolean).join(" · ");
    return {
      key: `event:${seq}`,
      runId: null,
      stream: "system",
      text: `▸ 告警命中(规则「${event.rule_name}」${detail ? ` · ${detail}` : ""})`,
      ts: event.ts,
    };
  }
  if (event.type === "cron.skipped") {
    // cron fire 撞桌面 run 单飞锁跳过(10-04-hermes-cron,协议 v9):一行系统
    // 摘要(runId=null 同 alerts.fired 先例口径;采集日志屏订阅处按 run 域过滤
    // 不续播本事件,跳过详情与列表刷新在定时任务屏 —— 10-04-cron-ui 涟漪适配)
    return {
      key: `event:${seq}`,
      runId: null,
      stream: "system",
      text: `▸ 定时任务跳过(「${event.name}」· ${event.reason}:桌面 run #${event.active_run_id} 进行中)`,
      ts: event.ts,
    };
  }
  if (event.type === "cron.completed") {
    // cron fire 完成(带运行摘要,协议 v9):一行系统摘要;活性与 notice 横幅
    // 在定时任务屏(10-04-cron-ui 涟漪适配,同 alerts.fired 口径)
    const detail = event.delivery_error ? ` · 投递失败:${event.delivery_error}` : "";
    return {
      key: `event:${seq}`,
      runId: null,
      stream: "system",
      text: `▸ 定时任务完成(「${event.name}」status=${event.status}${detail})`,
      ts: event.ts,
    };
  }
  // 穷尽防御:SidecarEvent = log/progress/completed/test.completed +
  // alerts.fired + cron.skipped/cron.completed 七种(模型下载域/server ensure
  // 三事件已随看图客户端制下线,10-15-vision-model-path 协议 v16);
  // 协议再添类型时此处编译期即报错
  const unknownEvent: never = event;
  return { key: `event:${seq}`, runId: null, stream: "system", text: `▸ 未识别事件(${String(unknownEvent)})`, ts: "" };
}

// ---------------------------------------------------------------------------
// 行级着色判定:Crawlab 级别着色思路(BSD-3 可直借,licenses.md 实核)——
// 错误关键词 = 错误(dead);WARNING 级/裸 stderr = 警示;INFO/DEBUG = 正常
// ---------------------------------------------------------------------------

/** stderr 结构化日志里的进度行(phase 信号源)不算错误,白名单放行 */
const PROGRESS_INFIX = /运行开始|采集完成|采集步骤完成|运行结束/;

const ERROR_PATTERN = /\b(error|fatal|traceback|exception|panic|failed)\b|失败|错误|异常/i;

export function isRowError(row: LogRow): boolean {
  if (row.stream === "system") return false;
  if (PROGRESS_INFIX.test(row.text)) return false;
  return ERROR_PATTERN.test(row.text);
}

/** 结构化日志级别段(python logging 行「… INFO myssia.pipeline: …」同款) */
const LEVEL_WARN = /(?:^|\s)(?:WARNING|WARN)\b/;
const LEVEL_INFO = /(?:^|\s)(?:INFO|DEBUG)\b/i;

/**
 * 警示行:WARNING/WARN 级 → 警示;带 INFO/DEBUG 级标的 stderr 行是正常运行
 * 日志(本仓采集管线日志全走 stderr),不着警示色;无级标的裸 stderr(非结构
 * 化诊断直吐)保守按警示。
 */
export function isRowWarn(row: LogRow): boolean {
  if (isRowError(row)) return false;
  if (row.stream !== "stderr") return false;
  if (LEVEL_WARN.test(row.text)) return true;
  return !LEVEL_INFO.test(row.text);
}

// ---------------------------------------------------------------------------
// L2 采集成果区(10-12-run-detail-outcome):「本轮采集到了什么」的答案位
// ---------------------------------------------------------------------------

/** 成果源行(record.stats.sources[] 防御派生;pipeline.py stats_dict 真源) */
export interface OutcomeSourceRow {
  name: string;
  engine: string;
  itemCount: number;
  durationText: string | null;
  skipped: boolean;
  skipReason: string | null;
  failed: boolean;
}

/** 推送概要行(record.stats.push[];ok=null = 旧库行无此键,如实不编) */
export interface OutcomePushRow {
  channel: string;
  ok: boolean | null;
  immediate: number;
  digest: number;
  archive: number;
}

export interface OutcomeModel {
  /** items_retained(pipeline.py:607 len(items));null = 无记录 */
  retained: number | null;
  /** item_failures 条目入库失败数 */
  itemFailures: number | null;
  sources: OutcomeSourceRow[];
  pushes: OutcomePushRow[];
}

function statsNumber(value: unknown): number | null {
  return typeof value === "number" && Number.isFinite(value) ? value : null;
}

/**
 * L2 成果派生(零协议:record.stats 已随 run.status 行在 wire 上)。渲染
 * 门槛:record/stats 缺位(running 行、无记录行)→ null 一行不渲染;空壳
 * stats(键全缺)同样 null——不拿空卡片糊弄。
 */
export function deriveOutcome(run: RunRowModel): OutcomeModel | null {
  const stats = run.entry.record?.stats;
  if (stats === null || stats === undefined) return null;
  const retained = statsNumber(stats["items_retained"]);
  const itemFailures = statsNumber(stats["item_failures"]);
  const sources: OutcomeSourceRow[] = (Array.isArray(stats["sources"]) ? stats["sources"] : []).flatMap((raw) => {
    if (typeof raw !== "object" || raw === null) return [];
    const row = raw as Record<string, unknown>;
    const durationSeconds = statsNumber(row["duration_seconds"]);
    return [
      {
        name: typeof row["source"] === "string" ? row["source"] : "未知源",
        engine: typeof row["engine"] === "string" ? row["engine"] : "—",
        itemCount: statsNumber(row["item_count"]) ?? 0,
        durationText: durationSeconds === null ? null : formatDuration(durationSeconds * 1000),
        skipped: row["skipped"] === true,
        skipReason: typeof row["skip_reason"] === "string" ? row["skip_reason"] : null,
        failed: row["failed"] === true || row["error"] != null,
      },
    ];
  });
  const pushes: OutcomePushRow[] = (Array.isArray(stats["push"]) ? stats["push"] : []).flatMap((raw) => {
    if (typeof raw !== "object" || raw === null) return [];
    const row = raw as Record<string, unknown>;
    if (typeof row["channel"] !== "string") return [];
    return [
      {
        channel: row["channel"],
        ok: typeof row["ok"] === "boolean" ? row["ok"] : null,
        immediate: statsNumber(row["immediate"]) ?? 0,
        digest: statsNumber(row["digest"]) ?? 0,
        archive: statsNumber(row["archive"]) ?? 0,
      },
    ];
  });
  if (retained === null && sources.length === 0 && pushes.length === 0) return null;
  return { retained, itemFailures, sources, pushes };
}

/** 条目预览(store.items since 派生;first_seen 客户端按 finishedAt 截窗) */
export interface OutcomePreviewItem {
  key: string;
  title: string;
  firstSeen: string;
}

/** 本轮新入库条目预览:store.items?category+since=started_at(零新协议),
 *  finishedAt 截窗在视图层(同刻后继轮的条目不混入) */
export async function loadOutcomePreviews(category: string, sinceIso: string): Promise<OutcomePreviewItem[]> {
  const result = await api.storeItems({ category, since: sinceIso, limit: 50 });
  // first_seen 可空(旧 wire 行);预览窗靠它截窗,空值无窗可言如实剔除
  return result.items.flatMap((item) =>
    item.first_seen === null
      ? []
      : [{ key: item.dedup_key ?? item.url, title: item.title, firstSeen: item.first_seen }],
  );
}
