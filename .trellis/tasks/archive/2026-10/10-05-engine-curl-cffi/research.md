# research — curl_cffi 引擎链评估(10-05-engine-curl-cffi,Q1/Q2 两问实证)

> 评估期:2026-10-05 午后。执行者:执行者-curl_cffi 评估(动态工作流子代理)。
> 机器:macOS darwin 25.4.0 arm64。实验环境:/tmp/curl-eval 独立 venv
> (uv venv + uv pip install httpx curl_cffi,**零 myssia import**——评估期零核心
> 依赖,亦天然免疫 selectolax 解析墙)。

## 0. 结论速览

- **Q1(成功率增量)**:本批七站实证规模下,「static_html 被拦 + 换 UA 无效 +
  仅 curl_cffi 能过」的 TLS 指纹归因形态**零例**。TLS 指纹增量**不可测/不成立**
  (倾向结论:不进链)。指纹模拟本身有效(echo 自证:chrome150 指纹真实生效),
  但「指纹墙」在单次探询规模上未找到可归因的站。
- **Q2(降级序)**:**不进 AUTO_CHAIN、亦不做链外注册——记档收束**(prd Goal 明文
  「答不出即不入链、记档收束」)。再触发条件与若将来实装的形态建议见 §4。
- **定案一句话**:七站三路矩阵零「仅 C 过」例 + 唯一硬墙(CF managed challenge)
  三路全拒,故 curl_cffi 相对 static_html+headers 配置的增量无实证,不进链,
  母任务 research 表回写终态收束。

## 1. 实验设计(Q1)

### 1.1 三路定义(计划指令定案,B 路控制组必在)

| 路 | 客户端 | UA | 语义 |
|---|---|---|---|
| A | httpx 0.28.1(HTTP/1.1) | `MYIA/0.1 (config-driven intelligence hub)`(与 `src/myssia/engines/fetch_base.py:135` DEFAULT_USER_AGENT 逐字节一致) | 现状 static_html 的忠实探针 |
| B | httpx 0.28.1(HTTP/1.1) | Chrome/150 UA(**取自 C 路对 echo 端点实发 UA 的回读**,与 C 逐字节同) | 控制组:今天在 static_html 里改 `source.headers` 就能达到的形态——B 过 = UA 归因,与 TLS 无关 |
| C | curl_cffi 0.16.3 `impersonate="chrome"`(DEFAULT_CHROME=chrome150,macOS Tahoe;实测协商 HTTP/3) | 由 curl-impersonate C 层设置(回读=Chrome/150) | 待评估引擎 |

B 与 C 的 UA 逐字节一致,差异收窄到 TLS+HTTP/2/3 指纹与底层栈(libcurl vs
python-ssl)——恰是 curl_cffi 相对「headers 可配的 httpx」的唯一增量面。

### 1.2 指纹自证(Phase 0,echo 端点,每路单次)

echo = `https://tls.browserleaks.com/json`(robots.txt 404=无限制,02 号证据记档)。

| 路 | status | HTTP | JA3 | JA4 | verdict |
|---|---|---|---|---|---|
| A | 200 | 1.1 | `304734bb1c086c3453b387400cf83f11` | `t13d1812h1_85036bcba153_d41ae481755e` | ok |
| B | 200 | 1.1 | `304734bb1c086c3453b387400cf83f11`(与 A 完全同) | `t13d1812h1_85036bcba153_d41ae481755e`(与 A 完全同) | ok |
| C | 200 | 3 | `ba1e7cdeb2ff07d7d0179cfd44c652f6` | `t13d1516h2_8daaf6152771_806a8c22fdea` | ok |

两点方法学效力:①**控制组成立**——B 换 UA 后 JA3/JA4 与 A 完全一致,证明
「改 UA 不改 TLS 指纹」,B/C 差异只能来自指纹与栈;②**impersonation 真实生效**
——C 呈 Chrome 系指纹(JA4 的 `h2` ALPN 令牌 vs A/B 的 `h1`),UA 回读为
Chrome/150。即:curl_cffi 的机制在本机可用且真实,以下矩阵差异(或无差异)
是站点侧事实,不是工具失效。

