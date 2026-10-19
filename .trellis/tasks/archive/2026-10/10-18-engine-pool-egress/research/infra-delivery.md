# 基建面探索结论(数据根/HTTP 栈/打包/代理池链路/风险)

> **出处**:本件由规划员于 2026-10-18 落盘,内容 = 本轮工作流「探索员」基建面只读取证结论原样收编(探索员只读不落盘,由规划员代写)。探索员实证方式:静态代码 + 文件系统 + `ps` 实测,未跑任何网络探测/doctor/打包。
> **规划员定点复核**(2026-10-18,见文末「复核记录」):对承重结论抽样核对路径:行号,全部一致。

## 1. configDelivery(数据根解析与蓝本送达)

【数据根解析】两侧同口径:显式 MYIA_HOME env 永远赢。
- CLI 侧:`cli.py:230-237` cron --db 缺省 `$MYIA_HOME/myssia.db`
- `desktop/entry.py:581-616` `_serve_context` 优先级 = 显式 params > MYIA_HOME env > .app bundle 探测(`myssia_home()`,`entry.py:502-511`:darwin=~/Library/Application Support/MYIA)> dev 回退 **home=None**(db/config 用仓库默认 DEFAULT_DB_PATH/DEFAULT_CONFIG_DIR)。〔定稿勘误 2026-10-18,拷问 F9:原句「dev 回退 cwd」与代码不符——entry.py 该函数 docstring 亦自称「dev 回退 cwd」,以代码为准 home=None;「dev 零变化」结论恰因 home=None 成立(design 3.3 的 `ctx.home is not None` 门直接挡住),不会命中仓库根的 config/proxy-pools.yaml〕
- Rust 侧:`desktop/src-tauri/src/main.rs:599-604` data_root 同优先级,平台后缀 `main.rs:621-629`(macOS=Library/Application Support/MYIA,注意是字面 MYIA 不是 bundle id com.myssia.app);spawn sidecar 时注入 MYIA_HOME(`main.rs:415-418`)

