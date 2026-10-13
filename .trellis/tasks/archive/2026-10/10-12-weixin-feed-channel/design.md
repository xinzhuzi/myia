# 微信入情报流 —— TG 全链形态的微信映射(design)

> 任务:10-12-weixin-feed-channel。主人令:「情报流里面是否有微信这个渠道?如果没有,
> 请你按照tg的UI设计方式,给微信也做一版」。本文档 = 拆解 TG 在情报流的全链形态,给出
> 微信品类/引擎/feed 层的组件级映射设计。**本档只设计,不含代码改动。**

---

## 0. G3 翻案记录(显式)

**主人 2026-10-12 指令翻案 G3,微信读回入情报流管线。**

- 原决议(10-11-wechat-ui-bridge prd.md:61/73,G3):读回消息**仅展示,不入情报管线**
  (store/dedup/分类均不接);「私人聊天当情报源」的产品语义另议。
- 本次主人令 = 对 G3 的直接翻案:微信消息经 wechat-bridge 桥读回后**入 store/dedup/feed**,
  与 telegram 同为情报流一等渠道。
- 原决议中仍有效的部分**不随翻案失效**:私有数据红线(内容不入 git/日志/报告原文)、
  静默铁律(不唤醒微信/不合成点击/不抢焦点)、像素验证 SMOKE 判例——本设计全程遵守。

---

## 1. TG 全链形态拆解(基线事实,全部实读)

### 1.1 feed 层(desktop/ui-src/src/screens/feed/)

三级信息架构(v8,feed-screen.tsx:169-178 `FeedView`):**作用域不进路由**,屏内 state 驱动
1→2→3 页面切换,Esc/返回钮逐级回退(`backLevel` :2824,3→2 时 kind 重派生)。

| 级 | 内容 | TG 形态落点 |
|---|---|---|
| 1 | 类型卡瀑布流(`feed-types-wall` :3435) | `TypeCard`(:1298)按 `CHANNEL_CARD_ORDER`(:981 api.ts,固定词表序 tg→site→daily)出卡;卡 = 类型头像 chip + 类型名/渠道数 + 今日/未读(stats 全库真值)+ 最新预览 3 条 |
| 2 | 该类型全渠道列表(`feed-channel-list` :3568) | `ChannelRow`(:1155,两行密度:名+时间 / 预览+未读徽标);**TG 专属账号区** `feed-tg-accounts`(:3579-3735,`telegram.status` 的 `web.accounts`,登录态●/○ + 管理钮→`/tg-account`) |
| 3 | 渠道详情 | TG = **聊天双栏**(10-11-tg-chat-two-pane):左栏 aside 监控会话列表 `feed-tg-group-pane`(:3808-3854,`tgGroupCards` :2510 = 渠道卡 kind=tg 成员,ChannelRow 复用)+ 右栏聊天头/工具条/气泡时间线 |

TG 专属件(feed 层的「TG 形态」本体):

1. **聊天气泡卡**:`FeedCard` 的 telegram 分支(:487-583)—— 频道名入泡顶
   (`channelDisplayName`,非节内语境)+ 窄泡 `w-fit min-w-[13rem] max-w-640px` + 正文气泡
   (点击=详情弹窗,弹开即已读)+ 泡底展开钮/时间;正文行 URL 段可点(`urlSegmentsOf`);
   无竖条/无元信息行(:470/:792 telegram 豁免)。聊天时间线 = 日期胶囊分组
   (`feed-chat-timeline` :4413)或平铺,气泡渲染与 `renderCard`(:2704)共用。
2. **监控台压缩条**(`feed-tg-console` :3873-3983,3 级聊天头 `ml-auto`):状态行
   (● 监控中·账号·自时刻 / 未登录警告)/ 扫码登录钮(`startWebLogin` :2855,
   `telegramWebLogin`)/ 原生网页预览钮(`launchTgNative` :2945)/ 管理钮(→`/tg-account`)/
   看全部历史消息(`openHistory` :2839,历史态=读态过滤豁免)。数据面 =
   `telegramGetStatus()`(settings/telegram-api.ts:65),`tgStatusNeeded` 门(:2592)=
   3 级 TG 渠道 ∨ 2 级 tg 页;phase 三层 idle/loading/ok/error(:2585-2616)。
