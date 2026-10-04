import { useCallback, useEffect, useRef, useState } from "react";
import { ChevronDown, RefreshCw } from "lucide-react";

import { EmptyState } from "@/components/empty-state";
import { PageHeader } from "@/components/layout/page-header";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Dialog, DialogContent, DialogDescription, DialogFooter, DialogHeader, DialogTitle } from "@/components/ui/dialog";
import { Input } from "@/components/ui/input";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Skeleton } from "@/components/ui/skeleton";
import { Switch } from "@/components/ui/switch";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { api, onSidecarEvent, SidecarRequestError } from "@/lib/api";
import type { CronJobRecord, UnlistenFn } from "@/lib/api";
import { cn } from "@/lib/utils";

import { ErrorBox } from "../sources/error-box";
import { loadCronOverview, type CronOverview } from "./api";
import {
  buildPayload,
  cronNextRunOverdueMs,
  cronStatusBadge,
  cronTickerStale,
  emptyCronJobForm,
  formatCronTime,
  fromJob,
  SCHEDULE_TEMPLATES,
  type CronJobFormState,
} from "./cron-form";

interface CronLoadState {
  status: "loading" | "error" | "ready";
  data: CronOverview | null;
  error: SidecarRequestError | null;
}

/** 顶部结构化提示:动作与事件共用(messaging Notice 形态;warn = cron.skipped) */
interface Notice {
  kind: "ok" | "error" | "warn";
  text: string;
}

/** 展开体运行历史态(惰性拉取;logs 屏 expanded Set 先例) */
interface RunsState {
  status: "loading" | "ready" | "error";
  executions: Awaited<ReturnType<typeof api.cronRuns>>["executions"];
  error: SidecarRequestError | null;
}

/** 单 job 手动暂停的落库原因(可见自解释;后端 reason 可选) */
const MANUAL_PAUSE_REASON = "桌面端手动暂停";

/**
 * 定时任务屏(10-04-cron-ui):cron.* 九方法管理面,蓝本 = Hermes
 * CronPage.tsx(NousResearch/Hermes-Agent,MIT;行号地图 =
 * research/hermes-cronpage-map.md,标注 H:)。
 *
 * 布局契约 = research/screen-spec.md §1,逐块蓝本对位:
 *   A 活性条三态(H CronPage 907-921 schedulerStaleAgeS 黄条段):正常灰字
 *     含 data_root / 僵死黄条 cron-stale / 急停红条 cron-estopped + 恢复全部
 *     + 注记「仅暂停调度,单 job 操作仍可用」Q4;右侧常驻 急停全部
 *     (确认 Dialog,H 930+ DeleteConfirm 独立确认组件形态)+ 手动刷新;
 *   B notice 横幅(messaging-screen.tsx 73-76/330-342 Notice 形态,
 *     H 895-905 Toast+LoadErrorNotice 的 MYIA 对位;动作与事件共用);
 *   C 工具行(新建定时任务主按钮 + 显示暂停/终态 Switch = list all);
 *   D job 表八列契约(spec §2;H 1000-1290 job 列表+行内动作+runs 展开段):
 *     行可展开 = cron.runs limit 10 惰性拉取(logs 屏 317/423-434 expanded
 *     Set 先例)+ run_summary 摘要行(D10 快照);
 *   E 空态引导卡(CLI 对照)。
 * 创建/编辑 Dialog(H 940-1000 创建 Modal:遮罩/aria-modal/max-w-3xl 形态;
 * H 143-175 三函数 → 本目录 cron-form.ts;H 348-450 主表单字段布局)。
 * run = 排队语义(grill 二 Q1;H cron-trigger-controller 的简化:不做行级
 * spinner 死等):notice「已排队,≤60 秒内开始」+ 行「已排队」态
 * (manual_run_at 非空 ∧ 未收讫 completed),completed 事件刷新收口。
 * 事件订阅 = messaging 模式(messaging-screen.tsx 811-837 cancelled+unlisten),
 * 零轮询;本地 1min 时钟 = 全屏唯一 interval,只重渲染逾期红标(spec §4)。
 */
