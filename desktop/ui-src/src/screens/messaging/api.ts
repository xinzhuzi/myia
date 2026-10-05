/**
 * 消息屏数据装配(本屏私有 api 模块;共享客户端 @/lib/api 只读不动)。
 *
 * 数据面 = sidecar 协议消息方法族(task 10-03-messaging-ui;契约权威:任务档
 * design.md §D2 + entry.py `_m_channels_*` / `_m_push_write`,双侧同步):
 *
 *   channels.list    {} → {data_root, updated_at, platforms, aliases, dead, rules}
 *                      目录(platforms,条目名已套别名)+ 别名原始覆盖层(aliases)
 *                      + 死信键(dead,`platform:chat_id`)+ 推送规则视图(rules,
 *                      品类 YAML 的 push 条目;下区规则面板数据源)
 *   channels.refresh {platform} → {platform, merged, entries}
 *                      单平台目录发现→桶替换;unknown_platform /
 *                      discover_not_supported(telegram 被动积累)/
 *                      channel_refresh_failed(凭据/网络)结构化上抛
 *   channels.alias   {platform, chat_id, name} / {name: null} → set / delete
 *   push.write       {file, push} → {file, written, changed, backed_up?, push}
 *                      **push = 该文件完整 push 数组**(全量替换;空数组=摘除
 *                      push 节);服务端文本手术保注释,校验失败零写入
 *   bridge.status    {} → {available, reason, fix_hint, bin_found,
 *                      weixin_configured, gateway_alive, bin_path}
 *                      微信桥接探测(probe_bridge 全量;纯文件存在性检查,
 *                      零读取零出网;10-03-messaging-weixin-bridge D4,协议 v4 #31)
 *   alerts.list      {} → {rules: [AlertRuleView]}
 *                      告警规则全量(10-04-alert-rules;View = 规则全字段 +
 *                      fired_count/last_fired_at 派生;空表 = 合法零惊扰态)
 *   alerts.save      {rules: [AlertRuleInput]} → {ok, rules: [AlertRuleView]}
 *                      **rules = 完整规则数组**(全量替换承建/改/启停;带 id
 *                      = 更新保 id,不带 = 新建,库中多余 id 删;构造期拒 =
 *                      alert_rule_invalid 整批零写入)
 *   alerts.delete    {id} → {ok}(fired 命中历史照留)
 *   alerts.test      {rule? | rule_id?, item? | item_id?} → {matched, muted,
 *                      actions, eval_error?, already_fired?}(dry 求值不真发;
 *                      真发测试借既有 push.test;事件 alerts.fired 见 types.ts)
 *
 * 惯例与 sources 屏一致:invoke 直连壳命令 `sidecar_request` +
 * asSidecarError 归一化(错误必得 code/path/message)。
 */
import { invoke } from "@tauri-apps/api/core";

import { api, SidecarRequestError } from "@/lib/api";
import type { SidecarErrorShape } from "@/lib/api";

// ---------------------------------------------------------------------------
// 错误归一化(与 sources 屏同规则;独立实现避免动共享层)
// ---------------------------------------------------------------------------

/** 任意抛出物 → SidecarRequestError(组件渲染 code/path/message 用)。 */
export function asSidecarError(raw: unknown): SidecarRequestError {
  if (raw instanceof SidecarRequestError) return raw;
  if (typeof raw === "string") {
    try {
      const parsed = JSON.parse(raw) as Partial<SidecarErrorShape>;
      if (parsed && typeof parsed.code === "string" && typeof parsed.message === "string") {
        return new SidecarRequestError({
          code: parsed.code,
          path: typeof parsed.path === "string" ? parsed.path : "$",
          message: parsed.message,
          data: parsed.data,
        });
      }
    } catch {
      // 非 JSON 文本:按裸消息包装
    }
    return new SidecarRequestError({ code: "transport_error", path: "$", message: raw });
  }
  return new SidecarRequestError({
    code: "sidecar_unavailable",
    path: "$",
    message: raw instanceof Error ? `Tauri IPC 不可用: ${raw.message}` : `Tauri IPC 不可用: ${String(raw)}`,
  });
}

// ---------------------------------------------------------------------------
// 协议类型(形状逐字段对照 desktop/entry.py 应答载荷)
// ---------------------------------------------------------------------------

