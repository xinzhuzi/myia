# implement.md — 统一日志模块执行计划

> 批次按可独立验证/revert 组织;每批末门禁过才进下一批。改码前对本批触及符号跑 `gitnexus impact -r shishi <symbol>`(AGENTS 铁律);提交前 `gitnexus detect-changes -r shishi --scope staged`。事实底册=`research/grill-facts.md`(grill 轮 1 双代理源码级核实,批0/批2 直引:plugin 产名/权限/坑清单、仓库引用面行号)。

## 规模清单(先报量纪律,总量≈3-4 个工作日)

| 批 | 内容 | 规模估 | 新文件 | 改面 |
|----|------|--------|--------|------|
| 批0 | log.py 模块+单测 | ~0.5-1 天 | src/myssia/log.py, tests/test_log.py | 零 |
| 批1 | 四入口路由+sidecar 改造 | ~1-1.5 天 | tests/desktop/test_sidecar_log_persistence.py(或扩既有) | cli.py/entry.py/vision/server.py+5 测试断言+spec 一行+前端文案 |
| 批2 | tauri-plugin-log+壳+UI | ~1 天 | ui-src/src/lib/log.ts+ErrorBoundary | Cargo.toml/main.rs/pyenv_*.rs/updater-card/capabilities |
| 批3 | spec+全量门禁 | ~0.5 天 | — | 两个 spec 档 |
| 批4 | 装机验证+归档 | ~0.5 天 | evidence(不入 git) | prd 回填 |

## 批0 模块本体:`src/myssia/log.py`(R0/AC0 半)

- [ ] 0.1 建 `src/myssia/log.py`(决议⑥模块名):常量(CAPACITY=4000/RETENTION_DAYS=7/BACKFILL_BUDGET=2000);`configure(mode, data_root, ring, proc)` 幂等(单前缀 myssia,决议③不设 prefix 参数);LogRecordFactory seq 盖章(装一次守卫);RingHandler;JsonlFileHandler(惰性句柄/本地日轮转/每行 flush/首错降级/文件行不落 seq);stderr handler(mode 分级);`stream_line` / `ring_snapshot` / `backfill`(重发 seq) / `suspend_stderr`+`resume_stderr`;启动时 `myssia-*.jsonl` 超期清理(单前缀)。
- [ ] 0.2 模块单测(落位 `tests/test_log.py`,根模块平铺判例=test_secrets.py):configure 幂等(handler 集不翻倍);seq 单调;ring 帽;JSONL 保真+跨天轮转(注入日期)+多进程并发 append(多进程互踢场景模拟);降级(只读数据根→主链不破+一条提示+永久静默);保留清理+邻居负断言;backfill 预算/坏行跳过/seq 重发单调/无文件零行为;凭据负断言(env 值样张不出现)。
- [ ] 门禁:`uv run pytest <新测试> -q` + `uv run ruff check`;impact:无既有符号改动,免。
- [ ] 提交点①(纯新增,revert 即回)。

## 批1 入口路由 + sidecar 改造(AC0 另半/1/2/3/5 Python 侧/6/7)

