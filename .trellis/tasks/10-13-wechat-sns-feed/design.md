# Design:微信朋友圈进情报流

侦察实证(2026-10-13,全部真跑):sns.db 在场/钥匙 20 覆盖/最新动态 42min/
XML 形状/通知 type 语义(1=赞 182 条,2=评论 67 条)。本档是执行者零歧义契约。

## §1 总体(四层,只读链路)

```
weixin.yaml 源(channel: sns, feed_kind: feed|notices)
  → WechatLocalEngine._fetch_sns(水位开窗)
  → wechat-bridge localdb sns feed|notices --since Nd --json(子进程)
  → E2 解密副本(sns 域新增,TTL/容量/源新即重建生命周期自动纳管)
  → E3 sns_query.py:SnsTimeLine XML 解析 / SnsMessage_tmp3 SQL 直查
  → 条目(#wxsns-<id> / #wxsnsn-<local_id> 强锚)→ store+feed
```

零 UI 改动:源名 `weixin-` 前缀 → 渠道卡/双栏/气泡自动归微信渠道
(feed-screen `channelCardKindOf` 按 engine 判 wx,engine 不变)。

## §2 桥:域与命令

### 2.1 域映射(`localdb.py`)

`DOMAIN_DB_FILES` 追加 `"sns": ["sns/sns.db"]`。**`DEFAULT_DOMAINS`
(message/session/contact)不动**——query 命令的缺省解密面零变化,sns 副本
只在 sns 命令显式请求时解密(按需,不摊 query 成本)。

### 2.2 CLI(`cli.py`,形态对齐 key-provider 多层子命令先例)

```
wechat-bridge localdb sns feed    --since 3d --json   # 动态
wechat-bridge localdb sns notices --since 3d --json   # 互动通知
```

- `--since` 复用 `_parse_since_days`(严格 `Nd` 形态,usage 拒同款)。
- `localdb sns` 子命令组不跑 UI 前置(localdb 族同纪律,零截窗零 AX)。
- 密钥链复用 `resolve_keys`(keys.json/取钥器/自愈/E1 同一全链;sns 钥匙
  已在 20/20 映射内,零新取钥面)。
- 版本 0.5.1 → 0.6.0(`__init__.py`/`pyproject.toml`/`component.json`
  三处同步;docs 无版本引用面)。

### 2.3 查询本体(新文件 `wechat_bridge/sns_query.py`)

**feed**:`SELECT tid, user_name, content FROM SnsTimeLine` 全表拉取 →
逐行 `xml.etree.ElementTree.fromstring`(stdlib;~4408 行 × 3KB 实测量级
亚秒级)→ 解析契约:

| 字段 | XPath(相对 TimelineObject) | 缺失行为 |
|---|---|---|
| id | `id` | 缺失/空 → 该行弃,计入 `parse_errors` |
| username | `username` | 同上(作者锚,必须有) |
| create_time | `createTime` | 非数字 → 弃行计 parse_errors |
| text | `contentDesc` | 可空(纯图/纯视频条目) |
| media | `ContentObject/mediaList/media` 列表 | 每条取 `type`;计数 |
| 转发源 | `sourceUserName` + `sourceNickName` | 可空;非空时入行 |

- 窗口过滤在 Python(createTime 在 XML 内,SQL 层无时间列):窗口外的行
  计入 `rows_out_of_window` 不进载荷(**解析在全表跑**,过滤后返回;估算
  4408 行×3KB ≈ 亚秒级,**实现时实测**——若 >2s 再加正则前置过滤 createTime
  快速路径+漏网慢路径兜底,v1 不做 tid 单调性赌博)。
- **解析失败不炸整轮**:单行 XML 坏/字段缺失 → 弃行 + `parse_errors` 计数
  (宁缺毋假,localdb_query 既有纪律)。**media type 数字语义不臆造**
  (2=图/4=视频未实证):media_types 原样透传供消费方自判,标题回退链
  不依赖它。
