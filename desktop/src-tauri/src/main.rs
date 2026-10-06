// MYIA 桌面壳:Tauri 2 窗口 + 持久 Python sidecar(stdin/stdout JSON-RPC)胶水。
// 协议权威定义:desktop/entry.py 模块注释 —— 请求行 {"id",method,params} →
// 应答行 {"id",result|{error:{code,path,message}}};无 id 的 {"type": …} 行是
// 流式事件(log/progress/completed),原样转发为 Tauri 事件 `sidecar://event`。
// 前端唯一入口:invoke("sidecar_request", { method, params })。
// spawn 源(10-05-desktop-managed-py-env 第 2 步)已切自管 Python 环境:
// `<数据根>/python/bin/python3 -m myssia_desktop_entry`(PYTHONPATH=随包源码),
// 环境探测/IPC/空态事件见 pyenv.rs;旧冻结 sidecar 链待第 7 步打包收口退役。
#![cfg_attr(not(debug_assertions), windows_subsystem = "windows")]

mod pyenv;
mod pyenv_components;
mod pyenv_install;
mod pyenv_migration;

use std::collections::HashMap;
use std::path::PathBuf;
use std::sync::atomic::{AtomicU64, Ordering};
use std::sync::Mutex;
use std::time::{Duration, Instant};

use serde_json::{json, Value};
use tauri::{AppHandle, Emitter, Listener, Manager, State};
use tauri_plugin_log::{RotationStrategy, Target, TargetKind, TimezoneStrategy};
use tauri_plugin_shell::process::{CommandChild, CommandEvent};
use tauri_plugin_shell::ShellExt;

// ---------------------------------------------------------------------------
// 壳日志(10-07-unified-logging 批2;design §6)
// ---------------------------------------------------------------------------

/// 壳/UI 共用日志文件名(tauri-plugin-log;活动文件恒 `shell.log`,按大小
/// 轮转归档 `shell_<YYYY-MM-DD_HH-MM-SS>.log`——源码 LOG_DATE_FORMAT/
/// rename_file_to_dated 真名复核,UseLocal 本地墙钟)。
const SHELL_LOG_FILE_NAME: &str = "shell";
/// 壳日志单文件上限(决议⑥:5MB;plugin 默认 40_000 字节过小必调)。
const SHELL_LOG_MAX_FILE_SIZE: u128 = 5 * 1024 * 1024;
/// 壳归档保留天数(design §4:与 Python 侧 RETENTION_DAYS=7 同值各持一份,
/// 不加 UI/env 旋钮)。
const SHELL_LOG_RETENTION_DAYS: u64 = 7;

/// 流式事件转发到前端所用的事件名。
const SIDECAR_EVENT: &str = "sidecar://event";
/// 壳层 sidecar 生命周期状态事件(C2 respawn;壳自发,非 sidecar 协议)。
/// 载荷 {state: "respawning"|"online"|"dead", attempt?, respawned?}。
const SIDECAR_STATE_EVENT: &str = "sidecar://state";
/// 单请求应答超时(run.start 立即返回;doctor 带代理探测时最重)。
const REQUEST_TIMEOUT: Duration = Duration::from_secs(120);
/// 自动 respawn 上限(超过转手动;退避序列 1/2/4/8/16s)。
const RESPAWN_MAX_ATTEMPTS: u32 = 5;
const RESPAWN_BASE_DELAY: Duration = Duration::from_secs(1);
/// respawn 后稳定存活该时长 → attempts 归零(下轮退避从头计)。
const RESPAWN_STABLE_AFTER: Duration = Duration::from_secs(10);

/// 第 n 次尝试的退避时长:1s·2^(n-1) → 1/2/4/8/16s(saturating,不溢出)。
fn backoff_delay(attempt: u32) -> Duration {
    RESPAWN_BASE_DELAY * 2u32.saturating_pow(attempt.saturating_sub(1))
}

struct Sidecar {
    child: Mutex<Option<CommandChild>>,
    /// id → 应答回递通道(pump 线程 demux 后回填)。
    pending: Mutex<HashMap<u64, tauri::async_runtime::Sender<Result<Value, Value>>>>,
    next_id: AtomicU64,
    /// 自动 respawn 已尝试次数(Terminated +1;稳定存活归零;手动拉起归零)。
    respawn_attempts: Mutex<u32>,
}

/// sidecar 常驻进程:自管 python `-m myssia_desktop_entry`(serve 协议),
/// 启动时 spawn,pump 任务独占消费其 stdout。
#[tauri::command]
async fn sidecar_request(
    app: AppHandle,
    state: State<'_, Sidecar>,
    method: String,
    params: Option<Value>,
) -> Result<Value, String> {
    let id = state.next_id.fetch_add(1, Ordering::SeqCst);
    let (tx, mut rx) = tauri::async_runtime::channel::<Result<Value, Value>>(1);
    state.pending.lock().unwrap().insert(id, tx);
    let request = json!({"id": id, "method": method, "params": params.unwrap_or(json!({}))});
    let write = {
        let mut guard = state.child.lock().unwrap();
        match guard.as_mut() {
            Some(child) => child.write(format!("{request}\n").as_bytes()).map_err(|e| e.to_string()),
            // 进程未运行两分源:环境未就绪(未配置/安装中/异常)→ 协议层报
            // 结构化 pyenv_not_ready(prd Req3,带 status 数据)——原样直出
            // 不再套 sidecar_not_running 信封(AC2 嵌套包装缺陷:真机实证
            // 前端只见外层码,路由/引导无从辨识,屏上整块 JSON blob 裸奔);
            // 其余维持进程级 sidecar_not_running(崩溃待 respawn/手动拉起)。
            None => match pyenv::unready_error(&app) {
                Some(error) => {
                    state.pending.lock().unwrap().remove(&id);
                    return Err(error.to_string());
                }
                None => Err("sidecar 进程未运行".into()),
            },
        }
    };
    if let Err(message) = write {
        state.pending.lock().unwrap().remove(&id);
        return Err(json!({"code": "sidecar_not_running", "path": "$", "message": message}).to_string());
    }
    match tokio::time::timeout(REQUEST_TIMEOUT, rx.recv()).await {
        Ok(Some(Ok(result))) => Ok(result),
        Ok(Some(Err(error))) => Err(error.to_string()), // 结构化错误对象原样给前端
        Ok(None) => Err(json!({"code": "sidecar_dropped", "path": "$",
            "message": "sidecar 应答通道关闭(进程可能已退出)"}).to_string()),
        Err(_) => {
            state.pending.lock().unwrap().remove(&id);
            Err(json!({"code": "sidecar_timeout", "path": "$",
                "message": "sidecar 应答超时(120s)"}).to_string())
        }
    }
}

/// stdout 单行分拣:有 type → 事件转发;有 id → 回递 pending 请求。
fn handle_stdout_line(app: &AppHandle, line: &str) {
    let parsed: Value = match serde_json::from_str(line) {
        Ok(value) => value,
        Err(e) => {
            log::warn!("sidecar stdout 非 JSON 行(忽略): {e}: {line}");
            return;
        }
    };
    if parsed.get("type").is_some() {
        let _ = app.emit(SIDECAR_EVENT, parsed);
        return;
    }
    if let Some(id) = parsed.get("id").and_then(Value::as_u64) {
        let state = app.state::<Sidecar>();
        let sender = state.pending.lock().unwrap().remove(&id);
        drop(state);
        if let Some(tx) = sender {
            let reply = match parsed.get("error") {
                Some(error) => Err(error.clone()),
                None => Ok(parsed.get("result").cloned().unwrap_or(Value::Null)),
            };
            let _ = tx.try_send(reply); // 容量 1,接收方未 recv 也进缓冲
        } else {
            // 迟到应答:请求已超时移除(sidecar_timeout 已回前端)。不留痕的
            // 静默丢弃会掩盖「壳超时 < sidecar 实际耗时」的配置问题,大声说出来。
            log::warn!(
                "sidecar 迟到应答(请求已超时移除,丢弃) id={id} method={:?}",
                parsed.get("method").and_then(Value::as_str).unwrap_or("?")
            );
        }
    }
}

