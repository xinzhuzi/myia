# 微信媒体与朋友圈导出(C3)

## Goal

聊天媒体解密(.dat V4,**解密算法零进货——外部件协议**)+ 朋友圈内容只读导出
(JSON/HTML,媒体分级如实标注)。数据面全走已交付的解密副本/本机文件只读链;
展示面并入既有微信本机工作台族(messaging 屏 WechatLocalSection 版式,TG 三级
界面判例:不新造画布、不新路由);UI 文案全人话(「聊天图片」「朋友圈」「导出」),
协议/字段保留标准英文(`dat_path`/`ext`/`is_wxgf`)。

父档:10-13-wechat-features(C3 行:聊天媒体解密+朋友圈只读导出;「拦截朋友圈
删除隐藏」已红线排除)。参考锚=hicccc77/WeFlow(CC BY-NC-SA,**只借设计零抄码**)
+ imldy/chatlog(Apache-2.0,media_v4 路径模型)。生态教训(PyWxDump/chatlog 自删、
wechat-dump-rs DMCA、WeChatMsg 清仓)= 解密算法件不进 MYIA 仓库是硬约束。

## 背景实测锚(2026-10-14 本机复核,执行者免重探)

**本机布局**(账号目录 `xwechat_files/wxid_oc2yhey1xkpw22_8253/`,定位常量
`plugins/wechat-bridge/wechat_bridge/system_checks.py:50` WECHAT_FILES_ROOT):

- 聊天图:`msg/attach/<dir1-32hex>/<yyyy-mm>/Img/<key-32hex>.dat`(正图)+
  `<key>_t.dat`(缩略图)。全树 **42,513 个 .dat**(其中 _t 缩略图 27,510)。
  V4 头实证(`xxd -l16` 样本):`0708 5632 0807 | 0004 0000 | f80c 0000`
  = 签名 7 字节 + int32LE aesSize(0x400)+ int32LE xorSize(3320),与 WeFlow
  imageDecryptService.ts:2215-2295 的 V4 分段规格逐字段吻合。
- 聊天视频:`msg/video/<yyyy-mm>/<key>.mp4` + `<key>_thumb.jpg`,**全明文**
  (2026-10 月:197 jpg + 32 mp4,`file` 报 ISO Media/JPEG;2026-07~09 月空)。
  视频消息 local_type=43(近 400 条抽 1 例命中,design 扩样)。
- 朋友圈缓存:`cache/<yyyy-mm>/Sns/Img/<2hex>/<30hex>`(无扩展名,V4 头同签名
  实证;2026-09=3590 文件、2026-10=5162)+ `cache/<yyyy-mm>/Sns/Video/<2hex>/<name>.mp4`
  (**明文** mp4;2026-09=61、2026-10=113)。
- **聊天消息→文件映射成立**:message 库 `Msg_<md5>` 行的 `packed_info_data`
  (protobuf)内含 32-hex key → `msg/attach/<dir1>/<yyyy-mm>/Img/<key>.dat`。
  近 40 条图片消息实测:正图命中 27/40(未下载/已清理=缺文件如实),**缩略图
  _t.dat 命中 40/40**。dir1 与 username 的推导关系未实证(design 采样;glob
  兜底合法,dir1 目录数有限)。
- **朋友圈帖→本地缓存映射不存在**(本轮新实证,推翻调研期「本地缓存优先」假设):
  sns.db content XML 的 `md5="…"` 属性 7104 个(去重 6954)对本地缓存文件
  **0 命中**;md5(url) 亦不合;反向取缓存名回查 sns.db 全部 13 表零命中。
  ⇒ 帖级朋友圈媒体**唯一路径 = CDN 回源**(url+key 在 content XML `<media>`
  节点内,形状:`<url type="1" md5="…" key="数字串" enc_idx="1" token="…">http://shmmsns.qpic.cn/…/0</url>`;
  WeFlow 判例:CDN 流 Isaac64 keystream XOR、视频仅头部 128KB 加密、`x-enc:1`
  头判密)。本地缓存只能做「考古浏览」(无帖级归属),本档不做。
- sns.db(解密副本)形状:SnsTimeLine 4 列(tid/user_name/content/pack_info_buf),
  SnsMessage_tmp3 互动通知(feed_id 可关联条目)。内容导出**零解密零风险**
  (sqlite3 -readonly 已验证可全量读)。

## Requirements

