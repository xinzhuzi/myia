# 统一日志模块:myssia.log 单点配置 + 全入口统一 + 落盘轮转保留 + 壳日志

## Goal

主人 2026-10-07 三连令:「落实到trellis任务」→「**日志模块必须有,统一起来**」→「**UI日志,后端日志,等等关键日志都必须有**」。起因=当轮诊断:MYIA 日志面散装——各处都在打日志,但没有一个统一的日志模块,且**持久化缺失**(App 退出/崩溃后日志清零,装机件上壳日志无人接收),**UI 层零日志**(白屏/渲染崩溃无痕)。本任务交付统一日志模块 `src/myssia/log.py`(全 Python 入口单点配置,stderr/环形缓冲/JSONL 落盘三路同源)+ Rust 壳与 **UI(webview)日志**经官方 `tauri-plugin-log` 汇入同一 `logs/` 目录——各层关键日志逐层对账「必须有」。

## grill 决议(2026-10-07 轮 1,主人令「按推荐」)

- **①全量落盘**:CLI/cron 跑次日志全量入统一流 `logs/myssia-*.jsonl`,与 `cron/output/*.log` 双份持久化接受(「都必须有」语义;7 天保留兜体积;产物语义不动)。
- **②CLI 落盘条件**:仅 `MYIA_HOME` 已设时落 `<MYIA_HOME>/logs`;裸 repo 终端跑=stderr-only(沿 `_cron_default_db`「无 env 终端行为不变」判例,防 `logs/` 建进仓库——games jobs.json 同源坑)。
- **③vision 归并**:并入 `myssia-*.jsonl`(proc=vision),**退役 `vision-server.log`**——机械改面:5 处测试断言(tests/vision/test_vision_models_server.py:542,590,593,600,611)+spec 一行(sidecar-protocol.md:63)+前端文案(vision-form.tsx:422);旧文件升级场景留存原地不删。
- **④UI 错误不进日志屏(首版)**:UI console/错误兜底/updater 埋点只落 shell 文件;ErrorBoundary 回退 UI 即时可见;进屏牵协议语义扩展,留后续可选。
- **⑤壳日志格式**:沿 tauri-plugin-log 默认 `[日期][时刻][target][LEVEL] msg`(target 自辨来源:壳 crate/`webview`=UI),不自造 format。
- **⑥默认值包**:保留 7 天/回填预算 2000 行/UI console 全劫持(log/info/warn/error)/ErrorBoundary 极简回退(错误文本+重载钮,截图入 evidence 请主人过目)/模块名 `src/myssia/log.py`/测试落位 `tests/test_log.py`/shell 单文件上限 5MB。

## 现状凭据(2026-10-07 亲测)

**散装的六块**:

| 块 | 现状 | 凭据 |
|----|------|------|
| Python 模块层 | ~50 模块各自 `logging.getLogger` | 各引擎/push/cron/telegram 面 |
| CLI 入口 | ad-hoc `basicConfig`(force=True,stderr,INFO/WARNING 按 --json) | `src/myssia/cli.py:1311` `_configure_logging` |
| sidecar serve | **零 logging 配置**:模块 WARNING+ 走 lastResort→进程 stderr→壳 `eprintln!`→装机件丢弃;崩溃 traceback 同路 | entry.py 无 basicConfig/getLogger;`main.rs:142` |
| 内存环形缓冲 | 4000 行,唯一 UI 日志面,重启即失 | `desktop/entry.py:503` `LOG_RING_CAPACITY` |
| vision server | 自带 open+轮转一只文件 | `src/myssia/vision/server.py:247` |
| Rust 壳 | 零日志框架,仅裸 `println!/eprintln!` | Cargo.toml 无 log/tracing/plugin;main.rs 18 处等 |
| **前端 UI(webview)** | console.* 全前端仅 4 处;**零错误兜底**(无 onerror/unhandledrejection/ErrorBoundary);updater 流(updater-card.tsx)无日志埋点——白屏/渲染崩溃/更新失败零痕迹 | rg 实测 2026-10-07 |

