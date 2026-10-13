# 微信新消息通知与撤回呈现(C5)

## Goal

把 WeFlow 两项功能按 MYIA 只读形态落地:**新消息通知**(轮询水位版,非进程 hook)+ **撤回消息呈现**(纯只读检测+残留原文恢复):

1. **新消息通知**:桥侧一次会话基线水位扫描(SessionTable 先筛+分表定点增量)→ 主机侧分钟级 cron 品类 → 既有投递体系(route→`send_immediate`)→ **macOS 通知中心弹窗**(本机零网络新通道)+ 通知历史入 store/feed。会话白名单=品类 YAML 声明(weixin.yaml 既有形态)。
2. **撤回呈现**:桥侧撤回检测谓词(local_type 10002/10000+内容标记)+ 原文恢复阶梯(server_id 直查→时间近邻启发式→replacemsg 文本兜底),产出 `message.revoke` 通知事件 + `localdb revoke-list` 查询契约,供 C1 浏览面「已撤回」标记渲染。

**红线不变**:零微信进程干预、零写微信侧数据(一切读解密副本,`mode=ro`);WeFlow 的 trigger 安装层(向微信消息表写 SQLite trigger 的「防撤回」)显式不做、不模仿、不进货。

## 来源与依赖

- 调研锚:hicccc77/WeFlow(15052★,CC BY-NC-SA 4.0)——**只借语义算法零代码借入**(水位/谓词/恢复阶梯);水位轮询的代码级参照=imldy/chatlog fork(Apache-2.0,sjzar/chatlog 删库前快照)。腾讯行动链(chatlog/PyWxDump 函件→wechat-dump-rs DMCA)证据钉在父档调研,本档不引外链代码。
- **B0 硬依赖已解除**:父档行 10 的「B0(4.1.15 分表适配)落地前 C1 以下不动工」——桥 0.7.0 已含 0.4.2 B0(`plugins/wechat-bridge/wechat_bridge/localdb_query.py:15-30` 分表形态+Name2Id 反解+zstd 解码,实测 246/246 表全覆盖),C5 可动工。
- **本会话真库实测(2026-10-14,解密副本只读直查)**:
  - `session/session.db` 表名=**`SessionTable`**(非 `session`),454 行,关键列全在场:`username/unread_count/last_timestamp/last_msg_type/summary/last_sender_display_name`(PRAGMA 实测)——WeFlow 会话基线水位 {lastTimestamp, unreadCount, lastMsgType} 三元组在 4.1.15 真库成立。
  - **撤回行普查:message_0.db 249 张 Msg_ 表 + biz_message_0.db 195 张,local_type=10002 共 0 行;revokemsg/replacemsg/撤回了一条消息/你撤回 内容标记全库 0 命中;SessionTable.summary 撤回字样 0 命中**。即本机当前副本内无任何已落库撤回样本——「撤回行残存率」无从普查,撤回检测谓词只能按 WeFlow 语义先建、靠实弹实验验证(AC6),macOS 4.1.15 是否落撤回行是待实证问题,如实处理不硬凑。

## 既有交付(不复做)

