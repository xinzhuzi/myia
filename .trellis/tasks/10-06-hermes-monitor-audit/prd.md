# Hermes 系监控全量排查+沙盘模拟

## Goal

主人 2026-10-06 令:将 Hermes 里面的监控排查一遍、模拟一遍。排查面=src/myssia/cron 十模块(jobs.json/tick 文件锁 at-most-once/executions 账本/自然语言 schedule/deliver 摘要)含 10-05-cron-heartbeat 的久未触发心跳告警规则族;模拟面=沙箱数据根多形态 job(间隔/cron 式/一次性)真实触发→账本/并发锁/摘要/心跳告警全链验证+清历史残留 serve 进程;产出 research.md 排查表+模拟回执+发现修复。

## Requirements

- TBD

## Acceptance Criteria

- [ ] TBD

## Notes

- Keep `prd.md` focused on requirements, constraints, and acceptance criteria.
- Lightweight tasks can remain PRD-only.
- For complex tasks, add `design.md` for technical design and `implement.md` for execution planning before `task.py start`.
