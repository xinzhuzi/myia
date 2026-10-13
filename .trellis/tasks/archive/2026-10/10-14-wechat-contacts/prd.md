# 微信联系人与找回(C4)

## Goal

在已打通的桥 localdb 只读链上,交付微信**联系人工作台**:好友/群聊/公众号/曾经的好友四类筛选浏览 + 关键字搜索 + 分页,三格式导出(JSON / CSV 带护 BOM / VCF vCard 3.0),以及「找回曾经的好友」的**考古呈现**——contact 表残留 + stranger 表 + room_verify_application 三源,逐条标证据与置信度,如实声明「部分找回、非保证」。一切读解密副本,零微信进程干预、零写微信侧数据;找回**只做考古列表与导出,无任何重加操作**(WeFlow 的 wcdbVerifyUser 桥接/重发验证属写侧,红线不进货)。

## 来源与依赖

- 父档:`.trellis/tasks/10-13-wechat-features/prd.md` #10 行「联系人:导出好友、群聊、公众号信息;找回部分曾经的好友」+ 子任务地图 C4 行;文案判例 AC-P5(UI 全人话,协议/字段标准英文);版式约束「并入既有微信工作台族,不新造画布」。
- 开源调研定稿(2026-10-14,工作流调研件,证据已 path:line 落档):
  - **产品语义锚 = hicccc77/WeFlow**(CC BY-NC-SA 4.0):四类筛选、JSON/CSV(BOM)/VCF(vCard 3.0,X-WECHAT-ID 自定义字段 + NOTE 收纳备注/标签/证据)三格式导出、分类判定序、系统账号排除集。**零抄码零文案照搬**——判定式是 contact 表字段数据事实(本档已在本地 4.1.15 副本实测自考,见下节),导出器/UI 全自写。
  - **码基辅锚 = labazhou2024/chatlog-keeper**(MIT):contact+stranger 双表同 schema 合并读的模式可借;显示名优先级链 remark>nick_name>alias 与 MYIA 既有链同序(直接复用,无需借码)。
  - **schema 文档辅锚 = LifeArchiveProject/greenbubbles**(MIT,docs/WECHAT_DATABASE_FORMAT.md):contact 全列集、stranger 表语义("Same column set as contact")、chatroom_member/contact_label/biz_info 表义、head_image.db 头像路径约定、**「blob 列标注 opaque 不臆造公共 schema」诚实契约**(extra_buffer 原样不解析)。
  - WeChatDataAnalysis(无 LICENSE):仅借 local_type 值谱认知(1=好友/2=群/3=残留/5=openim)与「former_friends 作为显式参数」形态,零码。
