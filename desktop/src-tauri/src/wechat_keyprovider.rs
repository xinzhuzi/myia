//! 微信本机桥「取钥器」配置面(task 10-13-wechat-keyprovider B5)。
//!
//! 设置页「微信账号」卡取钥器配置行的壳侧通道:spawn **安装态**桥可执行文件
//! (`~/.myia/plugins/wechat-bridge/bin/wechat-bridge`,与
//! `myssia.push.weixin_local.DEFAULT_BRIDGE_BIN` 同一钉死路径)执行
//! `localdb key-provider set|get|clear` 子命令(桥侧实现 = 任务 B2,组件源码
//! 并行落地)。配置只落桥自有 `<数据根>/wechat-bridge/config.json`,经桥管理
//! 命令读写——壳与前端都**不直写**桥配置文件(sidecar-protocol.md 契约纪律:
//! UI 层零 sidecar 协议变更,本面是壳自有 Tauri 命令,不是 sidecar 方法)。
//!
//! 三态判定(已配置/未配置/文件缺失):`get` 应答的 `key_provider.path`
//! 非空 = 已配置(桥 cli.py get 分支 `_emit({"key_provider": {path, state,
//! message}})`——**顶层没有** `key_provider_path` 键,那是桥 config.json 的
//! 键名,不在 get 应答里);壳侧再做文件存在 + 可执行复核(set 时桥校验过,
//! 但文件可能事后被删/失权,get 时如实重探,桥侧 `state` 字段不作为真源)。
//!
//! 子进程纪律:与 pyenv_install 同款 std::process(剥壳继承的
//! PYTHONPATH——桥启动器自设组件根;MYIA_HOME 注入规则与 spawn_sidecar
//! 同源:显式 env 尊重不夺权,未设才注入计算根),30s 防挂死兜底
//! (try_wait 轮询 + 超时 kill;与桥探针 DEFAULT_PROBE_TIMEOUT_SECONDS 同值
//! 量级——本面是纯配置读/写,不碰消息数据)。载荷是单 JSON(远小于管道
//! 缓冲),退出后读干管道即可,无管道写满死锁面。
//!
//! 错误信封沿仓惯例 `{"code","path","message"[,"data"]}` JSON 字符串
//! (前端 asSidecarError 同形解析);桥具名错误族原样透传(码名/人话/
//! fix_hint),与 wechat_local_sidecar.py `_run_bridge` 归一口径一致。

use std::io::Read;
use std::path::{Path, PathBuf};
use std::time::{Duration, Instant};

use serde_json::{json, Map, Value};
use tauri::{AppHandle, Manager};

/// 桥 bin 缺省落点(相对用户 home;与 DEFAULT_BRIDGE_BIN 同一钉死字面量,
/// Rust 侧无 `~` 展开原语故拆 home + 相对段)。装到别处时品类 YAML push 条目
/// `wechat_bridge_bin` 覆写只作用于发送通道——本配置面与协议面
/// (wechat_local_sidecar)同用缺省落点,不给 UI 留任意路径执行缝。
const BRIDGE_BIN_REL: &str = ".myia/plugins/wechat-bridge/bin/wechat-bridge";

/// key-provider 命令超时:纯配置读/写轻命令,30s 防挂死兜底。
const KEY_PROVIDER_TIMEOUT: Duration = Duration::from_secs(30);
/// try_wait 非阻塞轮询步长。
const POLL_INTERVAL: Duration = Duration::from_millis(50);
/// 失败兜底 stderr 尾部回显长度(字符;design §2「stderr 收尾 500 字符」同值)。
const STDERR_TAIL_CHARS: usize = 500;

/// 错误信封(asSidecarError 同形):JSON 字符串。
fn error_value(code: &str, message: &str, data: Option<Value>) -> String {
    match data {
        Some(payload) => json!({"code": code, "path": "$", "message": message, "data": payload}).to_string(),
        None => json!({"code": code, "path": "$", "message": message}).to_string(),
    }
}

