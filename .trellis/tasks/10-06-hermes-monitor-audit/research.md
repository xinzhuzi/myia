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
