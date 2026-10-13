/**
 * 微信本机桥「取钥器」配置 IPC 封装(10-13-wechat-keyprovider B5;消费方 =
 * 「微信账号」卡取钥器配置行)。invoke 直连壳侧 Tauri 命令 `wechat_key_provider`
 * (壳 spawn 安装态桥可执行文件执行 `localdb key-provider set/get/clear`,
 * 配置落桥自有 `<数据根>/wechat-bridge/config.json` 经桥管理命令——前端与壳
 * 都不直写桥配置文件)。错误归一化走 ./api 的 asSidecarError(惯例同
 * platform-accounts-api.ts);桥具名错误族码名/人话/fix_hint 原样上屏。
 *
 * 契约(与 src-tauri/src/wechat_keyprovider.rs 对齐):
 * - `wechat_key_provider {action:"get"}` → `{configured, path, file_exists,
 *   file_executable}`(三态派生唯一真源;path 回存桥配置原字面,可为 null)
 * - `wechat_key_provider {action:"set", path}` → `{ok}`(桥侧校验文件存在
 *   +可执行后才落盘;成功后前端重拉 get 刷新)
 * - `wechat_key_provider {action:"clear"}` → `{ok}`
 * - 错误 = 信封 `{code, path, message[, data.fix_hint]}` JSON 字符串
 *
 * 10-13-wechat-monitor-ui A1 扩展(密钥状态面 + 获取密钥流;契约 = 任务档
 * design.md 契约规格册 §B.1/§B.2/§B.3/§D.1,逐字段照抄零自造):
 * - command `wechat_key_status` → `{state, db_count, acquired_at,
 *   wechat_version, verdict_note}`(§B.1 = 桥 `localdb key-status` 的
 *   key_status 对象直转,wire snake_case;三态 = ready|stale|missing)
 * - command `wechat_key_acquire {force?}`(异步命令,终态回包)→
 *   `{result: ok|failed|cancelled, db_count?, error?}`(§B.2;progress 不在
 *   回包,走下方事件)
 * - command `wechat_key_acquire_cancel`(§B.2 单飞锁无参 cancel)
 * - event `wechat-key-acquire`(§B.3;载荷 `{seq, phase, detail}`,seq 单调
 *   递增,前端丢弃乱序旧包;phase 词面只作机器枚举,上屏词走 §D.3 词表)
 */
import { invoke } from "@tauri-apps/api/core";
import { listen, type UnlistenFn } from "@tauri-apps/api/event";

import { asSidecarError } from "./api";

/** 取钥器配置态(wechat_key_provider get 应答;wire snake_case) */
export interface KeyProviderState {
  /** 桥 config.json 的 key_provider_path 非空 = true */
  configured: boolean;
  /** 已配置的取钥器路径原字面(未配置 = null) */
  path: string | null;
  /** 配置路径的文件存在性(壳侧如实重探;set 后文件可能被删) */
  file_exists: boolean;
  /** 配置路径的可执行性(unix 执行位;非 unix 家族 = 存在即 true) */
  file_executable: boolean;
}

/** 三态视图(设置页「已配置/未配置/文件缺失」的派生口径) */
export type KeyProviderView = "configured" | "unset" | "missing";

/** 配置态 → 三态视图:未配置优先;已配置但文件缺席/不可执行 = 文件缺失。 */
export function keyProviderView(state: KeyProviderState): KeyProviderView {
  if (!state.configured || !state.path) return "unset";
  return state.file_exists && state.file_executable ? "configured" : "missing";
}

/**
 * wire 载荷 → KeyProviderState(TS 侧守门,惯例同 parsePyenvStatus):
 * configured 非布尔即抛(壳侧 serde 已钉死,出现即对齐破了,大声失败);
 * path 宽容 string|null(缺键 = null);两文件键宽容布尔(缺键 = false,
 * 与「文件缺失」三态同形,不拦状态展示)。
 */
export function parseKeyProviderState(raw: unknown): KeyProviderState {
  if (typeof raw !== "object" || raw === null) {
    throw new TypeError(`取钥器配置态载荷不是对象: ${String(raw)}`);
  }
  const record = raw as Record<string, unknown>;
  if (typeof record.configured !== "boolean") {
    throw new TypeError(`取钥器配置态 configured 非布尔: ${String(record.configured)}`);
  }
  return {
    configured: record.configured,
    path: typeof record.path === "string" ? record.path : null,
    file_exists: record.file_exists === true,
    file_executable: record.file_executable === true,
  };
}

async function callKeyProvider(action: string, path?: string): Promise<unknown> {
  try {
    return await invoke("wechat_key_provider", path !== undefined ? { action, path } : { action });
  } catch (raw) {
    throw asSidecarError(raw);
  }
}

