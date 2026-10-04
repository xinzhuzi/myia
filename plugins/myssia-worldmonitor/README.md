# myssia-worldmonitor — 全球情报监控台(World Monitor)

官方场景件(remote 分级,**门槛件:自有实例例外通道**):接入一个你已部署的
[World Monitor](https://github.com/koala73/worldmonitor) 实例(AI 新闻聚合、
地缘政治监控、基础设施追踪的实时态势感知台),把它的专题视图当作 MYIA 的
全局监控情报源之一。上游 AGPL-3.0,**只桩不抄**——零源码复制,部署构建
上下文直指上游 git。

## 为什么有门槛(platform)

上游描述即「Real-time global intelligence dashboard」= 另一个 MYIA(同物种,
盘点表 d 路判例)——默认不收,收录的唯一形态是「你已有自部署实例要接」的
例外通道。门槛 = 自有实例,不是物种本身拒绝:

1. 自部署:`docker/plugins/myssia-worldmonitor/compose.yml`(上游无预构建
   镜像,四服务 app+ais-relay+redis+redis-rest 照上游 quickstart 从上游
   git 构建,钉 tag v2.10.0;必设密钥经 `${VAR}` 注入,`openssl rand -hex 32`
   生成;127.0.0.1:3001 回环绑定);
2. 实例地址填进 endpoint(`plugin.modes.remote.endpoint`);启用 API 操作键
   (上游 `WORLDMONITOR_VALID_KEYS` / X-WorldMonitor-Key 语义)时,把键写入
   钥匙串:`myssia secret set myia/worldmonitor/api-key`;
3. 知情开启门槛开关(不落品类 YAML):
   `myssia gates set platforms.worldmonitor on`,或桌面 设置→门槛件 分区。

## 门槛的运行时语义(组织性不执法,D6)

- 开关=知情确认+状态面:开启后 `myssia plugin list` 门槛件分组显示
  「已启用」徽标,doctor 由 info 转 ok;未启用是正常态(info,不是故障);
- **不拦任何 direct_api 源**:你的 endpoint 你做主(真执法只属付费引擎的
  gate_closed 与未来 analysis lane);
- gates.yaml 缺失/损坏 = 全关(fail-closed),核心品类流水线照常
  (装不上不拦核心)。

## AGPL 边界

上游 AGPL-3.0:本仓库不复制其任何源码(部署 compose 的 build 上下文指向上
游 git,AGPL 义务留在上游构建产物侧);MYIA 只消费其部署实例的 HTTP 面。

## 铁律

实例不可达只降级为结构化 warning finding,核心品类流水线照常
(`myssia doctor` 可见)。
