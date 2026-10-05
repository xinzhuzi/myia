import { Fragment, useCallback, useEffect, useId, useMemo, useRef, useState } from "react";
import { createPortal } from "react-dom";
import {
  Clock,
  FileCode2,
  Inbox,
  LayoutDashboard,
  Loader2,
  MessageCircle,
  Play,
  RefreshCw,
  Rss,
  Search,
  Settings,
  Terminal,
} from "lucide-react";
import type { LucideIcon } from "lucide-react";
import { useNavigate } from "react-router-dom";

import { api, SidecarRequestError } from "@/lib/api";
import { cn } from "@/lib/utils";

/**
 * ⌘K 全局命令面板(10-04-interaction-batch A-cmd,缺口 #3;D4 留位换真件)。
 *
 * 壳层 = ui/dialog.tsx 同范式自含实现(portal 到 body + 遮罩 + data-state
 * 进出场动画 + 120ms 离场卸载 + 滚动锁定 + 开启聚焦输入 + 关闭后焦点还给
 * 触发器),面板体自增 combobox 语义:输入过滤 / ↑↓ 巡游(环回)/ Enter
 * 执行 / Esc 关闭。⌘K(Ctrl+K)开关监听在本组件内自含(不走 A-shell 的
 * use-hotkeys,免跨批文件依赖;带修饰键的组合不跳输入目标——全局唤起
 * 本就应在任何焦点下生效)。
 *
 * 命令面(清单自含,不复用 sidebar 的 NAV_GROUPS,避免与 A-shell 跨批
 * 耦合,重复属有意取舍):
 * - 导航八屏(App.tsx 路由表口径);
 * - 跑一次:health → 第一个可加载插件 → run.start;
 * - 刷新:window.location.reload(自含,不逐屏发刷新事件)。
 *
 * 10-05 复活注记:无头布局(d9ae353)整删 TopBar 时,本面板唯一渲染点随
 * 之消失成为不可达死 UI(主人「怎么解决」→ AppLayout 直挂复活,⌘K 全局
 * 热键本就自含,零视觉占用不回顶栏不破无头令);品类命令组与 category 族
 * props 随 TopBar 全球品类过滤(7152ff9 归情报流屏)一并退役,精确的逐品类
 * 跑一次入口在 cron 屏排程一览行尾。
 */

/** 与 --duration-fast(120ms)对应的离场卸载延迟,改 token 时同步改这里(dialog.tsx 同款) */
const EXIT_UNMOUNT_MS = 120;

/** 导航命令清单:App.tsx 路由表八屏(自含数据,不 import NAV_GROUPS) */
const SCREENS: ReadonlyArray<{ to: string; label: string; icon: LucideIcon; keywords: string }> = [
  { to: "/", label: "仪表盘", icon: LayoutDashboard, keywords: "dashboard home" },
  { to: "/feed", label: "情报流", icon: Inbox, keywords: "feed inbox" },
  { to: "/sources", label: "源管理", icon: Rss, keywords: "sources rss" },
  { to: "/cron", label: "定时任务", icon: Clock, keywords: "cron schedule timer jobs" },
  { to: "/yaml-editor", label: "配置编辑", icon: FileCode2, keywords: "yaml editor config" },
  { to: "/messaging", label: "消息", icon: MessageCircle, keywords: "messaging message push" },
  { to: "/logs", label: "采集日志", icon: Terminal, keywords: "logs terminal" },
  { to: "/settings", label: "设置", icon: Settings, keywords: "settings" },
];

/** 面板分组(渲染序 = commands 构建序,filter 保序故分组天然连续) */
const GROUP_ORDER = ["导航", "动作"] as const;
type CommandGroup = (typeof GROUP_ORDER)[number];

interface CommandItem {
  id: string;
  group: CommandGroup;
  label: string;
  /** 右侧弱色注记(品类 id / 动作说明) */
  hint?: string;
  /** 过滤补充匹配(英文路由尾 / 品类 id) */
  keywords?: string;
  icon: LucideIcon;
  run: () => void | Promise<void>;
}

export interface CommandPaletteProps {
  open: boolean;
  onOpenChange: (open: boolean) => void;
}

