# 情报流微信品类渠道(按 TG UI 形态对齐)

## Goal

情报流新增微信渠道:品类 yaml+引擎对接 wechat-bridge 桥(像素链读)入管线 store/dedup+feed 层微信 tab/品类卡对齐 TG 形态;G3 决议由主人本指令翻案(读回仅展示→入情报流)

## Requirements

- 品类配置:数据根 `config/weixin.yaml` 种入(生产真相源判例);仓库 `config/` 保持缺省关(隐私缺省)。红线字段 `enrich.enabled:false`(私有内容不送 LLM)/`push:[]`/`retention` 一个字节不动。
- 引擎对接:`wechat_local` 引擎经 wechat-bridge 桥像素链读(截屏+OCR,零点击),消息→条目入 store,锚=`wechat-local://chat/<chat>#wx-<sha1(chat|ts|side|text)>` 内容哈希锚(design.md §2.3)。
- 调度:cron job `*/30 * * * *` 注册进数据根 `cron/jobs.json`(微信监控,id `0e9f2daf2d6a`);宿主=桌面 sidecar(home 模式)或 `myssia cron serve`。
- feed 层:微信 tab/品类卡对齐 TG 形态(代码+mock 测试层交付,design.md 验收矩阵)。

## Acceptance Criteria

- [x] 结构化空态链路健康:引擎真拉 exit 0、runs 表账目在册、不可读态(`chat_title_unreadable`)如实弃载荷不张冠李戴、itemsStored=0 如实(research/pull-verification.md §2,run 102/103/104)。
- [x] cron 自动线已验(2026-10-13 05:44,dev serve 代行宿主):ticker 复活后首个 tick 自动派发 05:30 积压刻度(kind=late,lateness 849.4s 诚实记账),`jobs.json` `last_run_at` null→`05:44:10+08:00`、`repeat.completed` 0→1、`next_run_at` 重锚 06:00、`last_status=ok`;executions 账本 `source=tick` 行;run_id=107 入库;验后 serve 干净停、进程零残留(research/pull-verification.md §7)。生产常态宿主=桌面 sidecar,启停归主人/主会话运维。
- [ ] 条目级三件套——**明示顺延至后续任务(归主会话调度),勿再悬空**:库内 `wechat-local://chat/%` 锚实例 ≥1 + dedup 同锚沉默(同窗重读零新增)+ feed 屏非空。顺延依据:静默铁律(不点击/不滚动/不激活)禁止验收方把微信主窗带屏(判例 research/pull-verification.md §3,2026-10-13 05:41 重探窗口仍 onscreen:false/mean_luma=28/OCR 0 行,客观不可达)。补验口径(前置=主人保持微信主窗可见+目标会话打开,「文件传输助手」设为当前会话):**执行宿主=手动 CLI(终端上下文;判例 run 105/106/107——AX 辅助功能按宿主进程算,终端有授权读通;生产 sidecar 自动轮 run 108 `ax_permission_denied` 实证,须先修 AX「系统设置→隐私与安全性→辅助功能给 MYIA 授权」方可走)**;重拉前后 `dedup_total` 与锚计数对照、同参数二轮同锚沉默,全形状级零消息文本(AX 缺口全档见 research/pull-verification.md §9)。

## Notes

- 私有数据红线:微信消息内容只入库(myssia.db 属私有),不入 git/日志/报告原文;一切证据形状级(条数/盖戳名/哈希锚,零消息文本)。
- Keep `prd.md` focused on requirements, constraints, and acceptance criteria.
- Lightweight tasks can remain PRD-only.
- For complex tasks, add `design.md` for technical design and `implement.md` for execution planning before `task.py start`.
