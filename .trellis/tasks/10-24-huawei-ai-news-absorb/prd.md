# PRD — 华为云 AI 采集线收编:词表/定向优惠/厂商日报对齐后关停切换

## Goal

主人准备关停华为云 ai-news-bot(`~/Project/Server/华为云/ai-news-bot/`,云端 /opt/ai-news)。关停前,把该线两个月实弹迭代出的采集能力**整体收编进 MYIA**,使 MYIA 的情报产出质量不低于现役生产线;收编完成后华为云线可安全关停,零能力损失。

## 背景与证据

- 现役生产线 = 华为云 ai-news-bot 三件套(wf_crawl 论坛羊毛 / watch_deals 定向优惠 / ai_daily_report 四区块日报),对账底稿见本档 research.md(§1-§5,含文件行号)。
- 核心差距三条:①MYIA 分类词表冻结在 09-28 生产版,生产已迭代 10-03(五刀)/10-17(云服务器优先)/10-20(硬门槛/假信号/量化门槛/福利专区)三轮;②定向优惠监控与厂商日报聚合两路从未进过 MYIA 需求流;③三个源细节未跟(linux.sb 分类页/cocoloop 福利专区/btsb 复活)。

## Requirements

### R1 分类词表对齐到生产 10-20 版(myssia-classifier)

- 把华为云 wf_crawl.py 的 10-03/10-17/10-20 三轮词表增量完整移植进 builtin keywords.json:
  - `WOOL_HARD_KW` 真羊毛硬门槛替换现有宽松免费判据(FREE_KW 语义由硬门槛接管);
  - `WOOL_FAKE_KW` 假信号否决(听说/据说/合集/【推广 等;生产注释明示的「勿杀」白名单语义保留);
  - NOISE_KW 五刀增补(求助帖族+`吗$|呢$` 尾缀)进 builtin noise 过滤器;
  - 公益/倍率0 豁免付费信号→羊毛;
  - 云服务器/ECS/VPS 类免费优先判羊毛(先于 token 判定);
  - **付费/拉客帖(💰渠道)整体砍**(10-24 主人已裁,对齐生产 10-03 五刀令):paid_hit 或拉客词(中转/relay/逆向/号池/接入了/api站/聚合/车队/纳新/低价/优惠)分类直接丢弃,渠道不再作归宿;wool.yaml push route 的 channel 分支同步退役;
  - 🔑token 进 primary 循环(免免费信号可达,对齐生产 v3.1;MYIA「token 只能免费分支到达」旧设与生产相悖,adjudication 描述同步改写)。
- 金测集(myssia-classifier/tests/classify_gold.json)同步扩充钉住新语义;样本取生产实弹标题(research.md §2 各词表注释里的案发标题)。
- 词表升级是**全局**的:所有走 builtin 的品类随之生效(与生产行为一致)。
- myssia-classifier 版本 bump;主包 golden/测试同步。

### R2 wool 源细节对齐

- linuxsb 改抓 `/forum/2` 分类页(10-24 已实测:福利放送版块 50 帖,选择器与首页同构,落配置即跑);
- cocoloop 改抓福利专区 **HTML 页** `https://www.cocoloop.cn/c/welfare/19`(10-24 已实测:SSR 60 行 topic-list-item,既有选择器直用;不走生产 .json 路——该站 robots 禁 `*.json`);
- **ai-news.yaml 删自带的 cocoloop /latest 讨论流源**(10-24 主人已裁 Q2):图二讨论帖混入 AI 资讯的根治;daily-digest 分区一 sources/labels 清单同步删;cocoloop 的情报价值由 wool 侧福利专区承接;
- bbs.bt.sb 复活复测(MYIA firecrawl 云端通道重测;活则恢复源,死则如实保留移除态并记档);
- V2EX 保持现有 firecrawl 形态(生产用官方 API,MYIA 可顺带评估换 API 形态,实测定,不强制)。

### R3 定向优惠监控(watch-deals 新品类)

- 承载 TapNow / RunningHub / MiniMax 海螺三源,机制=快照 diff(首跑建基线不推;变动才产条目;抓取失败不动基线);
- `DEAL_SPECIFIC_KW` 量化门槛移植(纯营销话术零条产出);
- TapNow 已知降级态如实保留(0 条=合法静默,不误报);
- 推送路由并入现有羊毛/白嫖出口,进 daily-digest 既有「AI 白嫖与优惠」分区。

