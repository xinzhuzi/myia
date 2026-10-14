# Changelog

All notable changes to 世事 are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).
Earlier v0.x milestones are summarized in the README roadmap table and are not
repeated here.

## [Unreleased]

### Changed

- **评分模型缺省 glm-4-flash → glm-5.3-flash 全仓升级**(2026-10-13,主人令
  「最差也应该是 GLM-5.3-Flash」):源码缺省/仓库种子/实机 9 品类/UI 占位/
  测试 49 处(5dcf59e,golden 快照按数据保留);schema 表/示例/zero-cost
  双语文档同步,看图 glm-4.6v 视觉模型不动(b1294ba);设置页 AI 评分模型
  行去行话——enrich.model/yaml.save/doctor 回显全链人话化(0896b8a,主人
  实测「没理解」即判例)。
- **wechat_local 引擎换轨 localdb 通道**(2026-10-13,10-12-weixin-feed-
  channel,主人令):channel 字段二分支(engine_options.wechat_local,缺省
  pixel 向后兼容)——localdb 走桥解密副本只读(零截窗零 AX,与 pixel 分支
  隔离),源级水位增量窗;exit 21 key_unavailable=结构化 skip 不算 failure,
  指引一键取钥脚本(aac331f)。
- **微信消费侧模块归位 myssia/wechat 与 messaging/wechat**(2026-10-14,
  10-14-wechat-module,主人令对标 TG 形态解耦):push 三件(5474d4d)、
  sidecar 双件(b3f29df)、notify+engine 归位+registry 直载(9064447);
  桌面微信屏族 14 件归 messaging/wechat 子域(481b1e6);破 sidecar⇄
  push_local 顶层回环(ed8178c)。
- **feed 三级界面美化**(2026-10-14,10-14-feed-l3-beautify):标题锚定/
  时间线节奏/日期胶囊描边/进场淡入(4ee4d06)。
- **Tests reorganized by module; classifier now ships its own tests**(2026-10-05,
  10-05-tests-module-grouping):主包 `tests/` 由 94 文件平铺重组为镜像
  `src/myssia` 的 14 个模块组(alerts/cli/cron/credhunter/engines/push/store/
  vision…),根仅留跨切面测试与共享 fixtures;`myssia-classifier` 首次自带
  `tests/`(sdist 自下一版起随附,wheel 仍仅含 `myssia_classifier` 包体);
  根 `testpaths` 双目录,CI 单命令全量门禁不变,3604 收集零丢失实证。
- **Third full-chain rename: myia → myssia**(2026-10-04 终版命名决议:myssia 为
  项目唯一正式名——GitHub 仓库 xinzhuzi/myia、PyPI 发行名 myssia /
  myssia-classifier、CLI `myssia`、Python 模块 `src/myssia`、classifier 模块
  `myssia_classifier`、插件 id `myssia-*`;「世事」仍为中文名,README 标题作
  「myssia(中文名:世事)」)。镜像前两轮改名(58cb40b myia→shishi、0a085cc
  shishi→myia)的改动对象逐一照抄:src 树 92 模块、tests/desktop/entry.py/plugins
  的 import 与文档引用、pyproject scripts/wheel packages/workspace、
  build-sidecar.sh/myssia-core.spec、Dockerfile ENTRYPOINT、compose 服务名与
  ghcr.io/xinzhuzi/myia 镜像、desktop-release 资产别名 `myssia_*`、tauri
  updater endpoint 与内部工件名(`binaries/myssia-core`、`com.myssia.app`)、
  uv.lock 全量再生成。运行时数据身份保留旧名以兼容既有装机:钥匙链名空间
  `myia/<scope>/<name>`(keyring service `myia`)、`~/.myia` 插件安装根、
  `MYIA_PLUGIN_DIR`/`MYIA_HOME` 环境变量、桌面数据根
  `~/Library/Application Support/MYIA`、`mainBinaryName=MYIA`、默认 UA
  `MYIA/0.1`。myia 与 shishi 从此只是历史(docs/demo 录制物料与本文历史章节
  按时代锁定保留)。

### Added

- **微信本机桥:取钥器全链与库密钥钥匙串化**(2026-10-13~14,
  10-13-wechat-key-subsystem / 10-13-wechat-keyprovider):密钥获取固化进桥
  组件——C 收集器入件(零 exec、只读 mach 四调用,bin/ 首用时自动编译)+
  memsearch 重写(收集器→熵预筛→并发 sqlcipher 试开→HMAC 交叉验证)+
  setuid 自愈件(单用户本机读自己微信内存的威胁模型,sudo rm 即回归)+
  一键脚本 v2,0.4.0(46a4fac);自愈失败退避——不可闭合态 30min 冷却门、
  损坏即忘却、成功清戳,0.4.1(289d96f);localdb 查询适配 4.1.15 分表+
  取钥器协议,0.4.2(19c606b);copy_ttl_hours 0=永不过期(5342f82);密钥
  状态与获取编排命令 0.5.0(3e74788);设置页「取钥器」配置面(32433f3)。
  库密钥钥匙串化:resolve_keys 两级(钥匙串 myia/wechat/db-keys 优先/文件
  兜底)+keys-migrate/unmigrate 原子迁移(HMAC 验真门+回读逐字节门,生产
  实测拦住 security -w 128B 截断并回滚),生产 20 钥已迁、明文退役
  (b4fb27e)。