fn invalid_params(path: &str, message: String) -> String {
    json!({"code": "invalid_params", "path": path, "message": message}).to_string()
}

/// 桥 bin 绝对路径(home + 钉死相对段)。
pub fn bridge_bin_path(home: &Path) -> PathBuf {
    home.join(BRIDGE_BIN_REL)
}

/// 前导 `~` / `~/` 展开到 home(仅前导形态;`~user` 等不处理,原样透传)。
fn expand_home(input: &str, home: &Path) -> String {
    let trimmed = input.trim();
    if trimmed == "~" {
        return home.display().to_string();
    }
    if let Some(rest) = trimmed.strip_prefix("~/") {
        return home.join(rest).display().to_string();
    }
    trimmed.to_string()
}

/// 可执行文件判定:存在 + 任一执行位(unix);非 unix 家族落 .exe 即视为
/// 可执行,is_file 即可。
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

/// argv 组装(纯函数;动作封闭词表 get/set/clear,`--json` 按桥 CLI 文样
/// 落在子命令尾)。set 门:非空 + 展开后须为绝对路径(`~` 前缀先展开;
/// 相对路径拒——桥/取钥器都可能在不同 cwd 下跑,存绝对路径才无歧义)。
fn key_provider_argv(action: &str, path: Option<&str>, home: &Path) -> Result<Vec<String>, String> {
    match action {
        "get" | "clear" => Ok(vec![
            "localdb".into(),
            "key-provider".into(),
            action.into(),
            "--json".into(),
        ]),
        "set" => {
            let trimmed = path.unwrap_or("").trim();
            if trimmed.is_empty() {
                return Err(invalid_params(
                    "$.path",
                    "取钥器路径不能为空;要清除配置请用「清除配置」".into(),
                ));
            }
            let expanded = expand_home(trimmed, home);
            if !Path::new(&expanded).is_absolute() {
                return Err(invalid_params(
                    "$.path",
                    format!("取钥器路径须为绝对路径(可用 ~ 开头;收到:{trimmed})"),
                ));
            }
            Ok(vec![
                "localdb".into(),
                "key-provider".into(),
                "set".into(),
                expanded,
                "--json".into(),
            ])
        }
        other => Err(invalid_params(
            "$.action",
            format!("未知动作 {other}(合法:get/set/clear)"),
        )),
    }
}

/// get 成功载荷 → 三态快照(pure;file_exists/file_executable 壳侧如实重探,
/// `path` 回存配置原字面)。桥 get 应答形状 = `{"key_provider": {path, state,
/// message}}`(cli.py `_emit`;原文对账用例见
/// `provider_state_bridge_real_get_output`),`key_provider.path` 缺/空/null =
/// 未配置。
fn provider_state_value(payload: &Value, home: &Path) -> Value {
    let stored = payload
        .get("key_provider")
        .and_then(|provider| provider.get("path"))
        .and_then(Value::as_str)
        .map(str::trim)
        .filter(|value| !value.is_empty());
    match stored {
        None => json!({
            "configured": false,
            "path": null,
            "file_exists": false,
            "file_executable": false,
        }),
        Some(stored) => {
            let expanded = expand_home(stored, home);
            let path = Path::new(&expanded);
            json!({
                "configured": true,
                "path": stored,
                "file_exists": path.is_file(),
                "file_executable": is_executable_file(path),
            })
        }
    }
}

/// stderr 尾部(字符取尾,防多字节截半)。
fn stderr_tail(stderr: &str) -> String {
    let chars: Vec<char> = stderr.chars().collect();
    let start = chars.len().saturating_sub(STDERR_TAIL_CHARS);
    chars[start..].iter().collect()
}

/// 桥失败归一(与 wechat_local_sidecar `_run_bridge` 同口径):stdout 单 JSON
/// 携 `error{code,message,fix_hint}` → 码名/人话原样透传(fix_hint 进 data);
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
                (!data.is_empty()).then(|| Value::Object(data)),
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

