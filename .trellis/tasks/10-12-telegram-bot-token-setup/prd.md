# telegram bot 凭据配置(推送通道真达)

## Goal

配置 TELEGRAM_BOT_TOKEN,让 news 等双通道品类的 telegram 摘要真达。

## 背景(run 92 实证)

- 渠道分键修复(82def31)后 telegram 通道已真发送,唯一失败原因=
  `env_var_missing: TELEGRAM_BOT_TOKEN 未设置,钥匙链规范名 myia/push/TELEGRAM_*`;
- 凭据动作归主人(浏览器代办纪律:主人明文发凭据才代办,用完即弃+劝轮换)。

## Requirements

1. 主人侧:BotFather 取 token → 按钥匙链规范名写入(或经设置屏凭据面,若
   机器人凭据屏已支持 telegram——侧栏已有「机器人凭据」入口,先核覆盖面)。
2. 验证:下轮 news 采集 telegram 通道 ok=True,摘要真达主人 TG。

## Acceptance Criteria

- [ ] AC1 token 配置后一轮真跑 telegram 推送 ok=True(日志实证)。

## 边界

- AI 不代取凭据;只立档推动+配置后验证。

## grill 决议表(2026-10-12 深化;配置路径事实已核)

| # | 问题 | 决议 | 依据 | 可翻案 |
|---|------|------|------|--------|
| G1 | token 配置入口 | **UI 两分钟路径:设置 → 机器人凭据 → telegram**:填 TELEGRAM_BOT_TOKEN(@BotFather 令牌,必填)+ TELEGRAM_CHAT_ID(可选,给 bot 发条消息后消息屏目录自动记)→ 存钥匙链 myia/push/*,推送解析 env 缺失自动回退 | bot-credentials-screen.tsx:82-84 表单在;push/telegram.py:452/533 钥匙链回退对上 | 否(实证) |
| G2 | AI 侧工作 | 零开发;验证=主人配完后下一轮 news/cron,JSONL「推送完成 channel=telegram ok=True」+ 主人 TG 收到卡片 | run 92 已证链路通,唯缺 token | 否 |
| G3 | chat_id 可选性 | 缺省时推送层自动发现(消息屏目录);不拦配置 | 屏内 hint 原文 | 是 |
