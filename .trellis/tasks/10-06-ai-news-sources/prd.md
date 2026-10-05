# PRD:AI 资讯源扩容——厂商官方源 + 官网变更监控 + X 监控

> 立档:2026-10-06 · 来源:主人 gap 点名(「AI资讯里面,各大AI厂商监控,官网监控,X 上面的监控,你好像没有做啊」)
> 类型:源扩容,单档三 scope(各自独立可验) · 状态:planning,探查与接线待 start 后做

## 证据矩阵:主人点名三块,一块都没做(2026-10-06 亲核)

| # | 主人点名 | 现状(证据) | 缺口量级 |
|---|---------|-----------|---------|
| S1 | 各大AI厂商监控 | `plugins/ai-news.yaml` 活源仅 2:aihot.news(聚合器热榜,engine auto)+ cocoloop(Discourse 论坛);另两源注释态=linuxdo(登录墙占位)/reddit-ml(官方引擎已备,等主人 2026-10-31 前注册凭据)。OpenAI/Anthropic/DeepMind/Meta/xAI/Mistral/Qwen/DeepSeek/智谱/月之暗面/MiniMax 等厂商官方博客/新闻页**零源配置** | YAML 加源 + 逐源探查判例(honest UA 200/robots/出口可达——Bing RSS 本出口 302 墙判例在案,出口风险逐源记) |
| S2 | 官网监控(无 RSS 页面变更) | `plugins/myssia-urlwatch` 件已交付(desktop tier;`adapter.run(urls)` 快照对比,new/changed/unchanged/error 事件 + unified diff;cache 落 `~/.myia/urlwatch/cache.db` 跨 run 持久)——但**全仓零消费方**:引擎注册表 `src/myssia/engines/registry.py:107-126` 共 11 引擎无 monitor 形态;analysis_lane 是 enrich 平行位的装饰器通道(情感/关键词),不是采集通道,urlwatch 只是错误码词表被其借用 | urlwatch → 品类管线挂点(设计两案,下 §S2)+ ai-news 挂示范 watch 源 |
| S3 | X(Twitter)上面的监控 | 全仓无 X 通道(rg twitter/nitter 仅 theHarvester vendor 与 push/discord 无关命中)。正路 = `plugins/myssia-rsshub`(remote tier,RSSHub 封装,compose 在 `docker/plugins/myssia-rsshub/`):RSSHub 有 twitter 路由——但 ① 本机 Docker.app 已卸载(10-05-source-searxng research §0 逐项探查在案,同款受阻)② twitter 路由凭据现行要求待探查核实(X guest 访问已死,RSSHub 路由大概率要 auth token,凭据=主人决策)③ 官方 X API v2 读取=付费层,默认不走 | 通道决策 + 部署 + 凭据,主人侧前置为主 |

## 既有相邻事实(引用即已核,勿重复探查)

- RSS 通道判例:`plugins/news.yaml` gcores(`engine: static_html` + `extract.type: rss`,feedparser 条目映射;static_html 的 CSS 选择器硬接 RSS 会静默零产出——RSS 站必须走 rss 类型)
- Reddit 官方引擎:`10-05-reddit-official-engine` 已归档,ai-news.yaml 注释态待凭据;评估档 `10-05-reddit-source`(review)有 owner_left 决策五项
- 死路册(v12-backlog prd:205-208):GNews RSS(robots 禁)/Bing RSS(本出口 302 墙)/smzdm(反爬)/Reddit 直抓(robots 全禁)
- RSSHub AGPL 服务消费零代码复用判例(myssia-rsshub manifest;searxng 档沿用)
- changedetection.io = 弱需求备忘(urlwatch 覆盖大半,v12-backlog prd:202),本档不重启
- urlwatch 上游语义:**首次跑全部 new**(cache 冷启动),之后才有 changed 判定——S2 的 digest 语义必须适配,否则首日刷屏

## 三块方案倾向(planning 草案,grill 可翻)

### S1 厂商官方源(RSS 直连优先)