fn pump_task(app: AppHandle, mut rx: tauri::async_runtime::Receiver<CommandEvent>) {
    tauri::async_runtime::spawn(async move {
        while let Some(event) = rx.recv().await {
            match event {
                CommandEvent::Stdout(bytes) => {
                    handle_stdout_line(&app, &String::from_utf8_lossy(&bytes));
                }
                CommandEvent::Stderr(bytes) => {
                    // sidecar stderr(模块 WARNING+/崩溃 traceback)在装机件上的
                    // 唯一落点:批2 design §6 钉死 warn 级落 shell.log。
                    log::warn!("sidecar stderr: {}", String::from_utf8_lossy(&bytes));
                }
                CommandEvent::Error(message) => log::warn!("sidecar 错误: {message}"),
                CommandEvent::Terminated(payload) => {
                    log::warn!(
                        "sidecar 退出: code={:?} signal={:?}",
                        payload.code,
                        payload.signal
                    );
                    let state = app.state::<Sidecar>();
                    *state.child.lock().unwrap() = None;
                    // drop(child 关闭管道 = stdin EOF,serve 循环干净退出;
                    // 遗留 python 孤儿靠此自清 —— design §2.1② 注记,冒烟核)
                    {
                        let mut pending = state.pending.lock().unwrap();
                        for (_, tx) in pending.drain() {
                            let _ = tx.try_send(Err(json!({"code": "sidecar_terminated", "path": "$",
                                "message": "sidecar 进程已退出"})));
                        }
                    }
                    drop(state);
                    schedule_respawn(app.clone());
                }
                _ => {}
            }
        }
    });
}

/// 拉起 sidecar(setup 首启 / 自动 respawn / 手动 sidecar_restart 三处共用)。
/// spawn 后即起 pump 任务独占消费其 stdout;MYIA_HOME 注入规则同 v1.1.1。
/// 第 2 步起 spawn 源切自管 Python 环境(design §4):
/// `<数据根>/python/bin/python3 -m myssia_desktop_entry serve`(win 为
/// python.exe;serve 尾参是第 1 步入口模块 argv 契约——无参直通 CLI 空.help
/// 退出 0,sidecar 起即死,见 pyenv::ENTRY_ARGS),PYTHONPATH=随包
/// Resources/myssia-src(开发 Python 与应用 Python 分家,Req 4)。
/// 环境未就绪 → PyenvNotReadyError(结构化携带 status;setup/respawn 路径
/// downcast 识别后转空态事件,不当 io 失败重试)。
fn spawn_sidecar(app: &AppHandle) -> Result<CommandChild, Box<dyn std::error::Error>> {
    let data_root = data_root(app)?;
    let resource_dir = app.path().resource_dir()?;
    let installing = app.state::<pyenv::PyenvManager>().installing.lock().unwrap().clone();
    let status = pyenv::status_at(
        &data_root,
        Some(&resource_dir),
        installing.as_deref(),
        &pyenv::read_settings(&data_root),
    );
    if !pyenv::spawnable(status.state) {
        return Err(Box::new(pyenv::PyenvNotReadyError(status)));
    }
    let mut command = app
        .shell()
        .command(pyenv::python_bin_path(&data_root))
        .args(pyenv::ENTRY_ARGS) // RPC serve 模式;直通模式留给 CLI 场景
        .env("PYTHONPATH", pyenv::resource_src_dir(&resource_dir));
    // MYIA_HOME 注入尊重用户显式设置(自动化/自定位数据根的逃生口):
    // 已设则原样继承,不夺权;未设才计算平台根并注入 + 预建目录。
    if std::env::var_os("MYIA_HOME").is_none() {
        command = command.env("MYIA_HOME", &data_root);
    }
    // app/bundle 版本注入(C10):单一事实源 = tauri.conf.json 的 version
    // (package_info),sidecar `version` 应答透传为 app_version 字段;
    // 开发态缺省同源(与 .app 版本天然一致,无需另维护常量)。
    let app_version = app.package_info().version.to_string();
    command = command.env("MYIA_APP_VERSION", app_version);
    // 随包插件组件包目录锚点(10-05-bundled-plugins-install):release 且用户
    // 未显式设置才注入 MYIA_BUNDLED_PLUGINS=Resources/plugins(dev 构建定死
    // 不注入,dev 空表是稳定契约;已设原样继承不夺权,MYIA_HOME 同款惯例)。
    // 发现/一键安装走 sidecar plugins.bundled.* 单一事实源,UI 零 resourceDir 直查。
    if let Some(dir) = pyenv::bundled_plugins_env_value(
        &resource_dir,
        std::env::var_os(pyenv::BUNDLED_PLUGINS_ENV).is_some(),
        cfg!(debug_assertions),
    ) {
        command = command.env(pyenv::BUNDLED_PLUGINS_ENV, dir);
    }
    // crawl4ai 组件浏览器目录注入(10-06-native-plugin-components 轨A):
    // 组件装的 chromium 落数据根 playwright-browsers/,sidecar 及其子进程
    // (urlwatch ShellJob 的 render_crawl4ai.py、L3 引擎进程内驱动)经
    // PLAYWRIGHT_BROWSERS_PATH 找到二进制——装与用同源(pyenv_install 同目录)。
    // 目录在才注(未装组件零行为差,playwright 各回自家缺省位置,不夺
    // uvx 自管型 stealth_browser 的浏览器发现面);已设原样继承不夺权
    // (MYIA_HOME 同款惯例)。
    if std::env::var_os("PLAYWRIGHT_BROWSERS_PATH").is_none()
        && pyenv_components::should_inject_browsers_env(&data_root)
    {
        command = command.env(
            "PLAYWRIGHT_BROWSERS_PATH",
            pyenv_components::playwright_browsers_path(&data_root),
        );
    }
    let (rx, child) = command.spawn()?;
    pump_task(app.clone(), rx);
    Ok(child)
}

