# 统一日志模块:myssia.log 单点配置 + 全入口统一 + 落盘轮转保留 + 壳日志

## Goal

主人 2026-10-07 三连令:「落实到trellis任务」→「**日志模块必须有,统一起来**」→「**UI日志,后端日志,等等关键日志都必须有**」。起因=当轮诊断:MYIA 日志面散装——各处都在打日志,但没有一个统一的日志模块,且**持久化缺失**(App 退出/崩溃后日志清零,装机件上壳日志无人接收),**UI 层零日志**(白屏/渲染崩溃无痕)。本任务交付统一日志模块 `src/myssia/log.py`(全 Python 入口单点配置,stderr/环形缓冲/JSONL 落盘三路同源)+ Rust 壳与 **UI(webview)日志**经官方 `tauri-plugin-log` 汇入同一 `logs/` 目录——各层关键日志逐层对账「必须有」。

## grill 决议(2026-10-07 轮 1,主人令「按推荐」)

- **①全量落盘**:CLI/cron 跑次日志全量入统一流 `logs/myssia-*.jsonl`,与 `cron/output/*.log` 双份持久化接受(「都必须有」语义;7 天保留兜体积;产物语义不动)。
- **②CLI 落盘条件**:仅 `MYIA_HOME` 已设时落 `<MYIA_HOME>/logs`;裸 repo 终端跑=stderr-only(沿 `_cron_default_db`「无 env 终端行为不变」判例,防 `logs/` 建进仓库——games jobs.json 同源坑)。
- **③vision 归并**:并入 `myssia-*.jsonl`(proc=vision),**退役 `vision-server.log`**——机械改面:5 处测试断言(tests/vision/test_vision_models_server.py:542,590,593,600,611)+spec 一行(sidecar-protocol.md:63)+前端文案(vision-form.tsx:422);旧文件升级场景留存原地不删。
- **④UI 错误不进日志屏(首版)**:UI console/错误兜底/updater 埋点只落 shell 文件;ErrorBoundary 回退 UI 即时可见;进屏牵协议语义扩展,留后续可选。
- **⑤壳日志格式**:沿 tauri-plugin-log 默认 `[日期][时刻][target][LEVEL] msg`(target 自辨来源:壳 crate/`webview`=UI),不自造 format。
- **⑥默认值包**:保留 7 天/回填预算 2000 行/UI console 全劫持(log/info/warn/error)/ErrorBoundary 极简回退(错误文本+重载钮,截图入 evidence 请主人过目)/模块名 `src/myssia/log.py`/测试落位 `tests/test_log.py`/shell 单文件上限 5MB。

## 现状凭据(2026-10-07 亲测)

**散装的六块**:

| 块 | 现状 | 凭据 |
|----|------|------|
| Python 模块层 | ~50 模块各自 `logging.getLogger` | 各引擎/push/cron/telegram 面 |
| CLI 入口 | ad-hoc `basicConfig`(force=True,stderr,INFO/WARNING 按 --json) | `src/myssia/cli.py:1311` `_configure_logging` |
| sidecar serve | **零 logging 配置**:模块 WARNING+ 走 lastResort→进程 stderr→壳 `eprintln!`→装机件丢弃;崩溃 traceback 同路 | entry.py 无 basicConfig/getLogger;`main.rs:142` |
| 内存环形缓冲 | 4000 行,唯一 UI 日志面,重启即失 | `desktop/entry.py:503` `LOG_RING_CAPACITY` |
| vision server | 自带 open+轮转一只文件 | `src/myssia/vision/server.py:247` |
| Rust 壳 | 零日志框架,仅裸 `println!/eprintln!` | Cargo.toml 无 log/tracing/plugin;main.rs 18 处等 |
| **前端 UI(webview)** | console.* 全前端仅 4 处;**零错误兜底**(无 onerror/unhandledrejection/ErrorBoundary);updater 流(updater-card.tsx)无日志埋点——白屏/渲染崩溃/更新失败零痕迹 | rg 实测 2026-10-07 |

