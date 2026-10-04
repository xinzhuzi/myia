# 桌面 sidecar 协议(方法注册表与错误码)

> **单一事实源 = `desktop/entry.py` `_HANDLERS`**。本文是镜像快照,两者冲突时以代码为准;
> `method_not_found` 应答自带 `data.allowed = sorted(_HANDLERS)`(entry.py:1919),可随时机器对账。

## 帧格式(entry.py 模块 docstring:10-31)

- 传输:stdin/stdout JSON-line RPC(UTF-8,ensure_ascii=False;stderr 只作调试旁路不承载协议)。
  请求 `{"id","method","params"}`;应答 `{"id","result"}` 或
  `{"id","error":{code,path,message,data}}`;`id` 缺省 = 通知(只执行不应答);
  事件无 id,以 `type` 区分。
- 事件 10 类:`log` / `progress` / `completed`(run 族)/ `test.completed`(试抓 job,C13)/
  `image.models.progress` / `image.models.completed`(模型下载 job)/ `image.server.completed`(server 自启 job;vision-v2 批)/
  `alerts.fired`(run 终态告警命中回放;alert-rules 批)/
  `cron.skipped`(cron fire 撞桌面 run 单飞锁跳过)/ `cron.completed`(cron fire 完成,带运行摘要;hermes-cron 批)。
- 错误结构化透传(对齐 spec python/error-handling):`path` 字段路径、`message` 中文原因、`data` 原始细节。
- EOF = 干净退出 0(serve,entry.py:1941)。

## 方法注册表(本文现列 57 行;代码 `_HANDLERS` 现值 57,对账一致;单一事实源 = 代码)

