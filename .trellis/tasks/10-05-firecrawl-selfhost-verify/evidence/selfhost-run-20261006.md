# 自托管 Firecrawl 真跑成功实录(2026-10-06 11:57-13:35,CN 镜像前缀路线)

上轮(build-timeout-20261006.md)以 docker hub 拉层 ~50KB/s 超时告终;本轮按
「镜像前缀拉取 + docker tag 回原名」路线(不动 daemon/colima 配置)完成起栈
并真跑 AC1/AC2 全绿。全部命令亲跑,原始输出见同目录配套文件。

## ① 镜像前缀实测(吞吐留数)

- 前缀可达性:`docker manifest inspect` 三前缀全通
  (docker.1ms.run / docker.m.daocloud.io / dockerproxy.net,各 5001B 多架构清单)。
  **首个实测可用前缀 = `docker.1ms.run`**(manifest 与真拉双证)。
- `docker pull docker.1ms.run/library/postgres:17`:**166MB(content)/5s ≈ 33MB/s**
  (6 层全新,0 层 Already exists;日志 pull-1ms-postgres 段)——对比上轮直连
  docker hub 同类层 ~50KB/s,**提速约 600 倍量级**。
- `docker.1ms.run/library/golang:1.24`:首拉 759s 未完(12:15 colima VM 被并行
  searxng 线 `colima stop` 连带停机——host agent 日志 SIGINT 优雅停机实锤,非崩
  溃;已提交层保留);VM 复起后续拉 **17s 完**(content 327MB,复用已提交层)。
- tag 回原名:`docker tag docker.1ms.run/library/postgres:17 postgres:17`、
  `docker tag docker.1ms.run/library/golang:1.24 golang:1.24`(compose 构建面
  零感知)。其余基镜像(node:22-slim/redis:alpine/rabbitmq:3-management/
  foundationdb:7.3.63)上轮缓存直接复用。
- 配套文件:`env-mirror-fakeip-evidence-20261006.txt`(前缀探针+双镜像拉取
  日志+content size 全录)。

## ② 起栈(45 分钟时间盒内完成,过程有曲折如实记)

- 12:19 `docker compose up -d --build` 首发(api 构建至 Step 14/41 挂:容器内
  curl github.com:443 TLS `SSL_ERROR_SYSCALL`——宿主机同 URL 200/3.9s 正常,
  VM 侧瞬断,重试即过);
- 复跑过 Step 14 后挂 Step 20/41:`--mount=type=cache` 需 BuildKit,而本机
  docker CLI 无 buildx 插件(`docker buildx version`=unknown command),
  compose 5.6.0 固走 classic builder(镜像标签 com.docker.compose.image.builder=classic
  实证);`DOCKER_BUILDKIT=1` 对 compose 无效。
- **/tmp 克隆内外科修两处(零仓库改动,如实记)**:
  1. `apps/api/Dockerfile` Step 20 剥除三个 `--mount=type=cache`(缓存挂载仅
     加速重复构建,单发非必需)——classic builder 续跑 Step 1-19 缓存;
  2. 同步加 `--fetch-timeout 600000 --fetch-retries 5 --network-concurrency 4`
     (npm CDN 中途降速 ~20-40KB/s,首轮 721/780 包 pnpm 自身超时中止;
     耐心参数轮 780/780 全过)。
- 13:23 exit=0:六容器全 Up(api 3002 映射、nuq-postgres/rabbitmq healthy),
  **就绪探针 `curl http://127.0.0.1:3002/v0/health/readiness` → `{"status":"ok"}`
  首探即 200**。构建日志 /tmp/firecrawl-e2e.build{2..6}.log(exit 文件法全程)。
- 时间盒口径:12:19 起 45 分钟=13:04;13:03 检查点 pnpm 744/780 且推进中,
  掐掉重启=零缓存挂载下全量重下更劣,仿上轮「延长一轮」先例延至 13:25 硬顶,
  实际 13:23 完成。延展决策如本段所记,不美化。

## ③ fake-ip DNS 环境 vs SSRF 守卫(本轮最大发现,环境产物非上游缺陷)

- 起栈后首跑全站 500:api 侧 pdf/document 引擎 `Connection violated security
  rules.`(safeFetch.js:127),playwright-service 直打同拒:`Blocked insecure
  target URL ... resolves to a private/internal address`(pageStatusCode 403)。
- 根因:宿主 clash 类代理 fake-ip 模式在 TUN 层劫持**所有** UDP 53——VM
  resolv.conf 本就是公网 DNS(114.114.114.114/223.5.5.5),容器内强制
  `--dns 223.5.5.5` 仍解析出 198.18.x.x fake-ip;firecrawl 双守卫(api
  safeFetch + playwright-service)按 RFC 保留段 198.18.0.0/15 判内网拒连。
  构建期无守卫(curl/apt/pnpm 直连 fake-ip 经宿主 TUN 代理出网)故全程无碍。
