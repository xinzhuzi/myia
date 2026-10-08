import { useCallback, useEffect, useMemo, useRef, useState } from "react";
import {
  Bookmark,
  Check,
  ChevronDown,
  ChevronRight,
  Copy,
  Download,
  ExternalLink,
  FileText,
  Globe,
  Inbox,
  Percent,
  Play,
  Radar,
  RefreshCw,
  Rss,
  Search,
  Send,
  SlidersHorizontal,
  Sparkles,
  Star,
  Tags,
  X,
} from "lucide-react";
import { useNavigate } from "react-router-dom";

import { EmptyState } from "@/components/empty-state";
import { PageHeader } from "@/components/layout/page-header";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import {
  ContextMenu,
  ContextMenuContent,
  ContextMenuItem,
  ContextMenuSeparator,
  ContextMenuTrigger,
} from "@/components/ui/context-menu";
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";
import { Input } from "@/components/ui/input";
import { Skeleton } from "@/components/ui/skeleton";
import { api, onSidecarEvent, SidecarRequestError } from "@/lib/api";
import type { FeedEnrichResult, FeedItem, UnlistenFn } from "@/lib/api";

import {
  appendFeedPage,
  appendWatchlistKeyword,
  applyFeedFilter,
  bodyWithoutTitleDup,
  categoryColor,
  categoryOptionsFromHealth,
  cardDigest,
  channelDisplayName,
  channelKindOf,
  dayWindowStart,
  DEFAULT_FEED_DISPLAY,
  dealPriceView,
  defaultExportName,
  engineMapFromHealth,
  exportFeedView,
  FEED_PAGE_SIZE,
  fetchFeedPage,
  formatRelativeTime,
  groupFeedItems,
  groupFeedItemsByChannel,
  imAppOf,
  importLocalFeedStates,
  inDayWindow,
  isLaterResurface,
  isOpenableUrl,
  itemKey,
  KEYWORD_MAX_CHARS,
  LATER_RESURFACE_DAYS,
  listYamlTargets,
  LIVE_POLL_INTERVAL_MS,
  loadFeedDisplay,
  loadFeedStates,
  mergeFreshItems,
  primaryScore,
  READ_STATE_PROTOCOL,
  readYamlRaw,
  saveFeedDisplay,
  saveFeedStates,
  saveYamlRaw,
  setMarkerBulk,
  sortUnreadFirst,
  SOURCE_KIND_PROTOCOL,
  statesFromItems,
  streamKindCards,
  streamKindSubRows,
  telegramChannelCards,
  telegramMirrorUrlOf,
  toggleMarker,
  type ChannelKind,
  type ExportFormat,
  type FeedCategoryOption,
  type FeedDisplayOptions,
  type StreamKindCardData,
  type StreamKindSubRow,
  type TelegramChannelCardData,
  type YamlTargetFile,
} from "./api";
import type { FeedFilter, FeedStateMap } from "./api";
import { telegramGetStatus, telegramWebLogin, type TelegramStatus } from "@/screens/settings/telegram-api";
import { WebviewWindow } from "@tauri-apps/api/webviewWindow";

import { FeedCardFeedback } from "./feed-card-feedback";
import { MarkdownLite } from "./markdown-lite";

/*
 * 10-04-ui-kestra-anchor(情报流):满高列表骨架与行距密度借自 Apache-2.0
 * kestra/ui/src/components/executions/Executions.vue + design-system
 * KsDataTable(满高内滚+sticky 组头贴容器顶),借结构改语义。不抄:整表化
 * (保行级卡片交互)、复选/批量/分页(见 evidence/情报流-mapping.md)。
 */

/** 过滤页签(默认未读,Miniflux 式) */
const FILTERS: { key: FeedFilter; label: string }[] = [
  { key: "unread", label: "未读" },
  { key: "starred", label: "星标" },
  { key: "later", label: "稍后读" },
  { key: "all", label: "全部" },
];

/** 渠道类型呈现元(10-06-feed-channel-groups):渠道子组头图标/类型词/
 *  色调(品类分组下的二级组头与卡面呈现共用同一词表)。 */
const CHANNEL_KIND_META: Record<ChannelKind, { label: string; Icon: typeof Rss; className: string }> = {
  telegram: { label: "频道", Icon: Send, className: "text-primary" },
  watch: { label: "监控", Icon: Radar, className: "text-warning" },
  document: { label: "日报", Icon: FileText, className: "text-primary/80" },
  deal: { label: "优惠", Icon: Percent, className: "text-ok" },
  news: { label: "新闻", Icon: Rss, className: "text-muted-foreground" },
};

/** 源名展示词 channelDisplayName(telegram-<频道> 规约)已收编 api.ts
 *  (10-08-tg-channel-card):渠道卡聚合 label 与卡面头区共用同一词表。 */

const EMPTY_TEXT: Record<FeedFilter, { title: string; description: string }> = {
  unread: { title: "没有未读条目", description: "新采集的条目会按新→旧出现在这里" },
  starred: { title: "还没有星标", description: "点击条目卡上的星形按钮收藏重要情报" },
  later: {
    title: "稍后读还是空的",
    description: `点击书签按钮把条目放入稍后读;放入超过 ${LATER_RESURFACE_DAYS} 天会自动回到未读`,
  },
  all: { title: "情报流还是空的", description: "新采集的条目会按新→旧出现在这里;先跑一次采集" },
};

/** 搜索防抖(G1):输入停顿 300ms 提交;Enter 立即提交 */
const SEARCH_DEBOUNCE_MS = 300;

/** 图析行截断上限(字符;10-03-vision-pipeline:metadata.image_ocr 可达全文,
 *  feed 屏只出单行摘要,CSS truncate 再兜底一行;全文看卡片展开态)。 */
const IMAGE_OCR_SUMMARY_CHARS = 160;

/** 图析单行摘要:压平空白 + 超限截断加省略号;空串返回 null(不渲染行)。 */
function imageOcrSummary(text: string | null | undefined): string | null {
  if (!text) return null;
  const flat = text.replace(/\s+/g, " ").trim();
  if (!flat) return null;
  if (flat.length <= IMAGE_OCR_SUMMARY_CHARS) return flat;
  return `${flat.slice(0, IMAGE_OCR_SUMMARY_CHARS)}…`;
}

/** 展开态可见的图析详情存在性:OCR 全文 / 逐行 / 图说 / 图文件任一即算
 *  (10-03-vision-v2:三新键任意有值也让条目可展开)。 */
function hasImageDetails(item: FeedItem): boolean {
  return (
    imageOcrSummary(item.image_ocr) !== null ||
    Boolean(item.image_caption && item.image_caption.trim()) ||
    (item.image_files?.length ?? 0) > 0 ||
    (item.image_ocr_lines?.length ?? 0) > 0
  );
}

/** OCR 逐行置信度色阶(conf 0-1;两引擎刻度不可互比,色阶只是视觉提示非度量) */
function ocrConfClass(conf: number): string {
  if (conf >= 0.9) return "text-ok";
  if (conf >= 0.7) return "text-foreground/80";
  return "text-warning";
}

/** 空流 CTA「运行第一个插件」的状态机(idle → starting → collecting → done/error) */
type RunCtaState =
  | { phase: "idle" }
  | { phase: "starting" }
  | { phase: "collecting"; runId: number }
  | { phase: "done" }
  | { phase: "error"; message: string };

/** G8 卡片「AI 摘要」状态机(idle → loading → done 保留展示可重跑 / error 可重试;
 *  精评结果由服务端回填 items 表 + enrich_cache,重进屏重取即缓存命中零 token)。 */
type EnrichCardState =
  | { phase: "idle" }
  | { phase: "loading" }
  | { phase: "done"; result: FeedEnrichResult }
  | { phase: "error"; code: string; message: string };

/** G12 卡片「沉淀为关键词」就地面板状态机(closed → listing → ready ⇄ writing
 *  → note(saved/present/error;note 态可改词/换目标重写,亦可关闭收起)。 */
type KeywordPinState =
  | { phase: "closed" }
  | { phase: "listing" }
  | { phase: "list_error"; message: string }
  | { phase: "ready" }
  | { phase: "writing" }
  | { phase: "note"; kind: "saved" | "present" | "error"; message: string };

/** 「打开原文」:plugin-shell open(受控 shell:allow-open,scope 仅 https?://)。
 *  动态 import:浏览器直开(vitest/预览)不加载 Tauri 壳包,点击才触路。 */
async function openInBrowser(url: string): Promise<void> {
  const shell = await import("@tauri-apps/plugin-shell");
  await shell.open(url);
}

/** 右键菜单「复制链接」(A-feed):navigator.clipboard 尽力而为——不可用/
 *  权限拒 = 静默(菜单轻动作,不弹错误行打断浏览)。 */
function copyLink(url: string): void {
  try {
    void navigator.clipboard?.writeText(url)?.catch(() => {});
  } catch {
    // 老 webview 无剪贴板 API:静默
  }
}

/** 绝对时间(展开态元信息行):YYYY-MM-DD HH:mm */
function formatAbsoluteTime(iso: string | null): string {
  if (!iso) return "—";
  const then = new Date(iso);
  if (Number.isNaN(then.getTime())) return iso;
  const pad = (value: number) => String(value).padStart(2, "0");
  return `${then.getFullYear()}-${pad(then.getMonth() + 1)}-${pad(then.getDate())} ${pad(then.getHours())}:${pad(then.getMinutes())}`;
}

