import { AlertTriangle, Check, Clock, Cpu, Download, Play, RefreshCw, ShieldCheck, Square, X } from "lucide-react";
import { useCallback, useEffect, useState } from "react";

import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import type { SidecarRequestError } from "@/lib/api";
import { cn } from "@/lib/utils";

import { asSidecarError } from "./api";
import { ErrorBox } from "./error-box";
import { FieldInput } from "./field-input";
import {
  onPyenvStatusChanged,
  pyenvGetStatus,
  pyenvInstallComponent,
  pyenvStartSetup,
  pyenvSyncDeps,
  pyenvVerify,
  serviceStart,
  serviceStatus,
  serviceStop,
  PYENV_PHASE_ORDER,
  type PyenvComponent,
  type PyenvState,
  type PyenvStatus,
  type PyenvPhase,
  type PyenvStep,
  type PyenvStepStatus,
  type PyenvVerifyCheck,
  type ServiceStatus,
} from "./pyenv-api";

/**
 * 「Python 运行环境」分区(10-05-desktop-managed-py-env 第 4 步;design §5)。
 *
 * 2026-10-05 晚主人再裁(10-05-pyenv-settings-unify):本区撤特殊化回归
 * 标准分区版面——设置导航常驻、内容列比例列宽;卡补 CardHeader(与其他
 * 设置卡同款),镜像输入回 FieldInput 行(label 左/输入右 w-64,labelHint
 * 问号提示由 FieldInput 内建)。状态横幅/路径块 break-all/五阶段时间线/
 * 底部动作条为内容本体,原样保留。
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
      "Python 运行时与依赖不随安装包分发;点「开始配置」在线下载安装,全程状态见下方明细。首次运行需联网,离线无法完成配置。",
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
    label: "依赖待更新",
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

/** 慢启动健康对账轮询参数(复审修复:回执「稍后以状态对账为准」的兑现面)。
 *  每 5s 一次 × 上限 24 次 ≈ 2 分钟——绿即停,超限放弃(真故障看日志)。 */
const SERVICE_HEALTH_POLL_INTERVAL_MS = 5_000;
const SERVICE_HEALTH_POLL_MAX_ATTEMPTS = 24;

