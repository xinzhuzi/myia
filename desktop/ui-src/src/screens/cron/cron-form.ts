/**
 * 定时任务表单模型(10-04-cron-ui;蓝本 = Hermes CronPage 143-175
 * emptyCronJobForm/editorFormFromJob/buildPayload 三函数族 +
 * web/src/lib/cron-job.ts,MIT —— 字段裁成我们的十件:name/schedule/category/
 * deliver/failure_deliver/repeat/timezone/config/run_timeout/dry_run,
 * 蓝本的 prompt/skills/provider/model/script 等 agent 族字段不搬 B3)。
 *
 * 数值输入(repeat/run_timeout)表单态持串:空串 = 未填(∞ / 不限时),
 * buildPayload 解析为数;后端契约 = entry.py `_m_cron_create`/`_m_cron_edit`
 * (可选参数 None = 未提供;空串非法 —— 可清空字段此处直接省键)。
 */
import type {
  CronCreateParams,
  CronEditParams,
  CronJobRecord,
  CronStatusResult,
} from "@/lib/api";

/** 表单状态(全字段字符串输入 + dry_run 开关;create/edit 双 Dialog 共用) */
export interface CronJobFormState {
  name: string;
  /** 五形态排程串:30m / every 2h / every monday 9am / 0 9 * * * / in 30m 或 ISO 时刻 */
  schedule: string;
  /** 品类 YAML 路径(选择器选 parse_ok 项或手输) */
  category: string;
  /** 投递 spec:"local" | "platform:ref" */
  deliver: string;
  failureDeliver: string;
  /** 次数串;空 = ∞(times null) */
  repeat: string;
  timezone: string;
  /** 全局 pools YAML 路径(后端存 config_path 绝对路径) */
  config: string;
  /** 正数秒串;空 = 不限时 */
  runTimeout: string;
  dryRun: boolean;
}

/** 空表单(deliver 缺省 local,同蓝本 emptyCronJobForm 的缺省值纪律) */
export function emptyCronJobForm(): CronJobFormState {
  return {
    name: "",
    schedule: "",
    category: "",
    deliver: "local",
    failureDeliver: "",
    repeat: "",
    timezone: "",
    config: "",
    runTimeout: "",
    dryRun: false,
  };
}

/** job 记录 → 排程输入串预填(kind 决定重建形态:once=run_at、
 *  interval=`{minutes}m`、cron=expr;兜底 schedule_display) */
export function jobScheduleString(job: Pick<CronJobRecord, "schedule" | "schedule_display">): string {
  const { schedule } = job;
  if (typeof schedule?.expr === "string" && schedule.expr) return schedule.expr;
  if (typeof schedule?.run_at === "string" && schedule.run_at) return schedule.run_at;
  if (typeof schedule?.minutes === "number") return `${schedule.minutes}m`;
  return job.schedule_display ?? "";
}

/** job 记录 → 预填表单(编辑 Dialog;同蓝本 editorFormFromJob)。
 *  可选键「显式才有」:缺省回落空串/false。 */
export function fromJob(job: CronJobRecord): CronJobFormState {
  return {
    name: job.name ?? "",
    schedule: jobScheduleString(job),
    category: job.category ?? "",
    deliver: job.deliver || "local",
    failureDeliver: job.failure_deliver ?? "",
    repeat: job.repeat?.times == null ? "" : String(job.repeat.times),
    timezone: job.timezone ?? "",
    config: job.config_path ?? "",
    runTimeout: job.run_timeout == null ? "" : String(job.run_timeout),
    dryRun: job.dry_run ?? false,
  };
}

/** 可选字符串参数化:trim 后空串 = 未提供(undefined;后端空串即 invalid_params,
 *  协议无「清空」语义 —— failure_deliver/timezone/config 只能改不能清) */
function optionalParam(value: string): string | undefined {
  const text = value.trim();
  return text === "" ? undefined : text;
}

/** 整数参数(repeat):空串 = 未提供;非空透传 Number —— 形状错交后端
 *  invalid_params 原文回显(「错误回显原样」纪律),前端不静默吞字段。 */
