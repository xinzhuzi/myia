import { useCallback, useEffect, useRef, useState } from "react";
import {
  Activity,
  CircleCheck,
  CircleDot,
  CirclePlay,
  CircleStop,
  CircleX,
  Gauge,
  HeartPulse,
  Loader2,
  Play,
  RefreshCw,
  TrendingUp,
  TriangleAlert,
} from "lucide-react";

import { EmptyState } from "@/components/empty-state";
import { HintButton } from "@/components/label-hint";
import { PageHeader } from "@/components/layout/page-header";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Skeleton } from "@/components/ui/skeleton";
import { api, onSidecarEvent, SidecarRequestError } from "@/lib/api";
import type { Finding, SourceHealthState, UnlistenFn } from "@/lib/api";
import { cn } from "@/lib/utils";

import {
  buildCategoryCards,
  buildOverviewStats,
  buildSourceHealthCards,
  buildVerdict,
  cumulativeOutcomeSummary,
  fetchOutcomeWindow,
  fetchTrendWindow,
  formatDuration,
  formatRelativeTime,
  formatSuccessRate,
  loadDashboardData,
  OVERVIEW_WINDOW_DEFAULT,
  overviewTrendDays,
  runItemCount,
  runPushFailureText,
  successRateSeries,
  summarizeRuns,
  summarizeSourceHealth,
  TREND_WINDOW_DAYS,
  trendCounts,
  utcToday,
} from "./api";
import type {
  CategoryCardModel,
  CategoryTone,
  DashboardData,
  DashboardRun,
  DashboardVerdict,
  OverviewStats,
  OverviewWindow,
  RunOutcomeDay,
  RunSuccessSummary,
  SourceHealthCardModel,
  SourceHealthCounts,
  TrendDay,
  TrendWindowDays,
  VerdictTone,
} from "./api";
import { FeedbackStatsCard } from "./feedback-stats-card";
import { Sparkline } from "./sparkline";

/*
 * 10-04-ui-kestra-anchor(仪表盘运行区):结构借自 Apache-2.0
 * kestra/ui/src/components/executions/ExecutionRoot.vue +
 * ExecutionRootTopBar.vue(运行区头部「全部 run」全量出口),借结构改语义;
 * RunStatusChip/RecentRunRow 解剖对位 design-system KsExecutionStatus
 * (small 档)与 Executions.vue 表行,活跃行常驻运行态对位
 * ExecutionPending/ExecutionProgress。不抄:Tabs 切换族/写操作族(见
 * evidence/仪表盘运行区-mapping.md)。
 */

/** 品类 tone → 徽标(健康度四态语义沿用共享 Badge:ok/warning/destructive) */
const TONE_BADGE: Record<CategoryTone, { variant: "ok" | "warning" | "destructive"; label: string }> = {
  ok: { variant: "ok", label: "正常" },
  warning: { variant: "warning", label: "降级" },
  dead: { variant: "destructive", label: "异常" },
};

/**
 * 状态点(teardown-vercel-dashboard #3:8px 圆点+13px 标签,四色映射
 * Ready/Error/Building/Queued → ok/dead/warning/unknown;色走 D2 语义 token
 * bg-ok/warning/dead/unknown,与源管理 HealthBadge 同一色源)。
 */
const SOURCE_STATE: Record<SourceHealthState, { dot: string; label: string }> = {
  ok: { dot: "bg-ok", label: "正常" },
  degraded: { dot: "bg-warning", label: "退化" },
  dead: { dot: "bg-dead", label: "失效" },
  unknown: { dot: "bg-unknown", label: "未知" },
};

function StatusDot({ state, reason }: { state: SourceHealthState; reason?: string }) {
  const health = SOURCE_STATE[state];
  return (
    <span
      data-health={state}
      title={reason}
      className="inline-flex items-center gap-1.5 text-sm text-foreground"
    >
      <span aria-hidden className={cn("size-2 shrink-0 rounded-full", health.dot)} />
      {health.label}
    </span>
  );
}

/** run 状态 → 徽标(runs 表 status 语义;active = 当前会话进行中,C3)。
 *  10-04-ui-kestra-anchor:附描边圆图标(对位 Kestra KsExecutionStatus 的
 *  statusIcon),芯片解剖见 RunStatusChip */
function runStatusBadge(run: DashboardRun) {
  if (run.active) {
    return { variant: "default" as const, label: "运行中", icon: CirclePlay };
  }
  switch (run.status) {
    case "success":
      return { variant: "ok" as const, label: "成功", icon: CircleCheck };
    case "partial":
      return { variant: "warning" as const, label: "部分", icon: TriangleAlert };
    case "config_error":
      return { variant: "warning" as const, label: "配置", icon: TriangleAlert };
    case "failed":
      return { variant: "destructive" as const, label: "失败", icon: CircleX };
    case "cancelled":
      return { variant: "unknown" as const, label: "已取消", icon: CircleStop };
    case "running":
      // 表内 running 且无内存活跃 = sidecar 中断遗留的僵尸行(如实标注)
      return { variant: "warning" as const, label: "中断", icon: TriangleAlert };
    default:
      return { variant: "unknown" as const, label: run.status ?? "未知", icon: CircleDot };
  }
}

/** 状态芯片(Kestra KsExecutionStatus small 档:24px 高/12px 字/6px 圆角/
 *  状态色淡底 + 描边圆图标;与采集日志屏 StatusChip 同解剖,屏内私有复制) */
const RUN_CHIP_TONE: Record<string, string> = {
  default: "border-primary/25 bg-primary/15 text-primary",
  ok: "border-ok/30 bg-ok/15 text-ok",
  warning: "border-warning/30 bg-warning/15 text-warning",
  destructive: "border-destructive/30 bg-destructive/15 text-[#ff6b70]",
  unknown: "border-unknown/30 bg-unknown/10 text-unknown",
};
function RunStatusChip({
  badge,
  pulse = false,
}: {
  badge: { variant: "default" | "ok" | "warning" | "destructive" | "unknown"; label: string; icon: typeof CircleCheck };
  pulse?: boolean;
}) {
  const Icon = badge.icon;
  return (
    <span
      className={`inline-flex h-6 shrink-0 items-center gap-1 rounded-[6px] border px-2 text-xs font-medium tabular-nums ${RUN_CHIP_TONE[badge.variant]}`}
    >
      <Icon aria-hidden className={`size-3.5 ${pulse ? "animate-pulse" : ""}`} />
      {badge.label}
    </span>
  );
}

/** 「跑一次」状态机(G4,10-03-feed-ux;照抄 feed 空态 CTA 形状) */
type RunOnceState =
  | { phase: "idle" }
  | { phase: "starting" }
  | { phase: "collecting"; runId: number }
  | { phase: "done" }
  | { phase: "error"; message: string };

