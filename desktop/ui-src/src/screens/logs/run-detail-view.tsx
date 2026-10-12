import { useCallback, useEffect, useMemo, useRef, useState } from "react";
import { Check, ChevronLeft, Copy, Loader2, RotateCcw, Search } from "lucide-react";

import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";

import {
  domIdOf,
  formatAbsolute,
  formatRelative,
  isRowError,
  isRowWarn,
  rowMatchesQuery,
  splitTextOnQuery,
  synthesizeFailure,
} from "./api";
import type { LogRow, RerunState, RunRowModel } from "./api";
import { FailurePanel } from "./failure-panel";
import { runBadge, StatusChip } from "./run-status-chip";

/**
 * L2 轮详情页(10-12-logs-two-level-ui §3):页面级视图(非弹窗,PRD 判例 5),
 * 与 L1 互斥分支替换渲染。三分区(design §1):元信息头(固定)→ 失败原因区
 * (固定,仅终态非 success)→ 日志体(主滚动区独占滚动)。
 * 头区解剖借 feed v8 2 级工具条(feed-screen.tsx:3505 返回钮 + 词面同族,
 * flex flex-wrap items-center gap-2 border-b px-5 py-2.5);日志体 = 现状
 * RunLogBody 升格页面主体:内滚帽 max-h-[26rem] 解除(accordion 时代的卡内
 * 帽)→ flex-1 min-h-0 满高,「去内滚帽、滚动交中段」feed 整屏化同律。
 * 塌缩律(67546cd 不回归):日志体内滚容器直接 flex 子项(日志行/降级文案
 * 行)一律显式 shrink-0。
 */

export interface RunDetailViewProps {
  run: RunRowModel;
  startedAt: string | null | undefined;
  finishedAt: string | null | undefined;
  rows: LogRow[] | undefined;
  truncated: boolean;
  loadError: string | null;
  live: boolean;
  /** 日志搜索词(状态挂编排层,切级不重置,design §4.2;词面已 trim+lower) */
  query: string;
  onQueryChange: (value: string) => void;
  rerun: RerunState | undefined;
  onRerun: (run: RunRowModel) => void;
  onBack: () => void;
}

