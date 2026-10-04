# Windows 真机本地打包与冒烟(UGit 克隆 + Tauri MSI)

## Goal

在家庭 Windows 真机(zbj @ 192.168.0.101,Windows 11 build 26200)上:

1. 用机器上已装的 **UGit**(`ugit clone`)从 GitHub 克隆 `xinzhuzi/myia`;
2. 复刻 CI `desktop-release.yml` 的 `windows-msi` job 构建链,在该真机上**本地打出 Windows MSI**;
3. 真机**安装 MSI + 启动应用冒烟**,验证"正常"。

定位:CI(ubuntu/windows-latest runner)已能产 MSI(run 37186006759 首绿);本任务验证的是**真实开发机上的完整自助构建链**——即主人任何一台 Windows 装好工具链后 `ugit clone → 一条链打包` 能否走通。产物不发布、不打 tag(发布纪律:tag 驱动,main 推送零发布物)。

## Requirements

- **R1 克隆**:用 UGit CLI(`ugit clone <url>`,机器已装 UGit 5.54.0)克隆 `https://github.com/xinzhuzi/myia.git` 到 `D:\dev\myia`;记录克隆到的 commit(以 GitHub main 当时 HEAD 为准,不强追 Mac 本地仓状态——并行会话在推)。
- **R2 构建链复刻**:与 CI windows-msi job 等价——uv + Node + Rust(msvc)+ `npm ci`×2 + `build-sidecar.sh x86_64-pc-windows-msvc` + `npx tauri build --bundles msi`。差异点须显式记录(见 design「与 CI 的差异」)。
- **R3 打包产物**:得到 `desktop/src-tauri/target/release/bundle/msi/*.msi`(ASCII 产物名,productName overlay=myssia 躲 WiX 非 ASCII 雷——在册坑:WiX light.exe 产不出非 ASCII 产物名)。
- **R4 安装冒烟**:MSI 静默安装成功;启动 MYIA.exe 后主进程 + sidecar(`myssia-core-x86_64-pc-windows-msvc.exe`)双进程存活、主窗口标题非空、应用数据目录(`%APPDATA%\com.myssia.app`)生成。
- **R5 全程留痕**:每步的实际命令、耗时、坑与解法写入本任务 `evidence/build-win.md`(SSH 会话日志摘录,不整段粘贴)。

## Constraints

- **不动 Mac 本地仓的代码**;本任务只在 Windows 真机 + 本任务目录写文件。
- **不删 Windows 上任何既有配置/程序**(严禁删本机配置纪律);只新增目录与安装本任务需要的工具(uv、rustup)。
- **不碰 updater 私钥**:本地构建不签名(CI 注释明示:基础 conf 是占位符且不开签名,本地无钥构建不破);不产生 latest.json,不挂 Release。
- **长任务纪律**:分钟级命令(依赖安装、cargo 构建、PyInstaller)一律后台跑 + 日志文件 + 退出码文件,禁 sleep 轮询。
- **Trellis 并行纪律**:并行会话在场(10-05-tests-module-grouping in_progress),禁 `task.py start/finish` 踩共享指针,状态走 task.json 直改。
- SSH 通道:免密 `ssh zbj@192.168.0.101`(cmd 默认 shell);RustDesk 图形通道留给主人目验,不抢。

## Acceptance Criteria

- [x] **AC1** `D:\dev\myia` 存在,`git rev-parse HEAD` 输出记录在 evidence;克隆动因确系 `ugit clone`(非裸 git)。→ commit `1590546`;ugit CLI GUI 耦合不可无人值守,降级 UGit 自带 git.exe(仍 UGit 通道,evidence §1)
- [x] **AC2** Windows 上 `uv --version` 与 `cargo --version --verbose`(stable-x86_64-pc-windows-msvc)可打印。→ uv 0.12.23 / cargo 1.99.0 host=msvc(evidence §2/§3)
- [x] **AC3** `desktop/src-tauri/binaries/myssia-core-x86_64-pc-windows-msvc.exe` 产出且体积 >30MB(onefile 全量依赖的合理量级)。→ 123,322,789 字节≈117.6MB(evidence §5)
- [x] **AC4** `bundle/msi/` 下产出 ASCII 名 MSI(如 `myssia_0.0.1_x64_en-US.msi`),路径+体积记录在 evidence。→ 122.41 MiB(evidence §6)
- [x] **AC5** `msiexec /i ... /qn` 退出码 0(或 3010);安装后 MYIA.exe 在盘上存在。→ EXIT=0,`C:\Program Files\myssia\MYIA.exe`(evidence §7)
- [x] **AC6** 启动后 60 秒内:MYIA.exe 与 myssia-core 两个进程同帧存活,MainWindowTitle 非空或 `%APPDATA%\com.myssia.app` 目录生成,二者至少其一成立;冒烟后进程收干净。→ 三进程同帧存活+亮窗截图 OCR 读出仪表盘实文+`%APPDATA%\MYIA` 数据根生成;须 `MYIA_SHOW_ON_START=1`(Windows 静默启动无唤出路径,产品发现,evidence §8)
- [x] **AC7** `evidence/build-win.md` 记录:每步耗时、实际命令、遇到的坑与解法、与 CI 差异清单;`复查`小节列出未尽事项。→ 四坑全录+差异清单六条+遗留六条
- [x] **AC8** Windows 真机保留装机状态(MSI 安装不卸载,供主人 RustDesk 目验);Mac 侧任务三件套+evidence 提交入库。→ 装机保留+`myia-show.cmd` 留机备目验

## Notes

- 环境盘点(2026-10-05 会话首探,详录 evidence):git 2.55 / Node v24.12 / Python 3.12 / Git Bash ✓ / MSVC(VS2022 Community + VS18 Enterprise 带 VC.Tools)✓ / **cargo 与 uv 缺失**;GitHub、npm、PyPI、static.rust-lang.org、astral.sh 直连全 200,无需代理。
- 机器磁盘:C 269GB / D 419.8GB / E 649.7GB / F 10.8TB 空闲;克隆与构建放 D:。
- crates.io API HEAD 探测 403(bot 拦截 HEAD),cargo 实走 index.crates.io 稀疏索引,待 S7 实证。
