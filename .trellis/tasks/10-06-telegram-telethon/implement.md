# implement.md — 10-06-telegram-telethon 执行计划(先档后行,批间门禁)

## 批次 B1:bot 批量引擎(无前置,可先动)——✅ 2026-10-06 完(提交①)
1. ✅ `src/myssia/engines/telegram.py`(engine: telegram,设计 D2 契约)+ schema 词表两行(ENGINES/EngineName,收窄 hunk 判例)+ registry 注册;
2. ✅ 测试 `tests/engines/test_telegram_engine.py`(D5 引擎面,31 例);
3. ✅ 品类示范件 `plugins/telegram-groups.yaml`(源名规约 telegram-<群名>;schema sources min_length=1 → 活源待 token 空态而非注释态,token 未配=credential_missing 零请求);
4. ✅ 门禁:定向 pytest(765 passed 含 engines/schema/docs)+ruff 绿;docs zh/en schema.md 词表行同步。

## 批次 B2:过滤管线与出口接线——✅ 2026-10-06 完(提交②)
1. ✅ 粗筛词表配置化(源级 engine_options.telegram.keywords > 内置缺省 DEFAULT_COARSE_KEYWORDS,口味配置化)+ LLM 精筛挂点(enrich OpenAICompatClient 复用,glm-4-flash,llm_base_url/llm_api_key 成对引用;未配=降级纯粗筛);
2. ✅ 出口:高价值即时**合并单条**(merge_high_value,组合铁律,锚随消息 id 区间幂等)/普通入库进合并日报(daily-digest 已增「Telegram 群」分区);
3. ✅ 测试:tests/telegram/test_telegram_filter.py 25 例(同轮恰 1 条端到端+引擎集成);门禁 681 passed+ruff 绿。

## 批次 B3:常驻宿主 telegram serve(每时每刻)——✅ 2026-10-06 完(提交③)
1. ✅ `src/myssia/telegram/`:serve.py(长轮询 25s/退避 1s→300s/401/409 致命上抛/sink 注入零 pipeline 依赖)+offsets.py(数据根 telegram/offsets.json 原子写断点续拉)+events.py(telegram_events 表 executions 形态,outcome 七词表);引擎共享面抽出(updates_to_items/message_to_item/filter_config_from_options 升模块级,两档同语义);
2. ✅ CLI `myssia telegram serve`(品类装配/单 bot 校验/推送+入库 sink/致命错误退码 1);桌面接线位=TelegramServeHost 可嵌入 sidecar(模块文档注明 _CRON_TICKER 先例形态;entry.py 由并行任务持有,方法实装留桌面批,如实记档);
3. ✅ 测试 tests/telegram/test_telegram_serve.py 21 例(全 mock:poller/宿主/退避/账本/CLI 装配);全套 4423 passed+desktop 288 passed;ruff 绿。

## 批次 B4:Telethon 线(主人小号+验证码到位后)——✅ 2026-10-08 代码面完(真登录留主人)
1. ✅ extras 组件轨双收录:pyproject extras `telethon = ["telethon>=1.36,<2"]`(uv.lock 增 telethon 1.45.0 + pyaes/pyasn1/rsa 纯 Python 闭包)+ 桌面锁 requirements-lock.txt 照 llm extras 判例扩 `--extra telethon` 重导出(classifier 钉版手改保留;diff 实证既有条目零漂移,增量恰 4 轮)+ 设置页组件卡照 crawl4ai 判例(components.json telethon 行 + pyenv-card.tsx COMPONENT_META;Rust 壳注册表动态读零改动;测试 test_pyenv_resources 1e 节两例把守 extras 同字串/锁收录/闭包伴生件);
2. ✅ session 首登 CLI 流:`myssia telegram login`(`src/myssia/telegram/telethon_line.py` TelethonLoginFlow,全注入零交互可测)——api_id/api_hash 钥匙串解析 → 手机号 → 验证码 →(2FA 密码不回显)→ session 落数据根 `telegram/telethon.session` 0600(-journal 伴生件同收紧);已有 session 直接复用提示(`--force` 删旧重登 = 失效重登路径);**零凭据兜底**(2026-10-08 主人令追加:my.telegram.org 持续裸 ERROR,实测 Telethon v1.x 已不内置默认对,v1.0-1.45 源码亲验 api_id 空即 ValueError,兜底用文档公开示例对 2040/b18441…,限速风险在回执如实披露;钥匙串配了永远走自有对);session 失效 = session_expired 结构化告警+`login --force` 重登指引(引擎/宿主/CLI 三面一致,不静默);
3. ✅ telethon 引擎+宿主接入:批量档 `engine_options.telegram.mode: user`(iter_messages 单轮窗口,#tg- 锚/媒体组聚合/过滤挂点与 bot 模式同一份;无确认请求;session 路径 MYIA_HOME 派生不入 YAML——「session」是 schema 凭据后缀词)+ serve 宿主 telethon 线(TelethonUserHost:事件监听 add_event_handler,serve.dispatch_once 复用 bot 线全部分派语义含 F13 跨批媒体组记忆(事件面升级为宿主持久记忆+FIFO 帽,三成员相册跨事件回归测试钉死)/F14 出口 bool;FloodWait 服从服务器秒数,transport 指数退避 1s→300s;只读四面 connect/is_user_authorized/iter|add_event_handler/disconnect 零写接口,调用面记录测试断言);CLI serve 与桌面 entry 双线并跑(一线致命不拖另一线,gather return_exceptions);events 按 `telethon-user:<api_id>` 指纹分库(F8 判例,与任何 bot 分文件),offsets 零写(telethon session 内部自持断点);
4. ✅ 测试全 mock:`tests/telegram/test_telethon_line.py` 32 例(依赖门/凭据三态/消息面适配→updates_to_items 复用/登录流七路径含零凭据兜底与 2FA/宿主连接退避+FloodWait 服从+session 失效/事件→条目→账本词表/相册三成员/只读边界/引擎 user 模式七例含 FloodWait 与 AuthKey 名匹配)+ desktop 用户线装配 1 例 + pyenv_resources 2 例;定向门禁 tests/telegram+engines 122 + desktop 164 全绿,ruff 绿;两世界验证(venv 装/不装 telethon 均绿——import_module 拦截缝,2026-10-08 全量套件实证 builtins.__import__ 拦截对 importlib 无强制力);
5. ✅ e2e 沙箱适配:pyaes(PyPI 无轮,sdist-only)令锁版清单首次含源码构建件——wheels 夹具补种 setuptools/wheel 构建后端(隔离子进程同 --index-url,不种必炸,实测在案);
6. ✅ 装机外科(vite build+tauri build exit 0,ditto 换装+sha 对拍+adhoc 重签+open -g 拉起+心跳;明细见 prd 过程段);
7. 真登录 AC2 留主人:手机号+验证码到位后 `myssia telegram login`(零凭据兜底已可登)。

## 批次 B5:装机与终验
1. 装机外科(src/plugins/lock 同步+重签;组件卡像素验证);
2. AC1/AC2 真发回执;AC3 组件化全流程一例;
3. 过程/结果段回填;档置 review。

## 停点(已决:Grill 七决议见 prd;B1-B3 放行,B4 锁小号)
- B1-B3 前置:bot 四步(token 到手即通,B1 代码可先行);
- B4 前置:小号+验证码(一次性);
- 全程:每批先更新本档过程段再动码(三段纪律)。
