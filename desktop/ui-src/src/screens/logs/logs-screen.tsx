import { useCallback, useEffect, useMemo, useRef, useState } from "react";

import { Card, CardContent } from "@/components/ui/card";
import { SidecarRequestError } from "@/lib/api";
import type { SidecarEvent, UnlistenFn } from "@/lib/api";

import {
  buildRunRows,
  eventToRow,
  filterRunRows,
  loadRunLogs,
  loadRuns,
  rerunRun,
  subscribeRunEvents,
  tailToRows,
} from "./api";
import type { LogRow, LogsRunEntry, RerunState, RunFilterStatus, RunRowModel } from "./api";
import { RunDetailView } from "./run-detail-view";
import { RunListView } from "./run-list-view";

/**
 * 采集日志(10-12-logs-two-level-ui:两级界面重做)。
 *
 * 信息架构(design §1):accordion 内嵌折叠退役,两级下钻——
 *   L1 运行历史(RunListView)= Kestra Executions 表行解剖:每 run 一行直出,
 *     行内「采集了什么」摘要(summarizeRun,只吃 run.status 行);
 *   L2 轮详情(RunDetailView)= Kestra Execution 详情页同物种锚:元信息头 +
 *     失败原因区(三源合成)+ 完整日志体(自动滚底/错误行高亮/复制/搜索)。
 * 动线(design §4):L1 点行 → L2;返回钮 / Esc → L1;过滤态与列表滚动位置
 * 保持;新 running run 不自动跳级(行内状态芯片承担活性,accordion 时代的
 * 自动展开跟随策略整体退役)。
 *
 * 本文件 = 编排层:数据 hooks + 事件订阅 + view state + Esc 全局链 + 过滤态
 * (挂编排层,切级不重置,design §4.2)+ L1 滚动位置捕存回写。
 *
 * 数据面不变(零新协议):run.status + logs.tail(进 L2 才惰性拉取,
 * loadedRunsRef 缓存驻屏)+ sidecar://event 续播;@/lib/api client 零改动。
 * 10-07-logs-restart-visibility R1 合流的「上一程」历史行全家族保留(徽标 /
 * log_run_id 会话对齐拉取 / 旧行无号如实降级 / 撞号 h 前缀防混)。
 */

/** 两级视图状态(feed v8 `FeedView` 判别联合同门,feed-screen.tsx:175-178;
 *  作用域不进路由——App.tsx `Route path="logs"` 零改动,红线内)。
 *  本屏只有两级,无 feed 3→2 的 kind 重派生分支。 */
type LogsView = { level: 1 } | { level: 2; rowKey: string };

