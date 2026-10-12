# weixin 品类真拉验收(形状级证据;2026-10-13)

> 任务:10-12-weixin-feed-channel(review 态,实跑验收补全)。
> 本文全部证据为**形状级**:命令、退出码、计数、skip 码名、盖戳名、几何形态——
> 零消息文本(本轮实际也未产出任何消息载荷,见下)。

## 0. 一句话结论

**真拉三轮全部真实跑完(引擎 exit 0,run_id 102/103/104 入 runs 表),但每轮都是
结构化空态 `chat_title_unreadable`:微信主窗在册却未上屏(onscreen:false),
窗口服务器缓存帧近黑(mean_luma=28)→ OCR 零行 → 可见标题不可读(match=null)→
按引擎设计弃载荷不张冠李戴。itemsStored=0 如实。** 这是合法 skip 语义
(与 chat_not_open 同族),不是管线/引擎失败——静默铁律禁止验收方激活窗口,
故无法把会话带到可读态,如实终态。

## 1. 开局状态核验(全部本会话实跑)

| 项 | 命令/来源 | 结果 |
|---|---|---|
| 品类开关 | 数据根 `cron/jobs.json` | job `0e9f2daf2d6a` 微信监控 `*/30 * * * *` `enabled:true`(`last_run_at:null`,ticker 未跑过,本次为手动真拉) |
| 红线字段 | 数据根 `config/weixin.yaml` | `enrich.enabled:false` / `push:[]` / `retention:30d` 未动;与仓库 `config/weixin.yaml` 逐字节相同(diff IDENTICAL)。注:品类开关实为 cron 注册态,schema `CategoryConfig`(schema.py:1763)无顶层 enabled 字段 |
| 微信进程 | `pgrep -lf WeChat` | 主进程 pid 85172 在场 |
| 桥组件 | `ls ~/.myia/plugins/wechat-bridge/bin/` | `wechat-bridge` 在场 |
| 桥探针 | `bin/wechat-bridge --probe`(过滤) | state=degraded **仅因 localdb_key:unavailable**;wechat_process/ax_permission/screen_recording/main_window/localdb_storage 全 ok;版本 wechat 4.1.15 / bridge 0.3.1 |
| store 基线 | `sqlite3 <数据根>/myssia.db` | `items WHERE category='weixin'`=0;`source LIKE 'weixin-%'`=0;总 1722;`dedup_registry`=1747 |

## 2. 真拉命令与结果(三轮)

入口 = CLI 单品类面(cli.py:428 `myssia run <yaml> --once --json --db …`;
退出码映射 cli.py:1605 `_EXIT_BY_STATUS[status]`)。数据根 yaml + 数据根库
(判例:数据根是生产真相源;`--db` 缺省 cwd 相对,必须显式指数据根)。

```
/Users/zhengbingjin/Project/Github/MYIA/.venv/bin/myssia run \
  "$HOME/Library/Application Support/MYIA/config/weixin.yaml" \
  --once --json --db "$HOME/Library/Application Support/MYIA/myssia.db"
```

stdout 经形状过滤器(url/source/category/dedup_key/skip_reason/计数白名单,
title/content/metadata 全丢弃)后才可见;stderr 落 /tmp 用后即删(--json 模式
本就零日志输出,两轮 stderr 文件均 0 行)。

| 轮 | run_id | 引擎退出码 | status | 源报告 | items |
|---|---|---|---|---|---|
| 1(主拉) | 102 | 0(见轮 3 显式捕码) | success | `weixin-文件传输助手` skipped=true `chat_title_unreadable` item_count=0 | 0 |
| 2(去重轮,同参数立即) | 103 | — | success | 同上 | 0 |
| 3(退码轮) | 104 | **ENGINE_EXIT=0** | success | 同上 | 0 |

runs 表留存(sqlite3 只读):

```
102|success|chat_title_unreadable|0
103|success|chat_title_unreadable|0
104|success|chat_title_unreadable|0
```

fetch 阶段 `items_in=1` 口径注记 = 源数(pipeline.py:1381
`items_in=len(self.config.sources)`),非条目数。

## 3. 空态根因(桥直读诊断,输出同过滤器)

`bin/wechat-bridge messages read 文件传输助手 -k 50 --json`(经引擎同路径;
桥载荷只取 chat/ocr/capture 形状键):