function intParam(value: string): number | undefined {
  const text = value.trim();
  return text === "" ? undefined : Number(text);
}

/**
 * 表单 → 提交载荷。
 * - 无 base:create 全量载荷(必填 schedule/category + 非空可选键);
 * - 带 base:edit 部分更新载荷(job 引用 = base.id;**仅含变更键** ——
 *   空变更集由调用方拦,后端空更新集 = cron_edit_no_changes)。
 *   dry_run 不在 edit 参数面(entry.py `_m_cron_edit` 更新键集无此键)。
 */
export function buildPayload(form: CronJobFormState): CronCreateParams;
export function buildPayload(form: CronJobFormState, base: CronJobRecord): CronEditParams;
export function buildPayload(form: CronJobFormState, base?: CronJobRecord): CronCreateParams | CronEditParams {
  const schedule = form.schedule.trim();
  const category = form.category.trim();
  const deliver = form.deliver.trim() || "local";
  const repeat = intParam(form.repeat);
  const runTimeoutRaw = form.runTimeout.trim();
  const runTimeout = runTimeoutRaw === "" ? undefined : Number(runTimeoutRaw);

  if (base === undefined) {
    return {
      schedule,
      category,
      name: optionalParam(form.name),
      deliver,
      failure_deliver: optionalParam(form.failureDeliver),
      timezone: optionalParam(form.timezone),
      config: optionalParam(form.config),
      repeat,
      run_timeout: runTimeout,
      // 后端「显式才有」:false 即不落键(entry.py create 的 dry_run 三态)
      dry_run: form.dryRun ? true : undefined,
    };
  }

  // edit:逐键 diff,仅变更项入载荷(协议部分更新;空串字段省键,见 optionalParam)
  const updates: CronEditParams = { job: base.id };
  if (form.name.trim() !== base.name) updates.name = form.name.trim();
  if (schedule !== jobScheduleString(base)) updates.schedule = schedule;
  if (category !== base.category) updates.category = category;
  if (deliver !== base.deliver) updates.deliver = deliver;
  const failureDeliver = optionalParam(form.failureDeliver);
  if (failureDeliver !== undefined && failureDeliver !== base.failure_deliver) {
    updates.failure_deliver = failureDeliver;
  }
  const timezone = optionalParam(form.timezone);
  if (timezone !== undefined && timezone !== base.timezone) updates.timezone = timezone;
  const config = optionalParam(form.config);
  if (config !== undefined && config !== base.config_path) updates.config = config;
  if (repeat !== undefined && repeat !== base.repeat?.times) updates.repeat = repeat;
  if (runTimeout !== undefined && runTimeout !== base.run_timeout) updates.run_timeout = runTimeout;
  return updates;
}

// ---------------------------------------------------------------------------
// 常量镜像(蓝本 web/src/lib/cron-job.ts 152/173 同族;双向出处注释)
// ---------------------------------------------------------------------------

/** 逾期宽限(毫秒):next_run_at 晚于 now+15min 才标「逾期」——镜像 Hermes
 *  hermes_cli/cron.py:630 `_OVERDUE_GRACE_SECONDS = 15 * 60`(tick 拥挤可晚
 *  几分钟,不算调度死);MYIA 后端无对应常量,此值是 UI 侧契约
 *  (screen-spec §2「逾期红标=now>next+15min」)。 */
export const CRON_OVERDUE_GRACE_MS = 15 * 60 * 1000;

/** 僵死黄条阈值(秒):screen-spec §1 钉死 180(判据 !ticker_alive ||
 *  heartbeat_age_seconds > 180)。对照:后端活性窗 = tick×3+20s
 *  (entry.py:4302 `_CRON_TICKER_FRESH_SECONDS`,60s tick = 200s,
 *  ticker_alive 已含该窗)——UI 取更紧的 180 提前示警;H 蓝本同族思路
 *  cron-job.ts:173 `STALE_AFTER = 60*3+20`(~3 跳 + 余量)。 */
export const CRON_STALE_HEARTBEAT_S = 180;

