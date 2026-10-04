import { useId, type ReactNode } from "react";

import { Input } from "@/components/ui/input";
import { cn } from "@/lib/utils";

interface FieldInputProps extends React.ComponentProps<typeof Input> {
  /** 字段标签(中文;同时作为无障碍名) */
  label: string;
  /** 一行说明(引用规则/去向) */
  hint?: ReactNode;
  /** 校验错误(前端同口径校验,先挡一道) */
  error?: string | null;
}

/**
 * 表单字段(本屏私有;标签/hint/error 包装 + 共享 ui/input 基件)。
 * R2 刀4:内核转接共享 Input(带 data-slot=input)—— 与 SelectTrigger 同享
 * 基调层「微填充 + 低可见描边」的 Linear 输入质感;原先裸 input 吃不到
 * 该层,同屏出现两种输入质感(毒评④「控件像草稿」)。
 * 密钥类字段由调用方传 type="password" + autoComplete="new-password"。
 */
export function FieldInput({ label, hint, error, className, ...props }: FieldInputProps) {
  const id = useId();
  const errorId = `${id}-error`;
  return (
    <div className="flex min-w-0 flex-col gap-1">
      <label htmlFor={id} className="text-xs text-muted-foreground">
        {label}
      </label>
      <Input
        id={id}
        aria-invalid={error ? true : undefined}
        aria-describedby={error ? errorId : undefined}
        className={cn(error && "border-destructive/50", className)}
        {...props}
      />
      {error ? (
        <p id={errorId} className="text-2xs text-destructive">
          {error}
        </p>
      ) : hint ? (
        <p className="text-2xs text-muted-foreground">{hint}</p>
      ) : null}
    </div>
  );
}
