# Implement — 执行计划(有序清单)

> 每步完成勾选并回填一行实况;验证命令全部可复制直跑。
> 上下文阅读顺序:implement.jsonl 所列文件 → prd.md → design.md → 本文件。

## 第 0 步:上游实测(硬门——解析器设计的事实基础)

> **grill 取证(2026-10-17)已完成 0.1-0.5 主体**,证据在 `research/`
> (parsers.md + doctor.json + bili-search.yaml + ytdlp-flat-playlist.txt +
> twitter-anon-read.yaml);剩余项见下。

- [x] 0.1 临时 venv 装 Agent-Reach(探针 `/tmp/arprobe`,main 头仅探针允许)
- [x] 0.2 `agent-reach install --env=auto` 跑通——**实测它只做安全检查不真装**;
      落盘事实:agent-reach/yt-dlp 进 venv bin,twitter-cli 在 `~/.local/bin`
- [x] 0.3 doctor --json 全文存 `research/doctor.json`(4/16 渠道可用:
      youtube/bilibili ok,twitter warn 缺凭据,v2ex 403 需代理)
- [x] 0.4 三命令实测:bili search(YAML 骨架+空 bvid 坑)、yt-dlp
      flat-playlist(`-I` 限条数失效坑)、twitter tweet 免登录**实证成立**
- [x] 0.5 `research/parsers.md` 固化(命令/输出格式/坑/字段映射)
- [x] 0.6 **剩余**:查上游最新发布 tag(release/CHANGELOG)定 `<TAG>` 值回填
      design §2.1;在正式装机环境(自管 py)复验 doctor(B站/YouTube ok)
      — **实况(2026-10-17 第1轮)**:`gh api repos/…/releases` 实测最新
      发布 tag = **v1.5.0**(2026-06-11,非 prerelease)入 pyproject direct-
      URL;uv venv(自管 py)装 extras 后 `agent-reach doctor --json` 复验
      bilibili=ok/bili-cli、youtube=ok/yt-dlp、twitter=ok/twitter-cli。

**门:0.6 未完成不得进入第 2 步。**(已过,见上)

## 第 1 步:extras + registry + 引擎骨架(测试先行)

- [x] 1.1 `pyproject.toml` 增 `agent-reach` extras(direct-URL 钉 tag,
      含判例注释);`uv lock` 更新,`uv sync --all-extras`
      — 实况:钉 v1.5.0 zip 直装;hatchling 需 `[tool.hatch.metadata]
      allow-direct-references = true`(同轮补上);lock 增 agent-reach/
      loguru/win32-setctime/yt-dlp 四包;`uv run agent-reach --version`
      报 v1.5.0。不进 all/桌面锁(telethon/apprise 判例,PRD 约束 7)。
- [x] 1.2 `engines/agent_reach.py` 骨架:模块 docstring(契约全量,对标
      scrapling.py 的文档密度)+ 配置校验 + dependency_missing 探测
      + subprocess 骨架 + 失败语义总表全实现;**零真网调用**
      — 实况:校验选 fetch 期(credhunter/prompt 先例,渠道词表私有);
      失败语义总表 11 类全实现;env 最小化只透传 PATH/HOME;超时 kill
      兜底;解析双族(YAML 骨架/分隔行)。
- [x] 1.3 `engines/registry.py` 链外字典注册一行(带先例注释,credhunter 位)
      — 实况:feishu 后追加,注释 credhunter 先例;schema 词表同步补
      `agent_reach`(ENGINES 元组 + EngineName Literal,feishu 先例位;
      不补则品类 YAML 装载即拒——词表是 schema 门的必经面)。
- [x] 1.4 测试 `tests/engines/test_agent_reach.py`(mock
      `asyncio.create_subprocess_exec`;先例命名对齐 test_prompt_engine.py):
      校验错全矩阵 / 未装 dependency_missing / 退出码非 0 **与 stderr 含
      `ERROR:` 行双判据**→agent_reach_error / stderr 仅 WARNING 不算失败
      (twitter 实测形态)/ 超时 timeout / 输出解析失败 unparsed / YAML
      骨架 `ok: false`→error / `ok: true` 零条→合法空态 / **空 bvid 条目
      过滤**;auto 链零扰动断言(`resolve_engine` 既有测试不需改即绿)
      — 实况:47 用例全绿(夹具内嵌 research 两文件实测原文);`uv run
      pytest tests/engines/test_agent_reach.py -q` → 47 passed。
- 验证:`uv run pytest tests/engines/test_agent_reach.py -q` 绿 ✓(47 passed)

## 第 2 步:平台适配器(按 research/parsers.md 实测事实)

- [x] 2.1 bilibili search parser + 测试(fixture 用 research/bili-search.yaml
      真实输出,含空 bvid 用例)
      — 实况:YAML 骨架 parser;空 bvid 过滤计数进 WARNING 不静默;
      真跑 dry-run 实证(9 条 + 丢 1 条空 bvid 的 WARNING 落日志)。
- [x] 2.2 bilibili hot / rank(参数面按 `bili hot --help`/`bili rank --help`
      实测;~~user_videos 已证伪砍除~~——bili 命令面无 UP主投稿命令)
      — 实况:本机 `~/.local/bin/bili` 实跑两 help,均有 `-n/--max`
      (hot 另有 `-p/--page`,rank 另有 `--day [3|7]`,条数帽走 -n 即可);
      search 的 `--type video` 必带(CLI 缺省是 user 搜索,help 实读)。