/** 读取钥器配置态(设置行初始/保存后刷新的真相源)。 */
export async function wechatKeyProviderGet(): Promise<KeyProviderState> {
  return parseKeyProviderState(await callKeyProvider("get"));
}

/** 保存取钥器路径(桥侧校验存在+可执行;绝对路径,~ 前缀可用)。 */
export async function wechatKeyProviderSet(path: string): Promise<{ ok: boolean }> {
  return (await callKeyProvider("set", path)) as { ok: boolean };
}

/** 清除取钥器配置(回到未配置态;解密时桥会明确报错,不静默降级)。 */
export async function wechatKeyProviderClear(): Promise<{ ok: boolean }> {
  return (await callKeyProvider("clear")) as { ok: boolean };
}

// ---------------------------------------------------------------------------
// 密钥状态 + 获取密钥流(10-13-wechat-monitor-ui A1;契约 = 任务档 design.md
// 契约规格册 §B.1/§B.2/§B.3/§D.1,消费方 = 「微信账号」卡密钥状态行 + 三步面板)
// ---------------------------------------------------------------------------

/**
 * 取钥进度事件名(§B.3;与壳侧 src-tauri/src/wechat_keyprovider.rs 的
 * KEY_ACQUIRE_EVENT 常量同值成对,改值须两侧同步——壳侧同事并行实现,
 * 本文件按契约规格册 §B.3 先行,零运行时依赖)。
 */
export const KEY_ACQUIRE_EVENT_NAME = "wechat-key-acquire";

/** 密钥三态(§B.1 = 桥 key-status 的 state;ready=在场+抽样过/stale=抽样
 *  验真失败(微信版本变化后失配)/missing=keys.json 缺位)。 */
const KEY_STATUS_STATES = ["ready", "stale", "missing"] as const;
export type KeyStatusState = (typeof KEY_STATUS_STATES)[number];

/** `wechat_key_status` 应答(§B.1;wire snake_case;钥内容永不出现——
 *  db_count/时间戳 = 形状级证据)。 */
export interface WechatKeyStatus {
  state: KeyStatusState;
  /** mapping 键数(missing = 0) */
  db_count: number;
  /** keys.json 文件 mtime ISO 本地时(missing = null) */
  acquired_at: string | null;
  wechat_version: string | null;
  /** 三态判据人话(如「抽样 3 库验真通过」/「抽样验真失败:N/M」) */
  verdict_note: string | null;
}

/**
 * wire 载荷 → WechatKeyStatus(TS 侧守门,严校模式照抄 parseKeyProviderState
 * 的 configured 布林严校:核心判别字段 state 非契约枚举即抛——壳侧 serde 已
 * 钉死,出现即对齐破了,大声失败;db_count 非数字同抛(§A.1 恒在场);
 * 其余三键宽容 string|null(缺键 = null,不拦状态展示)。
 */
export function parseWechatKeyStatus(raw: unknown): WechatKeyStatus {
  if (typeof raw !== "object" || raw === null) {
    throw new TypeError(`密钥状态载荷不是对象: ${String(raw)}`);
  }
  const record = raw as Record<string, unknown>;
  if (!KEY_STATUS_STATES.includes(record.state as KeyStatusState)) {
    throw new TypeError(`密钥状态 state 非契约值: ${String(record.state)}`);
  }
  if (typeof record.db_count !== "number") {
    throw new TypeError(`密钥状态 db_count 非数字: ${String(record.db_count)}`);
  }
  return {
    state: record.state as KeyStatusState,
    db_count: record.db_count,
    acquired_at: typeof record.acquired_at === "string" ? record.acquired_at : null,
    wechat_version: typeof record.wechat_version === "string" ? record.wechat_version : null,
    verdict_note: typeof record.verdict_note === "string" ? record.verdict_note : null,
  };
}

/** 查询密钥三态(密钥状态行的真相源;恒 exit 0 的只读命令,三态皆正常态)。 */
export async function wechatKeyStatus(): Promise<WechatKeyStatus> {
  try {
    return parseWechatKeyStatus(await invoke("wechat_key_status"));
  } catch (raw) {
    throw asSidecarError(raw);
  }
}

/** 事件/回包共用的取钥阶段枚举(§B.3 机器枚举;上屏词另走 §D.3 词表)。 */
const KEY_ACQUIRE_PHASES = [
  "password",
  "attach",
  "wait_relogin",
  "derive",
  "done",
  "failed",
  "cancelled",
] as const;
export type KeyAcquirePhase = (typeof KEY_ACQUIRE_PHASES)[number];