function FeedCard({
  item,
  state,
  current,
  navFocused,
  kind,
  inChannelSection = false,
  onCurrent,
  onToggle,
  onOpenError,
  onEnriched,
  onOpenDetail,
}: {
  item: FeedItem;
  state: { read?: boolean; starred?: boolean; later?: boolean };
  /** 键盘「当前卡」(U/j/k 快捷键作用目标;hover/focus 进入时置位) */
  current: boolean;
  /** j/k 键盘巡游聚焦(仅键盘置位,鼠标 hover 即清):focus 环呈现与否 */
  navFocused: boolean;
  /** 渠道类型(10-06-feed-channel-groups:五档差异化呈现,判定见 api.ts) */
  kind: ChannelKind;
  /** 频道语境(10-08 验收:TG 分节详情的节内卡)——节头已标频道名,
   *  卡头不再重复渲染,只留相对时间;单频道流/source 作用域不在内 */
  inChannelSection?: boolean;
  onCurrent: (key: string) => void;
  onToggle: (item: FeedItem, marker: "starred" | "later" | "read") => void;
  onOpenError: (message: string) => void;
  /** G8 精评成功回传(FeedScreen 把 scores 并回列表,分数徽标即时刷新) */
  onEnriched: (item: FeedItem, result: FeedEnrichResult) => void;
  /** 主人令「点击信息,弹出详情」(10-08):标题/气泡/正文区点击 = 开详情
   *  弹窗(弹开即记已读);「展开条目」内联路径并存不废。 */
  onOpenDetail: (item: FeedItem) => void;
}) {
  // 展开态属卡片本地(每次进屏重置;不与已读/星标本地态混存)
  const [expanded, setExpanded] = useState(false);
  // G8 AI 摘要:卡片本地状态机(idle → loading → done/error)
  const [enrich, setEnrich] = useState<EnrichCardState>({ phase: "idle" });
  // G12 沉淀为关键词:就地面板(目标清单/选中目标/可编辑词面)
  const [pin, setPin] = useState<KeywordPinState>({ phase: "closed" });
  const [pinFiles, setPinFiles] = useState<YamlTargetFile[]>([]);
  const [pinTarget, setPinTarget] = useState("");
  const [pinKeyword, setPinKeyword] = useState(() =>
    (item.title || item.url).trim().slice(0, KEYWORD_MAX_CHARS),
  );
  const score = primaryScore(item);
  const time = formatRelativeTime(item.first_seen);
  const openable = isOpenableUrl(item.url);
  const rowKey = item.id ?? itemKey(item);
  const key = itemKey(item);
  const expandable = Boolean(item.content) || hasImageDetails(item);
  /** 收起态正文预览(10-08 验收:与标题重复的开头剥除,v3 cardDigest 同门;
   *  正文整段 = 标题时 null,预览行不渲染 —— 不再同屏读两遍) */
  const bodyPreview = bodyWithoutTitleDup(item);

  /** G8:单条精评(feed.enrich;item 传 dedup_key,resolve 口径同 feedback.mark)。
   *  无配置(enrich_not_configured)/超时/失败都走 error 态结构化明示,可重试。 */
  const runEnrich = useCallback(async () => {
    setEnrich({ phase: "loading" });
    try {
      const result = await api.feedEnrich({ item: item.dedup_key });
      setEnrich({ phase: "done", result });
      onEnriched(item, result);
    } catch (err) {
      setEnrich(
        err instanceof SidecarRequestError
          ? { phase: "error", code: err.code, message: err.message }
          : { phase: "error", code: "transport_error", message: String(err) },
      );
    }
  }, [item, onEnriched]);

  /** G12:开面板即拉品类 YAML 清单(坏文件 parse_ok=false 不给选,写入必过
   *  校验,不把用户往注定失败的路上引)。 */
  const openPin = useCallback(async () => {
    setPin({ phase: "listing" });
    try {
      const list = await listYamlTargets();
      const writable = list.files.filter((file) => file.parse_ok);
      setPinFiles(writable);
      setPinTarget(writable[0]?.file ?? "");
      setPin({ phase: "ready" });
    } catch (err) {
      setPin({
        phase: "list_error",
        message: err instanceof SidecarRequestError ? `${err.code}:${err.message}` : String(err),
      });
    }
  }, []);

  /** G12:yaml.read(mtime 基线)→ watchlist.keywords 原文手术 → yaml.save
   *  (乐观锁 + 服务端同门校验 + 跨文件 id 查重;改词不动 id,查重不破)。 */
  const writeKeyword = useCallback(async () => {
    const keyword = pinKeyword.trim();
    if (keyword === "") {
      setPin({ phase: "note", kind: "error", message: "关键词不能为空" });
      return;
    }
    if (keyword.length > KEYWORD_MAX_CHARS) {
      setPin({ phase: "note", kind: "error", message: `关键词超长(上限 ${KEYWORD_MAX_CHARS} 字)` });
      return;
    }
    if (pinTarget === "") {
      setPin({ phase: "note", kind: "error", message: "没有可写目标:plugins 目录内无可解析品类 YAML" });
      return;
    }
    setPin({ phase: "writing" });
    try {
      const raw = await readYamlRaw(pinTarget);
      const outcome = appendWatchlistKeyword(raw.content, keyword);
      if (!outcome.ok) {
        if (outcome.reason === "already_present") {
          setPin({ phase: "note", kind: "present", message: `「${keyword}」已在目标 YAML 的 watchlist.keywords,未重复写入` });
        } else if (outcome.reason === "keywords_unparsed") {
          setPin({ phase: "note", kind: "error", message: "该文件的 watchlist.keywords 排版无法就地解析;请到「配置」手动添加" });
        } else {
          setPin({ phase: "note", kind: "error", message: `关键词不合法(${outcome.reason === "keyword_too_long" ? "超长" : "为空"})` });
        }
        return;
      }
      const saved = await saveYamlRaw(pinTarget, outcome.content, raw.mtime);
      const name = pinFiles.find((file) => file.file === pinTarget)?.name ?? pinTarget;
      setPin({
        phase: "note",
        kind: "saved",
        message: `已写入 ${name}${saved.backed_up ? `(备份 ${saved.backed_up})` : ""}`,
      });
    } catch (err) {
      // mtime_conflict(并发改写)/ category_invalid(手术结果未过校验)等码原样明示
      setPin({
        phase: "note",
        kind: "error",
        message: err instanceof SidecarRequestError ? `${err.code}:${err.message}` : String(err),
      });
    }
  }, [pinKeyword, pinTarget, pinFiles]);
  // 品类色(D4):色条与品类徽标同源;无品类 → null(零色件)
  const color = categoryColor(item.category);
  // 渠道差异化呈现派生值(10-06-feed-channel-groups):价格/优惠行视图 +
  // urlwatch 目标页真链(watch_page 优先;条目 url 是 #watch-<sha> 锚)
  const deal = kind === "deal" ? dealPriceView(item) : null;
  const watchHref =
    kind === "watch"
      ? item.watch_page ?? (isOpenableUrl(item.url) ? item.url : null)
      : null;
  const watchHostname = (() => {
    if (watchHref === null) return null;
    try {
      return new URL(watchHref).hostname;
    } catch {
      return watchHref;
    }
  })();
  return (
    // 右键上下文菜单(A-feed,10-04-interaction-batch):ContextMenu 根是纯
    // Provider 零包装 DOM,asChild 把 onContextMenu 合到卡面(布局零扰动)。
    <ContextMenu>
      <ContextMenuTrigger asChild>
        {/* 三级密度卡(D4):13px 标题/正文、11px 元信息;hover 行背景 accent/50
            (teardown-linear-activity #5);品类色条/未读 accent 竖条(#6/D4)。
            j/k 键盘聚焦 = ring 环(A-feed;hover 只置 current 不亮环,Linear 式)。 */}
        <div
          data-testid={`feed-item-${rowKey}`}
          data-item-key={key}
          data-category={item.category ?? ""}
          data-kind={kind}
          data-unread={state.read ? "false" : "true"}
          data-current={current ? "true" : "false"}
          data-nav-focused={navFocused ? "true" : "false"}
          onMouseEnter={() => onCurrent(key)}
          onFocus={() => onCurrent(key)}
          className={`group/feed-item relative transition-colors duration-(--duration-fast) ease-out-expo ${
            kind === "telegram"
              ? `w-fit max-w-[min(100%,640px)] rounded-2xl rounded-tl-md border py-2 pl-3 pr-3 ${
                  state.read ? "border-border/40 bg-muted/25 hover:bg-muted/40" : "border-primary/25 bg-primary/10 hover:bg-primary/15"
                }`
              : `rounded-md border py-2 pr-3 pl-4 hover:bg-accent/50 ${
                  state.read ? "border-border/50 bg-muted/20" : "border-border bg-card"
                }`
          }${navFocused ? " ring-1 ring-primary/60" : ""}`}
        >
      {/* 左缘竖条:未读 = 2px 品牌紫亮档 #9869f7(primary-300;10-08 验收:
          #631bf3 卡底 2.30:1 不达非文字 3:1,提一档 4.40:1);已读 = 统一
          降饱和灰(10-08 审计 F4:品类色散列可落紫系与未读 accent 同色相,
          读态竖条通道失效——已读改走 muted 灰档,品类色只承担品类徽章通道) */}
      {/* TG 聊天气泡不带竖条(10-09 聊天主页风格:未读走泡底色/文字档) */}
      {kind !== "telegram" ? (
      <span
        aria-hidden
        data-testid={`feed-strip-${rowKey}`}
        className={`absolute top-2 bottom-2 left-0 w-0.5 rounded-full ${state.read ? "bg-muted-foreground/40" : "bg-[#9869f7]"}`}
      />
      ) : null}

      {/* ═══ 渠道差异化头区(10-06-feed-channel-groups)═══
          news/deal = 现状标题行形态(回归安全);telegram = 频道名行 +
          消息气泡(聊天感:正文气泡+时间+频道名);watch = 「有更新」徽标 +
          标题 + 目标页链接;document = 文档头(FileText + 标题)。
          10-08:标题/气泡点击 = 开详情弹窗(弹开即记已读);hover 用
          --link 文字档(F1:品牌紫文字档不达 AA);已读标题降 muted 档(F4)。*/}

      {/* 相对时间(公共件):右对齐灰色(teardown #4),hover 让位浮现的
          操作簇(#5);等宽数字(mono)——VL 指认时间戳与正文无视觉区分 */}
      {kind === "telegram" ? (
        <>
          {/* 聊天主页风格(10-09,主人令「做成 tg 的聊天主页风格」):
              频道名入泡顶(非节内语境),时间收泡底右下,窄泡左对齐;
              点击正文/摘要 = 详情弹窗(弹开即记已读)。 */}
          {!inChannelSection ? (
            <div className="flex items-center gap-1 text-2xs font-medium text-link">
              <Send aria-hidden className="size-3 shrink-0" />
              <span className="min-w-0 truncate">{channelDisplayName(item.source)}</span>
            </div>
          ) : null}
          <div
            className="mt-0.5 rounded-2xl rounded-tl-md border border-border/30 bg-background/40 px-3 py-2"
            data-testid={`feed-tg-bubble-${rowKey}`}
          >
            <button
              type="button"
              className={`w-full min-w-0 text-left text-sm leading-relaxed break-words whitespace-pre-wrap hover:text-link ${state.read ? "text-muted-foreground" : "text-foreground"}`}
              onClick={() => onOpenDetail(item)}
              title={`点击查看详情:${item.title || item.url}`}
            >
              {item.title || item.url}
            </button>
            {/* 收起正文行:经 bodyWithoutTitleDup 去标题重复开头(10-08 验收
                「正文复述标题,同屏读两遍」);无独有信息 = 行消失;展开态 =
                全文位,保留原文 */}
            {item.content && bodyPreview !== null ? (
              expanded ? (
                <p className="mt-1.5 text-sm leading-relaxed break-words whitespace-pre-wrap text-foreground/90">
                  {item.content}
                </p>
              ) : (
                <p
                  className="mt-1 line-clamp-2 cursor-pointer text-sm leading-relaxed text-muted-foreground hover:text-foreground/90"
                  onClick={() => onOpenDetail(item)}
                >
                  {bodyPreview}
                </p>
              )
            ) : null}
            {/* 泡底右下:展开钮(内联路径与详情弹窗并存,10-08 弹窗批语义)+
                时间(聊天惯例,等宽数字) */}
            <div className="mt-1 flex items-center justify-end gap-1">
              {expandable ? (
                <Button
                  variant="ghost"
                  size="icon"
                  className="size-5"
                  aria-label={expanded ? "收起条目" : "展开条目"}
                  aria-expanded={expanded}
                  onClick={() => setExpanded((current) => !current)}
                >
                  {expanded ? (
                    <ChevronDown className="size-3.5 text-muted-foreground" />
                  ) : (
                    <ChevronRight className="size-3.5 text-muted-foreground" />
                  )}
                </Button>
              ) : null}
              <time
                dateTime={item.first_seen ?? undefined}
                className="font-mono text-2xs text-muted-foreground"
              >
                {time}
              </time>
            </div>
          </div>
        </>
      ) : kind === "watch" ? (
        <>
          <div className="flex items-baseline justify-between gap-2 pr-1">
            <span className="flex min-w-0 items-center gap-1.5">
              {item.watch_event === "new" ? (
                <Badge variant="outline" className="shrink-0 text-2xs" title="urlwatch 首次快照(watch_event=new)">
                  已纳入监控
                </Badge>
              ) : (
                <Badge
                  variant="default"
                  className="shrink-0 border-primary/40 text-2xs"
                  data-testid={`feed-watch-badge-${rowKey}`}
                  title="urlwatch 变更事件(watch_event=changed)"
                >
                  有更新
                </Badge>
              )}
              <button
                type="button"
                className={`min-w-0 truncate text-left text-sm font-medium hover:text-link ${state.read ? "text-muted-foreground" : "text-foreground"}`}
                onClick={() => onOpenDetail(item)}
                title={`点击查看详情:${item.title || item.url}`}
              >
                {item.title || item.url}
              </button>
            </span>
            <time
              dateTime={item.first_seen ?? undefined}
              className="shrink-0 font-mono text-2xs text-muted-foreground transition-opacity duration-(--duration-fast) ease-out-expo group-hover/feed-item:opacity-0"
            >
              {time}
            </time>
          </div>
          {/* 目标页链接(watch_page 真链;受控 shell open 与「打开原文」同门;
              F1:文字档走 --link,品牌紫链接 2.30:1 不达 AA) */}
          {watchHref !== null && watchHostname !== null ? (
            <button
              type="button"
              className="mt-0.5 inline-flex w-fit items-center gap-1 text-2xs text-link hover:underline"
              data-testid={`feed-watch-target-${rowKey}`}
              title={`打开目标页:${watchHref}`}
              onClick={() =>
                void openInBrowser(watchHref).catch((err) =>
                  onOpenError(err instanceof Error ? err.message : String(err)),
                )
              }
            >
              <ExternalLink className="size-3 shrink-0" />
              {watchHostname}
            </button>
          ) : null}
        </>
      ) : (
        <div className="flex items-baseline justify-between gap-2 pr-1">
          {kind === "document" ? (
            <span className="flex min-w-0 items-center gap-1.5">
              <FileText aria-hidden className="size-3.5 shrink-0 text-primary/80" />
              <button
                type="button"
                className={`min-w-0 truncate text-left text-sm font-semibold hover:text-link ${state.read ? "text-muted-foreground" : "text-foreground"}`}
                onClick={() => onOpenDetail(item)}
                title={`点击查看详情:${item.title || item.url}`}
              >
                {item.title || item.url}
              </button>
            </span>
          ) : (
            <button
              type="button"
              className={`min-w-0 truncate text-left text-sm font-semibold hover:text-link ${state.read ? "text-muted-foreground" : "text-foreground"}`}
              onClick={() => onOpenDetail(item)}
              title={`点击查看详情:${item.title || item.url}`}
            >
              {item.title || item.url}
            </button>
          )}
          <time
            dateTime={item.first_seen ?? undefined}
            className="shrink-0 font-mono text-2xs text-muted-foreground transition-opacity duration-(--duration-fast) ease-out-expo group-hover/feed-item:opacity-0"
          >
            {time}
          </time>
        </div>
      )}

      {/* deal 价格/优惠行:现价突出(等宽大号)+ 原价划线 + 折扣/限免徽标
          (dealPriceView 镜像 games.yaml push 模板 elif 链与 classify 限免析取) */}
      {kind === "deal" && deal !== null && (deal.current !== null || deal.discount !== null) ? (
        <div className="mt-1 flex flex-wrap items-baseline gap-1.5" data-testid={`feed-deal-price-${rowKey}`}>
          {deal.free ? (
            <Badge variant="default" className="border-warning/40 text-2xs" title="限免(final_price 0 / 折扣 100% / 0 元双保险)">
              限免
            </Badge>
          ) : null}
          {deal.current !== null ? (
            <span className="font-mono text-base font-semibold text-foreground tabular-nums">
              {deal.current}
            </span>
          ) : null}
          {deal.original !== null ? (
            <span className="font-mono text-xs text-muted-foreground line-through tabular-nums">
              {deal.original}
            </span>
          ) : null}
          {deal.discount !== null && !deal.free ? (
            <Badge variant="secondary" className="font-mono text-2xs tabular-nums" title="折扣(discount_pct / savings_pct)">
              -{deal.discount}%
            </Badge>
          ) : null}
        </div>
      ) : null}

      {/* hover 浮现操作簇(#5):浮层质感(popover 面+轻阴影);focus-within 保键盘可达 */}
      <div
        data-feed-actions
        className="absolute top-1 right-1.5 flex items-center gap-0.5 rounded-md border border-border/70 bg-popover/95 p-0.5 opacity-0 shadow-popover transition-opacity duration-(--duration-fast) ease-out-expo group-hover/feed-item:opacity-100 focus-within:opacity-100"
      >
        {/* B2:卡片 👍/👎 反馈(channel=desktop,CLI feedback list 可见) */}
        <FeedCardFeedback item={item} />
        {/* G8:AI 摘要(feed.enrich 单条精评;loading 期禁用,done 后可重跑刷新) */}
        <Button
          variant="ghost"
          size="icon"
          className="size-6"
          aria-label="AI 摘要"
          aria-expanded={enrich.phase === "done"}
          title="AI 精评摘要(feed.enrich:骑品类 enrich 端点现跑,enrich_cache 命中零 token)"
          disabled={enrich.phase === "loading"}
          onClick={() => void runEnrich()}
        >
          <Sparkles
            className={
              enrich.phase === "done"
                ? "size-3.5 fill-primary text-primary"
                : enrich.phase === "loading"
                  ? "size-3.5 animate-pulse text-primary"
                  : "size-3.5 text-muted-foreground"
            }
          />
        </Button>
        {/* G12:沉淀为关键词(watchlist.keywords 写入;就地面板在卡内展开) */}
        <Button
          variant="ghost"
          size="icon"
          className="size-6"
          aria-label="沉淀为关键词"
          aria-expanded={pin.phase !== "closed"}
          title="沉淀为关键词:把本条目关键词写入所选品类 YAML 的 watchlist.keywords"
          onClick={() => (pin.phase === "closed" ? void openPin() : setPin({ phase: "closed" }))}
        >
          <Tags className={pin.phase !== "closed" ? "size-3.5 text-primary" : "size-3.5 text-muted-foreground"} />
        </Button>
        {openable ? (
          <Button
            variant="ghost"
            size="icon"
            className="size-6"
            aria-label="打开原文"
            title={`在浏览器打开:${item.url}`}
            onClick={() =>
              void openInBrowser(item.url).catch((err) =>
                onOpenError(err instanceof Error ? err.message : String(err)),
              )
            }
          >
            <ExternalLink className="size-3.5 text-muted-foreground" />
          </Button>
        ) : null}
        <Button
          variant="ghost"
          size="icon"
          className="size-6"
          aria-pressed={state.starred === true}
          aria-label="星标"
          onClick={() => onToggle(item, "starred")}
        >
          <Star className={state.starred ? "size-3.5 fill-warning text-warning" : "size-3.5 text-muted-foreground"} />
        </Button>
        <Button
          variant="ghost"
          size="icon"
          className="size-6"
          aria-pressed={state.later === true}
          aria-label="稍后读"
          // ① 到期重现知会(a11y label 兄弟位):稍后读不是黑洞,超窗回未读
          title={
            state.later
              ? `稍后读中:超过 ${LATER_RESURFACE_DAYS} 天自动回到未读;再点取消`
              : `放入稍后读;超过 ${LATER_RESURFACE_DAYS} 天自动回到未读`
          }
          onClick={() => onToggle(item, "later")}
        >
          <Bookmark className={state.later ? "size-3.5 fill-primary text-primary" : "size-3.5 text-muted-foreground"} />
        </Button>
        <Button
          variant="ghost"
          size="icon"
          className="size-6"
          aria-pressed={state.read === true}
          aria-label={state.read ? "标记未读" : "标记已读"}
          title="已读/未读切换(快捷键 U)"
          onClick={() => onToggle(item, "read")}
        >
          <Inbox className="size-3.5 text-muted-foreground" />
        </Button>
      </div>

      {kind !== "telegram" ? (
      <div className="mt-1 flex flex-wrap items-center gap-1.5">
        {expandable ? (
          <Button
            variant="ghost"
            size="icon"
            className="size-5"
            aria-label={expanded ? "收起条目" : "展开条目"}
            aria-expanded={expanded}
            onClick={() => setExpanded((current) => !current)}
          >
            {expanded ? (
              <ChevronDown className="size-3.5 text-muted-foreground" />
            ) : (
              <ChevronRight className="size-3.5 text-muted-foreground" />
            )}
          </Button>
        ) : null}
        {item.category && color ? (
          <span
            className="inline-flex w-fit shrink-0 items-center justify-center rounded-sm border px-1.5 py-0.5 text-2xs font-medium"
            style={{ color, backgroundColor: `${color}14`, borderColor: `${color}59` }}
          >
            {item.category}
          </span>
        ) : item.category ? (
          <Badge variant="secondary">{item.category}</Badge>
        ) : null}
        {/* telegram 渠道源名已在气泡头(channelDisplayName)——元信息行不重复;
            F9:其余渠道源名同走 channelDisplayName 词表(剥协议载体前缀),
            与 L2 渠道行/渠道卡同一套可读词,不再直出内部源 id */}
        <span className="text-2xs text-muted-foreground">{channelDisplayName(item.source)}</span>
        {item.tags.slice(0, 4).map((tag) => (
          <Badge key={tag} variant="outline" className="text-2xs">
            {tag}
          </Badge>
        ))}
        {score !== null ? (
          /* 终审修整:评分徽章强化边框+等宽数字——VL 指认「评分数字无背景或
             边框与文字混同」(default 变体 15% 底在暗卡上不够可见,40% 边框落实) */
          <Badge
            variant="default"
            className="border-primary/40 font-mono tabular-nums"
            title="精评分数(维度最高分)"
          >
            {score.toFixed(2)}
          </Badge>
        ) : null}
      </div>
      ) : null}

      {/* ═══ 正文块(渠道差异化,10-06-feed-channel-groups)═══
          telegram 正文在气泡内(头区已渲染)此处跳过;document = markdown
          文档视图(MarkdownLite,可折叠正文);watch = diff 变更明细(等宽
          块,展开态);news/deal = 现状两行摘要/展开全文(G2 零变化)。 */}
      {item.content && kind === "document" ? (
        expanded ? (
          <div className="mt-1.5" data-testid={`feed-doc-body-${rowKey}`}>
            <MarkdownLite markdown={item.content} />
            <p className="mt-1.5 text-2xs text-muted-foreground">
              首见 {formatAbsoluteTime(item.first_seen)}
              {item.pushed_at ? ` · 已推送 ${formatAbsoluteTime(item.pushed_at)}` : ""}
            </p>
          </div>
        ) : bodyPreview !== null ? (
          <p
            className="mt-1.5 cursor-pointer line-clamp-1 text-sm leading-relaxed text-muted-foreground hover:text-foreground/90"
            onClick={() => onOpenDetail(item)}
          >
            {bodyPreview.replace(/\s+/g, " ").trim()}
          </p>
        ) : null
      ) : item.content && kind === "watch" ? (
        expanded ? (
          <div className="mt-1.5" data-testid={`feed-watch-diff-${rowKey}`}>
            <span className="text-2xs text-muted-foreground">变更明细(diff)</span>
            <pre className="mt-0.5 overflow-x-auto rounded-md border border-border/60 bg-muted/30 px-2.5 py-2 font-mono text-xs leading-relaxed break-words whitespace-pre-wrap text-foreground/90">
              {item.content}
            </pre>
            <p className="mt-1.5 text-2xs text-muted-foreground">
              首见 {formatAbsoluteTime(item.first_seen)}
            </p>
          </div>
        ) : bodyPreview !== null ? (
          <p
            className="mt-1.5 cursor-pointer line-clamp-1 font-mono text-xs leading-relaxed text-muted-foreground hover:text-foreground/90"
            onClick={() => onOpenDetail(item)}
          >
            {bodyPreview.replace(/\s+/g, " ").trim()}
          </p>
        ) : null
      ) : item.content && kind !== "telegram" ? (
        expanded ? (
          // 展开态:全文 + 元信息(G2:C9 消号——正文与原文链接都在卡内)
          <div className="mt-1.5" data-testid={`feed-expanded-${item.id ?? itemKey(item)}`}>
            <p className="text-sm leading-relaxed break-words whitespace-pre-wrap text-foreground/90">
              {item.content}
            </p>
            <p className="mt-1.5 text-2xs text-muted-foreground">
              首见 {formatAbsoluteTime(item.first_seen)}
              {item.pushed_at ? ` · 已推送 ${formatAbsoluteTime(item.pushed_at)}` : ""}
              {openable ? ` · ${item.url}` : ""}
            </p>
          </div>
        ) : bodyPreview !== null ? (
          // 收起态摘要:正文 13px(D4 三级密度的正文级),去标题重复开头
          // (10-08 验收:不再复述标题);点击 = 详情弹窗
          <p
            className="mt-1.5 cursor-pointer line-clamp-2 text-sm leading-relaxed text-muted-foreground hover:text-foreground/90"
            onClick={() => onOpenDetail(item)}
          >
            {bodyPreview}
          </p>
        ) : null
      ) : null}

      {imageOcrSummary(item.image_ocr) ? (
        expanded ? (
          // 展开态(10-03-vision-v2):OCR 全文等宽块(保换行,详情态不截断)
          <div className="mt-1.5 flex flex-col gap-1" data-testid={`feed-image-ocr-${rowKey}`}>
            <span className="flex items-center gap-1.5 text-2xs text-muted-foreground">
              <Badge variant="outline" className="shrink-0" title="图析:配图 OCR 文本全文">
                图
              </Badge>
              OCR 全文
            </span>
            <pre className="whitespace-pre-wrap break-words rounded-md border border-border/60 bg-muted/30 px-2.5 py-2 font-mono text-xs leading-relaxed text-foreground/90">
              {item.image_ocr}
            </pre>
          </div>
        ) : (
          <p
            className="mt-1.5 flex items-center gap-1.5 text-2xs leading-relaxed text-muted-foreground"
            data-testid={`feed-image-ocr-${rowKey}`}
          >
            <Badge variant="outline" className="shrink-0" title="图析:配图 OCR 文本摘要">
              图
            </Badge>
            <span className="min-w-0 truncate" title={item.image_ocr ?? undefined}>
              {imageOcrSummary(item.image_ocr)}
            </span>
          </p>
        )
      ) : null}

      {expanded && (item.image_ocr_lines?.length ?? 0) > 0 ? (
        // 展开态:OCR 逐行表(文本 + 置信度色阶;conf 0-1 原样,引擎刻度不可互比)
        <div className="mt-1.5 flex flex-col gap-1" data-testid={`feed-image-ocr-lines-${rowKey}`}>
          <span className="text-2xs text-muted-foreground">OCR 逐行(置信度)</span>
          <div className="flex flex-col gap-0.5 rounded-md border border-border/60">
            {item.image_ocr_lines?.map((line, index) => (
              <div
                key={`${index}-${line.text.slice(0, 24)}`}
                className="flex items-baseline justify-between gap-2 px-2.5 py-0.5 odd:bg-muted/20"
              >
                <span className="min-w-0 break-words text-xs leading-relaxed">{line.text}</span>
                <span className={`shrink-0 font-mono text-2xs ${ocrConfClass(line.conf)}`}>
                  {(line.conf * 100).toFixed(0)}%
                </span>
              </div>
            ))}
          </div>
        </div>
      ) : null}

      {expanded && item.image_caption ? (
        // 展开态:配图视觉描述全文(metadata.image_caption)
        <div className="mt-1.5 flex flex-col gap-1" data-testid={`feed-image-caption-${rowKey}`}>
          <span className="text-2xs text-muted-foreground">配图描述(VL caption)</span>
          <p className="whitespace-pre-wrap break-words text-sm leading-relaxed text-foreground/90">
            {item.image_caption}
          </p>
        </div>
      ) : null}

      {expanded && (item.image_files?.length ?? 0) > 0 ? (
        // 展开态:落图文件路径文本列表(图片本尊显示属 v2.2,先以路径呈现)
        // TODO(v2.2): convertFileSrc 渲染本地图(内容寻址文件,安全 scope 待定)
        <div className="mt-1.5 flex flex-col gap-1" data-testid={`feed-image-files-${rowKey}`}>
          <span className="text-2xs text-muted-foreground">图文件 {item.image_files?.length} 张(路径)</span>
          <ul className="flex flex-col gap-0.5">
            {item.image_files?.map((path) => (
              <li key={path} className="break-all font-mono text-2xs text-muted-foreground">
                {path}
              </li>
            ))}
          </ul>
        </div>
      ) : null}

      {/* G8 AI 摘要回显:loading / done(复合分 + 模型 + 维度分 + 缓存命中)/
          错误(enrich_not_configured 等 graceful 明示,重按按钮即重试) */}
      {enrich.phase === "loading" ? (
        <p className="mt-1.5 text-2xs text-muted-foreground" data-testid={`feed-enrich-loading-${rowKey}`}>
          精评中…
        </p>
      ) : enrich.phase === "done" ? (
        <div className="mt-1.5 flex flex-col gap-1" data-testid={`feed-enrich-${rowKey}`}>
          <span className="flex flex-wrap items-center gap-1.5 text-2xs text-muted-foreground">
            <Badge variant="outline" className="shrink-0" title="AI 精评摘要(feed.enrich)">
              AI
            </Badge>
            精评 {enrich.result.score.toFixed(2)} · 模型 {enrich.result.model}
            <Badge variant="secondary" title="enrich_cache 命中 = 零 token">
              {enrich.result.cached ? "缓存命中" : "现跑"}
            </Badge>
          </span>
          <span className="flex flex-wrap items-center gap-1">
            {Object.entries(enrich.result.scores).map(([dimension, value]) =>
              typeof value === "number" ? (
                <Badge key={dimension} variant="outline" className="text-2xs">
                  {dimension} {value}
                </Badge>
              ) : null,
            )}
          </span>
        </div>
      ) : enrich.phase === "error" ? (
        <p
          className="mt-1.5 text-2xs text-warning"
          data-testid={`feed-enrich-error-${rowKey}`}
          title={`${enrich.code}:${enrich.message}`}
        >
          {enrich.code === "enrich_not_configured"
            ? `无精评配置:${enrich.message}(在品类 YAML enrich 节配置端点后重试)`
            : `精评失败(${enrich.code}):${enrich.message}`}
        </p>
      ) : null}

      {/* G12 沉淀为关键词:就地面板(目标清单 → 词面/目标 → 写入回执) */}
      {pin.phase !== "closed" ? (
        <div
          className="mt-1.5 flex flex-col gap-1.5 rounded-md border border-border/60 bg-muted/20 p-2"
          data-testid={`feed-keyword-pin-${rowKey}`}
        >
          <span className="flex items-center justify-between gap-2">
            <span className="text-2xs font-medium text-muted-foreground">沉淀为关键词(watchlist.keywords)</span>
            <Button
              variant="ghost"
              size="icon"
              className="size-5"
              aria-label="关闭沉淀面板"
              onClick={() => setPin({ phase: "closed" })}
            >
              <X className="size-3 text-muted-foreground" />
            </Button>
          </span>

          {pin.phase === "listing" ? (
            <p className="text-2xs text-muted-foreground" data-testid={`feed-keyword-listing-${rowKey}`}>
              载入品类 YAML 清单…
            </p>
          ) : pin.phase === "list_error" ? (
            <p className="flex items-center gap-2 text-2xs text-destructive" data-testid={`feed-keyword-list-error-${rowKey}`}>
              清单拉取失败:{pin.message}
              <Button variant="outline" size="sm" className="h-5 px-1.5 text-2xs" onClick={() => void openPin()}>
                重试
              </Button>
            </p>
          ) : (
            <div className="flex flex-col gap-1.5">
              <label className="flex flex-wrap items-center gap-1.5 text-2xs text-muted-foreground">
                关键词
                <input
                  type="text"
                  value={pinKeyword}
                  maxLength={KEYWORD_MAX_CHARS}
                  aria-label="沉淀关键词"
                  placeholder="来自条目标题,可改"
                  className="h-6 min-w-40 flex-1 rounded-md border border-border bg-background px-2 text-xs text-foreground placeholder:text-muted-foreground"
                  onChange={(event) => setPinKeyword(event.target.value)}
                  disabled={pin.phase === "writing"}
                />
              </label>
              <label className="flex flex-wrap items-center gap-1.5 text-2xs text-muted-foreground">
                目标 YAML
                <select
                  value={pinTarget}
                  aria-label="目标品类 YAML"
                  className="h-6 min-w-40 flex-1 rounded-md border border-border bg-background px-1.5 text-xs text-foreground"
                  onChange={(event) => setPinTarget(event.target.value)}
                  disabled={pin.phase === "writing" || pinFiles.length === 0}
                >
                  {pinFiles.length === 0 ? (
                    <option value="">无可解析品类 YAML</option>
                  ) : (
                    pinFiles.map((file) => (
                      <option key={file.file} value={file.file}>
                        {file.name}({file.category_name ?? file.category_id ?? "?"})
                      </option>
                    ))
                  )}
                </select>
              </label>
              <Button
                variant="outline"
                size="sm"
                className="w-fit"
                onClick={() => void writeKeyword()}
                disabled={pin.phase === "writing" || pinFiles.length === 0}
                title="yaml.read → watchlist.keywords 原文手术 → yaml.save(mtime 乐观锁 + 跨文件 id 查重)"
              >
                {pin.phase === "writing" ? "写入中…" : "写入"}
              </Button>
              {pin.phase === "note" ? (
                <p
                  className={`text-2xs ${pin.kind === "error" ? "text-destructive" : "text-muted-foreground"}`}
                  data-testid={`feed-keyword-note-${rowKey}`}
                >
                  {pin.message}
                </p>
              ) : null}
            </div>
          )}
        </div>
      ) : null}
        </div>
      </ContextMenuTrigger>
      {/* 右键菜单四动作(A-feed):打开原文/复制链接同「打开原文」URL 门
          (isOpenableUrl,非 http(s) 禁用);标已读 = 既有 toggle;沉淀 =
          直调卡内 openPin(G12 就地面板本尊零改)。 */}
      <ContextMenuContent>
        <ContextMenuItem
          disabled={!openable}
          onSelect={() =>
            void openInBrowser(item.url).catch((err) =>
              onOpenError(err instanceof Error ? err.message : String(err)),
            )
          }
        >
          打开原文
        </ContextMenuItem>
        <ContextMenuItem disabled={!openable} onSelect={() => copyLink(item.url)}>
          复制链接
        </ContextMenuItem>
        <ContextMenuItem onSelect={() => onToggle(item, "read")}>
          {state.read ? "标记未读" : "标记已读"}
        </ContextMenuItem>
        <ContextMenuSeparator />
        <ContextMenuItem onSelect={() => void openPin()}>沉淀为关键词…</ContextMenuItem>
      </ContextMenuContent>
    </ContextMenu>
  );
}

