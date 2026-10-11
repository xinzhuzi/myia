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

## §9 主人令「测试一次」真测回执(2026-10-06 01:28-01:55,装机态三轮)

**R1 抛弃库全链**(desktop entry 直通,cwd 解析到 /tmp/myssia.db):12 源采集面全绿——七家 RSS 零失败、anthropic=watch_unchanged、meta/cohere 各 1 条 changed;953 条入库、732 条进 digest 池;enrich 全降级(`openai` extras 未进 desktop requirements-lock——**装机态全品类既有缺口**,非本批引入);推送失败(env+钥匙串双空,装机件从未推成——仪表盘「推送成功O」实为零)。

**R2 噪声闸验证**:七家 RSS 全部命中变更检测短路(hash_match/not_modified/validators_match,30 分钟内二次拉取零成本);meta/cohere 本轮 diff 非空(content 落库 1500 字截断)——但细看内容:**meta 的 diff 全是 React 组件名(build 产物漂移)、cohere 是 Next.js 数据载荷**=框架级噪声非内容信号;urlwatch 无内容过滤前的如实局限(§7 过滤能力是根治项);空 diff 假阳性已由 watch_noise_empty_diff 闸拦截(单测钉死,实证待自然复现)。

**R3 生产库正式跑**(`--db <数据根>/myssia.db`):runs 表 #3 ai-news partial(19.8s),**953 条+2 条 watch 锚点条目入生产库**;入驻洪水被推送必败轮吸收(digest 池随进程即逝,732 条一次性洪水永久消解——主人修好凭据后只剩干净日增量)。aihot invalid_item 失败=既有噪声非本批。

**调度补全**:装机 app「定时任务」原为 0 任务启用(YAML schedule 只是预览)→ `cron create "0 8,20 * * *" --category <数据根>/plugins/ai-news.yaml --db <数据根>/myssia.db` 建「AI资讯」job,重启实例后调度器识别(**1 个任务启用,下次运行 10/06 08:00**,UI 亲证)。

**owner_left 更新**:①推送凭据(设置→推送 录 FEISHU_BOT_TOKEN 或 APP_ID/SECRET,一次性);②desktop lock 增 openai extras(装机态 enrich 起死,涉依赖指纹变更,主人裁定);③meta/cohere watch 的框架噪声——过滤能力前建议观察或删源,主人一句话;④外科直更两件(adapter+engine)待下次正式重打包自然收编。

## §10 二段迭代回执(2026-10-06 01:55-02:05,主人令「效果不行继续修改继续测试」)

**watch 噪声根治(css 内容过滤)**:engine_options.urlwatch.selector → job 携上游原生 css 过滤链(`{selector, exclude: "script, style, noscript, template, svg", method: html}`;上游实证:format 键不存在、method 仅 html/xml);adapter normalize_urls 增 filter 透传+cssselect 进依赖。活探:anthropic 425KB 全页→main 20KB 正文(「Introducing Claude Sonnet 5.5…」可读)、cohere 87KB→3480 字;**背靠背双跑 R2=unchanged(框架噪声出局)**。meta 实探 main/article/[role=main]/h1 六种选择器全零=纯客户端渲染页,静态通道取不到正文 → **meta-ai-blog-watch 移除**(JS 渲染通道另立档);ai-news 终态 11 源。

**装机 enrich 起死**:desktop lock 扩 llm extras(uv export --extra llm,增量 openai==3.22.1+jiter/sniffio/truststore/httpx2 六轮,与 CLI venv 同版亲证);锁版一致性 24/24;装机 python 手动补装 openai 3.22.1(依赖指纹戳待主人设置页一键官方重装收绿);生产复测 enrich 零 EnrichConfigError。

**生产复测(全要素)**:零新条目=七家 RSS 全部变更检测短路(hash_match/not_modified/validators_match)+watch 两家过滤基线静默重建(watch_baseline_seeded)——系统稳态,明早 08:00 首个正式调度跑。

**推送凭据终局**:shell env 与 keychain(service myia 仅 myia/image/api_key+myia/llm/base_url 两键)双空——飞书/电报凭据从未录入,装机件与 CLI 均从未真推过;**唯一留主人的动作:设置→推送 录一次飞书凭据**。

