/**
 * 凭证猎手屏(V1 只读,10-14-cred-hunter-panel):本地密钥库
 * (`credhunter-keystore.json`)的掩码-only 只读表格 —— 全部密钥 / 高危两
 * 视图 + 六列表格 + 行展开证据,零网络、零凭据暴露面扩大。
 *
 * 布局与行为思想对标 aipocket AllKeysPage/HighValuePage(AGPL,只借思想:
 * 列模型/过滤工具条/徽章分层/列宽持久化,零代码零上游标识符零上游文案,
 * PRD §2 判例);渲染骨架沿用本仓 sources 屏范式(Kestra KSFilter 工具条 +
 * TanStack Table 引擎 + ui/table 渲染层 + 列宽拖拽)。
 *
 * 红线(PRD §2 G11 三不借,永久不做):无导出、无全文 reveal/复制、不拿
 * 猎得键实测对话。协议面只含服务端算好的 masked_apikey,本屏不含任何
 * 复制/查看动作。V2 交互(验证触发/余额持久化/状态流转)全部不做。
 */
import { flexRender, getCoreRowModel, useReactTable, type ColumnDef } from "@tanstack/react-table";
import { ChevronDown, ChevronRight, RefreshCw, Search } from "lucide-react";
import { useCallback, useEffect, useMemo, useState } from "react";

import { EmptyState } from "@/components/empty-state";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Skeleton } from "@/components/ui/skeleton";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { cn } from "@/lib/utils";
import type { SidecarRequestError } from "@/lib/api";

import { ErrorBox } from "../settings/error-box";
import {
  asSidecarError,
  checkStateView,
  fetchCredhunterKeys,
  filterHighRisk,
  filterKeyRecords,
  formatDay,
  formatDateTime,
  KEY_SORT_MODES,
  loadColumnSizes,
  providerCounts,
  saveColumnSizes,
  sortKeyRecords,
} from "./api";
import type { CredhunterKeyRecord, CredhunterKeysListResult, KeySortMode } from "./api";

/** 载/错/就绪三态(discriminated union,error 分支 error 必非空) */
type LoadState =
  | { status: "loading"; data: null; error: null }
  | { status: "error"; data: null; error: SidecarRequestError }
  | { status: "ready"; data: CredhunterKeysListResult; error: null };

/** 视图档:全部密钥(缺省,全量 records)/ 高危(判据 api.ts HIGH_RISK_STATES) */
type KeyView = "all" | "high";

const KEY_VIEWS: { value: KeyView; label: string }[] = [
  { value: "all", label: "全部密钥" },
  { value: "high", label: "高危" },
];

/** 行展开区 id(证据列 aria-controls 引用) */
const detailRowId = (fingerprint: string) => `credhunter-key-detail-${fingerprint}`;

/** 传给单元格的回调集合(TanStack table.options.meta 惯例,sources 屏同款) */
interface CredhunterTableMeta {
  /** 已展开行(fingerprint 键) */
  expandedKeys: ReadonlySet<string>;
  toggleExpanded: (fingerprint: string) => void;
}

/**
 * 六列(PRD §3.3,列集固定):密钥 / 供应商 / 验证状态 / 命中 / 证据 /
 * 最近检查。无余额列(数据面无持久余额,不做假列);列宽可拖拽,size 与
 * minSize 为初始值与下限。**密钥列无任何复制/查看动作**(G11 红线)。
 */
