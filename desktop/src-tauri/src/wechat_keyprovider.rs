//! 微信本机桥「取钥器」配置面(task 10-13-wechat-keyprovider B5)。
//!
//! 设置页「微信账号」卡取钥器配置行的壳侧通道:spawn **安装态**桥可执行文件
//! (`~/.myia/plugins/wechat-bridge/bin/wechat-bridge`,与
//! `myssia.wechat.push_local.DEFAULT_BRIDGE_BIN` 同一钉死路径)执行
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
//! fix_hint),与 wechat/sidecar.py `_run_bridge` 归一口径一致。
//!
//! —— C 线扩展(10-13-wechat-monitor-ui;契约 = 任务档 design §B.1-§B.3)——
//!
//! 同文件加两命令族 + 一事件流(注册锚 main.rs generate_handler):
//! - `wechat_key_status`:spawn 桥 `localdb key-status --json`(§A.1 三态
//!   真源 ready/stale/missing,恒 exit 0),应答 = `key_status` 对象**直转**
//!   (wire snake_case 原样)。
//! - `wechat_key_acquire {force?}` + `wechat_key_acquire_cancel`(无参):
//!   取钥编排。spawn 桥 `localdb key-acquire --json [--force]
//!   --timeout-hint 600`;stdout **逐行读逐行发**(progress 行 → Tauri 事件
//!   `wechat-key-acquire`,载荷 `{seq, phase, detail}`);单飞锁(在途第二
//!   次 acquire 报 `acquire_in_progress`);壳帽 900s(超帽 kill 用户态链
//!   判 failed「获取超时」);取消 = 组信号停用户态树 + 落哨兵
//!   `<数据根>/wechat-localdb/cancel.keyacquire`(provider 的 root 段经
//!   osascript 提权,用户态杀不动——哨兵由部署件轮询自杀,§C)+ cancelled
//!   终态事件(终态事件**唯一发射点在取消方**,编排循环见旗标静默收
//!   cancelled,不双发)。
//! - progress 行的阶段映射:桥只转印不归类(§A.2「原样转印」),壳侧三档
//!   ——显式 `phase` 字段(v1.1 取钥器自报,最准)> message 关键词表(锚
//!   §C 部署件法定消息串)> 沿用上一阶段(初始 password = §C 序列首阶段)。
//!   终态信封取**首条**,其后行丢弃(镜像 provider 协议 §4「多条 result 取
//!   首条」)。
//! - 红线延续:provider result 的 **keys 密钥映射全程不读不发不上日志**,
//!   事件/返回值只碰 result/db_count/error 形状级字段;progress 的 message
//!   是协议法定人话,原样作 detail(§B.3)。

use std::io::{BufRead, BufReader, Read};
use std::path::{Path, PathBuf};
use std::sync::atomic::{AtomicBool, AtomicU64, Ordering};
use std::sync::{mpsc, Arc, Mutex};
use std::time::{Duration, Instant};

use serde::Serialize;
use serde_json::{json, Map, Value};
use tauri::{AppHandle, Emitter, Manager};

/// 桥 bin 缺省落点(相对用户 home;与 DEFAULT_BRIDGE_BIN 同一钉死字面量,
/// Rust 侧无 `~` 展开原语故拆 home + 相对段)。装到别处时品类 YAML push 条目
/// `wechat_bridge_bin` 覆写只作用于发送通道——本配置面与协议面
/// (wechat/sidecar)同用缺省落点,不给 UI 留任意路径执行缝。
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

/// 桥失败归一(与 wechat/sidecar `_run_bridge` 同口径):stdout 单 JSON
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

// ---------------------------------------------------------------------------
// 密钥状态查询 + 取钥编排(10-13-wechat-monitor-ui C 线;design §B.1-§B.3)
// ---------------------------------------------------------------------------

/// 取钥编排进度事件名(design §B.3;载荷 `{seq, phase, detail}`,phase ∈
/// password|attach|wait_relogin|derive|done|failed|cancelled)。**与前端成对**:
/// `desktop/ui-src/src/screens/settings/wechat-keyprovider-api.ts` 的
/// `KEY_ACQUIRE_EVENT_NAME` 常量同值(注释互指;改其一必同步另一)。
pub const KEY_ACQUIRE_EVENT: &str = "wechat-key-acquire";

/// 取钥请求的超时提示秒数(design §2/R2.3 三处统一:hint 600 / 桥内帽
/// clamp(120,1800) / 壳帽 900;桥侧钳制语义 = 协议 v1.1,§A.2)。
const KEY_ACQUIRE_TIMEOUT_HINT_SECONDS: u64 = 600;
/// 壳侧兜底帽(§B.2:读行超时或总时长超帽 → kill 用户态链 + 判 failed
/// 「超时」;>hint,防桥自身超时后壳挂死)。
const KEY_ACQUIRE_SHELL_CAP: Duration = Duration::from_secs(900);
/// 取消/超帽后组信号优雅宽限(SIGTERM → 宽限轮询 → SIGKILL 组;sidecar
/// run.cancel「SIGTERM→5s→SIGKILL」同款纪律,pyenv_components 服务停同族)。
const ACQUIRE_STOP_GRACE: Duration = Duration::from_secs(5);
/// key-status 命令帽:三态抽样验真秒级(§A.1「1-3 把/次秒级」)+ db 根
/// 探测余量,60s = 桥命令族帽(wechat.push_local DEFAULT_BRIDGE_TIMEOUT_SECONDS
/// 同值;30s 配置面帽不够盖盘 IO 慢顶)。
const KEY_STATUS_TIMEOUT: Duration = Duration::from_secs(60);
/// 取消哨兵文件(相对数据根;§B.2 取消动作②:部署件 root 段每 2s 轮询,
/// 见即自杀+自清——root 段用户态杀不动,哨兵是它唯一的取消通路)。
const CANCEL_SENTINEL_REL: &str = "wechat-localdb/cancel.keyacquire";

/// 取钥编排阶段(§B.3 **机器枚举**;上屏词走前端词表 §D.3,壳侧不造人话)。
#[derive(Clone, Copy, PartialEq, Eq, Debug, Serialize)]
#[serde(rename_all = "snake_case")]
pub enum KeyAcquirePhase {
    Password,
    Attach,
    WaitRelogin,
    Derive,
    Done,
    Failed,
    Cancelled,
}

impl KeyAcquirePhase {
    /// 机器词面解析(progress 行显式 `phase` 字段按此认;§B.3 枚举逐字)。
    fn parse(text: &str) -> Option<Self> {
        Some(match text {
            "password" => Self::Password,
            "attach" => Self::Attach,
            "wait_relogin" => Self::WaitRelogin,
            "derive" => Self::Derive,
            "done" => Self::Done,
            "failed" => Self::Failed,
            "cancelled" => Self::Cancelled,
            _ => return None,
        })
    }
}

/// `wechat-key-acquire` 事件载荷(§B.3:`{seq, phase, detail}`;detail =
/// provider progress 的 message 原文——协议法定人话;终态事件 done/
/// cancelled 为 null、failed 为人话错误。detail 恒在场(null 形态稳定,
/// 前端不必判键存在)。
#[derive(Clone, Debug, Serialize)]
pub struct KeyAcquireEvent {
    pub seq: u64,
    pub phase: KeyAcquirePhase,
    pub detail: Option<String>,
}

/// 取钥编排单飞锁 + 事件序号分配器(§B.2 简化定案:**单飞锁无参 cancel**,
/// 多窗并发取钥本就不该发生,在途第二次 acquire 直接拒)。
pub struct KeyAcquireManager {
    /// 在途槽(None = 空闲;占坑在 spawn 成功后连 pgid 一起写入)。
    in_flight: Mutex<Option<KeyAcquireInFlight>>,
    /// 事件 seq(**进程级**单调不重置:跨 run 也续增——前端「丢乱序旧包」
    /// 的判据不被新 run 重置破坏)。
    seq: AtomicU64,
}

/// 在途槽载荷。
struct KeyAcquireInFlight {
    /// 取消旗标(取消方置位;编排循环见位即静默收 cancelled,不发事件——
    /// 终态事件唯一发射点在取消方,不双发)。
    cancel_requested: Arc<AtomicBool>,
    /// 进程组 id(spawn 恒 process_group(0) ⇒ pgid == child pid;组信号
    /// 覆盖桥→provider 用户态子孙树)。
    pgid: u32,
}

/// 壳侧全局单飞槽(两命令共用;进程单实例[flock/单实例插件] ⇒ 全局即会话级)。
static KEY_ACQUIRE: KeyAcquireManager = KeyAcquireManager {
    in_flight: Mutex::new(None),
    seq: AtomicU64::new(0),
};

impl KeyAcquireManager {
    /// 下一个事件 seq(从 1 起,进程级单调)。
    fn next_seq(&self) -> u64 {
        self.seq.fetch_add(1, Ordering::SeqCst) + 1
    }
}

#[cfg(test)]
impl KeyAcquireManager {
    /// 测试专用独立实例(不碰全局槽,单测并行互不干扰)。
    fn new() -> Self {
        Self {
            in_flight: Mutex::new(None),
            seq: AtomicU64::new(0),
        }
    }

    /// 在途占坑探测(测试等 spawn 落槽用)。
    fn occupied(&self) -> bool {
        self.in_flight.lock().unwrap().is_some()
    }
}

/// 取钥编排终态(§B.2 命令返回值:`{result: "ok"|"failed"|"cancelled",
/// db_count?, error?}`;缺省键不出场)。
#[derive(Clone, Debug, PartialEq, Eq)]
struct AcquireOutcome {
    result: &'static str,
    db_count: Option<u64>,
    error: Option<String>,
}

