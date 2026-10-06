# SearXNG 搜索式情报源——接口探查 research

> **状态:已实测(2026-10-06 colima 解锁后 §8 清单真跑落 evidence,结案)。**
> 演进:2026-10-05 深夜文档取证草案(81d5110 入库,当时本机无容器运行时,
> §0 五步探查回执)→ 2026-10-06 docker 解锁(brew colima+docker+compose,
> 主人「剩下的问题全部做完」令+余量表授权)→ 本稿=草稿全量保留+实测数据
> 回填+挂点定案(§9)。凡「文档口径」段落的实测命中情况在 §8 逐项标注;
> 两处 prd 纠偏(pageno/publishedDate)均经实例证实。
>
> 取证时点:2026-10-05 文档 / 2026-10-06 实测。材料源(经 zread 逐文件读取
> GitHub `searxng/searxng` master 分支):`searx/settings.yml`、
> `searx/webapp.py`、`searx/webutils.py`、`searx/result_types/_base.py`、
> `searx/limiter.py`、`searx/limiter.toml`、`container/docker-compose.yml`、
> `container/settings.template.yml`、官方文档 `docs/dev/search_api.rst`、
> `docs/admin/api.rst`、`docs/admin/searx.limiter.rst`、
> `docs/admin/installation-docker.rst`。实测实例:searxng/searxng:latest
> = **2026.10.4+d48c4b555**(colima docker 29.8.2/29.5.2,aarch64)。
>
> AGPL 边界(prd.md:16-19 判例):MYIA 只把 SearXNG 当自托管 HTTP 服务消费,
> 本稿引用仅为其配置事实与接口契约描述,零代码复用(实测亦只经 HTTP 探针,
> 未拷贝其任何源码进 MYIA)。

## 0. 本机 docker 前置(2026-10-05 受阻 → 2026-10-06 解锁)

2026-10-05 深夜五步探针(receipt 在 81d5110 版 §0):docker/colima/podman/
orbstack 全无,Docker.app 已卸载——探查降级为纯文档取证。2026-10-06 本轮
docker 解锁后实测可用态:`docker info` Client 29.8.2(Context: colima)/
Server 29.5.2(colima VM aarch64,4CPU/8GiB/60GiB),`docker compose
version` 5.6.0。

**坑①(colima 部署陷阱,生产注记)**:最初按计划把 compose 目录放
`/tmp/searxng-probe`——bind mount 源路径在 macOS `/tmp`,而 **colima 默认
只共享家目录**,VM 内 `/tmp` 是本地空目录:容器看不到 settings.yml,
entrypoint 日志 `"/etc/searxng/settings.yml" does not exist, creating from
template` → 从镜像模板重建(**无 search.formats**)→ json 静默关闭 →
一切 `format=json` 403。迁移到 `~/.searxng-probe`(家目录=colima 默认
共享)后即刻正常。Docker Desktop 无此问题;凡 docker-in-VM(colima/
lima 类)部署,compose 目录必须放守护进程可见共享路径。

## 1. 起一个开 json 的实例(compose 步骤,官方口径+实测通过)

来源:`docs/admin/installation-docker.rst`(Compose instancing 节)+
`container/docker-compose.yml` + `container/settings.template.yml`。
**实测原样可跑**(2026-10-06,唯一改动=目录在家目录+`.env` 里
`SEARXNG_PORT=8888`):

```sh
# 1) 建环境(官方步骤)
mkdir -p ./searxng/core-config/ && cd ./searxng/
curl -fsSL \
  -O https://raw.githubusercontent.com/searxng/searxng/master/container/docker-compose.yml \
  -O https://raw.githubusercontent.com/searxng/searxng/master/container/.env.example
cp -i .env.example .env   # 单机自用可不动;MYIA 对齐加 SEARXNG_PORT=8888

# 2) 写 ./searxng/core-config/settings.yml(最小覆盖,见下)
# 3) 起服务
docker compose up -d
```

`core-config/settings.yml`(官方模板 `use_default_settings: true` 基础上
只加 `search.formats`——**json 开启就这一处**;实测生效判据=容器内
`cat /etc/searxng/settings.yml` 与宿主原件一致+`format=json` 200):

```yaml
use_default_settings: true   # 其余全继承官方默认,只覆盖下面几项

search:
  # 官方默认 formats: [html];要让 /search 出 json 必须显式加:
  formats: [html, json]

server:
  secret_key: "<随机串>"      # env SEARXNG_SECRET 可代
  # limiter 不写 = 默认 false(见 §5,自托管 MYIA 专用实例建议保持默认)
```

