# cron run dead-job

- command: `/Users/zhengbingjin/Project/Github/MYIA/.venv/bin/python -m myia.cli run /private/tmp/myia-cron-refix/plugins/smoke-dead.yaml --db /tmp/myia-cron-refix/myia.db --json`
- exit: 2  status: failed

**dead-job** · 定时运行失败
- 品类:/private/tmp/myia-cron-refix/plugins/smoke-dead.yaml
- 状态:❌ failed · 退出码 2
- 错误:Pipeline failed: all sources exhausted their engine chains.
- 日志尾部:
  -  776                               response = None
  -  777                           else:
  -  778 →                             raise RuntimeError(f"Failed on navigating ACS-GOTO:\n{str(e)}")
  -  779
  -  780                       # ──────────────────────────────────────────────────────────────
  -  781                       # Walk the redirect chain.  Playwright returns only the last
  -  782                       # hop, so we trace the `request.redirected_from` links until the
  -  783                       # first response that differs from the final one and surface its; firecrawl:http_502:firecra…

```json
{
  "job": {
    "id": "fa4aeb2fd8d1",
    "name": "dead-job",
    "category": "/private/tmp/myia-cron-refix/plugins/smoke-dead.yaml"
  },
  "run": {
    "status": "failed",
    "exit_code": 2,
    "timed_out": false,
    "run_id": 2,
    "dry_run": false,
    "duration_seconds": 42.9897,
    "error": "Pipeline failed: all sources exhausted their engine chains."
  },
  "sources": {
    "total": 1,
    "ok": 0,
    "failed": 1,
    "items": 0
  },
  "items_retained": 0,
  "push": [
    {
      "channel": "stdout",
      "ok": true,
      "immediate": 0,
      "digest": 0,
      "archive": 0
    }
  ],
  "failures": [],
  "failure_count": 0
}
```
