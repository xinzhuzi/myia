# docker 解锁后首次真跑尝试:build 网络超时实录(2026-10-06 00:56-01:44)

背景:基线(2026-10-05 深夜二)A 项 docker 解锁由前序步骤完成——本轮
00:56 亲验:`docker info` 通过(Client 29.8.2 / Server 29.5.2,context
colima,compose 5.6.0),`colima status` = running(macOS
Virtualization.Framework,aarch64)。前置满足,blocked 分支的 docker 前提
已解除,按 prd 复验口径起栈真跑。

## 起栈命令(与 docs/zh/zero-cost.md §4 模板逐字一致——本尝试同时验证该模板)

```
git clone --depth 1 https://github.com/firecrawl/firecrawl.git /tmp/firecrawl-e2e
cat > /tmp/firecrawl-e2e/.env <<'EOF'
PORT=3002
HOST=0.0.0.0
USE_DB_AUTHENTICATION=false
EOF
cd /tmp/firecrawl-e2e && docker compose up -d --build   # 后台 + exit 文件法
```

上游漂移核对(取证快照 10-05 → 本轮 clone 实物):
- SELF_HOST.md 已无「===== Required ENVS =====」段,但 `USE_DB_AUTHENTICATION=false`
  仍是明示必设项(SELF_HOST.md:25);根 `.env` 只覆写 compose 引用的变量
  (SELF_HOST.md:40);仅 API 发布 host 3002(SELF_HOST.md:47)。三行模板
  仍然有效(compose 内 `USE_DB_AUTHENTICATION: ${USE_DB_AUTHENTICATION:-false}`
  引用实核,docker-compose.yaml:33)。
- 上游 compose 新含 SEARXNG_ENDPOINT/SEARXNG_ENGINES/SEARXNG_CATEGORIES
  变量引用(docker-compose.yaml:55-57)——缺省空串仅 warning,不拦起栈。

## 时间线(全部亲跑亲录)

| 时刻 | 实况 |
|---|---|
| 00:58:51 | `docker compose up -d --build` 后台起(build.start 时间戳) |
| ~01:08 | 拉层中,各层 1-4MB 进度;redis(valkey 66.5MB)已完整 |
| ~01:18 | rabbitmq:3-management(408MB)、redis:alpine(160MB)已完整;最大层 97.52MB 下载中 |
| 01:26 | 多层 Download complete;剩 b9bd31abcf11 层 72.35/112.9MB |
| 01:33 | 同层 95.42/112.9MB(≈7 分钟 23MB ≈ 55KB/s 级) |
| 01:40 | 时间盒 20+20 已满 + 3 分钟缓冲尽;停(见下) |
| 01:44:04 | TaskStop 终止 build 任务;elapsed = 45 分钟 |

拉取成果(停时 `docker images` 亲录):117 层 Download/Pull complete;
node:22-slim 349MB、redis:alpine 160MB、rabbitmq:3-management 408MB、
foundationdb:7.3.63 1.53GB 均完整;playwright-service 浏览器层未完
(112.9MB 层 95.42MB);**api 镜像本地 build(npm ci 等)未及开始**。

## 降级决策(按计划口径执行)

- 时间盒:首盒 20 分钟 → 按降级路径延长一轮(至多再 20 分钟)→ 再给
  3 分钟收尾缓冲,共 45 分钟仍未出 exit 文件 → 判「仍不成」。
- 网络实测:docker hub 大层 ~50KB/s 级(见上 01:26→01:33 采样);按此
  速率,剩余拉层 + api 本地 build(npm ci,容器内同网络)预计远超时间
  盒,继续等待无意义。
- 处置:TaskStop 终止;`docker compose down --remove-orphans`(exit=0,
  本流零容器残留;剩余 Up 容器 searxng-core/searxng-valkey 属
  source-searxng 档的栈,不碰);**镜像层缓存与 /tmp/firecrawl-e2e 克隆
  (含 .env 三行)均保留**——colima VM 不删,复验时 `docker compose
  up -d --build` 续用缓存,已拉 2.4GB+ 层不必重下。

## AC 状态影响

- AC1/AC2 真跑仍未发生(无实例即无样本/对照)→ 档维持 blocked,复验
  口径不变(主人服务器或本机网络良好时窗口重试,起栈命令同上,缓存已备)。
- 本轮新增事实:docker 前置已解锁(colima 在跑);瓶颈转为 docker hub
  拉层带宽(本机网络),非环境缺失。zero-cost §4 模板可用性本轮已核至
  「compose 解析+拉层」一步,未及健康探针。
- 站单与 robots 实况(为复验备,全部 curl 亲取 2026-10-06):
  - https://quotes.toscrape.com/js/(JS 重站,官方爬虫练习场)robots.txt
    返回 404 = 无限制;
  - https://example.com/(静态站,IANA 文档域,页面自述许可文档示例用途)
    无 robots 文件;
  - https://news.ycombinator.com/ robots:`User-Agent: *` 段首页 / 允许
    (仅 Disallow 交互路径),Crawl-delay: 30(单次抓取无碍);
  - https://techcrunch.com/category/artificial-intelligence/ robots:
    通用 `*` 段该路径允许(仅挡 /wp-admin/、/search/ 等;特定 AI 爬虫
    UA 段不适用于我方缺省 UA)。
- Zenrows 凭据实查(AC2 前置):shell env 无 ZENROWS*;`~/.myia/gates.yaml`
  不存在(MYIA_HOME 未设)→ saas.zenrows 门槛未开、api_key 引用缺位
  → 本机无 Zenrows 基线可跑,AC2 真跑对照无论实例起否均留主人。
