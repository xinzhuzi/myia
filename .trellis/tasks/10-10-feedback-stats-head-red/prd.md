# feedback stats 契约测试 HEAD 预存红(bad 计数 0≠1)

## Goal

tests/feedback/test_feedback.py::TestCliFeedback::test_cli_list_and_stats_json_contract 在 HEAD(2026-10-10,stash 归因排除 urlwatch 修复档改动)即红:反馈记录成功落库(feedback_id=1 verdict=bad)但 stats 聚合 bad==0,疑似反馈统计聚合或测试夹具回归;单跑即红非顺序性。2026-10-10 全量门禁 5072 passed 唯一红

## 症状与证据(2026-10-10)

- 失败:`assert stats["stats"]["bad"] == 1` 实得 0(test_feedback.py:665)。
- 落库面正常:captured log `反馈已记录 feedback_id=1 verdict=bad channel=cli item_id=1
  dedup_key=https://x/stats` → 记录成功,统计聚合输出 bad=0(写读两侧有一侧错)。
- 归因:单跑即红(非顺序性);stash 掉 10-10-urlwatch-adapter-discovery 全部改动后
  在 HEAD 树上同样红 → 预存,与该修复档无关。
- 2026-10-10 全量门禁:5072 passed / 1 failed(即本例)/ 40 skipped。

## Requirements

- TBD

## Acceptance Criteria

- [ ] TBD

## Notes

- Keep `prd.md` focused on requirements, constraints, and acceptance criteria.
- Lightweight tasks can remain PRD-only.
- For complex tasks, add `design.md` for technical design and `implement.md` for execution planning before `task.py start`.
