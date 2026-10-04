# Python 工程约定

## 技术底座

- 纯 Python + uv;核心**零重依赖**:SQLite 单文件(不用 Redis/PG),重引擎(crawl4ai/scrapling/skyvern)一律 extras 可选依赖(`shishi[crawl4ai]`,发行名 shishi),未装时结构化报错并提示安装命令
- 核心依赖共 **6 个**:httpx、selectolax、PyYAML、APScheduler、pydantic、**jinja2**(推送模板渲染,SandboxedEnvironment 沙箱;2026-10-01 grill Q2 定案);除这 6 个外,新核心依赖进 PRD 论证后才加
- 全异步采集:`httpx.AsyncClient`;调度 APScheduler(进程内,不引编排平台——规划定案)
- Python 3.11+;类型注解全覆盖;pyproject.toml 为唯一配置源

## 依赖分层与 src/ 边界(2026-10-01 主人问询后定案)

- `src/` 下**全部是 MYIA 自有代码,不含任何外部框架的引用或复制源码**;也没有 git 子模块/vendored 代码
- 外部项目只以两种方式接入:
  1. **核心必装轻量依赖**(pyproject `dependencies`,5 个):httpx、selectolax、PyYAML、APScheduler、pydantic——运行时作为库调用
  2. **引擎可选依赖**(pyproject `[project.optional-dependencies]`):crawl4ai / scrapling / firecrawl-py / skyvern / openai / vision(看图:ocrmac + rapidocr-onnxruntime + openai)——只 **import 对方的库写适配层,永不复制对方源码进仓库**(许可与体积红线);按 roadmap 分版本实装,v0.1 只做 L1/L2 + firecrawl
- engines/ 下 crawl4ai.py、scrapling.py、stealth_browser.py、llm_browser.py 当前为占位壳(仅 `__future__` import,未引任何第三方库);实装排期见各 `vXX-engine-*` 任务,提前实装属越界
- 判断一个依赖放核心还是 extras 的标准:核心流水线(L1/L2+分类+推送)能跑 = 核心依赖;只有特定引擎/通道需要 = extras

## 目录结构(src/myia/)

```
cli.py          命令入口(输出对 AI/人类双友好)
schema.py       12 节品类 YAML 模型与校验 + images: sidecar 节(管线图片处理环开关;detail_fetch/detail_max_items(10-03-detail-images)= 无图条目详情页追抓:开时 fetch 尾部按管线顺序追抓、HTML 同域 <img> 写回 metadata.images 进同一识图环,每 run 上限 detail_max_items(1-50,缺省 10)、串行每请求 ≥1s、10s/页超时,失败只写 metadata.detail_status 绝不阻管线,源级 images_detail_max_items 覆写 = 该源独立预算;$.images 错误前缀,不入 12 节契约)(AI 写 YAML 的地基)
pipeline.py     编排:fetch→classify→dedup→analyze→push(自研 ~200 行量级)
engines/        六层引擎:fetch_base(公共底座)+ registry(降级编排,含零结果 L3 首遇探测:auto 链 static_html 真零结果且无 hint 的首遇源一次性降级 crawl4ai 探测(30s 短帽、单 run 预算 3=`FetchContext.l3_probe_budget`),出条落 L3 回写 hint、零条/异常回滚空页语义零误报;指纹 skip 与显式 engine 配置永不探测,存量 hint 源零打扰;10-04-crawl4ai-l3)+ L1-L6 各文件一一对应
classify/       builtin(七大类+双信号,数据与代码分离)/ custom(YAML 规则)
dedup.py store/ SQLite + 去重注册表 + 变更基线;接口可插拔(PG 留位)
enrich/         LLM 精评(批量/缓存/预算护栏)
push/           通道(feishu_card/telegram/webhook/stdout)+ 阈值分级路由 + 消息平台层(directory/targets/delivery:通道目录+对象解析+定向投递)
cron/           定时任务底座(schedule 解析/store 存锁/jobs 生命周期/executions 账本/occurrences 去重/tick+ticker 调度/runner 子进程执行体/summary 投递;蓝本 Hermes cron/,MIT;见下方「定时任务底座」节)
vision/         看图:双引擎 OCR(ocrmac+rapidocr-onnxruntime)+ OpenAI 兼容 VisionClient + vision.yaml 配置 + collect.py 管线图片处理环(fetch 尾部下载→OCR→可选 VL 描述,品类 images: 节驱动,降级只写 image_status 绝不阻管线)+ models.py 模型仓管(HF mlx-community 直下免 convert:snapshot_download+local_dir 断点续传、HfApi 预检磁盘不足即拒、清单/删除/激活,huggingface-hub 惰性 import 在 extras)+ server.py mlx_vlm.server 代管(status 2s 探 / ensure 自起+健康等待 ≤120s:并发互斥锁、超窗杀孤儿不留、日志 >5MB 轮转;失败结构化上抛绝不阻管线)(extras myia[vision],惰性 import;10-03-vision-v2)
```