### R4 AI 厂商行情聚合(新品类+日报分区)

- NVIDIA block 数据面:股价(现 Yahoo 通道,腾讯 qt.gtimg.cn 作华为云同款备选)+ GPU 跨区比价(美价 MSRP 表+汇率+国行 ZOL 实抓+便宜/贵%)+ B站「显卡日报」最新视频行(芝士华莱士合集 API);
- 源站单点失败不拖垮整块(生产 10-20 判例:价格源挂了股价照发,标降级提示);
- 以新分区并入 daily-digest(「AI 厂商行情」,detail 形态),取代已退役的 ai-vendor-watch 分区位;
- **公司/大V标签库落地(P2→P1 升格,10-24 技能深探)**:migrate-data.tgz 本地快照含 companies.json(20 公司:name/region/keywords)+influencers.json(22 人:name/role/region/keywords/min_score)——迁入 MYIA 为 ai-news 品类打标规则(命中打 `<公司名·🇨🇳/🌍>` tag);大V优先级排序与按公司分组渲染为后续可翻案项。

### R5 aihot 深挖(P1 尾档,可延后)

- aihot.news 三路合流(/daily 昨日回顾+/首页实时流+/hot 48h 热榜),X 原文直链进条目元数据供模板优先渲染。

### R6 关停前抢救(前置步)

- **本地 10-17 快照已位**(migrate-data.tgz:companies/influencers 标签库+wooly_sent/daily_sent_items/deals_snapshot/push_target×4+RUNBOOK)——抢救降级为「云端增量补拉」(10-17 后的注册表增量;SSH 通则拉,不通不阻塞关停,增量丢失最坏代价=个别条目重推一次);
- fc_cloud.json(firecrawl 云钥)不在快照内,若 MYIA 侧 keychain 已有等价凭据则免拉;
- 华为云版 `deals_shown` NameError bug(行 664,优惠队列清不掉→日报重演)记档告知主人,关停前不修(反正要关),MYIA 侧不移植。

### R7 一行富文本渲染规范(主人 10-24 判例,图二实发日报纠偏)

- 日报条目 = **「编号. 标题」一行**,链接挂**标题本身**(富文本可点,渲染后只见标题文字);
- **不带**任何额外可见物:`[来源]` 方括号前缀、「原文」尾注、裸 URL;
- 实证:MYIA 10-23 PM 实发日报每条尾巴挂「原文」、每行带「［热点聚合］［CocoLoop］」前缀——主人令「这种设计就不对,要一行富文本」;
- `store_report` 引擎的 `LINK_LABEL`(原文尾注)与 `label` 前缀渲染机制移除,`daily-digest.yaml` 分区 `labels` 配置随之退役;wool 速报模板本就标题即链接,不动;
- detail 分区明细行同纪律:文字为主,链接挂文字(如 📺 视频行),不出现裸链/尾注。

### R8 调度对齐生产节奏(10-24 技能深探新发现)

- 生产真实节奏:`8:00 采集 → 8:30 日报 → 12:00 午间轮全链式`(PM 槽=中午;图一图二均 12:01 产物=主人中午看报);
- MYIA 现状 PM 槽=20:05 晚间,与主人实际阅读节奏错位——**默认对齐**:daily-digest PM 20:05→12:05,第二跑采集线(wool/watch-deals/ai-vendor-daily)相应前移至 11:00-11:30 窗;可翻案。

### R9 工程加固:环境代理污染防(生产 10-20 同型事故)

- MYIA 主抓取路径客户端构造(pipeline.py:1374 等)不带 `trust_env=False`,环境 HTTP_PROXY 会静默劫持 `proxy: direct` 源(症状=全源 empty 不报错;vision/collect.py:366 已认知此 httpx 行为但主管线未防,全仓 trust_env 零命中);
- 修复:direct 语义=真直连(客户端显式 trust_env=False),测试钉住;生产排查口诀「源批量 empty 先 curl 直连 vs 代理各测一次」入运维档。

### 非目标(明确不做)

