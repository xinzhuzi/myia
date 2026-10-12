/**
 * 「微信账号」卡(10-11-platform-account-config;2026-10-11 主人令渠道本名制:
 * 自「平台账号」总卡拆出,微信就是微信)。
 *
 * 受限形态(裁定 D3):微信登录态由本机 Hermes-Agent 持有,MYIA 红线 =
 * 不读不写 Hermes 私有目录——本卡零新契约,只做桥接状态灯(三布尔,直读
 * probe_bridge)+ 登录指引(`hermes gateway setup` 终端扫码)+ 单活模型
 * 诚实披露。账号档列表/卡内登录/删除待上游契约后开放。
 */
import { Copy, User } from "lucide-react";
import { useCallback, useEffect, useState } from "react";

import { Badge } from "@/components/ui/badge";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import type { SidecarRequestError as SidecarRequestErrorType } from "@/lib/api";
import { cn } from "@/lib/utils";

import { asSidecarError } from "./api";
import { ErrorBox } from "./error-box";
import { platformAccountsGetStatus } from "./platform-accounts-api";

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

  useEffect(() => {
    void refresh();
  }, [refresh]);

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
      </CardContent>
    </Card>
  );
}