/** 通道目录条目(directory.ChannelEntry.to_dict;name 已套别名覆盖)。 */
export interface ChannelEntry {
  platform: string;
  chat_id: string;
  name: string;
  type: string;
  thread_id: string | null;
  last_seen: number | null;
}

/** 别名原始覆盖层(手工可编文件 channel_aliases.json 的持久形态)。 */
export type AliasMap = Record<string, Record<string, string>>;

/**
 * 一条 push 条目的摘要 + 写回 base(rules 视图)。
 *
 * `platform=null` 表示该通道不支持目录寻址(webhook/stdout),UI 不给
 * targets 选择器;`raw` 是条目的最小无损形态 —— push.write 全量替换的
 * 写回 base(UI 改 targets 后 `{...raw, targets}` 整文件提交,None 字段
 * 与 webhook 专属传输字段已剔除,保证回传过服务端同门校验)。
 */
export interface PushRuleEntry {
  index: number;
  channel: string;
  platform: string | null;
  targets: string[];
  has_template: boolean;
  route_count: number;
  raw: Record<string, unknown>;
}

/** 一个品类 YAML 的 push 规则组(坏文件 parse_ok=false + error 如实入列)。 */
export interface PushRuleFile {
  file: string;
  category_id: string | null;
  category_name: string | null;
  parse_ok: boolean;
  error: { path: string; code: string; message: string } | null;
  entries: PushRuleEntry[];
}

/** channels.list 应答(目录+别名+死信+规则四视图)。 */
export interface ChannelsView {
  data_root: string;
  updated_at: string | null;
  platforms: Record<string, ChannelEntry[]>;
  aliases: AliasMap;
  dead: string[];
  rules: PushRuleFile[];
}

/** channels.refresh 应答。 */
export interface RefreshResult {
  platform: string;
  merged: number;
  entries: ChannelEntry[];
}

/** channels.alias 应答。 */
export interface AliasResult {
  platform: string;
  chat_id: string;
  deleted: boolean;
  name: string | null;
}

/** push.write 应答;push = 写回后该文件实际生效的 push 数组。 */
export interface PushWriteResult {
  file: string;
  written: true;
  changed: boolean;
  backed_up?: string | null;
  push: unknown[];
}

/** bridge.status 应答(微信桥接探测;形状逐字段对照 desktop/entry.py
 * `_m_bridge_status` → myssia.push.weixin.probe_bridge 的 BridgeStatus)。 */
export interface BridgeStatusView {
  available: boolean;
  reason: string | null;
  fix_hint: string | null;
  bin_found: boolean;
  weixin_configured: boolean;
  gateway_alive: boolean;
  bin_path: string;
}

// ---------------------------------------------------------------------------
// 协议方法封装(走壳命令 sidecar_request;方法名与 entry.py 双侧同步)
// ---------------------------------------------------------------------------

/** 目录四视图(零平台 = 合法空态,UI 给「先配平台凭据」指引)。 */
export async function channelsList(): Promise<ChannelsView> {
  try {
    return await invoke<ChannelsView>("sidecar_request", { method: "channels.list", params: {} });
  } catch (raw) {
    throw asSidecarError(raw);
  }
}

/** 单平台目录发现(转圈态由调用方管理;失败结构化错误如实展示)。 */
export async function channelsRefresh(platform: string): Promise<RefreshResult> {
  try {
    return await invoke<RefreshResult>("sidecar_request", {
      method: "channels.refresh",
      params: { platform },
    });
  } catch (raw) {
    throw asSidecarError(raw);
  }
}

/** 别名设置(写 channel_aliases.json;立即生效,目录重建后仍生效)。 */
export async function channelsAliasSet(
  platform: string,
  chat_id: string,
  name: string,
): Promise<AliasResult> {
  try {
    return await invoke<AliasResult>("sidecar_request", {
      method: "channels.alias",
      params: { platform, chat_id, name },
    });
  } catch (raw) {
    throw asSidecarError(raw);
  }
}

