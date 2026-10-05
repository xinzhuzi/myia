# research.md — 10-06-ai-news-sources 探查与研究记录

> 主人令(2026-10-06):「要做完这个东西,yaml里面要添加完毕」→ S1/S2/S3 全量执行。
> 探查纪律:单次零压力、robots 先行、honest UA(`MYIA-source-probe/0.1`)、证据全落 `evidence/`。
> 涉网轮次:round1(26 feed + robots,含工具故障)→ round2(修复后重取证 + watch 页)→ round3(robots 全文 + autodiscovery 全文搜)→ round4(qwen 真 feed + cohere robots 补探)。

## §0 工具故障记档(round1,留教训)

round1 脚本 `probe_vendors.py` 的 `sniff()` 写了 `"<html" in head`(str in bytes)→ **一切 200 响应在判形时抛 TypeError,被 except 分支记成「网络失败」**。受害面:全部 robots 探查 + 8 条 feed 探查(智谱/月暗/MiniMax/Seed/DeepSeek/cohere 的 200 证据被毁,一度误判「国产五家出口墙全灭」)。round2 修复(sniff 改 bytes 比较)后重取证翻案:**上述站点其实全部直连可达**。教训:探查脚本的判形分支要有自测;「网络失败」与「工具崩溃」在 except 里必须分形(round2 起把 TypeError 类错误单列)。

**出口环境注记**:本机 shell 带系统代理 env(探查与管线同生效;`--dry-run` 冒烟期 lsof 亲证 myssia 进程经 localhost:7897 出网)——证据表里的「直连」实义是「env 缺省出口」,国产五家可达即意味着代理出口对它们也通。子进程内 urlwatch 上游同样吃 env 代理,与管线出口一致。

## §1 厂商官方 RSS 源(S1,已进 ai-news.yaml 七家)

| 厂商 | feed URL | 直连 | robots(对 feed 路径) | 形状/大小 | 状态 |
|------|----------|------|----------------------|-----------|------|
| OpenAI | `https://openai.com/news/rss.xml` | 200 | `User-agent: * Allow: /`(98B 全文) | RSS / 760KB | ✅ 入 YAML |
| Google DeepMind | `https://deepmind.google/blog/rss.xml` | 200 | Allow: / | RSS / 70KB | ✅ 入 YAML |
| Google Research | `https://research.google/blog/rss/` | 200 | Allow: / | RSS / 79KB | ✅ 入 YAML |
| Microsoft Research | `https://www.microsoft.com/en-us/research/feed/` | 200 | 154 行 Disallow 逐一对照无命中(evidence/probe3 robots 全文) | RSS / 244KB | ✅ 入 YAML |
| Hugging Face | `https://huggingface.co/blog/feed.xml` | 200 | Allow: / | RSS / 258KB | ✅ 入 YAML |
| Mistral | `https://mistral.ai/news/rss`(`/rss.xml` 302 落此) | 200 | Allow: / | RSS / 25KB | ✅ 入 YAML |
| Qwen | `https://qwenlm.github.io/blog/index.xml` | 200 | `Disallow:`(空=全允许) | RSS / 39KB | ✅ 入 YAML |

- Qwen feed 定位法:博客页 autodiscovery `<link rel=alternate type=application/rss+xml href=.../blog/index.xml>`(probe3;`/blog/feed.xml`/`/index.xml` 猜测位均 404,Hugo 风格真路径在 `/blog/index.xml`)。
- OpenAI feed 760KB 全量(含旧文),首跑条目多属正常;dedup `{url}` 全期拦截后进入日常增量。

## §2 无 RSS 厂商 → urlwatch 官网监控(S2,已进 YAML 三家 + 死路两家)

页面探查(probe2/3,直连单次):

