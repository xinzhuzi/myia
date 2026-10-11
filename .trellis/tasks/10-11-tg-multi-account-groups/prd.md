# TG 多账号监控台:情报流 2 级账号与群组管理,联合 telegram-web.yaml

主人原话(2026-10-11):「这个地方的配置,是要多个账号的,并且把它放到 情报流的 二级界面上面,你做好布局设计,做好多账号,然后每个账号里面控制展示群,要联合这个配置文件去做」。

## 背景与现状(已核实的仓库事实)

- **网页线(C 线 tg_web)多账号已支持**:设置 → Telegram 监控 → 网页登录卡有账号列表(添加/重新登录/删除,`telegram.status`/`telegramWebLogin`/`telegramWebDelete`,browser 模块单入口);每账号一个 Playwright persistent 配置档(`<数据根>/telegram-web/<账号键>/`),登录态持久。
- **监控目标(群)目前是纯手改配置**:`plugins/telegram-web.yaml` 的 `sources[]`(engine: tg_web;`name`/`url` 锚/`engine_options.tg_web.{account,chat,lookback_limit,keywords,llm_*}`;chat 支持 data-peer-id 全等或标题包含匹配);一账号多群 = 同 account 多源。加/换群要手改 yaml + 重启,主人不可自助。
- **watcher 生效链**:sidecar 常驻 serve 启动时装配 sources → 每账号×群一 Watcher 页;yaml 变更后**不热重载**(生效 = 重启 app 或重启 sidecar serve,方案阶段核实 web_host 是否可增量加减 watcher)。
- **情报流 2 级现状**:Telegram 类型页列出该类型下的渠道(来自条目聚合),只读,无账号管理、无群控制。
- **设置页已有可复用 IPC 面**:`telegram.status`(三线快照)/`telegramWebLogin`(browser 模块单入口)/`telegramWebDelete`;yaml 读写有配置编辑屏的既有通道。

## 需求(主人定调逐条)

### R1 情报流 2 级(Telegram 类型页)= 账号与监控群管理区

- Telegram 类型页顶部新增「账号与监控群」区:
  - **账号列表**:网页线账号(登录态●/重登/添加/删除)——复用设置页 telegram-api 三操作,同源不双写;
  - **每账号监控群列表**:该账号当前监控的群(读 telegram-web.yaml sources 按 account 过滤),每群可「取消监控」;
  - **添加监控群**:输入群名(标题包含匹配词)或从账号可见群中选择(若 web_dom 能枚举侧栏,计划阶段核实;不可行则 v1 手填),写入 yaml sources。
- 布局:与 2 级渠道列表上下分区或左右分栏,计划阶段出布局稿;不打断渠道列表主功能。

### R2 联合配置文件(telegram-web.yaml 为唯一事实源)

- 群勾选/取消 = 读写 telegram-web.yaml `sources[]`(增删该 account 的源条目),**带 schema 校验与失败回滚**(写坏拒载 = 空态事故,必须防);
- 账号删除时联动清理其名下 sources(带确认);
- 关键词等 engine_options 沿用源模板缺省,后续可编辑(本批不做逐源编辑器,除非 grill 判定必要)。

### R3 生效链路

- 配置变更后 watcher 生效:方案阶段核实 web_host 是否支持增量加减 watcher 页;
  - 可增量 → 变更即生效(增群=新 Watcher 页,取消=关页);
  - 不可增量 → 提供「重启监控」操作(重启 sidecar serve)并在 UI 如实标注生效时机。

### R4 边界

- bot 线(Bot API 占位,chat_id 未实填零请求)与 Telethon 线不动;
- 1 级类型卡瀑布流 / 3 级渠道详情不动(3 级 TG 详情的监控台/原生视图保留);
- 多账号帽(max_accounts=3,源级可调)如实呈现,超帽拒绝并说明;
- 登录态:每账号扫码一次(browser 模块 headed 窗),登录态持久;TG 新设备登录安全提醒词面如实(既有披露复用)。

## 验收标准(初稿,实施前经 grill 拷问修订)

