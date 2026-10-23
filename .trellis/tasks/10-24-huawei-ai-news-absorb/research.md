# research.md — 10-24-huawei-ai-news-absorb:华为云现役采集线对账底稿

> 本档为 2026-10-24 会话对账实录,全部结论有文件/行号证据。执行中如与现势冲突,以重测为准并回写本档。

## §1 现役生产线定位(排查链)

- 图上日报(AI信息 2026-10-23-PM 四区块)产地 ≠ 本地 Hermes(~/.hermes/cron/jobs.json 至今为空,`{"jobs": [], "updated_at": "2026-09-24"}`)。
- 现役 = `~/Project/Server/华为云/ai-news-bot/`(007idc 2026-10-17 迁华为云后的 v3.1),云端跑在 docker `python:3-alpine` + `/opt/ai-news` 挂载,链路见同目录 run_daily.sh(仅 6 行:wf_crawl → watch_deals → ai_daily_report)。
- 旧机参考件 = `/Volumes/郑冰津/爬虫/007idc-迁移包/`(旧版代码+workflows 摘要文档,已被华为云版迭代超越,仅作历史对照)。
- 华为云版三个 py 的注释里带完整纠偏史:09-28(双信号)/10-03(五刀)/10-17(迁移+云服务器优先)/10-19(多档合并)/10-20(硬门槛/假信号/量化门槛/福利专区/强制无代理)。

## §2 wf_crawl.py(论坛羊毛爬虫)实况要点

- 源 10 路(行 29-44):linux.sb **/forum/2 分类页**、bbs.bt.sb /latest(大陆被墙走云 FC 海外出口,**活着**)、sb.sb、nodeloc、**cocoloop 福利专区 JSON** `/c/welfare/19/l/latest.json`(10-20 改造:首页混合流被讨论帖稀释)、dalao、74站(JS壳 waitFor=10000)、V2EX×3 **官方 API** `api/topics/show.json?node_name=free|deals|share`(非 HTML)。
- 每源配额(行 34-44):linuxsb 16/btsb 12/sbsb 8/nodeloc 8/cocoloop 6/dalao 6/74站 3/V2EX 6+6+4,总量 cap 44。
- 词表体系(行 49-104,全部正则原文可直搬):
  - `FREE_KW`(09-28 版强免费信号)
  - `PAID_KW` 付费信号
  - `CAT_RULES` 八类(🎁羊毛/💳信用卡/🪜节点/🛒代买/🖥️服务器/💰渠道/🔑token/🤖AI信息)
  - `DEAD_KW` 失效帖(已耗尽/已跑路/…/已用完)
  - `NOISE_KW` 站务+**10-03 五刀求助帖**(报错/是什么/怎么办/…/`吗$|呢$`)+论坛自家活动
  - `REG_LURE_KW`+`DIRECT_GIVE_KW` 注册引流帖否决(09-28)
  - **`WOOL_HARD_KW` 真羊毛硬门槛(10-20 主人令:必须有可领/量化/动作信号)**
  - **`WOOL_FAKE_KW` 假信号(10-20:听说/据说/合集/【推广/直降叠加/N一个出/精品域名;但 TG 助力机器人/WorkBuddy 申请成功/自部署教程算真羊毛勿杀)**
- 裁决序(cat_of,行 203-239):注册引流否决 → 假信号否决 → WOOL_HARD 命中分支(**公益/倍率0 豁免 PAID→羊毛**;云服务器/ECS/VPS 非付费→羊毛[10-17];token 语境→🔑token;非付费→羊毛)→ 无免费信号走 CAT_RULES(跳过羊毛/渠道)→ **付费广告/拉客帖整体砍(10-03 五刀,含 中转/relay/逆向/号池/聚合/车队/纳新/低价/优惠)** → AI信息类与日报撞车剔除。
- 去重(行 242-347):URL 归一分页/回复参量 → 同 URL 跳过;跨源同标题指纹(前 18 非单词字符)合一;wooly_state.json seen 库 1500 上限滚动。**爬虫层不判新,全量活跃清单交给日报层**。

