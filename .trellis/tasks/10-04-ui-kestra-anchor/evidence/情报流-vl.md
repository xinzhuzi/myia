# 情报流屏 VL 毒评记录(10-04-ui-kestra-anchor)

- 评测对象:`evidence/情报流-kestra-after.png`(before 对照同目录;before = 改前
  现状截取,feed-screen.tsx 在 HEAD 干净,先截后改)
- 模型:qwen3-vl-8b-mlx(本地 8080;sips -Z 1100)
- 数据:真库只读(store.items 30 条真实条目,「今天」一组)。

## 第 1 轮(after)——结论:放行

VL 原文要点:
- 「高度贴近……紧凑卡片式列表、分组头 sticky、顶部动作区布局与 Kestra 暗色界面的
  工业级调度台风格一致」
- 「列表密度与节奏:优秀……紧凑但不拥挤;sticky 保持分组语义又不破坏滚动流畅」
- 「最扎眼的缺陷:无」;唯一弱项 = 搜索框提示文字略长(主观,前轮为清晰度刻意写,
  不属密度域,不动)。

VL 轮数:1(一轮即放行)。

## DOM 实测收口(像素主张真源)

| 主张 | 实测(feed-probe/sticky2-probe,1680×1050,30 条真库条目) |
|---|---|
| 满高列表内滚 | before:main scrollHeight 2283 > clientHeight 1002(页滚)→ after:1002=1002,列表容器 overflow-y-auto(scrollHeight 1948 / clientHeight 857) |
| 行密度 | 卡高 61→57px(py 10→8px);行距 8→6px(gap-2→gap-1.5);行 pitch 69→63px(≈9% 收紧) |
| sticky 组头贴顶 | 滚 400px 后 headerTop 193 == scrollerTop 193(stuck:true;修掉容器 pt-1 的 4px 露缝) |

测试:feed-screen.test.tsx 78/78 过(vitest run,本轮实测);tsc --noEmit 0 错。
