# myssia-firecrawl — 渲染抓取后端(Firecrawl)

官方场景件(remote 分级):接入一个已部署的 [Firecrawl](https://github.com/firecrawl/firecrawl)
实例,作 L3 `firecrawl` 引擎的渲染后端(纯 HTTP 客户端,云端/自有服务器
均接;`crawl4ai` 组件装好前或纯 JS 渲染站的后备通道)。上游 AGPL-3.0,
只以 manifest + 文档引用接入,零源码复制(不 vendor);桌面本机不装
Node 服务端(10-06-native-plugin-components 主人终裁:插件不提供 docker
模式,本机零 Docker)。

## 接入路径(remote:填 endpoint)

1. 选后端:官方云 `api.firecrawl.dev`(付费,按页计费)或按上游
   [SELF_HOST.md](https://github.com/firecrawl/firecrawl/blob/main/SELF_HOST.md)
   自部署一套自有服务器(部署属主人运维面,我方不复刻配方);
2. 设置页 →「随包官方插件件」卡 → 本件条目的 remote 配置面板:
   endpoint 填实例地址,API 键经面板写入系统钥匙串
   (`myssia secret set myia/firecrawl/api-key` 同一道门,值不落盘);
3. 未配置 = 缺省降级链既有行为不变:引擎死/未配 → 源级结构化失败,
   核心品类流水线照常(`myssia doctor` 的 firecrawl 连通项:未配置不红,
   配置了才探活)。

env 通道 `MYIA_FIRECRAWL_URL` / `MYIA_FIRECRAWL_API_KEY` 保留为开发后门
(显式 env 优先);桌面态端点由配置面板提供,不依赖 env。

## 引擎消费面

品类源 `engine: firecrawl` 即消费该后端(`engine_options.firecrawl`
的 endpoint/api_key 只允许 `env:`/`keychain:` 引用,禁明文——安全基线
「配置零明文凭据」);端点展示形态记来源,解析值不落日志。
