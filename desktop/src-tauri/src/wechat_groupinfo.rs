//! 微信群信息读取(task 10-13-wechat-groupinfo R2;「群信息」面板数据源)。
//!
//! 前端 `wechat-groupinfo-api.ts` `wechatGroupInfo()` 的壳侧对子(规格 =
//! 该文件头注「寻址」节,契约 = 任务档 prd「group-info 应答契约 v1」):
//! 两段 spawn 安装态桥 —— ①名→id 解析:寻址键已是 `@chatroom` 形态直查
//! 免解析;显示名则 spawn 桥 `sessions list --json` 按名**精确等值**解析出
//! `@chatroom` id(引擎 wechat_local `_resolve_session_id` 同律:id 非空
//! 且 ≠ 声明值才采信;桥自身对 `localdb group-info` 只做 `chat_room.username`
//! 精确等值直查,不做显示名解析)。②命中才 spawn 桥 `localdb group-info
//! <id> --json`,应答 = `group_info` 内层对象**直转**(wire snake_case 零改
//! 形,判例 wechat_key_status 的 key_status 直转,wechat_keyprovider.rs:
//! 1064-1075)。
//!
//! 解析不到 = 结构化 `group_not_resolved`(人话「未能定位该群(不在最近
//! 会话)」)——**不冒充 0 人**:桥空结构(member_count=0)是「库如实无此
//! 群」,解析不到是「壳侧定位失败」,两者分层(评审 10-13 修正,原「不在
//! 列表回空结构」的词面会把真 500 人群演成 0)。错误走前端面板错误态
//! (ErrorBox,重试可再解析)。
//!
//! 错误归一:桥具名错误族原样透传(exit 20 缺数据根 / 21 缺密钥 / 22 解密
//! 失败 —— 密钥链与 query/sns 同一全链;**错误族不是正常态**,与「缺表/
//! 缺行 = 键 null/空表且 exit 0」的查询层降级分层)。
//!
//! 红线:全程对微信数据**只读**(sessions list = 像素链截窗读,group-info =
//! 解密副本 SQL 只读);密钥零沾(本命令不读 keys.json,桥错误族也不回传
//! 密钥材料)。
//!
//! 孪生纪律:`error_value`/`run_bridge_with_deadline` 等胶水 =
//! wechat_keyprovider 同形孪生(私有不跨引,本地孪生保持文件独立,判例
//! wechat_group_export.rs error_value 注);桥 bin 落点与 MYIA_HOME 注入
//! 规则同一字面量/同一规则,漂移即两侧同步。

use std::path::{Path, PathBuf};
use std::time::{Duration, Instant};

use serde_json::{json, Map, Value};
use tauri::{AppHandle, Manager};

/// 桥 bin 缺省落点(相对用户 home;wechat_keyprovider::BRIDGE_BIN_REL 同一
/// 钉死字面量,组件部署位唯一)。
const BRIDGE_BIN_REL: &str = ".myia/plugins/wechat-bridge/bin/wechat-bridge";

/// 桥命令帽:两段 spawn 各自 90s —— sessions list 走像素链(截窗 + OCR +
/// VL 修字,桥读族最重命令,> 引擎族帽 60s 留慢机余量);localdb group-info
/// 是秒级单库只读,同一帽统一(总上界 180s 由面板 loading 态承接)。
const BRIDGE_TIMEOUT: Duration = Duration::from_secs(90);
/// try_wait 非阻塞轮询步长(wechat_keyprovider::POLL_INTERVAL 同值孪生)。
const POLL_INTERVAL: Duration = Duration::from_millis(50);
/// 失败兜底 stderr 尾部回显长度(design「stderr 收尾 500 字符」同值孪生)。
const STDERR_TAIL_CHARS: usize = 500;