/// 自动 respawn:指数退避(1/2/4/8/16s),超 5 次转手动(dead 态);spawn 失败
/// 按同序列自驱重试;稳定存活 10s 归零计数。锁内复核 child 仍空才 spawn,
/// 防与手动拉起双 spawn(C2)。
fn schedule_respawn(app: AppHandle) {
    tauri::async_runtime::spawn(async move {
        loop {
            let attempt = {
                let state = app.state::<Sidecar>();
                let mut guard = state.respawn_attempts.lock().unwrap();
                *guard += 1;
                *guard
            };
            if attempt > RESPAWN_MAX_ATTEMPTS {
                let _ = app.emit(
                    SIDECAR_STATE_EVENT,
                    json!({"state": "dead", "attempt": attempt - 1}),
                );
                log::warn!(
                    "desktop: sidecar 自动 respawn 超限(连续 {}/{RESPAWN_MAX_ATTEMPTS}),转手动拉起",
                    attempt - 1
                );
                return;
            }
            let _ = app.emit(SIDECAR_STATE_EVENT, json!({"state": "respawning", "attempt": attempt}));
            log::warn!(
                "desktop: sidecar 将在 {:?} 后自动 respawn(第 {attempt} 次)",
                backoff_delay(attempt)
            );
            tokio::time::sleep(backoff_delay(attempt)).await;
            {
                let state = app.state::<Sidecar>();
                let mut child_guard = state.child.lock().unwrap();
                if child_guard.is_some() {
                    // 手动拉起已抢先复活,本任务退出防双 spawn
                    return;
                }
                match spawn_sidecar(&app) {
                    Ok(child) => *child_guard = Some(child),
                    Err(error) => {
                        if let Some(not_ready) = error.downcast_ref::<pyenv::PyenvNotReadyError>() {
                            // 环境在运行途中转未就绪(数据根被清/戳被改判):
                            // 重试不会让环境就绪,转空态事件走 UI 引导(D2),
                            // 本任务退出(sidecar://state 停在 respawning 是刻意的:
                            // pyenv 空态事件才是此刻的真相,拉起按钮救不了环境)。
                            let _ = app.emit(pyenv::PYENV_STATUS_EVENT, &not_ready.0);
                            let _ = app.emit(pyenv::PYENV_NOT_READY_EVENT, &not_ready.0);
                            log::warn!("desktop: {not_ready};停止自动 respawn");
                            return;
                        }
                        log::warn!("desktop: sidecar respawn 失败(第 {attempt} 次): {error}");
                        continue; // attempts 已 +1,下一轮更长退避直至 dead
                    }
                }
            }
            let _ = app.emit(SIDECAR_STATE_EVENT, json!({"state": "online", "respawned": true}));
            log::info!("desktop: sidecar 自动 respawn 成功(第 {attempt} 次)");
            // 稳定计时:存活满 10s → attempts 归零(又死则 Terminated 走更长退避)。
            // *guard == attempt 复核:稳定窗口内若又死(Terminated 已 +1)或手动
            // 拉起已归零,本任务不得抢先归零(防两代 respawn 任务交错重置)。
            tokio::time::sleep(RESPAWN_STABLE_AFTER).await;
            let state = app.state::<Sidecar>();
            let mut attempts_guard = state.respawn_attempts.lock().unwrap();
            if *attempts_guard == attempt && state.child.lock().unwrap().is_some() {
                *attempts_guard = 0;
            }
            return;
        }
    });
}

/// 空闲则拉起 sidecar(幂等:进程健在直接返回,绝不杀活进程)。
/// 手动 sidecar_restart 与安装链就绪(pyenv_install 第 3 步)共用:
/// 安装完成 → 环境转 ready → 常驻 sidecar 无需等前端动作即起(AC1 主链)。
fn spawn_sidecar_if_idle(app: &AppHandle) -> Result<bool, Box<dyn std::error::Error>> {
    let state = app.state::<Sidecar>();
    let mut child_guard = state.child.lock().unwrap();
    if child_guard.is_some() {
        return Ok(false);
    }
    let child = spawn_sidecar(app)?;
    *child_guard = Some(child);
    drop(child_guard);
    *state.respawn_attempts.lock().unwrap() = 0;
    let _ = app.emit(
        SIDECAR_STATE_EVENT,
        json!({"state": "online", "respawned": false}),
    );
    Ok(true)
}

/// 手动拉起 sidecar(dead 态顶栏「拉起」按钮 / reprobe 升级链路;C2)。
/// 幂等:进程健在直接回 restarted=false,绝不杀活进程。
#[tauri::command]
async fn sidecar_restart(app: AppHandle) -> Result<Value, String> {
    let restarted = spawn_sidecar_if_idle(&app).map_err(|e| e.to_string())?;
    Ok(json!({ "restarted": restarted }))
}

/// 壳侧数据根解析(spawn 注入/自管环境探测共用,与 spawn 的 MYIA_HOME 注入
/// 规则同源):显式 `MYIA_HOME` env 尊重用户设置原样继承(自动化/自定位数据根
/// 的逃生口;entry.py `_serve_context` 同优先级链);未设才计算平台根并预建目录。
fn data_root(app: &AppHandle) -> Result<PathBuf, Box<dyn std::error::Error>> {
    if let Some(home) = std::env::var_os("MYIA_HOME") {
        return Ok(PathBuf::from(home));
    }
    myssia_home_dir(app)
}

/// MYIA 应用数据根(v1.1.1 桌面数据通路统一,与 entry.py `myssia_home()` 同路径):
/// macOS `~/Library/Application Support/MYIA` / Windows `%APPDATA%\MYIA`
/// (按 Roaming 惯例拼,APPDATA 重定向的边缘形态由 Python 侧 APPDATA env 兜底)
/// / Linux `~/.myia`。spawn sidecar 时经 `MYIA_HOME` env 注入 —— 桌面上下文
/// 的路径解析一处定案;sidecar 自带 .app bundle 探测作双保险。
fn myssia_home_dir(app: &AppHandle) -> Result<PathBuf, Box<dyn std::error::Error>> {
    let home = app.path().home_dir()?;
    let dir = home.join(platform_data_root_suffix());
    std::fs::create_dir_all(&dir)?;
    Ok(dir)
}

/// 平台数据根后缀(相对用户 home):`myssia_home_dir`(AppHandle 路径解析)
/// 与启动期日志目录解析(`data_root_before_app`,plugin 注册前无 AppHandle)
/// 共用同一拼装规则——不引第二套路径规则(design §2 单一职责)。
fn platform_data_root_suffix() -> PathBuf {
    if cfg!(target_os = "macos") {
        PathBuf::from("Library/Application Support/MYIA")
    } else if cfg!(target_os = "windows") {
        PathBuf::from("AppData").join("Roaming").join("MYIA")
    } else {
        PathBuf::from(".myia")
    }
}

/// 启动期数据根解析(tauri builder 之前,无 AppHandle 可用):与 `data_root`
/// 同规则——显式 `MYIA_HOME` 尊重原样继承;未设按平台根。home 目录来源 =
/// `HOME`/`USERPROFILE` env(acquire_instance_lock 同款惯例;tauri path
/// resolver 的 home 同源于此,极端 home 覆写形态两者一致漂移,可接受)。
fn data_root_before_app() -> Result<PathBuf, Box<dyn std::error::Error>> {
    if let Some(home) = std::env::var_os("MYIA_HOME") {
        return Ok(PathBuf::from(home));
    }
    let home = std::env::var_os("HOME")
        .or_else(|| std::env::var_os("USERPROFILE"))
        .ok_or("用户 home 目录不可解析(HOME/USERPROFILE 均未设)")?;
    Ok(PathBuf::from(home).join(platform_data_root_suffix()))
}

/// 壳日志目录解析 + 预建:`<数据根>/logs/`(与 Python 侧统一日志同目录,
/// design §0)。不可解析/不可建 → None(降级仅 Stdout,不阻启动——plugin 的
/// Folder target 在目录不可建时会硬失败阻起壳,故预建前置在此吸收)。
fn resolve_shell_logs_dir() -> Option<PathBuf> {
    let dir = data_root_before_app().ok()?.join("logs");
    std::fs::create_dir_all(&dir).is_ok().then_some(dir)
}

