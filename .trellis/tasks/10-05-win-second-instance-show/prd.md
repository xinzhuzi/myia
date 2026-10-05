# Windows 二实例唤出静默主窗

## Goal

对运行中的 MYIA Windows 实例再次启动(双击图标 / open)时,唤出并聚焦第一实例已藏的主窗口;同时补上 Windows 侧的单实例门。补齐「Windows 发布包静默启动后无唤出路径」的交付级 UX 缺口。

## 背景(在案实证)

- 10-03-quiet-launch:发布包主窗口 `visible:false` 出厂(tauri.conf.json),亮窗三途径 = dev 构建 / `MYIA_SHOW_ON_START=1` / macOS Dock Reopen(`RunEvent::Reopen`,`#[cfg(target_os="macos")]`)。
- macOS 全链在位:flock 单实例门(`acquire_instance_lock`,锁落数据根)+ 二实例 `open -b` 转激活 + Reopen 亮窗。
- **Windows 三无**:无 Dock、无托盘、单实例锁是 macOS-only flock——普通 Windows 用户双击图标**永远看不到窗口**(10-05-win-local-build evidence §8 坑 4 真机实证);且现状 Windows 每次双击都会多起一个静默实例,连单实例语义都没有。
- Windows 是正式交付目标(10-04-windows-build,CI windows-msi job)。

## 决议

主人 2026-10-05 批准按推荐方向修:**二实例唤出**——对运行中实例再次启动时唤出并聚焦已藏主窗(而非 Windows 启动即亮窗或加托盘)。

## Requirements

- **R1 Windows 单实例 + 唤出**:第二实例启动 → 检测到已有实例 → 唤出并聚焦第一实例主窗(show + set_focus)→ 第二实例自退。采用官方 `tauri-plugin-single-instance`(Windows 命名 mutex + 窗口消息;回调在第一实例进程内执行)。
- **R2 macOS 零行为变化**:官方插件在 macOS 是空操作,现有 flock 单实例门 + `open -b` 转激活 + Reopen 亮窗链路原样保留,不叠加不替换。
- **R3 门控与依赖隔离**:插件注册与依赖声明均以 `cfg(target_os = "windows")` 门控(target-specific dependency,Cargo.toml 已有 macOS 同款先例);mac 上 `cargo check --locked` 必须仍绿。
- **R4 唤窗逻辑与 macOS Reopen 同源**:show + set_focus 收敛为同一函数,Windows 二实例回调与 macOS Reopen 分支行为严格一致。

## 约束

- 只动本任务文件(main.rs / Cargo.toml / Cargo.lock / 本任务档);不推远端、不打 tag;Windows msi 产物归 tag 驱动的 desktop-release 流,本任务不出包。

## Acceptance Criteria

- [ ] **AC1** Windows 语义:第二实例启动后不常驻(自退),第一实例主窗被唤出并聚焦。→ 代码面落地(729b8f2:官方插件 Windows 门控首位注册,回调 `show_main_window`);**行为面待 Windows 真机按 Notes 四步验证后勾**(mac 侧无法验证,如实留 owner)。
- [x] **AC2** mac 编译门禁绿:`cargo check --locked` Finished 绿 + `cargo test` **54 passed / 0 failed**(desktop/src-tauri,2026-10-05 亲跑);本机 rustup 仅 aarch64-apple-darwin,`cargo check --target x86_64-pc-windows-msvc` 留真机/CI(windows-msi 产物归 tag 驱动 desktop-release 流)。
- [x] **AC3** macOS 零回归:改后 main.rs 亲读核验——flock 门 / `open -b` 转激活 / Reopen 亮窗(改走 `show_main_window`,同调用序列)/ MYIA_SHOW_ON_START(同)/ MYIA_SMOKE_ROUTE(未动)语义均未变;Windows 插件注册整体在 `#[cfg(target_os = "windows")]` 内,mac 编译产物不含该代码。
- [x] **AC4** 单测:54 用例全绿零失败;本次改动无新增纯函数面(插件回调依赖 AppHandle,无法纯测),未硬凑——已如实注明。

## 实现回执(2026-10-05)

- **方案**:A = 官方 `tauri-plugin-single-instance` 2.5.2(Windows 命名 mutex + 窗口消息)。B(自造 Windows 锁 + 自造跨进程唤窗 IPC)弃:std 在 Windows 无 flock,且仓内无现成通道可指使旧实例 show,等于复刻官方插件下半截。
- **改动面**:`main.rs`(builder 首位 Windows 门控注册插件 + `show_main_window<R: Runtime>` 三路收敛:Reopen / 二实例回调 / 启动即显)、`Cargo.toml`(target-specific 依赖)、`Cargo.lock`(2.5.2 入锁)。
- **爆炸半径**:gitnexus impact `Function:desktop/src-tauri/src/main.rs:main` upstream 0 调用者 risk LOW(进程入口);detect-changes staged 报 high = 3 符号中 2 个为行号漂移 + 7 条流全 `Main →` 下游传染(入口必连),diff 亲证纯加 hunk。
- **提交**:代码笔 729b8f2(--only 三路径);本任务档另笔(见 task.json.commit 链)。
- **未尽**:Windows 真机验证(Notes 四步)留 owner;`docs/zh|en/build-windows.md` 无需更新(行为修复非构建链变化)。

## Notes(Windows 真机验证步骤,留 owner)

真机:Windows 11 家庭机(D:\dev\myia 已有构建环境,`D:\dev\winbuild-log\myia-show.cmd` 留机)。

1. 拉最新 main(或携本提交的分支),复刻 build-windows 文档链:`set "PATH=C:\Program Files\Git\bin;%PATH%"` + overlay productName + `npm ci`×2 + `build-sidecar.sh x86_64-pc-windows-msvc` + `npx tauri build --bundles msi`,或直接等 tag 驱动的 CI windows-msi 产物。
2. 安装 msi(或复用已装机升级),双击 myssia 图标:进程应静默启动无窗口(与现状一致)。
3. 再次双击 myssia 图标:主窗口应立即亮出并获得焦点;任务管理器确认 MYIA.exe 仍只有一个主进程(第二实例已自退,sidecar myssia-core 双进程形态属 PyInstaller onefile 正常形态,勿误判)。
4. 回归:macOS 侧 `open -a`/Dock Reopen 亮窗、二实例转激活行为不变(开发机日常使用即可覆盖)。
