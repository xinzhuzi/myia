# design.md — 10-24-huawei-ai-news-absorb 技术设计

> 对账事实与生产代码行号见 research.md;需求口径见 prd.md。本档只讲 MYIA 侧怎么落。

## §1 总体边界

五个交付面互相独立、可分批合入:

| 面 | 落点 | 性质 |
|---|---|---|
| D1 词表 v2 | `myssia-classifier`(keywords.json+金测集+builtin.py 裁决序+版本) | 语义变更,全局生效 |
| D2 wool 源对齐 | `config/wool.yaml`(repo)+装机数据根 | 配置变更 |
| D3 watch-deals | 新品类 `config/watch-deals.yaml`+urlwatch 引擎小改 | 新增(近零代码) |
| D4 厂商行情 | 新链外引擎 `engines/vendor_market.py` + 新品类 `config/ai-vendor-daily.yaml` + daily-digest 分区 | 新增代码+配置 |
| D5 aihot 深挖+标签库 | `config/ai-news.yaml` 加两源+打标规则(20 公司/22 大V) | 配置变更(尾档可延,标签库 P1) |
| D6 一行富文本渲染 | `store_report.py`+daily-digest+wool 模板 | 渲染契约变更(独立小步) |
| D7 调度对齐+代理加固 | jobs.json 各品类 schedule+pipeline 客户端 trust_env | 行为+工程加固(独立小步) |

不动:push 通道层、dedup 核心、cron 底座、schema 主干(仅 D4 走既有的「链外引擎三处同步」惯例)。

## §2 D1 词表 v2(myssia-classifier)

> grill 第一轮修正(2026-10-24,事实全部实读 builtin.py/custom.py/pipeline.py):
> ①`filters` 键集被加载器钉死为恰 `{dead,noise,registration_lure}`(builtin.py:298)——**加 fake 是代码改动不是纯数据**;section 结构支持 keywords/patterns/case_insensitive(`吗$|呢$` 尾缀可落 patterns)✓。
> ②`adjudication` 数据节现状仅 `fallback_target`;免费分支裁决序**写死在 classify_title 代码**(builtin.py:399-421)——公益豁免/云服务器优先也是代码改动。
> ③影响面实证:`classify.builtin: true` 只有 ai-news+wool 两品类,词表收紧全局波及面=2。
> ④装机通道实证:keywords.json 经 `desktop/build-sidecar.sh:161` PyInstaller `--add-data` 冻结进 sidecar——升级=重建 sidecar 随正规发布流,无运行时 pip 通道。

### 数据面(keywords.json version 1→2)

- `categories[freebie]`:keywords/patterns 整体替换为生产 `WOOL_HARD_KW`(10-20 硬门槛)内容——keywords 兑换码/激活码/卡密/CDK/鸡蛋/盲盒/先到先得/免单/白嫖/随心蹬/0元/零元/领取,patterns 数量形态族(送领薅拿得抽赠补+数字、N天次张个枚GB条年月+免费、N元块刀token额度积分美金(?!起)、免费领/送/试用/骑/开/订阅/会员、教育公益版/公益站/公益/倍率0、免费{0,12}(GPT|Claude|…|大模型)、后台兑换)。原 FREE_KW 宽松词表退役(生产语义即如此)。
- `filters` 新增 `fake`(WOOL_FAKE_KW:听说/据说/关于抽奖红包/经验分享/踩坑记录/合集/盘点/资源大全/【推广/直降后叠加/N一个出/精品域名);description 记录生产「勿杀」判例(TG助力机器人/申请成功/自部署教程不算 fake——它们本来就不在表内,语义天然保留)。
- `filters.noise` 增补 10-03 五刀族:求助帖 keywords(报错/是什么/怎么办/怎么弄/求助/请教/有没有人/为什么/如何解决/怎么做/怎么样/需不需要/要不要/可不可以/能不能/有没有必要/是什么情况/啥情况/需要做些什么) + patterns(`吗$|呢$` 尾缀)+ 论坛活动族(广告位/开业/庆典/自动签到/签到报/抽奖.{0,8}(论坛|本站|广告位)/本论坛/本站)。

### 代码面(builtin.py,grill 修正:裁决序在代码不在数据)

