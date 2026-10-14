/**
 * 「微信本机」朋友圈分区(task 10-14-wechat-media-sns R5)。
 *
 * 微信本机工作台族的新分区(版式并入 WechatLocalSection 同族 Card,不新路由
 * 不新画布;接线归集成员——在 wechat-local.tsx 的 CardContent 内挂本组件):
 * 时间线列表(发帖人+时间+正文+媒体位)+ 导出按钮(触发桥 sns_export 并
 * 回报产物路径)。
 *
 * 数据面 = sidecar ``wechat_local.sns_feed``(包桥 ``localdb sns feed``)与
 * ``wechat_local.sns_export``(包 ``localdb sns export``);invoke 直连壳命令
 * (屏私有封装惯例,api.ts 共享门面不动——sidecar-protocol.md 变更纪律 3;
 * 本文件自带最小封装)。
 *
 * 文案全人话判例(AC5):「朋友圈」「导出」;零「回源」类工程词上屏——
 * 媒体状态词面由桥侧判例供给(已解密/明文复制/…),本层原样呈现。
 * 读回仅展示不入情报管线(G3 同判例);媒体下载缺省关,导出默认不带媒体。
 */
import { useCallback, useState } from "react";
import { invoke } from "@tauri-apps/api/core";

import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { SidecarRequestError } from "@/lib/api";

import { asSidecarError, formatLastSeen } from "../api";

// ---------------------------------------------------------------------------
// sidecar 最小封装(方法名与 entry.py 薄壳双侧同步;接线批归集成员)
// ---------------------------------------------------------------------------

/** 一条朋友圈动态(桥 localdb sns feed 载荷条目;sns_query 契约)。 */
export interface WechatSnsEntry {
  id: string;
  username: string;
  nickname: string | null;
  create_time: number;
  text: string | null;
  media_count: number;
  media_types: string[];
  ref_username: string | null;
  ref_nickname: string | null;
}

/** sns_export 应答(桥 localdb sns export 载荷;sns_export.py 契约)。 */
export interface WechatSnsExportView {
  format: "json" | "html";
  out_dir: string;
  files: string[];
  with_media: boolean;
  stats: Record<string, unknown>;
}

/** 朋友圈动态(只读;时间线窗口 = 天数)。 */
export async function wechatLocalSnsFeed(sinceDays: number): Promise<WechatSnsEntry[]> {
  try {
    const result = await invoke<{ sns: { feed: WechatSnsEntry[] } }>("sidecar_request", {
      method: "wechat_local.sns_feed",
      params: { since_days: sinceDays },
    });
    return result.sns.feed;
  } catch (raw) {
    throw asSidecarError(raw);
  }
}

/** 朋友圈导出(format 缺省 html;with_media 缺省关——媒体下载是显式选择)。 */
export async function wechatLocalSnsExport(params: {
  format: "json" | "html";
  since_days: number;
  with_media?: boolean;
  out?: string;
}): Promise<WechatSnsExportView> {
  try {
    const result = await invoke<{ sns_export: WechatSnsExportView }>("sidecar_request", {
      method: "wechat_local.sns_export",
      params,
    });
    return result.sns_export;
  } catch (raw) {
    throw asSidecarError(raw);
  }
}

// ---------------------------------------------------------------------------
// 组件
// ---------------------------------------------------------------------------

/** 结构化错误行(weatch-local 同族形态;面板内联内容,不带 role="alert")。 */
function SnsErrorBox({ error, testId }: { error: SidecarRequestError; testId: string }) {
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
      {fixHint ? <span className="min-w-0 break-words text-2xs opacity-80">修复指引:{fixHint}</span> : null}
    </div>
  );
}

/** 媒体类型徽标(media_types 判例:2=图/6=视频;其余中性计数)。 */
function MediaBadges({ types }: { types: string[] }) {
  if (types.length === 0) return null;
  const images = types.filter((t) => t === "2").length;
  const videos = types.filter((t) => t === "6").length;
  const rest = types.length - images - videos;
  return (
    <>
      {images > 0 ? <Badge variant="outline">图片 ×{images}</Badge> : null}
      {videos > 0 ? <Badge variant="outline">视频 ×{videos}</Badge> : null}
      {rest > 0 ? <Badge variant="outline">其他媒体 ×{rest}</Badge> : null}
    </>
  );
}

