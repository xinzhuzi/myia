import { Fragment, useMemo } from "react";
import type { RefObject } from "react";
import { Loader2, RefreshCw, RotateCcw, X } from "lucide-react";

import { EmptyState } from "@/components/empty-state";
import { PageHeader } from "@/components/layout/page-header";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Skeleton } from "@/components/ui/skeleton";

import { domIdOf, formatRelative, summarizeRun } from "./api";
import type { RerunState, RunFilterStatus, RunRowModel } from "./api";
import { runBadge, StatusChip, STATUS_FILTER_OPTIONS } from "./run-status-chip";

/**
 * L1 运行历史(10-12-logs-two-level-ui §2):每 run 一行直出,accordion 折叠
 * 退役(design §2.3 退役清单)。行解剖 = Kestra Executions.vue 表行延续
 * (定宽槽位列对齐 + 状态小芯片,10-04-ui-kestra-anchor 锚),升格摘要槽 =
 * 「本轮采集了什么」(summarizeRun 派生,数据真源只吃 run.status 行——
 * 1 级严禁逐行拉日志,logs.tail 惰性拉取归 L2)。
 * 行根仍是「按钮区 + 兄弟重跑钮」两节点(button 不可嵌套,现状纪律保留);
 * 点击进 L2 的语义 owner = 按钮区(testid run-row-{domId},去 aria-expanded)。
 * 塌缩律(67546cd 不回归):本组件的内滚容器 run-list 直接 flex 子项一律
 * 显式 shrink-0(行根/骨架/空态卡),子项无 overflow-hidden,双保险。
 */

export interface RunListViewProps {
  loading: boolean;
  /** 全量行模型(计数分母/空态判据) */
  allRows: RunRowModel[];
  /** 过滤后行模型(瀑布直出) */
  visibleRows: RunRowModel[];
  /** rowKey → started_at(相对时间槽;键=runRowKey 防两编号空间撞号互覆,
   *  历史行沿库可空,formatRelative 自兜「—」) */
  startedAtById: Map<string, string | null>;
  categories: string[];
  categoryFilter: string;
  statusFilter: RunFilterStatus | "all";
  onCategoryFilter: (value: string) => void;
  onStatusFilter: (value: RunFilterStatus | "all") => void;
  filtering: boolean;
  onResetFilters: () => void;
  refreshing: boolean;
  onRefresh: () => void;
  rerunByRun: Record<string, RerunState>;
  onRerun: (run: RunRowModel) => void;
  /** 点行进 L2(编排层 openRun:存 L1 滚动位 + 惰性 tail,design §4.1/§4.2) */
  onOpen: (run: RunRowModel) => void;
  /** run-list 内滚容器 ref(编排层持,openRun 时捕 scrollTop,design §4.2) */
  listRef: RefObject<HTMLDivElement | null>;
}

