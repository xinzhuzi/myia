# trafilatura extract 面增强评估定案(2026-10-05,planning 期收口)

> 证据口径:代码引用 = 本会话行级亲读(路径:行号);运行证据 = /tmp/traf-eval venv
> (trafilatura 2.3.0)离线夹具真跑,原始输出与脚本在 `evidence/`(零外网零 robots 负担)。
> 红线自查:本任务 planning 期零核心文件改动,产出仅本档目录内文件。

## 结论速览

- **共存边界(AC1)**:三分触发(规则缺失→兜底/规则跑空→质量门后兜底/字段级失败→不兜底);
  输出契约 = `{url, title, content[, published, author]}` 全部对齐 items schema 既有键**零新键**;
  provenance = 兜底条目 `metadata["extract_provenance"]="trafilatura"`,手写规则路径**零新键零改动**。
- **挂点档位(AC2)**:定案 = **static_html 引擎内回退**(extract 缺失/跑空时),enrich 平行否决
  (架构性理由:后段无钩子可挂+绕过引擎层礼貌设施,见 §3.2)。启发式噪声靠「触达面天然窄 +
  产出质量后验门」约束,不靠 pagetype(实证无判别力)。
- **定位红线**:兜底非首选,永不全量接管;「手写规则路径零回归」是 AC3 硬门(守军清单 §5)。

## 1. 地基:引擎链现状实读(行号级)

### 1.1 L2 static_html 的 extract 实现

- 提取出口分流 `src/myssia/engines/static_html.py:104-115`:`_fetch_page` 抓页→解码→变更指纹
  →按 `extract.type` 分流(rss→`extract_rss`,其余→`extract_html`)。
- **零条语义** `static_html.py:113-115`:`if not page_items: return [], None, True`——规则跑出
  空=该页零条+提前收尾,不报错、不记 failure(改版失效的现状=静默零产出,源级健康靠零结果暴露)。
- **extract 缺失现状** `src/myssia/engines/fetch_base.py:2195-2202`:`_check_extract_support` 对
  `extract=None` 且 `REQUIRES_EXTRACT=True`(static_html 即是)抛 `FetchError(error_type="extract_required")`,
  消息原文「static_html 引擎需要配置 extract 节(v0.1 不做自动结构化)」。本会话在 /tmp/traf-eval
  直调 `_check_extract_support` 复现(evidence/judge-output.txt):`raise FetchError: error_type=extract_required`。
- **字段级失败语义** `fetch_base.py:1814-1842`:`extract_html` 逐字段 `_field_value`,miss 的字段
  整条省略(1828/1838 的 None 过滤);`list` 型零字段命中的条目被 skip(1840-1841),整页零命中
  = 空列表。即「改版后字段级失败」最终衰减为「整页跑空」(②)或「条目缺 url→invalid_item」
  (`src/myssia/pipeline.py:1516-1528` 的条目级失败记账)。

### 1.2 降级链 / engine_hints / 失败记账(registry)

- 链序 `src/myssia/engines/registry.py:79-87`:`direct_api → static_html → crawl4ai → firecrawl
  → scrapling → stealth_browser → llm_browser`;hint-first(`registry.py:248-251`)。
- **零条也回写 hint** `registry.py:338-343`:引擎跑成功(含零条非 skip)→ `set_engine_hint(engine_name)`
  并 return;即改版失效源零条后 hint 仍是 static_html,下一轮 hint 命中照旧零条,**不误报也不自愈**。
- **L3 零结果探测** `registry.py:307-337`:auto 链上 static_html **真零结果**(非指纹 skip)且无
  hint 且预算有余的首遇源,继续走 crawl4ai 探测一次(30s 短帽);探测零条/异常回滚零结果快照
  (`_rollback_to_zero_fallback`,`registry.py:199-220`)。**触发信号 = static_html 零条**——这是
  挂点定案的关键交互面(§3.1)。
- 失败记账:每次引擎尝试异常 → `EngineFailure(source/engine/url/error_type/message)`
  (`registry.py:265-278`),error_type 面 = `classify_exception`(`fetch_base.py:297-311`,
  FetchError 走 `exc.error_type`,如 `parse`/`extract_required`/`dependency_missing` 族)。
- 管线侧另有「降级注记(自动恢复,不翻 run 状态)」通道(`src/myssia/pipeline.py:334` 附近
  field 注释,enrich 条目级失败先例)——兜底触发的软信号可挂此通道,不翻 run 状态。

