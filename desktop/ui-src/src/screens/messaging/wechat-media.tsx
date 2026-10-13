/**
 * 「微信本机」聊天媒体渲染件(task 10-14-wechat-media-sns R5)。
 *
 * 消息行媒体占位(wechat-local.tsx MessageRow「非文本消息,内容未导出(占位)」)
 * 的升级面:经桥 ``localdb media scan --decrypt`` 拉媒体清单,缩略图实显
 * (_t.dat 解密缓存)/视频显示 _thumb.jpg;点击同屏展开(组件内 state,
 * 不新造全局 viewer/画布);wxgf 词面「实况格式,暂不支持预览」。
 *
 * **消息列表本体 = C1(chat-export)交付面,本件只做媒体槽**:导出
 * ``MessageMediaSlot``(单条媒体槽,供 wechat-local MessageRow / C1 消息行
 * 替换占位)与 ``WechatChatMedia``(自足分区:会话 id + 天数 → 扫描 → 渲染;
 * 接线归集成员——在 wechat-local.tsx 的 CardContent 内挂载)。
 *
 * 缩略图 src 经 Tauri convertFileSrc(资产协议;C6 HTTP 媒体端点落地后可切
 * 端点 URL,组件只认 src 字符串)。数据面 = sidecar
 * ``wechat_local.media_scan``(包桥 ``localdb media scan --since Nd --decrypt``)。
 * 文案全人话(AC5):状态词面桥侧判例供给(待解密/已解密/文件缺失/…),
 * 路径/key 只出现在展开区 mono 块(协议面豁免)。
 */
import { useCallback, useState } from "react";
import { convertFileSrc, invoke } from "@tauri-apps/api/core";

import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { SidecarRequestError } from "@/lib/api";

import { asSidecarError, formatLastSeen } from "./api";

// ---------------------------------------------------------------------------
// sidecar 最小封装(方法名与 entry.py 薄壳双侧同步;接线批归集成员)
// ---------------------------------------------------------------------------

/** 一条媒体清单项(桥 localdb media scan 载荷;media.py 契约)。 */
export interface WechatMediaItem {
  message_ref: {
    ts: number;
    sender: string;
    local_type: number;
  };
  type: string;
  key: string | null;
  files: {
    thumb?: string | null;
    full?: string | null;
    video?: string | null;
    video_thumb?: string | null;
  };
  status: string | null;
  cached_path?: string | null;
}

/** media_scan 应答(media.py 载荷形状)。 */
export interface WechatMediaScanView {
  media: {
    chat_id: string;
    since_days: number;
    items: WechatMediaItem[];
    stats: Record<string, number>;
    provider: { configured: boolean; path: string | null };
  };
}

/** 聊天媒体扫描(decrypt=true:缩略图逐条解密进缓存,幂等零重解)。 */
export async function wechatLocalMediaScan(
  chatId: string,
  sinceDays: number,
  decrypt = true,
): Promise<WechatMediaScanView> {
  try {
    return await invoke<WechatMediaScanView>("sidecar_request", {
      method: "wechat_local.media_scan",
      params: { chat_id: chatId, since_days: sinceDays, decrypt },
    });
  } catch (raw) {
    throw asSidecarError(raw);
  }
}

// ---------------------------------------------------------------------------
// 媒体槽(单条;供消息行占位替换与扫描分区共用)
// ---------------------------------------------------------------------------

/** 本地文件路径 → 可渲染 src(资产协议;测试侧 mock convertFileSrc)。 */
function fileSrc(path: string): string {
  return convertFileSrc(path);
}

