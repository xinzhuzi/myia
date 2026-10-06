# research.md — 10-06-hermes-monitor-audit:Hermes 系监控排查+沙盘模拟

> 主人令(2026-10-06 凌晨):「将 Hermes 里面的监控也排查一遍,模拟一遍」。
> 排查 = Explore 代理十模块+告警面只读审计(七问,证据行号);模拟 = 本机沙盘(/tmp/hermes-sim,本地夹具服务器 127.0.0.1:8765 零外网)三形态 job 真跑。

## §1 沙盘模拟回执(全链实证,证据 evidence/)

| # | 验证项 | 结果 | 证据 |
|---|--------|------|------|
| 1 | schedule 三形态 | interval(every 1m)/cron 五段(*/1)/once(in 1m)全创建+按点触发;**秒级粒度被拒**('20s'/'45s' invalid duration——词表 30m/2h/1d/裸单位,分钟为地板) | serve1.log+账本 |
| 2 | 双 serve 并存 | 两实例都活着(cli 无单例守卫,设计如此),**tick 文件锁互斥:账本每射点恰一行**(01:56:00/01:57:00 各一条,无双发)——at-most-once 实证成立 | executions-ledger.txt |
| 3 | kill -9 恢复 | 锁随 fd 内核回收(tick.lock 文件残留无害);重启后**逾期坍缩补发一发**:scheduled 17:58:36 与 17:59:00 两射点坍缩为 01:59:21 一发/每 job(不连跑不跳过,F1.4 语义) | executions-ledger.txt |
| 4 | executions 账本 | 独立 `<数据根>/cron/executions.db`(与 myssia.db 分库);字段含 scheduled_instant/pid/claimed_at;终态裁剪 1000 行;CLI `cron runs` 带运行摘要 | 账本+runs 输出 |
| 5 | deliver local | `output/<job_id>/<时间戳>.md+.log`,内容=stdout digest 实文(Hermes 模拟条目 A/B ✓) | 沙盘 output/ |
| 6 | CLI 面 | cron status(ticker 活着/心跳 0s/2 启用 3 全部——一次性终态默认隐)/pause/resume/runs 全通 | 会话回执 |
| 7 | **cron_stale 心跳实弹** | 规则(API 建档)→冷静期→run 搭车扫描→fired 落库:`cron-stale:ai-news:<时间桶>` dedup(at-most-once)+「品类 ai-news 已 0 小时无成功采集」 | alert-fired.txt |

**沙盘翻出的两个校验器行为(非缺陷,fail-open 语义良好)**:
- scope 是封闭品类词表(七类+channel/server/token/global)——fixture 品类被拒载且逐行清晰告警不拦其余规则;
- push 动作必须带 `action_config.channel`(32 通道词表)——None 被拒载同款。

## §2 审计结论(Explore 代理,十模块+告警面,行号证据全文见会话)

**总评:Hermes 移植的监控面工程质量高**——tick 锁 errno 白名单上抛(防「看着健康、job 永不再跑」)、jobs.json mkstemp+fsync+os.replace 原子写、账本终态恰一次+死属主指纹回收、坏 expr 落 error 态绝不静默停摆、逾期坍缩补发语义明确。

**潜在缺陷九条(按风险排序,本轮不修,主人裁决)**:
1. **双 serve 心跳 marker last-writer-wins**:`cron status` 的 ticker_alive 只核最后写者 pid,后写者先停有最长 3×interval+20s 假阴性窗(cli.py:1816-1819);
2. **时钟回拨误杀活认领**:claim_is_live 对「未来戳」判 stale → 可清活 fire_claim → 双跑窗口(jobs.py:183-192);owner-fence 只弃回据不能停已跑进程;
3. **jobs.json 降级锁丢更新**:flock 30s 超时降进程内后,CLI pause/update 与 ticker 心跳写字段级互相覆盖(store.py:322-331);fire-claim 心跳写放大(每分钟全量重写+fsync)放大窗口;
4. tick 锁覆盖整个派发期(同步等子进程 run_timeout):长 job 期间他宿主全静默,积压坍缩为一发(tick.py:307-352)——设计语义但需知悉;
5. 去重闸 fail-open:账本暂不可读的轮次 due 去重失效可能重发(occurrences.py:96-100,宁重发不吞调度的取向);
6. 死属主回收时延 300s 节流+仅新宿主 tick:kill -9 后无人重启则孤儿子进程续跑可写同库;
7. no-op 执行体陷阱:直接调 tick() API 未注入 runner 会记假成功(tick.py:262-273;serve/cron tick 已注入);
8. 账本小项:finish 全表删旧、julianday 对手编时间戳失序、窗口子查询随历史增长(1000 行帽兜底);
9. heartbeat_scan 吞错只留 ERROR 日志不写错误 marker:扫描持续失败无操作者可见痕迹。

