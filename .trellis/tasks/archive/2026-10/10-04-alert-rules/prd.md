# PRD:情报流告警规则引擎(v12-backlog G5 主体)

## 背景

- 源头:UI 普查 G5(`archive/2026-10/10-03-ui-feature-census/prd.md:28`)——业界普遍有
  「通知中心+触发器+分级 digest」(OpenCTI)与「Rules 条件→动作」(Inoreader),MYIA 现状
  =推送凭据可配但无关键词即时告警、无 digest 汇总;拍板 P2,主体入 v12-backlog 池
  (池档 `10-03-v12-backlog/prd.md` 第 5 项)。
- **G5 前半已落地**:设置屏推送测试按钮(`push.test`,`desktop/entry.py:3613`,
  feed-ux 批);本档只做**主体:告警规则引擎**。
- 本档 planning 期的「收现状 + 草案 + grill 待决」已于 **2026-10-04 自律 grill(经主人
  /workflow 授权)闭环**:Q1-Q8 决议见下方「Grill 决议」节,Requirements/AC 已按决议
  改定;契约展开 = `design.md`(表结构/方法契约/引擎挂点/错误码/UI 布局),阶段与门禁
  = `implement.md`。

## 模仿对象:Inoreader Rules 语义

census 调研原始报告(`archive/2026-10/10-03-ui-feature-census/research/feed-monitors.md:21`):

> Rules:按**关键词/来源/提及**条件触发**打标、推送、邮件、标记已读**,2025 年起新增
> 「翻译/摘要」动作(Inoreader 官方博客,2025-10)。

MYIA 式转译:**条件(对一条情报的谓词)→ 动作(推送指定通道/加标签/沉淀关键词)**;
规则可启停、可即时测试(Inoreader 的 "test rule" 对应本仓 `push.test` 先例)。
OpenCTI 的「分级 digest」(汇总勿扰)是第二形态,v1 是否收见 Grill Q7。

## 现状实读(2026-10-04,main@1d4ad62)

### 条件候选(数据面支撑,`src/myia/store`)

| 条件 | 支撑字段/机制 | 出处 |
|---|---|---|
| 品类 | `ItemRecord.category`(七品类+channel) | `src/myia/store/models.py:85` |
| 关键词 | 标题/正文/来源三列 LIKE(`list_items.query`)与 metadata 任意字段 | `src/myia/store/base.py:61-79` |
| score 阈值 | `ItemRecord.scores`(enrich 精评回填,dict 维度→分值;前端取最大值) | `src/myia/store/models.py:86`、`ui-src/src/screens/feed/api.ts:254-256` |
| 免费信号 | 品类判定内部阶段「free signal beats paid signal」→ freebie/token;`BuiltinResult.matched` 留命中 trace | `myia-classifier/myia_classifier/builtin.py:14-15,140-145` |
| 提及量趋势 | `metric_history` 品类级 `keyword:<词>` mentions 快照(周环比现成) | `src/myia/store/base.py:258-330` |

**既有条件求值器(最大复用点)**:`push.route[]` 已是「条件→模式」雏形——
`RouteRuleConfig {when: ExprStr, mode, targets}`(`src/myia/schema.py:991-1007`),
`when` 表达式走 classify 白名单 AST 求值器(字面量/字段名/链式比较/and·or/
abs·min·max·round·len·int·float·str 白名单函数;禁属性访问/下标/lambda;
表达式 ≤1000 字符;资源护栏防 `9**9**9`;**never eval**),
`myia-classifier/myia_classifier/custom.py:11-31`。求值上下文 = `Item.view()`
(metadata 平铺 + url/title/source/category/scores/dedup_key),
`src/myia/pipeline.py:465-477`。

### 动作候选(方法面/管线面支撑)

| 动作 | 复用面 | 出处 |
|---|---|---|
| 推送(即时/指定通道+对象) | `send_immediate`(AM/PM 同槽位防重发注册表)、通道 targets 定向 | `src/myia/push/digest.py:292-351` |
| 推送(digest 汇总) | `DigestAggregator`(slot 内聚合、压制窗口) | `src/myia/push/digest.py:140-274` |
| 测试发送 | `push.test` 合成单条真发(先例,G5 前半) | `desktop/entry.py:3613` |
| 加标签 | `Item.add_tags` / classify rule tag 通路 | `src/myia/pipeline.py:480-486` |
| 沉淀为关键词 | G12 就地面板写品类 YAML `watchlist.keywords` | `ui-src/src/screens/feed/feed-screen.tsx:121-129` |

