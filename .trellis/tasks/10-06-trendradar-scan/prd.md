# PRD:TrendRadar 竞品拆解(平台源/订阅形态/告警节奏/许可证四面对标)

> 立档:2026-10-06 · 来历:grill 决议 Q4 小时级小档(telegram-telethon research.md §1-③ 已注记「值得专项拆解」)
> 对象:sansan0/TrendRadar(62,691★ gh api 实测,多平台舆情聚合 + AI 监控) · 类型:竞品只读拆解,零源码改动(链接者铁律)
> 状态:已完成(四面拆解 + 回写 + 定向提交,见结果段)

## 开始段:拆解面清单(本档交付物)

| # | 拆解面 | 要回答的问题 | 通道 |
|---|--------|-------------|------|
| F1 | 平台源清单 | 它监控哪些平台?TG 是怎么接的(源码级)? | zread MCP / gh |
| F2 | 关键词订阅形态 | 用户怎么定义「关注什么」(配置结构/正则/分级)? | 同上 |
| F3 | 告警与日报节奏 | 即时告警与摘要日报怎么分(频率/通道/去重)? | 同上 |
| F4 | 许可证与链接者评估 | 许可证是什么?能不能借、怎么借不违链接者铁律? | 同上 + LICENSE 文件亲读 |

交付去向:
- F1-F4 全部落本档(过程段随做随填,结果段完工汇总);
- TG 接法对 MYIA 的启示 → 追记 `10-06-telegram-telethon/research.md` 一节;
- feed/日报线启示 → 记入本档结果段(feed-channel-groups / daily-digest 线参考)。

## 过程段(随做随填)

**2026-10-06 拆解实录**(全走 zread MCP + gh CLI,零 clone 零压力):

1. 建档:`task.py create`(带来历与四面描述)→ prd 三段骨架。
2. 仓库结构:`zread get_repo_structure` —— 采集面 `trendradar/crawler/`(fetcher.py + rss/)、调度面 `core/scheduler.py` + `config/timeline.yaml`、订阅面 `config/frequency_words.txt` + `ai_interests.txt` + `custom/{keyword,ai}/`、推送面 `notification/`(dispatcher/batch/splitter/senders)。
3. 亲读证据(zread read_file,文件级出处):
   - `config/config.yaml`(v2.4.0)—— platforms/rss/filter/report/notification 全景;
   - `config/timeline.yaml`(v1.2.0)—— 调度积木全文;
   - `config/frequency_words.txt`(v1.1.0)—— 关键词 DSL 全文;
   - `trendradar/crawler/fetcher.py` —— 热榜抓取机制(newsnow API + 域名校验);
   - `pyproject.toml` —— 依赖清单(v6.10.0,无任何 TG 客户端库);
   - `LICENSE` —— GPL-3.0 全文。
   - `zread search_doc`「telegram 数据源还是推送通道」—— 架构页/多渠道分发页/MCP 通知页/issue 页交叉证实。
4. gh api 双验(2026-10-06):`repos/sansan0/TrendRadar` → 62,691★ / GPL-3.0 / pushed 2026-09-13(活跃);`repos/ourongxing/newsnow` → 21,962★ / **MIT**(热榜真上游)。
5. 本地对照(MYIA 侧):`src/myssia/push/` 目录清点(telegram.py 在列,约 40 渠道);`src/myssia/alerts/engine.py`(send_immediate/槽位防重)+ `src/myssia/push/digest.py`(DigestAggregator/时段槽)结构;`pyproject.toml:11` license=MIT。
6. 回写:telegram-telethon/research.md 追记 §4;定向提交 `git commit --only` 两档路径。

## 结果段(完工必填)

### F1 平台源清单:采集只有两类,TG 不是采集源

