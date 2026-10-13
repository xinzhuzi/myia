//! 微信聊天记录导出壳命令(task 10-14-wechat-chat-export R6;判例 key-acquire)。
//!
//! 「微信本机」只读会话入口导出行的壳侧通道:spawn 桥
//! `localdb export <chat> --format … --out <dir> --json`,桥 stdout 是
//! NDJSON 流(`{"progress":…}` 行 + 末行回执 `{"export":…}` / 错误
//! `{"error":…}`,R5 key-acquire 判例同构)→ 每行转 Tauri 事件
//! [`WECHAT_CHAT_EXPORT_EVENT`](载荷 `{job_id, seq, body}`,body = 桥行
//! 原样 JSON);终态回执**原样转前端**(壳不改形)。
//!
//! - **out_dir 缺省** = 壳内 `open_dir` 目录对话框(dialog 插件
//!   `blocking_pick_folder`;取消 = 返 `Ok(null)` 静默零 spawn,群导出
//!   `wechat_group_export` 判例同款)。
//! - **取消** = [`wechat_chat_export_cancel`] `{job_id}`:job 表 take 槽 +
//!   kill 进程组(SIGTERM → 宽限 → SIGKILL;桥自装 SIGTERM 处理器清
//!   staging 后回 `export_cancelled` 信封)。job_id 经首条事件下发
//!   (start 事件恒先于桥行,前端可靠捕获)。
//! - **超时**:无总帽(全库导出可长;取消是用户侧机制);读行空闲帽
//!   900s = key-acquire 壳帽同值(空闲超帽 = 桥挂死,kill 兜底)。
//! - **红线**:壳不读任何微信库零密钥;聊天内容只活在桥 stdout → 事件/
//!   回执里透传,壳侧日志只打形状(行计数/exit 码/路径)。

use std::io::BufRead;
use std::path::{Path, PathBuf};
use std::process::{Command, Stdio};
use std::sync::atomic::{AtomicBool, AtomicU64, Ordering};
use std::sync::{mpsc, Arc, Mutex};
use std::time::{Duration, Instant};

use serde_json::{json, Value};
use tauri::{AppHandle, Emitter, Manager};
use tauri_plugin_dialog::DialogExt;

/// 导出进度事件名(与前端 wechat-chat-export-api.ts 的
/// `WECHAT_CHAT_EXPORT_EVENT_NAME` 常量同值成对;改其一必同步另一)。
pub const WECHAT_CHAT_EXPORT_EVENT: &str = "wechat-chat-export-progress";

/// 六格式封闭词表(桥 CLI `--format` 同源;壳侧早拒拼错)。
pub(crate) const EXPORT_FORMATS: [&str; 6] = ["json", "txt", "csv", "md", "html", "xlsx"];

/// 读行空闲帽(秒):超帽 = 桥挂死,kill 进程组判错(key-acquire 壳帽同值)。
const EXPORT_IDLE_CAP: Duration = Duration::from_secs(900);
/// 取消/超帽后组信号优雅宽限(SIGTERM → 轮询 → SIGKILL;key-acquire 同款)。
const EXPORT_STOP_GRACE: Duration = Duration::from_secs(5);
/// 宽限轮询步长。
const POLL_INTERVAL: Duration = Duration::from_millis(100);

// ---------------------------------------------------------------------------
// 纯函数:argv 组装(单测直驱;`--json` 前置 = key-acquire argv 判例)
// ---------------------------------------------------------------------------

/// 导出命令参数(命令面收窄后的规范形态;时间戳已由桥侧归一,壳只透传)。
pub(crate) struct ChatExportParams {
    pub(crate) chat_id: String,
    pub(crate) format: String,
    pub(crate) out_dir: PathBuf,
    pub(crate) from_ts: Option<i64>,
    pub(crate) to_ts: Option<i64>,
    pub(crate) types: Vec<String>,
    pub(crate) sender: Option<String>,
    pub(crate) display_name_pref: Option<String>,
    pub(crate) name_mode: Option<String>,
    pub(crate) all: bool,
}