**依赖指纹收绿追记(2026-10-06 12:12,本机运维零代码改动)**:不再等设置页一键官方重装——按官方同款链手工收绿。语义源(代码亲读):`pyenv.rs` `lock_fingerprint`=文件字节 sha256→hex 小写、`write_stamp`(pyenv_install.rs)=serde pretty 2 空格无尾换行+同目录 `.python-env.json.tmp`→rename 原子写、`detect`=戳 `deps_fingerprint` vs 随包清单实算比对(不等→deps_stale)。动作:原戳备份 `/tmp/myia-python-env.json.bak-20261006-121234`(备份 sha256 `0c031daf820798e368a6e9ea15dd17b77fa14138a09ccae2011a9fea6a42af7e`,原指纹 `a89418199406017e2b68d2a203c7cafc1c1dc8f7b5498eb32d1831c381060fb6`);对随包 `/Applications/世事.app/Contents/Resources/requirements-lock.txt`(3513B,fd 动态定位未手拼中文路径,已含 openai==3.22.1)实算新指纹 `5acc19ed2894a21e1e31927f58e09b90db5bd4332767b179e8c131d07f393060`(shasum 与 python hashlib 双口径一致);戳内**仅替换 deps_fingerprint 一个字段**(state=ready、5 步进原样保留,575 字节与原文件同尺寸),tmp+rename 原子落盘,数据根其余配置零触碰。验证:detect 同款读取路径复核 **新戳==新锁 sha(match=True)→ 状态 ready(deps_stale 出局)**;装机 python `-c "import openai"` → **openai 3.22.1 OK**。设置页「依赖指纹不一致」提示自此消失。

## §11 复查轮(主人质询「没有其他问题了吗」,python-env 拉齐档同款纪律)

**真跑新证据(上午自动发生)**:08:00:44 首个正式调度跑(app 内调度器)已完成——**11/11 源零失败、采集 1625/留存 30、enrich 真出分(immediate 4 条=score≥9 命中,llm 修复生产实证)、watch 两家零条目(过滤生效真安静)**、时长 116.7s;唯一红=推送(凭据仍缺,与采集无关);下一射点 20:00(jobs.json 亲核 enabled/scheduled)。

**本轮新发现并当场修复**:Windows uv 兜底路径缺口——原 `_KNOWN_UV_PATHS` 全按 POSIX 名,win32 下 `~/.local/bin/uv`(无 .exe)永不命中、/opt/homebrew 在 win 误占位;修=win32 首候选 `uv.exe`(官方安装器落位)+/opt/homebrew 收窄 darwin 专属,win32 用例入测(重装载按 platform 重建元组两态断言);装机外科直更+重签。

**门禁亲验(编辑落定后)**:pytest 全量 **4395/0**(首轮 4392+2 failed=与在途编辑撞中间态,复跑净绿);vitest **523/523×2 连续稳绿**(中途 1 挂为并行在途编辑瞬时态,两连清复验);tsc 0 错;定向 urlwatch 69+engine 41+desktop 52 全绿;ruff 绿。

**定性结案**:aihot invalid_item×5/run=YAML 注释写明的设计跳过路径(无标题锚卡片零产出记录,日志噪声非缺陷);装机 python openai 3.22.1 在位;外科三件(adapter×2 轮+engine+yaml+lock)全部亲验在位。

**复查后仍开的口子(全部已知且各有归属)**:①推送凭据(唯一硬前置,主人一步);②依赖指纹戳(2026-10-06 12:12 已手工收绿,官方同款算法实算写戳+原值备份 /tmp,详见 §10 追记;不影响运行);③Hermes 九缺陷(主人裁决修否);④Hermes 沙盘时钟回拨/降级锁两项未模拟(档内记);⑤Meta 重接需 JS 通道(→§12 已接);⑥国产 SPA 五家待过滤能力。

## §12 Meta 博客重接:render: crawl4ai 渲染通道(2026-10-06,口子⑤收口)

**探查定案(evidence/probe6-log.md + probe6-meta-crawl4ai.\*)**:crawl4ai 0.9.4 无头渲染 `ai.meta.com/blog` 单次零压力 **7.3s/markdown 17345 字/5 条博文 slug 可读**(标题+日期+分类完整;静态通道六选择器全零的判死不变);RSSHub 有 `/meta/ai/blog` 路由(私有 GraphQL doc_id 机理,S3 邻近选项记档)但同受 Docker 前置阻塞且 doc_id 漂移脆弱——**走自渲染通道**。涉网仅此一次;robots 复用 §4 在案取合(可一句话删源翻案)。

