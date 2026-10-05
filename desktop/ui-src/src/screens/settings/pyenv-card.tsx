import { Check, Cpu, Download, RefreshCw, ShieldCheck, X } from "lucide-react";
import { useCallback, useEffect, useId, useState } from "react";

import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Switch } from "@/components/ui/switch";
import type { SidecarRequestError } from "@/lib/api";
import { cn } from "@/lib/utils";

import { asSidecarError } from "./api";
import { ErrorBox } from "./error-box";
import { HintButton } from "./label-hint";
import {
  onPyenvStatusChanged,
  pyenvGetStatus,
  pyenvInstallComponent,
  pyenvStartSetup,
  pyenvSyncDeps,
  pyenvVerify,
  PYENV_PHASE_ORDER,
  type PyenvComponent,
  type PyenvState,
  type PyenvStatus,
  type PyenvPhase,
  type PyenvStep,
  type PyenvStepStatus,
  type PyenvVerifyCheck,
} from "./pyenv-api";

/**
 * 「Python 运行环境」分区(10-05-desktop-managed-py-env 第 4 步;design §5)。
 *
 * 2026-10-05 全局版面判例(主人裁:600px 窄列「小家子气」):本区在
 * settings-screen 侧放开为居中大版面(max-w-4xl),卡内改全宽元素——
 * 状态横幅 / 路径块 break-all 全显不截断 / 镜像输入全宽 / 五阶段
 * 时间线 / 底部动作条;不再用 SettingRow 的 w-64 右置控件族。
 *
 * 字段面:开始配置(D2 显式动作)/ 安装路径 / Python 使用路径 / 运行时下载源
 * 覆盖 / PyPI 镜像覆盖(双镜像,D3)/ 安装明细(状态机五阶段逐项)/ 同步依赖
 * (D4,依赖漂移时出现)/ 可选组件开关(10-05-table-restore R4:首件「表格
 * 还原」按需装进自管环境,零重打包;卸载本期不做)。IPC 契约见 ./pyenv-api.ts
 * (波次钉死,与壳侧 pyenv.rs / pyenv_components.rs 对齐);组件安装本体复用
 * 壳侧安装链依赖段,本卡如实消费命令应答与状态事件,不伪造进度。
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
    hint: "Python 运行环境就绪,sidecar 可正常拉起;已装依赖与随包锁版清单一致,可随时点「检查状态」复验。",
  },
  error: {
    label: "异常",
    badge: "destructive",
    hint: "安装链失败或中断:查看下方明细的失败项,点「重新安装」重试(幂等,已完成的步骤会跳过)。",
  },
  deps_stale: {
    label: "依赖漂移",
    badge: "warning",
    hint:
      "应用更新后随包依赖清单已变(D4):点「同步依赖」幂等重跑安装链,已装依赖会跳过;期间不拦 sidecar 运行。",
  },
};

/** 状态横幅左边框色(随五态;横幅底统一 bg-accent/30)。 */
const STATE_BANNER_CLS: Record<PyenvState, string> = {
  not_configured: "border-border",
  installing: "border-l-2 border-l-warning/60",
  ready: "border-l-2 border-l-ok/60",
  error: "border-l-2 border-l-destructive/60",
  deps_stale: "border-l-2 border-l-warning/60",
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

/** 时间线节点(圆点)随阶段状态的形/色;运行态脉冲不叠转圈(标签位已有 spinner)。 */
function StepDot({ status }: { status: PyenvStepStatus }) {
  const base = "relative z-10 flex size-6 shrink-0 items-center justify-center rounded-full border";
  switch (status) {
    case "done":
      return (
        <span className={cn(base, "border-ok/50 bg-ok/15 text-ok")}>
          <Check className="size-3.5" />
        </span>
      );
    case "running":
      return (
        <span className={cn(base, "border-warning/60 bg-warning/15 text-warning")}>
          <span className="size-2 animate-pulse rounded-full bg-warning" />
        </span>
      );
    case "failed":
      return (
        <span className={cn(base, "border-destructive/60 bg-destructive/15 text-destructive")}>
          <X className="size-3.5" />
        </span>
      );
    default:
      return (
        <span className={cn(base, "border-border bg-muted/30")}>
          <span className="size-1.5 rounded-full bg-muted-foreground/50" />
        </span>
      );
  }
}

/** 路径展示块(全局版面:全宽 + break-all,长路径不再 truncate 截断)。 */
function PathField({
  testid,
  label,
  description,
  value,
}: {
  testid: string;
  label: string;
  description: string;
  value: string;
}) {
  return (
    <div className="flex flex-col gap-1.5">
      <span className="text-sm font-medium text-foreground">{label}</span>
      <p className="text-2xs leading-4 text-muted-foreground">{description}</p>
      <code
        data-testid={testid}
        title={value}
        className="break-all rounded-md border border-border/60 bg-muted/40 px-3 py-2 font-mono text-2xs leading-5 text-foreground/80"
      >
        {value}
      </code>
    </div>
  );
}

/** 镜像覆盖输入(全局版面:label 上/输入全宽/hint 下,不走 w-64 右置控件族)。 */
function MirrorField({
  label,
  labelHint,
  hint,
  placeholder,
  value,
  onChange,
}: {
  label: string;
  /** 高困惑字段的问号提示(10-05-ui-chore-batch ①):有值时 label 旁挂 LabelHint */
  labelHint?: string;
  hint: string;
  placeholder: string;
  value: string;
  onChange: (event: React.ChangeEvent<HTMLInputElement>) => void;
}) {
  const id = useId();
  return (
    <div className="flex flex-col gap-1.5">
      {/* 问号按钮在 label 外(labelable element 不得嵌 label,见 label-hint.tsx 头注) */}
      <div className="flex items-center gap-1">
        <label htmlFor={id} className="text-sm font-medium text-foreground">
          {label}
        </label>
        {labelHint ? <HintButton name={label} tip={labelHint} /> : null}
      </div>
      <Input id={id} aria-label={label} placeholder={placeholder} value={value} onChange={onChange} />
      <p className="text-2xs leading-4 text-muted-foreground">{hint}</p>
    </div>
  );
}

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

/**
 * 已知组件的展示文案(10-05-table-restore):注册表(components.json)是壳侧
 * 功能面(id/pip_spec/指纹)的唯一权威且只在壳侧消费;status.components[]
 * 契约两键钉死({id, installed}),展示文案归前端展示层——已知 id 用此处
 * 中文文案,未知 id 退回原 id 不拦渲染。
 */
const COMPONENT_META: Record<string, { label: string; description: string }> = {
  table: {
    label: "表格还原",
    description:
      "截图表格(行情/比价/参数对比/榜单)还原成结构化 Markdown:rapid_table 3.x onnx 引擎(与 extras myssia[table] 同栈闭包,含 rapidocr 单元格文字;不引 Paddle)。开关开 = 往自管环境装组件(首装联网,PyPI 镜像覆盖生效;SLANET-plus 结构模型首用时自动从 modelscope 下载,之后离线复用);管线侧行为由品类配置 images.table 控制",
  },
};

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
    setVerifyProblems(null);
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

  /** 检查状态(就绪态主按钮,10-05 主人判例):三查只读零副作用;
   *  未过 → 问题逐项上屏并给出「重新安装」入口(幂等链,已装步跳过)。 */
  const [verifyBusy, setVerifyBusy] = useState(false);
  const [verifyProblems, setVerifyProblems] = useState<PyenvVerifyCheck[] | null>(null);

  const handleVerify = useCallback(async () => {
    setVerifyBusy(true);
    setActionError(null);
    setNote(null);
    setVerifyProblems(null);
    try {
      const result = await pyenvVerify();
      if (result.ok) {
        setNote("检查通过:python 可执行、依赖指纹一致、sidecar 握手正常。");
      } else {
        setVerifyProblems(result.checks.filter((check) => !check.ok));
      }
    } catch (raw) {
      setActionError(asSidecarError(raw));
    } finally {
      setVerifyBusy(false);
    }
  }, []);

  /** 组件开关(10-05-table-restore R4):off→on = pyenv_install_component 装
   *  进自管环境(装后拉取回读,components[] 随新);on→off = 卸载本期不做,
   *  如实提示不伪造关闭。与主链动作(开始配置/同步依赖)反馈分槽,互不覆写。 */
  const [installingComponent, setInstallingComponent] = useState<string | null>(null);
  const [componentError, setComponentError] = useState<SidecarRequestError | null>(null);
  const [componentNote, setComponentNote] = useState<{ text: string; ok: boolean } | null>(null);

  const handleToggleComponent = useCallback(
    async (component: PyenvComponent, next: boolean) => {
      if (!next) {
        setComponentError(null);
        setComponentNote({
          text: "组件卸载本期未提供(档记后续):停用表格还原请把品类配置的 images.table 关掉;此处开关只管装进自管环境。",
          ok: false,
        });
        return;
      }
      setInstallingComponent(component.id);
      setComponentError(null);
      setComponentNote(null);
      try {
        const outcome = await pyenvInstallComponent(component.id);
        if (outcome.error) {
          setComponentNote({ text: `组件 ${component.id} 安装失败:${outcome.error}`, ok: false });
        } else {
          setComponentNote({
            text: `组件 ${component.id} 已装进自管环境(指纹已记;可重开幂等跳过)。`,
            ok: true,
          });
        }
        // 拉取是真相源:按结果回读状态(components[] 随新;镜像草稿不覆写)
        applyStatus(await pyenvGetStatus(), false);
      } catch (raw) {
        setComponentError(asSidecarError(raw));
      } finally {
        setInstallingComponent(null);
      }
    },
    [applyStatus],
  );

  const meta = status !== null ? STATE_META[status.state] : null;

  return (
    <Card data-testid="pyenv-card">
      <CardContent className="flex flex-col gap-6">
        {loadError ? <ErrorBox error={loadError} onRetry={() => void refresh()} /> : null}
        {status === null && loadError === null ? (
          <span data-testid="pyenv-loading" className="py-2 text-xs text-muted-foreground">
            环境状态装载中…
          </span>
        ) : null}

        {status !== null && meta ? (
          <>
            {/* 状态横幅:徽标 + 引导语,左边框随五态着色 */}
            <div className={cn("rounded-lg border bg-accent/30 p-4", STATE_BANNER_CLS[status.state])}>
              <div className="flex flex-wrap items-center gap-2">
                <Cpu className="size-4 text-muted-foreground" />
                <Badge variant={meta.badge} data-testid="pyenv-state-badge">
                  {meta.label}
                </Badge>
                <span className="text-2xs text-muted-foreground">当前环境状态</span>
              </div>
              <p data-testid="pyenv-state-hint" className="mt-2 text-xs leading-5 text-foreground/80">
                {meta.hint}
              </p>
            </div>

            {/* 环境信息:全宽路径块 */}
            <section aria-labelledby="pyenv-paths-title" className="flex flex-col gap-3">
              <h3 id="pyenv-paths-title" className="text-2xs font-medium tracking-wide text-muted-foreground">
                环境信息
              </h3>
              <PathField
                testid="pyenv-install-path"
                label="安装路径"
                description="install_only 包解压即得(数据根下,与 models/ 并排;绝不写安装目录)"
                value={status.install_path}
              />
              <PathField
                testid="pyenv-python-path"
                label="Python 使用路径"
                description="sidecar spawn 源(壳侧拉起自管 Python 的二进制)"
                value={status.python_path}
              />
            </section>

            {/* 双镜像覆盖(D3):镜像只换 URL 不绕 sha256 校验;空 = 默认源 */}
            <section aria-labelledby="pyenv-mirrors-title" className="flex flex-col gap-3">
              <h3 id="pyenv-mirrors-title" className="text-2xs font-medium tracking-wide text-muted-foreground">
                镜像源覆盖(可选)
              </h3>
              <MirrorField
                label="运行时下载源覆盖"
                labelHint="下载 Python 本体慢或不通时,把下载地址换成国内镜像站上同一个文件的地址。留空 = 官方源。只换下载地址,文件完整性校验照做,不会下到被改过的包。"
                hint="空 = 随包 manifest 钉版源(indygreg python-build-standalone cpython 3.12.7);镜像只换 URL,不绕 sha256 校验"
                placeholder="https://mirror.example/cpython-3.12.7-…-install_only.tar.gz"
                value={mirrorRuntime}
                onChange={(event) => setMirrorRuntime(event.target.value)}
              />
              <MirrorField
                label="PyPI 镜像覆盖"
                labelHint="装 Python 依赖包慢时,填国内镜像站地址(如清华、阿里)。留空 = 官方源。只改去哪儿下载,不影响装什么、装哪个版本。"
                hint="空 = 默认 PyPI;依赖安装(pip install --index-url)取此值"
                placeholder="https://pypi.tuna.tsinghua.edu.cn/simple"
                value={mirrorPypi}
                onChange={(event) => setMirrorPypi(event.target.value)}
              />
            </section>

            {/* 安装明细(design §3 状态机逐项;五阶段骨架恒在,steps 补态)。
                全局版面:五阶段竖向时间线(圆点 + 连接线),非密集行堆 */}
            <section aria-labelledby="pyenv-steps-title" className="flex flex-col gap-3">
              <h3 id="pyenv-steps-title" className="text-2xs font-medium tracking-wide text-muted-foreground">
                安装明细(失败可重试,已装步幂等跳过)
              </h3>
              <ol data-testid="pyenv-steps" className="flex flex-col">
                {mergedSteps(status.steps).map(({ phase, status: stepStatus, error }, index, all) => {
                  const stepMeta = STEP_STATUS_META[stepStatus];
                  return (
                    <li key={phase} data-testid={`pyenv-step-${phase}`} className="relative flex gap-3 pb-5 last:pb-0">
                      {index < all.length - 1 ? (
                        <span aria-hidden className="absolute bottom-0 left-[11px] top-7 w-px bg-border" />
                      ) : null}
                      <StepDot status={stepStatus} />
                      <div className="flex min-w-0 flex-1 flex-col gap-1 pt-0.5">
                        <div className="flex flex-wrap items-center justify-between gap-2">
                          <span className="text-sm text-foreground">{PHASE_LABEL[phase]}</span>
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
                    </li>
                  );
                })}
              </ol>
            </section>

            {/* 可选组件(10-05-table-restore R4):首件「表格还原」;装/状态回读
                如实呈现,卸载本期不做。注册表缺位(旧包)→ components 空 → 不渲染 */}
            {status.components.length > 0 ? (
              <section aria-labelledby="pyenv-components-title" className="flex flex-col gap-3">
                <h3 id="pyenv-components-title" className="text-2xs font-medium tracking-wide text-muted-foreground">
                  可选组件(按需装进自管环境,零重打包)
                </h3>
                <div
                  data-testid="pyenv-components"
                  className="flex flex-col divide-y divide-border/60 rounded-lg border border-border/60"
                >
                  {status.components.map((component) => {
                    const display = COMPONENT_META[component.id];
                    // 环境未配置/主链安装中:开关禁用(壳侧同门,前端先拦一道)
                    const envBlocked =
                      status.state === "not_configured" || status.state === "installing";
                    const busy = installingComponent === component.id;
                    return (
                      <div
                        key={component.id}
                        data-testid={`pyenv-component-${component.id}`}
                        className="flex flex-wrap items-center justify-between gap-3 p-4"
                      >
                        <div className="flex min-w-0 flex-1 flex-col gap-1">
                          <span className="text-sm font-medium text-foreground">
                            {display?.label ?? component.id}
                          </span>
                          <p className="text-2xs leading-4 text-muted-foreground">
                            {display?.description ?? "自管环境可选组件(按需安装)"}
                          </p>
                          {busy ? (
                            <span
                              role="status"
                              data-testid={`pyenv-component-${component.id}-busy`}
                              className="flex items-center gap-1 text-2xs text-warning"
                            >
                              <RefreshCw className="size-3 animate-spin" />
                              安装中(下载依赖,可能耗时数分钟)…
                            </span>
                          ) : null}
                        </div>
                        <div className="flex shrink-0 items-center gap-2">
                          <Badge
                            variant={component.installed ? "ok" : "outline"}
                            data-testid={`pyenv-component-${component.id}-state`}
                          >
                            {component.installed ? "已装" : "未装"}
                          </Badge>
                          <Switch
                            checked={component.installed}
                            disabled={busy || envBlocked}
                            aria-label={`组件开关 ${component.id}`}
                            title={
                              envBlocked
                                ? "Python 环境未就位/主链安装中:先完成「开始配置」再装组件"
                                : component.installed
                                  ? "已装进自管环境;卸载本期未提供(停用走品类配置 images.table)"
                                  : "往自管环境装该组件(pip,镜像覆盖生效)"
                            }
                            onCheckedChange={(checked) =>
                              void handleToggleComponent(component, checked)
                            }
                          />
                        </div>
                      </div>
                    );
                  })}
                </div>
                {componentError ? <ErrorBox error={componentError} /> : null}
                {componentNote ? (
                  <p
                    role={componentNote.ok ? "status" : "alert"}
                    data-testid="pyenv-component-note"
                    className={componentNote.ok ? "text-xs text-ok" : "text-xs text-destructive"}
                  >
                    {componentNote.text}
                  </p>
                ) : null}
              </section>
            ) : null}

            {/* 动作条:反馈在左、动作在右(全宽,主按钮不再 sm 收缩);同步依赖仅漂移态出现(D4)。
                10-05 主人判例:主按钮语义按态分家——就绪=「检查状态」(三查只读)、
                异常=「重新安装」(幂等链)、未配置/漂移=「开始配置」;体检未过时
                追加「重新安装」入口(状态不对就重装) */}
            <div className="flex flex-wrap items-center justify-between gap-3 border-t border-border/60 pt-4">
              <div className="min-w-0 flex-1">
                {actionError ? <ErrorBox error={actionError} /> : null}
                {verifyProblems ? (
                  <div
                    role="alert"
                    data-testid="pyenv-verify-problems"
                    className="flex flex-col gap-0.5 text-left text-2xs leading-4 text-destructive"
                  >
                    {verifyProblems.map((check) => (
                      <span key={check.id} data-testid={`pyenv-verify-problem-${check.id}`}>
                        [{check.id}] {check.detail}
                      </span>
                    ))}
                  </div>
                ) : null}
                {note ? (
                  <p role="status" data-testid="pyenv-action-note" className="text-xs text-ok">
                    {note}
                  </p>
                ) : null}
              </div>
              <div className="flex flex-wrap items-center gap-2">
                {status.state === "deps_stale" ? (
                  <Button
                    variant="outline"
                    onClick={() => void handleSyncDeps()}
                    disabled={syncBusy || setupBusy}
                    data-testid="pyenv-sync-deps"
                    title="D4:幂等重跑依赖安装链,已装依赖会跳过"
                  >
                    <RefreshCw className={syncBusy ? "size-4 animate-spin" : "size-4"} />
                    同步依赖
                  </Button>
                ) : null}
                {verifyProblems ? (
                  <Button
                    variant="outline"
                    onClick={() => void handleStartSetup()}
                    disabled={setupBusy || syncBusy}
                    data-testid="pyenv-reinstall-button"
                    title="体检未过:幂等重跑安装链(下载→校验→解压→依赖→自检,已装步跳过)"
                  >
                    <Download className="size-4" />
                    重新安装
                  </Button>
                ) : null}
                {status.state === "ready" ? (
                  <Button
                    onClick={() => void handleVerify()}
                    disabled={verifyBusy || setupBusy || syncBusy}
                    data-testid="pyenv-verify-button"
                    title="三查:python 可执行 / 依赖指纹 / sidecar 握手;只读零副作用,查出错给重装入口"
                  >
                    <ShieldCheck className={verifyBusy ? "size-4 animate-pulse" : "size-4"} />
                    检查状态
                  </Button>
                ) : (
                  <Button
                    onClick={() => void handleStartSetup()}
                    disabled={setupBusy || syncBusy || status.state === "installing"}
                    data-testid="pyenv-start-setup"
                    title="D2:显式开始配置(下载→校验→解压→依赖→自检);安装中不可重复触发;已装步幂等跳过"
                  >
                    <Download className={setupBusy ? "size-4 animate-pulse" : "size-4"} />
                    {status.state === "error" ? "重新安装" : status.state === "installing" ? "安装中…" : "开始配置"}
                  </Button>
                )}
              </div>
            </div>
          </>
        ) : null}
      </CardContent>
    </Card>
  );
}