export function CronScreen() {
  const [state, setCronState] = useState<CronLoadState>({
    status: "loading",
    data: null,
    error: null,
  });
  const [all, setAll] = useState(false);
  const [notice, setNotice] = useState<Notice | null>(null);
  const [createOpen, setCreateOpen] = useState(false);
  const [editJob, setEditJob] = useState<CronJobRecord | null>(null);
  const [estopOpen, setEstopOpen] = useState(false);
  const [estopBusy, setEstopBusy] = useState(false);
  const [expanded, setExpanded] = useState<ReadonlySet<string>>(() => new Set());
  const [runsByJob, setRunsByJob] = useState<Record<string, RunsState>>({});
  const fetchingRunsRef = useRef<Set<string>>(new Set());
  // 已收讫 cron.completed 的 job 集合(「已排队」态的客户端收口):事件发射点
  // 在后端 mark_job_run pop manual_run_at **之前**(tick.py `_process_due_job`
  // 顺序:execute_job 内发事件 → 才 mark),事件驱动的重拉可能仍带
  // manual_run_at —— 本地先清;再次 run 时从集合移除以恢复排队态显示
  const [queueCleared, setQueueCleared] = useState<ReadonlySet<string>>(() => new Set());

  // all 的最新值给稳定回调(reload)消费,避免订阅随开关重建
  const allRef = useRef(all);
  useEffect(() => {
    allRef.current = all;
  }, [all]);

  const reload = useCallback((allOverride?: boolean) => {
    const flag = allOverride ?? allRef.current;
    setCronState((prev) => ({
      status: prev.data === null ? "loading" : "ready",
      data: prev.data,
      error: null,
    }));
    void loadCronOverview(flag).then(
      (data) => setCronState({ status: "ready", data, error: null }),
      (error: SidecarRequestError) => setCronState({ status: "error", data: null, error }),
    );
  }, []);

  useEffect(() => {
    reload();
  }, [reload]);

  // ---- 事件驱动(4.2 契约提前接线:run 排队态的收口靠 completed 事件刷新;
  //      messaging 模式订阅,无 interval 轮询) ------------------------------
  useEffect(() => {
    let unlisten: UnlistenFn | null = null;
    let cancelled = false;
    void onSidecarEvent((event) => {
      if (event.type !== "cron.completed" && event.type !== "cron.skipped") return;
      if (event.type === "cron.completed") {
        setQueueCleared((prev) =>
          prev.has(event.job_id) ? prev : new Set(prev).add(event.job_id),
        );
        setNotice(
          event.ok
            ? { kind: "ok", text: `定时任务「${event.name}」完成(status=${event.status})` }
            : {
                kind: "error",
                text: `定时任务「${event.name}」失败(status=${event.status}${
                  event.delivery_error ? ` · 投递失败:${event.delivery_error}` : ""
                })`,
              },
        );
      } else {
        setNotice({
          kind: "warn",
          text: `定时任务「${event.name}」因运行占用跳过(桌面 run #${event.active_run_id} 进行中)`,
        });
      }
      reload();
    }).then((un) => {
      if (cancelled) un();
      else unlisten = un;
    });
    return () => {
      cancelled = true;
      unlisten?.();
    };
  }, [reload]);

  // ---- 活性条与全局动作 ----------------------------------------------------

  const toggleAll = useCallback(() => {
    const next = !all;
    setAll(next);
    allRef.current = next;
    reload(next);
  }, [all, reload]);

  const engageEstop = useCallback(() => {
    setNotice(null);
    setEstopBusy(true);
    void api.cronPause({ all: true }).then(
      () => {
        setEstopBusy(false);
        setEstopOpen(false);
        setNotice({ kind: "ok", text: "已急停全部定时任务(仅暂停调度,单 job 操作仍可用)" });
        reload();
      },
      (error: SidecarRequestError) => {
        setEstopBusy(false);
        setEstopOpen(false);
        setNotice({ kind: "error", text: error.message });
      },
    );
  }, [reload]);

  const resumeAll = useCallback(() => {
    setNotice(null);
    setEstopBusy(true);
    void api.cronResume({ all: true }).then(
      (result) => {
        setEstopBusy(false);
        // all:true 形态运行时必为 CronResumeAllResult;in-收窄取 cleared
        const cleared = "cleared" in result ? result.cleared : false;
        setNotice({ kind: "ok", text: cleared ? "已恢复调度(解除急停)" : "急停本就未生效" });
        reload();
      },
      (error: SidecarRequestError) => {
        setEstopBusy(false);
        setNotice({ kind: "error", text: error.message });
      },
    );
  }, [reload]);

  // ---- 行内动作(每动作开头 setNotice(null) 覆盖式,messaging 先例) --------

  const runJob = useCallback(
    (job: CronJobRecord) => {
      setNotice(null);
      void api.cronRun({ job: job.id }).then(
        () => {
          // 重新排队:移除该 job 的 completed 收讫标记(恢复「已排队」态显示)
          setQueueCleared((prev) => {
            if (!prev.has(job.id)) return prev;
            const next = new Set(prev);
            next.delete(job.id);
            return next;
          });
          setNotice({ kind: "ok", text: `「${job.name}」已排队,≤60 秒内开始` });
          reload();
        },
        (error: SidecarRequestError) => setNotice({ kind: "error", text: error.message }),
      );
    },
    [reload],
  );

  const pauseJob = useCallback(
    (job: CronJobRecord) => {
      setNotice(null);
      void api.cronPause({ job: job.id, reason: MANUAL_PAUSE_REASON }).then(
        () => {
          setNotice({ kind: "ok", text: `已暂停「${job.name}」` });
          reload();
        },
        (error: SidecarRequestError) => setNotice({ kind: "error", text: error.message }),
      );
    },
    [reload],
  );

  const resumeJob = useCallback(
    (job: CronJobRecord) => {
      setNotice(null);
      void api.cronResume({ job: job.id }).then(
        () => {
          setNotice({ kind: "ok", text: `已恢复「${job.name}」` });
          reload();
        },
        (error: SidecarRequestError) => setNotice({ kind: "error", text: error.message }),
      );
    },
    [reload],
  );

  const removeJob = useCallback(
    (job: CronJobRecord) => {
      setNotice(null);
      if (!window.confirm(`删除定时任务「${job.name}」?任务记录将删除;运行历史与输出目录保留。`)) return;
      void api.cronRemove({ job: job.id }).then(
        (result) => {
          setNotice({ kind: "ok", text: `已删除「${result.name}」` });
          reload();
        },
        (error: SidecarRequestError) => setNotice({ kind: "error", text: error.message }),
      );
    },
    [reload],
  );

  // ---- 行内展开(logs 屏 expanded Set + 惰性拉取先例) ----------------------

  const ensureRuns = useCallback((jobId: string) => {
    if (fetchingRunsRef.current.has(jobId)) return;
    fetchingRunsRef.current.add(jobId);
    setRunsByJob((prev) =>
      prev[jobId] ? prev : { ...prev, [jobId]: { status: "loading", executions: [], error: null } },
    );
    void api.cronRuns({ job: jobId, limit: 10 }).then(
      (result) =>
        setRunsByJob((prev) => ({ ...prev, [jobId]: { status: "ready", executions: result.executions, error: null } })),
      (error: SidecarRequestError) =>
        setRunsByJob((prev) => ({ ...prev, [jobId]: { status: "error", executions: [], error } })),
    );
  }, []);

  const toggleExpand = useCallback(
    (jobId: string) => {
      if (!expanded.has(jobId)) ensureRuns(jobId);
      setExpanded((prev) => {
        const next = new Set(prev);
        if (next.has(jobId)) next.delete(jobId);
        else next.add(jobId);
        return next;
      });
    },
    [expanded, ensureRuns],
  );

  // ---- 双 Dialog 提交 ------------------------------------------------------

  const submitCreate = useCallback(
    async (form: CronJobFormState): Promise<string | null> => {
      try {
        const result = await api.cronCreate(buildPayload(form));
        setCreateOpen(false);
        setNotice({ kind: "ok", text: `已创建「${result.job.name}」` });
        reload();
        return null;
      } catch (error) {
        return error instanceof SidecarRequestError ? error.message : String(error);
      }
    },
    [reload],
  );

  const submitEdit = useCallback(
    async (job: CronJobRecord, form: CronJobFormState): Promise<string | null> => {
      try {
        await api.cronEdit(buildPayload(form, job));
        setEditJob(null);
        setNotice({ kind: "ok", text: `已保存「${job.name}」` });
        reload();
        return null;
      } catch (error) {
        // 零更新集:提示后关闭(spec §3;后端 cron_edit_no_changes 原文入提示)
        if (error instanceof SidecarRequestError && error.code === "cron_edit_no_changes") {
          setEditJob(null);
          setNotice({ kind: "ok", text: `「${job.name}」没有要更新的字段,已关闭` });
          return null;
        }
        return error instanceof SidecarRequestError ? error.message : String(error);
      }
    },
    [reload],
  );

  const status = state.data?.status ?? null;
  const estopped = status?.estopped === true;
  const stale = status === null ? false : cronTickerStale(status);

  return (
    <div>
      <PageHeader
        title="定时任务"
        description="按排程自动跑品类采集;与 CLI myssia cron 管理同一批 job"
      />
      <div className="flex flex-col gap-4 px-6 pb-6">
        {/* ---------------- A 活性条(三态)+ 急停/刷新 ---------------- */}
        <div
          data-testid={estopped ? "cron-estopped" : stale ? "cron-stale" : "cron-vitality"}
          className={cn(
            "flex flex-wrap items-center justify-between gap-x-4 gap-y-2 rounded-md border px-4 py-2.5",
            estopped
              ? "border-destructive/30 bg-destructive/10 text-destructive"
              : stale
                ? "border-warning/30 bg-warning/10 text-warning"
                : "border-border bg-card text-muted-foreground",
          )}
        >
          {estopped ? (
            <div className="flex flex-wrap items-center gap-x-3 gap-y-1 text-sm">
              <span className="font-medium">已急停:调度暂停派发</span>
              <span className="text-xs opacity-80">急停仅暂停调度,单 job 操作仍可用;在途运行不受影响</span>
              <Button
                variant="destructive"
                size="sm"
                onClick={() => void resumeAll()}
                disabled={estopBusy}
                data-testid="cron-resume-all"
              >
                恢复全部
              </Button>
            </div>
          ) : stale ? (
            <div className="flex flex-wrap items-center gap-x-3 gap-y-1 text-sm">
              <span className="font-medium">调度器心跳迟滞或已停</span>
              <span className="text-xs opacity-80">
                ticker 未存活
                {status?.heartbeat_age_seconds != null ? `(心跳 ${Math.round(status.heartbeat_age_seconds)} 秒前)` : ""}
                ——job 可能不再按时触发,可先手动「刷新」复核
              </span>
            </div>
          ) : status !== null ? (
            <p className="flex flex-wrap items-baseline gap-x-2 gap-y-0.5 text-sm">
              <span className="text-foreground">ticker 活跃</span>
              <span aria-hidden>·</span>
              <span>
                下次 <span className="text-foreground">{formatCronTime(status.next_due_at)}</span>
              </span>
              <span aria-hidden>·</span>
              <span>{status.jobs_enabled} 个 job</span>
              <span aria-hidden>·</span>
              <span className="font-mono text-2xs">{status.data_root}</span>
            </p>
          ) : (
            <span className="text-sm">活性待载入…</span>
          )}
          <div className="flex items-center gap-2">
            <Button
              variant="destructive"
              size="sm"
              onClick={() => setEstopOpen(true)}
              data-testid="cron-estop-all"
            >
              急停全部
            </Button>
            <Button variant="outline" size="sm" onClick={() => reload()} data-testid="cron-refresh">
              <RefreshCw className="size-3.5" />
              刷新
            </Button>
          </div>
        </div>

        {/* ---------------- B notice 横幅(messaging 形态) ---------------- */}
        {notice ? (
          <div
            role={notice.kind === "error" ? "alert" : "status"}
            data-testid="cron-notice"
            className={cn(
              "rounded-md border px-4 py-3 text-sm",
              notice.kind === "error"
                ? "border-destructive/30 bg-destructive/10 text-destructive"
                : notice.kind === "warn"
                  ? "border-warning/30 bg-warning/10 text-warning"
                  : "border-ok/30 bg-ok/10 text-ok",
            )}
          >
            {notice.text}
          </div>
        ) : null}

        {/* ---------------- C 工具行 ---------------- */}
        <div className="flex items-center justify-between gap-4">
          <Button size="sm" onClick={() => setCreateOpen(true)} data-testid="cron-create-open">
            新建定时任务
          </Button>
          <div className="flex items-center gap-2 text-xs text-muted-foreground">
            <Switch checked={all} onCheckedChange={toggleAll} aria-label="显示暂停/终态" data-testid="cron-all-switch" />
            <span>显示暂停/终态</span>
          </div>
        </div>

        {/* ---------------- D job 表 / E 空态 + 载/错三态 ---------------- */}
        {state.status === "loading" ? (
          <div className="flex flex-col gap-2" data-testid="cron-loading">
            <Skeleton className="h-9 w-full" />
            <Skeleton className="h-9 w-full" />
            <Skeleton className="h-9 w-2/3" />
          </div>
        ) : null}

        {state.status === "error" && state.error ? <ErrorBox error={state.error} onRetry={() => reload()} /> : null}

        {state.status === "ready" && state.data ? (
          state.data.list.count === 0 ? (
            <EmptyState
              title="创建第一个定时任务"
              description={
                <>
                  选一个品类 YAML、定好排程,采集就按点自动跑。
                  <br />
                  CLI 建的 job 也在这里:<code>myssia cron list</code>(数据根一致即同一批 job)
                </>
              }
              action={
                <Button size="sm" onClick={() => setCreateOpen(true)}>
                  新建定时任务
                </Button>
              }
            />
          ) : (
            <div className="overflow-x-auto rounded-lg border border-border">
              <JobsTable
                jobs={state.data.list.jobs}
                expanded={expanded}
                runsByJob={runsByJob}
                queueCleared={queueCleared}
                onToggleExpand={toggleExpand}
                onRun={runJob}
                onPause={pauseJob}
                onResume={resumeJob}
                onEdit={setEditJob}
                onRemove={removeJob}
              />
            </div>
          )
        ) : null}
      </div>

      {/* ---------------- 急停确认 Dialog(急停双向之「急停全部」) ---------------- */}
      <Dialog open={estopOpen} onOpenChange={setEstopOpen}>
        <DialogContent className="max-w-md">
          <DialogHeader>
            <DialogTitle>急停全部定时任务?</DialogTitle>
            <DialogDescription>
              写入全局急停标记,tick 将跳过一切派发;在途运行不受影响。
              急停仅暂停调度,单 job 操作(立即运行/暂停/编辑/删除)仍可用,可随时「恢复全部」。
            </DialogDescription>
          </DialogHeader>
          <DialogFooter>
            <Button variant="outline" size="sm" onClick={() => setEstopOpen(false)} disabled={estopBusy}>
              取消
            </Button>
            <Button
              variant="destructive"
              size="sm"
              onClick={() => void engageEstop()}
              disabled={estopBusy}
              data-testid="cron-estop-confirm"
            >
              确认急停
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>

      {/* ---------------- 创建 Dialog ---------------- */}
      <CronFormDialog
        open={createOpen}
        onOpenChange={setCreateOpen}
        mode="create"
        onSubmit={(form) => submitCreate(form)}
      />

      {/* ---------------- 编辑 Dialog(预填 + 部分更新) ---------------- */}
      {editJob !== null ? (
        <CronFormDialog
          open
          onOpenChange={(open) => {
            if (!open) setEditJob(null);
          }}
          mode="edit"
          job={editJob}
          onSubmit={(form) => submitEdit(editJob, form)}
        />
      ) : null}
    </div>
  );
}