/// 组装 tauri-plugin-log builder(design §6 配置包):
/// - targets:Folder(`<数据根>/logs/shell.log`)+ Stdout 双写(装机件无人读
///   stdout 亦无害;dev 终端可见);降级态(目录不可建)仅 Stdout;
/// - max_file_size 5MB(决议⑥)+ KeepAll(归档名时间戳,>7 天由壳启动
///   自清 `clean_stale_shell_archives`,plugin 自身无按天保留);
/// - timezone UseLocal(归档名/行时间戳本地时区)。⚠️ 该调用会重置 formatter
///   ——决议⑤壳格式沿 plugin 默认(不自造 format),故不再另设 format,
///   「timezone 在前 format 在后」顺序坑在此不触发,留注防后人踩;
/// - level Info(壳生命周期/安装链/respawn 留痕面;DEBUG 噪音不进装机件)。
fn shell_log_plugin(logs_dir: Option<&std::path::Path>) -> tauri_plugin_log::Builder {
    let builder = tauri_plugin_log::Builder::new()
        .level(log::LevelFilter::Info)
        .max_file_size(SHELL_LOG_MAX_FILE_SIZE)
        .rotation_strategy(RotationStrategy::KeepAll)
        .timezone_strategy(TimezoneStrategy::UseLocal);
    match logs_dir {
        Some(dir) => builder.targets([
            Target::new(TargetKind::Folder {
                path: dir.to_path_buf(),
                file_name: Some(SHELL_LOG_FILE_NAME.into()),
            }),
            Target::new(TargetKind::Stdout),
        ]),
        None => builder.targets([Target::new(TargetKind::Stdout)]),
    }
}

/// 解析壳归档名时间戳:`shell_YYYY-MM-DD_HH-MM-SS.log` → (年,月,日,时,分,秒)
/// (plugin LOG_DATE_FORMAT 逐位严格解析,分隔符位不符/越界值 None;活动
/// `shell.log` 与 `.bak` 碰撞形态天然不匹配)。
fn parse_shell_archive_timestamp(file_name: &str) -> Option<(i64, u32, u32, u32, u32, u32)> {
    let stem = file_name.strip_prefix("shell_")?.strip_suffix(".log")?;
    let bytes = stem.as_bytes();
    if bytes.len() != 19 {
        return None;
    }
    let sep_at = |i: usize, expected: u8| bytes.get(i).is_some_and(|b| *b == expected);
    if !(sep_at(4, b'-')
        && sep_at(7, b'-')
        && sep_at(10, b'_')
        && sep_at(13, b'-')
        && sep_at(16, b'-'))
    {
        return None;
    }
    let num = |range: std::ops::Range<usize>| -> Option<u32> {
        let s = stem.get(range)?;
        s.chars().all(|c| c.is_ascii_digit()).then_some(())?;
        s.parse().ok()
    };
    let (year, month, day) = (num(0..4)?, num(5..7)?, num(8..10)?);
    let (hour, minute, second) = (num(11..13)?, num(14..16)?, num(17..19)?);
    if !(1..=12).contains(&month)
        || !(1..=31).contains(&day)
        || hour > 23
        || minute > 59
        || second > 59
    {
        return None;
    }
    Some((year as i64, month, day, hour, minute, second))
}

/// 墙钟时间 → 线性秒(「当作 UTC」的天数换算;Hinnant days_from_civil,
/// 1970-01-01=0)。归档时间戳(UseLocal 本地墙钟)与截止值同法比较,时区
/// 偏移在两侧相消(±UTC 偏移 ≤14h,对 7 天保留窗无感,如实取舍)。
fn naive_wall_clock_epoch(
    year: i64,
    month: u32,
    day: u32,
    hour: u32,
    minute: u32,
    second: u32,
) -> i64 {
    let y = if month <= 2 { year - 1 } else { year };
    let era = if y >= 0 { y } else { y - 399 } / 400;
    let yoe = y - era * 400;
    let mp = (i64::from(month) + 9) % 12;
    let doy = (153 * mp + 2) / 5 + i64::from(day) - 1;
    let doe = yoe * 365 + yoe / 4 - yoe / 100 + doy;
    (era * 146097 + doe - 719468) * 86400
        + i64::from(hour) * 3600
        + i64::from(minute) * 60
        + i64::from(second)
}

/// 壳归档保留清理(design §4/批2 2.6):启动时把 `logs/` 下归档名时间戳
/// **早于截止值**的 `shell_<时间戳>.log` 删除。红线:前缀钉死逐名解析,
/// 绝不整目录清理——活动 `shell.log`、名形不符件(`.bak` 碰撞形态)、
/// Python 侧 `myssia-*.jsonl`、旧 `vision-server.log`、`cron/output` 等
/// 邻居零触碰。回执 = 删除数(日志留痕用)。
fn clean_stale_shell_archives_with_cutoff(
    logs_dir: &std::path::Path,
    cutoff_epoch: i64,
) -> usize {
    let Ok(entries) = std::fs::read_dir(logs_dir) else {
        return 0;
    };
    let mut removed = 0;
    for entry in entries.flatten() {
        let file_name = entry.file_name();
        let Some(name) = file_name.to_str() else {
            continue;
        };
        let Some((y, m, d, h, mi, s)) = parse_shell_archive_timestamp(name) else {
            continue;
        };
        if naive_wall_clock_epoch(y, m, d, h, mi, s) < cutoff_epoch {
            if std::fs::remove_file(entry.path()).is_ok() {
                removed += 1;
            }
        }
    }
    removed
}

/// 启动期保留清理入口:`shell_<时间戳>.log` 归档 > 7 天删除(截止值 =
/// 当前 unix epoch − 7 天,同法「当 UTC」比较)。
fn clean_stale_shell_archives(logs_dir: &std::path::Path) -> usize {
    let now = std::time::SystemTime::now()
        .duration_since(std::time::UNIX_EPOCH)
        .map(|d| d.as_secs() as i64)
        .unwrap_or(0);
    let cutoff = now - SHELL_LOG_RETENTION_DAYS as i64 * 86400;
    clean_stale_shell_archives_with_cutoff(logs_dir, cutoff)
}

/// 沙箱窗标题(10-05-ui-chore-batch,池档 v12-backlog 第 9 项):显式
/// `MYIA_HOME`(补验/自动化拉起的独立数据根)时主窗标题加「(沙箱)」后缀,
/// 补验窗口与生产实例零视觉区分引过一场误诊断(主人亲历,见
/// 10-05-bundled-plugins-install prd「补验销号」段)。判定口径与
/// data_root/acquire_instance_lock 的 var_os 分支同源:壳自身进程 env 里
/// 出现 MYIA_HOME 即独立实例域(未设时壳根本不设此 env,只 spawn 时注入给
/// sidecar 子进程,不影响本判定);纯函数便于单测,setup 处消费。
fn sandbox_title(base_title: &str, myia_home: Option<&std::ffi::OsStr>) -> String {
    if myia_home.is_some() {
        format!("{base_title}(沙箱)")
    } else {
        base_title.to_string()
    }
}

/// tao 在 applicationDidFinishLaunching 无条件 activateIgnoringOtherApps(true)
/// (tao-0.37.1 app_state.rs:293,默认值出自 app_delegate.rs:106),连 `open -g`
/// 的后台启动语义都会被覆盖。窗口隐藏躲不开应用级自激活(键盘焦点仍被夺),
/// 只能在启动序列落定后把激活让回前一应用。
#[cfg(target_os = "macos")]
fn yield_focus_after_silent_start(app: AppHandle) {
    std::thread::spawn(move || {
        std::thread::sleep(Duration::from_millis(500));
        let _ = app.run_on_main_thread(|| {
            use objc2::MainThreadMarker;
            use objc2_app_kit::NSApplication;
            if let Some(marker) = MainThreadMarker::new() {
                NSApplication::sharedApplication(marker).deactivate();
            }
        });
    });
}

