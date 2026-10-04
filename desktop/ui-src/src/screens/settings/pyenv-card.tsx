import { Cpu, Download, RefreshCw } from "lucide-react";
import { useCallback, useEffect, useState } from "react";

import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import type { SidecarRequestError } from "@/lib/api";
import { cn } from "@/lib/utils";

import { asSidecarError } from "./api";
import { ErrorBox } from "./error-box";
import { FieldInput } from "./field-input";
import { SettingRow } from "./settings-row";
import {
  onPyenvStatusChanged,
  pyenvGetStatus,
  pyenvStartSetup,
  pyenvSyncDeps,
  PYENV_PHASE_ORDER,
  type PyenvState,
  type PyenvStatus,
  type PyenvPhase,
  type PyenvStep,
  type PyenvStepStatus,
} from "./pyenv-api";

/**
 * 「Python 运行环境」卡片(10-05-desktop-managed-py-env 第 4 步;design §5)。
 *
 * 字段面:开始配置(D2 显式动作)/ 安装路径 / Python 使用路径 / 运行时下载源
 * 覆盖 / PyPI 镜像覆盖(双镜像,D3)/ 安装明细(状态机五阶段逐项)/ 同步依赖
 * (D4,依赖漂移时出现)。IPC 契约见 ./pyenv-api.ts(波次钉死,与壳侧 pyenv.rs
 * 对齐);安装本体在第 3/5 步接管,本卡如实消费命令应答与状态事件,不伪造进度。
 */

/** 五态的展示元(徽标色 + 引导文案;文案口径 = prd D1-D5 与 design §3/§7)。 */
const STATE_META: Record<PyenvState, { label: string; badge: "outline" | "ok" | "warning" | "destructive"; hint: string }> = {
  not_configured: {
    label: "未配置",
    badge: "outline",
    hint:
      "Python 运行时与依赖不随安装包分发(D1);点「开始配置」在线下载安装,全程状态见下方明细。首跑需联网,离线无法完成配置。",
  },
  installing: {
    label: "安装中",
    badge: "warning",
    hint: "安装链执行中(下载 → 校验 → 解压 → 依赖 → 自检),明细逐项如下;完成或失败会经状态事件自动刷新。",
  },
  ready: {
    label: "就绪",
    badge: "ok",
    hint: "Python 运行环境就绪,sidecar 可正常拉起;已装依赖与随包锁版清单一致。",
  },
  error: {
    label: "异常",
    badge: "destructive",
    hint: "安装链失败或中断:查看下方明细的失败项,点「开始配置」重试(幂等,已完成的步骤会跳过)。",
  },
  deps_stale: {
    label: "依赖漂移",
    badge: "warning",
    hint:
      "应用更新后随包依赖清单已变(D4):点「同步依赖」幂等重跑安装链,已装依赖会跳过;期间不拦 sidecar 运行。",
  },
};

/** 状态机五阶段中文标(design §3:downloading→…→selfcheck)。 */
const PHASE_LABEL: Record<PyenvPhase, string> = {
  downloading: "下载运行时",
  verifying: "校验 sha256",
  extracting: "解压到数据根",
  installing_deps: "pip 安装依赖(锁版清单)",
  selfcheck: "自检(sidecar version 握手)",
};

/** 单阶段状态标(skipped = 幂等重试时已装步跳过,D4)。 */
const STEP_STATUS_META: Record<PyenvStepStatus, { label: string; cls: string }> = {
  pending: { label: "等待中", cls: "text-muted-foreground" },
  running: { label: "进行中", cls: "text-warning" },
  done: { label: "已完成", cls: "text-ok" },
  skipped: { label: "已跳过", cls: "text-muted-foreground" },
  failed: { label: "失败", cls: "text-destructive" },
};

/**
 * 安装明细 = 状态机五阶段骨架 + steps 补态(steps 来自进度戳/内存步进,
 * 可能只覆盖部分阶段;同相位多条记录取最新一条;缺失阶段按「等待中」呈现,
 * 保证「逐项可见」不因数据稀疏而缺行)。
 */
function mergedSteps(steps: PyenvStep[]): PyenvStep[] {
  const byPhase = new Map<PyenvPhase, PyenvStep>();
  for (const step of steps) byPhase.set(step.phase, step);
  return PYENV_PHASE_ORDER.map(
    (phase) => byPhase.get(phase) ?? { phase, status: "pending" as PyenvStepStatus, error: null },
  );
}