export function RunListView({
  loading,
  allRows,
  visibleRows,
  startedAtById,
  categories,
  categoryFilter,
  statusFilter,
  onCategoryFilter,
  onStatusFilter,
  filtering,
  onResetFilters,
  refreshing,
  onRefresh,
  rerunByRun,
  onRerun,
  onOpen,
  listRef,
}: RunListViewProps) {
  // run 状态分布(纯视图派生,现状零改语义:与 runBadge 同词表聚档)
  const distSegments = useMemo(() => {
    const dist = { running: 0, success: 0, partial: 0, failed: 0, other: 0 } as Record<string, number>;
    for (const run of visibleRows) {
      if (run.state === "running" || run.status === null) dist.running += 1;
      else if (run.status === "success") dist.success += 1;
      else if (run.status === "partial" || run.status === "config_error") dist.partial += 1;
      else if (run.status === "failed") dist.failed += 1;
      else dist.other += 1;
    }
    return [
      { key: "success", label: "成功", tone: "bg-ok", count: dist.success },
      { key: "running", label: "运行中", tone: "bg-primary", count: dist.running },
      { key: "partial", label: "部分/配置", tone: "bg-warning", count: dist.partial },
      { key: "failed", label: "失败", tone: "bg-dead", count: dist.failed },
      { key: "other", label: "其他", tone: "bg-unknown", count: dist.other },
    ].filter((segment) => segment.count > 0);
  }, [visibleRows]);

  return (
    /* 满高列表容器(Kestra app.scss section.full-container 同款:列表内滚、
     * 过滤条/节头常驻;骨架保留。根 = 编排层 flex 列的分支根,吃余高 flex-1
     * min-h-0——横幅在场时不再 100%+ 横幅高溢出) */
    <div className="flex min-h-0 flex-1 flex-col gap-4">
      <PageHeader
        title="采集日志"
        description="采集记录一行一轮(新→旧)· 行内摘要可读「本轮采集了什么」· 点行进详情看完整日志与失败原因"
        actions={
          <Button variant="outline" size="sm" onClick={onRefresh} disabled={loading}>
            <RefreshCw className={refreshing ? "size-3.5 animate-spin" : "size-3.5"} />
            刷新
          </Button>
        }
      />

      {/* 过滤条(品类/状态 select + 计数;日志搜索框已迁 L2——搜索对象是日志
          行,行只在 2 级在场,留 1 级 = 逐 run 拉尾违反数据真源边界,design §2.3) */}
      <div className="flex flex-wrap items-center gap-2 px-6" data-testid="logs-filter-bar">
        <Select value={categoryFilter} onValueChange={onCategoryFilter}>
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
        <Select value={statusFilter} onValueChange={(value) => onStatusFilter(value as RunFilterStatus | "all")}>
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
          <Button variant="ghost" className="gap-1 px-2 text-muted-foreground" onClick={onResetFilters}>
            <X aria-hidden className="size-3.5" />
            清除过滤
          </Button>
        ) : null}
        <span className="text-2xs text-muted-foreground" data-testid="logs-filter-count">
          {visibleRows.length} / {allRows.length} 轮
        </span>
      </div>

      <div className="flex min-h-0 flex-1 flex-col gap-3 px-6">
        {/* 节头 + run 状态分布条(纯视图派生,现状零改) */}
        <div className="flex flex-wrap items-center justify-between gap-2">
          <div className="flex items-center gap-2">
            <h2 className="text-base font-semibold text-foreground">运行历史</h2>
            <span className="text-2xs text-muted-foreground">
              {visibleRows.length} / {allRows.length} 轮 · 新→旧
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
              style={{ width: `${(segment.count / Math.max(visibleRows.length, 1)) * 100}%` }}
              title={`${segment.label} ${segment.count}`}
            />
          ))}
        </div>
        {/* run 摘要行瀑布(新→旧):列表区内滚(full-container),行间 gap-grid
            令牌。直接 flex 子项一律 shrink-0(塌缩律,10-11 实测缺它时 44px→6.5px
            黑条且 scrollHeight==clientHeight 永不出滚动条) */}
        <div
          ref={listRef}
          className="flex min-h-0 flex-1 flex-col gap-grid overflow-y-auto pb-block"
          data-testid="run-list"
        >
          {loading && allRows.length === 0 ? (
            <>
              <Skeleton className="h-12 w-full shrink-0 rounded-lg" />
              <Skeleton className="h-12 w-full shrink-0 rounded-lg" />
              <Skeleton className="h-12 w-full shrink-0 rounded-lg" />
            </>
          ) : allRows.length === 0 ? (
            <Card className="shrink-0">
              <CardContent>
                <EmptyState
                  compact
                  title="还没有采集记录"
                  description="从源管理触发一次采集后,采集记录将按新→旧出现在这里"
                />
              </CardContent>
            </Card>
          ) : visibleRows.length === 0 ? (
            <Card className="shrink-0">
              <CardContent>
                <EmptyState
                  compact
                  title="没有匹配的采集记录"
                  description="品类/状态过滤没有命中任何采集记录,放宽条件再试"
                />
                <div className="mt-3 flex justify-center">
                  <Button variant="outline" size="sm" onClick={onResetFilters}>
                    清除过滤
                  </Button>
                </div>
              </CardContent>
            </Card>
          ) : (
            visibleRows.map((run) => (
              <RunSummaryRow
                key={run.rowKey}
                run={run}
                startedAt={startedAtById.get(run.rowKey)}
                rerun={rerunByRun[run.rowKey]}
                onRerun={onRerun}
                onOpen={onOpen}
              />
            ))
          )}
        </div>
      </div>
    </div>
  );
}