- **真库实测定锚(本档规划期 2026-10-14 已跑,只读)**——这是判定式的**唯一权威源**(调研风险「local_type 语义漂移,须实测定稿」已消除):
  - 数据:`~/Library/Application Support/MYIA/wechat-localdb/decrypted/contact/contact.db`(15.5MB,22,091 行)+ 同目录 `message/message_0.db` 的 Name2Id。命令与全量数字见附录 A。
  - contact.db 表清单(sqlite_master):`contact / stranger / contact_label / chat_room / chat_room_info_detail / chatroom_member / biz_info / encrypt_name2id / name2id / openim_acct_type / openim_appid / openim_wording / oplog / room_verify_application / stranger_ticket_info / ticket_info / sqlite_sequence`。
  - `stranger` 列集与 `contact` **逐列相同**(PRAGMA 对拍),3 行(local_type=4)。`room_verify_application` 列集 = `msg_server_id / chatroom_name / hash_key / inviter_username / state / read_status / data_json / update_time`,**0 行**(语义推断:群验证/入群申请记录,标「推断」)。
  - **六桶划分恰覆盖全表零遗漏**(2+@+gh+former+friend+其他+系统号 加和 == COUNT(*) == 22,091):
    | 桶 | 判定 | 实测行数 |
    |---|---|---|
    | 系统号(诊断字段,不呈现) | username ∈ 排除集 | 4(在场:medianote/floatbottle/weixin/fmessage) |
    | 群聊 group | username LIKE '%@chatroom' | 105 |
    | 公众号 official | username LIKE 'gh\_%' | 346(其 lt1=280/lt0=63/lt3=3) |
    | 曾经的好友 former | local_type=3 AND nick_name<>''(非 chatroom/gh/系统号) | **20,310** |
    | 好友 friend | local_type=1(非 gh/chatroom/系统号) | 731 |
    | 其他 other | 其余 | 594(lt0 裸行 464 + lt3 无昵称 1 + lt5/6/7 openim·客服 129) |
  - **WeFlow 原版严判据在本机近乎失效**:其 `lt0+quan_pin 或 lt3+flag≠4+身份字段` 全式只命中 **1 行**(本机 lt3 行的 quan_pin/alias/remark 几乎全空,但 20,313/20,314 有 nick_name)。故 MYIA 判定式以 nick_name 残留为主信号、WeFlow 式身份字段降级为**附加证据位**,严判据计数保留为对照诊断字段 `strict_residual_count`。
  - **置信度分层(考古核心)**:20,310 候选 ∩ message_0.db `Name2Id.user_name` = **6,386 = Tier A「有会话痕迹」**;其余 13,924 = Tier B「仅通讯录残留」(可能含群内陌生人缓存,如实标低置信)。候选自有 Msg_ 表者 0(表已删,Name2Id 映射残留即证据)。另:候选 ∩ session.db SessionTable = 0(会话表不残留,分层不能靠 session)。
  - contact_label 表 3 行(label_id_ 4/5/6),但 **contact 表无标签关联列**(PRAGMA 全列在案),标签归属在 extra_buffer(opaque)内——按 greenbubbles 诚实契约**不解析**,标签只呈现表内清单不做逐人关联。
- 既有数据面全复用:桥 0.7.0 现役(`plugins/wechat-bridge/wechat_bridge/__init__.py:22`)、E2 解密副本管道、keys.json 20 钥(实测含 `contact/contact.db` 与 `contact/contact_fts.db`)。无外部阻塞。

## 既有交付盘点(不重做,直接复用)

| 交付 | 证据锚 |
|---|---|
| E2 解密副本生命周期(TTL/容量/源新即重建/自愈钩子)与 contact 域目标 | `plugins/wechat-bridge/wechat_bridge/localdb.py:1406`(ensure_decrypted_copies)、`localdb.py:1302-1307`(DOMAIN_DB_FILES:contact→contact/contact.db) |
| 编排样板(query_history/sns_history/group_info 三同构:E2→自愈→E3) | `localdb.py:1547`、`:1601`、`:1656`;group-info 的**域收缩纪律**(单 contact 域自足,不带 message/session)见 `localdb.py:1667-1674` |
| contact 域读件:显示名批量链(remark>nickname>alias)、备注链、群信息族(chat_room/chatroom_member/chat_room_info_detail/rowid 反解) | `wechat_bridge/localdb_query.py:368`(_contact_pick_names)、`:429`(_contact_pick_remarks)、`:545-752` |
| Name2Id 反解(rowid→user_name、md5(user_name)→Msg_ 表名) | `localdb_query.py:122`(name2id_maps)——Tier A 残留检查复用其 user_name 集合 |
| localdb 命令族注册模式 + 「状态查询不判错恒 exit 0 / 缺表降级空结构」判例 | `wechat_bridge/cli.py:108-194`(query/sns/group-info 注册形态)、`localdb_query.py` group_info 降级语义 |
| 密钥三态/取钥/自愈全链(本任务零新做) | `localdb.py:979`(key_status)、`:1187`(resolve_keys) |
| 群信息面板 + 群导出先例(**壳侧写盘:JSON + CSV UTF-8 BOM,保存对话框,取消=null 静默**) | `desktop/src-tauri/src/wechat_group_export.rs`、`desktop/ui-src/src/screens/feed/wechat-group-export-api.ts`、`wx-groupinfo-panel.tsx` |
| 微信本机工作台 UI 族(探针头/权限引导/只读会话/本地库查询分区卡) | `desktop/ui-src/src/screens/messaging/wechat-local.tsx:116-201`(WechatLocalSection) |
| sidecar 动作族(四动作封闭词表 + entry.py 薄壳) | `src/myssia/wechat_local_sidecar.py:199-204`(_ACTIONS)、`desktop/entry.py:4768-4799,7077-7080` |
| 测试基建:桥 pytest(test_group_info.py 判例)/sidecar pytest/Rust in-file tests/vitest | `tests/wechat-bridge/test_group_info.py`、`tests/desktop/test_wechat_local_handlers.py`、`wechat_group_export.rs`(in-file 7 tests)、`wechat-local.test.tsx` |

