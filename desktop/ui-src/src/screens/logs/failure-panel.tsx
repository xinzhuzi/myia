import type { FailureModel } from "./api";
import { StatusChip } from "./run-status-chip";
import type { RunBadgeModel } from "./run-status-chip";

/**
 * L2 失败原因区(10-12-logs-two-level-ui §3.2):「为什么失败」的答案位,
 * 常驻固定不随日志体滚走、不埋进 4000 行里。三证据源由 synthesizeFailure
 * 合成(exit_code 语义词 / error 字段原文 / stderr 错误行摘);渲染门槛
 * (PRD AC2「成功轮不显示」)在合成器把关,success/running 到不了这里。
 * 无据可查(PRD「如实无据就说无据」):三源全空 → 状态芯片语义 + 一句
 * 如实文案,不编造、不静默。
 * 布局帽:面板 max-h-40 shrink-0 overflow-y-auto;内滚容器直接子项显式
 * shrink-0(塌缩律 67546cd 同门,design §7)。
 */

export function FailurePanel({
  domId,
  badge,
  failure,
}: {
  domId: string;
  badge: RunBadgeModel;
  failure: FailureModel;
}) {
  // 无据判据(design §3.2):error 字段空 + 错误行摘空 + tail 非在途。
  // tail 在途(tailPending)时不判无据——答案还在路上;旧行无对齐号
  // (logAligned=false)直接走无据分支,「在途」对它是永假态不挂等待
  const noEvidence = failure.errorText === null && failure.errorRows.length === 0 && !failure.tailPending;
  return (
    <div className="shrink-0 px-5 pt-3">
      <div
        data-testid={`run-failure-${domId}`}
        className="flex max-h-40 flex-col gap-1.5 overflow-y-auto rounded-lg border border-border/60 bg-muted/20 p-3"
      >
        <div className="flex shrink-0 flex-wrap items-center gap-2">
          <StatusChip badge={badge} />
          {failure.exitCode !== null ? (
            <span className="inline-flex h-6 shrink-0 items-center rounded-[6px] border border-destructive/30 bg-destructive/15 px-2 font-mono text-xs font-medium text-[#ff6b70]">
              exit={failure.exitCode}
              {failure.exitLabel !== null ? ` · ${failure.exitLabel}` : ""}
            </span>
          ) : (
            /* exit=—(历史行 wire 真形:entry.py _history_run_rows 恒 None):
               如实报缺号,不编 0/1/2/3 语义 */
            <span
              className="shrink-0 font-mono text-xs text-muted-foreground"
              title="该轮未落 exit_code(上一程历史行 wire 真形)"
            >
              exit=—
            </span>
          )}
        </div>
        {failure.errorText !== null ? (
          <p className="shrink-0 break-words text-xs text-foreground/90" title={failure.errorText}>
            {failure.errorText}
          </p>
        ) : null}
        {failure.tailPending ? (
          <p className="shrink-0 text-2xs text-muted-foreground">
            <span className="mr-1 text-brand-from">▍</span>日志拉取中…(stderr 错误行摘待 tail 到位)
          </p>
        ) : null}
        {failure.errorRows.map((row, index) => (
          <p
            key={row.key}
            data-testid={`run-failure-line-${domId}-${index}`}
            className="shrink-0 truncate font-mono text-2xs text-dead"
            title={row.text}
          >
            {row.text}
          </p>
        ))}
        {failure.errorRowsTotal > failure.errorRows.length ? (
          <p className="shrink-0 text-2xs text-muted-foreground">
            另 {failure.errorRowsTotal - failure.errorRows.length} 条错误行在下方日志体(高亮)
          </p>
        ) : null}
        {noEvidence ? (
          <p data-testid={`run-failure-none-${domId}`} className="shrink-0 text-2xs text-muted-foreground">
            暂无结构化失败记录(该轮未落 error 字段,日志缓冲中亦无错误行)
          </p>
        ) : null}
      </div>
    </div>
  );
}
