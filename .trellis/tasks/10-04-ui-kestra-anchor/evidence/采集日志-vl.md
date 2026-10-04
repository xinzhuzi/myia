# 采集日志屏 VL 毒评记录(10-04-ui-kestra-anchor)

- 评测对象:`evidence/采集日志-kestra-after.png`(before 对照 `采集日志-kestra-before.png`)
- 模型:qwen3-vl-8b-mlx(本地 8080;sips -Z 1100 缩图)
- 夹具:桥 39941(世事.app sidecar),run.start 串行造 3 run 于临时 db /tmp/myia-kestra-smoke.db
  (真库只读):#3 config_error(/tmp/myia-broken.yaml)· #2 wool dry success · #1 myia-demo 真跑 success。
  展开态:#3(自动跟随)+ #1(手动展开,INFO 结构化行)。

## 第 1 轮(after)——结论:放行

VL 原文要点:
- 「非常贴近……满高列表、等宽日志终端、状态芯片、列对齐、暗色主题,完全复刻 Kestra Executions 的核心视觉语言」
- 放行理由成立:整体合格,仅细节瑕疵不影响核心体验。

三项 nit 的核验(校准规则:像素主张以 DOM 实测为准):
1. 「错误项红色对比度不足」——**不采信**:代码在案实算(WCAG 注释,logs-screen.tsx
   LogRowView)bg-dead/10 叠底 ≈ 4.67:1 达 AA;原 /15 档 4.43 不达才降档。VL 与实测冲突,实测为准。
2. 「复制日志按钮与『配置』(齿轮)按钮图标不一致」——**幻觉**:本屏无齿轮按钮
   (DOM 探针:meta 条右侧仅 复制日志/徽标;组头行尾是重跑 RotateCcw icon 钮)。不采信。
3. 「错误区拥挤/标题与列表缺分隔」——主观弱项;组头与日志体之间有 border-t + 摘要条
   分隔(探针 metaText =「总耗时220ms/7 行/1 错误行/logs.tail run_id=3 复制日志」),不再加线。

VL 轮数:1(一轮即放行)。

## DOM 实测收口(像素主张真源)

| 主张 | 实测(kestra-probe/chip-probe,1680×1050) |
|---|---|
| 满高列表内滚 | waterfall rect y=247→1050(height 803,overflow auto);before 为 height 382.5/overflow visible,页滚 |
| 列对齐 | 时间槽右缘 1339 ×3 行一致;耗时槽 1407 ×3;错误槽 1203 ×3(修 itemCount 槽常渲染后) |
| 状态芯片 = Kestra small 档 | 60×24px、radius 6px、font 12px、状态色 15% 底(Kestra KsExecutionStatus small:1.5rem/12px/radius-sm) |
| 相对开始时间 | 三组头均含「N 分钟前」(KsDateAgo inverted 同义) |
| 组头高 | 44px(before 同,行密度不变) |
| 终端 | 12px mono,max-h-26rem(不变) |

测试:logs-screen.test.tsx 15/15 过(vitest run,本轮实测);tsc --noEmit 0 错。
