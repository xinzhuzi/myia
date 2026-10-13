# 情报流详情弹窗整屏化(主人个案明示独占画布)

## Goal

主人令(2026-10-11 看图反馈):详情弹窗太小,要整个界面,一眼看出所有数据——独占画布判例的主人明示场景。改 feed 详情 Dialog:近全窗尺寸(去 max-w-xl)+正文去 max-h-72 帽(主滚动区承接)+动作簇常驻底栏。轻量档 PRD-only。

## Requirements

- feed 详情 Dialog 近全窗(去 max-w-xl)+正文去 max-h-72 内滚帽(主滚动区承接)+动作簇常驻底栏。

## Acceptance Criteria

- [x] AC1 全屏画布形态落地(6f55129,10-12 12:37):feed-screen.tsx `data-fullcanvas="true"` 结构(:1813)+vitest +2 断言(feed-screen.test.tsx:544)在库;装机重打包换装;后续 8f47727/dd8ee11 大改 feed 屏均保留该形态(2026-10-14 档务核亲证代码在位)。

## Notes

- Keep `prd.md` focused on requirements, constraints, and acceptance criteria.
- Lightweight tasks can remain PRD-only.
- For complex tasks, add `design.md` for technical design and `implement.md` for execution planning before `task.py start`.
