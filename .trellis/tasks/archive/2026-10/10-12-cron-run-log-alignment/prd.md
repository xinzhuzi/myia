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

## grill 决议表(阶段①质询定稿;执行注:工作流 dwfrun-59488108 因子代理池
配额窗(1308,15:42 重置)中断于 grill 首问,按主人「继续做哇」+「勿定时直接做」
判例转主会话直执,方法=grilling 设计树/前沿轮次,事实全部读码落定,零升级问)

| # | 前沿问题 | 决议 | 依据(读码实证) | 可翻案 |
|---|---------|------|----------------|--------|
| D1 | 会话键选什么 | **runs 行自增 id** | start_run 即插即返唯一 id(sqlite.py:2077);单写者=跑该行的进程;UI 对齐键 log_run_id 已建模(api.ts RunHistoryEntry) | 是 |
| D2 | JSONL 行 run_id 打标挂哪 | **log.py 进程级 run 上下文(ContextVar)+ `_entry_from_record` 缺省回落**;Pipeline.run() 在 start_run 后 bind、finally clear | 行 run_id 现从 record extra 读(log.py:140);引擎/三方日志不带 extra,逐调用改不现实;ContextVar 同 task await 链传播、线程不传播(后台线程隔离正确);sidecar 注册表子进程同时被 _pump_stream 盖注册表号——extra 优先于回落,两编号空间不串(stream_line 显式注入优先) | 是 |
| D3 | 盘扫触发与边界 | **带 run_id 时总是「环+盘」合并**;去重键 `(ts, run_id, line)`;文件界=数据根 logs/ 全部保留内文件(≤7 个,按日升序);无 run_id 语义不变(纯环) | stream_line 经 root 漏斗进环+盘同 ts 同行(log.py:379-406)→三 元组去重恰好折叠 sidecar 双写;子进程自标行(row id)与注册表号不同键天然不混;_read_tail 坏行容忍先例(log.py:194);桌面单机日志 MB 级、展开详情才拉,性能可受 | 是(「仅环空才盘扫」是备选,现决议取语义简单) |
| D4 | 完成回填谁做 | **Pipeline.run() finally 自回填 `set_run_log_run_id(run_id, run_id)`(非 dry),尽力而为(WARNING 吞异常)**;sidecar worker 3585 现状不动(其 latest_run 误挂是既有薄弱面,注册表行终值=注册表号,后写覆盖自回填,秩序正确:子进程先写自 id,worker 完成后覆盖注册表号) | dry 用 :memory: store(pipeline.py:1217-1220)会产假 id,故 dry 不 bind 不回填;runs 行插入在先、终态在后,自回填与 finish_run 同 store 同事务面 | 是 |
| D5 | 前端降级文案 | **「该轮未记录日志会话号,无可回看的日志」**(去时间断言);vitest 断言随改 | NULL ≠ 早于落库(cron 新行也是 NULL,#78 实证);补号后此态只剩真遗留行 | 是 |
| D6 | 断点续跑/接管路径 | 新 run 新行新号自然覆盖;被接管旧行维持 NULL→如实降级,零额外工作 | 接管 finish_run(pipeline.py:1581)只落终态不动 log_run_id | 否(自然语义) |
| D7 | 测试面 | pytest:bind/回落/clear、pipeline 自回填(含 dry 不回填)、盘扫合并(跨进程行命中/无 run_id 不变/坏行容忍/去重);vitest:文案;冒烟:夹具补无号行断言降级句 | 门禁既有分工:py 面归 pytest、UI 语义归 vitest、布局归无头冒烟 | 是 |

AC 不变(AC1-AC4 原文);边界补充:**base Store 契约若无 set_run_log_run_id 则
pipeline 侧 getattr 防御**(实测仅 sqlite.py:2110 有,base 未列——实现时按此办)。
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

> 终局回执(10-12 15:5x):AC1 活体证据=CLI 真跑 news.yaml(--db 显式指真库,
> 与 cron 子进程同路径):runs 行 88|news|success|log_run_id=88 自回填,今日
> JSONL 32 行按 run_id=88 打标(proc=cli);盘扫合并面由协议测试
> test_logs_tail_run_id_merges_disk_rows 实跑(跨进程行可达/双写折叠/缺省
> 纯环)。AC2=run.start 全链路协议测试 252 绿。AC3=冒烟无号行降级断言+
> vitest 新文案断言。AC4=全量 pytest 5421 过/vitest 762/build/冒烟/tauri
> 打包全绿;装机件 15:53 换装(PID 5972)。换装前旧行(telegram 84-87 等)
> 维持 NULL 如实降级;telegram serve 宿主落库路径是否经 Pipeline.run 待
> 下轮自然分晓(不經则如实降级,不在本档范围)。

- [x] AC1 cron 触发一轮采集后,其 runs 行带 log_run_id,2 级可回看该轮 JSONL 日志。
- [x] AC2 手动 run.start 路径回归不破(有号行照旧回看)。
- [x] AC3 无号遗留行降级句如实(不再断言「早于落库」)。
- [x] AC4 门禁(pytest 相关面 + vitest + tauri build)绿;装机换装。