### 管线挂点(求值时机候选的物理位置)

`Pipeline.run` 阶段链 = fetch→classify→dedup→analyze(enrich 回填 score)→
aggregate(可选)→push→maintenance(`src/myia/pipeline.py:942-1166`)。
push 阶段内已有 `resolve_route` 逐条路由(`src/myia/push/route.py:1-22`,
决策序:score 规则→品类覆盖→七品类缺省映射→保守 digest)。
sidecar 面:`run.start` 单飞(`run_busy`),终态走 `completed` 事件;
`store.items` 直读条目;`_HANDLERS` 现 43 方法,`PROTOCOL_VERSION = 6`
(`desktop/entry.py:336,3571-3615`)——新增方法族须 bump v7 并同步
`.trellis/spec/desktop/sidecar-protocol.md` 镜像表。

### feed 屏既有过滤/交互(去重关系参照)

- 过滤页签 未读/星标/稍后读/全部 = **前端 localStorage 本地态**
  (`ui-src/src/screens/feed/api.ts:154-236`,loadFeedStates/toggleMarker/
  setMarkerBulk/applyFeedFilter),服务端无已读/星标列;
- 搜索 G1 走 `store.items.query`(防抖 300ms);G8 单卡 AI 摘要;G12 沉淀面板;
- watchlist mute(品类 YAML `WatchlistConfig.mute`,`src/myia/schema.py:858-862`)
  = 「不感兴趣」语义,与告警触发是压制关系候选(Grill Q5)。

## Requirements(2026-10-04 grill 定稿)

1. **规则模型**:一条规则 = `{名称, 启停, when 表达式(复用 route 同款白名单
   AST 文法,零新语法), 动作(push|tag 二选一), 作用域(全局/单品类)}`;坏表达式
   装载期拒(fail fast,RouteRule 构造期先例),运行期求值错按 classify 先例隔离
   (单条 WARNING + 视为未命中,不 break 批)。
2. **求值**:ingest 时求值——`Pipeline.run()` 阶段循环后、maintenance 前的**独立
   轻量附加步**(不并入 `_stage_push` 收尾:其开头 `if not self.config.push` 直接
   return,品类未配 push 时并入收尾的告警全哑);同条目同规则只触发一次
   (alert_fired UNIQUE(rule_id, dedup_key) 占坑,见 Grill Q3/Q5)。
3. **动作(v1 = push + tag)**:push = 当前品类 `push[]` 内解析该类型第一条通道
   实例走 `send_immediate` 同门(槽位注册表防重发免费获得,双向压制;品类未配该
   类型 = 降级 WARNING+fired 记录不发,禁止跨品类借凭据);tag = `Item.add_tags`
   + `items.tags` 列回写(store 新增 `update_item_tags`)。沉淀为关键词/digest 汇总
   留 v2。
4. **sidecar 协议扩展(四方法定死)**:`alerts.list / alerts.save / alerts.delete /
   alerts.test` + `alerts.fired` 事件——启停不设独立方法(save 全量替换承建/改/启停,
   push.write 先例;命中计数不落 rules 行,由 alert_fired COUNT 派生);test 必须
   带参数 `{rule|rule_id, item?(合成字段|item_id,缺省取最近一条)}` 做 dry 求值
   展示将触发动作(不真发不落 fired),真发借既有 `push.test`;`PROTOCOL_VERSION`
   6→7(占位:若 10-04-hermes-cron 先合入占 v7 则顺延 v8);spec 镜像表分段追加。
   fired 事件通路 = run 完成时父进程查新 fired 回放(不依赖子进程 stderr 日志格式)。
5. **规则管理 UI(入口定死)**:消息屏下区「告警规则」子面板(顺延推送规则面板,
   同属消息心智);规则列表(启停开关、命中计数派生)+ 新建/编辑表单(when 表达式 +
   动作选择)+ 即时测试;feed 卡就地建规则留 v2。
