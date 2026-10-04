import { useCallback, useEffect, useRef, useState } from "react";
import { ChevronDown, Clock, FileCode2, Inbox, LayoutDashboard, MessageCircle, Rss, Settings, Terminal } from "lucide-react";
import type { LucideIcon } from "lucide-react";
import { NavLink } from "react-router-dom";

import { cn } from "@/lib/utils";

/**
 * 导航分组(10-04-ui-kestra-anchor 重锚 Kestra SideBar 模式):
 * 顶部主入口区(无组标题 = Kestra 顶层直链)→ 中部带标题分组
 * (KsSideBarSection:可折叠 + chevron)→ 底部账户区映射 = 设置行 +
 * sidecar 状态(本应用单用户无账户)。
 * [来源 Apache-2.0,只读参考,借结构改语义]
 *  kestra/ui/src/components/layout/SideBar.vue(顶层直链/分组/收藏/底部槽)
 *  kestra/ui/packages/design-system/.../KsSideBar(KsSideBarSection/KsSideBarItem).vue
 */
export interface NavEntry {
 to: string;
 label: string;
 icon: LucideIcon;
 /** 精确匹配(仅根路由需要) */
 end: boolean;
}

export interface NavGroup {
 /** null = 顶部主入口区(Kestra 顶层直链区,无组标题、不可折叠) */
 label: string | null;
 entries: NavEntry[];
}

/** 导航分组清单(prd A-shell「顺手 export」:供后续复用,如命令面/测试口径) */
export const NAV_GROUPS: NavGroup[] = [
 {
  label: null,
  entries: [
   { to: "/", label: "仪表盘", icon: LayoutDashboard, end: true },
   { to: "/feed", label: "情报流", icon: Inbox, end: false },
  ],
 },
 {
  label: "采集",
  entries: [
   { to: "/sources", label: "源管理", icon: Rss, end: false },
   // 定时任务(10-04-cron-ui):cron.* 管理屏,位次=源管理之后
   // (与 App.tsx 路由一致;Clock 图标=排程语义)
   { to: "/cron", label: "定时任务", icon: Clock, end: false },
   { to: "/yaml-editor", label: "配置编辑", icon: FileCode2, end: false },
   { to: "/logs", label: "采集日志", icon: Terminal, end: false },
  ],
 },
 {
  label: "推送",
  entries: [{ to: "/messaging", label: "消息", icon: MessageCircle, end: false }],
 },
];

/** 底部设置行(Kestra footer 槽;样式与主导航行一致) */
const SETTINGS_ENTRY: NavEntry = { to: "/settings", label: "设置", icon: Settings, end: false };

/** 按路由解析当前导航项(顶栏面包屑与侧栏激活态同一口径) */
export function resolveNav(pathname: string): { group: string | null; entry: NavEntry } | null {
 const all = [...NAV_GROUPS.map((group) => ({ label: group.label, entries: group.entries })), { label: null, entries: [SETTINGS_ENTRY] }];
 for (const group of all) {
  for (const entry of group.entries) {
   const matched = entry.end
    ? pathname === entry.to
    : pathname === entry.to || pathname.startsWith(entry.to + "/");
   if (matched) return { group: group.label, entry };
  }
 }
 return null;
}

// ---------------------------------------------------------------------------
// 折叠态本地记忆(localStorage;与 feed 屏本地态同纪律:损坏即弃、写失败不阻断)
// ---------------------------------------------------------------------------

/** 侧栏偏好(宽/折叠记忆) */
export interface SidebarPrefs {
 collapsed: boolean;
 /** 展开态宽度(px);null = 未自定义(拖拽调宽落地后写入,底座先支持记忆) */
 width: number | null;
}

