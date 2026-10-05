# Firecrawl 自托管真跑验证与部署指引(验证型档,预期零代码)

## Goal

把「Firecrawl 自托管兜底」从**设计默认**变成**实测在案**:docker compose
起自托管实例,真跑降级链中的既有 firecrawl 引擎,对 Zenrows 基线比质量,
落部署指引。**预期零代码改动**(若真跑暴露 API 兼容缺口,最小适配另立档)。

## 背景与现状(锚点——本档由池 10 候选大幅缩水而来)

- grill 事实核查(2026-10-05 深夜):**engines/firecrawl.py 已在且自托管
  是设计默认**——`DEFAULT_FIRECRAWL_ENDPOINT = "http://127.0.0.1:3002"`
  (firecrawl.py:48,自托管标准口),`MYIA_FIRECRAWL_URL`/
  `MYIA_FIRECRAWL_API_KEY` 调用时解析覆盖(:46-47);registry.py 已注册
  (:87/:114)并参与降级链(registry.py:4「…firecrawl, which needs an
  external service」)。池 10 原「Firecrawl OSS 自托管面未探」口径的
  真实缺口=**从未对真自托管实例跑通过**+无部署指引。
- 许可事实(grill 核查):server AGPL-3.0 / SDK MIT([repo](
  https://github.com/firecrawl/firecrawl));AGPL 按 RSSHub 判例=服务消费
  零代码复用合规;**不可 vendor 其 server 代码**。
- 官方自托管路径:docs.firecrawl.dev/contributing/self-host(docker
  compose);已知部分功能 cloud-only(官方明示)——缺口面如实记档。

## Requirements(验证型三件)

1. **真跑验证(主体)**:
   - docker compose 起自托管实例(本机);健康探针;
   - 挑 3-5 个真站(含 1 个 JS 重渲染站+1 个静态站对照)走既有
     FirecrawlEngine 真跑(MYIA_FIRECRAWL_URL 指向实例,零代码改动即测
     env 覆盖面);
   - 质量对照:同 URL 对 Zenrows 基线(gated 引擎)比正文完整度/
     导航剥净度(local-ocr/DOM 比对口径同 trafilatura 验收先例);
   - 差异记录:cloud-only 功能在自托管的缺失清单(如 Extract 结构化/
     某些绕过策略)如实落 evidence,不美化。
2. **部署指引(文档)**:
   - docs/README 增「自托管 Firecrawl 兜底」一节:compose 模板+env 接线
     (MYIA_FIRECRAWL_URL 指法)+AGPL 边界声明(服务消费零代码复用,
     同 RSSHub 先例句式);
   - zero-cost 指引若在册则补一行(零美元自托管路)。
3. **(可选,真跑暴露才做)doctor 端点连通项**:firecrawl 端点可达性
   doctor finding——**仅在真跑证明有价值(如实例挂了降级链静默劣化)
   才加**,否则零面。

## 测试

- 既有 engines 用例零回归(全量 pytest 门禁);
- 零新代码预期=零新测试;若 doctor 项落地→对应用例+vitest doctor 渲染。

## 验证

- 真跑产物全落 evidence/(compose 配置+请求/应答样本+对照表+截图);
- 复验口径:主人自有服务器部署后同法跑一站(AC manual)。

## Acceptance Criteria

- [ ] AC1 自托管实例真跑通:3-5 站 scrape 应答样本在档(含 JS 重站)。
- [ ] AC2 质量对照表:vs Zenrows 基线,差异与 cloud-only 缺口如实。
- [ ] AC3 指引:文档节+compose 模板+AGPL 边界句;零代码或最小适配另立
      (若适配,本档注记并指新档)。
- [ ] AC4 门禁:全量 pytest/vitest 零回归(纯文档+evidence 则豁免代码门禁,
      记档声明)。

## 边界与红线

- 不做:vendor/改其 server 代码(AGPL);把自托管 firecrawl 设为降级链
  缺省开启(现缺省链位=需外部服务才触达的语义不变,只是把它跑通+指路)。
- 前置:主人机器/服务器可跑 docker(与 SearXNG 档同款前提)。
