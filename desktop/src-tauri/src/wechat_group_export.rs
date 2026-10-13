//! 微信群信息导出(task 10-13-wechat-groupinfo R3)。
//!
//! 三级监控台「群信息」面板导出按钮的壳侧通道:前端**已持** group-info 应答
//! (wechat-groupinfo-api.ts `wechatGroupInfo()` 产物,契约 = 任务档 prd
//! 「group-info 应答契约 v1」),本命令吃 `{chat_id, json_payload}` 原样落盘,
//! **壳不重查**(零二次桥 spawn,数据只读纪律延续——本命令也不读任何微信库)。
//!
//! 两件成套(R3 钉死):
//! - JSON:系统保存对话框(dialog 插件 Rust 侧 `blocking_save_file`,缺省
//!   文件名 `群信息-<显示名>-<日期>.json`;插件注册先例 = 看图屏
//!   main.rs `tauri_plugin_dialog::init()`,capabilities `dialog:default`
//!   已含保存对话框)→ 所选路径写载荷全文(pretty + 尾换行,零改形);
//! - CSV:同目录**同名**成员表(`<所选项>.csv`,`with_extension` 推导),
//!   列 = 显示名/备注/wxid/是否群主,**UTF-8 BOM** 开头(Excel 直开中文
//!   不乱码),CRLF 行尾 + RFC 4180 引号转义 + 公式前缀(`=`+`-`@`tab)
//!   中和(成员昵称/备注攻击者可控,防表格软件直开按公式执行)。
//!
//! 取消 = 静默返回:用户关掉保存对话框(`blocking_save_file` → `None`)
//! 命令返回 `Ok(null)`,零写盘零提示;前端态机回 idle(成对实现 =
//! wechat-group-export-api.ts,注释互指)。
//!
//! 线程纪律:`blocking_save_file` 禁主线程(插件文档明示;插件内部自 hop
//! main thread 弹窗,desktop.rs save_file),故走
//! `tauri::async_runtime::spawn_blocking`——判例 wechat_key_status 的
//! spawn_blocking 同款(wechat_keyprovider.rs:1085)。
//!
//! 错误信封沿仓惯例 `{"code","path","message"}` JSON 字符串(前端
//! asSidecarError 同形解析);message 一律人话(「写入失败(路径): 原因」)。
//!
//! 红线:对微信数据零读(载荷由前端供给);密钥零沾(载荷契约无密钥键,
//! 本命令不碰库不碰 keys.json)。

use std::path::{Path, PathBuf};

use chrono::Local;
use serde_json::{json, Value};
use tauri::AppHandle;
use tauri_plugin_dialog::DialogExt;

/// 成员表头行(R3 钉死四列;列名人话,wxid 是任务令明准的成员行次要词面)。
const MEMBER_CSV_HEADER: &str = "显示名,备注,wxid,是否群主";

/// 错误信封(仓惯例同形;wechat_keyprovider::error_value 私有不跨引,本地
/// 同形孪生保持文件独立,并行改面零冲突)。
fn error_value(code: &str, message: &str) -> String {
    json!({"code": code, "path": "$", "message": message}).to_string()
}

/// 导出计划(纯形状:缺省文件名 + 成员表行;不触对话框不落盘,测试直驱)。
pub(crate) struct GroupExportPlan {
    /// 保存对话框缺省文件名:`群信息-<显示名>-<YYYY-MM-DD>.json`。
    pub(crate) default_file_name: String,
    /// 成员表行(每行 [显示名, 备注, wxid, 是否群主];缺 members 键/非数组
    /// = 空表如实降级,只写头行,不判错——契约缺表 = 空表)。
    pub(crate) csv_rows: Vec<[String; 4]>,
}

/// 导出结果(两件落盘绝对路径 + 成员行数;直转前端应答,wire snake_case)。
pub(crate) struct GroupExportOutcome {
    json_path: String,
    csv_path: String,
    member_rows: usize,
}

impl GroupExportOutcome {
    fn to_value(self) -> Value {
        json!({
            "json_path": self.json_path,
            "csv_path": self.csv_path,
            "member_rows": self.member_rows,
        })
    }
}

