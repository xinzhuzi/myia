# design — 配置组多平台账号配置(飞书账号线 + 微信受限状态卡)

## 0. 语义边界(裁定,见 prd)

本身账号(用户对自建应用的 OAuth 授权态)≠ 推送机器人(App 凭据/tenant token)。App ID/Secret **复用**推送区同一应用凭据(`FEISHU_APP_ID`/`FEISHU_APP_SECRET`,env→钥匙链回退惯例 `push/base.resolve_channel_credential`),本设计只管「用户授权」那一半。

## 1. 领域层:`src/myssia/feishu_account.py`(新)

- 键规约 `ACCOUNT_KEY_RE = ^feishu-[a-z0-9][a-z0-9_-]{0,62}$`(镜像 web_line.ACCOUNT_KEY_RE;作钥匙链 scope 恰好满足 `validate_secret_name` 的品类 id 规则)。
- 存储(目录即账号,镜像 tg_web 惯例):
  - `<数据根>/feishu-accounts/<账号键>/myssia-login.json` — `{label, authorized_at, refresh_ok, refreshed_at}`(零凭据面);
  - keychain `myia/<账号键>/user_access_token`、`myia/<账号键>/refresh_token`(两级命名,对齐 `^myia/<scope>/<name>$`)。
- 纯函数/IO 分离:
  - `authorize_url(app_id, redirect_uri, state)` → `https://accounts.feishu.cn/open-apis/authen/v1/authorize?app_id&redirect_uri&state`(纯函数);
  - `async exchange_code(app_id, app_secret, code, redirect_uri)` → POST `/authen/v1/oidc/access_token`(httpx.AsyncClient,`transport` 可注入 MockTransport 供单测);
  - `async refresh_tokens(app_id, app_secret, refresh_token)` → POST `/authen/v1/oidc/refresh_access_token`;
  - `async probe_account(...)` → 刷新闭环:读 refresh_token → refresh → 回写两 token + marker.refresh_ok/refreshed_at;失败置 refresh_ok=False(不抛,状态即结论);
  - `delete_account(data_root, key)` → 删 keychain 两项 + 账号目录(护栏在协议层)。
- 错误码族:`feishu_account_app_credential_missing / authorize_state_mismatch / feishu_oauth_exchange_failed / feishu_refresh_failed / account_key_invalid / account_delete_in_progress`。

## 2. 协议层:entry.py(PROTOCOL_VERSION 14→15)

- `_FEISHU_OAUTH_REDIRECT_PORT = 8731`(固定,主人需在飞书开放平台应用安全设置登记 `http://127.0.0.1:8731/callback`——AC8 留指引);占用冲突 → 结构化错。
- 内存槽 `_FEISHU_OAUTH_OPS`:`{state: {account_key, label, started_at, error?}}`(镜像 `_BROWSER_OPS` 台账范式);端点 ThreadingHTTPServer 仅绑 127.0.0.1,路径 `/callback`,5 分钟超时自停(守护线程)。
- 新方法四条:
  1. `platform_accounts.status` → `{feishu: {accounts: [{account, label, authorized_at, refresh_ok, refreshed_at}], authorize_in_progress: bool}, weixin: probe_bridge(...)七键}`(feishu 静态快照,探针显式触发不做 status 内联网刷新);
  2. `platform_accounts.feishu.authorize {account_key, label}` → 校验键规约 + app 凭据解析(env→kc)→ state 起端点 → `{authorize_url}`;同键已在授权中 → 结构化拒;
  3. `platform_accounts.feishu.delete {account_key}` → 授权中拒删(`account_delete_in_progress`)→ 领域层删除;
  4. `platform_accounts.feishu.probe {account_key}` → 刷新闭环,回 `{refresh_ok, refreshed_at}`(UI「重新检查」钮;授权回调成功后自动 probe 一次)。
- 回调处理:GET `/callback?code&state` → state 槽对账(mismatch 结构化留痕)→ exchange_code → keychain + marker → 自动 probe → 停端点;浏览器侧回一段极简 HTML(成功/失败文案,不做花页面)。
- Rust 壳零改动(一切经 `sidecar_request`)。

## 3. UI(镜像 tg-account 范式)

- `screens/settings/platform-accounts-api.ts`:status/authorize/delete/probe 封装 + 类型(镜像 telegram-api.ts);
- `screens/settings/platform-accounts-card.tsx`:飞书段(账号行 = 状态灯 + label/键 + 授权时间 + 重新检查 + 删除;「+添加账号」= 键名+备注 → authorize → 系统浏览器开授权 URL → 轮询对账 5s×24,镜像 telegram-card 轮询)+ 微信段(三布尔状态灯 + 已配置档有无 + `hermes gateway setup` 指引与复制钮 + 单活模型诚实披露);
- `screens/platform-accounts/platform-accounts-screen.tsx`:PageHeader(无头口径)+ 卡;
- 注册:App.tsx Route `/platform-accounts`;sidebar「配置」组加「平台账号」;command-palette 一条。

## 4. 测试

- pytest `tests/feishu_account/`:键规约/marker 读写/authorize_url 纯函数/exchange+refresh(MockTransport 注入)/probe 闭环(成功回写+失败置灰)/删除清三处;回调端点集成(真起 127.0.0.1 端口,伪造 code 回调,state mismatch 拒)。
- vitest `platform-accounts-card.test.tsx`:飞书段三态/添加授权流(mock api)/删除护栏/微信段渲染与指引复制。
- 门禁:全量 pytest + vitest + tsc -b + vite build + cargo build;装机 tauri build + 换装 + package_smoke。

## 5. 主人侧前置(AC8 指引)

飞书开放平台 → 开发者后台 → 应用安全设置 → 重定向 URL 登记 `http://127.0.0.1:8731/callback`;未登记时授权页会报「redirect_uri 不合法」——卡面指引带文案。
