import { CircleHelp } from "lucide-react";
import type { ReactNode } from "react";

import { Tooltip, TooltipContent, TooltipTrigger } from "@/components/ui/tooltip";

/**
 * 高困惑字段的问号提示(10-05-ui-chore-batch ①,池档 v12-backlog 第 8 项
 * tooltip 翻案;10-05-dashboard-glance 自 settings/ 上提 src/components/
 * 共享——ui/tooltip 基件本体不碰,上提的是业务消费入口组件,行为零变化),
 * 提示文案人话零行话。
 *
 * 两个导出的分工(a11y 关键):`HintButton` 只渲染问号按钮,必须放在
 * `<label>` 元素**外**作兄弟节点——button 是 labelable element,嵌进
 * label 会让同一个 label 同时标注输入框和按钮(getByLabelText 双匹配、
 * 点击 label 焦点行为含糊);`LabelHint` 用于无 label 语义的纯展示位
 * (如 SettingRow 的标题槽),文本与问号一体。
 * 图标按钮可聚焦(:focus-visible 同样触发 tooltip),aria-describedby 由
 * 基件接通——a11y 契约与 ui-base.test.tsx 基件自测同口径。
 */

export function HintButton({ name, tip }: { name: string; tip: string }) {
  return (
    <Tooltip>
      <TooltipTrigger
        aria-label={`${name}说明`}
        className="inline-flex shrink-0 items-center rounded-sm text-muted-foreground/70 transition-colors duration-(--duration-fast) hover:text-muted-foreground"
      >
        <CircleHelp className="size-3.5" aria-hidden="true" />
      </TooltipTrigger>
      <TooltipContent side="top">{tip}</TooltipContent>
    </Tooltip>
  );
}

export function LabelHint({ label, tip }: { label: ReactNode; tip: string }) {
  return (
    <span className="inline-flex items-center gap-1">
      {label}
      <HintButton name={typeof label === "string" ? label : "字段"} tip={tip} />
    </span>
  );
}
