import { useState } from "react";
import { Outlet } from "react-router-dom";

import { CommandPalette } from "@/components/layout/command-palette";
import { MigrationBanner } from "@/components/layout/migration-banner";
import { PyenvGateBanner } from "@/components/layout/pyenv-gate-banner";
import { Sidebar } from "@/components/layout/sidebar";

/**
 * 应用骨架(主人 2026-10-04「无头」指令,ZCode 范式):左侧导航侧栏通到顶,
 * 主内容区**直接就是内容**——无顶栏、无 PageHeader、无标题行。
 * 滚动只发生在内容区,侧栏常驻。
 *
 * 内容区顶部两条全局横幅位:PyenvGateBanner(D2 各屏引导空态卡,AC2
 * 收尾——环境未就绪时全局引导进设置,就绪自动隐)+ MigrationBanner
 * (存量迁移一次性引导,10-05 第 6 步 D5:旧数据根首启出现)。
 *
 * ⌘K 命令面板在此直挂(10-05 复活):无头布局整删 TopBar(d9ae353)时面板
 * 唯一渲染点连坐成不可达死 UI——热键与开关监听本就自含在组件内,直挂即活,
 * 零视觉占用,不回顶栏不破无头令(挂载级回归锚在 app-layout.test)。
 */
export function AppLayout() {
  const [paletteOpen, setPaletteOpen] = useState(false);
  return (
    <div className="flex h-full overflow-hidden bg-background text-foreground">
      <Sidebar />
      <main className="relative z-10 min-w-0 flex-1 overflow-y-auto">
        <PyenvGateBanner />
        <MigrationBanner />
        <Outlet />
      </main>
      <CommandPalette open={paletteOpen} onOpenChange={setPaletteOpen} />
    </div>
  );
}
