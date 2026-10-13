/**
 * 「微信账号」卡(10-11-platform-account-config;2026-10-11 主人令渠道本名制:
 * 自「平台账号」总卡拆出,微信就是微信)。
 *
 * 受限形态(裁定 D3):微信登录态由本机 Hermes-Agent 持有,MYIA 红线 =
 * 不读不写 Hermes 私有目录——本卡零新契约,只做桥接状态灯(三布尔,直读
 * probe_bridge)+ 登录指引(`hermes gateway setup` 终端扫码)+ 单活模型
 * 诚实披露。账号档列表/卡内登录/删除待上游契约后开放。
 *
 * 10-13-wechat-keyprovider B5:卡底新增「取钥器」配置行(微信桥配置分区既有
 * 版面内加行,不新造卡)——路径输入 + 三态(已配置/未配置/文件缺失)+ 未配置
 * 引导文案(指向 docs/wechat-keyprovider.md);读写经壳侧 Tauri 命令
 * spawn 桥 `localdb key-provider set/get/clear`,配置落桥自有 config.json。
 *
 * 10-13-wechat-monitor-ui A2/A3:取钥器行上方插入「数据库密钥」状态行
 * (因果序 = 状态→行动→工具配置;三态 ready/stale/missing = 壳侧
 * `wechat_key_status` 真源)+ 卡内三步获取面板(idle→confirm→running→result
 * 状态机;progress 消费 `wechat-key-acquire` 事件,seq 单调丢弃乱序旧包)。
 * 文案判例(硬):调试器/内部机制类协议行话(词表见任务档 design §4)永
 * 不上屏,人话词面逐字走 §4 文案表与 §D.3 阶段词表(如 attach 一律说
 * 「正在连接微信」)。
 *
 * 10-13-wechat-monitor-ui E2:未配置态追加「一键安装取钥器」行(D3 装机后
 * 首用引导;源在场=部署件束暂存目录入口件在场,壳侧 inspect)——安装 =
 * cp+700 到数据根私有区 bin/ 后自动经桥管理命令 set 保存路径;源不在 =
 * 引导文案(自带可执行件走路径输入)。
 */
import { Check, Copy, Save, User } from "lucide-react";
import { useCallback, useEffect, useRef, useState } from "react";

import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import type { SidecarRequestError as SidecarRequestErrorType } from "@/lib/api";
import { cn } from "@/lib/utils";

import { asSidecarError } from "./api";
import { ErrorBox } from "./error-box";
import { FieldInput } from "./field-input";
import { platformAccountsGetStatus } from "./platform-accounts-api";
import {
  KEY_ACQUIRE_PHASE_LABELS,
  KEY_ACQUIRE_STEP_PHASES,
  cancelKeyAcquire,
  keyProviderView,
  startKeyAcquire,
  subscribeKeyAcquire,
  wechatKeyProviderClear,
  wechatKeyProviderGet,
  wechatKeyProviderInspect,
  wechatKeyProviderInstall,
  wechatKeyProviderSet,
  wechatKeyStatus,
  type KeyAcquireOutcome,
  type KeyAcquirePhase,
  type KeyProviderInstallInfo,
  type KeyProviderState,
  type WechatKeyStatus,
} from "./wechat-keyprovider-api";

/** 状态灯:绿/灰两态(桥探测无忙碌面)。 */
function BridgeDot({ on, label }: { on: boolean; label: string }) {
  return (
    <span
      data-testid={`weixin-dot-${label}`}
      aria-label={`${label} ${on ? "正常" : "异常"}`}
      className={cn(
        "flex size-2.5 shrink-0 rounded-full",
        on ? "bg-ok" : "bg-muted-foreground/40",
      )}
    />
  );
}

/**
 * 密钥取得时间(keys.json mtime)→ 相对词面:「今天 11:22」/跨日「10-13 11:22」
 * (语义与 dashboard/api.ts 的 formatRelativeTime 同源:近事相对化、旧事落
 * 原文;invalid/缺位 = null 如实不显)。
 */