const COLUMNS: ColumnDef<CredhunterKeyRecord>[] = [
  {
    id: "masked",
    accessorKey: "masked_apikey",
    header: "密钥",
    size: 240,
    minSize: 160,
    enableSorting: false,
    cell: ({ row }) => (
      <div className="min-w-0" title={row.original.fingerprint}>
        <div className="truncate font-mono text-sm text-foreground">{row.original.masked_apikey}</div>
        <div className="truncate font-mono text-2xs text-muted-foreground">{row.original.fingerprint}</div>
      </div>
    ),
  },
  {
    id: "provider",
    accessorKey: "provider",
    header: "供应商",
    size: 110,
    minSize: 76,
    enableSorting: false,
    cell: ({ row }) => (
      <Badge variant="secondary">{String(row.original.provider ?? "") || "未知"}</Badge>
    ),
  },
  {
    id: "state",
    accessorFn: (row) => row.check_state ?? "",
    header: "验证状态",
    size: 110,
    minSize: 90,
    enableSorting: false,
    cell: ({ row }) => {
      const view = checkStateView(row.original.check_state);
      return <Badge variant={view.variant}>{view.label}</Badge>;
    },
  },
  {
    id: "hits",
    accessorKey: "hit_count",
    header: "命中",
    size: 150,
    minSize: 110,
    enableSorting: false,
    cell: ({ row }) => (
      <div className="min-w-0">
        <span className="text-sm tabular-nums text-foreground">{row.original.hit_count}</span>
        <div className="truncate text-2xs text-muted-foreground" title={`${row.original.first_seen} → ${row.original.last_seen}`}>
          {formatDay(row.original.first_seen)} → {formatDay(row.original.last_seen)}
        </div>
      </div>
    ),
  },
  {
    id: "sources",
    accessorFn: (row) => (row.sources ?? []).length,
    header: "证据",
    size: 96,
    minSize: 72,
    enableSorting: false,
    cell: ({ row, table }) => {
      const meta = table.options.meta as CredhunterTableMeta;
      const expanded = meta.expandedKeys.has(row.original.fingerprint);
      const count = (row.original.sources ?? []).length;
      return (
        <button
          type="button"
          aria-expanded={expanded}
          aria-controls={detailRowId(row.original.fingerprint)}
          aria-label={`${expanded ? "收起" : "展开"}证据 ${row.original.fingerprint}`}
          onClick={() => meta.toggleExpanded(row.original.fingerprint)}
          className="inline-flex h-7 items-center gap-1 rounded-md px-1.5 text-xs transition-colors duration-(--duration-fast) ease-out-expo hover:text-foreground"
        >
          {expanded ? <ChevronDown className="size-3" /> : <ChevronRight className="size-3" />}
          <span className="tabular-nums">{count} 条</span>
        </button>
      );
    },
  },
  {
    id: "last_check",
    accessorKey: "last_check",
    header: "最近检查",
    size: 130,
    minSize: 96,
    enableSorting: false,
    cell: ({ row }) =>
      row.original.last_check ? (
        <span className="text-sm tabular-nums" title={row.original.last_check}>
          {formatDateTime(row.original.last_check)}
        </span>
      ) : (
        <span className="text-xs text-muted-foreground">未验证</span>
      ),
  },
];

/** 库未建空态文案(PRD §3.3,逐字) */
const KEYSTORE_ABSENT_TITLE = "凭证猎手还没有密钥库";
const KEYSTORE_ABSENT_DESCRIPTION =
  "猎手(credhunt)尚未运行或尚无命中。可在品类 YAML 启用 engine: credhunter 源后跑一轮采集";

/**
 * 凭证猎手屏:一次 fetchCredhunterKeys 拉全量(纯文件读,零网络),视图/
 * 搜索/供应商过滤/排序全在客户端前置派生(纯函数在 api.ts,可单测);
 * TanStack Table 只作列宽引擎(拖拽 + localStorage 持久化)。
 */
