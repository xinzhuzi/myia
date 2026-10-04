# Design:情报流告警规则引擎(v12-backlog G5 主体)

> 决议来源:PRD「Grill 决议(2026-10-04)」Q1-Q8(自律 grill,经主人 /workflow 授权);本文把决议展开为可开工契约,与决议冲突时以 PRD 决议节为准。
> 行号口径:本文引用 = 当前工作区(10-03-shishi-everywhere 改名后 `src/myia/` → `src/shishi/`;`desktop/entry.py` 在途修改使 PRD 现状段的 `push.test` 3613 漂移为 3503)。全部行号 2026-10-04 实读核实。

## 1. 架构总览

```
规则(UI 管理)                 执行(ingest 附加步)                观察(协议/CLI)
──────────────                 ────────────────────                ──────────────
消息屏「告警规则」子面板   ┌─→ Pipeline.run() 阶段循环后、     ┌─→ alerts.fired 事件(run 终态回放)
  alerts.list/save/delete/  │   maintenance 前的独立轻量附加步   │   CLI: shishi alerts list(只读)
  test(sidecar 四方法)     │   _alert_pass:                     │   logs.tail:求值错 WARNING
        │                   │     mute 预筛 → when 求值 →        │
        ▼                   │     fired 占坑(UNIQUE)→ 动作     │
SQLite alert_rules  ────────┘     push: send_immediate 同门    └─→ SQLite alert_fired(命中历史)
       alert_fired(命中历史)          tag: add_tags + items.tags 回写
```

- 条件→动作语义模仿 Inoreader Rules(PRD 模仿对象节);求值器、护栏、隔离全部复用 classify 白名单 AST 既有机器,零新语法。
- 零惊扰默认:不配规则 = 附加步一次空表 SELECT 后短路,全链路外部行为不变。

## 2. 数据模型(表结构)

### 2.1 DDL(`src/shishi/store/sqlite.py`)

```sql
CREATE TABLE IF NOT EXISTS alert_rules (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    enabled INTEGER NOT NULL DEFAULT 1,     -- 0 | 1
    scope TEXT NOT NULL DEFAULT 'global',   -- 'global' | 品类 id(七品类之一)
    when_expr TEXT NOT NULL,                -- 白名单 AST 表达式原文(SQL 保留字 when 故列名带 _expr)
    action TEXT NOT NULL,                   -- 'push' | 'tag'
    action_config TEXT NOT NULL,            -- JSON:push {channel, targets?, template?} / tag {tags: [..]}
    created_at TEXT NOT NULL,               -- ISO-8601 UTC
    updated_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS alert_fired (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    rule_id INTEGER NOT NULL,               -- 指向 alert_rules.id;规则删除后历史照留(悬挂即历史事实)
    rule_name TEXT NOT NULL,                -- snapshot at fire time:规则删除后 fired 历史仍可读
    item_id INTEGER,                        -- 可空:items 被 retention 剪枝后历史仍可读
    dedup_key TEXT NOT NULL,                -- 去重身份(None 兜底 url,digest.py:327-328 同款在引擎侧先兜底)
    title TEXT,                             -- snapshot at fire time(FeedbackRecord 先例,models.py:148-159)
    category TEXT,                          -- snapshot at fire time
    action TEXT NOT NULL,                   -- 命中时规则的动作快照 'push' | 'tag'
    action_status TEXT NOT NULL DEFAULT 'pending',  -- pending|sent|send_failed|tagged|degraded_no_channel|skipped_dry_run
    created_at TEXT NOT NULL,
    UNIQUE (rule_id, dedup_key)             -- fired 去重 = 唯一约束(决议 Q5);at-most-once 门闩(决议 Q3)
);
CREATE INDEX IF NOT EXISTS idx_alert_fired_created ON alert_fired(created_at);
```

- **不 seed**(决议 Q2:零惊扰默认);无规则时空表即合法态。
- 命中计数不落 rules 行(决议 Q1:save 全量替换会清计数),由 `alert_fired` GROUP BY COUNT 派生(§3 `fired_counts`)。

### 2.2 迁移(双路径,决议 Q2)

