# Implement:10-04-hermes-cron(深化版 2026-10-04)

> 查改分家:实现前重读 research/hermes-cron-map.md(上游地图)+ research/myia-ground-truth.md(MYIA 实核+探针,下文 A/B/C/W 编号同该档);每个模块开工前先读对应上游文件再动笔。上游前缀 `H = ~/.hermes/hermes-agent`。

## Stage 0:基线

- [x] 0.1 `uv run pytest -q` 记录基线(预存红以 stash 验证 HEAD 树归因);`git status` 快照留档
  - 收口注记 2026-10-04:实现期基线未见留档物(evidence/ 无基线档);收口期以全量实跑替代归因,见 C1 注
  - 主会话补记同日:执行工作流基线日志在案「基线:0 条预存红/错误」(dwfrun-a5211e74 阶段 1,基线为最干净一档),回标完成
- [x] 0.2 核对探针仍绿:`uv run python .trellis/tasks/10-04-hermes-cron/research/probe-dow-normalizer.py`(APScheduler 3.11.3 实证环境)
  - 收口复跑 2026-10-04:ALL OK(九用例 + 端到端射日 Tue)

## Stage A:定时底座(自底向上,每步独立可测)

- [x] A1 `shishi/cron/constants.py` + `schedule.py`
  - constants 照抄 H:cron/constants.py 全文(TTL=300/SKEW=60/HEADROOM=3)
  - schedule 照抄 H jobs.py 642-1238 段:normalize_repeat_value / parse_duration / _WEEKDAY_TO_CRON_DOW / _parse_clock_time / _natural_every_to_cron / parse_schedule / compute_next_run 前端 / once 恢复窗 / 时间工具族
  - **normalize_dow 落产**(D1):把 probe-dow-normalizer.py 的实证器转正为库函数+九用例入测试(0/7=周日、列表、区间、步进、环绕 5-1、名字、大小写);cron 分支限 5 段、归一化后 `CronTrigger.from_crontab(expr, ZoneInfo(tz))`,`compute_next_run(cron)` = `get_next_fire_time(last_run_at or None, now)`
  - once 朴素时间戳锚配置时区;interval UTC 加法;错误文案照抄五形态清单
  - 测试 `tests/test_cron_schedule.py`:五形态解析+错误文案+next 计算(重锚/严格后继/恰在射点)+DST 回拨(New_York 2026-11-01 折叠小时,探针场景固化为测试)+dow 归一化九用例+端到端射日(`*/2` 周一午→周二)
- [x] A2 `shishi/cron/store.py`
  - 照抄 H jobs.py 存储段:跨进程建议锁(fcntl/msvcrt)、tmp+rename 原子写、_normalize_job_record 规整、意外磁盘 job 合并(_merge_unexpected_disk_jobs)、_stage_jobs_payload
  - 数据根:`Path(db_path).parent / "cron"`(与目录/账本同款,ground-truth A6);目录自建
  - 测试 `tests/test_cron_store.py`:并发写、崩溃残留合并、损坏 JSON 修复路径
- [x] A3 `shishi/cron/executions.py`
  - 照抄 H cron/executions.py:DDL(design §2.3,含 run_summary_json)/状态机/属主指纹(pid+start_time)/中断恢复/终态裁剪 1000;裁 metrics 上报
  - 测试 `tests/test_cron_executions.py`:全转移+死属主判定(指纹不匹配≠死亡)+恢复+终态不可变
- [x] A4 `shishi/cron/jobs.py`(生命周期)
  - 照抄 H jobs.py:create/get/list/update/pause/resume/trigger/rearm_oneshot/remove + _apply_schedule_update + mark_job_run + get_due_jobs(backlog 坍缩)+ advance_next_runs + 心跳标记族;estop marker 检查口(grill Q4 已批保留)
  - **grill 事实裁决落地**:trigger 复活 paused+计入 repeat+manual_run_at 标记;终态 `state="completed"` 留存 7 天清扫(`COMPLETED_ONESHOT_RETENTION_DAYS=7` 可覆写);recurring 算不出 next → `state="error"` 不静默停摆;failure_deliver 缺省回落 deliver、"none" 关闭;`_advance_after_run` 锚 run 完成时刻
  - job 字段按 design §2.1(D2/D4/D11 改造);mark_job_run 四态 last_status(ok/failed/delivery_failed/skipped_busy)
  - 测试 `tests/test_cron_jobs.py`:CRUD+repeat 退役+paused reason+schedule 变更重算+due 扫描坍缩+心跳+trigger 复活/计数/终态留存清扫/failure_deliver 回落
- [x] A5 `shishi/cron/occurrences.py`
  - 照抄 H cron/occurrences.py:scheduled_instant 去重 + pending_slot 三函数
  - 测试 `tests/test_cron_occurrences.py`
