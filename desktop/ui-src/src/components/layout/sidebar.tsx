import { useCallback, useState } from "react";
import { FileCode2, Inbox, LayoutDashboard, Loader2, MessageCircle, PanelLeftClose, PanelLeftOpen, PlugZap, Rss, Settings, Terminal, Unplug } from "lucide-react";
import type { LucideIcon } from "lucide-react";
import { NavLink } from "react-router-dom";

import { MyssiaMark } from "@/components/myssia-mark";
import { Button } from "@/components/ui/button";
import { useHotkeys } from "@/hooks/use-hotkeys";
import { useSidecarStatus } from "@/hooks/use-sidecar-status";
import { cn } from "@/lib/utils";

/**
 * 导航分组(D4 壳层对标 Linear 侧栏「倒 L」结构,research/teardown-linear-activity.md
 * 可抄清单 #1):顶部主入口区(无组标题)→ 中部带标题分组 → 底部账户区。
 * 底部账户区映射 = 设置行 + sidecar 状态(本应用单用户无账户,Linear 的
 * 「用户头像/设置」落成「设置 + 运行状态」)。
 */
export interface NavEntry {
  to: string;
  label: string;
  icon: LucideIcon;
  /** 精确匹配(仅根路由需要) */
  end: boolean;
}

export interface NavGroup {
  /** null = 顶部主入口区(Linear 工作区区,无组标题) */
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
      { to: "/yaml-editor", label: "配置编辑", icon: FileCode2, end: false },
      { to: "/logs", label: "采集日志", icon: Terminal, end: false },
    ],
  },
  {
    label: "推送",
    entries: [{ to: "/messaging", label: "消息", icon: MessageCircle, end: false }],
  },
];

/** 底部设置行(Linear:底部账户区;样式与主导航行一致,激活竖条同口径) */
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
const SIDEBAR_DEFAULT_WIDTH = 224; // 展开宽(w-56 换算);w-56 类被内联宽取代
const SIDEBAR_MIN_WIDTH = 200;
const SIDEBAR_MAX_WIDTH = 360;
const SIDEBAR_ICON_WIDTH = 56; // 折叠宽(w-14 换算)

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

/** 导航行:图标 16px 与文字对齐(可抄 #14);激活 = accent 行背景 + 左缘 2px
 *  品牌竖条(可抄 #1/#6 的竖条语言),不加粗;hover 半透明 accent。
 *  折叠态:行仍占满导航内容宽、图标居中、文字隐去(title 补可达性)——
 *  行宽不变是刻意的:竖条 -left-2 在两态都钉在侧栏左缘同一位置,
 *  不会因图标居中而飘到行中间(激活竖条在图标态的位置适配)。 */
function NavRow({ entry, collapsed }: { entry: NavEntry; collapsed: boolean }) {
  const { to, label, icon: Icon, end } = entry;
  return (
    <NavLink
      to={to}
      end={end}
      title={collapsed ? label : undefined}
      className={({ isActive }) =>
        cn(
          "relative flex h-8 items-center rounded-md text-sm text-muted-foreground",
          "transition-colors duration-(--duration-fast) ease-out-expo",
          collapsed ? "justify-center px-0" : "gap-2.5 px-2.5",
          isActive ? "bg-accent text-foreground" : "hover:bg-accent/60 hover:text-foreground",
        )
      }
    >
      {({ isActive }) => (
        <>
          <span
            aria-hidden
            className={cn(
              "absolute -left-2 top-1/2 h-4 w-0.5 -translate-y-1/2 rounded-full bg-primary",
              "transition-opacity duration-(--duration-fast) ease-out-expo",
              isActive ? "opacity-100" : "opacity-0",
            )}
          />
          <Icon className="size-4 shrink-0" />
          {collapsed ? null : label}
        </>
      )}
    </NavLink>
  );
}

/**
 * 左侧导航(Linear 质感):品牌区 → 分组导航 → 底部(设置 + sidecar 状态 + 折叠钮)。
 * 滚动只发生在分组导航区;分组标题 2xs 弱色(Linear 分组标题体感)。
 * 折叠态(D4):`[` 键或底部按钮切换;图标态 = 品牌标居中、分组标题隐去、
 * 导航行图标居中;宽/折叠记忆走 localStorage(重开窗口还原)。
 */