/// 组装桥 argv(纯)。筛选参数按在场拼接;`--all` 在场时桥按全库导出
/// (chat_id 位置参数保留 —— 桥 CLI 契约形状,--all 语义桥侧裁决)。
pub(crate) fn build_export_argv(params: &ChatExportParams) -> Vec<String> {
    let mut argv = vec![
        "localdb".to_string(),
        "export".to_string(),
        params.chat_id.clone(),
        "--format".to_string(),
        params.format.clone(),
        "--out".to_string(),
        params.out_dir.display().to_string(),
        "--json".to_string(),
    ];
    if let Some(ts) = params.from_ts {
        argv.push("--from-ts".into());
        argv.push(ts.to_string());
    }
    if let Some(ts) = params.to_ts {
        argv.push("--to-ts".into());
        argv.push(ts.to_string());
    }
    if !params.types.is_empty() {
        argv.push("--types".into());
        argv.push(params.types.join(","));
    }
    if let Some(sender) = &params.sender {
        argv.push("--sender".into());
        argv.push(sender.clone());
    }
    if let Some(pref) = &params.display_name_pref {
        argv.push("--display-name-pref".into());
        argv.push(pref.clone());
    }
    if let Some(mode) = &params.name_mode {
        argv.push("--name-mode".into());
        argv.push(mode.clone());
    }
    if params.all {
        argv.push("--all".into());
    }
    argv
}

// ---------------------------------------------------------------------------
// 纯函数:stdout 行状态机(progress 透传 / 终态信封收首条;杂行计数)
// ---------------------------------------------------------------------------

/// 桥 stdout 行处理状态机(纯;key-acquire `AcquireLineMachine` 同族)。
///
/// 行形(R5):progress 行 `{"progress":{…}}` → 透传(返回 Some(解析值));
/// 终态信封 `{"export":…}` / `{"error":…}` / `{"verify":…}` → 收首条返回
/// None;杂行(空/非 JSON/非对象)计数忽略,不炸不重试。
pub(crate) struct ExportLineMachine {
    envelope: Option<Value>,
    pub(crate) ignored_lines: usize,
    pub(crate) progress_lines: usize,
}

impl ExportLineMachine {
    pub(crate) fn new() -> Self {
        Self { envelope: None, ignored_lines: 0, progress_lines: 0 }
    }

    /// 喂一行:progress → `Some(原行 JSON)`;终态信封 → 收藏返回 `None`;
    /// 杂行 → 计数返回 `None`。
    pub(crate) fn feed(&mut self, line: &str) -> Option<Value> {
        let trimmed = line.trim();
        if trimmed.is_empty() {
            self.ignored_lines += 1;
            return None;
        }
        let Ok(parsed) = serde_json::from_str::<Value>(trimmed) else {
            self.ignored_lines += 1;
            return None;
        };
        if !parsed.is_object() {
            self.ignored_lines += 1;
            return None;
        }
        let object = parsed.as_object().expect("checked");
        if object.contains_key("progress") {
            self.progress_lines += 1;
            return Some(parsed);
        }
        if self.envelope.is_none()
            && (object.contains_key("export")
                || object.contains_key("error")
                || object.contains_key("verify"))
        {
            self.envelope = Some(parsed);
            return None;
        }
        self.ignored_lines += 1;
        None
    }
}

// ---------------------------------------------------------------------------
// job 表(多任务面:key-acquire 是单飞,导出允许多窗并行 → 键 = job_id)
// ---------------------------------------------------------------------------

/// 在途导出槽(pgid == 0 = spawn 占位,组信号跳过;spawn 成功后回填)。
struct ExportJobSlot {
    cancel_requested: Arc<AtomicBool>,
    pgid: u32,
}

/// 导出 job 表:job_id 分配(进程级单调)+ 在途槽(取消面 take 槽停组)。
/// 槽容器用 Vec(static 初始化须 const;Vec::new() 是 const,HashMap 不是,
/// 在途导出数量级个位数,线性扫描零成本)。
pub struct ExportJobTable {
    jobs: Mutex<Vec<(u64, ExportJobSlot)>>,
    next_id: AtomicU64,
}

