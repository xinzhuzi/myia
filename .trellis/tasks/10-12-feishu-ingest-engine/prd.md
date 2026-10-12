# 飞书采集引擎:feishu 群消息入库

## Goal

主人令铺源发现:MYIA 无飞书采集引擎(feishu 只有推送)。新增 engines/feishu.py:Open API 轮询群消息(GET /im/v1/chats/{chat_id}/messages,复用推送区 FEISHU_APP_ID/SECRET 钥匙链凭据,message_id 去重,chat_id=oc_ 前缀源配置)+registry 注册+新品类 yaml(AI中转站合伙人群 oc_f38a491eae5baf19898de28107087f05)+真跑验证。若应用缺 im:message 只读权限,结构化报错指引主人加权限

## Requirements

- TBD

## Acceptance Criteria

- [ ] TBD

## Notes

- Keep `prd.md` focused on requirements, constraints, and acceptance criteria.
- Lightweight tasks can remain PRD-only.
- For complex tasks, add `design.md` for technical design and `implement.md` for execution planning before `task.py start`.
