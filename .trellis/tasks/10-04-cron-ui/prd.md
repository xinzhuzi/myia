# 定时任务管理屏:照 Hermes CronPage 抄(桌面 cron UI)

## Goal

主人 2026-10-04 令立档:10-04-hermes-cron 已交付的定时底座(桌面即宿主+sidecar cron.* 九方法)补上可视化管理的皮。**蓝本 = Hermes web 控制台的 CronPage**(`~/.hermes/hermes-agent/web/src/pages/CronPage.tsx`,1294 行侧栏页)——模仿纪律:以其为准最大程度贴近;我们与 Hermes 的语义差(job=品类管线 job、无 profile/blueprint/skill 概念)按偏离表裁,不自由发挥。

**零协议变更**:九方法(cron.list/create/edit/pause/resume/run/remove/status/runs)与两事件(cron.completed/cron.skipped)已全部在库,本任务是纯前端薄壳(types.ts 前端镜像扩签名+client 门面+一屏),**不动 entry.py、无协议版本 bump**。

## Requirements

- **F1 入口**:侧栏主群新增「定时任务」(Clock 图标,排「源管理」后);HashRouter 加 `/cron` 路由(App.tsx `<Route path="cron">`),AppLayout 包裹。
- **F2 ticker 活性条**(蓝本 schedulerStaleAgeS 对位):屏首读 `cron.status`(心跳龄/最后错误/急停态/下次到期),僵死(>5min)黄条示警、急停态红条+「恢复全部」入口;镜像蓝本「调度器僵了页面会喊」。
- **F3 job 列表**(cron.list;table 基件):行=名称 / 排程人话(`schedule_display` 字段直读)/ 下次运行(逾期红标:now > next_run_at + grace)/ 上次状态四态色 badge(ok=success、failed=destructive、delivery_failed/skipped_busy=warning、paused=灰)/ deliver / repeat。含 `all=true` 切换显示暂停/终态(蓝本 Jobs 视图)。
- **F4 创建/编辑双 Dialog**(dialog 基件,蓝本双 Modal 对位):字段=schedule(自然语言/5 段 cron 手输,**parse 错误文案原样回显**)/category(绝对路径手填;create 即校验早失败的错误回显)/deliver spec/failure_deliver/repeat/timezone/run_timeout/dry_run(Switch)。编辑=same form 预填+cron.edit 部分更新。
- **F5 行内动作**:立即运行(cron.run,进行态 spinner+toast)/暂停(cron.pause,可填 reason)/恢复(cron.resume)/删除(cron.remove,Dialog 确认)。
- **F6 运行历史**:行展开(cron.runs):executions 尾查新→旧,status/finished_at/run_summary_json 摘要(状态/时长/留存/失败行);输出目录留 CLI 查看(档内注记)。
- **F7 刷新**:进屏全量拉 + 10s 轮询 + `cron.completed`/`cron.skipped` 事件即时刷新(toast+列表重拉);事件类型已在前端 SidecarEvent 联合。
- **F8 前端镜像纪律**:本屏消费的九方法签名入 types.ts SidecarProtocol mirror + client.ts 共享 `api` 门面(spec desktop/sidecar-protocol.md 纪律第 3 条)。

## 非目标(不抄清单)

- **Blueprints**(任务模板目录+实例化)——MYIA 无此概念,不造。
- **profile 多路选择器**——单数据根。
- **skills/model/provider/toolsets/prompt/monitor 表单族**——我们的 job 载荷是品类 YAML(对位 hermes-cron D2 偏离)。
- **前端排程翻译器**(蓝本 scheduleDescriber+i18n)——后端 `schedule_display` 已生成人话,直读;UI 全中文。
- **delivery-targets 选择器 API**——deliver 手输 spec(`feishu:群名`),附一行格式说明。
- 动 entry.py / 协议版本 / 后端任何文件。

## Constraints

- 蓝本对照:CronPage.tsx 的结构(列表行信息密度/逾期判定/双 Modal/触发 spinner/toast)逐块对照实现,组件 docstring 注明蓝本出处与行号段;偏离只出现在 design 偏离表。
- 逾期/僵死判定的前端镜像常量(grace、stale 阈值)与后端常量一致并注明出处(Hermes 前端同款做法:lib/cron-job.ts 镜像后端常量)。
- 遵守 desktop/frontend-ui.md token/基件纪律(基件 14 件,禁局部 ring/对比度红线);vitest 屏测 + tsc + build 三绿;不动并行线在途文件(树上有 ui-reskin-r2 线)。

## Acceptance Criteria

- [ ] AC1 入口:侧栏项+路由可达,屏在 AppLayout 内,导航态正确。
- [ ] AC2 活性条:status 数据渲染;模拟僵死/急停态的屏测各一(黄条/红条+恢复入口)。
- [ ] AC3 列表:mock 数据渲染全字段;四态色 badge 断言;逾期红标边界测试;all 切换。
- [ ] AC4 双 Dialog:创建全字段提交→cron.create 参数形状断言;parse 错误/category 校验错误回显断言;编辑预填+部分更新。
- [ ] AC5 动作四件:run(进行态+toast)/pause/resume/remove(确认)调用形状断言;删除需确认。
- [ ] AC6 历史:行展开渲染 runs;run_summary_json 摘要字段断言;空态。
- [ ] AC7 事件:cron.completed/cron.skipped 触发 toast+重拉(mock 事件流)。
- [ ] AC8 镜像:types.ts 九方法签名+client 门面;SidecarProtocol 对账测试同步(前端侧计数,若纪律要求)。
- [ ] AC9 回归:vitest 全量+tsc+build 三绿;entry.py 零改动(diff 空);蓝本对照 docstring 齐全。

## Grill 待决(三问带推荐,批复后回写)

Q1 位置:主群「源管理」后(推荐,情报域相邻)vs「消息」群;Q2 刷新:10s 轮询+事件即时(推荐)vs 纯事件;Q3 历史形态:行内展开(推荐,logs 屏先例)vs 独立 Dialog。
