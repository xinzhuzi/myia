# 微信统计与报告:私聊/群聊/年度/双人四类分析 + AI 报告 + 导出

## Goal

在桥 localdb 只读原语上净室实现四类统计分析(私聊/群聊/年度/双人),UI 挂微信工作台族「统计报告」分区,AI 叙事报告走 MYIA 既有 LLM 管线(缺省 glm-5.3-flash),产物(JSON 统计树 + AI 报告 Markdown)可导出落盘。**桥侧纯 SQL 零出网零 AI;AI 面、UI 面、导出面全在 MYIA 侧。**

参照系纪律(开源调研 10-14 定锚):主锚 hicccc77/WeFlow(★15052,活跃)为**仅设计参照**——其 LICENSE=CC BY-NC-SA 4.0(NC+SA 与 MIT 完全不兼容,比 GPL 更禁抄),**零抄码**;指标语义(年度 17 族/双人对照/会话/响应速度)与「一次聚合出一棵 JSON 树」「文件缓存+副本代次键」的形态可借,全部 SQL 在 MYIA 自己的 `localdb_query` 原语上重写。法律气候注记(chatlog 墓碑化 2025-10、wechat-dump-rs 被 DMCA 2026-01):统计码虽是纯 SQL,仍留在桥组件内,不散装进产品码。

## 数据事实与既有件(实锚,全部复用不重做)

- **E1→E2→E3 全链已通**:`localdb.resolve_keys` → `ensure_decrypted_copies` → 查询层;编排判例 `localdb.py:1656 group_info`(域收缩版),统计照此加 `stats_history`(域=`["message","contact"]`)。
- **4.1.15 分表已适配(B0,0.4.2)**:消息库按会话分表 `Msg_<md5(username)>` 无会话列;`localdb_query.py:147 find_message_tables`(表名 md5 反解挂 `colmap["chat"]`)、`:122 name2id_maps`(`Name2Id(user_name,is_session)`,rowid→wxid + md5→wxid 双映射,实测 246/246 表全覆盖)。
- **类型词表**:`localdb_query.py:61 MSG_TYPE_NAMES`(1 text/3 image/34 voice/43 video/47 sticker/48 location/49 file_or_link/10000 system/10002 revoke)。
- **文本解码**:`localdb_query.py:225 _decode_text_content`(WCDB_CT zstd 解码+占位计数,复用于高频短语提取)。
- **显示名**:`localdb_query.py:368 _contact_pick_names`(remark>nickname>alias 批量)。
- **时间归一**:`localdb_query.py:192 _normalize_ts`(s/ms 兼容;4.1.15 实况=秒)。
- **sidecar 协议面**:`src/myssia/wechat_local_sidecar.py` + `desktop/entry.py:7077-7080 _HANDLERS`;纯加法批不 bump PROTOCOL_VERSION(`wechat_local_sidecar.py:21-22` 判例)。
- **LLM 客户端**:`src/myssia/enrich/client.py:44 OpenAICompatClient`(OpenAI 兼容,token 记账);端点配置形态 = config yaml `enrich` 段(`config/exposure.yaml:86-92` 判例,`model: glm-5.3-flash`),装载判例 `pipeline.py:1196 _enrich_settings_from_config` + `enrich/settings.py resolve_endpoint`(credentials ref 解析)。
- **UI 件**:消息屏微信工作台 `messaging/wechat-local.tsx`(常驻分区版式判例);sidecar 调用封装判例 `messaging/api.ts`(`invoke("sidecar_request")`);Markdown 渲染 `feed/markdown-lite.tsx`;手绘 SVG 判例 `dashboard/sparkline.tsx`;**零图表库依赖**(package.json 无 chart 系,分布图走纯 CSS 条形)。
- **导出判例**:`desktop/src-tauri/src/wechat_group_export.rs` + `feed/wechat-group-export-api.ts`(前端已持载荷壳侧不重查、保存对话框 null=取消静默、两件成套落盘)。
- **版本真锁**:桥 0.7.0(`wechat_bridge/__init__.py:22`,与 pyproject.toml/component.json 三方同步,`tests/wechat-bridge/test_component_stamp.py` 把守)。
- **测试台**:`tests/wechat-bridge/bridge_testkit.py`(合成解密副本夹具形态)。

