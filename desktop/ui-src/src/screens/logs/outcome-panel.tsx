import { useEffect, useMemo, useState } from "react";

import { deriveOutcome, formatRelative, loadOutcomePreviews } from "./api";
import type { OutcomePreviewItem } from "./api";
import { domIdOf } from "./api";
import type { RunRowModel } from "./api";

/**
 * L2 采集成果区(10-12-run-detail-outcome):「本轮采集到了什么」的答案位,
 * 与失败原因区(FailurePanel,「为什么失败」)对偶,常驻固定不随日志体滚走。
 * 数据双源零新协议:① record.stats(run.status 行随身)→ 保留 N 条 / 每源
 * 采集数·引擎·耗时·跳过原因 / 推送概要;② store.items?since=started_at
 * 惰性拉条目标题预览,客户端按 first_seen ≤ finished_at 截窗(后继轮不混入)。
 * 渲染门槛在 deriveOutcome:running / 无记录 / 空 stats 一行不渲染。
 * 布局帽:面板 shrink-0(塌缩律 67546cd——外层 flex-col 直接子项);
 * 源行与预览各自 max-h 内滚,内滚容器直接子项显式 shrink-0 同律。
 */
export function OutcomePanel({
  run,
  startedAt,
  finishedAt,
}: {
  run: RunRowModel;
  startedAt: string | null | undefined;
  finishedAt: string | null | undefined;
}) {
  const domId = domIdOf(run);
  const outcome = useMemo(() => deriveOutcome(run), [run]);
  const [preview, setPreview] = useState<OutcomePreviewItem[] | null>(null);
  const [previewError, setPreviewError] = useState(false);

  // 条目预览惰性拉(切 run 即换靶;取消旗防错写;finishedAt 到位重截一拍)
  useEffect(() => {
    if (outcome === null || startedAt == null) return;
    let cancelled = false;
    setPreview(null);
    setPreviewError(false);
    loadOutcomePreviews(run.category, startedAt)
      .then((items) => {
        if (cancelled) return;
        setPreview(items.filter((item) => finishedAt == null || item.firstSeen <= finishedAt));
      })
      .catch(() => {
        if (!cancelled) setPreviewError(true);
      });
    return () => {
      cancelled = true;
    };
    // eslint-disable-next-line react-hooks/exhaustive-deps -- startedAt/finishedAt 变化只影响截窗,run.rowKey 才是拉取靶
  }, [run.rowKey, run.category, startedAt, outcome === null, finishedAt]);

  if (outcome === null) return null;
  const shownPreview = preview?.slice(0, 8) ?? [];
  return (
    <section className="shrink-0 px-5 pt-3" aria-label="采集成果">
      <div
        data-testid={`run-outcome-${domId}`}
        className="flex flex-col gap-2 rounded-lg border border-border/60 bg-muted/20 p-3"
      >
        {/* 头行:成果总量 + 入库失败 + 推送概要 */}
        <div className="flex shrink-0 flex-wrap items-center gap-x-3 gap-y-1">
          <span className="text-xs font-semibold text-foreground">采集成果</span>
          {outcome.retained !== null ? (
            <span data-testid={`run-outcome-retained-${domId}`} className="text-xs text-foreground">
              保留 <span className="font-mono font-medium">{outcome.retained}</span> 条
            </span>
          ) : null}
          {outcome.itemFailures !== null && outcome.itemFailures > 0 ? (
            <span className="text-2xs text-warning/85">{outcome.itemFailures} 条入库失败</span>
          ) : null}
          {outcome.retained === 0 && outcome.sources.every((source) => !source.failed) ? (
            <span className="text-2xs text-muted-foreground">本轮无新入库条目(去重后全旧或零采集)</span>
          ) : null}
          {outcome.pushes.map((push) => (
            <span
              key={push.channel}
              className="text-2xs text-muted-foreground"
              title={`推送渠道 ${push.channel}`}
            >
              推送 {push.channel}
              {push.ok === null ? "" : push.ok ? " ✓" : " ✗"}
              {push.immediate > 0 ? ` · 直发 ${push.immediate}` : ""}
              {push.digest > 0 ? ` · 日报 ${push.digest}` : ""}
              {push.archive > 0 ? ` · 归档 ${push.archive}` : ""}
            </span>
          ))}
        </div>
        {/* 每源成果行:源 · 引擎 · N 条 · 耗时 ·(跳过原因 | 失败如实) */}
        {outcome.sources.length > 0 ? (
          <div
            data-testid={`run-outcome-sources-${domId}`}
            className="flex max-h-36 flex-col gap-1 overflow-y-auto"
          >
            {outcome.sources.map((source, index) => (
              <p
                key={`${source.name}-${index}`}
                className={`shrink-0 truncate text-2xs font-mono ${source.failed ? "text-dead" : source.skipped ? "text-muted-foreground" : "text-foreground/90"}`}
                title={`${source.name} · ${source.engine}${source.skipReason ? ` · ${source.skipReason}` : ""}`}
              >
                {source.name} · {source.engine} · {source.itemCount} 条
                {source.durationText !== null ? ` · ${source.durationText}` : ""}
                {source.skipped ? (source.skipReason !== null ? ` · 跳过(${source.skipReason})` : " · 跳过") : ""}
                {source.failed ? " · 失败" : ""}
              </p>
            ))}
          </div>
        ) : null}
        {/* 条目标题预览(本轮新入库,前 8 条;全量在情报流) */}
        {previewError ? (
          <p className="shrink-0 text-2xs text-muted-foreground">
            <span className="mr-1 text-brand-from">▍</span>条目预览拉取失败(store.items 不可达)
          </p>
        ) : preview !== null && preview.length > 0 ? (
          <div
            data-testid={`run-outcome-preview-${domId}`}
            className="flex max-h-44 flex-col gap-1 overflow-y-auto border-t border-border/60 pt-2"
          >
            {shownPreview.map((item) => (
              <p key={item.key} className="shrink-0 truncate text-2xs text-foreground/85" title={item.title}>
                <span className="mr-1 text-muted-foreground/60">·</span>
                {item.title || "(无标题)"}
                <span className="ml-1.5 text-muted-foreground/70">{formatRelative(item.firstSeen)}</span>
              </p>
            ))}
            {preview.length > shownPreview.length ? (
              <p className="shrink-0 text-2xs text-muted-foreground">
                另 {preview.length - shownPreview.length} 条本轮新入库(情报流可看全)
              </p>
            ) : null}
          </div>
        ) : preview !== null && preview.length === 0 && outcome.retained !== 0 ? (
          <p className="shrink-0 text-2xs text-muted-foreground">
            <span className="mr-1 text-brand-from">▍</span>本轮新入库条目不在预览窗内(保留的 {outcome.retained} 条为旧行去重命中)
          </p>
        ) : null}
      </div>
    </section>
  );
}