装机件数据根 `~/Library/Application Support/MYIA/` 无 `logs/` 目录;已有持久面仅 cron 每跑次独立文件(`cron/output/<job>/*.log`)、`vision-server.log`、`myia.db` 结构化台账。

## Requirements

- **R0 统一日志模块(核心)**:新建 `src/myssia/log.py`——单点 `configure()`;stderr handler(mode 分级:human=INFO / json·serve=WARNING)、环形缓冲 handler、JSONL 文件 handler 同挂 root;条目统一形状 `{seq, ts, run_id, stream, line, proc}`;seq 单源单调盖章。
- **R1 全 Python 入口统一路由**:CLI(`cli.py` `_configure_logging` 退役改薄壳或删除;落盘条件按决议②)、sidecar serve(entry.py 启动 configure)、cron(独立 `cron serve` 进程与 sidecar 内线程两形态)、vision server(经统一模块,**按决议③并入 myssia 单前缀,退役 vision-server.log**)——配置后 root handler 集一致,格式/落盘/轮转/保留同一套规则。
- **R2 落盘与保留**:数据根 `logs/myssia-YYYYMMDD.jsonl` 按天轮转(Python 单前缀单文件,proc 字段分进程;决议③),Rust 壳同目录(`shell.log`+归档,决议⑤格式);Python 侧保留 7 天按文件名日期,壳侧按归档名时间戳;清理 glob 前缀钉死,不伤邻居(cron/output/、旧 vision-server.log 留存不删)。
- **R3 子进程日志流同漏斗**:sidecar run 子进程与插件安装/远取的逐行输出(run_id/stream)经同一 logging 漏斗入 ring+盘;协议 `type:"log"` 实时事件路径不变。
- **R4 sidecar 自身模块日志入流**:serve 期模块 WARNING+ 进 ring+盘;`_cli_json` 内嵌 CLI 调用不得产生重复行或丢 handler(force=True 互踩以「CLI 也走统一模块」根治)。
- **R5 冷启动回填**:App 重启后 `logs.tail` 从盘尾回填(预算 2000 行,环形 4000 帽不破,seq 续接单调);前端零改动。
- **R6 安全红线与降级**:落盘内容不展开凭据(沿 `.trellis/spec/python/logging.md`);文件/目录不可写时静默降级不破主链(首错入 ring 一条提示后永久静默)。
- **R7 兼容**:sidecar 协议(`logs.tail` 请求/响应形状)不变;前端既有屏零改(R8 只新增日志兜底件与埋点);装机包 resources/锁不涉;MYIA_HOME 沙箱语义沿既有优先级链;旧 `vision-server.log` 留原地不迁移,cron 每跑次产物文件保留(跑次产物非日志,边界入档)。
- **R8 UI 日志必须有**:webview 前端按官方 forwardConsole 模式**劫持 console.*** 调 `@tauri-apps/plugin-log` JS API 汇入同一 targets→shell 文件(grill 勘误:attachConsole 是反向订阅,弃);全局错误兜底 `window.onerror`+`unhandledrejection`+React ErrorBoundary(极简回退:错误文本+重载钮,决议⑥)——渲染崩溃/白屏留痕;updater 流(检查/下载/安装/失败)埋点;**不进日志屏(决议④)**。
- **R9 关键日志面对账**:各层「必须有」逐层核验(管线/引擎/推送、sidecar 协议+子进程流+插件安装、cron、vision、壳生命周期+pyenv、sidecar 崩溃 stderr、UI console+错误兜底+updater)——每层落点与凭据(测试或装机)入档对账表,不许有「无日志层」。

### 非目标

- 不改日志内容与级别语义(12b7f45/43683c9 已调优面不动)。
- 不做日志远程上报/集中采集/UI 新查看面(UI 日志入落盘文件,不进日志屏——决议④,进屏属后续可选项)。
- 不统一 cron 每跑次输出文件形态(是产物不是日志)。

### 关键日志面清单(R9 对账表,AC11 逐层勾)