/// 文件名净化:显示名可能含路径分隔符与冒号(macOS Finder 显示 `/`↔`:`,
/// Windows 禁 `\` `:`)与控制符——一律替 `_`,其余字符原样保真(不 ASCII 化,
/// 群名表情/中文照留)。
fn sanitize_file_name(raw: &str) -> String {
    raw.chars()
        .map(|c| match c {
            '/' | '\\' | ':' => '_',
            c if (c as u32) < 0x20 => '_',
            c => c,
        })
        .collect()
}

/// 缺省文件名 + 成员表行(纯函数)。display_name 缺行/空白 → 回落 chat_id
/// (寻址键原样,真名零虚构);日期 = 本地时当天 `%Y-%m-%d`(chrono 锁内
/// 已有同版,零新增 crate)。
fn plan_group_export(chat_id: &str, json_payload: &Value) -> GroupExportPlan {
    let display = json_payload
        .get("display_name")
        .and_then(Value::as_str)
        .map(str::trim)
        .filter(|name| !name.is_empty())
        .unwrap_or(chat_id);
    let date = Local::now().format("%Y-%m-%d").to_string();
    GroupExportPlan {
        default_file_name: format!("群信息-{}-{}.json", sanitize_file_name(display), date),
        csv_rows: member_csv_rows(json_payload),
    }
}

/// 载荷 members 键 → 成员表行。行内残缺(非对象/无 username)跳过不判错
/// (单行漂移不拦整表,判例 wechat-groupinfo-api.ts parseMembers 同门);
/// display/remark 非串 = 空单元格,is_owner 非真 = 「否」。
fn member_csv_rows(json_payload: &Value) -> Vec<[String; 4]> {
    let Some(members) = json_payload.get("members").and_then(Value::as_array) else {
        return Vec::new();
    };
    members
        .iter()
        .filter_map(|member| {
            let record = member.as_object()?;
            let username = record.get("username")?.as_str()?;
            let display = record.get("display").and_then(Value::as_str).unwrap_or("");
            let remark = record.get("remark").and_then(Value::as_str).unwrap_or("");
            let is_owner = record.get("is_owner").and_then(Value::as_bool).unwrap_or(false);
            Some([
                display.to_string(),
                remark.to_string(),
                username.to_string(),
                if is_owner { "是".to_string() } else { "否".to_string() },
            ])
        })
        .collect()
}

/// CSV 单元格转义(RFC 4180 引号照旧)+ **公式注入中和**:以 `=` `+` `-`
/// `@` `\t` 开头的单元格前置 `'`(Excel/WPS 文本前导符,公式当文本)——
/// 「显示名/备注」由任意群成员的微信昵称与备注决定(攻击者可控),昵称形如
/// `=HYPERLINK(...)`/`=cmd|…` 的成员表被表格软件直开时按公式执行(OWASP
/// CSV Injection 同款中和;引号转义只管 CSV 语法不管公式求值,故中和先于
/// 引号判定)。
fn csv_field(field: &str) -> String {
    let neutralized = match field.chars().next() {
        Some('=' | '+' | '-' | '@' | '\t') => format!("'{field}"),
        _ => field.to_string(),
    };
    if neutralized.contains(',')
        || neutralized.contains('"')
        || neutralized.contains('\n')
        || neutralized.contains('\r')
    {
        format!("\"{}\"", neutralized.replace('"', "\"\""))
    } else {
        neutralized
    }
}

/// 成员表 CSV 文本:BOM + 头行 + 数据行(CRLF;BOM 保 Excel 中文不乱码)。
fn build_member_csv(rows: &[[String; 4]]) -> String {
    let mut csv = String::from("\u{feff}");
    csv.push_str(MEMBER_CSV_HEADER);
    csv.push_str("\r\n");
    for row in rows {
        let cells: Vec<String> = row.iter().map(|cell| csv_field(cell)).collect();
        csv.push_str(&cells.join(","));
        csv.push_str("\r\n");
    }
    csv
}