## Requirements

### R1 桥统计查询层(新文件 `wechat_bridge/stats_query.py`,纯 SQL 净室)

单遍聚合原语:给定(表集,时间窗)一次 SELECT(时间/类型/发送者列,短语提取另走文本列受控行数)产出聚合树;SQLite `strftime(ts,'unixepoch','localtime')` 分桶。语义钉死:

- **桶**:hourly 24(`%H`)/weekday 7(SQL `%w` 0=周日 → 归一 `((w+6)%7)+1` 即 1=周一..7=周日)/daily `YYYY-MM-DD`(localtime)/monthly 12(`%m`)。
- **total** = 全部行;**sent/received** 按「我方/对方」方向(见 self_id 推导);system(10000)/revoke(10002)计入 type_counts 单列,**不计入 sent/received、不参与响应/会话/短语指标**;human_total = total − system − revoke。
- **active_days** = 真 `COUNT(DISTINCT 日期)`(WeFlow activeMonths*20 估算语义明确不采);**longest_streak** = daily 序列上连续有消息日的最长段(含起止日期)。
- **会话切分**:相邻消息间隔 >30 分钟 = 新会话;**initiative** = 会话首条非系统消息的方向。
- **响应速度**(私聊/双人):相邻异向消息时间差,仅取 ≤24h 的对;avg/median/fastest(秒)+ 采样对数。
- **高频短语 top_phrases**:仅 local_type=1 文本(经 `_decode_text_content` 真解码,压缩解码失败占位不计);分词 = CJK 二元组 + 拉丁词;停用词表(的了是我你吗呢吧哈+媒体占位文本);出现 ≥3 次才入榜;top 20;单窗文本行流式处理(fetchmany,硬帽 20 万行)。
- **self_id 推导**(4.1.15 real_sender_id 无 isSender 列):私聊表内 sender≠该表 chat_id 的**众数** wxid = 我方;群聊内 sender==self_id 计 sent。**双路互证义务**:实现时对真私聊跑「isSender 形态路径 vs real_sender_id 路径」计数对拍(调研验证案 4),若真数据证明私聊收件行 real_sender_id 为 0/空而非对方 wxid,则改「非 chat_id 即我方、0/空=对方」规则并在 implement.jsonl 留证。
- **会话枚举与系统账号过滤**:`Name2Id.is_session` + 表名反解并集;kind = group(`@chatroom`)/official(`gh_*`)/private(其余)/system;**年度报告的私谈集**排除 WeFlow isPrivateSession 同语义系统账号清单:自己、`filehelper`、`weixin`、`weixinteam`、`qqmail`、`weibo`、`gh_*`、`@chatroom`(annual 只统计 private kind)。
- **归属不明的分表**(md5 反解不出):跳过并在应答 `unattributed_tables` 如实计数,不静默。
- **指标禁止项**:不做任何写副本操作(查询连接恒 `mode=ro`,`localdb_query.py:95` 同款);不建索引不物化(v1 纪律,见 R4)。

### R2 桥 CLI:`localdb stats` 四子命令(`cli.py` localdb 族挂载)

```text
wechat-bridge localdb stats chats  --json [--refresh]
wechat-bridge localdb stats chat   <chat_id> [--since Nd | --all] --json [--refresh]
wechat-bridge localdb stats annual [--year N | --all] --json [--refresh]
wechat-bridge localdb stats dual   <chat_id> [--since Nd | --all] --json [--refresh]
```

- `--since Nd` 沿用 `_parse_since_days` 严格形态;`--all` = 全时间(WeFlow dual year=0 即全时间语义);二者互斥缺省报 usage。`--refresh` = 跳过文件缓存强制重算。
- 编排 = `localdb.py` 新 `stats_history()`(照 `group_info` 判例:E2 副本域 `["message","contact"]` → 自愈钩子同款 → `stats_query` 装配)。
- 退出码契约同 group-info 评审判例:**查询层降级(缺表/缺列/空库)= 空结构恒 exit 0;密钥链 = 20/21/22 结构化 error 非 exit 0**。stats 属状态查询不判错。

