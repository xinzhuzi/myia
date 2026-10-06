# design.md — 统一日志模块

> 对应 prd.md R0–R9。核心:一个模块、一个漏斗、一种文件形状、一套轮转保留;CLI/sidecar/cron/vision 全路由;Rust 壳与 UI(webview)经 tauri-plugin-log 汇入同一 `logs/` 目录——各层关键日志「必须有」逐层对账。

## 0. 总形

```
                          ┌─ stderr handler(mode 分级:human=INFO / json·serve=WARNING)
一条日志/一行子进程输出 ─→ root logger(经 src/myssia/log.py configure)─┼─ Ring handler(4000 帽,UI 数据面)
                          └─ JSONL File handler(数据根 logs/<prefix>-YYYYMMDD.jsonl,按天轮转+保留 7 天)

UI(webview):console.* / onerror / unhandledrejection / ErrorBoundary / updater 埋点
    └→ lib/log.ts 劫持 console(官方 forwardConsole 模式)→ @tauri-apps/plugin-log JS API(invoke plugin:log|log)─┐
Rust 壳:log:: 宏(生命周期/pyenv/sidecar stderr pump)────────────────────────────────────────────────┴→ plugin targets

<数据根>/logs/
  myssia-YYYYMMDD.jsonl   ← Python 全域单文件(CLI 跑次/serve/cron/**vision**,proc 字段分进程;按天文件,模块自管;决议③)
  shell.log + shell_<时间戳>.log 归档 ← Rust 壳 + UI webview(tauri-plugin-log 2.10;按大小轮转+归档名时间戳,格式沿 plugin 默认=决议⑤;清理见 §4)

> **grill 轮 1 决议(2026-10-07 主人令「按推荐」)**:①CLI/cron 全量落盘双份接受 ②CLI 仅 MYIA_HOME 设时落盘 ③vision 并入 myssia 单前缀、vision-server.log 退役 ④UI 错误不进日志屏 ⑤壳格式沿 plugin 默认 ⑥默认值包(保留 7 天/回填 2000/console 全劫持/ErrorBoundary 极简/log.py/tests/test_log.py/壳 5MB)。全文按此定稿。
```

> **事实勘误(grill 轮 1,2026-10-07 源码核实)**:①tauri-plugin-log v2 `TargetKind::Webview` 方向=Rust 日志→webview 控制台显示,**不捕获**前端 console——UI console 汇入的正路=JS 侧劫持 console 调插件 JS API(官方文档 forwardConsole 模式),需 capability `log:default`;`attachConsole()` 是反向订阅(不需要,弃)。②plugin **无按天轮转**:仅按大小(KeepAll/KeepOne/KeepSome,默认 max_file_size=40KB 过小必调)——「保留 7 天」由 KeepAll+归档名时间戳(`shell_YYYY-MM-DD_HH-MM-SS.log`,默认 UTC)自清实现。③壳已有 sidecar respawn(指数退避 1→16s、上限 5 次、`sidecar://state` 事件,main.rs:238-297)——崩溃自动重启后新 sidecar 回填即把崩溃前日志拉回日志屏,冷回填价值坐实。

条目统一形状(=今天环形条目超集):`{"ts": ISO-UTC, "run_id": int|null, "stream": "stdout"|"stderr", "line": str, "proc": "sidecar"|"cli"|"cron"|"vision"}`——ring 条目另带内存序 `seq`(仅 ring 内存概念,**文件行不含 seq**:多进程(sidecar/cron CLI/手动 CLI)并发 append 同一 JSONL 时 seq 各进程独立必冲突;回填时由模块按读入顺序重发 seq,单调性恢复)。**并发 append 声明**:同日文件多进程并发写,单行单次 write + `O_APPEND`(POSIX 行级原子),单行上限约束 64KB(逐行转发天然远小);UI/壳行落 shell 文件为插件文本格式,不进 ring;进日志屏属后续可选项,非目标。

## 1. 模块本体:`src/myssia/log.py`(R0)

公开面(名字直白,主人命名偏好):

```python
CAPACITY = 4000            # 环形帽(沿 entry.py:503 现值)
RETENTION_DAYS = 7
BACKFILL_BUDGET = 2000     # 冷回填预算,帽的一半给当期流留量

def configure(*, mode: Literal["human","json","serve"], data_root: Path | None,
              ring: bool = False, proc: str = "cli") -> None   # 单前缀 myssia(决议③),prefix 参数不设
    # 幂等:先摘自己上次的 handler 再挂(force 语义由模块自持)
def ring_snapshot(run_id: int | None = None, lines: int = ...) -> list[dict]
def stream_line(run_id: int | None, stream: str, line: str) -> dict   # 子进程行→同一漏斗,返回条目供协议事件发射
def backfill(data_root: Path) -> list[dict]   # serve 启动盘尾回填,seed 环形+重发 seq
def suspend_stderr() / resume_stderr()   # _cli_json 内嵌调用窗口用(见 §3)
```

