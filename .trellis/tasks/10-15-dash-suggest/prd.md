# 仪表盘 8→9 三建议

## 背景

主人令「做 前端小改动,3个」= 此前解释过的云端视觉评审三建议(仪表盘 8→9)。

## 三项落地(408a7d48)

### ① 概览卡四指标均分整行,消右侧留白

- 旧:活跃源格 `min-w-[232px] flex-[1.3]` 偏置 + 其余三格 `min-w-[150px]`,行内比例不均。
- 新:四格统一 `min-w-[170px]` + 等基 `flex-1`(CompactStat 基类自带),整行满宽均分。

### ② 源健康度环图加 hover 图例(答「绿橙含义」)

- 环图格根挂 `group/donut`;图例常驻 DOM、`group-hover/donut:opacity-100` 显隐
  (feed 悬停操作条同款 CSS 家族:`bg-popover/95 shadow-popover` + fast/ease-out-expo)。
- 内容 = 四态色点(HEALTH_RING_FILL 同源)+ 标签(正常/退化/失效/未知)+ 计数,
  与环图同过滤(零段不入);`pointer-events-none` 防悬停自身闪烁;右侧弹出避开卡底裁切。

### ③ 顶部摘要条与概览卡数据去重

- 旧:verdict facts 拼「今日采集 N 条 / M/K 源在线 / 推送成功 N」——与概览四格同屏三数双报。
- 新:`buildVerdict` facts 撤三个数字段,只装过程性事实(doctorFailed 降级提示、
  running>0 的「N 个采集中」);摘要条回归纯状态句(tone 点 + headline)。

## 测试

- verdict 各态块(ok/dead/warning/unknown)改钉去重契约(aria 汇总句 = 主句、无数字段)。
- api 级「facts 随窗/缺数/零源」三块并为「窗解耦」单块(facts 恒无数字段)。
- D4 概览条测试扩:四格均分类名契约 + 图例四态计数 + hover 显隐类。

## 验收

- [x] vitest 933/933 + tsc 绿
- [x] 打包覆盖安装(提交后执行)
- [ ] 主人目验 hover 图例显隐手感

## 边界

- 「N 个采集中」保留在摘要条(runSummary.running 概览四格没有,不属重复)。
- 告警数在 headline「N 项告警」出现属状态语义本身,不去。