**应答契约 v1(键序即实现序;wire snake_case)**:

`stats chats` → `{"stats_chats": {"chats": [{"chat_id","display_name","kind","message_count","first_ts","last_ts"}], "unattributed_tables": N, "copy": {...}}}`(年份清单由 UI 从 first_ts/last_ts 推导,免独立命令)。

`stats chat`(私聊/群聊通用一棵树;群聊 senders=发言排行)→

```json
{"stats_chat": {"chat_id","display_name","kind",
  "window": {"mode": "since|all", "from_ts","to_ts"},
  "total","sent","received","human_total",
  "type_counts": {"text":N,"image":N,"voice":N,"video":N,"sticker":N,"file_or_link":N,"location":N,"other":N,"system":N,"revoke":N},
  "hourly": [24],"weekday": [7],"monthly": [12],
  "daily": [{"date":"YYYY-MM-DD","count":N}],
  "active_days": N,"longest_streak": {"days":N,"from","to"},
  "top_phrases": [{"phrase","count"}],
  "senders": [{"sender_id","display","count"}],
  "sessions": {"threshold_minutes":30,"total","me_initiated","other_initiated"},
  "response": {"avg_seconds","median_seconds","fastest_seconds","pairs"},
  "self_id": "wxid_...","first_ts","last_ts",
  "cache": {"hit": false,"computed_ms": N}}}
```

`stats annual` → `{"stats_annual": {"year": N|"all", "years_available": [N…], "total","sent","received","human_total","type_counts","hourly","weekday","monthly","active_days","longest_streak", "chats_count", "top_chats": [{"chat_id","display_name","count"}](top20), "top_phrases", "midnight": {"count"(本地 0:00-5:59),"top_chat"}, "friend_contrast": [{"chat_id","display_name","early_count","late_count"}](early/late=年度上/下半两半窗计数,「失联/新朋友」呈现语义留 UI), "cache": {...}}}`。

`stats dual` → `{"stats_dual": {"chat_id","display_name", "window", "first_chat": {"ts","sender":"me|other","text"(截断 120 字,非文本=类型名)}, "me": {"count","initiated","avg_response_seconds","top_phrases"}, "other": {同形}, "heatmap": [[7][24] ints], "longest_streak","active_days","cache": {...}}}`。

### R3 缓存(严守父档「严禁每次全库扫」)

- 文件缓存:<数据根>/wechat-bridge/stats-cache/`<mode>-<sha1(参数+副本指纹)>`.json(数据根私有区桥资产,零出 git,keys.json 同纪律)。
- **副本代次指纹 = message_0.db 副本 mtime+size**(副本重建即失效,键自带;`_source_newer` 重建机制下 mtime 必变)。
- 载荷恒带 `cache:{hit,computed_ms}`;`--refresh` 旁路重算并覆写缓存;**确定性**:同键同副本重算两次逐字节一致(dict 构造序固定;AC 把守)。

### R4 性能纪律(先探针后裁决)

- 实现第一步:对真副本(346MB 量级)跑 `EXPLAIN QUERY PLAN` + 计时(只读),结果留 implement.jsonl。目标:annual 冷缓存单遍聚合 ≤60s;chat/dual 单表 ≤5s;缓存命中 <1s。
- 超标处置:**不自行建索引/不物化**(副本只读纪律);超标数据如实上报升级裁决(索引属写副本侧,桥纪律内定夺)。
- 进度流不做(worker/百分比进度 v1 砍):一次性 CLI + UI loading 态 + 缓存提示(「首次统计较慢,之后秒出」)足额;WeFlow worker 隔离是 Electron 常驻形态,MYIA 桥一次性子进程无此约束。

### R5 AI 报告(sidecar handler,MYIA 侧)

