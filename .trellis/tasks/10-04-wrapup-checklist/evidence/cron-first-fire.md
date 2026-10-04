# cron 首燃验收证据(桌面=定时宿主,冻结包 /Applications/世事.app 23:20 换装)

**任务**:目验操作单步骤 2/3/7 的自动化代做(活性条/首燃/清场+补拍 08-cron 屏)
**时间**:2026-10-04 23:33 – 23:54(+08:00)
**沙箱**:`MYIA_HOME=/tmp/myia-cron-firstfire`(先清后建,单实例锁按 MYIA_HOME 分域,`main.rs:280-291`;与主人默认根 `~/Library/Application Support/MYIA` 的既有实例互不干扰)
**品类夹具**:仓库 `desktop/fixture/plugin.yaml` 拷为 `<沙箱>/plugins/desktop-fixture.yaml`(static_html 引 `http://127.0.0.1:8765/page.html`,零凭据、零外网——本地夹具服务 `desktop/fixture/serve.py` 仅绑 127.0.0.1;夹具页固定 3 条 `li.item`)
**预验**:起 app 前先 dry-run 全链路(`uv run myssia run <夹具> --db <沙箱>/myia.db --dry` → fetch 1→3 / classify 3→3 / dedup 3→3 / push dry,0.08s,exit 0),排除夹具自身问题。

---

## 一、结论(FirstFireResult 口径)

**✅ 首燃判定通过。**冻结包桌面的 sidecar ticker 在 MYIA_HOME 沙箱内真实燃了:executions 账本(`<数据根>/cron/executions.db`)出现 **source="tick"、status="completed"** 的执行行(首次 23:36:34),真实管线跑通(源 1/1 ok、条目留存 3、时长 0.106s、`deliver=local` 落 `<数据根>/cron/output/<job_id>/<时间戳>.md`)。

四要素对照(ask 判据逐条):

| # | 判据 | 结果 | 证据 |
|---|------|------|------|
| 1 | `cron runs` 出现 source="tick" 行 | ✅ | 23:36:34 行:`{"source": "tick", "status": "completed", "scheduled_instant": "…T15:36:30Z", "claimed_at": "…23:36:34.148+08:00", …}`;run_summary:`run.status=ok, exit_code=0, sources.ok=1/total=1, items=3, items_retained=3, duration=0.106s, dry_run=false`(全文见下节) |
| 2 | 心跳龄新鲜(<90s) | ✅ | 验收全程反复采样:`ticker_alive=true, heartbeat_age_seconds` 始终在 0-60s 间循环(60s tick 间隔;空转 tick 也落心跳,`tick.py:328`) |
| 3 | jobs 的 last_run_at/last_status 更新 | ✅ | 首燃后 `cron list --json`:`"last_run_at": "2026-10-04T23:40:59.786680+08:00", "last_status": "ok", "repeat": {"times": null, "completed": 2→…→7}`(逐次递增) |
| 4 | 「立即运行」排队语义(cron run 后 ≤2 tick 内 manual 行出现) | ✅(语义)/⚠️(标签) | 23:41:15 `cron run` 戳 `manual_run_at=next_run_at="…23:41:15.766632+08:00"`(同一 isoformat 串,`jobs.py:1099-1108`);**恰 1 个 tick 后**(23:41:59,44s,≤2 tick)被消费执行完成,repeat.completed 递增,`scheduled_instant=null`(手动跑的身份标记,`jobs.py:2061-2066`)。**⚠️ 但执行行 `source` 写的是 "tick" 而非 "manual"**(见下「发现 1」) |

**截图交付度:1/3。**`08-cron-list.png` 已拍(OCR 验证内容:活性条「ticker 活跃 · 下次 10/04 23:52 · 1个job · /tmp/myia-cron-firstfire」+ 完成横幅「定时任务「首燃验证·每分钟」完成(status=ok)」+ 九列 job 行含 次数 6/∞)。展开屏与急停红条无法安全代拍(见「截图局限」节)。

---

## 二、关键命令与时间线(全部 +08:00)

### 1. 起 app(第 1 次)

```bash
MYIA_HOME=/tmp/myia-cron-firstfire MYIA_SHOW_ON_START=1 MYIA_SMOKE_ROUTE=cron \
  nohup /Applications/世事.app/Contents/MacOS/MYIA &   # pid 44838
# app.log: "desktop: sidecar(serve) spawned in 241 ms"(sidecar launcher 44844 → payload 44851,onefile 双进程)
# CGWindowList(按 pid 匹配):主窗 winID 10867,880×640@name=世事(首启 ~16-25s 出窗,按先例)
```

