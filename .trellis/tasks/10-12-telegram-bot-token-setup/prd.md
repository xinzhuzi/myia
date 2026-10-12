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