- **解法(仅 /tmp 克隆内,零 daemon 配置改动)**:宿主经 alidns DoH
  (`https://223.5.5.5/resolve`,HTTPS 不可被 fake-ip 劫持)取四站真实 IP,
  compose 给 api+playwright-service 加 `extra_hosts` 钉真 IP 绕过 DNS;
  `docker compose up -d --force-recreate api playwright-service` 后同请求
  pageStatusCode 200 全文(前后对照原文在 env-mirror-fakeip-evidence 文件)。
- **部署指引含义**:主人服务器无 fake-ip 环境则无此坑;有 clash fake-ip 的
  机器按上法加 extra_hosts 即可(已补进 zero-cost §4 注记)。

## ④ AC1 真跑(既有 FirecrawlEngine,零代码改动)

- 命令:`MYIA_FIRECRAWL_URL=http://127.0.0.1:3002 uv run --no-sync myssia test
  /tmp/firecrawl-e2e-category.yaml --json`(品类 YAML=上轮备好的四站档,
  `engine_options.firecrawl.endpoint: env:MYIA_FIRECRAWL_URL` 调用时解析,
  引擎日志掩码形态 `endpoint=env:MYIA_FIRECRAWL_URL` 合约亲证)。
- 结果:**四源全 ok=true、各 1 条、标题与正文齐**(JSON 落
  scrape-samples/ac1-engine-run-myssia-test.json;CLI 预览截断 201 字符是
  myssia test 展示层行为,非引擎截断——直连 API 应答全文为证)。
- 直连 `POST /v1/scrape`(formats markdown+html)五站全长样本:
  | 站 | markdown | html | 关键判定 |
  |---|---|---|---|
  | example.com(静态对照) | 958 字符 | — | 全文完整 |
  | quotes.toscrape.com/js(JS 重站) | 1574 | 3710 | **JS 渲染内容实锤在**:"The world as we have created it … by Albert Einstein"+Marilyn Monroe 引文在 md 与 html 双证(raw HTML 无引文,AC2 对照证) |
  | news.ycombinator.com | 18285 | 40113 | 首页条目表全量 |
  | techcrunch.com/category/artificial-intelligence | 20709 | 145135 | 文章卡片全量(列表亦 JS 渲染,见 AC2) |
  样本文件 scrape-samples/scrape-direct-*.json 四份。

## ⑤ AC2 质量对照(基线=static_html+trafilatura,**非 Zenrows**)

- Zenrows 侧:上轮已证本机凭据缺位(env 无 ZENROWS*、~/.myia/gates.yaml 不存
  在→saas.zenrows 门槛未开),vs Zenrows 对照仍留主人;本轮对照侧按放行口径
  改 **static_html+trafilatura 基线**(源级 `engine_options.static_html.
  extract_fallback: true` 显式开兜底,`myssia test` 四源真跑 + 引擎同款
  `_trafilatura_fallback` 助手全长复算,双口径一致)。
- 对照表(markdown 字符数):
  | 站 | 自托管 firecrawl | static_html+trafilatura | 差异解读 |
  |---|---|---|---|
  | quotes.toscrape.com/js | 1574(引文+作者+标签) | **0 条**(raw HTML 壳) | JS 渲染缺口正是 firecrawl 补位;HN 式静态站两者皆可 |
  | example.com | 958 | 156(仅正文段) | firecrawl 保留标题/链接/多语言全文 |
  | news.ycombinator.com | 18285(表格+链接) | 4101(扁平文本) | 链接结构与条目表完整度差 4.5 倍 |
  | techcrunch.com/category/artificial-intelligence | 20709(文章卡片) | 305(仅栏目简介) | 列表卡片 JS 渲染,基线拿不到 |
- 附:免费链真降级口径下(static 零结果自动升 L3)js-heavy-quotes/tc-ai 被
  本机 crawl4ai 接住也能出文(首跑 ac2 引擎记 crawl4ai),即 MYIA 自有 L3
  与自托管 firecrawl 在 JS 站功能等位,firecrawl 的增量=不占本机浏览器
  资源+独立扩缩容。
- cloud-only 缺口面(与上档结论一致,本轮未新增暴露):栈内基础 scrape
  (Fetch+Playwright→markdown/html)恰好覆盖引擎所需两格式;Fire-engine/
  截图/页面操作/LLM 抽取端点/agent-browser-interact 云端专属;默认栈无鉴权
  无 TLS。**API 兼容零缺口**:`/v1/scrape` 全参数(formats/timeout)真跑
  通过,`success:false` 时 error 码结构亦亲证(SCRAPE_ALL_ENGINES_FAILED
  样例在修 extra_hosts 前实录),无需另立适配档。
- 配套文件:scrape-samples/ac2-baseline-static-html-trafilatura.json(链跑)+
  ac2-baseline-full-lengths.json(全长复算)。

## ⑥ 收尾状态

- 起栈产物:六容器(本流专属,与 searxng 档容器无交叠);镜像 firecrawl-api/
  playwright-service/nuq-postgres 本地建成 + 基镜像全家(约 5.2GB)留存。
- /tmp/firecrawl-e2e 克隆含三处 /tmp 内修(Dockerfile 两处+compose extra_hosts,
  均带注释与日期);.env 仍为官方三行模板。复验同法可直接 `docker compose
  up -d`(镜像已建成,秒级)。