export function CommandPalette({ open, onOpenChange }: CommandPaletteProps) {
  const navigate = useNavigate();
  const listId = useId();
  const inputRef = useRef<HTMLInputElement | null>(null);
  const restoreFocusRef = useRef<HTMLElement | null>(null);

  const [query, setQuery] = useState("");
  const [activeIndex, setActiveIndex] = useState(0);
  const [runStarting, setRunStarting] = useState(false);
  const [runError, setRunError] = useState<string | null>(null);

  // 离场动画挂载态(dialog 范式:关闭后保持 120ms 播 out 再卸载)
  const [mounted, setMounted] = useState(open);
  const [state, setState] = useState<"open" | "closed">(open ? "open" : "closed");

  // ⌘K / Ctrl+K 开关监听(组件内自含;preventDefault 压掉浏览器/壳层默认)
  useEffect(() => {
    function onKeyDown(event: KeyboardEvent) {
      if ((event.metaKey || event.ctrlKey) && event.key.toLowerCase() === "k") {
        event.preventDefault();
        onOpenChange(!open);
      }
    }
    window.addEventListener("keydown", onKeyDown);
    return () => window.removeEventListener("keydown", onKeyDown);
  }, [open, onOpenChange]);

  // 开→播 in;关→播 out + 定时卸载(再开则撤销卸载)
  useEffect(() => {
    if (open) {
      setMounted(true);
      setState("open");
    } else {
      setState((prev) => (prev === "open" ? "closed" : prev));
    }
  }, [open]);

  useEffect(() => {
    if (!open && mounted) {
      const timer = window.setTimeout(() => setMounted(false), EXIT_UNMOUNT_MS);
      return () => window.clearTimeout(timer);
    }
    return undefined;
  }, [open, mounted]);

  // 开启即复位(输入/巡游/错误残留;关闭动画期保留态无害)
  useEffect(() => {
    if (open) {
      setQuery("");
      setActiveIndex(0);
      setRunError(null);
    }
  }, [open]);

  // 滚动锁定 + 初始聚焦输入 + 关闭后焦点还给开启前元素(dialog 范式)
  useEffect(() => {
    if (!mounted) return undefined;
    restoreFocusRef.current = document.activeElement as HTMLElement | null;
    const previousOverflow = document.body.style.overflow;
    document.body.style.overflow = "hidden";
    const raf = window.requestAnimationFrame(() => inputRef.current?.focus());
    return () => {
      window.cancelAnimationFrame(raf);
      document.body.style.overflow = previousOverflow;
      const target = restoreFocusRef.current;
      if (target && document.contains(target)) target.focus?.();
    };
  }, [mounted]);

  /** 跑一次:health → 第一个可加载插件 → run.start(品类定位已随品类组退役) */
  const runOnce = useCallback(async () => {
    if (runStarting) return;
    setRunStarting(true);
    setRunError(null);
    try {
      const health = await api.health();
      const plugin = health.plugins.find((candidate) => candidate.loaded) ?? health.plugins[0];
      if (!plugin) {
        // 保持打开,错误在面板脚注可见
        setRunError("插件目录为空:重启应用触发首跑初始化,或到「源管理」检查插件目录。");
        return;
      }
      await api.runStart({ yaml: plugin.file });
      onOpenChange(false);
    } catch (err) {
      setRunError(err instanceof SidecarRequestError ? `${err.code}: ${err.message}` : String(err));
    } finally {
      setRunStarting(false);
    }
  }, [onOpenChange, runStarting]);

  const commands = useMemo<CommandItem[]>(() => {
    const navCommands: CommandItem[] = SCREENS.map((screen) => ({
      id: `nav-${screen.to}`,
      group: "导航",
      label: screen.label,
      keywords: screen.keywords,
      icon: screen.icon,
      run: () => {
        onOpenChange(false);
        navigate(screen.to);
      },
    }));
    const actionCommands: CommandItem[] = [
      {
        id: "action-run",
        group: "动作",
        label: "跑一次",
        hint: "第一个可用品类",
        keywords: "run collect 采集",
        icon: Play,
        run: runOnce,
      },
      {
        id: "action-reload",
        group: "动作",
        label: "刷新",
        hint: "重载界面",
        keywords: "reload refresh",
        icon: RefreshCw,
        run: () => {
          onOpenChange(false);
          window.location.reload();
        },
      },
    ];
    return [...navCommands, ...actionCommands];
  }, [navigate, onOpenChange, runOnce]);

  const keyword = query.trim().toLowerCase();
  const filtered = useMemo(
    () =>
      keyword
        ? commands.filter(
            (item) =>
              item.label.toLowerCase().includes(keyword) ||
              (item.keywords?.toLowerCase().includes(keyword) ?? false),
          )
        : commands,
    [commands, keyword],
  );

  // 清单收缩(过滤词变化在 onChange 已重置;品类选项晚到)时钳制巡游下标
  useEffect(() => {
    setActiveIndex((index) => Math.min(index, Math.max(filtered.length - 1, 0)));
  }, [filtered.length]);

  const activeDescendantId =
    filtered.length > 0 ? `${listId}-opt-${Math.min(activeIndex, filtered.length - 1)}` : undefined;

  // 巡游高亮滚动跟随(nearest,不跳滚动;jsdom 未实现由测试 stub)
  useEffect(() => {
    if (!mounted || !activeDescendantId) return;
    document.getElementById(activeDescendantId)?.scrollIntoView({ block: "nearest" });
  }, [activeDescendantId, mounted]);

  if (!mounted) return null;

  return createPortal(
    <div
      data-slot="command-palette-overlay"
      data-state={state}
      className={cn(
        "fixed inset-0 z-50 flex items-start justify-center bg-black/60 px-4 pt-[16vh]",
        "data-[state=open]:animate-overlay-in data-[state=closed]:animate-overlay-out",
      )}
      onMouseDown={(event) => {
        if (event.target === event.currentTarget) onOpenChange(false);
      }}
      onKeyDown={(event) => {
        if (event.defaultPrevented) return;
        if (event.key === "Escape") {
          event.preventDefault();
          onOpenChange(false);
        } else if (event.key === "ArrowDown") {
          event.preventDefault();
          setActiveIndex((index) => (filtered.length > 0 ? (index + 1) % filtered.length : 0));
        } else if (event.key === "ArrowUp") {
          event.preventDefault();
          setActiveIndex((index) =>
            filtered.length > 0 ? (index - 1 + filtered.length) % filtered.length : 0,
          );
        } else if (event.key === "Enter") {
          event.preventDefault();
          const item = filtered[Math.min(activeIndex, filtered.length - 1)];
          if (item) void item.run();
        } else if (event.key === "Tab") {
          // 单焦点件(输入框)圈禁:Tab 不出面板
          event.preventDefault();
        }
      }}
    >
      <div
        role="dialog"
        aria-modal="true"
        aria-label="命令面板"
        tabIndex={-1}
        data-slot="command-palette"
        data-state={state}
        className={cn(
          "relative flex w-full max-w-lg flex-col overflow-hidden rounded-lg border border-border bg-card text-card-foreground shadow-drawer",
          "data-[state=open]:animate-dialog-in data-[state=closed]:animate-dialog-out",
          "focus:outline-none",
        )}
      >
        <div className="flex items-center gap-2.5 border-b border-border/60 px-4">
          <Search className="size-4 shrink-0 text-muted-foreground" aria-hidden />
          <input
            ref={inputRef}
            value={query}
            onChange={(event) => {
              setQuery(event.target.value);
              setActiveIndex(0);
            }}
            placeholder="搜索或跳转…"
            aria-label="搜索命令"
            role="combobox"
            aria-expanded="true"
            aria-controls={listId}
            aria-activedescendant={activeDescendantId}
            aria-autocomplete="list"
            className="h-11 min-w-0 flex-1 bg-transparent text-sm text-foreground outline-none placeholder:text-muted-foreground/60"
          />
          <kbd className="shrink-0 rounded-sm border border-border/60 bg-muted px-1.5 font-mono text-2xs leading-4 text-muted-foreground">
            esc
          </kbd>
        </div>

        <div id={listId} role="listbox" aria-label="命令列表" className="max-h-72 overflow-y-auto p-1.5">
          {filtered.length === 0 ? (
            <div className="px-3 py-8 text-center text-xs text-muted-foreground">无匹配命令</div>
          ) : (
            filtered.map((item, index) => {
              const ItemIcon = item.id === "action-run" && runStarting ? Loader2 : item.icon;
              return (
                <Fragment key={item.id}>
                  {index === 0 || filtered[index - 1].group !== item.group ? (
                    <div className="px-2.5 pb-0.5 pt-1 text-2xs text-muted-foreground">{item.group}</div>
                  ) : null}
                  <div
                    id={`${listId}-opt-${index}`}
                    role="option"
                    aria-selected={index === activeIndex}
                    className={cn(
                      "flex h-9 cursor-default items-center gap-2.5 rounded-md px-2.5 text-sm text-muted-foreground",
                      "transition-colors duration-(--duration-fast) ease-out-expo",
                      index === activeIndex ? "bg-accent text-foreground" : null,
                    )}
                    onMouseEnter={() => setActiveIndex(index)}
                    // 按下不抢焦(输入框保持焦点,combobox 惯例);点击照常派发
                    onMouseDown={(event) => event.preventDefault()}
                    onClick={() => void item.run()}
                  >
                    <ItemIcon
                      className={cn(
                        "size-4 shrink-0",
                        item.id === "action-run" && runStarting ? "animate-spin" : null,
                      )}
                      aria-hidden
                    />
                    <span className="flex-1 truncate">{item.label}</span>
                    {item.hint ? (
                      <span className="max-w-40 truncate text-2xs text-muted-foreground/70">{item.hint}</span>
                    ) : null}
                  </div>
                </Fragment>
              );
            })
          )}
        </div>

        <footer className="flex items-center gap-3 border-t border-border/60 px-4 py-2 text-2xs text-muted-foreground">
          <span>↑↓ 巡游</span>
          <span>↵ 执行</span>
          <span>esc 关闭</span>
          <span className="flex-1" />
          {runError ? (
            <span data-testid="palette-run-error" className="max-w-56 truncate text-destructive" title={runError}>
              {runError}
            </span>
          ) : null}
        </footer>
      </div>
    </div>,
    document.body,
  );
}
