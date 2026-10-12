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

- [x] AC1 四项全修或逐项注明不修理由;vitest+build+冒烟全绿;装机换装。

## 边界

- 纯打磨批,零协议/零数据面改动。

## grill 决议表(2026-10-12 深化;四项修法复核定案)

| # | 问题 | 决议 | 依据 | 可翻案 |
|---|------|------|------|--------|
| G1 | itemCount 死字段 | **删**:字段+itemsRetained 助手+其类型引用全清(grep 实证零消费方;摘要段 deriveOutcome 自带独立派生) | 复查员 grep 在案 | 否 |
| G2 | 错误横幅满高 | 编排层 return 根包 flex h-full min-h-0 flex-col,横幅自然高、L1/L2 分支根改 flex-1 min-h-0 | 复查员修法;jsdom 无布局,验法=无头冒烟错误态夹具(本档补:冒烟加一条 error 态断言) | 是 |
| G3 | view 滞留弹回 | detailRun===null 时 effect setView({level:1}) 复位;vitest 补用例(行消失→回 L1,行重现不弹回) | 复查员修法 | 否 |
| G4 | 时间 Map 撞号 | startedAtById/finishedAtById 键改 runRowKey(run);vitest 撞号用例已有(注册表5/历史5 同屏),补断言两行时间各自正确 | HEAD 平移旧账,顺手收 | 是 |
| G5 | 门禁 | build/vitest/冒烟三件 + 全量 pytest(纯前端面理论零 py 影响,跑一次兜底) | — | 否 |


## 终局回执(10-12 23:0x)

- AC1 ✓(四项全落+判别力用例);提交 fc142a6;换装随档1。