/// 单实例锁(主人规则 2026-10-03:同项目只许一个实例)。macOS LaunchServices
/// 只防 bundle 重复打开,防不住 `open -n` / 直跑二进制 / dev 与 release 混跑;
/// 官方 single-instance 插件在 macOS 是空操作,故自持 flock。锁落数据根
/// (与 sidecar 的 MYIA_HOME 同规则):dev 构建与装机包共用默认根即互斥,
/// 验证流用 MYIA_HOME 沙箱时属独立实例域(沙箱=独立环境,合理)。
/// Windows 侧不走 flock:单实例 + 二实例唤出统一由官方 single-instance
/// 插件承担(见 main() builder 首位注册,命名 mutex 按 identifier 全局互斥)。
#[cfg(target_os = "macos")]
fn acquire_instance_lock() -> Option<std::fs::File> {
    use std::os::fd::AsRawFd;
    let root = if let Some(home) = std::env::var_os("MYIA_HOME") {
        PathBuf::from(home)
    } else {
        PathBuf::from(std::env::var_os("HOME")?).join("Library/Application Support/MYIA")
    };
    std::fs::create_dir_all(&root).ok()?;
    let file = std::fs::File::create(root.join(".instance.lock")).ok()?;
    let held = unsafe { libc::flock(file.as_raw_fd(), libc::LOCK_EX | libc::LOCK_NB) } == 0;
    held.then_some(file) // 进程退出由内核放锁,File 永不显式关闭(mem::forget 持有)
}

/// 唤出并聚焦主窗(show + set_focus)。三路共用,保证亮窗行为同源
/// (10-05-win-second-instance-show 收敛):macOS Dock Reopen、Windows
/// 二实例回调、dev / MYIA_SHOW_ON_START 启动即显。
fn show_main_window<R: tauri::Runtime>(app: &impl Manager<R>) {
    if let Some(window) = app.get_webview_window("main") {
        let _ = window.show();
        let _ = window.set_focus();
    }
}

/// 前端就绪旗(白窗修复 10-06-smoke-window-politeness R1):前端 App mount
/// 完成后 emit `myia:ui-ready`,壳层收到置位。验证性亮窗(SMOKE_ROUTE/
/// SHOW_ON_START)以它门控——「等渲染完才亮」,杜绝先白屏后渲染糊脸。
static UI_READY: std::sync::atomic::AtomicBool = std::sync::atomic::AtomicBool::new(false);
/// 挂起中的亮窗请求(等 UI_READY 或超时兜底):0=无,1=亮但不抢焦点,2=亮且聚焦。
static PENDING_SHOW: std::sync::atomic::AtomicU8 = std::sync::atomic::AtomicU8::new(0);
/// 兜底等待:前端握手永远不来(极端:webview 崩/非 tauri 容器)也不许把窗
/// 永久藏死,5s 后照亮(此时可能仍是白窗,但验证流有截图断言兜底)。
const SHOW_FALLBACK: Duration = Duration::from_secs(5);

/// 按焦点档亮主窗(R2:验证路径默认不抢主人前台)。
fn show_window_now<R: tauri::Runtime>(app: &impl Manager<R>, focus: bool) {
    if let Some(window) = app.get_webview_window("main") {
        let _ = window.show();
        if focus {
            let _ = window.set_focus();
        }
    }
}

/// 结算挂起请求(原子取出):Some(focus) = 该亮窗了,None = 无挂起。
fn take_pending_show() -> Option<bool> {
    match PENDING_SHOW.swap(0, Ordering::AcqRel) {
        1 => Some(false),
        2 => Some(true),
        _ => None,
    }
}

/// 验证性亮窗(R1):前端就绪则立刻亮,否则挂起等 `myia:ui-ready` 事件
/// (事件回调里结算)+ 5s 兜底定时器双保险。
fn show_main_window_deferred<R: tauri::Runtime>(app: &impl Manager<R>, focus: bool) {
    if UI_READY.load(Ordering::Acquire) {
        show_window_now(app, focus);
        return;
    }
    PENDING_SHOW.store(if focus { 2 } else { 1 }, Ordering::Release);
    let handle = app.app_handle().clone();
    tauri::async_runtime::spawn(async move {
        tokio::time::sleep(SHOW_FALLBACK).await;
        if let Some(focus) = take_pending_show() {
            log::warn!("desktop: ui-ready 未至,亮窗兜底触发(可能未渲染完)");
            show_window_now(&handle, focus);
        }
    });
}

/// MYIA_SMOKE_GEOMETRY 解析(R3):`WxH+X+Y` 或 `WxH`(此时不动位置)。
/// 校验+夹取:W/H ∈ [200,1920]/[200,2160],X/Y ∈ [0,7680];非法输入 None 零行为。
fn parse_smoke_geometry(raw: &str) -> Option<(u32, u32, i32, i32)> {
    fn clamp_u32(v: u32, lo: u32, hi: u32) -> u32 {
        v.clamp(lo, hi)
    }
    let raw = raw.trim();
    let (size_part, pos_part) = match raw.split_once(['+']) {
        Some((s, p)) => (s, Some(p)),
        None => (raw, None),
    };
    let lowered = size_part.to_ascii_lowercase();
    let (w_str, h_str) = lowered.split_once('x')?;
    let w: u32 = w_str.trim().parse().ok()?;
    let h: u32 = h_str.trim().parse().ok()?;
    if w == 0 || h == 0 {
        return None;
    }
    let (x, y) = match pos_part {
        Some(p) => {
            let (x_str, y_str) = p.split_once('+')?;
            let x: i32 = x_str.trim().parse().ok()?;
            let y: i32 = y_str.trim().parse().ok()?;
            (x.clamp(0, 7680), y.clamp(0, 4320))
        }
        None => (-1, -1), // 哨兵:不设位置(沿用当前/居中)
    };
    Some((clamp_u32(w, 200, 1920), clamp_u32(h, 200, 2160), x, y))
}

