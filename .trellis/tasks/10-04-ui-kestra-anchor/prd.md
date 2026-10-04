# UI 全面 Kestra 化:开源真源码+真跑像素双真源重锚

## Goal

主人 2026-10-04 定锚:「照着一个开源的去做——K 开头的爬虫软件」(=Kestra,kestra-io/kestra,Apache-2.0;模仿总表旧对标之一)。**方法论修正**:此前按「谁最好看」选 Linear=工单物种,与 MYIA=情报调度台不同物种;Kestra=任务调度台与 MYIA 同物种,且开源=源码逐文件可对照(Hermes 判例:全应用唯一没被骂的屏就是开源直抄的)。

## 域映射(Kestra → MYIA)

| Kestra | MYIA | 说明 |
|---|---|---|
| Flows(流程定义列表/详情/编辑) | 品类插件(YAML 源管理/配置编辑) | 同构:定义→定时跑 |
| Executions(执行列表/Gantt/拓扑/重放) | 采集 runs(采集日志屏/仪表盘运行区) | 同构:跑了什么/多久/成败 |
| Logs(执行日志查看器) | 日志行/错误高亮 | Crawlab 之外更强的现成参照 |
| Namespaces | 品类分组 | 侧栏组织方式 |
| Triggers/定时 | 排程(schedule/cron) | 直接同域 |
| 通知/审计 | 推送反馈/告警 | Kestra 通知中心范式 |
| 空态/引导态 | 首跑引导(demo 一键跑) | Kestra 空态设计一并学(主人真库零蛋仪表教训) |

## Requirements

- R1 蓝本先行:clone kestra 读 ui/src 真源码(Vue3)+ 本地跑 UI 截真图(docker 或 dev server),逐屏拆解表(布局/交互/空态/密度/色板)——像素与代码双真源,不再靠文档想象。
- R2 全应用重锚:壳层/仪表盘/情报流/源管理/日志/设置/消息/YAML 按域映射逐屏对齐 Kestra 对应屏;可直借(Apache-2.0)的组件结构直接借,语义改我们的。
- R3 色板/密度基调对齐 Kestra 暗色(替换现 Linear 底色),全屏统一。
- R4 空态引导态:首跑零数据时呈现 Kestra 式引导(一键跑 demo),不再零蛋仪表。
- R5 功能面零改动(纯 UI 重锚);VL+DOM 实测双验收;主人目验终裁。

## Constraints

- Apache-2.0 归属注明;不 push(完成收口按主人令);MYIA 真库只读冒烟;os-etiquette 全程静默。
- Hermes 判例打法:逐文件对照+偏离表(为什么这个不抄),不整块 vendor。

## 待主人确认

K 开头=Kestra 这个认读对不对(若是别的,报名字即换)。
