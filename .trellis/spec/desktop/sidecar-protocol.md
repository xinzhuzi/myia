# 桌面 sidecar 协议(方法注册表与错误码)

> **单一事实源 = `desktop/entry.py` `_HANDLERS`**。本文是镜像快照,两者冲突时以代码为准;
> `method_not_found` 应答自带 `data.allowed = sorted(_HANDLERS)`(entry.py:1919),可随时机器对账。

## 帧格式(entry.py 模块 docstring:10-31)

- 传输:stdin/stdout JSON-line RPC(UTF-8,ensure_ascii=False;stderr 只作调试旁路不承载协议)。
  请求 `{"id","method","params"}`;应答 `{"id","result"}` 或
  `{"id","error":{code,path,message,data}}`;`id` 缺省 = 通知(只执行不应答);
  事件无 id,以 `type` 区分。
- 事件 7 类:`log` / `progress` / `completed`(run 族)/ `test.completed`(试抓 job,C13)/
  `alerts.fired`(run 终态告警命中回放;alert-rules 批)/
  `cron.skipped`(cron fire 撞桌面 run 单飞锁跳过)/ `cron.completed`(cron fire 完成,带运行摘要;hermes-cron 批)。
  (image.models.progress/completed 与 image.server.completed 三事件已随看图客户端制移除,vision-model-path 批。)
- 错误结构化透传(对齐 spec python/error-handling):`path` 字段路径、`message` 中文原因、`data` 原始细节。
- EOF = 干净退出 0(serve,entry.py:1941)。

## 方法注册表(本文现列 90 行;代码 `_HANDLERS` 现值 90,对账一致;单一事实源 = 代码)

