# serve 宿主跑次日志对齐(log_run_id 恒 1 修复)

## Goal

telegram/feishu serve 宿主(长驻线)落库的 runs 行 log_run_id 恒=1,2 级详情
logs.tail 对不上号;按 cron-run-log-alignment 同款语义修复(行 id 即会话键)。

## 背景(任务生成 agent 扫描产出,2026-10-12,实证)

- DB 实测:runs 90/91(telegram serve)、93-97(feishu serve)log_run_id 全=1;
  同期 CLI 行 92(news)=92 正确(10-12-cron-run-log-alignment 交付);
- =1 的成因假设(待实现者核):serve 宿主进程内 store 为独立连接,首行自增
  从 1 起,bind_run(run_id) 绑了**进程内号**而非主库行 id(或宿主不走
  Pipeline.run 自回填而由别处写死);
- 撞车标注:**telegram/feishu serve 域是并行会话在途面**(tg_web/web_thread/
  feishu.py 均 untracked 在途)——本档启动前先确认在途工作已落定。

## Requirements

1. 定位 serve 宿主落库路径(telegram serve / feishu serve 宿主)中 log_run_id
   的写入点,对齐「主库行 id 即会话键」语义(参照 pipeline.py 自回填)。
2. 修复后 serve 宿主新行 log_run_id=行 id;旧行(恒 1)不迁移,如实降级。

## Acceptance Criteria

- [ ] AC1 serve 宿主触发一轮采集,DB 新行 log_run_id=行 id(活体验证)。
- [ ] AC2 2 级详情可回看该轮日志(logs.tail 盘扫命中)。
- [ ] AC3 门禁绿(相关 pytest 面)+ 装机换装。

## 边界

- 不动 CLI/cron 已正确路径;不动并行在途文件(先等其落定)。

## grill 决议表(2026-10-12 深化;方法=grilling 设计树/前沿轮次,事实全部读码+DB+JSONL 实证)

| # | 前沿问题 | 决议 | 依据(实证) | 可翻案 |
|---|---------|------|------------|--------|
| G1 | 病根到底是什么 | **非 serve 宿主;= UI run.start worker 旧回填(entry.py:3585)覆盖** | 证据链三件:①runs 93-97(UI 触发)log_run_id=1,同期 98/99(cron 20:00,无 worker)log_run_id=98/99 正确;②JSONL 双写在盘:sidecar 转发版(外层 run_id=注册表号 1,proc=sidecar)+ 子进程原生版(run_id=行id,proc=cli)同文本并存;③频繁换装日每个 sidecar 会话首跑注册表号恒=1,worker 完成时 set_run_log_run_id(latest.id, 1) 覆盖了 CLI 自回填的正确值 | 否(实证) |
| G2 | 修法 | worker 回填改**条件回填:行 log_run_id IS NULL 才写**(旧行兼容);CLI 自回填(行id)为唯一权威值。_pump_stream 转发版(注册表号)不动——当前会话注册表行的 UI 回看靠它,环内自洽 | 3585 的覆盖在旧语义(注册表行走环)下曾是特性;10-12 起 DB 行对齐键=行id,覆盖变纯害 | 是 |
| G3 | 存量脏行(log_run_id=1) | **一次性回修**:UPDATE runs SET log_run_id=id WHERE log_run_id=1 AND id<当前——盘上原生行(proc=cli run_id=行id)在,回修有据;回修前后 SELECT 留档 | 93-97 全部有原生行在盘(rg 实证 96/97) | 是(不修则旧行如实降级亦可) |
| G4 | 验证 | 修后 UI 触发一轮 → DB 行 log_run_id=行id + 2 级详情 logs.tail?run_id=行id 命中**原生行**(不再只靠转发版);换装重启后历史行仍可回看 | — | 否 |

Requirements 按决议更新:原「定位 serve 宿主落库路径」改「改 entry.py:3585 为条件回填 + 存量回修脚本/SQL 一次性执行」。撞车标注维持(parallel telegram/feishu 在途,本档只动 entry.py 回填一行 + 数据回修,零交集)。

## G3 执行留痕(2026-10-12 22:36-22:49,真库回修 + 复查回滚)

- **备份**:`myssia.db.bak-20261012-logrun-fix`(回修前 22:37,integrity ok,99 行/max 99/脏 9 与活库一致);
  `myssia.db.bak-20261012-logrun-fix-id30-rollback`(id30 回滚前 22:48,sqlite3 `.backup` 一致快照,30=30 入档)。
- **改前 SELECT**(22:36:06):total=99,max_id=99,log_run_id=1 脏行 9;非空全景:
  30/myia-demo/1,88/news/88,89/telegram/1,90/telegram/1,91/telegram/1,92/news/92,
  93/feishu/1,94/feishu/1,95/feishu/1,96/feishu/1,97/feishu/1,98/ai-news/98,99/daily-digest/99。
- **UPDATE**(22:37):`UPDATE runs SET log_run_id=id WHERE log_run_id=1 AND id<(SELECT MAX(id) FROM runs)`,changes()=9(30,89,90,91,93-97)。
- **改后 SELECT**(22:37:08):脏 0,9 行 log_run_id=行id,total/max 99/99 不变。
- **有据核验**:89-97 原生 JSONL(proc=cli,run_id=行id)在盘 7-23 行/条(logs/myssia-20261012.jsonl);
  转发版(run_id=1,proc=sidecar)当日 189 行并存不动(G2)。
- **复查回滚 id=30**(22:48-22:49,挑刺轮发现):该行**无据**——原生 run_id=30 全日志目录 0 行
  (其轮 2026-10-06T21:34Z=本地 10-07 05:34,3.13s 短轮,仅转发版 3 行,在
  myssia-20261007.jsonl 的 run_id=1 混流[该文件 94 行]内);按 G3「无据不迁」与
  Requirements「旧行(恒 1)不迁移」处置:`UPDATE runs SET log_run_id=1 WHERE id=30`,changes()=1
  (混流可达优于零可达)。**终态**:全库仅 id=30 保留 log_run_id=1,其余非空行 log_run_id=行id。
- **工艺注**:改中活库 WAL 活跃(sidecar 长连接,98KB 未 checkpoint)——裸 cp 主文件不带 WAL
  会读到旧值假象(22:47 坏样本实证,已删);回滚前备份改用 sqlite3 `.backup` 一致快照
  (首份备份时 WAL 恰 0 字节,cp 无损)。

