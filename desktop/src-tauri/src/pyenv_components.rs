//! 桌面自管 Python 环境 —— 可选组件机制(10-05-table-restore 桌面侧,prd R4 /
//! 执行清单第 2 条)。
//!
//! 自管环境立好(desktop-managed-py-env D6)后的第一件可选重件验证「组件装进
//! 自管环境、零重打包」路线:组件 = 主清单(requirements-lock.txt)之外的
//! 可选 pip 包,由设置页开关按需装进 `<数据根>/python`,壳更新不重打包。
//!
//! == 组件注册表(随包;契约 = prd R4「组件注册表条目形态:id + pip spec 钉版」)
//! - `Resources/components.json`(tauri.conf resources 映射,与 runtime-manifest
//!   同款随包):`{components: [{id, pip_spec, label, description}]}`;
//! - 首件 = table(rapid_table 3.x onnx;**组件消费者是引擎,钉版跟引擎 API
//!   走**:src/myssia/vision/table.py 按 3.x API 写(裸 `RapidTable()` /
//!   `ocr_results=` 复数 / `pred_htmls` 复数),pyproject extras 钉
//!   `rapid-table>=3.0.2,<4`——1.x 虽模型随轮但 API 代差全断(`__init__`
//!   必传 `RapidTableInput`、`ocr_result`/`pred_html` 单数;质检高危修正,
//!   故不取 1.0.3);pip_spec = 组件闭包(空格分隔多条,与 extras
//!   `myssia[table]` 三件同源:rapid-table 主件钉 ==3.0.2 +
//!   rapidocr-onnxruntime(单元格文字,引擎显式喂 ocr_results)+ tqdm
//!   (3.0.2 轮隐性 import,extras 显式补));3.x 轮不内置模型,SLANET-plus
//!   结构模型首用时从 modelscope 下载 6.8MB(SHA256 校验,table.py 落地)——
//!   「首装需联网」含模型首用下载,之后离线复用);
//! - 读取宽容:文件缺位/不可读/不可解析 → 空表(旧包/并行波次中间态,
//!   `pyenv_get_status.components` 回空数组,设置屏不渲染组件行,零行为变化)。
//!
//! == 指纹(按组件记;主链 deps_fingerprint 的同构机制)==
//! - 组件指纹 = 当前注册表条目 pip_spec 整串的 sha256 hex(与
//!   pyenv::lock_fingerprint 同格式,只是基准从「随包清单文件」换成
//!   「spec 闭包字符串」——闭包任一件变脸(壳更新改钉版)= 指纹漂移 →
//!   installed=false,设置屏引导重装);
//! - 落盘 `<数据根>/pyenv-components/<id>.json`:
//!   `{state: "ready"|"error"|null, fingerprint, error}`(state 仅终态落值,
//!   null = 安装中断;error 恒在场,无错为 null,与 steps[].error 同惯例)。
//!
//! == 安装(pyenv_install_component IPC;复用安装链依赖段)==
//! - pip 子进程 = pyenv_install::run_pip_spec(argv 同源:`--no-input`/
//!   `--disable-pip-version-check`/`--index-url` 覆盖/剥 PYTHONPATH,Req 4
//!   环境隔离),PyPI 镜像索引继承 `pyenv-settings.json`(design §5,组件
//!   不另设镜像面),磁盘预检复用同一门;
//! - **安装后浏览器钩子(10-06-native-plugin-components 轨A,design §3)**:
//!   注册表条目可选 `post_install: "playwright-chromium"`——pip 闭包装完后
//!   用同一自管 pyenv 的 playwright 拉 chromium 进
//!   `<数据根>/playwright-browsers/`(PLAYWRIGHT_BROWSERS_PATH;数据根下,
//!   卸载组件/清数据根即整目录消,不散落 OS 缓存区,G-Q6 体积披露);
//!   失败 = 组件戳 error 态可见(既有 error 卡形态),不静默;未知钩子值 =
//!   注册表与壳版本漂移,结构化拒且零子进程副作用;磁盘预检按钩子加码
//!   (PLAYWRIGHT_CHROMIUM_DISK_BYTES);运行时 sidecar spawn 经
//!   should_inject_browsers_env 注入同一 PLAYWRIGHT_BROWSERS_PATH(render
//!   链子进程继承);
//! - 护栏:未知组件 id / Python 未就位(先走「开始配置」)/ 主安装链在跑 /
//!   组件安装单飞(同刻只许一个 pip)→ 结构化拒绝;
//! - 卸载本期不做(档记后续):开关只管装与状态回读,已装件关档如实呈现。
//!
//! == 状态(pyenv_get_status 扩展;契约两键钉死)==
//! - `components: [{id, installed}]`(installed = 戳 ready 且指纹与当前注册
//!   表一致);载荷与 `pyenv-status-changed` 事件同源(pyenv::status_at 组装)。
//!
//! == 轨B 壳服务组件(10-06-native-plugin-components 阶段2,design §2/G-Q5)==
//! 注册表条目可选 `kind: "service"` + `service: {start_cmd, health_url, port, env}`
//! + 可选 `pre_start` 钩子(当前唯一值 searxng-settings:确保
//! `<数据根>/services/searxng/settings.yml` 在场,缺则生成
//! `use_default_settings: true` + `formats: [html, json]` + 随机 secret_key
//! 两行关键覆盖机器化 + 随机 secret;plugins/searxng.yaml 头注原手工步骤的
//! 壳侧接管);缺 kind = 既有库组件,老消费端零感知(宽容读取惯例)。
//!
//! 生命周期 IPC:`service_start/stop/status`(main.rs generate_handler
//! 注册);状态落 `<数据根>/pyenv-components/<id>.service.json`
//! (running/stopped/pid/started_at/last_exit——G-Q5「装好默认停 + 状态记忆」:
//! 装好不自动起,启停只走设置卡按钮,壳重启后按戳 pid 复核对账)。
//!
//! 进程托管(轨B 形状定案,2026-10-06 沙箱实测背书):
//! - spawn:自管 python + start_cmd argv + env(值支持 `{service_dir}` 占位符
//!   → `<数据根>/services/<id>` 绝对路径;searxng 侧注入
//!   `SEARXNG_SETTINGS_PATH`);剥 PYTHONPATH(Req 4);stdin null;stdout/stderr
//!   追加落 `<数据根>/services/<id>/service.log`(不灌壳自身 stderr);
//!   **新进程组**(unix process_group(0)):整组停覆盖孙进程(granian 实测
//!   master→worker-1 两级进程树,只杀 master 会留占端口的 worker 孤儿),
//!   且与壳自身会话隔离(SIGINT/SIGUP 不传播)。
//! - stop:先 SIGTERM 进程组(优雅),宽限内不死再 SIGKILL 组;本会话
//!   子进程句柄可回收退出码(unix 信号死者记 -signal 惯例);跨壳重启的
//!   孤儿(壳退出后服务继续跑=状态记忆的一部分)停前先经 ps argv 复核
//!   (python 路径 + start_cmd 首尾 token 三锚点,防 pid 复用误杀无辜进程组)。
//! - 健康:`service_status` 轮 health_url(reqwest,2s 超时;searxng 上游
//!   /healthz 是纯文本 200,零上游搜索成本);设置卡绿点消费。
//!
//! 上游现实(searxng 组件行,2026-10-06 实测钉死,pyenv_install.rs
//! run_pip_src_no_build_isolation 注释同源):searxng 真身不在 PyPI(PyPI
//! 同名包是无关 MCP 包装器)→ git 钉 commit d48c4b555(=引擎探查实例
//! 2026.10.4+d48c4b555 同 commit);上游 setup.py 构建期 import 运行时依赖,
//! 构建隔离态单发安装必败 → 一段装依赖闭包 + 二段 --no-build-isolation
//! 装源码包(post_install 钩子 pip-src-no-build-isolation);服务端 = 上游
//! 当前 master 形态 granian(granian==2.8.3,WSGI 接口,arm64 轮在场;
//! searx.webserver/waitress 已被上游移除,design §2 的 -m searx.webserver
/// 依实测改形)。

use std::collections::HashMap;
use std::path::{Path, PathBuf};
use std::sync::Mutex;
use std::time::{Duration, Instant, SystemTime, UNIX_EPOCH};

use serde::{Deserialize, Serialize};
use sha2::{Digest, Sha256};
use tauri::{AppHandle, Manager};

/// 随包组件注册表资源文件名(tauri.conf resources 映射后位于 resource_dir 下)。
pub const COMPONENTS_RESOURCE_FILE: &str = "components.json";
/// 数据根下组件指纹目录名(逐组件一文件:`pyenv-components/<id>.json`)。
const COMPONENTS_STAMP_DIR: &str = "pyenv-components";
/// post_install 钩子:装完 pip 闭包后拉 playwright chromium(轨A crawl4ai,
/// 10-06-native-plugin-components design §3)。当前唯一钩子值——注册表写下
/// 即启用;未知值 = 注册表与壳版本漂移,安装期结构化拒(见 install_component)。
pub const POST_INSTALL_PLAYWRIGHT_CHROMIUM: &str = "playwright-chromium";
/// 数据根下 playwright 浏览器目录名(PLAYWRIGHT_BROWSERS_PATH 注入值;
/// 组件浏览器只落这里不散落 OS 缓存区——卸载组件/清理数据根即整目录消,
/// G-Q6 体积披露的落点承诺)。
pub const PLAYWRIGHT_BROWSERS_DIR: &str = "playwright-browsers";
/// playwright chromium 钩子的磁盘预检加码:G-Q6「chromium 下载约 300MB 级」,
/// 落盘含 chromium + headless shell + ffmpeg 解压总量(2026-10-06 沙箱实测
/// 557MB),保守取 600MB(在基础门 DISK_REQUIRED_BYTES 之上叠加;主人磁盘
/// 敏感,重件预检宁严勿松)。
pub(crate) const PLAYWRIGHT_CHROMIUM_DISK_BYTES: u64 = 600 * 1024 * 1024;

// ---------------------------------------------------------------------------
// 轨B 壳服务组件常量(10-06-native-plugin-components 阶段2,design §2)
// ---------------------------------------------------------------------------

/// post_install 钩子:装完 pip 依赖闭包后用 `--no-build-isolation` 二段装
/// 源码包直引 spec(searxng 上游 setup.py 构建期 import 运行时依赖,见
/// pyenv_install::run_pip_src_no_build_isolation 注释;源 spec 走注册表
/// `pip_src` 字段,未知字段/缺值安装期结构化拒)。
pub const POST_INSTALL_PIP_SRC_NO_BUILD_ISOLATION: &str = "pip-src-no-build-isolation";
/// pre_start 钩子:启动前确保 services/searxng/settings.yml 在场(缺则生成
/// 随机 secret_key 版;已有文件不覆盖——secret 不轮换,删文件=显式重置)。
pub const PRE_START_SEARXNG_SETTINGS: &str = "searxng-settings";
/// 服务数据目录名(`<数据根>/services/<id>/`:settings.yml、service.log;
/// 清数据根即整目录消,G-Q6 落点承诺)。
pub const SERVICES_DIR: &str = "services";
/// 服务 env 值占位符:替换为 `<数据根>/services/<id>` 绝对路径(searxng 侧
/// `SEARXNG_SETTINGS_PATH: {service_dir}/settings.yml`——注册表保持数据根
/// 无关的相对声明,拼装在壳侧)。
pub const SERVICE_DIR_PLACEHOLDER: &str = "{service_dir}";
/// 服务条目 id(searxng 组件;pre_start 钩子与 settings 生成器的锚点)。
pub const SEARXNG_SERVICE_ID: &str = "searxng";
/// 服务启动健康等待上限:granian+flask 冷启动实测 ~1s,20s 覆盖慢盘余量
/// (到顶未绿 = running+healthy=false 如实回,不谎报失败;进程死才是启动失败)。
const SERVICE_HEALTH_WAIT: Duration = Duration::from_secs(20);
/// 健康探测单次超时(reqwest;本地实例连接拒绝是即时的,2s 只兜慢顶)。
const SERVICE_HEALTH_PROBE_TIMEOUT: Duration = Duration::from_secs(2);
/// 服务停止优雅宽限(SIGTERM 进程组后等多久才升级 SIGKILL)。
const SERVICE_STOP_GRACE: Duration = Duration::from_secs(8);
/// SIGKILL 组信号后的收尾等待上限(理论上必死;封顶防悬挂)。
const SERVICE_STOP_KILL_GRACE: Duration = Duration::from_secs(3);
/// 健康等待轮询间隔。
const SERVICE_HEALTH_POLL_INTERVAL: Duration = Duration::from_millis(300);

// ---------------------------------------------------------------------------
// 注册表(随包 components.json;宽容读取)
// ---------------------------------------------------------------------------

/// 注册表单条目(契约形态:`{id, pip_spec, label, description}`;description
/// 缺省空串,未知附加字段忽略——与 runtime-manifest 同款宽容口径)。
#[derive(Clone, PartialEq, Eq, Debug, Deserialize, Serialize)]
pub struct ComponentSpec {
    pub id: String,
    /// 钉版 pip spec(组件闭包,空格分隔多条与 pyproject extras 同源,如
    /// `rapid-table==3.0.2 rapidocr-onnxruntime>=1.3 tqdm>=4`;壳更新改钉版
    /// 即指纹漂移)。
    pub pip_spec: String,
    pub label: String,
    #[serde(default)]
    pub description: String,
    /// 安装后钩子(可选;缺省 None = 纯 pip 组件,零行为差)。当前已知值
    /// [`POST_INSTALL_PLAYWRIGHT_CHROMIUM`](轨A crawl4ai)/
    /// [`POST_INSTALL_PIP_SRC_NO_BUILD_ISOLATION`](轨B searxng 源码包
    /// 二段装,源 spec 在 `pip_src` 字段);未知值安装期结构化拒(注册表与
    /// 壳版本漂移不静默)。指纹基准 = 闭包串(pip_spec+pip_src,见
    /// [`closure_fingerprint`])——钩子属安装链行为,不进漂移判定(钩子变更
    /// 随壳更新,重装引导由闭包漂移或手动触发)。
    #[serde(default)]
    pub post_install: Option<String>,
    /// 源码包二段安装 spec(可选;与 post_install=pip-src-no-build-isolation
    /// 钩子配套——searxng 上游 setup.py 构建期 import 运行时依赖,须先装
    /// 闭包再 --no-build-isolation 装源码包,单发必败,见模块注释)。进指纹
    /// 基准(闭包任一串变脸即漂移)。
    #[serde(default)]
    pub pip_src: Option<String>,
    /// 组件形态(可选;缺省 None = 轨A 库组件既有语义,老条目/老消费端零
    /// 感知)。当前唯一值 `"service"` = 轨B 壳服务组件(须伴随 `service` 节,
    /// 动作期 [`ComponentSpec::service_spec`] 校验)。
    #[serde(default)]
    pub kind: Option<String>,
    /// 服务声明(轨B;kind="service" 时必填,service_start/stop/status 消费)。
    #[serde(default)]
    pub service: Option<ServiceSpec>,
    /// 启动前件生成钩子(可选;当前唯一值 [`PRE_START_SEARXNG_SETTINGS`]
    /// ——确保 services/searxng/settings.yml 在场,缺则生成随机 secret_key 版;
    /// 已有不覆盖,secret 不轮换)。
    #[serde(default)]
    pub pre_start: Option<String>,
}

/// 轨B 服务声明(kind:"service" 条目的 service 节;design §2)。
#[derive(Clone, PartialEq, Eq, Debug, Deserialize, Serialize)]
pub struct ServiceSpec {
    /// 启动 argv(托管 python 之后追加:壳统一拼 `python_bin + start_cmd`;
    /// searxng = `-m granian --interface wsgi --host 127.0.0.1 --port 8888
    /// searx.webapp:app`,与上游 container/entrypoint.sh exec 形同源)。
    pub start_cmd: Vec<String>,
    /// 健康探测端点(绝对 http URL;2xx = 健康。searxng 上游 /healthz 是
    /// 纯文本 200,零上游搜索成本)。
    pub health_url: String,
    /// 监听端口(披露/UI 展示用;实际 bind 由 start_cmd 决定,声明与 argv
    /// 的一致性由仓测 components.json 契约测试把守)。
    pub port: u16,
    /// 子进程 env(值支持 [`SERVICE_DIR_PLACEHOLDER`] 占位符 → 服务数据目录
    /// 绝对路径;searxng 侧 SEARXNG_SETTINGS_PATH 指向生成的 settings.yml)。
    #[serde(default)]
    pub env: std::collections::BTreeMap<String, String>,
}