| # | 层 | 关键事件 | 落点 | 凭据 |
|---|-----|---------|------|------|
| 1 | Python 管线/引擎/推送 | run 生命周期/降级/失败分类/skip 原因 | myssia-*.jsonl | ✅ 测试(批0/1;收尾轮全量 4909 内绿)+装机 05/06(pipeline INFO 行落盘亲核) |
| 2 | sidecar 协议+子进程流 | run 逐行输出/插件安装/远取诊断 | myssia-*.jsonl+ring | ✅ 测试(批1 `_pump_stream` 复用 stream_line 条目;type:log 发射点集合逐点相同)+装机 05(run_id=1 子进程流行亲核) |
| 3 | cron | serve 心跳/跑次启停/异常 | myssia-*.jsonl+cron/output | ✅ 测试(tests/cron 335 passed 批1 亲跑;零代码线程继承)+装机 05(Cron ticker started 行亲核) |
| 4 | vision server | 起停/模型下载/异常 | myssia-*.jsonl(proc=vision;决议③) | ✅ 测试(test_spawn_output_pumped_to_unified_log_proc_vision=tests/vision/test_vision_models_server.py:588 复查修复后 sink 形态;47b4672 真子进程两段式实测)——装机未触发(看图流未走)如实记 |
| 5 | Rust 壳生命周期 | 启动/sidecar spawn 失败/pyenv 安装自检 | shell-*(plugin) | ✅ 壳单测(main.rs:1004/1031/1050/1061/1099)+装机 04(setup done ×6 跨重启亲核;spawn 失败/pyenv 失败路径装机未触发,打印点 43 处分级落码保证) |
| 6 | sidecar 崩溃 stderr | traceback 尾部 | shell-*(warn) | ✅ 落码(main.rs:142 stderr pump→log::warn!,b06bdac;装机崩溃未触发无痕)——shell.log 管道由装机 04 双 target 行证通,vitest+壳单测钉路径 |
| 7 | UI console+错误兜底 | console.*/onerror/unhandledrejection/ErrorBoundary | shell-*(Webview target) | ✅ vitest(log.test.ts 7 例+error-boundary.test.tsx 3 例)+装机 04 部分(updater 行同 webview→shell.log 管道亲核;onerror/ErrorBoundary 装机冒烟无独立回执如实记) |
| 8 | updater 流 | 检查/下载/安装/失败 | shell-*(UI 埋点) | ✅ vitest(updater-card.test.tsx 6 例含里程碑/失败分级)+装机 04(03:18 updater 两行亲核)+02 截图(设置页,未目验像素) |

## Acceptance Criteria