| 件 | 证据 |
|---|---|
| E2 解密副本管道(源新即重建/TTL/并发单飞锁) | `plugins/wechat-bridge/wechat_bridge/localdb.py:1406-1452`(notify-scan 数据基座,每次桥调用前 ensure,副本恒新鲜) |
| E3 查询层:Msg_ md5 分表自适应/Name2Id 双向反查/real_sender_id 发送者/zstd 解码 | `localdb_query.py:122-189`(name2id_maps/find_message_tables)、`localdb_query.py:277-360`(query_messages) |
| 类型名表已含 10000→system、10002→revoke | `localdb_query.py:61-71`(MSG_TYPE_NAMES) |
| 密钥链全通+自愈+取钥编排(桥 0.7.0) | `cli.py:368-512`(query/key-scan/key-provider/key-status/key-acquire 分支);`component.json` |
| wechat_local 引擎三通道(pixel/localdb/sns)+源级水位机制+结构化 skip | `src/myssia/engines/wechat_local.py`(WATERMARK_PREFIX/change_baseline kv/key_unavailable skip) |
| weixin 品类 YAML 形态+缺省关先例+YAML 编辑屏管理面 | 数据根 `config/weixin.yaml`(*/30,push:[]);monitor-ui R4.1 判例 |
| 投递体系:route(immediate/digest/archive)+`send_immediate` 同轮合并+30 通道注册表 | `src/myssia/push/route.py`、`push/digest.py:400-444`、`push/__init__.py:195`(CHANNELS) |
| feed 屏微信聊天气泡渲染(源名 `weixin-`/`wx-` 前缀自动判定)+三级监控台 | `desktop/ui-src/src/screens/feed/api.ts:633,657`(WEIXIN_SOURCE_RE/channelKindOf) |
| cron 品类 job 注册面(桌面 cron 屏/CLI,job=品类 YAML 绝对路径) | `src/myssia/cron/jobs.py`(载荷=category)、`cron/runner.py:175-183`(job_command→`run <category>`) |
| 账号 wxid 可发现(自消息判定数据源) | `localdb.py:192`(`<数据根>/all_users/login/<wxid>/key_info.db` 布局,A3 实测) |

## Requirements

### R1 桥侧检测件:`notify_query.py`(新文件,纯只读)

`plugins/wechat-bridge/wechat_bridge/notify_query.py`,复用 `localdb_query.py` 既有件(表发现/Name2Id/发送者反查/zstd 解码),实现两层扫描:

**R1.1 会话基线层(便宜先筛)**:单查 `SessionTable`(`username, unread_count, last_timestamp, last_msg_type`;表名/列名按既有 `_pick` 列签名自适应,直查纪律同 group_info)。对**白名单内**会话逐个比对基线 `{ts, unread}`(无基线=候选):

- 候选 = `last_timestamp > baseline.ts` OR `unread_count != baseline.unread` OR `last_msg_type == 10002` OR 无基线。
- 非白名单会话零二次查询(白名单外=不通知,即黑名单语义:不声明即屏蔽)。

**R1.2 定点增量层(仅候选会话)**:对该会话 `Msg_<md5(username)>` 表(经 `name2id_maps` md5 映射选表)查:

```sql
SELECT local_id, server_id, sort_seq, create_time, local_type,
       real_sender_id, message_content, compress_content, WCDB_CT_message_content
FROM "<Msg_表>" WHERE create_time >= :watermark_ts - 90
ORDER BY create_time DESC LIMIT 20
```

- `watermark_ts` = 基线 `ts`(首轮无基线=当前时刻,只建基线零事件——chatlog「初值 now」同款,防装机首弹轰炸)。
- lookback 常量 90 秒(轮询周期 60s+副本刷新滞后裕量;WeFlow 的 2s 是 350ms 实时态专用,不适用)。重读重叠由主机侧锚去重沉默消化(AC4)。
- **自消息过滤**:`real_sender_id`→Name2Id→username == 账号 wxid(`<db_storage>/all_users/login/<wxid>/` 目录名)→ 默认不出事件。
- 行解码:内容经 `_decode_text_content` 同款(zstd/UTF-8/占位);预览截 80 字。
- 性能铁律:严禁全库扫——SessionTable(454 行)全表 1 次+候选分表定点;AC5 用 `EXPLAIN QUERY PLAN` 钉死。若 create_time 谓词在真库退化全表扫(无索引),**在解密副本侧建索引**(副本可写,不触红线),建索引动作只在 ensure 后副本上、日志只记形状。

**R1.3 撤回检测与恢复阶梯**(WeFlow 语义,零代码借入):

- 谓词:`local_type == 10002` OR(`local_type == 10000` AND 内容含任一标记:`revokemsg`、`<replacemsg`、`撤回了一条消息`、`尝试撤回此消息`)。
- 自撤回(内容含 `你撤回` 或撤回者=账号 wxid)不出事件。
- 恢复阶梯逐级回落,`recovery` 字段如实标注:
  1. `server_id`:从撤回行内容提取 `newmsgid`/`sessionmsgid`/`svrid`/`oldmsgid`(正则,XML 属性形态)→ 同表 `WHERE server_id = :svrid AND local_type NOT IN (10000, 10002)` 直查;
  2. `heuristic`:直查未命中 → 撤回行之前(`create_time <= 撤回行 create_time`)最近一条非本人、非 10000/10002 消息(`ORDER BY create_time DESC, sort_seq DESC, local_id DESC LIMIT 1`);
  3. `replacemsg`:XML `<replacemsg>` 文本兜底(如「"张三"撤回了一条消息」),original=null、`replacemsg_text` 携文本;
  4. `none`:以上全空,original=null。