export function Sidebar() {
  const [prefs, setPrefs] = useState<SidebarPrefs>(() => loadSidebarPrefs());
  const collapsed = prefs.collapsed;
  const width = prefs.width ?? SIDEBAR_DEFAULT_WIDTH;

  const toggleCollapsed = useCallback(() => {
    setPrefs((prev) => {
      const next = { ...prev, collapsed: !prev.collapsed };
      saveSidebarPrefs(next);
      return next;
    });
  }, []);

  // [ = 折叠/展开;输入框守卫在底座(顶栏搜索/CodeMirror 内敲 [ 不抢键)
  useHotkeys({ "[": toggleCollapsed });

  return (
    <aside
      style={{ width: collapsed ? SIDEBAR_ICON_WIDTH : width }}
      className="flex shrink-0 flex-col border-r border-border bg-sidebar text-sidebar-foreground transition-[width] duration-(--duration-base) ease-out-expo"
    >
      <div
        className={cn(
          "flex h-12 shrink-0 items-center border-b border-border/60 px-4",
          collapsed && "justify-center px-0",
        )}
        title={collapsed ? "世事 MYIA" : undefined}
      >
        <MyssiaMark className="size-6 shrink-0" />
        {collapsed ? null : (
          <>
            <span className="text-sm font-medium text-sidebar-foreground">世事</span>
            {/* 整值 muted-foreground(WCAG 实算):/70 在 sidebar 底上仅 3.68,/80 仅 4.49,均 <4.5;整值 6.46 */}
            <span className="text-2xs text-muted-foreground">MYIA</span>
          </>
        )}
      </div>
      <nav className="flex flex-1 flex-col gap-4 overflow-y-auto px-2 pt-3 pb-2" aria-label="主导航">
        {NAV_GROUPS.map((group, index) => (
          <div key={group.label ?? `main-${index}`} className="flex flex-col gap-0.5">
            {group.label && !collapsed ? (
              <div className="px-2.5 pb-0.5 pt-1 text-2xs text-muted-foreground">{group.label}</div>
            ) : null}
            {group.entries.map((entry) => (
              <NavRow key={entry.to} entry={entry} collapsed={collapsed} />
            ))}
          </div>
        ))}
      </nav>
      <div className="flex shrink-0 flex-col gap-0.5 border-t border-border/60 px-2 pt-1.5 pb-2">
        <NavRow entry={SETTINGS_ENTRY} collapsed={collapsed} />
        <SidecarStatusBar collapsed={collapsed} />
        <Button
          variant="ghost"
          size="sm"
          className={cn(
            "h-7 w-full justify-start px-2.5 text-xs text-muted-foreground",
            collapsed && "justify-center px-0",
          )}
          onClick={toggleCollapsed}
          title={collapsed ? "展开侧栏（[）" : "折叠侧栏（[）"}
          aria-label={collapsed ? "展开侧栏" : "折叠侧栏"}
          aria-keyshortcuts="["
        >
          {collapsed ? <PanelLeftOpen className="size-3.5" /> : <PanelLeftClose className="size-3.5" />}
        </Button>
      </div>
    </aside>
  );
}

/** 侧栏底部 sidecar 状态区(D4):状态点 + 一行状态文字;排障三件套
 *  (sidecar 版 · 协议版 · app 版)退到 title 悬浮,不在界面放开发期文案。
 *  折叠态:状态缩成居中一点/一转;dead/offline 只留动作钮(修复 > 状态)。 */
