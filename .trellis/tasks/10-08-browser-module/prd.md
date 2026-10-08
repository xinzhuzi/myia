# PRD — 10-08-browser-module:浏览器专用模块(内嵌界面)+登录流修复

> 立档:2026-10-08 · 来源:主人报障「没看到弹出的浏览器」+设计指令「工具里嵌入一个界面调浏览器操作,单独做个模块单独搞浏览器」· 三段纪律

## 开始段

### 修复面(先修再建)
1. **根因已实锤**:装机自管 python 缺 playwright/telethon(G7 遗留)→「添加账号」调起登录静默失败、零弹窗零错误——**临时解锁已做**(pip 三件直装,登录按钮当下即可用);**静默失败本身是反模式**,卡面必须上浮错误(toast/行内红字)。
2. 根治:desktop requirements-lock 扩 telethon+playwright extras(照 llm/telethon 判例重新导出+classifier 钉版保留)+依赖指纹链同步+设置页一键「同步依赖」吃进(告别人工 pip)。

### 浏览器专用模块(主人点名的形态)
**定位**:MYIA 内一个**独立浏览器模块**(设置树一级分区或独立窗口),专门承载一切浏览器操作——首役=tg_web 登录流,后续=任何需要「人看一眼网页」的场景(凭据授权/验证码/手动核验)。

**内嵌形态度量(design 档定案,两案)**:
- 案甲(推荐先落):**Tauri 子窗口承载 Playwright headed 登录**——模块点「登录」→壳拉起一个 MYIA 品牌的子窗口(非"外部浏览器"观感,标题/图标归 MYIA),内里就是持久化配置档的 Chromium;实现薄(壳窗口管理+复用现有登录器),登录体验=完整真浏览器(兼容性零妥协)。
- 案乙(后置增强):**CDP screencast 流式内嵌**——headless Chromium 画面流入 app 内嵌画布,键鼠回注;体验=真·应用内浏览器,工程量中(Playwright CDP Page.screencastFrame+输入注入),甲稳后升级。

**模块面**:浏览器操作页(当前任务列表:登录中/已完成/失败重试)+每操作的窗口管理(聚焦/关闭)+日志尾巴;禁屏控令豁免面=用户主动点击触发的窗口(交互性窗口非自动化屏控,与主人操作意图一致)。

