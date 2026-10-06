# R1 归面总表:逐件过一遍(2026-10-06 grill 轮产物)

> 数据源:`plugins/*/plugin.yaml` 20 件全量脚本抽取(非手抄)+ `docker/plugins/` 实数 + 引擎源码头核。
> 四轨:A=壳库组件(components.json)/ B=壳服务组件(kind:service)/ C=desktop 插件包(~/.myia/plugins)/ D=remote 声明。
> 口径修正:plugins/ 32 条目 = 20 插件包 + 12 品类 YAML(品类文件=配置数据,经 bundled 卡平铺装,无需归轨)。

## 插件包 20 件

| # | 包 | tier | local | remote | gate | 目标轨 | 动作 |
|---|---|---|---|---|---|---|---|
| 1 | myssia-crawlab | remote | - | ✓ | platform | D | 注释 recipe 引用改写 |
| 2 | myssia-credentials | remote | - | ✓ | | D | 零动作 |
| 3 | myssia-credhunter | desktop | install | - | | C | 已有轨(装机面 bundled 卡可装) |
| 4 | myssia-douyin | **server-only** | - | ✓ | | D | tier 词汇见 G-Q2;注释改写 |
| 5 | myssia-maigret | desktop | install | - | | C | 已装 ✓ |
| 6 | myssia-maxun | **server-only** | - | ✓ | | D | 同 douyin |
| 7 | myssia-media | desktop | install | - | | C | 零动作 |
| 8 | myssia-mediacrawler | desktop | install | - | | C | 零动作(无 adapter,子进程型) |
| 9 | myssia-monitor | remote | - | ✓ | | D | 注释改写(changedetection.io 桩) |
| 10 | myssia-osint | desktop | - | ✓(占位) | | C(+D 占位) | 注释改写 |
| 11 | myssia-proxy | desktop | - | ✓(可选) | | C(+D 可选) | 注释改写 |
| 12 | myssia-rsshub | remote | - | ✓ | | D | 注释改写(AGPL 桩判例) |
| 13 | myssia-snownlp | desktop | install | - | **stale** | C | gate 已示警,处置见 G-Q3 |
| 14 | myssia-socialanalyzer | remote | - | ✓ | | D | 零动作 |
| 15 | myssia-spiderfoot | remote | - | ✓ | | D | 注释改写 |
| 16 | myssia-theharvester | desktop | install | - | | C | 零动作 |
| 17 | myssia-urlwatch | desktop | install | - | | C | 已装 ✓(内含 render_crawl4ai 场景件,待轨A 组件解锁) |
| 18 | myssia-webcheck | remote | - | ✓ | | D | 注释改写 |
| 19 | myssia-worldmonitor | remote | - | ✓ | platform | D | 注释改写 |
| 20 | **(缺)myssia-firecrawl** | — | — | — | | **D(新桩)** | grill 发现:firecrawl 引擎无市场条目,轨D 配置面板无挂点 → **G-Q1 定裁:建桩(tier: remote,零 adapter,golden 同步)** |

**零 manifest 用 `local.compose`;`requires` 全空** —— docker 模式删除 = 零迁移(再次实证)。
**注释 recipe 引用 10 处**(与 docker/plugins/ 10 配方一一对应):crawlab/douyin/maxun/monitor/osint/proxy/rsshub/spiderfoot/webcheck/worldmonitor。
**G-Q 定裁标注**:douyin/maxun server-only 词汇保留(G-Q2);snownlp stale 闸维持(G-Q3);scrapling 维持 extras(G-Q4);searxng 手动启停+状态记忆(G-Q5);组件体积披露(G-Q6)。

## 引擎适配器 14 个(src/myssia/engines/,registry/fetch_base 为核心不计)

| 引擎 | 运行时形态 | 归面 |
|---|---|---|
| direct_api / static_html / reddit / zenrows / scraperapi / saas / llm_browser(skyvern) | 纯 HTTP 客户端,零本机运行时 | 已合规,零动作 |
| firecrawl | HTTP 客户端 → 外部服务(cloud/服务器) | 轨D(G-Q1 市场桩 + doctor 连通项) |
| searxng | HTTP 客户端 → 本机服务(8888) | **轨B(本档实做)** |
| crawl4ai | 进程内库 + playwright 浏览器 | **轨A(本档实做)** |
| scrapling | 可选 extras(`myssia[scrapling]`,fetchers 另带自家 extras) | extras 维持(G-Q4) |
| stealth_browser(L5) | **uvx 自管型**(stdio 自启 `uvx invisible-playwright-mcp`) | 已合规原生,零动作(doctor 可见性随既有) |
| urlwatch / credhunter / maigret | desktop 包 adapter | 轨C ✓ |

## 品类 YAML 12 件(配置数据,不归轨,记录在案)

ai-news / ai-vendor-watch / credentials / exposure / games / gpu-prices / monitor / myssia-demo / news / **searxng(头部本机 docker 三步指引退役,阶段 4)** / stocks / wool
