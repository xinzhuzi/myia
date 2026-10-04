//! 桌面自管 Python 环境 —— 壳侧探测与 IPC 契约(10-05-desktop-managed-py-env 第 2 步)。
//!
//! 决议与设计出处:prd.md D1-D6(Req 3)/ design.md §1①②③④ §3 §4。
//! - 探测三态:ready(就绪)/ not_configured(未配置)/ deps_stale(依赖漂移);
//!   叠加安装链在跑的 installing 与安装失败的 error,共五态(IPC 契约波次钉死)。
//! - spawn 源已切自管环境:`<数据根>/python/bin/python3 -m myssia_desktop_entry
//!   serve`(PYTHONPATH=随包 Resources/myssia-src;Windows 为 python.exe)——
//!   main.rs `spawn_sidecar` 落地,design §4(argv 见 `ENTRY_ARGS`)。
//! - 未就绪(not_configured/installing/error)壳不 spawn、启动不崩:发
//!   `pyenv_not_ready` 空态事件(D2),协议层 `sidecar_request` 报结构化
//!   `pyenv_not_ready`(prd Req 3);deps_stale 照常 spawn(D4 不强制拦,漂移
//!   只是设置页「同步依赖」的提示)。
//!
//! == 落盘契约(与第 3 步安装链执行器对齐)==
//! - `<数据根>/python-env.json`:安装链进度戳。本模块只读,字段宽容:
//!   `{"state": "ready"|"error"|null, "deps_fingerprint": "<hex>",
//!     "steps": [{"phase","status","error"}, …(可带 ts 等附加字段,宽容忽略)]}`。
//!   state 落终态才由本模块判定 ready/error;null/缺省 = 安装中断(可重试)。
//!   deps_fingerprint = 随包 requirements-lock.txt 的 sha256 hex(安装时实算);
//!   与当前随包清单重算值不等 → deps_stale(D4 壳更新后依赖漂移)。
//! - `<数据根>/pyenv-settings.json`:镜像覆盖(壳自有,安装链读同文件接力):
//!   `{"mirror_runtime": "https://…", "mirror_pypi": "https://…"}`(null/缺省
//!   = 用默认源;design §5 双镜像覆盖)。
//!
//! == 事件 ==
//! - `pyenv-status-changed`:载荷同 `pyenv_get_status` 结果(状态(重)算即发;
//!   前端初始化仍以拉取 `pyenv_get_status` 为准,事件只作变更通知)。
//! - `pyenv_not_ready`:载荷同上;仅未就绪态发出(UI 各屏引导卡,D2)。

use std::path::{Path, PathBuf};
use std::sync::Mutex;

use serde::{Deserialize, Serialize};
use serde_json::{json, Value};
use tauri::{AppHandle, Emitter, Manager};

/// 状态变更事件名(IPC 契约波次钉死;载荷同 status 形态)。
pub const PYENV_STATUS_EVENT: &str = "pyenv-status-changed";
/// 空态事件名(design §1②:未就绪 → 不 spawn,UI 引导卡)。
pub const PYENV_NOT_READY_EVENT: &str = "pyenv_not_ready";
/// 随包入口模块名(design §4;与第 1 步随包 Resources/myssia-src 配对)。
pub const ENTRY_MODULE: &str = "myssia_desktop_entry";
/// spawn argv 契约(与第 1 步落地的 desktop/myssia_desktop_entry/__main__.py
/// 钉死:argv[0]=="serve" 才进 RPC 服务,否则直通 CLI——缺参会 print_help
/// 退出 0,sidecar 起即死。design §4 字面省了 serve 尾参,以入口模块 argv
/// 契约与第 1 步测试(tests/desktop/test_pyenv_resources.py serve 往返)为准)。
pub const ENTRY_ARGS: [&str; 3] = ["-m", ENTRY_MODULE, "serve"];
/// 随包源码目录名(tauri.conf resources 映射后位于 resource_dir 下)。
pub const RESOURCE_SRC_DIR: &str = "myssia-src";
/// 随包依赖锁版清单文件名(第 1 步随包;漂移比对基准)。
pub const RESOURCE_LOCK_FILE: &str = "requirements-lock.txt";
/// 环境进度戳文件名(数据根下;安装链写、壳读)。
const ENV_STAMP_FILE: &str = "python-env.json";
/// 镜像覆盖落盘文件名(数据根下;壳写、安装链读)。
const SETTINGS_FILE: &str = "pyenv-settings.json";