6. **可观测**:fired 历史可查(时间/规则/条目,CLI `shishi alerts list` 只读对齐
   feedback 先例);规则求值错误进 logs.tail 可见。
7. **零惊扰默认**:不配规则 = 现行为逐字节不变(附加步唯一开销 = 每 run 一次空表
   SELECT);dry-run 零告警(fired 不落真库不真发);mute 命中不触发(硬规则,引擎
   自跑 mute_hit + effective watchlist,不读 metadata['muted']);告警与既有
   push.route 并行不扰(route 照旧决定 immediate/digest,告警是叠加通道)。

## Acceptance Criteria(2026-10-04 按 grill 决议改定)

- [ ] 规则 CRUD+启停全走 sidecar `alerts.*` 四方法(启停并入 save 全量替换,无独立
      启停方法);协议版本 bump(本批预定 v7,若 hermes-cron 先占 v7 则 v8)且 spec
      镜像表对账一致(方法注册表分段追加)
- [ ] when 表达式复用 classify 白名单 AST:越权构造(属性访问/下标/lambda/超长)装载
      期结构化拒;`9**9**9` 类资源炸弹不出进程
- [ ] 命中即触发且同条目同规则不重复触发:alert_fired UNIQUE(rule_id,dedup_key)
      占坑先行、占坑成功才执行动作——崩溃/失败重跑不重发(至多一次,测试钉死)
- [ ] 推送动作经 `send_immediate` 同门:同槽位防重发注册表**双向压制**生效(route
      immediate 先发→告警被拦;告警先发→digest flush 被拦,两方向测试钉死);通道
      失败结构化上报不拦其余条目;品类未配该类型通道时降级(WARNING+fired 记录不发,
      禁止跨品类借凭据)
- [ ] 不配规则时全链路行为与现状逐字节一致(既有 route/digest 测试全绿);dry-run
      零告警(fired 不落真库、不真发);push 阶段 broken 时告警同步跳过
- [ ] mute 命中条目**不触发**(硬规则,测试钉死):判定 = 引擎自跑 mute_hit +
      effective watchlist(反馈 0.0 权重词并入),不读 metadata['muted'](与品类
      enrich 开关解耦)
- [ ] tag 动作两步落地:`Item.add_tags` + `items.tags` 列回写(store 新增
      update_item_tags)
- [ ] 规则管理 UI(消息屏下区子面板):建/改/删/启停/即时测试五操作落地,坏表达式
      UI 内可见结构化错误;alerts.test 三取材(草稿 rule/已存 rule_id/合成 item|
      item_id|缺省最近一条)dry 展示将触发动作
- [ ] `alerts.fired` 事件在 run 终态由父进程查新 fired 回放到达 webview(不依赖
      子进程 stderr 日志格式);fired 历史可查(sidecar + CLI `shishi alerts list`
      只读)且 logs.tail 可见求值错误
- [ ] 旧库(v6)打开自动升级 v7 零数据迁移(双路径:新库 _SCHEMA 基线 + 旧库幂等
      迁移);不 seed(零惊扰默认)

## Grill 决议(2026-10-04,自律 grill,经主人 /workflow 授权)

> 8 问全部按推荐成立;以下为决议原文转录,与上文推荐段冲突处以本节为准。
> 行号口径 = 2026-10-04 工作区实读(`src/myia/` 已随 10-03-shishi-everywhere 更名为
> `src/shishi/`;`desktop/entry.py` 在途修改使 push.test 由 3613 漂移至 3503——
> 上文「现状实读」段保留 main@1d4ad62 历史口径不动)。契约展开见 design.md。

