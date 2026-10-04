# 命令面板缺「定时任务」屏条目(SCREENS 七屏清单漏 cron)

## Goal

全链自测实证(dwf‌run-a25f5cbc 视觉验收):command-palette.tsx:47-55 SCREENS 仅七屏、注释自称路由表七屏,但 App.tsx:38 与 sidebar 均有 cron 屏——⌘K 面板无法导航到定时任务,只能走侧栏。修法=SCREENS 加一行+命令面板测试同步;轻量档 PRD-only。

## Requirements

- TBD

## Acceptance Criteria

- [ ] TBD

## Notes

- Keep `prd.md` focused on requirements, constraints, and acceptance criteria.
- Lightweight tasks can remain PRD-only.
- For complex tasks, add `design.md` for technical design and `implement.md` for execution planning before `task.py start`.
