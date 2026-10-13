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
 */
import { Copy, Save, User } from "lucide-react";
import { useCallback, useEffect, useState } from "react";

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
  keyProviderView,
  wechatKeyProviderClear,
  wechatKeyProviderGet,
  wechatKeyProviderSet,
  type KeyProviderState,
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

  useEffect(() => {
    void refresh();
    void refreshProvider();
  }, [refresh, refreshProvider]);

  const providerView = provider ? keyProviderView(provider) : null;
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