组件:

- **seq 单源**:装 `logging.setLogRecordFactory` 盖章——每条 record 生成时发 seq(模块计数器+锁,进程内单调)。ring 与文件两 handler 读同一 `record.seq` 天然一致;**文件行不落 seq**(跨进程必冲突,见 §0),回填时按读入顺序重发新 seq。
- **RingHandler(logging.Handler)**:record → 环形条目 append(run_id/stream 从 `extra` 注入的属性读,缺省 `None/"stderr"`);`ring_snapshot` 供 `logs.tail`。
- **JsonlFileHandler**:惰性打开当日文件、每行 flush、本地日变更换文件;**降级(R6)**:首错向 ring(不经文件,防递归)append 一条提示并置永久禁用,绝不向上抛;**自举细节**:override `handleError()`——logging 默认把 handler 异常打到 stderr(装机件无人接收且会刷),降级态下必须静默,日志模块自身故障不得经 logging 通路放大。
- **为什么不用 stdlib `TimedRotatingFileHandler`**(高星参考纪律的对照结论):它的轮转=**rename** 当前文件——多进程并发(cron CLI 子进程与 sidecar serve 同写当日文件,§0)下,一进程 rename 时另一进程仍持旧 fd 继续写被改名的文件,丢行;date-in-filename + `O_APPEND` 每-进程-自开当日文件(无 rename)才是多进程安全形态(multilog/timestamped TTY 日志同款模式)。手写面因此最小且必要。
- **stderr handler**:格式沿 CLI 现状 `%(asctime)s %(levelname)s %(name)s: %(message)s`;serve/json 模式 WARNING(对齐现契约,INFO 子进程行不重复上进程 stderr)。
- `stream_line`:`logging.getLogger("myssia.stream").info(line, extra={"run_id":…, "stream":…, "proc":…})` → 三 handler 一次走完(ring+盘必得;stderr 因 INFO 不过 WARNING 门——与今天子进程行只进 ring+事件的现状一致)。**返回条目**给调用方(entry.py pump)发射协议 `type:"log"` 事件——协议事件仍属 sidecar 层,不进模块。
- **协议事件发射点不变声明**:今天只有 `_pump_stream` 路径发 `type:"log"` 事件(run 子进程/vision 改管道后的子进程行),`_cli_json` 行只进 ring 不发事件——统一后发射点集合与现状逐点相同,不新增不删减(B6 事实)。

### 1.1 容量预算(量级自证)

- 单跑次日志行数≈几百行(WARNING 收敛后 INFO 流为主);cron 假设 10 job×每日 6 跑≈60 跑/日 + 手动跑次——**当日 myssia-*.jsonl 量级 ~1-5MB 封顶**(单行均值 <1KB);7 天保留总占用 <35MB,桌面件无感。
- 壳/ UI 侧:plugin max_file_size=5MB×KeepAll 归档,7 天自清——同量级。
- ring 4000 帽即流量上界的既有标尺(今天环形就是这个量),预算不构成架构约束。

### 1.2 测试隔离(批0 测试纪律)

- 模块测试 fixture 必须:①保存/恢复 `logging.root.handlers` 与 `logging.Logger.manager.loggerDict` 状态;②保存/恢复 LogRecordFactory(模块装的工厂要能卸,`setLogRecordFactory(None)` 复位);③monkeypatch 日期函数注入跨天;④tmp_path 作 data_root,断言零真实数据根触碰。
- entry.py 集成测试沿 tests/desktop/ 既有 MYIA_HOME 沙箱模式。

## 2. 入口路由(R1)