### 2. ticker 心跳 + 数据根(起 app 后 ~47s)

```bash
uv run myssia cron status --db /tmp/myia-cron-firstfire/myia.db --json
# → {"ticker_alive": true, "heartbeat_age_seconds": 41.9, "estopped": false,
#     "data_root": "/tmp/myia-cron-firstfire", "jobs_total": 0, "next_due_at": null}
```

> 桌面 UI 活性条第八屏同源信号(cron.status 协议)与此一致——截图 OCR「ticker 活跃 · 下次 10/04 23:52 · 1个job · /tmp/myia-cron-firstfire」互证。

### 3. 建 job(CLI,与桌面同数据根)

```bash
uv run myssia cron create "every 1m" \
  --category /tmp/myia-cron-firstfire/plugins/desktop-fixture.yaml \
  --db /tmp/myia-cron-firstfire/myia.db --deliver local \
  --name "首燃验证·每分钟" --json
# → job id=4cfe84917649, schedule kind=interval minutes=1, origin.source="cli",
#   next_run_at=23:36:30.090033+08:00, last_run_at=null
```

### 4. 首燃观测(采样每 20s)

```
[23:36:01] alive=True hb=27.9s runs count=0
[23:36:22] alive=True hb=48.6s runs count=0
[23:36:43] alive=False hb=8.9s  runs count=1 [('tick','completed')]   ← 首燃!23:36:34 完成
```

首燃行(run_summary 全文):

```json
{"id": "4a1db4c14ec64002bb8f2f7544929833", "job_id": "4cfe84917649",
 "source": "tick", "status": "completed",
 "scheduled_instant": "2026-10-04T15:36:30.090033+00:00",   // = next_run_at,准点
 "claimed_at": "23:36:34.148872+08:00", "started_at": "23:36:34.155527+08:00",
 "finished_at": "23:36:34.512624+08:00",
 "run_summary": {"run": {"status": "ok", "exit_code": 0, "duration_seconds": 0.106, "dry_run": false},
                 "sources": {"total": 1, "ok": 1, "items": 3}, "items_retained": 3, …},
 "pid": 44851, "error": null}
// 侧车真实 spawn 命令(deliver=local 摘要 .md 内原文):
//   /Applications/世事.app/Contents/MacOS/myssia-core run /private/tmp/…/desktop-fixture.yaml --db /tmp/myia-cron-firstfire/myssia.db --json
```

> 创建(23:35:30)→ 点火(23:36:34)恰 64s,= 1min 间隔 + 首 tick 对齐,符合预期窗口(70-150s 预算内)。

### 5. 外杀事件(详见第四节):第 1、2 个实例被外部杀

### 6. 重启后的 catch-up(计划外,但正是挂账里「崩溃恢复」的真实演练)

```
last_dispatch: {"scheduled_at": "23:37:34.518+08:00", "dispatched_at": "23:40:59.439+08:00",
                "lateness_seconds": 204.9, "kind": "catch_up"}
// 外杀窗口内到期的槽位,重启后首 tick 只补一发(at-most-once,积压坍缩),不重发。
```

### 7. manual 排队语义

```bash
date "+%H:%M:%S queueing manual"   # → 23:41:15
uv run myssia cron run 4cfe84917649 --db … --json
# → manual_run_at=next_run_at="23:41:15.766632+08:00"(同串)
# 23:41:59(44s 后 = 恰 1 个 tick)消费完成:executions 行 claimed 23:41:59.437,
#   finished 23:41:59.797, scheduled_instant=null(manual 身份),repeat.completed 2→3
```

### 8. 最终账本(三个实例接力写入,同数据根契约的实证)

```
total rows: 7(全部 completed,零 error)
  23:53:25 tick  sched 23:52:26    (实例3)
  23:51:25 tick  sched 23:46:59    (实例3 启动恢复 catch-up,实例2 被杀期间积压的槽)
  23:45:59 tick  sched 23:44:59    (实例2)
  23:43:59 tick  sched 23:42:59    (实例2)
  23:41:59 tick  sched None=manual (实例2;← source 标签缺口,发现1)
  23:40:59 tick  sched 23:37:34    (实例2 catch-up,lateness 204.9s)
  23:36:34 tick  sched 23:36:30    (实例1 首燃)
```

### 9. 清场(步骤 7)

```
kill 69575(实例3)→ 69575/69581/69588 三进程全部确认死透(/Applications 世事实例清零;target/ 路径实例 30096 系 23:36 被外部杀,非本验收所动)
cron remove 4cfe84917649 → removed=true, list count=0(output 目录与账本行按设计保留)
kill 44564(本地夹具服务)→ 127.0.0.1:8765 关闭
沙箱 /tmp/myia-cron-firstfire 整体保留供复核(见第六节)
```

