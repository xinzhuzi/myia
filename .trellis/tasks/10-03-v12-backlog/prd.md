# v1.2 待办池:Windows 构建 + crawl4ai L3 实装 + proxy_pool 对接

## Goal

grill 决议 2026-10-03 Q1:发布工程(v1.1.1)先行,以下三项排 v1.2。本档是
**待办池**(非执行档):收边界、现状与验收指针;开工时逐项拆正式任务
(复杂项按规矩补 design/implement)。

## Requirements(三项边界)

1. **Windows 产物化**
   - 现状:`desktop-release.yml` 已有 windows-latest job(msi,**构建级验证、
     允许失败**);PyInstaller 不可交叉编译 → CI native matrix 是唯一路。
   - v1.2 目标:msi/exe 产物可用(真机安装冒烟,对齐 v1.1.1 的 macOS 验收
     口径:cwd 无关路径解析 + 首跑种子 + 五屏数据/空态)。
   - 开放:主人有无 Windows 真机/VM 做冒烟(拆任务时问)。
   - **回标(2026-10-05,盘点员)**:**已消号**——归属 `10-04-windows-build`(已归档):
     CI desktop-release run 37186006759 三作业全绿、**windows-msi 首绿**(2026-10-04,
     产物 myssia_0.0.1_x64.msi+.sig ASCII);上文「允许失败」为池档过时口径,
     已被 0378ed3(productName 拆 WiX 非 ASCII 雷)/b0044c5(msi 布局 glob)两轮
     修复终结;真机安装冒烟七项留主人(wrapup-checklist 档);**本地自助构建链
     另线在途 `10-05-win-local-build`(in_progress:家庭 Windows 真机 UGit 克隆
     →复刻 CI 链本地打 MSI→静默安装冒烟)**。上方「现状/开放」小节仅存档备查。
2. **crawl4ai L3 实装**
   - 现状:`src/myia/engines/crawl4ai.py` 为薄层(~10KB);v0.2 任务
     (10-01-v02-engine-crawl4ai)按其范围已毕,L3 降级档实质缺位。
   - v1.2 目标:真引擎进降级链(L2 失败→L3 接管),extras 可选依赖
     `shishi[crawl4ai]`,测试走录制回放(CI 零外网,Python spec)。
   - **回标(2026-10-05,盘点员)**:**已消号**——归属 `10-04-crawl4ai-l3`(已归档,
     2026-10-04 交付 review):真引擎进降级链+首遇终身一次探测/预算 3/30s 帽/
     aihot 目标(grill 四决议)+探测 fixture 六件+真网双路冒烟;「L3 实质缺位」
     系池档过时口径(教训在册:选池档任务前先对归档验前提)。
     extras 现名 `myssia[crawl4ai]`(命名终局 myssia;现路径
     `src/myssia/engines/crawl4ai.py`)。
3. **proxy_pool 对接**
   - 现状:fetch_base 有 143 处 proxy 引用,transport 单上游(v0.2 已毕,
     10-01-v02-proxy-transport);池化(轮换/健康检查/住宅 IP)未写。
   - v1.2 目标:池化抽象 + 至少一家服务商实装;**服务商与预算是主人决策**,
     拆任务时先问。
   - **回标(2026-10-05,盘点员)**:**已消号**——归属 `10-04-proxy-pool`(已归档,
     f759c87):多上游轮换/被动健康/半开恢复/每池熔断+doctor 逐上游探测
     (2026-10-04 交付);服务商决策见本档「主人侧前置」节(已答:有);
     余量「代理池管理面板 UI」在第 6 项远期形态池继续留池。
4. **B2/B3/B4 桌面补实现**(grill Round 3 Q6:v1.1.1 先改宣称,补实现排 v1.2)
   - 桌面反馈入口(feed 卡片反馈按钮,对应 CLI feedback mark/list/stats)
   - settings 屏反馈开关分区(routes 骨架曾列)
   - dashboard 采集量趋势(v1.1 PRD 承诺项)
   - 与第 2 项 C 组批次(10-03-v112-desktop-batch)的取舍:实现顺序上
     C2/C1/C7 优先于本项。
   - **回标(2026-10-03 路由落档):本项整体移交 `10-03-v112-desktop-parity`
     (v1.1.2 桌面对齐批次)吸收,提前于 v1.2 开工——上文「排 v1.2」已被覆盖;
     本池剩余三项(Windows/crawl4ai/proxy_pool)与第 5 项 UI 池不变。**
