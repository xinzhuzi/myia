import { useCallback, useEffect, useRef, useState } from "react";
import { ChevronDown, Loader2, Play, RefreshCw } from "lucide-react";

import { EmptyState } from "@/components/empty-state";
import { PageHeader } from "@/components/layout/page-header";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Dialog, DialogContent, DialogDescription, DialogFooter, DialogHeader, DialogTitle } from "@/components/ui/dialog";
import { Input } from "@/components/ui/input";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Skeleton } from "@/components/ui/skeleton";
import { Switch } from "@/components/ui/switch";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { api, onSidecarEvent, SidecarRequestError } from "@/lib/api";
import type { CompletedEvent, CronJobRecord, RunExitStatus, UnlistenFn } from "@/lib/api";
import { cn } from "@/lib/utils";

import { ErrorBox } from "../sources/error-box";
import { formatScheduleRun, loadScheduleRows } from "../sources/api";
import type { ScheduleRow } from "../sources/api";
import { loadCronOverview, type CronOverview } from "./api";
import { RunOnceResultDialog } from "./run-once-result-dialog";
import {
  buildPayload,
  cronNextRunOverdueMs,
  cronStatusBadge,
  cronTickerStale,
  emptyCronJobForm,
  formatCronTime,
  fromJob,
  SCHEDULE_TEMPLATES,
  truncateCronText,
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
 * 排程一览品类行「跑一次」屏内态(2026-10-05 随排程一览自源管理屏迁入,
 * 状态机照抄源管理/仪表盘 RunOnceState 形状):发起后等 completed 事件按
 * run_id 对账收尾。本屏无健康度面,终态不 reload(源管理屏「终态后刷新
 * 健康度」的语义不适用于 cron 主面);终态/发起失败经 RunOnceResultDialog
 * 模态呈现(10-05-run-once-result-dialog),关闭即回 idle。
 */
type RunOnceState =
  | { phase: "idle" }
  | { phase: "starting"; file: string; name: string }
  | { phase: "collecting"; file: string; name: string; runId: number }
  | { phase: "done"; name: string; runId: number; status: RunExitStatus | null; exitCode: number | null }
  | { phase: "error"; name: string; message: string };

/**
 * 定时任务屏(10-04-cron-ui):cron.* 九方法管理面,蓝本 = Hermes
 * CronPage.tsx(NousResearch/Hermes-Agent,MIT;行号地图 =
 * research/hermes-cronpage-map.md,标注 H:)。
 *
 * 布局契约 = research/screen-spec.md §1,逐块蓝本对位:
 *   A 活性条三态(H CronPage 907-921 schedulerStaleAgeS 黄条段):正常灰字
 *     含 data_root / 僵死黄条 cron-stale / 急停红条 cron-estopped + 恢复全部
 *     + 注记「仅暂停调度,单个任务操作仍可用」Q4;右侧常驻 急停全部
 *     (确认 Dialog,H 930+ DeleteConfirm 独立确认组件形态)+ 手动刷新;
 *   B notice 横幅(messaging-screen.tsx 73-76/330-342 Notice 形态,
 *     H 895-905 Toast+LoadErrorNotice 的 MYIA 对位;动作与事件共用);
 *   C 工具行(新建定时任务主按钮 + 显示暂停/终态 Switch = list all);
 *   D job 表九列契约(spec §2,Stage 6 G2a 增「上次运行」;H 1000-1290 job
 *     列表+行内动作+runs 展开段):行可展开 = cron.runs limit 10 惰性拉取
 *     (logs 屏 317/423-434 expanded Set 先例)+ run_summary 摘要行
 *     (D10 快照);Stage 6 G1/G2b 错误可见性族 = state=error destructive
 *     「已停摆」badge(H530)+ badge title=last_error(H1158-1166)+
 *     行下 last_error/last_delivery_error 条件红行(H1218-1233);
 *   E 空态引导卡(CLI 对照);
 *   F 排程一览(2026-10-05 自源管理屏底部迁入,主人质疑「排程一览是什么
 *     意思?没在定时任务里面?」——排程语义归位本屏):逐品类 YAML
 *     schedule.preview 并发取未来 5 次运行(Apify 式 Next runs 预览,防
 *     cron 写错),行尾 ▶ 跑一次(run.start 单飞,completed 事件按 run_id
 *     对账收尾);单品类预览失败只塌该行(allSettled)。注意:此处是品类
 *     YAML schedule 节的纯计算预览,与上方 job 表(cron.* 任务面)互补——
 *     无 cron job 的品类也在此见排程。
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

  // ---- 排程一览(2026-10-05 自源管理迁入)-----------------------------------
  // 数据面:health 取品类清单(含无源品类)→ 逐品类 schedule.preview 并发;
  // health 整体失败静默(区块不渲染,不塌 cron 主面——预览失败不塌整区先例)
  const [scheduleRows, setScheduleRows] = useState<ScheduleRow[] | null>(null);
  /** 排程行「跑一次」:单飞状态机 + 最近一次终态回显 */
  const [runOnce, setRunOnce] = useState<RunOnceState>({ phase: "idle" });
  const runOnceRef = useRef<RunOnceState>({ phase: "idle" });
  runOnceRef.current = runOnce;

  useEffect(() => {
    void api.health()
      .then((health) => loadScheduleRows(health.plugins))
      .then(setScheduleRows)
      .catch(() => undefined);
  }, []);

  /** 排程行「跑一次」:run.start 单飞发起(run_busy 拒并发,忙碌态由按钮禁点表达) */
  const handleRunOnce = useCallback(async (row: ScheduleRow) => {
    setRunOnce({ phase: "starting", file: row.file, name: row.name });
    try {
      const started = await api.runStart({ yaml: row.file });
      setRunOnce({ phase: "collecting", file: row.file, name: row.name, runId: started.run_id });
    } catch (error) {
      const failure = error instanceof SidecarRequestError ? error : null;
      setRunOnce({
        phase: "error",
        name: row.name,
        message: failure ? `${failure.code}:${failure.message}` : String(error),
      });
    }
  }, []);

  // all 的最新值给稳定回调(reload)消费,避免订阅随开关重建
  const allRef = useRef(all);
  useEffect(() => {
    allRef.current = all;
  }, [all]);

  // G8(Stage 6)reload generation 守卫:useRef 自增,仅最新一次请求的应答
  // 允许落地(手动刷新/事件重拉/开关切换竞态时旧响应整包丢弃)——对位
  // H625-661 jobsRequestGenerationRef 同款
  const reloadGenerationRef = useRef(0);

  const reload = useCallback((allOverride?: boolean) => {
    const flag = allOverride ?? allRef.current;
    const generation = ++reloadGenerationRef.current;
    setCronState((prev) => ({
      status: prev.data === null ? "loading" : "ready",
      data: prev.data,
      error: null,
    }));
    void loadCronOverview(flag).then(
      (data) => {
        if (reloadGenerationRef.current !== generation) return;
        setCronState({ status: "ready", data, error: null });
      },
      (error: SidecarRequestError) => {
        if (reloadGenerationRef.current !== generation) return;
        // G4(Stage 6)错误不清列表:错误入 error state(ErrorBox 示错 +
        // 重试),jobs 保留旧值 ——「错误条 + 旧表共存」对位 H629
        // jobsLoadError 只置横幅不清 jobs 的同款语义
        setCronState((prev) => ({ status: "error", data: prev.data, error }));
      },
    );
  }, []);

  useEffect(() => {
    reload();
  }, [reload]);

  // ---- 事件驱动(4.2 契约提前接线:run 排队态的收口靠 completed 事件刷新;
  //      messaging 模式订阅,无 interval 轮询。排程一览「跑一次」的 run
  //      completed 收尾也走同一条订阅——run_id 对账防串台,不新增通道) ----
  useEffect(() => {
    let unlisten: UnlistenFn | null = null;
    let cancelled = false;
    void onSidecarEvent((event) => {
      // 排程行「跑一次」收尾(随排程一览迁入):只收自己发起的 run,
      // 别的入口(日志屏/仪表盘/CLI)发起的 run 不抢收;本屏无健康度面,
      // 终态不 reload,详情弹窗呈现(run-once-result-dialog)
      if (event.type === "completed") {
        const completed = event as CompletedEvent;
        const current = runOnceRef.current;
        if (current.phase !== "collecting" || completed.run_id !== current.runId) return;
        setRunOnce({
          phase: "done",
          name: current.name,
          runId: completed.run_id,
          status: completed.status,
          exitCode: completed.exit_code,
        });
        return;
      }
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
        setNotice({ kind: "ok", text: "已急停全部定时任务(仅暂停调度,单个任务操作仍可用)" });
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
  /** 跑一次忙碌中的品类文件(null = 空闲;run 单飞,忙碌期全区品类行禁点) */
  const runActiveFile =
    runOnce.phase === "starting" || runOnce.phase === "collecting" ? runOnce.file : null;

  return (
    <div>
      <PageHeader
        title="定时任务"
        description="按排程自动跑品类采集;与 CLI myssia cron 管理同一批任务"
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
              <span className="text-xs opacity-80">急停仅暂停调度,单个任务操作仍可用;在途运行不受影响</span>
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
                调度器未存活
                {status?.heartbeat_age_seconds != null ? `(心跳 ${Math.round(status.heartbeat_age_seconds)} 秒前)` : ""}
                ——任务可能不再按时触发,可先手动「刷新」复核
              </span>
            </div>
          ) : status !== null ? (
            <p className="flex flex-wrap items-baseline gap-x-2 gap-y-0.5 text-sm">
              <span className="text-foreground">调度器运行中</span>
              <span aria-hidden>·</span>
              <span>
                下次运行 <span className="text-foreground">{formatCronTime(status.next_due_at)}</span>
              </span>
              <span aria-hidden>·</span>
              <span>
                {status.jobs_total > status.jobs_enabled
                  ? `${status.jobs_enabled}/${status.jobs_total}`
                  : status.jobs_enabled}{" "}
                个任务启用
              </span>
              <span aria-hidden>·</span>
              <span>
                数据目录 <span className="font-mono text-2xs">{status.data_root}</span>
              </span>
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
          <div className="flex items-center gap-3 text-xs text-muted-foreground">
            {/* G5(Stage 6)列表计数:当前行数(=list.count,all 开关联动;
                对位 H1092 `{jobs.length}` 计数形态) */}
            <span data-testid="cron-job-count">共 {state.data?.list.count ?? 0} 个</span>
            <div className="flex items-center gap-2">
              <Switch checked={all} onCheckedChange={toggleAll} aria-label="显示暂停/终态" data-testid="cron-all-switch" />
              <span>显示暂停/终态</span>
            </div>
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

        {/* G4(Stage 6):error 态若持有旧数据(刷新失败)则错误条与旧表共存;
            首拉失败 data=null 走纯 ErrorBox */}
        {(state.status === "ready" || (state.status === "error" && state.data !== null)) && state.data ? (
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

        {/* ---------------- F 排程一览(2026-10-05 自源管理屏迁入) ----------------
            品类「跑一次」回显:进行中横幅(人话,run_id 类行话不上活性面,
            10-05-run-once-result-dialog)+ 终态/发起失败模态详情弹窗
            (grill Q3a+b:判词同族「详情进弹窗」);区块本体 = 每品类
            schedule/timezone 原文 + 未来 5 次运行(schedule.preview 纯计算),
            行尾 ▶ 立即跑一次该品类。 */}
        {runOnce.phase === "collecting" ? (
          <div
            role="status"
            data-testid="run-once-running"
            className="flex items-center gap-2 rounded-md border border-border bg-muted/30 px-4 py-3 text-sm text-muted-foreground"
          >
            <Loader2 className="size-3.5 animate-spin" />
            跑一次 {runOnce.name} 进行中,实时输出见
            <a
              href="#/logs"
              className="font-medium text-link transition-colors duration-(--duration-fast) hover:text-foreground"
              title="到采集日志屏跟踪该次运行实时输出"
            >
              日志屏
            </a>
            …
          </div>
        ) : null}
        {runOnce.phase === "done" || runOnce.phase === "error" ? (
          <RunOnceResultDialog
            outcome={runOnce}
            onDismiss={() => setRunOnce({ phase: "idle" })}
          />
        ) : null}

        {scheduleRows !== null ? (
          <Card data-testid="schedule-overview">
            <CardHeader>
              <CardTitle>排程一览</CardTitle>
              <CardDescription>
                每品类未来 5 次运行(schedule.preview 纯计算,品类 YAML schedule
                节;无 cron job 的品类也在此见排程);改 schedule 节到「配置编辑」;
                行尾 ▶ 立即跑一次该品类。
              </CardDescription>
            </CardHeader>
            <CardContent className="flex flex-col gap-2">
              {scheduleRows.length === 0 ? (
                <p className="text-xs text-muted-foreground">
                  插件目录下没有品类 YAML;先装品类再看排程。
                </p>
              ) : (
                <ul className="flex flex-col gap-1.5">
                  {scheduleRows.map((row) => (
                    <li
                      key={row.file}
                      data-testid={`schedule-row-${row.file}`}
                      className="grid min-h-11 grid-cols-[minmax(0,1fr)_auto_auto] items-center gap-x-4 gap-y-1 border-b border-border/40 py-1.5 text-xs last:border-b-0"
                    >
                      <span className="flex min-w-0 items-center gap-2">
                        <span className="truncate font-medium text-foreground">{row.name}</span>
                        {row.error ? (
                          <Badge variant="destructive" title={row.error}>
                            预览失败
                          </Badge>
                        ) : row.schedule ? (
                          <Badge variant="outline" className="font-mono" title="5 段 cron 原文">
                            {row.schedule}
                          </Badge>
                        ) : (
                          <Badge variant="unknown">无排程</Badge>
                        )}
                        {row.timezone ? (
                          <span className="font-mono text-2xs text-muted-foreground">{row.timezone}</span>
                        ) : null}
                      </span>
                      <span className="flex flex-wrap items-center justify-end gap-1 font-mono text-muted-foreground">
                        {row.error ? (
                          <span className="truncate text-destructive" title={row.error}>
                            {row.error}
                          </span>
                        ) : row.runs.length > 0 ? (
                          row.runs.map((run, index) => (
                            /* 时间数据可视化:最近一次运行品牌青高亮(下一跳最值得
                               关注),其余中性(源管理屏终审修整同款) */
                            <span
                              key={run}
                              className={
                                index === 0
                                  ? "inline-flex h-5 items-center rounded-sm border border-primary/40 bg-primary/10 px-1.5 font-mono text-2xs font-medium text-primary"
                                  : "inline-flex h-5 items-center rounded-sm border border-border/50 bg-muted/50 px-1.5 font-mono text-2xs"
                              }
                              title={index === 0 ? `最近一次即将运行:${run}` : run}
                            >
                              {formatScheduleRun(run)}
                            </span>
                          ))
                        ) : (
                          <span>—</span>
                        )}
                      </span>
                      {/* Kestra Flows Trigger 动作按钮范式:本行品类发起 run.start。
                          run 协议单飞(run_busy):忙碌期全区品类行禁点,发起行转 spinner */}
                      <Button
                        size="icon"
                        variant="ghost"
                        className="size-7"
                        disabled={runActiveFile !== null}
                        aria-label={`跑一次:${row.name}`}
                        title={`手动触发该品类采集一次(run.start ${row.file})`}
                        onClick={() => void handleRunOnce(row)}
                      >
                        {runActiveFile === row.file ? (
                          <Loader2 className="size-3.5 animate-spin" />
                        ) : (
                          <Play className="size-3.5" />
                        )}
                      </Button>
                    </li>
                  ))}
                </ul>
              )}
            </CardContent>
          </Card>
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

// 跑一次终态分色(runDoneTone)已随终态横幅弹窗化迁 run-once-result-dialog.tsx
// (outcomeVariant,10-05-run-once-result-dialog)

// ---------------------------------------------------------------------------
// job 表(九列契约 screen-spec §2,Stage 6 G2a 增「上次运行」列;colgroup
// 定宽 = sources-table 先例)
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
        <col className="w-35" />
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
          <TableHead>上次运行</TableHead>
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
        {/* G2a 上次运行(Stage 6):last_run_at 本地化,空 = 「—」
            (formatCronTime 内建;对位 H1202-1204 last: {formatTime(job.last_run_at)}) */}
        <TableCell>
          <span className="text-muted-foreground">{formatCronTime(job.last_run_at)}</span>
        </TableCell>
        <TableCell>
          {queued ? (
            <Badge variant="default" data-testid={`cron-queued-${job.id}`}>
              已排队
            </Badge>
          ) : badge ? (
            // G1(Stage 6):badge title 悬浮 last_error 细节(截断 120,
            // 对位 H1158-1166 title={lastResult.detail});有错才带,无错省键
            <Badge
              variant={badge.tone}
              title={job.last_error != null ? truncateCronText(job.last_error, 120) : undefined}
            >
              {badge.label}
            </Badge>
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
      {/* G2b(Stage 6)行下错误红行:主行后、展开行前,仅有值才渲染——
          last_error/last_delivery_error 各一行、截断 120(对位 H1218-1233
          三红行;我方无 last_fire_error 字段,蓝本第三行不搬) */}
      {job.last_error != null ? (
        <TableRow className="hover:bg-transparent">
          <TableCell colSpan={9} className="px-4 py-1 text-2xs text-destructive">
            <span className="block truncate" title={job.last_error}>
              上次错误:{truncateCronText(job.last_error, 120)}
            </span>
          </TableCell>
        </TableRow>
      ) : null}
      {job.last_delivery_error != null ? (
        <TableRow className="hover:bg-transparent">
          <TableCell colSpan={9} className="px-4 py-1 text-2xs text-destructive">
            <span className="block truncate" title={job.last_delivery_error}>
              投递错误:{truncateCronText(job.last_delivery_error, 120)}
            </span>
          </TableCell>
        </TableRow>
      ) : null}
      {isOpen ? (
        <TableRow className="hover:bg-transparent">
          {/* id 与展开钮 aria-controls 成对(logs 屏 163/261 先例) */}
          <TableCell id={`cron-runs-${job.id}`} colSpan={9} className="bg-sidebar/40 px-6 py-3">
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
  // G6(Stage 6)待聚焦字段 id(见下方聚焦效应)
  const [pendingFocus, setPendingFocus] = useState<string | null>(null);
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
    setPendingFocus(null);
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

  // G6(Stage 6)校验失败聚焦:首错字段 focus + scrollIntoView({block:
  // "center"})——对位 HJ cron-job.ts 77-85 focusCronField。错误字段在
  // 高级折叠内则先展开再聚焦:handleSubmit 同批 setAdvancedOpen(true)+
  // setPendingFocus(id)(React 18 批处理 = 同帧渲染),本效应在展开后的
  // DOM 上取元素聚焦。
  useEffect(() => {
    if (pendingFocus === null) return;
    const el = document.getElementById(pendingFocus);
    if (el === null) return;
    el.focus();
    el.scrollIntoView?.({ block: "center" });
    setPendingFocus(null);
  }, [pendingFocus]);

  const handleSubmit = () => {
    if (form.schedule.trim() === "") {
      setFormError("排程必填(如 every monday 9am / 0 9 * * * / in 30m)");
      setPendingFocus(fieldId("schedule"));
      return;
    }
    if (form.category.trim() === "") {
      setFormError("品类必填:从清单选择,或切「手输路径」");
      setPendingFocus(categoryMode === "manual" ? fieldId("category") : fieldId("category-select"));
      return;
    }
    // 数值字段前端校验(均在高级折叠内;文案 = entry.py invalid_params
    // 原文,错误回显「不吞不私造」纪律)——错则先展开折叠再聚焦
    if (form.repeat.trim() !== "" && !Number.isInteger(Number(form.repeat))) {
      setFormError("repeat 必须为整数(次数)");
      if (!advancedOpen) setAdvancedOpen(true);
      setPendingFocus(fieldId("repeat"));
      return;
    }
    const runTimeoutRaw = form.runTimeout.trim();
    if (runTimeoutRaw !== "" && !(Number(runTimeoutRaw) > 0)) {
      setFormError("run_timeout 必须为正数秒");
      if (!advancedOpen) setAdvancedOpen(true);
      setPendingFocus(fieldId("runTimeout"));
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
            {/* G3(Stage 6)可选 name:主字段组最上(schedule 之前)。
                create 非空才带键 / edit 走 diff —— cron-form buildPayload/
                fromJob 状态已备;留空后端缺省取品类文件名(jobs.py
                create_job `label_source = Path(category).name`[:50]) */}
            <div className="flex flex-col gap-1.5">
              <label htmlFor={fieldId("name")} className="text-xs font-medium text-foreground">
                名称(可选)
              </label>
              <Input
                id={fieldId("name")}
                value={form.name}
                onChange={(event) => setField("name", event.target.value)}
                placeholder="缺省取品类文件名"
                data-testid="cron-form-name"
              />
            </div>
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
          {/* G7(Stage 6)编辑 Dialog footer 左侧 font-mono 示 job.id
              (对位 H1065-1068 `{editJob.id}` mono 小字;create 不示) */}
          {mode === "edit" && job ? (
            <span
              className="mr-auto self-center truncate font-mono text-xs text-muted-foreground"
              title={job.id}
              data-testid="cron-edit-job-id"
            >
              {job.id}
            </span>
          ) : null}
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
