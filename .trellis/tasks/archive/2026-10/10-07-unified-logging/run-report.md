# 交付报告:统一日志模块——myssia.log 单点配置+全入口统一+落盘轮转保留+壳日志(10-07-unified-logging)

> 归档收尾者 2026-10-07 · task.json 置 completed 后归档 · 主人令三连:「落实到trellis任务」「日志模块必须有,统一起来」「UI日志,后端日志,等等关键日志都必须有」
> 勾选纪律:亲跑/亲验=勾并注据;commit 记录在档=引注;未做/不可考=如实记,不虚构。

## 1. 一句话结果

四批全落地全绿入库(批0 模块本体 `e54dca6`/批1 四入口路由 `61527ca`/批2 壳+UI 日志面 `b06bdac`+门禁补丁 `9a71593`/批3 spec `3a21377`),独立复查两 medium 发现已修(`47b4672`),装机验证证据六件在档(01-03 截图+04-06 文本快照,evidence 不入 git);收尾轮亲跑全量门禁双绿(just test=pytest 4909 passed 40 skipped+vitest 589 passed;just check EXIT=0)。**AC0-AC11 十二条全勾**,无「无日志层」存续;遗留=决议④明留的「UI 日志进日志屏」可选项与两处装机未触发场景(vision 行/崩溃 stderr,测试钉死)。

## 2. 各批提交对账(地面对账)

| 批 | commit | 内容摘要 | 当批门禁(commit 记录) |
|----|--------|---------|------------------------|
| 立档 | `c5b3f66` | 三件套+grill 六决议+两事实勘误+research/grill-facts.md;planning 零代码 | —(纯文档) |
| 批0 模块本体(提交点①) | `e54dca6` | `src/myssia/log.py`:configure 幂等/seq LogRecordFactory 单源/RingHandler 4000/JsonlFileHandler(date-in-filename+O_APPEND 无 rename/64KB 截断/首错降级静默)/保留清理/`stream_line`·`ring_snapshot`·`backfill`·`suspend·resume_stderr`;tests/test_log.py 21 例 | pytest 21 passed+ruff 双过+detect-changes=No changes(纯新增) |
| 批1 四入口路由(提交点②) | `61527ca` | cli.py 薄壳转调(决议② MYIA_HOME 门);entry.py `_LOG_RING`/`_ring_append` 退役(impact MEDIUM 12 调用方前置)24 调用点替换 `stream_line`;serve configure(ring=True proc=sidecar)+盘尾 backfill;`_m_logs_tail` 切道 ring_snapshot;`_cli_json` 挂起窗三向;vision 决议③并入+机械改面三处;test_sidecar_log_persistence.py 9 例 | 定向 375+cron 335+vision 166+desktop 322+test_log 21+邻域 61+ruff 双过+vitest vision-models 17 |
| 批2 壳+UI(提交点③) | `b06bdac` | tauri-plugin-log 2.10(Folder+Stdout/5MB/KeepAll/UseLocal/降级);启动清超期 shell 归档(前缀钉死);打印点 43 处 eprintln→log:: 分级(main.rs:142 pump=warn);lib/log.ts console 劫持+onerror/unhandledrejection 兜底;error-boundary.tsx 根级;updater-card 埋点;capabilities log:default;壳单测 5+vitest 三件 | cargo check+test --locked 85 passed 1 ignored+vitest 589 passed 28 files+tsc -b 零错;impact myssia_home_dir=CRITICAL(路径逐字节等价提取) |
| 批2 门禁补丁 | `9a71593` | feed-screen 既有三级路径用例竞态钉死(断言改 await waitFor,零产品码;证据三件=rg 零引用/隔离单跑同红/根因数据落地赛跑) | 修后 -t 10 连跑全绿+just test-ui 4 连跑 589 passed |
| 批3 spec(提交点④) | `3a21377` | python/logging.md「统一模块与落盘」节(六点);sidecar-protocol.md #41 行子进程输出统一日志描述;task.json in_progress 入档 | detect-changes=No changes detected(文档类) |
| 独立复查修复 | `47b4672` | 见 §4 | 定向 64 passed+vision/pipeline/desktop 604 passed+ruff 双过+真子进程两段式实测 |
| 批4 装机验证 | (无 commit,evidence 不入 git) | 见 §5 | — |
| 收尾归档 | 本轮 | 门禁亲跑+prd 回填+run-report+task.json completed+archive | 见 §3 收尾轮 |

