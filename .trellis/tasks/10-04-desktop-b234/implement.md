# implement:成功率趋势折线 + 核验回标 + 死代码清理

前置:prd.md(范围与拍板)、design.md(§1-§7)。每步做完打勾并记一行实测命令+结果;
定向门禁本会话自跑,全量门禁归脚本;不 push、不 task.py(并行会话在场)。

## 步骤

- [x] **0. 开工实读(§6 checklist,必做不可跳)**
  - `find src -name sqlite.py -o -name models.py` 确认模块布局(改名波在途);
  - `grep -n "PROTOCOL_VERSION = " desktop/entry.py` 取现值,本批 = 现值+1(记入步骤 3);
  - `git status --porcelain` + `git diff --stat` 读热点文件(entry.py /
    test_desktop_sidecar_protocol.py / types.ts / client.ts)在途改动,只追加不重排;
  - 重读 dashboard-screen.tsx 趋势块现状(档载 :468-519 为 grill 后复核值,
    fbbaaa7 判例:该域分钟级在漂,行号以现树为准)。
    实测(2026-10-04):布局=src/myia(store/sqlite.py + store/models.py);PROTOCOL_VERSION=7
    (entry.py:371)→本批 8;_HANDLERS=47→48;热点在途 diff=改名波(shishi→myia 文档
    引用,±等量)无功能冲突;趋势块现树=dashboard-screen.tsx:467-526。

- [x] **1. store 层聚合**(design §1)
  - `src/<现名>/store/sqlite.py` daily_item_counts(:830)之后加
    `daily_run_outcomes(days, category)`,docstring 抄 design §1 草稿
    (口径/返回/ValueError 全写明);
  - 无独立单测——与 daily_item_counts 同门,覆盖走协议测试(步骤 6)。

- [x] **2. 协议 handler**(design §2)
  - entry.py:`_m_runs_trend` 落 runs.list(:2572)之后,节注释带
    `# 方法:runs.trend(G6 成功率折线,10-04-desktop-b234)`;
  - `_HANDLERS` 注册紧跟 `"runs.list"`;模块 docstring 方法表+参数契约段各补一行
    (样式抄 store.trend:172);
  - `PROTOCOL_VERSION` = 步骤 0 实读值 +1。

- [x] **3. spec + CHANGELOG**(design §2)
  - `.trellis/spec/desktop/sidecar-protocol.md`:注册表 #48 行 + 表头行数 48 +
    分组注记(desktop-b234 批新增 1;协议 v N);
  - `CHANGELOG.md` Unreleased/Added 英文条目(对齐 alert-rules 条目风格)。

- [x] **4. 共享层类型与门面**(design §3;追加式)
  - types.ts:RunsTrendParams/RunOutcomeDay/RunsTrendResult + METHOD map 行;
  - client.ts:runsTrend 门面(storeTrend 之后)。

- [x] **5. UI 装配与渲染**(design §3;grill 修正后方案)
  - dashboard/api.ts:fillDailyOutcomes / successRateSeries / fetchOutcomeWindow
    (grill 修正:原稿 rateToPoints 独立映射作废——Sparkline 无透传口);
  - sparkline.tsx:加向后兼容可选 prop `max?: number`(固定上界;未传=现行为
    max 归一不变,存量零感知);
  - dashboard-screen.tsx 趋势块(:468-519 现树)加「成功率」第二行:共享窗口
    Select(windowDays :312)、Sparkline 喂 `values=rate`+`max={1}`+`area={false}`、
    摘要行**累计口径**(「近 N 天累计成功率 X%(S/T)」)+「不含进行中」Badge、
    独立错误态(testid:dashboard-rate-sparkline / dashboard-rate-error,人话文案);
  - refreshTrend(:333)升级 Promise.allSettled 双序列同窗并发、各自降级
    (fbbaaa7 分区降级判例对齐,勿用会一败俱败的 Promise.all)。

- [x] **6. 测试**(design §4;测试面归属=grill 修正)
  - 协议:test_desktop_sidecar_protocol.py 加 runs.trend 节——聚合/钳制/category/
    空态/注册面五用例;聚合用例断言 **statuses.running 如实计数**(分母剔除是
    前端行为,不在协议层断言);种子走 SQLiteStore.start_run/finish_run 直写;
  - vitest:dashboard-screen.test.tsx 加序列装配(**running 不入分母+零完结日
    不入序在此断言**)/渲染/窗口切换重查/allSettled 双向降级/空态/Sparkline
    max prop 固定刻度+存量回归;mock api.runsTrend。
    实测:协议 test_runs_trend_daily_outcomes_utc(test:2016)+注册面 47→48+版本 7→8;
    vitest 新增 17 用例(4 组件 G6 + 3 纯函数 G6 + 2 Sparkline max + 8 迁移)。

- [x] **7. 死代码清理**(design §5)
  - 删 trend-card.tsx + trend-card.test.tsx;
  - `grep -rn "trend-card\|TrendCard" desktop/ui-src/src` 零命中(记输出)。
    实测:rm 两文件后 grep exit 1(零命中);trend-card.test.tsx 里 api.ts 活函数的
    8 个用例先迁 dashboard-screen.test.tsx(防 B4 覆盖静默丢失),仅组件 3 用例随删。

- [x] **8. 对账与定向门禁**(design §2/§4;全部本会话实跑并记输出)
  - 对账(grill 修正:目标 = 实读 `_HANDLERS` 现值+1,**不预写死 48**——hermes-cron
    若先合入即更多):`uv run --no-sync python -c "import desktop.entry as e; import re, pathlib;
    spec=pathlib.Path('.trellis/spec/desktop/sidecar-protocol.md').read_text();
    rows=len(re.findall(r'^\| \d+ \| `', spec, re.M));
    print(len(e._HANDLERS), rows)"` → 两数相等(=开工实读值+1,建档时点参照 48);
  - `uv run --no-sync python -m pytest tests/test_desktop_sidecar_protocol.py -q` 全绿;
  - `npm --prefix desktop/ui-src run test` 全绿;
  - `npm --prefix desktop/ui-src run build` 通过。
    实测:对账 `48 48` 相等;pytest `116 passed in 6.03s`;vitest `19 files /
    295 tests passed`;build `✓ built in 1.49s`(chunk 警告存量非错误)。

- [x] **9. 收口回标**(零代码)
  - prd.md AC 逐项勾选+证据(命令+输出摘录);R1 矩阵终检结论回写,矩阵行号按
    终检时现树同步刷新(grill ③:勿回写失效坐标);
  - v12-backlog G6 消号注记:本档不开工前不动他档——收口时若树静顺手加一行
    「G6 已随 10-04-desktop-b234 交付」回标(与 10-04 平行批统一处理,撞在途就留主人);
  - README 核对:零改动即过(:280 口径属实),记一行核对结论。

## 完成定义

prd.md AC 全勾 + 定向门禁三命令绿 + 对账相等;全量 pytest/vitest/cargo 由脚本统一,
不在本任务重复。实现不了或撞只有主人能定的事 → escalate,不绕过不造假。