impl ComponentSpec {
    /// 是否轨B 服务组件(kind="service";注册表序/状态组装消费)。
    pub fn is_service(&self) -> bool {
        self.kind.as_deref() == Some("service")
    }

    /// 轨B 服务声明校验(未知 kind / kind 与 service 节不一致 → 结构化拒;
    /// 消费面 = service_start/stop/status 与安装链服务条目校验)。
    pub fn service_spec(&self) -> Result<&ServiceSpec, String> {
        match (self.kind.as_deref(), self.service.as_ref()) {
            (Some("service"), Some(service)) => Ok(service),
            (Some("service"), None) => Err(format!(
                "组件 {} 声明 kind=service 但缺 service 节(start_cmd/health_url/port)",
                self.id
            )),
            (Some(other), _) => Err(format!(
                "未知组件 kind: {other}(壳已知值: [service];注册表与壳版本漂移,结构化拒)"
            )),
            (None, Some(_)) => Err(format!(
                "组件 {} 携带 service 节但未声明 kind=service(注册表形态漂移)",
                self.id
            )),
            (None, None) => Err(format!(
                "组件 {} 不是服务组件(kind 缺省 = 轨A 库组件;启停/状态只接受 kind=service 条目)",
                self.id
            )),
        }
    }
}

/// 注册表文档(`{components: [...]}`;components 缺省空表)。
#[derive(Default, Deserialize)]
struct ComponentRegistryFile {
    #[serde(default)]
    components: Vec<ComponentSpec>,
}

/// 注册表路径(resource_dir 下随包 components.json)。
pub fn components_registry_path(resource_dir: &Path) -> PathBuf {
    resource_dir.join(COMPONENTS_RESOURCE_FILE)
}

/// 读随包注册表;缺位/不可读/不可解析 → 空表(设置屏零行为变化,见模块注释);
/// id/pip_spec 空串的条目剔除(防半截条目进指纹/安装面)。
pub fn load_registry(resource_dir: Option<&Path>) -> Vec<ComponentSpec> {
    let Some(dir) = resource_dir else {
        return Vec::new();
    };
    let Ok(text) = std::fs::read_to_string(components_registry_path(dir)) else {
        return Vec::new();
    };
    let Ok(registry) = serde_json::from_str::<ComponentRegistryFile>(&text) else {
        return Vec::new();
    };
    registry
        .components
        .into_iter()
        .filter(|spec| !spec.id.is_empty() && !spec.pip_spec.is_empty())
        .collect()
}

// ---------------------------------------------------------------------------
// 指纹与逐组件落盘戳
// ---------------------------------------------------------------------------

/// 组件指纹 = pip_spec 的 sha256 hex(小写;与主链 deps_fingerprint 同格式,
/// 基准换为单条 spec 字符串)。
pub fn spec_fingerprint(pip_spec: &str) -> String {
    let digest = Sha256::digest(pip_spec.as_bytes());
    digest.iter().map(|byte| format!("{byte:02x}")).collect()
}

/// 组件闭包指纹 = sha256(pip_spec [+ "\0" + pip_src])(轨B searxng 闭包两段
/// 装后漂移基准;**旧条目 pip_src 缺省时与 [`spec_fingerprint`] 恒等值**——
/// 老戳零迁移,既有组件 installed 判定不变)。
pub fn closure_fingerprint(spec: &ComponentSpec) -> String {
    match spec.pip_src.as_deref() {
        Some(src) if !src.trim().is_empty() => {
            let basis = format!("{}\0{}", spec.pip_spec, src);
            let digest = Sha256::digest(basis.as_bytes());
            digest.iter().map(|byte| format!("{byte:02x}")).collect()
        }
        _ => spec_fingerprint(&spec.pip_spec),
    }
}

/// 组件安装戳(`<数据根>/pyenv-components/<id>.json`;壳写,状态组装读)。
/// state 仅终态落 ready|error(null = 安装中断,可重试);fingerprint 只在
/// 安装成功后落值(与主链「指纹只在依赖步完成后落盘」同口径,不误判半装)。
#[derive(Default, Clone, PartialEq, Eq, Debug, Deserialize, Serialize)]
pub struct ComponentStamp {
    #[serde(default)]
    pub state: Option<String>,
    #[serde(default)]
    pub fingerprint: Option<String>,
    /// error 恒在场,无错为 null(与 steps[].error 同惯例)。
    #[serde(default)]
    pub error: Option<String>,
}

/// 组件 id 防御性校验(单一路径段):id 只与注册表对上才会进安装,但戳路径
/// 拼装仍独立校验一道,防未来注册表形态放宽时路径逃逸。
fn safe_component_id(id: &str) -> bool {
    !id.is_empty() && id != "." && id != ".." && Path::new(id).components().count() == 1
}

/// 逐组件戳路径:`<数据根>/pyenv-components/<id>.json`。
pub fn component_stamp_path(data_root: &Path, id: &str) -> PathBuf {
    data_root
        .join(COMPONENTS_STAMP_DIR)
        .join(format!("{id}.json"))
}

/// 读组件戳;不可读/不可解析/非法 id → None(等价未装,坏行不拦状态展示)。
pub fn read_component_stamp(data_root: &Path, id: &str) -> Option<ComponentStamp> {
    if !safe_component_id(id) {
        return None;
    }
    let text = std::fs::read_to_string(component_stamp_path(data_root, id)).ok()?;
    serde_json::from_str(&text).ok()
}

/// 写组件戳(临时文件 + 同目录 rename 原子写;与主链 write_stamp 同款)。
fn write_component_stamp(data_root: &Path, id: &str, stamp: &ComponentStamp) {
    if !safe_component_id(id) {
        return; // 防御:非法 id 不落盘(调用面 id 恒出自注册表,此为兜底)
    }
    let dir = data_root.join(COMPONENTS_STAMP_DIR);
    if std::fs::create_dir_all(&dir).is_err() {
        return;
    }
    let Ok(text) = serde_json::to_string_pretty(stamp) else {
        return;
    };
    let tmp = dir.join(format!(".{id}.json.tmp"));
    if std::fs::write(&tmp, text)
        .and_then(|()| std::fs::rename(&tmp, component_stamp_path(data_root, id)))
        .is_err()
    {
        eprintln!("desktop: 组件 {id} 指纹戳写入失败(不影响安装结果回包)");
    }
}

/// 组件已装判定:戳 ready 且指纹与当前注册表闭包(pip_spec+pip_src)一致
/// (漂移 = 未装,设置屏引导重装;Python 缺位由整体状态 not_configured/error
/// 另行呈现)。
pub fn is_component_installed(data_root: &Path, spec: &ComponentSpec) -> bool {
    let Some(stamp) = read_component_stamp(data_root, &spec.id) else {
        return false;
    };
    stamp.state.as_deref() == Some("ready")
        && stamp.fingerprint.as_deref() == Some(closure_fingerprint(spec).as_str())
}

// ---------------------------------------------------------------------------
// playwright 浏览器目录(轨A crawl4ai 组件;安装钩子与运行时注入共用)
// ---------------------------------------------------------------------------

/// 数据根浏览器目录绝对路径:`<数据根>/playwright-browsers/`。
/// 安装钩子(PLAYWRIGHT_BROWSERS_PATH 注入 playwright install)与 sidecar
/// spawn 运行时注入(main.rs)同源取此——装与用必须指向同一目录。
pub fn playwright_browsers_path(data_root: &Path) -> PathBuf {
    data_root.join(PLAYWRIGHT_BROWSERS_DIR)
}

/// sidecar spawn 时是否注入 `PLAYWRIGHT_BROWSERS_PATH`:目录在(组件装过
/// 浏览器)才注;缺位不注——playwright 回落自家缺省位置,未装组件的存量
/// 零行为差(含 uvx 自管型 stealth_browser:不夺其浏览器发现面)。调用侧
/// 仍遵守「已设原样继承不夺权」惯例(MYIA_HOME 同款,见 main.rs spawn_sidecar)。
pub fn should_inject_browsers_env(data_root: &Path) -> bool {
    playwright_browsers_path(data_root).is_dir()
}

/// 组件安装磁盘预算:基础门 + 钩子加码(已知钩子才加;未知值不加——它在
/// install_component 里先于预检被结构化拒,到不了这里)。
fn disk_budget(base: u64, hook: Option<&str>) -> u64 {
    if hook == Some(POST_INSTALL_PLAYWRIGHT_CHROMIUM) {
        base.saturating_add(PLAYWRIGHT_CHROMIUM_DISK_BYTES)
    } else {
        base
    }
}

// ---------------------------------------------------------------------------
// 状态组装(pyenv_get_status 扩展;两键契约)
// ---------------------------------------------------------------------------

// ---------------------------------------------------------------------------
// 轨B 壳服务组件(阶段2;design §2/G-Q5:手动启停 + 状态记忆,不隐式拉起)
// ---------------------------------------------------------------------------

/// 服务运行戳(`<数据根>/pyenv-components/<id>.service.json`;壳写,
/// service_start/stop/status 与设置卡健康点共读)。
///
/// state 仅 "running"|"stopped"(None/坏文件 = 从未写过 → 按 stopped 处理);
/// running 带 pid/started_at(unix epoch 秒);stopped 记 last_exit——本会话
/// spawn 的子进程才有 waitpid 可及(退出码/信号死者记 -signal),跨壳重启的
/// 孤儿死亡无法观测,last_exit 保持上次已知值(如实,不臆造)。
#[derive(Default, Clone, PartialEq, Eq, Debug, Deserialize, Serialize)]
pub struct ServiceStamp {
    #[serde(default)]
    pub state: Option<String>,
    #[serde(default)]
    pub pid: Option<u32>,
    #[serde(default)]
    pub started_at: Option<u64>,
    #[serde(default)]
    pub last_exit: Option<i32>,
}

/// `service_status`(及 start/stop 回包)载荷:状态机 running/stopped +
/// 健康点(health_url 2xx;仅 running 态可能为 true)+ 观测面。
#[derive(Clone, PartialEq, Eq, Debug, Serialize)]
pub struct ServiceStatus {
    pub id: String,
    /// "running" | "stopped"
    pub state: String,
    /// 健康点(health_url 2xx;stopped 恒 false;running 未绿 = 如实 false,
    /// 不谎报——慢启动/实例内部故障均如实呈现)。
    pub healthy: bool,
    pub pid: Option<u32>,
    pub started_at: Option<u64>,
    pub last_exit: Option<i32>,
}

/// 服务状态戳路径:`<数据根>/pyenv-components/<id>.service.json`(与组件
/// 指纹戳同目录,后缀区分;safe_component_id 同一道防路径逃逸)。
pub fn service_stamp_path(data_root: &Path, id: &str) -> PathBuf {
    data_root
        .join(COMPONENTS_STAMP_DIR)
        .join(format!("{id}.service.json"))
}

/// 服务数据目录:`<数据根>/services/<id>/`(settings.yml、service.log;
/// 清数据根即整目录消,G-Q6 落点)。
pub fn service_dir(data_root: &Path, id: &str) -> PathBuf {
    data_root.join(SERVICES_DIR).join(id)
}

/// 读服务状态戳;不可读/不可解析/非法 id → None(等价从未运行,坏行不拦启停)。
pub fn read_service_stamp(data_root: &Path, id: &str) -> Option<ServiceStamp> {
    if !safe_component_id(id) {
        return None;
    }
    let text = std::fs::read_to_string(service_stamp_path(data_root, id)).ok()?;
    serde_json::from_str(&text).ok()
}

/// 写服务状态戳(临时文件 + 同目录 rename 原子写;与组件指纹戳同款)。
fn write_service_stamp(data_root: &Path, id: &str, stamp: &ServiceStamp) {
    if !safe_component_id(id) {
        return; // 防御:非法 id 不落盘(调用面 id 恒出自注册表,此为兜底)
    }
    let dir = data_root.join(COMPONENTS_STAMP_DIR);
    if std::fs::create_dir_all(&dir).is_err() {
        return;
    }
    let Ok(text) = serde_json::to_string_pretty(stamp) else {
        return;
    };
    let tmp = dir.join(format!(".{id}.service.json.tmp"));
    if std::fs::write(&tmp, text)
        .and_then(|()| std::fs::rename(&tmp, service_stamp_path(data_root, id)))
        .is_err()
    {
        eprintln!("desktop: 服务组件 {id} 状态戳写入失败(不影响启停结果回包)");
    }
}

// —— settings.yml 生成器(searxng 两行关键覆盖机器化;design §2)——

/// 随机 secret_key(64 位 hex):unix 走 /dev/urandom(CSPRNG),Windows/
/// urandom 不可及回退 RandomState OS 种子 ×4 拼 256 bit 再 sha256——均 std
/// 内,零新依赖;searxng 拒绝缺省 ultrasecretkey 起服务,强随机是硬要求。
pub fn random_secret_key() -> String {
    let mut bytes = [0u8; 32];
    let filled = std::fs::File::open("/dev/urandom")
        .and_then(|mut file| std::io::Read::read_exact(&mut file, &mut bytes))
        .is_ok();
    if !filled {
        use std::hash::{BuildHasher, Hasher, RandomState};
        let mut seed = Vec::with_capacity(32);
        for _ in 0..4 {
            let hash = RandomState::new().build_hasher().finish();
            seed.extend_from_slice(&hash.to_le_bytes());
        }
        bytes.copy_from_slice(&seed);
    }
    let digest = Sha256::digest(&bytes);
    digest.iter().map(|byte| format!("{byte:02x}")).collect()
}

/// 生成 searxng settings.yml 内容(纯函数,单测主战场):
/// `use_default_settings: true`(其余全取上游包内默认 settings.yml)+
/// `search.formats: [html, json]`(json format 默认不开,开它是 MYIA 引擎
/// 消费的硬前提——403 专项文案的根因位)+ 随机 `server.secret_key`
/// (plugins/searxng.yaml 头注两行关键覆盖 + ultrasecretkey 替换的机器化)。
pub fn searxng_settings_yaml(secret_key: &str) -> String {
    format!(
        "# MYIA 壳服务组件生成(SearXNG;10-06-native-plugin-components 轨B/G-Q5)\n\
         # 覆盖面最小化:use_default_settings + formats json 两行关键覆盖 + 随机 secret_key\n\
         # 其余取上游包内默认 settings.yml;删本文件 → 下次启动按新 secret 重生成\n\
         use_default_settings: true\n\
         server:\n\
         \x20 secret_key: \"{secret_key}\"\n\
         search:\n\
         \x20 formats:\n\
         \x20   - html\n\
         \x20   - json\n"
    )
}

/// 确保 services/searxng/settings.yml 在场(缺则生成;已有文件不覆盖——
/// secret 不轮换,显式删文件 = 显式重置;幂等)。原子写(临时文件+rename)。
pub fn ensure_searxng_settings(data_root: &Path) -> std::io::Result<PathBuf> {
    let dir = service_dir(data_root, SEARXNG_SERVICE_ID);
    std::fs::create_dir_all(&dir)?;
    let path = dir.join("settings.yml");
    if path.exists() {
        return Ok(path);
    }
    let tmp = dir.join(".settings.yml.tmp");
    std::fs::write(&tmp, searxng_settings_yaml(&random_secret_key()))?;
    std::fs::rename(&tmp, &path)?;
    Ok(path)
}

// —— 服务子进程 spawn/停/探活(unix 组信号 + windows taskkill 树杀)——

/// 服务 env 值占位符解析:`{service_dir}` → 服务数据目录绝对路径(注册表
/// 声明保持数据根无关,拼装在壳侧;单 token 精确替换)。
pub fn resolve_service_env_value(value: &str, service_dir: &Path) -> String {
    value.replace(SERVICE_DIR_PLACEHOLDER, &service_dir.to_string_lossy())
}

/// 拉起服务子进程:自管 python + start_cmd;env(占位符已解析)+ 剥
/// PYTHONPATH(Req 4,与安装链 pip 同款纪律——服务只见自管环境
/// site-packages,不见壳进程可能继承的开发 PYTHONPATH);stdin null;
/// stdout/stderr 追加落服务数据目录 service.log;unix 新进程组(整组停
/// 覆盖 granian master→worker 孙进程树 + 与壳会话隔离)。
pub(crate) fn spawn_service_process(
    python_bin: &Path,
    svc: &ServiceSpec,
    service_dir: &Path,
    log_path: &Path,
) -> std::io::Result<std::process::Child> {
    use std::process::{Command, Stdio};
    let mut command = Command::new(python_bin);
    command.args(&svc.start_cmd);
    for (key, value) in &svc.env {
        command.env(key, resolve_service_env_value(value, service_dir));
    }
    command.env_remove("PYTHONPATH");
    command.stdin(Stdio::null());
    let log = std::fs::OpenOptions::new()
        .create(true)
        .append(true)
        .open(log_path)?;
    let log_stderr = log.try_clone()?;
    command.stdout(Stdio::from(log)).stderr(Stdio::from(log_stderr));
    #[cfg(unix)]
    {
        use std::os::unix::process::CommandExt;
        command.process_group(0);
    }
    command.spawn()
}