- 现有文件多为薄壳:任务是**填充**而非新建;新模块先在对应 PRD 登记
- plugins/*.yaml 是 schema 的端到端测试:发现 schema 缺口先回改 schema,不许插件私加字段

## 测试目录布局(2026-10-05 定案,task 10-05-tests-module-grouping)

- 主包测试**镜像 `src/myssia` 结构**落 `tests/<模块组>/`(现 14 组:alerts/classify/cli/cron/credhunter/desktop/engines/enrich/feedback/pipeline/plugins/push/store/vision);`tests/` 根只放跨切面件:conftest.py(全树唯一,`from conftest import` 助手链靠 pytest 装载它把 tests/ 送进 sys.path,子目录同享——**勿改回 `from tests.conftest import`**,历史见 718d56c)、共享 fixtures/、regen_push_targets_golden.py、docs/schema/secrets/skill_doc/smoke/trellis 守卫六件;**新测试按被测对象归组落位,不再新增根平铺**(test_cli_xxx → tests/cli/;分不清对象 = 横切,才许进根)
- 归组按「被测对象」不按 import 形态(import 了 pipeline 但测告警规则的归 alerts/);跨测试文件 import 必须同目录(test_yaml_editor_protocol_gaps ↔ test_desktop_sidecar_protocol 同在 desktop/);特性横切端到端归 pipeline/;`myssia-classifier` 的语义测试随包走 `myssia-classifier/tests/` 且**零 `myssia.` 依赖**(直引 `myssia_classifier`,连 caplog logger 名一起改;直引符号面经 `from myssia_classifier import …` 全量核验);主包 `tests/classify/test_classifier_package.py` 只测 shim 同一性与独立发行契约
- 路径取值:子目录文件取仓库根 `Path(__file__).resolve().parents[2]`、取共享 fixtures `parents[1] / "fixtures"`;根留文件维持 `parents[1]`/`parent / "fixtures"`。**移动测试文件后必跑全量** `uv run --no-sync python -m pytest -q`;数量不跌 ≠ 零丢失,零丢失要 collect-only 归一 diff 验(方法与工件见任务档 evidence/)
- 布局红线:根 `testpaths = ["tests", "myssia-classifier/tests"]` 保持 CI 单命令门禁(`ci.yml` 零路径硬编码);子目录**不加 `__init__.py`**(代价 = 测试文件 basename 全局唯一,新增重名即 pytest 模块冲突,改名解决);`.trellis` 归档与 CHANGELOG 历史里的旧路径不改写;`myssia-classifier` sdist 随附 tests 属刻意默认(G3 决议),wheel 仍仅含包体

## 消息平台层(2026-10-03 定案,task 10-03-hermes-messaging)

- **蓝本移植,不 vendor 原文**:源自 Hermes(NousResearch/Hermes-Agent,MIT)gateway 的通道目录/对象解析/定向投递逐文件重写为 MYIA 风格,模块 docstring 标注上游文件路径与 MIT 归属,上游对照表登记在各子任务档;不整块拷贝原文、不引 git 子模块。各平台一律 httpx 直连官方 API,不引平台 SDK(核心 6 依赖红线不动);接不上官方 API 的平台进 extras 并结构化报错
- **通道目录**(`push/directory.py`):`ChannelEntry(platform, chat_id, name, type, thread_id, last_seen)`;数据根下 `channel_directory.json`(tmp+rename 原子写)+ `channel_aliases.json` 别名覆盖层(load 与重建双向生效,重建后别名仍在——Hermes 同款回归点);重建为按平台桶整体替换,被动平台(Telegram 无列表 API)靠 `merge_entries` 增量积累;手工直编目录文件不保证保留,别名文件才是持久覆盖层;损坏/不可写退化为内存态,绝不阻塞推送
- **对象解析**(`push/targets.py`):spec 形态 `platform:名称或id`,解析顺序 = 显式 id/@username 直达(平台 `parse_direct_ref` 钩子,不经目录)→ 目录精确 id → 精确名(大小写不敏感)→ 唯一前缀(多义即未命中);别名是目录改名层,不是独立解析层级;未命中抛 `TargetResolveError` 内嵌候选列表(MYIA 增量,上游靠交互式 list);纯字符串/前缀匹配,无任何 eval
- **定向投递 + 死信**(`push/delivery.py`):按解析后对象逐一发送(immediate 单条 / digest 每(通道×对象)一卡),单对象失败不阻断同批;死信为错误分类制(Hermes 原味):`forbidden` 与 chat 级 `not_found` 单次硬失败即标 dead,瞬态错误(超时/网络/限流)不标;dead 期间跳过并记结构化日志(不发告警卡);投递成功一次即自愈;无阈值、无配置口
- **schema 同平台约束**:`push[].targets` / `push[].route[].targets` 元素平台前缀须与条目通道一致(内置字面映射 `feishu_card→feishu`、`telegram→telegram`),不一致在配置加载期即拒;跨平台 = 写多条 push 条目;targets 在场时 legacy `target` 可省;不配 targets = 现行为零迁移(golden 回测逐字节等价)
- **注册与刷新**:平台适配器挂现有 `Channel` 协议(`supports_targeting` / `parse_direct_ref` / `discover_directory`),`PLATFORMS` dict 注册表与 `CHANNELS` 并排(feishu/telegram 已接入);刷新三层 = run 前节流懒刷(>5 分钟且有已注册平台才发现,失败退回旧目录+告警)+ CLI `myia channels refresh/list` + 桌面按钮;无发现 API 的被动平台归 passive 上报(退出码 0),非失败

## 桌面发行数据根(v1.1.1 定案,task 10-03-v111-desktop-paths)

- **CLI 相对路径默认(`myia.db`/`plugins`)是仓库开发契约,永不在 CLI 层改动**;桌面上下文的解析全部收口在 `desktop/entry.py` 的 `_serve_context()`,优先级:显式 params > `MYIA_HOME` env(Tauri 壳 main.rs spawn 注入)> 冻结 .app bundle 探测 > dev 回退 cwd
- 平台数据根 `myia_home()`:macOS `~/Library/Application Support/MYIA` / Windows `%APPDATA%\MYIA` / Linux `~/.myia`;home 模式解析即建 `<home>` 与 `<home>/plugins`(全新数据根上 health/doctor 必须空态 OK,不得 plugins_dir 报错)
- 首跑种子:home 模式 && plugins 空 && 无 `.seeded` 标志 → 拷随包 `Resources/plugins/*.yaml`(官方品类 YAML 四件套);标志在即永不复种(尊重用户删除)。dev 模式零动作
- 市场面(`myia plugin list`,InstalledPluginStore)与品类 YAML 平铺共用 `<home>/plugins` 不冲突(health 扫描非递归);官方插件 = 品类 YAML 形态,经 health/doctor 可见,plugins.list 首跑空是合法态
- 改路径行为必须同步 `tests/desktop/test_desktop_sidecar_protocol.py` 的上下文/种子用例;发布前必跑「真实安装冒烟」(cwd=/ 全方法矩阵),mock 层绿不算数(v1.1 教训)

## 代理池池化(2026-10-04 定案,task 10-04-proxy-pool)

- **声明形态(混形兼容)**:全局配置 `pools` 节每池两种形态——字符串(v0.2,等价单上游池)或映射 `{upstreams: [...], max_failures?, probe_interval?}`;凭据只走 `env:`/`keychain:` 引用(明文加载期拒载红线),校验全挂 `load_proxy_pools` 的 LoadError 通道(`invalid_pool_upstreams`/`invalid_pool_policy`/`unknown_pool_field`),零第二套规则;`schema.py` 的 `pool:<名称>` 语法零改动
- **运行时(`engines/fetch_base.py:ProxyPoolTransport`)**:每池每 run 一个 facade(`FetchContext.pool_transports`,duck-type `request`/`get`/`stream`/`aclose`,**显式 **kwargs 透传**——图片环 per-request timeout 与 `follow_redirects=False` 走这条路);顺序游标轮换,transport 失败即换下一个可 admit 上游(消耗源 retry 预算);被动健康:连续 transport 失败计数达 `max_failures`(默认 3)摘除,成功(<400)清零,HTTP 状态失败不计数不清零;摘除过 `probe_interval`(默认 300s)由流量自然触发**半开单飞**试炼(成功归队/失败立即重摘除;`trial_in_flight` 清位 finally 覆盖含 CancelledError——sidecar 壳超时取消不留永久占坑);懒建 client 构建失败**不计数直接冒 `ProxyConfigError`**(依赖缺失真相不被健康模型吃掉);生命周期 = run,不落库不跨 run
- **每池熔断(派生态)**:全部上游摘除且无到期半开 → 请求零网络抛 `ProxyPoolExhaustedError`(`proxy_pool_exhausted`,带自愈时刻),mount 期与 retry 循环内两处同语义;**不睡等半开**(快速失败交还调用方,下一 run 自然重试)
- **不变量**:proxy_* 家族四类 `proxy_error`/`proxy_timeout`/`proxy_network`/`proxy_pool_exhausted` 全部 startswith("proxy_"),registry 的「不清 hint + 短路降级链」对四类一致(**registry.py/schema.py 零改动是红线**);轮换/健康收敛在 facade 内,降级链不感知池内部;浏览器三读者(crawl4ai/stealth_browser/scrapling)消费 mount 时刻的 `_active_proxy_url`,会话内不轮换
- **行为变化披露**:字符串(单上游)池失败语义从「逐源各自重试」变为「3 连败摘除 → 池熔断快速失败」——docs/en+zh schema.md 全局配置节同款披露文字,升级说明必须带上
- **回滚注记**:revert 后 `upstreams` 映射形态 YAML 会被旧加载器以 `invalid_pools` 结构化拒载(非静默)——回滚前需把池化 YAML 还原为字符串形态

## 桌面 Windows 发行(2026-10-04 定案,task 10-04-windows-build)

- **依赖平台标记红线**:vision extra 的 `ocrmac` 恒带 `sys_platform == 'darwin'` 标记(macOS Vision 独占,Windows 无 wheel,裸装拉 pyobjc 链必炸——生产 run 37117015528 实锤);动 vision extras 时标记不可丢;`myia-core.spec` 的 ocrmac collect_all 有同款 darwin 门(卫生项);uv.lock 重锁保持镜像 URL 体系并人工核 diff
- **产物与 latest.json 单写者**:desktop-release.yml 的 windows-msi 为正式 CI 目标(无 continue-on-error、timeout 60,失败=run 红但不牵连 mac 发布);msi 产物上传前改 ASCII 名 `myia_<版本>_x64.msi`/`.msi.sig`(GitHub 剥非 ASCII 资产名);latest.json 只由 release-finalize 归聚 job 单一产出(`needs: [macos-dmg, windows-msi]` + `if: always() && mac result 门`,darwin-aarch64 条目恒在、windows-x86_64 按产物存在条件并入),mac/windows job 不得自写(双写者竞态);dispatch 于分支跑时版本回退 tauri.conf.json,不以分支名当 semver
- **签名与冒烟口径**:v1 不购代码签名证书,SmartScreen「更多信息→仍要运行」+ Defender 误报白名单走 README 安装节文档化放行;Windows 真机冒烟七项清单(安装/放行/首跑种子/keychain→DPAPI 链/黑窗/passive 升级/单实例)归主人侧,交付判据 = CI 绿 + artifacts(10-04-windows-build prd)

## 定时任务底座(2026-10-04 定案,task 10-04-hermes-cron)

- **蓝本移植,不 vendor 原文**:源自 Hermes(NousResearch/Hermes-Agent,MIT)`cron/` 子系统,逐文件重写为 MYIA 风格、模块 docstring 标注上游文件路径与行号段;**上游对照表与偏离表(D1-D14)登记在任务档 design.md §1/§6,改 cron 代码前必读**——「偏离表之外全照抄」是纪律。croniter 不进依赖红线:cron 时刻计算 = APScheduler `CronTrigger` + POSIX dow 归一化层(`normalize_dow` 展开 0/7=周日、列表/区间/步进/环绕为周名;探针实证 APScheduler 数字周几为周一系,不归一化错位一天);cron 表达式限恰好 5 段
- **存储布局(不进 myia.db)**:数据根 = `--db` 父目录(`CronJobs.for_db`),全部落 `<数据根>/cron/`——`jobs.json`(job 注册表,tmp+rename 原子写 + 跨进程建议锁;他进程磁盘新增的未知 job 合并不覆盖)、`executions.db`(cron 专属 SQLite 执行账本,`run_summary_json` 摘要快照随终态)、`output/<job_id>/`(运行文档+stderr,倒序裁剪留 50)、`tick.lock`/`paused.marker`(estop)/心跳标记族;**SQLiteStore SCHEMA_VERSION 零改动是红线**
- **at-most-once 与多宿主**:tick 在文件锁内**先推进 next_run_at 再派发**(锁被他宿主持有 = 静默 return 0);fire claim TTL 300s 认领;`cron serve`(监督守护线程,崩了 respawn)/桌面 sidecar ticker(仅 home 模式)/手动 `cron tick` 三宿主共存;cron fire 撞桌面 run 单飞锁 = 跳过本 fire(`skipped_busy` + `cron.skipped` 事件,用户手点优先);同 db job 派发串行、不同 db 并行
- **执行体 = 子进程**(偏离 D11,对齐 sidecar「从不构造 Pipeline」铁律):spawn `myia run <品类> --json`(start_new_session 自成进程组;墙钟 run_timeout 缺省 3600s,超时 killpg SIGTERM→宽限→SIGKILL);退出码 0/2/3 映射 ok/failed/partial(3 算成功附注);摘要投递复用 push 平台层 directory+targets+delivery,deliver spec = `local`/`feishu:群名`/`telegram:id`/`stdout:debug`(内存缓冲+日志回显,协议流零污染);SendContext kind=`cron_summary`(受控扩值);投递失败记 `last_status="delivery_failed"` 不动 failure_streak