function CategoryCard({
  category,
  onRunFinished,
}: {
  category: CategoryCardModel;
  /** completed 后回调(仪表盘刷新 run 历史与品类状态) */
  onRunFinished: () => void;
}) {
  const tone = TONE_BADGE[category.tone];
  const [runOnce, setRunOnce] = useState<RunOnceState>({ phase: "idle" });

  const startRun = useCallback(async () => {
    setRunOnce({ phase: "starting" });
    try {
      const started = await api.runStart({ yaml: category.file });
      setRunOnce({ phase: "collecting", runId: started.run_id });
    } catch (err) {
      setRunOnce({
        phase: "error",
        message: err instanceof SidecarRequestError ? `${err.code}: ${err.message}` : String(err),
      });
    }
  }, [category.file]);

  // completed 事件 → done + 仪表盘刷新;订阅随 collecting 状态起止(同 feed CTA)
  useEffect(() => {
    if (runOnce.phase !== "collecting") return;
    let unlisten: UnlistenFn | null = null;
    let cancelled = false;
    void onSidecarEvent((event) => {
      if (event.type === "completed" && event.run_id === runOnce.runId) {
        setRunOnce({ phase: "done" });
        onRunFinished();
      }
    }).then((un) => {
      if (cancelled) un();
      else unlisten = un;
    });
    return () => {
      cancelled = true;
      unlisten?.();
    };
  }, [runOnce, onRunFinished]);

  const busy = runOnce.phase === "starting" || runOnce.phase === "collecting";
  return (
    <div
      data-testid={`category-${category.file}`}
      className="flex h-full items-center justify-between gap-2 rounded-md border border-border/60 bg-muted/40 px-3 py-2.5"
    >
      <div className="flex min-w-0 flex-col gap-0.5">
        <p className="truncate text-xs font-medium text-foreground">{category.name}</p>
        <p className="text-2xs text-muted-foreground">
          {category.sourceCount} 源
          {category.schedule ? ` · ${category.schedule}` : " · 手动"}
          {category.nextFireAt ? " · 有排程" : ""}
        </p>
        {runOnce.phase === "error" ? (
          <p className="text-2xs text-destructive" data-testid={`run-once-error-${category.file}`}>
            跑一次失败:{runOnce.message}
          </p>
        ) : null}
      </div>
      <div className="flex shrink-0 items-center gap-1">
        {!category.loaded ? <Badge variant="unknown">未载入</Badge> : null}
        <Badge variant={tone.variant}>{tone.label}</Badge>
        <Button
          variant="ghost"
          size="icon"
          className="size-6"
          aria-label={`跑一次:${category.name}`}
          title="手动触发该品类采集一次(run.start)"
          disabled={busy}
          onClick={() => void startRun()}
        >
          {runOnce.phase === "collecting" ? (
            <Loader2 className="size-3.5 animate-spin" />
          ) : (
            <Play className="size-3.5" />
          )}
        </Button>
      </div>
    </div>
  );
}

/** 近期 run 行,解剖对位 Kestra Executions.vue 表行(与采集日志屏组头同语言:
 *  #id mono · 品类 · 相对开始时间(KsDateAgo inverted)· 耗时 mono · 状态芯片);
 *  活跃行 = ExecutionPending/Progress 同义的常驻运行态:主色左缘 + 图标呼吸 +
 *  「日志」直采链接(纯导航;HashRouter 下 a#hash 与 Link 等价,免 Router 上下文) */
function RecentRunRow({ run }: { run: DashboardRun }) {
  const badge = runStatusBadge(run);
  const itemCount = runItemCount(run);
  const pushFailureText = runPushFailureText(run);
  return (
    <div
      data-testid={`recent-run-${run.runId}`}
      className={`flex items-center gap-2 border-b border-border/40 py-1.5 pl-2 last:border-b-0 ${
        run.active ? "border-l-2 border-l-primary bg-primary/5" : ""
      }`}
    >
      <span className="w-8 shrink-0 font-mono text-2xs text-muted-foreground">#{run.runId}</span>
      <span className="min-w-0 flex-1 truncate text-[13px] text-foreground">{run.category}</span>
      {run.dry ? (
        <Badge variant="outline" title="dry run(不落库)">
          试跑
        </Badge>
      ) : null}
      {/* 推送失败明细(凭据指引到主人眼前):错误原文单行截断,title 悬停全文;
          保持在 dry 试跑徽章之后(行内首个 Badge 的既有断言锚定 dry title) */}
      {pushFailureText !== null ? (
        <Badge variant="destructive" title={pushFailureText} className="max-w-56 truncate font-normal">
          {pushFailureText}
        </Badge>
      ) : null}
      <span className="flex shrink-0 items-center gap-3 text-2xs text-muted-foreground">
        {itemCount !== null ? (
          <span className="w-11 text-right tabular-nums">{itemCount} 条</span>
        ) : (
          <span className="w-11" aria-hidden />
        )}
        <span className="w-[68px] text-right tabular-nums" title={run.startedAt ?? undefined}>
          {formatRelativeTime(run.startedAt)}
        </span>
        <span className="w-14 text-right font-mono">{formatDuration(run.durationMs)}</span>
        <RunStatusChip badge={badge} pulse={run.active} />
        {run.active ? (
          <a
            href="#/logs"
            className="shrink-0 rounded-sm text-2xs font-medium text-link transition-colors duration-(--duration-fast) hover:text-foreground"
            title="到采集日志屏跟踪该 run 实时输出"
          >
            日志 →
          </a>
        ) : null}
      </span>
    </div>
  );
}

/** 常见 sidecar 错误码的人话(主人 2026-10-04 目验判例:raw code 不是给人看的)。 */
const SIDECAR_ERROR_HINTS: Record<string, string> = {
  pyenv_not_ready: "Python 运行环境未就绪——配置完成后数据即恢复(顶部横幅可一键前往设置)",
  internal_error: "核心内部错误——重试通常可恢复,持续出现请重启应用",
  sidecar_timeout: "核心响应超时——稍候重试",
  method_not_found: "核心版本过旧缺此方法——请更新应用",
  store_schema: "数据库版本不兼容——应用与数据需同版升级",
  transport_error: "与核心的连接异常——重试或重启应用",
};

function humanizeSidecarError(code: string, message: string): string {
  return SIDECAR_ERROR_HINTS[code] ?? message;
}

const SECTION_LABELS: Record<"doctor" | "runs" | "registry", string> = {
  doctor: "诊断/源健康度",
  runs: "历史采集",
  registry: "进行中采集",
};

// ---------------------------------------------------------------------------
// D2/D3(10-05-dashboard-glance):状态句行 + 告警清单——零新样式家族,
// 复用 StatusDot「状态点+词」解剖与健康度四色 token;verdict 行是常驻内容
// 不是 toast/横幅(主人弹窗判例:屏顶横幅慎用)。
// ---------------------------------------------------------------------------

/** verdict tone → 状态点色(健康度四色 token 同源;状态不只靠色,headline 文字达意) */
const VERDICT_TONE_DOT: Record<VerdictTone, string> = {
  ok: "bg-ok",
  warning: "bg-warning",
  dead: "bg-dead",
  unknown: "bg-unknown",
};