**Q1(协议面)按推荐四方法** `alerts.list/save/delete/test` + `alerts.fired` 事件,
三处钉死:①**启停不设独立方法**——alerts.save 全量替换承建/改/启停(push.write
全量先例 `desktop/entry.py:3359-3366`),命中计数不落 rules 行(save 全量会清计数),
由 alert_fired COUNT 派生;②**alerts.test 必须带参数** `{rule|rule_id, item?(合成
字段|item_id,缺省取最近一条走 store.items)}` 做 dry 求值展示将触发动作,真发借
push.test(`entry.py:3503` 先例);③**v7 不撞在途根本**——唯一协议占用方
10-04-hermes-cron 加 cron.* 9 方法(其 prd:27)与本族不相交且其明确不做 UI 屏,
版本号按合入顺序定(本批预定 v7,若 hermes-cron 先合入占 v7 则本批顺延 v8),spec
镜像表分段追加可并存;事件通路推荐 **run 完成时父进程查新 fired 回放**(不依赖子
进程 stderr 日志格式,_emit_progress 正则路线 `entry.py:2292` 备选),design 钉一条。

**Q2(规则存储)按推荐 SQLite 两表**(`alert_rules` + `alert_fired`)。迁移走
`_MIGRATIONS` 链追加 `_migrate_v7`(`sqlite.py:320-324` v2→v6 先例),双路径 = 新库
`_SCHEMA` 基线 + 旧库 `CREATE TABLE IF NOT EXISTS` 幂等迁移(`_migrate_v4_add_feedback`
`:232-267` 完整同构先例),现有库打开自动升级零数据迁移;**不 seed**(零惊扰默认,
AC 已钉);alert_fired 带 **title snapshot**(FeedbackRecord 先例
`store/models.py:148-159`,items 被 retention 剪枝后 fired 历史仍可读)。工作量项进
design:Store Protocol(base.py)扩 save/list/delete_alert_rule +
record_fired/has_fired/list_fired 方法族并同步契约 docstring。

**Q3(求值时机)按推荐 ingest 时挂 push 后**,但钉死形态为 **run() 阶段循环后的
独立轻量附加步**、明确不取「并入 _stage_push 收尾」——_stage_push 开头
`if not self.config.push` 直接 return(`pipeline.py:2115-2119`),品类未配 push 通道
时并入收尾的告警(含 tag-only 规则)全哑;独立步用 run_store(dry-run=内存库
`:966`,fired 不落真库,零告警承诺自动成立),且 push 阶段 broken 时
(result.items=[] `:1118`)告警同步跳过。失败重跑推演:重跑接管 fetch/classify/dedup
检查点(RESUME_CHECKPOINT_STAGES `:240`)后 analyze/push 对同批条目重跑、告警确会
再求值,防线 = **先 INSERT alert_fired 占坑(UNIQUE(rule_id,dedup_key) 冲突即跳过
动作)成功才推送**——至多一次语义与 send_immediate 的 registry 同哲学
(`digest.py:329-343`),崩溃/重跑不重发,唯一约束够;dedup_key 为 None 兜底
url(`:328` 同款)。

**Q4(动作集)按推荐 push+tag、沉淀/digest 留 v2**,叠加语义成立并补两处实现缺口:
①**同 key 同槽位自然压制双向收敛**——route immediate 先发则告警 send_immediate 被
registry.should_send 拦(`digest.py:329-331`),告警先发则 digest flush 被同注册表拦
(`:280-284`),两个方向测试钉死;②**通道凭据来源钉死**——send_immediate 需要
Channel 实例、凭据来自当前品类 push[],规则动作的 channel 引用在当前品类 push[] 内
解析该类型第一条,品类未配该类型 = 该动作降级(WARNING+fired 记录不发),禁止跨
品类借凭据;③**tag 动作补回写**——条目在 dedup 阶段已入库(`pipeline.py:1807`),
push 后 tag = Item.add_tags(`:480-486`)+ 新增 store.update_item_tags 回写 items 表
(base.py 现无此方法),进 design。

**Q5(去重/mute/route)按推荐全部成立**:fired 去重 = alert_fired(rule_id,
dedup_key) 唯一约束独立表,dedup_registry 是槽位防重发语义(last_pushed_at 可覆盖)
不复用正确;**mute 命中不触发**(硬规则测试钉死),判定源钉为引擎复用 mute_hit
(`scoring.py:76`)+ `_effective_watchlist`(`pipeline.py:2018-2028`,反馈 0.0 权重词
已并入)自跑——**不读 metadata['muted'] 标记**,因 enrich 未启用品类无该标记
(_stage_analyze 直通 `:1859-1863`),自跑判定与品类 enrich 开关解耦;route 照旧
并行、告警为叠加通道。

