import { ScrollText, X } from "lucide-react";
import { useCallback, useEffect, useRef } from "react";
import type { ReactNode } from "react";

import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";

import type { TestOutcomeView } from "./api";

interface TestResultDialogProps {
  /** 试抓结果视图(buildTestOutcome 产出 / 发起失败 catch 构造 launch_error 形) */
  outcome: TestOutcomeView;
  /** 关闭弹窗(只读无 dirty 守卫,直接关) */
  onClose: () => void;
}

/**
 * 试抓结果详情弹窗(10-05-test-result-dialog):撤源管理屏顶常驻横幅,详情类
 * 信息进模态(主人判词「这种提示做详情弹窗,而不是放到界面最上面展示」)。
 * 完成即弹:试抓由用户行内发起,等结果是其直接意图,少一次点击(Kestra
 * Trigger→Execution 详情同向,任务档 design 权衡记录)。
 *
 * 零新 npm 依赖(R5):手写 overlay 范式抄本屏在用的 YamlEditorDialog
 * (yaml-editor-dialog.tsx:84-118)—— fixed 遮罩 + 居中面板 role=dialog
 * aria-modal;ESC / 遮罩点击 / 关闭钮三径同关(只读无 dirty 守卫);面板挂载
 * 即聚焦(ESC 免先点进);event.defaultPrevented 的键事件不关(缺陷 2 判例)。
 * 样式全 token(spec frontend-ui 第 1 条),结构化明细吃满 test.completed
 * 既有报文(R2):概要 / 指纹判定 / 引擎退化链 / 条目预览(dedup_key+字段,
 * 截断如实标)/ 失败明细,协议零改动。
 */
