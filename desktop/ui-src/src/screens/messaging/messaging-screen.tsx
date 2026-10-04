import { AlertCircle, Bell, CheckCircle2, MessageCircle, RefreshCw, X } from "lucide-react";
import { useCallback, useEffect, useMemo, useState } from "react";

import { EmptyState } from "@/components/empty-state";
import { PageHeader } from "@/components/layout/page-header";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Skeleton } from "@/components/ui/skeleton";
import { Switch } from "@/components/ui/switch";
import {
  api,
  onSidecarEvent,
  type SidecarRequestError,
  type UnlistenFn,
} from "@/lib/api";
import { cn } from "@/lib/utils";

import { ErrorBox } from "../sources/error-box";
import {
  ALERT_CHANNELS,
  alertsDelete,
  alertsList,
  alertsSave,
  alertsTest,
  asSidecarError,
  bridgeStatus,
  channelsAliasDelete,
  channelsAliasSet,
  channelsList,
  channelsRefresh,
  formatIsoTimestamp,
  formatLastSeen,
  hasAlias,
  isDeadEntry,
  listAlertCategories,
  listSecretNames,
  parseCsvList,
  pushWrite,
  targetSpec,
} from "./api";
import type {
  AlertAction,
  AlertActionConfig,
  AlertCategoryOption,
  AlertRuleInput,
  AlertRuleView,
  AlertTestResult,
  AlertsTestParams,
  BridgeStatusView,
  ChannelEntry,
  ChannelsView,
  PushRuleEntry,
  PushRuleFile,
} from "./api";
import { buildPlatformCards, PlatformOverview } from "./platform-overview";

interface LoadState {
  status: "loading" | "error" | "ready";
  data: ChannelsView | null;
  error: SidecarRequestError | null;
}

/** 行内别名编辑态(一次只开一行:platform+chat_id 定位)。 */
interface AliasDraft {
  platform: string;
  chatId: string;
  value: string;
}

/** 顶部结构化提示:别名/刷新/保存动作的结果(ok)或失败(error)。 */
interface Notice {
  kind: "ok" | "error";
  text: string;
}

/**
 * 消息(task 10-03-messaging-ui):平台总览 + 通道目录 + 推送规则 + 底部状态条。
 *
 * 最上区·平台总览(task 10-03-messaging-hermes-look):左平台卡网格(头像 +
 * 名称 + 状态点)/ 右详情面板双栏 —— 详情含平台描述、三态状态说明、出站
 * 凭据指南(唯一入口;已实装平台)、已连接时的目录速览;三态(已连接绿 /
 * 需要设置黄 / 即将支持灰)由 secret.list 凭据探测 + channels.list 目录
 * 信号纯前端派生;全部/已连接/未启用三档筛选,切筛选带动选中切换。
 * 上区·通道目录:按平台分组(名称/类型/最后发现/死信徽标),每平台一个
 * 「刷新」按钮(触发 sidecar channels.refresh → discover_directory;失败
 * toast 结构化错误,旧目录不动),别名行内编辑写 channel_aliases.json 语义。
 * 下区·推送规则:按品类 YAML 分组列出 push 条目,每条目一个 targets 多选器
 * (选项 = 上区该平台目录条目,产出 `platform:名称`),保存走 push.write
 * 全量替换(服务端同门校验,失败零写入、界面如实报错)。
 * 下区·告警规则(10-04-alert-rules):对每条新入流情报求值,命中即推送/打标。
 * 列表行 = 启停 Switch(= 全量提交)/名称/scope/when 等宽摘要/动作徽章/命中
 * N/最近触发;新建编辑内联表单(when 文本校验反馈 = alerts.save 构造期错直显
 * + alerts.test dry 求值);删除二次确认;alerts.fired 事件 → toast + 命中数
 * 刷新(事件流既有通道 onSidecarEvent)。协议未实装(method_not_found)时
 * 子面板降级说明,不挡整屏。
 * 底部·状态条(R4;MYIA 版语义,不做 RAM/网关):sidecar 健康(health
 * 一来一回成功即存活证明)+ 已连接平台计数;常驻(sticky)于滚动底部。
 * 空态(目录为空)给「先配平台凭据」指引;断连态与现有屏同范式(ErrorBox+重试)。
 * 字号全走 D2 阶梯 token(task 10-03-ui-deep-imitation:辅文 11px=text-2xs,
 * 结构不动,仅 token 贯彻)。
 */
