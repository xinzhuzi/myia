# 情报流 1 级类型卡墙高度宽度取齐

## 背景

主人 10-15 截图报障「高度宽度要一致」:情报流 1 级类型卡墙(TG/微信/网站/日报…)
各卡尺寸不一致。

## 根因

- 卡墙容器 `feed-screen.tsx` 用 `columns-[260px] gap-4` = CSS 多列**瀑布流**:
  卡高度纯内容驱动,只有 `min-h-[340px]` 地板;预览条目多的卡长出,列底参差。
- TypeCard 根上挂着列布局遗物 `mb-4` / `break-inside-avoid`。
- 像素实测(主人截图):四卡宽度本已相等(4×524px,列距 36)——不一致面在高度。

## 修复(d3547600)

1. 容器:`columns-[260px]` → `grid gap-4 [grid-template-columns:repeat(auto-fill,minmax(260px,1fr))] [grid-auto-rows:1fr]`
   —— 等宽列 + 全墙行高取齐(1fr 行取最长行),任意窗口宽下全卡同尺寸。
2. TypeCard:去 `mb-4`/`break-inside-avoid`,加 `h-full` 满格;`min-h-[340px]` 竖版锚保留。
3. 契约测试:feed-screen.test.tsx 钉死 grid 形态 + 卡 `h-full` + 瀑布流遗物不得回流。
4. 无头烟测升级**像素级实测**:全部 `feed-type-card-*` bounding box 宽高逐一相等。

## 验收

- [x] vitest 934/934(含新契约)
- [x] tsc --noEmit 绿
- [x] feed-card-smoke 全过:boxes=[(325,340)×3] 全等
- [x] 打包覆盖安装(本档提交后执行)

## 边界

- 2 级 group 目录墙(`feed-screen.tsx` 另一处 columns,带 sticky 组头)不动:
  主人报障面是类型卡墙;组头墙瀑布语义另有注释约定(break-inside-avoid 与 sticky 互斥)。
