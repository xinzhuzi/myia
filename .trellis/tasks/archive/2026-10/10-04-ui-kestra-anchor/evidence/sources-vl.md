# 源管理屏 VL 毒评记录(10-04-ui-kestra-anchor 道-B)

校准规则:VL 管整体审美感受,像素级主张以 DOM/几何实测为准(8B VL 幻觉在案,实测推翻即不采信)。

## Before 基线(1 轮)
- 图:`sources-kestra-before.png`;提示词:对标 Kestra Flows 的 8 问毒评。
- 要点:整体「业余拼凑感」;密度过高;控件质感粗;与 Kestra 差距=无紫主色/无细边框分层/状态可视化弱。

## After 轮 1(修 1 刀)
- 实现:顶栏统计 dot + 主操作「新建品类」(紫 primary,NavBarAction primary 范式);表格出卡、满铺(KSFilter 式工具栏:搜索+分段筛选+刷新图标钮);行点击开编辑(NON_NAVIGATING_TARGETS 守卫);动作列图标钮(KsIconButton 28px)。
- VL 主张 → 实测裁决:
  - 「分段筛选无高亮」→ **推翻**:activeBg 实测 rgb(47,51,66)=#2f3342(--ks-bg-active 同款),含 shadow-sm+font-medium。
  - 「URL 截断无省略号」→ **推翻**:cell 类含 `truncate`,实测 overflow=false。
  - 「行无 hover」→ **推翻**:行类含 `hover:bg-accent/40`(44px 行高,cursor=pointer)。
  - 「全部品类下拉/跑一次位置错乱」→ **幻觉**:本屏无此二元素(截图内亦无)。
  - 整体「不像成品」→ 采纳一半:裸铺表格与下方卡片区混排显散。
- 修刀:表格区入 hairline 容器(rounded-lg border)+表头浅底带(bg-muted/30)。

## After 轮 2(放行)
- VL 重复同批幻觉锚点(「全部品类下拉」「跑一次」仍非本屏元素;「健康度无颜色区分」被推翻——HealthBadge/SummaryDot 四色圆点在案:ok #43f6b6/warning #ff8b61/dead #ff6a6c/unknown #9797a6)。
- 实测复核:图标钮 28×28 双钮 y 对齐(247px 同行);分段 188×34;表头 36px;行 44px。
- 裁决:VL 全部具体像素主张被实测推翻,整体否定建立在幻觉锚点上 → 按校准口径放行(实测为准,VL 整体否决不成立,记录在案)。

## 结论
源管理:Kestra 对标件 Flows.vue+KsDataTable/KsFilter/KsIconButton;VL 2 轮;实测+测试(17 绿)双收口。
