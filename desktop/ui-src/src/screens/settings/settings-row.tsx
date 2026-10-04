import type { ReactNode } from "react";

import { cn } from "@/lib/utils";

interface SettingRowProps {
  /** 行标题( Kestra SettingRow__label:600 字重) */
  label: ReactNode;
  /** 行说明(Kestra SettingRow__description:small 次级色);FieldInput 的 hint 同位 */
  description?: ReactNode;
  /** 右侧控件位(Kestra SettingRow__control:flex-shrink 0 + 右对齐) */
  children: ReactNode;
  /** 说明位错误文案(红,与 hint 同槽互斥呈现) */
  error?: ReactNode;
  className?: string;
}

/**
 * 设置行(10-04-ui-kestra-anchor):结构借自 Apache-2.0
 * kestra/ui/src/components/settings/components/block/SettingRow.vue
 * (label+description 左 / control 右,窄屏纵叠),借结构改语义——
 * 控件宽 256px(w-64)= Kestra 控件族同带;行距 py-3 对齐其
 * --ks-spacing-4(16px)上下内边距节奏。分隔线由父容器 divide-y 提供
 * (Kestra 行间 border-bottom default 同款)。
 */
export function SettingRow({ label, description, error, children, className }: SettingRowProps) {
  return (
    <div className={cn("flex flex-col gap-2 py-3 sm:flex-row sm:items-center sm:justify-between sm:gap-4", className)}>
      <div className="flex min-w-0 flex-col gap-0.5">
        <span className="text-left text-sm font-semibold text-foreground">{label}</span>
        {description ? <p className="text-left text-2xs leading-4 text-muted-foreground">{description}</p> : null}
        {error ? <p className="text-left text-2xs leading-4 text-destructive">{error}</p> : null}
      </div>
      <div className="flex w-full shrink-0 flex-wrap items-center gap-2 sm:w-64 sm:justify-end">{children}</div>
    </div>
  );
}