/// 两件落盘(JSON = 所选路径原样;CSV = `with_extension("csv")` 同目录同名)。
/// 返回成员行数。失败人话报哪件(路径 + 原因);JSON 已写而 CSV 失败时不删
/// 已落盘件(对用户数据零删除纪律,失败如实上屏哪件没成)。
fn write_group_export_files(
    json_path: &Path,
    payload: &Value,
    csv_rows: &[[String; 4]],
) -> Result<usize, String> {
    let mut json_body = serde_json::to_string_pretty(payload)
        .map_err(|err| error_value("export_failed", &format!("群信息序列化失败: {err}")))?;
    json_body.push('\n');
    std::fs::write(json_path, json_body).map_err(|err| {
        error_value(
            "export_failed",
            &format!("群信息写入失败({}): {err}", json_path.display()),
        )
    })?;
    let csv_path = json_path.with_extension("csv");
    std::fs::write(&csv_path, build_member_csv(csv_rows)).map_err(|err| {
        error_value(
            "export_failed",
            &format!("成员表写入失败({}): {err}", csv_path.display()),
        )
    })?;
    Ok(csv_rows.len())
}

/// 对话框结果 → 落盘接缝(纯函数,cargo 测试直驱;命令本体只剩弹窗接线)。
/// `None`(用户取消)= `Ok(None)` 静默返回,零写盘;`Some(path)` = 两件
/// 成套落盘,返回 `Some(outcome)`。
fn finish_group_export(
    picked: Option<PathBuf>,
    payload: &Value,
    plan: &GroupExportPlan,
) -> Result<Option<GroupExportOutcome>, String> {
    let Some(json_path) = picked else {
        return Ok(None);
    };
    let member_rows = write_group_export_files(&json_path, payload, &plan.csv_rows)?;
    let csv_path = json_path.with_extension("csv");
    Ok(Some(GroupExportOutcome {
        json_path: json_path.display().to_string(),
        csv_path: csv_path.display().to_string(),
        member_rows,
    }))
}

/// 群信息导出(面板「导出」按钮接活;R3):保存对话框 → JSON + 成员表 CSV
/// 两件成套落盘。应答 `Option`:`null` = 用户取消(前端静默);对象 =
/// `{json_path, csv_path, member_rows}`。载荷由前端供给,壳零重查零读库。
#[tauri::command]
pub async fn wechat_group_export(
    app: AppHandle,
    chat_id: String,
    json_payload: Value,
) -> Result<Option<Value>, String> {
    let plan = plan_group_export(&chat_id, &json_payload);
    let default_file_name = plan.default_file_name.clone();
    // 对话框在 spawn_blocking 线程弹(插件内部自 hop main thread);本线程
    // 只等结果。`blocking_save_file` → `None` = 用户取消。
    let dialog_app = app.clone();
    let joined = tauri::async_runtime::spawn_blocking(move || {
        dialog_app
            .dialog()
            .file()
            .set_file_name(&default_file_name)
            .add_filter("JSON", &["json"])
            .blocking_save_file()
            .map(|file| file.into_path())
    });
    let picked = joined
        .await
        .map_err(|err| error_value("internal_error", &format!("导出保存对话框线程失败: {err}")))?;
    let picked = match picked {
        None => None,
        Some(Ok(path)) => Some(path),
        Some(Err(err)) => {
            return Err(error_value("export_failed", &format!("保存路径不可用: {err}")))
        }
    };
    let outcome = finish_group_export(picked, &json_payload, &plan)?;
    match &outcome {
        None => log::info!("群信息导出:用户取消保存对话框(chat={chat_id}),静默返回零写盘"),
        Some(out) => log::info!(
            "群信息导出:JSON+成员表两件落盘 chat={chat_id} json={} csv={} 成员 {} 行",
            out.json_path,
            out.csv_path,
            out.member_rows
        ),
    }
    Ok(outcome.map(GroupExportOutcome::to_value))
}

#[cfg(test)]
mod tests {
    use super::*;
    use std::fs;