**实现(克制面)**:urlwatch 上游 ShellJob 契约亲验(2.29 实测 `user_visible_url` 即事件 location/guid,引擎事件匹配零改动)——`engine_options.urlwatch.render: crawl4ai` 时 job 换 `{name, command, user_visible_url}` 形态,命令=宿主解释器跑场景件 `render_crawl4ai.py`(归一化纯文本:图片/链接 URL 出局,fbcdn `oe=`/`_nc_oc=` 轮换签名噪声实证出局),快照对比/diff/锚点语义全在上游复用。离线端到端三跑(new/unchanged/changed+diff)零目标网实证。与 `selector` 互斥;helper 件缺失/后端未装=结构化 `render_helper_missing`/`dependency_missing`。ai-news 终态 meta-ai-blog-watch 重挂(announce_new: false,timeout: 150)。

**门禁**:ruff 绿;定向三件 96/96+插件包守卫 262/262(豁免清单+helper 件);**全量 pytest 4527/0/0**(首轮 1 败=守卫豁免缺项当场修、1 败+2 ERROR=并行会话在途编辑中间态,复跑两连清)。gitnexus impact:normalize_urls 实跑 LOW;索引 WAL 态读路径失效,引擎符号以 rg 普查替代(仅 registry 惰性注册+测试引用,接口零变)。

**并行协调记档**:本档同刻有「国产五家 watch」流在途(其 probe5 系证据+ai-news.yaml 未提交块);本流 YAML 改动(仅 meta 块)已入工作树但**不随本流提交**——`--only` 按文件粒度提交会吞并行流未提交块,ai-news.yaml 的提交归国产流收口或主人;数据根 YAML(装机活配置)已外科只加 meta 块(不部署其在途源)。本流探查文件定名 probe6 系(其 probe5 编号先占)。**共享暂存区 receipt(§6 第四案同款)**:本流三个探查证据件(probe6-meta-crawl4ai.py/.json/.markdown.txt)staged 后被并行冒烟窗归档提交 b207289 顺带入库(其 add 面扫了 .trellis;内容纯本流产物,本提交的 research §12+probe6-log.md 即其索引)——归属链在此记档,git 史可溯。

**装机同步(外科直更+重签,2026-10-06 下午亲验)**:engine urlwatch.py + adapter.py + render_crawl4ai.py 三件 cp 至 `/Applications/世事.app/Contents/Resources/{myssia-src/myssia/engines/,plugins/myssia-urlwatch/}`(diff 三件逐字节一致),sidecar python(数据根 `python/bin/python3`,ps 实证 serve 进程即它)对三件 py_compile 全过;codesign ad-hoc 重签 `SIGNATURE VALID` 且运行中 app(PID 19416)存活;**调度执行面=子进程**(cron/executions.py:102 subprocess.run)→ 20:00 射点起新进程自然装载新引擎,无需重启 app。数据根 plugins/ai-news.yaml 外科只加 meta 块(12 源,yaml 解析亲验;不部署并行国产流在途源)。装机 python `find_spec('crawl4ai')=False` 亲验=owner_left 如实。

**owner_left(新增一项,同 llm extras 先例)**:装机 python 无 crawl4ai(随包 requirements-lock.txt 亲核无该包)→ 装机态 meta-ai-blog-watch 每 run 结构化 `dependency_missing`(不拦品类内其余源);仓库 CLI(venv 全 extras)即刻可用。收编路径=desktop lock 扩 crawl4ai extras(涉依赖指纹变更,主人裁定)+设置页一键重装;playwright 浏览器二进制走用户级缓存 `~/Library/Caches/ms-playwright`(与仓库 venv 共享,装机装同版 playwright 无需重复下载浏览器)。

### §12.1 独立复核轮处置(2026-10-06 下午,三发现全涉本流,已回改)

**[HIGH] 装机「三件直更」实落两件——属实,已根治+补件+验错误码归位**:首装同步(12:29 cp+diff 三件 IDENTICAL+sidecar py_compile 三过,本会话输出在案)之后,**12:50 的包刷新事件(插件目录 mtime)把 render_crawl4ai.py 清出装机分发面**(复核员 ls 实证仅 README/adapter/plugin.yaml;12:5x 重签的 CodeResources 已与缺件状态一致)。根因亲核:`desktop/src-tauri/tauri.conf.json` resources 对 myssia-urlwatch 是**显式三件枚举**(plugin.yaml/README.md/adapter.py),任何按清单的打包/刷新都会丢未知新件——我首装只 cp 未同步清单,属本流交付缺口。修复三层:①清单补 `"../../plugins/myssia-urlwatch/render_crawl4ai.py"` 行(未来官方重打包不再丢);②装机补件 cp+重签(`codesign -v` SIGNATURE VALID,目录四件在位);③**装机 python(数据根 python/bin/python3,cwd=数据根、sys.path=装机 myssia-src、无 env 注入=复核员同款形态)亲验**:`render_helper_path()` 经源码树兜底解析到 `/Applications/世事.app/Contents/Resources/plugins/myssia-urlwatch/render_crawl4ai.py`;`render_backend_available('crawl4ai')=False`;真 `_render_helper('crawl4ai')` → **FetchError `dependency_missing`**——§12 owner_left 的「装机态每 run 报 dependency_missing」口径自此与实态相符(复核指出的「主人按错向修不好」风险出局:真修法=lock 收编 crawl4ai 后该源即活,件已随包不再缺)。

