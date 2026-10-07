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