## §3 watch_deals.py(定向优惠监控)实况要点

- 三源(行 72-231):TapNow pricing(华为云大陆出口已知降级 0 条,行 122-127 定性注释)、RunningHub 首页横幅(直抓锚点→FC markdown 兜底)、MiniMax 海螺 hailuoai.video/pricing(SSR 直抓)。
- **快照 diff 机制**(行 234-276):抓 → 与 deals_snapshot.json 指纹比对 → 变动行入队 deals_pending.json → 日报消费;**首跑只建基线不推**;抓取失败不动基线(防抖动误报)。
- `DEAL_SPECIFIC_KW`(行 23-27,10-20 主人令):优惠条目必须带量化信号(¥$数额/N元块刀credits积分额度天次/N折%/兑换码/CDK/coupon),纯话术(赢现金大奖/邀新争霸赛)不发。

## §4 ai_daily_report.py(四区块日报)实况要点

- **AI 日报**:aihot.news 三路合流——`/daily`(站方昨日回顾 25 条+分类+**X 原文直链** origins)、首页实时流 `/story/`、`/hot` 48h 热榜;三路标题指纹去重(前 16 字符);**条目级防重 daily_sent_items.json(item URL 永不重推)**;同日同槽只发一次(last_daily_report.txt)。
- **AI 厂商日报**(行 509-536):NVIDIA 恒定第一 = 腾讯美股接口股价(qt.gtimg.cn,10-20 因 Yahoo 403 华为云 IP 换道,行 30-50)+ GPU 三行跨区比价(行 70-109:美价=MSRP 常量表 `GPU_MSRP_USD={RTX PRO 6000:8500, RTX 5090:1999, RTX 4090:1599}`、汇率常量 `USD_CNY=7.25`、国行=ZOL 两页直抓含 5090 系列页 s11096、`title="..."...price-type">N<` 正则抽价、便宜/贵% 计算 <3% 判持平)+ **B站显卡日报视频**(行 53-67:UP主芝士华莱士 mid=22697887 合集 API `seasons_archives_list?season_id=2565297` 取最新「显卡日报」期)+ NVIDIA 新闻 ≤2 条;其余公司按 **companies.json/influencers.json 标签库**分组(行 170-192,数据件在云端 /opt/ai-news,本地迁移包**没有**)。
- **羊毛日报**(行 539-607):wooly_fresh(💰渠道砍掉[10-03 五刀])+ deals 队列并入;**同厂商多档合并**(行 574-599,10-19 主人令);wooly_sent URL 指纹(09-28 从标题指纹改 URL)。
- **去重状态只在群(chat_id)送达后落盘;私聊预览永不消耗去重标记**(行 634-667)。
- 尾戳 = `{time} 实时爬取生成 · 全条目指纹去重 · 无新内容自动静默`(行 611)。
- ⚠️ **真 bug(2026-10-24 发现)**:行 664 引用从未赋值的 `deals_shown` → 群送达成功(group_ok=True)后必然 NameError 崩溃,后果 = deals_pending 队列永远清不掉,**TapNow/RunningHub/MiniMax 条目会在羊毛日报里反复出现**。迁移不移植此 bug;可向主人核对最近日报是否常客重演。

## §5 MYIA 现状对账(差距精确定义)

### 5.1 词表:冻结在 09-28,生产已迭代到 10-20

`myssia-classifier/myssia_classifier/data/keywords.json` 自述「忠实移植自生产爬虫 wf_crawl.py(**2026-09-28 主人纠错版**),由金测集钉住语义」。已建模:FREE_KW→freebie.keywords、PAID_KW→signals.paid、DIRECT_GIVE_KW→signals.direct_give、token_context 细分、DEAD_KW→filters.dead、NOISE_KW(09-28 版)→filters.noise。

**缺失(生产 10-03/10-17/10-20 三轮)**:
1. `WOOL_HARD_KW` 硬门槛(10-20)——MYIA 免费判据还是 09-28 宽松版 FREE_KW
2. `WOOL_FAKE_KW` 假信号否决(10-20)——整体缺失
3. NOISE_KW 的 10-03 五刀增补(求助帖族+`吗$|呢$` 尾缀)——只在 wool.yaml 有三条 category-scoped drop 规则(10-19 我方试错版),builtin noise 表没有
4. 公益/倍率0 豁免 PAID(10-20)——缺失
5. 云服务器/ECS/VPS 免费优先→羊毛(10-17)——缺失