## Requirements

### R1 桥新命令 `localdb contacts`(分类 + 计数 + 分页行)

新文件 `plugins/wechat-bridge/wechat_bridge/contacts_query.py`:

- **CLI**(`cli.py` localdb 子命令族注册,判例 group-info):`localdb contacts --json [--type friend|group|official|former|other] [--keyword K] [--limit N] [--cursor C] [--with-residue] [--include-stranger]`;`--limit` 缺省 100、帽 1000;`--keyword` 对 `remark / nick_name / alias / username / quan_pin` 五列 LIKE `%K%`(纯 SQL,22k 行毫秒级;contact_fts.db 不解密不消费)。
- **判定序(钉死,每行恰归一桶)**:①username ∈ 系统号排除集 `{medianote, floatbottle, qmessage, qqmail, fmessage, weixin, weixinigram, weixin_team}` → system(不出行,只计入诊断);②`username LIKE '%@chatroom'` → group;③`username LIKE 'gh\_%'` → official(不叠 lt1 条件——本机 gh_ 三种 lt 都在,全量归公众号桶更诚实,与 WeFlow 的 gh_+lt1 组合有意分歧,分歧原因=真库实测);④`local_type=3 AND nick_name<>''` → former;⑤`local_type=1` → friend;⑥其余 → other。列漂移(PRAGMA 自适应,判例 execQuery)缺列 → 对应桶空 + 诊断字段标注,不判错。
- **行形状**(显示名复用既有语义链,SQL 内 COALESCE(remark,nick_name,alias,username) 同序):`{"username", "display_name", "remark"|"", "nickname"|"", "alias"|"", "type"(六桶名), "local_type"(原值), "evidence"([] 或见 R2), "description"|null}`;群聊行另带 `"member_count"`(chatroom_member 计数,判例 `_chatroom_member_ids` 同表)。
- **分页**:keyset 游标 = base64(JSON `{"v":1,"rowid":N,"filter":{"type","keyword"}}`),`WHERE rowid > N` 升序续拉;**scope 守卫**:请求 filter 与游标内不一致 → exit 2 `invalid_cursor`(判例 C1 page 同族)。首帧无游标从 rowid 最小起。
- **应答契约**(stdout 单 JSON,键序即此):`{"contacts": {"counts": {"friend","group","official","former","other","system"}, "former_tiers": {"msg_residue","table_only"}|null, "residue_checked": bool, "strict_residual_count": int, "labels": [{"id","name"}], "stranger": [...](R2 形状,仅 --include-stranger), "room_verify": {"present": bool, "rows": int}, "rows": [...], "next_cursor"|null, "has_more", "filter": {...}, "page_size"}}`。counts 恒全量返回(cheap GROUP BY,chip 计数直用);`former_tiers` 仅 `--with-residue` 时非 null。
- **编排**:`localdb.py` 增 `contacts_inventory(config, db_storage, keys, *, type_filter, keyword, limit, cursor, with_residue, include_stranger, data_root, now)`——E2 副本域:缺省/无 residue = `["contact"]`(15MB,group-info 域收缩纪律);`--with-residue` = `["contact","message"]`(Tier A 需要 message_0.db Name2Id;346MB 副本走既有 TTL 缓存复用,UI 只在考古面触发,不进轮询)。自愈钩子与三前辈同款。缺表/缺列降级空结构恒 exit 0(判例 group-info);密钥链错误族与 query 同码(20/21/22)。