- 新协议方法 `wechat_local.stats_report`(params: `{mode, stats_payload, tone?}`;`stats_payload` = 前端已持的桥 stats 应答,**桥不重查**,`wechat_group_export json_payload` 判例)。
- 实现:`src/myssia/wechat_local_sidecar.py` 新 handler + `desktop/entry.py _HANDLERS` 注册(纯加法)。
- LLM:`OpenAICompatClient` 直用;端点 = 新 `config/wechat-stats.yaml`(enrich 段形态照 exposure.yaml:86-92:`enabled`(缺省 false)/`model`(缺省 glm-5.3-flash)/`base_url`/`api_key` ref);装载复用 `EnrichSettings` + `resolve_endpoint` + credentials ref 解析(pipeline.py:1196 判例)。`enabled: false` 或 openai 包缺位 = 结构化 `ai_disabled`/`dependency_missing` 如实,UI 给指引文案。
- **喂模型粒度(隐私缺省,主人可翻案需显式指令)**:纯聚合数字 + top_phrases top20 + dual first_chat 首条(已截断);**零逐条消息原文时间线**。
- 产出:Markdown 叙事(章节:总览/时段画像/关系洞察/结语;prompt 模板常量随码);应答 `{"report_markdown","model","total_tokens"}`(token 记账 client 自带)。

### R6 UI:「统计报告」分区(微信工作台族,不新造画布)

- 位置:`messaging/wechat-local.tsx` 微信本机工作区新增常驻分区(判例:同版面常驻分区、无返回钮、三层防)。
- 新件:`messaging/wechat-stats-api.ts`(sidecar_request 封装 stats/stats_report;wire 守门判例 wechat-groupinfo-api.ts)+ `messaging/wx-stats-panel.tsx`(+.test.tsx)。
- 流:报告类型四选(私聊分析/群聊分析/年度报告/双人报告)→ 会话选择(`stats chats` 拉取;群聊分析选 @chatroom,私聊/双人选好友;年度免选)→ 时间窗(近 30 天/近一年/全部)→ 生成 → 结果渲染 → 「生成 AI 报告」→ 「导出」。
- 渲染:数字卡(总消息/我发/收到/连续天数)+ 纯 CSS 条形(hourly/weekday/type 分布,零新依赖)+ 排行清单(群发言/年度最常聊);双人 = 我/对方两列对照 + 7×24 热度格(CSS 透明度格);AI 报告经 `feed/markdown-lite.tsx` 渲染。
- 错误族:桥 20/21/22 结构化直显(wechat-local.tsx 既有形态);缓存命中显示耗时。

### R7 导出(壳侧,group export 判例)

- 新 Tauri 命令 `wechat_stats_export {default_name, json_payload, markdown_payload?}` → 新文件 `desktop/src-tauri/src/wechat_stats_export.rs` + `main.rs generate_handler` 注册。
- 保存对话框一次 → 同目录同名两件:`<名>.json`(统计树全量,零改形)+ `<名>.md`(AI 报告,缺席则只落 json);null = 用户取消静默;回执 `{json_path, markdown_path?}`。
- UI 侧封装并入 `wechat-stats-api.ts`。

### R8 红线与文案

- 零微信进程干预、零写微信侧数据、查询连接恒 mode=ro;桥 stats 模块零网络零 AI(零出网纪律,`localdb_query.py:4` 同源)。
- 桥 argv/stderr 零消息正文(短语仅入 stdout 契约载荷,红线 6);缓存文件落数据根私有区。
- 文案判例:功能名全人话(「私聊分析」「群聊分析」「年度报告」「双人报告」「连续聊天 N 天」「最爱聊天时段」),协议/字段(local_type/type_counts/hourly)保留英文。

### R9 版本与接线

- 桥 0.7.0 → 0.8.0(`__init__.py`/`pyproject.toml`/`component.json` 三方同步;与并行子档撞号由集成员统一排)。
- `component.json` cli_contract.commands 增 stats 四命令一行注记;`tests/wechat-bridge/test_component_stamp.py` 自然把守。

## Acceptance Criteria

