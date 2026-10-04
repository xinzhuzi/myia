# 源管理屏 ↔ Kestra 源文件对照(10-04-ui-kestra-anchor 道-B)

对标件(只读参考,Apache-2.0,借结构改语义):
- `kestra/ui/src/components/flows/Flows.vue`
- `kestra/ui/packages/design-system/src/components/Data/KsDataTable/KsDataTable.vue`(密度/满高分區)
- `kestra/ui/packages/design-system/src/components/Data/KsDataTable/KsFilter.vue`(工具栏)
- `kestra/ui/packages/design-system/src/components/Data/KsTable/KsTable.vue`(cell 密度)

## 借了什么(结构→语义)

| Kestra 结构 | 我们的落点 |
|---|---|
| TopNavBar actions:icon 动作 + `NavBarAction type="primary"`(Plus,新建流) | PageHeader actions:健康统计 dots(我域数据)+「新建品类」紫 primary 钮(锚 `#/yaml-editor` 既有深链,零新功能) |
| `section.full-container`:KsDataTable 满高铺底,无卡包裹 | 表格区出 Card,直接铺内容底;外缘 hairline 容器(rounded-lg border)收边——Kestra 单列表页无后续区块,本页下方还有排程/停用卡,加 hairline 保持圆角分层同族(偏离在案) |
| `#top` 槽 = KSFilter(搜索 + 表格选项 + refresh 回调) | 工具栏:前置放大镜搜索框 + 健康度分段筛选(rounded-lg 容器+active bg-accent)+ 刷新图标钮(原地转圈,有数据不卸表格) |
| 行点击 → router.push 流详情;`NON_NAVIGATING_TARGETS` 守卫 | 行点击 → 弹出 YAML 编辑对话框;同款守卫(button/a/input/[role=switch]/拖拽手柄不冒泡) |
| 动作列 `KsIconButton`(Play 图标钮 + tooltip) | 动作列图标钮:FlaskConical=试抓、Pencil=编辑(aria-label/title 承载语义,28px ghost) |
| 列:id+draft 徽标+labels+namespace+最近执行状态+统计图+triggers | 列:源名称/品类(名+文件名+加载失败徽标)/URL/引擎/健康度(四色 chip)/最近产出/启停/操作(域映射,功能面零改动) |

## 不抄什么+为什么

- **执行统计迷你时序图(TimeSeries/row)**:health 协议无逐 run 历史面(只有 latest+observed 计数),造图=伪造数据密度。
- **列显隐配置(useTableColumns/storageKey)**:本表列集固定 8 列,显隐配置徒增状态;Kestra 列多(7+扩展列)才需要。
- **批量勾选+bulk-actions(导出/删除/启停)**:sources.write 协议按单源 enable/disable 数组——批量启停其实协议可表达,但 v1 无批量确认语义,不新增功能面(R5)。
- **CSV 导出/zip 导入**:协议无对应方法。
- **draft 行样式类(disabled/dim)**:我们无 flow disabled 概念(启停走开关列如实呈现)。

## 密度/规格实测对照

- 行高 44px(Kestra el-table ≈41px 同带);表头 36px;动作图标钮 28px;分段控件 34px 高(active #2f3342 = --ks-bg-active 同值);行 hover bg-accent/40。
- 新建钮紫底 #631bf3(--ks-btn-primary-bg-default 同值)。
