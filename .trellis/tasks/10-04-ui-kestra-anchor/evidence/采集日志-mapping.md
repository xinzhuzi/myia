# 采集日志屏 ↔ Kestra 源码对照(10-04-ui-kestra-anchor)

改动文件(白名单内):`desktop/ui-src/src/screens/logs/logs-screen.tsx`(单文件;
api.ts/test.tsx 带并行任务未提交改动,未触碰)。

## 对标件(只读参考,Apache-2.0;借结构改语义,文件头注明)

| Kestra 源件 | 借了什么 | MYIA 落法 |
|---|---|---|
| `ui/src/components/executions/Executions.vue`(research/kestra-executions-ref/) | KsDataTable 表行解剖:KsId mono id · KsEntityLink 品类位 · KsDateAgo inverted 相对时间 · Duration mono · KsExecutionStatus small 状态芯片 | 组头重排为定宽槽位列对齐(#id w-9 · 品类 flex-1 · 错误行数 w-16 · 条数 w-11 · 相对时间 w-[68px] · 耗时 w-14 · 芯片);槽常渲染(空占位)保列对齐 |
| `ui/src/styles/app.scss` `section.full-container` | 满高列表容器:列表内滚、过滤条常驻、children flex:1 | 屏根 `h-full min-h-0 flex-col`;waterfall `flex-1 overflow-y-auto`(实测 before 页滚 382px → after 内滚 803px 到底) |
| `ui/src/components/executions/Gantt.vue`(卡头) | 头部摘要组(total_duration/tasks 以「/」分隔)+ 行尾动作(copy all logs link 钮 + 状态) | 展开体 meta 条重构:「总耗时 X / N 行 / N 错误行 / logs.tail run_id=N」+ 右侧「复制日志」link 钮(Clipboard API,失败如实回显);testid run-log-meta-N 保留 |
| `design-system/.../KsExecutionStatus/KsExecutionStatus.vue` | small 档规格:高 1.5rem(24px)/字 xs(12px)/radius-sm(6px)/gap 4px/描边圆图标/状态色淡底 | 本地 StatusChip:60×24px、6px 圆角、12px、状态色 15% 底 + 描边圆图标(CircleCheck/CirclePlay/TriangleAlert/CircleX/CircleStop 对位 Kestra material 圆描边系) |

## 不抄 + 为什么

- **KsDataTable 复选/批量操作(change state/restart/replay/kill/delete/Set labels)**:MYIA 桌面
  单飞(单活跃 run,run_busy 协议在案),无批量域;R5 功能面零改动。
- **分页/服务端排序/列配置(KSFilter properties)/CSV 导出**:run.status 为内存注册表全量
  (数十条级),无分页协议;导出属功能面。
- **Gantt 逐任务时间条(DynamicScroller + KsProgress 条)**:协议无 taskRunList/逐步时间戳,
  假造进度条违反「像素与代码双真源」;以展开日志体对位 Gantt 行展开详情(TaskRunDetails)交互。
- **Executions 顶部统计图(Sections dashboard)**:屏内已有 run 状态分布条(终审修整轮加,
  测试在案),保留不动。
- **品类链接色(KsEntityLink 是 RouterLink)**:我们的品类不可点(行级折叠才是主交互),
  诚实用前景色不作链接色。

## 兼容性核验

- logs-screen.test.tsx 15/15(vitest run 实测);tsc --noEmit 0 错。
- 保留 testid:run-group-header-N/run-error-count-N/run-log-meta-N/run-log-hits-N/
  run-rerun-*/logs-filter-*/run-waterfall/run-status-distribution 等(测试断言的
  textContent 口径:品类/耗时/「N 条」/状态词/「N 行」全保留)。
