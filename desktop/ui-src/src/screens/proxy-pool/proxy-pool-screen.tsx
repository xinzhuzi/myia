/**
 * 「代理池」独立屏(task 10-14-proxy-pool-panel R3;路由 /proxy-pool,
 * 侧栏「配置」组——接线见任务档 integrationSpec)。
 *
 * V1 只读面板:出口列表 / 按需测活 / 探测成功率统计。红线全守:
 * - 挂载零网络:进屏只调 proxy.history(纯读),绝不挂载即探测;
 * - 探测只由用户点「探测」触发(零后台探活,D2 归档决议);
 * - 凭据打码到底:上游只以打码 proxy_url 形态渲染,exit_ip 非凭据可显示;
 * - 不写回 pools.yaml(上游增删改属 V2,远期协议缺口);
 * - 健康卡 = 每声明上游一行(非库存大表,MYIA 是手写静态池)。
 *
 * 探测两态照抄 G10 handleProbe(settings-screen.tsx:1000-1008):路径非空
 * 走显式 {config},留空走 {config_auto:true} 由 sidecar 发现
 * <数据目录>/pools.yaml;auto 态未命中(proxy.config=null)的提示行靠
 * probeAutoMiss 屏侧跟踪(应答无新键,doctor-verify.tsx 同款手法)。
 */
import { useCallback, useEffect, useMemo, useState } from "react";
import { Link } from "react-router-dom";

import { PageHeader } from "@/components/layout/page-header";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Skeleton } from "@/components/ui/skeleton";
import { asSidecarError } from "@/screens/settings/api";
import { ErrorBox } from "@/screens/settings/error-box";
import type { SidecarRequestError } from "@/lib/api";

import {
  proxyHistory,
  proxyProbe,
  type ProxyHistoryResult,
  type ProxyPoolRow,
  type ProxyProbeResult,
} from "./api";

/** 历史拉取窗口(与 sidecar 缺省一致;成功率按此窗计算) */
const HISTORY_WINDOW = 20;

/** 按池分组(保池首次出现序;池内按 upstream_index 保序,缺键稳原序) */
function groupByPool(rows: ProxyPoolRow[]): { name: string; rows: ProxyPoolRow[] }[] {
  const order: string[] = [];
  const buckets = new Map<string, ProxyPoolRow[]>();
  for (const row of rows) {
    const name = row.pool ?? "?";
    let bucket = buckets.get(name);
    if (!bucket) {
      bucket = [];
      buckets.set(name, bucket);
      order.push(name);
    }
    bucket.push(row);
  }
  return order.map((name) => ({
    name,
    rows: [...(buckets.get(name) ?? [])].sort(
      (a, b) => (a.upstream_index ?? 0) - (b.upstream_index ?? 0),
    ),
  }));
}

/** 出口 IP 渲染值:null / undefined(兜底行缺键)统一显「—」 */
function exitIpText(row: ProxyPoolRow): string {
  return row.exit_ip ?? "—";
}

/** 历史窗口内每池探测成功率(= ok 行数 / 该池总行数;探测口径,非流量) */
function poolRates(history: ProxyHistoryResult): { name: string; ok: number; total: number }[] {
  const order: string[] = [];
  const stats = new Map<string, { ok: number; total: number }>();
  for (const snapshot of history.snapshots) {
    for (const row of snapshot.pools) {
      const name = row.pool ?? "?";
      let entry = stats.get(name);
      if (!entry) {
        entry = { ok: 0, total: 0 };
        stats.set(name, entry);
        order.push(name);
      }
      entry.total += 1;
      if (row.ok === true) entry.ok += 1;
    }
  }
  return order.map((name) => ({ name, ...stats.get(name)! }));
}

