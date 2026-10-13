# research.md — 10-06-hermes-align:蓝本深度排查(主人令「照着Hermes写好的去做」)

## §1 双机器人(实证)

| 机器人 | 凭据位置 | 形态 | 用途 |
|---|---|---|---|
| 主 agent | ~/.hermes/.env FEISHU_APP_ID/SECRET | websocket 长连接双向(DM+群,@提及门控,Typing/表情回应,卡片按钮) | 通用交互 agent;主群=「AI中转站合伙人群」oc_f38a…(=FEISHU_HOME_CHANNEL,MYIA 现用此凭据 ✓);另有主人 DM oc_9a79… |
| ai-analyst | ~/.hermes/profiles/ai-analyst/.env 独立 FEISHU_APP_ID | 同机制独立 profile(multiplex) | 分析员机器人(独立人格/任务面) |

## §2 Hermes 怎么做「监控」(与 MYIA 的三层偏离)

1. **任务形态(最大偏离)**:Hermes cron job=自然语言 prompt → `hermes chat -Q` 跑一次 agent 轮(bot_chat_delivery.py:727;agent 带浏览器/工具自己去查网站)→ 摘要=agent 的回答。MYIA=YAML 机械管线(引擎/选择器/模板)。Hermes 形态下「AI厂商监控」=一句话建 job,无需选择器工程。
2. **投递形态**:preferred_message_type="text"——日报=agent 写的 markdown 文本(adapter.py:281,455-481 md tag rows+4000 字拆分),经 im/v1/messages 发群;deliver 默认 home channel(scheduler_delivery.py:origin/home/explicit/bot-chat 四目标);MYIA=feishu_card 交互卡片(拆卡不截断,已通)。
3. **通道机制**:WebSocket 长连接双向(可对话可回应);MYIA=单向 API 推送。

## §3 照抄批次(建议序)

- **批次1(小)**:日报消息形态对齐——feishu 通道增文本 markdown 模式(照抄 Hermes md rows+4000 拆分实现在 plugins/platforms/feishu/adapter.py:455-481);cron deliver 缺省从 local 改 home。
- **批次2(中)**:双机器人分流——MYIA 通道增第二套飞书凭据键(ai-analyst 应用),告警走二号、日报走一号(照抄 multiplex 分工)。
- **批次3(大,产品级)**:prompt 任务形态——MYIA cron 增自然语言 job(照 hermes chat -Q:一轮 LLM+浏览工具,产出即摘要,deliver 走通道)。给 MYIA 装 Hermes 的灵魂:一句话定义监控。

## §4 主人 Hermes 实况旁证

cron/jobs.json 现空、executions 账本仅 1 笔(2026-09-24 direct)——主人对 Hermes 的 cron 用得少,但消息/机器人设施(channel_directory 2026-10-06 仍在更新)活跃;.ai-analyst profile 在册。

## §5 合并日报(Hermes 版式照抄,批次4)——布局规格、实现与真发回执

### 5.1 布局规格(主人截图 OCR,Hermes 产线原文)

```
<总标题> · <日期> · <AM|PM>
<分区一标题>
1. <一句话条目>(标题精炼,可带来源前缀)
2. …
--
<分区二标题>
1. <子标题(如厂商名)>
   <缩进明细行们>
2. …
<分区N…>
<时间> 实时爬取生成 · 全条目指纹去重 · 无新内容自动静默
```

要点:①多品类合成一条(分区=品类/报表,`--` 分隔线);②条目=编号+一句话(不是链接列表;链接可附在句尾);③尾戳=生成时间+指纹去重+静默声明;④全分区无新内容=整条静默不发;⑤超 4000 才 (i/N) 续段(组合铁律在案,通道层 POST_SPLIT_THRESHOLD 行边界拆段,不在报表层重做)。

### 5.2 实现(提交 8d3ed63,12 文件 +1419/−29)

- **新引擎 `src/myssia/engines/store_report.py`**(链外,prompt/urlwatch 判例):从 store 查本槽位窗(AM=本地 00:00 起/PM=12:00 起,`SLOT_BOUNDARY_HOUR` 同界)各品类新条目,按 `sections` 分区渲染上述布局,整份报表=一条目出仓。
  - 分区匹配键=**源名**(分类器 category 对 builtin 关闭的品类恒 None,games/ai-vendor-watch 无从按 category 查;源名是 items 表的稳定锚);
  - `labels` 来源前缀、`suffix_fields` 句尾附注(游戏价格 price_text/sale_price)、`style: detail`=编号子标题+缩进明细行(LLM markdown 结构符 `#`/`-`/`**` 剥除,防飞书 md 把缩进行渲染成标题/列表破坏版式)、`max_entries`/`max_lines` 截断帽+「另有 N 条省略」留痕;
  - 空分区整段跳过(`--` 只落已渲染分区之间);全空=零条目+skip 哨兵 `store_report_window_empty`(urlwatch 合法空态判例,doctor 不误诊);
  - dedup 锚点 `<源url>#report-<YYYYMMDD>-<am|pm>`(`#prompt-` 判例):每槽新键、同槽重跑幂等、跨槽必新;
  - store 注入缺席=结构化 `store_not_available`;pagination/extract 结构化拒(单报表语义);before/before_id 复合游标拉全窗口(items 表混着不在分区的源,单页 limit 会被无关新条目挤占)。
