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

## 批次 B3:常驻宿主 telegram serve(每时每刻)
1. `src/myssia/telegram/`(serve 循环/offset 持久/退避/事件账本,mock 可测);
2. CLI `myssia telegram serve` + desktop 侧接线(组件化位);测试 D5 serve 面;门禁+提交③。

## 批次 B4:Telethon 线(主人小号+验证码到位后)
1. extras 组件轨(pyproject extras+桌面锁 --extra telethon+设置页组件卡);
2. session 首登 CLI 流程(验证码交互,session 落数据根 0600,凭据入钥匙串);
3. telethon 源接入引擎与 serve(线程桥接);失败词表含 session_expired;
4. 测试:mock telethon 客户端;真跑 AC2;门禁+提交④。

## 批次 B5:装机与终验
1. 装机外科(src/plugins/lock 同步+重签;组件卡像素验证);
2. AC1/AC2 真发回执;AC3 组件化全流程一例;
3. 过程/结果段回填;档置 review。

## 停点(已决:Grill 七决议见 prd;B1-B3 放行,B4 锁小号)
- B1-B3 前置:bot 四步(token 到手即通,B1 代码可先行);
- B4 前置:小号+验证码(一次性);
- 全程:每批先更新本档过程段再动码(三段纪律)。
