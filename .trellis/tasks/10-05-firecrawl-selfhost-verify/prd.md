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
      —— blocked:本机 docker 前置不满足(Docker Desktop 已卸尽,坏符号
      链接+无 colima/podman/lima/orbstack+无 socket,探针全录
      evidence/docker-unavailable-probe.txt)。真跑与应答样本留主人服务器
      (AC manual;复验法=zero-cost §4 末注记:`myssia test <品类>.yaml
      --json` 挑 JS 重站跑一遍)。
- [ ] AC2 质量对照表:vs Zenrows 基线,差异与 cloud-only 缺口如实。
      —— blocked 同 AC1(无实例即无对照数据);cloud-only 缺口面已按官方
      四来源如实落 evidence/official-selfhost-sources.md 并入文档节
      (Fire-engine 全家/LLM 抽取自带端点/agent-browser-interact 云端/
      默认栈无鉴权无 TLS),vs Zenrows 的正文完整度对照缺真跑,不虚构。
- [x] AC3 指引:文档节+compose 模板+AGPL 边界句;零代码或最小适配另立
      (若适配,本档注记并指新档)。
      —— 2026-10-05 交付:README 双语「自托管 Firecrawl 兜底」节 +
      docs/{zh,en}/zero-cost.md §4 双语镜像(compose 起法+.env 三行模板+
      就绪探针+MYIA_FIRECRAWL_URL 指法+按源 env: 引用示例+AGPL 服务消费
      边界句同 RSSHub 先例+cloud-only 缺口清单),均标注「本机未实测」。
      模板逐句来自官方 self-host 文档(来源四件见 evidence)。零代码达成
      ——未暴露需适配的 API 缺口:引擎打 `POST /v1/scrape`,现行上游
      `apps/api/src/index.ts` 明挂 v1 路由(源码级佐证,非真跑,真跑归
      AC1 复验),故无需另立适配档。
- [ ] AC4 门禁:全量 pytest/vitest 零回归(纯文档+evidence 则豁免代码门禁,
      记档声明)。
      —— 豁免声明:本批零代码(仅 README/docs 双语 md+evidence+本档),
      按档内条款豁免全量代码门禁;定向门禁亲跑
      `uv run pytest tests/test_docs.py tests/engines/test_firecrawl.py -q`
      = 127 passed, 1 skipped(文档反漂移全套+firecrawl 引擎 18 用例零
      回归)。全量 pytest/vitest 由脚本统一跑。

## 边界与红线

- 不做:vendor/改其 server 代码(AGPL);把自托管 firecrawl 设为降级链
  缺省开启(现缺省链位=需外部服务才触达的语义不变,只是把它跑通+指路)。
- 前置:主人机器/服务器可跑 docker(与 SearXNG 档同款前提)。

## 放行回执(2026-10-05 深夜,主人令「都按建议去做」)

- 问题:自托管 docker 前提。做法:主人整体放行,排队第 5(验证型零代码预期);本机 compose 真跑先行,主人服务器复验 AC manual。
- 执行顺序(全五档):cron-heartbeat(先做,零前置)→ push-bark → push-apprise(点名即启)→ source-searxng → firecrawl-selfhost-verify。

## 实施注记(2026-10-05,blocked 分支如实记)

- **docker 前置不满足 → 走档内替代分支**(docs 节照写+标注本机未实测):
  本机 Docker Desktop 已卸载——`/usr/local/bin/docker` 为指向不存在的
  `/Applications/Docker.app` 的坏符号链接;无 daemon socket、无 DOCKER_HOST、
  无 colima/podman/lima/orbstack 任何替代运行时,仅剩 vmnetd 残留进程。
  五步探针全录 `evidence/docker-unavailable-probe.txt`。不擅自装容器运行时
  (主人已卸载即意图明示;档内前置=「主人机器可跑 docker」是前提不是待办)。
- **交付面(零代码)**:README 双语「自托管 Firecrawl 兜底」节 +
  `docs/{zh,en}/zero-cost.md` §4 双语镜像。compose 起法与 .env 模板逐句
  取自官方 SELF_HOST.md;就绪探针 `/v0/health/readiness` 取自官方文档站
  (钉 v2.11.162);资源上限(api 4C/8G)取自官方 docker-compose.yaml。
  AGPL 服务消费边界句同 RSSHub 先例(plugins/myssia-rsshub/README.md:5-6
  句式);cloud-only 缺口清单不美化(Fire-engine/截图/页面操作、LLM 抽取
  自带端点、agent-browser-interact、默认栈无鉴权无 TLS)。
- **API 兼容缺口核查(源码级,未真跑)**:引擎打 `POST {endpoint}/v1/scrape`
  (src/myssia/engines/firecrawl.py:181),现行上游 apps/api/src/index.ts
  `app.use("/v1", v1Router)` 明挂 v1 面;自托管 API key 可选(官方
  Troubleshooting 原句)与引擎「未配置 key 不发 Authorization 头」行为吻合
  (firecrawl.py:183-184)。**结论:暂无适配需求,不另立档**;若主人服务器
  复验暴露 v1 面行为差(如格式字段拒收),再立最小适配档。
- **doctor 端点连通项(Requirement 3)**:真跑未发生→「实例挂了降级链静默
  劣化」无实证,按档内「否则零面」不做。
- **门禁**:定向 `uv run pytest tests/test_docs.py tests/engines/test_firecrawl.py
  -q` = 127 passed, 1 skipped(2026-10-05 亲跑);全量归脚本。AC4 豁免
  条款已声明(纯文档+evidence 零代码)。
- **复验口径(AC manual,留主人)**:可跑 docker 的机器按 zero-cost §4 起
  栈 → `MYIA_FIRECRAWL_URL` 指实例(标准口可免)→ `uv run myssia test
  <品类>.yaml --json` 挑 1 个 JS 重站 + 1 个静态站 → 应答样本与 Zenrows
  对照落本档 evidence/,AC1/AC2 即闭。
