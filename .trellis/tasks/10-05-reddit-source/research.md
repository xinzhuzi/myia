# research:Reddit 情报源合规通道探查(评估档)

> 任务:10-05-reddit-source · 探查快照:2026-10-05(傍晚) · 定界=探查不实现
> 涉网纪律执行记录:`evidence/probe-log.md`(全程单次/先 robots/零压力/全记档)
> 引用标记:【A#】=probe-log A 表探查;【B#】=页面读取(存档 evidence);【搜】=搜索引擎多源交叉(二手);【仓】=仓库文件行号亲验

## 0. 结论速览

1. **robots 面零变化**:www.reddit.com robots 与 10-03 库档快照**字节级一致**(SHA-256 同值【A1】),全站 `Disallow: /`、无任何 API 豁免段;OAuth 宿主 oauth.reddit.com 同样全禁【A3】。→ **Reddit 官方 API 不是经 robots 豁免认可的通道**;但官方一手明言 **"Our robots.txt is for search engines, not Data API users."**【B6】——API 通道的合规面在 Developer Terms/Data API Terms(条款面),不在 robots 面。绕 robots 直抓站内(.rss/.json)仍被 Public Content Policy 点名为「未授权访问」【B3】,10-03 respect_robots 判例维持。
2. **重大时效(本轮发现,改写全局)**:Reddit **2026-09-30 公告**【搜:TechCrunch/TechRepublic/Mashable/unite.ai/crawlfeed 多源一致 + r/help 官方周报引用 + 一手侧证 B7】——RSS feed **2026-11-13 退役**;公 Data API 新申请 **2026-10-31 截止**;未注册 app **2027-01-12** 起移除;**公 Data API 2027-03 分阶段终结**,开发者被推向 Devvit 平台/付费许可。**官方免费 API 路的申请窗口只剩 ~26 天(至 2026-10-31)**。
3. **官方免费层额度一手坐实**:100 QPM/OAuth client id(10 分钟均值窗口,支持突发)【B6:Data API Wiki,publishedTime 2026-05-11】;OAuth 强制("Traffic not using OAuth ... will be blocked");UA 硬格式 `<platform>:<app ID>:<version> (by /u/<username>)`;**已删内容须同步删、官方建议 48h 常规清理**(留存已删内容=违约,即使去标识)。
4. **研究通道判明**:robots 注释自指的 r/reddit4researchers → Reddit for Researchers(RFR)program【B4】= 高校批文制(IRB+机构邮箱+赞助人)+ **BigQuery 历史数据集(5 年回看/6 个月延迟)**,非实时 API → **对 MYIA 实时情报收集结构性不适用**。
5. **聚合器路当前无经验证可用的零凭据合规通道**:Google News RSS=robots 禁(通用 UA Allow 清单无 /rss/)【A7】;Bing News RSS=robots 放行【A9】但**本机出口 302 墙三探不达**【C1-C3】;Pushshift=2023-05 起撤销/mod-only/无新摄入【C4】【搜】;Reddit 自家 .rss 即便可用也 2026-11-13 死。XFlux 型判例(只做可选后端永不默认,`connector-selection.md:11`)继续适用。
6. **停点确认**:两路全部停在主人决策点(通道选择/凭据申请/出口环境/数据保留义务),**零实现代码**,如定界。

## 1. robots.txt 现探与对照(AC1)

| 项 | 结果 |
|---|---|
| 内容探【A1】 | exit 0,538B,`evidence/reddit-robots-2026-10-05.txt` |
| 状态码另探【A2】 | **200** |
| 与 10-03 库档对照 | `diff -u` exit 0 + SHA-256 `41aea421…781857` 双档同值 → **字节级一致** |
| 豁免段 | **无**(仅注释行自指 Public Content Policy 与 r/reddit4researchers) |
| oauth.reddit.com【A3】 | 26B,`User-Agent: * Disallow: /`(API 宿主同样全禁) |
| 对照口径 | 两快照存档(10-03 库档 + 10-05 现探)+ 10-05 转述注(planning 期复核系转述未存档,如实记) |

