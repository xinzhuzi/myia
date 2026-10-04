# 顶栏清理+模块控件归位(主人判「顶栏没用,具体功能放具体模块」)

## Goal

主人 2026-10-04 目验:顶栏品牌字/面包屑/品类下拉/跑一次/搜索框在设置等屏全无作用,模块分割不清。修法=拆全局万能顶栏为各屏上下文控件:跑一次→源管理/定时任务、品类过滤→情报流/日志、品牌→侧栏已有删顶栏重复、面包屑删(侧栏即导航)、⌘K 留全局但仅图标触发不加假搜索框。各屏只留自己需要的控件

## Requirements

- TBD

## Acceptance Criteria

- [ ] TBD

## Notes

- Keep `prd.md` focused on requirements, constraints, and acceptance criteria.
- Lightweight tasks can remain PRD-only.
- For complex tasks, add `design.md` for technical design and `implement.md` for execution planning before `task.py start`.