- [x] A6 `shishi/cron/tick.py` + `ticker.py`
  - tick 照抄 H scheduler_tick.py 全时序(design §3.1);**派发分组=同 db 串行、不同 db 并行**(D13);ticker 照抄 H scheduler_thread.py SupervisedTickerThread 全文
  - 测试 `tests/test_cron_tick.py`:文件锁单飞、先推进后派发、并行池、单 job 失败不拖垮、ticker respawn
- [x] **门禁 G1(底座成形)**:`uv run pytest -q tests/test_cron_schedule.py tests/test_cron_store.py tests/test_cron_executions.py tests/test_cron_jobs.py tests/test_cron_occurrences.py tests/test_cron_tick.py` 全绿 + 全量回归零新红;小步提交
  - 收口实跑 2026-10-04:cron 七件套(含 runner)421 全绿;全量回归归因见 C1 注(4 红均 HEAD 态外来,与本批零耦合)

## Stage B:执行体 + 宿主 + 业务

- [x] B1 `shishi/cron/summary.py` + `runner.py`(D11/D12)
  - runner:`_self_command(["run", category, "--db", db, "--json", ...])` 子进程(参考 entry.py:2278/2341/2432 范式:Popen(start_new_session=True)、stdout JSON 泵、stderr 落 output/<job_id>/、墙钟 run_timeout 缺省 3600s→killpg SIGTERM→宽限 Timer→SIGKILL);退出码映射 0=ok/2=failed/3=partial 附注;RunResult.to_dict() 解析→summary 精简
  - summary:RunResult→摘要 dict+markdown 模板(状态/时长/源统计/留存/push 桶/失败行截断,design §5);SendContext kind 按 grill Q3 决议落
  - deliver≠local:宿主内 `asyncio.run(send_batch_to_targets(...))`(asyncio.run 先例 entry.py:3559;ChannelDirectory+DeliveryLedger 从数据根装载,A6);失败摘要走 failure_deliver
  - 测试 `tests/test_cron_runner.py`:spawn/JSON 解析/退出码映射/超时 killpg/deliver local+平台 spec(mock 子进程)/failure_deliver/delivery_failed 三态(用 RecordingChannel 范式 test_push.py:74)
- [x] B2 CLI:`shishi cron` 子命令族(design §4.1 十一个子命令)
  - 注册仿 channels 族(cli.py:452-485)插 `_add_run_parser` 后 + handlers dict;`--json` 契约(stdout 恰一份 JSON)
  - 测试:tests/test_cli.py 增 cron 用例(离线 mock runner;serve/tick 冒烟走 AC6)
- [x] B3 sidecar:desktop/entry.py
  - serve() 就绪后起 cron ticker(daemon Thread,数据根取 `_serve_context`;**不占 serve 线程**,B10 队头阻塞铁律);**cron fire 前查 `_RUNS_LOCK/_ACTIVE_RUN_ID`,占用=跳过+`skipped_busy`+`cron.skipped` 事件**(grill Q2 决议落;事件走 `_write_line`)
  - `_HANDLERS` 注册 cron.* 九方法(48→57)+ PROTOCOL_VERSION **v9**(design 起草时写 v7/43→52,先行批次 alert-rules/B234 顺延,复查修补回标实装口径);**协议四件套同步**:entry.py/tests 对账计数+用例(spec 范本 :2287)/spec desktop/sidecar-protocol.md/CHANGELOG;**ticker 句柄入 `_reset_sidecar_state` autouse 夹具**(B12 ⚠️ 线程泄漏)
  - 测试:test_desktop_sidecar_protocol.py 增族用例+ticker 生命周期用例
- [ ] **门禁 G2(端到端)**:AC6 真跑——`shishi cron create "every 2m" --category plugins/news.yaml --deliver <测试通道>` 起 serve ≥2 周期:子进程 run 执行、runs 表有记录、摘要到达、心跳/status 可查、runs 命令出摘要、remove 清场
  - 收口注记 2026-10-04:全链两轮真跑 PASS(evidence/smoke-e2e.md:serve ≥2 fire/runs 表 2 行/摘要落盘/心跳 33s 新鲜/runs 出摘要/remove 清场;evidence/smoke-refix.md:手动 tick 真派发/deliver stdout:debug 定向到达/failure_deliver 失败卡到达)。与原文口径两处如实偏差:①品类用本地 static_html fixture 非官方 news.yaml(离线冒烟外网不可达,evidence 在案);②**平台真发面(feishu/telegram 定向卡入群)未验**——冒烟环境无平台凭据,不伪造;平台卡面仅单测(RecordingChannel)覆盖。故本门与 AC6 留空,见 concerns
- [x] B4 文档:docs/zh/cron.md + docs/en/cron.md(建 job/自然语言语法+5 段 cron POSIX dow 语义/deliver spec/serve 形态/与 `--loop` 并存注记/digest 留池行为注记);README 功能清单补行
  - 复查修补 2026-10-04 落地:双语页 + README 双区文档表行 + tests/test_docs.py `BILINGUAL_PAGES` 收录(六页);docker compose 改 command 注记(Q7)随 §5 行为注记入页
  - 收口补齐 2026-10-04:README 核心亮点/Highlights 双区各补 cron 功能行;docker 注记指针修正(原指 docker/README.md——该档无 cron serve 内容,Q7 又不动 docker/,改指 docker-compose.yml 的 command 行并补容器内建 job 示例);§2 补 interval 完成时刻重锚 + 60s tick 量化注记(`every 1m` 实际约 2 分钟,smoke 实测口径)

