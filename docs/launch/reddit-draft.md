# Reddit r/selfhosted 发帖草稿(英文,v0.0.1 开源发布)

> **状态:草稿,正文可直接定稿;发布节奏由主人定,发帖前必须过「发帖前硬
> gate」与版规核实。**

> **发前必做:人工点开核实现行版规(下方版规信息均未经直接核实)。** 本写稿
> 环境对 reddit 的全部抓取通道均被拒(WebFetch 与 curl 带 UA 请求 `.json` API
> 均返回 403 拦截页;webReader 对 www 域报 "blocked by network security";
> old.reddit 强制登录),下列版规信息全部来自搜索引擎快照,且快照显示该版规则
> 近期反复调整。发帖前请亲自打开
> https://www.reddit.com/r/selfhosted/wiki/rules (或版块侧栏),以当日现行规则为准:
>
> 1. **项目展示贴的 flair 与时机——勿默认沿用旧规则。** 快照史料一(帖
>    `1rmt39o`,"New Project Friday here to stay, updated rules"):项目展示集中
>    "New Project Friday" flair、同名项目重发间隔 3 个月;快照史料二(更晚的
>    帖 `1sey9ch`,"Quarter 2 Update - Revisiting Rules. Again.",帖 ID base36
>    晚于前者):"New project Friday became new project whenever. That rule was
>    not followed."——即 NPF 集中制此后又已放松/改动,现行要求未定,发帖时按
>    侧栏当日规则选 flair 与时机。两帖链接(供人点开,需正常浏览器/登录态):
>    https://www.reddit.com/r/selfhosted/comments/1rmt39o/rules_update_new_project_friday_here_to_stay/
>    https://www.reddit.com/r/selfhosted/comments/1sey9ch/quarter_2_update_revisiting_rules_again/
> 2. **社区对 AI 腔营销文高度反感**(检索快照可见多条同类抱怨帖)——保持第
>    一人称、给具体细节、如实报限制。
> 3. 英文正文未绑定任何 flair/时机策略;规则核对结果只影响发帖时的 flair
>    选择与日期,不影响正文本身。
>
> 本稿口径是 **v0.0.1 发布后的现实**(`pip install myssia` on PyPI、Docker
> 镜像 `ghcr.io/xinzhuzi/myia`)——截至本稿写就,仓库 README 仍是旧版 +
> "install from source" 口径、PyPI 双包未上架(实测 404)、v0.0.1 tag 已推送【2026-10-05 更新:双包 0.0.1 已上线,此行过时仅存档】
> 但 Release 页未上线,故硬 gate 里把这些列为发帖前置条件,未满足前**不可发**
> (正文里的 "on PyPI" 等表述发早一天就是假话)。
>
> **2026-10-04 终态实核**:PyPI 双包仍 404(登记=主人门禁,在途,包名终局【2026-10-05 更新:双包 0.0.1 已上线,此行过时仅存档】
> `myssia` / `myssia-classifier`);v0.0.1 Release 已上线但资产带旧名前缀
> (`shishi_0.0.1_aarch64.dmg`,直链以 Release 页为准);Docker 0.0.1 镜像在
> `ghcr.io/xinzhuzi/shishi:0.0.1`(发布时旧仓名,后续版本在
> `ghcr.io/xinzhuzi/myia`);Windows msi 构建管线已绿(Release 页无 msi);
> 命名终局:CLI/模块/发行名 = `myssia`,GitHub 仓库 = `xinzhuzi/myia`,
> 「世事」为中文名;`myssia --version` 实输出 `myssia 0.0.1`。硬 gate 未过
> 前,本稿 pip 口径不可发;source-install 口径的现行版见
> `reddit-r-selfhosted.md`。
>
> 主文案英文,文末附中文对照草稿(便于主人先过目内容)。

## 标题候选(选一)

1. `I open-sourced my self-hosted intelligence hub: one YAML per thing to watch, fetch → classify → dedup → push — and my coding agent writes the YAML (MIT, Docker image + desktop dmg)`
2. `myssia (世事) — self-hosted "tell it what to watch, AI does the rest": one YAML per category, push to Telegram/Feishu, coding-agent-native (MIT, v0.0.1)`
3. `Stop rewiring scrapers + cron + diff watchers for every new thing to watch — myssia is one config-driven pipeline for any category (open source, MIT)`

## 正文

Hey r/selfhosted,