**源码残留对账**:`git status` 工作树除任务档未跟踪(本任务 evidence+他人两目录)外零改动——本任务源码全部随五 commits 入库,零残留零补提交需求。

## 3. 门禁回执

**收尾轮亲跑(2026-10-07 03:55-03:57,归档收尾者,当前 HEAD=47b4672)**:

| 门禁 | 命令 | 结果 |
|------|------|------|
| 全量测试 | `just test`(=pytest 全量+vitest 全量) | pytest **4909 passed, 40 skipped**(112.38s)+ vitest **589 passed(28 files)**,EXIT=0 |
| 静态门禁 | `just check`(=ruff@0.16.10+tsc -b && vite build+cargo check --locked) | ruff **All checks passed**;vite build ✓(1.53s);cargo check --locked **Finished**,EXIT=0 |

**未复跑如实记**:cargo test --locked——最后一个触及 Rust 的提交为批2 `b06bdac`(当时亲跑 85 passed 1 ignored 在案),其后 `9a71593`/`3a21377`/`47b4672` 零 Rust 改面(47b4672 纯 Python:entry.py/server.py/pipeline.py+两测试文件),收尾轮以 cargo check --locked 绿覆盖编译面。

## 4. 独立复查发现与处置(47b4672,两 medium 全修)

1. **logs.tail total/truncated 语义回归**:批1 切道 ring_snapshot 时先截尾再计数→total 恒 ≤lines、truncated 结构性恒 False,前端「缓冲截断」徽标永久不可达(logs-screen.tsx:394 消费),违 spec「语义逐字对齐旧实现」声明。**修法**:传 CAPACITY 取全量过滤视图(deque maxlen 结构性 ≤ 帽,等价旧实现「先全量过滤」),尾部截取归 `_m_logs_tail` 自理——total=过滤后总数、truncated=总数>lines;补 `test_logs_tail_total_and_truncated_semantics`(tests/desktop/test_sidecar_log_persistence.py:191,5 行 run_id 行 lines=2 → total=5/truncated=True/尾部 2 行,经 rpc 协议全通路含 backfill)钉死原死路径。
2. **vision 管道 EPIPE 连杀 server**:批1 子进程 stdout/stderr=PIPE+daemon 泵线程——sidecar 退出(App 退出/壳 respawn,恰是 design §5 回填依赖场景)→泵线程死→读端全关→server 下一次写即 EPIPE 死,`start_new_session` 的 nohup 存活语义被连坐废除,下次 ensure 重付 ≤120s Metal JIT 冷启。**修法**:中继 sink 文件(`<data_root>/logs/vision-server.out|.err`,open("ab") 句柄直传 spawn=O_APPEND 子进程自持 fd,父进程句柄 finally 即弃)+tail 跟读泵逐行 `stream_line(proc="vision")`;spawn 基线=预备时文件 size(上一程存量不重放)/超 5MB spawn 前 truncate 归零/跟读截断回绕 seek 重对齐/`_SINK_PUMPS` 活泵登记防双泵/sink 预备失败降级 DEVNULL 不阻 spawn/data_root=None 仍 DEVNULL(决议②)。**装机级证明**:真子进程两段式实测(setsid 子进程,父进程即退,3s 后子进程仍活且 sink 双流持续追加 29 行——旧 PIPE 形态此刻首次写即 EPIPE 死)。测试:`test_spawn_output_pumped_to_unified_log_proc_vision` 重写为 sink 断言(tests/vision/test_vision_models_server.py:588)+新增 `test_spawn_sink_over_cap_truncated_and_degrade_devnull`(:662)。

**复查无未处置发现**。

## 5. 装机验证五步证据指针(implement 4.2;evidence/ 不入 git)

