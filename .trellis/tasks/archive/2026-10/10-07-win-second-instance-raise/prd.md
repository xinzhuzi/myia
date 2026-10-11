# Windows 二实例唤出主窗(复核线)

## Goal

发布包 `visible:false` 出厂后,Windows 无 Dock 无托盘无 Reopen(macOS 限定),普通用户双击图标永无窗口——修此缺口。既定裁决留三方向(启动即 show / 托盘 / 二实例唤出);本线采用**二实例唤出**=三方向中最小不越权项:不抢首启焦点、不加新 UI 面,静默后台铁律不动。

## 探查结论(2026-10-07,本线唯一实质工作)

**缺口已修,同款方案,零代码改动。** 该缺口已于 2026-10-05 由 `10-05-win-second-instance-show`(代码笔 729b8f2)以完全相同的选型(官方 `tauri-plugin-single-instance`)落地,本线探查时在位于 main:

- 依赖门控:`desktop/src-tauri/Cargo.toml:66-70` — `tauri-plugin-single-instance = "2"` 仅 `[target.'cfg(target_os = "windows")'.dependencies]`,mac 依赖树零新增。
- 插件注册与唤出回调:`desktop/src-tauri/src/main.rs:726-734` — `#[cfg(target_os = "windows")]` builder 首位注册(官方要求插件序首位),第二实例启动 → 回调第一实例 `show_main_window`(show + set_focus)→ 第二实例自退。
- 唤窗与 macOS Reopen 同源:`desktop/src-tauri/src/main.rs:594-602` — `show_main_window` 三路共用(macOS Dock Reopen `main.rs:907-914` / Windows 二实例回调 / dev 与 `MYIA_SHOW_ON_START` 启动即显 `main.rs:884-890`),各平台亮窗行为严格一致。
- 此后唯一漂移:10-07 日志批 b06bdac 将回调内 `eprintln!` → `log::info!`(纯打印通道升级),机制本体未动(`git log -L 719,734:main.rs` 亲证)。

本线据此为**复核线**:不重写、不重复提交已在代码;建档记录裁决 + 亲跑域内门禁复核在位实现仍绿。

## Requirements

- **R1(复核)** 二次启动唤出已运行实例主窗:代码面在位(上行号);行为面验证归冒烟线(本线指令明确「真机验证归冒烟线,本线不做」;10-05 prd.md Notes 留有真机四步)。
- **R2(复核)** 首启行为零变化:插件仅 Windows 注册,首启只额外持命名 mutex 不显窗;`MYIA_SHOW_ON_START` / dev 构建启动即显路径(`main.rs:884-890`)未动。
- **R3(复核)** mac 不回归:Windows 插件块整体在 `#[cfg(target_os = "windows")]` 内,mac 编译产物不含该代码;macOS flock 单实例门(`main.rs:686-699`)/ Reopen 亮窗 / `open -b` 转激活链路亲读未动。

## Acceptance Criteria

- [x] **AC1** 二次启动唤出已运行实例主窗(代码面):single-instance 回调对主窗 `show + set_focus` 在位(`main.rs:726-734` + `main.rs:594-602`),与 macOS Reopen 同一函数同源;**行为面归冒烟线**,本线不做(如实注记)。
- [x] **AC2** 首启行为零变化:首启路径无任何新增显窗/抢焦点代码——插件回调仅在第二实例启动时于第一实例进程内触发;`show_on_start` 判定(`main.rs:884-885`)与 10-03-quiet-launch 以来语义一致。
- [x] **AC3** mac 不回归:域内门禁亲跑全绿——`cd desktop/src-tauri && cargo check --locked` exit 0(2026-10-07)+ `cargo test --locked` **85 passed / 0 failed / 1 ignored**(2026-10-07);Windows 插件依赖与注册均 mac 不编译。本机无 windows rustup target,`--target x86_64-pc-windows-msvc` 检查留真机/CI(与 10-05 同裁决)。

## 单测面注记(如实)

本线零代码改动,无新增可测纯函数面。唤出回调依赖 AppHandle/webview 窗口,无 tauri 运行时不可纯测——沿 10-05 同款裁决不硬凑;既有 86 用例(85 过 1 ignored)全绿即本线门禁。

## 复核回执(2026-10-07)

- 门禁:`cargo check --locked` Finished dev profile exit 0;`cargo test --locked` 85 passed / 0 failed / 1 ignored。
- 提交:零代码可提,仅本任务档入库(docs(task) 笔;`feat(desktop)` 无代码面故不适用,如实注记)。
- 未尽:Windows 真机行为验证归冒烟线。
