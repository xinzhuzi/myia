import { Check, Download, FileText, Layers, PackageOpen, RefreshCw, RotateCcw, Trash2 } from "lucide-react";
import { useCallback, useEffect, useState } from "react";

import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import type { SidecarRequestError } from "@/lib/api";
import { cn } from "@/lib/utils";

import { asSidecarError } from "./api";
import {
  bundledCategoryInstall,
  bundledPluginsInstall,
  bundledPluginsList,
  bundledPluginsUninstall,
  type BundledCategoryView,
  type BundledPluginsListResult,
  type BundledPluginView,
} from "./bundled-plugins-api";
import { ErrorBox } from "./error-box";

/**
 * 「装机组件」分区卡(10-05-bundled-plugins-install + 批二 batch2):随包
 * 插件组件包的发现 + 一键装/重装/卸载面 + 品类 YAML 平铺装面(sidecar
 * plugins.bundled.list/install/uninstall/category_install)。
 *
 * 组件包逐包行 = 名称/版本/tier·gate 徽章/已装态徽章(已装版本与随包版本
 * 不同 → 「可重装更新」)/安装·重装·卸载按钮/findings 行内展示(坏 manifest
 * 等条目级 finding 如实透出,不拦整表渲染)。空态如实:dir=null(dev 形态/
 * 旧包未注入 MYIA_BUNDLED_PLUGINS)→ 提示本分区在正式安装包内可用,不虚构。
 *
 * 批二:已装行「卸载」钮(普通确认——卸载=删安装根拷贝非危险操作,随包原件
 * 只读永不删,可随时重装);品类分区行(安装语义 = 单文件平铺拷到数据根
 * plugins/,与启动补种同落点;已存在如实呈现不覆盖,覆盖是知情操作经确认
 * 才发 force——与补种「幂等补缺绝不覆盖」语义对齐)。vendor 缺失不在安装时
 * 检查、不伪造完整性(osint/theHarvester 运行时走 adapter 既有结构化
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
  /** 正在安装/重装/卸载/品类装的件 id(行级 busy;装卸动作与拉取错误分槽)。 */
  const [busyId, setBusyId] = useState<string | null>(null);
  const [actionError, setActionError] = useState<SidecarRequestError | null>(null);
  const [actionNote, setActionNote] = useState<InstallOutcome | null>(null);

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
      setBusyId(plugin.id);
      setActionError(null);
      setActionNote(null);
      try {
        const result = await bundledPluginsInstall({ id: plugin.id, force: plugin.installed });
        setActionNote({
          text: `${plugin.id}@${result.version} 已${plugin.installed ? "重装" : "安装"} → ${result.dir}(整目录拷贝,manifest 校验通过)`,
          ok: true,
        });
        // 拉取是真相源:安装后回读已装态徽章随新
        await refresh();
      } catch (raw) {
        setActionError(asSidecarError(raw));
      } finally {
        setBusyId(null);
      }
    },
    [refresh],
  );

  /** 卸载(批二 R2):删安装根拷贝(随包原件只读永不删,可随时重装)——
   *  非危险操作,普通一次确认(不循钥匙链删除二次确认判例);取消零调用。 */
  const handleUninstall = useCallback(
    async (plugin: BundledPluginView) => {
      if (plugin.id === null || !plugin.installed) return;
      const confirmed = window.confirm(
        `卸载 ${plugin.name ?? plugin.id}(${plugin.id})?\n\n卸载 = 删除插件根里的安装拷贝;随包原件只读不受影响,可随时重装。`,
      );
      if (!confirmed) return;
      setBusyId(plugin.id);
      setActionError(null);
      setActionNote(null);
      try {
        const result = await bundledPluginsUninstall({ id: plugin.id });
        setActionNote({
          text: `${result.id} 已卸载(${result.path});随包原件只读,可随时重装`,
          ok: true,
        });
        await refresh();
      } catch (raw) {
        setActionError(asSidecarError(raw));
      } finally {
        setBusyId(null);
      }
    },
    [refresh],
  );

  /** 品类平铺装(批二 R3):未存在 → {id}(零 force);已存在 → 确认后
   *  {id, force:true} 覆盖(本地手改会丢失,知情操作;与补种「绝不覆盖」
   *  语义对齐——自动面永不覆盖,显式面知情才覆盖)。 */
  const handleCategoryInstall = useCallback(
    async (category: BundledCategoryView) => {
      if (category.id === null) return; // 坏 YAML 件:无可安装内容,按了也装不上
      if (category.exists) {
        const confirmed = window.confirm(
          `覆盖品类文件 ${category.file}?\n\n数据根已有同名文件(补种或自建);覆盖将丢失其中的本地修改。`,
        );
        if (!confirmed) return;
      }
      setBusyId(`category:${category.id}`);
      setActionError(null);
      setActionNote(null);
      try {
        const result = await bundledCategoryInstall({ id: category.id, force: category.exists });
        setActionNote({
          text: `${result.file} 已${category.exists ? "覆盖" : "安装"} → ${result.path}(单文件平铺,与启动补种同落点)`,
          ok: true,
        });
        await refresh();
      } catch (raw) {
        setActionError(asSidecarError(raw));
      } finally {
        setBusyId(null);
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
          安装包内已随包分发的官方插件组件包:一键装/重装/卸载(整目录拷贝,manifest 校验 + 版本矩阵 + 绝不半装,与 CLI{" "}
          <code>myssia plugin install/remove</code> 同一道门)。品类 YAML(羊毛/行情等)走启动补种自动补缺;本分区亦提供显式安装/覆盖(批二)。
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
                随包原件只读永不删(卸载 = 删安装根拷贝,可随时重装)。部分件(osint/theHarvester)运行需上游
                vendor 源码,装机包未含(许可边界);运行时按其结构化 <code>vendor_missing</code> 指引自行补齐。
              </p>
            </div>

            <div
              data-testid="bundled-plugins-rows"
              className="flex flex-col divide-y divide-border/60 rounded-lg border border-border/60"
            >
              {list.plugins.map((plugin) => {
                const busy = plugin.id !== null && busyId === plugin.id;
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
                          处理中(安装/重装/卸载)…
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
                      {plugin.installed ? (
                        <Button
                          size="sm"
                          variant="ghost"
                          disabled={busy}
                          data-testid={`bundled-plugin-${plugin.dir_name}-uninstall`}
                          aria-label={`卸载${plugin.name ?? plugin.dir_name}`}
                          title="卸载安装根拷贝(随包原件只读不受影响,可随时重装;普通确认)"
                          onClick={() => void handleUninstall(plugin)}
                        >
                          <Trash2 className={busy ? "size-3.5 animate-pulse" : "size-3.5"} />
                          卸载
                        </Button>
                      ) : null}
                    </div>
                  </div>
                );
              })}
            </div>

            {/* 品类配置分区(批二 R3):随包品类 YAML 发现/平铺装面。安装语义 =
                单文件平铺拷到数据根 plugins/(与启动补种同落点);已存在如实
                呈现不覆盖,覆盖是知情操作(确认后才发 force)。空表(dev 形态
                旧 sidecar)静默零渲染。 */}
            {list.categories.length > 0 ? (
              <section
                aria-labelledby="bundled-categories-title"
                data-testid="bundled-categories-section"
                className="flex flex-col gap-3"
              >
                <h3
                  id="bundled-categories-title"
                  className="text-2xs font-medium tracking-wide text-muted-foreground"
                >
                  品类配置(单文件平铺装到插件根;启动补种已自动补缺的件呈现「已存在」)
                </h3>
                <div
                  data-testid="bundled-categories"
                  className="flex flex-col divide-y divide-border/60 rounded-lg border border-border/60"
                >
                  {list.categories.map((category) => {
                    const busy = category.id !== null && busyId === `category:${category.id}`;
                    const installBlocked = category.id === null;
                    return (
                      <div
                        key={category.file}
                        data-testid={`bundled-category-${category.file}`}
                        className="flex flex-wrap items-center justify-between gap-3 p-4"
                      >
                        <div className="flex min-w-0 flex-1 flex-col gap-1">
                          <div className="flex flex-wrap items-center gap-1.5">
                            <FileText className="size-3.5 shrink-0 text-muted-foreground" />
                            <span className="text-sm font-medium text-foreground">
                              {category.name ?? category.file}
                            </span>
                            <span className="font-mono text-2xs text-muted-foreground">
                              {category.id ?? category.file}
                            </span>
                            <Badge
                              variant={category.exists ? "ok" : "outline"}
                              data-testid={`bundled-category-${category.file}-state`}
                            >
                              {category.exists ? "已存在" : "未装"}
                            </Badge>
                          </div>
                          {category.schedule ? (
                            <p className="text-2xs leading-4 text-muted-foreground">
                              排程 {category.schedule}(cron;随包文件 {category.file})
                            </p>
                          ) : null}
                          {category.findings.length > 0 ? (
                            <div
                              data-testid={`bundled-category-${category.file}-findings`}
                              className="flex flex-col gap-0.5"
                            >
                              {category.findings.map((finding, index) => (
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
                              品类安装中…
                            </span>
                          ) : null}
                        </div>
                        <div className="flex shrink-0 items-center gap-2">
                          <Button
                            size="sm"
                            variant={category.exists ? "outline" : "secondary"}
                            disabled={busy || installBlocked}
                            data-testid={`bundled-category-${category.file}-${category.exists ? "overwrite" : "install"}`}
                            aria-label={`${category.exists ? "覆盖" : "安装"}品类${category.name ?? category.file}`}
                            title={
                              category.id === null
                                ? "品类 YAML 坏件:无法通过校验,不可安装(见上方 finding)"
                                : category.exists
                                  ? "覆盖数据根同名文件(本地修改会丢失;确认后执行)"
                                  : "单文件平铺拷到插件根(与启动补种同落点)"
                            }
                            onClick={() => void handleCategoryInstall(category)}
                          >
                            {category.exists ? (
                              <RotateCcw className={busy ? "size-3.5 animate-pulse" : "size-3.5"} />
                            ) : (
                              <Download className={busy ? "size-3.5 animate-pulse" : "size-3.5"} />
                            )}
                            {category.exists ? "覆盖" : "安装"}
                          </Button>
                        </div>
                      </div>
                    );
                  })}
                </div>
              </section>
            ) : null}

            {actionError ? <ErrorBox error={actionError} /> : null}
            {actionNote ? (
              <p
                role={actionNote.ok ? "status" : "alert"}
                data-testid="bundled-install-note"
                className={cn("flex items-start gap-1.5 text-xs leading-5", actionNote.ok ? "text-ok" : "text-destructive")}
              >
                {actionNote.ok ? <Check className="mt-0.5 size-3.5 shrink-0" /> : null}
                {actionNote.text}
              </p>
            ) : null}
          </>
        ) : null}
      </CardContent>
    </Card>
  );
}