### R2 找回考古:三源 + 证据分层(如实标注)

- **Tier A「有会话痕迹」**:former 候选 username ∈ message_0.db `Name2Id.user_name`(集合加载复用 `name2id_maps` 的行读取;不扫 Msg_ 表)。行 `evidence` 含 `"msg_residue"`。
- **Tier B「仅通讯录残留」**:其余候选,`evidence` 为空数组,UI 侧标低置信。
- **附加证据位**(WeFlow 式,数据事实):候选行 quan_pin/alias/remark 任一非空 → evidence 加 `"identity_fields"`(本机实测仅 1 行,作证据增量呈现)。
- **stranger 表**(`--include-stranger`,缺省开):原样小数组 `[{"username","display_name","local_type","remark"|""}]`,UI 独立子卡「非好友联系人缓存」,不混入 former 计数(语义=greenbubbles「尚未入正常联系集的类联系人记录」,非曾好友;本机 3 行)。
- **room_verify_application**:只报存在性与行数进 `room_verify`;行数>0 时附前 100 行(`chatroom_name/inviter_username/state/update_time` 四列直读,data_json 原样字符串不解析)。语义标「推断:群验证/入群申请」。本机 0 行 → UI 呈「本机无记录」。
- **严判据对照**:`strict_residual_count` = WeFlow 原式在本库命中数(SQL 转写自写),作校准诊断字段,不出 UI。
- **红线**:零重加操作——不实现任何 verifyUser/重新加好友通路;考古=列表+证据+导出,句号。

### R3 三格式导出(壳侧写盘,群导出先例)

新文件 `desktop/src-tauri/src/wechat_contacts_export.rs`(注册 `main.rs`,判例 `wechat_group_export`):

- **命令** `wechat_contacts_export {type, keyword?, with_residue?, formats: ["json","csv","vcf"]}`:壳不收大载荷——保存对话框(blocking_save_file,取消=返 null 静默,群导出判例)定基础名 → spawn 安装态桥 `localdb contacts --type <t> [--keyword K] [--with-residue] --limit 0 --json`(`--limit 0` = 全量,桥内帽豁免)→ 三格式同基础名落盘(`<base>.json/.csv/.vcf`)→ 回执 `{"files": [{"name","path","rows"}], "total_rows"}`。
- **JSON**:桥应答 rows 数组原形直写(pretty,零改形;含 evidence/类型,provenance 不丢)。
- **CSV**:表头 `username,display_name,remark,nickname,alias,type,evidence,last_contact_hint`;UTF-8 **带 BOM**(`\uFEFF`,群导出同款);**注入转义**:字段以 `= + - @` 或 tab 开头 → 前置 `'`(C1 同规);evidence 数组序列化为 `|` 连接。
- **VCF(vCard 3.0,自写序列化)**:每联系人一 `BEGIN:VCARD/VERSION:3.0`;`FN`=display_name、`N`=display_name(未知结构不臆拆)、`NICKNAME`=nickname(在场时)、`X-WECHAT-ID`=username(自定义扩展字段名为 vCard 命名惯例,非许可表达)、`NOTE` 收纳:类型/证据(「会话痕迹」「仅残留」)/alias/description(人话标签行);CRLF 行尾 + RFC 2426 折叠(75 字节)与转义(`, ; \ 换行`);群聊行同型 vCard(member_count 入 NOTE)。
- **权限与隐私**:导出件落盘 `0600`(chatlog-keeper private_text_writer 语义);内容零入日志(回执只带路径与行数)。

