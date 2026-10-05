# PRD:Reddit 官方 Data API 引擎(实现档)

> 立档:2026-10-05 · 来源:`10-05-reddit-source` 探查档(research.md 为蓝本)
> 主人决议:「按建议全部解决」→ **官方 OAuth Data API 通道,凭据可选**
> 类型:实现档 · 蓝本:`../10-05-reddit-source/research.md`(引用即已核,标 §N)

## 定界

- **做什么**:新引擎 `engines/reddit.py`(`engine: reddit` 显式选用,链外注册循
  credhunter/zenrows 先例,**不进 AUTO_CHAIN**):OAuth2 client_credentials
  (POST `https://www.reddit.com/api/v1/access_token`)→ bearer → GET
  `https://oauth.reddit.com/r/<sub>/<listing>?limit=N&raw_json=1` → JSON 解析为
  items;凭据可选(engine_options.reddit.client_id/client_secret 走
  `env:`/`keychain:` 引用);schema `ENGINES`/`EngineName` 词表 +1;品类 YAML
  注释示例(不默认启用任何品类);MockTransport 全链测试(零外网);
  docs/skill 四处同步。
- **不做什么**:不动 AUTO_CHAIN 七层;不动任何既有引擎行为;不做跨 run token
  缓存(单源单次 fetch 取一次 token 即弃,配额 100 QPM 下无压力);不做多页
  翻页(单页 limit=N,循环间隔交由既有 run loop);不做 48h 已删内容自动清理
  (数据保留义务是主人裁决点,蓝本 §8.4,见 Notes 残余);**不动 `.rss`/`.json`
  直抓路线**(robots 全站禁,判例维持);不默认启用任何品类源。
- **降级语义(核心决议)**:凭据可选 = 未配/解析失败 → 结构化
  `credential_missing` **显式空态**(credhunter 先例:`last_skip_reason` +
  人话指引日志 + 零请求),**绝不拦核心**(品类内其余源照常,管线 skip 语义
  与 credhunter 空态同轨);配好即活。

## 背景与已核事实(引用即蓝本)

- robots 面:www.reddit.com 全站 `Disallow: /`【蓝本 §1/A1】、oauth 宿主同样
  全禁【A3】;**官方一手明言 "Our robots.txt is for search engines, not Data
  API users."**【B6】→ 授权 API 通道合规面在 Developer Terms/Data API Terms
  (条款面),不在 robots 面【§1 结论】。
- 时效:RSS 2026-11-13 退役;**公 Data API 新申请截止 2026-10-31**;公 Data API
  2027-03 分阶段终结【§3.2】→ 主人须 10-31 前注册 app(人肉步骤单,见 Notes)。
- 免费层:100 QPM/OAuth client id(10 分钟均值窗口)【B6】;OAuth 强制;UA 硬
  格式 `<platform>:<app ID>:<version> (by /u/<username>)`,禁谎报【B6】。
- 非商业口径:MYIA 个人非商业使用落在 Public Content Policy 许可内,**前提是走
  授权通道**【§2】。
- 挂点亲验(蓝本 §6.1 + 本档实现前复核):`src/myssia/engines/registry.py`
  `ENGINE_REGISTRY`/`AUTO_CHAIN`;`src/myssia/schema.py` `ENGINES`/`EngineName`
  词表、`respect_robots` 缺省 true(schema.py:728)、源级 headers(schema.py:752)、
  明文凭据守卫(schema.py:465 `_scan_secret_refs`,引擎选项内 `client_secret`
  键以 secret 后缀命中守卫=强制引用形态);`fetch_base.py` `request()` 的 robots
  守卫与限速;items 消费面 `pipeline.py Item.from_extracted`(url 必需,其余进
  metadata)。
- 先例:`engines/credhunter.py`(链外注册 + credential_missing 显式空态 +
  `_resolve_lane_key` 解析失败降空态留痕)、`engines/zenrows.py`/`saas.py`
  (链外注册 + 结构化 http_<status> + 凭据不落日志)、`tests/engines/
  test_saas_gated_engines.py`(MockTransport 三态矩阵测试形态)。

## 验收标准(AC)

- [x] AC1:引擎注册三锁 —— `ENGINE_REGISTRY` 在册 `reddit`、`AUTO_CHAIN`
  七层原样不动、`auto_degrade("reddit") == ["reddit"]`(链外显式选择=单级链);
  schema 双锁(`ENGINES` 元组 + `EngineName` Literal 收录 `reddit`)。
  **证据**:`registry.py` ENGINE_REGISTRY +1(带链外注释)、AUTO_CHAIN 未动;
  `schema.py` ENGINES 元组 + EngineName Literal 各 +1;测试
  `test_registry_offchain_locks` / `test_schema_vocabulary_accepts_reddit`
  断言全部(含 AUTO_CHAIN 七层全量比对)。