/**
 * 状态句行(D2):屏 root 首块(无头范式,PageHeader=null 不复活)——
 * StatusDot 家族「状态点+词」+ headline(text-base medium)+ facts
 * (text-xs muted,· 分隔);dead/warning 态整行可点跳源管理(与告警清单
 * 同目的地),ok/unknown 纯文本。role=status + aria-label 汇总句。
 */
function VerdictRow({ verdict }: { verdict: DashboardVerdict }) {
  const summary = [verdict.headline, ...verdict.facts].join(" · ");
  const clickable = verdict.tone === "dead" || verdict.tone === "warning";
  const content = (
    <>
      <span
        aria-hidden
        className={cn("size-2 shrink-0 self-center rounded-full", VERDICT_TONE_DOT[verdict.tone])}
      />
      <span className="text-base font-medium text-foreground">{verdict.headline}</span>
      {verdict.facts.length > 0 ? (
        <span className="text-xs text-muted-foreground">{verdict.facts.join(" · ")}</span>
      ) : null}
    </>
  );
  const rowClass = "flex flex-wrap items-baseline gap-x-2 gap-y-0.5 px-1 py-1";
  if (clickable) {
    return (
      <div className="px-6">
        <a
          href="#/sources"
          data-testid="dashboard-verdict"
          role="status"
          aria-label={summary}
          title="查看源管理"
          className={rowClass}
        >
          {content}
        </a>
      </div>
    );
  }
  return (
    <div className="px-6">
      <div data-testid="dashboard-verdict" role="status" aria-label={summary} className={rowClass}>
        {content}
      </div>
    </div>
  );
}

/** 告警清单行视图模型(坏源行 + 品类级 finding 补位行 + 全局 finding 行的统一形状) */
interface AlertRowModel {
  key: string;
  /** 行首状态点色(健康度四色 token 同源) */
  dot: string;
  /** 状态词(不只靠色:失效/退化/未知;finding 行 = 异常/提醒) */
  stateLabel: string;
  /** 主名:源名 / 品类名 / 全局 finding 主体名(凭据、数据库等) */
  primary: string;
  /** 次段:源行 = 所属品类名;品类行/全局行无 */
  secondary: string | null;
  /** 原因明细(reason/finding.message 原文直用——cli 已人话,零映射;行内截断) */
  detail: string;
  /** 相对时间右置(源行);finding 行无时刻 = null */
  time: string | null;
}

/**
 * 全局 finding 主体名(scope 人话映射):cli 实况非 plugin scope = credentials /
 * store / gates / feedback / components(cli.py:2957/3190/3389/3037/3104);
 * 映射只做已知主词,其余 scope 原文如实(补批三例定)。复审 low 修:db 分支
 * 系死码(cli 无 db scope),真实数据库相关 = store,改映射+删死分支。
 */
function findingScopeLabel(scope: string): string {
  if (scope === "credentials") return "凭据";
  if (scope === "store") return "数据库";
  return scope;
}

/**
 * 告警清单行装配(D3 + 补批一/三):坏源行优先(sourceCards 已按坏者优先
 * 排序);品类级 findings(scope 恰为 `plugin:<file>`,非 `/source:` 后缀)
 * 补位;全局 findings(非 plugin:* scope,如 credentials/store)也进行——
 * 清单漏全局行会出现「格>0 清单空」的两面不齐。行口径 = error+warning
 * (复审必改:与告警格计数/verdict 升态三面同源;info 级 = cli 明示的
 * 正常态注记,gate_disabled/analysis_lane_disabled/third_party_trace 等
 * 默认装机即有,不入告警也不进行)。触发 = 告警(error+warning)>0 或
 * 坏源(state≠ok)>0——两数据面不重合(findings 可只打品类级、退化可无
 * finding),双向都要兜;行数不足时多类拼合计。key 带序号去重:同品类/
 * 同 scope 可载入多条同 code finding(补批一),仅 file+code 会撞 React key。
 */
function buildAlertRows(
  sourceCards: SourceHealthCardModel[],
  categories: CategoryCardModel[],
  findings: Finding[],
): AlertRowModel[] {
  const rows: AlertRowModel[] = [];
  for (const card of sourceCards) {
    if (card.state === "ok") continue;
    rows.push({
      key: `source-${card.key}`,
      dot: SOURCE_STATE[card.state].dot,
      stateLabel: SOURCE_STATE[card.state].label,
      primary: card.name,
      secondary: card.pluginName,
      detail: card.reason,
      time: formatRelativeTime(card.lastObservedAt),
    });
  }
  for (const category of categories) {
    let seq = 0; // 同品类同 code 可多条:序号保 key 唯一
    for (const finding of findings) {
      if (finding.scope !== `plugin:${category.file}`) continue;
      if (finding.severity !== "error" && finding.severity !== "warning") continue; // info 不入清单
      seq += 1;
      rows.push({
        key: `category-${category.file}-${finding.code}-${seq}`,
        dot: finding.severity === "error" ? "bg-dead" : "bg-warning",
        stateLabel: finding.severity === "error" ? "异常" : "提醒",
        primary: category.name,
        secondary: null,
        detail: finding.message,
        time: null,
      });
    }
  }
  let scopeSeq = 0;
  for (const finding of findings) {
    // plugin:* 前缀 = 品类级(上循环)/ 源级(不入清单)两类,均不进全局行
    if (finding.scope.startsWith("plugin:")) continue;
    if (finding.severity !== "error" && finding.severity !== "warning") continue;
    scopeSeq += 1;
    rows.push({
      key: `scope-${finding.scope}-${finding.code}-${scopeSeq}`,
      dot: finding.severity === "error" ? "bg-dead" : "bg-warning",
      stateLabel: finding.severity === "error" ? "异常" : "提醒",
      primary: findingScopeLabel(finding.scope),
      secondary: null,
      detail: finding.message,
      time: null,
    });
  }
  return rows;
}

/**
 * 告警清单(D3):概览节内四格之下的异常清单,前三条封顶(grill Q4),行点
 * 跳源管理;溢出口 N = 清单外剩余异常数(坏源 + 品类级 findings,如实计);
 * 行集为空 = 零占位。容器语言复用 CategoryCard 的 rounded-md border 弱底家族。
 */
