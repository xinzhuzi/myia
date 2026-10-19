# s74源选择器失效修复(74站页面改版)

## Goal

2026-10-19 羊毛真网dry-run发现:s74(tkkgv8.gicp.fun)整源invalid_item(url=None,62条全灭),.card-url@href选择器取不到链接=页面改版;生产10-18两轮wool run同为partial同因。修法:firecrawl重渲染实测新DOM改extract选择器。非wool-quality-gate任务范围,独立小档。

## Requirements

- TBD

## Acceptance Criteria

- [ ] TBD

## Notes

- Keep `prd.md` focused on requirements, constraints, and acceptance criteria.
- Lightweight tasks can remain PRD-only.
- For complex tasks, add `design.md` for technical design and `implement.md` for execution planning before `task.py start`.