| # | 方法 | 处理器 | 语义 |
|---|------|----------------|------|
| 1 | `version` | `_m_version` | `myia --version` 等价:版本 + 协议版本 + app 版本(`app_version` 透传壳层 `MYIA_APP_VERSION`,dev/CLI 未注入 = null;v112 批 C10) |
| 2 | `health` | `_m_health` | 插件清单 + 源健康度 + 计数聚合 |
| 3 | `plugins.list` | `_m_plugins_list` | 已装市场插件 + findings |
| 4 | `doctor` | `_m_doctor` | 结构化诊断(问题全在 findings,完成即 0) |
| 5 | `run.start` | `_m_run_start` | 启动 run 子进程,立即返回 run_id;单飞 `run_busy` |
| 6 | `run.status` | `_m_run_status` | run 注册表查询;未知 id = 结构化 404 |
| 7 | `run.cancel` | `_m_run_cancel` | 取消进行中 run:killpg(SIGTERM→5s→SIGKILL);信号终局 status=cancelled(v112 批 C2) |
| 8 | `runs.list` | `_m_runs_list` | runs 表直读(新→旧,limit 钳制 [1,200]);重启后历史可达(v112 批 C3) |
| 9 | `logs.tail` | `_m_logs_tail` | 环形缓冲尾部日志,run_id 可选过滤 |
| 10 | `store.items` | `_m_store_items` | SQLite 单库直读情报流(新→旧);游标 `before`/`before_id` + `query`(v112 批 C1) |
| 11 | `feed.export` | `_m_feed_export` | 当前过滤视图导出 JSONL/CSV:sidecar 直写(数据不经 webview),只写对话框选定单文件;`export_path_invalid`/`export_write_failed`(feed-ux 批 G3) |
| 12 | `schedule.preview` | `_m_schedule_preview` | 品类排程 Next runs 预览(纯计算零副作用,count 钳制 [1,20];无排程明示 null 非 err;feed-ux 批 G4) |
| 13 | `secret.set` | `_m_secret_set` | 凭据只入系统钥匙链;值零回显零落日志 |
| 14 | `secret.list` | `_m_secret_list` | 只列名字,值永不可读 |
| 15 | `secret.delete` | `_m_secret_delete` | 删除凭据(误存清除口;二次删除 `secret_not_found`;v112 批 C5) |
| 16 | `sources.write` | `_m_sources_write` | 源启停写回(sources 屏私有封装) |
| 17 | `sources.test` | `_m_sources_test` | 试抓此源,异步 job(`test_busy` 单飞);结果走 `test.completed` 事件(v112 批 C13) |
| 18 | `yaml.list` | `_m_yaml_list` | plugins 目录品类 YAML 清单(坏文件也入列) |
| 19 | `yaml.read` | `_m_yaml_read` | 原文直读,注释/顺序逐字节保真(不经 dump) |
| 20 | `yaml.validate` | `_m_yaml_validate` | 干跑校验,findings 分级,永不抛校验错 |
| 21 | `yaml.template` | `_m_yaml_template` | 最小合法品类模板(id/name 占位) |
| 22 | `yaml.save` | `_m_yaml_save` | 同门校验→跨文件 id 查重→`.bak`→原子写(mtime 乐观锁) |
| 23 | `yaml.delete` | `_m_yaml_delete` | 围栏→`.bak` 留底→删主文件→连带删 `.disabled.json` |
| 24 | `image.config.read` | `_m_image_config_read` | vision.yaml 脱敏读取(不存在 = 全缺省) |
| 25 | `image.config.save` | `_m_image_config_save` | vision.yaml 保存,同门校验失败零写入 |
| 26 | `channels.list` | `_m_channels_list` | 消息屏目录四视图:platforms+aliases+dead+rules(零平台=合法空态) |
| 27 | `channels.refresh` | `_m_channels_refresh` | 单平台 `discover_directory`→桶替换+落盘;失败结构化上抛,旧桶不动 |
| 28 | `channels.alias` | `_m_channels_alias` | 别名 set/delete(name 非空/null 区分);落盘复核未生效即报错 |
| 29 | `push.write` | `_m_push_write` | push[] 全量替换:围栏→文本手术→双门→`.bak`→原子写;失败零写入 |
| 30 | `push.test` | `_m_push_test` | 合成单条测试条目真发指定通道(凭据沿用 env:/keychain: 引用链;PushSendError code 原文直传;stdout 通道卡片入应答 preview;feed-ux 批 G5 前半) |
| 31 | `bridge.status` | `_m_bridge_status` | 微信桥接探测:`probe_bridge()` 全量七键(available/reason/fix_hint/bin_found/weixin_configured/gateway_alive/bin_path);纯文件存在性探测零读取,无凭据无出网;bin 取品类 YAML 首个 weixin 条目 `weixin_hermes_bin` 覆写;永不抛业务错(10-03-messaging-weixin-bridge D4) |
| 32 | `feedback.mark` | `_m_feedback_mark` | 卡片 👍/👎 反馈入库(record_feedback 同门直调,channel=desktop;CLI `feedback list` 可见同条目 = 往返一致;条目不存在 `item_not_found`;v112 批 B2) |
| 33 | `feedback.list` | `_m_feedback_list` | 反馈记录直读(SQLiteStore.list_feedback,新→旧;键同 CLI `_feedback_row_dict`;v112 批 B2) |
| 34 | `feedback.stats` | `_m_feedback_stats` | 窗口统计 + 生效调参 + 调参历史(FeedbackTuner/TuningPolicy/load_active_tuning 同门,键同 CLI stats 载荷;v112 批 B2) |
| 35 | `store.trend` | `_m_store_trend` | 采集量趋势(SQLiteStore.daily_item_counts,UTC 逐日计数旧→新;days 钳制 [1,90],零数日补齐归前端;v112 批 B4) |
| 36 | `image.models.list` | `_m_image_models_list` | `<home>/models` 扫描 → `{models:[{name,path,bytes,active,incomplete}]}`;半成品 = 缺 config.json/*.safetensors 的目录(incomplete=true,可续传);空目录 = 合法空表(vision-v2 批) |
| 37 | `image.models.download` | `_m_image_models_download` | 异步 job(HF snapshot_download,repo 必须 `mlx-community/<name>`——MLX 量化权重直下免 convert;磁盘预检 + `local_dir` 断点续传);提交即返 `{job_id}`,进度/终态走 `image.models.progress`/`image.models.completed` 两事件(一切失败以完成事件 `ok:false+error` 收口);单飞 `download_busy`(vision-v2 批) |
| 38 | `image.models.delete` | `_m_image_models_delete` | 删模型目录 → `{ok}`;active 模型拒删 `model_active_refused`(在用权重删除会让本地 VL 突然失效;vision-v2 批) |
| 39 | `image.models.activate` | `_m_image_models_activate` | 激活 = vision.yaml `local.model` 原子改写(同门校验失败零写入)→ `{ok}`;半成品拒激活 `model_incomplete`,写失败 `image_config_invalid`(vision-v2 批) |
| 40 | `image.server.status` | `_m_image_server_status` | 本地 mlx_vlm.server 快照 `{running, base_url, model, healthy}`(探 `base_url/models` 2s 帽,零副作用;vision-v2 批) |
| 41 | `image.server.ensure` | `_m_image_server_ensure` | 快慢双路径:快路径已健康 → status+`{started:false}` 零后台;慢路径后台线程自起 `uvx --from mlx-vlm mlx_vlm.server` + 健康等待 ≤120s(同步等会冻死单线程 serve 循环全协议队头阻塞——复查修复拍板),应答立即返快照超集+`{ensuring:true, job_id}`,终态走 `image.server.completed` 事件;单飞 `ensure_busy`;日志 `<home>/vision-server.log`(>5MB 轮转;vision-v2 批) |
| 42 | `image.files.purge` | `_m_image_files_purge` | 按 mtime 清 `<数据根>/images` 超龄落图 `{days}`(整数 ≥1)→ `{deleted, bytes_freed}`;只删文件不动目录(内容寻址平铺);CLI 面能力零 UI;目录不存在 = 合法零删(vision-v2 批复查) |
| 43 | `feed.enrich` | `_m_feed_enrich` | 情报流卡单条「AI 摘要」:`{item}`(items.id 或 dedup_key/URL,`resolve_item_ref` 同 `feedback.mark` 口径)→ `{item_id, model, scores, score, cached}`;骑 `shishi.enrich.LLMEnricher` 现跑(端点 = 条目所属品类 YAML `enrich:` 节 `env:`/`keychain:` 引用解析;enrich_cache 缓存语义复用,命中零 token;分数原路回填 items 表);async `enrich()` 在 handler 内 `asyncio.run` 同步应答,挂 `EnrichSettings.timeout_seconds` 超时;未启用/缺端点/品类 YAML 缺失 = `enrich_not_configured`(graceful;fe-small-batch 批 G8) |
| 44 | `alerts.list` | `_m_alerts_list` | 告警规则清单(全量 id 升序,启用/停用同行——启停 = save 全量提交):`{}` → `{rules:[AlertRuleView]}`;AlertRuleView = 规则全字段 + `fired_count`/`last_fired_at` 自 alert_fired 表派生(计数不落规则行,save 全量替换不清计数;alert-rules 批) |
| 45 | `alerts.save` | `_m_alerts_save` | 规则**全量替换**(承建/改/启停一体,不设独立启停方法;push.write 全量先例):`{rules:[AlertRuleInput]}` → `{ok, rules}`;两道门 = 逐条过构造门(shishi.alerts.compile_rule:name/scope/when 白名单语法/action/action_config 形状)任一失败 `alert_rule_invalid`(data 三键 index/field/reason)**整批零写入** + diff 落库(带 id 更新保 id/不带新建/库中多余 id 删除,fired 历史照留;空数组 = 清空回到零惊扰默认;alert-rules 批) |
| 46 | `alerts.delete` | `_m_alerts_delete` | `{id}` → `{ok}`:删规则定义行,**fired 历史照留**(命中历史是事实);未知 id = `alert_not_found`(alert-rules 批) |
| 47 | `alerts.test` | `_m_alerts_test` | **dry 求值,不真发不落 fired**:`{rule?\|rule_id?, item?\|item_id?}` → `{matched, muted, actions, eval_error?, already_fired?}`;rule = 草稿(未保存即可测)/rule_id = 已存规则;item = 合成字段 dict(`Item.from_extracted` 构造,content 补丁生效)/item_id = 库内条目(求值上下文与引擎同门)/都缺 = 最近一条(空库 `alert_test_no_item`);muted = effective mute 压制(品类 watchlist + 反馈 0.0 词,命中即不评估);actions 展开 push 通道解析结果+降级原因 / tag 标签;already_fired 仅 rule_id 形态;真发测试借既有 `push.test`(alert-rules 批) |
| 48 | `runs.trend` | `_m_runs_trend` | run 成功率趋势(SQLiteStore.daily_run_outcomes:runs 表按 `substr(started_at,1,10)` UTC 逐日×status 聚合旧→新,`days` 钳制 [1,90] 缺省 14、`category?`、`db?` → `{days:[{date,total,statuses{…}}]}`,零数日补齐归前端 fillDailyOutcomes;statuses 开放词表原样分组,真实词表 4 态 running/success/partial/failed;服务端聚合而非前端算 runs.list —— limit≤200 在 cron 排程+手动 run 下 30 天窗可超限,截断会让序列静默失真;desktop-b234 批 G6) |
| 49 | `cron.list` | `_m_cron_list` | 定时 job 清单(`CronJobs.list_jobs`,缺省仅活跃;`all:true` 含暂停/终态;`db?` 覆写数据根;hermes-cron 批) |
| 50 | `cron.create` | `_m_cron_create` | 建定时 job:`{schedule, category, name?, deliver?, failure_deliver?, repeat?, timezone?, config?, run_timeout?, dry_run?, paused?, paused_reason?, db?}`;Q6 完整 `load_category_file` 早失败(`cron_category_invalid`,data=LoadError.to_dict)、Q5 绝对路径存储、时区链 timezone > 品类 YAML > 本地;schedule 解析/once 超窗/repeat 等 ValueError = `cron_create_failed`;origin=`{source:"desktop"}`(hermes-cron 批) |
| 51 | `cron.edit` | `_m_cron_edit` | 部分更新(同 create 可选字段):schedule 变更由底座重算 `next_run_at` 并重推导 repeat 缺省(once↔recurring 翻转);category 同款 Q6 早失败;空更新集 = `cron_edit_no_changes`;终态复活拒绝/解析失败 = `cron_edit_failed`(hermes-cron 批) |
| 52 | `cron.pause` | `_m_cron_pause` | 暂停 job(`reason?` 可选,F1.1);`{all:true}` = 全局急停 estop 标记(grill Q4:tick 跳过派发、在途 run 不受影响),与 `job` 互斥(hermes-cron 批) |
| 53 | `cron.resume` | `_m_cron_resume` | 恢复 job / 一次性重挂(`at?` = ISO 时刻,`rearm_oneshot`);`{all:true}` = 解除全局急停,与 `job`/`at` 互斥;recurring 拒 `at`/once 过窗 = `cron_resume_failed`(hermes-cron 批) |
| 54 | `cron.run` | `_m_cron_run` | 下次 tick 立即跑(`trigger_job`,manual 来源;复活 paused + 计入 repeat,§8.1 事实裁决;`manual_run_at=next_run_at`);终态 job 拒绝 = `cron_run_failed`(hermes-cron 批) |
| 55 | `cron.remove` | `_m_cron_remove` | 删 job 记录 → `{removed, job_id, name}`;output 目录与账本行保留(运行证据)(hermes-cron 批) |
| 56 | `cron.status` | `_m_cron_status` | ticker 活性快照(F1.6):`{ticker_alive, heartbeat_age_seconds, last_success_age_seconds, last_error, estopped, jobs_total, jobs_enabled, next_due_at}`;心跳新鲜窗 = interval×3+20s(CLI `cron status` 同公式);serve 内置 ticker 起过才活,dev 回退恒 not-alive(hermes-cron 批) |
| 57 | `cron.runs` | `_m_cron_runs` | 执行账本尾查(`ExecutionLedger.list_executions` 新→旧):`{job?, limit?=20 钳制 [1,500], db?}` → `{count, executions}`;`run_summary_json` 随行解析为 `run_summary`(D10 摘要快照;损坏串如实带 `{raw}`)(hermes-cron 批) |

分组:核心 10(1-9 + 13-14 的 logs.tail/secret.set/secret.list)+
源启停 1(16)+ 品类 YAML 编辑 6(18-23,task 10-03-yaml-editor)+
看图配置 2(24-25,task 10-03-image-input;10-03-vision-pipeline 拆四留二)+
消息 4(26-29,task 10-03-messaging-ui)+
feed-ux 3(11 `feed.export` G3 / 12 `schedule.preview` G4 / 30 `push.test` G5,task 10-03-feed-ux)。
v1.1.2 桌面对齐批(task 10-03-v112-desktop-parity)新增 8:7 `run.cancel`(C2)/
8 `runs.list`(C3)/ 15 `secret.delete`(C5)/ 17 `sources.test`(C13)+
32 `feedback.mark` / 33 `feedback.list` / 34 `feedback.stats`(B2)/
35 `store.trend`(B4,第二切片)。
weixin-bridge 批(task 10-03-messaging-weixin-bridge)新增 1:31 `bridge.status`。
vision-v2 批(task 10-03-vision-v2)新增 7:36-39 `image.models.*` 四 +
40-41 `image.server.*` 两 + 42 `image.files.purge`;协议 v5。
fe-small-batch 批(task 10-03-fe-small-batch)新增 1:43 `feed.enrich`(G8,
情报流卡 AI 摘要;前端门面接线归 G8 前端件);协议 v6。
alert-rules 批(task 10-04-alert-rules)新增 4:44-47 `alerts.*` 四方法 +
`alerts.fired` 回放事件(见下方契约段);协议 v7(hermes-cron 批未先合入,
v7 归本批——按合入顺序定案,开工实读 `PROTOCOL_VERSION`=6)。
desktop-b234 批(task 10-04-desktop-b234)新增 1:48 `runs.trend`(G6 成功率
折线:runs 表逐日×status 聚合,`days` 钳制 [1,90] 缺省 14、`category?`、`db?`
→ `{days:[{date,total,statuses{…}}]}` 旧→新;statuses 开放词表原样分组,真实
词表 4 态 running/success/partial/failed;服务端聚合因 runs.list limit≤200 在
cron 排程+手动 run 下 30 天窗可超限、前端聚合会静默失真);协议 v8。
hermes-cron 批(task 10-04-hermes-cron B3)新增 9:49-57 `cron.*` 九方法 +
`cron.skipped`/`cron.completed` 两事件 + serve 内置 cron ticker(见下方契约段);
协议 v9。

**store.items 参数(合流形状,v112 批 C1 × feed-ux G1/G3)**:`db/category/since/limit`
之外增 `before`(ISO,first_seen 严格小于)、`before_id`(与 before 组成
`(first_seen, id)` 复合游标,成对出现)、`query`(title/content/source 三列
LIKE NOCASE,%/_ 按字面转义)。旧调用零感知。

**feed-ux 批三方法参数(task 10-03-feed-ux,契约钉死于任务档 design.md §1)**:
`feed.export {format: jsonl|csv, path: 绝对路径, category?, query?}` →
`{path, count, bytes}`(path = 前端 `dialog.save()` 选定,只写该一个文件);
`schedule.preview {file: 围栏内品类 YAML, count?=5 钳制 [1,20]}` →
`{file, schedule: string|null, timezone, runs[]}`(build_cron_trigger 纯计算);
`push.test {channel: shishi.push.CHANNELS 键, target?(env:/keychain: 引用), template?}`
→ `{ok: true, channel, preview?}`(preview 仅 stdout 通道——serve stdout 是协议流,
卡片行入内存缓冲随应答回显)。协议版本随批 bump:v3(feed-ux 三方法)、
v4(weixin-bridge 批 `bridge.status`)、v5(vision-v2 批:`image.models.*` 四 +
`image.server.*` 两 + `image.files.purge` + `store.items` 投影三键,见下段)、
v6(fe-small-batch 批 `feed.enrich`,契约见下段)、v7(alert-rules 批 `alerts.*`
四方法 + `alerts.fired` 事件,契约见下段)、
v8(desktop-b234 批 `runs.trend` 成功率趋势逐日聚合)、
v9(hermes-cron 批 `cron.*` 九方法 + `cron.skipped`/`cron.completed` 事件 +
serve 内置 cron ticker,契约见下段)。

**vision-v2 批七方法契约(task 10-03-vision-v2;能力实现 `shishi.vision.models` /
`shishi.vision.server`,重依赖惰性,huggingface-hub 在 extras `shishi[vision]`)**:
`image.models.list` / `image.server.status` / `image.server.ensure` 零参;
`image.models.download {repo: mlx-community/<name>, name?(缺省 = repo 名段)}` →
`{job_id}` + **下载两事件** `image.models.progress {job_id, repo, done_bytes,
total_bytes?}` / `image.models.completed {job_id, ok, error?}`(磁盘预检不足
`disk_insufficient`、网络失败、未预期异常一律以完成事件 error 收口,不发请求
错误);`image.models.delete` / `image.models.activate` `{name}`;`image.files.purge
{days}`(整数 ≥1)。错误码:entry 静态 `invalid_params`(repo/name/days 形状)+
单飞 `download_busy` / `ensure_busy`;`VisionModelError` / `VisionServerError`
code 动态透传(`invalid_repo` / `hf_unavailable` / `repo_unreachable` /
`disk_insufficient` / `model_exists` / `model_incomplete` /
`model_active_refused` / `no_local_model` / `model_dir_missing` /
`spawn_failed` / `server_died` / `server_start_failed` 等,源头
`src/shishi/vision/`):delete/activate 透传为应答错误,download/ensure 收口为
完成事件 `error` 字段。`store.items` 的 `_item_dict` 白名单投影补
`image_caption` / `image_files` / `image_ocr_lines` **三键**(随落图开关
产生;`image_ocr_lines` 逐行 `{text, conf}` 原样透传供详情逐行置信度渲染,
形态不符整体置 None 不半投影——`image_ocr` 旧键 vision-pipeline 已有)。

**feed.enrich 契约(task 10-03-fe-small-batch G8;能力实现 `shishi.enrich`,
与 `myia run` 第二层漏斗同门)**:`feed.enrich {item: int|str, db?}` →
`{item_id, model, scores, score, cached}`。`item` 引用口径同 `feedback.mark`
(`resolve_item_ref`:items.id(int/纯数字串)或 dedup_key/URL;条目不存在
`item_not_found`)。端点配置 = 条目所属品类 YAML `enrich:` 节:插件目录扫描
品类 id 精确匹配(同 `_collect_category_ids` 确定性约定,坏文件不参与),
`base_url`/`api_key` 由 `EnrichSettings`/`LLMEnricher` 构造期走
`env:`/`keychain:` 引用解析(无内置端点、无默认 key,grill Q6);enrich_cache
缓存语义原样复用((url, model, scores_key) 命中零 token,`cached:true`),
分数经 `LLMEnricher.enrich` 原路回填 items 表(含缓存命中路径);async
`enrich()` 在 handler 内 `asyncio.run` 同步应答(serve 单线程,单条单批
不破队头),整段挂 `EnrichSettings.timeout_seconds` 超时帽。错误码:
`enrich_not_configured`(graceful 明示无配置,`data.reason` ∈
`enrich_disabled` / `endpoint_missing` / `category_yaml_not_found`)/
`enrich_timeout` / `enrich_failed`(预算耗尽或批次失败条目未获分,
`data` 带 `degrade_reason` + `failures`);`EnrichConfigError` code 原文透传
(`credential_unresolved` / `invalid_base_url` 等,追源头去
`src/shishi/enrich/`)。mute 命中走管线零 token 降权路径,照常应答
(三维 0 分 + `cached:false`)。

**alerts.* 契约(task 10-04-alert-rules;能力实现 `shishi.alerts` 包 + store
`alert_rules`/`alert_fired` 两表,管线挂点 `Pipeline._alert_pass` 为 run 阶段
循环后的独立轻量附加步)**:`alerts.list {}` → `{rules:[AlertRuleView]}`
(全字段 + `fired_count`/`last_fired_at` 派生,计数不落规则行——save 全量替换
不清计数);`alerts.save {rules:[AlertRuleInput]}` → `{ok, rules}`——**全量
替换承建/改/启停,不设独立启停方法**(编辑一条提交整个数组,push.write 先例);
两道门:①逐条构造期拒(`compile_rule`:name/scope('global'+七品类+channel)/
when 白名单 AST 语法/action ∈ {push,tag}/action_config 形状,push 需
channel ∈ `shishi.push.CHANNELS` + 可选 targets/template,tag 需非空 tags),
任一条失败 = `alert_rule_invalid`(data `{index, field, reason}`)整批零写入;
②diff 落库:带 id = 更新保 id(id 稳定是计数派生的前提),不带 = 新建,库中
多余 id = 删除(fired 历史照留),空数组 = 清空。`alerts.delete {id}` → `{ok}`。
`alerts.test {rule?|rule_id?, item?|item_id?}` → `{matched, muted, actions,
eval_error?, already_fired?}`——**dry 求值不真发不落 fired**;`muted` = 条目按
当前 effective mute(品类 watchlist + 反馈 0.0 权重词,`_effective_watchlist`
同门)被压制即 matched=false 不评估(引擎硬规则);`actions` = 将触发动作展开
(push:品类 `push[]` 同类型第一条解析结果 + targets/template + 降级原因
`item_no_category`/`category_yaml_not_found`/`category_push_missing`;tag:tags);
`already_fired` 仅 rule_id 形态;真发测试借既有 `push.test`。**事件
`alerts.fired {rule_id, rule_name, item_id, dedup_key, title, action,
action_status, ts}`**:run 终态收口处(发 `completed` 的同一监管线程)以
`list_fired(since=run.started_at)` 查库逐条回放(completed 之前发出;dry run
管线侧零落库零回放;查库回放零子进程日志格式耦合)。错误码:`alert_rule_invalid`
/ `alert_not_found`(delete、test 的 rule_id 形态、save 载荷未知 id)/
`alert_test_no_item`(缺省取材空库);`item_not_found` 复用 feedback 族
(item_id 形态);运行期求值错/mute 压制/通道降级/发送失败 = 非协议错
(WARNING 隔离,logs.tail 可见)。

**cron.* 契约(task 10-04-hermes-cron B3;能力实现 `myia.cron` 包,与 CLI
`myia cron` 同一 API 层(AC7);蓝本 Hermes cron/(MIT)gateway 内嵌 cron 的
等价物)**:`job` 引用 = id 或名字(`resolve_job_ref`:精确 id → 精确名 →
唯一前缀;重名 = `cron_ambiguous_job` 带 `data.candidates`,未找到 =
`cron_job_not_found`);数据根 = `db` 参数(缺省 = serve 上下文 db)的父
目录,cron 目录(jobs.json/executions.db/output/)挂数据根。`cron.list
{all?, db?}` → `{db, data_root, count, jobs}`(缺省仅活跃,`all:true` 含
paused/终态);`cron.create {schedule, category, name?, deliver?,
failure_deliver?, repeat?, timezone?, config?, run_timeout?, dry_run?,
paused?, paused_reason?, db?}` → `{job}`——Q6 完整 `load_category_file`
早失败(`cron_category_invalid`,data = LoadError.to_dict 的 errors[]),
Q5 绝对路径存储,时区链 timezone > 品类 YAML timezone > 本地,schedule
五形态解析失败/once 超窗/repeat 形状/paused 自相矛盾 = `cron_create_failed`
(ValueError 原文);`cron.edit` 同 create 可选字段做部分更新,schedule 变更
重算 `next_run_at`;`cron.pause {job, reason?}` / `{all:true}` estop;
`cron.resume {job, at?}` / `{all:true}`;`cron.run {job}` = trigger(manual
来源,复活 paused + 计入 repeat);`cron.remove {job}`(output/账本保留);
`cron.status {}` → ticker 活性 + 下次到期 + 急停态;`cron.runs {job?,
limit?=20 钳 [1,500]}` → executions 账本(`run_summary` 随行解析)。
**serve 内置 cron ticker**:serve() 就绪后起、EOF 关停(lifetime = serve),
daemon 线程绝不占 serve 线程(B10 队头阻塞铁律);监督 = `SupervisedTickerThread`
+ 专职 supervisor 线程周期 `restart_if_dead`(F2.2,CLI `cron serve` 主循环
同款,serve 线程阻塞在 readline 承担不了);**home 模式才起**(桌面生产
恒 home;dev 回落数据根 cwd 不起,防测试/开发 serve 污染仓库目录,dev
常宿形态用 `myia cron serve`);与 CLI serve 并存靠 tick 文件锁 + fire
claim 互斥(多宿主,照抄 Hermes)。**事件 `cron.skipped {job_id, name,
reason:"run_busy", active_run_id, ts}`**:cron fire 撞桌面 run 单飞锁
(`_RUNS_LOCK/_ACTIVE_RUN_ID`)= 跳过本 fire(grill Q2:advance 已消耗不排队
不回滚,与 at-most-once 一致,用户手点优先;`last_status="skipped_busy"`
由 tick 层落库,成功语义不动 streak);**事件 `cron.completed {job_id,
name, ok, status, delivery_error, summary, ts}`**:fire 完成——摘要直接取
runner 随执行行落账的 `run_summary_json`(D10,零二次解析子进程 stdout;
status 取摘要 run 块,账本无行时 summary=null/status 回落成功布尔,不虚构)。
桌面定时任务 UI 屏不在本批(PRD 非目标:sidecar 方法齐即可,UI 另立档)。

## 错误码表

### 协议级(分发层 `_handle_line` entry.py:1902-1936,5 个)

| code | 触发 |
|------|------|
| `parse_error` | 请求行不是合法 JSON |
| `invalid_request` | 请求非 JSON 对象 / 缺字符串 `method` |
| `invalid_params` | `params` 非对象(参数形状错由各处理器细分抛同名 code) |
| `method_not_found` | 未知方法;`data.allowed` 自带全量注册表 |
| `internal_error` | 处理器未捕获异常兜底;协议流不裸 traceback |

### 业务级(entry.py 内静态抛出)

| 族 | code | 场景 |
|----|------|------|
| 通用参数 | `invalid_params`(25 处) | 各处理器参数形状/取值校验 |
| CLI 包装 | `config` / `cli_error` | CLI 报文带 config+errors[] / 退出码异常无可解析输出(:439-443) |
| 环境 | `myia_home_unwritable` | serve 上下文数据根不可写(:291) |
| run | `run_busy` / `run_not_found` / `run_not_active` | 单飞拒绝并发 / 未知 id 或无进行中 run / 已终态拒取消(data 带 state;v112 批 C2) |
| 反馈 | `item_not_found` / `feedback`(另复用 `invalid_params` / `store_corrupt` 透传) | `feedback.mark`:条目引用解析不到 / verdict 校验或 TuningPolicy 构造失败;`feedback.list`/`stats` 参数形状(v112 批 B2) |
| 源启停 | `duplicate_source` / `last_source` / `source_unknown` / `source_file_unreadable` / `source_dir_unreadable` / `source_write_failed` / `stash_unreadable` / `category_invalid` | `sources.write` 全链路 |
| 试抓 | `test_busy`(另复用 `invalid_params` / `not_yaml_suffix` / `path_outside_root` / `source_file_unreadable`) | `sources.test`:单飞拒绝 / 参数形状 / 围栏 / 品类装不上(v112 批 C13);子进程级 CLI 错不走请求错误,经 `test.completed` 事件 `ok:false` 透传 |
| 品类 YAML 编辑 | `path_outside_root` / `not_yaml_suffix` / `invalid_file_stem` / `file_too_large` / `invalid_encoding` / `file_not_found` / `mtime_conflict` / `duplicate_category_id`(另复用 `category_invalid` / `source_file_unreadable` / `source_write_failed`) | 围栏 + 乐观锁 + 跨文件查重(yaml.* 六方法) |
| 看图配置 | `image_config_invalid` | `image.config.read` 装载拒载 / `image.config.save` 未过校验零写入(拆四留二后看图族仅余此码) |
| feed-ux 导出 | `export_path_invalid` / `export_write_failed` | `feed.export`:路径空/相对/父目录不存在 / 写盘 IO 失败(task 10-03-feed-ux G3) |
| feed-ux 排程 | `invalid_cron`(防御性;另复用 `invalid_params`/`not_yaml_suffix`/`path_outside_root`/`source_file_unreadable`) | `schedule.preview`:`build_cron_trigger` 兜底 / 参数 / 围栏 / 品类装不上(task 10-03-feed-ux G4) |
| 单条精评 | `enrich_not_configured` / `enrich_timeout` / `enrich_failed`(另复用 `invalid_params`/`item_not_found`/`store_corrupt`;`EnrichConfigError` code 动态透传) | `feed.enrich`:品类未启用 enrich/缺端点引用/品类 YAML 缺失(graceful,`data.reason` 三分)/ `asyncio.run` 整段超时 / 条目未获分(degrade_reason+failures 入 data);凭据解析失败透传 `credential_unresolved` 等(fe-small-batch 批 G8) |
| 消息 | `unknown_platform` / `discover_not_supported` / `channel_refresh_failed` / `alias_write_failed` / `push_write_unsupported`(另复用 `category_invalid` / `file_not_found` / `path_outside_root` / `source_write_failed` / `invalid_params`) | channels.* / push.write 全链路(task 10-03-messaging-ui;数据面错误码透传 push 层如 `credential_not_found` 经 `channel_refresh_failed.data.code` 携带) |
| 看图模型/服务 | `download_busy` / `ensure_busy`(另复用 `invalid_params`;activate 改写 vision.yaml 失败复用 `image_config_invalid`) | image.models.* / image.server.* 单飞拒绝与参数形状;`VisionModelError`/`VisionServerError` code 透传(delete/activate 走应答错误,download/ensure 走完成事件 error 字段,枚举见上方 vision-v2 契约段;task 10-03-vision-v2) |
| 告警规则 | `alert_rule_invalid` / `alert_not_found` / `alert_test_no_item`(另复用 `invalid_params` 互斥门/载荷形状、`item_not_found` 的 item_id 形态) | `alerts.save` 某条构造期拒(data `{index, field, reason}`,整批零写入)/ `alerts.delete`·`alerts.test`(rule_id 形态)·`alerts.save`(载荷未知 id)未知 id / `alerts.test` 缺省取材空库(task 10-04-alert-rules;求值错/mute/降级/发送失败 = 非协议错,WARNING 隔离走 logs.tail) |
| 定时任务 | `cron_category_invalid` / `cron_create_failed` / `cron_edit_failed` / `cron_edit_no_changes` / `cron_resume_failed` / `cron_run_failed` / `cron_ambiguous_job` / `cron_job_not_found`(另复用 `invalid_params` 参数形状/all 与 job 互斥) | `cron.create`/`cron.edit` 品类 YAML 装不上(Q6 早失败,data=LoadError.to_dict)/ `create` 的 schedule 五形态·once 超窗·repeat·paused 自相矛盾(ValueError 原文)/ `edit` 的 schedule 变更解析失败·终态复活拒绝 / `edit` 空更新集 / `resume` 的 recurring 拒 at·once 过窗 / `run` 终态 job 拒绝 / 名字引用重名(data.candidates)/ id 或名字未找到(task 10-04-hermes-cron;与 CLI `myia cron` 同码) |

### 透传族(`exc.code` 动态透传,不在 entry.py 静态出现)

`store.items` / `secret.*` / CLI 包装透传底层模块 code(例:`store_corrupt` /
`invalid_secret_name` / `plugins_dir`,枚举见 entry.py 模块 docstring:19-21)——追源头去
`src/shishi/` 对应模块,entry.py 只加 `path`/`data` 不改 code。`push.test` 同款透传
push 层 `PushSendError.code`(`missing_target` / `env_var_missing` /
`credential_resolve_failed` 等,追源头去 `src/shishi/push/`;task 10-03-feed-ux G5)。

## 变更纪律

1. 新增/改名方法:**只改 `_HANDLERS` 一处** + `tests/test_desktop_sidecar_protocol.py` 契约用例;
   本文注册表随同更新(行号注解允许漂移,方法名集合不许漂)。
2. 对账手法:发未知方法名,拿 `data.allowed` 与本文注册表比对;前端共享类型映射
   `SidecarProtocol`(types.ts)现盖 23 方法(核心 + image.config.* + v1.1.2 批八方法 +
   feed-ux 批三方法),`sources.write`/`yaml.*` 刻意未入共享映射——对账时按上表分组核对,勿以映射数当全量。
3. 封装面 ≠ 协议面:`ui-src/src/lib/api/client.ts` 的 `api` 门面盖核心 10 方法 +
   v1.1.2 桌面对齐批 8 方法(`runCancel`/`runsList`/`secretDelete`/`sourcesTest` +
   `feedbackMark`/`feedbackList`/`feedbackStats`/`storeTrend`,
   10-03-v112-desktop-parity)+ feed-ux 批 3 方法(`feedExport`/`schedulePreview`/
   `pushTest`,10-03-feed-ux;两批新方法全入共享门面,注册表新增行 ↔ 门面新增行
   同源对账,屏私名单不扩);
  `sources.write` 在 `screens/sources/api.ts`、`yaml.*` 在 `screens/yaml-editor/api.ts`、
  `image.config.*` 在 `screens/settings/vision-api.ts`、`channels.*`/`push.write`/
  `bridge.status` 在 `screens/messaging/api.ts` 屏私有封装(invoke 直连,不走共享门面);
  `cron.*` 九方法暂无任何前端接线(桌面定时任务 UI 屏是 hermes-cron 的 PRD 非目标,
  另立档;接线时按上表对账)。