export function MessagingScreen() {
  const [state, setState] = useState<LoadState>({ status: "loading", data: null, error: null });
  const [refreshing, setRefreshing] = useState<Set<string>>(new Set());
  const [aliasDraft, setAliasDraft] = useState<AliasDraft | null>(null);
  const [aliasBusy, setAliasBusy] = useState(false);
  /** targets 草稿:file → entryIndex → 已选 spec 列表(缺省回退 rules 视图值)。 */
  const [drafts, setDrafts] = useState<Record<string, Record<number, string[]>>>({});
  const [savingFile, setSavingFile] = useState<string | null>(null);
  const [notice, setNotice] = useState<Notice | null>(null);
  /** 钥匙链凭据名清单(平台总览凭据探测;加载失败降级为空名单)。 */
  const [secretNames, setSecretNames] = useState<string[]>([]);
  /** 微信桥接探测(bridge.status;失败降级 null = 灰态「需本机 Hermes」,
   * 不挡整屏目录视图——发送期的结构化错误是通道层的事)。 */
  const [bridge, setBridge] = useState<BridgeStatusView | null>(null);
  /** R4 状态条:sidecar 健康(health 一来一回成功即 true;null = 检测中)。 */
  const [sidecarHealthy, setSidecarHealthy] = useState<boolean | null>(null);

  const reload = useCallback(async () => {
    setState({ status: "loading", data: null, error: null });
    try {
      const [data, names, healthy, bridgeProbe] = await Promise.all([
        channelsList(),
        // 凭据探测(secret.list)是平台卡的次要信号:钥匙链不可用时降级为
        // 空名单,三态回退到「目录非空」单一证据,不挡整屏目录视图。
        listSecretNames().catch(() => [] as string[]),
        // R4 状态条信号一:health 方法本身即存活证明(成功应答 = true;
        // 任何失败降级为 false,不挡目录视图)
        api.health().then(
          () => true,
          () => false,
        ),
        // 微信桥接探测:失败降级 null(灰态),绝不挡目录视图
        bridgeStatus().catch(() => null),
      ]);
      setSecretNames(names);
      setSidecarHealthy(healthy);
      setBridge(bridgeProbe);
      setState({ status: "ready", data, error: null });
    } catch (error) {
      // channels.list 都失败了:sidecar 显然不可达,状态条如实转红
      setSidecarHealthy(false);
      setState({ status: "error", data: null, error: asSidecarError(error) });
    }
  }, []);

  useEffect(() => {
    void reload();
  }, [reload]);

  const platforms = useMemo(
    () => Object.keys(state.data?.platforms ?? {}).sort(),
    [state.data],
  );

  const handleRefresh = useCallback(
    async (platform: string) => {
      setNotice(null);
      setRefreshing((prev) => new Set(prev).add(platform));
      try {
        const result = await channelsRefresh(platform);
        setNotice({ kind: "ok", text: `${platform} 目录已刷新(${result.merged} 个会话)` });
        await reload();
      } catch (error) {
        const structured = asSidecarError(error);
        setNotice({ kind: "error", text: `${platform} 刷新失败:${structured.message}(code=${structured.code})` });
      } finally {
        setRefreshing((prev) => {
          const next = new Set(prev);
          next.delete(platform);
          return next;
        });
      }
    },
    [reload],
  );

  const startAliasEdit = useCallback(
    (entry: ChannelEntry) => {
      setNotice(null);
      const current = state.data?.aliases[entry.platform]?.[entry.chat_id] ?? entry.name;
      setAliasDraft({ platform: entry.platform, chatId: entry.chat_id, value: current });
    },
    [state.data],
  );

  const submitAlias = useCallback(
    async (apply: boolean) => {
      if (!aliasDraft) return;
      if (!apply) {
        setAliasDraft(null);
        return;
      }
      const value = aliasDraft.value.trim();
      if (!value) {
        setNotice({ kind: "error", text: "别名不能为空(要清除别名请用「取消别名」)" });
        return;
      }
      setAliasBusy(true);
      try {
        await channelsAliasSet(aliasDraft.platform, aliasDraft.chatId, value);
        setNotice({ kind: "ok", text: `已命名 ${aliasDraft.platform}:${value}` });
        setAliasDraft(null);
        await reload();
      } catch (error) {
        const structured = asSidecarError(error);
        setNotice({ kind: "error", text: `别名保存失败:${structured.message}(code=${structured.code})` });
      } finally {
        setAliasBusy(false);
      }
    },
    [aliasDraft, reload],
  );

  const removeAlias = useCallback(
    async (entry: ChannelEntry) => {
      setNotice(null);
      setAliasBusy(true);
      try {
        await channelsAliasDelete(entry.platform, entry.chat_id);
        setNotice({ kind: "ok", text: `已取消 ${entry.platform}:${entry.chat_id} 的别名(回退发现名)` });
        await reload();
      } catch (error) {
        const structured = asSidecarError(error);
        setNotice({ kind: "error", text: `别名删除失败:${structured.message}(code=${structured.code})` });
      } finally {
        setAliasBusy(false);
      }
    },
    [reload],
  );

  /** 当前生效 targets:草稿优先,缺省回退 rules 视图的落盘值。 */
  const currentTargets = useCallback(
    (file: string, entry: PushRuleEntry): string[] =>
      drafts[file]?.[entry.index] ?? entry.targets,
    [drafts],
  );

  const toggleTarget = useCallback(
    (file: string, entry: PushRuleEntry, spec: string) => {
      setNotice(null);
      const current = drafts[file]?.[entry.index] ?? entry.targets;
      const next = current.includes(spec)
        ? current.filter((candidate) => candidate !== spec)
        : [...current, spec];
      setDrafts((prev) => ({
        ...prev,
        [file]: { ...(prev[file] ?? {}), [entry.index]: next },
      }));
    },
    [drafts],
  );

  const saveRuleFile = useCallback(
    async (ruleFile: PushRuleFile) => {
      setNotice(null);
      setSavingFile(ruleFile.file);
      try {
        // 全量替换契约(design.md D2):提交该文件完整 push 数组 —— raw 为
        // base,仅覆盖 targets;push.write 服务端同门校验,失败零写入。
        const nextPush = ruleFile.entries.map((entry) =>
          entry.platform
            ? { ...entry.raw, targets: currentTargets(ruleFile.file, entry) }
            : entry.raw,
        );
        const result = await pushWrite(ruleFile.file, nextPush);
        setNotice({
          kind: "ok",
          text: result.changed
            ? `已保存 ${ruleFile.category_id ?? ruleFile.file} 的推送对象`
            : `${ruleFile.category_id ?? ruleFile.file} 无变更`,
        });
        setDrafts((prev) => {
          const next = { ...prev };
          delete next[ruleFile.file];
          return next;
        });
        await reload();
      } catch (error) {
        const structured = asSidecarError(error);
        setNotice({ kind: "error", text: `保存失败:${structured.message}(code=${structured.code})` });
      } finally {
        setSavingFile(null);
      }
    },
    [currentTargets, reload],
  );

  const data = state.data;

  /** R4 状态条信号二:已连接平台计数(与平台总览同一纯函数派生,不另立口径)。 */
  const cards = useMemo(
    () => buildPlatformCards(data?.platforms ?? {}, secretNames, bridge),
    [data, secretNames, bridge],
  );
  const connectedCount = useMemo(
    () => cards.filter((card) => card.status === "connected").length,
    [cards],
  );

  return (
    /* R2 重排:区块节奏消费具名令牌 gap-block(24px)+ pb-block(消息屏
        原本无底距,基调层补过,这里显式落字) */
    <div className="flex flex-col gap-block pb-block">
      <PageHeader
        title="消息"
        description="平台总览与接入态;通道目录浏览与别名命名;给推送规则挑选具体会话(保存写回品类 YAML)"
        actions={
          <>
            {data ? (
              <Badge variant="outline" data-testid="directory-updated">
                {data.updated_at ? `目录 ${data.updated_at.slice(0, 16).replace("T", " ")}` : "目录从未刷新"}
              </Badge>
            ) : null}
            <Button size="sm" variant="outline" onClick={() => void reload()} disabled={state.status === "loading"}>
              <RefreshCw className={state.status === "loading" ? "size-3.5 animate-spin" : "size-3.5"} />
              刷新
            </Button>
          </>
        }
      />

      {state.status === "error" && state.error ? (
        <ErrorBox error={state.error} onRetry={() => void reload()} />
      ) : null}

      {notice ? (
        /* 10-04-ui-kestra-anchor:通知走 Kestra 通知中心范式(结构借自
           Apache-2.0 design-system KsNotification/ElNotification:右上角浮卡
           +类型图标+可关闭,借结构改语义)。不自动消失:结果性通知(保存/
           刷新/别名)由用户关或下一次操作替换,行为面零改动 */
        <div className="pointer-events-none fixed top-16 right-6 z-50 flex flex-col items-end gap-2">
          <div
            role={notice.kind === "error" ? "alert" : "status"}
            data-testid="messaging-notice"
            className={
              "pointer-events-auto flex w-84 animate-pop-in items-start gap-2.5 rounded-lg border border-border border-l-2 bg-popover/95 px-4 py-3 shadow-popover backdrop-blur " +
              (notice.kind === "error" ? "border-l-destructive" : "border-l-ok")
            }
          >
            {notice.kind === "error" ? (
              <AlertCircle className="mt-0.5 size-4 shrink-0 text-dead" />
            ) : (
              <CheckCircle2 className="mt-0.5 size-4 shrink-0 text-ok" />
            )}
            <p
              className={
                "min-w-0 flex-1 text-left text-xs leading-5 " +
                (notice.kind === "error" ? "text-dead" : "text-foreground")
              }
            >
              {notice.text}
            </p>
            <button
              type="button"
              aria-label="关闭通知"
              className="-m-1 shrink-0 rounded-md p-1 text-muted-foreground transition-colors duration-(--duration-fast) ease-out-expo hover:bg-accent/60 hover:text-foreground"
              onClick={() => setNotice(null)}
            >
              <X className="size-3.5" />
            </button>
          </div>
        </div>
      ) : null}

      {/* ---------------- 最上区:平台总览(左卡网格 + 右详情面板 + 三态 tone + 筛选) ---------------- */}
      <PlatformOverview
        status={state.status}
        directory={data?.platforms ?? {}}
        secretNames={secretNames}
        dead={data?.dead ?? []}
        bridgeStatus={bridge}
      />

      {/* ---------------- 上区:通道目录(按平台分组) ---------------- */}
      <div className="px-6">
        <Card>
          {/* R2 刀3:卡头层级化(CardTitle 13 semibold + CardDescription),
              说明文字不再挤在标题行括号里 */}
          <CardHeader>
            <CardTitle as="h2" className="flex items-center gap-2">
              <MessageCircle className="size-4 text-muted-foreground" />
              通道目录
            </CardTitle>
            <CardDescription>目录 = 可寻址的推送对象;别名是手工命名,重建后仍生效</CardDescription>
          </CardHeader>
          <CardContent className="flex flex-col gap-4">

            {state.status === "loading" ? (
              <div className="flex flex-col gap-2" aria-label="加载中">
                {[0, 1, 2].map((index) => (
                  <Skeleton key={index} className="h-9 w-full" />
                ))}
              </div>
            ) : state.status === "ready" && platforms.length === 0 ? (
              <EmptyState
                title="通道目录还是空的"
                description="先到「设置」录入平台凭据(经钥匙链的 bot token),再回到这里点刷新;飞书会列出 bot 所在的群,telegram 会话随 bot 收到消息自动入目录。"
                tag="可空态"
              />
            ) : (
              platforms.map((platform) => (
                <div key={platform} className="flex flex-col gap-1.5" data-testid={`platform-${platform}`}>
                  <div className="flex items-center justify-between gap-2">
                    <p className="text-xs font-medium text-foreground">{platform}</p>
                    <Button
                      size="sm"
                      variant="ghost"
                      disabled={refreshing.has(platform)}
                      onClick={() => void handleRefresh(platform)}
                    >
                      <RefreshCw className={refreshing.has(platform) ? "size-3.5 animate-spin" : "size-3.5"} />
                      {refreshing.has(platform) ? "发现中…" : "刷新"}
                    </Button>
                  </div>
                  {/* Kestra 列表密度:逐行边框盒 → hairline 分隔行(hover 弱底) */}
                  <ul className="flex flex-col divide-y divide-border/60">
                    {(data?.platforms[platform] ?? []).map((entry) => {
                      const aliased = data ? hasAlias(entry, data.aliases) : false;
                      const dead = data ? isDeadEntry(entry, data.dead) : false;
                      const editing =
                        aliasDraft?.platform === entry.platform && aliasDraft?.chatId === entry.chat_id;
                      return (
                        <li
                          key={`${entry.platform}:${entry.chat_id}`}
                          className="flex flex-col gap-1 py-3 transition-colors duration-(--duration-fast) ease-out-expo hover:bg-accent/25"
                          data-testid={`entry-${entry.chat_id}`}
                        >
                          <div className="flex items-center justify-between gap-2">
                            <span className="flex min-w-0 items-center gap-2 text-sm">
                              <Badge variant="outline">{entry.type}</Badge>
                              <span className="truncate font-medium text-foreground">{entry.name}</span>
                              {aliased ? <Badge variant="secondary">别名</Badge> : null}
                              {dead ? (
                                <Badge variant="destructive" title="此前投递确认不可达,重发成功后自愈">
                                  死信
                                </Badge>
                              ) : null}
                              <span className="truncate font-mono text-2xs text-muted-foreground">
                                {entry.chat_id}
                              </span>
                            </span>
                            {/* 终审修整:辅助文字(最后发现)mono 弱化与主信息分层;
                                「改名/取消别名」钮距统一 gap-1.5(VL 指认辅助文字
                                未与主信息对齐、按钮间距不一致) */}
                            <span className="flex shrink-0 items-center gap-2.5">
                              <span className="font-mono text-2xs text-muted-foreground">
                                最后发现 {formatLastSeen(entry.last_seen)}
                              </span>
                              {editing ? null : (
                                <span className="flex items-center gap-1.5">
                                  <Button
                                    size="sm"
                                    variant="ghost"
                                    disabled={aliasBusy}
                                    onClick={() => startAliasEdit(entry)}
                                  >
                                    改名
                                  </Button>
                                  {aliased ? (
                                    <Button
                                      size="sm"
                                      variant="ghost"
                                      disabled={aliasBusy}
                                      onClick={() => void removeAlias(entry)}
                                    >
                                      取消别名
                                    </Button>
                                  ) : null}
                                </span>
                              )}
                            </span>
                          </div>
                          {editing && aliasDraft ? (
                            <div className="flex items-center gap-2 pl-1" role="group" aria-label="别名编辑">
                              <Input
                                aria-label={`别名 ${entry.chat_id}`}
                                className="w-56 text-xs"
                                value={aliasDraft.value}
                                autoFocus
                                disabled={aliasBusy}
                                onChange={(event) =>
                                  setAliasDraft({ ...aliasDraft, value: event.target.value })
                                }
                                onKeyDown={(event) => {
                                  if (event.key === "Enter") void submitAlias(true);
                                  if (event.key === "Escape") void submitAlias(false);
                                }}
                              />
                              <Button size="sm" disabled={aliasBusy} onClick={() => void submitAlias(true)}>
                                保存
                              </Button>
                              <Button size="sm" variant="ghost" disabled={aliasBusy} onClick={() => void submitAlias(false)}>
                                取消
                              </Button>
                            </div>
                          ) : null}
                        </li>
                      );
                    })}
                  </ul>
                </div>
              ))
            )}
          </CardContent>
        </Card>
      </div>

      {/* ---------------- 下区:推送规则面板(按品类文件分组) ---------------- */}
      <div className="px-6">
        <Card>
          <CardHeader>
            <CardTitle as="h2">推送规则</CardTitle>
            <CardDescription>给每条规则勾选具体推送对象;保存 = 全量写回该品类 YAML 的 push[]</CardDescription>
          </CardHeader>
          <CardContent className="flex flex-col gap-4">

            {state.status === "loading" ? (
              <div className="flex flex-col gap-2" aria-label="加载中">
                {[0, 1].map((index) => (
                  <Skeleton key={index} className="h-9 w-full" />
                ))}
              </div>
            ) : state.status === "ready" && (data?.rules.length ?? 0) === 0 ? (
              <EmptyState
                compact
                title="还没有品类 YAML"
                description="推送规则来自品类 YAML 的 push 节;先到「源管理/配置编辑」建品类。"
              />
            ) : (
              (data?.rules ?? []).map((ruleFile) => (
                <RuleFileGroup
                  key={ruleFile.file}
                  ruleFile={ruleFile}
                  data={data}
                  currentTargets={(entry) => currentTargets(ruleFile.file, entry)}
                  onToggle={(entry, spec) => toggleTarget(ruleFile.file, entry, spec)}
                  saving={savingFile === ruleFile.file}
                  onSave={() => void saveRuleFile(ruleFile)}
                />
              ))
            )}
          </CardContent>
        </Card>
      </div>

      {/* ---------------- 下区:告警规则子面板(10-04-alert-rules;同属「消息怎么发」心智) ---------------- */}
      <AlertRulesPanel />

      {/* ---------------- 底部:状态条(R4;常驻滚动底;MYIA 版语义,不做 RAM/网关) ---------------- */}
      <div
        className="sticky bottom-0 z-10 flex items-center justify-between gap-3 border-t border-border bg-background/95 px-6 py-2 text-2xs text-muted-foreground backdrop-blur"
        data-testid="messaging-statusbar"
      >
        <span className="flex items-center gap-1.5">
          <span
            aria-hidden="true"
            className={cn(
              "inline-block size-1.5 rounded-full",
              sidecarHealthy === true
                ? "bg-ok"
                : sidecarHealthy === false
                  ? "bg-destructive"
                  : "bg-muted-foreground/50",
            )}
          />
          {sidecarHealthy === true
            ? "sidecar 正常"
            : sidecarHealthy === false
              ? "sidecar 不可达"
              : "sidecar 检测中"}
        </span>
        <span>
          {state.status === "ready"
            ? `已连接平台 ${connectedCount}/${cards.length}`
            : "已连接平台 …"}
        </span>
      </div>
    </div>
  );
}