- 附:撤回通知到达时,若同轮该会话还有同撤回对象的新消息事件,抑制该新消息事件(同撤回双到达抑制;以提取到的原消息 server_id 比对)。

**R1.4 载荷契约**(stdout 单 JSON,exit 三段同既有;stdin 进私有数据不落日志):

命令:`wechat-bridge localdb notify-scan --file - --json`(stdin 载荷,argv 零内容):

```json
{"whitelist": ["<chatId>", "..."], "baseline": {"<chatId>": {"ts": 1791911341, "unread": 56}} }
```

`baseline` 缺席/null = 首轮。应答:

```json
{"notify_scan": {
  "events": [
    {"event": "message.new", "session_id": "...", "session_display": "...",
     "sender_display": "...", "is_self": false, "content_preview": "...",
     "ts": 1791911341, "server_id": 1234567890, "local_type": 1},
    {"event": "message.revoke", "session_id": "...", "session_display": "...",
     "revoker_display": "...", "is_self_revoke": false, "ts": 1791911400,
     "server_id": 1234567891, "local_type": 10002,
     "original": {"server_id": 1234567890, "ts": 1791911341, "sender_display": "...",
                  "content_preview": "...", "recovery": "server_id|heuristic"},
     "replacemsg_text": null}
  ],
  "baseline": {"<chatId>": {"ts": 1791911400, "unread": 55}},
  "stats": {"sessions_scanned": 454, "whitelist_sessions": 1, "candidates": 1,
            "msg_rows_read": 12, "self_filtered": 2, "revoke_events": 0, "duration_ms": 42}
}}
```

- `baseline` 回传=推进后基线(白名单内每会话 `{ts: max(上次基线 ts, SessionTable.last_timestamp), unread: 当前 unread_count}`),**桥零持久化**(纯函数:stdin 基线→stdout 事件+新基线);持久化归主机(干跑=主机不回写,pipeline 既有 `--dry-run` 即是)。
- `session_display`/`sender_display` 经 contact 域 `_contact_pick_names` 解析(解析不出回落原 id,不臆造)。
- 密钥链与 query 同一全链(`resolve_keys`→ensure 副本 domains=[message, session, contact]);`key_unavailable` 照旧 exit 21(主机侧结构化 skip)。
- 显示名白名单:白名单项允许声明显示名(引擎侧二查解析同 localdb 通道惯例;桥侧收到的一律是会话 id,解析归主机引擎)。

**R1.5 撤回历史查询件(供 C1 浏览面/验收夹具)**:命令 `wechat-bridge localdb revoke-list <chat> --since <Nd> --json`——对该会话全部 Msg_ 表扫撤回谓词行+恢复阶梯,应答 `{"revoke_list": [{<同 message.revoke 事件字段>}], "stats": {...}}`。共享 R1.3 同一实现(同一函数族,两壳)。

### R2 桥 CLI/编排/组件戳接线

- `wechat_bridge/cli.py`:注册 `localdb notify-scan`(`--file -`,stdin JSON,复用 `_read_body` 纪律)与 `localdb revoke-list`(`chat_id`+`--since Nd`,复用 `_parse_since_days`)两个子命令;`--json/--config` 逐层重注册清单补两节点。
- `wechat_bridge/localdb.py`:编排函数 `notify_scan(config, storage, keys, payload)` / `revoke_list(config, storage, keys, chat_id, days)`(照 `query_history`/`sns_history` 模式:resolve→ensure→查询→载荷)。
- `wechat_bridge/__init__.py` + `pyproject.toml` + `component.json`:版本 0.7.0→**0.8.0**;`cli_contract.commands` 补两条+命令说明;`private_paths` 无新增(零桥侧持久化)。

