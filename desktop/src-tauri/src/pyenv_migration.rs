//! 存量迁移引导(10-05-desktop-managed-py-env 第 6 步,D5/design §6)。
//!
//! 决议:新版首启检测旧数据根 —— **数据零迁移**(myssia.db/plugins/models/
//! keychain 全兼容沿用,prd D5),仅提示「新版改为自管 Python 环境,需一次性
//! 配置」引导进设置;旧冻结二进制随 app 更新自然消失。本模块只**检测与引导**,
//! 绝不改写任何存量数据(唯一落盘 = 引导标记文件,见下)。
//!
//! == 检测条件(design §6 字面)==
//! 数据根存在旧版痕迹(`myssia.db` 非空等)且 `python-env.json` 不存在
//! → 一次性引导横幅。条件短路:
//! - 旧版痕迹 = `myssia.db` 非空文件(entry.py:582 旧版 db 落点)或
//!   `plugins/` 非空(entry.py:574/583;品类 YAML 平铺 + 市场子目录)或
//!   `models/` 非空(entry.py:3184 视觉模型根)。0 字节 db 空壳不算痕迹
//!   (design §6「db 非空」字面);keychain 走系统钥匙串零落盘,无需检测。
//! - `python-env.json` 已存在 = 新版安装链已接管(配置中/已配置),不再引导。
//! - 引导标记已落盘 = 本引导出现过,永不复现(AC5「出现且仅出现一次」)。
//!
//! == 一次性语义(标记落盘,只出现一次)==
//! 命令 `pyenv_migration_banner` 是**查询即消费**:首次命中条件 → 落标记 +
//! 回 `show:true`;此后任何调用(含重启后)回 `show:false`。落标记原子写
//! (临时文件 + 同目录 rename,同 pyenv_install 进度戳惯例);写失败(数据根
//! 不可写 = 盘满/权限,该态下 sidecar/db 同样写不进,属致命盘况)→ 命令报错,
//! 前端不渲染横幅,下次启动重试——不牺牲「仅出现一次」换一次侥幸展示。
//! 标记判定按**文件存在性**(内容仅供排查):原子写下损坏即外部篡改,按已
//! 出现过处理,宁可少现不重现。

use std::path::{Path, PathBuf};

use crate::pyenv;
use serde::Serialize;
use tauri::AppHandle;

/// 旧版数据库落点(`<数据根>/myssia.db`,entry.py:582 home 模式 db 缺省)。
const LEGACY_DB_FILE: &str = "myssia.db";
/// 旧版插件目录(`<数据根>/plugins`,entry.py:574/583;品类 YAML + 市场子目录)。
const LEGACY_PLUGINS_DIR: &str = "plugins";
/// 旧版视觉模型根(`<数据根>/models`,entry.py:3184 home 模式模型落点)。
const LEGACY_MODELS_DIR: &str = "models";
/// 引导标记文件名(`<数据根>/pyenv-migration.json`;与 python-env.json/
/// pyenv-settings.json 同层,壳自有)。
const MIGRATION_MARKER_FILE: &str = "pyenv-migration.json";
/// 标记临时文件名(同目录 rename 原子写;惯例同 pyenv_install 进度戳)。
const MARKER_TMP_FILE: &str = ".pyenv-migration.json.tmp";

/// 引导标记路径(`<数据根>/pyenv-migration.json`)。
pub fn migration_marker_path(data_root: &Path) -> PathBuf {
    data_root.join(MIGRATION_MARKER_FILE)
}

// ---------------------------------------------------------------------------
// 检测(纯函数,单测主战场)
// ---------------------------------------------------------------------------

/// 目录非空(至少一个条目);不存在/不可读 = false。
fn dir_nonempty(dir: &Path) -> bool {
    std::fs::read_dir(dir)
        .map(|mut entries| entries.next().is_some())
        .unwrap_or(false)
}