impl AcquireOutcome {
    fn ok(db_count: Option<u64>) -> Self {
        Self {
            result: "ok",
            db_count,
            error: None,
        }
    }

    fn failed(error: impl Into<String>) -> Self {
        Self {
            result: "failed",
            db_count: None,
            error: Some(error.into()),
        }
    }

    fn cancelled() -> Self {
        Self {
            result: "cancelled",
            db_count: None,
            error: None,
        }
    }

    /// 终态事件形(§B.3:done/failed/cancelled;failed 的 detail = 人话错误)。
    fn terminal_event(&self) -> (KeyAcquirePhase, Option<String>) {
        match self.result {
            "ok" => (KeyAcquirePhase::Done, None),
            "cancelled" => (KeyAcquirePhase::Cancelled, None),
            _ => (KeyAcquirePhase::Failed, self.error.clone()),
        }
    }

    /// §B.2 返回值形态(wire:None 键不出场)。
    fn to_value(&self) -> Value {
        let mut object = Map::new();
        object.insert("result".into(), json!(self.result));
        if let Some(count) = self.db_count {
            object.insert("db_count".into(), json!(count));
        }
        if let Some(error) = &self.error {
            object.insert("error".into(), json!(error));
        }
        Value::Object(object)
    }
}

/// progress message → 机器阶段的关键词表(锚 §C 部署件法定消息串;检查序
/// password → attach → wait_relogin → derive,复合消息按链路后段阶段胜)。
/// 未命中 → 沿用上一阶段(步进条不被杂音打断)。
fn classify_progress_phase(message: &str, fallback: KeyAcquirePhase) -> KeyAcquirePhase {
    let lower = message.to_lowercase();
    if lower.contains("密码") || lower.contains("password") {
        KeyAcquirePhase::Password
    } else if lower.contains("连接") || lower.contains("挂载") || lower.contains("attach") {
        KeyAcquirePhase::Attach
    } else if lower.contains("重新登录")
        || lower.contains("退出登录")
        || lower.contains("扫码")
        || lower.contains("relogin")
    {
        KeyAcquirePhase::WaitRelogin
    } else if lower.contains("验证")
        || lower.contains("派生")
        || lower.contains("数据库")
        || lower.contains("derive")
        || lower.contains("verif")
    {
        KeyAcquirePhase::Derive
    } else {
        fallback
    }
}

/// 桥 stdout 行处理状态机(纯;spawn 读行循环的逐行转译核心)。
///
/// 行形(§A.2):provider progress 行由桥**原样转印**(`{"type":"progress",
/// "message","level"}`);终态为桥自身 `--json` 信封(`{"key_acquire":…}` /
/// `{"error":…}`)。progress → 阶段映射三档:显式 `phase` 字段(v1.1 取钥器
/// 自报,最准)> 关键词表 > 沿用上一阶段(初始 password = §C 序列首阶段)。
/// 终态信封取**首条**,其后信封行丢弃(镜像 provider 协议 §4「多条 result
/// 取首条」);杂行(空行/非 JSON/非对象)如实计数忽略,不炸不重试。
struct AcquireLineMachine {
    last_phase: KeyAcquirePhase,
    envelope: Option<Value>,
    ignored_lines: usize,
}

impl AcquireLineMachine {
    fn new() -> Self {
        Self {
            last_phase: KeyAcquirePhase::Password,
            envelope: None,
            ignored_lines: 0,
        }
    }

    /// 喂一行桥 stdout:progress 行返回应发事件(phase, message 原文);
    /// 终态信封行收进 `self.envelope` 并返回 None;杂行同样 None(已计数)。
    fn feed(&mut self, line: &str) -> Option<(KeyAcquirePhase, Option<String>)> {
        let trimmed = line.trim();
        if trimmed.is_empty() {
            self.ignored_lines += 1;
            return None;
        }
        let Ok(parsed) = serde_json::from_str::<Value>(trimmed) else {
            self.ignored_lines += 1;
            return None;
        };
        let Some(object) = parsed.as_object() else {
            self.ignored_lines += 1;
            return None;
        };
        if object.get("type").and_then(Value::as_str) == Some("progress") {
            let message = object
                .get("message")
                .and_then(Value::as_str)
                .map(str::to_string);
            let phase = object
                .get("phase")
                .and_then(Value::as_str)
                .and_then(KeyAcquirePhase::parse)
                .unwrap_or_else(|| {
                    classify_progress_phase(message.as_deref().unwrap_or(""), self.last_phase)
                });
            self.last_phase = phase;
            return Some((phase, message));
        }
        if self.envelope.is_none()
            && (object.contains_key("key_acquire") || object.contains_key("error"))
        {
            self.envelope = Some(parsed);
        } else {
            self.ignored_lines += 1;
        }
        None
    }
}

/// 取正整数 u64(0/非数 → None;db_count 形状守门——ok 面 0 库无意义,
/// 缺数让前端回落状态查询)。
fn positive_u64(value: Option<&Value>) -> Option<u64> {
    value.and_then(Value::as_u64).filter(|count| *count > 0)
}

/// 终态分类(纯):桥终态信封 + 退出码 + stderr 尾部 → §B.2 返回值形态。
/// 信封优先于退出码(桥具名 error 族的人话透传,§F);无信封按退出码兜底
/// (0 = 未返回结果;非 0 = 异常退出;None = 信号终止)。
fn classify_acquire_outcome(
    envelope: Option<&Value>,
    exit_code: Option<i32>,
    stderr_note: &str,
) -> AcquireOutcome {
    if let Some(payload) = envelope {
        if let Some(acquire) = payload.get("key_acquire").and_then(Value::as_object) {
            let result = acquire
                .get("result")
                .and_then(Value::as_str)
                .unwrap_or("");
            return match result {
                // already_ready = 桥短路(缓存抽样验真通过的合法即返,§A.2)
                "ok" | "already_ready" | "ready" => {
                    AcquireOutcome::ok(positive_u64(acquire.get("db_count")))
                }
                _ => AcquireOutcome::failed(
                    acquire
                        .get("error")
                        .and_then(Value::as_str)
                        .map(str::to_string)
                        .unwrap_or_else(|| format!("取钥未成功(result={result})")),
                ),
            };
        }
        if let Some(error) = payload.get("error").and_then(Value::as_object) {
            let message = error
                .get("message")
                .and_then(Value::as_str)
                .unwrap_or("桥返回失败(无说明)");
            return AcquireOutcome::failed(message.to_string());
        }
    }
    let suffix = if stderr_note.is_empty() {
        String::new()
    } else {
        format!(";stderr 尾部: {stderr_note}")
    };
    match exit_code {
        Some(0) => AcquireOutcome::failed(format!("桥未返回结果(stdout 无终态信封){suffix}")),
        Some(code) => AcquireOutcome::failed(format!("桥异常退出(exit={code}){suffix}")),
        None => AcquireOutcome::failed(format!("桥被信号终止,未返回终态{suffix}")),
    }
}

/// 取消哨兵路径(§B.2:`<数据根>/wechat-localdb/cancel.keyacquire`)。
fn cancel_sentinel_path(data_root: &Path) -> PathBuf {
    data_root.join(CANCEL_SENTINEL_REL)
}

/// 落取消哨兵(内容 = 落盘时刻 unix 秒,部署件只看在场性;父目录预建)。
fn write_cancel_sentinel(data_root: &Path) -> std::io::Result<()> {
    let path = cancel_sentinel_path(data_root);
    if let Some(parent) = path.parent() {
        std::fs::create_dir_all(parent)?;
    }
    let stamped = std::time::SystemTime::now()
        .duration_since(std::time::UNIX_EPOCH)
        .map(|elapsed| elapsed.as_secs())
        .unwrap_or(0);
    std::fs::write(&path, format!("{stamped}\n"))
}

/// 取钥编排 argv(纯;§A.2 契约写死:`--json` 前置、`--force` 可选、
/// `--timeout-hint` 恒 600 = design §2 三处统一的请求值)。
fn key_acquire_argv(force: bool) -> Vec<String> {
    let mut argv = vec![
        "localdb".to_string(),
        "key-acquire".to_string(),
        "--json".to_string(),
    ];
    if force {
        argv.push("--force".to_string());
    }
    argv.push("--timeout-hint".to_string());
    argv.push(KEY_ACQUIRE_TIMEOUT_HINT_SECONDS.to_string());
    argv
}

/// 超帽人话(§F 钉死「获取超时(15 分钟),可重试」;分钟数由帽折算,
/// 900s 壳帽恰为 15 分钟)。
fn timeout_error_message(cap: Duration) -> String {
    let minutes = (cap.as_secs() + 59) / 60;
    format!("获取超时({minutes} 分钟),可重试")
}

// —— 用户态进程树停(组信号;pyenv_components 服务停同族三件)——

/// 优雅停取钥链用户态段:SIGTERM 进程组 + 直接 pid 兜底(pgid == pid,
/// spawn 恒 process_group(0);组信号覆盖桥→provider 用户态子孙树——
/// provider 的 root 段经 osascript 提权在组外,归哨兵机制自理)。
#[cfg(unix)]
fn terminate_acquire_group(pgid: u32) {
    unsafe {
        libc::kill(-(pgid as libc::pid_t), libc::SIGTERM);
        libc::kill(pgid as libc::pid_t, libc::SIGTERM);
    }
}

/// 强杀兜底(SIGKILL 组 + 直接 pid;同 terminate 双路,对组长幂等无害)。
#[cfg(unix)]
fn force_kill_acquire_group(pgid: u32) {
    unsafe {
        libc::kill(-(pgid as libc::pid_t), libc::SIGKILL);
        libc::kill(pgid as libc::pid_t, libc::SIGKILL);
    }
}

