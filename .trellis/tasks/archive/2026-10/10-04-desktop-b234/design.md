# design:成功率趋势折线(runs.trend)+ 交付核验 + 死代码清理

对应 prd.md R1-R3。R1 是核验动作无设计;本文= R2 的四面设计 + R3 处置 + 并行波防护。
零 GUI:全部验证走协议 pytest + vitest(jsdom),无头可全证。

## §0 范围重述(拍板 1 已定稿)

B2/B3/B4 主体已交付(dc1cf86+3ac63af;证据矩阵见 prd「探查结论」)。本设计只覆盖
真增量:**G6 成功率折线**(服务端聚合 `runs.trend` + 仪表盘同块第二序列)与
trend-card 死代码清理。

## §1 store 层:runs 逐日×status 聚合

新增 `SQLiteStore.daily_run_outcomes`(`src/myia/store/sqlite.py`,紧邻
daily_item_counts:830 之后,镜像其口径):

```python
def daily_run_outcomes(self, *, days: int = 14, category: str | None = None
) -> list[dict[str, object]]:
    """Per-day per-status run counts for the last ``days`` days(成功率趋势,runs.trend)。

    Groups on ``substr(started_at, 1, 10)``(UTC calendar day,与 daily_item_counts
    同口径);窗口下界 = UTC now − days 天(仅 SQL 过滤);零数日补齐归前端。
    Returns ``[{date, total, statuses: {<status>: count}}]`` old → new,窗口内
    零 run 时为空列表(合法空态)。statuses 为开放词表原样分组——真实词表 4 态
    running/success/partial/failed(models.py:44-47 RUN_STATUSES;grill 修正:勿把
    cli.py 错误响应 error_type 的 config_error 误当 status 例举),未知状态照回,
    前端只消费 success/running 两键,其余求和入「完结未全成」。
    ValueError: days 非正整数(与 daily_item_counts 同口径)。
    """
```

SQL 形状(一次查询,零 Python 侧二次聚合):

```sql
SELECT substr(started_at, 1, 10) AS day, status, COUNT(*) AS n
FROM runs WHERE started_at IS NOT NULL AND started_at >= ?
  [AND category = ?]
GROUP BY day, status ORDER BY day ASC
```

Python 侧按 day 归并成 `{date, total, statuses{…}}`。窗口右端不设上界(未来时刻
started_at 不存在,无需防御)。

**为什么服务端**(拍板 2):runs.list limit≤200,cron 排程+手动下 30 天窗可超限,
前端聚合会静默失真;SQL GROUP BY 一次往返即真数据。

## §2 协议层:`runs.trend`(runs.* 家族 +1)

**方法契约**(参数校验逐字段抄 store.trend(entry.py:2745)/runs.list(:2572)先例,
错误结构化 `ProtocolError(code, message, path=…)`):

- params:`days`(int,缺省 14,钳制 [1,90],钳制不报错;bool 拒)、`category?`
  (非空 str,空串/非 str = invalid_params)、`db?`(缺省 `_serve_context().db`;
  `StoreSchemaError` → ProtocolError(exc.code, path="params.db", data=exc.details))。
- result:`{"days": [{"date": "YYYY-MM-DD", "total": int,
  "statuses": {"success": int, "running": int, …}}]}` 旧→新,只回有数日。
- 无新事件、无后台 job(纯读,一次往返)。

**落点**(全部追加式,热点文件纪律=先读现状再动手):

1. `desktop/entry.py`:
   - handler `_m_runs_trends`→命名对齐家族:`_m_runs_trend`,放 runs.list 实现
     (:2572-2598)之后、feedback 节之前,带节注释
     `# 方法:runs.trend(G6 成功率折线,10-04-desktop-b234;runs 表逐日×status 聚合)`;
   - `_HANDLERS` 注册表 `"runs.trend": _m_runs_trend`(紧跟 `"runs.list"` 行,
     entry.py:4043 附近);
   - 模块 docstring 方法清单两处补行(:49-57 方法表加一行 runs.trend;
     :157 参数契约段补一行,样式抄 store.trend 的 :172);
   - `PROTOCOL_VERSION = 7`(entry.py:371)→ **开工实读后 +1**(拍板 6;hermes-cron
     在途,预写死必撞车——alert-rules v7 判例原文见 spec 版本段)。
2. `.trellis/spec/desktop/sidecar-protocol.md`:注册表加 1 行(行号 #=开工实读
   `_HANDLERS` 现值+1,建档时点=48;grill 修正:hermes-cron 若先合入即更多,
   不预写死);分组注记补「desktop-b234 批(task 10-04-desktop-b234)新增 1:
   runs.trend(G6 成功率折线);协议 v N(实读值+1)」;表头行数与 `_HANDLERS`
   现值同步。
3. `CHANGELOG.md` Unreleased/Added:英文条目,对齐 alert-rules 条目风格
   (方法名+语义+口径一句话,指明 task)。
