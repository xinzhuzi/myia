# 市面有名爬虫/分析工具盘点表(Phase 2 第一遍,2026-10-05)

> 证据口径:license/星数/活跃度 = `gh api repos/<o>/<r>` 快照(2026-10-05);EasySpider/Crawlab license 以仓库内拆解档 `10-03-ui-deep-imitation/research/licenses.md`(2026-10-03 核)交叉印证。●=已核;○=收录实施时再核。归位判定框 a-e 见 prd.md(主人已批:优先零成本+本地执行硬规则)。

## 判定框速查

a=核心链新档(库型且更强) · b=插件+链外引擎(本地跑,照 credhunter/Photon 样板) · c=remote/server-only 桩(指自部署) · d=同物种默认不收 · e=不立项记档(许可/免费路径/活跃度不过关)

## 盘点表(22 行,按形态类)

### 库型(通用抓取库)

| 工具 | license | 星数 | 零成本/本地 | 判定 | 一句话理由 |
|---|---|---|---|---|---|
| Playwright | Apache-2.0 ● | 97k ● | 本地 ● | **已收**(L5 载体) | 隐身浏览器档已进程内使用 |
| Scrapy | BSD-3 ● | 64.6k ● | 本地 ● | **d(框架性错位)** | 全家桶框架+twisted;MYIA 已是编排层,嵌不进单源 fetch 语义 |
| Crawlee(python) | Apache-2.0 ● | 9.6k ● | 本地 ● | **暂缓(e 观望)** | 库形态干净,但 L1-L5 已覆盖 URL→内容;出现「现有档位拿不下的站点」再评估 |
| Selenium | Apache-2.0 ● | 34.5k ● | 本地 ● | **e(无增量)** | 与 Playwright 同生态位且更旧,无新增能力 |

### 采集专项型(平台内容采集)

| 工具 | license | 星数 | 零成本/本地 | 判定 | 一句话理由 |
|---|---|---|---|---|---|
| yt-dlp | Unlicense(公域) ● | 195k ● | 本地 CLI ● | **b·首批** | 视频/频道情报(元数据+下载),零成本本地 subprocess,公域许可最干净 |
| RSSHub | AGPL-3.0 ● | 46.4k ● | 自部署/公共实例 | **c·首批(桩)** | 万物转 RSS 扩资讯源;AGPL 只桩不抄;文档须标注公共实例=第三方留痕,缺省指自部署 |
| TikTokDownloader | GPL-3.0 ● | 16.5k ● | 本地 CLI ● | 备选(不进首批) | 抖音桌面本地路径候选;但 myssia-douyin 已覆盖该场景(remote),重复收录暂缓 |
| you-get | NOASSERTION ○ | 56.9k ● | 本地 ● | **e(被覆盖)** | yt-dlp 同生态位且覆盖更窄 |
| MediaCrawler | NOASSERTION ○ | 66.2k ● | 本地 ● | **e(许可缺失)** | 小红书/快手/B站/微博多平台;仓库无标准 license=法律风险,不立项 |
| weibo-search | NONE ○ | 2.3k ● | 本地 ● | **e(许可缺失)** | 无 LICENSE 文件;微博品类将来需要时走自研 lane |

### 平台型(采集编排平台)

| 工具 | license | 星数 | 零成本/本地 | 判定 | 一句话理由 |
|---|---|---|---|---|---|
| Crawlab | BSD-3 ● | 12.3k ● | 自部署 | **d(同物种)** | 本身就是采集编排台=竞品;价值在借码(UI 线已借),不进 plugins |
| EasySpider | AGPL-3.0 ●(拆解档 ●) | 44.6k ● | 本地 | **d(同物种+AGPL)** | 点选式建源与 YAML 编辑器远期形态同位;只看不抄 |
| Maxun | AGPL(已知 ●) | 17.6k ● | 自部署 | **已收**(server-only 桩) | ✓ |
| Gerapy | MIT ● | 3.5k ● | 自部署 | **d(同物种)** | scrapy 管理台,同 Crawlab 结论 |
| ScrapydWeb | GPL-3.0 ● | 3.4k ● | 自部署 | **e(不活跃)** | 2025-02 后停更 |
| SpiderKeeper | NONE ○ | 2.8k ● | 自部署 | **e(许可缺失+量级不足)** | — |
| 八爪鱼 | 闭源商业 | — | — | **e(闭源)** | 只可作交互参考(既有结论) |

### 分析侦察型(OSINT/曝面)

| 工具 | license | 星数 | 零成本/本地 | 判定 | 一句话理由 |
|---|---|---|---|---|---|
| SpiderFoot | MIT ● | 22.8k ● | 本地 ● | **b·首批** | OSINT 自动化最全能单件;MIT 最干净;本地 web/CLI |
| theHarvester | GPL-2.0 ● | 17.8k ● | 本地 ● | **b·首批** | 邮箱/子域/IP 侦察经典;GPL 走 Photon 式 submodule 样板 |
| Amass | Other(Apache 衍 ○) | 15.3k ● | 本地 ● | **暂缓(e 观察)** | 攻击面测绘主动扫描成分高,与 L0 被动探测纪律相抵;被动子模块价值待核 ○ |
| recon-ng | GPL-3.0 ● | 6.0k ● | 本地 ● | **e(不活跃)** | 2024-11 后停更 |
| Photon | GPL-3.0 ● | — | 本地 ● | **已收**(submodule 样板) | ✓ myssia-osint |
| Huginn | MIT ● | 50.0k ● | 自部署 | **d(同物种)** | 编程式自动化台=竞品生态位;MIT 可借码参考 |

