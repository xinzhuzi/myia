/**
 * 「Telegram 配置」总卡(10-08-tg-web-line W4;PRD 登录 UX 决议;
 * 10-08-browser-module 接线:登录动作改调浏览器模块统一入口;
 * 2026-10-11 主人令更名「Telegram 监控」→「Telegram 配置」,与侧栏
 * 「配置」组(YAML配置/Telegram)语义对齐;feed 分类显示名「Telegram 监控」
 * 是另一语义,不动)。
 *
 * 卡面三段(PRD「bot/session/web 三态行」)+ 账号列表化(PRD 多账号决议 ③):
 *
 * - **bot 段**:token 状态灯(绿 = keychain 在册;灰 = 未配,四步指引);
 * - **session 段**:telethon 用户线 session(绿 = 已首登;灰 = 未首登,
 *   CLI login 指引);
 * - **web 段**:网页线账号列表(每行:键 + 状态灯 + 检测 + 重登 + 删除)+
 *   「+添加账号」(起键名 → **经浏览器模块**拉起 MYIA 自管 Chromium 登录
 *   窗;单入口铁律 = 一切浏览器操作必经 browser.open,窗口台账/错误上浮
 *   集中在设置 →「浏览器」分区,卡面登录中/失败态与模块操作台账同源联动)。
 *   「检测」= 账号体检(10-11-tg-manage-absorb):常态读常驻哨兵真源秒回,
 *   无常驻占用走无头探针后台线程;行小字「上次体检 · 活/死」由 status
 *   轮询对账刷新(alive 与 logged_in 双键并存,死不自动清标记 → 引导重登)。
 *
 * 诚实披露三条在卡面文案常驻(PRD AC5):DOM 改版跟修哨兵在/ToS 灰色
 * 建议小号(同机同出口多账号可被关联)/api_id 到手切回 Telethon 正统线。
 * IPC 契约见 ./telegram-api.ts;凭据零外显(手机号+验证码全在登录窗内)。
 */
import { Activity, Globe, MessageCircle, Plus, RefreshCw, Send, Trash2, User } from "lucide-react";
import { useCallback, useEffect, useState } from "react";

import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { SidecarRequestError, type SidecarRequestError as SidecarRequestErrorType } from "@/lib/api";
import { cn } from "@/lib/utils";
import { formatRelativeTime } from "@/screens/feed/api";