### 5.2 源细节(wool.yaml)

- linuxsb 抓首页(生产抓 /forum/2 分类页)
- cocoloop 抓 /latest 混合流(生产 10-20 已改福利专区 JSON——正是被讨论帖稀释后主人改掉的)
- btsb 10-17 判死移除(MYIA 三通道实测 468;生产同源经云 FC 活着——需复测)
- V2EX/dalao/nodeloc/sb.sb/74站 与生产同源面
- tapnow-events 占位注释(生产华为云版也降级中,双方一致)

### 5.3 整路缺失(从未进过 MYIA 需求流)

- **watch_deals 定向优惠监控**(TapNow/RunningHub/海螺 快照diff+量化门槛+多档合并)——MYIA 零承载
- **厂商日报聚合视图**(腾讯股价+GPU 跨区比价+B站显卡视频+NVIDIA block)——MYIA stocks/gpu-prices 单件能力在,无聚合
- **aihot 深挖**(三路合流+X 原文直链)——MYIA 只抓 aihot 首页单路
- companies/influencers 公司人物标签库(数据件只在云端)

### 5.4 机制差异(非缺口,记录在案)

- 生产「群送达才记去重/预览不消耗」语义 vs MYIA url dedup+槽位锚点——语义等价度足够,不移植预览语义
- 生产每源配额 vs MYIA max_pages/max_entries 帽——暂不移植配额概念(设计可翻案)
- 生产飞书单卡 markdown 分区 vs MYIA daily-digest text 消息(Hermes 版式,10-06 批次4 定案)——版式维持 MYIA 现状

## §6 MYIA 承载面盘点(可复用件)

- `classify/` builtin = 数据代码分离的关键词表(升级即改 keywords.json+金测集,版本 bump 走 myssia-classifier 独立包)
- `engines/`:direct_api(json_path extract)/static_html/firecrawl/**urlwatch(变更监控,#watch- 判例)**/store_report(链外报表)/prompt(链外 LLM)——watch_deals 的快照 diff 形态与 urlwatch 引擎同构
- `config/daily-digest.yaml` 分区机制(源名锚+labels+style:detail+max_entries)——厂商行情分区直接挂
- `dedup.py` url 键+槽位锚;`cron/` 生产 jobs 机制全在
- stocks.yaml 已有 Yahoo 股价(生产因华为云 IP 被墙换腾讯接口;MYIA 本机走 proxy pool 可继续 Yahoo,腾讯接口作大陆备选)

## §8 10-24 主人判例:图二 MYIA 实发日报纠偏(渲染规范)

- 图二 = MYIA 10-23 PM 槽实发「情报日报」(OCR 存档):每条句尾挂「原文」、每行带「［热点聚合］［CocoLoop］」方括号前缀。
- 主人令:「这种设计就不对,要一行富文本,不要添加很多额外的 [] 原文等内容」。
- 根因 = `store_report.py:308` 句尾拼 `[原文](url)`(`LINK_LABEL`)+ `:306` `[{label}]` 前缀;docstring 行 30-33 的「布局纪律」是 10-06 对产线的误读——生产 `ai_daily_report.py:503` 实为 `f"{n}. [{t}]({e['url']})"`,**链接挂标题本身,无原文尾注、无来源前缀**。修正落 design §8(D6)/prd R7/AC9/implement Step 4.5。
- 图二同时实证词表/源面缺口:第 6-15 条 CocoLoop 求助讨论帖(「哪个大模型最强呢」「报错怎么办」「有能平替的方案不」)混进 AI 资讯——D1 五刀 noise 与 D2 cocoloop 福利专区改造的直接论据。

## §9 grill 第一轮事实修正(2026-10-24,全部实读代码/实测源)

