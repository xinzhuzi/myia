# myssia-worldmonitor — 全球情报监控台(World Monitor)

官方场景件(remote 分级,**门槛件:自有实例例外通道**):接入一个你已部署的
[World Monitor](https://github.com/koala73/worldmonitor) 实例(AI 新闻聚合、
地缘政治监控、基础设施追踪的实时态势感知台),把它的专题视图当作 MYIA 的
全局监控情报源之一。上游 AGPL-3.0,**只桩不抄**——零源码复制,MYIA 只
消费其部署实例的 HTTP 面。

## 为什么有门槛(platform)

上游描述即「Real-time global intelligence dashboard」= 另一个 MYIA(同物种,
盘点表 d 路判例)——默认不收,收录的唯一形态是「你已有自部署实例要接」的
例外通道。门槛 = 自有实例,不是物种本身拒绝:

1. 自部署:按上游仓库 [koala73/worldmonitor](https://github.com/koala73/worldmonitor)
   官方 quickstart 部署(四服务 app+ais-relay+redis+redis-rest,从上游 git
   构建,密钥经上游部署面的 `${VAR}` 注入,`openssl rand -hex 32` 生成;
   部署属主人运维面,插件不提供 docker 模式,我方不复刻配方);
2. **实例地址填进桌面 设置→门槛件→自有实例 表单**——落点不是品类 YAML,
   是全局 gates.yaml 的 `platforms.worldmonitor.endpoint`(部署栈自身密钥
   按上游部署面的 `${VAR}` 注入自配;上游 REST 操作键体系
   X-WorldMonitor-Key 属实例侧鉴权,设置面本件不设凭据位、MYIA 不代管);
3. 知情开启门槛开关(同表单开关,或
   `myssia gates set platforms.worldmonitor on`;组织性不执法)。

## 门槛的运行时语义(组织性不执法,D6)

- 开关=知情确认+状态面:开启后 `myssia plugin list` 门槛件分组显示
  「已启用」徽标,doctor 由 info 转 ok;未启用是正常态(info,不是故障);
- **不拦任何 direct_api 源**:你的 endpoint 你做主(真执法只属付费引擎的
  gate_closed 与未来 analysis lane);
- gates.yaml 缺失/损坏 = 全关(fail-closed),核心品类流水线照常
  (装不上不拦核心)。

## AGPL 边界

上游 AGPL-3.0:本仓库不复制其任何源码,也不分发其部署配方(部署在上游
部署面按其官方文档进行,AGPL 义务留在上游部署侧);MYIA 只消费其部署
实例的 HTTP 面。

## 铁律

实例不可达只降级为结构化 warning finding,核心品类流水线照常
(`myssia doctor` 可见)。
