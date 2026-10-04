# Implement:10-04-cron-ui

> 蓝本先读:`~/.hermes/hermes-agent/web/src/pages/CronPage.tsx`(行号地图=research/hermes-cronpage-map.md)+ `web/src/lib/cron-job.ts` 全文;MYIA 侧先读 **research/myia-ground-truth.md(参数键名/事件联合缺口/notice/先例全在)** + spec desktop/sidecar-protocol.md(镜像纪律)+ frontend-ui.md(token/基件红线)。

## Stage 0:基线与占地

- [ ] 0.1 `git status` 核 sidebar.tsx/App.tsx/types.ts 是否被 ui-reskin-r2 线占用;被占=等待环 4min×20 轮,仍占则 patch 交收口
- [ ] 0.2 `npm --prefix desktop/ui-src run test` + `run build` 基线绿记录

## Stage 1:骨架与数据层

- [ ] 1.1 types.ts:cron 九方法+yaml.list 复用签名入 SidecarProtocol mirror(参数键名按 ground-truth §1 逐字)+ **CronCompleted/CronSkipped 事件 interface 入 SidecarEvent 联合 + logs/api.ts eventToRow 穷尽守卫适配(runId=null 系统行,alerts.fired 先例)**;client.ts 共享门面 + client.test.ts 逐方法批断言(F8/AC8)
- [ ] 1.2 screens/cron/ 建骨架:路由(App.tsx)+侧栏项(sidebar.tsx)+空屏三态;api.ts invoke 封装
- [ ] 1.3 cron-form.ts:emptyCronJobForm/fromJob/buildPayload + 常量镜像(grace/stale 注双向出处)
- 测试:骨架渲染+路由可达

## Stage 2:列表与活性

- [ ] 2.1 活性条(status;僵死黄条判据 `!writer_alive||heartbeat_age>180s`;estopped 红条+**双向:急停全部红钮+确认 Dialog/恢复全部**,grill Q6)
- [ ] 2.2 job 列表(table;全字段+四态 badge(蓝本 STATUS_TONE 映射表形态,H 526-532)+逾期红标(15min grace)+all 切换;行内展开模式照 logs 屏 expanded Set+惰性拉取)
- 测试:四态色断言/逾期边界/空态/僵死与急停各一(**messaging 式传输层 mock+emitSidecarEvent 注入**,ground-truth §6)

## Stage 3:双 Dialog 与动作

- [ ] 3.1 创建 Dialog(**schedule 五种模板 chips**+手输;**category=yaml.list 选择器**坏文件禁选+手输兜底;全字段+错误回显:create 的 parse/category 校验错误)
- [ ] 3.2 编辑 Dialog(预填+部分更新)
- [ ] 3.3 行内动作:run(spinner+toast)/pause(reason)/resume/remove(确认)
- 测试:提交参数形状断言/错误回显断言/确认流

## Stage 4:历史与事件

- [ ] 4.1 行内展开 runs(cron.runs;run_summary_json 摘要;空态)
- [ ] 4.2 刷新(grill Q2 修正案):订阅模式照 messaging 811-837(cancelled+unlisten)消费 cron.completed/cron.skipped→**notice 横幅**(messaging 先例)+重拉;手动刷新按钮;逾期红标本地 1min 时钟重渲染;**不引入 interval 轮询**
- 测试:事件驱动重拉断言(mock 事件流)

## Stage 5:门禁与收口

- [ ] 5.1 `npm --prefix desktop/ui-src run test` + `run build`(tsc+vite)三绿;entry.py `git diff` 空(零协议变更)
- [ ] 5.2 docstring 蓝本标注终核(design §1 对照表逐行勾销)
- [ ] 5.3 spec 更新:desktop/sidecar-protocol.md 前端镜像面注一笔(消费方+1,方法不加);frontend-ui.md 若有屏清单则补
- [ ] 5.4 pathspec 提交(feat(desktop): 定时任务管理屏);grill 六问决议已批(2026-10-04 全按推荐)随批入 prd/design,无待回写项

## 验证命令速查

```bash
npm --prefix desktop/ui-src run test
npm --prefix desktop/ui-src run build
git diff --stat -- desktop/entry.py   # 应为空
```

## 回滚点

- Stage 5 前:删 screens/cron/ + 还原三个接线文件即净回滚;零数据/协议残留。