/// 错误信封(仓惯例 `{"code","path","message"[,"data"]}` JSON 字符串,前端
/// asSidecarError 同形解析;同形孪生纪律见模块头注)。
fn error_value(code: &str, message: &str, data: Option<Value>) -> String {
    match data {
        Some(payload) => json!({"code": code, "path": "$", "message": message, "data": payload})
            .to_string(),
        None => json!({"code": code, "path": "$", "message": message}).to_string(),
    }
}

fn invalid_params(path: &str, message: String) -> String {
    json!({"code": "invalid_params", "path": path, "message": message}).to_string()
}

/// stderr 尾部(字符取尾,防多字节截半;wechat_keyprovider 同形孪生)。
fn stderr_tail(stderr: &str) -> String {
    let chars: Vec<char> = stderr.chars().collect();
    let start = chars.len().saturating_sub(STDERR_TAIL_CHARS);
    chars[start..].iter().collect()
}

/// 可执行文件判定(unix 看执行位;非 unix 家族落 .exe 即视为可执行;
/// wechat_keyprovider 同形孪生)。
#[cfg(unix)]
fn is_executable_file(path: &Path) -> bool {
    use std::os::unix::fs::PermissionsExt;
    path.is_file()
        && std::fs::metadata(path)
            .map(|meta| meta.permissions().mode() & 0o111 != 0)
            .unwrap_or(false)
}
#[cfg(not(unix))]
fn is_executable_file(path: &Path) -> bool {
    path.is_file()
}

/// 桥失败归一(wechat_keyprovider 同形孪生):stdout 单 JSON 携
/// `error{code,message,fix_hint}` → 码名/人话原样透传(fix_hint 进 data);
/// 否则 `bridge_error` 兜底带 exit 码 + stderr 尾部。
fn bridge_error_value(exit_code: Option<i32>, stdout: &str, stderr: &str) -> String {
    if let Ok(payload) = serde_json::from_str::<Value>(stdout.trim()) {
        if let Some(error) = payload.get("error").and_then(Value::as_object) {
            let code = error
                .get("code")
                .and_then(Value::as_str)
                .filter(|code| !code.is_empty())
                .unwrap_or("bridge_error");
            let message = error
                .get("message")
                .and_then(Value::as_str)
                .unwrap_or("桥返回失败(无说明)");
            let mut data = Map::new();
            if let Some(hint) = error.get("fix_hint").and_then(Value::as_str) {
                data.insert("fix_hint".into(), json!(hint));
            }
            return error_value(
                code,
                message,
                (!data.is_empty()).then_some(Value::Object(data)),
            );
        }
    }
    error_value(
        "bridge_error",
        &format!(
            "wechat-bridge 组件返回了无法识别的结果(exit={:?});stderr 尾部: {}",
            exit_code,
            stderr_tail(stderr).trim()
        ),
        None,
    )
}
/// 同步跑桥子进程(在 spawn_blocking 线程;超时 kill 兜底;wechat_keyprovider
/// 同形孪生:剥 PYTHONPATH + MYIA_HOME 显式尊重/未设注入)。
fn run_bridge_with_deadline(
    bin: &Path,
    argv: &[String],
    myia_home_env: Option<PathBuf>,
    timeout: Duration,
) -> Result<(Option<i32>, String, String), String> {
    use std::io::{Read};
    use std::process::{Command, Stdio};
    let mut command = Command::new(bin);
    command
        .args(argv)
        .stdin(Stdio::null())
        .stdout(Stdio::piped())
        .stderr(Stdio::piped())
        .env_remove("PYTHONPATH");
    if let Some(root) = myia_home_env {
        command.env("MYIA_HOME", root);
    }
    let mut child = command.spawn().map_err(|e| {
        error_value(
            "spawn_failed",
            &format!("群信息命令拉起桥失败({}): {}", bin.display(), e),
            None,
        )
    })?;
    let deadline = Instant::now() + timeout;
    let mut stdout_pipe = child.stdout.take();
    let mut stderr_pipe = child.stderr.take();
    loop {
        match child.try_wait() {
            Ok(Some(status)) => {
                let mut stdout_buf = Vec::new();
                let mut stderr_buf = Vec::new();
                if let Some(mut pipe) = stdout_pipe.take() {
                    let _ = pipe.read_to_end(&mut stdout_buf);
                }
                if let Some(mut pipe) = stderr_pipe.take() {
                    let _ = pipe.read_to_end(&mut stderr_buf);
                }
                return Ok((
                    status.code(),
                    String::from_utf8_lossy(&stdout_buf).into_owned(),
                    String::from_utf8_lossy(&stderr_buf).into_owned(),
                ));
            }
            Ok(None) => {}
            Err(e) => {
                return Err(error_value(
                    "bridge_error",
                    &format!("等待桥子进程退出失败: {e}"),
                    None,
                ))
            }
        }
        if Instant::now() >= deadline {
            let _ = child.kill();
            let _ = child.wait();
            return Err(error_value(
                "bridge_timeout",
                &format!("群信息命令超过 {timeout:?} 未退出,子进程已终止"),
                None,
            ));
        }
        std::thread::sleep(POLL_INTERVAL);
    }
}

