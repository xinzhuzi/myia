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

- [ ] AC1 2 级 Telegram 页有账号与监控群管理区:账号登录态/添加/重登/删除可用(与设置页同源)。
- [ ] AC2 每账号可添加监控群(写 yaml 带校验)与取消监控(删源),yaml 落盘正确、写坏回滚不落盘。
- [ ] AC3 配置变更后 watcher 生效(增量重载或重启链路,方案定稿),新群消息入库进情报流。
- [ ] AC4 账号删除联动清理其 sources(带确认,防误删)。
- [ ] AC5 深度测试(检查员代码级+验收员动线截图:添加账号/加群/取消监控/重启后持久)+ 门禁全绿 + 换装覆盖安装。

## 边界与不做

- bot 线(Bot API)与 Telethon 线不纳入本管理区(如实呈现为不可用/未配置态);
- 不做逐源关键词编辑器(沿用源模板缺省;grill 判定必要再升级);
- 不动 1 级类型卡瀑布流与 3 级渠道详情的既有能力。

## 开放问题(实施前 grill 拷问)

1. watcher 增量加减:web_host 改造成本 vs 重启链路,计划阶段实测;
2. 群发现:web_dom 侧栏枚举可行性(能枚举 = 勾选式体验,不能 = 手填);
3. yaml 写入通道:复用配置编辑屏 yaml.save 还是新增 sidecar 方法;
4. 账号删除时其 sources 的处置(联动删 or 保留为孤儿源如实标注)。
