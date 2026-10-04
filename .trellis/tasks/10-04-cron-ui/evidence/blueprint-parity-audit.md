# 交付后蓝本并排审计(Hermes CronPage ↔ cron 屏,2026-10-04,只读审计员)

> 主人问「有与 Hermes 对比吗」触发。50 项特性对排 + 增量反核 + 偏离表复核。全文见会话;此处记结论与待办清单(权威行动版)。

## 结论

- 高危缺口:0。主流程(列表/创建/编辑/暂停恢复/删除/急停/历史/三态)全落位有测试;**12 项增量全部对得上 grill/PRD 决议,无越权增量**;B1-B7+grill 十决议与实现双向吻合。
- **未登记缺口 8 项**:中×2(G1/G2 错误可见性族)+ 中低×1(G3 name 表单)+ 低×5(G4 错误清列表/G5 列表计数/G6 校验不聚焦/G7 编辑不示 id/G8 reload 竞态守卫)。
- 文档勘误 3 处:R4 删除确认口径(PRD 写 Dialog/实现 window.confirm,design 已注册后者→PRD 勘误)、R7 PluginSlot 漏登记、R8 last_run 列隐式裁剪。
- 蓝本澄清:CronPage 本体无运行历史 UI(那是后端 routers 能力)——我方 F6 行内展开是注册增量,非对齐项。

## 待办(若批,零协议变更可落)

1. **G1+G2 同族修**:cronStatusBadge 加 state=error→destructive 分支;job 行补错误行渲染(last_error/last_delivery_error 红字,H1218-1233 对位)+ last_run_at 列(H1202-1204 对位,或并入展开);
2. **G3**:CronFormDialog 补 name 输入(可选;编辑 diff 已支持);
3. 低项打包:G4 reload 错误保留旧列表(data 不置 null)/G5 列表计数 (N)/G6 校验失败聚焦/滚动+展开折叠组/G7 编辑底部 job.id mono/G8 reload generation 守卫;
4. 勘误:prd F5「Dialog 确认」→window.confirm 对齐 design;design 偏离表补 PluginSlot 一行+last_run 裁剪条目。
