# myssia-spiderfoot — OSINT 聚合查询台(SpiderFoot)

官方场景件(remote 分级):接入一个已部署的 [SpiderFoot](https://github.com/smicallef/spiderfoot)
实例,做跨 200+ 数据源的 OSINT 关联查询(域名/邮箱/IP/泄露的组合画像)。
上游 MIT。

## 接入路径(remote:填 endpoint)

1. 自部署:按上游仓库 [smicallef/SpiderFoot](https://github.com/smicallef/spiderfoot)
   官方部署文档操作(官方镜像 `spiderfoot/spiderfoot`,数据卷持久化;
   部署属主人运维面,插件不提供 docker 模式,我方不复刻配方)。远程访问
   口令经上游部署面的 `SPIDERFOOT_PASSWORD` 注入并写入钥匙串:
   `myssia secret set myia/spiderfoot/password`;
2. 实例地址填进 endpoint;扫描任务经其 REST API 发起
   (`POST /api/spiderfoot/start` 一族),结果轮询回读;
3. 与 myssia-osint(Photon,进程内单站侦察)/myssia-theharvester(域名聚合)
   互补:SpiderFoot 是「多源关联台」,适合深挖单个高价值目标。

## 为什么是 remote 桩(desktop 缺席说明)

上游不在 PyPI(2026-10-05 实测)且是 Web 服务形态(UI+SQLite+任务队列),
进程内故事不成立 —— 盘点表原判 b 路改判 c 路,记档于任务 research.md。
MIT 许可本可直借,但形态不允许;自部署即零第三方(P0 本地执行硬规则的
「自有实例」形态)。

## 铁律

实例不可达只降级为结构化 warning finding,核心品类流水线照常
(装不上不拦核心;`myssia doctor` 可见)。
