# design:G9 服务端已读态(三列)+ 全库批量已读 + localStorage 一次性迁移

对应 prd.md R1-R5 / AC1-AC10;裁决基准 = prd「Grill 决议(2026-10-04)」Q1-Q4。
本文行号为设计当日(2026-10-04)工作树实读;开工步骤 0 重读刷新。
零 GUI:全部验证走协议 pytest + vitest(jsdom),无头可全证(b234 同款)。

## §0 决议映射(哪节落实哪条)

| 决议 | 落实节 |
|---|---|
| Q1 items 三列 + idx_items_dedup_key + SCHEMA_VERSION 8 | §1 §2 |
| Q1.3 按 dedup_key 置位(同键多行同置) | §3.1 §4.1 |
| Q2 一次性导入 + 服务端旗标 + 旧键不删 | §3.3 §4.3 §5.3 |
| Q3 三方法挂 store. 家族 + 投影三键 + 版本实读+1 | §4 |
| Q4 三态一次全迁 + retention 不豁免(明写) | §1 §5 §7 |

## §1 表结构(Q1)

### 1.1 DDL(items 表,`src/myia/store/sqlite.py` `_SCHEMA`,现 :87-121)

```sql
-- items 表尾部追加(push_slot 之后、raw 之前或之后均可,取尾部整段清晰):
    read INTEGER NOT NULL DEFAULT 0,      -- 1 = 已读(G9;0/1,与协议层 bool 互转)
    starred INTEGER NOT NULL DEFAULT 0,   -- 1 = 星标(策展态,同 retention 剪枝,PRD Q4.2)
    later INTEGER NOT NULL DEFAULT 0      -- 1 = 稍后读(同上;随条目剪枝会静默过期,明示)
```

新索引(_SCHEMA 内、idx_items_category 之后):

```sql
CREATE INDEX IF NOT EXISTS idx_items_dedup_key ON items(dedup_key);
```

- 三列 `NOT NULL DEFAULT 0`:新条目 = 未读/无星/无稍后读,语义即缺省;SQLite `ALTER TABLE ADD COLUMN ... NOT NULL DEFAULT 0` 合法(常量缺省免 rewrite 全表,SQLite 文档语义,实施时以迁移测试实证)。
- `idx_items_dedup_key` 动机:置位走 `WHERE dedup_key IN (...)`,现无索引全表扫(Q1.4);feedback 表同款先例 sqlite.py:180。非 UNIQUE——dated-key 旋转下同键多行是合法状态(sqlite.py:756-768 docstring)。

### 1.2 models(`src/myia/store/models.py` ItemRecord,现 :109-125)

```python
    read: bool = False       # G9 服务端读态(库列 0/1;新条目缺省 False)
    starred: bool = False    # 星标(策展;retention 剪枝不豁免,PRD Q4.2)
    later: bool = False      # 稍后读(同上)
```

字段位置:数据类字段顺序无关紧要,放 `raw` 之后、`id` 之前与既有可选列风格一致。

### 1.3 行映射(`sqlite.py:452-468` `_row_to_item`)

追加三行:`read=bool(row["read"])` / `starred=bool(row["starred"])` / `later=bool(row["later"])`。
`list_items`(:793-829)与 `get_item*` 均 `SELECT *` + `_row_to_item`,加列即通,无其它改动点。

### 1.4 save_item 不改(明确不改点)

`save_item`(:719-742)INSERT 列清单不含三列 → 新入库行三态全 DEFAULT 0(未读)。**这是语义**:采集管线永不携带读态,读态只由协议面置位。管线侧(collect/dedup/aggregate)零改动。

## §2 迁移(Q1.5)

### 2.1 `_migrate_v8_add_item_states`(sqlite.py,`_migrate_v7_add_alerts` :352 之后)