fn main() {
    let started = Instant::now();
    // 单实例门:已有实例持锁 → 转激活它并退出。激活须等本进程退干净再执行:
    // 两进程短暂共存同 bundle id 时 LaunchServices 可能选中将死的这个(实测踩过),
    // 故甩孤儿 shell 延时半秒后 open -b —— 既有实例经 Reopen 亮窗,不夺屏不弹窗。
    #[cfg(target_os = "macos")]
    match acquire_instance_lock() {
        Some(lock) => std::mem::forget(lock),
        None => {
            // 保留 eprintln(pre-logger 通道):此分支发生在 tauri builder 之前,
            // log plugin 尚未挂全局 logger,log::warn! 会被静默丢弃;本进程
            // 随即退出,终端 stderr 是唯一可见面。
            eprintln!("desktop: 已有 MYIA 实例在跑(单实例锁),转激活既有实例后退出");
            let _ = std::process::Command::new("/bin/sh")
                .args(["-c", "sleep 0.5; exec /usr/bin/open -b com.myssia.app"])
                .spawn();
            return;
        }
    }
    let builder = tauri::Builder::default();
    // 壳日志(批2 design §6):plugin 注册前先解析 `<数据根>/logs/`(既有
    // 数据根规则;不可建 → 降级仅 Stdout 不阻启动)+ 归档自清(>7 天,红线
    // 前缀钉死)。plugin 的全局 logger 在其 setup 挂起——setup 早于本壳一切
    // 业务留痕(pump/respawn/安装链),此后 log:: 宏全走 shell.log。
    let logs_dir = resolve_shell_logs_dir();
    if let Some(dir) = &logs_dir {
        let removed = clean_stale_shell_archives(dir);
        if removed > 0 {
            // 此刻 logger 未挂(log:: 会丢),用 eprintln 打一条启动期回执
            // (与单实例锁同款「pre-logger 通道」;dev 终端可见)。
            eprintln!(
                "desktop: 壳日志归档自清: 删除 {removed} 个 >{SHELL_LOG_RETENTION_DAYS} 天归档({})",
                dir.display()
            );
        }
    } else {
        eprintln!("desktop: 壳日志目录不可建(数据根不可解析/不可写),降级仅 Stdout");
    }
    // Windows 二实例唤出(10-05-win-second-instance-show):发布包主窗
    // visible:false 出厂,macOS 有 Dock Reopen 亮窗,Windows 无 Dock 无托盘
    // ——普通用户双击图标永无窗口(10-05-win-local-build evidence §8 坑 4)。
    // 官方插件:第二实例启动 → 命名 mutex 判重 → 窗口消息回调第一实例
    // (此处 show+focus 主窗)→ 第二实例自退,一并补上 Windows 单实例语义。
    // 插件按注册序初始化,官方要求置于插件列表首位;macOS 是空操作且已有
    // flock 单实例门,故仅 Windows 注册(mac 零行为变化)。
    #[cfg(target_os = "windows")]
    let builder = builder.plugin(tauri_plugin_single_instance::init(
        |app, argv, _cwd| {
            log::info!(
                "desktop: 第二实例启动(argv={argv:?}),唤出既有实例主窗后其自退"
            );
            show_main_window(app);
        },
    ));
    let app = builder
        // log:壳/UI 统一日志(批2;注册序在 single-instance 之后——Windows
        // 侧官方要求 single-instance 居首位不动,log 次位;macOS/Linux 居首)。
        .plugin(shell_log_plugin(logs_dir.as_deref()).build())
        .plugin(tauri_plugin_shell::init())
        // updater:前端经 @tauri-apps/plugin-updater 检查/下载/安装;签名公钥见 tauri.conf.json
        .plugin(tauri_plugin_updater::Builder::new().build())
        // process:更新安装完成后的进程重启(relaunch)
        .plugin(tauri_plugin_process::init())
        // dialog:看图屏系统文件选择器(前端 @tauri-apps/plugin-dialog;权限见 capabilities/default.json)
        .plugin(tauri_plugin_dialog::init())
        .invoke_handler(tauri::generate_handler![
            sidecar_request,
            sidecar_restart,
            pyenv::pyenv_get_status,
            pyenv::pyenv_start_setup,
            pyenv::pyenv_sync_deps,
            pyenv_install::pyenv_verify,
            pyenv_components::pyenv_install_component,
            // 轨B 壳服务组件生命周期(10-06-native-plugin-components 阶段2,
            // design §2/G-Q5:显式启停 + 状态记忆,不隐式拉起)
            pyenv_components::service_start,
            pyenv_components::service_stop,
            pyenv_components::service_status,
            pyenv_migration::pyenv_migration_banner
        ])
        .setup(move |app| {
            // 冷启动打点(沿用 spike 惯例):进程启动 → sidecar spawn 完成。
            // 先 manage 后 spawn:pump 任务一启动就会触达 Sidecar 状态
            // (spawn_sidecar 内起 pump),manage 必须先行。PyenvManager 同理
            // (spawn_sidecar/探测都要读它的 installing 槽)。
            app.manage(Sidecar {
                child: Mutex::new(None),
                pending: Mutex::new(HashMap::new()),
                next_id: AtomicU64::new(1),
                respawn_attempts: Mutex::new(0),
            });
            app.manage(pyenv::PyenvManager::default());
            // 组件机制(10-05-table-restore):单飞护栏内存槽(installing =
            // 在装组件 id;pyenv_install_component 占坑/清槽)。
            app.manage(pyenv_components::ComponentManager::default());
            // 轨B 服务组件管理器(10-06-native-plugin-components 阶段2):本会话
            // 拉起的服务子进程句柄表(退出码回收依赖句柄;跨会话孤儿靠状态戳
            // pid + ps argv 复核对账,G-Q5 状态记忆)。
            app.manage(pyenv_components::ServiceManager::default());
            // 自管 Python 环境探测(第 2 步):未就绪(not_configured/installing/
            // error)不 spawn、启动不崩——发空态事件走 UI 引导(D2),sidecar
            // 请求由协议层报结构化 pyenv_not_ready(prd Req 3);就绪/依赖漂移
            // 照常 spawn(漂移只是设置页「同步依赖」提示,D4 不强制拦)。
            let status = pyenv::current_status(app.handle())?;
            let _ = app.emit(pyenv::PYENV_STATUS_EVENT, &status);
            if pyenv::spawnable(status.state) {
                let child = spawn_sidecar(app.handle())?; // 首启 io 失败仍硬失败(与现状一致;respawn 只管运行中退出)
                *app.state::<Sidecar>().child.lock().unwrap() = Some(child);
            } else {
                let _ = app.emit(pyenv::PYENV_NOT_READY_EVENT, &status);
                log::warn!(
                    "desktop: Python 运行环境未就绪(state={:?}),不 spawn sidecar;UI 走引导空态",
                    status.state
                );
            }
            // MYIA_PYENV_AUTOSETUP 自动化端到端冒烟钩子(10-05 第 5 步;同
            // MYIA_SMOKE_ROUTE 先例,发布包无人设置,D2「用户显式点开始配置」
            // 的产品行为不变):设置即视为已点「开始配置」,拉起与
            // pyenv_start_setup 同一条安装链(镜像读沙箱 pyenv-settings.json,
            // 测试预写指向本地静态服务器)。挂在 if/else 之后:取值 "1" 仅
            // not_configured 态触发(AC1 全新装机主链);"force" 无视当前态重跑
            // ——ready 态幂等二跑验证用(AC4,已装步全 skipped;ready 态壳会先
            // spawn 常驻 sidecar,链成功后 spawn_sidecar_if_idle 幂等不杀活进程,
            // D4 未要求重启);installing 态会被 start_install_thread 的占坑护栏
            // 拒绝,不构成双跑。
            if let Ok(mode) = std::env::var("MYIA_PYENV_AUTOSETUP") {
                let allowed =
                    matches!(status.state, pyenv::PyenvState::NotConfigured) || mode == "force";
                if allowed {
                    match crate::pyenv_install::start_install_thread(app.handle().clone(), false) {
                        Ok(()) => {
                            log::info!("desktop: MYIA_PYENV_AUTOSETUP={mode} 冒烟钩子已拉起安装链")
                        }
                        Err(err) => {
                            log::warn!("desktop: MYIA_PYENV_AUTOSETUP 拉起安装链失败: {err}")
                        }
                    }
                }
            }
            // 验证窗几何(R3):MYIA_SMOKE_GEOMETRY="WxH+X+Y" 把验证窗变小
            // 挪角,不再全屏糊主人脸;未设零行为。须在一切 show 之前应用。
            if let Some((w, h, x, y)) = std::env::var("MYIA_SMOKE_GEOMETRY")
                .ok()
                .as_deref()
                .and_then(parse_smoke_geometry)
            {
                if let Some(win) = app.get_webview_window("main") {
                    let _ = win.set_size(tauri::LogicalSize::new(w, h));
                    if x >= 0 && y >= 0 {
                        let _ = win.set_position(tauri::LogicalPosition::new(x, y));
                    }
                }
            }
            // 白窗修复握手(R1):前端 App mount 完 emit `myia:ui-ready` →
            // 置就绪旗并结算挂起中的亮窗请求(此时渲染已毕,亮即成品)。
            if let Some(win) = app.get_webview_window("main") {
                let handle = app.app_handle().clone();
                let _ = win.listen("myia:ui-ready", move |_| {
                    UI_READY.store(true, Ordering::Release);
                    if let Some(focus) = take_pending_show() {
                        show_window_now(&handle, focus);
                    }
                });
            }
            // 沙箱窗自标识(池档 v12-backlog 第 9 项):显式 MYIA_HOME = 独立
            // 实例域(补验/自动化拉起),主窗标题加「(沙箱)」后缀防误当生产
            // 实例操作;未设零行为变化。置 MYIA_SMOKE_ROUTE 冒烟路由/亮窗之前,
            // 任何后续截图/自动化产物即带标识。
            if let Some(window) = app.get_webview_window("main") {
                if let Ok(base) = window.title() {
                    let _ = window.set_title(&sandbox_title(&base, std::env::var_os("MYIA_HOME").as_deref()));
                }
            }
            // MYIA_SMOKE_ROUTE 静默冒烟钩子(v1.1.1 装机五屏截图用):launchctl
            // setenv 传入路由名(如 "feed"),启动即设 window.location.hash("#/feed");
            // 未设则零行为变化。立即 + 1500ms 两次 eval 兜底 webview 未就绪的窗口期,
            // 同值幂等;不 show 不 focus,静默启动语义不受影响。
            if let Ok(route) = std::env::var("MYIA_SMOKE_ROUTE") {
                let hash = if route.starts_with('#') {
                    route
                } else {
                    format!("#/{}", route.trim_start_matches('/'))
                };
                if let Some(win) = app.get_webview_window("main") {
                    let script = format!(
                        "window.location.hash = {}",
                        serde_json::to_string(&hash).unwrap_or_else(|_| "\"#/\"".into())
                    );
                    let _ = win.eval(&script);
                    let (win, script) = (win.clone(), script.clone());
                    tauri::async_runtime::spawn(async move {
                        tokio::time::sleep(Duration::from_millis(1500)).await;
                        let _ = win.eval(&script);
                    });
                }
                // 冒烟亮窗改走就绪门控(R1):渲染完才亮、不抢焦点(R2);
                // run loop 时序由事件/兜底定时器天然保证(均在事件循环起来后)。
                show_main_window_deferred(&*app, false);
            }
            // 静默启动(10-03-quiet-launch):主窗口 visible:false 出厂,Dock 点击
            // (RunEvent::Reopen)或对运行中实例再 open -a 才亮出。dev 构建与
            // MYIA_SHOW_ON_START=1 例外照旧启动即显示(open 不透传 shell env,
            // 发布包自动化验证须直跑二进制或 open 两次)。
            let show_on_start =
                cfg!(debug_assertions) || std::env::var_os("MYIA_SHOW_ON_START").is_some();
            if show_on_start {
                // R1+R2:等渲染完才亮(白窗修复);焦点仅 dev 构建或显式
                // MYIA_SMOKE_FOCUS=1(要点击交互的验证才开,平时不抢主人前台)。
                let focus = cfg!(debug_assertions) || std::env::var_os("MYIA_SMOKE_FOCUS").is_some();
                show_main_window_deferred(&*app, focus);
            } else {
                #[cfg(target_os = "macos")]
                yield_focus_after_silent_start(app.handle().clone());
            }
            log::info!(
                "desktop: setup done in {} ms(sidecar {})",
                started.elapsed().as_millis(),
                if pyenv::spawnable(status.state) { "spawned" } else { "skipped(环境未就绪)" }
            );
            Ok(())
        })
        .build(tauri::generate_context!())
        .expect("tauri application failed to start");
    app.run(|app, event| {
        // Dock 图标点击 / 对运行中实例再 open -a:静默启动藏起的主窗口在此时亮出
        // (Windows 的对应通道是 single-instance 二实例回调,见 builder 首位注册)
        #[cfg(target_os = "macos")]
        if let tauri::RunEvent::Reopen {
            has_visible_windows: false,
            ..
        } = event
        {
            show_main_window(app);
        }
    });
}

