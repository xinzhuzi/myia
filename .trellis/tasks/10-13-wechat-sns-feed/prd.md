# PRD:微信朋友圈进情报流(本机 only + 互动通知)

主人令(2026-10-13,对话原文):「好,那么朋友圈也给我展示在情报流里面吧」+
AskUserQuestion 决议:「立任务并开工」+「只入本机情报流」+「要互动通知也进流」;
追加令(同日):「暂时先不发飞书」「所有的都暂时不发飞书」——朋友圈**零推送面**,
且全仓 14 品类的飞书推送已另行注释停发(运维动作,已落地,不入本档验收面)。

## 背景(侦察已毕,2026-10-13 实探)

- 朋友圈本地库在场:`db_storage/sns/sns.db`(21MB,4408 条动态),微信后台
  近实时同步(侦察时最新动态 42 分钟前,`sns.db-wal` 活跃写)——**不需要打开
  朋友圈页**。
- 密钥已覆盖:keys.json 20/20 含 `sns/sns.db`;同一把钥匙实解明文副本验证过。
- 数据形状(实探):
  - 动态表 `SnsTimeLine`(tid/user_name/content/pack_info_buf):content =
    一段干净 XML(`SnsDataItem/TimelineObject`):稳定 id、username、
    createTime(epoch 秒)、contentDesc(正文)、ContentObject/mediaList/media[]
    (type/thumb/url/videoDuration)、sourceUserName/sourceNickName(转发源)。
    纯图条目 contentDesc 空但 mediaList 在。
  - 互动通知表 `SnsMessage_tmp3`(create_time/type/from_username/
    from_nickname/feed_id/content/serialized_comment_buf…):type=1 赞(182 条,
    content 恒空)、type=2 评论(67 条,content=评论文本)。create_time 是
    SQL 刞(窗口过滤在 SQL 层)。

## 需求

R1 **朋友圈动态入情报流**:`weixin.yaml` 加源后,朋友圈动态作为条目进本机
store+feed,与 TMS 群消息同屏消费(feed 微信渠道双栏/气泡,零新 UI)。

R2 **互动通知入情报流**(主人显式勾选):赞/评通知也进流,可独立开关
(独立源声明;不想要的用户不加该源即可)。

R3 **幂等**:动态用微信侧全局 id 强锚(全期幂等,TG 同级);通知用表主键
local_id 强锚。

R4 **增量**:水位增量窗口(同 localdb 通道既有机制),不逐轮全量重读。

R5 **隐私红线沿袭**:enrich 关(内容不送 LLM)、push 空(零外发——主人令
「暂时不发飞书」背景下降格为结构性不配)、retention 30d、日志只留形状。

## 验收标准(AC)

- AC1 桥命令:`wechat-bridge localdb sns feed --since 3d --json` 与
  `localdb sns notices --since 3d --json` 真跑成功,载荷契约见 design §3;
  旧命令(query/key-*/probe)行为零变化。
- AC2 引擎:`channel: sns` 源经 myssia 管线真跑,动态+通知条目入 store,
  feed 屏微信渠道可见;重跑同窗零新增(dedup 幂等)。
- AC3 水位:第二轮起按增量开窗(--since 天数随水位收缩),skip/失败不推进。
- AC4 门禁:pytest 全量零新红;桥测试(golden 夹具)覆盖 feed/notices 两命令。
- AC5 装机:桥组件 0.6.0 装机件刷新换装,装机环境真跑 AC2(条目入 feed,
  截屏留证——文字内容脱敏,只证条目在场与形状)。
- AC6 配置:repo 样例 config/weixin.yaml 注释补 sns 形态;live 数据根
  weixin.yaml 加两源(weixin-朋友圈 / weixin-朋友圈互动)。

## 非目标

- 不做朋友圈媒体下载/展示(条目带 media 计数与占位,不拉图)。
- 不做发布/写面(只读红线)。
- 不做 UI 新面(渠道卡/双栏/气泡零改动;源名 weixin- 前缀自动归微信渠道)。
- 不推飞书(主人令;推送面结构性缺省空)。
- 不做全期回填(首拉窗口 since_days 缺省 3 天,深历史是需求出现再议)。

## 规模清单(查改分家纪律)

桥 `localdb_query.py`+`cli.py`+`config.py` ~350 行;桥测试 ~300 行;
引擎 `wechat_local.py` ~250 行;引擎测试 ~250 行;golden 夹具 +2 锚;
配置注释/两源;桥版本 0.5.1→0.6.0 + component.json 同步。AI 侧预计 2-3 小时。