- **微信本机桥:解密副本近实时与只读查询族**(2026-10-13,
  10-13-wechat-features 系):压缩消息解码补自管 3.12 主路 zstandard
  (f51d5ac,0.4.3);解密副本源新即重建+并发单飞+竞态重试,监控近实时
  (c1fde1b,0.4.4);发送者上屏真名不显 wxid(f1b849f,0.5.1);localdb
  sns 命令——朋友圈动态与互动通知只读查询(59ff041,0.6.0);群信息只读
  命令(843cc24,0.7.0)。
- **微信本机桥:send_text 发送真身**(2026-10-13~14,10-13-wechat-features /
  10-14-wechat-send-text):wxauto 三支柱热激活 UI 驱动落地(bba02c8,
  0.7.0,主人热激活批令);三源合体升级,收编并行全家桶线(dc0cd98);
  0.8.3 真机深测五缺陷修复与白名单双发闭环(0bec58d);成功逻辑全链入册
  ——时序七步/侧栏优先+搜索兜底/浮窗判据/三刀/五层验证(d004b92,
  0.8.4 真机验证版)。
- **微信六屏全家桶桌面集成层**(2026-10-14,10-13-wechat-features 六子):
  Rust 导出三件+UI 六屏+引擎 notify 件+stats sidecar+docs+config 入库
  (7748884)。六域验收回执:C1 聊天记录导出(b93382a:keyset 9821 行对拍、
  六格式 3391 行==SQL COUNT、SIGTERM 取消安全)、C2 统计与年报(e17c737:
  chat total=111062 契约自洽、annual --all 319ms、缓存 sha256 确定性)、
  C3 媒体与朋友圈(8213963:rows=4419/media_nodes=7065、vitest 886 全绿)、
  C4 联系人(8a16c71:16/16 真库 PASS、六桶 22092==COUNT、游标零重漏)、
  C5 通知与撤回(3ad6184:notify-scan 真库 454 会话、红线词表 grep 零)、
  C6 HTTP API(2974b68:门控真库深分页 p95≤45.3ms、tests 730 全绿零回归)。
- **微信监控 UI 全链与群信息面板**(2026-10-13,10-13-wechat-monitor-ui /
  10-13-wechat-groupinfo):密钥状态/获取密钥流/监控台群列表/一键安装取钥器
  (51b9ddf);群信息面板+全量导出(JSON+CSV),三级监控台群设置与成员
  上屏(dd8ee11)。
- **朋友圈线:引擎通道→信息流合流→独立品类**(2026-10-13~14,
  10-13-wechat-sns-feed / 10-13-wechat-sns-merge / 10-14-wechat-sns-5min):
  wechat_local 引擎 sns 通道——朋友圈动态与互动通知入情报流(id 强锚+
  水位增量,073698a);动态+互动合流上屏,发帖人必显——双源折叠单会话行+
  时间线 first_seen 混排+动态泡发帖人小签+同人合并组(8f47727,主人令);
  聊天气泡时间线设计重做——泡顶渠道名退役/发信人泡内 8 色 hash 小彩签/
  同人合并组/760px 居中列,TG/微信同套泡形(5afde42,主人令「搞的好看
  一点」);grill 深化批五缺陷修复——实体净化/SQL 契约防护/notices 域
  收缩等(c9affad);朋友圈拆独立品类 weixin-sns 挂 */5 全天档(28bf86c)。
- **六线收口:代理池面板/凭证猎手面板/点选建源向导/Windows 启动即亮窗**
  (2026-10-14,10-14-proxy-pool-panel / 10-14-cred-hunter-panel /
  10-14-visual-source-builder / 10-14-win-startup-show):桌面四档交付入库
  (3a518f9)。
- **系统原生确认弹窗与带 app 图标通知**(2026-10-14,
  10-14-native-system-dialog / 10-14-notify-app-icon):确认弹窗全量切系统
  原生弹窗,system-confirm 统一入口(18c2f51);原生通道异常加固——ACL 拒/
  插件故障=安全缺省取消(f9d726a);macos_notify 换壳代发——通知带世事
  app 图标/归组/点击唤起(bde22d8)。
- **组件安装体验:安装状态进按钮+排队自动装**(2026-10-13,
  10-13-component-install-ux):单飞弹错改 FIFO 受理,安装态壳侧化切屏不丢
  (0fdc12f);接力链终态原子化+链中止清队——grill 复审抓出双 pip 并发
  竞态(98ffb5e);组件行描述精简为一句以依赖开头(043932e,主人判例)。
