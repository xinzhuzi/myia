/**
 * 「微信本机」工作区(task 10-11-wechat-ui-bridge F3/F4;design §5.2)。
 *
 * 消息屏微信区的本机侧工作面,与上方平台总览的「微信本机」卡共用同一探针
 * 真源(wechat_local.probe,屏级拉取后下传),三块内容:
 *
 * - 状态头:探针三态胶囊(ok→可用绿 / degraded→降级黄 / 其余→不可用灰)+
 *   版本行(微信/桥组件版本,mono)+ 降级原因逐条(码名 + 修复指引);
 *   sidecar 未接线(method_not_found)时降级说明,不挡整屏(alerts 面板
 *   unsupported 判例同款)。
 * - AX 权限引导卡(F3):辅助功能授权分步指引,常驻渲染(装机授权主体是
 *   MYIA app 本体,design §5.1);探针 checks.ax_permission 在场时如实标注
 *   现状(未授权 → warning 强调)。版面遵循 10-05 判例:同版面常驻分区、
 *   无返回钮;文字三层防:容器 min-w-0 防撑破 / 列表行 truncate+title 防
 *   溢出 / 正文 break-words 防长串。
 * - 只读会话入口(F4,G2):选会话 → 拉最近消息展示;**读回仅展示,不入
 *   情报管线**(G3:零 store/dedup/分类接线,纯组件态);本地库查询行
 *   (chat_id + 天数 → 三域查询)同区承载 E 段产出。桥的错误族(design §6)
 *   结构化直显,不重试不静默(发送频控语义在桥内,本区无发送面)。
 */
import { useCallback, useState } from "react";

import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { cn } from "@/lib/utils";
import { SidecarRequestError } from "@/lib/api";

import { asSidecarError, formatLastSeen, wechatLocalMessages, wechatLocalQuery, wechatLocalSessions } from "./api";
import type { WechatLocalMessage, WechatLocalProbeView } from "./api";

/** 探针三态 → 胶囊(文案 + tone);与平台总览卡的 degraded 黄态同源。 */
function probePill(probe: WechatLocalProbeView | null, probeError: SidecarRequestError | null) {
  if (probeError?.code === "method_not_found") {
    return { label: "sidecar 未接线", tone: "border-border bg-muted/50 text-muted-foreground" as const };
  }
  if (probe?.state === "ok") return { label: "可用", tone: "border-ok/30 bg-ok/10 text-ok" as const };
  if (probe?.state === "degraded") return { label: "降级", tone: "border-warning/30 bg-warning/10 text-warning" as const };
  return { label: "不可用", tone: "border-border bg-muted/50 text-muted-foreground" as const };
}

/** 探针降级原因/不可用原因行(码名 + 修复指引;三层防:break-words)。 */
function ReasonList({ probe }: { probe: WechatLocalProbeView }) {
  if (probe.reasons.length === 0) return null;
  return (
    <ul className="flex flex-col gap-1" data-testid="wechat-local-reasons">
      {probe.reasons.map((reason) => (
        <li key={reason.code} className="min-w-0 break-words text-2xs leading-relaxed text-muted-foreground">
          <code className="font-mono text-foreground">{reason.code}</code>
          <span className="mx-1">—</span>
          {reason.fix_hint}
        </li>
      ))}
    </ul>
  );
}

/** 一条读回消息(只读展示;文本出原文,媒体类出「类型 + 占位」徽标)。 */
function MessageRow({ message }: { message: WechatLocalMessage }) {
  const isText = message.type === "text" && typeof message.text === "string";
  return (
    <li className="flex min-w-0 flex-col gap-0.5 rounded-md border border-border/50 px-2.5 py-1.5">
      <p className="flex min-w-0 flex-wrap items-center gap-1.5 text-2xs text-muted-foreground">
        {/* 三层防:时间/发送者单行 truncate + title 全文兜底 */}
        <span className="shrink-0 font-mono">{formatLastSeen(message.ts)}</span>
        <span className="min-w-0 truncate" title={message.sender}>
          {message.sender}
        </span>
        <Badge variant="outline">{message.type}</Badge>
      </p>
      {isText ? (
        <p className="min-w-0 whitespace-pre-wrap break-words text-xs leading-relaxed text-foreground">
          {message.text}
        </p>
      ) : (
        <p className="min-w-0 break-words text-xs italic text-muted-foreground">
          {message.media_placeholder ?? "非文本消息,内容未导出(占位)"}
        </p>
      )}
    </li>
  );
}