| 步 | 内容 | 证据指针 | 收尾轮核对状态 |
|----|------|---------|----------------|
| ① | 起 App→跑一次采集 | `01-dashboard-session1.png`(dashboard 跑次)+`06-run1-lines.txt`(run_id=1 五阶段行:运行开始/采集成功 items=30/采集完成/步骤完成/分类完成)+`05-myssia-jsonl-head.txt`(pipeline INFO 行) | 05/06 文本**亲核**✅;01 截图在档未目验像素(模型无图像输入)留主人过目 |
| ② | 数据根出现当日 myssia+壳(+vision 若触发)日志文件,内容可读 | `04-shell-log-snapshot.txt`(shell.log:setup done ×6+webview updater 两行)+`05-myssia-jsonl-head.txt`(proc=sidecar/proc=cli 行,字段 ts/run_id/stream/line/proc 齐全无 seq) | **亲核**✅;vision 行未触发(看图流未走)——测试钉死(§4-2 sink 断言) |
| ③ | UI 层:console+错误兜底冒烟验 shell 文件收行 | `04` 行 4-5:webview target `updater: 检查更新开始`/`检查完成: 已是最新(v0.0.1)`(03:18)——webview→shell.log 管道装机证通 | **亲核**✅;onerror/ErrorBoundary 装机冒烟无独立回执(行为由 vitest log.test.ts 7 例+error-boundary 3 例钉死)如实记 |
| ④ | updater 检查一次验埋点落盘 | `02-settings-system-after-updater-check.png`(设置页)+`04` updater 两行 | 同①③:文本亲核✅/截图在档未目验 |
| ⑤ | 重启 App→文件仍在、日志屏翻上一程历史(回填生效) | `04`(setup done 03:01/03:09/03:14/03:18/03:19/03:24=六次进程起落同一 shell.log 留存)+`05`(19:01:54Z 与 19:02:50Z 两会话行同文件)+`03-logs-screen.png`(日志屏) | 文件留存**亲核**✅;日志屏翻页=03 截图在档未目验像素 |

## 6. AC 对账总表(明细注记见 prd §Acceptance Criteria 行尾)

| AC | 判 | 主证据 |
|----|----|--------|
| AC0 模块+四入口+退役面 | ✅ | log.py 在档;proc 三锚点亲核;退役符号 rg 零命中;test_configure_idempotent+test_entrypoints_same_handlers |
| AC1 落盘保真 | ✅ | test_jsonl_fidelity/daily_rollover/multiprocess_append+装机 05 字段亲核 |
| AC2 跑次持久 | ✅ | test_run_logs_survive_restart+装机 06 |
| AC3 互踩根治 | ✅ | 三向测试+装机 05 恰一份形态亲核 |
| AC4 壳日志落盘 | ✅ | 壳单测 5 例+装机 04(失败路径装机未触发,落码保证,如实记) |
| AC5 保留双侧 | ✅ | Python 2 例+Rust 六邻居负断言 |
| AC6 冷启动回填 | ✅ | backfill 2 例+truncated 语义例+装机跨重启留存 |
| AC7 降级 | ✅ | test_degraded_readonly_root |
| AC8 门禁全绿 | ✅ | 收尾轮亲跑 §3 双 EXIT=0 |
| AC9 装机亲验 | ✅ | evidence 六件(文本亲核/截图在档未目验);vision 未触发如实记 |
| AC10 UI 日志落盘 | ✅ | vitest 16 例+装机 04 webview updater 行 |
| AC11 八层对账 | ✅ | prd §关键日志面清单凭据列逐层回填 |

## 7. 遗留事项(留主人/后续)

1. **UI 日志进日志屏(决议④明留)**:首版 UI 错误只落 shell 文件不进日志屏;进屏牵协议语义扩展,后续可选项另裁。
2. **两处装机未触发场景**:vision proc=vision 行(下次真机看图随手核 `logs/myssia-*.jsonl` 尾部)/sidecar 崩溃 stderr 留痕(运维事件,触发时看 shell.log warn 行)——均测试+落码钉死,非缺口。
3. **cron 独立 serve 进程 proc=cli**:design §2 表原写 proc="cron",实现沿 cli.py 入口未另设标识(spec `3a21377` 已按实态入档);如需细分属后续小改(一行参数)。
4. **ErrorBoundary 回退 UI 审美裁决**(决议⑥):截图留主人过目(01-03 在 evidence)。
5. **vision-server.out/.err 中继 sink**:复查修复新增产物面(5MB 截断帽自管),非目标面扩展已随 #41 行 spec 语义覆盖;如需纳入保留清理窗属后续小改。