---

## 三、两个非阻塞发现(建议随 wrapup 归档,不阻塞装机验收)

### 发现 1:执行行 `source` 恒写 "tick",manual 消费在账本不可辨(UI「手动」标签永不出现)

- **现象**:`cron run` 排队的手动跑,消费执行行的 `source` 仍是 `"tick"`(上表 23:41:59 行)。手动身份只能靠 `scheduled_instant=null` 间接辨认。
- **根因**:`create_execution` 的唯一派发调用点硬编码 `source="tick"`——`src/myssia/cron/tick.py:493-495`(`execution = cron.ledger.create_execution(job_id, source="tick", …)`,注释还写着「source='tick',design §2.3」)。而账本 schema 明确支持 manual 域:`src/myssia/cron/executions.py:332-334` docstring「source ∈ 'tick'|'manual',design §2.3」。全库无任何代码路径写 `"manual"`。
- **下游影响**:桌面端 RunsPanel 按 `exec.source === "manual"` 切「手动/排程」标签(`desktop/ui-src/src/screens/cron/cron-screen.tsx:823`)——该标签**恒显示「排程」**。主人目验步骤 3 的「行展开看执行记录」会看到全部标「排程」,属预期内显示缺口,不是排队没生效(排队生效与否以 manual_run_at 消费 + repeat.completed 递增为准)。
- **建议**:一行修(派发处把 `manual_run` 传给 create_execution),加一条断言 manual 消费行 source="manual" 的单测;不修也不影响定时语义,只影响账本可读性/UI 标签。

### 发现 2:验收期间 MYIA 实例被外部杀(两次,含主人自己的残留实例)

详见第四节。**与 fire 路径无关**(反证:第 3 个实例连续燃 3+ 次、共 7 次执行全程无崩溃,直到我主动清场杀掉;首燃那次也是账本完整落盘后才死)。但「桌面=定时宿主」形态若在真机长跑,值得主人知道本机当时有东西在周期性杀世事进程(候选:并行 ZCode 会话的清理脚本 / 主人本人清理弹窗;23:33-23:54 窗口内至少 6 个 ZCode workflow run 在跑)。

---

## 四、外杀事件时间线(两次)

**窗口 1:23:36:22 – 23:36:43(首燃完成后 ≤8s 内)**
- 我的沙箱实例 1(44838→44844→44851)死:心跳停在 23:36:34.5(= 首燃完成时刻),23:36:43 采到 writer pid 44851 已死。
- **主人默认根实例 30096(target/ 路径,23:14:57 起)同一窗口死**:其数据根 `~/Library/Application Support/MYIA/cron/` 无 jobs.json(零 job!),心跳停在 23:35:58(pid 30126=其 serve payload),下个 tick 23:36:58 永未发生。
- 判定依据:① 30096 无任何 cron job,不存在 fire 路径,不可能是 fire 崩溃;② 两实例几乎同时死;③ `~/Library/Logs/DiagnosticReports/` 无 23:36 前后 MYIA/世事/myssia-core crash report(最新是 23:20 的 node)→ 干净终止(SIGTERM/SIGKILL 类),非段错误。

**窗口 2:23:45:12(截图时还活)– 23:47:30(下次查时已死)**
- 实例 2(56813→56820→56827)死。死前窗口被人动过:窗口从 880×640 变 1500×799(tauri.conf.json 默认 880×640,工程无窗口态插件,配置内无 resizer),且屏幕从 MYIA_SMOKE_ROUTE=cron 指定的 #/cron 变成了「源管理」(代码无任何到 /sources 的自动跳转,App.tsx:43 只回落 /;唯一 navigate("/sources") 在 feed 屏的按钮回调,`feed-screen.tsx:1687`)→ 是有人在窗口里点过侧栏/拖拽过窗口。

**反证(fire 路径无罪)**:实例 3(69575,23:51:24 起)以同参数直跑,23:51:25(catch-up)与 23:53:25(正常槽)两次 fire 后三进程全部健康存活,心跳循环到 23:54 我主动 kill 为止。

**实例代际表**:

| 代 | app pid | sidecar launcher → payload | 窗 winID | 生卒 | 死因 |
|----|---------|---------------------------|----------|------|------|
| 1 | 44838 | 44844 → 44851 | 10867 | 23:33:37 – ~23:36:4x | 外杀(首燃后 ≤8s) |
| 2 | 56813 | 56820 → 56827 | 10989 | 23:41:05 – 23:45:12~23:47:30 间 | 外杀(死前窗口被人操作过) |
| 3 | 69575 | 69581 → 69588 | 11232 | 23:51:24 – 23:54:0x | **我主动清场 kill(验收完成)** |

---

## 五、截图局限(为什么只有列表屏 1/3)

- ✅ `docs/screenshots/install-cronline-1004/08-cron-list.png`(215KB,1760×1280@2x):OCR 逐行验证含——活性条「ticker 活跃 · 下次 10/04 23:52 · 1个job · /tmp/myia-cron-firstfire」+「急停全部」「刷新」按钮 + 完成横幅「定时任务「首燃验证·每分钟」完成(status=ok)」+ 新建按钮/计数「共1个」+ 九列 job 行:名称 首燃验证·每分钟 / every 1m / 下次 10/04 23:52 / 上次 10/04 23:51 / 成功 / local / **6/∞**。
- ❌ `08-cron-展开`:需要点行首展开 chevron。合成点击走 CGEvent 全局坐标,**安全前置检查(`topmost.swift`)两次都判定点击点当前被主人 ZCode 窗口(pid 39462)覆盖——我的窗口 onScreen=false(被移到非活跃 Space,与外杀事件 2 的「有人操作过窗口」互证)**;盲点=点进主人的编辑器,不可接受。
- ❌ 急停红条:同样需要两次点击(急停全部→确认急停),同上不可安全执行(且为可选件)。
- AXPress 替代路也断:raw AX API 按进程直查(`AXUIElementCreateApplication`)返回 AXWindows count=0——app 不暴露任何 AX 元素;System Events 进程表也枚举不到该 pid(129 个 app process 中无)。与 journal 既有记录「System Events 窗口计数 0 ≠ 无窗口」一致。
- 重新激活窗口(`open -b` → Reopen → show+focus,`main.rs:380-389`)可恢复可点性,但=当着主人正在用的工作屏抢前台,违反静默纪律;且展开屏对首燃核心证据无增量(账本明细已全量 CLI 取证)。**主人目验步骤 3(「行展开看执行记录」)顺手可补拍。**

---

## 六、沙箱复核指引(保留,未删)

```
数据根:/tmp/myia-cron-firstfire
  cron/jobs.json            # 验收后 count=0(job 已删;含 jobs 注册表结构)
  cron/executions.db        # 7 行 execution(全部 completed;含首燃/两次 catch-up/manual/正常槽)
  cron/output/4cfe84917649/ # 每 run 一份 .md 摘要(deliver=local 的实际投递物)+ .inflight/(正常收尾已清空)
  cron/ticker_heartbeat|ticker_last_success|catch_up_occurrences|tick.lock|estop 无
  plugins/desktop-fixture.yaml  # 品类夹具(static_html→127.0.0.1:8765;注意:夹具服务已杀,复核再跑需重启 serve.py)
  myssia.db                 # app home 模式主库(run 子进程 --db 指向它;cron 注册表/账本不进它,独立两文件)
复核命令(在仓库根):
  uv run myssia cron runs --db /tmp/myia-cron-firstfire/myia.db --json | head -50
  uv run myssia cron status --db /tmp/myia-cron-firstfire/myia.db --json
  # 注意:app 已清场,心跳龄会持续增大(writer 已死,ticker_alive=false 属预期;账本/输出不受影响)
```

---

## 七、验收结论回执

- 首燃(ask 步骤 4 主体):**✅ 通过**——桌面 ticker 真燃,证据链完整(心跳→建 job→source=tick 执行行→真实管线摘要→UI 同源活性条截屏互证)。
- 步骤 2(第八屏活性条):**✅ 通过**(截屏 OCR:「ticker 活跃 · 下次 <时刻> · N 个 job · <数据根>」,全字段与 CLI status 一致)。
- 步骤 3(建 job+等 2-3 分钟+立即运行):**✅ 通过**(7 次执行含首燃/catch-up×2/manual/正常槽;「≤60 秒内开始」的排队提示语义由 manual_run_at 消费时序证明,44s)。
- 步骤 7(清场):**✅ 完成**(job 删、实例杀净并验证、夹具服务关、沙箱保留)。
- 附带交付:外杀事件档案(第四节)、发现 1(source=manual 标签缺口,含根因行号)、发现 2(进程被周期性杀的环境风险提示)、发现 3(顺带实证重启 catch-up 恢复——挂账「崩溃恢复只能时间/真机暴露」项的第一次真实机暴露)。
