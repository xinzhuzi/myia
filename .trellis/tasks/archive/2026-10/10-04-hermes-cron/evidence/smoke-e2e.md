# 端到端冒烟(第 2 轮)— 2026-10-04 12:49–12:54 +08:00

任务:.trellis/tasks/10-04-hermes-cron;目标 = 验证「建 job → serve 常驻 → 跑一遍 → 摘要落盘 → 状态可查 → 清场」全链。
**结论:全链 PASS。** 第 1 轮断链点(B1 执行体未注入 serve)已由 B2 接线修复并经本轮真跑证实。

配套原始产物:`evidence/smoke-e2e-artifacts/`(serve.log、两份摘要 .md、jobs.json 快照)。

## 0. 第 1 轮断链点复核(修复在位)

- `src/myia/cli.py:112` — `from myia.cron.runner import CronRunner`(在位)
- `src/myia/cli.py:1778` — `kwargs={"interval": interval, "execute_job": CronRunner(cron).execute}`(在位;`_cmd_cron_serve` docstring cli.py:1767-1768 注明 B1 接线 G2)
- `src/myia/cron/ticker.py:123-130` — `run_ticker_loop(cron, stop_event, *, interval, execute_job=None, ...)` 接受注入
- 桌面 sidecar 同位接线参照 `desktop/entry.py:4269`(`"execute_job": _execute`)
- 运行时证实:serve.log 中 **`grep -c "cron runner not injected" serve.log` = 0**(第 1 轮每个 fire 一条 WARNING),每个 fire 改走 `myia.cron.runner: Cron job 'smoke-cron' spawning: ... -m myia.cli run ... --json`。

## 1. 沙箱与 fixture(全程零外网)

- 沙箱 `MYIA_HOME=/tmp/myia-cron-smoke`(先 `rm -rf` 后建;开跑前实测不存在,无第 1 轮残留)
- 本地源:`python3 -m http.server 8799 --bind 127.0.0.1 --directory /tmp/myia-cron-smoke/fixtures`(PID 64623;`curl` 回 200/1038 bytes)
  - `fixtures/index.html`:3 个 `article.post` 条目(虚构内容)
- 品类 `plugins/smoke-cron.yaml`:engine=static_html、extract list `article.post`、classify builtin、dedup `{url}`、push stdout、storage retention 30d
  - 首版 YAML 缺 `schedule` 字段被 schema 拒(exit 1 `$.schedule missing_field`),补 `schedule: "0 9,21 * * *"` 后通过——属 fixture 修正,非产品缺陷
- **预检**(自行追加,非 ask 要求):`MYIA_HOME=… uv run myia run <yaml> --db … --json` → exit 0、status success、3 items、stdout 恰一份 JSON;随后 **删除 myia.db 重置**,保证 runs 表两行全部来自 serve 的 fire
- 口径(沿用第 1 轮):任务文写 `uv run shishi`,实际入口是 `myia`(0a085cc 反转改名),本轮用 `uv run myia` 同参数执行

## 2. 建 job

```
$ MYIA_HOME=/tmp/myia-cron-smoke uv run myia cron create "every 1m" \
    --category /tmp/myia-cron-smoke/plugins/smoke-cron.yaml \
    --db /tmp/myia-cron-smoke/myia.db --deliver local --name smoke-cron
已建定时 job:smoke-cron(id=e58ba8433bad)
  schedule: every 1m
  下次运行: 2026-10-04T12:50:20.146972+08:00
  品类: /private/tmp/myia-cron-smoke/plugins/smoke-cron.yaml
create exit=0
```

## 3. serve 常驻 ≥2 周期

`nohup env MYIA_HOME=… uv run myia cron serve --db … > serve.log 2>&1 &`(PID 65082)。serve.log 全文:

```
12:49:24 INFO myia.cron.ticker: Cron ticker started (interval=60s)
12:49:24 INFO myia.cli: myia cron serve:常驻宿主已启动(数据根 /tmp/myia-cron-smoke,interval=60s,Ctrl-C 停)
12:50:24 INFO myia.cron.tick: Running job 'smoke-cron' (ID: e58ba8433bad)
12:50:24 INFO myia.cron.runner: Cron job 'smoke-cron' spawning: …/.venv/bin/python3 -m myia.cli run /private/tmp/…/smoke-cron.yaml --db /tmp/myia-cron-smoke/myia.db --json
12:50:24 INFO myia.cron.runner: Cron job 'smoke-cron' finished: ok
12:52:24 INFO myia.cron.tick: Running job 'smoke-cron' (ID: e58ba8433bad)
12:52:24 INFO myia.cron.runner: Cron job 'smoke-cron' spawning: …(同上)
12:52:24 INFO myia.cron.runner: Cron job 'smoke-cron' finished: ok
```