I kept assembling the same stack for every "I want to know when X happens"
problem: a scraper, a cron job, a diff watcher, a dedup hack, a webhook into
my messenger. Each new target (AI news, stock moves, freebies, GPU prices)
meant re-wiring all of it.

So I built **myssia** (世事 — Chinese for "the ways of the world") — an
open-source (MIT), self-hosted intelligence hub. Pure Python, one SQLite
file, no daemon, no Redis, no Postgres. **One YAML file = one intelligence
category:**

```yaml
id: demo-min
name: Minimal demo
schedule: "0 9 * * *"
sources:
  - name: example-news
    engine: static_html
    url: "https://example.com/news"
    extract:
      type: list
      item: "article"
      fields:
        title: "h2 a"
        url: "h2 a@href"
classify:
  builtin: false                 # demo items match no category; disable the filter
push:
  - channel: stdout              # zero-credential local verification
```

The YAML is the whole deployment: schedule (cron + timezone), any number of
sources, dedup keys, scoring thresholds, push channels. And because it's
agent-native, you don't even write it — the bundled Agent Skill
(`myssia skill install --agent claude`, Cursor supported too) teaches your
coding agent the 12-section schema; it generates the file, trial-fetches with
`myssia test`, rehearses with `--dry-run`, and repairs broken sources from
`myssia doctor --json` output. You say what you want; the agent does the rest.

What's inside:

- **Six-rung auto-degrading fetch ladder** — direct API → static HTML →
  crawl4ai / Firecrawl → Scrapling → stealth browser → LLM browser. A source
  never hard-codes an engine: when one rung fails, the next takes over, and
  the winning engine is remembered per source (in SQLite — never written back
  into your YAML). Heavy engines are optional extras; the core stays light.
- **Zero-token classifier** (7 keyword categories) plus optional LLM scoring
  (value / relevance / credibility, 0–10), then threshold routing: score ≥ 8
  pushes immediately, ≥ 5 joins the AM/PM digest, the rest is archived.
- **Push that respects your attention** — Feishu cards, Telegram, webhook or
  stdout, with a URL-key dedup registry: the same URL never pushes twice.
- **Credentials never touch the config** — only `env:VAR` / `keychain:`
  references are legal; a plaintext credential in YAML is rejected at load
  time. Backed by macOS Keychain / Windows DPAPI.
- **Feedback loop** — mark pushed items valuable / not valuable (works from
  the CLI today, plus Telegram/Feishu callback receivers; in-card buttons on
  the desktop app land in a later batch) — negative feedback retunes weights
  and thresholds over time.
- **Polite by default** — robots.txt respected, rate limiting on by default,
  and sources that demand human verification (CAPTCHA, phone numbers) fail
  with a structured error instead of being bypassed.

Three ways to run it:

- **CLI**: `pip install myssia` (heavy engines are optional extras, e.g.
  `pip install "myssia[crawl4ai]"`), then `myssia run --loop` for scheduled
  operation. **Gate: this line only goes out once the PyPI pair is live**
  (2026-10-04 status: still 404, registration in flight — until then the
  honest line is source install: `git clone` + `uv sync`).
