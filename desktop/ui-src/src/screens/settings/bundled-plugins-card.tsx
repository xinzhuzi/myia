import { Check, Download, Layers, PackageOpen, RefreshCw, RotateCcw } from "lucide-react";
import { useCallback, useEffect, useState } from "react";

import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import type { SidecarRequestError } from "@/lib/api";
import { cn } from "@/lib/utils";

import { asSidecarError } from "./api";
import {
  bundledPluginsInstall,
  bundledPluginsList,
  type BundledPluginsListResult,
  type BundledPluginView,
} from "./bundled-plugins-api";
import { ErrorBox } from "./error-box";

/**
 * 「装机组件」分区卡(10-05-bundled-plugins-install):随包插件组件包的
 * 发现 + 一键装/重装面(sidecar plugins.bundled.list/install)。
 *
 * 逐包行 = 名称/版本/tier·gate 徽章/已装态徽章(已装版本与随包版本不同 →
 * 「可重装更新」)/安装·重装按钮/findings 行内展示(坏 manifest 等条目级
 * finding 如实透出,不拦整表渲染)。空态如实:dir=null(dev 形态/旧包未注入
 * MYIA_BUNDLED_PLUGINS)→ 提示本分区在正式安装包内可用,不虚构清单。
 *
 * 卸载本期不做(档记后续):随包原件只读永不删(卸载 = 删安装根拷贝,可
 * 随时重装);文案明示卸载走 CLI `myssia plugin remove`。vendor 缺失不在
 * 安装时检查、不伪造完整性(osint/theHarvester 运行时走 adapter 既有结构化
 * vendor_missing 指引,许可红线:vendor/ submodule 不随包分发)。
 */

/** tier 徽章展示(desktop = 桌面默认集;其他 tier/未知如实原样回显)。 */
function TierBadge({ tier }: { tier: string | null }) {
  if (tier === null) return null;
  return (
    <Badge variant="outline" data-testid={`bundled-tier-${tier}`}>
      {tier}
    </Badge>
  );
}

/** gate 徽章(门槛件激活策略:paid/trace/platform/stale;无门槛件 = 不渲染)。 */
function GateBadge({ gate }: { gate: string | null }) {
  if (gate === null) return null;
  return (
    <Badge variant="warning" data-testid={`bundled-gate-${gate}`}>
      {gate}
    </Badge>
  );
}

/** 单件安装/重装的行内反馈(成功回执与结构化错误分离,同 pyenv-card 惯例)。 */
interface InstallOutcome {
  text: string;
  ok: boolean;
}