- 加载器:filters 键集 `{dead,noise,registration_lure}` → `+fake`;ClassifyTable 增 fake_filter 字段。
- `classify_title` 流程改造(对齐生产 v3.1 cat_of):
  1. dead → noise → **fake(新,插在 noise 后)** → registration_lure&&!direct_give → drop(现状保留);
  2. free_hit(WOOL_HARD/direct_give)分支内新增:命中 `公益|倍率\s?0|0\s?倍率` → 羊毛(豁免付费);命中 `云服务器|云虚拟机|云主机|ECS|轻量服务器|VPS` 且非付费 → 羊毛(先于 token_context);再 token_context → token;再非付费 → 羊毛(现状序内插两级);
  3. no-free 分支:primary 循环**纳入 token**(生产 CAT_RULES 含 🔑token——apikey/额度 标题免免费信号可达 token;MYIA 现状「token 只能免费分支到达」与生产相悖,adjudication 描述同步改写);
  4. **付费/拉客帖整体砍(生产 10-03 五刀;10-24 主人已裁 Q1「砍」)**:paid_target(💰渠道)不再作归宿,paid_hit 或拉客词(中转/relay/逆向/号池/接入了/api站/聚合/车队/纳新/低价/优惠)→ None;fallback(ai-news)语义保留(=生产 🤖AI信息 兜底,wool 日报里 [AI信息] 条目的等价物)。
- 表内 description 保留生产各规则的日期出处(09-28/10-03/10-17/10-20),维持「AI/用户可直接增改」的数据自治形态(词面仍纯数据;裁决序属代码,docstring 注明)。

### 测试与发布面

- 金测集 `myssia-classifier/tests/classify_gold.json`:**存量用例逐条裁决(留/改/删)先行**——09-28 宽松 FREE_KW 语义用例中与新硬门槛冲突的,按生产 10-20 语义改判或删除,裁决记录进用例 description;再扩新语义用例(每条 ≥2 例,样本取生产实弹标题)。
- 主包侧 `tests/classify/` 同步;`tests/plugins/` 若 wool.yaml 删 drop 规则/渠道路由波及 golden,再生成有据。
- 版本 bump 0.0.6→0.0.7(uv workspace 联动;桌面侧经 build-sidecar.sh 冻结打包,随重建生效)。

### 波及与取舍

- 全局生效面=ai-news+wool 两品类;wool 收量下降是预期(主人 10-20 生产令,非回归;交付汇报说明)。
- `config/wool.yaml`:三条 drop 规则(10-19 试错版)与 builtin noise 五刀重叠→**删除**;push route 的 `channel` 分支随渠道砍退役→**删除**(10-24 主人已裁 Q1);保留「免费AI端点」「合成条目」两条非重叠规则。
- 回滚:revert keywords.json+builtin.py+金测集+版本号+wool.yaml;运行期无状态迁移。

## §3 D2 wool 源对齐(config/wool.yaml)

| 源 | 现状 | 目标 | 实施要点 |
|---|---|---|---|
| linuxsb | 首页 `/` | `/forum/2` 分类页 | **已实测(10-24)**:版块页=「福利放送」50 帖,`div.post-body`/`a.post-title` 选择器与首页同构(首页 52 帖健康无回归)——纯 URL 切换,落配置即跑 |
| cocoloop | `/latest` 混合流 | 福利专区 **HTML 页** `https://www.cocoloop.cn/c/welfare/19` | **已实测(10-24)**:SSR 直出 60 行 `topic-list-item`/`raw-topic-link`,既有选择器直用,GO;不走生产 .json 路(该站 robots 禁 `*.json`,HTML 页零冲突) |
| bbsbtsb | 10-17 判死移除 | 复活复测 | 测试矩阵:MYIA firecrawl 云端 × {bbs.bt.sb/latest, bt.sb/latest}(生产用 bbs 域活着;MYIA 当年测的是 301 后新域)。活→恢复源(选择器按实测定);死→证据回写 wool.yaml 注释,维持移除 |
| V2EX×3 | firecrawl 云渲染 | 默认不动 | 顺带实测官方 API 形态(api/topics/show.json,direct_api+json_path),顺利则换(免 credits),不顺维持;robots 面注意 v2ex api 路径豁免需记据 |
| ai-news 的 cocoloop 源 | ai-news.yaml 自带 /latest 讨论流源 | **删除**(10-24 主人已裁 Q2) | 图二第 6-15 条讨论帖混入 AI 资讯的根治=删此源(生产 AI 资讯无 cocoloop,只用 aihot+厂商官方源);daily-digest 分区一 sources/labels 清单同步删;五刀 noise 只能杀带求助词的,「哪个大模型最强」类无边缀讨论帖根治靠删源 |

