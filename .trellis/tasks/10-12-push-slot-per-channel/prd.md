# 推送槽位防重按渠道分键(双通道互拦根治)

## Goal

主人报障(#88 详情日志 20 条「摘要同槽位拦截 channel=telegram」):news.yaml 双通道(feishu+telegram)下,去重注册表键=条目级不含渠道,feishu 先发即把 telegram 全拦——双通道配置实际只出第一通道摘要。修复=should_send/record_push 加 channel 维度进键,调用面四处全传,存量裸键行自然退役(items 去重先拦旧条目,无补发效应)。

## Requirements

- TBD

## Acceptance Criteria

- [ ] TBD

## Notes

- Keep `prd.md` focused on requirements, constraints, and acceptance criteria.
- Lightweight tasks can remain PRD-only.
- For complex tasks, add `design.md` for technical design and `implement.md` for execution planning before `task.py start`.
