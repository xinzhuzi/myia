# 日志约定

## 结构化优先

- 每次 run 输出 run 级与步骤级记录:耗时、条目数、**skip 原因**(变更指纹 unchanged / dedup 拦截 / robots 违规)——skip 是正常路径,必须可见
- 源健康度事件(引擎选择、降级发生、失败分类)都落日志与 store,doctor 汇总
- `--json` 模式下运行结果为机器可读 JSON;人类可读输出与 JSON 输出并存,同一信息两种皮
- 日志不含凭据值(引用名可以,展开后的值禁止);`--dry-run` 全链执行但不推送

## 级别语义

- ERROR:需要人/agent 介入(源 dead、配置错)
- WARNING:自动恢复的异常(降级发生、预算触顶)
- INFO:run/步骤生命周期;DEBUG:提取明细、关键词命中追溯

## 统一模块与落盘(10-07-unified-logging)

**模块单点** `src/myssia/log.py`:`configure(mode, data_root, ring, proc)` 幂等配置——先摘自己标记的 handler 再挂,`force=True` 互踢模式禁用(重复 configure 不拆他人 handler)。三 handler 同挂 root:stderr(mode 分级:human=INFO / json·serve=WARNING)+ 环形(`CAPACITY=4000` 帽,UI 数据面 `logs.tail` 唯一来源)+ JSONL 文件。数据根不在模块内解析:各入口用既有解析后传 `data_root`,不引入第二套路径规则。子进程行经 `stream_line(run_id, stream, line, proc)` 入同一漏斗并返回条目供协议事件发射;`suspend_stderr`/`resume_stderr` 供内嵌 CLI 调用窗口摘 stderr handler 防双份。

**入口路由**(五入口全走 configure;proc 词表 `cli`/`cron`/`sidecar`/`vision`/`feishu_callback`):CLI(`cli.py` `_configure_logging` 薄壳转调,`proc` 关键字参缺省 `"cli"`——其余调用点零改动)落盘条件=仅 `MYIA_HOME` 已设 → `<MYIA_HOME>/logs`,未设 → `data_root=None` 仅 stderr(防 logs/ 建进仓库);sidecar serve(`entry.py`)`ring=True, proc="sidecar"` + 启动盘尾回填(见下);cron 两形态——serve 内线程零代码继承 root 配置,独立 `myssia cron serve` 走 cli.py 入口 `proc="cron"`(10-07-logs-restart-visibility R2:独立常驻宿主行可辨来路,dispatch 前后无日志行发出无错标窗口;其余 cron 子命令仍 `"cli"`);vision server(`vision/server.py`)`proc="vision"` 落同一前缀文件(vision-server.log 与自带轮转退役,旧文件留原地不删);feishu_callback(`python -m myssia.push.feishu_callback` 独立进程)经 `configure(mode="serve", data_root=MYIA_HOME 感知解析, ring=False, proc="feishu_callback")`——`basicConfig` 退役,裸跑 = 仅 stderr(WARNING 门,决议②口径不在 CWD 建 logs/),`MYIA_HOME` 在场落 `<home>/logs/myssia-*.jsonl` 行 proc 可辨,ThreadingHTTPServer 请求线程继承 root 配置零额外接线(10-07-logs-restart-visibility R3)。

**文件形状**:数据根 `logs/myssia-YYYYMMDD.jsonl` 单前缀单文件,条目 `{ts, run_id, stream, line, proc}`;文件行**不落 seq**——seq 是环形内存概念(LogRecordFactory 盖章,进程内单调),多进程并发 append 同一文件时各进程计数器独立必冲突;回填时按读入顺序重发恢复单调。单行上限 64KB 截断(单行单次 write + `O_APPEND` 的行级原子前提)。

**轮转保留**:按天 = date-in-filename + `O_APPEND` 每进程自开当日文件、**无 rename**(stdlib `TimedRotatingFileHandler` 的 rename 轮转在多进程同写场景丢行,不用——cron CLI 子进程与 sidecar serve 同写当日文件是常态);`RETENTION_DAYS=7`,configure 时按 `myssia-*.jsonl` 单前缀 glob 清超期(名形不合/假日期跳过),**绝不整目录清理**(cron 产物/壳归档零触碰);同一清理窗纳入中继 sink `vision-server.out|.err`——无日期名按 mtime 折算本地日判超期(10-07-logs-restart-visibility low②),退役旧件 `vision-server.log` 仍留原地不删。

**降级语义**:文件路首错 → 向环形追加一条提示并永久禁用,主链不破、绝不向上抛;`handleError` 静默 override——日志模块自身故障不经 logging 通路放大。

**冷启动回填**:`backfill(data_root)` 在 serve 启动、home 解析后调用一次(不在每请求读盘)——当日文件尾+不足预算补前一文件尾,预算 `BACKFILL_BUDGET=2000`(帽的一半,当期实时流留量);只收完整可解析 JSONL 行,坏行跳过;条目按读入顺序 seed 环形并重发新 seq(proc 字段保留可辨上一程是谁);任何异常静默通过。壳 respawn 后崩溃前日志因此可达日志屏。

**凭据红线沿用**:上方「日志不含凭据值」对文件路同样成立——测试负断言钉死(env 值样张不出现在落盘文件)。

## 标题级采集日志(10-19-runlog-item-titles)

**动机**:引擎级日志按契约只记形状(「形状级,不记内容」),run 仪表能看到 `items=N` 却看不到「N 是哪几条」——漏发/错发归因只能猜。pipeline 采集咽喉(`_stage_fetch` 的 zip 源循环,「采集完成」行旁)新增一条标题级 INFO 行,一处覆盖全部引擎(含降级链最终胜出者),不动引擎级 9 处形状日志。

**形态**:`采集条目标题 source=%s items=%s titles=%s`(logger 用 %-style),每源每轮至多一条;`titles=` 为编号预览——外部标题先折叠空白(原始 `\n`/`\r`/`\t`/全角空格经 `" ".join(text.split())` 全折叠为单空格,JSONL 单行性即多进程 `O_APPEND` 行级原子前提不破),再按 60 字符截断加省略号,封顶前 10 条;条数由 `items=` 如实另报。10 条+编号最坏 <2KB UTF-8,距 64KB 行帽(`_MAX_LINE_BYTES`)两个数量级,`_cap_line` 字节级截断兜底不触发。源本轮零条目不追加该行(零噪音)。

**边界**:只记标题,永不记正文与 URL。新增曝光面 = 取到但未入库(指纹 skip 全旧/分类滤除)条目的标题也会随 JSONL 落盘并按 `RETENTION_DAYS=7` 保留——「采到过什么」有迹可查正是本留痕的目的,属已授权折中。与 dedup 契约不冲突:dedup 键永不 `{title}` 指纹(schema 守卫),日志记标题 ≠ 去重键用标题。