- **firecrawl 三层 endpoint 序**(2026-10-13,engines):本地自托管探测优先
  (127.0.0.1:3002,命中即用),miss 落显式配置云端兜底,皆无缺省空炮;
  三层专项用例(3601dd6,主人「本地→下载→云端」二修裁决);兜底改嵌套块
  形态——自查抓出点键静默丢配置(97a0541)。
- **五特性完整双语文档**(2026-10-14,10-14-product-docs-deep):微信本机
  工作台(六屏+通知线整机)/代理池(后端+面板+G10)/凭证猎手(引擎+
  G11 红线)/建源向导(五步),全部主张带代码锚,BILINGUAL_PAGES 入守卫
  (461a77a,tests/test_docs 143 绿);文档新鲜度刷新+遗留清账三件
  (afdb52e)。
- **定时任务管理屏**(10-04-cron-ui):桌面侧栏「采集」组新增「定时任务」屏
  (`/cron`,Clock 图标,源管理之后),照 Hermes web 控制台 CronPage 抄的
  可视化管理皮——ticker 活性条(正常灰字含数据根/僵死黄条/急停红条,
  急停全部=红钮+确认 Dialog、恢复全部=红条入口的双向操作)、job 列表
  (排程人话 `schedule_display` 直读、逾期红标 15min 宽限、上次状态四态
  badge、`all` 切换含暂停/终态、行内展开运行历史带 `run_summary_json`
  摘要)、创建/编辑双 Dialog(schedule 五种模板 chips 仍可改、category 走
  `yaml.list` 下拉选择器且坏文件行禁选带标+手输兜底、parse 错误原文回显)、
  行内动作四件(立即运行=排队语义 notice「≤60 秒内开始」、暂停可填
  reason、恢复、删除确认);刷新为事件驱动(`cron.completed`/
  `cron.skipped` 入 `SidecarEvent` 联合→notice 横幅+重拉,logs 屏
  `eventToRow` 穷尽守卫同步适配为 runId=null 系统行)+手动刷新+本地
  1min 时钟 tick 驱动逾期标走时,零 interval 轮询。零协议变更:cron.*
  九方法与两事件系 10-04-hermes-cron 已交付底座,本批纯前端薄壳
  (types.ts 镜像对账 35→45 方法,门面十方法入共享 `api`)。
- **Feed inline search takes over the browser find shortcut** (10-04
  fe-gap-census R1): Mod+F (⌘F / Ctrl+F) in the feed screen now focuses the
  inline search box and selects its text instead of the webview find bar, and
  Escape clears both the box and the committed query immediately instead of
  waiting out the 300 ms debounce (the native `type="search"` Esc reset
  doesn't fire for controlled inputs, so it's handled explicitly).
- **`alerts.fired` joined the desktop `SidecarEvent` union** (10-04 fe-gap-census
  R2): the protocol side has shipped the run-terminal replay (`entry.py`
  `_replay_alerts_fired`), so the event shape now rides the typed event stream —
  logs screen gains an exhaustive-guard formatting branch (system summary row,
  not replayed into the run-domain feed), and the messaging alert panel narrows
  the union directly instead of casting.
- **Item read-state protocol surface** (10-04-read-state-server, G9): three
  sidecar methods moving the desktop feed's read/starred/later state from
  webview localStorage into the server-side store — `store.state.mark`
  (`{keys: [dedup_key…], marker: read|starred|later, value}` → `{updated}`;
  rows sharing a dedup_key through dated-key rotation are marked together,
  matching the old localStorage itemKey semantics; idempotent explicit-value
  writes; `updated` is the SQLite rowcount — matched rows, same-value rows
  included, reported verbatim; keys capped at 2000 as a misuse guard,
  whole-library semantics must go through `mark_all`), `store.state.mark_all`
  (`{marker, value, category?}` → `{updated}`; category is exact equality
  like `list_items` — no query parameter, per the grill Q3.2 ruling that
  LIKE-in-UPDATE is scope creep; omitting category marks the entire library
  including unpaged items, which is where the feed's "mark all read"
  whole-library semantics now come from), and `store.state.import`
  (`{states: {key: {read?/starred?/later?}}}` → `{imported, skipped}`; the
  one-time localStorage migration gate — keys are triaged as direct
  dedup_key / `id:<n>` resolved through the items table / anything else
  (including `id:<url>`) honestly counted as skipped without resurrecting
  pruned entries; idempotence lives in the server-side `store_meta` flag
  `feed_state_imported_at` — the server flag is the single source of truth
  because webview data can be wiped independently, and an already-set flag
  answers `{imported: 0, skipped: 0}` without touching the items table). The
  `store.items`/`feed.export` JSONL projection now carries
  `read`/`starred`/`later` booleans (additive; CSV column set unchanged; the
  collect pipeline never persists state — `save_item`'s column list excludes
  the three columns, so state is only ever set through this surface).
  Protocol version bumped to 10 (57 → 60 methods; hermes-cron landed v9
  first, this batch took the next integer per the alert-rules racing
  precedent of reading `PROTOCOL_VERSION` at start of work).