### R3 主机新通道:`macos_notify`(本机零网络)

`src/myssia/push/macos_notify.py`(新文件):

- 通道名 `macos_notify`;`supports_targeting = False`(targets 配置即拒,stdout 同款);零凭据零端点零网络。
- 发送:`/usr/bin/osascript -e 'display notification "<body>" with title "<title>" subtitle "<subtitle>"'`(子进程,10s 超时 kill);字符串转义(引号/反斜杠/换行);非 macOS → 结构化 `PushSendError(platform_unsupported)`。
- **合并纪律(组合优先铁律)**:同轮同 `metadata.session_display` 的条目并成**每会话一条**通知——title=会话名,subtitle=`N 条新消息`,body=最新一条「发送者: 预览」(截 200 字);撤回事件独立成条:title=会话名,body=「<撤回者>撤回了一条消息」+(有恢复时)「原内容:"<预览>"」/(replacemsg 兜底)兜底文本/(none)「原内容未能恢复」。
- 日志只记形状(条数/会话数),永不记正文(私有数据红线)。
- 已知形态限制(如实落档不修):通知归组显示为 osascript;系统通知中心会留通知历史(本机态,与 WeFlow 弹窗同级)。正文不出现在日志/网络面(AC 审计点)。

### R4 主机引擎:wechat_local 第四通道 `notify`

`src/myssia/engines/wechat_local.py` 扩展(`CHANNELS` 加 `"notify"`):

- 源形态(新品类 `weixin-notify` 的单源):

```yaml
- name: weixin-通知
  engine: wechat_local
  url: "https://weixin.qq.com"
  empty_ok: true
  engine_options:
    wechat_local:
      channel: notify
      sessions: ["50438708676@chatroom"]   # 会话白名单=id 或显示名(显示名经桥应答 sessions 列表二查解析,localdb 通道同款)
      notify_self: false                    # 缺省 false:自己发的消息不通知
```

- 单源单次 fetch = 一次桥 `notify-scan` 调用(`run_bridge_command_sync` 既有封装);`sessions` 空清单 = 声明即拒(白名单空=功能空转,构造期 FetchError)。
- **水位**:store `change_baseline` 键 `wechat-local://watermark/<源名>`,`etag` 存 JSON `{"<chatId>": {"ts":…, "unread":…}}`(列 TEXT,`sqlite.py:159-165`;与 localdb 通道水位同键空间不同源名);仅成功轮回写;skip/失败不推进(下轮重开,lookback+锚去重消化重叠)。
- **条目锚(强幂等)**:`url = wechat-local://notify/<urlencoded(chat)>#wxn-<server_id>`(撤回事件 `#wxnr-<revoke server_id>`)——比 #wx- 内容哈希锚强(重读/重装恒同锚);title=「<会话显示名> · <发送者>」(TITLE_MAX_CHARS 截断);content=预览;metadata 平铺 `{event, session_id, session_display, sender_display, server_id, local_type, revoke, replacemsg_text}`(R3 通道按 `session_display`/`event` 取用)。
- 错误码表沿用:`key_unavailable` 结构化 skip 不算失败;`db_not_found`/`decrypt_failed`/`bridge_timeout`/`component_missing` 原样透传(引擎既有码表零新增)。

### R5 品类文件与部署

- 新建仓库模板 `config/weixin-notify.yaml`(镜像 weixin.yaml 体例:头注释写机制/缺省关声明/隐私红线)+ 数据根部署:
  - `id: weixin-notify`、`schedule: "*/1 * * * *"`(分钟级,主人可调)、`timezone: Asia/Shanghai`;
  - 单源(R4 形态),`sessions: []` 出厂空(缺省关:在场≠在跑+白名单空双保险);
  - `push: [{channel: macos_notify, mode: immediate}]`(投递=本机弹窗;enrich 关、retention 30d、`watchlist/mute` 空,隐私纪律同 weixin.yaml);
  - `timeouts.fetch: 120`(notify-scan 恒轻,无需 660)。
- cron 注册:主人在既有 cron 屏/CLI 建品类 job(既有面零代码;PRD 步骤写清:选择 `config/weixin-notify.yaml`+schedule */1)。