- **F1** `filters` 键集钉死恰 `{dead,noise,registration_lure}`(builtin.py:298)——加 fake 需改加载器+ClassifyTable;section 支持 keywords/patterns/case_insensitive(`吗$|呢$` 可落 patterns)✓。design §2 已修正。
- **F2** `adjudication` 数据节仅 `fallback_target`(ai-news 兜底);免费分支裁决序写死在 classify_title(builtin.py:399-421)——公益豁免/云服务器优先/渠道砍全是代码改动。design §2 已修正。
- **F3** 生产 v3.1 no-free 分支:CAT_RULES 循环**含 🔑token**(免免费可达)且循环后 paid/拉客词→None(渠道被五刀整体砍);MYIA 现状 token 只能免费分支到达(故意设计)+paid→渠道保留+wool.yaml 给 channel 配 digest 路由——三处与生产相悖,对齐=代码改+route 退役(报主人 grill Q1)。
- **F4** custom 规则求值面 = Item.view() = metadata+url/title/source/category/scores/dedup_key(pipeline.py:501-514),**content 不可达**——D3 的 DEAL_SPECIFIC_KW 须先给 urlwatch 引擎加 `metadata.watch_diff_head`(diff 摘要)。「零新代码」修正为「近零代码」。design §4 已修正。
- **F5** classifier 装机通道:keywords.json 经 desktop/build-sidecar.sh:161 PyInstaller --add-data 冻结进 sidecar;升级=重建 sidecar 随正规发布流,无运行时 pip 通道。AC8 闭环无缺口。
- **F6** 源实测(10-24 curl):cocoloop `/c/welfare/19` HTML SSR 60 行 topic-list-item/raw-topic-link(选择器直用 GO);linux.sb `/forum/2`=福利放送版块 50 帖、首页 52 帖,`div.post-body`/`a.post-title` 同构健康(无回归)。**方法论坑:单行压缩 HTML `grep -c` 恒 1,判源必须 `grep -o|wc -l`**(本轮自己踩的)。
- **F7** builtin:true 影响面=ai-news+wool 恰两品类(全 config grep 实证)。
- **F8** 图二第 6-15 条讨论帖混入源头=ai-news.yaml 自带 cocoloop /latest 讨论流源(非 wool 侧);生产 AI 资讯无 cocoloop 源——根治=删源(报主人 grill Q2),五刀 noise 只能杀带求助词形态。

### 主人裁决(2026-10-24「都按推荐」,已回写 prd R1/R2、design §2/§3、implement 1.3/1.5)

- ✅ Q1 渠道/paid 广告整体砍:对齐生产五刀,wool.yaml channel 路由同退役。
- ✅ Q2 ai-news 删 cocoloop 讨论流源:删,分区一清单同步;讨论帖混入根治。

## §10 技能层深探(2026-10-24 第二轮,主人令「深度再探索 Hermes 的 ai-news 技能与代码」)

### 10.1 技能定位

- `~/.hermes/skills/productivity/ai-news-secretary/SKILL.md`(v2.1/2.2)=整条产线的**运维知识库**(代码外的判例/坑/铁律全在这);`intel-hub/SKILL.md`=情报总控(四层流水线架构+多服务器地图)。
- 120 技能面里与采集相关仅此两个+feeds(空壳只有 DESCRIPTION);其余是通用技能(firecrawl 套件/lark 套件等),无第三处采集逻辑。

### 10.2 技能揭示的代码外新事实