/** 单条媒体槽:缩略图实显 + 状态词面 + 点击同屏展开(组件内 state)。 */
export function MessageMediaSlot({
  item,
  expanded,
  onToggle,
}: {
  item: WechatMediaItem;
  expanded: boolean;
  onToggle: () => void;
}) {
  const isVideo = item.type === "video";
  const wxgf = item.status === "实况格式,暂不支持预览";
  const thumbPath = isVideo
    ? item.files.video_thumb ?? null
    : item.cached_path ?? null; // 图:解密缓存产物;视频:明文 _thumb.jpg
  return (
    <div className="flex min-w-0 flex-col gap-1" data-testid="wechat-media-slot">
      <button
        type="button"
        className="flex min-w-0 items-start gap-2 rounded-md border border-border/50 p-1.5 text-left transition-colors duration-(--duration-fast) ease-out-expo hover:bg-accent/60"
        data-testid="wechat-media-row"
        onClick={onToggle}
        aria-expanded={expanded}
      >
        {thumbPath && !wxgf ? (
          <img
            src={fileSrc(thumbPath)}
            alt={isVideo ? "视频缩略图" : "聊天图片缩略图"}
            className="h-16 w-16 shrink-0 rounded-md border border-border/50 object-cover"
            data-testid="wechat-media-thumb"
          />
        ) : (
          <span
            className="flex h-16 w-16 shrink-0 items-center justify-center rounded-md border border-border/50 bg-muted/40 text-center text-2xs leading-tight text-muted-foreground"
            data-testid="wechat-media-placeholder"
          >
            {wxgf ? "实况格式,暂不支持预览" : (item.status ?? "未解密")}
          </span>
        )}
        <span className="flex min-w-0 flex-col gap-0.5">
          <span className="flex min-w-0 flex-wrap items-center gap-1.5 text-2xs text-muted-foreground">
            <span className="shrink-0 font-mono">{formatLastSeen(item.message_ref.ts)}</span>
            <span className="min-w-0 truncate" title={item.message_ref.sender}>
              {item.message_ref.sender}
            </span>
            <Badge variant="outline">{isVideo ? "视频" : "图片"}</Badge>
          </span>
          <span className="min-w-0 break-words text-xs text-foreground">
            {item.status ?? "未解密"}
          </span>
          <span className="min-w-0 text-2xs text-muted-foreground">
            {expanded ? "收起" : "展开详情"}
          </span>
        </span>
      </button>
      {expanded ? (
        <div
          className="flex min-w-0 flex-col gap-1 rounded-md border border-border/60 bg-muted/20 px-2.5 py-2"
          data-testid="wechat-media-detail"
        >
          {thumbPath && !wxgf ? (
            <img
              src={fileSrc(thumbPath)}
              alt={isVideo ? "视频缩略图(大图)" : "聊天图片(大图)"}
              className="max-h-72 max-w-full self-start rounded-md border border-border/50 object-contain"
              data-testid="wechat-media-large"
            />
          ) : null}
          <p className="min-w-0 break-all font-mono text-2xs text-muted-foreground" title="媒体 key">
            {item.key ?? "(无 key)"}
          </p>
          {Object.entries(item.files).map(([name, path]) =>
            path ? (
              <p
                key={name}
                className="min-w-0 break-all font-mono text-2xs text-muted-foreground"
                title={`${name} 源文件路径`}
              >
                {name}: {path}
              </p>
            ) : null,
          )}
          {item.cached_path ? (
            <p
              className="min-w-0 break-all font-mono text-2xs text-muted-foreground"
              title="解密缓存产物路径"
            >
              cached: {item.cached_path}
            </p>
          ) : null}
        </div>
      ) : null}
    </div>
  );
}

// ---------------------------------------------------------------------------
// 聊天图片分区(自足:输入会话 id + 天数 → 扫描 → 媒体列表)
// ---------------------------------------------------------------------------