// ---------------------------------------------------------------------------
// 状态模型(IPC 契约形态,serde 序列化即 JSON 字符串)
// ---------------------------------------------------------------------------

/// 环境五态(IPC 契约:`not_configured|installing|ready|error|deps_stale`)。
#[derive(Clone, Copy, PartialEq, Eq, Debug, Serialize)]
#[serde(rename_all = "snake_case")]
pub enum PyenvState {
    /// 未配置:全新装机首启,数据根无环境无进度戳(D2 引导空态)。
    NotConfigured,
    /// 安装中:安装链执行器在跑(壳内存态;本步恒不出现)。
    Installing,
    /// 就绪:python 在位 + 进度戳终态 ready + 依赖指纹一致。
    Ready,
    /// 异常:进度戳 error / 戳坏 / 中断 / ready 但 python 缺位(设置页可重试)。
    Error,
    /// 依赖漂移:环境健在但随包锁版清单指纹已变(D4「同步依赖」提示,不拦 spawn)。
    DepsStale,
}

/// 安装链阶段(design §3 状态机;IPC steps[].phase)。
#[derive(Clone, Copy, PartialEq, Eq, Debug, Serialize, Deserialize)]
#[serde(rename_all = "snake_case")]
pub enum PyenvPhase {
    Downloading,
    Verifying,
    Extracting,
    InstallingDeps,
    Selfcheck,
}

/// 单阶段状态(IPC steps[].status;skipped 留给第 3 步幂等跳过已装步)。
#[derive(Clone, Copy, PartialEq, Eq, Debug, Serialize, Deserialize)]
#[serde(rename_all = "snake_case")]
pub enum PyenvStepStatus {
    Pending,
    Running,
    Done,
    Skipped,
    Failed,
}

/// 安装链单阶段(IPC 契约:`{phase, status, error}`;error 恒出现,无错为 null)。
#[derive(Clone, PartialEq, Eq, Debug, Serialize, Deserialize)]
pub struct PyenvStep {
    pub phase: PyenvPhase,
    pub status: PyenvStepStatus,
    #[serde(default)]
    pub error: Option<String>,
}

impl PyenvStep {
    fn failed(phase: PyenvPhase, message: impl Into<String>) -> Self {
        Self {
            phase,
            status: PyenvStepStatus::Failed,
            error: Some(message.into()),
        }
    }
}

/// `pyenv_get_status` 结果 / 两事件共用载荷(IPC 契约波次钉死):
/// `{state, install_path, python_path, mirror_runtime, mirror_pypi, steps}`。
#[derive(Clone, PartialEq, Debug, Serialize)]
pub struct PyenvStatus {
    pub state: PyenvState,
    /// 安装路径:`<数据根>/python`(install_only 解压即得,design §3)。
    pub install_path: PathBuf,
    /// Python 使用路径:`<数据根>/python/bin/python3`(win 为 python.exe)。
    pub python_path: PathBuf,
    /// 运行时下载源覆盖(当前生效值;null = 默认 manifest 源)。
    pub mirror_runtime: Option<String>,
    /// PyPI index 覆盖(当前生效值;null = 默认 PyPI)。
    pub mirror_pypi: Option<String>,
    pub steps: Vec<PyenvStep>,
}

/// 安装链进度戳(`<数据根>/python-env.json`,第 3 步写;字段全宽容:
/// 未知附加字段忽略,缺 state 按非终态处理)。
#[derive(Deserialize, Default)]
struct EnvStamp {
    #[serde(default)]
    state: Option<String>,
    #[serde(default)]
    deps_fingerprint: Option<String>,
    #[serde(default)]
    steps: Vec<PyenvStep>,
}

/// 镜像覆盖(`<数据根>/pyenv-settings.json`;壳写,第 3 步安装链接力读)。
#[derive(Clone, PartialEq, Eq, Debug, Default, Serialize, Deserialize)]
pub struct PyenvSettings {
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub mirror_runtime: Option<String>,
    #[serde(default, skip_serializing_if = "Option::is_none")]
    pub mirror_pypi: Option<String>,
}

/// 壳侧环境管理器(setup 时 manage)。`installing` 是安装链执行器(第 3 步)
/// 的内存步进槽:安装中态不落盘(进程重启后按戳记判为中断 error 可重试),
/// 本步恒 None——探测据此区分「安装中」与「未配置」。
#[derive(Default)]
pub struct PyenvManager {
    pub installing: Mutex<Option<Vec<PyenvStep>>>,
}