### R4 接线:sidecar + 壳 + TS

- **sidecar**(`src/myssia/wechat_local_sidecar.py`):`_ACTIONS` 增 `"contacts"`(params `{type?, keyword?, limit?, cursor?, with_residue?, include_stranger?}` → 桥 `localdb contacts`,超时 `_QUERY_TIMEOUT_SECONDS` 族;with_residue=true 时超时上浮提示由 UI 态承接)。
- **entry.py 薄壳**:`_m_wechat_local_contacts` + METHOD 表 `"wechat_local.contacts"`(判例既有四方法)。
- **TS api**(`desktop/ui-src/src/screens/messaging/wechat-contacts-api.ts` 新文件):`wechatLocalContacts(params)`(invoke `sidecar_request` method `wechat_local.contacts`,parse 守门判例 `parseWechatGroupExportResult`)+ `wechatContactsExport(...)`(invoke `wechat_contacts_export`)。
- **UI**(`desktop/ui-src/src/screens/messaging/wechat-contacts.tsx` 新文件,`ContactsBrowser` 组件挂入 `wechat-local.tsx` WechatLocalSection 尾部分区,判例 SessionReader/LocalDbQuery 同款;**C1 同改此文件,集成员合流**):
  - **计数 chip 行(五桶,人话)**:「好友 731 · 群聊 105 · 公众号 346 · 曾经的好友 20,310 · 其他 594」数字为查询实值(此为 2026-10-14 实测锚,非硬编码);点击 chip = type 筛选 + 首页拉取。
  - **搜索框**:debounce 200ms 触发(WeFlow 120ms 语义,取整避抖);清空恢复当前桶首页。
  - **列表**:分页 100/页,「加载更多」cursor 续拉(C1「加载更早」同 idiom,不引入虚拟列表);行 = 显示名 + username(mono)+ 类型徽标 + former 行证据徽标(「会话痕迹」/「身份字段残留」;无徽标 = 仅残留低置信)。
  - **考古面(选「曾经的好友」chip 时)**:顶部常驻声明行(人话):「考古呈现:从本地库残留找出,不保证完整与准确;按证据分层,可能含群内陌生人缓存」;进入该 chip 才带 `with_residue`(面板「考古中…」态,346MB 副本首次解密耗时如实呈现);子卡:stranger 表(「非好友联系人缓存,N 条」)与 room_verify(「群申请记录,本机无记录/有 N 条」)。
  - **导出行**:格式三选(JSON 文件 / CSV 表格 / 通讯录 VCF)+ 「导出当前筛选」按钮 → 壳命令 → 回执路径列表可打开(群导出面板判例);错误族(asSidecarError)结构化直显不重试。
  - 标签清单(`labels`)呈现在面板尾注一行「库内标签:N 个」——不做逐人关联(见定锚节,诚实不臆造)。

### R5 版本与文档

桥 minor 递增:**集成时按当时现役取下一个 minor**(C1 已声明 0.7.0→0.8.0,本档预期 0.9.0,集成员统一裁决防撞);三方同步 `pyproject.toml` version、`component.json` "version"、`wechat_bridge/__init__.py:22`;README 命令表(`plugins/wechat-bridge/README.md:14-25`)+1 行 `localdb contacts`。

## Acceptance Criteria

