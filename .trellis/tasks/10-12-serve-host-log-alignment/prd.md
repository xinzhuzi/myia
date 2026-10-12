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
