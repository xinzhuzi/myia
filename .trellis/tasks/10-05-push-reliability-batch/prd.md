# 推送可靠性与平台升级批(深度对拍产出全量执行)

## Goal

Hermes 深度对拍(2026-10-05,上游钉死 af90026)产出的缺口与升级项**全量落地**
(主人「按照你的建议去做,都弄上」),以动态工作流四路并行执行,终局
全量门禁+换眼复审+装机换装。

## Requirements(四路,白名单互斥)

- **R1 投递重试账本**(缺口①):immediate 推送 at-least-once。蓝本 Hermes
  `gateway/delivery_ledger.py`(pending→attempting→delivered/failed→abandoned、
  MAX_ATTEMPTS=3、退避 30s/120s、24h 过期、启动 sweep)。MYIA 形态=持久化
  重试队列 JSON(数据根,原子写),pipeline 推送阶段失败且**非死信/非配置错**
  入队,每次 run 推送阶段先 flush 到期条目;时钟可注入。
  白名单:src/myssia/push/retry_ledger.py(新)、digest.py、delivery.py、
  src/myssia/pipeline.py、tests/push/test_push_retry_ledger.py(新)。
- **R2 飞书/TG 发送护栏**(缺口②③):飞书=瞬态重试(指数退避,可注入
  sleeper,常量化次数)+reply 失效码降级新消息(话题内不降级,对齐上游
  `_FEISHU_REPLY_FALLBACK_CODES`)+卡片长度护栏(超阈值拆多卡);telegram=
  retry_after 优先退避(timeout 永不重试,5xx/429 指数退避 ≤3 次)。
  蓝本:feishu `adapter.py:3925-3970`+8000/4000 常量;telegram
  `senders.py:70-96`。白名单:src/myssia/push/feishu_card.py、telegram.py、
  tests/push/test_feishu_retry.py(新,不改旧断言)。
- **R3 signal+bluebubbles 出壳**(升级①②):从结构化壳升真出站。蓝本
  `gateway/platforms/signal.py`(SIGNAL_HTTP_URL,JSON-RPC)与
  `bluebubbles.py`(SERVER_URL+PASSWORD,REST);凭据走
  resolve_channel_credential(env→myia/push/<ENV_KEY> 回退,同
  push-credential-journey 口径);服务不可达=结构化 transient。消息屏
  platform-overview 同步:signal 出 UPCOMING 入 IMPLEMENTED(带凭据指南,
  指路设置→推送)、bluebubbles 出 EXTRAS_SHELL_PLATFORM_IDS;__init__.py
  W3 注记更新(**仅本路碰 __init__.py**);python 壳断言改真发送断言;UI
  scoped vitest+tsc 绿。白名单:signal.py、bluebubbles.py、__init__.py、
  platform-overview.tsx、messaging-screen.test.tsx、platform-icons.test.tsx、
  tests/push/test_messaging_signal.py、test_messaging_bluebubbles.py。
- **R4 discord/slack 目录发现**(升级③):discover_directory 实装(仓内范式
  =feishu_card.py:586:翻页/限流退避/ChannelEntry 映射)。蓝本
  `channel_directory.py:174-197`(discord guild 枚举 text+forum)与
  `:235-317`(slack users.conversations 20×200+info 补名)。能力注记写在
  discord.py/slack.py 自身 docstring(**不碰 __init__.py**,避免与 R3 冲突);
  cli.py channels refresh 帮助文案若写死「当前:feishu」则同步。白名单:
  discord.py、slack.py、src/myssia/cli.py(仅文案行)、
  tests/push/test_messaging_discord.py、test_messaging_slack.py。

## Acceptance Criteria

- [ ] AC1(R1):瞬态失败的 immediate 批次入队→到期重投→3 次耗尽 abandoned
  →24h 过期清理→成功出队→死信不入队→原子写容错,全部有测试(fake clock)。
- [ ] AC2(R2):飞书瞬态重试/降级/拆卡、TG retry_after 退避逐错序列断言;
  既有 tests/push 零回归。
- [ ] AC3(R3):signal/bluebubbles 真发送路径(MockTransport)替壳
  dependency_missing 断言;消息屏两家状态/指南/UI 测试同步;scoped
  vitest+tsc 绿。
- [ ] AC4(R4):discord/slack 发现(翻页聚合/限流退避/补名)测试在案;
  channels.refresh 链路零协议变更。
- [ ] AC5:全量门禁=pytest 全量+vitest 全量+tsc build 绿(白名单域必须绿;
  并行在途外来红如实分类记档不拦本批);ruff 绿。
- [ ] AC6:每路 pathspec 提交(--only)零外来混入;蓝本锚注记+MIT 全部落。
- [ ] AC7:装机换装(worktree HEAD 构建静默换装)+装机版健康冒烟;回执留档。
- [ ] AC8:换眼复审(独立上下文读四路 diff)发现项修复或如实标注。

## Constraints

- 不 push;共享工作树并行会话在途——只碰白名单,staged 零停留(index.lock
  冲突 sleep 3 重试);绝不改 ~/.hermes 下任何文件;测试零外网零真发
  零真实钥匙串。
- 外部平台真凭据冒烟(signal/bluebubbles/discord/slack)留主人——依赖
  主人侧服务与凭据,如实入 notCovered。

## Notes

- 上游事实单与本批出处:journal 2026-10-05「消息模块×Hermes 深度对拍」段。
- 执行载体=动态工作流(主人 /workflow 令);本档=需求与验收权威。