function SidecarStatusBar({ collapsed }: { collapsed: boolean }) {
  const { status, info, error, reprobe } = useSidecarStatus();

  if (status === "online") {
    const appPart = info?.app_version ? ` · app v${info.app_version}` : "";
    const title = `sidecar v${info?.version} · 协议 v${info?.protocol}${appPart}`;
    if (collapsed) {
      return (
        <div className="flex h-8 items-center justify-center" title={title}>
          <span className="relative flex size-2 shrink-0">
            <span className="absolute inline-flex h-full w-full animate-ping rounded-full bg-ok opacity-60" />
            <span className="relative inline-flex size-2 rounded-full bg-ok" />
          </span>
        </div>
      );
    }
    return (
      <div className="flex h-8 items-center gap-2 rounded-md px-2.5 text-xs text-muted-foreground" title={title}>
        <span className="relative flex size-2 shrink-0">
          <span className="absolute inline-flex h-full w-full animate-ping rounded-full bg-ok opacity-60" />
          <span className="relative inline-flex size-2 rounded-full bg-ok" />
        </span>
        sidecar 已连接
      </div>
    );
  }

  if (status === "connecting") {
    if (collapsed) {
      return (
        <div className="flex h-8 items-center justify-center text-muted-foreground" title="连接 sidecar…">
          <Loader2 className="size-3 shrink-0 animate-spin" />
        </div>
      );
    }
    return (
      <div className="flex h-8 items-center gap-2 rounded-md px-2.5 text-xs text-muted-foreground">
        <Loader2 className="size-3 shrink-0 animate-spin" />
        连接 sidecar…
      </div>
    );
  }

  if (status === "respawning") {
    // 壳层自动重拉中(main.rs 退避序列):静待,动作按钮保持可点(提前手动拉起)
    if (collapsed) {
      return (
        <div className="flex h-8 items-center justify-center text-warning" title="sidecar 已退出,壳层按退避自动重拉">
          <Loader2 className="size-3 shrink-0 animate-spin" />
        </div>
      );
    }
    return (
      <div className="flex h-8 items-center gap-2 rounded-md px-2.5 text-xs text-warning" title="sidecar 已退出,壳层按退避自动重拉">
        <Loader2 className="size-3 shrink-0 animate-spin" />
        重拉 sidecar…
      </div>
    );
  }

  if (status === "dead") {
    // 自动重拉超限:唯一修复动作 = 手动拉起(reprobe 内含 sidecar_restart)
    if (collapsed) {
      return (
        <div className="flex h-8 items-center justify-center">
          <Button
            variant="ghost"
            size="icon"
            className="size-8 shrink-0 text-dead"
            title="拉起 sidecar"
            aria-label="拉起 sidecar"
            onClick={reprobe}
          >
            <PlugZap className="size-3" />
          </Button>
        </div>
      );
    }
    return (
      <div
        className="flex h-8 items-center gap-1.5 rounded-md pl-2.5 pr-1 text-xs text-dead"
        title={error ? `${error.code}: ${error.message}` : undefined}
      >
        <Unplug className="size-3 shrink-0" />
        <span className="flex-1">sidecar 已停止</span>
        <Button
          variant="ghost"
          size="icon"
          className="size-6 shrink-0"
          title="拉起 sidecar"
          aria-label="拉起 sidecar"
          onClick={reprobe}
        >
          <PlugZap className="size-3" />
        </Button>
      </div>
    );
  }

  if (collapsed) {
    return (
      <div className="flex h-8 items-center justify-center">
        <Button
          variant="ghost"
          size="icon"
          className="size-8 shrink-0 text-warning"
          title="重新探测 sidecar(失败时自动拉起)"
          aria-label="重新探测 sidecar"
          onClick={reprobe}
        >
          <PlugZap className="size-3" />
        </Button>
      </div>
    );
  }
  return (
    <div
      className="flex h-8 items-center gap-1.5 rounded-md pl-2.5 pr-1 text-xs text-muted-foreground"
      title={error ? `${error.code} @ ${error.path}: ${error.message}` : undefined}
    >
      <Unplug className="size-3 shrink-0 text-warning" />
      <span className="flex-1">{error?.code === "sidecar_unavailable" ? "未在 Tauri 环境中" : "sidecar 未连接"}</span>
      <Button
        variant="ghost"
        size="icon"
        className="size-6 shrink-0"
        title="重新探测 sidecar(失败时自动拉起)"
        aria-label="重新探测 sidecar"
        onClick={reprobe}
      >
        <PlugZap className="size-3" />
      </Button>
    </div>
  );
}
