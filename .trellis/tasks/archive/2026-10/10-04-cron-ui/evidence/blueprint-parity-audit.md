# 交付后蓝本并排审计(Hermes CronPage ↔ cron 屏,2026-10-04,只读审计员)

> 主人问「有与 Hermes 对比吗」触发。50 项特性对排 + 增量反核 + 偏离表复核。全文见会话;此处记结论与待办清单(权威行动版)。

## 结论

- 高危缺口:0。主流程(列表/创建/编辑/暂停恢复/删除/急停/历史/三态)全落位有测试;**12 项增量全部对得上 grill/PRD 决议,无越权增量**;B1-B7+grill 十决议与实现双向吻合。
- **未登记缺口 8 项**:中×2(G1/G2 错误可见性族)+ 中低×1(G3 name 表单)+ 低×5(G4 错误清列表/G5 列表计数/G6 校验不聚焦/G7 编辑不示 id/G8 reload 竞态守卫)。
- 文档勘误 3 处:R4 删除确认口径(PRD 写 Dialog/实现 window.confirm,design 已注册后者→PRD 勘误)、R7 PluginSlot 漏登记、R8 last_run 列隐式裁剪。
- 蓝本澄清:CronPage 本体无运行历史 UI(那是后端 routers 能力)——我方 F6 行内展开是注册增量,非对齐项。

## 待办(若批,零协议变更可落)

> **2026-10-04 Stage 6 已批执行,下四项全数落地勾销**(实现=desktop/ui-src/src/screens/cron/{cron-form.ts,cron-screen.tsx};测试=#20-#27 八用例,全量 23 文件/418 测试绿 + build 过 + entry.py diff 空):

1. ~~**G1+G2 同族修**~~ ✅:cronStatusBadge 加 state=error→destructive「已停摆」分支(cron-form.ts,优先于 last_status 派生,对位 H530)+ badge title=last_error 截断 120(H1158-1166);行下 last_error/last_delivery_error 条件红行 colSpan=9 各截 120(H1218-1233;我方无 last_fire_error,蓝本第三行不搬)+「上次运行」第九列 last_run_at 本地化空=「—」(H1202-1204);
2. ~~**G3**~~ ✅:CronFormDialog 主字段组最上补可选 name Input(placeholder「缺省取品类文件名」;create 非空才带键,edit 走 diff——buildPayload/fromJob 状态原本已备);
3. 低项打包 ✅:G4 reload 错误保留旧列表(data 不置 null,ErrorBox+旧表共存,对位 H629)/G5 工具行「共 N 个」=list.count(对位 H1092)/G6 校验失败 focus 首错+scrollIntoView+高级折叠先展开(对位 HJ cron-job.ts 77-85;repeat/run_timeout 数值前端校验文案=entry.py invalid_params 原文)/G7 编辑 footer font-mono job.id(对位 H1065-1068)/G8 reload generation 守卫(useRef 自增丢弃过期响应,对位 H625-661;代码审查项不设竞态测试);
4. 勘误 ✅:prd F5「Dialog 确认」→「window.confirm 确认(design 注册先例)」;design 偏离表补 B8 PluginSlot 不抄(无插件系统);last_run 裁剪疑虑随 G2a 全列展示消解(空=「—」,不裁剪)。