/// 环境未就绪的结构化 spawn 失败:respawn 路径 downcast 识别后转空态事件、
/// 停止重试(环境不会因重试而就绪);手动拉起路径转为可读报错。
#[derive(Debug)]
pub struct PyenvNotReadyError(pub PyenvStatus);

impl std::fmt::Display for PyenvNotReadyError {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(
            f,
            "Python 运行环境未就绪(state={:?}),不 spawn sidecar",
            self.0.state
        )
    }
}

impl std::error::Error for PyenvNotReadyError {}

// ---------------------------------------------------------------------------
// 路径拼装(纯函数;win 分支独立参数化,单测在 mac 主机也可覆盖)
// ---------------------------------------------------------------------------

/// 安装路径:`<数据根>/python`(design §3 布局,与既有 models/ 并排)。
pub fn python_install_dir(data_root: &Path) -> PathBuf {
    data_root.join("python")
}

/// Python 二进制路径:macOS/Linux `<数据根>/python/bin/python3`
/// (python-build-standalone install_only 布局),Windows `<数据根>/python/python.exe`。
pub fn python_bin_path_on(data_root: &Path, windows: bool) -> PathBuf {
    if windows {
        python_install_dir(data_root).join("python.exe")
    } else {
        python_install_dir(data_root).join("bin").join("python3")
    }
}

/// 当前平台的 Python 二进制路径(design §4 spawn 源)。
pub fn python_bin_path(data_root: &Path) -> PathBuf {
    python_bin_path_on(data_root, cfg!(target_os = "windows"))
}

/// 进度戳路径:`<数据根>/python-env.json`。
pub fn env_stamp_path(data_root: &Path) -> PathBuf {
    data_root.join(ENV_STAMP_FILE)
}

/// 镜像覆盖路径:`<数据根>/pyenv-settings.json`。
pub fn pyenv_settings_path(data_root: &Path) -> PathBuf {
    data_root.join(SETTINGS_FILE)
}

/// 随包源码目录(spawn 时注入 PYTHONPATH;dev python 与应用 python 分家,Req 4)。
pub fn resource_src_dir(resource_dir: &Path) -> PathBuf {
    resource_dir.join(RESOURCE_SRC_DIR)
}

/// 随包锁版清单路径(依赖漂移比对基准)。
pub fn resource_lock_path(resource_dir: &Path) -> PathBuf {
    resource_dir.join(RESOURCE_LOCK_FILE)
}

/// 清单 sha256 指纹(hex 小写;与进度戳 deps_fingerprint 同格式比对)。
/// 读失败返回 None(随包清单缺位——并行波次未落/旧包——不参与漂移判定)。
pub fn lock_fingerprint(lock: &Path) -> Option<String> {
    use sha2::{Digest, Sha256};
    let bytes = std::fs::read(lock).ok()?;
    let digest = Sha256::digest(&bytes);
    Some(digest.iter().map(|byte| format!("{byte:02x}")).collect())
}

// ---------------------------------------------------------------------------
// 探测(design §1①:python 就绪 + 依赖清单指纹)
// ---------------------------------------------------------------------------

/// 探测产物:终态 + 应透出的安装明细步进。
pub struct Detection {
    pub state: PyenvState,
    pub steps: Vec<PyenvStep>,
}