- [x] AC1 **划分闭包对真库**(只读):活副本上 `localdb contacts --json` 的 counts 六桶加和 == `SELECT COUNT(*) FROM contact`(22,091 量级,以同刻为准);counts 与附录 A 同刻手跑 SQL 逐桶一致;命令与输出留档本档 `research/`。
- [x] AC2 **分页与过滤零重漏**:任一桶 `--limit 100` 游标全量翻页,拼接 rowid 集无重复无遗漏,行数 == 该桶 count;`--keyword` 命中五列 LIKE 对拍 SQL 一致;filter 与游标不符 → exit 2 `invalid_cursor`。
- [x] AC3 **考古分层如实**:Tier A 集合 == former 候选 ∩ Name2Id.user_name(SQL 对拍,本机锚 6,386/13,924);每 former 行 evidence 正确(msg_residue/identity_fields);`strict_residual_count` 对拍 WeFlow 式 SQL(本机锚 1);stranger=3 行原样、room_verify present=true rows=0;缺表/缺列夹具降级空结构 exit 0。
- [x] AC4 **三格式真跑一致**:真库各格式全产——JSON 行数 == 筛选计数;CSV 首三字节 `EF BB BF`、Excel 打开中文不乱码、`=+-@`/tab 开头字段前置 `'` 用例过;VCF 被 macOS 通讯录预览识别、X-WECHAT-ID/NOTE 在场、CRLF+折叠+转义用例过(含逗号/分号/换行昵称夹具);导出件 0600。
- [x] AC5 **UI 端到端**:vitest(`wechat-contacts.test.tsx`)全绿;真机走通——五 chip 计数呈现/切换、搜索、加载更多、考古声明与证据徽标在场、三格式之一导出回执路径可打开;stranger/room_verify 子卡如实。
- [x] AC6 **接线完整**:`wechat_local.contacts` sidecar 动作 + entry.py 薄壳 + `wechat_contacts_export` 壳命令注册;桥错误族(20/21/22)经 UI 结构化直显(pytest + Rust in-file tests 过)。
- [x] AC7 **版本与文档**:三方版本同步、README 命令表 +1、component.json 戳与 `__version__` 一致(test_component_stamp.py 过)。
- [x] AC8 **红线守卫**:grep 守卫——源库路径零 WRITE/INSERT/UPDATE/DELETE、零 verifyUser/重加通路、零微信进程交互词;WeFlow/WeChatDataAnalysis 零码(无其特有标识串);夹具全合成数据,聊天内容/联系人明细零入 git。
- [x] AC9 **域收缩纪律**:无 `--with-residue` 的调用解密面仅 contact 域(15MB),不触 message(副本清单/E2 日志核验);UI 仅考古 chip 触发 residue。

> **复查回执(2026-10-14 复查员实跑,判定 PASS/needsFix=false)**:① realdb_ac_check.py 真跑(`python3 .trellis/tasks/10-14-wechat-contacts/research/realdb_ac_check.py`)→ 16/16 全 PASS(六桶闭包 sum=22092==COUNT、official/friend 游标零重漏 343/731、keyword 对拍 25、invalid_cursor exit2、Tier 6389/13925、strict 人集作用域=1、stranger 3、room_verify present rows0;22092 vs 前回执 22091=活库漂移,脚本头明示以同刻一致性为准);② 红线 grep contacts_query.py 写 SQL/网络/进程全零;Rust wechat_contacts_export.rs:164 Command::new=spawn 桥进程(twin 同形模式)非微信干预;③ pytest test_contacts_query 31 passed、vitest wechat-contacts.test.tsx 10 passed、cargo test wechat_contacts_export 12 passed(前回执遗留「main.rs 注册后真编译」本轮补验,main.rs:16/939 已注册)。装机像素验证(C4 面:联系人四桶 chip)归父档 AC-P4 回执(15-stats-sns-media-contacts.png)。
>
> **留档发现**:[info] 前回执遗留项⑥「Rust 真编译+cargo test 留注册后」已由集成落地并本轮真跑通过;AC4 三格式真跑(需真对话框)仍属装机面验收,未在本轮复跑(如实)。

## Constraints

