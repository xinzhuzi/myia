/**
 * 微信统计报告分区(10-14-wechat-stats-reports R6;消息屏微信工作台族,
 * 常驻分区判例:同版面、无返回钮、三层防)。
 *
 * 流:报告类型四选(私聊分析/群聊分析/年度报告/双人报告)→ 会话选择
 * (stats chats;群聊分析选 @chatroom,私聊/双人选好友,年度免选)→
 * 时间窗(近 30 天/近一年/全部;年度 = 年份或全部,年份从 chats 首末
 * 推导)→ 生成 → 数字卡 + 纯 CSS 条形(时段/类型)+ 排行 + 双人两列
 * 对照 + 7×24 热度格 → 「生成 AI 报告」(markdown-lite 渲染;隐私缺省
 * 喂聚合,ai_disabled/dependency_missing 给指引文案)→「导出」两件落盘。
 *
 * 零图表库依赖(纯 CSS 条形/格);错误族 20/21/22 结构化直显
 * (code+message+fix_hint);缓存命中显示耗时(「首次统计较慢,之后秒出」
 * 文案在生成按钮旁常驻提示)。
 */
import { useCallback, useMemo, useState } from "react";

import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { cn } from "@/lib/utils";
import { SidecarRequestError } from "@/lib/api";

import { MarkdownLite } from "@/screens/feed/markdown-lite";

import {
  wechatStatsAnnual,
  wechatStatsChat,
  wechatStatsChats,
  wechatStatsDual,
  wechatStatsExport,
  wechatStatsReport,
  yearsFromChats,
  type StatsAnnualView,
  type StatsCacheInfo,
  type StatsChatEntry,
  type StatsChatView,
  type StatsDualView,
  type StatsReportResult,
  type StatsWindow,
} from "./wechat-stats-api";

/** 报告类型(文案人话;wire mode 保留英文) */
type ReportKind = "chat" | "group" | "annual" | "dual";

const REPORT_KIND_LABELS: Array<{ kind: ReportKind; label: string }> = [
  { kind: "chat", label: "私聊分析" },
  { kind: "group", label: "群聊分析" },
  { kind: "annual", label: "年度报告" },
  { kind: "dual", label: "双人报告" },
];

const WEEKDAY_LABELS = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"];
const TYPE_LABELS: Array<{ key: string; label: string }> = [
  { key: "text", label: "文字" },
  { key: "image", label: "图片" },
  { key: "voice", label: "语音" },
  { key: "video", label: "视频" },
  { key: "sticker", label: "表情" },
  { key: "file_or_link", label: "文件/链接" },
  { key: "location", label: "位置" },
  { key: "other", label: "其他" },
  { key: "system", label: "系统" },
  { key: "revoke", label: "撤回" },
];

/** 结构化错误行(code+message+fix_hint;判例 wechat-local ReadOnlyError) */
function StatsError({ error, testId }: { error: SidecarRequestError; testId: string }) {
  const fixHint =
    typeof error.data === "object" && error.data !== null && "fix_hint" in error.data
      ? String((error.data as Record<string, unknown>).fix_hint)
      : null;
  return (
    <div
      className="flex min-w-0 flex-col gap-0.5 rounded-md border border-destructive/30 bg-destructive/10 px-3 py-2 text-xs text-destructive"
      data-testid={testId}
    >
      <span className="min-w-0 break-words">
        {error.message}(code={error.code})
      </span>
      {fixHint ? (
        <span className="min-w-0 break-words text-2xs opacity-80">修复指引:{fixHint}</span>
      ) : null}
    </div>
  );
}

/** 缓存耗时提示(R6:命中显示耗时;未命中显示计算耗时) */
function CacheHint({ cache }: { cache: StatsCacheInfo }) {
  return (
    <span className="text-2xs text-muted-foreground" data-testid="wx-stats-cache">
      {cache.hit
        ? `缓存命中(${cache.computed_ms}ms)`
        : `本次计算 ${cache.computed_ms}ms(首次统计较慢,之后秒出)`}
    </span>
  );
}

