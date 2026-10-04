# 配置编辑屏 VL 毒评记录(10-04-ui-kestra-anchor 道-B)

校准规则:VL 管整体审美感受,像素级主张以 DOM/几何实测为准。

## Before 基线
- 图:`yaml-editor-kestra-before.png`(未选文件 idle 态,卡嵌套双栏)。

## After 轮 1(修 1 刀)
- 实现:IDE 满高框架(FlowCreate full-container 范式)——左文件栏平铺侧板(border-r 细线分层,无卡包裹),右编辑区=工具条(文件名/dirty/路径+跑一次/校验/保存/⌘S)+满高 CodeMirror+底部 findings 抽屉(border-t)。
- 首评在 idle 态(未选文件)不公平 → 深链 ?file= 重截后评。
- VL 可立主张:「编辑面底色与全屏令牌族割裂」→ **实测成立**:CodeMirror oneDark 底 #282c34,非本仓 --background #14181f 族。
- 修刀:editor-pane.tsx 加 KESTRA_CHROME 主题(底/行号槽/激活行/选区/光标全走 --background/--border/--accent/--primary/--link 令牌;oneDark 只留语法配色)。

## After 轮 2(放行)
- VL 主张 → 实测裁决:
  - 「无行号/无语法高亮/无折叠标记」→ **幻觉**:basicSetup lineNumbers+foldGutter+yaml() 扩展在案,截图中代码高亮可见。
  - 「文件栏未用 border-r 分隔」→ **推翻**:aside 类含 `border-r border-border`(#2c303f,Kestra --ks-border-default 同值)。
  - 「findings 与编辑区无分隔」→ **推翻**:findings 容器含 `border-t border-border`。(「无折叠交互」是功能请求,超出纯 UI 重锚范围,不采。)
  - 「工具条与文件栏质感不一」→ 泛主观,两侧控件全走共享 Button/Input 基件,无实测支撑。
- 裁决:VL 核心主张全被实测推翻,唯一真点(编辑面底色)已修 → 放行。

## 结论
配置编辑:Kestra 对标件 FlowCreate.vue+MultiPanelFlowEditorView(顶栏动作位)+design-system KsEditor 令牌用法;VL 2 轮(深链编辑态);测试 27 绿。
