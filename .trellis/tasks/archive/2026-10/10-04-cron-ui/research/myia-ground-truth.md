# MYIA 地面真值(cron-ui 实现依据,2026-10-04 实读)

> 行号当日核实;每条都是实现者直接消费的形状。⚠️=对任务文档原稿的修正。

## 1. cron.* 九方法参数/返回(entry.py)

注册 `_HANDLERS` 4835-4843。公共:全部收可选 `db`(覆写,缺省=serve 上下文);`job` 引用=id 或名字,重名 `cron_ambiguous_job`(data.candidates)、未找到 `cron_job_not_found`(`_cron_resolve_job` 4485)。

| 方法 | 行 | params | 返回 |
|---|---|---|---|
| list | 4521 | `all`(bool 缺省 false) | `db,data_root,count,jobs` |
| create | 4536 | 必填 `schedule`/`category`;可选 `name`/`deliver`/`failure_deliver`/`timezone`/`config`/`paused_reason`/`repeat`(int)/`run_timeout`(正数秒)/`dry_run`/`paused` | `{job}` |
| edit | 4598 | `job` + 部分更新(同 create 族;`config`→存 `config_path` 绝对路径);零更新=`cron_edit_no_changes` | `{job}` |
| pause | 4643 | `job`+`reason`;或 `all:true`(急停,与 job 互斥) | `{job}` / `{estopped:true,marker}` |
| resume | 4664 | `job`+`at`(ISO 重挂);或 `all:true`(与 job/at 互斥) | `{job}` / `{estopped,cleared}` |
| run | 4698 | `job` | `{job}` |
| remove | 4710 | `job` | `{removed:true,job_id,name}` |
| status | 4721 | 仅公共 db | `db,data_root,ticker_alive,heartbeat_age_seconds,last_success_age_seconds,last_error,estopped,jobs_total,jobs_enabled,next_due_at` |
| runs | 4752 | `job`(可选过滤)/`limit`(缺省 20 钳 [1,500]) | `db,count,executions`(行含 `run_summary` 已解析;损坏=`{raw}`) |

**job dict**(myssia/cron/jobs.py 759-796 透传):`id/name/category(绝对)/schedule(dict)/schedule_display/repeat{times,completed}/enabled/state/paused_at/paused_reason/manual_run_at/created_at/next_run_at/last_run_at/last_status/last_error/last_delivery_error/failure_streak/deliver/origin/timezone` + 可选 `failure_deliver/db_path/config_path/run_timeout/dry_run`(显式才有)。

**executions 行**:executions.py 271-285:`id/job_id/source/status(claimed|running|completed|failed|unknown)/scheduled_instant/pid/process_start_time/claimed_at/started_at/finished_at/error/run_summary`(entry 侧换名)。

## 2. yaml.list(选择器数据源)

entry.py 2107-2118,零参数:`{plugins_dir, files:[{file(绝对路径), name, parse_ok, category_id, category_name, sources(int), error?}]}`;坏文件照样入列(`parse_ok:false`+`error{path,code,message}`)=**禁选带标的判据**;`*.yaml|*.yml` 字典序。

## 3. ⚠️ 事件联合缺口(原稿写错)

- Python 侧事件已实装(协议 v10,spec 注册表/事件契约在 sidecar-protocol.md 15/210 行);
- **TS `SidecarEvent` 联合(types.ts 1086-1094)现 8 员,不含 `cron.completed`/`cron.skipped`**——本任务要:两事件 interface(types.ts 992-1084 分段先例)+入联合;
- **涟漪**:logs 屏 `eventToRow` 尾部 `never` 穷尽守卫(logs/api.ts 262-267)编译期即报——须照 **alerts.fired 先例(249-261,runId=null 系统摘要行)**同步加分支;logs-screen 采集日志屏订阅处按 run 域过滤不续播(屏级过滤先例 399/407)。
- 订阅模式(messaging 811-837,本屏照此):`let unlisten; let cancelled=false; onSidecarEvent(e=>{if(e.type!=="cron.completed"&&e.type!=="cron.skipped")return; …}).then(un=>{cancelled?un():unlisten=un}); return ()=>{cancelled=true;unlisten?.()}`;共享入口 client.ts:237 `onSidecarEvent`(listen `sidecar://event`)。

## 4. ⚠️ toast 校准(原稿口径)

**库内无浮动 toast/无自动消失**——先例=屏内持久 notice 横幅:messaging-screen.tsx 73-76 `Notice{kind:"ok"|"error",text}` + 330-342 渲染(`role=alert|status`,ok/error 双配色,data-testid);每动作开头 `setNotice(null)` 覆盖式;事件驱动先例 alerts.fired→setNotice(816-819)。**本屏照抄 notice,不引新组件**。

## 5. types.ts 门面/镜像现状

- `SidecarProtocol` interface(types.ts 948-984)现 35 方法,**不含 cron.* 九行也不含 yaml.\***——补齐属 mirror 对账非协议变更;逐方法 Params/Result interface 分段定义(带与 entry.py 互指注释);
- 封装政策(client.ts 145-160):**新方法全入共享门面 `api`**(spec 注册表↔门面同源对账);yaml-editor 屏私有 api.ts 是明示历史例外——cron.* 走共享门面;
- 对账测试形态:**client.test.ts 19-31 逐方法 `expect(typeof api.xxx).toBe("function")` 批断言**(非总数计数)——加 cron 批。

## 6. 屏测 mock 两种形态(选型)

- **messaging 形态(本屏推荐,要测事件)**:mock `@tauri-apps/api/core`(invoke)+`api/event`(listen);`eventHandlers` 捕获+`emitSidecarEvent(payload)` 注入(messaging-screen.test.tsx 25-54);
- feed/logs 形态:mock `@/lib/api` 门面模块(importOriginal 部分覆写)。
- window.confirm spy 先例:yaml-editor-screen.test.tsx:268。

## 7. 列表/展开/table 先例

- **行内展开(logs 屏 317/423-434/657)**:`expanded:ReadonlySet<number>`+toggle(首次展开惰性拉取 `ensureTail`)+`loadedRunsRef/fetchingRef` 防重拉;组头整行 button+`aria-expanded/aria-controls`+ChevronDown 旋转;**折叠按钮与动作 Button 兄弟节点(button 不可嵌套)**;
- **table(sources-table.tsx)**:TanStack useReactTable(sorting/filter/pagination)+ui/table 基件+colgroup 定宽+行内操作经 `meta:{onToggle,...}` 注入;
- 蓝本状态色(H CronPage 526-532 STATUS_TONE):enabled/scheduled=success、paused=warning、error/completed=destructive——我们四态映射:ok→success、failed→destructive、delivery_failed/skipped_busy→warning、paused→中性灰。

## 8. ⚠️ 其他修正

- cron.create 的 `config` 参数(pools YAML)原 design 表单漏列——补进表单高级字段(可选);
- cron.status 返回键名为 `ticker_alive/heartbeat_age_seconds/...`(非草稿的 heartbeat_age/writer_alive 拼法)——types.ts 按上表逐字。