/// 探活服务 pid(kill(pid,0) 探测;非本会话子进程同样可及)。
#[cfg(unix)]
fn service_pid_alive(pid: u32) -> bool {
    // EPERM = 进程在但非同用户(本地桌面场景几乎不发生,按在处理);ESRCH
    // 才是确凿不在。
    unsafe {
        if libc::kill(pid as libc::pid_t, 0) == 0 {
            return true;
        }
        !matches!(
            std::io::Error::last_os_error().raw_os_error(),
            Some(libc::ESRCH)
        )
    }
}

/// Windows 探活(tasklist 按 PID 过滤;无 libc 依赖面)。
#[cfg(windows)]
fn service_pid_alive(pid: u32) -> bool {
    let Ok(output) = std::process::Command::new("tasklist")
        .args(["/FI", &format!("PID eq {pid}"), "/FO", "CSV", "/NH"])
        .output()
    else {
        return false;
    };
    String::from_utf8_lossy(&output.stdout).contains(&format!("\"{pid}\""))
}

/// 优雅停:SIGTERM 进程组 + 直接 pid 兜底(unix;windows 走 taskkill /T
/// 树杀)。记录 pid 理应恒为组长(spawn_service_process 恒 process_group(0)
/// ⇒ pgid == pid,组信号即全树);直接 pid 信号兜异常态(组长位让出/极端
/// 环境),对组长幂等无害——同进程两路可达。
#[cfg(unix)]
fn terminate_service(pid: u32) {
    unsafe {
        libc::kill(-(pid as libc::pid_t), libc::SIGTERM);
        libc::kill(pid as libc::pid_t, libc::SIGTERM);
    }
}

/// 强杀兜底:SIGKILL 进程组 + 直接 pid 兜底(同 terminate_service 双路)。
#[cfg(unix)]
fn force_kill_service(pid: u32) {
    unsafe {
        libc::kill(-(pid as libc::pid_t), libc::SIGKILL);
        libc::kill(pid as libc::pid_t, libc::SIGKILL);
    }
}

/// windows:树杀(优雅/强杀无区分;桌面服务组件可接受的简化,注释如实)。
#[cfg(windows)]
fn terminate_service(pid: u32) {
    let _ = std::process::Command::new("taskkill")
        .args(["/PID", &pid.to_string(), "/T", "/F"])
        .output();
}

#[cfg(windows)]
fn force_kill_service(pid: u32) {
    terminate_service(pid)
}

#[cfg(unix)]
fn service_group_alive(pid: u32) -> bool {
    // process_group(0) ⇒ pgid == pid;kill(-pgid, 0) = 组内还有任一存活进程即成功
    unsafe {
        if libc::kill(-(pid as libc::pid_t), 0) == 0 {
            return true;
        }
        !matches!(
            std::io::Error::last_os_error().raw_os_error(),
            Some(libc::ESRCH)
        )
    }
}

#[cfg(windows)]
fn service_group_alive(pid: u32) -> bool {
    service_pid_alive(pid)
}

/// 孤儿服务进程身份复核(防 pid 复用误杀无辜进程组):`ps -p <pid> -o
/// command=` 的 argv 必须同时含自管 python 绝对路径与 start_cmd 首尾 token
/// (三锚点侧写;本会话 spawn 的子进程不走此复核——Child 句柄即身份证明)。
/// 复核不过 = 状态戳的 pid 已被系统复用,不动它(戳如实转 stopped)。
pub fn pid_command_matches_service(
    pid: u32,
    python_bin: &Path,
    start_cmd: &[String],
) -> bool {
    let Some((head, tail)) = start_cmd.first().zip(start_cmd.last()) else {
        return false;
    };
    let Ok(output) = std::process::Command::new("ps")
        .args(["-p", &pid.to_string(), "-o", "command="])
        .output()
    else {
        return false;
    };
    if !output.status.success() {
        return false;
    }
    let command = String::from_utf8_lossy(&output.stdout).trim().to_string();
    if command.is_empty() {
        return false;
    }
    command.contains(python_bin.to_string_lossy().as_ref())
        && command.contains(head.as_str())
        && command.contains(tail.as_str())
}

/// 健康探测(health_url 2xx = 健康;reqwest 阻塞栈复用既有依赖,连接拒绝
/// 即时失败;rustls provider 兜底与下载链同源)。任何非 2xx(含 404/5xx)
/// 都算不健康——上游 /healthz 是纯文本 200,别的形态就是实例不对劲。
pub fn probe_health_url(url: &str) -> bool {
    crate::pyenv_install::install_ring_provider_if_missing();
    let Ok(client) = reqwest::blocking::Client::builder()
        .timeout(SERVICE_HEALTH_PROBE_TIMEOUT)
        .build()
    else {
        return false;
    };
    matches!(client.get(url).send(), Ok(resp) if resp.status().is_success())
}

/// 退出码归一(unix 信号死者记 -signal 惯例;waitpid 只对亲生可及)。
fn exit_code_of(exit: &std::process::ExitStatus) -> Option<i32> {
    if let Some(code) = exit.code() {
        return Some(code);
    }
    #[cfg(unix)]
    {
        use std::os::unix::process::ExitStatusExt;
        return exit.signal().map(|sig| -sig);
    }
    #[cfg(windows)]
    {
        None
    }
}

fn unix_epoch_secs() -> u64 {
    SystemTime::now()
        .duration_since(UNIX_EPOCH)
        .map(|d| d.as_secs())
        .unwrap_or(0)
}

/// 服务启动核心(纯逻辑,无 AppHandle;IPC 与装机态冒烟共用):
/// 契约校验(service 节/pre_start 钩子已知值,先于一切子进程)→ pre_start
/// 件生成(searxng settings.yml)→ spawn(新进程组,env 注入,日志落数据根)
/// → 状态戳 running → 有界健康等待:进程死 = Err(退出码 + 日志路径);
/// 到顶未绿 = Ok(running + healthy=false 如实回,不谎报)。
///
/// 成功回 `(状态, 子进程句柄)`——调用方(ServiceManager/冒烟)负责持有
/// (本会话内可回收退出码);句柄 drop 不杀进程(状态记忆跨壳重启的一部分)。
pub(crate) fn start_service_process(
    data_root: &Path,
    python_bin: &Path,
    spec: &ComponentSpec,
) -> Result<(ServiceStatus, std::process::Child), String> {
    let svc = spec.service_spec()?;
    if let Some(hook) = spec.pre_start.as_deref() {
        if hook != PRE_START_SEARXNG_SETTINGS {
            return Err(format!(
                "未知 pre_start 钩子: {hook}(注册表与壳版本漂移;壳已知值: \
                 [{PRE_START_SEARXNG_SETTINGS}])"
            ));
        }
        ensure_searxng_settings(data_root)
            .map_err(|e| format!("searxng settings.yml 生成失败: {e}"))?;
    }
    let dir = service_dir(data_root, &spec.id);
    std::fs::create_dir_all(&dir)
        .map_err(|e| format!("服务数据目录不可建({}): {e}", dir.display()))?;
    let log_path = dir.join("service.log");
    let started_at = unix_epoch_secs();
    let mut child = spawn_service_process(python_bin, svc, &dir, &log_path)
        .map_err(|e| format!("服务进程拉起失败({}): {e}", python_bin.display()))?;
    let pid = child.id();
    let prior_exit = read_service_stamp(data_root, &spec.id).and_then(|s| s.last_exit);
    write_service_stamp(
        data_root,
        &spec.id,
        &ServiceStamp {
            state: Some("running".into()),
            pid: Some(pid),
            started_at: Some(started_at),
            last_exit: prior_exit,
        },
    );
    eprintln!(
        "desktop: 服务组件 {} 已拉起(pid={pid},日志 {};健康端点 {})",
        spec.id,
        log_path.display(),
        svc.health_url
    );
    let deadline = Instant::now() + SERVICE_HEALTH_WAIT;
    loop {
        match child.try_wait() {
            Ok(Some(exit)) => {
                let code = exit_code_of(&exit);
                write_service_stamp(
                    data_root,
                    &spec.id,
                    &ServiceStamp {
                        state: Some("stopped".into()),
                        pid: None,
                        started_at: None,
                        last_exit: code,
                    },
                );
                return Err(format!(
                    "服务进程启动后即退出(退出码 {code:?};日志尾部见 {})",
                    log_path.display()
                ));
            }
            Ok(None) => {}
            Err(err) => {
                return Err(format!(
                    "服务进程状态回收失败: {err}(日志 {})",
                    log_path.display()
                ));
            }
        }
        if probe_health_url(&svc.health_url) {
            // 两相验证:健康端点 200 之后复核进程仍在(健康 200 + 进程健在
            // 才算 healthy=true——窄化「探到 200 的同一瞬进程崩了」的谎报窗)
            match child.try_wait() {
                Ok(None) => {}
                Ok(Some(exit)) => {
                    let code = exit_code_of(&exit);
                    write_service_stamp(
                        data_root,
                        &spec.id,
                        &ServiceStamp {
                            state: Some("stopped".into()),
                            pid: None,
                            started_at: None,
                            last_exit: code,
                        },
                    );
                    return Err(format!(
                        "服务进程启动后即退出(退出码 {code:?};日志尾部见 {})",
                        log_path.display()
                    ));
                }
                Err(err) => {
                    return Err(format!(
                        "服务进程状态回收失败: {err}(日志 {})",
                        log_path.display()
                    ));
                }
            }
            return Ok((
                ServiceStatus {
                    id: spec.id.clone(),
                    state: "running".into(),
                    healthy: true,
                    pid: Some(pid),
                    started_at: Some(started_at),
                    last_exit: None,
                },
                child,
            ));
        }
        if Instant::now() >= deadline {
            eprintln!(
                "desktop: 服务组件 {} 启动后 {}s 内健康端点未绿(进程存活;如实回 \
                 running+healthy=false,实例内部故障/慢启动见日志 {})",
                spec.id,
                SERVICE_HEALTH_WAIT.as_secs(),
                log_path.display()
            );
            return Ok((
                ServiceStatus {
                    id: spec.id.clone(),
                    state: "running".into(),
                    healthy: false,
                    pid: Some(pid),
                    started_at: Some(started_at),
                    last_exit: None,
                },
                child,
            ));
        }
        std::thread::sleep(SERVICE_HEALTH_POLL_INTERVAL);
    }
}

/// 服务停核心(SIGTERM 进程组 → 宽限 → SIGKILL 组 → 收尾;本会话句柄可
/// 回收退出码,孤儿先经 ps 身份复核再动组信号——防 pid 复用误杀无辜进程组;
/// 复核不过/已死 = 只转戳不动进程)。幂等:未在运行 → 直接回 stopped。
pub(crate) fn stop_service_process(
    data_root: &Path,
    python_bin: &Path,
    spec: &ComponentSpec,
    owned: Option<std::process::Child>,
) -> Result<ServiceStatus, String> {
    let svc = spec.service_spec()?;
    let prior = read_service_stamp(data_root, &spec.id).unwrap_or_default();
    let mut last_exit = prior.last_exit;
    if let Some(mut child) = owned {
        // 本会话亲生:句柄即身份证明,直接组停 + waitpid 回收退出码。
        let pid = child.id();
        eprintln!(
            "desktop: 服务组件 {} 停止中(SIGTERM 进程组 -{pid})",
            spec.id
        );
        terminate_service(pid);
        let deadline = Instant::now() + SERVICE_STOP_GRACE;
        let mut exit_status = None;
        while exit_status.is_none() && Instant::now() < deadline {
            exit_status = match child.try_wait() {
                Ok(st @ Some(_)) => st,
                Ok(None) => {
                    std::thread::sleep(Duration::from_millis(100));
                    None
                }
                Err(_) => break,
            };
        }
        if exit_status.is_none() {
            eprintln!(
                "desktop: 服务组件 {} 优雅停超时({}ms),升级 SIGKILL 进程组",
                spec.id,
                SERVICE_STOP_GRACE.as_millis()
            );
            force_kill_service(pid);
            exit_status = child.wait().ok();
        }
        if let Some(status) = exit_status {
            last_exit = exit_code_of(&status);
        }
        eprintln!(
            "desktop: 服务组件 {} 已停(组 -{pid} 零残留;退出观测 {:?})",
            spec.id, last_exit
        );
    } else if prior.state.as_deref() == Some("running") && prior.pid.is_some_and(service_pid_alive)
    {
        let pid = prior.pid.expect("is_some_and 已核");
        if pid_command_matches_service(pid, python_bin, &svc.start_cmd) {
            eprintln!(
                "desktop: 服务组件 {} 孤儿进程停止中(壳重启前拉起;SIGTERM 进程组 -{pid})",
                spec.id
            );
            terminate_service(pid);
            let deadline = Instant::now() + SERVICE_STOP_GRACE;
            while Instant::now() < deadline && service_group_alive(pid) {
                std::thread::sleep(Duration::from_millis(100));
            }
            if service_group_alive(pid) {
                force_kill_service(pid);
                let kill_deadline = Instant::now() + SERVICE_STOP_KILL_GRACE;
                while Instant::now() < kill_deadline && service_group_alive(pid) {
                    std::thread::sleep(Duration::from_millis(50));
                }
            }
            // 非亲生 waitpid 不可及:退出码无法观测,last_exit 保持 None 如实
            eprintln!(
                "desktop: 服务组件 {} 孤儿进程已停(组 -{pid} 零残留;跨会话退出码不可观测,last_exit=None 如实)",
                spec.id
            );
        } else {
            eprintln!(
                "desktop: 服务组件 {} 状态戳记 running(pid={})但 argv 复核不过(疑 pid 复用),\
                 不对它发组信号;戳如实转 stopped",
                spec.id, pid
            );
        }
    }
    let stamp = ServiceStamp {
        state: Some("stopped".into()),
        pid: None,
        started_at: None,
        last_exit,
    };
    write_service_stamp(data_root, &spec.id, &stamp);
    Ok(ServiceStatus {
        id: spec.id.clone(),
        state: "stopped".into(),
        healthy: false,
        pid: None,
        started_at: None,
        last_exit,
    })
}

/// 服务状态对账(幂等,零副作用除戳纠偏):
/// running 判定 = 本会话句柄 try_wait(可回收退出码)/ 状态戳 pid 探活(跨
/// 会话孤儿;壳退出后服务继续跑 = 状态记忆的一部分);戳记 running 但 pid
/// 已死 → 戳纠偏转 stopped(退出码不可观测,保持上次已知值)。
/// running 态顺带健康探测(≤2s);stopped 回 healthy=false。
pub(crate) fn reconcile_service_status(
    data_root: &Path,
    spec: &ComponentSpec,
    owned: Option<&mut std::process::Child>,
    owned_started_at: Option<u64>,
) -> Result<ServiceStatus, String> {
    let svc = spec.service_spec()?;
    let prior = read_service_stamp(data_root, &spec.id).unwrap_or_default();
    // —— owned 在场:try_wait 立即对账(死则回收退出码并纠偏戳)——
    if let Some(child) = owned {
        match child.try_wait() {
            Ok(Some(exit)) => {
                let code = exit_code_of(&exit);
                write_service_stamp(
                    data_root,
                    &spec.id,
                    &ServiceStamp {
                        state: Some("stopped".into()),
                        pid: None,
                        started_at: None,
                        last_exit: code,
                    },
                );
                return Ok(ServiceStatus {
                    id: spec.id.clone(),
                    state: "stopped".into(),
                    healthy: false,
                    pid: None,
                    started_at: None,
                    last_exit: code,
                });
            }
            Ok(None) => {
                let pid = child.id();
                let started_at = owned_started_at.or(prior.started_at);
                let healthy = probe_health_url(&svc.health_url);
                return Ok(ServiceStatus {
                    id: spec.id.clone(),
                    state: "running".into(),
                    healthy,
                    pid: Some(pid),
                    started_at,
                    last_exit: None,
                });
            }
            Err(err) => {
                return Err(format!("服务进程状态回收失败: {err}"));
            }
        }
    }
    // —— 无句柄(壳重启后/从未在本会话拉起):按戳 pid 探活对账 ——
    if prior.state.as_deref() == Some("running") {
        if let Some(pid) = prior.pid {
            if service_pid_alive(pid) {
                let healthy = probe_health_url(&svc.health_url);
                return Ok(ServiceStatus {
                    id: spec.id.clone(),
                    state: "running".into(),
                    healthy,
                    pid: Some(pid),
                    started_at: prior.started_at,
                    last_exit: None,
                });
            }
            eprintln!(
                "desktop: 服务组件 {} 状态戳记 running 但 pid={} 已不在(运行期间死亡),\
                 戳纠偏转 stopped(退出码不可观测,保持上次已知值)",
                spec.id, pid
            );
            write_service_stamp(
                data_root,
                &spec.id,
                &ServiceStamp {
                    state: Some("stopped".into()),
                    pid: None,
                    started_at: None,
                    last_exit: prior.last_exit,
                },
            );
        }
    }
    Ok(ServiceStatus {
        id: spec.id.clone(),
        state: "stopped".into(),
        healthy: false,
        pid: None,
        started_at: None,
        last_exit: prior.last_exit,
    })
}

