# 桌面补实现 B2/B3/B4:交付核验 + 成功率趋势折线补齐

## Goal

主人批(2026-10-04 /workflow 做软件三连):v1.1.1 只改了宣称的 B2/B3/B4 桌面功能补真实现(定义源=gap-census B 组+v111-release 改宣称记录),**含采集量/成功率趋势折线**;探查→grill→实现全流程。

**建档探查修正范围**(见下「探查结论」,拍板 1 已按推荐定稿):B2/B3/B4 三件主体
**已在 main 交付**(dc1cf86+3ac63af,归档档 10-03-v112-desktop-parity 记账"PRD 11 项
代码面全消号",README:280 已如实宣称交付)——本任务真工 = ①三件交付核验回标
(零代码)②**G6 成功率趋势折线**(批文点名的"成功率"半边,现树仅数字无序列)
③顺手清 trend-card 死代码。不重做已交付件。

## 背景(定义出处,三源)

1. **B 组定义**:`archive/2026-10/10-03-gap-census/prd.md` §2(宣称 vs 实际)——
   B2=README:244「卡片内反馈按钮」v1.1 宣称而桌面零入口(行 33);B3=settings 屏缺
   PRD 承诺「反馈开关」分区(行 34);B4=仪表盘缺「采集量趋势」(行 35)。原始承诺
   =`archive/2026-10/10-02-v11-desktop-app/prd.md` 范围节(五屏:仪表盘"采集量趋势"、
   设置"反馈开关";行 10-15)。
2. **改宣称记录**:`archive/2026-10/10-03-v111-release/prd.md` Requirements 4(行 26-28):
   v1.1.1 把 README 三项交付宣称改如实口径,补实现指向桌面对齐批次;验收记录(行 90、123)
   载明 README.md:277 中英两处改口。当前 README.md:280 口径已回填为
   「已随桌面对齐批次落地、随下个发布版交付(反馈 CLI 已可用)| ✅ 已交付」。
3. **v1.2 池**:`10-03-v12-backlog/prd.md` §4(行 27-35,B2/B3/B4 边界,已回标被
   v112-desktop-parity 吸收)+ §5 G6(行 40):「采集量/成功率趋势折线(与 B4 采集量
   趋势同属一块,拆任务时合并考虑)」。G6 证据源=`archive/2026-10/10-03-ui-feature-census/prd.md`
   行 29:「仅最近 N 次成功率数字,无时间序列 → P2:采集量/成功率折线(run 记录已有
   数据)」。

## 探查结论(2026-10-04 建档会话实查 + grill 后复核;行号动态——模块改名波与并行提交在途)

> 行号口径:建档读数后 dashboard 三件被 **fbbaaa7**(10:54「仪表盘分区降级——单方法
> 失败不再整屏报废」)改过 +52 行,下列行号已按 **grill 后复核值**更新;开工时以
> 现树为准(implement 步骤 0 强制重定位)。

### 1. B2/B3/B4 主体已交付(证据矩阵)

| 件 | 协议面 | UI 面 | 测试面 | 归属 |
|---|--------|-------|--------|------|
| B2 卡片反馈 | `feedback.mark/list/stats` 三方法:desktop/entry.py:2667/2709/2736(三 handler),`_HANDLERS` 注册 :4089-4091;channel=desktop 落库,CLI `feedback list` 往返一致 | feed-card-feedback.tsx(👍/👎,置灰防重)挂 feed-screen.tsx:317;仪表盘 FeedbackStatsCard(dashboard-screen.tsx:714) | tests/test_desktop_sidecar_protocol.py:3240(往返)/:3285(窗口统计);feed-card-feedback.test.tsx | dc1cf86+3ac63af |
| B3 反馈开关 | 复用 `yaml.save`/`doctor`(无新方法) | settings「评分与反馈」卡 EnrichFeedbackCard(settings-screen.tsx:205 定义、:698 实挂):逐品类 enrich.enabled 切换即写回+预算护栏+model 写回,doctor 复核 | settings.test.tsx:602(enrich-feedback-card) | dc1cf86 |
| B4 采集量趋势 | `store.trend`(entry.py:2789,注册 :4092)→ SQLiteStore.daily_item_counts(src/myia/store/sqlite.py:830,items 按 first_seen UTC 逐日) | 仪表盘内联趋势节(dashboard-screen.tsx:484-529,ui-deep-imitation D5 + fbbaaa7 分区降级):7/14/30 天 Select+自绘 Sparkline | test_desktop_sidecar_protocol.py:3304(UTC 逐日/category/钳制);dashboard-screen.test.tsx | dc1cf86+3ac63af+1d4ad62+fbbaaa7 |

> **R1 终检回标(2026-10-04 收口,行号=终检现树)**:上表三件协议面(handler+注册)、
> UI 面(挂载点)、测试面(协议+vitest)全部实测在位——B2 grep 实据
> `entry.py:2667/2709/2736` + `feed-screen.tsx:317` + `test:3240/3285`;B3
> `settings-screen.tsx:698` 实挂 + `settings.test.tsx:602`;B4 `entry.py:2789` +
> `sqlite.py:830` + `dashboard-screen.tsx:484-529` + `test:3304`。三件无需重做,
> 结论与建档判词一致。

归档档回证:`archive/2026-10/10-03-v112-desktop-parity/prd.md` 归档注记(行 120)与
workspace/journal-1.md:341(dc1cf86「B2 反馈闭环/B3 评分开关/B4 sparkline 趋势…PRD
11 项代码面全消号」)。**结论:三件无需重做,本档只做核验回标。**

### 2. 真缺口(本任务的可交付增量)

- **G6 成功率折线缺位**:仪表盘「近期 run 成功率」仅一个数字(dashboard-screen.tsx:625
  `run-success-rate`,装配 dashboard/api.ts:187-203 summarizeRuns:runs.list(limit 20,
  api.ts:75)合并行的 success/finished 占比)——**无时间序列**,与 census G6「仅数字,
  无时间序列」判词逐字吻合。数据源已在:runs 表(status 词表 4 态 running/success/
  partial/failed,sqlite.py:146-148 + models.py:44-47 RUN_STATUSES),但 sqlite 无逐日
  聚合、协议无 `runs.trend`、UI 无序列。
- **死代码**:desktop/ui-src/src/screens/dashboard/trend-card.tsx + trend-card.test.tsx
  零引用(ui-src 全树 grep `TrendCard`/`from "./trend-card"` 仅自身与测试命中;仪表盘
  实际用内联趋势节+共享 ./api 装配)——v112 UI 半边(3ac63af)入库后被 ui-deep-imitation
  内联版取代,未删。

### 3. 环境事实(开工必读)

- **模块改名波在途**:建档会话中亲历 `src/shishi/store/sqlite.py`→`src/myia/store/sqlite.py`
  staged rename(git status `R src/shishi/... -> src/myia/...`)。本档行号按 src/myia 布局
  实读;开工时 `find src -name sqlite.py` 重定位,勿信本档路径字面。
- **PROTOCOL_VERSION 竞态**:现值 7(entry.py:371,alert-rules 批);hermes-cron 批在途
  (src/myia/cron/ 未提交)。spec 判例(alert-rules v7 注记):「按合入顺序定案,开工实读
  PROTOCOL_VERSION」——本批 bump 值开工时实读再 +1,不预写死。
- **共享热点文件**:desktop/entry.py、tests/test_desktop_sidecar_protocol.py、
  desktop/ui-src/src/lib/api/{types,client}.ts——先读现状、追加式、绝不重排他人改动。

## Requirements

- **R1 核验回标(零代码)**:按上方矩阵终检三件交付物在位(协议/UI/测试三面),
  结论回写本档 AC;若终检发现真缺口(如断言失配),缺口修复入本批。
- **R2 成功率趋势折线(最小真实现)**:
  - store 层:runs 表逐日×status 聚合(镜像 daily_item_counts 口径:UTC 逐日、窗口下界
    SQL 过滤、只回有数日、days 非正整数 ValueError 同门)。
  - 协议层:新方法 `runs.trend`(runs.* 家族;参数 days 钳制 [1,90] 缺省 14、category?、
    db?;应答逐日 status 计数)。按 image.*/store.trend 家族先例全套:entry.py 模块
    docstring 方法表补行、_HANDLERS 注册、PROTOCOL_VERSION bump(实读后 +1)、
    spec 注册表行+版本注记、CHANGELOG Unreleased 条目、协议测试。
  - UI 层:仪表盘采集量趋势块(dashboard-screen.tsx:468-519)**同块**加「成功率」第二
    序列:复用窗口 Select(windowDays state :312)与 fbbaaa7 分区降级先例;零完结 run
    的日子不入线(不虚构 0%/100%);types.ts/client.ts 追加式补 RunsTrend 类型与
    runsTrend 门面。
  - 测试:协议级(聚合正确性/钳制/category 过滤/空态)入 test_desktop_sidecar_protocol.py;
    vitest 覆盖序列装配与渲染(dashboard-screen.test.tsx + api 纯函数)。
- **R3 死代码清理**:删 trend-card.tsx + trend-card.test.tsx,删后 grep 复核零引用、build 绿。

## Acceptance Criteria

- [x] R1:B2/B3/B4 三件交付矩阵终检通过(协议方法注册、UI 挂载、测试在位三项各实测),
      结论回写本档;v12-backlog G6 消号回标注记随收口统一落(本档不开工前不动他档)
      → 终检矩阵+回标见上「R1 终检回标」;v12-backlog prd §5 G6 已加消号注记
      (10-03-v12-backlog/prd.md「已消号」行,收口时该档树静无在途改动)
- [x] R2 协议:`runs.trend` 应答 = 逐日 `{date, total, statuses{…}}` 旧→新;days 钳制
      [1,90]、category 过滤、db 兜底三参数行为与 runs.list/store.trend 先例一致;
      协议测试覆盖聚合/钳制/过滤/空态 + statuses.running 如实计数(running 不入
      成功率分母是**前端装配行为**,其断言归 R2 UI 的 vitest——grill 修正:测试面
      归属对齐 design §4)
      → `_m_runs_trend`(entry.py:2617,参数校验逐字段抄 store.trend 先例);
      `test_runs_trend_daily_outcomes_utc`(test:2016):聚合(today success3+failed1/
      yesterday running1 如实计数/40 天前 partial 窗外)+ 钳制(0→1、91→90)+ category
      + 空串/非 int/bool 拒 + 空态 `{"days": []}`;`test_method_registry…` 47→48 +
      runs.trend 入 allowed;`test_protocol_version…` 7→8
- [x] R2 UI:仪表盘趋势块出现成功率折线,与采集量共用窗口切换;无完结 run 的日子
      不入线且卡面如实注记;vitest 断言 running 不入分母 + 零完结日不入序;成功率
      数值与「近期 run 成功率」卡口径差异(表内 status≠running vs 内存合并 active)
      有注记不冒充同源
      → dashboard-screen.tsx 趋势卡内 `dashboard-rate-section` 第二行(共享 windowDays
      Select + Sparkline max=1 area=false + 「不含进行中」/「零完结日不入线」Badge +
      独立 `dashboard-rate-error`);vitest:G6 折线用例(running 不入分母 0.8≠0.667 +
      固定刻度 points="3.0,28.2 257.0,11.4" + 累计口径摘要 67%(10/15))+ 窗口切换
      双查询 + allSettled 双向降级 + 空态不画 0% 平线 + Sparkline max 回归护栏
      (dashboard-screen.test.tsx,31 用例)
- [x] R2 对账:`method_not_found` 的 data.allowed 与 spec 注册表行数一致
      (=开工实读 `_HANDLERS` 现值 +1;不预写死数值——hermes-cron 在途,grill 修正),
      client 门面与 types METHOD map 同步
      → 对账命令实测输出 `48 48`(开工实读 47+1=48);client.ts runsTrend 门面 +
      types.ts METHOD map 行均紧跟 runs.list
- [x] R2 版本:PROTOCOL_VERSION 开工实读后 +1;CHANGELOG Unreleased 有英文条目;
      spec sidecar-protocol.md 注册表+分组注记+版本段更新
      → 开工实读=7(alert-rules 批),本批=8;CHANGELOG Unreleased/Added 英文条目;
      spec 注册表 48 行+表头 48+desktop-b234 分组注记+版本段 v8
- [x] R3:trend-card.tsx/trend-card.test.tsx 删除,全树 grep 零残留,build 绿
      → 两文件已删;`grep -rn "trend-card\|TrendCard" desktop/ui-src/src` 零命中
      (exit 1);build ✓(1.49s)。**附带处置**:trend-card.test.tsx 原承载
      fillDailyCounts/shiftUtcDate/toSparklinePoints 三个 api.ts 活函数的唯一测试,
      整删会静默丢 B4 验收落点覆盖 → 8 用例迁入 dashboard-screen.test.tsx
      (仅 TrendCard 组件 3 用例随死代码消亡),R3 边界内的保全取舍
- [x] 定向门禁(本会话自跑):`uv run --no-sync python -m pytest
      tests/test_desktop_sidecar_protocol.py -q` 全绿;`npm --prefix desktop/ui-src run test`
      与 `run build` 全绿。全量门禁由脚本统一,不在本任务内自跑
      → 三命令终跑实测:pytest `116 passed in 6.03s`;vitest `Test Files 19 passed (19)
      / Tests 295 passed (295)`;build `✓ built in 1.49s`(chunk 体积警告为存量,非错误)
- [x] README 核对:零改动即过(:280 宣称「采集量趋势」已含且属实;成功率半句是否
      加字留下一发布任务,不在本批)
      → 宣称行现树漂移至 :290-291/:301(改名波),「桌面卡片内反馈按钮、设置反馈
      开关、采集量趋势已随桌面对齐批次落地 main」与 R1 终检矩阵一致属实;本批
      README 零改动(git diff 中 README 改动均为并行会话改名波,非本档)

### 终检冒烟回标(2026-10-04 终检会话,无头独立复核)

- R1 / R2协议 / R2UI / R2对账 / R2版本 / R3 / README 七项 **passed**:协议面
  entry.py:4083-4092 注册表实读 + 真 sidecar spawn 全应答;UI 面三件 GUI 实测
  (B2 👍 aria-pressed 翻转+置灰 / B3 开关 aria-checked 三态 / B4+G6 双折线
  逐点对算);测试面协议 116 passed + vitest B234 范围套件全绿(dashboard 36/
  settings 30/feed-card 6/client 6/feed 60)。证据全量见 evidence/ 与
  smoke-run.log。
- 定向门禁 **manual**:vitest 全量 337 passed/1 failed,唯一失败 =
  top-bar.test.tsx「全局命令位留白」——并行 interaction-batch 波已把留白换成
  真命令面板触发器(top-bar.tsx:99),非 B234 回归,归属留主人裁量。
- 对账口径时效注记:48/48 与 PROTOCOL_VERSION=8 为**冒烟时点实读**;终检提交
  时点并行 hermes-cron B3 波已在工作树把 `_HANDLERS` 推至 57(cron.* 九方法)、
  版本推至 9——本档对账证据以冒烟时点为准,cron 面归其自档。

## 已拍板决议(grill 质询定稿,2026-10-04;主人「全按推荐」授权口径,事后可翻案)

质询结论:6 决议全 ok 维持;4 项 change 修正已采纳(见下「质询修正」)。定义链闭合
核验(gap-census §2 ↔ v11 PRD 五屏逐项对上;批文「成功率」半边=G6 逐字核实)、
协议扩张必要性核验(runs.list limit 钳制 [1,200] 实测 entry.py:157,dashboard 现拉
20 条 api.ts:75;hermes-cron 五文件 staged 在途,30 天窗超 200 论据成立)、验收可
自动化核验(对账 regex 实测有效、三定向命令在案、README 零改动口径实测成立)均过。

1. **范围定调**:B2/B3/B4 主体已交付(dc1cf86+3ac63af,README:280 宣称属实),本任务
   改为「核验回标+G6 成功率折线+死代码清理」,不重做三件。**定稿:按此改口径。**
2. **成功率数据通道**:**定稿:服务端聚合 `runs.trend`**(SQL GROUP BY 逐日×status)
   ——排程+手动 run 下 30 天窗可超 runs.list 的 200 上限,limit 截断会让序列悄悄
   失真;census"纯前端可画"是当时轻估。纯读一次往返、零事件零 job,与 store.trend
   先例对称,是 +1 方法的最小扩张。
3. **成功率口径**:**定稿:每日 `success/(total−running)`**(零完结日=无值不入线);
   词表 4 态(models.py:44-47);与「近期卡」(内存合并 active)口径差异如实注记、
   不冒充同源。
4. **UI 落位**:**定稿:采集量趋势块同块第二行**(v12-backlog G6 原话「同属一块」;
   windowDays state 共用)。
5. **死代码处置**:**定稿:删 trend-card.tsx+test**(零引用实证;api.ts toTrendWindow
   在用故保留)。
6. **协议版本纪律**:**定稿:开工实读 PROTOCOL_VERSION 再 +1**(现值 7,entry.py:371;
   hermes-cron 在途,alert-rules v7「按合入顺序定案」判例)。

### 质询修正(change 采纳,原文→修正)

1. **渲染方案(design §3 原稿)**:原文「rateToPoints 固定 [0,1] 域映射 + 复用
   Sparkline 喂 values」存在硬矛盾——Sparkline 只收 `values` 且 sparkPoints 内部
   强制 max 归一(sparkline.tsx:39-48),无 points/domain 透传口。**修正(采纳)**:
   给 Sparkline 加向后兼容可选 prop `max?: number`(固定上界;未传=现行为不变),
   成功率序列喂 `values=rate` + `max=1` 落实固定 [0,1] 刻度;驳回备选「退回 max
   归一+失真注记」——百分比序列按 max 归一会把 40%↔80% 拉成满格差,与「真刻度」
   目标直接冲突,加一个可选 prop 成本更低且向后兼容。同时 aria 摘要措辞统一为
   **累计口径**(「近 N 天累计成功率 X%(S/T)」,删「均值」歧义)。
2. **§1 docstring 状态例举**:原文例举含 `config_error` ——非 runs.status 值
   (全仓词表仅 4 态,models.py RUN_STATUSES;cli.py 的 config_error 是错误响应
   error_type)。**修正(采纳)**:例举改真实 4 态 running/success/partial/failed;
   开放词表原样分组的代码行为不变。
3. **AC R2 协议行测试归属**:原文「协议测试含 running 不入成功率分母的口径断言」
   放错面——分母剔除是前端 successRateSeries 行为,协议层只回逐日计数。
   **修正(采纳)**:协议断言改「statuses.running 如实计数」,分母剔除断言挪 R2 UI
   的 vitest(与 design §4/implement 步骤 6 实际分配对齐)。
4. **对账目标数值**:原稿写死「48 行(spec 47→48)」与拍板 6 精神不一致——
   hermes-cron 若先合入 cron.* 方法注册表即超 48。**修正(采纳)**:对账目标改
   「=开工实读 `_HANDLERS` 现值 +1」,对账命令本身动态打印两数相等即过(design
   §2/implement 步骤 8 已同步)。

### 质询连带处置(ok 项内建议,已顺手落)

- task.json title/description 旧口径「三件功能真做出来」与新范围不同步 → 已随手
  改为核验+G6+清理口径(2026-10-04)。
- dashboard 三件 10:54 被 fbbaaa7(分区降级)改过,PRD/design/jsonl 行号已按
  grill 后复核值整体刷新(趋势块 468-519、windowDays :312、summarizeRuns :187-203、
  FeedbackStatsCard :649、toSparklinePoints :300、fetchTrendWindow :334、
  run-success-rate :625);R1 终检回写时须再同步一次现树行号。

## 明确不做(防范围蔓延)

- 不重做/不加码 B2/B3/B4 已交付件(反馈标记回放、enrich 卡扩表单等均为已定设计的
  如实取舍,见各文件头注释,不翻案)。
- 不做 G7(run 重跑/过滤/日志搜索)、G9 等池内其余项——各归 v12-backlog 拆任务。
- 不动 README 交付宣称(:280 现口径属实;成功率半句措辞归下一发布任务)。
- 不做日志持久化(C4)、插件市场(C6)等 census 登记项。
- 装机/真机冒烟类验收归 10-04-wrapup-checklist;本任务无头验证(协议 pytest+vitest
  jsdom)即全证。
- 不 push、不跑 task.py start/finish/archive(并行会话在场,归档留主人)。

## 关联

- 定义源:archive/2026-10/10-03-gap-census(prd §2 B 组)、archive/2026-10/10-03-v111-release
  (改宣称记录)、10-03-v12-backlog(§4+§5 G6)、archive/2026-10/10-03-ui-feature-census(G6 行 29)
- 交付归属:archive/2026-10/10-03-v112-desktop-parity(B2/B3/B4 实现档+AC 口径)
- 并行任务:10-04-proxy-pool、10-04-windows-build(同批三连,互不相交);
  10-04-hermes-cron(协议版本竞态相关,在途)
