# Research: 微信消息 → feed 条目 → 3 级气泡真图 全链图谱(chain-map)

- Query: PRD 五问深挖(消息链/通路选型/渲染点/httpapi 与 media-cache/并行撞面)
- Scope: internal(纯只读零改动;git log/diff + 源码阅读)
- Date: 2026-10-17

---

## Q1 微信消息 → feed 条目链:字段、消费方、媒体丢失点

### 双消费链先分清(关键前提)

微信本地库数据有**两条互不相同的消费链**,PRD 待探①把它们混在一起了:

| 链 | 路径 | 用途 |
|---|---|---|
| **feed 采集链** | `src/myssia/wechat/engine.py` → 桥 `localdb query` → FeedItem 入 store | 情报流 3 级工作台的数据源(**本任务目标链**) |
| 桌面消息浏览链 | UI → sidecar `wechat_local.page` → 桥 `localdb page` | messaging 屏的会话浏览器(`desktop/ui-src/src/screens/messaging/wechat/wechat-local.tsx`),与 feed 无关 |

### feed 采集链逐跳(带锚点)

1. **品类配置**:`config/weixin.yaml`(注意:任务描述写 `config/config/`,实际仓库路径是根下 `config/`;打包映射 `desktop/src-tauri/tauri.conf.json:61` `../../config/weixin.yaml → config/weixin.yaml`;运行期数据根同名为 `<home>/config`)。源声明 `channel: localdb`、`chat`、`since_days`(weixin.yaml:85-97 二源样例)。
2. **引擎拉取**:`src/myssia/wechat/engine.py:567` `_fetch_localdb` → `engine.py:609-630` `_run_localdb_query`,argv = `localdb query <chat_id> --since Nd --json`(engine.py:618)。
3. **桥查询本体**:`plugins/wechat-bridge/wechat_bridge/localdb_query.py:423` `query_messages`——**只选 time/content/type/sender 四列**(localdb_query.py:445-450,列清单 `time, content, type, sender, sender_id, ct_content`),条目形状 `{ts, sender, type, text?|media_placeholder?}`(localdb_query.py:433-434)。**不选 `packed_info_data`,不提取媒体 key**——媒体信息在桥 query 应答里根本不存在(weixin.yaml:70 注释也自证:"localdb query_messages 只选时间/内容/类型/发送者四列,2026-10-13 实探")。
4. **引擎过滤(媒体第二丢失点)**:`engine.py:908-912`——
   ```python
   if message.get("type") != "text":
       skipped_type += 1  # v1 全文本;媒体行是类型占位(media_placeholder)
       continue
   ```
   图片行(type="image")**整行丢弃**,只计数进日志。
5. **条目构造**:`engine.py:955-972` `_localdb_message_to_item` → `{url(#wx- 内容锚), title, content, sender, side, ts, chat}`,注释明示"feed v1 不投影"后四键(进 metadata/raw 但协议面不出)。
6. **入库**:`item.metadata` → `raw`(entry.py:1546 注释:"pipeline 以 raw=item.metadata 入库")。
7. **读出投影**:`desktop/entry.py:1546` `_item_dict` 白名单投影——**`image_files` 已在白名单**(entry.py:1574-1580:全项非空 str 才投影,坏值整体置 None)。即:**若引擎侧往条目写 `image_files` 键,协议面零改动直达 UI**。
8. **UI 消费**:`desktop/ui-src/src/screens/feed/api.ts` FeedItem 带 `image_files`;feed-screen.tsx:233-239 `hasImageDetails` 把 `image_files` 算进可展开判定;feed-screen.tsx:1119(卡展开态)与 1896(详情弹窗)渲染 `<FeedLocalImages paths={item.image_files}>`(并行会话刚落的,见 Q5)。

### page API 输出字段(messaging 链,对照用)

`localdb_page.py:687-694` 条目 = `{seq, ts, sender, sender_id, type(类型名), local_type(原始 int)}` + `text|placeholder`(localdb_page.py:711-714)。**有 `local_type` 数值但没有媒体 key、没有 `packed_info_data`**(key 提取只存在于 media.py 的 `scan_chat_media`)。`localdb_export.py` 是六格式文件导出器(json/txt/csv/md/html/xlsx;localdb_export.py:61),复用 run_page 流(localdb_export.py:244-259),与 feed 链无关——PRD 撞面担忧的 export 改动不触及本链。

**结论(媒体丢在哪一步)**:两处——桥 `query_messages` 不选 packed_info_data(丢 key 源数据)+ 引擎 `engine.py:911` 非 text 行整行跳过(丢条目)。要让 3 级出图,两条都得动;现成的 `media_scan`(sidecar 已通,见 Q4)是拿 key→dat→cached_path 的既有通道。