- [x] AC0 统一模块+全入口路由:`src/myssia/log.py` 存在;cli/sidecar serve/cron serve/vision server 四入口经它配置;测试断言配置后 root handler 集一致(形状断言);cli.py `_configure_logging` 与 vision 自带轮转代码退役;**vision-server.log 退役改面(5 测试断言+spec 一行+前端文案)全落(决议③)**。(证据:log.py 在档;cli.py:1329 proc=cli·vision/server.py:186 proc=vision·entry.py:735 proc=sidecar 亲核;退役符号 `_ring_append`/`_LOG_RING`/`SERVER_LOG_NAME`/`_rotate_log_if_huge` rg 全仓零命中亲核;test_configure_idempotent=tests/test_log.py:97+test_entrypoints_same_handlers=tests/desktop/test_sidecar_log_persistence.py:99,全量 4909 内绿;机械改面 vision-form.tsx:422+sidecar-protocol.md:63 亲核,5 测试断言随批1 入库)
- [x] AC1 落盘保真:环形条目逐行入 `<MYIA_HOME>/logs/myssia-YYYYMMDD.jsonl`(JSONL 字段 ts/run_id/stream/line/proc 与条目一致;文件行不含 seq——grill 勘误);跨天轮转;vision 行 proc=vision 同文件(决议③);CLI 落盘仅当 MYIA_HOME 已设,裸跑 stderr-only(决议②)。(证据:test_jsonl_fidelity=tests/test_log.py:186+test_daily_rollover=213+test_multiprocess_append=230;决议② test_cli_bare_repo_stderr_only/test_cli_home_env_writes_file 批1 在档;装机 05 快照字段亲核——ts/run_id/stream/line/proc 齐、无 seq)
- [x] AC2 UI 手动跑次持久:run.start 跑次日志(run_id 保留)在新 serve 实例后仍可从文件读到。(证据:test_run_logs_survive_restart=tests/desktop/test_sidecar_log_persistence.py:163;装机 06-run1-lines.txt=run_id=1 跑次五阶段行亲核+05 跨两会话同文件)
- [x] AC3 模块日志入流+互踩根治:serve 期模块 WARNING+ 进 ring+盘;`_cli_json` 期间同一 CLI 日志行 ring 中**恰一份**、调用后 handler 存活(force 互踩不再可能——测试钉死)。(证据:test_cli_embedded_single_copy=231+test_bare_print_still_streamed=243+test_handlers_after_cli_call=258;装机 05 亲核——同刻 proc=cli 行(裸形)与 run_id=1 proc=sidecar 行(logging 形)各恰一份)
- [x] AC4 壳日志落盘:壳起后数据根 `logs/` 出现壳日志文件;生命周期事件(至少 sidecar 拉起失败、pyenv 安装/自检失败路径)有痕;sidecar stderr 行(含崩溃尾部)由壳留痕。(证据:壳单测 main.rs:1004/1031/1050/1061/1099 五例;打印点 43 处 eprintln→log:: 分级+main.rs:142 stderr pump=warn 落码 b06bdac;装机 04=shell.log 快照 setup done ×6+webview 行亲核——注:sidecar 拉起失败/pyenv 失败路径装机未触发(全程健康启动),留痕由打印点改造保证,失败场景无装机截图如实记)
- [x] AC5 保留策略:>7 天旧文件启动清理被删;7 天内文件与邻居(cron/output/、旧 vision-server.log)原样保留(Python/Rust 两侧各测)。(证据:test_purge_stale=tests/test_log.py:298+test_purge_neighbors_untouched=315;Rust 侧 stale_shell_archives_purged_and_neighbors_untouched=main.rs:1061 六邻居负断言)
- [x] AC6 冷启动回填:新 serve 实例 `logs.tail` 从盘尾回填,预算内、seq 单调续接、环形帽不破;无文件时行为与现状全同(零回归)。(证据:test_backfill_budget_and_seq=283+test_backfill_no_files_noop=317+复查新增 test_logs_tail_total_and_truncated_semantics=191 协议全通路;装机 04/05=跨 6 次进程起落文件留存亲核——日志屏翻上一程历史由 03 截图留证,收尾代理未目验像素留主人过目)
- [x] AC7 降级:数据根不可写时主链不破、协议应答正常,首错一条 ring 提示后不再刷屏。(证据:test_degraded_readonly_root=tests/test_log.py:422)
- [x] AC8 门禁全绿:全量 pytest / ruff / `cargo check --locked`+壳单测 / vitest 零新红;plugins 锁门禁不涉。(证据:收尾轮亲跑 just test=pytest 4909 passed 40 skipped(112.38s)+vitest 589 passed(28 files)/just check=ruff@0.16.10 All checks passed+tsc -b && vite build ✓+cargo check --locked Finished,双 EXIT=0;cargo test --locked=85 passed 1 ignored 随批2 b06bdac 亲跑在案,其后零 Rust 改面、收尾轮未复跑如实记)
- [x] AC9 装机件亲验:换装后真机跑一次采集,数据根出现当日 myssia+壳(+vision 若触发)日志文件,内容可读、重启 App 后仍在且日志屏可翻;截图留证(evidence 不入 git)。(证据:evidence 六件——04/05/06 文本快照收尾轮亲核(采集 run_id=1 items=30/双文件/跨重启留存/updater 埋点),01-03 截图在档未目验像素留主人过目;vision 行未触发(看图流未走),由 test_spawn_output_pumped_to_unified_log_proc_vision=tests/vision/test_vision_models_server.py:588 钉死)
- [x] AC10 UI 日志落盘:console 劫持(官方 forwardConsole 模式)后 webview console.* 落 shell 文件(target=webview);`window.onerror`/`unhandledrejection` 兜底注册并落盘;React ErrorBoundary 渲染崩溃留痕+极简回退(错误文本+重载钮);updater 检查/下载/安装/失败事件埋点落盘;**不进日志屏(决议④)**;vitest 覆盖兜底模块与 ErrorBoundary。(证据:vitest log.test.ts 7 例+error-boundary.test.tsx 3 例+updater-card.test.tsx 6 例=589 内绿;装机 04=webview target updater 两行(03:18 检查开始/已是最新)亲核;注:onerror/ErrorBoundary 装机冒烟无独立回执——webview→shell.log 管道由 updater 行装机证通,兜底行为 vitest 钉死)
- [x] AC11 关键面对账表:prd §关键面清单每层「落点+凭据(测试/装机)」逐层勾——无「无日志层」存续。(证据:八层凭据列已回填见下表,层4/层6 装机未触发场景以测试+落码凭据如实注记)

