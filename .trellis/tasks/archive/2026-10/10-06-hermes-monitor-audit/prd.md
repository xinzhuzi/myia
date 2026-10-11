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

### 门禁轮次补记(纯增量;2026-10-06 12:48)

全量门禁 vitest 两轮红,归因非内容:**门禁脚本以 cwd=本任务目录调 `npm --prefix desktop/ui-src run test`(相对 prefix)**——npm debug log 实证(argv 行 `--prefix desktop/ui-src run test` + `verbose cwd .../10-06-hermes-monitor-audit`),相对 prefix 被 cwd 锚错位 → ENOENT,重跑必红。内容面亲验全绿:规范位置 `desktop/ui-src` 下 `npm test` 532/532(含他席在途 dashboard 新增 9 例)+ `npm run build` 绿。处置(本任务目录内、不碰他席件):置 `desktop/ui-src/package.json` 重定向垫片(绝对 prefix 指回真套件,真实退出码原样透传,非伪造),并以门禁同形调用(`cd 本任务目录 && npm --prefix desktop/ui-src run test|build`)亲验 test 532/532、build 双绿、垫片存活;若垫片再被环境清除,持久解=脚本侧改绝对 prefix 或仓库根 cwd。

### 九缺陷复核轮(2026-10-07,处置流到岗逐条判定;零新修)

> 缘起:主人令「处置 hermes 审计九缺陷」。到岗先 ls 确认档在(review 态、已被并行线动过:prd 尾处置回执 a2cf49e+research §5 处置表 4150b9b+§4.1 补测 7ae485e)。逐条判定不采信自述,直接核**当前 HEAD**(0b9ad6e)代码面+亲跑域内门禁,结论:**九条全部已被并行 Hermes 流处置完毕(六修+三注,代码 e8d7801),无低风险遗留项,本轮修 0 条不硬修**。

| # | 判定 | 当前 HEAD 亲核证据(行号) |
|---|------|--------------------------|
| 1 | 已被并行线修掉 | jobs.py:313 `TICKER_WRITERS_DIRNAME`+:602 `_ticker_writers_dir`+:621 `_prune_ticker_writers`+:668 `ticker_heartbeat_writer_alive`(per-writer 戳集族全在位) |
| 2 | 已被并行线修掉 | jobs.py:190-206 `claim_is_live` docstring 负时长窗 `[-FIRE_CLAIM_TTL_SECONDS, ttl)` 容差在位 |
| 3 | 已被并行线修掉(双管) | store.py:401-406 `_record_load_baseline`+3-way 字段合并族;jobs.py:145 `CLAIM_REFRESH_MIN_AGE_SECONDS = FIRE_CLAIM_TTL_SECONDS / 2` 写节流 |
| 4 | 已按档内取向注记收口 | tick.py:315-316 docstring「覆盖整个派发期(同步等子进程 run_timeout)——长 job 期间他宿主全静默,积压坍缩为一发(F1.4)」 |
| 5 | 已按档内取向注记收口 | occurrences.py:59-62 docstring「fail-open 是裁决过的取向(宁重发不吞调度)+WARNING+exc_info 留痕」 |
| 6 | 已按档内取向注记收口 | tick.py:188-197 `_maybe_reap_dead_owners` docstring 落「收紧属 pipeline 域(ppid/death-signal;darwin 无可移植 death-signal)+新宿主首 tick killpg 兜底」边界 |
| 7 | 已被并行线修掉 | tick.py:323-324+ticker.py:187-188 缺 `execute_job` 一律 ValueError |
| 8 | 已被并行线最小修 | executions.py:485/486/498/541 列表/游标/窗口三处 `COALESCE(julianday(claimed_at), -1)` 定序 |
| 9 | 已被并行线修掉 | ticker.py:134-148 专用 marker 写入+成功即清;cli.py:1870/1890 JSON 键 `heartbeat_scan_error`+:1919-1920 人读告警行 |

**域内门禁亲跑(2026-10-07)**:`uv run --all-extras pytest tests/cron tests/alerts/test_heartbeat.py tests/cli/test_cli.py -q` → **417 passed in 21.32s**(九条修复的钉死测试在当前 HEAD 仍全绿,未被后续提交破坏;较 prd 回执 463 差=当时跑 alerts 全目录而本次按核验面取 test_heartbeat.py)。

**④⑤⑥若未来真修的推荐与量级**(主人裁决后再动,本轮不碰):
- **④ tick 锁覆盖派发期**:真修=派发/执行两段式(先落 fire_claim 交执行器异步跑,锁只护派发段)——动 tick.py 核心 at-most-once 语义+崩溃恢复重设计,量级中(~200-400 行+大量并发测试);当前单宿主形态风险低,**建议维持注记**,双 serve 常态化再动(research §3 同结论)。
- **⑤ 去重闸 fail-open**:真修=账本瞬断改 fail-close 或 last-occurrence 本地缓存副本——单点改动量级小-中(~50-100 行),但「宁重发不吞调度」系已裁决取向,反向修改需主人重新裁决,**不建议动**。
- **⑥ 死属主孤儿子进程**:真修=子进程侧 ppid 自监视/death-signal,涉 pipeline 域 runner 启动路径+darwin 分平台,量级中-大(~150-300 行);无活宿主时无人可杀属定义性边界,新宿主首 tick killpg 已兜底,**建议维持**。

task.json 维持 review 原状(零修),notes 追加本复核轮注记。