两 fire 间隔 120s(完成时刻重锚 + due 落 tick 后滑档,第 1 轮已观察并如实记录的口径行为,jobs.json 快照 lateness_seconds=60.0 佐证;非断链项)。

## 4. 验证(sqlite3 实查 + CLI)

**runs 表(myia.db,预检重置后全部由 serve fire 产生)≥2:PASS**

```
id  category    status   started_at                        finished_at
1   smoke-cron  success  2026-10-04T04:50:24.223900+00:00  2026-10-04T04:50:24.275740+00:00
2   smoke-cron  success  2026-10-04T04:52:24.221940+00:00  2026-10-04T04:52:24.272254+00:00
```

**executions 表(cron/executions.db)≥2 且带摘要:PASS**(第 1 轮 run_summary_json 非空行数=0)

```
id                                job_id        status     source  summary_len
c61be28b2e384a01b2879e5b74976bf1  e58ba8433bad  completed  tick    460
f499bfe9d5804c1da4314fbd859b47ef  e58ba8433bad  completed  tick    460
```

**output/<job_id>/ 摘要 ≥2 份且含状态/留存数:PASS** — `cron/output/e58ba8433bad/` 下 2 份 `.md`(+1 份 `.log`),每份均含:

```
- 状态:✅ ok · 退出码 0
- 时长:0.1s
- 源:1 个,正常 1 / 失败 0,采集条目 3   ← 第 2 fire 为 0(dedup 挡掉同 URL,静态源预期行为)
- 条目留存:3                            ← 第 2 fire 为 0,同上
- 推送:stdout(immediate 0 / digest 3 / archive 0)
```

**cron status 心跳新鲜:PASS** — `✓ ticker 活着(心跳 33s 前,上次成功 33s 前)`(新鲜判据 3×60+20=200s,cli.py:1322)

**cron runs 出摘要:PASS** — 两行均 `[completed] …(含运行摘要)`

**cron list 状态正确:PASS** — `smoke-cron [scheduled] id=e58ba8433bad / next_run … / last_status: ok  deliver: local`

## 5. 清场(铁律,全部成功)

1. `cron remove e58ba8433bad` → exit 0,`jobs.json` → `{"jobs": [], …}`
2. 杀 serve:`pkill -TERM -f "myia\.cli cron serve --db /tmp/myia-cron-smoke"` + `kill -TERM 65082` → 2s 后 `ps` 全树扫 `myia cron|myia\.cli|myia-cron-smoke` 零匹配
3. 杀 http.server:`kill -TERM 64623` → `ps -p 64623` 死透;`lsof -nP -iTCP:8799 -sTCP:LISTEN` 空(端口释放)
4. 删沙箱:`rm -rf /tmp/myia-cron-smoke` → `ls` 报 No such file or directory
5. 终扫:`ps aux | grep -E "myia cron|myia\.cli|myia-cron-smoke|http\.server 8799"` 零匹配;仅剩的 3 个 http.server(18923/17923/17931)系开跑前就在的无关进程(Downloads/q21-round4 等),按界不动

## 6. 与第 1 轮失败点逐项对账

| 第 1 轮失败点 | 本轮结果 |
|---|---|
| B1 执行体未注入 serve(tick 落 no-op stub,WARNING 每 fire 一条) | PASS:cli.py:1778 注入在位;serve.log 0 条 WARNING,2 次 `myia.cron.runner spawning` |
| myia.db 不存在、runs 表 0 行 | PASS:runs 2 行均 success(且为预检重置后由 serve 产生) |
| output/ 目录空 | PASS:2 份 .md(+1 .log),含状态/留存数 |
| run_summary_json 非空 = 0、CLI 无「(含运行摘要)」 | PASS:2 行 summary_len=460;`cron runs` 两行均带「(含运行摘要)」 |
| every 1m 实际 120s 间隔(口径观察,非断链) | 仍在(本轮 2 fire 同样 120s;重锚滑档口径行为,如实记录) |
