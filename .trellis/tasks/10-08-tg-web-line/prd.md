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
- [x] 引擎 tg_web(W2 批②,2026-10-08):`src/myssia/engines/tg_web.py`(批量档窗口引擎:配置档缺=`session_missing` 显式空态零浏览器/playwright 依赖门/登录态探针→`tg_web_logged_out` 与 `tg_web_dom_stale` 两哨兵结构化/开群失败分词表 `tg_web_chat_not_found`/窗口读取→`updates_to_items` bot 线全语义/过滤面 `TelegramFilterPipeline` 同一份且 tg_web 源过滤键与 bot 线 `engine_options.telegram` 兼容并集/单轮窗口拒 pagination/robots 豁免钉 web.telegram.org 授权第一方面,合规面走 PRD 披露)+ schema 两行 hunk(`ENGINES` 元组+`EngineName` Literal)+ registry 注册(链外判例,AUTO_CHAIN 七层原样)+ docs zh/en schema.md 词表行同步;测试 `tests/engines/test_tg_web_engine.py` 21 例全绿(注册表/词表/配置错误 7 形/显式空态/依赖门/登出哨兵/DOM 失配哨兵/开群失败 3 形/锚+粗筛复用/安静群合法空态),连带 schema+registry+docs 回归 339 全绿,ruff 绿。
- [x] 常驻 Watcher 与哨兵(W3 批③,2026-10-08):`src/myssia/telegram/web_host.py`(`TelegramWebWatcher` 每(账号×群)一页:page.evaluate 注入 MutationObserver→页内事件队列→轮询取走→单条抽取→`dom_message_to_update`→bot 线 `dispatch_once` 全语义复用(分拣/过滤/出口/账本/F13 媒体组记忆);`TelegramWebAccountHost` 每键一无头 context 多 Watcher 页,启动序=配置档门→依赖门→登录探针→开群挂 Watcher;`TelegramWebManager` 多键并跑+失效隔离(单键 fatal=记哨兵告警停该键不复活不退出,重启全量拉起由人)+`max_accounts` 帽缺省 3 源级可调+超帽结构化拒带 150-300MB/键资源披露+分键账本 `web-events-<sha8(tg-web:键)>.db`;哨兵两词表 `tg_web_logged_out`/`tg_web_dom_stale` 观察器安装失败/健康巡检 60s 双触发面,内存态+日志+账本 error 行三面留痕)+ serve 集成(cli.py `_cmd_telegram_serve` 引擎门收 tg_web 源+`_assemble_telegram_web_line` 第三线+`_run_telegram_hosts` 三线 gather;desktop/entry.py `_assemble_telegram_host` 同门逐句对齐,web manager close 收尾双面)。测试 `tests/telegram/test_web_host.py` 17 例全绿(Watcher 分派/哨兵×3/多键隔离/未知异常告警/装配分组+分键账本/帽拒+可调/CLI 第三线路由+web-login 在册),telegram+desktop+cli 646 全绿,ruff 绿;detect-changes 低风险(cli.py/entry.py 符号面与预期一致)。
- [x] 组件卡 UI+装配+测试(W4 批④,2026-10-08):sidecar 三方法(desktop/entry.py `telegram.status` 三线快照/`telegram.web.login` 后台 daemon 线程拉起 headed 登录窗,手机号+验证码全在页面内 sidecar 零读取零落日志/`telegram.web.delete` 整档删除;`_resolve_credential_probe` 注入缝;注册表 68→71 行,sidecar-protocol.md 三行同步对账测试过)+ 前端三件(`telegram-api.ts` IPC 封装/`telegram-card.tsx` Telegram 总卡:bot 段 token 状态灯+四步指引、session 段 telethon 首登态、web 段账号列表行(键+状态灯+重登 force+删除)+「+添加账号」键名校验前置+登录窗 5s×24 轮询对账+披露三条文案常驻 AC5;settings-screen 新分区「Telegram 监控」+SECTION_FIELD_TERMS 词面+渲染接线)。测试:vitest `telegram-card.test.tsx` 10 例全绿(全量 608/608,tsc -b 0 错,无 jest-dom 原生断言口径);无头 Playwright 冒烟 `desktop/scripts/tg-card-smoke.py`(vite build 产物+静态服务+`__TAURI_INTERNALS__.invoke` 注入夹具,程序化断言 9 项:三段/账号行/披露/添加动作链+busy/删除动作链,截图 /tmp/myssia-tg-card-smoke.png;chromium 二进制=playwright 缺省缓存与组件轨同源);desktop 协议测试 +4 例(状态三线/bot 未配空态/键校验+线程启动/删除),python 671 全绿 ruff 绿。
- [x] 装机/真跑+门禁(W5 批⑤,2026-10-08):
  - **W5 真跑标定与修复**:真开 web.telegram.org(无头沙箱配置档)标定选择器表——两处硬发现:①Web K 登录页隐藏壳里 `.chatlist-container` 也在 DOM(纯在场判据会假阳性「已登录」)→ 判据改**可见性口径**(`getClientRects`)+ 登出标志改 `body.has-auth-pages` 类,新共享探测件 `web_dom.login_state_probe_js`(登录流/引擎/宿主/哨兵同一份,四处消费面统一改接);②`launch_persistent_context` 原返 PlaywrightContextManager(只有 start 无 stop)→ 改返 `start()` 产物(Playwright 实例带 stop),修真跑收尾 AttributeError(node 进程泄漏面);连带 skill/SKILL.md 枚举表同步(词表对账测试红→补→绿)。真跑三证(全无头):探针 12 轮全 `logged_out`(真实登出态识别);引擎真网络 fetch 配置档缺=`session_missing` 显式空态零浏览器;配置档在但登出=`tg_web_logged_out` 结构化拒绝带重登指引零装死。**主人紧急纠偏令(03:1x):停止一切 GUI 弹出**——真登录窗拉起留主人(两条路径见结果段),本批零弹窗零 open,已在跑实例直接复用。
  - **装机外科**(零拉起口径):`npm run build`+`npx tauri build` exit 0(世事.app 20.24MiB+DMG 0.0.3);新包 sha256 对拍 **8/8 MATCH**(web_line/web_dom/web_host/tg_web.py/entry.py/cli.py/schema.py/registry.py);UI 卡件实证在包(index-*.js 含 telegram-web-account);备份 `/tmp/myssia-tgweb-backup-20261008-031523` 后 ditto 换装 /Applications/世事.app;`codesign --force --deep -s -`+`-vv` 双过+strict verify exit 0;装机 python 直载冒烟过(web 三件+引擎+registry+schema+entry 71 handlers 全命中);心跳双验复用**已在跑实例**(pid 91929/写者戳 …-91934,mtime 03:15:21→03:16:21 精确 +60s)——按纠偏令零拉起(查漏侦察员 03:17 所记 G6「装机包落后」扫描窗在换装前,本 swap 后已解);新代码待主人下次重启 app 生效。
  - **终局门禁**:全量 pytest **5030 passed/40 skipped/0 failed**;vitest **608/608**(29 文件);`tsc -b` 0 错;ruff 全绿。