#[cfg(test)]
mod tests {
    use super::*;

    /// 冒烟几何解析(R3):合法两形态/夹取/非法零行为。
    #[test]
    fn smoke_geometry_full_form() {
        assert_eq!(parse_smoke_geometry("900x600+40+400"), Some((900, 600, 40, 400)));
        assert_eq!(parse_smoke_geometry(" 720x480 \n"), Some((720, 480, -1, -1)));
    }

    #[test]
    fn smoke_geometry_clamps_and_rejects() {
        // 夹取:过小抬到下限,过大压到上限
        assert_eq!(parse_smoke_geometry("50x40+0+0"), Some((200, 200, 0, 0)));
        assert_eq!(parse_smoke_geometry("4000x5000+0+0"), Some((1920, 2160, 0, 0)));
        assert_eq!(parse_smoke_geometry("800x600+99999+0"), Some((800, 600, 7680, 0)));
        // 非法:零维/坏数字/缺高/位置只有一段 → None(零行为)
        assert_eq!(parse_smoke_geometry("0x600"), None);
        assert_eq!(parse_smoke_geometry("900"), None);
        assert_eq!(parse_smoke_geometry("ax600"), None);
        assert_eq!(parse_smoke_geometry("900x600+40"), None);
        assert_eq!(parse_smoke_geometry(""), None);
    }

    /// 挂起结算纯函数锁(R1):0 无/1 不抢焦/2 抢焦,取出即清零。
    #[test]
    fn pending_show_settles_once() {
        PENDING_SHOW.store(0, Ordering::Release);
        assert_eq!(take_pending_show(), None);
        PENDING_SHOW.store(1, Ordering::Release);
        assert_eq!(take_pending_show(), Some(false));
        assert_eq!(take_pending_show(), None); // 已清零
        PENDING_SHOW.store(2, Ordering::Release);
        assert_eq!(take_pending_show(), Some(true));
    }

    /// 退避纯函数锁:序列恰为 1/2/4/8/16s(RESPAWN_MAX_ATTEMPTS 内),溢出安全。
    #[test]
    fn backoff_delay_doubles_per_attempt() {
        assert_eq!(backoff_delay(1), Duration::from_secs(1));
        assert_eq!(backoff_delay(2), Duration::from_secs(2));
        assert_eq!(backoff_delay(3), Duration::from_secs(4));
        assert_eq!(backoff_delay(4), Duration::from_secs(8));
        assert_eq!(backoff_delay(5), Duration::from_secs(16));
    }

    #[test]
    fn backoff_delay_saturates_without_panic() {
        // 极端 attempt(防御):saturating_pow 封顶,不 panic、单调不降
        assert!(backoff_delay(u32::MAX) >= backoff_delay(RESPAWN_MAX_ATTEMPTS));
        assert_eq!(backoff_delay(0), Duration::from_secs(1)); // 防御性下界
    }