- **SnsTimeLine 无 is_relative_me 列**(实探列清单):自筛「自己发的」无据,
  feed v1 全收。
- nickname 解析:作者 wxid → contact 域反查(`_contact_pick_names` 复用);
  contact 域缺位/未解出 → nickname=None,消费方回落 username(如实)。
- 排序:create_time 升序返回(时间线顺序,旧→新;消费方零排序假设)。

**notices**:`SELECT local_id, create_time, type, from_username,
from_nickname, feed_id, content, is_relative_me FROM SnsMessage_tmp3
WHERE create_time >= ? ORDER BY create_time ASC`(窗口过滤在 SQL,同
query 形态)。type 映射 `1→"like"` / `2→"comment"` / 其余原样数字字符串
(未知类型如实透传,不臆造词面);**is_relative_me 原样透传**(真跑 3 条
赞全 0——语义未实证,消费方词面中性不依赖它);**feed_id 列是 INTEGER
雪花 id**(真跑实锤),载荷统一转 str。

### 2.4 载荷契约(stdout 单 JSON,键序稳定——golden 对账)

```jsonc
// feed
{"sns": {"mode": "feed", "since_days": 3, "feed": [
    {"id": "1503...", "username": "wxid_...", "nickname": "张三",
     "create_time": 1791891649, "text": "正文…",
     "media_count": 2, "media_types": ["2", "2"],
     "ref_username": null, "ref_nickname": null}],
  "rows_total": 4408, "rows_out_of_window": 4370, "parse_errors": 0,
  "content_decode": {"zstd_available": true},
  "domains": {"sns": "ok", "contact": "ok"}, "copy": {…E2 应答原样…}}}

// notices
{"sns": {"mode": "notices", "since_days": 3, "notices": [
    {"local_id": 123, "create_time": 1791649574, "type": "like",
     "from_username": "wxid_...", "from_nickname": "猫三三",
     "feed_id": "-3417…", "content": null, "is_relative_me": 1}],
  "rows_total": 249, "parse_errors": 0, "domains": {...}, "copy": {...}}}
```

错误族:`db_not_found`(20)/`key_unavailable`(21)/`decrypt_failed`(22)
与 query 同码同语义,零新码。

## §3 引擎(`src/myssia/engines/wechat_local.py`)

### 3.1 通道词表

`CHANNELS = ("pixel", "localdb", "sns")`。sns 专属选项(**交叉声明即拒**,
既有纪律):

| 键 | 词面/型 | 缺省 | 语义 |
|---|---|---|---|
| `feed_kind` | `feed`/`notices` | `feed` | 动态/互动通知 |
| `since_days` | 1-3650 int | 3 | 首拉/无水位窗口 |
| `read_timeout_seconds` | 正数 | 600 | 桥命令超时 |

- sns **不消费** `chat`/`sides`/`count`:chat/sides 是会话语义,朋友圈无
  会话概念(自己发的朋友圈 v1 也不筛——feed 全收,`is_relative_me` 是
  SnsMessage 的列不是 SnsTimeLine 的,自筛无据不臆造)。声明即拒
  (`invalid_engine_options`,消息写明该键属哪通道)。
- pixel/localdb 声明 `feed_kind` 同拒。

### 3.2 锚(强幂等,本任务核心升级)

- feed:`wechat-local://sns/<id>#wxsns-<id>`(id = 微信侧全局 id,XML 实证
  全期稳定;**比消息通道的内容哈希锚强**,TG `#tg-` 同级)。
- notices:`wechat-local://sns/notice/<local_id>#wxsnsn-<local_id>`
  (local_id = 表主键,数据不变则不变)。
- 标题:text 非空 → 首行截 80 字符(TITLE_MAX_CHARS 同律);text 空 →
  `[图片×N]`(media_count>0)/`[朋友圈动态]`(兜底;**视频型判别不做**,
  media type 数字语义未实证)。通知标题**中性词面不假设归属**(通知含
  好友间互动,is_relative_me=0):`{from_nickname} 赞了朋友圈动态` /
  `{from_nickname} 评论了朋友圈动态:{content 截断}`。