const SIDEBAR_STORAGE_KEY = "myssia.sidebar.v1";
const SIDEBAR_GROUPS_STORAGE_KEY = "myssia.sidebar-groups.v1";
const SIDEBAR_DEFAULT_WIDTH = 224; // 展开宽(w-56 换算);w-56 类被内联宽取代
const SIDEBAR_MIN_WIDTH = 200;
const SIDEBAR_MAX_WIDTH = 360;
const SIDEBAR_ICON_WIDTH = 56; // 折叠宽(w-14 换算)
const SIDEBAR_COLLAPSE_THRESHOLD = 120; // 拖拽到此宽以下自动折叠(icon 态)

export function loadSidebarPrefs(
 storage: Storage | null = typeof window === "undefined" ? null : window.localStorage,
): SidebarPrefs {
 if (storage === null) return { collapsed: false, width: null };
 try {
  const raw = storage.getItem(SIDEBAR_STORAGE_KEY);
  if (!raw) return { collapsed: false, width: null };
  const parsed: unknown = JSON.parse(raw);
  if (parsed === null || typeof parsed !== "object" || Array.isArray(parsed)) {
   return { collapsed: false, width: null };
  }
  const record = parsed as Record<string, unknown>;
  const width =
   typeof record.width === "number" && Number.isFinite(record.width)
    ? Math.min(SIDEBAR_MAX_WIDTH, Math.max(SIDEBAR_MIN_WIDTH, Math.round(record.width)))
    : null;
  return { collapsed: record.collapsed === true, width };
 } catch {
  return { collapsed: false, width: null }; // 损坏即弃(下次切换重写)
 }
}

export function saveSidebarPrefs(
 prefs: SidebarPrefs,
 storage: Storage | null = typeof window === "undefined" ? null : window.localStorage,
): void {
 if (storage === null) return;
 try {
  storage.setItem(SIDEBAR_STORAGE_KEY, JSON.stringify(prefs));
 } catch {
  // 配额/隐私模式写失败不阻断界面(记忆尽力而为)
 }
}

/** 分组折叠记忆(Kestra layoutStore.setMenuSectionCollapsed 的本地等价;
 * 独立存储键——不并入 sidebar.v1,避免污染其 {collapsed,width} 契约)。
 * 只记录显式折叠(true)的组,缺省 = 展开(Kestra defaultCollapsed=false)。 */
function loadGroupCollapsed(
 storage: Storage | null = typeof window === "undefined" ? null : window.localStorage,
): Record<string, boolean> {
 if (storage === null) return {};
 try {
  const raw = storage.getItem(SIDEBAR_GROUPS_STORAGE_KEY);
  if (!raw) return {};
  const parsed: unknown = JSON.parse(raw);
  if (parsed === null || typeof parsed !== "object" || Array.isArray(parsed)) return {};
  const out: Record<string, boolean> = {};
  for (const [key, value] of Object.entries(parsed as Record<string, unknown>)) {
   if (value === true) out[key] = true; // 只认真布尔,其余形态弃
  }
  return out;
 } catch {
  return {}; // 损坏即弃
 }
}

function saveGroupCollapsed(
 groups: Record<string, boolean>,
 storage: Storage | null = typeof window === "undefined" ? null : window.localStorage,
): void {
 if (storage === null) return;
 try {
  storage.setItem(SIDEBAR_GROUPS_STORAGE_KEY, JSON.stringify(groups));
 } catch {
  // 写失败不阻断
 }
}

/** 导航行(Kestra KsSideBarItem 规格):min-h 26px · px8/py4 · gap8 ·
 * 圆角 8(--ks-radius-base)· 字 12/500 · 图标 16px;
 * hover = bg-hover 填充 + 次级文字色;active = bg-active 填充 + link 色
 * (primary-200,--ks-text-link)——弃 Linear 左缘竖条,Kestra 以
 * 「填充 + 文字色」区分激活。折叠态:图标居中、文字隐去(title 补可达性)。 */