export function CredhunterScreen() {
  const [state, setState] = useState<LoadState>({ status: "loading", data: null, error: null });
  const [refreshing, setRefreshing] = useState(false);
  const [view, setView] = useState<KeyView>("all");
  const [query, setQuery] = useState("");
  const [sortMode, setSortMode] = useState<KeySortMode>("hits");
  /** 供应商 chips 多选(空 = 全量;与搜索正交叠加) */
  const [providerFilter, setProviderFilter] = useState<Set<string>>(new Set());
  const [expandedKeys, setExpandedKeys] = useState<Set<string>>(new Set());

  const reload = useCallback(async () => {
    setRefreshing(true);
    setState((prev) =>
      prev.status === "ready" ? { ...prev, error: null } : { status: "loading", data: null, error: null },
    );
    try {
      const data = await fetchCredhunterKeys();
      setState({ status: "ready", data, error: null });
    } catch (error) {
      setState({ status: "error", data: null, error: asSidecarError(error) });
    } finally {
      setRefreshing(false);
    }
  }, []);

  useEffect(() => {
    void reload();
  }, [reload]);

  const toggleExpanded = useCallback((fingerprint: string) => {
    setExpandedKeys((prev) => {
      const next = new Set(prev);
      if (next.has(fingerprint)) next.delete(fingerprint);
      else next.add(fingerprint);
      return next;
    });
  }, []);

  const records = state.data?.records ?? [];

  // 视图作用域(高危判据在 api.ts 单点常量);chips 计数也从视图作用域聚合
  const scoped = useMemo(() => (view === "high" ? filterHighRisk(records) : records), [view, records]);
  const providers = useMemo(() => providerCounts(scoped), [scoped]);
  const searched = useMemo(() => filterKeyRecords(scoped, query), [scoped, query]);
  const visible = useMemo(
    () =>
      providerFilter.size === 0
        ? searched
        : searched.filter((record) => providerFilter.has(String(record.provider ?? ""))),
    [searched, providerFilter],
  );
  const rows = useMemo(() => sortKeyRecords(visible, sortMode), [visible, sortMode]);

  const table = useReactTable({
    data: rows,
    columns: COLUMNS,
    getCoreRowModel: getCoreRowModel(),
    // 列宽非受控(sources 屏同形态):initialState 还原 localStorage 快照,
    // 拖拽由引擎自管;渲染期读 table.getState().columnSizing 持久化(下 effect)
    initialState: { columnSizing: loadColumnSizes() },
    columnResizeMode: "onChange",
    meta: { expandedKeys, toggleExpanded } satisfies CredhunterTableMeta,
  });

  // 列宽持久化:拖拽中每次变更即写(六列 JSON,量小;写失败不阻断)
  useEffect(() => {
    saveColumnSizes(table.getState().columnSizing);
  });

  const headers = table.getHeaderGroups()[0]?.headers ?? [];
  const leafColumns = table.getVisibleLeafColumns();
  const resizing = table.getState().columnSizingInfo.isResizingColumn !== false;

  // 过滤是否被用户收窄(决定「无匹配」与视图空态的文案取舍)
  const filtersActive = query.trim() !== "" || providerFilter.size > 0;

  return (
    <div className="flex h-full min-h-0 flex-col gap-3 px-6 pb-6">
      {/* 头部:视图切换 Segment + 只读说明 + 刷新(sources 工具条范式) */}
      <div className="flex flex-wrap items-center justify-between gap-2">
        <div className="flex items-center gap-3">
          <div
            role="group"
            aria-label="密钥视图"
            className="flex items-center gap-0.5 rounded-lg border border-border bg-muted/40 p-0.5"
          >
            {KEY_VIEWS.map(({ value, label }) => {
              const active = view === value;
              return (
                <button
                  key={value}
                  type="button"
                  aria-pressed={active}
                  onClick={() => setView(value)}
                  className={
                    "h-7 rounded-md px-2.5 text-xs transition-colors duration-(--duration-fast) ease-out-expo " +
                    (active
                      ? "bg-accent font-medium text-foreground shadow-sm"
                      : "text-muted-foreground hover:text-foreground")
                  }
                >
                  {label}
                </button>
              );
            })}
          </div>
          <span className="text-2xs text-muted-foreground">本地密钥库只读视图 · 密钥仅掩码显示</span>
        </div>
        <Button
          size="icon"
          variant="ghost"
          className="size-8"
          aria-label="刷新"
          title="重读本地密钥库"
          disabled={refreshing}
          onClick={() => void reload()}
        >
          <RefreshCw className={refreshing ? "size-3.5 animate-spin" : "size-3.5"} />
        </Button>
      </div>

      {/* 工具条:搜索 + 排序切换 */}
      <div className="flex flex-wrap items-center justify-between gap-2">
        <div className="relative w-64">
          <Search
            aria-hidden
            className="pointer-events-none absolute top-1/2 left-2.5 size-3.5 -translate-y-1/2 text-muted-foreground/70"
          />
          <Input
            value={query}
            onChange={(event) => setQuery(event.target.value)}
            placeholder="搜索:掩码 / 供应商…"
            aria-label="搜索密钥"
            className="pl-8"
          />
        </div>
        <div
          role="group"
          aria-label="排序方式"
          className="flex items-center gap-0.5 rounded-lg border border-border bg-muted/40 p-0.5"
        >
          {KEY_SORT_MODES.map(({ value, label }) => {
            const active = sortMode === value;
            return (
              <button
                key={value}
                type="button"
                aria-pressed={active}
                onClick={() => setSortMode(value)}
                className={
                  "h-7 rounded-md px-2.5 text-xs transition-colors duration-(--duration-fast) ease-out-expo " +
                  (active
                    ? "bg-accent font-medium text-foreground shadow-sm"
                    : "text-muted-foreground hover:text-foreground")
                }
              >
                {label}
              </button>
            );
          })}
        </div>
      </div>

      {/* 供应商 chips(当前视图记录聚合计数;单供应商无筛选意义不渲染) */}
      {state.status === "ready" && providers.length > 1 ? (
        <div role="group" aria-label="按供应商筛选" className="flex flex-wrap items-center gap-1.5">
          {providers.map(({ provider, count }) => {
            const active = providerFilter.has(provider);
            return (
              <button
                key={provider}
                type="button"
                aria-pressed={active}
                aria-label={`${provider}(${count} 个密钥)`}
                onClick={() =>
                  setProviderFilter((prev) => {
                    const next = new Set(prev);
                    if (next.has(provider)) next.delete(provider);
                    else next.add(provider);
                    return next;
                  })
                }
                className={
                  "inline-flex h-7 items-center gap-1.5 rounded-md border px-2.5 text-xs transition-colors duration-(--duration-fast) ease-out-expo " +
                  (active
                    ? "border-primary/40 bg-accent font-medium text-foreground shadow-sm"
                    : "border-border bg-muted/30 text-muted-foreground hover:text-foreground")
                }
              >
                <span className="max-w-40 truncate">{provider || "未知"}</span>
                <span
                  aria-hidden
                  className={
                    "inline-flex min-w-4 items-center justify-center rounded px-1 text-2xs leading-4 tabular-nums " +
                    (active ? "bg-primary/15 text-foreground" : "bg-muted text-muted-foreground")
                  }
                >
                  {count}
                </span>
              </button>
            );
          })}
          {providerFilter.size > 0 ? (
            <button
              type="button"
              onClick={() => setProviderFilter(new Set())}
              className="h-7 rounded-md px-1.5 text-xs text-muted-foreground underline-offset-2 transition-colors duration-(--duration-fast) ease-out-expo hover:text-foreground hover:underline"
            >
              清除
            </button>
          ) : null}
        </div>
      ) : null}

      {/* 主体:载 / 错 / 空 / 表 四态互斥(feed 屏范式) */}
      {state.status === "loading" ? (
        <div className="flex flex-col gap-2" data-testid="credhunter-loading">
          <Skeleton className="h-9 w-full" />
          <Skeleton className="h-9 w-full" />
          <Skeleton className="h-9 w-2/3" />
        </div>
      ) : state.status === "error" ? (
        <ErrorBox error={state.error} onRetry={() => void reload()} retrying={refreshing} />
      ) : state.data === null ? null : !state.data.exists ? (
        <EmptyState
          title={KEYSTORE_ABSENT_TITLE}
          description={KEYSTORE_ABSENT_DESCRIPTION}
          tag="只读"
        />
      ) : records.length === 0 ? (
        <EmptyState
          title="密钥库还没有记录"
          description={KEYSTORE_ABSENT_DESCRIPTION}
          tag="只读"
        />
      ) : rows.length === 0 ? (
        view === "high" && !filtersActive ? (
          <EmptyState compact title="没有已验证存活的泄漏凭证" tag="高危" />
        ) : (
          <EmptyState
            compact
            title="无匹配结果"
            description={filtersActive ? "换个搜索词或清除供应商过滤试试" : undefined}
            action={
              filtersActive ? (
                <Button
                  variant="outline"
                  size="sm"
                  onClick={() => {
                    setQuery("");
                    setProviderFilter(new Set());
                  }}
                >
                  清除过滤
                </Button>
              ) : undefined
            }
          />
        )
      ) : (
        <>
          <div className="min-h-0 flex-1 overflow-y-auto overflow-x-hidden rounded-lg border border-border">
            <Table className={cn("table-fixed", resizing && "select-none")} aria-label="密钥列表">
              {/* 列宽拖拽:首列(密钥)不定宽吃剩余,其余列渲染 getSize() 原值 */}
              <colgroup>
                {leafColumns.map((column, index) =>
                  index === 0 ? (
                    <col key={column.id} />
                  ) : (
                    <col key={column.id} style={{ width: column.getSize() }} />
                  ),
                )}
              </colgroup>
              <TableHeader className="bg-muted/30">
                <TableRow className="hover:bg-transparent">
                  {headers.map((header, index) => (
                    <TableHead
                      key={header.id}
                      style={index === 0 ? undefined : { width: header.getSize() }}
                      className="relative"
                    >
                      <span className="flex items-center gap-1">
                        {flexRender(header.column.columnDef.header, header.getContext())}
                      </span>
                      <span
                        aria-hidden
                        data-column-resize-handle={header.id}
                        onPointerDown={header.getResizeHandler()}
                        onDoubleClick={() => header.column.resetSize()}
                        onClick={(event) => event.stopPropagation()}
                        className="group absolute inset-y-0 right-0 z-10 flex w-2 cursor-col-resize touch-none items-stretch justify-center"
                      >
                        <span
                          className={cn(
                            "h-full w-px bg-border transition-colors duration-(--duration-fast) ease-out-expo",
                            "group-hover:bg-primary",
                            header.column.getIsResizing() && "bg-primary",
                          )}
                        />
                      </span>
                    </TableHead>
                  ))}
                </TableRow>
              </TableHeader>
              <TableBody>
                {table.getRowModel().rows.flatMap((row) => [
                  <TableRow key={row.id}>
                    {row.getVisibleCells().map((cell) => (
                      <TableCell key={cell.id}>{flexRender(cell.column.columnDef.cell, cell.getContext())}</TableCell>
                    ))}
                  </TableRow>,
                  expandedKeys.has(row.original.fingerprint) ? (
                    <TableRow key={`${row.id}-detail`} className="hover:bg-transparent" id={detailRowId(row.original.fingerprint)}>
                      <TableCell colSpan={row.getVisibleCells().length} className="whitespace-normal p-0">
                        <div className="bg-muted/20 px-4 py-3">
                          <div className="flex flex-col gap-1 font-mono text-2xs text-muted-foreground">
                            <span>指纹 {row.original.fingerprint}</span>
                            <span>
                              首次发现 {formatDateTime(row.original.first_seen)} · 最近发现{" "}
                              {formatDateTime(row.original.last_seen)} · 最近检查 {formatDateTime(row.original.last_check)}
                            </span>
                          </div>
                          <div className="mt-2 flex flex-col gap-0.5">
                            <span className="text-2xs text-muted-foreground">
                              证据来源({(row.original.sources ?? []).length})
                            </span>
                            {(row.original.sources ?? []).map((url) => (
                              <span key={url} className="truncate font-mono text-2xs text-foreground" title={url}>
                                {url}
                              </span>
                            ))}
                          </div>
                        </div>
                      </TableCell>
                    </TableRow>
                  ) : null,
                ])}
              </TableBody>
            </Table>
          </div>
          <div className="flex items-center justify-between text-2xs text-muted-foreground">
            <span>{`共 ${rows.length} 条${rows.length !== records.length ? `(全部 ${records.length} 条)` : ""}`}</span>
            <span className="font-mono" title={state.data.path}>
              {state.data.path}
            </span>
          </div>
        </>
      )}
    </div>
  );
}