export function RunDetailView({
  run,
  startedAt,
  finishedAt,
  rows,
  truncated,
  loadError,
  live,
  query,
  onQueryChange,
  rerun,
  onRerun,
  onBack,
}: RunDetailViewProps) {
  const domId = domIdOf(run);
  const badge = runBadge(run.status, run.state);
  const failure = useMemo(() => synthesizeFailure(run, rows), [run, rows]);
  const running = run.state === "running";
  const needle = query.trim().toLowerCase();
  const searching = needle !== "";
  const shownRows = useMemo(
    () => (rows === undefined ? undefined : searching ? rows.filter((row) => rowMatchesQuery(row, needle)) : rows),
    [rows, searching, needle],
  );
  const errorCount = rows?.filter(isRowError).length ?? 0;
  const scrollRef = useRef<HTMLDivElement | null>(null);
  const [copied, setCopied] = useState<null | { ok: boolean; count: number }>(null);

  // 自动滚底(现状 RunLogBody 原样):行集变化即贴底(终端惯例;展开瞬间
  // rows 未必到位,依赖数组带 rows 兜两拍;running 续播无条件贴底,Crawlab 同款)
  useEffect(() => {
    const el = scrollRef.current;
    if (el !== null) el.scrollTop = el.scrollHeight;
  }, [shownRows, run.rowKey]);

  /** 复制日志(Gantt copyAllLogs 同位,现状 copyLogs 原样):复制该 run 全部
   *  行(不受搜索过滤影响);无头/无焦点环境 clipboard 可能拒绝,失败如实回显 */
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
    <div className="flex h-full min-h-0 flex-col" data-testid="run-detail">
      {/* ═══ 元信息头(固定区,feed 2 级工具条解剖)═══ */}
      <div className="flex flex-wrap items-center gap-2 border-b px-5 py-2.5">
        {/* 返回钮(槽位第一;feed 返回钮同款解剖,词面随本屏物种) */}
        <Button
          variant="outline"
          size="sm"
          className="px-2 text-xs"
          data-testid="run-back"
          title="返回运行历史(Esc 同门)"
          onClick={onBack}
        >
          <ChevronLeft aria-hidden className="size-3.5" />
          运行历史
        </Button>
        {/* 身份簇:#id mono · 品类 · 徽标 · 状态芯片 */}
        <span className="shrink-0 font-mono text-xs text-muted-foreground">#{run.runId}</span>
        <span className="max-w-48 shrink-0 truncate text-xs font-medium text-foreground" title={run.category}>
          {run.category}
        </span>
        {run.dry ? (
          <Badge variant="outline" title="dry run(不落库)">
            试跑
          </Badge>
        ) : null}
        {run.history ? (
          <Badge
            variant="outline"
            data-testid={`run-history-badge-${domId}`}
            title="重启前会话的跑次(run.status 合流运行历史库)"
          >
            上一程
          </Badge>
        ) : null}
        <StatusChip badge={badge} testId={`run-status-chip-${domId}`} />
        {/* 事实簇(事实真源只报 run.status 行 + tail 到位后的行计数) */}
        <span
          data-testid={`run-detail-meta-${domId}`}
          className="flex min-w-0 flex-wrap items-center gap-x-2 gap-y-0.5 text-2xs text-muted-foreground"
        >
          <span
            className="shrink-0"
            title={startedAt ? formatRelative(startedAt) : undefined}
          >
            开始 <span className="font-mono">{formatAbsolute(startedAt)}</span>
          </span>
          {finishedAt ? (
            <span className="shrink-0">
              结束 <span className="font-mono">{formatAbsolute(finishedAt)}</span>
            </span>
          ) : null}
          <span className="shrink-0">
            耗时 <span className="font-mono">{run.durationText}</span>
          </span>
          <span className="shrink-0 font-mono">exit={run.exitCode ?? "—"}</span>
          {/* 来源标记如实报 logs.tail 实际查询号(历史行=会话对齐号,旧行=未对齐) */}
          <span className="min-w-0 truncate font-mono">logs.tail run_id={run.logRunId ?? "—"}</span>
          {rows !== undefined ? (
            <>
              <span className="shrink-0">{rows.length} 行</span>
              {errorCount > 0 ? (
                <span className="shrink-0 font-medium text-[#ff6b70]">{errorCount} 错误行</span>
              ) : null}
            </>
          ) : null}
        </span>
        {/* 动作簇(右缘):实时徽标 · 复制 · 重跑(feedback 与按钮同现状词面) */}
        <span className="ml-auto flex shrink-0 items-center gap-2.5">
          {running ? <Badge variant={live ? "ok" : "unknown"}>{live ? "实时跟踪中" : "未跟踪"}</Badge> : null}
          <button
            type="button"
            data-testid={`run-log-copy-${domId}`}
            onClick={copyLogs}
            disabled={rows === undefined || rows.length === 0}
            className="inline-flex shrink-0 items-center gap-1 rounded-sm text-2xs font-medium text-link transition-colors duration-(--duration-fast) hover:text-foreground disabled:cursor-not-allowed disabled:opacity-50"
          >
            {copied?.ok ? <Check aria-hidden className="size-3" /> : <Copy aria-hidden className="size-3" />}
            {copied === null ? "复制日志" : copied.ok ? `已复制 ${copied.count} 行` : "复制失败(剪贴板拒绝)"}
          </button>
          {rerun?.phase === "triggered" ? (
            <span
              data-testid={`run-rerun-ok-${domId}`}
              className="shrink-0 text-2xs font-medium text-ok"
              title={`新 run #${rerun.runId} 已启动,运行历史列表已刷新`}
            >
              已触发 #{rerun.runId}
            </span>
          ) : null}
          {rerun?.phase === "error" ? (
            <span
              data-testid={`run-rerun-err-${domId}`}
              className="max-w-44 shrink-0 truncate text-2xs text-destructive"
              title={rerun.message}
            >
              {rerun.message}
            </span>
          ) : null}
          {run.yaml !== null ? (
            <Button
              variant="ghost"
              size="icon"
              className="size-6 shrink-0 text-muted-foreground"
              data-testid={`run-rerun-${domId}`}
              aria-label={`重跑采集 #${run.runId}`}
              title={`重跑该 run(run.start 回放 ${run.yaml}${run.dry ? ",dry" : ""})`}
              disabled={rerun?.phase === "starting"}
              onClick={() => onRerun(run)}
            >
              {rerun?.phase === "starting" ? (
                <Loader2 aria-hidden className="size-3.5 animate-spin" />
              ) : (
                <RotateCcw aria-hidden className="size-3.5" />
              )}
            </Button>
          ) : null}
        </span>
      </div>

      {/* ═══ 失败原因区(固定区;渲染门槛在 synthesizeFailure,成功轮 null 不渲染)═══ */}
      {failure !== null ? <FailurePanel domId={domId} badge={badge} failure={failure} /> : null}

      {/* ═══ 日志体(主滚动区,内滚帽解除 → flex-1)═══ */}
      <div className="flex min-h-0 flex-1 flex-col">
        {/* 搜索工具行(迁自 L1 过滤条,design §2.3/§3.3:搜索对象是日志行,行只在
            L2 在场;输入即过滤 + 命中高亮三件套语义零改,只换挂载点) */}
        <div className="flex flex-wrap items-center gap-2 px-5 py-2">
          <div className="relative w-full max-w-sm min-w-48">
            <Search
              aria-hidden
              className="pointer-events-none absolute top-1/2 left-2.5 size-3.5 -translate-y-1/2 text-muted-foreground/70"
            />
            <Input
              type="search"
              value={query}
              onChange={(event) => onQueryChange(event.target.value)}
              onKeyDown={(event) => {
                // Esc 在输入框内 = 清词(框内守卫,feed L2 搜索同门
                // feed-screen.tsx:3534-3540);全局 Esc 链见编排层
                // (焦点守卫让位,两道互不抢)
                if (event.key === "Escape") {
                  onQueryChange("");
                }
              }}
              placeholder="搜索该轮日志(输入即过滤,命中高亮)"
              aria-label="搜索该轮日志"
              data-testid="log-search-input"
              className="pl-8 font-mono"
            />
          </div>
          {truncated ? <Badge variant="outline">缓冲截断</Badge> : null}
          {searching && shownRows !== undefined && rows !== undefined ? (
            <span data-testid={`run-log-hits-${domId}`} className="font-mono text-2xs text-muted-foreground">
              命中 {shownRows.length} / {rows.length} 行
            </span>
          ) : null}
        </div>
        {/* 全量日志行:等宽终端块,直接 flex 子项显式 shrink-0(塌缩律) */}
        <div
          ref={scrollRef}
          data-testid={`run-log-${domId}`}
          className="flex min-h-0 flex-1 flex-col gap-1 overflow-y-auto px-4 pb-3 pt-1 font-mono text-xs leading-relaxed"
        >
          {loadError !== null ? (
            <p className="shrink-0 text-dead">
              <span className="mr-1.5">●</span>日志加载失败({loadError})
            </p>
          ) : run.logRunId === null ? (
            /* 无会话号行:不拉取,如实降级——比拉一个必空的 run_id 再说
               「暂无日志」诚实。10-12-cron-run-log-alignment D5:文案去时间
               断言(NULL ≠ 早于落库,cron 新行也曾是 NULL;补号后此态只剩
               真遗留行) */
            <p className="shrink-0 text-muted-foreground">
              <span className="text-brand-from">▍</span> 该轮未记录日志会话号,无可回看的日志(旧 runs 行未记会话号)
            </p>
          ) : rows === undefined ? (
            <p className="shrink-0 text-muted-foreground">
              <span className="text-brand-from">▍</span> 正在拉取 logs.tail…
            </p>
          ) : searching && shownRows !== undefined && shownRows.length === 0 ? (
            <p className="shrink-0 text-muted-foreground">
              <span className="text-brand-from">▍</span> 无命中行(搜索词过滤掉了这轮采集的全部日志)
            </p>
          ) : rows.length === 0 ? (
            <p className="shrink-0 text-muted-foreground">
              <span className="text-brand-from">▍</span> 这轮采集暂无日志(环形缓冲只保留最近 4000 行)
            </p>
          ) : (
            shownRows?.map((row) => <LogRowView key={row.key} row={row} needle={needle} />)
          )}
        </div>
      </div>
    </div>
  );
}

/** 命中片段 <mark>:警示底 + 前景保持行色系(只标记不改语,WCAG 不降级;现状平移) */
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

/** 单条日志行(现状平移 + shrink-0 塌缩律):system 合成行 / stderr 结构化行
 *  两路;错误行 dead 高亮(bg-dead/10,P2 对比实算 4.67:1)、WARNING 级弱警示、
 *  INFO 不染 —— 判定函数 isRowError/isRowWarn 零改 */
function LogRowView({ row, needle }: { row: LogRow; needle: string }) {
  if (row.stream === "system") {
    return (
      <p data-testid="log-system-row" className="shrink-0 whitespace-pre-wrap break-words text-muted-foreground/80">
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
            "shrink-0 whitespace-pre-wrap break-words rounded-sm bg-dead/10 px-1 text-dead"
          : warn
            ? "shrink-0 whitespace-pre-wrap break-words px-1 text-warning/85" // WARNING 级 / 裸 stderr 诊断行弱警示
            : "shrink-0 whitespace-pre-wrap break-words px-1 text-foreground/90"
      }
    >
      <span className="mr-1.5 text-muted-foreground/60">·</span>
      <HighlightedText text={row.text} needle={needle} />
    </p>
  );
}