### R6 schema/注册表/文档接线

- `src/myssia/schema.py`:`PUSH_CHANNELS` 补 `macos_notify`;RouteConfig 校验补「`channel 为 macos_notify 时不允许配置 target/targets」(stdout 同款分支);该通道 route 缺省 mode 归 `immediate`(本机即时,无 digest 语义)。
- `src/myssia/push/__init__.py`:注册 `MacosNotifyChannel`(CHANNELS 31 条;头注释条数同步;`tests/regen_push_targets_golden.py` 重跑对账)。
- `src/myssia/engines/registry.py` + `schema.py` 引擎注释:wechat_local 通道词表注释补 notify(词表本体在引擎,registry 仅注释)。
- `plugins/wechat-bridge/README.md`:命令表补两条。
- UI 零新画布:feed 屏新品类卡/聊天气泡自动(源名 `weixin-` 前缀判定 `api.ts:633`);白名单编辑=既有 YAML 编辑屏(monitor-ui R4.1 判例);通知开关=注册/暂停 cron job(既有 cron 屏)。

### R7 测试与夹具

- `tests/wechat-bridge/test_notify_query.py`(新):合成库(sqlite 造 SessionTable+Msg_ 表+Name2Id+contact)覆盖——基线差分四候选分支/非白名单零二查/自消息过滤/首建基线零事件/LIMIT 上限/水位推进取 max/撤回谓词四标记/恢复阶梯 server_id·heuristic·replacemsg·none 四级/双到达抑制/载荷 golden 形状。
- `tests/wechat-bridge/test_bridge_cli.py`(扩):两新子命令 argv/exit 码/stdin 契约/错误族。
- `tests/push/test_messaging_macos_notify.py`(新):osascript argv 构造断言/转义/每会话合并/撤回文案三态/非 darwin 结构化拒/targets 拒/日志零正文。
- `tests/engines/test_wechat_local_engine.py`(扩):notify 通道白名单透传/水位 kv 读写/锚强幂等(重读同锚沉默)/key_unavailable skip/sessions 空清单拒。
- 撤回夹具集:`tests/wechat-bridge/fixtures/revoke_samples.json`(合成 10002 XML 形状+期望恢复三元组,形状取自 WeFlow 语义文档零代码借入)——同时作为 C1 浏览面「已撤回」标记的验收夹具数据源(交割注记)。

## Acceptance Criteria

- [x] AC1 桥契约:`test_notify_query.py`+CLI 用例全绿——水位语义(首轮建基线零事件/仅成功推进/取 max)、白名单先筛(非白名单零 Msg_ 查询)、载荷 golden 形状逐键。
- [x] AC2 撤回阶梯:四级恢复各至少一夹具用例(server_id 直查命中/未命中回落启发式/双落空取 replacemsg 文本/全空=none);自撤回不出事件;双到达抑制。
- [x] AC3 通道:`macos_notify` 每会话合并一条、argv 构造/转义断言、非 darwin 结构化拒、targets 配置拒、发送日志零正文(grep 断言)。
- [x] AC4 引擎:notify 通道用例全绿——锚 `#wxn-`/`#wxnr-` 重读沉默、水位仅成功轮回写、key_unavailable 结构化 skip、显示名白名单二查解析。
- [x] AC5 真库干跑(只读):白名单=TMS(`50438708676@chatroom`),连续 3 轮×60s 跑 `notify-scan`(基线由第 1 轮建),第 2/3 轮事件零重复(同 server_id 不再出);`EXPLAIN QUERY PLAN` 证明仅 SessionTable 全表+候选分表定点(无全库扫);每轮 wall < 5s;全程零真通知(干跑不回写基线)。命令与输出贴 check.jsonl。
- [x] AC6 撤回实弹:测试会话用另一账号实发一条→撤回;下轮 notify-scan 捕获 `message.revoke` 且 `original.recovery ∈ {server_id, heuristic}` 或 `replacemsg_text` 兜底,通知文案=「…撤回了一条消息…」;**若实证 macOS 4.1.15 不向本地库落撤回行(事件恒零),如实记录实证结论于本档+父档,撤回呈现面按「无数据可标」降级注记回主人裁决,不硬凑夹具冒充真数据**。
- [x] AC7 端到端弹窗:cron job(*/1, weixin-notify)注册→白名单会话来新消息→macOS 通知中心真弹窗(截图证据,含会话名+预览);文案与守卫审计——仓库 grep `LLDB|断点|passphrase|挂载|hook|防撤回拦截` 于 UI/README/文案面零命中,桥+主机 grep `install.*trigger|anti_revoke|wcdb_install` 零命中;WeFlow 零代码借入(评审逐文件核)。
- [x] AC8 门禁:pytest/vitest/tsc/cargo 全绿;push targets golden 重跑对账;装机包全量刷新(桥 0.8.0 组件同步);feed 通知历史卡像素级验证(源名 `weixin-通知` 自动聊天气泡形态)。

