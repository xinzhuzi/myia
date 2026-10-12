# TG会话进即已读(角标归零)

## Goal

主人令(2026-10-12 看图反馈):点击进监控会话,左栏未读角标应归零(TG 式进会话即已读)。角标口径=store.source_stats 全库未读,故须源级全量标已读:set_all_item_states/mark_all 增 source 精确等值作用域;UI 进 TG 会话(chatView)时自动 storeStateMarkAll({source})+stats 重拉。轻量档 PRD-only。

## Requirements

- [x] 全链已落:store set_all_item_states/mark_all 增 source 精确等值;UI 进 TG 会话自动 storeStateMarkAll({source})+stats 重拉角标归零;未读档顺手切「全部」(刚读的不消失,跨群工作台定案不翻案)
- [x] 门禁:pytest 5306/0+vitest 745/745+build 绿;装机重打包换装+重签 strict+装机包方法签名实证
- [x] 测试:协议 source 作用域(隔离/空串拒)+vitest 行为(mark_all 带 source+时间线不消失)+历史用例适配新语义

## Acceptance Criteria

- [ ] TBD

## Notes

- Keep `prd.md` focused on requirements, constraints, and acceptance criteria.
- Lightweight tasks can remain PRD-only.
- For complex tasks, add `design.md` for technical design and `implement.md` for execution planning before `task.py start`.