- 方法论注记:单行压缩 HTML 用 `grep -c` 数出的是行数恒 1,判源健康必须 `grep -o … | wc -l`(10-24 实证踩坑)。
- 分区同步:cocoloop 源名不变(wool 侧);ai-news 侧删源则分区一清单同步删。
- 回滚:git revert 单文件。

## §4 D3 watch-deals(定向优惠,近零代码)

> grill 修正(10-24 实读):custom 规则 `when` 经 `Item.view()` 求值=view = metadata + url/title/source/category/scores/dedup_key(pipeline.py:501-514),**content 不在求值面**——DEAL_SPECIFIC_KW 直接挂 diff content 不可达。修法:urlwatch 引擎把 diff 摘要(added 行前 N≈200 字符)写进 `metadata.watch_diff_head`,量化规则经 metadata 判(view 含 metadata ✓)。此为引擎小改(+1 字段+文档+测试),D3 由「零新代码」修正为「近零代码」;备选「content 进 view」面大不取。

`config/watch-deals.yaml` 新品类,三源全用 `engine: urlwatch`(链外,registry 在册;契约与生产 watch_deals 语义逐条对上):

| 生产语义(watch_deals.py) | urlwatch 引擎承载 |
|---|---|
| 首跑建基线不推 | `announce_new: false`(纯建基线零条目) |
| 变动才产条目 | `changed` 事件→条目,diff 进 content |
| 抓取失败不动基线 | `error` 事件=源级结构化失败,cache 快照不更新 |
| 每站一条汇总(非逐行刷屏) | 单页监控天然一条;`selector` 收窄快照域(横幅/pricing 区)降噪 |
| DEAL_SPECIFIC_KW 量化门槛 | 品类 custom classify 规则:`when` 无量化信号 → drop(话术变更零产出) |
| TapNow 已知降级 | JS 壳:先 `render: crawl4ai` 试,不通则如实留档降级态(0 条=合法静默) |

- 源:runninghub(`https://www.runninghub.cn/`,selector 收窄横幅区)、hailuo(`https://hailuoai.video/pricing`,SSR 直抓)、tapnow(降级候选)。
- `DEAL_SPECIFIC_KW` 正则原文移植进 classify 规则;`when` 表达式访问字段面(content)实施时核实,不够则规则挂在 title+content 合并视图(item_view 判例)。
- push:路由进既有「AI 白嫖与优惠」出口(digest 档),daily-digest 分区四 sources 清单**加三个源名**(场景件注释铁律:新源名须同步)。
- cron:生产数据根挂 `myssia cron create --category config/watch-deals.yaml --schedule "30 6,18 * * *"`(在 wool 8/20 与 digest 8:05/20:05 之前留足变更窗口;缺省 deliver local,推送由品类 push 节承担)。
- 同厂商多档合并(生产 10-19 推送层美化)不移植,记档可翻案。

## §5 D4 厂商行情(链外引擎 vendor_market + 品类 + 分区)

### 引擎 `engines/vendor_market.py`(prompt/store_report 判例:链外、显式 engine 才生效、auto 永不路过)

- 输入 `engine_options.vendor_market`:`msrp`(型号→USD 表)、`fx`(USD_CNY 常量,缺省 7.25)、`bilibili`(mid/season_id/标题关键词)、`stock`(provider: yahoo|tencent,双源任一活即出价)、可选 `extra_zol_pages`。
- 抓取三路(全走引擎 HTTP 栈+礼貌面,prompt 引擎同款;proxy 支持源级 `pool:`):
  1. 股价:Yahoo chart(现有 stocks.yaml 同端点;主)→ 败则腾讯 `qt.gtimg.cn/q=usNVDA`(gbk 解码,生产同款解析;备)→ 双败=股价行标降级,**不废整块**;
  2. ZOL 国行价:**复用 firecrawl 云客户端**(gpu-prices 判例:ZOL 反爬门,静态直抓 152B 壳;云渲染真页)抓 `detail.zol.com.cn/vga/` + `vga/s11096/`(5090 系列页),`title=…price-type>N<` 正则抽价,型号归一(Pro6000D/5090D 变体映射);
  3. B站合集 API:`seasons_archives_list?mid&season_id`,取最新标题含「显卡日报」期(UA+Referer+buvid3 头,生产同款)。