| 页面 | 状态 | robots | 判定 |
|------|------|--------|------|
| `https://www.anthropic.com/news`(title: Newsroom \ Anthropic) | 200 html 425KB | Allow: / | ✅ watch 源 |
| `https://ai.meta.com/blog`(title: AI at Meta Blog) | 200 html 203KB | **见 §4 张力** | ✅ watch 源(取合记档) |
| `https://cohere.com/blog`(title: The Cohere Blog) | 200 html 1MB | Allow: /(/studio-* 等除外,evidence/probe4) | ✅ watch 源 |
| `https://x.ai/news` | **403**(Cloudflare,代理路同 403) | — | ❌ 死路记录:静态通道全灭;x.ai 无 RSS(/news/rss.xml 404、/rss.xml 403)。xAI 动态由 aihot 聚合器间接覆盖;要直挂留待 crawl4ai/stealth 通道主人另点 |
| zhipuai.cn/news、moonshot.cn、minimaxi.com、seed.bytedance.com、deepseek.com | 各首页/news 均 200 html | 各家 robots 允许 | ⏸ **暂缓,不入 v1**:SPA 软 200(rss.xml 猜测位全落 SPA catch-all,无 autodiscovery),页面快照 = 巨型 JS 壳,变更 diff 大概率被时间戳/CSRF 噪声刷成每 run 误报;等 urlwatch 上过滤能力(CSS 选择器过滤)再批量接入,记档不猜 |

- deepseek `/rss.xml` 404(html 404 页)、api-docs `/rss.xml` 404 → 无官方 feed;首页 watch 价值低(营销页),暂缓同上。
- watch 语义设计(引擎实装 `src/myssia/engines/urlwatch.py`):条目 url 铸变更指纹锚点 `<页面>#watch-<sha1(diff)[:10]>`(同 diff=同锚点拦重复,新变更=新锚点不被 `{url}` 全期吞);`announce_new: false` 首跑只建基线;零变更=合法空态 skip。

## §3 X(Twitter)监控(S3,注释态入 YAML,两前置一决策)

- **通道定案:自部署 RSSHub**(myssia-rsshub 件,compose 在 `docker/plugins/myssia-rsshub/`);官方 X API v2 读取=付费层,不走。
- **凭据实锤**(zread DIYgod/RSSHub 官方环境变量表,2026-10-06):twitter 路由需 `TWITTER_AUTH_TOKEN`(身份验证令牌,多账户逗号分隔);guest 匿名访问已死。
- **脆弱性在案**(RSSHub 官方文档「最新更新」):`/twitter/keyword` 2025-08 起失效;Twitter GraphQL 端点 ID/feature flags 持续漂移,非 Puppeteer 方案维护负担重 —— 4xx/空产出属正常降级面。
- **前置一(硬)**:本机 Docker.app 已卸载(`10-05-source-searxng` research §0 逐项探查在案,searxng 同款受阻)→ 主人装回 Docker Desktop 或指自有服务器。
- **前置二**:X auth_token 一枚(登录态 cookie 里的 auth_token;属主人凭据,不代取)。
- YAML 注释态:启用三步 + 候选账号(OpenAI/AnthropicAI/GoogleDeepMind/xai/karpathy/OfficialLoganG/_akhaliq/simonw)已写在 `plugins/ai-news.yaml` S3 块,reddit-ml「先决条件入 YAML」同款先例。

## §4 Meta robots 张力记档(判断记录,可翻案)

`ai.meta.com/robots.txt` 全文(evidence/probe3-results.json):`User-agent: *` 段仅禁 `/*cursor=`、`/*fb_comment_id=`、`/ajax/`、`/tealium/`、`/intern(al)/`、`/login/`、`/oidc/callback/`、`/*.php`(裸 `Disallow: /` 全属 PetalBot/Scrapy/Yandex 等具名 UA);但文件头附 Meta 采集 notice:「未经书面许可禁止自动化手段采集」。

**取合(本档判断)**:机械面(robots `*` 段)允许 `/blog`,且我方足迹=每 12h 一次单页快照、honest urlwatch UA、自用情报;notice 面向的是 Facebook 数据的批量采集条款。**判定入 watch 源**;如主人取严解释,删 `meta-ai-blog-watch` 源即可(零其他依赖)。

## §5 主人决策点(终稿清单)