- `SCHEMA_VERSION` 6→7(`sqlite.py:74`);`_MIGRATIONS` 链(`sqlite.py:320-326`)追加 `7: _migrate_v7_add_alerts`——完整同构先例 `_migrate_v4_add_feedback`(`sqlite.py:232-267`):`CREATE TABLE IF NOT EXISTS` + `CREATE INDEX IF NOT EXISTS`,幂等、纯增量、现有表与行零触碰。
- 双路径:新库 `_SCHEMA` 基线直接含两表(基线 = 建表后重放迁移的幂等保证,`_MIGRATIONS` 注释原文);旧库(v6)打开时 `ensure_schema` 自动走 v7 迁移,**零数据迁移**(两表皆新表,无既有数据搬运)。
- 回滚:v7 库被旧版本打开 → 既有「不要降级打开新库」护栏直拦(`sqlite.py:545-550`)。

### 2.3 dataclass(`src/shishi/store/models.py`)

```python
@dataclass(slots=True)
class AlertRule:        # name/when/action/action_config/scope='global'/enabled=True/id/created_at/updated_at
@dataclass(slots=True)
class AlertFired:       # rule_id/rule_name/dedup_key/action/action_status='pending'/item_id/title/category/created_at/id
```

`when` 字段名与 `RouteRuleConfig.when`(`src/shishi/schema.py:991-1007`)对齐;store 层与 `when_expr` 列互转。

## 3. Store Protocol 扩展(`src/shishi/store/base.py`)

决议 Q2 工作量项:Protocol 扩规则方法族 + fired 方法族,契约 docstring 同步(每方法一行语义 + 参数约束 + 返回形态)。

| 方法 | 契约 |
|---|---|
| `save_alert_rule(rule: AlertRule) -> AlertRule` | 单条 upsert:带 id = UPDATE(未知 id 抛值错);无 id = INSERT;`updated_at` 落库侧刷新。协议层全量替换(§4)在此之上 diff 编排 |
| `list_alert_rules(*, enabled: bool \| None = None) -> list[AlertRule]` | 全量,id 升序;`enabled=None` 不过滤(引擎取 `enabled=True`) |
| `delete_alert_rule(rule_id: int) -> bool` | 删定义行;**不删 fired 历史**(决议:命中历史是事实);不存在返回 False |
| `record_fired(fired: AlertFired) -> AlertFired \| None` | **占坑门闩**:`INSERT`,UNIQUE(rule_id, dedup_key) 冲突返回 None(调用方跳过动作);成功返回落库行(含 id)。at-most-once 哲学同 send_immediate 的 registry(digest.py:329-343) |
| `mark_alert_fired_status(fired_id: int, status: str) -> None` | 动作结果回填(pending → 终态);§2.1 枚举 |
| `has_fired(rule_id: int, dedup_key: str) -> bool` | 命中预查(alerts.test 展示「该条目此规则已触发过」) |
| `list_fired(*, rule_id: int \| None = None, since: datetime \| None = None, limit: int = 100) -> list[AlertFired]` | 新→旧;`since` 过滤供 sidecar run 终态回放(§4.3);limit 钳制 [1,200](runs.list 先例) |
| `fired_counts() -> dict[int, int]` | `SELECT rule_id, COUNT(*) … GROUP BY rule_id`——决议「计数由 alert_fired COUNT 派生」的落点;alerts.list 载荷用它拼 `fired_count` |
| `update_item_tags(*, dedup_key: str, tags: Sequence[str]) -> bool` | 回写 `items.tags`(JSON 数组列,`sqlite.py:99`);按 dedup_key 定位(`get_item_by_dedup_key` 同门单行语义,base.py:53);行不存在 False。决议 Q4-③ 新增方法(base.py 现无) |

注:`dedup_key=None` 兜底 url 的责任在引擎侧(与 digest.py:327-328 `view.get("dedup_key") or view.get("url")` 同款),store 收到的 dedup_key 恒非空。

## 4. sidecar 协议(`desktop/entry.py`)

### 4.1 四方法(决议 Q1,三处钉死)

`_HANDLERS`(`desktop/entry.py:3571`,现 43 条)追加 4 条;`PROTOCOL_VERSION` 6→**7**(占位规则见 §4.4)。