- **只读红线**:一切读解密副本;唯一写动作 = 用户指定目录导出件(0600)。
- **许可红线**:WeFlow(CC BY-NC-SA)与 WeChatDataAnalysis(无许可)零码零文案照搬;chatlog-keeper(MIT)若借码须文件头归属注记(本设计自写,预期不触发);判定式/列名/表名=数据事实不受限;X-WECHAT-ID=vCard 扩展字段命名惯例。
- **诚实契约**:extra_buffer/data_json 等 blob 列 opaque 原样不解析(greenbubbles 判例);找回=考古呈现非保证,逐条证据分层;标签不做逐人关联(无关联列,实测在案)。
- **性能**:contact 域 15MB 级,LIKE 全扫毫秒级可接受;residue 链 346MB 副本走 E2 TTL 缓存,仅考古面按需触发,严禁轮询化。
- **文案判例**:UI 全人话(「曾经的好友」「考古呈现」「会话痕迹」),CLI/协议字段标准英文(`with_residue`/`next_cursor`/`strict_residual_count`)。
- **版式**:并入既有微信工作台族(wechat-local.tsx 分区卡),不新造画布、不引入虚拟列表/头像列(头像链留后续,见边界注记)。

## 边界注记(与兄弟档)

- **C1 查询导出**:C1 拥消息六格式导出引擎与 wechat-local.tsx 浏览面升级;本档联系人导出**分立**走群导出先例(壳侧写盘),不共用导出器(C1 边界注记已同款声明);两档同改 `wechat-local.tsx`,集成员合流;版本号接力(C1=0.8.0,本档随后取下一 minor)。
- **C6 HTTP API**:本档 `localdb contacts` CLI 契约即 C6 联系人端点的映射源;编排函数 `contacts_inventory` 为 C6 的同源调用点(C6 档已声明「C4 落位后扩量,不等待」)。
- **C2 统计报告**:好友/群清单消费本档 counts 与行通道;聚合 SQL 属 C2 自建。
- **C3 媒体与朋友圈**:无重叠(本档不碰 .dat/sns)。
- **头像链(后续增强,不在本档)**:事实已备——`db_storage/head_image/head_image.db` 在场、keys.json 含其钥(greenbubbles:按 username+MD5 取 blob);需新域目标+blob 解码+缓存层,值 UI 族当前无头像 idiom,留独立后续件。
- **排序增强(后续)**:按最后联系时间排序需 session 域 join(本机 friend∩session=345/731 可用但域成本+语义半覆盖),v1 行序=库序(rowid),UI 不承诺时间序。

## 附录 A:真库实测命令与输出(2026-10-14,规划期,只读)

```console
# 表清单
sqlite3 <decrypted>/contact/contact.db "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;"
# → biz_info chat_room chat_room_info_detail chatroom_member contact contact_label encrypt_name2id
#   name2id openim_acct_type openim_appid openim_wording oplog room_verify_application
#   sqlite_sequence stranger stranger_ticket_info ticket_info

# local_type 分布(22091 行)
sqlite3 ... "SELECT local_type, COUNT(*) FROM contact GROUP BY local_type ORDER BY 2 DESC;"
# → 3|20314  1|1022  0|527  2|98  6|72  5|56  7|2

# 六桶划分(PRAGMA 列集 + LIKE/IN 组合,python sqlite3 只读模式跑)
# → total 22091 == sum 22091 | sys 4 grp 105 off 346 former 20310 friend 731 other 594
# other 构成:lt0 464 + lt3 无昵称 1 + lt5 56 + lt6 72 + lt7 2

# stranger:COUNT=3;PRAGMA table_info(stranger) 与 contact 逐列相同
# room_verify_application:COUNT=0;列 msg_server_id chatroom_name hash_key inviter_username state read_status data_json update_time
# WeFlow 严判据命中:1 行;lt0+quan_pin:8 行;flag&8(blocked):0 行
# former ∩ message_0.db Name2Id.user_name:6386(Tier A);其余 13924(Tier B)
# former ∩ session.db SessionTable:0;friends ∩ Name2Id:274/1022;contact_label:3 行(4/5/6 号标签)
# contact 表无标签关联列(PRAGMA 全列在案,归属在 extra_buffer 内,不解析)
```

(实测者注:以上数字是 2026-10-14 副本时点锚,库随微信使用漂移;AC1 以「同刻对拍一致」为准,不以绝对值为准。)
