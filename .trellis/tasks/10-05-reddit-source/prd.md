# PRD:Reddit 情报源合规探查(评估档)

> 立档:2026-10-05 · 来源:v12-backlog 池档第 7 项(主人 2026-10-03 点名「Reddit 也是情报收集渠道」)
> 类型:**评估档,探查不实现** · 预计停点:主人决策(通道选择+凭据+注册)

## 定界

- **做什么**:robots.txt 现探(单次零压力)与 10-03 库档快照对照;Public Content Policy 口径核对;
  官方 Data API OAuth 免费层(额度现值/注册要求/凭据形态/robots 自指研究通道)与
  聚合器路(Google News RSS `site:reddit.com` 等,Pushshift 类存档现况)两通道评估;
  产出 `research.md`(对比表+推荐倾向+实现量预估:品类 YAML 形态适配/引擎挂点 direct_api vs rss/凭据入钥匙链路径)。
- **不做什么**:零实现代码、零注册、零凭据申请(凭据=主人决策点,不代申请);不直抓 Reddit 站内
  (10-03 判例:robots 全站禁抓,`respect_robots` 维持不可直抓)。
- **停点设计**:大概率停在主人决策点(通道选择+凭据申请),如实定界不硬做;档置 review 不归档。

## 涉网纪律(全程硬约束)

单次(每目标 URL 一次,不重试)、先查目标域 robots.txt 并记档、零压力、全部证据落 `evidence/`。

## 背景与既有事实(引用即已核)

- 10-03 库档快照:`evidence/reddit-robots-2026-10-03-archive-copy.txt`(538B,源
  `archive/2026-10/10-03-games-wrap/evidence/news-probe-reddit-robots.txt`,本轮亲验在库)
  ——全站 `User-agent: *` `Disallow: /`,注释自指 Public Content Policy 与 r/reddit4researchers。
- planning 期主会话 2026-10-05 复核(全站禁抓口径未变)系**转述、原文未存档**;对照口径记为
  「两快照存档(10-03 库档+本次重探)+10-05 转述注」,不虚称三快照。
- 判例:pool 档 `.trellis/tasks/10-03-v12-backlog/prd.md:95-107`;聚合器判例
  `.trellis/spec/domain/connector-selection.md:11`(XFlux 型只做可选后端,永不默认);
  supplier-map 趋势注 `archive/2026-10/10-03-free-tier-supplier-map/research.md:74`。

## 验收标准(AC)

- [x] AC1:robots.txt 现探完成(内容+状态码两探,各单次),与 10-03 快照逐行对照记档;
  若存在 robots 豁免段(如 API 前缀)逐条抄录并给出「官方 API 是否 robots 认可通道」结论。
  **证据**:内容探 exit 0/538B + 状态码 200(`evidence/reddit-robots-2026-10-05.txt`;probe-log A1/A2);
  对照=diff exit 0 + SHA-256 同值(字节级一致);无豁免段;oauth 宿主同样全禁(A3);
  结论「robots 面不认可、条款面认可(B6 一手 'robots.txt is for search engines, not Data API users')」
  落 `research.md` §1。
- [x] AC2:Public Content Policy 口径核对(读原文记档):自动化访问/非商业/研究通道的许可边界。
  **证据**:原文全读+关键段抄录 `evidence/public-content-policy-2026-10-05.md`(publishedTime 2025-05-29);
  判读(非商业可用/抓取=未授权访问/研究通道=RFR)落 `research.md` §2。
- [x] AC3:官方 Data API 免费层口径核实(涉网读取,目标域先探 robots 记档):OAuth-only 现况/
  免费层配额现值(带快照日期)/凭据形态(script app client_id+secret)/研究通道口子;
  零注册零凭据申请。
  **证据**:一手 Data API Wiki(publishedTime 2026-05-11)100 QPM/OAuth client id + OAuth 强制 +
  UA 硬格式 + 48h 删除义务(`evidence/data-api-wiki-2026-10-05.md`);审批制/非商业入口
  (`evidence/dev-platform-accessing-data-2026-10-05.md`);RFR=BigQuery 历史数据集非实时 API
  (`evidence/reddit-for-researchers-2026-10-05.md`);2026-09-30 收官公告时间线(二手多源+一手侧证
  `evidence/app-migration-terms-2026-10-05.md`)→ `research.md` §3;script app 凭据细节页在
  robots 禁域未取(如实记,`research.md` §9);零注册零申请(全程无账号操作)。
- [x] AC4:聚合器路评估(只评估不实现):Google News RSS(Bing News RSS 备选)robots 探查+可达性/
  字段面/延迟;Pushshift 类现况(服务状态/配额);若存在零凭据合规通道可做单次 PoC 请求并记档,
  否则如实记不做。
  **证据**:GNews RSS=robots 禁(A7,Allow 清单无 /rss/,PoC 不发起 C5);Bing RSS=robots 放行(A8/A9)
  但本出口三探 302 墙不达(C1-C3,0 items×3,PoC 失败如实记);Pushshift 307 空壳(C4)+2023-05 撤销
  多源(搜);XFlux 判例与 rsshub 插件关系 → `research.md` §4。
- [x] AC5:`research.md` 落官方 API vs 聚合器对比表(合规/配额/凭据/实现量/风险)+推荐倾向+两路
  实现量预估(品类 YAML 形态/引擎挂点/凭据钥匙链路径);owner 决策点清单成文;档置 review 不归档。
  **证据**:`research.md` §5 对比表/§6 实现量预估(挂点亲验:`src/myssia/engines/registry.py:79-87`、
  `direct_api.py:10-12,55-56`、`static_html.py:8-11`、`schema.py:597,728,752`、`fetch_base.py:2252,2272`)/
  §7 推荐倾向/§8 决策点五项;档置 review(task.json 亲改)。