【蓝本→数据根】`tauri.conf.json` bundle.resources 逐文件映射 config/*.yaml(`desktop/src-tauri/tauri.conf.json:45-63`);装机后每次 serve 启动 `_startup_seed`(`entry.py:653-674`)→ `migrate_legacy_plugins_dir`(旧 `<home>/plugins` 平铺配置一次性迁 `config/`,`config_layout.py`)+ `_seed_first_run`(`entry.py:619-650`):缺哪件补哪件、**绝不覆盖已存在文件**(手改件逐字节保留),`.seeded` 只是首次时刻记录。

【关键缺口】resources 清单里没有 proxy-pools.yaml(实测提取 bundle resources 配置件列表核对)——装机版蓝本不随包带 proxy-pools.yaml;装机 doctor 的 config_auto 缺省池文件是 `<home>/pools.yaml`(`entry.py:1515-1518`,非 `config/proxy-pools.yaml`,且本机该文件不存在);桌面 run.start 仅 params.config 显式给才拼 `--config`(`entry.py:3661-3662`,无自动发现);cron job 的 config_path 是逐 job 可选键(`cron/runner.py:190-192`,UI cron-form 可填,types.ts:926),run/test 子进程逐次 spawn。

【装机后改品类 yaml 生效动作】数据根 `config/*.yaml` 每次 cron fire 都是新起 `myssia run` 子进程读盘(`cron/runner.py:175-193`),改完下一 fire 即生效,无需重启 app;唯一例外是若在跑 `--loop` 常驻(桌面形态不用)。改仓库 config/ 蓝本只影响未来装机/升级补种且不覆盖既有件;proxy-pools.yaml 想随包须先加进 tauri.conf.json resources。

【真跑实况(只读实测)】ps:87086=/Applications/世事.app/Contents/MacOS/MYIA,87092=<数据根>/python/bin/python3 -m myssia_desktop_entry serve;ps eww 87092 见 MYIA_HOME=/Users/zhengbingjin/Library/Application Support/MYIA、MYIA_BUNDLED_PLUGINS=/Applications/世事.app/Contents/Resources/plugins。数据根 config/ 已有手放的 proxy-pools.yaml(652B,10-17 21:55);cron jobs.json 16 个 job 里仅「AI资讯」config_path 指向 config/proxy-pools.yaml,其余全 None;装机版品类中仅 ai-news.yaml 有 `proxy: pool:clash`(:299),其余源全部 `proxy: direct`;装机 app 版本 0.0.3,identifier com.myssia.app;WebKit 数据目录 ~/Library/WebKit/com.myssia.app 在场,~/Library/Caches/MYIA/(含 telegram-web)在场。

## 2. httpStack(HTTP 客户端栈)

【客户端构造】唯一的 run 级共享直连客户端:`pipeline.py:1309` `client = self._injected_client or httpx.AsyncClient(timeout=self._timeout)`——只传 timeout,无 headers/无 ssl 参数;CLI test 同构(`cli.py:3372` _build_async_client);doctor 探测另建 per-upstream `httpx.AsyncClient(proxy=..., timeout=...)`(`cli.py:3159`)。图片环自建下载 client(`pipeline.py:2052-2054`,timeout=10s,follow_redirects=False)。

【UA/请求头】引擎构造期 resolve_headers 解析 env:/keychain: 凭据引用(`fetch_base.py:356-391`);无源级 user-agent 时补 `DEFAULT_USER_AGENT="MYIA/0.1 (config-driven intelligence hub)"`(`fetch_base.py:135,2095-2096`)——这就是被爬站看到的直连缺省 UA。robots.txt 拉取(RobotsCache._fetch,`fetch_base.py:1498-1503`)裸 client.get 无 UA(httpx 缺省 python-httpx)。scrapling stealth 后端刻意不透传 MYIA UA(指纹同源,`scrapling.py:414-417`)。

【超时重试】缺省 30s(DEFAULT_TIMEOUT_SECONDS,`fetch_base.py:134`),per-request 可覆写(_send_with_retry timeout 形参);重试=源 retry+1 次,RETRYABLE={429,500,502,503,504}(`fetch_base.py:144`),退避 exponential/linear/none 封顶 60s(`fetch_base.py:2372-2379`)。

【TLS 可插性】不可插:全链 httpx 标准栈,构造点零 ssl_context/transport 参数,httpx.AsyncClient 的 TLS 指纹=Python ssl 默认(被 CF 类指纹墙识别的形态)。

【curl_cffi 依赖面】不在任何依赖面:pyproject core+extras 无(`pyproject.toml:13-113`,仅 scrapling extras);uv.lock 全锁 rg 'curl' 零命中;桌面锁 desktop/resources/requirements-lock.txt 亦无(该锁=core+llm+telethon+browser extras 经 `uv export --frozen --no-dev --no-emit-project --no-hashes --extra llm --extra telethon --extra browser` 冻结,锁头注释在文件前 26 行)。唯一关联:scrapling 引擎 docstring 提其 static 后端=AsyncFetcher curl_cffi(`scrapling.py:22`),但需另装 "scrapling[fetchers]"(`scrapling.py:86-87`),uv.lock 里 scrapling 0.4.15 的 deps 也无 curl-cffi。

【若引入 curl_cffi 的挂点】最顺路径=仿 ProxyPoolTransport 的 duck-type 面(request/get/stream/aclose+**kwargs 透传+is_proxy_egress,`fetch_base.py:969-1006`)造一个 curl_cffi facade 挂到 `_active_client`,或直接替换 `pipeline.py:1309` 的 run 级 client;受影响引擎=全部骑 _active_client 的(direct_api/static_html/prompt/saas[zenrows,scraperapi]/firecrawl/llm_browser 后端调用/reddit/searxng/feishu)+ RobotsCache(同 facade)+ 图片环(`pipeline.py:2052/2060`);浏览器引擎(crawl4ai/scrapling stealth/stealth_browser)与 urlwatch 不经此栈(浏览器有自己的指纹、scrapling static 已是 curl_cffi);注意 RobotsCache/_send_with_retry 消费的是 httpx.Response 对象,facade 需保持该形状(curl_cffi 响应需适配)。

【装机自管 py 带新依赖】加 pyproject extras → uv export 重出 requirements-lock.txt 随包 → 壳侧 `pyenv.rs:353-364` 依赖指纹漂移检测(装机指纹≠随包清单 sha256 → DepsStale 态),用户到 设置→Python环境 重跑安装链即补上(pip install -r 幂等)。

enrich/push 层无 proxy 支持(rg 实证零命中)——LLM 评分与推送出网仍直连,不在池覆盖面。

## 3. packaging(打包与换装)

- 本地:`just build-desktop`(justfile:42-43)= `npm --prefix desktop run tauri build`(beforeBuildCommand 链自带 vite 前端构建+随包源码树 __pycache__ 清理)
- CI:`desktop-release.yml:131` `npx tauri build --bundles app,dmg --config src-tauri/tauri.release.conf.json`(macos-14 arm64,msi 为 Windows 正式目标)
- 产物:`desktop/src-tauri/target/release/bundle/dmg/myssia_<版本>_aarch64.dmg` 与 `bundle/macos/myssia.app`(.tar.gz+.sig 更新包);README.md:228-248 装机说明(运行时与依赖不随包,首跑设置页在线装钉版 cpython 3.12.7+锁版依赖到数据根 python/)

【换装既有套路】以 10-15-feed-local-images 任务档为在案判例(`.trellis/tasks/10-15-feed-local-images/verification.md:14`):新包放 /Applications/世事.app,旧包备份为 /Applications/世事.backup-<ts>.app,新包本地 ad-hoc 签名+`codesign --verify --deep --strict` 通过,换装前后确认 MYIA 进程为空再动(不静默杀用户在跑实例)。

【验源】裸 grep/rg 对打包件失效——frontendDist 静态资产以 brotli 压缩内嵌进 Rust 主二进制(`desktop/ui-src/e2e/package_smoke.py:24-28`,Cargo.lock:322 brotli),正确验源=Rust 符号/中文消息字节或行为验证,或在案判例的形态:从安装件 Mach-O 提取内嵌 dist 比对 SHA256(package_smoke.py X0 步,verification.md:12-13 含安装件 Python 文件与源码逐字节一致比对)。

【WKWebView 缓存】webview 数据目录=~/Library/WebKit/com.myssia.app(实测在场;bundle id=`tauri.conf.json:6` com.myssia.app)、~/Library/Caches/MYIA/(实测含 telegram-web);前端换装后如 UI 未刷新按套路清 WKWebView 缓存(该步骤来自任务书背景;仓内未检到成文 runbook,属口传套路)。

## 4. proxyPool(代理池链路)

【声明与加载】池只在全局配置声明一次:`config/proxy-pools.yaml:12-13` 现有唯一池 `clash: http://127.0.0.1:7897`(本机 Clash Verge 混合口,注释记 2026-10-17 实测 google 302/reddit RSS 200)。加载器 load_proxy_pools_file→load_proxy_pools(`fetch_base.py:899-946, 800-896`):文件须 UTF-8、YAML 重复键拒载;池名语法 [A-Za-z0-9_-]+;上游 scheme 白名单 http/https/socks5/socks5h(`fetch_base.py:157`,socks 需 httpx[socks] 已在 pyproject:14);userinfo 只允许 env:/keychain: 引用、明文凭据装载期即拒;字符串形态=单上游池,映射形态可逐池覆写 max_failures(默认3)/probe_interval(默认300s)。品类 YAML 只写 `proxy: pool:<名>` 引用,凭据永不进品类件。

【注入链】CLI:`myssia run/test/cron` 各带可选 `--config <全局yaml>`(`cli.py:459-463`);_resolve_pools(`cli.py:3326-3336`)加载后注入 Pipeline(proxy_pools=,`cli.py:1560-1567` → `pipeline.py:1114-1116`)→ _context_for_run 注入 FetchContext.proxy_pools(`pipeline.py:1231-1239`)。不传 --config 时 proxy_pools=None,pool: 源在 fetch 前结构化报 proxy_pools_not_configured。

【分流点】BaseEngine.fetch()(`fetch_base.py:2135-2141`)→ resolve_proxy 语法/residential 门(:394-425)→ _prepare_proxy_transport(:2143-2190)是 direct 与 pool:<名> 的唯一分岔:direct 保持共享 context client(共享 httpx.AsyncClient,`pipeline.py:1309` 裸构造);pool:<名> 则取池共享 facade ProxyPoolTransport(FetchContext.pool_transport_for,:1986-2024,同池多源复用一个 facade,凭据此刻解析),ensure_operable() 熔断预检,然后 _active_client=facade、robots 缓存切同出口(robots_for_pool,:2037-2050),_active_proxy_url 固定为 mount 时刻上游供浏览器引擎直读(`crawl4ai.py:370/375` proxy_config、`stealth_browser.py:727-728`、`scrapling.py:410-411`;会话粘性不轮换)。图片下载环同口径:pool 源的配图/详情追抓骑同池 facade,解析失败降级 direct(`pipeline.py:1964-1992, 2042-2060`)。

【健康/熔断(v1.2 池化)】ProxyPoolTransport(`fetch_base.py:969-1243`):顺序游标轮换(每次从 cursor+1 环扫,D1);被动健康零后台任务——transport 级失败(httpx.TransportError 含 Timeout)连续计数,达 max_failures(3)摘除,成功(状态<400)清零复位,4xx/5xx 不计数(代理已送达,锅是源的);摘除上游 probe_interval(300s)后由流量自然触发半开单飞试炼;全部上游摘除且无到期半开=池熔断,零网络抛 ProxyPoolExhaustedError(带 recovery_in_seconds;`fetch_base.py:252-278, 1116-1135`)。生命周期=一个 run(D7):run 收尾 aclose_pool_transports(`pipeline.py:1474`),健康态不落库不跨 run。代理链失败分类独立于源失败:classify_proxy_transport→proxy_error/proxy_timeout/proxy_network(`fetch_base.py:314-328`),_wrap_proxy_transport_failure 包装(:2343-2370);降级链遇 proxy_* 前缀失败不清 engine hint 且短路全链(其余引擎骑同池必同错,`registry.py:348-366`)。

【urlwatch 为何只 direct】UrlwatchEngine._fetch_impl 结构化拒 proxy≠direct(`urlwatch.py:357-362`,proxy_unsupported):抓取由场景件 adapter 在子进程跑(`uv run --with urlwatch` 直连,场景件零第三方铁律;模块头注释 :24-25「不做配了代理池却悄悄直连的出口错配」);渲染通道经 sys.executable 跑 render_crawl4ai.py 同样直连。

【doctor 形态】`myssia doctor --config <全局yaml> [--probe-timeout 10]`(`cli.py:903-954`):_doctor_proxy(`cli.py:4173-4199`)加载池→_probe_proxy_pools(:3140-3200)逐池 resolve_upstreams 后全上游 asyncio.gather 并行探测(总耗时≈最慢上游,为塞进桌面 sidecar 120s 壳超时);探针 check_proxy_connectivity(`fetch_base.py:1274-1357`)打 https://api.ipify.org/?format=json 取出口 IP,结果含 ok/latency/status/exit_ip/error_type,凭据一律 mask_proxy_url 打码。失败→warning 级 finding(代理挂≠源死,`cli.py:3726-3747`)。桌面侧另有 proxy.probe/proxy.history 面板方法(proxy_panel.py,复用 _m_doctor,快照落 `<home>/proxy-probe-history.jsonl`)。

## 5. keyFiles(关键文件锚点)

- `src/myssia/engines/fetch_base.py`:135(DEFAULT_USER_AGENT)、:157(SUPPORTED_PROXY_SCHEMES)、:394-425(resolve_proxy 语法门)、:800-946(load_proxy_pools(_file))、:969-1243(ProxyPoolTransport)、:1274-1357(check_proxy_connectivity+ipify 探针)、:1939-2062(FetchContext.pool_transport_for/robots_for_pool/aclose)、:2135-2190(fetch→_prepare_proxy_transport=direct/pool 分流点)、:2291-2341(_send_with_retry 骑 _active_client)
- `src/myssia/pipeline.py`:1041,1114-1116,1231-1239,1309(Pipeline proxy_pools 注入与 run 级 httpx client)、:1964-1992,2049-2060(图片环按源骑池 facade)
- `src/myssia/cli.py`:428-463(run --config)、:903-954(doctor parser)、:1548-1574(_cmd_run 注池)、:3131-3200(client 工厂+并行探测)、:3326-3336(_resolve_pools)、:4025-4077,4173-4199(_cmd_doctor/_doctor_proxy)
- `src/myssia/engines/urlwatch.py`:24-25,357-362(仅 direct+子进程直连理由)
- `src/myssia/engines/registry.py`:83-91,107-179,348-366(链与 proxy_* 短路)
- `src/myssia/engines/scrapling.py`:22,86-87,410-411(curl_cffi 关联与 proxy 透传)
- `src/myssia/engines/crawl4ai.py`:370-375(浏览器代理挂点)
- `src/myssia/engines/llm_browser.py`:492-497(skyvern 池不可透传)
- `pyproject.toml:13-113`(依赖/extras,无 curl_cffi);`uv.lock`(rg 'curl' 零命中);`desktop/resources/requirements-lock.txt:1-26`(桌面锁来源=uv export 三 extras)
- `desktop/src-tauri/tauri.conf.json:45-63`(resources 逐文件清单,无 proxy-pools.yaml)
- `desktop/entry.py`:502-511(myssia_home)、:521-551(_bundle_config_dir)、:581-616(_serve_context)、:619-674(补种+迁移)、:1494-1527(doctor config_auto=<home>/pools.yaml)、:3641-3677(run.start)、:5595-5617(cron.create config_path)
- `src/myssia/cron/runner.py`:151-163(self_command,PYTHONPATH 注入)、:175-193(job_command 按 job.config_path 拼 --config)
- `src/myssia/config_layout.py`:36-80(plugins→config 一次性迁移)
- `desktop/src-tauri/src/main.rs`:398-448(spawn+MYIA_HOME 注入)、:599-643(data_root/平台后缀)
- `desktop/src-tauri/src/pyenv.rs`:296-364(依赖指纹漂移→DepsStale)
- `config/proxy-pools.yaml`:12-13(clash 单上游声明)
- `justfile:42-43`(build-desktop);`.github/workflows/desktop-release.yml:123-161`(tauri build 产物/改名)
- `desktop/ui-src/e2e/package_smoke.py:24-50`(brotli 内嵌+验源工具链)
- `src/myssia/proxy_panel.py:1-31`(proxy.probe/history 面板)

## 6. risks(探索员风险清单,原文)

1. proxy-pools.yaml 不在 tauri.conf.json resources——装机版不会随包/升级补种该件,新装机想用池须手放数据根或改 resources 清单重打包;且装机 doctor config_auto 只认 `<home>/pools.yaml`,与现行 config/proxy-pools.yaml 位置不一致,两条路径未收口。
2. cron 覆盖面不全:装机 jobs.json 16 个 job 仅「AI资讯」带 config_path,其余 None——若给这些品类源改 pool: 而不逐 job 补 config,fetch 前即报 proxy_pools_not_configured(零 I/O 结构化失败);run.start 同样无自动 --config。
3. curl_cffi 引入的真实影响面:facade 需完整 duck-type httpx(request/get/stream+Response 形状),RobotsCache/_send_with_retry/图片环逐跳复核(vision collect 层消费 follow_redirects=False 语义)都吃 httpx.Response;curl_cffi 的响应/重定向语义适配是隐藏工作量,未在本轮验证可行性。
4. httpx 池 facade 的上游 client(fetch_base.py:1152)与 curl_cffi 的代理/指纹是两套栈——若只在 direct 侧换 curl_cffi 而 pool 侧留 httpx,会出现「挂池的源 TLS 指纹仍是 python-httpx」的半吊子伪装,方案须两路同改或明确接受。
5. 代理伪装≠完全匿名:UA 缺省仍是 "MYIA/0.1 ..."(fetch_base.py:135)、robots 拉取无 UA(httpx 缺省)、DNS 在 socks5(非 socks5h)时仍本地解析、enrich(LLM 评分)/push(飞书/TG 等推送通道)出网完全不经池——被爬站看不到本地 IP 的目标可达,但整机的网络指纹面不止抓取栈。
6. urlwatch 引擎与 skyvern(llm_browser,其 API 只收服务端 proxy_location 枚举,llm_browser.py:492-497)两处明确不可挂池——这两类的目标站仍见相应出口 IP,是「被爬网站不再看到本地 IP」目标的已知例外面。
7. 池健康态生命周期=单 run 不跨 run(fetch_base.py D7):clash 单上游死后,摘除态下个 run 重置,表现为每 run 首次失败重试后才熔断;单上游池无轮换余地,clash 挂=该源当轮全败(proxy_pool_exhausted 快速失败)。
8. 装机版品类与仓库蓝本已漂移(数据根 config/ 有 searxng.yaml、weixin-sns.yaml、feishu-groups.yaml 等仓库外/未随包件,且有多个 .bak)——改仓库 config/ 推装机必须走数据根手改或重打包换装,补种机制不会覆盖装机已有件,存在双份真相漂移风险。
9. 验源/换装套路部分来自任务书口传背景(WKWebView 缓存清理步骤仓内未检到成文 runbook);brotli 内嵌导致打包件不可裸 grep 已由 package_smoke.py:24-28 与 Cargo.lock 佐证,但本轮未实际执行打包与换装验证。
10. 本轮未运行:myssia doctor 代理探测、任何网络连通性检查、uv export 重锁演练(纯只读取证,以上均为静态代码+文件系统+ps 实证)。

## 复核记录(规划员,2026-10-18)

对以下承重锚点做了定点复核,与探索员结论一致:
- `desktop/src-tauri/tauri.conf.json` resources 映射(实测 sed 40-70):config 清单 19 件(ai-news … wool),确无 proxy-pools.yaml。
- `config/proxy-pools.yaml:12` `clash: http://127.0.0.1:7897` 在场;`config/ai-news.yaml:299` reddit-ml `proxy: pool:clash` 在场(全仓唯一)。
- `desktop/entry.py` doctor config_auto 分支(实测 sed 1510-1522):`default_pools = ctx.home / "pools.yaml"`,存在才拼 --config——确与 config/proxy-pools.yaml 位置不一致。
- `desktop/entry.py:3641-3677` `_m_run_start`(实测):仅 `params.get("config")` 显式给才拼 `--config`,无自动发现。
- `src/myssia/cron/runner.py:151-193`(实测):`self_command` env=os.environ.copy()(MYIA_HOME 可透传到 job 子进程);`job_command` 仅 `job.config_path` 非空串才拼 `--config`。
- `src/myssia/engines/urlwatch.py:357-362`(实测):proxy≠direct 即 `proxy_unsupported` 结构化拒。
- `src/myssia/engines/fetch_base.py:2135-2145`(实测):fetch→resolve_proxy→_prepare_proxy_transport 分流点在位。
- `desktop/entry.py:619-674` `_seed_first_run`(实测):glob bundle `*.yaml/*.yml` 逐件补缺、target.exists() 即跳过(绝不覆盖);种子测试用夹具 bundle(tests/desktop/test_desktop_sidecar_protocol.py:1369-1451),不硬编码全量清单——resources 增件不炸种子测试。
- `tests/desktop/test_proxy_pool_panel.py:102,289-333`:config_auto 断言写死 `<home>/pools.yaml` 路径——改 config_auto 查找顺序时此组测试需同步(若保留旧路径回落则兼容)。
- `tests/cron/test_cron_runner.py:300-307`:job_command 组装测试在位,自动发现行为需在此扩测。