- [x] AC2:OAuth2 client_credentials 全链 —— POST token 端点(Basic auth =
  client_id:secret;`grant_type=client_credentials` + `device_id`)→ bearer →
  GET oauth 宿主列表端点(`Authorization: Bearer`、`limit`/`raw_json=1` 参数);
  单源单次 fetch 只取一次 token;JSON → items(url=permalink 绝对化/title/
  published=created_utc ISO/author/score/num_comments/content=selftext)。
  **证据**:`test_oauth_flow_and_listing_roundtrip`(Basic 头/form body/Bearer/
  参数/items 全字段断言)+ `test_token_fetched_once_per_fetch`(恰一次
  /access_token)+ `test_listing_and_limit_options_apply` / `test_source_url_query_is_ignored`
  / `test_multi_subreddit_path_passes_through`。
- [x] AC3:凭据可选三态 —— ①未配引用 → `credential_missing` 显式空态
  (`last_skip_reason` + 日志人话指引含 `myssia secret set myia/reddit/...`,
  **零请求**);②引用在而钥匙串未写/解析失败 → 同空态 + warning 留痕
  (credhunter `_resolve_lane_key` 同口径);③配好 → 正常产出。绝不拦核心。
  **证据**:`test_no_credentials_is_explicit_empty_state_zero_requests` /
  `test_unresolvable_keychain_ref_degrades_to_empty_state_with_warning` /
  `test_env_reference_credentials_roundtrip` /
  `test_fetch_source_registry_empty_state_is_skip_not_failure`(registry 面:
  skipped 源非 failures);半配置另立结构化拒
  `test_half_configured_credentials_rejected`。
- [x] AC4:UA 政策 —— 缺省 `desktop:com.myia.app:<ver>`(Reddit 硬格式
  `<platform>:<app ID>:<version>`,**不带用户名**——隐私取舍,蓝本 §8.5 的
  缺省侧);`engine_options.reddit.ua_username` 配置则拼 `(by /u/<name>)`;
  源级 `headers.User-Agent` 显式配置优先级最高(schema 既有能力,完整覆盖)。
  **证据**:`test_ua_username_appends_by_segment` /
  `test_source_level_user_agent_header_wins` / roundtrip 测试内 UA 断言。
- [x] AC5:robots 论证落地 —— 引擎不查两宿主 robots.txt(授权 API 通道不受
  爬虫 robots 语义管辖,官方一手声明【B6】为据;测试钉死零 robots 拉取);
  qps 限速与重试退避照常(通用礼貌);`.rss`/`.json` 直抓路线零改动
  (缺省 `respect_robots: true` 照旧拦它,测试不涉)。
  **证据**:论证文 = 引擎模块 docstring「robots 论证」节 + design.md §7;
  `test_no_robots_txt_fetch_on_any_host`(请求序列恰 2 次、零 /robots.txt,
  handler 不经 make_handler 包装防自动应答掩盖);fetch_base.py /
  RobotsCache / `_ensure_robots_allowed` 零改动(git diff 面)。
- [x] AC6:测试全链 MockTransport 零外网 —— OAuth 流/列表解析/凭据缺失结构化
  错/凭据坏(OAuth 401)/limit 参数(缺省 25、上限钳制、类型错结构化拒)/
  UA 三态/源 URL 校验(非 oauth 宿主、非法 listing)/payload 形状错/注册表
  三锁/零 robots 拉取/token 单次。
  **证据**:`tests/engines/test_reddit_engine.py` 35 例全过(零外网,双宿主
  MockTransport + InMemoryKeychainBackend);含
  `test_oauth_http_401_is_structured_and_leaks_no_credentials`(凭据零外泄)、
  `test_oauth_token_response_without_token_is_malformed` /
  `test_listing_payload_without_children_is_malformed` /
  `test_listing_non_json_is_json_decode`(形状错三态)、
  `test_malformed_children_entries_are_skipped_not_fatal`(逐条目宽容)、
  `test_extract_config_is_rejected` / `test_pagination_config_is_rejected`。
- [x] AC7:品类 YAML 注释示例落 `plugins/ai-news.yaml`(注释形态,不默认启用);
  docs/zh+en getting-started 凭据段、README 引擎说明、skill/SKILL.md §4.1
  引擎表行同步。
  **证据**:ai-news.yaml linuxdo 占位后新增注释块(整块注释,装载仍 2 源,
  `load_category_file` 亲验);getting-started zh/en §2 各加 Reddit 段(双语
  对照);README 架构块加链外引擎行 + 致谢加 Reddit Data API 行;SKILL.md
  §4.1 加链外官方 API 引擎段 + ENGINES 词表行(test_skill_doc 锁等值,已过);
  顺带对齐 docs/zh+en schema.md ENGINES 词表行(补齐既有 zenrows/scraperapi
  缺席债,与 schema.ENGINES 真值一致)。
- [x] AC8:门禁 —— 定向 pytest(engines/schema/registry 面)+ ruff 通过;
  `gitnexus detect-changes --scope staged` 核验改动面;真跑不做(MockTransport
  为准,涉网零)。
  **证据**:pytest 定向面 683+497+168 过(tests/engines+test_schema+
  test_skill_doc+test_docs+test_gates;tests/pipeline+tests/credhunter+
  test_smoke;tests/cli);ruff check + format 过;detect-changes 见提交前
  记录;全程零外网请求(涉网页面仅蓝本既有存档,本轮未发新请求)。

## Notes(人肉步骤单 + 残余)

见 design.md §9(人肉步骤单全文)与 §10(残余事项)。
