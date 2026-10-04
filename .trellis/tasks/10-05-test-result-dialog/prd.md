# 试抓结果改详情弹窗(源管理贴顶横幅设计错误修正)

## Goal

主人判词(2026-10-05 截图):「这种提示做详情弹窗,而不是放到界面最上面展示这东西,完全设计错误」。修正源管理屏试抓(C13)回显:试抓相关顶部常驻横幅(成功绿条/失败红条/进行中条)整体撤除,结果以模态详情弹窗呈现,并利用既有 `test.completed` 结构化报文把横幅塞不下的明细(引擎退化链逐条失败、逐条目预览+dedup_key、指纹判定)一并展示;行内 spinner(已有)承载进行中态。

判词截图(3466×160,一级 Vision OCR + 本机 VL 二级校对)即屏顶成功绿条原文:

`试抓 aihot:static_html · 20 条 · 退化 1 次 · 内容有变化或首次抓取,线上调度会正常提取`

## 现状证据矩阵

| # | 位置 | 现状 | 问题 |
|---|---|---|---|
| 1 | `desktop/ui-src/src/screens/sources/sources-screen.tsx:341-353` | 试抓完成摘要贴屏顶常驻横幅(ok 绿条 / fail 红条),一行塞引擎+条数+退化次数+指纹判定 | 判词直接命中:详情类信息贴顶展示 |
| 2 | `sources-screen.tsx:331-340` | 试抓进行中也是贴顶横幅,「异步 job #7」行话上屏 | 同族问题;行话违反 cron-ui 文案判例(job/裸 id 不上活性条) |
| 3 | `desktop/ui-src/src/screens/sources/api.ts:247-288` | `summarizeTestCompleted` 把结构化报文压成一行 `summary`,明细全丢 | 后端明明给了明细(见 #4) |
| 4 | `src/myssia/cli.py:2400-2463`(`_test_one_source`/`_fingerprint_view`) | `test.completed` 载荷自带:引擎退化链逐条失败(`failures[]`)、条目预览(`items[]`:fields+dedup_key+截断标记)、指纹判定(verdict+meaning) | 明细一应俱全,前端没用 |
| 5 | `sources-table.tsx:209-220` | 行内已有试抓 spinner(单飞期间全表试抓禁点) | 进行中态已有正确载体,顶部横幅冗余 |

## Requirements

- R1 试抓结果三形(事件成功形 / 事件失败形 / 发起失败形)一律进模态详情弹窗;试抓相关顶部横幅族整体撤除。
- R2 弹窗吃满既有结构化明细(**不新增协议**):状态、引擎(命中+配置)、条数、指纹判定、退化链逐条、条目预览(dedup_key+字段,截断如实标)、失败形 error 族逐条。
- R3 进行中态 = 行内 spinner(既有);提示实时输出在日志屏;「job #N」类行话不再上屏。
- R4 弹窗交互:ESC / 遮罩点击 / 关闭钮三径同关;只读无 dirty 守卫;提供「查看采集日志」深链(`#/logs`)。
- R5 零新 npm 依赖(手写 overlay,同 `YamlEditorDialog` 范式);sidecar 协议零变更。

## Acceptance Criteria

- [x] AC1 试抓完成后弹窗自动弹出(`role=dialog` + `aria-modal`),屏内不再有试抓结果/进行中常驻横幅(测试断言弹窗弹出+旧横幅 testid 清零)
- [x] AC2 成功形弹窗含:源名、引擎命中/配置、条数、指纹判定文案、退化链逐条(有失败时)、条目预览(dedup_key+字段;截断时「仅预览前 N 条」)(C13 用例一全断言)
- [x] AC3 失败形(事件 ok=false)弹窗含 error 族 + `data.errors` 逐条;发起失败(test_busy 等)同弹窗失败形(C13 用例二)
- [x] AC4 ESC/遮罩/关闭钮均关闭弹窗;进行中态仅行内 spinner(带日志屏提示 title),无「job #」字样上屏(断言 document.body 无「job #」)
- [x] AC5 `sources.test.tsx` C13 断言同步为弹窗断言;scoped vitest 我方 2 例绿(隔离树 17 过/3 红为并行线 5c188c0 预存 basename 债)+ `tsc --noEmit` 干净
- [x] AC6 提交 6d43209 五件全在 `screens/sources/` 内,零 package.json/types.ts/后端改动

> 真机目验(弹窗观感/交互手感)留主人;装机包未随本笔刷新(见完成汇报)。
> 混线注记:实现撞并行会话迁移排程一览/跑一次到 cron 屏(在途未提交),sources-screen/sources.test 两件经临时索引外科提交(只进我方 hunks,外来 hunks 原样留工作树),验证在 git archive 隔离树实跑门禁。

## 明确不在本档(留观,待主人裁决)

同屏「跑一次」终态横幅、「启停写回复核」横幅、存储告警条:同族贴顶模式,但各有任务出身(10-04-topbar-cleanup 等)且未被判词点名——不擅动,本档只修试抓一线。
