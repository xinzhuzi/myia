# design:Reddit 官方 Data API 引擎(实现档)

> 任务:10-05-reddit-official-engine · 蓝本:`../10-05-reddit-source/research.md`(§N 引用即已核)
> 决议链:主人「按建议全部解决」→ 官方 OAuth Data API 通道,凭据可选(未配 =
> credential_missing 显式空态,零核心影响;配好即活)。

## 1. 引擎一句话形态

`engines/reddit.py::RedditEngine(BaseEngine)` —— 链外引擎(credhunter/
zenrows 先例):`ENGINE_REGISTRY` 在册、`AUTO_CHAIN` 不在,`engine: reddit`
显式选择 = 单级链;OAuth2 client_credentials 取 bearer → GET
`oauth.reddit.com/r/<sub>/<listing>` 单页列表 → items(管线 `Item.from_extracted`
契约:url 必需 + title/content 管线键 + 其余进 metadata);凭据缺失 =
`credential_missing` 显式空态(credhunter 先例),配好即活。

## 2. 注册与词表(三锁 + 双锁)

- `registry.py::ENGINE_REGISTRY` +1:`"reddit": lambda: _load("reddit",
  "RedditEngine")`;`AUTO_CHAIN` 七层**原样不动**;`auto_degrade("reddit")`
  走既有「registered non-chain engine → 单级链」分支(registry.py:159-160,
  零新逻辑)。
- `schema.py::ENGINES` 元组 + `EngineName` Literal 各 +1 `"reddit"`(注释同
  credhunter/zenrows 风格:链外官方 API 引擎,凭据可选,缺省 credential_missing
  空态)。
- 风险面(gitnexus impact 亲跑,2026-10-05):`ENGINE_REGISTRY` 上游 0 直接
  (LOW)、`auto_degrade` 3 影响(LOW)、`resolve_engine` 3(LOW)、`ENGINES`
  0(LOW)——纯加法,无 HIGH/CRITICAL。

## 3. 源配置形态与 URL 契约

```yaml
- name: reddit-gaming
  engine: reddit                     # 显式选用,链外
  url: "https://oauth.reddit.com/r/GamingNews/new"   # r/<sub>/<listing>
  engine_options:
    reddit:
      client_id: keychain:myia/reddit/client-id       # env:/keychain: 引用
      client_secret: keychain:myia/reddit/client-secret
      limit: 25            # 缺省 25,1-100 钳制
      ua_username: ~       # 可选 Reddit 用户名(UA 段);缺省不带(隐私)
```

- URL 校验(fetch 前零 I/O 结构化拒,`invalid_reddit_source_url`):scheme
  https ∧ host 恰为 `oauth.reddit.com` ∧ path 匹配 `/r/<sub>/<listing>`;
  `<sub>` 允许 `[A-Za-z0-9_+-]+`(Reddit 多 sub 的 `a+b` 形态原样放行);
  `<listing>` 封闭词表 `new/hot/rising/top`(缺省语义取自 URL,不另配)。
  源 URL 的 query 被**忽略**(引擎全权构造 `limit`/`raw_json=1`)——防止
  用户在 URL 里手拼 limit 与引擎选项打架。
- `extract` 节:配置即结构化拒(`extract_unsupported`)—— 引擎内置 Reddit
  JSON 解析,extract 配置必是错配,可见优于静默忽略(credhunter 同款)。
- `pagination` 节:配置即结构化拒(`pagination_unsupported`)—— 单页语义,
  翻页/滚动都不属于本引擎(循环间隔交既有 run loop,蓝本决议)。

## 4. OAuth2 client_credentials 流

- **token 端点**:`POST https://www.reddit.com/api/v1/access_token`
  (公开文档常量):
  - `Authorization: Basic base64(client_id:client_secret)`;
  - body(x-www-form-urlencoded):`grant_type=client_credentials` +
    `device_id=myssia01`(≤30 位字母数字的稳定 device 标识;client_credentials
    通道的惯例参数,不带用户身份)。
  - 200 → `{access_token, token_type: "bearer", expires_in≈3600, scope}`;
    `access_token` 缺失/空 → `reddit_oauth_malformed` 结构化失败。
  - 4xx/5xx → `http_<status>` 结构化失败(saas 先例;消息只带端点常量与
    reason,不带凭据)。