export function TestResultDialog({ outcome, onClose }: TestResultDialogProps) {
  const panelRef = useRef<HTMLDivElement>(null);

  // 只读弹窗无 dirty 守卫:三径(ESC/遮罩/X)都直接关
  const attemptClose = useCallback(() => {
    onClose();
  }, [onClose]);

  // 键盘:ESC 关闭;已消费(被 preventDefault)的事件不再关弹窗
  // (YamlEditorDialog 缺陷 2 判例,10-04-yaml-editor-no-scroll)
  useEffect(() => {
    const onKeyDown = (event: KeyboardEvent) => {
      if (event.defaultPrevented) return;
      if (event.key === "Escape") attemptClose();
    };
    window.addEventListener("keydown", onKeyDown);
    return () => window.removeEventListener("keydown", onKeyDown);
  }, [attemptClose]);

  // 模态基础焦点:面板挂载即聚焦(ESC 无需先点进弹窗;轮廓不抢视觉)
  useEffect(() => {
    panelRef.current?.focus();
  }, []);

  // 失败明细行:event_error = error 族 + data.errors 逐条;launch_error =
  // code:message;report 形链耗尽前的整体超时(report.error)也入此节
  const failureLines: string[] = [];
  if (outcome.kind === "event_error") {
    failureLines.push(`试抓失败(${outcome.error ?? "error"})`);
    for (const entry of outcome.errors ?? []) {
      failureLines.push(`${entry.path}:${entry.message}`);
    }
  } else if (outcome.kind === "launch_error") {
    failureLines.push(`发起失败(${outcome.code ?? "error"}):${outcome.message ?? ""}`);
  } else if (outcome.error) {
    failureLines.push(`试抓失败:${outcome.error}`);
  }

  // 引擎命中:链耗尽时 report.engine 缺位,回落配置引擎,再缺位如实「—」
  const engineHit = outcome.engine ?? outcome.engineConfigured ?? "—";

  return (
    <div
      className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 p-6 animate-overlay-in"
      onClick={attemptClose}
      data-testid="test-result-overlay"
    >
      <div
        ref={panelRef}
        role="dialog"
        aria-modal="true"
        aria-label={`试抓结果 ${outcome.sourceName}`}
        tabIndex={-1}
        data-testid="test-result-dialog"
        className="flex max-h-[80vh] w-[min(760px,88vw)] flex-col rounded-lg border border-border bg-card shadow-drawer animate-dialog-in outline-none"
        onClick={(event) => event.stopPropagation()}
      >
        {/* 标题区:源名 + 状态徽章(色 + 文字双通道,不只靠颜色)+ X 关闭 */}
        <div className="flex shrink-0 items-center justify-between gap-2 border-b border-border px-4 py-3">
          <div className="flex min-w-0 items-center gap-2">
            <span className="truncate text-base font-semibold text-foreground">
              试抓结果 · {outcome.sourceName}
            </span>
            <Badge variant={outcome.ok ? "ok" : "destructive"} data-testid="test-result-status">
              {outcome.ok ? "成功" : "失败"}
            </Badge>
          </div>
          <Button size="sm" variant="ghost" aria-label="关闭对话框" onClick={attemptClose}>
            <X className="size-4" />
          </Button>
        </div>

        {/* 正文:分节滚动,有则渲染 */}
        <div className="flex min-h-0 flex-1 flex-col gap-4 overflow-y-auto px-4 py-3">
          {/* 1. 概要(kind=report):引擎命中/配置引擎/条数 */}
          {outcome.kind === "report" ? (
            <section className="flex flex-col gap-1.5" aria-label="概要">
              <SectionLabel>概要</SectionLabel>
              <p className="text-sm">
                <span className="text-muted-foreground">引擎命中</span>{" "}
                <span className="font-mono text-foreground">{engineHit}</span>
                {outcome.engineConfigured ? (
                  <>
                    <span className="text-muted-foreground">(配置 </span>
                    <span className="font-mono text-foreground">{outcome.engineConfigured}</span>
                    <span className="text-muted-foreground">)</span>
                  </>
                ) : null}
                <span className="text-muted-foreground"> · 条目 </span>
                <span className="font-semibold text-foreground">{outcome.itemCount ?? 0}</span>
                <span className="text-muted-foreground"> 条</span>
              </p>
            </section>
          ) : null}

          {/* 2. 指纹判定:meaning 全文 + verdict/skip_reason 技术小字 */}
          {outcome.fingerprint ? (
            <section className="flex flex-col gap-1.5" aria-label="指纹判定">
              <SectionLabel>指纹判定</SectionLabel>
              <p className="text-sm text-foreground">{outcome.fingerprint.meaning}</p>
              <p className="font-mono text-2xs text-muted-foreground">
                verdict={outcome.fingerprint.verdict}
                {outcome.fingerprint.skipReason
                  ? ` · skip_reason=${outcome.fingerprint.skipReason}`
                  : ""}
              </p>
            </section>
          ) : null}

          {/* 3. 引擎退化链:逐条 engine [error_type] message */}
          {outcome.failures && outcome.failures.length > 0 ? (
            <section className="flex flex-col gap-1.5" aria-label="引擎退化链">
              <SectionLabel>引擎退化({outcome.failures.length} 次)</SectionLabel>
              <ul className="flex flex-col gap-1">
                {outcome.failures.map((failure, index) => (
                  <li key={`${failure.engine}:${index}`} className="break-all text-xs">
                    <span className="font-mono text-foreground">{failure.engine}</span>{" "}
                    <span className="font-mono text-2xs text-muted-foreground">
                      [{failure.errorType}]
                    </span>{" "}
                    <span className="text-foreground">{failure.message}</span>
                  </li>
                ))}
              </ul>
            </section>
          ) : null}

          {/* 4. 条目预览:逐条 dedup_key(mono 2xs)+ 字段「k = v」行;截断如实标 */}
          {outcome.items && outcome.items.length > 0 ? (
            <section
              className="flex flex-col gap-1.5"
              aria-label="条目预览"
              data-testid="test-result-items"
            >
              <SectionLabel>条目预览</SectionLabel>
              <ul className="flex flex-col gap-2">
                {outcome.items.map((item, index) => (
                  <li
                    key={index}
                    className="flex flex-col gap-0.5 rounded-md border border-border/60 bg-muted/30 px-2.5 py-2"
                  >
                    {item.dedupKey !== null ? (
                      <p
                        className="truncate font-mono text-2xs text-muted-foreground"
                        title={item.dedupKey}
                      >
                        dedup_key: {item.dedupKey}
                      </p>
                    ) : item.dedupKeyError ? (
                      <p className="break-all font-mono text-2xs text-destructive">
                        dedup_key 求值失败: {item.dedupKeyError}
                      </p>
                    ) : (
                      <p className="font-mono text-2xs text-muted-foreground">dedup_key: —</p>
                    )}
                    {Object.entries(item.fields).map(([key, value]) => (
                      <p key={key} className="break-all font-mono text-2xs">
                        <span className="text-muted-foreground">{key} = </span>
                        <span className="text-foreground">{value}</span>
                      </p>
                    ))}
                  </li>
                ))}
              </ul>
              {outcome.itemsTruncated ? (
                <p className="text-2xs text-muted-foreground">
                  仅预览前 {outcome.items.length} 条
                </p>
              ) : null}
            </section>
          ) : null}

          {/* 5. 失败明细:error 族逐条如实呈现,绝不静默 */}
          {failureLines.length > 0 ? (
            <section
              className="flex flex-col gap-1.5 rounded-md border border-destructive/30 bg-destructive/10 px-3 py-2.5"
              aria-label="失败明细"
            >
              <SectionLabel>失败明细</SectionLabel>
              <ul className="flex flex-col gap-1">
                {failureLines.map((line, index) => (
                  <li key={index} className="break-all text-sm text-destructive">
                    {line}
                  </li>
                ))}
              </ul>
            </section>
          ) : null}
        </div>

        {/* 底部动作条:采集日志深链(与跑一次横幅的链接同款样式)+ 关闭 */}
        <div className="flex shrink-0 items-center justify-between gap-2 border-t border-border px-4 py-3">
          <a
            href="#/logs"
            title="到采集日志屏跟踪试抓子进程实时输出"
            className="inline-flex items-center gap-1.5 text-sm font-medium text-link transition-colors duration-(--duration-fast) hover:text-foreground"
          >
            <ScrollText className="size-3.5" />
            查看采集日志
          </a>
          <Button size="sm" variant="outline" onClick={attemptClose}>
            关闭
          </Button>
        </div>
      </div>
    </div>
  );
}

/** 分节小标(2xs 微标签惯例;不占 heading 层级——弹窗可访问名由 aria-label 承担) */
function SectionLabel({ children }: { children: ReactNode }) {
  return <p className="text-2xs font-medium text-muted-foreground">{children}</p>;
}
