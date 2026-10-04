# 桌面自管 Python 环境:包体不冻结,设置页按需下载

## Goal(主人指令,2026-10-05)

「这个软件自己创造一个 py 环境,打包时不应该将这个相关的 py 软件打入包体,让用户自己在设置里面自己下载。」

桌面端从 PyInstaller onefile 冻结 sidecar(118M,Python+依赖+模型全在包内)切换为 **MYStudio 已验证的自管环境模式**;grill 五问已全批(2026-10-05,主人「按照你的建议」+ 亲自钉定运行时 URL),决议如下。

## 决议(grill 2026-10-05 定案)

- **D1(交付形态)**:myssia 自有源码**随包**交付(纯 Python,轻,版本与壳严格配对);Python 运行时与第三方依赖**一律不进包**,运行期下载安装。
- **D2(首跑体验)**:引导空态——未配置时各依赖 sidecar 的屏显「Python 运行环境未配置」卡+一键跳设置;**不自动后台下载**(主人原话:让用户自己下载),配置动作 = 设置页显式点「开始配置」。
- **D3(运行时与依赖来源,主人钉 URL)**:运行时 = **indygreg/python-build-standalone `cpython-3.12.7+20241016`**,macOS 默认源 = 主人钦定
  `https://github.com/indygreg/python-build-standalone/releases/download/20241016/cpython-3.12.7+20241016-aarch64-apple-darwin-install_only.tar.gz`
  (Windows 取同 release 的 `x86_64-pc-windows-msvc-install_only` 等效件;mac 当前只发 aarch64,与现行 dmg 单架构一致)。依赖 = 环境内 `pip install` 按**锁版清单**(随包)。**双镜像可覆盖**:运行时包 URL、PyPI index 均可在设置页替换。
- **D4(更新解耦)**:壳更新(更新包骤降,不再含 Python)与依赖更新解耦;app 更新后依赖有漂移时,设置页出现「同步依赖」一键**幂等**重跑安装链,不强制自动。
- **D5(存量迁移)**:新版首启检测旧数据根——**数据零迁移**(myssia.db/plugins/models/keychain 全兼容沿用),仅提示「新版改为自管 Python 环境,需一次性配置」引导进设置;旧冻结二进制随 app 更新自然消失。
- **D6(后续件)**:表格还原等可选重件(前议)作为该环境的可选组件,环境立好后另行立档;vision extras 转设置开关进同一环境。

## Requirements

1. 包体剥离:安装包不含 Python 运行时/第三方依赖/内置 OCR 模型;含 myssia 源码、依赖锁版清单、sidecar 入口、运行时 sha256 校验清单。
2. 设置页「Python 运行环境」区块:开始配置/安装路径/使用路径/下载源(双镜像覆盖)/安装明细;下载→校验→解压→pip→自检全链状态可见,失败可重试。
3. Rust 壳拉起改造:sidecar spawn 从冻结二进制改为 `<数据根>/python/bin/python3 + 随包入口模块`;未配置时壳不 spawn,UI 走引导空态,协议层报「未配置」结构化状态。
4. 数据根布局:`<数据根>/python/`(install_only tar.gz 解压即得)与既有 `models/` 并排;绝不写安装目录/源码目录;开发 Python 与应用 Python 分家(MYStudio 铁律)。
5. 存量迁移与更新解耦按 D4/D5。

## Acceptance Criteria

- [ ] AC1 全新 mac 装机端到端:装包(包体显著小于 118M)→ 首启引导空态 → 设置「开始配置」→ 下载钉版运行时(默认 URL=D3)→ 校验+解压数据根 → pip 锁版装依赖 → sidecar 起活(version ping 过)→ 源管理/情报流/定时全功能;断网/坏包中途失败可重试续装
- [ ] AC2 未配置态:所有依赖 sidecar 的屏引导卡不崩溃;设置页显示路径/源/明细
- [ ] AC3 镜像覆盖:运行时 URL 与 PyPI index 均可设置覆盖并实测生效
- [ ] AC4 更新解耦:壳更新不含 Python;「同步依赖」幂等(重跑结果一致、已装跳过)
- [ ] AC5 存量迁移:旧数据根数据零丢失沿用,一次性引导出现且仅出现一次
- [ ] AC6 Windows 等效链(CI 门控;真机冒烟按 win-local-build 先例留主人侧)
- [ ] AC7 CLI/PyPI 发行通道零变化
- [ ] AC8 门禁:全量 pytest + vitest + tsc + tauri build 绿;装机冒烟+静默换装按交付纪律;docs zh/en getting-started 同步新安装叙事

## 非目标

- CLI 端发行形态不变;核心包依赖红线不动;不做运行时代码热更(仅环境与依赖管理);不做 mac x86_64 架构。