/// 同步跑桥子进程(在 spawn_blocking 线程;超时 kill 兜底)。
/// `myia_home_env`:None = 尊重显式 MYIA_HOME(不夺权);Some = 未设时注入
/// 的计算数据根(spawn_sidecar 同规则)。
fn run_bridge_with_deadline(
    bin: &Path,
    argv: &[String],
    myia_home_env: Option<PathBuf>,
    timeout: Duration,
) -> Result<(Option<i32>, String, String), String> {
    use std::process::{Command, Stdio};
    let mut command = Command::new(bin);
    command
        .args(argv)
        .stdin(Stdio::null())
        .stdout(Stdio::piped())
        .stderr(Stdio::piped())
        // 桥启动器自设组件根 PYTHONPATH;壳继承的(指向随包 myssia-src)会
        // 干扰组件自带依赖解析,剥掉(与 run_pip_install 同款纪律)。
        .env_remove("PYTHONPATH");
    if let Some(root) = myia_home_env {
        command.env("MYIA_HOME", root);
    }
    let mut child = command
        .spawn()
        .map_err(|e| {
            error_value(
                "spawn_failed",
                &format!("取钥器配置命令拉起失败({}): {}", bin.display(), e),
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
                &format!("取钥器配置命令超过 {timeout:?} 未退出,子进程已终止"),
                None,
            ));
        }
        std::thread::sleep(POLL_INTERVAL);
    }
}