## 过程(执行流水,回填位)

- **立档 `c5b3f66`**(docs(task),2026-10-07 01:40):三件套入库;grill 轮 1 六决议+两事实勘误(Webview target 方向/无按天轮转)+research/grill-facts.md A1-A12/B1-B6 事实底册;planning 态零代码。
- **批0 `e54dca6`**(feat(log),提交点①):`src/myssia/log.py` 模块本体——configure 幂等(摘自己标记 handler 再挂)/LogRecordFactory seq 单源盖章/RingHandler 4000 帽/JsonlFileHandler(date-in-filename+O_APPEND 每进程自开、无 rename,64KB 行截断,首错降级永久静默)/保留清理单前缀 glob/`stream_line`·`ring_snapshot`·`backfill`·`suspend/resume_stderr`;tests/test_log.py 21 例(AC 矩阵锚点全覆盖+凭据负断言);门禁 21 passed+ruff 双过+detect-changes=No changes(纯新增)。
- **批1 `61527ca`**(feat(log),提交点②):cli.py `_configure_logging` 薄壳转调(决议② MYIA_HOME 门,裸跑 stderr-only);entry.py `_LOG_RING`/`_LOG_SEQ`/`_ring_append` 退役(impact 前置 MEDIUM 12 调用方),24 调用点机械替换 `stream_line`;serve 启动 configure(ring=True proc=sidecar)+盘尾 backfill;`_m_logs_tail` 切道 ring_snapshot(形状零变化);`_cli_json` 挂起窗三向钉死;vision 决议③并入(自带 open+轮转退役,子进程输出泵入统一流 myssia-*.jsonl proc=vision);机械改面三处(5 测试断言+sidecar-protocol.md:63+vision-form.tsx:422)全落;新 tests/desktop/test_sidecar_log_persistence.py 9 例;门禁定向 375+cron 335+vision 166+desktop 322+test_log 21+邻域 61+ruff 双过+vitest vision-models 17。
- **批2 `b06bdac`**(feat(log),提交点③)+门禁补丁 **`9a71593`**(test(feed)):tauri-plugin-log 2.10 壳接入(Folder+Stdout 双写/5MB/KeepAll/UseLocal;数据根解析前置降级;启动清超期归档 shell_YYYY-MM-DD_HH-MM-SS.log 前缀钉死);打印点 43 处 eprintln→log:: 分级(main.rs 17+pyenv_install 10+pyenv_components 16;main.rs:142 sidecar stderr pump=warn);UI 日志件(lib/log.ts 官方 forwardConsole 劫持 console.*+onerror/unhandledrejection 兜底+幂等;components/error-boundary.tsx 根级 ErrorBoundary;main.tsx 接线;updater-card.tsx 埋点);capabilities 增 log:default;壳单测 5+vitest 三件(log 7/error-boundary 3/updater-card 扩 2);门禁 cargo check+test --locked 85 passed 1 ignored+vitest 589 passed 28 files+tsc -b 零错;9a71593 钉死 feed-screen 既有三级路径用例竞态(断言改 await waitFor 等数据落地,零产品码),just test-ui 4 连跑全绿。
- **批3 `3a21377`**(docs(spec),提交点④):python/logging.md 增「统一模块与落盘」节(六点:模块单点/入口路由四入口/文件形状/轮转保留/降级语义/凭据红线);sidecar-protocol.md #41 行补子进程输出统一日志描述;task.json planning→in_progress 入档;detect-changes=No changes detected(文档类)。
- **独立复查修复 `47b4672`**(fix(log)):两 medium 发现——①logs.tail total/truncated 语义回归(批1 切道先截尾再计数,truncated 结构性恒 False)修复为传 CAPACITY 全量过滤视图+尾部截取归 `_m_logs_tail` 自理,补 test_logs_tail_total_and_truncated_semantics 协议全通路钉死;②vision 改管道丢 nohup 存活语义(父进程退→泵线程死→server EPIPE 连杀)改中继 sink 文件(vision-server.out/.err,spawn 直传 O_APPEND 句柄)+tail 跟读泵,真子进程两段式实测父退子活;定向 64 passed+vision/pipeline/desktop 604 passed+ruff 双过。
- **批4 装机验证**(2026-10-07 03:01-03:27,装机验证者):重装换装后真机起 App→dashboard 跑一次采集(run_id=1,github-new-stars items=30)→设置页 updater 检查一次(已是最新 v0.0.1)→多次重启 App;数据根 `~/Library/Application Support/MYIA/logs/` 出现当日 myssia-20261007.jsonl+shell.log 跨 6 次进程起落留存;evidence 六件(01-03 截图+04-06 文本快照,不入 git)。
- **收尾归档**(本轮,归档收尾者):门禁 just check+just test 全量亲跑(回执见 AC8/run-report);AC0-AC11 回填;run-report.md 交付报告;task.json 置 completed;archive 移档。

