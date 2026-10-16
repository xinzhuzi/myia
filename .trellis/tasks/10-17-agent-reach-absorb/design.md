# Design — agent_reach 引擎(链外)技术设计

> 对应 prd.md。先例锚:`engines/credhunter.py`(链外首例)、`engines/saas.py`
> (gates/keychain 纪律)、`engines/scrapling.py`(extras 惰性探测+结构化缺装)、
> `engines/tg_web.py`(外部进程组件形态)。实现者动手前先读上述四个文件的
> 模块 docstring——本设计不重复其内容,只写差异。

## 1. 总体形态

```
config/<品类>.yaml          (源: engine: agent_reach + engine_options.agent_reach)
        │
        ▼
engines/registry.py         ("agent_reach": _load(...)) ← 链外字典(credhunter 先例位)
        │
        ▼
engines/agent_reach.py      AgentReachEngine(BaseEngine)
        │  asyncio.create_subprocess_exec → 上游 CLI(bili / yt-dlp / twitter)
        ▼
结构化条目 [{title,url,author,published,...}] → 既有管线(classify→dedup→push)
```

- **链外引擎**:显式 `engine: agent_reach` 才生效;`resolve_engine` 的 auto 链
  与 `AUTO_CHAIN` 常量零改动;失败=源级结构化 FetchError,不降级不拦品类。
- **MYIA 核心不 import agent-reach**:引擎零第三方 import(subprocess 是标准库),
  extras 只影响「装不装得上上游 CLI」,不影响核心装载——比 scrapling 的
  惰性 import 更进一步(连惰性 import 都不需要)。

## 2. 组件接入面

### 2.1 extras 定义(pyproject.toml)

```toml
# Agent-Reach 互联网能力路由器(10-17-agent-reach-absorb):官方警告 PyPI
# 同名包为假冒,direct-URL 钉 tag 直装 GitHub archive(真锁纪律,main 漂移
# 头禁用);上游工具(bili-cli/yt-dlp/twitter-cli)经 agent-reach install 装入。
agent-reach = ["agent-reach @ https://github.com/Panniantong/agent-reach/archive/<TAG>.zip"]
```

- `<TAG>` 执行期取发布 tag 最新值;uv.lock 会把 direct-URL 依赖连内容哈希锁死。
- 本机同步纪律:裸 `uv sync` 会卸 extras,一律 `uv sync --all-extras`(既有判例)。

### 2.2 上游工具安装与探测(grill 实测修订)

- 安装序列(用户侧/装机钩子,非引擎职责;v1.5.0 实测参数面修正):
  `pip install 'myssia[agent-reach]'` → `agent-reach install --env local
  --channels bilibili`(真装;`--env=auto` 与 `--safe` 均只做安全检查零改动,
  grill 实测原文 "No changes were made";可选渠道枚举不含 youtube,
  yt-dlp 随 pip 依赖直装)→ `agent-reach doctor --json` 体检。
- 引擎探测(fetch 前零网络检查):`shutil.which("agent-reach")` /
  `which("bili")` / `which("yt-dlp")` 任一缺位 → `dependency_missing`,
  message 附 extras 安装命令 + install 命令原文。
- **落盘位置实测**:因安装方式而异(`agent-reach`/`yt-dlp` 进 venv bin,
  twitter-cli 在用户级 `~/.local/bin`)——不硬编码路径,`shutil.which` 是
  唯一探测面;若需全平台健康检查,直接消费 `agent-reach doctor --json`
  (每平台 `{status, backends, active_backend}` 一次拿齐,不逐 CLI 散测)。

## 3. 引擎契约(engines/agent_reach.py)

### 3.1 源配置面(12 节契约内)

```yaml
sources:
  - name: bili-ai_news                    # <平台>-<渠道> 命名规约,全局唯一
    engine: agent_reach
    url: "agent-reach://bilibili"         # 身份标识不参与请求(schema url 必填,
                                           # searxng 先例:其 url 同款「身份标识
                                           # 不参与请求」语义注记)
    engine_options:
      agent_reach:
        channel: bilibili                 # bilibili | youtube
        action: search                    # bilibili: search|hot|rank;youtube: channel_videos
        query: "AI agent"                 # action=search 必填
        # channel_url: "https://www.youtube.com/@xxx"  # channel_videos 必填
        limit: 10                         # 单次条数帽,缺省 10,1-50
    # 无 extract 节——本引擎结构化拒 extract(REQUIRES_EXTRACT=False:
    # 上游输出是结构化 YAML/分隔行而非 HTML,字段归一(title/url/author)
    # 硬编码在 parser 内,css/json_path 语义不适用;配 extract 即
    # extract_unsupported 结构化拒)——实施期复查修正,与本节原示例的
    # extract 映射漂移已对齐实现
    rate_limit:
      qps: 0.2                            # 配额敏感平台,礼貌档必配
    proxy: direct                         # 本机直连实测通;遇阻挂 pool(基座已备)
```

品类级配套(品类 yaml 顶层,searxng/news 先例):`classify.builtin: false`
(B站搜索结果不属于七大论坛类,内置扫描关掉直通);`dedup.key: "{url}"`。

- `engine_options.agent_reach` 校验错→`invalid_channel` / `invalid_action` /
  `invalid_limit` / `missing_query`(action=search 缺 query)/
  `missing_channel_url`(channel_videos 缺 channel_url)(结构化,schema
  装载期或 fetch 期按既有各引擎先例的位置统一)。
