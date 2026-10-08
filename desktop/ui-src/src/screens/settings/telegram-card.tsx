/**
 * 「Telegram 监控」总卡(10-08-tg-web-line W4;PRD 登录 UX 决议;
 * 10-08-browser-module 接线:登录动作改调浏览器模块统一入口)。
 *
 * 卡面三段(PRD「bot/session/web 三态行」)+ 账号列表化(PRD 多账号决议 ③):
 *
 * - **bot 段**:token 状态灯(绿 = keychain 在册;灰 = 未配,四步指引);
 * - **session 段**:telethon 用户线 session(绿 = 已首登;灰 = 未首登,
 *   CLI login 指引);
 * - **web 段**:网页线账号列表(每行:键 + 状态灯 + 重登 + 删除)+
 *   「+添加账号」(起键名 → **经浏览器模块**拉起 MYIA 自管 Chromium 登录
 *   窗;单入口铁律 = 一切浏览器操作必经 browser.open,窗口台账/错误上浮
 *   集中在设置 →「浏览器」分区,卡面登录中/失败态与模块操作台账同源联动)。
 *
 * 诚实披露三条在卡面文案常驻(PRD AC5):DOM 改版跟修哨兵在/ToS 灰色
 * 建议小号(同机同出口多账号可被关联)/api_id 到手切回 Telethon 正统线。
 * IPC 契约见 ./telegram-api.ts;凭据零外显(手机号+验证码全在登录窗内)。
 */
import { Globe, MessageCircle, Plus, RefreshCw, Send, Trash2, User } from "lucide-react";
import { useCallback, useEffect, useState } from "react";

import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { SidecarRequestError, type SidecarRequestError as SidecarRequestErrorType } from "@/lib/api";
import { cn } from "@/lib/utils";

import { asSidecarError } from "./api";
import { ErrorBox } from "./error-box";
import { FieldInput } from "./field-input";
import {
  telegramGetStatus,
  telegramWebDelete,
  telegramWebLogin,
  type TelegramStatus,
  type TelegramWebAccount,
} from "./telegram-api";

/** 登录窗状态轮询参数(登录窗完成/失败后 status 面回读对账;5s × 24 ≈ 2 分钟)。 */
const LOGIN_POLL_INTERVAL_MS = 5_000;
const LOGIN_POLL_MAX_ATTEMPTS = 24;

/** 账号键规约镜像(``telegram-<标识>``;服务侧同源校验,前端先拦一道省往返)。 */
const ACCOUNT_KEY_RE = /^telegram-[a-z0-9][a-z0-9_-]{0,62}$/;

/** 状态灯:绿/灰/黄闪(登录中)三态。 */
function StatusDot({ on, busy, label }: { on: boolean; busy?: boolean; label: string }) {
  return (
    <span
      data-testid={`telegram-dot-${label}`}
      aria-label={`${label} ${on ? "已配置" : "未配置"}`}
      className={cn(
        "flex size-2.5 shrink-0 rounded-full",
        on ? "bg-ok" : busy ? "bg-warning animate-pulse" : "bg-muted-foreground/40",
      )}
    />
  );
}

/** 三段行的段落骨架(图标 + 标题 + 状态徽标 + 说明/指引)。 */
function LineSection({
  icon,
  title,
  ok,
  okLabel,
  missLabel,
  hint,
}: {
  icon: React.ReactNode;
  title: string;
  ok: boolean;
  okLabel: string;
  missLabel: string;
  hint: string;
}) {
  return (
    <div className="flex flex-col gap-1 p-4">
      <div className="flex flex-wrap items-center gap-2">
        {icon}
        <span className="text-sm font-medium text-foreground">{title}</span>
        <Badge variant={ok ? "ok" : "outline"}>{ok ? okLabel : missLabel}</Badge>
      </div>
      <p className="text-2xs leading-4 text-muted-foreground">{hint}</p>
    </div>
  );
}