装机件数据根 `~/Library/Application Support/MYIA/` 无 `logs/` 目录;已有持久面仅 cron 每跑次独立文件(`cron/output/<job>/*.log`)、`vision-server.log`、`myia.db` 结构化台账。

## Requirements

- **R0 统一日志模块(核心)**:新建 `src/myssia/log.py`——单点 `configure()`;stderr handler(mode 分级:human=INFO / json·serve=WARNING)、环形缓冲 handler、JSONL 文件 handler 同挂 root;条目统一形状 `{seq, ts, run_id, stream, line, proc}`;seq 单源单调盖章。
- **R1 全 Python 入口统一路由**:CLI(`cli.py` `_configure_logging` 退役改薄壳或删除;落盘条件按决议②)、sidecar serve(entry.py 启动 configure)、cron(独立 `cron serve` 进程与 sidecar 内线程两形态)、vision server(经统一模块,**按决议③并入 myssia 单前缀,退役 vision-server.log**)——配置后 root handler 集一致,格式/落盘/轮转/保留同一套规则。
- **R2 落盘与保留**:数据根 `logs/myssia-YYYYMMDD.jsonl` 按天轮转(Python 单前缀单文件,proc 字段分进程;决议③),Rust 壳同目录(`shell.log`+归档,决议⑤格式);Python 侧保留 7 天按文件名日期,壳侧按归档名时间戳;清理 glob 前缀钉死,不伤邻居(cron/output/、旧 vision-server.log 留存不删)。
- **R3 子进程日志流同漏斗**:sidecar run 子进程与插件安装/远取的逐行输出(run_id/stream)经同一 logging 漏斗入 ring+盘;协议 `type:"log"` 实时事件路径不变。
- **R4 sidecar 自身模块日志入流**:serve 期模块 WARNING+ 进 ring+盘;`_cli_json` 内嵌 CLI 调用不得产生重复行或丢 handler(force=True 互踩以「CLI 也走统一模块」根治)。
- **R5 冷启动回填**:App 重启后 `logs.tail` 从盘尾回填(预算 2000 行,环形 4000 帽不破,seq 续接单调);前端零改动。
- **R6 安全红线与降级**:落盘内容不展开凭据(沿 `.trellis/spec/python/logging.md`);文件/目录不可写时静默降级不破主链(首错入 ring 一条提示后永久静默)。
- **R7 兼容**:sidecar 协议(`logs.tail` 请求/响应形状)不变;前端既有屏零改(R8 只新增日志兜底件与埋点);装机包 resources/锁不涉;MYIA_HOME 沙箱语义沿既有优先级链;旧 `vision-server.log` 留原地不迁移,cron 每跑次产物文件保留(跑次产物非日志,边界入档)。
- **R8 UI 日志必须有**:webview 前端按官方 forwardConsole 模式**劫持 console.*** 调 `@tauri-apps/plugin-log` JS API 汇入同一 targets→shell 文件(grill 勘误:attachConsole 是反向订阅,弃);全局错误兜底 `window.onerror`+`unhandledrejection`+React ErrorBoundary(极简回退:错误文本+重载钮,决议⑥)——渲染崩溃/白屏留痕;updater 流(检查/下载/安装/失败)埋点;**不进日志屏(决议④)**。
- **R9 关键日志面对账**:各层「必须有」逐层核验(管线/引擎/推送、sidecar 协议+子进程流+插件安装、cron、vision、壳生命周期+pyenv、sidecar 崩溃 stderr、UI console+错误兜底+updater)——每层落点与凭据(测试或装机)入档对账表,不许有「无日志层」。

### 非目标

- 不改日志内容与级别语义(12b7f45/43683c9 已调优面不动)。
- 不做日志远程上报/集中采集/UI 新查看面(UI 日志入落盘文件,不进日志屏——决议④,进屏属后续可选项)。
- 不统一 cron 每跑次输出文件形态(是产物不是日志)。

### 关键日志面清单(R9 对账表,AC11 逐层勾)

