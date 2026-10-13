/**
 * 微信群信息面板(10-13-wechat-groupinfo R2;三级监控台「群信息」详情弹窗)。
 *
 * 形态判例:详情类用模态(任务令;FeedItemDetail 同族 Dialog 基件),尺寸取
 * 中量级 max-w-2xl(cron-screen.tsx:1172 大表单档)而非整屏画布 —— 群信息
 * 是读面不是工作面,成员列表 max-h 内滚即可,长公告靠折叠展开承接(10-08
 * 详情弹窗「小窗挤压长文」教训的针对性解法,不再整屏化)。
 *
 * 结构(任务令形态逐项):设置区(群名大字 / 群主 / 群公告可折叠长文截断展开 /
 * 成员 N 人)+ 成员列表(显示名为主,wxid 次要灰字,群主带「群主」标记)。
 * 导出按钮(R3)态机:idle「导出」→ 导出中(禁用)→ 成功/失败行内提示
 * (成功含两件落盘路径;取消保存对话框 = 静默回 idle 零提示)——壳侧
 * `wechat_group_export {chat_id, json_payload}` 接前端已持应答原样落盘
 * (JSON + 同目录同名成员表 CSV,通道 ./wechat-group-export-api),壳不重查。
 * 文案判例「行话零容忍」:可见词面全人话(群公告/群主/成员 N 人/备注);
 * chat_id / wxid 等协议词只作 title 悬浮与成员行次要灰字(任务令明准)。
 *
 * 数据 = ./wechat-groupinfo-api 的 wechatGroupInfo()(壳 spawn 桥 localdb
 * group-info,契约 prd「group-info 应答契约 v1」);缺库缺表如实降级
 * (owner/announcement null → 「—」,member_count null → 「成员数未知」,
 * 不虚构)。Esc 与遮罩关闭由 ui/dialog.tsx 基件承担;浮层让位收口同
 * FeedItemDetail(基件 Esc preventDefault,屏级巡游线自动让位)。
 */
import { useEffect, useState } from "react";

import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";
import type { SidecarRequestError } from "@/lib/api";

import { channelDisplayName } from "./api";
import {
  wechatGroupExport,
  type WechatGroupExportResult,
} from "./wechat-group-export-api";
import { wechatGroupInfo, type WechatGroupInfo } from "./wechat-groupinfo-api";
import { ErrorBox } from "@/screens/settings/error-box";
import { asSidecarError } from "@/screens/settings/api";

/** 群公告折叠阈(字符;feed-screen image_ocr 卡面摘要 160 字符判例同门,
 *  超 = 截断 + 「展开全文」钮,展开后全文 + 「收起」) */
const ANNOUNCEMENT_COLLAPSE_CHARS = 160;

/** 面板数据态三相位(载/错/成互斥;feed 空/载/错三态齐备判例同门) */
type PanelState =
  | { phase: "loading" }
  | { phase: "error"; error: SidecarRequestError }
  | { phase: "done"; info: WechatGroupInfo };

/**
 * 导出按钮态机(R3):idle「导出」可点 → exporting「导出中…」禁用 →
 * 成功(行内两件路径)/ 失败(行内人话,按钮回可点即重试)。取消保存
 * 对话框 = 壳回 null → 静默回 idle(零提示,不打扰)。
 */
type ExportState =
  | { phase: "idle" }
  | { phase: "exporting" }
  | { phase: "success"; result: WechatGroupExportResult }
  | { phase: "failed"; message: string };

/** 绝对时间(群公告发布时刻):YYYY-MM-DD HH:mm(feed-screen
 *  formatAbsoluteTime 同形;非 ISO 原样回显,不猜) */
function formatAnnouncementTime(iso: string): string {
  const then = new Date(iso);
  if (Number.isNaN(then.getTime())) return iso;
  const pad = (value: number) => String(value).padStart(2, "0");
  return `${then.getFullYear()}-${pad(then.getMonth() + 1)}-${pad(then.getDate())} ${pad(then.getHours())}:${pad(then.getMinutes())}`;
}

/**
 * 群信息面板(挂载即拉数;source = 微信群源名全称,内部剥 weixin- 前缀作
 * 寻址键)。onClose = Dialog onOpenChange(false) 收口,调用方置 null 卸载。
 */