- [x] 查漏修复批①(G1+G2,2026-10-08 补缺工程师,小步两缺口;批初登记撞 W5 收尾窗——prd.md 被 W5 持有,动码先行、W5 提交(11646cc)后补记如实):
  - **G1 死兜底对移除**:`telethon_line.py` 常量 `DEFAULT_FALLBACK_API_ID/HASH`(2040 对)+ login 回落路径(`run()` 的 try/except 兜底段)+ `used_default_creds` 成功回执披露段 + module/class docstring 共六处清除;凭据缺=结构化失败 `api_credentials_missing`(原语义保留)且 guidance 增强「站点不可达等恢复/换出口网络再取自有对,勿用网上流传的文档示例对(已被服务端拒)」人话出路;`assemble_user_host` 未首登 note 与 `engines/telegram.py` 空态日志两处指引文案同步去兜底化。测试改形:`test_login_zero_credential_falls_back_to_documented_pair` → `test_login_zero_credential_structured_failure`(零交互零客户端构造/fatal/指引在场/2040+b18441a1 零残留),CLI 烟测断言面改「凭据指引在场+示例对零残留」(凭据解析先于依赖门,`myssia[telethon]` 安装指引断言随之撤),invalid 用例与 :497 注释同步。10-06 prd.md B4 决议段追加**失效注记**(实证链=本档查漏节 G1),:77 AC2 真发指引同步改「先取自有对」。
  - **G2 telethon extras 增 python-socks** 三处固化+把守测试:pyproject extras `python-socks>=1.2.4,<3`(注释含理由);`uv lock` 解析钉 **2.8.2**(diff 恰 11 行纯增零漂移);桌面锁 `uv export --frozen --no-dev --no-emit-project --no-hashes --extra llm --extra telethon` 重导出+头注释 4 轮→5 轮+G2 批注+classifier 行手改回 PyPI 版(diff vs 备份实证:增量恰 `python-socks==2.8.2` 一轮既有零漂移);`test_pyenv_resources.py` 把守两例改形(组件窗仍钉主件,extras 双件逐件对锁钉版约束,companions 断言面不变)+ `components.json` telethon 行 description 补 python-socks(单行文本替换,json.dump 整写曾重排 searxng start_cmd 已还原弃用)。装机包内同件未动(G6/G7 装机同步归 W5/主人,建议 G2 合流后一次同步——查漏节原建议)。
  - 门禁:定向 `pytest tests/telegram/ tests/engines/test_telegram_engine.py tests/desktop/` **504 passed 0 failed**(含 test_telethon_line 32+engine 35+pyenv_resources 31);ruff check 四件全绿(format 非门禁:HEAD 两件本就非 format 干净,文件模式亲证,stdin 模式假阴性坑);`git commit --only` 定向两提交,W5 已交件零接触。

