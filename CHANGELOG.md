# Changelog

All notable changes to 世事 are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).
Earlier v0.x milestones are summarized in the README roadmap table and are not
repeated here.

## [Unreleased]

### Changed

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