### 1.3 items 消费面(输出契约的对齐基准)

- `Item.from_extracted`(`src/myssia/pipeline.py:448-477`):**管线已知键 = url/title/source/content**;
  其余字段全进 `metadata`;缺 url → `ValueError` → `invalid_item` 条目级失败记账(1516-1528)。
- `content` 键已在线:docstring「正文摘录(L3 无 extract 的 markdown / extract 显式映射的 content
  字段):LLM 精评的 credibility 维度依赖它」(`pipeline.py:443-445`);分析 lane 消费
  `{"url", text: title+content}`(`pipeline.py:1999`)。
- **L3 auto-structure 先例**(兜底输出契约的同构样板)`src/myssia/engines/crawl4ai.py:381-391`:
  crawl4ai 无 extract 时产出单条 `{url: 请求页 URL, title: metadata title, content: markdown}`
  (+可选 `images` 进 metadata)——trafilatura 兜底照此形态对齐,管线零新语义。

### 1.4 品类 YAML 手写规则实貌(亲读样例)

- `plugins/ai-news.yaml:33-43`:`type: list`,`item: "article[data-item-id]"`,fields
  title/url/image(CSS+@attr);`plugins/ai-news.yaml:67-72` Discourse `tr.topic-list-item`。
- `plugins/wool.yaml:34-39/56-62`:list 型,`a.min-w-0[href^="/posts/"]` 等选择器,url 取 `@href`。
- `plugins/news.yaml:32-37`:`type: rss`,fields 值=feedparser entry 属性(title/link/published)。
- `plugins/monitor.yaml:34-39`:`type: json_path`(`$[*].label` 等,JSON API 面)。
- 实貌结论:手写规则=**列表页条目形态为主**(item 卡片→title/url),单文章正文抽取(item 型)
  罕见——trafilatura 的「单页→正文」产出与列表规则**形态错位**,这是兜底只能做「单页一条」
  而非「替列表规则产条」的结构性依据。

## 2. AC1 共存边界定案

### 2.1 触发条件(三分)

| # | 触发条件 | 现状行为 | 定案 | 依据 |
|---|---|---|---|---|
| ① | **规则缺失**(`extract=None`,engine 为 static_html/auto) | `extract_required` 拒载→链降 L3+(烧浏览器/付费)或全链失败 | **兜底主路**:trafilatura 抽单页正文,过质量门才出条 | 「无规则长尾源」盲区正路;L2 成本拿到 L3 才有的结构化 |
| ② | **规则跑空**(extract 在,整页 0 条:改版选择器零命中) | 零条 return+hint 回写(§1.2);首遇源或触发 L3 探测 | **质量门后兜底**:兜底产出过门→出条+provenance+降级注记;不过门→维持零条语义 | 「改版失效兜底」盲区;零条信号不吞(§3.1 交互推演) |
| ③ | **字段级失败**(条目缺 url→invalid_item;或部分字段 miss) | 条目级失败记账,其余条目照常 | **不兜底** | 条目级失败=配置质量问题;trafilatura 单页一条形态无法重造列表条目 url;整页性衰减压到② |

不触达面(负向边界):`json_path` 源(direct_api/saas,`direct_api.py:50`/`saas.py:271-274`)
是 JSON API,无 HTML 可抽,**兜底永不挂**;`rss` 源走 feedparser 白名单路径,不挂;规则命中的源
trafilatura **永不触达**(结构性「兜底非首选」保证,见 §3.3)。

### 2.2 输出契约(零新键)

兜底产出 = **单页一条**:

```
{url: <请求页 URL>, title: <trafilatura title,可退化>, content: <正文纯文本>,
 [published: <date 字符串>], [author: <作者>], + metadata.extract_provenance="trafilatura"}
```

- 键面全部是 items schema/管线既有键:`url/title/content` = `Item.from_extracted` 已知键
  (`pipeline.py:465`);`content` 先例 = L3 auto-structure 同款(`crawl4ai.py:383-386`);
  `published`/`author` = rss 字段白名单与 news.yaml 既有字段名(`schema.py:602`、`news.yaml:37`)。
- **不新造任何键**(新键=schema 改动,超评估期);trafilatura JSON 面其余键
  (description/sitename/categories/tags/fingerprint/hostname/pagetype/…)不映射、丢弃
  (键面实证 evidence/matrix-output.json 各 note 字段)。