| 方法 | 载荷 → 应答 | 契约 |
|---|---|---|
| `alerts.list` | `{}` → `{rules: [AlertRuleView]}` | AlertRuleView = 规则全字段 + `fired_count`(fired_counts 派生)+ `last_fired_at`(list_fired 首行派生,无命中 null) |
| `alerts.save` | `{rules: [AlertRuleInput]}` → `{ok, rules: [AlertRuleView]}` | **全量替换承建/改/启停,不设独立启停方法**(钉死①;push.write 全量先例 `entry.py:3359-3366`「编辑一条提交整个数组」)。两道门:①逐条构造 AlertRule(构造期拒见 §5.1),任一条失败 → `alert_rule_invalid` 整批零写入;②全批构造成功后 diff 落库——载荷元素带 id = `save_alert_rule` 更新保 id,不带 = 新建,库中多余 id = `delete_alert_rule`。**id 稳定是计数派生的前提**(fired.rule_id 不悬空)。启停 = 整数组提交时该行 `enabled` 翻转 |
| `alerts.delete` | `{id}` → `{ok}` | 未知 id → `alert_not_found`;fired 历史照留 |
| `alerts.test` | `{rule? \| rule_id?, item? \| item_id?}` → `{matched, muted, actions, eval_error?, already_fired?}` | **dry 求值,不真发不落 fired**(钉死②)。`rule` = 草稿(未保存即可测);`rule_id` = 已存规则。`item` = 合成字段 dict(title/content/source/url/category/scores/metadata 任意子集,`Item.from_extracted` 构造);`item_id` = 库内条目(`get_item`,求值上下文与引擎同门 §5.2);两者都缺 = 取最近一条(`list_items` limit=1 新→旧),空库 → `alert_test_no_item`。应答 `actions` = 将触发的动作展开(push:通道解析结果 + targets/template + 降级原因;tag: tags),`already_fired` = has_fired(仅 rule_id 形态),`muted` = 该条目按当前 effective mute 是否被压制。**真发测试借既有 `push.test`**(`entry.py:3503`,feed-ux 批先例),不另建发送路径 |

### 4.2 事件 `alerts.fired`

```jsonc
{"type": "alerts.fired", "rule_id": 3, "rule_name": "竞对融资", "item_id": 42,
 "dedup_key": "…", "title": "…", "action": "push", "action_status": "sent", "ts": "…"}
```

UI 角标/通知用(PRD R4);v1 消费 = webview toast + 命中数刷新。

### 4.3 事件通路(决议 Q1 钉一条)

**主路线(采用)**:run 完成时父进程查新 fired 回放——子进程 run 落 alert_fired;sidecar 父进程在 run 终态收口(发 `completed` 事件的同一处,`_m_run_start` 的监管线程)以 `list_fired(since=run.started_at)` 查新命中,逐条 `_write_line` 发 `alerts.fired`。store 打开方式同 `_m_store_items`(sidecar 直读单库先例)。
**备选(不采用,记录在案)**:`_emit_progress` 正则解析子进程 stderr 日志(`entry.py:2292`)——不采用理由:依赖子进程日志格式(脆弱契约),而 fired 已结构化落库,查库回放零格式耦合。

### 4.4 版本号与在途并存(钉死③)

- 本批预定 **v7**;若 `10-04-hermes-cron`(唯一协议占用方,其 `cron.*` 9 方法族见其 prd:27,与本族不相交,且明确不做 UI 屏见其 prd:45)先合入占 v7,则本批顺延 **v8**——按合入顺序定,开工 Stage D 第一步实读 `PROTOCOL_VERSION` 当前值定案。
- spec 镜像表(`.trellis/spec/desktop/sidecar-protocol.md`)分段追加:方法注册表新增「alerts 段(4 行)」,总对账行数 43→47(若 v8 则注明顺延缘由);两批分段追加可并存,互不改写对方行。

## 5. 规则引擎(`src/shishi/alerts/`,新包)

```
src/shishi/alerts/
  __init__.py   # 再导出 AlertRule/AlertFired/AlertConfigError/AlertEngine/alert_view
  rule.py       # AlertRule dataclass + 构造期拒
  engine.py     # alert_view + AlertEngine(求值/mute 预筛/动作执行)
```

依赖方向:engine 只依赖 classifier Rule、push send_immediate、store 协议;**不 import Pipeline**(mute 词表/tuning 由 Pipeline 传入)。

### 5.1 构造期拒(rule.py,决议 Q7)

`AlertRule.__post_init__` 对齐 `RouteRule.__post_init__` 先例(`src/shishi/push/route.py:100-109`):