- [x] AC1 桥 stats 四命令对合成夹具(bridge_testkit 形态:Msg_<md5> 分表+Name2Id+contact 显示名)全绿;**SQL 聚合 vs Python 全量游标累加双算互证,两树逐字段相等**(调研验证案 1)。
- [x] AC2 真数据:chat 对 TMS 群真跑出真发言排行与时段分布;annual 真跑出 years_available 与全量指标;dual 对真实私聊真跑;发送者归因双路互证通过(或真数据证伪后按 R1 替代规则留证收编)。
- [x] AC3 类型语义:真库 local_type 分桶计数,1/3/34/43/47/49 每桶抽 3 条样本对照微信 UI 实际消息形态,记录留 implement.jsonl。
- [x] AC4 性能:EXPLAIN QUERY PLAN+计时留档;annual 冷缓存 ≤60s、缓存命中 <1s、`--refresh` 强制重算;同键重算两次逐字节一致(AC5 并测)。
- [x] AC5 缓存:命中/未命中态正确;副本重建(模拟 mtime 变)后旧缓存自动失效重算。
- [x] AC6 UI:统计报告分区四类报告渲染 + 会话选择 + AI 报告生成与渲染 + 导出两件落盘可打开(合成夹具单测 + 真数据对拍);文案人话审计零行话上屏。
- [x] AC7 红线守卫:grep 证 stats_query 无网络 import/无写连接(恒 mode=ro)/零微信进程 API;AI 喂模型载荷零逐条消息原文;桥 argv/stderr 零正文。
- [x] AC8 门禁全绿(桥测试族+desktop 测试+装机包门禁);版本三方同步 0.8.0;装机包刷新+像素验证(统计面板+AI 报告+导出流)。

> **复查回执(2026-10-14 复查员实跑,判定 PASS/needsFix=false)**:① chat 44092365100@chatroom → total=111062 sent=1268 received=108887 active_days=90 self_id=wxid_oc2yhey1xkpw22 cache miss 816ms;拷问点 total≠sent+received 差 907 → 复查 type_counts.system=907 revoke=0,human_total=110155==sent+received,契约(PRD R1「system/revoke 不计入 sent/received」)自洽;二次调用 cache hit ✓;② 确定性:两次 --refresh 重算后缓存文件 sha256 逐字节相同;③ annual --all 真跑(命令=localdb stats annual)years=[2026] total=20964 chats=162 computed 319ms≪60s;④ pytest test_stats_query+test_stats_cli 46 passed、test_wechat_stats_sidecar 28 passed、cargo test wechat_stats_export 3 passed;vitest wx-stats-panel 10 passed;⑤ 红线 grep stats_query.py 网络 import/print/sys.stderr/写 SQL 全零命中(连接经 localdb_query._open_copy mode=ro,stats_query.py:16)。装机像素验证(C2 面)归父档 AC-P4 回执(15-stats-sns-media-contacts.png)。
>
> **留档发现**:[info] 顶层无 `stats` 动词(stats 挂 localdb 子命令族,cli.py:338 stats_query.register_cli(localdb_sub))——与前轮回执 integrationSpec 接线规划一致,非缺陷。

## Notes

- AI 喂模型粒度(纯聚合缺省)、会话阈值 30 分钟、响应窗 24h 均为可翻案缺省(翻案需主人显式指令),非阻塞。
- C1(六格式聊天记录导出)与本档导出不重叠:本档导出统计树+AI 报告,聊天记录导出归 C1;保存对话框底座如 C1 先落可共用,集成员排。
- C6 HTTP API 后续把 stats 四命令映射进 HTTP 面(C6 档职责),本档只落 CLI+sidecar。
- WeFlow 指标语义对照表(仅设计参照):年度 17 族见其 annualReportService.ts:33-91(longestStreak/midnightKing/socialInitiative/responseSpeed/lostFriend/topPhrases);双人对照 dualReportService.ts:27-103(firstChat/专属短语/heatmap/initiative/streak/year=0 全时间)。本档 friend_contrast/sessions/response 即其语义的 SQL 等价式。
