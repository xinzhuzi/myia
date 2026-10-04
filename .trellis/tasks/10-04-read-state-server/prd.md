# G9 服务端已读态+全库批量已读

## Goal

census G9 架构级件,走 G5 同款自律 grill 全链:已读态从 localStorage 迁服务端(store+协议+UI 切换+本地态迁移),「全部标已读」升级为全库语义。grill 要点:存储位置(items 列 vs 独立表)/localStorage 迁移策略/协议方法面/版本号动态+1(与 hermes-cron v8 竞速)

## Grill 决议(2026-10-04,B 设计师回写;行号按回写当日工作树,`## 决议证据链` 为 grill 时实读)

### Q1 存储位置:items 表加 `read`/`starred`/`later` 三列(INTEGER DEFAULT 0),不建独立 item_state 表

1. **全库批量已读在列方案 = 单条 UPDATE**;独立表要为全库每键 `INSERT OR REPLACE` 一行,N 行写天然劣势。
2. **retention 剪枝自动带走状态**:`cleanup_expired` 删 items 行(sqlite.py:1871-1878)而 dedup_registry all-time 不自动删(sqlite.py:1922-1924)→ 条目剪枝后永不重入库,独立表状态行对已剪条目是纯死重还得另修剪枝(feedback/alert_fired 留 dedup_key 快照有统计/审计目的,读态没有)。
3. **键语义红线**:localStorage itemKey = dedup_key 优先(api.ts:141-144),而 items 行可共享同一 dedup_key(sqlite.py:760-764 dated-key 旋转,multiple rows may share a historical key)——**置位必须按 dedup_key**(`WHERE dedup_key IN (...)`,同键多行同置,与今天语义一致);按 items.id 置位会让同键行显示不同状态 = 回归。
4. items 表 dedup_key 现无索引(仅 url/category,sqlite.py:119-120),按键 UPDATE 是全表扫——**迁移里顺手补 `idx_items_dedup_key`**(feedback 表同款先例 sqlite.py:180)。
5. **迁移形态**:SCHEMA_VERSION 7→8(sqlite.py:83)+ `_migrate_v8`(PRAGMA table_info 幂等检查 + ALTER×3 + 索引,v2 先例 sqlite.py:232-242);models.ItemRecord/`_row_to_item`/`_item_dict` 跟进。
6. 如实注记:`_item_dict` 是 store.items 与 feed.export JSONL 共用投影(entry.py:739-787/940),加三键连带导出 JSONL 多三键(CSV 固定列 entry.py:934 不变),加法变化须记协议档。
7. 反方「管线表混入 UI 态」不成立:entry.py 每请求独立连接(entry.py:824-835)+ WAL + busy_timeout=5000(sqlite.py:607-609),单行 UPDATE 争用可忽略。

### Q2 localStorage 迁移:一次性导入 + 服务端幂等旗标 + 本地键保留不删,不设双写期

1. **首切**:前端过能力门(`api.version().protocol ≥ 新版`,client.ts:154-155 现成)后读 localStorage 全量 map(键 `myia.feed.states.v1`,api.ts:166)→ **单请求 `store.state.import` 一次搬完**(整 map 一个请求;逐键 RPC = N 往返,否),服务端按 dedup_key 逐键 UPDATE。
2. **幂等旗标必须放服务端 store_meta**(如 `feed_state_imported_at`;get/set_meta 现成 sqlite.py:683-696),已导即 no-op——放 localStorage 不行的根本原因:Tauri webview 数据可被独立清掉,旗标丢失会让旧 map 重放、把用户 v2 期已改的服务端态倒灌覆盖回旧值。
3. **回滚 = 旧键原样搁置不删**:升级回旧版时旧 build 读旧 localStorage 快照照常工作(丢 v2 期增量,可接受且如实),删键则回滚全灭;**双写期明确否掉**——两份真源一方失败即分叉,复杂度高于收益。
4. **key 形态三分**:dedup_key 直配;`id:<n>` 解析为 items.id 再映射其 dedup_key;`id:<url>`(api.ts:143 兜底形态)服务端无从解析→**跳过并计入应答 skipped**(服务端 dedup_key NOT NULL,save_item 校验 sqlite.py:717-718,此形态实际罕见,如实计数即可)。

