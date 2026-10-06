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
  /** record.stats.items_retained(pipeline.py `stats_dict`);无记录为 null */
  itemCount: number | null;
  /** 「上一程」行(run.status 合流 DB runs 历史;重启后跨会话可见) */
  history: boolean;
  /** logs.tail 的 run_id:历史行 = log_run_id 会话对齐号(旧行 null=不可回看),
   *  注册表行 = 自身 run_id */
  logRunId: number | null;
  /** 行唯一键(run:N / hist:N,见 runRowKey) */
  rowKey: string;
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

function itemsRetained(record: RunRecord | null): number | null {
  const raw = record?.stats?.["items_retained"];
  return typeof raw === "number" ? raw : null;
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
      itemCount: itemsRetained(run.record),
      history,
      logRunId: history ? (run.log_run_id ?? null) : run.run_id,
      rowKey: runRowKey(run),
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
  if (event.type === "image.models.progress") {
    // 模型下载进度(10-03-vision-v2):一行系统摘要(run_id=null,下载 job 不挂
    // run;后端 0.5s 节流;详情进度条在设置屏模型管理卡)
    const total = event.total_bytes === undefined ? "总量未知" : `${event.total_bytes}B`;
    return {
      key: `event:${seq}`,
      runId: null,
      stream: "system",
      text: `▸ 模型下载进度(job #${event.job_id} ${event.repo}:${event.done_bytes}B / ${total})`,
      ts: event.ts,
    };
  }
  if (event.type === "image.models.completed") {
    const outcome = event.ok
      ? `▸ 模型下载完成(job #${event.job_id})`
      : `▸ 模型下载失败(job #${event.job_id}:${event.error ?? "error"})`;
    return { key: `event:${seq}`, runId: null, stream: "system", text: outcome, ts: event.ts };
  }
  if (event.type === "image.server.completed") {
    // server ensure 终态(10-03-vision-v2 复查:ensure 慢路径应答即返,终态走
    // 本事件):一行系统摘要;徽章翻正在设置屏模型管理卡
    const outcome = event.ok
      ? `▸ 本地视觉服务已就绪(job #${event.job_id})`
      : `▸ 本地视觉服务确保启动失败(job #${event.job_id}:${event.error ?? "error"})`;
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
  // image.models.progress/completed + image.server.completed + alerts.fired +
  // cron.skipped/cron.completed 十种(10-03-vision-v2 增模型下载域/server
  // ensure 事件;10-04 fe-gap-census R2 增 alerts.fired;10-04-cron-ui 增
  // cron 域两事件);协议再添类型时此处编译期即报错
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
