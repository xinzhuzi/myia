# research/grill-facts.md — grill 轮 1 事实包(2026-10-07 双代理核实)

> 供实现批子代理直引;来源=GitHub tauri-apps/plugins-workspace v2 分支源码 + 本仓库 rg/fd 实测。与 design.md 决议互为印证。

## A. tauri-plugin-log v2 事实(源码级)

| # | 事实 | 来源 |
|---|------|------|
| A1 | 最新稳定版 **2.10.0**(2026-09-26);crates.io `max_version` 3.0.0-alpha.2 是 v3 alpha 线勿用 | plugins/log/Cargo.toml + crates.io |
| A2 | `TargetKind::Folder { path, file_name }`:file_name **不带扩展名**,活动文件恒 `{file_name}.log`(如 `shell.log`) | lib.rs Folder 文档注释 |
| A3 | **无按天轮转**;仅按大小:KeepAll(归档全留)/KeepOne(超限删当前,默认)/KeepSome(n) | lib.rs RotationStrategy |
| A4 | 归档名 `{file_name}_YYYY-MM-DD_HH-MM-SS.log`(常量 LOG_DATE_FORMAT,默认 UTC,可 UseLocal);重名先改 `.bak` | lib.rs rotate/rename_file_to_dated |
| A5 | `max_file_size` 默认 **40_000 字节**(过小必调);u128 clamp u64;写入 flush 时超限先 rotate 再写;启动已有文件 ≥max 也 rotate;FileOpenStrategy::Append 默认(续写) | lib.rs DEFAULT_MAX_FILE_SIZE |
| A6 | **`TargetKind::Webview` 方向=Rust 日志→webview 控制台显示**(emit `log://log`),不捕获前端 console | lib.rs Webview 文档注释 |
| A7 | UI console 汇入正路=JS 侧劫持 console(官方文档 forwardConsole 用户态 helper 模式)→`@tauri-apps/plugin-log` JS fn(invoke `plugin:log\|log`)→Rust 记 target=`webview`(带位置时 `webview::{location}`)流入全部 targets | commands.rs + guest-js/index.ts + tauri.app/plugin/logging |
| A8 | `attachConsole()`=**反向订阅**(Rust 日志打到 webview console),级别映射 Trace→log/Debug→debug/Info→info/Warn→warn/Error→error;本任务弃用 | guest-js/index.ts |
| A9 | JS 调用需 capability **`log:default`**(=allow-log);attachConsole 的 listen 走 core:event:default(⊂core:default);**Rust-only 可零 capability** | permissions/default.toml + tauri.app |
| A10 | 默认行格式 `{[YYYY-MM-DD][HH:MM:SS]}[{target}][{LEVEL}] {message}`;`Builder::format`/per-target `Target::format`(2.8.0+)可自定义;⚠️ `timezone_strategy()` 会**重置 formatter** 且字段序变——设置顺序必须 timezone 在前、format 在后 | lib.rs Builder |
| A11 | 默认 targets=Stdout+LogDir(各 OS app log 目录);我们显式 Folder 到数据根 | lib.rs |
| A12 | JS 侧支持 LogOptions{file,line,keyValues};`Builder::split()`/`skip_logger()` 可与自定义全局 logger 组合 | guest-js/commands.rs |

## B. 本仓库事实(rg/fd 实测)

| # | 事实 | 凭据 |
|---|------|------|
| B1 | `vision-server.log` 引用面:写入方 server.py:62/151-162/246-247/278/296;调用点 entry.py:4093(4099-4105 worker);**5 处测试断言** tests/vision/test_vision_models_server.py:542,590,593,600,611;spec sidecar-protocol.md:63;前端文案 vision-form.tsx:422;无读取/tail 消费方 | rg 全命中清单 |
| B2 | 壳有 sidecar respawn:Terminated→清 child+pending 回 `sidecar_terminated`→`schedule_respawn`(main.rs:145-160,238-297);指数退避 1/2/4/8/16s,上限 5 次后发 `{"state":"dead"}`;稳定 10s 归零;`sidecar://state` 事件 {respawning/online/dead};PyenvNotReadyError 停自动重试走 UI 引导;`sidecar_restart` 命令手动兜底 | main.rs:29-43,145-160,238-325 |
| B3 | CLI 数据根:无 MYIA_HOME→`./myssia.db`(cwd,DEFAULT_DB_PATH cli.py:222);有 env→`$MYIA_HOME/myssia.db`(cron 组 `_cron_default_db` cli.py:225-236,注释明言「无 env 的终端缺省行为不变」);data_root=db 父目录派生(cli.py:2143,4188-4190);**无 paths.py 统一点**,CLI/entry.py 两套同口径实现(entry.py `_serve_context` 598-633 + `myssia_home` 522-531,darwin=`~/Library/Application Support/MYIA`) | cli.py/entry.py |
| B4 | tests 布局:根=横切(test_secrets.py 判例=根模块平铺);模块进同名子目录(tests/cron/…);**新模块测试落位 `tests/test_log.py`**,桌面集成 tests/desktop/ | ls tests/ |
| B5 | 前端 console.* 全仓仅 4 处;无 onerror/unhandledrejection/ErrorBoundary;updater 卡片存在(updater-card.tsx)无埋点 | rg 实测 |
| B6 | `_ring_append`(entry.py:725)唯一汇聚点,条目 {seq,ts,run_id,stream,line};`_cli_json`(739-754)redirect_stderr 捕获 CLI WARNING+ 逐行入 ring;`_pump_stream`(3312)子进程 stdout/stderr 逐行:log 事件+ring;协议事件发射在 pump 侧,_cli_json 行只进 ring 不发事件 | entry.py |