/// 旧版痕迹在否(design §6「db 非空等」):myssia.db 非空文件 / plugins 非空 /
/// models 非空,任一命中即存量数据根。全新装机(空根或仅壳自有文件)不命中
/// —— 那是 D2 引导空态的领地,不是迁移引导的。
fn legacy_traces_present(data_root: &Path) -> bool {
    if let Ok(meta) = std::fs::metadata(data_root.join(LEGACY_DB_FILE)) {
        if meta.is_file() && meta.len() > 0 {
            return true;
        }
    }
    dir_nonempty(&data_root.join(LEGACY_PLUGINS_DIR))
        || dir_nonempty(&data_root.join(LEGACY_MODELS_DIR))
}

/// 引导标记已落盘否(按文件存在性;见模块注释一次性语义)。
fn marker_written(data_root: &Path) -> bool {
    migration_marker_path(data_root).exists()
}

/// 横幅该不该出现(design §6:旧痕迹 && python-env.json 不存在 && 未引导过)。
fn banner_due(data_root: &Path) -> bool {
    legacy_traces_present(data_root)
        && !pyenv::env_stamp_path(data_root).exists()
        && !marker_written(data_root)
}

/// 引导标记内容(排查用:何时出现过;判定只看文件存在性)。
#[derive(Serialize)]
struct MigrationMarker {
    banner_shown: bool,
    shown_at_unix: u64,
}

/// 落引导标记(原子写:临时文件 + 同目录 rename,惯例同安装链进度戳;
/// 数据根可能未建,先建目录 —— 与 pyenv::write_settings 同兜底)。
fn write_marker(data_root: &Path) -> std::io::Result<()> {
    std::fs::create_dir_all(data_root)?;
    let marker = MigrationMarker {
        banner_shown: true,
        shown_at_unix: std::time::SystemTime::now()
            .duration_since(std::time::UNIX_EPOCH)
            .map(|elapsed| elapsed.as_secs())
            .unwrap_or(0),
    };
    let text = serde_json::to_string_pretty(&marker).expect("引导标记序列化不可失败");
    let tmp = data_root.join(MARKER_TMP_FILE);
    std::fs::write(&tmp, text)?;
    std::fs::rename(&tmp, migration_marker_path(data_root))
}

/// 查询即消费(命令的纯核,单测直接打这里):命中条件 → 落标记 + true
/// (此后永不复现);否则 false。数据零触碰:唯一落盘 = 标记文件。
fn consume_banner(data_root: &Path) -> std::io::Result<bool> {
    if !banner_due(data_root) {
        return Ok(false);
    }
    write_marker(data_root)?;
    Ok(true)
}

// ---------------------------------------------------------------------------
// IPC 命令(第 6 步唯一新命令;载荷极简 {show: bool},横幅文案归前端)
// ---------------------------------------------------------------------------

/// `pyenv_migration_banner` 结果。
#[derive(Serialize)]
pub struct MigrationBannerDecision {
    pub show: bool,
}

/// 存量迁移一次性引导查询(D5/design §6):前端 AppLayout 挂载时调用一次。
/// 查询即消费 —— show:true 只会出现一次(标记落盘);之后(含重启)恒 false。
/// 数据根不可读/标记写失败 → Err(致命盘况,前端静默不渲染,见模块注释)。
#[tauri::command]
pub async fn pyenv_migration_banner(app: AppHandle) -> Result<MigrationBannerDecision, String> {
    let data_root = crate::data_root(&app).map_err(|e| e.to_string())?;
    let show = consume_banner(&data_root).map_err(|e| e.to_string())?;
    Ok(MigrationBannerDecision { show })
}

// ---------------------------------------------------------------------------
// 单测(门:implement.md 第 6 条「旧数据根夹具测试,数据零丢失断言」)
// ---------------------------------------------------------------------------

#[cfg(test)]
mod tests {
    use super::*;
    use std::collections::BTreeMap;