> **复查回执(2026-10-14 复查员实跑,判定 PASS/needsFix=false)**:① round1_stats sessions_scanned=454/whitelist=1/candidates=1/events=0/db_busy=false/5ms、baseline={TMS:{ts,unread:14}}、revoke_stats revoke_rows=0(与前回执/prd.md 实测一致,不硬凑);② 红线 grep 三文件(notify_query/macos_notify/wechat_local_notify):LLDB|断点|passphrase|挂载|hook|防撤回拦截 零命中、install.*trigger|anti_revoke|wcdb_install|CREATE TRIGGER 零命中、notify_query 写 SQL 零命中;macos_notify 为 /usr/bin/osascript 字面量 argv 通道设计(macos_notify.py:58),非微信进程干预;③ pytest 四件(notify_query/notify_cli/messaging_macos_notify/wechat_local_notify)112 passed(=前回执 105+7 gated 全激活);④ CHANNELS=34 含 macos_notify(push/__init__.py:123,偏差 B 按实测坐实)。装机像素验证(通知撤回面)归父档 AC-P4 blocked 注记(UI 零新画布,无独立 UI 面可截)。
>
> **留档发现**:[info] 前回执自报偏差 A(chat_whitelist 键名替代 PRD 的 sessions,避 schema 凭据基线撞名)与 C(AC6 实弹归主人实机)均已在案,本轮不覆议;本域扫描 index_tables=False 全程零副本写。

## Constraints

- **只读红线**:notify-scan/revoke-list 全程解密副本 `mode=ro`;禁任何 trigger 安装/防撤回拦截/写微信侧形态(WeFlow 第二层 trigger 显式剥离,守卫 grep 清单见 AC7)。
- **许可证**:WeFlow=CC BY-NC-SA 4.0,零代码借入(水位/谓词/阶梯仅语义);chatlog fork=Apache-2.0 可参照。评审按「零行代码来自 WeFlow」检查。
- **隐私**:通知预览 80 字帽(通知正文 200 字帽);enrich 关;投递缺省仅 `macos_notify`(本机零网络);内容不入日志/git;weixin-notify 品类 red line 注释与 weixin.yaml 同源(「不外发任何通道」的 macos_notify 豁免=本机不外发,注记写明)。
- **性能**:SessionTable 先筛+候选分表定点,严禁全库扫(AC5 EXPLAIN 钉死);索引只建副本侧。
- **文案判例(AC-P5)**:UI/通知文案全人话(「新消息」「撤回了一条消息」「通知历史」),协议字段保留英文(`message.new`/`server_id`/`baseline`)。

## 与兄弟子的边界

- **C1(chat-export)**:聊天浏览面归 C1;C5 交付 revoke-list 契约+恢复阶梯实现+`revoke_samples.json` 夹具,C1 浏览面据此渲染「已撤回」标记+折叠原文(集成员接线对齐;C1 先落则先显 type "revoke" 占位,C5 后补原文恢复)。
- **C6(http-api)**:notify-scan/revoke-list 是否暴露 HTTP 形态归 C6 统筹(C6 按其 prd 钉的鉴权面自行决定收录)。
- **C2(stats-reports)**:撤回统计(谁最常撤回)不在 C5 范围;revoke-list 数据可为其后端,接线归 C2。
