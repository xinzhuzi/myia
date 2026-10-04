# 推送凭据用户旅程接通(表单→钥匙链→运行时解析全链)

## Goal

用户**填一次凭据即可真收推送**:在设置屏按通道填好凭据 → 保存入钥匙链 →
真实 run 与发送测试同源解析,一条龙接通。消灭「教用户跑 curl / 改
~/.zshrc / 每 2 小时手工续 token / GUI app 根本读不到 env」的开发者级接入路。

## 背景与证据(2026-10-05 主人报「用户使用起来非常不方便」,当轮全链实核)

- 断链事实:品类 YAML push[] 的 target/凭据走 `env:` 引用
  (`pipeline._build_channel` 直传 → `resolve_credential` 只读 `os.environ`);
  GUI 启动的 app 不读 `~/.zshrc` → **用户照指南做完也收不到推送**
  (本机活证:四路实核 env 全空,真跑 feishu 报 `env_var_missing`)。
- 指南现状(`platform-overview.tsx` feishu steps):教用户 curl 换
  tenant_access_token、写入 ~/.zshrc、**约 2 小时过期手工重换**。
- 设置屏推送表单现状(`settings-screen.tsx:801-913`):通用单凭据位
  (品类 scope+凭据名段+值,术语向),只喂测试按钮;真实管线不消费。
- 飞书 tenant token 有效期 ~2h:`auth/v3/tenant_access_token/internal` 可用
  app_id+app_secret 换取——具备 app 侧自动 mint 的全部条件。

## Requirements

- R1 **解析接通(核心)**:通道凭据解析顺序=显式引用原样解析(`env:`/
  `keychain:`)→ env 缺失(`env_var_missing`)时回退钥匙链规范名
  `myia/push/<ENV_KEY>`(叶名=环境变量名)→ 两者皆缺报既有
  `env_var_missing` 码+文案指引「设置→推送」。接线面=feishu_card
  (token/target)、telegram(token/target)、webhook(endpoint)。
- R2 **飞书 token 自动续期**:FEISHU_BOT_TOKEN 缺失而
  FEISHU_APP_ID+FEISHU_APP_SECRET 可解析(env→kc 同一回退)时,通道自行
  mint tenant_access_token 并进程内缓存(过期前 120s 重 mint);手工 token
  路径保留兼容。
- R3 **设置屏推送分区重做**:按通道预设字段(去 scope/名段术语)——
  feishu_card:app_id/app_secret/chat_id;telegram:bot token/chat_id;
  webhook:url。逐字段保存 `myia/push/<ENV_KEY>`(空字段跳过不覆盖);
  「发送测试」与真实 run 同源解析。自定义品类级凭据位保留为高级入口。
- R4 **指南重写**:消息屏 feishu/telegram 指南改「设置→推送 填一次」,
  删 curl/zshrc/2h 手工段;平台侧建应用/开权限步骤保留(平台要求)。
- R5 平台卡状态判定(`matchSecretNames` 叶名命中)与钥匙链规范名天然
  对齐——保存后消息屏平台卡亮「已连接」,零额外改动。

## Acceptance Criteria

- [x] AC1:env 缺失+钥匙链规范名在 → 三通道发送/测试成功走钥匙链值
  (python 测试:InMemory 后端注入)。(tests/push/test_push_credential_journey.py
  12 用例:helper 三态+显式引用直通+TG/webhook 回退+飞书 mint 四态)
- [x] AC2:env 缺失+钥匙链也缺 → `env_var_missing` 结构化错误,文案含
  设置→推送指引(既有错误码不变,存量测试码断言不红)。
- [x] AC3:飞书 app_id/secret 在场 → mint+缓存生效,过期前重 mint
  (MockTransport 断言调用);手工 token 在场优先直用不 mint。(mint 恰一次
  缓存命中/手工 token 零 mint/mint 拒绝 feishu_token_mint_failed 三向断言)
- [x] AC4:设置屏推送分区:feishu 三字段保存三条 secret.set(空跳过)、
  测试按钮 target 与真实解析同源;telegram/webhook 同构(vitest)。
  (settings.test.tsx 推送 describe 重写:预设位三条/空跳过/全空拦截/
  自定义折叠区两用例;G5 测试 target=keychain:myia/push/FEISHU_CHAT_ID)
- [x] AC5:消息屏指南零 curl/零 zshrc/零「2 小时」字样,含「设置→推送」
  引导;指南相关存量断言同步改写(vitest)。(含 not.toContain curl/.zshrc
  反向断言;ntfy/slack 等 W3 长尾指南不在本任务面,维持原样)
- [x] AC6:门禁=pytest 定向(push/schema)+vitest 全量+tsc+ruff 绿;
  detect-changes staged 面净;零协议变更(secret.set/push.test 均既有)。
  (pytest 1119+1skip 绿、ruff 绿、tsc build 绿、detect-changes:python 批
  5 文件 28 符号 0 流程 low/desktop 批 13 符号;**vitest 全量 4 红系并行
  5c188c0(pluginFile API 层截断)改协议载荷未随测试断言,该线在途活跃,
  归属其线不代改,白名单 scoped=settings 35/messaging 53 全绿**)
- [ ] AC7:装机换装后,设置→推送 填飞书 app 凭据→发送测试,真链可达
  (凭据由主人填;链路与解析自动化证据留档,装机包刷新归本任务)。

## Constraints

- 钥匙链规范名纪律:一律 `myia/push/<ENV_KEY>`(与 matchSecretNames 叶名
  命中、env 文档键同构);不引入第二套命名。
- 显式 `keychain:` 引用语义零变化(用户 YAML 手写引用不被回退改写)。
- 值零明文:表单 type=password、保存即清、不回显(既有铁律)。
- 不 push;提交 pathspec 纪律(并行会话在途);装机链复用 /tmp/ks 流程。

## Notes

- 主人 2026-10-05:「用户使用起来非常不方便」→ 确认「就是这条路,立项修
  (推荐)」。三件(解析接通/自动续期/文案重写)方向已批;D1-D5 取舍见
  design.md,可翻案。
- 上一任务(10-05-keychain-silent-listing)已消「开屏弹密码框」;本任务
  消「填了也用不上」。真发一条到主人飞书/TG 仍需主人提供凭据(AC7)。