export function BundledPluginsCard() {
  const [list, setList] = useState<BundledPluginsListResult | null>(null);
  const [loadError, setLoadError] = useState<SidecarRequestError | null>(null);
  /** 正在安装/重装的件 id(行级 busy;装卸动作与拉取错误分槽)。 */
  const [installingId, setInstallingId] = useState<string | null>(null);
  const [installError, setInstallError] = useState<SidecarRequestError | null>(null);
  const [installNote, setInstallNote] = useState<InstallOutcome | null>(null);

  const refresh = useCallback(async () => {
    setLoadError(null);
    try {
      setList(await bundledPluginsList());
    } catch (raw) {
      setLoadError(asSidecarError(raw));
    }
  }, []);

  useEffect(() => {
    void refresh();
  }, [refresh]);

  /** 安装/重装:未装 → force=false(已装由后端 already_installed 结构化兜底);
   *  已装 → force=true 重装(先清后拷,陈旧文件不残留;已装版本低于随包 = 更新)。 */
  const handleInstall = useCallback(
    async (plugin: BundledPluginView) => {
      if (plugin.id === null) return; // manifest 坏件:目录内没有可安装的 manifest,按了也装不上
      setInstallingId(plugin.id);
      setInstallError(null);
      setInstallNote(null);
      try {
        const result = await bundledPluginsInstall({ id: plugin.id, force: plugin.installed });
        setInstallNote({
          text: `${plugin.id}@${result.version} 已${plugin.installed ? "重装" : "安装"} → ${result.dir}(整目录拷贝,manifest 校验通过)`,
          ok: true,
        });
        // 拉取是真相源:安装后回读已装态徽章随新
        await refresh();
      } catch (raw) {
        setInstallError(asSidecarError(raw));
      } finally {
        setInstallingId(null);
      }
    },
    [refresh],
  );

  return (
    <Card data-testid="bundled-plugins-card">
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          <Layers className="size-4 text-muted-foreground" />
          随包官方插件件(装机组件)
        </CardTitle>
        <CardDescription>
          安装包内已随包分发的官方插件组件包:一键装进插件根(整目录拷贝,manifest 校验 + 版本矩阵 + 绝不半装,与 CLI{" "}
          <code>myssia plugin install</code> 同一道门)。品类 YAML(羊毛/行情等)走启动补种,不在此面。
        </CardDescription>
      </CardHeader>
      <CardContent className="flex flex-col gap-4">
        {loadError ? <ErrorBox error={loadError} onRetry={() => void refresh()} /> : null}
        {list === null && loadError === null ? (
          <span data-testid="bundled-plugins-loading" className="text-xs text-muted-foreground">
            随包插件清单装载中…
          </span>
        ) : null}

        {list !== null && list.dir === null ? (
          /* 空态如实:env 未注入 = dev 形态/旧包;不虚构清单不硬造按钮 */
          <div data-testid="bundled-plugins-empty" className="flex flex-col gap-2 rounded-lg border bg-accent/30 p-4">
            <div className="flex items-center gap-2">
              <PackageOpen className="size-4 text-muted-foreground" />
              <span className="text-sm font-medium text-foreground">未发现随包插件目录</span>
            </div>
            <p className="text-xs leading-5 text-muted-foreground">
              当前运行形态未注入随包插件目录(dev 开发态或旧版本安装包;dev 形态刻意不注入,避免枚举出仓库里未随包分发的目录)。
              正式安装包内本分区会列出 10 件官方插件组件包;已装插件仍可经源管理/品类 YAML 正常使用。
            </p>
          </div>
        ) : null}

        {list !== null && list.dir !== null ? (
          <>
            <div className="flex flex-col gap-1">
              <code
                data-testid="bundled-plugins-dir"
                title={list.dir}
                className="break-all rounded-md border border-border/60 bg-muted/40 px-3 py-2 font-mono text-2xs leading-5 text-foreground/80"
              >
                {list.dir}
              </code>
              <p className="text-2xs leading-4 text-muted-foreground">
                随包原件只读永不删(卸载 = 删安装根拷贝,可随时重装;卸载走 CLI{" "}
                <code>myssia plugin remove &lt;id&gt;</code>,本屏不提供卸载)。部分件(osint/theHarvester)运行需上游
                vendor 源码,装机包未含(许可边界);运行时按其结构化 <code>vendor_missing</code> 指引自行补齐。
              </p>
            </div>

            <div
              data-testid="bundled-plugins-rows"
              className="flex flex-col divide-y divide-border/60 rounded-lg border border-border/60"
            >
              {list.plugins.map((plugin) => {
                const busy = plugin.id !== null && installingId === plugin.id;
                // 未装不兼容件禁装(知情禁用:随包件超前于当前 myssia,该等壳更新,
                // CLI 面 --force 仍可达);已装件不受此限——重装带 force 即强装通道。
                const installBlocked = plugin.id === null || (!plugin.installed && plugin.compatible_current === false);
                const updatable = plugin.installed && plugin.installed_version !== plugin.version && plugin.version !== null;
                return (
                  <div
                    key={plugin.dir_name}
                    data-testid={`bundled-plugin-${plugin.dir_name}`}
                    className="flex flex-wrap items-center justify-between gap-3 p-4"
                  >
                    <div className="flex min-w-0 flex-1 flex-col gap-1">
                      <div className="flex flex-wrap items-center gap-1.5">
                        <span className="text-sm font-medium text-foreground">{plugin.name ?? plugin.dir_name}</span>
                        <span className="font-mono text-2xs text-muted-foreground">{plugin.id ?? plugin.dir_name}</span>
                        {plugin.version ? (
                          <span className="text-2xs text-muted-foreground" data-testid={`bundled-version-${plugin.dir_name}`}>
                            {plugin.installed && updatable ? (
                              <>
                                随包 {plugin.version}(已装 {plugin.installed_version ?? "?"},可重装更新)
                              </>
                            ) : (
                              <>{plugin.version}</>
                            )}
                          </span>
                        ) : null}
                        <TierBadge tier={plugin.tier} />
                        <GateBadge gate={plugin.gate} />
                        <Badge
                          variant={plugin.installed ? "ok" : "outline"}
                          data-testid={`bundled-plugin-${plugin.dir_name}-state`}
                        >
                          {plugin.installed ? "已装" : "未装"}
                        </Badge>
                      </div>
                      <p className="text-2xs leading-4 text-muted-foreground">
                        {plugin.provides.length > 0 ? `能力:${plugin.provides.join("、")}` : "市场知识面(文档件)"}
                      </p>
                      {plugin.compatible_current === false ? (
                        <p role="alert" className="text-left text-2xs leading-4 text-warning">
                          随包件要求 myssia {plugin.compatible}(当前不兼容;重装可强制,插件将被跳过,核心流水线不受影响)
                        </p>
                      ) : null}
                      {plugin.findings.length > 0 ? (
                        <div data-testid={`bundled-plugin-${plugin.dir_name}-findings`} className="flex flex-col gap-0.5">
                          {plugin.findings.map((finding, index) => (
                            <p
                              key={`${finding.code}-${index}`}
                              role="alert"
                              className={cn(
                                "text-left text-2xs leading-4",
                                finding.severity === "error" ? "text-destructive" : "text-warning",
                              )}
                            >
                              [{finding.severity}] {finding.code}:{finding.message}
                            </p>
                          ))}
                        </div>
                      ) : null}
                      {busy ? (
                        <span role="status" className="flex items-center gap-1 text-2xs text-warning">
                          <RefreshCw className="size-3 animate-spin" />
                          {plugin.installed ? "重装中…" : "安装中…"}
                        </span>
                      ) : null}
                    </div>
                    <div className="flex shrink-0 items-center gap-2">
                      <Button
                        size="sm"
                        variant={plugin.installed ? "outline" : "secondary"}
                        disabled={busy || installBlocked}
                        data-testid={`bundled-plugin-${plugin.dir_name}-${plugin.installed ? "reinstall" : "install"}`}
                        aria-label={`${plugin.installed ? "重装" : "安装"}${plugin.name ?? plugin.dir_name}`}
                        title={
                          plugin.id === null
                            ? "manifest 坏件:目录内 manifest 无法通过校验,不可安装(见上方 finding)"
                            : installBlocked
                              ? "随包件要求更高版本 myssia,当前不可安装(请随壳更新;CLI 面可 --force 强制)"
                              : plugin.installed
                                ? "覆盖重装(先清后拷;已装版本低于随包版本时即更新)"
                                : "整目录拷贝装进插件根(manifest 校验 + 版本矩阵)"
                        }
                        onClick={() => void handleInstall(plugin)}
                      >
                        {plugin.installed ? (
                          <RotateCcw className={busy ? "size-3.5 animate-pulse" : "size-3.5"} />
                        ) : (
                          <Download className={busy ? "size-3.5 animate-pulse" : "size-3.5"} />
                        )}
                        {plugin.installed ? "重装" : "安装"}
                      </Button>
                    </div>
                  </div>
                );
              })}
            </div>

            {installError ? <ErrorBox error={installError} /> : null}
            {installNote ? (
              <p
                role={installNote.ok ? "status" : "alert"}
                data-testid="bundled-install-note"
                className={cn("flex items-start gap-1.5 text-xs leading-5", installNote.ok ? "text-ok" : "text-destructive")}
              >
                {installNote.ok ? <Check className="mt-0.5 size-3.5 shrink-0" /> : null}
                {installNote.text}
              </p>
            ) : null}
          </>
        ) : null}
      </CardContent>
    </Card>
  );
}