- `chat`: `{requested_id:"文件传输助手", visible_title:null, match:null}` →
  引擎映射 `chat_title_unreadable`(engines/wechat_local.py:350-358,弃载荷)。
- `sessions list` 的 `window` 块:**window_id 81322,1920x1050,onscreen:false**
  (托盘/后台态;窗口在册 = 探针 main_window:ok 的真相)。
- `capture` 块:state=ok,3840x2100(2x),**mean_luma=28.0**(近黑缓存帧)。
- `ocr` 块:engine=vision,n_lines=0,elapsed 0.035s。

即:像素链机制本身工作正常(截图/OCR 全跑通),但窗口服务器为该离屏窗持有的
最后渲染帧近黑,读不出任何文本。桥 README 判例「ordered-off 托盘窗可出完整帧」
(2026-10-11 实测)在本机当前态不成立——帧内容是运行时事实,非桥缺陷。
**静默铁律(不点击/不滚动/不激活)禁止验收方把窗口带屏**,故无可再推进的
合法动作;想真出条目 = 主人把微信主窗(及目标会话)保持可见打开态,再等
cron */30 或手动重拉。

## 4. 入库核验(只读,零文本导出)

拉后与基线逐项比对:

```
weixin_items        | 0   (基线 0,零新增)
weixin_source_items | 0   (基线 0)
dedup_registry_total| 1747(基线 1747,零新键)
wx_anchor_urls      | 0   (wechat-local://chat/% 形态零条)
weixin_runs         | 3   (102/103/104,本轮新增的运行账目)
```

- **盖戳形态**:条目零入库,故库内无 `weixin-<会话名>` 盖戳实例;源声明名
  `weixin-文件传输助手`(= 将来条目的 source 盖戳值,runs 表 stats 内同值)。
- **url 锚形态**:`wechat-local://chat/<chat>#wx-<sha1[:16]>`(engines/wechat_local.py:154-166
  `anchor_url`);本轮零实例(零条目)。

## 5. 去重验证(如实)

同参数二轮(run_id 103)零新增成立——**但成因是结构化空态 skip,不是 dedup**:
零条目流过 dedup 阶段(items_in=0),`dedup_registry` 计数不变只证明「没有新键」,
不能证明「同锚沉默」。dedupSilent 判 **false/不可断言**,如实。待真载荷窗口
(主窗可见)后补验:同窗重读 → 同内容哈希锚 → 零新增。

## 6. 红线遵守记录

- 静默:零点击/零滚动/零激活;桥只读命令(probe/messages read/sessions list)。
- 私有数据:全链输出经形状过滤器;桥原始 JSON 未落任何持久文件(轮 3 临时
  /tmp 文件用后即删,且该轮 items 为空本就零文本);本档零消息文本。
- git:pathspec 仅提交本文件;他人 M 状态文件(desktop/src-tauri/*.rs 等)未碰。
- 仓库 config/ 未动;数据根侧只新增 runs 账目(拉取的固有副作用)。

## 7. cron 自动线验证(grill 轮 2 补全;2026-10-13 05:41-05:46)

### 7.1 死态取证(本会话实跑)

- `ticker_heartbeat` 冻结 `1791840226.616231 24140`(=05:23:46+08,宿主 pid 24140);
  `ps -p 24140` 无此进程(exit 1),`pgrep -fl ticker` 无命中——宿主已死,无人接管。
- `cron/ticker_writers/` 死属主文件 `…-24140` 残留在册;jobs.json mtime 05:18。
- 微信 job `0e9f2daf2d6a`(*/30,created_at 05:18:41)`next_run_at=05:30` 已过刻度
  而无宿主触发:`last_run_at=null`/`repeat.completed=0`/`last_status=null`——
  「品类已开启」的自动拉取效果当时为零(grill 属实)。
- 宿主归属事实(代码在案):ticker 常驻循环宿主=「`myssia cron serve`(CLI 监督
  守护线程)或桌面 sidecar(`desktop/entry.py` `_start_cron_ticker`,home 模式才起)」
  (src/myssia/cron/ticker.py:22-32;desktop/entry.py:5587);多宿主并存靠
  tick 文件锁 + fire claim 互斥(cli.py:571)。宿主死=调度停,是全局运维事实
  (6 个品类 job 全停),非微信渠道缺陷。

