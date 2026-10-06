//! 桌面自管 Python 环境 —— 安装链执行器(10-05-desktop-managed-py-env 第 3 步)。
//!
//! 决议与设计出处:prd.md D1-D6(Req 2/AC1)/ design.md §1④ §3 §5。
//! 状态机 `idle → downloading → verifying → extracting → installing_deps →
//! selfcheck → ready | error(可重试)`,五阶段即 IPC steps[].phase 契约面。
//!
//! == 幂等与进度戳(design §3「每步完成落 <数据根>/python-env.json」)==
//! - 每次状态迁移(含 running)落盘进度戳(临时文件 + 同目录 rename 原子写);
//!   state 仅终态落 ready/error,进行中恒 null——进程重启后探测侧(第 2 步
//!   detect)按非终态判「中断可重试」,installing 是壳内存态不落盘。
//! - 重跑跳过已完成步,跳过判据 = 上一轮戳记 + 落盘实况双保险:
//!   downloading/verifying:本地归档在且 sha256 == manifest 钉值;
//!   extracting:`<数据根>/<python_bin>` 在位(解压走暂存目录 + 原子改名,
//!   终位出现即完整,不存在半截 python/);
//!   installing_deps:戳记 deps_fingerprint == 当前随包锁版清单指纹(指纹只在
//!   依赖步完成后才落盘,不会误跳过未装完的依赖);
//!   selfcheck:恒重跑(终门,秒级,重验环境真实可用)。
//! - 运行时包缓存 `<数据根>/downloads/runtime-<triple>.tar.gz`:成功后保留
//!   (幂等续装/修复跑免重下,~15-38MB);坏包(校验不过)即删,重试必重下。
//!
//! == 镜像覆盖(design §5 双镜像;D3「镜像覆盖只换 URL 不绕校验」)==
//! - mirror_runtime:整串替换下载 URL;sha256 恒取 manifest 钉值,镜像源
//!   内容对不上照样 checksum_mismatch。
//! - mirror_pypi:pip `--index-url` 覆盖;缺省 PyPI。
//! - 两者由 pyenv_start_setup 落 `<数据根>/pyenv-settings.json`(第 2 步),
//!   本模块读同文件接力。
//!
//! == 错误分类(结构化;steps[].error = "<kind>: <明细>" 前缀约定,
//!    五类用户可重试面 + setup_failed 内部类)==
//! network_failed / checksum_mismatch / disk_full / pip_failed /
//! selfcheck_failed / setup_failed(manifest 缺失、内部 io 等)。
//!
//! == 自检(design §3「起 sidecar 握手 version ping」)==
//! 与常驻 spawn 同源 argv(pyenv::ENTRY_ARGS)拉起短命 serve 进程,
//! stdin 写 version 请求即关(EOF=干净退出契约,entry.py serve),限时读回
//! 首行应答并校验 {id==1, result.name=="myssia"};PYTHONPATH=随包
//! Resources/myssia-src、MYIA_HOME=数据根,与常驻 spawn 注入面一致。
//!
//! == 线程模型 ==
//! 安装链跑在专用 std 线程(不占 tokio worker;reqwest 用阻塞客户端)。
//! 进度回调更新第 2 步 PyenvManager.installing 槽 + 广播
//! `pyenv-status-changed`(载荷与 pyenv_get_status 恒一致,经 emit_current
//! 重算);终态由胶水清槽后重算广播,成功即拉起常驻 sidecar
//! (main.rs spawn_sidecar_if_idle,AC1 主链),失败补发 pyenv_not_ready(D2)。

use std::fs;
use std::io::{Read, Write};
use std::path::{Component, Path, PathBuf};
use std::process::{Child, Command, Stdio};
use std::sync::{Arc, Mutex};
use std::time::Duration;

use serde::Deserialize;
use serde_json::Value;
use sha2::{Digest, Sha256};
use tauri::{AppHandle, Emitter, Manager};

use crate::pyenv::{self, PyenvPhase, PyenvSettings, PyenvStep, PyenvStepStatus};

/// 随包运行时清单资源文件名(tauri.conf resources 映射后位于 resource_dir 下)。
pub(crate) const MANIFEST_RESOURCE_FILE: &str = "runtime-manifest.json";
/// 编译目标三元组 = manifest 平台键(第 1 步钉死:平台键用 Rust target triple;
/// tauri::utils::platform::target_triple 与 updater 同源,运行时按宿主实况定)。
fn host_target_triple() -> Result<String, (InstallErrorKind, String)> {
    tauri::utils::platform::target_triple().map_err(|e| {
        (
            InstallErrorKind::SetupFailed,
            format!("宿主 target triple 不可定: {e}"),
        )
    })
}
/// 下载缓存目录名(数据根下)。
const DOWNLOADS_DIR: &str = "downloads";
/// 解压暂存目录名(数据根下;终位原子改名,残留即清)。
const STAGING_DIR: &str = ".pyenv-staging";
/// 磁盘预检门槛(design §3「需 ~500MB 余量」;下载+解压+依赖总量兜底)。
pub(crate) const DISK_REQUIRED_BYTES: u64 = 500 * 1024 * 1024;
/// 下载连接超时。
const DOWNLOAD_CONNECT_TIMEOUT: Duration = Duration::from_secs(30);
/// 下载总超时(38MB 包在极慢网络下的宽松上限;防无限挂死)。
const DOWNLOAD_TOTAL_TIMEOUT: Duration = Duration::from_secs(1800);
/// 自检 version 应答超时(serve 起活应秒级)。
const SELFCHECK_TIMEOUT: Duration = Duration::from_secs(30);
/// 自检后等待干净退出的宽限(EOF → exit 0 契约),超时 kill 兜底。
const SELFCHECK_EXIT_GRACE: Duration = Duration::from_secs(5);
/// pip 失败明细保留的输出尾部长度(防长日志撑爆 steps[].error)。
const PIP_OUTPUT_TAIL: usize = 1500;
/// 进度戳临时文件名(同目录 rename 原子写)。
const STAMP_TMP_FILE: &str = ".python-env.json.tmp";

// ---------------------------------------------------------------------------
// 错误分类(结构化;渲染约定 "<kind>: <明细>",前缀即分类码)
// ---------------------------------------------------------------------------

/// 安装链错误分类。前五类为契约钉死的用户可重试面(ask/design §3),
/// `SetupFailed` 是内部类(manifest 缺失/形态不符、非磁盘类 io 等)。
/// pub(crate):组件机制(pyenv_components)复用同一分类与渲染口径。
#[derive(Clone, Copy, PartialEq, Eq, Debug)]
pub(crate) enum InstallErrorKind {
    NetworkFailed,
    ChecksumMismatch,
    DiskFull,
    PipFailed,
    SelfcheckFailed,
    SetupFailed,
}

impl InstallErrorKind {
    fn as_str(self) -> &'static str {
        match self {
            InstallErrorKind::NetworkFailed => "network_failed",
            InstallErrorKind::ChecksumMismatch => "checksum_mismatch",
            InstallErrorKind::DiskFull => "disk_full",
            InstallErrorKind::PipFailed => "pip_failed",
            InstallErrorKind::SelfcheckFailed => "selfcheck_failed",
            InstallErrorKind::SetupFailed => "setup_failed",
        }
    }
}

/// 渲染为 steps[].error 字符串(分类码前缀,前端可据此分类重试文案)。
/// pub(crate):组件机制(10-05-table-restore)复用同一错误分类渲染口径。
pub(crate) fn render_error(kind: InstallErrorKind, detail: impl std::fmt::Display) -> String {
    format!("{}: {}", kind.as_str(), detail)
}

/// 本地 io 错误归类:空间类 → disk_full,其余 → setup_failed。
fn classify_io(err: &std::io::Error) -> InstallErrorKind {
    if matches!(
        err.kind(),
        std::io::ErrorKind::StorageFull | std::io::ErrorKind::WriteZero
    ) {
        InstallErrorKind::DiskFull
    } else {
        InstallErrorKind::SetupFailed
    }
}

// ---------------------------------------------------------------------------
// manifest 解析(第 1 步随包 runtime-manifest.json;平台键 = target triple)
// ---------------------------------------------------------------------------

/// 随包运行时清单(字段宽容:未知附加字段忽略;platforms 缺省空表)。
#[derive(Deserialize)]
struct RuntimeManifest {
    #[serde(default)]
    manifest_version: u32,
    #[serde(default)]
    platforms: std::collections::HashMap<String, PlatformRuntime>,
}

/// 单平台运行时条目(钉版:url + sha256 + 布局;D3)。
#[derive(Deserialize, Clone)]
struct PlatformRuntime {
    url: String,
    sha256: String,
    archive: String,
    extract_root_dir: String,
    python_bin: String,
}

fn load_manifest(path: &Path) -> Result<RuntimeManifest, (InstallErrorKind, String)> {
    let text = fs::read_to_string(path).map_err(|e| {
        (
            InstallErrorKind::SetupFailed,
            format!("runtime-manifest 不可读({}): {e}", path.display()),
        )
    })?;
    let manifest: RuntimeManifest = serde_json::from_str(&text).map_err(|e| {
        (
            InstallErrorKind::SetupFailed,
            format!("runtime-manifest 解析失败: {e}"),
        )
    })?;
    if manifest.manifest_version != 1 {
        return Err((
            InstallErrorKind::SetupFailed,
            format!("不支持的 manifest_version: {}", manifest.manifest_version),
        ));
    }
    Ok(manifest)
}

/// 单一目录名(无分隔、非 `.`/`..`)——extract_root_dir 防御性校验。
fn is_single_component(s: &str) -> bool {
    !s.is_empty() && s != "." && s != ".." && Path::new(s).components().count() == 1
}

/// 相对安全路径(无根前缀、无 `..` 段)——python_bin 防御性校验。
fn is_safe_relative(s: &str) -> bool {
    !s.is_empty()
        && Path::new(s)
            .components()
            .all(|c| matches!(c, Component::Normal(_) | Component::CurDir))
}

fn same_components(a: &Path, b: &Path) -> bool {
    a.components().eq(b.components())
}

// ---------------------------------------------------------------------------
// sha256 / 磁盘预检 / 进度戳(原子写)
// ---------------------------------------------------------------------------

/// 文件流式 sha256(hex 小写;读失败 None)。
fn file_sha256(path: &Path) -> Option<String> {
    let mut file = fs::File::open(path).ok()?;
    let mut hasher = Sha256::new();
    let mut buffer = [0u8; 64 * 1024];
    loop {
        let read = file.read(&mut buffer).ok()?;
        if read == 0 {
            break;
        }
        hasher.update(&buffer[..read]);
    }
    let digest = hasher.finalize();
    Some(digest.iter().map(|byte| format!("{byte:02x}")).collect())
}

/// 磁盘预检(design §3:~500MB 余量;在链首执行,覆盖下载+解压+依赖总量)。
/// pub(crate):组件安装(10-05-table-restore)复用同一预检门。
pub(crate) fn disk_precheck(
    data_root: &Path,
    required: u64,
) -> Result<(), (InstallErrorKind, String)> {
    fs::create_dir_all(data_root).map_err(|e| {
        (
            InstallErrorKind::SetupFailed,
            format!("数据根不可建({}): {e}", data_root.display()),
        )
    })?;
    let free = fs2::available_space(data_root).map_err(|e| {
        (
            InstallErrorKind::SetupFailed,
            format!("磁盘余量查询失败: {e}"),
        )
    })?;
    if free < required {
        return Err((
            InstallErrorKind::DiskFull,
            format!(
                "磁盘余量不足: 可用 {:.0} MB,需 {:.0} MB",
                free as f64 / 1e6,
                required as f64 / 1e6
            ),
        ));
    }
    Ok(())
}

