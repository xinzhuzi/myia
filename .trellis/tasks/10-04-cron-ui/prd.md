# 定时任务管理屏:照 Hermes CronPage 抄(桌面 cron UI)

## Goal

主人 2026-10-04 令立档:10-04-hermes-cron 已交付的定时底座(桌面即宿主+sidecar cron.* 九方法)补上可视化管理的皮。**蓝本 = Hermes web 控制台的 CronPage**(`~/.hermes/hermes-agent/web/src/pages/CronPage.tsx`,1294 行侧栏页)——模仿纪律:以其为准最大程度贴近;我们与 Hermes 的语义差(job=品类管线 job、无 profile/blueprint/skill 概念)按偏离表裁,不自由发挥。

**零协议变更**:九方法(cron.list/create/edit/pause/resume/run/remove/status/runs)与两事件(cron.completed/cron.skipped)已全部在库,本任务是纯前端薄壳(types.ts 前端镜像扩签名+client 门面+一屏),**不动 entry.py、无协议版本 bump**。

## Requirements

- **F1 入口**:侧栏主群新增「定时任务」(Clock 图标,排「源管理」后);HashRouter 加 `/cron` 路由(App.tsx `<Route path="cron">`),AppLayout 包裹。
- **F2 ticker 活性条**(蓝本 schedulerStaleAgeS 对位):屏首读 `cron.status`(heartbeat_age/last_error/**writer_alive**/estopped/next_due_at),僵死(`!writer_alive || heartbeat_age>180s`)黄条示警;急停态红条;**双向操作**(grill Q6):「急停全部」红钮+Dialog 确认(cron.pause all)与红条上「恢复全部」(cron.resume all)。
- **F3 job 列表**(cron.list;table 基件):行=名称 / 排程人话(`schedule_display` 字段直读)/ 下次运行(逾期红标:now > next_run_at + grace)/ 上次状态四态色 badge(ok=success、failed=destructive、delivery_failed/skipped_busy=warning、paused=灰)/ deliver / repeat。含 `all=true` 切换显示暂停/终态(蓝本 Jobs 视图)。
- **F4 创建/编辑双 Dialog**(dialog 基件,蓝本双 Modal 对位):字段=schedule(**常用模板 chips**点击填入仍可改:每 30 分钟/每小时/每天 9 点/工作日 9 点/每周一 9 点;自然语言/5 段 cron 手输,**parse 错误文案原样回显**)/**category 下拉选择器**(grill Q4:吃现成 `yaml.list` 列品类 YAML,坏文件 `parse_ok:false` 行禁选带标;留「手输入口」兜底)/deliver spec(附格式说明)/failure_deliver/repeat/**config(pools YAML,可选高级)**/timezone/run_timeout/dry_run(Switch)。编辑=same form 预填+cron.edit 部分更新。
- **F5 行内动作**:立即运行(cron.run,进行态 spinner+notice)/暂停(cron.pause,可填 reason)/恢复(cron.resume)/删除(cron.remove,Dialog 确认)。反馈用**屏内持久 notice 横幅**(messaging 先例,库内无浮动 toast,不引新组件——grill 事实校准)。
- **F6 运行历史**:行展开(cron.runs):executions 尾查新→旧,status/finished_at/run_summary 摘要(状态/时长/留存/失败行);输出目录留 CLI 查看(档内注记)。
- **F7 刷新**(grill Q2 修正案):**事件驱动为主,不引入 interval 轮询**(全仓 UI 零轮询先例)——进屏拉全量 + `cron.completed`/`cron.skipped` 事件即时重拉(notice 吃事件载荷 name/status)+ 手动刷新按钮;逾期红标走时用**本地 1 分钟时钟重渲染**(纯前端 tick,不重取数据)。**前置:两事件尚不在 TS `SidecarEvent` 联合**(现 8 员)——本任务补两事件 interface+入联合,并照 alerts.fired 先例同步适配 logs 屏 `eventToRow` 穷尽守卫(runId=null 系统摘要行;深化实证,原稿「事件已在前端联合」系误写)。
- **F8 前端镜像纪律**:本屏消费的方法(cron 九+yaml.list 复用)签名入 types.ts SidecarProtocol mirror(现 35 方法不含 cron.*,补齐=mirror 对账非协议变更)+ client.ts 共享 `api` 门面(client.test.ts 逐方法批断言同步,非计数式)。

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
- [ ] AC4 双 Dialog:创建全字段提交→cron.create 参数形状断言;parse 错误/category 校验错误回显断言;**chips 点击填入断言;category 选择器渲染 yaml.list 数据、坏文件行禁选、手输兜底**;编辑预填+部分更新。
- [ ] AC5 动作四件:run(进行态+toast)/pause/resume/remove(确认)调用形状断言;删除需确认;**急停全部(确认 Dialog)/恢复全部**断言。
- [ ] AC6 历史:行展开渲染 runs;run_summary_json 摘要字段断言;空态。
- [ ] AC7 事件与刷新:cron.completed/cron.skipped 触发 notice(载荷 name/status 断言)+重拉(mock 事件流,messaging 式传输层 mock+emitSidecarEvent 注入);手动刷新;**无 interval 轮询断言(实现审查项)**;逾期红标跨分钟走时(本地时钟 tick);**SidecarEvent 联合补两事件后 logs 屏穷尽守卫同步适配(runId=null 系统行断言)**。
- [ ] AC8 镜像:types.ts 方法签名(cron 九+yaml.list 复用)+两事件 interface 入联合;client 门面 + **client.test.ts 逐方法批断言**(对账形态=typeof 断言非计数,深化实证);status 返回键名按 ground-truth §1 逐字(ticker_alive/heartbeat_age_seconds/…)。
- [ ] AC9 回归:vitest 全量+tsc+build 三绿;entry.py 零改动(diff 空);蓝本对照 docstring 齐全。

## Grill 决议(2026-10-04 批复:六问全按推荐)

Q1 位置=主群「源管理」后 / Q2 刷新=**事件驱动+手动刷新+本地时钟 tick,不引入 interval 轮询**(全仓 UI 零轮询先例)/ Q3 历史=行内展开 / Q4 category=**yaml.list 下拉选择器**(坏文件带标禁选)+手输兜底 / Q5 schedule=**模板 chips**(五种,填入仍可改)/ Q6 急停=**双向**(急停全部红钮+确认 Dialog;恢复全部)。

**事实裁决五条**(grill 前源码坐实,随批生效):①协议形状五件(list=完整 job 记录/status 含 writer_alive+estopped+next_due_at/runs 钳 [1,500] 带解析摘要/事件载荷 skipped{reason,active_run_id}+completed{ok,status,delivery_error,summary});②**逾期 grace=15 分钟照抄**(H hermes_cli/cron.py:630,过点还在跑是常态);③僵死判据=`!writer_alive || heartbeat_age>180s`;④toast/confirm 先例在(messaging/feed 的 toast、window.confirm spy 先例);⑤screens 零 setInterval(→Q2 修正依据)。Round 2 依赖项随决议落定:选择器坏文件行=禁选带标、chips 仅填入与错误回显零耦合。