**Q6(UI 入口)按推荐消息屏下区子面板**,并行流核查通过:推送规则面板在
`messaging-screen.tsx:451-489`,「告警规则」子面板顺延其后同属消息心智;hermes-cron
明确不做 UI 屏(其 prd:45),crawl4ai-l3 为引擎层不动此屏;messaging/api.ts 在途
改动经 git diff 实证仅一行注释更名(myia.push→shishi.push)无功能占用。feed 卡就地
建规则留 v2。

**Q7(范围裁剪)按推荐 when 复用白名单 AST、不做表单构建器**,语法/资源护栏/隔离
全现成(`custom.py:74-143` 白名单+护栏,Rule.evaluate 求值错 WARNING+未命中
`:353-362`,RouteRule 构造期拒先例 `route.py:100-109`);补一处求值上下文缺口——
Item.view() 不含 content(`pipeline.py:465-478`;from_extracted 将 content 摘出
metadata `:453-461`),PRD 条件候选「关键词:标题/正文/来源」中正文条件在原生 view
写不了,修法 = 告警引擎构造 ctx=item.view() 后补 ctx['content']=item.content,route
共享的 view() 零波及;score 阈值用 metadata['score'] 标量(enrich 回填
`:1846-1847`,route 同读法),scores dict 禁下标不构成障碍、enrich 未启用时
score=None 走既有隔离;其余候选字段 category/title/source/url/dedup_key/tags 全在
view。

**Q8(CLI 面)按推荐桌面独占写路径 + CLI 只读 `myia alerts list`**(查 fired
历史),对齐 feedback 子命令先例(`cli.py:488-499`);CLI 写路径留 v2。

## Grill 待决(8 问,每问带推荐;已决,见上节)

**Q1 协议面形状**:`alerts.*` 方法族怎么切?五方法(list/save/delete/test/dryrun)
还是三方法(list/save/delete)+ 既有 `push.test` 借用?
**推荐**:四方法 `alerts.list / alerts.save / alerts.delete / alerts.test`
(save 承建/改,全量或按 id 替换同 push.write 先例;test = 取参数里的合成条目或
`item` 引用实跑一次求值并 dry 式展示将触发的动作,不真发;真发测试借既有
`push.test`)。事件 `alerts.fired {rule_id, rule_name, item_id, action, ts}`
(UI 角标/通知用)。协议 v6→v7。

**Q2 规则存储位置**:品类 YAML 新顶层节(sidecar PrivateAttr 先例 `_baseline`/
`_aggregate`/`_images`,`src/myia/schema.py:1566-1580`)vs SQLite 新表 vs
独立 `<home>/alerts.yaml`?
**推荐**:**SQLite 新表 `alert_rules`(rule 定义)+ `alert_fired`(命中历史)**。
理由:规则是 UI 高频增删的**运行态**而非源码化配置(feedback/tuning 同为先例);
跨品类全局规则(关键词条件天然跨品类)塞进单品类 YAML 语义拧巴;fired 去重
必须落库,定义与命中同库可同事务;品类 YAML 12 节公开契约不动(SKILL.md 一致性
测试零波及)。代价:规则不随 git 源码化——接受(与 feedback/tuning 同待遇)。

**Q3 求值时机**:ingest 时(pipeline 新 stage)vs run 完成后(sidecar 扫
`since` 上次扫描点)vs 独立定时任务?
**推荐**:**ingest 时**,挂 `Pipeline` push 阶段之后、maintenance 之前,作
不进 EXECUTED_STAGES 的轻量附加步(或并入 push 阶段收尾)。理由:analyze 后
score 已回填,条件字段最全;`Item.view()` 求值上下文与 route 求值同点同构;
dry-run 语义自然跟随(零持久化副作用=零告警);断点续跑不重复求值
(dedup 后条目只过一次)。sidecar 扫描方案的「零 pipeline 改动」优势不成立:
store 侧 `raw` 投影不含全部 metadata 求值面,补投影反而更大。