    /// 旧数据根夹具:还原真实存量布局 —— myssia.db(SQLite 头假体)+
    /// plugins/(品类 YAML 平铺 + 市场插件子目录,entry.py:535 互不干扰布局)+
    /// models/(视觉模型)+ 旧版伴随标记(`.seeded` entry.py:477 /
    /// `.instance.lock` 壳单实例锁)。返回夹具字节清单供零丢失比对。
    fn legacy_root(dir: &Path) -> BTreeMap<PathBuf, Vec<u8>> {
        let files: &[(&str, &[u8])] = &[
            ("myssia.db", b"SQLite format 3\x00--legacy-payload--"),
            ("plugins/tech.yaml", b"category: tech\ninterval: 1800\n"),
            (
                "plugins/market/hello/plugin.yaml",
                b"name: hello\nversion: 0.1.0\n",
            ),
            ("models/ocr/model.bin", b"\x00\x01model-bytes"),
            (".seeded", b""),
            (".instance.lock", b""),
        ];
        for (rel, bytes) in files {
            let path = dir.join(rel);
            std::fs::create_dir_all(path.parent().expect("夹具路径有父目录"))
                .expect("建夹具目录失败");
            std::fs::write(&path, bytes).expect("写夹具失败");
        }
        snapshot(dir)
    }

    /// 递归快照:相对路径 → 文件字节(零丢失断言的比对基线)。
    fn snapshot(root: &Path) -> BTreeMap<PathBuf, Vec<u8>> {
        fn walk(dir: &Path, prefix: &Path, out: &mut BTreeMap<PathBuf, Vec<u8>>) {
            for entry in std::fs::read_dir(dir).expect("快照读目录失败") {
                let entry = entry.expect("快照目录项失败");
                let rel = prefix.join(entry.file_name());
                let path = entry.path();
                if path.is_dir() {
                    walk(&path, &rel, out);
                } else {
                    out.insert(rel, std::fs::read(&path).expect("快照读文件失败"));
                }
            }
        }
        let mut out = BTreeMap::new();
        walk(root, Path::new(""), &mut out);
        out
    }

    /// 存量数据根 → 引导出现且仅出现一次(AC5 后半句;标记落盘钉死)。
    #[test]
    fn legacy_root_shows_banner_exactly_once() {
        let dir = tempfile::tempdir().expect("临时目录创建失败");
        legacy_root(dir.path());
        assert_eq!(consume_banner(dir.path()).unwrap(), true, "首次:出现");
        assert!(migration_marker_path(dir.path()).exists(), "标记已落盘");
        assert_eq!(consume_banner(dir.path()).unwrap(), false, "第二次:不现");
        // 模拟重启:新调用方同一数据根,仍不现
        assert_eq!(consume_banner(dir.path()).unwrap(), false, "重启后:仍不现");
    }

    /// 全新装机(空根)→ 不引导、不落标记(那是 D2 引导空态的领地);
    /// 壳自建文件(.instance.lock/pyenv-settings.json)同样不算旧痕迹。
    #[test]
    fn fresh_root_never_shows_and_writes_nothing() {
        let dir = tempfile::tempdir().expect("临时目录创建失败");
        assert_eq!(consume_banner(dir.path()).unwrap(), false);
        assert!(!migration_marker_path(dir.path()).exists(), "不落标记");

        // 壳启动自建伴随文件(单实例锁/镜像设置)+ 空 plugins 目录:仍不算存量
        std::fs::write(dir.path().join(".instance.lock"), b"").unwrap();
        std::fs::write(
            pyenv::pyenv_settings_path(dir.path()),
            r#"{"mirror_runtime": null}"#,
        )
        .unwrap();
        std::fs::create_dir(dir.path().join(LEGACY_PLUGINS_DIR)).unwrap();
        assert_eq!(
            banner_due(dir.path()),
            false,
            "空 plugins + 壳自有文件 ≠ 存量"
        );
        assert!(!migration_marker_path(dir.path()).exists());
    }