/// 桥上下文前置(home/bin 探测 + MYIA_HOME 注入决策;wechat_keyprovider
/// resolve_bridge_context 同形孪生,component_missing 同 B5 口径)。
fn resolve_bridge_context(app: &AppHandle) -> Result<(PathBuf, Option<PathBuf>), String> {
    let home = app
        .path()
        .home_dir()
        .map_err(|e| error_value("internal_error", &format!("用户 home 目录不可解析: {e}"), None))?;
    let bin = home.join(BRIDGE_BIN_REL);
    if !(bin.is_file() && is_executable_file(&bin)) {
        return Err(error_value(
            "component_missing",
            &format!("微信本机桥组件未安装或不可执行: {}", bin.display()),
            None,
        ));
    }
    let myia_home_env = if std::env::var_os("MYIA_HOME").is_some() {
        None
    } else {
        Some(crate::data_root(app).map_err(|e| {
            error_value("internal_error", &format!("数据根不可解析: {e}"), None)
        })?)
    };
    Ok((bin, myia_home_env))
}

/// 寻址键是否已是库内群 id 形态(`<非空前缀>@chatroom` → 直查免解析;规格
/// = wechat-groupinfo-api.ts 头注「寻址」节末句)。裸 `@chatroom`(前缀空)
/// 不算 id 形态:走名解析路径,解析不到如实 not_resolved,不拿形状可疑的
/// 键直查空结构。
fn is_chatroom_id(chat: &str) -> bool {
    chat.len() > "@chatroom".len() && chat.ends_with("@chatroom")
}

/// sessions 载荷按会话名精确解析 → 会话 id(引擎 wechat_local
/// `_resolve_session_id` 同律:`id` 非空且 ≠ 声明值、`name` 精确等值才
/// 采信;非数组/残缺行跳过;不在列表 = None,调用方报 not_resolved 不猜)。
fn resolve_session_id(payload: &Value, declared: &str) -> Option<String> {
    let sessions = payload.get("sessions")?.as_array()?;
    for session in sessions {
        let Some(record) = session.as_object() else {
            continue;
        };
        let (Some(id), Some(name)) = (
            record.get("id").and_then(Value::as_str),
            record.get("name").and_then(Value::as_str),
        ) else {
            continue;
        };
        if !id.is_empty() && id != declared && name == declared {
            return Some(id.to_string());
        }
    }
    None
}

/// 桥 stdout → 成功载荷(exit 0 且无 `error` 键;失败族经 bridge_error_value
/// 原样透传,非 JSON stdout 兜底 bridge_error;wechat_key_status 同判据孪生)。
fn bridge_success_payload(
    exit_code: Option<i32>,
    stdout: &str,
    stderr: &str,
) -> Result<Value, String> {
    let payload: Value = serde_json::from_str(stdout.trim())
        .map_err(|_| bridge_error_value(exit_code, stdout, stderr))?;
    let success = exit_code.unwrap_or(-1) == 0
        && payload.is_object()
        && payload.get("error").map(Value::is_null).unwrap_or(true);
    if success {
        Ok(payload)
    } else {
        Err(bridge_error_value(exit_code, stdout, stderr))
    }
}

