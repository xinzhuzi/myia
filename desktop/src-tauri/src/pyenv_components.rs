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
//! - 护栏:未知组件 id / Python 未就位(先走「开始配置」)/ 主安装链在跑 /
//!   组件安装单飞(同刻只许一个 pip)→ 结构化拒绝;
//! - 卸载本期不做(档记后续):开关只管装与状态回读,已装件关档如实呈现。
//!
//! == 状态(pyenv_get_status 扩展;契约两键钉死)==
//! - `components: [{id, installed}]`(installed = 戳 ready 且指纹与当前注册
//!   表一致);载荷与 `pyenv-status-changed` 事件同源(pyenv::status_at 组装)。

use std::path::{Path, PathBuf};
use std::sync::Mutex;

use serde::{Deserialize, Serialize};
use sha2::{Digest, Sha256};
use tauri::{AppHandle, Manager};

/// 随包组件注册表资源文件名(tauri.conf resources 映射后位于 resource_dir 下)。
pub const COMPONENTS_RESOURCE_FILE: &str = "components.json";
/// 数据根下组件指纹目录名(逐组件一文件:`pyenv-components/<id>.json`)。
const COMPONENTS_STAMP_DIR: &str = "pyenv-components";

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

/// 组件已装判定:戳 ready 且指纹与当前注册表 pip_spec 一致(漂移 = 未装,
/// 设置屏引导重装;Python 缺位由整体状态 not_configured/error 另行呈现)。
pub fn is_component_installed(data_root: &Path, spec: &ComponentSpec) -> bool {
    let Some(stamp) = read_component_stamp(data_root, &spec.id) else {
        return false;
    };
    stamp.state.as_deref() == Some("ready")
        && stamp.fingerprint.as_deref() == Some(spec_fingerprint(&spec.pip_spec).as_str())
}

// ---------------------------------------------------------------------------
// 状态组装(pyenv_get_status 扩展;两键契约)
// ---------------------------------------------------------------------------

/// `pyenv_get_status.components[]` 单条(契约两键钉死:`{id, installed}`;
/// 展示文案(label/description)是前端展示层的事,注册表不在载荷里复述)。
#[derive(Clone, PartialEq, Eq, Debug, Serialize)]
pub struct ComponentStatus {
    pub id: String,
    pub installed: bool,
}

/// 组装 components[](注册表序;注册表缺位 → 空表)。pyenv::status_at 调用。
pub fn component_statuses(data_root: &Path, resource_dir: Option<&Path>) -> Vec<ComponentStatus> {
    load_registry(resource_dir)
        .into_iter()
        .map(|spec| ComponentStatus {
            installed: is_component_installed(data_root, &spec),
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

/// 组件安装(复用安装链依赖段):磁盘预检 → run_pip_spec(镜像索引透传)→
/// 指纹戳。成功落 ready+指纹;失败/中断落 error+明细(installed=false 如实)。
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
    if let Err((kind, detail)) = pyenv_install::disk_precheck(data_root, disk_required_bytes) {
        return fail(pyenv_install::render_error(kind, detail), None);
    }
    match pyenv_install::run_pip_spec(python_bin, &spec.pip_spec, index_url) {
        Ok(()) => {
            write_component_stamp(
                data_root,
                &spec.id,
                &ComponentStamp {
                    state: Some("ready".into()),
                    fingerprint: Some(spec_fingerprint(&spec.pip_spec)),
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

    fn table_spec() -> ComponentSpec {
        ComponentSpec {
            id: "table".into(),
            pip_spec: TABLE_PIP_SPEC.into(),
            label: "表格还原".into(),
            description: "截图表格还原成结构化 Markdown".into(),
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

        // description 缺省空串(宽容);未知附加字段忽略
        write_registry(
            resource.path(),
            &registry_json(serde_json::json!([{
                "id": "x", "pip_spec": "x==1", "label": "X", "extra": 1,
            }])),
        );
        assert_eq!(
            load_registry(Some(resource.path())),
            vec![ComponentSpec {
                id: "x".into(),
                pip_spec: "x==1".into(),
                label: "X".into(),
                description: String::new(),
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

    #[cfg(unix)]
    mod install {
        use super::*;

        /// sh 桩 python:pip 调用记账到日志,可控失败;非 pip argv 即失败。
        fn stub_python(dir: &Path) -> PathBuf {
            let log = dir.join("pip-invocations.log");
            let fail = dir.join("pip-fail-marker");
            let bin = dir.join("python3");
            let script = format!(
                "#!/bin/sh\n\
                 if [ \"$1\" = \"-m\" ] && [ \"$2\" = \"pip\" ]; then\n\
                 \x20 printf '%s\\n' \"$*\" >> '{}'\n\
                 \x20 if [ -f '{}' ]; then echo 'stub pip boom' >&2; exit 1; fi\n\
                 \x20 exit 0\n\
                 fi\n\
                 exit 1\n",
                log.display(),
                fail.display(),
            );
            std::fs::write(&bin, script).expect("桩 python 写入失败");
            use std::os::unix::fs::PermissionsExt;
            std::fs::set_permissions(&bin, std::fs::Permissions::from_mode(0o755))
                .expect("桩 python 置可执行位失败");
            bin
        }

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

        fn pip_log(data_root: &Path) -> Vec<String> {
            std::fs::read_to_string(data_root.join("pip-invocations.log"))
                .map(|text| text.lines().map(String::from).collect())
                .unwrap_or_default()
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
    }
}
