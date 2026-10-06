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

- [x] AC1 自托管实例真跑通:3-5 站 scrape 应答样本在档(含 JS 重站)。
      —— **2026-10-06 达成**(镜像前缀路线,详录 evidence/selfhost-run-20261006.md):
      CN 镜像前缀 `docker.1ms.run` 实测可用(postgres:17 166MB/5s≈33MB/s,
      补齐 golang:1.24+postgres:17 后 docker tag 回原名,零 daemon 配置改动),
      `docker compose up -d --build` 六容器全 Up(api 3002 就绪探针首探即
      `{"status":"ok"}`);`MYIA_FIRECRAWL_URL=http://127.0.0.1:3002 uv run
      myssia test` 四站(quotes.toscrape.com/js + example.com + HN + TC-AI)
      全 ok,JS 重站渲染内容实锤在(爱因斯坦引文 md/html 双证),直连
      /v1/scrape 五份全长应答样本落 evidence/scrape-samples/。曲折与 /tmp
      内外科修(classic builder 剥 --mount / pnpm 耐心参数 / fake-ip 环境下
      extra_hosts 钉真 IP)全录档,主人服务器复验(AC manual)可直接
      `docker compose up -d`(镜像已建成)。
      —— 前 blocked 两轮留痕:2026-10-05 docker 前置不满足;2026-10-06 00:56
      docker hub 拉层 ~50KB/s 45 分钟超时(证据 evidence/build-timeout-20261006.md)。
- [x] AC2 质量对照表:vs Zenrows 基线,差异与 cloud-only 缺口如实。
      —— **2026-10-06 达成(基线=static_html+trafilatura,非 Zenrows,主人
      放行口径)**:Zenrows 凭据上轮已证缺位(env 无 ZENROWS*+gates.yaml 不
      存在),vs Zenrows 数字对照仍留主人(AC manual);本轮对照侧改
      static_html+trafilatura(源级 extract_fallback 开启,链跑+引擎同款
      助手全长复算双口径),对照表落 evidence/selfhost-run-20261006.md §⑤:
      JS 重站 1574 字符 vs **0 条**(raw HTML 壳,firecrawl 补位实证)、
      HN 18285 vs 4101、TC-AI 20709 vs 305(列表卡片 JS 渲染基线拿不到)、
      example 958 vs 156。附:免费链真降级口径下 JS 站被本机 crawl4ai 接住
      (功能等位,firecrawl 增量=渲染负载外移)。cloud-only 缺口面维持
      official-selfhost-sources.md 结论,本轮真跑零新增暴露;/v1/scrape
      参数面(formats/timeout)与失败结构(success:false+error 码)双向
      亲证,**API 兼容零缺口、维持不另立适配档**。
      —— 前 blocked 留痕:无实例即无对照数据(两轮,见 AC1 留痕)。
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
      —— 2026-10-06 更新:AC1 真跑达成后,README 双语节与 zero-cost §4
      双语的「本机未实测」标注已翻转为「2026-10-06 本机 colima docker
      实测通过」并补国内网络注记(镜像前缀 33MB/s/classic builder 剥
      --mount/fake-ip extra_hosts 三坑与对策)。
- [ ] AC4 门禁:全量 pytest/vitest 零回归(纯文档+evidence 则豁免代码门禁,
      记档声明)。
      —— 豁免声明:本批零代码(仅 README/docs 双语 md+evidence+本档),
      按档内条款豁免全量代码门禁;定向门禁亲跑
      `uv run pytest tests/test_docs.py tests/engines/test_firecrawl.py -q`
      = 127 passed, 1 skipped(文档反漂移全套+firecrawl 引擎 18 用例零
      回归)。全量 pytest/vitest 由脚本统一跑。
      —— 2026-10-06 复跑(本轮仍零代码零文档改动,仅本档+evidence):
      `uv run --no-sync pytest tests/test_docs.py tests/engines/test_firecrawl.py
      -q` = **127 passed, 1 skipped**,与基线逐字一致零回归。
      —— 2026-10-06 三跑(本轮文档标注翻转 README+zero-cost×2,门禁面
      复验):同定向命令复跑,结果见档内实施注记·续二。

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