- `action not in ('push','tag')` / `scope` 非 global 且非已知品类 / name 空 → `AlertConfigError`(中文结构化消息,`字段校验失败: …` 同款文案)。
- `try: Rule(name=f"alert→{action}", when=self.when, tag=…)` 捕 `RuleSyntaxError` → `AlertConfigError`(白名单 AST 越权构造:属性访问/下标/lambda/超 1000 字符,装载期即拒,`myia-classifier/myia_classifier/custom.py:74-143`)。
- action_config 形状:push 需 `channel ∈ shishi.push.CHANNELS` + 可选 `targets: list[str]`、`template: str`;tag 需 `tags: list[str]` 非空。store 载入(读库)与协议保存(写库)共用同一构造门——读库坏行 = 单行 WARNING 跳过(隔离),写库 = 结构化拒整批。

### 5.2 求值上下文(决议 Q7 补缺口)

`alert_view(item) -> dict`:`ctx = item.view()`(`pipeline.py:465-478`:metadata 平铺 + url/title/source/category/scores/dedup_key 顶层)后补 **`ctx['content'] = item.content`**——`Item.view()` 不含 content(`from_extracted` 将 content 摘出 metadata,`pipeline.py:453-461`),PRD 条件候选「关键词:标题/正文/来源」中正文条件在原生 view 写不了;route 共享的 `view()` 零波及(补丁在告警引擎侧,不改 `Item.view()`)。

字段面:`category/title/source/url/dedup_key/tags` 全在 view;score 阈值用 **`metadata['score']` 标量**(enrich 回填,`pipeline.py:1846-1847` docstring 明言 what push.route score rules read;route 同读法);`scores` 是 dict,白名单禁下标不构成障碍(单维阈值写 `score >= 4` 而非 `scores['x']`);enrich 未启用品类 score=None → 比较 TypeError → 既有隔离(WARNING + 未命中,`custom.py:353-362`)。

### 5.3 求值与隔离

运行期逐条目 × 逐启用规则:`Rule.evaluate`(白名单 AST,资源护栏防 `9**9**9`,never eval)。求值错 = 单条 WARNING + 视为未命中,不 break 批(`custom.py:353-362` 先例);错进 stderr → sidecar 环形缓冲 → `logs.tail` 可见(PRD R6/AC)。

### 5.4 mute 硬规则(决议 Q5)

- **mute 命中不触发**(硬规则,测试钉死):判定源 = 引擎自跑 `mute_hit(item.title, mute_words)`(`src/shishi/enrich/scoring.py:76`,title 子串语义)+ 词表来自 `_effective_watchlist`(`pipeline.py:2018-2028`,反馈 0.0 权重词已并入 mute)。
- **不读 `metadata['muted']` 标记**:enrich 未启用品类无该标记(`_stage_analyze` 直通,`pipeline.py:1859-1863`);自跑判定与品类 enrich 开关解耦。
- 命中 mute 的条目跳过全部规则求值,不落 fired。

## 6. 管线挂点(决议 Q3)

### 6.1 形态:run() 阶段循环后的独立轻量附加步

`Pipeline.run()` 阶段循环之后、maintenance 之前调 `_alert_pass`;**明确不取「并入 _stage_push 收尾」**——`_stage_push` 开头 `if not self.config.push` 直接 return(`pipeline.py:2115-2119`),品类未配 push 通道时并入收尾的告警(含 tag-only 规则)全哑。

```
_alert_pass(items, run_store, registry, dry_run, result):
  0 dry_run=True → 直接 return(钉死:最强零告警——不评估、不占坑、不发;
    非 dry 时 fired 落 run_store 恒真,dry-run 本就换内存库 pipeline.py:966)
  1 rules = run_store.list_alert_rules(enabled=True);空 → return(零惊扰:
    唯一开销 = 每 run 一次空表 SELECT,外部行为不变)
  2 tuning = load_active_tuning(run_store)(与 _stage_analyze 同门);
    mute_words = self._effective_watchlist(tuning)["mute"]
  3 逐条目:mute_hit(item.title, mute_words) 命中 → 跳过(§5.4)
  4 逐规则:evaluate(alert_view(item));求值错 → WARNING 未命中(§5.3)
  5 命中 → key = item.dedup_key or item.url(digest.py:327-328 同款兜底);
    fired = run_store.record_fired(占坑)→ None(UNIQUE 冲突)→ 跳过动作
  6 动作执行(§7)→ run_store.mark_alert_fired_status 回填终态
```

