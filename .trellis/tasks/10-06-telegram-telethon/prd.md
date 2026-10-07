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
- [x] AC4:全 mock 单测(引擎/过滤/凭据三态)+ 装机外科同步+像素验证;(统一收尾批 2026-10-06 20:31 结案:单测在案/装机 13+2 件全同步/像素验证=桌面接线批零 UI 改动不适用,见结果段)
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
- [~] 阶段二 Telethon 组件依赖+session 流程+引擎(B4,2026-10-08 代码面完,真登录留主人):
  - 依赖双轨:pyproject extras `telethon>=1.36,<2`(uv.lock 1.45.0 + pyaes/pyasn1/rsa 纯 Python 闭包)+ 桌面锁照 llm extras 判例扩 `--extra telethon` 重导出(diff 实证增量恰 4 轮零漂移)+ 组件卡照 crawl4ai 判例(components.json+COMPONENT_META,Rust 壳动态读零改动;test_pyenv_resources 1e 两例把守)。
  - `src/myssia/telegram/telethon_line.py`(B4 新件):登录流(手机号→验证码→2FA,session 落数据根 telegram/telethon.session 0600,复用提示/--force 重登)/消息面适配(telethon_message_to_update:Telethon Message→Bot API 同形,#tg- 锚/媒体组/过滤/出口全复用 bot 线零独立语义)/事件宿主(TelethonUserHost:serve.dispatch_once 同一份分派,F13 事件面升级宿主持久记忆+FIFO 帽,F14 bool 出口;FloodWait 服从服务器秒;transport 退避 1s→300s;只读四面零写接口);`assemble_user_host` 工厂(CLI/桌面同门;events 按 telethon-user:<api_id> 指纹分库,F8 判例;offsets 零写——telethon session 自持断点)。
  - 引擎 user 模式:engine_options.telegram.mode: user(iter_messages 窗口;凭据三态 api 凭据缺=credential_missing/session 未首登=session_missing 显式空态零请求、session 失效=session_expired 结构化+--force 指引、FloodWait=telegram_flood_wait 秒数披露;无确认请求;session 路径 MYIA_HOME 派生——「session」是 schema 凭据后缀词,YAML 明文路径会被凭据扫描拒)。
  - CLI:`myssia telegram login`(交互首登)+ serve 双线(bot+telethon 并跑,一线致命不拖另一线;双缺=结构化错误带两线指引);桌面 entry.py 装配同门(bundle.run 双 gather)。
  - **零凭据兜底**(2026-10-08 主人令追加,来历:主人侧 my.telegram.org 建应用持续裸 ERROR——该站服务端抽风,社区常见,重试/换出口或用默认对):login 在 api_id/api_hash 未配钥匙串时自动回落 Telethon 文档公开示例对(2040/b18441a1ff607e10f989894a5137bdb9);实测注记:Telethon v1.x(含 1.45)已不内置默认对(v1.0-1.45 源码亲验 api_id 空即 ValueError),「发行版内置」实为文档公开示例对;限速风险(略慢)在登录回执如实披露,钥匙串配了永远走自有对;引擎/serve 侧保持钥匙串主路径(空态指引附带默认对写法,不静默骑共享对跑排程)。
  - 测试:tests/telegram/test_telethon_line.py 32 例全 mock(登录流七路径含兜底/2FA/验证码错/限频服从;宿主退避/失效/事件→账本/相册三成员;引擎七例;只读边界调用面断言)+ desktop 用户线装配 1 例 + pyenv 2 例;e2e 沙箱补种 setuptools/wheel(pyaes sdist-only 构建前提);定向门禁 122+164 全绿,ruff 绿;两世界验证(venv 装/不装 telethon 均绿——import_module 拦截缝;顺带修复 tests/engines/test_telegram_engine.py telegram_context 空态注入内存钥匙串,HEAD 上真机钥匙串有 token 时该用例环境红,亲证非本批引入)。
  - 装机外科(2026-10-08 02:21-02:24):`npm run build`+`npx tauri build` exit 0(UI 件 COMPONENT_META 随包);备份 /tmp/myssia-b4-backup-20261008-022149 后 ditto 换装 /Applications/世事.app;**11 件 sha256 对拍全 MATCH**(telethon_line 新件+telegram 包六件+engines/telegram.py+cli.py+entry.py+requirements-lock.txt+components.json;lock 含 telethon 4 轮、components.json 含 telethon 行均实证在包);装机 python 直载冒烟过(dispatch_once/telethon_line/entry 装配符号全命中);`codesign --force --deep -s -` adhoc 重签+`-vv` 双过+strict verify exit 0;旧实例 quit 后 `open -g` 拉起新进程树 91929(壳)/91934(sidecar);ticker 心跳双验(写者戳 `…-91934` 即现+65s 续跳 mtime 精确 +60s)。**双线实况留痕(比预想更进一步)**:钥匙串已有 myia/telegram/bot-token(主人四步已完成)→ bot 线真起(logs 逐字:「telegram 宿主已起(品类 telegram-groups,线 bot,群 ['-1000000000000'])」;chat_id 仍占位待实填);数据根 telegram/telethon.session 已在场(02:16:58 落盘 —— 主人侧同窗在真机尝试 login;钥匙串无 api-id/api-hash → 若走本仓工作树代码即零凭据兜底对)→ telethon 用户线 graceful 未起,留痕逐字:「telethon 用户线依赖 telethon 未安装:请先执行 pip install 'myssia[telethon]'」(装机自管环境尚未跑「同步依赖」吃进新锁的 telethon 轮 —— 主人在设置页一键同步依赖+重启后用户线即活,session 已就位)。
  - AC2 真发留主人:手机号+验证码到位后 `myssia telegram login`(零凭据兜底已可登)→ serve 双线起,目标群(bot 进不去的群)消息进管线同过滤同出口;session 失效有结构化告警与重登指引(代码+测试面在案)。
- [ ] 阶段三 组件化件示例(待填)
- [~] 门禁+装机(2026-10-06 B1-B3 门禁三批全绿:4423 passed+desktop 288 passed+ruff 绿;装机外科已做):
  - 装机外科(世事.app /Applications/世事.app):定向同步 13 件(引擎 telegram.py/registry.py/schema.py/cli.py + telegram/ 包五件 + plugins telegram-groups/telegram-channels/daily-digest 三件),diff 逐字节一致核验;仓库 venv 3.12 对装机副本八项 import 冒烟全过(engine/vocab/serve/offsets/events/cli/plugins);并行会话曾中途同步过 telegram/ 包中间态(19:09-19:18 时间戳,缺 events/serve/cli),本次全量覆盖修正;清理三处 stale __pycache__ 后 adhoc 重签(codesign --force --deep -s -,verify --deep 通过;spctl 拒 adhoc 属常态,与装机前同制式)。
  - 统一装机收尾(2026-10-06 20:19-20:31,终局收尾员,覆盖桌面接线批 5345efe):备份 `/tmp/myssia-b3desktop-backup-20261006-201905`(bundle entry.py+telegram/serve.py 前版)后定向同步两件——`desktop/entry.py` → bundle `Resources/myssia-src/entry.py`、`src/myssia/telegram/serve.py` → bundle `myssia/telegram/serve.py`;stale `entry.cpython-312.pyc` 清除;四件 sha256 全量对拍 **4/4 一致**(entry.py `7de9db12…`/serve.py `7e66363b…`/store_report.py `c4b330c8…`/数据根 daily-digest.yaml `314aef59…`,后两件为 9859911 批 20:13 已同步件,本轮复核零漂移);装机 python(`<数据根>/python/bin/python3`)直载冒烟过(entry.py serve/cli_main+telegram 三装配符号 `_assemble/_start/_stop_telegram_host`+`TelegramServeHost`+store_report 全命中);`codesign --force --deep -s -` adhoc 重签+`codesign -vv` 双过(valid on disk/satisfies its Designated Requirement);沙箱 serve(MYIA_HOME 临时根+真品类件 copy)经 `logs.tail` 亲读 telegram graceful 留痕原文(bot token 未配 keychain:myia/telegram/bot-token+主人四步指引),EOF 退出码 0——装配路径离线真跑实证,零网络零真发;`open -g` 静默拉起装机包:前台 DoubaoWork 拉起前后不变、新进程树 13732(壳)/13738(sidecar,换装重签后拉起=新代码),ticker 心跳双验(新写者戳 `…-13738` age=29s 即现+65s 续跳 mtime +60s 与 `DEFAULT_TICK_INTERVAL_SECONDS=60` 吻合;旧死戳 `…-12989` 被写者顺手清,hermes 判例真机生效),telegram 宿主 graceful 文件证据=数据根无 telegram/ 目录(token 未配未起,serve 未被拦);装机实例保持常驻(cron 照跑)。窗口计数 osascript 返回空如实注记,静默性以前台不变为准。
  - AC4 的「像素验证」已随桌面接线批结案:该批零 UI 改动不适用(桌面接线批过程段明记);AC1 真发留主人 token。

## 结果(验收回执,完工填)
- [ ] AC1-5 勾选+证据(**终局收尾员 2026-10-06 终验对照,全留未勾,缺口如实**):
  - AC1 bot 线端到端:**未满足**——代码面全就绪(B1 引擎+B2 过滤出口+B3 serve,`myssia telegram serve` 可跑),真发回执缺主人四步(bot/关隐私/token/拉群),token 未入钥匙串即 credential_missing 零请求空态(设计如此);回执位留待 token 到手。
  - AC2 Telethon 线端到端:**未开工**(B4 批,锁主人小号+验证码前置)。
  - AC3 组件化件全流程一例:**未开工**(B5 批)。
  - AC4 全 mock 单测+装机外科+像素验证:**满足(统一收尾批 2026-10-06 20:31 结案)**——mock 单测在案(B1 31 例+B2 25 例+B3 21 例+桌面接线批 7 例);装机外科 13 件(B1-B3)+桌面接线两件(5345efe entry.py/serve.py,统一收尾批 20:19 同步+sha 对拍 4/4)+数据根补同步全数在案;像素验证=桌面接线批零 UI 改动不适用(判例在案)。
  - AC5 凭据零外显+风控披露:**代码与测试面在案**(token URL path 净化 bot***、httpx 异常消息同净化、凭据三态 reddit 判例、测试断言 BOT_TOKEN 不外显;小号风控披露在 research/prd);真跑前的完整验收留 AC1 同窗。
- [x] **数据根 YAML 同步**(终局收尾员补做,2026-10-06 19:4x):数据根 `~/Library/Application Support/MYIA/plugins/daily-digest.yaml`(cron「每日合并日报」job enabled 在跑的活件)先前缺「Telegram 群」分区 = B2 出口在装机侧断环;已备份 `.bak-20261006-finalconsolidate` 后以仓库件覆盖,diff 逐字节一致,telegram-mihomo_party_group 源在册 1 处。telegram-groups.yaml 未部署数据根(与"serve 常驻时不必挂 cron"自洽:cron jobs.json 无该品类建档,装机包内示范件已在)。
- [x] **终局门禁复核**(收尾员亲跑,2026-10-06 19:36-19:38,树=0b15e09+587f49b 静置后):全量 pytest 4711 passed/40 skipped/0 failed;vitest 570/570(26 文件);tsc -b 0 错;desktop `npm run build`(tsc -b && vite build)通过;装机件复核:两线 14 件(telegram 9+store 2+entry.py+plugins 2)仓库↔包内 cmp 逐字节一致,主二进制 sha256 `4af5d62b…ead3` 与 feed 档 19:19 回执一致,`codesign --verify --deep --strict` exit 0 亲验。附记:19:23 首轮全量曾 7 failed(test_telegram_serve.py),系 B3 工程师会话当时正在写入中间态(源/测试 mtime 落在跑窗内),提交定稿后两轮全绿,非代码红。
- [x] **统一收尾批门禁复核**(终局收尾员亲跑,2026-10-06 20:29-20:35,装机实例常驻并行):vitest **570/570**(26 文件,20:29:31 起 6s 完成)与 tsc -b **0 错**跑窗干净;全量 pytest 首轮(20:29-20:31)4 failed(desktop 装配 1+telegram serve 3)——mtime 取证定位根因=**并行会话(10-06-native-plugin-components 等)20:28:37-20:35:16 正在写入工作树中间态**(serve.py 20:28:37/entry.py 20:29:11/test_telegram_serve.py 20:30:45 均落首轮跑窗内),与本档 19:23 先例同型非代码红,单独复跑 4 例 4/4 passed;全量复跑(20:33-20:35)**4810 passed/40 skipped exit 0**——**如实分界:此绿基线=HEAD(5345efe)+20:33 时点并行在途件的工作树**(覆盖面 ⊇ HEAD,未引入红;纯 HEAD 基线因并行会话持续在写无法在本窗口重跑,stash 并行件属禁手;5345efe 定稿时分域绿 desktop 295+telegram 47 在案,9859911 纯 HEAD 全量 4722 在案);本收尾批零源码改动,不属「本批引入」修复面。另注首轮命令 `| tail` 管道吞退出码属 SOP 坑清单在案坑,复跑已直落盘保留真实 exit。装机外科对拍时点(20:19)工作树四件与 HEAD 零 diff 亲验,装机包=HEAD 定稿版,其后 20:28+ 并行再写工作树不影响装机定稿。装机四件 sha 对拍+重签+静默拉起+心跳+沙箱留痕明细见过程段「统一装机收尾」。

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

## 追加回执:独立深审修复批(2026-10-06 20:52,F8/F9/F10/F11/F12/F13/F14)

- **修复面七发现**(提交 `bced6c5`,10 文件 +614/−52,全 mock 零网络零钥匙串):
  - **F8(high) 多 bot 双宿主共享单键 offsets.json 交叉污染→静默丢单**:offsets.py 按
    bot token 指纹分键(`offsets-<sha8(token)>.json` 兄弟文件;update_id 是 per-bot
    独立序列,A bot 游标对 B bot 是越前游标=漏拉);旧单键迁移=**采纳一次即删**
    (单 bot 升级不断点;第二 bot 从 0 续拉由锚点去重兜底——重放安全、越前不安全);
    events.py 账本同指纹分库(`events-<sha8>.db`,counts 不跨 bot 混计);cli.py 与
    desktop/entry.py 装配面同批传 bot_token。多宿主交替写/迁移链/桌面装配指纹断言入档。
  - **F9 过滤配置校验晚于 offset 确认**:`_filter_options()` 前移到任何 I/O 之前
    (确认是全 bot 不可逆语义);时序测试钉死零请求零确认。
  - **F10 serve poller transport 异常未净化**:httpx 异常 str 带完整 URL(含 token);
    engines 导出 `mask_token_text` 公开件,serve transport+malformed 两路径过门,
    token 零外显断言入档。
  - **F11 telegram_events 无界增长**:executions 1000 行帽判例,record 每写一裁
    (同事务)+显式 prune();1005 写→帽 1000 最旧出列测试。
  - **F12 merge_high_value 区间文档措辞**:锚形态如实(首条 url+`-hv<N>-<尾 id>`,
    非 `<chat>-<min>-<max>` 区间对;数值序 id 全量在 merged_message_ids)。
  - **F13 媒体组跨轮**:长轮询分批把同 media_group_id 切两轮→后到带 caption 成员
    重复出条;`updates_to_items` 增 skip_groups 前缀(批量档窗口自带重叠免传,如实
    注记),serve 宿主跨轮记忆(chat:gid 保留一轮);相册切两轮测试。
  - **F14 未配通道虚账+资源收尾**:push sink 契约改返 bool(False=通道未配),账本新词
    `outcome=no_channel`(不再虚记 pushed);宿主退出收 poller 客户端 aclose(新增,
    软探兼容 fake),账本归装配方收(cli finally / desktop bundle close 各补)。
- **门禁**:pytest 全量 **4810 passed/40 skipped**;ruff 绿;gitnexus detect-changes
  (staged)= 10 文件 70 符号 0 执行流 **low**。store 层 F6 校验对称另批 `4acfc42`。
- **装机外科**(2026-10-06 20:45-20:48):`vite build`+`npx tauri build` exit 0
  (UI 批 eef5ff1 同窗,一次重打包覆盖两批);备份
  `/tmp/myssia-app-backup-20261006-204559-deepaudit`;ditto 换装;主二进制 sha256
  `26ad7151…` 构建产物与 /Applications 装机件双验一致;bundle myssia-src 八件
  (entry.py+telegram 包四件+engines/telegram.py+cli.py+store/sqlite.py)sha256
  对拍 **8/8 一致**;bundle 陈旧 `__pycache__` 清除后 adhoc 重签+`codesign -vv`
  双过(valid on disk/satisfies its Designated Requirement);旧实例(13732/13738)
  quit 后 `open -g` 静默拉起新进程树 **36514(壳)/36519(sidecar)**;ticker 心跳双验
  (新写者戳 `…-36519` 即现+65s 续跳精确 +60s 与 DEFAULT_TICK_INTERVAL_SECONDS 吻合,
  旧死戳顺手清);telegram 宿主 graceful 文件证据=数据根无 telegram/ 目录(token 未配
  未起;配好重启即活,首次起即走 F8 指纹键);装机实例保持常驻(cron 照跑)。
