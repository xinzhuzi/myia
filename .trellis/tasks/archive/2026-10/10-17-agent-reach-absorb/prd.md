# PRD — 吸收 Agent-Reach:X/YouTube/B站公开平台情报源

> 建档 2026-10-17。来源:主人发来 B站视频(BV1VtHf6yEHG)问「哪个能吸收」,
> 三工具裁决后主人令「做个 trellis 任务,针对这些进行吸收」。

## 一、背景与三工具裁决(为什么只有这一件)

视频介绍的三个开源工具,对 MYIA 现状逐一对账后裁决如下:

| 工具 | 裁决 | 依据 |
|---|---|---|
| **Scrapling**(D4Vinci/Scrapling,88k★) | **不吸收——已经有了** | MYIA L4 引擎 `engines/scrapling.py`(10-01-v03-engine-scrapling)已实装三后端+自愈选择器+无限滚动 |
| **patchright-enhanced**(whaleyxbt,基于 Patchright 4.9k★) | **不吸收——能力位已占** | L5 `stealth_browser.py` 用的 invisible_playwright_mcp 是同生态位反检测 Playwright 变体;同位换件无新增能力,仅当 L5 实跑撞墙再翻案 |
| **Agent-Reach**(Panniantong/Agent-Reach,98k★,MIT) | **吸收——本任务** | 填补真空白,见下 |

### Agent-Reach 是什么、为什么吸收

- GitHub 98k★,MIT,Python。定位「互联网能力路由器」:**本体是安装器+多后端路由器+健康检查器,真正干活的是它装好的上游 CLI**(`bili`、`yt-dlp`、`twitter`、`opencli`、`mcporter` 等),零 API 费。
- 16 平台里 MYIA 的空白:X/Twitter、YouTube、**B站**、小红书、公众号文章;已有覆盖:Reddit(10-05 官方 API 引擎)、GitHub、RSS、网页(static_html/crawl4ai/scrapling 全链)、Telegram、飞书、微信。
- 这批平台正是通用抓取引擎最难啃的(反爬+登录墙+动态渲染),Agent-Reach 用**平台语义读取**(搜索/投稿列表/字幕的结构化输出)绕开,与 MYIA 现有引擎互补不重叠。
- 完整上游契约见 `research/upstream-SKILL.md`(上游 SKILL.md 原文存档)。

## 二、目标

把 Agent-Reach 按链接者模式吸收进 MYIA,交付一条**从安装到情报条目**的完整链路:

1. **组件接入**:Agent-Reach 及其上游工具可被 MYIA 自管环境安装、探测、体检。
2. **新引擎** `engines/agent_reach.py`:链外引擎(credhunter/saas 先例),subprocess 调上游 CLI,产出结构化条目进既有管线(fetch→classify→dedup→push 全复用)。
3. **首批品类源(免登录档)**:
   - **B站**:关键词搜索/热门/排行监控(bili-cli 免登录,action 限 `search`/`hot`/`rank`);
   - **YouTube**:频道投稿监控(yt-dlp flat-playlist,无需登录);
   - X/Twitter 免登录单条读取能力**存档不建源**(grill 实证成立但对监控源形态价值弱,归 enrich 面后续档,见 AC8)。
4. 首跑真条目进 feed,dedup 以条目 url 为锚全期生效。

## 三、非目标(明确不做)

- **登录态平台一律不做**:X 搜索、小红书、Reddit(Cookie/OpenCLI)、Facebook、Instagram、Boss直聘——涉及 Cookie 凭据、封号风险、浏览器会话复用,后续另档按 keychain 模式评估。
- **Exa 搜索/Jina Reader 不吸收**:与现有 searxng/static_html 能力重复(复用已有资产纪律)。
- **写操作**(发帖/评论)不碰;上游源码一行不改(链接者铁律)。
- **不做 UI 面**:设置页组件化下载按钮、源健康度 UI 归 v12-backlog 池,不在本档。
- 不迁移/不改动既有品类与引擎的任何行为。

## 四、约束

1. **链接者铁律**:只写适配层,永不改上游;不复制上游源码进仓库。
2. **核心零新增依赖**:引擎经 `asyncio.create_subprocess_exec` 调 CLI,MYIA 核心不 import agent-reach 任何符号(scrapling 惰性 import 同款纪律);extras 可选依赖 direct-URL **钉 tag/commit**(上游官方警告 PyPI 同名包是假冒,必须 GitHub 直装;main 漂移头禁用——远取链真锁纪律)。
3. **链外引擎语义**:显式 `engine: agent_reach` 才生效,永不进 AUTO_CHAIN,失败=源级结构化失败,不降级、不拦品类。
4. **凭据零明文**:第一期零凭据;子进程环境最小化,不透传无关 env。
5. **礼貌采集**:B站/YouTube 均为配额敏感平台,源级 qps 限速必配;上游 CLI 已做重试链,MYIA 不再叠加重试。
6. **源命名规约**:`<平台>-<渠道标识>` 全局唯一(主人 2026-10-06 令),如 `bili-ai_news`、`yt-<频道>`。
7. 装机包不带 Agent-Reach 本体(插件源码不随包规范),用户侧经 extras/安装提示自装。

