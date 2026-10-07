# PRD:退化 AI 资讯三源复活(anthropic / cohere / meta)

> 立档:2026-10-07 · 来源:仪表盘告警点名三源退化 · 类型:PRD-only 轻量档(诊断+适配修复)

## 报障证据矩阵(2026-10-07 真网+生产库亲核)

告警来源:主人仪表盘(读生产库 `~/Library/Application Support/MYIA/myssia.db`,最近 ai-news 轮 = run 29,2026-10-06 19:25)。doctor 亲跑复核(`myssia doctor plugins/ai-news.yaml --db <生产库> --json`)与告警口径一致。

| 源 | 告警 | 真网诊断(逐一亲核) | 根因判定 |
|---|------|---------------------|---------|
| anthropic-news-watch | 指纹未跳过却产出 0 条(页面结构变化/反爬升级疑似) | curl `https://www.anthropic.com/news` = **HTTP 200/428KB**;robots `User-Agent: * Allow: /`;按 urlwatch css 过滤器仿真(`main` + exclude)→ **1 命中/14575 字节快照/1980 字可见正文**(远高于 200 字节哨兵线,选择器健康);生产库 run 29 实况:该源 n=**1**(真变更条目,变更监控本体在工作) | **非选择器过期、非反爬**。urlwatch 快照未变时 skip=`watch_unchanged`,而健康度词表 `FINGERPRINT_UNCHANGED_REASONS`(cli.py:329)只认 `not_modified/validators_match/hash_match`——**合法空态被误诊为退化**(与告警文案逐字吻合,doctor 亲跑已复现) |
| cohere-blog-watch | 同上 | curl `https://cohere.com/blog` = **HTTP 200/1038KB**;robots Allow /(blog 路径不在 Disallow 列);`main` 过滤仿真 → **1 命中/86207 字节快照/3340 字正文**(选择器健康);生产库全史:恒 `watch_unchanged`(页面真无变更),run 3 曾产 1 条 | 同上(同类误诊,fetch 面完全健康) |
| meta-ai-blog-watch | 最新一轮采集失败(实际 doctor 亲跑已到 **dead:连续 3 轮采集失败**) | curl `https://ai.meta.com/blog` = **HTTP 400**(全浏览器头+HTTP/2 仍 400;sitemap 403)——**对非浏览器指纹升级拦截,静态通道判死**;crawl4ai 真渲染(仓库 venv)= exit 0/1165 字可读博文列表;生产库 run 29 报错实锤:`dependency_missing:渲染后端 crawl4ai 未安装(渲染通道由运行 myssia 的解释器(…/Application Support/MYIA/python/bin/python3)执行)`——**桌面托管 python 未装 crawl4ai 组件**(`desktop/resources/components.json` 已声明该组件,设置页一键装;`pyenv-settings.json` 为空 = 主人未装) | **双根因**:① 桌面环境缺 crawl4ai 组件(装机面,先例「归主人」,设置页一键装即恢复);② 静态面被指纹墙拦死,渲染通道是唯一活路 |

### 补充事实(引用即已核)

- 三源均为 `engine: urlwatch` 变更监控(10-06-ai-news-sources S2 落地):零变更=合法空态是上游钉死语义(engines/urlwatch.py:17-18),但健康度词表从未收编 watch 系哨兵(store_report.py:134 注释在案)。
- zhipu/moonshot/minimax/seed 四个同型 watch 源同样被误诊 degraded——**本档不扩面**,记遗留推荐。
- classify builtin 实测:纯英文标题大部分 DROP(如 "Expanding the Cyber Verification Program"),含 Claude/GPT 等词的放行——与既有七家 RSS 源同语义,fetch 级产出即健康度口径,不新增过滤。
- golden 基件:`tests/fixtures/push_targets_golden/plugins/ai-news.yaml` 冻结副本 + `push_targets_golden_before.json`,改官方插件声明面必须 `uv run --no-sync python tests/regen_push_targets_golden.py --refreeze` 重产。

## 修复方案(链接者架构:只改配置,不改上游)

三源统一切到**列表抽取**(与品类内 aihot/cocoloop/七家 RSS 同范式:每轮真产出 N 条,dedup `{url}` 拦重推;健康度回「本轮产出 N 条」= ok,彻底绕开 watch 哨兵词表缺口):

| 源 | 引擎 | 抽取(已用引擎真实 extract_html 路径验证) |
|---|------|----------------------------------------|
| anthropic-news-watch(名不改,daily-digest 引用零动) | static_html(SSR 实证) | item=`main a[href^='/news/'], main a[href^='/claude-']`(14 条:11 新闻卡+3 特写卡);title=`h2, h4, [class*='__title']`(CSS-module 哈希类只押 `__title` 语义后缀);url=`@href`;published=`time` |
| cohere-blog-watch | static_html(SSR 实证) | item=`main a.flex[href^='/blog/']`(22 条文字卡,天然排除 /blog/tag/ 药丸);title=`p`(首 p=标题);url=`@href`;published=`p[class*='eyebrow']` |
| meta-ai-blog-watch | **crawl4ai(渲染通道,L3)+ extract list** | item=`a[aria-label][href^='https://ai.meta.com/blog/']`(渲染后 8 锚/4 独立最新帖;类名全混淆哈希,aria-label 是唯一稳定语义面);title=`@aria-label`(带 "Read " 前缀,无 transform 层,如实保留);url=`@href`。覆盖面如实记:最新 4 帖,特写 hero 与底部 Learn More 区不覆盖 |

- meta 桌面面依赖:设置页装 crawl4ai 组件(components.json 已声明,`pip_spec: crawl4ai>=0.9,<0.10` + playwright-chromium)即活;仓库 venv 验证道已具备(crawl4ai 实测可导入、渲染 exit 0)。
- 四个同型 watch 源(zhipu/moonshot/minimax/seed)不动:不属本档报障面,留待后续把 watch 系哨兵收编健康度词表(推荐,涉 cli.py 域,另行立档)。

## Acceptance Criteria

- [ ] AC1 真跑产出:`uv run --no-sync myssia test plugins/ai-news.yaml --source <源>` 逐源真跑,三源 item_count > 0(试抓不入库零持久化副作用)。
- [ ] AC2 golden 同步:`--refreeze` 重产后 `tests/push/test_push_schema_targets.py` 黄金回归绿,冻结副本与活库 JSON 同步。
- [ ] AC3 域内门禁:相关 pytest 域全绿(plugins 域 + golden 域 + schema 装载面),`myssia doctor plugins/ai-news.yaml` 装载检查零新增 finding。
- [ ] AC4 档+yaml+golden pathspec 一并提交(feat(plugins) 前缀),task.json 置 review;evidence/ 不入 git。
- [ ] AC5 判死条款:若某源真跑仍 0 条且无解,如实记根因、回退该源改动、档内推荐替代源,不硬编假产出。