- **热榜 = newsnow 聚合 API**(上游 ourongxing/newsnow,22k★,MIT):默认公共实例 `https://newsnow.busiyi.world/api/s`,单接口 `?id=<平台id>&latest`(`fetcher.py` DEFAULT_API_URL + fetch_data);config 默认 11 平台(头条/百度/华尔街见闻/澎湃/B站/财联社/凤凰/贴吧/微博/抖音/知乎),平台空间=newsnow 的 id 空间,可自部署换 api_url。
- **RSS = feedparser**(pyproject `feedparser==6.0.12`):feeds 列表 id/name/url/enabled/**max_age_days 每源覆盖全局** freshness_filter。
- **TG 仅是推送出口**:telegram 只出现在 `notification.channels`(bot_token/chat_id,Bot API);依赖清单零 telethon/pyrogram,零平台直爬依赖(仅 requests+feedparser)。→ **62k★ 同物种件也没做「TG 群/频道作为情报来源」,Telethon 引擎级在竞品是空位**(已回写 telegram-telethon 档)。
- 可借细节:`expected_domain` 域名安全校验(`fetcher.py._check_domain_safety`:HTTPS+主域/子域匹配、url+mobileUrl 双字段、防 `baidu.com@evil.com` userinfo 绕过,不过关整平台丢弃+告警)——防聚合 API 链接劫持,MYIA 接聚合器源时照搬此语义。

### F2 关键词订阅形态:双轨筛选 + 带 DSL 的词库 + 按时段换词库

- **双轨**:`filter.method = keyword`(零 token)/ `ai`(自然语言兴趣描述 `ai_interests.txt` + litellm,`min_score 0.7` 推送阈值、`reclassify_threshold 0.6` 增量/全量重分类权衡、batch 200 条 2s 间隔防限流)。
- **frequency_words.txt DSL**:两大区 `[GLOBAL_FILTER]`(全局排除)+ `[WORD_GROUPS]`;行语法 = 普通词 | `/正则/`(自动忽略大小写)| `词 => 别名` | `[组别名]` | `+必须词`(组内 AND)| `!排除词`(组内 NOT)| `@N`(限显示条数);显示名优先级 组别名 > 行别名拼接 > 关键词本身。
- **高阶玩法**:timeline 时间段可指定 `frequency_file` / `interests_file` / `filter_method`——晚间汇总用金融词库、白天用科技词库,「不同时段不同关注面」。

### F3 告警与日报节奏:三态报告语义 + 三级调度积木 + 窗口限次

- **运行模型**:无常驻进程,cron 唤醒(GitHub Actions 每小时/Docker 30 分钟),醒后三阶段 collect→analyze→push 各自可独立开关;静默期(default)只采集不推送——数据持续积累换汇总完整度。
- **timeline 三级积木**:periods(时间段,start>end 自动识别跨日)/ day_plans(日计划)/ week_map(周映射);重叠策略 error_on_overlap / last_wins;四预设 always_on / morning_evening / office_hours / night_owl。
- **report_mode 三态**:`daily`(当日汇总,含已推过的)/ `current`(当前在榜,持续在榜每次出现)/ `incremental`(只推新增,零重复,无新增不推)——即时/摘要被产品化为**三态而非两态**。
- **once 窗口限次**:每时段每天 analyze/push 各只一次(省 API+省打扰)。
- **推送管线**:翻译→按区域过滤→扩散渠道;渠道顺序执行;按渠道字节上限分批(默认 4000/钉钉 20000/飞书 30000)+ 3s 间隔;多账号分号分隔(max 3),`any()` 尽力而为语义。
- **在案教训(issue #1198)**:采集与推送节奏独立时,增量只反映最后一次采集而非「上次推送→现在」全窗口——MYIA 常驻 serve immediate 线天然免疫,**批量引擎线要警惕**。

### F4 许可证与链接者评估:GPL-3.0,零代码拷贝双重成立

- TrendRadar = **GPL-3.0**(LICENSE 全文亲读 + gh api 双验);MYIA = **MIT**(`pyproject.toml:11`)。
- 结论:**任何代码拷贝都被双重禁止**——①链接者铁律本就禁 fork/vendor/改源码;②GPL-3.0 传染性会迫使 MYIA 整体 GPL 化。可走的两条正路:
  1. **设计思想/产品语义借用**(配置形态、三态节奏、DSL 语法——不受版权保护,本档四面即此产物);
  2. **服务级消费**:自部署 TrendRadar 后经 webhook/HTML 报告/MCP 消费其输出(GPL 义务只及 TrendRadar 自身——同 MYIA 的 RSSHub AGPL 服务消费零代码复用判例)。
- **更精准的借法**:热榜真上游 **newsnow 是 MIT**——MYIA 若扩热榜品类,链接 newsnow API / 自部署 newsnow 无许可证障碍,根本不必碰 GPL 的 TrendRadar。

### feed/日报线启示(记入本档,供 feed-channel-groups / daily-digest 线参考)

MYIA 已有 immediate/digest 双轨(`alerts/engine.py` send_immediate 槽位防重 + `push/digest.py` DigestAggregator 时段槽)≈ TrendRadar 的 incremental/daily;push 渠道 ~40 对其 9 是碾压。**差距在节奏产品语义,可借三点**:
1. `current` 第三态(当前在榜)——热榜类源缺这个语义;
2. 预设模板产品化(四预设一键选,优于裸配置);
3. 按时段换词库/兴趣面。
反面教训一条:增量窗口必须显式覆盖「上次推送→现在」全窗口(issue #1198),批量引擎线设计时写死此约束。

### 回写指针

- telegram-telethon/research.md §4:TrendRadar TG 接法启示(TG=推送出口非采集源、竞品空位、GPL 禁借码、newsnow MIT 可链)。
- 本档四面结论如上,后续热榜/订阅 DSL 设计直接引本档。

## 涉网纪律

全走 zread MCP 或 gh CLI(免 clone、零压力);网络不通换 WebSearch。不 fork、不改上游、不 vendor——只读拆解。

## 验收标准(AC)

- [x] AC1:四面(F1-F4)各有落档结论,证据带文件级出处(仓库路径/文件名)。(见结果段;zread 亲读 config.yaml/timeline.yaml/frequency_words.txt/fetcher.py/pyproject.toml/LICENSE,gh api 双验星数与许可证)
- [x] AC2:telegram-telethon/research.md 追记 TrendRadar TG 接法启示一节。(§4)
- [x] AC3:本档过程/结果段回填,定向提交(git commit --only 本档 + telegram 档,不碰并行脏文件)。