## 结果(验收回执,完工填)
- [~] **AC1** web-login 一次登录→无头常驻读群→管线出口:**代码面全就绪,真登录锁主人一次验证码**——登录器/引擎/常驻 Watcher 全 mock+真网络无头双验(真实登出态识别/显式空态/结构化拒绝);无头常驻读到消息→出口的全链路在 mock 测试铁证(`test_web_host.py` Watcher 分派→`#tg-` 锚入库;`test_tg_web_engine.py` 锚+粗筛复用),真登录后的真发回执留主人登录同窗(路径见下)。
- [x] **AC2** 组件卡三态+登录按钮:W4 已交——bot/session/web 三段+账号列表(状态灯/重登/删除/+添加),vitest 10 例+无头 Playwright 冒烟 9 断言全绿(截图 /tmp/myssia-tg-card-smoke.png;登录窗拉起动作 = 主人点击,sidecar 后台线程+5s 轮询翻绿逻辑在测)。
- [x] **AC3** engine: tg_web 装载+锚幂等+哨兵:W2/W3 已交——21+17 例全 mock(session_missing 空态/`tg_web_logged_out`/`tg_web_dom_stale` 结构化/锚 `#tg-<chat>-<mid>` 进 bot 线 `updates_to_items` 铁证/多键隔离/max_accounts 帽)。
- [~] **AC4** 装机外科+重签+心跳:**已做**(8/8 sha 对拍+ditto 换装+adhoc 重签 strict verify 过+装机 python 直载冒烟+心跳 +60s 双验);`open -g` 拉起按主人紧急纠偏令(03:1x「停止一切 GUI 弹出」)**未执行**——复用已在跑实例(pid 91929)零拉起,新代码待主人下次重启生效。
- [x] **AC5** 档三段回填+披露三条卡面可见:开始/过程/结果三段齐;披露三条(DOM 跟修哨兵/建议小号/api_id 到手切正统)+登录态非加密注记在 `telegram-card.tsx` 常驻文案,vitest 断言在案。

### 主人下一步:真登录(差的那一次验证码)

**路径一(推荐,图形面)**:重启世事.app(新代码生效)→ 设置 → 「Telegram 监控」分区 → 「添加账号」:键名填 `telegram-alt1`(规约 `telegram-<标识>`,小写)→ 点「添加账号」→ 弹出的浏览器窗口里输手机号 → 验证码(TG 发你手机 App 内信或短信;如有两步验证再输密码)→ 卡面行转绿即成。之后把 mihomo 群源写成品类 YAML(engine: tg_web,见 design D4)或等 W5 真发批,`myssia telegram serve` 的 web 线无头常驻读群。

**路径二(终端,服务器场景同款)**:
```bash
cd /Users/zhengbingjin/Project/Github/MYIA
MYIA_HOME="$HOME/Library/Application Support/MYIA" .venv/bin/python -m myssia.cli \
  telegram web-login --account telegram-alt1        # 弹浏览器登录窗(手机号+验证码在页面内输)
# 失效重登加 --force;登录态落 ~/Library/Application Support/MYIA/telegram-web/telegram-alt1/(0600)
```
两条路径同一配置档(数据根 `telegram-web/<键>/`);登录后账号行/CLI 复用提示都会翻绿。

> 决议追加(主人问「多个账号登录,你能把控吗」):**多账号为一等能力**——①每账号独立 Playwright 配置档(数据根 telegram-web/<账号键>/,0600,cookie/登录态零共享);②每账号独立无头实例,源 YAML 以 account: 键声明归属(A 账号读群1/2,B 账号读群3);③组件卡账号列表化(每行状态灯+重登按钮+「+添加账号」);④失效隔离(单账号掉线仅其源受累,其他不牵连);⑤资源披露(每实例 ~150-300MB 内存,并发帽可配,建议≤3);⑥风控披露(同机同出口多账号可被 TG 关联,只读监控风险低,数量克制);⑦账号键命名规约同全称律:telegram-<标识>。Telethon 线 session 分文件、bot 线分键(F8 修复)同理多账号。

