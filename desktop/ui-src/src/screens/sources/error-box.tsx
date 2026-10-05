import { AlertTriangle, Cpu, RefreshCw } from "lucide-react";

import { Button } from "@/components/ui/button";
import type { SidecarRequestError } from "@/lib/api";

interface ErrorBoxProps {
  error: SidecarRequestError;
  /** 重试动作(缺省不显示按钮) */
  onRetry?: () => void;
  /** 是否正在重试 */
  retrying?: boolean;
}

/**
 * 结构化错误态:sidecar 协议错误必有 code/path/message(SidecarRequestError),
 * 全量如实展示 —— 不吞不掩饰;「协议缺口」类(method_not_found)附一句指向。
 */
export function ErrorBox({ error, onRetry, retrying = false }: ErrorBoxProps) {
  if (error.code === "pyenv_not_ready") {
    return (
      <div
        role="alert"
        data-testid="error-box-pyenv-gate"
        className="mx-6 rounded-md border border-warning/40 bg-warning/[0.06] px-4 py-3 text-sm"
      >
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
    );
  }
  return (
    <div
      role="alert"
      className="mx-6 rounded-md border border-destructive/30 bg-destructive/10 px-4 py-3 text-sm"
    >
      <div className="flex items-start justify-between gap-3">
        <div className="flex flex-col gap-1">
          <p className="flex items-center gap-1.5 font-medium text-destructive">
            <AlertTriangle className="size-4" />
            请求失败:{error.message}
          </p>
          <p className="font-mono text-xs text-muted-foreground">
            code={error.code} path={error.path}
          </p>
          {error.code === "method_not_found" ? (
            <p className="text-xs text-muted-foreground">
              sidecar 协议尚无此方法(entry.py 方法集待扩展);界面功能不可用属协议缺口,不是数据问题。
            </p>
          ) : null}
        </div>
        {onRetry ? (
          <Button variant="outline" size="sm" onClick={onRetry} disabled={retrying}>
            <RefreshCw className={retrying ? "size-3.5 animate-spin" : "size-3.5"} />
            重试
          </Button>
        ) : null}
      </div>
    </div>
  );
}