export function WxGroupInfoPanel({
  source,
  onClose,
}: {
  /** 微信群源名(源名全称律 weixin-<会话名>;寻址键派生见 api 模块) */
  source: string;
  onClose: () => void;
}) {
  const [state, setState] = useState<PanelState>({ phase: "loading" });
  const [tick, setTick] = useState(0);
  // 群公告展开态(默认折叠;换群重拉即回折叠,不跨群粘连)
  const [announceExpanded, setAnnounceExpanded] = useState(false);
  // 导出态机(idle 起;换群/重拉即回 idle,成功路径提示不跨群粘连)
  const [exportState, setExportState] = useState<ExportState>({ phase: "idle" });

  useEffect(() => {
    let cancelled = false;
    setState({ phase: "loading" });
    setAnnounceExpanded(false);
    setExportState({ phase: "idle" });
    wechatGroupInfo(source)
      .then((info) => {
        if (cancelled) return;
        setState({ phase: "done", info });
      })
      .catch((error) => {
        if (cancelled) return;
        // 已是 SidecarRequestError 原样返回,其余归一化(weixin-account-card 同款)
        setState({ phase: "error", error: asSidecarError(error) });
      });
    return () => {
      cancelled = true;
    };
  }, [source, tick]);

  /** 导出(R3):前端已持 group-info 应答原样交壳(chat_id + 全量载荷),
   *  壳弹保存对话框落盘,零重查。null = 用户取消,静默回 idle。 */
  const runExport = () => {
    if (state.phase !== "done" || exportState.phase === "exporting") return;
    const info = state.info;
    setExportState({ phase: "exporting" });
    wechatGroupExport(info.chat_id, info)
      .then((result) => {
        if (result === null) {
          setExportState({ phase: "idle" }); // 取消保存对话框 = 静默,零提示
          return;
        }
        setExportState({ phase: "success", result });
      })
      .catch((error) => {
        setExportState({ phase: "failed", message: asSidecarError(error).message });
      });
  };

  // 群名:桥 display_name 优先(库内实锚),解析不出回落行名(源剥前缀),
  // 再缺 = 寻址键原样 —— 三级回退全真名,零虚构
  const fallbackName = channelDisplayName(source);
  const groupName = state.phase === "done" ? (state.info.display_name ?? fallbackName) : fallbackName;

  return (
    <Dialog open onOpenChange={(next) => { if (!next) onClose(); }}>
      <DialogContent
        className="flex max-w-2xl flex-col gap-0 overflow-hidden p-0"
        data-testid="wx-groupinfo-dialog"
      >
        <DialogHeader className="flex-none border-b border-border/60 px-5 pb-3 pt-4">
          <DialogTitle className="text-base" data-testid="wx-groupinfo-title">
            群信息
          </DialogTitle>
        </DialogHeader>

        {state.phase === "loading" ? (
          <div
            className="flex min-h-40 flex-1 items-center justify-center px-5 py-6"
            data-testid="wx-groupinfo-loading"
          >
            <span className="text-xs text-muted-foreground">正在读取群信息…</span>
          </div>
        ) : state.phase === "error" ? (
          <div className="flex-1 px-5 py-4" data-testid="wx-groupinfo-error">
            <ErrorBox error={state.error} onRetry={() => setTick((value) => value + 1)} />
          </div>
        ) : (
          <>
            {/* 中段主滚动区:设置区 + 成员列表(长成员表在此滚,头/底常驻) */}
            <div className="flex min-h-0 flex-1 flex-col gap-4 overflow-y-auto px-5 py-4">
              {/* ═══ 设置区(群名大字 / 群主 / 群公告 / 成员 N 人)═══ */}
              <section className="flex flex-col gap-3" data-testid="wx-groupinfo-settings">
                {/* 群名大字(卡面 truncate 的反面:弹窗内不截断;chat_id 只
                    作 title 悬浮,协议词不上屏) */}
                <h3
                  className="break-words text-lg font-semibold leading-snug text-foreground"
                  data-testid="wx-groupinfo-name"
                  title={state.info.chat_id}
                >
                  {groupName}
                </h3>
                <div className="flex flex-col gap-0.5">
                  <span className="text-2xs text-muted-foreground">群主</span>
                  <span className="text-sm text-foreground" data-testid="wx-groupinfo-owner">
                    {state.info.owner?.display ?? "—"}
                    {state.info.owner ? (
                      <span className="ml-2 font-mono text-2xs text-muted-foreground">
                        {state.info.owner.username}
                      </span>
                    ) : null}
                  </span>
                </div>
                <AnnouncementBlock
                  info={state.info}
                  expanded={announceExpanded}
                  onToggle={() => setAnnounceExpanded((value) => !value)}
                />
                <div className="flex flex-col gap-0.5">
                  <span className="text-2xs text-muted-foreground">成员</span>
                  <span className="text-sm text-foreground" data-testid="wx-groupinfo-member-count">
                    {state.info.member_count === null ? "成员数未知" : `成员 ${state.info.member_count} 人`}
                  </span>
                </div>
              </section>

              {/* ═══ 成员列表(显示名为主,wxid 次要灰字,群主带标记)═══ */}
              <section className="flex min-h-0 flex-col gap-1.5">
                {state.info.members.length === 0 ? (
                  <p className="py-2 text-xs text-muted-foreground" data-testid="wx-groupinfo-members-empty">
                    暂无成员数据
                  </p>
                ) : (
                  <ul
                    className="max-h-72 overflow-y-auto rounded-md border border-border/60"
                    data-testid="wx-groupinfo-members"
                  >
                    {state.info.members.map((member) => (
                      <li
                        key={member.username}
                        data-testid={`wx-groupinfo-member-${member.username}`}
                        className="border-b border-border/40 px-2.5 py-1.5 last:border-b-0 hover:bg-accent/50"
                      >
                        <div className="flex items-center gap-1.5">
                          <span className="min-w-0 truncate text-sm text-foreground">
                            {member.display ?? "—"}
                          </span>
                          {member.is_owner ? (
                            <Badge
                              variant="secondary"
                              className="shrink-0 px-1 py-0 text-2xs"
                              data-testid="wx-groupinfo-owner-badge"
                            >
                              群主
                            </Badge>
                          ) : null}
                        </div>
                        <p className="truncate text-2xs text-muted-foreground">
                          {member.remark ? (
                            <span title={`备注:${member.remark}`}>备注 {member.remark} · </span>
                          ) : null}
                          <span className="font-mono">{member.username}</span>
                        </p>
                      </li>
                    ))}
                  </ul>
                )}
              </section>
            </div>

            {/* 动作簇(底栏常驻):导出态机(R3)——行内提示占左(成功含
                两件落盘路径,截断 + title 悬浮全路径),按钮居右 */}
            <div
              className="flex flex-none items-center justify-end gap-1.5 border-t border-border/60 px-5 py-3"
              data-testid="wx-groupinfo-actions"
            >
              <ExportStatus state={exportState} />
              <Button
                variant="outline"
                size="sm"
                disabled={exportState.phase === "exporting"}
                onClick={runExport}
                title={exportState.phase === "exporting" ? "正在导出…" : "导出"}
                data-testid="wx-groupinfo-export"
              >
                {exportState.phase === "exporting" ? "导出中…" : "导出"}
              </Button>
            </div>
          </>
        )}
      </DialogContent>
    </Dialog>
  );
}

