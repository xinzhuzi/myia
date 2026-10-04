# 屏布局与交互规格 + 测试用例清单(cron-ui)

> 布局=蓝本 CronPage 逐段对位(hermes-cronpage-map.md);token/基件守 frontend-ui.md;列序与区域如下为实现契约。

## 1. 屏区域(自上而下)

```
┌────────────────────────────────────────────────┐
│ A 活性条(常驻一行,三态:                     │
│   正常=灰字「ticker 活跃 · 下次 <时刻> · N 个 job · <data_root 灰字小字>」(Q3 数据根可见,│
│         一眼自解释「CLI 在别处建的 job 为什么看不见」); │
│   僵死=黄条 data-testid=cron-stale(判据 !ticker_alive||heartbeat_age_seconds>180); │
│   急停=红条 data-testid=cron-estopped+「恢复全部」按钮+注记一句 │
│         「急停仅暂停调度,单 job 操作仍可用」(Q4,忠实后端语义)) │
│   右侧常驻:「急停全部」红钮(确认 Dialog)+ 手动「刷新」│
├────────────────────────────────────────────────┤
│ B notice 横幅(有则显示,messaging 形态;事件与动作共用) │
├────────────────────────────────────────────────┤
│ C 工具行:「新建定时任务」主按钮 + 「显示暂停/终态」Switch(all)│
├────────────────────────────────────────────────┤
│ D job 表(table 基件):见列定义;行=可展开        │
│   展开体=cron.runs(默认 limit 10)+摘要行       │
├────────────────────────────────────────────────┤
│ E 空态:无 job 时引导卡(「创建第一个定时任务」+一行 CLI 对照) │
└────────────────────────────────────────────────┘
```

## 2. 表列定义(D)

| 列 | 宽 | 渲染 |
|---|---|---|
| 展开 ⇱ | icon | 整行 button aria-expanded( logs 先例;与动作钮兄弟不可嵌套) |
| 名称 | 弹性 | name(缺省截断 40,DeleteConfirm 同款 truncate) |
| 排程 | ~160 | schedule_display(人话直读) |
| 下次运行 | ~150 | next_run_at 本地化;**逾期红标**=now>next+15min(text-destructive+标「逾期」);终态/暂停=「—」 |
| 上次状态 | ~110 | badge 四态:ok=success/failed=destructive/delivery_failed·skipped_busy=warning/paused(或 state=paused)=中性;state=completed=灰「已完结」 |
| 投递 | ~120 | deliver(截断) |
| 次数 | ~80 | repeat:completed/times,∞=times null 显示「∞」 |
| 动作 | ~200 | 立即运行(**排队语义 Q1**:点击→notice「已排队,≤60 秒内开始」+行短时「已排队」态;completed 事件落地刷新——非 spinner 死等)/暂停/恢复/编辑/删除(删除经确认) |

## 3. 创建/编辑 Dialog(F4)

- 承载:dialog 基件;表单分三组——**chips 行**(五种,点击填 schedule 输入框)/主字段(schedule 手输、category 选择器)/**高级折叠**(deliver/failure_deliver/repeat/timezone/config/run_timeout/dry_run Switch);
- category 选择器:select 基件,数据=yaml.list;坏文件(parse_ok:false)项禁选带「解析失败」后缀;末项「手输路径…」切换 input;
- 错误回显:submit 失败把 ProtocolError message 原样入 notice/error 行(parse 文案/category 校验);编辑零更新(cron_edit_no_changes)提示后关闭;
- 编辑预填:fromJob(cron-form.ts);schedule 变更后端重算 next_run_at,保存后刷新列表。

## 4. 事件/时钟

- 订阅:messaging 模式(cancelled+unlisten);cron.completed→notice(ok/error 按 ok 字段)+重拉 list;cron.skipped→notice(warning 文案「因运行占用跳过」)+重拉;
- **无 started 事件(grill 二 Q2 定案)**:自动触发的 job「正在跑」不做行级态——进行态仅在历史展开可见(executions `running` 行);手动触发的可见性=「已排队」行态至 completed;
- 本地时钟:1min setInterval **只重渲染逾期标**(useMemo 依赖 now state;此为唯一 interval,与「无轮询」不冲突——不取数);

## 5. 测试用例清单(cron-screen.test.tsx;传输层 mock+emitSidecarEvent)

| # | 用例 | 断言要点(AC 对应) |
|---|---|---|
| 1 | 渲染:列表全字段 | name/schedule_display/deliver/repeat 渲染(AC3) |
| 2 | 四态 badge 色 | ok→success 类、failed→destructive、delivery_failed→warning、paused→中性(AC3) |
| 3 | 逾期红标边界 | next=now-16min 红 / now-14min 不红 / paused 无(AC3) |
| 4 | all 切换 | all=true 时 list 携 all:true;终态行出现「已完结」(AC3) |
| 5 | 活性条三态 | 正常/僵死(heartbeat_age_seconds>180)/estopped 红条+恢复按钮(AC2) |
| 6 | 急停全部 | 红钮→确认 Dialog→invoke cron.pause {all:true}(AC5) |
| 7 | 创建提交形状 | chips 点击→schedule 值;选择器选 parse_ok 项→category 绝对路径;全字段 payload 断言(AC4) |
| 8 | 创建错误回显 | create 报 parse 错误→错误行含原文(AC4) |
| 9 | 选择器坏文件禁选 | parse_ok:false 项 disabled+「解析失败」;手输兜底可提交(AC4) |
| 10 | 编辑预填+部分更新 | 只改 deliver→edit 仅含 job+deliver(AC4) |
| 11 | 动作四件 | run/pause/resume invoke 形状;remove 先 window.confirm(AC5) |
| 12 | run 排队语义 | run 后 notice「已排队/≤60 秒」+行「已排队」态;completed 事件到刷新(AC5,grill 二 Q1) |
| 19 | estopped 下单 job 操作 | estopped 态仍可暂停/编辑单 job(后端语义,Q4);红条含注记文案(AC2/AC5) |
| 13 | 历史展开 | 首次展开 invoke runs{job,limit:10};摘要字段渲染;空态(AC6) |
| 14 | 事件驱动 | emitSidecarEvent(completed)→notice(name/status)+list 重拉(AC7) |
| 15 | skipped 事件 | 文案含「跳过」;重拉(AC7) |
| 16 | 手动刷新 | 按钮→list+status 双拉(AC7) |
| 17 | 零轮询 | 实现审查:无 fetch 型 setInterval(vi 断言 listen 只一次+时钟 tick 不触发 invoke)(AC7) |
| 18 | logs 涟漪 | logs/api eventToRow 对 cron 两事件产出 runId=null 系统行(AC7,可放 logs 测) |
