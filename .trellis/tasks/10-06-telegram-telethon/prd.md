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
- [~] 阶段一 B3 常驻宿主(2026-10-06):
  - `src/myssia/telegram/serve.py`(TelegramServeHost):getUpdates **长轮询 25s**(httpx 超时 35s>挂起窗;空窗不忙轮)→ 每轮消息过 B2 过滤管线(两档共用)→ 高价值合并单条即时推/普通入库 → offset 持久(`offsets.py`,数据根 telegram/offsets.json 原子写,重启断点续拉)→ 事件账本(`events.py`,executions 形态新表 telegram_events,outcome 词表 stored/pushed/dropped_coarse/dropped_chat/dropped_textless/dropped_other/error,消息级记账);断线指数退避 1s→2s→…帽 300s 成功归零;401/409 致命错误不蒙头退避(结构化上抛宿主退出);sink 全注入(push_high_value/store_item),宿主本体零 pipeline 依赖(依赖方向红线)。
  - 引擎共享面抽出:`engines/telegram.py` 的消息分拣/聚合/锚(`updates_to_items`/`message_to_item`)与过滤配置解析(`filter_config_from_options`)升模块级,引擎方法成委托——serve 与批量档同一份消息语义(design D1)。
  - CLI `myssia telegram serve --category plugins/telegram-groups.yaml --db …`:装配品类(chat_id 唯一/单 bot token 校验,多 bot 拆品类各起宿主)→ 绑定×过滤管线 → 推送 sink(品类 push 首条通道 `_build_push_channel` 同门)/入库 sink(SQLiteStore+DedupRegistry,dedup key={url})→ offsets/events 落数据根 telegram/;Ctrl-C 干净停,致命错误退出码 1,装载/凭据失败结构化指引。
  - 桌面接线位(Grill Q6 桌面为主):TelegramServeHost 即 sidecar 嵌入单元(asyncio.run+daemon thread 照 _CRON_TICKER 先例),模块文档注明接线形态;entry.py 现由并行任务(10-06-feed-channel-groups)持有,sidecar 方法实装留桌面批——如实记档。
  - 测试 `tests/telegram/test_telegram_serve.py` 21 例(offsets 往返/坏文件兜底/拒非法值、账本词表/counts、poller URL 形状/401/409/transport/坏载荷+token 零外显、宿主一轮恰 1 推+入库+offset=max+1+账本分布、三类丢弃记账、重启续拉、退避翻倍归零、致命上抛、入库炸不带走循环、过滤炸降级入库、LLM 未配全入库、CLI 装配三例缺 token 指引/非 telegram 源拒/subparser 在册);全套 4423 passed+desktop 288 passed;ruff 绿。
  - 注:telegram serve CLI 的端到端真跑(AC1 前置)留主人 token 到手;桌面 entry.py 接线待并行任务落地后另批。
  - **桌面接线批落地**(2026-10-06,entry.py 时段已释放,独立提交):`desktop/entry.py` 增 `_assemble_telegram_host`/`_start_telegram_host`/`_stop_telegram_host` + serve() 两行接线(cron ticker 同款双宿主判例:serve() 就绪即起/EOF 即停、daemon 线程绝不占 serve 线程、home 模式才起、锁内查-占幂等、起不来只留痕不拦服务)。装配与 CLI `_cmd_telegram_serve` 逐句同门(品类=`<plugins>/telegram-groups.yaml` → chat_id 绑定×过滤管线 → keychain bot token → push 首条通道/入库 sink(SQLiteStore+DedupRegistry {url} 锚)→ offsets/events 落数据根 telegram/);重量依赖函数内惰性导入(dev 直通零加载成本);凭据缺失=graceful 不启动仅留痕(含主人四步指引,配好重启即活)。两处刻意不同于 cron:无 supervisor 重排(宿主自带退避,致命 401/409 是配置态,线程自退留痕重启由人决定=serve.py D4);与 CLI serve 的双宿主互斥=Bot API 同 token 409(非 tick 文件锁)。零新协议方法(`telegram.serve.status` 观测面留后续批);serve.py 模块文档「桌面接线位」段同步改「已落」。测试:`tests/desktop/test_desktop_sidecar_protocol.py` +7 例(lifecycle/幂等/dev 不起且不触装配/凭据缺失 graceful 留痕含四步/品类缺失 graceful/真装配件出真 TelegramServeHost+offsets-events 落数根+stop 注入面/致命自退留痕不复活/serve() 接线往返 EOF 关停);亲跑 `pytest tests/desktop -q` **295 passed**、`pytest tests/telegram -q` **47 passed**;真品类装配冒烟(仓库 telegram-groups.yaml+假 token+MYIA_HOME 沙箱,只装配不跑零网络)出真宿主+feishu_card 通道构建+events.db 落数根。装机包本批**未动**(/Applications 重签竞态,统一收尾批);像素验证于本批无 UI 改动不适用,装机侧真跑留收尾批与 AC1 token 同窗——如实记档。