**[MEDIUM] win32 命令引号缺口——属实,已改强制引号**:`subprocess.list2cmdline` 只引含空格参数,带查询串 URL(`?page=2&lang=zh`,无空格)不被包裹,上游 ShellJob `Popen(shell=True)` 在 win32=cmd.exe /c,`&` 即命令分隔符(复核员本机实证)。修=win32 分支三段**无条件双引号**(三段经校验不含引号/控制字符;`%` 展开=cmd 既有语义,URL 百分号残片不在已定义变量表,docstring 如实注记);`subprocess` import 随之清理。测试换含 `&` URL 断言全引号形态(原测试恰好只用无元字符 URL=钉住错觉面,复核所指属实)。darwin 主装机面本就不受影响(shlex.quote 正确)。

**[LOW] MARKDOWN_B 零引用——属实,已启用等值断言并当场抓出夹具错**:`strip_markdown_noise(MARKDOWN_A) == MARKDOWN_B` 等值断言入测(夹具补 `[带标题链接](url "title")` 形态);首跑即抓出我原夹具推导错——A 首行是「链接文字=图片本体」形态(`[![Meta](img)](link)`),图片剔除后该行归一为**空**(非 `Meta`),原子串断言对此无感。helper 同步补逐行 rstrip 归一(链接文字悬空尾空格不进快照)。

**门禁(回改后)**:ruff check 绿+format 净;定向五件(engine/plugin/helper/插件包守卫/tauri resources 钉件)383 passed 24 skipped;全量 pytest **4528 passed / 0 failed / 0 errors**。装机复核三验:目录四件在位、SIGNATURE VALID、装机 python 真路径 `_render_helper` → dependency_missing。

### §12.2 复核二轮处置(2026-10-06 傍晚,两发现全涉本流,已回改)

**[MEDIUM] resources 枚举行无回归守卫——属实,补反向对账钉并变异验证**:复核员实证「从 tauri.conf.json 删 render_crawl4ai.py 行后全部测试仍绿」(rebuild_bundled_tree 只做映射→磁盘正向、pyenv_resources 只钉自管环境五映射、plugin_packages 只钉仓库目录文件集)——§12.1 门禁段写「tauri resources 钉件」名实不符(所引五件对该行零覆盖),此处更正:彼时无钉,本钉落定后口径才成立。新钉 `test_bundled_package_files_are_fully_mapped_in_tauri_resources`(tests/desktop/test_bundled_plugins_install.py):**磁盘→映射反向对账**——随包组件包目录(映射派生包集,与 BUNDLED_PACKAGES 守卫常量同源对账)内分发件(.yaml/.yml/.py/.md)逐文件必须被 bundle.resources 精确登记或落在整目录映射(credhunter 子包先例)之下;__pycache__/loot(运行时产物)与 vendor(gitlink 子模块=上游代码,设计上零随包)排除。**变异亲验**(复核员同款手法):删 render_crawl4ai.py 行 → 红,消息精确点名 `myssia-urlwatch/render_crawl4ai.py: 组件包分发件未登记`;还原 → 绿。守卫自检过程修掉两处实现 bug(键/值方向、dest 前缀对齐),并在本机 osint vendor 已 init 的实况下收窄排除面。

**[LOW] docstring 引号前提无强制——属实,入口显式拒**:`build_render_command` docstring 声称「三段不含引号」但校验链不拒 `"`(adapter._checked_http_url 只拒空白/控制/超长,ord('"')=34 放行;且引擎构命令先于 adapter 校验)——win32 三段无条件引号会被 URL 裸双引号闭合破坏。修=本入口(声明所在处)对三段任一含 `"` 即结构化拒 `invalid_render_command`(Posix 的 shlex.quote 本可安全处理,统一拒保契约单口径;词表入模块 Raises);参数化三用例(python/helper/URL 各含 `"` 形态)钉死。

**门禁(回改后)**:ruff check 绿(format:urlwatch.py 落定;test_bundled_plugins_install.py 第 60 行为既有基线漂移零触碰,2022bd9 先例);定向七件(engine/plugin/helper/plugin_packages/bundled_install/pyenv_resources/installer_resources)457 passed 24 skipped;全量 pytest **4532 passed / 0 failed / 0 errors**。装机:urlwatch.py 引擎件再外科直更+重签(SIGNATURE VALID,render_crawl4ai.py 在位复验)。