- **Desktop cron sidecar surface** (10-04-hermes-cron, B3): nine sidecar
  methods wiring the desktop shell into the new `myia.cron` subsystem —
  `cron.list` / `cron.create` / `cron.edit` / `cron.pause` / `cron.resume` /
  `cron.run` / `cron.remove` / `cron.status` / `cron.runs`, all thin wrappers
  over the same `CronJobs`/`ExecutionLedger` API layer the `myia cron` CLI
  uses (identical semantics and error codes; job references accept id or
  name with `cron_ambiguous_job`/`cron_job_not_found` structured refusals;
  create reuses the CLI's gates — full `load_category_file` early-failure as
  `cron_category_invalid`, absolute category-path storage, timezone chain
  job > category YAML > local). `serve` now also hosts a cron ticker
  (daemon thread started once the RPC loop is ready, never on the serve
  thread itself — the head-of-line blocking rule; supervised via
  `SupervisedTickerThread` plus a dedicated supervisor thread polling
  `restart_if_dead`; home mode only — dev fallback keeps the repo cwd clean
  and defers to `myia cron serve`; coexists with the CLI host through the
  tick file lock and fire claims, Hermes' native multi-host design). Two
  events: `cron.skipped` — a cron fire that collides with the desktop
  single-flight run lock skips that fire (grill Q2: the advanced slot is
  consumed, nothing queued or rolled back, user-initiated runs win;
  `last_status="skipped_busy"` is recorded by the tick layer as a success
  semantics that leaves the failure streak untouched) and `cron.completed`
  — per-fire completion with the run summary lifted straight from the
  execution ledger's `run_summary_json` (no second parse of subprocess
  stdout; `summary: null` when the best-effort ledger write failed, never
  fabricated). The reset-between-tests fixture now stops the ticker
  (thread-leak guard). Protocol version bumped to 9 (48 → 57 methods).
- **Run success-rate trend** (10-04-desktop-b234, G6): new `runs.trend` sidecar
  method serving the dashboard's success-rate sparkline — a per-day × per-status
  aggregation over the `runs` table (`substr(started_at, 1, 10)` UTC calendar
  day, same window semantics as `store.trend`: `days` clamped to [1, 90]
  defaulting to 14, optional `category` filter, `db` fallback), answering
  `{days: [{date, total, statuses: {<status>: count}}]}` oldest → newest with
  only the days that have data. Aggregation happens server-side because
  `runs.list` caps at 200 rows — under cron scheduling plus manual runs a
  30-day window can exceed that limit, and a frontend-side aggregation over a
  truncated list would silently distort the series. `statuses` groups the
  open vocabulary verbatim (real vocabulary: running/success/partial/failed);
  excluding `running` from the rate denominator is a frontend assembly
  decision (dashboard `successRateSeries`), not a protocol behavior. Protocol
  version bumped to 8.
- **Alert-rules protocol surface** (10-04-alert-rules, Stage D): four sidecar
  methods for the desktop alert-rule manager — `alerts.list` (full rule list
  with per-rule `fired_count` / `last_fired_at` derived from the `alert_fired`
  history table, so counts survive the full-replacement save), `alerts.save`
  (whole-array replacement covering create/edit/enable-toggle in one call,
  following the `push.write` precedent: every entry passes the shared
  construction gate — name / scope / whitelisted-AST `when` syntax / action /
  action_config shape — and any failure is a structured `alert_rule_invalid`
  with `{index, field, reason}` and zero writes for the whole batch; ids are
  stable across replacement, rows missing from the payload are deleted while
  their fired history stays), `alerts.delete` (definition row only — hit
  history is a fact), and `alerts.test` (a **dry** evaluation that never sends
  and never records a fired row: draft `rule` or stored `rule_id` × synthetic
  `item` / stored `item_id` / latest-item default, answering `matched`,
  `muted` (current effective mute = category watchlist + feedback-tuned 0.0
  words), expanded `actions` (push channel resolution from the category's
  `push[]` with degrade reasons, or tag labels), `eval_error` when the
  runtime evaluation fails, and `already_fired` for the stored-rule form;
  real sends keep going through the existing `push.test`). New `alerts.fired`
  event: at each non-dry run's terminal state the sidecar parent replays rows
  recorded by the subprocess's alert pass via `list_fired(since=run.started_at)`
  — one event per new hit, emitted before `completed`, shape
  `{rule_id, rule_name, item_id, dedup_key, title, action, action_status, ts}`
  (querying the store rather than parsing subprocess logs keeps the replay
  free of log-format coupling). Engine/storage groundwork: `myia.alerts`
  package + `alert_rules`/`alert_fired` tables (schema v7 migration) +
  `Pipeline._alert_pass` attach point.
