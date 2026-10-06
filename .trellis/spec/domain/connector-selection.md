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
- **插件源码不随包:装机包只带声明(plugin.yaml/README),adapter/vendor 按需远取落数据根**(判例 2026-10-06 主人令「是这些源码不能随包,但是这些配置可以」,任务档 10-06-plugin-src-remote-fetch):装机包 `Resources/plugins/<id>/` 只准携带 `plugin.yaml`+`README.md` 声明件——源码(adapter.py/场景件)与数据件(vendor/ submodule 上游、`__pycache__` 缓存)一律不进包;点装时按包内 `plugins.lock.json` 内容寻址锁(url+sha256+size,机器事实源;`plugin.yaml install.source` 仍归人读)从 release 资产远取落 `~/.myia/plugins/<id>`(InstalledPluginStore 同门:manifest 校验/版本矩阵/整目录拷贝绝不半装),失败=结构化错误零静默零半装;旧装机包(锁缺席+包内有源码)回退包内直拷自愈;MYIA 自身 python 核心(myssia-src/)是产品本体,不属此列,随包不变;门禁 `tests/desktop/test_installer_resources.py` 键空间负断言(`*.py`/vendor/credhunter 子包/`__pycache__` 不在 resources 映射),回退即红

## 信号分级(选型时标注)

`极稳(开源可自托管)` > `云厂商级` > `营销型(一次性额度/会耗尽/会到期)` > `新兴(高波动)`

## 相关

- 候选池与免费层快照:`.trellis/tasks/archive/2026-10/10-03-free-tier-supplier-map/research.md`(引用时核机制见其末节)