3. **深链与原生窗**:`telegramKUrlOf`(api.ts:793)从条目 url 推导
   `https://web.telegram.org/k/#@<频道名>`(t.me 形态)或 `#<chatId>`(watcher 内部形态
   `web.telegram.org#tg-<chatId>-<msgId>`);`tg-native-window.ts` 窗口注册表
   (label `tg-native-<频道名>`,上限 3,`tg_native_open` Rust 建窗带返回钮)+
   工具条「情报视图/原生视图」段(:4016-4076,注意力表 + 存活红点)。
4. **进会话即已读**(10-12-tg-session-read,:2534-2574):`viewSource` 落到聊天会话 →
   `store.state.mark_all` 带 `source`(全库源级)+ stats 重拉角标归零;未读档顺手切「全部」。
5. **空态阶梯**(TG 三态 :4333-4368):状态未知(error+重试)/ 未登录(指引监控台)/
   监控在线(新消息预期词);零条目渠道/读态过滤空共用通用分支。
6. **判定词表**(api.ts,纯函数三件套):
   - `channelKindOf`(:646,条目五档 telegram>watch>document>deal>news):源名前缀
     `TELEGRAM_SOURCE_RE = /^(telegram|tg)[-_.]/i`(:628)**优先**,engine 词表次之
     (`engineMapFromHealth` :667,源→engine 映射来自 `health().categories`,零新 RPC)。
   - `channelCardKindOf`(:851,渠道卡三档 tg/site/daily):前缀优先 → tg;
     `TG_ENGINES = {tg_web, telegram, telethon, bot}`(:836)/`DAILY_ENGINES`(:839)词表。
   - `channelDisplayName`(:688):`SOURCE_DISPLAY_PREFIX_RE`(:682)剥 `telegram-` 等协议
     载体前缀显本名 —— 一屏一词,L2 行/卡面头区/详情弹窗共用。
   - 类型卡词表:`CHANNEL_CARD_LABELS`(:974)/`CHANNEL_CARD_ORDER`(:981)/
     `CHANNEL_KIND_ALIASES`(:940,搜索别名——「Tg」直出全部 TG 卡的主人实测主路径)。
7. **消费面**:数据全部走 `store.items`(`fetchFeedPage` api.ts:56,source 精确等值 +
   query 渠道内检索 + with_total);计数真值走 `store.source_stats`(STATS_PROTOCOL 门);
   渠道全集 = health 词表源 ∪ 已加载条目 source(`feedChannelCards` :890,零条目渠道也出卡)。

### 1.2 数据面(src/myssia + config/)

TG 三件 yaml(同品类 id=telegram,三线三文件):

| 文件 | 线 | engine | 源名规约 | 锚/去重 |
|---|---|---|---|---|
| config/telegram-channels.yaml | 公开频道网页预览 | `static_html`(普通链上引擎) | `telegram-<频道名>` | t.me 消息锚,{url} |
| config/telegram-groups.yaml | bot 线 | `telegram`(链外) | `telegram-<群原名>` | `#tg-<chat_id>-<mid>`,{url} |
| config/telegram-web.yaml | 网页线 | `tg_web`(链外) | `telegram-<群名>` | `#tg-<chat>-<mid>`(源 url 前缀入锚),{url} |

装配链(以 web 线为同构蓝本):

1. **schema 词表**:`ENGINES` 元组(schema.py:153-197)+ `EngineName` Literal(:262-273)
   收录 `telegram`/`tg_web`(装载期 fail-fast);`SourceConfig.url` 强制 http(s)
   (:825 `_check_url_scheme`)—— TG 线用真平台域做**锚**(`https://web.telegram.org`,
   「请求端点引擎自构」telegram-web.yaml:58)。
2. **链外注册**:`ENGINE_REGISTRY`(registry.py:107-161)在册、`AUTO_CHAIN` 不在 ——
   显式 `engine: tg_web` 才生效,单级链零降级(:204);auto 永不路过。
