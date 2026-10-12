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

## 结果(交付回执,2026-10-12)

- **引擎**:engines/feishu.py(engine: feishu,Open API 群消息窗口;端点=GET /im/v1/messages?container_id_type=chat——直调实测 chats/{id}/messages 路由不存在);锚 #fs-<chat>-<mid> 全期幂等;v1 仅 text 出条目,机器人自身回声(sender_type=app)不回采;权限缺失 feishu_permission_denied 结构化指引,凭据全缺 credential_missing 显式空态。
- **凭据链**:env→keychain:myia/push/<键> 兜底(推送区 GUI 表单落点,resolve 后端=context 注入,生产 None=系统钥匙串——telegram 同款;发现并绕开管线 FetchContext 不注入 backend 的坑)。
- **真跑回执**:AI中转站合伙人群 13 条入库(两轮复验幂等;主人换 apiKey 后 token mint 复验仍通)。
- **门禁**:引擎测试 6 用例;schema 词表+registry+skill/SKILL.md 枚举表同步;全量 pytest 5483/5483;wechat 三例全量并发 flake(单跑 49/49 绿,与本改动无涉)。
- **装机**:包内 myssia-src 实证 FeishuEngine 在;换装备份 /tmp/myssia-feishu-backup-20261012-171707;app 重启后常驻 cron 按 */30 自动跑。
- **实机**:config/feishu-groups.yaml 已铺(仓库 config/ 同源);LLM 精筛键缺= tg_web 线合法降级纯粗筛(如实)。