5. **UI 普查 P2/P3 项入池**(2026-10-03 ui-feature-census grill Q2 批复「全部入池不加码」;
   证据与业界参照见 `.trellis/tasks/10-03-ui-feature-census/prd.md` G 矩阵)
   - G5 主体:告警规则(Inoreader Rules 式条件→动作,涉 sidecar 协议扩展;
     G5 前半「推送测试按钮」已随 `10-03-feed-ux` 批次先行)
     → **已消号**:已做,归属 `10-04-alert-rules`(已归档)——消息屏告警面板
     alerts.save/test/fired(`messaging-screen.tsx:92-95`)+ sidecar 协议 v7
     (`desktop/entry.py:429`);2026-10-04 fe-gap-census matrix §二核验回标
   - G6:采集量/成功率趋势折线(与 B4 采集量趋势同属一块,拆任务时合并考虑)
     → **已消号**:采集量半边随 B4(10-03-v112-desktop-parity)、成功率半边随
     `10-04-desktop-b234`(`runs.trend` 协议方法 + 仪表盘同块第二序列,2026-10-04)
   - G7:run 重跑/按品类状态过滤/日志内搜索(重跑依赖 feed-ux G4 的手动触发通道)
     → **已消号**:已做,归属 `10-03-fe-small-batch`(已归档)——logs 屏三件齐
     (`logs-screen.tsx:38-40/:127/:135`,注释明引 G7);fe-gap-census matrix
     §二核验回标(2026-10-04)
   - G8:情报流卡片「AI 摘要」按钮(enrich 管线现成);情绪标注 v2 再议
     → **已消号**:已做,归属 `10-03-fe-small-batch`(已归档)——Sparkles 按钮
     +loading/done 态(`feed-screen.tsx:361-381`);情绪标注 v2 维持再议;
     fe-gap-census matrix §二核验回标(2026-10-04)
   - G9:快捷键与批量操作(全部标已读等)
     → **已消号**:已做,主体归属 `10-04-read-state-server`(已归档)——
     store.state.mark_all 全库批量语义三端+UI 能力门+按钮真话(commit
     afa7339);快捷键/右键批量件随 `10-04-interaction-batch`(已归档);
     余量档 10-04-g9-read-all(按品类批量入口+全库确认交互)同日撤并,
     不另立项;fe-gap-census matrix §二核验回标(2026-10-04);
     **余量翻案(2026-10-04 晚)**:撤并后主人令重开,余量两小件已由
     10-04-g9-read-all(重开)交付
   - G10:代理池连通性测试按钮(doctor --config 探测已有,差 UI)
     → **后端依赖已解锁**:`10-04-proxy-pool` 已归档(2026-10-04 fe-gap-census
     matrix §二核验:设置屏仅凭据表单 `settings-screen.tsx:132/383-384`,无测试
     按钮);维持留池(v1.2),增补回执见第 8 项
   - G12:条目卡「就地沉淀为关键词」入口(OpenCTI 快捷订阅铃铛式,衔接 yaml-editor)
     → **已消号**:已做,归属 `10-03-fe-small-batch`(已归档)——卡内沉淀面板
     (`feed-screen.tsx:382-393`);右键入口随 `10-04-interaction-batch` 在途
     (`feed-screen.tsx:725`);fe-gap-census matrix §二核验回标(2026-10-04)
   - G11 不入池:并入 F 类刻意不做(凭据导出,security-baseline 红线)