### R1 媒体解密外部件协议(链接者铁律核心交付)

- 新协议文档 `docs/wechat-mediadecrypt.md`(v1,形态照 docs/wechat-keyprovider.md):
  桥 spawn 用户自备可执行件,stdin 单行 JSON 请求 → stdout NDJSON(progress 0..N
  + result 恰一次)→ 退出码矩阵;无来源校验、无内置降级、无状态可重入。
  - action `decrypt_dat`:请求 `{action, dat_path, out_path}`(out_path=桥指定的
    私有区临时路径,件把明文产物写到该路径);result `{success, ext, is_wxgf,
    width?, height?}`。**钥匙=件内自理**(用户把 imageXorKey/imageAesKey 供给
    自己的件;MYIA 全链零媒体钥接触、零钥落盘)。
  - action `decrypt_stream`(R4 用):请求 `{action, in_path, key, out_path}`
    (桥完成 CDN 下载落临时文件后交件解 Isaac64;key=content XML 的数字串)。
- 桥配置新顶层键 `media_decrypt_path`(缺省空=未配置;`localdb media-decrypt
  set|get|clear` 管理命令,照 key-provider 判例)。未配置 → 媒体面结构化降级
  (新 exit 23 `media_unavailable`),**文本链(query/sns feed/导出正文)零影响**。
- 参考件 `plugins/wechat-bridge/examples/mediadecrypt_ref.py`:协议形状示范,
  **toy 算法**(如字节反转)+ 醒目声明「非真实微信解密,真实算法用户自备」——
  仓内零真实解密算法(AC7 守卫)。

### R2 聊天媒体寻径与解密编排(桥新模块 `wechat_bridge/media.py`)

- 寻径(纯只读):输入 chat 标识+窗口(复用 localdb_query 已交付的 `Msg_<md5>`
  表名/real_sender_id 解析),按 local_type 分流:3=图(key→Img/<key>.dat|_t.dat,
  **缩略图优先呈现**)、43=视频(key→msg/video/<yyyy-mm>/<key>.mp4+_thumb.jpg,
  明文零解密)、其余类型只报形状。产物=媒体清单:`{message_ref, type, key,
  files:{thumb?, full?, video?}, status}`,status 词面人话:「明文直读(视频)」
  「待解密」「文件缺失」「未配置解密件」。
- 解密编排:`localdb media decrypt <dat_path> --json` spawn 外部件 → 校验产物
  magic(JPEG/PNG/WebP/GIF 标准魔数表,与件声明的 ext 一致才收)→ 原子落私有
  缓存 `<数据根>/wechat-localdb/media-cache/<sha256(源路径+源mtime+源size)前16>.<ext>`
  (tmp+rename,文件 600/目录 700)。幂等:缓存命中零再解;源 mtime/size 变=重解。
  容量上限复用配置面新增 `media_cache_capacity_mb`(缺省 2048,LRU 清理)。
- 清单命令:`localdb media scan <chat> --since 30d --json`(只寻径不解密)+
  `--decrypt`(逐条解密并回填 cached_path)。
- 状态命令:`localdb media status --json`(件配置态+缓存统计)。

### R3 朋友圈只读导出(桥新模块 `wechat_bridge/sns_export.py`)

- `wechat-bridge localdb sns export --format json|html --out <dir> [--since Nd]
  [--with-media] --json`:
  - JSON:`entries[]`(复用 sns_query 既有解析+nickname 反查,扩展 media 全量字段:
    type(2=图/6=视频,已实证)/cdn_url/md5/key/width/height/status)+ 每条关联
    评论(`SnsMessage_tmp3.feed_id` ↔ 条目 id 关联,关联率如实披露,未关联的
    notices 单独成节,不强求 100%)。feed 载荷契约**只加不改**(既有引擎消费零破坏)。
  - HTML:单文件自包含正文 + `files/` 目录相对引用媒体;未解/未回源媒体显示
    人话占位(词面见 R4),不 base64 内嵌(346MB 级消息库教训:防单文件爆炸)。
  - 导出产物落 `--out` 指定目录(用户自选;缺省=数据根私有区
    `wechat-localdb/exports/sns-<时间戳>/`),文件 600。
- 媒体状态词面(词汇判例,全人话):「已解密」「明文复制」「未能下载(链接已失效)」
  「未配置解密件,未解密」「本地文件缺失」;实况/wxgf 产物(件报 is_wxgf=true)
  =「实况格式,暂不支持预览」(文件原样保留)。