import { asSidecarError } from "./api";
import { ErrorBox } from "./error-box";
import { FieldInput } from "./field-input";
import {
  telegramGetStatus,
  telegramWebCheck,
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
  /** 新账号备注名草稿(+添加账号行;人读,如「小号·尾号93105」)。 */
  const [newAccountLabel, setNewAccountLabel] = useState("");
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

  /** 登录窗/体检状态对账轮询(有账号 login_in_progress 或 check_in_progress
   * 时跑;完成即停 —— 10-11-tg-manage-absorb 泛化复用,非第二套轮询)。 */
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
        const anyRunning = next.web.accounts.some(
          (row) => row.login_in_progress || row.check_in_progress,
        );
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

  /** 拉起登录窗(新账号 = 草稿键+可选备注名;已有账号 = 重登,force 清档
   * —— 备注 label 由服务侧从旧标记随行,跨重登存续)。 */
  const startLogin = useCallback(
    async (account: string, force: boolean, label?: string) => {
      setBusyAccount(account);
      setActionError(null);
      setNote(null);
      try {
        const outcome = await telegramWebLogin(
          account,
          force,
          label !== undefined ? label : undefined,
        );
        if (outcome.started) {
          setNote(
            `账号 ${account} 登录窗口已打开(经浏览器模块):请在弹出的浏览器窗口里输入手机号 → 验证码(验证码在你手机 TG 里;如有两步验证再输密码;会话失效时登录页可直接用手机 Telegram 扫码登录,免等验证码)。登录状态会自动保存,本页每 ${LOGIN_POLL_INTERVAL_MS / 1000}s 自动核对一次(状态变绿即完成);窗口管理(聚焦/关闭)在设置 →「浏览器」分区。`,
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
          message: `账号键须为 telegram-<标识> 形式(小写字母数字,如 telegram-alt1),当前为 ${JSON.stringify(key)}`,
          data: null,
        }),
      );
      return;
    }
    const label = newAccountLabel.trim() || undefined;
    setNewAccount("");
    setNewAccountLabel("");
    void startLogin(key, false, label);
  }, [newAccount, newAccountLabel, startLogin]);

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

  /** 发起账号体检(10-11-tg-manage-absorb):常驻监控在跑时服务端读哨兵
   * 真源秒回;无常驻占用走无头探针后台线程(≤45s),行小字(上次体检/
   * 活死)由轮询对账刷新 —— 泛化 loginPoll,非第二套轮询。 */
  const runCheck = useCallback(
    async (account: string) => {
      setBusyAccount(account);
      setActionError(null);
      setNote(null);
      try {
        const outcome = await telegramWebCheck(account);
        if (outcome.started) {
          setNote(
            `账号 ${account} 检查已发起:常驻监控在跑时直接读其最新状态、秒回;否则后台检测至多约 45s 出结果(被占用会提示先停占用),本页每 ${LOGIN_POLL_INTERVAL_MS / 1000}s 自动核对(行小字见「上次检查 · 状态」)。`,
          );
          setLoginPoll(1);
          setStatus(await telegramGetStatus());
        } else {
          setNote(outcome.note ?? `账号 ${account} 体检正在进行中(稍候刷新看结果)。`);
        }
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
          Telegram 配置
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
                    ? "钥匙串 myia/telegram/bot-token 在册;四步(BotFather 建 bot → 关隐私模式 → 写 token → 拉进群)已完成。"
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
                    ? "数据目录 telegram/telethon.session 在场;需要 api-id/api-hash(钥匙串)+ 组件已装,serve 常驻后自动启动。"
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
                  零凭据通道:MYIA 托管的后台 Chromium 登录 web.telegram.org 一次,之后常驻读取群消息
                  → 与 bot 线同一套消息过滤与推送。登录时手机号+验证码在页面内输(验证码在你手机 TG
                  里;会话失效时登录页可直接用手机 Telegram 扫码登录,免等验证码)。说明:网页改版时有
                  自动监测并跟进修复(失配会明确告警,不会无声失效);
                  ToS 灰色同 userbot,建议各键专用小号(同机同出口多账号可被关联,只读监控风险低,数量克制,默认上限
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
                      className="flex flex-wrap items-start justify-between gap-2 rounded-md bg-muted/40 px-3 py-2"
                    >
                      <div className="flex min-w-0 flex-1 flex-col gap-0.5">
                        <span className="flex items-center gap-2 text-xs font-medium text-foreground">
                          <StatusDot
                            on={row.logged_in}
                            busy={row.login_in_progress}
                            label={row.account}
                          />
                          {row.label || row.account}
                        </span>
                        {row.label ? (
                          <span className="font-mono text-2xs text-muted-foreground">
                            {row.account}
                            {row.user_id ? ` · id ${row.user_id}` : ""}
                          </span>
                        ) : row.user_id ? (
                          <span className="text-2xs text-muted-foreground">
                            TG id {row.user_id}
                          </span>
                        ) : null}
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
                        {row.check_in_progress ? (
                          <span
                            role="status"
                            data-testid={`telegram-web-${row.account}-checkbusy`}
                            className="flex items-center gap-1 text-2xs text-warning"
                          >
                            <RefreshCw className="size-3 animate-spin" />
                            体检进行中(无头快查)…
                          </span>
                        ) : null}
                        {row.check_note ? (
                          <span
                            role={
                              row.check_note.includes("失败") || row.check_note.includes("failed")
                                ? "alert"
                                : "status"
                            }
                            data-testid={`telegram-web-${row.account}-checknote`}
                            className="break-all text-2xs text-muted-foreground"
                          >
                            {row.check_note}
                          </span>
                        ) : null}
                        {!row.check_in_progress ? (
                          row.last_verified_at ? (
                            <span
                              data-testid={`telegram-web-${row.account}-verified`}
                              className={cn(
                                "text-2xs",
                                row.alive === false ? "text-dead" : "text-muted-foreground",
                              )}
                            >
                              上次检查 {formatRelativeTime(row.last_verified_at)} ·{" "}
                              {row.alive === false ? "已失效(建议重新登录)" : "正常"}
                            </span>
                          ) : (
                            <span className="text-2xs text-muted-foreground">未体检</span>
                          )
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
                          disabled={
                            busyAccount === row.account || row.login_in_progress || row.check_in_progress
                          }
                          onClick={() => void runCheck(row.account)}
                          data-testid={`telegram-web-${row.account}-check`}
                          title="检查登录状态:常驻监控在跑时直接读最新状态;后台检测中被占用会提示先停占用"
                        >
                          <Activity className="size-3.5" />
                          检测
                        </Button>
                        <Button
                          variant="outline"
                          size="sm"
                          disabled={
                            busyAccount === row.account || row.login_in_progress || row.check_in_progress
                          }
                          onClick={() => void startLogin(row.account, true)}
                          data-testid={`telegram-web-${row.account}-relogin`}
                          title="重新登录(--force):清除旧登录数据后打开浏览器登录窗,手机号+验证码在页面内输"
                        >
                          重新登录
                        </Button>
                        <Button
                          variant="outline"
                          size="sm"
                          disabled={
                            busyAccount === row.account || row.login_in_progress || row.check_in_progress
                          }
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
                  labelHint="键名格式:telegram-<标识>(小写字母数字起头);每键独立浏览器配置档(0600),多账号互不相通。"
                  hint="输入键名后点「添加账号」,打开浏览器登录窗口"
                />
                <FieldInput
                  label="备注名(可选)"
                  aria-label="新账号备注名"
                  placeholder="小号·尾号93105"
                  value={newAccountLabel}
                  onChange={(event) => setNewAccountLabel(event.target.value)}
                  labelHint="人读的名字,登录后显示在账号列表(内部键名认不出是哪个号);不填就显示键名。"
                  hint="与手机号/验证码无关,只是给你认号用的标签"
                />
                <div className="flex flex-wrap items-center justify-between gap-2">
                  <MessageCircle className="size-3.5 text-muted-foreground" />
                  <Button
                    size="sm"
                    onClick={handleAdd}
                    disabled={busyAccount !== null}
                    data-testid="telegram-web-add"
                    title="打开浏览器登录窗口(手机号+验证码在页面内输;验证码在你手机 TG 里)"
                  >
                    <Plus className="size-3.5" />
                    添加账号
                  </Button>
                </div>
              </div>
              {/* 回执尾段(问题7):随主容器 divide-y 收段 —— note 原落主
                  border 容器之外仅 border-t 接缝,「盒外孤岛」观感根因;
                  收容器即收敛,text-ok 成功回执语义档原样不降饱和。 */}
              <div className="flex flex-col gap-2 p-4">
                {actionError ? <ErrorBox error={actionError} /> : null}
                {note ? (
                  <p role="status" data-testid="telegram-action-note" className="text-xs leading-5 text-ok">
                    {note}
                  </p>
                ) : null}
              </div>
            </div>
          </>
        ) : null}
      </CardContent>
    </Card>
  );
}
