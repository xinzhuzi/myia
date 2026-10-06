# design.md — 10-06-telegram-telethon 技术设计(执行级)

## D1 双宿主架构(照 cron serve 判例)

- **批量档(引擎面)**:`engine: telegram` 链外引擎——run 时拉一次窗口消息(getUpdates offset / Telethon iter_messages 增量),进管线走既有过滤出口;适合排程采集(与 16 源同律)。
- **常驻档(serve 面)**:`myssia telegram serve` 常驻宿主——长轮询/事件监听,秒级过粗筛→精筛→即时推(主人「每时每刻过滤」);与 cron serve 同款骨架(tick 锁不共用,各自独立;账本复用 executions 形态新表 telegram_events)。
- 两档共用:过滤管线、凭据解析、去重键、出口铁律。

## D2 引擎/宿主契约

### 批量引擎(engine: telegram,urlwatch/prompt 判例)
```yaml
- name: telegram-<群名>
  engine: telegram
  url: "https://api.telegram.org"          # 锚
  engine_options:
    telegram:
      chat_id: "-100xxxx"                   # 目标群/频道
      bot_token: keychain:myia/telegram/bot-token
      lookback_limit: 100                   # 单轮窗口帽
```
- 条目:消息文本=content,消息 id 铸锚 `#tg-<chat_id>-<message_id>`(全期幂等);媒体组聚合为一条(文本缺失取 caption,再缺=跳过)。
- 凭据三态:未配=credential_missing 显式空态零请求(同 reddit 先例)。

### 常驻宿主(serve)
- bot 线:getUpdates long_polling(timeout=25s),offset 持久数据根;断线指数退避;
- telethon 线:事件监听(telethon 事件循环在线程,asyncio 桥接判例同 urlwatch to_thread);session 文件落数据根 telegram/(0600),api_id/hash+session 路径入钥匙串;
- 过滤管线:关键词粗筛(配置表,零成本)→命中→LLM 精筛(glm-4-flash,提示词配置)→高价值=即时出口(合并铁律:同轮多条并一条)/普通=入库;
- 「每时每刻」语义:bot=秒级;telethon=事件级(秒内)。

## D3 依赖与组件轨(链接者)

- bot 线:零依赖(httpx 既有);
- telethon:**extras 组件轨**(`myssia[telethon]`,uv/桌面锁照 crawl4ai 组件判例:设置页组件卡=下载/就绪检查/失败可见;**不改 Telethon 源码**);
- 桌面锁:lock 扩 `--extra telethon`(llm extras 同款手法,指纹变更走设置一键重装)。

## D4 风险与边界

| 风险 | 处置 |
|---|---|
| bot 隐私模式(看不到普通消息) | 指引进凭据缺失消息与文档:BotFather /setprivacy 关闭 |
| 账号风控(telethon) | 小号建议入档+首登验证码流程 CLI 交互;session 失效=结构化告警+重登指引,不静默 |
| 限频 | bot 保守轮询(≥1s 间隔);telethon 走 FloodWaitError 服从退避 |
| 凭据泄露 | 钥匙串 only;token/session 不落日志(错误消息脱敏,saaS 同款纪律) |
| 只读边界 | 不实现发送/回复(另档);telethon 只 iter/监听,不 call 写接口 |

## D5 测试设计(全 mock 零真网)

- 引擎:凭据三态/窗口拉取/锚点幂等/媒体组聚合/失败词表(mock httpx);
- serve:长轮询循环/mock 事件流→粗筛→精筛→出口合并;断线退避;session 失效告警;
- 组件轨:lock 钉版/就绪检查/失败可见(mock 子进程);
- 真发:AC1/AC2 各一条端到端回执。