**沙盘建议复验的 5 个风险点**(audit 代理出,本轮已覆盖 1/2/3 主干,4/5 未做):时钟回拨注入、flock>30s 降级并发写、长执行×锁×坍缩边界。

## §3 遗留与移交

- 心跳规则的生产配置样例已在 ai-news 域可复用(scope=ai-news+auto 或 threshold_hours);主人要开一条真实心跳规则(如「ai-news 超 24h 无成功采集就告警」)一句话即可代配。
- 双 serve 部署形态若成为常态(桌面壳+CLI 并存),缺陷 1/3 值得修(单例守卫或心跳 marker 多写者仲裁);当前单宿主形态风险低。
- 沙盘残留清点:本机另有两组 `cron serve --db /tmp/myia-heartbeat-evidence/...`(00:59/01:00 起,疑似并行会话心跳验证在途)——**非本沙盘产物,不动**,留主人/并行会话自查。

## §4 复查轮补充(主人质询「没有其他问题了吗」)

- 生产实跑旁证:app 内调度器今晨 08:00:44 真实触发 AI资讯 job 并 08:02:41 完成(账本/ticker 戳亲核)——cron 系统**非沙盘、在装机态真实运转**;坍缩补发/账本/心跳戳与沙盘结论一致。
- 残留 heartbeat-evidence serve 复查:5 进程在跑(并行会话在途,非本档产物,维持不动)。
- 沙盘未覆盖两项如实重申:时钟回拨注入(审计缺陷 3)、flock>30s 降级并发写(缺陷 4)——修缺陷时一并做,不单独模拟。

## §5 九缺陷处置表(2026-10-06 主人令「做完剩下的问题」;处置主体=并行 Hermes 流,本流让行后验证收编)

> 让行记:本流开工探针(12:22)即见 cron 面在途改动引用本任务编号体系 → 按并行协调协议零编辑让行,mtime+git-status 双探针 150s 节奏监测;对方 12:30:21 最后前进、12:45:22 达 15 分钟安静阈值后本流转收编验证岗。九条**全部**由并行流交付(代码 e8d7801,回执另落 prd.md 尾 a2cf49e,门禁垫片 4e97a40),本流对照 §2 逐条亲核代码+亲跑门禁,无遗留缺口需本流补。

