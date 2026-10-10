"""MYIA 桌面 sidecar 入口:双模式。

模式一(直通,默认):: ``entry.py run <yaml> --json …`` 原样转发 :func:`myssia.cli.main`,
退出码 0/1/2/3 契约由 CLI 层保证(PyInstaller 打包路径与 v02 spike 完全兼容)。

模式二(RPC 服务):: ``entry.py serve`` 进入行分隔 JSON-RPC 子集(Tauri 壳的常驻
后端,stdin 收请求 / stdout 出应答与事件;stderr 只作调试旁路,不承载协议)。

== 协议(每行一份 JSON 文档,UTF-8,ensure_ascii=False) ==

请求(stdin):: ``{"id": 1, "method": "health", "params": {}}``
- ``id``:int 或字符串,应答原样回显;缺省 = 通知(只执行、不应答)。
- ``params`` 缺省按 ``{}``。

应答(stdout):: ``{"id": 1, "result": {...}}`` 或
``{"id": 1, "error": {"code": "...", "path": "$", "message": "...", "data": {...}}}``
- 错误结构化透传(对齐 spec python/error-handling):``code`` 错误类、``path``
  字段路径、``message`` 中文原因、``data`` 原始细节(CLI 报文整包入 data)。
- 协议级 code:``parse_error`` / ``invalid_request`` / ``invalid_params`` /
  ``method_not_found`` / ``internal_error``;业务级透传底层 code
  (``config`` + errors[] / ``plugins_dir`` / ``store_corrupt`` /
  ``invalid_secret_name`` / ``run_busy`` / ``run_not_found`` …)。

事件(stdout,无 id,以 ``type`` 字段区分)::

    {"type": "log",       "run_id": 3, "stream": "stderr", "line": "…", "ts": "…"}
    {"type": "progress",  "run_id": 3, "phase": "source_done", "source": "…", "items": "2", "ts": "…"}
    {"type": "completed", "run_id": 3, "exit_code": 0, "status": "success", …, "ts": "…"}
    {"type": "test.completed", "job_id": 1, "ok": true, "exit_code": 0, "result": {…}, "ts": "…"}
    {"type": "image.models.progress",  "job_id": 1, "repo": "…", "done_bytes": 1, "total_bytes": 2, "ts": "…"}
    {"type": "image.models.completed", "job_id": 1, "ok": true, "ts": "…"}
    {"type": "image.server.completed", "job_id": 1, "ok": true, "status": {…}, "ts": "…"}
    {"type": "alerts.fired", "rule_id": 3, "rule_name": "…", "item_id": 42, "dedup_key": "…",
     "title": "…", "action": "push", "action_status": "sent", "ts": "…"}
    {"type": "cron.skipped",   "job_id": "a1b2c3d4e5f6", "name": "早晚情报流",
     "reason": "run_busy", "active_run_id": 7, "ts": "…"}
    {"type": "cron.completed", "job_id": "a1b2c3d4e5f6", "name": "早晚情报流",
     "ok": true, "status": "ok", "delivery_error": null, "summary": {…运行摘要计数…},
     "ts": "…"}

== 方法集(覆盖现有 CLI 能力) ==

================= ============================== ============================
方法              CLI 等价                        结果要点
================= ============================== ============================
version           ``myssia --version``             name/version/protocol/app_version
health            ``myssia list --json``           源健康度 + summary 聚合
plugins.list      ``myssia plugin list --json``    已装插件清单 + findings
doctor            ``myssia doctor --json``         findings 全量(完成即 0)
run.start         ``myssia run <yaml>``            后台子进程,立即返回 run_id
run.status        (注册表 + DB runs 历史合流)     state/exit_code/status/record;
                                                 重启后接「上一程」历史行
                                                 (history 徽标,上限 50)
run.cancel        (进程组杀 run 子进程)           SIGTERM→5s 后 SIGKILL 兜底;
                                                 信号终局 status="cancelled"
runs.list         (SQLiteStore.list_runs 直读)   历史 run(新→旧;重启后可达)
runs.trend        (SQLiteStore.daily_run_outcomes) run 成功率趋势(UTC 逐日×status
                                                 计数,窗口 [1,90] 天)
logs.tail         (sidecar 内环形缓冲)            最近日志行(可按 run_id 过滤)
store.items       (SQLiteStore.list_items 直读)  情报流条目(新→旧;游标/搜索;
                                                 投影含 read/starred/later)
store.state.mark  (SQLiteStore.set_item_states)  按 dedup_key 批量置位读/星/稍后读
                                                 (同键多行同置;keys ≤2000 防线)
store.state.mark_all (SQLiteStore.set_all_item_states) 全库(可选 category)置位
                                                 (含未翻页条目;无 query)
store.state.import (SQLiteStore.import_item_states) localStorage 读态一次性搬迁
                                                 (服务端旗标幂等)
feedback.mark     (record_feedback 同门直调)      卡片 👍/👎 入库(channel=
                                                 desktop;CLI feedback list
                                                 可见同一条目)
feedback.list     (SQLiteStore.list_feedback)     反馈记录(新→旧;键同 CLI)
feedback.stats    (FeedbackTuner.stats + tuning)  窗口统计 + 生效调参 + 历史
store.trend       (SQLiteStore.daily_item_counts) 采集量趋势(UTC 逐日计数,
                                                 窗口 [1,90] 天)
feed.export       (list_items 同一查询面直写)     当前过滤视图导出 JSONL/CSV
                                                 (sidecar 直写,数据不经
                                                 webview;只写对话框选定的
                                                 单个文件)
feed.enrich       (LLMEnricher.enrich 同门)       单条情报卡 AI 摘要/精评
                                                 (item 引用同 feedback.mark;
                                                 品类 enrich 节端点;缓存复用
                                                 enrich_cache;未配置 =
                                                 enrich_not_configured)
schedule.preview  (build_cron_trigger 纯计算)     品类排程未来 count 次时刻
                                                 (Apify 式 Next runs 预览,
                                                 防 cron 写错)
secret.set        ``myssia secret set``            只入系统钥匙链,值零回显
secret.list       ``myssia secret list``           只有名字,值不可读
secret.delete     ``myssia secret delete``         误存凭据的 UI 清除口
sources.write     (品类 YAML 源启停写回)          disable 摘出/enable 移回
                                                 (文本手术,注释逐字节保真);
                                                 落盘前过 load_category 同门
sources.test      ``myssia test <yaml> --source``  试抓此源,异步 job;结果走
                                                 test.completed 事件(同步实现
                                                 会撞壳层 120s 硬超时,禁)
yaml.list         (plugins 目录扫描)              品类 YAML 清单(坏文件带
                                                 error 入列,可读可修)
yaml.read         (原文直读)                      UTF-8 原文(newline="" 逐
                                                 字节保真,≤1 MiB)
yaml.validate     (load_category 同门干跑)        findings 分级 error/warning,
                                                 零写入
yaml.template     (协议侧常量)                    最小合法品类模板文本
yaml.save         (校验→查重→.bak→原子写)         mtime 乐观锁;file 不存在 +
                                                 expected_mtime=null = 新建
yaml.delete       (.bak 留底→删主文件→连带暂存)   自建品类生命周期收尾
image.config.read  (vision.yaml 直读)              脱敏配置(keychain 引用不回明文)
image.config.save  (同门校验→原子写)               失败零写入(image_config_invalid)
image.models.list  (<home>/models 扫描)            已装模型清单(name/path/bytes/
                                                 active/incomplete 标;半成品
                                                 incomplete=true 可续传;空目录
                                                 =合法空表)
image.models.download (HF snapshot_download)       异步 job:提交即返 job_id,
                                                 结果走 image.models.progress/
                                                 completed 两事件(断点续传;
                                                 同名完整模型 model_exists 拒;
                                                 单飞 download_busy)
image.models.delete (active 拒删)                  {ok};正被 local.model 使用的
                                                 模型 model_active_refused
image.models.activate (vision.yaml 改写)           {ok};local.model 指向该模型
                                                 目录(同门校验原子写;半成品
                                                 model_incomplete 拒)
image.server.status (base_url/models 2s 探)        {running, base_url, model,
                                                 healthy}
image.server.ensure (nohup 自起 mlx_vlm.server)    应答立即返:已健康=status+
                                                 {started};否则快照超集+
                                                 {ensuring:true, job_id},自启+
                                                 健康等待 ≤120s 跑后台线程
                                                 (serve 循环不冻结),终态走
                                                 image.server.completed 事件;
                                                 并发第二单 ensure_busy
image.files.purge  (按 mtime 清 <home>/images)     {deleted, bytes_freed};
                                                 days≥1 整数;只删文件不动
                                                 目录(CLI 面能力,零 UI)
gates.get          (gates.yaml 脱敏读取)          {config, path};坏文件
                                                 fail-closed=全关+error 带回
                                                 (设置屏是修复入口,不炸)
gates.save         (同门校验→tmp+rename 原子写)    {ok, path};校验失败
                                                 gates_config_invalid 零写入
channels.list      (消息屏目录四视图)              目录(platforms)+别名(aliases)
                                                 +死信(dead)+推送规则(rules);
                                                 零平台=合法空态
channels.refresh   (单平台目录发现→合并)           调该平台 ``discover_directory``
                                                 →桶替换+落盘;失败结构化上抛,
                                                 旧目录不动(unknown_platform /
                                                 discover_not_supported /
                                                 channel_refresh_failed)
channels.alias     (别名 set/delete)               name 非空=set,null/空=delete;
                                                 写别名文件(原子)+落盘复核
push.write         (push[] 全量替换写回)           围栏→push 块文本手术(注释
                                                 保真)→反解析深等门→load_category
                                                 同门(含同平台约束)→.bak→原子
                                                 写;校验失败零写入
push.test          (通道 send(items, context))    合成单条测试条目真发指定通道
                                                 (凭据沿用 env:/keychain: 引用
                                                 链;stdout 通道卡片入应答
                                                 preview,协议流零污染)
alerts.list        (SQLiteStore.list_alert_rules)  告警规则全量(启用/停用同行;
                                                 fired_count/last_fired_at 派生)
alerts.save        (规则表全量替换)               建改启停一体:构造门整批过 →
                                                 diff 落库保 id;任一条无效 =
                                                 alert_rule_invalid 整批零写入
alerts.delete      (delete_alert_rule)             删定义行,fired 历史照留;
                                                 未知 id = alert_not_found
alerts.test        (compile_rule + evaluate 同门)  dry 求值不真发不落 fired:
                                                 {matched, muted, actions,
                                                 eval_error?, already_fired?}
cron.list          (CronJobs.list_jobs)           定时 job 清单(all=true 含
                                                 暂停/终态);薄封装 cron 包
cron.create        (CronJobs.create_job)          建定时 job(schedule 五形态;
                                                 Q6 品类早失败/Q5 绝对路径)
cron.edit          (CronJobs.update_job)          部分更新;schedule 变更重算
                                                 next_run_at
cron.pause         (pause_job/engage_estop)       暂停 job(reason 可选);
                                                 all=true 全局急停(Q4)
cron.resume        (resume_job/rearm_oneshot)     恢复/一次性重挂(at=ISO);
                                                 all=true 解除急停
cron.run           (CronJobs.trigger_job)         下次 tick 立即跑(manual;
                                                 复活 paused、计入 repeat)
cron.remove        (CronJobs.remove_job)          删记录;output 目录与账本
                                                 行保留(运行证据)
cron.status        (心跳标记族 + 到期扫描)         ticker 活性(心跳龄/最后
                                                 错误/下次到期/急停态)
cron.runs          (ExecutionLedger.list_executions) 执行账本尾查(新→旧,
                                                 含 run_summary 摘要)
================= ============================== ============================

- ``run.start`` params:``yaml``(必填)、``dry``(bool,缺省 false)、``db``、
  ``config``(全局 pools YAML)。同一时刻只允许一个 run(``run_busy`` 结构化拒绝);
  子进程 = 冻结包自启(直通模式)/ dev 下 ``python -m myssia.cli``,退出码
  0/1/2/3 由 CLI 原样带回,随 ``completed`` 事件透传(退出码语义保留)。
- ``run.cancel`` params:``run_id``(缺省 = 当前活跃 run);应答
  ``{run_id, cancelled, state}``;未知 id/无活跃 run = ``run_not_found``,
  已终态 = ``run_not_active``(data 带 state)。杀进程走 ``os.killpg``
  进程组(onefile bootloader+孙进程一锅端;run 子进程
  ``start_new_session=True`` 自成进程组)。
- ``runs.list`` params:``db``、``category``、``limit``(缺省 50,钳制 [1,200]);
  直读 runs 表(新→旧),sidecar 重启后历史仍在。
- ``runs.trend`` params(G6,10-04-desktop-b234):``days``(缺省 14,钳制 [1,90])、
  ``category?``、``db?`` → ``{days: [{date, total, statuses{…}}]}`` 旧→新,UTC
  逐日口径(statuses 开放词表原样分组,真实词表 4 态 running/success/partial/
  failed;零数日补齐归前端 fillDailyOutcomes)。
- ``store.items`` params:``db``、``category``、``since``(ISO 时间)、``limit``、
  ``query``(title/content/source 三列 LIKE NOCASE)、``before``(ISO 时间,
  first_seen 严格小于)、``before_id``(与 before 组成 ``(first_seen, id)``
  复合游标;同刻批量超单页 limit 也能翻页取尽)。投影自 v10 起含
  ``read``/``starred``/``later`` 三布尔键(feed.export JSONL 同源连带)。
- ``store.state.*`` 三方法(G9,10-04-read-state-server):``mark {keys:
  [dedup_key, …], marker: read|starred|later, value, db?}`` → ``{updated}``
  (SQLite UPDATE rowcount 口径,匹配行计数如实回传;同 dedup_key 多行
  同置,幂等;keys 上限 2000 = 误用防线,整库语义走 mark_all);
  ``mark_all {marker, value, category?, db?}`` → ``{updated}``(category
  精确等值与 list_items 同参,无 query——决议 Q3.2 钉死);``import
  {states: {<key>: {read?/starred?/later?}}, db?}`` → ``{imported,
  skipped}``(key 三分:dedup_key 直配 / ``id:<n>`` 解析 / 其余如实计
  skipped;store_meta 旗标 ``feed_state_imported_at`` 幂等,已设 = no-op
  应答不触库——服务端旗标是唯一真相)。
- ``secret.delete`` params:``name``;secrets 层 code 透传(``secret_not_found``
  第二次删除、``invalid_secret_name`` 等)。
- ``feedback.*`` 三方法(B2,10-03-v112-desktop-parity):``feedback.mark
  {item, verdict, db?}``(``item`` = items.id 或 dedup_key/URL;条目不存在 =
  ``item_not_found``)→ ``{feedback_id, item_id, dedup_key, verdict,
  channel:"desktop"}``;``feedback.list {verdict?, channel?, limit?=50, db?}``
  → ``{count, items[]}``(键同 CLI `_feedback_row_dict`);
  ``feedback.stats {window_days?=14, top?=5, db?}`` → ``{window_days, stats,
  active_tuning, tuning_history}``(键同 CLI stats 载荷)。
- ``store.trend`` params(B4,同批):``days``(缺省 14,钳制 [1,90])、
  ``category?``、``db?`` → ``{days: [{date, count}]}`` 旧→新,UTC 逐日口径
  (零数日补齐归前端 fillDailyCounts)。
- ``sources.test`` params:``file``(必填,围栏)、``source``(缺省 = 全部源)、
  ``timeout``(≤120)、``config``;应答 ``{job_id, state:"running", source?}``,
  结果走事件 ``test.completed {job_id, ok, exit_code, result?|error?, ts}``;
  单飞 = ``test_busy``,装不上品类 = ``source_file_unreadable``。
- ``feed.export`` params(task 10-03-feed-ux,契约钉死于任务档 design.md §1):
  ``format``(``jsonl``/``csv``)、``path``(绝对路径,前端 ``dialog.save()``
  选定;空/相对/父目录不存在 = ``export_path_invalid``)、``category``/``query``
  (与 ``store.items`` 同一查询面);应答 ``{path, count, bytes}``,写盘 IO 失败 =
  ``export_write_failed``。只写该一个文件,不建目录不删除任何东西。
- ``feed.enrich`` params(G8,10-03-fe-small-batch):``item``(items.id 或
  dedup_key/URL,解析口径同 ``feedback.mark``)、``db?``;应答
  ``{item_id, model, scores, score, cached}`` —— 单条现跑
  :class:`~myssia.enrich.LLMEnricher`(端点 = 条目所属品类 YAML ``enrich:``
  节,``base_url``/``api_key`` 走 ``env:``/``keychain:`` 引用解析;分数原路
  回填 items 表 + enrich_cache 缓存语义复用,缓存命中零 token;async
  :meth:`~myssia.enrich.LLMEnricher.enrich` 在 handler 内 ``asyncio.run``
  同步应答,整段挂 ``EnrichSettings.timeout_seconds`` 超时帽)。品类未启用
  enrich / 端点引用缺失 / 品类 YAML 不在 plugins 目录 =
  ``enrich_not_configured``(graceful,data.reason 三分);超时 =
  ``enrich_timeout``;条目未获分(预算耗尽/批次失败)= ``enrich_failed``;
  ``EnrichConfigError`` 的 code 原文透传(``credential_unresolved`` /
  ``invalid_base_url`` 等)。
- ``schedule.preview`` params:``file``(围栏同 yaml.*/sources.test)、``count``
  (缺省 5,钳制 [1,20]);应答 ``{file, schedule, timezone, runs[]}``,品类装不上 =
  ``source_file_unreadable``,纯计算零副作用。
- ``push.test`` params:``channel``(∈ myssia.push.CHANNELS)、``target?``
  (凭据引用)、``template?``;应答 ``{ok: true, channel, preview?}``(preview 仅
  stdout 通道);失败沿用通道 PushSendError code 原文直传。
- ``run.status`` / ``logs.tail`` params:``run_id``(可省)/ ``lines``(tail 上限)。
- ``health`` params:``plugins_dir``、``db``;``plugins.list`` params:``dir``;
  ``doctor`` params:``yamls[]``、``plugins_dir``、``db``、``config``、``probe_timeout``。
- ``sources.write`` params:``file``(必填)、``enable[]`` / ``disable[]``(至少
  其一);应答 ``enabled``/``disabled`` = 写回后的名字全集(往返一致由 UI 侧
  doctor 复核,存储形态见 :func:`_m_sources_write`)。
- ``yaml.*`` 六方法(task 10-03-yaml-editor,契约钉死于任务档 design.md §1,
  Python/TS 两侧注释互指):``yaml.list`` 零参数(目录由 serve 上下文定);
  ``yaml.read {file}``;``yaml.validate {content, file?}``;``yaml.template``
  零参数;``yaml.save {file, content, expected_mtime}``;
  ``yaml.delete {file}``。路径围栏(:func:`_fence_yaml_path`):后缀
  ``.yaml/.yml`` + resolve 后必须位于 plugins 目录内(``os.path.commonpath``,
  消解符号链接与 ``..`` 穿越)+ 新建 stem 过 :data:`CATEGORY_ID_RE` ——
  sidecar 是 UI 直连读写通道,不设围栏 = 桌面端任意文件读写原语。
- ``image.config.*`` 两方法(10-03-vision-pipeline 拆四留二:看图交互屏整拆,
  ``image.import/ocr/analyze/status`` 四方法与 ``image.progress/completed`` 两
  事件已删;配置入口保留——设置屏 VisionForm 依赖;能力实现在 ``myssia.vision``
  包,与 vision.yaml 机制不动):``image.config.read`` / ``image.config.save``
  读写 ``<home>/vision.yaml``(MYIA_HOME 第一个全局配置文件;云端 api_key 只收
  ``keychain:`` 引用,同门校验失败零写入)。业务错误码:``image_config_invalid``。
- ``image.models.*`` / ``image.server.*`` 六方法 + ``image.files.purge``
  (10-03-vision-v2,契约与前端 TS 侧同形状):``image.models.list`` 零参 →
  ``{models:[{name,path,bytes,active,incomplete}]}``(半成品 = 缺
  config.json 或 *.safetensors 的目录,incomplete=true);``image.models.
  download {repo, name?}``(repo 必须 ``mlx-community/<name>``,MLX 格式权重
  直下免 convert)→ ``{job_id}`` + ``image.models.progress {job_id, repo,
  done_bytes, total_bytes?}`` / ``image.models.completed {job_id, ok,
  error?}`` 两事件(磁盘预检不足 = ``disk_insufficient`` 完成事件;断点
  续传 = 半成品同名放行,完整同名 ``model_exists`` 拒;单飞
  ``download_busy``);``image.models.delete {name}`` /
  ``image.models.activate {name}`` → ``{ok}``(active 模型拒删
  ``model_active_refused``;半成品拒激活 ``model_incomplete``;激活 =
  vision.yaml ``local.model`` 原子改写);``image.server.status`` 零参 →
  ``{running, base_url, model, healthy}``;``image.server.ensure`` 零参 →
  应答立即返(已健康 = status+``{started:false}``;否则快照超集+
  ``{ensuring:true, job_id}``,自起 ``uvx --from mlx-vlm mlx_vlm.server`` +
  健康等待 ≤120s 跑**后台线程**——serve 循环单线程,同步等健康窗会把
  桌面全协议冻成队头阻塞),终态走 ``image.server.completed {job_id, ok,
  status?, error?, ts}`` 事件(ok 时 status = status+``{started}``;
  并发第二单 ``ensure_busy``;错误族 ``no_local_model`` /
  ``model_dir_missing`` / ``spawn_failed`` / ``server_died`` /
  ``server_start_failed`` 以事件 error 收口,子进程输出泵入统一日志
  ``<home>/logs/myssia-*.jsonl`` 的 proc=vision 行,决议③);``image.files.purge
  {days}`` → ``{deleted, bytes_freed}``。模型与 server 能力实现在
  ``myssia.vision.models`` / ``myssia.vision.server``(重依赖惰性,
  huggingface-hub 在 extras ``myssia[vision]``)。
- ``alerts.*`` 四方法 + ``alerts.fired`` 事件(10-04-alert-rules,契约钉死于
  任务档 design.md §4,引擎 = ``myssia.alerts``、挂点 = ``Pipeline._alert_pass``):
  ``alerts.list {}`` → ``{rules:[AlertRuleView]}``(全字段 + ``fired_count``/
  ``last_fired_at`` 自 alert_fired 派生);``alerts.save {rules:[AlertRuleInput]}``
  → ``{ok, rules}``(**全量替换**承建/改/启停:构造门整批过,任一条无效 =
  ``alert_rule_invalid``(data 三键 index/field/reason)整批零写入;带 id 更新
  保 id、库中多余 id 删除,空数组 = 清空);``alerts.delete {id}`` → ``{ok}``
  (未知 id = ``alert_not_found``;fired 历史照留);``alerts.test
  {rule?|rule_id?, item?|item_id?}`` → ``{matched, muted, actions,
  eval_error?, already_fired?}``(**dry 求值不真发不落 fired**;item 合成
  dict / item_id 库内条目 / 缺省最近一条,空库 = ``alert_test_no_item``;
  muted = effective mute 压制(品类 watchlist + 反馈 0.0 词);actions 展开
  push 通道解析结果与降级原因 / tag 标签;真发测试借既有 ``push.test``)。
  事件 ``alerts.fired {rule_id, rule_name, item_id, dedup_key, title, action,
  action_status, ts}``:run 终态收口处以 ``list_fired(since=run.started_at)``
  查库回放(completed 之前逐条发出;dry run 零落库零回放)。

- ``cron.*`` 九方法 + ``cron.skipped``/``cron.completed`` 两事件
  (10-04-hermes-cron B3,能力 = ``myssia.cron`` 包,与 CLI ``myssia cron`` 同一
  API 层):``cron.list {all?, db?}`` → ``{count, jobs}``;``cron.create
  {schedule, category, name?, deliver?, failure_deliver?, repeat?, timezone?,
  config?, run_timeout?, dry_run?, paused?, paused_reason?, db?}``(Q6 完整
  ``load_category_file`` 早失败 → ``cron_category_invalid``;schedule 解析/
  once 超窗/repeat 等 ``ValueError`` → ``cron_create_failed``);``cron.edit
  {job, …同 create 可选字段}``(空更新集 = ``cron_edit_no_changes``);
  ``cron.pause {job, reason?}`` / ``{all:true}`` 全局急停;``cron.resume
  {job, at?}`` / ``{all:true}`` 解除急停;``cron.run {job}``;``cron.remove
  {job}``;``cron.status {}`` → 心跳龄/最后错误/下次到期/急停态;``cron.runs
  {job?, limit?=20 钳制 [1,500]}`` → 执行账本(含 ``run_summary`` 摘要)。
  ``job`` 引用 = id 或名字(重名 → ``cron_ambiguous_job`` 带 candidates;
  未找到 → ``cron_job_not_found``)。数据根 = ``db`` 父目录(缺省 = serve
  上下文);serve 就绪后内置 cron ticker(daemon 线程,**home 模式才起**,
  dev 回退用 ``myssia cron serve``;监督线程 ``restart_if_dead`` 照抄),与
  CLI serve 并存靠 tick 文件锁 + fire claim 互斥(多宿主,照抄 Hermes)。
  事件 ``cron.skipped {job_id, name, reason:"run_busy", active_run_id, ts}``:
  cron fire 撞桌面 run 单飞锁 = 跳过本 fire(grill Q2;advance 已消耗,不
  排队不回滚;``last_status="skipped_busy"`` 由 tick 层落库,成功语义不动
  streak;用户手点优先);事件 ``cron.completed {job_id, name, ok, status,
  delivery_error, summary, ts}``:fire 完成(摘要 = runner 随执行行落账的
  ``run_summary_json``,零二次解析;账本写失败时 summary=null 如实)。

- telegram serve 常驻宿主(10-06-telegram-telethon 桌面接线批,零新方法
  纯生命周期件):serve 就绪后持 ``TelegramServeHost`` 于 daemon 线程
  (asyncio.run;**home 模式才起**,dev/测试回退 ``myssia telegram serve``),
  装配与 CLI 同门(品类 = ``<plugins>/telegram-groups.yaml`` → 绑定 →
  keychain token → 入库/推送 sink → offsets/events 落数据根 ``telegram/``);
  凭据缺失 = graceful 不启动仅留痕(主人四步配好重启即活)。EOF 即停
  (stop Event + 有界 join,长轮询挂起窗内 daemon 兜底)。与 CLI serve 的
  双宿主互斥靠 Bot API 同 token 409(telegram/serve.py 设计 D1);致命
  错误(401/409)线程自退留痕、不自动重排(D4 重启由人决定)。

铁律:凭据只进系统钥匙链(``secret.set`` 薄包装 myssia.secrets,值不落日志/协议流);
桌面零 Docker;任何插件装不上不拦核心(doctor/list 只产 findings)。

serve 上下文路径解析(v1.1.1 统一,优先级):显式 params > ``MYIA_HOME`` env
(Tauri 壳 spawn 时注入)> 冻结 .app bundle 探测(平台数据根
``~/Library/Application Support/MYIA`` / ``%APPDATA%\\MYIA`` / ``~/.myia``)>
dev 回退 cwd(仓库内运行行为不变)。home 模式下 db/plugins 缺省
``<home>/myssia.db``、``<home>/plugins``;serve 启动时品类补种 —— 随包
Resources 官方品类 YAML **缺哪件补哪件、绝不覆盖已存在文件**(每次启动
幂等;标志 ``.seeded`` = 「已做过一次补种」的记录,不再是复种抑制器);
health 应答附 ``first_run`` 供 UI 空态引导。

== 退出码 ==

- serve 模式:stdin EOF(壳退出/管道关闭)= 干净退出 0;serve 循环自身致命
  异常 = 1;run 子进程的原样退出码只在 ``completed`` 事件内透传,不改进程码。
- 直通模式:= CLI 契约 0/1/2/3 原样。
"""

from __future__ import annotations

import asyncio
import contextlib
import inspect
import io
import json
import os
import re
import shutil
import signal
import sqlite3
import subprocess
import sys
import threading
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable, Mapping, NamedTuple

import myssia
import yaml
from myssia import log as myssia_log
from myssia import push as myssia_push
from myssia.alerts import AlertConfigError, CompiledAlertRule, alert_view, compile_rule
from myssia.cli import DEFAULT_DB_PATH, DEFAULT_PLUGINS_DIR, main as cli_main
from myssia.classify.custom import RuleEvalError, evaluate_expression
from myssia.cron.jobs import AmbiguousJobReference, CronJobs
from myssia.cron.runner import CronRunner
from myssia.cron.ticker import (
    DEFAULT_TICK_INTERVAL_SECONDS,
    SupervisedTickerThread,
    run_ticker_loop,
)
from myssia.enrich import EnrichConfigError, EnrichSettings, LLMEnricher
from myssia.enrich.scoring import mute_hit
from myssia.engines.firecrawl import ENV_FIRECRAWL_API_KEY, ENV_FIRECRAWL_URL
from myssia.feedback import (
    FeedbackTuner,
    TuningPolicy,
    load_active_tuning,
    record_feedback,
    resolve_item_ref,
)
from myssia.pipeline import Item, make_cron_heartbeat_scan
from myssia.plugins.installed import (
    INSTALL_ROOT_ENV,
    InstalledPluginStore,
    PluginStoreError,
    default_install_root,
)
from myssia.plugins.manifest import load_manifest_file
from myssia.plugins.remote import (
    LOCK_FILENAME,
    PluginRemoteError,
    install_remote,
    load_plugins_lock,
)
from myssia.plugins.versioning import VersionRange, VersionSpecError
from myssia.push import ChannelDirectory, DeliveryLedger, DirectoryDiscoverUnsupported, PushSendError
from myssia.push.weixin import probe_bridge
from myssia.schema import (
    CATEGORY_ID_RE,
    CHANNEL_PLATFORMS,
    CategoryConfig,
    LoadError,
    # 私有符号受控复用(与 cli.py/manifest.py 复用 _SECRET_REF_RE 同一先例):
    # 重复键检测与凭据引用语法只此一处定义,防两处漂移。
    _PLUGIN_ID_RE,
    _SECRET_REF_RE,
    _UniqueKeyLoader,
    load_category,
    load_category_file,
)
from myssia.gates import (
    GATES_FILE_NAME,
    GatesConfig,
    GatesLoadError,
    load_gates_fail_closed,
    save_gates_config,
)
from myssia.secrets import (
    SecretError,
    delete_secret,
    get_secret,
    list_secrets,
    set_secret,
    validate_secret_name,
)
from myssia.store import FEEDBACK_CHANNEL_DESKTOP, SQLiteStore, StoreSchemaError
from myssia.store.models import ALERT_RULE_KIND_ITEM, AlertRule
from myssia.vision import (
    VISION_FILE_NAME,
    VisionConfig,
    VisionConfigError,
    load_vision_config,
    save_vision_config,
)
from myssia.vision.models import (
    VisionModelError,
    activate_model as vision_activate_model,
    delete_model as vision_delete_model,
    download_model as vision_download_model,
    list_models as vision_list_models,
)
from myssia.vision.server import (
    VisionServerError,
    ensure_vision_server,
    vision_server_status,
)

#: v2 = 消息族(channels.*/push.write)入表;yaml.*/image.* 并线期未及 bump,
#: 本次统一收口(v1 停在 10 方法时代)。
#: v3 = feed-ux 批(feed.export / push.test / schedule.preview;store.items 的
#: query/before/before_id 已随 v112 桌面对齐批在 v2 期内落地,不重复计)。
#: v4 = weixin-bridge 批(bridge.status 微信桥接探测,10-03-messaging-weixin-bridge)。
#: v5 = vision-v2 批(image.models.* 四方法 + image.server.* 两方法,及
#: store.items 投影补 image_caption/image_files/image_ocr_lines 三键,
#: 10-03-vision-v2;契约与前端 TS 侧同形状冻结)。
#: v6 = fe-small-batch G8(feed.enrich 单条情报卡 AI 摘要/精评:骑 enrich
#: 管线同门 LLMEnricher,品类 enrich 节端点 + enrich_cache 缓存语义复用,
#: 10-03-fe-small-batch)。
#: v7 = alert-rules 批(alerts.list/save/delete/test 四方法 + alerts.fired
#: 回放事件;规则引擎 myssia.alerts,10-04-alert-rules Stage D)。
#: v8 = desktop-b234 批(runs.trend:run 成功率趋势逐日×status 聚合,G6;
#: 10-04-desktop-b234)。
#: v9 = hermes-cron 批(cron.* 九方法 + cron.skipped/cron.completed 两事件
#: + serve 内置 cron ticker,10-04-hermes-cron B3)。
#: v10 = read-state-server 批(store.state.mark/mark_all/import 三方法 +
#: store.items 投影补 read/starred/later 三键;G9,10-04-read-state-server;
#: 开工实读 v9 后 +1——hermes-cron 已先合入,竞速条款顺延本批 v10)。
#: v11 = browser-module 批(browser.open/list/focus/close 四方法 + 移除
#: telegram.web.login(单入口铁律:登录改走浏览器模块);10-08-browser-module)。
#: v12 = tg-channel-card v2 批(store.items / store.state.mark_all /
#: feed.export 三方法增可选 source_kind(web/im)源大类过滤,卡片墙与
#: 第二层作用域查询;10-08-tg-channel-card)。
#: v13 = feed 计数口径根治批(store.items 增可选 with_total → 应答补
#: ``total`` = 同 WHERE 不分页全量计数,UI「已加载 N · 共 T 条」词面的
#: 数据源,能力门 COUNT_PROTOCOL = 13;10-09-tg-category-entry F2)。
#: v14 = feed v8 三级界面批(store.source_stats 分源聚合:每源
#: total/today/unread/latest_first_seen/latest_title 一答直出,1 级类型卡
#: 统计与 2 级行计数覆写的全库真值源,能力门 STATS_PROTOCOL = 14;
#: 10-09-tg-category-entry v8)。
PROTOCOL_VERSION = 14
#: 单次 run 的日志事件与环形上限一致;超限仅丢最旧行。
STATUS_BY_EXIT = {0: "success", 1: "config_error", 2: "failed", 3: "partial"}

#: 应用数据根环境变量名(Tauri 壳 spawn sidecar 时注入,优先级见 _serve_context)。
MYIA_HOME_ENV = "MYIA_HOME"
#: 品类补种标志文件名(数据根下;语义 = 「已做过一次补种」的记录 —— 首次
#: 补种时刻定格,不随幂等补缺刷新;补种本身每次启动照跑,见 _seed_first_run)。
SEED_MARKER = ".seeded"
#: 随包插件组件包目录锚点 env 名(壳层 spawn 时注入 Resources/plugins;
#: dev 构建不注入 = 合法空表,plugins.bundled.* 消费,10-05-bundled-plugins-install)。
BUNDLED_PLUGINS_ENV = "MYIA_BUNDLED_PLUGINS"


# ---------------------------------------------------------------------------
# 应用数据根与 serve 上下文(v1.1.1 桌面数据通路统一)
# ---------------------------------------------------------------------------


def myssia_home() -> Path:
    """平台应用数据根:darwin ``~/Library/Application Support/MYIA`` /
    win32 ``%APPDATA%\\MYIA`` / 其余 ``~/.myia``(design.md D1)。"""
    if sys.platform == "darwin":
        return Path.home() / "Library" / "Application Support" / "MYIA"
    if sys.platform == "win32":
        base = os.environ.get("APPDATA")
        root = Path(base) if base else Path.home() / "AppData" / "Roaming"
        return root / "MYIA"
    return Path.home() / ".myia"


def _inside_app_bundle() -> bool:
    """冻结二进制是否位于 .app 内(桌面发行形态;dev/CLI 直跑为 False)。"""
    if not getattr(sys, "frozen", False):
        return False
    return any(parent.suffix == ".app" for parent in Path(sys.executable).resolve().parents)


def _bundle_plugins_dir() -> Path | None:
    """随包官方插件目录(Tauri resources;dev 或无资源时 None)。

    候选按平台资源布局:macOS .app 的 ``Contents/Resources/plugins``、
    Windows/Linux 资源保持相对结构落在 exe 旁(``plugins/``);托管 Python
    形态(10-05-desktop-managed-py-env:壳 spawn ``python -m
    myssia_desktop_entry``,真解释器非冻结,``sys.frozen`` 恒空)按本文件
    布局定位 —— 资源树本件在 ``Resources/myssia-src/`` 下,父级即
    ``Resources``,随包 ``plugins`` 在其旁(与壳侧 pyenv.rs
    ``RESOURCE_SRC_DIR`` 同名锚点)。开发树本件在 ``desktop/`` 下,目录名
    不命中,dev 形态行为零变化(仍 None)。
    """
    candidates: list[Path] = []
    # 托管 Python 形态:exe 相对候选恒不可达(解释器在 <数据根>/python/,
    # 不在 .app 内),资源树布局是唯一可靠锚点。
    src_root = Path(__file__).resolve().parent
    if src_root.name == "myssia-src":
        candidates.append(src_root.parent / "plugins")
    if getattr(sys, "frozen", False):
        exe = Path(sys.executable).resolve()
        candidates += [
            exe.parent.parent / "Resources" / "plugins",
            exe.parent / "plugins",
            exe.parent / "resources" / "plugins",
        ]
    for candidate in candidates:
        if candidate.is_dir() and any(candidate.glob("*.yaml")):
            return candidate
    return None


def _has_category_yamls(root: Path) -> bool:
    """目录内是否已有品类 YAML(平铺 ``*.yaml``/``*.yml``,非递归)。"""
    return root.is_dir() and (any(root.glob("*.yaml")) or any(root.glob("*.yml")))


class ServeContext(NamedTuple):
    """serve 请求的路径上下文:显式 params 永远赢,这里只供缺省。

    ``home=None`` 即 dev 回退(cwd 相对常量,仓库内行为与 v1.1 逐字节一致);
    home 模式下 db/plugins 默认 ``<home>/myssia.db``、``<home>/plugins``,市场
    安装根尊重既有 ``MYIA_PLUGIN_DIR`` env,否则同为 ``<home>/plugins``
    (品类 YAML 平铺与市场插件子目录互不干扰:health 扫描非递归)。
    NamedTuple 而非 dataclass:本模块经 importlib 直载(测试),dataclass
    的注解解析依赖 sys.modules 注册,此处没有。
    """

    home: Path | None
    db: str
    plugins_dir: str
    install_root: str

    def first_run(self) -> bool:
        """首跑判定:home 模式且 plugins 目录内零品类 YAML(种子失败/被删光)。"""
        return self.home is not None and not _has_category_yamls(Path(self.plugins_dir))


def _serve_context() -> ServeContext:
    """解析当前 serve 上下文(每请求调用,极廉价;env 可被测试逐例注入)。

    优先级:**显式 params(各方法自行合并)> ``MYIA_HOME`` env > .app bundle
    探测 > dev 回退 cwd**。
    """
    env_home = os.environ.get(MYIA_HOME_ENV)
    if env_home:
        home = Path(env_home).expanduser()
    elif _inside_app_bundle():
        home = myssia_home()
    else:
        home = None
    if home is None:
        return ServeContext(
            home=None,
            db=DEFAULT_DB_PATH,
            plugins_dir=DEFAULT_PLUGINS_DIR,
            install_root=str(default_install_root()),
        )
    try:
        home.mkdir(parents=True, exist_ok=True)
        # plugins 目录一并建:全新数据根上 health/doctor 要的是空态 OK,
        # 不是 NotADirectoryError(prd 探查矩阵的「无创建逻辑」根因)
        (home / "plugins").mkdir(parents=True, exist_ok=True)
    except OSError as exc:
        raise ProtocolError(
            "myssia_home_unwritable", f"应用数据根不可创建: {home} ({exc})", path=f"env.{MYIA_HOME_ENV}"
        ) from exc
    install_root = os.environ.get(INSTALL_ROOT_ENV) or str(home / "plugins")
    return ServeContext(
        home=home,
        db=str(home / "myssia.db"),
        plugins_dir=str(home / "plugins"),
        install_root=str(Path(install_root).expanduser()),
    )


def _seed_first_run(ctx: ServeContext) -> bool:
    """品类补种:随包官方 YAML **缺哪件补哪件,绝不覆盖已存在文件**。

    AC5 补种语义(10-05-plugin-market-batch):每次启动幂等补缺 —— 官方
    新品类随升级自动出现(旧「全有或全无」退役);用户已有同名文件
    (手改/自建/旧版品类)逐字节原样保留。``<home>/.seeded`` 标志不再是
    复种抑制器,只记录首次补种时刻(存在即不重写);零缺件启动零写入。
    拷贝非原子可接受 —— 中途失败最坏少补几件,下次启动继续补缺。
    仅 home 模式调用;dev 模式零动作。
    """
    assert ctx.home is not None
    bundle = _bundle_plugins_dir()
    if bundle is None:
        return False
    plugins_dir = Path(ctx.plugins_dir)
    plugins_dir.mkdir(parents=True, exist_ok=True)
    copied: list[str] = []
    for pattern in ("*.yaml", "*.yml"):
        for source in sorted(bundle.glob(pattern)):
            target = plugins_dir / source.name
            if target.exists():
                continue  # 绝不覆盖已存在文件
            shutil.copy2(source, target)
            copied.append(source.name)
    if copied:
        marker = ctx.home / SEED_MARKER
        if not marker.exists():
            marker.write_text(_now_iso() + "\n", encoding="utf-8")
        myssia_log.stream_line(
            None, "stderr", f"sidecar: 品类补种 {len(copied)} 件 -> {plugins_dir}"
        )
    return bool(copied)


def _startup_seed() -> None:
    """serve 启动时的一次性种子入口;失败只留痕,绝不拦服务起来。"""
    try:
        ctx = _serve_context()
        if ctx.home is not None:
            _seed_first_run(ctx)
    except Exception as exc:  # noqa: BLE001 — 种子是增强,不是依赖
        print(f"sidecar: 首跑种子失败(忽略): {exc}", file=sys.stderr)


class ProtocolError(Exception):
    """协议层结构化错误 → 应答行 ``error`` 对象(code/path/message/data)。"""

    def __init__(self, code: str, message: str, *, path: str = "$", data: Any = None) -> None:
        super().__init__(message)
        self.code = code
        self.message = message
        self.path = path
        self.data = data


# ---------------------------------------------------------------------------
# 输出与统一日志(serve 线程 + run 工作线程共用;单写锁串行化)
# ---------------------------------------------------------------------------

_OUT: io.TextIOBase | None = None
_WRITE_LOCK = threading.Lock()


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="milliseconds")


def _write_line(payload: dict[str, Any]) -> None:
    """协议流单行写入(线程安全;_OUT 是 serve 启动时捕获的真实 stdout)。"""
    assert _OUT is not None
    with _WRITE_LOCK:
        _OUT.write(json.dumps(payload, ensure_ascii=False) + "\n")
        _OUT.flush()


def _respond(rid: Any, result: Any) -> None:
    _write_line({"id": rid, "result": result})


def _error(rid: Any, code: str, message: str, *, path: str = "$", data: Any = None) -> None:
    error: dict[str, Any] = {"code": code, "path": path, "message": message}
    if data is not None:
        error["data"] = data
    _write_line({"id": rid, "error": error})


def _configure_serve_logging(*, backfill: bool = False) -> None:
    """serve 形态统一日志(10-07-unified-logging 批1;design §2 sidecar 行)。

    ``myssia.log.configure(mode="serve", ring=True, proc="sidecar")``:ring =
    logs.tail 数据面,文件 = ``<home>/logs/myssia-*.jsonl``(home 缺省 dev
    形态 data_root=None,仅 ring+stderr,与旧行为零差);stderr 门 WARNING
    (子进程行 INFO 不重复上进程 stderr)。``backfill=True`` 仅 serve 启动
    用一次(会话冷启动:先清环形再盘尾回填,design §5——serve 可重入,
    不清会把上一会话已入环形的行再 seed 一遍);内嵌 CLI 窗口后的恢复
    不带 backfill(环形已活,重复 seed 会翻倍)。home 解析失败(不可建)
    不拦服务:降级 data_root=None 照常起(与 _startup_seed 同哲学)。
    """
    try:
        home = _serve_context().home
    except ProtocolError:
        home = None
    myssia_log.configure(mode="serve", data_root=home, ring=True, proc="sidecar")
    if backfill and home is not None:
        # 会话冷启动(home 形态):先清环形再盘尾回填(历史由盘接管,重入
        # 不重复 seed);dev 形态无盘可回填,环形保留 = 旧行为零差。
        myssia_log.reset_ring()
        myssia_log.backfill(home)


# ---------------------------------------------------------------------------
# in-process CLI 复用(health / plugins.list / doctor:stdout 单份 JSON 契约)
# ---------------------------------------------------------------------------


def _cli_json(argv: list[str]) -> tuple[int, dict[str, Any] | None]:
    """跑一次 CLI 子命令,捕获其 ``--json`` 单份文档与退出码。

    统一日志改造后(10-07-unified-logging 批1,design §3):cli_main 里
    ``_configure_logging`` 转调幂等 ``myssia.log.configure``——CLI 的
    logging 行在调用期间已由 ring handler 直入缓冲(force 互踩从根上
    消失,R4),被捕获 err 里只剩**裸 print**。窗口纪律:
    ``suspend_stderr`` 摘 stderr handler(cli_main 内的重配也不复挂,
    双份防线贯穿窗口)→ logging 行只走 ring+盘;窗口结束 ``resume_stderr``
    复挂通路 + 恢复 serve 形态配置(mode/proc/盘/ring 全回正,把 CLI
    残留的 human 级 stderr 门收回 WARNING);err 里的裸 print 行沿旧路
    ``stream_line`` 入流保「CLI 诊断可见」语义(run_id=null,stderr)。
    仅在 serve 循环线程调用;run 工作线程不经此路(无 stdout 重定向竞争)。
    """
    out, err = io.StringIO(), io.StringIO()
    try:
        myssia_log.suspend_stderr()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            code = cli_main(argv)
    except SystemExit as exc:  # 防御:--help/--version 类参数不可达,兜底不穿协议流
        raise ProtocolError("internal_error", f"CLI 异常退出: {exc.code}") from exc
    finally:
        myssia_log.resume_stderr()  # 窗口收口:复挂 stderr 通路(suspended 复位)
        _configure_serve_logging()  # serve 形态全恢复(mode/proc/盘/ring 重钉)
    for line in err.getvalue().splitlines():
        if line.strip():
            myssia_log.stream_line(None, "stderr", line)
    return code, _last_json(out.getvalue())


def _last_json(text: str) -> dict[str, Any] | None:
    """取 stdout 末份可解析 JSON(CLI --json 契约:恰好一份)。"""
    for line in reversed(text.splitlines()):
        line = line.strip()
        if not line:
            continue
        try:
            parsed = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(parsed, dict):
            return parsed
    return None


def _cli_error(code: int, payload: dict[str, Any] | None) -> ProtocolError:
    """CLI ``--json`` 错误报文 → 协议错误对象(code/path/message 透传)。"""
    if payload and "error" in payload:
        if payload["error"] == "config" and payload.get("errors"):
            first = payload["errors"][0]
            return ProtocolError(
                "config", str(first.get("message", "")), path=str(first.get("path", "$")), data=payload
            )
        return ProtocolError(str(payload["error"]), str(payload.get("message", "")), data=payload)
    return ProtocolError("cli_error", f"CLI 退出码 {code} 且无可解析 JSON 输出", data={"exit_code": code})


# ---------------------------------------------------------------------------
# 方法:version / health / plugins.list / doctor
# ---------------------------------------------------------------------------


def _m_version(params: dict[str, Any]) -> dict[str, Any]:
    """``myssia --version`` 等价:版本 + 协议版本 + app 版本(C10)。

    ``app_version`` 透传壳层注入的 ``MYIA_APP_VERSION``(main.rs spawn 时取
    package_info,单一事实源 = tauri.conf.json version);dev/CLI 场景未注入 =
    null(如实,不虚构)。
    """
    return {
        "name": "myssia",
        "version": myssia.__version__,
        "protocol": PROTOCOL_VERSION,
        "app_version": os.environ.get("MYIA_APP_VERSION") or None,
    }


def _m_health(params: dict[str, Any]) -> dict[str, Any]:
    """``myssia list --json`` 等价:插件清单 + 源健康度 + 计数聚合。

    plugins_dir/db 缺省走 serve 上下文(home 模式 = 数据根;dev = cwd 相对);
    home 模式零品类 YAML 时附 ``first_run=true``(UI 空态引导,不报错)。
    """
    ctx = _serve_context()
    argv = [
        "list",
        "--plugins-dir", str(params.get("plugins_dir") or ctx.plugins_dir),
        "--db", str(params.get("db") or ctx.db),
        "--json",
    ]
    code, payload = _cli_json(argv)
    if code != 0:
        raise _cli_error(code, payload)
    assert payload is not None
    counts = {"ok": 0, "degraded": 0, "dead": 0, "unknown": 0}
    for plugin in payload.get("plugins", []):
        for source in plugin.get("sources", []):
            state = source.get("health", {}).get("state")
            if state in counts:
                counts[state] += 1
    payload["summary"] = {
        "plugins": len(payload.get("plugins", [])),
        "sources": sum(counts.values()),
        **counts,
    }
    # healthy 语义对齐 doctor:dead=error 级;degraded 只算 warning。
    payload["healthy"] = counts["dead"] == 0 and payload.get("store_error") is None
    payload["first_run"] = ctx.first_run()
    payload["exit_code"] = code
    return payload


def _m_plugins_list(params: dict[str, Any]) -> dict[str, Any]:
    """``myssia plugin list --json`` 等价:已装市场插件 + findings。

    ``dir`` 缺省走 serve 上下文安装根(home 模式 = ``MYIA_PLUGIN_DIR`` env
    否则 ``<home>/plugins``;市场面首跑合法为空,design.md D7)。
    ``gates_file`` 缺省走 gates.yaml 上下文路径(门槛件分组/徽标派生,
    批二 D4;显式 params 永远赢)。
    """
    ctx = _serve_context()
    argv = [
        "plugin", "list", "--json",
        "--dir", str(params.get("dir") or ctx.install_root),
        "--gates-file", str(params.get("gates_file") or _gates_yaml_path(ctx)),
    ]
    code, payload = _cli_json(argv)
    if code != 0:
        raise _cli_error(code, payload)
    assert payload is not None
    payload["exit_code"] = code
    return payload


# ---------------------------------------------------------------------------
# 随包插件组件包:发现 / 一键安装(10-05-bundled-plugins-install)
# ---------------------------------------------------------------------------


def _bundled_plugins_root() -> Path | None:
    """随包插件组件包目录(``MYIA_BUNDLED_PLUGINS`` env;dev/未注入 = None)。

    壳层 spawn 时 release 且用户未显式设才注入 Resources/plugins(壳侧
    pyenv.rs ``bundled_plugins_env_value`` 同规则);**env 未设/目录不存在
    都是合法空态**(dev 形态、旧包、自动化冒烟未注入)——返回 None,发现
    面如实报空,不虚构。
    """
    raw = os.environ.get(BUNDLED_PLUGINS_ENV)
    if not raw:
        return None
    root = Path(raw).expanduser()
    return root if root.is_dir() else None


def _bundled_plugin_views(root: Path, install_root: str) -> list[dict[str, Any]]:
    """枚举随包目录下含 manifest 的子目录 → 发现条目视图(零参数,零异常上抛)。

    逐目录:目录序(确定性);manifest 可读 → 摘要(id/name/version/tier/gate/
    requires/provides——manifest schema 无 description 字段,摘要以实况字段为
    准,不硬凑);manifest 坏 → 条目照常入列,id=None + findings 带
    ``manifest_invalid``(沿 yaml.list「坏文件也入列」先例,坏件不拦整表)。
    已装态对齐安装根 ``InstalledPluginStore.entries()`` 的 plugin_id(manifest
    坏的已装目录按目录名兜底,locate 同口径):installed/installed_version
    (已装但 manifest 坏 → 版本 None,如实)。
    """
    installed = {entry.plugin_id or entry.dir_name: entry for entry in InstalledPluginStore(install_root).entries()}
    views: list[dict[str, Any]] = []
    for child in sorted(root.iterdir(), key=lambda item: item.name):
        if child.name.startswith(".") or not child.is_dir():
            continue
        manifest_file = (child / "plugin.yaml") if (child / "plugin.yaml").is_file() else (child / "plugin.yml")
        if not manifest_file.is_file():
            continue  # 平铺品类 YAML/散落文件不是组件包(补种面已覆盖品类)
        view: dict[str, Any] = {
            "dir_name": child.name,
            "path": str(child),
            "id": None,
            "name": None,
            "version": None,
            "tier": None,
            "gate": None,
            "compatible": None,
            "compatible_current": None,
            "requires": [],
            "provides": [],
            "installed": False,
            "installed_version": None,
            "findings": [],
        }
        try:
            manifest = load_manifest_file(manifest_file)
        except Exception as exc:  # noqa: BLE001 - LoadError 与意外 IO 一律条目级 finding
            first = str(exc).splitlines()[0] if str(exc) else type(exc).__name__
            detail = exc.to_dict() if hasattr(exc, "to_dict") else None
            view["findings"].append({
                "severity": "error", "scope": f"plugin:{child.name}", "code": "manifest_invalid",
                "message": f"随包插件 manifest 校验失败({manifest_file}): {first}",
                **({"detail": detail} if detail is not None else {}),
            })
            views.append(view)
            continue
        view.update({
            "id": manifest.id,
            "name": manifest.name,
            "version": manifest.version,
            "tier": manifest.tier,
            "gate": manifest.gate,
            "compatible": manifest.compatible,
            "compatible_current": _manifest_compatible_with_current(manifest.compatible),
            "requires": list(manifest.requires),
            "provides": list(manifest.provides),
        })
        # id 与目录名不一致(包内约定应一致;不一致如实透出,安装按 manifest id 落目录)
        if manifest.id != child.name:
            view["findings"].append({
                "severity": "warning", "scope": f"plugin:{child.name}", "code": "id_mismatch",
                "message": f"随包目录名 {child.name!r} 与 manifest id {manifest.id!r} 不一致(按 manifest id 为准)",
            })
        entry = installed.get(manifest.id)
        if entry is not None:
            view["installed"] = True
            view["installed_version"] = entry.manifest.version if entry.manifest is not None else None
            if entry.manifest is not None and _manifest_compatible_with_current(entry.manifest.compatible) is False:
                view["findings"].append({
                    "severity": "warning", "scope": f"plugin:{manifest.id}", "code": "incompatible_version",
                    "message": f"已装版本要求 myssia {entry.manifest.compatible},当前不兼容(插件将被跳过,核心流水线不受影响)",
                })
        views.append(view)
    return views


def _manifest_compatible_with_current(compatible: str) -> bool | None:
    """版本范围对当前 myssia 的兼容判定(范围串不可解析 → None,无从判断如实)。"""
    try:
        return VersionRange(compatible).contains(myssia.__version__)
    except VersionSpecError:
        return None


def _locate_bundled_plugin_dir(root: Path, plugin_id: str) -> Path:
    """随包目录内按 id 定位组件包目录(目录名直配 > manifest id 匹配兜底)。

    id 已过 ``_PLUGIN_ID_RE``(仅小写字母/数字/_-,无路径穿越可能);找不到
    → ``bundled_plugin_not_found`` 结构化拒。
    """
    direct = root / plugin_id
    if direct.is_dir() and any(direct.glob("plugin.y*ml")):
        return direct
    for child in sorted(root.iterdir(), key=lambda item: item.name):
        if child.name.startswith(".") or not child.is_dir():
            continue
        manifest_file = (child / "plugin.yaml") if (child / "plugin.yaml").is_file() else (child / "plugin.yml")
        if not manifest_file.is_file():
            continue
        try:
            manifest = load_manifest_file(manifest_file)
        except Exception:  # noqa: BLE001 - 坏 manifest 的目录不是可安装来源
            continue
        if manifest.id == plugin_id:
            return child
    raise ProtocolError(
        "bundled_plugin_not_found",
        f"随包插件目录内没有 id 为 {plugin_id!r} 的组件包(可用件见 plugins.bundled.list)",
        path="params.id",
    )


def _m_plugins_bundled_list(params: dict[str, Any]) -> dict[str, Any]:
    """``plugins.bundled.list``:随包插件组件包发现(装机态一键安装的数据面)。

    枚举 ``MYIA_BUNDLED_PLUGINS`` 目录下含 manifest 的子目录 → manifest 摘要
    +已装态(对齐安装根 InstalledPluginStore);**env 未设/目录不存在 =
    合法空表**(dev 形态/旧包/未注入如实,``dir=null`` 不虚构)。坏 manifest
    条目级 finding 不整表炸(yaml.list 先例)。

    批二(10-05-bundled-plugins-batch2 R3)增 ``categories`` 键:随包目录
    平铺品类 YAML 发现视图(``_bundled_category_views``);``count`` 语义
    不变(= 组件包数,兼容既有契约/UI),品类件数由 ``len(categories)``
    自取。"""
    root = _bundled_plugins_root()
    if root is None:
        return {"dir": None, "count": 0, "plugins": [], "categories": []}
    ctx = _serve_context()
    plugins = _bundled_plugin_views(root, ctx.install_root)
    categories = _bundled_category_views(root, ctx.plugins_dir)
    return {
        "dir": str(root),
        "count": len(plugins),
        "plugins": plugins,
        "categories": categories,
    }


def _bundled_dir_carries_source(pkg_dir: Path) -> bool:
    """随包组件包目录是否携带源码件(旧包形态判定,D3 回退门)。

    新分发规范(10-06 INV-1/2)包内组件包只有声明件(plugin.yaml +
    README.md);子树出现任意 ``*.py`` **文件**才算旧包形态(旧包必携
    adapter.py 或自有子包源码件如 credhunter/)——锁缺席时按旧「包内
    直拷」路径回退自愈,零硬切。

    目录存在不算源码信号:纯声明件目录被 ``__pycache__``/logs 等缓存
    目录污染时,按「非隐藏子目录」误判旧包会直拷装出缺 adapter 的空壳
    「已装」件;数据-only 目录(无任何 .py)本就无可跑入口,归
    plugin_lock_missing 结构化拒语义正确。
    """
    return any(child.is_file() and child.suffix == ".py" for child in pkg_dir.rglob("*"))


def _m_plugins_bundled_install(params: dict[str, Any]) -> dict[str, Any]:
    """``plugins.bundled.install {id, force?}``:随包组件包一键装进安装根。

    10-06 分发规范起三岔编排(声明随包、源码远取):

    1. **远取主路径**:随包 ``plugins.lock.json``(内容寻址锁)内有该件
       条目 → ``install_remote`` 拉资产 → sha256 校验 → 安全解包暂存 →
       ``InstalledPluginStore.install`` 同门落位;已装未 force 零网络先拒。
    2. **旧包回退**(D3):锁缺席(或无条目)但包内目录携带源码件 → 现行
       ``_locate_bundled_plugin_dir`` + ``store.install(source)`` 直拷,
       零改动(旧装机包自愈)。
    3. **结构化拒**:包内只有声明件而锁无条目 → ``plugin_lock_missing``
       (不静默不虚构——直拷声明件会装出不能跑的空壳件)。

    装卸门零新增:id 过 ``_PLUGIN_ID_RE`` 同门(防穿越,manifest.py/
    installed.py 同源正则)→ 远取/直拷殊途同归 ``InstalledPluginStore.install``
    (与 CLI ``myssia plugin install`` 同门:manifest 校验 → 版本矩阵 →
    整目录拷贝绝不半装;已装未 force/版本不兼容未 force 结构化拒,
    ``PluginStoreError`` code 原文透传,远取链失败额外带 data 定位信息
    url/sha256 期望实得/HTTP status)。应答 ``{ok, dir, version}`` 契约不变。
    """
    root = _bundled_plugins_root()
    if root is None:
        raise ProtocolError(
            "bundled_plugins_unavailable",
            "随包插件目录不可用(dev 形态或旧包未注入 MYIA_BUNDLED_PLUGINS);无法一键安装",
            path="params.id",
        )
    plugin_id = params.get("id")
    if not isinstance(plugin_id, str) or not _PLUGIN_ID_RE.match(plugin_id):
        raise ProtocolError(
            "invalid_params",
            "缺少合法字符串字段 id(插件 id 应为小写字母/数字开头,可含连字符/下划线,2-64 字符)",
            path="params.id",
        )
    force = params.get("force", False)
    if not isinstance(force, bool):
        raise ProtocolError("invalid_params", "force 必须为布尔", path="params.force")
    store = InstalledPluginStore(_serve_context().install_root)
    try:
        lock = load_plugins_lock(root)
        if lock is not None and plugin_id in lock.assets:
            result = install_remote(lock, plugin_id, store, force=force)
        else:
            source = _locate_bundled_plugin_dir(root, plugin_id)
            if _bundled_dir_carries_source(source):
                result = store.install(source, force=force)
            else:
                raise PluginRemoteError(
                    "plugin_lock_missing",
                    f"随包插件 {plugin_id} 无可安装来源:包内只有声明件(源码远取规范),"
                    f"而远取锁{'缺该件条目' if lock is not None else '缺失'}"
                    f"({root / LOCK_FILENAME});请更新安装包或核对锁文件",
                    data={"plugin_id": plugin_id, "lock": str(root / LOCK_FILENAME), "lock_present": lock is not None},
                )
    except PluginStoreError as exc:
        data: dict[str, Any] = {"errors": exc.errors} if exc.errors else {}
        data.update(getattr(exc, "data", None) or {})
        raise ProtocolError(
            exc.code,
            f"随包插件安装失败: {exc}",
            path="params.id",
            data=data or None,
        ) from exc
    return {"ok": True, "dir": result["path"], "version": result["version"]}


def _m_plugins_bundled_uninstall(params: dict[str, Any]) -> dict[str, Any]:
    """``plugins.bundled.uninstall {id}``:卸载 = 删安装根拷贝(批二 R2)。

    与 install 对称直调 ``InstalledPluginStore.remove``(CLI
    ``myssia plugin remove`` 同门:id 门/结构化错误/绝不半删);**随包原件
    只读永不删**,卸载后可随时经 ``plugins.bundled.install`` 重装。
    **不依赖随包目录**(``MYIA_BUNDLED_PLUGINS`` 未设也能卸)——卸载是
    安装根操作,与发现来源无关(dev 形态/旧包已装件同样可卸,如实)。
    ``PluginStoreError`` code 原文透传(``not_installed``/``io_error``)。
    应答 ``{ok, id, path}``。
    """
    plugin_id = params.get("id")
    if not isinstance(plugin_id, str) or not _PLUGIN_ID_RE.match(plugin_id):
        raise ProtocolError(
            "invalid_params",
            "缺少合法字符串字段 id(插件 id 应为小写字母/数字开头,可含连字符/下划线,2-64 字符)",
            path="params.id",
        )
    store = InstalledPluginStore(_serve_context().install_root)
    try:
        result = store.remove(plugin_id)
    except PluginStoreError as exc:
        raise ProtocolError(
            exc.code,
            f"随包插件卸载失败: {exc}",
            path="params.id",
        ) from exc
    return {"ok": True, "id": result["id"], "path": result["path"]}


def _bundled_category_views(root: Path, plugins_dir: str) -> list[dict[str, Any]]:
    """枚举随包目录平铺品类 YAML → 发现条目视图(批二 R3;零异常上抛)。

    与 ``_seed_first_run`` 同款 glob 口径(非递归 ``*.yaml``/``*.yml``),
    装机态两视图所见 = 补种所拷。逐件:id/name/schedule 经
    ``load_category_file`` 实读(坏 YAML → id=None + 条目级 finding
    ``category_invalid``,不整表炸,沿 yaml.list 先例);``exists`` = 数据根
    plugins/ 下同名文件在(= 补种/自建/本面已装,对齐补种落点);文件名 stem
    与 id 不一致 → ``id_mismatch`` warning 如实透出(定位仍按 id 双路兜底)。
    """
    target_dir = Path(plugins_dir)
    files = sorted([*root.glob("*.yaml"), *root.glob("*.yml")], key=lambda item: item.name)
    views: list[dict[str, Any]] = []
    for source in files:
        view: dict[str, Any] = {
            "file": source.name,
            "path": str(source),
            "id": None,
            "name": None,
            "schedule": None,
            "exists": (target_dir / source.name).exists(),
            "findings": [],
        }
        try:
            config = load_category_file(source)
        except Exception as exc:  # noqa: BLE001 - LoadError 与意外 IO 一律条目级 finding
            first = str(exc).splitlines()[0] if str(exc) else type(exc).__name__
            detail = exc.to_dict() if hasattr(exc, "to_dict") else None
            view["findings"].append({
                "severity": "error", "scope": f"category:{source.name}", "code": "category_invalid",
                "message": f"随包品类 YAML 校验失败({source}): {first}",
                **({"detail": detail} if detail is not None else {}),
            })
            views.append(view)
            continue
        view.update({"id": config.id, "name": config.name, "schedule": config.schedule})
        if config.id != source.stem:
            view["findings"].append({
                "severity": "warning", "scope": f"category:{source.name}", "code": "id_mismatch",
                "message": f"随包文件名 {source.name!r} 与品类 id {config.id!r} 不一致(定位按 id 双路兜底)",
            })
        views.append(view)
    return views


def _locate_bundled_category_yaml(root: Path, category_id: str) -> Path:
    """随包目录内按 id 定位品类 YAML(文件名 stem 直配 > YAML id 字段兜底)。

    id 已过 ``CATEGORY_ID_RE``(仅小写字母/数字/_-,无路径穿越可能);找不到
    → ``bundled_category_not_found`` 结构化拒。
    """
    files = sorted([*root.glob("*.yaml"), *root.glob("*.yml")], key=lambda item: item.name)
    for candidate in files:
        if candidate.stem == category_id:
            return candidate
    for candidate in files:  # 兜底:文件名漂移但 YAML id 命中(id_mismatch 件可达)
        try:
            config = load_category_file(candidate)
        except Exception:  # noqa: BLE001 - 坏 YAML 不是可安装来源
            continue
        if config.id == category_id:
            return candidate
    raise ProtocolError(
        "bundled_category_not_found",
        f"随包目录内没有 id 为 {category_id!r} 的品类 YAML(可用件见 plugins.bundled.list 的 categories)",
        path="params.id",
    )


def _m_plugins_bundled_category_install(params: dict[str, Any]) -> dict[str, Any]:
    """``plugins.bundled.category_install {id, force?}``:随包品类 YAML 平铺
    拷进数据根 plugins/(批二 R3)。

    与组件包安装语义刻意不同(组件包=整目录拷贝进安装根;品类=单文件平铺
    到数据根,与 ``_seed_first_run`` 补种同落点):id 过 ``CATEGORY_ID_RE``
    (schema 同源防穿越)→ 定位 → ``load_category_file`` 校验通过才装(坏件
    拒零拷贝)→ tmp+rename 原子拷到 ``<plugins_dir>/<源文件名>``。**已有同名
    文件未 force → ``category_exists`` 结构化拒(如实「已存在」不覆盖)**——
    与补种幂等补缺对齐不打架:补种=自动补缺永不覆盖,本面=显式知情操作,
    force 才覆盖。应答 ``{ok, file, path}``。
    """
    root = _bundled_plugins_root()
    if root is None:
        raise ProtocolError(
            "bundled_plugins_unavailable",
            "随包插件目录不可用(dev 形态或旧包未注入 MYIA_BUNDLED_PLUGINS);无法安装品类",
            path="params.id",
        )
    category_id = params.get("id")
    if not isinstance(category_id, str) or not CATEGORY_ID_RE.match(category_id):
        raise ProtocolError(
            "invalid_params",
            "缺少合法字符串字段 id(品类 id 应为小写字母/数字开头,可含连字符/下划线,1-64 字符)",
            path="params.id",
        )
    force = params.get("force", False)
    if not isinstance(force, bool):
        raise ProtocolError("invalid_params", "force 必须为布尔", path="params.force")
    source = _locate_bundled_category_yaml(root, category_id)
    try:
        load_category_file(source)
    except Exception as exc:  # noqa: BLE001 - LoadError 结构化(坏件拒,零拷贝)
        first = str(exc).splitlines()[0] if str(exc) else type(exc).__name__
        raise ProtocolError(
            "category_invalid",
            f"随包品类校验失败({source}): {first}",
            path="params.id",
        ) from exc
    target = Path(_serve_context().plugins_dir) / source.name
    if target.exists() and not force:
        raise ProtocolError(
            "category_exists",
            f"数据根已有同名品类文件 {target}(补种或用户自建件,如实不覆盖);确认覆盖请加 force",
            path="params.id",
        )
    tmp = target.with_name(f".{source.name}.tmp")
    try:
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, tmp)
        os.replace(tmp, target)  # 原子替换:force 覆盖不留半截,中途失败不留残件
    except OSError as exc:
        tmp.unlink(missing_ok=True)
        raise ProtocolError(
            "io_error",
            f"品类文件拷贝失败({source} → {target}): {exc}",
            path="params.id",
        ) from exc
    return {"ok": True, "file": source.name, "path": str(target)}


# ---------------------------------------------------------------------------
# 轨D remote 声明配置(10-06-native-plugin-components 阶段3,G-Q1/R7):
# tier=remote 插件件的端点/凭据引用读写 —— 设置页「随包官方插件件」卡条目
# 详情区 remote 配置面板的数据面。配置落数据根(remote-plugins.json),
# 引擎侧零改动:本层把配置桥接进 env 通道(引擎 firecrawl.py 既有解析),
# env 显式设置 = 开发后门恒优先(setdefault 语义)。
# ---------------------------------------------------------------------------

#: 数据根下的 remote 插件配置文件名(机器写面,JSON;人读人改走文件本身)。
REMOTE_PLUGINS_CONFIG = "remote-plugins.json"

#: 轨D 引擎桥接表:插件 id → (端点 env 名, API 键 env 名, 凭据规范名)。
#: 只列「引擎经 env 通道消费端点」的 remote 件;纯品类 YAML 消费的 remote 件
#: (rsshub/webcheck 等)不走 env,不在表内。env 名与引擎常量同源(firecrawl.py
#: 零改动的桥接点)。
_REMOTE_ENGINE_BRIDGE: dict[str, tuple[str, str, str]] = {
    "myssia-firecrawl": (ENV_FIRECRAWL_URL, ENV_FIRECRAWL_API_KEY, "myia/firecrawl/api-key"),
}

#: 本层已桥接写入的 env 值(变量名 → 我方写入值)。save 后再桥接时,只有
#: 「未设置 == 我方上次写值」的变量才允许更新——用户/开发者显式设置的 env
#: (开发后门)永不被配置面板覆写。
_BRIDGED_ENV: dict[str, str] = {}


def _remote_plugins_config_path() -> Path | None:
    """remote 插件配置路径(home 模式 ``<home>/remote-plugins.json``;dev 无)。"""
    ctx = _serve_context()
    if ctx.home is None:
        return None
    return ctx.home / REMOTE_PLUGINS_CONFIG


def _load_remote_plugins_config(path: Path) -> dict[str, dict[str, Any]]:
    """读 remote 插件配置(缺文件 = 空表;坏 JSON = 结构化拒,不静默吞)。"""
    if not path.is_file():
        return {}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        raise ProtocolError(
            "remote_config_invalid",
            f"remote 插件配置不可读({path}): {exc}",
            path="params.id",
        ) from exc
    if not isinstance(data, dict):
        raise ProtocolError(
            "remote_config_invalid",
            f"remote 插件配置顶层必须是对象({path})",
            path="params.id",
        )
    # 条目级宽容:非对象条目跳过(文件被手改出杂键不拦整个配置面)
    return {key: value for key, value in data.items() if isinstance(value, dict)}


def _save_remote_plugins_config(path: Path, data: dict[str, dict[str, Any]]) -> None:
    """原子写 remote 插件配置(tmp+rename;中途失败不留半截)。"""
    tmp = path.with_name(f".{path.name}.tmp")
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        tmp.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        os.replace(tmp, path)
    except OSError as exc:
        tmp.unlink(missing_ok=True)
        raise ProtocolError(
            "io_error",
            f"remote 插件配置写入失败({path}): {exc}",
            path="params.id",
        ) from exc


def _apply_remote_env_bridge(plugin_id: str, record: dict[str, Any]) -> None:
    """把一件 remote 配置桥接进 env(引擎零改动的通道;setdefault 语义)。

    - 端点:配置 endpoint(具体 http(s) 地址)→ ``os.environ.setdefault``;
      env 已设(开发后门)恒优先,不覆写;
    - API 键:配置 token 是 keychain 引用时,经钥匙串解析成值再入 env(引擎
      env 通道只认具体值;解析失败 = 跳过并留痕,引擎侧按「未配键」降级)。

    只动 ``_BRIDGED_ENV`` 记账内的自有值;save 后的再桥接同门(防覆写显式 env)。
    """
    bridge = _REMOTE_ENGINE_BRIDGE.get(plugin_id)
    if bridge is None:
        return  # 非引擎消费件:配置面存读即可,无 env 通道
    url_var, key_var, token_name = bridge
    endpoint = record.get("endpoint")
    if isinstance(endpoint, str) and endpoint.strip():
        value = endpoint.strip()
        if url_var not in os.environ or os.environ.get(url_var) == _BRIDGED_ENV.get(url_var):
            os.environ[url_var] = value
            _BRIDGED_ENV[url_var] = value
    token = record.get("token")
    if isinstance(token, str) and token.startswith("keychain:"):
        try:
            api_key = get_secret(token.removeprefix("keychain:"))
        except SecretError as exc:
            myssia_log.stream_line(None, "stderr", f"sidecar: {plugin_id} API 键桥接跳过: {exc}")
            return
        if key_var not in os.environ or os.environ.get(key_var) == _BRIDGED_ENV.get(key_var):
            os.environ[key_var] = api_key
            _BRIDGED_ENV[key_var] = api_key


def _startup_remote_env() -> None:
    """serve 启动的一次性 env 桥接;失败只留痕,绝不拦服务起来。

    firecrawl 桌面态端点由配置面板提供(写数据根配置),本函数在启动时把
    配置读进 env —— 引擎/doctor(同进程)即按既有 env 通道消费,桌面态零
    env 依赖;显式 env(开发后门)setdefault 语义恒优先。
    """
    try:
        path = _remote_plugins_config_path()
        if path is None:
            return
        for plugin_id, record in _load_remote_plugins_config(path).items():
            _apply_remote_env_bridge(plugin_id, record)
    except Exception as exc:  # noqa: BLE001 — 桥接是增强,不是依赖
        print(f"sidecar: remote 插件配置 env 桥接失败(忽略): {exc}", file=sys.stderr)


def _remote_plugin_id(params: dict[str, Any]) -> str:
    """params.id 的形状门(与 plugins.bundled.* 同门防穿越)。"""
    plugin_id = params.get("id")
    if not isinstance(plugin_id, str) or not _PLUGIN_ID_RE.match(plugin_id):
        raise ProtocolError(
            "invalid_params",
            "缺少合法字符串字段 id(插件 id 应为小写字母/数字开头,可含连字符/下划线,2-64 字符)",
            path="params.id",
        )
    return plugin_id


def _m_plugins_remote_get(params: dict[str, Any]) -> dict[str, Any]:
    """``plugins.remote.get {id}``:读一件 remote 插件的端点/凭据引用配置。

    应答 ``{id, endpoint, token, known}``:未配置 = endpoint/token null +
    known=false(如实,不虚构);``token`` 是 keychain 引用名(值永不出协议
    面,只有 secret.set 写入、secret.list 可见)。dev 形态(无数据根)→
    ``remote_config_unavailable`` 结构化拒(开发后门 = env,面板是桌面态面)。
    """
    path = _remote_plugins_config_path()
    if path is None:
        raise ProtocolError(
            "remote_config_unavailable",
            "remote 插件配置属桌面数据根(dev 形态无 MYIA_HOME);开发后门 = 显式 env(如 MYIA_FIRECRAWL_URL)",
            path="params.id",
        )
    plugin_id = _remote_plugin_id(params)
    record = _load_remote_plugins_config(path).get(plugin_id, {})
    return {
        "id": plugin_id,
        "endpoint": record.get("endpoint"),
        "token": record.get("token"),
        "known": bool(record),
    }


def _m_plugins_remote_save(params: dict[str, Any]) -> dict[str, Any]:
    """``plugins.remote.save {id, endpoint, token?}``:写一件 remote 插件配置。

    校验(与 schema keychain-only 判例同规,配置面禁明文凭据):
    - ``endpoint`` 必填,具体 http(s) 地址(env:/keychain: 引用不是端点,
      引用属品类 YAML/env 开发后门);
    - ``token`` 可选;给定则必须是 keychain: 规范引用(明文经面板只在
      secret.set 通道入钥匙串,永不落本配置;不传 = 保持现值)。

    写后即时再桥接 env(引擎同进程消费,无需重启壳);显式 env(开发后门)
    恒优先不被覆写(``_BRIDGED_ENV`` 记账)。应答 ``{ok, id, path, endpoint}``。
    """
    path = _remote_plugins_config_path()
    if path is None:
        raise ProtocolError(
            "remote_config_unavailable",
            "remote 插件配置属桌面数据根(dev 形态无 MYIA_HOME);开发后门 = 显式 env(如 MYIA_FIRECRAWL_URL)",
            path="params.id",
        )
    plugin_id = _remote_plugin_id(params)
    endpoint = params.get("endpoint")
    if not isinstance(endpoint, str) or not re.match(r"^https?://\S+$", endpoint.strip()):
        raise ProtocolError(
            "invalid_params",
            "endpoint 必须是 http(s) 地址(env:/keychain: 引用属品类 YAML/env 通道,不走本面板)",
            path="params.endpoint",
        )
    endpoint = endpoint.strip()
    token = params.get("token")
    if token is not None:
        if not isinstance(token, str) or not token.startswith("keychain:"):
            raise ProtocolError(
                "invalid_params",
                "token 必须是 keychain: 引用(明文凭据经 secret.set 入钥匙串,配置面只存引用)",
                path="params.token",
            )
        try:
            validate_secret_name(token.removeprefix("keychain:"))
        except SecretError as exc:
            raise ProtocolError(exc.code, str(exc), path="params.token") from exc
    data = _load_remote_plugins_config(path)
    record = dict(data.get(plugin_id, {}))
    record["endpoint"] = endpoint
    if token is not None:
        record["token"] = token
    data[plugin_id] = record
    _save_remote_plugins_config(path, data)
    _apply_remote_env_bridge(plugin_id, record)  # 即时生效(显式 env 优先不被覆写)
    return {"ok": True, "id": plugin_id, "path": str(path), "endpoint": endpoint}


def _m_doctor(params: dict[str, Any]) -> dict[str, Any]:
    """``myssia doctor --json`` 等价:结构化诊断(问题全在 findings,完成即 0)。

    G10(10-05-g10-proxy-probe)增可选布尔 ``config_auto``(缺省 false = 现
    行为逐字节不变):``config`` 缺省且为 true 时以 serve 上下文数据根发现
    缺省 ``<home>/pools.yaml``——命中才拼 ``--config``(路径经既有
    ``proxy.config`` 键天然回显,零新应答键),未命中不带 ``--config``
    (= 只看现状)。发现逻辑全在本层,cli.py 零改动(CLI 本无缺省路径概念)。
    """
    ctx = _serve_context()
    if "config_auto" in params and not isinstance(params["config_auto"], bool):
        raise ProtocolError("invalid_params", "config_auto 必须为布尔", path="params.config_auto")
    argv = ["doctor"]
    for yaml_path in params.get("yamls") or []:
        argv.append(str(yaml_path))
    argv += ["--plugins-dir", str(params.get("plugins_dir") or ctx.plugins_dir)]
    argv += ["--db", str(params.get("db") or ctx.db)]
    argv += ["--dir", str(params.get("dir") or ctx.install_root)]
    argv += ["--gates-file", str(params.get("gates_file") or _gates_yaml_path(ctx))]
    if params.get("config"):
        argv += ["--config", str(params["config"])]
    elif params.get("config_auto") and ctx.home is not None:
        default_pools = ctx.home / "pools.yaml"
        if default_pools.exists():
            argv += ["--config", str(default_pools)]
    if params.get("probe_timeout") is not None:
        argv += ["--probe-timeout", str(params["probe_timeout"])]
    argv.append("--json")
    code, payload = _cli_json(argv)
    if code != 0:
        raise _cli_error(code, payload)
    assert payload is not None
    payload["exit_code"] = code
    return payload


# ---------------------------------------------------------------------------
# 方法:store.items / store.state.*(G9 读态)/ secret.* (凭据只入钥匙链)
# ---------------------------------------------------------------------------

#: store.state.* 的 marker 枚举(items 表三列一一对应;列名白名单防注入,
#: 真白名单在 store 层 ``_ITEM_STATE_COLUMNS``)。
_ITEM_STATE_MARKERS = ("read", "starred", "later")
#: store.state.mark 单请求 keys 上限(G9 防御性常量):mark 的作用域 = 单键
#: toggle 与已加载批量(一页 50/limit ≤200),整库语义必须走 mark_all——
#: 上限是误用防线不是容量声明,超限 invalid_params 提示走 mark_all。
_STATE_MARK_KEYS_MAX = 2000
#: localStorage 读态一次性搬迁的幂等旗标键(store_meta;G9 Q2.2:服务端
#: 旗标是唯一真相,webview 数据可被独立清掉、客户端旗标不可信)。
FEED_STATE_IMPORTED_AT_META = "feed_state_imported_at"


def _item_dict(item: Any) -> dict[str, Any]:
    """ItemRecord → 协议字典(raw/content_hash 整包不出协议面)。

    例外是 vision 环产物的**白名单投影**:图析产物挂 ``metadata.image_ocr``
    / ``image_caption`` / ``image_files`` / ``image_ocr_lines``(collect.py,
    10-03-vision-v2 起后三键随落图开关产生),pipeline 以 ``raw=item.metadata``
    入库,feed 屏图析行与详情展开依赖它们(feed-screen.tsx)——只投影这些
    键,raw 其余键仍不出面;无图/类型不符/空白条目置 None,feed 屏零渲染
    变化。``image_ocr_lines`` 逐行 ``{text, conf}`` 原样透传(供详情逐行
    置信度渲染),形态不符(非 list[dict{str, num}])整体置 None 不硬抛。

    G9(v10)起随行带 ``read``/``starred``/``later`` 三布尔键(读态迁服务端,
    items 表三列直读):采集管线永不携带读态(save_item 列清单不含三列),
    置位只走 ``store.state.*``;feed.export JSONL 共用本投影连带多三键
    (CSV 固定列集不变)。

    10-06-feed-channel-groups 起再白名单两组渠道差异化呈现所需的键
    (同一「显式才有」纪律,异型/缺失置 None):价格/优惠七键
    (``price_text``/``sale_price``/``normal_price``/``final_price``/
    ``original_price``/``discount_pct``/``savings_pct``,供游戏/羊毛
    渠道的「价格/优惠行」;``final_price`` 兼收人民币分 int 与 CS/GOG
    美元串别名,换算归消费侧)与 urlwatch 事件两键(``watch_event``/
    ``watch_page``,供官网监控渠道的「变更事件样式」)。raw 其余键
    仍不出协议面。
    """
    raw = item.raw if isinstance(item.raw, Mapping) else {}
    ocr = raw.get("image_ocr")
    caption = raw.get("image_caption")
    files = raw.get("image_files")
    ocr_lines = raw.get("image_ocr_lines")
    projected_lines: list[dict[str, Any]] | None = None
    if isinstance(ocr_lines, list) and ocr_lines:
        sane = [
            {"text": str(line.get("text")), "conf": float(line.get("conf"))}
            for line in ocr_lines
            if isinstance(line, Mapping) and isinstance(line.get("text"), str)
            and isinstance(line.get("conf"), (int, float)) and not isinstance(line.get("conf"), bool)
        ]
        # 行数对不齐(夹杂坏行)= 源数据形态异常,整体置 None 不半投影
        projected_lines = sane if len(sane) == len(ocr_lines) else None
    projected_files: list[str] | None = None
    if isinstance(files, list) and files:
        # 同款严格门:全项皆非空 str 才投影,夹杂坏值整体置 None
        if all(isinstance(path, str) and path for path in files):
            projected_files = list(files)

    def _str_key(name: str) -> str | None:
        value = raw.get(name)
        return value if isinstance(value, str) and value.strip() else None

    def _num_key(name: str) -> int | float | str | None:
        value = raw.get(name)
        if isinstance(value, bool):
            return None
        if isinstance(value, (int, float)):
            return value
        # 字符串价格形态(CS/GOG 美元元 "0.50")原样透传,换算归消费侧
        return value if isinstance(value, str) and value.strip() else None

    return {
        "id": item.id,
        "url": item.url,
        "dedup_key": item.dedup_key,
        "title": item.title,
        "source": item.source,
        "content": item.content,
        "image_ocr": ocr if isinstance(ocr, str) and ocr.strip() else None,
        "image_caption": caption if isinstance(caption, str) and caption.strip() else None,
        "image_files": projected_files,
        "image_ocr_lines": projected_lines,
        # 价格/优惠白名单(10-06-feed-channel-groups:游戏/羊毛渠道差异化
        # 「价格/优惠行」;键 = games 四源 extract 字段名原样——price_text
        # (Epic "¥60.00" 直出)/ sale_price+normal_price(CS·GOG 美元元字符串)
        # / final_price(Epic·Steam 人民币分 int;CS·GOG 美元串别名)/
        # original_price(分 int)/ discount_pct(int)/ savings_pct(CS 字符串
        # %);异型/缺失置 None,raw 其余键仍不出协议面)
        "price_text": _str_key("price_text"),
        "sale_price": _str_key("sale_price"),
        "normal_price": _str_key("normal_price"),
        "final_price": _num_key("final_price"),
        "original_price": _num_key("original_price"),
        "discount_pct": _num_key("discount_pct"),
        "savings_pct": _str_key("savings_pct"),
        # urlwatch 变更事件白名单(同批:官网监控渠道差异化「变更事件样式」;
        # watch_event = new|changed,watch_page = 目标页真链——条目 url 是
        # #watch-<sha> 锚,目标页链接以本键为准)
        "watch_event": _str_key("watch_event"),
        "watch_page": _str_key("watch_page"),
        "tags": item.tags,
        "category": item.category,
        "scores": item.scores,
        "pushed_at": item.pushed_at.isoformat() if item.pushed_at else None,
        "push_slot": item.push_slot,
        "first_seen": item.first_seen.isoformat() if item.first_seen else None,
        "read": bool(item.read),
        "starred": bool(item.starred),
        "later": bool(item.later),
    }


def _m_store_items(params: dict[str, Any]) -> dict[str, Any]:
    """SQLiteStore.list_items 直读(数据面复用:SQLite 单库,零新后端)。

    游标(C1,与 feed-ux G1 合流形状):``before`` = first_seen 严格小于;
    ``before_id`` 与之组成 ``(first_seen, id)`` 复合游标(同刻条目超单页
    limit 也能推进直至取尽);``query`` = title/content/source 三列 LIKE
    NOCASE。``source`` = 源名精确等值(10-06-feed-channel-groups 三级下钻
    L3 渠道消息流;与 ``category`` 同门)。全部可选,旧调用零感知。

    ``with_total``(bool,可选;F2 计数口径根治,10-09-tg-category-entry,
    UI 能力门 protocol ≥ 13):true 时同一 WHERE 跑
    :meth:`SQLiteStore.count_items`(不分页全量计数),应答补 ``total`` 键
    —— feed 屏「已加载 N · 共 T 条」的 T,首页截断不再静默低估。缺省/false
    = 应答无 ``total`` 键(旧调用零感知;UI 未过门回落「已加载 N 条」词面)。
    """
    db = params.get("db") or _serve_context().db

    def _parse_iso(name: str) -> datetime | None:
        raw = params.get(name)
        if not raw:
            return None
        try:
            return datetime.fromisoformat(str(raw))
        except ValueError as exc:
            raise ProtocolError("invalid_params", f"{name} 不是合法 ISO 时间: {raw}", path=f"params.{name}") from exc

    since = _parse_iso("since")
    before = _parse_iso("before")
    before_id = params.get("before_id")
    if before_id is not None:
        if not isinstance(before_id, int) or isinstance(before_id, bool) or before_id < 1:
            raise ProtocolError("invalid_params", "before_id 必须为正整数(与 before 同传)", path="params.before_id")
        if before is None:
            raise ProtocolError("invalid_params", "before_id 需与 before 同传(复合游标)", path="params.before_id")
    query = params.get("query")
    if query is not None and not isinstance(query, str):
        raise ProtocolError("invalid_params", "query 必须为字符串", path="params.query")
    # 深审 F6 校验对称:category 与 source 同门强校验(非空字符串;省略 =
    # 不过滤)—— 此前 category 只靠 store 层兜底,协议面错误码/路径不对称。
    category = params.get("category")
    if category is not None and (not isinstance(category, str) or not category):
        raise ProtocolError(
            "invalid_params", "category 必须为非空字符串(品类精确等值)", path="params.category"
        )
    source = params.get("source")
    if source is not None and (not isinstance(source, str) or not source):
        raise ProtocolError("invalid_params", "source 必须为非空字符串(源名精确等值)", path="params.source")
    # 源大类过滤(10-08-tg-channel-card v2 卡片墙):im = 通讯软件源,
    # web = 其余含无源;词表与 store 层同门,非法值协议面即拒。
    source_kind = params.get("source_kind")
    if source_kind is not None and source_kind not in ("web", "im"):
        raise ProtocolError(
            "invalid_params", "source_kind 只接受 web/im(不过滤请省略)", path="params.source_kind"
        )
    limit = params.get("limit")
    if limit is not None and (not isinstance(limit, int) or limit < 1):
        raise ProtocolError("invalid_params", "limit 必须为正整数", path="params.limit")
    with_total = params.get("with_total")
    if with_total is not None and not isinstance(with_total, bool):
        raise ProtocolError("invalid_params", "with_total 必须为布尔", path="params.with_total")
    try:
        store = SQLiteStore(db)
    except StoreSchemaError as exc:
        raise ProtocolError(exc.code, str(exc), path="params.db", data=exc.details) from exc
    try:
        items = store.list_items(
            category=category, source=source, source_kind=source_kind, since=since,
            before=before, before_id=before_id, query=query or None, limit=limit,
        )
        # F2 计数口径根治:同一 WHERE 跑 COUNT(count_items 与 list_items 经
        # store 层单点 _items_filter_sql 构造,词义漂移即测试红),total =
        # 该过滤条件全量行数(不含 limit 分页)。
        total = (
            store.count_items(
                category=category, source=source, source_kind=source_kind, since=since,
                before=before, before_id=before_id, query=query or None,
            )
            if with_total
            else None
        )
    except ValueError as exc:  # store 层参数校验(空 category/source 等)
        raise ProtocolError("invalid_params", str(exc), path="params") from exc
    finally:
        store.close()
    result = {"db": str(db), "count": len(items), "items": [_item_dict(item) for item in items]}
    if with_total:
        result["total"] = total
    return result


def _m_store_source_stats(params: dict[str, Any]) -> dict[str, Any]:
    """分源聚合(v8 三级界面 1 级类型卡统计底座,10-09-tg-category-entry)。

    ``{since?, db?}`` → ``{rows: [{source, total, today, unread,
    latest_first_seen, latest_title}]}``;since = 当日窗锚 ISO(UI 传
    ``dayWindowStart().toISOString()``,03:00 窗锚与视图同源;省略 = today
    恒 0,「无窗无今日」如实)。非法 ISO → ``invalid_params``(_parse_iso
    同门)。UI 能力门 STATS_PROTOCOL = 14(v8 注记);低版本 sidecar 无此
    方法 → 客户端回落 catalog 已加载口径,**不发 RPC 试错**(门先行,
    COUNT_PROTOCOL 同模式)。
    """
    db = params.get("db") or _serve_context().db

    def _parse_iso(name: str) -> datetime | None:
        raw = params.get(name)
        if not raw:
            return None
        try:
            return datetime.fromisoformat(str(raw))
        except ValueError as exc:
            raise ProtocolError("invalid_params", f"{name} 不是合法 ISO 时间: {raw}", path=f"params.{name}") from exc

    since = _parse_iso("since")
    try:
        store = SQLiteStore(db)
    except StoreSchemaError as exc:
        raise ProtocolError(exc.code, str(exc), path="params.db", data=exc.details) from exc
    try:
        rows = store.source_stats(since=since)
    finally:
        store.close()
    return {"db": str(db), "rows": rows}


def _m_store_state_mark(params: dict[str, Any]) -> dict[str, Any]:
    """按 dedup_key 批量置位读态标记(G9,10-04-read-state-server §4.1)。

    ``{keys, marker, value, db?}`` → ``{updated}``;同 dedup_key 多行
    (dated-key 旋转)同置,与 localStorage itemKey 语义一致;幂等(显式
    置目标值)。``updated`` = SQLite UPDATE rowcount(匹配行数口径,置同值
    行也计入,如实回传不二次核算)。keys 上限 :data:`_STATE_MARK_KEYS_MAX`:
    整库语义走 ``store.state.mark_all``。
    """
    keys = params.get("keys")
    if not isinstance(keys, list) or not keys:
        raise ProtocolError("invalid_params", "keys 必须为非空字符串数组(dedup_key)", path="params.keys")
    if len(keys) > _STATE_MARK_KEYS_MAX:
        raise ProtocolError(
            "invalid_params",
            f"keys 超上限 {_STATE_MARK_KEYS_MAX}(整库语义请走 store.state.mark_all)",
            path="params.keys",
        )
    for key in keys:
        if not isinstance(key, str) or not key:
            raise ProtocolError("invalid_params", "keys 不能包含非字符串或空串", path="params.keys")
    marker = params.get("marker")
    if marker not in _ITEM_STATE_MARKERS:
        raise ProtocolError(
            "invalid_params", "marker 必须是 read/starred/later 之一", path="params.marker"
        )
    value = params.get("value")
    if not isinstance(value, bool):
        raise ProtocolError("invalid_params", "value 必须为布尔", path="params.value")
    db = params.get("db") or _serve_context().db
    try:
        store = SQLiteStore(db)
    except StoreSchemaError as exc:
        raise ProtocolError(exc.code, str(exc), path="params.db", data=exc.details) from exc
    try:
        updated = store.set_item_states(keys, marker, value)
    except ValueError as exc:  # store 层参数校验(marker 白名单等)
        raise ProtocolError("invalid_params", str(exc), path="params") from exc
    finally:
        store.close()
    return {"updated": updated}


def _m_store_state_mark_all(params: dict[str, Any]) -> dict[str, Any]:
    """全库(可选 category)置位读态标记(G9,§4.2)。

    ``{marker, value, category?, db?}`` → ``{updated}``;category 精确等值
    (与 list_items 同参,非 LIKE;不收 query——决议 Q3.2 钉死:LIKE 进
    UPDATE 是范围蠕变)。缺省 category = 全库所有条目(含未翻页/未加载),
    这是「全部标已读」的全库语义来源。
    """
    marker = params.get("marker")
    if marker not in _ITEM_STATE_MARKERS:
        raise ProtocolError(
            "invalid_params", "marker 必须是 read/starred/later 之一", path="params.marker"
        )
    value = params.get("value")
    if not isinstance(value, bool):
        raise ProtocolError("invalid_params", "value 必须为布尔", path="params.value")
    category = params.get("category")
    if category is not None and (not isinstance(category, str) or not category):
        raise ProtocolError(
            "invalid_params", "category 必须为非空字符串(全库请省略)", path="params.category"
        )
    # 源大类作用域(10-08-tg-channel-card v2):与 store.items 同词表同门。
    source_kind = params.get("source_kind")
    if source_kind is not None and source_kind not in ("web", "im"):
        raise ProtocolError(
            "invalid_params", "source_kind 只接受 web/im(全库请省略)", path="params.source_kind"
        )
    db = params.get("db") or _serve_context().db
    try:
        store = SQLiteStore(db)
    except StoreSchemaError as exc:
        raise ProtocolError(exc.code, str(exc), path="params.db", data=exc.details) from exc
    try:
        updated = store.set_all_item_states(marker, value, category, source_kind)
    except ValueError as exc:
        raise ProtocolError("invalid_params", str(exc), path="params") from exc
    finally:
        store.close()
    return {"updated": updated}


def _m_store_state_import(params: dict[str, Any]) -> dict[str, Any]:
    """localStorage 读态快照一次性搬迁(G9 搬迁门,Q2;§4.3)。

    ``{states: {<key>: {read?, starred?, later?}}, db?}`` → ``{imported,
    skipped}``;key 三分:dedup_key 直配 / ``id:<n>`` 先解析到键 / ``id:<url>``
    及无从解析形态如实计 skipped(条目已剪枝不复活)。幂等旗标 = store_meta
    :data:`FEED_STATE_IMPORTED_AT_META`:已设 → ``{imported: 0, skipped: 0}``
    不触库(重放不可能,Q2.2);未设 → 导入后落 ISO 时间戳。
    """
    states = params.get("states")
    if not isinstance(states, dict):
        raise ProtocolError(
            "invalid_params", "states 必须为对象({<key>: {read?/starred?/later?}})", path="params.states"
        )
    for key, snapshot in states.items():
        if not isinstance(key, str) or not key:
            raise ProtocolError(
                "invalid_params", "states 键必须为非空字符串(dedup_key 或 id:<n>)", path="params.states"
            )
        if not isinstance(snapshot, dict):
            raise ProtocolError("invalid_params", f"states[{key}] 必须为对象", path="params.states")
        for name, flag in snapshot.items():
            if name not in _ITEM_STATE_MARKERS or not isinstance(flag, bool):
                raise ProtocolError(
                    "invalid_params", f"states[{key}] 仅接受 read/starred/later 布尔键", path="params.states"
                )
    db = params.get("db") or _serve_context().db
    try:
        store = SQLiteStore(db)
    except StoreSchemaError as exc:
        raise ProtocolError(exc.code, str(exc), path="params.db", data=exc.details) from exc
    try:
        if store.get_meta(FEED_STATE_IMPORTED_AT_META) is not None:
            return {"imported": 0, "skipped": 0}  # 旗标已设:no-op,不触 items
        imported, skipped = store.import_item_states(states)
        store.set_meta(
            FEED_STATE_IMPORTED_AT_META, datetime.now(timezone.utc).isoformat()
        )
    finally:
        store.close()
    return {"imported": imported, "skipped": skipped}


def _m_secret_set(params: dict[str, Any]) -> dict[str, Any]:
    """薄包装 myssia.secrets.set_secret:凭据只入系统钥匙链;值零回显零落日志。"""
    name, value = params.get("name"), params.get("value")
    if not isinstance(name, str) or not name:
        raise ProtocolError("invalid_params", "缺少凭据名 name(myia/<scope>/<name>)", path="params.name")
    if not isinstance(value, str) or not value:
        raise ProtocolError("invalid_params", "缺少凭据值 value", path="params.value")
    try:
        set_secret(name, value)
    except SecretError as exc:
        raise ProtocolError(exc.code, str(exc), path="params.name") from exc
    return {"name": name, "stored": True}


def _m_secret_list(params: dict[str, Any]) -> dict[str, Any]:
    """薄包装 myssia.secrets.list_secrets:只有名字,值永不可读。"""
    try:
        names = list_secrets()
    except SecretError as exc:
        raise ProtocolError(exc.code, str(exc)) from exc
    return {"names": names}


def _m_secret_delete(params: dict[str, Any]) -> dict[str, Any]:
    """薄包装 myssia.secrets.delete_secret:误存凭据的 UI 清除口(C5)。

    凭据只有名字无值,无回显问题;重复删除第二次 ``secret_not_found``
    (幂等性归调用方,与 CLI 同门)。
    """
    name = params.get("name")
    if not isinstance(name, str) or not name:
        raise ProtocolError("invalid_params", "缺少凭据名 name(myia/<scope>/<name>)", path="params.name")
    try:
        delete_secret(name)
    except SecretError as exc:
        raise ProtocolError(exc.code, str(exc), path="params.name") from exc
    return {"name": name, "deleted": True}


# ---------------------------------------------------------------------------
# 方法:feed.export(情报流导出;G3,10-03-feed-ux)
# ---------------------------------------------------------------------------


def _m_feed_export(params: dict[str, Any]) -> dict[str, Any]:
    """导出情报流当前过滤视图为 JSONL / CSV(sidecar 直写,数据不经 webview)。

    查询面 = ``store.items`` 同源(:func:`SQLiteStore.list_items` 的
    ``category``/``query``,不带游标 —— 导出的是整个过滤视图而非单页);
    ``path`` = 前端 ``dialog.save()`` 用户选定(绝对路径,父目录必须已存在,
    覆盖确认归对话框侧)。只写这一个文件:不建目录、不删除任何东西;
    逐行流式写,大结果集不整载内存(design §1)。

    err:``export_path_invalid``(空/相对路径/父目录不存在)/
    ``export_write_failed``(IO 原文)。
    """
    import csv

    fmt = params.get("format")
    if fmt not in ("jsonl", "csv"):
        raise ProtocolError(
            "invalid_params", "format 必须是 jsonl 或 csv", path="params.format"
        )
    path_raw = params.get("path")
    if not isinstance(path_raw, str) or not path_raw.strip():
        raise ProtocolError("export_path_invalid", "缺少导出路径 path", path="params.path")
    target = Path(path_raw).expanduser()
    if not target.is_absolute():
        raise ProtocolError(
            "export_path_invalid", f"导出路径必须是绝对路径: {path_raw}", path="params.path"
        )
    parent = target.parent
    if not parent.is_dir():
        raise ProtocolError(
            "export_path_invalid", f"导出父目录不存在: {parent}", path="params.path"
        )
    category = params.get("category")
    if category is not None and (not isinstance(category, str) or not category):
        raise ProtocolError("invalid_params", "category 必须为非空字符串", path="params.category")
    query = params.get("query")
    if query is not None and not isinstance(query, str):
        raise ProtocolError("invalid_params", "query 必须为字符串", path="params.query")
    # 源大类作用域(10-08-tg-channel-card v2):与 store.items 同词表同门。
    source_kind = params.get("source_kind")
    if source_kind is not None and source_kind not in ("web", "im"):
        raise ProtocolError(
            "invalid_params", "source_kind 只接受 web/im(不过滤请省略)", path="params.source_kind"
        )

    db = params.get("db") or _serve_context().db
    try:
        store = SQLiteStore(db)
    except StoreSchemaError as exc:
        raise ProtocolError(exc.code, str(exc), path="params.db", data=exc.details) from exc
    try:
        items = store.list_items(category=category, source_kind=source_kind, query=query or None)
    except ValueError as exc:
        raise ProtocolError("invalid_params", str(exc), path="params") from exc
    finally:
        store.close()

    csv_columns = ("id", "first_seen", "category", "source", "title", "url", "content")
    written = 0
    try:
        with open(target, "w", encoding="utf-8", newline="") as handle:
            if fmt == "jsonl":
                for item in items:
                    handle.write(json.dumps(_item_dict(item), ensure_ascii=False) + "\n")
                    written += 1
            else:
                writer = csv.writer(handle)
                writer.writerow(csv_columns)  # 表头计入文件,不计入 count(条目数)
                for item in items:
                    row = _item_dict(item)
                    writer.writerow([row.get(column) for column in csv_columns])
                    written += 1
    except OSError as exc:
        raise ProtocolError(
            "export_write_failed", f"导出写盘失败: {target} ({exc})", path="params.path"
        ) from exc
    size = target.stat().st_size
    return {"path": str(target), "count": written, "bytes": size}


# ---------------------------------------------------------------------------
# 方法:feed.enrich(单条情报卡 AI 摘要/精评;G8,10-03-fe-small-batch)
# ---------------------------------------------------------------------------


class _EnrichItemAdapter:
    """ItemRecord → :meth:`LLMEnricher.enrich` 的鸭子类型单条形态。

    enrich() 对 items 的契约是 duck-typed(url/title/metadata/scores/
    add_tags/dedup_key,可选 content 属性;tests/enrich/test_enrich.py FakeItem
    同款先例),不引 pipeline.Item 重构造。``scores`` 恒起于 None:本次调用
    的产出才有意义,行内既有旧分不冒充本轮结果(未获分 = ``enrich_failed``
    结构化上报,不静默回落)。``metadata`` 种自 ``ItemRecord.raw``
    (pipeline 以 raw=item.metadata 入库,image_ocr/image_caption 等图析
    产物由此随单条再进 prompt,与管线条目同形)。
    """

    def __init__(self, record: Any) -> None:
        self.url = record.url
        self.title = record.title
        self.dedup_key = record.dedup_key
        self.content = record.content
        self.scores: dict[str, Any] | None = None
        self.metadata: dict[str, Any] = (
            dict(record.raw) if isinstance(record.raw, Mapping) else {}
        )
        self.tags: list[str] = list(record.tags or [])

    def add_tags(self, tags: list[str]) -> None:
        """mute 命中路径专用;就地内存去重合入,不回写 items 表。"""
        self.tags = list(dict.fromkeys([*self.tags, *tags]))


def _category_config_for_item(category: Any, plugins_dir: str) -> Any:
    """条目所属品类的已装配置(plugins 目录扫描,品类 id 精确匹配)。

    确定性同 :func:`_collect_category_ids`:同 id 多文件取字典序首个;
    坏文件(LoadError)不参与 id 空间 —— 装不起来的 YAML 供不了端点配置,
    如实按未配置处理(调用方报 ``enrich_not_configured``)。
    """
    if not isinstance(category, str) or not category:
        return None
    for path in _yaml_files(Path(plugins_dir)):
        try:
            config = load_category_file(path)
        except LoadError:
            continue
        if config.id == category:
            return config
    return None


def _m_feed_enrich(params: dict[str, Any]) -> dict[str, Any]:
    """情报流卡单条「AI 摘要」:骑 enrich 管线现跑 LLMEnricher(G8)。

    ``item`` 解析口径同 ``feedback.mark``(:func:`resolve_item_ref`:
    items.id(int/纯数字串)或 dedup_key/URL(str));端点配置 = 条目所属
    品类 YAML ``enrich:`` 节(schema ``EnrichConfig``),``base_url`` /
    ``api_key`` 沿 ``env:``/``keychain:`` 引用链在 :class:`EnrichSettings`
    / :class:`LLMEnricher` 构造期解析(无内置端点、无默认 key,grill Q6,
    与 ``myssia run`` 同门);enrich_cache 缓存语义复用((url, model,
    scores_key) 命中零 token),分数经 :meth:`LLMEnricher.enrich` 原路
    回填 items 表 + 缓存表。async :meth:`~myssia.enrich.LLMEnricher.enrich`
    在 handler 内 ``asyncio.run`` 同步应答,整段挂
    ``EnrichSettings.timeout_seconds`` 超时帽(单条单批,内层还有同值
    的 per-completion wait_for,外层兜缓存读写/渲染的全程)。

    err:``enrich_not_configured``(graceful 明示无配置:品类未启用
    enrich / 端点引用缺失 / 品类 YAML 不在 plugins 目录,``data.reason``
    三分 ``enrich_disabled`` / ``endpoint_missing`` /
    ``category_yaml_not_found``)/ ``enrich_timeout`` / ``enrich_failed``
    (预算耗尽或批次失败条目未获分,degrade_reason + failures 入 data);
    :class:`EnrichConfigError` 的 code 原文透传(``credential_unresolved``
    / ``invalid_base_url`` 等,追源头去 ``src/myssia/enrich/``)。
    """
    item_ref = params.get("item")
    if isinstance(item_ref, bool) or item_ref is None or item_ref == "":
        raise ProtocolError("invalid_params", "缺少条目引用 item(items.id 或 dedup_key/URL)", path="params.item")
    ctx = _serve_context()
    db = params.get("db") or ctx.db
    try:
        store = SQLiteStore(db)
    except StoreSchemaError as exc:
        raise ProtocolError(exc.code, str(exc), path="params.db", data=exc.details) from exc
    try:
        item = resolve_item_ref(store, item_ref)
        if item is None:
            raise ProtocolError(
                "item_not_found",
                f"条目不存在: {item_ref!r}(可传 items.id 或 dedup_key/URL)",
                path="params.item",
            )
        config = _category_config_for_item(item.category, ctx.plugins_dir)
        enrich_cfg = config.enrich if config is not None else None
        if enrich_cfg is None or not enrich_cfg.enabled:
            if config is None:
                reason = "category_yaml_not_found"
                detail = f"条目所属品类 {item.category!r} 的 YAML 不在 plugins 目录"
            else:
                reason = "enrich_disabled"
                detail = f"品类 {item.category!r} 未启用 enrich(enabled=false)"
            raise ProtocolError(
                "enrich_not_configured",
                f"无法精评:{detail};请在品类 YAML enrich 节配置并启用端点",
                path="params.item",
                data={"category": item.category, "reason": reason},
            )
        if enrich_cfg.base_url is None or enrich_cfg.api_key is None:
            raise ProtocolError(
                "enrich_not_configured",
                f"品类 {item.category!r} 的 enrich 节缺少端点引用"
                "(base_url/api_key 必须是 env:/keychain: 引用)",
                path="params.item",
                data={"category": item.category, "reason": "endpoint_missing"},
            )
        try:
            settings = EnrichSettings(
                base_url_ref=enrich_cfg.base_url, api_key_ref=enrich_cfg.api_key
            )
            enricher = LLMEnricher(enrich_cfg, settings)
        except EnrichConfigError as exc:
            raise ProtocolError(
                exc.code, str(exc), path="params.item",
                data={**exc.details, "category": item.category},
            ) from exc
        adapter = _EnrichItemAdapter(item)
        try:
            outcome = asyncio.run(
                asyncio.wait_for(
                    enricher.enrich([adapter], watchlist=config.watchlist, store=store),
                    timeout=settings.timeout_seconds,
                )
            )
        except asyncio.TimeoutError as exc:
            raise ProtocolError(
                "enrich_timeout",
                f"精评超时(>{settings.timeout_seconds}s):端点无响应",
                path="params.item",
                data={"timeout_seconds": settings.timeout_seconds},
            ) from exc
        if adapter.scores is None or "score" not in adapter.metadata:
            first_failure = outcome.failures[0]["message"] if outcome.failures else "端点未返回该条目评分"
            raise ProtocolError(
                "enrich_failed",
                f"精评未获分(degrade_reason={outcome.degrade_reason!r}):{first_failure}",
                path="params.item",
                data={
                    "degrade_reason": outcome.degrade_reason,
                    "failures": outcome.failures,
                },
            )
        return {
            "item_id": item.id,
            "model": enrich_cfg.model,
            "scores": adapter.scores,
            "score": adapter.metadata["score"],
            "cached": outcome.cached >= 1,
        }
    finally:
        store.close()


# ---------------------------------------------------------------------------
# 方法:sources.write(源启停写回;往返一致 = doctor 复核同名单集合)
# ---------------------------------------------------------------------------


def _stash_path(yaml_path: Path) -> Path:
    """停用源暂存文件:同目录 ``<yaml>.disabled.json``。

    存储形态属 Python 侧自由度(契约只钉名字集合往返):schema 顶层是
    extra=forbid 的 12 节公开契约(SKILL.md 逐字段锁定),停用源不进 YAML
    文档,lossless 暂存在旁边的 JSON 里,随 YAML 目录一起移动。
    """
    return yaml_path.parent / (yaml_path.name + ".disabled.json")


def _load_disabled_stash(yaml_path: Path) -> list[dict[str, Any]]:
    stash_file = _stash_path(yaml_path)
    if not stash_file.exists():
        return []
    try:
        data = json.loads(stash_file.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ProtocolError(
            "stash_unreadable",
            f"停用源暂存文件不可读: {stash_file} ({exc})",
            path="params.file",
        ) from exc
    if not isinstance(data, list) or not all(isinstance(item, dict) for item in data):
        raise ProtocolError(
            "stash_unreadable",
            f"停用源暂存文件损坏(应为对象列表): {stash_file}",
            path="params.file",
        )
    return data


def _source_names(entries: list[Any], *, where: str) -> list[str]:
    """按序取源名;缺 name / 重名都结构化拒绝(写回不可落在含糊名单上)。"""
    names: list[str] = []
    for index, entry in enumerate(entries):
        name = entry.get("name") if isinstance(entry, dict) else None
        if not isinstance(name, str) or not name:
            raise ProtocolError(
                "invalid_params",
                f"{where}[{index}] 缺少有效 name 字段,无法定位写回目标",
                path="params.file",
            )
        names.append(name)
    duplicates = sorted({name for name in names if names.count(name) > 1})
    if duplicates:
        raise ProtocolError(
            "duplicate_source", f"{where} 存在重名源: {duplicates}", path="params.file"
        )
    return names


def _atomic_write_text(path: Path, text: str) -> None:
    """同目录临时文件 + ``os.replace`` 原子落盘(读者侧零半写状态)。

    ``newline=""`` 关闭换行翻译:yaml.save 写回的用户原文逐字节保真
    (CRLF 不被翻译成 ``os.linesep``,Windows 上尤其;task 10-03-yaml-editor
    design §2 写侧保真)。sources.write 的文本手术(10-03-yaml-toggle-comments)
    走同一路径,其内容是手术后的用户原文逐行拼接 —— ``newline=""`` 从「无
    副作用」升级为「字节保真的半条命」,统一一条写入路径,不留两套语义。
    """
    tmp = path.with_name(path.name + ".tmp")
    with open(tmp, "w", encoding="utf-8", newline="") as handle:
        handle.write(text)
    os.replace(tmp, path)


# ---------------------------------------------------------------------------
# sources.write 文本手术(10-03-yaml-toggle-comments 根治)
# ---------------------------------------------------------------------------
# 设计:写回不再 ``yaml.safe_dump`` 整份重写(那会抹掉全文件注释),而是在
# 原文上按行搬运 ``sources:`` 条目 —— 移出的条目连同其前导空行与上方锚点
# 注释整段摘除(逐字节存进暂存),移回时原样插回。其余行(节间注释、行内
# 注释、引号与顺序风格、parked 注释占位)一律不动。手术不支持的形态(锚点/
# 别名引用、流式 sources、条目行无法与解析结果对齐)一律结构化拒写,绝不
# 静默回退 safe_dump 抹注释。

#: 暂存条目的保留键:值 = ``{"raw_block": 逐字节原文, "pred": 前一条目名|None}``。
#: 源条目自身字段原样平铺在外层(既有断言直读 ``stash[i]["name"]/["url"]``),
#: 保留键单独嵌套且命名空间化,避开 ``SourceConfig`` extra=allow 的用户扩展
#: 字段;真撞名时在落暂存前结构化拒写,不做静默覆盖。
_TOGGLE_META_KEY = "_myssia_toggle"

#: 整行注释行(缩进任意);锚点注释归属判定用。
_TOGGLE_LINE_COMMENT_RE = re.compile(r"^\s*#")

#: 条目短横线行:空格缩进 + ``- ``(裸 ``-`` 行也认);tab 缩进的 YAML 本就不合法。
_TOGGLE_ENTRY_DASH_RE = re.compile(r"^( +)-(?: +|$)")

#: 旧版暂存条目(无位置元数据)的移入定位哨兵:追加到 sources 块尾。
_TOGGLE_APPEND_AT_END = object()


def _split_keep_lines(text: str) -> list[str]:
    """按 ``\n`` 切行且逐字节无损:``"".join(result)`` 还原原文。

    行尾 ``\r`` 留在行内(CRLF 文件的每行仍是 ``…\r\n``,搬运时整行原样
    走);EOF 无结尾换行的末行原样保留(不加换行)。
    """
    parts = text.split("\n")
    lines = [part + "\n" for part in parts[:-1]]
    if parts[-1] != "":
        lines.append(parts[-1])
    return lines


def _toggle_sources_header(lines: list[str]) -> tuple[int, int]:
    """定位顶层空值 ``sources:`` 键行与块尾,返回 (键行下标, 块尾下标)(排他)。

    块尾 = 键行之后第一个「列 0 的非注释非空行」(下一个顶层节点)或 EOF;
    列 0 注释不结束块(parked 注释占位可以贴着下一节)。找不到键行(流式
    ``sources: []``、键带锚点等)= 手术不支持的形态。
    """
    raise_unsupported = lambda why: ProtocolError(  # noqa: E731 — 单点小闭包
        "source_write_unsupported",
        f"品类 YAML 存在文本手术不支持的结构({why});拒绝写回,原文零改动",
        path="params.file",
    )
    src_idx = None
    for i, line in enumerate(lines):
        body = line.rstrip("\r\n")
        if re.match(r"sources:\s*(#.*)?$", body):
            src_idx = i
            break
    if src_idx is None:
        raise raise_unsupported("找不到顶层空值 sources: 键行,疑为流式/内嵌形态")
    end = len(lines)
    for i in range(src_idx + 1, len(lines)):
        body = lines[i].rstrip("\r\n")
        if body and not body[0].isspace() and not body.startswith("#"):
            end = i
            break
    return src_idx, end


def _toggle_entry_dashes(lines: list[str], src_idx: int, block_end: int) -> tuple[list[int], int]:
    """块内条目短横线行(与首个条目同缩进;更深缩进 = 条目内嵌列表,不算)。

    返回 (短横线行下标列表, 条目缩进)。块序列的兄弟条目必须同缩进,更深
    的短横线只会是条目内部的嵌套序列(如 ``headers`` 下的列表值),不参与
    条目计数 —— 条目数与解析结果对不齐由调用方拒写。
    """
    dashes: list[int] = []
    indent: int | None = None
    for i in range(src_idx + 1, block_end):
        matched = _TOGGLE_ENTRY_DASH_RE.match(lines[i])
        if matched is None:
            continue
        if indent is None:
            indent = len(matched.group(1))
        if len(matched.group(1)) == indent:
            dashes.append(i)
    return dashes, (indent if indent is not None else 2)


def _toggle_chunk_spans(
    lines: list[str], src_idx: int, block_end: int, dashes: list[int]
) -> list[tuple[int, int]]:
    """每个条目的搬运区间 ``[前导空行起, 正文止)``(排他下标,与条目同序)。

    区间 = 前导空行 + 锚点注释 + 正文:锚点注释 = 紧贴条目首行上方的连续
    整行注释(上一条目正文或 ``sources:`` 行截断);前导空行 = 锚点上方的
    连续空行 —— 条目间分隔空行归属**后一条目**,这样「插回前驱区间之后」
    恰好逐字节还原原文布局;正文 = 自短横线行起连续的非空行,条目尾部的
    说明注释(如 wool.yaml 的 ``# No pagination…``)直接续在正文后,同属
    条目。条目尾随空行不归属(它要么是下一条目的前导,要么是块尾留白)。
    末条目的正文另设一道上界:紧贴正文(无空行)的**列 0** 整行注释,对其
    后的下一内容行做缩进前瞻 —— 仍有条目缩进续行(retry/headers 等)则注释
    嵌在本条目正文中段,随条目整段搬运(否则条目自身字段被截留在主文件,
    停用中间态解析时静默并入前一启用源);无续行(下一内容行顶格/空白/到
    块界)才是给下一顶层节写的分节注释,留在主文件(评审遗留 low:曾随末
    条目停用整体离开主文件,中间态一节注释不可见)。非末条目到不了这里
    (上界是后继条目的锚点起点,列 0 注释紧贴其上时本就随其搬运)。
    """
    anchors: list[int] = []
    for dash in dashes:
        j = dash - 1
        while j > src_idx and _TOGGLE_LINE_COMMENT_RE.match(lines[j]):
            j -= 1
        while j > src_idx and _toggle_is_blank(lines[j]):
            j -= 1
        anchors.append(j + 1)
    spans: list[tuple[int, int]] = []
    for k, dash in enumerate(dashes):
        last = k + 1 == len(dashes)
        limit = block_end if last else anchors[k + 1]
        stop = dash
        while stop < limit and not _toggle_is_blank(lines[stop]):
            if (
                last
                and _toggle_is_col0_comment(lines[stop])
                and not _toggle_col0_comment_has_continuation(lines, stop, limit)
            ):
                break  # 分节注释留在主文件,不入搬运块
            stop += 1
        spans.append((anchors[k], stop))
    return spans


def _toggle_is_blank(line: str) -> bool:
    """空白行(仅空白/仅换行);空行是条目分隔,不随任何条目搬运。"""
    return line.strip("\r\n").strip() == ""


def _toggle_is_col0_comment(line: str) -> bool:
    """列 0 起始的整行注释(先剥 ``\r\n``,CRLF 同判)。

    条目自身的尾说明注释有缩进(如 wool.yaml 的 ``# No pagination…``),
    不命中本判定。列 0 字形不必然等于分节注释:也可能嵌在条目正文中段
    (其后仍有本条目的缩进续行),归属由 ``_toggle_col0_comment_has_continuation``
    的缩进前瞻判定,本函数只认字形。
    """
    return line.rstrip("\r\n").startswith("#")


def _toggle_col0_comment_has_continuation(
    lines: list[str], comment_idx: int, limit: int
) -> bool:
    """列 0 注释(连同其后连续列 0 注释)之后是否仍有条目缩进续行。

    有 → 注释嵌在条目正文中段(YAML 注释透明,其后缩进字段仍属本条目),
    整段必须随条目搬运;无(下一内容行顶格 = 下一顶层节、空白分隔、或已到
    块界/EOF)→ 注释才是写给下一顶层节的分节注释,留在主文件。
    """
    j = comment_idx
    while j < limit and _toggle_is_col0_comment(lines[j]):
        j += 1
    if j >= limit or _toggle_is_blank(lines[j]):
        return False
    return lines[j][:1] in (" ", "\t")


def _toggle_alias_nodes(text: str) -> bool:
    """文档是否存在被引用两次的节点(YAML 别名/合并键 ``<<``)。

    用合成树的对象同一性判别:别名 = 同一节点对象出现两次。只定义未引用
    的锚点不拦(定义行随条目搬运仍自洽);有引用必拒 —— 行级搬运可能把
    定义挪到引用之后(前向引用直接拒载),不做这种隐晦破坏。
    """
    try:
        root = yaml.compose(text, Loader=yaml.SafeLoader)
    except yaml.YAMLError:
        return False  # 语法错走上游 category_invalid,不在这里报
    seen: set[int] = set()
    stack = [root]
    while stack:
        node = stack.pop()
        if node is None or not isinstance(node, yaml.SequenceNode | yaml.MappingNode | yaml.ScalarNode):
            continue
        if id(node) in seen:
            return True
        seen.add(id(node))
        if isinstance(node, yaml.MappingNode):
            stack.extend(key for key, _ in node.value)
            stack.extend(value for _, value in node.value)
        elif isinstance(node, yaml.SequenceNode):
            stack.extend(node.value)
    return False


def _toggle_fallback_block(source: dict[str, Any], indent: int) -> str:
    """旧版暂存条目(无 ``raw_block`` 元数据)移入时的兜底:由 dict 重序列化。

    数据无损、注释不还原(旧暂存本就没存原文);只服务 sidecar 升级窗口,
    常规路径一律走 ``raw_block`` 逐字节还原。序列化前剥离 ``_myssia_toggle``
    内部键(raw_block 缺失/非字符串的损坏暂存仍会带它走进这里):内部键
    写进主 YAML 后,该源再停用会撞保留键拒写(评审遗留 low:启停变砖)。
    """
    dumped = yaml.safe_dump(
        {k: v for k, v in source.items() if k != _TOGGLE_META_KEY},
        allow_unicode=True,
        sort_keys=False,
        default_flow_style=False,
    )
    body = dumped.splitlines()
    if not body:
        raise ProtocolError(
            "source_write_unsupported", "暂存条目为空,无法重构源块", path="params.file"
        )
    pad = " " * indent
    return "".join([f"{pad}- {body[0]}\n"] + [f"{pad}  {line}\n" for line in body[1:]])


def _sources_surgical_rewrite(
    original: str,
    source_names: list[str],
    disable: list[str],
    enable_back: list[dict[str, Any]],
) -> tuple[str, dict[str, dict[str, Any]]]:
    """在品类 YAML 原文上按行搬运 ``sources:`` 条目,返回 (新文本, 搬运元数据)。

    Args:
        original: 文件原始字节文本(经 ``newline=""`` 读入,CRLF 原样)。
        source_names: 解析态 ``sources`` 名单(与文本条目行按序一一对齐,
            对不齐 = 手术不支持的形态,拒写)。
        disable: 本次移出的源名(都已过未知/末源校验)。
        enable_back: 本次移回的暂存条目(带 ``_myssia_toggle`` 元数据;旧暂存
            无元数据走重序列化兜底),按移入顺序排列。

    Returns:
        (手术后全文, ``{源名: {"raw_block", "pred", "gap_before"}}``)——
        元数据供调用方塞进 ``.disabled.json`` 条目,供后续 enable 逐字节
        还原。

    移入定位:优先插回原位(暂存记录的 ``pred`` 前驱仍在文本中 → 插在其
    区间之后;``gap_before`` 记录的「前驱区间与被移条目原位之间的无主注释
    块」仍原样紧贴前驱区间 → 插在该块之后 —— 两活条目间空行分隔的 parked
    占位因此不被跳过;块首前驱为空 → 插在 ``sources:`` 行之后),前驱不在
    (也被停用)→ 追加到块尾;旧版暂存条目无位置元数据,一律追加块尾。
    gap 失配(停用后文件又被外部改过)→ 退回前驱区间之后(有 ``.bak`` 与
    两道门兜底,不做更激进的猜测)。每次移入后重扫文本,先前移回的条目可作
    后续条目的前驱,多次移回仍还原原始相对顺序。
    移回名已在文本中(崩溃窗口下主文件与暂存双份残留)→ 跳过移入、以文件
    为准,本次只完成暂存侧清理 —— 残留自愈不制造同名双条目。
    """
    lines = _split_keep_lines(original)
    src_idx, block_end = _toggle_sources_header(lines)
    dashes, entry_indent = _toggle_entry_dashes(lines, src_idx, block_end)
    if len(dashes) != len(source_names):
        raise ProtocolError(
            "source_write_unsupported",
            f"sources 条目行({len(dashes)} 个)与解析结果({len(source_names)} 个)"
            "无法对齐,疑为注释掉的条目/异常缩进之外的结构;拒绝写回,原文零改动",
            path="params.file",
        )
    spans = _toggle_chunk_spans(lines, src_idx, block_end, dashes)
    index_of = {name: k for k, name in enumerate(source_names)}

    # -- 移出:整段摘除,逐字节记入元数据(条目自身 + 上方锚点注释随行)
    moved: dict[str, dict[str, Any]] = {}
    for name in disable:
        k = index_of[name]
        start, stop = spans[k]
        prev_stop = spans[k - 1][1] if k > 0 else src_idx + 1
        moved[name] = {
            "raw_block": "".join(lines[start:stop]),
            "pred": source_names[k - 1] if k > 0 else None,
            # 前驱区间与被移条目区间之间的行(整行注释/空行,不归属任何
            # 条目):不记下它,enable 插回「前驱区间之后」就会跳过它 ——
            # 夹在两活条目间的 parked 占位被搬位、多段锚点注释被撕裂。
            "gap_before": "".join(lines[prev_stop:start]),
        }
    for k in sorted((index_of[name] for name in disable), reverse=True):
        start, stop = spans[k]
        del lines[start:stop]

    # -- 移入:在当前文本上逐条定位插回(每次重扫,先前移回的可作前驱)
    text_names = [name for name in source_names if name not in set(disable)]
    for entry in enable_back:
        name = entry["name"]
        if name in text_names:
            continue  # 双份残留自愈:文件已有同名源,以文件为准,只清暂存侧
        meta = entry.get(_TOGGLE_META_KEY) or {}
        raw = meta.get("raw_block")
        if isinstance(raw, str) and raw:
            pred: Any = meta.get("pred")  # None = 原位就是块首
        else:
            # 旧版暂存无位置元数据:追加块尾(区别于「元数据说自己在块首」)
            raw = _toggle_fallback_block(entry, entry_indent)
            pred = _TOGGLE_APPEND_AT_END
        src_idx, block_end = _toggle_sources_header(lines)
        dashes, _ = _toggle_entry_dashes(lines, src_idx, block_end)
        if len(dashes) != len(text_names):
            raise ProtocolError(
                "source_write_unsupported",
                f"移入 {name} 时条目行与名单对不齐;拒绝写回,原文零改动",
                path="params.file",
            )
        spans = _toggle_chunk_spans(lines, src_idx, block_end, dashes)
        if pred is _TOGGLE_APPEND_AT_END:
            at = spans[-1][1] if spans else src_idx + 1
            pos = len(text_names)
        elif pred is None:
            at, pos = src_idx + 1, 0  # 原位就是块首
        elif pred in text_names:
            q = text_names.index(pred)
            at, pos = spans[q][1], q + 1  # 兜底锚:前驱区间之后
            gap = meta.get("gap_before")  # 前驱与原位之间的无主注释块(逐字节)
            if isinstance(gap, str) and gap:
                gap_lines = _split_keep_lines(gap)
                seam = spans[q][1] + len(gap_lines)
                if lines[spans[q][1] : seam] == gap_lines:
                    at = seam  # 块仍原样紧贴前驱区间:插在其后 = 恰好原位
        else:
            at = spans[-1][1] if spans else src_idx + 1  # 前驱不在文本,追加块尾
            pos = len(text_names)
        inserted = _split_keep_lines(raw)
        if at < len(lines) and not inserted[-1].endswith("\n"):
            inserted[-1] += "\n"  # 块来自 EOF 无换行形态,插进中部时补行尾
        if at == len(lines) and lines and not lines[-1].endswith("\n"):
            lines[-1] += "\n"  # 接在无结尾换行的末行之后:先给前行补换行
        lines[at:at] = inserted
        text_names.insert(pos, name)
    return "".join(lines), moved


def _m_sources_write(params: dict[str, Any]) -> dict[str, Any]:
    """源启停写回品类 YAML(协议扩展 `sources.write` 收编,PRD 往返一致)。

    契约(ui-src/screens/sources/api.ts 模块头):``disable`` 把源从
    ``sources:`` 摘出(lossless 暂存到同目录 ``<yaml>.disabled.json``),
    ``enable`` 移回。写回是**文本手术**(10-03-yaml-toggle-comments 根治,
    取代旧 ``yaml.safe_dump`` 整份重写):在原文上按行搬运 ``sources:``
    条目,被搬条目自身及其上方锚点注释随行,其余行逐字节不动 —— 注释/
    顺序/引号风格天然保真,``plugin:`` 等 sidecar 节更是碰都不碰。手术不
    支持的形态(锚点/别名引用、流式 ``sources``、条目行与解析结果对不齐)
    = 结构化 ``source_write_unsupported`` 拒写,绝不静默回退 ``safe_dump``
    抹注释。移出条目的逐字节原文随暂存条目(``_myssia_toggle.raw_block``)进
    ``.disabled.json``,enable 时插回原位(前驱在 → 前驱之后;否则块首/
    块尾),停用→启用往返逐字节一致。落盘前两道门:手术结果反解析与预期
    文档深等(防线内错搬),再过 myia 自家装载器(:func:`load_category`,
    与 ``myssia run`` 同一道门)—— 失败即原样零写入。拒绝停用最后一个启用源
    (schema ``sources`` min_length=1,停满即拒载)。
    """
    yaml_raw = params.get("file")
    if not isinstance(yaml_raw, str) or not yaml_raw:
        raise ProtocolError("invalid_params", "缺少品类 YAML 路径 file", path="params.file")
    enable = params.get("enable")
    disable = params.get("disable")
    for label, value in (("enable", enable), ("disable", disable)):
        if value is None:
            continue
        if not isinstance(value, list) or not all(isinstance(item, str) and item for item in value):
            raise ProtocolError(
                "invalid_params", f"{label} 必须为非空字符串数组", path=f"params.{label}"
            )
    enable = list(enable or [])
    disable = list(disable or [])
    if not enable and not disable:
        raise ProtocolError("invalid_params", "enable/disable 至少提供其一", path="params")

    yaml_path = Path(yaml_raw)
    try:
        # newline="" 原样读(CRLF 不翻译):文本手术逐字节搬运的前提 ——
        # 读进什么搬什么,落盘(:func:`_atomic_write_text`,同样 newline="")
        # 才能逐字节保真,官方 YAML 往返 diff 为空。
        with open(yaml_path, encoding="utf-8", newline="") as handle:
            original = handle.read()
    except OSError as exc:
        raise ProtocolError(
            "source_file_unreadable", f"品类 YAML 不可读: {yaml_path} ({exc})", path="params.file"
        ) from exc
    try:
        doc = yaml.safe_load(original)
    except yaml.YAMLError as exc:
        raise ProtocolError(
            "category_invalid", f"品类 YAML 不是合法 YAML: {exc}", path="params.file"
        ) from exc
    if not isinstance(doc, dict) or not isinstance(doc.get("sources"), list):
        raise ProtocolError(
            "category_invalid", f"{yaml_path} 不是品类 YAML(缺少 sources 节)", path="params.file"
        )

    sources = list(doc["sources"])
    stash = _load_disabled_stash(yaml_path)
    enabled_names = _source_names(sources, where="sources")
    disabled_names = _source_names(stash, where="disabled_stash")

    unknown = [name for name in disable if name not in enabled_names]
    unknown += [name for name in enable if name not in disabled_names]
    if unknown:
        raise ProtocolError(
            "source_unknown",
            f"名单不在可写范围: {sorted(set(unknown))}"
            f"(现启用={enabled_names},现停用={disabled_names})",
            path="params",
            data={"enabled": enabled_names, "disabled": disabled_names},
        )
    if not [name for name in enabled_names if name not in set(disable)]:
        raise ProtocolError(
            "last_source",
            "拒绝停用最后一个启用源(品类必须保留至少一个源)",
            path="params.disable",
        )

    # 暂存侧名单(dict 保序 + 同名后到覆盖:崩溃窗口下的双份残留自愈);
    # 移回条目保留原始形态(含 _myssia_toggle 元数据)给文本手术取原文,
    # 应答/装载名单由手术后文本的反解析给出(见门一)。
    rest_stash = {
        name: source for name, source in zip(disabled_names, stash) if name not in set(enable)
    }
    out_stash = {
        name: source for name, source in zip(enabled_names, sources) if name in set(disable)
    }
    new_stash = list({**rest_stash, **out_stash}.values())
    back_raw = [source for name, source in zip(disabled_names, stash) if name in set(enable)]

    # -- 文本手术:原文按行搬运 sources 条目,失败/不支持都零写入 ----------
    # (多文档 ``---`` 文件在上方 safe_load 就抛 ComposerError → 既有
    #   category_invalid 拒载,零写入 —— 无需手术侧重复设卡。)
    if _toggle_alias_nodes(original):
        raise ProtocolError(
            "source_write_unsupported",
            f"品类 YAML 存在锚点/别名引用,文本手术不做行级搬运(零写入): {yaml_path}",
            path="params.file",
        )
    new_text, moved = _sources_surgical_rewrite(original, enabled_names, disable, back_raw)
    for name, meta in moved.items():
        out = out_stash[name]
        if _TOGGLE_META_KEY in out:
            raise ProtocolError(
                "source_write_unsupported",
                f"源 {name} 已含手术保留键 {_TOGGLE_META_KEY},拒绝静默覆盖: {yaml_path}",
                path="params.file",
            )
        out[_TOGGLE_META_KEY] = meta
    # 门一:手术后的文本反解析必须与「原文档 + 反解析源名单」深等 —— sources
    # 名单与顺序以手术后文本为准(移回源按前驱插回原位,应答 enabled 顺序 =
    # 文件实际顺序;api.ts 契约只钉名字集合往返,顺序不钉),其余任何键被手术
    # 波及都会在这里现形(零写入)。
    try:
        reread = yaml.safe_load(new_text)
    except yaml.YAMLError as exc:  # 手术产物连 YAML 都不是(如悬空别名)= 拒写
        raise ProtocolError(
            "source_write_unsupported",
            f"文本手术结果不再是合法 YAML(零写入): {yaml_path} ({exc})",
            path="params.file",
        ) from exc
    if not isinstance(reread, dict) or not isinstance(reread.get("sources"), list):
        raise ProtocolError(
            "source_write_unsupported",
            f"文本手术结果不是品类文档(零写入): {yaml_path}",
            path="params.file",
        )
    doc["sources"] = reread["sources"]
    new_sources = reread["sources"]
    if reread != doc:
        raise ProtocolError(
            "source_write_unsupported",
            f"文本手术波及了 sources 之外的内容(疑为未支持结构的漏网形态,零写入): {yaml_path}",
            path="params.file",
        )

    try:  # 门二:往返一致门,与 myssia run 同一装载器,失败零写入
        load_category(doc, source=str(yaml_path))
    except LoadError as exc:
        details = [
            {"path": item.path, "code": item.error_type, "message": item.message}
            for item in exc.errors
        ]
        raise ProtocolError(
            "category_invalid",
            f"写回后的源名单未过品类校验: {details}",
            path="params.file",
            data={"errors": details},
        ) from exc

    stash_file = _stash_path(yaml_path)
    try:
        # 覆盖前先把原文留底 <yaml>.bak(单份滚动,10-03-yaml-editor 决议 2
        # 的止血保留):手术已保注释,这里是第二道保险 —— 手术自身出 bug 时
        # 用户仍有操作前原文可回滚。
        shutil.copy2(yaml_path, yaml_path.with_suffix(yaml_path.suffix + ".bak"))
        # 先暂存后主文件:中途崩溃的最坏情形是「源同时在两处」(无损、可自愈),
        # 反过来则可能只存在于被覆盖的主文件里。
        if new_stash:
            _atomic_write_text(
                stash_file, json.dumps(new_stash, ensure_ascii=False, indent=2) + "\n"
            )
        elif stash_file.exists():
            stash_file.unlink()
        _atomic_write_text(yaml_path, new_text)
    except OSError as exc:
        raise ProtocolError(
            "source_write_failed", f"写回失败: {exc}", path="params.file"
        ) from exc
    return {
        "file": str(yaml_path),
        "written": True,
        "enabled": [str(source["name"]) for source in new_sources],
        "disabled": [str(source["name"]) for source in new_stash],
    }


# ---------------------------------------------------------------------------
# 方法:yaml.list / read / validate / template / save / delete
# (配置编辑器协议,task 10-03-yaml-editor;契约钉死于任务档 design.md §1,
#  TS 侧 ui-src/screens/yaml-editor/api.ts 注释互指)
# ---------------------------------------------------------------------------

#: 单个品类 YAML 的读写上限(字节):品类 YAML 百行量级,防误开/误写无关大文件。
#: 读堵不写堵等于没堵,yaml.read 与 yaml.save 共用同一常量(design §1)。
YAML_MAX_BYTES = 1024 * 1024

#: 最小合法品类模板(yaml.template 应答原文;UI 只回填 id/name)。
#: 协议侧维护 = schema 的家乡在此,模板随 schema 同仓演进,pytest 锁
#: ``load_category(safe_load(template))`` 必过 —— schema 演进时模板不会静默腐烂。
#: 完整 12 节权威示例见仓库 ``plugins/stocks.yaml``(头注释即指路标)。
_CATEGORY_TEMPLATE = """# 最小品类模板:必填仅 id/name/schedule + sources[](源必填 name/url,
# engine 缺省 auto、extract 缺省 L3 兜底、push 缺省空表)。
# 完整 12 节示例与逐字段注释见 plugins/stocks.yaml(权威示例);
# 凭据只允许 env:VAR / keychain:NAME 引用,明文即拒载(security-baseline)。
id: my-category
name: 我的品类
schedule: "0 9 * * *"
sources:
  - name: example
    url: "https://example.com/"
"""


def _fence_yaml_path(file_raw: Any) -> tuple[Path, ServeContext]:
    """yaml.* 方法的路径围栏:后缀 + resolve 后必须位于 plugins 目录内。

    安全底线(task 10-03-yaml-editor design §1):sidecar 是 UI 直连的读写
    通道,不设围栏 = 桌面端任意文件读写原语。三道门:

    1. 后缀 ∈ {``.yaml``, ``.yml``} → 否则 ``not_yaml_suffix``;
    2. ``Path.resolve()``(消解符号链接与 ``..``)后 ``os.path.commonpath``
       判定必须位于 serve 上下文 plugins 目录之下 → 否则 ``path_outside_root``
       (message 带两个路径,如实展示;不做字符串前缀比对,Windows 分隔符安全);
    3. 新建场景的 stem 检查在 :func:`_m_yaml_save` 内(file 不存在时才适用)。

    Returns:
        (resolve 后的目标路径, serve 上下文)—— 后续读写都落在 resolve 结果上,
        目录内符号链接指向目录内文件属合法形态。
    """
    if not isinstance(file_raw, str) or not file_raw:
        raise ProtocolError("invalid_params", "缺少文件路径 file", path="params.file")
    ctx = _serve_context()
    root = Path(ctx.plugins_dir).resolve()
    path = Path(file_raw).expanduser()
    if path.suffix not in (".yaml", ".yml"):
        raise ProtocolError(
            "not_yaml_suffix", f"文件后缀必须是 .yaml 或 .yml: {file_raw}", path="params.file"
        )
    resolved = path.resolve()
    try:
        inside = os.path.commonpath([str(resolved), str(root)]) == str(root)
    except ValueError:  # 跨盘符等无公共前缀情形,一律按越界处理
        inside = False
    if not inside:
        raise ProtocolError(
            "path_outside_root",
            f"文件路径越出 plugins 目录: {resolved}(根: {root})",
            path="params.file",
            data={"resolved": str(resolved), "root": str(root)},
        )
    return resolved, ctx


def _yaml_files(plugins_dir: Path) -> list[Path]:
    """plugins 目录内的品类 YAML 清单(``*.yaml``/``*.yml``,按文件名排序)。

    非递归 glob:``.disabled.json``/``.bak``/``.seeded`` 天然不命中,
    ``myssia-*/plugin.yaml`` 市场子目录不入列(health 扫描同款约定)。
    """
    if not plugins_dir.is_dir():
        raise ProtocolError(
            "source_dir_unreadable", f"plugins 目录不可读: {plugins_dir}", path="params"
        )
    files = {path for pattern in ("*.yaml", "*.yml") for path in plugins_dir.glob(pattern)}
    return sorted(files, key=lambda path: path.name)


def _yaml_file_entry(path: Path) -> dict[str, Any]:
    """yaml.list 单项:解析状态 + 品类元信息(坏文件也入列,parse_ok=false)。"""
    item: dict[str, Any] = {
        "file": str(path),
        "name": path.name,
        "parse_ok": False,
        "category_id": None,
        "category_name": None,
        "sources": None,
        "error": None,
    }
    try:
        config = load_category_file(path)
    except LoadError as exc:
        first = exc.errors[0]
        item["error"] = {"path": first.path, "code": first.error_type, "message": first.message}
        return item
    item["parse_ok"] = True
    item["category_id"] = config.id
    item["category_name"] = config.name
    item["sources"] = len(config.sources)
    return item


def _collect_category_ids(plugins_dir: Path, *, exclude: Path) -> dict[str, Path]:
    """目录扫描取 parse_ok 文件们的品类 id(yaml.save 跨文件查重用)。

    现状 loader 对重复 id 零守卫 —— 两个 ``id: stocks`` 会静默混品类,
    写盘门是唯一能拦的地方;同 id 多文件时取首个(字典序)保持确定性。
    """
    ids: dict[str, Path] = {}
    for path in _yaml_files(plugins_dir):
        if path.resolve() == exclude:
            continue
        try:
            config = load_category_file(path)
        except LoadError:
            continue  # 坏文件本就装不起来,不参与 id 空间
        ids.setdefault(config.id, path)
    return ids


def _iter_keychain_refs(node: Any, path: str = "$"):
    """递归枚举文档中的 ``keychain:`` 引用,产出 ``(字段路径, 凭据名)``。

    ``env:`` 不对照(名单运行时才知,必误报 —— 决议 8);引用语法判定复用
    schema 的 :data:`_SECRET_REF_RE`(同一先例:cli.py/manifest.py 受控复用),
    非 ref 形态的普通字符串直接跳过。
    """
    if isinstance(node, Mapping):
        for key, value in node.items():
            yield from _iter_keychain_refs(value, f"{path}.{key}")
    elif isinstance(node, (list, tuple)):
        for index, value in enumerate(node):
            yield from _iter_keychain_refs(value, f"{path}[{index}]")
    elif isinstance(node, str):
        match = _SECRET_REF_RE.match(node)
        if match is not None and match.group("kc") is not None:
            yield path, match.group("kc")


def _validate_yaml_content(
    content: str, *, source: str | None = None
) -> tuple[list[dict[str, Any]], CategoryConfig | None]:
    """yaml.validate / yaml.save 共享的同一道校验门(防两门漂移)。

    流程:``_UniqueKeyLoader`` 解析(重复键即 ``yaml_parse_error``)→
    :func:`load_category` 同门校验(与 ``myssia run`` 一致)→ ``keychain:``
    引用对照已录入凭据名单。**不落盘** —— validate 干跑零写入由调用方保证,
    save 在此之后才碰文件系统。

    Returns:
        (findings, config):findings 每项 ``{path, code, message, level}``,
        ``level`` ∈ error/warning(warning 不拦保存 —— 先写 YAML 后
        ``myssia secret set`` 补凭据是合法流,决议 8);config 为装载成功的
        品类模型(用于 save 的跨文件查重与 validate 的 category 摘要)。
    """
    findings: list[dict[str, Any]] = []
    try:
        doc = yaml.load(content, Loader=_UniqueKeyLoader)
    except yaml.YAMLError as exc:
        findings.append(
            {"path": "$", "code": "yaml_parse_error",
             "message": f"YAML 语法无法解析: {exc}", "level": "error"}
        )
        return findings, None
    config: CategoryConfig | None = None
    try:
        config = load_category(doc if isinstance(doc, Mapping) else doc, source=source)
    except LoadError as exc:
        for detail in exc.errors:
            findings.append(
                {"path": detail.path, "code": detail.error_type,
                 "message": detail.message, "level": "error"}
            )
    if isinstance(doc, Mapping):
        try:
            known = set(list_secrets())
        except SecretError:
            known = None  # 钥匙链不可用:对照降级跳过,不误报 warning
        if known is not None:
            for ref_path, name in _iter_keychain_refs(doc):
                if name not in known:
                    findings.append(
                        {"path": ref_path, "code": "secret_unknown", "level": "warning",
                         "message": f"凭据 {name} 尚未录入钥匙链"
                                    f"(先 myssia secret set {name} 或桌面端凭据页录入;"
                                    f"保存不受影响,补录前相关源会采集失败)"}
                    )
    return findings, config


def _m_yaml_list(params: dict[str, Any]) -> dict[str, Any]:
    """plugins 目录的品类 YAML 清单(目录由 serve 上下文定,不开放目录参数)。

    目录扫描而非取自 health:**坏文件也入列**(parse_ok=false + error)——
    编辑器的核心用例之一就是修好 health 加载不了的文件。
    """
    ctx = _serve_context()
    plugins_dir = Path(ctx.plugins_dir)
    return {
        "plugins_dir": str(plugins_dir),
        "files": [_yaml_file_entry(path) for path in _yaml_files(plugins_dir)],
    }


def _m_yaml_read(params: dict[str, Any]) -> dict[str, Any]:
    """品类 YAML 原文直读:不经任何 yaml dump 往返,注释/顺序逐字节原样。

    ``newline=""`` 是硬要求:Python 默认 universal newlines 会把 CRLF 读成
    LF,写回即变字节 —— 「逐字节保真」承诺靠它成立(design §1);失败一律
    结构化(invalid_encoding / file_too_large / file_not_found)。
    """
    resolved, _ctx = _fence_yaml_path(params.get("file"))
    try:
        stat = resolved.stat()
    except FileNotFoundError as exc:
        raise ProtocolError(
            "file_not_found", f"文件不存在: {resolved}", path="params.file"
        ) from exc
    except OSError as exc:
        raise ProtocolError(
            "source_file_unreadable", f"文件不可读: {resolved} ({exc})", path="params.file"
        ) from exc
    if stat.st_size > YAML_MAX_BYTES:
        raise ProtocolError(
            "file_too_large",
            f"文件超过 1 MiB 上限: {stat.st_size} 字节(limit={YAML_MAX_BYTES})",
            path="params.file",
            data={"size": stat.st_size, "limit": YAML_MAX_BYTES},
        )
    try:
        with open(resolved, encoding="utf-8", newline="") as handle:
            content = handle.read()
    except UnicodeDecodeError as exc:
        raise ProtocolError(
            "invalid_encoding",
            f"文件不是有效的 UTF-8 编码: {resolved} ({exc});请转存 UTF-8 后重试",
            path="params.file",
        ) from exc
    except OSError as exc:
        raise ProtocolError(
            "source_file_unreadable", f"文件不可读: {resolved} ({exc})", path="params.file"
        ) from exc
    return {"file": str(resolved), "content": content, "size": stat.st_size, "mtime": stat.st_mtime}


def _m_yaml_validate(params: dict[str, Any]) -> dict[str, Any]:
    """干跑校验:findings 分级返回,**永不抛校验错**(校验结果即正常应答)。

    ``valid`` = 无 error 级 finding(warning 不翻假);``file`` 仅作错误
    上下文,可不带。零写入(design §1:validate 干跑不落盘)。
    """
    content = params.get("content")
    if not isinstance(content, str):
        raise ProtocolError("invalid_params", "缺少字符串字段 content", path="params.content")
    file_raw = params.get("file")
    source = file_raw if isinstance(file_raw, str) and file_raw else None
    findings, config = _validate_yaml_content(content, source=source)
    category = None
    if config is not None:
        category = {"id": config.id, "name": config.name, "sources": len(config.sources)}
    return {
        "valid": not any(finding["level"] == "error" for finding in findings),
        "findings": findings,
        "category": category,
    }


def _m_yaml_template(params: dict[str, Any]) -> dict[str, Any]:
    """最小合法品类模板(id/name 占位,UI 按用户输入回填;决议 6 单模板)。"""
    return {"content": _CATEGORY_TEMPLATE}


def _m_yaml_save(params: dict[str, Any]) -> dict[str, Any]:
    """编辑写回:同门校验 error 级零容忍零写入 → 跨文件 id 查重 → ``.bak`` → 原子落盘。

    流程钉序(design §1):**围栏+stem 正则 → :func:`_validate_yaml_content`
    (error 级零容忍;warning 收集透传)→ 跨文件品类 id 查重 → 旧文件拷
    ``.bak``(新建无此步)→ :func:`_atomic_write_text`**(写用户原文,
    ``newline=""`` 逐字节保真)。

    - 新建语义:file 不存在 + ``expected_mtime=null`` = 创建;file 不存在 +
      非 null mtime = ``file_not_found``(「想改却不存在」与「想建」分开,
      防路径手误建出影子文件)。新建 stem 必须过品类 id 同款正则
      :data:`CATEGORY_ID_RE`,防 ``My Category.yaml`` 脏名进 plugins 目录。
    - 乐观锁:yaml.read 带回 mtime,save 对照;不符即 ``mtime_conflict``
      (与 sources.write 两条写路径靠它互斥,不靠运气)。file 已存在 +
      null mtime = 新建意图撞上已有文件,同样 ``mtime_conflict`` —— 绝不
      无锁覆盖。"""
    file_raw = params.get("file")
    content = params.get("content")
    if not isinstance(file_raw, str) or not file_raw:
        raise ProtocolError("invalid_params", "缺少文件路径 file", path="params.file")
    if not isinstance(content, str):
        raise ProtocolError("invalid_params", "缺少字符串字段 content", path="params.content")
    expected_mtime = params.get("expected_mtime")
    if expected_mtime is not None and (
        isinstance(expected_mtime, bool) or not isinstance(expected_mtime, (int, float))
    ):
        raise ProtocolError(
            "invalid_params", "expected_mtime 必须为数字或 null", path="params.expected_mtime"
        )

    resolved, ctx = _fence_yaml_path(file_raw)
    if len(content.encode("utf-8")) > YAML_MAX_BYTES:
        raise ProtocolError(
            "file_too_large",
            f"内容超过 1 MiB 上限: {len(content.encode('utf-8'))} 字节(limit={YAML_MAX_BYTES})",
            path="params.content",
            data={"size": len(content.encode("utf-8")), "limit": YAML_MAX_BYTES},
        )

    exists = resolved.exists()
    created = not exists
    if created:  # 新建场景:stem 正则 → mtime 语义(「想建」必须显式声明 null)
        if not CATEGORY_ID_RE.match(resolved.stem):
            raise ProtocolError(
                "invalid_file_stem",
                f"新建文件名 {resolved.name} 不合规:stem 必须过品类 id 同款正则"
                f" {CATEGORY_ID_RE.pattern}(小写字母/数字/``-``/``_``,1-64 字符;"
                f"中文名放 name: 字段)",
                path="params.file",
            )
        if expected_mtime is not None:
            raise ProtocolError(
                "file_not_found",
                f"目标文件不存在且携带非空 expected_mtime(非新建意图): {resolved};"
                f"请核对路径,或以 expected_mtime=null 显式新建",
                path="params.file",
            )
    else:
        current_mtime = resolved.stat().st_mtime
        if expected_mtime is None:
            raise ProtocolError(
                "mtime_conflict",
                f"目标文件已存在,新建意图(expected_mtime=null)撞上已有文件: {resolved};"
                f"请先 yaml.read 重读后再保存",
                path="params.expected_mtime",
            )
        if float(expected_mtime) != current_mtime:
            raise ProtocolError(
                "mtime_conflict",
                f"文件已被外部改动(CLI/别的窗口/启停开关),读时 mtime="
                f"{expected_mtime},当前 mtime={current_mtime};请 yaml.read 重读后再保存",
                path="params.expected_mtime",
                data={"expected_mtime": expected_mtime, "current_mtime": current_mtime},
            )

    findings, config = _validate_yaml_content(content, source=str(resolved))
    errors = [finding for finding in findings if finding["level"] == "error"]
    if errors or config is None:
        raise ProtocolError(
            "category_invalid",
            f"内容未过品类校验(error 级 {len(errors)} 处),零写入",
            path="params.content",
            data={"errors": errors},
        )
    conflict = _collect_category_ids(Path(ctx.plugins_dir), exclude=resolved).get(config.id)
    if conflict is not None:
        raise ProtocolError(
            "duplicate_category_id",
            f"品类 id {config.id!r} 已被 {conflict} 使用(重复 id 会静默混品类)",
            path="params.content",
            data={"conflicts": [str(conflict)]},
        )

    backed_up: str | None = None
    try:
        if exists:  # 旧文件留底 .bak(单份滚动);新建无此步
            bak = resolved.with_suffix(resolved.suffix + ".bak")
            shutil.copy2(resolved, bak)
            backed_up = str(bak)
        _atomic_write_text(resolved, content)
    except OSError as exc:
        raise ProtocolError(
            "source_write_failed", f"写回失败: {exc}", path="params.file"
        ) from exc
    return {
        "file": str(resolved),
        "written": True,
        "created": created,
        "backed_up": backed_up,
        "mtime": resolved.stat().st_mtime,
        "warnings": [finding for finding in findings if finding["level"] == "warning"],
    }


def _m_yaml_delete(params: dict[str, Any]) -> dict[str, Any]:
    """删除品类文件:围栏 → 拷 ``.bak`` → 删主文件 → 连带删 ``.disabled.json``。

    钉序的崩溃方向性:先备份后删,中途崩溃最坏 = 文件还在(无损方向)。
    ``.disabled.json`` 暂存归启停管,编辑器不碰 —— 唯一例外就是删除品类后的
    连带清理(暂存无主,留着是脏文件)。全删光 = 合法空态:``.seeded`` 标志
    在即不复种,feed 空态「新建」CTA 引导重建,恰好闭环。
    """
    resolved, _ctx = _fence_yaml_path(params.get("file"))
    if not resolved.exists():
        raise ProtocolError("file_not_found", f"文件不存在: {resolved}", path="params.file")
    bak = resolved.with_suffix(resolved.suffix + ".bak")
    try:
        shutil.copy2(resolved, bak)
        resolved.unlink()
    except OSError as exc:
        raise ProtocolError(
            "source_write_failed", f"删除失败(已先留底 {bak}): {exc}", path="params.file"
        ) from exc
    with contextlib.suppress(OSError):  # 暂存清理是尽力而为:主契约已完成
        _stash_path(resolved).unlink(missing_ok=True)
    return {"file": str(resolved), "deleted": True, "backed_up": str(bak)}


# ---------------------------------------------------------------------------
# 方法:schedule.preview(排程未来时刻预览;G4,10-03-feed-ux)
# ---------------------------------------------------------------------------


def _m_schedule_preview(params: dict[str, Any]) -> dict[str, Any]:
    """品类排程的 Next runs 预览(Apify 式,防 cron 写错;纯计算零副作用)。

    ``build_cron_trigger`` → ``get_next_fire_time`` 链推进 ``count`` 次
    (ISO-8601 本地时刻串;时区随品类 ``timezone`` 节,缺省系统时区)。
    ``file`` 过 :func:`_fence_yaml_path` 围栏 + ``load_category_file`` 同门
    装载(装不上 = ``source_file_unreadable``,与 sources.test 同款错误);
    品类无排程(schedule 空串)明示 ``schedule: null`` + ``runs: []``,
    不是错误(design §1)。``count`` 缺省 5,钳制 [1, 20]。
    """
    from myssia.pipeline import build_cron_trigger

    resolved, _ctx = _fence_yaml_path(params.get("file"))
    count = params.get("count", 5)
    if not isinstance(count, int) or isinstance(count, bool) or count < 1:
        raise ProtocolError("invalid_params", "count 必须为正整数", path="params.count")
    count = min(count, 20)
    try:
        config = load_category_file(resolved)
    except LoadError as exc:
        raise ProtocolError(
            "source_file_unreadable", f"品类 YAML 装不上: {exc}",
            path="params.file", data={"file": str(resolved)},
        ) from exc
    schedule = config.schedule or None
    runs: list[str] = []
    if schedule:
        try:
            trigger = build_cron_trigger(schedule, config.timezone)
        except ValueError as exc:  # schema 已校验 cron,此处防御性兜底
            raise ProtocolError("invalid_cron", str(exc), path="params.file") from exc
        # 推进姿势:previous 恒 None + now = 上一时刻 +1µs —— 严格递增,
        # 不依赖 apscheduler 对 previous_fire_time 分支的版本细节。
        from datetime import timedelta

        cursor = datetime.now(timezone.utc)
        while len(runs) < count:
            fire = trigger.get_next_fire_time(None, cursor)  # type: ignore[assignment]
            if fire is None:
                break
            runs.append(fire.isoformat())
            cursor = fire + timedelta(microseconds=1)
    return {"file": str(resolved), "schedule": schedule, "timezone": config.timezone, "runs": runs}


# ---------------------------------------------------------------------------
# 方法:sources.test(试抓此源,异步 job;C13)
# ---------------------------------------------------------------------------

# 同步实现禁令的依据:每源试抓缺省 120s(cli.py DEFAULT_TEST_TIMEOUT_SECONDS)
# = 壳层单请求 120s 硬超时(main.rs REQUEST_TIMEOUT),同步必撞 sidecar_timeout;
# 且 serve 循环单线程,同步会把整个桌面后端卡死至抓完 —— 照 image.analyze
# 先例做异步 job:提交即返 job_id,结果走 test.completed 事件。
_TEST_LOCK = threading.Lock()
_TEST_ACTIVE_JOB: int | None = None
_TEST_NEXT_JOB_ID = 0


def _sources_test_worker(job_id: int, cmd: list[str], env: dict[str, str], source: str | None) -> None:
    """后台线程:试抓子进程 → stderr 入环形缓冲(run_id=null)→ test.completed。"""
    global _TEST_ACTIVE_JOB
    try:
        proc = subprocess.Popen(
            cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=env,
            text=True, encoding="utf-8", errors="replace", bufsize=1,
            start_new_session=True,
        )
        # stdout 收集(末份 --json 文档;不进环形缓冲——试抓报告不是日志行),
        # stderr 走 _pump_stream(环形缓冲 + log 事件,logs.tail 可诊断)。
        stdout_lines: list[str] = []

        def _collect_stdout() -> None:
            assert proc.stdout is not None
            for raw in proc.stdout:
                stdout_lines.append(raw)

        readers = [
            threading.Thread(target=_collect_stdout, daemon=True),
            threading.Thread(target=_pump_stream, args=(None, proc.stderr, "stderr"), daemon=True),
        ]
        for thread in readers:
            thread.start()
        exit_code = proc.wait()
        for thread in readers:
            thread.join(timeout=5)
        payload = None
        for raw in reversed(stdout_lines):
            line = raw.strip()
            if not line:
                continue
            try:
                parsed = json.loads(line)
            except json.JSONDecodeError:
                continue
            if isinstance(parsed, dict):
                payload = parsed
                break
        ok = exit_code == 0 and payload is not None and "error" not in payload
        event: dict[str, Any] = {
            "type": "test.completed", "job_id": job_id, "ok": ok,
            "exit_code": exit_code, "ts": _now_iso(),
        }
        if ok:
            event["result"] = payload
        else:
            event["error"] = (payload or {}).get("error", "cli_error") if payload else "cli_error"
            if payload:
                event["data"] = payload
        _write_line(event)
    except Exception as exc:  # noqa: BLE001 — 兜底:事件必须可见
        _write_line({
            "type": "test.completed", "job_id": job_id, "ok": False, "exit_code": None,
            "error": "internal_error", "data": {"message": f"{type(exc).__name__}: {exc}"},
            "ts": _now_iso(),
        })
    finally:
        with _TEST_LOCK:
            if _TEST_ACTIVE_JOB == job_id:
                _TEST_ACTIVE_JOB = None


def _m_sources_test(params: dict[str, Any]) -> dict[str, Any]:
    """试抓此源(C13):围栏 → 异步 job(``myssia test <yaml> --source <s> --json``)。

    ``file`` 过 :func:`_fence_yaml_path`(试抓不得成为任意文件读原语);
    品类装不上 = ``source_file_unreadable``;单飞 = ``test_busy``。
    结果只走 ``test.completed`` 事件(提交即返,不阻塞 serve 循环)。
    """
    global _TEST_ACTIVE_JOB, _TEST_NEXT_JOB_ID
    file_raw = params.get("file")
    if not isinstance(file_raw, str) or not file_raw:
        raise ProtocolError("invalid_params", "缺少品类 YAML 路径 file", path="params.file")
    resolved, _ctx = _fence_yaml_path(file_raw)
    source = params.get("source")
    if source is not None and (not isinstance(source, str) or not source):
        raise ProtocolError("invalid_params", "source 必须为非空字符串", path="params.source")
    timeout = params.get("timeout")
    if timeout is not None:
        if not isinstance(timeout, (int, float)) or isinstance(timeout, bool) or timeout <= 0:
            raise ProtocolError("invalid_params", "timeout 必须为正数秒(≤120)", path="params.timeout")
        if timeout > 120:
            raise ProtocolError("invalid_params", "timeout 上限 120s(壳层单请求硬超时同值)", path="params.timeout")
    config = params.get("config")
    if config is not None and not isinstance(config, str):
        raise ProtocolError("invalid_params", "config 必须为字符串(全局 pools YAML 路径)", path="params.config")
    # 装不上品类:结构化即时拒(同 CLI load_category_file 门,零外网预检)
    try:
        load_category_file(resolved)
    except LoadError as exc:
        raise ProtocolError(
            "source_file_unreadable", f"品类 YAML 装不上: {exc}",
            path="params.file", data={"file": str(resolved)},
        ) from exc
    with _TEST_LOCK:
        if _TEST_ACTIVE_JOB is not None:
            raise ProtocolError(
                "test_busy", f"已有试抓在执行 job_id={_TEST_ACTIVE_JOB}(单飞)",
                data={"active_job_id": _TEST_ACTIVE_JOB},
            )
        _TEST_NEXT_JOB_ID += 1
        job_id = _TEST_NEXT_JOB_ID
        _TEST_ACTIVE_JOB = job_id
    argv_tail = ["test", str(resolved), "--json"]
    if source:
        argv_tail += ["--source", source]
    if timeout is not None:
        argv_tail += ["--timeout", str(timeout)]
    if config:
        argv_tail += ["--config", config]
    cmd, env = _self_command(argv_tail)
    threading.Thread(
        target=_sources_test_worker, args=(job_id, cmd, env, source), daemon=True,
    ).start()
    return {"job_id": job_id, "state": "running", **({"source": source} if source else {})}


# ---------------------------------------------------------------------------
# 方法:run.start / run.status / logs.tail(run 子进程 + 注册表 + 日志流)
# ---------------------------------------------------------------------------

_RUNS_LOCK = threading.Lock()
_RUNS: dict[int, dict[str, Any]] = {}
_NEXT_RUN_ID = 0
_ACTIVE_RUN_ID: int | None = None
#: run 子进程注册表(run.cancel 的杀进程落点;C2)。与 _RUNS 分家:
#: _RUNS 条目会整个进 run.status 应答,Popen 对象绝不能随行出协议面。
_RUN_PROCS: dict[int, subprocess.Popen] = {}
#: run.cancel 兜底计时器(持有引用防 GC 提前回收计时线程)。
_CANCEL_TIMERS: list[threading.Timer] = []
#: SIGTERM 后的 SIGKILL 宽限(run 子进程自清理窗口;killpg 进程组杀)。
_CANCEL_KILL_GRACE_SECONDS = 5.0
#: run.status 合流的 DB 历史行上限(10-07-logs-restart-visibility R1;防长列表)。
_RUN_HISTORY_LIMIT = 50

#: pipeline 结构化日志(logging 规范 key=value 形态)→ 进度事件。
#: 日志文案变化时优雅退化(进度事件停发,log 事件照常),不影响正确性。
_PROGRESS_PATTERNS: tuple[tuple[re.Pattern[str], str, tuple[str, ...]], ...] = (
    (re.compile(r"运行开始 category=(\S+) run_id=(\S+) sources=(\S+) dry_run=(\S+)"), "run_start",
     ("category", "pipeline_run_id", "sources", "dry_run")),
    (re.compile(r"采集完成 source=(\S+) engine=(\S+) items=(\S+)"), "source_done",
     ("source", "engine", "items")),
    (re.compile(r"采集步骤完成 sources=(\S+) items=\S+ source_failures=(\S+)"), "fetch_done",
     ("sources", "source_failures")),
    (re.compile(r"运行结束 category=(\S+) run_id=(\S+) status=(\S+) items=(\S+)"), "run_end",
     ("category", "pipeline_run_id", "run_status", "items")),
)


def _self_command(argv_tail: list[str]) -> tuple[list[str], dict[str, str]]:
    """构造 run 子进程命令:冻结包自启(直通模式)/ dev 下 ``python -m myssia.cli``。

    dev 下子进程未必装了 myia(conftest 靠 sys.path 注入 src/),以
    PYTHONPATH 指到 <repo>/src 保证可复现;冻结模式 PyInstaller 包自带全部模块。
    """
    env = os.environ.copy()
    if getattr(sys, "frozen", False):
        return [sys.executable, *argv_tail], env
    src = Path(__file__).resolve().parent.parent / "src"
    env["PYTHONPATH"] = str(src) + os.pathsep + env.get("PYTHONPATH", "")
    return [sys.executable, "-m", "myssia.cli", *argv_tail], env


def _emit_progress(run_id: int, line: str) -> None:
    for pattern, phase, fields in _PROGRESS_PATTERNS:
        match = pattern.search(line)
        if match is None:
            continue
        event = {"type": "progress", "run_id": run_id, "phase": phase, "ts": _now_iso()}
        event.update(dict(zip(fields, match.groups())))
        _write_line(event)
        return


def _pump_stream(run_id: int, stream_obj: Any, stream_name: str) -> None:
    """逐行转发子进程输出:统一漏斗(ring+盘)+ log 事件;stderr 兼做进度信号源。

    ``stream_line`` 返回的条目与环形同 seq 同 ts——事件直接复用其 line/ts,
    条目在两处的可见性一致(10-07-unified-logging 批1)。"""
    for raw in stream_obj:
        line = raw.rstrip("\n")
        if not line.strip():
            continue
        entry = myssia_log.stream_line(run_id, stream_name, line)
        _write_line({
            "type": "log", "run_id": run_id, "stream": stream_name,
            "line": entry["line"], "ts": entry["ts"],
        })
        if stream_name == "stderr":
            _emit_progress(run_id, entry["line"])


def _run_record_dict(record: Any) -> dict[str, Any]:
    """RunRecord → 协议字典(runs.list 行与 completed.record 同一形状,防两处漂移)。"""
    return {
        "run_id": record.id,
        "category": record.category,
        "status": record.status,
        "started_at": record.started_at.isoformat() if record.started_at else None,
        "finished_at": record.finished_at.isoformat() if record.finished_at else None,
        "stats": record.stats,
        "steps": record.steps,
        "error": record.error,
        "log_run_id": getattr(record, "log_run_id", None),
    }


def _replay_alerts_fired(run_id: int, db: str, started_at: str) -> int:
    """run 终态回放:查本 run 新增的 fired 行,逐条发 ``alerts.fired`` 事件。

    主路线(design §4.3):子进程 ``_alert_pass`` 把命中结构化落 ``alert_fired``
    表,父进程在 run 终态(发 ``completed`` 的同一收口处)以
    ``list_fired(since=run.started_at)`` 查新命中回放 —— 查库零格式耦合
    (备选的 stderr 正则解析因依赖子进程日志格式而弃)。事件形状钉死
    (design §4.2):``{type, rule_id, rule_name, item_id, dedup_key, title,
    action, action_status, ts}``。回放尽力而为:查库/解析失败只 stderr 注记,
    绝不拦 ``completed`` 事件。

    Returns:
        本次回放的事件条数(失败 = 0)。
    """
    store = None
    try:
        store = SQLiteStore(db)
        rows = store.list_fired(since=datetime.fromisoformat(started_at), limit=200)
        for fired in reversed(rows):  # list_fired 新→旧;回放按入库序(旧→新)
            _write_line({
                "type": "alerts.fired",
                "rule_id": fired.rule_id,
                "rule_name": fired.rule_name,
                "item_id": fired.item_id,
                "dedup_key": fired.dedup_key,
                "title": fired.title,
                "action": fired.action,
                "action_status": fired.action_status,
                "ts": fired.created_at.isoformat() if fired.created_at else _now_iso(),
            })
        return len(rows)
    except Exception as exc:  # noqa: BLE001 — 回放失败不拦 completed(尽力而为)
        print(f"sidecar: alerts.fired 回放失败 run_id={run_id}: {exc}", file=sys.stderr)
        return 0
    finally:
        if store is not None:
            store.close()


def _run_worker(run_id: int, cmd: list[str], env: dict[str, str], *, dry: bool, db: str,
                yaml_path: str, started_at: str, wall_start: float) -> None:
    """后台线程:跑 run 子进程 → 流式 log/progress 事件 → completed 事件。

    ``start_new_session=True``:run 自成进程组(dev 单进程形态行为不变)——
    冻结包是 onefile 双进程(bootloader + 真实 python 采集孙进程),
    run.cancel 用 killpg 才能一锅端,裸 ``proc.kill`` 只杀 bootloader
    漏孙进程(design §2.2 实证;dev 测试单进程,孙进程证据在装机冒烟)。
    """
    global _ACTIVE_RUN_ID
    proc = None
    try:
        proc = subprocess.Popen(
            cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=env,
            text=True, encoding="utf-8", errors="replace", bufsize=1,
            start_new_session=True,
        )
        with _RUNS_LOCK:
            _RUN_PROCS[run_id] = proc
        readers = [
            threading.Thread(target=_pump_stream, args=(run_id, proc.stdout, "stdout"), daemon=True),
            threading.Thread(target=_pump_stream, args=(run_id, proc.stderr, "stderr"), daemon=True),
        ]
        for thread in readers:
            thread.start()
        exit_code = proc.wait()
        for thread in readers:
            thread.join(timeout=10)
        record: dict[str, Any] | None = None
        # 非 dry 且采集语义退出码:runs 表有本 run 的持久化记录(stats/steps)。
        if not dry and exit_code in (0, 2, 3):
            store = None
            try:
                store = SQLiteStore(db)
                latest = store.latest_run()
                if latest is not None:
                    record = _run_record_dict(latest)
                    # 会话号回填(10-07-logs-restart-visibility R1):把注册表
                    # run_id 落到 runs 行——JSONL 日志行按会话号打 run_id,重启后
                    # 历史行展开 logs.tail 靠它对齐。尽力而为:回填失败只损失
                    # 「上一程」日志可达性,不连累 record 附挂(latest_run 启发式
                    # 的既有薄弱面照旧,回填跟随同一行,不放大误挂范围)。
                    try:
                        store.set_run_log_run_id(latest.id, run_id)
                    except Exception:  # noqa: BLE001 — 日志身份尽力而为,缺位不拦 completed
                        pass
            except Exception:  # noqa: BLE001 — record 尽力而为,缺位不拦 completed
                record = None
            finally:
                if store is not None:
                    store.close()
        status = STATUS_BY_EXIT.get(exit_code) if exit_code is not None else None
        if record is not None:
            status = record["status"]
        # 取消信号终局(SIGTERM/SIGKILL 都呈负退出码):可辨认终态 cancelled,
        # 优先于 runs 表残留状态(被杀 run 的表行停在 running,不回填不误报)。
        with _RUNS_LOCK:
            cancel_requested = bool(_RUNS.get(run_id, {}).get("cancel_requested"))
        if cancel_requested and exit_code is not None and exit_code < 0:
            status = "cancelled"
        duration_ms = int((datetime.now(timezone.utc).timestamp() - wall_start) * 1000)
        entry = _RUNS[run_id]
        entry.update(state="done", exit_code=exit_code, status=status,
                     finished_at=_now_iso(), duration_ms=duration_ms, record=record)
        # 告警回放(design §4.3 主路线):子进程 _alert_pass 已把新命中结构化落
        # alert_fired;终态收口处查库逐条发 alerts.fired(completed 之前,UI 角标
        # 先到、completed 触发的刷新随即带上新计数)。dry run 管线侧零落库,跳过。
        if not dry:
            _replay_alerts_fired(run_id, db, started_at)
        _write_line({
            "type": "completed", "run_id": run_id, "exit_code": exit_code, "status": status,
            "dry": dry, "duration_ms": duration_ms, "record": record, "ts": _now_iso(),
        })
    except Exception as exc:  # noqa: BLE001 — 工作线程兜底:错误必须以事件形式可见
        entry = _RUNS[run_id]
        entry.update(state="done", exit_code=None, status=None, finished_at=_now_iso(),
                     error=f"{type(exc).__name__}: {exc}")
        _write_line({"type": "completed", "run_id": run_id, "exit_code": None, "status": None,
                     "dry": dry, "error": f"{type(exc).__name__}: {exc}", "ts": _now_iso()})
    finally:
        with _RUNS_LOCK:
            _RUN_PROCS.pop(run_id, None)
            if _ACTIVE_RUN_ID == run_id:
                _ACTIVE_RUN_ID = None


def _m_run_cancel(params: dict[str, Any]) -> dict[str, Any]:
    """取消进行中的 run(进程组杀;C2)。SIGTERM → 宽限后 SIGKILL 兜底,立即返回。

    错误:未知 id / 无进行中 run = ``run_not_found``;已终态 = ``run_not_active``
    (data 带 state)。onefile 双进程必须 ``os.killpg``(bootloader 会转发
    SIGTERM 给孙进程;SIGKILL 兜底也走进程组,防孙进程成孤儿继续采集)。
    """
    run_id = params.get("run_id")
    with _RUNS_LOCK:
        if run_id is None:
            run_id = _ACTIVE_RUN_ID
            if run_id is None:
                raise ProtocolError("run_not_found", "当前没有进行中的 run", path="params.run_id")
        entry = _RUNS.get(run_id)
        if entry is None:
            raise ProtocolError("run_not_found", f"无此 run_id: {run_id}", path="params.run_id")
        if entry.get("state") != "running":
            raise ProtocolError(
                "run_not_active", f"run {run_id} 已终态,不可取消",
                path="params.run_id", data={"state": entry.get("state")},
            )
        proc = _RUN_PROCS.get(run_id)
        entry["cancel_requested"] = True
    if proc is not None and proc.poll() is None:
        def _kill_group(sig: int) -> None:
            try:
                os.killpg(os.getpgid(proc.pid), sig)  # type: ignore[arg-type]
            except (ProcessLookupError, PermissionError):
                pass  # 进程已收尸/权限边界:宽限兜底自然无事可做

        _kill_group(signal.SIGTERM)
        timer = threading.Timer(_CANCEL_KILL_GRACE_SECONDS, _kill_group, args=(signal.SIGKILL,))
        timer.daemon = True
        timer.start()
        with _RUNS_LOCK:
            _CANCEL_TIMERS.append(timer)
    return {"run_id": run_id, "cancelled": True, "state": "running"}


def _m_run_start(params: dict[str, Any]) -> dict[str, Any]:
    """启动 run 子进程(立即返回);dry/real 与退出码语义由 CLI 层保证。"""
    global _NEXT_RUN_ID, _ACTIVE_RUN_ID
    yaml_path = params.get("yaml")
    if not isinstance(yaml_path, str) or not yaml_path:
        raise ProtocolError("invalid_params", "缺少品类 YAML 路径 yaml", path="params.yaml")
    dry = bool(params.get("dry", False))
    db = str(params.get("db") or _serve_context().db)
    with _RUNS_LOCK:
        if _ACTIVE_RUN_ID is not None:
            raise ProtocolError(
                "run_busy", f"已有 run 在执行 run_id={_ACTIVE_RUN_ID}(桌面单飞;请等待 completed 事件)",
                data={"active_run_id": _ACTIVE_RUN_ID},
            )
        _NEXT_RUN_ID += 1
        run_id = _NEXT_RUN_ID
        _ACTIVE_RUN_ID = run_id
    argv_tail = ["run", yaml_path, "--db", db]
    if dry:
        argv_tail.append("--dry-run")
    if params.get("config"):
        argv_tail += ["--config", str(params["config"])]
    cmd, env = _self_command(argv_tail)
    started_at = _now_iso()
    _RUNS[run_id] = {
        "run_id": run_id, "yaml": yaml_path, "db": db, "dry": dry, "state": "running",
        "exit_code": None, "status": None, "started_at": started_at,
        "finished_at": None, "duration_ms": None, "record": None,
    }
    threading.Thread(
        target=_run_worker,
        args=(run_id, cmd, env), kwargs={"dry": dry, "db": db, "yaml_path": yaml_path,
                                         "started_at": started_at,
                                         "wall_start": datetime.now(timezone.utc).timestamp()},
        daemon=True,
    ).start()
    return {"run_id": run_id, "state": "running", "yaml": yaml_path, "dry": dry, "db": db}


def _history_run_rows(db: str, exclude_db_ids: set[int], limit: int) -> list[dict[str, Any]]:
    """runs 表 → 「上一程」历史行(10-07-logs-restart-visibility R1;尽力而为)。

    - 只收 ``finished_at`` 非 None 的收口行:库内 status=running 无 finished_at
      的行是崩溃残留/他进程在途,历史徽标下冒充「运行中」会说谎,如实不列;
    - 去重:``exclude_db_ids`` = 注册表行 record.run_id 集(同跑次不双列;
      裸 run_id 是两个编号空间,耐久身份只有 record.run_id,dry run 缺位即
      无从去重——DB 无 dry 行,天然不撞);
    - 上限 ``limit``(防长列表);僵尸行与去重行**不占余量**:递增拉取窗
      (首窗 = limit + 排除数,收不满即翻倍扩窗续拉尾段)直到收满 ``limit``
      条合格历史或行尽(low①;``ORDER BY id DESC`` 前缀稳定,扩窗后旧窗
      前段不重扫,``consumed`` 只走增量);
    - 行形状 = 注册表条目超集:RunEntry 键全在场(yaml/exit_code 无库源,置
      None;dry 恒 False——dry run 不落库)+ ``history: True`` 徽标 +
      ``log_run_id``(展开历史行调 ``logs.tail?run_id=`` 的对齐键,旧库行
      None = 无法对齐,如实降级);
    - 尽力而为:库打不开/读失败 → 空列表(注册表视图不受 DB 故障牵连——
      run.cancel/单飞锁语义都活在注册表侧,历史合流不能反客为主)。
    """
    try:
        store = SQLiteStore(db)
    except (StoreSchemaError, sqlite3.Error, OSError):
        return []
    rows: list[dict[str, Any]] = []
    try:
        window = limit + len(exclude_db_ids)
        consumed = 0
        while True:
            records = store.list_runs(limit=window)
            for record in records[consumed:]:
                if len(rows) >= limit:
                    break
                if record.id in exclude_db_ids or record.finished_at is None:
                    continue
                duration_ms = None
                if record.started_at is not None:
                    duration_ms = int(
                        (record.finished_at - record.started_at).total_seconds() * 1000
                    )
                rows.append({
                    "run_id": record.id,
                    "yaml": None,
                    "db": db,
                    "dry": False,
                    "state": "done",
                    "exit_code": None,
                    "status": record.status,
                    "started_at": record.started_at.isoformat() if record.started_at else None,
                    "finished_at": record.finished_at.isoformat(),
                    "duration_ms": duration_ms,
                    "record": _run_record_dict(record),
                    "history": True,
                    "log_run_id": getattr(record, "log_run_id", None),
                })
            if len(rows) >= limit or len(records) < window:
                break  # 收满 limit 条 或 DB 行尽(返回量 < 拉取窗)
            consumed = len(records)
            window *= 2
    except (sqlite3.Error, OSError, ValueError):
        return []
    finally:
        store.close()
    return rows


def _m_run_status(params: dict[str, Any]) -> dict[str, Any]:
    """run 注册表查询合流 DB 历史(10-07-logs-restart-visibility R1)。

    - ``run_id`` 指定:注册表单行查(语义不变;未知 id = 结构化 404)——
      历史行不经此路(会话号与 DB 号是两个空间,按 DB 号查注册表必歧义);
    - ``run_id`` 缺省:注册表全部(新→旧,现有语义/形状逐字节不变)在前,
      DB runs 表「上一程」历史行(新→旧,带 ``history`` 徽标)接续在后;
      同跑次以 record.run_id 去重不双列;历史 ≤ ``_RUN_HISTORY_LIMIT``。
      重启后注册表空 → 历史行接管日志屏列表(回填行的 UI 入口),空库
      零行 = 空态形状与现状全同。
    """
    run_id = params.get("run_id")
    with _RUNS_LOCK:
        if run_id is not None:
            entry = _RUNS.get(run_id)
            if entry is None:
                raise ProtocolError("run_not_found", f"无此 run_id: {run_id}", path="params.run_id")
            runs = [dict(entry)]
        else:
            runs = [dict(_RUNS[key]) for key in sorted(_RUNS, reverse=True)]
    if run_id is None:
        seen_db_ids = {
            (row.get("record") or {}).get("run_id")
            for row in runs
            if isinstance(row.get("record"), dict)
        }
        seen_db_ids.discard(None)
        db = str(params.get("db") or _serve_context().db)
        runs += _history_run_rows(db, seen_db_ids, _RUN_HISTORY_LIMIT)
    return {"runs": runs}


def _m_runs_list(params: dict[str, Any]) -> dict[str, Any]:
    """runs 表直读(SQLiteStore.list_runs,新→旧;C3)。

    run.status 只读内存注册表,sidecar 重启即空 —— 历史成功率的真数据源
    是 runs 表;内存态仅保留「进行中」语义。limit 钳制 [1,200](钳制不报错)。
    """
    limit_raw = params.get("limit", 50)
    if limit_raw is None:
        limit_raw = 50
    if not isinstance(limit_raw, int) or isinstance(limit_raw, bool):
        raise ProtocolError("invalid_params", "limit 必须为整数", path="params.limit")
    limit = max(1, min(limit_raw, 200))
    category = params.get("category")
    if category is not None and not isinstance(category, str):
        raise ProtocolError("invalid_params", "category 必须为字符串", path="params.category")
    db = params.get("db") or _serve_context().db
    try:
        store = SQLiteStore(db)
    except StoreSchemaError as exc:
        raise ProtocolError(exc.code, str(exc), path="params.db", data=exc.details) from exc
    try:
        records = store.list_runs(category=category or None, limit=limit)
    except ValueError as exc:
        raise ProtocolError("invalid_params", str(exc), path="params") from exc
    finally:
        store.close()
    return {"db": str(db), "count": len(records), "runs": [_run_record_dict(record) for record in records]}


# ---------------------------------------------------------------------------
# 方法:runs.trend
# (G6 成功率折线,10-04-desktop-b234;runs 表逐日×status 聚合 —— runs.list 的
# limit≤200 在 cron 排程 + 手动 run 下 30 天窗可超限,前端聚合会静默失真,
# SQL GROUP BY 一次往返即真数据;口径 = UTC 逐日,与 store.trend 同窗同门)
# ---------------------------------------------------------------------------


def _m_runs_trend(params: dict[str, Any]) -> dict[str, Any]:
    """run 成功率趋势(days 钳制 [1,90];逐日 status 计数,零数日补齐归前端)。"""
    days = params.get("days", 14)
    if days is None:
        days = 14
    if not isinstance(days, int) or isinstance(days, bool):
        raise ProtocolError("invalid_params", "days 必须为整数", path="params.days")
    days = max(1, min(days, 90))
    category = params.get("category")
    if category is not None and (not isinstance(category, str) or not category):
        raise ProtocolError("invalid_params", "category 必须为非空字符串", path="params.category")
    db = params.get("db") or _serve_context().db
    try:
        store = SQLiteStore(db)
    except StoreSchemaError as exc:
        raise ProtocolError(exc.code, str(exc), path="params.db", data=exc.details) from exc
    try:
        rows = store.daily_run_outcomes(days=days, category=category)
    except ValueError as exc:
        raise ProtocolError("invalid_params", str(exc), path="params") from exc
    finally:
        store.close()
    return {"days": [
        {"date": row["date"], "total": row["total"], "statuses": row["statuses"]}
        for row in rows
    ]}


# ---------------------------------------------------------------------------
# 方法:feedback.mark / feedback.list / feedback.stats
# (B2,10-03-v112-desktop-parity:桌面反馈入口;与 CLI ``myssia feedback`` 同门
# 直调 myssia.feedback —— channel="desktop" 落库,CLI ``feedback list`` 无过滤
# 即见同一条目,往返一致;载荷键逐一对齐 cli.py `_feedback_row_dict` / stats 报文)
# ---------------------------------------------------------------------------


def _feedback_row_dict(record: Any) -> dict[str, Any]:
    """反馈行机器形态(键同 cli.py `_feedback_row_dict`;本地小助手防跨模块私有引用)。"""
    return {
        "id": record.id,
        "item_id": record.item_id,
        "dedup_key": record.dedup_key,
        "verdict": record.verdict,
        "channel": record.channel,
        "title": record.title,
        "category": record.category,
        "created_at": record.created_at.isoformat() if record.created_at else None,
    }


def _m_feedback_mark(params: dict[str, Any]) -> dict[str, Any]:
    """卡片 👍/👎 入库(record_feedback 同门,channel=desktop;B2)。

    ``item`` = items.id(int)或 dedup_key/URL(str),经 :func:`resolve_item_ref`
    解析;条目不存在 = ``item_not_found``;verdict ∉ {good,bad} = ``feedback``。
    """
    item_ref = params.get("item")
    if isinstance(item_ref, bool) or item_ref is None or item_ref == "":
        raise ProtocolError("invalid_params", "缺少条目引用 item(items.id 或 dedup_key/URL)", path="params.item")
    verdict = params.get("verdict")
    if verdict not in ("good", "bad"):
        raise ProtocolError("feedback", f"verdict 必须是 good 或 bad,得到 {verdict!r}", path="params.verdict")
    db = params.get("db") or _serve_context().db
    try:
        store = SQLiteStore(db)
    except StoreSchemaError as exc:
        raise ProtocolError(exc.code, str(exc), path="params.db", data=exc.details) from exc
    try:
        item = resolve_item_ref(store, item_ref)
        if item is None:
            raise ProtocolError(
                "item_not_found",
                f"条目不存在: {item_ref!r}(可传 items.id 或 dedup_key/URL)",
                path="params.item",
            )
        try:
            record = record_feedback(
                store, verdict=verdict, channel=FEEDBACK_CHANNEL_DESKTOP, item=item
            )
        except ValueError as exc:
            raise ProtocolError("feedback", str(exc), path="params") from exc
    finally:
        store.close()
    return {
        "feedback_id": record.id,
        "item_id": record.item_id,
        "dedup_key": record.dedup_key,
        "verdict": record.verdict,
        "channel": record.channel,
    }


def _m_feedback_list(params: dict[str, Any]) -> dict[str, Any]:
    """反馈记录清单(SQLiteStore.list_feedback 直读,新→旧;B2)。"""
    verdict = params.get("verdict")
    if verdict is not None and verdict not in ("good", "bad"):
        raise ProtocolError("invalid_params", f"verdict 必须是 good 或 bad,得到 {verdict!r}", path="params.verdict")
    channel = params.get("channel")
    if channel is not None and (not isinstance(channel, str) or not channel):
        raise ProtocolError("invalid_params", "channel 必须为非空字符串", path="params.channel")
    limit = params.get("limit", 50)
    if limit is None:
        limit = 50
    if not isinstance(limit, int) or isinstance(limit, bool) or limit < 1:
        raise ProtocolError("invalid_params", "limit 必须为正整数", path="params.limit")
    db = params.get("db") or _serve_context().db
    try:
        store = SQLiteStore(db)
    except StoreSchemaError as exc:
        raise ProtocolError(exc.code, str(exc), path="params.db", data=exc.details) from exc
    try:
        rows = store.list_feedback(verdict=verdict, channel=channel, limit=limit)
    except ValueError as exc:
        raise ProtocolError("invalid_params", str(exc), path="params") from exc
    finally:
        store.close()
    return {"count": len(rows), "items": [_feedback_row_dict(row) for row in rows]}


def _m_feedback_stats(params: dict[str, Any]) -> dict[str, Any]:
    """窗口统计 + 生效调参 + 调参历史(键同 CLI ``feedback stats --json``;B2)。"""
    window_days = params.get("window_days", 14)
    if window_days is None:
        window_days = 14
    if not isinstance(window_days, int) or isinstance(window_days, bool) or window_days < 1:
        raise ProtocolError("invalid_params", "window_days 必须为正整数", path="params.window_days")
    top = params.get("top", 5)
    if top is None:
        top = 5
    if not isinstance(top, int) or isinstance(top, bool) or top < 1:
        raise ProtocolError("invalid_params", "top 必须为正整数", path="params.top")
    try:
        policy = TuningPolicy(window_days=window_days, top_n=top)
    except ValueError as exc:
        raise ProtocolError("feedback", str(exc), path="params") from exc
    db = params.get("db") or _serve_context().db
    try:
        store = SQLiteStore(db)
    except StoreSchemaError as exc:
        raise ProtocolError(exc.code, str(exc), path="params.db", data=exc.details) from exc
    try:
        tuner = FeedbackTuner(policy)
        stats = tuner.stats(store)
        active = load_active_tuning(store)
        history = [
            {
                "id": row.id,
                "kind": row.kind,
                "payload": dict(row.payload),
                "created_at": row.created_at.isoformat() if row.created_at else None,
            }
            for row in store.list_tuning(limit=10)
        ]
    except ValueError as exc:
        raise ProtocolError("feedback", str(exc), path="params") from exc
    finally:
        store.close()
    return {
        "window_days": policy.window_days,
        "stats": stats.to_dict(),
        "active_tuning": active.to_dict(),
        "tuning_history": history,
    }


# ---------------------------------------------------------------------------
# 方法:store.trend
# (B4,10-03-v112-desktop-parity:采集量趋势 —— items 按 first_seen UTC 逐日
# 计数,SQLiteStore.daily_item_counts 直读;口径 = UTC 逐日,不做时区换算)
# ---------------------------------------------------------------------------


def _m_store_trend(params: dict[str, Any]) -> dict[str, Any]:
    """采集量趋势(days 钳制 [1,90];零数日补齐归前端 fillDailyCounts)。"""
    days = params.get("days", 14)
    if days is None:
        days = 14
    if not isinstance(days, int) or isinstance(days, bool):
        raise ProtocolError("invalid_params", "days 必须为整数", path="params.days")
    days = max(1, min(days, 90))
    category = params.get("category")
    if category is not None and (not isinstance(category, str) or not category):
        raise ProtocolError("invalid_params", "category 必须为非空字符串", path="params.category")
    db = params.get("db") or _serve_context().db
    try:
        store = SQLiteStore(db)
    except StoreSchemaError as exc:
        raise ProtocolError(exc.code, str(exc), path="params.db", data=exc.details) from exc
    try:
        rows = store.daily_item_counts(days=days, category=category)
    except ValueError as exc:
        raise ProtocolError("invalid_params", str(exc), path="params") from exc
    finally:
        store.close()
    return {"days": [{"date": date, "count": count} for date, count in rows]}


def _m_logs_tail(params: dict[str, Any]) -> dict[str, Any]:
    """环形缓冲尾部;lines 上限 = 缓冲容量,run_id 可选过滤。

    数据面切到统一模块环形(``myssia.log.ring_snapshot``,批1):语义
    逐字对齐旧实现(run_id 过滤 + 尾部截取);serve 启动的盘尾回填
    (design §5)让重启后这里也能翻到上一程历史——请求/响应形状零变化。
    """
    lines = params.get("lines", 200)
    if not isinstance(lines, int) or lines < 1:
        raise ProtocolError("invalid_params", "lines 必须为正整数", path="params.lines")
    lines = min(lines, myssia_log.CAPACITY)
    run_id = params.get("run_id")
    # total/truncated 相对**过滤后总数**(旧实现语义,复查①):ring_snapshot
    # 自带尾部截取,先截尾再计数会让 total 恒 ≤ lines、truncated 恒 False,
    # 前端「缓冲截断」徽标死亡。环形帽结构性 ≤ CAPACITY,故传 CAPACITY 取
    # 全量过滤视图,尾部截取归本函数自理。
    snapshot = myssia_log.ring_snapshot(run_id=run_id, lines=myssia_log.CAPACITY)
    return {
        "lines": snapshot[-lines:],
        "total": len(snapshot),
        "truncated": len(snapshot) > lines,
    }


# ---------------------------------------------------------------------------
# 方法:image.config.read / config.save
# (看图配置协议;10-03-vision-pipeline 拆四留二:image.import/ocr/analyze/
#  status 四方法、image.progress/completed 两事件与 _image_analyze_worker
#  已整拆——看图能力并入情报管线;配置读写是设置屏 VisionForm 的依赖故留。
#  能力实现在 myssia.vision 包:settings=vision.yaml 同门校验,引擎层不动)
# ---------------------------------------------------------------------------


def _vision_yaml_path(ctx: ServeContext) -> Path:
    """vision.yaml 路径:home 模式落数据根;dev 回退 cwd 相对(与 db/plugins 同约)。"""
    return ctx.home / VISION_FILE_NAME if ctx.home is not None else Path(VISION_FILE_NAME)


def _gates_yaml_path(ctx: ServeContext) -> Path:
    """gates.yaml 路径:与 vision.yaml 同位(home 模式落数据根;dev 回退 cwd 相对)。

    门槛件知情启用配置(10-05-plugin-market-batch 批二 D4):plugins.list 的
    分组徽标 / doctor 的门槛 findings / 设置面 gates.get/save 共用本路径,
    解析挂 ``_serve_context`` 优先级链(显式 params > MYIA_HOME env > bundle
    探测 > dev cwd)。
    """
    return ctx.home / GATES_FILE_NAME if ctx.home is not None else Path(GATES_FILE_NAME)


def _m_gates_get(params: dict[str, Any]) -> dict[str, Any]:
    """gates.get:门槛配置脱敏读取(design §6.7 契约 ``{config, path}``)。

    坏文件 **fail-closed 不炸设置屏**:全关态 + 结构化 ``error`` 带回
    (与 CLI plugin list 的 ``gates.error`` 同形状),UI 据此提示「已按全关
    处理」并可用一次合法 save 覆写修复 —— 与 :func:`_m_image_config_read`
    的 fail fast 不同属刻意:vision.yaml 坏是单能力失效,门槛配置坏时
    设置屏必须仍可进(它是修复入口)。
    """
    ctx = _serve_context()
    path = _gates_yaml_path(ctx)
    config, error = load_gates_fail_closed(path)
    return {
        "config": config.to_payload(),
        "path": str(path),
        "exists": path.exists(),
        "error": error,
    }


def _m_gates_save(params: dict[str, Any]) -> dict[str, Any]:
    """gates.save:同门校验(:class:`GatesConfig` 构造即校验)→ tmp+rename 原子写。

    校验失败(未知字段/明文凭据/非布尔等)= ``gates_config_invalid``
    结构化 error **零写入**;成功应答 design §6.7 契约 ``{ok, path}``。
    """
    payload = params.get("config")
    if not isinstance(payload, dict):
        raise ProtocolError("invalid_params", "缺少对象字段 config", path="params.config")
    try:
        config = GatesConfig.from_payload(payload)
    except GatesLoadError as exc:
        raise ProtocolError(
            "gates_config_invalid",
            f"门槛配置未过校验,零写入: {exc}",
            path="params.config",
            data=exc.to_dict(),
        ) from exc
    saved = save_gates_config(_gates_yaml_path(_serve_context()), config)
    return {"ok": True, "path": str(saved)}


def _load_vision(ctx: ServeContext) -> VisionConfig:
    """装载 vision.yaml(VisionConfigError → image_config_invalid,fail fast)。"""
    try:
        return load_vision_config(_vision_yaml_path(ctx))
    except VisionConfigError as exc:
        raise ProtocolError(
            "image_config_invalid", f"vision 配置拒载: {exc}", path="vision.yaml", data=exc.to_dict()
        ) from exc


def _m_image_config_read(params: dict[str, Any]) -> dict[str, Any]:
    """vision.yaml 脱敏读取:文件不存在 = 全缺省(合法未配置态)。"""
    ctx = _serve_context()
    path = _vision_yaml_path(ctx)
    config = _load_vision(ctx)
    return {"file": str(path), "exists": path.exists(), "config": config.to_payload()}


def _m_image_config_save(params: dict[str, Any]) -> dict[str, Any]:
    """vision.yaml 保存:同门校验(:class:`VisionConfig` 构造即校验)失败零写入。"""
    payload = params.get("config")
    if not isinstance(payload, dict):
        raise ProtocolError("invalid_params", "缺少对象字段 config", path="params.config")
    try:
        config = VisionConfig.from_payload(payload)
    except VisionConfigError as exc:
        raise ProtocolError(
            "image_config_invalid", f"看图配置未过校验,零写入: {exc}",
            path="params.config", data=exc.to_dict(),
        ) from exc
    path = save_vision_config(_vision_yaml_path(_serve_context()), config)
    return {"ok": True, "file": str(path)}


# ---------------------------------------------------------------------------
# 方法:image.models.list / download / delete / activate + image.server.status
#       / image.server.ensure(10-03-vision-v2;能力实现 myssia.vision.models /
#       myssia.vision.server,契约与前端 TS 侧同形状冻结)
# ---------------------------------------------------------------------------

#: 模型下载单飞(桌面一次一个大模型;并发下载只会互相抢带宽与磁盘)。
_MODELS_DL_LOCK = threading.Lock()
_MODELS_DL_ACTIVE_JOB: int | None = None
_MODELS_DL_NEXT_JOB_ID = 0


def _vision_models_root(ctx: ServeContext) -> Path:
    """模型根:vision.yaml 同目录 ``models/``(home 模式 = ``<home>/models``)。"""
    return _vision_yaml_path(ctx).parent / "models"


def _active_model_path(ctx: ServeContext) -> str:
    """当前激活模型路径(lenient:vision.yaml 拒载按未配置,清单不因坏配置炸)。"""
    try:
        return load_vision_config(_vision_yaml_path(ctx)).local_model
    except VisionConfigError:
        return ""


def _require_model_name(params: dict[str, Any]) -> str:
    """模型名参数校验(非空字符串;delete/activate 共用)。"""
    name = params.get("name")
    if not isinstance(name, str) or not name:
        raise ProtocolError("invalid_params", "缺少模型名 name", path="params.name")
    return name


def _m_image_models_list(params: dict[str, Any]) -> dict[str, Any]:
    """已装模型清单(空目录 = 合法空表,UI 给下载引导不报错)。"""
    ctx = _serve_context()
    active = _active_model_path(ctx)
    return {
        "models": vision_list_models(_vision_models_root(ctx), active_path=active or None)
    }


def _m_image_models_download(params: dict[str, Any]) -> dict[str, Any]:
    """模型下载(异步 job,仿 sources.test 先例):提交即返,结果走两事件。

    ``repo`` 必须 ``mlx-community/<name>``(MLX 格式权重直下免 convert);
    ``name`` 缺省 = repo 名段。磁盘预检不足 / 网络失败都以
    ``image.models.completed {ok:false, error}` 收口(error = 结构化 code)。
    """
    global _MODELS_DL_ACTIVE_JOB, _MODELS_DL_NEXT_JOB_ID
    repo = params.get("repo")
    if not isinstance(repo, str) or not repo.strip():
        raise ProtocolError(
            "invalid_params", "缺少仓库全名 repo(mlx-community/<name>)", path="params.repo"
        )
    name = params.get("name")
    if name is not None and (not isinstance(name, str) or not name.strip()):
        raise ProtocolError("invalid_params", "name 必须是非空字符串或省略", path="params.name")
    repo = repo.strip()
    name = (name or "").strip() or None
    with _MODELS_DL_LOCK:
        if _MODELS_DL_ACTIVE_JOB is not None:
            raise ProtocolError(
                "download_busy",
                f"已有模型下载在执行 job_id={_MODELS_DL_ACTIVE_JOB}(单飞)",
                data={"active_job_id": _MODELS_DL_ACTIVE_JOB},
            )
        _MODELS_DL_NEXT_JOB_ID += 1
        job_id = _MODELS_DL_NEXT_JOB_ID
        _MODELS_DL_ACTIVE_JOB = job_id
    threading.Thread(
        target=_image_models_download_worker,
        args=(job_id, repo, name, _vision_models_root(_serve_context())),
        daemon=True,
    ).start()
    return {"job_id": job_id}


def _image_models_download_worker(
    job_id: int, repo: str, name: str | None, models_root: Path
) -> None:
    """后台线程:snapshot_download → 进度/完成事件(绝不阻塞 serve 循环)。"""
    global _MODELS_DL_ACTIVE_JOB

    def _on_progress(done_bytes: int, total_bytes: int | None) -> None:
        event: dict[str, Any] = {
            "type": "image.models.progress",
            "job_id": job_id,
            "repo": repo,
            "done_bytes": done_bytes,
        }
        if total_bytes is not None:
            event["total_bytes"] = total_bytes
        event["ts"] = _now_iso()
        _write_line(event)

    error: str | None = None
    try:
        try:
            vision_download_model(repo, models_root, name=name, on_progress=_on_progress)
        except VisionModelError as exc:
            error = exc.code
            myssia_log.stream_line(None, "stderr", f"sidecar: 模型下载失败 {repo}: [{exc.code}] {exc}")
        except Exception as exc:  # noqa: BLE001 — 事件必须可见,错误收口为完成事件
            error = type(exc).__name__
            myssia_log.stream_line(None, "stderr", f"sidecar: 模型下载未预期异常 {repo}: {exc}")
        completed: dict[str, Any] = {
            "type": "image.models.completed",
            "job_id": job_id,
            "ok": error is None,
            "ts": _now_iso(),
        }
        if error is not None:
            completed["error"] = error
        _write_line(completed)
    finally:
        with _MODELS_DL_LOCK:
            if _MODELS_DL_ACTIVE_JOB == job_id:
                _MODELS_DL_ACTIVE_JOB = None


def _m_image_models_delete(params: dict[str, Any]) -> dict[str, Any]:
    """删除模型目录(active 拒删——在用权重删除会让本地 VL 突然失效)。"""
    name = _require_model_name(params)
    ctx = _serve_context()
    active = _active_model_path(ctx)
    try:
        vision_delete_model(name, _vision_models_root(ctx), active_path=active or None)
    except VisionModelError as exc:
        raise ProtocolError(
            exc.code, str(exc), path="params.name", data=exc.to_dict()
        ) from exc
    return {"ok": True}


def _m_image_models_activate(params: dict[str, Any]) -> dict[str, Any]:
    """激活模型 = vision.yaml ``local.model`` 指向该目录(同门校验原子写)。"""
    name = _require_model_name(params)
    ctx = _serve_context()
    try:
        vision_activate_model(name, _vision_models_root(ctx), _vision_yaml_path(ctx))
    except VisionModelError as exc:
        raise ProtocolError(
            exc.code, str(exc), path="params.name", data=exc.to_dict()
        ) from exc
    except VisionConfigError as exc:  # 拒载/写失败零半载(activate 内同门)
        raise ProtocolError(
            "image_config_invalid", f"vision.yaml 改写失败,零写入: {exc}",
            path="params.name", data=exc.to_dict(),
        ) from exc
    return {"ok": True}


def _m_image_server_status(params: dict[str, Any]) -> dict[str, Any]:
    """本地 mlx_vlm.server 状态(base_url/models 2s 探;零副作用)。"""
    return vision_server_status(_load_vision(_serve_context()))


#: server ensure 单飞(应答立即返回,健康等待跑后台线程;10-03-vision-v2 复查:
#: serve 循环单线程,同步等 120s 健康窗会把桌面全协议冻成队头阻塞)。
_SERVER_ENSURE_LOCK = threading.Lock()
_SERVER_ENSURE_ACTIVE_JOB: int | None = None
_SERVER_ENSURE_NEXT_JOB_ID = 0


def _m_image_server_ensure(params: dict[str, Any]) -> dict[str, Any]:
    """确保本地 mlx_vlm.server 在跑:健康即返;否则后台自启,应答立即回。

    快路径(≤2s 快照探,与 status 同帽):已健康 → ``status + {started:false}``
    零后台零事件(冻结契约原样)。慢路径:起后台线程跑
    :func:`ensure_vision_server`(自启 + 健康等待 ≤120s / 并发互斥 / 超窗杀
    孤儿,纪律全在能力层),应答立即返回快照超集
    ``{running, base_url, model, healthy, started:false, ensuring:true, job_id}``,
    终态走 ``image.server.completed {job_id, ok, status?, error?, ts}`` 事件
    (ok 时 status = status+{started});并发第二单 = ``ensure_busy`` 结构化拒。
    子进程输出经统一日志管道落 ``<home>/logs/myssia-*.jsonl`` 的 proc=vision
    行(决议③;vision-server.log 已退役,见 vision/server.py)。
    """
    global _SERVER_ENSURE_ACTIVE_JOB, _SERVER_ENSURE_NEXT_JOB_ID
    ctx = _serve_context()
    config = _load_vision(ctx)
    snapshot = vision_server_status(config)  # ≤2s 快照(与 image.server.status 同帽)
    if snapshot["healthy"]:
        return {**snapshot, "started": False}
    with _SERVER_ENSURE_LOCK:
        if _SERVER_ENSURE_ACTIVE_JOB is not None:
            raise ProtocolError(
                "ensure_busy",
                f"已有确保启动在执行 job_id={_SERVER_ENSURE_ACTIVE_JOB}(单飞)",
                data={"active_job_id": _SERVER_ENSURE_ACTIVE_JOB},
            )
        _SERVER_ENSURE_NEXT_JOB_ID += 1
        job_id = _SERVER_ENSURE_NEXT_JOB_ID
        _SERVER_ENSURE_ACTIVE_JOB = job_id
    threading.Thread(
        target=_image_server_ensure_worker,
        args=(job_id, config, _vision_yaml_path(ctx).parent),
        daemon=True,
    ).start()
    return {**snapshot, "started": False, "ensuring": True, "job_id": job_id}


def _image_server_ensure_worker(job_id: int, config: VisionConfig, data_root: Path) -> None:
    """后台线程:ensure_vision_server → image.server.completed 事件(不阻 serve 循环)。"""
    global _SERVER_ENSURE_ACTIVE_JOB
    error: str | None = None
    status: dict[str, Any] | None = None
    try:
        status = ensure_vision_server(config, data_root=data_root)
    except VisionServerError as exc:
        error = exc.code
        myssia_log.stream_line(None, "stderr", f"sidecar: vision server ensure 失败: [{exc.code}] {exc}")
    except Exception as exc:  # noqa: BLE001 — 事件必须可见,错误收口为完成事件
        error = type(exc).__name__
        myssia_log.stream_line(None, "stderr", f"sidecar: vision server ensure 未预期异常: {exc}")
    completed: dict[str, Any] = {
        "type": "image.server.completed",
        "job_id": job_id,
        "ok": error is None,
        "ts": _now_iso(),
    }
    if error is not None:
        completed["error"] = error
    if status is not None:
        completed["status"] = status
    _write_line(completed)
    with _SERVER_ENSURE_LOCK:  # 对齐下载 worker:事件先发,单飞位后清
        if _SERVER_ENSURE_ACTIVE_JOB == job_id:
            _SERVER_ENSURE_ACTIVE_JOB = None


# ---------------------------------------------------------------------------
# 方法:image.files.purge(10-03-vision-v2 复查:落图零回收 —— 内容寻址只进
# 不出,给 CLI 面一个按 mtime 清 <数据根>/images 超龄文件的口;UI 不做)
# ---------------------------------------------------------------------------

#: 落图目录名(与管线侧 myssia.vision.collect.PERSIST_DIR_NAME 同名同位:
#: 数据根 ``images/``,home 模式 = <home>/images)。
IMAGE_FILES_DIR_NAME = "images"


def _m_image_files_purge(params: dict[str, Any]) -> dict[str, Any]:
    """按 mtime 清 ``<数据根>/images`` 下超龄落图 → ``{deleted, bytes_freed}``。

    ``days`` 整数 ≥1(按文件 mtime,< now-days*86400 即删);只删文件不动
    目录(管线落图 = 平铺内容寻址文件);单文件删除失败容忍跳过(竞态/占用
    不该让整次回收报错)。目录不存在 = 合法零删。零 UI(记录为 CLI 面能力)。
    """
    days = params.get("days")
    if not isinstance(days, int) or isinstance(days, bool) or days < 1:
        raise ProtocolError(
            "invalid_params", "缺少整数字段 days(≥1,按文件 mtime 清超龄落图)",
            path="params.days",
        )
    images_root = Path(_serve_context().db).expanduser().resolve().parent / IMAGE_FILES_DIR_NAME
    cutoff = datetime.now(timezone.utc).timestamp() - days * 86400
    deleted = 0
    bytes_freed = 0
    if images_root.is_dir():
        for candidate in sorted(images_root.rglob("*")):
            try:
                if not candidate.is_file() or candidate.stat().st_mtime >= cutoff:
                    continue
                size = candidate.stat().st_size
                candidate.unlink()
            except OSError:
                continue  # 竞态/权限:尽力而为,逐文件隔离
            deleted += 1
            bytes_freed += size
    return {"deleted": deleted, "bytes_freed": bytes_freed}


# ---------------------------------------------------------------------------
# 方法:channels.list / channels.refresh / channels.alias / push.write
# (消息屏协议,task 10-03-messaging-ui;契约钉死于任务档 design.md §D2,
#  TS 侧 ui-src/screens/messaging/api.ts 注释互指;能力实现在 myssia.push 包:
#  directory=通道目录+别名覆盖、delivery=死信账本;push 校验门=myssia.schema)
# ---------------------------------------------------------------------------

#: 单别名长度上限(防误贴长文本;发现名不受此限,只限手工别名)。
ALIAS_MAX_LEN = 120


def _messaging_root(ctx: ServeContext) -> Path:
    """消息数据根 = db 父目录(pipeline 同款:目录/别名/死信三文件同根)。"""
    return Path(ctx.db).expanduser().resolve().parent


def _push_rules_view(ctx: ServeContext) -> list[dict[str, Any]]:
    """品类 YAML 的 push 条目视图(消息屏下区规则面板数据源)。

    每文件 ``{file, category_id, category_name, parse_ok, error, entries}``;
    entries 每条 ``{index, channel, platform, targets, has_template,
    route_count, raw}``。platform 取 :data:`myssia.schema.CHANNEL_PLATFORMS`
    (webhook/stdout 不支持目录寻址 → None,UI 不给这类条目出 targets
    选择器)。**raw 是该条目的最小无损形态**(push.write 全量替换的写回
    base:UI 改 targets 后整文件提交)—— None 字段与 webhook 专属的
    timeout/retries 族不携带,保证 raw 原样回传能过 push.write 的
    load_category 同门(schema 对非 webhook 通道显式配置传输字段即拒)。
    坏文件 parse_ok=false + error 如实入列(与 yaml.list 同哲学:坏文件
    可看见才能被修)。
    """
    rules: list[dict[str, Any]] = []
    for path in _yaml_files(Path(ctx.plugins_dir)):
        item: dict[str, Any] = {
            "file": str(path),
            "category_id": None,
            "category_name": None,
            "parse_ok": False,
            "error": None,
            "entries": [],
        }
        try:
            config = load_category_file(path)
        except LoadError as exc:
            first = exc.errors[0]
            item["error"] = {"path": first.path, "code": first.error_type, "message": first.message}
            rules.append(item)
            continue
        item["parse_ok"] = True
        item["category_id"] = config.id
        item["category_name"] = config.name
        item["entries"] = [
            {
                "index": index,
                "channel": push.channel,
                "platform": CHANNEL_PLATFORMS.get(push.channel),
                "targets": list(push.targets),
                "has_template": push.template is not None,
                "route_count": len(push.route),
                "raw": _push_raw_dict(push),
            }
            for index, push in enumerate(config.push)
        ]
        rules.append(item)
    return rules


def _push_raw_dict(push: Any) -> dict[str, Any]:
    """PushConfig → 最小无损 dict(与 YAML 声明形态一致;push.write 可直收)。

    只携带显式声明的字段:None 的 target/template、空 targets、空 route
    都不出现 —— UI 原样回传时与「手写 YAML 的最小条目」等价,不引入
    schema 会拒的显式默认值(如非 webhook 通道的 timeout)。W2 平台可选
    凭据引用字段(10-03-messaging-w2-platforms)同理:显式声明才携带,
    回传经 load_category 同门校验(schema 保证只在宿主通道出现)。
    """
    raw: dict[str, Any] = {"channel": push.channel}
    if push.target is not None:
        raw["target"] = push.target
    if push.targets:
        raw["targets"] = list(push.targets)
    if push.template is not None:
        raw["template"] = push.template
    for field in (
        "ntfy_token",
        "dingtalk_secret",
        "wecom_corpid",
        "wecom_corpsecret",
        "wecom_agentid",
        "weixin_hermes_bin",
    ):
        value = getattr(push, field, None)
        if value is not None:
            raw[field] = value
    if push.route:
        raw["route"] = [
            {"when": rule.when, "mode": rule.mode, **({"targets": list(rule.targets)} if rule.targets else {})}
            for rule in push.route
        ]
    return raw


def _m_channels_list(params: dict[str, Any]) -> dict[str, Any]:
    """通道目录四视图:目录(platforms)+ 别名(aliases)+ 死信(dead)+ 规则(rules)。

    目录条目的 name 已套别名覆盖(:class:`ChannelDirectory` 加载期语义);
    aliases 是手工可编的原始覆盖层(UI 据此区分「发现名/手工别名」);
    dead 为死信键快照(``platform:chat_id``,UI 徽标用);rules 见
    :func:`_push_rules_view`。零平台 = 合法空态(UI 给「先配平台凭据」指引)。
    """
    ctx = _serve_context()
    root = _messaging_root(ctx)
    directory = ChannelDirectory(root)
    ledger = DeliveryLedger(root)
    platforms_view: dict[str, list[dict[str, Any]]] = {
        platform: [entry.to_dict() for entry in directory.entries(platform)]
        for platform in directory.platforms()
    }
    return {
        "data_root": str(root),
        "updated_at": directory.updated_at,
        "platforms": platforms_view,
        "aliases": directory.aliases_snapshot(),
        "dead": ledger.dead_keys(),
        "rules": _push_rules_view(ctx),
    }


def _m_channels_refresh(params: dict[str, Any]) -> dict[str, Any]:
    """单平台目录发现 → 桶替换 + 持久化;失败结构化上抛,旧桶不动。

    与 pipeline 懒刷(:func:`myssia.pipeline` run 前节流刷新)同一发现
    通道类、同一合并语义;差别只在错误处理 —— 推送路径吞错继续,UI 路径
    必须把凭据缺失/网络失败如实带回给用户。发现凭据 = 通道类缺省 env
    引用(``env:FEISHU_BOT_TOKEN`` 族;push 条目无 token 字段,run 时同源)。
    telegram 无目录发现 API(被动积累)→ ``discover_not_supported``。
    """
    platform_raw = params.get("platform")
    if not isinstance(platform_raw, str) or not platform_raw.strip():
        raise ProtocolError(
            "invalid_params", "缺少平台名 platform(如 feishu)", path="params.platform"
        )
    platform = platform_raw.strip()
    platform_cls = myssia_push.PLATFORMS.get(platform)
    if platform_cls is None:
        raise ProtocolError(
            "unknown_platform",
            f"未知平台 {platform!r}(已注册: {sorted(myssia_push.PLATFORMS)})",
            path="params.platform",
            data={"allowed": sorted(myssia_push.PLATFORMS)},
        )
    if not callable(getattr(platform_cls, "discover_directory", None)):
        raise ProtocolError(
            "discover_not_supported",
            f"平台 {platform} 无目录发现 API(telegram 靠入站观测被动积累,"
            "条目会随 bot 收到消息自动入目录;也可直接在规则里手写 targets)",
            path="params.platform",
        )
    adapter = platform_cls()
    try:
        discovered = adapter.discover_directory()
        entries = asyncio.run(discovered) if inspect.isawaitable(discovered) else discovered
    except DirectoryDiscoverUnsupported as exc:
        # W2 平台(ntfy/dingtalk/wecom,10-03-messaging-w2-platforms 蓝本事实):
        # 无自动发现是平台形态而非失败——与 telegram 被动积累同一错误族
        # (discover_not_supported),UI 据文案指引用户走直达 id / 别名登记。
        raise ProtocolError(
            "discover_not_supported",
            str(exc),
            path="params.platform",
            data={"platform": platform},
        ) from exc
    except PushSendError as exc:
        raise ProtocolError(
            "channel_refresh_failed",
            f"{platform} 目录发现失败,旧目录不动: [{exc.code}] {exc}",
            path="params.platform",
            data={"platform": platform, "code": exc.code},
        ) from exc
    except Exception as exc:  # noqa: BLE001 — 网络/协议异常同样结构化上抛,不裸穿
        raise ProtocolError(
            "channel_refresh_failed",
            f"{platform} 目录发现失败,旧目录不动: {type(exc).__name__}: {exc}",
            path="params.platform",
            data={"platform": platform},
        ) from exc
    ctx = _serve_context()
    bucket = ChannelDirectory(_messaging_root(ctx)).commit_platform_refresh(platform, entries)
    return {
        "platform": platform,
        "merged": len(bucket),
        "entries": [entry.to_dict() for entry in bucket],
    }


def _m_channels_alias(params: dict[str, Any]) -> dict[str, Any]:
    """别名 set / delete(payload 区分:name 非空 = set,null/空串 = delete)。

    写入走 :meth:`ChannelDirectory.set_alias`(别名文件原子覆盖 + 内存态
    立即生效);set_alias 是核心侧 best-effort(写失败不阻塞推送),UI 写
    路径必须确认落盘 —— 重读别名文件对照,未生效即结构化报错,零静默。
    """
    platform_raw = params.get("platform")
    chat_raw = params.get("chat_id")
    name = params.get("name")
    if not isinstance(platform_raw, str) or not platform_raw.strip():
        raise ProtocolError("invalid_params", "缺少平台名 platform", path="params.platform")
    if not isinstance(chat_raw, str) or not chat_raw.strip():
        raise ProtocolError("invalid_params", "缺少会话 id chat_id", path="params.chat_id")
    deleting = name is None or (isinstance(name, str) and not name.strip())
    cleaned = ""
    if not deleting:
        if not isinstance(name, str):
            raise ProtocolError(
                "invalid_params", "name 必须是非空字符串(设置)或 null(删除)", path="params.name"
            )
        cleaned = name.strip()
        if len(cleaned) > ALIAS_MAX_LEN:
            raise ProtocolError(
                "invalid_params", f"别名超长(>{ALIAS_MAX_LEN} 字符)", path="params.name"
            )
    platform, chat_id = platform_raw.strip(), chat_raw.strip()
    ctx = _serve_context()
    root = _messaging_root(ctx)
    ChannelDirectory(root).set_alias(platform, chat_id, cleaned)
    persisted = ChannelDirectory(root).aliases_snapshot().get(platform, {})
    if deleting:
        applied = chat_id not in persisted
    else:
        applied = persisted.get(chat_id) == cleaned
    if not applied:
        raise ProtocolError(
            "alias_write_failed",
            f"别名写入未生效(检查数据根可写性): {root}",
            path="params",
            data={"platform": platform, "chat_id": chat_id},
        )
    return {"platform": platform, "chat_id": chat_id, "deleted": deleting, "name": cleaned or None}


def _m_bridge_status(params: dict[str, Any]) -> dict[str, Any]:
    """微信桥接探测(#28,10-03-messaging-weixin-bridge design D4)。

    result = :func:`myssia.push.weixin.probe_bridge` 全量(BridgeStatus 七键:
    available/reason/fix_hint/bin_found/weixin_configured/gateway_alive/
    bin_path)。纯文件系统存在性探测(永不读 Hermes 私有文件内容),
    无凭据、无出网、无入站;bin 路径取品类 YAML 首个 weixin 条目的
    ``weixin_hermes_bin`` 覆写(design D2),缺省 DEFAULT_HERMES_BIN。
    prd R2:UI 灰卡据此如实披露「需本机 Hermes」,不装可用。
    """
    ctx = _serve_context()
    hermes_bin: str | None = None
    for path in _yaml_files(Path(ctx.plugins_dir)):
        try:
            config = load_category_file(path)
        except LoadError:
            continue  # 坏文件不阻塞探测(yaml.list 会如实展示其错误)
        for push in config.push:
            if push.channel == "weixin" and push.weixin_hermes_bin:
                hermes_bin = push.weixin_hermes_bin
                break
        if hermes_bin:
            break
    return probe_bridge(hermes_bin).to_payload()


#: push.write 重序列化行宽(官方 YAML 阅读宽一致;模板长行不被硬拆)。
_PUSH_DUMP_WIDTH = 100

#: 顶层 push 块形态键行(nil 值,条目在后续缩进行)。
_PUSH_BLOCK_KEY_RE = re.compile(r"^push:\s*(#.*)?$")
#: 顶层 push 单行流式形态(``push: []``)键行。
_PUSH_FLOW_KEY_RE = re.compile(r"^push:\s*\[.*\]\s*(#.*)?$")


class _PushEntryDumper(yaml.SafeDumper):
    """push 条目重序列化:多行字符串(模板)优先 literal 块形态,保模板可读。

    PyYAML 缺省把多行字符串转义成双引号单行(语义无损但人不可读);literal
    块(``|``)与官方品类 YAML 的 ``template: |`` 写法一致。字符串含尾随
    空格等 literal 不可表示形态时,emitter 自动回落引号风格(不丢信息)。
    """


def _represent_str_literal(dumper: yaml.Dumper, data: str) -> Any:
    style = "|" if "\n" in data else None
    return dumper.represent_scalar("tag:yaml.org,2002:str", data, style=style)


_PushEntryDumper.add_representer(str, _represent_str_literal)


def _dump_push_entries(entries: list[Any]) -> list[str]:
    """新 push 数组 → 缩进 2 的 YAML 条目行(不含 ``push:`` 键行,尾随一空行)。

    缩进 2 与官方品类 YAML 的 ``  - channel: …`` 序列风格一致;sort_keys=False
    保持调用方给的键序(UI 提交的是「原条目 + 改过的 targets」)。
    """
    dumped = yaml.dump(
        entries,
        Dumper=_PushEntryDumper,
        allow_unicode=True,
        sort_keys=False,
        default_flow_style=False,
        width=_PUSH_DUMP_WIDTH,
    )
    return [f"  {line}\n" for line in dumped.splitlines()] + ["\n"]


def _push_section_span(lines: list[str]) -> tuple[int, int] | None:
    """定位顶层 push 节区间 ``(起点, 排他终点)``;无 push 键行 → None。

    块形态(``push:`` nil 值):终点 = 下一个列 0 非注释非空行或 EOF(块尾
    空行归区间内,随替换归一为一个空行分隔);单行流式(``push: []``):
    区间即该行。多行流式/键带锚点不在此命中 —— 由调用方按「doc 有 push 而
    文本定位不到」结构化拒写(不做静默猜测,零写入)。
    """
    for i, line in enumerate(lines):
        body = line.rstrip("\r\n")
        if _PUSH_BLOCK_KEY_RE.match(body):
            end = len(lines)
            for j in range(i + 1, len(lines)):
                nxt = lines[j].rstrip("\r\n")
                if nxt and not nxt[0].isspace() and not nxt.startswith("#"):
                    end = j
                    break
            return i, end
        if _PUSH_FLOW_KEY_RE.match(body):
            return i, i + 1
    return None


def _m_push_write(params: dict[str, Any]) -> dict[str, Any]:
    """push[] 全量替换写回:围栏 → 文本手术只换 push 块 → 双门 → ``.bak`` → 原子写。

    契约(design.md §D2):``{file, push}`` 的 push 是**该文件的完整 push
    数组**(UI 侧「编辑一条提交整个数组」,与 sources.write 的文件作用域
    一致)。手术在原文上只动 push 节(块尾/EOF 追加/整节摘除三形),其余
    行(节间注释、行内注释、引号风格)逐字节不动 —— 与 sources.write 的
    文本手术同一保真哲学,绝不做整文件 safe_dump 重写。两道门:手术结果
    反解析必须与「原文档 + 新 push」深等(防波及 push 之外);再过
    :func:`load_category`(``myssia run`` 同门,含 targets 格式与同平台
    约束)—— 任一失败原样透传结构化错误,零写入。空数组 = 摘除 push 节
    (品类允许无 push,条目仅入库);文件本就无 push 节且新数组空 = 无操作
    (changed=false,不落盘)。
    """
    push_raw = params.get("push")
    if not isinstance(push_raw, list):
        raise ProtocolError(
            "invalid_params", "缺少完整 push 数组 push(list,空数组=摘除 push 节)", path="params.push"
        )
    resolved, ctx = _fence_yaml_path(params.get("file"))
    if not resolved.exists():
        raise ProtocolError("file_not_found", f"文件不存在: {resolved}", path="params.file")
    try:
        stat = resolved.stat()
        if stat.st_size > YAML_MAX_BYTES:
            raise ProtocolError(
                "file_too_large",
                f"文件超过 1 MiB 上限: {stat.st_size} 字节(limit={YAML_MAX_BYTES})",
                path="params.file",
                data={"size": stat.st_size, "limit": YAML_MAX_BYTES},
            )
        with open(resolved, encoding="utf-8", newline="") as handle:
            original = handle.read()
    except FileNotFoundError as exc:
        raise ProtocolError("file_not_found", f"文件不存在: {resolved}", path="params.file") from exc
    except UnicodeDecodeError as exc:
        raise ProtocolError(
            "invalid_encoding",
            f"文件不是有效的 UTF-8 编码: {resolved} ({exc});请转存 UTF-8 后重试",
            path="params.file",
        ) from exc
    except OSError as exc:
        raise ProtocolError(
            "source_file_unreadable", f"品类 YAML 不可读: {resolved} ({exc})", path="params.file"
        ) from exc
    try:
        doc = yaml.load(original, Loader=_UniqueKeyLoader)
    except yaml.YAMLError as exc:
        raise ProtocolError(
            "category_invalid", f"品类 YAML 不是合法 YAML: {exc}", path="params.file"
        ) from exc
    if not isinstance(doc, dict) or not isinstance(doc.get("sources"), list):
        raise ProtocolError(
            "category_invalid", f"{resolved} 不是品类 YAML(缺少 sources 节)", path="params.file"
        )

    # -- 文本手术:三形(替换块 / EOF 追加 / 摘除),定位不到才拒 ------------
    lines = _split_keep_lines(original)
    span = _push_section_span(lines)
    if span is None and "push" in doc:
        raise ProtocolError(
            "push_write_unsupported",
            f"push 节形态不支持文本手术(多行流式/锚点,零写入): {resolved}",
            path="params.file",
        )
    changed = True
    if push_raw:
        block = ["push:\n", *_dump_push_entries(push_raw)]
        if span is None:  # 文件无 push 节:EOF 追加(空行与前节分隔)
            if lines and not lines[-1].endswith("\n"):
                lines[-1] += "\n"
            if not lines or not _toggle_is_blank(lines[-1]):
                lines.append("\n")
            lines.extend(block)
        else:
            start, end = span
            lines[start:end] = block
    elif span is not None:
        start, end = span
        del lines[start:end]  # 空数组 = 整节摘除(块尾空行随区间走)
    else:
        changed = False  # 本就无 push 节,空数组 = 无操作
    new_text = "".join(lines)

    # -- 门一:手术结果反解析与「原文档 + 新 push」深等(零写入)------------
    expected = dict(doc)
    if push_raw:
        expected["push"] = push_raw
    else:
        expected.pop("push", None)
    try:
        reread = yaml.safe_load(new_text)
    except yaml.YAMLError as exc:
        raise ProtocolError(
            "push_write_unsupported",
            f"push 块替换结果不再是合法 YAML(零写入): {resolved} ({exc})",
            path="params.file",
        ) from exc
    if reread != expected:
        raise ProtocolError(
            "push_write_unsupported",
            f"push 块替换波及了 push 之外的内容(疑为未支持结构的漏网形态,零写入): {resolved}",
            path="params.file",
        )

    # -- 门二:myssia run 同门装载校验(targets 格式/同平台约束在此拦)---------
    try:
        load_category(reread, source=str(resolved))
    except LoadError as exc:
        details = [
            {"path": item.path, "code": item.error_type, "message": item.message}
            for item in exc.errors
        ]
        raise ProtocolError(
            "category_invalid",
            f"写回后的 push 配置未过品类校验: {details}",
            path="params.push",
            data={"errors": details},
        ) from exc

    if not changed:
        return {"file": str(resolved), "written": True, "changed": False, "push": list(push_raw)}
    backed_up: str | None = None
    try:
        bak = resolved.with_suffix(resolved.suffix + ".bak")
        shutil.copy2(resolved, bak)
        backed_up = str(bak)
        _atomic_write_text(resolved, new_text)
    except OSError as exc:
        raise ProtocolError("source_write_failed", f"写回失败: {exc}", path="params.file") from exc
    return {
        "file": str(resolved),
        "written": True,
        "changed": True,
        "backed_up": backed_up,
        "push": list(expected.get("push") or []),
    }


# ---------------------------------------------------------------------------
# 方法:push.test(推送通道连通性测试;G5 前半,10-03-feed-ux)
# ---------------------------------------------------------------------------


def _m_push_test(params: dict[str, Any]) -> dict[str, Any]:
    """合成单条测试条目走既有通道 ``send(items, context)`` —— **真发消息**。

    ``channel`` ∈ :data:`myssia.push.CHANNELS`(通道名与品类 YAML ``push[]``
    同一注册表);``target`` 可选 ``env:``/``keychain:`` 凭据引用(设置屏
    表单的 scope/secretName 组合出 ``keychain:myia/<scope>/<name>``),
    缺省走通道默认 env 引用链 —— 凭据缺失/发送失败沿用通道既有结构化
    错误分类直传(PushSendError code 原文,design §1)。

    ``stdout`` 通道特殊处理:serve 模式 stdout 是协议流,卡片行改写入
    内存缓冲并随应答 ``preview`` 字段回显(同 ``Pipeline._build_channel``
    的 ``--json`` 模式 ``out`` 注入先例),协议流零污染。
    """
    channel_name = params.get("channel")
    if not isinstance(channel_name, str) or channel_name not in myssia_push.CHANNELS:
        raise ProtocolError(
            "invalid_params",
            f"channel 必须是 {sorted(myssia_push.CHANNELS)} 之一",
            path="params.channel",
        )
    target = params.get("target")
    if target is not None and (not isinstance(target, str) or not target):
        raise ProtocolError(
            "invalid_params", "target 必须为非空凭据引用(env:/keychain:)", path="params.target"
        )
    template = params.get("template")
    if template is not None and not isinstance(template, str):
        raise ProtocolError("invalid_params", "template 必须为字符串", path="params.template")

    kwargs: dict[str, Any] = {}
    if target is not None:
        kwargs["target"] = target
    if template is not None:
        kwargs["template"] = template
    preview_io: io.StringIO | None = None
    if channel_name == "stdout":
        # serve 模式 stdout = 协议流:卡片行入内存缓冲,应答 preview 回显
        preview_io = io.StringIO()
        kwargs["out"] = preview_io
    channel = myssia_push.CHANNELS[channel_name](**kwargs)

    now = datetime.now()
    item = {
        "url": "https://example.com/myssia-push-test",
        "dedup_key": f"myssia-push-test-{now.strftime('%Y%m%d%H%M%S')}",
        "title": f"MYIA 推送测试({now.strftime('%Y-%m-%d %H:%M:%S')})",
        "source": "myia",
        "category": None,
    }
    context = myssia_push.SendContext(
        slot="am" if now.hour < 12 else "pm",
        date=now.strftime("%Y-%m-%d"),
        category=None,
        kind="immediate",
    )
    try:
        asyncio.run(channel.send([item], context))
    except PushSendError as exc:
        # 通道契约:凭据缺失/模板/传输/API 失败一律结构化 PushSendError(code 原文直传)
        raise ProtocolError(exc.code, str(exc), path="params.channel") from exc
    preview = preview_io.getvalue() if preview_io is not None else None
    return {"ok": True, "channel": channel_name, **({"preview": preview} if preview else {})}


# ---------------------------------------------------------------------------
# 方法:alerts.list / alerts.save / alerts.delete / alerts.test
# (10-04-alert-rules Stage D:告警规则桌面管理面;引擎 = src/myssia/alerts,
# 管线挂点 = Pipeline._alert_pass,契约钉死于任务档 design.md §4)
# ---------------------------------------------------------------------------

#: AlertRuleInput 载荷的合法键(schema 铁律:未知字段不许静默忽略)。kind/
#: params 是心跳规则(10-05-cron-heartbeat)的加法可选键:语义校验(越表/
#: cron_stale 形状/item 带 params 拒)走下方同一道 ``compile_rule`` 构造门。
_ALERT_RULE_INPUT_KEYS = frozenset(
    {"id", "name", "when", "action", "action_config", "scope", "enabled", "kind", "params"}
)

#: AlertConfigError 消息里的字段名抽取(``字段校验失败: <字段> 必须是/无效/
#: 不能为空/含未知键 …``,myssia.alerts.rule 文案族);抽不中兜底整表名。
_ALERT_FIELD_RE = re.compile(r"字段校验失败:\s*(.+?)\s+(?:必须是|无效|不能为空|含未知键)")


def _alert_rule_invalid(index: int | None, reason: str, *, path: str,
                        field: str | None = None) -> ProtocolError:
    """构造期拒 → 结构化 ``alert_rule_invalid``(design §10:data 三键)."""
    match = _ALERT_FIELD_RE.match(reason)
    return ProtocolError(
        "alert_rule_invalid",
        f"告警规则无效: {reason}" if index is None else f"告警规则第 {index} 条无效: {reason}",
        path=path,
        data={
            "index": index,
            "field": field or (match.group(1) if match else "alert_rules"),
            "reason": reason,
        },
    )


def _alert_rule_from_payload(raw: Any, index: int | None, *, path: str) -> AlertRule:
    """AlertRuleInput 载荷 → :class:`AlertRule`(类型门 + 构造门,零落库).

    类型形状错与语义错(``compile_rule``:scope/when 白名单语法/action/
    action_config 形状)同报 ``alert_rule_invalid``——都是「这一条规则无效,
    整批零写入」的构造期拒(写库门与读库门共用,myssia.alerts.rule)。
    """
    if not isinstance(raw, dict):
        raise _alert_rule_invalid(
            index, f"告警规则必须是对象,得到 {type(raw).__name__}", path=path, field="rule"
        )
    unknown = sorted(set(raw) - _ALERT_RULE_INPUT_KEYS)
    if unknown:
        raise _alert_rule_invalid(
            index, f"告警规则含未知键 {unknown}(允许 {sorted(_ALERT_RULE_INPUT_KEYS)})",
            path=path, field=unknown[0],
        )
    rule_id = raw.get("id")
    if rule_id is not None and (isinstance(rule_id, bool) or not isinstance(rule_id, int)):
        raise _alert_rule_invalid(index, f"id 必须为整数,得到 {rule_id!r}", path=path, field="id")
    name = raw.get("name")
    if not isinstance(name, str) or not name.strip():
        raise _alert_rule_invalid(index, f"name 必须为非空字符串,得到 {name!r}", path=path, field="name")
    when = raw.get("when")
    if not isinstance(when, str) or not when.strip():
        raise _alert_rule_invalid(index, f"when 必须为非空表达式字符串,得到 {when!r}",
                                  path=path, field="when")
    action = raw.get("action")
    if not isinstance(action, str):
        raise _alert_rule_invalid(index, f"action 必须为字符串,得到 {action!r}",
                                  path=path, field="action")
    action_config = raw.get("action_config")
    if action_config is None:
        action_config = {}
    if not isinstance(action_config, dict):
        raise _alert_rule_invalid(
            index, f"action_config 必须是键值映射,得到 {type(action_config).__name__}",
            path=path, field="action_config",
        )
    scope = raw.get("scope")
    if scope is None:
        scope = "global"
    if not isinstance(scope, str):
        raise _alert_rule_invalid(index, f"scope 必须为字符串,得到 {scope!r}", path=path, field="scope")
    enabled = raw.get("enabled")
    if enabled is None:
        enabled = True
    if not isinstance(enabled, bool):
        raise _alert_rule_invalid(index, f"enabled 必须为布尔,得到 {enabled!r}",
                                  path=path, field="enabled")
    # kind/params(10-05-cron-heartbeat 加法可选):这里只做类型形状门,
    # 语义门(kind 越表/cron_stale 形状/item 带 params 拒)统一走下方
    # compile_rule——与读库路径共用同一道构造门,零第二实现。
    kind = raw.get("kind")
    if kind is None:
        kind = ALERT_RULE_KIND_ITEM
    if not isinstance(kind, str):
        raise _alert_rule_invalid(index, f"kind 必须为字符串,得到 {kind!r}", path=path, field="kind")
    params = raw.get("params")
    if params is not None and not isinstance(params, dict):
        raise _alert_rule_invalid(
            index, f"params 必须是键值映射或 null,得到 {type(params).__name__}",
            path=path, field="params",
        )
    rule = AlertRule(
        id=rule_id, name=name, when=when, action=action,
        action_config=action_config, scope=scope, enabled=enabled,
        kind=kind, params=params,
    )
    try:
        compile_rule(rule)
    except AlertConfigError as exc:
        raise _alert_rule_invalid(index, str(exc), path=path) from exc
    return rule


def _alert_rule_views(store: SQLiteStore, rules: list[Any]) -> list[dict[str, Any]]:
    """AlertRule 行 → 视图(全字段 + fired_count/last_fired_at 派生,design §4.1)."""
    counts = store.fired_counts()
    views: list[dict[str, Any]] = []
    for rule in rules:
        latest = store.list_fired(rule_id=rule.id, limit=1) if rule.id else []
        views.append({
            "id": rule.id,
            "name": rule.name,
            "enabled": rule.enabled,
            "scope": rule.scope,
            "when": rule.when,
            "action": rule.action,
            "action_config": rule.action_config,
            # 心跳规则(10-05-cron-heartbeat)随全字段透传:旧壳不传 kind/
            # params 的载荷 = item 语义零漂移;新 UI 按回显渲染心跳表单。
            "kind": rule.kind,
            "params": rule.params,
            "created_at": rule.created_at.isoformat() if rule.created_at else None,
            "updated_at": rule.updated_at.isoformat() if rule.updated_at else None,
            "fired_count": counts.get(rule.id or -1, 0),
            "last_fired_at": (
                latest[0].created_at.isoformat() if latest and latest[0].created_at else None
            ),
        })
    return views


def _m_alerts_list(params: dict[str, Any]) -> dict[str, Any]:
    """告警规则清单(全量,id 升序;启用/停用同行返回——启停 = save 全量提交)."""
    db = params.get("db") or _serve_context().db
    try:
        store = SQLiteStore(db)
    except StoreSchemaError as exc:
        raise ProtocolError(exc.code, str(exc), path="params.db", data=exc.details) from exc
    try:
        rules = store.list_alert_rules()
        return {"db": str(db), "count": len(rules), "rules": _alert_rule_views(store, rules)}
    finally:
        store.close()


def _m_alerts_save(params: dict[str, Any]) -> dict[str, Any]:
    """``alerts.save``:规则**全量替换**(design §4.1 钉死①;push.write 先例).

    ``{rules: [AlertRuleInput]}`` 的 rules 是规则表的完整数组——承建/改/
    启停不设独立方法,编辑一条提交整个数组。两道门:①逐条过构造门
    (:func:`_alert_rule_from_payload` 类型门 + ``compile_rule`` 语义门),
    任一条失败 → ``alert_rule_invalid`` **整批零写入**;②全批构造成功后
    diff 落库——带 id = 更新保 id(id 稳定是 fired_count 派生的前提),
    不带 = 新建,库中多余 id = 删除(fired 历史照留,命中历史是事实)。
    空数组 = 清空规则表(回到零惊扰默认)。
    """
    rules_raw = params.get("rules")
    if not isinstance(rules_raw, list):
        raise ProtocolError(
            "invalid_params", "缺少完整规则数组 rules(list,空数组=清空规则表)", path="params.rules"
        )
    db = params.get("db") or _serve_context().db
    try:
        store = SQLiteStore(db)
    except StoreSchemaError as exc:
        raise ProtocolError(exc.code, str(exc), path="params.db", data=exc.details) from exc
    try:
        # 门一:全批先构造(零写入)——任一条失败整批拒
        incoming = [
            _alert_rule_from_payload(raw, index, path="params.rules")
            for index, raw in enumerate(rules_raw)
        ]
        # 门二:diff 落库(先删多余,再按载荷序更新/新建)
        existing_ids = {rule.id for rule in store.list_alert_rules()}
        incoming_ids = {rule.id for rule in incoming if rule.id is not None}
        for stale_id in sorted(existing_ids - incoming_ids):
            store.delete_alert_rule(stale_id)
        saved = []
        for rule in incoming:
            try:
                saved.append(store.save_alert_rule(rule))
            except ValueError as exc:
                if rule.id is not None and "不存在" in str(exc):
                    raise ProtocolError(
                        "alert_not_found", f"告警规则不存在: id={rule.id}",
                        path="params.rules", data={"id": rule.id},
                    ) from exc
                raise _alert_rule_invalid(
                    incoming.index(rule), str(exc), path="params.rules"
                ) from exc
        return {"db": str(db), "ok": True, "rules": _alert_rule_views(store, saved)}
    finally:
        store.close()


def _m_alerts_delete(params: dict[str, Any]) -> dict[str, Any]:
    """``alerts.delete {id}``:删定义行,fired 历史照留(命中历史是事实)."""
    rule_id = params.get("id")
    if isinstance(rule_id, bool) or not isinstance(rule_id, int):
        raise ProtocolError("invalid_params", "缺少规则 id(整数)", path="params.id")
    db = params.get("db") or _serve_context().db
    try:
        store = SQLiteStore(db)
    except StoreSchemaError as exc:
        raise ProtocolError(exc.code, str(exc), path="params.db", data=exc.details) from exc
    try:
        if not store.delete_alert_rule(rule_id):
            raise ProtocolError(
                "alert_not_found", f"告警规则不存在: id={rule_id}",
                path="params.id", data={"id": rule_id},
            )
        return {"ok": True, "id": rule_id}
    finally:
        store.close()


def _alert_test_synthetic_item(raw: dict[str, Any]) -> Item:
    """合成条目 dict → :class:`Item`(``Item.from_extracted`` 同门,design §4.1).

    ``title/content/source/url/category/scores/metadata`` 任意子集;url 缺省
    合成占位(from_extracted 的 url 门不因此拒——身份仅用于 already_fired
    预查与展示)。``category``/``scores``/``metadata`` 落 Item 顶层/合并进
    metadata(from_extracted 只认 url/title/source/content 四键)。
    """
    fields = dict(raw)
    if not isinstance(fields.get("url"), str) or not fields["url"].strip():
        fields["url"] = (
            "https://example.com/myssia-alert-test/"
            + datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S%f")
        )
    item = Item.from_extracted(
        {key: value for key, value in fields.items()
         if key not in ("category", "scores", "metadata")},
        source=fields.get("source") if isinstance(fields.get("source"), str) else None,
    )
    if "category" in fields:
        item.category = fields["category"]
    if "scores" in fields:
        item.scores = fields["scores"]
    if isinstance(fields.get("metadata"), dict):
        item.metadata.update(fields["metadata"])
    return item


def _alert_item_from_record(record: Any) -> Item:
    """库内条目(:class:`ItemRecord`)→ 求值同门 Item(design §5.2 上下文).

    metadata 种自 ``items.raw``(pipeline 以 raw=item.metadata 入库)并回填
    tags 行列;content/scores/category/dedup_key 按行列还原——与引擎
    ``alert_view`` 的求值上下文同形。
    """
    metadata: dict[str, Any] = dict(record.raw) if isinstance(record.raw, Mapping) else {}
    if record.tags:
        metadata.setdefault("tags", list(record.tags))
    return Item(
        url=record.url,
        title=record.title,
        source=record.source,
        category=record.category,
        scores=record.scores,
        dedup_key=record.dedup_key,
        content=record.content,
        metadata=metadata,
    )


def _alert_test_actions(compiled: CompiledAlertRule, config: Any, category: Any) -> list[dict[str, Any]]:
    """将触发的动作展开(dry,不真发;design §4.1:push 通道解析结果 + 降级原因).

    push 的通道解析与引擎 ``_resolve_alert_channel`` 同语义:当前品类
    ``push[]`` 内该类型第一条(禁止跨品类借凭据)——dry 测试只展开解析结果,
    不构建通道实例、不发送。真发测试借既有 ``push.test``。
    """
    rule = compiled
    if rule.rule.action == "tag":
        return [{"action": "tag", "tags": list(rule.tags)}]
    entry: dict[str, Any] = {"action": "push", "channel": rule.channel}
    if not isinstance(category, str) or not category:
        return [{**entry, "resolved": False, "degrade_reason": "item_no_category"}]
    if config is None:
        return [{**entry, "resolved": False, "degrade_reason": "category_yaml_not_found"}]
    for push in config.push:
        if push.channel == rule.channel:
            resolved = {**entry, "resolved": True, "resolved_target": push.target}
            if push.template is not None:
                resolved["resolved_template"] = push.template
            if rule.targets:
                resolved["targets"] = list(rule.targets)
            if rule.template is not None:
                resolved["template"] = rule.template
            return [resolved]
    return [{**entry, "resolved": False, "degrade_reason": "category_push_missing"}]


def _m_alerts_test(params: dict[str, Any]) -> dict[str, Any]:
    """``alerts.test``:**dry 求值,不真发不落 fired**(design §4.1 钉死②).

    ``rule``(草稿,未保存即可测)与 ``rule_id``(已存规则)二选一;
    ``item``(合成字段 dict)、``item_id``(库内条目,求值上下文与引擎同门)
    二选一,两者都缺 = 取最近一条(空库 → ``alert_test_no_item``)。
    应答 ``{matched, muted, actions, eval_error?, already_fired?}``:
    ``muted`` = 该条目按当前 effective mute(品类 watchlist + 反馈 0.0
    权重词,与 ``Pipeline._effective_watchlist`` 同门)是否被压制——命中
    mute 即未命中(matched=false,不评估,引擎硬规则);``eval_error`` =
    求值期错误如实上报(引擎运行期 WARNING+未命中的同款事实);``already_fired``
    仅 rule_id 形态携带;``actions`` = 将触发的动作展开(push 通道解析 +
    降级原因 / tag 标签)。真发测试借既有 ``push.test``。
    """
    rule_raw = params.get("rule")
    rule_id = params.get("rule_id")
    if rule_raw is not None and rule_id is not None:
        raise ProtocolError("invalid_params", "rule(草稿)与 rule_id(已存规则)二选一", path="params.rule")
    if rule_raw is None and rule_id is None:
        raise ProtocolError("invalid_params", "缺少规则引用 rule(草稿)或 rule_id(已存规则)", path="params.rule")
    item_raw = params.get("item")
    item_id = params.get("item_id")
    if item_raw is not None and item_id is not None:
        raise ProtocolError("invalid_params", "item(合成条目)与 item_id(库内条目)二选一", path="params.item")
    if item_raw is not None and not isinstance(item_raw, dict):
        raise ProtocolError("invalid_params", "item 必须是合成字段对象(title/content/source/url/category/scores/metadata 任意子集)", path="params.item")
    if item_raw is not None:
        for key, value in item_raw.items():
            if key == "category" and value is not None and not isinstance(value, str):
                raise ProtocolError("invalid_params", "item.category 必须为字符串或 null", path="params.item.category")
            if key == "scores" and value is not None and not isinstance(value, dict):
                raise ProtocolError("invalid_params", "item.scores 必须为对象或 null", path="params.item.scores")
            if key == "metadata" and value is not None and not isinstance(value, dict):
                raise ProtocolError("invalid_params", "item.metadata 必须为对象", path="params.item.metadata")
    if item_id is not None and (isinstance(item_id, bool) or not isinstance(item_id, int)):
        raise ProtocolError("invalid_params", "item_id 必须为整数(items.id)", path="params.item_id")

    ctx = _serve_context()
    db = params.get("db") or ctx.db
    try:
        store = SQLiteStore(db)
    except StoreSchemaError as exc:
        raise ProtocolError(exc.code, str(exc), path="params.db", data=exc.details) from exc
    try:
        # 规则取材:草稿过同一道构造门;rule_id 读库(未知 → alert_not_found)
        if rule_raw is not None:
            rule = _alert_rule_from_payload(rule_raw, None, path="params.rule")
        else:
            assert rule_id is not None  # 上方互斥门保证
            stored = [r for r in store.list_alert_rules() if r.id == rule_id]
            if not stored:
                raise ProtocolError(
                    "alert_not_found", f"告警规则不存在: id={rule_id}",
                    path="params.rule_id", data={"id": rule_id},
                )
            rule = stored[0]
        # 条目取材三分:合成 dict / items.id / 最近一条(空库 → alert_test_no_item)
        if item_raw is not None:
            item = _alert_test_synthetic_item(item_raw)
        elif item_id is not None:
            record = store.get_item(item_id)
            if record is None:
                raise ProtocolError(
                    "item_not_found", f"条目不存在: item_id={item_id}",
                    path="params.item_id", data={"item_id": item_id},
                )
            item = _alert_item_from_record(record)
        else:
            latest = store.list_items(limit=1)
            if not latest:
                raise ProtocolError(
                    "alert_test_no_item",
                    "库内无条目且未传 item/item_id,缺省取最近一条失败",
                    path="params.item", data={},
                )
            item = _alert_item_from_record(latest[0])

        # mute 词表:品类 watchlist + 反馈 0.0 权重词(_effective_watchlist 同门)
        config = _category_config_for_item(item.category, ctx.plugins_dir)
        tuning = load_active_tuning(store)
        mute_words = list(config.watchlist.mute) if config is not None else []
        for word in tuning.effective_mute_words():
            if word not in mute_words:
                mute_words.append(word)
        muted = mute_hit(item.title, mute_words) is not None

        try:
            compiled = compile_rule(rule)
        except AlertConfigError as exc:  # 读库坏行(草稿形态已在构造门拦下)
            raise _alert_rule_invalid(None, str(exc), path="params.rule") from exc
        view = alert_view(item)
        result: dict[str, Any] = {"matched": False, "muted": muted, "actions": []}
        if not muted and compiled.applies_to_scope(view.get("category")):
            try:
                result["matched"] = bool(evaluate_expression(rule.when, view))
            except RuleEvalError as exc:
                result["eval_error"] = str(exc)  # 求值错:引擎 WARNING+未命中,dry 如实上报
        if rule_id is not None:
            result["already_fired"] = store.has_fired(rule_id, item.dedup_key or item.url)
        result["actions"] = _alert_test_actions(compiled, config, item.category)
        return result
    finally:
        store.close()


# ---------------------------------------------------------------------------
# 方法:cron.* + serve 内置 ticker
# (10-04-hermes-cron B3:桌面 sidecar 的定时任务面。能力 = myssia.cron 包,
# 与 CLI ``myssia cron`` 同一 API 层(AC7);蓝本 Hermes cron/(MIT)的 gateway
# 内嵌 cron 等价物——多宿主(tick 文件锁 + fire claim 互斥)照抄)
# ---------------------------------------------------------------------------

#: serve 内置 cron ticker 的 tick 间隔秒(ticker.py 缺省 60s;测试注入小值)。
CRON_TICK_INTERVAL_SECONDS: float = DEFAULT_TICK_INTERVAL_SECONDS
#: 心跳新鲜度判定窗(CLI ``cron status`` 同款公式:interval×3 + 20s)。
_CRON_TICKER_FRESH_SECONDS: float = DEFAULT_TICK_INTERVAL_SECONDS * 3 + 20

_CRON_TICKER_LOCK = threading.Lock()
#: ticker 句柄(SupervisedTickerThread,F2.2 同款监督线程);测试夹具拆线防
#: 线程泄漏(B12)。
_CRON_TICKER: SupervisedTickerThread | None = None
#: 宿主监督线程(周期 restart_if_dead;serve 线程阻塞在 readline 承担不了
#: ticker.py 契约里的宿主监督职责,由本专职线程代行,CLI serve 主循环同款)。
_CRON_SUPERVISOR: threading.Thread | None = None
_CRON_STOP: threading.Event | None = None


def _cron_emit_event(payload: dict[str, Any]) -> None:
    """ticker 线程发协议事件(``cron.skipped`` / ``cron.completed``)。

    ``_write_line`` 单写锁串行化(线程安全,B10 队头阻塞铁律的另一半:
    ticker 绝不进 serve 线程,事件只能旁路直写)。``_OUT`` 未就绪(直通
    模式/单测直调)时丢弃 + 入环形日志——事件是观测面,发射失败绝不带走
    调度路径。
    """
    try:
        if _OUT is not None:
            _write_line(payload)
        else:
            myssia_log.stream_line(
                None, "stderr", f"sidecar: cron 事件丢弃(_OUT 未就绪): {payload.get('type')}"
            )
    except Exception as exc:  # noqa: BLE001 — 观测面失败只留痕
        myssia_log.stream_line(None, "stderr", f"sidecar: cron 事件发送失败: {exc}")


def _cron_dispatch_gate(job: dict[str, Any]) -> bool:
    """tick 派发钩子(grill Q2):cron fire 前查桌面 run 单飞锁。

    占用 = 跳过本 fire(advance 已消耗,不排队不回滚——与 at-most-once
    一致;用户手点优先于 cron)。``last_status="skipped_busy"`` 由 tick 层
    落库(``myssia.cron.tick._process_due_job`` 状态显式覆写,成功语义不动
    streak);本钩子只补发 ``cron.skipped`` 协议事件供桌面 UI 即时可见。
    """
    with _RUNS_LOCK:
        active_run_id = _ACTIVE_RUN_ID
    if active_run_id is None:
        return True
    _cron_emit_event({
        "type": "cron.skipped",
        "job_id": job.get("id"),
        "name": job.get("name"),
        "reason": "run_busy",
        "active_run_id": active_run_id,
        "ts": _now_iso(),
    })
    return False


def _cron_execute_job(
    cron: CronJobs, job: dict[str, Any]
) -> tuple[bool, str | None, str | None]:
    """tick 执行体包装(``CronRunner.execute``)→ ``cron.completed`` 事件。

    事件载荷(design §4.2):job_id/status/摘要计数——摘要直接取 runner 随
    执行行落账的 ``run_summary_json``(D10,零二次解析子进程 stdout);取不
    到(账本 best-effort 写失败)事件照发,``summary=null`` 如实,不虚构。
    """
    runner = CronRunner(cron)
    success, error, delivery_error = runner.execute(job)
    summary: Any = None
    execution_id = str(job.get("execution_id") or "")
    if execution_id:
        try:
            row = cron.ledger.get_execution(execution_id)
            raw = row.get("run_summary_json") if row else None
            if isinstance(raw, str) and raw:
                summary = json.loads(raw)
        except Exception:  # noqa: BLE001 — 事件是观测面
            summary = None
    run_status: str | None = None
    if isinstance(summary, dict):
        run_block = summary.get("run")
        if isinstance(run_block, dict) and isinstance(run_block.get("status"), str):
            run_status = run_block["status"]
    _cron_emit_event({
        "type": "cron.completed",
        "job_id": job.get("id"),
        "name": job.get("name"),
        "ok": bool(success),
        "status": run_status or ("ok" if success else "failed"),
        "delivery_error": delivery_error,
        "summary": summary,
        "ts": _now_iso(),
    })
    return success, error, delivery_error


def _start_cron_ticker() -> None:
    """serve() 就绪后起 cron ticker(design §4.2):daemon 线程,绝不占
    serve 线程(B10);数据根取 ``_serve_context`` 的 db 父目录。

    - 幂等:一个 sidecar 进程至多一套 ticker(``_CRON_TICKER_LOCK`` 内
      查-占原子);serve EOF 关停后重入 serve 会重起(lifecycle = serve)。
    - **home 模式才起**(``_serve_context().home is not None``):桌面生产
      形态恒为 home;dev/测试 serve 落数据根 cwd,起真 ticker 会在仓库建
      ``cron/`` 目录——dev 常宿形态用 ``myssia cron serve``(同底座同互斥);
      测试验 ticker 走 ``MYIA_HOME`` 注入。
    - 监督:F2.2 同款 :class:`SupervisedTickerThread`(线程崩了 respawn,
      restart 计数入日志)+ 专职 supervisor 线程周期 ``restart_if_dead``。
    - 起动失败只留痕,绝不拦服务起来(首跑种子同哲学)。
    """
    global _CRON_TICKER, _CRON_SUPERVISOR, _CRON_STOP
    with _CRON_TICKER_LOCK:
        if _CRON_SUPERVISOR is not None and _CRON_SUPERVISOR.is_alive():
            return
        try:
            ctx = _serve_context()
        except ProtocolError as exc:
            myssia_log.stream_line(None, "stderr", f"sidecar: cron ticker 未起({exc.code}: {exc.message})")
            return
        if ctx.home is None:
            return
        cron = CronJobs.for_db(ctx.db)
        stop = threading.Event()
        interval = float(CRON_TICK_INTERVAL_SECONDS)

        def _execute(job: dict[str, Any]) -> tuple[bool, str | None, str | None]:
            return _cron_execute_job(cron, job)

        ticker = SupervisedTickerThread(
            run_ticker_loop,
            args=(cron, stop),
            kwargs={
                "interval": interval,
                "execute_job": _execute,
                "dispatch_gate": _cron_dispatch_gate,
                # 心跳告警低频兜底扫描(10-05-cron-heartbeat 收尾件):
                # cron_stale 评估不依赖品类 run 成功,ticker 直挂每 5 分钟
                # 一扫(CLI ``cron serve`` 同位接线)。
                "heartbeat_scan": make_cron_heartbeat_scan(ctx.db),
            },
            stop_event=stop,
            name="cron-ticker",
        )
        ticker.start()

        def _supervise() -> None:
            poll = min(interval, 30.0)  # ticker 死亡的发现时延上限(CLI serve 同款)
            while not stop.wait(poll):
                ticker.restart_if_dead()
            ticker.join(timeout=poll + 5.0)
        supervisor = threading.Thread(
            target=_supervise, daemon=True, name="cron-ticker-supervisor"
        )
        supervisor.start()
        _CRON_TICKER, _CRON_SUPERVISOR, _CRON_STOP = ticker, supervisor, stop
        myssia_log.stream_line(
            None, "stderr",
            f"sidecar: cron ticker 已起(数据根 {cron.store.data_root},interval={interval:.0f}s)",
        )


def _stop_cron_ticker(join_timeout: float = 2.0) -> None:
    """关停 cron ticker(serve EOF / 测试夹具 B12):置 stop → 有界 join。

    幂等;先摘全局引用再 join(重入安全)。``Event.wait`` 可中断,idle
    ticker 即醒即退;mid-fire(执行体在跑)时 join 超时后线程在下一轮
    自行退出,daemon 语义兜底——绝不为等 fire 阻塞调用方。
    """
    global _CRON_TICKER, _CRON_SUPERVISOR, _CRON_STOP
    with _CRON_TICKER_LOCK:
        stop = _CRON_STOP
        supervisor = _CRON_SUPERVISOR
        ticker = _CRON_TICKER
        _CRON_TICKER = _CRON_SUPERVISOR = _CRON_STOP = None
    if stop is not None:
        stop.set()
    if supervisor is not None and supervisor.is_alive():
        supervisor.join(join_timeout)
    if ticker is not None and ticker.is_alive():
        ticker.join(join_timeout)


def _cron_jobs_from_params(params: dict[str, Any]) -> tuple[CronJobs, str]:
    """cron.* 族的数据根构造:``db`` 覆写(缺省 = serve 上下文 db),数据根
    = db 父目录(A6,与 CLI ``--db`` 同款推导;cron 目录挂数据根)。"""
    db = params.get("db")
    if db is not None and (not isinstance(db, str) or not db):
        raise ProtocolError("invalid_params", "db 必须为非空字符串", path="params.db")
    db = db or _serve_context().db
    return CronJobs.for_db(db), db


def _cron_resolve_job(cron: CronJobs, ref: Any) -> dict[str, Any]:
    """job 引用解析(id 或名字;重名带 candidates,未找到结构化 404)。"""
    if isinstance(ref, bool) or not isinstance(ref, str) or not ref.strip():
        raise ProtocolError("invalid_params", "缺少 job 引用(id 或名字)", path="params.job")
    try:
        job = cron.resolve_job_ref(ref.strip())
    except AmbiguousJobReference as exc:
        raise ProtocolError(
            "cron_ambiguous_job", str(exc), path="params.job",
            data={"candidates": [m.get("id") for m in exc.matches]},
        ) from exc
    if job is None:
        raise ProtocolError("cron_job_not_found", f"找不到 cron job:{ref}", path="params.job")
    return job


def _cron_opt_str(params: dict[str, Any], key: str) -> str | None:
    """可选字符串参数校验(None = 未提供;提供了必须非空字符串)。"""
    value = params.get(key)
    if value is not None and (not isinstance(value, str) or not value.strip()):
        raise ProtocolError("invalid_params", f"{key} 必须为非空字符串", path=f"params.{key}")
    return value


def _cron_category_checked(category: str) -> CategoryConfig:
    """Q6 早失败:完整 ``load_category_file`` 装不上即拒(create/edit 同门);
    装上即返回品类配置(create 取其 ``timezone`` 兜底缺省时区)。"""
    try:
        return load_category_file(category)
    except LoadError as exc:
        raise ProtocolError(
            "cron_category_invalid", f"品类 YAML 装不上: {exc}",
            path="params.category", data=exc.to_dict(),
        ) from exc


def _m_cron_list(params: dict[str, Any]) -> dict[str, Any]:
    """cron.list:job 清单(缺省仅活跃;all=true 含暂停/终态)。"""
    all_jobs = params.get("all", False)
    if not isinstance(all_jobs, bool):
        raise ProtocolError("invalid_params", "all 必须为布尔", path="params.all")
    cron, db = _cron_jobs_from_params(params)
    jobs = cron.list_jobs(include_disabled=all_jobs)
    return {
        "db": db,
        "data_root": str(cron.store.data_root),
        "count": len(jobs),
        "jobs": [dict(job) for job in jobs],
    }


def _m_cron_create(params: dict[str, Any]) -> dict[str, Any]:
    """cron.create:建定时 job(Q6 品类早失败;Q5 绝对路径存储由底座落地;
    时区链 timezone > 品类 YAML timezone > 本地,锚 schedule 解析随档存)。"""
    schedule = params.get("schedule")
    if not isinstance(schedule, str) or not schedule.strip():
        raise ProtocolError(
            "invalid_params",
            "缺少 schedule(五形态:30m / every 2h / every monday 9am / "
            "0 9 * * * / in 30m 或 ISO 时刻)",
            path="params.schedule",
        )
    category = params.get("category")
    if not isinstance(category, str) or not category.strip():
        raise ProtocolError("invalid_params", "缺少 category(品类 YAML 路径)", path="params.category")
    name = _cron_opt_str(params, "name")
    deliver = _cron_opt_str(params, "deliver")
    failure_deliver = _cron_opt_str(params, "failure_deliver")
    timezone = _cron_opt_str(params, "timezone")
    config = _cron_opt_str(params, "config")
    repeat = params.get("repeat")
    if repeat is not None and (isinstance(repeat, bool) or not isinstance(repeat, int)):
        raise ProtocolError("invalid_params", "repeat 必须为整数(次数)", path="params.repeat")
    run_timeout = params.get("run_timeout")
    if run_timeout is not None and (
        isinstance(run_timeout, bool)
        or not isinstance(run_timeout, (int, float))
        or float(run_timeout) <= 0
    ):
        raise ProtocolError("invalid_params", "run_timeout 必须为正数秒", path="params.run_timeout")
    dry_run = params.get("dry_run")
    if dry_run is not None and not isinstance(dry_run, bool):
        raise ProtocolError("invalid_params", "dry_run 必须为布尔", path="params.dry_run")
    paused = params.get("paused", False)
    if not isinstance(paused, bool):
        raise ProtocolError("invalid_params", "paused 必须为布尔", path="params.paused")
    paused_reason = _cron_opt_str(params, "paused_reason")
    cron, _db = _cron_jobs_from_params(params)
    config_obj = _cron_category_checked(category)
    try:
        job = cron.create_job(
            category=category,
            schedule=schedule,
            name=name,
            repeat=repeat,
            deliver=deliver,
            failure_deliver=failure_deliver,
            timezone=timezone or config_obj.timezone,
            config_path=(
                str(Path(config).expanduser().resolve()) if config else None
            ),
            run_timeout=run_timeout,
            # 仅显式设置才持久化(Hermes 可选键风格;create_job 对 None 不落键)
            dry_run=True if dry_run else None,
            paused=paused,
            paused_reason=paused_reason,
            origin={"source": "desktop"},
        )
    except ValueError as exc:  # schedule 五形态/once 超窗/repeat/paused/timezone
        raise ProtocolError("cron_create_failed", str(exc), path="params") from exc
    return {"job": dict(job)}


def _m_cron_edit(params: dict[str, Any]) -> dict[str, Any]:
    """cron.edit:部分更新;schedule 变更由底座重算 next_run_at 并重推导
    repeat 缺省(once↔recurring 翻转)。"""
    cron, _db = _cron_jobs_from_params(params)
    job = _cron_resolve_job(cron, params.get("job"))
    category = _cron_opt_str(params, "category")
    if category is not None:
        _cron_category_checked(category)
    config = _cron_opt_str(params, "config")
    updates: dict[str, Any] = {}
    for key in ("schedule", "name", "deliver", "failure_deliver", "timezone"):
        value = params.get(key)
        if value is not None:
            updates[key] = value
    if category is not None:
        updates["category"] = category
    if config is not None:
        updates["config_path"] = str(Path(config).expanduser().resolve())
    repeat = params.get("repeat")
    if repeat is not None:
        if isinstance(repeat, bool) or not isinstance(repeat, int):
            raise ProtocolError("invalid_params", "repeat 必须为整数(次数)", path="params.repeat")
        updates["repeat"] = repeat
    run_timeout = params.get("run_timeout")
    if run_timeout is not None:
        if (
            isinstance(run_timeout, bool)
            or not isinstance(run_timeout, (int, float))
            or float(run_timeout) <= 0
        ):
            raise ProtocolError("invalid_params", "run_timeout 必须为正数秒", path="params.run_timeout")
        updates["run_timeout"] = run_timeout
    if not updates:
        raise ProtocolError(
            "cron_edit_no_changes",
            "未给出任何要更新的字段(schedule/name/category/deliver/…)",
            path="params",
        )
    try:
        updated = cron.update_job(job["id"], updates)
    except ValueError as exc:  # schedule 解析失败/once 超窗/终态复活拒绝
        raise ProtocolError("cron_edit_failed", str(exc), path="params") from exc
    return {"job": dict(updated or {})}


def _m_cron_pause(params: dict[str, Any]) -> dict[str, Any]:
    """cron.pause:暂停 job(reason 可选,F1.1);``all:true`` = 全局急停
    estop 标记(grill Q4;在途 run 不受影响,tick 跳过派发)。"""
    all_flag = params.get("all", False)
    if not isinstance(all_flag, bool):
        raise ProtocolError("invalid_params", "all 必须为布尔", path="params.all")
    job_ref = params.get("job")
    reason = _cron_opt_str(params, "reason")
    if all_flag and job_ref is not None:
        raise ProtocolError("invalid_params", "all 是全局急停,不要再带 job", path="params.job")
    cron, _db = _cron_jobs_from_params(params)
    if all_flag:
        marker = cron.engage_estop(reason or "paused via sidecar cron.pause all")
        return {"estopped": True, "marker": str(marker)}
    if job_ref is None:
        raise ProtocolError("invalid_params", "缺少 job(或 all=true 踩全局急停)", path="params.job")
    job = _cron_resolve_job(cron, job_ref)
    updated = cron.pause_job(job["id"], reason=reason)
    return {"job": dict(updated or {})}


def _m_cron_resume(params: dict[str, Any]) -> dict[str, Any]:
    """cron.resume:恢复 job / 一次性重挂(``at`` = ISO 时刻);``all:true``
    = 解除全局急停。"""
    all_flag = params.get("all", False)
    if not isinstance(all_flag, bool):
        raise ProtocolError("invalid_params", "all 必须为布尔", path="params.all")
    at = params.get("at")
    if at is not None and (not isinstance(at, str) or not at.strip()):
        raise ProtocolError("invalid_params", "at 必须为非空 ISO 时刻串", path="params.at")
    job_ref = params.get("job")
    if all_flag and (job_ref is not None or at is not None):
        raise ProtocolError("invalid_params", "all 是解除全局急停,不要再带 job/at", path="params")
    cron, _db = _cron_jobs_from_params(params)
    if all_flag:
        cleared = cron.disengage_estop()
        return {"estopped": cron.is_estopped(), "cleared": cleared}
    if job_ref is None:
        raise ProtocolError("invalid_params", "缺少 job(或 all=true 解除全局急停)", path="params.job")
    job = _cron_resolve_job(cron, job_ref)
    try:
        updated = (
            cron.rearm_oneshot(job["id"], at)
            if at is not None
            else cron.resume_job(job["id"])
        )
    except ValueError as exc:  # recurring 拒 at / once 已过窗 / 覆盖活认领
        raise ProtocolError("cron_resume_failed", str(exc), path="params") from exc
    if updated is None:  # pragma: no cover - resolve 已保证存在
        raise ProtocolError(
            "cron_job_not_found", f"找不到 cron job:{job_ref}", path="params.job"
        )
    return {"job": dict(updated)}


def _m_cron_run(params: dict[str, Any]) -> dict[str, Any]:
    """cron.run:安排下次 tick 立即跑(manual 来源;复活 paused、计入
    repeat,§8.1 事实裁决)。"""
    cron, _db = _cron_jobs_from_params(params)
    job = _cron_resolve_job(cron, params.get("job"))
    try:
        updated = cron.trigger_job(job["id"])
    except ValueError as exc:  # 终态 job 拒绝
        raise ProtocolError("cron_run_failed", str(exc), path="params") from exc
    return {"job": dict(updated or {})}


def _m_cron_remove(params: dict[str, Any]) -> dict[str, Any]:
    """cron.remove:删 job 记录;output 目录与账本行保留(运行证据)。"""
    cron, _db = _cron_jobs_from_params(params)
    job = _cron_resolve_job(cron, params.get("job"))
    if not cron.remove_job(job["id"]):  # pragma: no cover - resolve 已保证存在
        raise ProtocolError(
            "cron_job_not_found", f"找不到 cron job:{job['id']}", path="params.job"
        )
    return {"removed": True, "job_id": job["id"], "name": job.get("name")}


def _m_cron_status(params: dict[str, Any]) -> dict[str, Any]:
    """cron.status:ticker 活性(心跳龄/最后错误)+ 下次到期 + 急停态(F1.6)。"""
    cron, db = _cron_jobs_from_params(params)
    heartbeat_age = cron.get_ticker_heartbeat_age()
    success_age = cron.get_ticker_success_age()
    last_error = cron.get_ticker_last_error()
    writer_alive = cron.ticker_heartbeat_writer_alive()
    estopped = cron.is_estopped()
    jobs = cron.list_jobs(include_disabled=True)
    enabled_jobs = [job for job in jobs if job.get("enabled", True)]
    next_due_at = min(
        (job["next_run_at"] for job in enabled_jobs if job.get("next_run_at")),
        default=None,
    )
    heartbeat_fresh = (
        heartbeat_age is not None and heartbeat_age <= _CRON_TICKER_FRESH_SECONDS
    )
    return {
        "db": db,
        "data_root": str(cron.store.data_root),
        "ticker_alive": heartbeat_fresh and writer_alive,
        "heartbeat_age_seconds": heartbeat_age,
        "last_success_age_seconds": success_age,
        "last_error": last_error,
        "estopped": estopped,
        "jobs_total": len(jobs),
        "jobs_enabled": len(enabled_jobs),
        "next_due_at": next_due_at,
    }


def _m_cron_runs(params: dict[str, Any]) -> dict[str, Any]:
    """cron.runs:执行账本尾查(新→旧;limit 钳制 [1,500];run_summary
    摘要随行解析,损坏串如实带 raw)。"""
    limit = params.get("limit", 20)
    if limit is None:
        limit = 20
    if isinstance(limit, bool) or not isinstance(limit, int):
        raise ProtocolError("invalid_params", "limit 必须为整数", path="params.limit")
    limit = max(1, min(limit, 500))
    cron, db = _cron_jobs_from_params(params)
    job_ref = params.get("job")
    job_id_filter: str | None = None
    if job_ref is not None:
        job = _cron_resolve_job(cron, job_ref)
        job_id_filter = job["id"]
    records: list[dict[str, Any]] = []
    for row in cron.ledger.list_executions(job_id=job_id_filter, limit=limit):
        record = dict(row)
        raw_summary = record.pop("run_summary_json", None)
        try:
            record["run_summary"] = json.loads(raw_summary) if raw_summary else None
        except (TypeError, ValueError):  # 手编/损坏的摘要:如实带原串
            record["run_summary"] = {"raw": raw_summary}
        records.append(record)
    return {"db": db, "count": len(records), "executions": records}


# ---------------------------------------------------------------------------
# Telegram 监控状态与网页线账号管理(10-08-tg-web-line W4;设置页总卡消费)
# + 浏览器专用模块(10-08-browser-module 案甲,PRD 单入口铁律):
#
# telegram.* 两方法:telegram.status(bot token 在册/telethon session 在场/
# 网页线账号列表;web 段登录态与浏览器模块操作台账联动)、
# telegram.web.delete(删配置档)。原 telegram.web.login 已**移除**——一切
# 浏览器操作(登录打头)必经浏览器模块统一入口,禁止任何功能旁路直启
# Chromium(主人令:这个功能就要调用起来专用浏览器模块)。
#
# browser.* 四方法(浏览器模块 = 浏览器操作的唯一治理位:窗口生命周期/
# 错误上浮/操作台账集中):browser.open(kind+session_key,后台线程拉起
# headed 登录窗,复用 web_line 登录器零重写)、browser.list(操作台账+
# 日志尾巴)、browser.focus / browser.close(每操作窗口管理)。
# ---------------------------------------------------------------------------

#: 浏览器操作台账(op_id → 记录;进程内有效 —— 操作是会话态,重启即清,
#: 登录态落配置档不受影响)。op_id = 会话键(首役 kind=tg_web_login 一键
#: 一操作,重登覆盖旧记录;未来新类别以 `<kind>:<键>` 命名空间隔离)。
_BROWSER_OPS: dict[str, dict[str, Any]] = {}
_BROWSER_OPS_LOCK = threading.Lock()

#: 每操作日志尾巴容量(环形;登录器 print 回执逐行入账,超量裁头)。
_BROWSER_OP_LOG_LINES = 60

#: browser.open 已登记的操作类别(单入口铁律的登记面:新浏览器需求须在
#: 此登记后才可经模块拉窗,未登记类别结构化拒)。
_BROWSER_KINDS: dict[str, str] = {
    "tg_web_login": "TG 网页线登录(web.telegram.org;复用 web_line 登录器)",
}


def _telegram_data_root() -> Path:
    """telegram 面的数据根(serve 上下文 home;dev 回退 cwd —— web_line
    ``default_data_root`` 同口径,登录流与状态面落同一根)。"""
    ctx = _serve_context()
    return Path(ctx.home) if ctx.home is not None else Path.cwd()


def _resolve_credential_probe(ref: str, backend: Any | None = None) -> str:
    """凭据存在性探针(只回值给 configured 判定,值本身零落日志零回显;
    独立模块级函数 = 协议测试的注入缝)。"""
    from myssia.schema import resolve_credential

    return resolve_credential(ref, backend=backend)


def _m_telegram_status(params: dict[str, Any]) -> dict[str, Any]:
    """``telegram.status``:三线状态快照(bot/telethon/web;只读零副作用)."""
    data_root = _telegram_data_root()
    bot_configured = False
    bot_error: str | None = None
    try:
        token = _resolve_credential_probe("keychain:myia/telegram/bot-token")
        bot_configured = bool(token.strip()) and token.strip() not in {
            "token",
            "changeme",
        }
    except Exception as exc:  # noqa: BLE001 - 凭据解析失败如实回显(值不回显)
        bot_error = f"{type(exc).__name__}"
    session_path = data_root / "telegram" / "telethon.session"
    web_accounts: list[dict[str, Any]] = []
    try:
        from myssia.telegram.web_line import (
            list_accounts,
            profile_dir,
            read_login_marker,
        )

        for account in list_accounts(data_root):
            marker = read_login_marker(profile_dir(data_root, account))
            # 卡面 ↔ 模块联动(10-08-browser-module):登录中/失败态真源 =
            # 浏览器模块操作台账(op_id = 账号键);无操作 = 静稳态。
            with _BROWSER_OPS_LOCK:
                op = _BROWSER_OPS.get(account)
            op_phase = op.get("phase") if op is not None else None
            web_accounts.append(
                {
                    "account": account,
                    "logged_in": marker is not None,
                    "logged_in_at": (
                        marker.get("logged_in_at") if marker else None
                    ),
                    "login_in_progress": op_phase == "running",
                    "login_note": (
                        op.get("note") if op is not None else None
                    ),
                }
            )
    except Exception as exc:  # noqa: BLE001 - 状态面炸不拦协议,如实带 error
        web_accounts = []
        bot_error = bot_error or f"web_accounts_failed:{type(exc).__name__}"
    return {
        "bot": {"configured": bot_configured, "error": bot_error},
        "session": {"exists": session_path.exists()},
        "web": {"accounts": web_accounts},
    }


class _BrowserWindowClosed(Exception):
    """browser.close 置停令后注入 sleep 抛出 —— 登录流尽快收尾(窗已关)."""


def _browser_log(op_id: str, line: str) -> None:
    """操作日志入账(环形;登录器 print 回执逐行带时间戳进台账)."""
    with _BROWSER_OPS_LOCK:
        record = _BROWSER_OPS.get(op_id)
        if record is None:
            return
        log: list[str] = record["log"]
        log.append(f"{_now_iso()} {line}")
        if len(log) > _BROWSER_OP_LOG_LINES:
            del log[: len(log) - _BROWSER_OP_LOG_LINES]


def _browser_op_public(record: dict[str, Any]) -> dict[str, Any]:
    """台账记录 → 协议投影(掐掉线程内句柄 stop_event/page/loop,只留面)."""
    return {
        "op_id": record["op_id"],
        "kind": record["kind"],
        "session_key": record["session_key"],
        "url": record["url"],
        "phase": record["phase"],
        "note": record["note"],
        "fix_hint": record["fix_hint"],
        "started_at": record["started_at"],
        "finished_at": record["finished_at"],
        "log_tail": list(record["log"][-20:]),
    }


def _browser_humanize_failure(exc: Exception) -> tuple[str, str]:
    """失败 → (人话 note, 修复指引)。静默失败=反模式(PRD AC2):依赖缺/
    浏览器二进制缺/登录超时,每类失败都带可见出路,不装死。"""
    from myssia.telegram.web_line import TelegramWebError

    if isinstance(exc, TelegramWebError):
        if exc.reason == "dependency_missing":
            return (
                f"登录窗拉起失败:playwright 未安装({exc})",
                "设置 →「Python 环境」→ 同步依赖(桌面锁已收录 playwright);"
                "或终端执行 pip install 'myssia[browser]'",
            )
        if exc.reason == "login_timeout":
            return (
                f"登录等待超时:{exc}",
                "重新点「添加账号 / 重新登录」再试;反复超时查网络/代理出口",
            )
        return (f"{exc.reason}: {exc}", "重试;反复失败展开日志尾巴定位")
    text = str(exc)
    lowered = text.lower()
    if "executable doesn't exist" in lowered or "playwright install" in lowered:
        return (
            "浏览器二进制缺失(Chromium 未下载):"
            + text[:300],
            "设置 →「Python 环境」→ 安装「JS 渲染抓取(crawl4ai)」组件"
            "(含 Chromium 下载,落数据根 playwright-browsers);"
            "或终端执行 playwright install chromium",
        )
    return (
        f"{type(exc).__name__}: {text[:400]}",
        "重试;反复失败展开日志尾巴定位",
    )


def _browser_make_sleep(op_id: str, stop_event: threading.Event):
    """注入登录流的 sleep:细粒度可中断(≤0.25s 检查停令)+ 顺带捕获登录
    线程事件循环(browser.focus 经 run_coroutine_threadsafe 回该循环调度
    page.bring_to_front —— Playwright async 对象只能在其归属循环上动)。"""

    async def _sleep(seconds: float) -> None:
        loop = asyncio.get_running_loop()
        with _BROWSER_OPS_LOCK:
            record = _BROWSER_OPS.get(op_id)
            if record is not None:
                record["loop"] = loop
        deadline = loop.time() + max(0.0, float(seconds))
        while True:
            if stop_event.is_set():
                raise _BrowserWindowClosed(
                    f"操作 {op_id} 窗口已由用户关闭(browser.close)"
                )
            remaining = deadline - loop.time()
            if remaining <= 0:
                return
            await asyncio.sleep(min(0.25, remaining))

    return _sleep


def _browser_thread_main(
    op_id: str, session_key: str, force: bool
) -> None:
    """操作线程:跑既有登录器(web_line.TelegramWebLoginFlow,零重写),
    print 回执进日志尾巴,收尾写台账(running → done/failed/closed)."""
    from myssia.telegram.web_line import TelegramWebLoginFlow

    with _BROWSER_OPS_LOCK:
        record = _BROWSER_OPS.get(op_id)
        if record is None:  # pragma: no cover - 删除竞态防御
            return
        stop_event: threading.Event = record["stop_event"]
        kind: str = record["kind"]

    def _print(message: str) -> None:
        _browser_log(op_id, message)

    def _on_page_opened(page: Any) -> None:
        with _BROWSER_OPS_LOCK:
            current = _BROWSER_OPS.get(op_id)
            if current is not None:
                current["page"] = page
        _browser_log(op_id, "浏览器窗口已就位(页面打开)")

    def _finish(phase: str, note: str, fix_hint: str | None) -> None:
        with _BROWSER_OPS_LOCK:
            current = _BROWSER_OPS.get(op_id)
            if current is None:  # pragma: no cover - 删除竞态防御
                return
            current["phase"] = phase
            current["note"] = note
            current["fix_hint"] = fix_hint
            current["finished_at"] = _now_iso()
            current["page"] = None
            current["loop"] = None

    if kind != "tg_web_login":  # pragma: no cover - 词表单键,新类别接入时扩
        _finish("failed", f"类别 {kind} 未接线", None)
        return
    try:
        asyncio.run(
            TelegramWebLoginFlow(
                print_fn=_print,
                sleep=_browser_make_sleep(op_id, stop_event),
                on_page_opened=_on_page_opened,
            ).run(_telegram_data_root(), session_key, force=force)
        )
    except _BrowserWindowClosed as exc:
        _browser_log(op_id, str(exc))
        _finish("closed", f"窗口已关闭:{exc}", None)
        return
    except Exception as exc:  # noqa: BLE001 - 一切失败人话上浮(AC2)
        note, fix_hint = _browser_humanize_failure(exc)
        _browser_log(op_id, note)
        _finish("failed", note, fix_hint)
        return
    _finish("done", "登录完成(登录态已落配置档,0700/0600)", None)


def _m_browser_open(params: dict[str, Any]) -> dict[str, Any]:
    """``browser.open``:浏览器操作统一入口(PRD 单入口铁律;首役 tg_web
    登录,复用 web_line 登录器;手机号+验证码全在浏览器页面内,零读取)."""
    kind = params.get("kind")
    if not isinstance(kind, str) or kind not in _BROWSER_KINDS:
        raise ProtocolError(
            "invalid_params",
            "kind 必须是浏览器模块已登记的操作类别:"
            f"{sorted(_BROWSER_KINDS)}(新浏览器需求须先在模块登记,"
            "禁止旁路直启 Chromium)",
            path="params.kind",
            data={"allowed": sorted(_BROWSER_KINDS)},
        )
    session_key = params.get("session_key")
    if not isinstance(session_key, str):
        raise ProtocolError(
            "invalid_params", "session_key 必须是字符串", path="params.session_key"
        )
    url = params.get("url")
    if url is not None and not isinstance(url, str):
        raise ProtocolError(
            "invalid_params", "url 可选,须为字符串", path="params.url"
        )
    force = params.get("force", False)
    if not isinstance(force, bool):
        raise ProtocolError(
            "invalid_params", "force 必须是布尔", path="params.force"
        )
    if kind == "tg_web_login":
        from myssia.telegram.web_line import (
            INSTALL_COMMAND,
            WEB_ORIGIN,
            TelegramWebError,
            require_playwright,
            validate_account_key,
        )

        try:
            key = validate_account_key(session_key)
        except TelegramWebError as exc:
            raise ProtocolError(
                "invalid_params", str(exc), path="params.session_key"
            ) from exc
        if url is None:
            url = WEB_ORIGIN
        # 依赖前置检查(AC2:拔依赖 → 点按钮立即可见错误+修复指引,
        # 不等后台线程失败;真装态此调用零副作用只是 import 探针)。
        try:
            require_playwright()
        except TelegramWebError as exc:
            raise ProtocolError(
                "dependency_missing",
                "登录窗拉不起来:playwright 库未安装。修复:设置 →"
                "「Python 环境」→ 同步依赖(桌面锁已收录 playwright),"
                f"或终端执行 {INSTALL_COMMAND}",
                path="params.kind",
                data={"kind": kind, "install_command": INSTALL_COMMAND},
            ) from exc
        session_key = key
        op_id = key
    else:  # pragma: no cover - 词表单键;新类别在此接线
        raise ProtocolError(
            "invalid_params", f"类别 {kind} 未接线", path="params.kind"
        )

    with _BROWSER_OPS_LOCK:
        current = _BROWSER_OPS.get(op_id)
        if current is not None and current.get("phase") == "running":
            return {
                "started": False,
                "op_id": op_id,
                "note": "该操作的浏览器窗口已在进行中(到「浏览器」模块聚焦/关闭)",
            }
        _BROWSER_OPS[op_id] = {
            "op_id": op_id,
            "kind": kind,
            "session_key": session_key,
            "url": url,
            "phase": "running",
            "note": "登录窗拉起中(浏览器窗口即将弹出)",
            "fix_hint": None,
            "started_at": _now_iso(),
            "finished_at": None,
            "log": [
                f"{_now_iso()} 操作登记:{kind} 会话 {session_key}"
                f"(force={force})"
            ],
            "stop_event": threading.Event(),
            "page": None,
            "loop": None,
        }
    thread = threading.Thread(
        target=_browser_thread_main,
        args=(op_id, session_key, force),
        daemon=True,
        name=f"browser-op-{op_id}",
    )
    thread.start()
    return {"started": True, "op_id": op_id, "kind": kind, "url": url}


def _m_browser_list(params: dict[str, Any]) -> dict[str, Any]:
    """``browser.list``:操作台账(最新在前;phase=running/done/failed/
    closed,带人话 note/修复指引/日志尾巴)。"""
    with _BROWSER_OPS_LOCK:
        records = sorted(
            _BROWSER_OPS.values(),
            key=lambda record: str(record.get("started_at")),
            reverse=True,
        )
        operations = [_browser_op_public(record) for record in records]
    return {"operations": operations, "kinds": dict(_BROWSER_KINDS)}


def _m_browser_focus(params: dict[str, Any]) -> dict[str, Any]:
    """``browser.focus``:把进行中操作的浏览器窗口带到前台(bring_to_front,
    经登录线程事件循环调度)。"""
    op_id = params.get("op_id")
    if not isinstance(op_id, str):
        raise ProtocolError(
            "invalid_params", "op_id 必须是字符串", path="params.op_id"
        )
    with _BROWSER_OPS_LOCK:
        record = _BROWSER_OPS.get(op_id)
        phase = record.get("phase") if record is not None else None
        page = record.get("page") if record is not None else None
        loop = record.get("loop") if record is not None else None
    if record is None:
        raise ProtocolError(
            "unknown_operation",
            f"操作 {op_id} 不在台账(进程重启后会清空,重开操作即可)",
            path="params.op_id",
        )
    if phase != "running":
        raise ProtocolError(
            "window_not_active",
            f"操作 {op_id} 窗口不在运行中(当前态:{phase});"
            "聚焦只对进行中的窗口有效",
            path="params.op_id",
        )
    if page is None or loop is None:
        raise ProtocolError(
            "window_not_active",
            f"操作 {op_id} 的浏览器窗口还没就位(刚拉起),稍等片刻再聚焦",
            path="params.op_id",
        )
    try:
        future = asyncio.run_coroutine_threadsafe(page.bring_to_front(), loop)
        future.result(timeout=10.0)
    except Exception as exc:  # noqa: BLE001 - 跨线程调度失败如实上浮
        raise ProtocolError(
            "focus_failed",
            f"聚焦失败:{type(exc).__name__}: {exc}",
            path="params.op_id",
        ) from exc
    return {"focused": True, "op_id": op_id}


def _m_browser_close(params: dict[str, Any]) -> dict[str, Any]:
    """``browser.close``:请求关闭进行中操作的浏览器窗口(置停令 → 注入
    sleep 抛收尾异常 → 登录流 finally 关 context;台账转 closed)。"""
    op_id = params.get("op_id")
    if not isinstance(op_id, str):
        raise ProtocolError(
            "invalid_params", "op_id 必须是字符串", path="params.op_id"
        )
    with _BROWSER_OPS_LOCK:
        record = _BROWSER_OPS.get(op_id)
        phase = record.get("phase") if record is not None else None
        stop_event = record.get("stop_event") if record is not None else None
    if record is None:
        raise ProtocolError(
            "unknown_operation",
            f"操作 {op_id} 不在台账(进程重启后会清空,重开操作即可)",
            path="params.op_id",
        )
    if phase != "running" or not isinstance(stop_event, threading.Event):
        raise ProtocolError(
            "window_not_active",
            f"操作 {op_id} 窗口不在运行中(当前态:{phase});"
            "关闭只对进行中的窗口有效",
            path="params.op_id",
        )
    stop_event.set()
    _browser_log(op_id, "已收到关闭请求(窗口收尾中)")
    return {
        "closed": True,
        "op_id": op_id,
        "note": "已请求关闭:窗口收尾后台账转「已关闭」(刷新可见)",
    }


def _m_telegram_web_delete(params: dict[str, Any]) -> dict[str, Any]:
    """``telegram.web.delete``:删账号配置档(登录态随档消失;幂等)."""
    import shutil

    from myssia.telegram.web_line import (
        TelegramWebError,
        profile_dir,
        validate_account_key,
    )

    account = params.get("account")
    if not isinstance(account, str):
        raise ProtocolError(
            "invalid_params", "account 必须是字符串(账号键)", path="params.account"
        )
    try:
        key = validate_account_key(account)
    except TelegramWebError as exc:
        raise ProtocolError("invalid_params", str(exc), path="params.account") from exc
    directory = profile_dir(_telegram_data_root(), key)
    with _BROWSER_OPS_LOCK:
        op = _BROWSER_OPS.get(key)
        op_running = op is not None and op.get("phase") == "running"
    if op_running:
        raise ProtocolError(
            "login_in_progress",
            f"账号 {key} 登录窗正在进行中:先到「浏览器」模块关闭登录窗,"
            "再回来删除配置档",
            path="params.account",
        )
    if directory.exists():
        shutil.rmtree(directory)
    with _BROWSER_OPS_LOCK:
        _BROWSER_OPS.pop(key, None)
    return {"deleted": True, "account": key, "existed": True}


# ---------------------------------------------------------------------------
# 分发与 serve 循环
# ---------------------------------------------------------------------------

_HANDLERS: dict[str, Callable[[dict[str, Any]], dict[str, Any]]] = {
    "version": _m_version,
    "health": _m_health,
    "plugins.list": _m_plugins_list,
    "plugins.bundled.list": _m_plugins_bundled_list,
    "plugins.bundled.install": _m_plugins_bundled_install,
    "plugins.bundled.uninstall": _m_plugins_bundled_uninstall,
    "plugins.bundled.category_install": _m_plugins_bundled_category_install,
    "plugins.remote.get": _m_plugins_remote_get,
    "plugins.remote.save": _m_plugins_remote_save,
    "doctor": _m_doctor,
    "run.start": _m_run_start,
    "run.status": _m_run_status,
    "run.cancel": _m_run_cancel,
    "runs.list": _m_runs_list,
    "runs.trend": _m_runs_trend,
    "feedback.mark": _m_feedback_mark,
    "feedback.list": _m_feedback_list,
    "feedback.stats": _m_feedback_stats,
    "store.trend": _m_store_trend,
    "logs.tail": _m_logs_tail,
    "store.items": _m_store_items,
    "store.source_stats": _m_store_source_stats,
    "store.state.mark": _m_store_state_mark,
    "store.state.mark_all": _m_store_state_mark_all,
    "store.state.import": _m_store_state_import,
    "feed.export": _m_feed_export,
    "feed.enrich": _m_feed_enrich,
    "schedule.preview": _m_schedule_preview,
    "secret.set": _m_secret_set,
    "secret.list": _m_secret_list,
    "secret.delete": _m_secret_delete,
    "sources.write": _m_sources_write,
    "sources.test": _m_sources_test,
    "yaml.list": _m_yaml_list,
    "yaml.read": _m_yaml_read,
    "yaml.validate": _m_yaml_validate,
    "yaml.template": _m_yaml_template,
    "yaml.save": _m_yaml_save,
    "yaml.delete": _m_yaml_delete,
    "image.config.read": _m_image_config_read,
    "image.config.save": _m_image_config_save,
    "image.models.list": _m_image_models_list,
    "image.models.download": _m_image_models_download,
    "image.models.delete": _m_image_models_delete,
    "image.models.activate": _m_image_models_activate,
    "image.server.status": _m_image_server_status,
    "image.server.ensure": _m_image_server_ensure,
    "image.files.purge": _m_image_files_purge,
    "gates.get": _m_gates_get,
    "gates.save": _m_gates_save,
    "channels.list": _m_channels_list,
    "channels.refresh": _m_channels_refresh,
    "channels.alias": _m_channels_alias,
    "push.write": _m_push_write,
    "push.test": _m_push_test,
    "bridge.status": _m_bridge_status,
    "alerts.list": _m_alerts_list,
    "alerts.save": _m_alerts_save,
    "alerts.delete": _m_alerts_delete,
    "alerts.test": _m_alerts_test,
    "cron.list": _m_cron_list,
    "cron.create": _m_cron_create,
    "cron.edit": _m_cron_edit,
    "cron.pause": _m_cron_pause,
    "cron.resume": _m_cron_resume,
    "cron.run": _m_cron_run,
    "cron.remove": _m_cron_remove,
    "cron.status": _m_cron_status,
    "cron.runs": _m_cron_runs,
    # Telegram 监控总卡面(10-08-tg-web-line W4):三线状态/网页线账号
    # 配置档删除。登录动作已改走浏览器模块(10-08-browser-module 单入口
    # 铁律:telegram.web.login 移除,browser.* 四方法为唯一浏览器入口)。
    "telegram.status": _m_telegram_status,
    "telegram.web.delete": _m_telegram_web_delete,
    # 浏览器专用模块(10-08-browser-module 案甲):统一入口 open + 操作
    # 台账 list + 窗口管理 focus/close;一切浏览器操作必经此处。
    "browser.open": _m_browser_open,
    "browser.list": _m_browser_list,
    "browser.focus": _m_browser_focus,
    "browser.close": _m_browser_close,
}


def _handle_line(line: str) -> None:
    """单请求处理:分发 → 应答;一切错误结构化,协议流不裸 traceback。"""
    try:
        request = json.loads(line)
    except json.JSONDecodeError as exc:
        _error(None, "parse_error", f"请求行不是合法 JSON: {exc}")
        return
    if not isinstance(request, dict):
        _error(None, "invalid_request", "请求必须是 JSON 对象")
        return
    rid = request.get("id")
    method = request.get("method")
    if not isinstance(method, str) or not method:
        _error(rid, "invalid_request", "缺少字符串字段 method", path="method")
        return
    handler = _HANDLERS.get(method)
    if handler is None:
        _error(rid, "method_not_found", f"未知方法 {method}", path="method",
               data={"allowed": sorted(_HANDLERS)})
        return
    params = request.get("params")
    if params is None:
        params = {}
    if not isinstance(params, dict):
        _error(rid, "invalid_params", "params 必须是对象", path="params")
        return
    try:
        result = handler(params)
    except ProtocolError as exc:
        _error(rid, exc.code, exc.message, path=exc.path, data=exc.data)
        return
    except Exception as exc:  # noqa: BLE001 — 兜底:内部错误也必须结构化
        print(f"sidecar: internal_error on {method}: {exc}", file=sys.stderr)
        _error(rid, "internal_error", f"{type(exc).__name__}: {exc}")
        return
    if rid is not None:
        _respond(rid, result)


# ---------------------------------------------------------------------------
# telegram serve 常驻宿主(10-06-telegram-telethon 桌面接线批,AC4 前置)
# (cron ticker 同款双宿主判例:serve 生命周期 daemon 线程,home 模式才起,
# 起不来只留痕不拦服务;能力 = myssia.telegram 包,装配与 CLI
# ``myssia telegram serve`` 同门。零新协议方法——``telegram.serve.status``
# 等观测面留待后续批)
# ---------------------------------------------------------------------------

#: 桌面档品类文件名(CLI ``myssia telegram serve`` 默认 ``plugins/telegram-groups.yaml``
#: 同门单文件;多 bot/多品类拆档各起宿主走 CLI serve,不在此扩)。
_TELEGRAM_CATEGORY_FILENAME = "telegram-groups.yaml"


def _telegram_source_categories(*configs: Any) -> dict[str, str]:
    """源名 → 品类 id 映射(telegram 三线落库盖戳用,10-09-tg-category-entry).

    此前 telegram 三线(bot 长轮询/telethon/网页线)落库都不带 category ——
    条目在情报流 L1 品类层隐身,只混进「全部条目」总数(TG 群监控装了像没
    装)。本映射按品类文件的 sources 词表把条目归行:主品类 telegram-groups
    与专用件 telegram-web 各归各行;同名源先到先得(与装配侧「同一群只跑
    一线」判例同门);未登记源 = 不入映射,落库 None 不猜。
    """
    mapping: dict[str, str] = {}
    for config in configs:
        if config is None:
            continue
        config_id = str(getattr(config, "id", "") or "")
        for source in getattr(config, "sources", []) or []:
            name = str(getattr(source, "name", "") or "")
            if name and config_id and name not in mapping:
                mapping[name] = config_id
    return mapping

_TELEGRAM_HOST_LOCK = threading.Lock()
#: 宿主线程句柄(asyncio.run + daemon;测试夹具拆线防线程泄漏,cron 同款)。
_TELEGRAM_THREAD: threading.Thread | None = None
#: 停止 Event(注入宿主 ``should_stop``;轮间检查点生效,挂起窗 daemon 兜底)。
_TELEGRAM_STOP: threading.Event | None = None


class _TelegramHostBundle(NamedTuple):
    """装配产物:``host`` = 宿主本体(观测面/测试锚),``run`` = async 主程
    (宿主 run_forever + client 收尾),``close`` = sync 收尾(store 关闭),
    ``label`` = 启动留痕摘要。"""

    host: Any
    run: Any
    close: Any
    label: str


def _assemble_telegram_host(
    ctx: ServeContext, stop: threading.Event
) -> _TelegramHostBundle | None:
    """桌面档装配:与 CLI ``_cmd_telegram_serve`` 同门(逐句对照移植)。

    品类(plugins/telegram-groups.yaml)→ 每 chat_id 一绑定(过滤管线同引擎
    配置)→ **双线**(B4 起):bot 线(单 bot token,keychain 解析,长轮询)
    + telethon 用户线(账号 session 事件监听,``assemble_user_host`` 工厂,
    session 未首登/凭据缺 = 留痕零阻塞)→ 推送 sink(品类 push 首条通道)/
    入库 sink(SQLiteStore + DedupRegistry,{url} 锚幂等)→ offsets/events
    落数据根 ``telegram/``(按线分键,F8)。

    返回 None = graceful 空态(已留痕,**不拦服务**):品类缺失/装载失败、
    含非 telegram 引擎源、chat_id 缺失或被占、多 token 引用、双线凭据全缺
    (bot token 未配且 telethon session 未首登)。重量依赖(httpx/telegram
    包)函数内惰性导入:dev 直通模式零加载成本。
    """
    category_path = Path(ctx.plugins_dir) / _TELEGRAM_CATEGORY_FILENAME
    if not category_path.exists():
        myssia_log.stream_line(
            None, "stderr",
            f"sidecar: telegram 宿主未起(品类缺失 {category_path.name};"
            "telegram serve 常驻监控待品类就绪后重启生效)",
        )
        return None
    try:
        config = load_category_file(category_path)
    except Exception as exc:  # noqa: BLE001 — 装载失败留痕收空态
        myssia_log.stream_line(
            None, "stderr",
            f"sidecar: telegram 宿主未起(品类装载失败 {category_path.name}): {exc}",
        )
        return None
    non_telegram = [
        s.name for s in config.sources if s.engine not in ("telegram", "tg_web")
    ]
    if non_telegram:
        myssia_log.stream_line(
            None, "stderr",
            f"sidecar: telegram 宿主未起(品类含非 telegram/tg_web 引擎源: {', '.join(non_telegram)};批量采集走 run)",
        )
        return None

    import httpx

    from myssia.dedup import DedupRegistry
    from myssia.engines.fetch_base import FetchError
    from myssia.engines.telegram import filter_config_from_options
    from myssia.pipeline import _build_push_channel
    from myssia.push.base import SendContext
    from myssia.schema import CredentialResolveError, resolve_credential
    from myssia.secrets import get_backend
    from myssia.store.models import ItemRecord
    from myssia.telegram.events import TelegramEventLedger
    from myssia.telegram.filter import TelegramFilterPipeline
    from myssia.telegram.offsets import OffsetStore
    from myssia.telegram.serve import (
        TelegramPoller,
        TelegramServeHost,
        TelegramSourceBinding,
    )

    bindings: dict[str, TelegramSourceBinding] = {}
    token_ref: str | None = None
    try:
        backend = get_backend()
        for source in config.sources:
            if source.engine == "tg_web":
                continue  # web 线源走 assemble_web_manager(账号×群绑定,下方)
            options = (source.extra_params.get("engine_options") or {}).get(
                "telegram", {}
            )
            chat_id = options.get("chat_id")
            if not isinstance(chat_id, (str, int)):
                myssia_log.stream_line(
                    None, "stderr",
                    f"sidecar: telegram 宿主未起(源 {source.name} 缺 engine_options.telegram.chat_id)",
                )
                return None
            chat_key = str(chat_id).strip()
            if chat_key in bindings:
                myssia_log.stream_line(
                    None, "stderr",
                    f"sidecar: telegram 宿主未起(chat_id {chat_key} 被多源占用: "
                    f"{bindings[chat_key].source_name} / {source.name})",
                )
                return None
            ref = options.get("bot_token", "keychain:myia/telegram/bot-token")
            if token_ref is None:
                token_ref = str(ref)
            elif str(ref) != token_ref:
                myssia_log.stream_line(
                    None, "stderr",
                    "sidecar: telegram 宿主未起(单宿主只支持单 bot token;多 bot 请拆品类走 CLI serve)",
                )
                return None
            bindings[chat_key] = TelegramSourceBinding(
                chat_id=chat_key,
                source_name=source.name,
                source_url=source.url,
                pipeline=TelegramFilterPipeline(
                    filter_config_from_options(options), keychain_backend=backend
                ),
            )
    except FetchError as exc:  # filter_config_from_options 的结构化拒
        myssia_log.stream_line(
            None, "stderr", f"sidecar: telegram 宿主未起(过滤配置拒): {exc}"
        )
        return None

    try:
        bot_token = resolve_credential(token_ref or "", backend=backend)
    except CredentialResolveError:
        # bot token 未配 = bot 线不起(四步未完成的常态;是否还有救看 telethon
        # 用户线 —— session 已首登则单线起,双缺才整体空态,CLI 同门)。
        myssia_log.stream_line(
            None, "stderr",
            f"sidecar: telegram bot 线未起(bot token 未配 {token_ref})\n"
            "主人四步:BotFather 建 bot → /setprivacy 关闭隐私模式 → "
            "myssia secret set myia/telegram/bot-token → 拉进目标群(配好重启即活)",
        )
        bot_token = None

    db_path = Path(ctx.db)
    data_root = db_path.parent
    store = SQLiteStore(db_path)
    registry = DedupRegistry(store, tz=config.timezone)
    push_channel = None
    if config.push:
        push_channel = _build_push_channel(config.push[0], data_root=data_root)

    def _store_item(item: dict) -> bool:
        # CLI ``_cmd_telegram_serve`` 同款:dedup key={url} 锚幂等,metadata
        # 收余键,seen 双写(store + registry)。category = 源名→品类映射盖戳
        # (10-09-tg-category-entry:三线共用本 sink;主品类 telegram-groups
        # 与专用件 telegram-web 各归各行,未登记源 = None 不猜)。映射变量
        # 在装配段稍后赋值,闭包晚绑定,宿主首条入库前必已就位。
        key = str(item.get("url") or "")
        if not key or registry.is_seen(key):
            return False
        metadata = {
            k: v
            for k, v in item.items()
            if k not in ("url", "title", "content", "source")
        }
        store.save_item(
            ItemRecord(
                url=key,
                dedup_key=key,
                title=str(item.get("title") or ""),
                source=item.get("source"),
                content=item.get("content"),
                category=source_categories.get(str(item.get("source") or "")),
                raw=metadata,
            )
        )
        registry.mark_seen(key)
        return True

    async def _push_high_value(item: dict) -> bool:
        # CLI 同款:品类 push 首条通道;未配 push = 仅入库留痕(日报兜底)。
        # 深审 F14:返回 bool —— False = 通道未配,宿主不虚计 pushed(账本
        # 记 no_channel);True = 真实送达。
        if push_channel is None:
            myssia_log.stream_line(
                None, "stderr",
                f"sidecar: telegram 高价值条目仅入库(品类未配 push 通道) url={item.get('url')}",
            )
            return False
        now = datetime.now(config.timezone)
        context = SendContext(
            slot="am" if now.hour < 12 else "pm",
            date=now.strftime("%Y-%m-%d"),
            category=config.name,
            kind="immediate",
        )
        await push_channel.send([item], context)
        return True

    telegram_dir = data_root / "telegram"

    # bot 线(token 在才起;F8 指纹分键 offsets/events)。
    bot_host = None
    bot_ledger = None
    client = None
    if bot_token is not None:
        client = httpx.AsyncClient()
        bot_ledger = TelegramEventLedger(
            telegram_dir / "events.db", bot_token=bot_token
        )
        bot_host = TelegramServeHost(
            poller=TelegramPoller(client, bot_token),
            bindings=bindings,
            # 深审 F8:offsets/events 按 bot token 指纹分键 —— 桌面宿主与 CLI
            # serve(可能不同 bot)共享同一数据根时各 bot 各游标各账本;旧单键
            # offsets.json 由 OffsetStore 采纳一次即删。
            offsets=OffsetStore(telegram_dir / "offsets.json", bot_token=bot_token),
            ledger=bot_ledger,
            push_high_value=_push_high_value,
            store_item=_store_item,
            should_stop=stop.is_set,
        )

    # telethon 用户线(B4;session 已首登才试 —— 未首登是常态,留痕零阻塞)。
    from myssia.telegram.telethon_line import assemble_user_host

    user_host, user_ledger, user_note = assemble_user_host(
        telegram_dir, bindings, backend, _store_item, _push_high_value,
        data_root=data_root,
    )
    if user_note:
        myssia_log.stream_line(
            None, "stderr", f"sidecar: telegram telethon 用户线未起({user_note})"
        )

    # TG 网页线(C 线,W3;engine: tg_web 源按账号分组,帽/隔离/哨兵语义
    # 见 web_host 工厂;键超帽/未首登 = 留痕零阻塞,不动摇其余两线)。
    # 首真跑补(2026-10-08):sidecar 装配面并入专用件 plugins/telegram-web.yaml
    # 的 tg_web 源 —— 专用件是 C 线正户(G9 同名复用跨文件合法,重名唯一性
    # 按文件把守);主品类同名 tg_web 源在时专用件同名源跳过(同一群只跑
    # 一线判例);专用件装载失败/含非 tg_web 源 = 留痕不拦主品类源装配)。
    from myssia.telegram.web_host import assemble_web_manager

    web_sources = [s for s in config.sources if s.engine == "tg_web"]
    web_category_path = Path(ctx.plugins_dir) / "telegram-web.yaml"
    web_config = None  # 专用件缺位 = 无 C 线正户(映射只有主品类侧;先绑定防 UnboundLocal)
    if web_category_path.exists():
        try:
            web_config = load_category_file(web_category_path)
        except Exception as exc:  # noqa: BLE001 — 专用件坏档不拦主品类源
            myssia_log.stream_line(
                None, "stderr",
                f"sidecar: telegram-web.yaml 装载失败(web 线按 telegram-groups"
                f" 源装配): {exc}",
            )
            web_config = None
        if web_config is not None:
            group_names = {s.name for s in web_sources}
            for source in web_config.sources:
                if source.engine != "tg_web":
                    myssia_log.stream_line(
                        None, "stderr",
                        f"sidecar: telegram-web.yaml 含非 tg_web 源 {source.name}"
                        "(已忽略;批量采集走 myssia run)",
                    )
                elif source.name in group_names:
                    myssia_log.stream_line(
                        None, "stderr",
                        f"sidecar: telegram-web.yaml 源 {source.name} 与"
                        " telegram-groups.yaml tg_web 源同名(主品类侧保留,"
                        "专用件侧跳过 —— 同一群只跑一线)",
                    )
                else:
                    web_sources.append(source)
                    group_names.add(source.name)
    # 源→品类映射(落库盖戳用;主品类在前 = 同名源主品类侧优先,与上方
    # 「同一群只跑一线」去重同序)。
    source_categories = _telegram_source_categories(config, web_config)
    web_manager, web_note = assemble_web_manager(
        web_sources,
        telegram_dir=telegram_dir,
        data_root=data_root,
        backend=backend,
        store_item=_store_item,
        push_high_value=_push_high_value,
        should_stop=stop.is_set,
    )
    if web_note:
        myssia_log.stream_line(
            None, "stderr", f"sidecar: telegram TG 网页线未起({web_note})"
        )
    if bot_host is None and user_host is None and web_manager is None:
        myssia_log.stream_line(
            None, "stderr",
            "sidecar: telegram 宿主未起(bot token 与 telethon session 双缺;"
            "配好任一线后重启即活;TG 网页线 = myssia telegram web-login 零凭据开线)",
        )
        with contextlib.suppress(Exception):
            store.close()
        return None

    async def _run() -> None:
        # 三线并跑:一线致命不拖其余线(CLI ``_run_telegram_hosts`` 同门;
        # 致命者留痕上抛到线程边界,健康线继续服务;web manager 自带单键
        # 失效隔离 —— 哨兵告警停单键不退出)。
        try:
            tasks = [
                host.run_forever()
                for host in (bot_host, user_host, web_manager)
                if host is not None
            ]
            results = await asyncio.gather(*tasks, return_exceptions=True)
            for result in results:
                if isinstance(result, BaseException) and not isinstance(
                    result, asyncio.CancelledError
                ):
                    myssia_log.stream_line(
                        None, "stderr",
                        f"sidecar: telegram 一线致命退出(其余线已先留痕): {result}",
                    )
                    raise result
        finally:
            if client is not None:
                with contextlib.suppress(Exception):
                    await client.aclose()

    def _close() -> None:
        # 深审 F14:装配面收尾 —— 账本连接与 store 同批关闭(HTTP 客户端由
        # _run 的 finally + 宿主退出路径 poller.aclose 双保险收;web
        # manager 各键账本由其 close 统一收)。
        for ledger in (bot_ledger, user_ledger):
            if ledger is not None:
                with contextlib.suppress(Exception):
                    ledger.close()
        if web_manager is not None:
            with contextlib.suppress(Exception):
                web_manager.close()
        with contextlib.suppress(Exception):
            store.close()

    lines = [
        name
        for name, on in (
            ("bot", bot_host),
            ("telethon", user_host),
            ("web", web_manager),
        )
        if on
    ]
    label = (
        f"品类 {config.id},线 {'+'.join(lines)},群 {sorted(bindings) or '待实填 chat_id'},"
        f"数据根 {data_root}"
    )
    return _TelegramHostBundle(
        host=bot_host if bot_host is not None else user_host,
        run=_run,
        close=_close,
        label=label,
    )


def _start_telegram_host() -> None:
    """serve() 就绪后起 telegram 宿主:cron ticker 同款判例 + 两处刻意不同。

    同款:daemon 线程绝不占 serve 线程;幂等(锁内查-占,serve EOF 后重入
    serve 会重起);home 模式才起(dev/测试数据根落 cwd,常宿形态 =
    ``myssia telegram serve``);起动失败只留痕绝不拦服务。

    刻意不同(telegram/serve.py 设计 D1/D4):无 supervisor 重排 —— 宿主
    自带断线指数退避(transport/5xx 不崩),致命错误(401 token 失效 /
    409 双宿主互斥 / B4 起 telethon 线 session 失效)是配置态问题,蒙头
    重启只会复读失败,线程自退留痕、重启由人决定。与 CLI serve 的并存
    互斥 = Bot API 同 token 409。
    """
    global _TELEGRAM_THREAD, _TELEGRAM_STOP
    with _TELEGRAM_HOST_LOCK:
        if _TELEGRAM_THREAD is not None and _TELEGRAM_THREAD.is_alive():
            return
        try:
            ctx = _serve_context()
        except ProtocolError as exc:
            myssia_log.stream_line(
                None, "stderr", f"sidecar: telegram 宿主未起({exc.code}: {exc.message})"
            )
            return
        if ctx.home is None:
            return
        stop = threading.Event()
        try:
            bundle = _assemble_telegram_host(ctx, stop)
        except Exception as exc:  # noqa: BLE001 — 增强件,装配炸不拦服务
            myssia_log.stream_line(
                None, "stderr", f"sidecar: telegram 宿主装配失败(不拦服务): {exc}"
            )
            return
        if bundle is None:
            return  # 空态已在装配函数留痕
        run, close = bundle.run, bundle.close

        def _thread_main() -> None:
            try:
                asyncio.run(run())
            except Exception as exc:  # noqa: BLE001 — D4:致命上抛到线程边界留痕
                myssia_log.stream_line(
                    None, "stderr",
                    f"sidecar: telegram 宿主退出({type(exc).__name__}: {exc};"
                    "401/409 属配置态,调整后重启应用生效)",
                )
            finally:
                close()

        thread = threading.Thread(
            target=_thread_main, daemon=True, name="telegram-serve-host"
        )
        thread.start()
        _TELEGRAM_THREAD, _TELEGRAM_STOP = thread, stop
        myssia_log.stream_line(
            None, "stderr",
            f"sidecar: telegram 宿主已起({bundle.label};退出即停)",
        )


def _stop_telegram_host(join_timeout: float = 2.0) -> None:
    """关停 telegram 宿主(serve EOF / 测试夹具):置 stop → 有界 join。

    幂等;先摘全局引用再 join(重入安全)。宿主的 stop 在轮间检查点生效,
    长轮询挂起窗(至多 25s)内 join 超时即返回 —— daemon 语义兜底(线程
    下一轮自退/随进程退出),绝不为等宿主阻塞调用方(cron mid-fire 同
    哲学;offsets 逐轮持久,中途死零损坏,重拉由锚点去重兜底)。
    """
    global _TELEGRAM_THREAD, _TELEGRAM_STOP
    with _TELEGRAM_HOST_LOCK:
        stop = _TELEGRAM_STOP
        thread = _TELEGRAM_THREAD
        _TELEGRAM_THREAD = _TELEGRAM_STOP = None
    if stop is not None:
        stop.set()
    if thread is not None and thread.is_alive():
        thread.join(join_timeout)


def serve(stdin: Any | None = None, stdout: Any | None = None) -> int:
    """RPC 服务循环:逐行读请求、写应答/事件;stdin EOF = 干净退出 0。

    Args:
        stdin: 请求流(缺省 sys.stdin;测试注入 StringIO)。
        stdout: 协议流(缺省 sys.stdout;启动即捕获,事件线程直写此对象,
            不经 sys.stdout —— run/CLI 期间的重定向不会污染协议流)。

    Returns:
        退出码:EOF 正常结束 = 0(spec python/error-handling 契约)。
    """
    global _OUT
    _OUT = stdout if stdout is not None else sys.stdout
    # 统一日志(10-07-unified-logging 批1):serve 形态 configure(ring+盘+
    # stderr WARNING)+ 盘尾冷回填(design §5)——重启后 logs.tail 可翻上一程
    # 历史;必须先于任何 stream_line 消费者(种子/桥接/cron/telegram)。
    _configure_serve_logging(backfill=True)
    _startup_seed()
    _startup_remote_env()
    # cron ticker(10-04-hermes-cron B3):就绪后起、EOF 关停;lifetime =
    # serve。daemon 线程绝不占本线程(B10 队头阻塞);home 模式才起,
    # 失败只留痕不拦服务。
    _start_cron_ticker()
    # telegram 宿主(10-06-telegram-telethon 桌面接线批):同款生命周期
    # 判例;凭据缺失 graceful 不启动仅留痕(见 _start_telegram_host)。
    _start_telegram_host()
    source = stdin if stdin is not None else sys.stdin
    while True:
        raw = source.readline()
        if not raw:  # EOF:壳侧关闭管道 = 正常关停
            _stop_cron_ticker(join_timeout=1.0)
            _stop_telegram_host()
            return 0
        line = raw.strip()
        if line:
            _handle_line(line)


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "serve":
        sys.exit(serve())
    # 直通模式:退出码 0/1/2/3 契约由 myssia.cli.main 原样保证(v02 spike 兼容)。
    sys.exit(cli_main())