- [x] AC1 2 级 Telegram 页有账号与监控群管理区:账号登录态/添加/重登/删除可用(与设置页同源)。
- [x] AC2 每账号可添加监控群(写 yaml 带校验)与取消监控(删源),yaml 落盘正确、写坏回滚不落盘。
- [x] AC3 配置变更后 watcher 生效(增量重载或重启链路,方案定稿),新群消息入库进情报流。
- [x] AC4 账号删除联动清理其 sources(带确认,防误删)。
- [x] AC5 深度测试(检查员代码级+验收员动线截图:添加账号/加群/取消监控/重启后持久)+ 门禁全绿 + 换装覆盖安装。

## 边界与不做

- bot 线(Bot API)与 Telethon 线不纳入本管理区(如实呈现为不可用/未配置态);
- 不做逐源关键词编辑器(沿用源模板缺省;grill 判定必要再升级);
- 不动 1 级类型卡瀑布流与 3 级渠道详情的既有能力。

## 开放问题(实施前 grill 拷问)

1. watcher 增量加减:web_host 改造成本 vs 重启链路,计划阶段实测;
2. 群发现:web_dom 侧栏枚举可行性(能枚举 = 勾选式体验,不能 = 手填);
3. yaml 写入通道:复用配置编辑屏 yaml.save 还是新增 sidecar 方法;
4. 账号删除时其 sources 的处置(联动删 or 保留为孤儿源如实标注)。

## v2 修正(2026-10-10/11,主人纠偏「消息、情报流这块都需要这个 TG 账号」)

主人定调:**TG 账号是跨屏共享底座,不是情报流一家的配置**。账号管理唯一管理面 = 设置 → Telegram 监控(已建,多账号增删/重登);情报流与消息推送都是消费方:

- 情报流(监控):账号登录态 → watcher 观察群 → 消息入库;
- 消息(推送):TG 高价值即时/日报推送复用同一账号与分拣产物;
- 账号状态一处管理(setup 页),两屏只读消费 + 快捷跳转,不建第二管理面。

AC1-AC5 已全勾(2026-10-11 凌晨交付,ee687ea 前后链路):
- [x] 2 级 Telegram 页 = 账号与监控群管理区(多账号行/登录态/添加/重登/删除,与设置页同源);
- [x] 每账号可添加监控群(写 yaml 带校验)与取消监控(删源),yaml 落盘正确、写坏回滚不落盘;
- [x] 配置变更后 watcher 生效(增量重载或重启链路),新群消息入库进情报流;
- [x] 账号删除联动清理其 sources(带确认,防误删);
- [x] 深度测试(检查员代码级+验收员动线截图)+ 门禁全绿 + 换装覆盖安装。

## v3 追加(2026-10-11,主人令「clash-party 停订,改监控 clashv8,抓返回 URL」)

- [x] telegram-web.yaml 换源:停 Clash-Party(-2349572233,注释可回切),挂 clashv8(标题包含「免费VPN」;粗筛词面向订阅/URL:订阅/链接/节点/机场/http/https/url/URL/免费);存量 20 条回填 category=telegram(库备份 .bak)。
- [x] 3 级 TG 气泡正文 URL 链接化(urlSegmentsOf 纯函数 + URL 段可点浏览器直开):clashv8 返回的订阅 URL 一点即开。
- [x] 遗留 CLI telegram serve(pid 1187,旧代码写者+长轮询占位)清理。
- [x] 换装(含链接化)+ app 还原;alt1 会话登出待重登(哨兵告警 tg_web_logged_out,重登后 clashv8 监控即活)。

## v3 追加(2026-10-11,主人令「需要有一个账号模块,因为以后会有多个账号的」)

**核心设计定调:账号模块 = 一等公民实体。**

