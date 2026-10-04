# Implement:10-04-cron-ui

> 蓝本先读:`~/.hermes/hermes-agent/web/src/pages/CronPage.tsx`(行号地图=research/hermes-cronpage-map.md)+ `web/src/lib/cron-job.ts` 全文;MYIA 侧先读 **research/myia-ground-truth.md(参数键名/事件联合缺口/notice/先例全在)** + **research/types-draft.md(接口逐字抄,落地时对源复核)** + **research/screen-spec.md(布局契约+18 条测试用例清单)** + spec desktop/sidecar-protocol.md + frontend-ui.md。

## Stage 0:基线与占地

- [x] 0.1 `git status` 核 sidebar.tsx/App.tsx/types.ts 是否被 ui-reskin-r2 线占用;被占=等待环 4min×20 轮,仍占则 patch 交收口(收口核:树上占线实为 10-04-ui-kestra-anchor——sidebar.tsx 混该线 Kestra 重锚大改,cron 份仅 Clock import+导航项两 hunk,收口期 hunk 分离提交;App/types/client/logs 五文件 diff 纯 cron 无混)
- [x] 0.2 `npm --prefix desktop/ui-src run test` + `run build` 基线绿记录(收口期复跑代替:23 文件/409 测试全过+build 1.99s 三绿,存证见 journal 收口段)

## Stage 1:骨架与数据层

- [x] 1.1 types.ts:cron 九方法+yaml.list 复用签名入 SidecarProtocol mirror(**按 research/types-draft.md 逐字抄后对源复核**,可选键边界 `?:` 以后端「显式才有」为准)+ **CronCompleted/CronSkipped 事件 interface 入 SidecarEvent 联合 + logs/api.ts eventToRow 穷尽守卫适配(runId=null 系统行,alerts.fired 先例)**;client.ts 共享门面 + client.test.ts 逐方法批断言(F8/AC8)
- [x] 1.2 screens/cron/ 建骨架:路由(App.tsx)+侧栏项(sidebar.tsx)+空屏三态;api.ts invoke 封装
- [x] 1.3 cron-form.ts:emptyCronJobForm/fromJob/buildPayload + 常量镜像(grace/stale 注双向出处)
- 测试:骨架渲染+路由可达

## Stage 2:列表与活性

> 布局与列定义按 research/screen-spec.md §1-§2 契约执行。

- [x] 2.1 活性条(status;三态:正常/僵死黄条 `!ticker_alive||heartbeat_age_seconds>180s`/急停红条;**双向:急停全部红钮+确认 Dialog/恢复全部**,grill Q6)
- [x] 2.2 job 列表(table;全字段+四态 badge(蓝本 STATUS_TONE 映射表形态,H 526-532)+逾期红标(15min grace)+all 切换;行内展开模式照 logs 屏 expanded Set+惰性拉取)
- 测试:按 **research/screen-spec.md §5 用例清单 #1-#18** 逐条落(编号对应 AC);mock=messaging 式传输层+emitSidecarEvent(ground-truth §6)

## Stage 3:双 Dialog 与动作

- [x] 3.1 创建 Dialog(**schedule 五种模板 chips**+手输;**category=yaml.list 选择器**坏文件禁选+手输兜底;全字段+错误回显:create 的 parse/category 校验错误)
- [x] 3.2 编辑 Dialog(预填+部分更新)
- [x] 3.3 行内动作:**run=排队语义(grill 二 Q1:notice「已排队,≤60 秒内开始」+行短时「已排队」态,completed 事件刷新)**/pause(reason)/resume/remove(确认);estopped 下单 job 操作照常开放(Q4)
- 测试:提交参数形状断言/错误回显断言/确认流

## Stage 4:历史与事件

- [x] 4.1 行内展开 runs(cron.runs;run_summary_json 摘要;空态)
- [x] 4.2 刷新(grill Q2 修正案):订阅模式照 messaging 811-837(cancelled+unlisten)消费 cron.completed/cron.skipped→**notice 横幅**(messaging 先例)+重拉;手动刷新按钮;逾期红标本地 1min 时钟重渲染;**不引入 interval 轮询**(收口核:screens/ 全树唯一 setInterval = cron-screen.tsx:566 的 1min 时钟,测试断言 tick 零取数)
- 测试:事件驱动重拉断言(mock 事件流)

## Stage 5:门禁与收口