- 附加步不进 `STAGE_OPTION_NAMES`/`RESUME_CHECKPOINT_STAGES`(`pipeline.py:235-240`)/`EXECUTED_STAGES`,不写 `runs.steps`(轻量附加步,PRD 推荐原文);自身失败 = WARNING 隔离,不影响 run 终态(与 stage 隔离哲学一致)。
- **输入 = `result.items` 而非 `current`**:push 阶段 broken 时 `result.items = []`(`pipeline.py:1118`,items 只统计走完全链的条目)——broken 时告警同步跳过,同哲学。
- dry-run 语义:run_store 在 dry 下是内存库(`pipeline.py:966`);§6.1-0 直接短路比「落内存库」更强,决议「零告警承诺自动成立」取强式。

### 6.2 失败重跑推演(至多一次)

重跑(resume)接管 fetch/classify/dedup 检查点(`RESUME_CHECKPOINT_STAGES`,`pipeline.py:240`)后,analyze/push 对检查点同批条目重跑,告警确会再求值——防线 = §6.1-5 **先 INSERT alert_fired 占坑,UNIQUE(rule_id, dedup_key) 冲突即跳过动作,占坑成功才执行动作**:崩溃在动作前(pending 残留)或重跑再评估,均被唯一约束拦住,不重发。与 `send_immediate` 槽位 registry 的 at-most-once 同哲学(`digest.py:329-343`);唯一约束够,无需额外状态机。

## 7. 动作执行(决议 Q4)

v1 动作集 = **push + tag**;每规则单动作(存储二选一);沉淀为关键词 / digest 汇总留 v2。

### 7.1 push 动作(send_immediate 同门)

- 通道凭据来源钉死:`Channel` 实例 = 在**当前品类 `push[]` 内解析该 `channel` 类型的第一条**(`Pipeline._build_channel` 同门,`pipeline.py:908-930`,凭 dict registry + 注入);**品类未配该类型 = 该动作降级**(WARNING + fired 记录不发,`action_status='degraded_no_channel'`);**禁止跨品类借凭据**。
- 发送:`await send_immediate([item], channels=[ch], registry=registry, category=…, tz=self._tz, item_specs=[targets or None])`(`digest.py:290-351` 签名)——registry 复用 run() 的 `DedupRegistry`(`_ensure_registry(run_store)`,`pipeline.py:894-895,1007`),槽位防重发免费获得;单通道失败不拦其余(partial failure 内建)。
- 双向压制(测试两方向钉死,决议 Q4-①):
  - route immediate 先发(管线序:push 阶段在前)→ 告警 send_immediate 被 `registry.should_send` 拦(`digest.py:329-331`);
  - 告警先发(route 走 digest 的条目)→ digest flush 被同注册表拦(`digest.py:280-288`)。
- 结果回填:`any(r.ok)` → `sent`,否则 `send_failed`。

### 7.2 tag 动作(决议 Q4-③ 补回写)

条目在 dedup 阶段已入库(`pipeline.py:1807` `store.save_item`),push 后 tag 两步:

1. 内存:`item.add_tags(tags)`(`pipeline.py:480-486`,保序去重合并 metadata['tags']);
2. 回写:`run_store.update_item_tags(dedup_key=key, tags=item.metadata['tags'])` 落 `items.tags` JSON 列(§3 新增方法)——否则标签只在当批内存对象,库行不带走。

`action_status='tagged'`(回写 False = 行已剪,WARNING + 状态如实)。

## 8. CLI(决议 Q8)

- 桌面 sidecar 独占写路径;CLI 只读 `shishi alerts list`(查 fired 历史),对齐 feedback 子命令先例(`src/shishi/cli.py:487-502` `_add_feedback_parser`):`--rule <id>` 过滤、`--limit`(钳制 [1,200])、`--json` 机器可读;输出行 = 时间/规则名(快照)/条目标题/动作/状态。CLI 写路径留 v2。
- 注:决议原文「myia alerts list」为 CLI 泛称;当前 binary 名 `shishi`(cli.py docstring 口径)。

## 9. UI 布局(决议 Q6:消息屏下区子面板)

`desktop/ui-src/src/screens/messaging/messaging-screen.tsx` 推送规则面板(:451-489)之后,同款 Card 追加「告警规则」子面板(同属「消息怎么发」心智,`alerts.list` 一次拉齐):