- 模块边界:网页线(C 线 tg_web)TG 账号池的唯一管理面,载体 = 设置 · Telegram 监控卡(已建成,多账号增删/重登/登录态全通);情报流 2 级与消息推送都是消费方,不建第二管理面。
- 模块能力清单:
  - 账号生命周期:添加(键名→headed 扫码)/重登/删除(配置档+联动清理);
  - 登录态:每账号独立(Playwright persistent 配置档,持久),状态●/○ 实时;
  - 每账号监控群:联合 telegram-web.yaml sources(按 account 归属),勾选/取消即改即生效(生效链路见开放问题);
- 消费方契约(单一事实源 = sidecar telegram.status + yaml):
  - 情报流 2 级:账号选择 → 该账号监控群列表 → 渠道详情;
  - 消息推送:TG 高价值即时/日报复用同账号与分拣产物;
  - 3 级原生视图:/k/ 深链按账号会话直达频道。
- 扩展预留:今后新渠道类型(微信/飞书…)进同一「账号模块」框架(类型徽标区分),不另起炉灶。

## v10 追加(2026-10-10/11,主人令「单独放到配置逻辑下面,这个 yaml 配置模块改名为 YAML配置,都放到配置逻辑下面,现在有采集,推送,再加个配置」)

侧栏信息架构重排(与并行会话的 yaml-editor「打开位置」功能共存,重构避让其活跃文件):

- [x] AC33 侧栏新增「配置」分组(位于 推送 之后、设置 之前):YAML配置(原配置编辑更名,route /yaml-editor 不变)+ TG账号(新路由 /tg-account,Telegram 监控卡+三线状态从设置屏抽为独立屏);采集组移除配置编辑。
- [x] AC34 设置屏移除 Telegram 分区(分区导航/搜索词表同步);feed 3 级监控台「管理」钮改指 /tg-account。
- [x] AC35 测试随动(sidebar 组/settings 抽除断言/新屏冒烟)+ 换装双实锤 + 入库。

### v10 终局注记(2026-10-11,工作流 dwfrun-0b40c399 五段交付)

- 交付 commit 94787ee(feat(desktop),10 files +118/−40;telegram-card.test.tsx→tg-account-screen.test.tsx 91% 重命名随迁;telegram-card.tsx 组件留在 settings/ 由新屏跨屏 import)。
- 门禁:build + feed/settings/layout 三路 vitest exit=0(相关四文件 94/94)。
- 换人深检 5 条 P2 全部留存待点单(工作流口径 P2 酌情,均不阻塞):
  - F1 ⌘K 命令面板未随「八屏→九屏」同步:/tg-account 无命令入口,/yaml-editor 在面板仍标旧名「配置编辑」;command-palette.test.tsx:153-165 toEqual 精确钉 8 项,缺口测试抓不住(command-palette.tsx:49-59);
  - F2 「配置编辑」→「YAML配置」更名只落侧栏与屏题,settings-screen.tsx(378/394/397/1384/1731)、settings/api.ts:104、messaging-screen.tsx(533/623)、cron-screen.tsx:638、sources 两处等十余处用户可见文案仍指旧名;App.tsx:27/30 注释失真;
  - F3 /tg-account 路由接线零测试(App.tsx:56 新行无用例触达;仓内先例 cron-screen.test.tsx:249-266 挂 <App/> 断言可达未循);
  - F4 feed 3 级监控台「管理」钮换靶(/settings?section=telegram → /tg-account,feed-screen.tsx:3823-3831)零断言;
  - F5 侧栏「配置」组仅数据面断言(NAV_GROUPS/resolveNav),无 DOM 渲染锚(renderSidebar 断言组标题与两条 NavLink);resolveNav 生产代码零消费者。
- 验收:换人验收员 headless 四动线截图通过(侧栏三组/YAML配置屏/TG账号屏/设置屏无 Telegram 分区)。
- 换装:新 chunk index-CSSPkkY9 双实锤(新包命中 1、旧装 0→换装后 1);WKWebView 缓存已清;osascript 温和退净后 ditto 换装,app 后台还常驻(PID 73747,无抢焦)。
- 遗留:真实数据装机像素截图待主人点亮 app 终验;alt1 会话重登(v3 遗留,哨兵告警在案)。
