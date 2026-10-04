# 设置屏 ↔ Kestra 源文件对照(10-04-ui-kestra-anchor 道-B)

对标件(只读参考,Apache-2.0,借结构改语义):
- `kestra/ui/src/components/settings/BasicSettings.vue`
- `kestra/ui/src/components/settings/components/Wrapper.vue`
- `kestra/ui/src/components/settings/components/block/Block.vue`
- `kestra/ui/src/components/settings/components/block/SettingRow.vue`

## 借了什么(结构→语义)

| Kestra 结构 | 我们的落点 |
|---|---|
| Wrapper:`width: min(600px, 100%-48px)` 居中单列 | 内容列 `max-w-[600px]`(600px 整,实测 contentWidth=600) |
| Block:h2 标题 + KsCard 零内边距 + 行 | 卡(CardHeader 标题/描述)+ CardContent 行组 |
| SettingRow:label(600 字重)+description(small 次级)左 / control(flex-shrink 0 右对齐)右,行 padding 16px,行间 border-bottom | 新建 `settings-row.tsx`:label(text-sm semibold)+hint(text-2xs)左 / 控件位 w-64 右,py-3,父容器 divide-y;FieldInput/vision 双 Select/推送通道全部收编此范式 |
| SettingRow stacked 变体 | 窄屏 sm: 断点纵叠(flex-col gap-2) |
| KsSelect/KsInput 控件 32px | 共享 Input/SelectTrigger(--control-h 32px 档,基调层已有) |
| 每块多行 + 个别 stacked 复合行(flow_template) | pools 探测行/enrich model 行 = 控件+尾随动作钮同轨(输入 flex-1+action 并排) |

## 不抄什么+为什么

- **单页无分区导航(Kestra settings 是一页 BasicSettings)**:我们的五分区(通用/视觉/推送/更新/高级)+ ?section= 深链是既有功能面(census #7 过滤框也在),R5 零改动保留左导航;Kestra 无对应结构,导航样式维持本仓侧栏族。
- **默认命名空间/日志级别/编辑器类型等设置项**:我域无此配置面;我们的行=LLM/代理/推送/看图凭据与结构(域映射)。
- **KsEditor flow_template 行**:YAML 模板编辑已有专用配置编辑屏,不在设置重复。
- **语言/主题切换**:本仓暗色单主题(index.css 在案)。

## 密度/规格实测

- 内容列 600px;行 py-3(上下≈12px+行高 32;Kestra 16px 上下,因我们 hint 长文两行,取半档防胖);控件右轨 1155(同卡全行一致);行间 divide-border/60。