// ---------------------------------------------------------------------------
// 状态组装(pyenv_get_status 扩展;两键契约 + 轨B kind 附加键)
// ---------------------------------------------------------------------------

/// `pyenv_get_status.components[]` 单条(契约:`{id, installed}` 两键钉死,
/// 轨B 服务组件附加 `kind: "service"`(skip_serializing_if:库组件条目 wire
/// 形不变——两键契约零破,老前端宽容忽略附加键);展示文案(label/
/// description)是前端展示层的事,注册表不在载荷里复述)。
#[derive(Clone, PartialEq, Eq, Debug, Serialize)]
pub struct ComponentStatus {
    pub id: String,
    pub installed: bool,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub kind: Option<String>,
}

/// 组装 components[](注册表序;注册表缺位 → 空表)。pyenv::status_at 调用。
pub fn component_statuses(data_root: &Path, resource_dir: Option<&Path>) -> Vec<ComponentStatus> {
    load_registry(resource_dir)
        .into_iter()
        .map(|spec| ComponentStatus {
            installed: is_component_installed(data_root, &spec),
            kind: spec.is_service().then(|| "service".to_string()),
            id: spec.id,
        })
        .collect()
}

// ---------------------------------------------------------------------------
// 安装本体(纯逻辑,无 AppHandle;单测主战场)
// ---------------------------------------------------------------------------

/// `pyenv_install_component` 结果(契约:`{id, installed, error}`;error 恒
/// 在场,无错为 null,与 steps[].error 同惯例)。
#[derive(Clone, PartialEq, Eq, Debug, Serialize)]
pub struct ComponentInstallOutcome {
    pub id: String,
    pub installed: bool,
    pub error: Option<String>,
}

/// 组件安装(复用安装链依赖段;轨A crawl4ai 带浏览器钩子,design §3):
/// 契约校验(未知 post_install 钩子零副作用拒)→ 磁盘预检(钩子加码)→
/// run_pip_spec(镜像索引透传)→ playwright chromium 钩子(落
/// `<数据根>/playwright-browsers/`)→ 指纹戳。成功落 ready+指纹;任一步
/// 失败/中断落 error+明细(installed=false 如实;重试幂等——pip 已装自动
/// 跳过、浏览器二进制续装)。
pub(crate) fn install_component(
    data_root: &Path,
    python_bin: &Path,
    spec: &ComponentSpec,
    index_url: Option<&str>,
    disk_required_bytes: u64,
) -> ComponentInstallOutcome {
    use crate::pyenv_install;
    let fail = |error: String, fingerprint: Option<String>| {
        write_component_stamp(
            data_root,
            &spec.id,
            &ComponentStamp {
                state: Some("error".into()),
                fingerprint,
                error: Some(error.clone()),
            },
        );
        ComponentInstallOutcome {
            id: spec.id.clone(),
            installed: false,
            error: Some(error),
        }
    };
    // —— 契约校验先于一切子进程:未知 post_install 钩子 / 钩子配套字段缺失
    //    = 注册表与壳版本漂移(新壳读旧表不会发生——旧表无此字段;新表配旧壳
    //    字段被忽略走纯 pip),结构化拒且零 pip/浏览器副作用 ——
    if let Some(hook) = spec.post_install.as_deref() {
        match hook {
            POST_INSTALL_PLAYWRIGHT_CHROMIUM => {}
            POST_INSTALL_PIP_SRC_NO_BUILD_ISOLATION => {
                if spec
                    .pip_src
                    .as_deref()
                    .map(str::trim)
                    .unwrap_or("")
                    .is_empty()
                {
                    return fail(
                        format!(
                            "post_install 钩子 {} 需要非空 pip_src 字段(当前缺失;注册表与壳版本漂移)",
                            POST_INSTALL_PIP_SRC_NO_BUILD_ISOLATION
                        ),
                        None,
                    );
                }
            }
            other => {
                return fail(
                    format!(
                        "未知 post_install 钩子: {other}(注册表与壳版本漂移;壳已知值: \
                         [{POST_INSTALL_PLAYWRIGHT_CHROMIUM}, {POST_INSTALL_PIP_SRC_NO_BUILD_ISOLATION}])"
                    ),
                    None,
                );
            }
        }
    }
    if let Err((kind, detail)) = pyenv_install::disk_precheck(
        data_root,
        disk_budget(disk_required_bytes, spec.post_install.as_deref()),
    ) {
        return fail(pyenv_install::render_error(kind, detail), None);
    }
    match pyenv_install::run_pip_spec(python_bin, &spec.pip_spec, index_url) {
        Ok(()) => {
            // —— 安装后钩子:pip 闭包成功后的二段动作;任一失败 = error 戳
            //    可见,不静默(重试幂等——已装段自动跳过)——
            if let Some(hook) = spec.post_install.as_deref() {
                match hook {
                    POST_INSTALL_PLAYWRIGHT_CHROMIUM => {
                        // 轨A crawl4ai:拉 chromium 进数据根浏览器目录
                        if let Err((kind, detail)) =
                            pyenv_install::run_playwright_install_chromium(
                                python_bin,
                                &playwright_browsers_path(data_root),
                            )
                        {
                            return fail(pyenv_install::render_error(kind, detail), None);
                        }
                    }
                    POST_INSTALL_PIP_SRC_NO_BUILD_ISOLATION => {
                        // 轨B searxng:二段装源码包(依赖已在场;构建期 import
                        // 才可解析,见 run_pip_src_no_build_isolation 注释)
                        let src = spec.pip_src.clone().unwrap_or_default();
                        if let Err((kind, detail)) =
                            pyenv_install::run_pip_src_no_build_isolation(
                                python_bin,
                                &src,
                                index_url,
                            )
                        {
                            return fail(pyenv_install::render_error(kind, detail), None);
                        }
                    }
                    _ => unreachable!("契约校验已把未知钩子拦在子进程之前"),
                }
            }
            write_component_stamp(
                data_root,
                &spec.id,
                &ComponentStamp {
                    state: Some("ready".into()),
                    fingerprint: Some(closure_fingerprint(spec)),
                    error: None,
                },
            );
            ComponentInstallOutcome {
                id: spec.id.clone(),
                installed: true,
                error: None,
            }
        }
        Err((kind, detail)) => fail(pyenv_install::render_error(kind, detail), None),
    }
}

// ---------------------------------------------------------------------------
// 胶水:AppHandle → IPC 命令(main.rs 注册)
// ---------------------------------------------------------------------------

/// 壳侧组件管理器(setup 时 manage):installing = 正在安装的组件 id
/// (单飞护栏:同刻只许一个组件 pip,防两代 pip 写同一环境互踩)。
#[derive(Default)]
pub struct ComponentManager {
    pub installing: Mutex<Option<String>>,
}

/// 装组件进自管环境(R4:设置页开关消费)。链路:注册表对 id → 环境在位
/// 护栏 → 主链/组件单飞护栏 → 后台线程跑依赖段(磁盘预检 + pip spec +
/// 镜像索引)→ 指纹戳 → 广播 `pyenv-status-changed`(components[] 随新)。
/// pip 阻塞跑在 spawn_blocking(不占 async runtime worker);卸载本期不做。
#[tauri::command]
pub async fn pyenv_install_component(
    app: AppHandle,
    id: String,
) -> Result<ComponentInstallOutcome, String> {
    // —— 注册表对 id(未知 id 结构化拒;注册表缺位 = 无组件可装,同报)——
    let data_root = crate::data_root(&app).map_err(|e| e.to_string())?;
    let resource_dir = app.path().resource_dir().ok();
    let registry = load_registry(resource_dir.as_deref());
    let Some(spec) = registry.iter().find(|entry| entry.id == id) else {
        let known: Vec<&str> = registry.iter().map(|entry| entry.id.as_str()).collect();
        return Err(format!(
            "未知组件 id: {id}(随包注册表现有: {known:?};注册表缺位时无可装组件)"
        ));
    };
    // —— 环境在位(先走完整配置;与 pyenv_sync_deps 同口径)——
    let python_bin = crate::pyenv::python_bin_path(&data_root);
    if !python_bin.exists() {
        return Err("Python 运行环境未就位:请先在设置页「开始配置」完成环境安装,再装组件".into());
    }
    // —— 护栏:主安装链在跑 / 组件安装单飞 ——
    if app
        .state::<crate::pyenv::PyenvManager>()
        .installing
        .lock()
        .unwrap()
        .is_some()
    {
        return Err("Python 环境安装进行中:请等安装完成后再装组件".into());
    }
    {
        let manager = app.state::<ComponentManager>();
        let mut slot = manager.installing.lock().unwrap();
        if slot.is_some() {
            return Err("组件安装进行中,请稍候(同刻只装一个)".into());
        }
        *slot = Some(id.clone());
    }
    // —— 依赖段后台执行(spawn_blocking;镜像索引继承 pyenv-settings.json)——
    let index_url = crate::pyenv::read_settings(&data_root).mirror_pypi;
    let spec = spec.clone();
    let root = data_root.clone();
    let joined = tauri::async_runtime::spawn_blocking(move || {
        install_component(
            &root,
            &python_bin,
            &spec,
            index_url.as_deref(),
            crate::pyenv_install::DISK_REQUIRED_BYTES,
        )
    });
    let outcome = match joined.await {
        Ok(outcome) => outcome,
        Err(err) => ComponentInstallOutcome {
            id: id.clone(),
            installed: false,
            error: Some(format!("组件安装线程失败: {err}")),
        },
    };
    // —— 清槽 + 广播(components[] 随新;拉取仍是前端真相源)——
    *app.state::<ComponentManager>().installing.lock().unwrap() = None;
    let _ = crate::pyenv::emit_current(&app);
    Ok(outcome)
}

// ---------------------------------------------------------------------------
// 轨B 生命周期 IPC(service_start/stop/status;main.rs generate_handler 注册)
// ---------------------------------------------------------------------------

/// 壳侧服务组件管理器(setup 时 manage):本会话拉起的服务子进程句柄
/// (id → 亲生进程;退出码回收依赖句柄)。跨壳重启的孤儿不在表内——靠
/// 状态戳 pid + ps argv 复核对账(G-Q5 状态记忆的一部分)。
#[derive(Default)]
pub struct ServiceManager {
    pub children: Mutex<HashMap<String, ServiceChild>>,
}

/// 亲生服务子进程句柄 + 启动时刻(status 对账的 started_at 来源)。
pub struct ServiceChild {
    pub child: std::process::Child,
    pub started_at: u64,
}

/// 注册表对 id + 轨B 服务声明校验(未知 id / 非服务组件 → 结构化拒;
/// service_* 三 IPC 共用入口)。
fn resolve_service_spec(app: &AppHandle, id: &str) -> Result<(PathBuf, ComponentSpec), String> {
    let data_root = crate::data_root(app).map_err(|e| e.to_string())?;
    let resource_dir = app.path().resource_dir().ok();
    let registry = load_registry(resource_dir.as_deref());
    let Some(spec) = registry.into_iter().find(|entry| entry.id == id) else {
        return Err(format!(
            "未知组件 id: {id}(注册表内条目均不可作为服务启停;components.json 缺位时无可装组件)"
        ));
    };
    spec.service_spec().map(|_| ())?;
    Ok((data_root, spec))
}

/// 取出本会话亲生句柄(状态对账/停服全程持有所有权;探活/探测不在锁内):
/// running 仍真 → 调用方负责放回(park_child_if_running);已死 → 由对账
/// 回收退出码,不再放回。
fn take_owned_child(app: &AppHandle, id: &str) -> Option<ServiceChild> {
    app.state::<ServiceManager>()
        .children
        .lock()
        .unwrap()
        .remove(id)
}

/// 对账后仍 running 的亲生句柄放回管理器(否则已被回收/进孤儿表)。
fn park_child_if_running(app: &AppHandle, id: &str, entry: Option<ServiceChild>, running: bool) {
    if running {
        if let Some(entry) = entry {
            app.state::<ServiceManager>()
                .children
                .lock()
                .unwrap()
                .insert(id.to_string(), entry);
        }
    }
}

/// 阻塞面:状态对账(含 ≤2s 健康探测;从 async 命令包进 spawn_blocking)。
/// 亲生句柄全程独占持有(探活/探测不在管理器锁内);对账后仍 running 才放回。
fn current_service_status_blocking(
    app: &AppHandle,
    data_root: &Path,
    spec: &ComponentSpec,
) -> Result<ServiceStatus, String> {
    let mut entry = take_owned_child(app, &spec.id);
    let owned_started_at = entry.as_ref().map(|e| e.started_at);
    let status = {
        let mut child = entry.as_mut().map(|e| &mut e.child);
        reconcile_service_status(data_root, spec, child.as_deref_mut(), owned_started_at)?
    };
    let running = status.state == "running";
    park_child_if_running(app, &spec.id, entry, running);
    Ok(status)
}

/// 启动服务组件(G-Q5:显式动作;装好默认停,启停只走设置卡按钮,引擎侧
/// 不隐式拉起)。幂等:已在运行(本会话句柄/跨会话孤儿戳 pid 存活)→ 原样
/// 回当前状态,绝不重复 spawn、绝不杀活进程。
#[tauri::command]
pub async fn service_start(app: AppHandle, id: String) -> Result<ServiceStatus, String> {
    let (data_root, spec) = resolve_service_spec(&app, &id)?;
    let python_bin = crate::pyenv::python_bin_path(&data_root);
    if !python_bin.exists() {
        return Err(
            "Python 运行环境未就位:请先在设置页「开始配置」完成环境安装,再启动服务组件".into(),
        );
    }
    if !is_component_installed(&data_root, &spec) {
        return Err(format!(
            "服务组件 {id} 尚未安装:请先在该组件行装组件(pip 闭包装完才有可启动的服务进程)"
        ));
    }
    // 护栏:pip 变异进行中(主链/组件安装)不启服务——site-packages 正在被写,
    // 此时起服务读到的是半套环境(与安装侧反向护栏对称的轻量前置)。
    if app
        .state::<crate::pyenv::PyenvManager>()
        .installing
        .lock()
        .unwrap()
        .is_some()
    {
        return Err("Python 环境安装进行中:请等安装完成后再启动服务组件".into());
    }
    if app
        .state::<ComponentManager>()
        .installing
        .lock()
        .unwrap()
        .is_some()
    {
        return Err("组件安装进行中:请等组件安装完成后再启动服务组件".into());
    }
    let handle = app.clone();
    let joined = tauri::async_runtime::spawn_blocking(move || {
        // 幂等先行:已在运行 → 原样回(健康点顺带对账)
        if let Ok(status) = current_service_status_blocking(&handle, &data_root, &spec) {
            if status.state == "running" {
                return Ok(status);
            }
        }
        let python = crate::pyenv::python_bin_path(&data_root);
        let (status, child) = start_service_process(&data_root, &python, &spec)?;
        let started_at = status.started_at.unwrap_or_default();
        handle
            .state::<ServiceManager>()
            .children
            .lock()
            .unwrap()
            .insert(
                spec.id.clone(),
                ServiceChild {
                    child,
                    started_at,
                },
            );
        Ok(status)
    });
    match joined.await {
        Ok(result) => result,
        Err(err) => Err(format!("服务启动线程失败: {err}")),
    }
}

/// 停止服务组件(SIGTERM 进程组 → 宽限 → SIGKILL 组;跨会话孤儿先经
/// ps argv 身份复核再动组信号——防 pid 复用误杀无辜进程组)。幂等:未在
/// 运行 → 直接回 stopped(不报错,设置卡按钮语义即幂等关)。
#[tauri::command]
pub async fn service_stop(app: AppHandle, id: String) -> Result<ServiceStatus, String> {
    let (data_root, spec) = resolve_service_spec(&app, &id)?;
    let python_bin = crate::pyenv::python_bin_path(&data_root);
    let handle = app.clone();
    let joined = tauri::async_runtime::spawn_blocking(move || {
        let owned = take_owned_child(&handle, &spec.id).map(|entry| entry.child);
        stop_service_process(&data_root, &python_bin, &spec, owned)
    });
    match joined.await {
        Ok(result) => result,
        Err(err) => Err(format!("服务停止线程失败: {err}")),
    }
}

