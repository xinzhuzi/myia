/**
 * 微信群信息 IPC 封装(10-13-wechat-groupinfo R2;消费方 = 三级监控台
 * 「群信息」面板 wx-groupinfo-panel.tsx)。invoke 直连壳侧 Tauri 命令
 * `wechat_group_info {chat}`(壳 spawn 安装态桥执行 `localdb group-info
 * <chat> --json`,判例同 wechat_key_status 的 `localdb key-status --json`
 * 直转,wechat_keyprovider.rs:1077-1110);错误归一化走
 * screens/settings/api 的 asSidecarError(惯例同 wechat-keyprovider-api.ts,
 * 复用既有实现零新造)。
 *
 * 寻址(10-13 实锚勘误):桥 `localdb group-info` 按 `chat_room.username`
 * **精确等值**匹配(localdb_query.py `_chat_room_row` `WHERE username = ?`),
 * 与 `localdb query` 同族 —— 桥自身**不做**显示名解析;引擎侧对 query 的
 * 兼容是 MYIA 调用方拿应答 sessions 列表按名解析再查(sessions-name
 * resolution,src/myssia/engines/wechat_local.py「localdb chat 寻址」节)。
 * 三级监控台群行手里只有源名(源名全称律 `weixin-<会话名>`),前端零进程
 * 面拿不到 sessions 列表 —— 故**名→id 解析钉在壳侧命令内**:壳先 spawn 桥
 * `sessions list --json` 按名精确解析(同名不多见;不在列表如实空结构,
 * 与引擎「不在前 20 = 解析不到不猜」同律),命中才 spawn `localdb
 * group-info <id> --json`;寻址键本身已是 `xxx@chatroom` 形态则直查免解析。
 * 壳侧实现本契约时以此段为规格。
 *
 * 契约(任务档 prd.md「group-info 应答契约 v1」钉死,逐字段照抄零自造;
 * 缺表/缺行 = 对应键 null 或空表,桥恒 exit 0 如实降级):
 *
 *     {"group_info": {
 *       "chat_id": "50438708676@chatroom",
 *       "display_name": "TMS 中转站交流1️⃣",
 *       "member_count": 97,
 *       "owner": {"username": "wxid_x", "display": "名字"},
 *       "announcement": {"text": "…", "editor_display": "名字", "published_at": "2026-…"},
 *       "status": null,
 *       "members": [{"username": "wxid_a", "display": "花开相随", "remark": "备注", "is_owner": false}]
 *     }}
 *
 * 与壳侧成对(判例 wechat-keyprovider-api.ts KEY_ACQUIRE_EVENT_NAME 头注):
 * 命令名 `wechat_group_info`、参数键 `chat`、应答 = 桥 `group_info` 内层
 * 对象直转 —— 壳侧并行实现,本文件按 prd 契约先行,零运行时依赖;改任一
 * 侧须两侧同步。
 */
import { invoke } from "@tauri-apps/api/core";

import { channelDisplayName } from "./api";
import { asSidecarError } from "@/screens/settings/api";

/** 群主(owner 键;缺行 = null,不拦面板其余区) */
export interface WechatGroupOwner {
  username: string;
  /** 显示名(contact 域解析不出 = null,面板如实显「—」) */
  display: string | null;
}

/** 群公告(announcement 键;chat_room_info_detail 缺行 = null) */
export interface WechatGroupAnnouncement {
  text: string | null;
  editor_display: string | null;
  published_at: string | null;
}

/** 群成员行(members 表行;contact 域解析不出的字段如实 null) */
export interface WechatGroupMember {
  username: string;
  /** 显示名(名为主;null 面板回落备注/—,不猜) */
  display: string | null;
  /** 备注名(contact.remark;无 = null) */
  remark: string | null;
  /** 是否群主(chat_room.owner 对拍;缺键 = false) */
  is_owner: boolean;
}

/** `wechat_group_info` 应答(= 桥 `group_info` 对象;wire snake_case) */
export interface WechatGroupInfo {
  /** 会话 id(寻址键解析后的库内实锚;面板只作 title 悬浮,不上屏词面) */
  chat_id: string;
  /** 群显示名(lookup_contact;解析不出 = null,面板回落行名) */
  display_name: string | null;
  /** 成员数(chatroom_member 缺表 = null,面板如实「成员数未知」) */
  member_count: number | null;
  owner: WechatGroupOwner | null;
  announcement: WechatGroupAnnouncement | null;
  /** 群状态原值(chat_room_status_;v1 零上屏零词表,原样透传不拦面板) */
  status: unknown;
  /** 成员清单(缺表 = 空表) */
  members: WechatGroupMember[];
}

