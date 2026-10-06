# PRD — 10-06-telegram-telethon:Telegram 接入(链接者架构)

> 立档:2026-10-06 · 来源:主人令(GitHub 调研轮 +「Telethon 本软件要做」+「其他插件设置下载+配置」+「做链接者,不做源码修改者」)
> 调研全记录:research.md(四类件/星数/借鉴点/隐私模式坑/链接者定调)

## 总目标

MYIA 具备三层 Telegram 消息获取能力,全部走「链接者」形态,组合进既有情报管线(粗筛→LLM 精筛→高价值即时推/其余进合并日报),出口遵守组合铁律。

## 三层能力(按优先序)

### 阶段一:Bot 线(engine: telegram,手搓零依赖)
- `getUpdates` 长轮询(25s 挂起)收 bot 所在群消息;httpx 直调,**不引 PTB 库**(借其过滤器分层模式);
- 引擎形态:链外引擎判例(urlwatch/prompt 同款),源名规约 `telegram-<群名>`;
- 双层过滤挂点:关键词粗筛(零成本)→ LLM 精筛(glm-4-flash)→ 高价值即时单条/合并、普通入库进日报;
- 凭据:keychain:myia/telegram/bot-token(值零外显);机器人限频礼貌(30msg/s 上限内的保守轮询)。
- **主人前置四步**:BotFather 建 bot → `/setprivacy` 关隐私模式(否则看不到普通消息)→ token 发我 → 拉进目标群。

### 阶段二:Telethon 线(userbot,主人点名原生做)
- 账号 session 读任意已加入群(bot 进不去的群覆盖);Telethon 以 extras/组件轨形态依赖(**不改其源码**);
- session 凭据三件入钥匙串(api_id/api_hash/session 文件);**建议挂小号**(风控隔离);首登一次性验证码流程走 CLI 交互,登录态持久数据根;
- 引擎复用阶段一的过滤挂点与出口;群清单配置驱动(engine_options.telegram.chats)。
- **主人前置**:小号手机号 + 首登验证码(一次性)。

### 阶段三:其他 TG 件组件化(设置下载+配置,零源码改动)
- 形态:设置页组件卡(照自管 Python 环境组件轨先例:下载/就绪检查/失败可见)+ 品类 YAML 配置驱动;
- 候选:tgcf(如需转发形态)/RSSHub TG 路由(与 X 线共用部署);
- TrendRadar(62k★)单列:**专项拆解档**(源清单/订阅形态/告警节奏借鉴,不引入本体)。

## 验收标准(AC)

- [ ] AC1:bot 线端到端——主人四步后,目标群发测试消息,秒级进管线、按铁律出口(高价值即时单条/普通入合并日报),真发回执在档;
- [ ] AC2:Telethon 线端到端——小号首登一次,目标群(bot 进不去的群)消息进管线,同过滤同出口;session 失效有结构化告警与重登指引;
- [ ] AC3:组件化件至少一例走「设置下载→配置→使用」全流程,零上游源码改动(链接者铁律验证);
- [ ] AC4:全 mock 单测(引擎/过滤/凭据三态)+ 装机外科同步+像素验证;
- [ ] AC5:凭据零外显(钥匙串),token/session 不落日志;账号风控披露如实(小号建议/限频参数)。

## 边界与不做

- 不 fork/修改任何上游源码(链接者定调);不引 PTB/aiogram 大库(bot 线手搓);
- 不做 TG「发送/回复」能力(本任务只读监控;双向交互是 Hermes 第三层 websocket 线的事,另档);
- TrendRadar 拆解可另立小档,不阻塞本任务。

## 主人决策点

1. bot 线四步(建 bot/关隐私/token/拉群)何时做;
2. Telethon 小号+验证码(一次性);
3. TrendRadar 拆解要不要排(一句话立档)。