### 7.2 复活与自动触发(dev serve 代行,验后即停)

动作:05:44:09 起后台 `myssia cron serve --db <数据根>/myssia.db`
(仓库 .venv 二进制,与 §2 手动真拉同源;dispatch_gate=CLI 形传 None,不撞桌面单飞锁)。
`run_ticker_loop` 启动即首个 tick(ticker.py:212-217),微信 job 05:30 积压刻度
被判定 due(积压坍缩只补一发,tick.py:307)→ 自动派发子进程(serve 日志原文):

```
05:44:09,434 INFO myssia.cron.tick: Running job '微信监控' (ID: 0e9f2daf2d6a)
05:44:09,434 INFO myssia.cron.runner: Cron job '微信监控' spawning:
  .venv/bin/python3 -m myssia.cli run <数据根>/config/weixin.yaml
  --db <数据根>/myssia.db --json
05:44:10,360 INFO myssia.cron.runner: Cron job '微信监控' finished: ok
```

此为**真实自动触发**(ticker 自主扫描→派发,非手动 `cron tick`、非手动 `myssia run`)。

### 7.3 账目对照(触发前后,全形状级)

| 账目 | 前(05:41 快照) | 后(05:45 验读) |
|---|---|---|
| jobs.json `last_run_at` | null | `2026-10-13T05:44:10.361632+08:00` |
| jobs.json `repeat.completed` | 0 | 1 |
| jobs.json `next_run_at` | 05:30(已过) | `06:00:00+08:00`(重锚) |
| jobs.json `last_status` | null | `ok` |
| jobs.json `last_dispatch` | — | `{scheduled_at:05:30, dispatched_at:05:44:09.42, lateness_seconds:849.4, kind:"late"}`(迟发诚实记账) |
| executions 账本 | 55 行(最新 2026-10-12) | +1 行 `f009289dcc1c4dec…\|0e9f2daf2d6a\|tick\|completed`(source=tick=自动派发铁证) |
| runs 表 | max_run_id=106 | +1 行 `107\|weixin\|success` |
| weixin_items / wx_anchor_urls / dedup_total | 0 / 0 / 1747 | 0 / 0 / 1747(空态一致,零条目零键变更) |
| ticker_heartbeat | 1791840226(pid 24140,冻结) | 1791841509(pid 94048,新鲜;writer 已换 `-94048`,死属主文件被清) |

run 107 的 stats 形状核验(与手动轮 102/103/104 完全同态):源报告
`weixin-文件传输助手` `skipped:true` `skip_reason=chat_title_unreadable`
`item_count=0`,五阶段(fetch/classify/dedup/analyze/push)全 ok、
dedup 阶段 `items_in=0`——自动触发轮引擎行为与手动轮一致,空态语义复现。

### 7.4 干净停与残留核验

05:46:07 `kill -INT 94048` → serve 日志「收到中断信号→Cron ticker stopped→
cron serve 已退出」,后台任务 exit 0;`ps -p 94048`/`pgrep myssia` 双无命中——
零进程残留。心跳冻结在存活最后一跳(无宿主=无心跳,诚实语义)。

**判定:cron 自动线验收缺口已补实**——注册态 job 可自动触发且账目三处
(jobs.json/账本/runs)齐落钉。生产常态宿主=桌面 sidecar(主人开 app 即起),
常驻启停归主人/主会话运维,本档 dev serve 代行仅作验证、已停。

## 8. 三件套顺延判(grill 轮 2;窗口重探)

05:41 桥只读重探(`sessions list`,形状键):主窗 `window_id 85182`(上轮 81322,
微信窗口已重建)、`onscreen:false`、`capture.mean_luma=28.0`、`ocr.n_lines=0`——
与 §3 同态,离屏近黑帧未变。静默铁律禁止验收方带屏(§3 判例),故条目级三件套
(锚实例/dedup 同锚沉默/feed 屏非空)本会话客观不可达,**明示顺延后续任务**
(前置=主人保持主窗可见+目标会话打开;补验口径=重拉前后 dedup_total 与锚计数
对照,见 prd.md Acceptance Criteria)。勿留悬空:顺延依据、前置条件、补验
口径均已落 prd.md,非 TBD。