- **列表端点**:`GET https://oauth.reddit.com/r/<sub>/<listing>?limit=<N>&raw_json=1`,
  `Authorization: Bearer <token>`。`raw_json=1` 关 HTML 实体转义(标题里的
  `&amp;` 等)。
- **token 生命周期**:引擎实例内取一次、fetch 内复用;**不做跨 run 缓存**
  (每 run 每源 1 token + 1 列表请求 = 2 请求,100 QPM 下无压力;跨 run 缓存
  引入状态面,收益为负)。token 值不落日志、不进错误消息。
- **httpx 复用面**:两请求都骑 `self._active_client`(共享 context client;
  源级 `proxy: pool:<名称>` 由 fetch() 壳的 `_prepare_proxy_transport` 统一
  mount,引擎零感知);超时用 context 缺省。

## 5. 凭据三态(核心决议实现)

键:`engine_options.reddit.client_id` / `client_secret`,值为 `env:`/
`keychain:` 引用。明文守卫由 schema 兜底(`client_secret` 键名以 secret 后缀
命中 `_scan_secret_refs`,启动即拒明文——引擎层不再重复执法)。

| 态 | 判定 | 行为 |
|---|---|---|
| 未配 | 两引用任一为 None | `last_skip_reason = "credential_missing"` + info 日志(人话指引:`myssia secret set myia/reddit/client-id` / `client-secret` + 官方 app 注册页)+ `return []`,**零请求** |
| 配而解析失败 | `CredentialResolveError` | 同上空态 + **warning** 留痕(credhunter `_resolve_lane_key` 同口径:引用在而钥匙串未写/解析坏 = 配置问题可见,不静默) |
| 配好 | 两值解析成功 | 正常 OAuth + 列表产出 |

- 与 credhunter 空态同轨:`FetchOutcome.skipped=True`、`skip_reason=
  "credential_missing"`,管线/CLI/doctor 面(`EXPLICIT_EMPTY_SKIP_REASONS`)
  零改动即识别。
- 键名建议(档内钉死):钥匙串 `myia/reddit/client-id` +
  `myia/reddit/client-secret`(循 `myia/llm/base_url` 命名惯例,
  ai-news.yaml:126)。

## 6. UA 政策(Reddit 开发者条款硬格式)

格式 `<platform>:<app ID>:<version> (by /u/<username>)`,禁谎报【蓝本 B6】。

| 优先级 | 来源 | 值 |
|---|---|---|
| 1(最高) | 源级 `headers.User-Agent` | 原样(schema 既有能力,完整覆盖) |
| 2 | `engine_options.reddit.ua_username` | `desktop:com.myia.app:1.0 (by /u/<name>)` |
| 3(缺省) | — | `desktop:com.myia.app:1.0` |

**张力记录**(蓝本 §8.5):UA 用户名段是 Reddit 条款建议的联系方式,但会把
Reddit 账号身份钉进每个请求日志;缺省**不带**(隐私优先),文档写明如何配。
App 标识段 `com.myia.app` 与 Tauri identifier 同形(诚实标识自家 app,非谎报)。

## 7. robots 论证(为何不查两宿主 robots.txt)

- **事实**:www.reddit.com robots 全站 `Disallow: /`【蓝本 A1】;oauth 宿主
  同样全禁【A3】。
- **官方一手口径**(Data API Wiki,蓝本 B6 存档):"Our robots.txt is for
  search engines, not Data API users." —— robots.txt 是搜索引擎爬虫礼貌面;
  OAuth 授权 Data API 调用的合规面在 Developer Terms / Data API Terms(条款面:
  OAuth 强制 + 非商业口径 + UA 硬格式 + 48h 删除义务),与 robots 无关。
