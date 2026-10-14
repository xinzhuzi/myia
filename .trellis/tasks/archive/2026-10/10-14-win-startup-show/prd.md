# Windows 发布包启动即亮窗

## Goal

tauri.windows.conf.json visible:true + main.rs 单实例唤出(若缺),根治双击图标永无窗口;真机构建留 tag 窗如实注。

## Background

- 根因:主窗出厂 `visible:false`(`desktop/src-tauri/tauri.conf.json:19`,10-03-quiet-launch 的 macOS 静默启动立场漏到了全平台)。macOS 有 Dock Reopen 亮窗兜底(`main.rs:1105-1112`);Windows 无 Dock、无托盘——普通用户**首次**双击图标永远看不到窗口(10-05-win-local-build evidence §8 坑 4 真机实证)。
- 前置:二实例唤出已在位(10-05-win-second-instance-show,commit 729b8f2)——`main.rs:868-876` Windows 门控首位注册官方 single-instance 插件、回调 `show_main_window`(`main.rs:739-744`),依赖在 `Cargo.toml:73-77`(windows 门控)。但它只救「第二次及以后的双击」,首启仍无窗——本轨补首启亮窗。
- 判例史:主人 2026-10-05 曾在「二实例唤出 / Windows 启动即亮窗 / 加托盘」三方向中批二实例唤出(archive/10-05-win-second-instance-show/prd.md:16);本轨即「启动即亮窗」方向的落子,与二实例唤出叠加成完整闭环(首启亮 + 再点聚焦)。

## Requirements

- **R1 平台覆盖件**:`desktop/src-tauri/tauri.windows.conf.json`——windows[0] 为**主配置 windows[0] 的全量镜像 + visible 翻转 true**。为何必须全量:平台配置合并是 `json_patch::merge`(tauri-utils 2.10.1 `config/parse.rs:185` → json-patch 4.2.0 `lib.rs:666-683`,RFC 7396)——非对象节点(含 `app.windows` **数组**)整组替换而非逐条递归合并,写增量 `{"visible":true}` 会在 Windows 生效配置里丢 title/1920×1080/focus/backgroundColor。
- **R2 单实例唤出**:已落(见 Background),本轨核对在位即止,main.rs 生产代码**零改动**。
- **R3 沙箱自动化不受累**:`MYIA_SHOW_ON_START` 语义逐字保持(`main.rs:1082-1088` Rust 逻辑零触碰);覆盖件仅在 `Target::Windows` 时参与合并(tauri-utils `config/parse.rs:51-56`),macOS 静默启动/冒烟链路(SMOKE_ROUTE/GEOMETRY/FOCUS、ui-ready 门控)完全不动。今日唯一 Windows 消费者是 tag 时 desktop-release.yml 的 windows-msi job(只构建不启动 app),无静默启动诉求的 Windows 消费者存在——**无需 env 抑制门**(docs/zh/build-windows.md:92 的远程自动化提示本就要 `MYIA_SHOW_ON_START=1` 达到的正是亮窗效果,新默认与其同向)。
- **R4 防漂移锚**:main.rs 单测 `windows_override_mirrors_base_window_config`——锚死「覆盖件 = 主配置镜像 + visible 翻转」不变式:丢键/值漂移/visible 回翻都会在任意宿主的 cargo test 先红(否则坏形状要等 tag 时 windows-msi 才炸,CI 的 rust-check 跑 ubuntu-24.04 不解析 windows 覆盖件,ci.yml:59)。

## Acceptance Criteria

- [x] **AC1** tauri.windows.conf.json 落地:windows[0] 携带主配置 windows[0] 全部键且逐字相等、visible 恰为 true(cargo 单测 `windows_override_mirrors_base_window_config` 锚定)。
- [x] **AC2** 配置形状验证:RFC 7396 合并模拟——Windows 生效 windows[0] = `{"title":"世事","width":1920,"height":1080,"visible":true,"focus":false,"backgroundColor":"#10131a"}`,且 windows 之外一切节点与主配置逐字相等(macOS 侧 visible:false 不动)。机器验证 = 镜像锚单测(AC1);合并语义源码论证已逐字复核(tauri-utils 2.10.1 `config/parse.rs:51-56` Target::Windows→`tauri.windows.conf.json`、`parse.rs:185` `merge(&mut config, &platform_config)`;json-patch 4.2.0 `lib.rs:666` `merge` 对非对象节点 `*doc = patch.clone()` 整组替换——数组整换)。**交叉 `cargo check --target x86_64-pc-windows-msvc` 在 mac 宿主不可行(2026-10-14 复查实测:失败于 `ring v0.17.14` 构建脚本 `'assert.h' file not found`,MSVC 目标需 C 交叉工具链,死于依赖阶段未及 tauri-build;前档「交叉 check 通过」主张无产物佐证,撤回)**;覆盖件的真实解析首消费者 = tag 时 windows-msi job(真机 Windows runner)。
- [x] **AC3** 宿主 `cargo check` 通过;`cargo test` 全绿(启动行为纯函数既有测 + 新增防漂移锚)。
- [x] **AC4** MYIA_SHOW_ON_START 语义保持:main.rs 生产代码零改动(git diff 仅 tests 模块新增);macOS 静默启动行为不变。
- [ ] **AC5** 真机 Windows 发布包双击 → 启动即见窗口(不抢焦点,任务栏闪烁提示;再点图标经 single-instance set_focus 聚焦)。**留待下个 tag 的 windows-msi 产物真机验证——本轨验证 = cargo check + 配置形状 + 单测,如实注。**

## Notes

- **真机构建留 tag 窗**:CI rust-check 跑 ubuntu-24.04 不解析 windows 覆盖件(ci.yml:59,76);windows-msi(desktop-release.yml:168)是覆盖件第一个真实消费者,tag 时验证窗口形状。
- **focus:false 照镜像**:窗出现不抢前台焦点(任务栏闪烁提示);再双击图标走 single-instance 回调 set_focus 聚焦。若主人想要「启动即抢焦点」,翻 tauri.windows.conf.json 的 focus(同步改防漂移锚豁免集)即可。
- **翻案权注记**:本事项池档原有两方向——托盘常驻(点托盘唤窗)与二实例唤出(已落);本轨在最稳档(零新插件依赖、零生产代码改动)取「启动即亮窗 + 既有二实例唤出」组合。托盘方向仍留池,主人可翻。
- 覆盖件为 JSON 无注释,合并语义陷阱(数组整组替换)的完整论证在 main.rs 测试 `windows_override_mirrors_base_window_config` 的文档注释与本档 R1。
- **复查补注(2026-10-14,修复员本会话)**:宿主 `cargo check` EXIT 0、`cargo test` 147 passed/0 failed/1 ignored(含镜像锚测)本会话实跑;交叉 check 受阻详情见 AC2(ring C 交叉工具链,与本轨配置形状无关)。另:`docs/zh/build-windows.md` §7「发布包默认静默启动……直接双击图标会看起来没打开」段已因本轨翻新而陈旧(Windows 发布包此后启动即亮窗,MYIA_SHOW_ON_START 提示不再必要)——该文件在本轨独占域(desktop/src-tauri/)之外,留主人/编排侧同步,本轨不动。