| # | 方法 | 处理器 | 语义 |
|---|------|----------------|------|
| 1 | `version` | `_m_version` | `myia --version` 等价:版本 + 协议版本 + app 版本(`app_version` 透传壳层 `MYIA_APP_VERSION`,dev/CLI 未注入 = null;v112 批 C10) |
| 2 | `health` | `_m_health` | 插件清单 + 源健康度 + 计数聚合 |
| 3 | `plugins.list` | `_m_plugins_list` | 已装市场插件 + findings |
| 4 | `doctor` | `_m_doctor` | 结构化诊断(问题全在 findings,完成即 0);可选布尔 `config_auto`(缺省 false 现行为不变;G10 10-05-g10-proxy-probe):`config` 缺省且 true → 发现 `<数据根>/pools.yaml`,命中才带 `--config`(路径经既有 `proxy.config` 回显,零新应答键;未命中/dev 无 home = 只看现状 `proxy.config=null`;手填 `config` 永远赢;非布尔 `invalid_params`) |
| 5 | `run.start` | `_m_run_start` | 启动 run 子进程,立即返回 run_id;单飞 `run_busy` |
| 6 | `run.status` | `_m_run_status` | run 注册表查询;未知 id = 结构化 404;缺省 `run_id` 全量视图 = 会话注册表(新→旧,行形状逐字节不变)在前 + DB runs 表「上一程」历史行接续(重启后日志屏翻得到上一程;10-07-logs-restart-visibility R1)——历史行 = RunEntry 键全在场超集:`history:true` 徽标 + `log_run_id` 会话对齐键(展开走既有 `logs.tail?run_id=<log_run_id>` 回填,零新协议;`yaml`/`exit_code` 无库源置 null、`dry` 恒 false、`state` 恒 done;`log_run_id` 旧库行 null = 无法对齐如实降级);同跑次按 `record.run_id` 去重不双列(会话计数器与 DB 自增两编号空间不同源,裸 run_id 必撞号),历史上限 50;无 `finished_at` 僵尸行不进历史(徽标下冒充运行中会说谎);库打不开/读失败降级仅注册表视图(run.cancel/单飞锁语义活在注册表侧);空库应答形状与现状全同;**形状兼容**:历史行只加徽标/对齐新键,旧前端忽略照跑,PROTOCOL_VERSION 不 bump(加法可选字段先例) |
| 7 | `run.cancel` | `_m_run_cancel` | 取消进行中 run:killpg(SIGTERM→5s→SIGKILL);信号终局 status=cancelled(v112 批 C2) |
| 8 | `runs.list` | `_m_runs_list` | runs 表直读(新→旧,limit 钳制 [1,200]);重启后历史可达(v112 批 C3) |
| 9 | `logs.tail` | `_m_logs_tail` | 环形缓冲尾部日志,run_id 可选过滤;数据面 = 统一日志模块 `myssia.log.ring_snapshot`(批1 切道,语义逐字对齐旧实现:run_id 过滤+尾部截取,lines 钳制 ≤ 环形帽 4000);serve 冷启动 `backfill` 盘尾回填(预算 2000 行:当日 `logs/myssia-*.jsonl` 尾+不足补前一文件尾,坏行跳过,按读入顺序 seed 环形重发 seq;壳 respawn 后崩溃前日志可达日志屏)——**params/result 形状零变化**、前端 `screens/logs/` 零改;`type:"log"` 事件发射点集合与旧实现逐点相同(10-07-unified-logging design §5) |
| 10 | `store.items` | `_m_store_items` | SQLite 单库直读情报流(新→旧);游标 `before`/`before_id` + `query`(v112 批 C1) |
| 11 | `feed.export` | `_m_feed_export` | 当前过滤视图导出 JSONL/CSV:sidecar 直写(数据不经 webview),只写对话框选定单文件;`export_path_invalid`/`export_write_failed`(feed-ux 批 G3) |
| 12 | `schedule.preview` | `_m_schedule_preview` | 品类排程 Next runs 预览(纯计算零副作用,count 钳制 [1,20];无排程明示 null 非 err;feed-ux 批 G4) |
| 13 | `secret.set` | `_m_secret_set` | 凭据只入系统钥匙链;值零回显零落日志 |
| 14 | `secret.list` | `_m_secret_list` | 只列名字,值永不可读 |
| 15 | `secret.delete` | `_m_secret_delete` | 删除凭据(误存清除口;二次删除 `secret_not_found`;v112 批 C5) |
| 16 | `sources.write` | `_m_sources_write` | 源启停写回(sources 屏私有封装) |
| 17 | `sources.test` | `_m_sources_test` | 试抓此源,异步 job(`test_busy` 单飞);结果走 `test.completed` 事件(v112 批 C13) |
| 18 | `yaml.list` | `_m_yaml_list` | config 目录品类 YAML 清单(坏文件也入列) |
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
| 36 | `image.files.purge` | `_m_image_files_purge` | 按 mtime 清 `<数据根>/images` 超龄落图 `{days}`(整数 ≥1)→ `{deleted, bytes_freed}`;只删文件不动目录(内容寻址平铺);CLI 面能力零 UI;目录不存在 = 合法零删(vision-v2 批复查) |
| 37 | `feed.enrich` | `_m_feed_enrich` | 情报流卡单条「AI 摘要」:`{item}`(items.id 或 dedup_key/URL,`resolve_item_ref` 同 `feedback.mark` 口径)→ `{item_id, model, scores, score, cached}`;骑 `shishi.enrich.LLMEnricher` 现跑(端点 = 条目所属品类 YAML `enrich:` 节 `env:`/`keychain:` 引用解析;enrich_cache 缓存语义复用,命中零 token;分数原路回填 items 表);async `enrich()` 在 handler 内 `asyncio.run` 同步应答,挂 `EnrichSettings.timeout_seconds` 超时;未启用/缺端点/品类 YAML 缺失 = `enrich_not_configured`(graceful;fe-small-batch 批 G8) |
| 38 | `alerts.list` | `_m_alerts_list` | 告警规则清单(全量 id 升序,启用/停用同行——启停 = save 全量提交):`{}` → `{rules:[AlertRuleView]}`;AlertRuleView = 规则全字段 + `fired_count`/`last_fired_at` 自 alert_fired 表派生(计数不落规则行,save 全量替换不清计数;alert-rules 批) |
| 39 | `alerts.save` | `_m_alerts_save` | 规则**全量替换**(承建/改/启停一体,不设独立启停方法;push.write 全量先例):`{rules:[AlertRuleInput]}` → `{ok, rules}`;两道门 = 逐条过构造门(shishi.alerts.compile_rule:name/scope/when 白名单语法/action/action_config 形状)任一失败 `alert_rule_invalid`(data 三键 index/field/reason)**整批零写入** + diff 落库(带 id 更新保 id/不带新建/库中多余 id 删除,fired 历史照留;空数组 = 清空回到零惊扰默认;alert-rules 批);AlertRuleInput/View **加法可选** `kind`('item' 缺省|'cron_stale')+`params`(心跳参数 `{threshold_hours}` 或 `{auto:true}`+可选 `job_id`;item 规则带 params 拒)——语义校验同走 compile_rule 构造门,PROTOCOL_VERSION 不 bump(gates 加法可选字段先例;10-05-cron-heartbeat) |
| 40 | `alerts.delete` | `_m_alerts_delete` | `{id}` → `{ok}`:删规则定义行,**fired 历史照留**(命中历史是事实);未知 id = `alert_not_found`(alert-rules 批) |
| 41 | `alerts.test` | `_m_alerts_test` | **dry 求值,不真发不落 fired**:`{rule?\|rule_id?, item?\|item_id?}` → `{matched, muted, actions, eval_error?, already_fired?}`;rule = 草稿(未保存即可测)/rule_id = 已存规则;item = 合成字段 dict(`Item.from_extracted` 构造,content 补丁生效)/item_id = 库内条目(求值上下文与引擎同门)/都缺 = 最近一条(空库 `alert_test_no_item`);muted = effective mute 压制(品类 watchlist + 反馈 0.0 词,命中即不评估);actions 展开 push 通道解析结果+降级原因 / tag 标签;already_fired 仅 rule_id 形态;真发测试借既有 `push.test`(alert-rules 批) |
| 42 | `runs.trend` | `_m_runs_trend` | run 成功率趋势(SQLiteStore.daily_run_outcomes:runs 表按 `substr(started_at,1,10)` UTC 逐日×status 聚合旧→新,`days` 钳制 [1,90] 缺省 14、`category?`、`db?` → `{days:[{date,total,statuses{…}}]}`,零数日补齐归前端 fillDailyOutcomes;statuses 开放词表原样分组,真实词表 4 态 running/success/partial/failed;服务端聚合而非前端算 runs.list —— limit≤200 在 cron 排程+手动 run 下 30 天窗可超限,截断会让序列静默失真;desktop-b234 批 G6) |
| 43 | `cron.list` | `_m_cron_list` | 定时 job 清单(`CronJobs.list_jobs`,缺省仅活跃;`all:true` 含暂停/终态;`db?` 覆写数据根;hermes-cron 批) |
| 44 | `cron.create` | `_m_cron_create` | 建定时 job:`{schedule, category, name?, deliver?, failure_deliver?, repeat?, timezone?, config?, run_timeout?, dry_run?, paused?, paused_reason?, db?}`;Q6 完整 `load_category_file` 早失败(`cron_category_invalid`,data=LoadError.to_dict)、Q5 绝对路径存储、时区链 timezone > 品类 YAML > 本地;schedule 解析/once 超窗/repeat 等 ValueError = `cron_create_failed`;origin=`{source:"desktop"}`(hermes-cron 批) |
| 45 | `cron.edit` | `_m_cron_edit` | 部分更新(同 create 可选字段):schedule 变更由底座重算 `next_run_at` 并重推导 repeat 缺省(once↔recurring 翻转);category 同款 Q6 早失败;空更新集 = `cron_edit_no_changes`;终态复活拒绝/解析失败 = `cron_edit_failed`(hermes-cron 批) |
| 46 | `cron.pause` | `_m_cron_pause` | 暂停 job(`reason?` 可选,F1.1);`{all:true}` = 全局急停 estop 标记(grill Q4:tick 跳过派发、在途 run 不受影响),与 `job` 互斥(hermes-cron 批) |
| 47 | `cron.resume` | `_m_cron_resume` | 恢复 job / 一次性重挂(`at?` = ISO 时刻,`rearm_oneshot`);`{all:true}` = 解除全局急停,与 `job`/`at` 互斥;recurring 拒 `at`/once 过窗 = `cron_resume_failed`(hermes-cron 批) |
| 48 | `cron.run` | `_m_cron_run` | 下次 tick 立即跑(`trigger_job`,manual 来源;复活 paused + 计入 repeat,§8.1 事实裁决;`manual_run_at=next_run_at`);终态 job 拒绝 = `cron_run_failed`(hermes-cron 批) |
| 49 | `cron.remove` | `_m_cron_remove` | 删 job 记录 → `{removed, job_id, name}`;output 目录与账本行保留(运行证据)(hermes-cron 批) |
| 50 | `cron.status` | `_m_cron_status` | ticker 活性快照(F1.6):`{ticker_alive, heartbeat_age_seconds, last_success_age_seconds, last_error, estopped, jobs_total, jobs_enabled, next_due_at}`;心跳新鲜窗 = interval×3+20s(CLI `cron status` 同公式);serve 内置 ticker 起过才活,dev 回退恒 not-alive(hermes-cron 批) |
| 51 | `cron.runs` | `_m_cron_runs` | 执行账本尾查(`ExecutionLedger.list_executions` 新→旧):`{job?, limit?=20 钳制 [1,500], db?}` → `{count, executions}`;`run_summary_json` 随行解析为 `run_summary`(D10 摘要快照;损坏串如实带 `{raw}`)(hermes-cron 批) |
| 52 | `store.state.mark` | `_m_store_state_mark` | 按 dedup_key 批量置位读态(G9):`{keys:[dedup_key,…], marker: read\|starred\|later, value, db?}` → `{updated}`(SQLite UPDATE rowcount 口径,匹配行数如实回传含置同值行;同键多行 dated-key 旋转同置,与 localStorage itemKey 语义一致;幂等;keys ≤2000 = 误用防线非容量声明,超限 invalid_params 提示走 mark_all;read-state-server 批) |
| 53 | `store.state.mark_all` | `_m_store_state_mark_all` | 全库置位(G9「全部标已读」全库语义来源):`{marker, value, category?, db?}` → `{updated}`;category 精确等值与 `list_items` 同参(非 LIKE,不收 query——决议 Q3.2 钉死);缺省 = 全库所有条目含未翻页/未加载;rowcount 口径同 mark(read-state-server 批) |
| 54 | `store.state.import` | `_m_store_state_import` | localStorage 读态一次性搬迁(G9 Q2 搬迁门):`{states: {<key>: {read?/starred?/later?}}, db?}` → `{imported, skipped}`;key 三分:dedup_key 直配/`id:<n>` 先解析到键/`id:<url>` 及无从解析形态如实计 skipped(已剪枝条目不复活);幂等旗标 = store_meta `feed_state_imported_at`(服务端是唯一真相,webview 清数据击不穿):已设 → `{imported:0, skipped:0}` 不触库,未设 → 导入后落 ISO 时间戳(read-state-server 批) |
| 55 | `gates.get` | `_m_gates_get` | gates.yaml 整读:`{}` → `{config, path, exists, error}`(config = GatesConfig.to_payload 同形状,凭据位只回 `keychain:` 引用永不回值;文件缺失 = 全关默认态 exists=false;**坏文件不 fail fast** —— fail-closed 全关态 + `error` 拒载明细(LoadError.to_dict)带回,设置屏是修复入口,一次合法 save 覆写修复,与 image.config.read 的 fail fast 不同属刻意;设置屏门槛件分区消费;10-05-plugin-market-batch 批二) |
| 56 | `gates.save` | `_m_gates_save` | gates.yaml 整存:`{config}` → `{ok, path}`(tmp+rename 原子写;`GatesConfig` 构造即校验,失败 `gates_config_invalid`(data=LoadError.to_dict)零落盘;缺 config 对象 = `invalid_params`;10-05-plugin-market-batch 批二) |
| 57 | `plugins.bundled.list` | `_m_plugins_bundled_list` | 随包插件组件包发现:`{}` → `{dir, count, plugins, categories}`(枚举 env `MYIA_BUNDLED_PLUGINS` 目录下含 plugin.yaml 的子目录,逐包 manifest 摘要 id/name/version/tier/gate/requires/provides + 版本兼容判定 + 已装态 installed/installed_version——对齐安装根 InstalledPluginStore 的 plugin_id;**双锚独立:组件包根与品类锚(`Resources/config`,布局探测)均缺席 = 合法空表** `{dir:null, count:0, plugins:[], categories:[]}`(dev 形态/旧包/未注入如实;单锚缺席不吞另一视图);坏 manifest 条目级 finding(manifest_invalid)不整表炸,沿 yaml.list 先例;目录名与 manifest id 不一致 → id_mismatch warning 如实透出;批二 R3 增 `categories` 键=平铺品类 YAML 发现视图(2026-10-11 拆分起源 `Resources/config`,与组件包目录分居,见 #66 行注);`count` 语义不变=组件包数;10-05-bundled-plugins-install,批二扩) |
| 58 | `plugins.bundled.install` | `_m_plugins_bundled_install` | 随包组件包一键装:`{id, force?}` → `{ok, dir, version}`(id 过 `_PLUGIN_ID_RE` 同门防穿越 → **三岔编排**(10-06-plugin-src-remote-fetch 改,源码不随包规范):①包内 plugins.lock.json 在+条目在 → `install_remote` 远取主路径(fetch→size/sha256 内容寻址校验→安全解包 `.staging/`→`InstalledPluginStore.install` 同门落位,finally 清残;远取失败词表 `plugin_fetch_failed`/`integrity_mismatch`/`plugin_archive_invalid`/坏锁 `plugin_lock_invalid` 结构化拒零静默);②锁缺席+包内目录携源码件(`*.py` 子树存在)→ 旧包直拷回退(原 `_locate_bundled_plugin_dir`+`store.install` 零改动,旧装机包自愈);③否则 `plugin_lock_missing` 结构化拒(防直拷纯声明件静默半装);store 同门不变:manifest 校验→版本矩阵→整目录拷贝绝不半装;已装未 force/版本不兼容未 force → PluginStoreError code 原文透传 already_installed/incompatible_version 等(已装未 force 远取路径零网络先拒);env 不可用 `bundled_plugins_unavailable`、id 不在目录 `bundled_plugin_not_found`;10-05-bundled-plugins-install,10-06-plugin-src-remote-fetch 改三岔) |
| 59 | `plugins.bundled.uninstall` | `_m_plugins_bundled_uninstall` | 随包组件包卸载:`{id}` → `{ok, id, path}`(id 过 `_PLUGIN_ID_RE` 同门 → 直调 `InstalledPluginStore.remove` 与 CLI `myssia plugin remove` 同门:删安装根 `<install_root>/<id>` 整目录,绝不半删;**随包原件只读永不删**,卸载后可随时经 #64 重装;**不依赖 bundled root**——卸载是安装根操作,`MYIA_BUNDLED_PLUGINS` 未设的 dev 形态/旧包同样可卸已装件,如实;PluginStoreError code 原文透传 not_installed/io_error;10-05-bundled-plugins-batch2 R2) |
| 60 | `plugins.bundled.category_install` | `_m_plugins_bundled_category_install` | 随包品类 YAML 平铺安装:`{id, force?}` → `{ok, file, path}`(与组件包安装语义刻意不同:品类=单文件平铺拷到 `<config_dir>/<源文件名>`,与 `_seed_first_run` 补种同落点;id 过 `CATEGORY_ID_RE`(schema 同源防穿越)→ 定位(文件名 stem 直配 > YAML id 字段兜底)→ `load_category_file` 校验通过才装(坏件 `category_invalid` 拒零拷贝)→ tmp+rename 原子拷贝;**已有同名文件未 force → `category_exists` 结构化拒如实「已存在」不覆盖**——与补种幂等补缺对齐不打架:补种=自动补缺永不覆盖,本面=显式知情,force 才覆盖;**id/冲突定义**:品类 id = YAML `id:` 字段(CATEGORY_ID_RE),冲突 = 数据根 config/ 下同名文件存在(文件级,内容同否不判);与组件包零冲突(组件包锚 Resources/plugins 子目录 vs 品类锚 Resources/config 平铺,2026-10-11 拆分);env 不可用 `bundled_plugins_unavailable`、id 合形不在目录 `bundled_category_not_found`;品类无卸载面(补种只补不删,删文件走 yaml-editor 屏);10-05-bundled-plugins-batch2 R3) |
| 61 | `plugins.remote.get` | `_m_plugins_remote_get` | 轨D remote 声明配置读:`{id}` → `{id, endpoint, token, known}`(id 过 `_PLUGIN_ID_RE` 同门;配置落数据根 `<home>/remote-plugins.json`,缺文件/缺条目 = endpoint/token null + known=false 如实;token 是 keychain 引用名,值永不出协议面——只有 secret.set 写入/secret.list 可见名;dev 形态无 MYIA_HOME → `remote_config_unavailable` 结构化拒(开发后门=显式 env);坏 JSON → `remote_config_invalid`;10-06-native-plugin-components 阶段3 G-Q1/R7) |
| 62 | `plugins.remote.save` | `_m_plugins_remote_save` | 轨D remote 声明配置写:`{id, endpoint, token?}` → `{ok, id, path, endpoint}`(endpoint 必填 http(s) 具体地址——env:/keychain: 引用属品类 YAML/env 通道不走本面板,违者 invalid_params;token 可选、给定必须是 keychain: 规范引用(secrets 名门同源校验),明文凭据只经 secret.set 入钥匙串永不落本配置,不传=保持现值;tmp+rename 原子写;写后即时 env 桥接——`_apply_remote_env_bridge` 把 firecrawl 端点/键桥进 `MYIA_FIRECRAWL_URL`/`MYIA_FIRECRAWL_API_KEY`(引擎零改动的通道;显式 env=开发后门恒优先,`_BRIDGED_ENV` 记账防覆写);10-06-native-plugin-components 阶段3) |
| 63 | `telegram.status` | `_m_telegram_status` | 三线状态快照(只读零副作用,设置页 Telegram 总卡初拉):`{}` → `{bot:{configured,error}, session:{exists}, web:{accounts:[{account, logged_in, logged_in_at, label?, user_id?, last_verified_at?, alive?, login_in_progress, login_note, check_in_progress?, check_note?}]}}`;bot.configured = `_resolve_credential_probe("keychain:myia/telegram/bot-token")` 探查(值零回显,占位值视同未配);session.exists = 数据根 `telegram/telethon.session` 在场;web.accounts = `telegram-web/` 下合法键目录 + 登录标记回读 + **浏览器模块操作台账**联读(login_in_progress/login_note 真源 = `browser.open` 操作记录,卡面 ↔ 模块同源联动)+ **体检台账**联读(check_in_progress/check_note 真源 = telegram.web.check 操作记录)+ 体检结论透传(last_verified_at/alive 从登录标记 marker 读,与 logged_in 双键并存不覆盖 —— 标记在场 = 复用快捷面,死只引导重登不清标记);新键全可选,旧 UI 忽略照跑(PROTOCOL_VERSION 不 bump,加法可选字段先例);数据根 = serve 上下文 home(dev 回退 cwd);10-08-tg-web-line W4;台账联读 10-08-browser-module;体检面 10-11-tg-manage-absorb) |
| 64 | `browser.open` | `_m_browser_open` | 浏览器操作统一入口(PRD 单入口铁律:一切浏览器操作必经浏览器模块,原 `telegram.web.login` 已随 v11 移除):`{kind, session_key, url?, force?}` → `{started, op_id, kind, url}`;kind 须在 `_BROWSER_KINDS` 登记词表(现役 `tg_web_login`,未登记类别 invalid_params+allowed——禁止旁路直启 Chromium);tg_web_login:session_key 过 `validate_account_key` 全称律、**依赖前置探针**(`require_playwright` 缺装 → `dependency_missing` 同步结构化拒,人话+修复指引,AC2 静默失败=反模式)、后台 daemon 线程跑既有 `TelegramWebLoginFlow`(注入 print_fn=日志尾巴/sleep=停令可中断/on_page_opened=窗口管理句柄,零重写)开 headed Chromium——**手机号+验证码(+2FA)全在浏览器页面内由用户输入,sidecar 零读取零落日志**;同 op 在跑 → `{started:false}` 幂等回执;op_id=会话键;10-08-browser-module 案甲) |
| 65 | `telegram.web.delete` | `_m_telegram_web_delete` | 删网页线账号配置档:`{account}` → `{deleted, account, existed}`(键同门校验;登录窗在跑 → `login_in_progress` 结构化拒,指引去「浏览器」模块关窗;`shutil.rmtree` 整档删除,登录态随档消失;浏览器台账同键同清;幂等——档缺同样 `{deleted:true}`;源 YAML 引用该键的 tg_web 源此后显式空态;10-08-tg-web-line W4) |
| 66 | `browser.list` | `_m_browser_list` | 浏览器操作台账(设置 →「浏览器」分区模块页):`{}` → `{operations:[{op_id, kind, session_key, url, phase, note, fix_hint, started_at, finished_at, log_tail[]}], kinds}`;phase = `running`/`done`/`failed`/`closed`,最新在前;失败行带人话 note + 修复指引 fix_hint(依赖缺失/浏览器二进制缺失/登录超时三族人话化);log_tail = 环形日志尾巴(60 行容量,投影最近 20);线程内句柄(stop_event/page/loop)不外泄;台账为进程内会话态,重启即清(登录态落配置档不受影响);10-08-browser-module 案甲) |
| 67 | `browser.focus` | `_m_browser_focus` | 聚焦进行中操作的浏览器窗口:`{op_id}` → `{focused, op_id}`(经登录线程事件循环 `run_coroutine_threadsafe(page.bring_to_front)`——Playwright async 对象只能在其归属循环上动);未知操作 → `unknown_operation`;终态/窗口未就位 → `window_not_active`;跨线程调度失败 → `focus_failed`;10-08-browser-module 案甲) |
| 68 | `browser.close` | `_m_browser_close` | 请求关闭进行中操作的浏览器窗口:`{op_id}` → `{closed, op_id, note}`(置停令 → 注入 sleep 抛 `_BrowserWindowClosed` → 登录流 finally 关 context,台账转 `closed`;登录态已落档的不受影响);未知操作/终态 → `unknown_operation`/`window_not_active` 同 focus;10-08-browser-module 案甲) |
| 69 | `store.source_stats` | `_m_store_source_stats` | 分源聚合(v8 三级界面 1 级类型卡统计底座):`{since?, db?}` → `{db, rows:[{source, total, today, unread, latest_first_seen, latest_title}]}`(每源一行 GROUP BY source,新→旧按 MAX(first_seen) 排;today = `first_seen >= since` 条数,since = 当日窗锚 ISO(`dayWindowStart().toISOString()` 与视图同源),省略 = today 恒 0「无窗无今日」;unread = 未标已读 COALESCE(read,0)=0,不含 later 到期重现加成;latest_title 二遍逐源取同刻最新 id;NULL source 行照出 `source:null`,归并口径在 UI;非法 ISO = `invalid_params`;UI 能力门 STATS_PROTOCOL = 14 未过门不发 RPC 试错;10-09-tg-category-entry v8) |
| 70 | `platform_accounts.status` | `_m_platform_accounts_status` | 平台账号快照(配置组「本身账号」面,裁定语义 = 本身账号 ≠ 推送机器人,机器人凭据仍归设置→推送;10-11-platform-account-config):`{}` → `{feishu:{accounts:[{account,label,authorized_at,refresh_ok,refreshed_at}], authorize_in_progress}, weixin: probe_bridge 七键}`;feishu 静态快照(目录即账号 `<数据根>/feishu-accounts/<键>/`,零网络),刷新探针显式走 feishu.probe;weixin 零新契约直读桥三布尔,探测缺位降级灰态不炸 |
| 71 | `platform_accounts.feishu.authorize` | `_m_platform_accounts_feishu_authorize` | 发起飞书账号授权:`{account, label?}` → `{authorize_url, redirect_uri, account}`(user_access_token 授权码流;系统浏览器开授权页 + 本地回调端点 `127.0.0.1:8731/callback` 接 code → 换 token 对入钥匙链 `myia/<账号键>/user_access_token`+`/refresh_token` + 写标记 + 尽力首刷);键全称律 `feishu-<标识>`;同键授权中 → `authorize_in_progress`;App 凭据缺失(env→钥匙链 `myia/push/FEISHU_APP_ID/SECRET` 回退后仍无)→ `feishu_account_app_credential_missing`(指引设置→推送,账号线复用同一应用);端口占用 → `authorize_endpoint_unavailable`;端点仅绑 127.0.0.1,5 分钟超时自停(10-11-platform-account-config) |
| 72 | `platform_accounts.feishu.delete` | `_m_platform_accounts_feishu_delete` | 删飞书账号:`{account}` → `{deleted, account}`(钥匙链两 token 项 + 账号目录;授权进行中 → `account_delete_in_progress` 拒;键同门校验;镜像 telegram.web.delete 口径;10-11-platform-account-config) |
| 73 | `platform_accounts.feishu.probe` | `_m_platform_accounts_feishu_probe` | 刷新闭环探针:`{account}` → `{account, refresh_ok, refreshed_at?|reason?}`(refresh 可成功 = 绿且新 token 对回写钥匙链 = 续期闭环;失败是**状态**不是异常:`refresh_ok:false`+`reason` 置灰;无 refresh_token = `feishu_refresh_token_missing` 同形态指引重授权;UI「重新检查」钮 + 授权回调成功后自动一发;10-11-platform-account-config) |
| 74 | `telegram.web.check` | `_m_telegram_web_check` | 账号登录态体检(10-11-tg-manage-absorb AC1):`{account}` → `{started, account, note}`;键同门校验(`invalid_account`)/配置档缺 `profile_missing` 同步拒/依赖前置探针 `dependency_missing`(判例 browser.open)/登录窗在跑 `login_in_progress` 拒(判例 telegram.web.delete)/同键体检在跑 → `{started:false}` 幂等回执。**分层并发相处**(三占用者共用 profile_dir,Chromium 单实例锁使第二开者必败):常态面(TG 监控主使用态)= 读常驻哨兵真源零新浏览器 —— manager 单实例槽 `_TELEGRAM_WEB_MANAGER`(装配挂/_close 摘)`status()` 该键 running 且无告警 = 活(note 带 `web_monitor_sentry`;哨兵 60s 周期在查),哨兵已记 `tg_web_logged_out` = 死(note 带哨兵 detail)→ `web_line.record_verification` 落标记 + 台账 done,毫秒级秒回不起线程;槽空/dev/serve 未起 = 无常驻占用走探针路径:daemon 线程 `asyncio.run(check_logged_in)`(每线程新 loop,≤45s)→ 结论 `record_verification` 落标记 + 台账 done;探针异常(含 TelegramWebError re-raise 面)/`probe_failed:*` = 台账 **failed** + note 人话「常驻 web 线/登录窗/批量采集占用配置档时探针会冲突失败;先停监控或关登录窗再测」(批量采集独立进程无法感知,只能人话兜底)—— 整体 try/except 兜底绝不卡 running(否则同键永久幂等拒 + status 行 check_in_progress 永真);结果面经 `telegram.status` 行小字回读(last_verified_at/alive/check_note) |
| 75 | `wechat_local.probe` | `_m_wechat_local_probe` | 微信本机桥三态探针(10-11-wechat-ui-bridge F2):`{}` → 桥 `--probe` 载荷原样(`{ok, state, checks, wechat_version, bridge_version, reasons[, config]}`,三态 = ok/degraded/bridge_unavailable,判据矩阵在桥内;checks 含 screen_recording——2026-10-12 勘误:AX 定论死路后像素链为唯一读路,degraded 驱动权限=屏幕录制(AX 仅保留报告不驱动),reason 码 screen_recording_denied 映射通道错误族 11);实现本体 `myssia.wechat_local_sidecar`(随包),薄壳换轨 `WechatLocalSidecarError`→`ProtocolError`;**健康面自健康**——组件缺席/超时/应答不可解析都返回同形合成载荷(state 恒 bridge_unavailable,reasons 带 component_missing/probe_timeout/probe_unparseable),永不抛;探针零成本零读取(不读消息内容);UI「微信本机」卡三态派生唯一真源 |
| 76 | `wechat_local.sessions` | `_m_wechat_local_sessions` | 微信本机会话列表(10-11-wechat-ui-bridge F4 只读入口第一步):`{limit?}` → 桥 `sessions list --json` 载荷(`{sessions:[{id,name,unread}]}`,首版 N=20,limit 1..100);只读浏览面不经目录不落 store;桥 Phase C 未落地如实 `not_implemented`(exit 1 过渡码原样透传,不谎报具名族);bin 缺失 `component_missing`、超时 `bridge_timeout`(60s kill 兜底) |
| 77 | `wechat_local.messages` | `_m_wechat_local_messages` | 微信本机最近消息(10-11-wechat-ui-bridge F4;G2 读回展示):`{chat_id, count?}` → 桥 `messages read` 载荷(`{messages:[{ts,sender,type,text?,media_placeholder?}]}`,缺省 K=50,count 1..200);**读回仅展示不入情报管线**(G3:零 store/dedup/分类接线);媒体类 = 类型+占位描述不识别内容(prd R1a);参数门 invalid_params(path 精确到 params.chat_id/params.count) |
| 78 | `wechat_local.query` | `_m_wechat_local_query` | 微信本机本地库查询(10-11-wechat-ui-bridge F2;E 段三域只读):`{chat_id, since_days?}` → 桥 `localdb query --since Nd --json` 载荷(`{chat_id, since_days, messages, display_name, sessions, domains, copy}`);G4 message/session/contact 三域;since_days 缺省 30(design §7 limits.history_days 同值)、上界 3650 防呆;**超时 600s**(独立于 60s 命令族:桥侧 sqlcipher 单库解密上界 300s,多域副本首建累计可超 60s,600s=2×单库上界盖住;副本 kept 语义让 kill 后重试只补缺库);密钥途径未闭合如实 `key_unavailable`(exit 21,D4 语义;外部密钥 keys.json 重验通路 resolve_keys,D4② 一步闭合)/副本缺 `decrypt_failed`(exit 22)/定位失败 `db_not_found`(exit 20);聊天内容只在应答载荷(stdout 契约),sidecar 层零日志零落盘(红线 6) |
| 79 | `wechat_local.page` | `_m_wechat_local_page` | 微信本机分页查询(10-14-wechat-chat-export R7;keyset 游标续拉):`{chat_id, cursor?, limit?, asc?, from_ts?, to_ts?, types?, sender?}` → 桥 `localdb page` 载荷(`{page:{chat_id,display_name,messages,next_cursor,has_more,filter,page_size}}`;E2 副本域 message+contact,尾部 wxid→显示名批量解析);limit 帽 1000;types 数组→CLI 逗号;游标 scope 不符/未知类型名 → `invalid_cursor`/`invalid_types`(exit 2 原样);超时 600s(判例 query);实现本体 `myssia.wechat_local_sidecar._page` |
| 80 | `wechat_local.conversations` | `_m_wechat_local_conversations` | 微信本机会话普查(10-14-wechat-chat-export R7):`{limit?}`(帽 5000)→ 桥 `localdb conversations` 载荷(`{conversations:[{chat_id,display_name,is_group,msg_count,first_ts,last_ts}],total,unresolved_tables}`;逐表 COUNT/MIN/MAX+副本指纹缓存);超时 600s |
| 81 | `wechat_local.stats` | `_m_wechat_local_stats` | 微信本机统计查询(10-14-wechat-stats-reports R5;四模式中继):`{mode∈chats|chat|annual|dual, chat_id?, since_days?|all?, year?, refresh?}` → 桥 `localdb stats` 载荷(单遍 GROUP BY 聚合+文件缓存 `<数据根>/wechat-bridge/stats-cache/`);实现本体 `myssia.wechat_stats_sidecar`(独立模块,复用 `_run_bridge`/错误族);查询层降级恒 exit 0,密钥链 20/21/22 透传;超时 600s |
| 82 | `wechat_local.stats_report` | `_m_wechat_local_stats_report` | 微信统计 AI 叙事报告(10-14-wechat-stats-reports R5;MYIA 侧不重查):`{mode, stats_payload, tone?}` → 报告文本;端点 = `<数据根>/config/wechat-stats.yaml`(enrich 段形态,凭据引用制明文拒载);`enabled:false`/端点缺 → `ai_disabled`,openai 包缺位 → `dependency_missing`(结构化);隐私缺省:纯聚合数字+top 短语,**零逐条消息原文**(入口防御性递归剥 messages) |
| 83 | `wechat_local.sns_feed` | `_m_wechat_local_sns_feed` | 微信朋友圈动态(10-14-wechat-media-sns R5;只读):`{since_days?}`(缺省 30,帽 3650)→ 桥 `localdb sns feed --since Nd --json` 载荷;argv 契约钉死在 tests/desktop/test_wechat_local_media_handlers.py;超时 600s(盖副本首建) |
| 84 | `wechat_local.sns_export` | `_m_wechat_local_sns_export` | 微信朋友圈导出(10-14-wechat-media-sns R5):`{format?∈json|html(缺省 json), out?, since_days?(缺省 30), with_media?(缺省 false)}` → 桥 `localdb sns export` 载荷(`{sns_export:{format,out_dir,files,with_media,stats}}`);`with_media=true` = 唯一受限 CDN GET 豁免(docs/wechat-mediadecrypt.md §11);超时 600s |
| 85 | `wechat_local.media_scan` | `_m_wechat_local_media_scan` | 微信会话媒体寻径(10-14-wechat-media-sns R5):`{chat_id, since_days?(缺省 30), decrypt?(缺省 false)}` → 桥 `localdb media scan` 载荷(`{media:{items,stats,provider}}`;缩略图优先寻径,decrypt 逐条解密回填 cached_path);未配置解密件+decrypt → `media_unavailable`(exit 23 原样);超时 600s |
| 86 | `wechat_local.media_decrypt` | `_m_wechat_local_media_decrypt` | 微信单件媒体解密(10-14-wechat-media-sns R5):`{dat_path}` → 桥 `localdb media decrypt` 载荷(`{media_decrypt:{dat_path,cached_path,ext,is_wxgf,width,height,cache}}`;解密钥仅内存过手不落盘);未配置解密件 → `media_unavailable`(exit 23);超时 600s |
| 87 | `wechat_local.contacts` | `_m_wechat_local_contacts` | 微信联系人六桶(10-14-wechat-contacts R6;分类浏览/找回考古):`{type?∈friend|group|official|former|other, keyword?, limit?(0..1000,0=全量导出态), cursor?, with_residue?, include_stranger?(只收开态,false=invalid_params——桥 CLI 缺省开无关闭旗标)}` → 桥 `localdb contacts` 载荷(`{contacts:{counts,former_tiers,residue_checked,strict_residual_count,labels,stranger,room_verify,rows,next_cursor,has_more,filter,page_size,degraded}}`);with_residue 触发 message 域副本首建 → 超时 600s(不用 60s 命令族帽);缺表降级恒 exit 0 |
| 88 | `proxy.probe` | `_PROXY_PANEL["proxy.probe"]` | 代理池逐上游探测+快照落盘(task 10-14-proxy-pool-panel R1):`{config?, config_auto?, probe_timeout?}`(DoctorParams 子集)→ doctor 应答原形状+纯增键 `snapshot:{persisted, reason?}`(实现=字面复用 `_m_doctor` 零分叉,config_auto 非布尔门继承);落 `<home>/proxy-probe-history.jsonl` 一行一快照 {at,config,pools}(pools 行引擎已打码;保留帽 200 裁最旧原子重写;文件 0600);落盘失败不 fail 探测(persisted=false+reason: no_home/write_failed/no_proxy_section) |
| 89 | `proxy.history` | `_PROXY_PANEL["proxy.history"]` | 探测历史零网络纯读:`{limit?(钳制[1,100]缺省20), pool?}` → `{snapshots:[{at,config,pools}], count, truncated, home_available, skipped?}`(新→旧;pool 过滤只回该池行;坏行跳过 skipped 如实;文件不存在=合法空表;home_available=false=dev 无数据根);实现本体 `src/myssia/proxy_panel.py` |
| 90 | `credhunter.keys.list` | `_m_credhunter_keys_list` | 凭证猎手面板数据面(task 10-14-cred-hunter-panel §3.1):`{}`(多余键忽略,gates.get 同门)→ `{path, exists, version, count, records[]}`——本地密钥库 `credhunter-keystore.json` **纯文件读**(零网络零写入,库缺绝不建档);records 按 last_seen 新→旧,行 = `{fingerprint, masked_apikey, provider, first_seen, last_seen, hit_count, sources[], last_check, check_state}`,**无 apikey 键**(全文在 handler 投影时丢弃,Q9 掩码-only:前 8+`…MASKED…`+后 4,长 9-12 只前 8、≤8 只前 2);库不存在 = 合法未建库态 `{exists:false, version:null, count:0, records:[]}`;坏 JSON/结构不符(version≠1)→ `keystore_invalid`、IO 不可读 → `keystore_unreadable`(同名镜像插件 `keystore.py` 错误族;路径/掩码规则内联镜像 `keystore.py:78-86`/`findings.py:54-66`,插件动态加载不 import);数据根 = `MYIA_HOME` env > cwd(镜像 `default_keystore_path`);消费方 = `screens/credhunter/` 屏私有封装 |
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
read-state-server 批(task 10-04-read-state-server,协议件)新增 3:58-60
`store.state.mark`/`mark_all`/`import`(G9 读态迁服务端三方法;`store.items`
投影连带补 `read`/`starred`/`later` 三布尔键,feed.export JSONL 同源连带、
CSV 固定列集不变);协议 v10——竞速条款落地:hermes-cron 已先合入 v9,
本批开工实读 `PROTOCOL_VERSION`=9 后 +1 = 10(alert-rules 先例,按合入
顺序定案)。
plugin-market-batch 批二(task 10-05-plugin-market-batch 第 11 步)新增 2:
61-62 `gates.get`/`gates.save`(门槛件知情启用配置 `<home>/gates.yaml` 读写,
设置屏门槛件分区消费;能力实现 `src/myssia/gates.py`,契约 = 任务档
design.md §6.7 + entry.py `_m_gates_get`/`_m_gates_save` 实况——get 应答较
§6.7 早稿多 `exists`/`error` 两键:坏文件 fail-closed 不炸设置屏,拒载明细
带回,保存即覆写修复)。**协议版本未随批 bump**:地基路定案维持 v10(两方法
在 v10 内交付,注册表 62 行;gates UI 无 protocol 版本能力门,旧壳+新 UI
组合经 method_not_found 结构化降级不白屏;若后续补 bump v11,版本用例随迁)。
g10-proxy-probe 批(task 10-05-g10-proxy-probe)给既有 `doctor` 增可选布尔
`config_auto`(注册表 #4 行注;设置屏代理区「探测」留空路径一键化:sidecar 以
serve 上下文数据根发现缺省 `<home>/pools.yaml`,命中才拼 `--config`,发现逻辑
全在 entry.py `_m_doctor`,cli.py 零改动)——**同样不 bump**:零新方法零新
应答键、缺省 false 现行为逐字节不变,旧壳+新 UI 组合旧 `_m_doctor` 忽略未知
键照跑(不带 config,`proxy.config=null` 前端提示行降级),循 gates 先例维持
v10。
bundled-plugins-install 批(task 10-05-bundled-plugins-install)新增 2:
63-64 `plugins.bundled.list`/`install`(随包插件组件包发现与一键装——壳层
spawn 时注入 `MYIA_BUNDLED_PLUGINS=Resources/plugins`(release 且用户未显式
设才注入;dev 构建定死不注入 = 空表稳定契约,防枚举仓库 plugins/ 20 件未打包
件致断言数字两态漂;壳侧 pyenv.rs `bundled_plugins_env_value` 与本表注册 63/64
行为同一套),发现/安装全走 sidecar 单一事实源,UI 零 resourceDir 直查;装卸门
零新增 = 直调 `InstalledPluginStore.install` 与 CLI 同门(见注册表 64 行注)。
**协议版本未随批 bump**:循 plugin-market-batch gates 批二「地基路」先例——
旧壳+新 UI 组合下设置屏「装机组件」分区经 method_not_found 结构化降级(不
白屏),与 gates UI 无版本能力门同款;注册表 64 行。
bundled-plugins-batch2 批(task 10-05-bundled-plugins-batch2,前轮四件翻案)
新增 2:65 `plugins.bundled.uninstall`(卸载=删安装根拷贝,直调
`InstalledPluginStore.remove` 与 CLI `myssia plugin remove` 同门;不依赖
bundled root,dev 形态可卸)+ 66 `plugins.bundled.category_install`(品类
YAML 平铺安装,与补种同落点;已存在未 force 拒,force 才覆盖——两语义对齐
不打架:补种自动补缺永不覆盖,安装面显式知情);#63 连带增 `categories`
发现键(`count` 语义不变)。**同样不 bump v10**:循本族「地基路」先例——
旧壳+新 UI 组合下卸载钮/品类分区经 method_not_found 结构化降级不白屏,
新增应答键(`categories`)旧 UI 忽略零回归;注册表 66 行。
native-plugin-components 阶段3(task 10-06-native-plugin-components,
G-Q1/R7 轨D)新增 2:67-68 `plugins.remote.get`/`save`(remote 插件件
端点/凭据引用配置,落数据根 `<home>/remote-plugins.json`;设置屏「随包
官方插件件」卡条目详情区 remote 配置面板消费)。**不 bump v10**:两方法
加法,旧壳+新 UI 组合经 method_not_found 结构化降级(面板区静默不渲染),
循 bundled 族先例;注册表 68 行。连带两处既有面扩展(零新方法):①
serve 启动 `_startup_remote_env` 把数据根 remote 配置桥接进 env
(`MYIA_FIRECRAWL_URL`/`MYIA_FIRECRAWL_API_KEY`,setdefault 语义=显式 env
开发后门恒优先;firecrawl 桌面态端点由面板提供、引擎代码零改动);②
`doctor`(#4)应答增 `firecrawl` 键(cli.py `_doctor_firecrawl`:未配置
`{configured:false,probe:null}` 零 finding 不红;配置了才 GET 端点根探活,
不可达 warning `firecrawl_unreachable`,消息只含展示形态不落解析值)——
应答加法旧 UI 忽略零回归,同样不 bump。
tg-web-line W4 批(task 10-08-tg-web-line)新增 3:69 `telegram.status` /
70 `telegram.web.login` / 71 `telegram.web.delete`(设置页 Telegram 总卡
数据面)。**不 bump v10**:循 bundled 族「地基路」先例——旧壳+新 UI 组合
经 method_not_found 结构化降级不白屏。
browser-module 批(task 10-08-browser-module,案甲)**改形 +1 净增 3**:
移除 `telegram.web.login`(单入口铁律:一切浏览器操作必经浏览器模块,
Telegram 卡「添加账号/重新登录」改调 `browser.open`,禁止旁路直启
Chromium)+ 新增 70 `browser.open` / 72 `browser.list` / 73 `browser.focus`
/ 74 `browser.close`(操作台账/窗口管理/日志尾巴);`telegram.status` 的
web 段改为台账联读(应答形状零变)。**bump v11**:本批含**移除**——
旧 UI(调 telegram.web.login)+ 新壳组合会 method_not_found,版本门
是两侧对齐的唯一信号;注册表 74 行。
tg-manage-absorb 批(task 10-11-tg-manage-absorb)新增 1:80
`telegram.web.check`(账号体检;契约见注册表 80 行注)+ `telegram.status`
web 行新可选键(last_verified_at/alive/check_in_progress/check_note)。
**不 bump v15**:循 gates/run.status 历史行批「地基路」纯加法先例 ——
新方法旧壳经 method_not_found 结构化降级不白屏,新键旧 UI 忽略照跑;
注册表 80 行。
wechat-ui-bridge F2 批(task 10-11-wechat-ui-bridge)新增 4:81-84
`wechat_local.probe`(微信本机桥三态探针)/ `wechat_local.sessions` /
`wechat_local.messages`(只读命令族,F4 消息屏只读入口数据面)/
`wechat_local.query`(本地库三域查询)。实现本体 = `myssia.
wechat_local_sidecar`(随包打包),entry.py 只留四枚三行薄壳;桥具名
错误族(design §6 码表)原样透传。**不 bump v15**:同上地基路纯加法
先例(新方法旧壳 method_not_found 结构化降级,消息屏「微信本机」卡
按灰态呈现即正确行为);注册表 84 行。
六域接线批(0.8.0,task 10-13-wechat-features 集成员)纯加法 9:85-93
`wechat_local.page`/`wechat_local.conversations`(10-14-wechat-chat-export
C1 分页+普查)、`wechat_local.stats`/`wechat_local.stats_report`
(10-14-wechat-stats-reports C2;stats_report 实现本体在独立模块
`myssia.wechat_stats_sidecar`)、`wechat_local.sns_feed`/
`wechat_local.sns_export`/`wechat_local.media_scan`/
`wechat_local.media_decrypt`(10-14-wechat-media-sns C3)、
`wechat_local.contacts`(10-14-wechat-contacts C4)。**不 bump
PROTOCOL_VERSION**:同上地基路纯加法先例;注册表 93 行。
proxy-pool-panel 批(task 10-14-proxy-pool-panel)新增 2:94-95
`proxy.probe`/`proxy.history`(代理池只读面板数据面:探测=字面复用
`_m_doctor`+快照落盘,history=零网络纯读;实现本体
`src/myssia/proxy_panel.py`,工厂注入 entry 依赖)。**不 bump v15**——
同地基路纯加法先例,旧壳经 method_not_found 结构化降级;注册表 95 行。
cred-hunter-panel 批(task 10-14-cred-hunter-panel)新增 1:96
`credhunter.keys.list`(凭证猎手面板数据面:本地密钥库掩码-only 只读
列表,契约见注册表 96 行注;前端共享映射 `SidecarProtocol` 同批 +1 行,
消费方 `screens/credhunter/` 屏私有封装)。**不 bump v15**——同地基路
纯加法先例;注册表 96 行。

**store.items 参数(合流形状,v112 批 C1 × feed-ux G1/G3)**:`db/category/since/limit`
之外增 `before`(ISO,first_seen 严格小于)、`before_id`(与 before 组成
`(first_seen, id)` 复合游标,成对出现)、`query`(title/content/source 三列
LIKE NOCASE,%/_ 按字面转义)。旧调用零感知。v10(read-state-server 批)起
`_item_dict` 投影随行带 `read`/`starred`/`later` 三布尔键(G9 读态迁服务端:
采集管线永不携带读态,置位只走 `store.state.*`;旧 UI 忽略新键零回归);
`feed.export` JSONL 共用同一投影连带多三键(加法变化),CSV 固定列集不变。
v13(feed 计数口径根治批,10-09-tg-category-entry F2)起 `store.items` 增可选
布尔 `with_total`:true 时同一 WHERE 跑 `SQLiteStore.count_items`(store 层
`_items_filter_sql` 单点构造,与 `list_items` 严格同口径),应答补 `total` =
该过滤条件全量行数(不含 limit 分页)——feed 屏「已加载 N · 共 T 条」的 T,
首页截断不再静默低估;缺省/false 应答无 `total` 键(旧调用零感知,旧 sidecar
+ 新 UI 组合 UI 回落「已加载 N 条」词面)。**bump v13**(UI 能力门
COUNT_PROTOCOL = 13)。

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
serve 内置 cron ticker,契约见下段)、
v10(read-state-server 批 `store.state.*` 三方法 + `store.items` 投影补
`read`/`starred`/`later` 三键;契约见注册表 52-54 行与 store.items 段注记)、
v16(vision-model-path 批:`image.models.*` 四方法 + `image.server.*` 两方法
与三事件**移除**——看图本地通道改 LM Studio 客户端制,vision.yaml `local`
增可选 `api_key` 键、缺省 base_url 改 `:1234/v1`;见下段)。
plugin-market-batch 批二 `gates.get`/`gates.save`(契约见注册表 55-56 行)
未随批 bump,在 v10 内交付(地基路定案,理由见上方批注段)。