/** 纯 CSS 条形组(横向;max 归一;零图表库) */
function BarRow({ label, value, max, testId }: { label: string; value: number; max: number; testId?: string }) {
  const pct = max > 0 ? Math.max((value / max) * 100, value > 0 ? 1.5 : 0) : 0;
  return (
    <div className="flex min-w-0 items-center gap-2" data-testid={testId}>
      <span className="w-14 shrink-0 text-right text-2xs text-muted-foreground">{label}</span>
      <div className="h-2 min-w-0 flex-1 overflow-hidden rounded-full bg-muted/60">
        <div className="h-full rounded-full bg-primary/70" style={{ width: `${pct}%` }} />
      </div>
      <span className="w-12 shrink-0 text-right font-mono text-2xs text-foreground">{value}</span>
    </div>
  );
}

/** 7×24 热度格(CSS 透明度;行 = 周一..周日) */
function Heatmap({ grid }: { grid: number[][] }) {
  const max = Math.max(1, ...grid.flat());
  return (
    <div className="flex min-w-0 flex-col gap-1 overflow-x-auto" data-testid="wx-stats-heatmap">
      <div className="flex items-center gap-1 pl-10">
        {Array.from({ length: 24 }, (_, h) => (
          <span key={h} className="w-3 text-center text-2xs text-muted-foreground">
            {h % 6 === 0 ? h : ""}
          </span>
        ))}
      </div>
      {grid.map((row, weekday) => (
        <div key={weekday} className="flex items-center gap-1">
          <span className="w-9 shrink-0 text-right text-2xs text-muted-foreground">
            {WEEKDAY_LABELS[weekday] ?? ""}
          </span>
          {row.map((value, hour) => (
            <span
              key={hour}
              className="h-3 w-3 shrink-0 rounded-sm bg-primary"
              style={{ opacity: value > 0 ? 0.15 + (value / max) * 0.85 : 0.04 }}
              title={`${WEEKDAY_LABELS[weekday] ?? ""} ${String(hour).padStart(2, "0")}:${String(value)} 条`}
            />
          ))}
        </div>
      ))}
    </div>
  );
}

/** 数字卡 */
function StatCard({ label, value, testId }: { label: string; value: string; testId: string }) {
  return (
    <div
      className="flex min-w-0 flex-col gap-0.5 rounded-md border border-border/50 bg-muted/30 px-3 py-2"
      data-testid={testId}
    >
      <span className="min-w-0 truncate text-2xs text-muted-foreground">{label}</span>
      <span className="min-w-0 truncate font-mono text-base font-semibold text-foreground">{value}</span>
    </div>
  );
}

function formatSeconds(seconds: number | null | undefined): string {
  if (seconds === null || seconds === undefined) return "—";
  if (seconds < 60) return `${seconds} 秒`;
  if (seconds < 3600) return `${(seconds / 60).toFixed(1)} 分钟`;
  return `${(seconds / 3600).toFixed(1)} 小时`;
}

function formatTs(ts: number | null | undefined): string {
  if (!ts) return "—";
  return new Date(ts * 1000).toLocaleDateString();
}

