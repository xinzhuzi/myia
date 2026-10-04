# Phase 2 盘点表(初版,2026-10-05)

> 核实通道:`gh api repos/<owner>/<repo>`(license/pushed_at/stars,2026-10-05 实测);
> 标记:●=已核实(api 或政策判定)/○=待人工补核。归位字母 = prd 判定框 a-e(D1 定案)。
> **本表待主人过目(AC2);过目后按 design §3 定批次。**

## 一、候选盘点(16 新候选 ● + 3 参照/已收 ●)

### 库型:通用抓取/解析(a 路评估组——进引擎链须答「比 scrapling 强在哪+降级序插哪」,答不出不入链)

| 工具 | 上游 | license | 活跃(pushed) | stars | 免费路径 | 本地可跑 | 建议归位 | 一句话理由 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| scrapy | scrapy/scrapy | BSD-3-Clause ● | 2026-10-04 ● | 64.6k ● | 本地开源 | ✓ | **a 评估** | 抓取框架之王;但 MYIA 是「单 URL→结构化」语义,框架级重装,增量须论证 |
| crawlee-py | apify/crawlee-python | Apache-2.0 ● | 2026-10-02 ● | 9.6k ● | 本地开源(Apify 云是可选) | ✓ | **a 评估** | 现代框架+请求自适应轮换;同上,进链前须答增量 |
| selectolax | rushter/selectolax | MIT ● | 2026-10-04 ● | 1.7k ● | 本地开源 | ✓ | **a 评估(解析内件)** | 极快 HTML 解析;属引擎内部件候选而非市场件,评估 static_html 档换装收益 |
| trafilatura | adbar/trafilatura | Apache-2.0 ● | 2026-10-02 ● | 6.9k ● | 本地开源 | ✓ | **a 评估(正文抽取)** | 正文/元数据抽取质量口碑最好;「URL→结构化」核心语义,进链候选 |
| python-readability | buriy/python-readability | Apache-2.0 ● | 2026-08-27 ● | 2.9k ● | 本地开源 | ✓ | **a 评估(与 trafilatura 二选一)** | 同类正文抽取,功能面窄于 trafilatura |
| newspaper3k | codelucas/newspaper | MIT ● | 2026-09-15 ● | 15.2k ● | 本地开源 | ✓ | **a 评估(新闻结构化)** | 新闻专用(nlp 摘要/多语言);维护节奏历史上断续,评估时核 4.x 分支状态 |
| curl_cffi | lexiforest/curl_cffi | MIT ● | 2026-10-02 ● | 6.6k ● | 本地开源 | ✓ | **a/b 评估(TLS 指纹)** | 浏览器 TLS/JA3 指纹模拟,直连被 Cloudflare 拦时比 plain httpx 强一档;**注意上游已从 yifeikong 迁 lexiforest**(本表用新址) |

### 采集专项/反检测

| 工具 | 上游 | license | 活跃 | stars | 免费路径 | 本地可跑 | 建议归位 | 一句话理由 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| undetected-chromedriver | ultrafunkamsterdam/… | GPL-3.0 ● | 2025-07(停更 ~14 月)● | 12.9k ● | 本地开源 | ✓ | **e 记档** | GPL+停滞+与现有 stealth_browser(playwright 底座)档重叠;待其复活或 playwright-stealth 需求实证再翻案 |
| Zenrows / ScraperAPI / Crawlbase 型 | 厂商 SaaS | 专有 | — | — | 按页付费 | ✗ | **e(D2 硬规则)** | 目标 URL 集+API key 绑定=最坏留痕形态;至多文档级可选后端,永不缺省 |

### OSINT/侦察(b 路组——照 credhunter/Photon 先例:插件+链外引擎)