/// 服务状态查询(就绪检查态:对账 + 健康点;设置卡绿点/启停按钮初值消费)。
#[tauri::command]
pub async fn service_status(app: AppHandle, id: String) -> Result<ServiceStatus, String> {
    let (data_root, spec) = resolve_service_spec(&app, &id)?;
    let handle = app.clone();
    let joined = tauri::async_runtime::spawn_blocking(move || {
        current_service_status_blocking(&handle, &data_root, &spec)
    });
    match joined.await {
        Ok(result) => result,
        Err(err) => Err(format!("服务状态探测线程失败: {err}")),
    }
}

// ---------------------------------------------------------------------------
// 单测(门:10-05-table-restore 桌面侧「cargo 单测」;sh 桩部分 unix 门控)
// ---------------------------------------------------------------------------

#[cfg(test)]
mod tests {
    use super::*;

    /// 注册表 JSON(契约形态:{components:[{id,pip_spec,label,description}]})。
    fn registry_json(components: serde_json::Value) -> String {
        serde_json::json!({ "components": components }).to_string()
    }

    /// 测试基准 spec 串(与随包 components.json / pyproject extras
    /// myssia[table] 同源的三件闭包;tests/desktop/test_pyenv_resources.py
    /// 交叉对齐把守两侧不漂移)。
    const TABLE_PIP_SPEC: &str = "rapid-table==3.0.2 rapidocr-onnxruntime>=1.3 tqdm>=4";

    /// crawl4ai 组件闭包(10-06-native-plugin-components 轨A;与随包
    /// components.json 同源,tests/desktop/test_pyenv_resources.py 交叉对齐):
    /// 窗 >=0.9,<0.10 = 本仓 uv.lock/dev 实测 0.9.4 所在线,引擎与
    /// render_crawl4ai 场景件均按 0.9.x API 探测写作;0.10+ 未验不冒进。
    const CRAWL4AI_PIP_SPEC: &str = "crawl4ai>=0.9,<0.10";

    fn base_spec(id: &str, pip_spec: &str, label: &str, description: &str) -> ComponentSpec {
        ComponentSpec {
            id: id.into(),
            pip_spec: pip_spec.into(),
            label: label.into(),
            description: description.into(),
            post_install: None,
            pip_src: None,
            kind: None,
            service: None,
            pre_start: None,
        }
    }

    fn table_spec() -> ComponentSpec {
        base_spec(
            "table",
            TABLE_PIP_SPEC,
            "表格还原",
            "截图表格还原成结构化 Markdown",
        )
    }

    fn crawl4ai_spec() -> ComponentSpec {
        ComponentSpec {
            post_install: Some(POST_INSTALL_PLAYWRIGHT_CHROMIUM.into()),
            ..base_spec(
                "crawl4ai",
                CRAWL4AI_PIP_SPEC,
                "JS 渲染抓取(crawl4ai)",
                "JS 渲染抓取引擎(crawl4ai + playwright chromium)",
            )
        }
    }

    fn write_registry(resource: &Path, text: &str) {
        std::fs::write(components_registry_path(resource), text).expect("注册表写入失败");
    }

    /// 注册表读取:契约文件原样消费;缺位/坏文件/半截条目宽容为空表/剔除。
    #[test]
    fn registry_load_is_tolerant_and_filtered() {
        let resource = tempfile::tempdir().expect("资源临时目录创建失败");
        // 契约形态(随包 components.json 同款,含闭包多 spec 串)原样进表
        write_registry(
            resource.path(),
            &registry_json(serde_json::json!([{
                "id": "table",
                "pip_spec": TABLE_PIP_SPEC,
                "label": "表格还原",
                "description": "截图表格还原成结构化 Markdown",
            }])),
        );
        let registry = load_registry(Some(resource.path()));
        assert_eq!(registry, vec![table_spec()]);
        assert_eq!(registry[0].pip_spec, TABLE_PIP_SPEC);

        // description 缺省空串(宽容);未知附加字段忽略;post_install 缺省
        // None(纯 pip 组件,零行为差)——crawl4ai 带钩子条目原样进表
        write_registry(
            resource.path(),
            &registry_json(serde_json::json!([{
                "id": "x", "pip_spec": "x==1", "label": "X", "extra": 1,
            }])),
        );
        assert_eq!(
            load_registry(Some(resource.path())),
            vec![base_spec("x", "x==1", "X", "")]
        );
        write_registry(
            resource.path(),
            &registry_json(serde_json::json!([{
                "id": "crawl4ai", "pip_spec": CRAWL4AI_PIP_SPEC,
                "label": "JS 渲染抓取(crawl4ai)",
                "description": "d",
                "post_install": POST_INSTALL_PLAYWRIGHT_CHROMIUM,
            }])),
        );
        assert_eq!(
            load_registry(Some(resource.path())),
            vec![ComponentSpec {
                description: "d".into(),
                ..crawl4ai_spec()
            }]
        );

        // id/pip_spec 空串剔除;缺 key 的条目整文件解析失败 → 空表
        write_registry(
            resource.path(),
            &registry_json(serde_json::json!([
                { "id": "", "pip_spec": "x==1", "label": "A" },
                { "id": "y", "pip_spec": "", "label": "B" },
            ])),
        );
        assert!(load_registry(Some(resource.path())).is_empty());
        write_registry(
            resource.path(),
            &registry_json(serde_json::json!([{ "id": "z" }])),
        );
        assert!(load_registry(Some(resource.path())).is_empty());

        // 文件缺位 / 坏 JSON / resource_dir 缺位 → 空表(零行为变化)
        std::fs::remove_file(components_registry_path(resource.path())).unwrap();
        assert!(load_registry(Some(resource.path())).is_empty());
        write_registry(resource.path(), "{ not json");
        assert!(load_registry(Some(resource.path())).is_empty());
        assert!(load_registry(None).is_empty());
    }

    /// 指纹:同 spec 串稳定、异 spec 串不同;64 位 hex 小写。
    #[test]
    fn spec_fingerprint_is_stable_sha256_hex() {
        let a = spec_fingerprint(TABLE_PIP_SPEC);
        assert_eq!(a, spec_fingerprint(TABLE_PIP_SPEC));
        // 闭包任一件变脸(壳更新改钉版)即不同指纹
        let drifted_pin = "rapid-table==3.0.3 rapidocr-onnxruntime>=1.3 tqdm>=4";
        assert_ne!(a, spec_fingerprint(drifted_pin));
        assert_ne!(a, spec_fingerprint("rapid-table==3.0.2"));
        assert_eq!(a.len(), 64);
        assert!(a
            .chars()
            .all(|c| c.is_ascii_hexdigit() && !c.is_ascii_uppercase()));
    }

    /// 空白 spec 串(全空白可过注册表非空滤)→ run_pip_spec 拒跑,
    /// 零子进程拉起(python 路径故意不存在即证:未触 spawn)。
    #[test]
    fn blank_pip_spec_is_rejected_without_spawning() {
        let (_, detail) = crate::pyenv_install::run_pip_spec(
            Path::new("/nonexistent/python3-guard-probe"),
            "   ",
            None,
        )
        .expect_err("空白 spec 应拒跑");
        assert!(detail.contains("pip spec 为空"), "实际: {detail}");
    }

    /// 浏览器目录路径与注入判定(轨A):目录在才注(未装组件零行为差,
    /// playwright 各回各家);路径 = 数据根下 playwright-browsers/。
    #[test]
    fn browsers_env_injection_gated_on_directory_presence() {
        let data = tempfile::tempdir().expect("数据根临时目录创建失败");
        let browsers = playwright_browsers_path(data.path());
        assert_eq!(
            browsers,
            data.path().join(PLAYWRIGHT_BROWSERS_DIR),
            "浏览器目录必须在数据根下(卸载组件/清数据根即整目录消)"
        );
        assert!(!should_inject_browsers_env(data.path()), "目录缺位不注");
        std::fs::create_dir_all(&browsers).unwrap();
        assert!(should_inject_browsers_env(data.path()), "目录在即注");
    }

    /// 磁盘预算:已知钩子加码 600MB、无钩子/未知钩子不加;saturating 不溢出。
    #[test]
    fn disk_budget_adds_chromium_headroom_only_for_known_hook() {
        let base = 500 * 1024 * 1024u64;
        assert_eq!(disk_budget(base, None), base);
        assert_eq!(disk_budget(base, Some("bogus")), base);
        assert_eq!(
            disk_budget(base, Some(POST_INSTALL_PLAYWRIGHT_CHROMIUM)),
            base + PLAYWRIGHT_CHROMIUM_DISK_BYTES
        );
        assert_eq!(
            disk_budget(u64::MAX, Some(POST_INSTALL_PLAYWRIGHT_CHROMIUM)),
            u64::MAX,
            "saturating_add 不得溢出回绕"
        );
    }

    /// installed 判定:ready+指纹一致才 true;漂移/error/中断/缺戳/坏戳 false;
    /// id 防御(路径逃逸形 id 拒读)。
    #[test]
    fn installed_requires_ready_stamp_with_matching_fingerprint() {
        let data = tempfile::tempdir().expect("数据根临时目录创建失败");
        let spec = table_spec();

        // 缺戳 → 未装
        assert!(!is_component_installed(data.path(), &spec));
        // ready + 指纹一致 → 已装
        write_component_stamp(
            data.path(),
            &spec.id,
            &ComponentStamp {
                state: Some("ready".into()),
                fingerprint: Some(spec_fingerprint(&spec.pip_spec)),
                error: None,
            },
        );
        assert!(is_component_installed(data.path(), &spec));
        // 指纹漂移(闭包改钉版,壳更新场景)→ 未装(引导重装)
        let drifted = ComponentSpec {
            pip_spec: "rapid-table==3.0.3 rapidocr-onnxruntime>=1.3 tqdm>=4".into(),
            ..spec.clone()
        };
        assert!(!is_component_installed(data.path(), &drifted));
        // error 终态 / 非终态(中断)→ 未装
        for state in [Some("error".to_string()), None] {
            write_component_stamp(
                data.path(),
                &spec.id,
                &ComponentStamp {
                    state,
                    fingerprint: None,
                    error: Some("pip_failed: boom".into()),
                },
            );
            assert!(!is_component_installed(data.path(), &spec));
        }
        // 坏戳 → 未装(不拦状态展示)
        std::fs::create_dir_all(data.path().join(COMPONENTS_STAMP_DIR)).unwrap();
        std::fs::write(component_stamp_path(data.path(), &spec.id), "{ broken").unwrap();
        assert!(!is_component_installed(data.path(), &spec));
        // 路径逃逸形 id:读戳拒读、写戳拒写
        assert!(read_component_stamp(data.path(), "../escape").is_none());
        assert!(read_component_stamp(data.path(), "a/b").is_none());
    }

    /// 状态组装:components[] 两键形态({id, installed})随注册表与戳实况;
    /// 注册表缺位 → 空。经 pyenv::status_at 闭环(与 pyenv_get_status 同源)。
    #[test]
    fn component_statuses_two_key_shape_via_status_at() {
        let data = tempfile::tempdir().expect("数据根临时目录创建失败");
        let resource = tempfile::tempdir().expect("资源临时目录创建失败");
        write_registry(
            resource.path(),
            &registry_json(serde_json::json!([{
                "id": "table", "pip_spec": TABLE_PIP_SPEC,
                "label": "表格还原", "description": "d",
            }])),
        );
        // 未装 → installed:false
        let status = crate::pyenv::status_at(
            data.path(),
            Some(resource.path()),
            None,
            &crate::pyenv::PyenvSettings::default(),
        );
        let rendered = serde_json::to_value(&status).unwrap();
        assert_eq!(
            rendered["components"],
            serde_json::json!([{ "id": "table", "installed": false }]),
            "components[] 须恰为两键形态"
        );
        // 落 ready 戳 → installed:true
        write_component_stamp(
            data.path(),
            "table",
            &ComponentStamp {
                state: Some("ready".into()),
                fingerprint: Some(spec_fingerprint(TABLE_PIP_SPEC)),
                error: None,
            },
        );
        let status = crate::pyenv::status_at(
            data.path(),
            Some(resource.path()),
            None,
            &crate::pyenv::PyenvSettings::default(),
        );
        assert_eq!(
            serde_json::to_value(&status).unwrap()["components"],
            serde_json::json!([{ "id": "table", "installed": true }])
        );
        // 注册表缺位 → 空表
        let status = crate::pyenv::status_at(
            data.path(),
            None,
            None,
            &crate::pyenv::PyenvSettings::default(),
        );
        assert!(status.components.is_empty());
    }

    // —— 安装链真跑(sh 桩 python;unix 门控,惯例同 pyenv_install 单测)——

    /// sh 桩 python:pip / playwright 调用各自记账到日志,可控失败;
    /// 非 pip/playwright argv 即失败。playwright 分支同时记
    /// PLAYWRIGHT_BROWSERS_PATH(钩子落点断言依据)。pip 带
    /// --no-build-isolation flag(轨B searxng 二段装)路由独立记账文件
    /// (pip-src-invocations.log)+ 独立失败开关(src-fail-marker;一段
    /// 闭包装不受影响)。
    fn stub_python(dir: &Path) -> PathBuf {
        let log = dir.join("pip-invocations.log");
        let fail = dir.join("pip-fail-marker");
        let pw_fail = dir.join("playwright-fail-marker");
        let src_log = dir.join("pip-src-invocations.log");
        let src_fail = dir.join("src-fail-marker");
        let bin = dir.join("python3");
        let script = format!(
            "#!/bin/sh\n\
             if [ \"$1\" = \"-m\" ] && [ \"$2\" = \"pip\" ]; then\n\
             \x20 case \"$*\" in\n\
             \x20   *--no-build-isolation*)\n\
             \x20     printf '%s\\n' \"$*\" >> '{}'\n\
             \x20     if [ -f '{}' ]; then echo 'stub src pip boom' >&2; exit 1; fi\n\
             \x20     exit 0\n\
             \x20     ;;\n\
             \x20 esac\n\
             \x20 printf '%s\\n' \"$*\" >> '{}'\n\
             \x20 if [ -f '{}' ]; then echo 'stub pip boom' >&2; exit 1; fi\n\
             \x20 exit 0\n\
             fi\n\
             if [ \"$1\" = \"-m\" ] && [ \"$2\" = \"playwright\" ]; then\n\
             \x20 printf 'playwright browsers=%s argv=%s\\n' \"$PLAYWRIGHT_BROWSERS_PATH\" \"$*\" >> '{}'\n\
             \x20 if [ -f '{}' ]; then echo 'stub playwright boom' >&2; exit 1; fi\n\
             \x20 exit 0\n\
             fi\n\
             exit 1\n",
            src_log.display(),
            src_fail.display(),
            log.display(),
            fail.display(),
            log.display(),
            pw_fail.display(),
        );
        std::fs::write(&bin, script).expect("桩 python 写入失败");
        use std::os::unix::fs::PermissionsExt;
        std::fs::set_permissions(&bin, std::fs::Permissions::from_mode(0o755))
            .expect("桩 python 置可执行位失败");
        bin
    }
    fn pip_log(data_root: &Path) -> Vec<String> {
        std::fs::read_to_string(data_root.join("pip-invocations.log"))
            .map(|text| text.lines().map(String::from).collect())
            .unwrap_or_default()
    }

    #[cfg(unix)]
    mod install {
        use super::*;


        fn install(
            python: &Path,
            data_root: &Path,
            index_url: Option<&str>,
        ) -> ComponentInstallOutcome {
            install_component(
                data_root,
                python,
                &table_spec(),
                index_url,
                1024 * 1024, // 磁盘门注小值(预检本身另测)
            )
        }