端口对齐(实测):compose 端口映射 `${SEARXNG_PORT}:${SEARXNG_PORT}` 双侧
同值,`.env` 设 `SEARXNG_PORT=8888` → 宿主 `http://127.0.0.1:8888`,与
prd.md:40 缺省 `searxng_base_url=http://127.0.0.1:8888` 对齐。卷:
`/etc/searxng`(配置)+`/var/cache/searxng`。compose 附带 `valkey` 服务:
默认不开 limiter 时闲着,**别删**——§8-④ limiter 验证直接复用(真不需要
时可整段删)。镜像体量:core ~300MB+valkey ~40MB,拉取约 1-2 分钟。

## 2. GET /search 接口形状(文档口径+实测对账全命中)

端点(来源 `docs/dev/search_api.rst`):`GET|POST /` 与 `GET|POST /search`
等价;GET 用 URL 查询参数。**实测**:全程用 GET /search。

### 2.1 请求参数

| 参数 | 取值 | 说明 |
|---|---|---|
| `q` | 必填 | 查询词;缺省=400 `{"error": "No query"}`(实测命中) |
| `format` | `json`/`csv`/`rss` | **须在 settings 激活,未激活 403**(实测:json/csv 双验,Flask HTML 页);不传=html |
| `pageno` | 整数,缺省 1 | 搜索页码(**实测确认:是 `pageno` 不是 `p`**) |
| `language` | 语言/地区码 | **实测 zh-CN 接受**(§8-⑤);SearXNG 按 regions 过滤引擎 |
| `safesearch` | `0`/`1`/`2` | 实测传 1 全程 200;仅对支持的上游生效 |
| `categories` | 逗号分隔 | **实测关键:缺省走 general 类=全新实例仅 9 个小引擎,弱网出口可能全灭;`categories=web` 才是大池**(§8-②/§9) |
| `time_range` | `day`/`month`/`year` | 可选,未实测(实现段按需) |

**prd 纠偏 ①**(实测证实):prd.md:26 写 `&p=<页>`——实际参数名是
**`pageno`**。

MYIA 调用形(实测定稿):

```
GET {base_url}/search?q=<关键词>&format=json&language=zh-CN&safesearch=1&pageno=1&categories=web
```

### 2.2 响应 JSON 形状(实测与文档口径一致)

顶层七个键(**没有 `number_of_results` 顶层字段**,实测确认):

```json
{
  "query": "<原始查询词>",
  "results": [ <Result 字典>, ... ],
  "answers":   [ ... ],
  "corrections":[ ... ],
  "infoboxes": [ ... ],
  "suggestions":[ ... ],
  "unresponsive_engines": [ ["引擎名","错误文案"], ... ]
}
```

`results[]` 元素字段(§2.3 骨架 23 键**实测全中**;**加粗=映射目标**):

| 字段 | 类型 | 实测情况 |
|---|---|---|
| **`url`** | str\|null | 条目 url(实测同 URL 不同标题可重复出现→feed 层 url metric 去重必要) |
| **`title`** | str | 条目 title(实测中文标题直出 UTF-8) |
| **`content`** | str | 摘要(实测可空串;与 title 相同时被置空) |
| `publishedDate` | isoformat\|null | **实测 web 池前 12 条全 null**(§2.2「多数 general 上游不给」证实) |
| `engines` | str 数组 | 命中该结果的 SearXNG 上游引擎名(实测如 `["google cse","naver"]`) |
| `engine` | str | 首发引擎名 |
| `score`/`positions` | float/int 数组 | 聚合排名元数据(实测在) |
| `template` | str | `default.html`=网页结果;**实测 images.html 行会混入 web 池**(55 条中 20 条),实现按 template 过滤有据 |
| `parsed_url` | 数组 | urlparse 序列化(url 已够) |
| 其余 | — | `img_src`/`thumbnail`/`author`/`metadata`/`length`/`views`/`priority`/`category`/`open_group`/`close_group`/`pubdate`(deprecated);实测另见 images 行附加键 `filesize`/`formats`/`img_format`/`resolution`/`source`/`thumbnail_src` |

**prd 纠偏 ②**(实测证实):prd.md:27 写 `publisheddates 可空`——实际
字段名是 **`publishedDate`**(驼峰单数),且摘要字段就是 `content`,
没有 `result.abstract`。

### 2.3 实快照(2026-10-06 实测,替换草稿的文档推导骨架)