/** TG 渠道卡(10-08-tg-channel-card,主人令「渠道单独一个卡片,点击进去才是
 *  详情」):流内按渠道聚合的摘要卡,聊天列表形态 —— 频道名 + 最新一条预览 +
 *  条数/未读 + 最新相对时间;未读 >0 带左缘 accent 竖条(与消息卡未读竖条
 *  同语言)。点击进该渠道 source 作用域消息流(详情本体,气泡逐条)。 */
function TgChannelCard({
  card,
  onOpen,
}: {
  card: TelegramChannelCardData;
  onOpen: () => void;
}) {
  const time = formatRelativeTime(card.latest.first_seen);
  const preview = (card.latest.title || card.latest.url).replace(/\s+/g, " ").trim();
  const digest = cardDigest(card.latest);
  return (
    <button
      type="button"
      data-testid={`feed-tg-channel-card-${card.key}`}
      onClick={onOpen}
      className="group/tg-card relative w-full overflow-hidden rounded-md border border-border bg-card px-3 py-2.5 text-left transition-colors duration-(--duration-fast) ease-out-expo hover:border-primary/40 hover:bg-accent/40"
      title={`打开 ${card.label} 的消息流:${card.count} 条 · 未读 ${card.unread}(口径 = 当前视图 ∪ 当日窗可见条目)`}
    >
      {card.unread > 0 ? (
        <span aria-hidden data-testid={`feed-tg-channel-unread-${card.key}`} className="absolute top-2 bottom-2 left-0 w-0.5 rounded-full bg-[#9869f7]" />
      ) : null}
      <span className="flex items-center gap-1.5">
        <Send aria-hidden className="size-3.5 shrink-0 text-primary" />
        <span className="min-w-0 truncate text-sm font-medium text-foreground">{card.label}</span>
        <time
          dateTime={card.latest.first_seen ?? undefined}
          className="ml-auto shrink-0 font-mono text-2xs text-muted-foreground"
        >
          {time}
        </time>
      </span>
      <span className="mt-0.5 block truncate text-sm leading-relaxed text-muted-foreground">{preview}</span>
      {digest !== null ? (
        <span
          className="mt-0.5 block truncate text-2xs leading-relaxed text-muted-foreground"
          data-testid={`feed-tg-channel-digest-${card.key}`}
        >
          {digest}
        </span>
      ) : null}
      <span className="mt-1 flex items-center gap-1.5 text-2xs text-muted-foreground">
        {card.count} 条{card.unread > 0 ? ` · 未读 ${card.unread}` : ""}
        <ChevronRight
          aria-hidden
          className="ml-auto size-3.5 shrink-0 text-muted-foreground/70 transition-transform duration-(--duration-fast) ease-out-expo group-hover/tg-card:translate-x-0.5"
        />
      </span>
    </button>
  );
}

/**
 * TG 分节节头(10-08 审计 F3):通讯软件详情层的节头退化版 —— 频道名 +
 * 条数/未读 + chevron 的细条,去 preview/digest 大卡形制。此前节头卡复用
 * TgChannelCard(带最新条目预览/摘要),与节内首条气泡背靠背重复同一消息,
 * 看似两条消息;细条与消息卡拉开视觉档位,点击进单频道过滤的动线不变
 * (testid 沿用 feed-tg-channel-card-*,面包屑/键盘语义零变化)。
 */
function TgSectionHeader({
  card,
  onOpen,
}: {
  card: TelegramChannelCardData;
  onOpen: () => void;
}) {
  return (
    <button
      type="button"
      data-testid={`feed-tg-channel-card-${card.key}`}
      onClick={onOpen}
      className="group/tg-head flex w-full items-center gap-2 rounded-md border border-transparent px-2 py-1 text-left transition-colors duration-(--duration-fast) ease-out-expo hover:border-border hover:bg-accent/40"
      title={`打开 ${card.label} 的消息流:${card.count} 条 · 未读 ${card.unread}`}
    >
      <span aria-hidden className="flex size-7 shrink-0 items-center justify-center rounded-full bg-primary/15">
        <Send className="size-3.5 text-primary" />
      </span>
      <span className="min-w-0 truncate text-sm font-medium text-foreground">{card.label}</span>
      <span className="ml-auto shrink-0 font-mono text-2xs text-muted-foreground">
        {card.count} 条{card.unread > 0 ? ` · 未读 ${card.unread}` : ""}
      </span>
      <ChevronRight
        aria-hidden
        className="size-3.5 shrink-0 text-muted-foreground/70 transition-transform duration-(--duration-fast) ease-out-expo group-hover/tg-head:translate-x-0.5"
      />
    </button>
  );
}

/** 源大类卡(10-08-tg-channel-card v2,主人令「网页集中在一起,其他通讯软件
 *  一个通讯软件一个卡片,点击进入第二层才是详情展示」):L3 多渠道作用域
 *  第一层的卡片墙本体 —— 网页一张(Globe)/ 每通讯软件一张(Telegram =
 *  Send),散条目卡不再出现在第一层;点击进第二层详情(网页 = 条目平铺,
 *  通讯软件 = 按频道分节全铺)。形制与 TgChannelCard 同语言(未读竖条/
 *  最新预览/计数/chevron)。
 *
 *  10-08 审计追加:F2 计数口径注记(hasMore 时「已加载 N 条」+ title 补
 *  「首页 50 截断」,与 L1 行 title 同门,不再静默低估);F5 键盘巡游
 *  (墙卡带 data-item-key/data-nav-focused 入 j/k 巡游集,U/Enter 进详情);
 *  F10 墙卡内次级概览行(大类内 top3 源,streamKindSubRows 复用聚合)。 */
function SourceKindCard({
  card,
  onOpen,
  truncated = false,
  subRows = [],
  navFocused = false,
  onCurrent,
}: {
  card: StreamKindCardData;
  onOpen: () => void;
  /** 计数口径注记(F2):true = 可见条目只是已加载首页(FEED_PAGE_SIZE 截断),
   *  词面改「已加载 N 条」+ title 注记,不再以全量词面静默低估 */
  truncated?: boolean;
  /** 次级概览行(F10):大类内 top3 源(名称/条数/未读) */
  subRows?: StreamKindSubRow[];
  /** j/k 键盘巡游聚焦(F5):focus 环呈现与否 */
  navFocused?: boolean;
  /** hover/focus 进入 = 置键盘「当前卡」(F5 巡游集口径) */
  onCurrent?: () => void;
}) {
  const time = formatRelativeTime(card.latest.first_seen);
  const preview = (card.latest.title || card.latest.url).replace(/\s+/g, " ").trim();
  const Icon = card.key === "im" ? Send : Globe;
  const digest = cardDigest(card.latest);
  return (
    <button
      type="button"
      data-testid={`feed-kind-card-${card.key}`}
      data-item-key={`kind:${card.key}`}
      data-nav-focused={navFocused ? "true" : "false"}
      onMouseEnter={onCurrent}
      onFocus={onCurrent}
      onClick={onOpen}
      className={`group/kind-card relative w-full overflow-hidden rounded-md border border-border bg-card px-3 py-2.5 text-left transition-colors duration-(--duration-fast) ease-out-expo hover:border-primary/40 hover:bg-accent/40${navFocused ? " ring-1 ring-primary/60" : ""}`}
      title={`打开「${card.label}」详情:${card.count} 条 · 未读 ${card.unread}(口径 = 当前视图 ∪ 当日窗可见条目${truncated ? `;首页 ${FEED_PAGE_SIZE} 条截断,更早条目未计入` : ""})`}
    >
      {card.unread > 0 ? (
        <span aria-hidden data-testid={`feed-kind-card-unread-${card.key}`} className="absolute top-2 bottom-2 left-0 w-0.5 rounded-full bg-[#9869f7]" />
      ) : null}
      <span className="flex items-center gap-1.5">
        <Icon aria-hidden className="size-3.5 shrink-0 text-primary" />
        <span className="min-w-0 truncate text-sm font-medium text-foreground">{card.label}</span>
        <time
          dateTime={card.latest.first_seen ?? undefined}
          className="ml-auto shrink-0 font-mono text-2xs text-muted-foreground"
        >
          {time}
        </time>
      </span>
      <span className="mt-0.5 block truncate text-sm leading-relaxed text-muted-foreground">{preview}</span>
      {digest !== null ? (
        <span
          className="mt-0.5 block truncate text-2xs leading-relaxed text-muted-foreground"
          data-testid={`feed-kind-digest-${card.key}`}
        >
          {digest}
        </span>
      ) : null}
      <span className="mt-1 flex items-center gap-1.5 text-2xs text-muted-foreground">
        {truncated ? `已加载 ${card.count} 条` : `${card.count} 条`}
        {card.unread > 0 ? ` · 未读 ${card.unread}` : ""}
        <ChevronRight
          aria-hidden
          className="ml-auto size-3.5 shrink-0 text-muted-foreground/70 transition-transform duration-(--duration-fast) ease-out-expo group-hover/kind-card:translate-x-0.5"
        />
      </span>
      {/* 次级概览行(F10):大类内谁在出料(top3 源 + 条数/未读) */}
      {subRows.length > 0 ? (
        <span
          className="mt-1 flex flex-col gap-0.5 border-t border-border/50 pt-1"
          data-testid={`feed-kind-subs-${card.key}`}
        >
          {subRows.map((row) => (
            <span key={row.key} className="flex items-center gap-1.5 text-2xs text-muted-foreground">
              <span aria-hidden className="size-1 shrink-0 rounded-full bg-muted-foreground/60" />
              <span className="min-w-0 truncate">{row.label}</span>
              <span className="ml-auto shrink-0 font-mono tabular-nums">
                {row.count}
                {row.unread > 0 ? ` · 未读 ${row.unread}` : ""}
              </span>
            </span>
          ))}
        </span>
      ) : null}
    </button>
  );
}

/**
 * 消息详情弹窗(主人令「点击信息,弹出详情」,10-08):标题全文 + 元信息簇
 * (来源渠道/品类/时间/精评评分/图析)+ 正文与图析全文 + 动作簇(👍👎 反馈
 * 复用 FeedCardFeedback,打开原文/复制链接/星标/稍后读/已读切换复用卡内
 * 既有实现)。Esc 与遮罩点击关闭由 ui/dialog.tsx 基件承担;「展开条目」
 * 内联路径并存不废(卡内就地展开仍是正文快读路径)。
 */
function FeedItemDetail({
  item,
  state,
  kind,
  onClose,
  onToggle,
  onOpenError,
}: {
  item: FeedItem;
  state: { read?: boolean; starred?: boolean; later?: boolean };
  kind: ChannelKind;
  onClose: () => void;
  onToggle: (item: FeedItem, marker: "starred" | "later" | "read") => void;
  onOpenError: (message: string) => void;
}) {
  const score = primaryScore(item);
  const color = categoryColor(item.category);
  const openable = isOpenableUrl(item.url);
  const kindMeta = CHANNEL_KIND_META[kind];
  const KindIcon = kindMeta.Icon;
  return (
    <Dialog open onOpenChange={(next) => { if (!next) onClose(); }}>
      <DialogContent className="max-w-xl gap-3" data-testid="feed-detail-dialog">
        <DialogHeader>
          {/* 标题全文(卡面 truncate 的反面:弹窗内不截断) */}
          <DialogTitle
            className="pr-6 text-base leading-relaxed break-words whitespace-pre-wrap"
            data-testid="feed-detail-title"
          >
            {item.title || item.url}
          </DialogTitle>
          {/* 元信息簇:来源渠道(词表名)+ 品类 + 时间(相对+绝对 title)+
              精评评分 + 图析在场徽标 */}
          <div
            className="flex flex-wrap items-center gap-1.5 text-2xs text-muted-foreground"
            data-testid="feed-detail-meta"
          >
            <span className="inline-flex items-center gap-1">
              <KindIcon aria-hidden className={`size-3 shrink-0 ${kindMeta.className}`} />
              {channelDisplayName(item.source)}
            </span>
            {item.category && color ? (
              <span
                className="inline-flex w-fit shrink-0 items-center justify-center rounded-sm border px-1.5 py-0.5 text-2xs font-medium"
                style={{ color, backgroundColor: `${color}14`, borderColor: `${color}59` }}
              >
                {item.category}
              </span>
            ) : item.category ? (
              <Badge variant="secondary">{item.category}</Badge>
            ) : null}
            <time
              dateTime={item.first_seen ?? undefined}
              title={`首见 ${formatAbsoluteTime(item.first_seen)}`}
              className="font-mono"
            >
              {formatRelativeTime(item.first_seen)}
            </time>
            {item.pushed_at ? (
              <span title={`已推送 ${formatAbsoluteTime(item.pushed_at)}`}>
                推送 {formatRelativeTime(item.pushed_at)}
              </span>
            ) : null}
            {score !== null ? (
              <Badge variant="default" className="border-primary/40 font-mono tabular-nums" title="精评分数(维度最高分)">
                {score.toFixed(2)}
              </Badge>
            ) : null}
            {hasImageDetails(item) ? (
              <Badge variant="outline" title="图析:配图 OCR/图说全文在下方">
                图
              </Badge>
            ) : null}
          </div>
        </DialogHeader>
        {/* 正文(去标题重复开头,10-08 验收「标题下正文首段再次复述」;
            正文整段 = 标题时零渲染;超高内滚不 line-clamp) */}
        {(() => {
          const body = bodyWithoutTitleDup(item);
          return body !== null ? (
            <p
              className="max-h-72 overflow-y-auto whitespace-pre-wrap break-words text-sm leading-relaxed text-foreground/90"
              data-testid="feed-detail-content"
            >
              {body}
            </p>
          ) : null;
        })()}
        {/* 图析全文:OCR 全文 + VL 图说(10-03-vision-v2 同一套字段) */}
        {item.image_ocr ? (
          <div className="flex flex-col gap-1" data-testid="feed-detail-ocr">
            <span className="text-2xs text-muted-foreground">配图 OCR 全文</span>
            <pre className="max-h-56 overflow-y-auto whitespace-pre-wrap break-words rounded-md border border-border/60 bg-muted/30 px-2.5 py-2 font-mono text-xs leading-relaxed text-foreground/90">
              {item.image_ocr}
            </pre>
          </div>
        ) : null}
        {item.image_caption ? (
          <div className="flex flex-col gap-1" data-testid="feed-detail-caption">
            <span className="text-2xs text-muted-foreground">配图描述(VL caption)</span>
            <p className="whitespace-pre-wrap break-words text-sm leading-relaxed text-foreground/90">
              {item.image_caption}
            </p>
          </div>
        ) : null}
        {/* 动作簇(复用卡内既有实现;10-08 验收权重理顺):打开原文 = 唯一
            实底主钮(品牌紫大面积底 = F1 保留档),其余全 ghost 同档次 ——
            👍👎 反馈 / 复制链接 / 星标 / 稍后读 / 已读切换 */}
        <div
          className="flex flex-wrap items-center gap-1.5 border-t border-border/60 pt-3"
          data-testid="feed-detail-actions"
        >
          <FeedCardFeedback item={item} />
          {openable ? (
            <Button
              variant="default"
              size="sm"
              onClick={() =>
                void openInBrowser(item.url).catch((err) =>
                  onOpenError(err instanceof Error ? err.message : String(err)),
                )
              }
            >
              <ExternalLink className="size-3.5" />
              打开原文
            </Button>
          ) : null}
          <Button variant="ghost" size="sm" onClick={() => copyLink(item.url)}>
            <Copy className="size-3.5" />
            复制链接
          </Button>
          <Button
            variant="ghost"
            size="sm"
            aria-pressed={state.starred === true}
            onClick={() => onToggle(item, "starred")}
          >
            <Star className={state.starred ? "size-3.5 fill-warning text-warning" : "size-3.5"} />
            星标
          </Button>
          <Button
            variant="ghost"
            size="sm"
            aria-pressed={state.later === true}
            title={
              state.later
                ? `稍后读中:超过 ${LATER_RESURFACE_DAYS} 天自动回到未读;再点取消`
                : `放入稍后读;超过 ${LATER_RESURFACE_DAYS} 天自动回到未读`
            }
            onClick={() => onToggle(item, "later")}
          >
            <Bookmark className={state.later ? "size-3.5 fill-primary text-primary" : "size-3.5"} />
            稍后读
          </Button>
          <Button
            variant="ghost"
            size="sm"
            aria-pressed={state.read === true}
            title="弹开详情即记已读;此钮在已读/未读间切换(误开撤销口)"
            onClick={() => onToggle(item, "read")}
          >
            <Inbox className="size-3.5" />
            {state.read ? "标记未读" : "标记已读"}
          </Button>
        </div>
      </DialogContent>
    </Dialog>
  );
}