**「官方 API 是否 robots 认可通道」结论**:robots 面不是;条款面是(OAuth+审批)。且官方一手把两者边界挑明【B6】。对 MYIA 实现的含义:任何 reddit.com/oauth.reddit.com URL 源会被全引擎共享的 robots 守卫(`fetch_base.py:2252` 调用面亲验【仓】,含 direct_api)按缺省 `respect_robots: true`(`schema.py:728`)拦下 → API 源实现须显式 `respect_robots: false` + 档内引用 B6 一手声明作依据。

## 2. Public Content Policy 口径核对(AC2)

原文全读【B3】(页面 publishedTime 2025-05-29;摘录 `evidence/public-content-policy-2026-10-05.md`):

- **非商业可用**:"Our terms have always aligned with our Default Open value — you can use Reddit content for non-commercial uses ... but talk to us if you have commercial purposes in mind."
- **抓取=未授权访问**:"...entities using unauthorized access (for example, **by scraping** or using data brokers) or misusing authorized access to collect public data in bulk..."(点名 generative AI 语境)
- 三类被许可方:品牌监控/LLM 厂商/**研究者**("continue to provide access ... for research")。
- 被许可方限制清单:不得留存已删内容、不得敏感属性画像、不得人脸识别/背景调查等。

**判读**:MYIA(个人非商业)落在「非商业可用」口径内,**前提是走授权通道**(OAuth API);直抓站内与政策正面冲突。MYIA 若某日商业化(带广告/付费功能),现行条款要求先取得 Reddit 许可——记入长期风险。

## 3. 官方 Data API 通道全景(AC3)

### 3.1 现行免费层(一手,2026-05-11 快照)【B6】

| 项 | 口径 |
|---|---|
| 额度 | **100 QPM/OAuth client id**,10 分钟均值窗口;另有聊天消息/房限额 |
| 认证 | **OAuth 强制**;无凭据流量直接 blocked(不适用缺省限额) |
| 凭据形态 | 注册 app(审批制:"To request, please contact us here"【B6】/"approved developers"【B5】/"sign-up" 非商业入口【B5】);OAuth2 token;**script app 的 client_id+secret 细节在 www.reddit.com 域 OAuth2 指引页(robots 全禁,按纪律未取,凭据形态细节标记未核)** |
| UA | 硬格式 `<platform>:<app ID>:<version> (by /u/<username>)`;禁谎报 |
| 数据义务 | 已删内容须删;**建议 48h 常规清理**;留存已删=违约 |
| 限速头 | X-Ratelimit-Used/Remaining/Reset |

### 3.2 2026-09-30 公告时间线(二手多源交叉 + 一手侧证)

| 时点 | 事件 | 证据级 |
|---|---|---|
| 2026-10-31 | 停收新 API 访问申请 | 【搜】多源一致(TechCrunch 2026-09-30 报道等) |
| 2026-11-13 | **RSS feed 支持退役**(官方称其为"large-scale scraping 的常见面") | 【搜】多源一致 |
| 2027-01-12 | 未注册 app 开始被移除(注册可豁免) | 【搜】两轮搜索独立命中 |
| 2027-03 | **公 Data API 访问分阶段终结**;迁移向 Devvit | 【搜】多源一致 |
| 侧证 | App Migration Program 2026(一手【B7】):2026-03-31~12-31,Data API app 迁 Devvit 悬赏 $1,000,迁移截止 2026-12-31 | 一手 |
| 一手原文 | r/redditdev 公告帖(www.reddit.com,robots 全禁**未取**) | 未取得(如实) |

### 3.3 研究通道(RFR)【B4】

高校附属+IRB+机构邮箱+赞助人,免费,BigQuery Analytics Hub,5 年历史+6 月延迟,单项目 ≤1 年,禁再分发。**非实时、非 REST,MYIA 不适用**;且官方明示"用开发者 API 做学术研究=违反政策"【B5】——RFR 与非商业 API 是两条独立通道,池档「robots 自指 r/reddit4researchers 为研究/非商业通道」的表述须按此修正。

## 4. 聚合器路评估(AC4)

| 候选 | robots | 可达性(本机出口) | 字段面/配额 | 判 |
|---|---|---|---|---|
| Google News RSS `news.google.com/rss/search?q=site:reddit.com` | **禁**(`*` 段 Allow 清单无 /rss/)【A7】 | 未探(robots 已禁,按纪律不发起)【C5】 | — | **不合规,弃** |
| Bing News RSS `bing.com/news/search?q=site:reddit.com&format=rss` | **放行**(cn.bing.com `*` 段未禁 /news/search;www 从本网 302→cn【A8/A9】) | **不可达**:www 变体 302 吞路径落首页【C1】;cn 直取 302→根【C2】;ensearch=1 同墙【C3】 | 未取得载荷(0 items×3) | robots 合规但**本出口验证失败**;有国际出口可复验 |
| Pushshift 类 | 无禁令【A10】 | api 根 307 空跳【C4】 | 2023-05 撤销,mod-only,无新摄入【搜】 | **死通道** |
| XFlux 型聚合器 | — | 未探(存在性与模式=supplier-map 已核 ●) | — | 判例:收紧源优先评估聚合器、**只做可选后端永不默认**(`connector-selection.md:11`、supplier-map:74) |
| 自部署 RSSHub(仓库已随包 myssia-rsshub 插件【仓】) | 取决于部署实例 | — | RSSHub 的 reddit 路由**自身依赖 Reddit 公开面**(同受 2026-11-13/2027-03 收紧冲击),不构成绕过 | 不改变结论 |

**PoC 判定**:存在零凭据且 robots 合规的候选(Bing News RSS),但本机出口三探不达 → **PoC 未取得正向载荷,如实记失败**;不硬做。

## 5. 两路对比表(合规/配额/凭据/实现量/风险)

| 维度 | 官方 Data API OAuth 免费层 | 聚合器(Bing News RSS 型) |
|---|---|---|
| 合规 | 条款面正路(robots 不适用,B6 一手);非商业可用(B3) | robots 放行(A9);内容经新闻索引二手转述,无 Reddit 条款关系 |
| 配额 | 100 QPM/client(10min 均值)【B6】;**通道本身 2027-03 终结**【搜】 | 未知(未取得载荷);新闻索引延迟+覆盖面受新闻媒体报道偏置 |
| 凭据 | OAuth app(client_id+secret,审批制;**新申请 2026-10-31 截止**) | 零凭据 |
| 实现量 | 中(OAuth token 生命周期小改 + UA/限速头 + respect_robots:false 记档;见 §6.1) | 近零(现有 `extract.type: rss` 直接吃;见 §6.2) |
| 数据保真 | 一手全文+分数+评论+作者,实时 | 二手标题/链接/摘要,仅「被新闻报道的 Reddit 内容」子集 |
| 风险 | ①通道 26 天申请窗口+2027-03 终结倒计时 ②48h 删除义务 vs MYIA 长期库张力 ③商业化须另行许可(B3) | ①本出口不可达(运维环境依赖) ②Google News 主候选 robots 违规被排除 ③覆盖偏置 ④服务方随时改版 |
| 判例符合度 | connector-selection「免费路径」:✅ 免费层存在(但通道进入终结倒计时,信号分级=「营销型/收缩中」) | 「聚合器只做可选后端永不默认」:✅ 定位即可选后端 |

## 6. 实现量预估(两路;探查档只预估不实现)

### 6.1 官方 API 路(若主人决策走此路)

- **品类 YAML 形态**(现有 schema 零改动即可表达大半):`engine: direct_api` + `url: https://oauth.reddit.com/r/GamingNews/new?limit={limit}` + `extract.type: json_path`(data.children[].data.*)+ 源级 `headers.User-Agent`(`schema.py:752` 源级 headers 已支持,UA 值非凭据不触发明文守卫)+ `rate_limit.respect_robots: false`(`schema.py:728` 缺省 true,守卫调用面 `fetch_base.py:2252` 亲验)+ 限速参数(100 QPM→`requests_per_minute` 预算内)。
- **引擎缺口(唯一真实现量)**:direct_api 现为**静态 Bearer 键池**(`direct_api.py:10-12,55-56`,401/403/429 轮换,无 token 生命周期);Reddit OAuth bearer ~1h 过期 → 需 token 获取/缓存/刷新小改(client_credentials/userless 或 script app password grant;**凭据形态细节未核**,见 §3.1)。预估:engine_options 扩展 + token 缓存 ≈ 100-200 行 + 测试(参照 zenrows/saas gated 先例的量级)。
- **凭据入钥匙链路径**:`keychain:myia/reddit/client_id` + `keychain:myia/reddit/client_secret`(惯例同 `plugins/ai-news.yaml:126` `keychain:myia/llm/base_url`;明文守卫 `schema.py:465` 强制)。
- **政策面配套(必须)**:48h 已删内容清理义务【B6】 vs myia.db 长期保留的张力 → 需要主人裁决保留策略(数据面或豁免声明);UA 硬格式含 Reddit 用户名(隐私取舍,主人定)。
- **时限**:申请须 **2026-10-31 前**(主人亲自:Reddit 账号+app 注册+审批);通道 2027-03 终结前需关注 Devvit 迁移形态再评估。

### 6.2 聚合器路(若主人决策走此路/作为可选后端)

- **品类 YAML 形态**:`engine: static_html` + `extract.type: rss`(10-03-news-rss 落地路径,`static_html.py:8-11,217,221`【仓】;fields=feedparser 白名单 `schema.py:597`)+ `url: https://www.bing.com/news/search?q=site%3Areddit.com&format=rss`。**零引擎改动**。
- **前提条件**:出口环境可达(本机三探失败【C1-C3】;主人若有国际出口/代理池路由,先复验 PoC 再接线)。代理池(pools.yaml)可按源路由——现有能力。
- **凭据**:零。
- **定位**:按判例**只做可选后端永不默认**;品类 YAML 层面以注释锚定判例出处。

## 7. 推荐倾向(供主人决策,非决定)

- **若要真 Reddit 情报(全文/评论/实时)→ 官方 Data API 是唯一正路**,但它是**限时窗口决策**:2026-10-31 前申请(免费层 100 QPM 对个人情报场景绰绰有余),2027-03 通道终结前大概率有一次「迁移 Devvit 或转付费」的再决策。**不申请窗口即关**。
- **若只要「Reddit 上被新闻化的事件流」且接受偏置 → 聚合器路近零实现**,但当前出口不可达,先决条件=出口环境;且永不作默认源(判例)。
- **两条都不选(暂缓)是可接受答案**:政策面收紧方向明确(PCP 把 scraping 点名为未授权访问;RSS/API 全面收官),「等 Devvit 形态明朗再进」的机会成本很低。
- **任何形式的绕 robots 直抓(.rss/.json/伪装 UA)明确不建议**:政策点名+判例+UA 谎报禁令【B6】三重堵死。

## 8. 主人决策点清单(owner_left)

1. **通道选择**:官方 API(限时限窗)/聚合器可选后端/暂缓观望——三选一。
2. **凭据与注册(官方路)**:Reddit 账号+app 注册+非商业申请,**2026-10-31 前**,须主人亲自(本档不代申请)。
3. **出口环境(聚合器路)**:是否提供/指定国际出口(代理池路由)供 Bing RSS 复验。
4. **数据保留义务(官方路)**:Reddit 条款 48h 已删内容清理建议 vs MYIA 长期库——接受条款张力或加清理机制,主人裁决。
5. **UA 隐私(官方路)**:UA 硬格式要求携带 Reddit 用户名,是否接受。

## 9. 残余不确定/未核项(如实)

- r/redditdev 公告一手原文未取(robots 全禁);时间线为二手多源交叉+一手侧证。
- script app 凭据形态细节(client_id/secret/grant 类型)未核(指引页在 robots 禁域);若走官方路,实现档首步补核。
- api.reddit.com 宿主 robots 未探(单次纪律下本轮选了 oauth 宿主;两宿主预计同口径,实现时若用 api 宿主须补探)。
- Bing RSS 在国际出口下的字段面/延迟未测(本出口不可达)。
- 2027-03 后 Devvit 形态是否留有个人非商业数据通道:未知,持续跟踪项。
