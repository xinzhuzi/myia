# 微信聊天记录查询与导出(C1)

## Goal

在已打通的桥 localdb 只读链(B0 分表适配已落,0.4.2 commit 19c606b)上,交付两件事:①**查询增强**——按会话的 keyset 分页(全量翻页)/时间窗/类型/发送者筛选,外加会话清单普查;②**六格式导出器**(JSON/TXT/CSV/Markdown/HTML/Excel)+ 取消安全的导出任务面;并把查询能力接成桌面微信工作台族的**浏览面数据通道**(sidecar 动作 + Tauri 命令 + TS api + 既有「只读会话入口」最小升级)。一切读写只落在解密副本(读)与用户指定目录/桥私有区(写),零微信进程干预、零写微信侧数据。

## 来源与依赖

- 蓝本:父档 `.trellis/tasks/10-13-wechat-features/prd.md` #8「消息导出」+ 子任务地图 C1 行;文案判例 AC-P5(「聊天记录」人话,协议/字段标准英文)。
- 开源调研定稿(工作流调研件,2026-10-14):
  - **产品语义锚 = hicccc77/WeFlow**(CC BY-NC-SA 4.0)——只借格式选项矩阵/任务控制/显示名优先级**语义,零借码**(SA 传染+NC 禁商,连改造借用都不做)。
  - **码基锚 = labazhou2024/chatlog-keeper**(MIT)——per-shard keyset 游标、`(create_time,rowid)` 双键谓词、显示名回退链 remark→nick_name→alias、private_text_writer(0600)语义;若直接借用代码片段,文件头带 MIT 归属注记。
  - **WeChatDataAnalysis**(无许可证)——只借思想:导出清单密封(sha256 manifest)。
- **B0 已落,无外部阻塞**:桥 0.7.0 现役(`plugins/wechat-bridge/wechat_bridge/__init__.py:22`、`component.json` version),4.1.15 分表适配(Msg_ 表识别/Name2Id 反解/real_sender_id/zstd 解码)在 `localdb_query.py:15-30`(0.4.2)。file 变体 localType(34359738417 等)是否在真库存在 = 本任务 R3 普查项,不是外部依赖。
- 数据资产:keys.json + E2 解密副本管道(`localdb.py` `ensure_decrypted_copies`,TTL/容量/源新即重建)已就位;真库锚 = TMS 群(50438708676@chatroom)。

## Requirements

### R1 keyset 分页查询通道(桥新命令 `localdb page`)

新文件 `plugins/wechat-bridge/wechat_bridge/localdb_page.py`:

- 谓词(chatlog-keeper 语义,自写实现):每 Msg_ 分表(经既有 `find_message_tables`+`colmap["chat"]` 选表,跨 message_0.db 与 biz_message_0.db 双库分片)`WHERE (create_time > ? OR (create_time = ? AND rowid > ?)) [AND create_time >= ? AND create_time <= ?] ORDER BY create_time, rowid <ASC|DESC> LIMIT ?`——翻页成本 O(页),严禁 OFFSET。
- **游标(不透明)**:base64(JSON `{"v":1,"chat_id","order","window":{"from_ts","to_ts"},"shards":{"<db相对路径>::<表名>":{"ts":<int>,"rowid":<int>}}}`)。**scope 守卫**:请求的 chat_id/order/window 与游标内不一致 → exit 2 用法错 `invalid_cursor`(防串会话/串窗口复用,chatlog-keeper 版本号+scope 校验语义)。首帧(无游标)= 从时间窗端点起取。
- **索引自举**:解密副本是桥私有产物,允许建索引——首次 page/export 时对涉及 Msg_ 表 `CREATE INDEX IF NOT EXISTS idx_<表名>_ct ON "<表名>"("create_time")`(SQLite 索引隐式追加 rowid 尾列,ORDER BY create_time,rowid 可整体命中);副本目录旁落标记文件(键=副本 mtime),副本重建(TTL/源新)后标记失效、下次自举重建;每次建后 `EXPLAIN QUERY PLAN` 断言 `SEARCH ... USING INDEX`(出现 `SCAN` 即测试失败)。
- **筛选**:CLI `--from-ts/--to-ts`(unix 秒;输入 >1e12 视毫秒除 1000、>1e15 视微秒除 1e6 归一,WeFlow 语义)、`--types text,image,…`(按 R3 类型名)、`--sender <wxid>`(按解析前原始 id 匹配)、`--asc/--desc`(缺省 desc=最新在前)、`--limit N`(缺省 200,CLI 帽 1000)。
- **应答契约**(stdout 单 JSON,键序即此):`{"page": {"chat_id", "display_name", "messages": [{"seq"(行 rowid), "ts", "sender", "sender_id", "type"(类型名), "local_type"(原值), "text"?, "placeholder"?}], "next_cursor"|"null", "has_more", "filter", "page_size"}}`——消息条目语义与既有 `query_messages` 同族(`localdb_query.py:341-357`):sender 经显示名链解析、`sender_id` 留原 wxid、非文本出占位不臆造。
- 编排:`localdb.py` 增 `page_history(config, db_storage, keys, chat_id, *, cursor, limit, asc, from_ts, to_ts, types, sender, data_root)`——E2 副本(域 `["message","contact"]`)→ 自愈钩子 → R1 查询,样板照 `query_history`(`localdb.py:1547-1598`)。