/**
 * 摘要行(design §2.1 槽位表):#id mono → 品类(定宽槽)→ 徽标簇 →
 * 「采集了什么」摘要(弹性槽)→ 相对开始时间 → 耗时 mono → 状态芯片 ‖ 重跑钮。
 * 展开箭头退役(accordion 语义终结)、「N 错误行」槽退役(其真源是 logs.tail
 * 行,L1 不拉日志;失败信号由摘要错误段 + 状态芯片承担)、「N 条」独立槽并入
 * 摘要成果段(避免同屏读两遍)。
 */
function RunSummaryRow({
  run,
  startedAt,
  rerun,
  onRerun,
  onOpen,
}: {
  run: RunRowModel;
  startedAt: string | null | undefined;
  rerun: RerunState | undefined;
  onRerun: (run: RunRowModel) => void;
  onOpen: (run: RunRowModel) => void;
}) {
  const starting = rerun?.phase === "starting";
  const domId = domIdOf(run);
  const badge = runBadge(run.status, run.state);
  // 摘要合成声源 = wire 原始行(签名 LogsRunEntry;模型随身携带,design §2.2)
  const summary = summarizeRun(run.entry);
  const summaryText = summary.empty ?? summary.segments.map((segment) => segment.text).join(" · ");
  return (
    <div className="shrink-0 rounded-lg border border-border bg-card animate-fade-in">
      <div className="flex min-h-11 items-center gap-1 rounded-lg pr-2 transition-colors duration-(--duration-fast) hover:bg-accent/60">
        <button
          type="button"
          data-testid={`run-row-${domId}`}
          onClick={() => onOpen(run)}
          className="flex min-h-11 min-w-0 flex-1 items-center gap-2.5 rounded-lg px-3 py-2 text-left"
        >
          {/* KsId 档:mono 弱色,定宽槽让多行 id 列对齐 */}
          <span className="w-9 shrink-0 font-mono text-xs text-muted-foreground">#{run.runId}</span>
          {/* KsEntityLink 位:品类定宽槽(摘要槽接管弹性位;title 全文兜截断) */}
          <span className="w-40 shrink-0 truncate text-[13px] font-medium text-foreground" title={run.category}>
            {run.category}
          </span>
          {run.dry ? (
            <Badge variant="outline" title="dry run(不落库)">
              试跑
            </Badge>
          ) : null}
          {/* 「上一程」徽标:与试跑同 variant=outline 并排槽位(历史行 dry 恒
              false,两者不并存,现状纪律) */}
          {run.history ? (
            <Badge
              variant="outline"
              data-testid={`run-history-badge-${domId}`}
              title="重启前会话的跑次(run.status 合流运行历史库)"
            >
              上一程
            </Badge>
          ) : null}
          {/* 「采集了什么」摘要槽(AC1 断言锚):title 全文兜 CSS truncate */}
          <span
            data-testid={`run-summary-${domId}`}
            title={summaryText}
            className="min-w-0 flex-1 truncate text-2xs text-muted-foreground"
          >
            {summary.empty !== null
              ? summary.empty
              : summary.segments.map((segment, index) => (
                  <Fragment key={index}>
                    {index > 0 ? <span aria-hidden className="text-muted-foreground/50"> · </span> : null}
                    <span className={segment.tone === "dead" ? "text-[#ff6b70]" : undefined}>
                      {/* #ff6b70 而非 text-dead:行 hover 底 accent/60 上对比实算档(现状组头同款) */}
                      {segment.text}
                    </span>
                  </Fragment>
                ))}
          </span>
          {/* KsDateAgo inverted:相对开始时间,title 绝对时间(槽宽 80:两位数分钟
              「37 分钟前」在 68px 折两行,终审裁图实证,放宽一行收口) */}
          <span className="w-20 shrink-0 text-right tabular-nums" title={startedAt ?? undefined}>
            {formatRelative(startedAt)}
          </span>
          {/* Duration:mono 定宽右对齐 */}
          <span className="w-[56px] shrink-0 text-right font-mono">{run.durationText}</span>
          <StatusChip badge={badge} testId={`run-status-chip-${domId}`} />
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
        {/* 重跑钮只挂注册表行:历史行 yaml 无库源,run.start 无从回放 */}
        {run.yaml !== null ? (
          <Button
            variant="ghost"
            size="icon"
            className="size-6 shrink-0 text-muted-foreground"
            data-testid={`run-rerun-${domId}`}
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
        ) : null}
      </div>
    </div>
  );
}
