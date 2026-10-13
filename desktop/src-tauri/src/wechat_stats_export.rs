//! 微信统计报告导出(task 10-14-wechat-stats-reports R7)。
//!
//! 消息屏微信工作台「统计报告」分区导出按钮的壳侧通道:前端**已持**桥
//! stats 应答与 AI 报告 Markdown(wechat-stats-api.ts 产物),本命令吃
//! `{default_name, json_payload, markdown_payload?}` 原样落盘,**壳不重查
//! 不读任何微信库**(判例 wechat_group_export.rs 成对实现,注释互指)。
//!
//! 两件成套(R7 钉死):
//! - JSON:系统保存对话框(dialog 插件 `blocking_save_file`,缺省文件名
//!   由前端给,如 `年度报告-2026.json`)→ 所选路径写统计树全文
//!   (pretty + 尾换行,零改形);
//! - Markdown:同目录**同名** `<所选项去扩展名>.md` 写 AI 报告文本
//!   (UTF-8 + 尾换行);`markdown_payload` 缺席(null)= 只落 JSON 一件,
//!   回执 `markdown_path` 缺省。
//!
//! 取消 = 静默返回:用户关掉保存对话框(`None`)→ 命令返回 `Ok(null)`,
//! 零写盘零提示;前端态机回 idle。
//!
//! 线程纪律:`blocking_save_file` 禁主线程,走
//! `tauri::async_runtime::spawn_blocking`(判例 wechat_group_export.rs
//! 同款)。错误信封沿仓惯例 `{"code","path","message"}` JSON 字符串
//! (前端 asSidecarError 同形解析);message 一律人话。
//!
//! 红线:对微信数据零读(载荷由前端供给);密钥零沾。

use std::path::{Path, PathBuf};

use serde_json::{json, Value};
use tauri::AppHandle;
use tauri_plugin_dialog::DialogExt;

/// 错误信封(仓惯例同形;与 wechat_group_export::error_value 各自本地
/// 同形孪生,保持文件独立,并行改面零冲突)。
fn error_value(code: &str, message: &str) -> String {
    json!({"code": code, "path": "$", "message": message}).to_string()
}

/// 导出结果(落盘绝对路径;markdown 缺席 = None,直转前端应答)。
pub(crate) struct StatsExportOutcome {
    json_path: String,
    markdown_path: Option<String>,
}

impl StatsExportOutcome {
    fn to_value(self) -> Value {
        match self.markdown_path {
            Some(md) => json!({"json_path": self.json_path, "markdown_path": md}),
            None => json!({"json_path": self.json_path}),
        }
    }
}

/// 两件落盘(JSON = 所选路径原样 pretty;Markdown = `with_extension("md")`
/// 同目录同名,`markdown_payload` 缺席则不写)。JSON 已写而 Markdown 失败时
/// 不删已落盘件(对用户数据零删除纪律,失败如实报哪件没成)。
fn write_stats_export_files(
    json_path: &Path,
    json_payload: &Value,
    markdown_payload: Option<&str>,
) -> Result<Option<String>, String> {
    let mut json_body = serde_json::to_string_pretty(json_payload)
        .map_err(|err| error_value("export_failed", &format!("统计树序列化失败: {err}")))?;
    json_body.push('\n');
    std::fs::write(json_path, json_body).map_err(|err| {
        error_value(
            "export_failed",
            &format!("统计 JSON 写入失败({}): {err}", json_path.display()),
        )
    })?;
    let Some(markdown) = markdown_payload else {
        return Ok(None);
    };
    let md_path = json_path.with_extension("md");
    let mut md_body = markdown.to_string();
    if !md_body.ends_with('\n') {
        md_body.push('\n');
    }
    std::fs::write(&md_path, md_body).map_err(|err| {
        error_value(
            "export_failed",
            &format!("AI 报告写入失败({}): {err}", md_path.display()),
        )
    })?;
    Ok(Some(md_path.display().to_string()))
}

/// 对话框结果 → 落盘接缝(纯函数,cargo 测试直驱;命令本体只剩弹窗接线)。
/// `None`(用户取消)= `Ok(None)` 静默返回,零写盘。
fn finish_stats_export(
    picked: Option<PathBuf>,
    json_payload: &Value,
    markdown_payload: Option<&str>,
) -> Result<Option<StatsExportOutcome>, String> {
    let Some(json_path) = picked else {
        return Ok(None);
    };
    let markdown_path = write_stats_export_files(&json_path, json_payload, markdown_payload)?;
    Ok(Some(StatsExportOutcome {
        json_path: json_path.display().to_string(),
        markdown_path,
    }))
}