3. **引擎本体** engines/tg_web.py:`fetch()` 自持传输(Playwright persistent 配置档开
   Chromium 读 DOM)→ `updates_to_items` 复用 bot 线消息面(`#tg-` 锚 + 过滤管线)
   → 产出 `[{url, title, content, ...}]`;结构化空态词汇表:`session_missing`(配置档缺)/
   `tg_web_logged_out` / `tg_web_dom_stale`——绝不装死。
4. **入库盖戳**:pipeline.py `Item.from_extracted(raw, source.name)`(:466)—— 条目
   `source` = yaml 源名(即 `telegram-<频道>` 规约的落点),`category=self.config.id`
   (:1295)= `telegram`;`dedup.key: "{url}"` 模板(dedup.py `make_key` :91)渲染锚全串。
5. **feed 回读**:health()(entry.py:874,`myssia list --json` 等价)透出品类源词表
   (name+engine)→ 前端 `engineMapFromHealth` 装配判定词表;store.items 直读条目。
6. **常驻/批量双档**:批量 = cron schedule 批窗口;常驻 = `myssia telegram serve`
   (telegram/web_host.py)。feed 消费只认 store,与档位无关。

### 1.3 已就绪的微信地基(10-11 档交付,本任务直接消费)

- 桥组件 wechat-bridge 0.3.1(本机 `~/.myia/plugins/wechat-bridge` 已装):
  `sessions list --json` → `{sessions:[{id,name,unread,time,preview,conf}],count,...}`;
  `messages read <id> -k N` → `{messages:[{ts,sender,type:"text",text,side,conf}],count,
  chat:{requested_id,visible_title,match,note},ocr:{...}}`(pixel.py:1042/:1122,
  MessageRow.to_payload :200)。**硬边界:读到的是当前打开会话**(`chat.match` 如实,
  false 时消费方自行取舍,绝不张冠李戴)。