## 实施注记·续(2026-10-06,docker 解锁后真跑尝试受阻实况)

- **前置变化**:前序步骤完成 A 项 docker 解锁(brew 装 colima/docker/
  docker-compose 并 colima start);本轮 00:56 亲验 `docker info`(Client
  29.8.2/Server 29.5.2,context colima)+`colima status`(running,
  Virtualization.Framework)——档内「前置:主人机器/服务器可跑 docker」
  在本机已成立,blocked 的原始理由(docker 不可用)消除,按复验口径起栈。
- **起栈与超时**(详录 evidence/build-timeout-20261006.md):官方仓
  `--depth 1` 克隆 /tmp/firecrawl-e2e(不落仓库根,零 vendor 零外来
  脏面);上游漂移核对——SELF_HOST.md 改版无 Required ENVS 段但
  `USE_DB_AUTHENTICATION=false` 仍必设(:25),compose 引用实核
  (docker-compose.yaml:33),三行模板仍有效;`docker compose up -d
  --build` 后台+exit 文件法,45 分钟未完(docker hub 大层 ~50KB/s 级,
  117 层完成含 foundationdb 1.53GB,playwright 层 95/113MB,api 本地
  build 未及开始)→ 按计划时间盒纪律(20+20 延长+缓冲)TaskStop 降级,
  `docker compose down --remove-orphans` 清场零残留;镜像缓存+/tmp
  克隆(含 .env)保留备复验。**AC1/AC2 真跑仍留主人服务器,档维持
  blocked,瓶颈从「无 docker」迁移为「docker hub 拉层带宽」**。
- **站单四站+robots 亲取**(备复验直接用,全部 curl 2026-10-06):
  quotes.toscrape.com/js/(JS 重站,robots 404=无限制)、example.com
  (静态,IANA 文档域自述许可)、news.ycombinator.com/(首页允许,
  Crawl-delay 30 单次无碍)、techcrunch.com/category/artificial-
  intelligence/(通用段允许该路径)。两份临时品类 YAML(firecrawl 侧
  env:MYIA_FIRECRAWL_URL 引用+免费链对照侧)已备 /tmp 并过
  load_category_file 真载校验,因栈未起未及真跑,复验时直接取用。
- **Zenrows 凭据实查**:env 无 ZENROWS*、~/.myia/gates.yaml 不存在 →
  saas.zenrows 门槛未开;AC2 的 vs Zenrows 对照本机无论实例起否均不可
  得,留主人(如主人配 gates.yaml saas.zenrows.api_key 引用+钥匙串值)。
- **本轮交付面**:零代码零产品文档改动(验证型预期维持);新增证据
  evidence/build-timeout-20261006.md;AC4 定向门禁复跑 127 passed
  1 skipped 与基线一致。

## 收口注记(2026-10-06,「余量全清」归档会话;档维持 blocked 不归档)

- 统一批全量门禁亲跑绿(pytest 4461/40/0+vitest 523+tsc -b 零错+vite
  build+cargo check --locked+cargo test 56+ruff 全仓)+推送 CI 绿
  (run 37352272165,conclusion=success,headSha ff3e4a9 亲验);本档
  零代码零产品文档,门禁面无增量,AC4 定向基线(127 passed 1 skipped)
  维持逐字一致。
- AC1/AC2 真跑与 vs Zenrows 对照仍留主人(docker hub 拉层带宽 ~50KB/s
  级+saas.zenrows 凭据缺位,详见 evidence/build-timeout-20261006.md);
  镜像缓存 2.4GB+ 与 /tmp/firecrawl-e2e 克隆(含 .env)保留,网络良好
  窗口续跑 `docker compose up -d --build` 可免重下。
