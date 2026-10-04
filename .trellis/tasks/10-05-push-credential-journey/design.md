# design:推送凭据用户旅程接通

## D1 钥匙链规范名与回退策略

- 规范名:`myia/push/<ENV_KEY>`(feishu:FEISHU_APP_ID/FEISHU_APP_SECRET/
  FEISHU_CHAT_ID/FEISHU_BOT_TOKEN;telegram:TELEGRAM_BOT_TOKEN/
  TELEGRAM_CHAT_ID;webhook:MYIA_WEBHOOK_URL)。叶名=环境变量名:
  `matchSecretNames` 按叶名命中 → 平台卡「已连接」判定零改动对齐。
- 回退:通道解析点(env 引用)在 `env_var_missing` 时查
  `secrets_store.get_secret("myia/push/<ENV_KEY>")`;任何 SecretError
  (not_found/backend unavailable)→ 维持 `env_var_missing` 码、文案附
  「设置→推送」指引。显式 `keychain:` 引用与构造注入(token=)路径零变化。
- 落点:`push/base.py` 新增 `resolve_channel_credential(ref, *, env_key,
  label)`;feishu_card/telegram/webhook 的 token/target/endpoint 解析点改调
  该 helper。测试注入走 `secrets_store.set_backend(InMemoryKeychainBackend())`
  (模块既有注入缝,不新增构造参数面)。

## D2 飞书 tenant token 自动 mint/缓存

- 解析顺序(send 期,async):①构造 token= 注入;②FEISHU_BOT_TOKEN
  (env→kc 回退,D1);③FEISHU_APP_ID+FEISHU_APP_SECRET(各 env→kc 回退)
  → POST `auth/v3/tenant_access_token/internal` mint。
- 缓存:模块级 `{app_id: (token, expires_at_monotonic)}`,expire 提前
  120s 失效重 mint(app_id 变更天然分键);进程内存,sidecar 常驻够用,
  重启重 mint 一次可接受(无落盘泄面)。
- mint 的 HTTP 走通道既有注入 client(tests MockTransport 同缝);非零
  code/网络失败 → PushSendError(`feishu_token_mint_failed`),不吞。
- `_resolve_token`(sync)升级为 async `_obtain_token`,send/
  discover_directory/带图上传三处 token 取用点统一切换。

## D3 设置屏推送分区重做(settings-screen.tsx)

- 通道 Select 保留;表单体按通道切换预设字段:
  feishu_card=[app_id, app_secret(password), chat_id(可选)] /
  telegram=[bot token(password), chat_id(可选)] / webhook=[url]。
- 保存:逐非空字段 `secret.set myia/push/<ENV_KEY>`;空字段跳过不覆盖
  (清除走危险区 secret.delete,占位提示注明);成功态回显凭据名清单。
- 发送测试:target=`keychain:myia/push/<通道目标键>`(feishu=CHAT_ID/
  telegram=CHAT_ID/webhook=URL)——与真实 run 同一解析链(D1 接通后
  push.test 与 pipeline 等价)。
- 旧通用表单(品类 scope/名段)保留为「自定义凭据位(YAML keychain:
  引用)」折叠区,存量能力不砍。

## D4 指南重写(platform-overview.tsx)

- feishu:keys 改 [FEISHU_APP_ID, FEISHU_APP_SECRET, FEISHU_CHAT_ID];
  steps=建应用→加机器人→开权限(im:message:send_as_bot + im:chat:readonly,
  im:resource 可选)→发布版本→拉 bot 进群→**「到 设置→推送 填
  app_id/app_secret/群 chat_id,保存后点发送测试;token 自动续期无需
  手工换」**;chat_id 可从消息屏刷新目录挑。删 curl/zshrc/2h 段。
- telegram:steps=BotFather 建 bot→**「到 设置→推送 填 bot token」**→
  给 bot 发条消息→消息屏刷新目录挑会话。删 zshrc 段。
- 存量指南断言(messaging-screen.test「curl 命令」「zshrc」等)同步改写。

## D5 兼容与边界

- 服务器/CLI 用户 env 路完全不变(env 优先);YAML 种子零迁移(回退使
  env 引用在「装了桌面凭据的机器」自动可用)。
- 单元测试触碰真钥匙串的问题:回退路径测试一律 `set_backend(InMemory)`
  + fixture reset;存量 telegram env_var_missing 用例补注入,消除真钥匙串
  读(机器无 myia/push/* 项本也无害,但纪律是零触碰)。
- 并行会话在途:白名单=base/feishu_card/telegram/webhook/settings-screen/
  platform-overview + 对应测试;提交一律 `git commit --only --`。

## 风险

- 飞书 mint 端点限频:桌面低频场景(发送即 mint/2h 一次)远低于阈;
  缓存已把 mint 压到最小频率。
- 设置屏测试改写面较大(push describe 重写):按新交互逐条重写断言,
  不保留旧表单断言(旧表单保留在折叠区,断言迁移到「自定义凭据位」组)。
