# 前端缺口三层矩阵(2026-10-04 普查落档)

> 普查员:只读核验,未动 desktop/ 与 src/ 任何文件。证据口径:逐条对 `desktop/ui-src/src` 工作树实读(rg/Read),对比度为独立 WCAG 实算(Python 脚本,方法与 fe-small-batch 记录值 4.15/3.41 对齐吻合)。对标底稿 = `archive/2026-10/10-03-ui-deep-imitation/research/` 三份 teardown 表(本会话全文实读)。
>
> **在途声明**:10-04-interaction-batch 六件(⌘K 面板/右键菜单/快捷键底座/侧栏折叠/仪表盘时间范围/feed j-k)已在工作树见产物(未提交,git status 大量 M/R),**全部标「在途,勿重复立项」**,本矩阵只记实况不路由。

## 路由执行记录 2026-10-04(主人令全部做完)

> 执行态勾注(文档批回写):普查落档同日,主人令 §处置路由汇总全部做完;逐条执行态如下。

- **直接小修 4 条(R1/R2/R3/R4)→ 由本工作流冲突面批执行**:R1 feed Cmd+F 聚焦搜索框(+Esc 即时清空+搜索框 focus ring)/ R2 AlertsFiredEvent 入 SidecarEvent 联合+logs 穷尽守卫适配 / R3 tauri.conf.json 版本号对齐发布线(归收官流)/ R4 池 prd 回标(档内——已由文档批即席执行,回执 `10-03-v12-backlog/prd.md` Requirements 第 5 项,四条已消号标注 2026-10-04 落)。
- **G9(R5)→ 已立档,后分两流(2026-10-04 复审修整注)**:全库批量已读 store/协议本体已由 `10-04-read-state-server` 交付(status=review,commit afa7339:`store.state.mark_all` 全库语义三端+UI 能力门+全库按钮真话);余量档=`.trellis/tasks/10-04-g9-read-all/`(planning,仅按品类批量入口+全库确认交互增量,其 prd「依赖核实结论」节立档时已钉死不重复造)——两档非双档悬空。
- **入池 2 条(R6/R7)→ 已入池**:R6 G10 代理池连通性测试按钮(后端 `10-04-proxy-pool` 已归档=依赖解锁)+ R7 七件小件(侧栏分组折叠/源管理多选点簇筛选/设置 tooltip/snooze 到期重现/设置搜索/suppressed 词表 v2/P3 消息标题跳级)——增补回执 `10-03-v12-backlog/prd.md` Requirements 第 5 项 G10 行(依赖解锁)+ 第 8 项(新增块);池纪律不挂 in_progress。
- **关闭 3 条 → 维持关闭,不再立项**:R8(语义不匹配/过度 4 项:feed 条目删除/设置 homepage/渠道 Tab/凭据表格化)、R9(在途 6 件归 interaction-batch+对标已实装 24 项)、§3.2 真机手验(已归 `10-04-wrapup-checklist` 档)。
- **R9 定稿注记(2026-10-04 复审修整)**:gap-matrix 处置路由原文六件=缺口 **#1/#3/#4/#5/#7/#8**(`research/gap-matrix.md:47`);interaction-batch 实际交付 **#1/#2/#3/#4/#5/#8**(其 prd.md:23 分诊口径)。差一件:**#7 设置搜索设置项未随批做,仍悬置留池**(rg 核 `settings-screen.tsx` 仅 useSearchParams 路由参数,无设置搜索功能);#2 侧栏折叠以 A-shell 最小快捷键底座并入本批替补(原路由「单独立项」未走)。定稿按此口径,勿把 #7 记为已做。
- **R9 注记补正(同日 FixStage,主人令「将所有问题都做完」)**:#7 已于复审修整阶段补做——设置屏分区导航上方加过滤输入,实时过滤分区名(label/id 不分大小写,纯前端零 RPC,Linear settings 口径;`settings-screen.tsx` 分区过滤节 + `settings.test.tsx`「分区过滤」describe 4 用例 scoped vitest 全绿)。定稿口径以本段为准:**#7 = 复审修整阶段补做,非悬置**;上段「勿把 #7 记为已做」作废(该 rg 证据在补做前成立)。

## 一、对标交互缺口逐条核(teardown 可抄清单 vs 实装)

### 1.1 linear-activity(情报流与壳层,可抄清单 14 条)