### R2 会话清单普查(桥新命令 `localdb conversations`)

同在 `localdb_page.py`:对全部识别出的 Msg_ 分表逐表 `SELECT COUNT(*), MIN(create_time), MAX(create_time)`(一次性普查,非逐页),表名 md5 经 Name2Id 反解 chat_id,显示名走既有 `_contact_pick_names` 批量链(`localdb_query.py:368`),`is_group = chat_id.endswith("@chatroom")`;按 `last_ts` 降序。应答:`{"conversations": [{"chat_id", "display_name"|"null", "is_group", "msg_count", "first_ts", "last_ts"}], "total"}`;`--limit N`(缺省 500)。反解不出的表(chat 不明)计入 `total` 但不入清单旁注 `unresolved_tables`(计数形状,不猜归属)。

### R3 类型普查 + 映射表扩展 + type-49 XML 人话化

- **真库普查(先行,只读)**:对解密副本各 Msg_ 表 `SELECT local_type, COUNT(*) GROUP BY local_type`,产出**形状计数件**(零聊天内容)`tests/wechat-bridge/fixtures/local_type_census.json` 作测试基线;与 WeFlow 映射表(localType 1/3/34/43/47/49/48/42/50/10000 + file 变体 49+34359738417/103079215153/25769803825)对拍,真库在场的变体进映射、不在场的不臆造。
- 扩展 `localdb_query.py` `MSG_TYPE_NAMES`(`localdb_query.py:61-71`):补真库实证变体(含大数 file 族 → `file`、42 → `card`、50 → `call`);未知仍回落 `type_<N>`(既有判例不变)。
- **type-49 XML→人话**(解析目标清单借 chatlog-keeper,MIT):纯 stdlib `xml.etree`,坏 XML/缺节点 → 原占位 + stats 计数(`wx_parse_failed`,如实降级判例)。产出行文案:
  - 链接卡(appmsg type=5):`【链接】{title} {description} {url}`
  - 引用(type=57):`{title}(引用:{refermsg 摘要≤50字})`
  - 合并转发(type=19 recordinfo):`【聊天记录】{displayname} 的 {N} 条消息`
  - 文件(type=6):`【文件】{title}({size 人话})`
  - 表情(47 XML desc 在场):desc,否则维持占位。
- 落点:`localdb_query.py` 新函数 `humanize_content(local_type, content) -> str`,R1 消息条目与 R4 导出共用(文本消息与 type-49 族产人话,其余类型维持「类型+占位」)。

### R4 六格式导出器(桥新命令 `localdb export`)

新文件 `plugins/wechat-bridge/wechat_bridge/localdb_export.py`:

- CLI:`localdb export <chat> --format json|txt|csv|md|html|xlsx --out <dir> [--from-ts/--to-ts](归一同 R1;`--since Nd` 糖) [--types] [--sender] [--display-name-pref remark-first|nickname-first] [--name-mode classic|date-range] [--all] --json`;`--all` = 全库导出,产物按会话分子目录 `<out>/聊天记录导出-<YYYYMMDD-HHMMSS>/<会话显示名或id>/`(每会话一文件,xlsx 亦按会话一簿)。
- 数据面 = R1 分页通道复用(同游标逐批,批 500);**禁全量载入内存**(JSON 用手写流式数组写出;xlsx 用 `xlsxwriter` `constant_memory=True`,pyproject 增纯 Python 依赖 `xlsxwriter`)。
- 格式规格:
  - **JSON**:单文件流式数组,元素 = R1 消息条目原形(含 seq/local_type/sender_id,零信息丢失)。
  - **TXT**:日分隔行 `—— YYYY-MM-DD ——`,消息行 `[HH:MM:SS] 发送者(类型名): 内容`;缺时间列 → 无日分隔如实。
  - **CSV**:表头 `time,sender,sender_id,type,content`;UTF-8 **带 BOM**(Excel 中文判例,`wechat_group_export.rs` 同款);**注入转义**:内容以 `= + - @` 或 tab 开头 → 前置 `'`(用真库实际出现数做用例)。
  - **Markdown**:二级标题按日,消息 `**发送者** · HH:MM:SS` + 内容引用块;特殊字符标准 md 转义。
  - **HTML**:**自包含单文件**——内联 CSS、零外链零脚本零远程请求,日分隔 + 左右气泡(自己/对方两侧样式语义,WechatExporter 模板外置思想不做,样式内联即定);全部插值 `html.escape`;HTML 源 `grep -E 'src=|href="http'` 零命中(内容原文里的 URL 照显,但非元素属性)。
  - **Excel(xlsx)**:列 = 时间/发送者/类型/内容;**单表行帽 1,048,576**(含表头)→ `Sheet2/Sheet3…` 顺延分表;阈值行为用夹具演练。
- **文件名**(双模式,WeFlow 语义):classic = `聊天记录-{显示名|chat_id}-{YYYYMMDD-HHMMSS}.{ext}`;date-range = `聊天记录-{显示名|chat_id}-{from}__{to}.{ext}`(from/to = `YYYYMMDD`);显示名过文件系统消毒( `[\\/:*?"<>|]` → `_`)。
- **显示名优先级**:`--display-name-pref` 两档——`remark-first`(缺省=既有链 remark>nickname>alias)/`nickname-first`(跳过 remark);群昵称档**不进本期**(4.1.15 副本可解性未验,如实不做)。
- 编排:`localdb.py` 增 `export_history(...)`(E2 域同 R1,自愈钩子同款)。

### R5 导出任务面:进度/取消/暂存/清单/隐私

- **进度 = key-acquire NDJSON 判例**(`localdb.py:52-59`、README:22):stdout = NDJSON progress 行 + 末行单 JSON 回执;节流 = 最小间隔 400ms 或增量 1200 条(先到即发),phase 切换(scan/write/每会话切换)强制发。progress 行形状 `{"progress": {"phase", "rows", "current_chat"?, "pct_est"?}}`;回执 = `{"export": {"chat_id"?, "display_name", "format", "files": [{"name", "path", "rows", "sha256"}], "manifest_path", "total_rows", "time_range"?, "elapsed_ms"}}`。
- **取消安全(暂存+原子落位,替代 WeFlow worker 协议)**:全部产物先写 `<out>/.wechat-export-staging-<pid>-<ts>/`,完成(含 manifest)后逐件 `os.replace` 到最终名;SIGTERM/异常 → staging 整目录清除,零半成品最终件(重跑即净);`--all` 每会话完成即落位(会话粒度提交)。
- **清单密封**(WeChatDataAnalysis 思想):`manifest.json` 最后写,含每件 sha256 + 导出选项回显 + 行数 + 时间范围;提供 `--verify <manifest路径>` 子动作重算对账。
- **隐私**:导出件与 manifest 落盘即 `0600`(chatlog-keeper private_text_writer 语义;`os.open` mode 位);聊天内容不入日志/报告——进度行只带计数与形状。

### R6 浏览面数据通道(sidecar + 壳 + TS + 最小 UI)

