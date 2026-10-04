# Hermes CronPage 蓝本行号地图(cron-ui,2026-10-04 实读)

> `H = ~/.hermes/hermes-agent`;蓝本=`H/web/src/pages/CronPage.tsx`(1294 行)。实现每块前读对应段;偏离见 design §3(B1-B7)。

| 段(行号) | 内容 | cron-ui 对位 |
|---|---|---|
| 62-76 | formatTime/asText/truncateText 工具 | 本屏同款小工具(时间本地化/截断) |
| 82-141 | NameCheckboxPicker(skills 多选) | **不抄**(B3) |
| 143-175 | emptyCronJobForm/editorFormFromJob/buildPayload 三函数 | cron-form.ts 状态机对位(字段裁成我们的八件+config) |
| 197-348 | CronAdvancedFields(monitor/script/interpreter 等高级区) | **不抄**(B3);我们高级区=config/timezone/run_timeout/dry_run 折叠区 |
| 348-450 | CronJobFormFields 主表单 | 双 Dialog 表单布局对位(schedule/category/deliver/failure_deliver/repeat) |
| 450-524 | 行显示辅助:getJobName/Title/ScheduleDisplay/State/RepeatDisplay/Mode/jobKey/profileLabel | 同族小函数(四态 badge/人话排程直读 schedule_display/repeat 显示) |
| **526-532** | **STATUS_TONE 状态→色映射**(enabled/scheduled=success、paused=warning、error/completed=destructive) | 我们的四态映射(ground-truth §7);Hermes 的 completed=destructive 与我们终态语义不同,不照搬色,照搬「state→tone 映射表」形态 |
| 534-700 | CronPage 主组件:triggerController(spinner)/profiles/view(jobs\|blueprints)/i18n/双 Modal 状态(create+edit)/availableSkills 等 | 屏状态机骨架(裁掉 profiles/blueprints/skills/model 族);双 Dialog 状态对位 createModalOpen/editJob/creating/saving |
| 895-905 | Toast+LoadErrorNotice(加载失败横幅+重试) | notice 横幅(MYIA 先例非蓝本组件)+错误重试 |
| 907-921 | schedulerStaleAgeS 黄条(data-testid=cron-scheduler-stale)+Segmented 视图切换 | 活性条(判据=writer_alive/heartbeat_age_seconds,grill Q6 双向);Segmented **不抄**(单视图) |
| 923+ | blueprints 分支 | **不抄**(B1) |
| 930+ | DeleteConfirmDialog(独立确认组件,title+truncate 描述+loading) | 删除确认 Dialog 对位(truncate 名称) |
| 940-1000 | 创建 Modal:遮罩(fixed inset-0 z-100 遮罩点击关)+max-w-3xl max-h-90vh+aria-modal+关闭钮 | 双 Dialog 形态对位(dialog 基件承载,aria 同款) |
| 1000-1290 | job 列表渲染:行(name/title/schedule 人话+next_run 逾期红标 cronNextRunOverdueMs(15min grace)/state Tone/last_run/repeat/mode)+行内动作(Trigger spinner/pause/resume/edit/delete)+runs 展开区 | table 行+动作簇+行内展开(logs 屏先例)逐块对位 |
| lib/cron-job.ts 全文 198 行 | 表单模型/`cronLastResult`/`cronNextRunOverdueMs`(镜像 `_OVERDUE_GRACE_SECONDS=15*60`)/`cronSchedulerStaleAgeS`(镜像 STALE_AFTER) | cron-form.ts 常量镜像段(grace=15min 双向注释 H cron.py:630) |
| lib/cron-trigger-controller.ts | 手动触发进行态(键 Set+回调) | run 动作 spinner 键 Set(简化:cron.completed 事件清) |
