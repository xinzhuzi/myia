import { AlertTriangle, Cpu } from "lucide-react";

import { Button } from "@/components/ui/button";
import type { SidecarRequestError } from "@/lib/api";

interface ErrorBoxProps {
  error: SidecarRequestError;
  /** 重试动作(缺省不显示按钮) */
  onRetry?: () => void;
  retrying?: boolean;
}

/**
 * 结构化错误态:sidecar 协议错误必有 code/path/message,全量如实展示。
 *
 * pyenv_not_ready 变体(10-05 D2/AC2 收尾):环境未就绪不是「重试可救」的
 * 传输错误——改渲染人话引导(状态语 + 深链设置 python-env 分区),不显
 * code 行与重试钮(重试对环境配置无意义,入口在设置页)。
 */
export function ErrorBox({ error, onRetry, retrying = false }: ErrorBoxProps) {
  if (error.code === "pyenv_not_ready") {
    return (
      <div
        role="alert"
        data-testid="error-box-pyenv-gate"
        className="rounded-md border border-warning/40 bg-warning/[0.06] px-4 py-3 text-sm"
      >
        <div className="flex flex-col gap-1">
          <p className="flex items-center gap-1.5 font-medium text-warning">
            <Cpu className="size-4 shrink-0" />
            {error.message}
          </p>
          <a
            href="#/settings?section=python-env"
            className="text-xs text-primary underline underline-offset-2 hover:text-primary/80"
          >
            前往设置 →「Python 环境」完成配置(就绪后本功能自动恢复)
          </a>
        </div>
      </div>
    );
  }

  return (
    <div
      role="alert"
      className="rounded-md border border-destructive/30 bg-destructive/10 px-4 py-3 text-sm"
    >
      <div className="flex items-start justify-between gap-3">
        <div className="flex flex-col gap-1">
          <p className="flex items-center gap-1.5 font-medium text-destructive">
            <AlertTriangle className="size-4" />
            {error.message}
          </p>
          <p className="font-mono text-xs text-muted-foreground">
            code={error.code} path={error.path}
          </p>
        </div>
        {onRetry ? (
          <Button variant="outline" size="sm" onClick={onRetry} disabled={retrying}>
            重试
          </Button>
        ) : null}
      </div>
    </div>
  );
}