export function LogsScreen() {
  const [runs, setRuns] = useState<LogsRunEntry[]>([]);
  /** 逐 run 日志行(键=rowKey):进 L2 时 tail 打底 + 事件续播(未进过的 run
   *  先缓冲,进入时合并,事件比快照新排在 tail 历史之后) */
  const [rowsByRun, setRowsByRun] = useState<Record<string, LogRow[]>>({});
  const [truncatedByRun, setTruncatedByRun] = useState<Record<string, boolean>>({});
  /** 逐 run tail 拉取失败(code:message);成功即清除,重进可重试 */
  const [loadErrors, setLoadErrors] = useState<Record<string, string>>({});
  const [view, setView] = useState<LogsView>({ level: 1 });
  const [live, setLive] = useState(false);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<SidecarRequestError | null>(null);
  const eventSeq = useRef(0);
  /** 已成功 tail 打底的 run(键=rowKey;返回再进不重拉,缓存驻屏,现状语义零改) */
  const loadedRunsRef = useRef<Set<string>>(new Set());
  /** 拉取在途的 run(键=rowKey;防双发) */
  const fetchingRef = useRef<Set<string>>(new Set());
  /** L1 内滚容器 ref + 滚动位置(design §4.2:openRun 时捕 scrollTop,返回
   *  L1 的 effect 回写——feed v8 三级没有做恢复,本档 AC3 明示要求,对 feed
   *  先例的唯一偏离已留档;jsdom 无真实布局不测,无头冒烟断言) */
  const runListRef = useRef<HTMLDivElement | null>(null);
  const l1ScrollTopRef = useRef(0);

  /** run 日志惰性加载(Kestra 步骤展开同款,现状 ensureTail 原样):首次进
   *  L2 才 logs.tail;历史行按 logRunId 会话对齐号拉(旧行 null=不拉,渲染层
   *  如实降级);加载期间到达的事件行已在缓冲,合并时排在 tail 历史之后 */
  const ensureTail = useCallback((run: Pick<RunRowModel, "rowKey" | "logRunId">) => {
    const key = run.rowKey;
    if (loadedRunsRef.current.has(key) || fetchingRef.current.has(key)) return;
    const tailRunId = run.logRunId;
    if (tailRunId === null) return;
    fetchingRef.current.add(key);
    void loadRunLogs(tailRunId)
      .then((tail) => {
        loadedRunsRef.current.add(key);
        setRowsByRun((prev) => ({ ...prev, [key]: [...tailToRows(tail), ...(prev[key] ?? [])] }));
        setTruncatedByRun((prev) => ({ ...prev, [key]: tail.truncated }));
        setLoadErrors((prev) => {
          if (!(key in prev)) return prev;
          const next = { ...prev };
          delete next[key];
          return next;
        });
      })
      .catch((err) => {
        const message = err instanceof SidecarRequestError ? `${err.code} · ${err.message}` : String(err);
        setLoadErrors((prev) => ({ ...prev, [key]: message }));
      })
      .finally(() => {
        fetchingRef.current.delete(key);
      });
  }, []);

  const refreshRuns = useCallback(async () => {
    try {
      const list = await loadRuns();
      setRuns(list);
      // 跟随策略(design §4.3 定稿:默认不自动跳级)——现状「初次进屏自动展开
      // 最新 run / 新 running run 自动展开」(knownRowKeysRef + follow 分支)
      // 是 accordion 时代的跟随遗产,两级 IA 下「自动展开」=「进屏自动跳 L2」,
      // 违反 PRD 默认不自动跳级,整体退役;新 run 活性由 L1 行状态芯片 +
      // completed 触发的列表刷新承担。
    } catch (err) {
      setError(
        err instanceof SidecarRequestError
          ? err
          : new SidecarRequestError({ code: "transport_error", path: "$", message: String(err) }),
      );
    }
  }, []);

  useEffect(() => {
    void (async () => {
      setLoading(true);
      await refreshRuns();
      setLoading(false);
    })();
  }, [refreshRuns]);

  /** 事件流订阅(挂屏一次,不随切级变化,现状原样):任意 run 的事件按 run_id
   *  归组缓冲;completed 另触发列表刷新(终态/耗时落表)。 */
  useEffect(() => {
    let cancelled = false;
    const unlisten: Promise<UnlistenFn> = subscribeRunEvents((event: SidecarEvent) => {
      // 采集日志只续播 run 域事件(log/progress/completed;10-03-vision-pipeline
      // 拆屏后协议已无 image.* 事件,过滤保留为穷尽防御)
      if (event.type !== "log" && event.type !== "progress" && event.type !== "completed") return;
      if (event.type === "completed") {
        void refreshRuns();
      }
      eventSeq.current += 1;
      const row = eventToRow(event, eventSeq.current);
      // run 域事件必带 run_id;null 分支仅为类型穷尽(提取局部量以保持闭包内收窄)。
      // 事件 run_id = 本会话注册表号 → 行键取 `run:` 前缀空间(历史行走 `hist:`,
      // 两编号空间撞号也不串体)
      const runId = row.runId;
      if (runId === null) return;
      const key = `run:${runId}`;
      setRowsByRun((prev) => ({ ...prev, [key]: [...(prev[key] ?? []), row] }));
    }).then((fn) => {
      if (!cancelled) setLive(true);
      return fn;
    });
    unlisten.catch(() => {
      // 事件通道不可用(如浏览器直开):tail 历史仍可用,不拦界面
    });
    return () => {
      cancelled = true;
      setLive(false);
      void unlisten.then((fn) => fn()).catch(() => undefined);
    };
  }, [refreshRuns]);

  // ---- 两级动线(design §4.1)----------------------------------------------

  /** 进 L2:捕 L1 滚动位(§4.2)+ 惰性 tail(§4.1;缓存命中不重拉) */
  const openRun = useCallback(
    (run: RunRowModel) => {
      const el = runListRef.current;
      if (el !== null) l1ScrollTopRef.current = el.scrollTop;
      setView({ level: 2, rowKey: run.rowKey });
      ensureTail(run);
    },
    [ensureTail],
  );

  /** 返回 L1(feed `backLevel` 同名同构;本屏只有两级,无 3→2 重派生分支) */
  const backLevel = useCallback(() => setView({ level: 1 }), []);

  // ---- 过滤(品类·状态,挂编排层,切级不重置 §4.2)+ 搜索(L2 词面)+ 重跑 --

  const [categoryFilter, setCategoryFilter] = useState("all");
  const [statusFilter, setStatusFilter] = useState<RunFilterStatus | "all">("all");
  /** 日志搜索词(挂编排层:输入框在 L2,词面跨切级存活;搜索对象是日志行,
   *  行只在 L2 在场——框不迁则 1 级 50 行 × tail = 协议风暴,design §2.3) */
  const [query, setQuery] = useState("");
  /** 逐 run 重跑反馈(键=rowKey;starting/triggered/error;8s 自动隐去) */
  const [rerunByRun, setRerunByRun] = useState<Record<string, RerunState>>({});
  const rerunTimersRef = useRef<Map<string, ReturnType<typeof setTimeout>>>(new Map());

  const runRows = useMemo(() => buildRunRows(runs), [runs]);
  /** run_id → started_at/finished_at(时间槽用;不进 RunRowModel——api.ts 属
   *  数据层,展示派生留视图层;历史行沿库可空,format* 自兜「—」) */
  const startedAtById = useMemo(
    () => new Map(runs.map((run) => [run.run_id, run.started_at] as const)),
    [runs],
  );
  const finishedAtById = useMemo(
    () => new Map(runs.map((run) => [run.run_id, run.finished_at] as const)),
    [runs],
  );

  const categories = useMemo(() => Array.from(new Set(runRows.map((row) => row.category))).sort(), [runRows]);
  const visibleRunRows = useMemo(
    () => filterRunRows(runRows, categoryFilter, statusFilter),
    [runRows, categoryFilter, statusFilter],
  );
  const filtering = categoryFilter !== "all" || statusFilter !== "all";

  /** 当前 L2 目标行(刷新后行集变动的防御:view 指向的行消失则回落 L1) */
  const detailRun = useMemo(
    () => (view.level === 2 ? (runRows.find((run) => run.rowKey === view.rowKey) ?? null) : null),
    [view, runRows],
  );
  const level = detailRun !== null ? 2 : 1;

  const clearRerunFeedback = useCallback((key: string) => {
    setRerunByRun((prev) => {
      if (!(key in prev)) return prev;
      const next = { ...prev };
      delete next[key];
      return next;
    });
  }, []);

  /** 反馈 8s 自动隐去(定时器挂 ref,卸载统一清) */
  const scheduleRerunClear = useCallback((key: string) => {
    const timers = rerunTimersRef.current;
    const previous = timers.get(key);
    if (previous !== undefined) clearTimeout(previous);
    timers.set(
      key,
      setTimeout(() => {
        timers.delete(key);
        clearRerunFeedback(key);
      }, 8000),
    );
  }, [clearRerunFeedback]);

  useEffect(() => {
    const timers = rerunTimersRef.current;
    return () => {
      for (const timer of timers.values()) clearTimeout(timer);
      timers.clear();
    };
  }, []);

  /**
   * 重跑(G7):骑 G4 手动触发通道 run.start 回放 yaml/dry/db——不新增协议;
   * 成功反馈新 run_id 并刷新列表(L1/L2 双可达,design §2.3;不再有「展开
   * 跟随」——两级 IA 下新 run 落列表,主人点行即达);失败如实报错误码。
   */
  const handleRerun = useCallback(
    (run: RunRowModel) => {
      // 历史行 yaml=null 无从回放(按钮本就不渲染,此为类型收窄守卫)
      if (run.yaml === null) return;
      setRerunByRun((prev) => ({ ...prev, [run.rowKey]: { phase: "starting" } }));
      void rerunRun({ yaml: run.yaml, dry: run.dry, db: run.db })
        .then((started) => {
          setRerunByRun((prev) => ({ ...prev, [run.rowKey]: { phase: "triggered", runId: started.run_id } }));
          scheduleRerunClear(run.rowKey);
          void refreshRuns();
        })
        .catch((err) => {
          const message = err instanceof SidecarRequestError ? `${err.code} · ${err.message}` : String(err);
          setRerunByRun((prev) => ({ ...prev, [run.rowKey]: { phase: "error", message } }));
          scheduleRerunClear(run.rowKey);
        });
    },
    [refreshRuns, scheduleRerunClear],
  );

  const resetFilters = useCallback(() => {
    setCategoryFilter("all");
    setStatusFilter("all");
    setQuery("");
  }, []);

  /** Esc 全局链(design §4.1,feed v8 同门 feed-screen.tsx:3041-3095):仅
   *  2 级响应回 L1,1 级 no-op(不挂 listener)。守卫随迁 feed 先例——
   *  ①焦点在 INPUT/TEXTAREA/SELECT/contentEditable 不抢(输入框 Esc 归清词
   *  自身语义,run-detail-view 框内守卫);②修饰键组合不抢;另随迁 feed 的
   *  defaultPrevented 让位(浮层基件对 Esc 先 preventDefault 放行原生冒泡,
   *  feed-screen.tsx:3046——Radix Select 下拉开着时先关下拉不切级)。
   *  与 feed 的差异如实注明:本屏无菜单/浮层,feed 的 [role="menu"] 第三道
   *  守卫不需要。 */
  useEffect(() => {
    if (level !== 2) return;
    const onKeyDown = (event: KeyboardEvent) => {
      if (event.defaultPrevented) return;
      if (event.metaKey || event.ctrlKey || event.altKey || event.shiftKey) return;
      const target = event.target as HTMLElement | null;
      if (
        target &&
        (target.tagName === "INPUT" ||
          target.tagName === "TEXTAREA" ||
          target.tagName === "SELECT" ||
          target.isContentEditable)
      ) {
        return;
      }
      event.preventDefault();
      backLevel();
    };
    window.addEventListener("keydown", onKeyDown);
    return () => window.removeEventListener("keydown", onKeyDown);
  }, [level, backLevel]);

  /** 返回 L1:回写滚动位置(design §4.2,AC3「列表位置保持」) */
  useEffect(() => {
    if (level !== 1) return;
    const el = runListRef.current;
    if (el !== null && l1ScrollTopRef.current > 0) el.scrollTop = l1ScrollTopRef.current;
  }, [level]);

  return (
    <>
      {/* 结构化错误横幅:挂编排层、互斥分支之上(design §2.3 R2 修正)——
          拆分支后若误钉 L1,L2 在途的 run.status 结构化错误会静默不可见 */}
      {error ? (
        <div className="px-6">
          <Card data-testid="logs-error">
            <CardContent>
              <p className="text-sm font-medium text-destructive">
                采集日志不可用(sidecar 错误码 {error.code})
              </p>
              <p className="mt-1 text-xs text-muted-foreground">{error.message}</p>
            </CardContent>
          </Card>
        </div>
      ) : null}
      {level === 1 || detailRun === null ? (
        <RunListView
          loading={loading}
          allRows={runRows}
          visibleRows={visibleRunRows}
          startedAtById={startedAtById}
          categories={categories}
          categoryFilter={categoryFilter}
          statusFilter={statusFilter}
          onCategoryFilter={setCategoryFilter}
          onStatusFilter={setStatusFilter}
          filtering={filtering}
          onResetFilters={resetFilters}
          refreshing={loading}
          onRefresh={() => void refreshRuns()}
          rerunByRun={rerunByRun}
          onRerun={handleRerun}
          onOpen={openRun}
          listRef={runListRef}
        />
      ) : (
        <RunDetailView
          run={detailRun}
          startedAt={startedAtById.get(detailRun.runId)}
          finishedAt={finishedAtById.get(detailRun.runId)}
          rows={rowsByRun[detailRun.rowKey]}
          truncated={truncatedByRun[detailRun.rowKey] ?? false}
          loadError={loadErrors[detailRun.rowKey] ?? null}
          live={live}
          query={query}
          onQueryChange={setQuery}
          rerun={rerunByRun[detailRun.rowKey]}
          onRerun={handleRerun}
          onBack={backLevel}
        />
      )}
    </>
  );
}