- [ ] 1.1 **前置**:`gitnexus impact -r shishi _ring_append`(退役波及面全列,对 design §9 风险1);`impact _m_logs_tail`。
- [ ] 1.2 cli.py:`_configure_logging` 转调 `myssia.log.configure`(home 用既有解析;--json→mode="json");**落盘条件决议②**:MYIA_HOME 设→`<MYIA_HOME>/logs`,未设→data_root=None 仅 stderr(防仓库污染);行为对齐断言(stderr 级别/格式不变;裸跑零新文件)。
- [ ] 1.3 entry.py:serve 启动 `configure(mode="serve", …, ring=True, proc="sidecar")`+`backfill`;`_LOG_RING`/`_LOG_SEQ`/`_ring_append` 退役;调用点(664/753/1359/3148/3317 等,以 impact 清单为准)机械替换为 `stream_line`(返回条目供协议 `type:"log"` 事件发射,事件路径不动);`_m_logs_tail`→`ring_snapshot`;`_cli_json` 窗口 `suspend_stderr`/`resume_stderr`+裸 print 行沿旧路入流。
- [ ] 1.4 vision server(决议③并入):`vision/server.py` 自带 open+`_rotate_log_if_huge` 退役,改 `configure(proc="vision", ring=False)` 落 myssia-*.jsonl;**机械改面**:5 处测试断言(tests/vision/test_vision_models_server.py:542,590,593,600,611 改断言 myssia-*.jsonl 的 proc=vision 行)+spec(sidecar-protocol.md:63 日志路径描述)+前端文案(vision-form.tsx:422);旧 vision-server.log 留原地不删(升级场景)。
- [ ] 1.5 cron:零代码(线程形态继承 root;独立 serve 走 cli.py);`cron/output` 不动;确认无回归即可。
- [ ] 1.6 测试:扩 `tests/desktop/test_desktop_sidecar_protocol.py` 或新 `tests/desktop/test_sidecar_log_persistence.py`:四入口 handler 集一致(AC0);AC1 字段保真;AC2 run_id 落盘+新 serve 实例可读;AC3 恰一份/裸 print 仍入流/窗口后 handler 完整;AC5/6/7 见批0 复用+serve 集成路径。夹具一律 tmp+MYIA_HOME,不碰真实数据根。
- [ ] 门禁:`uv run pytest tests -k 'log or sidecar_protocol or vision' -q` 定向 → 全量 `uv run pytest --all-extras`(后台+exit 文件,禁 sleep 轮询)+ `uv run ruff check`。
- [ ] 提交点②。

## 批2 Rust 壳 + UI 日志面:tauri-plugin-log(AC4/AC5 壳半/AC10)

- [ ] 2.1 `desktop/src-tauri/Cargo.toml` 加 `tauri-plugin-log = "2"`;`cargo check --locked` 过(lock 随改随更)。
- [ ] 2.2 builder:Folder target=`data_root(app)/logs`(创建失败降级 Stdout)+ Stdout;max_file_size 5MB(决议⑥)+KeepAll(归档名时间戳,启动自清 >7 天);格式沿 plugin 默认(决议⑤,不自造 format;注意 timezone_strategy 会重置 formatter 的顺序坑);capabilities 增 `log:default`;**真名复核**活动 `shell.log`/归档 `shell_<时间戳>.log` 后钉清理 glob。
- [ ] 2.3 壳侧打印点改造:main.rs 18 + pyenv_components.rs 16 + pyenv_install.rs 10 处 → `log::` 宏分级;main.rs:142 sidecar stderr pump → `log::warn!`(崩溃 traceback 唯一落点)。
- [ ] 2.4 **UI 日志件**:`desktop/ui-src/src/lib/log.ts`(官方 forwardConsole 模式劫持 console.*→plugin JS API;+onerror+unhandledrejection 前缀化);根级 ErrorBoundary(极简回退:错误文本+重载钮);App 启动接线;updater-card 埋点(检查/下载里程碑/安装/失败,`updater:` 前缀,经劫持链落盘)。
- [ ] 2.5 vitest:log.ts 兜底注册/ErrorBoundary 回退渲染/updater 埋点调用;壳单测:路径拼装/`shell-*` glob 负断言不删邻居/降级分支。
- [ ] 2.6 壳侧保留:启动 `shell-*` glob 清理(>7 天)。
- [ ] 门禁:`cargo check --locked && cargo test` + `cd desktop/ui-src && npx vitest run` + `tsc` 零错。
- [ ] 提交点③。

## 批3 spec 更新 + 全量收口(AC8)