/// 组内存活探测(kill(-pgid, 0);ESRCH 才是确凿不在,EPERM 按在处理)。
#[cfg(unix)]
fn acquire_group_alive(pgid: u32) -> bool {
    unsafe {
        if libc::kill(-(pgid as libc::pid_t), 0) == 0 {
            return true;
        }
        !matches!(
            std::io::Error::last_os_error().raw_os_error(),
            Some(libc::ESRCH)
        )
    }
}

/// windows:taskkill 树杀(优雅/强杀无区分;pyenv_components 服务停同款
/// 简化——微信桥本身 macOS-only,本分支只为编译完整)。
#[cfg(windows)]
fn terminate_acquire_group(pgid: u32) {
    let _ = std::process::Command::new("taskkill")
        .args(["/PID", &pgid.to_string(), "/T", "/F"])
        .output();
}

/// 组停收敛:SIGTERM → 宽限轮询 → SIGKILL(unix;windows 单发 taskkill)。
/// pgid == 0 = 占位形态(spawn 未成)直接跳过——组信号 -0 会误伤自家进程组。
fn stop_acquire_group(pgid: u32) {
    if pgid == 0 {
        return;
    }
    terminate_acquire_group(pgid);
    #[cfg(unix)]
    {
        let deadline = Instant::now() + ACQUIRE_STOP_GRACE;
        while Instant::now() < deadline && acquire_group_alive(pgid) {
            std::thread::sleep(POLL_INTERVAL);
        }
        if acquire_group_alive(pgid) {
            log::warn!("desktop: 取钥链用户态段优雅停超时,升级 SIGKILL 进程组 -{pgid}");
            force_kill_acquire_group(pgid);
        }
    }
}

/// 限时收割:EOF 后进程垂死,try_wait 轮询至宽限;仍在则 kill+wait 收尾
/// (kill 后 wait 必然即返;封顶防挂)。
fn reap_child(child: &mut std::process::Child) -> Option<std::process::ExitStatus> {
    let deadline = Instant::now() + ACQUIRE_STOP_GRACE + POLL_INTERVAL;
    loop {
        if let Ok(Some(status)) = child.try_wait() {
            return Some(status);
        }
        if Instant::now() >= deadline {
            let _ = child.kill();
            return child.wait().ok();
        }
        std::thread::sleep(POLL_INTERVAL);
    }
}

/// 取消核心(§B.2 取消动作三连;命令面/单测共用):
/// ① take 在途槽(空 = 无在途,`{ok:false}` 如实回,不造事件)
/// ② 置取消旗标 + 停用户态进程树(组信号 SIGTERM→宽限→SIGKILL)
/// ③ 落哨兵 + 发射 cancelled 终态事件(**终态事件唯一发射点**)。
/// 哨兵写失败不撤取消(用户态链已停、旗标已置):降级记日志,root 段按
/// 自身超时自清(§2「最迟自清窗 = 其 timeout」),返回值携带 note 如实披露。
fn request_cancel<F>(
    state: &KeyAcquireManager,
    data_root: &Path,
    mut emit: F,
) -> Result<Value, String>
where
    F: FnMut(u64, KeyAcquirePhase, Option<&str>),
{
    let slot = state.in_flight.lock().unwrap().take();
    let Some(slot) = slot else {
        return Ok(json!({"ok": false, "note": "当前没有进行中的密钥获取"}));
    };
    slot.cancel_requested.store(true, Ordering::SeqCst);
    stop_acquire_group(slot.pgid);
    let sentinel_note = match write_cancel_sentinel(data_root) {
        Ok(()) => None,
        Err(err) => {
            log::error!(
                "desktop: 取消哨兵写入失败({err});提权段将按自身超时自清(最迟 10 分钟)"
            );
            Some("取消哨兵写入失败,提权段将按自身超时自清(最迟 10 分钟)".to_string())
        }
    };
    emit(state.next_seq(), KeyAcquirePhase::Cancelled, None);
    log::info!("desktop: 微信取钥编排已取消(用户态链已停,哨兵已落;提权段由部署件轮询自杀)");
    Ok(match sentinel_note {
        None => json!({"ok": true}),
        Some(note) => json!({"ok": true, "note": note}),
    })
}

/// 取钥编排核心(阻塞;命令面经 spawn_blocking 包裹,单测直跑假桥)。
///
/// 链路:spawn 桥 `localdb key-acquire --json [--force] --timeout-hint 600`
/// (unix 新进程组)→ stdout 逐行读(**读行超时 = 剩余帽**,总时长超帽同门)
/// → progress 行转 emit 回调(事件发射归调用方:命令面发 Tauri 事件,单测
/// 收进 Vec)→ 终态信封分类 → §B.2 返回值。取消 = 取消方 take 槽 + 置旗标
/// + 发射 cancelled 终态事件;本循环见旗标或失槽即**静默**收 cancelled
/// (终态事件不双发)。超帽 = stop_acquire_group + failed「获取超时」。
///
/// 红线:provider result 的 keys 密钥映射全程不读不发——只碰
/// result/db_count/error 三个形状级字段;事件 detail 只携 provider 人话。
fn run_key_acquire<F>(
    bin: &Path,
    force: bool,
    myia_home_env: Option<PathBuf>,
    state: &KeyAcquireManager,
    cap: Duration,
    mut emit: F,
) -> Result<AcquireOutcome, String>
where
    F: FnMut(u64, KeyAcquirePhase, Option<&str>),
{
    use std::process::{Command, Stdio};
    let argv = key_acquire_argv(force);
    let cancel_flag = Arc::new(AtomicBool::new(false));
    let mut command = Command::new(bin);
    command
        .args(&argv)
        .stdin(Stdio::null())
        .stdout(Stdio::piped())
        .stderr(Stdio::piped())
        // 桥启动器自设组件根 PYTHONPATH;壳继承的会干扰组件依赖解析
        // (B5 同款纪律)。
        .env_remove("PYTHONPATH");
    if let Some(root) = &myia_home_env {
        command.env("MYIA_HOME", root);
    }
    #[cfg(unix)]
    {
        use std::os::unix::process::CommandExt;
        // 独立进程组:取消/超帽的组信号可达桥→provider 用户态子孙树,
        // 且不误伤壳自身会话。
        command.process_group(0);
    }
    // 单飞锁 + spawn 同临界区:占坑检查、spawn、pgid 落槽一气呵成(锁内
    // fork/exec 微秒级;cancel 面只 take 不嵌套锁,无死锁面)。
    let mut child = {
        let mut guard = state.in_flight.lock().unwrap();
        if guard.is_some() {
            return Err(error_value(
                "acquire_in_progress",
                "已有一次密钥获取在进行中",
                None,
            ));
        }
        let child = command.spawn().map_err(|e| {
            error_value(
                "spawn_failed",
                &format!("密钥获取命令拉起失败({}): {e}", bin.display()),
                None,
            )
        })?;
        *guard = Some(KeyAcquireInFlight {
            cancel_requested: cancel_flag.clone(),
            pgid: child.id(),
        });
        child
    };
    log::info!("desktop: 微信取钥编排启动(force={force},壳帽 {cap:?})");
    let stdout_pipe = child.stdout.take().expect("piped stdout 句柄");
    let stderr_pipe = child.stderr.take().expect("piped stderr 句柄");
    // stdout 读行线程(阻塞读 → channel;EOF 即退)。
    let (tx, rx) = mpsc::channel::<String>();
    let reader = std::thread::spawn(move || {
        let reader = BufReader::new(stdout_pipe);
        for line in reader.lines() {
            match line {
                Ok(text) => {
                    if tx.send(text).is_err() {
                        break; // 接收侧已收摊(超帽/取消先到)
                    }
                }
                Err(_) => break,
            }
        }
    });
    // stderr 旁路线程:900s 面上不排干会堵死子进程管道(§A.2 桥只记一行
    // 摘要,防御性留尾 2×STDERR_TAIL_CHARS 环替)。
    let stderr_note = Arc::new(Mutex::new(String::new()));
    let stderr_sink = stderr_note.clone();
    let stderr_reader = std::thread::spawn(move || {
        let mut reader = BufReader::new(stderr_pipe);
        let mut line = String::new();
        loop {
            line.clear();
            match reader.read_line(&mut line) {
                Ok(0) | Err(_) => break,
                Ok(_) => {
                    let mut note = stderr_sink.lock().unwrap();
                    note.push_str(&line);
                    let chars: Vec<char> = note.chars().collect();
                    if chars.len() > STDERR_TAIL_CHARS * 4 {
                        let start = chars.len() - STDERR_TAIL_CHARS * 2;
                        *note = chars[start..].iter().collect();
                    }
                }
            }
        }
    });
    let deadline = Instant::now() + cap;
    let mut machine = AcquireLineMachine::new();
    let mut timed_out = false;
    loop {
        if cancel_flag.load(Ordering::SeqCst) {
            break; // 取消方接管:终态事件归它
        }
        let remaining = deadline.saturating_duration_since(Instant::now());
        if remaining.is_zero() {
            timed_out = true;
            break;
        }
        match rx.recv_timeout(remaining) {
            Ok(line) => {
                if cancel_flag.load(Ordering::SeqCst) {
                    break;
                }
                if let Some((phase, detail)) = machine.feed(&line) {
                    emit(state.next_seq(), phase, detail.as_deref());
                }
            }
            Err(mpsc::RecvTimeoutError::Timeout) => {
                timed_out = true;
                break;
            }
            Err(mpsc::RecvTimeoutError::Disconnected) => break, // stdout EOF
        }
    }
    if timed_out {
        stop_acquire_group(child.id());
    }
    let exit_code = reap_child(&mut child).and_then(|status| status.code());
    let _ = reader.join();
    let _ = stderr_reader.join();
    let stderr_tail_now = stderr_tail(&stderr_note.lock().unwrap());
    // 终态归属:槽仍在(未被取消方 take)→ 本循环拥有终态发射权。
    let we_own_terminal = {
        let mut guard = state.in_flight.lock().unwrap();
        let mine = guard
            .as_ref()
            .map(|slot| Arc::ptr_eq(&slot.cancel_requested, &cancel_flag))
            .unwrap_or(false);
        if mine {
            *guard = None;
        }
        mine
    };
    if !we_own_terminal {
        // 取消方已发射 cancelled 终态事件;本命令静默收 cancelled(取钥结果
        // 以状态查询为准,用户故事 = 已取消)。
        log::info!("desktop: 微信取钥编排被取消(终态事件由取消方发射)");
        return Ok(AcquireOutcome::cancelled());
    }
    let outcome = if timed_out {
        AcquireOutcome::failed(timeout_error_message(cap))
    } else {
        classify_acquire_outcome(
            machine.envelope.as_ref(),
            exit_code,
            stderr_tail_now.trim(),
        )
    };
    let (phase, detail) = outcome.terminal_event();
    emit(state.next_seq(), phase, detail.as_deref());
    log::info!(
        "desktop: 微信取钥编排终态: result={} db_count={:?}",
        outcome.result,
        outcome.db_count
    );
    Ok(outcome)
}

