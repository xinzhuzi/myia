# 复查修补冒烟(AC6 口径补强 + 复查项 1/3 真跑验证)— 2026-10-04 13:14–13:17 +08:00

任务:.trellis/tasks/10-04-hermes-cron;触发 = 独立复查修补(六项发现的第 1/3/5 项)。
**结论:PASS。** 手动 `cron tick` 真派发(项 1 修复)、stdout 系 deliver spec 可用(项 3 修复)、AC6 的 deliver 定向到达 + failure_deliver 失败摘要到达在真跑面补齐(项 5)。

配套原始产物:`evidence/smoke-refix-artifacts/`(tick1.log 全程 stderr、两份输出文档、品类/fixture 副本、预检 JSON)。

## 0. 修复在位复核

- `src/myia/cli.py` `_cmd_cron_tick`:传 `execute_job=CronRunner(cron).execute`(与 `_cmd_cron_serve` 同款;复查项 1 修法)
- `src/myia/cron/summary.py` `deliver_run_summary`:platform == "stdout" → `_deliver_summary_via_stdout`(内存缓冲 + logger 回显,push.test 先例同款;复查项 3 修法)

## 1. 沙箱与 fixture

- 沙箱 `/tmp/myia-cron-refix`(rm -rf 后建;开跑前不存在)
- 本地源:`python3 -m http.server 8801 --bind 127.0.0.1`(curl 200/334 bytes);fixture 品类 `smoke-refix.yaml`(static_html list `article.post`、classify builtin:false、dedup {url}、push stdout、retention 30d)
- 失败品类 `smoke-dead.yaml`:同款但 url 指向 8802 死端口(无监听)
- 预检:`myia run smoke-refix.yaml --json` → exit 0、status success、items 3(首版 classify 未关被 builtin 全筛(classify_unmatched 3),fixture 修正后达标);`smoke-dead.yaml --dry-run` 装载合法(exit 2 为真跑死端口预期)
- **零情报外网**:源全走 127.0.0.1。如实注记:dead 品类的引擎链自动降级触达 L4 firecrawl 端点获 http_502(无凭据请求被拒),非情报访问;不影响验证目标

## 2. 建 job(AC6 原文口径 `--deliver <stdout/…>`)

```
myia cron create "every 1m" --category …/smoke-refix.yaml --db … --deliver stdout:debug --name ok-job
myia cron create "every 1m" --category …/smoke-dead.yaml  --db … --deliver local --failure-deliver stdout:debug --name dead-job
```

`cron run <id>` ×2(trigger)→ `myia cron tick --db …`(手动 tick,项 1 场景)→ exit 0,「派发 2 个 job」。

## 3. 验证(tick1.log + sqlite3 实查)

| 验证点 | 结果 |
|---|---|
| 手动 tick 真派发(项 1) | **PASS**:log 有 `Cron job 'ok-job' spawning: … -m myia.cli run … --json`;`grep -c "cron runner not injected"` = 0(无 no-op stub WARNING) |
| deliver 定向到达(AC6/项 3) | **PASS**:`Cron 摘要(stdout 通道回显): {"channel":"stdout","kind":"cron_summary",…,"text":"**ok-job** · 定时运行摘要\n…条目留存:3…推送:stdout(immediate 0 / digest 3 / archive 0)"}`;stdout:debug 不再报 [unknown_platform] |
| failure_deliver 收到失败摘要(AC6) | **PASS**:dead-job 失败卡经 stdout:debug 回显,含「❌ failed · 退出码 2」「Pipeline failed: all sources exhausted their engine chains.」+ stderr 尾部 + 输出文档路径 |
| 三态语义(F1.7) | PASS:ok-job `last_status: ok`;dead-job `last_status: failed`(投递本身成功,无 delivery_failed) |
| executions 账本(D10) | PASS:一 [completed] 一 [failed],均「(含运行摘要)」 |
| runs 表(真跑管线落库) | PASS:`1|smoke-refix|success`、`2|smoke-dead|failed` |
| 输出文档 | PASS:`cron/output/<job_id>/*.md` 各 1 份(ok-job-summary.md / dead-job-summary.md 已随档) |

## 4. 口径注记(与 AC6/F3.3 原文的剩余偏差,如实登记)

- **未用官方 `plugins/news.yaml`**:其源为外网(gcores.com RSS),离线冒烟不可达;沿用 G2 第 2 轮先例的本地 static_html fixture(先例 smoke-e2e.md §1 同款)
- **未真发平台通道卡**(F3.3「定向卡入群」/W1 先例 feishu 入群):冒烟环境无平台凭据(feishu/telegram token 均未配置),真发不可行、不伪造;AC6 原文的 `<stdout/测试通道>` 面已由本轮 stdout 通道真跑覆盖,平台卡面由单测(RecordingChannel 范式,test_cron_runner.py)覆盖
- failure_deliver/deliver 平台 spec 定向到达的真跑面同上(凭据缺失);本轮覆盖 stdout 面

## 5. 清场(全部成功)

杀 http.server(PID 10885)→ `rm -rf /tmp/myia-cron-refix` → `ps` 扫 `myia-cron-refix|http.server 8801` 零残留。
