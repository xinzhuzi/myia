import { HardDrive, RefreshCw, Trash2 } from "lucide-react";
import { useCallback, useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";

import { pyenvGetStatus } from "./pyenv-api";
import { SettingRow } from "./settings-row";
import { reclaimStorage, storageUsage, type StorageUsage } from "./storage-api";

/**
 * 「磁盘占用」分区卡(10-14-leftover-sweep-install storage 域):只读占用
 * 视图(数据根全量逻辑字节,含隐藏文件;顶层文件全聚合、未知目录归
 * 「其余」)+ 第一批整目录回收(白名单 target:playwright-browsers /
 * 注册表 service id)。文案边界在壳侧 hint 钉死(Q10:重装幂等口径、
 * telegram 登录态不可回收、wechat-localdb TTL 默认 24h 自清),本卡只
 * 渲染不改写;回收后壳侧广播 pyenv-status-changed,本卡重拉占用与组件
 * 状态(crawl4ai / searxng 行转「未装」的真相源 = pyenv_get_status)。
 *
 * 只消费既有基件(Card / SettingRow / Badge / Button),不新造排版件
 * (与 10-14-ui-sweep-batch 风格面解耦)。
 */

/** 字节量展示(1024 基;≥100 取整,否则 1 位小数)。 */
function formatBytes(bytes: number): string {
  if (bytes < 1024) return `${bytes} B`;
  const units = ["KB", "MB", "GB", "TB"];
  let value = bytes / 1024;
  let unit = 0;
  while (value >= 1024 && unit < units.length - 1) {
    value /= 1024;
    unit += 1;
  }
  return `${value >= 100 ? Math.round(value) : value.toFixed(1)} ${units[unit]}`;
}

/** 回收回执的本地回显(target → 已回收字节数)。 */
interface ReclaimNote {
  target: string;
  bytes: number;
}

export function StorageCard() {
  const navigate = useNavigate();
  const [usage, setUsage] = useState<StorageUsage | null>(null);
  const [loading, setLoading] = useState(true);
  const [loadError, setLoadError] = useState<string | null>(null);
  /** 已装服务组件 id(回收行来源;pyenv_get_status 失败宽容为空) */
  const [serviceIds, setServiceIds] = useState<string[]>([]);
  const [reclaiming, setReclaiming] = useState<string | null>(null);
  const [reclaimError, setReclaimError] = useState<string | null>(null);
  const [reclaimNote, setReclaimNote] = useState<ReclaimNote | null>(null);

  const refresh = useCallback(async () => {
    setLoading(true);
    setLoadError(null);
    try {
      // 组件状态查询失败不拦占用视图(服务回收行按无服务处理,宽容)
      const [nextUsage, status] = await Promise.all([
        storageUsage(),
        pyenvGetStatus().catch(() => null),
      ]);
      setUsage(nextUsage);
      setServiceIds(
        status
          ? status.components
              .filter((component) => component.kind === "service" && component.installed)
              .map((component) => component.id)
          : [],
      );
    } catch (error) {
      setUsage(null);
      setLoadError(error instanceof Error ? error.message : String(error));
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    void refresh();
  }, [refresh]);

  const handleReclaim = useCallback(
    async (target: string) => {
      setReclaiming(target);
      setReclaimError(null);
      try {
        const outcome = await reclaimStorage(target);
        setReclaimNote({ target, bytes: outcome.reclaimed_bytes });
        await refresh();
      } catch (error) {
        setReclaimError(error instanceof Error ? error.message : String(error));
      } finally {
        setReclaiming(null);
      }
    },
    [refresh],
  );

  return (
    <Card data-testid="storage-card">
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          <HardDrive className="size-4 text-muted-foreground" />
          磁盘占用(数据根)
        </CardTitle>
        <CardDescription>
          数据根全量逻辑字节(metadata().len(),含隐藏文件;顶层文件全聚合、未知目录归「其余」);回收按整目录、重装幂等
        </CardDescription>
      </CardHeader>
      <CardContent className="flex flex-col gap-2">
        {loading ? (
          <p role="status" data-testid="storage-loading" className="text-xs text-muted-foreground">
            扫描中…(数万文件,秒级)
          </p>
        ) : null}
        {loadError ? (
          <div role="alert" data-testid="storage-error" className="flex flex-wrap items-center gap-2">
            <p className="min-w-0 flex-1 text-xs text-destructive-text">占用扫描失败:{loadError}</p>
            <Button size="sm" variant="outline" data-testid="storage-retry" onClick={() => void refresh()}>
              <RefreshCw className="size-3.5" />
              重试
            </Button>
          </div>
        ) : null}
        {reclaimError ? (
          <p role="alert" data-testid="storage-reclaim-error" className="text-xs text-destructive-text">
            回收失败:{reclaimError}
          </p>
        ) : null}
        {reclaimNote && !loading ? (
          <p role="status" data-testid="storage-reclaim-note" className="text-xs text-ok">
            已回收 {reclaimNote.target}(约 {formatBytes(reclaimNote.bytes)})
          </p>
        ) : null}
        {usage ? (
          <>
            <div
              data-testid="storage-total"
              className="flex items-center justify-between gap-2 border-b border-border/60 pb-3"
            >
              <span className="text-sm font-semibold">总占用</span>
              <Badge variant="outline" className="font-mono text-xs">
                {formatBytes(usage.total)}
              </Badge>
            </div>
            <div className="divide-y divide-border/60">
              {usage.items.map((item) => (
                <div key={item.id} data-testid={`storage-item-${item.id}`}>
                  <SettingRow label={item.label} description={item.hint}>
                    <Badge variant="outline" className="font-mono text-2xs">
                      {formatBytes(item.bytes)}
                    </Badge>
                    {item.id === "models" ? (
                      <Button
                        size="sm"
                        variant="ghost"
                        data-testid="storage-models-manage"
                        onClick={() => navigate("/settings?section=vision")}
                      >
                        去模型管理
                      </Button>
                    ) : null}
                    {item.reclaimable && item.bytes > 0 ? (
                      <Button
                        size="sm"
                        variant="outline"
                        data-testid={`storage-reclaim-${item.id}`}
                        disabled={reclaiming !== null}
                        onClick={() => void handleReclaim(item.id)}
                      >
                        <Trash2 className="size-3.5" />
                        {reclaiming === item.id ? "回收中…" : "回收"}
                      </Button>
                    ) : null}
                  </SettingRow>
                  {item.id === "services" && serviceIds.length > 0 ? (
                    <div className="flex flex-col border-t border-dashed border-border/60 sm:pl-4">
                      {serviceIds.map((id) => (
                        <SettingRow
                          key={id}
                          label={`服务 ${id}`}
                          description={`停止服务进程并删除 services/${id}/ 与安装双戳(pip 件随 Python 环境重建回收)`}
                        >
                          <Button
                            size="sm"
                            variant="outline"
                            data-testid={`storage-service-reclaim-${id}`}
                            disabled={reclaiming !== null}
                            onClick={() => void handleReclaim(id)}
                          >
                            <Trash2 className="size-3.5" />
                            {reclaiming === id ? "回收中…" : "停止并回收"}
                          </Button>
                        </SettingRow>
                      ))}
                    </div>
                  ) : null}
                </div>
              ))}
            </div>
          </>
        ) : null}
      </CardContent>
    </Card>
  );
}
