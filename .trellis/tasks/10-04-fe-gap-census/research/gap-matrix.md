# 前端缺口矩阵(2026-10-04,主人目验判例驱动;证据=代码实核 rg + 真数据无头复现)

## 先回答主人的质问:「你有对比让你模仿的工具的界面吗?」

诚实答案:**研究级对比有,像素级目验没有**。三份拆解表来自官方文档/Geist 设计系统/截图视觉分析(带来源与「未实证」标注);但本会话模型无图像输入,装机七屏的像素核对要靠主人的眼睛——**你这次看仪表盘就是第一轮真对比**,抓出的问题(internal_error 裸放+整屏报废)已修(commit「仪表盘分区降级」)。后续每轮目验反馈都应回流到本矩阵。

## 事件定性:仪表盘 internal_error

**真数据根复现干净**:HEAD 构建 sidecar × 真数据根,13 RPC 全绿(36-85ms),仪表盘满血(evidence/dashboard-headless-repro-clean.png)。**错误出自并行会话的在途构建实例**(00:37/02:23 脏树产物,跑十小时)。但暴露的真缺陷已修:`loadDashboardData` 三方法任一失败整屏报废 → 改 `Promise.allSettled` 分区降级 + 人话错误码映射(internal_error→「核心内部错误…」)+ 全败才整屏卡。

## 一、对标交互缺口(teardown 可抄清单 vs 实装,代码级核)

| # | 缺口 | 对标出处 | 实况 | 量级 |
|---|---|---|---|---|
| 1 | feed **j/k 键盘导航**(条目间移动+focus 环) | teardown-linear-activity #9 | **未做**(仅 U 键切已读;rg key=j/k=0) | 小 |
| 2 | 侧栏**折叠**(`[` 快捷键/图标态) | teardown-linear-activity #1 | 未做(壳层批明示不做,无快捷键系统) | 中(需先立快捷键系统) |
| 3 | **全局命令面板**(⌘K 本体,现为留位) | Linear cmd+K | top-bar 只有占位 UI,无面板 | 中 |
| 4 | 仪表盘**卡片级时间范围**(Vercel 每卡右上 range) | teardown-vercel-dashboard #2 | 仅趋势卡有 Select;概览/源健康卡无 | 小 |
| 5 | feed **右键上下文菜单**(复制链接/沉淀/标已读) | teardown-linear-activity #7 | 未做(G12 沉淀走卡内按钮,右键无) | 小 |
| 6 | 条目**snooze/稍后读提醒** | Linear H 键 | 稍后读有(本地态),无到期重现 | 大(v2) |
| 7 | 设置**搜索设置项** | Linear settings(未实证) | 无 | 小 |
| 8 | 列表**Display options 下拉**(未读优先/分组维度切换) | teardown-linear-activity #3 | 分组固定按时间四桶,无切换 | 小 |
| 9 | 状态点 building 态 **pulse 呼吸** | teardown-vercel #6 微交互 | sparkline 末点有 pulse(部分落地) | 已基本落 |
| 10 | 骨架屏形状一致性 | Vercel skeleton | feed/dashboard 已做;sources/logs 有骨架待核 | 待核 |

## 二、功能池余量终态(census G 矩阵+后续新增)

| 项 | 状态 |
|---|---|
| G1-G5 前半/G7/G8/G12 | ✅ 全落(feed-ux+fe-small-batch+alert-rules) |
| **G9 服务端全库批量已读** | ❌ 现实现=已加载作用域;全库需 store/协议,架构级待立项 |
| G10 代理池连通性测试按钮 | ❌ v1.2(依赖 proxy_pool 后端) |
| G11 凭据导出 | 红线不做 |
| 远期形态:八爪鱼点选式建源/代理池管理面板/凭证猎手面板 | ❌ v1.2 池第 6 项 |
| v1.2 池其余:Windows/crawl4ai L3(刚转 review)/proxy_pool | 在途/池 |

## 三、质量债(在案小件)

- AlertsFiredEvent 未入 SidecarEvent 联合(logs 屏穷尽守卫适配)——alert-rules 遗留
- suppressed 状态词表 v2(告警 push 被同槽位拦截现记 send_failed)
- 消息屏告警面板真机手验(协议已落,差真调一轮)
- 装机包版本号 0.0.1(桌面 version 未随发布线对齐;1.1.2 线在途)
- 三处 P2 对比度旁核已在 fe-small-batch 闭;P3 消息标题跳级仍登记

## 处置路由

1/3/4/5/7/8 = 下一批「对标交互小批」候选(合计约一天量,可一档做完);2 需先立快捷键系统(单独立项);6 = v2;G9 架构级另 grill;其余按池走。
