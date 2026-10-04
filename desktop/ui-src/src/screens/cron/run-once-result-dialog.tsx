import { Badge } from "@/components/ui/badge";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";
import type { RunExitStatus } from "@/lib/api";

/** 跑一次终态(done)或发起失败(error)形;cron 屏 RunOnceState 的两终态子集 */
export type RunOnceOutcome =
  | { phase: "done"; name: string; runId: number; status: RunExitStatus | null; exitCode: number | null }
  | { phase: "error"; name: string; message: string };

/** 终态人话(RunExitStatus → 中文,如实分级;未知枚举原样示不吞) */
const STATUS_TEXT: Record<Exclude<RunExitStatus, null>, string> = {
  success: "成功",
  config_error: "配置错误",
  failed: "失败",
  partial: "部分完成",
  cancelled: "已取消",
};

/** 状态徽章文案:done 取终态人话(status 缺位回落 exit/终态未知);error = 发起失败 */
function outcomeText(outcome: RunOnceOutcome): string {
  if (outcome.phase === "error") return "发起失败";
  if (outcome.status) return STATUS_TEXT[outcome.status] ?? outcome.status;
  return outcome.exitCode !== null ? `exit ${outcome.exitCode}` : "终态未知";
}

/** 徽章三分色:success=ok / failed+config_error=destructive / 其余(含终态未知)=warning */
function outcomeVariant(outcome: RunOnceOutcome): "ok" | "warning" | "destructive" {
  if (outcome.phase === "error") return "destructive";
  if (outcome.status === "success") return "ok";
  if (outcome.status === "failed" || outcome.status === "config_error") return "destructive";
  return "warning";
}

/**
 * 跑一次结果详情弹窗(10-05-run-once-result-dialog,grill Q3a+b 决议):
 * 判词同族「详情类信息进弹窗,不贴屏顶」——终态(成功/部分/失败如实分色)
 * 与发起失败(run_busy 等)统一模态呈现;run_id/status/exit 是 trace 值,
 * 收进 mono 技术小字(活性条行话判例:活性面只留人话)。
 *
 * Dialog 基件(本屏 job 编辑/急停同款,Radix):ESC/遮罩/X 三径关由基件
 * 承担;关闭 = 屏层清 runOnce(idle),结果只驻屏内不跨屏(与试抓弹窗同语义)。
 */
export function RunOnceResultDialog({
  outcome,
  onDismiss,
}: {
  outcome: RunOnceOutcome;
  onDismiss: () => void;
}) {
  return (
    <Dialog
      open
      onOpenChange={(open) => {
        if (!open) onDismiss();
      }}
    >
      <DialogContent className="max-w-md" data-testid="run-once-dialog">
        <DialogHeader>
          <DialogTitle className="flex items-center gap-2">
            <span className="truncate">跑一次结果 · {outcome.name}</span>
            <Badge variant={outcomeVariant(outcome)} data-testid="run-once-status">
              {outcomeText(outcome)}
            </Badge>
          </DialogTitle>
          <DialogDescription>
            {outcome.phase === "error"
              ? "发起失败,可重试;忙碌解除后按钮回可用。"
              : "手动触发的品类采集已结束;实时输出与逐条明细见采集日志。"}
          </DialogDescription>
        </DialogHeader>
        {/* 正文:error 形发起错误原文;done 形 trace 值收 mono 技术小字
            (活性条行话判例的弹窗侧收口) */}
        <div className="flex flex-col gap-1.5">
          {outcome.phase === "error" ? (
            <p className="break-all text-sm text-destructive">发起失败:{outcome.message}</p>
          ) : (
            <p className="break-all font-mono text-2xs text-muted-foreground">
              status={outcome.status ?? "—"} · run_id={outcome.runId}
              {outcome.exitCode !== null ? ` · exit ${outcome.exitCode}` : ""}
            </p>
          )}
        </div>
        <DialogFooter>
          <a
            href="#/logs"
            title="到采集日志屏跟踪该次运行实时输出"
            className="mr-auto inline-flex items-center gap-1.5 text-sm font-medium text-link transition-colors duration-(--duration-fast) hover:text-foreground"
          >
            查看采集日志
          </a>
          {/* 关闭走基件自带 X 钮(aria-label=关闭),不另设底部按钮(与屏内
              job 编辑/急停弹窗一致) */}
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
}