**vision-v2 批立、vision-model-path 批收窄(task 10-03-vision-v2 立;
10-15-vision-model-path 客户端制收窄,协议 v16)**:`image.models.*` 四方法、
`image.server.*` 两方法与 `image.models.progress/completed`、
`image.server.completed` 三事件已移除——MYIA 不自跑视觉大模型,本地看图 =
LM Studio 等 OpenAI 兼容端点的纯客户端(vision.yaml `local` = base_url /
model / api_key 三件套,能力实现 `myssia.vision.client`,配置面只剩
`image.config.*`);`image.files.purge {days}`(整数 ≥1)保留。管线侧
`vl:local` 前的 server ensure 环同批拆除(端点不在跑 = 既有
`vl_skipped_error` 降级)。
`store.items` 的 `_item_dict` 白名单投影补
`image_caption` / `image_files` / `image_ocr_lines` **三键**(随落图开关
产生;`image_ocr_lines` 逐行 `{text, conf}` 原样透传供详情逐行置信度渲染,
形态不符整体置 None 不半投影——`image_ocr` 旧键 vision-pipeline 已有)。

`_item_dict` 白名单再补两组**渠道差异化呈现键**(task 10-06-feed-channel-groups,
同「显式才有/异型置 None」纪律;feed.export JSONL 连带,CSV 固定列集不变):
价格/优惠七键 `price_text` / `sale_price` / `normal_price` / `final_price` /
`original_price` / `discount_pct` / `savings_pct`(键名 = games 四源 extract
字段原样;`final_price` 兼收 Epic·Steam 人民币分 int 与 CS·GOG 美元串别名,
换算归消费侧)+ urlwatch 事件两键 `watch_event`(new|changed)/ `watch_page`
(目标页真链;条目 url 是 `#watch-<sha>` 锚,目标页链接以本键为准)。前端
渠道类型判定:telegram-*/tg-* 前缀(源名规约)→ 消息卡;engine=urlwatch
(health().plugins[].sources[].name→engine 映射)或 watch_event → 变更事件;
engine=prompt/store_report → 日报文档;品类 games/wool 或价格键存在 → 价格行;
其余走默认新闻列表卡。同批 `store.items` 增 `source` **精确等值**参数
(与 `category` 同门,非 LIKE;空串/非字符串 invalid_params)—— 三级下钻
L1 品类 → L2 渠道 → L3 渠道消息流(`category`+`source`+游标组合联查)的
L3 查询面。

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
channel ∈ `shishi.push.CHANNELS` + 可选 targets/template,tag 需非空 tags;
加法可选 `kind`('item' 缺省|'cron_stale')+`params`——cron_stale 钉品类
scope+when 恒 'true'+阈值二选一,item 带 params 拒;旧载荷零 kind/params =
item 语义零漂移,10-05-cron-heartbeat 批,PROTOCOL_VERSION 不 bump),
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
| 门槛件 | `gates_config_invalid`(另复用 `invalid_params`) | `gates.save` 载荷未过 `GatesConfig` 同门校验(明文凭据 `credential_plaintext`/未知字段/非法 endpoint 等;data = `LoadError.to_dict` 的 errors[] 明细)零写入;`gates.save` 缺 config 对象 = `invalid_params`(`gates.get` 不校验 params —— 多余键忽略,仅入口层「params 非对象」通用拒绝;task 10-05-plugin-market-batch 批二第 11 步,遗留修对齐代码实况) |
| feed-ux 导出 | `export_path_invalid` / `export_write_failed` | `feed.export`:路径空/相对/父目录不存在 / 写盘 IO 失败(task 10-03-feed-ux G3) |
| feed-ux 排程 | `invalid_cron`(防御性;另复用 `invalid_params`/`not_yaml_suffix`/`path_outside_root`/`source_file_unreadable`) | `schedule.preview`:`build_cron_trigger` 兜底 / 参数 / 围栏 / 品类装不上(task 10-03-feed-ux G4) |
| 单条精评 | `enrich_not_configured` / `enrich_timeout` / `enrich_failed`(另复用 `invalid_params`/`item_not_found`/`store_corrupt`;`EnrichConfigError` code 动态透传) | `feed.enrich`:品类未启用 enrich/缺端点引用/品类 YAML 缺失(graceful,`data.reason` 三分)/ `asyncio.run` 整段超时 / 条目未获分(degrade_reason+failures 入 data);凭据解析失败透传 `credential_unresolved` 等(fe-small-batch 批 G8) |
| 消息 | `unknown_platform` / `discover_not_supported` / `channel_refresh_failed` / `alias_write_failed` / `push_write_unsupported`(另复用 `category_invalid` / `file_not_found` / `path_outside_root` / `source_write_failed` / `invalid_params`) | channels.* / push.write 全链路(task 10-03-messaging-ui;数据面错误码透传 push 层如 `credential_not_found` 经 `channel_refresh_failed.data.code` 携带) |
| 看图模型/服务 | `download_busy` / `ensure_busy`(另复用 `invalid_params`;activate 改写 vision.yaml 失败复用 `image_config_invalid`) | image.models.* / image.server.* 单飞拒绝与参数形状;`VisionModelError`/`VisionServerError` code 透传(delete/activate 走应答错误,download/ensure 走完成事件 error 字段,枚举见上方 vision-v2 契约段;task 10-03-vision-v2) |
| 告警规则 | `alert_rule_invalid` / `alert_not_found` / `alert_test_no_item`(另复用 `invalid_params` 互斥门/载荷形状、`item_not_found` 的 item_id 形态) | `alerts.save` 某条构造期拒(data `{index, field, reason}`,整批零写入)/ `alerts.delete`·`alerts.test`(rule_id 形态)·`alerts.save`(载荷未知 id)未知 id / `alerts.test` 缺省取材空库(task 10-04-alert-rules;求值错/mute/降级/发送失败 = 非协议错,WARNING 隔离走 logs.tail) |
| 定时任务 | `cron_category_invalid` / `cron_create_failed` / `cron_edit_failed` / `cron_edit_no_changes` / `cron_resume_failed` / `cron_run_failed` / `cron_ambiguous_job` / `cron_job_not_found`(另复用 `invalid_params` 参数形状/all 与 job 互斥) | `cron.create`/`cron.edit` 品类 YAML 装不上(Q6 早失败,data=LoadError.to_dict)/ `create` 的 schedule 五形态·once 超窗·repeat·paused 自相矛盾(ValueError 原文)/ `edit` 的 schedule 变更解析失败·终态复活拒绝 / `edit` 空更新集 / `resume` 的 recurring 拒 at·once 过窗 / `run` 终态 job 拒绝 / 名字引用重名(data.candidates)/ id 或名字未找到(task 10-04-hermes-cron;与 CLI `myia cron` 同码) |
| 读态置位 | (仅复用 `invalid_params` + 透传 `store_corrupt`/`schema_version_newer`) | `store.state.mark` 的 keys 非非空数组/含非字符串或空串/超 2000、marker 不在 read/starred/later 枚举、value 非 bool;`store.state.mark_all` 的 marker/value/category 空串;`store.state.import` 的 states 非对象/键非字符串/值非对象/标记键非枚举布尔(task 10-04-read-state-server;参数形状全静态校验,无新业务 code) |
| 随包插件一键装 | `bundled_plugins_unavailable` / `bundled_plugin_not_found`(另复用 `invalid_params` id/force 形状;装卸门错误码 `PluginStoreError.code` 动态透传见透传族) | `plugins.bundled.install`:env `MYIA_BUNDLED_PLUGINS` 未设/目录不可达(dev 形态/旧包/未注入如实;`bundled_plugins_unavailable`)/ id 过正则门但随包目录内无此件(`bundled_plugin_not_found`,可用件见 list;task 10-05-bundled-plugins-install) |
| 随包品类平铺装 | `bundled_category_not_found` / `category_exists` / `category_invalid` / `io_error`(另复用 `bundled_plugins_unavailable`/`invalid_params`) | `plugins.bundled.category_install`:id 过 `CATEGORY_ID_RE` 但随包平铺 YAML 内无此件(`bundled_category_not_found`,可用件见 list 的 categories)/ 数据根已有同名文件未 force(`category_exists`——如实「已存在」不覆盖,与补种幂等补缺语义对齐)/ 随包 YAML 装不上(`category_invalid`,坏件拒零拷贝)/ tmp+rename 拷贝 IO 失败;task 10-05-bundled-plugins-batch2 R3 |