### 监控/代理型(已全覆盖)

| 工具 | license | 判定 | 备注 |
|---|---|---|---|
| changedetection.io | Apache-2.0 ● | **已收**(remote 桩) | ✓ myssia-monitor |
| proxy_pool | MIT ● | **已收**(自实现精简版) | ✓ myssia-proxy |

## 第二波候选(并行会话 PRD 骨架补遗,gh api 已核 2026-10-05)

| 工具 | license | 星数 | 零成本/本地 | 判定 | 一句话理由 |
|---|---|---|---|---|---|
| maigret | MIT ● | 38.3k ● | 本地 ● | **b·首批(升格)** | 用户名跨 3000+ 站侦察;MIT 极干净、极活跃(10-04 仍在推);OSINT 件里许可与活跃度双最优 |
| curl_cffi | MIT ●(repo 已迁 lexiforest) | 6.7k ● | 本地 ● | **a 候选(另立引擎任务,不入插件批)** | 浏览器 TLS 指纹模拟无浏览器;潜在「L2.5」档(比 static_html 强、比 crawl4ai 便宜);属核心链改动,须单独答「降级序插哪」 |
| trafilatura | Apache-2.0 ● | 6.9k ● | 本地 ● | **观察(核心 extract 能力增强候选)** | 自动正文抽取,语义属「URL→结构化内容」核心侧而非插件;与 L2 手写 extract 规则互补,另立评估 |
| undetected-chromedriver | GPL-3.0 ● | 12.9k ● | 本地 ● | **e(被 L5 覆盖+趋缓)** | 2025-07 后慢维护;playwright 隐身已占 L5 |
| urlwatch | NOASSERTION ○ | 3.1k ● | 本地 ● | **e(被覆盖)** | changedetection.io 已收同场景 |

## 首批收录建议(修订:maigret 升格进首批)

按「零成本优先+本地跑+许可干净」排序:

1. **myssia-media(yt-dlp,Unlicense)** — 视频情报品类+链外引擎,subprocess 照 Photon 样板。
2. **myssia-maigret(MIT)** — 用户名侦察 lane;OSINT 件里许可与活跃度双最优。
3. **myssia-rsshub(RSSHub,AGPL)** — 资讯源扩容 remote 桩;自部署优先,公共实例文档标注留痕。
4. **myssia-spiderfoot(MIT)或 myssia-theharvester(GPL-2)二选一** — 聚合侦察 lane,首批只做一件。

## 未核项(○ 汇总,收录实施时核)

- you-get/MediaCrawler/weibo-search/SpiderKeeper 的许可详情(API 报 NOASSERTION/NONE,实施前读仓库原文确认)
- Amass 现行 license 条款与其被动模式能力边界
- TikTokDownloader 桌面本地形态的依赖重量(实施时评)

## 第三波:开源分析方案盘点(2026-10-05 晚,find-skills 三源法;主人令「找开源分析方案查融合」)

> 发现通道:skills.sh 注册表(仅 ctf-osint 方法论件,无可吸收)+ GitHub 原生搜索(topic text-analysis/osint)+ gh api 逐件验真(license/星/活跃)。判定框同前(P0 零成本+本地执行)。

| 工具 | license | 星数 | 归位 | 一句话理由 |
|---|---|---|---|---|
| trafilatura | Apache-2.0 ● | 6.9k ● | a/b 候选(引擎侧另立任务) | 自动正文抽取;「URL→结构化内容」语义属核心 extract 面 |
| python-readability | Apache-2.0 ● | 2.9k ● | 同族备选 | 与 trafilatura 同生态位,选一即可 |
| newspaper3k | MIT ● | 15.2k ● | 同族备选 | 新闻结构化三件套里星最高,但年代偏老 |
| web-check(lissy93) | MIT ● 极活跃 | 35k ● | **c·二批候选** | 网站技术栈/DNS/SSL/头分析;JS 生态自部署桩,与 exposure lane 互补 |
| social-analyzer(qeeqbox) | AGPL-3.0 ● | 24.2k ● | c·二批候选(只桩) | 社媒画像深挖;与 maigret 互补(占用 vs 画像);2026-01 后趋缓 |
| LibreTranslate | AGPL-3.0 ● | 17.0k ● | c·备选 | 自托管翻译(外文情报);当前无品类消费面,缓 |
| RapidFuzz | MIT ● | 4.1k ● | 核心库增强候选 | dedup/实体对齐模糊匹配;库型不进插件层 |
| worldmonitor | AGPL-3.0 ● | 87.6k ● | **d(同物种不收)** | 描述即「Real-time global intelligence dashboard」=另一个 MYIA |
| yake | NOASSERTION ○ | 1.9k ● | e(许可未验) | 无监督关键词;仓库无标准 license |
| snownlp | MIT ● | 6.6k ● | e(不活跃) | 中文情感分析经典但 2020 年停更 |

**结论**:分析侧开源件当前融合 0 件(首批全是采集/侦察件;MYIA 分析回路=自研关键词分类+LLM 精评+OCR/VL)。二批建议:web-check+social-analyzer 两桩(c 路快件)+trafilatura extract 增强(引擎侧另立任务)。