/** 一个品类 YAML 的规则组:坏文件如实展示错误;targeting 条目出多选器。 */
function RuleFileGroup({
  ruleFile,
  data,
  currentTargets,
  onToggle,
  saving,
  onSave,
}: {
  ruleFile: PushRuleFile;
  data: ChannelsView | null;
  currentTargets: (entry: PushRuleEntry) => string[];
  onToggle: (entry: PushRuleEntry, spec: string) => void;
  saving: boolean;
  onSave: () => void;
}) {
  const targetingEntries = ruleFile.entries.filter((entry) => entry.platform !== null);
  return (
    <div className="flex flex-col gap-2 rounded-md border border-border/60 p-3" data-testid={`rule-file-${ruleFile.category_id ?? ruleFile.file}`}>
      <div className="flex items-center justify-between gap-2">
        <p className="flex min-w-0 items-center gap-2 text-sm">
          <span className="truncate font-medium text-foreground">
            {ruleFile.category_name ?? ruleFile.file}
          </span>
          {ruleFile.parse_ok ? null : <Badge variant="destructive">加载失败</Badge>}
          <span className="truncate font-mono text-2xs text-muted-foreground">{ruleFile.file}</span>
        </p>
        {ruleFile.parse_ok && targetingEntries.length > 0 ? (
          <Button size="sm" disabled={saving} onClick={onSave}>
            {saving ? "保存中…" : "保存推送对象"}
          </Button>
        ) : null}
      </div>
      {ruleFile.parse_ok ? null : (
        <p className="text-xs text-destructive" role="alert">
          {ruleFile.error?.code}:{ruleFile.error?.message}(修好后此处自动恢复;去「配置编辑」处理)
        </p>
      )}
      {ruleFile.parse_ok && ruleFile.entries.length === 0 ? (
        <p className="text-xs text-muted-foreground">该品类未配置 push 通道(条目仅入库)。</p>
      ) : null}
      {ruleFile.entries.map((entry) => {
        const bucket = entry.platform ? (data?.platforms[entry.platform] ?? []) : [];
        const selected = currentTargets(entry);
        return (
          <div
            key={`${ruleFile.file}:${entry.index}`}
            className="flex flex-col gap-1.5 rounded-md bg-muted/30 px-3 py-2"
            data-entry-index={entry.index}
          >
            <p className="flex flex-wrap items-center gap-1.5 text-xs">
              <Badge variant="default">{entry.channel}</Badge>
              {entry.has_template ? <Badge variant="outline">自定义模板</Badge> : null}
              {entry.route_count > 0 ? <Badge variant="outline">规则 ×{entry.route_count}</Badge> : null}
              {entry.platform === null ? (
                <span className="text-muted-foreground">该通道不支持目录寻址(对象由 target 引用决定)</span>
              ) : selected.length === 0 ? (
                <span className="text-warning">未选对象(该规则不会定向投递)</span>
              ) : (
                <span className="font-mono text-muted-foreground">{selected.join(", ")}</span>
              )}
            </p>
            {entry.platform ? (
              bucket.length === 0 ? (
                <p className="text-2xs text-muted-foreground">
                  {entry.platform} 目录为空:先在上区「刷新」(飞书)或等 bot 收到消息(telegram 被动积累)。
                </p>
              ) : (
                <div className="flex flex-col gap-1" role="group" aria-label={`推送对象 ${entry.channel}`}>
                  {bucket.map((option) => {
                    const spec = targetSpec(option);
                    const dead = data ? isDeadEntry(option, data.dead) : false;
                    return (
                      <label key={option.chat_id} className="flex min-h-7 items-center gap-2 text-xs">
                        <input
                          type="checkbox"
                          className="accent-primary"
                          checked={selected.includes(spec)}
                          onChange={() => onToggle(entry, spec)}
                          aria-label={`对象 ${option.name}`}
                        />
                        <span className="truncate">{option.name}</span>
                        <span className="truncate font-mono text-2xs text-muted-foreground">
                          {option.chat_id}
                        </span>
                        {dead ? <Badge variant="destructive">死信</Badge> : null}
                      </label>
                    );
                  })}
                </div>
              )
            ) : null}
          </div>
        );
      })}
    </div>
  );
}