### Q3 协议面:3 新方法 + store.items 投影补三键,全挂既有 `store.` 数据面家族

现有 store.items/store.trend(entry.py:4092-4094);_HANDLERS 里无 `items.*` 家族,现造新家族无益。

1. **`store.state.mark`** `{keys:[dedup_key...], marker:'read'|'starred'|'later', value:bool}` → `{updated}`——单键 toggle 与已加载批量同门,前端算好目标 value 显式置位(幂等,无读-改-写竞态)。
2. **`store.state.mark_all`** `{marker, value, category?}` → `{updated}`——全库批量语义的核心件:服务端单 UPDATE;键单形状(keys 列全库键)就此**否掉**——全库键单在请求里都装不下,且逐键写丢掉单 UPDATE 的全部意义;category 可选与 store.items 同词,**不收 query**(LIKE 语义进 UPDATE 是范围蠕变,PRD 原文是全库语义);UI 侧同步把「作用域=已加载条目」的按钮 title 换成全库真话(feed-screen.tsx:807-814 现注记作废)。
3. **`store.state.import`** `{states:{key:{read?,starred?,later?}}}` → `{imported, skipped}`——Q2 搬迁门,幂等旗标在 store_meta。
4. **store.items 投影补 read/starred/later**(_item_dict,entry.py:770-787),未读计数/过滤随页内条目直接派生;**未读过滤全库化(查询参数)本批不做,范围钉死**。
5. **版本号**:动手时实读 PROTOCOL_VERSION(本刻 = 8,entry.py:379)+1 → 9;与 hermes-cron 批竞速按 alert-rules 批先例「按合入顺序定案,开工实读」(sidecar-protocol.md:86-87);SCHEMA_VERSION 同批 7→8;协议档 mirror 同步加行+版本注记。

### Q4 范围:三态(已读/星标/稍后读)一次全迁,不拆分

1. 三态在 localStorage 本就同键同对象(FeedItemState,api.ts:157-166),服务端存储形状同一份三列;只迁 read = applyFeedFilter/feed-screen.tsx:820 一半查服务端一半查 localStorage 的双源混血,复杂度高于全迁而非更低——分开迁的「省」只有哲学层(read 短暂、star 策展),工程零收益。
2. **必须钉进 PRD 的语义决策:starred/later 不豁免 retention 剪枝**(cleanup_expired 无此豁免,sqlite.py:1871-1878)——已推送条目 90 天(缺省)后连条目带星标一起消失,「稍后读」会静默过期;今天 localStorage 方案同样丢条目(服务端剪后本地键成死重,且永不自清),故无回归,但迁服务端后用户预期会抬高。**本批按「接受 + PRD 明写」处理;剪枝豁免另立任务**(动 cleanup 策略 = 动 10-01-v02-storage-hardening 既有定案,不搭车)。

## Requirements(由决议展开)