/** 状态机五阶段中文标(design §3:downloading→…→selfcheck)。 */
const PHASE_LABEL: Record<PyenvPhase, string> = {
  downloading: "下载运行时",
  verifying: "校验 sha256",
  extracting: "解压到数据目录",
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
 * 轨B 服务组件(10-06-native-plugin-components 阶段2)的启停交互语义:
 * 装好默认停(G-Q5),启停只走本卡按钮;健康绿点 = service_status 对账的
 * healthy(2xx),stopped 恒灰;启停动作后按回包如实翻态(不伪造进度)。
 */
const COMPONENT_META: Record<string, { label: string; description: string }> = {
  table: {
    label: "表格还原",
    description:
      "依赖 rapid_table + rapidocr-onnxruntime,把截图表格还原成 Markdown;首装联网拉 SLANET 模型(6.8MB)",
  },
  trafilatura: {
    label: "正文抽取兜底",
    description:
      "依赖 trafilatura + selectolax:网页正文抽取缺失时自动补抽,默认关(MYIA_EXTRACT_FALLBACK=1 才启用)",
  },
  crawl4ai: {
    label: "JS 渲染抓取(crawl4ai)",
    description:
      "依赖 crawl4ai + playwright,无头浏览器渲染纯客户端页面;附带下载 Chromium 约 600MB,耗时数分钟",
  },
  telethon: {
    label: "Telegram 用户线(telethon)",
    description:
      "依赖 telethon(纯 Python 轻量):用自己的 Telegram 账号读已加入的群(bot 进不去的群)",
  },
  searxng: {
    label: "关键词日报(SearXNG)",
    description:
      "依赖 SearXNG(GitHub 钉版源码)+ granian,自托管聚合搜索约 100MB;装好默认停,手动启停",
  },
  "wechat-bridge": {
    label: "微信本机桥(wechat-bridge)",
    description:
      "依赖 pyobjc + pillow:像素链读微信会话 + 本地库只读(sqlcipher)",
  },
};

/**
 * 组件安装按钮(10-13-component-install-ux;主人指令「状态就表现在按钮
 * 效果上面」):一行一按钮,安装全生命周期五态由按钮本体承载——
 * 安装(可点)/ 安装中…(转圈)/ 排队中…/ 已装 / 重试安装(附失败小字)。
 * 状态真源 = status.components[].install_state(壳侧广播 + 拉取,切屏
 * 重开不丢);pending 仅做点击 → 受理回执间隙的防双击过渡。
 */
function ComponentInstallButton({
  component,
  envBlocked,
  pending,
  onInstall,
}: {
  component: PyenvComponent;
  /** 主链未配置/安装中:一切安装动作禁用(壳侧同门,前端先拦一道) */
  envBlocked: boolean;
  pending: boolean;
  onInstall: () => void;
}) {
  const testId = `pyenv-component-${component.id}-install`;
  // pending 优先于一切态(点击瞬间到回执/事件到达前,按钮必须不可再点)
  const installState = pending ? ("installing" as const) : component.install_state;
  const blockedTitle = envBlocked
    ? "Python 环境未就位/主链安装中:先完成「开始配置」再装组件"
    : null;

  if (installState === "installing") {
    return (
      <Button variant="outline" size="sm" disabled data-testid={testId} title={blockedTitle ?? "下载依赖+按需拉浏览器,可能耗时数分钟;完成后按钮自动变「已装」"}>
        <RefreshCw className="size-3.5 animate-spin" />
        安装中…
      </Button>
    );
  }
  if (installState === "queued") {
    return (
      <Button variant="outline" size="sm" disabled data-testid={testId} title={blockedTitle ?? "等前面的组件装完自动开装(同刻只装一个,防互踩);壳重启会清空队列,重新点「安装」即可"}>
        <Clock className="size-3.5" />
        排队中…
      </Button>
    );
  }
  if (component.installed) {
    return (
      <Button
        variant="outline"
        size="sm"
        disabled
        data-testid={testId}
        className="border-ok/40 text-ok hover:bg-ok/[0.04]"
        title="已装进应用管理的环境;卸载将在后续版本提供(停用请调整品类/源配置不再引用该组件)"
      >
        <Check className="size-3.5" />
        已装
      </Button>
    );
  }
  if (installState === "error") {
    return (
      <Button
        variant="outline"
        size="sm"
        disabled={envBlocked}
        onClick={onInstall}
        data-testid={testId}
        className="border-warning/50 text-warning hover:bg-warning/[0.06]"
        title={blockedTitle ?? "上次安装失败;点此重试(幂等:已装依赖自动跳过,浏览器二进制续装)"}
      >
        <AlertTriangle className="size-3.5" />
        重试安装
      </Button>
    );
  }
  return (
    <Button size="sm" disabled={envBlocked} onClick={onInstall} data-testid={testId} title={blockedTitle ?? "把该组件装进应用管理的环境(pip,镜像覆盖生效);已有组件在装时自动排队"}>
      <Download className="size-3.5" />
      安装
    </Button>
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

  /** 组件安装(10-13-component-install-ux 主人指令:状态进按钮,一行一
   * 按钮):点击 → 受理制回执(占槽开装 / 入队)→ 拉真值(install_state
   * 是渲染真源)。Err 只剩结构性拒绝(未知 id / 环境未就位——envBlocked
   * 已先拦,真 Err 罕见)仍走 ErrorBox 如实呈现;完成/失败态走事件 +
   * 拉取,回执不做进度承诺。卸载本期不做,不提供关闭动作。 */
  const [installPendingId, setInstallPendingId] = useState<string | null>(null);
  const [componentError, setComponentError] = useState<SidecarRequestError | null>(null);
  const [componentNote, setComponentNote] = useState<{ text: string; ok: boolean } | null>(null);

  const handleInstallComponent = useCallback(
    async (component: PyenvComponent) => {
      setInstallPendingId(component.id);
      setComponentError(null);
      setComponentNote(null);
      try {
        const outcome = await pyenvInstallComponent(component.id);
        setComponentNote(
          outcome.queued
            ? { text: `组件 ${component.id} 已排队:等前面的组件装完自动开装(同刻只装一个)。`, ok: true }
            : {
                text: `组件 ${component.id} 安装已开始(下载依赖,可能耗时数分钟;完成自动刷新)。`,
                ok: true,
              },
        );
        // 拉取是真相源:安装中/排队态以回读为准(镜像草稿不覆写)
        applyStatus(await pyenvGetStatus(), false);
      } catch (raw) {
        setComponentError(asSidecarError(raw));
      } finally {
        setInstallPendingId(null);
      }
    },
    [applyStatus],
  );

  /** 服务组件实况(轨B:已装服务行初拉/事件刷新后对账;启停回包如实翻态)。
   *  healthy = service_status 对账真值(健康端点 2xx);stopped 恒无绿点。 */
  const [serviceStates, setServiceStates] = useState<Record<string, ServiceStatus>>({});
  const [serviceBusy, setServiceBusy] = useState<string | null>(null);
  const [serviceError, setServiceError] = useState<SidecarRequestError | null>(null);
  const [serviceNote, setServiceNote] = useState<{ text: string; ok: boolean } | null>(null);

  const refreshServiceStatus = useCallback(async (id: string): Promise<ServiceStatus | null> => {
    try {
      const next = await serviceStatus(id);
      setServiceStates((prev) => ({ ...prev, [id]: next }));
      return next;
    } catch (raw) {
      // 探测失败不拦渲染(按钮仍可用;错误如实给一次,不覆写动作回执)
      setServiceError(asSidecarError(raw));
      return null;
    }
  }, []);

  /** 状态刷新时对已装服务行批量对账(初拉/事件/装完回读共用一条通道)。 */
  useEffect(() => {
    if (status === null) return;
    for (const component of status.components) {
      if (component.kind === "service" && component.installed) {
        void refreshServiceStatus(component.id);
      }
    }
  }, [status, refreshServiceStatus]);

  /**
   * 慢启动健康对账轮询(复审修复 10-06-native-plugin-components):启动回包
   * running+healthy=false 时,回执承诺「稍后以状态对账为准」但原先无任何自动
   * 触发源——健康点滞留黄闪直到用户切屏重挂载。本轮询每 5s 对账一次,绿即停,
   * 上限 24 次(约 2 分钟)自动放弃(持续未绿 = 实例真故障,日志指引已在回执)。
   */
  const [healthPoll, setHealthPoll] = useState<{ id: string; attempts: number } | null>(null);

  useEffect(() => {
    if (healthPoll === null) return;
    if (healthPoll.attempts >= SERVICE_HEALTH_POLL_MAX_ATTEMPTS) {
      setHealthPoll(null);
      return;
    }
    let cancelled = false;
    const timer = setTimeout(() => {
      void refreshServiceStatus(healthPoll.id).then((next) => {
        if (cancelled) return;
        // 绿即停;stopped(预热失败退出)/探测失败 → 继续按次计,至上限
        if (next?.state === "running" && next.healthy) {
          setHealthPoll(null);
        } else {
          setHealthPoll((prev) =>
            prev && prev.id === healthPoll.id ? { ...prev, attempts: prev.attempts + 1 } : prev,
          );
        }
      });
    }, SERVICE_HEALTH_POLL_INTERVAL_MS);
    return () => {
      cancelled = true;
      clearTimeout(timer);
    };
  }, [healthPoll, refreshServiceStatus]);

  /** 服务启停(G-Q5:显式动作;回包如实翻态 + 回执,不伪造进度)。 */
  const handleServiceToggle = useCallback(
    async (component: PyenvComponent, start: boolean) => {
      setServiceBusy(component.id);
      setServiceError(null);
      setServiceNote(null);
      setHealthPoll(null); // 新动作重置旧轮询(对账口径以最新动作回包为准)
      try {
        const outcome = start ? await serviceStart(component.id) : await serviceStop(component.id);
        setServiceStates((prev) => ({ ...prev, [component.id]: outcome }));
        if (start && outcome.state === "running" && !outcome.healthy) {
          setHealthPoll({ id: component.id, attempts: 0 }); // 慢启动:起轮询对账
        }
        setServiceNote(
          start
            ? outcome.state === "running" && outcome.healthy
              ? { text: `服务 ${component.id} 已启动且健康检查通过(进程 pid=${outcome.pid})。`, ok: true }
              : { text: `服务 ${component.id} 已启动(pid=${outcome.pid})但健康端点尚未通过——实例可能在预热,本页每 ${SERVICE_HEALTH_POLL_INTERVAL_MS / 1000}s 自动核对一次(状态变绿即停);持续未绿请查数据目录 services/${component.id}/service.log。`, ok: false }
            : { text: `服务 ${component.id} 已停止(进程组退出,零残留)。`, ok: true },
        );
      } catch (raw) {
        setServiceError(asSidecarError(raw));
      } finally {
        setServiceBusy(null);
      }
    },
    [],
  );

  const meta = status !== null ? STATE_META[status.state] : null;

  return (
    <Card data-testid="pyenv-card">
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          <Cpu className="size-4 text-muted-foreground" />
          环境状态与安装
        </CardTitle>
        <CardDescription>
          状态随安装链实时刷新;下载源镜像可选(只换地址,不绕完整性校验),异常可幂等重装
        </CardDescription>
      </CardHeader>
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
                description="install_only 包解压即得(数据目录下,与 models/ 并排;绝不写安装目录)"
                value={status.install_path}
              />
              <PathField
                testid="pyenv-python-path"
                label="Python 使用路径"
                description="sidecar spawn 源(桌面壳启动应用管理的 Python)"
                value={status.python_path}
              />
            </section>

            {/* 双镜像覆盖(D3):镜像只换 URL 不绕 sha256 校验;空 = 默认源。
                行式回归 FieldInput(label 左/输入右 w-64,labelHint 问号内建),
                与全设置屏输入行同一词汇 */}
            <section aria-labelledby="pyenv-mirrors-title" className="flex flex-col gap-3">
              <h3 id="pyenv-mirrors-title" className="text-2xs font-medium tracking-wide text-muted-foreground">
                镜像源覆盖(可选)
              </h3>
              <div className="divide-y divide-border/60">
                <FieldInput
                  label="运行时下载源覆盖"
                  aria-label="运行时下载源覆盖"
                  placeholder="https://mirror.example/cpython-3.12.7-…-install_only.tar.gz"
                  value={mirrorRuntime}
                  onChange={(event) => setMirrorRuntime(event.target.value)}
                  labelHint="下载 Python 本体慢或不通时,把下载地址换成国内镜像站上同一个文件的地址。留空 = 官方源。只换下载地址,文件完整性校验照做,不会下到被改过的包。"
                  hint="空 = 随包 manifest 钉版源(indygreg python-build-standalone cpython 3.12.7);镜像只换 URL,不绕 sha256 校验"
                />
                <FieldInput
                  label="PyPI 镜像覆盖"
                  aria-label="PyPI 镜像覆盖"
                  placeholder="https://pypi.tuna.tsinghua.edu.cn/simple"
                  value={mirrorPypi}
                  onChange={(event) => setMirrorPypi(event.target.value)}
                  labelHint="装 Python 依赖包慢时,填国内镜像站地址(如清华、阿里)。留空 = 官方源。只改去哪儿下载,不影响装什么、装哪个版本。"
                  hint="空 = 默认 PyPI;依赖安装(pip install --index-url)取此值"
                />
              </div>
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

            {/* 可选组件(10-05-table-restore R4;10-13-component-install-ux
                按钮化):状态进按钮(主人指令「状态就表现在按钮效果上面」)——
                安装/安装中/排队中/已装/重试安装五态单按钮承载,取代
                Badge+开关+旁挂 spinner 三处散落;安装态真源 =
                status.components[].install_state(壳侧广播/拉取,切屏重开不丢)。
                注册表缺位(旧包)→ components 空 → 不渲染 */}
            {status.components.length > 0 ? (
              <section aria-labelledby="pyenv-components-title" className="flex flex-col gap-3">
                <h3 id="pyenv-components-title" className="text-2xs font-medium tracking-wide text-muted-foreground">
                  可选组件(按需安装,零重打包)
                </h3>
                <div
                  data-testid="pyenv-components"
                  className="flex flex-col divide-y divide-border/60 rounded-lg border border-border/60"
                >
                  {status.components.map((component) => {
                    const display = COMPONENT_META[component.id];
                    // 环境未配置/主链安装中:安装按钮禁用(壳侧同门,前端先拦一道)
                    const envBlocked =
                      status.state === "not_configured" || status.state === "installing";
                    const pending = installPendingId === component.id;
                    // 轨B 服务组件(已装):启停按钮 + 健康绿点(启停本就是按钮态;
                    // 状态未知时按 stopped 呈现,对账毫秒级即至)
                    const service = component.kind === "service" && component.installed;
                    const running = service && (serviceStates[component.id]?.state ?? "stopped") === "running";
                    const healthy = Boolean(running && serviceStates[component.id]?.healthy);
                    const serviceToggleBusy = serviceBusy === component.id;
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
                            {display?.description ?? "可选组件(按需安装)"}
                          </p>
                          {component.install_state === "error" && component.install_error ? (
                            <p
                              role="alert"
                              data-testid={`pyenv-component-${component.id}-error`}
                              className="text-left text-2xs leading-4 text-destructive"
                            >
                              上次安装失败:{component.install_error}(重试幂等,已装依赖自动跳过)
                            </p>
                          ) : null}
                          {serviceToggleBusy ? (
                            <span
                              role="status"
                              data-testid={`pyenv-service-${component.id}-busy`}
                              className="flex items-center gap-1 text-2xs text-warning"
                            >
                              <RefreshCw className="size-3 animate-spin" />
                              {running ? "停止中(SIGTERM 进程组,宽限内未退会升级强杀)…" : "启动中(等待健康端点通过,冷启动秒级)…"}
                            </span>
                          ) : null}
                        </div>
                        <div className="flex shrink-0 items-center gap-2">
                          {service ? (
                            <>
                              <Badge
                                variant={running ? "ok" : "outline"}
                                data-testid={`pyenv-service-${component.id}-run-state`}
                              >
                                {running ? "运行中" : "已停止"}
                              </Badge>
                              <span
                                data-testid={`pyenv-service-${component.id}-health`}
                                title={
                                  running
                                    ? healthy
                                      ? "健康端点 /healthz 返回 2xx"
                                      : "运行中但健康端点未过(实例内部故障/慢启动;日志见数据目录 services 目录)"
                                    : "服务未运行(装好默认停;点「启动」拉起)"
                                }
                                aria-label={`服务健康 ${component.id}`}
                                className={cn(
                                  "flex size-2.5 rounded-full",
                                  running ? (healthy ? "bg-ok" : "bg-warning animate-pulse") : "bg-muted-foreground/40",
                                )}
                              />
                              <Button
                                variant="outline"
                                size="sm"
                                onClick={() => void handleServiceToggle(component, !running)}
                                disabled={serviceToggleBusy || envBlocked}
                                data-testid={`pyenv-service-${component.id}-${running ? "stop" : "start"}`}
                                title={
                                  running
                                    ? "SIGTERM 进程组(覆盖 granian 子进程树)→ 宽限 → SIGKILL 兜底;停止后状态记忆为已停止"
                                    : "拉起服务进程组并等待健康端点通过;装好默认停,启停只走此按钮(引擎不隐式拉起)"
                                }
                              >
                                {running ? <Square className="size-3.5" /> : <Play className="size-3.5" />}
                                {running ? "停止" : "启动"}
                              </Button>
                            </>
                          ) : (
                            <ComponentInstallButton
                              component={component}
                              envBlocked={envBlocked}
                              pending={pending}
                              onInstall={() => void handleInstallComponent(component)}
                            />
                          )}
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
                {serviceError ? <ErrorBox error={serviceError} /> : null}
                {serviceNote ? (
                  <p
                    role={serviceNote.ok ? "status" : "alert"}
                    data-testid="pyenv-service-note"
                    className={serviceNote.ok ? "text-xs text-ok" : "text-xs text-destructive"}
                  >
                    {serviceNote.text}
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
                    title="开始配置(下载 → 校验 → 解压 → 安装依赖 → 自检);安装中不可重复触发;已完成的步骤自动跳过"
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