// ---------------------------------------------------------------------------
// 告警规则子面板(10-04-alert-rules Stage E;契约 = 任务档 design.md §4/§9)
// ---------------------------------------------------------------------------

/** 表单草稿(新建无 id;编辑带 id + 保留 enabled——启停在行上,表单不出)。 */
interface AlertFormDraft {
  id?: number;
  enabled: boolean;
  name: string;
  scope: string;
  when: string;
  action: AlertAction;
  channel: string;
  targets: string;
  template: string;
  tags: string;
}

/** 测试面板态:key 定位触发源(行 = `rule-{id}`,草稿 = "draft")。 */
interface AlertTestPanelState {
  key: string;
  running: boolean;
  result: AlertTestResult | null;
  error: SidecarRequestError | null;
}

function emptyAlertDraft(): AlertFormDraft {
  return {
    enabled: true,
    name: "",
    scope: "global",
    when: "",
    action: "push",
    channel: "",
    targets: "",
    template: "",
    tags: "",
  };
}

function ruleToDraft(rule: AlertRuleView): AlertFormDraft {
  return {
    id: rule.id,
    enabled: rule.enabled,
    name: rule.name,
    scope: rule.scope,
    when: rule.when,
    action: rule.action,
    channel: rule.action_config.channel ?? "",
    targets: (rule.action_config.targets ?? []).join(", "),
    template: rule.action_config.template ?? "",
    tags: (rule.action_config.tags ?? []).join(", "),
  };
}