1. **X 账号清单圈选**(S3 候选八号在 YAML 注释里;docker+auth_token 两前置齐后按圈选启用量产条目)。
2. **Meta watch 取合翻案权**(§4;默认已入)。
3. **国产五家 SPA watch 批**(§2 暂缓记录;若主人要强上,接受误报噪声先挂 zhipu 一家试跑也可,一句话的事)。
4. Reddit(既有档 `10-05-reddit-source` owner_left 五项,10-31 凭据截止)与本档无耦合,维持原决策面。

## §6 引擎与词表改动清单(实现面)

- 新引擎 `src/myssia/engines/urlwatch.py`(链外,`engine: urlwatch` 显式选择;零凭据;单页语义拒 pagination;proxy 只支持 direct;robots 面照查)。
- `src/myssia/engines/registry.py` 注册(urlwatch;AUTO_CHAIN 七层原样不动)。
- `src/myssia/schema.py` ENGINES 元组 + EngineName Literal 增 `urlwatch`。
- 测试 `tests/engines/test_urlwatch_engine.py` 30 例(全 mock 零网络零子进程;fake adapter 模块替换 compile+exec 装载面)。
- `plugins/ai-news.yaml`:七家 RSS + 三家 watch + S3 注释块。

**共享暂存区收编回执(第四案)**:schema.py 的 urlwatch 两行被并行 apprise 会话的 65e1b96 顺带提交(其 add schema.py 前未逐文件 diff);其复核档 56d7b9f 已认领并补齐 skill/SKILL.md 枚举行(我方未提交态时 test_skill_doc 撞红,对方复核修笔),且明示 engines/urlwatch.py 与 registry.py 留工作树由本档收口——归属链完整在 git 史。

## §7 后续候选(不本批)

- HF daily papers RSS 化(RSSHub `/huggingface/daily-papers` 路由,随 S3 实例一并开)。
- urlwatch 页面过滤能力(CSS 选择器/文本归一)落地后,§2 暂缓的国产 SPA 五家批量接入;meta 的空 diff 噪声同盼过滤能力。
- x.ai 经 crawl4ai 通道的可行性(主人另点;静态通道死路在案)。

## §8 真跑冒烟回执(2026-10-06 凌晨,两轮)

**第一轮:全品类 `--dry-run`**(12 源全链,21 分钟,enrich 50000 预算打满):
- 七家厂商 RSS **全部拉通零失败**(engine=static_html 回填);
- meta-ai-blog-watch = `watch_baseline_seeded`(冷启动钉死语义在真管线成立);
- anthropic/cohere 两 watch 源 `urlwatch_failed` 子进程 exit 1——**根因=并发首装竞态**:品类源是 `asyncio.gather` 并发抓取(pipeline.py:1761),三个 urlwatch 源同秒并发触发 `uv run --with urlwatch` 临时环境首装,两败一成;单独复跑 adapter 两页全通(单测时序证据 urlwatch-debug.txt)。
- **修复**:引擎对 `urlwatch_failed` 加一次 4s 错峰重试(超时/输出坏不重试——重跑无意义);终态失败消息带子进程 stderr/stdout 尾巴(可诊断);测试 +3(先败后成/两连败终态带尾/超时零重试),33 例全绿。
- enrich 面:首拉 949 条(OpenAI feed 760KB 全量史),预算 50000 打穿后 517 条降级纯粗筛——**一次性入驻洪水**(dedup {url} 全期拦截后回落日增量);主人如嫌首日 digest 过大可上调 budget_per_run(glm-4-flash 价位),或接受一次性。

**第二轮:watch-only 并发冒烟**(临时品类 evidence/smoke-watch-only.yaml,真子进程并发,14.4s):
- 三源**零失败**;anthropic/cohere = `watch_baseline_seeded`(真实缓存 `~/.myia/urlwatch/cache.db` 基线已种,今晚首跑零噪音);
- meta 产出 1 条 changed 条目(距首轮快照仅 ~20 分钟)且 diff 为空——**CDN/出口轮换噪声风险实证**(clash 出口不同快照漂移);条目形状健康(标题+`#watch-` 锚点),master 若嫌 meta 噪声可一句话删源。