/// 桥 group-info 应答 → `group_info` 内层对象直转(缺对象/非对象 = 桥侧
/// 形状漂移,结构化报不静默;key_status_value 同形孪生)。
fn group_info_value(payload: &Value) -> Result<Value, String> {
    match payload.get("group_info").filter(|inner| inner.is_object()) {
        Some(inner) => Ok(inner.clone()),
        None => Err(error_value(
            "bridge_error",
            "group-info 应答缺 group_info 对象(桥侧形状漂移)",
            None,
        )),
    }
}

/// spawn 桥子进程并等结果(spawn_blocking 线程;BRIDGE_TIMEOUT 帽)。
async fn run_bridge_spawn(
    bin: PathBuf,
    argv: Vec<String>,
    myia_home_env: Option<PathBuf>,
) -> Result<(Option<i32>, String, String), String> {
    let joined =
        tauri::async_runtime::spawn_blocking(move || {
            run_bridge_with_deadline(&bin, &argv, myia_home_env, BRIDGE_TIMEOUT)
        });
    match joined.await {
        Ok(Ok(outcome)) => Ok(outcome),
        Ok(Err(error)) => Err(error),
        Err(err) => Err(error_value(
            "internal_error",
            &format!("群信息命令线程失败: {err}"),
            None,
        )),
    }
}

/// 群信息读取(R2;面板「群信息」弹窗唯一数据源):名→id 解析(sessions
/// list 像素链)→ `localdb group-info <id>` 直转。应答 = `group_info` 对象;
/// 解析不到 = `group_not_resolved`(人话,不冒充 0 人);桥错误族(缺根
/// 20/缺钥 21/解密失败 22)原样透传走面板错误态。只读,密钥零沾。
#[tauri::command]
pub async fn wechat_group_info(app: AppHandle, chat: String) -> Result<Value, String> {
    let key = chat.trim().to_string();
    if key.is_empty() {
        return Err(invalid_params("$.chat", "群寻址键不能为空".into()));
    }
    let (bin, myia_home_env) = resolve_bridge_context(&app)?;

    // ① 名→id 解析:@chatroom 形态直查免解析;显示名 → sessions list 精确
    // 等值解析(不在列表 = 结构化 not_resolved,不冒充 0 人)。
    let chat_id = if is_chatroom_id(&key) {
        key.clone()
    } else {
        let argv = vec!["sessions".into(), "list".into(), "--json".into()];
        let (exit_code, stdout, stderr) =
            run_bridge_spawn(bin.clone(), argv, myia_home_env.clone()).await?;
        let payload = bridge_success_payload(exit_code, &stdout, &stderr)?;
        match resolve_session_id(&payload, &key) {
            Some(id) => id,
            None => {
                log::info!("群信息:会话名解析不到(@chatroom id 不知),报 group_not_resolved chat={key}");
                return Err(error_value(
                    "group_not_resolved",
                    "未能定位该群(不在最近会话)",
                    None,
                ));
            }
        }
    };

    // ② 群信息直查(桥按 chat_room.username 精确等值;缺表/缺行 = 桥侧
    // 键 null/空表如实降级 exit 0,错误族 20/21/22 走透传)。
    let argv = vec![
        "localdb".into(),
        "group-info".into(),
        chat_id.clone(),
        "--json".into(),
    ];
    let (exit_code, stdout, stderr) = run_bridge_spawn(bin, argv, myia_home_env).await?;
    let payload = bridge_success_payload(exit_code, &stdout, &stderr)?;
    let info = group_info_value(&payload)?;
    log::info!(
        "群信息:两段链跑通 chat={key} → id={chat_id} 成员 {} 人",
        info.get("member_count").and_then(Value::as_i64).unwrap_or(-1)
    );
    Ok(info)
}