function NavRow({ entry, collapsed }: { entry: NavEntry; collapsed: boolean }) {
 const { to, label, icon: Icon, end } = entry;
 return (
  <NavLink
   to={to}
   end={end}
   title={collapsed ? label : undefined}
   className={({ isActive }) =>
    cn(
     "flex min-h-[26px] items-center gap-2 rounded-md py-1 text-xs font-medium",
     "transition-colors duration-(--duration-fast) ease-out-expo",
     collapsed ? "justify-center px-0" : "px-2",
     isActive
      ? "bg-accent text-link"
      : "text-foreground hover:bg-accent hover:text-secondary-foreground",
    )
   }
  >
   {({ isActive }) => (
    <>
     <Icon className={cn("size-4 shrink-0", isActive && "text-link")} aria-hidden />
     {collapsed ? null : label}
    </>
   )}
  </NavLink>
 );
}

/** 分组区(Kestra KsSideBarSection 借构):标题钮(12/400/dim 色,hover 提
 * 前景色)+ chevron 14px 折叠旋 -90°;条目区 grid-rows 0fr↔1fr 折叠动画
 * (250ms · Kestra 缓动 cubic-bezier(0.22,1,0.36,1)),折叠时内层 inert
 * 防键盘焦点(Kestra 同款)。chevron 紧随文字(Kestra 原版排布)。 */
function GroupSection({
 label,
 entries,
 collapsed,
 onToggle,
}: {
 label: string;
 entries: NavEntry[];
 collapsed: boolean;
 onToggle: (label: string) => void;
}) {
 const isCollapsed = collapsed === true;
 return (
  <section className="flex flex-col">
   <button
    type="button"
    aria-expanded={!isCollapsed}
    onClick={() => onToggle(label)}
    className="flex w-full items-center gap-2 px-2.5 pb-1 pt-2 text-xs font-normal text-muted-foreground transition-colors duration-(--duration-fast) ease-out-expo hover:text-foreground"
   >
    <span className="min-w-0 truncate text-left">{label}</span>
    <ChevronDown
     aria-hidden
     className={cn(
      "size-3.5 shrink-0 transition-transform duration-(--duration-fast) ease-out-expo",
      isCollapsed && "-rotate-90",
     )}
    />
   </button>
   <div
    className={cn(
     "grid transition-[grid-template-rows] duration-[250ms] ease-[cubic-bezier(0.22,1,0.36,1)]",
     isCollapsed ? "grid-rows-[0fr]" : "grid-rows-[1fr]",
    )}
   >
    <div className="min-h-0 overflow-hidden" inert={isCollapsed ? true : undefined}>
     <div className="flex flex-col gap-1">
      {entries.map((entry) => (
       <NavRow key={entry.to} entry={entry} collapsed={false} />
      ))}
     </div>
    </div>
   </div>
  </section>
 );
}

/**
 * 左侧导航(Kestra SideBar 模式):品牌区(含折叠钮,= Kestra header 槽的
 * header-toggle)→ 分组导航(可折叠分组)→ 底部(设置 + sidecar 状态)。
 * 面板 = bg-sidebar + 右缘 1px 描边,扁平无内分隔线(Kestra 同款);
 * 滚动只发生在分组导航区;折叠态 = 品牌标与折叠钮纵向堆叠(56px 宽)、
 * 分组标题隐去、导航行图标居中;宽/折叠/分组折叠记忆走 localStorage。
 */
