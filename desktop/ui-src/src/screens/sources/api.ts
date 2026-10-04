/**
 * 源管理数据装配(本屏私有 api 模块)。
 *
 * 数据面 = sidecar 协议既有方法(entry.py `_HANDLERS`,注册表见
 * .trellis/spec/desktop/sidecar-protocol.md):
 *   health → myssia list --json 等价:插件清单 + 源健康度(ok/degraded/dead/unknown)
 *            + summary 聚合;doctor → myssia doctor --json 等价(结构化 findings)。
 *
 * 启停写回(`sources.write`,已收编进 entry.py `_HANDLERS`):本模块保留
 * 屏私有 invoke 通道(spec 变更纪律第 3 条「封装面 ≠ 协议面」:sources.write
 * 不入共享 client 门面;错误归一化与共享 client 同规则)。契约:
 *
 *   请求  {"method": "sources.write", "params": {"file", "enable"?, "disable"?}}
 *   应答  {"file", "written": true, "enabled": string[], "disabled": string[]}
 *   语义  file = health 报告里的品类 YAML 路径原样回传;disable 把源从
 *         sources: 摘出(lossless 暂存:顶层 disabled_sources: 节,文本手术
 *         注释逐字节保真);enable 移回。
 *   往返一致 = 写回后 doctor({yamls:[file]}) 报告的 sources 名单与应答
 *         enabled 完全一致(见 verifySourceRoundTrip)。
 *
 * 试抓此源(C13,10-03-v112-desktop-parity):发起走共享门面 `api.sourcesTest`
 * (本批新方法全入共享 client,spec 注册表新增行 ↔ 门面新增行同源对账);
 * 结果经 `test.completed` 事件回屏 → buildTestOutcome 结构化视图,由试抓
 * 详情弹窗展示(10-05-test-result-dialog:横幅撤除,协议零改动只消费)。
 */
import { invoke } from "@tauri-apps/api/core";

import { api, SidecarRequestError } from "@/lib/api";
import type {
  FingerprintSkips,
  HealthSummary,
  LoadErrorDetail,
  PluginReport,
  SidecarErrorShape,
  SourceHealth,
} from "@/lib/api";

// ---------------------------------------------------------------------------
// 视图模型:health 两层(插件/源)扁平成表格行
// ---------------------------------------------------------------------------

/** 表格一行 = 品类插件 × 源;health 只报 sources: 里启用的源,故 enabled 恒真 */
export interface SourceRow {
  /** 品类 YAML 路径(health PluginReport.file 原样;启停写回的目标) */
  pluginFile: string;
  pluginId: string | null;
  pluginName: string | null;
  pluginLoaded: boolean;
  /** 插件加载失败明细(loaded=false 时非空;表格里以徽标+悬浮提示呈现) */
  pluginLoadErrors: LoadErrorDetail[] | null;
  /** 品类调度周期(展示用;health PluginReport.schedule) */
  pluginSchedule: string | null;
  sourceName: string;
  url: string;
  engine: string;
  engineHint: string | null;
  health: SourceHealth;
  fingerprintSkips: FingerprintSkips;
}

export interface SourcesData {
  rows: SourceRow[];
  summary: HealthSummary;
  /** health 的 plugins_dir / db(空态文案里交代数据从哪来) */
  pluginsDir: string;
  db: string;
  /** store 打不开时的结构化明细(如实展示,不伪装成「暂无数据」) */
  storeError: { error_type: string; message: string } | null;
  /** health 的插件原序清单(排程一览按品类枚举;无源品类也在内) */
  plugins: PluginReport[];
}

/** 扁平化 PluginReport[] → SourceRow[];插件保持原序,源保持 YAML 声明序。 */
export function flattenHealthPlugins(plugins: PluginReport[]): SourceRow[] {
  const rows: SourceRow[] = [];
  for (const plugin of plugins) {
    for (const source of plugin.sources) {
      rows.push({
        pluginFile: plugin.file,
        pluginId: plugin.id,
        pluginName: plugin.name,
        pluginLoaded: plugin.loaded,
        pluginLoadErrors: plugin.load_errors,
        pluginSchedule: plugin.schedule,
        sourceName: source.name,
        url: source.url,
        engine: source.engine,
        engineHint: source.engine_hint,
        health: source.health,
        fingerprintSkips: source.fingerprint_skips,
      });
    }
  }
  return rows;
}