export function PyenvCard() {
  const [status, setStatus] = useState<PyenvStatus | null>(null);
  const [loadError, setLoadError] = useState<SidecarRequestError | null>(null);
  /** 动作(开始配置/同步依赖)的结构化错误与回执;与拉取错误分槽,均在卡片底部 */
  const [actionError, setActionError] = useState<SidecarRequestError | null>(null);
  const [note, setNote] = useState<string | null>(null);
  const [setupBusy, setSetupBusy] = useState(false);
  const [syncBusy, setSyncBusy] = useState(false);
  /** 双镜像覆盖草稿(初拉与本人动作回包时回填;事件刷新不覆写,防打断输入) */
  const [mirrorRuntime, setMirrorRuntime] = useState("");
  const [mirrorPypi, setMirrorPypi] = useState("");

  const applyStatus = useCallback((next: PyenvStatus, syncMirrors: boolean) => {
    setStatus(next);
    if (syncMirrors) {
      setMirrorRuntime(next.mirror_runtime ?? "");
      setMirrorPypi(next.mirror_pypi ?? "");
    }
  }, []);

  /** 拉取一次状态(初始化与拉取失败后的重试共用)。 */
  const refresh = useCallback(async () => {
    setLoadError(null);
    try {
      applyStatus(await pyenvGetStatus(), true);
    } catch (raw) {
      setLoadError(asSidecarError(raw));
    }
  }, [applyStatus]);

  useEffect(() => {
    let cancelled = false;
    let unlisten: (() => void) | null = null;
    void refresh();
    void onPyenvStatusChanged(
      (next) => {
        if (!cancelled) applyStatus(next, false);
      },
      (error) => {
        if (!cancelled) setLoadError(asSidecarError(error));
      },
    )
      .then((unlistenFn) => {
        if (cancelled) unlistenFn();
        else unlisten = unlistenFn;
      })
      .catch(() => {
        // 浏览器直开无事件通道:拉取态已够用(惯例同 use-sidecar-status)
      });
    return () => {
      cancelled = true;
      unlisten?.();
    };
  }, [refresh, applyStatus]);

  /** 开始配置(D2):镜像覆盖随本次动作整体替换式保存(空 = 清回默认源)。 */
  const handleStartSetup = useCallback(async () => {
    setSetupBusy(true);
    setActionError(null);
    setNote(null);
    try {
      const next = await pyenvStartSetup({ mirrorRuntime, mirrorPypi });
      applyStatus(next, true);
      setNote("开始配置已发出,下载源覆盖已保存;进度见安装明细(状态事件实时刷新)。");
    } catch (raw) {
      setActionError(asSidecarError(raw));
    } finally {
      setSetupBusy(false);
    }
  }, [mirrorRuntime, mirrorPypi, applyStatus]);

  /** 同步依赖(D4):依赖漂移时的一键幂等重跑。 */
  const handleSyncDeps = useCallback(async () => {
    setSyncBusy(true);
    setActionError(null);
    setNote(null);
    try {
      const next = await pyenvSyncDeps();
      applyStatus(next, true);
      setNote("同步依赖已发出(幂等重跑安装链,已装依赖会跳过);进度见安装明细。");
    } catch (raw) {
      setActionError(asSidecarError(raw));
    } finally {
      setSyncBusy(false);
    }
  }, [applyStatus]);

  const meta = status !== null ? STATE_META[status.state] : null;

  return (
    <Card data-testid="pyenv-card">
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          <Cpu className="size-4 text-muted-foreground" />
          Python 运行环境
          {meta ? (
            <Badge variant={meta.badge} data-testid="pyenv-state-badge">
              {meta.label}
            </Badge>
          ) : null}
        </CardTitle>
        <CardDescription>
          运行时与依赖按需下载(D1/D2:不随包分发,设置页显式配置);下载 → 校验 → 解压 → pip 锁版依赖 → 自检全链状态可见,失败可重试
        </CardDescription>
      </CardHeader>
      <CardContent className="flex flex-col gap-1">
        {loadError ? <ErrorBox error={loadError} onRetry={() => void refresh()} /> : null}
        {status === null && loadError === null ? (
          <span data-testid="pyenv-loading" className="py-2 text-xs text-muted-foreground">
            环境状态装载中…
          </span>
        ) : null}

        {status !== null && meta ? (
          <>
            <p data-testid="pyenv-state-hint" className="py-2 text-xs leading-5 text-muted-foreground">
              {meta.hint}
            </p>

            <div className="divide-y divide-border/60">
              <SettingRow
                label="安装路径"
                description="install_only 包解压即得(数据根下,与 models/ 并排;绝不写安装目录)"
              >
                <code
                  data-testid="pyenv-install-path"
                  className="max-w-full truncate font-mono text-2xs text-muted-foreground"
                  title={status.install_path}
                >
                  {status.install_path}
                </code>
              </SettingRow>
              <SettingRow label="Python 使用路径" description="sidecar spawn 源(壳侧拉起自管 Python 的二进制)">
                <code
                  data-testid="pyenv-python-path"
                  className="max-w-full truncate font-mono text-2xs text-muted-foreground"
                  title={status.python_path}
                >
                  {status.python_path}
                </code>
              </SettingRow>
            </div>

            {/* 双镜像覆盖(D3):镜像只换 URL 不绕 sha256 校验;空 = 默认源 */}
            <div className="divide-y divide-border/60">
              <FieldInput
                label="运行时下载源覆盖"
                aria-label="运行时下载源覆盖"
                placeholder="https://mirror.example/cpython-3.12.7-…-install_only.tar.gz"
                value={mirrorRuntime}
                onChange={(event) => setMirrorRuntime(event.target.value)}
                hint="空 = 随包 manifest 钉版源(indygreg python-build-standalone cpython 3.12.7);镜像只换 URL,不绕 sha256 校验"
              />
              <FieldInput
                label="PyPI 镜像覆盖"
                aria-label="PyPI 镜像覆盖"
                placeholder="https://pypi.tuna.tsinghua.edu.cn/simple"
                value={mirrorPypi}
                onChange={(event) => setMirrorPypi(event.target.value)}
                hint="空 = 默认 PyPI;依赖安装(pip install --index-url)取此值"
              />
            </div>

            {/* 安装明细(design §3 状态机逐项;五阶段骨架恒在,steps 补态) */}
            <div data-testid="pyenv-steps" className="divide-y divide-border/60">
              {mergedSteps(status.steps).map(({ phase, status: stepStatus, error }) => {
                const stepMeta = STEP_STATUS_META[stepStatus];
                return (
                  <div key={phase} data-testid={`pyenv-step-${phase}`} className="flex flex-col gap-0.5 py-2">
                    <div className="flex items-center justify-between gap-2">
                      <span className="text-xs text-foreground">{PHASE_LABEL[phase]}</span>
                      <span
                        data-testid={`pyenv-step-${phase}-status`}
                        className={cn("flex items-center gap-1 text-2xs", stepMeta.cls)}
                      >
                        {stepStatus === "running" ? <RefreshCw className="size-3 animate-spin" /> : null}
                        {stepMeta.label}
                      </span>
                    </div>
                    {error ? (
                      <p
                        role="alert"
                        data-testid={`pyenv-step-${phase}-error`}
                        className="text-left text-2xs leading-4 text-destructive"
                      >
                        {error}
                      </p>
                    ) : null}
                  </div>
                );
              })}
            </div>

            {/* 动作条(拆解表第 5 条:反馈在左、动作在右);同步依赖仅漂移态出现(D4) */}
            <div className="flex flex-wrap items-center justify-between gap-2 border-t border-border/60 pt-3">
              <div className="min-w-0 flex-1">
                {actionError ? <ErrorBox error={actionError} /> : null}
                {note ? (
                  <p role="status" data-testid="pyenv-action-note" className="text-xs text-ok">
                    {note}
                  </p>
                ) : null}
              </div>
              <div className="flex flex-wrap items-center gap-2">
                {status.state === "deps_stale" ? (
                  <Button
                    size="sm"
                    variant="outline"
                    onClick={() => void handleSyncDeps()}
                    disabled={syncBusy || setupBusy}
                    data-testid="pyenv-sync-deps"
                    title="D4:幂等重跑依赖安装链,已装依赖会跳过"
                  >
                    <RefreshCw className={syncBusy ? "size-3.5 animate-spin" : "size-3.5"} />
                    同步依赖
                  </Button>
                ) : null}
                <Button
                  size="sm"
                  onClick={() => void handleStartSetup()}
                  disabled={setupBusy || syncBusy || status.state === "installing"}
                  data-testid="pyenv-start-setup"
                  title="D2:显式开始配置(下载→校验→解压→依赖→自检);安装中不可重复触发"
                >
                  <Download className={setupBusy ? "size-3.5 animate-pulse" : "size-3.5"} />
                  开始配置
                </Button>
              </div>
            </div>
          </>
        ) : null}
      </CardContent>
    </Card>
  );
}