**Q4 动作集与推送通道复用**:v1 动作收哪些?推送怎么复用?
**推荐**:v1 动作二选一存储但实现三态:`push`(channel+targets?+template?,
走 `send_immediate` 同门,槽位注册表防重发免费获得)与 `tag`(走
`Item.add_tags` 语义,入库前加标签);**「沉淀为关键词」动作留 v2**(G12 已有
就地面板,规则化沉淀等 UI 需求实证)。分级 digest 汇总(OpenCTI 式)留 v2,
v1 告警一律即时单卡。

**Q5 与既有过滤/dedup 的关系**:命中去重用什么?watchlist mute 与告警谁赢?
与 push.route 的优先级?
**推荐**:fired 去重 = `alert_fired (rule_id, dedup_key)` 唯一约束(独立于
`dedup_registry`——那是推送槽位防重发,语义不同不复用表);**mute 命中不触发**
(watchlist mute = 用户明示不感兴趣,告警硬穿 mute 违背漏斗语义,测试钉死);
push.route 照旧并行跑:告警是**叠加**通道不改变 route 的 immediate/digest 判定,
route immediate 命中 + 告警命中 = 两条都发(通道不同即不同卡;同通道同槽位时
槽位注册表自然压制重复卡)。

**Q6 规则管理 UI 入口**:消息屏规则区扩(现 push 规则面板旁,
`ui-src/src/screens/messaging/messaging-screen.tsx:451-475`)vs 设置屏新分区 vs
feed 屏条目卡就地「以此建规则」?
**推荐**:v1 = **消息屏下区**加「告警规则」子面板(与推送规则同属「消息怎么发」
心智,数据面 `alerts.list` 一次拉齐);feed 卡就地建规则(预填 title 关键词条件,
Inoreader 式顺手)留 v2——G12 沉淀面板已占就地交互位,先不叠加。

**Q7 v1 范围裁剪**:条件算子直接复用 when 白名单表达式,还是另造表单化条件构建器
(Inoreader Query Builder 式)?digest 汇总要吗?
**推荐**:条件 = **when 表达式原文,v1 不做表单构建器**(白名单 AST 已含
品类/关键词 contains(`in`)/score 阈值/免费信号=`category in ['freebie','token']`
全部候选形态;文法一致性测试与资源护栏现成);表单化(下拉拼条件)留 v2。
digest 汇总留 v2(见 Q4)。提及量趋势条件(metric_history 周环比)留 v2——
它是「品类级」而非「条目级」谓词,求值模型不同,不混入 v1。

**Q8 CLI 面要不要同步暴露**:`myia alerts` 子命令(建/删/列/历史)还是桌面独占?
**推荐**:v1 **桌面 sidecar 独占 + CLI 只读历史**(`myia alerts list` 查 fired,
对齐 `feedback list` 先例);规则的建删走 UI(运行态数据,与 feedback mark 的
desktop 通道同哲学)。CLI 写路径留 v2 视需求。

## 边界(明确不做)

- 不做云端索引式告警(Brand24/Google Alerts 全网监听,F 类延伸,census 拍板不追)。
- 不做 70+ 渠道矩阵(changedetection 式);通道面 = 既有 `myia.push` 通道集。
- 不做表单化条件构建器、趋势/提及量条件、digest 汇总、规则级翻译/摘要动作、
  CLI 写路径、feed 卡就地建规则(v2 候选)。
- 本档(planning/design 期)不改任何代码;design.md 与 implement.md 已按 grill
  决议立档(2026-10-04),实现按 implement.md 阶段推进。

## 关系档

- 父档(池):`10-03-v12-backlog`(第 5 项 G5 主体);拆任务引用闭环由父档 AC 约束。
- 证据档:`archive/2026-10/10-03-ui-feature-census/prd.md` G 矩阵 G5 行 +
  `research/feed-monitors.md`(Inoreader Rules 语义与官方 URL)。
- 前半搭车档:`10-03-feed-ux`(push.test)。
- 协议在途并存档:`10-04-hermes-cron`(唯一协议占用方,cron.* 9 方法族与本档
  alerts.* 不相交;PROTOCOL_VERSION v7 归属按合入顺序定,见 Grill 决议 Q1-③)。
- 相邻入池项:G6 趋势折线(与 store.trend/metric_history 同族)、G12 沉淀入口
  (本档 v2 动作的 UI 依托)。
