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

- [x] AC1(R1):瞬态失败的 immediate 批次入队→到期重投→3 次耗尽 abandoned
  →24h 过期清理→成功出队→死信不入队→原子写容错,全部有测试(fake clock)。
  - 证据:tests/push/test_push_retry_ledger.py 30 用例逐项对上——入队
    (test_transient_immediate_failure_enqueues_with_first_backoff)/到期重投
    (test_run_flushes_due_retry_at_push_stage)/30s-120s 退避档与 3 次耗尽
    abandoned(test_backoff_tiers_30_120_then_final_strike+
    test_exhausted_entry_abandoned_and_kept_for_observation)/24h 过期
    (test_stale_entry_expired_after_24h)/成功出队(test_delivered_entry_leaves_queue)/
    死信与配置错不入队(test_dead_error_never_enqueues)/原子写容错
    (test_atomic_write_leaves_no_tmp_and_file_always_parseable+
    test_corrupt_file_degrades_to_empty_then_rewrites)/全程 fake clock
    (test_full_heal_loop_with_fake_clock);落库载体 d613310(收编)+换眼复审
    R1-high 修复 9b9b540(定向重投回归 test_targeted_retry_resends_to_resolved_
    target_not_exploded)+复审二轮 338faa4(防重发闸门拦重投/零报告误判
    mark_delivered 永久丢,/tmp/r1_repro.py 复现+slot_dedup 开关+三形回归,
    tests/push 1091 批注);本收口重跑 tests/push 1088 全过(exit 0,f64c0ef)。
- [x] AC2(R2):飞书瞬态重试/降级/拆卡、TG retry_after 退避逐错序列断言;
  既有 tests/push 零回归。
  - 证据:tests/push/test_feishu_retry.py 27 用例(飞书瞬态退避逐错序列+reply
    失效码降级+卡片长度拆分+telegram retry_after,grep retry_after 命中该文件);
    末次槽降级烧槽位缺陷两笔修复 a371526/4863430(503×2→230011 逐错序列
    复现+回归用例);本收口干净 worktree(f64c0ef)重跑 `pytest tests/push -q`
    =1088 passed in 15.12s exit 0=零回归。
- [x] AC3(R3):signal/bluebubbles 真发送路径(MockTransport)替壳
  dependency_missing 断言;消息屏两家状态/指南/UI 测试同步;scoped
  vitest+tsc 绿。
  - 证据:7502a0c 恰好白名单九文件;test_messaging_signal.py 21+
    test_messaging_bluebubbles.py 23 用例壳断言已改 MockTransport 真发送断言;
    消息屏 messaging-screen.test.tsx/platform-icons.test.tsx 随 7502a0c 同步;
    批内门禁 tests/push 1060+messaging 66+tsc+build 绿(7502a0c 批注);
    复审二轮 adcdbc5(signal 应答校验 fail-closed:200+JSON 缺 result 不再
    放行,测试+2,tests/push 1093 批注);本收口重跑 vitest 全量 23 文件 433
    全过+npm run build(tsc+vite)exit 0(两笔复审修复均纯 python,UI 面不变)。
- [x] AC4(R4):discord/slack 发现(翻页聚合/限流退避/补名)测试在案;
  channels.refresh 链路零协议变更。
  - 证据:f143000 恰好白名单四文件,test_messaging_discord.py 30+
    test_messaging_slack.py 32 用例(guild 两跳翻页聚合/限流退避/info 补名);
    channels.refresh 链路零协议变更=d556bb7 仅 src/myssia/cli.py 帮助文案
    6+/3-,零协议文件改动。
