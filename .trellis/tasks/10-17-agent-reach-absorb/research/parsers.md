# 上游实测固化(grill 取证,2026-10-17,临时 venv /tmp/arprobe 探针)

> 本文件是 parsers/命令面的事实依据;格式若与实现期上游新版不符,以实测
> 重跑为准并回填本文件。

## 安装与落盘(实测)

- `pip install 'agent-reach @ https://github.com/Panniantong/agent-reach/archive/main.zip'`
  直装成功;**PyPI 同名包为假冒**(上游官方警告)。
- 落盘因安装方式而异:`agent-reach`/`yt-dlp` 进 venv bin;本机既有
  `~/.local/bin/twitter`(用户级)。**结论:引擎用 `shutil.which` 探测,
  不硬编码路径。**
- `agent-reach install --env=auto` **只做安全检查不真装**(输出原文
  "Safe mode check complete. No changes were made. 4/16 channels active");
  真装需显式授权(`--system` / `--env=local --system`)。
- `agent-reach doctor --json`:每平台 `{status, name, message, tier,
  backends[], active_backend}`;全平台一次拿齐(比逐 CLI 散测稳)。
  全文存 `doctor.json`。

## doctor 快照(2026-10-17 本机,4/16 可用)

| 平台 | status | active_backend | 备注 |
|---|---|---|---|
| youtube | ok | yt-dlp | 免配置 |
| bilibili | ok | bili-cli | **上游 2026-03 起停更**(install 输出原文);备胎后端:OpenCLI、B站搜索 API |
| rss / web | ok | feedparser / Jina Reader | 与 MYIA 现有能力重复,不吸收 |
| twitter | warn | null | twitter-cli 已装缺显式凭据;**但单条读取免登录实测成立**(下) |
| reddit/小红书/xueqiu | warn | null | 需 Cookie,第一期不做 |
| v2ex | warn | null | 本机直连 403(需代理) |

## 命令与输出格式(实测固化)

### bilibili — `bili search "query" --type video -n <N>`

输出 = **YAML**,骨架 `ok/schema_version/data[]`(证据 `bili-search.yaml`):

```yaml
ok: true
schema_version: '1'
data:
- id: BV1xwVr6FEh4
  bvid: BV1xwVr6FEh4
  title: ...
  author: AI大模型码农
  play: 1205203
  duration: '1353:6'
```

坑(实测):
1. **存在 bvid 为空的条目**(第三条 `bvid: ''`)——解析必须过滤,无法构造
   dedup 锚;条目 URL = `https://www.bilibili.com/video/<bvid>`。
2. bili 命令面**没有 UP主投稿列表**;免登录可用 = `search` / `hot`(热门)
  / `rank`(排行);`feed/favorites/history` 等均需扫码登录;写操作命令
  (`like/coin/dynamic-post`)存在但链接者铁律不碰。

### twitter — `twitter tweet <URL>`(免登录单条读取,**实测成立**)

- 证据 `twitter-anon-read.yaml`:elonmusk 名推真数据(id/text/author/
  metrics 全回来),**零凭据**。
- stderr 带 `WARNING twitter_cli.client: Failed to init ClientTransaction`
  但 `ok: true` 照常——**stdout 是判据,stderr WARNING 不是失败**。
- 输出同款 YAML 骨架(bili/twitter-cli 同族契约,parser 可共享骨架)。
- 形态判断:单条读取对「监控 feed 源」价值弱(源要的是新内容流,搜索要
  Cookie);真正价值在 enrich/detail-fetch(给已有条目追抓推文上下文)——
  第一期不建 twitter 源,能力存档留 enrich 面。

### youtube — `yt-dlp --flat-playlist --print "%(id)s|%(title)s|%(channel)s" <频道URL>`

- 输出 = 自定义分隔行 `DdCEmlAydcw|Inside ...|NA`(证据
  `ytdlp-flat-playlist.txt`);成功时 exit=0、stderr 空。
- 坑(实测):
  1. **`-I 1:3` 与 `--print` 组合不可靠**(实测限制失效打出 9 条)——
     限条数用 `--playlist-end <N>`。
  2. 错误 handle(404)时 stderr 出现 `ERROR: [youtube:tab] ...` 行;
     **退出码不可单信**(yt-dlp 各版本失败退出码行为不一)——解析一律
     双判据:退出码非 0 **或** stderr 含 `ERROR:` 行 → 失败。
  3. **频道根 URL 会被展开成多 tab**(2026-10-17 真跑实锤,首轮门禁
     发现):`@anthropic-ai` 根 URL 下 `--playlist-end 10` 实跑出 25 条
     (Videos/Shorts/Live 各算一个 playlist,`--playlist-end` 是
     per-playlist 帽);投稿监控必须用 `/videos` tab URL
     (`@anthropic-ai/videos` 实测恰出 10 条)。Shorts/Live 另开源再配。
- 频道 handle 要核对(如 Anthropic 官方是 `@anthropic-ai` 不是
  `@AnthropicAI`,错 handle 报 404)。

## 网络环境备注

- 本机直连:B站/twitter/x.com OK;YouTube 本次实测经直连成功(视频页
  API);上游文档提 Reddit/Twitter 可能需代理——MYIA 侧源级 `proxy:`
  基座已备,第一期 B站/YouTube 直连,遇阻再挂 pool(记档不阻塞)。
