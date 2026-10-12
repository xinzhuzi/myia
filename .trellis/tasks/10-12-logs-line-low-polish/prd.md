# 采集日志线 low 收尾批

## Goal

logs-two-level-ui 复查留档的 4 条 low 一批收尾(全部复查员定位+终审员核实
在案,证据见该档交付报告)。

## 清单(含修法,复查员原话)

1. `logs/api.ts:91` itemCount 死字段——「N 条」槽并入摘要段后零消费方,
   删字段+itemsRetained 助手,或注释标注留档。
2. `logs-screen.tsx:313` 错误横幅与 h-full 分支成兄弟后满高算术缺口——编排层
   return 根包 flex h-full min-h-0 flex-col,横幅自然高、分支根 flex-1。
3. `logs-screen.tsx:207` view 滞留 {level:2}——detailRun=null 时 effect 里
   setView({level:1}) 复位(行消失又重现不弹回)。
4. `logs-screen.tsx:190` startedAtById/finishedAtById 裸 run_id 键撞号(HEAD
   平移旧账)——改键为 runRowKey。

## Acceptance Criteria

- [ ] AC1 四项全修或逐项注明不修理由;vitest+build+冒烟全绿;装机换装。

## 边界

- 纯打磨批,零协议/零数据面改动。