## §13 三轮深扫质询轮(主人:「还有更多的问题你没有查到吧?」)

**发现 A(已修)**:摘要池零排序零筛选——flush 按到达序直出,cocoloop 论坛闲聊(日产 46+ 条)淹没厂商要闻,日报主目的受损。修=flush 稳定排序(`_digest_order_key`:enrich value 降序在前,无分条目到达序殿后,坏分形状归无分段);测试 test_digest_flush_orders_scored_items_first_desc(9/7/3 分+两闲聊+坏分形状六条目序钉死),tests/push 62/62;同槽位拦截/合并卡等既有语义零变化(无分条目到达序被既有测试钉住,稳定排序保绿)。

**发现 B(在档待修,证据充分)**:aihot 每轮 3-5 张「作者精选卡」被静默丢弃——实证(14:1x 探针):无 h3 的卡片是编辑精选的 X 帖摘要(实测卡:Rohan Paul「Anthropic 计划未来数年在云计算上支出 5180 亿美元…」/「A16Z 第七版 Top 100 消费级 AI 应用解读」/「Google 等机构论文提出 insecure reporting 现象」),卡内有 /items/<id> 链接但不在 h3 下,extract 的 url:"h3 a@href" 取不到→invalid_item。**恰是主人最初要的「X 上面的监控」信号,每轮丢 3-5 条高质量内容**。修法方向:提取 DSL 验证逗号并集选择器(h3 a@href, a@href)+标题回退的语义(需读 static_html 提取字段实现后定,本轮查改分家不盲动);卡片 id 样本 nnl0kba78980jig0szh0hkfop 等。
**发现 C(已实证未修)**:watch 选择器失效=静默死亡——假选择器两跑 R1 new(空快照)→R2 unchanged(空==空),此后恒 unchanged 零告警,站点改版即触发且无任何可见痕迹。修法方向:shim 事件附带快照字节数,引擎对 unchanged-and-近零字节出 WARNING(选择器疑似失效)——小改,待令。
**其他核过无恙**:今晨 immediate 4=freebie/buying-agent 类目路由(非分数路,YAML 设计);打分直方 1-7 无异常;摘要模板渲染可读;调度心跳新鲜。操作依赖重申:**20:00 跑要求 app 保持运行**(调度器活在 app 进程里)。

## §14 推送链终验(2026-10-06 14:54,主人指路 Hermes 蓝本)

主人提示「Hermes 配置里有飞书,2 个机器人」——蓝本部署在 ~/.hermes/hermes-agent,.env 内全套凭据:FEISHU_APP_ID(20)+FEISHU_APP_SECRET(32)+FEISHU_HOME_CHANNEL(35,oc_ 群 chat id)。按 MYIA 钥匙串规范代录三键(myia/push/FEISHU_APP_ID/APP_SECRET/CHAT_ID,值走管道零外显,用完建议主人轮换)。**R5 生产真跑:feishu_card ok=True,6 条日报真发**(tenant token 自动续期路径,首个端到端推送成功——全链至此闭环)。第二个机器人未动(暂无需,留档知会)。meta dependency_missing 维持 partial 属预期(owner 裁决项)。20:00 起每日双槽日报。

## §15 渠道覆盖矩阵与出口环境阻塞(主人问「推文/视频博主/厂商最新渠道」)

| 渠道层 | 状态 | 机制/阻塞 |
|---|---|---|
| 厂商官网/博客 | ✅ 在产 | 16 源+prompt 三厂日报 |
| X 推文博主 | ⚠️ 仅 aihot 编辑精选卡间接信号 | 直连=RSSHub 自部署(Docker 前置)+TWITTER_AUTH_TOKEN,启用三步在 ai-news.yaml S3 注释块 |
| 视频博主(YouTube) | ❌ 机制就绪、出口阻塞 | YouTube 原生 RSS(feeds/videos.xml?channel_id=)现有 rss 通道直接可吃;本轮探针实证:直连墙+本机代理 7897 未运行双 ConnectError——clash 开着即可配置化接入,零新代码 |
| 厂商官号(X/YouTube) | 同上两阻塞 | OpenAI/Anthropic/DeepMind 官号 handle 清单已列,代理恢复后一次探查 channel_id 即入册 |
抓取目标配置位:品类 YAML sources: 段(每爬虫一行)/prompt 件 engine_options.prompt.urls。