4. 对账:`method_not_found` 应答 `data.allowed`(entry.py:4104,=sorted(_HANDLERS))
   与 spec 注册表行数一致(**=开工实读 `_HANDLERS` 现值+1**,不预写死——grill
   修正);实测命令见 implement.md 步骤 8。spec 是镜像快照,单一事实源=代码。

**族先例说明**:批文说「按 image.* 家族先例」——image.* 的范式=前缀家族+spec 注册
行+协议版本 bump+docstring 契约段+协议测试全套。本方法语义上属 runs.* 族
(run.start/status/cancel、runs.list),故族名取 runs.*,**流程照 image.* 先例走全**。

## §3 UI 层:仪表盘趋势块加「成功率」第二序列

**共享层(追加式,热点文件)**:

- `desktop/ui-src/src/lib/api/types.ts`(:698-711 StoreTrend 区之后、:887 METHOD map
  追加一行):
  ```ts
  export interface RunsTrendParams { days?: number; category?: string; db?: string; }
  export interface RunOutcomeDay {
    /** YYYY-MM-DD(UTC) */
    date: string;
    total: number;
    statuses: Record<string, number>;
  }
  export interface RunsTrendResult { days: RunOutcomeDay[]; }
  // METHOD map 追加:"runs.trend": { params: RunsTrendParams; result: RunsTrendResult };
  ```
- `desktop/ui-src/src/lib/api/client.ts`(:209 storeTrend 之后追加):
  ```ts
  /** run 逐日×status 聚合(成功率趋势,G6) */
  runsTrend: (params: RunsTrendParams = {}): Promise<RunsTrendResult> =>
    request("runs.trend", params),
  ```

**dashboard 屏私有装配**(`desktop/ui-src/src/screens/dashboard/api.ts`,B4 节之后追加
「成功率趋势(G6)」节,纯函数风格与 fillDailyCounts 一致):

- `fillDailyOutcomes(rows: RunOutcomeDay[], days: number, today: string): RunOutcomeDay[]`
  ——补零窗口(镜像 fillDailyCounts:285;零 run 日 = total 0)。
- `successRateSeries(filled: RunOutcomeDay[]): Array<{ date: string; rate: number }>`
  ——逐日 `rate = success/(total−running)`(拍板 3);`total−running === 0` 的日子
  **不入序**(不虚构 0%/100%);running 取 `statuses.running ?? 0`。
- `fetchOutcomeWindow(days)`:拉 runs.trend + fillDailyOutcomes;失败上抛由调用侧
  降级(见下「渲染」的 allSettled 模式)。
- **刻度修正(grill change 采纳)**:原稿的 `rateToPoints` 独立映射作废——Sparkline
  组件只收 `values` 且内部强制 max 归一(sparkline.tsx:39-48,`y=pad+spanY*(1-value/max)`),
  无 points/domain 透传口,独立映射无入口可喂。改为**给 Sparkline 加向后兼容可选
  prop `max?: number`**(固定上界;未传=现行为 `Math.max(...values)` 不变,存量
  采集量序列零感知):成功率序列喂 `values=series.map(s=>s.rate)` + `max=1`,
  即落实固定 [0,1] 真刻度(否则 max 归一把 40%↔80% 拉成满格差,失真)。驳回备选
  「退回 max 归一+失真注记」:与真刻度目标直接冲突,加可选 prop 成本更低。

**渲染**(`dashboard-screen.tsx` 采集量趋势块 :468-519 内,同块第二行;拍板 4):

- 标题行「成功率」+ 复用同一个窗口 Select(不新增状态:窗口 state 已在
  :312 windowDays,成功率序列共享之)。
- **数据拉取对齐 fbbaaa7 分区降级判例**(10:54「单方法失败不再整屏报废」,主人
  目验判例「报错你也不处理」):`refreshTrend`(:333)升级为
  `Promise.allSettled([fetchTrendWindow(days), fetchOutcomeWindow(days)])`——两序列
  同窗并发、各自 fulfilled/rejected 分流,一条失败另一条照画,错误走人话文案。
- Sparkline(sparkline.tsx:51)复用:`values = series.map(s => s.rate)` +
  `max={1}`(见上刻度修正);`aria-label` 用**累计口径**(grill 修正,删「均值」
  歧义):`近 N 天累计成功率 X%(S/T 次成功),无完结 run 的日子不入线`;
  `area={false}`(比率序列渐变填充语义弱,更克制)。
- 摘要行:`近 N 天累计成功率 X%(S/T 次成功)` + Badge「不含进行中」——口径注记
  (与「近期 run 成功率」卡差异:该卡吃内存合并 active(api.ts:187-203
  summarizeRuns),逐日序列只见表内 status,running 一律不进分母。两处口径差异
  在卡面如实标注,不冒充同源)。
- 错误态:独立 `data-testid="dashboard-rate-error"` 人话文案(对齐 fbbaaa7 判例),
  采集量趋势失败不连带(allSettled 分流;反之亦然)。