/** 探测行三态徽章(连通·延迟 / 不通 / 未探测;doctor-verify.tsx:157-163 同款) */
function PoolRowBadge({ row }: { row: ProxyPoolRow }) {
  if (row.ok === true) {
    return (
      <Badge variant="ok">
        连通{typeof row.latency_seconds === "number" ? ` · ${row.latency_seconds}s` : ""}
      </Badge>
    );
  }
  if (row.ok === false) return <Badge variant="destructive">不通</Badge>;
  return <Badge variant="unknown">未探测</Badge>;
}

/** 单上游健康行:打码 URL + 三态徽章 + 出口 IP + 人话原因 + 错误类短标签 */
function UpstreamRow({ row }: { row: ProxyPoolRow }) {
  return (
    <li
      className="flex flex-wrap items-center gap-x-3 gap-y-1 rounded-sm bg-muted/30 px-2 py-1.5 text-xs"
      data-testid="proxy-upstream-row"
    >
      <span className="max-w-56 truncate font-mono text-foreground" title={row.proxy_url ?? ""}>
        {row.proxy_url ?? "—"}
      </span>
      <PoolRowBadge row={row} />
      <span className="text-muted-foreground" data-testid="proxy-exit-ip">
        出口 IP:{exitIpText(row)}
      </span>
      {row.message ? (
        <span className="min-w-0 flex-1 truncate text-muted-foreground" title={row.message}>
          {row.message}
        </span>
      ) : null}
      {row.error_type ? (
        <Badge variant="outline" className="font-mono" title={`错误类型:${row.error_type}`}>
          {row.error_type}
        </Badge>
      ) : null}
    </li>
  );
}