## 过程(执行流水,开工逐项回填)
- [~] 阶段一 bot 线引擎+测试(B1 已落,2026-10-06):
  - B1 引擎:`src/myssia/engines/telegram.py`(engine: telegram 链外,reddit/urlwatch/prompt 判例)——getUpdates 批量窗口(零长轮询,25s 挂起属 B3 serve 档)+chat_id 群分拣+媒体组聚合(同 media_group_id 取首条有 text/caption 铸锚)+锚 `#tg-<chat_id>-<message_id>` 全期幂等+确认请求(offset=max+1 best-effort,多群共 bot 确认互偷已记档);凭据三态 reddit 判例(未配/解析失败/占位值=credential_missing 显式空态零请求,四步人话指引);token 零外显(URL path 净化 `bot***`,httpx 异常消息同净化);robots 豁免同 reddit 口径(授权 Bot API 通道);pagination 拒(单轮窗口语义)。
  - 词表/注册/schema 两行(ENGINES+EngineName,hunk 收窄)+docs zh/en schema.md 词表行同步;示范件 `plugins/telegram-groups.yaml`(源 telegram-mihomo_party_group 活源待 token 空态——schema sources min_length=1 故非注释态,token 未写钥匙串即 credential_missing 零请求;chat_id 占位待实填)。
  - 测试 `tests/engines/test_telegram_engine.py` 31 例全绿(四态矩阵:空态零请求/结构化拒/开启态往返含 401/409 指引+净化/注册表),tests/engines+test_schema+test_docs 计 765 passed;ruff 绿。
  - AC1 真发留给主人 token 到手(如实记档);B2 过滤+B3 serve 续。
- [~] 阶段一 B2 过滤与出口(2026-10-06):
  - `src/myssia/telegram/` 包落地:`telegram/filter.py` 过滤管线(批量引擎与 B3 serve 两档共用,design D1)——粗筛词表三层(源级 `engine_options.telegram.keywords` > 内置缺省 `DEFAULT_COARSE_KEYWORDS`:免费/白嫖/羊毛/token/额度/优惠/折扣/赠送/福利/激活码/兑换码/促销/coupon/free/giveaway;ASCII 大小写不敏感,显式空表=关闭)→ 粗筛未命中零痕迹跳过(不占库不占日报);LLM 精筛挂点(enrich `OpenAICompatClient` 复用,缺省 glm-4-flash,凭据 `llm_base_url`/`llm_api_key` 成对引用 prompt 契约明文拒;端点未配=降级纯粗筛零 token,失败/解析坏=降级全部普通出仓,宁漏推不误推);阈值 `score_threshold` 缺省 8(Grill Q5)可配 1-10。
  - 出口=组合铁律:`merge_high_value()` 同轮多条高价值合并**单条**(score=组内最高,route `score>=8 → immediate` 一轮至多推一条;合并锚 `<源url>#tg-<chat>-<min>-hv<n>-<max>` 随消息 id 区间稳定→批量档重拉幂等);普通条目带 score 逐条出仓走 archive 入库;daily-digest.yaml 增「Telegram 群」分区(sources: telegram-mihomo_party_group,与 telegram-groups.yaml 同步维护)。
  - 引擎接线:`engines/telegram.py` 增 `completer` 注入口(prompt 判例)+`_filter_options()`(keywords/threshold/model/llm refs/timeout 校验,半配/明文/越界=invalid_engine_options)+`_apply_filter()`(高价值合并单条+普通出仓);条目增 `chat_id`/`message_id` 观测键(合并锚区间与 B3 账本面)。
  - 测试 `tests/telegram/test_telegram_filter.py` 25 例(粗筛/精筛/降级/合并锚幂等/**同轮 5 条恰 1 条合并**端到端+引擎集成 mock getUpdates+fake completer 恰 1 合并条目);tests/telegram+tests/engines+test_schema 计 681 passed;ruff 绿。
- [ ] 阶段二 Telethon 组件依赖+session 流程+引擎(待填)
- [ ] 阶段三 组件化件示例(待填)
- [ ] 门禁+装机(待填)

## 结果(验收回执,完工填)
- [ ] AC1-5 勾选+证据(待填)

## Grill 决议(2026-10-06,主人批「全按推荐」)

| Q | 决议 |
|---|---|
| 1 开工时机 | **B1-B3 立即开工**(代码零前置,token 到手即端到端) |
| 2 bot 首批群 | **仅 mihomo_party_group**,稳后扩 |
| 3 Telethon 小号 | 有则 B4 随时;无则 B4 缓,bot 线先行(风控披露在档) |
| 4 TrendRadar 拆解 | **排小时级小档**,不阻塞主线 |
| 5 即时口径 | 粗筛命中→LLM 打分,**≥8 分即时单条**,其余进日报;口味配置化 |
| 6 常驻宿主 | **桌面 app 内接线为主**(app 开着=监控活着),CLI 形态留给服务器场景 |
| 7 保留期 | 90 天照旧可配;敏感群单源短保留 |
