# 引擎链评估:curl_cffi 浏览器 TLS 指纹无浏览器(L2.5 候选档)

## Goal

评估 curl_cffi 为引擎降级链的「L2.5」新档候选:**浏览器 TLS 指纹模拟、无浏览器**——比 `static_html`(L2)强、比 `crawl4ai`(L3)便宜。本任务先做评估与定案(判定框 a 路两问),定案通过才进实现;答不出即不入链、记档收束。

## 背景与证据(全部引自 10-05-plugin-market-batch 既有档,本任务零新证据)

- **来源裁决**:母任务 research 第二波(2026-10-05,gh api 已核)——`curl_cffi | MIT ●(repo 已迁 lexiforest)| 6.7k ● | 本地 ● | a 候选(另立引擎任务,不入插件批)| 浏览器 TLS 指纹模拟无浏览器;潜在「L2.5」档(比 static_html 强、比 crawl4ai 便宜);属核心链改动,须单独答「降级序插哪」`(`.trellis/tasks/10-05-plugin-market-batch/research.md` 第二波表)。
- **拆任务依据**:母任务 design §1(a 路进链必答两问)/§3 尾句「a 路候选单独拆任务(涉引擎链与降级序,复杂度高于收录)」;implement 第 9 条「a 路候选(curl_cffi/trafilatura)不在本任务做:单独拆任务(引擎链+降级序设计)」。
- **链现状**(改动对象):`direct_api → static_html → crawl4ai ⇄ firecrawl → scrapling → stealth_browser → llm_browser`(`src/myssia/engines/registry.py` 模块文档);static_html=L2、crawl4ai=L3,「L2.5」即预判插二者之间。
- **宪法约束**:本地开源库、MIT 可直借、零成本本地跑(D2 硬规则全过);借轮子不自研(D3 分工线:指纹/反检测属「通用轮子借库」侧)。

## 定案问题(a 路两问,母任务 design §1 原文;两问都有实证答案才准进链)

1. **比现有档强在哪**(成本/成功率/反检测维度):curl_cffi 的 TLS/JA3 指纹模拟对「static_html 被 TLS 指纹墙拦、又不需要真浏览器渲染」的站点类,成功率增量是多少?须用可复现实验(同批 URL 三路对比 static_html/curl_cffi/crawl4ai)回答,不许拍脑袋。
2. **降级序插哪一档**:「L2.5」是预判不是定案——候选位=static_html 失败后、crawl4ai 之前;须回答:插进 `AUTO_CHAIN` 还是照 credhunter/zenrows 先例只注册 `ENGINE_REGISTRY` 链外显式选用?对 `engine: auto` 语义、`engine_hints` 胜者持久化、失败记账的影响各是什么?(答不出=不入链,落 b 或记档。)

## Requirements(骨架,planning 期细化)

- R1:两问实证材料(见上)入 `research.md`,含失败模式与边界(TLS 指纹之外的 JS 渲染站点 curl_cffi 依旧拿不下,如实记)。
- R2:依赖面评估:curl_cffi 带 C 扩展(curl-impersonate 二进制),对「核心 6 依赖红线/可选依赖纪律(`dependency_missing` 不拦链)」的合规路径(`.trellis/spec/python/index.md`)。
- R3:若定案进链:降级序/schema `EngineName` 词表/registry/AUTO_CHAIN 改动清单+爆炸半径(GitNexus impact,核心管线纪律);若定案不入链:记档一行收束,母任务 research 表回写终态。

## Acceptance Criteria(骨架)

- [x] AC1:两问各有实证答案(非推断),材料在档可复核。(research.md §1-§4;evidence/01-05 原始输出:七站三路矩阵+echo 指纹自证+robots 记档+PyPI 轮子清单)
- [x] AC2:进链/不进链定案记档;进链则降级序定案+核心链改动清单;不进链则母任务 research 表回写终态。(定案=不进链、不做链外注册、记档收束,见下方定案段;母任务 `.trellis/tasks/10-05-plugin-market-batch/research.md` 第二波表 curl_cffi 行已回写终态——时点在归档前,满足 R3 时序)
- [x] AC3:本任务止于评估定案——planning 期零核心文件改动;实现另立阶段(本档转实现前须先补 design/implement)。
  - 自查声明(2026-10-05 收束时):全程 `git status --porcelain` 核对,本任务仅写 `.trellis/tasks/10-05-engine-curl-cffi/` 内文件(research/prd/task.json/evidence)+ prd R3 明文要求的母任务 research 表终态回写一行;零核心文件改动(无 src/、tests/、desktop/、docs/、pyproject 触碰);实验全部在 /tmp/curl-eval 独立 venv,探针脚本零 myssia import。红线零违反,勾选留收口复核。
  - 收口复核回标 2026-10-05(勾选落笔):验收轮 confirmed(材料链逐格核验:探针 UA 控制组逐字节比对/矩阵原始日志归因计数/代码行号 registry.py:261/279/307/316-320 亲核/robots 8 host 原文在档);零核心改动经 `git show 43cad69 --stat` 归档轮亲证——14 件全在 .trellis/ 下(evidence 10 + 本档 prd/research/task.json 3 + 母任务 research 表终态回写 1,后者系 prd R3 明文要求),与自查声明一致。

## 定案(2026-10-05 评估收束:不进链,记档收束)

- **Q1(比现有档强在哪)**:七站三路矩阵(A=httpx+MYIA 缺省 UA / B=httpx+Chrome UA 控制组 / C=curl_cffi chrome150,B/C 的 UA 逐字节同)实证:「A 拒+B 拒+C 过」的 TLS 指纹归因形态**零例**;唯一硬墙(scrapingcourse CF managed challenge)三路全拒——curl_cffi 不执行 JS,该盲区与 static_html 同;amazon 呈反增量(未知 UA 拿全页、浏览器 UA 两路同收 202 拦截页);aihot 墙=nginx 已知爬虫 UA 黑名单(与归档 10-04-crawl4ai-l3 manifest 互证),现行 `source.headers` 配置可解。**本批规模下 TLS 指纹增量不可测/不成立**(计划指令诚实边界条款,严禁凑数)。
- **Q2(降级序插哪)**:**不进 AUTO_CHAIN、亦不做链外注册**。进链三重否决:①零实证增量(Goal 明文「答不出即不入链、记档收束」);②`registry.py:261/279/307/316-320` 的 L3 零结果探测对「下一档=crawl4ai」硬编码,插档会静默改道 10-04-crawl4ai-l3 语义(隐藏爆炸半径);③被墙源每 run 多烧一次全量 HTTP+失败噪音。再触发条件与若将来实装的链外注册形态备忘见 research.md §4.3/§4.4。
- **回写**:母任务 research 第二波表 curl_cffi 行终态已回写(活档未归档,时序合规);本档转 review。

## Constraints

- 核心管线(pipeline.py/registry.py)改动必须先报爆炸半径再动手(AGENTS.md GitNexus 纪律);评估期不动任何核心文件。
- 装不上不拦核心铁律;可选依赖缺失=结构化失败继续降级。

## Notes

- 2026-10-05 建档(「两引擎任务建档」路,与母任务批三并行会话互不阻塞)。母任务:`.trellis/tasks/10-05-plugin-market-batch/`(research 第二波证据/design §1 §3/implement 第 9 条)。
