# 仪表盘运行区 VL 毒评记录(10-04-ui-kestra-anchor)

- 评测对象:`evidence/仪表盘运行区-kestra-after.png`(before 对照同目录;before 系
  HEAD 版临时换回截取后恢复,见 mapping.md 流程注记)
- 模型:qwen3-vl-8b-mlx(本地 8080;sips -Z 1100)
- 数据:真库只读(doctor/runs.list/store.trend);近期 run 区 1 行 = 真库真实历史
  (注册表夹具跑在临时 db,mergeDashboardRuns 按口径不并入,如实)。

## 第 1 轮(after)——结论:放行

VL 原文要点:
- 「与 Kestra 暗色调度台的贴近度极高……信息密度与视觉节奏高度一致」
- 「近期 run 成功率运行区质感优秀:状态芯片颜色精准……表格行对齐工整,无错位;
  『全部 run』链接可点暗示明确」
- 唯一 nit:「推送成功/告警卡右上『1』字体大小与其他文字不一致」。

nit 核验(校准规则:像素主张以 DOM 实测为准)——**不采信**:stat-font-probe 实测
四张概览卡数值 fontSize 20px / weight 600 / tabular-nums 完全一致(text-2xl 令牌
为基调层 20px 档,四卡同 className)。VL 与实测冲突,实测为准。

VL 轮数:1(一轮即放行)。

## DOM 实测收口(像素主张真源)

| 主张 | 实测(dash-run-probe/stat-font-probe,1680×1050) |
|---|---|
| run 行槽位对齐 | #id(w-8)· 条数(w-11 right=705)· 相对时间(w-[68px] right=785)· 耗时(w-14 right=853)|
| 状态芯片 | h=24px(Kestra KsExecutionStatus small 同档) |
| 出口链接 | a[href="#/logs"] ×2(「全部 run →」+ 活跃行「日志 →」;HashRouter 下 a#hash 等价 Link,免 Router 上下文)|
| 概览四卡数值字体 | 20px/600/tabular-nums 四卡一致 |

测试:dashboard-screen.test.tsx 36/36 过(vitest run,本轮实测);tsc --noEmit 0 错。