```python
def _migrate_v8_add_item_states(conn: sqlite3.Connection) -> None:
    """v7 → v8: add ``items.read/starred/later`` + ``idx_items_dedup_key`` (G9 读态迁服务端).

    Idempotent: fresh v8 databases already created the columns & index via
    ``_SCHEMA``; legacy v7 databases get them here. Existing rows keep the
    DEFAULT 0 (unread) -- 迁移不猜测读态,首切由 store.state.import 搬运
    localStorage 快照(Q2)。dedup_key 索引非 UNIQUE:dated-key 旋转下同键
    多行合法,置位按键同置(Q1.3)。
    """
    columns = {str(row[1]) for row in conn.execute("PRAGMA table_info(items)").fetchall()}
    if "read" not in columns:
        conn.execute("ALTER TABLE items ADD COLUMN read INTEGER NOT NULL DEFAULT 0")
    if "starred" not in columns:
        conn.execute("ALTER TABLE items ADD COLUMN starred INTEGER NOT NULL DEFAULT 0")
    if "later" not in columns:
        conn.execute("ALTER TABLE items ADD COLUMN later INTEGER NOT NULL DEFAULT 0")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_items_dedup_key ON items(dedup_key)")
    logger.info("存储迁移完成: items 表新增 read/starred/later 三列 + idx_items_dedup_key(G9)")
```

逐列独立 if(PAGMA 幂等检查,v2 先例 :232-242):三列 ALTER 中断后重开可续,不要求原子批。
注册:`_MIGRATIONS`(:400-406 字典)加 `8: _migrate_v8_add_item_states`;`SCHEMA_VERSION = 8`(:83)。

### 2.2 既有行语义

v7 存量行迁移后三态全 0(未读)——**迁移不猜测读态**;用户既有读态在 localStorage,由 §5.3 一次性导入补齐。已剪枝条目(不在 items 表)的本地键导入时自然落空(import 应答如实,不复活条目)。

## §3 store 层方法契约(新增三方法 + 旗标,sqlite.py items 节)

### 3.1 `set_item_states`——按键置位(store.state.mark 的底座)

```python
def set_item_states(self, dedup_keys: list[str], marker: str, value: bool) -> int:
    """置位一批 dedup_key 的读态标记(G9,store.state.mark 底座)。

    marker ∈ {"read", "starred", "later"};UPDATE items SET <marker> = ?
    WHERE dedup_key IN (...) —— 同键多行(dated-key 旋转)同置,与 localStorage
    itemKey 语义一致(Q1.3);幂等(显式置目标值,无读-改-写)。
    Returns: 实改行数(rowcount;含本已同值行?否——SQLite UPDATE rowcount 计
    匹配行,如实回传不另算)。
    ValueError: marker 非法 / dedup_keys 空 / 含空串。
    """
```

- 实现要点:marker 白名单字典防 SQL 注入(列名不可参数化,`{"read": "read", ...}` 显式映射);`IN` 占位符按长度展开;`self._lock` + commit 与 save_item 同纪律。
- rowcount 口径如实:SQLite `UPDATE ... WHERE` 的 rowcount = 匹配行数(SQLite 语义: changed rows 直连模式默认返回匹配数),不做「实改值」二次核算——协议应答 `updated` 即此数,docstring 明写口径。

### 3.2 `set_all_item_states`——全库单 UPDATE(store.state.mark_all 底座)

```python
def set_all_item_states(self, marker: str, value: bool, category: str | None = None) -> int:
    """全库(可选 category)置位(G9,store.state.mark_all 底座)。

    单条 UPDATE items SET <marker> = ? [WHERE category = ?];category 词义与
    list_items 同参(精确等值,非 LIKE;不收 query——决议 Q3.2 钉死)。
    Returns: rowcount。ValueError: marker 非法 / category 空串(与 list_items 同校验)。
    """
```

### 3.3 `import_item_states`——一次性搬迁(store.state.import 底座)