function MediaErrorBox({ error, testId }: { error: SidecarRequestError; testId: string }) {
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

/** 聊天图片分区:media_scan → 缩略图实显(媒体面;读回不入情报管线)。 */
export function WechatChatMedia() {
  const [chatId, setChatId] = useState("");
  const [sinceDays, setSinceDays] = useState("30");
  const [loading, setLoading] = useState(false);
  const [items, setItems] = useState<WechatMediaItem[] | null>(null);
  const [stats, setStats] = useState<Record<string, number> | null>(null);
  const [error, setError] = useState<SidecarRequestError | null>(null);
  const [expandedKey, setExpandedKey] = useState<string | null>(null);

  const runScan = useCallback(async () => {
    const id = chatId.trim();
    if (!id) {
      setError(
        new SidecarRequestError({ code: "invalid_params", path: "params.chat_id", message: "会话 id 不能为空" }),
      );
      return;
    }
    const days = Number.parseInt(sinceDays, 10);
    if (!Number.isFinite(days) || days <= 0) {
      setError(
        new SidecarRequestError({ code: "invalid_params", path: "since_days", message: "天数须为正整数" }),
      );
      return;
    }
    setError(null);
    setLoading(true);
    try {
      const view = await wechatLocalMediaScan(id, days);
      setItems(view.media.items);
      setStats(view.media.stats);
    } catch (raw) {
      setItems(null);
      setStats(null);
      setError(asSidecarError(raw));
    } finally {
      setLoading(false);
    }
  }, [chatId, sinceDays]);

  const slotKey = (item: WechatMediaItem, index: number): string =>
    `${item.message_ref.ts}-${item.key ?? index}`;

  return (
    <div className="flex min-w-0 flex-col gap-2" data-testid="wechat-media-section">
      <p className="min-w-0 break-words text-xs font-medium text-foreground">
        聊天图片
        <span className="ml-2 text-2xs font-normal text-muted-foreground">
          窗口内图片/视频缩略图(本机文件只读;缩略图经你的解密件解出,点击展开详情)
        </span>
      </p>
      <div className="flex min-w-0 flex-wrap items-center gap-2">
        <Input
          aria-label="聊天图片会话 id"
          placeholder="会话 id(如 filehelper)"
          className="h-8 w-56 text-xs"
          value={chatId}
          disabled={loading}
          onChange={(event) => setChatId(event.target.value)}
        />
        <Input
          aria-label="聊天图片天数"
          type="number"
          min={1}
          step={1}
          className="h-8 w-20 text-xs"
          value={sinceDays}
          disabled={loading}
          onChange={(event) => setSinceDays(event.target.value)}
        />
        <span className="text-2xs text-muted-foreground">天</span>
        <Button
          size="sm"
          variant="outline"
          disabled={loading}
          data-testid="wechat-media-scan"
          onClick={() => void runScan()}
        >
          {loading ? "扫描中…" : "扫描媒体"}
        </Button>
      </div>
      {error ? <MediaErrorBox error={error} testId="wechat-media-error" /> : null}
      {items !== null && items.length === 0 ? (
        <p className="text-2xs text-muted-foreground" data-testid="wechat-media-empty">
          窗口内没有图片/视频消息(库内无命中或窗口外)。
        </p>
      ) : null}
      {stats ? (
        <p className="min-w-0 break-words text-2xs text-muted-foreground" data-testid="wechat-media-stats">
          消息 {String(stats.messages ?? 0)} 条:图片 {String(stats.image ?? 0)}、视频 {String(stats.video ?? 0)}、
          其他 {String(stats.other ?? 0)};文件缺失 {String(stats.image_file_missing ?? 0)}
          {typeof stats.decrypted === "number" ? `;已解出 ${stats.decrypted}` : ""}
        </p>
      ) : null}
      {items && items.length > 0 ? (
        <ul className="flex max-h-96 flex-col gap-1.5 overflow-y-auto" data-testid="wechat-media-list">
          {items.map((item, index) => (
            <li key={slotKey(item, index)}>
              <MessageMediaSlot
                item={item}
                expanded={expandedKey === slotKey(item, index)}
                onToggle={() =>
                  setExpandedKey((current) =>
                    current === slotKey(item, index) ? null : slotKey(item, index),
                  )
                }
              />
            </li>
          ))}
        </ul>
      ) : null}
    </div>
  );
}
