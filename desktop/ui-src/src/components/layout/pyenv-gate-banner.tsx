import { ArrowRight, Cpu, X } from "lucide-react";
import { useCallback, useEffect, useRef, useState } from "react";
import { useNavigate } from "react-router-dom";

import { Button } from "@/components/ui/button";
import {
  onPyenvStatusChanged,
  pyenvGetStatus,
  type PyenvState,
} from "@/screens/settings/pyenv-api";

/**
 * Python 环境门禁横幅(10-05-desktop-managed-py-env D2「各屏引导空态卡」,
 * AC2 收尾):环境未就绪(not_configured / installing / error)时在内容区
 * 顶部全局引导——一句人话状态 + 「前往设置」深链(#/settings?section=
 * python-env);ready / deps_stale(不拦 sidecar)不出现。真相源 =
 * pyenv_get_status 初拉 + pyenv-status-changed 事件随动(安装完成自动
 * 消失);关闭只隐本会话,下一个状态事件如实复现。裸 code 报错条的时代
 * 由 ErrorBox 的 pyenv_not_ready 变体与本横幅共同收口。
 */
const GATE_TEXT: Partial<Record<PyenvState, { title: string; detail: string }>> = {
  not_configured: {
    title: "Python 运行环境未配置,功能待配置后可用",
    detail:
      "运行时与依赖不随安装包分发:请在设置的「Python 环境」分区点「开始配置」在线安装(首跑需联网,约一分钟)。",
  },
  installing: {
    title: "Python 运行环境安装中…",
    detail: "下载 → 校验 → 解压 → 依赖 → 自检进行中,完成后本横幅自动消失;进度明细见设置页。",
  },
  error: {
    title: "Python 运行环境异常",
    detail: "安装链失败或中断:请在设置的「Python 环境」分区查看明细并点「重新安装」重试(已装步骤会跳过)。",
  },
};

export function PyenvGateBanner() {
  const [state, setState] = useState<PyenvState | null>(null);
  const [dismissed, setDismissed] = useState(false);
  const stateRef = useRef<PyenvState | null>(null);
  const navigate = useNavigate();

  /** 状态入态;变迁(≠上一态)时复位会话级关闭——新问题应复现引导,
   *  同态进度事件(installing 反复广播)不扰关闭决定。 */
  const apply = useCallback((next: PyenvState) => {
    if (stateRef.current === next) return;
    stateRef.current = next;
    setDismissed(false);
    setState(next);
  }, []);

  useEffect(() => {
    let cancelled = false;
    let unlisten: (() => void) | null = null;
    pyenvGetStatus()
      .then((status) => {
        if (!cancelled) apply(status.state);
      })
      .catch(() => {
        // 浏览器直开/致命盘况:辅助引导不拦主界面,真相源在设置屏 PyenvCard
      });
    // Promise.resolve 包一层:mock/浏览器直开下 listen 可能返回非 Promise
    // (裸 undefined),直接 .then 会在效应里炸(真机恒为 Promise,防御仅测试面)
    void Promise.resolve(
      onPyenvStatusChanged((next) => {
        if (!cancelled) apply(next.state);
      }),
    )
      .then((unlistenFn) => {
        if (cancelled) unlistenFn?.();
        else unlisten = unlistenFn ?? null;
      })
      .catch(() => {
        // 浏览器直开无事件通道:拉取态已够用
      });
    return () => {
      cancelled = true;
      unlisten?.();
    };
  }, [apply]);

  // 仅未就绪三态有引导文案;ready/deps_stale 不拦 sidecar,查表得 undefined 即隐
  const meta = state !== null ? GATE_TEXT[state] : null;
  if (!meta || dismissed) return null;

  return (
    <div
      data-testid="pyenv-gate-banner"
      role="status"
      className="flex items-start gap-3 border-b border-border/60 bg-muted/40 px-4 py-3"
    >
      <Cpu className="mt-0.5 size-4 shrink-0 text-warning" />
      <div className="min-w-0 flex-1">
        <p className="text-sm font-medium text-foreground">{meta.title}</p>
        <p className="mt-1 text-xs leading-5 text-muted-foreground">{meta.detail}</p>
      </div>
      <div className="flex shrink-0 items-center gap-1.5">
        <Button
          size="sm"
          onClick={() => navigate("/settings?section=python-env")}
          data-testid="pyenv-gate-goto-settings"
          title="跳转设置 → Python 环境(开始配置 / 重新安装)"
        >
          前往设置
          <ArrowRight className="size-3.5" />
        </Button>
        <Button
          size="icon"
          variant="ghost"
          onClick={() => setDismissed(true)}
          data-testid="pyenv-gate-close"
          aria-label="关闭引导(本次会话内不再显示)"
          title="关闭引导(本次会话内不再显示)"
        >
          <X className="size-4" />
        </Button>
      </div>
    </div>
  );
}
