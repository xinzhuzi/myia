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

- [ ] AC1:两问各有实证答案(非推断),材料在档可复核。
- [ ] AC2:进链/不进链定案记档;进链则降级序定案+核心链改动清单;不进链则母任务 research 表回写终态。
- [ ] AC3:本任务止于评估定案——planning 期零核心文件改动;实现另立阶段(本档转实现前须先补 design/implement)。

## Constraints

- 核心管线(pipeline.py/registry.py)改动必须先报爆炸半径再动手(AGENTS.md GitNexus 纪律);评估期不动任何核心文件。
- 装不上不拦核心铁律;可选依赖缺失=结构化失败继续降级。

## Notes

- 2026-10-05 建档(「两引擎任务建档」路,与母任务批三并行会话互不阻塞)。母任务:`.trellis/tasks/10-05-plugin-market-batch/`(research 第二波证据/design §1 §3/implement 第 9 条)。