### 透传族(`exc.code` 动态透传,不在 entry.py 静态出现)

`store.items` / `secret.*` / CLI 包装透传底层模块 code(例:`store_corrupt` /
`invalid_secret_name` / `config_dir`,枚举见 entry.py 模块 docstring:19-21)——追源头去
`src/shishi/` 对应模块,entry.py 只加 `path`/`data` 不改 code。`push.test` 同款透传
push 层 `PushSendError.code`(`missing_target` / `env_var_missing` /
`credential_resolve_failed` 等,追源头去 `src/shishi/push/`;task 10-03-feed-ux G5)。
`plugins.bundled.install` 透传插件仓 `PluginStoreError.code`(installed.py 装卸门
唯一 fail-fast 面:already_installed / incompatible_version / manifest_invalid /
invalid_source / io_error;task 10-05-bundled-plugins-install,`data.errors` 带
manifest 校验明细);`plugins.bundled.uninstall` 同族透传 remove 侧
`PluginStoreError.code`(not_installed / io_error;批二 R2——卸载=安装根操作,
id 正则门与 install 同门,invalid_plugin_id 形态在协议层先拦为 invalid_params)。

## 变更纪律

1. 新增/改名方法:**只改 `_HANDLERS` 一处** + `tests/desktop/test_desktop_sidecar_protocol.py` 契约用例;
   本文注册表随同更新(行号注解允许漂移,方法名集合不许漂)。
