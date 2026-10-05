# SearXNG 搜索式情报源——接口探查 research

> **状态:文档取证草案——未实测,docker 前置未满足。**
> AC1 降级口径:prd.md:63-64「AC 门控:无 docker 环境则 fixture 充分+真跑
> 留部署后」;本稿接口形状全部从 SearXNG 官方材料核对(非猜测),凡属
> 「文档口径、未经本机实例验证」处均逐段标注,**实现批开工前须先按 §8
> 清单真跑补齐快照**。
>
> 取证时点:2026-10-05(深夜)。材料源(经 zread 逐文件读取 GitHub
> `searxng/searxng` master 分支):`searx/settings.yml`、`searx/webapp.py`、
> `searx/webutils.py`、`searx/result_types/_base.py`、`searx/limiter.py`、
> `searx/limiter.toml`、`container/docker-compose.yml`、
> `container/settings.template.yml`、官方文档 `docs/dev/search_api.rst`、
> `docs/admin/api.rst`、`docs/admin/searx.limiter.rst`、
> `docs/admin/installation-docker.rst`(线上对应 docs.searxng.org)。
>
> AGPL 边界(prd.md:16-19 判例):MYIA 只把 SearXNG 当自托管 HTTP 服务消费,
> 本稿引用仅为其配置事实与接口契约描述,零代码复用。

## 0. 为什么未实测——本机 docker 前置探查回执(2026-10-05)

| 检查 | 命令 | 结果 |
|---|---|---|
| docker CLI | `docker version` | `command not found: docker` |
| PATH 中的 docker 符号链接 | `ls -la /usr/local/bin/docker` | 符号链接存在但**悬空**:`-> /Applications/Docker.app/.../docker` |
| Docker Desktop 应用 | `ls /Applications/Docker.app` | `No such file or directory`(应用已卸载,残留符号链接) |
| 直连悬空链接 | `/usr/local/bin/docker version` | `no such file or directory` |
| docker socket | `ls /var/run/docker.sock` | 不存在 |
| 替代运行时 | `which colima podman nerdctl` | 全部 not found |
| 容器数据目录 | `ls ~/.docker ~/.colima ~/.orbstack` | 全部不存在 |

结论:**本机无任何容器运行时可用**(Docker Desktop 已卸载干净,仅剩
`/usr/local/bin` 残留悬空链接)。探查段真跑(compose 起实例+接口快照)
不可执行,按档内 AC 门控降级;恢复路径=装回 Docker Desktop(或
colima)后,§1 步骤原样可跑,§8 清单即补齐项。

## 1. 起一个开 json 的实例(compose 步骤,官方口径)

来源:`docs/admin/installation-docker.rst`(Compose instancing 节)+
`container/docker-compose.yml` + `container/settings.template.yml`。

```sh
# 1) 建环境(官方步骤)
mkdir -p ./searxng/core-config/ && cd ./searxng/
curl -fsSL \
  -O https://raw.githubusercontent.com/searxng/searxng/master/container/docker-compose.yml \
  -O https://raw.githubusercontent.com/searxng/searxng/master/container/.env.example
cp -i .env.example .env   # 按需改(单机自用可不动)

# 2) 写 ./searxng/core-config/settings.yml(最小覆盖,见下)
# 3) 起服务
docker compose up -d
```

`core-config/settings.yml`(在官方模板 `use_default_settings: true`
基础上只加 `search.formats`——**json 开启就这一处**):

```yaml
use_default_settings: true   # 其余全继承官方默认,只覆盖下面几项

search:
  # 官方默认 formats: [html](settings.yml「remove format to deny
  # access」);要让 /search 出 json 必须显式加:
  formats: [html, json]

server:
  secret_key: "<随机串>"      # env SEARXNG_SECRET 可代;不自用调试可暂用占位
  # limiter 不写 = 默认 false(见 §5,自托管 MYIA 专用实例建议保持默认)
```

端口对齐:容器内监听 **8080**(compose 默认 `${SEARXNG_PORT:-8080}`);
官方手动例 `-p 8888:8080` → 宿主 `http://127.0.0.1:8888`,与 prd.md:40
的缺省 `searxng_base_url=http://127.0.0.1:8888` 正好对齐。卷:
`/etc/searxng`(配置,即 core-config 挂载点)+ `/var/cache/searxng`
(favicon 缓存等)。compose 里附带一个 `valkey` 服务(limiter 才需要,
默认不开 limiter 时它是闲着的,可整段删掉减一个容器)。

