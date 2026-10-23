# 情报采集线收编定案(2026-10-24,task 10-24-huawei-ai-news-absorb)

华为云 ai-news-bot(生产参照件 `~/Project/Server/华为云/ai-news-bot/`,只读)能力收编进 MYIA 后的硬约定。对账底稿与生产代码行号见任务档 research.md。

## classifier 词表(0.0.7 起)

- `myssia-classifier/myssia_classifier/data/keywords.json` version 2:**词面是数据、裁决序是代码**——升词表=keywords.json+builtin.py 双改,金测集(78 条)是语义唯一权威,先写用例先红再改。
- 裁决序(free 分支):公益/倍率0 豁免付费→云服务器语境且非付费→token_context→羊毛;no-free 走主循环(**含 token**,免免费可达)→付费/拉客词(五刀)整体 `None`,💰渠道退役为历史标签(CATEGORY_CHANNEL 保留不再赋值)。
- filters 四键 `{dead, noise, fake, registration_lure}`(加载器钉死键集);与生产 v3.1 的 4 条有意分歧(付费砍先于 AI信息兜底)在 fixture description 逐条留档,可翻案。
- 品类想再收紧(如促销帖)走品类级 custom drop 规则,机制保留(wool_quality_gate 测试钉住),不动 builtin。

## 引擎面

- `vendor_market` 链外引擎(prompt/store_report 判例):股价 Yahoo 主/腾讯 gbk 备、ZOL 走 firecrawl 云客户端、B站合集 API;MSRP 表+汇率常量进 engine_options;`#vendor-<date>` 锚同日幂等;**单路失败降级不废块**(生产 10-20 判例)。
- urlwatch 引擎 changed 条目铸 `metadata.watch_diff_head`(added 行摘要)——custom 规则 `when` 求值面=Item.view(metadata+固定字段),**不含 content**;要消费 diff 内容走 metadata(白名单 `match()` 规则形态,classifier 0.0.7 起)。

## 渲染纪律(主人 2026-10-24 令)

- store_report 条目=「N. [标题](url)」**链接挂标题**,禁原文尾注/来源前缀(labels 机制已退役,options 键表已删);标题截断 60;wool 速报=编号+类别emoji 前缀(生产羊毛区块定稿)。

## 直连语义与运维

- 管线自建 httpx client 一律 `trust_env=False`(`proxy: direct`=真直连)——环境 HTTP(S)_PROXY 会静默劫持 direct 源成全源 empty 不报错(生产 10-20 同型事故;vision 线判例推广到主管线);出网代理走显式 `pools`。
- 调度(PM 槽=午间,对齐生产 8:00/8:30/12:00 节奏):daily-digest `5 8,12`/wool `0 8,11`/watch-deals `30 6,10`/ai-vendor-daily `0 7,11`(五段 cron 异分钟双时刻须拆 job,统一取整)。
- 排查口诀:源批量 empty 先 curl 直连 vs 代理各测一次再动代码;aihot 改版→解析静默归零,巡检=看条目数(哨兵=健康度 degraded)。
- 真跑纪律:`myssia run` 的 `--db` 缺省是 **cwd 相对**(cli.py:457),沙箱验证必须显式 `--db` 或 MYIA_HOME+cron 组;urlwatch adapter 缓存硬编码 `~/.myia`(MYIA_HOME 不隔离,待修小步)。
- 不可达判例(勿再试):linux.do(CF Turnstile+禁爬)/nodeseek/e7ai/naixi/btsb(SafeLine WAF,firecrawl 云端双域复测 10-24);X 直抓全路线死亡,X 信息唯一路径=aihot /daily 原文直链。