6. **UI 模仿总表远期形态三项入池**(2026-10-03 `10-03-ui-deep-imitation` grill 决议②:
   不入 v1.x 视觉批次,沉本池;对标与取材策略见该任务 prd「取材策略」节)
   - 八爪鱼点选式任务配置(可视化建源,YAML 编辑器的远期形态;对标八爪鱼/EasySpider/Maxun)
   - 代理池管理面板(出口列表/测活/成功率统计,对标 jhao104/proxy_pool 面板;
     与第 3 项 proxy_pool 后端对接、G10 测试按钮同属一族,拆任务时合并考虑)
   - 凭证猎手面板(key/余额/高危列表,对标 aipocket;**只展示与管理,不含导出**——
     与 G11 红线区分)
7. **Reddit 情报源**(2026-10-03 主人点名入池:「Reddit 也是情报收集渠道」;
   RSS 采集能力已随 `10-03-news-rss` 落地,缺的只是 Reddit 的合规通道)
   - 现状(wrap 三路探查,证据 `archive/2026-10/10-03-games-wrap/evidence/news-probe-reddit-*`):
     `new.json` 对 honest UA 403;`.rss` 200 Atom 且 round2 实测 `entry link@href`
     25/25 可提取,但 robots.txt `User-agent: *` `Disallow: /` 全站禁抓 +
     Public Content Policy 限自动化——respect_robots 判例维持不可直抓
     (news-rss prd 同判)。
   - 可行路径(connector-selection「免费路径是什么」):官方 Data API OAuth
     免费层(非商业 ~100 QPM 口径,robots.txt 自指 r/reddit4researchers 为
     研究/非商业通道;拆任务时核实额度并加快照日期);聚合器(XFlux 型,
     supplier-map 判例:收紧源优先评估聚合器,但只做可选后端永不默认)。
   - robots/政策会漂移:拆任务时先重探 robots.txt 再定通道。
   - 场景通用:games(r/GamingNews 曾候选)之外,ai-news 等场景同享。