## 2. GET /search 接口形状(文档口径,未实测)

端点(来源 `docs/dev/search_api.rst`):`GET|POST /` 与 `GET|POST /search`
等价(`/` 带 q 会 308 跳 `/search`);GET 用 URL 查询参数。

### 2.1 请求参数

| 参数 | 取值 | 说明 |
|---|---|---|
| `q` | 必填 | 查询词;支持各上游语法(如 `site:github.com SearXNG`) |
| `format` | `json`/`csv`/`rss` | **须在 settings 激活,未激活返回 403 Forbidden**;不传=html |
| `pageno` | 整数,缺省 1 | 搜索页码(**注意:是 `pageno`,不是 `p`**) |
| `language` | 语言码 | 缺省取 `search.default_lang`(官方默认 `auto`)。prd 示例的 `zh-CN` 属 SearXNG locale 集合,接受面待实测确认(§8-⑤) |
| `safesearch` | `0`/`1`/`2` | 0 None / 1 Moderate / 2 Strict,缺省取 `search.safe_search`(默认 0);仅对支持的上游生效 |
| `categories` | 逗号分隔 | 缺省 general(聚合多引擎) |
| `time_range` | `day`/`month`/`year` | 可选,仅支持的上游生效 |

**prd 纠偏 ①**:prd.md:26 写 `&p=<页>`——实际参数名是 **`pageno`**
(search_api.rst ``pageno`` : default ``1``)。

示例调用(prd.md:26 修正版):

```
GET {base_url}/search?q=<关键词>&format=json&language=zh-CN&safesearch=1&pageno=1
```

### 2.2 响应 JSON 形状(当前 master,来源 `webapp.py`→`webutils.get_json_response`)

顶层六个键(**没有 `number_of_results` 顶层字段**——当前 master 已无):

```json
{
  "query": "<原始查询词>",
  "results": [ <Result 字典>, ... ],          // 合并去重后的有序结果
  "answers":   [ ... ],                        // 直接答案(计算器等),常空
  "corrections":[ ... ],                       // 拼写纠正词,常空
  "infoboxes": [ ... ],                        // 侧栏知识卡,常空
  "suggestions":[ ... ],                       // 联想词,常空
  "unresponsive_engines": [ ["引擎名","错误文案"], ... ]  // 挂掉的上游,非错误
}
```

`results[]` 元素= `Result.as_dict()`(`searx/result_types/_base.py`
MainResult 全字段;实际响应里以 LegacyResult 字典出,标准键必有默认、
上游可带附加键)。MYIA 关心的字段(**加粗=映射目标**):

| 字段 | 类型 | 说明 |
|---|---|---|
| **`url`** | str\|null | 结果链接(**条目 url**;无 scheme 会补 http) |
| **`title`** | str | 标题(**条目 title**;空白已归一) |
| **`content`** | str | 摘要/描述(**条目 content**;可为空串;与 title 相同时被置空) |
| `publishedDate` | isoformat 字符串\|null | 发布日期,**多数 general 上游不给=null**(注意驼峰单数) |
| `engines` | str 数组 | 命中该结果的 SearXNG 上游引擎名集合(set 序列化) |
| `engine` | str | 首发引擎名(合并后可能为空) |
| `score` / `positions` | float / int 数组 | 聚合排名元数据 |
| `template` | str | 渲染模板名(网页结果=`default.html`;非 default 即特殊类结果如图片/视频,MYIA 可按此过滤只要网页结果) |
| `parsed_url` | 数组 | urlparse 六元组序列化(用途不大,url 已够) |
| 其余 | — | `img_src`/`thumbnail`/`author`/`metadata`/`length`/`views`/`priority`/`category`/`open_group`/`close_group`/`pubdate`(deprecated) |

序列化规则(`webutils.JSONEncoder`):datetime→isoformat、set→list、
timedelta→秒数;`publishedDate` 为 null 时输出 null。

**prd 纠偏 ②**:prd.md:27 写 `publisheddates 可空`——实际字段名是
**`publishedDate`**(驼峰单数),且 `results[].content` 就是摘要,没有
`result.abstract` 字段。

### 2.3 示例响应骨架(文档推导,**未实测**,真跑批以实快照替换)