/** 别名删除(条目名回退发现名;占位别名条目随之消失)。 */
export async function channelsAliasDelete(platform: string, chat_id: string): Promise<AliasResult> {
  try {
    return await invoke<AliasResult>("sidecar_request", {
      method: "channels.alias",
      params: { platform, chat_id, name: null },
    });
  } catch (raw) {
    throw asSidecarError(raw);
  }
}

/**
 * push[] 全量替换写回(design.md D2 定案:完整写回而非增量 patch)。
 *
 * push 必须是该文件**完整** push 数组 —— UI 侧「编辑一条提交整个数组」;
 * 同平台约束等校验在服务端 load_category 同门把关,失败零写入
 * (结构化错误原样带回,界面不假装成功)。
 */
export async function pushWrite(file: string, push: unknown[]): Promise<PushWriteResult> {
  try {
    return await invoke<PushWriteResult>("sidecar_request", {
      method: "push.write",
      params: { file, push },
    });
  } catch (raw) {
    throw asSidecarError(raw);
  }
}

/**
 * 微信桥接探测(10-03-messaging-weixin-bridge D4;屏私有封装,invoke 直连
 * 不入共享门面——sidecar-protocol.md 变更纪律 3)。
 *
 * 纯展示信号:调用方对失败降级为 null(平台卡按灰态「需本机 Hermes」
 * 呈现,不挡整屏目录视图;发送期的结构化 `bridge_unavailable` 是通道层事)。
 */
export async function bridgeStatus(): Promise<BridgeStatusView> {
  try {
    return await invoke<BridgeStatusView>("sidecar_request", { method: "bridge.status", params: {} });
  } catch (raw) {
    throw asSidecarError(raw);
  }
}

// ---------------------------------------------------------------------------
// 告警规则方法族(task 10-04-alert-rules;契约权威 = 任务档 design.md §4
// —— alerts.list/save/delete/test 四方法 + alerts.fired 事件。协议实现
// 落地前按本契约编码,侧未实装时 method_not_found 由调用方降级呈现)
// ---------------------------------------------------------------------------

/** 动作二选一(v1;每规则单动作,存储/协议同形)。 */
export type AlertAction = "push" | "tag";

/** push:channel 必填 + 可选 targets/template;tag:tags 非空(design §5.1)。 */
export interface AlertActionConfig {
  channel?: string;
  targets?: string[];
  template?: string;
  tags?: string[];
}

/**
 * alerts.list 应答的规则视图 = 规则全字段 + 两个派生列(design §4.1):
 * fired_count(alert_fired GROUP BY COUNT 派生,删规则不清零——历史是事实)、
 * last_fired_at(无命中 null)。协议字段名 `when` 与 RouteRuleConfig.when
 * 对齐(store 层 when_expr 列互转,design §2.3)。
 *
 * kind(10-05-cron-heartbeat):'item' = 条目条件规则(when 表达式求值于
 * 条目);'cron_stale' = 心跳规则(品类久未成功触发,when 恒占位 "true",
 * 阈值在 params)。旧 sidecar 应答无 kind 字段 → 视图层按 'item' 容缺省
 * (加法可选字段,旧壳新 UI 双向不炸)。
 */
export type AlertRuleKind = "item" | "cron_stale";

/** cron_stale 专属参数:显式 threshold_hours 或 auto 二选一(服务端同门校验)。 */
export interface AlertHeartbeatParams {
  threshold_hours?: number;
  auto?: boolean;
  job_id?: string;
}

export interface AlertRuleView {
  id: number;
  name: string;
  enabled: boolean;
  /** 'global' | 品类 id(七品类之一;cron_stale 必须品类) */
  scope: string;
  when: string;
  action: AlertAction;
  action_config: AlertActionConfig;
  kind?: AlertRuleKind;
  params?: AlertHeartbeatParams | null;
  created_at: string;
  updated_at: string;
  fired_count: number;
  last_fired_at: string | null;
}

/**
 * alerts.save 载荷的规则输入:视图减派生列;id 缺省 = 新建,带 id = 更新
 * 保 id(全量替换的 diff 语义:库中多余 id 由服务端删除,design §4.1)。
 */
export type AlertRuleInput = Omit<
  AlertRuleView,
  "fired_count" | "last_fired_at" | "created_at" | "updated_at" | "id"
> & {
  id?: number;
};