/// 环境探测(纯函数,壳侧单测主战场)。判定链:
/// 1. `installing_steps` 在(安装链在跑)→ installing;
/// 2. 无进度戳:python 也没有 → not_configured(全新装机,D2 空态);
///    python 在 → ready 兜底(手工预置环境:真伪由 serve version 握手与
///    respawn 机制兜底,壳侧不拦死);
/// 3. 戳不可读/不可解析 → error(明细带上原因);
/// 4. 戳 state=error → error(步进原样透出,设置页可重试);
/// 5. 戳 state=ready:python 缺位 → error;依赖指纹与随包清单不一致 →
///    deps_stale;否则 ready;
/// 6. 戳无终态(安装中断)→ error(提示重试;第 3 步幂等续装)。
pub fn detect(
    data_root: &Path,
    bundled_lock: Option<&Path>,
    installing_steps: Option<&[PyenvStep]>,
) -> Detection {
    if let Some(steps) = installing_steps {
        return Detection {
            state: PyenvState::Installing,
            steps: steps.to_vec(),
        };
    }
    let python = python_bin_path(data_root);
    let stamp_text = match std::fs::read_to_string(env_stamp_path(data_root)) {
        Ok(text) => text,
        Err(err) if err.kind() == std::io::ErrorKind::NotFound => {
            return Detection {
                state: if python.exists() {
                    PyenvState::Ready
                } else {
                    PyenvState::NotConfigured
                },
                steps: Vec::new(),
            };
        }
        Err(err) => {
            return Detection {
                state: PyenvState::Error,
                steps: vec![PyenvStep::failed(
                    PyenvPhase::Selfcheck,
                    format!("python-env.json 不可读: {err}"),
                )],
            };
        }
    };
    let stamp: EnvStamp = match serde_json::from_str(&stamp_text) {
        Ok(stamp) => stamp,
        Err(err) => {
            return Detection {
                state: PyenvState::Error,
                steps: vec![PyenvStep::failed(
                    PyenvPhase::Selfcheck,
                    format!("python-env.json 无法解析: {err}"),
                )],
            };
        }
    };
    match stamp.state.as_deref() {
        Some("ready") => {
            if !python.exists() {
                return Detection {
                    state: PyenvState::Error,
                    steps: vec![PyenvStep::failed(
                        PyenvPhase::Selfcheck,
                        format!("环境进度戳记 ready 但 Python 缺位: {}", python.display()),
                    )],
                };
            }
            // 依赖漂移(D4):安装时指纹 vs 当前随包清单指纹;任一侧缺指纹
            // 无从比对 → 不拦(旧戳/清单未随包是并行波次的合法中间态)。
            let drifted = match (
                stamp.deps_fingerprint.as_deref(),
                bundled_lock.and_then(|lock| lock_fingerprint(lock)),
            ) {
                (Some(installed), Some(current)) => installed != current,
                _ => false,
            };
            Detection {
                state: if drifted {
                    PyenvState::DepsStale
                } else {
                    PyenvState::Ready
                },
                steps: stamp.steps,
            }
        }
        Some("error") => Detection {
            state: PyenvState::Error,
            steps: stamp.steps,
        },
        Some(other) => Detection {
            state: PyenvState::Error,
            steps: vec![PyenvStep::failed(
                PyenvPhase::Selfcheck,
                format!("python-env.json 记录未知状态: {other}"),
            )],
        },
        None => {
            // 非终态戳:安装中断(进程退出/断电落在两枚进度戳之间)。
            let mut steps = stamp.steps;
            steps.push(PyenvStep::failed(
                PyenvPhase::Selfcheck,
                "安装链未走到终态(中断):请在设置页重新配置续装(幂等,已装步会跳过)",
            ));
            Detection {
                state: PyenvState::Error,
                steps,
            }
        }
    }
}

/// 该态是否允许 spawn:就绪与依赖漂移放行(漂移是提示不是拦截,D4);
/// 未配置/安装中/异常不 spawn(空态事件走 UI 引导,D2)。
pub fn spawnable(state: PyenvState) -> bool {
    matches!(state, PyenvState::Ready | PyenvState::DepsStale)
}

// ---------------------------------------------------------------------------
// 镜像覆盖落盘
// ---------------------------------------------------------------------------

/// 归一:去空白;空串 → None(= 清回默认源)。
fn normalize_mirror(value: Option<&str>) -> Option<String> {
    value
        .map(|raw| raw.trim().to_string())
        .filter(|trimmed| !trimmed.is_empty())
}

/// 读镜像覆盖;不可读/不可解析 → 缺省(镜像丢失不该拦状态查询,下次保存自愈)。
pub fn read_settings(data_root: &Path) -> PyenvSettings {
    std::fs::read_to_string(pyenv_settings_path(data_root))
        .ok()
        .and_then(|text| serde_json::from_str(&text).ok())
        .unwrap_or_default()
}

/// 写镜像覆盖(MYIA_HOME 显式根可能未建,先建目录)。
pub fn write_settings(data_root: &Path, settings: &PyenvSettings) -> std::io::Result<()> {
    std::fs::create_dir_all(data_root)?;
    let text = serde_json::to_string_pretty(settings).expect("镜像覆盖序列化不可失败");
    std::fs::write(pyenv_settings_path(data_root), text)
}

// ---------------------------------------------------------------------------
// 状态组装(纯 → 胶水)
// ---------------------------------------------------------------------------