- **sidecar**(`src/myssia/wechat_local_sidecar.py`):`_ACTIONS`(`wechat_local_sidecar.py:199-204`)增 `"page"`(params `{chat_id, cursor?, limit?, asc?, from_ts?, to_ts?, types?, sender?}` → 桥 `localdb page`,超时走 `_QUERY_TIMEOUT_SECONDS` 族)与 `"conversations"`(`{limit?}` → `localdb conversations`)。导出**不走 sidecar**(常驻服务不该背长任务),走壳命令。
- **壳命令**(新文件 `desktop/src-tauri/src/wechat_chat_export.rs`,注册进 `main.rs` invoke_handler,判例 `wechat_group_export`):`wechat_chat_export {chat_id, format, out_dir?, from_ts?, to_ts?, types?, sender?, display_name_pref?, name_mode?, all?}`——`out_dir` 缺省时壳内 `open_dir` 对话框(取消 = 返 null 静默,群导出判例);spawn 桥 `localdb export`,NDJSON → Tauri 事件 `wechat-chat-export-progress`(判例 key-acquire `KEY_ACQUIRE_EVENT_NAME`);配套 `wechat_chat_export_cancel {job_id}` kill 进程组(壳内 job 表);回执原样转前端。**page/conversations 零壳改**(走通用 `sidecar_request`)。
- **TS api**:`desktop/ui-src/src/screens/messaging/api.ts` 增 `wechatLocalPage`/`wechatLocalConversations`(invoke `sidecar_request` method `wechat_local.page`/`wechat_local.conversations`,parse 守卫判例 `parseWechatGroupExportResult`);新文件 `desktop/ui-src/src/screens/messaging/wechat-chat-export-api.ts`(invoke `wechat_chat_export` + 进度事件订阅 + cancel 封装)。
- **最小 UI 升级**(`desktop/ui-src/src/screens/messaging/wechat-local.tsx` 只读会话入口,并入既有版式不新造画布):①「加载更早」按钮游标续拉(首帧 = 最新一页倒转上屏);②时间窗快捷档(7 天/30 天/全部 → from_ts);③导出行——格式下拉(六格式人话名:JSON 文件/纯文本/CSV 表格/Markdown/网页/Excel 表格)+ 目标目录选择 + 进度条 + 取消 + 回执路径列表。媒体预览、.dat 解密、仿微信气泡全画布 = **C3 边界,本档不做**。

### R7 版本与文档

桥 0.7.0 → **0.8.0** 三方同步:`pyproject.toml` version、`component.json` "version"、`wechat_bridge/__init__.py:22` `__version__`;README 命令表(`README.md:14-25`)增 `localdb page`/`localdb conversations`/`localdb export` 三行(判例 0.6.0 波 `59ff041`)。

## Acceptance Criteria

- [x] AC1 **keyset 等价 + 索引验真(真库,只读)**:TMS 群真副本上 `localdb page --limit 500` 全量翻页拼接 vs 单次 `ORDER BY create_time,rowid` 全量查询,序列与总条数一致;`EXPLAIN QUERY PLAN` 输出含 `SEARCH … USING INDEX`(零 `SCAN`);命令与输出留档本档 `research/`。
- [x] AC2 **真库类型普查落基线**:各 Msg_ 表 `GROUP BY local_type` 形状计数(零内容)产出 `tests/wechat-bridge/fixtures/local_type_census.json`;映射表对真库在场的类型全覆盖,未知回落 `type_<N>` 的行占比记录在档。
- [x] AC3 **六格式真跑一致**:单会话真库六件全产——JSON 条数 == 同过滤 SQL `COUNT(*)`;CSV 注入转义(真库 `=+-@` 开头内容用例);HTML 断网可开、源码 `grep` 零外链元素属性、内容插值全转义;xlsx 分表行为(夹具演练 1,048,576 帽);manifest sha256 全对(`--verify` 过)。
- [x] AC4 **导出中断安全**:真跑中途 SIGTERM → staging 清空、零半成品最终件;原目录重跑成功落位;`--all` 下已完成的会话件保留。
- [x] AC5 **翻页延迟预算**:346MB 副本大会话游标位 0/100/1000 各取页,p95 ≤ 2s(命令与耗时留档)。
- [x] AC6 **显示名与占位如实**:浏览/导出条目显示名 remark 优先;解析不出的发送者保留 wxid;非文本消息「类型+占位」不臆造;type-49 人话化覆盖链接/引用/合并转发/文件四形,坏 XML 计数降级。
- [x] AC7 **浏览面通道端到端**:桌面只读会话入口真机走通——最新页加载 +「加载更早」续拉 + 时间窗过滤 + 六格式之一导出回执路径可打开;vitest(`wechat-local.test.tsx` + 新 api 测试)全绿。
- [x] AC8 **版本与文档**:0.8.0 三方同步,README 命令表 +3。
- [x] AC9 **红线守卫**:零微信进程干预、零写微信侧数据(grep 守卫:源库路径零 WRITE/INSERT/UPDATE/DELETE);导出件/manifest 0600;聊天内容零入 git/日志/报告(夹具全合成数据)。