// ---------------------------------------------------------------------------
// job 表(八列契约 screen-spec §2;colgroup 定宽 = sources-table 先例)
// ---------------------------------------------------------------------------

interface JobsTableProps {
  jobs: CronJobRecord[];
  expanded: ReadonlySet<string>;
  runsByJob: Record<string, RunsState>;
  /** 已收讫 cron.completed 的 job(「已排队」态客户端收口,见 CronScreen) */
  queueCleared: ReadonlySet<string>;
  onToggleExpand: (jobId: string) => void;
  onRun: (job: CronJobRecord) => void;
  onPause: (job: CronJobRecord) => void;
  onResume: (job: CronJobRecord) => void;
  onEdit: (job: CronJobRecord) => void;
  onRemove: (job: CronJobRecord) => void;
}

function JobsTable(props: JobsTableProps) {
  // 本地 1min 时钟(spec §4):全屏唯一 interval——只驱动逾期红标随 now
  // 重算重渲染,**不取数不触发任何 invoke**(零轮询;screen-spec #17 断言)
  const [nowMs, setNowMs] = useState(() => Date.now());
  useEffect(() => {
    const timer = window.setInterval(() => setNowMs(Date.now()), 60_000);
    return () => window.clearInterval(timer);
  }, []);
  return (
    <Table>
      <colgroup>
        <col className="w-10" />
        <col />
        <col className="w-40" />
        <col className="w-[150px]" />
        <col className="w-28" />
        <col className="w-30" />
        <col className="w-20" />
        <col className="w-50" />
      </colgroup>
      <TableHeader>
        <TableRow>
          <TableHead className="w-10">
            <span className="sr-only">展开运行历史</span>
          </TableHead>
          <TableHead>名称</TableHead>
          <TableHead>排程</TableHead>
          <TableHead>下次运行</TableHead>
          <TableHead>上次状态</TableHead>
          <TableHead>投递</TableHead>
          <TableHead>次数</TableHead>
          <TableHead className="text-right">动作</TableHead>
        </TableRow>
      </TableHeader>
      <TableBody data-testid="cron-job-rows">
        {props.jobs.map((job) => (
          <JobRow key={job.id} job={job} nowMs={nowMs} {...props} />
        ))}
      </TableBody>
    </Table>
  );
}

