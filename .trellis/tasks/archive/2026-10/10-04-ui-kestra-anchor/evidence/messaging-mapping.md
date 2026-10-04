# 消息屏 ↔ Kestra 源文件对照(10-04-ui-kestra-anchor 道-B)

对标件(只读参考,Apache-2.0,借结构改语义):
- `kestra/ui/packages/design-system/src/components/Feedback/KsNotification.ts`(通知中心范式)
- 其底座 Element Plus ElNotification(右上浮卡+类型图标+可关闭)
- Kestra 列表密度(KsDataTable 行分隔/hover 族)

## 借了什么(结构→语义)

| Kestra 结构 | 我们的落点 |
|---|---|
| KsNotification:右上角浮卡、类型图标(success/error/warning/info 各图标)、customClass 类型色、可关闭 | 操作结果通知(别名/刷新/保存/删除回执)=右上 fixed 浮卡:类型图标(CheckCircle2/AlertCircle)+左色条 2px(ok/destructive)+关闭钮(aria-label 关闭通知);popover 底+毛玻璃+shadow-popover+pop-in 入场 |
| ElNotification 停留行为(auto-close) | **不抄自动消失**:我们的通知是结果性回执(保存成功/失败原因),静默消失=掩盖;由用户关或下一次操作替换(行为面零改动,记档) |
| KsDataTable 行 hairline 分隔+hover | 通道目录逐行边框盒 → divide-y hairline 行(py-3,hover bg-accent/25) |
| KsTag/徽标族 | 目录行内 type/别名/死信徽标维持共享 Badge 基件(死信=destructive 红) |

## 不抄什么+为什么

- **ElNotification 全局 toast 挂载/队列**:我们单通知位(一次操作一条回执,新替旧)足够,不引全局队列状态。
- **Kestra EE 告警中心(Alerting)**:告警规则面板是本仓自有域(10-04-alert-rules 刚落),保持既有结构。
- **平台总览重排**:platform-overview 为近期产物且不属通知范式核心映射,本轮只动通知与目录行(范围克制,记档)。

## 密度/规格实测

- toast:圆角 10px、阴影链尾 `0 4px 16px rgb(13 6 24/.45)`、左条 2px --ok/--destructive、宽 w-84(336px);目录行高 53px(py-3)。