- [x] AC5:全量门禁=pytest 全量+vitest 全量+tsc build 绿(白名单域必须绿;
  并行在途外来红如实分类记档不拦本批);ruff 绿。
  - 证据(本收口干净 worktree f64c0ef 重跑):pytest 全量 3964 passed/32
    skipped/2 failed(92.69s)——两红均外来域非本批白名单:①tests/plugins/
    test_plugin_packages.py 七 compose 断言红,系 plugin-market 批二
    0195806/7df322b/66ace59 增三 compose 未随测试(该线修复正以未提交形态
    在主树,预期集恰增 crawlab/worldmonitor/webcheck);②tests/test_skill_doc.py
    枚举表红,系 60e2f52 schema.ENGINES 增 zenrows/scraperapi 未随 SKILL.md
    (该提交 stat 无 skill 文件);白名单域(tests/push+消息屏 UI)全绿。
    ruff check=All checks passed(exit 0);vitest 全量 23 文件 433 全过;
    npm run build(tsc+vite)exit 0。批内锚:d613310 收编时全量 3935 过。
    复审二轮后代码尖(adcdbc5)复跑:pytest 全量 3969 passed/32 skipped/
    同两外来红(90.95s)、tests/push 1093 全过(15.32s)、push 域 ruff 绿。
- [x] AC6:每路 pathspec 提交(--only)零外来混入;蓝本锚注记+MIT 全部落。
  - 证据:R3=7502a0c 九文件、R4=f143000 四文件+d556bb7 文案单文件、R2 修复
    4863430/f64c0ef 面收敛,皆白名单内;R1/R2 原始实装载体为 d613310 收编
    提交(源头会话 3h 无活动,telegram 156 行等并行在途改进随收、全量 3935
    门禁验后落库)——载体偏离 pathspec 纪律如实注记于此,非静默混入;
    蓝本锚注记+MIT:Hermes af90026 在 d613310/7502a0c/f143000/4863430/
    9b9b540 批注全落。
- [x] AC7:装机换装(worktree HEAD 构建静默换装)+装机版健康冒烟;回执留档。
  - **终局刷新(03:06)**:换装 b72fee4(=f64c0ef+复审修复 338faa4/adcdbc5+纯文档;备份 /tmp/世事.app.bak-wf2-030701;回执 /tmp/wf2-install.exit=ok installed,装机版 secret list 静默+cron list exit=0)。HEAD f2e0194 首刷因并行打包线 Cargo sha2 依赖未提交(pyenv.rs 已入库而 Cargo.toml/lock 躺工作树)于 worktree 构建必炸,未采——该线补齐依赖提交后下次装机自刷。
  - 证据:回执 /tmp/wf-batch-install.exit=「ok installed
    f64c0ef225c7942f486a44eef691dc9ce736e14f bak=/tmp/世事.app.bak-wf-025213」
    (worktree HEAD f64c0ef 干净构建静默换装,世事.app 132.24 MiB);装机版
    /Applications/世事.app/Contents/MacOS/myssia-core secret list=两条凭据名
    exit=0 零授权框、cron list --json=exit 0。谱系注记:装机钉版 f64c0ef
    (换装毕 02:52),其后的复审二轮两笔 338faa4(02:54:44)/adcdbc5(02:57:05)
    未随包——循 0355528 判例如实注记,下次装机自刷。
- [x] AC8:换眼复审(独立上下文读四路 diff)发现项修复或如实标注。
  - 证据:复审产出五笔全落——9b9b540(批注「R1 换眼复审 R1-high」:定向重投
    spec 逐字符炸开,修复+回归用例)、4863430(R2:降级烧槽位 AssertionError
    逐错序列复现+修)、f64c0ef(R2 换眼复审:蓝本偏离归属伪托如实化,行为
    零改动,tests/push 1088+ruff 绿)、338faa4(R1 二轮:防重发闸门拦重投+
    零报告误判 mark_delivered,/tmp/r1_repro.py 复现+修,tests/push 1091)、
    adcdbc5(R3 二轮:signal 应答校验 fail-closed,tests/push 1093)。

## Constraints

- 不 push;共享工作树并行会话在途——只碰白名单,staged 零停留(index.lock
  冲突 sleep 3 重试);绝不改 ~/.hermes 下任何文件;测试零外网零真发
  零真实钥匙串。
- 外部平台真凭据冒烟(signal/bluebubbles/discord/slack)留主人——依赖
  主人侧服务与凭据,如实入 notCovered。

## Notes

- 上游事实单与本批出处:journal 2026-10-05「消息模块×Hermes 深度对拍」段。
- 执行载体=动态工作流(主人 /workflow 令);本档=需求与验收权威。