/**
 * 导出行内提示(R3;idle/导出中 = 零渲染,动作簇只剩按钮):成功 = 两件
 * 落盘路径各占一行(截断 + title 悬浮全路径,「已导出」+「成员表 N 行」
 * 人话);失败 = 壳侧人话 message 原样(按钮回可点,再点即重试)。取消 =
 * 态机静默回 idle,本件零渲染零提示。role="status" 语义(读屏可达,判例
 * vision-form.tsx 存档提示行)。
 */
function ExportStatus({ state }: { state: ExportState }) {
  if (state.phase === "success") {
    return (
      <div
        className="min-w-0 flex-1 text-2xs leading-snug"
        role="status"
        data-testid="wx-groupinfo-export-success"
      >
        <p className="truncate text-ok" title={state.result.json_path}>
          已导出:{state.result.json_path}
        </p>
        <p
          className="truncate text-muted-foreground"
          title={`成员表(${state.result.member_rows} 行):${state.result.csv_path}`}
        >
          成员表 {state.result.member_rows} 行:{state.result.csv_path}
        </p>
      </div>
    );
  }
  if (state.phase === "failed") {
    return (
      <p
        className="min-w-0 flex-1 truncate text-2xs text-destructive"
        role="status"
        title={state.message}
        data-testid="wx-groupinfo-export-failed"
      >
        导出失败:{state.message}
      </p>
    );
  }
  return null;
}

/** 群公告块(null 如实「—」;长文默认截断 160 字符,展开/收起就地切换) */
function AnnouncementBlock({
  info,
  expanded,
  onToggle,
}: {
  info: WechatGroupInfo;
  expanded: boolean;
  onToggle: () => void;
}) {
  const announcement = info.announcement;
  const text = announcement?.text ?? null;
  const editor = announcement?.editor_display ?? null;
  const publishedAt = announcement?.published_at ?? null;
  const collapsible = text !== null && text.length > ANNOUNCEMENT_COLLAPSE_CHARS;
  // 可见文本:短文全文直出;长文折叠 = 前 160 字符 + 省略号(title 悬浮留
  // 全文,feed-screen image_ocr 摘要判例),展开 = 全文
  const visible =
    text === null ? null : collapsible && !expanded ? `${text.slice(0, ANNOUNCEMENT_COLLAPSE_CHARS)}…` : text;
  return (
    <div className="flex flex-col gap-0.5" data-testid="wx-groupinfo-announcement">
      <span className="text-2xs text-muted-foreground">群公告</span>
      {visible !== null ? (
        <>
          <p className="whitespace-pre-wrap break-words text-sm leading-relaxed text-foreground/90">
            {visible}
          </p>
          {/* 公告元信息:编辑人 + 发布时刻(各自如实缺席,双双无 = 零渲染) */}
          {editor !== null || publishedAt !== null ? (
            <p className="text-2xs text-muted-foreground">
              {editor !== null ? `${editor} 编辑` : null}
              {editor !== null && publishedAt !== null ? " · " : null}
              {publishedAt !== null ? (
                <time dateTime={publishedAt}>{formatAnnouncementTime(publishedAt)}</time>
              ) : null}
            </p>
          ) : null}
          {collapsible ? (
            <button
              type="button"
              data-testid="wx-groupinfo-announcement-toggle"
              aria-expanded={expanded}
              onClick={onToggle}
              className="w-fit text-2xs text-primary hover:underline"
            >
              {expanded ? "收起" : "展开全文"}
            </button>
          ) : null}
        </>
      ) : (
        <span className="text-sm text-muted-foreground">—</span>
      )}
    </div>
  );
}
