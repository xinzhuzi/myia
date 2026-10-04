# 空态引导态 ↔ Kestra 源文件对照(10-04-ui-kestra-anchor 道-B)

对标件(只读参考,Apache-2.0,借结构改语义):
- `kestra/ui/packages/design-system/src/components/Data/KsEmptyState.vue`
- `kestra/ui/src/components/flows/NoExecutions.vue`
- `kestra/ui/src/components/onboarding/execution/OverviewBottom.vue` + `OverviewCard.vue`

## 借了什么(结构→语义)

| Kestra 结构 | 我们的落点 |
|---|---|
| KsEmptyState:左对齐 inner(max-w 370) artwork 120px+title xl semibold+description+actions 行,块间 gap 21px,section 呼吸 3rem | FirstRunGuide:MyssiaMark 48px+品牌光晕(自有品牌层)+标题 text-xl semibold+说明 text-sm(交代 pluginsDir)+「一键跑 demo」主钮;块间 gap-5(20px≈21),py-16 |
| NoExecutions:「need help」标签(sm 次级色)+ OverviewBottom 引导卡列表 | 「需要指引?」text-xs muted + 三张指引卡(边框堆叠 rounded-lg+divide:图标 16px+标题 sm medium+描述 2xs+chevron;hover bg-accent) |
| OverviewCard:icon+text(title/desc)+OpenInNew/ChevronRight 尾图标,行 padding spacing-4/5,hover bg-hover+图标提色 | 同构;卡内容=我域指引:模板新建品类(→配置编辑)/采集结果在日志屏(→日志)/精评与推送凭据(→设置) |
| Kestra blueprint「从蓝图创建流」(FlowCreate blueprintId 预填) | 「一键跑 demo」:yaml.template 取模板→id 段替换 myssia-demo→yaml.save 落盘→run.start→去日志屏链接(既有协议面的 UI 编排,零新后端功能);同名文件冲突走 mtime 锁结构化错误,如实呈现 |

## 不抄什么+为什么

- **KsEmptyState 120px 插画画作/learnMore 外链**:本地应用无营销插画资产;品牌 MyssiaMark+光晕(自有层)承担锚点,外链课程不适用。
- **产品导览 Tour(TourOverlay/tourScenes)**:超出纯 UI 重锚(R5),后续任务可议。
- **KsNoData(表内小空态)**:表格内筛选空结果仍走共享 EmptyState(表级语义)。

## 密度/规格实测

- 引导区 pt 64px;卡行高 67-68px(py-4);块间 gap-5;标签 text-xs;「需要指引?」→列表 mb-3。
- 交互闭环:demo 点击 → savedFile 含 myssia-demo.yaml、savedContent 含 `id: myssia-demo`、完成态 run #N+日志屏链接(测试在案)。
