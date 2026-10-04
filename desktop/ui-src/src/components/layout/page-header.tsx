import * as React from "react";

interface PageHeaderProps {
  title: string;
  description?: React.ReactNode;
  actions?: React.ReactNode;
}

/** 七屏共用页头:页标题 + 一行中文说明(右侧动作位)。
 *  R2 刀3 层级令牌:标题升 text-2xl(20px/600/紧字距,--text-2xl 阶梯档),
 *  与卡标题(13 semibold)/正文(13~14)/辅文(12~11)拉开级差;
 *  顶留白 pt-8(32px):顶栏下沿→页标题的呼吸(VL R2 轮评:24px 仍显压迫,
 *  Linear 顶栏→内容首行 ~32px)。 */
export function PageHeader({ title, description, actions }: PageHeaderProps) {
  return (
    <div className="flex items-start justify-between gap-4 px-6 pt-8 pb-1">
      <div className="flex flex-col gap-1.5">
        {/* 字距走 --text-2xl--letter-spacing(-0.011em),不加 tracking-tight
            (其 -0.025em 对中文标题过紧,且会盖掉令牌) */}
        <h1 className="text-2xl font-semibold text-foreground">{title}</h1>
        {description ? <p className="text-xs text-muted-foreground">{description}</p> : null}
      </div>
      {actions ? <div className="flex items-center gap-2">{actions}</div> : null}
    </div>
  );
}