/**
 * wire 载荷 → WechatGroupInfo(TS 侧守门,惯例同 parseWechatKeyStatus):
 * 核心判别字段严校 —— chat_id 非字符串 / owner 在场但 username 非字符串 /
 * members 非数组即抛(壳侧 serde 已钉死,出现即对齐破了,大声失败);
 * 展示字段一律宽容 string|null(缺键 = null,不拦面板渲染);members 内
 * 单行残缺(非对象/无 username)丢弃不抛(判例
 * parseKeyProviderInstallInfo 的 files filter 同门:单项漂移不拦整体)。
 */
export function parseWechatGroupInfo(raw: unknown): WechatGroupInfo {
  if (typeof raw !== "object" || raw === null) {
    throw new TypeError(`群信息载荷不是对象: ${String(raw)}`);
  }
  const record = raw as Record<string, unknown>;
  if (typeof record.chat_id !== "string" || record.chat_id === "") {
    throw new TypeError(`群信息 chat_id 非字符串: ${String(record.chat_id)}`);
  }
  const owner = parseOwner(record.owner);
  const announcement = parseAnnouncement(record.announcement);
  const members = parseMembers(record.members);
  return {
    chat_id: record.chat_id,
    display_name: typeof record.display_name === "string" ? record.display_name : null,
    member_count:
      typeof record.member_count === "number" ? record.member_count : null,
    owner,
    announcement,
    status: record.status,
    members,
  };
}

/** owner 键守门:null 宽容;在场则 username 严校(群主对拍的锚字段)。 */
function parseOwner(raw: unknown): WechatGroupOwner | null {
  if (raw === null || raw === undefined) return null;
  if (typeof raw !== "object") {
    throw new TypeError(`群信息 owner 非对象: ${String(raw)}`);
  }
  const record = raw as Record<string, unknown>;
  if (typeof record.username !== "string" || record.username === "") {
    throw new TypeError(`群信息 owner.username 非字符串: ${String(record.username)}`);
  }
  return {
    username: record.username,
    display: typeof record.display === "string" ? record.display : null,
  };
}

/** announcement 键守门:null 宽容;三展示键全宽容 string|null。 */
function parseAnnouncement(raw: unknown): WechatGroupAnnouncement | null {
  if (raw === null || raw === undefined) return null;
  if (typeof raw !== "object") {
    throw new TypeError(`群信息 announcement 非对象: ${String(raw)}`);
  }
  const record = raw as Record<string, unknown>;
  return {
    text: typeof record.text === "string" ? record.text : null,
    editor_display: typeof record.editor_display === "string" ? record.editor_display : null,
    published_at: typeof record.published_at === "string" ? record.published_at : null,
  };
}

/** members 键守门:键缺席/非数组 = 形状漂移抛(契约恒空表也不缺键);
 *  行内残缺丢弃不抛(单行漂移不拦整表,判例见主函数头注)。 */
function parseMembers(raw: unknown): WechatGroupMember[] {
  if (!Array.isArray(raw)) {
    throw new TypeError(`群信息 members 非数组: ${String(raw)}`);
  }
  const members: WechatGroupMember[] = [];
  for (const entry of raw) {
    if (typeof entry !== "object" || entry === null) continue;
    const record = entry as Record<string, unknown>;
    if (typeof record.username !== "string" || record.username === "") continue;
    members.push({
      username: record.username,
      display: typeof record.display === "string" ? record.display : null,
      remark: typeof record.remark === "string" ? record.remark : null,
      is_owner: record.is_owner === true,
    });
  }
  return members;
}

/**
 * 源名 → 群信息寻址键:剥 `weixin-` 前缀取会话名(channelDisplayName 同一
 * 词表,源名全称律 `weixin-<会话名>`)。值 = 会话显示名或会话 id(源声明
 * 直写 id 时剥前缀即 id 原样)—— 名→id 解析在壳侧命令内(模块头注「寻址」
 * 节:桥精确等值不解析,壳 spawn `sessions list` 按名解析后直查;解析不到
 * 如实空结构,不猜)。
 */
export function wxGroupInfoChatKey(source: string): string {
  return channelDisplayName(source);
}

/**
 * 读群信息(群信息面板的唯一数据源;桥恒 exit 0 的只读命令,缺库缺表 =
 * 对应键 null/空表如实降级,三态皆正常态)。catch 后走 asSidecarError ——
 * 桥具名错误族(code/message/fix_hint)原样上屏,面板错误态给重试。
 */
export async function wechatGroupInfo(source: string): Promise<WechatGroupInfo> {
  try {
    return parseWechatGroupInfo(await invoke("wechat_group_info", { chat: wxGroupInfoChatKey(source) }));
  } catch (raw) {
    throw asSidecarError(raw);
  }
}
