# myssia-socialanalyzer — 社媒画像分析台(social-analyzer)

官方场景件(remote 分级,无门槛件):接入一个已部署的
[social-analyzer](https://github.com/qeeqbox/social-analyzer) 实例,对给定
用户名做 1000+ 社媒站点的存在性检测与画像聚合(名称/头像/简介/链接)。
上游 AGPL-3.0,**只桩不抄**——零源码复制,仅声明依赖与文档引用。

## 与 myssia-maigret 的分工

- **maigret**(MIT,desktop adapter):跨 3000+ 站的用户名**占用快扫**,
  本机子进程即起即用;
- **social-analyzer**(AGPL,remote 桩):单站**画像深挖**(检测类型更细:
  名称匹配/头像/元数据聚合),上游自带 Web/API 形态故走自部署实例接入;
- 上游 2026-01 后趋缓(盘点表记档),桩件按现状声明,不钉版承诺。

## 接入路径(remote:填 endpoint)

1. 自部署:上游自带部署栈(app+selenium 网格,栈较重),部署按
   [qeeqbox/social-analyzer](https://github.com/qeeqbox/social-analyzer)
   上游仓库的部署文档操作——MYIA 不携带任何插件部署配方(终裁
   2026-10-06:插件 docker 模式全删;上游栈重不适合薄封装,本件本就
   只桩);
2. 实例地址填进 endpoint(`plugin.modes.remote.endpoint`);
3. 上游自部署 Web/API 面无内建鉴权——回环/内网部署自担边界(本件不带
   token 声明,凭据自管)。

## AGPL 边界

上游 AGPL-3.0:本仓库不复制其任何源码,不分发其部署文件;MYIA 只消费其
部署实例的 HTTP 面,AGPL 义务留在上游侧。

## 铁律

实例不可达只降级为结构化 warning finding,核心品类流水线照常
(装不上不拦核心;`myssia doctor` 可见)。