### 1.3 站点清单与 robots 记录(涉网纪律)

每站先 `curl -s https://<host>/robots.txt` 单次查并原文记档(evidence/02 系列)。
**reddit 被 robots 剔除**(`User-agent: * → Disallow: /` 全站禁抓,02 号证据原文),
否则它本是文献在案的 TLS 墙例。终版清单(7 站,首轮 5 + 二轮 2):

| 站 | URL | 选站理由 | robots 结论 |
|---|---|---|---|
| aihot.news item | `/items/bzodztryi4kvwm4kz9mrwb6nn` | 归档基线 URL(见 §3.1) | `*` 组明文「不再 Disallow /items/」(02b) |
| airbnb 首页 | `https://www.airbnb.com/` | curl_cffi README 经典 TLS 指纹墙例 | `*` 组放行首页(02c) |
| nowsecure.nl | `https://nowsecure.nl/` | Cloudflare 挑战测试页 | robots 无任何 Disallow(02) |
| scrapingcourse | `/cloudflare-challenge` | CF managed challenge 测试页 | `*` 仅禁 `/ecommerce/*`(02c) |
| Hacker News 首页 | `https://news.ycombinator.com/` | 无墙对照(假阳性检查) | 放行首页,Crawl-delay 30(02b) |
| amazon 首页 | `https://www.amazon.com/` | TLS 墙文献例(python TLS 常 503 captcha) | `*` 组放行首页(02d) |
| zillow 售房页 | `/homes/for_sale/` | Cloudflare 硬墙文献例 | `*` 组明文 Allow 该路径(02d) |

纪律执行:每 URL 每路**单次**探询性请求,超时 20s,失败不重试不轰炸,同站相邻
请求间 1s 礼貌间隔(脚本 `time.sleep(1)` 落地,probe_tls_matrix.py)。

## 2. 四/三路对比矩阵(原始数据)

### 2.1 内容站矩阵(03/04 号日志;B 路控制组在列,未省略)

| 站 | A(httpx+MYIA UA) | B(httpx+Chrome UA) | C(curl_cffi chrome150) | 归因 |
|---|---|---|---|---|
| aihot item | 200 / 47028B / h1.1 / 0.36s | 200 / 47028B / h1.1 / 0.19s | 200 / 47028B / h3 / 0.06s | **无墙**:三路字节同,标题同(`GPT-6.1 Sol (Max)…· AIHOT`) |
| airbnb 首页 | 200 / 633437B / 1.87s | 200 / 619327B / 1.96s | 200 / 633032B / h3 / 1.63s | **无墙**(历史 TLS 墙未复现,见 §3.3) |
| nowsecure.nl | 200 / 179833B | 200 / 179833B | 200 / 179833B / h3 | **无墙**(现配置不发挑战) |
| scrapingcourse CF | **403** challenge / 5618B | **403** challenge / 5810B | **403** challenge / 6002B / h3 | **硬墙**:三路全拒(`cf-mitigated: challenge`,标题 `Just a moment...`) |
| HN 首页 | 200 / 34678B | 200 / 34678B | 200 / 34678B / h3 | 无墙对照 ✓(零假阳性) |
| amazon 首页 | 200 / **767407B** 全页 / 1.87s | **202** / 2007B 薄页 / 1.09s | **202** / 2007B 薄页 / 0.97s | **反增量**:未知 UA 拿全页,浏览器 UA 两路同收 CloudFront 202 拦截页 |
| zillow 售房页 | 200 / 672916B | 200 / 672908B | 200 / 672902B / h3 | 无墙(单次规模) |

判据(`classify`,probe_tls_matrix.py):2xx+载荷≥200B+非挑战页标题 = ok。
一处**如实更正**:amazon 的 202+2007B 被脚本机械判「ok」(2xx 通道),人工判读
应为软拦截(202 CloudFront 反机器人过渡页,字节数即自证)——上表已按原始字段
更正标注,原始数据不变。

### 2.2 归因矩阵判读(计划指令的判据)