## 查漏(2026-10-08 03:17,查漏侦察员;基线=HEAD 49ab005[W4 已交]+W5 在途脏工作树)

**方法与证据**:全部结论来自本窗亲跑(rg/fd/wc/shasum/ls/pytest/importlib.metadata,逐条注脚);两档 AC 对照以两 PRD 原文为准;装机面以 `/Applications/世事.app/Contents/Resources` 与数据根 `~/Library/Application Support/MYIA/` 实物为据;session 文件只报位置/形状/大小,内容零读取。

### 在途界定(本节不计缺口,只钉边界)

- **W5 在途(批⑤,扫描窗内活跃写)**:工作树脏 7 件 mtime 03:08-03:12(git status 亲取)——`src/myssia/telegram/web_line.py`/`web_dom.py`(docstring 已见「W5 真跑标定口径」)/`web_host.py`、`src/myssia/engines/tg_web.py` + 三测试件;另 `desktop/entry.py`、`desktop/ui-src/src/screens/settings/`(settings-screen.tsx/telegram-api.ts/telegram-card.tsx/telegram-card.test.tsx)、`desktop/scripts/tg-card-smoke.py`、`tests/desktop/test_desktop_sidecar_protocol.py`、`.trellis/spec/desktop/sidecar-protocol.md`。
- **测试面如实注记**:本窗首两轮 pytest 亲见红(三件套 5 failed / tests/telegram 2 failed),跑窗与上述并行写入窗重叠=在途中间态(判例同 10-06 档 19:23/20:29 先例);在途定稿后同命令 **10 连绿**(三件套 189/189×5、tests/telegram 133/133×5;`tests/engines/test_tg_web_engine.py` 单独 21 passed、`tests/engines/test_telegram_engine.py` 35 passed)。非代码红,不入 GapList。

### AC vs 现状速照(详证在各档,此处只对账)

- **本档**:AC1-5 全未勾;W1-W4 已交(bac74e9/e53dc64/26b4cb7/49ab005),AC1/AC4 后半/AC5=W5 装机真跑批承载(在途)。
- **10-06-telegram-telethon**:AC1 真发回执缺(→G8 chat_id 占位);AC2 真登缺(→G1 死兜底对+G3 半成品 session+G7 装机未同步,三缺连锁);AC3 阶段三未开工(→G11);AC4 已勾在案;AC5 代码/测试面在案,真跑验收留 AC1 同窗。

### GapList(fixable=false 注归属)

