# implement.md — 10-06-telegram-telethon 执行计划(先档后行,批间门禁)

## 批次 B1:bot 批量引擎(无前置,可先动)
1. `src/myssia/engines/telegram.py`(engine: telegram,设计 D2 契约)+ schema 词表两行(ENGINES/EngineName,收窄 hunk 判例)+ registry 注册;
2. 测试 `tests/engines/test_telegram_engine.py`(D5 引擎面);
3. 品类示范件 `plugins/telegram-groups.yaml`(源名规约 telegram-<群名>,注释态待主人拉群);
4. 门禁:定向 pytest+ruff;提交①。

## 批次 B2:过滤管线与出口接线
1. 粗筛词表配置化(品类 YAML watchlist 复用判定)+ LLM 精筛挂点(enrich 客户端复用);
2. 出口:高价值即时**合并单条**(组合铁律)/普通入库进合并日报(daily-digest 增「Telegram 群」分区);
3. 测试:同轮 N 条高价值恰一条(mock 通道);门禁+提交②。

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

## 停点(主人决策位)
- B1-B3 前置:bot 四步(token 到手即通,B1 代码可先行);
- B4 前置:小号+验证码(一次性);
- 全程:每批先更新本档过程段再动码(三段纪律)。
