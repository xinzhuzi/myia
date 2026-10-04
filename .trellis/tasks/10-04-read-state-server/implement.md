# implement:G9 服务端已读态 + 全库批量已读 + localStorage 一次性迁移

前置:prd.md(Grill 决议 Q1-Q4 = 裁决基准)、design.md(§1-§7)。每步做完打勾并记一行实测命令+结果;
定向门禁本会话自跑,全量门禁归脚本;**不 push、不 task.py start/finish(收口员直改 task.json)**。
行号以开工当日现树为准(设计日行号已注,改名波在途会漂)。

## 步骤

- [x] **0. 开工实读(必做不可跳,design §4.5/§6.1 基线)**
  - `grep -n "PROTOCOL_VERSION = " desktop/entry.py` 取现值 → 本批版本 = 现值+1(设计日 8→9;若 hermes-cron 已合入则顺延,记入步骤 3);
  - `grep -c '"[a-z.]*": _m_' desktop/entry.py` 或数 `_HANDLERS` 注册行 → 本批后预期 +3;
  - `git status --porcelain -- src/myia/store/ desktop/entry.py desktop/ui-src/src/screens/feed/ desktop/ui-src/src/lib/api/` 读在途改动,只追加不重排;
  - 核对 `SCHEMA_VERSION = ` 现值 = 7(src/myia/store/sqlite.py:83)。
    实测(2026-10-04,三流开工实读回执汇总):PROTOCOL_VERSION=9(hermes-cron 已先合入 v9,竞速顺延)→ 本批 10;_HANDLERS=57 → 60;SCHEMA_VERSION=7;在途 diff=改名波残痕+他流 runs.trend 件(与本批编辑点零重叠;协议件曾等 22 分钟至 513eb11 落地后才动手)。收口复核现树:entry.py:456 `PROTOCOL_VERSION = 10`、`_HANDLERS` 注册 60 行、sqlite.py:88 `SCHEMA_VERSION = 8`,三方与档注记一致。

- [x] **1. 表结构 + 迁移(design §1 §2)**
  - sqlite.py:`_SCHEMA` items DDL 尾部加三列 + `idx_items_dedup_key`(放 idx_items_category 后);`SCHEMA_VERSION = 8`;
  - `_migrate_v7_add_alerts`(:352)后落 `_migrate_v8_add_item_states`(docstring 抄 design §2.1 草稿);`_MIGRATIONS` 加 `8:`;
  - models.py `ItemRecord` 加 read/starred/later 三 bool 字段(design §1.2);
  - `_row_to_item`(:452)加三行映射;**save_item 不改**(design §1.4 明确不改点)。
  - 定向:`python -m pytest tests/test_feedback.py -q`(迁移注册不破既有 v3→v4 链)。

- [x] **2. store 层三方法(design §3)**
  - sqlite.py items 节:`set_item_states` / `set_all_item_states` / `import_item_states`,docstring 抄 design §3 契约(按键置位红线/rowcount 口径/key 三分/整键覆盖语义全写明);
  - marker 白名单字典映射列名(防注入);`_lock` + commit 同 save_item 纪律。
  - 定向:覆盖走协议测试(步骤 6,b234「无独立单测」同门)。

- [x] **3. 协议 handler + 版本(design §4)**
  - entry.py:`_m_store_state_mark` / `_m_store_state_mark_all` / `_m_store_state_import` 落 `_m_store_items` 后,节注释 `# 方法:store.state.mark / mark_all / import(G9 读态迁服务端,10-04-read-state-server)`;
  - import handler 首行 `get_meta("feed_state_imported_at")` 已设即 no-op 应答;未设导入后 `set_meta`(ISO 时间戳);
  - 校验:marker 枚举/value bool/keys 非空且 ≤2000/states 形态,invalid_params + path(抄 _m_store_items :790-806 风格);db 缺省同收口;
  - `_HANDLERS` 三行紧跟 `"store.items"`;`PROTOCOL_VERSION` = 步骤 0 实读值 +1,版本注释追加 v9 行(design §4.5 草稿);
  - `_item_dict`(:739-787)追加 read/starred/later 三键(bool 投影);模块 docstring 方法表 + store.items 契约段补行;CSV 列集不动(:934)。
  - 定向:`python -m pytest tests/test_desktop_sidecar_protocol.py -q`。