/**
 * 情报流:条目卡片列表 + 未读/星标/稍后读三态(本地态,localStorage 持久)
 * + 游标分页加载(见 ./api 的协议缺口注记)+ 服务端搜索(G1,防抖/Enter
 * 提交,query 随游标透传)+ 屏内品类下拉服务端过滤(10-04-topbar-cleanup
 * 归位)+ 卡片展开/打开原文(G2)+ 导出当前视图(G3,dialog.save → feed.export)。
 *
 * D4 结构性重做(10-03-ui-deep-imitation,对标 teardown-linear-activity
 * #4/#5/#6/#11):三级信息密度(13px 标题/正文 + 11px 元信息)、品类色条、
 * 分组时间轴(今天/昨天/7 天内/更早,sticky 组头)、hover 浮现操作簇 +
 * 行背景 accent/50、未读 accent 竖条 + U 快捷键、空/载/错三态按
 * frontend-ui-engineering(贴形骨架/带重试错误卡/EmptyState)。
 *
 * fe-small-batch(10-03-fe-small-batch):G8 卡片「AI 摘要」(feed.enrich 单条
 *  精评,loading/错误态,无配置 graceful 明示)/ G9 过滤区批量操作(全部标
 *  已读/未读,计数同步)/ G12 卡片「沉淀为关键词」(yaml.read → watchlist
 *  文本手术 → yaml.save,mtime 乐观锁 + 跨文件 id 查重);P2⑤ 搜索框焦点环
 *  归 index.css 全局 :focus-visible 体系(不再局部 ring-1 覆写)。
 *
 * interaction-batch(10-04,A-feed):j/k 键盘导航(扩既有 U 键 effect 同守卫,
 *  边界钳制 + scrollIntoView 最近侧 + focus 环仅键盘巡游时呈现)/ 显示选项
 *  下拉(未读优先 + 分组维度 时间/品类/不分组,myssia.feed.display.v1 本地
 *  持久)/ 卡片右键上下文菜单(打开原文/复制链接/标已读切换/沉淀为关键词,
 *  基件 ui/context-menu.tsx 本批自建)。
 *
 * read-state-server(10-04,G9 后半):已读/星标/稍后读迁服务端 —— 能力门
 *  (挂载一次 api.version,protocol ≥ READ_STATE_PROTOCOL)分流:过门走
 *  store.state.*(单键 mark 乐观 + 失败回滚;「全部标已读/未读」= mark_all
 *  全库语义,title 换真话,就地翻转不整页重拉)+ 首启 localStorage 一次性
 *  搬迁(importLocalFeedStates,旧键保留不删);未过门(旧 sidecar 配新 UI)
 *  旧 localStorage 通路原样保留,零行为变化。
 *
 * g9-read-all(10-04,R1/R2/R4):品类分组组头「本组全部已读」(mark_all 带
 *  category 精确等值 = 该品类全库含未翻页;未分类组不出钮 —— null 传
 *  category 等于全库置位,红线;时间/不分组无组头入口)+ 全库两按钮 inline
 *  二次确认(一次点击进确认态,再点执行;Esc/失焦/「取消」退出;品类组头
 *  钮豁免确认 —— 作用域小一级,title 如实)。
 *
 * fe-gap-census R1(10-04):Mod+F 聚焦内联搜索框(拦截浏览器查找并全选
 *  词面)+ Esc 即时清空(词面与已提交 query 同步归零,不等 300ms 防抖)。
 *
 * topbar-cleanup 归位(10-04):品类过滤从全局顶栏拆下自建 —— 屏内品类下拉
 *  (词汇源 health().plugins,value = 品类 id 与 store.items 精确等值,
 *  「全部品类」= null 不传参;不再吃 Outlet context)+ 工具条一行收纳
 *  (KsFilter 范式,同源管理/日志工具行:品类下拉 + 读态分段 + 计数/批量 +
 *  右侧显示选项/搜索/刷新,置于列表头部;刷新自页头迁入工具条图标位)。
 *
 * feed-channel-groups(10-06,主人令「情报流也要分渠道」+「不同渠道表现的
 *  方式不一样」):品类分组下再按渠道(items.source 源名全称)二级分组,
 *  渠道类型五档差异化呈现 —— telegram-* 消息卡(聊天感气泡+频道名+时间)/
 *  RSS 新闻标题列表(现状)/ engine urlwatch 变更事件(「有更新」徽标+
 *  目标页链接 watch_page)/ engine prompt·store_report 日报(markdown 文档
 *  视图,MarkdownLite 可折叠正文)/ 游戏·羊毛价格优惠行(现价突出+原价
 *  划线+折扣/限免徽标;价格键 = _item_dict 白名单投影,entry.py)。
 *
 * feed-channel-groups 追加(10-06,主人令「情报流要不停地过信息日志,每天
 *  凌晨 3 点清零,继续过滤」):实时滚动视图 —— completed / cron.completed
 *  事件即时刷新 + 30s 可见性轮询兜底(隐藏暂停;mergeFreshItems 前插新键,
 *  已加载行与游标零扰动);每日 03:00 清零 = 视图层当日窗(03:00 → 次日
 *  03:00,窗口锚写死),滚动流(未读/全部)过窗离场、视图从零累计,
 *  store 数据不动(retention 照旧),星标/稍后读与 later 到期重现跨窗可见。
 *
 * tg-channel-card(10-08,主人令「TG 渠道要单独做界面……要单独一个卡片,
 *  点击进去才是详情」+ 拍板「情报流这个界面上面都放置这种卡片渠道」/「只
 *  TG」):多渠道作用域流(全部条目/品类流)中 telegram 条目按渠道聚合为
 *  置顶渠道卡区(TgChannelCard:频道名 + 最新一条预览 + 条数/未读 + 未读
 *  accent 竖条;计数口径 = 当前过滤视图 ∪ 当日窗可见条目,title 注记),
 *  TG 消息卡不再逐条进流(时间分组/平铺吃 streamItems,组头计数如实);
 *  点卡进该渠道 source 作用域消息流(详情本体零变化),面包屑增「全部条目」
 *  中间层一键回流(category=null 时原 backToL2 只能落 L1,动线断裂);
 *  j/k 巡游与 U 键吃 streamItems(不落未渲染卡);全 TG 流不误现空态
 *  (空态门仍按 visible,渠道卡区在 ternary 之前独立呈现)。聚合纯函数
 *  telegramChannelCards / 展示词 channelDisplayName 收编 api.ts。
 *
 * tg-channel-card v2.1(10-08,主人令「点击信息,弹出详情」+ 审计 F1-F10
 *  逐项整改):消息详情弹窗(FeedItemDetail,标题全文+元信息簇+动作簇,
 *  复用卡内动作实现;Esc/遮罩关闭走 ui/dialog.tsx 基件;弹开即记已读,
 *  「展开条目」内联路径并存)/ F1 文字档全走 --link(品牌紫只留按钮底/
 *  焦点环/竖条等非文字件)/ F2 hasMore 时「已加载 N 条」词面 + 墙卡截断
 *  注记 / F3 TG 节头退化细条(去 preview/digest 重复形制)/ F4 已读降档
 *  (标题 muted + 竖条统一降饱和灰)/ F5 墙卡入 j/k 巡游集(U/Enter 进
 *  详情)/ F6 streamTitle 可见化 + 面包屑终端段 / F7 协议词出 tooltip /
 *  F8 品类色板避语义色域且全档过 4.5:1 / F9 源名词表一词一源 / F10 墙卡
 *  内 top3 源次级概览(streamKindSubRows)。
 */