/// 取钥器配置读写(get/set/clear;桥管理命令唯一通道,壳不直写桥 config.json)。
///
/// 应答:get → `{configured, path, file_exists, file_executable}`(三态真源);
/// set/clear → `{ok: true}`(前端随后重拉 get 刷新)。桥 bin 缺失 =
/// `component_missing`(与 Python 侧同码同口径);桥具名错误族原样透传。
#[tauri::command]
pub async fn wechat_key_provider(
    app: AppHandle,
    action: String,
    path: Option<String>,
) -> Result<Value, String> {
    let home = app
        .path()
        .home_dir()
        .map_err(|e| error_value("internal_error", &format!("用户 home 目录不可解析: {e}"), None))?;
    let bin = bridge_bin_path(&home);
    if !(bin.is_file() && is_executable_file(&bin)) {
        return Err(error_value(
            "component_missing",
            &format!("微信本机桥组件未安装或不可执行: {}", bin.display()),
            Some(json!({
                "fix_hint": "先到设置安装 wechat-bridge 组件(微信本机消息功能的前置),再配置取钥器"
            })),
        ));
    }
    let argv = key_provider_argv(&action, path.as_deref(), &home)?;
    // MYIA_HOME 注入规则与 spawn_sidecar 同源:显式 env 尊重原样继承
    // (自动化/自定位数据根的逃生口);未设才注入计算根,保证桥把配置
    // 写进与 sidecar 一致的数据根(桥 config.py myssia_home 同序解析)。
    let myia_home_env = if std::env::var_os("MYIA_HOME").is_some() {
        None
    } else {
        Some(crate::data_root(&app).map_err(|e| {
            error_value("internal_error", &format!("数据根不可解析: {e}"), None)
        })?)
    };
    let bin_for_thread = bin.clone();
    let joined = tauri::async_runtime::spawn_blocking(move || {
        run_bridge_with_deadline(&bin_for_thread, &argv, myia_home_env, KEY_PROVIDER_TIMEOUT)
    });
    let (exit_code, stdout, stderr) = match joined.await {
        Ok(Ok(outcome)) => outcome,
        Ok(Err(error)) => return Err(error),
        Err(err) => {
            return Err(error_value(
                "internal_error",
                &format!("取钥器配置命令线程失败: {err}"),
                None,
            ))
        }
    };
    let payload: Value = match serde_json::from_str(stdout.trim()) {
        Ok(value) => value,
        Err(_) => return Err(bridge_error_value(exit_code, &stdout, &stderr)),
    };
    let success = exit_code.unwrap_or(-1) == 0
        && payload.is_object()
        && payload.get("error").map(Value::is_null).unwrap_or(true);
    if !success {
        return Err(bridge_error_value(exit_code, &stdout, &stderr));
    }
    match action.as_str() {
        "get" => Ok(provider_state_value(&payload, &home)),
        _ => Ok(json!({"ok": true})),
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    /// argv 门:set 空路径/相对路径/未知动作结构化拒;get/clear/set 形状。
    #[test]
    fn key_provider_argv_fence() {
        let home = Path::new("/Users/tester");
        // get / clear:固定四段,--json 收尾(桥 CLI 文样同款)
        assert_eq!(
            key_provider_argv("get", None, home).unwrap(),
            vec!["localdb", "key-provider", "get", "--json"]
        );
        assert_eq!(
            key_provider_argv("clear", None, home).unwrap(),
            vec!["localdb", "key-provider", "clear", "--json"]
        );
        // set:非空 + 展开前导 ~ + 绝对路径
        assert_eq!(
            key_provider_argv("set", Some("/opt/tools/kp"), home).unwrap(),
            vec!["localdb", "key-provider", "set", "/opt/tools/kp", "--json"]
        );
        assert_eq!(
            key_provider_argv("set", Some("~/bin/kp"), home).unwrap(),
            vec!["localdb", "key-provider", "set", "/Users/tester/bin/kp", "--json"]
        );
        // 空路径(缺参/空白)拒,指引走 clear
        let err = key_provider_argv("set", Some("   "), home).unwrap_err();
        assert!(err.contains("invalid_params"), "空路径应 invalid_params: {err}");
        assert!(err.contains("清除配置"), "空路径报错应指引清除: {err}");
        assert!(key_provider_argv("set", None, home).is_err());
        // 相对路径拒(存绝对路径才无 cwd 歧义)
        let err = key_provider_argv("set", Some("bin/kp"), home).unwrap_err();
        assert!(err.contains("绝对路径"), "相对路径应拒: {err}");
        // 未知动作拒
        let err = key_provider_argv("probe", None, home).unwrap_err();
        assert!(err.contains("未知动作"), "未知动作应拒: {err}");
    }

    /// 前导 ~ 展开:恰 `~` / `~/<rest>` / 其余原样(含 ~user 不处理)。
    #[test]
    fn expand_home_leading_tilde_only() {
        let home = Path::new("/Users/tester");
        assert_eq!(expand_home("~", home), "/Users/tester");
        assert_eq!(expand_home(" ~/bin/kp ", home), "/Users/tester/bin/kp");
        assert_eq!(expand_home("/abs/kp", home), "/abs/kp");
        assert_eq!(expand_home("~other/bin", home), "~other/bin");
    }

    /// get 载荷 → 三态快照:缺键/null/空白 = 未配置;有路径如实探文件
    /// (存在+可执行位分别回填;`path` 回存原字面)。夹具 = 桥 get 应答真实
    /// 形状 `{"key_provider": {path, state, message}}`(cli.py `_emit`)。
    #[test]
    fn provider_state_maps_configured_and_missing() {
        let home = Path::new("/Users/tester");
        // 未配置三形态:key_provider 对象缺 path / path null(桥未配置态
        // 原文即 null)/ 空白串
        for payload in [
            json!({}),
            json!({"key_provider": {"path": null, "state": "unconfigured", "message": "未配置外部取钥器"}}),
            json!({"key_provider": {"path": "   "}}),
        ] {
            let state = provider_state_value(&payload, home);
            assert_eq!(state["configured"], json!(false));
            assert_eq!(state["path"], json!(null));
        }
        // 顶层 `key_provider_path`(桥 config.json 键名,**不在 get 应答里**)
        // 不识别 → 如实归未配置:桥侧形状再漂移时这里显式爆雷,不静默假绿
        let state = provider_state_value(&json!({"key_provider_path": "/opt/kp"}), home);
        assert_eq!(state["configured"], json!(false), "顶层旧形状不应被识别为已配置");
        // 文件缺失:路径指向不存在文件 → configured=true 但两 false
        let state = provider_state_value(
            &json!({"key_provider": {"path": "/myia-不存在路径/kp", "state": "missing_file", "message": "已配置但文件不存在"}}),
            home,
        );
        assert_eq!(state["configured"], json!(true));
        assert_eq!(state["file_exists"], json!(false));
        assert_eq!(state["file_executable"], json!(false));
        // 真文件:普通文件(不可执行)vs chmod +x(可执行);~ 前缀展开后探测
        let dir = tempfile::tempdir().expect("临时目录创建失败");
        let plain = dir.path().join("plain-kp");
        std::fs::write(&plain, b"#!/bin/sh\n").expect("普通文件写入失败");
        let exec = dir.path().join("exec-kp");
        std::fs::write(&exec, b"#!/bin/sh\n").expect("可执行文件写入失败");
        #[cfg(unix)]
        {
            use std::os::unix::fs::PermissionsExt;
            std::fs::set_permissions(&exec, std::fs::Permissions::from_mode(0o755))
                .expect("chmod 失败");
        }
        let state = provider_state_value(&json!({"key_provider": {"path": plain.to_str()}}), home);
        assert_eq!(state["file_exists"], json!(true));
        // unix:普通文件(无执行位)不可执行;非 unix 家族 is_file 即视为可执行
        assert_eq!(state["file_executable"], json!(!cfg!(unix)), "普通文件执行位判定");
        let state = provider_state_value(&json!({"key_provider": {"path": exec.to_str()}}), home);
        assert_eq!(state["file_exists"], json!(true));
        assert_eq!(state["file_executable"], json!(true));
        // 目录:is_file=false → 两 false(is_file 对目录本就为 false)
        let state = provider_state_value(&json!({"key_provider": {"path": dir.path().to_str()}}), home);
        assert_eq!(state["file_exists"], json!(false));
        assert_eq!(state["file_executable"], json!(false), "目录不应判可执行");
    }

    /// 桥真实 get 输出**原文**对账(评审 medium:此前单测夹具自造顶层
    /// `key_provider_path` 形状,cargo test 假绿,与桥 cli.py `_emit` 实际
    /// 输出从未对账)。四态原文逐字取自本机实跑
    /// `MYIA_HOME=<tmp> python3 -m wechat_bridge localdb key-provider get --json`
    /// (indent=1、键序 path→state→message 与 `_emit` 一致;需真实文件的
    /// 两态以 format! 代入 path,模板即实跑原文)——桥侧形状再漂移时此
    /// 用例先红。
    #[test]
    fn provider_state_bridge_real_get_output() {
        let home = Path::new("/Users/tester");
        // 未配置态原文:path=null → configured=false 四键齐断言
        let unconfigured = r#"{
 "key_provider": {
  "path": null,
  "state": "unconfigured",
  "message": "未配置外部取钥器;localdb key-provider set <path> 配置(协议:docs/wechat-keyprovider.md)"
 }
}"#;
        let payload: Value =
            serde_json::from_str(unconfigured).expect("桥未配置态原文应可解析");
        let state = provider_state_value(&payload, home);
        assert_eq!(state["configured"], json!(false));
        assert_eq!(state["path"], json!(null));
        assert_eq!(state["file_exists"], json!(false));
        assert_eq!(state["file_executable"], json!(false));

        let dir = tempfile::tempdir().expect("临时目录创建失败");
        // 已配置且可执行态原文(set 后 get 实跑形状)
        let exec = dir.path().join("kp");
        std::fs::write(&exec, b"#!/bin/sh\n").expect("可执行文件写入失败");
        #[cfg(unix)]
        {
            use std::os::unix::fs::PermissionsExt;
            std::fs::set_permissions(&exec, std::fs::Permissions::from_mode(0o755))
                .expect("chmod 失败");
        }
        let configured = format!(
            r#"{{
 "key_provider": {{
  "path": {path:?},
  "state": "configured",
  "message": "外部取钥器已配置: {path}"
 }}
}}"#,
            path = exec.display().to_string()
        );
        let payload: Value = serde_json::from_str(&configured).expect("桥已配置态原文应可解析");
        let state = provider_state_value(&payload, home);
        assert_eq!(state["configured"], json!(true));
        assert_eq!(state["path"], json!(exec.display().to_string()));
        assert_eq!(state["file_exists"], json!(true));
        assert_eq!(state["file_executable"], json!(true));

        // 已配置但文件缺失态原文(set 后删文件再 get 实跑形状)
        let missing = format!(
            r#"{{
 "key_provider": {{
  "path": {path:?},
  "state": "missing_file",
  "message": "已配置但文件不存在: {path}"
 }}
}}"#,
            path = dir.path().join("gone-kp").display().to_string()
        );
        let payload: Value = serde_json::from_str(&missing).expect("桥文件缺失态原文应可解析");
        let state = provider_state_value(&payload, home);
        assert_eq!(state["configured"], json!(true));
        assert_eq!(state["file_exists"], json!(false));
        assert_eq!(state["file_executable"], json!(false));

        // 已配置但缺可执行位态原文(set 后 chmod -x 再 get 实跑形状)
        let plain = dir.path().join("plain-kp");
        std::fs::write(&plain, b"#!/bin/sh\n").expect("普通文件写入失败");
        let not_executable = format!(
            r#"{{
 "key_provider": {{
  "path": {path:?},
  "state": "not_executable",
  "message": "已配置但文件缺可执行位: {path}"
 }}
}}"#,
            path = plain.display().to_string()
        );
        let payload: Value =
            serde_json::from_str(&not_executable).expect("桥缺执行位态原文应可解析");
        let state = provider_state_value(&payload, home);
        assert_eq!(state["configured"], json!(true));
        assert_eq!(state["file_exists"], json!(true));
        // unix:无执行位即不可执行;非 unix 家族 is_file 即视为可执行
        assert_eq!(state["file_executable"], json!(!cfg!(unix)));
    }

    /// 桥失败归一:具名 error 载荷(code/message/fix_hint)原样透传进错误
    /// 信封;非 JSON / 无 error → bridge_error 兜底带 exit 码 + stderr 尾部。
    #[test]
    fn bridge_error_passthrough_and_fallback() {
        let value = bridge_error_value(
            Some(2),
            r#"{"error":{"code":"usage","message":"路径不存在","fix_hint":"填一个存在的可执行文件"}}"#,
            "",
        );
        assert!(value.contains("\"code\":\"usage\""), "码名应透传: {value}");
        assert!(value.contains("路径不存在"));
        assert!(value.contains("填一个存在的可执行文件"), "fix_hint 应进 data: {value}");
        // 具名 error 缺 fix_hint → data 不出场
        let value = bridge_error_value(Some(1), r#"{"error":{"code":"key_unavailable","message":"未配置外部取钥器"}}"#, "");
        assert!(value.contains("\"code\":\"key_unavailable\""));
        assert!(!value.contains("fix_hint"));
        // 非 JSON stdout → 兜底 bridge_error + stderr 尾部回显
        let value = bridge_error_value(Some(1), "not-json", "line1\nline2 报错尾部");
        assert!(value.contains("\"code\":\"bridge_error\""));
        assert!(value.contains("报错尾部"), "stderr 尾部应回显: {value}");
        // stderr 尾部截断(长 stderr 只留尾段,多字节不截半)
        let long_stderr = "错".repeat(600);
        let value = bridge_error_value(Some(1), "", &long_stderr);
        let tail_count = value.matches('错').count();
        assert!(
            (STDERR_TAIL_CHARS - 2..=STDERR_TAIL_CHARS + 2).contains(&tail_count),
            "尾部应约 {STDERR_TAIL_CHARS} 字符,实测 {tail_count}"
        );
    }

    /// bin 落点:home + 钉死相对段(与 Python DEFAULT_BRIDGE_BIN 同一字面量)。
    #[test]
    fn bridge_bin_path_pins_default_location() {
        assert_eq!(
            bridge_bin_path(Path::new("/Users/tester")),
            PathBuf::from("/Users/tester/.myia/plugins/wechat-bridge/bin/wechat-bridge")
        );
    }
}