- [ ] 3.1 `.trellis/spec/python/logging.md` 增「统一模块与落盘」节:模块单点/入口路由/文件形状/轮转保留/降级语义/凭据红线沿用。
- [ ] 3.2 `.trellis/spec/desktop/sidecar-protocol.md`:`logs.tail` 补冷启动回填行为(形状不变声明)。
- [ ] 3.3 全量门禁:pytest 全量 / ruff / `cargo check --locked`+`cargo test` / `vitest run`(前端零改防意外);`gitnexus detect-changes` 核改动面。
- [ ] 提交点④(文档)。

## 批4 装机验证 + 归档(AC9/AC11)

- [ ] 4.1 重打包 + 静默换装(沿纪律:先验源再删旧、换装后清 WKWebView 缓存)。
- [ ] 4.2 真机验:起 App→跑一次采集→数据根 `logs/` 出现当日 myssia+壳日志(myssia 内 proc=vision 行随看图触发核验,决议③);**UI 层**:devtools console 一条+人为触发一次错误兜底(或 ErrorBoundary 冒烟)验 shell 文件收行;updater 检查一次验埋点落盘;重启 App→文件仍在、日志屏翻到上一程历史(回填生效);截图+OCR 留证 evidence(不入 git)。
- [ ] 4.3 深复查(对照 design §9 风险表逐项)+ **AC11 对账表逐层勾**(prd §关键日志面清单:每层落点+凭据测试或装机,无「无日志层」存续),回填 prd.md AC 勾选与过程/结果段。
- [ ] 4.4 归档:task.py 置 completed + archive(沿 `--no-commit`+新旧路径一起 add 外科纪律)。

## 验证命令速查

```bash
# Python 定向
uv run pytest tests -k 'log or sidecar_protocol or vision' -q
# Python 全量(本机必须 --all-extras;后台+exit 文件)
uv run pytest --all-extras -q
uv run ruff check
# Rust
cargo check --locked && cargo test        # desktop/src-tauri 下
# 前端(批3 防意外)
cd desktop/ui-src && npx vitest run
# GitNexus
gitnexus impact -r shishi _ring_append
gitnexus detect-changes -r shishi --scope staged
```

## 测试矩阵(AC → 文件 → 用例;实现与复查共用对账面)

| AC | 文件 | 用例(挂 pytest -k 锚点) |
|----|------|------|
| AC0 | tests/test_log.py + tests/desktop/* | `test_configure_idempotent` / 四入口 handler 集形状一致 `test_entrypoints_same_handlers` |
| AC1 | tests/test_log.py | `test_jsonl_fidelity`(字段保真/无 seq)/ `test_daily_rollover`(注入日期)/ `test_multiprocess_append`(并发互踢) |
| AC2 | tests/desktop/test_sidecar_log_persistence.py | `test_run_logs_survive_restart`(run_id 落盘+新实例可读) |
| AC3 | 同上 | `test_cli_embedded_single_copy`(恰一份)/ `test_bare_print_still_streamed` / `test_handlers_after_cli_call` |
| AC4 | desktop/src-tauri 内嵌 #[cfg(test)] | 路径拼装/降级分支;装机=4.2 人工 |
| AC5 | tests/test_log.py + 壳单测 | `test_purge_stale`(>7 天删)/ `test_purge_neighbors_untouched`(cron/output+旧 vision-server.log 负断言)/ 壳 glob 同款 |
| AC6 | tests/desktop/* | `test_backfill_budget_and_seq`(预算/重发单调/帽)/ `test_backfill_no_files_noop`(零回归) |
| AC7 | tests/test_log.py | `test_degraded_readonly_root`(主链不破+一条提示+静默) |
| AC8 | — | 门禁命令亲跑回执(批3) |
| AC10 | ui-src *.test.tsx | console 劫持转发/onerror 注册/ErrorBoundary 回退/updater 埋点调用断言 |
| AC11 | prd 对账表 | 批4 逐层勾 |

## 回滚点

批0 纯新增独立;批1 含 `_ring_append` 退役(波及面 impact 前置+定向测试兜底);批2/批3 各自独立。任批 revert 即回;遗留 `logs/*.jsonl` 死文件人工删;无迁移无协议耦合(design §8)。