真实 55 条全量:`evidence/2026-10-06-search-web-zhcn.json`(71907 bytes,
q=人工智能 监管&language=zh-CN&categories=web);零结果态实拍:
`evidence/2026-10-06-search-default-general-zero.json`(288 bytes)。
首条形(节选,字段顺序无关):

```json
{
  "url": "https://dream.kotra.or.kr/dream/cms/link/actionLinkBoardDetail.do?...",
  "engine": "naver", "parsed_url": ["https","dream.kotra.or.kr","/dream/cms/...", "","",""],
  "template": "default.html",
  "title": "我国建立人工智能安全监管制度的必要性及现实路径",
  "content": "…摘要…",
  "img_src": "", "iframe_src": "", "audio_src": "", "thumbnail": "",
  "publishedDate": null, "pubdate": "",
  "length": null, "views": "", "author": "", "metadata": "", "priority": "",
  "engines": ["naver"], "open_group": false, "close_group": false,
  "positions": [3], "score": 1.0, "category": ""
}
```

## 3. 分页语义(文档口径+实测增量成立)

- `pageno` 从 1 起;逐页对所有支持 paging 的上游取第 N 页再聚合
  (`search.max_page: 0`=不设限)。**实测**:同词 p1=55 条 → p2=62 条,
  其中 **55 条为新 URL**(7 条重叠)——上游语义分页+增量真实有效。
- 注意:分页支持以引擎自报为准——本构建 `/config` 里 bing 主引擎
  `paging: false`(google cse/naver 实测可翻)。
- 深页对上游放大请求且质量陡降;prd.md:36-38 形态(逐词**一页**+
  interval ≥1800s)与该语义匹配。**定案(实测佐证):每词固定
  `pageno=1` 一页**;general/web 类一页即多引擎合并去重后 20-65 条
  (实测四词 55/60/65/65),对「关键词日报」足够。

## 4. 空结果 / 坏参数 / 错误形态(实测逐格命中)

| 场景 | HTTP | 实测响应体 |
|---|---|---|
| 正常但零结果(引擎全灭) | 200 | `{"query":..., "results": [], ...}`+unresponsive_engines 列失败上游(实测 288 bytes 快照在 evidence) |
| 缺 `q` 且 format=json | 400 | `{"error": "No query"}` |
| `format=json` 未激活 | **403** | **Flask 默认 HTML 错误页(非 JSON)**;csv 同拦(实测双验);路由层即拒,零上游成本 |
| limiter 拦截(启用时) | 429 | 纯文本 `Too Many Requests`(实测 17 bytes;连 `/config` 都拦,见 §5) |
| 参数形态坏 | 400 | `{"error": "<SearxParameterException 消息>"}`(文档口径,未单独实测) |
| 实例内部错误 | 500 | `{"error": "search error"}`(文档口径,未遇) |

能力探测面:`GET /config` 返回 engines/categories/limiter.enabled 等,
doctor/装机排障一行 curl 可判「实例活吗、json 开吗(403 与否)、limiter
开吗」;`GET /healthz` 恒 200 文本 OK(实测均通)。**403 特判**=部署侧
没开 json,MYIA 引擎报错文案直指 settings.yml(实现段照此)。

## 5. 限流口径(两态实测定案)

默认态:**官方默认不开**(settings.yml `server.limiter: false`;实测
`/config` → `limiter.enabled: false`)——裸 curl/httpx 全通零拦截。

开启态(`server.limiter: true` + `valkey.url: valkey://valkey:6379/0`,
compose 自带 valkey 服务)实测矩阵(evidence/2026-10-06-limiter-states.txt):

| 客户端 | 头 | 结果 |
|---|---|---|
| 裸 curl | UA=curl,无 Accept-Language | **429**(连 `/config` 都拦) |
| httpx 默认 | UA=python-httpx/0.28.1,无 Accept-Language | **429** |
| httpx 仅补 Accept-Language | +`Accept-Language: zh-CN,zh;q=0.9` | **200 JSON** |
| httpx 浏览器全套 | Accept/A-L/A-E+Chrome UA | 200 JSON |

**定案**:拦的是**缺 Accept-Language** 这一件;`python-httpx` UA 本身
不在拦截面。机制参考(`searx/limiter.py`+`docs/admin/searx.limiter.rst`,
文档口径):启用后 `/search` 依次探测 http_accept/http_accept_encoding/
http_accept_language/http_user_agent/http_sec_fetch/ip_limit;`ip_lists`
pass 列表优先;link-local 直通;limiter.toml 默认 `link_token=false`。
env 覆盖通道:`SEARXNG_LIMITER`/`SEARXNG_PUBLIC_INSTANCE`。