/** 步进条四阶段(§D.2;done/failed/cancelled = 结果页形态,不入步进条)。 */
export const KEY_ACQUIRE_STEP_PHASES = ["password", "attach", "wait_relogin", "derive"] as const;
export type KeyAcquireStepPhase = (typeof KEY_ACQUIRE_STEP_PHASES)[number];

/** 阶段词表(§D.3 phase→上屏,逐字段照规格册;协议行话不上屏,grill 决议⑦)。 */
export const KEY_ACQUIRE_PHASE_LABELS: Record<KeyAcquireStepPhase, string> = {
  password: "等待输入密码",
  attach: "正在连接微信",
  wait_relogin: "等待重新登录",
  derive: "正在验证数据库",
};

/** `wechat-key-acquire` 事件载荷(§B.3)。 */
export interface KeyAcquireEvent {
  /** 单调递增;前端丢弃乱序旧包 */
  seq: number;
  phase: KeyAcquirePhase;
  /** provider progress 的 message 原文(已是人话);可为 null */
  detail: string | null;
}

/**
 * wire 载荷 → KeyAcquireEvent(TS 侧守门,同 parseWechatKeyStatus 口径):
 * seq 非数字/phase 非契约枚举即抛(壳侧钉死,出现即对齐破了);detail 宽容
 * string|null。
 */
export function parseKeyAcquireEvent(raw: unknown): KeyAcquireEvent {
  if (typeof raw !== "object" || raw === null) {
    throw new TypeError(`取钥进度事件载荷不是对象: ${String(raw)}`);
  }
  const record = raw as Record<string, unknown>;
  if (typeof record.seq !== "number") {
    throw new TypeError(`取钥进度事件 seq 非数字: ${String(record.seq)}`);
  }
  if (!KEY_ACQUIRE_PHASES.includes(record.phase as KeyAcquirePhase)) {
    throw new TypeError(`取钥进度事件 phase 非契约值: ${String(record.phase)}`);
  }
  return {
    seq: record.seq,
    phase: record.phase as KeyAcquirePhase,
    detail: typeof record.detail === "string" ? record.detail : null,
  };
}

/** `wechat_key_acquire` 终态回包(§B.2;progress 走事件,回包只承载终态)。 */
export type KeyAcquireResult = "ok" | "failed" | "cancelled";

export interface KeyAcquireOutcome {
  result: KeyAcquireResult;
  db_count?: number;
  error?: string | null;
}

/**
 * wire 载荷 → KeyAcquireOutcome(TS 侧守门):result 非契约枚举即抛;
 * db_count/error 宽容(可选键,缺省不拦结果展示)。
 */
export function parseKeyAcquireOutcome(raw: unknown): KeyAcquireOutcome {
  if (typeof raw !== "object" || raw === null) {
    throw new TypeError(`取钥终态载荷不是对象: ${String(raw)}`);
  }
  const record = raw as Record<string, unknown>;
  if (!(["ok", "failed", "cancelled"] as const).includes(record.result as KeyAcquireResult)) {
    throw new TypeError(`取钥终态 result 非契约值: ${String(record.result)}`);
  }
  return {
    result: record.result as KeyAcquireResult,
    db_count: typeof record.db_count === "number" ? record.db_count : undefined,
    error: typeof record.error === "string" ? record.error : null,
  };
}

/**
 * 发起获取密钥(§B.2 异步命令):force = true 跳过桥侧缓存短路直走取钥器
 * (「重新获取」场景:钥匙失效但 keys.json 在场,不 force 永远空转——
 * grill 决议②);progress 经 KEY_ACQUIRE_EVENT_NAME 事件流到达,本回包 =
 * 终态。单飞锁:同会话只允许一个 acquire 在途,第二个报「已有获取在进行」。
 */
export async function startKeyAcquire(force: boolean): Promise<KeyAcquireOutcome> {
  try {
    return parseKeyAcquireOutcome(await invoke("wechat_key_acquire", { force }));
  } catch (raw) {
    throw asSidecarError(raw);
  }
}

/** 取消进行中的获取(§B.2 单飞锁无参 cancel:kill 用户态链 + 落哨兵文件,
 *  提权段由部署件轮询哨兵自理;终态经事件 `cancelled` 收口)。 */
export async function cancelKeyAcquire(): Promise<void> {
  try {
    await invoke("wechat_key_acquire_cancel");
  } catch (raw) {
    throw asSidecarError(raw);
  }
}