/// 纯组装:探测 + 路径 + 镜像 → 契约载荷(单测直接覆盖)。
pub fn status_at(
    data_root: &Path,
    resource_dir: Option<&Path>,
    installing_steps: Option<&[PyenvStep]>,
    settings: &PyenvSettings,
) -> PyenvStatus {
    let bundled_lock = resource_dir.map(resource_lock_path);
    let detection = detect(data_root, bundled_lock.as_deref(), installing_steps);
    PyenvStatus {
        state: detection.state,
        install_path: python_install_dir(data_root),
        python_path: python_bin_path(data_root),
        mirror_runtime: settings.mirror_runtime.clone(),
        mirror_pypi: settings.mirror_pypi.clone(),
        steps: detection.steps,
    }
}

/// 胶水:解析数据根/资源目录/安装内存态 → 当前状态(spawn 与命令共用)。
pub fn current_status(app: &AppHandle) -> Result<PyenvStatus, Box<dyn std::error::Error>> {
    let data_root = crate::data_root(app)?;
    let installing = app
        .state::<PyenvManager>()
        .installing
        .lock()
        .unwrap()
        .clone();
    let settings = read_settings(&data_root);
    let resource_dir = app.path().resource_dir().ok();
    Ok(status_at(
        &data_root,
        resource_dir.as_deref(),
        installing.as_deref(),
        &settings,
    ))
}

/// 协议层「未配置」结构化错误(prd Req 3):`sidecar_request` 在环境未就绪时
/// 报 `pyenv_not_ready`,与进程崩溃的 `sidecar_not_running` 区分;就绪态返回
/// None(调用方回退原语义)。
pub fn unready_error(app: &AppHandle) -> Option<Value> {
    let status = current_status(app).ok()?;
    if spawnable(status.state) {
        return None;
    }
    let hint = match status.state {
        PyenvState::NotConfigured => "Python 运行环境未配置:请在设置页「Python 运行环境」完成配置",
        PyenvState::Installing => "Python 运行环境安装中:请稍候",
        _ => "Python 运行环境异常:请在设置页查看安装明细并重试",
    };
    Some(json!({
        "code": "pyenv_not_ready",
        "path": "$",
        "message": hint,
        "data": status,
    }))
}

// ---------------------------------------------------------------------------
// IPC 命令(契约波次钉死;前端参数键按 tauri 默认映射传 camelCase:
// invoke("pyenv_start_setup", { mirrorRuntime, mirrorPypi }))
// ---------------------------------------------------------------------------

/// 重算状态 + 广播 `pyenv-status-changed`(命令收尾共用)。
fn emit_current(app: &AppHandle) -> Result<PyenvStatus, String> {
    let status = current_status(app).map_err(|e| e.to_string())?;
    let _ = app.emit(PYENV_STATUS_EVENT, &status);
    Ok(status)
}

/// 环境状态查询:三态/五态 + 路径 + 双镜像 + 安装明细(前端初始化以此为准)。
#[tauri::command]
pub async fn pyenv_get_status(app: AppHandle) -> Result<PyenvStatus, String> {
    current_status(&app).map_err(|e| e.to_string())
}

/// 开始配置(D2:显式动作,不自动后台下载)。第 2 步桩:镜像覆盖整体替换式
/// 落盘(缺省 = 默认源;空串归一为缺省),第 3 步安装链读同文件接力执行;
/// 安装本体未落——如实返回当前探测态(尚未配置 = not_configured)。
#[tauri::command]
pub async fn pyenv_start_setup(
    app: AppHandle,
    mirror_runtime: Option<String>,
    mirror_pypi: Option<String>,
) -> Result<PyenvStatus, String> {
    let data_root = crate::data_root(&app).map_err(|e| e.to_string())?;
    let settings = PyenvSettings {
        mirror_runtime: normalize_mirror(mirror_runtime.as_deref()),
        mirror_pypi: normalize_mirror(mirror_pypi.as_deref()),
    };
    write_settings(&data_root, &settings).map_err(|e| e.to_string())?;
    emit_current(&app)
}

/// 同步依赖(D4:依赖漂移时的一键幂等重跑)。第 2 步桩:重探测如实回当前态
/// (deps_stale 维持 deps_stale);第 3/5 步接管安装链 deps 段的幂等重跑。
#[tauri::command]
pub async fn pyenv_sync_deps(app: AppHandle) -> Result<PyenvStatus, String> {
    emit_current(&app)
}

// ---------------------------------------------------------------------------
// 壳侧单测(门:implement.md 第 2 步「壳侧单测」)
// ---------------------------------------------------------------------------

#[cfg(test)]
mod tests {
    use super::*;