1. **真实 cron 节奏(华为云 crontab 三条直挂,无 run_daily.sh)**:`0 8` wf_crawl+watch_deals(容器带 mihomo 代理 env)→ `30 8` 日报三合一卡 → `0 12` 午间轮全链式。**PM 槽=中午 12 点**(slot=hour<12?AM:PM,12:00 跑即 PM)——图一图二两份日报均 12:01 产物=主人中午看报。MYIA 现状 PM=20:05 晚间,节奏错位。
2. **数据件本地 10-17 快照在位**:`~/Project/Server/华为云/data-pending/migrate-data.tgz` 含 companies.json(20 公司:字段 name/region/x_accounts/keywords)/influencers.json(22 人:name/handle/role/region/keywords/**min_score**)/wooly_sent/daily_sent_items/deals_snapshot/push_target×4 版本/RUNBOOK.md/已停用旧线脚本(ai_news_crawl/push)+状态日志。Step 0 抢救从「七件必拉」降级为「10-17 后注册表增量补拉,不阻塞关停」。
3. **标签库规格实证**:推送优先级=大V个人(创始人/CEO min_score=0 全推)>公司官方>行业速览(命中≥3家的综合帖);分析师需站点评分≥60;命中打 🇨🇳/🌍 region 标签。
4. **不可达源勿再试清单(生产实测排除)**:linux.do(CF Turnstile+禁爬条款)、nodeseek(JS 全壳 0KB 连 FC 都是)、e7ai(宝塔 WAF)、naixi(登录墙)。
5. **X/Twitter 直抓全路线死亡判例(2026-09-30 实测,勿再试)**:主页登录墙/syndication 429/xcancel 停服/nitter 403/RSSHub 公共实例全 502/Firecrawl search 只搜到 bio。**唯一可行路径=aihot /daily 的 [原文](x.com/status) 直链**(每轮 ~27 条中 ~9 条带),渲染时 X 直链优先。
6. **aihot 单源依赖风险与格式哨兵**:生产自己记着「补一手源是既定待办」(MYIA 17 源已领先,此项不迁);/daily 于 09-30 改版过(双格式兼容在 parse_daily),**站点改版→解析静默归零不报错,巡检=看条目数**。
7. **HTTP_PROXY 污染坑(生产 10-20 事故)**:cron 容器 env 代理被 urllib 自动继承→直连可达源全被塞进死 mihomo→全源 empty 且不报错;正解=显式 `ProxyHandler({})` 无代理直连。**MYIA 同型暴露实证**:`pipeline.py:1374` `httpx.AsyncClient(timeout=…)` 无 trust_env=False(trust_env 缺省真=读环境代理),`proxy: direct` 在有 HTTP_PROXY 的环境下会被静默劫持;vision/collect.py:366 注释已认知此 httpx 行为但主管线未防。全仓 trust_env 零命中。
8. **技能文档滞后于代码的判例**:技能 v2.1(09-25 定稿)说羊毛区块「🤖AI信息已剔除」,但现行代码 `ai_daily_report.py:548` 只排 💰渠道,AI信息条目保留(图一第 1 条 [AI信息] 智谱送周卡实证)——**以代码+实发日报为准**,技能是历史快照。
9. **停用线清单(勿迁勿再启用)**:ai_news_crawl.py+ai_news_push.py(*/30 增量推送,09-25 被 run_daily 取代)、TrendShift/GitHub 仓库趋势区块(09-25 移除)、重磅标准即时增补链路、Mac 本地 RSS(已删)。
10. **推送目标**:生产=AI福利群(chat_id)+主人私聊(open_id)双发;push_target.json 10-17 版在 tarball。MYIA 现状=analyst DM 单发,群目标列为可翻案开放点(需 bot 在群+凭据)。
11. **羊毛区块渲染定稿(09-25)**:`N. [类别emoji] [标题](原帖链接)` 平铺、无来源尾巴(主人令论坛站名不显示)、只放白嫖类——MYIA wool 速报模板需加类别 emoji 前缀(D6 扩展)。
12. **aipocket(凭证猎手)**:仍在 007idc 未随迁(PG+Redis);MYIA 已有 credhunter 引擎承载,intel-hub 四层图里属采集层并列件,本任务不涉。
13. 生产弱于 MYIA 的点(记录不迁):aihot 单源依赖 vs MYIA 17 源;sb.sb 生产抓首页(优惠区 404 后改的)与 MYIA 一致;nodeloc 生产用首页 MYIA 用 /latest(等价)。

## §11 执行收尾纪要(2026-10-24 主会话,工作流 dwfrun-ad2ff00d 落地后)

### 交付实况

