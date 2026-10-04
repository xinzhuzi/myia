# 跑一次终态横幅改详情弹窗+进行中行话清理(cron 屏)

## Goal

10-05-test-result-dialog grill Q3a+b 决议(主人 2026-10-05「按推荐」批):cron 屏排程一览的「跑一次」回显沿用判词同族错误——终态详情(成功/部分/失败+exit code)贴屏顶常驻横幅、进行中横幅带「异步 run #N」行话。本档对齐试抓结果弹窗同款范式:终态/发起失败进模态详情弹窗,进行中清话术,行话不上活性面。

## 现状证据

- `desktop/ui-src/src/screens/cron/cron-screen.tsx:603-640`:`runOnce` 三横幅——进行中(`run-once-running`,文案「异步 run #N」行话)/终态(`run-once-ok|fail`,`跑一次 x 完成(run #N · 成功…)`贴顶常驻)/发起失败(`run-once-error` 红条)
- 终态后 `reload()` 刷新健康度(既有行为,弹窗化后保留)
- 蓝本同物种参照:试抓弹窗 `test-result-dialog.tsx`(10-05-test-result-dialog,判词「这种提示做详情弹窗」同款)

## Requirements

- R1 终态(phase=done)与发起失败(phase=error)进模态详情弹窗(手写 overlay 范式,零新依赖);撤对应贴顶横幅
- R2 弹窗内容:品类名+状态徽章(成功=ok/部分=warning/失败=destructive,如实分级沿用 runDoneTone 语义)、终态说明(status/exit code/终态未知如实,trace 值收 mono 技术小字)、失败形发起错误(code:message);底部「查看采集日志」深链(#/logs)+关闭。本屏无健康度面不 reload(既有语义,如实注记);实现取屏内既有 Dialog 基件(job 编辑同款,Radix 承担 ESC/遮罩/X 与焦点),不再造第三份手写 overlay
- R3 进行中态保留横幅但清行话:「异步 run #N」删,保留日志屏深链与 spinner(活性条行话判例;run_id 类 trace 值可进弹窗技术小字)
- R4 完成即弹(Q1 决议同物种:发起即等待);ESC/遮罩/X 三径同关;样式全 token
- R5 启停复核横幅、存储/复核告警条按 grill 决议保留,零改动;协议/后端零改动

## Acceptance Criteria

- [x] AC1 done/error 两形弹模态弹窗(role=dialog aria-modal),cron 屏内无 run-once 终态/错误横幅;进行中横幅在且无「run #」字样
- [x] AC2 弹窗含品类名/状态徽章(三分色)/终态或错误明细/trace 技术小字(run_id/status/exit)/采集日志深链;终态不 reload(本屏无健康度面,既有语义)
- [x] AC3 ESC/遮罩/X 三径关;新发起即关旧弹窗(起手置 null)
- [x] AC4 cron-screen.test.tsx 跑一次用例断言同步弹窗;scoped vitest 全绿+tsc --noEmit 过
- [x] AC5 改动只在 cron 屏目录+测试;零 package.json/协议/后端

## Notes

- 轻量任务,PRD-only(横幅→弹窗的完整范式已由 test-result-dialog 落定,本档为同款移植)
- 手写 overlay 已第三处(YamlEditor/TestResult/RunOnce)——共享基件抽取记 backlog,不在本档

> 收口(2026-10-05):AC1-5 全勾——cron scoped 34/34 绿+全量 428/428 绿+tsc 0;进行中横幅「run #」反向断言在;终态/发起失败/关闭(基件 X)/trace 技术小字均有断言。真机目验留主人。