        /// 成功:pip argv 逐条含闭包三件(位置参数,无 -r);落 ready+指纹
        /// (整串 sha256);installed 翻真。
        #[test]
        fn success_pins_closure_specs_without_r_flag_and_stamps_ready() {
            let dir = tempfile::tempdir().expect("临时目录创建失败");
            let python = stub_python(dir.path());
            let outcome = install(&python, dir.path(), None);

            assert_eq!(
                outcome,
                ComponentInstallOutcome {
                    id: "table".into(),
                    installed: true,
                    error: None
                }
            );
            let lines = pip_log(dir.path());
            assert_eq!(lines.len(), 1, "组件安装恰跑一次 pip");
            // 闭包三件逐条作位置参数(质检高危修正面:跟引擎 extras 同源全装,
            // 裸装主件会让引擎 dependency_missing 于 rapidocr_onnxruntime)
            assert!(
                lines[0].contains("-m pip install")
                    && TABLE_PIP_SPEC
                        .split_whitespace()
                        .all(|spec| lines[0].contains(spec)),
                "argv 应含闭包全部 spec: {}",
                lines[0]
            );
            assert!(
                !lines[0].contains(" -r "),
                "spec 是位置参数,不走 -r: {}",
                lines[0]
            );
            let stamp = read_component_stamp(dir.path(), "table").expect("成功应落戳");
            assert_eq!(stamp.state.as_deref(), Some("ready"));
            assert_eq!(
                stamp.fingerprint.as_deref(),
                Some(spec_fingerprint(TABLE_PIP_SPEC).as_str())
            );
            assert_eq!(stamp.error, None);
            assert!(is_component_installed(dir.path(), &table_spec()));
        }

        /// 镜像索引继承:pyenv-settings 的 mirror_pypi 经 --index-url 透传(R4)。
        #[test]
        fn mirror_pypi_index_url_is_passed_through() {
            let dir = tempfile::tempdir().expect("临时目录创建失败");
            let python = stub_python(dir.path());
            let outcome = install(&python, dir.path(), Some("https://pypi.example/simple"));

            assert!(outcome.installed);
            let lines = pip_log(dir.path());
            assert!(
                lines[0].contains("--index-url https://pypi.example/simple"),
                "镜像覆盖应透传: {}",
                lines[0]
            );
        }

        /// 失败:pip_failed 分类 + 明细回显;落 error 戳;installed 如实 false。
        #[test]
        fn pip_failure_classified_and_stamped_error() {
            let dir = tempfile::tempdir().expect("临时目录创建失败");
            let python = stub_python(dir.path());
            std::fs::write(dir.path().join("pip-fail-marker"), b"1").unwrap();
            let outcome = install(&python, dir.path(), None);

            assert!(!outcome.installed);
            let error = outcome.error.expect("失败应带明细");
            assert!(error.starts_with("pip_failed: "), "实际: {error}");
            assert!(error.contains("stub pip boom"), "输出尾部应回显: {error}");
            let stamp = read_component_stamp(dir.path(), "table").expect("失败也应落戳");
            assert_eq!(stamp.state.as_deref(), Some("error"));
            assert_eq!(stamp.fingerprint, None, "失败不落指纹(防误判已装)");
            assert!(!is_component_installed(dir.path(), &table_spec()));
        }

        /// 磁盘预检不足 → disk_full 分类挂零安装(pip 桩零调用)。
        #[test]
        fn disk_precheck_failure_blocks_before_pip() {
            let dir = tempfile::tempdir().expect("临时目录创建失败");
            let python = stub_python(dir.path());
            let outcome = install_component(
                dir.path(),
                &python,
                &table_spec(),
                None,
                u64::MAX, // 预检必不过
            );
            assert!(!outcome.installed);
            let error = outcome.error.expect("预检失败应带明细");
            assert!(error.starts_with("disk_full: "), "实际: {error}");
            assert!(pip_log(dir.path()).is_empty(), "预检不过零 pip 调用");
        }

        // —— crawl4ai 轨A:post_install 浏览器钩子(10-06-native-plugin-components)——

        fn install_crawl4ai(python: &Path, data_root: &Path) -> ComponentInstallOutcome {
            install_component(data_root, python, &crawl4ai_spec(), None, 1024 * 1024)
        }

        /// crawl4ai 成功链:pip 闭包 → playwright chromium 钩子恰各跑一次;
        /// 钩子 PLAYWRIGHT_BROWSERS_PATH = 数据根 playwright-browsers/(G-Q6
        /// 落点);落 ready+指纹(基准仍是 pip_spec)。
        #[test]
        fn crawl4ai_success_runs_chromium_hook_into_data_root_browsers_dir() {
            let dir = tempfile::tempdir().expect("临时目录创建失败");
            let python = stub_python(dir.path());
            let outcome = install_crawl4ai(&python, dir.path());

            assert_eq!(
                outcome,
                ComponentInstallOutcome {
                    id: "crawl4ai".into(),
                    installed: true,
                    error: None
                }
            );
            let lines = pip_log(dir.path());
            assert_eq!(lines.len(), 2, "pip + playwright 恰各一次: {lines:?}");
            assert!(
                lines[0].contains("-m pip install") && lines[0].contains(CRAWL4AI_PIP_SPEC),
                "pip 段先跑且带闭包窗: {}",
                lines[0]
            );
            assert!(
                lines[1].starts_with("playwright browsers=")
                    && lines[1].contains("install chromium"),
                "钩子段 = playwright install chromium: {}",
                lines[1]
            );
            assert!(
                lines[1].contains(
                    playwright_browsers_path(dir.path())
                        .to_str()
                        .expect("临时目录路径可 utf-8")
                ),
                "PLAYWRIGHT_BROWSERS_PATH 必须落数据根浏览器目录: {}",
                lines[1]
            );
            let stamp = read_component_stamp(dir.path(), "crawl4ai").expect("成功应落戳");
            assert_eq!(stamp.state.as_deref(), Some("ready"));
            assert_eq!(
                stamp.fingerprint.as_deref(),
                Some(spec_fingerprint(CRAWL4AI_PIP_SPEC).as_str()),
                "指纹基准仍是 pip_spec(钩子不进漂移判定)"
            );
            assert_eq!(stamp.error, None);
            assert!(is_component_installed(dir.path(), &crawl4ai_spec()));
        }

        /// chromium 钩子失败:pip 已成功也如实翻 error 戳(不静默)、不落指纹
        /// (防误判已装);重试幂等(pip 段 already satisfied 跳过)。
        #[test]
        fn chromium_hook_failure_stamps_error_after_pip_success() {
            let dir = tempfile::tempdir().expect("临时目录创建失败");
            let python = stub_python(dir.path());
            std::fs::write(dir.path().join("playwright-fail-marker"), b"1").unwrap();
            let outcome = install_crawl4ai(&python, dir.path());

            assert!(!outcome.installed);
            let error = outcome.error.expect("钩子失败应带明细");
            assert!(error.starts_with("pip_failed: "), "复用可重试分类: {error}");
            assert!(error.contains("stub playwright boom"), "输出尾部应回显: {error}");
            let lines = pip_log(dir.path());
            assert_eq!(lines.len(), 2, "pip 成功 + 钩子失败各留痕: {lines:?}");
            let stamp = read_component_stamp(dir.path(), "crawl4ai").expect("失败也应落戳");
            assert_eq!(stamp.state.as_deref(), Some("error"));
            assert_eq!(stamp.fingerprint, None, "失败不落指纹(防误判已装)");
            assert!(!is_component_installed(dir.path(), &crawl4ai_spec()));
        }

        /// 未知 post_install 钩子:结构化拒且零子进程副作用(注册表与壳版本
        /// 漂移不静默装一半)。
        #[test]
        fn unknown_post_install_hook_rejected_without_spawning() {
            let dir = tempfile::tempdir().expect("临时目录创建失败");
            let python = stub_python(dir.path());
            let bogus = ComponentSpec {
                post_install: Some("bogus-hook".into()),
                ..crawl4ai_spec()
            };
            let outcome =
                install_component(dir.path(), &python, &bogus, None, 1024 * 1024);

            assert!(!outcome.installed);
            let error = outcome.error.expect("契约漂移应带明细");
            assert!(
                error.contains("未知 post_install 钩子") && error.contains("bogus-hook"),
                "实际: {error}"
            );
            assert!(
                pip_log(dir.path()).is_empty(),
                "契约校验先于一切子进程(零 pip/零 playwright)"
            );
            let stamp = read_component_stamp(dir.path(), "crawl4ai").expect("拒也应落戳");
            assert_eq!(stamp.state.as_deref(), Some("error"));
        }
    }

    // —— 轨B 壳服务组件(10-06-native-plugin-components 阶段2;design §2/G-Q5)——

    /// searxng 服务条目(与随包 components.json 同源;仓测锚点):闭包两段装
    /// + granian 服务端 + healthz 健康端点 + SEARXNG_SETTINGS_PATH 注入。
    const SEARXNG_PIP_SPEC: &str = "-r https://raw.githubusercontent.com/searxng/searxng/d48c4b555421e824342c51d68482dd0898e54d0f/requirements.txt granian==2.8.3 setuptools>=75 wheel>=0.45";
    const SEARXNG_PIP_SRC: &str =
        "searxng@git+https://github.com/searxng/searxng.git@d48c4b555421e824342c51d68482dd0898e54d0f";
    const SEARXNG_START_CMD: &[&str] = &[
        "-m",
        "granian",
        "--interface",
        "wsgi",
        "--host",
        "127.0.0.1",
        "--port",
        "8888",
        "searx.webapp:app",
    ];

    fn searxng_spec() -> ComponentSpec {
        let service = ServiceSpec {
            start_cmd: SEARXNG_START_CMD.iter().map(|s| s.to_string()).collect(),
            health_url: "http://127.0.0.1:8888/healthz".into(),
            port: 8888,
            env: [(
                "SEARXNG_SETTINGS_PATH".to_string(),
                format!("{SERVICE_DIR_PLACEHOLDER}/settings.yml"),
            )]
            .into_iter()
            .collect(),
        };
        ComponentSpec {
            post_install: Some(POST_INSTALL_PIP_SRC_NO_BUILD_ISOLATION.into()),
            pip_src: Some(SEARXNG_PIP_SRC.into()),
            kind: Some("service".into()),
            service: Some(service),
            pre_start: Some(PRE_START_SEARXNG_SETTINGS.into()),
            ..base_spec(
                "searxng",
                SEARXNG_PIP_SPEC,
                "关键词日报(SearXNG)",
                "自托管聚合搜索服务组件",
            )
        }
    }

    /// 注册表:searxng 服务条目(kind/service/pre_start/pip_src 节)原样进表;
    /// kind/service 节一致性校验(服务条目缺 service 节、库条目带 service 节、
    /// 未知 kind → service_spec 结构化拒;库组件默认 None 走既有安装链零行为差)。
    #[test]
    fn registry_loads_searxng_service_entry_and_validates_kind() {
        let resource = tempfile::tempdir().expect("资源临时目录创建失败");
        write_registry(
            resource.path(),
            &serde_json::to_string(&serde_json::json!({ "components": [serde_json::to_value(searxng_spec()).unwrap()] }))
                .unwrap(),
        );
        assert_eq!(load_registry(Some(resource.path())), vec![searxng_spec()]);
        assert!(searxng_spec().is_service());
        assert!(searxng_spec().service_spec().is_ok());

        // 形态漂移三态:service 节缺失 / 库条目携带 service 节 / 未知 kind
        let missing_node = ComponentSpec {
            service: None,
            ..searxng_spec()
        };
        assert!(
            missing_node
                .service_spec()
                .unwrap_err()
                .contains("缺 service 节")
        );
        let library_with_node = ComponentSpec {
            kind: None,
            ..searxng_spec()
        };
        assert!(library_with_node
            .service_spec()
            .unwrap_err()
            .contains("未声明 kind=service"));
        let unknown_kind = ComponentSpec {
            kind: Some("daemon".into()),
            ..searxng_spec()
        };
        assert!(
            unknown_kind
                .service_spec()
                .unwrap_err()
                .contains("未知组件 kind")
        );
        // 库组件默认态(table)→ 「不是服务组件」结构化拒
        let err = table_spec().service_spec().unwrap_err();
        assert!(
            err.contains("不是服务组件") && err.contains("table"),
            "实际: {err}"
        );
        // 闭包指纹:searxng 两段闭包进基准(pip_spec+pip_src);库组件恒等老口径
        let fp = closure_fingerprint(&searxng_spec());
        assert_eq!(fp.len(), 64);
        assert_ne!(
            fp,
            spec_fingerprint(SEARXNG_PIP_SPEC),
            "pip_src 必须进指纹基准"
        );
        assert_eq!(
            closure_fingerprint(&table_spec()),
            spec_fingerprint(TABLE_PIP_SPEC),
            "库组件闭包指纹与老口径恒等(老戳零迁移)"
        );
    }

    /// 状态载荷:components[] 服务条目带 kind:"service";库条目仍恰两键
    /// (skip_serializing_if——老前端宽容忽略附加键,两键契约零破)。
    #[test]
    fn component_statuses_add_kind_for_service_rows_only() {
        let data = tempfile::tempdir().expect("数据根临时目录创建失败");
        let resource = tempfile::tempdir().expect("资源临时目录创建失败");
        write_registry(
            resource.path(),
            &serde_json::to_string(&serde_json::json!({ "components": [
                serde_json::to_value(table_spec()).unwrap(),
                serde_json::to_value(searxng_spec()).unwrap(),
            ] }))
            .unwrap(),
        );
        let status = crate::pyenv::status_at(
            data.path(),
            Some(resource.path()),
            None,
            &crate::pyenv::PyenvSettings::default(),
        );
        let rendered = serde_json::to_value(&status).unwrap();
        assert_eq!(
            rendered["components"],
            serde_json::json!([
                { "id": "table", "installed": false },        // 库条目:恰两键
                { "id": "searxng", "installed": false, "kind": "service" },
            ]),
            "服务条目带 kind:service;库条目 wire 形不变"
        );
    }

    /// settings.yml 生成器:两行关键覆盖 + 随机 secret;幂等(已有不覆盖,
    /// secret 不轮换;删文件 = 显式重置,新 secret 不同);坏 secret 形态
    /// (非 hex)不产生——random_secret_key 恒 64 位小写 hex。
    #[test]
    fn searxng_settings_generator_shape_secret_stability_and_idempotence() {
        let yaml = searxng_settings_yaml(&"a".repeat(64));
        for needle in [
            "use_default_settings: true",
            "formats:",
            "- html",
            "- json",
            "secret_key:",
        ] {
            assert!(yaml.contains(needle), "settings.yml 缺关键覆盖 {needle}: {yaml}");
        }
        assert!(
            yaml.contains(&format!("secret_key: \"{}\"", "a".repeat(64))),
            "secret 须带引号落形(yaml 字符串边界): {yaml}"
        );
        // 随机源:64 位 hex 且两次调用不同(searxng 拒缺省 ultrasecretkey 起服务)
        let secret_a = random_secret_key();
        let secret_b = random_secret_key();
        assert_eq!(secret_a.len(), 64);
        assert!(secret_a
            .chars()
            .all(|c| c.is_ascii_hexdigit() && !c.is_ascii_uppercase()));
        assert_ne!(secret_a, secret_b, "两次生成必须不同(强随机)");

        // 落盘幂等:ensure 两回同一路径且内容不变;删文件后重生成换新 secret
        let data = tempfile::tempdir().expect("数据根临时目录创建失败");
        let first = ensure_searxng_settings(data.path()).expect("首次生成失败");
        assert_eq!(
            first,
            service_dir(data.path(), "searxng").join("settings.yml")
        );
        let first_text = std::fs::read_to_string(&first).expect("settings.yml 不可读");
        assert!(first_text.contains("use_default_settings: true"));
        let second = ensure_searxng_settings(data.path()).expect("幂等二跑失败");
        assert_eq!(second, first);
        assert_eq!(
            std::fs::read_to_string(&second).unwrap(),
            first_text,
            "已有文件不得覆盖(secret 不轮换)"
        );
        std::fs::remove_file(&first).unwrap();
        let third_text =
            std::fs::read_to_string(ensure_searxng_settings(data.path()).unwrap()).unwrap();
        assert_ne!(third_text, first_text, "删文件 = 显式重置(新 secret)");
    }

    /// env 占位符解析:{service_dir} → 服务数据目录绝对路径(注册表声明保持
    /// 数据根无关);无占位符值原样透传。
    #[test]
    fn service_env_placeholder_resolves_to_service_dir() {
        let data = tempfile::tempdir().expect("数据根临时目录创建失败");
        let dir = service_dir(data.path(), "searxng");
        assert_eq!(
            resolve_service_env_value("{service_dir}/settings.yml", &dir),
            dir.join("settings.yml").to_string_lossy().to_string()
        );
        assert_eq!(
            resolve_service_env_value("http://127.0.0.1:8888", &dir),
            "http://127.0.0.1:8888"
        );
    }