    /// 沙箱窗自标识(10-05-ui-chore-batch):显式 MYIA_HOME 加「(沙箱)」后缀;
    /// 判定只看有无(var_os 分支),与 data_root/单实例锁同口径。
    #[test]
    fn sandbox_title_appends_suffix_when_myia_home_set() {
        use std::ffi::OsStr;
        assert_eq!(
            sandbox_title("世事", Some(OsStr::new("/tmp/myia-sandbox"))),
            "世事(沙箱)"
        );
        // 指向默认根的显式设置也算独立实例域(同单实例锁口径),后缀照加
        assert_eq!(
            sandbox_title("世事", Some(OsStr::new("/默认/数据根"))),
            "世事(沙箱)"
        );
    }

    #[test]
    fn sandbox_title_passthrough_when_myia_home_unset() {
        assert_eq!(sandbox_title("世事", None), "世事");
    }

    // -----------------------------------------------------------------------
    // 壳日志(10-07-unified-logging 批2;AC4/AC5 壳半)
    // -----------------------------------------------------------------------

    /// MYIA_HOME 环境变量互斥:env 是进程全局,env 触面测试之间串行,
    /// 防并行测试互踩(cargo test 默认多线程)。
    static ENV_LOCK: std::sync::Mutex<()> = std::sync::Mutex::new(());

    /// 显式 MYIA_HOME → `<root>/logs` 拼装 + 目录预建;根不可建(父路径
    /// 是普通文件)→ None 降级(仅 Stdout,不阻启动)。
    #[test]
    fn shell_logs_dir_resolves_and_degrades() {
        let _guard = ENV_LOCK.lock().unwrap();
        let previous = std::env::var_os("MYIA_HOME");
        // 可建根:logs 目录被预建
        let root = tempfile::tempdir().expect("临时数据根创建失败");
        std::env::set_var("MYIA_HOME", root.path());
        let logs = resolve_shell_logs_dir().expect("可建根应解析出 logs 目录");
        assert_eq!(logs, root.path().join("logs"));
        assert!(logs.is_dir(), "logs 目录应被预建(plugin Folder 依赖)");
        // 不可建根:MYIA_HOME 指到普通文件之下 → create_dir_all 失败 → None
        let blocker = tempfile::tempdir().expect("临时目录创建失败");
        let file = blocker.path().join("plain-file");
        std::fs::write(&file, b"x").expect("占位普通文件写入失败");
        std::env::set_var("MYIA_HOME", file.join("under").join("logs-parent"));
        assert!(
            resolve_shell_logs_dir().is_none(),
            "根不可建应降级 None(仅 Stdout)"
        );
        match previous {
            Some(value) => std::env::set_var("MYIA_HOME", value),
            None => std::env::remove_var("MYIA_HOME"),
        }
    }

    /// 归档名时间戳解析(plugin LOG_DATE_FORMAT 真名复核):合法形态全字段;
    /// 活动 shell.log / .bak 碰撞形态 / 名形不符 / 越界值一律 None。
    #[test]
    fn shell_archive_timestamp_parses_plugin_name_shape() {
        assert_eq!(
            parse_shell_archive_timestamp("shell_2026-10-07_09-30-45.log"),
            Some((2026, 10, 7, 9, 30, 45))
        );
        // 名形不符(红线:前缀钉死,别的一切不匹配)
        assert_eq!(parse_shell_archive_timestamp("shell.log"), None);
        assert_eq!(parse_shell_archive_timestamp("shell_2026-10-07_09-30-45.log.bak"), None);
        assert_eq!(parse_shell_archive_timestamp("shell_20261007_093045.log"), None);
        assert_eq!(parse_shell_archive_timestamp("myssia-20261007.jsonl"), None);
        assert_eq!(parse_shell_archive_timestamp("shell_2026-1x-07_09-30-45.log"), None);
        // 越界字段(月 13 / 时 24):形态合法但值不合法 → None(不误删)
        assert_eq!(parse_shell_archive_timestamp("shell_2026-13-01_00-00-00.log"), None);
        assert_eq!(parse_shell_archive_timestamp("shell_2026-10-07_24-00-00.log"), None);
    }

    /// 墙钟线性秒(Hinnant days_from_civil):对照 datetime 同口径参考值
    /// (2026-10-07 亲算:1791365445;闰日 2000-02-29:951825600)。
    #[test]
    fn naive_wall_clock_epoch_matches_reference() {
        assert_eq!(naive_wall_clock_epoch(1970, 1, 1, 0, 0, 0), 0);
        assert_eq!(naive_wall_clock_epoch(2000, 2, 29, 12, 0, 0), 951825600);
        assert_eq!(naive_wall_clock_epoch(2026, 10, 7, 9, 30, 45), 1791365445);
        assert_eq!(naive_wall_clock_epoch(2024, 1, 1, 0, 0, 0), 1704067200);
    }

    /// 归档保留清理(AC5 壳半):>截止值的归档删;新归档/活动 shell.log/
    /// 邻居(Python myssia-*.jsonl、旧 vision-server.log、.bak 碰撞形态、
    /// cron 产物)零触碰——负断言钉死「绝不整目录清理」红线。
    #[test]
    fn stale_shell_archives_purged_and_neighbors_untouched() {
        let logs = tempfile::tempdir().expect("临时 logs 目录创建失败");
        let write = |name: &str| std::fs::write(logs.path().join(name), b"log line\n")
            .unwrap_or_else(|e| panic!("{name} 写入失败: {e}"));
        // 截止值 = 2026-01-01 00:00:00(naive 同法)
        let cutoff = naive_wall_clock_epoch(2026, 1, 1, 0, 0, 0);
        write("shell_2025-12-25_00-00-00.log"); // 超期 → 删
        write("shell_2024-06-01_08-00-00.log"); // 远超期 → 删
        write("shell_2026-06-01_00-00-00.log"); // 期内 → 留
        write("shell.log"); // 活动文件永不动 → 留
        write("shell_2025-12-25_00-00-00.log.bak"); // 碰撞形态不匹配 → 留
        write("myssia-20251225.jsonl"); // Python 侧单前缀 → 留
        write("vision-server.log"); // 升级场景旧文件 → 留
        write("cron-job-output.log"); // cron 每跑次产物 → 留

        let removed = clean_stale_shell_archives_with_cutoff(logs.path(), cutoff);

        assert_eq!(removed, 2, "恰删两个超期归档");
        assert!(!logs.path().join("shell_2025-12-25_00-00-00.log").exists());
        assert!(!logs.path().join("shell_2024-06-01_08-00-00.log").exists());
        for kept in [
            "shell_2026-06-01_00-00-00.log",
            "shell.log",
            "shell_2025-12-25_00-00-00.log.bak",
            "myssia-20251225.jsonl",
            "vision-server.log",
            "cron-job-output.log",
        ] {
            assert!(
                logs.path().join(kept).exists(),
                "邻居/期内件 {kept} 不得被清理(红线)"
            );
        }
    }

    /// 目录缺位(数据根被整体清走等极端态)→ 零动作零 panic(与 Python 侧
    /// 「无文件静默通过」同语义)。
    #[test]
    fn stale_shell_archive_cleanup_missing_dir_is_noop() {
        let base = tempfile::tempdir().expect("临时目录创建失败");
        let missing = base.path().join("no-such-logs");
        assert_eq!(clean_stale_shell_archives_with_cutoff(&missing, 0), 0);
    }
}