/// 三命令共用前置(纯胶水):home/bin 探测(component_missing 同 B5 口径)
/// + MYIA_HOME 注入决策(spawn_sidecar 同规则:显式 env 尊重不夺权,未设
/// 才注入计算根——桥把密钥缓存/配置落在与 sidecar 一致的数据根)。
fn resolve_bridge_context(app: &AppHandle) -> Result<(PathBuf, Option<PathBuf>), String> {
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
                "fix_hint": "先到设置安装 wechat-bridge 组件(微信本机消息功能的前置),再进行密钥操作"
            })),
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

/// 桥 key-status 应答 → §B.1 直转(取 `key_status` 内层对象原样返回,wire
/// snake_case 不改形;缺对象/非对象 = 桥侧形状漂移,结构化报不静默)。
fn key_status_value(payload: &Value) -> Result<Value, String> {
    match payload.get("key_status").filter(|inner| inner.is_object()) {
        Some(inner) => Ok(inner.clone()),
        None => Err(error_value(
            "bridge_error",
            "key-status 应答缺 key_status 对象(桥侧形状漂移)",
            None,
        )),
    }
}

/// 密钥状态查询(design §B.1):spawn 桥 `localdb key-status --json`
/// (§A.1 三态真源:ready/stale/missing 皆正常态,恒 exit 0),应答 =
/// `key_status` 对象**直转**。钥内容不出现在本面(形状级证据判例:只有
/// state/db_count/acquired_at/wechat_version/verdict_note 五键)。
#[tauri::command]
pub async fn wechat_key_status(app: AppHandle) -> Result<Value, String> {
    let (bin, myia_home_env) = resolve_bridge_context(&app)?;
    let argv = vec!["localdb".into(), "key-status".into(), "--json".into()];
    let joined = tauri::async_runtime::spawn_blocking(move || {
        run_bridge_with_deadline(&bin, &argv, myia_home_env, KEY_STATUS_TIMEOUT)
    });
    let (exit_code, stdout, stderr) = match joined.await {
        Ok(Ok(outcome)) => outcome,
        Ok(Err(error)) => return Err(error),
        Err(err) => {
            return Err(error_value(
                "internal_error",
                &format!("密钥状态命令线程失败: {err}"),
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
    key_status_value(&payload)
}

/// 取钥编排(design §B.2:异步命令 + `wechat-key-acquire` 事件流)。
/// 进度 = 桥 stdout 逐行读逐行发(progress 行 → `{seq, phase, detail}`);
/// 返回值 = 终态 `{result: "ok"|"failed"|"cancelled", db_count?, error?}`。
/// 单飞:同会话只允许一个 acquire 在途,第二次直接 `acquire_in_progress`
/// 拒(取消无参 = `wechat_key_acquire_cancel`)。壳帽 900s(超帽 kill
/// 用户态链判 failed「获取超时」)。`force` 透传(ready 态「重新获取」
/// 场景:不 force 桥短路 already_ready,失效钥匙永远空转——grill 决议②)。
#[tauri::command]
pub async fn wechat_key_acquire(app: AppHandle, force: Option<bool>) -> Result<Value, String> {
    let (bin, myia_home_env) = resolve_bridge_context(&app)?;
    let cap = KEY_ACQUIRE_SHELL_CAP;
    let emit_app = app.clone();
    let joined = tauri::async_runtime::spawn_blocking(move || {
        let emit = move |seq: u64, phase: KeyAcquirePhase, detail: Option<&str>| {
            let _ = emit_app.emit(
                KEY_ACQUIRE_EVENT,
                KeyAcquireEvent {
                    seq,
                    phase,
                    detail: detail.map(str::to_string),
                },
            );
        };
        run_key_acquire(
            &bin,
            force.unwrap_or(false),
            myia_home_env,
            &KEY_ACQUIRE,
            cap,
            emit,
        )
    });
    match joined.await {
        Ok(Ok(outcome)) => Ok(outcome.to_value()),
        Ok(Err(error)) => Err(error),
        Err(err) => Err(error_value(
            "internal_error",
            &format!("取钥编排线程失败: {err}"),
            None,
        )),
    }
}

/// 取消进行中的取钥编排(§B.2 简化定案:单飞锁无参 cancel)。三连:停
/// 用户态进程树(组信号)→ 落哨兵(提权段轮询自杀)→ cancelled 终态事件。
/// 无在途 → `{ok:false}` 如实回(不造事件;取消钮只在 running 态可点,
/// 此形态 = UI 竞态兜底)。不 spawn 桥,故无 bin 探测前置。
#[tauri::command]
pub async fn wechat_key_acquire_cancel(app: AppHandle) -> Result<Value, String> {
    let data_root = crate::data_root(&app).map_err(|e| {
        error_value("internal_error", &format!("数据根不可解析: {e}"), None)
    })?;
    let emit_app = app.clone();
    let joined = tauri::async_runtime::spawn_blocking(move || {
        let emit = move |seq: u64, phase: KeyAcquirePhase, detail: Option<&str>| {
            let _ = emit_app.emit(
                KEY_ACQUIRE_EVENT,
                KeyAcquireEvent {
                    seq,
                    phase,
                    detail: detail.map(str::to_string),
                },
            );
        };
        request_cancel(&KEY_ACQUIRE, &data_root, emit)
    });
    match joined.await {
        Ok(result) => result,
        Err(err) => Err(error_value(
            "internal_error",
            &format!("取钥取消线程失败: {err}"),
            None,
        )),
    }
}

// ---------------------------------------------------------------------------
// 取钥器部署件「一键安装」(E2;design §C 部署位/D3 装机后首用引导)
// ---------------------------------------------------------------------------

/// 部署件四件套(E1 产出;入口件 keyprovider-lldb.sh,余为随行运行件)。
const KEYPROVIDER_BUNDLE_FILES: [&str; 4] = [
    "keyprovider-lldb.sh",
    "keyprovider_wrap.py",
    "keyprovider_root.sh",
    "wcdb_key_tool_macos.py",
];
/// 入口件(源目录有效性判定 = 它在场;缺它即「源不在」)。
const KEYPROVIDER_BUNDLE_ENTRY: &str = "keyprovider-lldb.sh";
/// 安装落点(相对数据根;§C 部署位 `<数据根>/wechat-localdb/bin/`,700)。
const KEYPROVIDER_BIN_REL: &str = "wechat-localdb/bin";

/// 安装源候选(纯函数):显式 env 覆盖(`MYIA_KEYPROVIDER_BUNDLE`)最高优 →
/// E1 出产暂存目录。源 = §C 改造后的部署件束(攻坚档 tools/ 三件打包适配的
/// 产物,E1 出产到 /tmp/wxkey-deploy 仓外不进 git);攻坚档原始三件非协议
/// 形态,不作拷贝源(开发机自定束目录走 env 覆盖)。
fn keyprovider_bundle_candidates(env_override: Option<PathBuf>) -> Vec<PathBuf> {
    let mut candidates = Vec::new();
    if let Some(dir) = env_override {
        candidates.push(dir);
    }
    candidates.push(PathBuf::from("/tmp/wxkey-deploy"));
    candidates
}

/// 束源解析结果三分支:在场且属主链可信 / 在场但属主链不可信(拒并提示,
/// 不静默回落下一候选——env 显式指定的束被静默替换更危险)/ 不在场。
enum ResolvedBundleSource {
    /// 在场有效(束目录,在场文件清单)。
    Found(PathBuf, Vec<String>),
    /// 在场但属主链校验未过(人话拒因,inspect 透出 + install 结构化拒)。
    Unsafe(String),
    /// 所有候选均缺入口件。
    Missing,
}

/// 单级目录属主可信判定(纯函数,单测锚):属主 = 当前用户,或 root 属主
/// 且他人不可写(755 形态)或世界可写但带 sticky(1777 形态——/tmp、
/// /var、/var/folders 均在此列)。其余(他人属主目录)不可信。
#[cfg(unix)]
fn bundle_level_owner_trusted(owner_uid: u32, mode: u32, me: u32) -> bool {
    // 0o002 = S_IWOTH(他人可写);0o1000 = S_ISVTX(sticky;POSIX 固定
    // 位值,libc 常量在 macOS 侧是 u16 与 mode 的 u32 不混算,故用字面量)。
    owner_uid == me || (owner_uid == 0 && (!(mode & 0o002 != 0) || (mode & 0o1000 != 0)))
}

/// 束源目录属主链校验(评审修③:多用户机器防投毒)——/tmp 世界可写,其他
/// 本地用户可预建束目录投放恶意四件,「一键安装」会以受害者身份把它 cp 进
/// 私有 bin、chmod 700 并自动设为取钥器,后续 acquire 即以受害者身份执行。
/// 规则:束目录及其每级父目录(上行到根)均须通过
/// [`bundle_level_owner_trusted`];任一级不可信即 Err(人话拒因)。
#[cfg(unix)]
fn bundle_source_ownership_safe(dir: &Path) -> Result<(), String> {
    use std::os::unix::fs::MetadataExt;
    let me = unsafe { libc::getuid() };
    let mut level = Some(dir);
    while let Some(path) = level {
        let meta = std::fs::metadata(path)
            .map_err(|e| format!("束源路径元数据不可读({}): {e}", path.display()))?;
        if !bundle_level_owner_trusted(meta.uid(), meta.mode(), me) {
            return Err(format!(
                "目录 {} 属主 uid={} 非当前用户(uid={me})亦非可信 root 形态",
                path.display(),
                meta.uid()
            ));
        }
        level = path.parent();
    }
    Ok(())
}

/// 非 unix 同款恒过(无 uid 语义;同 perform_bundle_install 的家族纪律)。
#[cfg(not(unix))]
fn bundle_source_ownership_safe(_dir: &Path) -> Result<(), String> {
    Ok(())
}

/// 首个有效束源:入口件在场的候选先行属主链校验(不可信 = 在场被拒,
/// 带 Vec 清单)。缺入口 = 源不在。
fn resolve_bundle_source(env_override: Option<PathBuf>) -> ResolvedBundleSource {
    for dir in keyprovider_bundle_candidates(env_override) {
        if !dir.join(KEYPROVIDER_BUNDLE_ENTRY).is_file() {
            continue;
        }
        if let Err(reason) = bundle_source_ownership_safe(&dir) {
            log::warn!("desktop: 取钥器束源属主校验未过,已拒({reason})");
            return ResolvedBundleSource::Unsafe(reason);
        }
        let files = KEYPROVIDER_BUNDLE_FILES
            .iter()
            .filter(|name| dir.join(**name).is_file())
            .map(|name| name.to_string())
            .collect::<Vec<_>>();
        return ResolvedBundleSource::Found(dir, files);
    }
    ResolvedBundleSource::Missing
}

/// 安装落点目录(数据根/wechat-localdb/bin)。
fn keyprovider_bin_dir(data_root: &Path) -> PathBuf {
    data_root.join(KEYPROVIDER_BIN_REL)
}

/// 安装执行(unix):束文件逐件 cp + chmod 700,返回(入口件绝对路径,已拷
/// 清单)。目录预建 700。任何一步失败 = 结构化 install_failed(已拷文件留
/// 在场,重装幂等覆盖)。
#[cfg(unix)]
fn perform_bundle_install(
    source: &Path,
    files: &[String],
    data_root: &Path,
) -> Result<(PathBuf, Vec<String>), String> {
    use std::os::unix::fs::PermissionsExt;
    let target_dir = keyprovider_bin_dir(data_root);
    std::fs::create_dir_all(&target_dir).map_err(|e| {
        error_value(
            "install_failed",
            &format!("取钥器安装目录创建失败({}): {e}", target_dir.display()),
            None,
        )
    })?;
    let _ = std::fs::set_permissions(&target_dir, std::fs::Permissions::from_mode(0o700));
    let mut copied = Vec::new();
    for name in files {
        let from = source.join(name);
        let to = target_dir.join(name);
        std::fs::copy(&from, &to).map_err(|e| {
            error_value("install_failed", &format!("拷贝 {name} 失败: {e}"), None)
        })?;
        std::fs::set_permissions(&to, std::fs::Permissions::from_mode(0o700)).map_err(|e| {
            error_value(
                "install_failed",
                &format!("设置权限(700)失败 {name}: {e}"),
                None,
            )
        })?;
        copied.push(name.clone());
    }
    Ok((target_dir.join(KEYPROVIDER_BUNDLE_ENTRY), copied))
}

/// 非 unix 家族同款(无执行位语义,普通拷贝;微信桥本身 macOS-only,此分支
/// 只为编译完整——同 stop_acquire_group 的 windows 分支纪律)。
#[cfg(not(unix))]
fn perform_bundle_install(
    source: &Path,
    files: &[String],
    data_root: &Path,
) -> Result<(PathBuf, Vec<String>), String> {
    let target_dir = keyprovider_bin_dir(data_root);
    std::fs::create_dir_all(&target_dir).map_err(|e| {
        error_value(
            "install_failed",
            &format!("取钥器安装目录创建失败({}): {e}", target_dir.display()),
            None,
        )
    })?;
    let mut copied = Vec::new();
    for name in files {
        std::fs::copy(source.join(name), target_dir.join(name))
            .map_err(|e| error_value("install_failed", &format!("拷贝 {name} 失败: {e}"), None))?;
        copied.push(name.clone());
    }
    Ok((target_dir.join(KEYPROVIDER_BUNDLE_ENTRY), copied))
}

/// 取钥器部署件「一键安装」(E2;action 形随 `wechat_key_provider`)。
/// - `inspect`:源在场/已安装探测(纯 fs 读,零拷贝),应答
///   `{available, source_dir, installed, installed_path, files}`。
/// - `install`:束文件 cp → `<数据根>/wechat-localdb/bin/` + chmod 700,应答
///   `{ok, installed_path, copied}`(路径保存仍走桥管理命令 set,前端编排)。
/// acquire 在途 → `acquire_in_progress` 拒(不热换在跑的取钥器文件)。
#[tauri::command]
pub async fn wechat_key_provider_install(app: AppHandle, action: String) -> Result<Value, String> {
    let data_root = crate::data_root(&app).map_err(|e| {
        error_value("internal_error", &format!("数据根不可解析: {e}"), None)
    })?;
    let env_override = std::env::var_os("MYIA_KEYPROVIDER_BUNDLE").map(PathBuf::from);
    let installed_path = keyprovider_bin_dir(&data_root).join(KEYPROVIDER_BUNDLE_ENTRY);
    let installed = installed_path.is_file();
    let installed_value = |installed: bool| -> Value {
        if installed {
            json!(installed_path.display().to_string())
        } else {
            Value::Null
        }
    };
    match action.as_str() {
        "inspect" => Ok(match resolve_bundle_source(env_override) {
            ResolvedBundleSource::Found(dir, files) => json!({
                "available": true,
                "source_dir": dir.display().to_string(),
                "installed": installed,
                "installed_path": installed_value(installed),
                "files": files,
            }),
            // 在场但属主链不可信:如实披露拒因(前端 guidance 展示;不静默
            // 装作「源不在」——束明明在场,用户值得知道为何被拒)。
            ResolvedBundleSource::Unsafe(reason) => json!({
                "available": false,
                "source_unsafe_reason": reason,
                "source_dir": Value::Null,
                "installed": installed,
                "installed_path": installed_value(installed),
                "files": [],
            }),
            ResolvedBundleSource::Missing => json!({
                "available": false,
                "source_dir": Value::Null,
                "installed": installed,
                "installed_path": installed_value(installed),
                "files": [],
            }),
        }),
        "install" => {
            if KEY_ACQUIRE.in_flight.lock().unwrap().is_some() {
                return Err(error_value(
                    "acquire_in_progress",
                    "已有一次密钥获取在进行中,请在它结束后再安装",
                    None,
                ));
            }
            let resolved = resolve_bundle_source(env_override);
            let ResolvedBundleSource::Found(source, files) = resolved else {
                if let ResolvedBundleSource::Unsafe(reason) = resolved {
                    return Err(error_value(
                        "install_source_unsafe",
                        &format!("取钥器束源属主校验未通过,已拒绝安装:{reason}"),
                        Some(json!({
                            "fix_hint": "束源目录必须由当前用户放置(多用户机器防他人投放);删除该目录后由本人重新放置部署件束,或用 MYIA_KEYPROVIDER_BUNDLE 指向本人属主的束目录"
                        })),
                    ));
                }
                return Err(error_value(
                    "install_source_missing",
                    "未检测到可安装的取钥器部署件(束暂存目录缺入口文件)",
                    Some(json!({
                        "fix_hint": "把部署件束(入口 keyprovider-lldb.sh 起四件)放到 /tmp/wxkey-deploy,或用环境变量 MYIA_KEYPROVIDER_BUNDLE 指定束目录"
                    })),
                ));
            };
            let (entry, copied) = perform_bundle_install(&source, &files, &data_root)?;
            log::info!(
                "desktop: 取钥器部署件已安装({} 件,入口 {})",
                copied.len(),
                entry.display()
            );
            Ok(json!({
                "ok": true,
                "installed_path": entry.display().to_string(),
                "copied": copied,
            }))
        }
        other => Err(invalid_params(
            "$.action",
            format!("未知动作 {other}(合法:inspect/install)"),
        )),
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

    // —— C 线(密钥状态查询 + 取钥编排;design §B/§C 契约对账)——

    /// 取钥 argv 契约钉死:--json 前置;--force 可选;--timeout-hint 恒 600
    /// (design §2 三处统一的请求值;§A.2 命令文样)。
    #[test]
    fn key_acquire_argv_pins_contract() {
        assert_eq!(
            key_acquire_argv(false),
            vec!["localdb", "key-acquire", "--json", "--timeout-hint", "600"]
        );
        assert_eq!(
            key_acquire_argv(true),
            vec!["localdb", "key-acquire", "--json", "--force", "--timeout-hint", "600"]
        );
    }

    /// key-status 应答直转(§B.1):三态夹具(§A.1 形状)内层对象原样回;
    /// 缺 key_status / 非对象 = 形状破裂报 bridge_error(不静默)。
    #[test]
    fn key_status_passthrough_three_states() {
        let ready = json!({
            "key_status": {"state": "ready", "db_count": 20,
                "acquired_at": "2026-10-13T11:22:00+08:00",
                "wechat_version": "4.1.15", "verdict_note": "抽样 3 库验真通过"}
        });
        let stale = json!({
            "key_status": {"state": "stale", "db_count": 20,
                "acquired_at": "2026-10-13T11:22:00+08:00",
                "wechat_version": "4.1.15", "verdict_note": "抽样验真失败:1/3"}
        });
        let missing = json!({
            "key_status": {"state": "missing", "db_count": 0, "acquired_at": null,
                "wechat_version": null, "verdict_note": "密钥缓存缺位"}
        });
        for payload in [&ready, &stale, &missing] {
            assert_eq!(key_status_value(payload).unwrap(), payload["key_status"]);
        }
        // 形状破裂:空对象 / key_status 非对象 → 结构化拒(桥侧形状再漂移
        // 时这里显式爆雷,不静默假绿)
        let err = key_status_value(&json!({})).unwrap_err();
        assert!(err.contains("bridge_error"), "缺 key_status 应 bridge_error: {err}");
        let err = key_status_value(&json!({"key_status": "broken"})).unwrap_err();
        assert!(err.contains("bridge_error"), "非对象应 bridge_error: {err}");
    }

    /// progress message → 阶段关键词表(锚 §C 法定消息串)+ 未知消息沿用
    /// 上一阶段(步进条不被杂音打断)。
    #[test]
    fn classify_progress_phase_table() {
        use KeyAcquirePhase::*;
        assert_eq!(classify_progress_phase("等待输入管理员密码", Derive), Password);
        assert_eq!(classify_progress_phase("正在连接微信", Password), Attach);
        assert_eq!(
            classify_progress_phase("请在微信中退出登录并重新扫码", Password),
            WaitRelogin
        );
        assert_eq!(classify_progress_phase("等待重新登录", Attach), WaitRelogin);
        assert_eq!(classify_progress_phase("正在验证 20 个数据库", Password), Derive);
        assert_eq!(classify_progress_phase("正在派生密钥材料", Password), Derive);
        // 英文片段(小写归一)
        assert_eq!(classify_progress_phase("attach: ready", Password), Attach);
        // 未命中 → 沿用上一阶段
        assert_eq!(classify_progress_phase("随便说点啥", WaitRelogin), WaitRelogin);
    }

    /// 行状态机:progress 行出事件(detail 原文)/ 显式 phase 字段覆盖关键
    /// 词归类 / 终态信封首条收、后续丢 / 杂行计数忽略。
    #[test]
    fn acquire_line_machine_shapes() {
        let mut machine = AcquireLineMachine::new();
        let (phase, detail) = machine
            .feed(r#"{"type":"progress","message":"等待输入管理员密码","level":0}"#)
            .expect("progress 行应出事件");
        assert_eq!((phase, detail.as_deref()), (KeyAcquirePhase::Password, Some("等待输入管理员密码")));
        // 显式 phase 字段优先(v1.1 取钥器自报;message 不含关键词也认)
        let (phase, _) = machine
            .feed(r#"{"type":"progress","message":"whatever","phase":"wait_relogin"}"#)
            .expect("显式 phase 行应出事件");
        assert_eq!(phase, KeyAcquirePhase::WaitRelogin);
        // 终态信封:首条收,第二条(协议违例形态)丢弃
        let envelope = json!({"key_acquire": {"result": "ok", "db_count": 7}});
        assert!(machine.feed(&serde_json::to_string(&envelope).unwrap()).is_none());
        assert!(
            machine
                .feed(r#"{"key_acquire":{"result":"ok","db_count":9}}"#)
                .is_none()
        );
        assert_eq!(machine.envelope.as_ref(), Some(&envelope));
        // 杂行(非 JSON / 非对象 / 空行)忽略不炸
        assert!(machine.feed("not-json").is_none());
        assert!(machine.feed("42").is_none());
        assert!(machine.feed("").is_none());
        assert!(machine.ignored_lines >= 3);
    }

    /// 终态分类:already_ready 短路 → ok;桥 error 族人话透传(exit 21 形态);
    /// 无信封按退出码兜底;db_count 只认正整数。
    #[test]
    fn classify_acquire_outcome_shapes() {
        // already_ready(桥短路,§A.2)→ ok + db_count 直转
        assert_eq!(
            classify_acquire_outcome(
                Some(&json!({"key_acquire": {"result": "already_ready", "db_count": 20}})),
                Some(0),
                ""
            ),
            AcquireOutcome::ok(Some(20))
        );
        assert_eq!(
            classify_acquire_outcome(
                Some(&json!({"key_acquire": {"result": "ok", "db_count": 3}})),
                Some(0),
                ""
            ),
            AcquireOutcome::ok(Some(3))
        );
        // 桥 error 族(未配取钥器 exit 21 形态,§F)→ failed + 人话透传
        let outcome = classify_acquire_outcome(
            Some(&json!({"error": {"code": "key_unavailable",
                "message": "未配置外部取钥器,请在设置中指定可执行文件路径"}})),
            Some(21),
            "",
        );
        assert_eq!(outcome.result, "failed");
        assert_eq!(
            outcome.error.as_deref(),
            Some("未配置外部取钥器,请在设置中指定可执行文件路径")
        );
        // 无信封:exit 0 = 未返回结果;非 0 = 异常退出附 stderr 尾部
        let outcome = classify_acquire_outcome(None, Some(0), "");
        assert_eq!(outcome.result, "failed");
        assert!(outcome.error.unwrap().contains("未返回结果"));
        let outcome = classify_acquire_outcome(None, Some(2), "boom 尾部");
        let error = outcome.error.expect("异常退出应带错误");
        assert!(
            error.contains("exit=2") && error.contains("boom 尾部"),
            "异常退出应附 stderr 尾部: {error}"
        );
        // db_count 形状守门:0 → None(ok 面 0 库无意义,前端回落状态查询)
        assert_eq!(
            classify_acquire_outcome(
                Some(&json!({"key_acquire": {"result": "ok", "db_count": 0}})),
                Some(0),
                ""
            )
            .db_count,
            None
        );
    }

    /// 哨兵路径钉死(§B.2:数据根下 wechat-localdb/cancel.keyacquire)+
    /// 超帽人话(§F「获取超时(15 分钟),可重试」在 900s 壳帽下逐字成立)。
    #[test]
    fn sentinel_path_and_timeout_message() {
        assert_eq!(
            cancel_sentinel_path(Path::new("/data")),
            PathBuf::from("/data/wechat-localdb/cancel.keyacquire")
        );
        assert_eq!(
            timeout_error_message(Duration::from_secs(900)),
            "获取超时(15 分钟),可重试"
        );
    }

    /// 哨兵落盘回环:父目录预建 + 可再写(取消幂等面)。
    #[test]
    fn write_cancel_sentinel_creates_parents() {
        let dir = tempfile::tempdir().expect("临时目录创建失败");
        let root = dir.path().join("nested-data-root");
        write_cancel_sentinel(&root).expect("哨兵写入失败");
        let path = cancel_sentinel_path(&root);
        assert!(path.is_file(), "哨兵应落地: {}", path.display());
        // 再写不炸(覆盖形态)
        write_cancel_sentinel(&root).expect("哨兵覆盖写失败");
    }

    /// 事件载荷形态钉死:detail 恒在场(null 序列化),phase snake_case
    /// 词面 = §B.3 枚举逐字。
    #[test]
    fn key_acquire_event_payload_shape() {
        let payload = serde_json::to_value(KeyAcquireEvent {
            seq: 7,
            phase: KeyAcquirePhase::WaitRelogin,
            detail: None,
        })
        .expect("事件序列化不可失败");
        assert_eq!(payload["seq"], json!(7));
        assert_eq!(payload["phase"], json!("wait_relogin"));
        assert_eq!(payload["detail"], json!(null), "detail 应恒在场(null 形态)");
        // 常量与前端 KEY_ACQUIRE_EVENT_NAME 成对同值(§B.3)
        assert_eq!(KEY_ACQUIRE_EVENT, "wechat-key-acquire");
    }

    // —— C 线进程级用例(假桥可执行件;unix 门控同 pyenv_components sh 桩)——

    /// 假桥可执行件(sh 桩):body 决定形态(progress NDJSON / 终态信封 /
    /// 挂死)。
    #[cfg(unix)]
    fn write_mock_bridge(dir: &Path, name: &str, body: &str) -> PathBuf {
        use std::os::unix::fs::PermissionsExt;
        let path = dir.join(name);
        std::fs::write(&path, format!("#!/bin/sh\n{body}\n")).expect("写假桥失败");
        std::fs::set_permissions(&path, std::fs::Permissions::from_mode(0o755))
            .expect("chmod 失败");
        path
    }

    /// 测试事件收集器形态。
    type CollectedEvents = Arc<Mutex<Vec<(u64, KeyAcquirePhase, Option<String>)>>>;

    /// 等待占坑(编排 spawn 后即在途;上限 10s 防永挂)。
    fn wait_for_in_flight(state: &KeyAcquireManager) {
        let deadline = Instant::now() + Duration::from_secs(10);
        while Instant::now() < deadline {
            if state.occupied() {
                return;
            }
            std::thread::sleep(Duration::from_millis(5));
        }
        panic!("acquire 未在期限内占坑");
    }

    /// progress 行逐行读逐行发(§B.2/§B.3):seq 从 1 起单调递增;阶段按
    /// 关键词表归类;detail = message 原文;终态 done 事件 + ok 返回值
    /// (db_count 直转);第二 run(短路形态)seq **进程级续增不重置**——
    /// 前端「丢乱序旧包」判据不被新 run 破坏。
    #[cfg(unix)]
    #[test]
    fn progress_lines_to_events_seq_monotonic() {
        let dir = tempfile::tempdir().expect("临时目录创建失败");
        let bridge = write_mock_bridge(
            dir.path(),
            "mock-wechat-bridge",
            r#"printf '%s\n' \
  '{"type":"progress","message":"等待输入管理员密码","level":0}' \
  '{"type":"progress","message":"正在连接微信","level":0}' \
  '{"type":"progress","message":"请在微信中退出登录并重新扫码","level":0}' \
  '{"type":"progress","message":"正在验证 20 个数据库","level":0}' \
  '{"key_acquire":{"result":"ok","db_count":20}}'"#,
        );
        let state = KeyAcquireManager::new();
        let events: CollectedEvents = Arc::new(Mutex::new(Vec::new()));
        let sink = events.clone();
        let outcome = run_key_acquire(
            &bridge,
            false,
            None,
            &state,
            Duration::from_secs(30),
            move |seq, phase, detail| {
                sink.lock().unwrap().push((seq, phase, detail.map(str::to_string)));
            },
        )
        .expect("取钥编排应成功");
        assert_eq!(outcome, AcquireOutcome::ok(Some(20)));
        assert_eq!(
            outcome.to_value(),
            json!({"result": "ok", "db_count": 20})
        );
        let collected = events.lock().unwrap();
        let seqs: Vec<u64> = collected.iter().map(|(seq, _, _)| *seq).collect();
        assert_eq!(seqs, vec![1, 2, 3, 4, 5], "seq 应从 1 起单调递增: {seqs:?}");
        assert_eq!(
            collected
                .iter()
                .map(|(_, phase, _)| *phase)
                .collect::<Vec<_>>(),
            vec![
                KeyAcquirePhase::Password,
                KeyAcquirePhase::Attach,
                KeyAcquirePhase::WaitRelogin,
                KeyAcquirePhase::Derive,
                KeyAcquirePhase::Done,
            ]
        );
        // detail = provider progress 的 message 原文(§B.3)
        assert_eq!(collected[0].2.as_deref(), Some("等待输入管理员密码"));
        assert_eq!(collected[3].2.as_deref(), Some("正在验证 20 个数据库"));
        // done 终态 detail = null(结果页 N 库文案走返回值 db_count)
        assert_eq!(collected[4].2, None);
        drop(collected);
        // 第二 run(already_ready 短路形态):seq 续增(进程级单调)
        let bridge_short = write_mock_bridge(
            dir.path(),
            "mock-short-circuit",
            r#"printf '%s\n' '{"key_acquire":{"result":"already_ready","db_count":20}}'"#,
        );
        let sink = events.clone();
        let outcome = run_key_acquire(
            &bridge_short,
            false,
            None,
            &state,
            Duration::from_secs(30),
            move |seq, phase, detail| {
                sink.lock().unwrap().push((seq, phase, detail.map(str::to_string)));
            },
        )
        .expect("短路形态应 ok");
        assert_eq!(outcome, AcquireOutcome::ok(Some(20)));
        let collected = events.lock().unwrap();
        let last = collected.last().expect("短路 run 应有 done 终态事件");
        assert_eq!(last.0, 6, "第二 run 终态 seq 应续增不重置: {}", last.0);
        assert_eq!(last.1, KeyAcquirePhase::Done);
    }

    /// 单飞锁(§B.2 简化定案):在途第二次 acquire → acquire_in_progress
    /// 「已有一次密钥获取在进行中」;取消后槽释放,后续 acquire 可再入。
    #[cfg(unix)]
    #[test]
    fn single_flight_lock_rejects_second_acquire() {
        let dir = tempfile::tempdir().expect("临时目录创建失败");
        let bridge = write_mock_bridge(dir.path(), "mock-stall", "sleep 60");
        let state = Arc::new(KeyAcquireManager::new());
        let events: CollectedEvents = Arc::new(Mutex::new(Vec::new()));
        let handle = {
            let bridge = bridge.clone();
            let sink = events.clone();
            let state = state.clone();
            std::thread::spawn(move || {
                run_key_acquire(
                    &bridge,
                    false,
                    None,
                    &state,
                    Duration::from_secs(60),
                    move |seq, phase, detail| {
                        sink.lock().unwrap().push((seq, phase, detail.map(str::to_string)));
                    },
                )
            })
        };
        wait_for_in_flight(&state);
        // 在途第二次 acquire:结构化拒(命令错误信封,§F)
        let err = run_key_acquire(&bridge, false, None, &state, Duration::from_secs(5), |_, _, _| {})
            .expect_err("单飞期第二次 acquire 应拒绝");
        assert!(err.contains("acquire_in_progress"), "码名应 acquire_in_progress: {err}");
        assert!(err.contains("已有一次密钥获取在进行中"), "法定人话应在场: {err}");
        // 取消收尾(槽释放)
        let cancel_out = request_cancel(&state, dir.path(), |_, _, _| {}).expect("取消应成功");
        assert_eq!(cancel_out["ok"], json!(true));
        let joined = handle
            .join()
            .expect("编排线程应正常收")
            .expect("取消后的编排不应报错");
        assert_eq!(joined, AcquireOutcome::cancelled());
        // 槽已释放:再入合法(短路形态即返)
        let bridge_short = write_mock_bridge(
            dir.path(),
            "mock-short-2",
            r#"printf '%s\n' '{"key_acquire":{"result":"already_ready","db_count":4}}'"#,
        );
        let again = run_key_acquire(&bridge_short, false, None, &state, Duration::from_secs(10), |_, _, _| {})
            .expect("取消后应可再入");
        assert_eq!(again.result, "ok");
        assert_eq!(again.db_count, Some(4));
    }

    /// 取消三连(§B.2):停用户态树 + 哨兵文件落 `<数据根>/wechat-localdb/
    /// cancel.keyacquire` + cancelled 终态事件(取消方发射);编排命令收
    /// cancelled 且**不双发**终态事件。
    #[cfg(unix)]
    #[test]
    fn cancel_drops_sentinel_file() {
        let dir = tempfile::tempdir().expect("临时目录创建失败");
        let root = dir.path().to_path_buf();
        let bridge = write_mock_bridge(
            dir.path(),
            "mock-stall-cancel",
            r#"printf '%s\n' '{"type":"progress","message":"正在连接微信","level":0}'; sleep 60"#,
        );
        let state = Arc::new(KeyAcquireManager::new());
        let events: CollectedEvents = Arc::new(Mutex::new(Vec::new()));
        let handle = {
            let bridge = bridge.clone();
            let sink = events.clone();
            let state = state.clone();
            std::thread::spawn(move || {
                run_key_acquire(
                    &bridge,
                    false,
                    None,
                    &state,
                    Duration::from_secs(60),
                    move |seq, phase, detail| {
                        sink.lock().unwrap().push((seq, phase, detail.map(str::to_string)));
                    },
                )
            })
        };
        wait_for_in_flight(&state);
        // 取消(事件收集走独立通道,验证「终态事件由取消方发射」)
        let cancel_events: CollectedEvents = Arc::new(Mutex::new(Vec::new()));
        let cancel_sink = cancel_events.clone();
        let cancel_out = request_cancel(&state, &root, move |seq, phase, detail| {
            cancel_sink
                .lock()
                .unwrap()
                .push((seq, phase, detail.map(str::to_string)));
        })
        .expect("取消应成功");
        assert_eq!(cancel_out["ok"], json!(true));
        // ② 哨兵落地(§B.2 取消动作;数据根下 wechat-localdb/ 私有区)
        let sentinel = cancel_sentinel_path(&root);
        assert!(sentinel.is_file(), "取消哨兵应落地: {}", sentinel.display());
        assert_eq!(
            sentinel,
            root.join("wechat-localdb").join("cancel.keyacquire")
        );
        // ③ cancelled 终态事件由取消方发射(恰一条,phase=cancelled,detail=null)
        let cancelled_events = cancel_events.lock().unwrap();
        assert_eq!(cancelled_events.len(), 1, "取消方应恰发一条终态事件");
        assert_eq!(cancelled_events[0].1, KeyAcquirePhase::Cancelled);
        assert_eq!(cancelled_events[0].2, None);
        drop(cancelled_events);
        // 编排命令收 cancelled;编排侧不双发 cancelled 终态
        let joined = handle
            .join()
            .expect("编排线程应正常收")
            .expect("取消后的编排不应报错");
        assert_eq!(joined, AcquireOutcome::cancelled());
        let all = events.lock().unwrap();
        assert!(
            !all.iter().any(|(_, phase, _)| *phase == KeyAcquirePhase::Cancelled),
            "编排侧不得双发 cancelled 终态: {all:?}"
        );
    }

    /// 壳帽(§B.2/§F):读行停滞超帽 → kill 用户态链 + 判 failed「获取超时
    /// …可重试」+ failed 终态事件(detail = 人话);测试以 1s 小帽代 900s,
    /// 语义同门(帽值是参数,消息分钟数由帽折算)。
    #[cfg(unix)]
    #[test]
    fn shell_cap_over_deadline_fails() {
        let dir = tempfile::tempdir().expect("临时目录创建失败");
        let bridge = write_mock_bridge(
            dir.path(),
            "mock-stall-cap",
            r#"printf '%s\n' '{"type":"progress","message":"正在连接微信","level":0}'; sleep 60"#,
        );
        let state = KeyAcquireManager::new();
        let events: CollectedEvents = Arc::new(Mutex::new(Vec::new()));
        let sink = events.clone();
        let started = Instant::now();
        let outcome = run_key_acquire(
            &bridge,
            false,
            None,
            &state,
            Duration::from_secs(1),
            move |seq, phase, detail| {
                sink.lock().unwrap().push((seq, phase, detail.map(str::to_string)));
            },
        )
        .expect("超帽是终态(failed)不是命令错误");
        assert!(
            started.elapsed() < Duration::from_secs(20),
            "超帽应收在帽+宽限内,实测 {:?}",
            started.elapsed()
        );
        assert_eq!(outcome.result, "failed");
        let error = outcome.error.clone().expect("超帽应带人话");
        assert!(error.contains("获取超时"), "超帽人话应在场: {error}");
        assert!(error.contains("重试"), "重试指引应在场: {error}");
        assert_eq!(
            outcome.to_value(),
            json!({"result": "failed", "error": error})
        );
        let collected = events.lock().unwrap();
        let last = collected.last().expect("应有终态事件");
        assert_eq!(last.1, KeyAcquirePhase::Failed);
        assert_eq!(last.2.as_deref(), Some(error.as_str()));
    }

    // —— E 线(部署件一键安装;design §C 部署位/D3 装机后首用引导)——

    /// 束源候选序:env 覆盖最高优 → /tmp/wxkey-deploy 兜底;源解析只认
    /// 入口件在场的候选(缺入口 = 源不在),文件清单如实反映在场件;
    /// 属主链校验(tempfile 目录全链 = 当前用户/root 可信形态 → Found)。
    #[test]
    fn bundle_source_candidates_and_resolution() {
        let dir = tempfile::tempdir().expect("临时目录创建失败");
        // 候选序:显式覆盖在前,暂存目录恒在候选尾
        let candidates = keyprovider_bundle_candidates(Some(dir.path().to_path_buf()));
        assert_eq!(candidates.len(), 2);
        assert_eq!(candidates[0], dir.path());
        assert_eq!(candidates[1], PathBuf::from("/tmp/wxkey-deploy"));
        assert_eq!(keyprovider_bundle_candidates(None).len(), 1);
        // 空目录(无入口件)不被认作源:结果不会是覆盖目录自身的 Found
        // (兜底候选若在场则如实解析它——Found 它/在场被拒/不在场皆合理,
        // 唯一不许的是把空覆盖目录当源)。
        match resolve_bundle_source(Some(dir.path().to_path_buf())) {
            ResolvedBundleSource::Found(resolved, _) => {
                assert_ne!(resolved, dir.path().to_path_buf());
            }
            ResolvedBundleSource::Unsafe(_) | ResolvedBundleSource::Missing => {}
        }
        // 只放入口件 → 源有效,清单如实只含入口件
        std::fs::write(dir.path().join(KEYPROVIDER_BUNDLE_ENTRY), "#!/bin/bash\n")
            .expect("写入口件失败");
        let ResolvedBundleSource::Found(resolved, files) =
            resolve_bundle_source(Some(dir.path().to_path_buf()))
        else {
            panic!("入口件在场应有效");
        };
        assert_eq!(resolved, dir.path());
        assert_eq!(files, vec![KEYPROVIDER_BUNDLE_ENTRY]);
        // 全四件在场 → 清单齐
        for name in KEYPROVIDER_BUNDLE_FILES {
            std::fs::write(dir.path().join(name), "#!/bin/bash\n").expect("写束件失败");
        }
        let ResolvedBundleSource::Found(_resolved, files) =
            resolve_bundle_source(Some(dir.path().to_path_buf()))
        else {
            panic!("全件束应有效");
        };
        assert_eq!(files.len(), KEYPROVIDER_BUNDLE_FILES.len());
    }

    /// 属主链单级判定(评审修③核心):本人属主过;root 属主 + 755(他人
    /// 不可写)过;root 属主 + 1777 sticky(/tmp 形态)过;root 属主 +
    /// 1777 无 sticky(他人可投放且无 sticky 护栏)拒;他人属主一律拒。
    #[cfg(unix)]
    #[test]
    fn bundle_level_owner_trusted_matrix() {
        let me = unsafe { libc::getuid() };
        // 本人属主:任何模式都过(自己的目录自己负责)
        assert!(bundle_level_owner_trusted(me, 0o777, me));
        // root 属主 + 他人不可写(755/700):过
        assert!(bundle_level_owner_trusted(0, 0o755, me));
        assert!(bundle_level_owner_trusted(0, 0o700, me));
        // root 属主 + 世界可写但 sticky(/tmp 1777 形态):过
        assert!(bundle_level_owner_trusted(0, 0o1777, me));
        // root 属主 + 世界可写无 sticky:拒(他人可随意投放)
        assert!(!bundle_level_owner_trusted(0, 0o0777, me));
        // 他人属主:一律拒(模式无关)
        assert!(!bundle_level_owner_trusted(4242, 0o755, me));
        assert!(!bundle_level_owner_trusted(4242, 0o1777, me));
    }

    /// 属主链上行校验:系统真实路径(/ 与 /tmp 所在链 = root 755/1777
    /// sticky 形态)应过;根目录自身必过。他人属主目录无法在测试里构造
    /// (chown 需 root),该分支由矩阵单测锚定 + Unsafe 集成路径靠真机
    /// 拒因文案人工核验(见 check 档)。
    #[cfg(unix)]
    #[test]
    fn bundle_source_ownership_safe_walks_system_paths() {
        assert!(bundle_source_ownership_safe(Path::new("/")).is_ok());
        // macOS /tmp → /private/tmp(root 1777 sticky)真实链
        assert!(bundle_source_ownership_safe(Path::new("/tmp")).is_ok());
        let dir = tempfile::tempdir().expect("临时目录创建失败");
        assert!(bundle_source_ownership_safe(dir.path()).is_ok());
    }

    /// 安装执行:cp 到 `<数据根>/wechat-localdb/bin/` + 每件 700 + 返回入口
    /// 件绝对路径;重装幂等覆盖(unix 权限位逐件断言)。
    #[cfg(unix)]
    #[test]
    fn perform_bundle_install_copies_with_mode_700() {
        use std::os::unix::fs::PermissionsExt;
        let source_dir = tempfile::tempdir().expect("源临时目录创建失败");
        for name in KEYPROVIDER_BUNDLE_FILES {
            std::fs::write(source_dir.path().join(name), format!("#!/bin/bash\n# {name}\n"))
                .expect("写束件失败");
        }
        let root = tempfile::tempdir().expect("数据根临时目录创建失败");
        let files: Vec<String> = KEYPROVIDER_BUNDLE_FILES.iter().map(|name| name.to_string()).collect();
        let (entry, copied) =
            perform_bundle_install(source_dir.path(), &files, root.path()).expect("安装应成功");
        assert_eq!(
            entry,
            root.path().join("wechat-localdb").join("bin").join("keyprovider-lldb.sh")
        );
        assert_eq!(copied.len(), KEYPROVIDER_BUNDLE_FILES.len());
        for name in KEYPROVIDER_BUNDLE_FILES {
            let installed = root.path().join("wechat-localdb/bin").join(name);
            assert!(installed.is_file(), "{name} 应已安装: {}", installed.display());
            assert_eq!(
                std::fs::metadata(&installed).unwrap().permissions().mode() & 0o777,
                0o700,
                "{name} 权限应为 700"
            );
            let body = std::fs::read_to_string(&installed).unwrap();
            assert!(body.contains(name), "{name} 内容应来自源(真拷贝)");
        }
        // 重装幂等:二次安装覆盖成功(内容可变)
        std::fs::write(source_dir.path().join(KEYPROVIDER_BUNDLE_ENTRY), "#!/bin/bash\n# v2\n")
            .expect("改写源入口件失败");
        let _ = perform_bundle_install(source_dir.path(), &files, root.path())
            .expect("重装应幂等成功");
        assert!(std::fs::read_to_string(&entry).unwrap().contains("v2"));
    }

    /// 单件拷贝失败如实报 install_failed(源件被并发删除形态)。
    #[cfg(unix)]
    #[test]
    fn perform_bundle_install_reports_copy_failure() {
        let source_dir = tempfile::tempdir().expect("源临时目录创建失败");
        std::fs::write(source_dir.path().join(KEYPROVIDER_BUNDLE_ENTRY), "#!/bin/bash\n")
            .expect("写入口件失败");
        let root = tempfile::tempdir().expect("数据根临时目录创建失败");
        // 清单里混入一个源不存在的件(并发删除形态)→ 结构化失败
        let files = vec![KEYPROVIDER_BUNDLE_ENTRY.to_string(), "ghost件.py".to_string()];
        let err = perform_bundle_install(source_dir.path(), &files, root.path())
            .expect_err("缺源件应失败");
        assert!(err.contains("install_failed"), "码名应 install_failed: {err}");
        assert!(err.contains("ghost件.py"), "失败件名应在场: {err}");
    }
}