| 形态 | 判读 | 本批出现次数 |
|---|---|---|
| A 拒 + B 拒 + C 过 | TLS 指纹归因(curl_cffi 可进链的实证基础) | **0** |
| A 拒 + B 过 | UA 归因(headers 配置可解,curl_cffi 增量存疑) | **0**(aihot 的墙只打已知爬虫 UA,MYIA 未知 UA 直过,连 A 都不拒) |
| 全拒 | 硬墙(JS 挑战类,curl_cffi 不够) | **1**(scrapingcourse) |
| 全过 | 本站无墙 | 5(aihot/airbnb/nowsecure/zillow/HN) |
| A 过 + B/C 拒 | 反增量(impersonation 引更多审视) | **1**(amazon) |

**Q1 答案:本批规模下 TLS 指纹增量不可测/不成立。**倾向结论:不进链(依据
计划指令诚实边界条款,严禁凑数)。

## 3. 失败模式与边界(如实)

### 3.1 crawl4ai 路的覆盖边界(归档引用,不重跑)

归档 `.trellis/tasks/archive/2026-10/10-04-crawl4ai-l3/evidence/smoke/`:
- `direct-engine-run.log`/`manifest.md`:aihot item 页 crawl4ai 真跑 PASS
  (engine=crawl4ai, items=1, markdown_len=3949, elapsed 1.99s,hint 回写 crawl4ai);
- `manifest.md:5` 并记:**裸 curl(缺省 UA)直访该页 403,系 nginx UA 黑名单**
  ——本次矩阵用 MYIA UA 直过 200,与归档结论互证:该站墙是「已知爬虫 UA 黑名单」
  (curl/SemrushBot 等),非 TLS 指纹墙,亦不拦未知 UA。
- 七站中仅 aihot 与归档 URL 重合;其余六站无 crawl4ai(真浏览器)对照——**不补跑**
  (计划指令:优先引用归档,URL 不重合时如实记覆盖边界,不装不强凑)。

### 3.2 JS 渲染站:curl_cffi 依旧拿不下(prd R1 明文要求如实记)

curl_cffi 是「无浏览器的浏览器**传输层**指纹」,**不执行 JS**。本批实证:
scrapingcourse CF managed challenge 三路全拒(403 `Just a moment...`,
`cf-mitigated: challenge`)——指纹完全对齐 Chrome 也过不了挑战,这类站仍需
L3+(crawl4ai/stealth_browser)。JS 渲染空壳页同理:拿回的 HTML 同 static_html
 一样是壳,curl_cffi 无渲染能力。**「L2.5」的想象空间只覆盖「TLS 墙 + 静态
HTML 有内容」的交集,本批未找到该交集的现实站。**

### 3.3 时点性与波动(单次探询的固有边界)

airbnb(README 时代经典 TLS 墙)与 nowsecure.nl(挑战测试页)在 2026-10-05
单次探询下均直放——边缘策略随时间放宽/收紧,本结论是时点性的。同因,amazon
的 202 拦截页与 UA 相关行为也可能随出口 IP/时段波动。**本实验不重试不复跑**
(涉网纪律),波动一律如实记「环境时点性」。

### 3.4 其余未验项

- aihot item 页静态 HTML(47028B)是否含完整正文(还是仅 SSR 骨架)未验——
  三路字节一致已足以回答「墙」问题,正文抽取不在本评估范围(单次纪律未重取)。
- 六座公共站均未与真实 myssia static_html 管线串跑(评估期零核心 import);
  A 路已按 DEFAULT_USER_AGENT 逐字节对齐,等价性建立在 UA 一致 + httpx 同版本
  (0.28.1 与仓库 uv.lock 的 httpx 主版本同代)上。
- GitNexus impact 未跑:零核心文件改动,无编辑对象(AGENTS.md 纪律针对「改
  符号前」,本任务不改符号;若将来实装,impact 属实现阶段动作,见 §4.4)。

## 4. Q2:降级序插哪(AUTO_CHAIN vs 链外注册)

以当前树为地基准(全部亲读,非推断):

### 4.1 地基准事实(代码引用)

- **AUTO_CHAIN 七档**:`src/myssia/engines/registry.py:79-87`
  (direct_api→static_html→crawl4ai→firecrawl→scrapling→stealth_browser→llm_browser)。