- **Docker**: a
  [compose file](https://github.com/xinzhuzi/myia/blob/main/docker/docker-compose.yml)
  ships in the repo; the v0.0.1 multi-arch image is on GHCR — the 0.0.1 tag
  lives under the repo's short-lived name at push time
  (`ghcr.io/xinzhuzi/shishi:0.0.1`); the repo is back to `myia` and later
  releases publish under `ghcr.io/xinzhuzi/myia` (releases are tag-driven;
  pushes to main no longer publish images).
- **Desktop app** — see below.

**On the version:** v0.0.1 makes the desktop app daily-drivable:

- v0.0.1 unified the desktop data paths, bundled the official plugins on
  first run, and added a **zero-credential demo** — GitHub's new-star board
  via one unauthenticated API call — so the first "run" click shows real data
  instead of a config error. Nothing to fill in.
- v0.0.1 also added a **signed update channel**: the settings screen checks
  for updates, downloads and installs them with signature verification, then
  relaunches.
- The PyPI packages ride the same release pipeline — **still in flight**
  (registration pending as of 2026-10-04), gate 2 below. Naming settled
  2026-10-04: CLI / module / distribution name is `myssia` (`import myssia`
  works), the GitHub repository stays `xinzhuzi/myia`, and 「世事」 is the
  Chinese name.
- The macOS (Apple Silicon) installer is on
  [GitHub Releases](https://github.com/xinzhuzi/myia/releases/tag/v0.0.1)
  — grab the dmg (heads-up: the asset currently carries the short-lived old
  repo name, `shishi_0.0.1_aarch64.dmg`; the Releases page is authoritative).
  It is **not** Apple-notarized (notarization needs a paid developer
  account, which I don't have yet), so first launch takes the right-click →
  Open → Open dance; every installer is built in public CI with traceable
  logs, and the code is fully auditable.
- Windows: the msi pipeline went green in CI right after this release (a
  verification run produced the msi artifact), but no Windows installer is
  attached to v0.0.1 and no install has been smoke-tested — the first
  Windows package ships with the next release. No "works on Windows" claims
  yet.

Desktop screenshots (all fed by real demo-plugin data):
[dashboard](https://github.com/xinzhuzi/myia/blob/main/docs/screenshots/dashboard.png) ·
[feed](https://github.com/xinzhuzi/myia/blob/main/docs/screenshots/feed.png) ·
[sources](https://github.com/xinzhuzi/myia/blob/main/docs/screenshots/sources.png) ·
[logs](https://github.com/xinzhuzi/myia/blob/main/docs/screenshots/logs.png) ·
[settings](https://github.com/xinzhuzi/myia/blob/main/docs/screenshots/settings.png)

**Landed on main since the release** (shipping with the next version — not
in the v0.0.1 dmg): scheduled jobs — `myssia cron`, natural-language
schedules or 5-field cron, three coexisting hosts with run summaries
delivered to targeted channels; alert rules evaluated against every incoming
item (dry-test that never sends); a ⌘K command palette; feed read/starred/
later state moved server-side (whole-library "mark all read"); and a
keyboard-interaction batch (j/k navigation, context menu, unread-first,
collapsible sidebar).

Honest status:

- The PyPI pair (`myssia` / `myssia-classifier`) is still in flight —
  registration pending as of 2026-10-04; until it lands, CLI install is from
  source (`git clone` + `uv sync`; the repo is a uv workspace).
- Releases currently ship a macOS (Apple Silicon) installer only — the
  Windows msi pipeline is green in CI (build level: no installer in
  Releases, no install smoke-tested); no "works on Windows" claims yet.
- The desktop in-card feedback buttons aren't in yet (the feedback loop works
  via CLI + Telegram/Feishu callback receivers today).
- 2000+ tests run in CI, none of them touching the real network (2026-10-04
  local `pytest --collect-only`: 3604; CI runs the authoritative count).

Links:

- Repo: https://github.com/xinzhuzi/myia (MIT)
- Release v0.0.1: https://github.com/xinzhuzi/myia/releases/tag/v0.0.1
- Getting started: [docs/en/getting-started.md](https://github.com/xinzhuzi/myia/blob/main/docs/en/getting-started.md)
  (bilingual; the Chinese (zh) tree ships in-repo and tests keep both in sync)
- Agent Skill (for your coding agent): https://github.com/xinzhuzi/myia/blob/main/skill/SKILL.md

Happy to answer questions — especially on the degrade chain and the
credential handling. What would *you* point it at first?

## 发帖前硬 gate(未全部满足不发;写稿时点实测状态已注)

1. **v0.0.1 Release 已上线**(写稿实测 Release 页 404,tag 已推送;2026-10-04
   实核已上线,资产带旧名前缀 `shishi_*`):dmg 等
   资产 URL 当日从 Release 页复制粘贴,禁止手改版本号拼链。
2. **PyPI 双包已上架**(写稿实测 pypi.org/pypi/myssia/json 与
   /myssia-classifier/json 均 404;2026-10-04 终态复测仍 404,登记=主人
   门禁在途,若 pypi.org 侧曾按旧名建过 pending publisher 需删旧建新):
   两个 JSON API 返回 200 再发——正文
   "on PyPI" 的全部表述以此为前提。
3. **命名决议落地(2026-10-04 终版)**:myssia 为项目唯一正式名——发行名/CLI/
   模块名全链统一(`src/myssia`、`myssia.cli:main`),「世事」为中文名;
   GitHub 仓库保持 `xinzhuzi/myia`(split naming,owner decision B)。
   发布前干净环境 `python -c "import myssia"` 实测通过。
4. **README 已同步切到 pip + 0.0.1 口径**(快速开始 / 下载安装段 / 版本号 /
   `myssia-classifier` 目录链接)——否则读者点进仓库第一屏就与帖子矛盾。
5. **CHANGELOG [Unreleased] 已定版为 [0.0.1]**;顺带把 README 与 CHANGELOG
   关于桌面反馈按钮交付批次的口径对齐(两处现在一个写桌面对齐批次、一个写
   v1.2,读者对照会发现打架)。
6. **截图清单按当版实际 UI 核对**:第六屏「消息」已在开发分支合入,若随
   v0.0.1 发布,截图链接清单按实际增补。
7. **CI 测试数以当日实数刷新**:写稿时本地 `pytest --collect-only` 实测
   2159 条,正文用 "2000+";2026-10-04 终态复测 3604 条;CI 实跑数若不同,
   以 CI 为准。
8. **版规核对**(见顶部「发前必做」):按当日侧栏规则选 flair 与发帖时机。

## 中文对照草稿(发布前主人过目用,不直接发出)

各位好,我给自己造了个开源自托管情报中枢 **myssia(中文名:世事)**(MIT,
纯 Python + SQLite 单文件、无守护进程):想盯的每类情报(AI 资讯/股票异动/
羊毛/显卡行情)就是一个 YAML 文件,抓取→分类→去重→打分→推送到
Telegram/飞书全自动。YAML 都不用自己写:内置 Agent Skill 让编码 agent 照
12 节规范现场生成、`myssia test` 试抓验证、坏了凭 `myssia doctor` 自修——
说需求,AI 做其余。

内里:六级采集降级梯(API→静态 HTML→crawl4ai/Firecrawl→Scrapling→隐身浏览器→
LLM 浏览器,胜出引擎按源记忆);零 token 七类关键词分类器 + 可选 LLM 精评,
score ≥ 8 立推、≥ 5 进早晚摘要;飞书/Telegram/webhook/stdout 四通道 + URL 键
去重(同一 URL 不推第二遍);凭据只走 env/系统钥匙链,YAML 里出现明文凭据
加载即拒;robots.txt 默认尊重、要真人验证的源结构化报错不绕过;反馈闭环 CLI
现已可用(桌面卡片内按钮后续批次)。三种跑法:CLI `myssia run --loop`、
Docker(0.0.1 镜像在 `ghcr.io/xinzhuzi/shishi:0.0.1`,后续版本在
`ghcr.io/xinzhuzi/myia`)、桌面应用;数据单 SQLite 文件。

**v0.0.1 起桌面端可日常用**:macOS(Apple Silicon)安装包在 GitHub Releases
(资产名 `shishi_0.0.1_aarch64.dmg`——发布时仓库短暂用旧名,以 Release 页为
准;未做 Apple 公证,首开右键→打开,安装包公开 CI 构建);装机首跑种子官方
插件,含零凭据演示件(GitHub 新星榜,一次免鉴权 API 调用),第一次点运行就出
真数据;设置页走签名更新通道,验签后自动下载安装。桌面截图(均为 demo 插件
真实数据):仪表盘/信息流/源管理/日志/设置。

**PyPI 双包(`myssia` / `myssia-classifier`)在途**(2026-10-04 实核 404,登记【2026-10-05 更新:双包 0.0.1 已上线,此行过时仅存档】
未完成):上架后 `pip install myssia` 直装、`import myssia` 可用(命名终局:
CLI/模块/发行名 = myssia,GitHub 仓库 = xinzhuzi/myia,「世事」为中文名)。

发布后合入 main、随下个版本(如实:v0.0.1 安装包里没有):定时任务
`myssia cron`(自然语言排程 + 运行摘要定向投递)、告警规则、⌘K 命令面板、
已读状态进服务端、feed 键盘流(j/k 导航/右键菜单/未读优先/侧栏折叠)。

如实说:PyPI 未上架前 CLI 走源码安装(git clone + uv sync);Windows msi 构建
管线已绿(CI 验证 run 产出工件)但 Release 页没有 Windows 包、装机未验证;
桌面卡片内反馈按钮还没做(反馈闭环 CLI + 回调接收现已可用);CI 2000+ 测试
零真实网络(2026-10-04 工作树 collect 实测 3604)。

仓库 https://github.com/xinzhuzi/myia ,求建议:你会先拿它盯什么?

---

> 2026-10-04 终态刷新,待主人定稿。