/** 视图 → save 载荷(全量替换的写回 base;启停翻转走这里保 id)。 */
function ruleToInput(rule: AlertRuleView): AlertRuleInput {
  return {
    id: rule.id,
    name: rule.name,
    enabled: rule.enabled,
    scope: rule.scope,
    when: rule.when,
    action: rule.action,
    action_config: rule.action_config,
  };
}

/** 草稿 → save/test 载荷(targets/tags 逗号分隔解析;可选项空则不携带)。 */
function draftToInput(draft: AlertFormDraft): AlertRuleInput {
  const targets = parseCsvList(draft.targets);
  const tags = parseCsvList(draft.tags);
  const action_config: AlertActionConfig =
    draft.action === "push"
      ? {
          channel: draft.channel,
          ...(targets.length > 0 ? { targets } : {}),
          ...(draft.template.trim() ? { template: draft.template.trim() } : {}),
        }
      : { tags };
  return {
    ...(draft.id !== undefined ? { id: draft.id } : {}),
    name: draft.name.trim(),
    enabled: draft.enabled,
    scope: draft.scope,
    when: draft.when.trim(),
    action: draft.action,
    action_config,
  };
}

/** 列表行的动作徽章文本:push → 通道名;tag → 标签清单(design §9)。 */
function actionBadgeText(rule: AlertRuleView): string {
  if (rule.action === "push") {
    return `推送 → ${rule.action_config.channel ?? "?"}`;
  }
  return `打标:${(rule.action_config.tags ?? []).join(" / ") || "?"}`;
}

/**
 * 告警规则子面板:列表(启停/名称/scope/when 摘要/动作/命中 N/最近触发)
 * + 新建编辑内联表单 + dry 测试 + 删除二次确认 + alerts.fired 事件消费。
 *
 * 面板自管数据与错误:alerts.list 失败不拖挂整屏 —— 旧版 sidecar
 * (method_not_found)降级为「协议未实装」说明;其余错误局部呈现 + 重试。
 */
