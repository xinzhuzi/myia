# myssia-webcheck — 网站全息体检台(web-check)

官方场景件(remote 分级,无门槛件):接入一个已部署的
[web-check](https://github.com/Lissy93/web-check) 实例,对任意网站做一站式
曝面分析:技术栈指纹、DNS 记录、SSL 证书链、安全响应头、开放端口、爬虫
抓取、链接与重定向等 20+ 探测维度。与 exposure lane 互补——credhunter 查
「凭证泄露」,web-check 查「站点本身的曝面」。上游 MIT,零源码复制。

## 接入路径(remote:填 endpoint)

1. 自部署:`docker/plugins/myssia-webcheck/compose.yml`(官方镜像
   `lissy93/web-check`,单服务零凭据,127.0.0.1:3000 回环绑定);
2. 实例地址填进 endpoint(`plugin.modes.remote.endpoint`);
3. 上游自部署形态无内建鉴权——回环/内网部署自担边界,要暴露到不受信
   网络请自行加反代鉴权(本件不带 token 声明,凭据自管)。

## 定位与互补

- myssia-osint(Photon)/myssia-theharvester/myssia-spiderfoot 偏「人/组织/
  域名」的 OSINT 聚合;web-check 偏「单个站点」的技术曝面体检——同类目标
  不同切面,按需组合;
- 无门槛件:MIT 自部署即零成本零第三方,无需知情开关(与 crawlab/
  worldmonitor 的 platform 门槛件不同)。

## 铁律

实例不可达只降级为结构化 warning finding,核心品类流水线照常
(装不上不拦核心;`myssia doctor` 可见)。