---

## Q2 图到 webview 通路选型

### 现状装机件盘点

- **UI 取数据形态**:全部走 `invoke("sidecar_request", {method, params})` → desktop/entry.py `_HANDLERS` 薄壳(如 entry.py:4600-4615 `_m_wechat_local_media_scan/_m_wechat_local_media_decrypt`)→ `src/myssia/wechat/sidecar.py:443-455` `_ACTIONS` 封闭词表 → 一次性桥子进程。**UI 从不经 HTTP 拿业务数据**。
- **桥 httpapi 有无 UI 直连先例**:**没有**。`rg '5032|http_api' desktop/ui-src/src` 零命中;`localdb serve` 只有 CLI 入口(plugins/wechat-bridge/wechat_bridge/cli.py:487-495, 1371),main.rs/entry.py 均不 spawn 它。httpapi(10-14-wechat-http-api)当前是无桌面消费方的独立能力。
- **assetProtocol scope 现状**(tauri.conf.json:26-31,HEAD 已含):
  ```json
  "assetProtocol": { "enable": true, "scope": ["$APPDATA/wechat-localdb/media-cache/**"] }
  ```
  CSP img-src = `'self' data: asset: http://localhost`(HEAD;工作树并行会话加了 `http://asset.localhost`,见 Q5)。
  ⚠️ **静态 scope 根不匹配(与 PRD 假设冲突,如实标注)**:桥数据根 = `myssia_home()` = `~/Library/Application Support/MYIA`(config.py:151-162;Rust 侧同值 main.rs:611-624 且 spawn 时注入 `MYIA_HOME`,main.rs:417-418)。media-cache 实际落点 = `.../Application Support/MYIA/wechat-localdb/media-cache`(media.py:152-155)。而 `$APPDATA` 无论解析为裸 `Application Support` 还是 identifier 域,都**不含 `MYIA` 段**——即该静态 scope 条目在缺省安装上**匹配不到任何真实文件**(仅 MYIA_HOME 恰设为 `$APPDATA` 时成立)。该条来自 7748884c(10-14 六域全家桶)。
- **既有图渲染先例(可复用形态)**:
  1. **TG/通用 feed 线**:`metadata.image_files`(绝对路径 list;视觉管线 persist 开关产物,落 `MYIA_HOME/images/<sha16>.<ext>`,schema.py:1609-1614;写入点 `src/myssia/vision/collect.py` `item.metadata["image_files"]`)→ entry.py 白名单投影 → **新 `FeedLocalImages`**(desktop/ui-src/src/screens/feed/feed-local-images.tsx,并行会话在途件):每图 `invoke("feed_image_path")` 拿 Rust 授权 → `convertFileSrc` → `<img>`,拒绝/加载失败有人话降级。
  2. **微信媒体槽**(messaging 屏):`wechat-media.tsx:90-183` `MessageMediaSlot`——`media_scan --decrypt` 后拿 `cached_path`,`fileSrc = convertFileSrc(path)` 直转(wechat-media.tsx:84-87),缩略图 64px + 点击同屏大图;wxgf 词面"实况格式,暂不支持预览"。**注意它没走 Rust 授权,纯赌静态 scope——按上面根不匹配结论,真机上缩略图大概率 403**(该屏 10-14 交付时未做真机看图终验,与 media-key-hunt 收口注记一致:"UI 链另立"未了)。
  3. **Rust 按件动态授权范式**(并行会话 10-15-feed-local-images 新落,desktop/src-tauri/src/feed_images.rs):`feed_image_path` 命令——Rust 侧 `crate::data_root(&app)`(尊重 MYIA_HOME,main.rs:599-604)→ canonicalize + 囚于 `root/images` + 后缀白名单(png/jpg/jpeg/gif/webp)+ 魔数校验(PNG/JPEG/GIF/WEBP 头)→ `app.asset_protocol_scope().allow_file(&file)` 按件授权 → 返回路径给前端 convertFileSrc。**该命令写死 `root.join("images")`(feed_images.rs:18-20),media-cache 路径会被拒**。
- **detail-images 线(10-03)弹窗组件**:`FeedItemDetail`(feed-screen.tsx:1779 起;整屏画布 Dialog,头/滚动中段/动作簇三段)——中段已渲染 OCR 全文(1862-1873)、VL caption(1874-1883)、`<FeedLocalImages paths={item.image_files} testId="feed-detail-images">`(1896)。即**详情弹窗的图片位已就绪,复用面 = 直接喂 paths**。

