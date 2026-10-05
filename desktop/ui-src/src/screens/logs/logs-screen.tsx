import { useCallback, useEffect, useMemo, useRef, useState } from "react";
import {
  Check,
  ChevronDown,
  CirclePlay,
  CircleStop,
  CircleX,
  CircleCheck,
  Copy,
  Loader2,
  RefreshCw,
  RotateCcw,
  Search,
  TriangleAlert,
  X,
} from "lucide-react";

import { EmptyState } from "@/components/empty-state";
import { PageHeader } from "@/components/layout/page-header";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Skeleton } from "@/components/ui/skeleton";
import { SidecarRequestError } from "@/lib/api";
import type { RunEntry, SidecarEvent, UnlistenFn } from "@/lib/api";

import {
  buildRunRows,
  eventToRow,
  filterRunRows,
  isRowError,
  isRowWarn,
  loadRunLogs,
  loadRuns,
  rerunRun,
  rowMatchesQuery,
  splitTextOnQuery,
  subscribeRunEvents,
  tailToRows,
} from "./api";
import type { LogRow, RunFilterStatus, RunRowModel } from "./api";

/**
 * 采集日志(D4 结构性重做;10-04-ui-kestra-anchor 重锚 Kestra):
 * 列表态对标 kestra/ui/src/components/executions/Executions.vue(KsDataTable
 * 表行解剖 [Apache-2.0,借结构改语义])——满高列表容器(section.full-container
 * 同款:列表内滚、过滤条常驻)+ 定宽槽位列对齐(#id mono · 品类 · 相对开始
 * 时间(KsDateAgo inverted 同义)· 耗时 mono · 状态小芯片(KsExecutionStatus
 * small:24px 高/xs 12px/描边圆图标/状态色淡底))。
 * 展开态对标同目录 Gantt.vue 头部解剖:摘要组(总耗时/行数/错误行)+ 行尾
 * 动作(复制日志 link 钮 + 状态),日志体仍等宽终端块。
 * 不抄:Kestra 复选/批量操作/分页/列配置/CSV 导出(单机单 run 单飞,无此域,
 * 功能面零改动 R5);Gantt 逐任务时间条(协议无 taskRunList 时间轴,造假数据
 * 违反像素双真源)。
 * 数据面不变:run.status + logs.tail(展开时惰性拉取,缓存)+ sidecar://event 续播。
 *
 * G7 三件:①run 行重跑(骑 G4 手动触发通道 run.start,不新增协议;成功反馈
 * 新 run_id,新 run 经列表刷新自动展开跟随);②品类·状态过滤条(与源管理
 * compact 密度同款 select);③日志搜索(输入即过滤 + 命中片段高亮)。
 */

/** 状态过滤键 → 过滤选项文案(与 runBadge 同词表) */
const STATUS_FILTER_OPTIONS: Array<{ value: RunFilterStatus; label: string }> = [
  { value: "running", label: "运行中" },
  { value: "success", label: "成功" },
  { value: "partial", label: "部分" },
  { value: "config_error", label: "配置" },
  { value: "failed", label: "失败" },
  { value: "cancelled", label: "已取消" },
];

/** run 状态 → 状态芯片模型(Kestra KsExecutionStatus 解剖:图标+文案+状态色;
 * 退出码语义 0/1/2/3 + cancelled,见 types.ts RunExitStatus) */
function runBadge(status: RunEntry["status"], state: RunEntry["state"]) {
  if (state === "running" || status === null) {
    return { variant: "default" as const, label: "运行中", icon: CirclePlay };
  }
  switch (status) {
    case "success":
      return { variant: "ok" as const, label: "成功", icon: CircleCheck };
    case "partial":
      return { variant: "warning" as const, label: "部分", icon: TriangleAlert };
    case "config_error":
      return { variant: "warning" as const, label: "配置", icon: TriangleAlert };
    case "failed":
      return { variant: "destructive" as const, label: "失败", icon: CircleX };
    case "cancelled":
      // run.cancel 信号终局(C2,v1.1.2 桌面对齐批)
      return { variant: "unknown" as const, label: "已取消", icon: CircleStop };
  }
}

/** 状态芯片(Kestra KsExecutionStatus small 档:高 24px/字 xs 12px/圆角 6px/
 * 状态色文字+淡底+描边圆图标;色比沿用 Badge 四态实算档,WCAG 不降级) */