function JobRow({
  job,
  nowMs,
  expanded,
  runsByJob,
  queueCleared,
  onToggleExpand,
  onRun,
  onPause,
  onResume,
  onEdit,
  onRemove,
}: JobsTableProps & { job: CronJobRecord; nowMs: number }) {
  const isOpen = expanded.has(job.id);
  const overdueMs = cronNextRunOverdueMs(job, nowMs);
  const badge = cronStatusBadge(job);
  // 排队态 = trigger 已戳 manual_run_at 且未收讫 completed(收讫集合见上)
  const queued = job.manual_run_at != null && !queueCleared.has(job.id);
  const terminal = job.state === "completed";
  return (
    <>
      <TableRow>
        <TableCell>
          {/* 展开钮:独立 button,与动作钮兄弟节点不可嵌套(logs 屏先例) */}
          <button
            type="button"
            aria-expanded={isOpen}
            aria-controls={`cron-runs-${job.id}`}
            aria-label={isOpen ? `收起「${job.name}」运行历史` : `展开「${job.name}」运行历史`}
            onClick={() => onToggleExpand(job.id)}
            className="flex size-6 items-center justify-center rounded-md text-muted-foreground transition-colors duration-(--duration-fast) ease-out-expo hover:bg-accent hover:text-foreground"
          >
            <ChevronDown
              className={cn(
                "size-3.5 transition-transform duration-(--duration-fast) ease-out-expo",
                isOpen && "rotate-180",
              )}
            />
          </button>
        </TableCell>
        <TableCell>
          <span className="block max-w-[40ch] truncate font-medium text-foreground" title={job.name}>
            {job.name}
          </span>
        </TableCell>
        <TableCell>
          <span className="block truncate text-muted-foreground" title={job.schedule_display}>
            {job.schedule_display}
          </span>
        </TableCell>
        <TableCell>
          {job.state === "paused" || terminal ? (
            <span className="text-muted-foreground">—</span>
          ) : overdueMs !== null ? (
            <span className="text-destructive" title={`已逾期 ${Math.round(overdueMs / 60000)} 分钟`}>
              {formatCronTime(job.next_run_at)} · <span>逾期</span>
            </span>
          ) : (
            <span>{formatCronTime(job.next_run_at)}</span>
          )}
        </TableCell>
        <TableCell>
          {queued ? (
            <Badge variant="default" data-testid={`cron-queued-${job.id}`}>
              已排队
            </Badge>
          ) : badge ? (
            <Badge variant={badge.tone}>{badge.label}</Badge>
          ) : (
            <span className="text-muted-foreground">—</span>
          )}
        </TableCell>
        <TableCell>
          <span className="block truncate text-muted-foreground" title={job.deliver}>
            {job.deliver}
          </span>
        </TableCell>
        <TableCell className="text-muted-foreground">
          {job.repeat?.completed ?? 0}/{job.repeat?.times ?? "∞"}
        </TableCell>
        <TableCell>
          {/* estopped 下单 job 操作照常开放(grill Q4:急停只拦派发) */}
          <div className="flex justify-end gap-1">
            <Button variant="ghost" size="sm" onClick={() => onRun(job)}>
              运行
            </Button>
            {job.state === "paused" ? (
              <Button variant="ghost" size="sm" onClick={() => onResume(job)}>
                恢复
              </Button>
            ) : (
              <Button variant="ghost" size="sm" onClick={() => onPause(job)}>
                暂停
              </Button>
            )}
            <Button variant="ghost" size="sm" onClick={() => onEdit(job)}>
              编辑
            </Button>
            <Button variant="ghost" size="sm" className="text-destructive" onClick={() => onRemove(job)}>
              删除
            </Button>
          </div>
        </TableCell>
      </TableRow>
      {isOpen ? (
        <TableRow className="hover:bg-transparent">
          {/* id 与展开钮 aria-controls 成对(logs 屏 163/261 先例) */}
          <TableCell id={`cron-runs-${job.id}`} colSpan={8} className="bg-sidebar/40 px-6 py-3">
            <RunsPanel jobId={job.id} state={runsByJob[job.id]} />
          </TableCell>
        </TableRow>
      ) : null}
    </>
  );
}