## AC
- [~] AC1 登录流真通:设置页点「添加账号」→**MYIA 子窗口**弹出网页版 TG→手机号+验证码→卡面转绿(真跑回执;临时解锁后即可验);**工程面已齐**——「添加账号/重新登录」已改调浏览器模块统一入口 `browser.open`(单入口铁律),拉窗/轮询/转绿链路 vitest+无头冒烟钉死;装机自管 python 三件在位亲证(playwright/telethon/python_socks importable),**差主人一次真输验证码**(步骤见结果段「主人登录步骤」);
- [x] AC2 静默失败消灭:依赖缺失/浏览器缺失等一切失败在卡面上浮人话错误+修复指引(测试钉死:拔依赖→可见错误)——`browser.open` 同步依赖前置探针(缺装=点按钮立即可见 `dependency_missing` 人话+安装命令+深链「Python 环境」同步依赖);线程内失败三族(依赖缺/浏览器二进制缺 Executable doesn't exist/登录超时)人话化+`fix_hint` 修复指引,卡面与模块页双上浮(ErrorBox dependency_missing 变体+模块页失败行 alert/fix 区);pytest `test_browser_open_dependency_missing_visible_error`+vitest 拔依赖用例+冒烟失败行断言三面钉死;
- [x] AC3 根治链:lock 扩 extras+指纹链绿+一键同步吃到 playwright/telethon(判例判据)——pyproject `extras[browser]=playwright>=1.63,<2`(uv.lock diff 恰 13 行纯增零漂移);桌面锁 `uv export --extra llm --extra telethon --extra browser` 定向重导,diff 实证增量恰 3 轮(playwright==1.63.0/greenlet==3.5.6/pyee==13.0.1=临时解锁 pip 三件同源固化)既有零漂移+classifier 钉版保留;`test_browser_covered_by_desktop_lock` 逐件+闭包伴生件把守;指纹链绿=test_pyenv_e2e 全链随新锁跑通(安装戳 deps_fingerprint=新锁 sha256);telethon+python-socks 前批 G2 已在锁(本批复验在包);
- [x] AC4 浏览器模块独立分区落地(案甲)+操作列表/窗口管理(程序化验证:vitest+无头冒烟)——设置树「浏览器」一级分区+模块页(操作台账 running/done/failed/closed 四态行/失败重试/聚焦/关闭/环形日志尾巴 60 行容量投影 20);sidecar `browser.open/list/focus/close` 四方法(kind 登记词表拒旁路=单入口铁律的登记面);窗口=案甲 MYIA 自管 Chromium(复用 web_line 登录器零重写,`on_page_opened` 注入缝+停令可中断 sleep 两处加法);vitest 模块页 8 例+协议面 6 例+无头 Playwright 冒烟 13 断言全过;
- [x] AC5 三段回填+装机外科;案乙 screencast 留 design 待令。

## 过程(随批回填)
- [x] 临时解锁与根因档案(已做:pip 三件+探针,待填提交→已归 10-08-tg-web-line 查漏批 G7 在案)/ [x] AC2 错误上浮 / [x] AC3 lock 根治 / [x] AC4 模块甲 / [x] 装机与真跑(装机已做;真跑=主人输验证码,见结果段)
- **建设批(2026-10-08,提交 8467f3a+617c680)**:①案甲模块——`entry.py` browser.* 四方法+操作台账(op_id=会话键,一键一操作重登覆盖;线程内句柄 stop_event/page/loop 不外泄协议面);close=置停令→注入 sleep 抛 `_BrowserWindowClosed`→登录流 finally 关窗(零重写);focus=经登录线程事件循环 `run_coroutine_threadsafe(page.bring_to_front)`(Playwright async 对象只能在其归属循环上动);`telegram.web.login` **移除**(单入口铁律,PROTOCOL_VERSION 10→11——含移除的批次必须 bump,版本门=新旧壳/ UI 对齐唯一信号);`telegram.status` web 段改台账联读(卡面↔模块同源),`telegram.web.delete` 在跑侧拒指引去模块关窗。②web_line.py 两处加法注入缝(`on_page_opened`/既有 sleep),登录器本体零改动。③前端——设置树「浏览器」一级分区(空态提示行改 SECTIONS 动态派生)、`browser-module.tsx` 模块页、`browser-api.ts` 契约、telegram 卡改调 `browser.open`(回执文案带模块指引)、ErrorBox 增 `dependency_missing` 变体(人话+深链 python-env)。④AC3 锁链三件套(pyproject/uv.lock/桌面锁+把守测试)。⑤冒烟双脚本(browser-module-smoke 新建 13 断言;tg-card-smoke mock 面随接线改 browser.open)。⑥规范同步:sidecar-protocol.md 注册表 71→74 行+分组段记 v11 bump 理由。
- **装机外科(2026-10-08 13:45-13:57)**:`npm run build`+`npx tauri build` exit 0(世事.app 17.75MiB+DMG 0.0.3);sha 对拍 **4/4 MATCH**(entry.py/web_line.py/web_dom.py/requirements-lock.txt);UI 内嵌件 **7/7 锚点**(Mach-O brotli 解出 index-*.js 含 browser-module-card/browser-op-/browser.open/browser.list/tg_web_login/统一入口与台账/error-box-dependency-missing);备份 `/tmp/myssia-browser-backup-20261008-135103` 后 ditto 换装 /Applications/世事.app;`codesign --force --deep -s -`+`-vv` 双过+strict verify exit 0;装机 python 直载冒烟过(**74 handlers+browser 四方法在册+协议 v11+telegram.web.login 已移除**+包内锁含 playwright 三轮);装机自管 python 三件 importable 亲证(playwright/telethon/python_socks;G7 临时解锁存续,新锁固化后一键同步即钉版);心跳=**恰一次 `open -g`**(任务上限内):MYIA 52114+sidecar 52122 同存活、sidecar CPU 0:00.51→0:00.52 推进、`13:52:15 setup done(sidecar spawned)` 本次实例启动日志在册;osascript 礼貌退场双进程退净。
- 门禁:pytest 全量 **5044 passed/40 skipped/0 failed**;vitest **617/617**(30 文件);`tsc -b` 0 错;ruff 全绿;browser-module-smoke 13 断言+tg-card-smoke 9 断言全过(截图 /tmp/myssia-browser-module-smoke.png、/tmp/myssia-tg-card-smoke.png);detect-changes high=预期面(20 文件/61 符号/6 执行流全在 Telegram 卡改线+设置屏分区,无预期外漂移,已按纪律记录);`git commit --only` 两笔定向,不推远端。

## 结果(完工填)
- [~] **AC1** 工程链已通、差主人真跑(输验证码);**[x] AC2** 拔依赖→`dependency_missing` 同步可见(pytest+vitest+冒烟三面钉死);**[x] AC3** extras[browser] 入锁增量恰 3 轮零漂移+指纹链绿+把守测试在册;**[x] AC4** 模块独立分区+四方法+台账/窗口管理/日志尾巴(vitest 617 全量+无头冒烟 13 断言);**[x] AC5** 三段回填+装机外科(换装+重签+直载+心跳,恰一次 open -g)。案乙(CDP screencast 内嵌)留 design 待令。

### 主人登录步骤(路径一,推荐)
重启世事.app(已换装新代码)→ 设置 → 「Telegram 监控」分区 → 键名填 `telegram-alt1`(规约 `telegram-<标识>`,小写;已有同名配置档则直接点该行「重新登录」)→ 点「添加账号」→ 弹出的浏览器窗口里输手机号 → 验证码(TG 发你手机 App 内信或短信;如有两步验证再输密码)→ 卡面行转绿即成;窗口管理(聚焦/关闭)与操作台账在 设置 →「浏览器」分区;失效重登=行内「重新登录」(清档 force)。终端路径同 10-08-tg-web-line 路径二(`myssia telegram web-login --account telegram-alt1`),两路径同一配置档。

> 若点「添加账号」见到黄条「playwright 库未安装」:设置 →「Python 环境」→ 同步依赖(新锁已收录 playwright)即可;浏览器二进制缺失同理装「JS 渲染抓取(crawl4ai)」组件(含 Chromium)。

> 决议追加(主人令「这个功能就要调用起来专用浏览器模块」):**架构铁律——一切浏览器操作(tg_web 登录打头)必须经浏览器模块入口调用,禁止任何功能旁路直启 Chromium**。模块=浏览器操作的唯一治理位(窗口生命周期/账号配置档/错误上浮/操作审计集中);Telegram 卡的「添加/重登」按钮改为调用模块 API(模块负责拉窗+状态回报+卡面联动),其余未来浏览器需求(验证码/授权/核验)同律接入。