export function TelegramCard() {
  const [status, setStatus] = useState<TelegramStatus | null>(null);
  const [loadError, setLoadError] = useState<SidecarRequestErrorType | null>(null);
  const [actionError, setActionError] = useState<SidecarRequestErrorType | null>(null);
  const [note, setNote] = useState<string | null>(null);
  /** 新账号键草稿(+添加账号行) */
  const [newAccount, setNewAccount] = useState("");
  const [busyAccount, setBusyAccount] = useState<string | null>(null);
  /** 登录窗轮询(拉起后启动;status 面无 running 即停,上限放弃) */
  const [loginPoll, setLoginPoll] = useState(0);

  const refresh = useCallback(async () => {
    setLoadError(null);
    try {
      setStatus(await telegramGetStatus());
    } catch (raw) {
      setLoadError(asSidecarError(raw));
    }
  }, []);

  useEffect(() => {
    void refresh();
  }, [refresh]);

  /** 登录窗状态对账轮询(有账号 login_in_progress 时跑;完成即停)。 */
  useEffect(() => {
    if (loginPoll <= 0 || loginPoll > LOGIN_POLL_MAX_ATTEMPTS) {
      if (loginPoll > LOGIN_POLL_MAX_ATTEMPTS) setLoginPoll(0);
      return;
    }
    let cancelled = false;
    const timer = setTimeout(() => {
      void telegramGetStatus().then((next) => {
        if (cancelled) return;
        setStatus(next);
        const anyRunning = next.web.accounts.some((row) => row.login_in_progress);
        setLoginPoll(anyRunning ? loginPoll + 1 : 0);
      }).catch(() => {
        if (!cancelled) setLoginPoll(loginPoll + 1);
      });
    }, LOGIN_POLL_INTERVAL_MS);
    return () => {
      cancelled = true;
      clearTimeout(timer);
    };
  }, [loginPoll]);

  /** 拉起登录窗(新账号 = 草稿键;已有账号 = 重登,force 清档)。 */
  const startLogin = useCallback(
    async (account: string, force: boolean) => {
      setBusyAccount(account);
      setActionError(null);
      setNote(null);
      try {
        const outcome = await telegramWebLogin(account, force);
        if (outcome.started) {
          setNote(
            `账号 ${account} 登录窗已拉起(经浏览器模块):请在弹出的浏览器窗口里输入手机号 → 验证码(验证码在你手机 TG 里;如有两步验证再输密码)。登录态会自动落档,本页每 ${LOGIN_POLL_INTERVAL_MS / 1000}s 自动对账(转绿即完成);窗口管理(聚焦/关闭)在设置 →「浏览器」分区。`,
          );
          setLoginPoll(1);
          setStatus(await telegramGetStatus());
        } else {
          setNote(outcome.note ?? `账号 ${account} 登录窗已在进行中(到「浏览器」分区管理窗口)。`);
        }
      } catch (raw) {
        setActionError(asSidecarError(raw));
      } finally {
        setBusyAccount(null);
      }
    },
    [],
  );

  const handleAdd = useCallback(() => {
    const key = newAccount.trim();
    if (!ACCOUNT_KEY_RE.test(key)) {
      setActionError(
        new SidecarRequestError({
          code: "invalid_account",
          path: "account",
          message: `账号键应为全称律 telegram-<标识>(小写字母数字,如 telegram-alt1),当前为 ${JSON.stringify(key)}`,
          data: null,
        }),
      );
      return;
    }
    setNewAccount("");
    void startLogin(key, false);
  }, [newAccount, startLogin]);

  const handleDelete = useCallback(
    async (account: string) => {
      setBusyAccount(account);
      setActionError(null);
      setNote(null);
      try {
        await telegramWebDelete(account);
        setNote(`账号 ${account} 配置档已删除(登录态随档消失;常驻 web 线重启后不再拉起该键)。`);
        setStatus(await telegramGetStatus());
      } catch (raw) {
        setActionError(asSidecarError(raw));
      } finally {
        setBusyAccount(null);
      }
    },
    [],
  );

  const accounts: TelegramWebAccount[] = status?.web.accounts ?? [];

  return (
    <Card data-testid="telegram-card">
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          <Send className="size-4 text-muted-foreground" />
          Telegram 监控
        </CardTitle>
        <CardDescription>
          三条消息线(bot / 用户 session / 网页登录)的状态与动作:网页线零凭据,
          一次登录后无头常驻读群,消息全走同一套过滤与推送
        </CardDescription>
      </CardHeader>
      <CardContent className="flex flex-col gap-4">
        {loadError ? <ErrorBox error={loadError} onRetry={() => void refresh()} /> : null}
        {status === null && loadError === null ? (
          <span data-testid="telegram-loading" className="py-2 text-xs text-muted-foreground">
            状态装载中…
          </span>
        ) : null}

        {status !== null ? (
          <>
            <div className="flex flex-col divide-y divide-border/60 rounded-lg border border-border/60">
              <LineSection
                icon={<Send className="size-4 text-muted-foreground" />}
                title="bot 线(Bot API)"
                ok={status.bot.configured}
                okLabel="token 已录"
                missLabel="未配置"
                hint={
                  status.bot.configured
                    ? "钥匙串 myia/telegram/bot-token 在册;四步(BuildFather 建 bot → 关隐私模式 → 写 token → 拉进群)已完成。"
                    : "四步:BotFather 建 bot → /setprivacy 关闭隐私模式 → myssia secret set myia/telegram/bot-token → 拉进目标群(配置在推送凭据区与品类 YAML)。"
                }
              />
              <LineSection
                icon={<User className="size-4 text-muted-foreground" />}
                title="用户 session(Telethon)"
                ok={status.session.exists}
                okLabel="session 在"
                missLabel="未首登"
                hint={
                  status.session.exists
                    ? "数据根 telegram/telethon.session 在场;需要 api-id/api-hash(钥匙串)+ 组件已装,serve 常驻自动拉起。"
                    : "一次性首登:钥匙串写 api-id/api-hash(my.telegram.org 取值)后终端 myssia telegram login(手机号+验证码,建议挂小号);api_id 到手优先本线(正统)。"
                }
              />
              <div className="flex flex-col gap-2 p-4">
                <div className="flex flex-wrap items-center gap-2">
                  <Globe className="size-4 text-muted-foreground" />
                  <span className="text-sm font-medium text-foreground">网页登录(tg_web)</span>
                  <Badge variant={accounts.some((row) => row.logged_in) ? "ok" : "outline"}>
                    {accounts.filter((row) => row.logged_in).length}/{accounts.length || 0} 已登录
                  </Badge>
                </div>
                <p className="text-2xs leading-4 text-muted-foreground">
                  零凭据通道:MYIA 自管无头 Chromium 登 web.telegram.org 一次,之后常驻读群消息 DOM
                  → 与 bot 线同一套粗筛/精筛/推送。披露:DOM 改版有跟修哨兵(失配即结构化告警不装死);
                  ToS 灰色同 userbot,建议各键专用小号(同机同出口多账号可被关联,只读监控风险低,数量克制,缺省帽
                  3);api_id 到手建议切回 Telethon 正统线,本线退役或备份;登录态 = 配置档文件(0600,非加密)。
                </p>
                <div data-testid="telegram-web-accounts" className="flex flex-col gap-2">
                  {accounts.length === 0 ? (
                    <p data-testid="telegram-web-empty" className="text-2xs text-muted-foreground">
                      尚无账号:点下方「添加账号」起键名(telegram-&lt;标识&gt;)拉起登录窗。
                    </p>
                  ) : null}
                  {accounts.map((row) => (
                    <div
                      key={row.account}
                      data-testid={`telegram-web-account-${row.account}`}
                      className="flex flex-wrap items-center justify-between gap-2 rounded-md border border-border/60 bg-muted/20 px-3 py-2"
                    >
                      <div className="flex min-w-0 flex-1 flex-col gap-0.5">
                        <span className="flex items-center gap-2 font-mono text-xs text-foreground">
                          <StatusDot
                            on={row.logged_in}
                            busy={row.login_in_progress}
                            label={row.account}
                          />
                          {row.account}
                        </span>
                        {row.login_in_progress ? (
                          <span
                            role="status"
                            data-testid={`telegram-web-${row.account}-busy`}
                            className="flex items-center gap-1 text-2xs text-warning"
                          >
                            <RefreshCw className="size-3 animate-spin" />
                            登录窗进行中(页面内输手机号+验证码)…
                          </span>
                        ) : null}
                        {row.login_note ? (
                          <span
                            role={row.login_note.includes("失败") || row.login_note.includes("timeout") ? "alert" : "status"}
                            className="break-all text-2xs text-muted-foreground"
                          >
                            {row.login_note}
                          </span>
                        ) : row.logged_in_at ? (
                          <span className="text-2xs text-muted-foreground">
                            登录于 {row.logged_in_at}
                          </span>
                        ) : null}
                      </div>
                      <div className="flex shrink-0 items-center gap-2">
                        <Button
                          variant="outline"
                          size="sm"
                          disabled={busyAccount === row.account || row.login_in_progress}
                          onClick={() => void startLogin(row.account, true)}
                          data-testid={`telegram-web-${row.account}-relogin`}
                          title="清档重登(--force):拉起浏览器登录窗,手机号+验证码在页面内输"
                        >
                          重新登录
                        </Button>
                        <Button
                          variant="outline"
                          size="sm"
                          disabled={busyAccount === row.account || row.login_in_progress}
                          onClick={() => void handleDelete(row.account)}
                          data-testid={`telegram-web-${row.account}-delete`}
                          title="删除该账号配置档(登录态随档消失;源 YAML 引用该键的 tg_web 源会显式空态)"
                        >
                          <Trash2 className="size-3.5" />
                          删除
                        </Button>
                      </div>
                    </div>
                  ))}
                </div>
                <FieldInput
                  label="添加账号(键名)"
                  aria-label="新账号键名"
                  placeholder="telegram-alt1"
                  value={newAccount}
                  onChange={(event) => setNewAccount(event.target.value)}
                  labelHint="全称律 telegram-<标识>(小写字母数字起头);每键独立浏览器配置档(0600),多账号互不相通。"
                  hint="起键名后点「添加账号」拉起浏览器登录窗"
                />
                <div className="flex flex-wrap items-center justify-between gap-2">
                  <MessageCircle className="size-3.5 text-muted-foreground" />
                  <Button
                    size="sm"
                    onClick={handleAdd}
                    disabled={busyAccount !== null}
                    data-testid="telegram-web-add"
                    title="拉起 headed 浏览器登录窗(手机号+验证码在页面内输;验证码在你手机 TG 里)"
                  >
                    <Plus className="size-3.5" />
                    添加账号
                  </Button>
                </div>
              </div>
            </div>

            <div className="flex flex-col gap-2 border-t border-border/60 pt-3">
              {actionError ? <ErrorBox error={actionError} /> : null}
              {note ? (
                <p role="status" data-testid="telegram-action-note" className="text-xs leading-5 text-ok">
                  {note}
                </p>
              ) : null}
            </div>
          </>
        ) : null}
      </CardContent>
    </Card>
  );
}
