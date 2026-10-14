# 情报流三级界面美化(条目详情视图)

## 背景

主人令(10-14 晚):「界面问题要再进行优化,美观一下,情报流里面的三级界面,一定要好看,使用相关skill进行处理美化」。

## 方法

frontend-design + apple-design 双技能过流程:无头冒烟基线截图(feed-card-smoke.py,装机同源 ui 构建)→ 本机 VL(qwen3-vl-8b)设计评审定病灶 → 仓内 token 体系内克制修整 → 复跑冒烟 + VL 终审。

## VL 病灶(基线)与修整(全部类名级,零结构改动)

| 病灶 | 修整 |
|---|---|
| 标题被状态与动作钮挤压 | 标题 text-base→text-lg + tracking-tight(身份锚);头区 gap-x-3→4 / gap-y-1→1.5;console gap-x-2→3 |
| 状态点「●」字形发虚 | 文字圆点换真色点 span(size-1.5 rounded-full bg-ok);词面断言 toContain 不受影响 |
| 消息间距过小 | 时间线容器 gap-3→4 / px-5→6 / py-3→4;组内列表 mt-1→2 |
| 日期分隔弱 | 胶囊加细描边 border-border/50 + 降底色 bg-muted/30 + tracking-wide |
| 气泡局促 | 泡内边距 px-3 py-1.5→px-3.5 py-2;发信人行 mb-0.5→1 |
| 未读分界存在感不足 | 居中化:线-字-品牌青点-线;词面 未读→以上未读 |
| 界面缺少生命感 | 时间线进场 animate-fade-in(key 随渠道切重放;reduced-motion 全局归零) |

## 红线遵守

顶栏等高契约(py-2.5+min-h-11,测试钉死)padding 不动,呼吸感走 gap;token 工具类之外零新增;阴影/渐变/大圆角零触碰。

## 验收

- [x] AC1 冒烟基线+终版截图与 VL 评审留档(evidence-l3-after.png;终审成品感 8.5/10,层次/节奏/胶囊全过)。
- [x] AC2 feed 屏 219/219 + 全量 vitest 942/942 + tsc 过(既有断言零改动——仅一处 ● 圆点字形不进 textContent,断言 toContain 不涉)。
- [x] AC3 重打包换装(哈希资源面)+ 实例重启(21:02)+ 装机同源冒烟复跑全过。
