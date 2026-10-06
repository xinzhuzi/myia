# research.md — 10-06-hermes-align:蓝本深度排查(主人令「照着Hermes写好的去做」)

## §1 双机器人(实证)

| 机器人 | 凭据位置 | 形态 | 用途 |
|---|---|---|---|
| 主 agent | ~/.hermes/.env FEISHU_APP_ID/SECRET | websocket 长连接双向(DM+群,@提及门控,Typing/表情回应,卡片按钮) | 通用交互 agent;主群=「AI中转站合伙人群」oc_f38a…(=FEISHU_HOME_CHANNEL,MYIA 现用此凭据 ✓);另有主人 DM oc_9a79… |
| ai-analyst | ~/.hermes/profiles/ai-analyst/.env 独立 FEISHU_APP_ID | 同机制独立 profile(multiplex) | 分析员机器人(独立人格/任务面) |

## §2 Hermes 怎么做「监控」(与 MYIA 的三层偏离)

1. **任务形态(最大偏离)**:Hermes cron job=自然语言 prompt → `hermes chat -Q` 跑一次 agent 轮(bot_chat_delivery.py:727;agent 带浏览器/工具自己去查网站)→ 摘要=agent 的回答。MYIA=YAML 机械管线(引擎/选择器/模板)。Hermes 形态下「AI厂商监控」=一句话建 job,无需选择器工程。
2. **投递形态**:preferred_message_type="text"——日报=agent 写的 markdown 文本(adapter.py:281,455-481 md tag rows+4000 字拆分),经 im/v1/messages 发群;deliver 默认 home channel(scheduler_delivery.py:origin/home/explicit/bot-chat 四目标);MYIA=feishu_card 交互卡片(拆卡不截断,已通)。
3. **通道机制**:WebSocket 长连接双向(可对话可回应);MYIA=单向 API 推送。

## §3 照抄批次(建议序)

- **批次1(小)**:日报消息形态对齐——feishu 通道增文本 markdown 模式(照抄 Hermes md rows+4000 拆分实现在 plugins/platforms/feishu/adapter.py:455-481);cron deliver 缺省从 local 改 home。
- **批次2(中)**:双机器人分流——MYIA 通道增第二套飞书凭据键(ai-analyst 应用),告警走二号、日报走一号(照抄 multiplex 分工)。
- **批次3(大,产品级)**:prompt 任务形态——MYIA cron 增自然语言 job(照 hermes chat -Q:一轮 LLM+浏览工具,产出即摘要,deliver 走通道)。给 MYIA 装 Hermes 的灵魂:一句话定义监控。

## §4 主人 Hermes 实况旁证

cron/jobs.json 现空、executions 账本仅 1 笔(2026-09-24 direct)——主人对 Hermes 的 cron 用得少,但消息/机器人设施(channel_directory 2026-10-06 仍在更新)活跃;.ai-analyst profile 在册。