/// 进度戳原子写(临时文件 + 同目录 rename;崩溃不落半截 JSON)。
fn write_stamp(data_root: &Path, stamp: &pyenv::EnvStamp) -> Result<(), std::io::Error> {
    fs::create_dir_all(data_root)?;
    let text = serde_json::to_string_pretty(stamp).expect("进度戳序列化不可失败");
    let tmp = data_root.join(STAMP_TMP_FILE);
    fs::write(&tmp, text)?;
    fs::rename(&tmp, pyenv::env_stamp_path(data_root))
}

// ---------------------------------------------------------------------------
// 安装链本体(纯逻辑,无 AppHandle;单测主战场)
// ---------------------------------------------------------------------------

/// 安装链入参(胶水从 AppHandle 解析;测试直接构造)。
pub(crate) struct ChainConfig {
    /// 数据根(安装目标与进度戳/镜像文件所在)。
    pub data_root: PathBuf,
    /// 随包资源目录(resource_dir;自检 PYTHONPATH 与 manifest/锁版清单定位)。
    pub resource_dir: PathBuf,
    /// manifest 路径(默认 resource_dir/runtime-manifest.json;测试可指沙箱)。
    pub manifest_path: PathBuf,
    /// 随包锁版清单路径(pip -r 入参 + 漂移指纹基准)。
    pub lock_path: PathBuf,
    /// 镜像覆盖(读 pyenv-settings.json 的快照)。
    pub settings: PyenvSettings,
    /// 仅依赖段(pip + 自检;D4「同步依赖」,运行时段标记 skipped)。
    pub deps_only: bool,
    /// 磁盘预检门槛(默认 DISK_REQUIRED_BYTES;测试可注小值/u64::MAX)。
    pub disk_required_bytes: u64,
    /// 目标三元组(manifest 平台键;默认 HOST_TRIPLE,测试用合成键)。
    pub target_triple: String,
    /// 壳版本号(下载 UA + 自检 MYIA_APP_VERSION 注入)。
    pub app_version: String,
}

/// 链终态(success=false 时失败明细已在 steps[].error)。
pub(crate) struct ChainOutcome {
    pub success: bool,
    pub steps: Vec<PyenvStep>,
}

/// 五阶段顺序表(IPC steps 契约序)。
const PHASES: [PyenvPhase; 5] = [
    PyenvPhase::Downloading,
    PyenvPhase::Verifying,
    PyenvPhase::Extracting,
    PyenvPhase::InstallingDeps,
    PyenvPhase::Selfcheck,
];

/// 初始步进:全 pending;deps_only 模式运行时段直接标 skipped。
fn initial_steps(deps_only: bool) -> Vec<PyenvStep> {
    PHASES
        .iter()
        .map(|&phase| {
            let runtime_phase = matches!(
                phase,
                PyenvPhase::Downloading | PyenvPhase::Verifying | PyenvPhase::Extracting
            );
            PyenvStep {
                phase,
                status: if deps_only && runtime_phase {
                    PyenvStepStatus::Skipped
                } else {
                    PyenvStepStatus::Pending
                },
                error: None,
            }
        })
        .collect()
}

/// 链执行器:持有步进与戳记态,逐阶段推进。
struct Runner<'a> {
    cfg: &'a ChainConfig,
    python_bin: PathBuf,
    steps: Vec<PyenvStep>,
    /// 依赖指纹(依赖步完成/跳过时落值;终态 ready 戳携带,D4 漂移基准)。
    deps_fingerprint: Option<String>,
    on_update: &'a dyn Fn(&[PyenvStep]),
}

impl<'a> Runner<'a> {
    fn idx(&self, phase: PyenvPhase) -> usize {
        self.steps
            .iter()
            .position(|step| step.phase == phase)
            .expect("五阶段步进恒在")
    }

    fn status(&self, phase: PyenvPhase) -> PyenvStepStatus {
        self.steps[self.idx(phase)].status
    }

    fn set(&mut self, phase: PyenvPhase, status: PyenvStepStatus, error: Option<String>) {
        let idx = self.idx(phase);
        self.steps[idx].status = status;
        self.steps[idx].error = error;
    }

    /// 落非终态戳(state=null;进行中)。
    fn persist(&self) {
        let stamp = pyenv::EnvStamp {
            state: None,
            deps_fingerprint: self.deps_fingerprint.clone(),
            steps: self.steps.clone(),
        };
        if let Err(err) = write_stamp(&self.cfg.data_root, &stamp) {
            log::warn!("desktop: 安装链进度戳写入失败(继续执行): {err}");
        }
    }

    /// 广播步进快照(更新 installing 内存槽 + pyenv-status-changed)。
    fn publish(&self) {
        (self.on_update)(&self.steps);
    }

    fn running(&mut self, phase: PyenvPhase) {
        self.set(phase, PyenvStepStatus::Running, None);
        self.persist();
        self.publish();
    }

    fn done(&mut self, phase: PyenvPhase) {
        self.set(phase, PyenvStepStatus::Done, None);
        self.persist();
        self.publish();
    }

    fn skip(&mut self, phase: PyenvPhase) {
        self.set(phase, PyenvStepStatus::Skipped, None);
    }

    /// 落终态戳(ready/error;state 终态值)。
    fn persist_terminal(&self, state: &str) {
        let stamp = pyenv::EnvStamp {
            state: Some(state.to_string()),
            deps_fingerprint: self.deps_fingerprint.clone(),
            steps: self.steps.clone(),
        };
        if let Err(err) = write_stamp(&self.cfg.data_root, &stamp) {
            log::warn!("desktop: 安装链终态戳写入失败: {err}");
        }
    }

    /// 终态成功:落 ready 戳(终态广播由胶水清槽后重算,不在此回调——
    /// 否则 installing 槽压过终态探测)。
    fn finish_ok(mut self) -> ChainOutcome {
        self.set(PyenvPhase::Selfcheck, PyenvStepStatus::Done, None);
        self.persist_terminal("ready");
        ChainOutcome {
            success: true,
            steps: self.steps,
        }
    }

    /// 终态失败:failed 步 + error 戳。可重试(幂等续装)。
    fn fail(
        mut self,
        phase: PyenvPhase,
        kind: InstallErrorKind,
        detail: impl std::fmt::Display,
    ) -> ChainOutcome {
        self.set(
            phase,
            PyenvStepStatus::Failed,
            Some(render_error(kind, detail)),
        );
        self.persist_terminal("error");
        ChainOutcome {
            success: false,
            steps: self.steps,
        }
    }
}

/// setup 级失败(manifest 缺失/形态不符):无 Runner 时的独立落戳路径。
fn setup_failure(
    cfg: &ChainConfig,
    on_update: &dyn Fn(&[PyenvStep]),
    kind: InstallErrorKind,
    detail: impl std::fmt::Display,
) -> ChainOutcome {
    let mut steps = initial_steps(cfg.deps_only);
    let phase = if cfg.deps_only {
        PyenvPhase::InstallingDeps
    } else {
        PyenvPhase::Downloading
    };
    let idx = steps
        .iter()
        .position(|s| s.phase == phase)
        .expect("五阶段恒在");
    steps[idx].status = PyenvStepStatus::Failed;
    steps[idx].error = Some(render_error(kind, detail));
    let stamp = pyenv::EnvStamp {
        state: Some("error".into()),
        deps_fingerprint: None,
        steps: steps.clone(),
    };
    if let Err(err) = write_stamp(&cfg.data_root, &stamp) {
        log::warn!("desktop: 安装链终态戳写入失败: {err}");
    }
    on_update(&steps);
    ChainOutcome {
        success: false,
        steps,
    }
}

/// 下载运行时包(design §3:HTTPS;镜像只换 URL 不绕校验)。
/// 落 `<数据根>/downloads/runtime-<triple>.tar.gz`(先 .part 后改名,
/// 半截文件永不冒充完整包)。
fn download_runtime(
    url: &str,
    dest: &Path,
    app_version: &str,
) -> Result<(), (InstallErrorKind, String)> {
    install_ring_provider_if_missing();
    let client = reqwest::blocking::Client::builder()
        .connect_timeout(DOWNLOAD_CONNECT_TIMEOUT)
        .timeout(DOWNLOAD_TOTAL_TIMEOUT)
        .user_agent(format!("myssia-desktop/{app_version}"))
        .build()
        .map_err(|e| {
            (
                InstallErrorKind::NetworkFailed,
                format!("HTTP 客户端构建失败: {e}"),
            )
        })?;
    let response = client
        .get(url)
        .send()
        .and_then(|resp| resp.error_for_status())
        .map_err(|e| {
            (
                InstallErrorKind::NetworkFailed,
                format!("下载失败({url}): {e}"),
            )
        })?;
    if let Some(parent) = dest.parent() {
        fs::create_dir_all(parent).map_err(|e| {
            (
                classify_io(&e),
                format!("下载目录不可建({}): {e}", parent.display()),
            )
        })?;
    }
    let part = PathBuf::from(format!("{}.part", dest.display()));
    let mut file = fs::File::create(&part).map_err(|e| {
        (
            classify_io(&e),
            format!("临时文件创建失败({}): {e}", part.display()),
        )
    })?;
    let mut response = response;
    let copied = std::io::copy(&mut response, &mut file)
        .map_err(|e| (classify_io(&e), format!("下载写入失败: {e}")))?;
    let _ = file.sync_all();
    drop(file);
    fs::rename(&part, dest).map_err(|e| (classify_io(&e), format!("下载收尾改名失败: {e}")))?;
    log::info!("desktop: 运行时包下载完成({copied}B)← {url}");
    Ok(())
}

/// reqwest(rustls-no-provider 栈,与 tauri-plugin-updater 同款)需要
/// process 级 crypto provider;updater 只在自查更新时装,这里兜底装 ring。
/// pub(crate):服务组件健康探测(pyenv_components,轨B)复用同一兜底。
pub(crate) fn install_ring_provider_if_missing() {
    if rustls::crypto::CryptoProvider::get_default().is_none() {
        let _ = rustls::crypto::ring::default_provider().install_default();
    }
}

/// sha256 校验(manifest 钉值;镜像绕不过)。坏包即删,重试必重下。
fn verify_runtime(archive: &Path, expected_sha256: &str) -> Result<(), (InstallErrorKind, String)> {
    let actual = file_sha256(archive).ok_or((
        InstallErrorKind::SetupFailed,
        format!("归档不可读({})", archive.display()),
    ))?;
    let expected = expected_sha256.trim().to_ascii_lowercase();
    if actual != expected {
        let _ = fs::remove_file(archive); // 坏包不缓存
        return Err((
            InstallErrorKind::ChecksumMismatch,
            format!(
                "sha256 不符: 期望 {expected},实得 {actual}({})",
                archive.display()
            ),
        ));
    }
    Ok(())
}

/// 解压 install_only tar.gz:暂存目录解压 → 校根目录 → 原子改名就位。
/// 终位 `<数据根>/python/` 一旦出现即完整(幂等续装的跳过依据)。
fn extract_runtime(
    archive: &Path,
    data_root: &Path,
    extract_root_dir: &str,
) -> Result<(), (InstallErrorKind, String)> {
    let staging = data_root.join(STAGING_DIR);
    if staging.exists() {
        fs::remove_dir_all(&staging).map_err(|e| {
            (
                classify_io(&e),
                format!("暂存目录残留清理失败({}): {e}", staging.display()),
            )
        })?;
    }
    fs::create_dir_all(&staging).map_err(|e| {
        (
            classify_io(&e),
            format!("暂存目录不可建({}): {e}", staging.display()),
        )
    })?;
    let file = fs::File::open(archive).map_err(|e| {
        (
            classify_io(&e),
            format!("归档打开失败({}): {e}", archive.display()),
        )
    })?;
    let mut tar = tar::Archive::new(flate2::read::GzDecoder::new(file));
    tar.set_preserve_permissions(true);
    tar.unpack(&staging).map_err(|e| {
        (
            InstallErrorKind::SetupFailed,
            format!("解压失败(归档 sha256 已验过但不可解压,疑 manifest 钉版有误): {e}"),
        )
    })?;
    let extracted_root = staging.join(extract_root_dir);
    if !extracted_root.is_dir() {
        return Err((
            InstallErrorKind::SetupFailed,
            format!(
                "归档根目录缺失: 期望 {}/,实际不在({})",
                extract_root_dir,
                extracted_root.display()
            ),
        ));
    }
    let target = data_root.join(extract_root_dir);
    if target.exists() {
        fs::remove_dir_all(&target).map_err(|e| {
            (
                classify_io(&e),
                format!("旧安装目录清理失败({}): {e}", target.display()),
            )
        })?;
    }
    fs::rename(&extracted_root, &target).map_err(|e| {
        (
            classify_io(&e),
            format!(
                "安装目录就位改名失败({} → {}): {e}",
                extracted_root.display(),
                target.display()
            ),
        )
    })?;
    let _ = fs::remove_dir_all(&staging); // 暂存残壳清理,失败不拦(下次自清)
    log::info!("desktop: 运行时解压就位: {}", target.display());
    Ok(())
}

