# 前端缺口普查:对标交互缺口+功能池余量+质量债(主人目验驱动)

## Goal

主人 2026-10-04 目验判例驱动:仪表盘报错处理已修(分区降级 commit);本档沉淀三层缺口矩阵——①对标交互缺口(teardown 可抄清单 vs 实装逐条核);②功能池余量终态;③质量债。附带真数据仪表盘无头复现证据(13 RPC 全绿,证明 internal_error 系并行在途构建实例)

## Requirements

### 一层口径:对标交互缺口逐条核(证据=代码实读)

- 对照 `archive/2026-10/10-03-ui-deep-imitation/research/` 三份 teardown 可抄清单(linear-activity 14 条 / vercel-dashboard 11 条 / linear-settings 9 条,共 34 条),逐条对 `desktop/ui-src/src` 现状核「已实装/部分/未做/在途」,每条附 file:line 证据;零命中以 rg exit=1 留痕。
- 10-04-interaction-batch 在途六件(⌘K 面板/右键菜单/快捷键底座/侧栏折叠/仪表盘时间范围/feed j-k)一律标「在途,勿重复立项」,只记工作树实况不路由。
- 每条差距给路由建议(直接小修 ≤20 行/立档/入 v12-backlog 池/关闭),只建议不执行;关闭项必须给语义理由。

### 二层口径:功能池余量终态(G 系逐项定性)

- ui-feature-census G1-G12 逐项标注终态(已做=归哪个任务/在途/留池/关闭),以当前工作树代码证据为准,不以池文档自述为准;发现池清单与实况漂移(如 v12-backlog 仍列已消号项)如实登记为文档债。
- 后续新增池项(snooze 到期重现/设置搜索/远期形态三项)一并核现状归属。

### 三层口径:质量债存量(fe-small-batch 残留+在案小件)

- 点名三项逐条核:P1(源管理排序键盘可达+destructive 徽章对比度)/旁核对比度三处(侧栏小字/日志错误行/设置 destructive 按钮)/text-2xs 是否清零;对比度项必须独立 WCAG 复算(方法与债档记录值校准吻合后方采信),不得只抄代码注释。
- 在案小件(AlertsFiredEvent 联合/suppressed 词表/消息屏真机手验/装机包版本号)复核现状并路由。

### 红线

- 不编辑 desktop/ 与 src/ 下任何文件(普查只读);档内引用先读原文核验;产出落 `research/matrix.md` + 回写本 prd。

## Acceptance Criteria

- [x] 三份 teardown 可抄清单 34 条全部逐条核,状态+file:line 证据齐(matrix.md §1.1-§1.3;零命中项留 rg exit 痕迹)
- [x] 在途六件全部标「在途,勿重复立项」,未对其重复路由(matrix.md §1 在途声明+各表)
- [x] G1-G12+后续池项逐项终态定性,已做项均回指归档任务与代码证据;池文档漂移(G5 主体/G7/G8/G12 未消号)已登记(matrix.md §2)
- [x] P1 两项/旁核三处对比度独立 WCAG 复算达标(6.46/4.67/4.73/5.87-6.14,旧值 4.15/3.41 复算吻合债档);text-[11px] 全树 rg 零命中(matrix.md §3.1)
- [x] 在案小件四项复核:AlertsFiredEvent 前置条件已满足(entry.py:2429 已实装)→ 路由小修;tauri.conf 版本 0.0.1 仍在;真机手验归 wrapup-checklist(matrix.md §3.2)
- [x] 处置路由汇总落档且只建议未执行(R1-R9,matrix.md 末节);本普查未动 desktop/ 与 src/ 任何文件
- [ ] (留主人)R1-R5 拍板与执行排期

## Notes

- Keep `prd.md` focused on requirements, constraints, and acceptance criteria.
- Lightweight tasks can remain PRD-only.
- For complex tasks, add `design.md` for technical design and `implement.md` for execution planning before `task.py start`.