**对 MYIA 的口径(实现段照此写,实测背书)**:

1. 自托管 MYIA 专用实例(绑 127.0.0.1/内网)→ **保持 limiter 默认
   false**,自家采集零拦截面;与 robots 立场(§6)一致。
2. 实例若同时对外必须开 limiter → MYIA 客户端**常发
   `Accept-Language: zh-CN,zh;q=0.9`**(一行头即过,实测;比进
   limiter.toml pass_ip 白名单更零运维)。
3. MYIA 侧礼貌间隔不因自托管省略(prd.md:38):interval ≥1800s+逐词
   串行+词间页延时——上游元搜索的礼貌由 SearXNG 聚合层承担(其自带
   `ban_time_on_fail`/`suspended_times` 熔断),MYIA 不放大。

## 6. robots 口径(结案落定)

实例内置 `robots.txt`(webapp.py 路由原文,文档口径):

```
User-agent: *
Allow: /info/en/about
Disallow: /stats
Disallow: /image_proxy
Disallow: /preferences
Disallow: /*?*q=*
```

即 SearXNG 默认对外来爬虫**禁搜**(`/*?*q=*` 覆盖一切搜索请求)——
「公共实例明禁 API 滥用」(prd.md:79-80 红线)的服务端体现,也是 MYIA
只走自托管、不代理公共实例的依据。

**自家实例策略=允许自家采集(结案落定)**:MYIA 采集的是主人自己部署的
实例,robots 管的是第三方爬虫,实例主人(=MYIA 使用者本人)对自家流量
自授权;上游(真正搜索源)的礼貌由 SearXNG 聚合层统一承担(§5-3),
MYIA 端再加间隔不放大。此口径随实现批落进引擎模块文档(同 reddit
官方 API 引擎「robots 面不适用钉死端点」论证形态,
src/myssia/engines/registry.py:121-125 先例)。

## 7. 对实现段的落地指导(锚点既有层,挂点定案细化见 §9)

- **注册形态**:链外源引擎,同 `reddit` 先例(src/myssia/engines/
  registry.py:121-125)——`ENGINE_REGISTRY` 加一行 `"searxng"`,
  **不进** `AUTO_CHAIN`(registry.py:83-91),显式 `engine: searxng`
  才生效(搜索型源没有「降级链」语义,坏了就是本源结构化失败)。
  ⚠️ 错峰注记:探查批写作时 registry.py 有 10-06-ai-news-sources 在途
  未提交改动(urlwatch 注册行)——**ad19a9a 提交时复核实已收口**(urlwatch
  注册行已由对方落库,registry.py:130,工作树干净),实现批可直接开工;
  动该文件前仍须例行 `git status` 复核共享工作树,防同窗互踩
  (65e1b96 教训在案)。
- **base_url 缺省+env**:`searxng_base_url` 缺省 `http://127.0.0.1:8888`,
  env `MYIA_SEARXNG_URL` 覆盖——同 firecrawl 先例(src/myssia/engines/
  firecrawl.py:46-48 `ENV_FIRECRAWL_URL`/`DEFAULT_FIRECRAWL_ENDPOINT`)。
- **条目映射**:`{url: r["url"], title: r["title"], content: r["content"]}`
  (content 可空串);`publishedDate` 非空 isoformat 时透传否则 None;
  过滤 `template != "default.html"` 的特殊结果(images 卡,实测混入);
  坏行跳过(缺 url/title)沿用 fetch 层既有 skip 口径。
- **错误面**:非 2xx→`FetchError`(`http_<status>` 同 firecrawl.py:18-20);
  **403 特判**=「实例未开 json format」部署侧提示(§4 实测);429=
  limiter 拦截→提示 Accept-Language/limiter 口径(§5 实测);400/5xx
  透传 `error` 字段;连接拒绝=「searxng 实例未起」结构化失败(同
  firecrawl 自托管死服务优雅降级口径,firecrawl.py:13-15)。
- **零凭据**:queries 明文非凭据可落 YAML(prd.md:81 红线),无 env/
  keychain 面,比 firecrawl 更简。
- **fixture 基准**:`evidence/2026-10-06-search-web-zhcn.json` 实快照
  即测试夹具蓝本(六用例:正常多词多结果/空 results/坏行/pageno 语义/
  env 两态/schema queries 必填)。