- title 质量注记(如实记):文章页 A2 实证 title 拿成站名「EXAMPLE 新闻网」而非文章题(正文
  text 首行携带真标题);兜底 title 取 trafilatura title 即可,title 空/站名由 classify/push 既有
  容错消化;是否用 text 首行修补留实现期,评估期不定。

### 2.3 provenance 标注

- **兜底条目**:`metadata["extract_provenance"] = "trafilatura"`——单值观测标记,doctor/日志/排障
  可区分「规则产出」与「启发式产出」;下游(dedup/classify/push/分析 lane)不消费此键。
- **手写规则路径零新键零改动**:不给规则产出加 `provenance="rules"` 之类——加了就改变既有 items
  形态,守军测试面的既有断言(golden/协议测试)会被打爆,违背零回归红线。
- API 钉版:`trafilatura.extract(output_format="json", with_metadata=True)` 返回 JSON 串(稳定面);
  `bare_extraction` 在 2.3.0 返回 `Document` 对象非 dict(v1 脚本实测 AttributeError,见
  evidence/matrix-script.py docstring),实现期不用。

### 2.4 逐源行为矩阵(三列;现状 vs 加 trafilatura 后)

离线夹具真跑,原始输出 `evidence/matrix-output.json`(脚本 `evidence/matrix-script.py`,
trafilatura 2.3.0):

| 源形态 \ 路径 | 现状(手写规则) | 加 trafilatura 后(定案挂点=引擎内回退) |
|---|---|---|
| **有规则源**(列表页 B1/文章页 A1) | B1:3 条结构化条目(title/url/image,字段精确);A1:item 规则精确命中 title+content | **不变**:规则命中→trafilatura 永不触达(兜底只在①②触发) |
| **无规则源**(extract=None) | `extract_required` 拒载→链降 L3+(烧浏览器/付费)或全链失败(evidence/judge-output.txt 实证) | 文章页 A2:**单条 {url,title,content 203 字符}**,导航/广告/页脚剥除干净(text 无「广告:全场五折」无「© 2026」无 nav 链接),date 正确;列表页 B2:退化伪文章(78 字符=导航+标题拼接)→**被质量门拦住不出条**(§3.3) |
| **改版失效源**(规则在,零命中 C1) | 整页 0 条静默失效,零条 return+hint 回写;首遇或触发 L3 探测 | 改版**文章页** C2:正文仍在,兜底可救(203 字符+provenance+降级注记);改版**列表页** C3:退化(51 字符导航+标题)→质量门拦住,维持零条语义 |

矩阵行为学要点(取证原文见 matrix-output.json):文章页 203 字符 vs 列表/改版列表页 51-78 字符,
正文长度分离度好——支撑「产出质量后验门」设计;纯导航页 text_chars=6 也未被 trafilatura 自身
拒(evidence/judge-output.txt D 行),**trafilatura 自判阈值过宽,质量门必须自己设**。

## 3. AC2 挂点档位定案

### 3.1 定案:static_html 引擎内回退;交互面逐项

**定案 = 回退挂点(static_html 引擎内,extract 缺失①/跑空②时)**。与三大交互面的推演:

- **降级链**:兜底成功=static_html 出条,链停在 L2(比 L3 烧浏览器/付费 SaaS 便宜一个量级);
  兜底失败(trafilatura 返 None 或质量门不过)=**维持零条语义**——auto 链的 L3 探测触发信号
  (static_html 真零结果)保真:JS 渲染空壳页兜底同样拿不到正文(空壳 HTML 无可抽),零条照旧,
  探测照常。触发面唯一被吃掉的情形=「服务端渲染且正文仍在的改版源」——那正是兜底产出正确的
  情形,比探测后烧 crawl4ai 更优。
- **engine_hints**:兜底成功→hint 回写 static_html——与现状零条也回写 static_html
  (`registry.py:338-343`)语义同级不变差;胜者语义的受染(「引擎赢了但产出是启发式」)由
  provenance 标注+doctor 可见消解。兜底失败→零条,现行为原样。
- **失败记账**:①触发=现状本就 raise extract_required(FetchError 记账后降级),改走兜底后该
  失败消失,**换来的是出条**(正向);②触发=新增「降级注记」(自动恢复不翻 run 状态,
  `pipeline.py:334` 既有通道先例),`rules_empty` 信号不丢,doctor 仍见「该源规则已烂」。

