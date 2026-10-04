import { useCallback, useState } from "react";
import { Outlet } from "react-router-dom";

import { Sidebar } from "@/components/layout/sidebar";
import { TopBar } from "@/components/layout/top-bar";

/**
 * 应用骨架:左侧导航(七屏,Kestra SideBar 模式:分组可折叠 + 底部
 * sidecar 状态区;结构对位 kestra/ui/src/components/layout/OnlyLeftMenu
 * Layout.vue [Apache-2.0,借结构改语义])+ 顶栏(极简形态:仅屏标题 +
 * ⌘K 命令面板图标触发器;承担 Kestra KsTopNavBar 的 60px 边线顶栏角色)
 * + 内容区。暗色单主题(Kestra ks-theme-dark 基调);滚动只发生在内容区,
 * 侧栏/顶栏常驻。
 *
 * 品类全局态(C8,10-03-feed-ux):选中值提升到本层(不引状态库,
 * Outlet context 即 router 原生的 prop drilling 通道)→ 情报流屏服务端
 * category 过滤;「全部品类」= null(不传参)。顶栏品类下拉已拆(壳层
 * 清理,后续 feed/sources 屏自放上下文版),当前唯一写入方是命令面板
 * 的「切换品类」命令(TopBar 透传 onCategoryChange)。
 */
export interface CategoryFilterContext {
  /** 顶栏选中的品类;null = 全部品类 */
  category: string | null;
}

export function AppLayout() {
  const [category, setCategory] = useState<string | null>(null);
  const handleCategoryChange = useCallback((next: string | null) => setCategory(next), []);
  return (
    <div className="flex h-full overflow-hidden bg-background text-foreground">
      <Sidebar />
      <div className="flex min-w-0 flex-1 flex-col">
        <TopBar category={category} onCategoryChange={handleCategoryChange} />
        {/* R2 刀1 呼吸感:内容列 1200px 收束(max-w-content/--content-max),
            超宽屏不摊满;main 仍为唯一滚动容器,屏根保持 main 直接子,
            index.css 基调层的区块 gap 升档选择器依赖此结构 */}
        <main className="mx-auto min-h-0 w-full max-w-content flex-1 overflow-y-auto">
          <Outlet context={{ category } satisfies CategoryFilterContext} />
        </main>
      </div>
    </div>
  );
}