8. **fe-gap-census 增补入池**(2026-10-04 `10-04-fe-gap-census` 普查处置路由
   R6/R7;判词与证据出处 = `.trellis/tasks/10-04-fe-gap-census/research/matrix.md`)
   - G10 代理池连通性测试按钮(回执:即第 5 项 G10——后端 `10-04-proxy-pool`
     已归档=依赖解锁,差设置屏测试按钮;与第 6 项代理池管理面板同族,
     拆任务时合并考虑;出处 matrix §二 G10 行/路由 R6)
   - 侧栏分组级折叠(每组 ChevronDown 旋转 ~150ms;区别于在途
     interaction-batch 的整栏 `[` 折叠键——现状分组固定展开,
     `rg ChevronDown sidebar.tsx` 零命中;出处 matrix §1.1 #2/路由 R7)
     → **已消号(2026-10-05)**:登记口径已过时——`7853d96`(2026-10-04
     Kestra 基调重锚批)已落全链路:`sidebar.tsx` GroupSection(:198-243;
     标题钮 aria-expanded + ChevronDown size-3.5 折叠旋 -rotate-90,过渡
     `duration-(--duration-fast)`=**120ms**(原「~150ms」口径不准;定义
     `index.css:112`)、条目区 grid-rows 0fr↔1fr **250ms** Kestra 缓动
     cubic-bezier(0.22,1,0.36,1)、折叠时内层 inert 防键盘焦点);独立
     存储键 `myssia.sidebar-groups.v1`(:86/:135/:155)与整栏折叠键
     `myssia.sidebar.v1` 分立,两组语义独立共存;`rg ChevronDown
     sidebar.tsx` 今已命中。处置=池档销号,零代码改动(归属
     `10-05-fe-gap-batch` ②a 销号核验)。
   - 源管理多选点簇筛选(多选过滤 trigger=点簇+「n/m」徽章;现状=单输入全局
     筛选+健康度三态按钮组 `sources-table.tsx:287-291`;出处 matrix §1.2 #5/
     路由 R7)
     → **已消号(2026-10-05)**:`10-05-fe-gap-batch` ②b 实做落地——
     sources-table.tsx 增 clusterFilter Set(簇键=pluginFile)+ 簇 chips 条
     (aria-pressed+逐簇源数徽章+「清除」钮,单簇不渲染)+ data 前置派生
     与 globalFilter/健康度按钮组正交叠加(空 Set=全量;刷新后失效簇键
     自动剔除防空屏)+ n/m 徽章 aria-live;vitest 四用例(单簇/多选×健康度
     叠加/n·m 计数/清空复位)入 sources.test.tsx。
   - 设置 tooltip 辅助(引导文案已有、零 Tooltip 消费;弱需求,顺手批可带;
     出处 matrix §1.3 #8/路由 R7)
     → **裁撤(2026-10-05,`10-05-fe-gap-batch` ②c)**:维持弱需求判定不
     做——基件 `ui/tooltip.tsx` 在库而全 UI 零业务消费(唯一引用=基件自测
     ui-base.test.tsx),settings-screen.tsx 零命中;同轮已排源管理点簇
     (②b)与代理池测试按钮两 UI 件,避免面铺宽。**翻案极小方案**(留池,
     半小时量):ui/tooltip.tsx 直接消费,设置屏 3-5 个高困惑字段(enrich
     模型/探测路径/gates 凭据引用)挂 Radix Tooltip + vitest a11y 断言。
     → **已消号(2026-10-05 晚,翻案落地)**:归属 `10-05-ui-chore-batch`
     子件①——五字段挂通(预算护栏行/代理池池名/gates SaaS API Key 值/
     运行时下载源覆盖/PyPI 镜像覆盖),新组件 label-hint.tsx(HintButton+
     LabelHint)消费既有基件,a11y 断言 aria-describedby 接通三例入
     settings/pyenv 测试;基件不装包红线维持(自研实现非 Radix 真包)。
   - snooze 到期重现(稍后读=本地态 later 桶、无到期重现,Linear H 键未对标;
     matrix 原文标「留池(v2)」;出处 matrix §二/路由 R7)
     → **已消号(2026-10-06)**:归属 `10-05-fe-gap-leftovers` ①(949802a)
     ——feed 层最小面落地:LATER_RESURFACE_DAYS=7 天提醒时效(与时间分组
     「7 天内/更早」同界),已读+稍后读条目放入超窗即到期重现于默认未读
     视图(applyFeedFilter 并入,now 注入可测;取消稍后读即离场);锚点
     first_seen——置位时刻服务端(0/1 列)/本地态(map)均无落点,不为
     时效扩存储;first_seen 缺失/无效保守不起重现;书签 title 知会规则+
     稍后读空态文案;纯函数 isLaterResurface/applyFeedFilter 边界 + 服务端
     通路屏测(到期回未读/未到期只在桶/桶内全量可见)vitest feed 91/91。
   - 设置搜索(`rg 搜索 settings-screen.tsx` 零命中;teardown 自身标注
     「未实证」低置信;出处 matrix §二/路由 R7)
     → **已消号(2026-10-06)**:归属 `10-05-fe-gap-leftovers` ②(b8a6a7b)
     ——登记口径已过时(10-04-interaction-batch 已补分区级过滤框,census
     #7);余量=字段级:导航匹配扩区内字段词面(SECTION_FIELD_TERMS 策展
     清单,查 base_url/镜像不再落「无匹配分区」)+ 右列直属卡逐卡过滤
     (Searchable:分区名命中整区显示/字段词命中只显命中卡/全不命中卡全隐
     +指路空态行);整件子组件区(视觉/门槛件/装机/Python)按区词面整件
     显隐不进组件内部(穿 5 子组件文件超小件面,如实注记);既有四用例随
     新语义更新 + 新增三用例,vitest settings 7 文件 120/120。
   - suppressed 状态词表 v2(action_status 词表 `types.ts:1021` 无 suppressed;
     出处 matrix §3.2/路由 R7)
     → **已消号·词表先行(2026-10-06)**:归属 `10-05-fe-gap-leftovers`
     ③(305c7be)——消费点先核:action_status 两 UI 消费位(messaging 屏
     toast / logs 屏 eventToRow)均原样透传渲染、无词表分档,故按池档口径
     只加词表+注记:AlertsFiredEvent.action_status 词表补 suppressed 并
     注明 v2 预留语义(同槽位防重发拦截专属终态;现状该路径记 send_failed
     ——engine.py `_execute_push_with` 零报告回落,后端
     ALERT_ACTION_STATUSES/store/models.py 未收词,真拆分归 v2 后端批;
     行号漂移注记:池档原引 types.ts:1021,今 types.ts:1436)。
   - P3 消息标题跳级(fe-small-batch prd 判「不入本批」;当前消息屏仅
     PageHeader h1、未见跳级复现;维持登记、勿扩大;出处 matrix §3.1/路由 R7)
     → **已消号(2026-10-05)**:归属 `10-05-messaging-heading-levels`——登记
     口径已过时(PageHeader 无头化后「仅 PageHeader h1」不复存;真实形态=
     消息屏首标题即 platform-overview 的悬空 h3),修法=CardTitle 加 `as`
     prop + 消息屏四分区卡头 `as="h2"`、详情面板 h3/h4 归位,视觉零变化;
     勿扩大纪律延续:其余屏的 CardTitle 用法与无标题现状未动

9. **补验沙箱窗自标识(工程实践小件,2026-10-05 晚入池)**
   - 现状:装机件 UI 补验按判例走 MYIA_SHOW_ON_START=1 直跑二进制+沙箱
     MYIA_HOME(全屏终端 Space 墙下的亮窗正解)——窗口与生产态零视觉区分;
     本轮主人亲历:补验窗口弹出后在沙箱实例里点了「检查状态」,见
     `[deps_fingerprint] 进度戳无依赖指纹` 失败项,引出一场诊断(真机无恙,
     证据见 archive/2026-10/10-05-bundled-plugins-install prd「补验销号」段)。
   - 改进:补验/自动化拉起的实例在窗体自标识(标题后缀「(沙箱)」或顶栏
     细横幅,按 MYIA_HOME 指向一次性目录判定),UI 半行级 + vitest 一例。
   - 量级:半小时;随下个桌面 UI 批顺手带,不单独立项。
   - **回标(2026-10-05 晚)**:**已消号**——归属 `10-05-ui-chore-batch`
     子件②:Rust 侧最小面落地(纯函数 sandbox_title + setup set_title,
     判定=壳进程 env 显式 MYIA_HOME,与 data_root/单实例锁 var_os 分支同
     口径;置冒烟路由/亮窗之前),主窗标题「世事(沙箱)」;测试按实现面
     取 cargo 单测两例(Some 加后缀/None 透传)非 vitest。
10. **GitHub 集成候选批(2026-10-05 深夜盘点轮入池;主人令「都落实到
    trellis 任务文档」)**——盘点口径:RSSHub 已在(官方场景件
    plugins/myssia-rsshub,DIYgod/RSSHub 封装,AGPL 只作自托管 HTTP 服务
    消费零代码复用);以下为核实后**未集成**且与产品(自托管情报调度台)
    相性好的候选,按价值排序,全部自托管友好;开工时逐件拆正式任务:

   - **Apprise(推送统一层,扩张比最高)**:MIT,一个 pip 依赖解锁 100+
     推送目标(Discord/Slack/Teams/Pushover/Gotify/…),现推送面 6 通道
     (telegram/feishu/ntfy/dingtalk/wecom/weixin);挂点=push 层新增
     `apprise` 通道(目标串走该库原生 URL 形态,凭据引用体系 env:/keychain:
     照旧),extras 形态(`myssia[apprise]`)与 trafilatura 先例同构;
     桌面锁不进(可选件)。
   - **Bark(iOS 推送十行级小通道)**:自建或官方端点,HTTP POST 一发即达,
     通知即时性远超 TG/飞书;挂点=push 层 `bark` 通道(端点+可选 key 走
     凭据引用);可与 Apprise 同批或单拆。
   - **SearXNG(自托管元搜索 → 情报源)**:搜索式情报(关键词日报/舆情面),
     走现有 static_html/direct_api 引擎层零新引擎;拆任务时先探其
     format=json 接口与 robots 口径(自托管实例 robots 自控)。
   - **Firecrawl OSS server(自托管 JS 渲染+正文,gates 引擎族自托管兜底)**:
     给 Zenrows/ScraperAPI 之外添零供应商依赖的一条路(自托管 API 兼容层);
     ui-feature-census 时只评过其 SaaS 面参考价值低,自托管面未探——拆任务
     时先探 OSS server 与 SaaS API 的兼容度再定「gated 引擎」还是独立引擎。
   - **cron 心跳告警(原生小功能,非外部依赖)**:executions 账本上加
     「某品类久未触发」规则(healthchecks.io 式 dead-man switch),与告警
     规则族(alerts.save/fired,10-04-alert-rules)合并考虑,监控自身调度
     健康。
   - 弱需求备忘(idea 池,不拆任务):changedetection.io(UI 模仿册在案,
     urlwatch 覆盖大半,增量=快照/diff 可视化)、gallery-dl(媒体情报扩容,
     yt-dlp 同族)、ArchiveBox(urlwatch 变更时网页留档)。
   - 死路不再追(档内在案):Pushshift(2023-05 起 mod-only)、GNews RSS
     (robots 禁)、Bing RSS(本出口 302 墙 PoC)、smzdm(反爬)、Reddit
     直抓(robots 全禁,官方 API 路在 `10-05-reddit-source` 决策+并行
     reddit-official-engine 线)。
   - 备忘(本轮盘点同期工程面状态,非池项):11 笔未推(CI 未验新代码)、
     装机包(9c287b1 构建)落后 HEAD 五笔——推送过 CI 后应走重打包换装
     (「完成=装机包刷新」判例);待主人过目 4 档 review
     (telegram-token-dedupe/ui-chore-batch/win-second-instance-show/
     reddit-source,后者 10-31 API 申请截止剩 26 天)。
   - **回标(2026-10-05 深夜 grill 深化轮)**:真候选拆正式档——Apprise→
     `10-05-push-apprise`、Bark→`10-05-push-bark`、SearXNG→
     `10-05-source-searxng`、Firecrawl→`10-05-firecrawl-selfhost-verify`、
     cron 心跳→`10-05-cron-heartbeat`(五档 prd+task.json 齐,planning,
     各含背景锚点/grill 决议/实现细节/UI 美化/测试用例级/验证含装机件
     像素/AC/边界)。grill 事实修正三处:①「现推送面 6 通道」失实——
     PushChannel 实数 **31**(schema.py:229,slack/discord/teams/matrix/
     mattermost/…已在),Apprise 增量=长尾非「6→160」;②Apprise 原生含
     `bark://`,Apprise/Bark 两档关系改「不互斥,先落地者裁或并存主人定」;
     ③Firecrawl 引擎**已在库且默认自托管端点** 127.0.0.1:3002
     (firecrawl.py:48,MYIA_FIRECRAWL_URL/KEY 调用时覆盖)+已入降级链
     (registry.py)——候选缩水为「真跑验证+部署指引」验证型档。弱需求
     备忘与死路清单维持本池不动。
## 主人侧前置(2026-10-03 grill Q4 已答)

- **Windows 真机/VM:有**——v1.2 Windows 拆任务按完整安装冒烟口径(对齐 macOS 的
  cwd 无关路径解析 + 首跑种子 + 五屏数据/空态),不做降级。
- **proxy 服务商与预算:有**——拆 proxy_pool 任务时主人提供具体服务商,先做池化
  抽象 + 该服务商实装。

## Acceptance Criteria(池档口径)

- [ ] v1.2 规划时三项各自拆成正式任务并引用本档
- [ ] 本档不挂 in_progress(它是池,不是工)

## 本轮纪要(2026-10-05 收口轮)

池档口径不动(上两项维持未勾)。同轮收口归档四件,与本池沾边的动向如实记:
`10-05-engine-curl-cffi` 定案**不进 AUTO_CHAIN 亦不链外注册**(七站三路矩阵
零「仅 curl_cffi 过」例,再触发条件=出现「TLS 墙+静态 HTML 有内容」实证源)、
`10-05-extract-trafilatura` 定案 static_html 引擎内回退(实现另立阶段,首步
须跑 impact _fetch_page/extract_html)——两者若 v1.2 开工属引擎链域引用;
另 `10-05-plugin-market-batch` 与 `10-05-table-restore` 同轮归档(CI run
37277285803 五作业全绿;table-restore AC4 装机开关真装链因装机包内容早于
组件链入库结构性受阻留 owner 重装后再验)。

## 本轮纪要(2026-10-05 低危尾款清扫轮,task 10-05-lowrisk-sweep)

**冻结广播(先说最重要)**:plugin manifest「install.source 统一切 shishi
批末专项」**作废,任何并行会话勿再执行**——2026-10-05 二次亲核,GitHub 现以
`xinzhuzi/myia` 为真名(`gh api repos/xinzhuzi/myia` → full_name=xinzhuzi/myia
且无重定向来源;shishi 访问被 301 解析到 myia),全仓 20 件 manifest source
现值即真名、fresh install 零重定向;照旧执行「切 shishi」会把 20 件改成别名
方向。`plugins/myssia-crawlab/plugin.yaml` 原过时注记(方向反了)已同轮更正;
GitNexus 索引名 shishi 系索引层滞后,与远端名无关,不在本专项范围。

低危尾款四件处置结果(详情与引线 = `10-05-lowrisk-sweep` prd.md):

- **①a zenrows css_extractor 显式 null 判值——销号**:ead33f7 已修在库
  (`src/myssia/engines/zenrows.py:82` 判值口径 `is not None`;守卫
  `tests/engines/test_saas_gated_engines.py:312-338`),本轮亲证,零代码零测试。
- **①b saas gated「零上游请求」守卫 robots 盲区——销号**:ead33f7 两守卫在库
  (`test_saas_gated_engines.py:176-192` 关闭态连 robots 拉取一并零请求;
  `:194-211` robots 拒+门开=robots_disallowed 零付费上游),本轮亲证。
- **①c sidecar-protocol「gates.get 非法参数」超前半句——销号**:超前半句
  已删对齐代码(`.trellis/spec/desktop/sidecar-protocol.md:282` 现文口径=
  多余键忽略仅入口层通用拒绝;grep「非法参数」该文件零命中),本轮亲证。
- **①d install.source 仓库名——修注记不修值**:真名反转亲证(myia=真名),
  20 件 source 值零改动;唯一改动=crawlab plugin.yaml 注记更正(git diff
  仅注释行);golden 面排查=`test_plugin_packages.py:165` 只锁 `https://`
  前缀不锁仓库名,无需再生;`desktop/src-tauri/tauri.conf.json:91` updater
  endpoint 同为 myia 真名无需改。

## 本轮纪要(2026-10-05 收口归档轮)

五档收口归档(archive/2026-10),消号项逐条回标:**①a** zenrows 显式 null
判值/**①b** robots 盲区守卫/**①c** 协议文档超前半句——三件销号
(`10-05-lowrisk-sweep`,348af86);**①d** install.source=真名反转注记更正+
冻结广播(同档);**②a** 侧栏分组级折叠销号(7853d96 已在库)/**②b** 源管理
点簇筛选实做(c26f681)/**②c** 设置 tooltip 裁撤记档(`10-05-fe-gap-batch`);
G10 探测一键化(`10-05-g10-proxy-probe`,ebfb34e)、trafilatura L2 兜底
(`10-05-trafilatura-impl`,ba8af60)、装机组件接线(`10-05-bundled-plugins-install`,
f77f894;装机链 UI 验证受阻待 owner 重打包,回执如实注)同轮归档;
`10-05-reddit-source` 按其 AC 维持 review 不归档(停主人决策点五项)。
收口门禁全绿(全量 pytest 4284/0 failed+净树 +31 对账/vitest 474/cargo 54/
ruff/协议对账 64 三方一致/守军九件 302),CI run 37304222631 success @
3470b59(归档轮 gh 亲验,六流提交均亲证在其历史内);池档口径不动
(上方两项 AC 维持未勾)。
