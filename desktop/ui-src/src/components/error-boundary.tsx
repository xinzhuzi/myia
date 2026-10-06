// 根级 React ErrorBoundary(10-07-unified-logging 批2;AC10/design §6):
// 渲染崩溃留痕 + 极简回退。didCatch 经(劫持后的)console.error 落
// shell.log——log.ts 先于渲染链安装(main.tsx 接线序),此处只需打 console。
// 回退 UI 极简(决议⑥:错误文本 + 重新加载钮,无花活;审美裁决留主人,
// 装机截图入 evidence)。UI 错误不进日志屏(决议④)。
import { Component, type ErrorInfo, type ReactNode } from "react";

interface ErrorBoundaryProps {
  children: ReactNode;
}

interface ErrorBoundaryState {
  error: Error | null;
}

export class ErrorBoundary extends Component<ErrorBoundaryProps, ErrorBoundaryState> {
  state: ErrorBoundaryState = { error: null };

  static getDerivedStateFromError(error: Error): ErrorBoundaryState {
    return { error };
  }

  componentDidCatch(error: Error, info: ErrorInfo): void {
    // 崩溃组件 + 错误 + 堆栈首行(componentStack 首行是崩溃位)
    const firstFrame = info.componentStack?.split("\n").find((line) => line.trim() !== "");
    console.error(
      `errorboundary: 渲染崩溃: ${error.message}`,
      firstFrame?.trim() ?? "",
    );
  }

  render(): ReactNode {
    if (this.state.error) {
      return (
        <div
          className="flex min-h-screen flex-col items-center justify-center gap-4 p-8 text-center"
          data-testid="error-boundary"
        >
          <p className="max-w-xl font-mono text-sm whitespace-pre-wrap text-destructive">
            {`界面渲染出错:${this.state.error.message}`}
          </p>
          <button
            type="button"
            className="rounded-md border border-border px-4 py-2 text-sm hover:bg-muted"
            onClick={() => window.location.reload()}
            data-testid="error-boundary-reload"
          >
            重新加载
          </button>
        </div>
      );
    }
    return this.props.children;
  }
}