- 归档判据:AC1/AC2 未达成(真跑未发生),依「CI 未绿则涉门禁档留守」
  同精神——真跑未成的验证档不伪勾不归档,留主人服务器复验后续收。

## 实施注记·续二(2026-10-06 11:57-13:35,镜像前缀路线真跑全绿,AC1/AC2 闭)

- **路线**:按主人令走「镜像前缀拉取+docker tag 回原名」(零 daemon/colima
  配置改动)。三前缀 manifest 全通,**docker.1ms.run 首个真拉可用**:
  postgres:17 166MB/5s≈33MB/s(vs 上轮 docker hub 直连 ~50KB/s);golang:1.24
  首拉 759s 未完系**并行 searxng 线 `colima stop` 连带停了共享 colima VM**
  (host agent 日志 SIGINT 优雅停机实锤,非崩溃;VM 磁盘无损,复起后续拉
  17s 完,已提交层复用)。上轮卡死的 112.9MB 层实为 postgres:17 基镜像层
  (层 ID b9bd31abcf11 比对实锤)。
- **起栈曲折(全录 evidence/selfhost-run-20261006.md §②)**:①容器内
  github TLS 瞬断(Step 14 FDB deb,宿主同 URL 200——重试即过);②本机
  docker CLI 无 buildx 插件→compose 固走 classic builder→Dockerfile
  `--mount=type=cache` 行不可解析(标签 builder=classic 实证);/tmp 克隆
  内剥除三缓存挂载+pnpm 耐心参数(npm CDN 中途降速 ~20-40KB/s,首轮 721/780
  超时,次轮 780/780 过)。13:23 六容器全 Up,readiness 首探 200
  {"status":"ok"}。时间盒 45 分钟到点时 pnpm 744/780 推进中,按上轮
  「延长一轮」先例延至硬顶 13:25,实际 13:23 完成(延展决策如实记)。
- **fake-ip 环境 vs SSRF 守卫(本轮最大发现,§③)**:宿主 clash fake-ip 在
  TUN 层劫持所有 UDP 53(容器强制 --dns 223.5.5.5 仍回 198.18.x.x),
  firecrawl 双守卫(api safeFetch+playwright-service)按 RFC 保留段判内网
  拒连→起栈后首跑全站 500。解法=宿主 alidns DoH 取四站真实 IP,compose
  给 api/playwright-service 加 extra_hosts 钉真 IP(仅 /tmp 克隆内),
  force-recreate 后全通。**主人服务器无 fake-ip 环境无此坑**;对策已入
  zero-cost §4 注记。
- **AC1**:四站 myssia test 全 ok(引擎零改动,env 覆盖面真测);直连
  /v1/scrape 五份全长样本落 evidence/scrape-samples/;JS 重站渲染内容
  md/html 双证。
- **AC2**:基线按放行口径=static_html+trafilatura(非 Zenrows,Zenrows
  数字对照留主人),对照表+免费链 crawl4ai 功能等位注记落 §⑤;API 兼容
  零缺口(v1 面参数+失败结构双向亲证),维持不另立适配档。
- **文档**:README 双语节+zero-cost §4 双语「未实测」标注翻转为实测通过
  +国内网络三坑注记(镜像前缀/无 buildx 剥 --mount/fake-ip extra_hosts)。
- **门禁**:定向 `uv run --no-sync pytest tests/test_docs.py
  tests/engines/test_firecrawl.py -q` = 127 passed, 1 skipped(文档反漂移
  全套过=标注翻转零破坏;firecrawl 引擎 18 用例零回归);全量 pytest/
  vitest 归脚本统一批,本档零代码改动面维持。
- **收尾**:六容器 compose down 清场(镜像 5.2GB+留存,复验 `docker
  compose up -d` 秒级);/tmp 克隆三处 /tmp 内修带注释留存;本流零仓库外
  脏面。**档置 review**:AC1/AC2 本机闭+AC3 既有+AC4 定向绿,vs Zenrows
  数字对照与主人服务器 AC manual 复验留主人。