export function FeedScreen() {
  const navigate = useNavigate();
  /** 三级下钻(10-06-feed-channel-groups 主人令「二级界面分类,一层一层
   *  点击进去」):L1 品类列表(挂载缺省)→ L2 渠道列表 → L3 消息流(分型
   *  呈现主场)。L3 作用域 = {category, source}(可空 = 全部);查询走
   *  store.items category+source 精确等值 + 游标;返回经面包屑。 */
  const [drill, setDrill] = useState<
    | { level: 1 }
    | { level: 2; category: string }
    | {
        level: 3;
        category: string | null;
        source: string | null;
        /** 源大类作用域(10-08-tg-channel-card v2,仅过 SOURCE_KIND_PROTOCOL
         *  门时有值):null = 卡片墙第一层;web = 网页详情;im = 通讯软件
         *  详情(source=null 分节全铺 / source=单频道过滤)。 */
        kind: "web" | "im" | null;
        /** 含历史态(10-09-tg-category-entry,监控台入口):绕过当日窗,
         *  展示该作用域全部入库条目(监控台「看全部历史消息」专用)。 */
        history: boolean;
      }
  >({ level: 1 });
  /** 源大类能力门(10-08-tg-channel-card v2):protocol ≥ SOURCE_KIND_PROTOCOL
   *  = sidecar 三方法支持 source_kind → L3 走卡片墙;未过门 = v1 形态原样
   *  (TG 频道卡区 + 消息列表)。与 serverStateReady 同一次 version 调用合流。 */
  const [sourceKindReady, setSourceKindReady] = useState(false);
  /** L3 查询作用域(drill 派生;L1/L2 = 全局首页,计数源)。kind 仅在过门
   *  且未定源时随参(source 精确等值视图不需要大类过滤)。 */
  const streamScope =
    drill.level === 3
      ? {
          category: drill.category,
          source: drill.source,
          sourceKind:
            sourceKindReady && drill.source === null ? (drill.kind ?? null) : null,
        }
      : { category: null, source: null, sourceKind: null };
  /** 下钻作用域键(refresh/loadMore/liveRefresh 依赖;变化即重查) */
  const scopeKey =
    drill.level === 3 ? `3:${drill.category ?? "*"}:${drill.source ?? "*"}:${drill.kind ?? "*"}` : "root";
  /** 品类下拉选项(health().plugins 派生,挂载一次;L1 品类列表词汇源) */
  const [categoryOptions, setCategoryOptions] = useState<FeedCategoryOption[]>([]);
  /** 源名→engine 映射(10-06-feed-channel-groups:渠道类型判定的词表源;
   *  同一次 health 调用顺带装配,零新 RPC;health 失败 = 空映射,渠道判定
   *  退化为前缀+品类+字段三级) */
  const [engineBySource, setEngineBySource] = useState<Map<string, string>>(new Map());
  const [items, setItems] = useState<FeedItem[]>([]);
  /** 未过门通路的本地态(localStorage 持久;过门后状态源 = 条目派生,不再读写) */
  const [localStates, setLocalStates] = useState<FeedStateMap>({});
  const [filter, setFilter] = useState<FeedFilter>("unread");
  /** A-feed 显示选项:未读优先 + 分组维度(本地持久,进屏 loadFeedDisplay 回填) */
  const [display, setDisplay] = useState<FeedDisplayOptions>(DEFAULT_FEED_DISPLAY);
  const [cursor, setCursor] = useState<string | null>(null);
  /** 复合游标第二键(同刻条目翻页不跳不重;C1) */
  const [cursorId, setCursorId] = useState<number | null>(null);
  const [hasMore, setHasMore] = useState(false);
  const [loading, setLoading] = useState(true);
  const [loadingMore, setLoadingMore] = useState(false);
  const [error, setError] = useState<SidecarRequestError | null>(null);
  /** health.first_run:空流时区分「无插件(首跑初始化)」与「有插件未采集」 */
  const [firstRun, setFirstRun] = useState(false);
  const [cta, setCta] = useState<RunCtaState>({ phase: "idle" });
  /** G1 搜索:输入框即时值 / 已提交值(防抖 300ms 或 Enter) */
  const [searchInput, setSearchInput] = useState("");
  const [query, setQuery] = useState("");
  /** Mod+F 聚焦目标(fe-gap-census R1:⌘F/Ctrl+F 拦截浏览器查找改聚内联搜索框) */
  const searchInputRef = useRef<HTMLInputElement>(null);
  /** G3 导出:格式选择 + 进行中 + 回显;G2 打开原文失败回显 */
  const [exportFormat, setExportFormat] = useState<ExportFormat>("jsonl");
  const [exporting, setExporting] = useState(false);
  const [exportNote, setExportNote] = useState<string | null>(null);
  const [openError, setOpenError] = useState<string | null>(null);
  /** G9 读态置位失败回显(服务端通路;失败即回滚,本行如实告知,惯例同 openError) */
  const [markError, setMarkError] = useState<string | null>(null);
  /** G9·R2 全库批量二次确认:inline confirm(settings 先例)—— null = 无;
   *  "read" / "unread" = 对应方向待确认(一次点击进入确认态,再点「确认」
   *  才执行;Esc / 失焦 / 「取消」退出)。品类组头钮豁免(作用域小一级,
   *  即时执行 + title 如实)。 */
  const [confirmAllMark, setConfirmAllMark] = useState<"read" | "unread" | null>(null);
  /** L1 闲置品类折叠(10-09-tg-category-entry,主人令零计数行降噪):缺省收起 */
  const [idleOpen, setIdleOpen] = useState(false);
  const [tgWebline, setTgWebline] = useState<TelegramStatus | null>(null);
  const [tgLoginBusy, setTgLoginBusy] = useState(false);

  /** G9 能力门:null = 探测中(按未过门处理,走旧通路);true = sidecar
   *  protocol ≥ READ_STATE_PROTOCOL → 服务端读态通路。直调 api.version,
   *  失败即未过门(design §5.1,不引入全局 hook 依赖)。 */
  const [serverStateReady, setServerStateReady] = useState<boolean | null>(null);
  const useServerState = serverStateReady === true;

  /** 请求序号守卫(深审 F2):流查询(refresh/liveRefresh/loadMore)每次
   *  发包取新票,应答落地前对票 —— 旧应答(慢回包/切作用域后在途的旧域
   *  包)一律丢弃:旧 refresh 覆盖掉 liveRefresh 已并入的新行、旧域
   *  liveRefresh 把全局行混进品类/渠道流,两类竞态一并钉死。 */
  const feedSeqRef = useRef(0);
  const nextFeedSeq = useCallback(() => {
    feedSeqRef.current += 1;
    return feedSeqRef.current;
  }, []);
  /** L1/L2 概览查询的独立对票(与流查询互不失效:概览慢回包不废流,反之亦然)。 */
  const overviewSeqRef = useRef(0);

  useEffect(() => {
    setLocalStates(loadFeedStates());
    setDisplay(loadFeedDisplay());
  }, []);

  // 品类下拉选项 + 源名→engine 映射(挂载一次):health().plugins → id 去重
  // + 名称回显(同旧顶栏纪律)+ sources[].name→engine(渠道类型判定词表源,
  // 10-06-feed-channel-groups);失败静默收敛为仅「全部品类」+ 空映射 —— 不拦
  // 情报流,选中过滤自然空态,渠道判定退化前缀+品类+字段
  useEffect(() => {
    let cancelled = false;
    void api
      .health()
      .then((health) => {
        if (!cancelled) {
          setCategoryOptions(categoryOptionsFromHealth(health.plugins));
          setEngineBySource(engineMapFromHealth(health.plugins));
        }
      })
      .catch(() => {
        if (!cancelled) setCategoryOptions([]);
      });
    return () => {
      cancelled = true;
    };
  }, []);

  /** 当日窗(10-06 追加:凌晨 3 点清零的**视图层**当日窗;store 数据不动,
   *  retention 照旧)。60s 滴答跟随:跨越 03:00 时 windowStart 前移,旧窗
   *  条目自然离场 = 视图重新从零累计;滚动流(未读/全部)受窗,星标/稍后
   *  读与 later 到期重现条目是显式留存,跨窗可见。 */
  const [windowStart, setWindowStart] = useState(() => dayWindowStart());
  useEffect(() => {
    const timer = window.setInterval(() => setWindowStart(dayWindowStart()), 60_000);
    return () => window.clearInterval(timer);
  }, []);

  // 能力门探测(挂载一次):低版本/探测失败 → false(旧 localStorage 通路);
  // 同一次应答顺带置源大类门(10-08-tg-channel-card v2,零新 RPC)
  useEffect(() => {
    let cancelled = false;
    void api
      .version()
      .then((info) => {
        if (!cancelled) {
          const protocol = typeof info?.protocol === "number" ? info.protocol : -1;
          setServerStateReady(protocol >= READ_STATE_PROTOCOL);
          setSourceKindReady(protocol >= SOURCE_KIND_PROTOCOL);
        }
      })
      .catch(() => {
        if (!cancelled) {
          setServerStateReady(false);
          setSourceKindReady(false);
        }
      });
    return () => {
      cancelled = true;
    };
  }, []);

  // 防抖提交(G1):输入停顿 300ms → query(触发服务端重查);Enter 即时
  useEffect(() => {
    const next = searchInput.trim();
    if (next === query) return;
    const timer = setTimeout(() => setQuery(next), SEARCH_DEBOUNCE_MS);
    return () => clearTimeout(timer);
  }, [searchInput, query]);

  const refresh = useCallback(async () => {
    const seq = nextFeedSeq();
    setLoading(true);
    setError(null);
    try {
      const page = await fetchFeedPage({
        cursor: null,
        cursorId: null,
        category: streamScope.category,
        source: streamScope.source,
        sourceKind: streamScope.sourceKind,
        query,
      });
      if (seq !== feedSeqRef.current) return; // F2:旧应答丢弃( newer 包已在途/已落地)
      setItems(page.items);
      setCursor(page.nextCursor);
      setCursorId(page.nextCursorId);
      setHasMore(page.hasMore);
      if (page.items.length === 0) {
        // 空结果才追问 health(一次 RPC):空态文案按有无插件分叉
        try {
          setFirstRun((await api.health()).first_run ?? false);
        } catch {
          // health 失败不遮蔽情报流自身的空态;CTA 点击时还有一次兜底
        }
      }
    } catch (err) {
      if (seq !== feedSeqRef.current) return; // F2:旧域错误不污染新作用域
      setError(
        err instanceof SidecarRequestError
          ? err
          : new SidecarRequestError({ code: "transport_error", path: "$", message: String(err) }),
      );
    } finally {
      // loading 无条件清:守卫化会把 loading 卡死在更晚的 liveRefresh 票上
      setLoading(false);
    }
    // 依赖含 scopeKey:下钻/回退切换作用域即重查(L3-all 与 L1 同参,重查幂等)
  }, [streamScope.category, streamScope.source, scopeKey, query, nextFeedSeq]);

  useEffect(() => {
    void refresh();
  }, [refresh]);

  /** L1/L2 概览数据(深审 F1):按品类查询的首页页 —— store.items 带
   *  category 游标(每品类一页 50,勿全量拉),L1 行计数与 L2 渠道列表的
   *  真数据源。此前两者只吃全局首页 50 条:长尾品类/渠道的全部条目落在
   *  全局首页之外 = 假空态/假零计数(下钻进去明明有货)。查询不带 query
   *  (L1/L2 是当日窗概览,搜索词只属 L3 流)。 */
  const [categoryPages, setCategoryPages] = useState<Record<string, FeedItem[]>>({});
  /** 概览词表键(稳定字符串):health 选项 ∪ 全局页条目品类 —— 词表外
   *  品类(插件已卸/改名遗留数据)也出行,零计数如实(旧 L1 行为对齐)。
   *  join 成串做依赖:字符串值比较,items 身份每轮刷新不触发概览重查。 */
  const overviewCategoryKey = useMemo(() => {
    const ids = new Set(categoryOptions.map((option) => option.id));
    for (const item of items) {
      if (item.category != null) ids.add(item.category);
    }
    return [...ids].sort().join("\n");
  }, [categoryOptions, items]);
  const refreshOverview = useCallback(async () => {
    if (overviewCategoryKey === "") return;
    overviewSeqRef.current += 1;
    const seq = overviewSeqRef.current;
    const ids = overviewCategoryKey.split("\n");
    const settled = await Promise.allSettled(
      ids.map((id) => fetchFeedPage({ cursor: null, cursorId: null, category: id, query: null })),
    );
    if (seq !== overviewSeqRef.current) return; // F2 同款对票:旧概览包丢弃
    const next: Record<string, FeedItem[]> = {};
    settled.forEach((outcome, index) => {
      if (outcome.status === "fulfilled") next[ids[index]] = outcome.value.items;
    });
    setCategoryPages(next);
  }, [overviewCategoryKey]);

  // 概览随层级与词汇源变化重查(L3 流不查 —— 流本体即数据面)
  useEffect(() => {
    if (drill.level === 3) return;
    void refreshOverview();
  }, [drill.level, refreshOverview]);

  // L2 定向补查:进层即取该品类页(概览未覆盖/词汇源迟到时保底;进层取新)
  const l2Category = drill.level === 2 ? drill.category : null;
  useEffect(() => {
    if (l2Category === null) return;
    let cancelled = false;
    overviewSeqRef.current += 1;
    const seq = overviewSeqRef.current;
    void fetchFeedPage({ cursor: null, cursorId: null, category: l2Category, query: null })
      .then((page) => {
        if (!cancelled && seq === overviewSeqRef.current) {
          setCategoryPages((current) => ({ ...current, [l2Category]: page.items }));
        }
      })
      .catch(() => {
        // 概览尽力而为:失败静默(L2 以已有页呈现,计数口径如实)
      });
    return () => {
      cancelled = true;
    };
  }, [l2Category]);

  /** 实时滚动刷新(10-06 追加:主人令「情报流要不停地过信息日志」):
   *  静默拉首页 → mergeFreshItems 前插新键(已加载行与游标零扰动,新条目
   *  持续进流);失败静默(轮询尽力而为,不打错误卡——手点刷新钮才走
   *  错误路径)。触发面:completed / cron.completed 事件即时 + 30s 可见性
   *  轮询兜底(CLI 独立跑的采集无事件;隐藏暂停不打 sidecar)。
   *  F2 对票 + L1/L2 顺带刷新概览(计数实时);L3 才并入流本体。 */
  const liveRefresh = useCallback(async () => {
    const seq = nextFeedSeq();
    try {
      const page = await fetchFeedPage({
        cursor: null,
        cursorId: null,
        category: streamScope.category,
        source: streamScope.source,
        sourceKind: streamScope.sourceKind,
        query,
      });
      if (seq !== feedSeqRef.current) return; // F2:旧应答丢弃(含切域后在途包)
      setItems((current) => mergeFreshItems(current, page.items).items);
      if (drill.level !== 3) void refreshOverview();
    } catch {
      // 尽力而为:轮询失败静默(下一轮/事件/手点刷新再试)
    }
  }, [streamScope.category, streamScope.source, drill.level, query, nextFeedSeq, refreshOverview]);

  // 事件驱动即时刷新:桌面 run 终态(completed)+ cron 派发 run 落地
  // (cron.completed);与空流 CTA 的定向订阅并行,重复刷新幂等无害
  useEffect(() => {
    let unlisten: UnlistenFn | null = null;
    let cancelled = false;
    void onSidecarEvent((event) => {
      if (event.type === "completed" || event.type === "cron.completed") void liveRefresh();
    }).then((un) => {
      if (cancelled) un();
      else unlisten = un;
    });
    return () => {
      cancelled = true;
      unlisten?.();
    };
  }, [liveRefresh]);

  // 轮询兜底:可见时 30s 一发;隐藏暂停,恢复可见即刷
  useEffect(() => {
    const timer = window.setInterval(() => {
      if (!document.hidden) void liveRefresh();
    }, LIVE_POLL_INTERVAL_MS);
    const onVisibilityChange = () => {
      if (!document.hidden) void liveRefresh();
    };
    document.addEventListener("visibilitychange", onVisibilityChange);
    return () => {
      window.clearInterval(timer);
      document.removeEventListener("visibilitychange", onVisibilityChange);
    };
  }, [liveRefresh]);

  // G9 状态源切换(§5.2):过门后 states 不再从 localStorage 派生,改由页内
  // 条目派生(store.items 投影三键);applyFeedFilter / sortUnreadFirst /
  // 渲染管线零改动,只换状态源。
  const states = useMemo<FeedStateMap>(
    () => (useServerState ? statesFromItems(items) : localStates),
    [useServerState, items, localStates],
  );

  // G9 一次性搬迁(Q2):过门且旧 map 非空 → 单请求 store.state.import(会话
  // 哨位防双调,幂等真相在服务端 store_meta);搬迁晚于首页应答时轻量
  // refresh 一次,让已导入读态即时对齐(搬迁对用户透明,不弹窗)。
  // refresh 随 query/category 变化重跑无妨:哨位已挡,重入零 RPC。
  useEffect(() => {
    if (!useServerState) return;
    let cancelled = false;
    void importLocalFeedStates().then((outcome) => {
      if (!cancelled && outcome !== null && outcome.imported > 0) void refresh();
    });
    return () => {
      cancelled = true;
    };
  }, [useServerState, refresh]);

  const loadMore = useCallback(async () => {
    if (loadingMore || cursor === null) return;
    const seq = nextFeedSeq();
    setLoadingMore(true);
    try {
      const page = await fetchFeedPage({
        cursor,
        cursorId,
        category: streamScope.category,
        source: streamScope.source,
        sourceKind: streamScope.sourceKind,
        query,
      });
      if (seq !== feedSeqRef.current) return; // F2:refresh/liveRefresh 已接管,旧页不追加
      setCursor(page.nextCursor);
      setCursorId(page.nextCursorId);
      setItems((current) => {
        const merged = appendFeedPage(current, page);
        // 追加 0 条防御判停(复合游标下不应发生;保留兜底防死循环)
        setHasMore(page.hasMore && merged.added > 0);
        return merged.items;
      });
    } catch (err) {
      if (seq !== feedSeqRef.current) return;
      setError(
        err instanceof SidecarRequestError
          ? err
          : new SidecarRequestError({ code: "transport_error", path: "$", message: String(err) }),
      );
    } finally {
      setLoadingMore(false);
    }
  }, [cursor, cursorId, loadingMore, streamScope.category, streamScope.source, query, nextFeedSeq]);

  /** 未过门通路的本地态写入:置 state + localStorage 持久(过门后不走此路) */
  const updateStates = useCallback((next: FeedStateMap) => {
    setLocalStates(next);
    saveFeedStates(next);
  }, []);

  /** A-feed 显示选项切换:置 state + 本地持久(myssia.feed.display.v1) */
  const updateDisplay = useCallback((next: FeedDisplayOptions) => {
    setDisplay(next);
    saveFeedDisplay(next);
  }, []);

  /** G9 服务端通路单键置位:乐观翻本地条目 → store.state.mark(keys=[itemKey],
   *  前端算好目标值显式置位,无读-改-写);失败回滚到调用前真值(不瞎取反,
   *  防连点竞态)+ feed-mark-error 行明示(惯例同 openError)。 */
  const markItemState = useCallback(
    (item: FeedItem, marker: "starred" | "later" | "read", value: boolean) => {
      const key = itemKey(item);
      const previous = items.find((candidate) => itemKey(candidate) === key)?.[marker] === true;
      if (previous === value) return;
      const flip = (target: boolean) =>
        setItems((current) =>
          current.map((candidate) =>
            itemKey(candidate) === key ? { ...candidate, [marker]: target } : candidate,
          ),
        );
      flip(value);
      void api
        .storeStateMark({ keys: [key], marker, value })
        .then(() => setMarkError(null))
        .catch((err) => {
          flip(previous);
          setMarkError(err instanceof SidecarRequestError ? `${err.code}: ${err.message}` : String(err));
        });
    },
    [items],
  );

  const markRead = useCallback(
    (item: FeedItem) => {
      const key = itemKey(item);
      if (states[key]?.read) return;
      if (useServerState) {
        markItemState(item, "read", true);
      } else {
        updateStates({ ...states, [key]: { ...(states[key] ?? {}), read: true } });
      }
    },
    [states, useServerState, markItemState, updateStates],
  );

  const toggle = useCallback(
    (item: FeedItem, marker: "starred" | "later" | "read") => {
      const key = itemKey(item);
      const current = states[key] ?? {};
      const target = !current[marker];
      if (useServerState) {
        markItemState(item, marker, target);
      } else {
        updateStates(toggleMarker(states, key, marker));
      }
    },
    [states, useServerState, markItemState, updateStates],
  );

  /** G8:精评成功 → 把维度分并回列表条目(卡片分数徽标即时刷新;items 表
   *  已由服务端回填,这里只是本地视图对齐,不重拉整页)。 */
  const onEnriched = useCallback((item: FeedItem, result: FeedEnrichResult) => {
    setItems((current) =>
      current.map((candidate) =>
        itemKey(candidate) === itemKey(item) ? { ...candidate, scores: result.scores } : candidate,
      ),
    );
  }, []);

  /** 消息详情弹窗(主人令「点击信息,弹出详情」,10-08):存 itemKey 而非
   *  条目对象 —— 刷新/巡游换来的新对象按 key 重新命中,读态/星标翻转到哪版
   *  条目,弹窗就吃到哪版(弹窗内动作即时回显)。条目被过滤离场不关弹窗
   *  (items 是已加载全集,命中仍在);条目彻底不在集内(理论上仅作用域
   *  切换,弹窗开着时交互被遮罩挡住)则 detailItem 为 null 零渲染。 */
  const [detailKey, setDetailKey] = useState<string | null>(null);
  const detailItem = useMemo(
    () => (detailKey === null ? null : items.find((candidate) => itemKey(candidate) === detailKey) ?? null),
    [detailKey, items],
  );
  /** 开详情 = 记已读(邮件式语义:点开即读)+ 置弹窗键 */
  const openDetail = useCallback(
    (item: FeedItem) => {
      setDetailKey(itemKey(item));
      markRead(item);
    },
    [markRead],
  );
  const closeDetail = useCallback(() => setDetailKey(null), []);

  /** G9 批量:全部标已读/未读(可选 category = 品类分组组头入口;可选
   *  sourceKind = 源大类作用域,10-08-tg-channel-card v2 卡片墙第二层)——
   *  过门后 store.state.mark_all 单 UPDATE:category/source_kind 缺省 =
   *  全库(含未翻页/未加载条目),传 category = 该品类全库精确等值(协议
   *  不收 query,决议 Q3.2),传 sourceKind = 大类全库(web/im,与 category
   *  可叠加);就地翻转已加载行内作用域条目即时反馈,不整页重拉,失败按
   *  调用前快照回滚(只回滚作用域内行,域外行不动);未过门 = 旧本地批量
   *  (作用域 = 已加载条目,无品类/大类入口,title 如实注明)。 */
  const markAllRead = useCallback(
    (value: boolean, category?: string, sourceKind?: "web" | "im") => {
      if (useServerState) {
        // 作用域谓词:全库 = 全部已加载行;品类 = 该 category 精确等值行;
        // 大类 = im(通讯软件前缀源)/ web(其余含无源)
        const inScope = (candidate: FeedItem) =>
          (category === undefined || candidate.category === category) &&
          (sourceKind === undefined ||
            (sourceKind === "im" ? imAppOf(candidate.source) !== null : imAppOf(candidate.source) === null));
        const snapshot = new Map(
          items.filter(inScope).map((candidate) => [itemKey(candidate), candidate.read === true]),
        );
        setItems((current) =>
          current.map((candidate) => (inScope(candidate) ? { ...candidate, read: value } : candidate)),
        );
        void api
          .storeStateMarkAll({
            marker: "read",
            value,
            ...(category !== undefined ? { category } : {}),
            ...(sourceKind !== undefined ? { source_kind: sourceKind } : {}),
          })
          .then(() => setMarkError(null))
          .catch((err) => {
            setItems((current) =>
              current.map((candidate) =>
                inScope(candidate)
                  ? { ...candidate, read: snapshot.get(itemKey(candidate)) ?? false }
                  : candidate,
              ),
            );
            setMarkError(err instanceof SidecarRequestError ? `${err.code}: ${err.message}` : String(err));
          });
        return;
      }
      updateStates(setMarkerBulk(items, states, "read", value));
    },
    [useServerState, items, states, updateStates],
  );
  const unreadLoaded = useMemo(
    () => items.filter((candidate) => !(states[itemKey(candidate)]?.read)).length,
    [items, states],
  );

  // ① later 到期重现:now 随过滤重算取值(窗口为天级,会话内漂移无感);
  //  到期稍后读条目经 applyFeedFilter 并入未读视图(机制见 ./api.ts ① 节)
  // ② 当日窗(10-06 追加):滚动流(未读/全部)只显 03:00 窗内条目 ——
  //  过窗即离场(视图层清零);later 到期重现条目是显式留存,窗后照现。
  const visible = useMemo(() => {
    const filtered = applyFeedFilter(items, states, filter, new Date());
    // 历史态(10-09-tg-category-entry 监控台入口):绕过当日窗,全部入库条目可见
    if (drill.level === 3 && drill.history) return filtered;
    if (filter !== "unread" && filter !== "all") return filtered;
    return filtered.filter(
      (item) =>
        inDayWindow(item.first_seen, windowStart) ||
        isLaterResurface(item, states[itemKey(item)]),
    );
  }, [items, states, filter, windowStart, drill]);

  /** 展示序(A-feed):过滤结果 → 未读优先(可选;未读浮前,两类各自稳定保序) */
  const displayItems = useMemo(
    () => (display.unreadFirst ? sortUnreadFirst(visible, states) : visible),
    [display.unreadFirst, visible, states],
  );

  /** 三层作用域派生(10-08-tg-channel-card v2):wallLayout = 卡片墙第一层
   *  (网页一张 + 每通讯软件一张,散条目卡退场);webDetailLayout = 网页
   *  详情(条目平铺);imDetailLayout = 通讯软件分节详情(频道卡降为节头,
   *  节内消息全量平铺)。legacyStreamLayout = 未过源大类门的多渠道流 = v1
   *  形态原样(TG 频道卡区 + 消息列表,双形态一门之隔)。 */
  const wallLayout =
    sourceKindReady && drill.level === 3 && drill.source === null && drill.kind === null;
  const imDetailLayout =
    sourceKindReady && drill.level === 3 && drill.source === null && drill.kind === "im";
  const legacyStreamLayout = drill.level === 3 && drill.source === null && !sourceKindReady;
  /** 聊天视图(10-09 聊天主页风格):TG 消息流(im 分节/单频道/TG 品类
   *  历史态)日期分隔走居中胶囊,消息气泡贴聊天语言。 */
  const chatStyleGroups =
    drill.level === 3 &&
    (drill.kind === "im" ||
      (drill.source ?? "").startsWith("telegram") ||
      (drill.history === true && (drill.category ?? "").startsWith("telegram")));
  /** TG 品类渠道页(10-09-tg-category-entry):品类 id telegram 前缀 = 该页
   *  顶部出「网页线监控台」卡(登录/监控状态 + 历史入口)。 */
  const isTelegramCategory = drill.level === 2 && drill.category.startsWith("telegram");

  /** v1 形态派生(未过门回落;过门后恒空 = 零渲染):渠道卡区 + 消息列表
   *  剔除 telegram。 */
  const tgCards = useMemo<TelegramChannelCardData[]>(
    () => (legacyStreamLayout ? telegramChannelCards(displayItems, states) : []),
    [legacyStreamLayout, displayItems, states],
  );
  const streamItems = useMemo(
    () =>
      legacyStreamLayout
        ? displayItems.filter((item) => channelKindOf(item, engineBySource) !== "telegram")
        : displayItems,
    [legacyStreamLayout, displayItems, engineBySource],
  );

  /** 卡片墙(v2 第一层):网页/通讯软件大类卡,计数口径 = 当前视图可见条目。 */
  const wallCards = useMemo<StreamKindCardData[]>(
    () => (wallLayout ? streamKindCards(displayItems, states) : []),
    [wallLayout, displayItems, states],
  );

  /** TG 分节详情(v2 第二层):频道节头卡(含节内 count/unread/latest,
   *  点击进单频道过滤视图 = 既有 source 作用域)。 */
  const imDetailCards = useMemo<TelegramChannelCardData[]>(
    () => (imDetailLayout ? telegramChannelCards(displayItems, states) : []),
    [imDetailLayout, displayItems, states],
  );
  /** TG 网页线快照(10-09-tg-category-entry:进 Telegram 分节详情或品类
   *  渠道页拉一次;失败静默 = 不出状态条,不拦浏览)。放在派生之后
   *  (imDetailLayout 在上方派生链产出,提前引用会踩 TDZ)。deps 必须含
   *  isTelegramCategory——L1→L2 钻入时只有它翻转(imDetailLayout 恒
   *  false),漏掉 = 监控台永远等不到快照(v2 在途改动实测踩坑)。 */
  useEffect(() => {
    if (!imDetailLayout && !isTelegramCategory) return;
    let cancelled = false;
    void telegramGetStatus()
      .then((status) => {
        if (!cancelled) setTgWebline(sanitizeTelegramStatus(status));
      })
      .catch(() => {
        if (!cancelled) setTgWebline(null);
      });
    return () => {
      cancelled = true;
    };
  }, [imDetailLayout, isTelegramCategory]);

  /** 分组(L3 显示选项):时间四桶(D4 缺省)/ 不分组(平铺)。三级下钻
   *  (10-06-feed-channel-groups)后品类维度 = L1/L2 层级本体,L3 组内不再
   *  出品类分组;历史本地存储的 groupMode="category" 就地映射回时间四桶
   *  (loadFeedDisplay 兼容旧值,不丢用户其余选项)。
   *  category 字段恒 null(时间桶无品类组头;品类批量入口移驻 L2 头部)。
   *  10-08-tg-channel-card:分组/平铺吃 streamItems(TG 条目已折叠进渠道
   *  卡区,组头计数如实反映列表本体)。10-08 v2:卡片墙与 TG 分节详情无
   *  时间分组(墙无消息卡;分节详情以频道为节)。 */
  const groups = useMemo<
    {
      key: string;
      label: string;
      items: FeedItem[];
      color: string | null;
      category: string | null;
    }[] | null
  >(() => {
    if (display.groupMode === "none" || wallLayout || imDetailLayout) return null;
    return groupFeedItems(streamItems).map((group) => ({
      key: group.key,
      label: group.label,
      items: group.items,
      color: null,
      category: null,
    }));
  }, [display.groupMode, streamItems, wallLayout, imDetailLayout]);

  /** 键盘「当前卡」(U/j/k 快捷键作用目标;hover/focus 进入卡时置位) */
  const [currentKey, setCurrentKey] = useState<string | null>(null);
  /** j/k 键盘巡游标志(Linear 式:focus 环只在键盘巡游时呈现,鼠标 hover 即清) */
  const [navByKeyboard, setNavByKeyboard] = useState(false);

  /** hover/focus 进入卡 = 置当前卡并退出键盘巡游态(focus 环让位 hover 背景) */
  const onCurrentCard = useCallback((key: string) => {
    setCurrentKey(key);
    setNavByKeyboard(false);
  }, []);


  // R2:全库批量确认态在屏期间 Esc 全局收口(焦点在确认钮簇内/外都退出确认);
  //  输入框/可编辑目标内按 Esc 归其自身语义(如搜索框 R1 即时清空),不抢确认
  //  退出 —— 守卫与上方 u/j/k 键 effect 同源(feed 本地惯例,不引外部 hook)。
  useEffect(() => {
    if (confirmAllMark === null) return;
    const onKeyDown = (event: KeyboardEvent) => {
      if (event.key !== "Escape") return;
      const target = event.target as HTMLElement | null;
      if (
        target &&
        (target.tagName === "INPUT" ||
          target.tagName === "TEXTAREA" ||
          target.tagName === "SELECT" || // 深审 F6:下拉内 Esc 归其自身语义
          target.isContentEditable)
      ) {
        return;
      }
      setConfirmAllMark(null);
    };
    window.addEventListener("keydown", onKeyDown);
    return () => window.removeEventListener("keydown", onKeyDown);
  }, [confirmAllMark]);

  /** 单卡渲染(分组/平铺两路共用;右键菜单随卡在 FeedCard 内;渠道类型
   *  随卡判定 —— 五档差异化呈现,engine 词表源 = health 装配的源名映射;
   *  TG 分节详情语境下卡头省频道名行,频道归属由节头承担) */
  const renderCard = (entry: FeedItem) => (
    <FeedCard
      key={itemKey(entry)}
      item={entry}
      state={states[itemKey(entry)] ?? {}}
      current={currentKey === itemKey(entry)}
      navFocused={currentKey === itemKey(entry) && navByKeyboard}
      kind={channelKindOf(entry, engineBySource)}
      inChannelSection={imDetailLayout}
      onCurrent={onCurrentCard}
      onToggle={toggle}
      onOpenError={setOpenError}
      onEnriched={onEnriched}
      onOpenDetail={openDetail}
    />
  );

  /** G3 导出当前视图:dialog.save → feed.export;回显 path/count(取消 = 静默) */
  const exportCurrentView = useCallback(async () => {
    setExporting(true);
    setExportNote(null);
    try {
      const outcome = await exportFeedView({
        format: exportFormat,
        category: drill.level === 3 ? drill.category : null,
        sourceKind:
          drill.level === 3 && drill.source === null ? (drill.kind ?? null) : null,
        query,
      });
      if (outcome.path !== null) {
        setExportNote(`已导出 ${outcome.count} 条 → ${outcome.path}(${outcome.bytes} 字节)`);
      }
    } catch (err) {
      setExportNote(
        `导出失败:${err instanceof SidecarRequestError ? `${err.code}: ${err.message}` : String(err)}`,
      );
    } finally {
      setExporting(false);
    }
  }, [exportFormat, drill, query]);

  /** 空流 CTA:health 取第一个可加载插件 → run.start(yaml 绝对路径,与 sources.write 同口径) */
  const startFirstPlugin = useCallback(async () => {
    setCta({ phase: "starting" });
    try {
      const health = await api.health();
      const plugin = health.plugins.find((candidate) => candidate.loaded) ?? health.plugins[0];
      if (!plugin) {
        setCta({
          phase: "error",
          message: "插件目录为空:重启应用触发首跑初始化,或到「源管理」检查插件目录。",
        });
        return;
      }
      const started = await api.runStart({ yaml: plugin.file });
      setCta({ phase: "collecting", runId: started.run_id });
    } catch (err) {
      setCta({
        phase: "error",
        message: err instanceof SidecarRequestError ? `${err.code}:${err.message}` : String(err),
      });
    }
  }, []);

  // completed 事件 → 回 idle(可再跑)+ 自动刷新;订阅随 collecting 状态起止
  useEffect(() => {
    if (cta.phase !== "collecting") return;
    let unlisten: UnlistenFn | null = null;
    let cancelled = false;
    void onSidecarEvent((event) => {
      if (event.type === "completed" && event.run_id === cta.runId) {
        setCta({ phase: "done" });
        void refresh();
      }
    }).then((un) => {
      if (cancelled) un();
      else unlisten = un;
    });
    return () => {
      cancelled = true;
      unlisten?.();
    };
  }, [cta, refresh]);

  const searchActive = query !== "";

  /** G9 批量两钮 title(双路真话;R2 确认态确认钮沿用同一支)。三级下钻
   *  (10-06)后按作用域分档:全库流(无品类)= 全库真话;品类流 = 该品类
   *  全库真话(mark_all 带 category 精确等值);渠道流不出钮(feed.export/
   *  mark_all 无 source 参数,范围不实则不出现)。10-08 审计 F7:协议方法名
   *  (store.state.mark_all / source_kind)不再进用户面 tooltip,人话说清
   *  范围与持久性即可,协议细节归开发者文档/日志。 */
  const bulkScopeCategory = drill.level === 3 ? drill.category : null;
  /** 源大类批量作用域(v2:第二层详情传 source_kind,卡片墙/单频道不传) */
  const bulkScopeKind =
    drill.level === 3 && drill.source === null ? (drill.kind ?? undefined) : undefined;
  const bulkKindLabel = bulkScopeKind === "web" ? "网页" : "Telegram";
  const bulkHidden = drill.level === 3 && drill.source !== null;
  const markAllReadTitle = !useServerState
    ? `把已加载的 ${items.length} 条(未读 ${unreadLoaded})全部标记为已读;本地态,未翻页条目不含`
    : bulkScopeKind !== undefined
      ? `把${bulkKindLabel}范围${bulkScopeCategory !== null ? `·品类「${bulkScopeCategory}」` : ""}的全部条目(含未翻页)标记为已读,服务端持久`
      : bulkScopeCategory !== null
        ? `把品类「${bulkScopeCategory}」的全库条目(含未翻页)标记为已读,服务端持久`
        : "把全库所有条目(含未翻页)标记为已读,服务端持久";
  const markAllUnreadTitle = !useServerState
    ? `把已加载的 ${items.length} 条(已读 ${items.length - unreadLoaded})全部恢复未读;本地态`
    : bulkScopeKind !== undefined
      ? `把${bulkKindLabel}范围${bulkScopeCategory !== null ? `·品类「${bulkScopeCategory}」` : ""}的全部条目(含未翻页)恢复为未读,服务端持久`
      : bulkScopeCategory !== null
        ? `把品类「${bulkScopeCategory}」的全库条目(含未翻页)恢复为未读,服务端持久`
        : "把全库所有条目(含未翻页)恢复为未读,服务端持久";

  // ---------------------------------------------------------------------------
  // 三级下钻派生(10-06-feed-channel-groups):L1 品类行 / L2 渠道行的
  // 计数与词表。计数源(深审 F1)= 按品类查询页(categoryPages,每品类
  // 独立首页 50)× 当日窗 —— 不再吃全局首页 50 条(长尾品类假空态/假零);
  // L1/L2 是「今日滚动窗」的概览,过窗条目不计入(title 注记口径,如实)。
  // ---------------------------------------------------------------------------
  const categoryLabelOf = useCallback(
    (id: string) => categoryOptions.find((option) => option.id === id)?.label ?? id,
    [categoryOptions],
  );

  /** 窗内谓词(L1/L2 计数用;later 到期重现条目视同显式留存,计回窗) */
  const inWindowOrResurfaced = useCallback(
    (item: FeedItem) =>
      inDayWindow(item.first_seen, windowStart) ||
      isLaterResurface(item, states[itemKey(item)]),
    [windowStart, states],
  );

  /** 品类页条目 → 行计数累积(品类守卫:服务端已滤,防御共享 mock/旧包)。 */
  const l1Rows = useMemo(() => {
    const byCategory = new Map<string, { today: number; unread: number; channels: Set<string> }>();
    const touch = (id: string) => {
      let row = byCategory.get(id);
      if (!row) {
        row = { today: 0, unread: 0, channels: new Set() };
        byCategory.set(id, row);
      }
      return row;
    };
    for (const [categoryId, pageItems] of Object.entries(categoryPages)) {
      for (const item of pageItems) {
        if (item.category === null || item.category !== categoryId) continue;
        if (!inWindowOrResurfaced(item)) continue;
        const row = touch(item.category);
        row.today += 1;
        if (!(item.read === true)) row.unread += 1;
        if (item.source) row.channels.add(item.source);
      }
    }
    const seen = new Set<string>();
    const rows: { id: string; label: string; today: number; unread: number; channels: number; color: string | null }[] = [];
    for (const option of categoryOptions) {
      seen.add(option.id);
      const row = byCategory.get(option.id);
      rows.push({
        id: option.id,
        label: option.label,
        today: row?.today ?? 0,
        unread: row?.unread ?? 0,
        channels: row?.channels.size ?? 0,
        color: categoryColor(option.id),
      });
    }
    for (const [id, row] of byCategory) {
      if (seen.has(id)) continue;
      rows.push({ id, label: id, today: row.today, unread: row.unread, channels: row.channels.size, color: categoryColor(id) });
    }
    return rows;
  }, [categoryPages, categoryOptions, inWindowOrResurfaced]);

  /** L1 全局行计数(全部条目 · 滚动流)= 各品类页窗内计数之和 + 无品类
   *  条目(全局首页页兜底;各品类页服务端互斥,无双重计)。 */
  const l1AllStats = useMemo(() => {
    let today = 0;
    let unread = 0;
    const channels = new Set<string>();
    const count = (item: FeedItem) => {
      if (!inWindowOrResurfaced(item)) return;
      today += 1;
      if (!(item.read === true)) unread += 1;
      if (item.source) channels.add(item.source);
    };
    for (const pageItems of Object.values(categoryPages)) {
      for (const item of pageItems) {
        if (item.category == null) continue; // 无品类条目走全局页一面
        count(item);
      }
    }
    for (const item of items) {
      if (item.category != null) continue; // 已在品类页计
      count(item);
    }
    return { today, unread, channels: channels.size };
  }, [categoryPages, items, inWindowOrResurfaced]);

  /** L2 渠道行数据(F1):该品类的**品类查询页**按渠道分组(首现顺序)+
   *  各行窗内计数 —— 不再从全局首页过滤(长尾渠道假空态)。 */
  const l2Channels = useMemo(() => {
    if (drill.level !== 2) return [];
    const pageItems = (categoryPages[drill.category] ?? []).filter(
      (item) => item.category === drill.category,
    );
    return groupFeedItemsByChannel(pageItems, engineBySource).map((channel) => {
      const windowed = channel.items.filter(inWindowOrResurfaced);
      return {
        ...channel,
        // F9:渠道行展示名走 channelDisplayName 词表(与卡面/渠道卡同一套),
        // key 仍是源名全称(下钻作用域词,testid 同源不受影响)
        label: channelDisplayName(channel.key),
        today: windowed.length,
        unread: windowed.filter((item) => !(item.read === true)).length,
      };
    });
  }, [drill, categoryPages, engineBySource, inWindowOrResurfaced]);

  /** L2 窗内已加载条目(F3 作用域面:豁免钮实际作用的 keys = 所见行)。 */
  const l2WindowedItems = useMemo(
    () =>
      drill.level === 2
        ? (categoryPages[drill.category] ?? [])
            .filter((item) => item.category === drill.category)
            .filter(inWindowOrResurfaced)
        : [],
    [drill, categoryPages, inWindowOrResurfaced],
  );

  /** F3 作用域收窄:L2 批量钮 = 当日窗内已加载品类页的**逐键置位**
   *  (store.state.mark keys)—— UI 所见(窗内行)= 实际作用域,不再走
   *  全库 mark_all(此前豁免钮作用域 = 该品类全库含未翻页,大于所见面);
   *  未读反向出口同门(keys 置 false,误触可逆)。乐观翻品类页行,失败按
   *  调用前快照回滚(仅作用域内行)。 */
  const markWindowScoped = useCallback(
    (value: boolean) => {
      if (!useServerState || drill.level !== 2) return;
      const keys = l2WindowedItems.map(itemKey);
      if (keys.length === 0) return;
      const keySet = new Set(keys);
      const snapshot = new Map(
        l2WindowedItems.map((item) => [itemKey(item), item.read === true]),
      );
      const rewrite = (readOf: (key: string) => boolean) =>
        setCategoryPages((current) => ({
          ...current,
          [drill.category]: (current[drill.category] ?? []).map((item) =>
            item.category === drill.category && keySet.has(itemKey(item))
              ? { ...item, read: readOf(itemKey(item)) }
              : item,
          ),
        }));
      rewrite(() => value);
      void api
        .storeStateMark({ keys, marker: "read", value })
        .then(() => setMarkError(null))
        .catch((err) => {
          rewrite((key) => snapshot.get(key) ?? false);
          setMarkError(err instanceof SidecarRequestError ? `${err.code}: ${err.message}` : String(err));
        });
    },
    [useServerState, drill, l2WindowedItems],
  );

  /** 下钻导航动作 */
  const openAllStream = useCallback(() => {
    setDrill({ level: 3, category: null, source: null, kind: null, history: false });
    setCurrentKey(null);
    setNavByKeyboard(false);
  }, []);
  const openCategory = useCallback((id: string) => {
    setDrill({ level: 2, category: id });
    setCurrentKey(null);
  }, []);
  const openCategoryStream = useCallback(() => {
    setDrill((current) =>
      current.level === 2 ? { level: 3, category: current.category, source: null, kind: null, history: false } : current,
    );
    setCurrentKey(null);
  }, []);
  const openChannel = useCallback((source: string) => {
    setDrill((current) =>
      current.level === 2 ? { level: 3, category: current.category, source, kind: "im", history: false } : current,
    );
    setCurrentKey(null);
  }, []);
  /** 渠道卡点击(v1 频道卡区 / v2 TG 分节节头共用):进该渠道消息流,
   *  保留当前品类与源大类作用域(卡片墙进 TG 详情后点节头 = 单频道过滤)。 */
  const openChannelFromStream = useCallback((source: string) => {
    setDrill((current) =>
      current.level === 3 && current.source === null
        ? { level: 3, category: current.category, source, kind: current.kind, history: current.history }
        : current,
    );
    setCurrentKey(null);
    setNavByKeyboard(false);
  }, []);
  /** 监控台历史入口(10-09-tg-category-entry):TG 品类渠道页「看全部历史
   *  消息」——L3 历史态绕过当日窗,展示该品类全部入库条目。 */
  const openCategoryHistory = useCallback(() => {
    setDrill((current) =>
      current.level === 2
        ? { level: 3, category: current.category, source: null, kind: null, history: true }
        : current,
    );
    setCurrentKey(null);
  }, []);
  /** 卡片墙点击(v2):进源大类第二层详情(网页=条目平铺 / 通讯软件=分节全铺)。
   *  history 透传(10-09 v2.2 验收员主发现:历史卡片墙点 Telegram 卡此前
   *  硬编码 history:false —— 当日窗回魂,老条目本体在分节详情消失,历史
   *  只剩墙卡计数;与 openChannelFromStream 的透传同门)。 */
  const openKind = useCallback((kind: "web" | "im") => {
    setDrill((current) =>
      current.level === 3 && current.source === null && current.kind === null
        ? { level: 3, category: current.category, source: null, kind, history: current.history }
        : current,
    );
    setCurrentKey(null);
    setNavByKeyboard(false);
  }, []);
  /** 单频道 → 回 TG 分节详情(v2 面包屑「Telegram」中间层同门;openKind 的
   *  守卫只认卡片墙起点,这里从 source 作用域回流)。 */
  const backToImDetail = useCallback(() => {
    setDrill((current) =>
      current.level === 3
        ? { level: 3, category: current.category, source: null, kind: "im", history: current.history }
        : current,
    );
    setCurrentKey(null);
  }, []);
  /** 异形应答不进状态条(旧 sidecar/测试桩可能缺 web 段;null = 条不出) */
  const sanitizeTelegramStatus = useCallback((status: TelegramStatus | null | undefined) => {
    return status && Array.isArray(status?.web?.accounts) ? status : null;
  }, []);
  /** 网页线扫码登录(10-09-tg-category-entry):浏览器模块统一入口,同操
   *  作在跑 = started:false 幂等;拉起后重拉状态对账(登录窗完成态由轮询
   *  /手动刷新对账,此处一次性)。失败静默,条内可再点。 */
  const startWebLogin = useCallback(async () => {
    const account = tgWebline?.web.accounts[0]?.account;
    if (!account) return;
    setTgLoginBusy(true);
    try {
      await telegramWebLogin(account);
      const next = await telegramGetStatus();
      setTgWebline(sanitizeTelegramStatus(next));
    } catch {
      // 尽力而为:失败态在设置 · Telegram 总卡有完整台账,条内不弹错
    } finally {
      setTgLoginBusy(false);
    }
  }, [tgWebline]);
  /** 内置浏览器预览(10-09-tg-category-entry v3 AC11,主人令「是否加载了
   *  内置浏览器界面,展示 tg 内容」):取该品类最新条目 url 推导频道公开
   *  镜像 t.me/s/<频道名>,WebviewWindow 应用内窗口直开(免二次登录)。
   *  职责分离:数据入库仍由后台 watcher 登录会话负责,本窗口**仅内容展示**,
   *  不做任何采集/登录动作;推导不出(私有频道/无 t.me 链)= 按钮置灰,
   *  title 如实;开窗失败(tauri://error)= 条内出说明,不装死。 */
  const [tgPreviewNote, setTgPreviewNote] = useState<string | null>(null);
  const tgPreviewUrl = useMemo(() => {
    const category = drill.level === 2 ? drill.category : null;
    if (category === null || !category.startsWith("telegram")) return null;
    for (const item of categoryPages[category] ?? []) {
      const mirror = telegramMirrorUrlOf(item.url);
      if (mirror) return mirror;
    }
    return null;
  }, [categoryPages, drill]);
  const openTgPreview = useCallback((mirror: string) => {
    setTgPreviewNote(null);
    try {
      // 标签带时间戳 = 每次点击新窗,不与既有窗撞 label(撞了也走 error 注记)
      const win = new WebviewWindow(`tg-preview-${Date.now()}`, {
        url: mirror,
        title: "Telegram 预览(内置浏览器)",
        width: 460,
        height: 780,
      });
      void win.once("tauri://error", () => {
        setTgPreviewNote(
          "预览窗打开失败(镜像不可达或窗口创建被拒;私有频道无公开预览)——条目「打开原文」仍可系统浏览器直看。",
        );
      });
    } catch {
      setTgPreviewNote("预览窗打开失败(窗口创建异常)——条目「打开原文」仍可系统浏览器直看。");
    }
  }, []);
  /** 回卡片墙(第二层详情回流;面包屑「全部条目/品类」同门)。history 透传
   *  (10-09 v2.2:历史分节详情回墙不丢历史态,与 openKind 同门)。 */
  const backToStreamAll = useCallback(() => {
    setDrill((current) =>
      current.level === 3
        ? { level: 3, category: current.category, source: null, kind: null, history: current.history }
        : current,
    );
    setCurrentKey(null);
  }, []);
  const backToL1 = useCallback(() => setDrill({ level: 1 }), []);
  const backToL2 = useCallback(() => {
    setDrill((current) => (current.level === 3 && current.category !== null ? { level: 2, category: current.category } : { level: 1 }));
  }, []);

  // U = 当前卡已读/未读切换;j/k = 当前卡上/下移(Linear Inbox 惯例;输入框/
  // 可编辑目标内敲不触发,守卫与既有 U 键同源,不引外部 hook——feed 本地惯例);
  // Mod+F(macOS ⌘F / Win·Linux Ctrl+F)= 拦截浏览器查找,聚焦内联搜索框并
  // 全选词面(可直接改写;fe-gap-census R1,linear-activity #8)。
  // 10-08:F5 墙卡(kind:web / kind:im)纳入巡游集,U/Enter 语义对齐进大类
  // 详情;Enter 在消息卡 = 开详情弹窗(与点击同门,详情弹窗开着时巡游键让位)。
  // (本 effect 置于下钻导航动作之后:闭包引用 openKind/openDetail。)
  useEffect(() => {
    // 三级下钻(10-06):巡游/搜索快捷键只属 L3 消息流(L1/L2 无卡无搜索框)
    if (drill.level !== 3) return;
    const onKeyDown = (event: KeyboardEvent) => {
      const pressed = event.key.toLowerCase();
      if ((event.metaKey || event.ctrlKey) && pressed === "f") {
        event.preventDefault();
        searchInputRef.current?.focus();
        searchInputRef.current?.select();
        return;
      }
      // 详情弹窗开着:巡游/置位键让位(防焦点绕过遮罩在背后卡上移动)
      if (detailKey !== null) return;
      if (pressed !== "u" && pressed !== "j" && pressed !== "k" && pressed !== "enter") return;
      if (event.metaKey || event.ctrlKey || event.altKey) return;
      const target = event.target as HTMLElement | null;
      if (
        target &&
        (target.tagName === "INPUT" ||
          target.tagName === "TEXTAREA" ||
          target.tagName === "SELECT" || // 深审 F6:下拉聚焦时敲键是选型操作(u/j/k 不抢)
          target.isContentEditable)
      ) {
        return;
      }
      // Enter 命中本就是点击语义的控件(button/link)时归其原生行为,不双触发
      if (pressed === "enter" && target && (target.tagName === "BUTTON" || target.tagName === "A")) {
        return;
      }
      // 墙卡作用域(F5):currentKey = kind:web / kind:im,U/Enter = 进大类详情;
      // j/k 不拦截,落下方巡游段(墙层 keys 即墙卡)
      if (currentKey !== null && currentKey.startsWith("kind:") && (pressed === "u" || pressed === "enter")) {
        const kindKey = currentKey.slice("kind:".length);
        if (kindKey === "web" || kindKey === "im") openKind(kindKey);
        return;
      }
      if (pressed === "u") {
        if (currentKey === null) return;
        const item = items.find((candidate) => itemKey(candidate) === currentKey);
        if (item) toggle(item, "read");
        return;
      }
      if (pressed === "enter") {
        if (currentKey === null) return;
        const item = items.find((candidate) => itemKey(candidate) === currentKey);
        if (item) openDetail(item);
        return;
      }
      // j/k:展示序上/下移;边界钳制不回绕(首卡 k / 末卡 j 原地不动),
      // 未选中时 j 落首卡、k 落末卡(当前卡被过滤离场同此路径)。
      // v1 形态吃 streamItems(TG 折叠进渠道卡区);第二层详情/单频道吃
      // displayItems(全部真实渲染,含 TG 分节);卡片墙吃墙卡(F5:
      // kind:web / kind:im 入巡游集,墙层不再静默空转)。
      const keys = wallLayout
        ? wallCards.map((card) => `kind:${card.key}`)
        : (legacyStreamLayout ? streamItems : displayItems).map(itemKey);
      if (keys.length === 0) return;
      const index = currentKey === null ? -1 : keys.indexOf(currentKey);
      const next =
        pressed === "j"
          ? keys[index < 0 ? 0 : Math.min(index + 1, keys.length - 1)]
          : keys[index < 0 ? keys.length - 1 : Math.max(index - 1, 0)];
      setCurrentKey(next);
      setNavByKeyboard(true);
      // 巡游卡滚入视口(最近侧;jsdom 无 scrollIntoView 实现时静默跳过)
      const escaped =
        typeof CSS !== "undefined" && typeof CSS.escape === "function" ? CSS.escape(next) : next;
      const node = document.querySelector<HTMLElement>(`[data-item-key="${escaped}"]`);
      if (node && typeof node.scrollIntoView === "function") node.scrollIntoView({ block: "nearest" });
    };
    window.addEventListener("keydown", onKeyDown);
    return () => window.removeEventListener("keydown", onKeyDown);
  }, [
    drill.level,
    currentKey,
    items,
    toggle,
    streamItems,
    wallLayout,
    legacyStreamLayout,
    displayItems,
    wallCards,
    detailKey,
    openDetail,
    openKind,
  ]);

  /** L3 流头部作用域文案 */
  const streamTitle =
    drill.level !== 3
      ? ""
      : drill.source !== null
        ? channelDisplayName(drill.source)
        : drill.kind === "web"
          ? `${drill.category !== null ? `${categoryLabelOf(drill.category)} · ` : ""}网页`
          : drill.kind === "im"
            ? `${drill.category !== null ? `${categoryLabelOf(drill.category)} · ` : ""}Telegram`
            : drill.category !== null
              ? `${categoryLabelOf(drill.category)} · 全部渠道`
              : sourceKindReady
                ? "全部条目 · 卡片墙"
                : "全部条目 · 滚动流";

  /** 面包屑(L2/L3):情报流 / 品类 / 渠道 —— 屏内既有交互语言,零新基件 */
  const breadcrumb = drill.level === 1 ? null : (
    <nav aria-label="情报流导航" className="flex flex-wrap items-center gap-1 px-6 text-xs text-muted-foreground" data-testid="feed-breadcrumb">
      <button
        type="button"
        className="rounded-sm px-1 py-0.5 hover:text-foreground"
        data-testid="feed-crumb-home"
        onClick={backToL1}
      >
        情报流
      </button>
      {drill.category !== null ? (
        <>
          <ChevronRight aria-hidden className="size-3" />
          <button
            type="button"
            className="rounded-sm px-1 py-0.5 hover:text-foreground"
            data-testid="feed-crumb-category"
            onClick={drill.level === 3 ? backToL2 : backToL1}
          >
            {categoryLabelOf(drill.category)}
          </button>
        </>
      ) : null}
      {/* 全部条目中间层(10-08-tg-channel-card):第二层详情/单频道从全部
          条目作用域点进,回流一键返卡片墙(v2)/滚动流(v1) */}
      {drill.level === 3 && drill.category === null && (drill.source !== null || drill.kind !== null) ? (
        <>
          <ChevronRight aria-hidden className="size-3" />
          <button
            type="button"
            className="rounded-sm px-1 py-0.5 hover:text-foreground"
            data-testid="feed-crumb-all-stream"
            onClick={backToStreamAll}
          >
            全部条目
          </button>
        </>
      ) : null}
      {/* Telegram 中间层(v2):单频道视图从 TG 分节详情点进,一键回分节 */}
      {drill.level === 3 && drill.kind === "im" && drill.source !== null ? (
        <>
          <ChevronRight aria-hidden className="size-3" />
          <button
            type="button"
            className="rounded-sm px-1 py-0.5 hover:text-foreground"
            data-testid="feed-crumb-im"
            onClick={backToImDetail}
          >
            Telegram
          </button>
        </>
      ) : null}
      {drill.level === 3 && drill.source !== null ? (
        <>
          <ChevronRight aria-hidden className="size-3" />
          <span className="px-1 py-0.5 text-foreground">{channelDisplayName(drill.source)}</span>
        </>
      ) : drill.level === 3 && drill.kind === "web" ? (
        <>
          <ChevronRight aria-hidden className="size-3" />
          <span className="px-1 py-0.5 text-foreground">网页</span>
        </>
      ) : drill.level === 3 && drill.kind === "im" ? (
        <>
          <ChevronRight aria-hidden className="size-3" />
          <span className="px-1 py-0.5 text-foreground">Telegram</span>
        </>
      ) : null}
      {/* 作用域终端段(10-08 审计 F6):卡片墙/滚动流/品类合流三层此前没有
          终端词,面包屑只剩孤零零「情报流」—— 补可见当前位置词(streamTitle
          同源,墙层 = 「全部条目 · 卡片墙」) */}
      {drill.level === 3 && drill.source === null && drill.kind === null ? (
        <>
          <ChevronRight aria-hidden className="size-3" />
          <span className="px-1 py-0.5 text-foreground" data-testid="feed-crumb-current">
            {streamTitle}
          </span>
        </>
      ) : null}
      {drill.level === 2 ? (
        <>
          <ChevronRight aria-hidden className="size-3" />
          {/* 终端词 = 「渠道页」而非品类名复读(10-09 v2.2 验收员挑刺:
              「Telegram 监控 → Telegram 监控」同词重复;品类词已在上一段) */}
          <span className="px-1 py-0.5 text-foreground">渠道页</span>
        </>
      ) : null}
    </nav>
  );

  /** L1/L2 概览行公共骨架(下钻行:图标 + 名称 + 类型词 + 计数 + chevron) */
  const drillRow = (options: {
    testId: string;
    onOpen: () => void;
    icon: React.ReactNode;
    label: string;
    meta: React.ReactNode;
    color: string | null;
  }) => (
    <button
      key={options.testId}
      type="button"
      data-testid={options.testId}
      onClick={options.onOpen}
      className="group/row flex w-full items-center gap-2.5 rounded-md border border-border/60 bg-card px-3 py-2.5 text-left transition-colors duration-(--duration-fast) ease-out-expo hover:border-primary/40 hover:bg-accent/40"
    >
      {options.color !== null ? (
        <span aria-hidden className="size-2 shrink-0 rounded-full" style={{ backgroundColor: options.color }} />
      ) : null}
      {options.icon}
      <span className="min-w-0 flex-1">
        <span className="block truncate text-sm font-medium text-foreground">{options.label}</span>
        <span className="mt-0.5 block text-2xs text-muted-foreground">{options.meta}</span>
      </span>
      <ChevronRight aria-hidden className="size-4 shrink-0 text-muted-foreground/70 transition-transform duration-(--duration-fast) ease-out-expo group-hover/row:translate-x-0.5" />
    </button>
  );

  return (
    /* 满高列表容器(10-04-ui-kestra-anchor:Kestra Executions 列表密度——列表区
     * 内滚、过滤条/组头常驻;页面级 gap-block 滚动让位) */
    <div className="flex h-full min-h-0 flex-col gap-4">
      <PageHeader
        title="情报流"
        description={
          drill.level === 1
            ? `品类 → 渠道 → 消息流 三级下钻(${
                useServerState ? "服务端持久,随库同步" : "本地态,随浏览器存储持久"
              })`
            : undefined
        }
      />
      {breadcrumb}

      {drill.level === 1 ? (
        /* ═══ L1 品类列表(10-06 三级下钻首页):全部条目滚动流(置顶)+ 品类行 ═══ */
        <div className="flex min-h-0 flex-1 flex-col gap-3 overflow-y-auto px-6 pb-6" data-testid="feed-l1">
          {/* 当日窗知会(全局):滚动流语义一眼可见 */}
          <span
            className="text-2xs text-muted-foreground"
            data-testid="feed-day-window"
            title={`当日窗:每天 03:00 清零滚动流(03:00 → 次日 03:00),过窗条目离场、视图从零累计;store 数据不清(retention 照旧),星标/稍后读跨窗可见;实时滚动 = 采集事件即时刷新 + 30s 可见性轮询;L1/L2 计数 = 按品类查询首页(每品类 50)× 当日窗`}
          >
            当日窗 03:00 起 · 实时滚动 · 今日 {l1AllStats.today} 条 / 未读 {l1AllStats.unread}
          </span>

          {error ? (
            <Card data-testid="feed-error">
              <CardContent className="flex flex-col gap-1.5 pt-1">
                {error.code === "pyenv_not_ready" ? (
                  /* D2/AC2:环境未就绪非重试可救——人话引导进设置(10-05 收尾) */
                  <>
                    <p className="text-sm font-medium text-warning">{error.message}</p>
                    <a
                      href="#/settings?section=python-env"
                      className="w-fit text-xs text-link underline underline-offset-2 hover:text-link/80"
                    >
                      前往设置 →「Python 环境」完成配置(就绪后情报流自动恢复)
                    </a>
                  </>
                ) : (
                  <>
                    <p className="text-sm font-medium text-destructive">
                      情报流不可用(sidecar 错误码 {error.code})
                    </p>
                    <p className="text-xs text-muted-foreground">{error.message}</p>
                    <Button
                      variant="outline"
                      size="sm"
                      className="w-fit"
                      onClick={() => void refresh()}
                      disabled={loading}
                    >
                      <RefreshCw className={loading ? "size-3.5 animate-spin" : "size-3.5"} />
                      重试
                    </Button>
                  </>
                )}
              </CardContent>
            </Card>
          ) : null}

          {loading && items.length === 0 ? (
            <div className="flex flex-col gap-1.5" data-testid="feed-loading" aria-busy="true" aria-label="情报流加载中">
              {[0, 1, 2, 3].map((row) => (
                <div key={row} className="rounded-md border border-border/50 px-3 py-2.5">
                  <Skeleton className="h-4 w-2/5" />
                  <Skeleton className="mt-1.5 h-3 w-1/4" />
                </div>
              ))}
            </div>
          ) : !error && items.length === 0 ? (
            /* 空态三支(L1 原样收编):搜索空 / 首跑 / 空流 CTA(质检件:!error 门) */
            searchActive ? (
              <Card data-testid="feed-search-empty">
                <CardContent className="p-0">
                  <EmptyState
                    title="没有匹配的条目"
                    description={`服务端全库搜索「${query}」零命中;换个关键词,或清空搜索看全部条目。`}
                  />
                </CardContent>
              </Card>
            ) : firstRun ? (
              <Card data-testid="feed-first-run">
                <CardContent className="p-0">
                  <EmptyState
                    title="还没有可运行的插件"
                    description="应用首次运行尚未装上官方插件;重启应用会自动完成初始化,或到「源管理」查看插件目录。"
                    tag="首跑"
                    action={
                      <Button variant="outline" size="sm" onClick={() => navigate("/sources")}>
                        去源管理
                      </Button>
                    }
                  />
                </CardContent>
              </Card>
            ) : (
              <Card data-testid="feed-run-cta">
                <CardContent className="p-0">
                  <EmptyState
                    title="情报流还是空的"
                    description={
                      cta.phase === "collecting"
                        ? `采集中(run #${cta.runId}),完成后自动刷新…`
                        : cta.phase === "done"
                          ? "本次采集已结束;若仍无条目,可到「日志」查看运行明细。"
                          : cta.phase === "error"
                            ? cta.message
                            : "先运行一个插件:采集到的条目会按新→旧出现在这里。"
                    }
                    action={
                      cta.phase === "collecting" ? (
                        <Button size="sm" disabled>
                          <RefreshCw className="size-3.5 animate-spin" />
                          采集中…
                        </Button>
                      ) : (
                        <Button
                          size="sm"
                          onClick={() => void startFirstPlugin()}
                          disabled={cta.phase === "starting"}
                        >
                          <Play className="size-3.5" />
                          {cta.phase === "starting" ? "启动中…" : "运行第一个插件"}
                        </Button>
                      )
                    }
                  />
                </CardContent>
              </Card>
            )
          ) : (
            <>
              {/* 置顶:全部条目滚动流(全局 L3;主人令「不停地过信息日志」的窗口) */}
              {drillRow({
                testId: "feed-drill-all",
                onOpen: openAllStream,
                icon: <Inbox aria-hidden className="size-4 shrink-0 text-primary" />,
                label: "全部条目 · 滚动流",
                meta: `今日 ${l1AllStats.today} 条 · 未读 ${l1AllStats.unread} · ${l1AllStats.channels} 渠道(跨品类全局流)`,
                color: null,
              })}
              <div className="flex flex-col gap-1.5" data-testid="feed-l1-categories">
                {/* 10-09-tg-category-entry:今日有货的品类行在前,零计数行折叠
                    进「今日未更新」(缺省收起)——零计数如实但不再刷屏 */}
                {l1Rows
                  .filter((row) => row.today > 0)
                  .map((row) =>
                    drillRow({
                      testId: `feed-drill-cat-${row.id}`,
                      onOpen: () => openCategory(row.id),
                      icon: null,
                      label: row.label,
                      meta: `今日 ${row.today} 条 · 未读 ${row.unread} · ${row.channels} 渠道`,
                      color: row.color,
                    }),
                  )}
                {l1Rows.some((row) => row.today === 0) ? (
                  <>
                    <button
                      type="button"
                      data-testid="feed-l1-idle-toggle"
                      onClick={() => setIdleOpen((current) => !current)}
                      className="flex w-fit items-center gap-1 rounded-sm px-1 py-0.5 text-2xs text-muted-foreground hover:text-foreground"
                      aria-expanded={idleOpen}
                    >
                      {idleOpen ? (
                        <ChevronDown aria-hidden className="size-3" />
                      ) : (
                        <ChevronRight aria-hidden className="size-3" />
                      )}
                      今日未更新 · {l1Rows.filter((row) => row.today === 0).length} 个品类
                    </button>
                    {idleOpen ? (
                      <div className="flex flex-col gap-1.5 opacity-60" data-testid="feed-l1-idle-categories">
                        {l1Rows
                          .filter((row) => row.today === 0)
                          .map((row) =>
                            drillRow({
                              testId: `feed-drill-cat-${row.id}`,
                              onOpen: () => openCategory(row.id),
                              icon: null,
                              label: row.label,
                              meta: `今日 ${row.today} 条 · 未读 ${row.unread} · ${row.channels} 渠道`,
                              color: row.color,
                            }),
                          )}
                      </div>
                    ) : null}
                  </>
                ) : null}
              </div>
            </>
          )}
        </div>
      ) : drill.level === 2 ? (
        /* ═══ L2 渠道列表:品类内按渠道分组,渠道卡片带类型基因 ═══ */
        <div className="flex min-h-0 flex-1 flex-col gap-3 overflow-y-auto px-6 pb-6" data-testid="feed-l2">
          <div className="flex items-center justify-between gap-2">
            <span
              className="text-2xs text-muted-foreground"
              data-testid="feed-day-window"
              title="当日窗 03:00 → 次日 03:00;L2 计数 = 该品类查询首页(50 条页)× 当日窗"
            >
              当日窗 03:00 起 · 今日 {l2Channels.reduce((sum, channel) => sum + channel.today, 0)} 条
            </span>
            {/* 品类批量入口(g9-read-all R1 迁驻;深审 F3 作用域收窄):逐键置位
                当日窗内已加载行(store.state.mark)—— UI 所见 = 实际作用域,不再
                mark_all 全库越面;反向出口(窗内全部未读)同门,误触可逆;只在
                过门时出现(未过门旧通路无品类作用域)。 */}
            {useServerState ? (
              <span className="flex items-center gap-1">
                <Button
                  variant="ghost"
                  size="sm"
                  className="px-2 text-xs text-muted-foreground"
                  data-testid="feed-category-mark-all"
                  aria-label={`把「${categoryLabelOf(drill.category)}」当日窗内已加载的 ${l2WindowedItems.length} 条标为已读(作用域=所见行)`}
                  title={`把「${categoryLabelOf(drill.category)}」当日窗内已加载的 ${l2WindowedItems.length} 条标为已读(作用域=所见行,服务端持久;历史/未翻页不动)`}
                  disabled={l2WindowedItems.length === 0 || l2WindowedItems.every((item) => item.read === true)}
                  onClick={() => markWindowScoped(true)}
                >
                  本品类窗内已读
                </Button>
                <Button
                  variant="ghost"
                  size="sm"
                  className="px-2 text-muted-foreground"
                  data-testid="feed-category-mark-unread"
                  aria-label={`把「${categoryLabelOf(drill.category)}」当日窗内已加载的 ${l2WindowedItems.length} 条恢复未读(反向出口)`}
                  title={`把「${categoryLabelOf(drill.category)}」当日窗内已加载的 ${l2WindowedItems.length} 条恢复未读(反向出口,误触可逆;作用域=所见行,服务端持久)`}
                  disabled={l2WindowedItems.length === 0 || l2WindowedItems.every((item) => item.read !== true)}
                  onClick={() => markWindowScoped(false)}
                >
                  窗内未读
                </Button>
              </span>
            ) : null}
          </div>
          {/* Telegram 监控台(10-09-tg-category-entry,主人令「点进 Telegram
              监控 = 浏览器网页扫码登录 + 持续监控」;AC6 归一后品类名 =
              Telegram 监控,台名随动):TG 品类渠道页顶部大卡——未登录给
              扫码入口,已登录显监控中;历史消息一跳直达。 */}
          {isTelegramCategory && tgWebline !== null ? (
            <div
              data-testid="feed-tg-console"
              className="rounded-md border border-primary/30 bg-primary/5 px-3 py-2.5"
            >
              <div className="flex flex-wrap items-center gap-2">
                <span className="text-sm font-medium text-foreground">Telegram 监控台</span>
                {tgWebline.web.accounts.some((a) => a.logged_in) ? (
                  <span
                    className="inline-flex items-center gap-1 text-2xs text-ok"
                    data-testid="feed-tg-console-live"
                  >
                    ● 监控中 · {tgWebline.web.accounts.filter((a) => a.logged_in).map((a) => a.account).join("、")}
                    {tgWebline.web.accounts.find((a) => a.logged_in)?.logged_in_at
                      ? ` · 自 ${formatAbsoluteTime(tgWebline.web.accounts.find((a) => a.logged_in)?.logged_in_at ?? null)}`
                      : ""}
                  </span>
                ) : (
                  <span className="text-2xs text-warning">
                    未登录 —— 扫码登录网页版 telegram,登录后 7×24 监控,新消息自动入库
                  </span>
                )}
                <span className="ml-auto flex items-center gap-1">
                  {!tgWebline.web.accounts.some((a) => a.logged_in) &&
                  tgWebline.web.accounts.length > 0 ? (
                    <Button
                      variant="outline"
                      size="sm"
                      className="h-6 px-2 text-2xs"
                      data-testid="feed-tg-console-login"
                      disabled={tgLoginBusy || tgWebline.web.accounts[0].login_in_progress}
                      onClick={() => void startWebLogin()}
                    >
                      {tgWebline.web.accounts[0].login_in_progress
                        ? "登录中…"
                        : tgLoginBusy
                          ? "拉起中…"
                          : "扫码登录网页版"}
                    </Button>
                  ) : null}
                  {/* 内置浏览器预览(AC11):应用内 WebviewWindow 直开频道公开
                      镜像;推导不出 = 置灰 + title 如实(不装死) */}
                  <Button
                    variant="outline"
                    size="sm"
                    className="h-6 px-2 text-2xs"
                    data-testid="feed-tg-console-preview"
                    disabled={tgPreviewUrl === null}
                    title={
                      tgPreviewUrl === null
                        ? "暂无可推导的 t.me 公开链接(私有频道或条目无链接),内置预览不可用"
                        : `内置浏览器预览:${tgPreviewUrl}`
                    }
                    onClick={() => tgPreviewUrl && openTgPreview(tgPreviewUrl)}
                  >
                    内置浏览器预览
                  </Button>
                  <Button
                    variant="ghost"
                    size="sm"
                    className="h-6 px-1.5 text-2xs"
                    onClick={() => navigate("/settings?section=telegram")}
                  >
                    管理
                  </Button>
                </span>
              </div>
              <button
                type="button"
                data-testid="feed-tg-console-history"
                onClick={openCategoryHistory}
                className="mt-1.5 inline-flex items-center gap-1 text-2xs text-primary hover:underline"
              >
                <Inbox aria-hidden className="size-3" />
                看全部历史消息(不限当日窗)
              </button>
              {tgPreviewNote ? (
                <span
                  className="mt-1 block text-2xs text-warning"
                  data-testid="feed-tg-console-preview-note"
                >
                  {tgPreviewNote}
                </span>
              ) : null}
            </div>
          ) : null}
          {/* 置顶:该品类全部渠道合流 */}
          {drillRow({
            testId: "feed-drill-cat-all",
            onOpen: openCategoryStream,
            icon: <Inbox aria-hidden className="size-4 shrink-0 text-primary" />,
            label: "全部渠道",
            meta: `品类 ${categoryLabelOf(drill.category)} · 今日 ${l2Channels.reduce((sum, channel) => sum + channel.today, 0)} 条 · 未读 ${l2Channels.reduce((sum, channel) => sum + channel.unread, 0)}`,
            color: categoryColor(drill.category),
          })}
          {l2Channels.length === 0 ? (
            isTelegramCategory ? (
              /* TG 品类空态(10-09-tg-category-entry):不再甩「先跑采集」
                  死胡同——监控在线给「新消息即时入库」预期 + 历史直达;
                  AC6 归一后口径 = 「Telegram 监控」,不再专属网页线一词 */
              <Card>
                <CardContent className="p-0">
                  <EmptyState
                    title="监控在线,窗内暂无新消息"
                    description="Telegram 监控在线,新消息入库即出现在这里;更早的入库记录点「看全部历史消息」直达。"
                  />
                </CardContent>
              </Card>
            ) : (
              <Card>
                <CardContent className="p-0">
                  <EmptyState
                    title="该品类暂无窗内条目"
                    description={`「${categoryLabelOf(drill.category)}」在当日窗(03:00 起)内没有条目;先跑一轮采集,或到「全部条目 · 滚动流」看历史。`}
                  />
                </CardContent>
              </Card>
            )
          ) : (
            <div className="flex flex-col gap-1.5" data-testid="feed-l2-channels">
              {l2Channels.map((channel) => {
                const kindMeta = CHANNEL_KIND_META[channel.kind];
                const KindIcon = kindMeta.Icon;
                return drillRow({
                  testId: `feed-drill-ch-${channel.key ?? "unknown"}`,
                  onOpen: () => channel.key !== null && openChannel(channel.key),
                  icon: <KindIcon aria-hidden className={`size-4 shrink-0 ${kindMeta.className}`} />,
                  label: channel.label,
                  meta: `${kindMeta.label}渠道 · 今日 ${channel.today} 条 · 未读 ${channel.unread}`,
                  color: null,
                });
              })}
            </div>
          )}
        </div>
      ) : (
        /* ═══ L3 消息流(分型呈现主场):工具条 + 列表区 ═══ */
        <>
          {/* 工具条:读态分段 + 计数/批量 + 右侧显示选项/搜索/刷新/导出
              (品类下拉退役 —— 品类选择 = L1/L2 层级本体;source 作用域下
              导出不出钮,feed.export 无 source 参数范围不实) */}
          <div className="flex flex-wrap items-center gap-2 px-6" data-testid="feed-toolbar">
            {/* 作用域标题(10-08 审计 F6):streamTitle 此前只进 sr-only,墙层
                用户看不到任何当前位置词 —— 提为工具条左侧可见文案(sr-only
                aria-live 保留,播报语义不变) */}
            <span className="text-xs font-medium text-foreground" data-testid="feed-stream-title">
              {streamTitle}
            </span>
            {/* 读态分段(KsFilter 范式):微填充容器 + 内钮 h-7,激活 = bg-accent */}
            <div
              role="group"
              aria-label="读态过滤"
              className="flex items-center gap-0.5 rounded-lg border border-border bg-muted/40 p-0.5"
            >
              {FILTERS.map((entry) => {
                const active = filter === entry.key;
                return (
                  <button
                    key={entry.key}
                    type="button"
                    aria-label={`过滤:${entry.label}`}
                    aria-pressed={active}
                    title={
                      entry.key === "unread"
                        ? "未读过滤会隐藏已加载行全已读的分组;切「全部」可恢复"
                        : undefined
                    }
                    onClick={() => setFilter(entry.key)}
                    className={
                      "h-7 rounded-md px-2.5 text-xs transition-colors duration-(--duration-fast) ease-out-expo " +
                      (active
                        ? "bg-accent font-medium text-foreground shadow-sm"
                        : "text-muted-foreground hover:text-foreground")
                    }
                  >
                    {entry.label}
                  </button>
                );
              })}
            </div>
            {/* 计数口径(10-08 审计 F2):hasMore(服务端返回满页)时「共/N 条」
                的全量词面是静默低估 —— 改「已加载 N 条」如实;未截断才可说
                「共」。根治(sidecar 窗内 count)待协议侧,前端先不再说满话 */}
            <span className="text-2xs text-muted-foreground" data-testid="feed-count">
              {hasMore
                ? filter === "all"
                  ? `已加载 ${items.length} 条(首页截断,更早条目未计入)`
                  : `已加载 ${visible.length} / ${items.length} 条`
                : filter === "all"
                  ? `共 ${items.length} 条`
                  : `${visible.length} / ${items.length} 条`}
            </span>
            {/* 当日窗知会(滚动流语义;仅未读/全部两档受窗,星标/稍后读跨窗可见) */}
            {filter === "unread" || filter === "all" ? (
              <span
                className="text-2xs text-muted-foreground"
                data-testid="feed-day-window"
                title={
                  drill.level === 3 && drill.history
                    ? "历史态:显示该作用域全部入库条目(不限当日窗);返回渠道页可回到滚动流。"
                    : `当日窗:每天 03:00 清零滚动流(03:00 → 次日 03:00),过窗条目离场、视图从零累计;store 数据不清(retention 照旧),星标/稍后读跨窗可见;实时滚动 = 采集事件即时刷新 + 30s 可见性轮询`
                }
              >
                {drill.level === 3 && drill.history ? "含历史 · 不限当日窗" : "当日窗 03:00 起 · 实时滚动"}
              </span>
            ) : null}
            {searchActive ? (
              <span className="text-2xs text-muted-foreground" data-testid="feed-search-scope">
                服务端搜索「{query}」
                {streamScope.category ? ` × 品类 ${categoryLabelOf(streamScope.category)}` : ""}
                {streamScope.source ? ` × 渠道 ${streamScope.source}` : ""}
                {streamScope.sourceKind ? ` × ${streamScope.sourceKind === "web" ? "网页" : "Telegram"}` : ""} × 本地
                {FILTERS.find((entry) => entry.key === filter)?.label}过滤
              </span>
            ) : null}
            {!bulkHidden && confirmAllMark === null ? (
              <>
                <Button
                  variant="ghost"
                  size="sm"
                  className="px-2 text-xs text-muted-foreground"
                  aria-label="全部标已读"
                  title={markAllReadTitle}
                  onClick={() => setConfirmAllMark("read")}
                  disabled={items.length === 0 || unreadLoaded === 0}
                >
                  全部标已读
                </Button>
                <Button
                  variant="ghost"
                  size="sm"
                  className="px-2 text-xs text-muted-foreground"
                  aria-label="全部标未读"
                  title={markAllUnreadTitle}
                  onClick={() => setConfirmAllMark("unread")}
                  disabled={items.length - unreadLoaded === 0}
                >
                  全部标未读
                </Button>
              </>
            ) : null}
            {!bulkHidden && confirmAllMark !== null ? (
              <span
                data-testid="feed-confirm-all-group"
                className="flex items-center gap-0.5"
                onBlur={(event) => {
                  const next = event.relatedTarget;
                  if (next instanceof Node && event.currentTarget.contains(next)) return;
                  setConfirmAllMark(null);
                }}
              >
                <Button
                  variant="destructive"
                  size="sm"
                  className="px-2 text-xs"
                  autoFocus
                  aria-label={confirmAllMark === "read" ? "确认全部标已读" : "确认全部标未读"}
                  title={confirmAllMark === "read" ? markAllReadTitle : markAllUnreadTitle}
                  onClick={() => {
                    const value = confirmAllMark === "read";
                    setConfirmAllMark(null);
                    markAllRead(value, bulkScopeCategory ?? undefined, bulkScopeKind);
                  }}
                >
                  {confirmAllMark === "read" ? "确认全部标已读" : "确认全部标未读"}
                </Button>
                <Button
                  variant="ghost"
                  size="sm"
                  className="px-2 text-xs text-muted-foreground"
                  onClick={() => setConfirmAllMark(null)}
                >
                  取消
                </Button>
              </span>
            ) : null}
            <div className="ml-auto flex items-center gap-2">
              {/* 显示选项:未读优先 + 分组维度(时间/不分组;品类维度 = L1/L2
                  层级本体,L3 不再重复) */}
              <DropdownMenu>
                <DropdownMenuTrigger asChild>
                  <Button
                    variant="outline"
                    size="sm"
                    aria-label="显示选项"
                    title="显示选项:未读优先 / 分组维度(本地记忆)"
                  >
                    <SlidersHorizontal className="size-3.5" />
                    显示
                    <ChevronDown className="size-3.5" />
                  </Button>
                </DropdownMenuTrigger>
                <DropdownMenuContent align="end">
                  <DropdownMenuLabel>显示</DropdownMenuLabel>
                  <DropdownMenuItem
                    onClick={() => updateDisplay({ ...display, unreadFirst: !display.unreadFirst })}
                    title="未读条目浮到列表前(未读/已读各自稳定保序)"
                  >
                    {display.unreadFirst ? (
                      <Check className="size-3.5" />
                    ) : (
                      <span className="size-3.5" aria-hidden />
                    )}
                    未读优先
                  </DropdownMenuItem>
                  <DropdownMenuSeparator />
                  <DropdownMenuLabel>分组</DropdownMenuLabel>
                  <DropdownMenuItem onClick={() => updateDisplay({ ...display, groupMode: "time" })}>
                    {display.groupMode !== "none" ? (
                      <Check className="size-3.5" />
                    ) : (
                      <span className="size-3.5" aria-hidden />
                    )}
                    时间分组(今天 / 昨天 / 7 天内 / 更早)
                  </DropdownMenuItem>
                  <DropdownMenuItem onClick={() => updateDisplay({ ...display, groupMode: "none" })}>
                    {display.groupMode === "none" ? (
                      <Check className="size-3.5" />
                    ) : (
                      <span className="size-3.5" aria-hidden />
                    )}
                    不分组(平铺)
                  </DropdownMenuItem>
                </DropdownMenuContent>
              </DropdownMenu>
              {/* KsFilter 搜索位:前导图标入框,Mod+F 聚焦与 Esc 即时清空保留 */}
              <div className="relative">
                <Search
                  aria-hidden
                  className="pointer-events-none absolute top-1/2 left-2.5 size-3.5 -translate-y-1/2 text-muted-foreground/70"
                />
                <Input
                  ref={searchInputRef}
                  type="search"
                  value={searchInput}
                  aria-label="搜索条目"
                  placeholder="搜索标题 / 摘要 / 来源(服务端,当前作用域)"
                  className="w-64 pl-8 text-xs"
                  onChange={(event) => setSearchInput(event.target.value)}
                  onKeyDown={(event) => {
                    if (event.key === "Enter") setQuery(searchInput.trim());
                    if (event.key === "Escape") {
                      setSearchInput("");
                      setQuery("");
                    }
                  }}
                />
              </div>
              {/* KsFilter refresh 位:重发当前 品类 × 渠道 × 搜索词 的查询 */}
              <Button
                variant="ghost"
                size="icon"
                className="size-8"
                aria-label="刷新"
                title="重新拉取当前作用域的条目(品类 × 渠道 × 搜索词)"
                onClick={() => void refresh()}
                disabled={loading}
              >
                <RefreshCw className={loading ? "size-3.5 animate-spin" : "size-3.5"} />
              </Button>
              {/* G3 导出组(仅 source 未定作用域:feed.export 无 source 参数,
                  渠道流不出钮防范围不实) */}
              {streamScope.source === null ? (
                <div className="flex items-center gap-2">
                  <div
                    role="group"
                    aria-label="导出格式"
                    className="flex items-center gap-0.5 rounded-md border border-(--control-border) bg-(--control-bg) p-0.5"
                  >
                    <Button
                      variant={exportFormat === "jsonl" ? "secondary" : "ghost"}
                      size="sm"
                      className="h-6 gap-0 px-2 text-xs"
                      aria-pressed={exportFormat === "jsonl"}
                      title={`JSON Lines 格式(默认文件名 ${defaultExportName("jsonl")})`}
                      onClick={() => setExportFormat("jsonl")}
                    >
                      JSONL
                    </Button>
                    <Button
                      variant={exportFormat === "csv" ? "secondary" : "ghost"}
                      size="sm"
                      className="h-6 gap-0 px-2 text-xs"
                      aria-pressed={exportFormat === "csv"}
                      title={`CSV 格式(默认文件名 ${defaultExportName("csv")})`}
                      onClick={() => setExportFormat("csv")}
                    >
                      CSV
                    </Button>
                  </div>
                  <Button
                    variant="outline"
                    size="sm"
                    onClick={() => void exportCurrentView()}
                    disabled={exporting}
                    title="导出当前过滤视图(品类 × 搜索词)为本地文件"
                  >
                    <Download className={exporting ? "size-3.5 animate-pulse" : "size-3.5"} />
                    {exporting ? "导出中…" : "导出当前视图"}
                  </Button>
                </div>
              ) : null}
            </div>
          </div>

          {/* 列表区(内滚):导出回执/错误横幅/加载/空态/分组列表都在滚动面内 */}
          <div className="flex min-h-0 flex-1 flex-col gap-3 overflow-y-auto px-6 pb-6" data-testid="feed-l3">
            <span className="sr-only" aria-live="polite">{streamTitle}</span>
            {exportNote ? (
              <p className="text-xs text-muted-foreground" data-testid="feed-export-result">
                {exportNote}
              </p>
            ) : null}
            {openError ? (
              <p className="text-xs text-destructive" data-testid="feed-open-error">
                打开原文失败:{openError}
              </p>
            ) : null}
            {markError ? (
              <p className="text-xs text-destructive" data-testid="feed-mark-error">
                标记状态失败(已回滚):{markError}
              </p>
            ) : null}

            {error ? (
              <Card data-testid="feed-error">
                <CardContent className="flex flex-col gap-1.5 pt-1">
                  {error.code === "pyenv_not_ready" ? (
                    <>
                      <p className="text-sm font-medium text-warning">{error.message}</p>
                      <a
                        href="#/settings?section=python-env"
                        className="w-fit text-xs text-link underline underline-offset-2 hover:text-link/80"
                      >
                        前往设置 →「Python 环境」完成配置(就绪后情报流自动恢复)
                      </a>
                    </>
                  ) : (
                    <>
                      <p className="text-sm font-medium text-destructive">
                        情报流不可用(sidecar 错误码 {error.code})
                      </p>
                      <p className="text-xs text-muted-foreground">{error.message}</p>
                      <Button
                        variant="outline"
                        size="sm"
                        className="w-fit"
                        onClick={() => void refresh()}
                        disabled={loading}
                      >
                        <RefreshCw className={loading ? "size-3.5 animate-spin" : "size-3.5"} />
                        重试
                      </Button>
                    </>
                  )}
                </CardContent>
              </Card>
            ) : null}

            {loading && items.length === 0 ? (
              // 三态(frontend-ui-engineering):骨架块贴新卡三级形状
              <div className="flex flex-col gap-1.5" data-testid="feed-loading" aria-busy="true" aria-label="情报流加载中">
                {[0, 1, 2, 3].map((row) => (
                  <div key={row} className="rounded-md border border-border/50 px-3 py-2">
                    <div className="flex items-center justify-between gap-2 pr-1">
                      <Skeleton className="h-4 w-2/3" />
                      <Skeleton className="h-3 w-14" />
                    </div>
                    <div className="mt-1.5 flex items-center gap-1.5">
                      <Skeleton className="h-3 w-16" />
                      <Skeleton className="h-3 w-20" />
                      <Skeleton className="h-3 w-12" />
                    </div>
                    <Skeleton className="mt-1.5 h-4 w-full" />
                    <Skeleton className="mt-1 h-4 w-4/5" />
                  </div>
                ))}
              </div>
            ) : !error && visible.length === 0 ? (
              items.length === 0 && searchActive ? (
                <Card data-testid="feed-search-empty">
                  <CardContent className="p-0">
                    <EmptyState
                      title="没有匹配的条目"
                      description={`服务端搜索「${query}」零命中;换个关键词,或清空搜索看全部条目。`}
                    />
                  </CardContent>
                </Card>
              ) : items.length === 0 ? (
                <Card>
                  <CardContent className="p-0">
                    <EmptyState title={EMPTY_TEXT[filter].title} description={EMPTY_TEXT[filter].description} />
                  </CardContent>
                </Card>
              ) : (
                <Card>
                  <CardContent className="p-0">
                    <EmptyState title={EMPTY_TEXT[filter].title} description={EMPTY_TEXT[filter].description} />
                  </CardContent>
                </Card>
              )
            ) : wallLayout ? (
              /* ═══ 卡片墙(v2 第一层,主人令「网页集中在一起,其他通讯软件
                  一个通讯软件一个卡片,点击进入第二层才是详情展示」):
                  网页一张 + 每通讯软件一张,散条目卡退场 ═══ */
              wallCards.length > 0 ? (
                <section aria-label="来源卡片墙" data-testid="feed-kind-wall" className="flex flex-col gap-1.5">
                  {wallCards.map((card) => (
                    <SourceKindCard
                      key={card.key}
                      card={card}
                      onOpen={() => openKind(card.key)}
                      truncated={hasMore}
                      subRows={streamKindSubRows(displayItems, states, card.key)}
                      navFocused={currentKey === `kind:${card.key}` && navByKeyboard}
                      onCurrent={() => onCurrentCard(`kind:${card.key}`)}
                    />
                  ))}
                </section>
              ) : null
            ) : imDetailLayout ? (
              /* ═══ Telegram 分节详情(v2 第二层,决议「按频道分节全铺」):
                  节头 = 细条节头(F3:频道名+条数/未读+chevron,不再复述最新
                  一条 —— 此前节头大卡与节内首条气泡背靠背重复同一消息),
                  节内消息全量平铺,不点也能同屏看完全部消息 ═══ */
              imDetailCards.length > 0 ? (
                <div className="flex flex-col gap-4" data-testid="feed-im-sections">
                  {/* 网页线监控状态条(10-09-tg-category-entry,主人令「扫码
                      登录,一直监控网页上的数据」入口打通):已登录 = 监控中
                      +管理跳转;未登录 = 扫码登录直达(浏览器模块统一入口);
                      快照拉取失败 = 条不出,不拦浏览。 */}
                  {tgWebline !== null ? (
                    <div
                      data-testid="feed-tg-webline-strip"
                      className="flex flex-wrap items-center gap-2 rounded-md border border-border/60 bg-muted/20 px-3 py-2 text-2xs text-muted-foreground"
                    >
                      <span className="font-medium text-foreground/80">Telegram 监控 · 网页线</span>
                      {tgWebline.web.accounts.length === 0 ? (
                        <>
                          <span>尚未配置网页线账号</span>
                          <Button
                            variant="ghost"
                            size="sm"
                            className="h-5 px-1.5 text-2xs"
                            onClick={() => navigate("/settings?section=telegram")}
                          >
                            前往设置 · Telegram
                          </Button>
                        </>
                      ) : tgWebline.web.accounts.some((a) => a.logged_in) ? (
                        <>
                          <span className="inline-flex items-center gap-1 text-ok" data-testid="feed-tg-webline-live">
                            ● 监控中 · {tgWebline.web.accounts.filter((a) => a.logged_in).map((a) => a.account).join("、")}
                          </span>
                          <Button
                            variant="ghost"
                            size="sm"
                            className="h-5 px-1.5 text-2xs"
                            onClick={() => navigate("/settings?section=telegram")}
                          >
                            管理 → 设置 · Telegram
                          </Button>
                        </>
                      ) : (
                        <>
                          <span className="text-warning">未登录 —— 扫码登录后即常驻监控,随时随地带数据</span>
                          <Button
                            variant="outline"
                            size="sm"
                            className="h-5 px-1.5 text-2xs"
                            data-testid="feed-tg-webline-login"
                            disabled={tgLoginBusy || tgWebline.web.accounts[0].login_in_progress}
                            onClick={() => void startWebLogin()}
                          >
                            {tgWebline.web.accounts[0].login_in_progress
                              ? "登录中…"
                              : tgLoginBusy
                                ? "拉起中…"
                                : `扫码登录(${tgWebline.web.accounts[0].account})`}
                          </Button>
                        </>
                      )}
                    </div>
                  ) : null}
                  {imDetailCards.map((card) => (
                    <section key={card.key} aria-label={`Telegram 频道:${card.label}`}>
                      <TgSectionHeader card={card} onOpen={() => openChannelFromStream(card.key)} />
                      <div className="mt-1 flex flex-col gap-1.5">
                        {displayItems
                          .filter((item) => item.source === card.key)
                          .map(renderCard)}
                      </div>
                    </section>
                  ))}
                </div>
              ) : null
            ) : (
              <>
                {/* TG 渠道卡区(10-08-tg-channel-card v1 形态,未过源大类门
                    时回落;过门后 tgCards 恒空 = 零渲染):可见集含 TG 条目时
                    置顶呈现,每渠道一卡;消息列表本体不再逐条铺 TG 卡。 */}
                {tgCards.length > 0 ? (
                  <section aria-label="TG 频道" data-testid="feed-tg-channels" className="flex flex-col gap-1.5">
                    <div className="flex items-center gap-2 py-0.5">
                      <span className="text-2xs font-medium text-muted-foreground">TG 频道</span>
                      <span className="text-2xs text-muted-foreground">{tgCards.length} 个</span>
                      <span aria-hidden className="h-px flex-1 bg-border/70" />
                    </div>
                    {tgCards.map((card) => (
                      <TgChannelCard key={card.key} card={card} onOpen={() => openChannelFromStream(card.key)} />
                    ))}
                  </section>
                ) : null}
                {/* 时间分组头(D4):sticky 组头 + 组内卡片(渠道分型呈现);
                    10-08 起 TG 条目折叠进渠道卡区(v1)/网页详情平铺(v2),
                    分组吃 streamItems */}
                {groups !== null ? (
                  <div className="flex flex-col gap-4">
                    {groups.map((group) => (
                      <section key={group.key} aria-label={`时间分组:${group.label}`}>
                        <div
                          data-testid={`feed-group-${group.label}`}
                          className={
                            chatStyleGroups
                              ? "mx-auto w-fit rounded-full bg-muted/60 px-3 py-1 text-2xs text-muted-foreground"
                              : "sticky top-0 z-10 -mx-6 flex items-center gap-2 bg-background/95 px-6 py-2.5 backdrop-blur-sm"
                          }
                        >
                          {chatStyleGroups ? (
                            `${group.label} · ${group.items.length} 条`
                          ) : (
                            <>
                              <span className="text-2xs font-medium text-muted-foreground">{group.label}</span>
                              <span className="text-2xs text-muted-foreground">{group.items.length} 条</span>
                              <span aria-hidden className="h-px flex-1 bg-border/70" />
                            </>
                          )}
                        </div>
                        {/* 组内行距 6px(Kestra 列表密度档) */}
                        <div className="flex flex-col gap-1.5">{group.items.map(renderCard)}</div>
                      </section>
                    ))}
                  </div>
                ) : (
                  // 不分组:平铺(行距同组内 6px 密度档)
                  <div className="flex flex-col gap-1.5" data-testid="feed-flat-list">
                    {streamItems.map(renderCard)}
                  </div>
                )}
              </>
            )}

            {hasMore && !loading ? (
              <Button variant="outline" size="sm" className="self-center" onClick={() => void loadMore()} disabled={loadingMore}>
                {loadingMore ? "加载中…" : "加载更早的条目"}
              </Button>
            ) : null}
          </div>
        </>
      )}

      {/* 消息详情弹窗(主人令「点击信息,弹出详情」):Portal 渲染,Esc/遮罩
          点击关闭(ui/dialog.tsx 基件);动作簇复用卡内既有实现 */}
      {detailItem !== null ? (
        <FeedItemDetail
          item={detailItem}
          state={states[itemKey(detailItem)] ?? {}}
          kind={channelKindOf(detailItem, engineBySource)}
          onClose={closeDetail}
          onToggle={toggle}
          onOpenError={setOpenError}
        />
      ) : null}
    </div>
  );
}