/**
 * 订阅 `wechat-key-acquire` 进度事件(载荷经 parseKeyAcquireEvent 守门;
 * listen + UnlistenFn 范本照 pyenv-api.ts 的 onPyenvStatusChanged)。
 * 载荷不合契约时不静默:交 onMalformed 上屏(默认忽略);seq 乱序旧包的
 * 丢弃由消费方按 seq 单调判据自理(§B.3)。
 */
export function subscribeKeyAcquire(
  onEvent: (event: KeyAcquireEvent) => void,
  onMalformed: (error: unknown) => void = () => undefined,
): Promise<UnlistenFn> {
  return listen<unknown>(KEY_ACQUIRE_EVENT_NAME, (event) => {
    try {
      onEvent(parseKeyAcquireEvent(event.payload));
    } catch (error) {
      onMalformed(error);
    }
  });
}

export type { UnlistenFn };

// ---------------------------------------------------------------------------
// 部署件一键安装(E2;契约 = 壳侧 wechat_key_provider_install {action:
// "inspect"|"install"},消费方 = 「微信账号」卡取钥器区的安装行)
// ---------------------------------------------------------------------------

/** `wechat_key_provider_install {action:"inspect"}` 应答(源在场/已安装探测)。 */
export interface KeyProviderInstallInfo {
  /** 束源在场(入口件 keyprovider-lldb.sh 在场 = true) */
  available: boolean;
  /** 命中的束源目录(available = false 时为 null) */
  source_dir: string | null;
  /** 落点入口件已在场(曾装过) */
  installed: boolean;
  /** 落点入口件绝对路径(未装 = null) */
  installed_path: string | null;
  /** 束源在场文件名清单(供 UI 如实披露) */
  files: string[];
  /** 束源在场但属主链校验未过被拒的人话原因(null = 无此形态;评审修③:
   *  多用户机器防他人预建束目录投放——前端如实披露拒因,不静默装作源不在) */
  source_unsafe_reason: string | null;
}

/**
 * wire 载荷 → KeyProviderInstallInfo(TS 侧守门,严校模式照抄
 * parseKeyProviderState 的核心布林严校:available 非布尔即抛;其余键宽容
 * string|null / 数组(缺省不拦状态展示)。
 */
export function parseKeyProviderInstallInfo(raw: unknown): KeyProviderInstallInfo {
  if (typeof raw !== "object" || raw === null) {
    throw new TypeError(`取钥器安装态载荷不是对象: ${String(raw)}`);
  }
  const record = raw as Record<string, unknown>;
  if (typeof record.available !== "boolean") {
    throw new TypeError(`取钥器安装态 available 非布尔: ${String(record.available)}`);
  }
  return {
    available: record.available,
    source_dir: typeof record.source_dir === "string" ? record.source_dir : null,
    installed: record.installed === true,
    installed_path: typeof record.installed_path === "string" ? record.installed_path : null,
    files: Array.isArray(record.files)
      ? record.files.filter((name): name is string => typeof name === "string")
      : [],
    source_unsafe_reason:
      typeof record.source_unsafe_reason === "string" ? record.source_unsafe_reason : null,
  };
}

async function callKeyProviderInstall(action: string): Promise<unknown> {
  try {
    return await invoke("wechat_key_provider_install", { action });
  } catch (raw) {
    throw asSidecarError(raw);
  }
}

/** 探测部署件束源与安装态(纯读;设置卡未配置态的安装行数据源)。 */
export async function wechatKeyProviderInspect(): Promise<KeyProviderInstallInfo> {
  return parseKeyProviderInstallInfo(await callKeyProviderInstall("inspect"));
}

/** `wechat_key_provider_install {action:"install"}` 应答。 */
export interface KeyProviderInstallOutcome {
  ok: boolean;
  /** 落点入口件绝对路径(随后自动经桥管理命令 set 保存) */
  installed_path: string;
  copied: string[];
}

/** 一键安装(cp 束件到数据根私有区 bin/ + 700;路径保存走 wechatKeyProviderSet)。 */
export async function wechatKeyProviderInstall(): Promise<KeyProviderInstallOutcome> {
  const raw = await callKeyProviderInstall("install");
  if (typeof raw !== "object" || raw === null) {
    throw new TypeError(`取钥器安装结果载荷不是对象: ${String(raw)}`);
  }
  const record = raw as Record<string, unknown>;
  const installedPath = record.installed_path;
  if (typeof installedPath !== "string") {
    throw new TypeError(`取钥器安装结果缺 installed_path: ${String(raw)}`);
  }
  return {
    ok: record.ok === true,
    installed_path: installedPath,
    copied: Array.isArray(record.copied)
      ? record.copied.filter((name): name is string => typeof name === "string")
      : [],
  };
}