- R1 存储与迁移:items 加 `read`/`starred`/`later` 三列(INTEGER DEFAULT 0)+ `idx_items_dedup_key`;SCHEMA_VERSION 7→8,`_migrate_v8` 幂等(PRAGMA table_info 检查);models.ItemRecord/_row_to_item/_item_dict 跟进;新条目入库默认三态全 false(save_item 列清单不含三列,DEFAULT 0 即未读)。
- R2 store 层方法:按 dedup_key 置位(同键多行同置)/全库单 UPDATE(可选 category)/导入(id:<n> 映射、id:<url> 跳过计数)/`feed_state_imported_at` 旗标(get/set_meta)。
- R3 协议:`store.state.mark` / `store.state.mark_all` / `store.state.import` 三方法挂 store. 家族;store.items(及连带 feed.export JSONL)投影补三键(加法);PROTOCOL_VERSION 开工实读+1;协议档 mirror 加行+版本注记。
- R4 UI 切换:能力门(protocol ≥ 新版)分流通/旧;过门后服务端态为唯一真源,toggle/批量走 RPC(乐观更新+失败回滚);「全部标已读/未读」按钮语义升级为全库(title 换真话);未读计数/过滤随页内条目派生。
- R5 一次性导入:过能力门且本地 map 非空 → 单请求 `store.state.import`;服务端旗标幂等;localStorage 旧键保留不删,不设双写期。

## Acceptance Criteria

- [x] AC1 旧库升级:v7 库开箱自动迁移到 v8,三列+索引在位,既有行三态全 0(未读),schema_version=8;fresh 库直接建 v8 形状(两路径同形)。(协议迁移用例+store 层 test_read_state.py,收口全量 3585 绿内)
- [x] AC2 `store.state.mark`:按 dedup_key 置位,同 dedup_key 多行(dated-key 旋转)同置;marker/value 校验拒非法参数(invalid_params);返回 `{updated}` = 实改行数语义如实。(协议用例齐)
- [x] AC3 `store.state.mark_all`:全库单条 UPDATE;category 可选过滤与 store.items 同词;无 query 参数(决议钉死)。(协议用例+handler 参数面 grep 复核)
- [x] AC4 `store.state.import`:dedup_key 直配 / `id:<n>` 经 items.id→dedup_key 映射 / `id:<url>` 跳过计入 skipped;二次调用命中 `feed_state_imported_at` 旗标 = no-op(imported=0)。(协议用例齐)
- [x] AC5 store.items 应答与 feed.export JSONL 条目含 read/starred/later(加法,既有键不动);CSV 列集不变。(_item_dict 三键 entry.py:881-883/JSONL 同源 :1157/CSV 固定七列 :1151 复核+用例)
- [x] AC6 协议档 mirror:.trellis/spec/desktop/sidecar-protocol.md 注册表加三方法行 + 版本 bump 注记(按开工实读值);_HANDLERS 注册表数与档对账。(档 58-60 行/v10 竞速注记在位;grep `": _m_'` = 60 与档相等)
- [x] AC7 UI:过能力门后 toggle/星标/稍后读全部走服务端(乐观+失败回滚);「全部标已读/未读」= 全库语义,title 如实(不再写「已加载条目/本地态」);未过门(protocol < 新版,如旧 sidecar 配新 UI)旧 localStorage 通路照常。(vitest read-state-server 套件,350 全绿内)
- [x] AC8 一次性导入:模拟 v1 localStorage map(含三种 key 形态)导入后服务端态正确;旧键 `myia.feed.states.v1` 不被删除。(vitest 导入用例;现树键名 myssia.feed.states.v1 为改名波漂移,以现树为准)
- [x] AC9 语义明示:PRD 本档明写 starred/later 不豁免 retention 剪枝(见 Q4.2);「稍后读」随条目剪枝过期按无回归处理。(本档 Q4.2 在案)
- [x] AC10 未读过滤全库化(查询参数)不在本批:store.items 不加 read 过滤参数(范围钉死,防范围蠕变)。(_m_store_items 参数面 grep:仅 before/before_id/query/limit,无 read 过滤)

## Notes

- 决议证据链的行号为 grill 时实读;feed-screen.tsx 在改名波在途diff 中行号有漂移(grill 引 :807-814/:820,回写日工作树实际为 markAllRead 定义 :890-902、applyFeedFilter 调用 :903、批量按钮 title :1123-1141,语义一致),实现以现树为准。
- 本批不动:cleanup 剪枝策略(另立任务)、未读过滤查询参数(另立)、CSV 导出列(固定不动)。