/** 执行状态 → badge 变体(claimed/running=中性、completed=ok、failed=destructive、unknown=outline) */
const EXEC_BADGE: Record<string, { label: string; tone: "secondary" | "ok" | "destructive" | "outline" }> = {
  claimed: { label: "已认领", tone: "secondary" },
  running: { label: "运行中", tone: "secondary" },
  completed: { label: "已完成", tone: "ok" },
  failed: { label: "失败", tone: "destructive" },
  unknown: { label: "未知", tone: "outline" },
};

/** 展开体:cron.runs 尾查 10 条 + 摘要行(spec §1 D;摘要 = run_summary 快照) */
function RunsPanel({ jobId, state }: { jobId: string; state: RunsState | undefined }) {
  if (state === undefined || state.status === "loading") {
    return (
      <p className="text-xs text-muted-foreground" role="status">
        载入运行历史…
      </p>
    );
  }
  if (state.status === "error" && state.error) {
    return (
      <p className="text-xs text-destructive" role="alert">
        运行历史读取失败:{state.error.message}
      </p>
    );
  }
  if (state.executions.length === 0) {
    return <p className="text-xs text-muted-foreground">暂无运行历史</p>;
  }
  return (
    <ul className="flex flex-col gap-1.5" data-testid={`cron-runs-${jobId}-list`}>
      {state.executions.map((exec) => {
        const badge = EXEC_BADGE[exec.status] ?? { label: exec.status, tone: "outline" as const };
        const summary = exec.run_summary;
        return (
          <li key={exec.id} className="flex flex-col gap-0.5">
            <div className="flex flex-wrap items-baseline gap-x-3 gap-y-0.5 text-xs text-muted-foreground">
              {/* F6 时刻=finished_at(在途/异常行无终态回落 claimed_at) */}
              <span className="font-medium text-foreground">
                {formatCronTime(exec.finished_at ?? exec.claimed_at)}
              </span>
              <span>{exec.source === "manual" ? "手动" : "排程"}</span>
              <Badge variant={badge.tone}>{badge.label}</Badge>
              {/* F6 run 语义状态:退出码 3 = partial(账本行完成但管线部分失败) */}
              {summary?.run.status === "partial" ? <Badge variant="warning">部分成功</Badge> : null}
              {summary ? (
                <span>
                  源 {summary.sources.ok}/{summary.sources.total}
                  {summary.run.duration_seconds != null ? ` · ${summary.run.duration_seconds.toFixed(1)}s` : ""}
                  {` · 留存 ${summary.items_retained}`}
                  {summary.run.dry_run ? " · dry-run" : ""}
                </span>
              ) : null}
              {exec.error ? <span className="text-destructive">{exec.error}</span> : null}
            </div>
            {/* F6 失败行:summary.failures 逐行(后端已 ≤5 条/单行截 120) */}
            {(summary?.failures ?? []).map((line, index) => (
              <p key={`${exec.id}-failure-${index}`} className="pl-4 text-2xs text-destructive">
                {line}
              </p>
            ))}
            {summary && summary.failure_count > summary.failures.length ? (
              <p className="pl-4 text-2xs text-muted-foreground">
                共 {summary.failure_count} 条失败,示前 {summary.failures.length} 条
              </p>
            ) : null}
          </li>
        );
      })}
    </ul>
  );
}