- [x] **4. 协议档 mirror(design §4.5)**
  - .trellis/spec/desktop/sidecar-protocol.md:注册表加三方法行(参数/应答/错误码);分组注记段追加 read-state-server 批一行(含 store.items 投影三键 + feed.export JSONL 加法注记 + 竞速顺延条款);版本 bump 注记;
  - 对账:档内方法行数 == `_HANDLERS` 实数(implementer 记两数)。

- [x] **5. UI:api 层 + 能力门 + 导入(design §5.1/§5.3)**
  - feed/api.ts:`READ_STATE_PROTOCOL = <步骤 3 版本>` 常量;`statesFromItems` 纯函数;mark/markAll/importState 三 RPC 封装(client.ts api 面板加行,types.ts 补类型 + FeedItem 三可选键);
  - 能力门:挂载时 `api.version()`,失败/低版本走旧通路(旧通路代码零改动);
  - 导入:map 非空 → 单请求 import,模块级布尔防双调;**旧键不删**(loadFeedStates/saveFeedStates 保留)。
  - 定向:`cd desktop/ui-src && npx vitest run src/screens/feed`。

- [x] **6. UI:feed-screen 切换(design §5.2)**
  - states 源切换:过门后 `statesFromItems(items)` 喂既有 applyFeedFilter/toggleMarker(管线函数零改动);toggle → `store.state.mark` 乐观+失败回滚;
  - 批量按钮:markAllRead 改发 `store.state.mark_all`(全库),title 换全库真话(现 :1123-1141 注记作废);就地翻转已加载行,不整页重拉;
  - `grep -n "setMarkerBulk" desktop/ui-src/src -r` 核实过门后死支,保留不删(design §5.4),注记在案。

- [x] **7. 测试补齐(design §6 清单)**
  - 协议 pytest 10 用例(§6.1 编号 1-10,迁移用例抄 tests/test_feedback.py:248 形状);
  - vitest 5 组(§6.2:statesFromItems/乐观回滚/mark_all/title/能力门/导入触发)。

- [x] **8. 全量门禁(收口)**
  - `python -m pytest tests/ -q` 全绿;
  - `cd desktop/ui-src && npm test` 全绿;`npm run build`(tsc 类型门)过;
  - `git diff --stat` 复核只动白名单文件(sqlite.py/models.py/entry.py/协议档/feed 三件套/types.ts/client.ts/测试)。

  收口实测(2026-10-04,收口员会话,repo 根执行):
  - `.venv/bin/python -m pytest tests/ -q` = **3585 passed, 19 skipped in 86.45s**(系统 python 缺 feedparser 走项目 venv;含 tests/test_desktop_sidecar_protocol.py + tests/test_read_state.py 定向 = 157 passed);
  - `cd desktop/ui-src && npm test` = **Test Files 21 passed (21),Tests 350 passed (350)**(feed-screen 69 用例含 read-state-server 新套件);
  - `cd desktop/ui-src && npm run build` = tsc -b + vite **✓ built in 1.53s**(>500kB chunk 警告为既有提示非失败;构建产物落 desktop/ui/ 未染 tracked 树);
  - `git diff --stat`(本批 9 文件)= 1096 insertions/36 deletions,全落白名单:spec 协议档/entry.py/UI 六件/协议测试;store 件(sqlite.py/models.py/CHANGELOG)已被改名流 513eb11 `git add -u` 先行收编入库,现树 clean;
  - 白名单外脏件均已隔离不收编:10-03-v12-backlog/prd.md、fe-gap-census/matrix.md(他任务)、myia.db(v6 旧形状残留,见收口注记)。

## 完成定义

prd AC1-AC10 逐条可勾;两份 jsonl(implement/check)策填在案;协议档与 `_HANDLERS` 对账数相等;
PROTOCOL_VERSION/SCHEMA_VERSION 与档注记三方一致。
