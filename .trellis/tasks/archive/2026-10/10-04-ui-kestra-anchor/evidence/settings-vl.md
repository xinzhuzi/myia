# 设置屏 VL 毒评记录(10-04-ui-kestra-anchor 道-B)

校准规则:VL 管整体审美感受,像素级主张以 DOM/几何实测为准。

## Before 基线
- 图:`settings-kestra-before.png`(左分区导航+卡内 FieldInput 纵排[标签上/输入下])。

## After 轮 1(修 2 刀)
- 实现:内容列 600px 居中(Kestra Wrapper 范式);FieldInput 重构为 SettingRow 横排(label+hint 左/控件右 w-64);LLM/代理/推送/看图卡行间 divide-y;推送通道与看图双 Select 同范式;enrich 行暂留嵌套盒。
- VL 主张 → 实测裁决:
  - 「LLM API Key 无占位符」→ **推翻**:实测 placeholder="输入后才写入;保存即清,永不回显"。
  - 「enrich.model 行控件对齐跑偏」→ **成立**:实测 enrich 模型输入右缘 1031 ≠ 主行 1155(嵌套盒 p-4+尾随钮内缩)。
  - 「pools 行间距/换行异常」→ **成立**:探测行 rowH=68(action 钮换行)。
- 修刀:①enrich 扁平化(去嵌套盒,开关行+model 行进 divide-y,保存钮入 FieldInput action 位);②FieldInput 控件改填充制(flex-1 填 w-64 容器,action 同行不换行)。

## After 轮 2(放行)
- 实测:主行输入右缘全对齐 1155;enrich 行=输入 1048+保存钮收尾 1155(控件组同轨,Kestra 控件+尾随钮同构);pools 行=输入 1103+探测钮 1155(同构,不再换行);内容列宽 600。
- VL 主张 → 实测裁决:
  - 「评分与反馈卡内行间无分隔线」→ **推翻**:enrich 组外层 divide-y divide-border/60 在案。
  - 「base_url/model/LLM Key 标签与控件错位」→ **推翻**:三行输入右缘同为 1155,行高 32。
  - 「保存 LLM 兜底按钮未对齐」→ **幻觉**:无此钮名;卡底保存条(CardSaveBar border-t)右对齐为 Kestra 卡级保存位。
- 裁决:两轮具体主张或被实测推翻或已修,控件轨一致 → 放行。

## 结论
设置:Kestra 对标件 BasicSettings.vue+Wrapper/Block/SettingRow;VL 2 轮(修 2 刀);测试 60 绿;vision/push 分区补证据图(同范式无单独 VL)。