| 入口 | 改造 |
|------|------|
| `cli.py` `_configure_logging` | 退役改薄壳:转调 `myssia.log.configure(mode=…, data_root=<既有 home 解析>, proc="cli")`。--json 收敛 WARNING 语义由 mode 吸收。**落盘条件(决议②)**:仅 `MYIA_HOME` 已设→`<MYIA_HOME>/logs`;未设→`data_root=None` 仅 stderr(终端可见,防 logs/ 建进仓库——games jobs.json 同源坑)。 |
| sidecar serve(entry.py) | 启动处 `configure(mode="serve", data_root=<serve 上下文 home>, ring=True, proc="sidecar")` + `backfill(home)`;`_LOG_RING`/`_LOG_SEQ`/`_ring_append` **退役**,改 import 模块(`_m_logs_tail`→`ring_snapshot`;pump/`_cli_json`/安装远取日志→`stream_line`)。 |
| cron | sidecar 内线程形态自动继承 root 配置;独立 `myssia cron serve` 走 cli.py 统一入口(proc="cron")。`cron/output/*.log` 每跑次产物**不动**(产物非日志,边界)。 |
| vision server | **决议③并入**:`vision/server.py:247` 自带 open+`_rotate_log_if_huge` 退役;改 `configure(mode="serve", data_root=…, ring=False, proc="vision")` 落 myssia-*.jsonl;**子进程输出改管道**:原「子进程持 fd 写 vision-server.log」改为 stderr 管道→`_pump_stream` 同款→`stream_line(run_id=None, stream="stderr", proc="vision")` 入同文件(崩溃 traceback 不丢)。`vision-server.log` 退役,机械改面:5 处测试断言(tests/vision/test_vision_models_server.py:542,590,593,600,611)+spec(sidecar-protocol.md:63)+前端文案(vision-form.tsx:422);旧文件留原地不删。 |

数据根解析一律用各入口**既有**解析(cli 的 home 链、entry.py serve 上下文链、Rust `data_root(app)`)——模块只收 `data_root` 参数,不自己解析(单一职责,不引入第二套路径规则)。

## 3. `_cli_json` 互踩——以统一根治(R4)

今天的坑:cli_main 里 `_configure_logging(basicConfig force=True)` 会拆掉 root 上 sidecar 的 handler;CLI 日志又经 `redirect_stderr` 捕获后手动逐行 `_ring_append`。统一后:

- cli_main 调 `myssia.log.configure`(幂等重挂同款 handler 集)——**force 互踩从根上消失**,行在 cli_main 期间已由 ring handler 直入缓冲。
- `_cli_json` 的 `redirect_stderr` 捕获里只剩**裸 print**(非 logging 输出,如 entry.py:677)——若原样再逐行 `stream_line` 会与 ring handler 双份。修法:调用窗口 `suspend_stderr()`(摘 stderr handler)→ logging 行只走 ring+盘、不写被捕获 err;err 内容=裸 print,沿旧路 `stream_line` 入流保「CLI 诊断可见」语义;窗口结束 `resume_stderr()`。
- 测试双向钉死:①同一 CLI logging 行 ring 中恰一份;②裸 print 行仍入 ring;③窗口后 handler 集完整。

## 4. 保留策略(R2)

- `RETENTION_DAYS = 7` 常量,Python/Rust 各持一份(不加 UI/env 旋钮——非目标)。
- Python:`configure()` 时(即每进程启动)按 `myssia-*.jsonl` glob 清理超期文件(单前缀,决议③)。
- Rust:plugin 按大小轮转(KeepAll)产归档 `shell_YYYY-MM-DD_HH-MM-SS.log`;壳启动解析归档名时间戳,< 今天−7 天删除;活动 `shell.log` 永不动。
- **红线**:前缀 glob 钉死(`myssia-*.jsonl` / `shell_<时间戳>.log`),绝不整目录清理;测试负断言(cron/output/ 原样、升级场景旧 vision-server.log 留存不删)。

## 5. 冷启动回填(R5)

`backfill(data_root)` 在 serve 启动、home 解析后调用一次(不在 `_m_logs_tail` 内每请求读盘):

- 当日文件尾 + 不足预算时前一文件尾,预算 `BACKFILL_BUDGET=2000`;
- 只收完整可解析 JSONL 行,坏行跳过(崩溃截尾容忍);条目按读入顺序 seed 环形并**重发新 seq**(文件行无 seq,§0);proc 字段保留可辨「上一程是谁」;
- 任何异常(无文件/无目录/全坏行)静默通过=与现状全同。
- 协议 `logs.tail` params/result 形状零变化;前端 `screens/logs/` 零改动。
- 壳 respawn 事实(main.rs:238-297)加持:sidecar 崩溃→壳指数退避重启→新进程回填把崩溃前日志拉回日志屏——崩溃现场 App 内即可翻看。

## 6. Rust 壳 + UI 日志面(AC4/AC10)

选型 `tauri-plugin-log` 2.10(官方 tauri-plugins-workspace,链接者路线;备选=自写 append 模块,弃)。**Rust 壳与 UI 共用同一 plugin 实例**——UI 的 JS API 调用最终也流经同一 targets:

```rust
tauri_plugin_log::Builder::new()
    .targets([Folder { path: data_root(app).join("logs"), file_name: Some("shell") }, Stdout])
    .level(Info)
    .max_file_size(5MB)                      // 默认 40KB 过小,必调
    .rotation_strategy(KeepAll)              // 归档名带时间戳;>7 天由壳启动自清(§4)
    .timezone_strategy(UseLocal)             // 归档名/时间戳本地时区(注意:该调用会重置 formatter,须在其后再设 format)
```

- `logs` 目录创建失败→降级仅 Stdout,不阻启动。
- **壳侧改造点**:main.rs 18 + pyenv_components.rs 16 + pyenv_install.rs 10 处 `println!/eprintln!` → `log::info!/warn!/error!` 按语义分级;**重点** main.rs:142 sidecar stderr pump → `log::warn!`(sidecar 崩溃 traceback 装机件唯一落点);respawn 链路(schedule_respawn/backoff/超限 dead 事件,main.rs:238-297)全程 info/warn 留痕。
- **UI 侧(AC10,新增件;机制按事实勘误①修正)**:
  - `desktop/ui-src/src/lib/log.ts`:**劫持 console**(官方 forwardConsole 模式——覆写 `console.log/info/warn/error` 原样执行后调 `@tauri-apps/plugin-log` JS API,Rust 端记 target=`webview` 流入 Folder 文件);注册 `window.onerror`+`unhandledrejection` → 前缀化(来源+消息+堆栈首行)同路落盘;App 启动调用一次。**不用** `attachConsole`(那是反向:Rust 日志显示到 webview 控制台)。
  - React ErrorBoundary(根级包裹):`componentDidCatch` → 劫持后的 `console.error`(崩溃组件+错误+堆栈首行)落盘;回退 UI 极简(错误文本+重新加载钮,无花活)。
  - updater 埋点(updater-card.tsx):检查开始/结果、下载进度里程碑、安装请求、失败——`console.info/warn/error` 前缀 `updater:`(经劫持链落盘);事件流既有 UI 不改,只加埋点。
  - capabilities 增 `log:default`(JS invoke `plugin:log|log` 的唯一权限面);CSP 不涉(走 Tauri IPC 非外链)。
- 产名事实:活动文件恒 `shell.log`,轮转归档 `shell_YYYY-MM-DD_HH-MM-SS.log`——清理 glob=该前缀解析时间戳,实现批真名复核。

## 7. 兼容性与安全

- 协议零方法增删、零形状变化;`sidecar-protocol.md` 仅补回填行为描述。
- 装机包 resources/锁/plugins.lock.json 全不涉;`logs/` 在运行期数据根。
- 凭据红线:三路同源零展开零新增字段,上游脱敏(secrets.py)已管;测试加负断言(env 值样张不出现在文件)。
- MYIA_HOME 沙箱:全走既有解析;测试一律 tmp 沙箱,不碰真实数据根。

## 8. 回滚

纯增量+收敛改造:新模块 1 文件;入口改造四处(每处小);`_ring_append` 退役触及 entry.py 多调用点(impact 前置,见 implement.md)。批次独立 commit,任批 revert 即回。遗留 `logs/*.jsonl` 死文件人工删。无数据迁移、无协议版本耦合。

## 9. 风险与已知取舍

| 风险 | 评估 | 对策 |
|------|------|------|
| `_ring_append` 退役波及 entry.py 多调用点 | 改造面最大的单点(664/753/1359/3148/3317 等行) | 批1 前 `gitnexus impact -r shishi _ring_append` 全列;`stream_line` 返回条目保持调用点形状近似,逐点机械替换+定向测试 |
| LogRecordFactory 全局单例与多入口重复 configure | 幂等 configure+工厂只装一次 | 模块级安装守卫;测试双 configure 断言 handler 集不翻倍 |
| handler 链内做盘 I/O(锁内) | 桌面件量级低(环形 4000 帽即流量标尺) | 单句柄复用+每行 flush;实测瓶颈再改异步队列(设计外留档) |
| `_cli_json` 双份/漏行 | 统一根治+窗口 suspend 双保险 | AC3 三向测试钉死 |
| tauri-plugin-log 产名与清理 glob | 已核实:活动 `shell.log`+归档 `shell_<时间戳>.log` | 清理 glob 按此钉;实现批真名复核一次 |
| UI 日志量(console 转发全量) | 前端现状 console 仅 4 处,量级低 | attachConsole 默认级别即可;若噪音超预期加级别过滤(实现批裁量) |
| ErrorBoundary 回退 UI 引入新视觉 | 极简文本+重载钮,无设计面 | 截图入 evidence,主人过目;审美裁决留主人 |
| 回填顶掉当期实时日志 | 预算 2000 < 帽 4000 | 减半留量;测试断言回填后 ring 长度 ≤ 帽 |