    /// 临时数据根 + 可选的「python 已在位」标记(python-build-standalone
    /// install_only 布局只验路径存在性,落个普通文件即足以探测)。
    fn sandbox(python_present: bool) -> tempfile::TempDir {
        let dir = tempfile::tempdir().expect("临时目录创建失败");
        if python_present {
            let bin = python_bin_path(dir.path());
            std::fs::create_dir_all(bin.parent().unwrap()).expect("建 bin 目录失败");
            std::fs::write(&bin, b"#!/bin/sh\n").expect("落 python 标记失败");
        }
        dir
    }

    fn write_stamp(data_root: &Path, body: &str) {
        std::fs::write(env_stamp_path(data_root), body).expect("写进度戳失败");
    }

    /// spawn argv 契约钉死:第 1 步入口模块 myssia_desktop_entry/__main__ 要求
    /// argv[0]=="serve" 才进 RPC(缺参 = 直通 CLI 空.help 退出 0,sidecar 起
    /// 即死)——防 spawn 尾参再被回退掉(质检高危曾犯)。
    #[test]
    fn entry_args_pin_serve_argv_contract() {
        assert_eq!(ENTRY_ARGS, ["-m", "myssia_desktop_entry", "serve"]);
    }

    /// 五个状态枚举的 JSON 字符串恰为契约钉死值。
    #[test]
    fn state_strings_match_ipc_contract() {
        let render = |state| {
            serde_json::to_value(state)
                .unwrap()
                .as_str()
                .unwrap()
                .to_string()
        };
        assert_eq!(render(PyenvState::NotConfigured), "not_configured");
        assert_eq!(render(PyenvState::Installing), "installing");
        assert_eq!(render(PyenvState::Ready), "ready");
        assert_eq!(render(PyenvState::Error), "error");
        assert_eq!(render(PyenvState::DepsStale), "deps_stale");
    }

    /// 契约载荷键集恰为六键;step 键集恰为三键(error 恒在场,无错为 null)。
    #[test]
    fn status_payload_shape_matches_ipc_contract() {
        let status = status_at(
            Path::new("/data"),
            None,
            None,
            &PyenvSettings {
                mirror_runtime: Some("https://mirror.example/runtime.tar.gz".into()),
                mirror_pypi: None,
            },
        );
        let value = serde_json::to_value(&status).unwrap();
        let mut keys: Vec<&str> = value
            .as_object()
            .unwrap()
            .keys()
            .map(String::as_str)
            .collect();
        keys.sort_unstable();
        assert_eq!(
            keys,
            [
                "install_path",
                "mirror_pypi",
                "mirror_runtime",
                "python_path",
                "state",
                "steps"
            ]
        );
        assert_eq!(value["install_path"], "/data/python");
        assert_eq!(value["python_path"], "/data/python/bin/python3");
        assert_eq!(
            value["mirror_runtime"],
            "https://mirror.example/runtime.tar.gz"
        );
        assert_eq!(value["mirror_pypi"], Value::Null);

        let step = serde_json::to_value(PyenvStep::failed(PyenvPhase::Verifying, "boom")).unwrap();
        let mut step_keys: Vec<&str> = step
            .as_object()
            .unwrap()
            .keys()
            .map(String::as_str)
            .collect();
        step_keys.sort_unstable();
        assert_eq!(step_keys, ["error", "phase", "status"]);
        assert_eq!(step["phase"], "verifying");
        assert_eq!(step["status"], "failed");
        assert_eq!(step["error"], "boom");
        // 无错 step:error 恒在场为 null(形态稳定,前端不必判键存在)
        let ok_step = serde_json::to_value(PyenvStep {
            phase: PyenvPhase::Extracting,
            status: PyenvStepStatus::Done,
            error: None,
        })
        .unwrap();
        assert_eq!(ok_step["error"], Value::Null);
    }

    /// spawn 放行表:就绪/依赖漂移放行(D4 漂移不拦);其余三态不 spawn(D2 空态)。
    #[test]
    fn spawnable_matches_design() {
        assert!(spawnable(PyenvState::Ready));
        assert!(spawnable(PyenvState::DepsStale));
        assert!(!spawnable(PyenvState::NotConfigured));
        assert!(!spawnable(PyenvState::Installing));
        assert!(!spawnable(PyenvState::Error));
    }

