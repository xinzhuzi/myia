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