/// pip 锁版装依赖(design §3:环境内 pip install -r 随包清单;索引可覆盖)。
/// pip 自身幂等(已装 pinned 版 → Requirement already satisfied,AC4 已装跳过)。
fn run_pip(
    python: &Path,
    lock: &Path,
    index_url: Option<&str>,
) -> Result<(), (InstallErrorKind, String)> {
    run_pip_install(
        python,
        vec!["-r".into(), lock.as_os_str().to_os_string()],
        index_url,
    )
}

/// 组件 pip spec 安装(10-05-table-restore 组件机制:spec 为位置参数,不走
/// -r——`-r rapid-table==…` 会被 pip 当 requirements 文件读,语义即错)。
/// spec 字符串可含空格分隔多条(组件闭包,与 pyproject extras 同源),逐条
/// 作位置参数传 pip install(`pip install a==1 b>=2` 标准形态)。与主链
/// run_pip 同源:同一子进程组装段(索引覆盖/PYTHONPATH 隔离/失败尾部回显),
/// 消费方 pyenv_components.rs。
pub(crate) fn run_pip_spec(
    python: &Path,
    spec: &str,
    index_url: Option<&str>,
) -> Result<(), (InstallErrorKind, String)> {
    let requirements: Vec<std::ffi::OsString> = spec
        .split_whitespace()
        .map(std::ffi::OsString::from)
        .collect();
    if requirements.is_empty() {
        return Err((
            InstallErrorKind::PipFailed,
            "pip spec 为空(全空白):注册表条目无效".to_string(),
        ));
    }
    run_pip_install(python, requirements, index_url)
}

/// 组件安装后浏览器钩子(10-06-native-plugin-components 轨A:crawl4ai):
/// 用同一自管 pyenv 的 playwright 拉 chromium 二进制进
/// `<数据根>/playwright-browsers`(PLAYWRIGHT_BROWSERS_PATH 注入值,与
/// main.rs spawn_sidecar 运行时注入同目录——装与用必须同源)。浏览器只落
/// 数据根(卸载组件/清理数据根即整目录消,不散落 OS 缓存区,G-Q6);与
/// run_pip_install 同款子进程纪律:剥 PYTHONPATH(Req 4)、失败输出尾部回显;
/// 错误分类复用 pip_failed(用户可重试面同族;重跑幂等——已装二进制跳过)。
pub(crate) fn run_playwright_install_chromium(
    python: &Path,
    browsers_path: &Path,
) -> Result<(), (InstallErrorKind, String)> {
    let mut command = Command::new(python);
    command.args(["-m", "playwright", "install", "chromium"]);
    command.env("PLAYWRIGHT_BROWSERS_PATH", browsers_path);
    // 与开发 Python 分家(Req 4):playwright 不见壳进程可能继承的 PYTHONPATH。
    command.env_remove("PYTHONPATH");
    let output = command.output().map_err(|e| {
        (
            InstallErrorKind::PipFailed,
            format!("playwright 拉起失败({}): {e}", python.display()),
        )
    })?;
    if output.status.success() {
        return Ok(());
    }
    let mut combined = String::from_utf8_lossy(&output.stdout).into_owned();
    combined.push_str(&String::from_utf8_lossy(&output.stderr));
    let tail: String = combined
        .chars()
        .skip(combined.chars().count().saturating_sub(PIP_OUTPUT_TAIL))
        .collect();
    Err((
        InstallErrorKind::PipFailed,
        format!(
            "playwright install chromium 退出码 {:?},输出尾部: {}",
            output.status.code(),
            tail.trim_end()
        ),
    ))
}

/// pip install 子进程公共段:argv 组装(-m pip install --no-input
/// --disable-pip-version-check <requirement_args> [--index-url …])、剥
/// PYTHONPATH(Req 4 与开发 Python 分家)、失败输出尾部回显(PIP_OUTPUT_TAIL)。
fn run_pip_install(
    python: &Path,
    requirement_args: Vec<std::ffi::OsString>,
    index_url: Option<&str>,
) -> Result<(), (InstallErrorKind, String)> {
    run_pip_install_with_extra_flags(python, requirement_args, index_url, &[])
}

/// run_pip_install 的带额外 flag 形态(当前唯一消费方:轨B searxng 源码包
/// 二段装的 --no-build-isolation;flag 插在 requirement 之前,与手写 argv
/// `pip install … --no-build-isolation <reqs>` 同形)。
fn run_pip_install_with_extra_flags(
    python: &Path,
    requirement_args: Vec<std::ffi::OsString>,
    index_url: Option<&str>,
    extra_flags: &[&str],
) -> Result<(), (InstallErrorKind, String)> {
    let mut command = Command::new(python);
    command.args([
        "-m",
        "pip",
        "install",
        "--no-input",
        "--disable-pip-version-check",
    ]);
    command.args(extra_flags);
    command.args(&requirement_args);
    if let Some(index) = index_url {
        command.args(["--index-url", index]);
    }
    // 与开发 Python 分家(Req 4):pip 不见壳进程可能继承的 PYTHONPATH。
    command.env_remove("PYTHONPATH");
    let output = command.output().map_err(|e| {
        (
            InstallErrorKind::PipFailed,
            format!("pip 拉起失败({}): {e}", python.display()),
        )
    })?;
    if output.status.success() {
        return Ok(());
    }
    let mut combined = String::from_utf8_lossy(&output.stdout).into_owned();
    combined.push_str(&String::from_utf8_lossy(&output.stderr));
    let tail: String = combined
        .chars()
        .skip(combined.chars().count().saturating_sub(PIP_OUTPUT_TAIL))
        .collect();
    Err((
        InstallErrorKind::PipFailed,
        format!(
            "pip 退出码 {:?},输出尾部: {}",
            output.status.code(),
            tail.trim_end()
        ),
    ))
}

/// 组件源码包二段安装(10-06-native-plugin-components 轨B:searxng)。
///
/// 上游现实(2026-10-06 沙箱实测):searxng 真身**不在 PyPI**(PyPI 同名包
/// 是无关 MCP 包装器),只能 git 钉 commit 装;且其 setup.py 构建期
/// ``from searx import get_setting`` 即 import 运行时依赖(msgspec 等),
/// PEP517 构建隔离态下单发安装必败(ModuleNotFoundError)。故闭包拆两段:
/// 一段 run_pip_spec 装钉版依赖闭包(-r 上游 commit 钉版 requirements.txt
/// 原文 URL)+ granian + setuptools/wheel 构建后端;二段本函数用
/// ``--no-build-isolation`` 装源码包直引 spec(依赖已在场,构建期 import
/// 全部可解析)。与 run_pip_install 同款子进程纪律(剥 PYTHONPATH/失败输出
/// 尾部回显);错误分类复用 pip_failed(用户可重试面同族;重跑幂等——
/// 已装自动跳过)。PyPI 镜像 --index-url 只覆盖 PyPI 依赖解析,git 直引
/// 段走 github.com(与 Playwright CDN 同理,镜像不覆盖属预期,文案已披露)。
pub(crate) fn run_pip_src_no_build_isolation(
    python: &Path,
    src_spec: &str,
    index_url: Option<&str>,
) -> Result<(), (InstallErrorKind, String)> {
    if src_spec.trim().is_empty() {
        return Err((
            InstallErrorKind::PipFailed,
            "pip_src spec 为空(全空白):注册表条目无效".to_string(),
        ));
    }
    run_pip_install_with_extra_flags(
        python,
        vec![std::ffi::OsString::from(src_spec)],
        index_url,
        &["--no-build-isolation"],
    )
}