/** 并发语义上单方法即可;store 打不开时 health 仍返回(list 契约),原样透传。 */
export async function loadSourcesData(): Promise<SourcesData> {
  const health = await api.health();
  return {
    rows: flattenHealthPlugins(health.plugins),
    summary: health.summary,
    pluginsDir: health.plugins_dir,
    db: health.db,
    storeError: health.store_error,
    plugins: health.plugins,
  };
}

// ---------------------------------------------------------------------------
// 排程一览(G4,10-03-feed-ux):schedule.preview 逐品类并发,单品类失败不塌整区
// ---------------------------------------------------------------------------

/** 排程一览一行:品类 + schedule/timezone 原文 + 未来 5 次预览 */
export interface ScheduleRow {
  /** 品类 YAML 路径(health PluginReport.file) */
  file: string;
  /** 品类展示名(name ?? 文件名) */
  name: string;
  schedule: string | null;
  timezone: string | null;
  /** 未来运行时刻(ISO 原文;界面本地化渲染) */
  runs: string[];
  /** 单品类预览失败(结构化 code:message;不塌整区) */
  error: string | null;
}

/** 逐品类 schedule.preview(Promise.allSettled 并发;count=5 与设计一致) */
export async function loadScheduleRows(plugins: PluginReport[], count = 5): Promise<ScheduleRow[]> {
  const settled = await Promise.allSettled(
    plugins.map((plugin) => api.schedulePreview({ file: plugin.file, count })),
  );
  return plugins.map((plugin, index) => {
    const outcome = settled[index];
    if (outcome.status === "rejected") {
      const failure =
        outcome.reason instanceof SidecarRequestError
          ? `${outcome.reason.code}: ${outcome.reason.message}`
          : String(outcome.reason);
      return {
        file: plugin.file,
        name: plugin.name ?? plugin.file,
        schedule: plugin.schedule,
        timezone: plugin.timezone,
        runs: [],
        error: failure,
      };
    }
    return {
      file: plugin.file,
      name: plugin.name ?? plugin.file,
      schedule: outcome.value.schedule,
      timezone: outcome.value.timezone,
      runs: outcome.value.runs,
      error: null,
    };
  });
}

/** ISO 时刻 → 其自带偏移的墙钟「MM-DD HH:mm」短行(排程预览按品类时区计算,展示墙钟不换算本机时区,跨时区机器渲染一致) */
export function formatScheduleRun(iso: string, now: Date = new Date()): string {
  const wall = /^(\d{4})-(\d{2})-(\d{2})T(\d{2}):(\d{2})/.exec(iso);
  if (wall === null) return iso; // 非预期形态原样展示,不做本地时区换算
  const [, year, month, day, hour, minute] = wall;
  return `${Number(year) === now.getFullYear() ? "" : `${year}-`}${month}-${day} ${hour}:${minute}`;
}

// ---------------------------------------------------------------------------
// 启停写回:协议扩展提案 sources.write(契约见模块头注释)
// ---------------------------------------------------------------------------

export interface SourcesWriteParams {
  file: string;
  enable?: string[];
  disable?: string[];
}

export interface SourcesWriteResult {
  file: string;
  written: true;
  enabled: string[];
  disabled: string[];
}

/** 任意抛出物 → SidecarRequestError(与共享 client.toSidecarError 同规则;此处独立实现避免动共享层)。 */
export function asSidecarError(raw: unknown): SidecarRequestError {
  if (raw instanceof SidecarRequestError) return raw;
  if (typeof raw === "string") {
    try {
      const parsed = JSON.parse(raw) as Partial<SidecarErrorShape>;
      if (parsed && typeof parsed.code === "string" && typeof parsed.message === "string") {
        return new SidecarRequestError({
          code: parsed.code,
          path: typeof parsed.path === "string" ? parsed.path : "$",
          message: parsed.message,
          data: parsed.data,
        });
      }
    } catch {
      // 非 JSON 文本:按裸消息包装
    }
    return new SidecarRequestError({ code: "transport_error", path: "$", message: raw });
  }
  return new SidecarRequestError({
    code: "sidecar_unavailable",
    path: "$",
    message: raw instanceof Error ? `Tauri IPC 不可用: ${raw.message}` : `Tauri IPC 不可用: ${String(raw)}`,
  });
}

/**
 * 启停写回:经壳命令 sidecar_request 调 `sources.write`(已收编;屏私有
 * invoke 通道保留,spec 变更纪律第 3 条)。
 */
export async function writeSourceToggle(params: SourcesWriteParams): Promise<SourcesWriteResult> {
  try {
    return await invoke<SourcesWriteResult>("sidecar_request", {
      method: "sources.write",
      params,
    });
  } catch (raw) {
    throw asSidecarError(raw);
  }
}

