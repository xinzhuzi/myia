/**
 * 「平台账号」总卡(10-11-platform-account-config):配置组「本身账号」面。
 *
 * 裁定语义(主人两轮纠偏钉死):本身账号(用户对自建应用的授权态)≠
 * 推送机器人(App 凭据/bot token)——本卡只做账号,机器人凭据归设置→推送。
 *
 * 卡面两段:
 * - **飞书段**:账号列表行(状态灯三态:绿=refresh 闭环通过/灰=失效或未探/
 *   黄闪=授权进行中 + label/键 + 授权时间 + 「重新检查」+ 删除)+
 *   「+添加账号」(起键名 `feishu-<标识>` → 构造 OAuth 授权 URL 经**系统
 *   浏览器**打开,本地回调端点接 code 换 token,轮询对账镜像 telegram-card
 *   5s×24)。App 凭据复用推送区同一应用(缺 → 结构化错带指引)。
 * - **微信段**:桥接状态灯(零新契约,直读 bridge 三布尔)+ 登录指引
 *   (`hermes gateway setup` 终端扫码;MYIA 红线 = 不读 Hermes 私有内容,
 *   卡内登录/删除等上游契约)。诚实披露:单活模型(env 一组账号)。
 *
 * IPC 契约见 ./platform-accounts-api.ts;token 零外显(全在钥匙链)。
 */
import { Copy, Globe, MessageSquare, Plus, RefreshCw, Trash2, User } from "lucide-react";
import { useCallback, useEffect, useRef, useState } from "react";

import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import type { SidecarRequestError as SidecarRequestErrorType } from "@/lib/api";
import { cn } from "@/lib/utils";

import { asSidecarError } from "./api";
import { ErrorBox } from "./error-box";
import { Input } from "@/components/ui/input";
import {
  feishuAccountAuthorize,
  feishuAccountDelete,
  feishuAccountProbe,
  platformAccountsGetStatus,
  type FeishuAccount,
  type PlatformAccountsStatus,
} from "./platform-accounts-api";

/** 授权轮询参数(回调端点换 token 完成后 status 面回读对账;5s × 24 ≈ 2 分钟)。 */
const AUTHORIZE_POLL_INTERVAL_MS = 5_000;
const AUTHORIZE_POLL_MAX_ATTEMPTS = 24;

/** 账号键规约镜像(``feishu-<标识>``;服务侧同源校验,前端先拦一道省往返)。 */
const FEISHU_KEY_RE = /^feishu-[a-z0-9][a-z0-9_-]{0,62}$/;

/** 状态灯:绿/灰/黄闪(授权中)三态(镜像 telegram-card.StatusDot)。 */
function StatusDot({ on, busy, label }: { on: boolean; busy?: boolean; label: string }) {
  return (
    <span
      data-testid={`platform-dot-${label}`}
      aria-label={`${label} ${on ? "正常" : "异常"}`}
      className={cn(
        "flex size-2.5 shrink-0 rounded-full",
        on ? "bg-ok" : busy ? "bg-warning animate-pulse" : "bg-muted-foreground/40",
      )}
    />
  );
}