/// version ping 自检:短命 serve 进程握手(与常驻 spawn 同源 argv/env 注入)。
pub(crate) fn selfcheck_version_ping(
    python: &Path,
    resource_dir: &Path,
    data_root: &Path,
    app_version: &str,
) -> Result<(), (InstallErrorKind, String)> {
    use std::io::BufRead;
    let mut child = Command::new(python)
        .args(pyenv::ENTRY_ARGS)
        .env("PYTHONPATH", pyenv::resource_src_dir(resource_dir))
        .env("MYIA_HOME", data_root)
        .env("MYIA_APP_VERSION", app_version)
        .stdin(Stdio::piped())
        .stdout(Stdio::piped())
        .stderr(Stdio::piped())
        .spawn()
        .map_err(|e| {
            (
                InstallErrorKind::SelfcheckFailed,
                format!("自检进程拉起失败({}): {e}", python.display()),
            )
        })?;
    // stderr 异步收集(失败明细;不死等——进程退出即 EOF)。
    let stderr_buffer: Arc<Mutex<Vec<u8>>> = Arc::new(Mutex::new(Vec::new()));
    if let Some(stderr) = child.stderr.take() {
        let sink = Arc::clone(&stderr_buffer);
        std::thread::spawn(move || {
            use std::io::Read;
            let mut sink_guard = sink.lock().unwrap();
            let _ = std::io::BufReader::new(stderr).read_to_end(&mut sink_guard);
        });
    }
    let stderr_tail = || {
        let buffer = stderr_buffer.lock().unwrap();
        let text = String::from_utf8_lossy(&buffer).into_owned();
        let count = text.chars().count();
        text.chars()
            .skip(count.saturating_sub(600))
            .collect::<String>()
    };
    // 写请求即关 stdin:serve 逐行应答后 EOF 干净退出(entry.py serve 契约)。
    if let Some(mut stdin) = child.stdin.take() {
        let _ = writeln!(stdin, r#"{{"id":1,"method":"version","params":{{}}}}"#);
        let _ = stdin.flush();
    }
    let stdout = child.stdout.take().expect("stdout piped");
    let (tx, rx) = std::sync::mpsc::channel::<Option<String>>();
    std::thread::spawn(move || {
        let mut line = String::new();
        let read = std::io::BufReader::new(stdout)
            .read_line(&mut line)
            .unwrap_or(0);
        let _ = tx.send(if read > 0 { Some(line) } else { None });
    });
    let line = match rx.recv_timeout(SELFCHECK_TIMEOUT) {
        Ok(Some(line)) => line,
        Ok(None) => {
            let _ = child.kill();
            let _ = child.wait();
            return Err((
                InstallErrorKind::SelfcheckFailed,
                format!(
                    "自检进程无应答即退出(缺依赖/崩溃?): stderr 尾部: {}",
                    stderr_tail()
                ),
            ));
        }
        Err(_) => {
            let _ = child.kill();
            let _ = child.wait();
            return Err((
                InstallErrorKind::SelfcheckFailed,
                format!("自检 version 应答超时({}s)", SELFCHECK_TIMEOUT.as_secs()),
            ));
        }
    };
    let reply: Value = serde_json::from_str(line.trim_end()).map_err(|e| {
        (
            InstallErrorKind::SelfcheckFailed,
            format!("自检应答非 JSON({e}): {line:?}"),
        )
    })?;
    if let Some(error) = reply.get("error") {
        return Err((
            InstallErrorKind::SelfcheckFailed,
            format!("自检应答报错: {error}"),
        ));
    }
    let id_ok = reply.get("id").and_then(Value::as_u64) == Some(1);
    let name_ok = reply.pointer("/result/name").and_then(Value::as_str) == Some("myssia");
    if !id_ok || !name_ok {
        return Err((
            InstallErrorKind::SelfcheckFailed,
            format!("自检应答形态不符(非 version 结果): {line:?}"),
        ));
    }
    wait_with_grace(&mut child, SELFCHECK_EXIT_GRACE);
    log::info!(
        "desktop: 自检 version ping 通过({})",
        reply
            .pointer("/result/version")
            .and_then(Value::as_str)
            .unwrap_or("?")
    );
    Ok(())
}

/// 限时等子进程退出(EOF → 0 契约);宽限过后 kill 兜底,绝不悬挂。
fn wait_with_grace(child: &mut Child, grace: Duration) {
    let deadline = std::time::Instant::now() + grace;
    loop {
        match child.try_wait() {
            Ok(Some(_)) => return,
            Ok(None) if std::time::Instant::now() < deadline => {
                std::thread::sleep(Duration::from_millis(50))
            }
            _ => {
                let _ = child.kill();
                let _ = child.wait();
                return;
            }
        }
    }
}

/// 安装链入口(catch_unwind 兜底:线程 panic 也落 error 终态戳,
/// 防非终态戳 + 死线程把状态卡在「中断」语义之外)。
pub(crate) fn run_chain(cfg: &ChainConfig, on_update: &dyn Fn(&[PyenvStep])) -> ChainOutcome {
    match std::panic::catch_unwind(std::panic::AssertUnwindSafe(|| execute(cfg, on_update))) {
        Ok(outcome) => outcome,
        Err(payload) => {
            let detail = if let Some(text) = payload.downcast_ref::<&str>() {
                (*text).to_string()
            } else if let Some(text) = payload.downcast_ref::<String>() {
                text.clone()
            } else {
                "未知 panic".to_string()
            };
            log::error!("desktop: 安装链线程 panic: {detail}");
            let mut steps = pyenv::read_stamp(&cfg.data_root)
                .map(|stamp| stamp.steps)
                .unwrap_or_default();
            let phase = steps
                .iter()
                .rev()
                .find(|step| step.status == PyenvStepStatus::Running)
                .map(|step| step.phase)
                .unwrap_or(PyenvPhase::Selfcheck);
            steps.retain(|step| step.phase != phase);
            steps.push(PyenvStep {
                phase,
                status: PyenvStepStatus::Failed,
                error: Some(render_error(
                    InstallErrorKind::SetupFailed,
                    format!("安装线程异常退出: {detail}"),
                )),
            });
            let stamp = pyenv::EnvStamp {
                state: Some("error".into()),
                deps_fingerprint: None,
                steps: steps.clone(),
            };
            if let Err(err) = write_stamp(&cfg.data_root, &stamp) {
                log::warn!("desktop: panic 兜底终态戳写入失败: {err}");
            }
            ChainOutcome {
                success: false,
                steps,
            }
        }
    }
}

/// 状态机主体(纯逻辑:manifest 解析 → 幂等跳过判定 → 磁盘预检 → 五阶段)。
fn execute(cfg: &ChainConfig, on_update: &dyn Fn(&[PyenvStep])) -> ChainOutcome {
    // —— manifest 解析与防御性校验 ——
    let manifest = match load_manifest(&cfg.manifest_path) {
        Ok(manifest) => manifest,
        Err((kind, detail)) => return setup_failure(cfg, on_update, kind, detail),
    };
    let platform = match manifest.platforms.get(&cfg.target_triple) {
        Some(platform) => platform.clone(),
        None => {
            return setup_failure(
                cfg,
                on_update,
                InstallErrorKind::SetupFailed,
                format!(
                    "runtime-manifest 无本平台条目: {}(有: {:?})",
                    cfg.target_triple,
                    manifest.platforms.keys().collect::<Vec<_>>()
                ),
            )
        }
    };
    if platform.archive != "tar.gz" {
        return setup_failure(
            cfg,
            on_update,
            InstallErrorKind::SetupFailed,
            format!("不支持的归档形态: {}", platform.archive),
        );
    }
    if !is_single_component(&platform.extract_root_dir) {
        return setup_failure(
            cfg,
            on_update,
            InstallErrorKind::SetupFailed,
            format!(
                "extract_root_dir 必须是单一目录名: {:?}",
                platform.extract_root_dir
            ),
        );
    }
    if !is_safe_relative(&platform.python_bin) {
        return setup_failure(
            cfg,
            on_update,
            InstallErrorKind::SetupFailed,
            format!("python_bin 必须是安全相对路径: {:?}", platform.python_bin),
        );
    }
    // 布局一致性守卫:manifest 是解压布局权威,壳 spawn 路径是 pyenv.rs 常量
    // (第 2 步);二者漂移会让 ready 后常驻 spawn 断链,装配期即拦。
    // 比对取数据根相对形态(manifest python_bin 为数据根相对路径)。
    let spawn_layout =
        pyenv::python_bin_path_on(&cfg.data_root, cfg.target_triple.contains("windows"));
    let spawn_layout_rel = spawn_layout
        .strip_prefix(&cfg.data_root)
        .unwrap_or(&spawn_layout);
    if !same_components(Path::new(&platform.python_bin), spawn_layout_rel) {
        return setup_failure(
            cfg,
            on_update,
            InstallErrorKind::SetupFailed,
            format!(
                "manifest python_bin({}) 与壳 spawn 布局({})不一致",
                platform.python_bin,
                spawn_layout_rel.display()
            ),
        );
    }

    let archive_path = cfg
        .data_root
        .join(DOWNLOADS_DIR)
        .join(format!("runtime-{}.tar.gz", cfg.target_triple));
    let python_bin = cfg.data_root.join(&platform.python_bin);
    let lock_fingerprint = pyenv::lock_fingerprint(&cfg.lock_path);
    let prior = pyenv::read_stamp(&cfg.data_root).unwrap_or_default();

    let mut runner = Runner {
        cfg,
        python_bin,
        steps: initial_steps(cfg.deps_only),
        deps_fingerprint: None,
        on_update,
    };

    // —— 幂等跳过判定(落盘实况为准,戳记作辅助)——
    if !cfg.deps_only {
        let expected = platform.sha256.trim().to_ascii_lowercase();
        let archive_ok = !expected.is_empty()
            && archive_path.is_file()
            && file_sha256(&archive_path).as_deref() == Some(expected.as_str());
        if archive_ok {
            runner.skip(PyenvPhase::Downloading);
            runner.skip(PyenvPhase::Verifying);
        }
        if runner.python_bin.exists() {
            runner.skip(PyenvPhase::Extracting);
        }
    }
    // 依赖指纹一致(戳记指纹只在依赖步完成后落盘)= 上一轮已按当前清单装完。
    let deps_installed = matches!(
        (prior.deps_fingerprint.as_deref(), lock_fingerprint.as_deref()),
        (Some(installed), Some(current)) if installed == current
    );
    if deps_installed {
        runner.skip(PyenvPhase::InstallingDeps);
        runner.deps_fingerprint = lock_fingerprint.clone();
    }

    // 初始快照落戳 + 广播(UI 即刻见五阶段与跳过判定)。
    runner.persist();
    runner.publish();

    // —— 磁盘预检(仅当确有大块落盘动作:下载/解压/依赖任一将跑)——
    let needs_space = [
        PyenvPhase::Downloading,
        PyenvPhase::Extracting,
        PyenvPhase::InstallingDeps,
    ]
    .iter()
    .any(|&phase| runner.status(phase) == PyenvStepStatus::Pending);
    if needs_space {
        if let Err((kind, detail)) = disk_precheck(&cfg.data_root, cfg.disk_required_bytes) {
            let phase = if cfg.deps_only {
                PyenvPhase::InstallingDeps
            } else {
                PyenvPhase::Downloading
            };
            return runner.fail(phase, kind, detail);
        }
    }

    // —— downloading(镜像只换 URL,sha256 恒取 manifest 钉值)——
    if runner.status(PyenvPhase::Downloading) == PyenvStepStatus::Pending {
        runner.running(PyenvPhase::Downloading);
        let url = cfg
            .settings
            .mirror_runtime
            .clone()
            .unwrap_or_else(|| platform.url.clone());
        match download_runtime(&url, &archive_path, &cfg.app_version) {
            Ok(()) => runner.done(PyenvPhase::Downloading),
            Err((kind, detail)) => return runner.fail(PyenvPhase::Downloading, kind, detail),
        }
    }

    // —— verifying ——
    if runner.status(PyenvPhase::Verifying) == PyenvStepStatus::Pending {
        runner.running(PyenvPhase::Verifying);
        match verify_runtime(&archive_path, &platform.sha256) {
            Ok(()) => runner.done(PyenvPhase::Verifying),
            Err((kind, detail)) => return runner.fail(PyenvPhase::Verifying, kind, detail),
        }
    }

    // —— extracting ——
    if runner.status(PyenvPhase::Extracting) == PyenvStepStatus::Pending {
        runner.running(PyenvPhase::Extracting);
        match extract_runtime(&archive_path, &cfg.data_root, &platform.extract_root_dir) {
            Ok(()) => runner.done(PyenvPhase::Extracting),
            Err((kind, detail)) => return runner.fail(PyenvPhase::Extracting, kind, detail),
        }
    }

    // —— installing_deps(pip 锁版;索引覆盖)——
    if runner.status(PyenvPhase::InstallingDeps) == PyenvStepStatus::Pending {
        runner.running(PyenvPhase::InstallingDeps);
        match run_pip(
            &runner.python_bin,
            &cfg.lock_path,
            cfg.settings.mirror_pypi.as_deref(),
        ) {
            Ok(()) => {
                runner.deps_fingerprint = lock_fingerprint.clone();
                runner.done(PyenvPhase::InstallingDeps);
            }
            Err((kind, detail)) => return runner.fail(PyenvPhase::InstallingDeps, kind, detail),
        }
    }

    // —— selfcheck(恒重跑:终门重验环境真实可用)——
    runner.running(PyenvPhase::Selfcheck);
    match selfcheck_version_ping(
        &runner.python_bin,
        &cfg.resource_dir,
        &cfg.data_root,
        &cfg.app_version,
    ) {
        Ok(()) => runner.finish_ok(),
        Err((kind, detail)) => return runner.fail(PyenvPhase::Selfcheck, kind, detail),
    }
}

// ---------------------------------------------------------------------------
// 环境体检(10-05 主人判例:就绪态主按钮=「检查状态」,查出错引导重装)
// ---------------------------------------------------------------------------

/// 体检单项(IPC 契约:`{id, ok, detail}`;
/// id = python_binary | deps_fingerprint | sidecar_handshake)。
#[derive(Clone, serde::Serialize)]
pub struct PyenvVerifyCheck {
    pub id: String,
    pub ok: bool,
    pub detail: String,
}

/// 体检结果(IPC 契约:`{ok, checks:[…]}`;ok = 全部单项通过)。
#[derive(serde::Serialize)]
pub struct PyenvVerifyResult {
    pub ok: bool,
    pub checks: Vec<PyenvVerifyCheck>,
}

/// 环境体检三查:①python 二进制在位且可执行(--version);②依赖指纹
/// 与随包锁版清单一致(进度戳 vs 现算);③sidecar version 握手(与安装链
/// selfcheck 同源)。只读不落戳、不翻状态、不碰网络——查出错的重装入口
/// = pyenv_start_setup 幂等链(已装步全跳过);指纹单项漂移对应
/// deps_stale 的「同步依赖」,detail 内自带引导。
#[tauri::command]
pub async fn pyenv_verify(app: AppHandle) -> Result<PyenvVerifyResult, String> {
    let data_root = crate::data_root(&app).map_err(|e| e.to_string())?;
    let resource_dir = app.path().resource_dir().map_err(|e| e.to_string())?;
    let status = pyenv::current_status(&app).map_err(|e| e.to_string())?;
    let python = PathBuf::from(&status.python_path);

    let mut checks: Vec<PyenvVerifyCheck> = Vec::new();

    // ① 二进制在位 + 可执行(握手的前置;缺位则 ③ 不单独跑)
    let (binary_ok, binary_detail) = if python.exists() {
        match Command::new(&python).arg("--version").output() {
            Ok(output) if output.status.success() => (
                true,
                String::from_utf8_lossy(&output.stdout).trim().to_string(),
            ),
            Ok(output) => (
                false,
                format!(
                    "退出码 {:?}:{} {}",
                    output.status.code(),
                    String::from_utf8_lossy(&output.stdout).trim(),
                    String::from_utf8_lossy(&output.stderr).trim()
                ),
            ),
            Err(err) => (false, format!("拉起失败: {err}")),
        }
    } else {
        (false, format!("二进制缺位: {}", python.display()))
    };
    checks.push(PyenvVerifyCheck {
        id: "python_binary".into(),
        ok: binary_ok,
        detail: binary_detail,
    });

    // ② 依赖指纹:进度戳落值 vs 随包锁版清单现算(同 lock_fingerprint 口径)
    let stamp_fp = pyenv::read_stamp(&data_root).and_then(|stamp| stamp.deps_fingerprint);
    let lock_fp = pyenv::lock_fingerprint(&pyenv::resource_lock_path(&resource_dir));
    let (fp_ok, fp_detail) = match (&stamp_fp, &lock_fp) {
        (Some(recorded), Some(current)) if recorded == current => {
            (true, format!("一致({current})"))
        }
        (Some(recorded), Some(current)) => (
            false,
            format!("漂移:进度戳 {recorded} ≠ 随包 {current};「同步依赖」幂等对齐,或重装"),
        ),
        (None, Some(_)) => (false, "进度戳无依赖指纹(安装链未走完;重装可重建)".into()),
        (Some(_), None) => (false, "随包锁版清单缺位(壳资源异常;重装不可自愈需换包)".into()),
        (None, None) => (false, "进度戳与随包清单双双缺位;重装可重建".into()),
    };
    checks.push(PyenvVerifyCheck {
        id: "deps_fingerprint".into(),
        ok: fp_ok,
        detail: fp_detail,
    });

    // ③ sidecar version 握手(python 缺位时跳过——① 已定位根因,不重复报)
    if binary_ok {
        let app_version = app.package_info().version.to_string();
        let (shake_ok, shake_detail) =
            match selfcheck_version_ping(&python, &resource_dir, &data_root, &app_version) {
                Ok(()) => (true, "version 应答正常".into()),
                Err((_, detail)) => (false, detail),
            };
        checks.push(PyenvVerifyCheck {
            id: "sidecar_handshake".into(),
            ok: shake_ok,
            detail: shake_detail,
        });
    }

    let ok = checks.iter().all(|check| check.ok);
    Ok(PyenvVerifyResult { ok, checks })
}

// ---------------------------------------------------------------------------
// 胶水:AppHandle → 后台安装线程(IPC 命令 pyenv_start_setup/sync_deps 调用)
// ---------------------------------------------------------------------------

/// 拉起后台安装线程(幂等护栏:安装进行中拒绝二次启动;组件 pip 单飞
/// 在跑时同样拒启——主链 deps 段与组件 pip 都写同一自管环境)。
/// 即刻占坑 installing 槽并广播,链体在专用 std 线程推进,进度经
/// `pyenv-status-changed` 广播、终态经戳记 + 重算广播。
pub(crate) fn start_install_thread(app: AppHandle, deps_only: bool) -> Result<(), String> {
    let data_root = crate::data_root(&app).map_err(|e| e.to_string())?;
    let resource_dir = app.path().resource_dir().map_err(|e| e.to_string())?;
    let settings = pyenv::read_settings(&data_root);
    // —— 护栏:组件 pip 单飞在跑(与组件侧反向护栏对称:pyenv_components.rs
    //    pyenv_install_component 先查本侧 installing 再占组件坑,这里先查
    //    组件坑再占主链坑)。先后双锁非原子,TOCTOU 残余窗极窄且两侧对称,
    //    不为此扩权(单锁结构改动不成比例);消息风格镜像组件侧反向护栏。
    if app
        .state::<crate::pyenv_components::ComponentManager>()
        .installing
        .lock()
        .unwrap()
        .is_some()
    {
        return Err("组件安装进行中:请等组件安装完成后再开始安装或同步 Python 环境".into());
    }
    {
        let manager = app.state::<pyenv::PyenvManager>();
        let mut slot = manager.installing.lock().unwrap();
        if slot.is_some() {
            return Err("Python 环境安装已在进行中,请稍候".into());
        }
        *slot = Some(initial_steps(deps_only));
    }
    let _ = pyenv::emit_current(&app); // 广播 installing(含初始步进)
    let app_for_thread = app.clone();
    let spawn_result = std::thread::Builder::new()
        .name("pyenv-install".into())
        .spawn(move || {
            install_thread_main(app_for_thread, data_root, resource_dir, settings, deps_only)
        });
    if let Err(err) = spawn_result {
        // 线程起不来:回滚占坑,防 installing 槽死锁后续重试。
        *app.state::<pyenv::PyenvManager>()
            .installing
            .lock()
            .unwrap() = None;
        return Err(format!("安装线程启动失败: {err}"));
    }
    Ok(())
}

/// 安装线程主体:跑链 → 清槽 → 终态广播(成功拉起常驻 sidecar / 失败补空态)。
fn install_thread_main(
    app: AppHandle,
    data_root: PathBuf,
    resource_dir: PathBuf,
    settings: PyenvSettings,
    deps_only: bool,
) {
    // 三元组不可定(极端宿主)→ 空串走 setup_failed(「无本平台条目」明细)。
    let target_triple = host_target_triple().unwrap_or_default();
    let cfg = ChainConfig {
        manifest_path: resource_dir.join(MANIFEST_RESOURCE_FILE),
        lock_path: resource_dir.join(pyenv::RESOURCE_LOCK_FILE),
        app_version: app.package_info().version.to_string(),
        target_triple,
        disk_required_bytes: DISK_REQUIRED_BYTES,
        data_root,
        resource_dir,
        settings,
        deps_only,
    };
    let app_for_updates = app.clone();
    let on_update = move |steps: &[PyenvStep]| {
        *app_for_updates
            .state::<pyenv::PyenvManager>()
            .installing
            .lock()
            .unwrap() = Some(steps.to_vec());
        let _ = pyenv::emit_current(&app_for_updates);
    };
    let outcome = run_chain(&cfg, &on_update);
    // 终态:清 installing 槽 → 按戳记重算真实态并广播。
    *app.state::<pyenv::PyenvManager>()
        .installing
        .lock()
        .unwrap() = None;
    let status = pyenv::emit_current(&app);
    if outcome.success {
        // 就绪即拉起常驻 sidecar(AC1 主链:安装完成 → 服务可用,不等前端动作;
        // 幂等:进程健在不动作,绝不杀活进程)。
        if let Err(err) = crate::spawn_sidecar_if_idle(&app) {
            log::warn!("desktop: 安装链就绪但常驻 sidecar 拉起失败(可手动拉起): {err}");
        }
    } else if let Ok(status) = status {
        let _ = app.emit(pyenv::PYENV_NOT_READY_EVENT, &status);
    }
    let failure_note = outcome
        .steps
        .iter()
        .rev()
        .find(|step| step.status == PyenvStepStatus::Failed)
        .and_then(|step| step.error.clone())
        .unwrap_or_default();
    if outcome.success {
        log::info!("desktop: 安装链终态: ready(deps_only={deps_only})");
    } else {
        log::warn!(
            "desktop: 安装链终态: error(deps_only={deps_only}): {failure_note}"
        );
    }
}

// ---------------------------------------------------------------------------
// 单测(门:implement.md 第 3 步「单测(含坏包/中断重试);本地静态服务器
// 钉版文件全链真跑」)。design §8:「本地起静态服务器供运行时 tar.gz(钉版
// 文件本地化)全链真跑」——归档为钉版结构(python/bin/python3 等)的合成
// tar.gz + 合成 manifest(sha256 实算),下载/校验/解压/pip/自检五段全部
// 真跑:HTTP 真下载(reqwest 阻塞栈)、sha256 真校验、tar.gz 真解压、
// 真子进程 stub python(pip/serve 按 argv 分发)。真运行时(15-38MB)+
// 真 pip 依赖的端到端属第 5 步沙箱门(AC1),不在此重复。
// 依赖 sh 桩的部分 #[cfg(unix)] 门控(CI windows 仅编译不跑测)。
// ---------------------------------------------------------------------------

#[cfg(test)]
mod tests {
    use super::*;
    use crate::pyenv::PyenvState;
    use std::sync::atomic::{AtomicUsize, Ordering};

    /// stub python 的 serve 语义(自检段行为注入;坏自检两形态 + 正常)。
    #[derive(Clone, Copy, Debug)]
    enum ServeMode {
        Ok,
        Garbage,
        Exit,
    }

    // —— 本地静态服务器(手写 HTTP/1.0;零新依赖)——

    enum ServerBehavior {
        Serve(Vec<u8>),
        NotFound,
        Drop,
    }

    struct TestServer {
        addr: std::net::SocketAddr,
        requests: Arc<AtomicUsize>,
    }

    impl TestServer {
        fn url(&self, path: &str) -> String {
            format!("http://127.0.0.1:{}{path}", self.addr.port())
        }

        fn request_count(&self) -> usize {
            self.requests.load(Ordering::SeqCst)
        }
    }

    fn start_test_server(behavior: ServerBehavior) -> TestServer {
        let listener = std::net::TcpListener::bind("127.0.0.1:0").expect("测试服务器绑定失败");
        let addr = listener.local_addr().expect("测试服务器端口解析失败");
        let requests = Arc::new(AtomicUsize::new(0));
        let counter = Arc::clone(&requests);
        std::thread::spawn(move || {
            for stream in listener.incoming() {
                let mut stream = match stream {
                    Ok(stream) => stream,
                    Err(_) => break,
                };
                counter.fetch_add(1, Ordering::SeqCst);
                let _ = stream.set_read_timeout(Some(Duration::from_secs(5)));
                // 丢弃请求头(读到 \r\n\r\n 界;GET 无 body)
                let mut seen = Vec::new();
                let mut buffer = [0u8; 1024];
                while !seen.ends_with(b"\r\n\r\n") && seen.len() < 8192 {
                    match stream.read(&mut buffer) {
                        Ok(0) | Err(_) => break,
                        Ok(n) => seen.extend_from_slice(&buffer[..n]),
                    }
                }
                match &behavior {
                    ServerBehavior::Serve(body) => {
                        let mut response = format!(
                            "HTTP/1.0 200 OK\r\nContent-Length: {}\r\nConnection: close\r\n\r\n",
                            body.len()
                        )
                        .into_bytes();
                        response.extend_from_slice(body);
                        let _ = stream.write_all(&response);
                        let _ = stream.flush();
                    }
                    ServerBehavior::NotFound => {
                        let _ = stream.write_all(
                            b"HTTP/1.0 404 Not Found\r\nContent-Length: 0\r\nConnection: close\r\n\r\n",
                        );
                        let _ = stream.flush();
                    }
                    ServerBehavior::Drop => {} // 连接即断,不给应答
                }
                let _ = stream.shutdown(std::net::Shutdown::Both);
            }
        });
        TestServer { addr, requests }
    }

    // —— 钉版结构合成运行时归档(install_only 布局:根目录 python/)——

    fn sha256_hex(bytes: &[u8]) -> String {
        let digest = Sha256::digest(bytes);
        digest.iter().map(|byte| format!("{byte:02x}")).collect()
    }

    /// 合成 install_only tar.gz:python/bin/python3 = 按 argv 分发的 sh 桩
    /// (pip 记账/可控失败;serve 应答 version ping/坏应答/即退)。
    fn build_stub_runtime(pip_log: &Path, fail_marker: &Path, serve: ServeMode) -> Vec<u8> {
        let serve_branch = match serve {
            ServeMode::Ok => concat!(
                r#"cat >/dev/null 2>&1"#,
                "\n",
                r#"  printf '%s\n' '{"id":1,"result":{"name":"myssia","version":"stub","protocol":10,"app_version":"0.0.1-test"}}'"#,
                "\n",
                "  exit 0",
            ),
            ServeMode::Garbage => concat!(
                r#"cat >/dev/null 2>&1"#,
                "\n",
                "  printf 'not-json\\n'\n",
                "  exit 0",
            ),
            ServeMode::Exit => "  exit 3",
        };
        let script = format!(
            "#!/bin/sh\n\
             # 第 3 步安装链单测桩:按 argv 分发 pip / serve 语义\n\
             if [ \"$1\" = \"-m\" ] && [ \"$2\" = \"pip\" ]; then\n\
             \x20 printf '%s\\n' \"$*\" >> '{pip_log}'\n\
             \x20 if [ -f '{fail_marker}' ]; then\n\
             \x20   echo 'stub pip boom' >&2\n\
             \x20   exit 1\n\
             \x20 fi\n\
             \x20 exit 0\n\
             fi\n\
             if [ \"$1\" = \"-m\" ] && [ \"$2\" = \"myssia_desktop_entry\" ]; then\n\
             {serve_branch}\n\
             fi\n\
             exit 1\n",
            pip_log = pip_log.display(),
            fail_marker = fail_marker.display(),
            serve_branch = serve_branch,
        );
        let mut compressed =
            flate2::write::GzEncoder::new(Vec::new(), flate2::Compression::default());
        {
            let mut builder = tar::Builder::new(&mut compressed);
            let append = |builder: &mut tar::Builder<&mut flate2::write::GzEncoder<Vec<u8>>>,
                          path: &str,
                          mode: u32,
                          data: &[u8]| {
                let mut header = tar::Header::new_gnu();
                header.set_size(data.len() as u64);
                header.set_mode(mode);
                header.set_mtime(1);
                header.set_cksum();
                builder
                    .append_data(&mut header, path, data)
                    .expect("合成归档追加失败");
            };
            append(&mut builder, "python/bin/python3", 0o755, script.as_bytes());
            append(
                &mut builder,
                "python/lib/dummy.txt",
                0o644,
                b"stub runtime payload\n",
            );
            builder.into_inner().expect("合成归档封卷失败");
        }
        compressed.finish().expect("合成归档压缩收尾失败")
    }

    /// 测试夹具:沙箱数据根 + 沙箱资源根(manifest/锁版清单);归档与
    /// sha256 由调用方拿到后再起服务器/写 manifest(URL 依赖端口)。
    struct Fixture {
        data: tempfile::TempDir,
        resource: tempfile::TempDir,
        archive_bytes: Vec<u8>,
        archive_sha256: String,
        pip_log: PathBuf,
        pip_fail_marker: PathBuf,
    }

    /// 测试用平台键(manifest 平台键形如 target triple;非 windows 词根 →
    /// unix 布局,与 pyenv::python_bin_path_on 守卫自洽)。
    const TEST_TRIPLE: &str = "test-host-triple";

    fn fixture(serve: ServeMode) -> Fixture {
        let data = tempfile::tempdir().expect("数据根临时目录创建失败");
        let resource = tempfile::tempdir().expect("资源根临时目录创建失败");
        let pip_log = data.path().join("pip-invocations.log");
        let pip_fail_marker = data.path().join("pip-fail-marker");
        let archive_bytes = build_stub_runtime(&pip_log, &pip_fail_marker, serve);
        let archive_sha256 = sha256_hex(&archive_bytes);
        Fixture {
            data,
            resource,
            archive_bytes,
            archive_sha256,
            pip_log,
            pip_fail_marker,
        }
    }

    impl Fixture {
        /// 写合成 manifest(钉版:sha256 实算;布局 = install_only)。
        fn write_manifest(&self, url: &str, sha256: &str) {
            let manifest = serde_json::json!({
                "manifest_version": 1,
                "platforms": {
                    TEST_TRIPLE: {
                        "url": url,
                        "sha256": sha256,
                        "archive": "tar.gz",
                        "extract_root_dir": "python",
                        "python_bin": "python/bin/python3",
                    }
                }
            });
            fs::write(
                self.resource.path().join(MANIFEST_RESOURCE_FILE),
                serde_json::to_string_pretty(&manifest).unwrap(),
            )
            .expect("合成 manifest 写入失败");
        }

        /// manifest 变体:自定义平台键/布局(负例守卫用)。
        fn write_manifest_variant(&self, body: serde_json::Value) {
            fs::write(
                self.resource.path().join(MANIFEST_RESOURCE_FILE),
                serde_json::to_string_pretty(&body).unwrap(),
            )
            .expect("合成 manifest 变体写入失败");
        }

        fn write_lock(&self, content: &str) -> PathBuf {
            let path = self.resource.path().join(pyenv::RESOURCE_LOCK_FILE);
            fs::write(&path, content).expect("锁版清单写入失败");
            path
        }

        fn lock_path(&self) -> PathBuf {
            self.resource.path().join(pyenv::RESOURCE_LOCK_FILE)
        }

        fn cfg(&self, settings: PyenvSettings) -> ChainConfig {
            self.cfg_with(settings, false, 1024 * 1024)
        }

        fn cfg_with(
            &self,
            settings: PyenvSettings,
            deps_only: bool,
            disk_required: u64,
        ) -> ChainConfig {
            ChainConfig {
                data_root: self.data.path().to_path_buf(),
                resource_dir: self.resource.path().to_path_buf(),
                manifest_path: self.resource.path().join(MANIFEST_RESOURCE_FILE),
                lock_path: self.lock_path(),
                settings,
                deps_only,
                disk_required_bytes: disk_required,
                target_triple: TEST_TRIPLE.into(),
                app_version: "0.0.1-test".into(),
            }
        }

        fn archive_cache_path(&self) -> PathBuf {
            self.data
                .path()
                .join(DOWNLOADS_DIR)
                .join(format!("runtime-{TEST_TRIPLE}.tar.gz"))
        }

        fn python_path(&self) -> PathBuf {
            self.data.path().join("python/bin/python3")
        }

        fn stamp_text(&self) -> String {
            fs::read_to_string(pyenv::env_stamp_path(self.data.path())).expect("进度戳读取失败")
        }

        fn pip_log_lines(&self) -> Vec<String> {
            fs::read_to_string(&self.pip_log)
                .map(|text| text.lines().map(String::from).collect())
                .unwrap_or_default()
        }
    }

    /// 跑链 + 记录进度回调快照(断言广播节奏用)。
    fn run_with_recording(cfg: &ChainConfig) -> (ChainOutcome, Vec<Vec<PyenvStep>>) {
        let updates = Arc::new(Mutex::new(Vec::new()));
        let sink = Arc::clone(&updates);
        let outcome = run_chain(cfg, &move |steps: &[PyenvStep]| {
            sink.lock().unwrap().push(steps.to_vec());
        });
        let updates = updates.lock().unwrap().clone();
        (outcome, updates)
    }

    fn step_status(steps: &[PyenvStep], phase: PyenvPhase) -> PyenvStepStatus {
        steps
            .iter()
            .find(|step| step.phase == phase)
            .expect("五阶段恒在")
            .status
    }

    fn step_error(steps: &[PyenvStep], phase: PyenvPhase) -> String {
        steps
            .iter()
            .find(|step| step.phase == phase)
            .expect("五阶段恒在")
            .error
            .clone()
            .expect("失败步应带 error 明细")
    }

    fn all_statuses(steps: &[PyenvStep]) -> Vec<PyenvStepStatus> {
        steps.iter().map(|step| step.status).collect()
    }

    // —— 纯逻辑测试(全平台)——

    /// 错误分类字符串恰为契约钉死值(五类用户面 + setup_failed 内部类)。
    #[test]
    fn error_kind_strings_are_pinned() {
        assert_eq!(InstallErrorKind::NetworkFailed.as_str(), "network_failed");
        assert_eq!(
            InstallErrorKind::ChecksumMismatch.as_str(),
            "checksum_mismatch"
        );
        assert_eq!(InstallErrorKind::DiskFull.as_str(), "disk_full");
        assert_eq!(InstallErrorKind::PipFailed.as_str(), "pip_failed");
        assert_eq!(
            InstallErrorKind::SelfcheckFailed.as_str(),
            "selfcheck_failed"
        );
        assert_eq!(InstallErrorKind::SetupFailed.as_str(), "setup_failed");
        // steps[].error 渲染 = "<kind>: <明细>"(分类码前缀可机判)
        assert_eq!(
            render_error(InstallErrorKind::DiskFull, "余量 3 MB"),
            "disk_full: 余量 3 MB"
        );
    }

    /// deps_only 模式初始步进:运行时段直接 skipped,依赖/自检 pending。
    #[test]
    fn initial_steps_deps_only_marks_runtime_phases_skipped() {
        let full = initial_steps(false);
        assert_eq!(full.len(), 5);
        assert!(full
            .iter()
            .all(|step| step.status == PyenvStepStatus::Pending));
        let deps_only = initial_steps(true);
        assert_eq!(
            all_statuses(&deps_only),
            [
                PyenvStepStatus::Skipped,
                PyenvStepStatus::Skipped,
                PyenvStepStatus::Skipped,
                PyenvStepStatus::Pending,
                PyenvStepStatus::Pending,
            ]
        );
        assert!(deps_only.iter().all(|step| step.error.is_none()));
    }

    /// 防御性路径校验:extract_root_dir 单一目录名;python_bin 安全相对路径。
    #[test]
    fn path_guards_reject_traversal_and_absolute() {
        assert!(is_single_component("python"));
        assert!(!is_single_component("python/bin"));
        assert!(!is_single_component(""));
        assert!(!is_single_component("."));
        assert!(!is_single_component(".."));
        assert!(is_safe_relative("python/bin/python3"));
        assert!(!is_safe_relative("/abs/python3"));
        assert!(!is_safe_relative("../escape"));
        assert!(!is_safe_relative(""));
        assert!(same_components(
            Path::new("python/bin/python3"),
            Path::new("python/bin/python3")
        ));
        assert!(!same_components(
            Path::new("python/bin/python3"),
            Path::new("python/python.exe")
        ));
    }

    // —— 全链真跑测试(unix:sh 桩 + 本地 HTTP)——

    #[cfg(unix)]
    mod chain {
        use super::*;

        /// 全链真跑:本地静态服务器 → 下载 → sha256 → 解压 → pip → 自检 → ready;
        /// 进度戳形态与第 2 步读者(detect)闭环。
        #[test]
        fn full_chain_over_local_http_reaches_ready() {
            let fixture = fixture(ServeMode::Ok);
            let lock = fixture.write_lock("apprise==1.8.0\n");
            let server = start_test_server(ServerBehavior::Serve(fixture.archive_bytes.clone()));
            fixture.write_manifest(&server.url("/runtime.tar.gz"), &fixture.archive_sha256);
            let (outcome, updates) = run_with_recording(&fixture.cfg(PyenvSettings::default()));

            assert!(outcome.success, "全链应成功: {:?}", outcome.steps);
            assert_eq!(
                all_statuses(&outcome.steps),
                [
                    PyenvStepStatus::Done,
                    PyenvStepStatus::Done,
                    PyenvStepStatus::Done,
                    PyenvStepStatus::Done,
                    PyenvStepStatus::Done,
                ]
            );
            // 运行时真解压就位:可执行位保留(install_only 布局),载荷文件在
            assert!(fixture.python_path().is_file());
            assert!(fixture.data.path().join("python/lib/dummy.txt").is_file());
            {
                use std::os::unix::fs::PermissionsExt;
                let mode = fs::metadata(fixture.python_path())
                    .unwrap()
                    .permissions()
                    .mode();
                assert_ne!(mode & 0o111, 0, "python3 必须保留可执行位");
            }
            // pip 真被调起:argv 记账含锁版清单路径
            assert_eq!(fixture.pip_log_lines().len(), 1);
            assert!(fixture.pip_log_lines()[0].contains("-m pip install"));
            assert!(fixture.pip_log_lines()[0].contains(lock.to_str().unwrap()));
            // 归档缓存保留(幂等续装基础);下载恰一次
            assert!(fixture.archive_cache_path().is_file());
            assert_eq!(server.request_count(), 1);
            // 进度回调节奏:每阶段 running/done 双迁 → ≥10 次快照,末帧自检 running
            assert!(
                updates.len() >= 10,
                "进度广播应逐阶段推进: {}",
                updates.len()
            );
            assert_eq!(
                step_status(updates.last().unwrap(), PyenvPhase::Selfcheck),
                PyenvStepStatus::Running
            );
            // 终态戳形态(state/deps_fingerprint/steps)+ 第 2 步读者闭环 → ready
            let stamp: serde_json::Value = serde_json::from_str(&fixture.stamp_text()).unwrap();
            assert_eq!(stamp["state"], "ready");
            assert_eq!(
                stamp["deps_fingerprint"].as_str().map(String::from),
                pyenv::lock_fingerprint(&lock)
            );
            assert_eq!(stamp["steps"].as_array().unwrap().len(), 5);
            for step in stamp["steps"].as_array().unwrap() {
                let mut keys: Vec<&str> = step
                    .as_object()
                    .unwrap()
                    .keys()
                    .map(String::as_str)
                    .collect();
                keys.sort_unstable();
                assert_eq!(keys, ["error", "phase", "status"]);
            }
            let detection = pyenv::detect(fixture.data.path(), Some(&lock), None);
            assert_eq!(detection.state, PyenvState::Ready);
        }

        /// 幂等重跑(AC4):已完成步全部 skipped,无重复下载/pip,结果一致。
        #[test]
        fn second_run_skips_completed_steps() {
            let fixture = fixture(ServeMode::Ok);
            fixture.write_lock("apprise==1.8.0\n");
            let server = start_test_server(ServerBehavior::Serve(fixture.archive_bytes.clone()));
            fixture.write_manifest(&server.url("/runtime.tar.gz"), &fixture.archive_sha256);
            let cfg = fixture.cfg(PyenvSettings::default());
            assert!(run_chain(&cfg, &|_| {}).success);

            let (outcome, _) = run_with_recording(&cfg);
            assert!(outcome.success);
            assert_eq!(
                all_statuses(&outcome.steps),
                [
                    PyenvStepStatus::Skipped,
                    PyenvStepStatus::Skipped,
                    PyenvStepStatus::Skipped,
                    PyenvStepStatus::Skipped,
                    PyenvStepStatus::Done, // 自检恒重跑(终门重验)
                ]
            );
            assert_eq!(server.request_count(), 1, "第二次不应再下载");
            assert_eq!(fixture.pip_log_lines().len(), 1, "第二次不应再跑 pip");
            assert_eq!(
                serde_json::from_str::<serde_json::Value>(&fixture.stamp_text()).unwrap()["state"],
                "ready"
            );
        }

        /// 坏包:manifest 钉值与实收内容不符 → checksum_mismatch;坏归档即删,
        /// 重试必重下。
        #[test]
        fn checksum_mismatch_classified_and_archive_discarded() {
            let fixture = fixture(ServeMode::Ok);
            fixture.write_lock("apprise==1.8.0\n");
            let server = start_test_server(ServerBehavior::Serve(fixture.archive_bytes.clone()));
            // manifest 钉的是「另一份内容」的 sha256 → 必失配
            let wrong_sha = sha256_hex(b"not-the-real-archive");
            fixture.write_manifest(&server.url("/runtime.tar.gz"), &wrong_sha);
            let (outcome, _) = run_with_recording(&fixture.cfg(PyenvSettings::default()));

            assert!(!outcome.success);
            assert_eq!(
                step_status(&outcome.steps, PyenvPhase::Downloading),
                PyenvStepStatus::Done
            );
            assert_eq!(
                step_status(&outcome.steps, PyenvPhase::Verifying),
                PyenvStepStatus::Failed
            );
            assert!(step_error(&outcome.steps, PyenvPhase::Verifying)
                .starts_with("checksum_mismatch: "));
            assert!(
                !fixture.archive_cache_path().exists(),
                "坏包必须删除(重试必重下)"
            );
            let stamp: serde_json::Value = serde_json::from_str(&fixture.stamp_text()).unwrap();
            assert_eq!(stamp["state"], "error");
        }

        /// 断网(连接即断)→ network_failed;终态 error 可重试。
        #[test]
        fn network_failure_classified_when_server_drops() {
            let fixture = fixture(ServeMode::Ok);
            fixture.write_lock("apprise==1.8.0\n");
            let server = start_test_server(ServerBehavior::Drop);
            fixture.write_manifest(&server.url("/runtime.tar.gz"), &fixture.archive_sha256);
            let (outcome, _) = run_with_recording(&fixture.cfg(PyenvSettings::default()));

            assert!(!outcome.success);
            assert_eq!(
                step_status(&outcome.steps, PyenvPhase::Downloading),
                PyenvStepStatus::Failed
            );
            assert!(
                step_error(&outcome.steps, PyenvPhase::Downloading).starts_with("network_failed: ")
            );
            let stamp: serde_json::Value = serde_json::from_str(&fixture.stamp_text()).unwrap();
            assert_eq!(stamp["state"], "error");
            assert!(!fixture.python_path().exists());
            assert_eq!(server.request_count(), 1, "确实发起过一次下载");
        }

        /// 源 404(镜像 URL 配错/文件下架)→ 同归 network_failed 可重试。
        #[test]
        fn http_404_classified_as_network_failure() {
            let fixture = fixture(ServeMode::Ok);
            fixture.write_lock("apprise==1.8.0\n");
            let server = start_test_server(ServerBehavior::NotFound);
            fixture.write_manifest(&server.url("/runtime.tar.gz"), &fixture.archive_sha256);
            let (outcome, _) = run_with_recording(&fixture.cfg(PyenvSettings::default()));

            assert!(!outcome.success);
            assert!(
                step_error(&outcome.steps, PyenvPhase::Downloading).starts_with("network_failed: "),
                "404 应带状态码明细: {}",
                step_error(&outcome.steps, PyenvPhase::Downloading)
            );
            assert!(
                step_error(&outcome.steps, PyenvPhase::Downloading).contains("404"),
                "明细应含状态码便于排查源配置"
            );
            assert_eq!(
                serde_json::from_str::<serde_json::Value>(&fixture.stamp_text()).unwrap()["state"],
                "error"
            );
        }

        /// 断网失败后换镜像重试 → 成功(AC1「断网/坏包中途失败可重试续装」)。
        #[test]
        fn network_failure_then_mirror_retry_succeeds() {
            let fixture = fixture(ServeMode::Ok);
            fixture.write_lock("apprise==1.8.0\n");
            let dead = start_test_server(ServerBehavior::Drop);
            fixture.write_manifest(&dead.url("/runtime.tar.gz"), &fixture.archive_sha256);
            let first = run_chain(&fixture.cfg(PyenvSettings::default()), &|_| {});
            assert!(!first.success);

            // 换镜像(整串 URL 替换;D3)重跑 → 全链成功
            let good = start_test_server(ServerBehavior::Serve(fixture.archive_bytes.clone()));
            let settings = PyenvSettings {
                mirror_runtime: Some(good.url("/mirror/runtime.tar.gz")),
                mirror_pypi: None,
            };
            let (outcome, _) = run_with_recording(&fixture.cfg(settings));
            assert!(outcome.success, "镜像重试应成功: {:?}", outcome.steps);
            assert_eq!(good.request_count(), 1);
            assert_eq!(
                serde_json::from_str::<serde_json::Value>(&fixture.stamp_text()).unwrap()["state"],
                "ready"
            );
        }

        /// 镜像覆盖只换 URL 不绕校验(D3):镜像源内容与 manifest 钉值不符照样
        /// checksum_mismatch。
        #[test]
        fn mirror_cannot_bypass_checksum() {
            let fixture = fixture(ServeMode::Ok);
            fixture.write_lock("apprise==1.8.0\n");
            let _default = start_test_server(ServerBehavior::Drop);
            // manifest 用默认 URL(已死)+ 钉好包 sha256;镜像给坏内容
            fixture.write_manifest(&_default.url("/runtime.tar.gz"), &fixture.archive_sha256);
            let corrupt =
                start_test_server(ServerBehavior::Serve(b"corrupted-not-a-tarball".to_vec()));
            let settings = PyenvSettings {
                mirror_runtime: Some(corrupt.url("/mirror/runtime.tar.gz")),
                mirror_pypi: None,
            };
            let (outcome, _) = run_with_recording(&fixture.cfg(settings));
            assert!(!outcome.success);
            assert_eq!(
                step_status(&outcome.steps, PyenvPhase::Verifying),
                PyenvStepStatus::Failed
            );
            assert!(step_error(&outcome.steps, PyenvPhase::Verifying)
                .starts_with("checksum_mismatch: "));
            assert_eq!(corrupt.request_count(), 1, "下载确实走了镜像 URL");
        }

        /// 中断续装(AC1「幂等续装」):崩溃在 verify 后/extract 前
        /// (非终态戳 + 归档在 + python 未解压)→ 重跑免重下,直落 extract。
        #[test]
        fn interrupted_install_resumes_without_redownload() {
            let fixture = fixture(ServeMode::Ok);
            fixture.write_lock("apprise==1.8.0\n");
            let server = start_test_server(ServerBehavior::Serve(fixture.archive_bytes.clone()));
            fixture.write_manifest(&server.url("/runtime.tar.gz"), &fixture.archive_sha256);
            let cfg = fixture.cfg(PyenvSettings::default());
            assert!(run_chain(&cfg, &|_| {}).success);

            // 模拟中断:清掉 python 与 pip 记账,戳回退到「verify 完、extract 前」
            fs::remove_dir_all(fixture.data.path().join("python")).unwrap();
            fs::remove_file(&fixture.pip_log).unwrap();
            let mid_run = serde_json::json!({
                "state": null,
                "deps_fingerprint": null,
                "steps": [
                    {"phase": "downloading", "status": "done", "error": null},
                    {"phase": "verifying", "status": "done", "error": null},
                ]
            });
            fs::write(
                pyenv::env_stamp_path(fixture.data.path()),
                mid_run.to_string(),
            )
            .unwrap();

            let (outcome, _) = run_with_recording(&cfg);
            assert!(outcome.success, "续装应成功: {:?}", outcome.steps);
            assert_eq!(
                all_statuses(&outcome.steps),
                [
                    PyenvStepStatus::Skipped, // 归档在且 sha 匹配 → 免重下
                    PyenvStepStatus::Skipped,
                    PyenvStepStatus::Done, // extract 重跑(python 曾缺位)
                    PyenvStepStatus::Done, // 依赖重跑(中断戳无指纹)
                    PyenvStepStatus::Done,
                ]
            );
            assert_eq!(server.request_count(), 1, "续装绝不重下归档");
            assert_eq!(fixture.pip_log_lines().len(), 1);
            // 中断态在续装前按第 2 步语义 = error(可重试);续装后 = ready
            assert_eq!(
                serde_json::from_str::<serde_json::Value>(&fixture.stamp_text()).unwrap()["state"],
                "ready"
            );
        }

        /// 磁盘预检不足 → disk_full(挂在首个将跑阶段),零下载零解压。
        #[test]
        fn disk_precheck_blocks_with_disk_full() {
            let fixture = fixture(ServeMode::Ok);
            fixture.write_lock("apprise==1.8.0\n");
            let server = start_test_server(ServerBehavior::Serve(fixture.archive_bytes.clone()));
            fixture.write_manifest(&server.url("/runtime.tar.gz"), &fixture.archive_sha256);
            let cfg = fixture.cfg_with(PyenvSettings::default(), false, u64::MAX);
            let (outcome, _) = run_with_recording(&cfg);

            assert!(!outcome.success);
            assert_eq!(
                step_status(&outcome.steps, PyenvPhase::Downloading),
                PyenvStepStatus::Failed
            );
            assert!(step_error(&outcome.steps, PyenvPhase::Downloading).starts_with("disk_full: "));
            assert!(!fixture.archive_cache_path().exists());
            assert!(!fixture.python_path().exists());
            let stamp: serde_json::Value = serde_json::from_str(&fixture.stamp_text()).unwrap();
            assert_eq!(stamp["state"], "error");
        }

        /// pip 失败 → pip_failed(依赖段专属分类);修因重试 → 幂等续装成功。
        #[test]
        fn pip_failure_classified_and_retry_recovers() {
            let fixture = fixture(ServeMode::Ok);
            fixture.write_lock("apprise==1.8.0\n");
            let server = start_test_server(ServerBehavior::Serve(fixture.archive_bytes.clone()));
            fixture.write_manifest(&server.url("/runtime.tar.gz"), &fixture.archive_sha256);
            let cfg = fixture.cfg(PyenvSettings::default());
            fs::write(&fixture.pip_fail_marker, b"1").unwrap(); // 让桩 pip 失败

            let (first, _) = run_with_recording(&cfg);
            assert!(!first.success);
            assert_eq!(
                step_status(&first.steps, PyenvPhase::Downloading),
                PyenvStepStatus::Done
            );
            assert_eq!(
                step_status(&first.steps, PyenvPhase::Verifying),
                PyenvStepStatus::Done
            );
            assert_eq!(
                step_status(&first.steps, PyenvPhase::Extracting),
                PyenvStepStatus::Done
            );
            assert_eq!(
                step_status(&first.steps, PyenvPhase::InstallingDeps),
                PyenvStepStatus::Failed
            );
            let pip_error = step_error(&first.steps, PyenvPhase::InstallingDeps);
            assert!(pip_error.starts_with("pip_failed: "), "实际: {pip_error}");
            assert!(
                pip_error.contains("stub pip boom"),
                "pip 输出尾部应带回显: {pip_error}"
            );

            // 修因(移除失败标记)重试:运行时段全 skipped,依赖段重跑 → ready
            fs::remove_file(&fixture.pip_fail_marker).unwrap();
            let (second, _) = run_with_recording(&cfg);
            assert!(second.success, "重试应恢复: {:?}", second.steps);
            assert_eq!(
                all_statuses(&second.steps),
                [
                    PyenvStepStatus::Skipped,
                    PyenvStepStatus::Skipped,
                    PyenvStepStatus::Skipped,
                    PyenvStepStatus::Done,
                    PyenvStepStatus::Done,
                ]
            );
            assert_eq!(server.request_count(), 1);
        }

        /// 自检失败两形态:serve 即退(缺依赖/崩溃)与应答非 JSON → selfcheck_failed。
        #[test]
        fn selfcheck_failure_classified() {
            for serve in [ServeMode::Exit, ServeMode::Garbage] {
                let fixture = fixture(serve);
                fixture.write_lock("apprise==1.8.0\n");
                let server =
                    start_test_server(ServerBehavior::Serve(fixture.archive_bytes.clone()));
                fixture.write_manifest(&server.url("/runtime.tar.gz"), &fixture.archive_sha256);
                let (outcome, _) = run_with_recording(&fixture.cfg(PyenvSettings::default()));

                assert!(
                    !outcome.success,
                    "serve={serve:?} 应自检失败: {:?}",
                    outcome.steps
                );
                assert_eq!(
                    step_status(&outcome.steps, PyenvPhase::InstallingDeps),
                    PyenvStepStatus::Done
                );
                assert_eq!(
                    step_status(&outcome.steps, PyenvPhase::Selfcheck),
                    PyenvStepStatus::Failed
                );
                assert!(step_error(&outcome.steps, PyenvPhase::Selfcheck)
                    .starts_with("selfcheck_failed: "));
                let stamp: serde_json::Value = serde_json::from_str(&fixture.stamp_text()).unwrap();
                assert_eq!(stamp["state"], "error");
            }
        }

        /// PyPI 索引覆盖透传:pip argv 带 --index-url(design §5)。
        #[test]
        fn mirror_pypi_index_flag_passed_to_pip() {
            let fixture = fixture(ServeMode::Ok);
            fixture.write_lock("apprise==1.8.0\n");
            let server = start_test_server(ServerBehavior::Serve(fixture.archive_bytes.clone()));
            fixture.write_manifest(&server.url("/runtime.tar.gz"), &fixture.archive_sha256);
            let settings = PyenvSettings {
                mirror_runtime: None,
                mirror_pypi: Some("https://pypi.example/simple".into()),
            };
            let (outcome, _) = run_with_recording(&fixture.cfg(settings));
            assert!(outcome.success);
            let lines = fixture.pip_log_lines();
            assert_eq!(lines.len(), 1);
            assert!(
                lines[0].contains("--index-url https://pypi.example/simple"),
                "实际: {}",
                lines[0]
            );
        }

        /// deps_only(D4 同步依赖):运行时段 skipped;指纹一致 → pip 也 skipped;
        /// 自检重跑 → ready。
        #[test]
        fn deps_only_skips_runtime_and_satisfied_pip() {
            let fixture = fixture(ServeMode::Ok);
            fixture.write_lock("apprise==1.8.0\n");
            let server = start_test_server(ServerBehavior::Serve(fixture.archive_bytes.clone()));
            fixture.write_manifest(&server.url("/runtime.tar.gz"), &fixture.archive_sha256);
            assert!(run_chain(&fixture.cfg(PyenvSettings::default()), &|_| {}).success);
            fs::remove_file(&fixture.pip_log).unwrap(); // 清记账

            let cfg = fixture.cfg_with(PyenvSettings::default(), true, 1024 * 1024);
            let (outcome, _) = run_with_recording(&cfg);
            assert!(outcome.success);
            assert_eq!(
                all_statuses(&outcome.steps),
                [
                    PyenvStepStatus::Skipped,
                    PyenvStepStatus::Skipped,
                    PyenvStepStatus::Skipped,
                    PyenvStepStatus::Skipped, // 指纹一致 → 已装跳过(AC4)
                    PyenvStepStatus::Done,
                ]
            );
            assert!(fixture.pip_log_lines().is_empty(), "依赖已装不应再跑 pip");
            assert_eq!(server.request_count(), 1);
        }

        /// 依赖漂移(D4):锁版清单变脸后 deps_only 重跑依赖段,新指纹落戳;
        /// 旧清单视角 = deps_stale,新清单视角 = ready。
        #[test]
        fn deps_only_reruns_pip_when_lock_changed() {
            let fixture = fixture(ServeMode::Ok);
            fixture.write_lock("apprise==1.8.0\n");
            let server = start_test_server(ServerBehavior::Serve(fixture.archive_bytes.clone()));
            fixture.write_manifest(&server.url("/runtime.tar.gz"), &fixture.archive_sha256);
            assert!(run_chain(&fixture.cfg(PyenvSettings::default()), &|_| {}).success);

            // 壳更新随包清单变脸(D4 漂移);旧清单另存快照供旧视角比对
            // (write_lock 同路径覆写,旧内容须先另存)。
            let old_lock = fixture.data.path().join("old-lock-snapshot.txt");
            fs::write(&old_lock, "apprise==1.8.0\n").unwrap();
            let new_lock = fixture.write_lock("apprise==1.9.0\n");
            assert_eq!(
                pyenv::detect(fixture.data.path(), Some(&new_lock), None).state,
                PyenvState::DepsStale,
                "新清单视角应报依赖漂移"
            );

            let cfg = fixture.cfg_with(PyenvSettings::default(), true, 1024 * 1024);
            let (outcome, _) = run_with_recording(&cfg);
            assert!(outcome.success);
            assert_eq!(
                step_status(&outcome.steps, PyenvPhase::InstallingDeps),
                PyenvStepStatus::Done
            );
            assert_eq!(
                fixture.pip_log_lines().len(),
                2,
                "漂移后应重跑 pip(首轮 1 + 漂移重跑 1)"
            );
            // 终态指纹 = 新清单;两侧 detect 闭环
            assert_eq!(
                pyenv::detect(fixture.data.path(), Some(&new_lock), None).state,
                PyenvState::Ready
            );
            assert_eq!(
                pyenv::detect(fixture.data.path(), Some(&old_lock), None).state,
                PyenvState::DepsStale,
                "旧清单视角仍应报漂移(指纹以最新安装为准)"
            );
            let _ = server;
        }

        /// manifest 无本平台条目 / python_bin 与壳 spawn 布局不一致 → setup_failed。
        #[test]
        fn manifest_guards_are_setup_failures() {
            // 无本平台条目
            let case_missing_platform = fixture(ServeMode::Ok);
            case_missing_platform.write_lock("apprise==1.8.0\n");
            case_missing_platform.write_manifest_variant(serde_json::json!({
                "manifest_version": 1,
                "platforms": { "other-triple": { "url": "https://x/y.tar.gz", "sha256": "ab", "archive": "tar.gz", "extract_root_dir": "python", "python_bin": "python/bin/python3" } }
            }));
            let (outcome, _) =
                run_with_recording(&case_missing_platform.cfg(PyenvSettings::default()));
            assert!(!outcome.success);
            let error = step_error(&outcome.steps, PyenvPhase::Downloading);
            assert!(
                error.starts_with("setup_failed: ") && error.contains("无本平台条目"),
                "实际: {error}"
            );
            assert_eq!(
                serde_json::from_str::<serde_json::Value>(&case_missing_platform.stamp_text())
                    .unwrap()["state"],
                "error"
            );

            // python_bin 与壳 spawn 布局(pyenv.rs 常量)不一致
            let case_layout_drift = fixture(ServeMode::Ok);
            case_layout_drift.write_lock("apprise==1.8.0\n");
            let server = start_test_server(ServerBehavior::Serve(
                case_layout_drift.archive_bytes.clone(),
            ));
            let mut manifest = serde_json::json!({
                "manifest_version": 1,
                "platforms": { TEST_TRIPLE: {
                    "url": server.url("/runtime.tar.gz"),
                    "sha256": case_layout_drift.archive_sha256,
                    "archive": "tar.gz",
                    "extract_root_dir": "python",
                    "python_bin": "python/bin/python3",
                } }
            });
            manifest["platforms"][TEST_TRIPLE]["python_bin"] =
                serde_json::json!("python/bin/weird-python");
            case_layout_drift.write_manifest_variant(manifest);
            let (outcome, _) = run_with_recording(&case_layout_drift.cfg(PyenvSettings::default()));
            assert!(!outcome.success);
            let error = step_error(&outcome.steps, PyenvPhase::Downloading);
            assert!(
                error.starts_with("setup_failed: ") && error.contains("不一致"),
                "实际: {error}"
            );
        }
    }
}