// ---------------------------------------------------------------------------
// 试抓此源(C13):sources.test 异步 job;结果视图自 test.completed 事件
// (10-05-test-result-dialog:结构化明细吃满,由详情弹窗展示,不再压一行摘要)
// ---------------------------------------------------------------------------

/** 引擎退化链一条(EngineFailure.to_dict 的引擎段:engine/error_type/message) */
interface TestOutcomeFailure {
  engine: string;
  errorType: string;
  message: string;
}

/** 条目预览一条:dedup_key(或其求值错误,互斥)+ 截断字段(k → 已字符串化值) */
interface TestOutcomeItem {
  dedupKey: string | null;
  /** dedup_key 求值失败(模板缺字段等;如实呈现,不静默) */
  dedupKeyError: string | null;
  fields: Record<string, string>;
}

/**
 * 试抓结果详情弹窗的视图模型(三 kind,10-05-test-result-dialog):
 * report = 事件 ok 且报文里有本源报告(引擎/条数/指纹/退化链/条目预览);
 * event_error = 事件 ok=false(CLI error 族 + data.errors 逐条)或报告缺源;
 * launch_error = sources.test 发起被拒(test_busy 等,屏层 catch 构造)。
 */
export interface TestOutcomeView {
  sourceName: string;
  ok: boolean;
  kind: "report" | "event_error" | "launch_error";
  // kind="report" 专属
  /** 命中引擎(report.engine;链耗尽时缺位) */
  engine?: string;
  /** 配置引擎(report.engine_configured) */
  engineConfigured?: string;
  itemCount?: number;
  fingerprint?: { verdict: string; meaning: string; skipReason: string | null };
  failures?: TestOutcomeFailure[];
  items?: TestOutcomeItem[];
  /** 后端只带前 N 条预览(report.items_truncated) */
  itemsTruncated?: boolean;
  // kind="event_error"(事件 ok=false):error + data.errors[] {path, message};
  // kind="report" 且链耗尽超时时也可携带 report.error({error_type, message})
  error?: string;
  errors?: { path: string; message: string }[];
  // kind="launch_error"(sources.test invoke 被拒):code + message
  code?: string;
  message?: string;
}

type UnknownRecord = Record<string, unknown>;

function isRecord(value: unknown): value is UnknownRecord {
  return typeof value === "object" && value !== null;
}

/** data.errors[] → {path, message}(形状不符的条目跳过,不虚构) */
function parseEventErrors(data: UnknownRecord | undefined): { path: string; message: string }[] {
  if (!data || !Array.isArray(data.errors)) return [];
  const errors: { path: string; message: string }[] = [];
  for (const entry of data.errors) {
    if (!isRecord(entry) || typeof entry.message !== "string") continue;
    errors.push({
      path: typeof entry.path === "string" ? entry.path : "",
      message: entry.message,
    });
  }
  return errors;
}

/** fingerprint {skip_reason, verdict, meaning} → 视图形;缺 meaning 视为无判定 */
function parseFingerprint(raw: unknown): TestOutcomeView["fingerprint"] {
  if (!isRecord(raw) || typeof raw.meaning !== "string") return undefined;
  return {
    verdict: typeof raw.verdict === "string" ? raw.verdict : "",
    meaning: raw.meaning,
    skipReason: typeof raw.skip_reason === "string" ? raw.skip_reason : null,
  };
}

/** failures[] → {engine, errorType, message}(引擎退化链逐条) */
function parseFailures(raw: unknown): TestOutcomeFailure[] {
  if (!Array.isArray(raw)) return [];
  const failures: TestOutcomeFailure[] = [];
  for (const entry of raw) {
    if (!isRecord(entry) || typeof entry.message !== "string") continue;
    failures.push({
      engine: typeof entry.engine === "string" ? entry.engine : "?",
      errorType: typeof entry.error_type === "string" ? entry.error_type : "?",
      message: entry.message,
    });
  }
  return failures;
}

/** items[] → {dedupKey / dedupKeyError, fields}(fields 值字符串化,null → 「—」) */
function parseItems(raw: unknown): TestOutcomeItem[] {
  if (!Array.isArray(raw)) return [];
  const items: TestOutcomeItem[] = [];
  for (const entry of raw) {
    if (!isRecord(entry)) continue;
    const fields: Record<string, string> = {};
    if (isRecord(entry.fields)) {
      for (const [key, value] of Object.entries(entry.fields)) {
        fields[key] = value === null ? "—" : String(value);
      }
    }
    items.push({
      dedupKey: typeof entry.dedup_key === "string" ? entry.dedup_key : null,
      dedupKeyError: typeof entry.dedup_key_error === "string" ? entry.dedup_key_error : null,
      fields,
    });
  }
  return items;
}