- [x] 2.3 youtube channel_videos parser + 测试(fixture 用
      ytdlp-flat-playlist.txt;`--playlist-end` 限条数断言)
      — 实况:分隔行 parser 首末段切分(标题含 `|` 容错);**真跑新实锤
      坑(已回填 parsers.md 坑③):频道根 URL 被 yt-dlp 展开成多 tab,
      `--playlist-end` 是 per-playlist 帽(根 URL 下 limit 10 实跑出 25
      条),channel_url 必须用 `/videos` tab(修正后恰 10 条)**。
- 验证:`uv run pytest tests/engines/test_agent_reach.py -q` 绿 ✓(47 passed)

## 第 3 步:品类源(首批免登录档)

- [x] 3.1 新品类 `config/bilibili-watch.yaml`(B站关键词监控,首源
      `bili-ai_news` 查询词定「AI agent」;12 节全内联注释,对标
      news.yaml 的注释密度;qps ≤0.2;**品类级 `classify.builtin: false`+
      `dedup.key: "{url}"`**(searxng 先例,搜索结果非七大论坛类))
- [x] 3.2 YouTube 源:并入 bilibili-watch 或独立 `config/youtube-watch.yaml`
      (首源选一个活跃频道,执行期定;源名 `yt-<频道>` 规约;handle 先核对,
      错 handle 报 404 实测坑)
      — 实况:独立品类(与 B站节奏/watchlist 各异,便于按平台单独停跑);
      首源 `yt-anthropic`,handle `@anthropic-ai` curl 实测 200(错写
      `@AnthropicAI` 会 404);channel_url 用 `/videos` tab(坑③)。
- [x] 3.3 两品类 `--dry-run --json` 本地装载检查(schema 校验)
      — 实况:`uv run myssia run config/bilibili-watch.yaml --dry-run --json`
      → success,9 条真条目(空 bvid 1 条过滤 WARNING 落地);youtube 同款
      → success,10 条真条目。**本轮真跑条件说明**:本机 `~/.local/bin/bili`
      与 venv yt-dlp 在位故 dry-run 走了真上游;装机环境的正式真跑验收
      (第 4 步 AC3/AC4 存证)仍归第 4 步执行期。
- 验证:`uv run myssia run config/bilibili-watch.yaml --dry-run --json`
  (及 youtube 同款)零 schema 错 ✓(两文件均 status: success)

## 第 4 步:真跑验收(装机环境)

- [x] 4.1 自管 py 环境装 extras + `agent-reach install --env local
      --channels bilibili`(v1.5.0 实测**无 `--system` 旗标**——`--env=auto`/
      `--safe` 只检查不装,真装 `--env local`;验收实录修正,引擎
      UPSTREAM_INSTALL_COMMAND 已同步)
      — 实况:验收员装齐后 doctor 复验 bilibili/youtube 均 ok。
- [x] 4.2 B站源真跑 ≥1 条目(AC3);YouTube 源真跑 ≥1 条目(AC4)
      — 实况:B站 **8 条**、YouTube **10 条**(URL 锚全对
      bilibili.com/video/<bvid> 与 youtube.com/watch?v=<id>);注意正确
      调用形态是 console script `myssia run ...`(包无 `__main__.py`,
      `python -m myssia` 不通——验收员复跑纠正,实施报告在档)。
- [x] 4.3 同源二次跑 dedup(AC5):YouTube(稳定频道源)二次跑零新增 ✓;
      B站 search 是动态源,二次抓回集合本身翻新,dedup_seen 拦掉全部
      重复(交集比对验证),存活 2 条为真新视频——动态源语义下属通过;
      条目进 feed 属装机环境常驻跑(见 notCovered 声明)。
- [x] 4.4 dependency_missing 链路:受限 PATH 探针(仅子进程级,磁盘零
      改动,验后复原+正常路 dry-run/doctor 复验过)→ 结构化报错+安装
      提示原文逐字一致 ✓(提示命令措辞的 v1.5.0 参数面漂移已修,见 4.1)。

## 第 5 步:门禁 + 文档收尾

- [x] 5.1 全量门禁(CI 同款):`uv run pytest`(全量零新红)+
      `uvx ruff@0.16.10 check .`(仓库无 mypy 门禁,grill 核实 CI 实况)
      — 实况:全量 6434 passed 56 skipped(主会话亲验,含措辞修后);ruff 绿
- [x] 5.2 spec 更新:`.trellis/spec/python/index.md` 引擎清单/依赖节补
      agent-reach 一行(trellis-update-spec 流程)
- [x] 5.3 README(如有引擎表)与品类 yaml 注释复核;research/ 样例文件
      与实现一致(格式漂移则回填 parsers.md)
- [ ] 5.4 提交:代码与 uv.lock 一笔;品类 yaml 一笔;任务档一笔
      (混线文件分离纪律);`gitnexus detect-changes --scope staged`
      核受影响面(文档/配置类豁免判例适用与否如实)

## 回滚点

- 单向新增:任一步翻车 `git revert` 对应提交即净;品类 yaml 删除即停跑;
  引擎文件删除+registry 一行回退 = 完整卸载,零存量残留。
