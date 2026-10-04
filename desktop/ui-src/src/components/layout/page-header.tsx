import * as React from "react";

interface PageHeaderProps {
  title: string;
  description?: React.ReactNode;
  actions?: React.ReactNode;
}

/** 七屏共用页头:页标题 + 一行中文说明(右侧动作位)。
 *  语义对位 Kestra KsTopNavBar(标题/描述/右侧动作三件套;[来源 Apache-2.0]
 *  kestra/ui/packages/design-system/.../KsTopNavBar/KsTopNavBar.vue,借结构
 *  改语义):Kestra 的 60px 边线顶栏由本仓 TopBar 承担(不在本任务白名单),
 *  此处为内容流内页头——标题间垂直 gap 对齐 --ks-spacing-1(4px=gap-1),
 *  横向 px-6 = --ks-spacing-5(24px,与 Kestra 顶栏 px16/宽屏 px24 同档);
 *  描述 12px(--ks-font-size-sm)弱色。
 *  R2 刀3 层级令牌:标题 text-2xl(20px/600/紧字距)与卡标题/正文/辅文
 *  拉开级差;顶留白 pt-8(32px):顶栏下沿→页标题的呼吸(R2 轮评定档)。 */
export function PageHeader({ title, description, actions }: PageHeaderProps) {
  return (
    <div className="flex items-start justify-between gap-4 px-6 pt-8 pb-1">
      <div className="flex flex-col gap-1">
        {/* 字距走 --text-2xl--letter-spacing(-0.011em),不加 tracking-tight
            (其 -0.025em 对中文标题过紧,且会盖掉令牌) */}
        <h1 className="text-2xl font-semibold text-foreground">{title}</h1>
        {description ? <p className="text-xs text-muted-foreground">{description}</p> : null}
      </div>
      {actions ? <div className="flex items-center gap-2">{actions}</div> : null}
    </div>
  );
}