export function Sidebar() {
 const [prefs, setPrefs] = useState<SidebarPrefs>(() => loadSidebarPrefs());
 const [groupCollapsed, setGroupCollapsed] = useState<Record<string, boolean>>(() => loadGroupCollapsed());
 const collapsed = prefs.collapsed;
 const width = prefs.width ?? SIDEBAR_DEFAULT_WIDTH;
 const [dragging, setDragging] = useState(false);
 const dragState = useRef<{ startX: number; startWidth: number } | null>(null);

 const toggleGroup = useCallback((label: string) => {
  setGroupCollapsed((prev) => {
   const next = { ...prev, [label]: prev[label] !== true };
   saveGroupCollapsed(next);
   return next;
  });
 }, []);

 // 鼠标拖拽右缘调宽:拖到 <COLLAPSE_THRESHOLD 自动折叠(icon 态),拖宽自动展开;松手持久化
 const onDragStart = useCallback((e: React.PointerEvent) => {
  e.preventDefault();
  dragState.current = { startX: e.clientX, startWidth: collapsed ? SIDEBAR_ICON_WIDTH : width };
  setDragging(true);
 }, [collapsed, width]);

 useEffect(() => {
  if (!dragging) return;
  const onMove = (e: PointerEvent) => {
   if (!dragState.current) return;
   const delta = e.clientX - dragState.current.startX;
   const target = dragState.current.startWidth + delta;
   setPrefs((prev) => {
    if (target <= SIDEBAR_COLLAPSE_THRESHOLD) {
     return { ...prev, collapsed: true };
    }
    const clamped = Math.max(SIDEBAR_MIN_WIDTH, Math.min(SIDEBAR_MAX_WIDTH, target));
    return { collapsed: false, width: clamped };
   });
  };
  const onUp = () => {
   setDragging(false);
   dragState.current = null;
   setPrefs((prev) => {
    saveSidebarPrefs(prev);
    return prev;
   });
  };
  document.addEventListener("pointermove", onMove);
  document.addEventListener("pointerup", onUp);
  return () => {
   document.removeEventListener("pointermove", onMove);
   document.removeEventListener("pointerup", onUp);
  };
 }, [dragging]);

 return (
  <aside
   style={{ width: collapsed ? SIDEBAR_ICON_WIDTH : width }}
   className={cn(
    "relative flex shrink-0 flex-col border-r border-border bg-sidebar text-sidebar-foreground",
    dragging ? "" : "transition-[width] duration-(--duration-base) ease-out-expo",
   )}
  >
   {/* 拖拽手柄:右缘 6px 命中区,hover/drag 高亮;拖到窄端自动折叠 */}
   <div
    role="separator"
    aria-orientation="vertical"
    aria-label="拖拽调整侧栏宽度(拖到最窄折叠为图标)"
    onPointerDown={onDragStart}
    className={cn(
     "absolute inset-y-0 right-0 z-10 w-1.5 cursor-col-resize select-none",
     dragging ? "bg-primary/40" : "bg-transparent hover:bg-primary/20",
    )}
    style={{ marginRight: "0px" }}
   />
   {/* 品牌区已删(主人「无头」);macOS 标题栏走 overlay 沉浸式 */}
   {/* 分组节奏:组间 16px,组内行距 4px(gap-1) */}
   <nav className="flex flex-1 flex-col gap-4 overflow-y-auto px-2 pt-3 pb-2" aria-label="主导航">
    {NAV_GROUPS.map((group, index) =>
     !collapsed && group.label !== null ? (
      <GroupSection
       key={group.label}
       label={group.label}
       entries={group.entries}
       collapsed={groupCollapsed[group.label] === true}
       onToggle={toggleGroup}
      />
     ) : (
      <div key={group.label ?? `main-${index}`} className="flex flex-col gap-1">
       {group.entries.map((entry) => (
        <NavRow key={entry.to} entry={entry} collapsed={collapsed} />
       ))}
      </div>
     ),
    )}
   </nav>
   <div className="flex shrink-0 flex-col gap-1 px-2 pt-2 pb-2.5">
    <NavRow entry={SETTINGS_ENTRY} collapsed={collapsed} />
   </div>
  </aside>
 );
}

/** 侧栏底部 sidecar 状态区(D4):状态点 + 一行状态文字;排障三件套
 * (sidecar 版 · 协议版 · app 版)退到 title 悬浮,不在界面放开发期文案。
 * 折叠态:状态缩成居中一点/一转;dead/offline 只留动作钮(修复 > 状态)。 */