- content:动态 = text(空则媒体占位文);通知 = content(评论原文)或赞
  占位。metadata:`kind:"sns"`/`sns_kind`/`username`/`nickname`/`ts`/
  `media_count`(raw 面,feed v1 不投影)。

### 3.3 水位

复用既有机制零改动:`watermark_key(源名)` + `_read_watermark`/
`_advance_watermark`(`--since` 天数 = ceil(水位差),仅成功推进)。两源
独立水位(键含源名,天然隔离)。

### 3.4 skip 语义与水位防御

`key_unavailable` → 结构化 skip(密钥缺位合法预期态,last_skip_reason
置位,零条目不告警)——localdb 同款。sns 首查触发副本首建,超时缺省
600s 同 localdb 判例。

**可疑空水位防御**(grill 挑刺补):feed 应答零条目且 `parse_errors > 0`
(XML 坏行吞噬整窗的形状)→ **不推进水位**(下轮重开同窗;微信 XML
格式变化时中间窗口不丢);正常零条目(安静窗,parse_errors=0)照常推进。
notices SQL 直查无解析面,零条目恒正常推进。

### 3.5 源 YAML 形态(live + repo 样例注释)

```yaml
- name: weixin-朋友圈            # 源名全称律(渠道归属+去重键)
  engine: wechat_local
  url: "https://weixin.qq.com"
  empty_ok: true
  engine_options:
    wechat_local:
      channel: sns
      feed_kind: feed
      since_days: 3
- name: weixin-朋友圈互动
  … feed_kind: notices …
```

## §4 测试

- 桥(`tests/wechat-bridge/`):`test_sns_query.py`——合成 XML 夹具
  (正文/纯图/转发/坏 XML 四形态)+ notices type 映射 + 窗口过滤 +
  contact 缺位回落;golden_cli_payloads.json 加 `localdb_sns_feed`/
  `localdb_sns_notices` 两锚(合成载荷,真跑形状对齐)。
- 引擎(`tests/engines/test_wechat_local_engine.py` 追加):sns 通道
  options 校验(交叉拒)/feed+notices 条目铸造/锚稳定性(同窗重读同锚)/
  水位推进与 skip 不推进/超时与错误族映射。
- 既有 localdb/pixel 测试零改动(行为不变证明)。

## §5 风险与边界

- **tid 不单调**:已实证不可赌(SQL 无时间列),全表解析过滤是 v1 正解;
  性能实测亚秒级,4408 行增长到十万级再议(非目标)。
- **XML schema 漂移**(微信升级改字段):解析失败 → 弃行计数,不炸整轮
  (宁缺毋假);parse_errors 持续高位是升级信号,消费面如实可见。
- **隐私**:朋友圈内容红线 = 消息红线同款(只活桥 stdout→内存→store;
  日志形状级;不入 git;enrich/push 结构性关)。
- **SnsMessage_tmp3 表名漂移**(tmp3 后缀疑似版本产物):v1 直查
  `SnsMessage_tmp3`,缺表 → 结构化 `db_not_found` 形状错误(微信版本变化
  如实报,红线 7 同款),发现式查询是过度设计。**local_id 稳定性注记**:
  通知表清空/重装微信会让 local_id 重置 → 通知重发(新锚),feed 读态
  消化,如实接受(v1 注记,不做对账)。
- **并行会话避让**:桥文件干净(0.5.1 已提交);`.trellis/tasks/
  10-13-wechat-key-subsystem/`(planning)与归档档 1 行注记属并行会话,
  提交时 pathspec 圈定本任务文件,不收编。

## §6 回滚

纯加法(新命令/新通道值/新源),回滚 = live yaml 删两源(数据面即停)+
桥版本回落;store 既有条目随 retention 30d 自然过期,无 schema 迁移。