```
┌─ Card:告警规则 ──────────────────────────────── [新建规则] ─┐
│ 说明文案:对每条新入流情报求值,命中即推送/打标;保存 = 全量写回规则表 │
│ ┌────────────────────────────────────────────────────┐ │
│ │ [Switch启停] 名称  ⟨全局|品类id⟩  when 等宽摘要      │ │
│ │              动作徽章(push→通道名 / tag→标签)  命中 N │ │
│ │              [测试] [编辑] [删除(二次确认)]          │ │
│ └────────────────────────────────────────────────────┘ │
│ 空态 EmptyState:「还没有告警规则」                          │
│ 表单(新建/编辑,内联展开):name · scope(全局/品类下拉=yaml.list)│
│   · when textarea(等宽) · action 单选 push|tag            │
│   push → channel 下拉(shishi.push.CHANNELS 名集;          │
│     提示文案「执行时取该品类 push[] 第一个此类型通道;未配置则降级不发」)│
│     · targets 可选 · template 可选                          │
│   tag  → tags 逗号分隔                                      │
│ 测试结果面板:matched / muted(压制提示)/ actions 展开 /      │
│   already_fired / 坏 when 结构化错误(alerts.save 构造期错直显)│
└──────────────────────────────────────────────────────────┘
```

- 数据流:`messaging/api.ts` 增 `alertsList/alertsSave/alertsDelete/alertsTest` + 视图类型(该文件在途改动经 `git diff` 实证仅一行注释更名 myia.push→shishi.push,无功能占用);`lib/api/types.ts` 同步。
- 事件消费:webview 监听 `alerts.fired` → toast + 规则行命中数刷新。
- 并行流核查(决议 Q6):hermes-cron 不做 UI 屏(其 prd:45);crawl4ai-l3 为引擎层不动此屏;feed 卡就地建规则留 v2。

## 10. 错误码

| code | 场景 | data |
|---|---|---|
| `alert_rule_invalid` | `alerts.save` 某条构造期拒(name/scope/when 语法/action/config 形状) | `{index, field, reason}`(整批零写入) |
| `alert_not_found` | `alerts.delete` / `alerts.test`(rule_id 形态)未知 id | `{id}` |
| `item_not_found` | `alerts.test` 的 item_id 未知 | `{item_id}`(对齐 feedback.mark 先例,spec 镜像表 :52) |
| `alert_test_no_item` | `alerts.test` 无 item/item_id 且库空(缺省取最近一条失败) | `{}` |

运行期求值错 / mute 压制 / 通道降级 / 发送失败 = **非协议错**:WARNING 隔离(§5.3/§7.1),logs.tail 可见,不拦批、不影响 run 终态。

## 11. 测试面

| 层 | 文件 | 覆盖 |
|---|---|---|
| store | `tests/test_store_alerts.py`(新) | v6→v7 迁移(旧库打开自动升级/幂等重放/新库基线);两表 CRUD;record_fired UNIQUE 占坑冲突;fired_counts 派生;update_item_tags 回写;delete_rule 不删 fired |
| 引擎 | `tests/test_alert_engine.py`(新) | 构造期拒全形态(属性访问/下标/lambda/超长/bad action/scope);`9**9**9` 资源护栏;alert_view 含 content(view 零波及回归);score=None 隔离;mute 硬规则(enrich 未启用仍压制;反馈 0.0 词并入) |
| 管线 | `tests/test_alert_pipeline.py`(新) | 零规则逐字节不变(全量回归零新红);dry-run 短路零落库;broken(result.items=[])跳过;占坑至多一次(重跑/崩溃窗口);双向压制两方向;凭据降级(WARNING+fired 不发);tag 两步回写;附加步失败 WARNING 不改 run 终态 |
| 协议 | `tests/test_desktop_sidecar_protocol.py`(增) | 四方法载荷契约;全量替换保 id;构造期错整批零写入;alerts.test 三取材形态;`alert_*` 错误码;PROTOCOL_VERSION 断言(按 §4.4 占位定案值);alerts.fired 回放事件 |
| CLI | `tests/test_cli.py`(增) | `shishi alerts list` 只读(--rule/--limit/--json);无写子命令 |
| UI | `messaging-screen.test.tsx`(增,vitest) | 子面板渲染/列表/启停=全量提交/坏 when 结构化错直显/测试结果面板/删除二次确认 |