```json
{
  "query": "竞品 发布",
  "results": [
    {
      "url": "https://example.com/news/1",
      "engine": "duckduckgo",
      "parsed_url": ["https","example.com","/news/1","","",""],
      "template": "default.html",
      "title": "示例标题",
      "content": "示例摘要……",
      "img_src": "", "iframe_src": "", "audio_src": "", "thumbnail": "",
      "publishedDate": null, "pubdate": "",
      "length": null, "views": "", "author": "", "metadata": "", "priority": "",
      "engines": ["duckduckgo", "bing"],
      "open_group": false, "close_group": false,
      "positions": [1, 2], "score": 5.0, "category": ""
    }
  ],
  "answers": [], "corrections": [], "infoboxes": [], "suggestions": [],
  "unresponsive_engines": [["google", "CAPTCHA"]]
}
```

## 3. 分页语义(文档口径)

- `pageno` 从 1 起,整数;逐页对**所有支持 paging 的上游**取第 N 页再聚合
  (settings.yml `search.max_page: 0`=不设限,各引擎自身有页数上限,
  如 Google 系到十余页即空)。
- 页与页之间是**上游语义分页**(非偏移量),深页结果质量陡降且对上游
  放大请求;prd.md:36-38 的形态(逐词**一页**+interval ≥1800s)与该
  语义匹配。
- **建议(实现批采纳,真跑批佐证)**:每词固定 `pageno=1` 一页。
  general 类一页即多引擎合并去重后的结果(典型 20-30 条),对「关键词
  日报」足够;翻页深挖留给边界(不做)。

## 4. 空结果 / 坏参数 / 错误形态(来源 `webapp.py` /search 路由)

| 场景 | HTTP | 响应体 |
|---|---|---|
| 正常但零结果(冷门词/全上游空) | 200 | `{"query":..., "results": [], ...}`(空数组,不报错) |
| 部分/全部上游挂 | 200 | 正常 200,失败上游只进 `unresponsive_engines` 数组(译文文案) |
| 缺 `q` 且 format=json | 400 | `{"error": "No query"}` |
| 参数形态坏(如 pageno 非整数) | 400 | `{"error": "<SearxParameterException 消息>"}` |
| `format=json` 未在 settings 激活 | **403** | Flask 默认 HTML 错误页(**非 JSON**;MYIA 引擎侧应特判 403=部署侧没开 json,报错文案直指 settings.yml) |
| limiter 拦截(仅启用时) | 429 | 文本体(见 §5) |
| 实例内部错误 | 500 | `{"error": "search error"}`(JSON,gettext 翻译后) |

能力探测面:`GET /config` 返回 engines/categories/limiter.enabled 等
(`docs/admin/api.rst`),doctor/装机排障可用一行 curl 判断「实例活着吗、
json 开了吗(403 与否)、limiter 开了吗」;`GET /healthz` 恒 200 文本 OK。

## 5. 限流口径(limiter / 机器人检测默认态)

默认态结论:**官方默认不开**(settings.yml `server.limiter: false` 且
`valkey.url: false`→limiter 模块不挂 before_request,零请求被拦)。

机制(来源 `searx/limiter.py` + `docs/admin/searx.limiter.rst`):

- 启用=两件套:`server.limiter: true` **且** 配好 valkey(`valkey.url`/
  env `SEARXNG_VALKEY_URL`);缺 valkey 时仅记 error 日志照常跑(除非
  `public_instance: true` 强制要求并 exit 1)。
- 启用后 `/search` 上依次探测:http_accept / http_accept_encoding /
  http_accept_language / **http_user_agent** / http_sec_fetch / ip_limit;
  `ip_lists` 的 pass 列表优先于一切(pass 命中连 UA 检查都跳过);
  link-local 地址直通。limiter.toml 默认:`link_token=false`、
  `pass_searxng_org=true`、无自定义 pass/block 列表。
- env 覆盖通道:`SEARXNG_LIMITER` / `SEARXNG_PUBLIC_INSTANCE`
  (settings.yml server 节注释)。

**对 MYIA 的口径(实现批照此写)**:

1. 自托管 MYIA 专用实例(绑 127.0.0.1/内网,无公网暴露)→ **保持
   limiter 默认 false**,不给自家采集加拦截面;这与「自家实例策略=允许
   自家采集」的 robots 立场(§6)一致。
2. 若实例同时对外(public_instance)必须开 limiter → MYIA 客户端要么进
   `limiter.toml` 的 `pass_ip` 列表,要么带全 Accept 系头+常规 UA
   (httpx 默认头缺 Accept-Language,可能被 probe 拦成 429)——探查批
   真跑时顺带验证(§8-④)。