- [ ] 阶段二 Telethon 组件依赖+session 流程+引擎(待填)
- [ ] 阶段三 组件化件示例(待填)
- [~] 门禁+装机(2026-10-06 B1-B3 门禁三批全绿:4423 passed+desktop 288 passed+ruff 绿;装机外科已做):
  - 装机外科(世事.app /Applications/世事.app):定向同步 13 件(引擎 telegram.py/registry.py/schema.py/cli.py + telegram/ 包五件 + plugins telegram-groups/telegram-channels/daily-digest 三件),diff 逐字节一致核验;仓库 venv 3.12 对装机副本八项 import 冒烟全过(engine/vocab/serve/offsets/events/cli/plugins);并行会话曾中途同步过 telegram/ 包中间态(19:09-19:18 时间戳,缺 events/serve/cli),本次全量覆盖修正;清理三处 stale __pycache__ 后 adhoc 重签(codesign --force --deep -s -,verify --deep 通过;spctl 拒 adhoc 属常态,与装机前同制式)。
  - AC4 的「像素验证」留桌面接线批(entry.py 由并行任务持有);AC1 真发留主人 token。

## 结果(验收回执,完工填)
- [ ] AC1-5 勾选+证据(**终局收尾员 2026-10-06 终验对照,全留未勾,缺口如实**):
  - AC1 bot 线端到端:**未满足**——代码面全就绪(B1 引擎+B2 过滤出口+B3 serve,`myssia telegram serve` 可跑),真发回执缺主人四步(bot/关隐私/token/拉群),token 未入钥匙串即 credential_missing 零请求空态(设计如此);回执位留待 token 到手。
  - AC2 Telethon 线端到端:**未开工**(B4 批,锁主人小号+验证码前置)。
  - AC3 组件化件全流程一例:**未开工**(B5 批)。
  - AC4 全 mock 单测+装机外科+像素验证:**部分满足**——mock 单测在案(B1 31 例+B2 25 例+B3 21 例,全量 pytest 4711 passed/40 skipped/0 failed 亲跑 19:36-19:38);装机外科已做(过程段 13 件+数据根补同步,见下);**像素验证留桌面接线批**(B3 桌面接线位如实记档,entry.py 时段由并行任务持有)。
  - AC5 凭据零外显+风控披露:**代码与测试面在案**(token URL path 净化 bot***、httpx 异常消息同净化、凭据三态 reddit 判例、测试断言 BOT_TOKEN 不外显;小号风控披露在 research/prd);真跑前的完整验收留 AC1 同窗。
- [x] **数据根 YAML 同步**(终局收尾员补做,2026-10-06 19:4x):数据根 `~/Library/Application Support/MYIA/plugins/daily-digest.yaml`(cron「每日合并日报」job enabled 在跑的活件)先前缺「Telegram 群」分区 = B2 出口在装机侧断环;已备份 `.bak-20261006-finalconsolidate` 后以仓库件覆盖,diff 逐字节一致,telegram-mihomo_party_group 源在册 1 处。telegram-groups.yaml 未部署数据根(与"serve 常驻时不必挂 cron"自洽:cron jobs.json 无该品类建档,装机包内示范件已在)。
- [x] **终局门禁复核**(收尾员亲跑,2026-10-06 19:36-19:38,树=0b15e09+587f49b 静置后):全量 pytest 4711 passed/40 skipped/0 failed;vitest 570/570(26 文件);tsc -b 0 错;desktop `npm run build`(tsc -b && vite build)通过;装机件复核:两线 14 件(telegram 9+store 2+entry.py+plugins 2)仓库↔包内 cmp 逐字节一致,主二进制 sha256 `4af5d62b…ead3` 与 feed 档 19:19 回执一致,`codesign --verify --deep --strict` exit 0 亲验。附记:19:23 首轮全量曾 7 failed(test_telegram_serve.py),系 B3 工程师会话当时正在写入中间态(源/测试 mtime 落在跑窗内),提交定稿后两轮全绿,非代码红。

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