/** 单会话(私聊/群聊)结果渲染 */
function ChatResult({ view, isGroup }: { view: StatsChatView; isGroup: boolean }) {
  const hourlyMax = Math.max(1, ...view.hourly);
  const typeEntries = TYPE_LABELS.map(({ key, label }) => ({
    label,
    value: view.type_counts[key as keyof typeof view.type_counts] ?? 0,
  }));
  const typeMax = Math.max(1, ...typeEntries.map((e) => e.value));
  return (
    <div className="flex min-w-0 flex-col gap-3" data-testid="wx-stats-result">
      <div className="grid grid-cols-2 gap-2 sm:grid-cols-4">
        <StatCard label="总消息" value={String(view.total)} testId="wx-stats-card-total" />
        <StatCard label="我发" value={String(view.sent)} testId="wx-stats-card-sent" />
        <StatCard label="收到" value={String(view.received)} testId="wx-stats-card-received" />
        <StatCard
          label="连续聊天天数"
          value={String(view.longest_streak.days)}
          testId="wx-stats-card-streak"
        />
      </div>
      <div className="flex min-w-0 flex-col gap-1">
        <p className="text-2xs text-muted-foreground">
          {view.longest_streak.days > 0 && view.longest_streak.from
            ? `最长连续 ${view.longest_streak.days} 天(${view.longest_streak.from} 起)`
            : "无连续天段"}
          ;活跃 {view.active_days} 天;会话 {view.sessions.total} 段(我发起 {view.sessions.me_initiated}
          ,对方发起 {view.sessions.other_initiated});回复速度平均{" "}
          {formatSeconds(view.response.avg_seconds)}(采样 {view.response.pairs} 对)
        </p>
        <CacheHint cache={view.cache} />
      </div>
      <div className="grid min-w-0 gap-3 lg:grid-cols-2">
        <div className="flex min-w-0 flex-col gap-1" data-testid="wx-stats-hourly">
          <p className="text-2xs font-medium text-foreground">最爱聊天时段(24 小时)</p>
          {view.hourly.map((value, hour) => (
            <BarRow
              key={hour}
              label={`${String(hour).padStart(2, "0")}时`}
              value={value}
              max={hourlyMax}
              testId={`wx-stats-hourly-${hour}`}
            />
          ))}
        </div>
        <div className="flex min-w-0 flex-col gap-1" data-testid="wx-stats-type">
          <p className="text-2xs font-medium text-foreground">消息类型分布</p>
          {typeEntries.map((entry) => (
            <BarRow key={entry.label} label={entry.label} value={entry.value} max={typeMax} />
          ))}
          <p className="text-2xs font-medium text-foreground">一周分布</p>
          {view.weekday.map((value, weekday) => (
            <BarRow key={weekday} label={WEEKDAY_LABELS[weekday] ?? ""} value={value} max={Math.max(1, ...view.weekday)} />
          ))}
        </div>
      </div>
      {view.top_phrases.length > 0 ? (
        <div className="flex min-w-0 flex-wrap items-center gap-1.5" data-testid="wx-stats-phrases">
          <p className="text-2xs font-medium text-foreground">高频短语:</p>
          {view.top_phrases.map((phrase) => (
            <Badge key={phrase.phrase} variant="secondary">
              {phrase.phrase} ×{phrase.count}
            </Badge>
          ))}
        </div>
      ) : null}
      {isGroup && view.senders.length > 0 ? (
        <div className="flex min-w-0 flex-col gap-1" data-testid="wx-stats-senders">
          <p className="text-2xs font-medium text-foreground">发言排行(前 10)</p>
          {view.senders.slice(0, 10).map((sender, index) => (
            <div key={sender.sender_id} className="flex min-w-0 items-baseline gap-2 text-xs">
              <span className="w-5 shrink-0 text-right font-mono text-2xs text-muted-foreground">
                {index + 1}
              </span>
              <span className="min-w-0 truncate" title={sender.sender_id}>
                {sender.display}
              </span>
              <span className="ml-auto shrink-0 font-mono text-2xs text-muted-foreground">
                {sender.count}
              </span>
            </div>
          ))}
        </div>
      ) : null}
    </div>
  );
}

