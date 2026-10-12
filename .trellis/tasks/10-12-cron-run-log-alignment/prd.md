# cron/CLI 跑次日志对齐补全(2 级空白根治)

## 现象(主人报障,10-12)

2 级详情大量「成功」轮空白,日志体显示「该跑次早于日志对齐落库,无可回看的日志」。
实证(截图 #78 daily-digest 为今日 08:05 cron 跑次,**不是**老行)。

## 根因(已实锤,两层)

1. **会话号只覆盖 sidecar run.start 一条路**:`entry.py:3585` 完成 回填
   `set_run_log_run_id(latest.id, run_id)` 只发生在注册表 worker;cron 定时跑
   按 B14 铁律是**独立子进程**(`cron/runner.py run_subprocess` → CLI
   `myssia run`),其 runs 行走 CLI 路径,从不分配/回填会话号。
   实测:库里 80 行,79 行无号;唯一有号 = 10-06 UI 手动触发的 myia-demo。
   即 **定时跑次(列表的绝大多数)天然全部空白**。
2. **logs.tail 够不着子进程日志**:`_m_logs_tail` → `myssia/log.py ring_snapshot`
   只读 sidecar 进程内存环(`_RING`,serve 启动盘尾回填一次)——cron 子进程的
   JSONL 行落盘但进不了环;就算补了号,跨进程行也拉不到。
3. 文案误导:NULL ≠ 早于落库(cron 新行也是 NULL),时间断言是错的。

## 修复设计(executor 零歧义)

- **会话键 = runs 行自增 id**:`store.start_run()` 在跑次开始即插行(sqlite.py:2077),
  id 天然唯一、单写者(该子进程自己)。CLI/Pipeline 路径:拿到 start_run 返回的
  row id 后设日志上下文,使该进程后续 JSONL 行 `run_id` 字段 = 此 id(pipeline.py
  现有 run 日志上下文挂接点);完成时 `set_run_log_run_id(row_id, row_id)`。
  sidecar run.start 注册表路径**不动**(两编号空间并存,UI 已按 log_run_id 对齐)。
- **logs.tail 盘扫回退**:`_m_logs_tail` 带 `run_id` 过滤时,除内存环外加扫数据根
  `logs/myssia-*.jsonl` 轮转文件(保留 7 天,界内有界;按 entry.run_id 过滤后取尾),
  与环结果按 seq/ts 合并去重。无 run_id 过滤的缺省语义**不变**(仍纯内存环)。
- **文案**:`run-detail-view.tsx` 降级句改「该轮未记录日志会话号,无可回看的日志」
  (去时间断言;补号后此态只剩真正的遗留行)。
- 测试:CLI 路径打标+回填单测;logs.tail 盘扫回退(run_id 命中跨进程行/未命中
  空 result 不报错);组件测试文案断言随改;冒烟夹具补一条「无号行」断言降级句。

## 边界

- 不动 B14 子进程隔离、不动 sidecar 注册表编号空间、不动 JSONL 轮转保留策略。
- run.start 回填的 `latest_run()` 启发式在并发完成时可能误挂邻行(既有薄弱面,
  本档顺手收窄:改为按本次 start_run 已知 row id 回填——sidecar worker 若拿不到
  row id 则维持现状,不强扩)。

## AC

- [ ] AC1 cron 触发一轮采集后,其 runs 行带 log_run_id,2 级可回看该轮 JSONL 日志。
- [ ] AC2 手动 run.start 路径回归不破(有号行照旧回看)。
- [ ] AC3 无号遗留行降级句如实(不再断言「早于落库」)。
- [ ] AC4 门禁(pytest 相关面 + vitest + tauri build)绿;装机换装。