## 五、验收标准

- [x] **AC1 组件可装可体检**:在 MYIA 自管 Python 环境装上钉版本的 Agent-Reach,`agent-reach install --env local --channels bilibili`(v1.5.0 实测无 `--system` 旗标,验收实录修正)装齐 B站上游件,`agent-reach doctor --json` 报告两平台 `status: ok`(实测 bilibili/youtube 均 ok);未装环境下引擎报 `dependency_missing`(附 `pip install 'myssia[agent-reach]'` + install 命令原文提示;`myssia doctor` 经既有源健康度机制自然呈现,不新增 doctor 面)。注意 `install --env=auto`/`--safe` 只做安全检查**不真装**(grill 实测)。
- [x] **AC2 引擎契约**:`engine: agent_reach` 显式配置生效;未配置时 auto 链行为与现状逐字节一致(零存量扰动);CLI 失败(退出码非 0 **或** stderr 含 `ERROR:` 行,yt-dlp 双判据实测坑)→`agent_reach_error`、超时→`timeout`、未装→`dependency_missing`、输出不认→`agent_reach_output_unparsed`,全部结构化(测试覆盖)。
- [x] **AC3 B站源真跑**:新品类 `config/bilibili-watch.yaml` B站源(action 限 `search`/`hot`/`rank`——bili-cli 无 UP主投稿命令,grill 实测)dry-run 真跑,产出 ≥1 条结构化条目(标题/URL/UP主;**空 bvid 条目过滤**,实测坑);`classify.builtin: false`(搜索结果非七大论坛类,searxng 先例);dedup key `{url}`。
- [x] **AC4 YouTube 源真跑**:YouTube 频道源 dry-run 真跑,产出 ≥1 条结构化条目(标题/URL/频道名)。
- [x] **AC5 管线贯通**:两源条目经 dedup(以视频 URL 为锚)二次跑零重复;分类/推送走既有通道不新写一行。
- [x] **AC6 门禁全绿**:pytest 全量零新红;新增引擎测试(mock subprocess,不依赖真网);`uv.lock` 更新入库。
- [x] **AC7 文档**:品类 yaml 全节内联注释(AI 写 YAML 的参考义务);spec(python/index.md 引擎清单)与 README 相应小节更新。
- [x] **AC8 X 能力存档**:twitter-cli 免登录单条读取**已实证成立**(grill 取证,证据 `research/twitter-anon-read.yaml`,elonmusk 名推真数据零凭据);但单条读取对「监控源」形态价值弱(源要新内容流,搜索要 Cookie),**第一期不建 twitter 源**,能力存档留 enrich/detail-fetch 面后续档。本 AC 完成态=PRD 此节定案,无需实现动作。

## 六、风险与开放问题

> grill 取证(2026-10-17,证据全在 `research/`)后,原两个开放问题已闭环,
> 新增两条实测风险。

- ~~上游命令输出格式未验~~ → **已实证**:bili/twitter-cli 输出同款 YAML 骨架(`ok/schema_version/data`),yt-dlp 用 `--print` 分隔行;坑(空 bvid 条目、`-I` 限条数失效、退出码不可单信)全部固化在 `research/parsers.md`。
- ~~上游工具落盘位置未知~~ → **已实证**:落盘因安装方式而异(venv bin / `~/.local/bin`),引擎用 `shutil.which` 探测;健康检查直接消费 `agent-reach doctor --json`(每平台 `status/backends/active_backend` 一次拿齐)。
- **bili-cli 上游 2026-03 起停更**(install 输出原文):B站通道有备胎后端(OpenCLI、B站搜索 API,doctor 的 backends 列表),短期 bili-cli 免登录仍可用;若实效,该源降级停跑并如实标注,不硬闯。
- **install 的装机体验**:`--env=auto`/`--safe` 只检查不装,真装 `--env local --channels <渠道>`(v1.5.0 实测无 `--system`;可选渠道枚举不含 youtube——yt-dlp 随 pip 依赖直装)——引擎提示与文档已按实测形态修正(实施期验收实录)。
- YouTube 频道列表有 IP 配额(单 IP 低频无碍,`--playlist-end` 限条数+qps 限速兜底);本机直连实测通,遇阻再挂 proxy pool(记档不阻塞)。