/// 统计报告导出(面板「导出」按钮接活;R7):保存对话框一次 → JSON 统计树
/// (+ 在场 AI 报告 Markdown)两件成套落盘。应答 `Option`:`null` = 用户
/// 取消(前端静默);对象 = `{json_path, markdown_path?}`。载荷由前端供给,
/// 壳零重查零读库。
#[tauri::command]
pub async fn wechat_stats_export(
    app: AppHandle,
    default_name: String,
    json_payload: Value,
    markdown_payload: Option<String>,
) -> Result<Option<Value>, String> {
    let default = if default_name.trim().is_empty() {
        "统计报告.json".to_string()
    } else {
        default_name
    };
    let default_label = default.clone(); // 供收尾日志(spawn 闭包拿走所有权)
    // 对话框在 spawn_blocking 线程弹(插件内部自 hop main thread);本线程
    // 只等结果。`blocking_save_file` → `None` = 用户取消。
    let dialog_app = app.clone();
    let joined = tauri::async_runtime::spawn_blocking(move || {
        dialog_app
            .dialog()
            .file()
            .set_file_name(&default)
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
    let outcome = finish_stats_export(picked, &json_payload, markdown_payload.as_deref())?;
    match &outcome {
        None => log::info!(
            "统计报告导出:用户取消保存对话框(缺省名 {default_label}),静默返回零写盘"
        ),
        Some(out) => log::info!(
            "统计报告导出:两件落盘 json={} md={:?}",
            out.json_path,
            out.markdown_path
        ),
    }
    Ok(outcome.map(StatsExportOutcome::to_value))
}

#[cfg(test)]
mod tests {
    use super::*;
    use std::fs;

    /// 契约夹具(任务档 prd R2 应答契约 v1 同形;面板侧 vitest 夹具同源)。
    fn contract_payload() -> Value {
        json!({
            "stats_annual": {
                "year": 2026,
                "total": 20961,
                "sent": 10533,
                "received": 10173,
                "human_total": 20706,
                "type_counts": {"text": 17940, "image": 1135, "other": 746},
                "hourly": [0, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22],
                "weekday": [1, 2, 3, 4, 5, 6, 7],
                "monthly": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
                "active_days": 90,
                "longest_streak": {"days": 90, "from": "2026-07-07", "to": "2026-10-04"},
                "chats_count": 162,
                "top_chats": [{"chat_id": "wxid_x", "display_name": "好友", "count": 3525}],
                "top_phrases": [{"phrase": "这个", "count": 1283}],
                "midnight": {"count": 2155, "top_chat": null},
                "friend_contrast": []
            }
        })
    }

    /// 两件成套(R7 验收):JSON 可解析回原载荷零改形;Markdown 同目录
    /// 同名成套;回执两路径齐备。
    #[test]
    fn export_writes_json_and_markdown_pair() {
        let dir = tempfile::tempdir().unwrap();
        let payload = contract_payload();
        let json_path = dir.path().join("年度报告-2026.json");
        let outcome = finish_stats_export(
            Some(json_path.clone()),
            &payload,
            Some("# 总览\n\n全年 20,961 条消息。\n"),
        )
        .unwrap()
        .unwrap();
        let written: Value = serde_json::from_str(&fs::read_to_string(&json_path).unwrap()).unwrap();
        assert_eq!(written, payload);
        let md_path = dir.path().join("年度报告-2026.md");
        assert_eq!(outcome.json_path, json_path.display().to_string());
        assert_eq!(
            outcome.markdown_path.as_deref(),
            Some(md_path.display().to_string().as_str())
        );
        let md = fs::read_to_string(&md_path).unwrap();
        assert!(md.starts_with("# 总览"));
        assert!(md.ends_with('\n')); // 尾换行补齐
    }

    /// Markdown 缺席(null)= 只落 JSON 一件;回执 markdown_path 缺省。
    #[test]
    fn export_without_markdown_writes_json_only() {
        let dir = tempfile::tempdir().unwrap();
        let payload = contract_payload();
        let json_path = dir.path().join("私聊分析.json");
        let outcome =
            finish_stats_export(Some(json_path.clone()), &payload, None).unwrap().unwrap();
        assert!(outcome.markdown_path.is_none());
        assert_eq!(fs::read_dir(dir.path()).unwrap().count(), 1, "只落一件");
        assert!(serde_json::from_str::<Value>(
            &fs::read_to_string(&json_path).unwrap()
        )
        .is_ok());
    }

    /// 对话框取消 = 静默:`None` 接缝 → `Ok(None)`,零写盘。
    #[test]
    fn dialog_cancel_returns_silently_without_writes() {
        let dir = tempfile::tempdir().unwrap();
        let outcome =
            finish_stats_export(None, &contract_payload(), Some("# x\n")).unwrap();
        assert!(outcome.is_none());
        assert_eq!(fs::read_dir(dir.path()).unwrap().count(), 0, "取消零写盘");
    }
}