| # | 处置 | 测试 | 提交 | 交付方 |
|---|------|------|------|--------|
| 1 | **已修**:per-writer 心跳戳集 `ticker_writers/<host>-<pid>`(jobs.py),任一同机活写者即活+顺手清死同胞/24h 超期戳,age 取全写者最新鲜;遗留单 marker 回落兼容,cli.py status 判读零改自动受益(pid 存活+新鲜窗方向) | test_cron_jobs.py 3 例:双写者死一活一判活/清死同胞保异机/最新鲜龄 | e8d7801 | 并行交付,本流验证 |
| 2 | **已修**:claim_is_live 负时长容忍(−FIRE_CLAIM_TTL 300s 容差内视为活);远未来仍 stale「永不楔死」红线不变,owner 证死仍立失效 | test_cron_jobs.py 2 例:回拨 −4min 认领保持/远未来 1h 仍可回收 | e8d7801 | 并行交付,本流验证 |
| 3 | **已修(双管)**:store.py 临界区读基线+落盘戳不匹配 ⇒ 字段级 3-way 合并(我方 diff 覆写/他方未触字段保留/整行恢复照旧/同字段我方赢);jobs.py 认领心跳写节流(TTL/2=150s,60s 节奏 2-3 跳落一次盘)削写放大 | test_cron_store.py 4 例(他方字段存活/同字段我方赢/删除不复活/整行恢复)+ test_cron_jobs.py 节流 1 例,owner_scoped 随契约更新 | e8d7801 | 并行交付,本流验证 |
| 4 | **注记收口**:tick() docstring 就地落「锁覆盖同步派发期/长 job 他宿主静默/坍缩为一发 F1.4」设计语义知悉,不做异步派发翻修(主人令允许缓解+文档) | —(文档) | e8d7801 | 并行交付,本流验证 |
| 5 | **注记收口**:fail-open 取向保留;WARNING+exc_info 留痕于 HEAD 既有(occurrences.py `Cannot check completed occurrence`),docstring 补裁决依据(重发代价=多跑一轮幂等管线,反向=射点无声消失) | 既有面由 test_cron_occurrences.py 覆盖 | e8d7801 | 并行交付,本流验证 |
| 6 | **注记收口(defer)**:无活宿主时无人杀孤儿子进程属定义性边界;收紧需子进程侧 ppid/death-signal 自监视(pipeline 域,darwin 无可移植 death-signal),cron 域不翻修;新宿主首 tick killpg+账本 unknown 是现存兜底 | —(文档) | e8d7801 | 并行交付,本流验证 |
| 7 | **已修**:Stage A no-op 占位桩移除,缺 `execute_job` 的 `tick()`/`run_ticker_loop()` 一律 ValueError(serve/CLI/sidecar 三宿主均已注入 CronRunner);假成功面归零 | test_cron_tick.py 2 例:缺 runner 契约(无假成功/预算不耗/槽不吞/账本空)+循环 fail fast;原桩契约测试随之更新 | e8d7801 | 并行交付,本流验证 |
| 8 | **最小修+注记**:手编垃圾 claimed_at 的 julianday→NULL 失序,列表/游标/窗口三处 COALESCE(-1) 定序为确定「最老」;全表删旧与窗口子查询按 1000 行终态帽注记知悉(排序面钉死亚毫秒) | test_cron_executions.py 1 例:垃圾戳恒垫底+游标翻页可达+窗口 latest 不受染 | e8d7801 | 并行交付,本流验证 |
| 9 | **已修**:扫描失败写专用 `heartbeat_scan_last_error` marker(与 ticker_last_error 死活面分立互不染),成功一扫即清;`cron status` JSON 键 `heartbeat_scan_error`+人读告警行双面可见 | test_cron_jobs.py 生命周期 1 例+test_cron_tick.py 循环隔离/清面 2 例+test_cli.py CLI 契约 1 例 | e8d7801 | 并行交付,本流验证 |

**本流验证门禁(2026-10-06 12:47 亲跑)**:`uv run --all-extras pytest tests/cron tests/alerts tests/cli/test_cli.py -q` → **463 passed in 29.44s**;`uv run --all-extras ruff check src/myssia/cron/ src/myssia/cli.py tests/cron/ tests/cli/test_cli.py` → All checks passed;`ruff format --check` 同面 12 文件会重排,与 HEAD~1 基线计数**完全一致**(e8d7801 零新增格式漂移,沿 2022bd9 在案先例)。

**本流操作事故披露(已闭环)**:基线比对期间一次 `git stash --keep-index --include-untracked` 误卷并行会话在途件;逐文件比对后全部复原——push 面 7 文件 stash 内容与 f299432 已提交内容逐字节一致(零丢失)、ai-news.yaml 未提交块恢复原位(` M` 态回归并行国产流预期形态)、hermes 流垫片 package.json 恢复后与 4e97a40 HEAD 一致(零损伤);stash 栈已清空。
