# 照抄 Hermes:蓝本深度对标与对齐

## Goal

主人令「照着Hermes写好的去做」——深读蓝本 ~/.hermes/hermes-agent:飞书双机器人的分工与实现、cron jobs.json 里主人真实运行的监控任务与 deliver 形态、日报/告警的消息设计;对照 MYIA 现状产出偏离表,把可照抄的部分(任务编排/通道用法/消息形态)对齐落地。

## Requirements

- TBD

## Acceptance Criteria

- [ ] TBD

## Notes

- Keep `prd.md` focused on requirements, constraints, and acceptance criteria.
- Lightweight tasks can remain PRD-only.
- For complex tasks, add `design.md` for technical design and `implement.md` for execution planning before `task.py start`.

---

> **骨架补记(2026-10-06 三段纪律巡检)**:本档 prd 此前保持 TBD 骨架,实际执行与回执落 research.md 与 task.json notes;巡检补过程/结果回填段如下,条目均为既有在档记录的指针,未新造内容。Requirements/AC 仍 TBD 属实记录(需求原文由 task.json description 承载)。

## 过程(执行流水,回填位)

- [x] 蓝本深度排查(双机器人实证/三层偏离/照抄三批次建议)——research.md §1-§4;回执见 task.json notes「深度排查交付」
- [x] 批次4 合并日报(Hermes 版式照抄):store_report 引擎+daily-digest 场景件+既有品类 digest 路由降噪,提交 8d3ed63(12 文件 +1419/−29),测试 37 例+全量 4580 passed——research.md §5.2
- [ ] 批次1 日报消息形态对齐(feishu text 模式+deliver 缺省 home)——待主人圈定开工(research.md §3)
- [ ] 批次2 双机器人分流——待圈定(research.md §3)
- [ ] 批次3 prompt 任务形态——待圈定(research.md §3)

## 结果(验收回执,完工填)

- [x] 排查交付回执:三层偏离表+照抄三批次建议(task.json notes,status=review)
- [x] 批次4 真发回执:PM 槽 111 条渲染 16 条目发主人 DM 1 条(env:FEISHU_CHAT_ID,凭据零外显);同槽二次重跑 dedup_seen=1 幂等静默;生产 cron 挂点(job fb85edaf94ac)+装机外科重签+装机态装载校验——research.md §5.3
- [ ] 批次1-3 验收(待开工后回填)