function AlertRulesPanel() {
  const [rules, setRules] = useState<AlertRuleView[] | null>(null);
  const [loadError, setLoadError] = useState<SidecarRequestError | null>(null);
  const [unsupported, setUnsupported] = useState(false);
  const [categories, setCategories] = useState<AlertCategoryOption[]>([]);
  const [form, setForm] = useState<AlertFormDraft | null>(null);
  const [saving, setSaving] = useState(false);
  const [togglingId, setTogglingId] = useState<number | null>(null);
  const [pendingDelete, setPendingDelete] = useState<number | null>(null);
  const [deleting, setDeleting] = useState(false);
  const [testPanel, setTestPanel] = useState<AlertTestPanelState | null>(null);
  const [notice, setNotice] = useState<{ kind: "ok" | "error"; text: string } | null>(null);

  const loadRules = useCallback(async () => {
    setRules(null);
    setLoadError(null);
    setUnsupported(false);
    try {
      const view = await alertsList();
      setRules(view.rules);
    } catch (error) {
      const structured = asSidecarError(error);
      // 旧版 sidecar 无 alerts.* 方法:降级说明(bridge.status 失败降级同款
      // 哲学),其余错误(库损坏/服务故障)局部呈现 + 重试
      if (structured.code === "method_not_found") setUnsupported(true);
      else setLoadError(structured);
    }
  }, []);

  useEffect(() => {
    void loadRules();
  }, [loadRules]);

  // scope 品类下拉(yaml.list)是次要信号:失败降级空名单(下拉只剩「全局」)
  useEffect(() => {
    let cancelled = false;
    listAlertCategories()
      .catch(() => [] as AlertCategoryOption[])
      .then((options) => {
        if (!cancelled) setCategories(options);
      });
    return () => {
      cancelled = true;
    };
  }, []);

  // alerts.fired 事件(design §4.2/§9):toast(本面板 notice)+ 规则行命中数
  // 刷新 —— 本地增量(fired_count+1 / last_fired_at=事件 ts),不整表重拉。
  // alerts.fired 已入 SidecarEvent 联合(10-04 fe-gap-census R2),此处直接窄化
  useEffect(() => {
    let unlisten: UnlistenFn | null = null;
    let cancelled = false;
    void onSidecarEvent((event) => {
      if (event.type !== "alerts.fired") return;
      setNotice({
        kind: "ok",
        text: `告警命中:${event.rule_name}${event.title ? `「${event.title}」` : ""}(${event.action_status})`,
      });
      setRules((prev) =>
        prev
          ? prev.map((rule) =>
              rule.id === event.rule_id
                ? { ...rule, fired_count: rule.fired_count + 1, last_fired_at: event.ts }
                : rule,
            )
          : prev,
      );
    }).then((un) => {
      if (cancelled) un();
      else unlisten = un;
    });
    return () => {
      cancelled = true;
      unlisten?.();
    };
  }, []);

  /** 启停 = 整数组提交时该行 enabled 翻转(design §4.1 钉死①,不设独立启停方法)。 */
  const toggleRule = useCallback(
    async (rule: AlertRuleView) => {
      setNotice(null);
      setTogglingId(rule.id);
      try {
        const next = (rules ?? []).map((candidate) =>
          candidate.id === rule.id ? { ...candidate, enabled: !candidate.enabled } : candidate,
        );
        const result = await alertsSave(next.map(ruleToInput));
        setRules(result.rules);
      } catch (error) {
        const structured = asSidecarError(error);
        setNotice({ kind: "error", text: `启停失败:${structured.message}(code=${structured.code})` });
      } finally {
        setTogglingId(null);
      }
    },
    [rules],
  );

  const submitForm = useCallback(async () => {
    if (!form) return;
    // 前端轻预检(完整门 = 服务端 alerts.save 构造期拒,alert_rule_invalid 直显)
    if (!form.name.trim()) {
      setNotice({ kind: "error", text: "规则名称不能为空" });
      return;
    }
    if (!form.when.trim()) {
      setNotice({ kind: "error", text: "when 表达式不能为空" });
      return;
    }
    if (form.action === "push" && !form.channel) {
      setNotice({ kind: "error", text: "推送动作需选择通道(channel)" });
      return;
    }
    if (form.action === "tag" && parseCsvList(form.tags).length === 0) {
      setNotice({ kind: "error", text: "打标动作需至少一个标签(逗号分隔)" });
      return;
    }
    setNotice(null);
    setSaving(true);
    try {
      // 全量替换:其余规则原样(id 保稳)+ 本草稿替换/追加
      const base = (rules ?? []).filter((rule) => rule.id !== form.id);
      const result = await alertsSave([...base.map(ruleToInput), draftToInput(form)]);
      setRules(result.rules);
      setForm(null);
      setNotice({ kind: "ok", text: `告警规则已保存:${form.name.trim()}` });
    } catch (error) {
      const structured = asSidecarError(error);
      setNotice({ kind: "error", text: `保存失败:${structured.message}(code=${structured.code})` });
    } finally {
      setSaving(false);
    }
  }, [form, rules]);

  const confirmDelete = useCallback(async (ruleId: number) => {
    setNotice(null);
    setDeleting(true);
    try {
      await alertsDelete(ruleId);
      setRules((prev) => (prev ? prev.filter((rule) => rule.id !== ruleId) : prev));
      setPendingDelete(null);
      setNotice({ kind: "ok", text: "规则已删除(命中历史照留,可在 CLI `myssia alerts list` 查看)" });
    } catch (error) {
      const structured = asSidecarError(error);
      setNotice({ kind: "error", text: `删除失败:${structured.message}(code=${structured.code})` });
    } finally {
      setDeleting(false);
    }
  }, []);

  /** dry 测试:行(rule_id)/草稿(rule)两形态;不真发不落 fired(design §4.1)。 */
  const runTest = useCallback(async (key: string, params: AlertsTestParams) => {
    setNotice(null);
    setTestPanel({ key, running: true, result: null, error: null });
    try {
      const result = await alertsTest(params);
      setTestPanel({ key, running: false, result, error: null });
    } catch (error) {
      setTestPanel({ key, running: false, result: null, error: asSidecarError(error) });
    }
  }, []);

  return (
    <div className="px-6">
      <Card>
        <CardHeader className="flex-row items-start justify-between gap-2">
          <div className="flex min-w-0 flex-col gap-0.5">
            <CardTitle as="h2" className="flex items-center gap-2">
              <Bell className="size-4 text-muted-foreground" />
              告警规则
            </CardTitle>
            <CardDescription>对每条新入流情报求值,命中即推送/打标;保存 = 全量写回规则表</CardDescription>
          </div>
          {unsupported ? null : (
            <Button
              size="sm"
              className="shrink-0"
              disabled={form !== null || saving}
              onClick={() => {
                setNotice(null);
                setTestPanel(null);
                setForm(emptyAlertDraft());
              }}
            >
              新建规则
            </Button>
          )}
        </CardHeader>
        <CardContent className="flex flex-col gap-4" data-testid="alert-rules-panel">

          {notice ? (
            <div
              role={notice.kind === "error" ? "alert" : "status"}
              className={
                notice.kind === "error"
                  ? "rounded-md border border-destructive/30 bg-destructive/10 px-3 py-2 text-xs text-destructive"
                  : "rounded-md border border-ok/30 bg-ok/10 px-3 py-2 text-xs text-ok"
              }
              data-testid="alert-rules-notice"
            >
              {notice.text}
            </div>
          ) : null}

          {unsupported ? (
            <p className="text-xs text-muted-foreground" data-testid="alert-rules-unsupported">
              当前 sidecar 版本还没有告警规则方法(需要协议 v7 的 alerts.* 方法族);升级后此处自动可用,其余面板功能不受影响。
            </p>
          ) : rules === null && loadError === null ? (
            <div className="flex flex-col gap-2" aria-label="加载中">
              {[0, 1].map((index) => (
                <Skeleton key={index} className="h-9 w-full" />
              ))}
            </div>
          ) : loadError ? (
            <div
              className="flex flex-col gap-1.5 rounded-md border border-destructive/30 bg-destructive/10 px-3 py-2 text-xs text-destructive"
              data-testid="alert-rules-error"
            >
              <span>
                告警规则加载失败:{loadError.message}(code={loadError.code})
              </span>
              <Button
                size="sm"
                variant="outline"
                className="self-start"
                onClick={() => void loadRules()}
              >
                重试
              </Button>
            </div>
          ) : (rules ?? []).length === 0 && form === null ? (
            <EmptyState
              compact
              title="还没有告警规则"
              description="新建规则后,每条新入流的情报都会求值一次:命中即立即推送或打标;不配规则则一切照旧(零惊扰)。"
            />
          ) : (
            <ul className="flex flex-col gap-2">
              {(rules ?? []).map((rule) => (
                <li
                  key={rule.id}
                  className="flex flex-col gap-1.5 rounded-md border border-border/60 px-3 py-2"
                  data-testid={`alert-rule-${rule.id}`}
                >
                  <div className="flex items-center justify-between gap-2">
                    <span className="flex min-w-0 items-center gap-2 text-sm">
                      <Switch
                        checked={rule.enabled}
                        disabled={togglingId === rule.id}
                        onCheckedChange={() => void toggleRule(rule)}
                        aria-label={`启停 ${rule.name}`}
                      />
                      <span className="truncate font-medium text-foreground">{rule.name}</span>
                      <Badge variant="outline">{rule.scope === "global" ? "全局" : rule.scope}</Badge>
                      <code className="truncate font-mono text-2xs text-muted-foreground" title={rule.when}>
                        when {rule.when}
                      </code>
                    </span>
                    <span className="flex shrink-0 items-center gap-1">
                      {togglingId === rule.id ? <span className="text-2xs text-muted-foreground">提交中…</span> : null}
                      <Button
                        size="sm"
                        variant="ghost"
                        disabled={testPanel?.running === true}
                        onClick={() => {
                          setForm(null);
                          void runTest(`rule-${rule.id}`, { rule_id: rule.id });
                        }}
                      >
                        测试
                      </Button>
                      <Button
                        size="sm"
                        variant="ghost"
                        onClick={() => {
                          setNotice(null);
                          setTestPanel(null);
                          setPendingDelete(null);
                          setForm(ruleToDraft(rule));
                        }}
                      >
                        编辑
                      </Button>
                      {pendingDelete === rule.id ? (
                        <>
                          <Button
                            size="sm"
                            variant="destructive"
                            disabled={deleting}
                            onClick={() => void confirmDelete(rule.id)}
                          >
                            {deleting ? "删除中…" : "确认删除"}
                          </Button>
                          <Button
                            size="sm"
                            variant="ghost"
                            disabled={deleting}
                            onClick={() => setPendingDelete(null)}
                          >
                            取消
                          </Button>
                        </>
                      ) : (
                        <Button
                          size="sm"
                          variant="ghost"
                          onClick={() => {
                            setNotice(null);
                            setPendingDelete(rule.id);
                          }}
                        >
                          删除
                        </Button>
                      )}
                    </span>
                  </div>
                  <p className="flex flex-wrap items-center gap-2 pl-9 text-2xs text-muted-foreground">
                    <Badge variant={rule.action === "push" ? "default" : "secondary"}>
                      {actionBadgeText(rule)}
                    </Badge>
                    <span>命中 {rule.fired_count}</span>
                    <span>最近触发 {formatIsoTimestamp(rule.last_fired_at)}</span>
                    {!rule.enabled ? <Badge variant="outline">已停用</Badge> : null}
                  </p>
                </li>
              ))}
            </ul>
          )}

          {form ? (
            <AlertRuleForm
              draft={form}
              categories={categories}
              saving={saving}
              testRunning={testPanel?.key === "draft" && testPanel.running}
              onChange={setForm}
              onCancel={() => setForm(null)}
              onSubmit={() => void submitForm()}
              onTest={() => void runTest("draft", { rule: draftToInput(form) })}
            />
          ) : null}

          {testPanel ? <AlertTestResultPanel state={testPanel} /> : null}
        </CardContent>
      </Card>
    </div>
  );
}

