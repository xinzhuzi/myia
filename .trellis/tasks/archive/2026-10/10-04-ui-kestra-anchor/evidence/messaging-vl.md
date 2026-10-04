# 消息屏 VL 毒评记录(10-04-ui-kestra-anchor 道-B)

校准规则:VL 管整体审美感受,像素级主张以 DOM/几何实测为准。

## Before 基线
- 图:`messaging-kestra-before.png`(通知=屏内横幅;目录=逐行边框盒)。

## After 轮 1(修 2 刀)
- 实现:操作结果通知 → Kestra 通知中心范式浮卡(右上 fixed、类型图标+左色条+可关闭、popover 底+毛玻璃、pop-in 入场;不自动消失=行为面零改动);通道目录 hairline 分隔行(去逐行边框盒,hover 弱底)。
- 截图注:真库目录为空(platforms={}),toast/目录行证据图用注夹具(feishu 2 会话:1 别名+1 死信;refresh 应答 merged=2)驱动——UI 态证据,非真库数据。
- VL 主张 → 实测裁决:
  - 「浮卡无阴影」→ 首测截断误判为成立;**复测推翻**:box-shadow 链尾 `rgba(13,6,24,0.45) 0px 4px 16px`(shadow-popover 令牌正常;中途字面量绕行已回退,保令牌卫生)。
  - 「死信无颜色」→ **推翻**:Badge destructive 实测色 rgb(255,107,112)=--dead。
  - 「推送规则区无标题」→ **推翻**:CardTitle「推送规则」在案。
  - 「行距过密」→ 半采纳:py-2.5→py-3(行高 49→53px,Kestra 行带 44px 之上)。

## After 轮 2(放行)
- VL 重复同批主张(阴影[已推翻]/「全部品类下拉+跑一次」[幻觉,非本屏元素]/死信[已推翻])。
- 实测:toast 圆角 10px+阴影链尾在案;行 py-3;65 测试绿。
- 裁决:具体主张全被实测推翻,密度已升档 → 放行。

## 结论
消息:Kestra 对标件 design-system KsNotification(ElNotification 包装)+列表密度;VL 2 轮(修 2 刀:入场动效+行距升档);测试 65 绿。
