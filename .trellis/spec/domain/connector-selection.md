# 云端连接器选型门禁(2026-10-03 grill 定案)

## 适用范围

一切要求用户自配 key/端点的云端连接器:push 通道(`src/shishi/push/`)、抓取引擎(`src/shishi/engines/`)、vision/enrich 云端端点(`src/shishi/vision|enrich/`)。

## 硬规则

- **云端连接器必须有免费路径**:稳定免费层或开源自托管替代,二居一;都没有 = 不立项。新连接器 PRD 必须回答「免费路径是什么」,无答案不开工
  - Why:BYO-key 架构下免费路径就是装机门槛;免费层是结构性营销(Fly.io/X API 免费层翻车在案),不是承诺
- **优先级排序**:本地/自托管 > 多年稳定免费层 > 新兴聚合器;聚合器(XFlux 型)只做可选后端,永不默认
- **OpenAI 兼容端点优先**:vision/enrich 换 `base_url` 即接,非兼容端点须额外论证适配成本
- **免费额度进用户文档的,一律带快照日期 +「以官网为准」**;引用 research 快照中 ○(未核)项前,先核实并回写升 ●
- **插件一律本机原生运行,零 docker 模式**(判例 2026-10-06:主人令「MYIA 控制所有插件」「插件都不要docker模式」;管控面唯一入口=设置页 UI,四轨模型=壳库组件(components.json)/壳服务组件(kind:service)/desktop 插件包(~/.myia/plugins)/remote 声明(modes.remote),任务档 10-06-native-plugin-components):插件要么在管控面内(声明→装/启停/健康/卸载全走 app),要么不存在,游离手工资产=违例;插件不提供 docker 模式——schema `compose` 字段已删、`REQUIRES_TOKENS` 词表空、`docker/plugins/` 配方整删,插件部署配方一律外链上游官方文档、仓库零携带;产品自身 server 形态(根 `Dockerfile` + `docker/docker-compose.yml`)不属插件面,保留

## 信号分级(选型时标注)

`极稳(开源可自托管)` > `云厂商级` > `营销型(一次性额度/会耗尽/会到期)` > `新兴(高波动)`

## 相关

- 候选池与免费层快照:`.trellis/tasks/archive/2026-10/10-03-free-tier-supplier-map/research.md`(引用时核机制见其末节)