/** 新建/编辑内联表单:when 文本 + 服务端校验反馈(alerts.save/test 构造期错直显)。 */
function AlertRuleForm({
  draft,
  categories,
  saving,
  testRunning,
  onChange,
  onCancel,
  onSubmit,
  onTest,
}: {
  draft: AlertFormDraft;
  categories: AlertCategoryOption[];
  saving: boolean;
  testRunning: boolean;
  onChange: (draft: AlertFormDraft) => void;
  onCancel: () => void;
  onSubmit: () => void;
  onTest: () => void;
}) {
  const inputClass = "h-8 w-full text-xs";
  return (
    <form
      className="flex flex-col gap-2 rounded-md border border-border/60 bg-muted/30 p-3"
      data-testid="alert-rule-form"
      onSubmit={(event) => {
        event.preventDefault();
        onSubmit();
      }}
    >
      <p className="text-xs font-medium text-foreground">
        {draft.id !== undefined ? `编辑规则(id=${draft.id})` : "新建规则"}
      </p>
      <div className="grid grid-cols-2 gap-2">
        <label className="flex flex-col gap-1 text-xs">
          名称
          <Input
            aria-label="规则名称"
            className={inputClass}
            value={draft.name}
            onChange={(event) => onChange({ ...draft, name: event.target.value })}
          />
        </label>
        <label className="flex flex-col gap-1 text-xs">
          作用域
          {/* 原生 select 带 data-slot=select-trigger 样式钩子:与 Radix
              SelectTrigger 同享基调层微填充/低可见描边,暗色族感一致 */}
          <select
            aria-label="规则作用域"
            data-slot="select-trigger"
            className={cn("cursor-pointer px-2.5", inputClass)}
            value={draft.scope}
            onChange={(event) => onChange({ ...draft, scope: event.target.value })}
          >
            <option value="global">全局(所有品类)</option>
            {categories.map((option) => (
              <option key={option.category_id} value={option.category_id}>
                {option.category_name ? `${option.category_name}(${option.category_id})` : option.category_id}
              </option>
            ))}
          </select>
        </label>
      </div>
      <label className="flex flex-col gap-1 text-xs">
        when 表达式(白名单 AST;可用字段 title/content/source/url/category/score/tags 等,如
        <code className="font-mono"> &apos;融资&apos; in title or score &gt;= 4</code>)
        <textarea
          aria-label="when 表达式"
          rows={2}
          className="w-full rounded-md border border-(--control-border) bg-(--control-bg) px-2 py-1 font-mono text-xs outline-none transition-[color,border-color,box-shadow] duration-(--duration-fast) ease-out-expo placeholder:text-muted-foreground/70 focus-visible:ring-[3px] focus-visible:ring-ring/40"
          value={draft.when}
          onChange={(event) => onChange({ ...draft, when: event.target.value })}
        />
      </label>
      <div className="flex items-center gap-4 text-xs">
        动作
        <label className="flex items-center gap-1">
          <input
            type="radio"
            name="alert-action"
            className="accent-primary"
            checked={draft.action === "push"}
            onChange={() => onChange({ ...draft, action: "push" })}
          />
          推送
        </label>
        <label className="flex items-center gap-1">
          <input
            type="radio"
            name="alert-action"
            className="accent-primary"
            checked={draft.action === "tag"}
            onChange={() => onChange({ ...draft, action: "tag" })}
          />
          打标
        </label>
      </div>
      {draft.action === "push" ? (
        <>
          <label className="flex flex-col gap-1 text-xs">
            通道(channel)
            <select
              aria-label="推送通道"
              data-slot="select-trigger"
              className={cn("cursor-pointer px-2.5", inputClass)}
              value={draft.channel}
              onChange={(event) => onChange({ ...draft, channel: event.target.value })}
            >
              <option value="">选择通道…</option>
              {ALERT_CHANNELS.map((channel) => (
                <option key={channel} value={channel}>
                  {channel}
                </option>
              ))}
            </select>
          </label>
          <p className="text-2xs text-muted-foreground">
            执行时取该品类 push[] 第一个此类型通道;未配置则降级不发(命中照记,状态 degraded_no_channel)。
          </p>
          <label className="flex flex-col gap-1 text-xs">
            推送对象(可选,逗号分隔;缺省走通道默认)
            <Input
              aria-label="推送对象"
              className={inputClass}
              value={draft.targets}
              onChange={(event) => onChange({ ...draft, targets: event.target.value })}
            />
          </label>
          <label className="flex flex-col gap-1 text-xs">
            消息模板(可选)
            <Input
              aria-label="消息模板"
              className={inputClass}
              value={draft.template}
              onChange={(event) => onChange({ ...draft, template: event.target.value })}
            />
          </label>
        </>
      ) : (
        <label className="flex flex-col gap-1 text-xs">
          标签(逗号分隔,至少一个)
          <Input
            aria-label="标签列表"
            className={inputClass}
            value={draft.tags}
            onChange={(event) => onChange({ ...draft, tags: event.target.value })}
          />
        </label>
      )}
      <div className="flex items-center gap-2">
        <Button size="sm" type="submit" disabled={saving}>
          {saving ? "保存中…" : "保存规则"}
        </Button>
        <Button size="sm" variant="outline" type="button" disabled={testRunning} onClick={onTest}>
          {testRunning ? "求值中…" : "测试(dry)"}
        </Button>
        <Button size="sm" variant="ghost" type="button" onClick={onCancel}>
          取消
        </Button>
      </div>
    </form>
  );
}