impl ExportJobTable {
    /// 测试用独立实例(不碰全局表)。
    #[cfg(test)]
    pub(crate) fn new() -> Self {
        Self { jobs: Mutex::new(Vec::new()), next_id: AtomicU64::new(0) }
    }

    /// 预登记(spawn 前):返回 job_id + 取消旗标;pgid 占位 0。
    fn register(&self) -> (u64, Arc<AtomicBool>) {
        let job_id = self.next_id.fetch_add(1, Ordering::SeqCst) + 1;
        let flag = Arc::new(AtomicBool::new(false));
        self.jobs.lock().unwrap().push((
            job_id,
            ExportJobSlot { cancel_requested: flag.clone(), pgid: 0 },
        ));
        (job_id, flag)
    }

    /// spawn 后回填 pgid(组信号可达)。
    fn set_pgid(&self, job_id: u64, pgid: u32) {
        if let Some((_id, slot)) =
            self.jobs.lock().unwrap().iter_mut().find(|(id, _slot)| *id == job_id)
        {
            slot.pgid = pgid;
        }
    }

    /// 正常完成:摘槽(取消面从此 unknown job)。
    fn finish(&self, job_id: u64) {
        self.jobs.lock().unwrap().retain(|(id, _slot)| *id != job_id);
    }

    /// 取消:take 槽 + 置旗标 + 停进程组(在 = true;unknown/已完成 = false)。
    fn cancel(&self, job_id: u64) -> bool {
        let mut jobs = self.jobs.lock().unwrap();
        let Some(index) = jobs.iter().position(|(id, _slot)| *id == job_id) else {
            return false;
        };
        let (_id, slot) = jobs.remove(index);
        drop(jobs);
        slot.cancel_requested.store(true, Ordering::SeqCst);
        stop_export_group(slot.pgid);
        true
    }
}

/// 壳侧全局 job 表(进程单实例 ⇒ 全局即会话级;与 key-acquire 单飞槽同址惯例)。
static EXPORT_JOBS: ExportJobTable = ExportJobTable {
    jobs: Mutex::new(Vec::new()),
    next_id: AtomicU64::new(0),
};

// ---------------------------------------------------------------------------
// 用户态进程组停(SIGTERM → 宽限 → SIGKILL;key-acquire 同族私有件的
// 本地同形孪生 —— wechat_group_export.rs error_value 孪生同判例,并行改面
// 零冲突;改信号纪律须两处同步)
// ---------------------------------------------------------------------------

#[cfg(unix)]
fn terminate_export_group(pgid: u32) {
    unsafe {
        libc::kill(-(pgid as libc::pid_t), libc::SIGTERM);
        libc::kill(pgid as libc::pid_t, libc::SIGTERM);
    }
}

#[cfg(unix)]
fn force_kill_export_group(pgid: u32) {
    unsafe {
        libc::kill(-(pgid as libc::pid_t), libc::SIGKILL);
        libc::kill(pgid as libc::pid_t, libc::SIGKILL);
    }
}