- **链外先例**:`registry.py:103-117` —— credhunter(源引擎,组装型非抓取型)
  与 zenrows/scraperapi(付费 SaaS,gates.yaml 知情开关前置于 fetch,关闭态
  `gate_closed` 零上游请求)注册于 ENGINE_REGISTRY 而不在 AUTO_CHAIN;模块
  文档 `registry.py:34-43` 明示两类的链外理由各属。
- **链外引擎的运行语义**:`registry.py:159-160`(auto_degrade 对链外名返回
  单档链 `[preferred]`,auto 永不路过)+ `resolve_engine`(`registry.py:128-136`,
  注册表查表即得,链内链外同一入口)。
- **hint 机制**:`registry.py:248-250`(hint 命中即前置,仍在链内才生效)、
  `:338-339`(成功者回写 hint)、`:293-295`(hint 失败且非 proxy_* 即清除回落)。
- **L3 零结果探测对档名的键控**:`registry.py:261`(探测短帽只注入
  `engine_options.crawl4ai.timeout`)、`:279`/`:307`(异常/零条回滚分支判
  `engine_name == "crawl4ai"`)、`:316-320`(武装条件判 `"crawl4ai" in chain`/
  `not in attempted`)——**探测语义硬编码「下一档= crawl4ai」**。
- **失败记账**:每次尝试记 EngineFailure(`registry.py:265-273`),hint 命中
  引擎失败即清 hint 回落,proxy_* 家族短路(`:296-304`)。
- **schema 词面**:`src/myssia/schema.py:150-165`(ENGINES 元组)与
  `:217-221`(EngineName Literal)——进链/链外都要动这里,是核心 schema 面。

### 4.2 逐维分析

1. **engine: auto 语义**:curl_cffi 免费本地,zenrows 的「auto 不得暗路由付费
   流量」理由**不能援引**(性质不同,计划指令预判正确)。但进链的正当性仍须
   Q1 增量实证支撑——七站矩阵零「仅 C 过」例,进链等于给**所有** auto 源在
   static_html 与 crawl4ai 之间加一档,而该档的收益未被证明。
2. **与 L3 探测的交互(进链的隐藏爆炸半径)**:若按预判插 static_html 之后、
   crawl4ai 之前,`fetch_source` 的零结果探测会先武装再命中 curl_cffi 而非
   crawl4ai(`registry.py:261/279/307` 的键控全写死 crawl4ai),10-04-crawl4ai-l3
   的「L3 首遇探测」语义被静默改道——探测短帽注入的 `engine_options.crawl4ai.
   timeout` 对 curl_cffi 档无效,须同步改写四处键控。这是**进链成本显著高于
   表面一行的实证**。
3. **engine_hints 胜者持久化**:curl_cffi 若在链内胜出即钉 hint。钉住的语义
   只有在「该源长期只有指纹档能过」时才合意;本批该类源为零,hint 面无实证
   需求。反之,链外注册(显式 engine: curl_cffi)不写 hint 也能跑
   (fetch_source 对单档链同样回写 hint——注意链外胜者也会钉 hint,
   `registry.py:338-339` 不分链内外;可接受,源级显式配置语义本就「用户说了算」)。
4. **失败记账与运行成本**:进链后每个被墙源每 run 多烧一次全量 HTTP
   (curl_cffi 失败后才轮到 crawl4ai)——对 §3.2 的 JS 挑战墙,curl_cffi 与
   static_html 同盲区,多出的请求是纯开销+目标站负担+失败日志噪音。
   EngineFailure 面本身无需新失败类(复用 classify_exception 通道),但
   dependency_missing(未装 extras 时)在链内= 多一档结构化失败记录,链外=
   显式选择的单档失败。
5. **R2 依赖面**:curl_cffi 带 C 扩展(cffi + curl-impersonate 二进制捆包)。
   亲装实证:`uv pip install` mac arm64 wheel 直装(0.16.3,01 号日志);PyPI
   JSON(05 号日志)示 0.16.3 轮子覆盖 mac x86_64/arm64、manylinux x86_64/
   aarch64/i686/armv7l/riscv64、musllinux、win_amd64/win_arm64、android,
   requires_python>=3.10(abi3)——**三桌面平台轮子齐**,无 ocrmac 式平台
   标记风险。可选依赖纪律路径成熟:照 crawl4ai/scrapling 先例进
   `[project.optional-dependencies]`(如 `curl_cffi = ["curl_cffi>=0.16"]`),
   引擎模块惰性 import,缺装报 `dependency_missing` 结构化失败继续降级
   (registry.py 模块文档 :13-18 的既有约定)——合规无障碍,但合规≠该做。

