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

## 结果(交付回执,2026-10-12)

- 代码 1 笔:屏根 h-full min-h-0 + 表格区 flex-1 + SourcesTable 满高(边框容器内滚)。
- 无头桥像素验证(dev 与装机件双验):分页底缘距视口底 24px(修复前数百 px);装机冒烟全 PASS;vitest 全量 762/762;tsc 绿。
- 装机:换装备份 /tmp/myssia-srcfull-backup-20261012-161600;strict verify 过;WKWebView 缓存清。转 review。