/** 年度报告结果渲染 */
function AnnualResult({ view }: { view: StatsAnnualView }) {
  const hourlyMax = Math.max(1, ...view.hourly);
  return (
    <div className="flex min-w-0 flex-col gap-3" data-testid="wx-stats-result">
      <div className="grid grid-cols-2 gap-2 sm:grid-cols-4">
        <StatCard label="总消息(私聊)" value={String(view.total)} testId="wx-stats-card-total" />
        <StatCard label="聊过的人" value={String(view.chats_count)} testId="wx-stats-card-chats" />
        <StatCard label="我发" value={String(view.sent)} testId="wx-stats-card-sent" />
        <StatCard
          label="连续聊天天数"
          value={String(view.longest_streak.days)}
          testId="wx-stats-card-streak"
        />
      </div>
      <div className="flex min-w-0 flex-col gap-1">
        <p className="text-2xs text-muted-foreground">
          深夜(0-5:59)消息 {view.midnight.count} 条
          {view.midnight.top_chat ? `,深夜之最:${view.midnight.top_chat.display_name ?? view.midnight.top_chat.chat_id}` : ""}
          ;活跃 {view.active_days} 天;可用年份:{view.years_available.join(" / ") || "—"}
        </p>
        <CacheHint cache={view.cache} />
      </div>
      <div className="flex min-w-0 flex-col gap-1" data-testid="wx-stats-hourly">
        <p className="text-2xs font-medium text-foreground">最爱聊天时段(24 小时)</p>
        {view.hourly.map((value, hour) => (
          <BarRow key={hour} label={`${String(hour).padStart(2, "0")}时`} value={value} max={hourlyMax} />
        ))}
      </div>
      {view.top_chats.length > 0 ? (
        <div className="flex min-w-0 flex-col gap-1" data-testid="wx-stats-top-chats">
          <p className="text-2xs font-medium text-foreground">最常聊的人(前 10)</p>
          {view.top_chats.slice(0, 10).map((chat, index) => (
            <div key={chat.chat_id} className="flex min-w-0 items-baseline gap-2 text-xs">
              <span className="w-5 shrink-0 text-right font-mono text-2xs text-muted-foreground">
                {index + 1}
              </span>
              <span className="min-w-0 truncate" title={chat.chat_id}>
                {chat.display_name ?? chat.chat_id}
              </span>
              <span className="ml-auto shrink-0 font-mono text-2xs text-muted-foreground">
                {chat.count}
              </span>
            </div>
          ))}
        </div>
      ) : null}
      {view.top_phrases.length > 0 ? (
        <div className="flex min-w-0 flex-wrap items-center gap-1.5" data-testid="wx-stats-phrases">
          <p className="text-2xs font-medium text-foreground">高频短语:</p>
          {view.top_phrases.map((phrase) => (
            <Badge key={phrase.phrase} variant="secondary">
              {phrase.phrase} ×{phrase.count}
            </Badge>
          ))}
        </div>
      ) : null}
    </div>
  );
}

/** 双人对照结果渲染(两列 + 热度格) */
function DualResult({ view }: { view: StatsDualView }) {
  return (
    <div className="flex min-w-0 flex-col gap-3" data-testid="wx-stats-result">
      <div className="grid grid-cols-2 gap-2 sm:grid-cols-4">
        <StatCard label="我的消息" value={String(view.me.count)} testId="wx-stats-card-me" />
        <StatCard label="对方消息" value={String(view.other.count)} testId="wx-stats-card-other" />
        <StatCard
          label="连续聊天天数"
          value={String(view.longest_streak.days)}
          testId="wx-stats-card-streak"
        />
        <StatCard label="活跃天数" value={String(view.active_days)} testId="wx-stats-card-active" />
      </div>
      <div className="flex min-w-0 flex-col gap-1">
        {view.first_chat ? (
          <p className="min-w-0 break-words text-2xs text-muted-foreground">
            最初一条:{view.first_chat.sender === "me" ? "我" : "对方"} ·{" "}
            {formatTs(view.first_chat.ts)} ·「{view.first_chat.text ?? "—"}」
          </p>
        ) : null}
        <CacheHint cache={view.cache} />
      </div>
      <div className="grid min-w-0 gap-2 sm:grid-cols-2" data-testid="wx-stats-dual-columns">
        {(
          [
            { key: "me", label: "我", side: view.me },
            { key: "other", label: "对方", side: view.other },
          ] as const
        ).map(({ key, label, side }) => (
          <div
            key={key}
            className="flex min-w-0 flex-col gap-1.5 rounded-md border border-border/50 px-3 py-2"
            data-testid={`wx-stats-dual-${key}`}
          >
            <p className="text-2xs font-medium text-foreground">{label}</p>
            <p className="text-xs text-muted-foreground">
              消息 {side.count} 条;开启话题 {side.initiated} 次;平均回复{" "}
              {formatSeconds(side.avg_response_seconds)}
            </p>
            {side.top_phrases.length > 0 ? (
              <div className="flex min-w-0 flex-wrap gap-1">
                {side.top_phrases.slice(0, 8).map((phrase) => (
                  <Badge key={phrase.phrase} variant="secondary">
                    {phrase.phrase} ×{phrase.count}
                  </Badge>
                ))}
              </div>
            ) : null}
          </div>
        ))}
      </div>
      <div className="flex min-w-0 flex-col gap-1">
        <p className="text-2xs font-medium text-foreground">聊天热度(一周 × 24 小时)</p>
        <Heatmap grid={view.heatmap} />
      </div>
    </div>
  );
}