- pagination 不支持(单次语义,同 searxng 先例);`pagination:` 出现即
  `invalid_pagination`。

### 3.2 subprocess 调用纪律

- `asyncio.create_subprocess_exec`(绝不用 shell=True;参数列表显式构造,
  query 等值不经 shell 拼接)。
- 整个调用包 `asyncio.wait_for`,超时帽 `engine_options.agent_reach.timeout`
  (缺省 60s,5-300)→ `timeout`。
- **环境最小化**:子进程 env 只透传 `PATH`/`HOME`(上游 CLI 需要定位
  `~/.agent-reach/`),其余 env 一律不传(凭据零泄漏面)。
- **失败双判据(grill 实测坑)**:退出码非 0 **或** stderr 含 `ERROR:` 行
  (yt-dlp 失败时退出码行为跨版本不可单信)→ `agent_reach_error`,stderr
  原文截断入 message;**stderr 的 `WARNING` 行不是失败**(twitter-cli 实测
  免登录读取时必带 ClientTransaction WARNING 但 `ok: true` 照常出数据)。
- stdout 解析后条目数为 0:上游骨架 `ok: false` → `agent_reach_error`;
  `ok: true` 零条 → 合法空态零条目(源没更新不是故障,同 urlwatch 的
  unchanged 语义)。

### 3.3 输出解析(grill 实测固化,证据 research/parsers.md)

两族输出、每 channel 一个 parser 函数(新增 channel 不改引擎骨架):

- **YAML 骨架族**(bili-cli / twitter-cli 同族契约):
  `ok: true / schema_version: '1' / data: [{...}]`——PyYAML(core 既有六
  依赖之一)直接 `yaml.safe_load`,读 `ok` 与 `data[]`。
  **必过坑:bili search 实测存在 `bvid: ''` 空条目,无锚即弃**(计入
  解析统计,不静默)。
- **分隔行族**(yt-dlp):`--print "%(id)s|%(title)s|%(channel)s"` 自定义
  分隔行,逐行 split;**限条数用 `--playlist-end <N>`**(`-I 1:3` 与
  `--print` 组合实测失效,打出 9 条)。
- 解析失败 → `agent_reach_output_unparsed`(样例前 200 字节入 message,
  留升级上游格式的余地)。

### 3.4 失败语义总表

| error_type | 触发 | 消息要点 |
|---|---|---|
| `dependency_missing` | agent-reach 或上游 CLI 缺位 | 安装命令原文 |
| `invalid_channel`/`invalid_action`/`invalid_limit`/`missing_query`/`missing_channel_id`/`invalid_pagination` | 配置错 | 指向 yaml 键 |
| `agent_reach_error` | CLI 退出非 0 | stderr 截断 |
| `agent_reach_output_unparsed` | 输出不认 | 样例字节截断 |
| `timeout` | 超时帽 | 命令与帽值 |

robots 面:平台官方 API/CLI 通道,同 reddit 引擎先例论证(授权通道,
robots.txt 不适用于钉死的官方端点);礼貌由 qps 限速承担。

## 4. 平台适配器(第一批,grill 实测后定案)

| channel | action | 上游命令(实测固化) | 条目锚 | 备注 |
|---|---|---|---|---|
| bilibili | search | `bili search "<query>" --type video -n <limit>` | `https://www.bilibili.com/video/<bvid>` | 免登录;空 bvid 条目过滤;**B站禁用 yt-dlp**(上游明令) |
| bilibili | hot / rank | `bili hot` / `bili rank`(参数面执行期按 `bili <cmd> --help` 定) | 同上 | 免登录;全站热门/排行,天然 feed 形态 |
| youtube | channel_videos | `yt-dlp --flat-playlist --print "%(id)s\|%(title)s\|%(channel)s" --playlist-end <limit> <channel_url>` | `https://www.youtube.com/watch?v=<id>` | 免登录;`--playlist-end` 限条数;字幕提取归 enrich 面不做 |

**已证伪/移出的形态**(grill 实测):
- ~~bilibili `user_videos`(UP主投稿列表)~~——bili 命令面无此命令
  (`feed/favorites` 等均需扫码登录),**砍**;UP主监控留待上游备胎后端
  (OpenCLI/B站搜索 API)或登录态后续档。
- ~~twitter channel~~——免登录单条读取实证成立(`research/twitter-anon-read.yaml`)
  但监控源形态价值弱,不建源;归 enrich/detail-fetch 面后续档(PRD AC8)。

条目归一字段:bilibili `title/author/url(bvid 拼接)/play/duration`;
youtube `title/url(id 拼接)/channel`;`published` 两平台 flat 输出均无
(不做假数据,模板不显示时间或后续 enrich)。

## 5. 权衡记录(备选与否决理由)

- **否决:import agent-reach 当库用**——上游定位是 CLI 路由器,库 API 非其
  稳定契约;subprocess 面就是它给 Agent 的官方面(SKILL.md 明示),跟着
  官方面走升级成本最低。
- **否决:进 AUTO_CHAIN 降级链**——平台语义读取与「URL→HTML」的降级链
  语义不同构,混入会让 auto 链的零结果探测逻辑污染;链外是 credhunter 起
  全部特殊引擎的一致裁决。
- **否决:Exa/Jina 通道**——与 searxng/static_html 重复(复用已有资产)。
- **回滚**:纯新增(引擎文件+registry 一行+extras 一行+品类 yaml),零存量
  文件行为改动;revert 单提交即净。uv.lock 变更随同提交。
