# implement.md — 10-08-tg-web-line 执行计划(先档后行,批间门禁)

## W1 登录器与配置档
persistent context 启停/账号键目录/权限收紧/web-login CLI(mock 测试)→ 门禁+提交①
## W2 引擎 tg_web
schema 两行+registry+批量档开页读取+update 同形复用(mock)→ 提交②
## W3 常驻 Watcher 与哨兵
serve 集成(每键 context)/MutationObserver 注入/登出+DOM 失配哨兵/多键隔离+max_accounts → 提交③
## W4 设置页账号列表卡
Telegram 总卡升级(bot/session/web 三段+账号列表+添加/重登/删除)/vitest+无头冒烟 → 提交④
## W5 装机与真跑
外科+重签+拉起;真登录一次(mihomo 群)→ 消息进管线出口回执;AC 勾选;三段回填 → 提交⑤

停点:W5 真登录需主人手机号+验证码一次(页面内);其余零前置。

## 首真跑终局批(2026-10-08 晚,主会话直做)
真登录(CLI 拉窗+主人输码,17:51:50 落档)→ 首活登录态暴露两根因(登录态瞬态误杀=稳态探测件修;开群交互链全灭=受信点击契约重构)→ 活 DOM 标定(Clash-Party channel,data-peer-id 形态)→ e2e 真跑回执(20 条真读/13 条目入库/20 锚/push ok)→ serve 双形态验证(web 单线+bot+web 合体)→ sidecar 并入装配补(专用件 tg_web 源进 app 内 web 线)→ 装机外科②(7 件对拍+重签)→ 门禁全量 4982 过 → 提交⑥

遗留(非本档):常驻期实时新消息捕获留生产期首条自证;讨论群加入(主人)+bot 线 G8 chat_id(主人)两可选。
