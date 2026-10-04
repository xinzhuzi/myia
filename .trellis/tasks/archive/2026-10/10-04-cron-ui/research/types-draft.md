# types.ts 签名草案(cron-ui,逐字照抄级)

> 依据 ground-truth §1/§2(entry.py 实读)转写;入 types.ts 时按现有分段惯例(每段带与 entry.py 互指注释)。字段语义存疑处以 ground-truth 为准。

```ts
// ── cron.* 参数/结果(entry.py 4521-4790;db 公共参数全族可选,屏缺省不传) ──

export interface CronJobRecord {
  id: string;                 // 12 位 hex
  name: string;
  category: string;           // 绝对路径
  schedule: { kind: "once" | "interval" | "cron"; display: string;
              run_at?: string; minutes?: number; expr?: string };
  schedule_display: string;
  repeat: { times: number | null; completed: number };
  enabled: boolean;
  state: "scheduled" | "paused" | "completed" | "error";
  paused_at: string | null;
  paused_reason: string | null;
  manual_run_at?: string | null;
  created_at: string;
  next_run_at: string | null;
  last_run_at: string | null;
  last_status: "ok" | "failed" | "delivery_failed" | "skipped_busy" | null;
  last_error: string | null;
  last_delivery_error: string | null;
  failure_streak: number;
  deliver: string;            // "local" | "platform:ref"
  origin: { source?: string } | null;
  timezone: string | null;
  failure_deliver?: string | null;
  db_path?: string | null;
  config_path?: string | null;
  run_timeout?: number | null;
  dry_run?: boolean;
}

export interface CronCreateParams {
  schedule: string;  category: string;          // 必填
  name?: string; deliver?: string; failure_deliver?: string;
  timezone?: string; config?: string; paused_reason?: string;
  repeat?: number; run_timeout?: number; dry_run?: boolean; paused?: boolean;
}
export interface CronEditParams {                  // job + 任意部分更新
  job: string; schedule?: string; name?: string; category?: string;
  deliver?: string; failure_deliver?: string; timezone?: string;
  config?: string; repeat?: number; run_timeout?: number;
}
export interface CronRunSummary { status?: string; duration_seconds?: number;
  sources?: { ok?: number; failed?: number }; items_retained?: number;
  push?: Record<string, number>; item_failures?: number; raw?: string }

export interface CronListParams { all?: boolean }
export interface CronListResult { db: string; data_root: string; count: number; jobs: CronJobRecord[] }

export interface CronStatusResult { db: string; data_root: string;
  ticker_alive: boolean; heartbeat_age_seconds: number | null;
  last_success_age_seconds: number | null; last_error: string | null;
  estopped: boolean; jobs_total: number; jobs_enabled: number; next_due_at: string | null }

export interface CronExecutionRow { id: string; job_id: string;
  source: "tick" | "manual"; status: "claimed" | "running" | "completed" | "failed" | "unknown";
  scheduled_instant: string | null; pid: number | null; process_start_time: number | null;
  claimed_at: string | null; started_at: string | null; finished_at: string | null;
  error: string | null; run_summary: CronRunSummary | null }

export interface CronRunsParams { job?: string; limit?: number }   // limit 钳 [1,500] 后端自做
export interface CronRunsResult { db: string; count: number; executions: CronExecutionRow[] }

export interface CronPauseAllResult { estopped: boolean; marker: string }
export interface CronResumeAllResult { estopped: boolean; cleared: boolean }
export interface CronRemoveResult { removed: boolean; job_id: string; name: string }

// SidecarProtocol 增行(9):
// "cron.list"/"cron.create"/"cron.edit"/"cron.pause"/"cron.resume"/"cron.run"/"cron.remove"/"cron.status"/"cron.runs"
// pause/resume 单 job 返回 {job: CronJobRecord};all 形态见上;run 返回 {job};create/edit 返回 {job}

// ── 事件(types.ts 992-1084 分段先例;入联合 1086-1094,现 8 员 → 10) ──

export interface CronSkippedEvent { type: "cron.skipped"; job_id: string; name: string;
  reason: string; active_run_id: number | null; ts: string }
export interface CronCompletedEvent { type: "cron.completed"; job_id: string; name: string;
  ok: boolean; status: string; delivery_error: string | null;
  summary: CronRunSummary; ts: string }

// ── yaml.list 复用(选择器;entry.py 1995-2118) ──

export interface YamlFileEntry { file: string; name: string; parse_ok: boolean;
  category_id: string | null; category_name: string | null; sources: number | null;
  error: { path: string; code: string; message: string } | null }
export interface YamlListResult { plugins_dir: string; files: YamlFileEntry[] }
```

**风险注**:上表为转写草案,落地时逐键对 entry.py/myssia/cron 源复核一遍(尤其可选键的 `?:` 与 `| null` 边界——后端「显式才有」→ 全部 `?:`);发现不符以源码为准并回改本档。