> **复查回执(2026-10-14 复查员实跑,判定 PASS/needsFix=false)**:① real_check 真跑 `.venv/bin/python .trellis/tasks/10-14-wechat-chat-export/research/real_check.py` → rows=9821 pages=20 keyset_sequence_equal=True census_mapping_consistent=True RESULT: PASS(脚本全程 mode=ro,localdb_query.py:247);② pytest 两件 33 passed;③ vitest 两件 27 passed(前轮回执 23,集成后增量,全绿);④ cargo test wechat_chat_export 5 passed 0 failed(main.rs:932 现役注册下真跑);⑤ 前轮回执遗留 AC3/AC4/AC5 本轮全部补真跑:六格式真库导出(TMS 30d 窗)各 3391 行==同窗 SQL COUNT 3391、CSV 28 行注入转义、HTML grep 'src=|href="http' 零命中、manifest --verify ok=true exit=0、产物/manifest 全 0600;SIGTERM 中途杀 --all 导出→error export_cancelled、staging 目录零残留、已完成会话件保留;翻页 p95(行位 0/100/1000×5 采样)≤0.08s≪2s;索引在场 EXPLAIN=SEARCH USING COVERING INDEX idx_Msg_3aec..._ct;README.md:26-28 命令表 +3、桥 0.8.3;红线 grep 两模块 INSERT|UPDATE|DELETE|db_storage 零命中;ruff(0.17.0)两件 All checks passed(回执缺口已闭)。
>
> **留档发现**:[low] 成功路径 staging 目录不清理——六次成功导出后 /tmp/myia-review-c1 残留六个空 .wechat-export-staging-<pid>-<ts>/ 目录,localdb_export.py:810 的 rmtree 仅在 except 分支,成功落位后目录本体遗留(PRD R5 仅强制 SIGTERM/异常清理,不构成 AC 违例,建议顺手修);[info] 前回执称 main.rs「已还原,git 零 diff」,当前树 main.rs:15/932-933 已注册 wechat_chat_export(16 insertions)——与 cli.py 已接线、版本 0.8.3 同证系并行集成会话落位,非缺陷;[info] 05:38-05:39 两次观察到真副本 TMS 表 transient 'no such table'(db mtime 全程 05:37:43 未变,05:39:44 复查在场 9821 行+索引)——未复现,最可能为并行会话 E2 副本重建/建索引竞态窗口,无确证产品缺陷,留档知会。

## Constraints

- **只读红线**:一切查询读解密副本;唯一写动作 = 桥私有区副本索引自举 + 用户指定目录导出件。
- **许可红线**:WeFlow(CC BY-NC-SA)与 WeChatDataAnalysis(无许可)**零码借**;chatlog-keeper(MIT)借码须文件头 MIT 归属注记。
- **规模红线**:346MB 库严禁逐页全表扫(R1 索引自举 + EXPLAIN 断言);导出严禁全量入内存(流式)。
- **文案判例**:UI 全人话(「聊天记录」「加载更早」),CLI/协议字段标准英文(`from_ts`/`next_cursor`)。
- 版式:并入既有微信工作台族(wechat-local.tsx 分区卡),不新造画布。

## 边界注记(与兄弟档)

- C2 统计报告:消费本档 R1/R2 通道;聚合 SQL 属 C2 自建。
- C3 媒体与朋友圈:浏览面媒体预览 + .dat 解密 + 导出件媒体内嵌归 C3(本档非文本=占位行);仿微信全画布浏览面归 C3(父档总表 #1 行)。
- C4 联系人:contact 导出走群导出先例(wechat_group_export),与本档消息导出分立。
- C5 通知撤回:轮询水位可复用 R1 谓词;撤回呈现消费 R3 类型映射(10002 已映射)。
- C6 HTTP API:将把本档三命令映射 HTTP,契约以本档 CLI 为准。
