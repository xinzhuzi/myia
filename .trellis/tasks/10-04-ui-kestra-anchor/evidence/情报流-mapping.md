# 情报流屏 ↔ Kestra 源码对照(10-04-ui-kestra-anchor)

改动文件(白名单内):`desktop/ui-src/src/screens/feed/feed-screen.tsx`(单文件;
api.ts/反馈子件/测试未触碰)。

## 对标件(只读参考,Apache-2.0;借结构改语义)

| Kestra 源件 | 借了什么 | MYIA 落法 |
|---|---|---|
| `executions/Executions.vue` + `ui/src/styles/app.scss` `section.full-container` | 列表密度骨架:满高列表内滚、过滤条常驻列表之外、表体自带滚动 | 屏根 `h-full min-h-0 flex-col`;列表区(导出回执/横幅/空态/分组列表)统一进 `flex-1 overflow-y-auto` 内滚容器 |
| KsDataTable 行密度(14px 基字、紧凑行距、border 分行) | 行距/内边距收紧档 | 卡 py-2.5→py-2(10→8px)、组内/平铺行距 gap-2→gap-1.5(8→6px);pitch 69→63px(实测)。13px 标题/11px 元信息三级密度(前轮 teardown 血统)保留——两档密度语言不冲突 |
| KsDataTable sticky navbar(KSFilter 在表体滚动时常驻) | 列表滚动时分组语义常驻 | sticky 组头贴内滚容器顶(修前容器 pt-1 会露 4px 缝,已除;实测 stuck:true) |

## 不抄 + 为什么

- **整表化(单卡容器 + border 分行 + 列头)**:情报流卡是富交互行(hover 浮现操作簇/
  左缘未读条/品类色条/右键菜单/行内 AI 摘要面板),Kestra 表行是纯展示行;表化会拆掉
  这些已验收的行级交互(G9/A-feed 在案),且卡片列语义(标题+元信息双行)与表格列头
  不同构。保留卡列表,只借密度与满高骨架。
- **KsDataTable 复选/批量/分页**:读流无批量域;「加载更早」按钮即增量分页(R1 在案)。
- **KSFilter 列配置/图表开关**:无列概念;显示选项(未读优先/分组维度)已由 A-feed
  下拉承担,同位不同形。

## 兼容性核验

- feed-screen.test.tsx 78/78(vitest run 实测);tsc --noEmit 0 错。
- 测试锁定的类面全保留:feed-item hover:bg-accent/50、strip bg-primary/opacity-70、
  actions opacity-0/group-hover、time text-2xs、组头 sticky。
