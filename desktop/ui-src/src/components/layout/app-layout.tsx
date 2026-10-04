import { Outlet } from "react-router-dom";

import { Sidebar } from "@/components/layout/sidebar";

/**
 * 应用骨架(主人 2026-10-04「无头」指令,ZCode 范式):左侧导航侧栏通到顶,
 * 主内容区**直接就是内容**——无顶栏、无 PageHeader、无标题行。
 * 滚动只发生在内容区,侧栏常驻。
 */
export function AppLayout() {
  return (
    <div className="flex h-full overflow-hidden bg-background text-foreground">
      <Sidebar />
      <main className="relative z-10 min-w-0 flex-1 overflow-y-auto">
        <Outlet />
      </main>
    </div>
  );
}
