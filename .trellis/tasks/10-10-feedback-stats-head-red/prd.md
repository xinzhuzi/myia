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

## 根因(2026-10-10 定谳)

**测试时间炸弹,产品无病**:`test_cli_list_and_stats_json_contract` 种子反馈冻结在
`NOW = 2026-10-02 12:00 UTC`,而被测的 CLI `feedback stats` 按 `tuner.stats` 缺省
**真实墙钟**切 7 天窗口——2026-10-09 20:00(本地)起种子跌出窗口,bad 计数 0≠1,
必红。该文件其余 tuner 测试全部显式注入 `now=NOW`(`apply(now=...)`)永确定性,
唯此一例经 CLI 边界漏墙钟。

## 修法

种子改真实当下(`record_feedback` 缺省 `datetime.now(timezone.utc)`),并留注记
说明为何此处不可用冻结 NOW。纯测试修复,不触及 `src/`,装机包无需重打。

## Requirements

- TBD

## Acceptance Criteria

- [ ] TBD

## Notes

- Keep `prd.md` focused on requirements, constraints, and acceptance criteria.
- Lightweight tasks can remain PRD-only.
- For complex tasks, add `design.md` for technical design and `implement.md` for execution planning before `task.py start`.
