import { memo, useCallback, useEffect, useMemo, useRef, useState } from "react";
import {
  Bookmark,
  Check,
  ChevronDown,
  ChevronRight,
  Copy,
  Download,
  ExternalLink,
  FileText,
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
  cardDigest,
  categoryColor,
  channelCardKindOf,
  channelDisplayName,
  channelKindOf,
  dayWindowStart,
  DEFAULT_FEED_DISPLAY,
  dealPriceView,
  defaultExportName,
  engineMapFromHealth,
  exportFeedView,
  feedChannelCards,
  fetchFeedPage,
  filterChannelsByQuery,
  formatRelativeTime,
  groupFeedItems,
  importLocalFeedStates,
  isOpenableUrl,
  itemKey,
  KEYWORD_MAX_CHARS,
  LATER_RESURFACE_DAYS,
  listYamlTargets,
  LIVE_POLL_INTERVAL_MS,
  COUNT_PROTOCOL,
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
  statesFromItems,
  telegramMirrorUrlOf,
  toggleMarker,
  type ChannelCardKind,
  type ChannelKind,
  type ExportFormat,
  type FeedChannelCardData,
  type FeedDisplayOptions,
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

/** 渠道卡类型元(v6 渠道墙):三档徽标词/图标/色调(条目级 CHANNEL_KIND_META
 *  的渠道级姊妹; TG = Send 品牌紫 / 网站 = Rss 灰 / 日报 = FileText 淡紫) */
const CHANNEL_CARD_META: Record<ChannelCardKind, { label: string; Icon: typeof Rss; className: string }> = {
  tg: { label: "TG", Icon: Send, className: "text-primary" },
  site: { label: "网站", Icon: Rss, className: "text-muted-foreground" },
  daily: { label: "日报", Icon: FileText, className: "text-primary/80" },
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

/** React.memo:悬停 onCurrent 只改 currentKey,未记忆化时整墙 50+ 卡全量
 *  重渲染(CSS columns 下放大为主人实测的悬停闪动);state 空对象用
 *  模块级常量保身份稳定,marked 卡仅在 toggle 时换身份。 */
const FEED_CARD_NO_STATE: { read?: boolean; starred?: boolean; later?: boolean } = {};

const FeedCard = memo(function FeedCard({
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
            j/k 键盘聚焦 = ring 环(A-feed;hover 只置 current 不亮环,Linear 式)。
            P2-3 拉出泡根(10-09-tg-category-entry,v4 深检遗留翻案):telegram
            卡根只留布局(w-fit 窄泡/min-w/max-w/relative 定位锚)与 data-*,
            底色 = 中性卡底(bg-card,展开态富块落点);未读/已读着色底收编进
            气泡 div —— 富块(OCR/图说/图文件/enrich/沉淀面板)作为泡外兄弟
            节点,不再渲染在着色泡内呈双泡观感。悬停操作簇(absolute 根锚)/
            右键/j-k 定位(root data-item-key)不动。 */}
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
          className={`group/feed-item relative ${
            kind === "telegram"
              ? "w-fit min-w-[13rem] max-w-[min(100%,640px)] rounded-md border border-border/40 bg-card py-2 pl-3 pr-3"
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
              点击正文/摘要 = 详情弹窗(弹开即记已读)。P2-3:着色底收编于此
              (未读亮泡 primary/10 / 已读降档 muted,v4 AC12 口径不变,仅从
              根容器下移;hover 提亮随 group/feed-item 联动,观感同前)。 */}
          {!inChannelSection ? (
            <div className="flex items-center gap-1 text-2xs font-medium text-link">
              <Send aria-hidden className="size-3 shrink-0" />
              <span className="min-w-0 truncate">{channelDisplayName(item.source)}</span>
            </div>
          ) : null}
          <div
            className={`mt-0.5 rounded-2xl rounded-tl-md border px-3 py-2 ${
              state.read
                ? "border-border/40 bg-muted/25 group-hover/feed-item:bg-muted/40"
                : "border-primary/25 bg-primary/10 group-hover/feed-item:bg-primary/15"
            }`}
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
});

/**
 * 渠道行(v7 AC25,双栏监控台的右栏「群组列表」行;镜像 TG 桌面聊天列表的
 * 两行密度,借形不改语义):一行一渠道 —— 类型头像 chip(圆角方 size-8,
 * 内置类型图标 + 同色系淡档底,头像位即类型徽标不再挂 Badge 词标)+
 * 渠道名(channelDisplayName 词表)+ 最新相对时间(mono);行 2 = 最新一条
 * 预览(cardDigest,F6 同文回退标题,零条目 = 知会词)+ 未读徽标(unread
 * >0 才渲染,9+ 截断)。选中高亮 = bg-accent 填充 + 渠道名转 text-link
 * (Kestra NavRow「填充 + 文字色」范式);hover = bg-accent/50;键盘巡游环
 * = ring(仅 navByKeyboard 时)。计数 title 沿用「已加载口径」真话(全库
 * 首页 50 条铺底)。memo 同 FeedCard(hover onCurrent 只改 listCurrentKey)。
 */
/** 类型头像 chip 底色档(v7 右栏行):同色系淡档,头像位即类型徽标 */
const CHANNEL_ROW_AVATAR_TONE: Record<ChannelCardKind, string> = {
  tg: "bg-primary/10 text-primary",
  site: "bg-muted text-muted-foreground",
  daily: "bg-primary/5 text-primary/80",
};

const ChannelRow = memo(function ChannelRow({
  card,
  selected,
  current,
  navFocused,
  onCurrent,
  onOpen,
}: {
  card: FeedChannelCardData;
  /** 选中高亮(scope.source === card.key;bg-accent 填充 + 名字转 link 色) */
  selected: boolean;
  /** 键盘「当前行」(j/k 右栏环作用目标;hover/focus 进入时置位) */
  current: boolean;
  /** j/k 键盘巡游聚焦(focus 环呈现与否,仅右栏环巡游时) */
  navFocused: boolean;
  onCurrent: (key: string) => void;
  onOpen: (key: string) => void;
}) {
  const meta = CHANNEL_CARD_META[card.kind];
  const KindIcon = meta.Icon;
  const digest = card.latest ? cardDigest(card.latest) : null;
  // 深检 F6:短消息(TG 入库常态,title==content≤100 字)经 bodyWithoutTitleDup
  // 去重后 digest = null —— 回退渲染标题作预览,「最新一条预览」不因同文形态
  // 整行消失(仅零条目渠道才落知会词)。
  const preview =
    digest ?? (card.latest ? card.latest.title || card.latest.url : null);
  const time = card.latest ? formatRelativeTime(card.latest.first_seen) : null;
  return (
    <div
      data-testid={`feed-channel-row-${card.key}`}
      data-item-key={card.key}
      data-channel-kind={card.kind}
      data-selected={selected ? "true" : "false"}
      data-unread={card.unread > 0 ? "true" : "false"}
      data-current={current ? "true" : "false"}
      data-nav-focused={navFocused ? "true" : "false"}
      role="button"
      tabIndex={0}
      aria-current={selected ? "true" : undefined}
      aria-label={`打开渠道:${card.label}`}
      onMouseEnter={() => onCurrent(card.key)}
      onFocus={() => onCurrent(card.key)}
      onClick={() => onOpen(card.key)}
      onKeyDown={(event) => {
        // Space = ARIA 按钮激活语义(深检 F5;preventDefault 防页滚)。Enter
        // 让位全局巡游线(v7 §4「Enter 落点跟随当前环」+ 真机实证):行持
        // 焦点时按 Enter,行内激活与全局环 Enter(可能落在左栏条目环开详情)
        // 同键并发 —— React 18 discrete 事件下行内 setState 同步 flush 抢先
        // 复位环状态,全局线读到回退态落错分支。行 onFocus/onMouseEnter 已
        // 把 listCurrentKey 置为本行,Enter 归全局线同样打开本行,语义无损。
        if (event.key === " ") {
          event.preventDefault();
          onOpen(card.key);
        }
      }}
      className={`relative cursor-pointer ${
        selected ? "bg-accent" : "hover:bg-accent/50"
      }${navFocused ? " ring-1 ring-primary/60" : ""}`}
    >
      <div className="flex items-start gap-2.5 px-2.5 py-2">
        {/* 类型头像 chip:图标 + 色调按 CHANNEL_CARD_META 词表,底色同色系淡档 */}
        <span
          aria-hidden
          className={`mt-0.5 flex size-8 shrink-0 items-center justify-center rounded-md ${CHANNEL_ROW_AVATAR_TONE[card.kind]}`}
        >
          <KindIcon className="size-4" />
        </span>
        <div className="min-w-0 flex-1">
          {/* 行 1:渠道名 + 最新相对时间(零条目不显) */}
          <div className="flex items-baseline justify-between gap-2">
            <span
              className={`min-w-0 truncate text-sm font-medium ${selected ? "text-link" : "text-foreground"}`}
              title={card.key}
            >
              {card.label}
            </span>
            {time !== null ? (
              <time
                dateTime={card.latest?.first_seen ?? undefined}
                className="shrink-0 font-mono text-2xs text-muted-foreground"
              >
                {time}
              </time>
            ) : null}
          </div>
          {/* 行 2:最新预览(cardDigest;同文回退标题,F6;零条目给知会词)+
              未读徽标(unread >0 才渲染,9+ 截断;title 注已加载口径真话) */}
          <div className="mt-0.5 flex items-center justify-between gap-2">
            <p className="min-w-0 truncate text-xs text-muted-foreground">
              {preview ?? "今日暂无新条目"}
            </p>
            {card.unread > 0 ? (
              <span
                data-testid={`feed-channel-unread-${card.key}`}
                className="min-w-5 shrink-0 rounded-full bg-primary px-1.5 text-center text-2xs font-medium text-primary-foreground tabular-nums"
                title="已加载口径:未读 = 已加载条目中的未读(不限今日)。首屏铺底为全库首页 50 条,更早条目未计入。"
              >
                {card.unread > 9 ? "9+" : card.unread}
              </span>
            ) : null}
          </div>
        </div>
      </div>
    </div>
  );
});

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

/** sidecar 错误卡(pyenv_not_ready 引导 / 通用重试):v7 落位 = 左栏主体位
 *  —— catalog 域错 = 总览态显示;stream 域错 = 选中态显示(两态互斥,双票
 *  守卫防旧域错误污染新域)。 */
function FeedErrorCard({
  error,
  onRetry,
  busy,
}: {
  error: SidecarRequestError;
  onRetry: () => void;
  busy: boolean;
}) {
  return (
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
            <Button variant="outline" size="sm" className="w-fit" onClick={onRetry} disabled={busy}>
              <RefreshCw className={busy ? "size-3.5 animate-spin" : "size-3.5"} />
              重试
            </Button>
          </>
        )}
      </CardContent>
    </Card>
  );
}

/**
 * 情报流:条目卡片列表 + 未读/星标/稍后读三态(本地态,localStorage 持久)
 * + 游标分页加载(见 ./api 的协议缺口注记)+ 服务端搜索(G1,防抖/Enter
 * 提交,query 随游标透传)+ 屏内品类下拉服务端过滤(10-04-topbar-cleanup
 * 归位)+ 卡片展开/打开原文(G2)+ 导出当前视图(G3,dialog.save → feed.export)。
 *
 * v7 双栏监控台(10-10,主人定调「右侧是群组,左侧是群组中的数据」+「先
 *  进行计划设计,再进行重构」,镜像 Telegram 桌面但群组列表在右是主人明确
 *  指定):**右栏 = 渠道/群组列表(aside,导航本体,常驻;ChannelRow 两行
 *  密度,搜索置顶过滤,选中行 bg-accent 高亮)+ 左栏 = 选中渠道的数据主区
 *  (section:工具条分叉 + TG 监控台降常驻条 + 时间线滚动区;未选中 = 引导
 *  空态)**。没有「落地页 → 详情页」切换,只有「选中 → 载入数据」——瀑布流
 *  落地页/渠道行导航页/返回动线全部收编进这一屏(v6 渠道详情整页单列 +
 *  大片空白被主人截图点名,双栏收编)。数据接线 = 双缓冲(§3.2 最关键结构
 *  改动):catalogItems 全库铺底只喂右栏聚合,streamItems 选中渠道流只喂
 *  左栏;读态 = 双缓冲并集投影(右栏徽标与左栏气泡同源联动)。键盘双环
 *  (§4):j/k = 右栏行,Shift+J/K = 左栏条目,Enter/U 落点跟随当前环,
 *  U 右栏环 = 当前渠道已加载条目一键标已读(triage);Esc 清选中回总览
 *  (弹窗开着让位);Mod+F 直聚焦右栏搜索框(searchFocusPending 补焦机制
 *  随搜索框常驻退役)。R1 吸收:选中态计数 title 删「当日窗视图首页」残词;
 *  R2 吸收:tgStatusPhase 三态机,首拉在途不出「状态未知」卡。
 *
 * v6 渠道瀑布流信息架构(10-09-tg-category-entry,主人三次纠偏后的最终
 * 定调:「每条情报流中的卡片表示一种情报支持性渠道」「从哪种渠道中获取
 * 信息,才是能集中到一个卡片里面的」「点击卡片进入这个情报获取的详情」):
 * **卡片 = 信息获取渠道**(一个网站/一个 TG 频道/一个日报源),不是单条
 * 消息也不是分类——首屏 = 渠道瀑布流(AC20:全集 = health sources ∪ 已加载
 * 条目 source 去重,零条目渠道也出卡;卡面 = 类型徽标 + 渠道名 + 最新一条
 * cardDigest 预览 + 今日 N · 未读 M,计数 title 注明已加载口径);搜索 =
 * 客户端过滤渠道卡(AC21:渠道名/源 id 包含匹配,清空恢复);点渠道卡 =
 * 该渠道条目流详情(AC22:复用 source 作用域查询,TG = 聊天气泡时间线,
 * 网站/日报 = 条目卡瀑布流,加载更早照旧,条目点击 = 详情弹窗;TG 渠道
 * 详情顶部保留监控台)。v5 的消息瀑布流首屏/品类·渠道筛选 chips/搜索全库
 * 检索随 AC23 退场;读态分段/刷新/导出/显示选项/键盘 j-k-U-Enter 保留并随
 * 新 IA 归位(读态分段与显示选项 = 渠道详情内条目流语义;U 在渠道墙上
 * 降级为无操作——渠道卡无单键读态语义,Enter = 进详情)。
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
  /** v7 双栏监控台信息架构(10-10,主人定调「右侧是群组,左侧是群组中的
   *  数据」):无「落地页 → 详情页」页面切换,只有「选中 → 载入数据」——
   *  右栏 = 渠道/群组列表(导航本体,常驻);左栏 = 选中渠道的数据主区。
   *  scope.source = null 即「总览态」(左栏出引导空态);非 null = 该渠道
   *  条目流(source 精确等值查询)+ history 历史态(TG 监控台「看全部
   *  历史消息」,读态过滤豁免)。作用域是屏内 state,不进路由。 */
  const [scope, setScope] = useState<{
    /** null = 总览态(左栏引导空态);非 null = 选中渠道,左栏出其条目流 */
    source: string | null;
    /** 含历史态(监控台入口):读态过滤豁免,已读未读全显 */
    history: boolean;
  }>({ source: null, history: false });
  /** 总览态派生总开关(v6 wallMode 改名不改形:null = 无选中渠道) */
  const overviewMode = scope.source === null;
  /** 计数口径能力门(10-09-tg-category-entry F2 根治):protocol ≥
   *  COUNT_PROTOCOL = store.items 支持 with_total → 首拉带全量计数,
   *  词面「已加载 N · 共 T 条」;未过门/应答无 total = 回落「已加载 N 条」。
   *  SOURCE_KIND_PROTOCOL 门随 v5 信息架构退役:web/im 源大类视图撤销,
   *  查询不再携 source_kind —— 低版本 sidecar 的回退语义 = 与新面同构,
   *  仅少 total 词面(version 探测与读态/计数门保留,合流同一次调用)。 */
  const [countReady, setCountReady] = useState(false);
  /** 源名→engine 映射(右栏渠道全集词表源 + 类型徽标判定;
   *  health().plugins 派生,挂载一次,零新 RPC;health 失败 = 空映射,
   *  渠道全集退化为已加载条目 source、类型退化为源名前缀判定) */
  const [engineBySource, setEngineBySource] = useState<Map<string, string>>(new Map());
  /** 双缓冲(v7 §3.2,本批最关键结构改动):单一 items 同时喂「右栏聚合」
   *  与「左栏流」会把右栏其他行的数据饿死 —— 拆两域。catalogItems = 全库
   *  铺底(首页 50,只喂右栏:channelCards 聚合 + 总览统计);streamItems
   *  = 选中渠道条目流(全套游标机件,仅选中态拉取,总览态清空)。 */
  const [catalogItems, setCatalogItems] = useState<FeedItem[]>([]);
  const [streamItems, setStreamItems] = useState<FeedItem[]>([]);
  /** catalog 首拉应答已落(v7 §2.4 冷启动防闪:总览态 firstRun/空流 CTA
   *  以此为门,catalog 在途一拍不出 CTA 免闪现) */
  const [catalogLoaded, setCatalogLoaded] = useState(false);
  const [catalogLoading, setCatalogLoading] = useState(true);
  const [catalogError, setCatalogError] = useState<SidecarRequestError | null>(null);
  /** 未过门通路的本地态(localStorage 持久;过门后状态源 = 条目派生,不再读写) */
  const [localStates, setLocalStates] = useState<FeedStateMap>({});
  const [filter, setFilter] = useState<FeedFilter>("unread");
  /** A-feed 显示选项:未读优先 + 分组维度(本地持久,进屏 loadFeedDisplay 回填) */
  const [display, setDisplay] = useState<FeedDisplayOptions>(DEFAULT_FEED_DISPLAY);
  // ── stream 域游标机件(v6 items 全套对票迁入,仅选中态活跃)──
  const [cursor, setCursor] = useState<string | null>(null);
  /** 复合游标第二键(同刻条目翻页不跳不重;C1) */
  const [cursorId, setCursorId] = useState<number | null>(null);
  const [hasMore, setHasMore] = useState(false);
  /** 同条件全量计数(F2 根治;过 COUNT_PROTOCOL 门且应答带 total 才非 null):
   *  「已加载 N · 共 T 条」的 T。随 refresh/liveRefresh 整页重查刷新(loadMore
   *  游标翻页不改 total —— 同 WHERE 计数与翻页无关);切作用域重查自然重置。 */
  const [total, setTotal] = useState<number | null>(null);
  const [loading, setLoading] = useState(false);
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
  const [tgWebline, setTgWebline] = useState<TelegramStatus | null>(null);
  const [tgLoginBusy, setTgLoginBusy] = useState(false);

  /** G9 能力门:null = 探测中(按未过门处理,走旧通路);true = sidecar
   *  protocol ≥ READ_STATE_PROTOCOL → 服务端读态通路。直调 api.version,
   *  失败即未过门(design §5.1,不引入全局 hook 依赖)。 */
  const [serverStateReady, setServerStateReady] = useState<boolean | null>(null);
  const useServerState = serverStateReady === true;

  /** 请求序号守卫(深审 F2;v7 拆双票):catalog 与 stream 各持一票,域内
   *  查询(refresh/liveRefresh/loadMore)每次发包取新票,应答落地前对票
   *  —— 旧应答(慢回包/切作用域后在途的旧域包)一律丢弃;双票防两域包
   *  互踩(catalog 静默合流不该被 stream 旧票判废,反之亦然)。 */
  const catalogSeqRef = useRef(0);
  const streamSeqRef = useRef(0);
  const nextCatalogSeq = useCallback(() => {
    catalogSeqRef.current += 1;
    return catalogSeqRef.current;
  }, []);
  const nextStreamSeq = useCallback(() => {
    streamSeqRef.current += 1;
    return streamSeqRef.current;
  }, []);

  useEffect(() => {
    setLocalStates(loadFeedStates());
    setDisplay(loadFeedDisplay());
  }, []);

  // 源名→engine 映射(挂载一次):health().plugins → sources[].name→engine
  // —— v6 渠道墙的渠道全集词表源(零条目渠道也出卡的 health 半边)+ 类型
  // 徽标判定;失败静默收敛为空映射(渠道全集退化为已加载条目 source,
  // 不拦情报流)
  useEffect(() => {
    let cancelled = false;
    void api
      .health()
      .then((health) => {
        if (!cancelled) setEngineBySource(engineMapFromHealth(health.plugins));
      })
      .catch(() => {
        if (!cancelled) setEngineBySource(new Map());
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
  // 同一次应答顺带置计数口径门(F2 根治,零新 RPC;源大类门随 v5 信息架构
  // 退役,见 scope 注记)
  useEffect(() => {
    let cancelled = false;
    void api
      .version()
      .then((info) => {
        if (!cancelled) {
          const protocol = typeof info?.protocol === "number" ? info.protocol : -1;
          setServerStateReady(protocol >= READ_STATE_PROTOCOL);
          setCountReady(protocol >= COUNT_PROTOCOL);
        }
      })
      .catch(() => {
        if (!cancelled) {
          setServerStateReady(false);
          setCountReady(false);
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

  /** 右栏铺底拉取(v7 §3.2):全库首页 50(零 source 参数),只喂 catalogItems
   *  (channelCards 聚合 + 总览统计);挂载即拉,countReady 门翻转补一查。
   *  空结果追问 health(firstRun 分叉,总览空态用)。 */
  const refreshCatalog = useCallback(async () => {
    const seq = nextCatalogSeq();
    setCatalogLoading(true);
    setCatalogError(null);
    try {
      const page = await fetchFeedPage({
        cursor: null,
        cursorId: null,
        source: null,
        // F2 根治:过计数门才带 with_total(旧 sidecar 忽略未知参数属预期,
        // 应答无 total = 词面回落,不为旧面报错)。query 不进服务端查询
        // (搜索 = 客户端过滤右栏行,v6 AC21 语义原样)。
        withTotal: countReady,
      });
      if (seq !== catalogSeqRef.current) return; // F2:旧应答丢弃(新包已在途/已落地)
      setCatalogItems(page.items);
      setCatalogLoaded(true);
      if (page.items.length === 0) {
        // 空结果才追问 health(一次 RPC):空态文案按有无插件分叉
        try {
          setFirstRun((await api.health()).first_run ?? false);
        } catch {
          // health 失败不遮蔽情报流自身的空态;CTA 点击时还有一次兜底
        }
      }
    } catch (err) {
      if (seq !== catalogSeqRef.current) return; // F2:旧域错误不污染新域
      setCatalogError(
        err instanceof SidecarRequestError
          ? err
          : new SidecarRequestError({ code: "transport_error", path: "$", message: String(err) }),
      );
    } finally {
      // loading 无条件清:守卫化会把 loading 卡死在更晚的 liveRefresh 票上
      setCatalogLoading(false);
    }
  }, [countReady, nextCatalogSeq]);

  /** 左栏流拉取(v7 §3.2):查询带 source = scope.source(fetchFeedPage 既有
   *  精确等值参数);仅选中态拉取,整页替换 + 游标机件重置。 */
  const refreshStream = useCallback(async () => {
    if (scope.source === null) return;
    const seq = nextStreamSeq();
    setLoading(true);
    setError(null);
    try {
      const page = await fetchFeedPage({
        cursor: null,
        cursorId: null,
        source: scope.source,
        withTotal: countReady,
      });
      if (seq !== streamSeqRef.current) return; // F2:旧应答丢弃(切域后在途包)
      setStreamItems(page.items);
      setCursor(page.nextCursor);
      setCursorId(page.nextCursorId);
      setHasMore(page.hasMore);
      setTotal(page.total);
    } catch (err) {
      if (seq !== streamSeqRef.current) return; // F2:旧域错误不污染新作用域
      setError(
        err instanceof SidecarRequestError
          ? err
          : new SidecarRequestError({ code: "transport_error", path: "$", message: String(err) }),
      );
    } finally {
      // loading 无条件清:守卫化会把 loading 卡死在更晚的 liveRefresh 票上
      setLoading(false);
    }
  }, [scope.source, countReady, nextStreamSeq]);

  // catalog 挂载即拉;countReady 门翻转(version 异步竞速)补一查,total 不缺场
  useEffect(() => {
    void refreshCatalog();
  }, [refreshCatalog]);
  // stream 仅选中态拉取;切总览清流态(左栏回引导空态);切渠道先清旧流再拉
  // (旧渠道行不再残留;对票守卫同时兜住已在途的旧域包)
  useEffect(() => {
    setStreamItems([]);
    setCursor(null);
    setCursorId(null);
    setHasMore(false);
    setTotal(null);
    setError(null);
    setLoadingMore(false);
    if (scope.source !== null) void refreshStream();
  }, [scope.source, refreshStream]);

  /** 实时滚动刷新(10-06 追加:主人令「情报流要不停地过信息日志」;v7 拆
   *  双域):静默拉首页 → mergeFreshItems 前插新键(已加载行与游标零扰动,
   *  新条目持续进流);失败静默(轮询尽力而为,不打错误卡——手点刷新钮
   *  才走错误路径)。触发面:completed / cron.completed 事件即时 + 30s
   *  可见性轮询兜底。F2 各域对票;选中态双刷(右栏行计数与左栏流同涨)。 */
  const liveRefreshCatalog = useCallback(async () => {
    const seq = nextCatalogSeq();
    try {
      const page = await fetchFeedPage({
        cursor: null,
        cursorId: null,
        source: null,
        withTotal: countReady,
      });
      if (seq !== catalogSeqRef.current) return; // F2:旧应答丢弃(含手点刷新接管后)
      setCatalogItems((current) => mergeFreshItems(current, page.items).items);
      setCatalogLoaded(true);
    } catch {
      // 尽力而为:轮询失败静默(下一轮/事件/手点刷新再试)
    }
  }, [countReady, nextCatalogSeq]);

  const liveRefreshStream = useCallback(async () => {
    if (scope.source === null) return;
    const seq = nextStreamSeq();
    try {
      const page = await fetchFeedPage({
        cursor: null,
        cursorId: null,
        source: scope.source,
        withTotal: countReady, // F2 根治:实时滚动顺带刷新 total(新条目落地 T 随动)
      });
      if (seq !== streamSeqRef.current) return; // F2:旧应答丢弃(含切域后在途包)
      setStreamItems((current) => mergeFreshItems(current, page.items).items);
      setTotal(page.total);
    } catch {
      // 尽力而为:轮询失败静默(下一轮/事件/手点刷新再试)
    }
  }, [scope.source, countReady, nextStreamSeq]);

  // 事件驱动即时刷新:桌面 run 终态(completed)+ cron 派发 run 落地
  // (cron.completed);与空流 CTA 的定向订阅并行,重复刷新幂等无害。
  // v7 双栏:选中态双刷(catalog 喂右栏行计数,stream 喂左栏流),总览态
  // liveRefreshStream 自守卫空转。
  useEffect(() => {
    let unlisten: UnlistenFn | null = null;
    let cancelled = false;
    void onSidecarEvent((event) => {
      if (event.type === "completed" || event.type === "cron.completed") {
        void liveRefreshCatalog();
        void liveRefreshStream();
      }
    }).then((un) => {
      if (cancelled) un();
      else unlisten = un;
    });
    return () => {
      cancelled = true;
      unlisten?.();
    };
  }, [liveRefreshCatalog, liveRefreshStream]);

  // 轮询兜底:可见时 30s 一发;隐藏暂停,恢复可见即刷(双域同上)
  useEffect(() => {
    const timer = window.setInterval(() => {
      if (!document.hidden) {
        void liveRefreshCatalog();
        void liveRefreshStream();
      }
    }, LIVE_POLL_INTERVAL_MS);
    const onVisibilityChange = () => {
      if (!document.hidden) {
        void liveRefreshCatalog();
        void liveRefreshStream();
      }
    };
    document.addEventListener("visibilitychange", onVisibilityChange);
    return () => {
      window.clearInterval(timer);
      document.removeEventListener("visibilitychange", onVisibilityChange);
    };
  }, [liveRefreshCatalog, liveRefreshStream]);

  // G9 状态源切换(§5.2):过门后 states 不再从 localStorage 派生,改由页内
  // 条目派生(store.items 投影三键);v7 双缓冲并集投影 —— 选中渠道内标读,
  // 右栏该行未读徽标即时降(两栏读态同源联动)。applyFeedFilter /
  // sortUnreadFirst / 渲染管线零改动,只换状态源。
  const allLoadedItems = useMemo(() => [...catalogItems, ...streamItems], [catalogItems, streamItems]);
  const states = useMemo<FeedStateMap>(
    () => (useServerState ? statesFromItems(allLoadedItems) : localStates),
    [useServerState, allLoadedItems, localStates],
  );

  // G9 一次性搬迁(Q2):过门且旧 map 非空 → 单请求 store.state.import(会话
  // 哨位防双调,幂等真相在服务端 store_meta);搬迁晚于首页应答时轻量刷
  // catalog 一次,让已导入读态即时对齐(搬迁对用户透明,不弹窗)。
  // 重跑无妨:哨位已挡,重入零 RPC。
  useEffect(() => {
    if (!useServerState) return;
    let cancelled = false;
    void importLocalFeedStates().then((outcome) => {
      if (!cancelled && outcome !== null && outcome.imported > 0) void refreshCatalog();
    });
    return () => {
      cancelled = true;
    };
  }, [useServerState, refreshCatalog]);

  /** 加载更早(v7 归 stream 域,时间线尾部按钮):复合游标翻页 + 判停零改 */
  const loadMore = useCallback(async () => {
    if (loadingMore || cursor === null) return;
    const seq = nextStreamSeq();
    setLoadingMore(true);
    try {
      const page = await fetchFeedPage({
        cursor,
        cursorId,
        source: scope.source,
      });
      if (seq !== streamSeqRef.current) return; // F2:refresh/liveRefresh 已接管,旧页不追加
      setCursor(page.nextCursor);
      setCursorId(page.nextCursorId);
      setStreamItems((current) => {
        const merged = appendFeedPage(current, page);
        // 追加 0 条防御判停(复合游标下不应发生;保留兜底防死循环)
        setHasMore(page.hasMore && merged.added > 0);
        return merged.items;
      });
    } catch (err) {
      if (seq !== streamSeqRef.current) return;
      setError(
        err instanceof SidecarRequestError
          ? err
          : new SidecarRequestError({ code: "transport_error", path: "$", message: String(err) }),
      );
    } finally {
      setLoadingMore(false);
    }
  }, [cursor, cursorId, loadingMore, scope.source, nextStreamSeq]);

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

  /** 双缓冲翻转 helper(v7 §3.2 缓冲写路面):条目可能只在 catalog(选中前
   *  看过的行)或只在 stream(选中后加载)—— 读写态一律两缓冲同翻;漏一边
   *  则另一栏呈现旧态(右栏徽标/左栏气泡脱钩)。 */
  const flipItem = useCallback(
    (key: string, marker: "starred" | "later" | "read", value: boolean) => {
      const flip = (current: FeedItem[]) =>
        current.map((candidate) =>
          itemKey(candidate) === key ? { ...candidate, [marker]: value } : candidate,
        );
      setCatalogItems(flip);
      setStreamItems(flip);
    },
    [],
  );

  /** G9 服务端通路单键置位:乐观翻本地条目 → store.state.mark(keys=[itemKey],
   *  前端算好目标值显式置位,无读-改-写);失败回滚到调用前真值(不瞎取反,
   *  防连点竞态)+ feed-mark-error 行明示(惯例同 openError)。
   *  v7:previous 真值查双缓冲并集(条目可能只在其中一边)。 */
  const markItemState = useCallback(
    (item: FeedItem, marker: "starred" | "later" | "read", value: boolean) => {
      const key = itemKey(item);
      const previous =
        (catalogItems.find((candidate) => itemKey(candidate) === key) ??
          streamItems.find((candidate) => itemKey(candidate) === key))?.[marker] === true;
      if (previous === value) return;
      flipItem(key, marker, value);
      void api
        .storeStateMark({ keys: [key], marker, value })
        .then(() => setMarkError(null))
        .catch((err) => {
          flipItem(key, marker, previous);
          setMarkError(err instanceof SidecarRequestError ? `${err.code}: ${err.message}` : String(err));
        });
    },
    [catalogItems, streamItems, flipItem],
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
   *  已由服务端回填,这里只是本地视图对齐,不重拉整页)。v7:只写
   *  streamItems —— 精评钮在左栏时间线卡上,条目必在当前流;catalog 不需要
   *  分数(右栏行只聚合计数,漏改才会精评后徽标不即时刷)。 */
  const onEnriched = useCallback((item: FeedItem, result: FeedEnrichResult) => {
    setStreamItems((current) =>
      current.map((candidate) =>
        itemKey(candidate) === itemKey(item) ? { ...candidate, scores: result.scores } : candidate,
      ),
    );
  }, []);

  /** 消息详情弹窗(主人令「点击信息,弹出详情」,10-08):存 itemKey 而非
   *  条目对象 —— 刷新/巡游换来的新对象按 key 重新命中,读态/星标翻转到哪版
   *  条目,弹窗就吃到哪版(弹窗内动作即时回显)。条目被过滤离场不关弹窗
   *  (streamItems 是已加载全集,命中仍在;v7 §3.3:命中域 = streamItems,
   *  总览态无条目弹窗天然不出);条目彻底不在集内(理论上仅作用域切换,
   *  弹窗开着时交互被遮罩挡住)则 detailItem 为 null 零渲染。 */
  const [detailKey, setDetailKey] = useState<string | null>(null);
  const detailItem = useMemo(
    () => (detailKey === null ? null : streamItems.find((candidate) => itemKey(candidate) === detailKey) ?? null),
    [detailKey, streamItems],
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

  /** G9 批量:全部标已读/未读(v7 总览态工具条入口 = 全库语义;选中渠道
   *  不出钮 —— mark_all 无 source 参数,范围不实则不出现)—— 过门后
   *  store.state.mark_all 单 UPDATE 全库(含未翻页/未加载条目);就地翻转
   *  已加载行即时反馈,不整页重拉,失败按调用前快照回滚;未过门 = 旧本地
   *  批量(作用域 = 已加载条目,title 如实注明)。v7:只翻 catalogItems
   *  (入口仅总览态,选中态零歧义;右栏行徽标随之即时降)。 */
  const markAllRead = useCallback(
    (value: boolean) => {
      if (useServerState) {
        const snapshot = new Map(catalogItems.map((candidate) => [itemKey(candidate), candidate.read === true]));
        setCatalogItems((current) =>
          current.map((candidate) => ({ ...candidate, read: value })),
        );
        void api
          .storeStateMarkAll({ marker: "read", value })
          .then(() => setMarkError(null))
          .catch((err) => {
            setCatalogItems((current) =>
              current.map((candidate) => ({
                ...candidate,
                read: snapshot.get(itemKey(candidate)) ?? false,
              })),
            );
            setMarkError(err instanceof SidecarRequestError ? `${err.code}: ${err.message}` : String(err));
          });
        return;
      }
      updateStates(setMarkerBulk(catalogItems, states, "read", value));
    },
    [useServerState, catalogItems, states, updateStates],
  );

  /** U 键 triage(v7 §4 右栏环):当前渠道已加载条目一键标已读 —— 单请求
   *  storeStateMark(keys 数组协议既有),乐观双缓冲翻(右栏徽标与左栏气泡
   *  同步降),失败按快照回滚;未过门 = setMarkerBulk 本地态同构;范围 =
   *  已加载口径(与右栏未读徽标同门),已加载 0 条 = 无操作。 */
  const markChannelRead = useCallback(
    (source: string) => {
      const loaded = allLoadedItems.filter((candidate) => candidate.source === source);
      if (loaded.length === 0) return;
      const keys = loaded.map(itemKey);
      if (useServerState) {
        const snapshot = new Map(loaded.map((candidate) => [itemKey(candidate), candidate.read === true]));
        const flipAll = (current: FeedItem[]) =>
          current.map((candidate) =>
            candidate.source === source ? { ...candidate, read: true } : candidate,
          );
        setCatalogItems(flipAll);
        setStreamItems(flipAll);
        void api
          .storeStateMark({ keys, marker: "read", value: true })
          .then(() => setMarkError(null))
          .catch((err) => {
            const rollback = (current: FeedItem[]) =>
              current.map((candidate) =>
                candidate.source === source
                  ? { ...candidate, read: snapshot.get(itemKey(candidate)) ?? false }
                  : candidate,
              );
            setCatalogItems(rollback);
            setStreamItems(rollback);
            setMarkError(err instanceof SidecarRequestError ? `${err.code}: ${err.message}` : String(err));
          });
        return;
      }
      updateStates(setMarkerBulk(loaded, states, "read", true));
    },
    [allLoadedItems, useServerState, states, updateStates],
  );
  /** 批量钮禁用口径(总览态):catalog 域未读数(v7 bulk 钮只在总览在场) */
  const unreadLoaded = useMemo(
    () => catalogItems.filter((candidate) => !(states[itemKey(candidate)]?.read)).length,
    [catalogItems, states],
  );

  // ① later 到期重现:now 随过滤重算取值(窗口为天级,会话内漂移无感);
  //  到期稍后读条目经 applyFeedFilter 并入未读视图(机制见 ./api.ts ① 节)
  // ② 当日窗(10-06 追加):当日窗只作用于右栏行「今日」计数(v7 渠道流无
  //  当日窗,深检 F1 定案);历史态(监控台「看全部历史消息」/空态「看全部
  //  条目」入口)读态过滤也豁免,已读未读全显。
  const visible = useMemo(() => {
    if (scope.history) return streamItems;
    return applyFeedFilter(streamItems, states, filter, new Date());
  }, [streamItems, scope.history, filter, states]);

  /** 展示序(A-feed):过滤结果 → 未读优先(可选;未读浮前,两类各自稳定保序) */
  const displayItems = useMemo(
    () => (display.unreadFirst ? sortUnreadFirst(visible, states) : visible),
    [display.unreadFirst, visible, states],
  );

  // ---------------------------------------------------------------------------
  // 右栏渠道全集派生(v7 §3.3,v6 AC20/AC21 语义迁址):全集 = health sources
  // ∪ catalog 条目 source 去重(feedChannelCards,零条目渠道也出行);搜索 =
  // 客户端渠道名/源 id 包含匹配(filterChannelsByQuery,大小写不敏感,清空
  // 恢复全量)。总览统计(Σtoday/Σunread)纯派生零新 RPC。
  // ---------------------------------------------------------------------------
  const channelCards = useMemo(
    () => feedChannelCards(catalogItems, states, engineBySource, windowStart),
    [catalogItems, states, engineBySource, windowStart],
  );
  const visibleChannels = useMemo(
    () => filterChannelsByQuery(channelCards, query),
    [channelCards, query],
  );
  const overviewStats = useMemo(
    () => ({
      today: channelCards.reduce((sum, card) => sum + card.today, 0),
      unread: channelCards.reduce((sum, card) => sum + card.unread, 0),
    }),
    [channelCards],
  );

  /** 渲染形态派生(v6 双形态):渠道墙 = 渠道卡瀑布流(AC20);渠道详情 =
   *  该渠道条目流 —— TG 渠道 = 聊天视图(气泡时间线 + 日期胶囊),网站/
   *  日报渠道 = 条目卡瀑布流。TG 判定走渠道卡同一 engine 词表
   *  (channelCardKindOf:tg_web/telegram 引擎 → 前缀规约兜底)。 */
  const activeChannelKind =
    scope.source !== null ? channelCardKindOf(scope.source, engineBySource.get(scope.source)) : null;
  const chatView = activeChannelKind === "tg";
  /** TG 渠道详情(监控台钉顶判定,v6 = TG 渠道卡进入的详情视图)。 */
  const isTgChannel = chatView;

  /** TG 网页线快照(10-09-tg-category-entry:TG 渠道选中时拉一次,监控台条
   *  呈现)。v7 R2 吸收(v6 深检遗留):状态态拆三层 phase —— idle/loading/
   *  ok/error,替换 `tgWebline === null` 双态:首拉在途(loading)监控台条
   *  与「状态未知」卡都不出(时间线骨架已在转,不再闪现「状态未知」一拍);
   *  error(拉取失败/异形应答)才出「监控状态未知 + 重试」;ok 出监控台条
   *  (旧 tgWebline 数据态保留在 phase=ok 内)。deps 必须含 isTgChannel
   *  ——进入 TG 渠道时只有它翻转,漏掉 = 监控台永远等不到快照(v2 实测
   *  踩坑);tgStatusTick = 空态「重试」钮触发重拉。 */
  type TgStatusPhase = "idle" | "loading" | "ok" | "error";
  const [tgStatusPhase, setTgStatusPhase] = useState<TgStatusPhase>("idle");
  const [tgStatusTick, setTgStatusTick] = useState(0);
  useEffect(() => {
    if (!isTgChannel) return;
    let cancelled = false;
    setTgStatusPhase("loading");
    void telegramGetStatus()
      .then((status) => {
        if (cancelled) return;
        const clean = sanitizeTelegramStatus(status);
        setTgWebline(clean);
        setTgStatusPhase(clean !== null ? "ok" : "error");
      })
      .catch(() => {
        if (cancelled) return;
        setTgWebline(null);
        setTgStatusPhase("error");
      });
    return () => {
      cancelled = true;
    };
  }, [isTgChannel, tgStatusTick]);
  /** 空态重试(深检 F2):重拉(效果内先落 loading,旧台与「在线」话术即时退场) */
  const retryTgStatus = useCallback(() => {
    setTgStatusTick((tick) => tick + 1);
  }, []);

  /** 分组(显示选项,仅聊天视图):TG 频道作用域的日期胶囊分组走时间四桶
   *  (v4 聊天主页风格);不分组 = 平铺。瀑布流卡片墙(AC13)恒平铺多列
   *  (break-inside-avoid 瀑布布局与 sticky 组头互斥,时间语义由卡面相对
   *  时间承担)。历史本地存储的 groupMode="category" 就地映射回时间四桶
   *  (loadFeedDisplay 兼容旧值,不丢用户其余选项)。 */
  const groups = useMemo<
    {
      key: string;
      label: string;
      items: FeedItem[];
      color: string | null;
      category: string | null;
    }[] | null
  >(() => {
    if (!chatView || display.groupMode === "none") return null;
    return groupFeedItems(displayItems).map((group) => ({
      key: group.key,
      label: group.label,
      items: group.items,
      color: null,
      category: null,
    }));
  }, [chatView, display.groupMode, displayItems]);

  /** v7 键盘双环(§4):j/k 巡游环 = 右栏渠道行(主人方向钉死);左栏条目
   *  巡游整体上移 Shift 层(Shift+J/K);Enter/U 落点跟随「当前环」。
   *  listCurrentKey = 右栏环,itemCurrentKey = 左栏环;navPane 标当前环。 */
  const [listCurrentKey, setListCurrentKey] = useState<string | null>(null);
  const [itemCurrentKey, setItemCurrentKey] = useState<string | null>(null);
  const [navPane, setNavPane] = useState<"list" | "timeline">("list");
  /** 键盘巡游标志(Linear 式:focus 环只在键盘巡游时呈现,鼠标 hover 即清) */
  const [navByKeyboard, setNavByKeyboard] = useState(false);

  /** hover/focus 进入右栏行 = 置列表环当前行并切右栏环(退键盘巡游态) */
  const onCurrentRow = useCallback((key: string) => {
    setListCurrentKey(key);
    setNavPane("list");
    setNavByKeyboard(false);
  }, []);

  /** hover/focus 进入条目卡 = 置条目环当前卡并切左栏环(退键盘巡游态) */
  const onCurrentCard = useCallback((key: string) => {
    setItemCurrentKey(key);
    setNavPane("timeline");
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

  /** 单卡渲染(时间线/单列列表两路共用;右键菜单随卡在 FeedCard 内;
   *  渠道类型随卡判定 —— 五档差异化呈现,engine 词表源 = health 装配的
   *  源名映射;TG 卡带频道名行,列表里卡片自带来源渠道语义。
   *  v7 双环:环呈现与否看 navPane 是否在 timeline。 */
  const renderCard = (entry: FeedItem) => (
    <FeedCard
      key={itemKey(entry)}
      item={entry}
      state={states[itemKey(entry)] ?? FEED_CARD_NO_STATE}
      current={itemCurrentKey === itemKey(entry)}
      navFocused={itemCurrentKey === itemKey(entry) && navPane === "timeline" && navByKeyboard}
      kind={channelKindOf(entry, engineBySource)}
      onCurrent={onCurrentCard}
      onToggle={toggle}
      onOpenError={setOpenError}
      onEnriched={onEnriched}
      onOpenDetail={openDetail}
    />
  );

  /** G3 导出(v6 口径):dialog.save → feed.export 全库直出(渠道过滤属
   *  首屏视图语义,feed.export 无 source/query 参数,词面如实);取消 = 静默 */
  const exportCurrentView = useCallback(async () => {
    setExporting(true);
    setExportNote(null);
    try {
      const outcome = await exportFeedView({ format: exportFormat });
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
  }, [exportFormat]);

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

  // completed 事件 → 回 idle(可再跑)+ 自动刷新右栏铺底(CTA 只在总览态
  // 可达,新条目落库即出行/计数;订阅随 collecting 状态起止)
  useEffect(() => {
    if (cta.phase !== "collecting") return;
    let unlisten: UnlistenFn | null = null;
    let cancelled = false;
    void onSidecarEvent((event) => {
      if (event.type === "completed" && event.run_id === cta.runId) {
        setCta({ phase: "done" });
        void refreshCatalog();
      }
    }).then((un) => {
      if (cancelled) un();
      else unlisten = un;
    });
    return () => {
      cancelled = true;
      unlisten?.();
    };
  }, [cta, refreshCatalog]);

  const searchActive = query !== "";

  /** G9 批量两钮 title(双路真话;R2 确认态确认钮沿用同一支)。v7 总览态
   *  入口 = 全库语义;选中渠道不出钮(feed.export/mark_all 无 source 参数,
   *  范围不实则不出现)。 */
  const bulkHidden = scope.source !== null;
  const markAllReadTitle = !useServerState
    ? `把已加载的 ${catalogItems.length} 条(未读 ${unreadLoaded})全部标记为已读;本地态,未翻页条目不含`
    : "把全库所有条目(含未翻页)标记为已读,服务端持久";
  const markAllUnreadTitle = !useServerState
    ? `把已加载的 ${catalogItems.length} 条(已读 ${catalogItems.length - unreadLoaded})全部恢复未读;本地态`
    : "把全库所有条目(含未翻页)恢复为未读,服务端持久";

  /** 选中作用域动作(v7 AC25 动线):点右栏行 = 选中该渠道,左栏载入其流;
   *  右栏原地不动(行高亮随 data-selected)。清左栏键盘环,列表环落在被点行。 */
  const openChannel = useCallback((key: string) => {
    setScope({ source: key, history: false });
    setListCurrentKey(key);
    setItemCurrentKey(null);
    setNavPane("list");
    setNavByKeyboard(false);
    setTgPreviewNote(null);
  }, []);
  /** 清选中回总览(v7 替代 v6 backToWall:双栏无页面切换,工具条「总览」
   *  钮 / Esc 同此口;搜索词跨选中保留,清选中不清词)。 */
  const clearSelection = useCallback(() => {
    setScope({ source: null, history: false });
    setItemCurrentKey(null);
    setNavPane("list");
    setNavByKeyboard(false);
    setTgPreviewNote(null);
  }, []);
  /** 历史入口(监控台「看全部历史消息」/ 空态「看全部条目」):历史态 =
   *  该渠道全部入库条目、已读未读全显(深检 F1 后渠道流默认已无当日窗,
   *  历史态的增量语义 = 读态过滤豁免)。 */
  const openHistory = useCallback(() => {
    setScope((current) => ({ ...current, history: true }));
    setItemCurrentKey(null);
  }, []);
  /** 退出历史(历史出口收编工具条钮) */
  const exitHistory = useCallback(() => {
    setScope((current) => ({ ...current, history: false }));
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
      // webline 与 phase 成对落(深检 C4,P2;与首拉 effect 同构):异形应答
      // 把 webline 洗成 null 时 phase 同步落 error —— 否则 webline 双门卸掉
      // 监控台条而 phase 停留 ok,空态链谎落「监控在线」。
      const clean = sanitizeTelegramStatus(next);
      setTgWebline(clean);
      setTgStatusPhase(clean !== null ? "ok" : "error");
    } catch {
      // 尽力而为:失败态在设置 · Telegram 总卡有完整台账,条内不弹错
    } finally {
      setTgLoginBusy(false);
    }
  }, [tgWebline]);
  /** 内置浏览器预览(10-09-tg-category-entry v3 AC11,主人令「是否加载了
   *  内置浏览器界面,展示 tg 内容」):取该渠道最新条目 url 推导频道公开
   *  镜像 t.me/s/<频道名>,WebviewWindow 应用内窗口直开(免二次登录)。
   *  职责分离:数据入库仍由后台 watcher 登录会话负责,本窗口**仅内容展示**,
   *  不做任何采集/登录动作;推导不出(私有频道/无 t.me 链)= 按钮置灰,
   *  title 如实;开窗失败(tauri://error)= 条内出说明,不装死。 */
  const [tgPreviewNote, setTgPreviewNote] = useState<string | null>(null);
  const tgPreviewUrl = useMemo(() => {
    if (scope.source === null || !isTgChannel) return null;
    for (const item of streamItems) {
      if (item.source !== scope.source) continue;
      const mirror = telegramMirrorUrlOf(item.url);
      if (mirror) return mirror;
    }
    return null;
  }, [streamItems, scope.source, isTgChannel]);
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

  // v7 键盘语义终案(§4):j/k 巡游环 = 右栏渠道行(主人方向钉死);左栏
  // 条目巡游整体上移 Shift 层(Shift+J/K);Enter/U 落点跟随「当前环」
  // (navPane)。U 在右栏环 = 当前渠道已加载条目一键标已读(triage);在
  // 左栏环 = 当前条目已读/未读切换(既有 toggle)。Esc = 清选中回总览(仅
  // 弹窗闭时可达;弹窗开着按 Esc 只关弹窗,Radix 自 handling)。Mod+F = 聚焦
  // 右栏搜索框并全选(搜索框随右栏常驻 = ref 恒挂载,直聚焦;弹窗开着让位)。
  // 输入框/textarea/select/contentEditable 内敲键不触发;Enter 命中 button/a
  // 归原生(feed 本地惯例守卫,不引外部 hook)。
  //
  // **实时状态镜(双环真机实证修复)**:window keydown 挂在 passive effect
  // 里,effect 重挂滞后于 DOM commit —— 真实浏览器中 Shift+J 后紧接 Enter
  // (4ms 键序实测)可踩到旧闭包(navPane 还是 list),Enter 落错环;jsdom/
  // act 同步刷新故单测永不复现。render 期同步回写 ref,handler 一律读镜不
  // 信闭包;effect 依赖数组只留 mount 一次。
  const keyStateRef = useRef({
    navPane,
    itemCurrentKey,
    listCurrentKey,
    scopeSource: scope.source,
    detailKey,
    allLoadedItems,
    displayItems,
    visibleChannels,
    toggle,
    markChannelRead,
    openDetail,
    openChannel,
    clearSelection,
  });
  keyStateRef.current = {
    navPane,
    itemCurrentKey,
    listCurrentKey,
    scopeSource: scope.source,
    detailKey,
    allLoadedItems,
    displayItems,
    visibleChannels,
    toggle,
    markChannelRead,
    openDetail,
    openChannel,
    clearSelection,
  };
  useEffect(() => {
    const onKeyDown = (event: KeyboardEvent) => {
      // 浮层让位收口(深检 C1,P1):DropdownMenu/ContextMenu/Dialog/命令面板
      // 等浮层基件对 Esc(及各自已接管的键)先 preventDefault 再放行原生冒泡
      // —— window 侧见 defaultPrevented 一律让位,防「关菜单连带清选中」
      // (v7 Esc 清选中为新增分支,v6 键白名单无 escape,无此回退面)。
      if (event.defaultPrevented) return;
      const snapshot = keyStateRef.current;
      const pressed = event.key.toLowerCase();
      if ((event.metaKey || event.ctrlKey) && pressed === "f") {
        // 详情弹窗开着让位(焦点陷阱内把焦点打到遮罩后行为未定义,§1.2/§4)
        if (snapshot.detailKey !== null) return;
        event.preventDefault();
        searchInputRef.current?.focus();
        searchInputRef.current?.select();
        return;
      }
      // 详情弹窗开着:全部巡游/置位键让位(防焦点绕过遮罩在背后卡上移动)
      if (snapshot.detailKey !== null) return;
      if (
        pressed !== "u" &&
        pressed !== "j" &&
        pressed !== "k" &&
        pressed !== "enter" &&
        pressed !== "escape"
      ) {
        return;
      }
      if (event.metaKey || event.ctrlKey || event.altKey) return; // Shift 仅 j/k 分流用
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
      // (渠道行根是 div[role=button],Enter 归全局巡游语义,不在此列)
      if (pressed === "enter" && target && (target.tagName === "BUTTON" || target.tagName === "A")) {
        return;
      }
      if (pressed === "escape") {
        // Esc 清选中回总览(复审铁律:弹窗守卫之后才可达;总览态 = no-op)。
        // 浮层在场守卫(深检 C1 第二道):defaultPrevented 收口依赖浮层基件
        // 接管 Esc —— 自研 dropdown 内容挂载后经 rAF 抢焦,此窗口期内 Esc 落
        // 在触发器/body 上无人 preventDefault;菜单还开着就不清选中(关菜单
        // 交给浮层自身 machinery,触发器侧配套 Esc 关闭见 ui/dropdown-menu)。
        if (snapshot.scopeSource !== null && !document.querySelector('[role="menu"]')) {
          snapshot.clearSelection();
        }
        return;
      }
      if (pressed === "u") {
        if (snapshot.navPane === "timeline") {
          // 左栏环:当前条目已读/未读切换(既有 toggle)
          if (snapshot.itemCurrentKey === null) return;
          const item = snapshot.allLoadedItems.find(
            (candidate) => itemKey(candidate) === snapshot.itemCurrentKey,
          );
          if (item) snapshot.toggle(item, "read");
          return;
        }
        // 右栏环:当前渠道已加载条目一键标已读(triage;已加载 0 条 = 无操作)
        const targetSource = snapshot.listCurrentKey ?? snapshot.scopeSource;
        if (targetSource === null) return;
        // 在场校验(深检 C3,P2;与同 handler Enter 分支同门):targetSource
        // 来自巡游环时须仍在右栏在场 —— 搜索收窄把巡游行过滤出局后 listCurrentKey
        // 不清,按 U 不得对隐形渠道置位;scopeSource 兜底(选中渠道恒在场)不校验。
        if (
          snapshot.listCurrentKey !== null &&
          !snapshot.visibleChannels.some((card) => card.key === targetSource)
        ) {
          return;
        }
        snapshot.markChannelRead(targetSource);
        return;
      }
      if (pressed === "enter") {
        if (snapshot.navPane === "timeline") {
          if (snapshot.itemCurrentKey === null) return;
          const item = snapshot.allLoadedItems.find(
            (candidate) => itemKey(candidate) === snapshot.itemCurrentKey,
          );
          if (item) snapshot.openDetail(item);
          return;
        }
        if (snapshot.listCurrentKey === null) return;
        if (snapshot.visibleChannels.some((card) => card.key === snapshot.listCurrentKey)) {
          snapshot.openChannel(snapshot.listCurrentKey);
        }
        return;
      }
      // j/k 巡游:环分栏(event.shiftKey 守卫分流)—— 裸 j/k = 右栏渠道行,
      // Shift+J/K = 左栏条目;边界钳制不回绕(首行 k / 末行 j 原地不动),
      // 未选中时 j 落首、k 落末(当前行被过滤离场同此路径)。
      const toTimeline = event.shiftKey;
      const keys = toTimeline
        ? snapshot.displayItems.map(itemKey)
        : snapshot.visibleChannels.map((card) => card.key);
      if (keys.length === 0) return;
      if (toTimeline && snapshot.scopeSource === null) return; // 总览无条目环
      const currentIndex = toTimeline
        ? snapshot.itemCurrentKey === null
          ? -1
          : keys.indexOf(snapshot.itemCurrentKey)
        : snapshot.listCurrentKey === null
          ? -1
          : keys.indexOf(snapshot.listCurrentKey);
      const next =
        pressed === "j"
          ? keys[currentIndex < 0 ? 0 : Math.min(currentIndex + 1, keys.length - 1)]
          : keys[currentIndex < 0 ? keys.length - 1 : Math.max(currentIndex - 1, 0)];
      if (toTimeline) {
        setItemCurrentKey(next);
        setNavPane("timeline");
      } else {
        setListCurrentKey(next);
        setNavPane("list");
      }
      setNavByKeyboard(true);
      // 巡游行滚入视口(最近侧;jsdom 无 scrollIntoView 实现时静默跳过)
      const escaped =
        typeof CSS !== "undefined" && typeof CSS.escape === "function" ? CSS.escape(next) : next;
      const node = document.querySelector<HTMLElement>(`[data-item-key="${escaped}"]`);
      if (node && typeof node.scrollIntoView === "function") node.scrollIntoView({ block: "nearest" });
    };
    window.addEventListener("keydown", onKeyDown);
    return () => window.removeEventListener("keydown", onKeyDown);
    // 依赖数组 = mount 一次:易变态全部经 keyStateRef 实时镜读取(见上注)
  }, []);

  /** 作用域文案(工具条左侧可见词;sr-only aria-live 同源播报;v7:总览 =
   *  「全部情报」,选中 = 渠道名) */
  const streamTitle = overviewMode ? "全部情报" : channelDisplayName(scope.source);

  return (
    /* 满高双栏行(v7 §0:左 section 先、右 aside 后,flex 行内自然落右;
     * 无页面级滚动,两栏各自内滚 —— Kestra「满高内滚」惯例沿用) */
    <div className="flex h-full min-h-0">
      {/* ═══ 左栏:数据主区(§2,flex-1 min-w-0)═══ */}
      <section aria-label="数据主区" className="flex min-w-0 flex-1 flex-col">
      {/* 工具条(§2.1 读态工具条,按选中态分叉;全部是既有控件归位,零新
          控件):总览钮(仅选中)+ 作用域词 + 读态分段(仅选中非历史)+
          计数词面(仅选中)/ 知会词(仅选中)/ 批量(仅总览)+ 右侧显示
          选项(仅选中)/ 刷新(两态)/ 导出(仅总览)。搜索框已迁右栏顶。 */}
      <div className="flex flex-wrap items-center gap-2 border-b px-5 py-2.5" data-testid="feed-toolbar">
        {/* 总览钮(仅选中态;替代 v6 feed-back-to-wall —— 双栏无页面切换,
            语义 = 清选中回总览;Esc 同门) */}
        {!overviewMode ? (
          <Button
            variant="outline"
            size="sm"
            className="px-2 text-xs"
            data-testid="feed-back-to-overview"
            title="回到总览(全部情报;Esc 同门)"
            onClick={clearSelection}
          >
            <ChevronDown className="size-3.5 rotate-180" />
            总览
          </Button>
        ) : null}
        {/* 作用域标题(10-08 审计 F6 沿用):可见当前位置词 */}
        <span className="text-xs font-medium text-foreground" data-testid="feed-stream-title">
          {streamTitle}
        </span>
        {/* 读态分段(KsFilter 范式):微填充容器 + 内钮 h-7,激活 = bg-accent。
            仅选中态渲染(条目流语义);深检 F4:历史态(已读未读全显)读态
            过滤不生效,分段随之隐藏,不给死控件。 */}
        {!overviewMode && !scope.history ? (
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
                    ? "未读过滤会隐藏已读条目(到期稍后读除外);切「全部」可恢复"
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
        ) : null}
        {/* 计数词面(仅选中态;testid = feed-stream-count,右栏脚注独占
            feed-count —— 复审 R1-1 消歧,两 testid 恒单匹配)。既有 F2 口径
            —— 过 COUNT_PROTOCOL 门(protocol ≥ 13)且应答带 total → 截断时
            「已加载 X · 共 T 条」;未过门/无 total = 回落 F2 半程词面。
            R1 吸收:title 删「当日窗视图首页」残词,统一「已加载口径」。 */}
        {!overviewMode ? (
        <span
          className="text-2xs text-muted-foreground"
          data-testid="feed-stream-count"
          title={
            total !== null && total > streamItems.length
              ? `共 ${total} 条 = 当前过滤条件(store.items 同 WHERE)全量计数,含未翻页;已加载 ${streamItems.length} 条为已加载口径`
              : undefined
          }
        >
          {total !== null && total > streamItems.length
            ? filter === "all"
              ? `已加载 ${streamItems.length} · 共 ${total} 条`
              : `已加载 ${visible.length} / ${streamItems.length} · 共 ${total} 条`
            : hasMore
              ? filter === "all"
                ? `已加载 ${streamItems.length} 条(首页截断,更早条目未计入)`
                : `已加载 ${visible.length} / ${streamItems.length} 条`
              : filter === "all"
                ? `共 ${streamItems.length} 条`
                : `${visible.length} / ${streamItems.length} 条`}
        </span>
        ) : null}
        {/* 知会词(仅选中态;总览统计在引导空态):选中 = 全量流(深检 F1:
            当日窗只作用于右栏行「今日」计数,渠道流不裁剪);历史态 = 读态
            豁免(已读未读全显),给退出钮(历史出口收编工具条) */}
        {!overviewMode ? (
        <span
          className="text-2xs text-muted-foreground"
          data-testid="feed-day-window"
          title={
            scope.history
              ? "历史态:该渠道全部入库条目,已读未读全显(读态过滤豁免);点「退出历史」回到读态视图。"
              : "渠道流 = 该渠道全部入库条目(新→旧,当日窗不裁剪,加载更早翻页取尽);读态分段过滤未读/星标/稍后读"
          }
        >
          {scope.history ? "全部历史 · 已读未读全显" : "全量 · 新→旧 · 实时滚动"}
        </span>
        ) : null}
        {scope.history ? (
          <Button
            variant="ghost"
            size="sm"
            className="px-2 text-xs text-muted-foreground"
            data-testid="feed-history-exit"
            title="退出历史态:回到读态过滤视图(未读/星标/稍后读/全部)"
            onClick={exitHistory}
          >
            退出历史
          </Button>
        ) : null}
        {/* G9 批量(仅总览态:全库语义与总览语境相符;mark_all 无 source
            参数,选中态不出钮防范围不实) */}
        {!bulkHidden && confirmAllMark === null ? (
          <>
            <Button
              variant="ghost"
              size="sm"
              className="px-2 text-xs text-muted-foreground"
              aria-label="全部标已读"
              title={markAllReadTitle}
              onClick={() => setConfirmAllMark("read")}
              disabled={catalogItems.length === 0 || unreadLoaded === 0}
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
              disabled={catalogItems.length - unreadLoaded === 0}
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
                markAllRead(value);
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
          {/* 显示选项(仅选中态,条目流语义):未读优先 + 分组维度(分组仅
              聊天视图生效,单列列表恒平铺) */}
          {!overviewMode ? (
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
          ) : null}
          {/* KsFilter refresh 位:重发当前域查询(总览 = 右栏铺底,选中 = 该
              渠道条目流) */}
          <Button
            variant="ghost"
            size="icon"
            className="size-8"
            aria-label="刷新"
            title={overviewMode ? "重新拉取渠道全集铺底(全库首页)" : "重新拉取该渠道条目流"}
            onClick={() => void (overviewMode ? refreshCatalog() : refreshStream())}
            disabled={overviewMode ? catalogLoading : loading}
          >
            <RefreshCw className={(overviewMode ? catalogLoading : loading) ? "size-3.5 animate-spin" : "size-3.5"} />
          </Button>
          {/* G3 导出组(仅总览态:feed.export 无 source 参数,选中态不出钮
              防范围不实;导出 = 全库条目直出) */}
          {overviewMode ? (
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
                title="导出全库条目为本地文件"
              >
                <Download className={exporting ? "size-3.5 animate-pulse" : "size-3.5"} />
                {exporting ? "导出中…" : "导出全库"}
              </Button>
            </div>
          ) : null}
        </div>
      </div>

      {/* TG 监控台条(§2.2:仅选中渠道 kind=tg 且状态 phase=ok;落位 = 工具条
          之下、时间线滚动区之外,监控状态常驻可见不随流滚走。R2 吸收:首拉
          在途(loading)不出条也不出「状态未知」卡——时间线骨架已在转,不再
          闪现「状态未知」一拍;error 才落空态阶梯的重试卡)。内容与 v6 卡
          零增删只重排:状态段 + 右侧钮簇(扫码登录|登录中…、内置浏览器预览、
          管理)+ 第二行「看全部历史消息」+ 预览失败注记行。 */}
      {isTgChannel && tgStatusPhase === "ok" && tgWebline !== null ? (
        <div
          data-testid="feed-tg-console"
          className="mx-5 mt-3 rounded-md border border-primary/30 bg-primary/5 px-3 py-2.5"
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
            onClick={openHistory}
            className="mt-1.5 inline-flex items-center gap-1 text-2xs text-primary hover:underline"
          >
            <Inbox aria-hidden className="size-3" />
            看全部历史消息(含已读)
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

      {/* 时间线滚动区(§0:左栏内滚;总览态 = 引导空态,选中态 = 条目流)+
          导出/错误/标记回执行(既有位置语义,随滚动区走) */}
      <div className="flex min-h-0 flex-1 flex-col gap-3 overflow-y-auto px-5 py-3">
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

        {/* 错误态(§7):catalog 域错 = 总览态显示;stream 域错 = 选中态显示
            (两态互斥,双票守卫防旧域错误污染新域) */}
        {overviewMode && catalogError ? (
          <FeedErrorCard error={catalogError} onRetry={() => void refreshCatalog()} busy={catalogLoading} />
        ) : null}
        {!overviewMode && error ? (
          <FeedErrorCard error={error} onRetry={() => void refreshStream()} busy={loading} />
        ) : null}

        {overviewMode ? (
          /* ═══ 总览引导空态(§2.4):统计行(纯派生零新 RPC)+ 指向右栏的
              主词面;firstRun / 空流 CTA 两分支以 catalogLoaded 为门(catalog
              在途一拍不出 CTA 免闪现;统计行同门,与右栏行骨架同期落位)═══ */
          <div className="flex flex-1 flex-col items-center justify-center gap-2" data-testid="feed-overview">
            {catalogLoaded ? (
              <>
                <p
                  className="font-mono text-xs text-muted-foreground tabular-nums"
                  data-testid="feed-overview-stats"
                  title="渠道全集 = 插件 health 源 ∪ 已加载条目来源;计数为已加载口径(全库首页 50 条铺底;今日 = 当日窗 03:00 起)"
                >
                  {`${channelCards.length} 个渠道 · 今日 ${overviewStats.today} 条 · 未读 ${overviewStats.unread}`}
                </p>
                {catalogItems.length === 0 ? (
                  firstRun ? (
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
                  <Card>
                    <CardContent className="p-0">
                      <EmptyState
                        title="从右侧选择一个群组或渠道"
                        description="这里显示它的消息流(新→旧全量);右栏顶部搜索可按名称 / 源 id 过滤群组。"
                      />
                    </CardContent>
                  </Card>
                )}
              </>
            ) : null}
          </div>
        ) : loading && streamItems.length === 0 ? (
          // 三态(frontend-ui-engineering):骨架块贴卡三级形状(选中切换 =
          // 左栏骨架,右栏纹丝不动)
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
          // 空态阶梯(v7 §7,落位更新文案基调不变):TG 渠道三态(状态未知
          // 仅拉取失败 —— R2;未登录 / 监控在线)/ 零条目渠道 / 读态过滤空。
          // TG 首拉在途(loading)不出任何空态卡(R2:不闪「状态未知」;
          // 单 RPC 在途窗极短,一拍空白设计接受不收)。
          isTgChannel && tgStatusPhase === "loading" ? null :
          isTgChannel && tgStatusPhase === "error" ? (
            /* TG 渠道空态 · 状态未知(深检 F2;R2 后仅 error 态可达):
                telegram.status 拉取失败(监控台同门缺席)——不称「在线」、
                不指路不存在的监控台,给重试拉状态。 */
            <Card data-testid="feed-tg-status-unknown">
              <CardContent className="p-0">
                <EmptyState
                  title="监控状态未知"
                  description="暂时拿不到 Telegram 监控状态(状态服务未就绪或请求失败);是否登录、新消息是否入库以「设置 · Telegram」的台账为准。"
                  action={
                    <Button variant="outline" size="sm" onClick={retryTgStatus}>
                      重试拉取状态
                    </Button>
                  }
                />
              </CardContent>
            </Card>
          ) : isTgChannel && tgWebline !== null && !tgWebline.web.accounts.some((a) => a.logged_in) ? (
            /* TG 渠道空态 · 未登录(深检 F2):如实说未登录,指路监控台
                (此分支监控台条必在场——同以 phase=ok 为门)。 */
            <Card>
              <CardContent className="p-0">
                <EmptyState
                  title="未登录,暂无新消息入库"
                  description="上方监控台扫码登录网页版 telegram 后,7×24 监控自动入库,新消息即出现在这里;「全部」页签可看已入库的已读条目。"
                />
              </CardContent>
            </Card>
          ) : isTgChannel ? (
            /* TG 渠道空态 · 监控在线:不再甩「先跑采集」死胡同——给「新
                消息即时入库」预期 + 监控台条「看全部历史消息」直达 */
            <Card>
              <CardContent className="p-0">
                <EmptyState
                  title="监控在线,暂无未读新消息"
                  description="Telegram 监控在线,新消息入库即出现在这里;已读条目切「全部」页签或点监控台「看全部历史消息(含已读)」直达。"
                />
              </CardContent>
            </Card>
          ) : streamItems.length === 0 ? (
            /* 零条目渠道:不空转,给回流动线(CTA 改「回总览」,v6 为
                「返回渠道墙」—— 双栏无墙,总览即家) */
            <Card data-testid="feed-channel-empty">
              <CardContent className="p-0">
                <EmptyState
                  title="该渠道暂无入库条目"
                  description="采集到该渠道的条目后会出现在这里;可先回总览看其他渠道。"
                  action={
                    <Button variant="outline" size="sm" onClick={clearSelection}>
                      回总览
                    </Button>
                  }
                />
              </CardContent>
            </Card>
          ) : (
            <Card>
              <CardContent className="p-0">
                <EmptyState
                  title={EMPTY_TEXT[filter].title}
                  description={EMPTY_TEXT[filter].description}
                  action={
                    !scope.history ? (
                      <Button
                        variant="outline"
                        size="sm"
                        data-testid="feed-empty-history"
                        onClick={openHistory}
                      >
                        看全部条目(含已读)
                      </Button>
                    ) : undefined
                  }
                />
              </CardContent>
            </Card>
          )
        ) : chatView ? (
          /* ═══ TG 聊天视图(v4 既有全套,原样迁入左栏滚动区):气泡时间线,
              日期分隔走居中胶囊;含历史态照旧 ═══ */
          groups !== null ? (
            <div className="flex flex-col gap-4" data-testid="feed-chat-timeline">
              {groups.map((group) => (
                <section key={group.key} aria-label={`时间分组:${group.label}`}>
                  <div
                    data-testid={`feed-group-${group.label}`}
                    className="mx-auto w-fit rounded-full bg-muted/60 px-3 py-1 text-2xs text-muted-foreground"
                  >
                    {`${group.label} · ${group.items.length} 条`}
                  </div>
                  <div className="mt-1 flex flex-col gap-1.5">{group.items.map(renderCard)}</div>
                </section>
              ))}
            </div>
          ) : (
            // 不分组:平铺(行距 6px 密度档)
            <div className="flex flex-col gap-1.5" data-testid="feed-flat-list">
              {displayItems.map(renderCard)}
            </div>
          )
        ) : (
          /* ═══ 网站/日报渠道条目流(§2.3):v6 columns 多列瀑布流降为单列
              纵向列表(Kestra 行密度;左栏宽下单列读性最优),内容卡直出
              (deal 价格行/watch「有更新」徽标随卡);点击卡片 = 详情弹窗,
              悬停操作簇/右键随卡保留 ═══ */
          <div className="flex flex-col gap-1.5" data-testid="feed-stream-list">
            {displayItems.map(renderCard)}
          </div>
        )}

        {hasMore && !loading && !overviewMode ? (
          <Button variant="outline" size="sm" className="self-center" onClick={() => void loadMore()} disabled={loadingMore}>
            {loadingMore ? "加载中…" : "加载更早的条目"}
          </Button>
        ) : null}
      </div>
      </section>

      {/* ═══ 右栏:渠道列表(§1 群组列表,主人指定在右;导航本体常驻)═══ */}
      <aside
        aria-label="渠道列表"
        className="flex w-72 max-xl:w-64 shrink-0 flex-col border-l bg-muted/20"
      >
        {/* 搜索框(贴顶,§1.2:v6 工具条搜索位整体迁址,语义零改 —— 防抖
            300ms + Enter 即时 + Esc 即时清空,filterChannelsByQuery 客户端
            过滤右栏行,不发服务端查询;随右栏常驻 = ref 恒挂载,Mod+F 直聚焦) */}
        <div className="border-b px-3 py-2.5">
          <div className="relative">
            <Search
              aria-hidden
              className="pointer-events-none absolute top-1/2 left-2.5 size-3.5 -translate-y-1/2 text-muted-foreground/70"
            />
            <Input
              ref={searchInputRef}
              type="search"
              value={searchInput}
              data-testid="feed-channel-search"
              aria-label="搜索渠道"
              placeholder="搜索群组/渠道(名称 / 源 id,如 Tg)"
              className="w-full pl-8 text-xs"
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
          {searchActive ? (
            <p className="mt-1.5 text-2xs text-muted-foreground" data-testid="feed-search-scope">
              渠道过滤「{query}」· 按渠道名 / 源 id 包含匹配
            </p>
          ) : null}
        </div>
        {/* 行列表(内滚):ChannelRow 行形骨架(catalog 首拉)/ 搜索零命中
            行内小空态 / 渠道行(选中高亮 + 未读徽标) */}
        <div className="min-h-0 flex-1 overflow-y-auto py-1" data-testid="feed-channel-list">
          {catalogLoading && channelCards.length === 0 ? (
            <div
              className="flex flex-col gap-1 px-1.5"
              data-testid="feed-channel-loading"
              aria-busy="true"
              aria-label="渠道列表加载中"
            >
              {[0, 1, 2, 3, 4].map((row) => (
                <div key={row} className="flex items-start gap-2.5 rounded-md px-1.5 py-2">
                  <Skeleton className="mt-0.5 size-8 rounded-md" />
                  <div className="min-w-0 flex-1">
                    <div className="flex items-center justify-between gap-2">
                      <Skeleton className="h-3.5 w-2/5" />
                      <Skeleton className="h-2.5 w-8" />
                    </div>
                    <Skeleton className="mt-1.5 h-3 w-4/5" />
                  </div>
                </div>
              ))}
            </div>
          ) : visibleChannels.length === 0 && searchActive ? (
            /* 搜索零命中(§7 阶梯 1):右栏列表尾行内小空态(v6 墙态整卡
                等降格;testid 保留) */
            <div className="px-3 py-8 text-center" data-testid="feed-search-empty">
              <p className="text-xs font-medium text-foreground">没有匹配的渠道</p>
              <p className="mt-1 text-2xs leading-relaxed text-muted-foreground">
                {`搜索「${query}」零命中渠道(按渠道名 / 源 id 包含匹配);换个关键词,或清空搜索看全部渠道。`}
              </p>
            </div>
          ) : (
            visibleChannels.map((card) => (
              <ChannelRow
                key={card.key}
                card={card}
                selected={scope.source === card.key}
                current={listCurrentKey === card.key}
                navFocused={listCurrentKey === card.key && navPane === "list" && navByKeyboard}
                onCurrent={onCurrentRow}
                onOpen={openChannel}
              />
            ))
          )}
        </div>
        {/* 脚注(§1.4):渠道数词面;搜索时命中数。testid = feed-count 独占
            (复审 R1-1:选中态工具条条目计数另挂 feed-stream-count,防双挂) */}
        <div
          className="border-t px-3 py-2 text-2xs text-muted-foreground"
          data-testid="feed-count"
          title={`渠道全集 = 插件 health 源 ∪ 已加载条目来源;计数为已加载口径(全库首页 50 条铺底)`}
        >
          {searchActive
            ? `命中 ${visibleChannels.length} / ${channelCards.length} 个渠道`
            : `${channelCards.length} 个渠道`}
        </div>
      </aside>

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
