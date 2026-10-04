import { useEffect, useState } from "react";
import { Search } from "lucide-react";
import { useLocation } from "react-router-dom";

import { CommandPalette } from "@/components/layout/command-palette";
import { resolveNav } from "@/components/layout/sidebar";
import { api } from "@/lib/api";

/** 品类选项(命令面板「切换品类」清单;health().plugins 的 id 去重 + 名称回显) */
interface CategoryOption {
  id: string;
  label: string;
}

/** 命令位快捷键文案:macOS ⌘K,其余平台 Ctrl K(桌面跨平台惯例) */
const COMMAND_KEY =
  typeof navigator !== "undefined" && /Mac|iPhone|iPad/.test(navigator.platform ?? "") ? "⌘K" : "Ctrl K";

/**
 * 顶栏(壳层清理后极简形态):左侧仅当前屏标题(与侧栏导航同一解析口径),
 * 右侧仅 ⌘K 命令面板的图标触发器。已拆除:品牌字/面包屑(侧栏已有品牌 +
 * 导航,顶栏重复)、品类下拉与全局跑一次(后续由 feed/sources 屏自放
 * 上下文版)、假搜索框(触发器收为图标按钮,不占宽)。品类全局态仍由
 * AppLayout 持有并经 Outlet context 下发,命令面板内仍可切换品类
 * (options 清单自本组件 health() 取得,透传面板)。
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
  const location = useLocation();
  const nav = resolveNav(location.pathname);

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
        // health 失败不拦顶栏:品类清单收敛为空,命令面板仅「全部品类」
        if (!cancelled) setOptions([]);
      });
    return () => {
      cancelled = true;
    };
  }, []);

  return (
    <header className="flex h-12 shrink-0 items-center border-b border-border bg-background/80">
      {/* 栅格:顶栏内容列与 main 同一收束(max-w-content)+ 同一 px-6,
          屏标题左缘 = 内容左缘,两线对齐(Linear 顶栏/内容同栅格) */}
      <div className="mx-auto flex h-full w-full max-w-content items-center gap-3 px-6">
        {/* 屏标题:当前路由在侧栏导航口径下的页面名,仅此一段(无面包屑) */}
        {nav ? (
          <span className="truncate text-sm font-medium text-foreground">{nav.entry.label}</span>
        ) : null}

        <div className="flex-1" />

        {/* ⌘K 命令面板图标触发器:无假输入框占宽,仅一个方形图标钮
            (可达语义与 command-palette.test.tsx「top-bar 接线」节对齐) */}
        <button
          type="button"
          aria-haspopup="dialog"
          aria-expanded={paletteOpen}
          aria-label="打开命令面板"
          title={`命令面板(${COMMAND_KEY}:导航/跑一次/刷新/切品类)`}
          onClick={() => setPaletteOpen(true)}
          className="flex size-7 cursor-pointer items-center justify-center rounded-md border border-(--control-border) bg-(--control-bg) text-muted-foreground outline-none transition-colors duration-(--duration-fast) ease-out-expo hover:border-(--control-border) hover:bg-(--control-bg-hover) hover:text-foreground focus-visible:ring-[3px] focus-visible:ring-ring/40"
        >
          <Search className="size-3.5 shrink-0" aria-hidden />
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