2. 对账手法:发未知方法名,拿 `data.allowed` 与本文注册表比对;前端共享类型映射
   `SidecarProtocol`(types.ts)现盖 47 方法(核心 + image.config.* + v1.1.2 批八方法 +
   feed-ux 批三方法 + vision-v2/fe-small-batch/read-state-server 批 + cron-ui 批
   `cron.*` 九方法与 `yaml.list` 复用,10-04-cron-ui + gates 批两方法,10-05-plugin-
   market-batch 批二),`sources.write`/`yaml.*`(除 `yaml.list`)刻意未入共享映射——
   对账时按上表分组核对,勿以映射数当全量。
3. 封装面 ≠ 协议面:`ui-src/src/lib/api/client.ts` 的 `api` 门面盖核心 10 方法 +
   v1.1.2 桌面对齐批 8 方法(`runCancel`/`runsList`/`secretDelete`/`sourcesTest` +
   `feedbackMark`/`feedbackList`/`feedbackStats`/`storeTrend`,
   10-03-v112-desktop-parity)+ feed-ux 批 3 方法(`feedExport`/`schedulePreview`/
   `pushTest`,10-03-feed-ux;两批新方法全入共享门面,注册表新增行 ↔ 门面新增行
   同源对账,屏私名单不扩);
  `sources.write` 在 `screens/sources/api.ts`、`yaml.*` 在 `screens/yaml-editor/api.ts`、
  `image.config.*` 在 `screens/settings/vision-api.ts`、`channels.*`/`push.write`/
  `bridge.status` 在 `screens/messaging/api.ts` 屏私有封装(invoke 直连,不走共享门面)。
 `cron.*` 九方法 + `yaml.list` 已由 10-04-cron-ui 接线(定时任务屏):十方法全入
  共享门面(`cronList`/`cronCreate`/`cronEdit`/`cronPause`/`cronResume`/`cronRun`/
  `cronRemove`/`cronStatus`/`cronRuns`/`yamlList`)——`yaml.list` 属第二消费方复用,
  按同源对账入面,yaml.* 其余仍屏私有;消费方 = `screens/cron/`(list/status/runs
  + 动作四件 + estop 双向;事件 cron.completed/cron.skipped 已入 `SidecarEvent`
  联合与 logs 屏 eventToRow)。
 `gates.get`/`gates.save` 已由 10-05-plugin-market-batch 批二第 11 步接线(设置屏
  门槛件分区):两方法入共享门面(`gatesGet`/`gatesSave`),消费方 =
  `screens/settings/`(门槛件三卡:付费通道/自有实例/分析件 D8 占位)。
 `plugins.bundled.list`/`install` 已由 10-05-bundled-plugins-install 接线(设置屏
  「装机组件」分区):两方法走**屏私有封装面**(`screens/settings/
  bundled-plugins-api.ts`,invoke sidecar_request 直连+错误归一化,沿 pyenv-api.ts
  types+invoke 封装先例;不进共享门面——单屏单消费方,yaml.* 同款惯例),
  消费方 = `screens/settings/bundled-plugins-card.tsx`(逐包行+一键装/重装;
  SidecarProtocol 共享映射数不变,对账时勿按 47 计本族)。
  批二(10-05-bundled-plugins-batch2)同面扩三键:`uninstall`/`category_install`
  两方法与 list 新增 `categories` 键均走同一 bundled-plugins-api.ts 屏私有封装
  (消费方不变=bundled-plugins-card.tsx 增卸载钮+品类分区行;共享门面与
  SidecarProtocol 映射数仍不变,对账口径同上)。
 `store.state.*` 三方法的前端接线归 10-04-read-state-server 前端件(feed 屏
  能力门:`api.version().protocol >= 10` 走服务端态通路,否则原样走旧
  localStorage 通路——旧 sidecar + 新 UI 组合可用;接线落成后按上表 52-54 行对账)。