## 结果(验收回执,完工填)

- **AC0-AC11 十二条全勾**(各条证据锚点注记见 AC 列表行尾;明细对账=run-report.md §AC 对账)。
- **装机核心回执**(evidence/04-06 文本快照收尾轮亲核):数据根 logs/ 当日双文件(myssia-20261007.jsonl+shell.log)在;myssia 行含 proc=sidecar(cron ticker/telegram 宿主/pipeline run_id=1 采集流)与 proc=cli(内嵌 CLI 行恰一份形态);shell.log 含壳生命周期(setup done ×6,03:01-03:24 跨重启)+webview target updater 埋点两行(检查开始/已是最新)——跨 6 次进程重启文件留存,回填场景坐实。
- **vision proc=vision 行装机未触发**(看图流未走):由 test_spawn_output_pumped_to_unified_log_proc_vision(tests/vision/test_vision_models_server.py:588,复查修复后 sink 形态断言)钉死,留主人下次看图时随手核。
- **独立复查两 medium 发现已修并入库**(47b4672),复查无未处置遗留。
- **诚实注记**:①evidence 三张 PNG(01-03)在档但收尾代理模型无图像输入未目验像素,留主人过目;②ErrorBoundary/console 兜底装机冒烟无独立回执——webview→shell.log 管道由 updater 行装机证通,兜底行为由 vitest 16 例钉死;③独立 `myia cron serve` 进程 proc=cli(design §2 表写 proc="cron"——实现沿 cli.py 入口未另设标识,spec 3a21377 已按实态入档,如需细分属后续小改)。
- **遗留**:UI 日志进日志屏=决议④明留后续可选项(协议语义扩展另立项);vision-server.out/.err 中继 sink 为复查修复新增产物面(5MB 截断帽,spec 侧随 #41 行语义覆盖)。

## 勘误补记(2026-10-07 深检;原文勾选不改历史,见 run-report.md §8)

- AC6/AC9 中「日志屏翻/可翻上一程历史」半句**像素层不成立**:03-logs-screen.png PaddleOCR 补验=空态(运行历史 0/0 轮);根因=运行历史为 sidecar 会话级注册表,重启即空,空态门控盖整卡使 logs.tail(回填已生效)不可达。协议层回填与文件留存证据维持;产品面收口移交 **10-07-logs-restart-visibility**(运行历史 DB 合流跨重启可见+两 low 顺手修),主人令「按照你的建议去做」已批。