/** 只读命令的结构化错误行(code + message + fix_hint;失败不重试不静默)。
 * 不带 role="alert":本区错误是面板内联内容,页面级 alert 语义归屏顶 ErrorBox,
 * 避免断连态双 alert 干扰读屏与测试选择器。 */
function ReadOnlyError({ error, testId }: { error: SidecarRequestError; testId: string }) {
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

interface WechatLocalSectionProps {
  /** wechat_local.probe 探针(屏级拉取;null = 探测缺位/失败,如实灰态)。 */
  probe: WechatLocalProbeView | null;
  /** 探针错误(method_not_found = sidecar 未接线 → 降级说明)。 */
  probeError: SidecarRequestError | null;
  /** 探针刷新中(外层「刷新」按钮共用状态)。 */
  refreshing: boolean;
  onRefresh: () => void;
}

export function WechatLocalSection({ probe, probeError, refreshing, onRefresh }: WechatLocalSectionProps) {
  const pill = probePill(probe, probeError);
  const axState = probe?.checks.ax_permission;
  return (
    <div className="px-6">
      <Card>
        <CardHeader className="flex-row items-start justify-between gap-2">
          <div className="flex min-w-0 flex-col gap-0.5">
            <CardTitle as="h2" className="flex items-center gap-2">
              微信本机
              <span
                className={cn(
                  "inline-flex shrink-0 items-center gap-1.5 rounded-full border px-2 py-0.5 text-2xs",
                  pill.tone,
                )}
                data-testid="wechat-local-state-pill"
              >
                {pill.label}
              </span>
            </CardTitle>
            <CardDescription>
              本机桥只读面(选会话 → 拉最近消息展示;读回不入情报管线)+ 本地库三域查询;与上方「微信」官方桥分工,出站归官方桥
            </CardDescription>
          </div>
          <Button
            size="sm"
            variant="outline"
            className="shrink-0"
            disabled={refreshing}
            data-testid="wechat-local-refresh"
            onClick={onRefresh}
          >
            刷新状态
          </Button>
        </CardHeader>
        <CardContent className="flex flex-col gap-4" data-testid="wechat-local-section">
          {probeError?.code === "method_not_found" ? (
            <p className="text-xs text-muted-foreground" data-testid="wechat-local-unsupported">
              当前 sidecar 还没有 wechat_local.* 方法(需要 10-11-wechat-ui-bridge F2 的协议批);升级后此处自动可用,其余面板功能不受影响。
            </p>
          ) : null}
          {probeError && probeError.code !== "method_not_found" ? (
            <ReadOnlyError error={probeError} testId="wechat-local-probe-error" />
          ) : null}

          {probe ? (
            <div className="flex min-w-0 flex-col gap-1.5" data-testid="wechat-local-probe-summary">
              <p className="min-w-0 truncate font-mono text-2xs text-muted-foreground" title={`wechat ${probe.wechat_version ?? "?"} / bridge ${probe.bridge_version ?? "?"}`}>
                微信 {probe.wechat_version ?? "?"} / 桥组件 {probe.bridge_version ?? "?"}
              </p>
              {probe.state !== "ok" ? <ReasonList probe={probe} /> : null}
            </div>
          ) : null}

          {/* ---- F3:AX 权限引导卡(常驻;授权主体 = MYIA app 本体)---- */}
          <div
            className={cn(
              "flex min-w-0 flex-col gap-1.5 rounded-md border p-3",
              axState === "fail"
                ? "border-warning/40 bg-warning/10"
                : "border-border/60 bg-muted/30",
            )}
            data-testid="wechat-local-ax-guide"
          >
            <p className="flex min-w-0 flex-wrap items-center gap-2 text-xs font-medium text-foreground">
              系统权限引导:辅助功能(AX)
              {axState === "ok" ? <Badge variant="default">已授权</Badge> : null}
              {axState === "fail" ? <Badge variant="destructive">未授权</Badge> : null}
            </p>
            <p className="min-w-0 break-words text-2xs leading-relaxed text-muted-foreground">
              本机桥读会话/消息走 macOS 辅助功能通道;授权主体是 MYIA app 本体(装机一次性)。步骤:打开
              <span className="mx-1 font-mono text-foreground" title="系统设置 → 隐私与安全性 → 辅助功能">
                系统设置 → 隐私与安全性 → 辅助功能
              </span>
              ,打开 MYIA 的开关,回到本屏点「刷新状态」。桥不抢前台焦点、不合成鼠标点击、不激活微信窗口(静默铁律)。
            </p>
          </div>

          {/* ---- F4:只读会话入口(G2 选会话 → 拉最近消息;G3 不入管线)---- */}
          <SessionReader />
          <LocalDbQuery />
        </CardContent>
      </Card>
    </div>
  );
}

// ---------------------------------------------------------------------------
// 只读会话入口(F4)
// ---------------------------------------------------------------------------

/** 只读会话面板内部态(纯组件态,读回不入 store/dedup——G3)。 */
function SessionReader() {
  const [loadingSessions, setLoadingSessions] = useState(false);
  const [sessions, setSessions] = useState<Array<{ id: string; name: string; unread: number }> | null>(null);
  const [selectedId, setSelectedId] = useState<string | null>(null);
  const [loadingMessages, setLoadingMessages] = useState(false);
  const [messages, setMessages] = useState<WechatLocalMessage[] | null>(null);
  const [error, setError] = useState<SidecarRequestError | null>(null);
  const [messagesError, setMessagesError] = useState<SidecarRequestError | null>(null);

  const loadSessions = useCallback(async () => {
    setError(null);
    setMessagesError(null);
    setLoadingSessions(true);
    try {
      const result = await wechatLocalSessions();
      setSessions(result.sessions);
    } catch (raw) {
      setSessions(null);
      setError(asSidecarError(raw));
    } finally {
      setLoadingSessions(false);
    }
  }, []);

  const openSession = useCallback(async (chatId: string) => {
    setSelectedId(chatId);
    setMessagesError(null);
    setMessages(null);
    setLoadingMessages(true);
    try {
      const result = await wechatLocalMessages(chatId);
      setMessages(result.messages);
    } catch (raw) {
      setMessagesError(asSidecarError(raw));
    } finally {
      setLoadingMessages(false);
    }
  }, []);

  return (
    <div className="flex min-w-0 flex-col gap-2" data-testid="wechat-local-readonly">
      <div className="flex min-w-0 flex-wrap items-center justify-between gap-2">
        <p className="min-w-0 break-words text-xs font-medium text-foreground">
          只读会话入口
          <span className="ml-2 text-2xs font-normal text-muted-foreground">
            拉回的消息仅此处展示,不进情报流、不打标、不去重(G3)
          </span>
        </p>
        <Button
          size="sm"
          variant="outline"
          className="shrink-0"
          disabled={loadingSessions}
          data-testid="wechat-local-load-sessions"
          onClick={() => void loadSessions()}
        >
          {loadingSessions ? "拉取中…" : "拉取会话列表"}
        </Button>
      </div>
      {error ? <ReadOnlyError error={error} testId="wechat-local-sessions-error" /> : null}
      {sessions !== null && sessions.length === 0 ? (
        <p className="text-2xs text-muted-foreground">会话列表为空(桥返回零条;确认微信主窗口已开)。</p>
      ) : null}
      {sessions && sessions.length > 0 ? (
        <ul className="flex min-w-0 flex-col gap-1" data-testid="wechat-local-session-list">
          {sessions.map((session) => (
            <li key={session.id}>
              <button
                type="button"
                aria-pressed={selectedId === session.id}
                className={cn(
                  "flex w-full min-w-0 items-center gap-2 rounded-md border px-2.5 py-1.5 text-left text-xs transition-colors duration-(--duration-fast) ease-out-expo hover:bg-accent/60",
                  selectedId === session.id ? "border-primary/40 bg-primary/10" : "border-border/50",
                )}
                data-testid={`wechat-local-session-${session.id}`}
                title={`${session.name}(${session.id})`}
                onClick={() => void openSession(session.id)}
              >
                <span className="min-w-0 flex-1 truncate font-medium text-foreground">{session.name}</span>
                {session.unread > 0 ? <Badge variant="secondary">未读 {session.unread}</Badge> : null}
                <span className="min-w-0 max-w-40 shrink truncate font-mono text-2xs text-muted-foreground">
                  {session.id}
                </span>
              </button>
            </li>
          ))}
        </ul>
      ) : null}
      {selectedId ? (
        <div className="flex min-w-0 flex-col gap-1.5">
          <p className="min-w-0 break-words text-2xs text-muted-foreground">
            会话 <code className="font-mono text-foreground">{selectedId}</code> 的最近消息
            {loadingMessages ? "(拉取中…)" : ""}
          </p>
          {messagesError ? <ReadOnlyError error={messagesError} testId="wechat-local-messages-error" /> : null}
          {messages !== null && messages.length === 0 ? (
            <p className="text-2xs text-muted-foreground">窗口内暂无可读文本消息(AX 只见已加载消息;历史请用下方本地库查询)。</p>
          ) : null}
          {messages && messages.length > 0 ? (
            <ul className="flex min-w-0 flex-col gap-1" data-testid="wechat-local-messages">
              {messages.map((message, index) => (
                <MessageRow key={`${message.ts}-${index}`} message={message} />
              ))}
            </ul>
          ) : null}
        </div>
      ) : null}
    </div>
  );
}

// ---------------------------------------------------------------------------
// 本地库查询(E 段产出消费面;G4 三域)
// ---------------------------------------------------------------------------

/** 本地库查询行(chat_id + 天数 → 桥 localdb query;结果同区只读展示)。 */
function LocalDbQuery() {
  const [chatId, setChatId] = useState("");
  const [sinceDays, setSinceDays] = useState("30");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<{ displayName: string | null; messages: WechatLocalMessage[]; domains: Record<string, string> } | null>(null);
  const [error, setError] = useState<SidecarRequestError | null>(null);

  const runQuery = useCallback(async () => {
    const id = chatId.trim();
    if (!id) {
      setError(new SidecarRequestError({ code: "invalid_params", path: "params.chat_id", message: "会话 id 不能为空" }));
      return;
    }
    setError(null);
    setLoading(true);
    try {
      const days = Number.parseInt(sinceDays, 10);
      const view = await wechatLocalQuery(id, Number.isFinite(days) && days > 0 ? days : undefined);
      setResult({
        displayName: view.display_name,
        messages: view.messages,
        domains: view.domains,
      });
    } catch (raw) {
      setResult(null);
      setError(asSidecarError(raw));
    } finally {
      setLoading(false);
    }
  }, [chatId, sinceDays]);

  return (
    <div className="flex min-w-0 flex-col gap-2" data-testid="wechat-local-db-query">
      <p className="min-w-0 break-words text-xs font-medium text-foreground">
        本地库查询(历史)
        <span className="ml-2 text-2xs font-normal text-muted-foreground">
          解密副本只读,零出网零微信进程交互;密钥途径未裁决(D4)时如实报 key_unavailable
        </span>
      </p>
      <div className="flex min-w-0 flex-wrap items-center gap-2">
        <Input
          aria-label="本地库会话 id"
          placeholder="会话 id(如 filehelper)"
          className="h-8 w-56 text-xs"
          value={chatId}
          disabled={loading}
          onChange={(event) => setChatId(event.target.value)}
        />
        <Input
          aria-label="历史天数"
          type="number"
          min={1}
          step={1}
          className="h-8 w-20 text-xs"
          value={sinceDays}
          disabled={loading}
          onChange={(event) => setSinceDays(event.target.value)}
        />
        <span className="text-2xs text-muted-foreground">天</span>
        <Button size="sm" variant="outline" disabled={loading} data-testid="wechat-local-db-run" onClick={() => void runQuery()}>
          {loading ? "查询中…" : "查询本地库"}
        </Button>
      </div>
      {error ? <ReadOnlyError error={error} testId="wechat-local-db-error" /> : null}
      {result ? (
        <div className="flex min-w-0 flex-col gap-1.5" data-testid="wechat-local-db-result">
          <p className="flex min-w-0 flex-wrap items-center gap-1.5 text-2xs text-muted-foreground">
            <span className="min-w-0 truncate">
              {result.displayName ? `展示名:${result.displayName}` : "展示名未解析(contact 域缺列或副本缺失)"}
            </span>
            {Object.entries(result.domains).map(([domain, status]) => (
              <Badge key={domain} variant={status === "ok" ? "outline" : "secondary"}>
                {domain}:{status}
              </Badge>
            ))}
          </p>
          {result.messages.length === 0 ? (
            <p className="text-2xs text-muted-foreground">窗口内零条文本消息(库内无命中或副本缺域,domains 徽标如实)。</p>
          ) : (
            <ul className="flex min-w-0 flex-col gap-1">
              {result.messages.map((message, index) => (
                <MessageRow key={`${message.ts}-${index}`} message={message} />
              ))}
            </ul>
          )}
        </div>
      ) : null}
    </div>
  );
}