- **词表三处同步**:schema `ENGINES`/`EngineName` + engines/registry 注册 + skill/SKILL.md 与 docs zh/en schema.md 枚举表。
- **新场景件 `plugins/daily-digest.yaml`**:schedule 08:05/20:05(错峰在采集 08:00/20:00 之后);push feishu_card `msg_form: text` 模板 `{{ items[0].report_markdown }}`,route 永真 immediate;分区=AI 资讯(16 源带 labels)/AI 厂商官网(detail,max_lines 20)/游戏喜加一与折扣(suffix 价格);`empty_ok: true`。
- **既有品类 digest 路由降噪**(合并日报成唯一日报出口):ai-news/games 的 digest 档改 archive **并加 `url != ''` 兜底封边**(route 层保守缺省是 digest,不封边会残留逐品类单发出口——server/token 分类未命中、CS 缺价条目都会漏进 digest);ai-vendor-watch 整条 immediate 改 archive(其 09:00 产的日报条目由合并日报「AI 厂商官网」分区承载,AM 报表因 09:00>08:05 空分区跳过、PM 报表收口);保留 immediate(score≥9/白给/喜加一)。grep 面:三品类无 `mode: digest` 残留(测试钉住)。
- **测试**:`tests/engines/test_store_report_engine.py` 37 例全 mock(词表/链外、options 校验、槽位窗边界、版式渲染快照逐行断言、明细归一、空窗静默、同槽幂等锚点、截断帽、超长报表过 feishu text 续段 (i/N)、品类路由降噪参数化);`tests/plugins/test_plugins.py` 7 例断言随批次4 语义更新。全量 4580 passed / 40 skipped,uvx ruff 过;gitnexus detect-changes(staged)= 12 文件 18 符号 0 执行流受影响,风险 LOW。

### 5.3 真发回执(生产数据根 `~/Library/Application Support/MYIA`)

- **PM 槽真发**(2026-10-06 17:42,repo CLI 对生产 myssia.db):窗口内 111 条(aihot 8 / cocoloop 98 / hf-blog 1 / seed-home-watch 3 / ai-vendor-watch 1;games 11:00 跑过 AM 槽故本窗无),渲染 16 条目(AI 资讯 15+「另有 65 条省略」;AI 厂商官网 detail 1 条含 Anthropic/OpenAI/DeepMind 明细,行帽处「明细超长省略」),`feishu_card immediate=1 ok=True` **发主人 DM 1 条消息**(env:FEISHU_CHAT_ID;凭据三键经 env/钥匙链解析,值零外显);头行 `情报日报 · 2026-10-06 · PM`、尾戳 `17:42 实时爬取生成 · 全条目指纹去重 · 无新内容自动静默`,与规格逐行对齐。
- **同槽幂等静默**:17:43 二次重跑 `dedup_seen=1` 拦截,零条目零发送(发一条,不发第二条)。
- **cron 挂点**:生产 jobs.json 新增 `每日合并日报`(id fb85edaf94ac,`5 8,20 * * *`,tz Asia/Shanghai,next 2026-10-06 20:05;误建重复件 cda938f57363 已 remove,现存 4 job)。
- **装机外科**:bundle(`世事.app/Contents/Resources`)同步 myssia-src 三件(store_report.py 新/registry.py/schema.py)+ plugins 四件(daily-digest 新/ai-news/games/ai-vendor-watch);数据根 plugins 同步同四件;`codesign --force --deep -s -` 重签,`codesign -vv` = valid on disk / satisfies DR。
- **装机态装载校验**(数据根 python + bundle myssia-src):registry 解析 store_report、四 YAML 全装载、路由无 digest;装机 runtime 全链 `--dry-run` 真跑 = success,空窗 skip 哨兵如常(内存库空 → 静默路径装机态同样成立)。

已知取舍(如实记档):immediate 已推条目(score≥9/喜加一)仍会出现在合并日报里(「窗口内全部新条目」语义,日报=全量总结);ai-vendor-watch 09:00 产出只进 PM 报表(AM 08:05 在其前),如需进 AM 报可把 vendor cron 提前到 08:02(未动,最小面)。