/** 测试结果面板(design §9):matched / muted / actions 展开 / already_fired / 错误直显。 */
function AlertTestResultPanel({ state }: { state: AlertTestPanelState }) {
  return (
    <div
      className="flex flex-col gap-1 rounded-md border border-border/60 bg-muted/30 px-3 py-2 text-xs"
      data-testid="alert-test-result"
    >
      <p className="font-medium text-foreground">
        测试结果{state.key === "draft" ? "(草稿,dry 求值,不真发不落 fired)" : "(dry 求值,取最近一条条目)"}
      </p>
      {state.running ? <p className="text-muted-foreground">求值中…</p> : null}
      {!state.running && state.error ? (
        <p className="text-destructive">
          测试失败:{state.error.message}(code={state.error.code})
        </p>
      ) : null}
      {!state.running && state.result ? (
        <>
          <p className={state.result.matched ? "text-ok" : "text-muted-foreground"}>
            {state.result.matched ? "✓ 命中" : "✗ 未命中"}
          </p>
          {state.result.muted ? (
            <p className="text-warning">该条目被 mute 词表压制(跳过全部规则求值,不触发)。</p>
          ) : null}
          {state.result.eval_error ? (
            <p className="text-destructive">when 求值错:{state.result.eval_error}</p>
          ) : null}
          {state.result.already_fired ? (
            <p className="text-muted-foreground">该条目此规则已触发过(占坑去重,不会再发)。</p>
          ) : null}
          {state.result.actions.map((action, index) => (
            <p key={index} className="font-mono text-2xs text-muted-foreground">
              {action.action === "push"
                ? `推送 → ${action.channel ?? "?"}${
                    action.resolved
                      ? `(解析:${action.resolved_target ?? "?"})`
                      : "(该品类 push[] 无此类型通道,降级不发)"
                  }${action.degrade_reason ? `:${action.degrade_reason}` : ""}${
                    action.targets && action.targets.length > 0 ? ` 对象 ${action.targets.join(", ")}` : ""
                  }${action.template ? ` 模板「${action.template}」` : ""}`
                : `打标:${(action.tags ?? []).join(", ")}`}
            </p>
          ))}
          {!state.result.matched && state.result.actions.length === 0 && !state.result.eval_error ? (
            <p className="text-muted-foreground">无动作展开(未命中)。</p>
          ) : null}
        </>
      ) : null}
    </div>
  );
}