- **Sidecar protocol version bumped to 7** (`PROTOCOL_VERSION`,
  desktop/entry.py): covers the alert-rules batch's four methods and the
  `alerts.fired` event above (43 → 47 methods).

- **Messaging screen** (commit `4be1325`): a sixth desktop screen (「消息」) for the
  messaging platform — platform-grouped channel directory (name / type / last-seen /
  dead-letter badge), inline alias editing, per-platform directory refresh, and a
  push-rule panel that picks concrete targets (`platform:name` specs) from the
  directory. Empty and disconnected states follow the existing screen patterns.
- **Four sidecar protocol methods**: `channels.list` (directory + aliases + dead +
  rules merged view), `channels.refresh` (per-platform `discover_directory` with
  bucket replace; old bucket untouched on failure), `channels.alias` (set/delete),
  and `push.write` (full push-array replacement per file, following the
  `sources.write` pattern: path fencing → comment-preserving text surgery →
  re-parse deep-equality gate → `load_category` gate → `.bak` → atomic write;
  validation failures leave the file untouched).
- **Sidecar protocol version bumped to 2** (`PROTOCOL_VERSION`, desktop/entry.py):
  the unified bump that was deferred while the `yaml.*`/`image.*` method families
  merged in parallel; v2 covers everything merged since v1 (10 → 27 methods).
- **v1.1.2 desktop parity batch — protocol methods** (10-03-v112-desktop-parity;
  absorbed into the v2 ledger above, no further bump per the one-bump merge
  policy): `run.cancel` (process-group kill — SIGTERM, 5s grace, SIGKILL
  fallback; signal-terminated runs report a distinguishable `cancelled` status),
  `runs.list` (runs-table read, newest first — run history survives a sidecar
  restart), `secret.delete` (mistyped-credential removal; `secret_not_found`
  on the second delete), and `sources.test` (async trial-fetch job fenced like
  `yaml.*`; the 120s per-source CLI timeout equals the shell's hard per-request
  timeout, so a synchronous implementation is forbidden by construction —
  results arrive via the new `test.completed` event).
- **v1.1.2 desktop parity batch — `store.items` cursor & search**: composite
  cursor `before` (strictly-older `first_seen`) + `before_id` (tuple
  comparison) so same-timestamp item bursts larger than one page can paginate
  to exhaustion, plus `query` (NOCASE LIKE over title/content/source). The
  feed screen now paginates with the composite cursor (the old
  since-reuse + client-dedup + added==0 stop is kept only as a defensive
  backstop). This lands the merged C1×G1/G3 shape agreed with the feed-ux
  batch (its Python half is superseded by this change).
- **Desktop shell respawn** (`desktop/src-tauri/src/main.rs`): the sidecar is
  automatically restarted after a crash — exponential backoff (1/2/4/8/16s,
  max 5 attempts, counter resets after 10s of stable life) with the lifecycle
  published as shell events (`sidecar://state`: respawning/online/dead);
  a new `sidecar_restart` command (idempotent) backs the top-bar badge's
  probe→restart→re-probe recovery path, so a killed sidecar no longer bricks
  the UI with permanent `sidecar_not_running` errors.