| # | 可抄项 | 状态 | 证据(file:line) | 路由建议 |
|---|---|---|---|---|
| 1 | 侧栏「倒 L」分组+底部状态区;`[` 折叠;激活=accent 行背景 | **已实装**(折叠键=在途件) | `components/layout/sidebar.tsx:32-55`(NAV_GROUPS 三区)、`:204-233`(分组渲染+底部设置/状态/折叠钮)、`:139`(isActive→`bg-accent text-foreground`) | 关闭(已做) |
| 2 | 分组可折叠(ChevronDown 旋转 ~150ms) | **未做** | `rg ChevronDown sidebar.tsx` 零命中;分组固定展开(rg 实跑 exit=1) | 入 v12-backlog 池 |
| 3 | 列表头部:左 Tabs+右 Display options 下拉 | **已实装**(Display options=在途件) | 左页签:`screens/feed/feed-screen.tsx:79-90`(FILTERS 未读/星标/稍后读/全部)+ `:1104` 起按钮组;右下拉:`:1183-1208`(未读优先+分组切换,A-feed) | 关闭(已做/在途) |
| 4 | 情报卡行=品类标+粗标题+右对齐灰色相对时间 | **已实装** | `feed-screen.tsx:336-352`(truncate 标题+`<time>` 右对齐 text-2xs muted) | 关闭(已做) |
| 5 | hover:行背景 accent/50+操作按钮浮现 | **已实装** | `feed-screen.tsx:322`(`hover:bg-accent/50`)、`:355-357`(操作簇 `opacity-0→group-hover:opacity-100`,focus-within 保键盘可达) | 关闭(已做) |
| 6 | 未读左侧 2px accent 竖条+`U` 快捷键 | **已实装** | `feed-screen.tsx:326-334`(w-0.5 竖条,未读 bg-primary)、`:949`(pressed==="u") | 关闭(已做) |
| 7 | 右键 ContextMenu(复制链接/标已读/沉淀) | **在途(A-feed)** | `components/ui/context-menu.tsx`(基件已落);`feed-screen.tsx:308-727`(三动作+沉淀入口 `:725`) | 在途,勿重复立项 |
| 8 | `Cmd+F` 内联过滤,Esc 清空 | **部分** | G1 搜索框已落:`feed-screen.tsx:1210-1219`(`type="search"`,Enter 即时+300ms 防抖 `:786-791`);Esc 清空靠 `type="search"` 原生行为+防抖,**无 Cmd+F 聚焦绑定**(keydown 守卫仅 u/j/k,`:949`) | 直接小修 ≤20 行(feed 屏 keydown effect 加 mod+f 聚焦搜索框) |
| 9 | 全键盘 J/K 导航+focus 环 | **在途(A-feed)** | `feed-screen.tsx:934-983`(currentKey 巡游+scrollIntoView nearest)、`:324/:992`(ring 环仅键盘巡游呈现) | 在途,勿重复立项 |
| 10 | 删除无确认,200ms ease-out 高度折叠离场 | **未做**(feed 无删除交互) | `rg "Backspace|删除" feed-screen.tsx` 零命中;G 矩阵亦无条目删除项 | 关闭(语义不匹配:MYIA feed=留存库非 Linear 收件箱;清理走 retention,不为对标硬加) |
| 11 | 数字 tabular-nums;元信息 muted 小一号 | **已实装** | `index.css:218`(`font-feature-settings:"tnum"` 全局)+`:124` 注释;元信息 text-2xs muted(`feed-screen.tsx:348`) | 关闭(已做) |
| 12 | 主题 3 变量派生法 | **维持现状(关闭)** | `index.css:11-48` 为逐 token 直落 hex(非 LCH 三变量派生);teardown 自身判「本仓 :root 已同构,坚持」 | 关闭(拆解表已判坚持) |
| 13 | Tab/内容切换 ease-out 仅 opacity/transform | **已实装(基件层)** | `components/ui/tabs.tsx:169`(TabsContent `animate-fade-in`,token 时长仅 opacity;keyframes `index.css:151-155`) | 关闭(已做) |
| 14 | 图标 16px 与文字 baseline 对齐 | **已实装(惯例贯彻)** | `sidebar.tsx:122-126`(注释明示可抄 #14)+`:153`(size-4);feed 操作簇 size-3.5 同惯例 | 关闭(已做) |

### 1.2 vercel-dashboard(仪表盘,可抄清单 11 条)

| # | 可抄项 | 状态 | 证据 | 路由建议 |
|---|---|---|---|---|
| 1 | 顶栏=搜索位+主操作,**不放统计条** | **已实装** | `components/layout/top-bar.tsx:71-121`(品类过滤+GlobalRun+⌘K 命令位,无统计);仪表盘 PageHeader 动作仅刷新 `dashboard-screen.tsx:418-433`;统计在概览卡 `:468` 起 | 关闭(已做) |
| 2 | 概览条一行四格(小标签+大数字 tnum) | **已实装**(窗口切换=在途件) | `dashboard-screen.tsx:468-558`(今日采集/活跃源/推送成功/告警四格;uppercase 弱色标签 `:479`;大数字 `text-2xl tabular-nums` `:268`);A-dash 独立窗口 Select `:482-499` | 关闭(已做/在途) |
| 3 | StatusDot=8px 圆点+标签,四色映射 | **已实装** | `dashboard-screen.tsx:62-82`(size-2 圆点+health.label,注释明引 teardown #3) | 关闭(已做) |
| 4 | 源健康卡(名称+muted 次行+相对时间,网格 gap-6) | **已实装** | `dashboard-screen.tsx:280-291`(注释明引 #4)、`:703-704`(卡网格 aria-label+gap) | 关闭(已做) |
| 5 | 多选过滤 trigger=点簇+「n/m」徽章 | **未做** | `screens/sources/sources-table.tsx:287-291`(筛选=单输入全局筛选+健康度三态按钮组,无多选 trigger/点簇/n/m) | 入 v12-backlog 池 |
| 6 | 趋势卡=Select 时间范围+自绘 sparkline+building pulse | **已实装** | `dashboard-screen.tsx:319`(windowDays Select);`screens/dashboard/sparkline.tsx:28-29/115-120`(pulse 末点呼吸,注释明引 #6) | 关闭(已做) |
| 7 | 空态=居中标题+描述+主按钮 | **已实装** | `components/empty-state.tsx:22-60`(EmptyState:图标光晕+标题+description+action 槽,compact/整屏两档) | 关闭(已做) |
| 8 | skeleton=同构卡(灰块+短条) | **已实装(四屏齐)** | feed `feed-screen.tsx:1258-1276`(三级形状);dashboard `dashboard-screen.tsx:502-508`;sources `sources-screen.tsx:274`;logs `logs-screen.tsx:607-609`——gap-matrix #10「sources/logs 待核」**核毕=已实装** | 关闭(已做) |
| 9 | 4px 基数密度收进 D2 token | **已实装(token 层)** | `index.css:65-67`(`--spacing-table: 0.25rem` 注释明示 compact 4px 基数)+`:104-120`(D2 token 暴露节) | 关闭(已做) |
| 10 | 圆角维持 8px 不追 Vercel 6px | **已实装(维持)** | `index.css:48`(`--radius: 0.5rem`) | 关闭(已做) |
| 11 | 数字 tnum;时间/ID/错误码 mono | **已实装** | 全局 tnum `index.css:218`;mono 用例:`dashboard-screen.tsx:214`(runId)、`:445/:459/:638`(错误码)、`:220`(时长);logs 屏日志体等宽 | 关闭(已做) |

### 1.3 linear-settings(设置屏,可抄清单 9 条)

| # | 可抄项 | 状态 | 证据 | 路由建议 |
|---|---|---|---|---|
| 1 | 左列分区导航+当前项高亮左竖条+路由 | **已实装** | `screens/settings/settings-screen.tsx:61-63`(注释明引 #1)、`:373-375`(`?section=` 深链)、`:606/:619`(aria-current+左竖条 bg-primary) | 关闭(已做) |
| 2 | 右列每子区一屏:区标题+描述+Card 堆叠 | **已实装** | `settings-screen.tsx:63-64`、SECTIONS 定义 `:94-122`;分区渲染 `:592` 起 | 关闭(已做) |
| 3 | 概览页=「设置 homepage」每区一行摘要 | **未做** | `rg "overview|概览|homepage|每区一行" settings-screen.tsx` 零命中;设置直入默认分区 | 入 v12-backlog 池(低价值:分区仅 5,摘要页冗余)或关闭——倾向**关闭** |
| 4 | 推送区=渠道 Tab(彩色状态点)+类别分组开关 | **未做(部分语义已他处承担)** | 推送=表单 Select:`settings-screen.tsx:799-812`;渠道状态点在消息屏:`screens/messaging/platform-overview.tsx:1037/1248`(StateDotTone 语义 token) | 关闭(形态判定:MYIA 渠道配置=凭据表单,非 Linear 通知中心 Tab;状态点语义已由消息屏承担) |
| 5 | 开关行自动保存无按钮;输入类 sticky 保存条 | **已实装** | `settings-screen.tsx:201-202/:302`(开关即时生效,注释明引 #5);`CardSaveBar :159-160`(卡片底栏保存条,自创项已标注) | 关闭(已做) |
| 6 | 危险操作 Destructive Card+二次确认 | **已实装(inline 形态)** | `settings-screen.tsx:902-914`(destructive 边框卡置区页底部);inline 二次确认 `:398`(注释:同看图模型卡惯例) | 关闭(已做;AlertDialog→inline 为仓内有意惯例) |
| 7 | 表格页复用源管理 DataTable 范式 | **部分(有意不复用)** | 凭据名清单=Badge 流式排列+行内确认:`settings-screen.tsx:922-945`(非 DataTable);DataTable 范式本尊在源管理 `sources-table.tsx:235` | 关闭(场景不匹配:凭据仅名称无列维,表格化属过度) |
| 8 | 设置文案=onboarding 语气+tooltip 辅助 | **部分** | 引导文案已有(CardDescription:`settings-screen.tsx:94/:108/:122`);**零 Tooltip 消费**(`rg Tooltip settings-screen.tsx` 零命中) | 入 v12-backlog 池(弱需求,顺手批可带) |
| 9 | label/icon/button baseline 对齐纪律 | **已实装(惯例贯彻)** | `sidebar.tsx:122-126` 注释;基件层 items-center 惯例(button/badge/dropdown) | 关闭(已做) |

**一层小结**:34 条可抄项 = 已实装/维持 24、在途 4(右键菜单/j-k/Display options/概览窗口)、部分 3(Cmd+F 聚焦、设置 tooltip、—— Cmd+F 为唯一可小修差口)、未做且未关 3(侧栏分组折叠、多选点簇、设置 homepage)。仪表盘报错分区降级(prd Goal 判例)已核:`dashboard-screen.tsx:451-465`(sectionErrors 降级卡)+`:440-449`(全败整屏卡)。

## 二、功能池余量终态(ui-feature-census G1-G12 + 后续)

| 项 | 终态 | 证据 |
|---|---|---|
| G1 条目搜索 | **已做**(10-03-feed-ux) | `feed-screen.tsx:1210-1219`(服务端全库搜索,防抖/Enter);协议方法 `lib/api/client.ts:142` |
| G2 详情/打开原文 | **已做**(10-03-feed-ux) | 展开:`feed-screen.tsx:204-220`;系统浏览器打开:`:394-409` |
| G3 导出 | **已做**(10-03-feed-ux) | JSONL/CSV:`feed-screen.tsx:1075-1096` |
| G4 排程管理+手动触发 | **已做**(10-03-feed-ux) | 品类卡跑一次:`dashboard-screen.tsx:111-178`;排程一览(schedule.preview 并发):`sources-screen.tsx:64`;协议 `types.ts:506/:904` |
| G5 前半 推送测试按钮 | **已做**(10-03-feed-ux) | `settings-screen.tsx:541-571`(push.test 真发) |
| G5 主体 告警规则 | **已做**(10-04-alert-rules,已归档) | 消息屏告警面板:`messaging-screen.tsx:92-95`(alerts.save/test/fired);协议 v7:`desktop/entry.py:429`(只读核验) |
| G6 趋势统计 | **已做**(B4+10-04-desktop-b234,池内已消号) | 趋势卡+sparkline:`dashboard-screen.tsx:319`/`sparkline.tsx`;池回标 `10-03-v12-backlog/prd.md:41-43` |
| G7 run 重跑/过滤/日志搜索 | **已做**(10-03-fe-small-batch) | `logs-screen.tsx:38-40/:127/:135`(三件齐,注释明引 G7) |
| G8 AI 摘要按钮 | **已做**(10-03-fe-small-batch) | `feed-screen.tsx:361-381`(Sparkles 按钮+loading/done 态) |
| G9 批量已读 | **部分→余量留池** | 已落:全部标已读按钮 `feed-screen.tsx:1128-1141`,但**作用域=已加载条目**(`:890-891` 注释如实注明;单条 U/j/jk 键盘已随 interaction-batch 补齐);**全库批量已读未做**(需 store/协议扩展,架构级) | 
| G10 代理池连通性测试 | **留池(v1.2),后端已解锁** | 设置屏仅凭据表单(`settings-screen.tsx:132/383-384`),无测试按钮;后端 10-04-proxy-pool 已归档=依赖就绪 |
| G11 凭据导出 | **关闭(红线不做)** | census 拍板 Q3;`settings-screen.tsx:914`(「值永不可读(secrets.py 契约)」) |
| G12 就地沉淀 | **已做**(10-03-fe-small-batch) | 卡内面板 `feed-screen.tsx:382-393`;右键入口在途 `:725` |
| 远期形态三项(八爪鱼点选建源/代理池面板/凭证猎手) | **留池(v1.2 第 6 项)** | `10-03-v12-backlog/prd.md:49-56` |
| snooze 到期重现(gap-matrix #6) | **留池(v2)** | 稍后读=本地态(`feed-screen.tsx` later 桶),无到期重现;Linear H 键未对标 |
| 设置搜索(gap-matrix #7) | **留池 → 同日 FixStage 已补做** | census 时 `rg 搜索 settings-screen.tsx` 零命中;teardown 自身标注「未实证」低置信;补做回执见上「R9 注记补正」 |

**池文档债**:v12-backlog 池 prd 第 5 节仍列 G5 主体/G7/G8/G12 为待做(`10-03-v12-backlog/prd.md:38-47`),实际均已消号——**池清单漂移,需回标**(非产品代码,档内小修)。→ **已回标(2026-10-04,R4 执行毕,见文首路由执行记录)**。

## 三、质量债存量(fe-small-batch 残留逐条核 + 在案小件)

### 3.1 fe-small-batch 残留(本档点名三项)

| 债项 | 现状 | 证据(含独立复算) |
|---|---|---|
| P1-a 源管理表头排序键盘不可达 | **已修** | `sources-table.tsx:330-346`:排序控件=原生 `<button>`(注释明示「键盘可达(P1):Tab 可聚焦,Enter/Space 由 UA 合成 click」);`aria-sort` `:328` |
| P1-b destructive 徽章对比 4.15 | **已修(独立复算达标)** | `components/ui/badge.tsx:15-17`(文字提亮 #ff6b70,注释记 5.42~6.14);本会话 Python 实算:card 底 5.87 / background 底 6.14,均 ≥4.5;旧值复算 4.15/4.34 与债档记录吻合 |
| 旁核① 侧栏两处小字对比边缘 | **已修(独立复算达标)** | `sidebar.tsx:199-200`(注释:「/70 仅 3.68,/80 仅 4.49;整值 6.46」);实算 #8b94a7 vs #080b13 = **6.46**,与注释一致 |
| 旁核② 日志错误行对比 4.43 | **已修(独立复算达标)** | `logs-screen.tsx:113-115`(bg-dead/10 叠 sidebar 底,注释记 ≈4.67);实算 #e5484d on #1e1119 = **4.67** |
| 旁核③ 设置 destructive 按钮 3.41 | **已修(独立复算达标)** | `components/ui/button.tsx:16-18`(实底压暗 #c53136,注释记 3.41 旧值);实算 #fdebec on #c53136 = **4.73**,hover(/90 叠底)5.44-5.51 |
| text-[11px] 漂移清零(归 text-2xs) | **已清零** | `rg "text-\[11px\]" desktop/ui-src/src` 零命中(exit=1 实跑);token 在 `index.css:126-128`(--text-2xs: 11px) |
| P2⑤ feed 搜索框焦点环 | 已随重做落 | 搜索输入 `feed-screen.tsx:1210-1215` 为简式边框(该框已随 G1/列表头重做迁移至过滤区,原 ring-1 偏离已不复存;当前无 :focus-visible ring 类——**顺带小缺口**,可与 Cmd+F 绑定同批补) |
| P3 消息标题跳级 | **仍登记(勿扩大)** | fe-small-batch prd:20「不入本批」;当前消息屏仅 PageHeader h1(`messaging-screen.tsx:306`+`page-header.tsx:14`),未见跳级复现,维持登记 |

### 3.2 在案小件(gap-matrix 遗留,现状复核)

| 债项 | 现状 | 证据 | 路由 |
|---|---|---|---|
| AlertsFiredEvent 未入 SidecarEvent 联合 | **解锁待做**:联合确缺,但协议侧已实装(注释前置条件已满足) | `lib/api/types.ts:1009-1012`(注释:「协议侧 alerts.fired 实装(entry.py `_write_line`)时再加入联合」)+`:1026-1033`(联合无 AlertsFiredEvent);`desktop/entry.py:2429-2460`(alerts.fired 回放已实装,v7 `:429`)——**前置条件已满足,可入联合** | 直接小修 ≤20 行(入联合+logs 屏穷尽守卫适配 `screens/logs/api.ts unknownEvent`) |
| suppressed 状态词表 v2 | **未做(仍登记)** | `types.ts:1021` action_status 词表 = pending/sent/send_failed/tagged/degraded_no_channel/skipped_dry_run,无 suppressed | 入 v12-backlog 池 |
| 消息屏告警面板真机手验 | **留装机验收**(已立档) | `10-04-wrapup-checklist/prd.md` 第二节(装机/真机验收)+第三节(真机飞书/TG 收卡) | 关闭(已归 wrapup-checklist 档) |
| 装机包版本号 0.0.1 | **未对齐(仍在)** | `desktop/src-tauri/tauri.conf.json:5` = "0.0.1";`desktop/package.json:4`/`ui-src/package.json:4` = 0.1.0 | 直接小修 ≤20 行(收官流改 tauri.conf version 对齐发布线;本普查红线不动 desktop/) |

## 处置路由汇总(只建议不执行)

| # | 领域 | 建议 | 量级 |
|---|---|---|---|
| R1 | feed Cmd+F 聚焦搜索框(+Esc 即时清空+搜索框 focus ring 补齐) | 直接小修 ≤20 行 | low |
| R2 | AlertsFiredEvent 入 SidecarEvent 联合+logs 穷尽守卫适配 | 直接小修 ≤20 行 | medium |
| R3 | tauri.conf.json 版本号 0.0.1 对齐发布线 | 直接小修 ≤20 行(归收官流) | medium |
| R4 | v12-backlog 池 prd 回标 G5 主体/G7/G8/G12 已消号 | 直接小修(档内文档) | low |
| R5 | G9 全库批量已读(store/协议扩展) | 立档(架构级,先 grill) | medium |
| R6 | G10 代理池连通性测试按钮(后端已解锁) | 入 v12-backlog 池(v1.2,与代理池面板同族拆批) | low |
| R7 | 侧栏分组可折叠 / 源管理多选点簇筛选 / 设置 tooltip 辅助 / snooze 到期重现 / 设置搜索 / suppressed 词表 / P3 消息标题跳级 | 入 v12-backlog 池 | low |
| R8 | linear #10 feed 条目删除 / settings #3 设置 homepage / settings #4 渠道 Tab / settings #7 凭据表格化 | 关闭(语义不匹配或过度,理由见各表) | low |
| R9 | 六件在途(⌘K/右键/快捷键底座/侧栏折叠/仪表盘窗口/feed j-k)+ 对标已实装 24 项 | 关闭(在途归 interaction-batch;已做项见各表) | — |

## 附:核验方法留痕

- 代码证据:本会话 rg/Read 实跑,路径均相对 `desktop/ui-src/src`;`rg ChevronDown sidebar.tsx`、`rg "text-\[11px\]"`、`rg "Backspace|删除" feed-screen.tsx` 等零命中项以 exit=1 留痕。
- 对比度:Python 脚本按 WCAG 相对亮度公式独立计算(混合色 = over@alpha 叠加 base),复算旧值 4.15/3.41 与债档记录吻合后方采信新值;未运行浏览器取色工具。
- 档案:三份 teardown、interaction-batch prd、ui-feature-census prd、fe-small-batch prd、v12-backlog prd、wrapup-checklist prd 均本会话全文实读;gap-matrix.md(本档 research/ 前身)亦实读,其「待核」项(sources/logs 骨架)本轮核毕。
- 未做:未跑 `npm test`/`tsc`(普查只读不验构建,在途双流占有工作树);未做像素级目验(需主人装机,见 wrapup-checklist)。