## 收尾

- [x] C1 全量 `uv run pytest -q` 零新红;桌面协议测试全绿;`uv run shishi cron --help` 面=design §4.1
  - 收口实跑 2026-10-04:`uv run pytest -q` → 3573 passed / 19 skipped / **4 failed**;4 红全为 HEAD 态外来(test_alert_rules ×3 + test_baseline ×1:断言 `schema_version=="7"` vs 已提交 `SCHEMA_VERSION=8`;两测试文件的未提交 diff 仅 shishi→myia 改名、`src/myia/store/sqlite.py` 与 HEAD 一致、cron 与 store 零耦合)——本批新红为 0。桌面协议 123 全绿;`uv run myia cron --help` 十一子命令面核对=§4.1
- [x] C2 `gitnexus detect-changes -r shishi --scope staged` 核验改动面(红线:核心依赖零新增、SQLiteStore 零改动、`run --loop` 零改动)
  - 收口注记 2026-10-04:三红线已用 git diff 直接核过(pyproject.toml diff 空=依赖零新增;sqlite.py diff 空;cli.py diff 纯增量零删=`run --loop` 原样);detect-changes `--scope staged` 需 staged 面,本批纪律不 git add,留待提交期(C5)逐批执行
  - 主会话补记同日:提交落地后 index 即被并行改名波(shishi→myia→myssia)占用,staged 机器核验不可行;以独立复查(AC+D1-D14+红线逐项 verified)+三红线直核收口,回标完成
- [x] C3 spec 更新:python/index.md 增 cron/ 小节(存储布局/蓝本归属/偏离表指针);desktop/sidecar-protocol.md 增 cron.* 表+事件两枚
- [x] C4 蓝本对照终核:每模块 docstring 上游标注(research/hermes-cron-map.md 勾销)
  - 收口核验 2026-10-04:九模块(constants/schedule/store/executions/jobs/occurrences/tick/ticker/runner)+summary+__init__ docstring 均带 Hermes 上游路径与 MIT 归属(逐文件 grep 核过);design.md 对照表 §1 与偏离表 §6(D1-D14)完整在档
- [x] C5 提交分批:底座(A)/执行体+CLI(B1-B2)/sidecar+文档(B3-B4)三批,逐批 detect-changes;并行会话在场用 pathspec 限定提交
  - 主会话补记 2026-10-04:执行工作流底座批的固定路径 `src/shishi/cron` 撞上运行中途整包改名(shishi→myia),batch-A 提交落空;收口批统一收编为 **e3d3e60**(全功能:jobs/occurrences/tick/runner/summary/CLI/sidecar)+**e0f79cb**(双语文档+spec+任务收口),pathspec 纪律全程未收编并行文件。任务档历史路径 shishi/myia 均映射现 `src/myssia/`(并行线又翻一轮 myia→myssia),回标完成

## 回滚点

- G1 前:删 src/shishi/cron/ 即净回滚(无数据残留风险)
- G2 后:回滚同上;`<data_root>/cron/` 数据目录无害,可留可删

## 验证命令速查

```bash
uv run pytest -q tests/test_cron_schedule.py tests/test_cron_store.py tests/test_cron_executions.py tests/test_cron_jobs.py tests/test_cron_occurrences.py tests/test_cron_tick.py tests/test_cron_runner.py
uv run shishi cron list
uv run shishi cron create "every 2m" --category plugins/news.yaml --deliver local
uv run shishi cron serve   # 另终端;Ctrl-C 停
uv run shishi cron status && uv run shishi cron runs
uv run python .trellis/tasks/10-04-hermes-cron/research/probe-dow-normalizer.py
gitnexus detect-changes -r shishi --scope staged
```

## 终局补记(2026-10-04,归档后;原文勾选框与收口注记保持历史原状)

- **平台真发半面已闭环(飞书)**:归档时 G2/AC6 留空所缺的「平台定向卡真发」,已由后续批次(10-04-wrapup-checklist「按建议做完」流)实证——hermes-cron 运行摘要卡于 2026-10-04 18:41 真发 `feishu:AI福利群`(沙箱 fixture 品类一轮,跑完即删 job、令牌即用即废;执行链证据 `../10-04-wrapup-checklist/evidence/feishu-cron-card.md`)。AC6「deliver 定向到达」的真发半面据此闭环;failure_deliver/三态语义此前已单测覆盖。
- **仍缺**:TG 定向真发(全机无 TELEGRAM 凭据,wrapup 长期挂账,主人建 bot 后可补);官方 news.yaml 真网品类整跑(离线冒烟口径已在案,装机后随手可验)。
