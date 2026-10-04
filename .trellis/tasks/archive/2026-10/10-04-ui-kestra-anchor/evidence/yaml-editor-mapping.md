# 配置编辑屏 ↔ Kestra 源文件对照(10-04-ui-kestra-anchor 道-B)

对标件(只读参考,Apache-2.0,借结构改语义):
- `kestra/ui/src/components/flows/FlowCreate.vue`(full-container 编辑器分区)
- `kestra/ui/src/components/flows/MultiPanelFlowEditorView.vue`(编辑器顶栏动作位)
- `kestra/ui/packages/design-system/src/components/Form/KsEditor`(编辑面令牌用法:底=暗于卡面的 input 档)

## 借了什么(结构→语义)

| Kestra 结构 | 我们的落点 |
|---|---|
| `section.full-container flush-top`:编辑器满高,无卡嵌套 | 双 Card 嵌套拆除:左文件栏=平铺侧板(`border-r border-border` 细线分层,右缘呼吸 pr-3);右编辑区满高 |
| 编辑器顶栏:标题+动作(execute/validate/save) | 工具条 h-11 border-b:左=文件名+dirty `*`+未保存草稿徽标+路径(mono 弱色);右=跑一次(outline)/校验(secondary)/保存(primary)/⌘S kbd |
| Monaco 满高编辑面 | CodeMirror 满高;铬色(底/行号槽/激活行/选区/光标)改走本仓令牌(KESTRA_CHROME 主题,叠在 oneDark 上只留语法配色) |
| 底部校验错误面板 | findings 抽屉:border-t,max-h-44 滚动,校验/保存/doctor/跑一次结果同舱 |
| FlowCreate setupError 结构化错误态 | ErrorBox(list.error/actionError)+重试(原有) |

## 不抄什么+为什么

- **Topology/Source 双面板切换(MultiPanelTabs)**:CodeMirror 原文即本屏全部语义;拓扑视图=品类解析图谱,协议面无对应,不做假图。
- **Monaco**:vite 体积约束+CodeMirror 已在案(任务决议 5),换内核超出 UI 重锚。
- **蓝图(blueprint)导入**:无对应协议。
- **多标签页(MultiPanelEditorTabs)**:编辑内核按单文件受控(dirty 守卫语义),多标签=新功能面。

## 密度/规格实测

- 工具条 44px(h-11)border-b;文件栏 256px(w-64)border-r;编辑面底 var(--background) #14181f(--ks-bg-input 同族);行号槽右缘 border(--ks-border-default 同值)。