- **实现含义**:本引擎的请求走 `_send_with_retry` + `_acquire_rate_limit`
  (保留 qps 限速与退避重试的通用礼貌),**不经 `_ensure_robots_allowed`**
  (不拉两宿主 robots.txt,少两次无意义请求);`respect_robots` 源级开关对本
  引擎的 API 请求无操作面(它管的是爬虫语义)。
- **边界(重要)**:该豁免**只属于本引擎的官方 API 端点**(token 端点 +
  oauth 宿主列表端点,常量钉死);引擎不提供任何通用绕 robots 能力,通用引擎
  (static_html/direct_api)的 `.rss`/`.json` 直抓路线**零改动**——robots 全禁
  照旧拦它(蓝本 §4 与 Public Content Policy 把绕 robots 直抓点名「未授权
  访问」【B3】)。测试钉死:本引擎请求序列里零 `/robots.txt`。

## 8. 限速礼貌与重试

- 单页小 `limit`(缺省 25,硬钳 1-100;蓝本「单页小 limit」决议)。
- 请求节流交 `source.rate_limit`(缺省 qps 0.5——对 API 宿主保守但无害,
  用户可调);100 QPM 免费层【B6】下永不触顶。
- 重试退避沿 `_send_with_retry` 既有策略(源级 `retry` 缺省 3;429/5xx 指数
  退避)——「无重试风暴」:引擎自身不做任何额外重试循环,OAuth 失败不重取
  token(凭据坏重试无意义,4xx 立即结构化失败)。

## 9. 人肉步骤单(主人亲自,2026-10-31 前)

1. 浏览器登录 Reddit 账号 → <https://www.reddit.com/prefs/apps> → "create
   another app...";
2. 选 **script** 型;name 随意(如 `myssia`);redirect uri 填
   `http://localhost:8080`(script 型不用回调,占位即可);
3. 拿到 **client_id**(应用名下方短串)与 **client_secret**(标记 secret 的串);
4. 写入钥匙串(CLI 子命令真名已核:`myssia secret set`,值走 stdin 管道不落
   shell history):
   ```bash
   myssia secret set myia/reddit/client-id < id.txt
   myssia secret set myia/reddit/client-secret < secret.txt
   ```
   (或桌面端凭据页录入同键名);
5. 品类 YAML 把源 `engine:` 指到 `reddit` 并按 §3 形态写好引用(或解开
   plugins/ai-news.yaml 里注释掉的示例)——即活。
6. 验证:`uv run myssia test <品类>.yaml --json` 看该源 `ok` 与 items;
   `myssia doctor` 可核钥匙串键在不在。

时效提醒:官方新 API 申请窗口 **2026-10-31 截止**(蓝本 §3.2);RSS 通道
2026-11-13 退役;公 Data API 2027-03 分阶段终结 —— 注册完成后凭据长期有效,
通道终结前(2027-03)有一次「迁移 Devvit 或转付费」的再决策(research §7)。

## 10. 残余事项(如实)

- **48h 已删内容清理义务**(蓝本 §3.1/B6)vs MYIA 长期库:主人裁决点
  (research §8.4)未决——引擎不实现自动清理;现状 = 接受条款张力(个人
  非商业场景,Reddit 的措辞是「建议」常规清理)。若日后裁决要清理,属数据
  面任务另立档。
- **2027-03 通道终结**:持续跟踪项;Devvit 形态明朗后再评估(research §9)。
- **商业化前门**:MYIA 若商业化须先取得 Reddit 许可(Public Content Policy,
  蓝本 §2)——长期风险记录,非本档范围。
- token 端点 / oauth 宿主 robots 本轮未再探(蓝本 A1/A3 已存档 2026-10-05
  快照;涉网纪律单次勿反复,engine 实现不依赖 robots 状态)。
- client_credentials 凭据形态细节:蓝本 §9 标记「script app 细节未核」
  (指引页在 robots 禁域);实现按 OAuth2 公开规范 + Reddit 官方文档通行
  形态(Basic auth + client_credentials + device_id),MockTransport 测试
  钉死请求形状;主人首次真跑(人肉步骤单第 6 步)即是实活核验。