#[cfg(unix)]
fn export_group_alive(pgid: u32) -> bool {
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

#[cfg(windows)]
fn terminate_export_group(pgid: u32) {
    let _ = std::process::Command::new("taskkill")
        .args(["/PID", &pgid.to_string(), "/T", "/F"])
        .output();
}

#[cfg(windows)]
fn force_kill_export_group(_pgid: u32) {
    // terminate 已 /T /F 树杀;强杀同 fn 不再二段
}

#[cfg(windows)]
fn export_group_alive(_pgid: u32) -> bool {
    false
}

/// 组停收敛:SIGTERM → 宽限轮询 → SIGKILL;pgid == 0 = 占位(spawn 未成)
/// 直接跳过(-0 组信号会误伤壳自身进程组)。
fn stop_export_group(pgid: u32) {
    if pgid == 0 {
        return;
    }
    terminate_export_group(pgid);
    #[cfg(unix)]
    {
        let deadline = Instant::now() + EXPORT_STOP_GRACE;
        while Instant::now() < deadline && export_group_alive(pgid) {
            std::thread::sleep(POLL_INTERVAL);
        }
        if export_group_alive(pgid) {
            log::warn!("desktop: 导出进程优雅停超时,升级 SIGKILL 进程组 -{pgid}");
            force_kill_export_group(pgid);
        }
    }
}

// ---------------------------------------------------------------------------
// 错误信封 + 桥上下文(home/bin 探测;resolve_bridge_context 的本地孪生,
// bridge_bin_path 复用 pub 件)
// ---------------------------------------------------------------------------

fn error_value(code: &str, message: &str) -> String {
    json!({"code": code, "path": "$", "message": message}).to_string()
}

fn resolve_export_bridge_context(
    app: &AppHandle,
) -> Result<(PathBuf, Option<PathBuf>), String> {
    let home = app
        .path()
        .home_dir()
        .map_err(|e| error_value("internal_error", &format!("用户 home 目录不可解析: {e}")))?;
    let bin = crate::wechat_keyprovider::bridge_bin_path(&home);
    if !(bin.is_file() && is_executable(&bin)) {
        return Err(error_value(
            "component_missing",
            &format!("微信本机桥组件未安装或不可执行: {}", bin.display()),
        ));
    }
    let myia_home_env = if std::env::var_os("MYIA_HOME").is_some() {
        None
    } else {
        Some(
            crate::data_root(app)
                .map_err(|e| error_value("internal_error", &format!("数据根不可解析: {e}")))?,
        )
    };
    Ok((bin, myia_home_env))
}

#[cfg(unix)]
fn is_executable(path: &Path) -> bool {
    use std::os::unix::fs::PermissionsExt;
    path.is_file()
        && std::fs::metadata(path)
            .map(|meta| meta.permissions().mode() & 0o111 != 0)
            .unwrap_or(false)
}

#[cfg(not(unix))]
fn is_executable(path: &Path) -> bool {
    path.is_file()
}

// ---------------------------------------------------------------------------
// 编排核心(spawn 桥 + 逐行转事件 + 终态回执;阻塞,命令面 spawn_blocking
// 包裹,单测直驱假桥脚本)
// ---------------------------------------------------------------------------

/// 编排结果:终态信封(桥回执原样)或取消合成信封。
#[derive(Debug)]
enum ExportOutcome {
    /// 桥终态行原样(`{"export":…}` / `{"error":…}` / `{"verify":…}`)。
    Receipt(Value),
    /// 桥被杀未见终态(SIGKILL 段):合成取消信封(前端按 error 呈现)。
    Cancelled,
    /// 空闲超帽 / spawn 失败 / 未回执退出(人话错误信封文本)。
    Failed(String),
}

/// 编排核心:spawn(独立进程组)→ stdout 逐行读(空闲帽)→ progress 行
/// emit 回调 → 终态信封。取消 = 取消面 take 槽置旗标停组;本循环见旗标
/// 即停读等子进程退出(SIGTERM 段桥自清 staging 回错误信封,SIGKILL 段
/// 合成 Cancelled)。
fn run_chat_export<F>(
    bin: &Path,
    params: &ChatExportParams,
    myia_home_env: Option<PathBuf>,
    jobs: &ExportJobTable,
    mut emit: F,
) -> ExportOutcome
where
    F: FnMut(u64, u64, Value),
{
    let argv = build_export_argv(params);
    let (job_id, cancel_flag) = jobs.register();
    let mut command = Command::new(bin);
    command
        .args(&argv)
        .stdin(Stdio::null())
        .stdout(Stdio::piped())
        .stderr(Stdio::piped())
        // 桥启动器自设组件根 PYTHONPATH;壳继承的会干扰组件依赖解析
        // (key-acquire B5 同款纪律)。
        .env_remove("PYTHONPATH");
    if let Some(root) = &myia_home_env {
        command.env("MYIA_HOME", root);
    }
    #[cfg(unix)]
    {
        use std::os::unix::process::CommandExt;
        // 独立进程组:取消的组信号可达桥整树,不误伤壳自身会话。
        command.process_group(0);
    }
    let mut child = match command.spawn() {
        Ok(child) => child,
        Err(err) => {
            jobs.finish(job_id);
            return ExportOutcome::Failed(error_value(
                "spawn_failed",
                &format!("导出命令拉起失败({}): {err}", bin.display()),
            ));
        }
    };
    jobs.set_pgid(job_id, child.id());
    log::info!(
        "desktop: 聊天记录导出启动 job={job_id} chat={} format={} all={}",
        params.chat_id,
        params.format,
        params.all
    );
    // start 事件恒先于桥行:前端可靠捕获 job_id(取消面寻址键)。
    emit(
        job_id,
        0,
        json!({"progress": {"phase": "starting", "rows": 0}}),
    );
    let stdout_pipe = child.stdout.take().expect("piped stdout");
    let stderr_pipe = child.stderr.take().expect("piped stderr");
    let (tx, rx) = mpsc::channel::<String>();
    let reader = std::thread::spawn(move || {
        for line in std::io::BufReader::new(stdout_pipe).lines() {
            match line {
                Ok(text) => {
                    if tx.send(text).is_err() {
                        break;
                    }
                }
                Err(_) => break,
            }
        }
    });
    let stderr_tail = std::thread::spawn(move || {
        let mut tail = String::new();
        if let Ok(lines) = std::io::BufReader::new(stderr_pipe)
            .lines()
            .collect::<Result<Vec<_>, _>>()
        {
            for line in lines.iter().rev().take(3) {
                tail.push_str(line);
                tail.push('\n');
            }
        }
        tail
    });
    let mut machine = ExportLineMachine::new();
    let mut seq: u64 = 0;
    let outcome: ExportOutcome; // 各 break 路径必赋值(编译器核验)
    let mut reader = Some(reader);
    // 空闲帽(非总帽):每收到一行重置 —— 全库导出可长,只有真静默才判挂死。
    let mut idle_deadline = Instant::now() + EXPORT_IDLE_CAP;
    loop {
        if cancel_flag.load(Ordering::SeqCst) {
            stop_export_group(child.id());
            outcome = ExportOutcome::Cancelled;
            break;
        }
        let left = idle_deadline.saturating_duration_since(Instant::now());
        if left.is_zero() {
            stop_export_group(child.id());
            outcome = ExportOutcome::Failed(error_value(
                "bridge_timeout",
                "导出桥 900 秒无输出(疑似挂死),已终止;可重试",
            ));
            break;
        }
        match rx.recv_timeout(left.min(Duration::from_millis(250))) {
            Ok(line) => {
                idle_deadline = Instant::now() + EXPORT_IDLE_CAP;
                if let Some(progress) = machine.feed(&line) {
                    seq += 1;
                    emit(job_id, seq, progress);
                } else if let Some(envelope) = machine.envelope.clone() {
                    outcome = ExportOutcome::Receipt(envelope);
                    break;
                }
            }
            Err(mpsc::RecvTimeoutError::Timeout) => continue,
            Err(mpsc::RecvTimeoutError::Disconnected) => {
                // stdout EOF:等桥退出收终态(信封已收 = 正常;否则按退出码兜底)
                let _ = reader.take().map(|handle| handle.join());
                let status = child.wait();
                let tail = stderr_tail.join().unwrap_or_default();
                if let Some(envelope) = machine.envelope.clone() {
                    outcome = ExportOutcome::Receipt(envelope);
                } else if cancel_flag.load(Ordering::SeqCst) {
                    outcome = ExportOutcome::Cancelled;
                } else {
                    let code = status.ok().and_then(|s| s.code());
                    outcome = ExportOutcome::Failed(error_value(
                        "bridge_error",
                        &format!(
                            "导出桥未返回回执(exit={});stderr 尾部: {tail}",
                            code.map(|c| c.to_string()).unwrap_or_else(|| "信号终止".into())
                        ),
                    ));
                }
                break;
            }
        }
    }
    // 收割(读侧已断/取消路径的垂死子进程;kill+wait 必返)
    let _ = child.kill();
    let _ = child.wait();
    let _ = reader.take().map(|handle| handle.join());
    jobs.finish(job_id);
    log::info!(
        "desktop: 聊天记录导出结束 job={job_id} progress行={} 杂行={}",
        machine.progress_lines,
        machine.ignored_lines
    );
    outcome
}

// ---------------------------------------------------------------------------
// 命令面
// ---------------------------------------------------------------------------

/// 聊天记录导出(R6):目录对话框(缺省)→ spawn 桥 → NDJSON 进度事件 →
/// 终态回执原样转前端。应答 `Option`:`null` = 用户取消目录选择(静默);
/// 对象 = 桥终态行(`{"export":…}` 成功 / `{"error":…}` 桥侧失败)。
#[tauri::command]
pub async fn wechat_chat_export(
    app: AppHandle,
    chat_id: String,
    format: String,
    out_dir: Option<String>,
    from_ts: Option<i64>,
    to_ts: Option<i64>,
    types: Option<Vec<String>>,
    sender: Option<String>,
    display_name_pref: Option<String>,
    name_mode: Option<String>,
    all: Option<bool>,
) -> Result<Option<Value>, String> {
    if !EXPORT_FORMATS.contains(&format.as_str()) {
        return Err(error_value(
            "invalid_params",
            &format!("不支持的导出格式 {format:?}(合法:{EXPORT_FORMATS:?})"),
        ));
    }
    let (bin, myia_home_env) = resolve_export_bridge_context(&app)?;
    // out_dir 缺省 = 壳内目录对话框;取消 = Ok(null) 静默零 spawn
    // (wechat_group_export 对话框取消判例同款;blocking_pick_folder 禁
    // 主线程 → spawn_blocking 弹,插件内部自 hop main thread)。
    let picked_dir = match out_dir {
        Some(dir) => Some(PathBuf::from(dir)),
        None => {
            let dialog_app = app.clone();
            let joined = tauri::async_runtime::spawn_blocking(move || {
                dialog_app.dialog().file().blocking_pick_folder()
            });
            match joined.await {
                Ok(Some(file)) => Some(file.into_path().map_err(|err| {
                    error_value("export_failed", &format!("所选目录不可用: {err}"))
                })?),
                Ok(None) => None,
                Err(err) => {
                    return Err(error_value(
                        "internal_error",
                        &format!("导出目录对话框线程失败: {err}"),
                    ))
                }
            }
        }
    };
    let Some(out_dir_path) = picked_dir else {
        log::info!("desktop: 聊天记录导出:用户取消目录选择,静默返回零 spawn");
        return Ok(None);
    };
    let params = ChatExportParams {
        chat_id,
        format,
        out_dir: out_dir_path,
        from_ts,
        to_ts,
        types: types.unwrap_or_default(),
        sender,
        display_name_pref,
        name_mode,
        all: all.unwrap_or(false),
    };
    let emit_app = app.clone();
    let joined = tauri::async_runtime::spawn_blocking(move || {
        let emit = move |job_id: u64, seq: u64, body: Value| {
            let _ = emit_app.emit(
                WECHAT_CHAT_EXPORT_EVENT,
                json!({"job_id": job_id, "seq": seq, "body": body}),
            );
        };
        run_chat_export(&bin, &params, myia_home_env, &EXPORT_JOBS, emit)
    });
    match joined.await {
        Ok(ExportOutcome::Receipt(receipt)) => Ok(Some(receipt)),
        Ok(ExportOutcome::Cancelled) => Ok(Some(json!({
            "error": {"code": "export_cancelled", "message": "导出已取消(staging 已由桥清理)"}
        }))),
        Ok(ExportOutcome::Failed(error)) => Err(error),
        Err(err) => Err(error_value(
            "internal_error",
            &format!("导出编排线程失败: {err}"),
        )),
    }
}

/// 取消进行中的导出(job_id 寻址;进度事件首条携带)。无该 job = 如实
/// `{ok:false}`(UI 竞态兜底,不造事件)。
#[tauri::command]
pub async fn wechat_chat_export_cancel(job_id: u64) -> Result<Value, String> {
    let cancelled = tauri::async_runtime::spawn_blocking(move || EXPORT_JOBS.cancel(job_id));
    match cancelled.await {
        Ok(true) => {
            log::info!("desktop: 聊天记录导出已取消 job={job_id}(组信号已发)");
            Ok(json!({"ok": true}))
        }
        Ok(false) => Ok(json!({"ok": false, "note": "该导出任务不在进行中(已完成或不存在)"})),
        Err(err) => Err(error_value(
            "internal_error",
            &format!("导出取消线程失败: {err}"),
        )),
    }
}

// ---------------------------------------------------------------------------
// 单测(纯函数 + 假桥脚本端到端;零真桥零真库)
// ---------------------------------------------------------------------------

#[cfg(test)]
mod tests {
    use super::*;

    /// argv 全参形状(纯函数;--json 前置 = key-acquire 判例)。
    #[test]
    fn export_argv_carries_filters_in_order() {
        let params = ChatExportParams {
            chat_id: "50438708676@chatroom".into(),
            format: "xlsx".into(),
            out_dir: PathBuf::from("/tmp/out"),
            from_ts: Some(1_760_000_000),
            to_ts: Some(1_760_100_000),
            types: vec!["text".into(), "file".into()],
            sender: Some("wxid_a".into()),
            display_name_pref: Some("nickname-first".into()),
            name_mode: Some("date-range".into()),
            all: true,
        };
        let argv = build_export_argv(&params);
        assert_eq!(
            argv,
            vec![
                "localdb", "export", "50438708676@chatroom", "--format", "xlsx",
                "--out", "/tmp/out", "--json", "--from-ts", "1760000000",
                "--to-ts", "1760100000", "--types", "text,file", "--sender",
                "wxid_a", "--display-name-pref", "nickname-first", "--name-mode",
                "date-range", "--all",
            ]
        );
        // 最小参形状
        let minimal = ChatExportParams {
            chat_id: "filehelper".into(),
            format: "json".into(),
            out_dir: PathBuf::from("/o"),
            from_ts: None,
            to_ts: None,
            types: vec![],
            sender: None,
            display_name_pref: None,
            name_mode: None,
            all: false,
        };
        assert_eq!(
            build_export_argv(&minimal),
            vec!["localdb", "export", "filehelper", "--format", "json", "--out", "/o", "--json"]
        );
    }

    /// 行状态机:progress 透传 / 终态信封收首条 / 杂行计数(key-acquire
    /// `AcquireLineMachine` 同族语义)。
    #[test]
    fn line_machine_passes_progress_and_keeps_first_envelope() {
        let mut machine = ExportLineMachine::new();
        assert!(machine.feed("").is_none());
        assert!(machine.feed("不是 JSON").is_none());
        let progress = machine
            .feed("{\"progress\":{\"phase\":\"write\",\"rows\":500}}")
            .expect("progress 行透传");
        assert_eq!(progress["progress"]["rows"], json!(500));
        let receipt = machine.feed("{\"export\":{\"total_rows\":500}}");
        assert!(receipt.is_none(), "终态信封不透传(回执归返回值)");
        assert!(machine.feed("{\"export\":{\"total_rows\":999}}").is_none());
        assert!(machine.feed("{\"error\":{\"code\":\"usage\"}}").is_none());
        assert_eq!(machine.progress_lines, 1);
        assert_eq!(machine.ignored_lines, 4); // 空行 + 非 JSON + 第二条信封 + 已收后的 error 信封
        assert_eq!(machine.envelope.as_ref().unwrap()["export"]["total_rows"], json!(500));
    }

    /// job 表:登记 → 回填 pgid → 取消 take;unknown job 如实 false。
    #[test]
    fn job_table_register_cancel_and_unknown() {
        let table = ExportJobTable::new();
        let (job_id, flag) = table.register();
        table.set_pgid(job_id, 4242);
        assert!(!flag.load(Ordering::SeqCst));
        assert!(table.cancel(job_id));
        assert!(flag.load(Ordering::SeqCst));
        assert!(!table.cancel(job_id), "已取消/未知 job 如实 false");
        let (other, _flag) = table.register();
        table.finish(other);
        assert!(!table.cancel(other));
    }

    /// 假桥端到端:NDJSON progress 流 + 回执行 → 事件序 + 回执原样;
    /// 假桥 = mktemp shell 脚本(零真桥零真库)。
    #[test]
    #[cfg(unix)]
    fn fake_bridge_stream_emits_events_and_returns_receipt() {
        use std::io::Write;
        let dir = tempfile::tempdir().unwrap();
        let script = dir.path().join("fake-bridge.sh");
        let mut fh = std::fs::File::create(&script).unwrap();
        writeln!(
            fh,
            "#!/bin/sh\n\
             echo '{{\"progress\":{{\"phase\":\"scan\",\"rows\":0}}}}'\n\
             echo '{{\"progress\":{{\"phase\":\"write\",\"rows\":1200}}}}'\n\
             echo '{{\"export\":{{\"total_rows\":1200,\"manifest_path\":\"/tmp/m.json\"}}}}'\n\
             exit 0"
        )
        .unwrap();
        drop(fh);
        use std::os::unix::fs::PermissionsExt;
        std::fs::set_permissions(&script, std::fs::Permissions::from_mode(0o755)).unwrap();
        let params = ChatExportParams {
            chat_id: "c@chatroom".into(),
            format: "json".into(),
            out_dir: dir.path().join("out"),
            from_ts: None,
            to_ts: None,
            types: vec![],
            sender: None,
            display_name_pref: None,
            name_mode: None,
            all: false,
        };
        let table = ExportJobTable::new();
        let events: std::sync::Mutex<Vec<(u64, u64, Value)>> = std::sync::Mutex::new(vec![]);
        let outcome = run_chat_export(&script, &params, None, &table, |job, seq, body| {
            events.lock().unwrap().push((job, seq, body));
        });
        match outcome {
            ExportOutcome::Receipt(receipt) => {
                assert_eq!(receipt["export"]["total_rows"], json!(1200))
            }
            other => panic!("期望回执,得到 {other:?}"),
        }
        let events = events.into_inner().unwrap();
        // start 合成事件 + 两条桥 progress(事件体 = 桥行原样)
        assert_eq!(events.len(), 3);
        assert_eq!(events[0].1, 0, "start 事件 seq=0 恒先发(job_id 寻址键)");
        assert_eq!(events[0].2["progress"]["phase"], json!("starting"));
        assert_eq!(events[1].2["progress"]["rows"], json!(0));
        assert_eq!(events[2].2["progress"]["rows"], json!(1200));
        assert!(events[0].0 > 0);
        assert!(table.cancel(events[0].0) == false, "完成后 job 已摘");
    }

    /// 假桥失败:exit 非 0 且无终态信封 → bridge_error 兜底(stderr 尾部)。
    #[test]
    #[cfg(unix)]
    fn fake_bridge_death_without_receipt_maps_to_error() {
        use std::io::Write;
        let dir = tempfile::tempdir().unwrap();
        let script = dir.path().join("die.sh");
        let mut fh = std::fs::File::create(&script).unwrap();
        writeln!(fh, "#!/bin/sh\necho boom >&2\nexit 3").unwrap();
        drop(fh);
        use std::os::unix::fs::PermissionsExt;
        std::fs::set_permissions(&script, std::fs::Permissions::from_mode(0o755)).unwrap();
        let params = ChatExportParams {
            chat_id: "c".into(),
            format: "txt".into(),
            out_dir: dir.path().join("o"),
            from_ts: None,
            to_ts: None,
            types: vec![],
            sender: None,
            display_name_pref: None,
            name_mode: None,
            all: false,
        };
        let outcome = run_chat_export(&script, &params, None, &ExportJobTable::new(), |_, _, _| {});
        match outcome {
            ExportOutcome::Failed(message) => {
                assert!(message.contains("bridge_error"), "{message}");
                assert!(message.contains("exit=3"), "{message}");
            }
            other => panic!("期望失败兜底,得到 {other:?}"),
        }
    }
}