/**
 * 统计报告分区(常驻;R6 全流)。纯组件态:结果/AI 报告/导出回执都在
 * 本组件 state,不入 store(读回不入情报管线,G3 同源纪律)。
 */
export function WechatStatsPanel() {
  const [kind, setKind] = useState<ReportKind>("chat");
  const [chats, setChats] = useState<StatsChatEntry[] | null>(null);
  const [chatsError, setChatsError] = useState<SidecarRequestError | null>(null);
  const [loadingChats, setLoadingChats] = useState(false);
  const [chatId, setChatId] = useState<string>("");
  const [window, setWindow] = useState<StatsWindow>({ kind: "since", days: 30 });
  const [year, setYear] = useState<number | "all">("all");
  const [result, setResult] = useState<
    { kind: ReportKind; chat: StatsChatView } | { kind: "annual"; annual: StatsAnnualView } | { kind: "dual"; dual: StatsDualView } | null
  >(null);
  const [error, setError] = useState<SidecarRequestError | null>(null);
  const [loading, setLoading] = useState(false);
  const [report, setReport] = useState<StatsReportResult | null>(null);
  const [reportError, setReportError] = useState<SidecarRequestError | null>(null);
  const [reportLoading, setReportLoading] = useState(false);
  const [exportReceipt, setExportReceipt] = useState<string | null>(null);

  const needsChat = kind !== "annual";
  const chatFilter = useCallback(
    (chat: StatsChatEntry) =>
      kind === "group" ? chat.kind === "group" : chat.kind === "private",
    [kind],
  );
  const selectableChats = useMemo(
    () => (chats ?? []).filter(chatFilter),
    [chats, chatFilter],
  );
  const years = useMemo(() => yearsFromChats(chats ?? []), [chats]);

  const loadChats = useCallback(async () => {
    setError(null);
    setChatsError(null);
    setLoadingChats(true);
    try {
      const view = await wechatStatsChats();
      setChats(view.chats);
      setChatsError(null);
    } catch (raw) {
      setChats(null);
      setChatsError(raw instanceof SidecarRequestError ? raw : new SidecarRequestError({ code: "bridge_error", path: "$", message: String(raw) }));
    } finally {
      setLoadingChats(false);
    }
  }, []);

  const generate = useCallback(async () => {
    setError(null);
    setReport(null);
    setReportError(null);
    setExportReceipt(null);
    if (needsChat && !chatId) {
      setError(new SidecarRequestError({ code: "invalid_params", path: "chat_id", message: "请先选择一个会话" }));
      return;
    }
    setLoading(true);
    try {
      if (kind === "annual") {
        setResult({ kind: "annual", annual: await wechatStatsAnnual(year) });
      } else if (kind === "dual") {
        setResult({ kind: "dual", dual: await wechatStatsDual(chatId, window) });
      } else {
        setResult({ kind, chat: await wechatStatsChat(chatId, window) });
      }
    } catch (raw) {
      setResult(null);
      setError(
        raw instanceof SidecarRequestError
          ? raw
          : new SidecarRequestError({ code: "bridge_error", path: "$", message: String(raw) }),
      );
    } finally {
      setLoading(false);
    }
  }, [chatId, kind, needsChat, window, year]);

  /** AI 报告载荷 = 前端已持的桥应答(桥不重查) */
  const statsPayloadForReport = useMemo<unknown>(() => {
    if (!result) return null;
    if ("annual" in result) return { stats_annual: result.annual };
    if ("dual" in result) return { stats_dual: result.dual };
    return { stats_chat: result.chat };
  }, [result]);

  const generateReport = useCallback(async () => {
    if (!statsPayloadForReport) return;
    setReportError(null);
    setReportLoading(true);
    try {
      setReport(
        await wechatStatsReport(
          result?.kind === "annual" ? "annual" : result?.kind === "dual" ? "dual" : "chat",
          statsPayloadForReport,
        ),
      );
    } catch (raw) {
      setReport(null);
      setReportError(
        raw instanceof SidecarRequestError
          ? raw
          : new SidecarRequestError({ code: "bridge_error", path: "$", message: String(raw) }),
      );
    } finally {
      setReportLoading(false);
    }
  }, [result, statsPayloadForReport]);

  const exportResult = useCallback(async () => {
    if (!statsPayloadForReport) return;
    setExportReceipt(null);
    try {
      const name =
        result && "annual" in result
          ? `年度报告-${result.annual.year === "all" ? "全部" : result.annual.year}.json`
          : result && "dual" in result
            ? `双人报告-${result.dual.display_name ?? result.dual.chat_id}.json`
            : result && result.kind === "group"
              ? `群聊分析-${result.chat.display_name ?? result.chat.chat_id}.json`
              : `私聊分析-${result?.chat.display_name ?? result?.chat.chat_id ?? "会话"}.json`;
      const receipt = await wechatStatsExport(name, statsPayloadForReport, report?.report_markdown);
      if (receipt) {
        setExportReceipt(
          `已导出:${receipt.json_path}${receipt.markdown_path ? ` + ${receipt.markdown_path}` : ""}`,
        );
      } // null = 用户取消,静默
    } catch (raw) {
      setError(
        raw instanceof SidecarRequestError
          ? raw
          : new SidecarRequestError({ code: "export_failed", path: "$", message: String(raw) }),
      );
    }
  }, [report, result, statsPayloadForReport]);

  return (
    <div className="flex min-w-0 flex-col gap-2.5" data-testid="wx-stats-panel">
      <p className="min-w-0 break-words text-xs font-medium text-foreground">
        统计报告
        <span className="ml-2 text-2xs font-normal text-muted-foreground">
          解密副本只读统计,零出网;首次统计较慢,之后秒出(文件缓存)
        </span>
      </p>

      {/* 报告类型四选 */}
      <div className="flex min-w-0 flex-wrap gap-1.5" data-testid="wx-stats-kind">
        {REPORT_KIND_LABELS.map(({ kind: k, label }) => (
          <Button
            key={k}
            size="sm"
            variant={kind === k ? "default" : "outline"}
            className="h-7 text-xs"
            data-testid={`wx-stats-kind-${k}`}
            onClick={() => {
              setKind(k);
              setResult(null);
              setReport(null);
              setReportError(null);
              setError(null);
              setExportReceipt(null);
              // 任一类型都可能消费 chats(私聊/群聊/双人选会话;年度推
              // 导年份清单),未拉过即拉
              if (chats === null && !loadingChats) {
                void loadChats();
              }
            }}
          >
            {label}
          </Button>
        ))}
      </div>

      {/* 会话选择 + 时间窗 */}
      <div className="flex min-w-0 flex-wrap items-center gap-2">
        {needsChat ? (
          <>
            <Button
              size="sm"
              variant="outline"
              className="h-7 text-xs"
              disabled={loadingChats}
              data-testid="wx-stats-load-chats"
              onClick={() => void loadChats()}
            >
              {loadingChats ? "拉取中…" : "拉取会话"}
            </Button>
            <select
              aria-label="选择会话"
              className="h-7 min-w-0 max-w-64 rounded-md border border-border bg-background px-2 text-xs"
              data-testid="wx-stats-chat-select"
              value={chatId}
              disabled={loadingChats || selectableChats.length === 0}
              onChange={(event) => setChatId(event.target.value)}
            >
              <option value="">
                {selectableChats.length === 0 ? "先拉取会话列表" : "选择会话…"}
              </option>
              {selectableChats.map((chat) => (
                <option key={chat.chat_id} value={chat.chat_id}>
                  {`${chat.display_name ?? chat.chat_id}(${chat.message_count})`}
                </option>
              ))}
            </select>
          </>
        ) : (
          <select
            aria-label="统计年份"
            className="h-7 rounded-md border border-border bg-background px-2 text-xs"
            data-testid="wx-stats-year-select"
            value={String(year)}
            onChange={(event) => setYear(event.target.value === "all" ? "all" : Number(event.target.value))}
          >
            <option value="all">全部年份</option>
            {years.map((y) => (
              <option key={y} value={y}>
                {y} 年
              </option>
            ))}
          </select>
        )}
        {kind !== "annual" ? (
          <select
            aria-label="时间窗"
            className="h-7 rounded-md border border-border bg-background px-2 text-xs"
            data-testid="wx-stats-window-select"
            value={window.kind === "since" ? String(window.days) : "all"}
            onChange={(event) =>
              setWindow(event.target.value === "all" ? { kind: "all" } : { kind: "since", days: Number(event.target.value) })
            }
          >
            <option value="30">近 30 天</option>
            <option value="365">近一年</option>
            <option value="all">全部</option>
          </select>
        ) : null}
        <Button
          size="sm"
          className="h-7 text-xs"
          disabled={loading}
          data-testid="wx-stats-generate"
          onClick={() => void generate()}
        >
          {loading ? "统计中…" : "生成"}
        </Button>
      </div>

      {chatsError ? <StatsError error={chatsError} testId="wx-stats-chats-error" /> : null}
      {error ? <StatsError error={error} testId="wx-stats-error" /> : null}

      {result && "annual" in result ? <AnnualResult view={result.annual} /> : null}
      {result && !("annual" in result) && !("dual" in result) ? (
        <ChatResult view={result.chat} isGroup={result.kind === "group"} />
      ) : null}
      {result && "dual" in result ? <DualResult view={result.dual} /> : null}

      {result ? (
        <div className="flex min-w-0 flex-wrap items-center gap-2" data-testid="wx-stats-actions">
          <Button
            size="sm"
            variant="outline"
            className="h-7 text-xs"
            disabled={reportLoading}
            data-testid="wx-stats-ai"
            onClick={() => void generateReport()}
          >
            {reportLoading ? "生成中…" : "生成 AI 报告"}
          </Button>
          <Button
            size="sm"
            variant="outline"
            className="h-7 text-xs"
            data-testid="wx-stats-export"
            onClick={() => void exportResult()}
          >
            导出
          </Button>
          {exportReceipt ? (
            <span
              className="min-w-0 break-all text-2xs text-muted-foreground"
              data-testid="wx-stats-export-receipt"
            >
              {exportReceipt}
            </span>
          ) : null}
        </div>
      ) : null}

      {reportError ? <StatsError error={reportError} testId="wx-stats-ai-error" /> : null}
      {report ? (
        <div
          className={cn("flex min-w-0 flex-col gap-1 rounded-md border border-border/60 p-3")}
          data-testid="wx-stats-ai-report"
        >
          <p className="text-2xs text-muted-foreground">
            AI 报告(模型 {report.model},消耗 {report.total_tokens} tokens;基于聚合数字,零逐条原文)
          </p>
          <MarkdownLite markdown={report.report_markdown} testId="wx-stats-ai-markdown" />
        </div>
      ) : null}
    </div>
  );
}
