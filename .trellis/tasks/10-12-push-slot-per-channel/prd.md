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

## 终局回执(10-12 17:1x)

- 活体验证:换装后真跑 news(双通道,run 92)——telegram 通道**零「同槽位拦截」**,
  真去发送(digest=1);feishu 各发各的(ok=True)。telegram ok=False 的失败原因
  = `env_var_missing: TELEGRAM_BOT_TOKEN 未设置`——**既有凭据缺口**(B 线 bot
  token 在案),非本修问题;配好 token 后摘要即双通道真达。
- 门禁:push/store/pipeline/telegram/alerts 面 1631+88 全绿;全量 pytest 我方
  相关面全过(3 红归因并行在途新文件 feishu/skill-doc);tauri 打包绿,装机件
  17:0x 换装。
- 提交 82def31;测试断言迁移 5 例(digest 登记/immediate 登记/重投闸门对拍/
  partial-success 防丢失/resume 不双推/双向压制)。
