# 多品类共享 TG bot token 409 修复:同 token 单轮询器

## Goal

真机 doctor(2026-10-05 晚)发现 games 与 news 两个品类共享同一个
`TELEGRAM_BOT_TOKEN`,双常驻(`myssia run --loop`)导致 Telegram API 返回
409 Conflict(getUpdates 并发冲突互踢)。这是产品缺陷而非配置错误:产品应
支持多品类共享同一 bot token 而不互踢。

## 背景与根因(代码实况)

- 轮询器:`TelegramFeedbackPoller`(`src/myssia/push/telegram_feedback.py`)
  —— 桌面形态无公网回调端点,靠 Bot API `getUpdates` 长轮询收卡片按钮
  反馈(grill Q7 定案)+ 被动积累会话目录(10-03 D2)。
- 接线:`Pipeline.run_forever`(`src/myssia/pipeline.py`)只要品类配了
  telegram 推送通道,就 `_build_feedback_poller()` 起后台任务
  `_feedback_poll_loop` 轮询。推送(send)与轮询(getUpdates)共用同一
  `env:TELEGRAM_BOT_TOKEN`(schema 不设 per-channel token 位)。
- 409 机制:每个 `myssia run <yaml> --loop` 是独立进程;games 与 news 两个
  常驻进程各起一个 getUpdates 轮询器、同 token 并发长轮询 → Telegram 对
  同 token 只允许一个并发 getUpdates 消费方,回 409 互踢,反馈接收双废。
- 现状缓解仅 `myssia doctor` 的 `telegram_token_poll_conflict` warning
  (提示部署侧裁决),库内不做任何互斥(旧文档明言"跨进程互斥不在库内
  实现")。

## 决议(主人批准的推荐方向)

1. 同一 bot token 至多一个 getUpdates 轮询器,由产品在库内保证:
   - **进程内注册表**按 token 摘要(sha256)去重,后到者禁动(不复用
     回调流——跨管线 fan-out 属架构改动,明言不做);
   - **跨进程文件锁**(flock LOCK_NB,蓝本 = `myssia/cron/tick.py` 的
     tick.lock 同款守卫导入与竞争 errno 判定):锁文件名含 token 摘要、
     内容只写属主 pid/品类(凭据零明文红线),抢不到锁的常驻进程禁动
     并记一次结构化日志。
2. 推送型使用方不受影响:单次 `run` 本就不轮询;轮询仍只在常驻模式启动,
   且租约抢不到时静默禁动(推送照常,只是不接收反馈)。
3. doctor finding `telegram_token_poll_conflict` 改写:从"会 409 互踢"改为
   披露新语义(先到常驻者独占接收,后到者禁动;反馈/目录只入先到者库)。
4. 禁止大改架构:不动 schema、不动 store、不加配置面;改动收敛在
   `push/telegram_feedback.py`(租约原语)+ `pipeline.py`(轮询循环接
   租约)+ `cli.py`(doctor 文案)。

## Acceptance Criteria

- [x] AC1 进程内去重:同进程内对同一 token 第二次获取轮询租约返回 None
  (禁动),第一次获取者在释放后可重新获取;不同 token 互不干扰。
  证据:`tests/push/test_messaging_telegram.py::TestPollLease::
  test_same_token_denied_until_release` / `test_release_is_idempotent`(绿)。
- [x] AC2 跨进程互斥(同机两进程语义):对同一锁文件,第二个独立的
  flock 持有方(绕过进程内注册表、模拟另一进程)存在时,获取租约返回
  None;持有方释放后可获取。
  证据:`TestPollLease::test_cross_process_holder_denies_then_allows`
  (独立 fd 抢先 flock 同一锁文件 → 禁动 → 放锁后可取);另
  `test_lock_file_holds_no_token_material` 钉死凭据红线(锁文件名/内容
  只见 sha256 摘要与 pid)。
- [x] AC3 409 回归复现 + 修复后行为:mock transport 下两个品类管线同 token
  常驻,修复前语义(双轮询器并发 getUpdates)由测试复现冲突计数;修复后
  仅持租约者发出 getUpdates 请求,另一方零请求、推送不受影响。
  证据:`TestTelegram409Regression::test_api_409_body_raises_structured_error`
  (Telegram 真实 409 回包形状 → 结构化 telegram_api_error)+
  `TestResidentTokenDedupe::test_second_resident_category_never_polls`
  (games 先到独占轮询且反馈入其库;news 零请求 + 禁动告警可诊断)。
- [x] AC4 既有行为不回归:未配 telegram 通道 / 凭据不可解析时轮询不启动
  (既有测试守住的边界不变);租约释放幂等;轮询循环取消(Ctrl-C)时
  租约被释放。
  证据:`TestPipelineWiring::test_poller_absent_without_telegram_channel` /
  `test_poller_absent_when_token_unresolvable`(既有,仍绿)+
  `tests/feedback/test_feedback.py::
  TestFeedbackPollLoop::test_loop_acquires_lease_and_releases_on_cancel`。
- [x] AC5 定向门禁:`uv run --no-sync pytest` 覆盖 tests/push(telegram
  反馈)、tests/feedback、tests/pipeline、tests/cli 相关用例全绿。
  证据(2026-10-05):`tests/push` 1099 passed / `tests/feedback` 77
  passed / `tests/pipeline` 111 passed / `tests/cli` 168 passed。
- [x] AC6 doctor 文案与新语义一致(多品类共配 telegram 不再宣称必然 409
  互踢,改为披露单接收方语义)。
  证据:`tests/cli/test_cli_full.py::
  test_multiple_telegram_categories_flagged_as_poll_conflict` 断言
  message 同时含「409」(平台约束)与「单轮询器」(库内防护);docs
  zh/en(getting-started、write-a-plugin)四处同步改写。

## Notes

- 凭据红线:锁文件名/日志/异常消息只出现 token 的 sha256 摘要,绝不出现
  token 本体。
- 反馈路由边界(如实披露):同 token 的反馈回调与会话目录观测只进"先到
  的常驻品类"的库;跨库分发是后续产品决策,本任务不做。