    /// 契约夹具(任务档 prd「group-info 应答契约 v1」同形;面板侧 vitest
    /// 夹具同源)。
    fn contract_payload() -> Value {
        json!({
            "chat_id": "50438708676@chatroom",
            "display_name": "TMS 中转站交流1️⃣",
            "member_count": 97,
            "owner": {"username": "wxid_owner", "display": "老王"},
            "announcement": {
                "text": "本群仅供技术交流,禁止广告。",
                "editor_display": "老王",
                "published_at": "2026-10-13T09:30:00"
            },
            "status": null,
            "members": [
                {"username": "wxid_owner", "display": "老王", "remark": null, "is_owner": true},
                {"username": "wxid_a", "display": "花开相随", "remark": "备注名", "is_owner": false},
                {"username": "wxid_b", "display": null, "remark": null, "is_owner": false}
            ]
        })
    }

    /// 载荷写盘(R3 验收③):JSON 可解析回原载荷零改形;CSV 同目录同名
    /// 成套,行数 = 头 + 成员,群主行「是」、成员行「否」。
    #[test]
    fn export_writes_json_payload_verbatim_and_member_csv() {
        let dir = tempfile::tempdir().unwrap();
        let payload = contract_payload();
        let plan = plan_group_export("50438708676@chatroom", &payload);
        let json_path = dir.path().join("群信息-TMS-2026-10-13.json");
        let outcome =
            finish_group_export(Some(json_path.clone()), &payload, &plan).unwrap().unwrap();
        // JSON 逐字节语义等值(pretty 再解析回原载荷)
        let written: Value =
            serde_json::from_str(&fs::read_to_string(&json_path).unwrap()).unwrap();
        assert_eq!(written, payload);
        // CSV 同目录同名(扩展名替换成套)
        let csv_path = dir.path().join("群信息-TMS-2026-10-13.csv");
        assert_eq!(outcome.json_path, json_path.display().to_string());
        assert_eq!(outcome.csv_path, csv_path.display().to_string());
        assert_eq!(outcome.member_rows, 3);
        let csv = fs::read_to_string(&csv_path).unwrap();
        let lines: Vec<&str> = csv.lines().collect();
        assert_eq!(lines.len(), 4); // 头 + 3 成员
        // 首行带 BOM 字符(lines() 不剥;BOM 本体由 BOM 专项测试断言)
        assert_eq!(lines[0], "\u{feff}显示名,备注,wxid,是否群主");
        assert_eq!(lines[1], "老王,,wxid_owner,是"); // remark null = 空单元格
        assert_eq!(lines[2], "花开相随,备注名,wxid_a,否");
        assert_eq!(lines[3], ",,wxid_b,否"); // display null = 空单元格
    }

    /// CSV BOM(R3):UTF-8 BOM 开头保 Excel 直开中文不乱码;含逗号/引号
    /// 字段按 RFC 4180 加引号转义。
    #[test]
    fn member_csv_carries_utf8_bom_and_escapes_rfc4180() {
        let dir = tempfile::tempdir().unwrap();
        let payload = json!({
            "chat_id": "x@chatroom",
            "display_name": "转义群",
            "members": [
                {"username": "wxid_c", "display": "名,字", "remark": "引\"号", "is_owner": false}
            ]
        });
        let plan = plan_group_export("x@chatroom", &payload);
        let json_path = dir.path().join("转义.json");
        finish_group_export(Some(json_path.clone()), &payload, &plan).unwrap().unwrap();
        let bytes = fs::read(dir.path().join("转义.csv")).unwrap();
        assert_eq!(&bytes[..3], &[0xEF, 0xBB, 0xBF], "UTF-8 BOM 必在文件头");
        let csv = String::from_utf8(bytes).unwrap();
        assert!(csv.starts_with("\u{feff}显示名,备注,wxid,是否群主\r\n"));
        // 逗号字段整体加引号;内部引号翻倍
        assert!(csv.contains("\"名,字\","));
        assert!(csv.contains("\"引\"\"号\","));
    }