// ---------------------------------------------------------------------------
// 创建/编辑 Dialog(chips 行 + 主字段 + 高级折叠;spec §3)
// ---------------------------------------------------------------------------

const MANUAL_CATEGORY_VALUE = "__manual__";

interface CronFormDialogProps {
  open: boolean;
  onOpenChange: (open: boolean) => void;
  mode: "create" | "edit";
  /** 编辑预填源(create 为 null) */
  job?: CronJobRecord | null;
  /** 提交:resolve null=成功(对话框由提交方收口);string=错误原文入表单错误行 */
  onSubmit: (form: CronJobFormState) => Promise<string | null>;
}

function CronFormDialog({ open, onOpenChange, mode, job, onSubmit }: CronFormDialogProps) {
  const [form, setForm] = useState<CronJobFormState>(emptyCronJobForm);
  const [formError, setFormError] = useState<string | null>(null);
  const [submitting, setSubmitting] = useState(false);
  const [advancedOpen, setAdvancedOpen] = useState(false);
  const [categoryMode, setCategoryMode] = useState<"select" | "manual">("select");
  const [yamlFiles, setYamlFiles] = useState<Awaited<ReturnType<typeof api.yamlList>> | null>(null);
  const [yamlError, setYamlError] = useState<string | null>(null);
  const yamlFetchedRef = useRef(false);

  const fieldId = (key: string) => `cron-${mode}-${key}`;

  // 开(或换 job)→ 重置表单;首开懒拉 yaml.list(选择器数据源)
  useEffect(() => {
    if (!open) return;
    setForm(job ? fromJob(job) : emptyCronJobForm());
    setFormError(null);
    setSubmitting(false);
    setAdvancedOpen(false);
    setCategoryMode("select");
    if (!yamlFetchedRef.current) {
      yamlFetchedRef.current = true;
      void api.yamlList().then(
        (result) => setYamlFiles(result),
        (error: SidecarRequestError) => setYamlError(error.message),
      );
    }
  }, [open, job]);

  // 预填路径不在清单内(CLI 手建/文件已删)→ 自动落手输兜底
  useEffect(() => {
    if (!open || yamlFiles === null) return;
    if (form.category !== "" && !yamlFiles.files.some((entry) => entry.file === form.category)) {
      setCategoryMode("manual");
    }
  }, [open, yamlFiles, form.category]);

  const setField = useCallback(<K extends keyof CronJobFormState>(key: K, value: CronJobFormState[K]) => {
    setForm((prev) => ({ ...prev, [key]: value }));
  }, []);

  const handleSubmit = () => {
    if (form.schedule.trim() === "") {
      setFormError("排程必填(如 every monday 9am / 0 9 * * * / in 30m)");
      return;
    }
    if (form.category.trim() === "") {
      setFormError("品类必填:从清单选择,或切「手输路径」");
      return;
    }
    setFormError(null);
    setSubmitting(true);
    void onSubmit(form).then((error) => {
      setSubmitting(false);
      if (error !== null) setFormError(error);
    });
  };

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="max-w-3xl">
        <DialogHeader>
          <DialogTitle>{mode === "create" ? "新建定时任务" : `编辑「${job?.name ?? ""}」`}</DialogTitle>
          <DialogDescription>
            排程五形态:30m / every 2h / every monday 9am / 0 9 * * * / in 30m(或 ISO 时刻)。
            {mode === "edit" ? "只提交变更字段;排程变更将重算下次运行时刻。" : ""}
          </DialogDescription>
        </DialogHeader>

        <div className="flex flex-col gap-4">
          {/* chips 行:五种模板,点击填入排程输入框 */}
          <div className="flex flex-wrap items-center gap-1.5">
            {SCHEDULE_TEMPLATES.map((template) => (
              <Button
                key={template}
                type="button"
                variant="outline"
                size="sm"
                className="font-mono text-xs"
                onClick={() => setField("schedule", template)}
                data-testid={`cron-chip-${template}`}
              >
                {template}
              </Button>
            ))}
          </div>

          {/* 主字段 */}
          <div className="grid gap-4 sm:grid-cols-2">
            <div className="flex flex-col gap-1.5">
              <label htmlFor={fieldId("schedule")} className="text-xs font-medium text-foreground">
                排程
              </label>
              <Input
                id={fieldId("schedule")}
                value={form.schedule}
                onChange={(event) => setField("schedule", event.target.value)}
                placeholder="every monday 9am"
                className="font-mono"
                data-testid="cron-form-schedule"
              />
            </div>
            <div className="flex flex-col gap-1.5">
              <label htmlFor={categoryMode === "manual" ? fieldId("category") : undefined} className="text-xs font-medium text-foreground">
                品类(品类 YAML)
              </label>
              {categoryMode === "select" ? (
                <div className="flex items-center gap-2">
                  <Select
                    value={form.category || ""}
                    onValueChange={(value) => {
                      if (value === MANUAL_CATEGORY_VALUE) {
                        setCategoryMode("manual");
                        return;
                      }
                      setField("category", value);
                    }}
                  >
                    <SelectTrigger
                      id={fieldId("category-select")}
                      className="w-full"
                      aria-label="品类 YAML 选择器"
                      data-testid="cron-form-category"
                      disabled={yamlFiles === null}
                    >
                      <SelectValue placeholder={yamlError ? "清单读取失败,请手输" : yamlFiles === null ? "载入清单…" : "选择品类 YAML"} />
                    </SelectTrigger>
                    <SelectContent>
                      {(yamlFiles?.files ?? []).map((entry) => (
                        <SelectItem
                          key={entry.file}
                          value={entry.file}
                          disabled={!entry.parse_ok}
                          title={entry.file}
                        >
                          {entry.parse_ok
                            ? `${entry.category_name ?? entry.name}`
                            : `${entry.name} · 解析失败`}
                        </SelectItem>
                      ))}
                      <SelectItem value={MANUAL_CATEGORY_VALUE}>手输路径…</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
              ) : (
                <div className="flex items-center gap-2">
                  <Input
                    id={fieldId("category")}
                    value={form.category}
                    onChange={(event) => setField("category", event.target.value)}
                    placeholder="/绝对/路径/news.yaml"
                    className="font-mono"
                    data-testid="cron-form-category-input"
                  />
                  <Button type="button" variant="ghost" size="sm" onClick={() => setCategoryMode("select")}>
                    从清单选择
                  </Button>
                </div>
              )}
            </div>
          </div>

          {/* 高级折叠(原生 button + aria-expanded/controls,frontend-ui 约定) */}
          <div className="rounded-md border border-border">
            <button
              type="button"
              aria-expanded={advancedOpen}
              aria-controls={fieldId("advanced")}
              onClick={() => setAdvancedOpen((prev) => !prev)}
              className="flex w-full items-center justify-between px-3 py-2 text-xs font-medium text-muted-foreground"
            >
              高级选项(投递 / 次数 / 时区 / config / 超时 / dry-run)
              <ChevronDown
                className={cn(
                  "size-3.5 transition-transform duration-(--duration-fast) ease-out-expo",
                  advancedOpen && "rotate-180",
                )}
              />
            </button>
            {advancedOpen ? (
              <div id={fieldId("advanced")} className="grid gap-4 border-t border-border px-3 py-3 sm:grid-cols-2">
                {(
                  [
                    { key: "deliver", label: "投递 deliver", placeholder: "local(默认)或 platform:名称" },
                    { key: "failureDeliver", label: "失败投递 failure_deliver", placeholder: "留空 = 不另投" },
                    { key: "repeat", label: "次数 repeat", placeholder: "整数;留空 = ∞" },
                    { key: "timezone", label: "时区 timezone", placeholder: "Asia/Shanghai;留空随品类/本地" },
                    { key: "config", label: "全局代理池 config", placeholder: "pools YAML 绝对路径(可选)" },
                    { key: "runTimeout", label: "超时 run_timeout(秒)", placeholder: "正数秒;留空 = 不限时" },
                  ] as const
                ).map(({ key, label, placeholder }) => (
                  <div key={key} className="flex flex-col gap-1.5">
                    <label htmlFor={fieldId(key)} className="text-xs text-muted-foreground">
                      {label}
                    </label>
                    <Input
                      id={fieldId(key)}
                      value={form[key]}
                      onChange={(event) => setField(key, event.target.value)}
                      placeholder={placeholder}
                      data-testid={`cron-form-${key}`}
                    />
                  </div>
                ))}
                <div className="flex items-center gap-2">
                  {/* 编辑态禁用:cron.edit 更新键集无 dry_run(entry.py
                      `_m_cron_edit` 4620-4637),可切不可交 = 误导 affordance */}
                  <Switch
                    id={fieldId("dry-run")}
                    checked={form.dryRun}
                    onCheckedChange={(checked) => setField("dryRun", checked)}
                    disabled={mode === "edit"}
                    title={mode === "edit" ? "dry_run 不支持编辑(协议更新键集无此字段)" : undefined}
                  />
                  <label htmlFor={fieldId("dry-run")} className="text-xs text-muted-foreground">
                    dry-run(零持久化试跑)
                    {mode === "edit" ? "(创建后不可改)" : ""}
                  </label>
                </div>
              </div>
            ) : null}
          </div>

          {formError ? (
            <p role="alert" data-testid="cron-form-error" className="text-xs text-destructive">
              {formError}
            </p>
          ) : null}
        </div>

        <DialogFooter>
          <Button variant="outline" size="sm" onClick={() => onOpenChange(false)} disabled={submitting}>
            取消
          </Button>
          <Button size="sm" onClick={handleSubmit} disabled={submitting} data-testid="cron-form-submit">
            {submitting ? "提交中…" : mode === "create" ? "创建" : "保存"}
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
}