```python
def import_item_states(self, states: dict[str, dict[str, bool]]) -> tuple[int, int]:
    """导入 localStorage 读态快照(G9,Q2 搬迁门;幂等旗标在调用方 handler)。

    key 三分(Q2.4):dedup_key 直配;`id:<n>` 先 SELECT dedup_key FROM items
    WHERE id=<n> 取键(取不到 = 跳过);`id:<url>` 及任何无从解析形态 = 跳过。
    每键单条 UPDATE(三列合并一条:UPDATE items SET read=?, starred=?, later=?
    WHERE dedup_key = ?;缺省态继承现有列值——只覆盖快照中出现的键)。同键
    多行同置(与 3.1 同红线)。
    Returns: (imported=有匹配行的键数, skipped=无匹配/无法解析的键数)。
    幂等性由 handler 侧 store_meta 旗标保证;本方法本身可重复调用(重放 =
    再覆盖,故旗标必须先行,见 §4.3)。
    """
```

- 覆盖语义:导入 = 快照值覆盖服务端列(仅快照中出现的标记键;三键全缺省的 `{}` 值条目跳写)。设计取舍:**整键覆盖**而非逐键合并——快照是 v1 期唯一真源,合并无信息可合。
- 规模:逐键 UPDATE 在事务内单连接提交;v1 map 量级 = 用户点过的条目数(百级典型),N 键 N 条 UPDATE 一次 commit,可接受;不引入批量 CASE WHEN(复杂度不匹配量级)。

### 3.4 旗标(既有设施,零新增代码)

`feed_state_imported_at` = ISO 时间戳,`get_meta`/`set_meta`(:683-696)现成;handler 首行检查,已设即 no-op 应答。

## §4 协议面(desktop/entry.py)

### 4.1 `store.state.mark`(Q3.1)

```
方法: store.state.mark
参数: {db?: str, keys: [dedup_key, ...], marker: "read"|"starred"|"later", value: bool}
应答: {updated: <int>}
错误: invalid_params — keys 非非空数组/含非字符串或空串;marker 不在枚举;
      value 非 bool;keys 超上限(见下)。
```

- 校验口径抄 `_m_store_items`(:790-806)既有风格(逐字段 ProtocolError invalid_params + path)。
- keys 上限 **2000**(防御性常量):mark 的作用域 = 单键 toggle 与已加载批量(一页 50/limit ≤200),整库语义必须走 mark_all——上限是误用防线不是容量声明,超限 invalid_params 提示走 mark_all。
- db 参数缺省同 store.items 收口(默认库解析先例 :868-872)。

### 4.2 `store.state.mark_all`(Q3.2)

```
方法: store.state.mark_all
参数: {db?: str, marker: 同上枚举, value: bool, category?: str}
应答: {updated: <int>}
约束: 无 query 参数(决议 Q3.2 钉死,LIKE 进 UPDATE 是范围蠕变)
```

### 4.3 `store.state.import`(Q3.3 / Q2)

```
方法: store.state.import
参数: {db?: str, states: {<key>: {read?: bool, starred?: bool, later?: bool}}}
应答: {imported: <int>, skipped: <int>}
幂等: handler 首行 get_meta("feed_state_imported_at");已设 → {imported: 0, skipped: 0}
      不触库(服务端旗标是唯一真相,Q2.2——localStorage 旗标会被 webview 清数据击穿);
      未设 → import_item_states(...) + set_meta(时间戳)。
```

### 4.4 store.items / feed.export 投影补三键(Q3.4 / Q1.6)

`_item_dict`(:739-787)返回字典追加:

```python
        "read": bool(item.read),
        "starred": bool(item.starred),
        "later": bool(item.later),
```

连带面(feed/export 共用同一投影,entry.py:940):

- **feed.export JSONL 多三键**——加法变化,协议档 mirror 记注(Q1.6 如实注记);
- **CSV 固定列集不变**(:934 `csv_columns` 明确不动);
- 模块 docstring 方法表 + store.items 契约段各补一行(样式抄 b234 runs.trend 先例)。

### 4.5 注册与版本(Q3.5)