| id | 缺口 | 面 | 严重度 | fixable | 证据与修法 |
|---|---|---|---|---|---|
| G1 | **死兜底对仍在产线**(ApiIdInvalidError 实证,主人令修) | 源码 | high | ✅ | 常量 `src/myssia/telegram/telethon_line.py:86-87`+登录回落使用 `:446-448`+指引文案两处(`telethon_line.py:368`、`engines/telegram.py:436`)+PRD 决议记录(10-06 prd.md B4「零凭据兜底」段)+测试四引用(`tests/telegram/test_telethon_line.py:497/502/585/760`)。**推荐修法:移除常量与回落路径**,api 凭据缺=结构化失败带人话指引(my.telegram.org 恢复/换出口再取自有对;文档示例对 2040 已被服务端拒,不可用);PRD 决议追加失效注记同批 |
| G2 | **telethon extras 缺 python-socks**(主人手装过,须 extras+lock 固化) | 依赖 | high | ✅ | `pyproject.toml:81` extras 仅 `telethon>=1.36,<2`;uv.lock 全文无 python-socks(rg `name = "python-socks"` 0 命中;telethon 1.45.0 依赖仅 pyaes/rsa,uv.lock:4068-4072,非传递可覆盖);桌面锁 `desktop/resources/requirements-lock.txt` 同缺(装机包内件亲读:telethon==1.45.0 在、python-socks 无)。修=extras 增 `python-socks`+`uv lock`+桌面锁 `uv export --extra llm --extra telethon` 重导出(锁头注释「增量仅 4 轮」须同步)。手装位未定位:repo .venv 与装机 python(`<数据根>/python/bin/python3`)2026-10-08 亲测均 NOT-INSTALLED——固化后随锁走,不依赖手装 |
| G3 | **数据根 session 未授权半成品未处置**(设计二选一须落实) | 数据 | medium | ✅(清理动作) | `~/Library/Application Support/MYIA/telegram/telethon.session`(28672B,10-08 02:16 落盘;10-06 prd.md B4 装机段注记来历=主人真机 login 尝试,钥匙串无 api 对→兜底对→必拒)。连带代码面:login 零依赖复用检查 `telethon_line.py:450-457` 把「文件在」当「已登录」,半成品会得「直接复用」误导提示。**推荐处置:清理**(rm 该 session;--force 覆盖在真对到手前不可行);bot 线账本 events-69e1a1d5.db 保留不动 |
| G4 | **本档 jsonl 双空**(策展补) | 档案 | low | ✅ | check.jsonl/implement.jsonl 均 0 行(wc -l 亲测;对照 10-06 档 23+9 行,条目形 `{"file","reason"}`)。策展范围:W1-W4 批上下文(search-sop/security-baseline/yaml-schema 等 spec+本档 design D1-D6+web_line/web_dom/tg_web/web_host/桌面卡源与测试)+本查漏节自引 |
| G5 | **tauri 种子清单缺 telegram 三件 YAML** | 装机 | medium | ✅ | `desktop/src-tauri/tauri.conf.json:39-78` resources 枚举无 telegram-groups/telegram-channels/daily-digest → B4 批 `npx tauri build` 全新重生成 Resources 已把 B1 手拷件洗掉(装机包 Resources/plugins/ 亲 ls:三件+daily-digest 全缺席;数据根活件不受影响)。修=resources 补三行,净装机种子才齐、重打包不再丢 |
| G6 | 装机包整体落后 W1-W4(bundle 缺 web 三件/tg_web 引擎/cli 新版/schema+registry 词表) | 装机 | — | ❌ **在途代理(W5 装机批)** | 包内 telegram/ 仅 6 件(缺 web_line/web_dom/web_host)、engines/ 仅 telegram.py(缺 tg_web.py)、cli.py sha `eb14df8…`≠HEAD `71ef4c6…`、entry.py=B4 版。W5 外科+重签范畴,如实注记 |
| G7 | 装机自管 python 未吃 telethon 轮(用户线装机态死) | 装机 | medium | ❌ **主人**(一键动作) | `<数据根>/python/bin/python3` 亲测 telethon/pyaes/rsa/python-socks/playwright 全 NOT-INSTALLED(B4 留痕口径一致)。动作=设置页一键同步依赖+重启;**建议等 G2 合流后做**,一次吃到 python-socks,免二次同步 |
| G8 | chat_id 仍占位(仓库+数据根双占位;AC1 真发前置) | 配置 | medium | ❌ **主人**(实填真值) | 仓库 `plugins/telegram-groups.yaml:50` 与数据根件 `:47` 均 `"-1000000000000"`;B4 装机留痕 bot 线已起但群占位→消息全量 dropped_chat。动作=bot 已在群发条消息/@userinfobot 取真 id,仓库+数据根两处回填;AC1 真发回执同窗 |
| G9 | tg_web 无示范源 YAML(设计 D4 形态在、plugins/ 零例;W5 真跑前置) | 配置 | low | ✅ | design.md:19-28 已定形态(account/chat/lookback_limit);W5 mihomo 真跑需源件——W5 批顺带落或查漏修复批补(落件时决议是否进 daily-digest 分区) |
| G10 | pyproject `all` extra 未收纳 telethon(同缺 simplex/apprise/vision 件,既有滞后面) | 依赖 | low | ✅(可选) | `pyproject.toml:82`。顺 G2 一行同批或另批,非阻塞 |
| G11 | 10-06 阶段三「组件化件一例」未开工(AC3) | 范围 | low | ❌ **主人**(排期决策) | 10-06 prd.md:78「待填」;TrendRadar 拆解小档已独立在案(`.trellis/tasks/10-06-trendradar-scan/`),组件化本体(tgcf/RSSHub 轨)未动 |

### 无缺口面(核过即录)

- 源码面:schema/registry/docs zh+en 词表 `tg_web` 四处在案(schema.py:195/267、registry.py:160、docs zh/en schema.md:33/37);telegram 域零 TODO/FIXME;cli.py W3 面(web-login+第三线装配 4 处)在 HEAD;`telethon_line.py`/`engines/telegram.py`/`cli.py` 相对 HEAD 零 diff(git diff --stat 亲验)。
- 组件卡:`desktop/resources/components.json` telethon 行在且 repo↔装机包 sha 一致(`1fed38d5…`);UI 总卡=W4 已交(49ab005)。
- 数据根:daily-digest.yaml 两分区(频道 :102-105/群 :111-113)与仓库件同步;telegram-web/ 尚无配置档(W5 真登录前置,符合预期);tg_web 线零凭据设计,数据根无凭据落痕。