| 工具 | 上游 | license | 活跃 | stars | 免费路径 | 本地可跑 | 建议归位 | 一句话理由 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| maigret | soxoj/maigret | MIT ● | 2026-10-04 ● | 38.3k ● | 本地开源 | ✓ | **b(首批打样候选)** | 账号名全平台枚举,MIT+pip 装零 docker,形态与 credhunter 同款 |
| theHarvester | laramies/theHarvester | GPL-2.0 ● | 2026-10-02 ● | 17.8k ● | 本地开源 | ✓ | **b(GPL→submodule 照 Photon)** | 邮箱/子域/IP 侦察经典;GPL 走 vendor submodule 样板 |
| SpiderFoot | smicallef/spiderfoot | MIT ● | 2026-04-13 ● | 22.8k ● | 本地开源 | ✓ | **c(server-only 桩)** | 自带 web UI 的 OSINT 平台,mit 本可直借但形态是服务;对齐 maxun/monitor 先例 |

### 监控/变更

| 工具 | 上游 | license | 活跃 | stars | 免费路径 | 本地可跑 | 建议归位 | 一句话理由 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| urlwatch | thp/urlwatch | BSD-3-Clause ●(license 文件名 COPYING 致 gh 探测 NOASSERTION;raw 全文人工核 2026-10-05) | 2026-07-10 ● | 3.1k ● | 本地开源 | ✓ | **b(首批打样候选)** | 轻量变更监控 CLI,零 docker;与 monitor 插件(changedetection remote)互补本地形态 |
| changedetection.io | dgtlmoon/changedetection.io | Apache-2.0 ● | 2026-10-02 ● | 34.8k ● | 本地开源/自部署 | ✓(自部署) | **已收 ●(monitor 插件先例)** | 不重复收录,作 c 路样板参照 |

### 平台/编排型(c/d 路组)

| 工具 | 上游 | license | 活跃 | stars | 免费路径 | 本地可跑 | 建议归位 | 一句话理由 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Huginn | huginn/huginn | MIT ● | 2026-10-04 ● | 50.0k ● | 本地开源/自部署 | ✓(docker) | **c(server-only 桩)** | agent 编排鼻祖;MIT 可直借,但 Ruby 服务形态=remote 桩+compose |
| Crawlab | crawlab-team/crawlab | BSD-3-Clause ● | 2026-02-10 ● | 12.3k ● | 本地开源/自部署 | ✓(docker) | **d 默认不收(c 备选)** | 同物种竞品(爬虫调度台);BSD 可借但语义牵强,仅当接用户既有部署才走 c |
| EasySpider | NaiboWang/EasySpider | AGPL-3.0 ● | 2026-09-17 ● | 44.6k ● | 本地开源(桌面 exe) | ✓ | **d/e(AGPL 只看不抄)** | 可视化点选爬虫桌面软件;AGPL 红线=不抄码不绑定,只作八爪鱼式远期形态对标物(ui-imitation 拆解表已有) |
| 八爪鱼 | 闭源商业 | — | — | — | 付费 | ✗ | **e(参照物)** | 已作 UI 模仿对标(10-03 拆解),不收录 |

### 已在体系(不重复收录,记录归位)

| 工具 | 位置 | 说明 |
| --- | --- | --- |
| playwright | 引擎链 stealth_browser/llm_browser 底座 ● | 库型已进核心,占位 |
| Photon | plugins/myssia-osint(vendor submodule,GPL)● | b 路+submodule 样板先例 |

## 二、覆盖度对表(AC2 口径)

- 形态类:**6**(库型/采集专项/OSINT/监控/平台/分析——分析并入库型 a 评估组计数)≥4 ✓
- 有名工具:核实 ● 16 项新增 + 已在体系 2 + 参照 4(SaaS×3 并一行、八爪鱼)≥15 ✓
- 待人工补核:无(urlwatch license 已补核,全表 ●)。

## 三、批次建议(design §3:首批=零 docker、宽松许可、adapter 形态)

- **首批(打样收录流水线)**:maigret(MIT,b 路)+ urlwatch(license 补核通过后,b 路);可选第三件 theHarvester(GPL submodule 打样,稍重);
- **二批(c 路打样)**:Huginn 或 SpiderFoot(server-only 桩+compose);
- **a 路评估组**(scrapy/crawlee/selectolax/trafilatura/readability/newspaper/curl_cffi):**不在本任务做**,逐个另拆任务(涉引擎链与降级序设计);
- **e 路记档**:undetected-chromedriver、SaaS 型、八爪鱼、EasySpider(AGPL)。