    /// 服务状态戳:读写回环;坏文件/路径逃逸形 id 拒读(与组件指纹戳同款
    /// 防御与宽容口径)。
    #[test]
    fn service_stamp_roundtrip_and_defensive_paths() {
        let data = tempfile::tempdir().expect("数据根临时目录创建失败");
        assert!(read_service_stamp(data.path(), "searxng").is_none(), "缺戳 = None");
        let stamp = ServiceStamp {
            state: Some("running".into()),
            pid: Some(4242),
            started_at: Some(1730000000),
            last_exit: None,
        };
        write_service_stamp(data.path(), "searxng", &stamp);
        assert_eq!(read_service_stamp(data.path(), "searxng"), Some(stamp));
        std::fs::create_dir_all(data.path().join(COMPONENTS_STAMP_DIR)).unwrap();
        std::fs::write(service_stamp_path(data.path(), "searxng"), "{ broken").unwrap();
        assert!(
            read_service_stamp(data.path(), "searxng").is_none(),
            "坏戳宽容为 None(不拦启停)"
        );
        assert!(read_service_stamp(data.path(), "../escape").is_none());
        assert!(service_stamp_path(data.path(), "a/b")
            .starts_with(data.path().join(COMPONENTS_STAMP_DIR)));
    }

    /// 健康探测(reqwest 阻塞栈):2xx = true;404/非 2xx = false;连接拒绝
    /// (端口无人听)= false 即时(本地手写 HTTP/1.0 服务器,惯例同
    /// pyenv_install 链单测的下载桩)。
    #[test]
    fn health_probe_classifies_2xx_as_healthy_and_refusals_as_down() {
        use std::io::{Read, Write};
        let serve = std::net::TcpListener::bind("127.0.0.1:0").expect("测试服务器绑定失败");
        let addr = serve.local_addr().expect("端口解析失败");
        std::thread::spawn(move || {
            for conn in serve.incoming() {
                let mut conn = match conn {
                    Ok(c) => c,
                    Err(_) => break,
                };
                let _ = conn.set_read_timeout(Some(Duration::from_secs(5)));
                let mut seen = Vec::new();
                let mut buf = [0u8; 1024];
                while !seen.ends_with(b"\r\n\r\n") && seen.len() < 8192 {
                    match conn.read(&mut buf) {
                        Ok(0) | Err(_) => break,
                        Ok(n) => seen.extend_from_slice(&buf[..n]),
                    }
                }
                let path = String::from_utf8_lossy(&seen)
                    .lines()
                    .next()
                    .unwrap_or_default()
                    .to_string();
                let (code, body) = match path.as_str() {
                    "GET /ok HTTP/1.1" => ("200 OK", "OK"),
                    "GET /old HTTP/1.1" => ("404 Not Found", "gone"),
                    _ => ("500 Internal Server Error", "boom"),
                };
                let _ = conn.write_all(
                    format!(
                        "HTTP/1.0 {code}\r\nContent-Length: {}\r\nConnection: close\r\n\r\n{body}",
                        body.len()
                    )
                    .as_bytes(),
                );
                let _ = conn.flush();
                let _ = conn.shutdown(std::net::Shutdown::Both);
            }
        });
        assert!(probe_health_url(&format!("http://{addr}/ok")));
        assert!(!probe_health_url(&format!("http://{addr}/old")));
        assert!(!probe_health_url(&format!("http://{addr}/boom")));
        let dead = std::net::TcpListener::bind("127.0.0.1:0").unwrap();
        let dead_addr = dead.local_addr().unwrap();
        drop(dead); // 立即释放 = 该端口无人听(连接拒绝)
        assert!(!probe_health_url(&format!("http://{dead_addr}/healthz")));
    }

    /// searxng 两段装安装链(sh 桩 python):一段闭包(-r requirements URL
    /// + granian + setuptools/wheel)→ 二段 --no-build-isolation 装 pip_src
    /// 直引 spec → ready 戳指纹基准 = 闭包两段(pip_spec+pip_src)。
    /// 二段失败如实翻 error(重试幂等);钩子配套字段缺失零子进程拒。
    #[cfg(unix)]
    mod searxng_install {
        use super::*;

        /// searxng 组件装(段序断言依赖桩把两段 pip 分别记账)。fail_src =
        /// 一段成功后二段失败(验证 error 态如实、不静默)。
        fn install_searxng(dir: &Path, python: &Path, fail_src: bool) -> ComponentInstallOutcome {
            std::fs::remove_file(dir.join("pip-fail-marker")).ok();
            if fail_src {
                std::fs::write(dir.join("src-fail-marker"), b"1").unwrap();
            } else {
                std::fs::remove_file(dir.join("src-fail-marker")).ok();
            }
            install_component(dir, python, &searxng_spec(), None, 1024 * 1024)
        }

        /// 一段闭包 pip 记账行(既有 pip-invocations.log 里的闭包装)。
        fn closure_pip_line(dir: &Path) -> String {
            pip_log(dir)
                .into_iter()
                .find(|line| line.contains("-r "))
                .expect("一段闭包 pip 必须留痕(含 -r requirements URL)")
        }

        /// 二段源码包 pip 记账行(pip-src-invocations.log;桩按
        /// --no-build-isolation flag 路由)。
        fn src_pip_lines(dir: &Path) -> Vec<String> {
            std::fs::read_to_string(dir.join("pip-src-invocations.log"))
                .map(|text| text.lines().map(String::from).collect())
                .unwrap_or_default()
        }

        #[test]
        fn success_installs_closure_then_src_and_stamps_closure_fingerprint() {
            let dir = tempfile::tempdir().expect("临时目录创建失败");
            let python = stub_python(dir.path());
            let outcome = install_searxng(dir.path(), &python, false);

            assert_eq!(
                outcome,
                ComponentInstallOutcome {
                    id: "searxng".into(),
                    installed: true,
                    error: None
                }
            );
            // 一段闭包:-r 上游 commit 钉版 requirements URL + granian + 构建后端
            let closure = closure_pip_line(dir.path());
            assert!(closure.contains("-m pip install"), "实际: {closure}");
            assert!(
                closure.contains("-r https://raw.githubusercontent.com/searxng/searxng/d48c4b555421e824342c51d68482dd0898e54d0f/requirements.txt")
                    && closure.contains("granian==2.8.3")
                    && closure.contains("setuptools")
                    && closure.contains("wheel"),
                "一段闭包须四件齐(实测两段装口径): {closure}"
            );
            // 二段源码包:--no-build-isolation + git 直引 commit 钉 spec
            let src_lines = src_pip_lines(dir.path());
            assert_eq!(src_lines.len(), 1, "二段源码包恰一次: {src_lines:?}");
            assert!(
                src_lines[0].contains("--no-build-isolation")
                    && src_lines[0].contains(SEARXNG_PIP_SRC),
                "二段装 = --no-build-isolation + pip_src 直引: {}",
                src_lines[0]
            );
            assert!(
                src_lines[0]
                    .split_whitespace()
                    .position(|t| t == SEARXNG_PIP_SRC)
                    .unwrap_or(0)
                    > src_lines[0]
                        .split_whitespace()
                        .position(|t| t == "--no-build-isolation")
                        .unwrap_or(1),
                "flag 应在 spec 之前(argv 组装序): {}",
                src_lines[0]
            );
            // ready 戳:指纹基准 = 闭包两段(pip_spec+pip_src)
            let stamp = read_component_stamp(dir.path(), "searxng").expect("成功应落戳");
            assert_eq!(stamp.state.as_deref(), Some("ready"));
            assert_eq!(
                stamp.fingerprint.as_deref(),
                Some(closure_fingerprint(&searxng_spec()).as_str())
            );
            assert!(is_component_installed(dir.path(), &searxng_spec()));
            // 闭包漂移引导:任一段变脸(pip_src 升 commit)→ 未装
            let drifted = ComponentSpec {
                pip_src: Some("searxng@git+https://github.com/searxng/searxng.git@1111111111111111111111111111111111111111".into()),
                ..searxng_spec()
            };
            assert!(!is_component_installed(dir.path(), &drifted));
        }

        #[test]
        fn src_phase_failure_stamps_error_after_closure_success() {
            let dir = tempfile::tempdir().expect("临时目录创建失败");
            let python = stub_python(dir.path());
            let outcome = install_searxng(dir.path(), &python, true);

            assert!(!outcome.installed);
            let error = outcome.error.expect("二段失败应带明细");
            assert!(error.starts_with("pip_failed: "), "复用可重试分类: {error}");
            assert!(error.contains("stub src pip boom"), "输出尾部应回显: {error}");
            assert!(
                !src_pip_lines(dir.path()).is_empty(),
                "一段闭包成功 + 二段失败各留痕"
            );
            let stamp = read_component_stamp(dir.path(), "searxng").expect("失败也应落戳");
            assert_eq!(stamp.state.as_deref(), Some("error"));
            assert_eq!(
                stamp.fingerprint,
                None,
                "失败不落指纹(防误判已装)"
            );
            assert!(!is_component_installed(dir.path(), &searxng_spec()));
        }

        /// 钩子配套字段缺失(pip-src-no-build-isolation 无 pip_src)→
        /// 契约校验先于一切子进程,零 pip/零源码段副作用。
        #[test]
        fn src_hook_without_pip_src_field_rejected_without_spawning() {
            let dir = tempfile::tempdir().expect("临时目录创建失败");
            let python = stub_python(dir.path());
            let malformed = ComponentSpec {
                pip_src: None,
                ..searxng_spec()
            };
            let outcome = install_component(dir.path(), &python, &malformed, None, 1024 * 1024);

            assert!(!outcome.installed);
            let error = outcome.error.expect("契约漂移应带明细");
            assert!(error.contains("需要非空 pip_src 字段"), "实际: {error}");
            assert!(
                pip_log(dir.path()).is_empty() && src_pip_lines(dir.path()).is_empty(),
                "契约校验先于一切子进程(零闭包/零源码段 pip)"
            );
            let stamp = read_component_stamp(dir.path(), "searxng").expect("拒也应落戳");
            assert_eq!(stamp.state.as_deref(), Some("error"));
        }
    }

    // —— 服务启停生命周期真跑(unix;sh 桩服务进程 + 本地 HTTP 健康桩)——
    #[cfg(unix)]
    mod service_lifecycle {
        use super::*;
        use std::io::{Read, Write};

        /// 本地健康桩服务器(手写 HTTP/1.0;/healthz 恒 200 OK;惯例同
        /// pyenv_install 链单测的下载桩,零新依赖)。
        fn start_health_server() -> std::net::SocketAddr {
            let serve =
                std::net::TcpListener::bind("127.0.0.1:0").expect("健康桩绑定失败");
            let addr = serve.local_addr().expect("健康桩端口解析失败");
            std::thread::spawn(move || {
                for conn in serve.incoming() {
                    let mut conn = match conn {
                        Ok(c) => c,
                        Err(_) => break,
                    };
                    let _ = conn.set_read_timeout(Some(Duration::from_secs(5)));
                    let mut seen = Vec::new();
                    let mut buf = [0u8; 2048];
                    while !seen.ends_with(b"\r\n\r\n") && seen.len() < 8192 {
                        match conn.read(&mut buf) {
                            Ok(0) | Err(_) => break,
                            Ok(n) => seen.extend_from_slice(&buf[..n]),
                        }
                    }
                    let body = "OK";
                    let _ = conn.write_all(
                        format!(
                            "HTTP/1.0 200 OK\r\nContent-Length: {}\r\n\
                             Connection: close\r\n\r\n{}",
                            body.len(),
                            body
                        )
                        .as_bytes(),
                    );
                    let _ = conn.flush();
                    let _ = conn.shutdown(std::net::Shutdown::Both);
                }
            });
            addr
        }

        /// sh 桩服务进程:-m granian argv → 记录 env/argv/PPID 到
        /// service-spawn.log 后常驻(sleep;SIGTERM 默认语义即退);在场
        /// svc-exit-marker 即刻退出非零码(启动即死用例)。非 granian argv
        /// 即失败(意外 argv 不许冒充服务)。
        fn stub_service_python(dir: &Path) -> PathBuf {
            let log = dir.join("service-spawn.log");
            let fail = dir.join("svc-exit-marker");
            let bin = dir.join("python3");
            let script = format!(
                "#!/bin/sh\n\
                 if [ \"$1\" = \"-m\" ] && [ \"$2\" = \"granian\" ]; then\n\
                 \x20 printf 'argv=%s\\nSEARXNG_SETTINGS_PATH=%s\\n' \"$*\" \"$SEARXNG_SETTINGS_PATH\" >> '{}'\n\
                 \x20 printf 'PYTHONPATH=%s\\n' \"${{PYTHONPATH:-<unset>>}}\" >> '{}'\n\
                 \x20 if [ -f '{}' ]; then echo 'stub service instant death' >&2; exit 78; fi\n\
                 \x20 while :; do sleep 5; done\n\
                 fi\n\
                 exit 1\n",
                log.display(),
                log.display(),
                fail.display(),
            );
            std::fs::write(&bin, script).expect("桩服务 python 写入失败");
            use std::os::unix::fs::PermissionsExt;
            std::fs::set_permissions(&bin, std::fs::Permissions::from_mode(0o755))
                .expect("桩服务 python 置可执行位失败");
            bin
        }

        /// 壳外孤儿桩(复刻壳重启前拉起的进程:process_group(0) ⇒ 自立组长
        /// ——spawn_service_process 的进程组面必须一致,组信号才有锚点;
        /// stdio 全 null 防测试管道被残留桩持有)。
        fn orphan_stub(python: &Path) -> std::process::Child {
            use std::os::unix::process::CommandExt;
            use std::process::{Command, Stdio};
            Command::new(python)
                .args(["-m", "granian", "--interface", "wsgi", "searx.webapp:app"])
                .stdin(Stdio::null())
                .stdout(Stdio::null())
                .stderr(Stdio::null())
                .process_group(0)
                .spawn()
                .expect("孤儿桩拉起失败")
        }

        fn spawn_log(dir: &Path) -> String {
            std::fs::read_to_string(dir.join("service-spawn.log")).unwrap_or_default()
        }

        /// searxng 条目(health_url 指向本地健康桩端口;其余与随包注册表同源)。
        fn searxng_spec_on(health_addr: &std::net::SocketAddr) -> ComponentSpec {
            ComponentSpec {
                service: Some(ServiceSpec {
                    health_url: format!("http://{health_addr}/healthz"),
                    ..searxng_spec()
                        .service
                        .expect("searxng_spec 恒带 service 节")
                }),
                ..searxng_spec()
            }
        }

        /// 成功链:pre_start 生成 settings.yml → spawn(新进程组,env 占位符
        /// 已解析成服务目录绝对路径,PYTHONPATH 剥离,日志落数据根)→ 状态戳
        /// running → 健康等待过(健康桩 200)→ 回 running+healthy=true+句柄。
        #[test]
        fn start_generates_settings_spawns_group_and_reaches_healthy() {
            let dir = tempfile::tempdir().expect("临时目录创建失败");
            let python = stub_service_python(dir.path());
            let health = start_health_server();
            let spec = searxng_spec_on(&health);

            let (status, child) = start_service_process(dir.path(), &python, &spec)
                .expect("桩服务启动应成功");

            assert_eq!(status.state, "running");
            assert!(status.healthy, "健康桩 200 → healthy=true");
            let pid = status.pid.expect("running 必带 pid");
            assert_eq!(status.id, "searxng");
            assert!(status.started_at.is_some());
            // pre_start:settings.yml 已生成且 secret 随机
            let settings =
                std::fs::read_to_string(service_dir(dir.path(), "searxng").join("settings.yml"))
                    .expect("settings.yml 应已生成");
            assert!(settings.contains("use_default_settings: true"));
            // spawn 面:argv/env/PYTHONPATH 三锚点
            let log = spawn_log(dir.path());
            assert!(log.contains("-m granian"), "argv 透传: {log}");
            assert!(
                log.contains(&format!(
                    "SEARXNG_SETTINGS_PATH={}",
                    service_dir(dir.path(), "searxng").join("settings.yml").to_string_lossy()
                )),
                "env 占位符必须解析为服务目录绝对路径: {log}"
            );
            assert!(
                log.contains("PYTHONPATH=<unset>>"),
                "PYTHONPATH 必须剥干净(Req 4): {log}"
            );
            // 日志文件已建(数据根服务目录下)
            assert!(service_dir(dir.path(), "searxng").join("service.log").is_file());
            // 状态戳:running + pid + started_at
            let stamp =
                read_service_stamp(dir.path(), "searxng").expect("启动后应落状态戳");
            assert_eq!(stamp.state.as_deref(), Some("running"));
            assert_eq!(stamp.pid, Some(pid));
            assert_eq!(stamp.started_at, status.started_at);
            // 进程组:pgid == pid(process_group(0) ⇒ 自立组;整组停的锚点)
            let group = service_group_alive(pid);
            assert!(group, "服务进程组应存活");
            // 收尾:交停服核心回收,零残留
            let stopped = stop_service_process(dir.path(), &python, &spec, Some(child))
                .expect("停服应成功");
            assert_eq!(stopped.state, "stopped");
            assert!(!service_group_alive(pid), "停后组内零存活");
            let stamp = read_service_stamp(dir.path(), "searxng").unwrap();
            assert_eq!(stamp.state.as_deref(), Some("stopped"));
            assert!(stamp.last_exit.is_some(), "亲生句柄应能观测退出: {:?}", stamp.last_exit);
        }

