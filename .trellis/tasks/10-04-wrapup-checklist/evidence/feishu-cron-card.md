# hermes-cron 运行摘要卡真发飞书「AI福利群」— 收卡验证证据

- 执行时间:2026-10-04 18:40–18:42(主人机器,Darwin arm64)
- 执行人:主控代跑(W1 冒烟既定先例:真发一张卡进主人自己的群;只发一张摘要卡,绝不刷屏)
- 结论:**✅ 真发成功,一张摘要卡经 feishu:AI福利群 定向投递;跑完即删 job、沙箱即弃、凭据即用即废**

## 执行链(四步,全部真跑)

### 1. 凭据(~/.hermes/profiles/ai-analyst/.env → env)

- 键名先读确认:该文件含 `FEISHU_APP_ID` / `FEISHU_APP_SECRET`(另有 FEISHU_DOMAIN/CONNECTION_MODE/GROUP_POLICY)。
- 仓库无换取代码(`src/myssia/push/feishu_card.py:117` 凭据引用 = `env:FEISHU_BOT_TOKEN`,手工换取的 tenant_access_token;10-03-messaging-core design.md:75 同约定),故按 W1 冒烟同法用 APP_ID/SECRET 现换:
  `POST https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal` → **code=0, expire=7200, token_len=42**(令牌落沙箱 `chmod 600` 临时文件,不回显终端、不落证据)。

### 2. 通道目录(现有数据根已含,未触发 refresh)

- 仓库根(现有数据根)`channel_directory.json` feishu 桶已含 **AI福利群(chat_id=oc_5fdad6bc0f6155d6bdabecb25b82f9e4, type=group)** —— 与任务给的前缀一致,按任务门控「没有则现刷」判定**无需** `channels refresh`。
- 沙箱数据根 `/tmp/myia-cron-feishu-card/` 建好后副本拷入,`feishu:AI福利群` 由 `ChannelDirectory(数据根)` 名字解析命中(解析失败会报 `[target_unresolved]`,W1 步骤 4 负对照已证非静默回退)。

### 3. 沙箱 + 本地 static_html fixture(确定性,免外网)

- 沙箱数据根:`/tmp/myia-cron-feishu-card/`(job 注册表 cron/jobs.json、账本 cron/executions.db 均在此,不碰仓库 myia.db)。
- fixture:`python3 -m http.server 8813 --bind 127.0.0.1` 服务 `plugins/index.html`(3 条 `article.post` 条目);品类 YAML `plugins/feishu-cron-card.yaml` = static_html 引擎 + list 抽取 + `push: [{channel: stdout}]`(**条目推送走 stdout,只有 --deliver 的运行摘要卡走飞书——一张卡的保证**)。两份 fixture 文件随档:`feishu-cron-card-artifacts/fixture.yaml` / `fixture-index.html`。
- 建 job(真实命令):
  `myssia cron create "every 1m" --category /tmp/…/feishu-cron-card.yaml --db /tmp/…/myia.db --deliver feishu:AI福利群 --name feishu-card-once --json`
  → job **id=03928b7a8201**,interval every 1m,next_run_at=18:41:54。
- 触发+真发:`myssia cron run 03928b7a8201 --db …`(manual 立即跑,免等自然到期)→ `myssia cron tick --db …`,tick 日志全文见 `feishu-cron-card-artifacts/tick1.log`,关键三行:

```
18:40:59,927 spawning: …python3 -m myssia.cli run /private/tmp/myia-cron-feishu-card/plugins/feishu-cron-card.yaml --db … --json
18:41:00,845 Cron 摘要已投递: job=03928b7a8201 spec=feishu:AI福利群
18:41:00,845 Cron job 'feishu-card-once' finished: ok
```

### 4. 只此一张 + 清理

- tick 完当秒 `myssia cron remove 03928b7a8201` → `{"removed": true}`;`cron list --all` 确认无 job(沙箱 jobs.json 无可再触发者;仓库侧无 serve 守护盯着该沙箱数据根)。全程仅此一次 tick、仅此一张卡进群。
- 清理完成:httpd 已停(8813 端口已关)、`rm -rf /tmp/myia-cron-feishu-card`(含 .token 令牌文件)、`unset FEISHU_BOT_TOKEN FEISHU_APP_ID FEISHU_APP_SECRET`(env 中 FEISHU* 计数=0;本流程令牌本就只活在各命令进程内)。

## 验证对照(任务口径逐项)

| 验证点 | 结果 | 证据 |
| --- | --- | --- |
| SendReport ok | ✅ | `src/myssia/cron/summary.py:397-400`:任一 report `not r.ok` 会先 return 错误串(397-398),打不出 400 行「已投递」日志;tick 日志打出「Cron 摘要已投递」即全部 SendReport ok=True。且数据根无 `delivery_ledger.json`(死信账本只记失败,`src/myssia/push/delivery.py:232`)= 零死信 |
| API 200 | ✅(以 code=0 信封判定) | feishu `_parse_response`(`src/myssia/push/feishu_card.py:565-574`,573 行要求信封 `code==0` 否则 PushSendError)→投递报错;本次零错误 ⇒ 飞书服务端 HTTP 200 族 + code=0。字面 HTTP 状态行未入日志(httpx logger 未在 CLI 日志面开启),如实注记;此口径与 W1 冒烟「ok=True items=1(卡片到达飞书服务端)」一致 |
| executions 行 | ✅ | `myssia cron runs --db … --json` → 1 行:job_id=03928b7a8201, source=tick, **status=completed, error=null**, run{status=ok, exit_code=0, items=3, push stdout ok=true};直查 `cron/executions.db`(SQLite)同形;全文 `feishu-cron-card-artifacts/executions.json` |
| 摘要 markdown 落盘 | ✅ | `cron/output/03928b7a8201/2026-10-04_18-41-00_223425.md`(1153 字节)落沙箱,即卡内同文;副本 `feishu-cron-card-artifacts/summary-card.md` |
| 条目真实采集(非空跑) | ✅ | httpd 访问日志 18:41:00 `GET /index.html 200`(`feishu-cron-card-artifacts/httpd-access.log`);run 汇总 sources ok=1/1、items=3、条目留存 3 |

群内目视由主人确认(出站-only 链路无回执,与 W1 同口径)。

## 工件清单(evidence/feishu-cron-card-artifacts/)

`tick1.log`(tick 全日志)· `summary-card.md`(卡内摘要同文)· `executions.json`(账本行)· `fixture.yaml` / `fixture-index.html`(品类与 fixture)· `httpd-access.log`(fixture 抓取访问记录)