function AlertList({ rows }: { rows: AlertRowModel[] }) {
  if (rows.length === 0) return null;
  const shown = rows.slice(0, 3);
  const overflow = rows.length - shown.length;
  return (
    <div
      data-testid="dashboard-alert-list"
      className="flex flex-col rounded-md border border-border/60 bg-muted/40 px-3"
    >
      {shown.map((row) => (
        <a
          key={row.key}
          href="#/sources"
          data-testid={`alert-row-${row.key}`}
          title={row.detail}
          className="flex min-w-0 items-center gap-2 border-b border-border/40 py-1.5 last:border-b-0"
        >
          <span className="inline-flex shrink-0 items-center gap-1.5 text-sm text-foreground">
            <span aria-hidden className={cn("size-2 shrink-0 rounded-full", row.dot)} />
            {row.stateLabel}
          </span>
          <span className="shrink-0 text-sm font-medium text-foreground">{row.primary}</span>
          {row.secondary !== null ? (
            <span className="shrink-0 text-xs text-muted-foreground">{row.secondary}</span>
          ) : null}
          <span className="min-w-0 flex-1 truncate text-xs text-muted-foreground">— {row.detail}</span>
          {row.time !== null ? (
            <span className="shrink-0 font-mono text-xs text-muted-foreground">{row.time}</span>
          ) : null}
        </a>
      ))}
      {overflow > 0 ? (
        <a
          href="#/sources"
          data-testid="dashboard-alert-overflow"
          className="border-t border-border/40 py-1.5 text-xs font-medium text-link transition-colors duration-(--duration-fast) hover:text-foreground"
        >
          还有 {overflow} 个异常 · 查看全部 →
        </a>
      ) : null}
    </div>
  );
}

/**
 * 概览格卡(终审修整:单卡内 divide-x 四格 → 四张独立等宽等高 Card;
 * VL 指认「四卡紧密堆叠、卡高不一/宽度不一、右侧告警卡错位」——
 * grid gap-grid + 基调层 [data-slot=card] height:100% 天然等高等宽)。
 * teardown-vercel-dashboard #2 血统保留:小标签 = 大写+弱色,大数字 = tnum
 * 全局已开;value=null 显 — 不虚构。note = 弱注记(口径说明)。
 * R3(10-05-dashboard-glance):口径型 note 收进 ⓘ 悬停(HintButton,
 * ui/tooltip 基件,键盘 focus 可达)——扫读面只剩标签+大数字;错误/降级型
 * note(noteKind="alert")保留明文,错误不藏 hover。
 */
function StatCell({
  label,
  value,
  note,
  noteKind = "meta",
  destructive = false,
  testid,
}: {
  label: string;
  value: number | string | null;
  note: string;
  /** note 性质:meta = 口径注记(ⓘ 悬停);alert = 错误/降级注记(明文) */
  noteKind?: "meta" | "alert";
  destructive?: boolean;
  testid: string;
}) {
  return (
    <Card data-testid={testid} className="gap-2">
      <div className="flex h-full min-h-24 flex-col gap-1.5 px-card py-4">
        <p className="text-2xs font-medium uppercase tracking-wider text-muted-foreground">{label}</p>
        <p
          className={cn(
            "text-2xl font-semibold tabular-nums",
            destructive ? "text-destructive" : "text-foreground",
          )}
        >
          {value === null ? "—" : value}
        </p>
        {noteKind === "alert" ? (
          <p className="mt-auto text-2xs leading-snug text-muted-foreground">{note}</p>
        ) : (
          <div className="mt-auto">
            <HintButton name={label} tip={note} />
          </div>
        )}
      </div>
    </Card>
  );
}

/**
 * 趋势图包装(终审修整,VL 指认「纯色折线无数据点无坐标轴刻度」):
 * Sparkline 画布参数同源(viewBox 260×48 / pad 3,preserveAspectRatio=none
 * 线性拉伸)→ 归一坐标按容器百分比叠加层即可与折线逐点贴合:
 * ① y 轴刻度列(顶/中/底三档,HTML 免 SVG 拉伸变形)+ 图域上下留白;
 * ② 网格层:三条水平细线(0%/50%/100% 刻度线);
 * ③ 数据点层:每值一枚 6px 圆点(card 色描环,与线交叠清晰);
 * ④ 轴刻度行由调用侧渲染(x 轴起/中/止 + 峰值单位标注)。
 * sparkline.tsx 零改动(可选层全在屏内)。
 */
function TrendChart({
  values,
  max,
  pulse = false,
  area = true,
  yLabels,
  className,
  "aria-label": ariaLabel,
  "data-testid": dataTestId,
}: {
  values: number[];
  max?: number;
  pulse?: boolean;
  area?: boolean;
  /** y 轴三档刻度文案(顶/中/底;缺省不渲染刻度列) */
  yLabels?: [string, string, string];
  className?: string;
  "aria-label": string;
  "data-testid"?: string;
}) {
  const W = 260;
  const H = 48;
  const PAD = 3;
  const domainMax = max !== undefined && max > 0 ? max : Math.max(...values, 0);
  const points =
    values.length === 0
      ? []
      : values.map((value, index) => ({
          x: values.length === 1 ? W / 2 : PAD + ((W - PAD * 2) * index) / (values.length - 1),
          y: domainMax === 0 ? H / 2 : PAD + (H - PAD * 2) * (1 - value / domainMax),
        }));
  return (
    <div className={cn("flex items-stretch gap-2 py-1.5", className)}>
      {/* y 轴刻度列:与网格三线同高对齐(justify-between 同步 0%/50%/100%) */}
      {yLabels ? (
        <div
          aria-hidden
          className="flex w-9 shrink-0 flex-col justify-between py-px text-right font-mono text-2xs leading-none text-muted-foreground/80"
        >
          <span>{yLabels[0]}</span>
          <span>{yLabels[1]}</span>
          <span>{yLabels[2]}</span>
        </div>
      ) : null}
      <div className="relative min-w-0 flex-1">
        {/* 网格层:0%/50%/100% 三条刻度线(border 族,弱于折线) */}
        <div aria-hidden className="pointer-events-none absolute inset-0 flex flex-col justify-between">
          <span className="h-px w-full bg-border/60" />
          <span className="h-px w-full bg-border/40" />
          <span className="h-px w-full bg-border/60" />
        </div>
        <Sparkline
          values={values}
          max={max}
          pulse={pulse}
          area={area}
          className="relative z-10"
          aria-label={ariaLabel}
          data-testid={dataTestId}
        />
        {/* 数据点层:与折线逐点贴合(同参归一 → 百分比定位) */}
        <div aria-hidden className="pointer-events-none absolute inset-0 z-20">
          {points.map((point, index) => (
            <span
              key={index}
              className="absolute size-1.5 -translate-x-1/2 -translate-y-1/2 rounded-full bg-primary ring-2 ring-card"
              style={{ left: `${(point.x / W) * 100}%`, top: `${(point.y / H) * 100}%` }}
            />
          ))}
        </div>
      </div>
    </div>
  );
}

/**
 * 趋势分区错误条(终审修整,VL 指认「method_not_found 错误信息未有效视觉
 * 隔离」):行内 <p> 升级为独立警示块——图标 + 左侧文案 + 等宽错误码胶囊,
 * 与图表以垂直间距分明隔离(role=alert 可达性同步升格)。
 */
function TrendErrorAlert({
  title,
  code,
  message,
  testid,
}: {
  title: string;
  code: string;
  message: string;
  testid: string;
}) {
  return (
    <div
      role="alert"
      data-testid={testid}
      className="flex items-start gap-2.5 rounded-md border border-destructive/30 bg-destructive/10 px-3 py-2.5"
    >
      <TriangleAlert aria-hidden className="mt-0.5 size-3.5 shrink-0 text-destructive" />
      <p className="min-w-0 flex-1 text-xs text-destructive">
        <span className="font-medium">{title}</span>
        <span className="ml-1">{humanizeSidecarError(code, message)}</span>
        <code className="ml-1.5 rounded-sm border border-destructive/25 bg-destructive/15 px-1 py-px font-mono text-2xs">
          [{code}]
        </code>
      </p>
    </div>
  );
}