export function PlatformAccountsCard() {
  const [status, setStatus] = useState<PlatformAccountsStatus | null>(null);
  const [loadError, setLoadError] = useState<SidecarRequestErrorType | null>(null);
  const [actionError, setActionError] = useState<SidecarRequestErrorType | null>(null);
  const [note, setNote] = useState<string | null>(null);
  /** 新账号键/备注草稿(+添加授权行) */
  const [newAccount, setNewAccount] = useState("");
  const [newAccountLabel, setNewAccountLabel] = useState("");
  const [authorizing, setAuthorizing] = useState(false);
  /** 逐行动作忙位与探针结果提示 */
  const [busyAccount, setBusyAccount] = useState<string | null>(null);
  const [probeNote, setProbeNote] = useState<string | null>(null);
  /** 授权轮询(发起后启动;status 面见新账号即停,上限放弃) */
  const pollRef = useRef(0);

  const refresh = useCallback(async () => {
    setLoadError(null);
    try {
      setStatus(await platformAccountsGetStatus());
    } catch (raw) {
      setLoadError(asSidecarError(raw));
    }
  }, []);

  useEffect(() => {
    void refresh();
  }, [refresh]);

  /** 发起飞书账号授权:系统浏览器开授权页 + 启动轮询对账(见新账号即停)。 */
  const handleAuthorize = useCallback(async () => {
    const key = newAccount.trim();
    if (!FEISHU_KEY_RE.test(key) || authorizing) return;
    setActionError(null);
    setProbeNote(null);
    setAuthorizing(true);
    try {
      const result = await feishuAccountAuthorize(key, newAccountLabel.trim());
      // 系统浏览器打开授权页(plugin-shell open 受控门,http(s) scope 在册);
      // 动态 import:浏览器直开(vitest)不加载 Tauri 壳包,点击才触路。
      const shell = await import("@tauri-apps/plugin-shell");
      await shell.open(result.authorize_url);
      setNote(`授权页已在系统浏览器打开(账号 ${key});完成授权后本卡自动对账。`);
      setNewAccount("");
      setNewAccountLabel("");
      const pollId = pollRef.current + 1;
      pollRef.current = pollId;
      for (let attempt = 0; attempt < AUTHORIZE_POLL_MAX_ATTEMPTS; attempt += 1) {
        await new Promise((resolve) => setTimeout(resolve, AUTHORIZE_POLL_INTERVAL_MS));
        if (pollRef.current !== pollId) return;
        const snapshot = await platformAccountsGetStatus();
        setStatus(snapshot);
        if (snapshot.feishu.accounts.some((entry) => entry.account === key)) {
          setNote(`账号 ${key} 授权完成并已入列。`);
          break;
        }
      }
    } catch (raw) {
      setActionError(asSidecarError(raw));
    } finally {
      setAuthorizing(false);
    }
  }, [authorizing, newAccount, newAccountLabel]);

  /** 重新检查:显式触发刷新闭环探针(成功置绿并续期;失败置灰带原因)。 */
  const handleProbe = useCallback(async (account: FeishuAccount) => {
    setActionError(null);
    setProbeNote(null);
    setBusyAccount(account.account);
    try {
      const result = await feishuAccountProbe(account.account);
      if (result.refresh_ok) {
        setProbeNote(`账号 ${account.account} 授权态有效(token 已续期)。`);
      } else {
        setProbeNote(
          `账号 ${account.account} 授权态失效(${result.reason ?? "unknown"}):请删除后重新添加授权。`,
        );
      }
      await refresh();
    } catch (raw) {
      setActionError(asSidecarError(raw));
    } finally {
      setBusyAccount(null);
    }
  }, [refresh]);

  const handleDelete = useCallback(
    async (account: FeishuAccount) => {
      const label = account.label ?? account.account;
      if (!window.confirm(`确定删除账号「${label}」(${account.account})?\n\n钥匙链中的授权 token 与账号记录将一并清除。`)) {
        return;
      }
      setActionError(null);
      setProbeNote(null);
      setBusyAccount(account.account);
      try {
        await feishuAccountDelete(account.account);
        pollRef.current += 1; // 停掉可能在对账该键的轮询
        await refresh();
      } catch (raw) {
        setActionError(asSidecarError(raw));
      } finally {
        setBusyAccount(null);
      }
    },
    [refresh],
  );

  const feishuAccounts = status?.feishu.accounts ?? [];
  const weixin = status?.weixin ?? null;

  return (
    <Card data-testid="platform-accounts-card">
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          <Globe className="size-4 text-muted-foreground" />
          平台账号
        </CardTitle>
        <CardDescription>
          本身账号(个人授权态)管理:与「推送机器人」凭据是两回事——机器人配置在 设置→推送
        </CardDescription>
      </CardHeader>
      <CardContent className="flex flex-col gap-4">
        {loadError ? <ErrorBox error={loadError} onRetry={() => void refresh()} /> : null}
        {actionError ? <ErrorBox error={actionError} /> : null}
        {note ? (
          <p role="status" data-testid="platform-note" className="text-xs text-ok">
            {note}
          </p>
        ) : null}
        {probeNote ? (
          <p role="status" data-testid="probe-note" className="text-xs text-foreground">
            {probeNote}
          </p>
        ) : null}
        {status === null && !loadError ? (
          <span data-testid="platform-loading" className="py-2 text-xs text-muted-foreground">
            状态装载中…
          </span>
        ) : null}

        {/* 飞书段:账号列表 + 添加授权 */}
        <div className="flex flex-col gap-2 rounded-md border border-border p-4">
          <div className="flex flex-wrap items-center gap-2">
            <MessageSquare className="size-3.5 text-muted-foreground" />
            <span className="text-sm font-medium text-foreground">飞书账号</span>
            <Badge variant={feishuAccounts.length > 0 ? "ok" : "outline"}>
              {feishuAccounts.length} 个已授权
            </Badge>
            {status?.feishu.authorize_in_progress ? (
              <Badge variant="warning">授权进行中</Badge>
            ) : null}
          </div>
          <p className="text-2xs leading-4 text-muted-foreground">
            user_access_token 授权态(复用推送区同一自建应用);前置:应用安全设置登记重定向 URL
            {" "}
            <code className="font-mono">http://127.0.0.1:8731/callback</code>
            ,未登记时授权页会报「redirect_uri 不合法」。
          </p>
          {feishuAccounts.length > 0 ? (
            <ul className="flex flex-col gap-1.5" aria-label="飞书账号清单">
              {feishuAccounts.map((entry) => (
                <li
                  key={entry.account}
                  className="flex items-center gap-2 rounded-md border border-border bg-muted/30 px-2.5 py-2"
                  data-testid={`feishu-account-${entry.account}`}
                >
                  <StatusDot
                    on={entry.refresh_ok === true}
                    busy={busyAccount === entry.account && entry.refresh_ok !== false}
                    label={`feishu-${entry.account}`}
                  />
                  <span className="flex min-w-0 flex-1 flex-col">
                    <span className="truncate text-sm text-foreground">
                      {entry.label ?? entry.account}
                    </span>
                    <span className="truncate font-mono text-2xs text-muted-foreground">
                      {entry.account}
                      {entry.authorized_at ? ` · 授权于 ${entry.authorized_at.slice(0, 16)}` : ""}
                      {entry.refresh_ok === false ? " · 授权态失效" : entry.refresh_ok === null ? " · 未检查" : ""}
                    </span>
                  </span>
                  <Button
                    size="sm"
                    variant="outline"
                    disabled={busyAccount === entry.account}
                    onClick={() => void handleProbe(entry)}
                  >
                    <RefreshCw className={cn("size-3.5", busyAccount === entry.account && "animate-spin")} />
                    重新检查
                  </Button>
                  <Button
                    size="sm"
                    variant="outline"
                    disabled={busyAccount === entry.account}
                    title="删除授权(钥匙链 token 与账号记录一并清除)"
                    onClick={() => void handleDelete(entry)}
                  >
                    <Trash2 className="size-3.5" />
                    删除
                  </Button>
                </li>
              ))}
            </ul>
          ) : (
            <p className="text-2xs text-muted-foreground">还没有已授权账号;下方「+添加账号」发起授权。</p>
          )}

          <div className="flex flex-col gap-1.5 rounded-md border border-border bg-muted/30 p-2">
            <p className="text-xs font-medium text-foreground">添加账号(键名)</p>
            <p className="text-2xs text-muted-foreground">
              起键名点「发起授权」,系统浏览器打开飞书授权页,完成后本卡自动对账入列。
            </p>
            <div className="flex items-center gap-1.5">
              <Input
                value={newAccount}
                aria-label="飞书账号键名"
                placeholder="feishu-<标识>(如 feishu-work)"
                onChange={(event) => setNewAccount(event.target.value)}
                className={cn(
                  "h-8 flex-1",
                  newAccount.trim().length > 0 && !FEISHU_KEY_RE.test(newAccount.trim()) && "border-destructive",
                )}
              />
              <Input
                value={newAccountLabel}
                aria-label="飞书账号备注"
                placeholder="备注名(可选,如 工作号)"
                onChange={(event) => setNewAccountLabel(event.target.value)}
                className="h-8 w-40"
              />
              <Button
                size="sm"
                disabled={!FEISHU_KEY_RE.test(newAccount.trim()) || authorizing}
                onClick={() => void handleAuthorize()}
              >
                <Plus className={cn("size-3.5", authorizing && "animate-pulse")} />
                {authorizing ? "授权中…" : "发起授权"}
              </Button>
            </div>
            {newAccount.trim().length > 0 && !FEISHU_KEY_RE.test(newAccount.trim()) ? (
              <p role="alert" className="text-2xs text-destructive">
                键名不合规:全称律 feishu-{"<标识>"},小写字母/数字/-/_
              </p>
            ) : null}
          </div>
        </div>

        {/* 微信段:桥接状态 + 指引(受限形态,诚实披露) */}
        <div className="flex flex-col gap-2 rounded-md border border-border p-4">
          <div className="flex flex-wrap items-center gap-2">
            <User className="size-3.5 text-muted-foreground" />
            <span className="text-sm font-medium text-foreground">微信(经 Hermes 桥)</span>
            <Badge variant={weixin?.available ? "ok" : "outline"}>
              {weixin?.available ? "桥可用" : "桥不可用"}
            </Badge>
          </div>
          <ul className="flex flex-col gap-1 text-2xs text-muted-foreground" aria-label="微信桥接状态">
            <li className="flex items-center gap-1.5">
              <StatusDot on={weixin?.bin_found === true} label="weixin-bin" />
              Hermes CLI {weixin?.bin_found ? "在场" : "未找到"}
              {weixin?.bin_path ? <code className="truncate font-mono">({weixin.bin_path})</code> : null}
            </li>
            <li className="flex items-center gap-1.5">
              <StatusDot on={weixin?.weixin_configured === true} label="weixin-configured" />
              微信账号档{weixin?.weixin_configured ? "已配置(扫码登录过)" : "缺失"}
            </li>
            <li className="flex items-center gap-1.5">
              <StatusDot on={weixin?.gateway_alive === true} label="weixin-gateway" />
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
                  setProbeNote("已复制 hermes gateway setup(扫码登录在 Hermes 终端向导内完成)。");
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
            MYIA 不读不写 Hermes 私有目录,账号档列表/卡内登录/删除待上游提供契约后开放。
          </p>
        </div>
      </CardContent>
    </Card>
  );
}