    /// 公式注入中和:以 `=` `+` `-` `@` `\t` 开头的单元格前置 `'`(公式
    /// 当文本,Excel/WPS 直开不执行);普通单元格原样,RFC 4180 引号转义
    /// 照旧(中和后含逗号仍加引号)。成员昵称/备注攻击者可控的针对防。
    #[test]
    fn csv_field_neutralizes_formula_prefix_cells() {
        // = 开头且含引号:前导 ' 中和 + 整体加引号、内部引号翻倍(两道并存)
        assert_eq!(
            csv_field("=HYPERLINK(\"http://x\")"),
            "\"'=HYPERLINK(\"\"http://x\"\")\""
        );
        assert_eq!(csv_field("=cmd|' /C calc'!A0"), "'=cmd|' /C calc'!A0");
        assert_eq!(csv_field("+1+1"), "'+1+1");
        assert_eq!(csv_field("-x"), "'-x");
        assert_eq!(csv_field("@import"), "'@import");
        assert_eq!(csv_field("\t跳格开头"), "'\t跳格开头");
        // 普通单元格零改形(前导中和不误伤)
        assert_eq!(csv_field("花开相随"), "花开相随");
        assert_eq!(csv_field("名字x"), "名字x");
        assert_eq!(csv_field("wxid_owner"), "wxid_owner");
        assert_eq!(csv_field("是"), "是");
        assert_eq!(csv_field(""), "");
        // 中和先于引号判定:= 开头且含逗号 → 前导 ' + 整体加引号
        assert_eq!(csv_field("=1,2"), "\"'=1,2\"");
        // 原有 RFC 4180 语义不回退
        assert_eq!(csv_field("名,字"), "\"名,字\"");
        assert_eq!(csv_field("引\"号"), "\"引\"\"号\"");
    }

    /// 成员表整链:昵称 = 公式载荷的成员行经 build_member_csv 中和落盘
    /// (端到端:display/remark 两列攻击者可控面)。
    #[test]
    fn member_csv_neutralizes_attacker_controlled_name_cells() {
        let rows = vec![
            [
                "=HYPERLINK(\"http://evil\")".to_string(),
                "+SUM(A1)".to_string(),
                "wxid_evil".to_string(),
                "否".to_string(),
            ],
        ];
        let csv = build_member_csv(&rows);
        // = 开头且含引号:中和前导 ' + RFC 4180 引号翻倍,两道并存
        assert!(csv.contains("\"'=HYPERLINK(\"\"http://evil\"\")\""), "{csv}");
        assert!(csv.contains("'+SUM(A1)"), "{csv}");
        assert!(!csv.contains("\r\n=HYPERLINK"), "公式原样不得出现在行首: {csv}");
    }

    /// 对话框取消(R3)= 静默返回:`None` 接缝 → `Ok(None)`,零写盘
    /// (接缝测试:原生对话框在 cargo test 里弹不出,命令本体对该接缝
    /// 零改形直通——`wechat_group_export` 只把 `blocking_save_file` 的
    /// `None` 原样喂进本函数)。
    #[test]
    fn dialog_cancel_returns_silently_without_writes() {
        let dir = tempfile::tempdir().unwrap();
        let payload = contract_payload();
        let plan = plan_group_export("50438708676@chatroom", &payload);
        let outcome = finish_group_export(None, &payload, &plan).unwrap();
        assert!(outcome.is_none());
        assert_eq!(fs::read_dir(dir.path()).unwrap().count(), 0, "取消零写盘");
    }

    /// 缺省文件名:`群信息-<显示名>-<当天>.json`;显示名含路径分隔符/冒号
    /// 净化为 `_`;display_name 缺行回落 chat_id(真名零虚构)。
    #[test]
    fn default_file_name_sanitizes_display_and_falls_back_to_chat_id() {
        let today = Local::now().format("%Y-%m-%d").to_string();
        let payload = json!({
            "chat_id": "50438708676@chatroom",
            "display_name": "AI/中转:站\\群",
            "members": []
        });
        let plan = plan_group_export("50438708676@chatroom", &payload);
        assert_eq!(
            plan.default_file_name,
            format!("群信息-AI_中转_站_群-{today}.json")
        );
        // display_name 缺行 → chat_id 原样(净化后 @ 无害)
        let bare = json!({"chat_id": "50438708676@chatroom", "display_name": null, "members": []});
        let plan = plan_group_export("50438708676@chatroom", &bare);
        assert!(plan.default_file_name.starts_with("群信息-50438708676@chatroom-"));
        // members 缺键 = 空表如实降级(只写头行,不判错)
        let plan = plan_group_export("x@chatroom", &json!({"chat_id": "x@chatroom"}));
        assert!(plan.csv_rows.is_empty());
    }
}
