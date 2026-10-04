# 仪表盘运行区 ↔ Kestra 源码对照(10-04-ui-kestra-anchor)

改动文件(白名单内):`desktop/ui-src/src/screens/dashboard/dashboard-screen.tsx`(单文件;
api.ts/反馈卡/sparkline/测试未触碰)。before 截图流程:dashboard-screen.tsx 在 HEAD
干净 → 临时 `git show HEAD:` 换回 → 截图 → 恢复 after 版(无 stash,零风险)。

## 对标件(只读参考,Apache-2.0;借结构改语义)

| Kestra 源件 | 借了什么 | MYIA 落法 |
|---|---|---|
| `executions/ExecutionRoot.vue` + `ExecutionRootTopBar.vue` | 执行页骨架:状态显著 + 到全量列表的出口(Overview ↔ Executions 列表互链) | 「近期 run 成功率」卡头右侧「全部 run →」出口(纯导航 #/logs);不搬整页 TopBar——MYIA 仪表盘是聚合屏非单执行详情页,页级动作已由应用 TopBar(全局跑一次)承担 |
| `executions/Executions.vue`(表行解剖,与采集日志屏同语言) | #id mono · 品类 · 相对时间(KsDateAgo inverted)· 耗时 mono · 状态芯片 | RecentRunRow 重排定宽槽位列对齐;条数槽常渲染保列齐 |
| `design-system/.../KsExecutionStatus.vue` | small 档芯片 + statusIcon(描边圆图标族) | RunStatusChip(屏内私有,24px/12px/6px 圆角/状态色淡底);运行中图标呼吸(animate-pulse) |
| `executions/ExecutionPending.vue`/`ExecutionProgress.vue`(进行中态常驻) | 活跃 run 的常驻运行态呈现 | 活跃行:主色左缘(border-l-primary + bg-primary/5)+ 芯片呼吸 + 「日志 →」直采链接(采集日志屏自动展开跟随活跃 run,跨屏闭环) |

## 不抄 + 为什么

- **ExecutionRoot 的 Tabs 盒条(Gantt/Topology/Logs/Overview…)**:MYIA 仪表盘是七屏
  聚合首页,各域已有专屏(采集日志/源管理/…),页内 Tabs 会造二级导航与侧栏冗余。
- **TopBar 状态动作族(restart/replay/kill/pause/resume/delete)**:均为执行域写操作;
  MYIA 对应能力 = 采集日志屏行级重跑(G7 在案)+ 协议 run.cancel(未授权上屏,不加功能面)。
- **TriggerFlow 主按钮**:全局跑一次已在应用 TopBar(在案),卡内再加触发钮 = 重复入口;
  品类卡跑一次(icon ghost)保留原样——Kestra 列表行内触发同为小图标钮。
- **Metrics/Outputs 表**:协议无对应域。

## 兼容性核验

- dashboard-screen.test.tsx 36/36(vitest run 实测);tsc --noEmit 0 错。
- 保留断言面:run-success-rate 父级「N/M 次成功」「N 个运行中」、recent-run-N testid
  (getAllByTestId(/^recent-run-/) 计数)、「已取消」标签、「还没有 run 记录」空文案。
- Link → a[href="#/logs"]:HashRouter 下等价导航,且免 Router 上下文(测试直渲染屏组件)。