| # | 层 | 关键事件 | 落点 | 凭据 |
|---|-----|---------|------|------|
| 1 | Python 管线/引擎/推送 | run 生命周期/降级/失败分类/skip 原因 | myssia-*.jsonl | 测试(批0/1) |
| 2 | sidecar 协议+子进程流 | run 逐行输出/插件安装/远取诊断 | myssia-*.jsonl+ring | 测试(批1) |
| 3 | cron | serve 心跳/跑次启停/异常 | myssia-*.jsonl+cron/output | 测试(批1 回归) |
| 4 | vision server | 起停/模型下载/异常 | myssia-*.jsonl(proc=vision;决议③) | 测试(批1) |
| 5 | Rust 壳生命周期 | 启动/sidecar spawn 失败/pyenv 安装自检 | shell-*(plugin) | 壳单测(批2) |
| 6 | sidecar 崩溃 stderr | traceback 尾部 | shell-*(warn) | 壳单测(批2) |
| 7 | UI console+错误兜底 | console.*/onerror/unhandledrejection/ErrorBoundary | shell-*(Webview target) | vitest(批2) |
| 8 | updater 流 | 检查/下载/安装/失败 | shell-*(UI 埋点) | vitest+装机(批2/4) |

## Acceptance Criteria

- [ ] AC0 统一模块+全入口路由:`src/myssia/log.py` 存在;cli/sidecar serve/cron serve/vision server 四入口经它配置;测试断言配置后 root handler 集一致(形状断言);cli.py `_configure_logging` 与 vision 自带轮转代码退役;**vision-server.log 退役改面(5 测试断言+spec 一行+前端文案)全落(决议③)**。
- [ ] AC1 落盘保真:环形条目逐行入 `<MYIA_HOME>/logs/myssia-YYYYMMDD.jsonl`(JSONL 字段 ts/run_id/stream/line/proc 与条目一致;文件行不含 seq——grill 勘误);跨天轮转;vision 行 proc=vision 同文件(决议③);CLI 落盘仅当 MYIA_HOME 已设,裸跑 stderr-only(决议②)。
- [ ] AC2 UI 手动跑次持久:run.start 跑次日志(run_id 保留)在新 serve 实例后仍可从文件读到。
- [ ] AC3 模块日志入流+互踩根治:serve 期模块 WARNING+ 进 ring+盘;`_cli_json` 期间同一 CLI 日志行 ring 中**恰一份**、调用后 handler 存活(force 互踩不再可能——测试钉死)。
- [ ] AC4 壳日志落盘:壳起后数据根 `logs/` 出现壳日志文件;生命周期事件(至少 sidecar 拉起失败、pyenv 安装/自检失败路径)有痕;sidecar stderr 行(含崩溃尾部)由壳留痕。
- [ ] AC5 保留策略:>7 天旧文件启动清理被删;7 天内文件与邻居(cron/output/、旧 vision-server.log)原样保留(Python/Rust 两侧各测)。
- [ ] AC6 冷启动回填:新 serve 实例 `logs.tail` 从盘尾回填,预算内、seq 单调续接、环形帽不破;无文件时行为与现状全同(零回归)。
- [ ] AC7 降级:数据根不可写时主链不破、协议应答正常,首错一条 ring 提示后不再刷屏。
- [ ] AC8 门禁全绿:全量 pytest / ruff / `cargo check --locked`+壳单测 / vitest 零新红;plugins 锁门禁不涉。
- [ ] AC9 装机件亲验:换装后真机跑一次采集,数据根出现当日 myssia+壳(+vision 若触发)日志文件,内容可读、重启 App 后仍在且日志屏可翻;截图留证(evidence 不入 git)。
- [ ] AC10 UI 日志落盘:console 劫持(官方 forwardConsole 模式)后 webview console.* 落 shell 文件(target=webview);`window.onerror`/`unhandledrejection` 兜底注册并落盘;React ErrorBoundary 渲染崩溃留痕+极简回退(错误文本+重载钮);updater 检查/下载/安装/失败事件埋点落盘;**不进日志屏(决议④)**;vitest 覆盖兜底模块与 ErrorBoundary。
- [ ] AC11 关键面对账表:prd §关键面清单每层「落点+凭据(测试/装机)」逐层勾——无「无日志层」存续。

## 过程(执行流水,回填位)

- (空位;执行由此续填)

## 结果(验收回执,完工填)

- (空位)