export function ProxyPoolScreen() {
  const [history, setHistory] = useState<ProxyHistoryResult | null>(null);
  const [historyError, setHistoryError] = useState<SidecarRequestError | null>(null);
  const [probePath, setProbePath] = useState("");
  const [probing, setProbing] = useState(false);
  const [probeResult, setProbeResult] = useState<ProxyProbeResult | null>(null);
  const [probeError, setProbeError] = useState<SidecarRequestError | null>(null);
  /** G10 同款:auto 态屏侧跟踪(挂载/初始不发 config_auto,不冒「未找到」) */
  const [probeAutoMiss, setProbeAutoMiss] = useState(false);

  const loadHistory = useCallback(async () => {
    setHistoryError(null);
    try {
      setHistory(await proxyHistory({ limit: HISTORY_WINDOW }));
    } catch (error) {
      setHistoryError(asSidecarError(error));
    }
  }, []);

  // 挂载零网络红线:进屏只读历史,绝不探测
  useEffect(() => {
    void loadHistory();
  }, [loadHistory]);

  const handleProbe = useCallback(async () => {
    const path = probePath.trim();
    setProbeAutoMiss(!path);
    setProbing(true);
    setProbeError(null);
    try {
      const result = await proxyProbe(path ? { config: path } : { config_auto: true });
      setProbeResult(result);
      await loadHistory(); // 落了快照(persisted)→ 历史区即刷
    } catch (error) {
      setProbeError(asSidecarError(error));
    } finally {
      setProbing(false);
    }
  }, [probePath, loadHistory]);

  /** 总览/池卡数据源:本屏探测应答优先,回看时用历史最新快照(只读投影) */
  const overview = useMemo(() => {
    if (probeResult) {
      return { pools: probeResult.proxy.pools, at: probeResult.generated_at };
    }
    const newest = history?.snapshots[0];
    if (newest) return { pools: newest.pools, at: newest.at };
    return null;
  }, [probeResult, history]);

  const overviewStats = useMemo(() => {
    const rows = overview?.pools ?? [];
    return {
      poolCount: groupByPool(rows).length,
      upstreamCount: rows.length,
      ok: rows.filter((row) => row.ok === true).length,
      bad: rows.filter((row) => row.ok === false).length,
      unknown: rows.filter((row) => row.ok !== true && row.ok !== false).length,
    };
  }, [overview]);

  const rates = useMemo(() => (history ? poolRates(history) : []), [history]);
  const autoMissHint =
    probeAutoMiss && probeResult !== null && probeResult.proxy.config === null;

  return (
    <div className="flex flex-col gap-block pb-block">
      <PageHeader
        title="代理池"
        description="出口列表 / 按需测活 / 探测成功率统计(只读;池凭据归 设置 · 代理池 卡入钥匙串)"
      />
      <div className="flex flex-col gap-card px-6">
        {/* 头部·配置与探测 */}
        <Card>
          <CardHeader>
            <CardTitle>配置与探测</CardTitle>
            <CardDescription>
              探测只在你点按钮时发生(进屏不探测);结果存入本机历史,供成功率统计
            </CardDescription>
          </CardHeader>
          <CardContent className="flex flex-col gap-2">
            <div className="flex flex-wrap items-center gap-2">
              <Input
                className="min-w-64 max-w-md flex-1"
                aria-label="全局 pools YAML 路径"
                placeholder="留空=自动探测 <数据目录>/pools.yaml"
                value={probePath}
                onChange={(event) => setProbePath(event.target.value)}
                data-testid="proxy-config-input"
              />
              <Button size="sm" onClick={() => void handleProbe()} disabled={probing} data-testid="proxy-probe-button">
                探测
              </Button>
              {probing ? (
                <span className="text-xs text-muted-foreground" data-testid="probe-waiting">
                  探测进行中,逐上游测试最长约 2 分钟,请稍候…
                </span>
              ) : null}
            </div>
            {probeError ? <ErrorBox error={probeError} onRetry={() => void handleProbe()} retrying={probing} /> : null}
            {probeResult?.proxy.config ? (
              <p className="font-mono text-2xs text-muted-foreground" data-testid="proxy-config-path">
                已加载配置:{probeResult.proxy.config}
              </p>
            ) : null}
            {autoMissHint ? (
              <p className="text-xs text-muted-foreground" data-testid="proxy-auto-miss">
                未找到缺省 pools.yaml——可在上方填入全局配置路径后重探,或
                <Link to="/settings" className="mx-1 text-primary underline underline-offset-2">
                  去设置屏 · 代理池卡
                </Link>
                入凭据
              </p>
            ) : null}
            {probeResult && !probeResult.snapshot.persisted ? (
              <p className="text-xs text-muted-foreground" data-testid="probe-not-persisted">
                {probeResult.snapshot.reason === "no_home"
                  ? "开发模式无数据根:本次探测结果不落历史"
                  : `本次探测结果未落历史(原因:${probeResult.snapshot.reason ?? "未知"})`}
              </p>
            ) : null}
          </CardContent>
        </Card>

        {historyError ? <ErrorBox error={historyError} onRetry={() => void loadHistory()} /> : null}

        {/* 总览卡(借 jhao104 /count 的分组聚合形态,纯应答形状借用) */}
        <Card>
          <CardHeader>
            <CardTitle>总览</CardTitle>
            <CardDescription>
              最近一次探测的分组计数{overview ? `(${overview.at})` : ""}
            </CardDescription>
          </CardHeader>
          <CardContent className="flex flex-col gap-2">
            {overview === null && historyError === null ? (
              <Skeleton className="h-6 w-64" aria-label="历史读取中" />
            ) : null}
            {overview ? (
              <div className="flex flex-wrap items-center gap-x-4 gap-y-1 text-xs" data-testid="proxy-overview">
                <span>
                  池数 <span className="font-medium text-foreground">{overviewStats.poolCount}</span>
                </span>
                <span title="按探测应答行计数;凭据缺失的池只回一行兜底,声明数以 pools.yaml 为准">
                  已解析上游 <span className="font-medium text-foreground">{overviewStats.upstreamCount}</span>
                </span>
                <span>
                  可用 <span className="font-medium text-ok">{overviewStats.ok}</span>
                </span>
                <span>
                  不通 <span className="font-medium text-destructive">{overviewStats.bad}</span>
                </span>
                <span>
                  未探测 <span className="font-medium text-unknown">{overviewStats.unknown}</span>
                </span>
              </div>
            ) : null}
            {!overview && !historyError ? (
              <p className="text-xs text-muted-foreground">尚未探测——点上方「探测」查看池现状</p>
            ) : null}
          </CardContent>
        </Card>

        {/* 每池健康卡(非库存表:MYIA 是手写静态池,每声明上游一张行) */}
        {overview && overviewStats.poolCount > 0
          ? groupByPool(overview.pools).map((pool) => (
              <Card key={pool.name} data-testid={`proxy-pool-card-${pool.name}`}>
                <CardHeader>
                  <CardTitle className="font-mono">{pool.name}</CardTitle>
                  <CardDescription>{pool.rows.length} 个上游(按声明顺序)</CardDescription>
                </CardHeader>
                <CardContent>
                  <ul className="flex flex-col gap-1">
                    {pool.rows.map((row, index) => (
                      <UpstreamRow key={`${pool.name}-${row.upstream_index ?? index}`} row={row} />
                    ))}
                  </ul>
                </CardContent>
              </Card>
            ))
          : null}

        {/* 探测历史区(只读;口径红线 3 + 拷问修正③) */}
        <Card>
          <CardHeader>
            <CardTitle>探测历史</CardTitle>
            <CardDescription>
              探测成功率(非流量成功率)——doctor 轻探测的通过占比,不代表真实流量成功率;仅记本屏发起的探测(设置屏的探测不落历史)
            </CardDescription>
          </CardHeader>
          <CardContent className="flex flex-col gap-2">
            {history === null && historyError === null ? <Skeleton className="h-6 w-64" /> : null}
            {history && history.home_available === false ? (
              <p className="text-xs text-muted-foreground" data-testid="proxy-history-dev-nohome">
                开发模式无数据根:探测可用,但历史不落盘(成功率统计需要打包/安装形态)
              </p>
            ) : null}
            {history && history.home_available && history.count === 0 ? (
              <p className="text-xs text-muted-foreground" data-testid="proxy-history-empty">
                尚无探测记录,点上方探测开始
              </p>
            ) : null}
            {rates.length > 0 ? (
              <div className="flex flex-col gap-1.5" data-testid="proxy-history-rates">
                {rates.map((rate) => {
                  const pct = rate.total > 0 ? Math.round((rate.ok / rate.total) * 100) : 0;
                  return (
                    <div key={rate.name} className="flex items-center gap-2 text-xs" data-testid="proxy-history-rate">
                      <span className="w-24 shrink-0 truncate font-mono text-foreground" title={rate.name}>
                        {rate.name}
                      </span>
                      <div className="h-1.5 w-40 shrink-0 rounded bg-muted" aria-hidden>
                        <div className="h-1.5 rounded bg-ok" style={{ width: `${pct}%` }} />
                      </div>
                      <span className="text-muted-foreground">
                        探测成功率 {pct}%({rate.ok}/{rate.total})
                      </span>
                    </div>
                  );
                })}
                {history?.truncated ? (
                  <p className="text-2xs text-muted-foreground">
                    更早的探测未拉取(窗口最近 {HISTORY_WINDOW} 条)
                  </p>
                ) : null}
                {history?.skipped ? (
                  <p className="text-2xs text-muted-foreground">历史文件有 {history.skipped} 行损坏已跳过</p>
                ) : null}
              </div>
            ) : null}
            {history && history.count > 0 ? (
              <ul className="flex flex-col gap-0.5">
                {history.snapshots.map((snapshot) => (
                  <li
                    key={snapshot.at}
                    className="flex flex-wrap items-center gap-x-3 text-2xs text-muted-foreground"
                    data-testid="proxy-history-snapshot"
                  >
                    <span className="font-mono">{snapshot.at}</span>
                    <span className="max-w-72 truncate font-mono" title={snapshot.config ?? ""}>
                      {snapshot.config ?? "(自动探测)"}
                    </span>
                    <span>{snapshot.pools.length} 行</span>
                  </li>
                ))}
              </ul>
            ) : null}
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
