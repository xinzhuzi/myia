/**
 * 浏览器专用模块页(10-08-browser-module 案甲;设置树「浏览器」一级分区)。
 *
 * PRD 主人令:工具内嵌界面调浏览器操作,单独模块单独搞浏览器——本页 =
 * 一切浏览器操作的治理面(单入口铁律):操作台账(登录中/完成/失败+重试)
 * + 每操作窗口管理(聚焦/关闭)+ 日志尾巴。首役 = tg_web 登录(Telegram
 * 卡「添加账号/重新登录」即调 browser.open,两侧状态同源联动);未来
 * 凭据授权/验证码/手动核验等浏览器需求同律接入(到模块登记新 kind)。
 *
 * 窗口形态(案甲):模块点「登录」→ 后台线程拉起 MYIA 自管 Chromium
 * (持久化配置档,复用既有 web-login 登录器零重写);禁屏控令豁免面 =
 * 用户主动点击触发的交互性窗口。IPC 契约见 ./browser-api.ts;失败零
 * 静默:依赖缺失/浏览器缺失/超时在卡面与模块页双上浮人话错误+修复指引。
 */
import { AppWindow, ChevronDown, Globe, RefreshCw } from "lucide-react";
import { useCallback, useEffect, useState } from "react";

import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import type { SidecarRequestError as SidecarRequestErrorType } from "@/lib/api";

import { asSidecarError } from "./api";
import { browserClose, browserFocus, browserList, browserOpen, type BrowserListResult } from "./browser-api";
import { ErrorBox } from "./error-box";

/** 台账轮询参数(有进行中操作时跑;5s × 24 ≈ 2 分钟,超上限放弃转手动)。 */
const POLL_INTERVAL_MS = 5_000;
const POLL_MAX_ATTEMPTS = 24;

/** phase → 徽标形态(登录中黄/完成绿/失败红/已关闭灰)。 */
const PHASE_BADGE: Record<string, { label: string; variant: "ok" | "destructive" | "outline" | "warning" }> = {
  running: { label: "登录中", variant: "warning" },
  done: { label: "完成", variant: "ok" },
  failed: { label: "失败", variant: "destructive" },
  closed: { label: "已关闭", variant: "outline" },
};