### 4.3 定案

**不进链,亦不做链外注册,记档收束。**理由链:

1. Q1 增量不可测/不成立(prd Goal:「答不出即不入链、记档收束」——本档自带的
   缺省判决路径);
2. 唯一实证的墙(JS managed challenge)恰是 curl_cffi 的盲区,该场景已有
   L3/L5 档承接;
3. 本批唯一 UA 类墙(aihot/nginx 黑名单)已可用现行 `source.headers` 配置解,
   零代码;
4. 链外注册仍要动 schema 词面+registry+引擎模块+测试(核心文件面),零实证
   收益下违反「先证后建」;
5. 进链另有 §4.2-2 的 L3 探测键控改写成本,爆炸半径大于表面。

**再触发条件**(任一满足即重开评估,循本档材料续答而非重来):

- 真实源池出现实证案例:「static_html 被拦(403/挑战)、换 UA 无效(B 路
  控制组同拒)、内容在静态 HTML 内(不需 JS 渲染)」——即 §3.2 交集的现实站;
- 届时形态建议:**链外 ENGINE_REGISTRY 注册**(循 credhunter 先例:显式
  `engine: curl_cffi` 单档链,auto 永不路过;extras 可选依赖+惰性 import+
  dependency_missing 不拦显式选择的源级失败语义),**不进 AUTO_CHAIN**;
  进链须连同 L3 探测键控改写一起重新设计,并先跑 GitNexus impact。

### 4.4 若将来实装的改动清单备忘(非本任务范围)

- `src/myssia/engines/curl_cffi.py`(新引擎模块,照 saas.py 骨架纪律:模块
  docstring 注理由与边界)+ `registry.py` ENGINE_REGISTRY 一行(链外);
- `schema.py` ENGINES 元组与 EngineName Literal 各加一词;
- `pyproject.toml` optional-dependencies 加 extras 组;tests/engines/ 新测
  (缺装 dependency_missing、单档链语义、robots 礼貌约束复用 fetch_base);
- 提交前 `gitnexus detect-changes -r shishi --scope staged`(AGENTS.md 纪律)。

## 5. R3 落实与母任务回写

- 本档即「记档一行收束」的落笔(research.md §0/§4.3 + prd.md 定案段)。
- 母任务 `.trellis/tasks/10-05-plugin-market-batch/research.md` 第二波表
  curl_cffi 行已回写终态(时点:母任务尚在活档未归档,回写于归档前——prd R3
  时序要求满足)。
- 不推远端、不打 tag(收口阶段统一)。

## 6. 材料清单(evidence/)

| 文件 | 内容 |
|---|---|
| `01-venv-install.log` | /tmp/curl-eval venv 装机日志(httpx 0.28.1 + curl_cffi 0.16.3,mac arm64) |
| `02-robots-raw.md` + `02b/02c/02d-robots-supplement*.md` | 全部 8 host robots.txt 原文/定向摘录(reddit 全站禁抓原文在列) |
| `probe_tls_matrix.py` | 首轮探针(三路定义/判据/纪律落地;零 myssia import) |
| `03-tls-matrix-run.log` | 首轮原始输出(Phase 0 echo 自证 + 5 站矩阵 + 全量 JSON) |
| `probe_tls_matrix_phase2.py` + `04-tls-matrix-phase2.log` | 二轮补测(amazon/zillow)原始输出 |
| `05-pypi-wheels.md` | PyPI 0.16.3 轮子平台清单(单次 API 查询) |

复跑口径:`uv venv /tmp/curl-eval && uv pip install --python /tmp/curl-eval httpx curl_cffi`
,再以该 venv 的 python 依次跑两个探针脚本(涉网纪律:单次探询,不复跑轰炸)。