### R4 朋友圈媒体回源(阶梯交付,默认关)

- `--with-media` **缺省关**:桥对 content XML 逐 media 节点做 HTTPS GET(只读、
  零进程干预;URL/token 均来自库内),`x-enc:1` 响应落临时文件交外部件
  `decrypt_stream` 解;URL 失效(403/404)如实标注「未能下载(链接已失效)」。
- 本地明文视频缓存**无帖级映射(实测不存在)**,不参与帖级导出;聊天明文
  视频/缩略图按 R2 直读复制。
- 真 CDN 端到端属主人开箱裁量(AC4 注记);协议+编排+夹具级验证随本档交付。

### R5 桌面 UI(微信本机工作台族)

- sidecar 新动作(`src/myssia/wechat_local_sidecar.py` `_ACTIONS` 封闭表):
  `sns_feed`(包既有 `localdb sns feed` 命令)、`sns_export`、`media_scan`、
  `media_decrypt`;entry.py 薄壳照 7075 区判例注册 4 个 `wechat_local.*` 方法。
- `desktop/ui-src/src/screens/messaging/wechat-sns.tsx`:朋友圈分区(时间线列表:
  发帖人+时间+正文+媒体位;导出按钮触发 sns_export 并回报产物路径)——版式并入
  WechatLocalSection 同族(Card/分区,不新路由)。
- `desktop/ui-src/src/screens/messaging/wechat-media.tsx`:媒体渲染件——消息行
  媒体占位(wechat-local.tsx:77-79 现状「非文本消息,内容未导出(占位)」)升级为
  缩略图(media_scan→_t.dat 解密缓存);视频显示 _thumb.jpg+时长;点击同屏展开
  (组件内 state,不新造全局 viewer/画布)。**消息列表本体=C1(chat-export)
  交付面,本件只做媒体槽替换,接线归集成员**。

### R6 门禁与守卫

- pytest:tests/wechat-bridge/test_media.py(寻径 golden 夹具/编排 mock 件/缓存
  幂等)+ test_sns_export.py(解析/导出器/关联夹具);tests/desktop/
  test_wechat_local_handlers.py 增 4 动作。全量 `python -m pytest tests/` 零新红。
- vitest+tsc:wechat-sns/wechat-media 两测试件;`npx vitest run` + `tsc -b` 零错。
- 红线守卫(AC7):新码 grep 零命中——`INSERT|UPDATE|DELETE|DROP|TRIGGER` 于
  微信库路径、`installSnsBlockDeleteTrigger`、微信进程 API(NSAppleScript/
  CGEvent 至微信、task_for_pid);产物只写 MYIA 私有区;仓内零 V4/Isaac64
  真实算法(grep AES/ECB/isaac 于新增产品码=零);密钥/内容零入日志。

## Acceptance Criteria

- [x] AC1 协议与配置:docs/wechat-mediadecrypt.md v1 在场且自洽(第三方凭文档
  可写件,无须读桥源码);`localdb media-decrypt set|get|clear` 真跑;未配置时
  `media decrypt/scan --decrypt` exit 23 结构化 `media_unavailable`,同场
  `localdb query`/`sns feed`/`sns export` 正文照常出(零影响实证)。
- [x] AC2 寻径:`media scan` 对真库真会话跑,图片消息 key→`_t.dat` 近期窗口
  命中率 ≥90%(本轮基线 40/40),正图缺文件如实「本地文件缺失」;视频消息
  mp4 明文直读;黄金夹具(合成 msg/ 树)覆盖三分支。
- [x] AC3 解密编排:配置外部件后对真 V4 样本(`msg/attach/**/Img/*_t.dat`)
  端到端:产物 magic 与 ext 一致、落 media-cache 600、重复调用幂等(二跑零
  spawn,以 mock 件计数断言)、源 mtime 扰动后重解;wxgf 产物原样保留+词面
  「实况格式,暂不支持预览」。
- [x] AC4 朋友圈导出:`sns export --format json` 真跑全量(基线 SnsTimeLine
  4419 条),JSON 含 nickname 回填+media 清单+评论区关联(关联率数字在载荷
  `stats` 如实);`--format html` 产物浏览器打开可读(files/ 相对引用);
  `--with-media` 缺省关实证(无网络请求,以 mock 断言);开启后夹具级(本地
  http stub)验证 x-enc 流程与失效标注;真 CDN 端到端=主人开箱后补验(注记)。
