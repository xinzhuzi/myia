# implement.md — 10-24-huawei-ai-news-absorb 执行计划

> 前置阅读:research.md(对账事实)→ prd.md(需求/AC)→ design.md(落点)。生产代码只读参照:`~/Project/Server/华为云/ai-news-bot/{wf_crawl,watch_deals,ai_daily_report}.py`。
> 每步门禁未过不进下一步;回滚点=该步开始前的 git 提交。

## Step 0 关停前抢救(前置,不阻塞码面)

> 10-24 技能深探后降级:本地 10-17 快照 `~/Project/Server/华为云/data-pending/migrate-data.tgz` 已含 companies/influencers 标签库+wooly_sent/daily_sent_items/deals_snapshot/push_target×4+RUNBOOK+停用线脚本——只需解包归档+云端增量补拉。

- [x] 0.1 解包 migrate-data.tgz 至 `~/Project/Server/华为云/ai-news-bot/cloud-snapshot-20261017/`(含密钥件 fc/push_target chmod 600,不进 git);RUNBOOK.md 归档研读
- [x] 0.2 SSH 探测(`server-华为云.sh`,密码动态读 华为云-服务器.md);通→增量补拉 10-17 后的 wooly_sent/daily_sent_items/deals_snapshot 三个注册表(丢增量最坏代价=个别条目重推一次,不阻塞)
- [x] 0.3 fc_cloud.json(firecrawl 云钥)核 MYIA keychain 是否已有等价(myia/firecrawl/*);无且 SSH 通→补拉 chmod 600
- [x] 0.4 deals_shown bug 告知主人(交付汇报项,关停前不修云端)

**验证**:解包目录清单在档;增量拉取结果或不阻塞说明;门禁=无。

## Step 1 词表 v2(myssia-classifier)— D1

> grill 修正:本步含**代码改动**(builtin.py 加载器键集+裁决序),非纯数据。

- [x] 1.0 存量金测用例逐条裁决先行:09-28 宽松语义用例与新硬门槛冲突的按生产 10-20 语义改判/删,裁决记进用例 description(留档可追溯)
- [x] 1.1 金测集扩新语义用例(硬门槛放行/拦截、fake 否决、五刀求助尾缀 `吗$|呢$`、公益豁免付费、云服务器优先于 token、token 免免费可达、付费/拉客砍、fallback AI信息兜底;样本取 research.md §2 案发标题,每语义 ≥2 例)
- [x] 1.2 跑金测集确认新用例全红(先钉预期)
- [x] 1.3 `keywords.json` v2(freebie 换 WOOL_HARD、filters.noise 增五刀族) + `builtin.py` 代码面(filters 键集+ClassifyTable 增 fake;classify_title 插 fake 否决/公益豁免/云服务器优先;primary 循环纳入 token;paid_target 渠道砍→None;adjudication 描述改写)——裁决序改动已裁(10-24 主人 Q1「砍」)
- [x] 1.4 金测集全绿;`uv run --no-sync python -m pytest myssia-classifier/tests -q` 零红
- [x] 1.5 主包联动:`config/wool.yaml` 删三条重叠 drop 规则+push route 的 channel 分支(留 免费AI端点/合成条目;Q1 已裁);`config/ai-news.yaml` 删 cocoloop 讨论流源(Q2 已裁)+daily-digest 分区一清单同步;主包 `tests/classify/`、`tests/plugins/` 跑全量,golden 波及再生成并 diff 核
- [x] 1.6 版本 bump 0.0.6→0.0.7(pyproject 三方一致);`uv sync --all-extras` 后 dist-info 复核

**验证**:`uv run --no-sync python -m pytest -q` 全量;`uvx ruff check`;金测集新增/改判用例计数记档。
**回滚点**:revert keywords.json+builtin.py+金测集+版本+两 yaml。

## Step 2 wool 源对齐 — D2

> grill 修正(10-24 实测):cocoloop 福利专区 HTML(SSR 60 行)/linuxsb /forum/2(50 帖,选择器同构)均已验活——2.1/2.2 从「实测验证」降为「落配置即跑」,首跑核对条数即可。

- [x] 2.1 cocoloop 福利专区:wool.yaml 改 url `https://www.cocoloop.cn/c/welfare/19`+注释(实测记录+避 .json 路 robots 理由);首跑核 >0 条福利帖
- [x] 2.2 linuxsb:wool.yaml 改 url `https://linux.sb/forum/2`(选择器已验同构);首跑核 >0 条
- [x] 2.3 btsb 复活复测:MYIA firecrawl 云端 × {bbs.bt.sb/latest, bt.sb/latest};活→恢复源(选择器实测定)+注释翻案记录;死→证据(状态码/页面形态)回写注释维持移除
- [x] 2.4 V2EX API 形态实测(direct_api+json_path);顺利→换三源(免 credits),不顺→维持 firecrawl 记档
- [x] 2.5 真跑验证:`MYIA_HOME=<沙箱> uv run --no-sync myssia run config/wool.yaml --json` 各源计数核对(讨论帖混入应显著下降)

**验证**:单品类 run --json 各源 items 计数;tests/plugins golden 波及处理。
**回滚点**:revert config/wool.yaml。

## Step 3 watch-deals 新品类 — D3

> grill 修正:先做 urlwatch 引擎小改(diff 摘要进 metadata),再落品类。

- [x] 3.0 urlwatch 引擎:changed 条目 `metadata.watch_diff_head` = added 行摘要(前 ~200 字符,截断留痕);docstring+引擎测试同步
- [x] 3.1 `config/watch-deals.yaml`:三源 urlwatch(runninghub selector 收窄/hailuo 直抓/tapnow render: crawl4ai 试,不通记降级);`announce_new: false`;DEAL_SPECIFIC_KW 移植为 classify drop 规则(挂 `watch_diff_head` 经 metadata 求值,Item.view 含 metadata 实证在案)
- [x] 3.2 单测:DEAL_SPECIFIC_KW 话术 0 条/量化放行(正则单测+品类装载测试+watch_diff_head 求值链路测试,镜像 `tests/plugins/` 归组)
- [x] 3.3 daily-digest 分区四 sources 加 watch-deals 三源名
- [x] 3.4 沙箱首跑:建基线零条目(`last_skip_reason=watch_unchanged`/new-baseline 留痕);二次跑幂等
- [x] 3.5 真跑:RunningHub+海螺真入库(首跑基线后无推送=正确);cron 挂点统一归 Step 4.6(避免挂后即改)

**验证**:run --json 两次对比;cron jobs.json 新 job 在册;`uv run --no-sync python -m pytest -q` 全量。
**回滚点**:删品类文件+cron remove+revert daily-digest。

## Step 4 厂商行情 — D4

- [x] 4.1 引擎 `src/myssia/engines/vendor_market.py`(design §5 契约:三路抓取+确定性计算+单条目 metadata.vendor_report+#vendor-<date> 锚;单路失败降级不废块);注册三处同步(schema.ENGINES/registry/SKILL+docs zh/en)
- [x] 4.2 单测 `tests/engines/test_vendor_market_engine.py`(mock 三路:全活/股价死/ZOL 死/B站死四形态,锚点幂等,计算行含 便宜/贵/持平 分支)
- [x] 4.3 品类 `config/ai-vendor-daily.yaml`(classify builtin:false;push archive;cron 挂点统一归 Step 4.6)
- [x] 4.4 daily-digest「AI 厂商官网」分区改造为「AI 厂商行情」(sources/style/max_lines);分区测试快照更新
- [x] 4.5 真跑:产出含股价+GPU 比价行+视频行条目(或降级标注);`MYIA_HOME=<沙箱> myssia run config/ai-vendor-daily.yaml --json` 验锚点同日幂等

**验证**:引擎单测+全量 pytest;真跑 --json 报告行抽查(比价行数值合理性人工核)。
**回滚点**:revert 引擎+品类+分区三件,cron remove。

## Step 4.5 一行富文本渲染规范 — D6(独立小步,可先行)

- [x] 4.5.1 `src/myssia/engines/store_report.py`:渲染块改 `N. [标题](url)`(链接挂标题);删 `LINK_LABEL` 尾注拼接与 `entry.label` 前缀渲染;docstring 布局纪律段改写(记 10-24 主人令「要一行富文本,不加 [] 原文等额外内容」,纠正 10-06 对产线的误读);`DEFAULT_TITLE_CHARS` 80→60
- [x] 4.5.2 options 校验键表删 `labels`;`config/daily-digest.yaml` 分区一删 16 行 labels 映射
- [x] 4.5.3 `tests/engines/test_store_report_engine.py` 版式快照按新契约重生成;`tests/plugins/` labels 相关同步
- [x] 4.5.4 目验:dry-run 快照或沙箱真发,逐行核零「原文」/零方括号前缀/单行可点(AC9)
- [x] 4.5.5 wool.yaml 速报模板加类别 emoji 前缀(生产羊毛区块定稿 `N. [类别emoji] 标题` 形态,digest/immediate 两档同改;渠道砍后类别集合收敛)

**验证**:`uv run --no-sync python -m pytest tests/engines/test_store_report_engine.py tests/plugins -q` + 全量;目验截图。
**回滚点**:revert 引擎+daily-digest+测试三件。

## Step 4.6 调度对齐+代理加固 — D7(独立小步)

- [x] 4.6.1 管线客户端 `trust_env=False`(pipeline.py:1374/2185 两构造点;direct=真直连语义);单测=monkeypatch HTTP_PROXY 环境下 direct 源零代理挂载(AC11)
- [x] 4.6.2 调度对齐(R8):daily-digest `5 8,20`→`5 8,12`;wool `0 8,20`→`0 8,11`;watch-deals `30 6,18`→`30 6,10`;ai-vendor-daily `0 7,19`→`0 7,11`(五段 cron 单表达式双时刻同分钟,异分钟须拆 job,此处统一取整);jobs.json 经 cron update/重建,AM 槽不动(可翻案 8:05→8:30 对齐)
- [x] 4.6.3 生产口诀「源批量 empty 先 curl 直连 vs 代理各测一次」记入 spec 运维面(随 6.4 spec 更新一并)

**验证**:`myssia cron list` schedule 与 design §9 表一致;trust_env 单测绿;全量 pytest。
**回滚点**:cron update 还原 + revert 客户端单点。

## Step 5 aihot 深挖+标签库(ai-news 品类强化)— D5

- [x] 5.1 `ai-news.yaml` 加 aihot-daily(双格式兼容)/aihot-hot 两源;X 直链进条目 metadata,渲染时优先(design §6)
- [x] 5.2 真跑两源 >0 条+条目数哨兵(改版静默归零防御);标题去重与既有 aihot 源冲突核(url 键分流验证)
- [x] 5.3 标签库迁入:从 cloud-snapshot-20261017/{companies,influencers}.json 生成 ai-news custom rules(20 公司+22 大V,命中打 `<name>·🇨🇳/🌍` tag;生成脚本一次性,产物固化进 YAML;AC12 真跑抽验 ≥3 条带 tag)

**验证**:单品类 run --json;全量 pytest。

## Step 6 收尾交付

- [x] 6.1 全量门禁:`uv run --no-sync python -m pytest -q` 零新红 + `uvx ruff check` + 触及 golden 再生成 diff 核
- [x] 6.2 AC7 关停就绪对照表:MYIA 承载面 vs 华为云三件套逐能力「已承载/已对齐/如实弃用(列明)」——落本档尾或交付汇报
- [x] 6.3 装机:classifier 0.0.7+两新品类随包;打包刷新+装机换装;装机态真跑一轮 daily-digest 含新分区(截图+OCR 像素证据,AC8)
- [x] 6.4 spec 更新(python/index.md 增 vendor_market 判例行;classify 节记词表 v2 出处)+ 交付汇报(首段:华为云线可否关停;wool 收量下降预期说明;deals_shown bug 已告知)

## 依赖图

```
Step0(独立,随时;抢救已降级=解包+增量)
Step1(词表)────┐
Step2(wool源)───┤
Step3(watch)────┼─→ Step6 收尾
Step4(厂商)─────┤      (Step5 标签库 P1;aihot 部分可延后/独立)
Step4.5(渲染)───┤
Step4.6(调度+加固)┘
```

Step1-4.6 相互独立可并行/分批合入;每步独立回滚。