export function BrowserModuleCard() {
  const [ledger, setLedger] = useState<BrowserListResult | null>(null);
  const [loadError, setLoadError] = useState<SidecarRequestErrorType | null>(null);
  const [actionError, setActionError] = useState<SidecarRequestErrorType | null>(null);
  const [note, setNote] = useState<string | null>(null);
  const [busyOp, setBusyOp] = useState<string | null>(null);
  /** 有 running 操作时的对账轮询(完成/失败即停,上限放弃)。 */
  const [poll, setPoll] = useState(0);

  const refresh = useCallback(async () => {
    setLoadError(null);
    try {
      setLedger(await browserList());
    } catch (raw) {
      setLoadError(asSidecarError(raw));
    }
  }, []);

  useEffect(() => {
    void refresh();
  }, [refresh]);

  useEffect(() => {
    if (poll <= 0 || poll > POLL_MAX_ATTEMPTS) {
      if (poll > POLL_MAX_ATTEMPTS) setPoll(0);
      return;
    }
    let cancelled = false;
    const timer = setTimeout(() => {
      void browserList().then((next) => {
        if (cancelled) return;
        setLedger(next);
        const anyRunning = next.operations.some((row) => row.phase === "running");
        setPoll(anyRunning ? poll + 1 : 0);
      }).catch(() => {
        if (!cancelled) setPoll(poll + 1);
      });
    }, POLL_INTERVAL_MS);
    return () => {
      cancelled = true;
      clearTimeout(timer);
    };
  }, [poll]);

  const runAction = useCallback(
    async (opId: string, action: () => Promise<unknown>, successNote: string) => {
      setBusyOp(opId);
      setActionError(null);
      setNote(null);
      try {
        await action();
        setNote(successNote);
        setLedger(await browserList());
      } catch (raw) {
        setActionError(asSidecarError(raw));
      } finally {
        setBusyOp(null);
      }
    },
    [],
  );

  const handleFocus = useCallback(
    (opId: string) =>
      void runAction(opId, () => browserFocus(opId), `已请求聚焦操作 ${opId} 的浏览器窗口(带到前台)。`),
    [runAction],
  );

  const handleClose = useCallback(
    (opId: string) =>
      void runAction(opId, () => browserClose(opId), `已请求关闭操作 ${opId} 的浏览器窗口(收尾后台账转「已关闭」)。`),
    [runAction],
  );

  /** 失败重试:同 kind+会话键重开(force 清档重登,登录器惯例)。 */
  const handleRetry = useCallback(
    (opId: string, kind: string, sessionKey: string) =>
      void runAction(
        opId,
        () => browserOpen(kind, sessionKey, { force: true }),
        `操作 ${sessionKey} 已重新拉起浏览器窗口(清档重登)。`,
      ),
    [runAction],
  );

  const operations = ledger?.operations ?? [];
  const kinds = ledger?.kinds ?? {};

  return (
    <Card data-testid="browser-module-card">
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          <Globe className="size-4 text-muted-foreground" />
          浏览器操作
        </CardTitle>
        <CardDescription>
          一切浏览器操作的统一入口与台账(单入口:窗口生命周期/错误上浮/操作审计集中在本模块;
          登录窗 = MYIA 自管 Chromium,由你的点击触发拉起)。新浏览器需求(授权/验证码/核验)登记后同律接入。
        </CardDescription>
      </CardHeader>
      <CardContent className="flex flex-col gap-3">
        {loadError ? <ErrorBox error={loadError} onRetry={() => void refresh()} /> : null}
        {ledger === null && loadError === null ? (
          <span data-testid="browser-module-loading" className="py-2 text-xs text-muted-foreground">
            操作台账装载中…
          </span>
        ) : null}

        {ledger !== null ? (
          <div data-testid="browser-operations" className="flex flex-col gap-2">
            {operations.length === 0 ? (
              <p data-testid="browser-operations-empty" className="text-xs text-muted-foreground">
                尚无浏览器操作:到「Telegram 监控」分区点「添加账号 / 重新登录」即在本模块登记第一条操作
                (登录窗与账号状态两侧联动);这里也是未来授权/验证码/手动核验窗口的统一台账。
              </p>
            ) : null}
            {operations.map((op) => {
              const badge = PHASE_BADGE[op.phase] ?? { label: op.phase, variant: "outline" as const };
              const running = op.phase === "running";
              return (
                <div
                  key={op.op_id}
                  data-testid={`browser-op-${op.op_id}`}
                  className="flex flex-col gap-2 rounded-lg border border-border/60 bg-muted/20 px-3 py-2"
                >
                  <div className="flex flex-wrap items-center justify-between gap-2">
                    <div className="flex min-w-0 flex-wrap items-center gap-2">
                      <AppWindow className="size-3.5 shrink-0 text-muted-foreground" />
                      <span className="font-mono text-xs text-foreground">{op.session_key}</span>
                      <Badge variant={badge.variant} data-testid={`browser-op-${op.op_id}-phase`}>
                        {running ? <RefreshCw className="mr-1 size-3 animate-spin" /> : null}
                        {badge.label}
                      </Badge>
                      <span className="text-2xs text-muted-foreground">
                        {kinds[op.kind] ?? op.kind}
                        {op.started_at ? ` · 起 ${op.started_at}` : ""}
                      </span>
                    </div>
                    <div className="flex shrink-0 items-center gap-2">
                      {running ? (
                        <>
                          <Button
                            variant="outline"
                            size="sm"
                            disabled={busyOp === op.op_id}
                            onClick={() => handleFocus(op.op_id)}
                            data-testid={`browser-op-${op.op_id}-focus`}
                            title="把该操作的浏览器窗口带到前台(bring_to_front)"
                          >
                            聚焦
                          </Button>
                          <Button
                            variant="outline"
                            size="sm"
                            disabled={busyOp === op.op_id}
                            onClick={() => handleClose(op.op_id)}
                            data-testid={`browser-op-${op.op_id}-close`}
                            title="请求关闭该操作的浏览器窗口(登录态已落档的不受影响)"
                          >
                            关闭
                          </Button>
                        </>
                      ) : null}
                      {op.phase === "failed" ? (
                        <Button
                          variant="outline"
                          size="sm"
                          disabled={busyOp === op.op_id}
                          onClick={() => handleRetry(op.op_id, op.kind, op.session_key)}
                          data-testid={`browser-op-${op.op_id}-retry`}
                          title="清档重登:重新拉起该会话的浏览器窗口(force)"
                        >
                          <RefreshCw className="size-3.5" />
                          重试
                        </Button>
                      ) : null}
                    </div>
                  </div>
                  {op.note ? (
                    <p
                      role={op.phase === "failed" ? "alert" : "status"}
                      data-testid={`browser-op-${op.op_id}-note`}
                      className={op.phase === "failed" ? "break-all text-2xs text-destructive" : "break-all text-2xs text-muted-foreground"}
                    >
                      {op.note}
                    </p>
                  ) : null}
                  {op.phase === "failed" && op.fix_hint ? (
                    <p data-testid={`browser-op-${op.op_id}-fix`} className="break-all rounded-md border border-warning/40 bg-warning/[0.06] px-2 py-1.5 text-2xs text-warning">
                      修复指引:{op.fix_hint}
                    </p>
                  ) : null}
                  {op.log_tail.length > 0 ? (
                    <details data-testid={`browser-op-${op.op_id}-log`} className="text-2xs text-muted-foreground">
                      <summary className="flex cursor-pointer select-none items-center gap-1">
                        <ChevronDown className="size-3" />
                        日志尾巴(最近 {op.log_tail.length} 行)
                      </summary>
                      <pre className="mt-1 max-h-48 overflow-auto whitespace-pre-wrap break-all rounded-md bg-muted/40 px-2 py-1.5 font-mono text-2xs leading-4">
                        {op.log_tail.join("\n")}
                      </pre>
                    </details>
                  ) : null}
                </div>
              );
            })}
          </div>
        ) : null}

        <div className="flex flex-col gap-2 border-t border-border/60 pt-3">
          {actionError ? <ErrorBox error={actionError} /> : null}
          {note ? (
            <p role="status" data-testid="browser-action-note" className="text-xs leading-5 text-ok">
              {note}
            </p>
          ) : null}
          <p className="text-2xs leading-4 text-muted-foreground">
            台账为会话态(重启 app 后清空,已落档的登录态不受影响);登录窗由你的点击触发拉起,
            手机号/验证码/两步验证全在浏览器页面内输入,本模块零读取零落日志。
          </p>
        </div>
      </CardContent>
    </Card>
  );
}