## 8. 实测补齐清单(2026-10-06 全项真跑,evidence 落档)

1. ✅ compose 起实例+`/healthz`(200 OK)+`/config`(limiter false,
   261 引擎/82 启用/33 类)。
2. ✅ 缺省参数实快照:general 默认类=**0 结果**(弱引擎池+本机出口受限,
   快照 `…-default-general-zero.json`);`categories=web`=55 条
   (`…-search-web-zhcn.json`);§2.2/§2.3 逐字段对账全命中(⑧)。
3. ✅ 三态实拍:未开 json 的 403(Flask HTML,csv 同)/ 缺 q 的 400
   `{"error": "No query"}` / 引擎全灭空 results 200;`pageno=2` 增量
   55→62 条(55 新 URL)。
4. ✅ limiter 两态:默认 false 直连;开 true+valkey 后裸 curl 429(连
   /config)、httpx 默认头 429、**仅补 Accept-Language 即 200**
   (`…-limiter-states.txt`)。
5. ✅ `language=zh-CN` 接受面:全程 200,naver/google cse 返回中文结果,
   与无 language 参数分布一致。
6. ✅ 查询词示例集:舆情词×2+竞品词×1+事件词×1(55/60/65/65 条),
   各前 3 条脱敏落 `…-query-set.json`。
7. ⬜ 20 条入库截图:随实现批一起做(prd.md:62-64 AC 门控,本批探查
   段范围外)。
8. ✅(附加)结果契约核验:23 键骨架全中+images 附加键 6 个+
   publishedDate 全 null+template 过滤必要性+unresponsive 形状
   (`…-probe-log.txt` ⑧节)。

本机出口引擎实况(自托管策展参考,逐次可抖动):可达出结果=google cse
(+images)/naver/qwant videos;flap=duckduckgo(CAPTCHA↔timeout)、
wikipedia/wikidata;拒=brave 429、google 主引擎 access denied、yahoo/
seznam timeout;异常=bing settings 启用后 enabled:true 却静默零结果
(!bang 定向亦 0、unresponsive 空;容器内 urllib 直测 bing 0.42s 200,
网络可达、问题在引擎实现侧,未深挖如实记)。**引擎策展=部署侧一回事**
(§9-5)。终态 `/config` 全量启用清单:`…-config-final.txt`。

## 9. 挂点定案(结案结论,实现批照此开工)

**总判:探查通过,接口契约与 prd 设想完全兼容(仅两处参数纠偏已在
§2.1/§2.2 证实),实现段就绪——续本档两段式的第二段执行,不另立新档**
(prd AC2-6 本就属本档;探查数据已把实现面的未知数清零)。开工前置:
registry.py 与 10-06-ai-news-sources 在途件错峰(§7 注记)。

实现批要点(prd.md:33-50+§7 细化,实测新增三条):

1. **请求形状**:`GET {base}/search?q=<词>&format=json&language=zh-CN
   &safesearch=1&pageno=1&categories=web`——`categories=web` 为实测
   定案(默认 general 类弱池,弱网出口可全灭);常发
   `Accept-Language: zh-CN,zh;q=0.9` 头(limiter-on 实例一行头即过,
   limiter-off 无害)。
2. **条目与去重**:template 过滤(只要 default.html)+缺 url/title 跳过
   +`publishedDate` 非空透传;去重走 feed 层既有 url metric 键(实测同
   URL 不同标题会重复出现,必要)。
3. **礼貌参数**:interval ≥1800s+逐词串行+词间短延时(自托管也不放大,
   §5-3);每词固定 pageno=1。
4. **引擎策展属部署侧**:MYIA 不绑死上游引擎名单;本机实测可达面记
   §8 供部署参考,settings 覆盖启用(`engines: - name: X disabled:
   false`)是自托管正路。bing 静默零结果为未解观察项,部署侧如需 bing
   另行排查(非 MYIA 面)。
5. **生产部署(留主人服务器)**:主人侧同法起栈=官方 compose 三步+
   `settings.yml` 两行(formats+secret)+`.env` 端口对齐;注意 docker-in-VM
   共享路径坑(§0);服务器出口与本机不同,起栈后用 §8 方法一次 healthz/
   config/一条 web 类查询冒烟即可交付;MYIA 侧只改 `searxng_base_url`
   (或 env MYIA_SEARXNG_URL)指向服务器实例。装机包不内置该栈(自托管
   服务属主人运维面,同 RSSHub/Firecrawl 判例)。