function formatAcquiredAt(iso: string | null): string | null {
  if (!iso) return null;
  const then = new Date(iso);
  if (Number.isNaN(then.getTime())) return null;
  const now = new Date();
  const pad = (value: number) => String(value).padStart(2, "0");
  const hm = `${pad(then.getHours())}:${pad(then.getMinutes())}`;
  const sameDay =
    then.getFullYear() === now.getFullYear() &&
    then.getMonth() === now.getMonth() &&
    then.getDate() === now.getDate();
  if (sameDay) return `今天 ${hm}`;
  return `${pad(then.getMonth() + 1)}-${pad(then.getDate())} ${hm}`;
}

/** 三步面板状态机(§D.2):idle(收起,状态行即入口)→ confirm → running → result。 */
type AcquirePanelState = "idle" | "confirm" | "running" | "result";

export function WeixinAccountCard() {
  const [status, setStatus] = useState<Awaited<ReturnType<typeof platformAccountsGetStatus>> | null>(null);
  const [loadError, setLoadError] = useState<SidecarRequestErrorType | null>(null);
  const [note, setNote] = useState<string | null>(null);

  const refresh = useCallback(async () => {
    setLoadError(null);
    try {
      setStatus(await platformAccountsGetStatus());
    } catch (raw) {
      setLoadError(asSidecarError(raw));
    }
  }, []);

  // 取钥器配置态(B5):get 是三态真源;保存/清除成功后重拉刷新。
  const [provider, setProvider] = useState<KeyProviderState | null>(null);
  const [providerError, setProviderError] = useState<SidecarRequestErrorType | null>(null);
  const [providerDraft, setProviderDraft] = useState("");
  const [providerBusy, setProviderBusy] = useState(false);
  const [providerNote, setProviderNote] = useState<string | null>(null);

  const refreshProvider = useCallback(async () => {
    setProviderError(null);
    try {
      setProvider(await wechatKeyProviderGet());
    } catch (raw) {
      setProviderError(asSidecarError(raw));
    }
  }, []);

  // 密钥三态(10-13-wechat-monitor-ui A2):wechat_key_status 是真源
  // (桥 key-status 自带抽样重验;probe 只看文件在场,钥匙失配时会说谎)。
  const [keyStatus, setKeyStatus] = useState<WechatKeyStatus | null>(null);
  const [keyStatusError, setKeyStatusError] = useState<SidecarRequestErrorType | null>(null);

  const refreshKeyStatus = useCallback(async () => {
    setKeyStatusError(null);
    try {
      setKeyStatus(await wechatKeyStatus());
    } catch (raw) {
      setKeyStatusError(asSidecarError(raw));
    }
  }, []);

  // 部署件一键安装(E2;D3 装机后首用引导):源在场=束暂存目录入口件在
  // 场(壳侧 inspect 纯读);安装=cp+700 后自动经桥管理命令 set 保存路径,
  // 「一键」即配置齐。源不在 = 引导文案(自带可执行件走下方路径输入)。
  const [installInfo, setInstallInfo] = useState<KeyProviderInstallInfo | null>(null);
  const [installError, setInstallError] = useState<SidecarRequestErrorType | null>(null);
  const [installBusy, setInstallBusy] = useState(false);
  const [installNote, setInstallNote] = useState<string | null>(null);

  const refreshInstall = useCallback(async () => {
    setInstallError(null);
    try {
      setInstallInfo(await wechatKeyProviderInspect());
    } catch (raw) {
      setInstallError(asSidecarError(raw));
    }
  }, []);

  const installProvider = useCallback(async () => {
    if (installBusy) return;
    setInstallBusy(true);
    setInstallError(null);
    setInstallNote(null);
    try {
      const outcome = await wechatKeyProviderInstall();
      await wechatKeyProviderSet(outcome.installed_path);
      setInstallNote(`取钥器已安装并配置:${outcome.installed_path}`);
      setProviderDraft("");
      await Promise.all([refreshProvider(), refreshKeyStatus(), refreshInstall()]);
    } catch (raw) {
      setInstallError(asSidecarError(raw));
    } finally {
      setInstallBusy(false);
    }
  }, [installBusy, refreshInstall, refreshKeyStatus, refreshProvider]);

  // 获取密钥三步面板(A3;§D.2 状态机 idle→confirm→running→result)。
  const [panel, setPanel] = useState<AcquirePanelState>("idle");
  /** ready 态入口(「重新获取」):force 直走取钥器 + confirm 追加覆盖语义行
   *  (grill 决议②:缓存短路会让失效/重取场景永远空转,必须 --force 才真取)。 */
  const [acquireRegain, setAcquireRegain] = useState(false);
  const [acquirePhase, setAcquirePhase] = useState<KeyAcquirePhase | null>(null);
  const [acquireDetail, setAcquireDetail] = useState<string | null>(null);
  const [cancelling, setCancelling] = useState(false);
  const [cancelError, setCancelError] = useState<string | null>(null);
  const [resultOk, setResultOk] = useState<boolean | null>(null);
  const [resultDbCount, setResultDbCount] = useState<number | null>(null);
  const [resultError, setResultError] = useState<string | null>(null);
  /** §B.3:seq 单调递增,丢弃乱序旧包;settled = 终态只收敛一次。 */
  const lastSeqRef = useRef(0);
  const settledRef = useRef(false);

  /** 终态收敛(回包与终态事件谁先到都只生效一次):cancelled 回 idle(放弃流),
   *  ok 进结果页成功形并重拉三态,failed 进失败形带人话。 */
  const finishAcquire = useCallback(
    (outcome: KeyAcquireOutcome) => {
      if (settledRef.current) return;
      settledRef.current = true;
      setCancelling(false);
      if (outcome.result === "cancelled") {
        setPanel("idle");
        return;
      }
      if (outcome.result === "ok") {
        setResultOk(true);
        setResultDbCount(typeof outcome.db_count === "number" ? outcome.db_count : null);
        setResultError(null);
        setPanel("result");
        void refreshKeyStatus();
        return;
      }
      setResultOk(false);
      setResultError(outcome.error ?? "获取密钥失败,可重试。");
      setResultDbCount(null);
      setPanel("result");
    },
    [refreshKeyStatus],
  );

  // 事件订阅(§B.3):进度只驱动步进条与 detail 行;终态兜底收敛(正常路由 =
  // startAcquire 回包,其携 db_count/error;事件先到也能收口,防回包挂死)。
  useEffect(() => {
    let unlisten: (() => void) | null = null;
    let disposed = false;
    subscribeKeyAcquire((event) => {
      if (event.seq <= lastSeqRef.current) return;
      lastSeqRef.current = event.seq;
      setAcquirePhase(event.phase);
      setAcquireDetail(event.detail);
      if (event.phase === "done") finishAcquire({ result: "ok" });
      else if (event.phase === "failed") finishAcquire({ result: "failed", error: event.detail });
      else if (event.phase === "cancelled") finishAcquire({ result: "cancelled" });
    })
      .then((fn) => {
        if (disposed) fn();
        else unlisten = fn;
      })
      .catch(() => {
        /* 订阅失败不炸卡面:终态真源仍是 acquire 回包 */
      });
    return () => {
      disposed = true;
      unlisten?.();
    };
  }, [finishAcquire]);

  useEffect(() => {
    void refresh();
    void refreshProvider();
    void refreshKeyStatus();
    void refreshInstall();
  }, [refresh, refreshProvider, refreshKeyStatus, refreshInstall]);

  const providerView = provider ? keyProviderView(provider) : null;

  /** 状态行按钮 → confirm(未配取钥器/获取进行中不开门)。 */
  const openAcquireConfirm = useCallback(() => {
    if (providerView !== "configured" || panel === "running") return;
    setAcquireRegain(keyStatus?.state === "ready");
    setPanel("confirm");
  }, [keyStatus, panel, providerView]);

  /** confirm「开始」→ running(force = 重新获取场景跳过桥侧缓存短路)。 */
  const startAcquire = useCallback(async () => {
    setAcquirePhase(null);
    setAcquireDetail(null);
    setCancelError(null);
    setCancelling(false);
    setResultOk(null);
    setResultDbCount(null);
    setResultError(null);
    settledRef.current = false;
    // lastSeqRef 跨 run 保留最大值不清零:壳侧 seq 是进程级单调续增
    // (不因新 run 重置),清零会使上一轮迟到的事件(seq>0)全过水位检查,
    // 把刚开始的新一轮 prematurely 收敛成上一轮的终态(错结果页/提前回
    // idle)。新一轮真事件 seq 必然 > 旧轮已见最大值,水位天然成立。
    setPanel("running");
    try {
      finishAcquire(await startKeyAcquire(acquireRegain));
    } catch (raw) {
      finishAcquire({ result: "failed", error: asSidecarError(raw).message });
    }
  }, [acquireRegain, finishAcquire]);

  /** running「取消」:调取消命令后「正在取消…」直到 cancelled 终态。 */
  const cancelRunningAcquire = useCallback(async () => {
    if (panel !== "running" || cancelling) return;
    setCancelling(true);
    try {
      await cancelKeyAcquire();
    } catch (raw) {
      setCancelling(false);
      setCancelError(asSidecarError(raw).message);
    }
  }, [panel, cancelling]);

  /** 失败形「重试」回 confirm(覆盖语义沿用本次流入口的判定)。 */
  const retryAcquire = useCallback(() => {
    setResultOk(null);
    setResultDbCount(null);
    setResultError(null);
    setAcquirePhase(null);
    setAcquireDetail(null);
    setPanel("confirm");
  }, []);

  const closeAcquire = useCallback(() => setPanel("idle"), []);

  /** 步进条单步视图:当前高亮、已完成打勾、未到置灰。 */
  const stepView = (index: number): "done" | "current" | "pending" => {
    if (acquirePhase === "done") return "done";
    // 终态三值(done/failed/cancelled)不在步进条内 → -1 = 首步待位
    const current = acquirePhase
      ? (KEY_ACQUIRE_STEP_PHASES as readonly KeyAcquirePhase[]).indexOf(acquirePhase)
      : -1;
    if (current === -1) return index === 0 ? "current" : "pending";
    if (index < current) return "done";
    if (index === current) return "current";
    return "pending";
  };

  /** 结果页成功形的库数:回包 db_count 优先,缺省回落重拉后的三态真源。 */
  const resultCount = resultDbCount ?? (keyStatus?.state === "ready" ? keyStatus.db_count : null);
  // 草稿镜像已存值(空草稿 = 回显现值;改过才算 dirty,保存钮才亮)
  const storedPath = provider?.configured ? (provider.path ?? "") : "";
  const draftValue = providerDraft !== "" ? providerDraft : storedPath;
  const draftDirty = providerDraft.trim() !== "" && providerDraft !== storedPath;

  const saveProvider = useCallback(async () => {
    const value = draftValue.trim();
    if (!value || providerBusy) return;
    setProviderBusy(true);
    setProviderError(null);
    setProviderNote(null);
    try {
      await wechatKeyProviderSet(value);
      setProviderNote(`取钥器路径已保存:${value}`);
      setProviderDraft("");
      await refreshProvider();
    } catch (raw) {
      setProviderError(asSidecarError(raw));
    } finally {
      setProviderBusy(false);
    }
  }, [draftValue, providerBusy, refreshProvider]);

  const clearProvider = useCallback(async () => {
    if (providerBusy) return;
    setProviderBusy(true);
    setProviderError(null);
    setProviderNote(null);
    try {
      await wechatKeyProviderClear();
      setProviderNote("已清除取钥器配置(读本地消息时会明确报错,不静默降级)。");
      setProviderDraft("");
      await refreshProvider();
    } catch (raw) {
      setProviderError(asSidecarError(raw));
    } finally {
      setProviderBusy(false);
    }
  }, [providerBusy, refreshProvider]);

  const weixin = status?.weixin ?? null;

  return (
    <Card data-testid="weixin-account-card">
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          <User className="size-4 text-muted-foreground" />
          微信账号
        </CardTitle>
        <CardDescription>
          登录态由本机 Hermes-Agent 持有:MYIA 不读不写 Hermes 私有目录,扫码登录在其终端向导内完成
        </CardDescription>
      </CardHeader>
      <CardContent className="flex flex-col gap-3">
        {loadError ? <ErrorBox error={loadError} onRetry={() => void refresh()} /> : null}
        {note ? (
          <p role="status" data-testid="weixin-note" className="text-xs text-ok">
            {note}
          </p>
        ) : null}
        {status === null && !loadError ? (
          <span data-testid="weixin-loading" className="py-2 text-xs text-muted-foreground">
            状态装载中…
          </span>
        ) : null}

        <div className="flex flex-wrap items-center gap-2">
          <span className="text-sm font-medium text-foreground">桥接状态</span>
          <Badge variant={weixin?.available ? "ok" : "outline"}>
            {weixin?.available ? "可用" : "不可用"}
          </Badge>
        </div>
        <ul className="flex flex-col gap-1 text-2xs text-muted-foreground" aria-label="微信桥接状态">
          <li className="flex items-center gap-1.5">
            <BridgeDot on={weixin?.bin_found === true} label="bin" />
            Hermes CLI {weixin?.bin_found ? "在场" : "未找到"}
            {weixin?.bin_path ? <code className="truncate font-mono">({weixin.bin_path})</code> : null}
          </li>
          <li className="flex items-center gap-1.5">
            <BridgeDot on={weixin?.weixin_configured === true} label="configured" />
            微信账号{weixin?.weixin_configured ? "已配置(扫码登录过)" : "缺失"}
          </li>
          <li className="flex items-center gap-1.5">
            <BridgeDot on={weixin?.gateway_alive === true} label="gateway" />
            Hermes gateway {weixin?.gateway_alive ? "在跑" : "未运行"}
          </li>
        </ul>
        <p className="text-2xs leading-4 text-muted-foreground">
          登录/切换账号在终端执行:
          <code className="mx-1 rounded-sm border border-border/60 bg-muted px-1 font-mono">
            hermes gateway setup
          </code>
          <button
            type="button"
            aria-label="复制微信登录指引命令"
            title="复制命令"
            className="inline-flex rounded-md p-0.5 text-muted-foreground hover:bg-accent hover:text-foreground"
            onClick={() => {
              try {
                void navigator.clipboard?.writeText("hermes gateway setup")?.catch(() => {});
                setNote("已复制 hermes gateway setup(扫码登录在 Hermes 终端向导内完成)。");
              } catch {
                /* 剪贴板不可用静默(轻动作) */
              }
            }}
          >
            <Copy className="size-3" />
          </button>
          (扫码登录在 Hermes 交互式向导内完成)。
        </p>
        <p className="text-2xs leading-4 text-muted-foreground" data-testid="weixin-disclosure">
          诚实披露:微信登录态由本机 Hermes-Agent 持有(单活:同一时刻生效账号一个);
          MYIA 不读不写 Hermes 私有目录,账号列表/卡内登录/删除待后续版本开放。
        </p>

        {/* 密钥状态行(10-13-wechat-monitor-ui A2):插在取钥器配置行上方
            (因果序 = 状态→行动→工具配置)。三态徽标 + 取得时间(mtime 相对
            词面)+ 按钮态联动:missing/stale=「获取密钥」;ready=「重新获取」;
            未配取钥器置灰引导。verdict_note = 三态判据人话小字。 */}
        <div
          className="mt-1 flex flex-col gap-2 border-t border-border/60 pt-3"
          data-testid="weixin-keystatus"
        >
          <div className="flex flex-wrap items-center gap-2">
            <span className="text-sm font-medium text-foreground">数据库密钥</span>
            {keyStatus === null && !keyStatusError ? (
              <span className="text-2xs text-muted-foreground">状态装载中…</span>
            ) : null}
            {keyStatus ? (
              <Badge
                variant={
                  keyStatus.state === "ready" ? "ok" : keyStatus.state === "stale" ? "warning" : "outline"
                }
                data-testid="weixin-keystatus-badge"
              >
                {keyStatus.state === "ready"
                  ? `已就绪 ${keyStatus.db_count} 库`
                  : keyStatus.state === "stale"
                    ? "已失效"
                    : "未获取"}
              </Badge>
            ) : null}
            {keyStatus && formatAcquiredAt(keyStatus.acquired_at) ? (
              <span data-testid="weixin-keystatus-time" className="text-2xs text-muted-foreground">
                {`· ${formatAcquiredAt(keyStatus.acquired_at)}`}
              </span>
            ) : null}
            <Button
              size="sm"
              className="h-6 px-2 text-2xs"
              data-testid="weixin-keystatus-refresh"
              disabled={providerView !== "configured" || panel === "running"}
              title={
                providerView !== "configured"
                  ? "先配置取钥器"
                  : keyStatus?.state === "ready"
                    ? "重新走一遍获取流程(当前密钥在新密钥验证通过后覆盖)"
                    : "开始获取密钥"
              }
              onClick={openAcquireConfirm}
            >
              {keyStatus?.state === "ready" ? "重新获取" : "获取密钥"}
            </Button>
          </div>
          {providerView !== "configured" ? (
            <p className="text-2xs leading-4 text-muted-foreground">
              先配置取钥器:在下方「取钥器」一栏保存可执行文件路径后,才能在这里获取密钥。
            </p>
          ) : null}
          {keyStatusError ? <ErrorBox error={keyStatusError} onRetry={() => void refreshKeyStatus()} /> : null}
          {keyStatus?.verdict_note ? (
            <p className="text-2xs leading-4 text-muted-foreground">{keyStatus.verdict_note}</p>
          ) : null}
        </div>

        {/* 获取密钥三步面板(A3;§D.2 卡内状态机,非独立屏;testid 全表 =
            weixin-keyacquire-{confirm|start|running|cancel|result|retry}) */}
        {panel === "confirm" ? (
          <div
            data-testid="weixin-keyacquire-confirm"
            className="flex flex-col gap-2 rounded-sm border border-border/60 p-3"
          >
            <p className="text-xs leading-5 text-foreground">
              接下来会弹出系统密码框;请在微信里退出登录并重新扫码一次。
            </p>
            <p className="text-2xs leading-4 text-muted-foreground">全程只读,微信数据不会被修改。</p>
            {acquireRegain ? (
              <p className="text-2xs leading-4 text-warning">当前密钥将在新密钥验证通过后覆盖。</p>
            ) : null}
            <div className="flex items-center gap-1.5">
              <Button size="sm" data-testid="weixin-keyacquire-start" onClick={() => void startAcquire()}>
                开始
              </Button>
              <Button size="sm" variant="ghost" data-testid="weixin-keyacquire-cancel" onClick={closeAcquire}>
                取消
              </Button>
            </div>
          </div>
        ) : null}
        {panel === "running" ? (
          <div
            data-testid="weixin-keyacquire-running"
            className="flex flex-col gap-2 rounded-sm border border-border/60 p-3"
          >
            <ol className="flex flex-col gap-1" aria-label="获取密钥进度">
              {KEY_ACQUIRE_STEP_PHASES.map((stepPhase, index) => {
                const view = stepView(index);
                return (
                  <li
                    key={stepPhase}
                    aria-current={view === "current" ? "step" : undefined}
                    className={cn(
                      "flex items-center gap-1.5 text-2xs",
                      view === "done" && "text-ok",
                      view === "current" && "text-foreground",
                      view === "pending" && "text-muted-foreground/60",
                    )}
                  >
                    {view === "done" ? (
                      <Check className="size-3 shrink-0" aria-hidden="true" />
                    ) : (
                      <span
                        aria-hidden="true"
                        className={cn(
                          "size-1.5 shrink-0 rounded-full",
                          view === "current" ? "bg-primary" : "bg-muted-foreground/40",
                        )}
                      />
                    )}
                    {KEY_ACQUIRE_PHASE_LABELS[stepPhase]}
                  </li>
                );
              })}
            </ol>
            {acquireDetail ? (
              <p className="font-mono text-2xs leading-4 text-muted-foreground">{acquireDetail}</p>
            ) : null}
            {cancelError ? (
              <p role="alert" className="text-2xs leading-4 text-warning">
                {cancelError}
              </p>
            ) : null}
            <div>
              <Button
                size="sm"
                variant="ghost"
                data-testid="weixin-keyacquire-cancel"
                disabled={cancelling}
                onClick={() => void cancelRunningAcquire()}
              >
                {cancelling ? "正在取消…" : "取消"}
              </Button>
            </div>
          </div>
        ) : null}
        {panel === "result" ? (
          <div
            data-testid="weixin-keyacquire-result"
            className="flex flex-col gap-2 rounded-sm border border-border/60 p-3"
          >
            {resultOk ? (
              <p className="text-xs leading-5 text-ok">
                {`密钥就绪,${resultCount === null ? "" : `${resultCount} 个`}数据库已可解密`}
              </p>
            ) : (
              <p role="alert" className="text-xs leading-5 text-warning">
                {resultError ?? "获取密钥失败,可重试。"}
              </p>
            )}
            <div className="flex items-center gap-1.5">
              {resultOk ? (
                <Button size="sm" onClick={closeAcquire}>
                  完成
                </Button>
              ) : (
                <Button size="sm" data-testid="weixin-keyacquire-retry" onClick={retryAcquire}>
                  重试
                </Button>
              )}
            </div>
          </div>
        ) : null}

        {/* 取钥器配置行(10-13-wechat-keyprovider B5):微信本机消息库的解密
            钥匙外置获取件。三态徽标 + 状态文案 + 路径输入(保存/清除经壳侧
            Tauri 命令 spawn 桥管理子命令,前端不碰桥配置文件)。 */}
        <div
          className="mt-1 flex flex-col gap-2 border-t border-border/60 pt-3"
          data-testid="weixin-keyprovider"
        >
          <div className="flex flex-wrap items-center gap-2">
            <span className="text-sm font-medium text-foreground">取钥器</span>
            {providerView === null && !providerError ? (
              <span data-testid="weixin-keyprovider-loading" className="text-2xs text-muted-foreground">
                配置装载中…
              </span>
            ) : (
              <Badge
                variant={providerView === "configured" ? "ok" : providerView === "missing" ? "warning" : "outline"}
                data-testid="weixin-keyprovider-badge"
              >
                {providerView === "configured" ? "已配置" : providerView === "missing" ? "文件缺失" : "未配置"}
              </Badge>
            )}
          </div>

          {providerView === "unset" ? (
            <p
              data-testid="weixin-keyprovider-guidance"
              className="text-2xs leading-4 text-muted-foreground"
            >
              未配置取钥器:读取微信本地消息库时不会自动获取解密钥匙(会明确报错,不静默降级)。
              自制或取得一个密钥获取工具(可执行文件)后,把它的路径填到下面保存;
              协议写法与示例见仓库
              <code className="mx-1 rounded-sm border border-border/60 bg-muted px-1 font-mono">
                docs/wechat-keyprovider.md
              </code>
              。
            </p>
          ) : null}

          {/* 部署件一键安装(E2;D3 装机后首用引导):源在场=安装钮(cp+700+
              自动保存路径,「一键」即配置齐);源不在=引导文案;安装后按钮
              态变「重新安装」(束源升级形态)。note/error 置于未配置门之外,
              安装成功翻转配置态后回执仍在场。 */}
          {providerView === "unset" ? (
            <div data-testid="weixin-keyprovider-install" className="flex flex-col gap-1.5">
              {installInfo?.available ? (
                <div>
                  <Button
                    size="sm"
                    className="h-6 px-2 text-2xs"
                    data-testid="weixin-keyprovider-install-button"
                    disabled={installBusy || panel === "running"}
                    title={
                      installInfo.installed
                        ? "把束源四件重新拷贝到数据根私有区并覆盖配置"
                        : "把取钥器部署件安装到数据根私有区,并自动保存为取钥器路径"
                    }
                    onClick={() => void installProvider()}
                  >
                    {installBusy ? "正在安装…" : installInfo.installed ? "重新安装取钥器" : "一键安装取钥器"}
                  </Button>
                </div>
              ) : null}
              {installInfo === null && !installError ? (
                <span data-testid="weixin-keyprovider-install-loading" className="text-2xs text-muted-foreground">
                  安装态装载中…
                </span>
              ) : null}
              {installInfo && !installInfo.available && installInfo.source_unsafe_reason ? (
                <p
                  data-testid="weixin-keyprovider-install-unsafe"
                  role="alert"
                  className="text-2xs leading-4 text-warning"
                >
                  检测到部署件但束源目录属主校验未通过,已拒绝一键安装(多用户
                  机器防他人投放):
                  <span className="ml-1 font-mono">{installInfo.source_unsafe_reason}</span>
                  ;请删除该目录后由本人重新放置部署件束。
                </p>
              ) : null}
              {installInfo && !installInfo.available ? (
                <p
                  data-testid="weixin-keyprovider-install-guidance"
                  className="text-2xs leading-4 text-muted-foreground"
                >
                  未检测到可安装的取钥器部署件:请先把部署件束(四个文件,入口为
                  <code className="mx-1 rounded-sm border border-border/60 bg-muted px-1 font-mono">
                    keyprovider-lldb.sh
                  </code>
                  )放入本机
                  <code className="mx-1 rounded-sm border border-border/60 bg-muted px-1 font-mono">/tmp/wxkey-deploy</code>
                  目录后再回到这里一键安装;或按上方指引自带可执行文件、填入其路径。
                </p>
              ) : null}
            </div>
          ) : null}
          {installError ? <ErrorBox error={installError} onRetry={() => void refreshInstall()} /> : null}
          {installNote ? (
            <p role="status" data-testid="weixin-keyprovider-install-note" className="text-xs text-ok">
              {installNote}
            </p>
          ) : null}
          {providerView === "missing" ? (
            <p role="alert" data-testid="weixin-keyprovider-missing" className="text-2xs leading-4 text-warning">
              配置的取钥器文件不存在或不可执行:
              <code className="mx-1 rounded-sm border border-border/60 bg-muted px-1 font-mono">
                {provider?.path}
              </code>
              ;请核对路径后重新保存。
            </p>
          ) : null}
          {providerView === "configured" ? (
            <div className="flex flex-wrap items-center gap-1.5 text-2xs leading-4 text-muted-foreground">
              <span data-testid="weixin-keyprovider-current">
                当前取钥器:
                <code className="mx-1 rounded-sm border border-border/60 bg-muted px-1 font-mono">
                  {provider?.path}
                </code>
                (需要解密时桥会调用它)
              </span>
              <Button
                size="sm"
                variant="ghost"
                className="h-6 px-2 text-2xs"
                disabled={providerBusy}
                aria-label="清除取钥器配置"
                title="清除后读本地消息会明确报错(未配置取钥器);需要时重新保存路径即可"
                onClick={() => void clearProvider()}
              >
                清除配置
              </Button>
            </div>
          ) : null}

          <FieldInput
            label="取钥器路径"
            aria-label="取钥器路径"
            placeholder="可执行文件绝对路径,如 /opt/tools/wechat-keyprovider"
            value={draftValue}
            hint="保存进微信桥自己的配置文件;读本地消息需要解密钥匙时,桥会按协议调用这个工具"
            labelHint="取钥器 = 帮 MYIA 拿到微信本地消息库解密钥匙的外部小工具(一个可执行文件)。MYIA 自己不带它、也不校验它从哪来;路径要用绝对位置(~ 开头也行)。"
            onChange={(event) => setProviderDraft(event.target.value)}
            action={
              <Button
                size="sm"
                disabled={!draftDirty || providerBusy}
                aria-label="保存取钥器路径"
                title={draftDirty ? "保存路径(桥会先校验文件存在且可执行)" : "先填一个与当前不同的路径"}
                onClick={() => void saveProvider()}
              >
                <Save className="size-3.5" />
                保存路径
              </Button>
            }
          />
          {providerError ? <ErrorBox error={providerError} onRetry={() => void refreshProvider()} /> : null}
          {providerNote ? (
            <p role="status" data-testid="weixin-keyprovider-note" className="text-xs text-ok">
              {providerNote}
            </p>
          ) : null}
        </div>
      </CardContent>
    </Card>
  );
}