- **v1.1.2 desktop parity batch — second slice, protocol methods**:
  `feedback.mark` / `feedback.list` / `feedback.stats` (B2 — desktop feedback
  entries via the same `myia.feedback` code path as the CLI with
  `channel="desktop"`, so `myia feedback list` sees the same rows;
  payload keys aligned with the CLI's row/stats shapes) and `store.trend`
  (B4 — per-day item counts over `first_seen`, UTC calendar days, window
  clamped to [1, 90]). No `PROTOCOL_VERSION` bump of its own: the batch rides
  the existing ledger per the one-bump merge policy (currently at 5 after the
  vision-v2 bump).
- **v1.1.2 desktop parity batch — second slice, UI**: feed-card 👍/👎 feedback
  (greyed out after marking — manual marks carry no idempotency key), a
  dashboard feedback-stats card, a dashboard collection-trend card (hand-rolled
  SVG sparkline, 7/14/30-day window switch, zero new npm deps; the
  `fillDailyCounts` aggregation is vitest-covered), a top-bar global
  "run once + cancel" control (C12; category follows the top-bar selector,
  ✕ calls `run.cancel`), and a settings「评分与反馈」partition (B3/C11 —
  per-category `enrich.enabled` toggle + `enrich.model` writeback via
  `yaml.read → comment-preserving text surgery → yaml.save (mtime optimistic
  lock) → doctor re-verify`; `budget_per_run` shown read-only as the guard
  rail; push-channel declarations get a link to the YAML editor screen, and
  the global pools writeback stays deferred pending the yaml-editor decision).
  `version` now also reports `app_version` (C10 — the shell injects
  `MYIA_APP_VERSION` from `package_info()`, i.e. the single source of truth in
  `tauri.conf.json`; dev/CLI report `null` honestly), surfaced in the top-bar
  connection tooltip.
- **feed-ux batch — three sidecar protocol methods** (10-03-feed-ux):
  `feed.export` (export the current filtered view as JSONL/CSV; the sidecar
  writes the user-picked `dialog.save()` path directly — data never transits
  the webview, only that one file is written; `export_path_invalid` /
  `export_write_failed`), `schedule.preview` (Apify-style next-runs preview
  per category via `build_cron_trigger`, pure computation, count clamped to
  [1,20]; a category without a schedule reports `schedule: null`, not an
  error), and `push.test` (sends one synthetic item through a real channel —
  credential resolution follows the existing `env:`/`keychain:` reference
  chain and channel `PushSendError` codes pass through verbatim; the stdout
  channel's card lands in the response `preview` field so the serve-mode
  protocol stream stays clean).
- **Sidecar protocol version bumped to 3** (`PROTOCOL_VERSION`,
  desktop/entry.py): covers the feed-ux batch's three methods above
  (27 → 30; the `store.items` cursor/search groundwork landed earlier under
  the v2 ledger via the C1×G1 merged shape).
- **feed-ux batch — feed screen UX** (10-03-feed-ux): server-side item search
  (G1 — debounced 300ms + Enter submit, `query` rides the pagination cursor so
  it covers the whole store, not just loaded pages; the counter line reports
  the server-search × local-filter layers honestly), inline card expansion
  with full content and metadata (G2, closing census C9), 「打开原文」 via
  `@tauri-apps/plugin-shell` `open()` — a scoped `shell:allow-open`
  capability allowing only `https?://` URLs (the v1.1 review posture of
  zero shell-execute grants for the webview is preserved; non-http(s) item
  URLs render no button), and view export (G3 — JSONL/CSV format toggle,
  `dialog.save()` with a dated default name, path/count feedback line).
- **feed-ux batch — dashboard / sources / settings** (10-03-feed-ux): a
  per-category 「跑一次」 button on the dashboard category cards (G4 —
  `run.start` + `completed`-event state machine copied from the feed empty
  CTA; busy disables the button, failures show inline), a 「排程一览」
  section on the sources screen (G4 — per-category `schedule.preview` fired
  concurrently via `Promise.allSettled`; a single category's failure collapses
  only its own row), the top-bar category selector is now wired (C8 — options
  from `health().plugins` deduped by id, selection lifted to the layout and
  applied as server-side `store.items` filtering via router outlet context;
  the dead `defaultValue="all"` skeleton comment is gone), and a 「发送测试」
  button in the settings push form (G5 first half — `push.test` with the
  form's current channel; when scope+credential-name are filled the target
  reference `keychain:myia/<scope>/<name>` is composed, otherwise the
  channel's default env chain is exercised as-is; ok/fail badge + structured
  error line).

### Changed

- **Naming reversal: `myia` is the technical identity again** (owner decision,
  2026-10-04): MYIA is the repo / PyPI / CLI / module name, 「世事」 the Chinese
  brand name — romaji `shishi` survives only inside Chinese-name annotations
  (e.g. 「MYIA(中文名:世事)」). Everything the 1.1.1-era rename touched is
  precisely reverted: module tree `src/shishi` → `src/myia` (all imports,
  `-m` subprocess refs, plugin adapters, loggers), `[project.scripts]
  myia = "myia.cli:main"`, wheel `packages = ["src/myia"]`, extras
  self-references `myia[…]`, PyPI names `myia` / `myia-classifier` (both still
  unpublished — nothing to migrate), Docker image `ghcr.io/xinzhuzi/myia`,
  GitHub repo `xinzhuzi/myia`, sidecar `_m_version` name `myia` (protocol
  methods and versions untouched), desktop release ASCII aliases back to
  `myia.*`. The historical sections below keep the `shishi` names they
  actually shipped with.
- **Versioning reset to 0.0.1** (owner decision, 2026-10-03): the version
  sequence restarts from `0.0.1`. The `v1.1.1` git tag and its GitHub Release
  were removed, and every version source was reset accordingly: root and
  classifier `pyproject.toml`, `myia.__version__`, `tauri.conf.json`,
  `Cargo.toml` (+ `Cargo.lock`), plus the `myia-classifier` dependency
  window (`>=0.0.1,<0.1`). The `1.x` sections below remain as the historical
  record of the retired sequence.
- **Tag-driven releases** (10-03-tag-release): publishing is now triggered
  exclusively by pushing a `v*` tag. The Docker workflow no longer publishes on
  every push to main — GHCR receives only `X.Y.Z` + `latest` per release (and
  pre-release tags do not move `latest`); PyPI publishing rides the same tag
  with a version-consistency guard (tag must match both `pyproject.toml`
  versions) and attaches wheels/sdists to the GitHub Release once publish
  succeeds. **Status as of the v0.0.1 tag (2026-10-03): not yet landed** — the
  two PyPI runs on the tag both failed at the trusted-publisher gate (runs
  37115937696 / 37117015481; shishi/shishi-classifier pending publishers not
  registered yet), so `pip install shishi` is unavailable and the Release
  carries the four desktop assets only (`shishi_0.0.1_aarch64.dmg`,
  `shishi.app.tar.gz{,.sig}`, `latest.json`). Wheels/sdists land after the
  owner registers the pending publishers and re-runs the failed jobs.
  TestPyPI rehearsal remains available via manual dispatch.

### Fixed

- **微信桥 0.8.4 真机打磨**(2026-10-14,10-14-wechat-send-text 轮):AX 门
  边界五组对照关闭+doctor 提示改诚实(90f130d);搜索网络区抓障三修
  (eeef485);followups 三件+搜索中文化(5d6f9a9);OCR 降级链三刀加固
  (ed0d844);刀4 正文慢落退避重读(d95663c);全半角 NFKC 归一双点修复
  (995879e);消息区回读几何修复——下缘 0.70→0.715,最新气泡底部窄带
  漏扫(d1af26f)。
- **微信桥 0.3.2 前置门勘误**(2026-10-13,10-12-weixin-feed-channel 生产
  轮):AX 检查退出 UI 前置门、屏幕录制接管(独立码 16)——修前像素链被
  不需要的 AX 权限拦死,生产 06:00 run 108 ax_permission_denied 实锤
  (fe9e5cb)。
- **feed 三级左栏平台隔离**(2026-10-13,主人令「微信是微信,TG 是 TG,
  不能混在一起」):imGroupCards 按 activeChannelKind 同平台收窄,收回
  10-12 微信线的 tg+wx 混列(2035b36)。
- **UI 文案人话化·全屏族**(2026-10-13,10-12-ui-wording-audit):词不达意
  审计 46 项改词/旗舰族统一/10 处失效指引修复——仪表盘/日志/源管理/定时/
  配置编辑(f574a57 系 7 件)、消息/账号/凭据屏群(b96c37b)、情报流
  (3340178)、设置与壳层(0fe0cbb)。
- **后端错误文案人话化与种子同步**(2026-10-13,10-13-recommendations-exec):
  错误文案衔接前端词表(9c35ad0);9 条「文本手术/零写入」同族漏网补齐,
  统一「无法保存:…;文件未做任何改动」句式(10588a0);telegram-web 种子
  同步实机——baidu 源关键词+handgame/baidu 两源(d657be9),tg_web 示范件
  把守同步(ab7f5b7)。

<!-- v0.0.4 草稿·窗口注记(主人评审用,定版时随裁):本批口径=2026-10-13
     T00:00:00 起入库 187 件,用户可见面入正文,docs(task)/chore(task)/
     research 等内部件不计;v0.0.3..HEAD 全差量 426 件,其中 10-08→10-12 的
     239 件差量(browser-module / tg 系 / feed detail 等)不在本批口径,扩窗
     与否留主人裁决。G10 一键化本体(ebfb34e,2026-10-05)落在 v0.0.3 tag
     (2026-10-07)窗口内,如实不重复入账——本批 G10 面=代理池面板+深文档
     G10 节。storage/py314 域截至本草稿未落库,主人推 tag 前若落库须补录
     对应条目。 -->

## [0.0.1] — 2026-10-03

- **First release of the reset version sequence** (owner decision, 2026-10-03 —
  see the versioning-reset entry under Unreleased; the retired `1.x` sections
  below are the historical record). Released under the renamed distribution
  identity `shishi` / `shishi-classifier` via the tag-driven channels, with
  every version source at `0.0.1`:
  - **GitHub Release `v0.0.1`** (tag → commit `96751a5`): four desktop assets —
    `shishi_0.0.1_aarch64.dmg`, `shishi.app.tar.gz` + `.sig` (updater-signed),
    and `latest.json` (`version: 0.0.1`) for the signed update channel.
  - **GHCR**: `0.0.1` + `latest` image tags per release (no more per-push
    `sha-*` accumulation).
  - **PyPI: not landed yet** — both PyPI runs on the tag failed at the
    trusted-publisher gate (runs 37115937696 / 37117015481); `shishi` /
    `shishi-classifier` wheels/sdists are neither on PyPI nor attached to the
    Release until the owner registers the pending publishers and re-runs.

## [1.1.1] — 2026-10-03
- **定名「世事」,发行身份全面更名**:产品名 MYIA→世事(桌面端已于本版本完成);PyPI 发行名 `myia`→`shishi`、`myia-classifier`→`shishi-classifier`(均系首次发布,零迁移);CLI 命令 `myia`→`shishi`;GitHub 仓库更名 `MYIA`→`shishi`(旧链接自动重定向);Docker 镜像 ghcr 同步更名。Python 模块名 `myia`/`myia_classifier` 本版本过渡保留,下版本一并更名。


### Fixed

- **Desktop data paths** (commit `45639c3`): the installed app lost all data
  paths when launched from Finder (`cwd=/`) — three competing path policies,
  no bundled plugins, no first-run seed. Now unified behind a single rule:
  explicit params > `MYIA_HOME` env (injected by the Tauri shell) > frozen
  `.app` bundle detection > dev cwd fallback. Repo/CLI behavior is unchanged.
  - Official category YAMLs (ai-news / wool / stocks / gpu-prices, plus the new
    demo below) are bundled as app resources and seeded into the app data root
    on first run (idempotent via a `.seeded` marker).
  - A virgin data root reports a healthy empty state (and `first_run` for UI
    guidance) instead of a `plugins_dir` error; the feed screen offers a
    first-run "run your first plugin" call-to-action.

### Added

- **Out-of-the-box demo plugin** (`plugins/myia-demo.yaml`, bundled): a
  zero-credential GitHub new-stars watcher over the GitHub Search API
  (single unauthenticated JSON request). A fresh install shows real data on
  the very first plugin run — no `config_error`, no secrets to fill in.
- **Per-item AI summary on the feed** (desktop, protocol v6 `feed.enrich`):
  a card action that runs the enrich pipeline on a single item and shows the
  composite score, per-dimension scores and model — cached hits cost zero
  tokens; unconfigured enrichment degrades to a fix-it hint instead of an
  error.
- **Logs screen power tools** (desktop): re-run a past run from its header
  (replays the same yaml/dry/db flags), filter runs by category and status,
  and search within logs with match highlighting.
- **Feed batch actions & keyword pinning** (desktop): mark all loaded items
  read/unread in one click; pin any feed card's keywords into a category
  YAML watchlist straight from the card (mtime-guarded, cross-file id
  checked).
- **Signed update channel**: Tauri updater with signature verification
  (endpoints + pubkey injected by the release CI) and a new "Software update"
  card in the desktop settings screen — check for updates, review the notes,
  download & install (passive), then relaunch. Failures surface as structured
  errors.
- **Version alignment**: `shishi`, `shishi-classifier` and the desktop app all
  report `1.1.1` (`shishi --version` matches the .app bundle version).
- **PyPI dual packages**: `shishi` and `shishi-classifier` publish via a manual
  release workflow (TestPyPI rehearsal first, then PyPI).
- **README**: download & install section pointing at GitHub Releases with the
  macOS right-click-to-open Gatekeeper guidance (the installer is not
  Apple-notarized; builds are public and auditable), real-data desktop
  screenshots, and install instructions corrected to the uv-workspace path.

## [1.1.0] — 2026-10-02

### Added

- **Desktop app** (Tauri 2 shell, Python core embedded as a PyInstaller
  sidecar): JSON-RPC sidecar protocol (10 methods + streaming events) and a
  React 19 + Tailwind 4 UI with five real screens — dashboard, sources, feed,
  logs, settings — plus updater configuration and a tag-triggered release
  pipeline producing signed `.app`/`.dmg` artifacts (`desktop/UPDATER.md`).
- **Settings screen credential forms** (LLM / proxy pool / push channels):
  values go only through `secret.set` into the OS keychain (macOS Keychain /
  Windows DPAPI), never into component state or YAML; `doctor` verification
  is rendered inline.
- **Source-managed plugin architecture** (in-process plugin tier, zero
  docker): Photon OSINT as a pinned submodule with an in-process adapter,
  a lightweight proxy-pool fetcher, monitor/credentials as remote plugins,
  douyin/maxun documented as server-only; plugin compose files moved out of
  `plugins/` into `docker/plugins/`.
- `shishi skill install` / `skill path` commands (four agent targets,
  `--link` / `--force`).

### Notes

- In-card feedback buttons (desktop), the settings feedback toggle and
  collection-trend charts are **not** part of this release — the feedback
  loop works via the CLI (plus Telegram/Feishu callback receivers); the
  desktop pieces are scheduled for v1.2.

## [1.0.0] — 2026-10-02

### Added

- First public release: the complete pipeline
  (fetch → classify → dedup → analyze → enrich → push) with a fully
  documented 12-section YAML schema, six fetch engines on an auto-degrading
  ladder (L1 `direct_api` → L6 `llm_browser`), the seven-category keyword
  classifier, SQLite single-file storage with retention/VACUUM, threshold-
  routed push (Feishu card / Telegram / webhook / stdout), keychain-backed
  secrets, an agent-facing skill sheet, and bilingual (zh/en) docs kept
  consistent with the code by tests.

[0.0.1]: https://github.com/xinzhuzi/myia/releases/tag/v0.0.1

<!-- 1.x sequence retired 2026-10-03 (versioning reset to 0.0.1): the
     v1.0.0/v1.1.0/v1.1.1 tags and their GitHub Releases were deleted, so the
     [1.1.1]/[1.1.0]/[1.0.0] headings above are kept as the historical record
     with no link targets (verified: `git tag` lists only v0.0.1 and
     releases/tags/v1.1.1 returns 404). -->