/** report.error({error_type, message},如链耗尽前的整体超时)→ 一行文案 */
function parseReportError(raw: unknown): string | undefined {
  if (!isRecord(raw)) return undefined;
  const errorType = typeof raw.error_type === "string" ? raw.error_type : "";
  const message = typeof raw.message === "string" ? raw.message : "";
  if (!errorType && !message) return undefined;
  return [errorType, message].filter(Boolean).join(":");
}

/**
 * test.completed 事件 → 详情弹窗视图(10-05-test-result-dialog):吃满既有
 * 结构化报文(引擎命中/配置、条数、指纹判定、退化链逐条、条目预览 + 截断
 * 标记);失败形带 error 族与 data.errors 逐条。防御式取值与屏内旧摘要同款,
 * 报文缺本源报告 → event_error 形「报告里没有该源的结果」。
 */
export function buildTestOutcome(
  event: {
    ok: boolean;
    error?: string;
    result?: Record<string, unknown>;
    data?: Record<string, unknown>;
  },
  sourceName: string,
): TestOutcomeView {
  if (!event.ok) {
    return {
      sourceName,
      ok: false,
      kind: "event_error",
      error: event.error ?? "error",
      errors: parseEventErrors(event.data),
    };
  }
  const result = event.result ?? {};
  const reports = Array.isArray(result.sources) ? (result.sources as unknown[]) : [];
  const report = reports.find((entry) => isRecord(entry) && entry.source === sourceName);
  if (!isRecord(report)) {
    return {
      sourceName,
      ok: false,
      kind: "event_error",
      error: "报告里没有该源的结果",
      errors: [],
    };
  }
  return {
    sourceName,
    ok: report.ok !== false,
    kind: "report",
    engine: typeof report.engine === "string" ? report.engine : undefined,
    engineConfigured:
      typeof report.engine_configured === "string" ? report.engine_configured : undefined,
    itemCount: typeof report.item_count === "number" ? report.item_count : 0,
    fingerprint: parseFingerprint(report.fingerprint),
    failures: parseFailures(report.failures),
    items: parseItems(report.items),
    itemsTruncated: report.items_truncated === true,
    error: parseReportError(report.error),
  };
}

// ---------------------------------------------------------------------------
// 往返一致复核:写回后 doctor({yamls:[file]}) 对照 sources 名单
// ---------------------------------------------------------------------------

export interface RoundTripCheck {
  consistent: boolean;
  /** 写回应答承诺的启用名单 */
  expected: string[];
  /** doctor 实际报告的启用名单 */
  actual: string[];
  pluginFile: string;
  /** 不一致时的一行中文说明(供错误态展示) */
  message: string;
}

/** 名单一致 = 同一名字集合(忽略顺序;YAML 写回不承诺保序)。 */
export function sameNameSet(a: string[], b: string[]): boolean {
  if (a.length !== b.length) return false;
  const sortedA = [...a].sort();
  const sortedB = [...b].sort();
  return sortedA.every((name, index) => name === sortedB[index]);
}

/**
 * doctor 复核往返:只对本次写回的品类 YAML 做体检,取该插件源名单与写回
 * 应答的 enabled 对照。doctor 的 findings 不在此解析(全面诊断属仪表盘),
 * 名单不一致即往返失败(结构化结果,不抛错 —— 供界面直接渲染)。
 */
export async function verifySourceRoundTrip(
  file: string,
  expected: string[],
): Promise<RoundTripCheck> {
  const doctor = await api.doctor({ yamls: [file] });
  const plugin = doctor.plugins.find((candidate) => candidate.file === file);
  const actual = plugin ? plugin.sources.map((source) => source.name) : [];
  const consistent = plugin !== undefined && sameNameSet(expected, actual);
  return {
    consistent,
    expected,
    actual,
    pluginFile: file,
    message: consistent
      ? "doctor 复核与写回结果一致"
      : plugin === undefined
        ? `doctor 未报告该品类(${file});写回可能未落盘或路径不一致`
        : `源名单不一致:期望 [${expected.join(", ") || "无"}],doctor 实际 [${actual.join(", ") || "无"}]`,
  };
}