- 不移植:每源配额机制、飞书单卡版式(MYIA 维持 text 日报)、「群送达才记/预览不消耗」去重语义;
- **停用线不迁勿再启用**(技能档 10-24 判例):ai_news_crawl/push(*/30 增量线)、TrendShift/GitHub 趋势区块、重磅标准即时增补链路、Mac 本地 RSS;
- **X 直抓全路线已死勿再试**(2026-09-30 生产实测判例);X 信息唯一路径=aihot 原文直链(D5 承接);
- **不可达源勿再试**:linux.do(CF Turnstile+禁爬条款)、nodeseek(JS 全壳)、e7ai(宝塔 WAF)、naixi(登录墙)——wool.yaml 占位注释补记判死证据;
- 不引入新核心依赖(汇率用常量表沿用生产,不做汇率 API;六依赖红线不动);
- 不动 wechat/TG/messaging 等无关线。

## Constraints

- MYIA 工程纪律全守:核心零重依赖、明文凭据拒载、schema 铁律(缺口回改 schema 不私加字段)、测试镜像目录布局;
- 分类词表改动=独立包 myssia-classifier 语义变更,金测集是唯一权威口径,升版有据;
- 装机交付判定含装机包刷新与像素级目验(交付判例);
- 词表换硬门槛后 wool 收量会**下降**(生产行为如此,主人 10-20 自己定的)——交付汇报须说明预期变化,不算回归。

## Acceptance Criteria

- [x] AC1 词表:myssia-classifier 金测集含 10-20 全部新语义用例(硬门槛/假信号/五刀 noise/公益豁免/云服务器优先/付费渠道砍[Q1 已裁]/token 免免费可达),全绿;主包 classify 相关测试同步绿;classifier 版本 bump。
- [x] AC2 源对齐:cocoloop 福利专区真跑 >0 条且为福利帖(非讨论帖);linuxsb /forum/2 真跑出帖;btsb 复活结论如实记档(活:恢复入源;死:证据在档维持移除)。
- [x] AC3 watch-deals:RunningHub+海螺真跑入库;首跑建基线零推送(静默留痕);DEAL_SPECIFIC_KW 单测钉住(话术标题 0 条、量化标题放行)。
- [x] AC4 厂商行情:真跑产出含股价+GPU 比价≥2 行+视频行(或如实降级标注)的条目;daily-digest 新分区渲染目验(真发主人 DM 或 dry-run 快照+OCR 证据)。
- [x] AC5 全量门禁:`uv run --no-sync python -m pytest -q` 全量零新红;ruff 过;触及 golden 的变更再生成有据。
- [x] AC6 抢救:本地 10-17 快照(migrate-data.tgz 七件套)解包归档到位;云端增量补拉完成或不阻塞说明;华为云 bug 记档已告知。
- [x] AC7 关停就绪声明:逐能力对照表(MYIA 承载面 vs 华为云三件套)全部「已承载/已对齐/如实弃用(列明)」,交付汇报首段明确「华为云线可关停」或列残余缺口。
- [x] AC8 装机:装机包刷新+装机态真跑一轮 daily-digest 含新分区(像素级证据)。
- [x] AC9 渲染规范:store_report 产出的日报逐行核——零「原文」字样、零方括号来源前缀、条目单行且标题可点;`tests/engines/test_store_report_engine.py` 版式快照按新契约更新全绿;真发或 dry-run 快照目验。
- [x] AC10 调度对齐:PM 日报 12:05 发出(或翻案记录),采集线前移后 12:05 报窗有当日午前新条目;jobs.json 各品类 schedule 与设计表一致。
- [x] AC11 代理加固:显式 `trust_env=False` 直连语义落地并有测试钉住(HTTP_PROXY 环境下 direct 源不被劫持的单测)。
- [x] AC12 标签库:companies(20)/influencers(22)迁入 ai-news 打标规则,真跑条目带 `公司·🇨🇳/🌍` tag 抽验 ≥3 条。

## 开放裁决点(规划期默认,可翻案)

1. V2EX 换官方 API 形态与否——默认「实测顺利则换」,不顺则维持 firecrawl;
2. ~~companies/influencers 标签库 P2~~——10-24 升格 P1(R4,数据件本地快照在位;大V优先级排序/分组渲染仍为后续);
3. 腾讯股价接口——默认 Yahoo 主+腾讯备(双源任一活即出价);
4. aihot 深挖若当期排不下,可独立尾档延后,不阻塞关停声明;
5. PM 槽 20:05→12:05 调度对齐(R8)——默认对齐生产午间轮节奏;
6. 推送群目标——生产=AI福利群+私聊双发,MYIA 默认维持 analyst DM 单发(群目标需 bot 在群+凭据,要加另裁)。
