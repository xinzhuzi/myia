# research.md — 10-06-telegram-telethon:GitHub TG 件调研与架构定调

> 主人令(2026-10-06):调研全记录;**尤其 Telethon 本软件要做**;其他插件走「设置下载+配置」;**「我们做链接者,不做源码修改者」**。

## §1 四类「能获取 TG 消息」的件(2026-10-06 gh api 实测星数)

### ① Bot API 线(收自己群的消息;对应路线二)
| 件 | 星级 | 机制 | 借鉴点 |
|---|---|---|---|
| python-telegram-bot/python-telegram-bot | 29.5k★ | getUpdates 长轮询/webhook | 过滤器分层模式范本;**不引库**,MYIA 手搓 httpx 零依赖(同 Hermes 网关手法) |
| aiogram(~5k)/telegraf(~7k,Node) | | 同机制异步版 | 备选,不采用 |

**实操坑(调研翻出)**:bot 进群默认**隐私模式**——看不到普通消息;须 BotFather `/setprivacy` 关闭或提管理员。主人操作四步:建 bot→关隐私→发 token→拉群。

### ② MTProto/userbot 线(bot 进不去的群;主人点名要做)
| 件 | 星级 | 说明 |
|---|---|---|
| **Telethon**(LonamiExs/Telethon) | ~11k★ | 账号 session 读任意已加入群——**本软件原生做**(引擎级);MIT 许可可依赖;凭据(session 文件/api_id/api_hash)入钥匙串 |
| Pyrogram/pyrofork | ~4k★ | 同类备选,API 更现代 |
| TDLib(官方 C++) | ~7k★ | 底层重,不采用 |

**风控建议**:挂小号(不挂主人常用号);session 失效重登走一次性验证码流程。

### ③ 成品监控件(对标/借鉴,不引入)
| 件 | 星级 | 关系 |
|---|---|---|
| **TrendRadar**(sansan0/TrendRadar) | **62k★** | 同物种大件:多平台舆情聚合+AI 分析+关键词订阅(TG 在源列表)——**值得专项拆解**(源清单/订阅形态/告警节奏整块借鉴) |
| tgcf(aahnik/tgcf) | ~2k★ | 「监控→过滤→转发」与我们的「粗筛→精筛→推送」同构,设计互证 |
| AstrBot | 41k★ | 多 IM 接入框架,链接者路线的另一种实现,不引入 |

### ④ 路由件
RSSHub(46k★)telegram 路由(与 X 线共用同一部署,一鱼两吃);RSS-Bridge(公开频道)。

## §2 架构定调(主人令,长期有效)

1. **链接者,不做源码修改者**:外部件一律链接/封装/组件化(RSSHub 只桩、urlwatch 不 vendor、crawl4ai 组件轨判例),永不 fork 改上游;
2. **组件化接入形态**:设置页下载组件(自管 Python 环境组件轨先例)→ 配置驱动 → 使用;**不改源码**;
3. **Telethon 例外=原生做**(引擎级深度集成,主人明示);
4. 命名规约:`telegram-<频道/群原名>` 全称前缀(已定);文件/品类/源三级不缩写。

## §3 现状锚(已就绪部分)

- 公开频道线:plugins/telegram-channels.yaml(t.me/s 网页预览,durov 样例已真跑 20 条入库;等频道清单挂调度);
- 合并日报「Telegram 频道」分区已配(daily-digest.yaml);
- 情报流渠道分组+分型呈现 UI 在途(10-06-feed-channel-groups)。

## §4 TrendRadar 专项拆解启示(2026-10-06,全文见 10-06-trendradar-scan/prd.md)

> §1-③ 点名的 62k★ 同物种件已专项拆解(zread 亲读 config/frequency_words.txt/timeline.yaml/fetcher.py/pyproject.toml/LICENSE + gh api 双验)。对本档的直接启示:

1. **TG 在 TrendRadar 只是推送出口,不是采集源**:telegram 仅出现在 `config.yaml notification.channels`(bot_token/chat_id,Bot API);依赖清单零 telethon/pyrogram,采集面= newsnow 热榜聚合 API + RSS(feedparser)两类。→ **「TG 群/频道作为情报来源」在头部竞品是空位,Telethon 引擎级(本档主线)是差异化能力,无对标可抄,D1/D2 自定调设计无翻案压力**。
2. 它把 TG Bot 当推送通道的形态(多账号分号分隔、token/chat_id 配对)——MYIA `push/telegram.py` 已有等价物,push 渠道 ~40 对其 9,零增量。
3. **许可证红线**:TrendRadar = GPL-3.0(LICENSE 亲读),MYIA = MIT——**一行代码都不能借**(GPL 传染 + 链接者铁律双重禁);可借的只有设计思想(其热榜源清单/关键词 DSL/三态报告节奏已拆解落 trendradar-scan 档)。
4. **旁路可链**:其热榜真上游 newsnow(ourongxing/newsnow,22k★)是 **MIT**——未来若扩热榜品类,链 newsnow API/自部署即可,不必碰 GPL 的 TrendRadar。
