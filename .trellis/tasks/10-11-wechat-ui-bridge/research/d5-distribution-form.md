# D5 组件分发形态——裁决执行档(随包源码 + pip_src 相对路径)

2026-10-12,主人「都解决」令执行。D5 三条路(prd.md:PyPI / 安装器 copy 形态 / 手装)之外的**正解路线**:随包源码 + `pip_src` 相对路径白名单解析到 tauri Resources——零 PyPI 发布纪律、零 git 凭据墙(git 直引对私有仓不可行)、复用 searxng 两段装先例的既有壳机制,安装器零新形态(copy 形态的 Rust+设置页工程量全免)。

## 落地面(全部已实现并验证)

1. **组件源码 pip 元数据**:`plugins/wechat-bridge/pyproject.toml`(新)——name `wechat-bridge`,version `0.3.0` 与 component.json/`__init__.__version__` 三方单源;主依赖 = 像素链 pyobjc(`pyobjc-framework-Quartz`/`-Vision`,>=12,<13,`sys_platform == 'darwin'` 标记,Windows 零拉)+ `pillow`(>=12,<13;uv.lock 实测 pyobjc 12.2.2/pillow 12.3.0 在窗内);sqlcipher3/pysqlcipher3 编译型绑定放 extras `[sqlcipher]` 刻意不入主链(现行解密走 sqlcipher CLI,brew install sqlcipher 前置写明 README/描述/pyproject 注释);console script `wechat-bridge = wechat_bridge.cli:main`;setuptools 后端 + 显式 `packages = ["wechat_bridge"]`(flat 布局 bin/ 在场,自动发现必歧义)。
2. **壳侧路径解析**:`desktop/src-tauri/src/pyenv_install.rs` `resolve_pip_src_spec` + `run_pip_src_no_build_isolation` 新参 `resource_dir`——远程直引(`://`/`git+`,searxng 形态)透传;相对路径白名单解析到 `<resource_dir>/components/<rel>`(`is_safe_relative` 拒绝对路径/`..`/空段;落点缺位结构化拒)——注册表是随包资产,无法借此装任意装机路径。常量 `COMPONENTS_SRC_RESOURCE_DIR = "components"`。
3. **安装链透传(最小改动)**:`pyenv_components.rs` `install_component` 增 `resource_dir: Option<&Path>` 形参并透传给二段钩子;IPC `pyenv_install_component` 传 `resource_dir.as_deref()`。两段装结构不动,6 处既有测试调用点补 `None`。
4. **注册表条目**:`desktop/resources/components.json` 增 `wechat-bridge` 行——`pip_spec: "setuptools>=75 wheel>=0.45"`(一段构建后端闭包,searxng 同款;像素链依赖随源码 pyproject 装,不引第三种钉版口径)、`pip_src: "wechat-bridge"`、`post_install: "pip-src-no-build-isolation"`、描述带就绪前置(brew sqlcipher/AX 授权)与 D4 语义(默认关+提权+exit 21)。
5. **随包映射**:`desktop/src-tauri/tauri.conf.json` resources 增 `"../../plugins/wechat-bridge": "components/wechat-bridge"`(整目录进包;`__pycache__` 由 beforeBuildCommand 清)。
6. **契约测试**:`tests/desktop/test_pyenv_resources.py` 增 4 测(源码映射+元数据在位 / 注册表行契约+披露锚点 / 全表 pip_src 白名单词形守门 / pyproject↔component.json↔__version__ 三方对齐+依赖面);Rust 增 5 测(`pip_src_resolution_whitelists_relative_under_resources_components`、`components_src_resource_dir_is_pinned`、`bundled_src_install` 两测经 install_component 真跑桩 python:相对路径解析到白名单根/穿越形 setup_failed 且 src 段零子进程)。

## 验证(2026-10-12 本机实跑)

- 契约:`uv run --no-sync python -m pytest tests/desktop/test_pyenv_resources.py -q` → **36 passed**;`tests/desktop -q` 全量 → **397 passed**。
- Rust:`cargo test`(desktop/src-tauri)→ **90 passed, 1 ignored**(新增 5 测在列);`cargo check` 零警告。
- 组件单测:`tests/wechat-bridge -q` → **168 passed, 7 skipped**(与 1453e65 基线持平);`ruff check` 全绿。
- **pip 装冒烟(独立 venv `/tmp/wechat-bridge-smoke`,uv venv --seed,零碰仓库 .venv)**:①一段 `pip install --no-input --disable-pip-version-check setuptools>=75 wheel>=0.45` → setuptools 84.0.0/wheel 0.48.0(3.12 的 uv seed 只带 pip,坐实一段闭包必要性);②二段 `pip install --no-input --disable-pip-version-check --no-build-isolation plugins/wechat-bridge` → Successfully installed(源码目录直接出 wheel,主依赖闭包自动解析:pyobjc-core/Cocoa/Quartz/CoreML/Vision 12.2.2 + pillow 12.3.0,全在钉窗内);③`wechat-bridge --probe`(MYIA_HOME 指临时目录)→ **exit 0,`{"state":"degraded","bridge_version":"0.3.0"}`,checks 七项齐**(wechat_process/ax_*/main_window/localdb_*/bridge_component;degraded 与本机在装 0.3.0 目录形态既有实况一致,如实),全程只读零激活。

## 与既有形态的关系

- 开发态/本机已装目录形态(`~/.myia/plugins/wechat-bridge/bin/wechat-bridge`,MYIA 侧 `DEFAULT_BRIDGE_BIN`)**零改动**:bin 启动器候选 2 本就选自管环境 python,包经组件链 pip 装进自管环境后 `python -m wechat_bridge` 照常可 import;`wechat_bridge_bin` 覆写可指向自管环境 console script(`<数据根>/python/bin/wechat-bridge`)。
- 新机器分发闭环 = 装壳(随包 Resources/components/wechat-bridge)→ 设置页装组件(两段装)→ 桥在自管环境;AC7 剩余仍只有主人 sudo 提权命令一条(prd.md,不在本轮)。
- impact 审计:`run_pip_src_no_build_isolation`/`install_component` 均 CRITICAL(上游全在本 crate:生产调用面各 1 个 + 测试),已全量改齐并由 `cargo test` 全绿收口。
