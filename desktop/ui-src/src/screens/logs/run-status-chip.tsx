import { CircleCheck, CirclePlay, CircleStop, CircleX, TriangleAlert } from "lucide-react";

import type { RunFilterStatus, RunRowModel } from "./api";

/**
 * L1/L2 共用状态件(10-12-logs-two-level-ui §5:现状 logs-screen.tsx 代码平移,
 * 词面/语义/视觉零改)。Kestra KsExecutionStatus 解剖沿袭(d4 重锚先例):
 * 图标 + 文案 + 状态色淡底描边芯片。
 */

/** 状态过滤键 → 过滤选项文案(与 runBadge 同词表) */
export const STATUS_FILTER_OPTIONS: Array<{ value: RunFilterStatus; label: string }> = [
  { value: "running", label: "运行中" },
  { value: "success", label: "成功" },
  { value: "partial", label: "部分" },
  { value: "config_error", label: "配置" },
  { value: "failed", label: "失败" },
  { value: "cancelled", label: "已取消" },
];

export interface RunBadgeModel {
  variant: "default" | "ok" | "warning" | "destructive" | "unknown";
  label: string;
  icon: typeof CircleCheck;
}

/** run 状态 → 状态芯片模型(Kestra KsExecutionStatus 解剖:图标+文案+状态色;
 * 退出码语义 0/1/2/3 + cancelled,见 types.ts RunExitStatus) */
export function runBadge(status: RunRowModel["status"], state: RunRowModel["state"]): RunBadgeModel {
  if (state === "running" || status === null) {
    return { variant: "default", label: "运行中", icon: CirclePlay };
  }
  switch (status) {
    case "success":
      return { variant: "ok", label: "成功", icon: CircleCheck };
    case "partial":
      return { variant: "warning", label: "部分", icon: TriangleAlert };
    case "config_error":
      return { variant: "warning", label: "配置", icon: TriangleAlert };
    case "failed":
      return { variant: "destructive", label: "失败", icon: CircleX };
    case "cancelled":
      // run.cancel 信号终局(C2,v1.1.2 桌面对齐批)
      return { variant: "unknown", label: "已取消", icon: CircleStop };
  }
}

/** 状态芯片(Kestra KsExecutionStatus small 档:高 24px/字 xs 12px/圆角 6px/
 * 状态色文字+淡底+描边圆图标;色比沿用 Badge 四态实算档,WCAG 不降级) */
const STATUS_CHIP_TONE: Record<string, string> = {
  default: "border-primary/25 bg-primary/15 text-primary",
  ok: "border-ok/30 bg-ok/15 text-ok",
  warning: "border-warning/30 bg-warning/15 text-warning",
  destructive: "border-destructive/30 bg-destructive/15 text-[#ff6b70]",
  unknown: "border-unknown/30 bg-unknown/10 text-unknown",
};

export function StatusChip({ badge, testId }: { badge: RunBadgeModel; testId?: string }) {
  const Icon = badge.icon;
  return (
    <span
      data-testid={testId}
      className={`inline-flex h-6 shrink-0 items-center gap-1 rounded-[6px] border px-2 text-xs font-medium tabular-nums ${STATUS_CHIP_TONE[badge.variant]}`}
    >
      <Icon aria-hidden className="size-3.5" />
      {badge.label}
    </span>
  );
}