/**
 * 源健康卡(teardown-vercel-dashboard #4:名称 14 medium + muted 次行 + 相对
 * 时间 muted 右置;状态点居首行左 = Vercel 项目卡「状态点+词 → 名称 → 次行
 * → 相对时间」层级)。
 */
function SourceCard({ card }: { card: SourceHealthCardModel }) {
  // R2 刀2:走 Card 槽位(基调层等高/统一内边距;旧 raw div 不吃等高,列高不一)
  return (
    <Card data-testid={`source-card-${card.key}`} className="gap-2">
      <div className="flex items-start justify-between gap-2 px-card">
        <StatusDot state={card.state} reason={card.reason} />
        <span className="font-mono text-xs text-muted-foreground">
          {formatRelativeTime(card.lastObservedAt)}
        </span>
      </div>
      <div className="flex flex-col gap-1 px-card">
        <p className="truncate text-base font-medium text-foreground" title={`${card.name} · ${card.engine}`}>
          {card.name}
        </p>
        <p className="truncate text-xs text-muted-foreground">
          {card.pluginName}
          {card.latestItemCount !== null ? ` · 最近 ${card.latestItemCount} 条` : ""}
        </p>
      </div>
    </Card>
  );
}

/** 源健康度卡栅格类(坏源栅格与 ok 折叠组栅格同款;补批五拆两栅格共用) */
const SOURCE_GRID_CLASS = "grid grid-cols-1 gap-grid sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4";

/**
 * 仪表盘(结构性重做,10-03-ui-deep-imitation D4;对标 teardown-vercel-dashboard):
 * 概览条(今日采集/活跃源/推送成功/告警;头 Select = 全屏唯一时间窗,补批四)
 * → 采集量趋势(自绘 SVG sparkline,D5 决议⑥零依赖;窗口随概览 Select;活跃
 * run 时末点呼吸)+ 成功率第二序列 → 源健康度卡网格(StatusDot 四色 + 相对
 * 时间,gap-6;补批五:正常源折叠组)→ 品类状态 → 最近采集成功率 + 反馈统计。
 * 数据 = doctor + runs.list + run.status + store.trend(见 ./api;C3:重启 .app
 * 后历史 run 仍可达)。加载/错误/空态三态齐备;趋势独立降级不拖垮整屏。
 */