- sidecar 四方法(spec #81-84,desktop/sidecar-protocol.md:103-106):
  `wechat_local.probe/sessions/messages/query`,实现本体 `myssia.wechat_local_sidecar`
  (entry.py 三行薄壳);桥 bin 缺省落点 = `myssia.push.weixin_local.DEFAULT_BRIDGE_BIN`。
- 桥调用基建可复用:`bin_path` / `run_bridge_command_sync` / `parse_bridge_payload` /
  `probe_local_bridge`(src/myssia/push/weixin_local.py;wechat_local_sidecar.py:29-37 消费样例)。
- 前端探针封装已有:`wechatLocalProbe()` + `WechatLocalProbeView`
  (messaging/api.ts:421/:467),三态 ok/degraded/bridge_unavailable。

---

## 2. 微信映射设计

### 2.1 品类 config/weixin.yaml(G7:品类 id=weixin,feed 显示名「微信」)

单文件单线(对应 TG 的差异见 §3-②);字段形态逐节对齐 telegram-web.yaml:

```yaml
id: weixin
name: 微信监控

schedule: "*/30 * * * *"          # 批量档窗口读取(镜像 TG web 线节奏)
timezone: Asia/Shanghai

timeouts:
  fetch: 120                      # 单源一次桥读(截图+OCR)上界余量

sources:
  # 源名全称律(G7 对称纪律):weixin-<会话原名>,feed 渠道名/L2 行/日报分区
  # 匹配键;桥不能点击切会话(静默铁律),本源只在「当前打开会话」与声明
  # chat 匹配时产出(chat.match),不匹配 = 结构化空态,不张冠李戴。
  - name: weixin-<会话名>
    engine: wechat_local
    url: "https://weixin.qq.com"        # 锚(schema http(s) 形状要求;引擎零 HTTP)
    empty_ok: true                      # 当前会话不匹配/窗口零消息 = 合法空(doctor 口径)
    engine_options:
      wechat_local:
        chat: "<会话名>"                # 与像素链可见标题匹配(同 messages read 的 id)
        count: 50                       # 最近 K 条,1..200(协议上界 _LIMIT_MESSAGES_MAX)
        sides: [left]                   # 采集侧:缺省 left=对方消息;right=自己/center=系统行
    rate_limit: {qps: 0.5, jitter: "2s", backoff: exponential, respect_robots: true}
    proxy: direct
    retry: 1                            # 本机桥读,重试 1 防截图重打

watchlist: {keywords: [], mute: []}
classify: {builtin: false, rules: []}   # 首版全入库,筛选交给 feed 读态(见 §3-⑦)
dedup: {key: "{url}"}                   # #wx- 内容哈希锚(§2.3)
enrich: {enabled: false}                # 红线 3:私有内容不出本机(不送 LLM)
push: []                                # 红线 3:不外发任何通道;条目只入 store+feed
storage: {retention: 30d, vacuum: monthly}   # 隐私谨慎缺省(TG 90d;可配,见 §3-⑪)
```

要点:

- `url` 用官方域 `https://weixin.qq.com` 仅为**源锚与 schema 形状**(TG 判例:锚铸去重键、
  请求端点引擎自构;本引擎的「端点」是本机桥子进程,零 HTTP)。robots 面不适用
  (tg_web.py 同款论证:驱动的是已授权本机会话,不对任何站点发请求)。
- `push: []` 是显式红线声明(CategoryConfig.push 缺省即空表,schema.py:1761 —— 但写出来
  防后人误加飞书外发)。
- 品类显示名 `name: 微信监控`;feed 类型卡词面「微信」出自前端 `CHANNEL_CARD_LABELS`
  (§2.5),与品类 name 解耦(同 TG:品类 name「Telegram 监控」/ 类型卡「TG」)。

### 2.2 引擎 wechat_local(链外,子进程桥直调)

**对接面抉择:引擎直调子进程桥(`myssia.push.weixin_local` 的
`bin_path`/`run_bridge_command_sync`/`parse_bridge_payload`),不经 sidecar
(`myssia.wechat_local_sidecar`)。** 论证按 TG web 线同构:tg_web 引擎自持 Playwright
传输直读会话,`telegram.status` 等 sidecar 方法只是 UI 健康面,数据面从不绕道桌面 IPC;
微信引擎的数据面同理 = 管线进程内起桥子进程(与 wechat_local_sidecar.py:109 `_run_bridge`
同款封装,可在引擎侧复用同组 helper),`wechat_local.*` sidecar 方法保持纯 UI 探针/浏览面。
引擎跑在 cron/CLI 进程里,sidecar 可能根本不在场 —— 绕道 IPC 在 cron 档是死路。

装配三处(全部有 tg_web 判例可抄):

1. `schema.py`:`ENGINES` 元组(:153)与 `EngineName`(:262)各加 `"wechat_local"`
   (装载期 fail-fast);docs zh/en schema.md 词表同步(test_docs.py 一致性锁)。
2. `registry.py`:`ENGINE_REGISTRY`(:107)加链外条目
   `"wechat_local": lambda: _load("wechat_local", "WechatLocalEngine")`,AUTO_CHAIN 不进
   —— auto 永不路过(注释镜像 :155-160 tg_web 条目)。
3. `engines/wechat_local.py`(新):`fetch()` 流程 ——
   1. 解析 `engine_options.wechat_local`(chat 必填/count 1..200/sides ⊆ {left,right,center}
      缺省 [left]/read_timeout_seconds 缺省 60);形状错 = 结构化 FetchError。
   2. `bin_path(None)` 定位桥 bin;缺失 = 结构化 `component_missing`(与 sidecar 同码名,
      fix_hint 指设置组件卡)。
   3. `run_bridge_command_sync([bin, "messages", "read", chat, "-k", str(count), "--json"],
      "", timeout)`;`LocalBridgeTimeoutError` → `bridge_timeout`。
   4. 桥具名错误族原样透传为结构化空态/失败码(§6 码表:wechat_not_running /
      window_closed / screen_recording_denied(11 族) 等)—— 与 tg_web 的
      session_missing/logged_out/dom_stale 哨兵同纪律,绝不装死。
   5. `chat.match === false` → **结构化空态**(skip 理由 `chat_not_open`,title 人话
      「当前打开会话『X』与声明『Y』不匹配」);`match === null`(标题不可读)→ 同空态,
      理由 `chat_title_unreadable`。绝不把载荷归到不匹配源名下。
   6. `match === true` → 逐条装配(items 词表对齐 tg_web 产出口径):
      - `url` = `wechat-local://chat/<urlencoded(chat)>#wx-<sha1hex16>`(§2.3)
      - `title` = text 截断(TG 同律:标题=首行/全文截断)
      - `content` = text 全文
      - metadata:`sender`/`side`/`ts`/`conf`/`chat`(raw 面;feed v1 不投影,见 §2.4)
      - 过滤:`type != "text"` 跳过;`side` 不在声明 sides 跳过;`conf` 低于
        `min_conf`(缺省 0.5,与桥 VL 触发档一致)可选跳过(v1 先不配,全收)。
   7. 多源并发成本注记:每源一次桥读 = 一次截图+OCR;同轮多源会重复读同一窗口
      (像素链无会话切换)。v1 接受(声明源数少);后续可选:FetchContext 挂 per-run
      桥读 memo(tg_web 评论线程预算同款机制位),设计留口不预建。

### 2.3 锚与去重(#wx- 内容哈希锚)

TG 锚 = 平台消息 id(`#tg-<chat>-<mid>`,全期幂等)。微信像素链**没有消息 id**
(MessageRow 只有 ts(最近居中时间标记原文,无绝对日期)/side/text/pixel.py:190-205),
锚只能内容铸:

```
hash = sha1( chat_id | ts_marker | side | normalize(text) )[:16]   # normalize=压空白
url  = wechat-local://chat/<chat>#wx-<hash>
dedup key = "{url}"(品类 yaml,与 TG 三件同模板)
```

- 同窗重读同消息 → 同锚 → dedup 沉默(幂等目标达成)。
- **如实限制(§3-⑧)**:OCR 修字/置信度波动使文本微变 → 新锚 → 重复条目;ts 锚缺失段
  (时间标记是间歇出现的)内同文本同侧消息会并锚。缓解 = normalize 压空白 + side/ts
  入盐;残留重复靠 feed 读态消化,不静默去重假装无误差。
- `wechat-local://` 自定义 scheme(非 http(s))是**有意**:`isOpenableUrl`(api.ts:91)
  判 false → 卡面/右键/详情弹窗的「打开原文/复制链接」如实缺席 —— 私聊消息没有公开 URL
  (TG 的 t.me 公开锚是平台属性,微信没有对应物)。正文内粘贴的 http(s) 链接不受影响
  (气泡 URL 段渲染只认正文文本,api.ts:810)。

### 2.4 入库链(与 TG 逐点同构)

引擎 items → `Item.from_extracted(raw, source.name)`(pipeline.py:466)→
条目 `source = weixin-<会话名>`(盖戳规约=源名全称律,feed 侧 `channelDisplayName` 剥
`weixin-` 前缀显会话本名)→ `category = "weixin"`(:1295)→ dedup `make_key("{url}")`
→ store.upsert(first_seen=入库时刻)→ **feed 消费零新 RPC**:

- `store.items` 白名单投影(entry.py `_item_dict` :1595)已覆盖气泡卡所需全部字段
  (url/title/content/source/category/读态三键);`sender/side/ts` 留在 raw 不投影
  —— feed v1 气泡卡不需要(频道名行=源名,与 TG 同形);若后续要在群聊气泡显示发送者,
  再走白名单扩键 + PROTOCOL_VERSION bump + 契约测试字面量三处同步(bump 教训,档 44d541f)。
- `health()`(entry.py:874)自动透出 weixin 品类源词表(engine=wechat_local)→
  前端 `engineMapFromHealth` 零改动即带上 → 渠道墙/类型判定自动成立。
- `store.source_stats` 分源聚合按 source 精确等值,weixin-<会话> 天然成行。
- cron:schedule 声明即被既有 cron 装配收录(telegram-web.yaml 同款,零新机制)。
- 日报(daily-digest.yaml):**不设微信分区**(红线 3:日报是外发产物);weixin 条目
  因 push: [] 本就不进任何 push 面,分区匹配键(源名)不写即不沾。

### 2.5 feed 层组件级设计(文件落点/复用件)

复用优先:微信的 feed 形态 = TG 形态的**第四类型档 + 气泡渲染共用**,新增文件零个
(全部在既有文件扩词表/扩分支);唯一新 api 文件不需要(probe 复用 messaging 封装)。

**A. api.ts(词表三处 + 判定两函数)**

| 落点 | 改动 |
|---|---|
| `ChannelKind`(:625) | 加 `"weixin"` 五档→六档 |
| `channelKindOf`(:646) | 加 `WEIXIN_SOURCE_RE = /^(weixin|wx)[-_.]/i` 前缀判定,**列于 TELEGRAM_SOURCE_RE 之后、engine 词表之前**(前缀优先同门) |
| `ChannelCardKind`(:832) | 加 `"wx"` 三档→四档 |
| `channelCardKindOf`(:851) | weixin 前缀优先 → `wx`;`WX_ENGINES = {"wechat_local"}` 词表次之 |
| `SOURCE_DISPLAY_PREFIX_RE`(:682) | 加 `weixin\|wx` —— `channelDisplayName` 剥前缀显会话本名(一词一源纪律) |
| `CHANNEL_CARD_LABELS`(:974) | 加 `wx: "微信"`(G7 显示名落点) |
| `CHANNEL_CARD_ORDER`(:981) | `["tg", "wx", "site", "daily"]` —— IM 双档相邻,心智模型序 |
| `CHANNEL_KIND_ALIASES`(:940) | 加 `wx: ["wx", "weixin", "微信", "wechat"]`(搜索「微信/wx」直出整档,v6.1 主人实测主路径同门) |

**B. feed-screen.tsx(组件扩档)**

| 落点 | 改动 |
|---|---|
| `CHANNEL_KIND_META`(:149) | 加 `weixin: {label:"微信", Icon: MessageCircle, className:"text-[#07C160]"}`(lucide MessageCircle;微信官方绿 #07C160,与 messaging/platform-icons.tsx:232 weixin_local 品牌色同源;暗卡底对比 ≈6.9:1 过 4.5 档,F8 审计口径) |
| `CHANNEL_CARD_META`(:159) | 加 `wx: {label:"微信", Icon: MessageCircle, className:"text-[#07C160]"}` |
| `CHANNEL_ROW_AVATAR_TONE`(:1149) | 加 `wx: "bg-[#07C160]/10 text-[#07C160]"`(tg 的 primary 淡档同构) |
| `FeedCard` 气泡分支(:487/:470/:792/:846) | 条件 `kind === "telegram"` → `kind === "telegram" || kind === "weixin"`(气泡/泡顶频道名/无竖条/无元信息行/正文 URL 段全套共用;`data-kind=weixin` 由 item kind 自然带出) |
| `chatView`(:2496) | `activeChannelKind === "tg" || === "wx"`(3 级双栏对 weixin 生效) |
| `tgGroupCards`(:2510) | 改名/泛化 `imGroupCards` = kind ∈ {tg, wx} 成员(左栏「监控会话」对微信同出;testid `feed-tg-group-*` 结构词不动,新增 `data-im-kind` 之类的区分留给实现期定) |
| 进会话即已读 effect(:2534) | `chatView` 派生值已覆盖(改的是 chatView 定义本身),微信会话同享 mark_all(source) 语义 |
| 3 级聊天头(:3861-3985) | TG 分支保持;新增 **wx 监控台压缩条**(`feed-wx-console` testid):状态行(probe 三态:● 桥在线 · 微信 <版本>/ degraded · 首因/ 不可用)+ 管理钮(→`/messaging`,微信本机工作区在消息屏,非独立屏)+ 看全部历史消息(openHistory 复用);**无扫码登录钮、无原生网页预览钮**(§3-④⑤)。数据面 = `wechatLocalProbe()`(messaging/api.ts:467,import 复用 telegram-api 同位:117),`wxProbeNeeded` 门镜像 `tgStatusNeeded`(:2592) |
| 原生视图段(:4016) | `isTgChannel` 门保持 TG 专属 —— wx 不渲染(如实无钮) |
| 2 级渠道页(:3579) | TG 账号区 `view.kind === "tg"` 保持;新增 `view.kind === "wx"` **桥状态区**(镜像账号区结构:probe 三态 pill + 版本行 + reasons 列表 + 「到消息屏处理」钮;单卡无列表 —— 微信单本机客户端无账号概念,§3-⑫);testid `feed-wx-bridge-*` 族 |
| 空态阶梯(:4333-4368) | 新增 wx 分支(在 TG 三态之后、通用零条目之前):probe error →「桥状态未知+重试」;`bridge_unavailable` →「桥不可用(组件未装/微信未运行)+ 前往设置」;`degraded` →「桥降级(<首因>:窗口未开/屏幕录制权限)+ 指引」;`ok` →「桥在线,暂无新消息入库(当前打开会话需与声明的监控会话匹配)」 |
| 键盘/巡游/详情弹窗 | 零改动(环集合来自 displayItems/visibleChannels 派生,类型档扩展自动兼容) |

**C. 深链与原生窗:有意缺席。** `telegramKUrlOf`/`tg-native-window.ts` 无微信对应物
——微信无公开网页镜像可从条目推导,`wechat-local://` 锚也无从换算任何可开 URL。
设计定案:**不造**「打开微信会话」深链(桥静默铁律禁点击切会话,任何「跳到会话」的
按钮都是谎言);3 级聊天头只承载「回消息屏看桥态」的管理动线。

**D. TypeCard/ChannelRow 渲染**:零组件改动 —— 词表扩展后 `CHANNEL_CARD_META[kind]`/
`CHANNEL_ROW_AVATAR_TONE[kind]` 索引自动成立;`aggregateTypeCards`(:1021)按
CHANNEL_CARD_ORDER 归并,wx 档自动出卡(成员 = health weixin 源 ∪ 条目 source)。

---

## 3. 有意差异清单(与 TG 逐条如实)

1. **像素链读「当前打开会话」语义**:桥不能点击切换会话(静默铁律,README:48),每轮
   只读微信主窗当前打开的会话;源声明 chat 与 `chat.match` 不符 = 结构化空态
   `chat_not_open`,绝不张冠李戴。TG 的 Playwright/bot 线可主动定位任意 chat —— 微信不能。
2. **无 bot/web 双线,只有本机桥一线**:TG 三件 yaml 三条采集线,微信首版单引擎
   (`wechat_local`)单 yaml;`localdb query`(D4 密钥途径)是另一条潜在深历史线,
   本任务不接(密钥未闭合,E1 实测负结论在档)。
3. **首版会话范围 = 最近 K 条**(像素窗口现存,缺省 50,上界 200):不滚动翻历史
   (深历史是微信客户端滚动加载面;tg_web 批量档同款窗口语义,但 TG 有 serve 常驻档
   兜新消息,微信首版只有批量档 —— 窗口外消息若期间未被读到即漏采,如实)。
4. **无深链/无原生视图/无公开镜像**:TG 的 `telegramKUrlOf` /k/ 深链 + 原生窗 +
   t.me/s 镜像三件,微信零对应;条目 `wechat-local://` 锚不可打开,「打开原文/复制链接」
   如实缺席。
5. **无登录流**:TG 监控台有扫码登录钮(`telegramWebLogin`);微信桥消费本机已登录的
   桌面客户端,登录动作发生在微信本体,监控台只报 probe 三态(含屏幕录制权限指引)。
6. **私有数据不出本机**:`enrich.enabled: false` + `push: []`(红线 3);TG 三线都有
   feishu archive/即时出口。微信条目只进本机 store+feed。
7. **零 LLM 筛选**:TG 引擎内置关键字粗筛 + LLM 精筛(score≥8 即时);微信 v1 不做
   (红线 3 同根),`classify.builtin: false` 全入库,筛选交给 feed 读态/星标。
8. **锚 = 内容哈希,非平台消息 id**:`#wx-<sha1(chat|ts|side|text)>`;OCR 文本微变会
   另立新锚(重复条目风险),ts 间歇锚缺失段同侧同文本并锚 —— 与 `#tg-<chat>-<mid>`
   的全期强幂等不可比,如实。
9. **条目 url 自定义 scheme**(`wechat-local://`):isOpenableUrl false(见 §2.3)。
10. **3 级左栏数据源 = yaml 声明源**:TG 左栏监控会话 = store/health 渠道全集;微信首版
    同构(声明即显示),桥 `sessions list` 的全会话清单**不接** feed(留后议:接了会把
    未声明会话也铺进左栏,与「声明制监控」的 v1 语义冲突)。
11. **retention 30d(TG 90d)**:私聊内容隐私谨慎缺省;敏感会话可再单源改短,反之也可调长。
12. **2 级无账号区,改桥状态区**:TG 多账号列表(telegram.status web.accounts);
    微信单本机客户端,无账号概念,状态区 = probe 三态单卡。

---

## 4. 测试面与 golden/契约纪律(实现期清单)

- **引擎**:`tests/engines/test_wechat_local_engine.py`(新,镜像 test_tg_web_engine.py
  形态):engine_options 形状/桥缺失 component_missing/match=false 空态/sides 过滤/
  锚稳定性(同文本同窗同锚、微变文本另锚)/超时桥接 —— 全 mock 桥子进程,零真机。
- **registry/schema**:`tests/engines/test_registry.py`(词表↔注册表同步断言)、
  `tests/test_schema.py`(ENGINES fail-fast)、docs 一致性(test_docs.py/test_skill_doc.py,
  zh/en schema.md 词表同步)。
- **feed 前端**:`feed-screen.test.tsx` 增 wx 档用例:类型卡第四档词面/顺序、气泡卡
  `data-kind=weixin`、3 级双栏 + wx 监控台三态、2 级桥状态区、空态阶梯 wx 分支、
  搜索别名(「微信」「wx」直出);`api` 纯函数用例(channelKindOf/channelCardKindOf/
  channelDisplayName 的 weixin 前缀档)。
- **golden 纪律(铁律 5)**:动品类面必同步 golden 基件 —— 本批 golden 面 =
  feed 层既有断言快照与 push_targets golden 不沾(无 push 改动);若实现期引入 UI 快照
  基件,wx 档入快照必须与词表同步再生成。
- **契约测试字面量(铁律 5,bump 教训 44d541f)**:本设计**零 sidecar 新方法、零
  _item_dict 投影扩键 → 不 bump PROTOCOL_VERSION** → `tests/desktop/
  test_desktop_sidecar_protocol.py` 版本断言零改;若实现期决定投影 sender/side(§2.4
  留口),须 bump 三处同步(entry.py PROTOCOL_VERSION + api.ts 能力门 + 契约测试字面量)。
- **SMOKE 判例(铁律 2)**:像素验证只走 `MYIA_SMOKE_GEOMETRY=WxH+X+Y` 形态;
  静默铁律全程(不唤醒微信/不合成点击/不抢焦点)。

---

## 5. 红线对齐核对

| 红线 | 本设计的落点 |
|---|---|
| 私有数据(prd 红线 6/任务铁律 3) | 微信内容只活在桥 stdout 载荷 → 管线内存 → myssia.db(store);enrich 关/push 空/日报无分区;设计档与后续报告只留形状(本文档零消息原文) |
| 静默(铁律 2) | 引擎只消费桥既有只读命令;不新增任何写通道/点击/激活;SMOKE 判例如上 |
| git 纪律(铁律 1) | 实现批 pathspec 限定;不碰并行会话 M 状态文件(desktop/entry.py 动前先核 git status——本设计恰好不动 entry.py) |
| 品类命名(铁律 4/G7) | id=weixin / feed 词面「微信」/ config/weixin.yaml / 源名 `weixin-<会话名>` |
| 勿往仓库 .venv 装包(铁律 6) | 引擎零新依赖(桥子进程是受管组件,不在仓内装) |