    /// 平台路径布局:mac/Linux bin/python3;Windows 安装根 python.exe(design §4)。
    #[test]
    fn python_paths_follow_platform_layout() {
        let root = Path::new("/data");
        assert_eq!(
            python_bin_path_on(root, false),
            Path::new("/data/python/bin/python3")
        );
        assert_eq!(
            python_bin_path_on(root, true),
            Path::new("/data/python/python.exe")
        );
        // 当前主机(macOS)走 unix 布局
        assert_eq!(python_bin_path(root), python_bin_path_on(root, false));
    }

    /// 全新数据根 → not_configured,步进为空(D2 引导空态的探测根)。
    #[test]
    fn detect_fresh_root_is_not_configured() {
        let dir = sandbox(false);
        let detection = detect(dir.path(), None, None);
        assert_eq!(detection.state, PyenvState::NotConfigured);
        assert!(detection.steps.is_empty());
    }

    /// 终态 ready 戳 + python 在位 + 指纹一致 → ready,步进原样透出。
    #[test]
    fn detect_ready_stamp_with_matching_fingerprint_is_ready() {
        let dir = sandbox(true);
        let lock = dir.path().join("requirements-lock.txt");
        std::fs::write(&lock, "apprise==1.8.0\n").unwrap();
        let fingerprint = lock_fingerprint(&lock).unwrap();
        write_stamp(
            dir.path(),
            &format!(
                r#"{{"state":"ready","deps_fingerprint":"{fingerprint}",
                     "steps":[{{"phase":"downloading","status":"done","error":null}},
                              {{"phase":"selfcheck","status":"done","error":null}}]}}"#
            ),
        );
        let detection = detect(dir.path(), Some(&lock), None);
        assert_eq!(detection.state, PyenvState::Ready);
        assert_eq!(detection.steps.len(), 2);
        assert_eq!(detection.steps[0].phase, PyenvPhase::Downloading);
        assert_eq!(detection.steps[0].status, PyenvStepStatus::Done);
    }

    /// 随包清单变脸(壳更新,D4)→ deps_stale。
    #[test]
    fn detect_fingerprint_mismatch_is_deps_stale() {
        let dir = sandbox(true);
        let old_lock = dir.path().join("old-lock.txt");
        let new_lock = dir.path().join("new-lock.txt");
        std::fs::write(&old_lock, "apprise==1.8.0\n").unwrap();
        std::fs::write(&new_lock, "apprise==1.9.0\n").unwrap();
        write_stamp(
            dir.path(),
            &format!(
                r#"{{"state":"ready","deps_fingerprint":"{}","steps":[]}}"#,
                lock_fingerprint(&old_lock).unwrap()
            ),
        );
        let detection = detect(dir.path(), Some(&new_lock), None);
        assert_eq!(detection.state, PyenvState::DepsStale);
    }

    /// 指纹任一侧缺位(旧戳/清单未随包)→ 不参与漂移判定,维持 ready。
    #[test]
    fn detect_missing_fingerprint_or_lock_skips_drift_check() {
        let dir = sandbox(true);
        let lock = dir.path().join("requirements-lock.txt");
        std::fs::write(&lock, "apprise==1.8.0\n").unwrap();
        // 戳记无指纹 + 清单在
        write_stamp(dir.path(), r#"{"state":"ready","steps":[]}"#);
        assert_eq!(
            detect(dir.path(), Some(&lock), None).state,
            PyenvState::Ready
        );
        // 戳记有指纹 + 清单缺位(并行波次未落 resources 的合法中间态)
        write_stamp(
            dir.path(),
            &format!(
                r#"{{"state":"ready","deps_fingerprint":"{}","steps":[]}}"#,
                lock_fingerprint(&lock).unwrap()
            ),
        );
        assert_eq!(detect(dir.path(), None, None).state, PyenvState::Ready);
    }

    /// error 终态戳 → error,失败步进的 error 原样透出(设置页可重试可见)。
    #[test]
    fn detect_error_stamp_surfaces_steps() {
        let dir = sandbox(true);
        write_stamp(
            dir.path(),
            r#"{"state":"error","steps":[{"phase":"downloading","status":"failed","error":"network_failed: 连接超时"}]}"#,
        );
        let detection = detect(dir.path(), None, None);
        assert_eq!(detection.state, PyenvState::Error);
        assert_eq!(detection.steps.len(), 1);
        assert_eq!(
            detection.steps[0].error.as_deref(),
            Some("network_failed: 连接超时")
        );
    }

    /// 戳不可解析 → error(结构化原因进 selfcheck 步,不崩)。
    #[test]
    fn detect_unparseable_stamp_is_error() {
        let dir = sandbox(true);
        write_stamp(dir.path(), "{ not json");
        let detection = detect(dir.path(), None, None);
        assert_eq!(detection.state, PyenvState::Error);
        assert!(detection.steps[0]
            .error
            .as_deref()
            .unwrap()
            .contains("无法解析"));
    }

    /// ready 戳但 python 缺位(数据根被清/盘坏)→ error(重装指引)。
    #[test]
    fn detect_ready_stamp_without_python_is_error() {
        let dir = sandbox(false);
        write_stamp(
            dir.path(),
            r#"{"state":"ready","deps_fingerprint":"ab","steps":[]}"#,
        );
        let detection = detect(dir.path(), None, None);
        assert_eq!(detection.state, PyenvState::Error);
        assert!(detection.steps[0]
            .error
            .as_deref()
            .unwrap()
            .contains("Python 缺位"));
    }

    /// 非终态戳(安装中断在两枚进度戳之间)→ error + 重试提示(第 3 步幂等续装)。
    #[test]
    fn detect_interrupted_install_is_error_with_retry_hint() {
        let dir = sandbox(true);
        write_stamp(
            dir.path(),
            r#"{"steps":[{"phase":"downloading","status":"done","error":null}]}"#,
        );
        let detection = detect(dir.path(), None, None);
        assert_eq!(detection.state, PyenvState::Error);
        assert_eq!(detection.steps.len(), 2); // 原步进 + 追加的失败项
        assert!(detection.steps[1]
            .error
            .as_deref()
            .unwrap()
            .contains("中断"));
    }

    /// python 在而戳不在(手工预置环境)→ ready 兜底:真伪由 serve version
    /// 握手与 respawn 兜底,壳侧不拦死(见模块注释)。
    #[test]
    fn detect_python_without_stamp_falls_back_to_ready() {
        let dir = sandbox(true);
        let detection = detect(dir.path(), None, None);
        assert_eq!(detection.state, PyenvState::Ready);
    }

    /// 安装链内存步进在 → installing 优先(第 3 步接管;本步恒 None 但钉行为)。
    #[test]
    fn detect_installing_in_memory_wins() {
        let dir = sandbox(false);
        let steps = vec![PyenvStep {
            phase: PyenvPhase::Downloading,
            status: PyenvStepStatus::Running,
            error: None,
        }];
        let detection = detect(dir.path(), None, Some(&steps));
        assert_eq!(detection.state, PyenvState::Installing);
        assert_eq!(detection.steps, steps);
    }

    /// 镜像覆盖:写读回环 + 归一(空白串 → 缺省;带空白 URL → 修剪)。
    #[test]
    fn mirror_settings_roundtrip_and_normalize() {
        let dir = sandbox(false);
        assert_eq!(
            normalize_mirror(Some("  https://mirror.example/pypi  ")).as_deref(),
            Some("https://mirror.example/pypi")
        );
        assert_eq!(normalize_mirror(Some("   ")), None);
        assert_eq!(normalize_mirror(None), None);

        let settings = PyenvSettings {
            mirror_runtime: Some("https://mirror.example/runtime.tar.gz".into()),
            mirror_pypi: None,
        };
        write_settings(dir.path(), &settings).unwrap();
        assert_eq!(read_settings(dir.path()), settings);
        // 坏文件自愈为缺省(镜像丢失不拦状态查询)
        std::fs::write(pyenv_settings_path(dir.path()), "{ broken").unwrap();
        assert_eq!(read_settings(dir.path()), PyenvSettings::default());
    }

    /// PyenvNotReadyError 可从 Box<dyn Error> downcast —— respawn 路径靠它
    /// 区分「环境未就绪(转空态、停重试)」与「io 失败(按退避续试)」。
    #[test]
    fn not_ready_error_downcasts_through_box() {
        let error: Box<dyn std::error::Error> = Box::new(PyenvNotReadyError(PyenvStatus {
            state: PyenvState::NotConfigured,
            install_path: PathBuf::from("/data/python"),
            python_path: PathBuf::from("/data/python/bin/python3"),
            mirror_runtime: None,
            mirror_pypi: None,
            steps: Vec::new(),
        }));
        let not_ready = error.downcast_ref::<PyenvNotReadyError>().unwrap();
        assert_eq!(not_ready.0.state, PyenvState::NotConfigured);
        assert!(error.to_string().contains("未就绪"));
    }
}