- 探查清单草案(17 家,主人可增删):OpenAI / Anthropic / Google DeepMind / Google Research / Meta AI / Microsoft Research / xAI / Mistral / Cohere / Hugging Face(blog + daily papers)/ Qwen / DeepSeek / 智谱 / 月之暗面 / MiniMax / 字节 Seed
- 每源走 news-probe 判例(单次零压力 + 先 robots + honest UA + 证据落 `evidence/`):有官方 RSS → 直用 rss 通道进 ai-news.yaml;无 RSS 的页面 → 归 S2(urlwatch)或 S3(RSSHub 路由),不硬抓
- schedule 复用 ai-news 既有 8/20 双槽;dedup `{url}` 语义照旧

### S2 官网变更监控(urlwatch 接线,实现件)

- 挂点两案,start 前 grill 定:
  - a) 新提取类型 `extract.type: watch`:static_html 收文本 → urlwatch 快照比对 → changed/new 事件产条目(diff 摘要进 content)
  - b) 链外引擎 `engine: urlwatch`(同 credhunter/reddit 先例,显式 engine 才生效)
- 关键语义:首次全 new 的冷启动适配(首跑只建快照不产条目,或首跑条目全量归 digest 不 immediate);零变更=合法空态(上游已钉)
- ai-news 示范挂 1-2 个无 RSS 官网页(如 xAI news、某厂商 changelog/pricing 页,探查后定)
- 「装不上不拦核心」铁律沿用:uv 缺失只降级源级结构化失败,不炸品类

### S3 X 监控(RSSHub twitter 路由)

- 前置一:自部署 RSSHub(docker compose 在库)——本机 Docker 已卸载,主人装回 Docker Desktop 或指自有服务器;探查段可先文档取证(同 searxng 草案法)
- 前置二:twitter 路由凭据形态探查(RSSHub 现行要求 auth token 与否)——凭据申请=主人,不代申请
- 候补:官方 X API v2(付费层,额度现值探查)——默认不走,除非主人点名
- 账号清单草案:厂商官号(OpenAI/Anthropic/DeepMind/xAI/…)+ 关键研究者,主人圈选后配

## 主人决策点(预置,如实停)

1. S1 厂商清单增删(草案 17 家)
2. S2 挂点两案选型(grill 后带推荐)
3. S3 通道裁决:自部署 RSSHub(装 Docker?)vs X API 付费 vs 暂缓;凭据申请属主人
4. X 账号监控清单圈选

## 验收标准(AC)

- [x] AC1:S1 探查表落 `research.md`(§1:七家 200 RSS+robots 对照逐家记录;§2 watch 页探查;证据 `evidence/probe{,2,3}-log.md` + `probe4-*.json`),可用源进 `plugins/ai-news.yaml`(七家 RSS),`--dry-run` 全链冒烟回执落 evidence(回执注记见 §0:round1 sniff 工具故障销号)。
- [x] AC2:S2 挂点实现 + 测试(`tests/engines/test_urlwatch_engine.py` 30 例全 mock 零网络,含首跑冷启动 announce_new=false 钉死、去重锚点指纹两性[同 diff 同锚/异 diff 异锚]、unchanged 合法空态、robots 面、adapter 错误码三态);ai-news 挂三家 watch 源(Anthropic/Meta/Cohere)。
- [x] AC3:S3 通道探查落 `research.md` §3(TWITTER_AUTH_TOKEN 实锤=zread 官方环境变量表;twitter 路由脆弱性官方文档在案;X API 付费层不走),YAML 注释态入位启用三步+候选账号八号;不部署不代申请。
- [x] AC4:涉网探查全走单次+先 robots+honest UA+证据落 `evidence/`(四轮脚本+回执全在档;round1 工具故障与 round2 重取证翻案记档 §0)。
- [ ] AC5:门禁全量绿(pytest 4377/0+vitest 516/0+tsc 0 错+build ✓ 已亲验;装机包刷新=判例处理中)。

## 涉网纪律(全程硬约束)

单次(每目标 URL 一次,不重试)、先查目标域 robots.txt 并记档、honest UA、零压力、全部证据落 `evidence/`。
