# 技术设计——桌面自管 Python 环境

## 1. 架构总览(组件与数据流)

```
┌ Tauri 壳(Rust)───────────────────────────────┐
│ ① 环境探测:数据根/python 是否就绪(版本+依赖清单指纹) │
│ ② 未就绪 → 不 spawn,UI 空态事件(pyenv_not_ready)  │
│ ③ 就绪 → spawn <数据根>/python/bin/python3        │
│        -m myssia_desktop_entry(PYTHONPATH=随包源码)│
│ ④ 安装链执行器:下载→校验→解压→pip→自检(状态机+幂等) │
└──────────────────────────────────────────────┘
随包(Resources):myssia 源码 + 入口模块 + requirements-lock.txt + runtime-manifest.json
数据根:<MYIA_HOME>/python/(install_only 解压即得)/ models/(既有)/ db、plugins(既有)
```

## 2. 随包交付物

- `Resources/myssia-src/`:myssia 自有源码树(src/myssia + desktop 入口模块),纯 Python 零二进制;版本与壳同发同配对
- `Resources/runtime-manifest.json`:平台 → {url, sha256, 解压布局};macOS 条目 = 主人钉的 `cpython-3.12.7+20241016-aarch64-apple-darwin-install_only.tar.gz`(D3 原文);Windows = 同 release `x86_64-pc-windows-msvc-install_only` 等效件
- `Resources/requirements-lock.txt`:依赖锁版(pip `--require-hashes` 可选加强;来源 = pyproject dependencies 编译产物)
- 打包链变化:`build-sidecar.sh`/PyInstaller 链退役(档注保留一段历史说明);tauri.conf `externalBin` → `resources`;desktop-release.yml 去 sidecar 构建段;包体预估 15-25M 量级

## 3. 安装链(状态机 + 幂等)

`idle → downloading → verifying → extracting → installing_deps → selfcheck → ready | error(可重试)`

- 每步完成落 `<数据根>/python-env.json` 进度戳;重试跳过已完成步(幂等,D4)
- 下载:HTTPS + sha256 校验(manifest 钉版);镜像覆盖只换 URL,**不绕校验**
- 解压:install_only tar.gz 内即 `python/` 目录,解压落 `<数据根>/python/`;磁盘预检(需 ~500MB 余量)
- 依赖:spawn 新 python `-m pip install -r 随包锁版清单`(`--index-url` 取设置覆盖或缺省)
- 自检:起 sidecar 握手 version ping,过 → ready
- 错误分类结构化:network_failed / checksum_mismatch / disk_full / pip_failed / selfcheck_failed,设置页逐项可见可重试

## 4. 壳 spawn 与协议兼容

- spawn:`Command(<数据根>/python/bin/python3).args(["-m","myssia_desktop_entry"]).env(PYTHONPATH=Resources/myssia-src, MYIA_HOME=数据根)`;Windows 为 `python.exe`
- sidecar 协议**零改动**(version 门/方法面照旧);「环境就绪」是壳侧前置状态,不进协议
- 未配置态:壳不 spawn;UI 各屏按 `pyenv_not_ready` 渲染引导卡(D2)

## 5. 设置屏

「Python 运行环境」区块字段:开始配置按钮 / 安装路径 / Python 使用路径 / 运行时下载源(覆盖)/ PyPI 镜像(覆盖)/ 安装明细(状态机逐项)/ 同步依赖(D4,依赖漂移时出现)。IPC 走既有 settings 通道。

## 6. 存量迁移(D5)

首启检测:数据根存在旧版痕迹(db 非空等)且 `python-env.json` 不存在 → 一次性引导横幅(标记落盘,只出现一次);数据/模型/钥匙串零迁移。

## 7. 风险与边界

- 首跑必须联网(下载运行时+依赖)——D2 已认,引导文案明示离线不可用直至配置完成
- python-build-standalone 无代码签名(mac Gatekeeper:解压到数据根非隔离扩展属性,sha256 校验兜底完整性;Win 无 SmartScreen 面向非 exe 文件)
- 回滚:数据根布局不变,旧版包可直接回落重装,数据无损

## 8. 验证策略

- 单元:manifest 解析/状态机幂等/镜像覆盖逻辑(Rust+TS 双侧)
- 集成:本地起静态服务器供运行时 tar.gz(钉版文件本地化)全链真跑;坏 sha256/断网中断重试
- 端到端:AC1 全新沙箱数据根(`MYIA_HOME` 隔离)首跑到全功能;装机冒烟+静默换装按交付纪律