### 3.2 enrich 平行的否决理由(反对面如实记)

1. **后段无钩子可挂**:enrich 语义=LLM 精评+事件聚合(token 成本,输入是 items 不是页面,
   `src/myssia/enrich/` 全模块无追抓面);fetch 零条的源在 classify/dedup/analyze 拿不到任何
   items,「平行」挂点无米下锅——要先重抓页面,而那是 fetch 层的事。
2. **绕过引擎层礼貌设施**:后段自建重抓=绕开 `BaseEngine.request` 的 robots/限速/304 协商/重试
   单点(`fetch_base.py:2236-2256`),违反 spec 纪律「throttling lives once in the engine layer」
   (`.trellis/spec/python/index.md` 技术底座节)。
3. **「不动链」优势不成立**:research 第六波列 enrich 平行的本意是保守替代;实读后,后段挂点
   需要的改动(传源 URL+重抓+条目合成+独立礼貌层)比引擎内一个分流分支更大。

引擎内回退自身的受染风险(反对面,如实记):①`extract_required` 从「拒」变「兜底」松动
「v0.1 不做自动结构化」语义(`fetch_base.py:2201` 原话)——实现期须以 **opt-in 开关**(全局或
源级,缺省关)落地,保既有源零行为差;②hint 胜者语义受染(provenance 消解,§3.1);
③兜底分支进 `_fetch_page` 出口,与 rss 分流(`static_html.py:104-115`)同构,新分支须有独立
测试(mock trafilatura),不动既有断言。

### 3.3 启发式噪声的天然约束(挂点如何约束)

1. **触达面天然窄**:兜底只在「规则缺失①/规则跑空②」的 static_html 源触达;规则命中的源
   trafilatura 永不进(B1 矩阵行)——「兜底非首选,永不全量接管」的结构性保证,不依赖运维自觉。
2. **产出质量后验门**(设计记档留实现):兜底产出必须过最低正文量门(text 长度阈值;夹具实证
   文章 203 vs 列表退化 51-78,分离度好;阈值缺省值与标定留实现期),不过门=视同启发式失败=
   维持零条语义,不产伪条目。**pagetype 判据不可用**:四夹具恒 None(evidence/judge-output.txt),
   页面前验(og:type/结构化数据)覆盖面不足,弃用。
3. **形态错位兜底**:列表页源即使进了兜底,产出=单条伪文章(B2/C3 形态),质量门是主约束;
   实现期可再收紧「缺省仅 item 型/extract=None 源生效」为可选项(记档,不定案)。

## 4. 依赖面(R2)

- **extras 路径**:trafilatura 进 `[project.optional-dependencies]`(组名留实现期,先例
  vision/crawl4ai),**不进核心 dependencies**——核心 6 依赖红线不动
  (`.trellis/spec/python/index.md:6`);引擎内惰性 import,`ImportError` → 结构化报错+安装命令
  提示,`dependency_missing` 族记账不拦链——「装不上不拦核心铁律」:手写规则路径照常,兜底
  能力结构化降级(prd Constraints 原文)。
- **共存实证**(`evidence/coexist-proof.txt`):`uv venv /tmp/traf-eval && uv pip install
  --python /tmp/traf-eval -e . 'selectolax<1' trafilatura` → 同 venv 内 trafilatura 2.3.0 +
  selectolax 0.4.13 + lxml 6.1.3 + myssia(含 engines/registry)import 全绿;**装了 trafilatura
  的环境里手写规则路径真跑产出正确**(`extract_html` → `{'title': 'T1', 'url': '.../x'}`)。
- **`'selectolax<1'` 钉版不可省**(边界条件,如实记):自由解析装 selectolax 1.0.0 撞 Modest
  解析器移除墙(评审亲测+计划员复验);trafilatura 对 selectolax 无硬依赖(走 lxml 路径),
  但 MYIA 自己的 extract_html 面钉 <1。lxml 6.1.3 等传递依赖与核心 6 依赖零冲突(同 venv 实证);
  若未来上游钉版冲突,按「装不上不拦核心」记边界不拦链。

## 5. 守军清单(AC3 硬门勾选依据:「手写规则路径零回归」)