/** 朋友圈分区:时间线 + 导出(纯组件态,读回不入 store/dedup)。 */
export function WechatSnsTimeline() {
  const [sinceDays, setSinceDays] = useState("30");
  const [loading, setLoading] = useState(false);
  const [feed, setFeed] = useState<WechatSnsEntry[] | null>(null);
  const [error, setError] = useState<SidecarRequestError | null>(null);
  const [exportFormat, setExportFormat] = useState<"html" | "json">("html");
  const [exporting, setExporting] = useState(false);
  const [exportResult, setExportResult] = useState<WechatSnsExportView | null>(null);
  const [exportError, setExportError] = useState<SidecarRequestError | null>(null);

  const daysValue = (): number | null => {
    const parsed = Number.parseInt(sinceDays, 10);
    return Number.isFinite(parsed) && parsed > 0 ? parsed : null;
  };

  const loadFeed = useCallback(async () => {
    const days = daysValue();
    if (days === null) {
      setError(
        new SidecarRequestError({ code: "invalid_params", path: "since_days", message: "天数须为正整数" }),
      );
      return;
    }
    setError(null);
    setLoading(true);
    try {
      setFeed(await wechatLocalSnsFeed(days));
    } catch (raw) {
      setFeed(null);
      setError(asSidecarError(raw));
    } finally {
      setLoading(false);
    }
  }, [sinceDays]);

  const runExport = useCallback(async () => {
    const days = daysValue();
    if (days === null) {
      setExportError(
        new SidecarRequestError({ code: "invalid_params", path: "since_days", message: "天数须为正整数" }),
      );
      return;
    }
    setExportError(null);
    setExporting(true);
    try {
      setExportResult(await wechatLocalSnsExport({ format: exportFormat, since_days: days }));
    } catch (raw) {
      setExportResult(null);
      setExportError(asSidecarError(raw));
    } finally {
      setExporting(false);
    }
  }, [sinceDays, exportFormat]);

  const ordered = feed ? [...feed].reverse() : null; // 桥侧升序,时间线最新在前

  return (
    <div className="flex min-w-0 flex-col gap-2" data-testid="wechat-sns-section">
      <p className="min-w-0 break-words text-xs font-medium text-foreground">
        朋友圈
        <span className="ml-2 text-2xs font-normal text-muted-foreground">
          只读时间线(正文与媒体状态);导出产物落在本机私有目录
        </span>
      </p>
      <div className="flex min-w-0 flex-wrap items-center gap-2">
        <Input
          aria-label="朋友圈天数"
          type="number"
          min={1}
          step={1}
          className="h-8 w-20 text-xs"
          value={sinceDays}
          disabled={loading || exporting}
          onChange={(event) => setSinceDays(event.target.value)}
        />
        <span className="text-2xs text-muted-foreground">天</span>
        <Button
          size="sm"
          variant="outline"
          disabled={loading || exporting}
          data-testid="wechat-sns-load"
          onClick={() => void loadFeed()}
        >
          {loading ? "拉取中…" : "拉取朋友圈"}
        </Button>
        <select
          aria-label="导出格式"
          className="h-8 rounded-md border border-border bg-background px-2 text-xs"
          value={exportFormat}
          disabled={exporting || loading}
          onChange={(event) => setExportFormat(event.target.value === "json" ? "json" : "html")}
        >
          <option value="html">网页</option>
          <option value="json">数据</option>
        </select>
        <Button
          size="sm"
          variant="outline"
          disabled={loading || exporting}
          data-testid="wechat-sns-export"
          onClick={() => void runExport()}
        >
          {exporting ? "导出中…" : "导出"}
        </Button>
      </div>
      {error ? <SnsErrorBox error={error} testId="wechat-sns-error" /> : null}
      {exportError ? <SnsErrorBox error={exportError} testId="wechat-sns-export-error" /> : null}
      {exportResult ? (
        <div
          className="flex min-w-0 flex-col gap-0.5 rounded-md border border-border/60 bg-muted/30 px-3 py-2"
          data-testid="wechat-sns-export-result"
        >
          <p className="min-w-0 break-words text-xs text-foreground">
            已导出(格式 {exportResult.format === "html" ? "网页" : "数据"},共 {exportResult.files.length} 个文件)
          </p>
          <p className="min-w-0 break-all font-mono text-2xs text-muted-foreground" title={exportResult.out_dir}>
            {exportResult.out_dir}
          </p>
        </div>
      ) : null}
      {ordered !== null && ordered.length === 0 ? (
        <p className="text-2xs text-muted-foreground" data-testid="wechat-sns-empty">
          窗口内没有朋友圈动态(库内无命中或窗口外)。
        </p>
      ) : null}
      {ordered && ordered.length > 0 ? (
        <ul className="flex max-h-96 flex-col gap-1 overflow-y-auto" data-testid="wechat-sns-timeline">
          {ordered.map((entry) => (
            <li
              key={entry.id}
              className="flex min-w-0 flex-col gap-0.5 rounded-md border border-border/50 px-2.5 py-1.5"
              data-testid={`wechat-sns-entry-${entry.id}`}
            >
              <p className="flex min-w-0 flex-wrap items-center gap-1.5 text-2xs text-muted-foreground">
                <span className="min-w-0 truncate font-medium text-foreground" title={entry.username}>
                  {entry.nickname ?? entry.username}
                </span>
                <span className="shrink-0 font-mono">{formatLastSeen(entry.create_time)}</span>
                <MediaBadges types={entry.media_types} />
              </p>
              {entry.text ? (
                <p className="min-w-0 whitespace-pre-wrap break-words text-xs leading-relaxed text-foreground">
                  {entry.text}
                </p>
              ) : null}
              {entry.media_count > 0 ? (
                <p className="min-w-0 break-words text-2xs text-muted-foreground">
                  媒体 {entry.media_count} 项(导出后可见状态:已解密/明文复制等)
                </p>
              ) : null}
              {entry.ref_nickname ? (
                <p className="min-w-0 break-words text-2xs text-muted-foreground">转发自 {entry.ref_nickname}</p>
              ) : null}
            </li>
          ))}
        </ul>
      ) : null}
    </div>
  );
}