        /// 启动即死:进程退出码回显 + 状态戳 stopped+last_exit;不误报 running。
        #[test]
        fn start_failure_when_process_dies_immediately_records_exit_code() {
            let dir = tempfile::tempdir().expect("临时目录创建失败");
            let python = stub_service_python(dir.path());
            std::fs::write(dir.path().join("svc-exit-marker"), b"1").unwrap();
            let health = start_health_server();
            let spec = searxng_spec_on(&health);

            let err = start_service_process(dir.path(), &python, &spec)
                .expect_err("启动即死应结构化失败");
            assert!(
                err.contains("启动后即退出") && err.contains("78"),
                "退出码应回显: {err}"
            );
            assert!(
                err.contains("service.log"),
                "失败明细应指向日志路径: {err}"
            );
            let stamp =
                read_service_stamp(dir.path(), "searxng").expect("死亡也应落状态戳");
            assert_eq!(stamp.state.as_deref(), Some("stopped"));
            assert_eq!(stamp.last_exit, Some(78));
        }

        /// 状态对账三态:①亲生句柄在 → running+健康探测;②句柄死(被外部杀)
        /// → try_wait 回收退出码,戳纠偏 stopped;③无句柄(壳重启态)按戳
        /// pid 探活——活 = running(孤儿,状态记忆),死 = 戳纠偏 stopped。
        #[test]
        fn reconcile_covers_owned_alive_owned_dead_and_orphan_stamp_states() {
            let dir = tempfile::tempdir().expect("临时目录创建失败");
            let python = stub_service_python(dir.path());
            let health = start_health_server();
            let spec = searxng_spec_on(&health);

            // ①亲生活:running + healthy(健康桩)
            let (_, mut child) = start_service_process(dir.path(), &python, &spec).unwrap();
            let pid = child.id();
            let status = reconcile_service_status(
                dir.path(),
                &spec,
                Some(&mut child),
                read_service_stamp(dir.path(), "searxng").map(|s| s.started_at).flatten(),
            )
            .unwrap();
            assert_eq!(status.state, "running");
            assert!(status.healthy);
            assert_eq!(status.pid, Some(pid));
            // ②外部杀掉 → 对账回收退出码(信号死者记 -signal)并纠偏戳
            // (TERM → 进程死亡有毫秒级窗口,对账前先等死亡落定——对账语义
            //  仍是「探测瞬间的真相」,这里只是不让测试跟窗口赛跑)
            terminate_service(pid);
            let deadline = Instant::now() + Duration::from_secs(5);
            while matches!(child.try_wait(), Ok(None)) && Instant::now() < deadline {
                std::thread::sleep(Duration::from_millis(50));
            }
            let status =
                reconcile_service_status(dir.path(), &spec, Some(&mut child), None).unwrap();
            assert_eq!(status.state, "stopped");
            let signal = status.last_exit.expect("信号死者应记 -signal");
            assert!(signal < 0, "SIGTERM 死者记 -15 惯例: {signal}");
            let stamp = read_service_stamp(dir.path(), "searxng").unwrap();
            assert_eq!(stamp.state.as_deref(), Some("stopped"));
            assert_eq!(stamp.last_exit, status.last_exit);

            // ③孤儿态:戳记 running + 活 pid(壳外拉起的同形桩)→ 无句柄对账
            //    running;再杀掉 → 戳纠偏 stopped
            let mut orphan = orphan_stub(&python);
            let orphan_pid = orphan.id();
            write_service_stamp(
                dir.path(),
                "searxng",
                &ServiceStamp {
                    state: Some("running".into()),
                    pid: Some(orphan_pid),
                    started_at: Some(1730000000),
                    last_exit: None,
                },
            );
            let status =
                reconcile_service_status(dir.path(), &spec, None, None).unwrap();
            assert_eq!(status.state, "running", "孤儿存活按戳如实回 running");
            assert!(status.healthy, "健康桩可及 → healthy");
            assert_eq!(status.pid, Some(orphan_pid));
            terminate_service(orphan_pid);
            let _ = orphan.wait();
            let status =
                reconcile_service_status(dir.path(), &spec, None, None).unwrap();
            assert_eq!(status.state, "stopped", "孤儿死后戳纠偏 stopped");
            let stamp = read_service_stamp(dir.path(), "searxng").unwrap();
            assert_eq!(stamp.state.as_deref(), Some("stopped"));
        }

        /// 停孤儿(壳重启后):ps argv 身份复核通过 → 组信号停,零残留;
        /// pid 被无关进程复用(argv 复核不过)→ 不动它,只转戳(防误杀)。
        #[test]
        fn stop_orphan_kills_verified_process_and_refuses_recycled_pid() {
            let dir = tempfile::tempdir().expect("临时目录创建失败");
            let python = stub_service_python(dir.path());
            let health = start_health_server();
            let spec = searxng_spec_on(&health);

            // 「孤儿」= 壳外 spawn 的同形桩(复刻壳重启前拉起的进程)
            let mut orphan = orphan_stub(&python);
            let orphan_pid = orphan.id();
            write_service_stamp(
                dir.path(),
                "searxng",
                &ServiceStamp {
                    state: Some("running".into()),
                    pid: Some(orphan_pid),
                    started_at: Some(1730000000),
                    last_exit: Some(0),
                },
            );
            // 身份复核:同形桩 → 过
            assert!(pid_command_matches_service(
                orphan_pid,
                &python,
                &searxng_spec().service.unwrap().start_cmd
            ));
            let stopped =
                stop_service_process(dir.path(), &python, &spec, None).unwrap();
            assert_eq!(stopped.state, "stopped");
            let _ = orphan.wait(); // 亲生父收尸(僵尸不算活进程;真实系统由 launchd 收)
            assert!(!service_group_alive(orphan_pid), "孤儿组零残留");
            // 跨会话退出码不可观测:保持上次已知值(不臆造)
            assert_eq!(stopped.last_exit, Some(0));

            // pid 复用形态:戳记 running 指向一个无关 sleep 进程 → 复核不过
            // → 不发组信号(进程活着走出停服),戳如实转 stopped
            let mut innocent = std::process::Command::new("/bin/sleep")
                .arg("30")
                .stdin(std::process::Stdio::null())
                .stdout(std::process::Stdio::null())
                .stderr(std::process::Stdio::null())
                .spawn()
                .expect("无关进程拉起失败");
            let innocent_pid = innocent.id();
            write_service_stamp(
                dir.path(),
                "searxng",
                &ServiceStamp {
                    state: Some("running".into()),
                    pid: Some(innocent_pid),
                    started_at: Some(1730000001),
                    last_exit: None,
                },
            );
            let stopped =
                stop_service_process(dir.path(), &python, &spec, None).unwrap();
            assert_eq!(stopped.state, "stopped", "戳如实转 stopped");
            // 无关进程必须活着走出(未被误杀)——退出码 9(sleep 被 TERM 杀
            // 则为 -15;显式 kill 后 wait 才可对账,此处只需「未死」)
            assert!(
                innocent.try_wait().unwrap().is_none(),
                "argv 复核不过的进程严禁发组信号(防 pid 复用误杀)"
            );
            let _ = innocent.kill();
            let _ = innocent.wait();
        }

        /// 幂等停:未在运行(无戳/戳 stopped)→ 直接回 stopped,零信号。
        #[test]
        fn stop_is_idempotent_when_not_running() {
            let dir = tempfile::tempdir().expect("临时目录创建失败");
            let python = stub_service_python(dir.path());
            let health = start_health_server();
            let spec = searxng_spec_on(&health);

            // 无戳
            let stopped = stop_service_process(dir.path(), &python, &spec, None).unwrap();
            assert_eq!(stopped.state, "stopped");
            assert_eq!(stopped.last_exit, None);
            // 戳 stopped(带历史退出码)
            write_service_stamp(
                dir.path(),
                "searxng",
                &ServiceStamp {
                    state: Some("stopped".into()),
                    pid: None,
                    started_at: None,
                    last_exit: Some(0),
                },
            );
            let stopped = stop_service_process(dir.path(), &python, &spec, None).unwrap();
            assert_eq!(stopped.last_exit, Some(0), "历史退出码原样保留");
        }

        /// 未知 pre_start 钩子:结构化拒且零子进程(注册表与壳版本漂移
        /// 不静默拉起半套服务)。
        #[test]
        fn unknown_pre_start_hook_rejected_without_spawning() {
            let dir = tempfile::tempdir().expect("临时目录创建失败");
            let python = stub_service_python(dir.path());
            let health = start_health_server();
            let bogus = ComponentSpec {
                pre_start: Some("bogus-generator".into()),
                ..searxng_spec_on(&health)
            };
            let err = start_service_process(dir.path(), &python, &bogus)
                .expect_err("未知钩子应拒");
            assert!(
                err.contains("未知 pre_start 钩子") && err.contains("bogus-generator"),
                "实际: {err}"
            );
            assert!(
                spawn_log(dir.path()).is_empty(),
                "契约校验先于一切子进程(零服务进程拉起)"
            );
            assert!(read_service_stamp(dir.path(), "searxng").is_none());
        }

        /// 装机态真跑(阶段2「真跑」门;#[ignore] 显式跑:环境由 bash 预备,
        /// MYIA_SEARXNG_SERVICE_SMOKE_ROOT 指向沙箱数据根——venv 在
        /// <root>/python/bin/python3,闭包已按注册表闭包装好;跑法见
        /// implement.jsonl 时间盒记录)。链路全真:真随包注册表(desktop/
        /// resources/components.json)→ pre_start 生成 settings.yml → 真启
        /// granian(新进程组)→ /healthz 200 → categories=web json 查询有
        /// 结果 → 停 → 进程组零残留。体积测量为 G-Q6 披露提供实测数。
        #[test]
        #[ignore = "真网真服务冒烟:MYIA_SEARXNG_SERVICE_SMOKE_ROOT=<沙箱数据根> cargo test -- --ignored --nocapture"]
        fn searxng_service_real_smoke_over_registered_lifecycle() {
            let Ok(root) = std::env::var("MYIA_SEARXNG_SERVICE_SMOKE_ROOT") else {
                panic!("真跑冒烟须设 MYIA_SEARXNG_SERVICE_SMOKE_ROOT=<沙箱数据根>(venv 在 <root>/python,闭包已装)");
            };
            let data_root = std::path::PathBuf::from(root);
            let python = crate::pyenv::python_bin_path(&data_root);
            assert!(
                python.exists(),
                "沙箱数据根缺 python 布局(应 <root>/python/bin/python3): {}",
                python.display()
            );
            // 真 registries:随包 components.json(桌面资源目录 = manifest_dir/../resources)
            let resource_dir = std::path::Path::new(env!("CARGO_MANIFEST_DIR"))
                .join("../resources");
            let registry = load_registry(Some(&resource_dir));
            let spec = registry
                .iter()
                .find(|e| e.id == "searxng")
                .expect("真注册表必须已有 searxng 服务条目")
                .clone();
            let svc = spec.service_spec().expect("searxng 条目必须是合法服务声明");
            eprintln!(
                "desktop-smoke: 真注册表条目就位(start_cmd={:?},health={})",
                svc.start_cmd, svc.health_url
            );

            // —— 起服务:pre_start 生成 settings.yml → spawn → 健康等待 ——
            let (status, child) = start_service_process(&data_root, &python, &spec)
                .expect("真服务启动应成功(granian 起来且 /healthz 转绿)");
            let pid = status.pid.expect("running 必带 pid");
            assert_eq!(status.state, "running");
            assert!(status.healthy, "装机态真跑门:健康端点必须转绿(20s 内)");

            // —— /healthz 直连对账(壳外视角同源)——
            assert!(
                probe_health_url(&svc.health_url),
                "probe_health_url 对真服务必须为 true"
            );

            // —— categories=web json 查询:真搜索、真上游引擎(实测弱网出口
            //    brave/google cse 常不可达,bing/ddg 系在——results 数量只断
            //    非零,引擎池构成不锁)——
            crate::pyenv_install::install_ring_provider_if_missing();
            let client = reqwest::blocking::Client::builder()
                .timeout(Duration::from_secs(90))
                .build()
                .expect("真跑查询客户端构建失败");
            // 查询参数手工 form-encode(桌面 reqwest 裁剪特性面无 .query();
            // 与引擎 searxng.py 的 urlencode 参数集逐项同源)
            let percent_encode = |input: &str| -> String {
                let mut out = String::new();
                for byte in input.as_bytes() {
                    if byte.is_ascii_alphanumeric() || matches!(byte, b'-' | b'_' | b'.' | b'~') {
                        out.push(*byte as char);
                    } else {
                        out.push_str(&format!("%{byte:02X}"));
                    }
                }
                out
            };
            let query = [
                ("q", "人工智能 监管"),
                ("format", "json"),
                ("language", "zh-CN"),
                ("safesearch", "1"),
                ("pageno", "1"),
                ("categories", "web"),
            ]
            .into_iter()
            .map(|(k, v)| format!("{}={}", k, percent_encode(v)))
            .collect::<Vec<_>>()
            .join("&");
            let resp = client
                .get(format!("http://127.0.0.1:8888/search?{query}"))
                .header("Accept-Language", "zh-CN,zh;q=0.9")
                .send()
                .expect("真搜索请求应可达(服务在跑)");
            assert_eq!(
                resp.status(),
                200,
                "json 接口必须 200(settings.yml 已开 json)"
            );
            let payload: serde_json::Value = resp.json().expect("json 应答可解析");
            let results = payload
                .get("results")
                .and_then(|v| v.as_array())
                .expect("results 数组必须在");
            let unresponsive = payload
                .get("unresponsive_engines")
                .and_then(|v| v.as_array())
                .map(|a| a.len())
                .unwrap_or(0);
            eprintln!(
                "desktop-smoke: 真查询落地 results={} 条(上游不可达引擎 {} 个)",
                results.len(),
                unresponsive
            );
            for result in results.iter().take(5) {
                eprintln!(
                    "  - {} | {}",
                    result.get("title").and_then(|t| t.as_str()).unwrap_or("?"),
                    result.get("url").and_then(|u| u.as_str()).unwrap_or("?")
                );
            }
            assert!(
                !results.is_empty(),
                "装机态真跑门:categories=web json 查询必须有结果(全灭=弱网出口上游全断,如实记,不造假)"
            );

            // —— 停服务:组信号 → 零残留 ——
            let stopped = stop_service_process(&data_root, &python, &spec, Some(child))
                .expect("停服应成功");
            assert_eq!(stopped.state, "stopped");
            assert!(
                stopped.last_exit.is_some(),
                "亲生句柄应能观测退出: {:?}",
                stopped.last_exit
            );
            assert!(
                !service_group_alive(pid),
                "真跑零残留门:进程组(含 granian worker 子进程)必须整组退出"
            );
            // 端口视角:8888 不再有人听
            let port_probe = std::net::TcpStream::connect("127.0.0.1:8888");
            assert!(
                port_probe.is_err(),
                "真跑零残留门:8888 必须释放(连接必拒)"
            );
            // 全系统视角:与沙箱根相关的 granian/searx 进程零残留(ps 扫描)
            let ps = std::process::Command::new("ps")
                .args(["-eo", "pid,command"])
                .output()
                .expect("ps 扫描失败");
            let ps_text = String::from_utf8_lossy(&ps.stdout).into_owned();
            let leaked: Vec<&str> = ps_text
                .lines()
                .filter(|line| {
                    line.contains("granian")
                        && line.contains(data_root.to_string_lossy().as_ref())
                })
                .collect();
            assert!(
                leaked.is_empty(),
                "真跑零残留门:沙箱根下 granian 进程须零残留(实得 {leaked:?})"
            );
            eprintln!(
                "desktop-smoke: 真启停全链收尾(零残留;last_exit={:?})",
                stopped.last_exit
            );

            // —— G-Q6 体积披露实测:闭包闭包闭包(venv 全量;uv venv 本体
            //    含解释器 ~40MB,closure ≈ 其余)——
            let du = std::process::Command::new("du")
                .arg("-sh")
                .arg(data_root.join("python"))
                .output();
            if let Ok(out) = du {
                eprintln!(
                    "desktop-smoke G-Q6 体积实测: venv 全量(含解释器)= {}",
                    String::from_utf8_lossy(&out.stdout).trim()
                );
            }
        }
    }
}