- 计算:美价=MSRP 常量;`≈¥ = round(usd*fx)`;`diff%`→ 便宜/贵/持平(<3%)——纯确定性,零 LLM。
- 产出:**一条目**(run 一条),markdown 报告放 `metadata.vendor_report`(prompt_summary/report_markdown 同款合并判例),URL 锚 `<源url>#vendor-<YYYYMMDD>`(#prompt- 判例:每日新键、同日幂等);单路失败=该行降级标注,整条照出(生产 10-20 判例)。
- 注册三处同步:`schema.ENGINES`/`engines/registry.py`/SKILL+docs 枚举(store_report 批次4 惯例)。

### 品类 `config/ai-vendor-daily.yaml`

- 单源 engine: vendor_market;`classify.builtin: false`(报表条目无标题可筛,prompt 判例);`dedup.key: {url}`(锚点已铸日期);push 路由 archive(仅入库)——**发送由 daily-digest 承担**(ai-vendor-watch 退役件同款分工)。
- cron:生产数据根 `--schedule "0 7,19 * * *"`(AM 07:00 产→08:05 日报收;PM 19:00→20:05 收)。

### daily-digest 分区

- 「AI 厂商官网」分区(已静默)改造为「AI 厂商行情」:sources `[ai-vendor-daily]`、`style: detail`、max_lines 20;分区四 sources 增 watch-deals 三源名。

### 回滚

- 引擎+品类+分区三件独立 git revert;cron job `myssia cron remove`;无数据迁移(dedup 锚点自然过期)。

## §6 D5 aihot 深挖+标签库(ai-news 品类强化)

### aihot 三路合流

- `ai-news.yaml` 增 `aihot-daily`(/daily,双格式兼容——09-30 改版判例:旧编号格式+新 `### [标题](items链)+摘要+[原文](直链)` 格式都要解)、`aihot-hot`(/hot 48h 榜)两源;**X 原文直链进条目 metadata**(origins 字段,渲染时 x.com 直链优先于 aihot 转述页——X 直抓全死判例下的唯一路径)。
- **改版哨兵**:aihot 解析静默归零不报错(生产判例),实施时以条目数哨兵兜底(urlwatch 空态留痕/doctor 可见),巡检口径=看条目数。

### 公司/大V标签库(10-24 P2→P1 升格)

- 数据源:本地 `~/Project/Server/华为云/data-pending/migrate-data.tgz` 内 companies.json(20 公司:name/region/keywords)+influencers.json(22 人:name/role/region/keywords/min_score);
- 落地形态=**ai-news.yaml custom classify rules 生成**(脚本从两 JSON 生成 `when: "<任一 keyword> in title" → tag: "<name>·🇨🇳/🌍"` 规则块,固化进 YAML 单文件自包含,免新资源机制;x_accounts 字段弃用——无 X 抓取);
- 大V min_score 优先级排序与按公司分组渲染=后续可翻案项(需 digest 层排序机制,本轮不做);
- 排期:并 Step 5(同属 ai-news 品类配置面),AC12 验收。

## §8 D6 一行富文本渲染规范(主人 10-24 判例,独立小步)

### 现状缺陷(store_report.py 实证)

- `:308` `head = f"{head} [{LINK_LABEL}]({entry.url})"`——句尾追加 `[原文](url)` 尾注;
- `:306` `head = f"[{entry.label}] {head}"`——来源前缀方括号;
- docstring「布局纪律」段(行 30-33)写着「链接以 [原文](url) 附在句尾;labels 可带来源前缀」——**对生产版式的误读**:生产 `ai_daily_report.py:503` 实为 `f"{n}. [{t}]({e['url']})"`,链接挂标题本身,无原文尾注、无来源前缀。

### 目标契约

- 一句话条目:`N. [标题](url)`——渲染后 = 「N. 标题」单行富文本,标题整体可点;
- `LINK_LABEL` 常量与尾注拼接删除;`entry.label` 前缀渲染删除;
- `labels` 引擎选项退役:options 校验键表(§:395)删 `labels`,`daily-digest.yaml` 分区一删 16 行 labels 映射(唯一消费者);
- `suffix` 句尾附注(游戏价格)保留——是信息不是链接装饰;detail 明细行保留;
- 标题截断 `DEFAULT_TITLE_CHARS` 80→60 对齐产线一行纪律(可调,非硬门);
- docstring 布局纪律段改写,记 10-24 主人令出处。

### 测试面

- `tests/engines/test_store_report_engine.py` 版式快照逐行断言全部随新契约重生成;`tests/plugins/` 若钉 labels 行为同步;真发/dry-run 快照目验(AC9)。

### 回滚

- revert 引擎+daily-digest+测试三件;无数据面波及(渲染层纯函数)。

## §7 兼容性总表

- schema:新增 engine 名 `vendor_market`(枚举+registry+文档),无字段结构变更;
- 依赖:零新依赖(firecrawl 走既有 extras;腾讯接口纯 httpx);
- 凭据:firecrawl/飞书全走既有 keychain 引用,零明文;
- 数据:keywords.json version 2(加载器按 version 校验,旧表共存于历史版本);urlwatch cache 新增目标自建基线;
- 装机:Resources/config 增两件 yaml(补种幂等);classifier 0.0.7 经 build-sidecar.sh:161 PyInstaller --add-data 冻结打包,随 sidecar 重建生效(升级通道=正规发布流,无运行时 pip);装机态验证走 AC8。

## §9 D7 调度对齐+工程加固(10-24 技能深探新发现,独立小步)

### 调度对齐(生产真实节奏)

| 品类 | 现状 schedule | 目标(对齐生产 8:00/8:30/12:00 午间轮) |
|---|---|---|
| daily-digest | 5 8,20 | **5 8,12**(PM 槽=午间,图一图二均 12:01 产物=主人中午看报;可翻案) |
| wool | 0 8,20 | 0 8,**11**(第二跑前移,12:05 报窗有午前新条目) |
| watch-deals | (新增) | 30 6,**10**(五段 cron 异分钟须拆 job,统一取整) |
| ai-vendor-daily | (新增) | 0 7,**11**(同上取整) |
| ai-token-deals/games/stocks/TG 线 | 不动 | 不在本任务节奏面 |

- jobs.json 改走 `myssia cron update`/重建,AM 槽不动(8:05 报 vs 生产 8:30——MYIA 采集 8:00 起跑后 5 分钟即报,窗内条目少一档,可翻案对齐 8:30)。

### 环境代理污染防(生产 10-20 同型事故)

- 事实:`pipeline.py:1374` `httpx.AsyncClient(timeout=…)`(及 2185 注入点)无 `trust_env=False`——httpx 缺省读环境 HTTP_PROXY/HTTPS_PROXY,`proxy: direct` 在带代理 env 的宿主(cron sidecar/用户 shell)会被静默劫持,症状=直连可达源全 empty 不报错;vision/collect.py:366 注释已认知此 httpx 行为,主管线未防,全仓 trust_env 零命中。
- 修复:管线客户端构造处显式 `trust_env=False`(direct 语义=真直连);显式 proxy/pool 路径本就传 `proxy=`,不受影响;单测=monkeypatch 设 HTTP_PROXY 环境后 direct 源请求断言零代理挂载。
- 运维档:生产口诀「源批量 empty 先 curl 直连 vs 代理各测一次再动代码」记入 spec/spec 更新面。

### wool 速报模板类别 emoji(生产羊毛区块渲染定稿)

- 生产格式 `N. [类别emoji] [标题](链接)` 平铺;MYIA wool.yaml digest 模板 `- [title](url)` → `{{ item.category_label }}` 前缀(分类标签随 Q1 渠道砍后收敛);immediate 路线同款式。与 D6 同渲染纪律,并 Step 4.5 实施。

### 回滚

- 调度:cron update 还原;trust_env:revert 单点+测试;wool 模板:revert 单文件。