    /// python-env.json 已存在(新版安装链已接管:配置中/已配置/曾中断)→ 不引导。
    #[test]
    fn configured_root_skips_banner() {
        let dir = tempfile::tempdir().expect("临时目录创建失败");
        legacy_root(dir.path());
        std::fs::write(pyenv::env_stamp_path(dir.path()), r#"{"state":"ready"}"#).unwrap();
        assert_eq!(consume_banner(dir.path()).unwrap(), false);
        assert!(!migration_marker_path(dir.path()).exists());
    }

    /// 0 字节 db 空壳(设计字面「db 非空」)+ 空插件/模型 → 不算存量;
    /// 仅非空 db 一项即足以命中(等价清单的最小形态)。
    #[test]
    fn db_trace_requires_nonempty_file() {
        let dir = tempfile::tempdir().expect("临时目录创建失败");
        std::fs::write(dir.path().join(LEGACY_DB_FILE), b"").unwrap();
        assert!(!legacy_traces_present(dir.path()), "0 字节 db 不算痕迹");
        std::fs::write(dir.path().join(LEGACY_DB_FILE), b"SQLite format 3\x00").unwrap();
        assert!(legacy_traces_present(dir.path()), "非空 db 单项即命中");
        assert_eq!(consume_banner(dir.path()).unwrap(), true);
    }

    /// 标记内容形态:banner_shown 恒 true + unix 秒时间戳(判定只看存在性,
    /// 内容是排查线索;钉住防字段漂移)。
    #[test]
    fn marker_payload_shape() {
        let dir = tempfile::tempdir().expect("临时目录创建失败");
        legacy_root(dir.path());
        consume_banner(dir.path()).unwrap();
        let text = std::fs::read_to_string(migration_marker_path(dir.path())).unwrap();
        let value: serde_json::Value = serde_json::from_str(&text).unwrap();
        assert_eq!(value["banner_shown"], serde_json::json!(true));
        assert!(value["shown_at_unix"].as_u64().is_some(), "unix 秒时间戳在");
        // 无残留临时文件(原子写收尾干净)
        assert!(!dir.path().join(MARKER_TMP_FILE).exists());
    }

    /// 坏标记文件(外部篡改)按文件存在性 = 已出现过:宁可少现不重现。
    #[test]
    fn corrupt_marker_still_counts_as_shown() {
        let dir = tempfile::tempdir().expect("临时目录创建失败");
        legacy_root(dir.path());
        std::fs::write(migration_marker_path(dir.path()), "{ broken").unwrap();
        assert_eq!(consume_banner(dir.path()).unwrap(), false);
    }

    /// **门:数据零丢失断言**(implement.md 第 6 条门,prd D5「数据零迁移」)。
    /// 全量引导流转(检测 → 消费 → 落标记)后:旧 db/plugins/models 及伴随
    /// 文件逐字节原样;唯一新增 = 数据根层的引导标记,绝无任何写进
    /// plugins//models/ 或触碰 db/keychain 落点。
    #[test]
    fn legacy_data_zero_loss_through_banner_flow() {
        let dir = tempfile::tempdir().expect("临时目录创建失败");
        let before = legacy_root(dir.path());

        assert_eq!(consume_banner(dir.path()).unwrap(), true, "存量根首查出现");

        let after = snapshot(dir.path());
        // 1) 原有文件逐字节原样(零丢失)
        for (rel, bytes) in &before {
            assert_eq!(
                after.get(rel),
                Some(bytes),
                "存量文件被改写: {}",
                rel.display()
            );
        }
        // 2) 唯一新增 = 引导标记(数据根层);原有文件一个不少
        let added: Vec<&PathBuf> = after
            .keys()
            .filter(|rel| !before.contains_key(*rel))
            .collect();
        assert_eq!(
            added,
            vec![&PathBuf::from(MIGRATION_MARKER_FILE)],
            "唯一新增是引导标记,别无他物"
        );
        // 3) 引导流转不产生 python-env.json(那属安装链;本步只引导不配置)
        assert!(!pyenv::env_stamp_path(dir.path()).exists());
    }
}
