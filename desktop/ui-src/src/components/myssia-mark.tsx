import { cn } from "@/lib/utils";

/**
 * 世事品牌标(eye+universe)。事实源:desktop/branding/myssia-icon.svg
 * (本文件是 public/myssia-icon.svg 的原样拷贝,构建时随产物分发)。
 */
export function MyssiaMark({ className }: { className?: string }) {
  return (
    <img
      src="/myssia-icon.svg"
      alt="世事"
      draggable={false}
      className={cn("size-8 select-none", className)}
    />
  );
}
