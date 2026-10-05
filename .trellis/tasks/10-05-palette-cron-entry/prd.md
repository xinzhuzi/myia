# 命令面板缺「定时任务」屏条目(SCREENS 七屏清单漏 cron)

## Goal

全链自测实证(dwf‌run-a25f5cbc 视觉验收):command-palette.tsx:47-55 SCREENS 仅七屏、注释自称路由表七屏,但 App.tsx:38 与 sidebar 均有 cron 屏——⌘K 面板无法导航到定时任务,只能走侧栏。修法=SCREENS 加一行+命令面板测试同步;轻量档 PRD-only。

## Requirements

- TBD

## Acceptance Criteria

- [x] SCREENS 补行:command-palette.tsx:52 增 `/cron`「定时任务」(Clock=sidebar.tsx:46 同款;位次=源管理后,与 App.tsx:38/sidebar 一致;keywords「cron schedule timer jobs」;落 303f57b+529af11)
- [x] 测试同步:command-palette.test.tsx 八屏期望+「定时任务」条目,新增 cron 关键词过滤/Enter 导航 2 例;vitest 单文件 21/21 绿(2026-10-05 实跑)
- [x] 门禁全绿(脚本统一执行,2026-10-05 收尾档确认)

## Notes

- Keep `prd.md` focused on requirements, constraints, and acceptance criteria.
- Lightweight tasks can remain PRD-only.
- For complex tasks, add `design.md` for technical design and `implement.md` for execution planning before `task.py start`.