- [x] AC5 UI:微信本机工作台出现「朋友圈」分区(动态列表+发帖人必显+导出钮,
  导出回报产物路径);消息行媒体占位升级为缩略图实显(真会话真图);全文案
  人话判例复核(「聊天图片」「朋友圈」「导出」;零「回源」「.dat」类工程词
  上屏——路径/扩展名在 mono 块属协议面除外)。
- [x] AC6 版本与换装:桥 0.7.0→0.8.0(component.json+stamp 测试同步);装机
  环境 bundle 热修+组件 rsync 换装(10-13-wechat-sns-feed AC5 判例),装机
  真跑 AC5 截屏留证(脱敏,只证形状)。
- [x] AC7 红线守卫:R6 grep 清单全零命中(命令与输出留 check.jsonl);examples
  件零真实算法;全程零微信进程干预、零写微信侧(含 CDN 只 GET)。
- [x] AC8 端到端真数据:两链各真跑一次留证——①会话→含图消息→缩略图显示;
  ②朋友圈→导出件打开可见正文与媒体状态词面。夹具演示不算过。

> **复查回执(2026-10-14 复查员实跑,判定 PASS/needsFix=false)**:① real_check 真跑:rows=4419 parsed=4419 entries_with_media=3519 media_nodes=7065(与前轮回执逐字一致);② R6 红线 grep 三组全零:写 SQL(INSERT|UPDATE|DELETE|DROP|TRIGGER)、真实算法(AES|ECB|isaac)、密钥入日志;③ pytest test_media+test_sns_export+test_sns_query 56 passed + test_wechat_local_media_handlers 12 passed(前轮回执 12 gated-skip 现已激活);④ 全量 vitest 41 文件 886/886 passed;⑤ CLI 已接线真跑:localdb media status / media-decrypt get → 结构化 unconfigured 态+人话指引(指向 docs/wechat-mediadecrypt.md),media-cache 目录/容量 2048MB 就位。装机像素验证(C3 面:朋友圈分区+聊天图片缩略图文案)归父档 AC-P4 回执(15-stats-sns-media-contacts.png)。
>
> **留档发现**:[info] sns_export.py:111 urllib.request.urlopen 命中网络 grep——经核为 PRD 设计内 CDN 回源只读 GET(AC7 明示「CDN 只 GET」,--with-media 缺省关,AC4 注记无网络请求以 mock 断言),非红线违例;decrypt exit 23 端到端需外部解密件配置,unconfigured 态如实结构化降级,无法在无件条件下复跑(如实)。

## 非目标

- 不做 wxgf/实况**解码**(ffmpeg/wasm 零进货;文件原样保留+如实词面;系统
  ffmpeg 外部依赖留后续裁量)。
- 不做朋友圈本地缓存「考古浏览」面(帖级映射实测不存在;需求出现再议)。
- 不做媒体钥提取/保管(钥归外部件;MYIA 零接触——与 keyProvider「产品代码
  零取钥实现」同构)。
- 不做朋友圈写面/拦截删除隐藏(红线;WeFlow installSnsBlockDeleteTrigger=
  snsService.ts:1236 反例,AC7 grep 守卫)。
- 不做语音帖(SnsNoteVoice 表在场,导出如实标「语音,暂不支持」)。
- 不做全量批量解密(42,513 .dat 按需解:浏览/导出窗口内逐条)。
- 不做聊天记录六格式导出器本体(C1 交付面;本档只供 media 命令)。

## 规模清单(查改分家纪律)

协议文档 ~150 行;media.py ~450 + 测试 ~350;sns_export.py ~350 + 测试 ~300;
cli/config 接线 ~120;sidecar+entry ~120 + 测试 ~150;UI 两组件+分区 ~500 +
测试 ~400;example ~120 行。AI 侧预计 6-9 小时。

## 依赖与排序

- 前置:无硬前置(keys.json/E2 管道/sns 查询全在案);R4 真跑依赖主人供给
  外部件+开 `--with-media`,不阻塞 R1-R3/AC1-AC3/AC5 正文链。
- 与 C1(chat-export)拼面:C1 消息列表先落(占位现状已是),本档 R5 媒体槽
  替换;C1 HTML 导出嵌媒体时消费本档 `media scan/decrypt` 命令(契约以本文
  R2 为准)。