- [x] 5.1 `npm --prefix desktop/ui-src run test` + `run build`(tsc+vite)三绿;entry.py `git diff` 空(零协议变更)(收口实测:409 测试/23 文件全过、build 1.99s、`git diff --stat -- desktop/entry.py` 空)
- [x] 5.2 docstring 蓝本标注终核(design §1 对照表逐行勾销)(收口抽核:cron-screen.tsx:55-60 活性条对位 H 907-921;cron-form.ts:149/152/176 常量镜像与 STATUS_TONE 526-532 出处注齐)
- [x] 5.3 spec 更新:desktop/sidecar-protocol.md 前端镜像面注一笔(消费方+1,方法不加);frontend-ui.md 若有屏清单则补(七屏→八屏;CHANGELOG Unreleased Added 同批入)
- [x] 5.4 pathspec 提交(feat(desktop): 定时任务管理屏);grill 六问决议已批(2026-10-04 全按推荐)随批入 prd/design,无待回写项

## Stage 6:蓝本对排缺口修复(2026-10-04 交付后审计追设;~~待主人批~~ **已批已执行完毕**,见下方勾选与 evidence 勾销)

> 出处=evidence/blueprint-parity-audit.md(50 项对排);全部零协议变更。规格已展开到执行级(文件:行/形状/蓝本对位/测试);事实核:error 态 job 保持 enabled → 缺省列表可见,纯前端可修。

- [x] 6.1 **G1+G2 错误可见性族**(中×2)(2026-10-04 落地:cron-form.ts `cronStatusBadge`/`truncateCronText` + cron-screen.tsx 第九列/红行/badge title;#20/#21/#22 过)
  - G1 badge:cron-form.ts:199-204 `cronStatusBadge` 抢占序=paused→「已暂停」/completed→「已完结」/**新增 `state=error`→destructive「已停摆」(优先于 last_status 派生,对位 H530)**;badge 加 `title={job.last_error}`(悬浮细节,对位 H1158-1166)
  - G2a 列:表加**第九列「上次运行」**(排「下次运行」后,~140px,`job.last_run_at` 本地化,空=「—」;对位 H1202-1204;注意 list 已富化 `latest_execution` 可作交叉)
  - G2b 行下错误红行:主行之后、展开钮行之前,条件渲染 `<TableRow><TableCell colSpan={9} className="text-destructive">`:`last_error`(前缀「上次错误:」)与 `last_delivery_error`(前缀「投递错误:」)各一行、截断 120,仅有值时渲染(对位 H1218-1233 三红行;我方无 last_fire_error 字段)
  - 测试 #20/#21/#22(见 screen-spec §5 增补)
- [x] 6.2 **G3 name 表单**(中低)(落地:cron-screen.tsx CronFormDialog 主字段组最上 name Input;buildPayload/fromJob 状态原本已备;#23 过)
- [x] 6.3 低项打包(全落:cron-screen.tsx reload 保留旧数据+generation 守卫/工具行计数/pendingFocus 聚合聚焦/编辑 footer id;#24-#27 过;G8 代码审查项)
  - G4:reload 错误分支**不清列表**(cron-screen.tsx:115 一带):错误入 error state,ErrorBox 显示但 jobs 保留旧值(对位 H629「错误条+旧列表共存」);#24
  - G5:工具行右侧「共 N 个」=当前行数(all 开关联动;对位 H1092);#25
  - G6:提交校验失败→focus 首个错字段+`scrollIntoView({block:"center"})`;错误字段在高级折叠内则先展开再聚焦(对位 HJ:77-85 focusCronField);#26
  - G7:编辑 Dialog footer 左侧 `font-mono` 显示 job.id(对位 H1065-1068);并入 #27
  - G8:reload 加 generation 计数守卫(useRef 自增、过期响应丢弃;对位 H625-661);实现审查项(代码存在性,不写竞态测试)
- [x] 6.4 文档勘误:prd F5「Dialog 确认」→「window.confirm 确认(design 注册先例)」;design 偏离表补 **B8 PluginSlot 扩展槽不抄(无插件系统)**;审计报告 evidence 勾销对应项(2026-10-04 三处均已改)
- [x] 6.5 门禁复跑(vitest+build+entry.py diff 空)+ pathspec 提交 fix(desktop);screen-spec §2/§5 随改随更(九列/错误行/#20-#27)(执行批门禁 2026-10-04 过:23 文件/418 测试全绿、build 1.93s、`git diff --stat -- desktop/entry.py` 空;screen-spec §2/§5 核对与实现一致;pathspec 提交按 Stage 6 交办「不 commit」暂缓→**收口会话补落**:门禁复跑同绿=23 文件/418 测试 5.06s+build 1.96s+entry.py diff 空,fix(desktop) 一笔+docs(task) 一笔随收口入库)

## 验证命令速查

```bash
npm --prefix desktop/ui-src run test
npm --prefix desktop/ui-src run build
git diff --stat -- desktop/entry.py   # 应为空
```

## 回滚点

- Stage 5 前:删 screens/cron/ + 还原三个接线文件即净回滚;零数据/协议残留。