### 三选一论证

| 选项 | 装机件账 | 判定 |
|---|---|---|
| A. 桥 HTTP(httpapi)直连 | 需常驻 `localdb serve` 进程(现无任何宿主);`<img src>` 无法带 Bearer 头,而 httpapi 的 URL `access_token` 通道**仅 SSE 放行**(httpapi.py:311-330,633-638 media 仅 GET+Bearer)→ 要么改 token 放宽策略(红线邻域,WeFlow 语义刻意排除)要么 JS fetch→blob 中转;**allowlist 目录是 `wechat-localdb/http-media/` ≠ media-cache**(httpapi.py:115,184-186)→ 解密产物还需搬/链一步;CSP connect-src 还得加 `127.0.0.1:5032` | 移动件最多,否 |
| B. asset 协议直读 media-cache | 静态 scope 已在(但根错,见上);**正路 = 复刻 feed_images.rs 按件动态授权**:Rust 端 data_root 定根(天然吃 MYIA_HOME 沙箱),把授权根从 `images/` 扩到 `wechat-localdb/media-cache/`(或加兄弟命令),魔数校验白名单加 wxgf 占位;CSP `asset:` 已在,convertFileSrc/降级 UI 均有现成件(FeedLocalImages / MessageMediaSlot 两套形态) | **推荐** |
| C. sidecar IPC 转 base64 | 无新协议面,但图片全量过 sidecar stdin/stdout JSON-RPC(单图 MB 级 base64 膨胀 33%),内存双份、无浏览器缓存复用、逐条阻塞 | 备选 |

**唯一推荐:B 的按件动态授权变体**。理由:① 与并行会话刚建立、已过测试的 `feed_image_path` 范式同构(review 面最小);② Rust `data_root()` 是唯一同时正确处理 MYIA_HOME 覆写与平台缺省根的定根点,静态 scope 猜路径已被证实不可靠;③ 解密产物 0600 落在 media-cache,按件授权 = 每张图显式过白名单 + 魔数门,与桥侧 magic 校验(media.py:173-211)双保险,私有数据红线好讲故事;④ 零常驻进程、零 CSP connect-src 扩张。**备选:C**,仅当真机 WebView 对 asset 协议出现不可修复问题时启用(并行任务自注"真实系统 WebView 尚未目验",留了这个逃生口)。

**附带需要决策的一笔**:静态 scope 条目 `$APPDATA/wechat-localdb/media-cache/**` 是死配置——要么修正为 `$APPDATA/MYIA/wechat-localdb/media-cache/**`(仍会被 MYIA_HOME 覆写打穿),要么删掉走纯动态授权(与并行会话 Owner decision"逐文件动态授权替代跨平台静态路径猜测"一致)。如实记录,取舍归主线。

---

## Q3 3 级渲染点与最小侵入位

### 3 级 = feed 屏渠道详情视图(确认)

`feed-screen.tsx:2970-2980`:"渲染形态派生(v8:3 级渠道详情双形态)……微信共用聊天双栏/气泡渲染(10-12-weixin-feed-channel)"。`chatView = activeChannelKind === "tg" || activeChannelKind === "wx"`(feed-screen.tsx:2980)。时间线容器在 5478-5513(`feed-chat-timeline` / `feed-flat-list`,居中 max-w-[760px],日期胶囊 + 未读分割线)。

### 气泡组件通用性(确认通用)

