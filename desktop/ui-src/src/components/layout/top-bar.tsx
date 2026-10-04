import { useEffect, useState } from "react";
import { ChevronRight, Search } from "lucide-react";
import { NavLink, useLocation } from "react-router-dom";

import { CommandPalette } from "@/components/layout/command-palette";
import { GlobalRun } from "@/components/layout/global-run";
import { resolveNav } from "@/components/layout/sidebar";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { api } from "@/lib/api";

/** 品类下拉选项(health().plugins 的 id 去重 + 名称回显;排序稳定) */
interface CategoryOption {
  id: string;
  label: string;
}

/** 命令位快捷键文案:macOS ⌘K,其余平台 Ctrl K(桌面跨平台惯例) */
const COMMAND_KEY =
  typeof navigator !== "undefined" && /Mac|iPhone|iPad/.test(navigator.platform ?? "") ? "⌘K" : "Ctrl K";

/**
 * 顶栏(D4 壳层对标 Linear):左侧面包屑(工作区 › 分组 › 页面,与侧栏
 * 导航同一解析口径),右侧品类全局过滤 + 全局跑一次 + 全局命令位。
 * sidecar 状态已迁侧栏底部账户区(Linear 底部状态区)。
 */
export function TopBar({
  category,
  onCategoryChange,
}: {
  category: string | null;
  onCategoryChange: (next: string | null) => void;
}) {
  const [options, setOptions] = useState<CategoryOption[]>([]);
  const [paletteOpen, setPaletteOpen] = useState(false);

  useEffect(() => {
    let cancelled = false;
    void api
      .health()
      .then((health) => {
        if (cancelled) return;
        // id 去重(目录内同 id 多文件时首现优先)+ 名称回显;装不上的
        // 插件 id=null 不入选项(选了也无数据可滤)
        const seen = new Map<string, string>();
        for (const plugin of health.plugins) {
          if (plugin.id && !seen.has(plugin.id)) {
            seen.set(plugin.id, plugin.name ?? plugin.id);
          }
        }
        setOptions(
          [...seen.entries()]
            .map(([id, name]) => ({ id, label: name }))
            .sort((a, b) => a.id.localeCompare(b.id)),
        );
      })
      .catch(() => {
        // health 失败不拦顶栏:保持「全部品类」可用,选中过滤自然空态
        if (!cancelled) setOptions([]);
      });
    return () => {
      cancelled = true;
    };
  }, []);

  return (
    <header className="flex h-12 shrink-0 items-center border-b border-border bg-background/80">
      {/* R2 刀2 栅格:顶栏内容列与 main 同一收束(max-w-content)+ 同一 px-6,
          面包屑左缘 = 页标题左缘 = 内容左缘,三线对齐(Linear 顶栏/内容同栅格) */}
      <div className="mx-auto flex h-full w-full max-w-content items-center gap-3 px-6">
        <Breadcrumb />

        <div className="flex-1" />

        {/* R2 校准轮①:品类 Select 直接作顶栏兄弟(去外包 div 的 gap-2 内档),
            顶栏四个控件兄弟间距统一 gap-3,一行一档 */}
        <Select
          value={category ?? "all"}
          onValueChange={(value) => onCategoryChange(value === "all" ? null : value)}
        >
          <SelectTrigger size="sm" className="w-36" aria-label="品类选择">
            <SelectValue />
          </SelectTrigger>
          {/* R2 刀4:浮层阴影走 --shadow-popover 令牌(面分层体系),替默认 shadow-md */}
          <SelectContent className="shadow-popover">
            <SelectItem value="all">全部品类</SelectItem>
            {options.map((option) => (
              <SelectItem key={option.id} value={option.id}>
                {option.label}
              </SelectItem>
            ))}
          </SelectContent>
        </Select>

        <GlobalRun category={category} />

        {/* 全局命令位:⌘K 命令面板真触发器(D4 留位 → interaction-batch A-cmd)。
            R2 刀4 控件规格:静息微填充 + 低可见描边(--control-* 令牌,与
            Input/SelectTrigger 同族),不再裸 muted/30 底 + 独立描边 */}
        <button
          type="button"
          aria-haspopup="dialog"
          aria-expanded={paletteOpen}
          aria-label="打开命令面板"
          title="命令面板(⌘K:导航/跑一次/刷新/切品类)"
          onClick={() => setPaletteOpen(true)}
          className="flex h-7 w-44 cursor-pointer items-center gap-1.5 rounded-md border border-(--control-border) bg-(--control-bg) px-2 text-xs text-muted-foreground outline-none transition-colors duration-(--duration-fast) ease-out-expo hover:border-(--control-border) hover:bg-(--control-bg-hover) hover:text-foreground focus-visible:ring-[3px] focus-visible:ring-ring/40"
        >
          <Search className="size-3 shrink-0" aria-hidden />
          <span className="flex-1 truncate text-left">搜索或跳转…</span>
          <kbd className="rounded-sm border border-border/60 bg-muted px-1 font-mono text-2xs leading-4 text-muted-foreground">
            {COMMAND_KEY}
          </kbd>
        </button>
        <CommandPalette
          open={paletteOpen}
          onOpenChange={setPaletteOpen}
          category={category}
          categoryOptions={options}
          onCategoryChange={onCategoryChange}
        />
      </div>
    </header>
  );
}

/** 面包屑:世事 › 分组 › 页面(当前页为末段,foreground 中字重;前段弱色) */
function Breadcrumb() {
  const location = useLocation();
  const nav = resolveNav(location.pathname);
  if (!nav) return null;
  return (
    <nav aria-label="面包屑" className="flex min-w-0 items-center gap-1">
      <NavLink
        to="/"
        className="text-xs text-muted-foreground transition-colors duration-(--duration-fast) ease-out-expo hover:text-foreground"
      >
        世事
      </NavLink>
      {nav.group ? (
        <>
          <ChevronRight className="size-3 shrink-0 text-muted-foreground/50" aria-hidden />
          <span className="text-xs text-muted-foreground">{nav.group}</span>
        </>
      ) : null}
      <ChevronRight className="size-3 shrink-0 text-muted-foreground/50" aria-hidden />
      <span className="truncate text-sm font-medium text-foreground">{nav.entry.label}</span>
    </nav>
  );
}

/**
 * 全局命令位(D4 留位 → A-cmd 真件):触发按钮 + CommandPalette(面板本体
 * 含 ⌘K 自含监听,品类 options 与切换回调自本组件下传/透传)。
 */