- 九步全过,全量门禁绿(pytest+ruff 脚本级直跑),9 笔提交:e0f4cd3c(词表v2)/8aa19856(主包联动)/a01876e4(wool源)/5b67d161(vendor_market)/2cda699c(watch-deals)/3272c0a2(渲染D6)/c1e1a3a5(trust_env+调度)/870b036c(aihot+标签库)/9f2768c8(装机收口);装机件已换装(旧包备份世事.app.bak-20261024-061010)。
- 验收员两条 low 已闭案:
  - **AC3 误诊闭案**:urlwatch 基线本就落 ~/.myia/urlwatch/cache.db(引擎 docstring 契约),非 myssia.db change_baseline(那是数值基线机制);CacheEntry 9 行实证——watch-deals 三源(runninghub 10181B/hailuo 679071B/tapnow 284B 降层)+ai-news 四源 05:32 自愈重播(s3 误删事故的 announce_new:false 重建)。下一轮 cron 遇 cache 即 watch_unchanged,无变更盲窗。
  - **AC10 文档矛盾闭案**:design §9 表 10:30/11:15 vs implement 4.6.2「统一取整」——实际落地 30 6,10 与 0 7,11 照 implement(五段 cron 异分钟须拆 job 的取整理由在案);design 表已回改对齐,非实施偏差。

### 事故与告知(工作流 findings 中须主人知悉的三条)

1. **【s5 非预期真推】**实施员沙箱跑未显式 --db,落入仓库根 gitignored 开发库 myssia.db,first_run_quiet 的 immediate 豁免(「宁可重发不可漏发」故意设计)使 235 条 RSS 历史积压合并成一条消息真实发到「AI信息分析师」私聊——主人若见一条大消息即此;真库无此积压形态,后续验证一律显式 --db(已记档,cli.py:457 --db 缺省 cwd 相对是既有坑,与 urlwatch adapter 硬编码 ~/.myia 同列待修小步)。
2. **【s3 误删自愈】**清沙箱时时间戳单位取错,误删 ~/.myia/urlwatch/cache.db 全量 110 行;announce_new:false 机制次日自动重建基线,最坏代价=一个变更窗漏报,已自愈实证(05:32 四源重播)。
3. **【AC6 告知主人】华为云关停前须知**:云端 ai_daily_report.py:664 deals_shown 未赋值 bug——每次群送达成功必 NameError 崩溃,deals_pending 队列永不清理,优惠条目(TapNow/RunningHub/MiniMax)在羊毛日报反复重演(云端 daily.log ≥3 次崩溃实证、现存 4 条积压)。关停后此 bug 随之消亡,MYIA 侧未移植。

### AC7 关停就绪对照表(MYIA vs 华为云三件套)

| 生产能力 | MYIA 承载 | 状态 |
|---|---|---|
| wf_crawl 词表四层否决/双信号/硬门槛(10-20 版) | classifier 0.0.7 词表 v2+裁决序(金测 78 条钉住) | 已对齐(4 条生产分歧有意收紧,fixture 留档可翻案) |
| 10 源论坛面 | 9 活源+g4f(btsb WAF 判死维持移除,双域复测在案) | 已对齐(如实弃用 1 源) |
| watch_deals 定向优惠 | watch-deals 品类(urlwatch+量化闸门) | 已承载 |
| 厂商日报聚合(股价/GPU比价/B站视频) | vendor_market 引擎+「AI 厂商行情」分区 | 已承载 |
| aihot 三路+X 直链+标签库 | aihot-daily/hot 两源+42 条打标规则 | 已承载(旧编号格式双正则不可考,哨兵兜底) |
| 四区块日报版式 | daily-digest(一行富文本 10-24 令) | 已对齐 |
| 调度 8:00/8:30/12:00 午间轮 | 5 8,12 PM 槽+采集线前移 | 已对齐 |
| 数据件/指纹库 | cloud-snapshot-20261017 归档+云端增量拉取 | 已归档 |
| 停用线(*/30增量/TrendShift/重磅) | 不迁(判例在档) | 如实弃用 |

**结论:华为云线可关停。** 残余可翻案项(V2EX API 换形/proxy pool 骑乘取舍/wool 促销品类级收紧/装机启动生效)均在各步 findings 记档,不阻塞关停。
