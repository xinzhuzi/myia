# PRD — 10-08-tg-web-line:TG 网页会话线(自管无头浏览器)

> 立档:2026-10-08 02:30 · 来源:主人批 C 线方向(「网页登录,然后抓取」「本项目可以做到?」→ 确认)· 三段纪律:开始/过程/结果

## 开始段(设计与决议)

### 背景链
B 线(Telethon)代码全就绪但卡 api_id:my.telegram.org 裸 ERROR→限流,兜底凭据 2040 对被服务端拒(ApiIdInvalidError 实证);bot 线卡群权限(chat_admin_required)。C 线=零外部凭据、零群权限的桥。

### 方案(照主人确认的原理)
1. MYIA 自管 Chromium(Playwright persistent context;数据根 telegram-web/ 配置档 0600;chromium 复用 crawl4ai 组件轨既有下载,零新增重依赖);
2. `myssia telegram web-login`:首次 headed 弹窗开 web.telegram.org,用户输手机号+验证码一次,登录态存配置档;之后无头常驻;
3. 监听器读群消息 DOM(新消息节点)→ telethon_message_to_update 同形 update → **全复用 bot 线分拣/过滤(LLM 精筛)/合并单条出口/幂等锚**;
4. 新源类型 `engine: tg_web`(schema 词表两行 hunk 判例),YAML 一行一群;哨兵判例:DOM 选择器失效→结构化告警不装死。

### 登录 UX 放哪(主人问「哪个模块里让用户登录比较好」——决议)
**设置页「Telegram 监控」组件卡**(把 B4 的 telethon 组件卡升级为 Telegram 总卡):
- 卡面三态行:bot token(已录=绿)/ 用户 session(Telethon)/ **网页登录(按钮:未登录=「登录网页版」,已登录=绿色+「重新登录」)**;
- 点击→MYIA 拉起登录窗(带进度与「验证码在你手机 TG 里」指引)→引擎检测登录成功→卡面翻绿;
- 理由:组件卡是「状态+动作+修复」的既有聚合位(Python 环境卡判例:状态/开始配置/重新安装);凭据区(推送)语义不合(这是采集不是推送);源管理屏是健康视图非操作位;CLI `web-login` 并行保留(服务器场景)。

### 诚实披露(档内钉死)
DOM 改版跟修(哨兵在)/ToS 灰色同 userbot,登录**建议小号**/api_id 到手切回 Telethon 正统线,本线退役或备份/登录态=配置档文件(0600,非加密,同 session 判例口径)。

## AC
- [ ] AC1 web-login 一次登录成功→无头常驻读到目标群新消息→过管线出口(真跑回执);
- [ ] AC2 组件卡三态+登录按钮,点击拉起登录窗,登录成功卡面翻绿(vitest+无头冒烟,禁屏控);
- [ ] AC3 engine: tg_web 源装载+消息→条目(锚幂等)+哨兵(DOM 失效结构化告警)全 mock 测试;
- [ ] AC4 装机外科+重签+open -g 拉起+心跳;
- [ ] AC5 档三段回填;披露三条在设置卡文案可见(建议小号)。

## 过程(执行流水,随批回填)
- [x] 部件:Playwright persistent 登录器(W1 批①,2026-10-08):`src/myssia/telegram/web_line.py`(账号键全称律校验/配置档 `<数据根>/telegram-web/<键>/` 0700+内件 0600 硬化/登录标记复用/`TelegramWebLoginFlow` headed 流 + `_wait_for_login` 轮询会话列表/无头探针 `check_logged_in`/`launch_persistent_context` 工厂含 `ensure_playwright_browsers_env` 同源注入 + playwright 惰性依赖门 `myssia[crawl4ai]` 组件轨)+ `src/myssia/telegram/web_dom.py`(选择器表标定件 v1 `2026-10-08.v1`:登录/登出/消息列/文本/发送者/时间戳/媒体七面多候选;MutationObserver 安装/清空/单条抽取/窗口读取四 JS 注入件;`dom_message_to_update` → Bot API update 同形,`#tg-` 锚直进 bot 线 `updates_to_items` 铁证在测)+ CLI `myssia telegram web-login --account <键> [--force]`(`cli.py` `_cmd_telegram_web_login`);DOM 监听器本体在 W3 宿主批。测试 `tests/telegram/test_web_line.py` 29 例全绿(键校验/权限/复用/force/超时结构化/依赖门/DOM 映射进 bot 线管线/JS 件形态),ruff 绿。
- [ ] 引擎 tg_web+schema+registry(待填)
- [ ] 组件卡 UI+装配(待填)
- [ ] 测试/门禁(待填)
- [ ] 装机/真跑(待填)

## 结果(验收回执,完工填)
- [ ] AC 逐条勾+证据(待填)

> 决议追加(主人问「多个账号登录,你能把控吗」):**多账号为一等能力**——①每账号独立 Playwright 配置档(数据根 telegram-web/<账号键>/,0600,cookie/登录态零共享);②每账号独立无头实例,源 YAML 以 account: 键声明归属(A 账号读群1/2,B 账号读群3);③组件卡账号列表化(每行状态灯+重登按钮+「+添加账号」);④失效隔离(单账号掉线仅其源受累,其他不牵连);⑤资源披露(每实例 ~150-300MB 内存,并发帽可配,建议≤3);⑥风控披露(同机同出口多账号可被 TG 关联,只读监控风险低,数量克制);⑦账号键命名规约同全称律:telegram-<标识>。Telethon 线 session 分文件、bot 线分键(F8 修复)同理多账号。
