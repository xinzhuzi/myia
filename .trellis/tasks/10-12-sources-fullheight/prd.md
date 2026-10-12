# 源管理屏满高布局:表格区铺满视口

## Goal

主人实测:源管理表格到分页即止,下方大片空底——屏根容器缺 h-full(对照情报流/配置编辑屏均 flex h-full min-h-0)。修法=屏根 h-full+表格区 flex-1+SourcesTable 满高(边框容器内滚,分页钉底);Kestra full-container 范式补完(源码注释本就自称 full-container 但从未实现高度)

## Requirements

- TBD

## Acceptance Criteria

- [ ] TBD

## Notes

- Keep `prd.md` focused on requirements, constraints, and acceptance criteria.
- Lightweight tasks can remain PRD-only.
- For complex tasks, add `design.md` for technical design and `implement.md` for execution planning before `task.py start`.