export function DashboardScreen() {
  const [data, setData] = useState<DashboardData | null>(null);
  const [error, setError] = useState<SidecarRequestError | null>(null);
  const [loading, setLoading] = useState(true);
  const [trend, setTrend] = useState<TrendDay[] | null>(null);
  const [trendError, setTrendError] = useState<SidecarRequestError | null>(null);
  const [outcomes, setOutcomes] = useState<RunOutcomeDay[] | null>(null);
  const [outcomeError, setOutcomeError] = useState<SidecarRequestError | null>(null);
  const [trendLoading, setTrendLoading] = useState(true);
  // 统一时间窗(补批四,联动合一):概览头 Select = 全屏唯一时间窗,驱动概览
  // 四格 + 采集量趋势 + 成功率两折线(趋势卡自有 Select 已删);今日档 = 1 天
  // 趋势窗(单点,sparkline 单值居中已有处理,如实画)
  const [overviewWindow, setOverviewWindow] = useState<OverviewWindow>(OVERVIEW_WINDOW_DEFAULT);
  // 源健康度折叠正常源(补批五):坏源照旧铺开,ok 源进折叠组默认收起
  const [okSourcesExpanded, setOkSourcesExpanded] = useState(false);

  const refresh = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      setData(await loadDashboardData());
    } catch (err) {
      setError(
        err instanceof SidecarRequestError
          ? err
          : new SidecarRequestError({ code: "transport_error", path: "$", message: String(err) }),
      );
    } finally {
      setLoading(false);
    }
  }, []);

  const trendSeq = useRef(0);
  /**
   * 双趋势同窗并发拉取(统一时间窗后单窗口单拉数):采集量(store.trend)与
   * 成功率(runs.trend)allSettled 分流 —— 一条失败另一条照画,各自错误各自
   * 降级(fbbaaa7 分区降级判例,勿用会一败俱败的 Promise.all);概览采集格
   * 同吃 trend(趋势卡与概览四格共用一窗数据,不再另拉一份)。迟响应护栏
   * (复审 low):序号过期的旧窗慢回整笔丢弃,不用旧窗和冒充新窗。
   */
  const refreshTrend = useCallback(async (days: number) => {
    const seq = ++trendSeq.current;
    setTrendLoading(true);
    setTrendError(null);
    setOutcomeError(null);
    const toSidecarError = (err: unknown): SidecarRequestError =>
      err instanceof SidecarRequestError
        ? err
        : new SidecarRequestError({ code: "transport_error", path: "$", message: String(err) });
    const [trendR, outcomeR] = await Promise.allSettled([
      fetchTrendWindow(days),
      fetchOutcomeWindow(days),
    ]);
    if (seq !== trendSeq.current) return; // 旧窗迟回:新窗已在途/已落,整笔丢弃
    if (trendR.status === "fulfilled") setTrend(trendR.value);
    else setTrendError(toSidecarError(trendR.reason));
    if (outcomeR.status === "fulfilled") setOutcomes(outcomeR.value);
    else setOutcomeError(toSidecarError(outcomeR.reason));
    setTrendLoading(false);
  }, []);

  useEffect(() => {
    void refresh();
  }, [refresh]);

  // 统一时间窗:概览窗直接驱动两折线(今日档 = 1 天窗,overviewTrendDays 换算)
  useEffect(() => {
    void refreshTrend(overviewTrendDays(overviewWindow));
  }, [refreshTrend, overviewWindow]);

  const healthCounts: SourceHealthCounts | null = data?.doctor ? summarizeSourceHealth(data.doctor) : null;
  const runSummary: RunSuccessSummary | null = data ? summarizeRuns(data.runs) : null;
  const categories: CategoryCardModel[] = data?.doctor ? buildCategoryCards(data.doctor) : [];
  const sourceCards: SourceHealthCardModel[] = data?.doctor ? buildSourceHealthCards(data.doctor, data.runs) : [];
  // 统一时间窗:概览四格与趋势卡同吃一份 trend(单窗口单拉数)
  const overview: OverviewStats | null = data
    ? buildOverviewStats(data.doctor, data.runs, trend, utcToday(), overviewWindow)
    : null;
  /** 统一窗口人话前缀(可见文案与 aria 同词):今日 / 近 N 天 */
  const windowLabel = overviewWindow === "today" ? "今日" : `近 ${overviewWindow} 天`;

  const counts = trend ? trendCounts(trend) : [];
  const trendTotal = counts.reduce((sum, count) => sum + count, 0);
  const trendPeak = counts.reduce((max, count) => Math.max(max, count), 0);
  const collecting = runSummary !== null && runSummary.running > 0;
  const rateSeries = outcomes !== null ? successRateSeries(outcomes) : [];
  const outcomeSummary = outcomes !== null ? cumulativeOutcomeSummary(outcomes) : null;

  // D1/D3(10-05-dashboard-glance):状态句 + 告警清单装配,零新拉数。
  // doctorFailed = doctor 分区失败或整屏 error(整屏 error 且 data 仍在时
  // verdict 显「数据不全」级;data 整体不可达时 buildVerdict 返回 null 不渲染)
  const doctorFailed = error !== null || (data !== null && data.doctor === null);
  const verdict = buildVerdict({ overview, health: healthCounts, categories, runSummary, doctorFailed });
  const alertRows = buildAlertRows(sourceCards, categories, data?.doctor?.findings ?? []);
  const deadCategoryCount = categories.filter((category) => category.tone === "dead").length;
  const warningCategoryCount = categories.filter((category) => category.tone === "warning").length;
  // 补批五:坏源(state≠ok)照旧铺开,ok 源收进折叠组
  const badSourceCards = sourceCards.filter((card) => card.state !== "ok");
  const okSourceCards = sourceCards.filter((card) => card.state === "ok");

  return (
    <div data-testid="dashboard-screen-root" className="flex flex-col gap-block pb-6">
      <PageHeader title="仪表盘" description="概览条 / 采集量趋势 / 源健康度 / 品类与最近采集" />

      {/* D2 状态句先行:屏首常驻内容行(无头范式首块)——一句话回答
          「系统还好吗 / 今天有什么新东西 / 有没有要我处理的」 */}
      {verdict !== null ? <VerdictRow verdict={verdict} /> : null}

      {error ? (
        <div className="px-6">
          <Card data-testid="dashboard-error">
            <CardContent className="pt-1">
              <p className="text-sm font-medium text-destructive">仪表盘数据不可用</p>
              <p className="mt-1 text-xs text-muted-foreground">
                {humanizeSidecarError(error.code, error.message)}
                <span className="ml-1 font-mono">[{error.code}]</span>
                ——点概览条右上「刷新数据」重试
              </p>
            </CardContent>
          </Card>
        </div>
      ) : data !== null && data.sectionErrors.length > 0 ? (
        <div className="px-6">
          <Card data-testid="dashboard-section-errors">
            <CardContent className="pt-1">
              <p className="text-sm font-medium text-warning">部分数据不可用,已降级显示其余分区</p>
              {data.sectionErrors.map((sectionError) => (
                <p key={sectionError.section} className="mt-1 text-xs text-muted-foreground">
                  {SECTION_LABELS[sectionError.section]}:{humanizeSidecarError(sectionError.error.code, sectionError.error.message)}
                  <span className="ml-1 font-mono">[{sectionError.error.code}]</span>
                </p>
              ))}
              <p className="mt-1 text-xs text-muted-foreground">点概览条右上「刷新数据」重试失败分区。</p>
            </CardContent>
          </Card>
        </div>
      ) : null}

      {/* 概览条(D4;teardown #2 血统:大写小标签 + 大数字 tnum)。
          终审修整:单卡 divide-x 四格 → 节头 + 四张独立等宽等高卡(VL 指认
          「四卡紧密堆叠/卡高不一/告警卡错位」);节头与源健康度/品类状态
          同款家族(图标+标题+右侧窗口 Select)。
          统一时间窗(补批四):此 Select = 全屏唯一时间窗(今日(UTC)/7/14/30
          天),同步驱动概览四格与下方两折线;活跃源/告警 = doctor 点快照
          不随窗,窗口档注记口径 */}
      <section
        data-testid="dashboard-overview"
        aria-label={overviewWindow === "today" ? "今日概览" : `近 ${overviewWindow} 天概览`}
        className="flex flex-col gap-4 px-6"
      >
        <div className="flex flex-wrap items-center justify-between gap-2">
          <div className="flex items-center gap-2">
            <Gauge className="size-3.5 text-muted-foreground" aria-hidden />
            <h2 className="text-base font-semibold text-foreground">
              {overviewWindow === "today" ? "今日概览(UTC)" : `近 ${overviewWindow} 天概览(UTC)`}
            </h2>
          </div>
          <div className="flex items-center gap-2">
            <Select
              value={overviewWindow === "today" ? "today" : String(overviewWindow)}
              onValueChange={(value) => {
                const next: OverviewWindow =
                  value === "today" ? "today" : (Number(value) as TrendWindowDays);
                if (next === overviewWindow) return;
                // 统一时间窗:切窗即弃旧窗趋势数据(不用旧窗和冒充新窗),
                // effect 按新窗重查补新;概览四格与两折线同步换窗
                setTrend(null);
                setOutcomes(null);
                setOverviewWindow(next);
              }}
            >
              <SelectTrigger size="sm" className="w-28" aria-label="概览时间范围">
                <SelectValue />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="today">今日(UTC)</SelectItem>
                {TREND_WINDOW_DAYS.map((option) => (
                  <SelectItem key={option} value={String(option)}>
                    {option} 天
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
            {/* 刷新钮(10-05 二迁:独立刷新行 → 概览卡头右上角,不占独立行;
                KsIconButton 同解剖 28px ghost 图标钮,sources-table 判例;
                onClick 沿既有刷新逻辑 refresh + refreshTrend(统一窗后趋势
                单笔重查,概览不再另拉),loading 期 RefreshCw 原地自转
                (updater-card 同款)) */}
            <Button
              variant="ghost"
              size="icon"
              className="size-7"
              aria-label="刷新数据"
              title="重新拉取仪表盘数据(doctor / runs / 趋势)"
              disabled={loading}
              onClick={() => {
                void refresh();
                void refreshTrend(overviewTrendDays(overviewWindow));
              }}
            >
              <RefreshCw className={loading ? "size-3.5 animate-spin" : "size-3.5"} />
            </Button>
          </div>
        </div>
        <div className="grid grid-cols-2 gap-4 md:grid-cols-4">
          {loading && overview === null ? (
            [0, 1, 2, 3].map((index) => <Skeleton key={index} className="h-28 w-full rounded-lg" />)
          ) : overview === null ? null : (
                <>
                  <StatCell
                    testid="stat-window-items"
                    label={overviewWindow === "today" ? "今日采集" : `近 ${overviewWindow} 天采集`}
                    value={overview.windowItems}
                    note={
                      trendError !== null
                        ? trendError.code === "pyenv_not_ready"
                          ? "数据待 Python 环境配置 · 如实显 —"
                          : `趋势不可达(${trendError.code})· 如实显 —`
                        : overviewWindow === "today"
                          ? "UTC 日口径 · items 入库"
                          : `UTC 逐日 ${overviewWindow} 天求和 · items 入库`
                    }
                    noteKind={trendError !== null ? "alert" : "meta"}
                  />
                  <StatCell
                    testid="stat-active-sources"
                    label="活跃源"
                    value={
                      overview.activeSources !== null && overview.totalSources !== null
                        ? `${overview.activeSources}/${overview.totalSources}`
                        : null
                    }
                    note={
                      overview.totalSources === null
                        ? "诊断不可达 · doctor 分区失败"
                        : overviewWindow === "today"
                          ? `共 ${overview.totalSources} 源 · ok+degraded`
                          : `共 ${overview.totalSources} 源 · ok+degraded · 即时快照不随窗`
                    }
                    noteKind={overview.totalSources === null ? "alert" : "meta"}
                  />
                  <StatCell
                    testid="stat-window-push"
                    label="推送成功"
                    value={overview.windowPushOk}
                    note={
                      overviewWindow === "today"
                        ? "今日(UTC)各轮采集的推送成功数 · 受最近 20 轮上限(runs.list)"
                        : `近 ${overviewWindow} 天(UTC)各轮采集的推送成功数 · 受最近 20 轮上限(runs.list)`
                    }
                    noteKind="meta"
                  />
                  <StatCell
                    testid="stat-alerts"
                    label="告警"
                    value={overview.alerts}
                    note={
                      overviewWindow === "today"
                        ? "doctor error+warning 发现"
                        : "doctor error+warning 发现 · 即时快照不随窗"
                    }
                    noteKind="meta"
                    destructive={(overview.alerts ?? 0) > 0}
                  />
                </>
              )}
        </div>
        {/* R2 告警升格清单(D3):触发 = 告警或坏源非零,坏源行优先 + 品类级
            findings 补位,前三条封顶,行点跳源管理;皆零零占位 */}
        <AlertList rows={alertRows} />
      </section>

      {/* R2 刀2 重排:趋势卡升全宽 hero(与品类卡的配对等高拉伸会把短卡
          拉成空壳——实测 679px 等高中趋势卡近半是死区;Linear 参考亦为
          全宽区块纵向节奏),品类状态独立成节移至源健康度之上 */}
      <section aria-label="采集量趋势" className="px-6">
        {/* 采集量趋势(teardown #6:自绘 sparkline;building 态末点呼吸)。
            统一时间窗(补批四):窗口随概览头 Select,趋势卡不再自有 Select */}
        <Card>
          <CardHeader>
            <div className="flex items-center justify-between gap-2">
              <CardTitle className="flex items-center gap-2">
                <TrendingUp className="size-3.5 text-muted-foreground" />
                采集量趋势
                {collecting ? (
                  <Badge variant="default" className="animate-pulse">
                    采集中
                  </Badge>
                ) : null}
              </CardTitle>
            </div>
            <CardDescription>每日入库条目数(UTC 逐日;窗口随概览时间范围)</CardDescription>
          </CardHeader>
          <CardContent className="flex flex-col gap-3">
            {trendLoading && trend === null ? (
              <>
                <Skeleton className="h-12 w-full" />
                <Skeleton className="h-3 w-2/3" />
              </>
            ) : trendError ? (
              <TrendErrorAlert
                title="趋势不可用"
                code={trendError.code}
                message={trendError.message}
                testid="dashboard-trend-error"
              />
            ) : (
              <>
                <TrendChart
                  values={counts}
                  className="h-20"
                  yLabels={[`${trendPeak}`, `${Math.round(trendPeak / 2)}`, "0"]}
                  data-testid="dashboard-sparkline"
                  pulse={collecting}
                  aria-label={`${windowLabel}采集量趋势,共 ${trendTotal} 条,峰值 ${trendPeak} 条`}
                />
                {trend !== null && trend.length > 0 ? (
                  <p
                    className="flex items-center justify-between pl-11 font-mono text-2xs text-muted-foreground"
                    data-testid="trend-axis"
                  >
                    <span>{trend[0].date}</span>
                    <span className="text-muted-foreground/80">峰值 {trendPeak} 条/日</span>
                    <span>{trend[trend.length - 1].date}</span>
                  </p>
                ) : null}
                <p className="flex flex-wrap items-center gap-1.5 text-2xs text-muted-foreground">
                  <span data-testid="trend-total">
                    {windowLabel}共 {trendTotal} 条 · 峰值 {trendPeak} 条/日
                  </span>
                  <Badge variant="outline">UTC 逐日</Badge>
                </p>
              </>
            )}

            {/* 成功率第二序列(G6,10-04-desktop-b234):与采集量同吃统一
                时间窗(补批四);口径 = 每日 success/(total−running),与
                「最近采集成功率」卡(内存合并 active)不同源,卡面如实注记
                不冒充同源。终审修整:标题升 text-sm/medium(VL 指认与「不含
                进行中」辅注字号无级差);错误走独立警示条(视觉隔离);图加
                网格+数据点 + y 满刻度标注 */}
            <div className="mt-5 flex flex-col gap-2.5 border-t border-border/60 pt-5" data-testid="dashboard-rate-section">
              <p className="flex items-center gap-1.5 text-sm font-medium text-foreground">
                成功率
                <Badge variant="outline">不含进行中</Badge>
              </p>
              {trendLoading && outcomes === null ? (
                <>
                  <Skeleton className="h-12 w-full" />
                  <Skeleton className="h-3 w-2/3" />
                </>
              ) : outcomeError ? (
                <TrendErrorAlert
                  title="成功率趋势不可用"
                  code={outcomeError.code}
                  message={outcomeError.message}
                  testid="dashboard-rate-error"
                />
              ) : rateSeries.length === 0 ? (
                <p className="text-xs text-muted-foreground" data-testid="dashboard-rate-empty">
                  {windowLabel}无已完结采集——成功率无从谈起,先跑一轮再说
                </p>
              ) : (
                <>
                  <TrendChart
                    values={rateSeries.map((point) => point.rate)}
                    max={1}
                    area={false}
                    yLabels={["100%", "50%", "0"]}
                    data-testid="dashboard-rate-sparkline"
                    aria-label={
                      outcomeSummary && outcomeSummary.rate !== null
                        ? `${windowLabel}累计成功率 ${formatSuccessRate(outcomeSummary.rate)}` +
                          `(${outcomeSummary.success}/${outcomeSummary.finished} 次成功),无完结采集的日子不入线`
                        : `${windowLabel}成功率趋势,无完结采集的日子不入线`
                    }
                  />
                  <p className="flex items-center justify-between pl-11 font-mono text-2xs text-muted-foreground">
                    <span>{rateSeries[0]?.date}</span>
                    <span className="text-muted-foreground/80">刻度 0–100%</span>
                    <span>{rateSeries[rateSeries.length - 1]?.date}</span>
                  </p>
                  {outcomeSummary && outcomeSummary.rate !== null ? (
                    <p className="flex flex-wrap items-center gap-1.5 text-2xs text-muted-foreground">
                      <span data-testid="rate-summary">
                        {windowLabel}累计成功率 {formatSuccessRate(outcomeSummary.rate)}(
                        {outcomeSummary.success}/{outcomeSummary.finished} 次成功)
                      </span>
                      <Badge variant="outline">零完结日不入线</Badge>
                    </p>
                  ) : null}
                </>
              )}
            </div>
          </CardContent>
        </Card>
      </section>

      {/* 源健康度卡网格(D4;teardown #3/#4:四态点 + 14 medium 名称 + muted 次行 + 相对时间;gap-6)。
          补批五折叠正常源:坏源(state≠ok)照旧铺开,ok 源收进折叠组默认收起
          (spec 折叠组惯例 = 原生 button + aria-expanded/aria-controls) */}
      <section aria-label="源健康度" className="flex flex-col gap-3 px-6">
        <div className="flex flex-wrap items-center justify-between gap-2">
          <div className="flex items-center gap-2">
            <HeartPulse className="size-3.5 text-muted-foreground" />
            <h2 className="text-base font-semibold text-foreground">源健康度</h2>
            <span className="text-xs text-muted-foreground">
              {sourceCards.length} 个源 · 异常优先
            </span>
          </div>
          {healthCounts === null ? null : (
            <div className="flex items-center gap-3">
              {(Object.keys(SOURCE_STATE) as SourceHealthState[]).map((state) => (
                <span
                  key={state}
                  data-testid={`health-${state}`}
                  title={`${SOURCE_STATE[state].label} ${healthCounts[state]}`}
                  className="inline-flex items-center gap-1.5 text-xs text-muted-foreground"
                >
                  <span aria-hidden className={cn("size-2 rounded-full", SOURCE_STATE[state].dot)} />
                  {healthCounts[state]}
                </span>
              ))}
            </div>
          )}
        </div>
        {loading && !data ? (
          <div className={SOURCE_GRID_CLASS}>
            {[0, 1, 2, 3].map((index) => (
              <Skeleton key={index} className="h-28 w-full" />
            ))}
          </div>
        ) : sourceCards.length === 0 ? (
          <EmptyState
            compact
            title="暂无源"
            description="已载品类下的采集源会在此按健康度展示;先到「源管理」确认品类与源配置"
          />
        ) : (
          <>
            {badSourceCards.length > 0 ? (
              <div data-testid="source-health-grid" className={SOURCE_GRID_CLASS}>
                {badSourceCards.map((card) => (
                  <SourceCard key={card.key} card={card} />
                ))}
              </div>
            ) : null}
            {okSourceCards.length > 0 ? (
              <div className="flex flex-col gap-3">
                <button
                  type="button"
                  data-testid="source-ok-toggle"
                  aria-expanded={okSourcesExpanded}
                  aria-controls="source-ok-group"
                  onClick={() => setOkSourcesExpanded((expanded) => !expanded)}
                  className="self-start rounded-sm text-xs font-medium text-link transition-colors duration-(--duration-fast) hover:text-foreground"
                >
                  {okSourceCards.length} 个源正常 · {okSourcesExpanded ? "收起" : "展开"}
                </button>
                {okSourcesExpanded ? (
                  <div id="source-ok-group" data-testid="source-ok-group" className={SOURCE_GRID_CLASS}>
                    {okSourceCards.map((card) => (
                      <SourceCard key={card.key} card={card} />
                    ))}
                  </div>
                ) : null}
              </div>
            ) : null}
          </>
        )}
      </section>

      {/* 品类状态(R2 重排:自趋势配对中独立;节头与源健康度同款 = 小卡栅格节
          统一「图标+标题+口径注记 → 栅格」家族,与概览/趋势大卡家族分层) */}
      <section aria-label="品类状态" className="flex flex-col gap-3 px-6">
        <div className="flex flex-wrap items-center gap-2">
          <CircleDot className="size-3.5 text-muted-foreground" />
          <h2 className="text-base font-semibold text-foreground">品类状态</h2>
          <span className="text-xs text-muted-foreground">
            已载品类、调度与诊断评级(
            {deadCategoryCount > 0
              ? `${deadCategoryCount} 品类异常`
              : warningCategoryCount > 0
                ? `${warningCategoryCount} 品类有提醒`
                : "无异常"}
            )
          </span>
        </div>
        {loading && !data ? (
          <div className="grid grid-cols-1 gap-grid sm:grid-cols-2">
            {[0, 1, 2, 3].map((index) => (
              <Skeleton key={index} className="h-14 w-full" />
            ))}
          </div>
        ) : categories.length === 0 ? (
          <EmptyState
            compact
            title="暂无品类"
            description="首次启动会自动装载随包官方品类;若仍未出现,重启应用重试初始化,或到「源管理」查看插件目录"
          />
        ) : (
          <div className="grid grid-cols-1 gap-grid sm:grid-cols-2">
            {categories.map((category) => (
              <CategoryCard key={category.file} category={category} onRunFinished={() => void refresh()} />
            ))}
          </div>
        )}
      </section>

      <div className="grid grid-cols-1 gap-grid px-6 md:grid-cols-2">
        {/* 近期 run 成功率(运行区;行解剖对位 Kestra Executions 表行,头部
            「全部 run」= ExecutionRoot 到 Executions 列表的全量出口,纯导航) */}
        <Card>
          <CardHeader>
            <div className="flex items-center justify-between gap-2">
              <CardTitle className="flex items-center gap-2">
                <Activity className="size-3.5 text-muted-foreground" />
                最近采集成功率
              </CardTitle>
              <a
                href="#/logs"
                className="shrink-0 text-xs font-medium text-link transition-colors duration-(--duration-fast) hover:text-foreground"
              >
                全部采集 →
              </a>
            </div>
            <CardDescription>最近 {runSummary?.total ?? 0} 次采集的完成与成功分布</CardDescription>
          </CardHeader>
          <CardContent className="flex flex-col gap-2">
            {loading && !data ? (
              <>
                <Skeleton className="h-8 w-24" />
                <Skeleton className="h-3 w-full" />
              </>
            ) : runSummary === null ? null : (
              <>
                <div className="flex items-baseline gap-2">
                  <span data-testid="run-success-rate" className="text-2xl font-semibold text-foreground">
                    {formatSuccessRate(runSummary.successRate)}
                  </span>
                  <span className="text-2xs text-muted-foreground">
                    {runSummary.success}/{runSummary.finished} 次成功
                    {runSummary.running > 0 ? ` · ${runSummary.running} 个运行中` : ""}
                  </span>
                </div>
                <div className="flex flex-col">
                  {runSummary.recent.length === 0 ? (
                    <p className="flex items-center gap-1.5 py-2 text-xs text-muted-foreground">
                      <Activity className="size-3.5" />
                      还没有采集记录;跑一次后这里会列出最近结果
                    </p>
                  ) : (
                    runSummary.recent.map((run) => <RecentRunRow key={run.runId} run={run} />)
                  )}
                </div>
              </>
            )}
          </CardContent>
        </Card>

        {/* 反馈统计(B2,10-03-v112-desktop-parity;feedback.stats 好/坏 + Top 类目) */}
        <FeedbackStatsCard />
      </div>
    </div>
  );
}