`FeedCard`(feed-screen.tsx:546 起)对 telegram/weixin **走同一分支**:
- 卡根:feed-screen.tsx:573-574 `kind === "telegram" || kind === "weixin"` → 气泡布局档(w-fit min-w-[13rem] max-w-72%,无竖条);
- 泡体:635-639(唯一可见箱,rounded-2xl,testid 沿用 `feed-tg-bubble-${rowKey}`);
- 发信人行:641-653(weixin 用 MessageCircle 绿点 #07C160,646-650);
- **正文按钮:654-663**(title/chatSender.body,点击开详情);
- 正文预览/全文:667-705;
- 展开钮+时间:706-733;
- 卡展开态图区:**1119** `<FeedLocalImages paths={item.image_files}>`(并行会话把旧路径列表换成了真图件);
- 详情弹窗图区:1896(同上,testid=feed-detail-images)。

### 给消息加图片区的最小侵入点

- **气泡内(PRD 目标形态"气泡内 <img>")**:泡体 div(635-638)内、正文按钮(663)之后正文预览(667)之前插一个"微信图片区"槽位——条件 = item 带微信媒体引用(新键,如 `metadata.image_files` 或专用键),复用 `FeedLocalImages` 的 SavedImage 单件(授权+convertFileSrc+降级)或 `MessageMediaSlot` 的缩略图形态(64px cover + 点击放大)。**注意**:FeedLocalImages 现在授权根只有 `images/`,media-cache 路径会被 Rust 拒(见 Q2)——UI 件可复用,Rust 授权面必须扩。
- **卡展开态/详情弹窗**:1119/1896 两处已由 `image_files` 驱动,**引擎只要写键就免费点亮**(hasImageDetails:233-239 连展开钮都会自动出现)。
- 深链定位已有兜底:3431-3438(data-item-key=dedup_key 12×250ms 重试),图区加载不破坏既有锚。

---

## Q4 media.py / media-cache 与 httpapi 交互现状

### scan/decrypt/status 的调用方盘点

| 能力 | 桥 CLI | sidecar 动作(entry.py) | UI 消费 |
|---|---|---|---|
| `scan_chat_media`(寻径;--decrypt 回填 cached_path) | cli.py:355 附近 `localdb media scan` | `wechat_local.media_scan`(sidecar.py:343-359;entry.py:4600) | **有**:`wechat-media.tsx:65-78` `wechatLocalMediaScan`(messaging 屏聊天图片分区) |
| `decrypt_dat_file`(单件) | `localdb media decrypt` | `wechat_local.media_decrypt`(sidecar.py:362-367;entry.py:4609) | 无(messaging 屏未用单件) |
| `media_status`(件配置态+缓存统计) | cli.py:401, 1265/1283 | **无 sidecar 方法、无 UI 消费**(`_ACTIONS` 词表 sidecar.py:443-455 不含) | 无 |

即:media_status 是纯 CLI 面若要做"未配置解密件"的结构化降级提示,得新增 sidecar 动作或复用 media_scan 应答里已有的 `provider.configured`(media.py:846,wechat-media.tsx:60 也已带)。

### 寻径与缓存事实(锚点)

- key 提取:`media.py:563-590` `media_extract_key`(packed_info_data protobuf 两级 length-delimited 里找 32-hex)。
- 图寻径:`media.py:611-630` `image_files_for` → `msg/attach/<dir1>/<yyyy-mm>/Img/<key>[_t].dat`,缩略图优先;视频明文:`media.py:633-646`。
- scan 条目:`media.py:726-778` = `{message_ref{ts,sender,local_type}, type, key, files{thumb|full|video...}, status}`,--decrypt 后加 `cached_path`(media.py:867)。
- 缓存:`media.py:152-155` `cache_dir` = `<数据根>/wechat-localdb/media-cache`;键 = sha256(源路径+mtime+size) 前 16(media.py:158-164);tmp+rename 原子、600/700(media.py:444-474);LRU 容量治理缺省 2048MB(media.py:358-395)。
- 状态词面(降级文案现成):media.py:123-129(明文直读(视频)/待解密/文件缺失/未配置解密件/已解密/实况格式,暂不支持预览/解密失败)。

### httpapi 媒体端点形态(锚点)

- 路由:`GET /api/v1/media/<rel>`(httpapi.py:633-638);鉴权 = Bearer 头/POST body token,**URL query access_token 仅 SSE**(httpapi.py:311-330)→ `<img src>` 直连不可行。
- allowlist:**只服务 `<数据根>/wechat-localdb/http-media/`**(httpapi.py:115 `MEDIA_DIR_NAME="http-media"`,184-186 `media_dir_path`;路径穿越守卫 491-515)。**与 media-cache 不同目录**——PRD 疑点坐实:media.py:34-35 注记宣称"media-cache 同时是 C6(HTTP 媒体端点)的指定读取落点",但实现服务的是 http-media;两目录名不一致是**文档与实现的既存冲突**(C6 原设计意图 vs 落地形态),如实上报,不是本任务要修的债但选型时不能假装 httpapi 能发 media-cache 的图。

### 解密产物 → webview <img> 最短路(按推荐 B)

```
UI(3 级渲染时,每条图片消息)
  → invoke("sidecar_request" wechat_local.media_scan {chat_id, since_days, decrypt:true})   [已有]
      桥 scan_chat_media + decrypt_dat_file → cached_path(<root>/wechat-localdb/media-cache/<sha16>.jpg)
  → invoke("feed_image_path_v2" {path: cached_path})   [需扩:授权根加 media-cache;wxgf 不进图门]
      Rust data_root() 定根 + 囚禁 + 魔数 + allow_file
  → convertFileSrc(allowed) → <img>
```
引擎侧配套(链路补全):`_fetch_localdb` 对 image 行不再 skip,按 (ts,key) 关联 media_scan 产物,把 `cached_path`(或 dat 引用+惰性解密标记)写进条目 metadata(键名建议直接复用 `image_files` 吃现成投影与 UI 槽,或专用键区分渠道)——**写键即全链点亮**,这是 Q1/Q3 的接缝。

---

## Q5 并行改动核对(git log 近 24-72h)

### 四桥文件:无在途、近期无提交

近 72h 四文件零提交;末次提交均 ≥10-14:

| 文件 | 末次提交 |
|---|---|
| localdb_export.py | afdb52eb 2026-10-14 19:42(docs sweep) |
| localdb_page.py | dc0cd985 2026-10-14 03:24(send_text 三源合体) |
| httpapi.py | 0bec58d9 2026-10-14 04:10(r3 真机深测五缺陷修复 0.8.3) |
| media.py | dc0cd985 2026-10-14 03:24 |

PRD 提的"localdb_export.py 会话初 M 现已提交"核实:工作树 plugins/ 全净。**桥侧四文件可放心动。**

### 真正在途的并行面 = 10-15-feed-local-images(未提交工作树,全在 desktop/)

任务档 `.trellis/tasks/10-15-feed-local-images/prd.md`:AC 全勾、"已打包换装,待人审;真实系统 WebView 和用户已有持久化图片尚未目验,不宣称微信媒体链闭环"。涉及文件(git status):
- `desktop/src-tauri/src/feed_images.rs`(**新文件**,untracked)——feed_image_path 命令 + 单测;
- `desktop/src-tauri/src/main.rs`(+2 行:mod 注册 + 命令挂载);
- `desktop/src-tauri/tauri.conf.json`(CSP img-src 加 `http://asset.localhost`;assetProtocol scope 未动);
- `desktop/ui-src/src/screens/feed/feed-local-images.tsx`(+test,新文件);
- `desktop/ui-src/src/screens/feed/feed-screen.tsx`(1119/1896 两处换 FeedLocalImages,-15+4 行);
- 另有 smoke 脚本/测试小改(feed-card-smoke.py 等)。

**撞面结论**:本任务(feed-wx-images)与它在同一批文件上工作(feed-screen.tsx、tauri.conf.json、main.rs/feed_images.rs),但语义正交——它管 `images/`(视觉管线持久化图),本任务管 `wechat-localdb/media-cache/`(微信解密图)。正确姿势 = **等其提交后在其上叠加**(扩 feed_images.rs 授权根 / 复用 FeedLocalImages 组件),不要重写其文件。

### 其它工作树改动(背景,避误伤)

`.trellis/scripts/*`、若干 spec/prd 文档、desktop/scripts/*-smoke.py——均属上述任务及其它会话,不碰。

---

## 与 PRD 假设的冲突清单(如实)

1. **httpapi ≠ 现成图通道**:R7 媒体端点 allowlist 是 `http-media/` 非 `media-cache/`(httpapi.py:115 vs media.py:34-35 注记);且 `<img>` 无法过 Bearer 鉴权;且无人 spawn serve。PRD"桥 HTTP 直连"选项的装机成本被低估。
2. **assetProtocol 静态 scope 是死配置**:`$APPDATA/wechat-localdb/media-cache/**` 与真实根 `.../MYIA/wechat-localdb/media-cache` 不匹配(见 Q2);`wechat-media.tsx` 的 convertFileSrc 直转在真机大概率拿不到图(无真机终验记录)。
3. **品类配置路径**:任务描述写 `config/config/`,实为 `config/weixin.yaml`。
4. **feed 链媒体信息两段丢**:桥 query 四列(无 key)+ 引擎 skip 非 text(engine.py:911)——PRD 待探①只问"丢在哪一步",答案是两步都要补。
5. **好消息一条**:`metadata.image_files` 白名单投影(entry.py:1574-1614)+ UI 图槽(FeedLocalImages/hasImageDetails)已全通,引擎写键即点亮卡展开/详情两处;气泡内 `<img>` 是纯 UI 新增位(feed-screen.tsx:663 后)。

## Caveats / Not Found

- 未真机验证 WebView asset 协议行为(并行任务同样留白);静态 scope 根不匹配的结论基于 Tauri v2 `$APPDATA` 语义与 `myssia_home()` 源码推演,两种 `$APPDATA` 解释都不含 MYIA 段,故结论稳。
- `10-14-wechat-media-sns` 任务档未逐字重读(其 R5 交付 wechat-media.tsx 已直接读码);archive 未翻。
- media-cache 真实磁盘内容未查看(私有数据红线;仅引用代码事实)。
