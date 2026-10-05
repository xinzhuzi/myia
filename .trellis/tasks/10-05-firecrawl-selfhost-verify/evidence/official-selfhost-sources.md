# 官方 self-host 资料取证(10-05-firecrawl-selfhost-verify,2026-10-05)

本机 docker 不可用(见 docker-unavailable-probe.txt),真跑分支转 blocked;
「自托管 Firecrawl 兜底」文档节(compose 模板/env 接线/cloud-only 缺口/AGPL
边界)以下列官方来源为准逐句落笔,并标注「本机未实测」。取证时间
2026-10-05;上游 master 面快照。

## 来源 1:仓库 SELF_HOST.md(官方自托管指南)

<https://github.com/firecrawl/firecrawl/blob/master/SELF_HOST.md>

关键摘录:

- 起法三步:装 Docker → 根目录建 `.env` → `docker compose build` +
  `docker compose up`;实例落在 `http://localhost:3002`。
- `.env` 必填面(===== Required ENVS ===== 段原文):
  `PORT=3002`、`HOST=0.0.0.0`、`USE_DB_AUTHENTICATION=false`
  (注释原句:"To turn on DB authentication, you need to set up Supabase.")。
- `PLAYWRIGHT_MICROSERVICE_URL` / `REDIS_URL` 由 docker-compose.yaml
  自动配置,不需手设(文件内注释原句:"This is now autoconfigured by the
  docker-compose.yaml. You shouldn't need to set it.")。
- 自托管 API key 可选(Troubleshooting 段原句:"When using Firecrawl SDKs
  with a self-hosted instance, API keys are optional. API keys are only
  required when connecting to the cloud service (api.firecrawl.dev).")——
  与 MYIA 引擎行为吻合:api_key 未配置则不发 Authorization 头
  (src/myssia/engines/firecrawl.py:183-184)。
- 官方示例验证调用打 **v1 面**:`curl -X POST http://localhost:3002/v1/crawl …`。
- Fire-engine 缺口明示(Considerations 段):"self-hosted instances of
  Firecrawl do not have access to Fire-engine, which includes advanced
  features for handling IP blocks, robot detection mechanisms, and more."
- 安全面:强 PostgreSQL 凭据、数据库端口不外露、公网部署必换
  `BULL_AUTH_KEY`。

## 来源 2:仓库 docker-compose.yaml(官方栈结构)

<https://github.com/firecrawl/firecrawl/blob/master/docker-compose.yaml>

服务清单:playwright-service(2 CPU/4G 上限)、api(端口
`${PORT:-3002}`,4 CPU/8G 上限)、redis、rabbitmq(healthcheck 门)、
nuq-postgres(实验性 FoundationDB 替代另列)。api 的 depends_on 拿
redis/playwright/rabbitmq;v1 面即此栈服务。

## 来源 3:apps/api/src/index.ts(v1 路由挂载——引擎兼容性源码级证据)

<https://github.com/firecrawl/firecrawl/blob/master/apps/api/src/index.ts>

原文:`app.use("/v1", v1Router);`(另有 v0Router 与 `app.use("/v2", v2Router)`)。
→ 现行自托管 API 服务端同时挂 v0/v1/v2 三面;MYIA 引擎打的
`POST {endpoint}/v1/scrape`(firecrawl.py:181)与自托管 v1 面同构。
**注:此为源码级佐证,非真跑验证**——真跑(起实例→3-5 站→对照)按档
留主人服务器(AC manual)。

## 来源 4:docs.firecrawl.dev/contributing/self-host(官方文档站,钉 v2.11.162)

<https://docs.firecrawl.dev/contributing/self-host>

- 就绪探针:`GET /v0/health/readiness` → `{"status":"ok"}`;真验证示例
  `POST /v2/scrape` body `{"url": "https://example.com", "formats":
  ["markdown"], "timeout": 60000}`。
- `.env` 面:与来源 1 一致外加 PostgreSQL 凭据(建议 ≥32 随机字符、
  `POSTGRES_DB=postgres` 保持);`REDIS_URL` 不应覆写(compose 网内自解析)。
- cloud-only/栈外能力清单(原意转述):截图与页面操作类格式默认栈不可用
  (依赖 Fire-engine);LLM 抽取自带 OpenAI 兼容提供方或 Ollama;agent /
  browser / interact / 专用格式为云端或需外部服务;默认栈不含持久化存储、
  TLS、HA、鉴权——"not a production architecture"(正式部署需自行加固)。

## cloud-only 缺口清单(汇总,如实入文档不美化)

1. **Fire-engine 全家**:IP 封禁处理/机器人检测对抗等强反爬绕过;截图、
   页面操作(interact)类格式——默认自托管栈均不可用。
2. **LLM 结构化抽取(/extract、JSON 格式)**:需自带 OpenAI 兼容端点
   (或 Ollama),不自带即缺。
3. **agent / browser / 深研等新品类端点**:云端功能。
4. **运维面**:默认栈无鉴权无 TLS(`USE_DB_AUTHENTICATION=false` 前提),
   公网部署须自行加固(反代+强凭据+换 BULL_AUTH_KEY)。
5. 基础 scrape(Fetch + Playwright 渲染 → markdown/html)= 栈内能力,
   即 MYIA L3 兜底所需面(MYIA 引擎只消费 markdown/html 两种格式,
   firecrawl.py:114-126)。

## AGPL 边界(同 RSSHub 判例)

上游 server AGPL-3.0 / SDK MIT。MYIA 以 HTTP API 服务消费接入(零源码
复制、零 SDK 依赖——engines/firecrawl.py 纯 httpx 实现),合规面同
RSSHub 插件先例(plugins/myssia-rsshub/README.md:5-6「上游 AGPL-3.0,
只以 manifest+文档引用接入,零源码复制」);红线=不可 vendor 其 server
代码进本仓库(MIT)。
