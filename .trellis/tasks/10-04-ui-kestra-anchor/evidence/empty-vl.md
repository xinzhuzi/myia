# 空态引导态 VL 毒评记录(10-04-ui-kestra-anchor 道-B)

校准规则:VL 管整体审美感受,像素级主张以 DOM/几何实测为准。

## Before 基线
- 图:`empty-kestra-before.png`(--empty 伪造 health.first_run):旧空态=居中品牌标+死文案,无动作无引导。

## After 轮 1(修 1 刀)
- 实现:FirstRunGuide(Kestra KsEmptyState 左对齐结构:artwork+标题+描述+动作行;NoExecutions/OverviewBottom:「需要指引?」标签+边框堆叠指引卡[图标+标题+描述+chevron]×3)+「一键跑 demo」(yaml.template→yaml.save myssia-demo.yaml→run.start→去日志屏链接)。
- VL 主张 → 裁决:
  - 「无品牌图标」→ **推翻**(首测探针抓到的是按钮内 Rocket svg;MyssiaMark 是 img[48px],复测确认在案)。
  - 「按钮与说明间距过近/卡间留白不足/需要指引?字号不配」→ **采纳**(对齐 Kestra 实测值修:块间 gap-4→gap-5[KsEmptyState gap 21px]、区呼吸 py-10→py-16[其 padding 3rem]、卡行 py-3.5→py-4、标签 text-2xs→text-xs[其 --ks-font-size-sm])。

## After 轮 2(放行)
- VL 主张 → 实测裁决:
  - 「无品牌图标」→ **再推翻**(img 在案,幻觉)。
  - 「卡片边框粗细不一」→ **推翻**:三卡同 border-border 1px,高 67/68/68 均匀。
  - 「排程一瞥与引导卡混在一起」→ **推翻**:排程区是独立 Card(gap-block 分区+卡边框);且「空品类目录→排程空态文案」有测试锚定(sources.test.tsx),保留为既有功能面。
- 一键 demo 行为闭环加交互测试(桩协议:yaml.template/yaml.save/run.start 对账+完成态链接),18 绿。

## 结论
空态引导态:Kestra 对标件 KsEmptyState.vue+NoExecutions.vue+OverviewBottom.vue/OverviewCard.vue;VL 2 轮(修 1 刀=Kestra 实测间距档);R4 首跑引导+一键 demo 落地(既有协议面编排,零新后端功能)。