/** alerts.list 应答。 */
export interface AlertsListView {
  rules: AlertRuleView[];
}

/** alerts.save 应答(写回后全量规则视图,id 稳定 = 计数派生前提)。 */
export interface AlertsSaveResult {
  ok: true;
  rules: AlertRuleView[];
}

/**
 * alerts.test 应答(dry 求值,不真发不落 fired,design §4.1 钉死②):
 * actions = 将触发的动作展开 —— push 携通道解析结果 + 降级原因,
 * tag 携 tags;eval_error = 坏 when 的求值错文本;muted = mute 压制;
 * already_fired 仅 rule_id 形态有值(草稿无从查历史)。
 * 字段名与协议实发对齐(entry.py _alert_test_actions):
 * resolved(bool) / resolved_target(解析描述) / degrade_reason(降级原因)。
 */
export interface AlertTestResult {
  matched: boolean;
  muted: boolean;
  actions: Array<{
    action: AlertAction;
    /** push:通道名;tag 无 */
    channel?: string;
    targets?: string[] | null;
    template?: string | null;
    /** push:该品类 push[] 是否解析到同类型通道(false = 降级不发) */
    resolved?: boolean;
    /** push:解析到的通道描述(该品类 push[] 第一条同类型通道的 target) */
    resolved_target?: string | null;
    /** push:未解析到时的降级原因(category_push_missing/item_no_category/category_yaml_not_found) */
    degrade_reason?: string | null;
    /** tag:将打的标签 */
    tags?: string[];
  }>;
  eval_error?: string;
  already_fired?: boolean;
}

/** alerts.test 载荷:rule(草稿,未保存即可测)与 rule_id 二选一;item/item_id 缺省取最近一条。 */
export interface AlertsTestParams {
  rule?: AlertRuleInput;
  rule_id?: number;
  item?: Record<string, unknown>;
  item_id?: number;
}

/** 规则全量拉齐(空表 = 合法零惊扰态)。 */
export async function alertsList(): Promise<AlertsListView> {
  try {
    return await invoke<AlertsListView>("sidecar_request", { method: "alerts.list", params: {} });
  } catch (raw) {
    throw asSidecarError(raw);
  }
}

/**
 * 规则全量替换写回(design §4.1 钉死①:承建/改/启停,不设独立启停方法;
 * push.write 全量先例「编辑一条提交整个数组」)。启停 = 整数组提交时该行
 * enabled 翻转;构造期拒 = alert_rule_invalid 整批零写入(结构化错直显)。
 */
export async function alertsSave(rules: AlertRuleInput[]): Promise<AlertsSaveResult> {
  try {
    return await invoke<AlertsSaveResult>("sidecar_request", { method: "alerts.save", params: { rules } });
  } catch (raw) {
    throw asSidecarError(raw);
  }
}

/** 删规则定义行(fired 命中历史照留;未知 id → alert_not_found)。 */
export async function alertsDelete(id: number): Promise<{ ok: true }> {
  try {
    return await invoke<{ ok: true }>("sidecar_request", { method: "alerts.delete", params: { id } });
  } catch (raw) {
    throw asSidecarError(raw);
  }
}

/** dry 求值测试(不真发不落 fired;真发测试借既有 push.test)。 */
export async function alertsTest(params: AlertsTestParams): Promise<AlertTestResult> {
  try {
    return await invoke<AlertTestResult>("sidecar_request", { method: "alerts.test", params });
  } catch (raw) {
    throw asSidecarError(raw);
  }
}

// ---------------------------------------------------------------------------
// 告警表单辅助(纯函数:下拉选项 / 逗号分隔解析)
// ---------------------------------------------------------------------------

/**
 * push 动作 channel 下拉名集 = `myssia.push.CHANNELS` 键集镜像(30 条:
 * 8 核心 + W3 长尾 22;同步源 src/myssia/push/__init__.py:181-191)。
 * UI 只做名集提示,凭据解析在执行期(品类 push[] 第一个此类型通道,
 * 未配置则降级不发 —— design §7.1)。
 */
