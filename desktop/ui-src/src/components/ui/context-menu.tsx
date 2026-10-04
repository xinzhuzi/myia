import { Slot } from "@radix-ui/react-slot";
import * as React from "react";
import { createPortal } from "react-dom";

import { cn } from "@/lib/utils";

/**
 * shadcn/ui context-menu API 子集,无 @radix-ui/react-context-menu 依赖
 * (任务红线不装包;asChild 复用已装的 @radix-ui/react-slot)。自建范式同
 * ui/dropdown-menu.tsx(10-04-interaction-batch A-feed 落,清单基件原缺自建):
 * - 定位:fixed 锚定右键 pointer 坐标(trigger 的 contextmenu 事件捕获),
 *   视口内夹紧;滚动/缩放即关(菜单跟指针不跟元素,原生右键菜单惯例);
 * - 键盘:↑/↓/Home/End 巡游,Esc/Tab 关闭(右键无按钮 trigger,不还焦);
 * - 离场:播 pop-out 120ms(--duration-fast)后卸载;
 * - 根不渲染包装 DOM(纯 Provider):包列表卡等块级内容零增层级零布局扰动
 *   (dropdown 的 relative inline-flex 壳是给 trigger 锚定用的,这里不需要)。
 */

/** 与 --duration-fast(120ms)对应的离场卸载延迟,改 token 时同步改这里 */
const EXIT_UNMOUNT_MS = 120;

const ITEM_SELECTOR = '[role="menuitem"]:not([disabled])';

/** 右键锚点 = pointer 坐标(contextmenu 事件的 clientX/clientY) */
type ContextMenuAnchor = { x: number; y: number };

type ContextMenuContextValue = {
  open: boolean;
  setOpen: (open: boolean) => void;
  anchor: ContextMenuAnchor;
  setAnchor: (anchor: ContextMenuAnchor) => void;
};

const ContextMenuContext = React.createContext<ContextMenuContextValue | null>(null);

function useContextMenu(component: string) {
  const ctx = React.useContext(ContextMenuContext);
  if (!ctx) throw new Error(`<${component}> 必须在 <ContextMenu> 内使用`);
  return ctx;
}

function ContextMenu({
  open: openProp,
  defaultOpen = false,
  onOpenChange,
  children,
}: React.PropsWithChildren<{
  open?: boolean;
  defaultOpen?: boolean;
  onOpenChange?: (open: boolean) => void;
}>) {
  const [internal, setInternal] = React.useState(defaultOpen);
  const isControlled = openProp !== undefined;
  const open = isControlled ? openProp : internal;
  const [anchor, setAnchor] = React.useState<ContextMenuAnchor>({ x: 0, y: 0 });

  const setOpen = React.useCallback(
    (next: boolean) => {
      if (!isControlled) setInternal(next);
      onOpenChange?.(next);
    },
    [isControlled, onOpenChange],
  );

  const ctx = React.useMemo(
    () => ({ open, setOpen, anchor, setAnchor }),
    [open, setOpen, anchor],
  );

  // 纯 Provider 无包装 DOM(见头注):块级内容包裹零布局扰动
  return <ContextMenuContext.Provider value={ctx}>{children}</ContextMenuContext.Provider>;
}

function ContextMenuTrigger({
  asChild = false,
  onContextMenu,
  ...props
}: React.ComponentProps<"div"> & { asChild?: boolean }) {
  const { open, setOpen, setAnchor } = useContextMenu("ContextMenuTrigger");
  const Comp = asChild ? Slot : "div";

  return (
    <Comp
      data-slot="context-menu-trigger"
      data-state={open ? "open" : "closed"}
      {...props}
      onContextMenu={(event: React.MouseEvent<HTMLElement>) => {
        // asChild 时子元素非 div:事件面按 HTMLElement 收,透传回 div 形态 prop
        onContextMenu?.(event as React.MouseEvent<HTMLDivElement>);
        if (event.defaultPrevented) return;
        // 抑制原生右键菜单,换应用内菜单(pointer 坐标即锚点)
        event.preventDefault();
        setAnchor({ x: event.clientX, y: event.clientY });
        setOpen(true);
      }}
    />
  );
}

