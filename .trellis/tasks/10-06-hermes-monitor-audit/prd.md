# Hermes 系监控全量排查+沙盘模拟

## Goal

主人 2026-10-06 令:将 Hermes 里面的监控排查一遍、模拟一遍。排查面=src/myssia/cron 十模块(jobs.json/tick 文件锁 at-most-once/executions 账本/自然语言 schedule/deliver 摘要)含 10-05-cron-heartbeat 的久未触发心跳告警规则族;模拟面=沙箱数据根多形态 job(间隔/cron 式/一次性)真实触发→账本/并发锁/摘要/心跳告警全链验证+清历史残留 serve 进程;产出 research.md 排查表+模拟回执+发现修复。

## Requirements

- TBD

## Acceptance Criteria

- [ ] TBD

## Notes

- Keep `prd.md` focused on requirements, constraints, and acceptance criteria.
- Lightweight tasks can remain PRD-only.
- For complex tasks, add `design.md` for technical design and `implement.md` for execution planning before `task.py start`.

## 九缺陷处置回执(2026-10-06,主人令「都做完」;代码 e8d7801 / 档务本提交)

> 处置对象 = research.md §2 九条。定向门禁亲跑:`uv run --all-extras pytest tests/cron -q` 335 passed、`tests/cli/test_cli.py tests/alerts/test_heartbeat.py tests/desktop` 336 passed、`tests/test_docs.py tests/test_gates.py tests/test_smoke.py` 198 passed;`uv run --all-extras ruff check` 改动 12 文件全绿。沙盘级实证:双写者后死一活一 → `cron status` ticker_alive=True(修复前假阴性);扫描失败 marker 经 status JSON 可见。

1. **双 serve 心跳 last-writer-wins(cli.py:1816-1819)——已修**:`jobs.py` 心跳标记族增 per-writer 戳集(`ticker_writers/<host>-<pid>`,每实例一份),`ticker_heartbeat_writer_alive` 任一同机活写者即活、`get_ticker_heartbeat_age` 取全写者最新鲜;写者顺手清同机死同胞与沉默超期(24h)戳,遗留单 marker 形态回落兼容。CLI 判读逻辑零改(合取式自动受益)。测试:双写者死一活一/清死同胞/最新鲜龄 3 例。
2. **时钟回拨误杀活认领(jobs.py claim_is_live)——已修**:负时长落在 `-FIRE_CLAIM_TTL_SECONDS` 容差(300s)内视为活——回拨瞬间活 fire_claim 不被清扫放掉、他宿主不得重认领(双跑窗关闭);远未来戳(超容差)仍 stale、「永不楔死」红线不变;owner 可证死仍立即失效(回拨救不了真死)。测试:回拨 −4min 认领保持/远未来 1h 仍可回收 2 例。
3. **jobs.json 降级锁字段级互相覆盖 + 心跳写放大——已修(双管)**:① `store.py` 临界区读基线(load_baseline)+ 落盘时戳不匹配 ⇒ 字段级 3-way 合并(我方有意变更 diff 覆写、他方对未触字段的更新保留、整行缺失恢复照旧、同字段冲突我方赢);无基线(锁外载荷/嵌套 save 后)退回 append-only 原语义。② `jobs.py` fire/run 认领心跳写节流:`CLAIM_REFRESH_MIN_AGE_SECONDS=TTL/2`(150s),60s 心跳节奏 2-3 跳才落一次盘,观测年龄上限 ≈210s<300s 保活无虞。测试:他方 pause 字段存活/同字段我方赢/删除键不复活/整行恢复 4 例 + 节流契约 1 例(真实时钟心跳用例经 monkeypatch 阈值保旧语义)。
4. **tick 锁覆盖派发期长 job 静默(tick.py)——注记收口**:档内明言「设计语义但需知悉」;tick() docstring 就地落证据(锁覆盖同步派发期、长 job 期他宿主静默、积压坍缩为一发 F1.4),不做异步派发翻修。
5. **去重闸 fail-open(occurrences.py)——注记收口**:档内明言「宁重发不吞调度」取向;docstring 补裁决依据(账本瞬断代价=多跑一轮可幂等管线,反向=射点无声消失;每次 fail-open 带 WARNING+exc_info 留痕不静默)。
6. **死属主回收 300s 节流+仅新宿主(tick.py `_maybe_reap_dead_owners`)——注记收口**:无活宿主时无人可杀孤儿子进程属定义性边界;收紧需子进程侧 ppid/death-signal 自监视(pipeline 域、darwin 无可移植 death-signal),不做 cron 域翻修;新宿主首 tick 的 D14 killpg+账本 unknown 是现存兜底,docstring 就地落边界。
7. **no-op 执行体陷阱(tick.py)——已修**:Stage A 占位桩移除,`execute_job=None` 的 `tick()`/`run_ticker_loop()` 一律 ValueError(serve/CLI/sidecar 三个生产宿主均已注入 CronRunner,desktop entry 亲核);缺 runner 派发零副作用/账本零行。测试:缺 runner 契约(无假成功/预算不耗/槽不吞/账本空)+循环 fail fast 2 例,原 no-op 桩契约测试随之更新。
8. **账本小项三件(executions.py)——最小修+注记**:手编垃圾 claimed_at 的 julianday→NULL 失序 → 三处查询(list ORDER BY/游标谓词/latest_executions 窗口)COALESCE(-1) 定序为确定「最老」,游标翻页可达;finish 全表删旧与窗口子查询增长按 1000 行终态帽注记知悉(排序面被帽钉死亚毫秒,docstring 落证据)。测试:垃圾戳恒垫底+游标可达+窗口不受染 1 例。
9. **heartbeat_scan 吞错无操作者痕迹(ticker.py)——已修**:失败写专用 `heartbeat_scan_last_error` marker(与 ticker_last_error 死活面分立互不误染,原「不写 ticker marker」理由保留),成功一扫即清;`cron status` JSON 键 `heartbeat_scan_error` + 人读告警行双面可见。测试:marker 生命周期/循环隔离用例扩展(status 面)/CLI 契约 3 例。