const STATUS_CHIP_TONE: Record<string, string> = {
  default: "border-primary/25 bg-primary/15 text-primary",
  ok: "border-ok/30 bg-ok/15 text-ok",
  warning: "border-warning/30 bg-warning/15 text-warning",
  destructive: "border-destructive/30 bg-destructive/15 text-[#ff6b70]",
  unknown: "border-unknown/30 bg-unknown/10 text-unknown",
};
function StatusChip({
  badge,
  testId,
}: {
  badge: { variant: "default" | "ok" | "warning" | "destructive" | "unknown"; label: string; icon: typeof CircleCheck };
  testId?: string;
}) {
  const Icon = badge.icon;
  return (
    <span
      data-testid={testId}
      className={`inline-flex h-6 shrink-0 items-center gap-1 rounded-[6px] border px-2 text-xs font-medium tabular-nums ${STATUS_CHIP_TONE[badge.variant]}`}
    >
      <Icon aria-hidden className="size-3.5" />
      {badge.label}
    </span>
  );
}

/** 相对开始时间(Kestra KsDateAgo inverted 同义:列表里读「多久前」比绝对时间快;
 * title 挂绝对时间补全语义) */
function formatRelative(iso: string | undefined): string {
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

/** 命中片段 <mark>:警示底 + 前景保持行色系(只标记不改语,WCAG 不降级) */
function HighlightedText({ text, needle }: { text: string; needle: string }) {
  if (needle === "") return <>{text}</>;
  return (
    <>
      {splitTextOnQuery(text, needle).map((part, index) =>
        part.hit ? (
          <mark
            key={index}
            data-testid="log-search-hit"
            className="rounded-[2px] bg-warning/30 text-foreground underline decoration-warning/60 decoration-1 underline-offset-2"
          >
            {part.text}
          </mark>
        ) : (
          <span key={index}>{part.text}</span>
        ),
      )}
    </>
  );
}

function LogRowView({ row, needle }: { row: LogRow; needle: string }) {
  if (row.stream === "system") {
    return (
      <p data-testid="log-system-row" className="whitespace-pre-wrap break-words text-muted-foreground/80">
        <span className="mr-1.5 text-brand-from">▸</span>
        <HighlightedText text={row.text} needle={needle} />
      </p>
    );
  }
  const error = isRowError(row);
  const warn = isRowWarn(row);
  return (
    <p
      data-testid="log-row"
      data-error={error ? "true" : undefined}
      data-warn={warn ? "true" : undefined}
      className={
        error
          ? // 错误行 dead 色高亮(D4;P2 对比实算:bg-dead/10 叠 bg-sidebar ≈ 4.67:1,
            // 原 bg-dead/15 ≈ 4.43:1 不达 WCAG AA 正文 4.5,降档到 /10)
            "whitespace-pre-wrap break-words rounded-sm bg-dead/10 px-1 text-dead"
          : warn
            ? "whitespace-pre-wrap break-words px-1 text-warning/85" // WARNING 级 / 裸 stderr 诊断行弱警示
            : "whitespace-pre-wrap break-words px-1 text-foreground/90"
      }
    >
      <span className="mr-1.5 text-muted-foreground/60">·</span>
      <HighlightedText text={row.text} needle={needle} />
    </p>
  );
}

/** 重跑状态反馈(G7):starting 打转 → triggered 报新 run_id → 8s 后自动隐去 */
type RerunState =
  | { phase: "starting" }
  | { phase: "triggered"; runId: number }
  | { phase: "error"; message: string };

/**
 * 折叠组头 = 每 run 统计行,解剖对位 Kestra Executions.vue 表行(定宽槽位列
 * 对齐):#id mono(KsId)· 品类(KsEntityLink 位)· 相对开始时间(KsDateAgo
 * inverted)· 耗时 mono(Duration)· 状态芯片(KsExecutionStatus small)。
 * 错误行数/条数沿用 G7 口径放时间槽左侧。折叠控件与重跑按钮是兄弟节点
 * (button 不可嵌套);testid/aria-expanded 留在折叠按钮上(它才是展开语义的owner)。
 */
function RunGroupHeader({
  run,
  badge,
  errorCount,
  startedAt,
  expanded,
  onToggle,
  rerun,
  onRerun,
}: {
  run: RunRowModel;
  badge: { variant: "default" | "ok" | "warning" | "destructive" | "unknown"; label: string; icon: typeof CircleCheck };
  errorCount: number;
  startedAt: string | undefined;
  expanded: boolean;
  onToggle: (runId: number) => void;
  rerun: RerunState | undefined;
  onRerun: (run: RunRowModel) => void;
}) {
  const starting = rerun?.phase === "starting";
  return (
    <div className="flex min-h-11 items-center gap-1 pr-2 transition-colors duration-(--duration-fast) hover:bg-accent/60">
      <button
        type="button"
        data-testid={`run-group-header-${run.runId}`}
        aria-expanded={expanded}
        aria-controls={`run-group-body-${run.runId}`}
        onClick={() => onToggle(run.runId)}
        className="flex min-h-11 min-w-0 flex-1 items-center gap-2.5 px-3 py-2 text-left"
      >
        <ChevronDown
          aria-hidden
          className={`size-3.5 shrink-0 text-muted-foreground transition-transform duration-(--duration-fast) ${expanded ? "" : "-rotate-90"}`}
        />
        {/* KsId 档:mono 弱色,定宽槽让多行 id 列对齐 */}
        <span className="w-9 shrink-0 font-mono text-xs text-muted-foreground">#{run.runId}</span>
        {/* KsEntityLink 位:品类即 run 的「流程」主体(不可点,不作链接色——
            Kestra 该槽是 RouterLink,我们行级折叠为主交互,诚实呈现) */}
        <span className="min-w-0 flex-1 truncate text-[13px] font-medium text-foreground">{run.category}</span>
        {run.dry ? (
          <Badge variant="outline" title="dry run(不落库)">
            试跑
          </Badge>
        ) : null}
        <span className="ml-auto flex shrink-0 items-center gap-3 text-2xs text-muted-foreground">
          {errorCount > 0 ? (
            <span data-testid={`run-error-count-${run.runId}`} className="w-[64px] shrink-0 text-right font-medium text-[#ff6b70]">
              {/* #ff6b70 而非 text-dead:组头 hover 底 accent/60 上 4.35<4.5,#ff6b70 实算 5.5+(WCAG) */}
              {errorCount} 错误行
            </span>
          ) : (
            <span className="w-[64px] shrink-0" aria-hidden />
          )}
          {/* 条数槽常渲染(空占位)——Kestra 表行列对齐:任何行同槽同位 */}
          {run.itemCount !== null ? (
            <span className="w-11 shrink-0 text-right tabular-nums">{run.itemCount} 条</span>
          ) : (
            <span className="w-11 shrink-0" aria-hidden />
          )}
          {/* KsDateAgo inverted:相对开始时间,title 绝对时间 */}
          <span className="w-[68px] shrink-0 text-right tabular-nums" title={startedAt ?? undefined}>
            {formatRelative(startedAt)}
          </span>
          {/* Duration:mono 定宽右对齐 */}
          <span className="w-[56px] shrink-0 text-right font-mono">{run.durationText}</span>
          <StatusChip badge={badge} testId={`run-status-chip-${run.runId}`} />
        </span>
      </button>
      {rerun?.phase === "triggered" ? (
        <span
          data-testid={`run-rerun-ok-${run.runId}`}
          className="shrink-0 text-2xs font-medium text-ok"
          title={`新 run #${rerun.runId} 已启动,正在展开跟随`}
        >
          已触发 #{rerun.runId}
        </span>
      ) : null}
      {rerun?.phase === "error" ? (
        <span
          data-testid={`run-rerun-err-${run.runId}`}
          className="max-w-44 shrink-0 truncate text-2xs text-destructive"
          title={rerun.message}
        >
          {rerun.message}
        </span>
      ) : null}
      <Button
        variant="ghost"
        size="icon"
        className="size-6 shrink-0 text-muted-foreground"
        data-testid={`run-rerun-${run.runId}`}
        aria-label={`重跑采集 #${run.runId}`}
        title={`重跑该 run(run.start 回放 ${run.yaml}${run.dry ? ",dry" : ""})`}
        disabled={starting}
        onClick={() => onRerun(run)}
      >
        {starting ? (
          <Loader2 aria-hidden className="size-3.5 animate-spin" />
        ) : (
          <RotateCcw aria-hidden className="size-3.5" />
        )}
      </Button>
    </div>
  );
}

/**
 * 展开组的日志体:头部解剖对标 Kestra Gantt.vue 卡头——左侧摘要组
 * (总耗时/行数/错误行,「/」分隔)+ 右侧行尾动作(复制日志 link 钮
 * ContentCopy 同位 + 截断/实时徽标);来源标记 logs.tail run_id=N 并入摘要尾。
 * 日志体 = 等宽终端块,新行到达自动滚底(Crawlab revealLine 同款,无条件滚)。
 * 搜索态(G7):needle 非空时行集即时过滤(命中才显示)+ 命中片段高亮,
 * 摘要报「命中 X / Y 行」。
 */
function RunLogBody({
  runId,
  rows,
  durationText,
  truncated,
  loadError,
  running,
  live,
  needle,
}: {
  runId: number;
  rows: LogRow[] | undefined;
  durationText: string;
  truncated: boolean;
  loadError: string | null;
  running: boolean;
  live: boolean;
  needle: string;
}) {
  const scrollRef = useRef<HTMLDivElement | null>(null);
  const [copied, setCopied] = useState<null | { ok: boolean; count: number }>(null);
  const searching = needle !== "";
  const shownRows = useMemo(
    () => (rows === undefined ? undefined : searching ? rows.filter((row) => rowMatchesQuery(row, needle)) : rows),
    [rows, searching, needle],
  );
  const errorCount = rows?.filter(isRowError).length ?? 0;

  // 自动滚底(D4):行集变化即贴底(终端惯例;展开瞬间 rows 未必到位,依赖数组带 rows 兜两拍)
  useEffect(() => {
    const el = scrollRef.current;
    if (el !== null) el.scrollTop = el.scrollHeight;
  }, [shownRows, runId]);

  /** 复制日志(Gantt copyAllLogs 同位):复制该 run 全部行(不受搜索过滤影响);
   *  无头/无焦点环境 clipboard 可能拒绝,失败如实回显 */
  const copyLogs = useCallback(() => {
    if (rows === undefined || rows.length === 0) return;
    const text = rows.map((row) => row.text).join("\n");
    void navigator.clipboard
      .writeText(text)
      .then(() => setCopied({ ok: true, count: rows.length }))
      .catch(() => setCopied({ ok: false, count: rows.length }));
  }, [rows]);
  useEffect(() => {
    if (copied === null) return;
    const timer = setTimeout(() => setCopied(null), 2000);
    return () => clearTimeout(timer);
  }, [copied]);

  return (
    <div id={`run-group-body-${runId}`} data-testid={`run-log-${runId}`} className="border-t border-border bg-sidebar">
      <div
        data-testid={`run-log-meta-${runId}`}
        className="flex flex-wrap items-center justify-between gap-x-3 gap-y-1 px-4 py-2 text-2xs text-muted-foreground"
      >
        {/* Gantt 卡头摘要组:label 弱色 + value,「/」分隔 */}
        <span className="flex min-w-0 items-center gap-2">
          <span className="shrink-0">
            <span className="mr-1">总耗时</span>
            <span className="font-mono">{durationText}</span>
          </span>
          <span aria-hidden className="text-muted-foreground/50">/</span>
          <span className="shrink-0">{rows?.length ?? 0} 行</span>
          {errorCount > 0 ? (
            <>
              <span aria-hidden className="text-muted-foreground/50">/</span>
              <span className="shrink-0 font-medium text-[#ff6b70]">{errorCount} 错误行</span>
            </>
          ) : null}
          <span aria-hidden className="text-muted-foreground/50">/</span>
          <span className="min-w-0 truncate font-mono">logs.tail run_id={runId}</span>
        </span>
        <span className="flex shrink-0 items-center gap-2.5">
          {truncated ? <Badge variant="outline">缓冲截断</Badge> : null}
          {shownRows !== undefined ? (
            searching ? (
              <span data-testid={`run-log-hits-${runId}`} className="font-mono">
                命中 {shownRows.length} / {rows?.length ?? 0} 行
              </span>
            ) : null
          ) : null}
          {running ? <Badge variant={live ? "ok" : "unknown"}>{live ? "实时跟踪中" : "未跟踪"}</Badge> : null}
          <button
            type="button"
            data-testid={`run-log-copy-${runId}`}
            onClick={copyLogs}
            disabled={rows === undefined || rows.length === 0}
            className="inline-flex shrink-0 items-center gap-1 rounded-sm text-2xs font-medium text-link transition-colors duration-(--duration-fast) hover:text-foreground disabled:cursor-not-allowed disabled:opacity-50"
          >
            {copied?.ok ? (
              <Check aria-hidden className="size-3" />
            ) : (
              <Copy aria-hidden className="size-3" />
            )}
            {copied === null ? "复制日志" : copied.ok ? `已复制 ${copied.count} 行` : "复制失败(剪贴板拒绝)"}
          </button>
        </span>
      </div>
      {/* 终审修整:日志体四周呼吸(px-3→px-4 + 顶部 pt)+ 行间 gap
          (VL 指认「行距过密、状态标签与时间戳贴边」) */}
      <div
        ref={scrollRef}
        className="flex max-h-[26rem] flex-col gap-1 overflow-y-auto px-4 pt-2 pb-3 font-mono text-xs leading-relaxed"
      >
        {loadError !== null ? (
          <p className="text-dead">
            <span className="mr-1.5">●</span>日志加载失败({loadError})
          </p>
        ) : rows === undefined ? (
          <p className="text-muted-foreground">
            <span className="text-brand-from">▍</span> 正在拉取 logs.tail…
          </p>
        ) : searching && shownRows !== undefined && shownRows.length === 0 ? (
          <p className="text-muted-foreground">
            <span className="text-brand-from">▍</span> 无命中行(搜索词过滤掉了这轮采集的全部日志)
          </p>
        ) : rows.length === 0 ? (
          <p className="text-muted-foreground">
            <span className="text-brand-from">▍</span> 这轮采集暂无日志(环形缓冲只保留最近 4000 行)
          </p>
        ) : (
          shownRows?.map((row) => <LogRowView key={row.key} row={row} needle={needle} />)
        )}
      </div>
    </div>
  );
}

export function LogsScreen() {
  const [runs, setRuns] = useState<RunEntry[]>([]);
  /** 逐 run 日志行:展开时 tail 打底 + 事件续播(未加载的 run 先缓冲,加载时合并) */
  const [rowsByRun, setRowsByRun] = useState<Record<number, LogRow[]>>({});
  const [truncatedByRun, setTruncatedByRun] = useState<Record<number, boolean>>({});
  /** 逐 run tail 拉取失败(code:message);成功即清除,重展开可重试 */
  const [loadErrors, setLoadErrors] = useState<Record<number, string>>({});
  const [expanded, setExpanded] = useState<ReadonlySet<number>>(new Set());
  const [live, setLive] = useState(false);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<SidecarRequestError | null>(null);
  const eventSeq = useRef(0);
  /** 已成功 tail 打底的 run(重展开不重拉,缓存驻屏) */
  const loadedRunsRef = useRef<Set<number>>(new Set());
  /** 拉取在途的 run(防双发) */
  const fetchingRef = useRef<Set<number>>(new Set());
  /** 已见过的 run_id(自动跟随=新出现的 running run 才展开,不打扰用户折叠态) */
  const knownRunIdsRef = useRef<Set<number>>(new Set());

  /** 展开 run 的日志惰性加载(Kestra 步骤展开同款):首次展开才 logs.tail;
   *  加载期间到达的事件行已在缓冲,合并时排在 tail 历史之后(事件比快照新) */
  const ensureTail = useCallback((runId: number) => {
    if (loadedRunsRef.current.has(runId) || fetchingRef.current.has(runId)) return;
    fetchingRef.current.add(runId);
    void loadRunLogs(runId)
      .then((tail) => {
        loadedRunsRef.current.add(runId);
        setRowsByRun((prev) => ({ ...prev, [runId]: [...tailToRows(tail), ...(prev[runId] ?? [])] }));
        setTruncatedByRun((prev) => ({ ...prev, [runId]: tail.truncated }));
        setLoadErrors((prev) => {
          if (!(runId in prev)) return prev;
          const next = { ...prev };
          delete next[runId];
          return next;
        });
      })
      .catch((err) => {
        const message = err instanceof SidecarRequestError ? `${err.code} · ${err.message}` : String(err);
        setLoadErrors((prev) => ({ ...prev, [runId]: message }));
      })
      .finally(() => {
        fetchingRef.current.delete(runId);
      });
  }, []);

  const refreshRuns = useCallback(async () => {
    try {
      const list = await loadRuns();
      setRuns(list);
      // 跟随策略(Crawlab 活动任务跟踪同款):初次进屏展开最新 run;
      // 之后仅新出现的 running run 自动展开跟随,用户折叠过的不强扒
      const known = knownRunIdsRef.current;
      let followId: number | null = null;
      if (known.size === 0 && list.length > 0) {
        followId = list[0].run_id;
      } else {
        const newcomer = list.find((run) => run.state === "running" && !known.has(run.run_id));
        followId = newcomer ? newcomer.run_id : null;
      }
      if (followId !== null) {
        const target = followId;
        setExpanded((prev) => (prev.has(target) ? prev : new Set(prev).add(target)));
        ensureTail(target);
      }
      knownRunIdsRef.current = new Set(list.map((run) => run.run_id));
    } catch (err) {
      setError(
        err instanceof SidecarRequestError
          ? err
          : new SidecarRequestError({ code: "transport_error", path: "$", message: String(err) }),
      );
    }
  }, [ensureTail]);

  useEffect(() => {
    void (async () => {
      setLoading(true);
      await refreshRuns();
      setLoading(false);
    })();
  }, [refreshRuns]);

  /** 事件流订阅(挂屏一次,不随展开态变化):任意 run 的事件按 run_id 归组缓冲;
   *  completed 另触发列表刷新(终态/耗时落表)。 */
  useEffect(() => {
    let cancelled = false;
    const unlisten: Promise<UnlistenFn> = subscribeRunEvents((event: SidecarEvent) => {
      // 采集日志只续播 run 域事件(log/progress/completed;10-03-vision-pipeline
      // 拆屏后协议已无 image.* 事件,过滤保留为穷尽防御)
      if (event.type !== "log" && event.type !== "progress" && event.type !== "completed") return;
      if (event.type === "completed") {
        void refreshRuns();
      }
      eventSeq.current += 1;
      const row = eventToRow(event, eventSeq.current);
      // run 域事件必带 run_id;null 分支仅为类型穷尽(提取局部量以保持闭包内收窄)
      const runId = row.runId;
      if (runId === null) return;
      setRowsByRun((prev) => ({ ...prev, [runId]: [...(prev[runId] ?? []), row] }));
    }).then((fn) => {
      if (!cancelled) setLive(true);
      return fn;
    });
    unlisten.catch(() => {
      // 事件通道不可用(如浏览器直开):tail 历史仍可用,不拦界面
    });
    return () => {
      cancelled = true;
      setLive(false);
      void unlisten.then((fn) => fn()).catch(() => undefined);
    };
  }, [refreshRuns]);

  const handleToggle = useCallback(
    (runId: number) => {
      if (!expanded.has(runId)) ensureTail(runId);
      setExpanded((prev) => {
        const next = new Set(prev);
        if (next.has(runId)) next.delete(runId);
        else next.add(runId);
        return next;
      });
    },
    [expanded, ensureTail],
  );

  const runRows = useMemo(() => buildRunRows(runs), [runs]);
  /** run_id → started_at(相对时间用;不进 RunRowModel——api.ts 属数据层,
   *  展示派生留视图层) */
  const startedAtById = useMemo(() => new Map(runs.map((run) => [run.run_id, run.started_at])), [runs]);

  // ---- G7:过滤(品类·状态)+ 搜索 + 重跑 ---------------------------------

  const [categoryFilter, setCategoryFilter] = useState("all");
  const [statusFilter, setStatusFilter] = useState<RunFilterStatus | "all">("all");
  const [query, setQuery] = useState("");
  /** 逐 run 重跑反馈(starting/triggered/error;8s 自动隐去) */
  const [rerunByRun, setRerunByRun] = useState<Record<number, RerunState>>({});
  const rerunTimersRef = useRef<Map<number, ReturnType<typeof setTimeout>>>(new Map());

  const needle = query.trim().toLowerCase();
  const categories = useMemo(() => Array.from(new Set(runRows.map((row) => row.category))).sort(), [runRows]);
  const visibleRunRows = useMemo(
    () => filterRunRows(runRows, categoryFilter, statusFilter),
    [runRows, categoryFilter, statusFilter],
  );
  const filtering = categoryFilter !== "all" || statusFilter !== "all";

  const clearRerunFeedback = useCallback((runId: number) => {
    setRerunByRun((prev) => {
      if (!(runId in prev)) return prev;
      const next = { ...prev };
      delete next[runId];
      return next;
    });
  }, []);

  /** 反馈 8s 自动隐去(定时器挂 ref,卸载统一清) */
  const scheduleRerunClear = useCallback((runId: number) => {
    const timers = rerunTimersRef.current;
    const previous = timers.get(runId);
    if (previous !== undefined) clearTimeout(previous);
    timers.set(
      runId,
      setTimeout(() => {
        timers.delete(runId);
        clearRerunFeedback(runId);
      }, 8000),
    );
  }, [clearRerunFeedback]);

  useEffect(() => {
    const timers = rerunTimersRef.current;
    return () => {
      for (const timer of timers.values()) clearTimeout(timer);
      timers.clear();
    };
  }, []);

  /**
   * 重跑(G7①):骑 G4 手动触发通道 run.start 回放 yaml/dry/db——不新增协议;
   * 成功反馈新 run_id 并刷新列表(follow 策略自动展开新 running run 承担
   * 「正在跑」主反馈);失败如实报错误码。
   */
  const handleRerun = useCallback(
    (run: RunRowModel) => {
      setRerunByRun((prev) => ({ ...prev, [run.runId]: { phase: "starting" } }));
      void rerunRun(run)
        .then((started) => {
          setRerunByRun((prev) => ({ ...prev, [run.runId]: { phase: "triggered", runId: started.run_id } }));
          scheduleRerunClear(run.runId);
          void refreshRuns();
        })
        .catch((err) => {
          const message = err instanceof SidecarRequestError ? `${err.code} · ${err.message}` : String(err);
          setRerunByRun((prev) => ({ ...prev, [run.runId]: { phase: "error", message } }));
          scheduleRerunClear(run.runId);
        });
    },
    [refreshRuns, scheduleRerunClear],
  );

  const resetFilters = useCallback(() => {
    setCategoryFilter("all");
    setStatusFilter("all");
    setQuery("");
  }, []);

  /** 终审修整:run 状态分布(状态条可视化,VL 指认「全屏无任何图表/进度
   * 可视化」)——与 runBadge 同一词表聚档,零新协议,纯视图层派生 */
  const statusDist = useMemo(() => {
    const dist = { running: 0, success: 0, partial: 0, failed: 0, other: 0 } as Record<string, number>;
    for (const run of visibleRunRows) {
      if (run.state === "running" || run.status === null) dist.running += 1;
      else if (run.status === "success") dist.success += 1;
      else if (run.status === "partial" || run.status === "config_error") dist.partial += 1;
      else if (run.status === "failed") dist.failed += 1;
      else dist.other += 1;
    }
    return dist;
  }, [visibleRunRows]);
  const distSegments = [
    { key: "success", label: "成功", tone: "bg-ok", count: statusDist.success },
    { key: "running", label: "运行中", tone: "bg-primary", count: statusDist.running },
    { key: "partial", label: "部分/配置", tone: "bg-warning", count: statusDist.partial },
    { key: "failed", label: "失败", tone: "bg-dead", count: statusDist.failed },
    { key: "other", label: "其他", tone: "bg-unknown", count: statusDist.other },
  ].filter((segment) => segment.count > 0);

  return (
    /* 满高列表容器(对标 Kestra app.scss section.full-container:列表内滚、
     * 过滤条/节头常驻;R2 的 gap-block 页面滚动让位) */
    <div className="flex h-full min-h-0 flex-col gap-4">
      <PageHeader
        title="采集日志"
        description="采集记录瀑布(新→旧)· 逐轮耗时/条数统计 · 错误行高亮 · 展开组流式续播自动滚底"
        actions={
          <Button variant="outline" size="sm" onClick={() => void refreshRuns()} disabled={loading}>
            <RefreshCw className={loading ? "size-3.5 animate-spin" : "size-3.5"} />
            刷新
          </Button>
        }
      />

      {/* 过滤条(G7②③):品类/状态 select + 日志搜索。
          R2 刀4:一行控件统一 32px 档(default size),与源管理工具行同族 */}
      <div className="flex flex-wrap items-center gap-2 px-6" data-testid="logs-filter-bar">
        <Select value={categoryFilter} onValueChange={setCategoryFilter}>
          <SelectTrigger
            className="max-w-48 text-muted-foreground"
            aria-label="品类过滤"
            data-testid="filter-category"
          >
            <SelectValue />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="all">全部品类</SelectItem>
            {categories.map((category) => (
              <SelectItem key={category} value={category}>
                {category}
              </SelectItem>
            ))}
          </SelectContent>
        </Select>
        <Select value={statusFilter} onValueChange={(value) => setStatusFilter(value as RunFilterStatus | "all")}>
          <SelectTrigger
            className="text-muted-foreground"
            aria-label="状态过滤"
            data-testid="filter-status"
          >
            <SelectValue />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="all">全部状态</SelectItem>
            {STATUS_FILTER_OPTIONS.map((option) => (
              <SelectItem key={option.value} value={option.value}>
                {option.label}
              </SelectItem>
            ))}
          </SelectContent>
        </Select>
        {filtering ? (
          <Button variant="ghost" className="gap-1 px-2 text-muted-foreground" onClick={resetFilters}>
            <X aria-hidden className="size-3.5" />
            清除过滤
          </Button>
        ) : null}
        <span className="text-2xs text-muted-foreground" data-testid="logs-filter-count">
          {visibleRunRows.length} / {runRows.length} 轮
        </span>
        <div className="relative ml-auto">
          <Search aria-hidden className="pointer-events-none absolute top-1/2 left-2.5 size-3.5 -translate-y-1/2 text-muted-foreground/70" />
          <Input
            type="search"
            value={query}
            onChange={(event) => setQuery(event.target.value)}
            placeholder="搜索日志(输入即过滤,命中高亮)"
            aria-label="搜索日志"
            data-testid="log-search-input"
            className="w-64 pl-8 font-mono"
          />
        </div>
      </div>

      {error ? (
        <div className="px-6">
          <Card data-testid="logs-error">
            <CardContent>
              <p className="text-sm font-medium text-destructive">
                采集日志不可用(sidecar 错误码 {error.code})
              </p>
              <p className="mt-1 text-xs text-muted-foreground">{error.message}</p>
            </CardContent>
          </Card>
        </div>
      ) : null}

      <div className="flex min-h-0 flex-1 flex-col gap-3 px-6">
        {/* 终审修整:节头 + run 状态分布条——VL 指认「页面标题与区块标题字号无
            级差、全屏无图表/进度可视化」;分布条与图例同 render,纯视图派生 */}
        <div className="flex flex-wrap items-center justify-between gap-2">
          <div className="flex items-center gap-2">
            <h2 className="text-base font-semibold text-foreground">运行历史</h2>
            <span className="text-2xs text-muted-foreground">
              {visibleRunRows.length} / {runRows.length} 轮 · 新→旧
            </span>
          </div>
          <div className="flex flex-wrap items-center gap-3">
            {distSegments.map((segment) => (
              <span key={segment.key} className="inline-flex items-center gap-1.5 text-2xs text-muted-foreground">
                <span aria-hidden className={`size-1.5 rounded-full ${segment.tone}`} />
                {segment.label} {segment.count}
              </span>
            ))}
          </div>
        </div>
        <div
          className="flex h-1.5 w-full overflow-hidden rounded-full bg-muted/60"
          data-testid="run-status-distribution"
          role="img"
          aria-label={`采集状态分布:${distSegments.map((s) => `${s.label} ${s.count}`).join("、") || "无采集"}`}
        >
          {distSegments.map((segment) => (
            <span
              key={segment.key}
              className={segment.tone}
              style={{ width: `${(segment.count / Math.max(visibleRunRows.length, 1)) * 100}%` }}
              title={`${segment.label} ${segment.count}`}
            />
          ))}
        </div>
        {/* run 瀑布:每 run 一段折叠组(Crawlab 运行瀑布 + Kestra 步骤折叠);
            列表区内滚(full-container),组间 gap-grid 令牌 */}
        <div className="flex min-h-0 flex-1 flex-col gap-grid overflow-y-auto pb-block" data-testid="run-waterfall">
          {loading && runs.length === 0 ? (
            <>
              <Skeleton className="h-12 w-full rounded-lg" />
              <Skeleton className="h-12 w-full rounded-lg" />
              <Skeleton className="h-12 w-full rounded-lg" />
            </>
          ) : runRows.length === 0 ? (
            <Card>
              <CardContent>
                <EmptyState
                  compact
                  title="还没有采集记录"
                  description="从源管理触发一次采集后,采集记录将按新→旧出现在这里"
                />
              </CardContent>
            </Card>
          ) : visibleRunRows.length === 0 ? (
            <Card>
              <CardContent>
                <EmptyState
                  compact
                  title="没有匹配的采集记录"
                  description="品类/状态过滤或搜索词没有命中任何采集记录,放宽条件再试"
                />
                <div className="mt-3 flex justify-center">
                  <Button variant="outline" size="sm" onClick={resetFilters}>
                    清除过滤
                  </Button>
                </div>
              </CardContent>
            </Card>
          ) : (
            visibleRunRows.map((run) => {
              const badge = runBadge(run.status, run.state);
              const rows = rowsByRun[run.runId];
              const errorCount = rows?.filter(isRowError).length ?? 0;
              return (
                <div
                  key={run.runId}
                  data-testid={`run-group-${run.runId}`}
                  className="overflow-hidden rounded-lg border border-border bg-card animate-fade-in"
                >
                  <RunGroupHeader
                    run={run}
                    badge={badge}
                    errorCount={errorCount}
                    startedAt={startedAtById.get(run.runId)}
                    expanded={expanded.has(run.runId)}
                    onToggle={handleToggle}
                    rerun={rerunByRun[run.runId]}
                    onRerun={handleRerun}
                  />
                  {expanded.has(run.runId) ? (
                    <RunLogBody
                      runId={run.runId}
                      rows={rows}
                      durationText={run.durationText}
                      truncated={truncatedByRun[run.runId] ?? false}
                      loadError={loadErrors[run.runId] ?? null}
                      running={run.state === "running"}
                      live={live}
                      needle={needle}
                    />
                  ) : null}
                </div>
              );
            })
          )}
        </div>
      </div>
    </div>
  );
}