**处理域文件面**(json_path/extract 消费集,本次评估行号级定位毕;实现期动其中任何一件前先跑
`gitnexus impact -r shishi <symbol>` 报爆炸半径——AGENTS.md 纪律):

1. `src/myssia/engines/fetch_base.py`:`extract_html`(1814-1842)/`extract_rss`(1845-1874)/
   `_field_value`(1792-1811)/`_check_extract_support`(2195-2209)/`ExtractionError`(290-293)
2. `src/myssia/engines/static_html.py`:`_fetch_page` 出口分流(104-117)
3. `src/myssia/engines/direct_api.py`:json_path 消费(50/95)
4. `src/myssia/engines/saas.py`:json_path 消费(256-285)
5. `src/myssia/schema.py`:`ExtractConfig`(605-715)/`RSS_ENTRY_FIELDS`(602)/`EXTRACT_TYPES`(168)
6. `src/myssia/pipeline.py`:`Item.from_extracted`(448-477)/`invalid_item` 记账(1516-1528)
7. `src/myssia/engines/registry.py`:零条/L3 探测/hint 回写(307-351)

**守军测试面**(零回归判据=下列测试全绿+新增兜底测试只测新分支不动既有断言;存在性本会话
`ls` 核验):

- `tests/engines/test_static_html.py`(L2 分流/翻页/零条)
- `tests/engines/test_fetch_base.py`(extract_html/_field_value/错误分类)
- `tests/engines/test_registry.py`(降级链/hint/L3 探测回滚)
- `tests/engines/test_direct_api.py` / `tests/engines/test_saas_gated_engines.py`(json_path 面)
- `tests/pipeline/test_pipeline.py` / `tests/pipeline/test_baseline.py` /
  `tests/pipeline/test_analysis_lane.py`(items 消费/content 列/分析 lane)
- `tests/test_schema.py`(golden:schema 契约面)

## 6. 验收口径(R3,定案)

- **硬门**:手写规则路径零回归(§5 守军清单测试面全绿)。
- **trafilatura 路径=可用性验收**:「无规则源拿到可用正文」为判据(A2/C2 形态:正文完整、
  导航/广告/页脚剥除);启发式噪声(B2/C3 列表页退化)**如实记档不设硬性质量门**——质量门
  只裁「出不出条」(零条保真),不给启发式产出打质量分。
- 红线原文重申:定位「兜底非首选,永不全量接管」(prd Constraints)。

## 7. 留实现期的设计要点(R4 改动清单+爆炸半径说明)

定案**动引擎链**(static_html 分流+extras 声明),实现期改动清单:

1. `pyproject.toml`:`[project.optional-dependencies]` 增 trafilatura 组(命名待定)。
2. `src/myssia/engines/fetch_base.py` 或 `static_html.py`:兜底函数(惰性 import;
   `extract(output_format="json")` → items 映射(§2.2 契约);质量门;opt-in 开关读入)。
3. `src/myssia/engines/static_html.py`:`_fetch_page` 兜底分流(①②两分支;③不进);
   `extract=None` 的触达须处理 `_check_extract_support` 的 `REQUIRES_EXTRACT` 面
   (覆写或分流前移,实现期定)。
4. 失败记账/降级注记:②触发的软信号挂管线降级注记通道。
5. 测试:`tests/engines/test_static_html.py` 增兜底分支用例(mock trafilatura 注入 sys.modules,
   同 rapid_table/rapidocr mock 先例);缺 extras 的 skip 守卫(同 TestRealEngineFixture 纪律)。

爆炸半径:受影响执行流 = fetch 链上 static_html 源的 `extract=None`/跑空两分支;既有规则命中源
零行为差(opt-in 缺省关);registry/schema 层**零改动是目标**(兜底在引擎内消化,不动链序/不动
ExtractConfig)。实现期首步跑 `gitnexus impact -r shishi _fetch_page` 与 `extract_html` 核验。

## 8. 证据索引

- `evidence/coexist-proof.txt` — 依赖共存实证(命令+装包面+双向真跑输出)
- `evidence/matrix-output.json` — 行为矩阵原始输出(三列×两行,trafilatura 2.3.0)
- `evidence/matrix-script.py` — 矩阵取证脚本(离线夹具,可复现)
- `evidence/judge-output.txt` — pagetype 判别力探测(恒 None)+ extract_required 拒载实证
- `evidence/judge-script.py` — 判据验证脚本