- `_HANDLERS`(注册表 :4092-4094 起)加三行,紧跟 `"store.items"` 之后(家族聚簇);预期 48 → 51(开工以步骤 0 实读为准)。
- `PROTOCOL_VERSION`:**开工实读现值 + 1**(设计日 = 8,entry.py:379 → 本批 9);hermes-cron 批竞速按 alert-rules 先例「按合入顺序定案,开工实读」(sidecar-protocol.md:86-87)。版本注释追加一行:`#: v9 = read-state-server 批(store.state.mark/mark_all/import 三方法 + store.items 投影补 read/starred/later;G9,10-04-read-state-server)。`
- 协议档 mirror(.trellis/spec/desktop/sidecar-protocol.md):注册表加三行 + 分组注记段追加本批一行 + 版本 bump 注记(含「若 hermes-cron 先合入则顺延 +1」竞速条款)。

### 4.6 handler 实现纪律

- 每方法独立 `_m_store_state_mark` / `_m_store_state_mark_all` / `_m_store_state_import`,落 `_m_store_items` 之后;每请求 `SQLiteStore(db)` 独立连接 + try/finally close(:790-806 同款);StoreSchemaError → ProtocolError(exc.code, str(exc), path="params.db")同款。
- store 层 ValueError → ProtocolError("invalid_params", str(exc), path="params")同款(:804-806)。

## §5 UI 切换(desktop/ui-src)

### 5.1 能力门(Q2.1)

- feed 屏挂载时一次 `api.version()`(client.ts:154-155 现成;或复用 `useSidecarStatus().info.protocol`,hook 已暴露 use-sidecar-status.ts:35-41——取直调 `api.version()`,不引入全局 hook 依赖,失败即按未过门处理)。
- `protocol >= <本批版本常量 9>` → 服务端态通路;否则(protocol < 9 或 version 调用失败)→ 旧 localStorage 通路**原样保留**(旧 sidecar + 新 UI 组合可用,AC7)。常量单点定义(如 `feed/api.ts` 导出 `READ_STATE_PROTOCOL = 9`,与后端实读值同步)。

### 5.2 状态源与操作通路(过门后)

- **读**:states 不再从 localStorage 派生,改由页内条目派生——`store.items` 应答每条带 read/starred/later(§4.4),`FeedItem` 类型(types.ts)补三可选键;`FeedStateMap` 兼容层:`statesFromItems(items)` 纯函数(现 FeedStateMap 形状,喂既有 applyFeedFilter/toggleMarker 渲染管线不动)——最小改动面策略。
- **toggle(单键)**:前端算好目标 value(现 toggleMarker 已算),发 `store.state.mark {keys:[itemKey(item)], marker, value}`;乐观更新(本地条目立即翻),失败回滚 + 既有错误 toast 路径。
- **批量(全部标已读/未读)**:`store.state.mark_all {marker:"read", value}`——**全库语义,不再按已加载条目置位**;按钮 title 换真话(现 :1123-1141「作用域 = 已加载条目…本地态,未翻页条目不含」注记作废,改「全库所有条目(含未翻页)」);本地条目同步翻转(已加载行即时反馈),成功后可轻量 refresh 或就地置位(就地置位,避免整页重拉)。
- **未读计数/过滤**:`applyFeedFilter`(feed-screen.tsx:903 调用)输入改服务端派生 states,逻辑函数本身零改动;计数随页内条目派生(Q3.4:全库未读计数不在本批)。

### 5.3 一次性导入(Q2)

流程(feed 屏挂载、能力门已过、每会话至多一次):

1. `loadFeedStates()` 读旧 map(键 `myia.feed.states.v1`,api.ts:166-179);
2. map 非空 → 单请求 `store.state.import {states: map}`(整 map 一个请求,Q2.1;逐键 RPC 否);
3. 应答 `{imported, skipped}` 仅记日志/调试面,不弹窗(搬迁对用户透明;skipped = id:<url> 形态如实计数,Q2.4);
4. **旧键保留不删**(Q2.3 回滚路径:降级旧 build 读旧快照照常工作,丢 v2 期增量可接受且如实);
5. 重复调用安全:服务端旗标 no-op 兜底(Q2.2 根本理由:webview 数据可被独立清掉,客户端旗标不可信)。

前端会话内去重:模块级布尔(防 React StrictMode 双挂载双调);不做 localStorage 旗标(决议否掉,服务端才是真相)。

### 5.4 本地代码去留

