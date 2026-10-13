/**
 * 微信群信息导出 IPC 封装(10-13-wechat-groupinfo R3;消费方 = 群信息面板
 * 「导出」按钮 wx-groupinfo-panel.tsx)。invoke 直连壳侧 Tauri 命令
 * `wechat_group_export {chat_id, json_payload}`:前端**已持** group-info
 * 应答(./wechat-groupinfo-api 的 wechatGroupInfo() 产物),壳**不重查**
 * ——保存对话框(dialog 插件 Rust 侧 blocking_save_file,spawn_blocking
 * 线程,判例 wechat_key_status)→ 所选路径写 JSON(pretty,零改形)+
 * 同目录**同名**成员表 CSV(UTF-8 BOM 保 Excel 中文不乱码)。
 *
 * 应答三态(与壳侧成对,判例 wechat-groupinfo-api.ts 头注):
 * - `null` = 用户取消保存对话框 —— **静默语义**,面板态机回 idle 零提示;
 * - 对象 = `{json_path, csv_path, member_rows}`(两件落盘绝对路径 + 成员
 *   行数,wire snake_case 原样);
 * - throw = 失败(壳侧人话 message 经 asSidecarError 归一化,面板原样上屏)。
 * 命令名 `wechat_group_export`、参数键 `chat_id`/`json_payload`、应答 =
 * `Option<{json_path, csv_path, member_rows}>` —— 壳侧实现 =
 * wechat_group_export.rs;改任一侧须两侧同步。
 */
import { invoke } from "@tauri-apps/api/core";

import { asSidecarError } from "@/screens/settings/api";

/** `wechat_group_export` 成功应答(两件成套落盘回执) */
export interface WechatGroupExportResult {
  /** 群信息 JSON 落盘绝对路径(保存对话框所选) */
  json_path: string;
  /** 成员表 CSV 落盘绝对路径(同目录同名,.csv) */
  csv_path: string;
  /** 成员表数据行数(缺 members 键 = 0,如实) */
  member_rows: number;
}

/**
 * 成功应答守门(判例 parseWechatGroupInfo 的核心判别字段严校):两路径
 * 非空串 / 行数非负整数,漂移即抛(壳侧 serde 已钉死,出现即对齐破了,
 * 大声失败)。
 */
export function parseWechatGroupExportResult(raw: unknown): WechatGroupExportResult {
  if (typeof raw !== "object" || raw === null) {
    throw new TypeError(`导出回执不是对象: ${String(raw)}`);
  }
  const record = raw as Record<string, unknown>;
  if (typeof record.json_path !== "string" || record.json_path === "") {
    throw new TypeError(`导出回执 json_path 非字符串: ${String(record.json_path)}`);
  }
  if (typeof record.csv_path !== "string" || record.csv_path === "") {
    throw new TypeError(`导出回执 csv_path 非字符串: ${String(record.csv_path)}`);
  }
  if (
    typeof record.member_rows !== "number" ||
    !Number.isInteger(record.member_rows) ||
    record.member_rows < 0
  ) {
    throw new TypeError(`导出回执 member_rows 非非负整数: ${String(record.member_rows)}`);
  }
  return {
    json_path: record.json_path,
    csv_path: record.csv_path,
    member_rows: record.member_rows,
  };
}

/**
 * 导出群信息(面板导出按钮唯一通道):null = 用户取消保存对话框(静默
 * 返回,面板不提示);对象 = 两件落盘回执;throw = 失败(人话)。
 */
export async function wechatGroupExport(
  chatId: string,
  jsonPayload: unknown,
): Promise<WechatGroupExportResult | null> {
  try {
    const raw = await invoke("wechat_group_export", { chatId, jsonPayload });
    return raw === null ? null : parseWechatGroupExportResult(raw);
  } catch (raw) {
    throw asSidecarError(raw);
  }
}
