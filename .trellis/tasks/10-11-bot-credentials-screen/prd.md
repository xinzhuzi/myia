# 机器人凭据屏:设置推送分区抽独立屏 + 凭据位扩全通道

主人选型(2026-10-11):侧栏「配置」组抽「机器人凭据」独立屏,与账号屏并列(账号/机器人语义各是各);同时凭据表单从 5 通道预设扩到已实装全通道。

## 背景

- 裁定语义(10-11-platform-account-config):本身账号 ≠ 推送机器人。配置组现有 YAML配置/Telegram/飞书/微信(账号面);机器人凭据面在 设置→推送,且**表单只预设 5 通道**(feishu_card/telegram/webhook/bark/apprise),其余通道(qqbot/wecom/dingtalk/slack/discord/email 等)凭据无 GUI,只能 YAML/keychain 手工。
- 主人问「其他渠道怎么没有」→ 选定:抽屏 + 扩全通道。

## 方案

1. **抽屏**:设置→推送分区(settings-screen.tsx 通道清单式配置:通道 Select + 凭据表单 + 保存(secret.set)+ 发送测试(push.test)+ 自定义凭据位兜底)抽为独立屏 `/bot-credentials`,侧栏「配置」组挂「机器人凭据」条目(与 Telegram/飞书/微信并列);设置屏原分区摘除留注释(照 Telegram 分区抽出先例)。
2. **扩通道**:PUSH_FIELDS_BY_CHANNEL 按「已实装通道集合」(platform-overview implemented 集合为基准)补齐凭据位;多字段通道(email/matrix/feishu_card 双字段)按字段集铺开;自定义凭据位兜底保留。
3. **发送测试**:逐通道 target 惯例对照 PUSH_TEST_TARGET_KEY 既有 5 例;push.test 协议不动。

## Acceptance Criteria

- [ ] TBD(探查回填后定稿:通道清单以探查表为准)

## Notes

- 协议面 secret.set/push.test 不动;channel 通道声明/启停仍在品类 YAML(写回走 /yaml-editor)。
- UI 范式:/bot-credentials 独立屏(PageHeader 无头)+ 侧栏配置组 + 命令面板;IA 断言同步。
