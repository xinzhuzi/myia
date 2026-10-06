# myssia-crawlab — 分布式爬虫管理台(Crawlab)

官方场景件(remote 分级,**门槛件:自有实例例外通道**):接入一个你已部署的
[Crawlab](https://github.com/crawlab-team/crawlab) 实例,把它的爬虫编排/任务
调度面当作 MYIA 的采集执行台之一(spider 管理、任务队列、分布式节点)。
上游 BSD-3-Clause,只以 manifest+文档引用接入,零源码复制。

## 为什么有门槛(platform)

Crawlab 本身就是采集编排平台,与 MYIA 同生态位(盘点表 d 路判例)——默认
不收,收录的唯一形态是「你已有自部署实例要接」的例外通道。门槛 = 自有
实例,不是物种本身拒绝:

1. 自部署(按上游官方 quickstart/部署文档,官方镜像
   `crawlabteam/crawlab`;部署属主人运维面,插件不提供 docker 模式,
   我方不复刻配方);
2. **实例地址与凭据都填进桌面 设置→门槛件→自有实例 表单**——落点不是
   品类 YAML,是全局 gates.yaml 的 `platforms.crawlab.endpoint` / `token`
   (部署侧启用 API token/反代鉴权才需要凭据;键走设置面规范名
   `myia/platforms/crawlab-token`,CLI 等价
   `myssia secret set myia/platforms/crawlab-token`);
3. 知情开启门槛开关(同表单开关,或
   `myssia gates set platforms.crawlab on`;组织性不执法)。

## 门槛的运行时语义(组织性不执法,D6)

- 开关=知情确认+状态面:开启后 `myssia plugin list` 门槛件分组显示
  「已启用」徽标,doctor 由 info 转 ok;未启用是正常态(info,不是故障);
- **不拦任何 direct_api 源**:你的 endpoint 你做主(真执法只属付费引擎的
  gate_closed 与未来 analysis lane);
- gates.yaml 缺失/损坏 = 全关(fail-closed),核心品类流水线照常
  (装不上不拦核心)。

## 铁律

实例不可达只降级为结构化 warning finding,核心品类流水线照常
(`myssia doctor` 可见)。