function ContextMenuContent({
  className,
  children,
  onKeyDown,
  ...props
}: React.ComponentProps<"div">) {
  const { open, setOpen, anchor } = useContextMenu("ContextMenuContent");
  const contentRef = React.useRef<HTMLDivElement>(null);
  const [mounted, setMounted] = React.useState(open);
  const [state, setState] = React.useState<"open" | "closed">(open ? "open" : "closed");

  React.useEffect(() => {
    if (open) {
      setMounted(true);
      setState("open");
    } else {
      setState((prev) => (prev === "open" ? "closed" : prev));
    }
  }, [open]);

  React.useEffect(() => {
    if (!open && mounted) {
      const timer = window.setTimeout(() => setMounted(false), EXIT_UNMOUNT_MS);
      return () => window.clearTimeout(timer);
    }
    return undefined;
  }, [open, mounted]);

  // pointer 锚定定位 + 外点/滚动/缩放关闭 + 开启聚焦
  React.useEffect(() => {
    if (!mounted) return undefined;
    const content = contentRef.current;

    function position() {
      const node = contentRef.current;
      if (!node) return;
      const margin = 8;
      // 视口内夹紧(菜单不溢出;jsdom 下 offsetWidth=0 也安全)
      const left = Math.min(Math.max(anchor.x, margin), window.innerWidth - node.offsetWidth - margin);
      const top = Math.min(Math.max(anchor.y, margin), window.innerHeight - node.offsetHeight - margin);
      node.style.top = `${Math.round(top)}px`;
      node.style.left = `${Math.round(left)}px`;
    }

    function handleOutside(event: Event) {
      const target = event.target as Node;
      if (!contentRef.current || contentRef.current.contains(target)) return;
      setOpen(false);
    }

    const raf = window.requestAnimationFrame(() => {
      position();
      content?.focus();
    });
    // 菜单跟指针不跟元素:视口滚动/缩放即关(原生右键菜单惯例)
    const close = () => setOpen(false);
    window.addEventListener("resize", close);
    window.addEventListener("scroll", close, true);
    document.addEventListener("pointerdown", handleOutside, true);
    return () => {
      window.cancelAnimationFrame(raf);
      window.removeEventListener("resize", close);
      window.removeEventListener("scroll", close, true);
      document.removeEventListener("pointerdown", handleOutside, true);
    };
  }, [mounted, anchor, setOpen]);

  function handleKeyDown(event: React.KeyboardEvent<HTMLDivElement>) {
    onKeyDown?.(event);
    if (event.defaultPrevented) return;
    const items = contentRef.current
      ? [...contentRef.current.querySelectorAll<HTMLElement>(ITEM_SELECTOR)]
      : [];
    if (event.key === "Escape" || event.key === "Tab") {
      event.preventDefault();
      setOpen(false);
      return;
    }
    if (items.length === 0) return;
    const index = items.indexOf(document.activeElement as HTMLElement);
    let next: HTMLElement | undefined;
    if (event.key === "ArrowDown") next = items[(index + 1 + items.length) % items.length];
    else if (event.key === "ArrowUp") next = items[(index - 1 + items.length) % items.length];
    else if (event.key === "Home") next = items[0];
    else if (event.key === "End") next = items[items.length - 1];
    if (next) {
      event.preventDefault();
      next.focus();
    }
  }

  if (!mounted) return null;

  return createPortal(
    <div
      ref={contentRef}
      role="menu"
      tabIndex={-1}
      data-slot="context-menu-content"
      data-state={state}
      className={cn(
        "fixed z-50 min-w-40 max-w-64 overflow-hidden rounded-md border border-border bg-popover p-1 text-popover-foreground shadow-popover",
        "focus:outline-none",
        "data-[state=open]:animate-pop-in data-[state=closed]:animate-pop-out",
        className,
      )}
      onKeyDown={handleKeyDown}
      {...props}
    >
      {children}
    </div>,
    document.body,
  );
}

function ContextMenuItem({
  className,
  variant = "default",
  onSelect,
  onClick,
  disabled,
  ...props
}: React.ComponentProps<"button"> & {
  variant?: "default" | "destructive";
}) {
  const { setOpen } = useContextMenu("ContextMenuItem");

  return (
    <button
      type="button"
      role="menuitem"
      data-variant={variant}
      disabled={disabled}
      data-slot="context-menu-item"
      className={cn(
        "flex w-full cursor-default items-center gap-2 rounded-sm px-2 py-1.5 text-left text-sm whitespace-nowrap select-none",
        "transition-colors duration-(--duration-fast) ease-out-expo",
        "focus:bg-accent focus:text-accent-foreground focus:outline-none",
        "data-[variant=destructive]:text-destructive data-[variant=destructive]:focus:bg-destructive/10",
        "disabled:pointer-events-none disabled:opacity-50",
        "[&_svg]:pointer-events-none [&_svg:not([class*='size-'])]:size-4 [&_svg]:shrink-0",
        "[&>kbd]:ml-auto [&>kbd]:text-2xs [&>kbd]:font-normal [&>kbd]:text-muted-foreground",
        className,
      )}
      {...props}
      onClick={(event) => {
        onClick?.(event);
        if (event.defaultPrevented) return;
        onSelect?.(event);
        if (event.defaultPrevented) return;
        setOpen(false);
      }}
    />
  );
}

function ContextMenuLabel({ className, ...props }: React.ComponentProps<"div">) {
  return (
    <div
      data-slot="context-menu-label"
      className={cn("px-2 py-1.5 text-2xs text-muted-foreground", className)}
      {...props}
    />
  );
}

function ContextMenuSeparator({ className, ...props }: React.ComponentProps<"div">) {
  return (
    <div
      role="separator"
      aria-orientation="horizontal"
      data-slot="context-menu-separator"
      className={cn("-mx-1 my-1 h-px bg-border", className)}
      {...props}
    />
  );
}

function ContextMenuGroup({ className, ...props }: React.ComponentProps<"div">) {
  return (
    <div
      role="group"
      data-slot="context-menu-group"
      className={cn("grid gap-0.5", className)}
      {...props}
    />
  );
}

export {
  ContextMenu,
  ContextMenuContent,
  ContextMenuGroup,
  ContextMenuItem,
  ContextMenuLabel,
  ContextMenuSeparator,
  ContextMenuTrigger,
};
