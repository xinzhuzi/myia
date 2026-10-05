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
   - 源管理多选点簇筛选(多选过滤 trigger=点簇+「n/m」徽章;现状=单输入全局
     筛选+健康度三态按钮组 `sources-table.tsx:287-291`;出处 matrix §1.2 #5/
     路由 R7)
   - 设置 tooltip 辅助(引导文案已有、零 Tooltip 消费;弱需求,顺手批可带;
     出处 matrix §1.3 #8/路由 R7)
   - snooze 到期重现(稍后读=本地态 later 桶、无到期重现,Linear H 键未对标;
     matrix 原文标「留池(v2)」;出处 matrix §二/路由 R7)
   - 设置搜索(`rg 搜索 settings-screen.tsx` 零命中;teardown 自身标注
     「未实证」低置信;出处 matrix §二/路由 R7)
   - suppressed 状态词表 v2(action_status 词表 `types.ts:1021` 无 suppressed;
     出处 matrix §3.2/路由 R7)
   - P3 消息标题跳级(fe-small-batch prd 判「不入本批」;当前消息屏仅
     PageHeader h1、未见跳级复现;维持登记、勿扩大;出处 matrix §3.1/路由 R7)
     → **已消号(2026-10-05)**:归属 `10-05-messaging-heading-levels`——登记
     口径已过时(PageHeader 无头化后「仅 PageHeader h1」不复存;真实形态=
     消息屏首标题即 platform-overview 的悬空 h3),修法=CardTitle 加 `as`
     prop + 消息屏四分区卡头 `as="h2"`、详情面板 h3/h4 归位,视觉零变化;
     勿扩大纪律延续:其余屏的 CardTitle 用法与无标题现状未动

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