// ---------------------------------------------------------------------------
// 展示派生(纯函数,蓝本 cron-job.ts `cronLastResult`/`cronNextRunOverdueMs`/
// `cronSchedulerStaleAgeS` 对位;供组件与测试直接消费)
// ---------------------------------------------------------------------------

/** schedule 模板 chips(PRD F4 点名五种:每 30 分钟/每小时/每天 9 点/
 *  工作日 9 点/每周一 9 点;均 parser 实证支持:parse_duration 1h=60m、
 *  "weekdays at 9am" → cron 1-5(schedule.py `_DAYSPEC_TO_CRON_DOW`);
 *  once 形态(in 30m/ISO 时刻)不设 chip,走手输) */
export const SCHEDULE_TEMPLATES = ["30m", "every 1h", "0 9 * * *", "weekdays at 9am", "every monday 9am"] as const;

/** 上次状态 badge 色(四态映射,ground-truth §7;蓝本 STATUS_TONE 526-532
 *  的「state→tone 映射表」形态,色板用我们的四态:ok→success 族 ok /
 *  failed→destructive / delivery_failed·skipped_busy→warning / paused→中性灰)。
 *  返回值 = Badge variant 名,屏幕零逻辑直用。 */
export type CronBadgeTone = "ok" | "warning" | "destructive" | "secondary";

export interface CronStatusBadge {
  label: string;
  tone: CronBadgeTone;
}

const CRON_LAST_STATUS_BADGE: Record<
  Exclude<CronJobRecord["last_status"], null | "paused">,
  CronStatusBadge
> = {
  ok: { label: "成功", tone: "ok" },
  failed: { label: "失败", tone: "destructive" },
  delivery_failed: { label: "投递失败", tone: "warning" },
  skipped_busy: { label: "占用跳过", tone: "warning" },
};

/** job → 上次状态 badge;paused/终态由 state 抢占(screen-spec §2 上次状态列),
 *  无状态(从未跑且非暂停/终态)= null 渲染「—」 */
export function cronStatusBadge(job: Pick<CronJobRecord, "state" | "last_status">): CronStatusBadge | null {
  if (job.state === "completed") return { label: "已完结", tone: "secondary" };
  if (job.state === "paused") return { label: "已暂停", tone: "secondary" };
  if (job.last_status === null) return null;
  return CRON_LAST_STATUS_BADGE[job.last_status] ?? { label: job.last_status, tone: "secondary" };
}

/** next_run_at 逾期毫秒数(超出 15min 宽限才算;即将到时/宽限内/暂停/终态/
 *  无可解析时刻 = null)。蓝本 cron-job.ts `cronNextRunOverdueMs` 同款。 */
export function cronNextRunOverdueMs(
  job: Pick<CronJobRecord, "next_run_at" | "enabled" | "state">,
  nowMs: number = Date.now(),
): number | null {
  if (!job.enabled || job.state === "paused" || job.state === "completed") return null;
  if (job.next_run_at === null) return null;
  const at = Date.parse(job.next_run_at);
  if (Number.isNaN(at)) return null;
  const overdue = nowMs - at;
  return overdue > CRON_OVERDUE_GRACE_MS ? overdue : null;
}

/** ticker 僵死判定(screen-spec §1:!ticker_alive || heartbeat_age_seconds>180;
 *  heartbeat null 时后端必 ticker_alive=false,并入首支) */
export function cronTickerStale(
  status: Pick<CronStatusResult, "ticker_alive" | "heartbeat_age_seconds">,
): boolean {
  return !status.ticker_alive || (status.heartbeat_age_seconds ?? 0) > CRON_STALE_HEARTBEAT_S;
}

/** ISO 时刻本地化(MM-DD HH:mm);null/不可解析 = 「—」(蓝本 formatTime 对位) */
export function formatCronTime(iso: string | null): string {
  if (iso === null || iso === "") return "—";
  const date = new Date(iso);
  if (Number.isNaN(date.getTime())) return "—";
  return date.toLocaleString("zh-CN", {
    month: "2-digit",
    day: "2-digit",
    hour: "2-digit",
    minute: "2-digit",
  });
}