`loadFeedStates`/`saveFeedStates`/`toggleMarker`/`setMarkerBulk`(api.ts:166-230)**保留**:未过门通路(5.1)继续用;`setMarkerBulk` 在过门后不再被调用(批量走 mark_all)——死代码不删(未过门通路仍引用 loadFeedStates/saveFeedStates/toggleMarker;setMarkerBulk 若确认仅批量按钮用,过门后成死支,本批保留不删,防止未过门组合回归,实现时以 grep 引用核实)。

## §6 测试面

### 6.1 协议 pytest(tests/test_desktop_sidecar_protocol.py,新增 ~10 用例)

1. **迁移**:v7 库手造(store_meta schema_version=7 + 旧形状 items 表)→ 任一协议方法开库 → 三列+索引在位、行保留、schema_version=8(test_feedback.py:248 v3→v4 同款形状);
2. fresh 库直建 v8(两路径同形,AC1);
3. `store.state.mark` 单键置位 → store.items 应答 read=true(投影联通);
4. **同 dedup_key 多行同置**(dated-key 旋转手造两行同键,AC2 红线);
5. `store.state.mark` 非法 marker/value/空 keys/超 2000 → invalid_params;
6. `store.state.mark_all` 全库置位(计数=全库行数)+ category 过滤(只置该类);
7. `store.state.import` 三形态:dedup_key 直配置上 / `id:<n>` 映射置上 / `id:<url>` 计 skipped(AC4);
8. `store.state.import` 二次调用 no-op(imported=0,旗标在 store_meta 可直查);
9. store.items + feed.export JSONL 含三键、CSV 列集不变(AC5,抄 :390-482 store.items 测试形状);
10. `entry.PROTOCOL_VERSION == 9`(与实读基线,步骤 0 记录值) + `_HANDLERS` 计数对账(51)。

### 6.2 vitest(desktop/ui-src,`npm test`)

- `statesFromItems`:条目三键 → FeedStateMap 形状(缺省全 false 不产键,与 loadFeedStates 缺省语义对齐);
- toggle 乐观+失败回滚(mock api.mark 抛错 → 条目态回翻、错误上抛 toast 路径);
- mark_all 按钮:点击发 `store.state.mark_all`(不按已加载 keys)、title 文案含全库语义、不再含「本地态/未翻页」;
- 能力门:protocol=9 走服务端通路(不写 localStorage);protocol=8/调用失败走旧通路(写 `myia.feed.states.v1`);
- 导入触发:map 非空 + 过门 → 单次 `store.state.import`(StrictMode 双挂载只一发);map 空 → 不调。

### 6.3 门禁命令(全量,收口跑;定向随步)

```
python -m pytest tests/test_desktop_sidecar_protocol.py tests/test_feedback.py -q   # 协议+迁移回归
python -m pytest tests/ -q                                                          # 全量后端
cd desktop/ui-src && npm test                                                       # 全量前端
cd desktop/ui-src && npm run build                                                  # tsc -b 类型门
```

## §7 风险 / 回滚 / 竞速

| 风险 | 处置 |
|---|---|
| hermes-cron 批先合入抢 v9 | 开工实读 PROTOCOL_VERSION,本批 = 实读+1;协议档注记顺延条款(alert-rules 先例 sidecar-protocol.md:86-87) |
| 旧 sidecar + 新 UI | 能力门分流,旧 localStorage 通路原样保留(§5.1) |
| 新 sidecar + 旧 UI | 协议加法(store.items 多三键),旧 UI 忽略新键,零回归 |
| 降级回滚(新→旧 build) | 旧键未删,旧 build 读旧快照照常(丢 v2 期增量,明示可接受,Q2.3) |
| starred/later 随剪枝消失 | 无回归(今天同样丢,且本地键成死重永不自清);PRD Q4.2 明写;豁免另立任务 |
| import 重放倒灌 | 服务端旗标 no-op,重放不可能(Q2.2);旗标在 store_meta 与库同寿命 |
| 迁移中断续跑 | 逐列独立幂等 if(§2.1),重开即续 |
