import { useId, type ReactNode } from "react";

import { Input } from "@/components/ui/input";
import { cn } from "@/lib/utils";

import { SettingRow } from "./settings-row";

interface FieldInputProps extends React.ComponentProps<typeof Input> {
  /** 字段标签(中文;同时作为无障碍名) */
  label: string;
  /** 一行说明(引用规则/去向;SettingRow 的 description 位) */
  hint?: ReactNode;
  /** 校验错误(前端同口径校验,先挡一道) */
  error?: string | null;
  /** 控件右缘追加位(徽标/动作钮;如云端 key 的「已入钥匙链」徽标) */
  action?: ReactNode;
}

/**
 * 表单字段(本屏私有):10-04-ui-kestra-anchor 起改 Kestra SettingRow
 * 横排范式(结构借自 Apache-2.0 kestra settings/components/block/
 * SettingRow.vue,借结构改语义)——label+hint/error 左、输入控件右
 * (w-64 控件族);内核仍是共享 ui/input 基件(微填充+低可见描边)。
 * 密钥类字段由调用方传 type="password" + autoComplete="new-password"。
 */
export function FieldInput({ label, hint, error, action, className, ...props }: FieldInputProps) {
  const id = useId();
  const errorId = `${id}-error`;
  return (
    <SettingRow
      label={<label htmlFor={id}>{label}</label>}
      description={hint}
      error={error ? <span id={errorId}>{error}</span> : null}
    >
      <Input
        id={id}
        aria-label={props["aria-label"] ?? label}
        aria-invalid={error ? true : undefined}
        aria-describedby={error ? errorId : undefined}
        className={cn("min-w-0 flex-1", error && "border-destructive/50", className)}
        {...props}
      />
      {action}
    </SettingRow>
  );
}