export const ALERT_CHANNELS: string[] = [
  "feishu_card",
  "telegram",
  "ntfy",
  "dingtalk",
  "wecom",
  "weixin",
  "webhook",
  "stdout",
  "slack",
  "discord",
  "whatsapp_cloud",
  "line",
  "qqbot",
  "google_chat",
  "teams",
  "msgraph_webhook",
  "matrix",
  "mattermost",
  "irc",
  "simplex",
  "signal",
  "bluebubbles",
  "email",
  "sms",
  "homeassistant",
  "a2a",
  "yuanbao",
  "buzz",
  "photon",
  "raft",
];

/** scope 下拉的品类选项(yaml.list 的 parse_ok 且有 category_id 项)。 */
export interface AlertCategoryOption {
  category_id: string;
  category_name: string | null;
}

/**
 * 品类下拉选项 = yaml.list 派生(design §9:scope 全局/品类下拉=yaml.list;
 * 形状对照 entry.py `_m_yaml_list`,坏文件不入选项)。失败由调用方降级为
 * 空名单(下拉只留「全局」,不挡子面板)。
 */
export async function listAlertCategories(): Promise<AlertCategoryOption[]> {
  interface YamlFileEntry {
    parse_ok: boolean;
    category_id: string | null;
    category_name: string | null;
  }
  const result = await invoke<{ plugins_dir: string; files: YamlFileEntry[] }>("sidecar_request", {
    method: "yaml.list",
    params: {},
  });
  return result.files
    .filter((file) => file.parse_ok && file.category_id !== null)
    .map((file) => ({ category_id: file.category_id as string, category_name: file.category_name }));
}

/** 逗号分隔输入 → 去空白的非空项列表(tags/targets 表单字段共用)。 */
export function parseCsvList(text: string): string[] {
  return text
    .split(",")
    .map((piece) => piece.trim())
    .filter((piece) => piece.length > 0);
}

// ---------------------------------------------------------------------------
// 视图装配纯函数(展示格式化,零协议往返)
// ---------------------------------------------------------------------------

/** last_seen(Unix 秒)→ 本地日期时间串;null → "—"(从未发现)。 */
export function formatLastSeen(lastSeen: number | null): string {
  if (lastSeen === null || lastSeen === undefined) return "—";
  const date = new Date(lastSeen * 1000);
  if (Number.isNaN(date.getTime())) return "—";
  return date.toLocaleString(undefined, {
    year: "numeric",
    month: "2-digit",
    day: "2-digit",
    hour: "2-digit",
    minute: "2-digit",
  });
}

/** ISO-8601 时间戳(alerts 域:规则 updated_at / fired 的 last_fired_at)→ 本地
 *  日期时间串;null → "—"(从未触发);解析失败原样返回(不吞数据)。 */
export function formatIsoTimestamp(iso: string | null): string {
  if (iso === null || iso === undefined || iso === "") return "—";
  const date = new Date(iso);
  if (Number.isNaN(date.getTime())) return iso;
  return date.toLocaleString(undefined, {
    year: "numeric",
    month: "2-digit",
    day: "2-digit",
    hour: "2-digit",
    minute: "2-digit",
  });
}

/** 目录条目 → targets spec(`platform:名称`;与 schema 契约同源)。 */
export function targetSpec(entry: ChannelEntry): string {
  return `${entry.platform}:${entry.name}`;
}

/** 该条目是否已标死信(dead 键 = `platform:chat_id`,小写平台前缀)。 */
export function isDeadEntry(entry: ChannelEntry, dead: string[]): boolean {
  return dead.includes(`${entry.platform}:${entry.chat_id}`);
}

/** 该条目名是否来自手工别名(区分「发现名/手工命名」)。 */
export function hasAlias(entry: ChannelEntry, aliases: AliasMap): boolean {
  return Boolean(aliases[entry.platform]?.[entry.chat_id]);
}

// ---------------------------------------------------------------------------
// 平台总览数据(task 10-03-messaging-platforms R3:凭据探测,零新协议方法)
// ---------------------------------------------------------------------------

/**
 * 钥匙链凭据名清单(既有 secret.list;平台卡「已连接/需要设置」派生的
 * 凭据信号)。只有名字,值永不可读;调用方对失败降级为空名单
 * (钥匙链不可用的主机上,平台状态回退到「目录非空」单一信号)。
 */
export async function listSecretNames(): Promise<string[]> {
  return (await api.secretList()).names;
}