#[cfg(test)]
mod tests {
    use super::*;
    use serde_json::json;

    /// 寻址键形态判别:`@chatroom` 结尾直查免解析;显示名/裸 wxid 不算。
    #[test]
    fn chatroom_id_form_is_detected_by_suffix() {
        assert!(is_chatroom_id("50438708676@chatroom"));
        assert!(is_chatroom_id("x@chatroom"));
        assert!(!is_chatroom_id("TMS 中转站交流"));
        assert!(!is_chatroom_id("wxid_owner"));
        assert!(!is_chatroom_id("@chatroom")); // 前缀空:形态可疑,仍按名解析路径走
    }

    /// sessions 按名精确解析(引擎 _resolve_session_id 同律):命中取 id;
    /// id==声明值不采信;名字不等不采信;不在列表 None;残缺行跳过。
    #[test]
    fn session_name_resolution_is_exact_and_guards_id_equality() {
        let payload = json!({
            "sessions": [
                {"id": "111@chatroom", "name": "测试会话", "unread": 1},
                {"id": "222@chatroom", "name": "另一群", "unread": null},
                {"id": "333@chatroom", "name": "333@chatroom"},
                {"id": "", "name": "空 id 行"},
                "junk"
            ]
        });
        assert_eq!(
            resolve_session_id(&payload, "测试会话").as_deref(),
            Some("111@chatroom")
        );
        // 声明值本身就是 id:不按 name 采信(引擎 id != declared 守卫)
        assert_eq!(resolve_session_id(&payload, "333@chatroom"), None);
        // 名字不等:None(解析不到,不猜)
        assert_eq!(resolve_session_id(&payload, "不在列表"), None);
        // sessions 缺席/非数组:None
        assert_eq!(resolve_session_id(&json!({}), "x"), None);
        assert_eq!(resolve_session_id(&json!({"sessions": "[]"}), "x"), None);
    }

    /// 桥成功判据:exit 0 且无 error 键;具名错误族原样透传(code/message/
    /// fix_hint);非 JSON stdout 兜底 bridge_error 带 exit 码。
    #[test]
    fn bridge_payload_gates_success_and_passthroughs_named_errors() {
        let ok =
            bridge_success_payload(Some(0), "{\"group_info\": {\"chat_id\": \"x\"}}", "").unwrap();
        assert_eq!(ok["group_info"]["chat_id"], "x");

        let named = bridge_success_payload(
            Some(21),
            "{\"error\": {\"code\": \"key_unavailable\", \"message\": \"密钥缺位\", \"fix_hint\": \"先取钥\"}}",
            "",
        )
        .unwrap_err();
        assert!(named.contains("\"code\":\"key_unavailable\""), "{named}");
        assert!(named.contains("密钥缺位"), "{named}");
        assert!(named.contains("先取钥"), "{named}");

        let fallback = bridge_success_payload(Some(1), "不是 JSON", "stderr 尾巴").unwrap_err();
        assert!(fallback.contains("\"code\":\"bridge_error\""), "{fallback}");
        assert!(fallback.contains("stderr 尾巴"), "{fallback}");

        // exit 非 0 但 stdout 无 error 键:仍判失败(兜底信封)
        let nonzero = bridge_success_payload(Some(20), "{\"group_info\": {}}", "").unwrap_err();
        assert!(nonzero.contains("\"code\":\"bridge_error\""), "{nonzero}");
    }

    /// 应答直转:取 group_info 内层原样;缺对象 = 形状漂移结构化报。
    #[test]
    fn group_info_inner_object_is_transferred_verbatim() {
        let inner = json!({"chat_id": "1@chatroom", "member_count": 3, "members": []});
        let ok = group_info_value(&json!({"group_info": inner})).unwrap();
        assert_eq!(ok, inner);
        let err = group_info_value(&json!({})).unwrap_err();
        assert!(err.contains("group_info"), "{err}");
    }
}