**压缩画法取舍**(设计取舍记录,非拍板):零完结日跳过后折线只在有数日子间连段,
x 轴与上排采集量折线**不对齐**;对齐画法需 Sparkline 支持 null 断点(再扩公共组件
接口,v2 再议)。卡面注记已如实说明,不构成误导。

## §4 测试面

**协议级**(`tests/test_desktop_sidecar_protocol.py`,runs.trend 节追加;种子用
SQLiteStore.start_run/finish_run 同门直写,先例=runs.list 测试 :1989-2012):

1. 聚合正确性:今天 success×2 + failed×1、昨天 running×1(只 start 不 finish)、
   40 天前 partial×1(窗外)→ 应答逐日 total/statuses 断言,40 天前不入窗;
   **statuses.running 如实计数**(grill 修正:running 不入成功率分母是前端装配
   行为,其断言在下方 vitest,协议层只验计数真实)。
2. `days` 钳制:0→1、91→90、非 int/bool 拒(invalid_params)。
3. `category` 过滤 + 空串拒。
4. 空态:零 run 库 → `{"days": []}`(合法空态,非错误)。
5. 注册面:`data.allowed` 含 runs.trend(抄 :2186-2197 注册断言段,若该段是
   全量方法清单断言则同步 +1)。

**vitest**(`dashboard-screen.test.tsx` 追加 + api 纯函数用例入同文件或
dashboard/api 相邻用例;jsdom 无头):

1. `successRateSeries`:零完结日不入序、**running 不入分母**(拍板 3 口径的
   断言归此,grill 修正)、rate 数值断言。
2. 渲染:mock api.runsTrend → 成功率折线出现(testid `dashboard-rate-sparkline`)、
   摘要行累计口径文案、窗口切换触发 runsTrend 重查(与 store.trend 同窗并发)。
3. 降级:runsTrend 拒绝 → 成功率区显人话错误、采集量趋势不受连带(反之亦然;
   allSettled 分流)。
4. 空态:全窗口零完结 run → 空序列提示(如实「无完结 run」非画 0% 平线)。
5. Sparkline `max` prop:传 max=1 时 50% 画在半高(固定刻度断言)、不传时存量
   行为不变(回归护栏)。

**定向命令**(本会话自跑口径,全量归脚本):

```
uv run --no-sync python -m pytest tests/test_desktop_sidecar_protocol.py -q
npm --prefix desktop/ui-src run test
npm --prefix desktop/ui-src run build
```

## §5 R3 死代码清理

删 `desktop/ui-src/src/screens/dashboard/trend-card.tsx` +
`trend-card.test.tsx`(零引用实证:全树 grep 仅自身命中;内联趋势节
dashboard-screen.tsx:468-519 + 共享 ./api 装配已全面取代)。删后:
`grep -rn "trend-card\|TrendCard" desktop/ui-src/src` 零命中 + build 绿。
api.ts 的 `toTrendWindow`(:325)保留——fetchTrendWindow(:334)在用。

## §6 并行波防护(开工 checklist)

1. **路径重定位**:模块改名波在途(建档时亲历 src/shishi→src/myia staged rename)。
   开工先 `find src -name sqlite.py -o -name models.py` 确认布局;测试文件 import
   段跟随现树(协议测试现用 `from myia.store.models import …`,test:3217 先例)。
2. **PROTOCOL_VERSION 实读**(拍板 6):开工 `grep -n "PROTOCOL_VERSION = " desktop/entry.py`
   取现值 +1;hermes-cron 批若先合入,版本号与 spec 版本段以合入顺序为准。
3. **热点文件追加式**:entry.py / test_desktop_sidecar_protocol.py / types.ts /
   client.ts 先 `git diff` 读他会在途改动,只追加不重排;提交前重读一次防竞态。
4. **树静不可等**:多工作流常驻,「绿 HEAD 即取」纪律(journal 判例);定向门禁
   绿即收口,全量门禁交脚本。

## §7 风险与回退

- dashboard 三件是**最热活跃域**(grill 实测:fbbaaa7 10:54「仪表盘分区降级」+114/−26,
  建档读数两分钟后即漂移;更早 fe-small-batch 1d4ad62 动过文案)——开工必须重读
  趋势块现状(:468-519 为 grill 后复核值),块结构若再变,落位随之调整(同块原则
  不变);**R1 终检回写时同步刷新矩阵行号**,勿回写失效坐标。
- runs 表 started_at 为 TEXT ISO(substr 前 10 位=UTC 日)与 items first_seen 同存法,
  无时区换算风险;若开工实读发现存法漂移(带偏移量的 ISO),以 substr 口径为准并
  在卡面注记维持「UTC 逐日」如实口径。
- 回退单元小:协议方法纯读零副作用,UI 区块独立降级——任一环出问题可单独回退
  该提交,不影响已交付 B2/B3/B4。Sparkline `max` prop 向后兼容(未传=现行为),
  回退时无需动存量调用。