3. MYIA 侧礼貌间隔不因自托管省略(prd.md:38):interval ≥1800s+逐词
   串行+页间延时——上游元搜索的礼貌由 SearXNG 聚合层承担(其自带
   `ban_time_on_fail`/`suspended_times` 熔断:CAPTCHA 1h、429 3min、
   cloudflare CAPTCHA 15 天等),MYIA 不放大。

## 6. robots 口径

实例内置 `robots.txt`(webapp.py 路由原文):

```
User-agent: *
Allow: /info/en/about
Disallow: /stats
Disallow: /image_proxy
Disallow: /preferences
Disallow: /*?*q=*
```

即 SearXNG 默认对外来爬虫**禁搜**(`/*?*q=*` 覆盖一切搜索请求)——
这正是「公共实例明禁 API 滥用」(prd.md:79-80 红线)的服务端体现,
也是 MYIA 只走自托管、不代理公共实例的依据。

**自家实例策略=允许自家采集**(prd.md:29-31):MYIA 采集的是主人自己
部署的实例,robots 管的是第三方爬虫,实例主人(=MYIA 使用者本人)对
自家流量自授权;上游(真正的搜索源)的礼貌由 SearXNG 聚合层统一承担
(§5-3),MYIA 端再加间隔不放大。此口径随探查批落进引擎模块文档
(同 reddit 官方 API 引擎「robots 面不适用钉死端点」的论证形态,
registry.py:121-125 先例)。

## 7. 对实现段的落地指导(锚点既有层)

- **注册形态**:链外源引擎,同 `reddit` 先例(src/myssia/engines/
  registry.py:121-125)——`ENGINE_REGISTRY` 加一行 `"searxng"`,**不进**
  `AUTO_CHAIN`(registry.py:83-91),显式 `engine: searxng` 才生效,
  auto 永不路过(搜索型源没有「降级链」语义,坏了就是本源结构化失败)。
- **base_url 缺省+env**:`searxng_base_url` 缺省 `http://127.0.0.1:8888`,
  env `MYIA_SEARXNG_URL` 覆盖——同 firecrawl 先例(src/myssia/engines/
  firecrawl.py:46-48 `ENV_FIRECRAWL_URL`/`DEFAULT_FIRECRAWL_ENDPOINT`)。
- **条目映射**:`{url: r["url"], title: r["title"], content: r["content"]}`
  (content 可空串);`publishedDate` 非空 isoformat 时透传,否则 None;
  可选过滤 `template != "default.html"` 的特殊结果(图片/视频卡)。
  坏行跳过(缺 url/title)沿用 fetch 层既有 skip 口径。
- **错误面**:非 2xx→`FetchError`(http_<status> 同 firecrawl.py:18-20);
  **403 特判**=「实例未开 json format」部署侧提示;400/5xx 透传
  `error` 字段;连接拒绝=「searxng 实例未起」结构化失败(同 firecrawl
  自托管死服务优雅降级口径,firecrawl.py:13-15)。
- **零凭据**:queries 明文非凭据可落 YAML(prd.md:81 红线),无 env/
  keychain 面,比 firecrawl 更简。
- **fixture 基准**:§2.3 骨架即测试夹具蓝本(六用例:正常多词多结果/
  空 results/坏行/pageno 语义/env 两态/schema queries 必填),真跑批
  换实快照对齐。

## 8. 待 docker 批实测补齐清单(AC1 真跑项,docker 恢复后照单执行)

1. compose 起实例(§1 步骤),curl `/healthz`+`/config` 确认活+json 开。
2. `GET /search?q=<示例词>&format=json&language=zh-CN&safesearch=1
   &pageno=1` 实快照落 evidence(date 戳);对照 §2.2/§2.3 逐字段核。
3. 三态实拍:未开 json 的 403(改回默认 settings 复现)/ 缺 q 的 400 /
   冷门词空 results 200;`pageno=2` 是否有增量(佐证 §3 一页建议)。
4. limiter 两态:默认 false 直连;开 true+valkey 后 httpx 默认头是否
   429、补 Accept-Language 后是否过(§5-2 口径定案)。
5. `language=zh-CN` 接受面实测(§2.1 待确认项)。
6. 查询词示例集(关键词日报骨架用):中文舆情词×2、竞品词×1、事件词×1,
   各取实快照前 3 条(脱敏后)入 evidence。
7. 20 条入库截图(prd.md:62 验证项)随实现批一起做。
