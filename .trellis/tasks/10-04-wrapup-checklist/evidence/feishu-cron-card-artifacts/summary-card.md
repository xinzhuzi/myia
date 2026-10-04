# cron run feishu-card-once

- command: `/Users/zhengbingjin/Project/Github/MYIA/.venv/bin/python3 -m myssia.cli run /private/tmp/myia-cron-feishu-card/plugins/feishu-cron-card.yaml --db /tmp/myia-cron-feishu-card/myssia.db --json`
- exit: 0  status: ok

**feishu-card-once** · 定时运行摘要
- 品类:/private/tmp/myia-cron-feishu-card/plugins/feishu-cron-card.yaml
- 状态:✅ ok · 退出码 0
- 时长:0.1s
- 源:1 个,正常 1 / 失败 0,采集条目 3
- 条目留存:3
- 推送:stdout(immediate 0 / digest 3 / archive 0)

```json
{
  "job": {
    "id": "03928b7a8201",
    "name": "feishu-card-once",
    "category": "/private/tmp/myia-cron-feishu-card/plugins/feishu-cron-card.yaml"
  },
  "run": {
    "status": "ok",
    "exit_code": 0,
    "timed_out": false,
    "run_id": 1,
    "dry_run": false,
    "duration_seconds": 0.0724,
    "error": null
  },
  "sources": {
    "total": 1,
    "ok": 1,
    "failed": 0,
    "items": 3
  },
  "items_retained": 3,
  "push": [
    {
      "channel": "stdout",
      "ok": true,
      "immediate": 0,
      "digest": 3,
      "archive": 0
    }
  ],
  "failures": [],
  "failure_count": 0
}
```
