# Design — 引擎侧 IP 伪装:按源挂池与池配置装机送达链路

## 1. Boundaries

**改动面(产品代码/配置,共 5 件 + 测试)**:
- `config/telegram-channels.yaml`(1 处 proxy 值 + 行内注释)
- `config/telegram-groups.yaml`(1 处 proxy 值)
- `config/ai-news.yaml`(**5 处** proxy 值:deepmind-blog / google-research / qwen-blog / openai-news / hf-blog,后两处定稿升挂)
- `desktop/src-tauri/tauri.conf.json`(resources 增 1 映射行)
- `desktop/entry.py`(doctor config_auto 查找顺序 + run.start 自动拼 --config)
- `src/myssia/cron/runner.py`(job_command 自动拼 --config)
- 测试:`tests/desktop/test_proxy_pool_panel.py`(config_auto 顺序)、`tests/desktop/`(run.start 自动发现新测)、`tests/cron/test_cron_runner.py`(job_command 自动发现新测)

**零改动面(红线)**:`src/myssia/engines/fetch_base.py`、`src/myssia/pipeline.py`、`src/myssia/engines/registry.py`、`src/myssia/schema.py`、`src/myssia/cli.py`(CLI 层显式 --config 契约不变)、pyproject/uv.lock/requirements-lock.txt(零新依赖)。stay-direct 清单品类件零改动。

## 2. 挂池决策与判据

**判据**(与源盘点对齐;定稿版——挂池判据从单一可达性扩为两类,拷问 F1/F2 收口):
- **挂池·被墙域(可达性)**:目标域裸连被墙(国内无 TUN 不可达),当前可达性隐性依赖本机 TUN 全局模式 → 挂 `pool:clash` 把出口显式化、免 TUN。成本:低频 RSS,单上游池,零轮换开销。
- **挂池·风控墙强站(防拉黑,定稿新增)**:目标域海外可达但 CF 风控强(403/质询面)→ 挂池藏 IP,恰是主人「被爬站分辨不出本地 IP」的需求面;「等出问题再挂」在此类站不成立——应用层拒绝不进任何自动信号(见观察位判据盲区)。
- **观察位(机制留档,本批无观察位)**:判据 =「transport 失败**或 403/质询类应用层拒绝**实录即挂」(定稿修正;原「仅 transport 失败」有盲区:403 不在 RETRYABLE_STATUS_CODES={429,500,502,503,504}(fetch_base.py:145 实测),既不重试也不产生 transport 错,自动信号永远等不到,只能靠日报/人工观察实录)。
- **stay-direct**:国内站 / firecrawl 云渲染(目标站见云端 IP)/ urlwatch 硬拒 / 引擎不消费 proxy 字段(agent_reach/tg_web/wechat_local)/ 零抓取源 / **海外可达无风控墙公共 API(残余风险显式备档待主人裁决,prd「残余风险与主人裁决」节)** —— 一律不动(research/source-inventory.md §5 全表)。

**本批落点(7 处 direct→pool:clash;后 2 处为定稿升挂)**:

| 源 | 品类件:proxy 行 | 引擎 | 说明 |
|---|---|---|---|
| telegram-durov | config/telegram-channels.yaml:38 | static_html | t.me 被墙;消费 _active_client,池接线生效 |
| telegram-mihomo_party_group | config/telegram-groups.yaml:59 | telegram(BaseEngine) | 空态预挂(bot_token 指向 disabled 键,零请求);激活即走池,免再改配置;telegram.py:569 有 proxy transport 包装 |
| deepmind-blog | config/ai-news.yaml:127 | static_html | deepmind.google 被墙 |
| google-research | config/ai-news.yaml:138 | static_html | research.google 被墙 |
| qwen-blog | config/ai-news.yaml:182 | static_html | qwenlm.github.io 被墙 |
| openai-news | config/ai-news.yaml:116 | static_html | openai.com 海外可达但 CF 风控强;原观察位**定稿升挂**(拷问 F2):观察判据抓不住 403/质询,此站恰是「IP 被分辨→拉黑」的真实风险面 |
| hf-blog | config/ai-news.yaml:160 | static_html | huggingface.co 同上;可达性时断时续,挂池同时收可达性收益 |

(定稿取消——openai-news/hf-blog 升挂池,本批无观察位。)观察位注释模板留档,供未来 stay-direct 候选升挂用:`# 观察位:遇 transport 失败或 403/质询类应用层拒绝实录即挂 pool:clash(池声明见 proxy-pools.yaml)`。

**已知代价(披露,非缺陷)**:无 Clash 的装机上这 7+1 源(7 新挂 + reddit-ml 既有)快速失败(proxy_error → 3 连败摘除 → proxy_pool_exhausted,零网络熔断),direct 源零牵连(registry proxy_* 短路只断同池链);单上游池 clash 挂=当轮该源全败,下一 run 重置(v1.2 池化语义)。蓝本默认带 clash 池是单人自用机产品决策。

## 3. 池配置装机送达设计(三层收口)

原则:**显式优先;home 模式才自动;文件在场才拼**。三个入口共用同一目标文件路径 `<home>/config/proxy-pools.yaml`(= resources 补种落点 = 本机现有手放件位置)。

### 3.1 蓝本随包(tauri.conf.json)

resources 映射增 `"../../config/proxy-pools.yaml": "config/proxy-pools.yaml"`。`_seed_first_run`(entry.py:619-650)glob bundle `*.yaml` 逐件补缺、绝不覆盖——新装机/升级自动出现该件,本机既有 652B 手放件逐字节保留。种子测试用夹具 bundle(test_desktop_sidecar_protocol.py:1369-1451),不硬编码全量清单,resources 增件不炸。

### 3.2 doctor config_auto 查找顺序(entry.py:1515-1518)

现状只认 `<home>/pools.yaml`(本机不存在 → config_auto 空转)。改为:
```
候选 = [<home>/config/proxy-pools.yaml, <home>/pools.yaml(旧位兼容)]
第一个存在者拼 --config;都不在 → 维持现状不拼
```
旧位回落保 `tests/desktop/test_proxy_pool_panel.py:289-333` 既有断言(写 `<home>/pools.yaml` 的用例)不炸;新增用例断言双在场时 config/ 优先。

### 3.3 run.start 自动发现(entry.py `_m_run_start`,:3641-3677)

```
if params.config:            # 显式优先(现状不变)
    argv_tail += ["--config", params.config]
elif ctx.home is not None and (ctx.home / CONFIG_DIR_NAME / "proxy-pools.yaml").exists():
    argv_tail += ["--config", str(ctx.home / CONFIG_DIR_NAME / "proxy-pools.yaml")]
```
ctx 取 `_serve_context()`(函数体现在已为 db 调过一次,收口为单次调用复用,避免重复解析)。dry-run 同样受益(argv 组装在 dry 分支之后统一走)。**路径一律走 `CONFIG_DIR_NAME`**(entry.py:353 已自 myssia.config_layout 导入,:605/:614 同款用法;拷问 F8 定稿),禁写 `"config"` 字面量——常量改名即静默漂移。

### 3.4 cron job_command 自动发现(runner.py:175-193)

```
config = job.get("config_path")
if isinstance(config, str) and config.strip():
    argv += ["--config", config.strip()]          # 显式优先(现状不变)
elif (home := os.environ.get("MYIA_HOME")) and (Path(home) / CONFIG_DIR_NAME / "proxy-pools.yaml").exists():
    argv += ["--config", str(Path(home) / CONFIG_DIR_NAME / "proxy-pools.yaml")]
```
- **常量同源(拷问 F8 定稿)**:runner.py 顶部 import 区新增 `from myssia.config_layout import CONFIG_DIR_NAME`(config_layout.py:25,同包可导,与 entry.py 同一真源)——两侧零 `"config"` 字面量;若未来常量改名,两处随 import 自动同步。
- MYIA_HOME 透传链已核验:Tauri 壳 spawn sidecar 注入(main.rs:415-418)→ sidecar 内 tick/ticker → runner `self_command` env=os.environ.copy()(runner.py:158)→ job 子进程继承。
- **dev 模式门**:独立 `myssia cron serve` / 仓库 dev 无 MYIA_HOME → 零变化,per-job config_path 契约不变。CLI `myssia run` 不经此函数,显式 --config 契约不变(python spec 红线:CLI 相对路径默认是仓库开发契约,永不在 CLI 层改动)。
- 装机收益:jobs.json 16 个 job 里 15 个无 config_path 的 job 自动获得池配置,免逐 job 手补;既有「AI资讯」显式 config_path 继续赢。

### 3.5 生效时序

装机侧品类 yaml 每次cron fire/run 都是新起 `myssia run` 子进程读盘(runner.py:175-193)——数据根 proxy 值手改后下一 fire 即生效,无需重启 app;桌面 sidecar 代码(entry.py/runner.py)更新需覆盖安装新包(换装前后确认 MYIA 进程为空)。

## 4. curl_cffi 终局裁决:不采纳(候选关闭,重开判据备档)

**终局(2026-10-18 定稿)**:**不采纳,本任务关闭该候选**。五条理由全部有代码实证(research/infra-delivery.md §2 依赖面 + risks 3/4;拷问亲证 rg 'curl' 全锁零命中、duck-type 面真工作量、两栈分歧、DepsStale 代价、scrapling 例外),且主人需求本就是 IP 层出口而非 TLS 反指纹。下列采纳判据任一命中才重开裁决。

**为什么现在不做**:
1. 目标错位:本任务验收是 IP 层出口分流(经池 exit_ip ≠ 本地 ISP IP),TLS 指纹(Python ssl 默认形态被 CF 类识别)不在验收面。
2. 隐藏工作量未验证:RobotsCache/_send_with_retry/图片环消费 httpx.Response 对象,curl_cffi 响应/重定向语义适配(follow_redirects=False 逐跳)是 duck-type facade(request/get/stream/aclose + **kwargs,fetch_base.py:969-1006 同款面)之外的真工作,research 未验证可行性。
3. 两栈分歧风险:httpx 池 facade 上游 client 与 curl_cffi 是两套栈——只改 direct 侧会出「挂池源 TLS 指纹仍 python-httpx」的半吊子伪装;两路同改=工作量翻倍且池 facade 也要换芯。
4. 依赖面代价:pyproject 增 extras → uv export 重出 requirements-lock.txt → 装机指纹漂移 DepsStale(pyenv.rs:353-364)→ 用户手跑 Python 环境安装链。
5. 现成例外已够:scrapling static 后端本就 curl_cffi(需另装 fetchers extras),浏览器引擎有自家指纹——真遇指纹墙的源可先换引擎而非换全栈。

**采纳判据(未来任务触发任一即重开裁决)**:
- (a) 有池化源挂池后仍被 TLS 指纹墙拦(CF 403/质询,且换引擎不可行)且该源为目标必需;
- (b) 接受完整 httpx duck-type 面适配并补 RobotsCache/图片环/retry 的行为等价测试;
- (c) direct+pool 两路同改,或书面明确接受两栈分歧及其披露。

## 5. Compatibility / 行为变化披露

- home 模式 run/cron 缺省自动加载池文件后:原本报 proxy_pools_not_configured 的漏配池源直接走池(修复性变化);无 Clash 装机上被墙域池源快速失败(见 §2 披露)。
- doctor config_auto 语义扩:双位回落,旧位用例兼容;面板快照仍记实际用的 config 路径。
- 蓝本 proxy 值变化对仓库 dev:`myssia run config/ai-news.yaml`(不带 --config)时 7 个新池源会报 proxy_pools_not_configured——与 reddit-ml 现状同款(ai-news.yaml:282-283 注释即此口径),dev 习惯是带 --config;不构成回归。
- golden/IronLaw/roundtrip 门禁:源盘点 §2 已逐条核验,proxy 值改动不触碰(golden 只比 push 子树;豁免针对 proxy-pools.yaml 文件本身进品类枚举,与值无关;roundtrip 不动 proxy 字段)。
- 版本面:不 bump 版本号(装机现 0.0.3,仓库 main 已 0.0.4,新包自然携带 0.0.4);零新依赖 → 无 DepsStale。

## 6. Rollback shape

- 代码/配置回滚:两个提交各自独立可 revert(见 implement.md 提交切分);yaml revert 即回 direct;送达链 revert 即回显式-only。
- 装机回滚(**原子联动,拷问 F6 定稿**):换回旧包 + **同批**还原数据根 7 处 .bak,缺一即留中间态——旧包无自动发现,只换包不还原数据根,则 TG频道/TG群等 job(config_path=None)每次 fire 报 proxy_pools_not_configured;两步须在同一 cron fire 间隔内完成(先还原数据根或同时,再换包均可)。
- 蓝本回滚注意:proxy-pools.yaml 已随包后,降级到旧包只是不再补种该件(既有件不删),无破坏;反向(revert 池化 YAML 回字符串形态才需动 load 语义——本任务不动池化形态,不适用,引 spec 旧注仅为备忘)。

## 7. 装机换装流程(判例对齐)

0. 换装跨度披露(拷问 F4 定稿):装机 0.0.3 → main(0.0.4+)是**全量跨越**,非本任务单一逻辑安装;v0.0.3..HEAD 含多笔运行时行为提交(至少 abe51b9c 日报出站切 bot、b1684dfc 日报分区三新源、9880aa0a 思考层魔搭、a99f6174 games 羊毛面)。装机后必做冒烟 = 日报送达预期 bot 且 AI 白嫖分区含三新源(A7);其余面在任务档记录「已跨越、未逐面冒烟」。
1. `just build-desktop`(justfile:42-43)→ 产物 desktop/src-tauri/target/release/bundle/macos/myssia.app。
2. 换装前后 `ps aux | rg -i "世事|MYIA|myssia_desktop_entry"` 确认进程为空(不静默杀在跑实例)。
3. 旧包 → /Applications/世事.backup-<ts>.app;新包入 /Applications/世事.app;本地 ad-hoc 签名 + `codesign --verify --deep --strict` 通过。
4. 验源:package_smoke.py 套路(安装件 Python 文件与源码逐字节一致;brotli 内嵌 dist 不可裸 grep,见 infra-delivery.md §3)。
5. 数据根手改 **7 处** proxy 值(.bak 先行;文件在 ~/Library/Application Support/MYIA/config/)。**硬约束(拷问 F5 定稿):步骤 3 换装完成且新 sidecar 在跑之前,禁止手改数据根 proxy 值**——反序则旧包无自动发现,池源下一 fire 即报 proxy_pools_not_configured。**并行设防(拷问 F3 定稿):手改前三件各记 sha256+mtime 快照,写完立即复核 diff 只含目标 proxy 行**,不一致先停手排查;数据根今晨(10-18 01:20-02:49)有并行会话编辑实录(ai-news/ai-token-deals/daily-digest),须与并行会话约定数据根独占操作窗口。
6. UI 未刷新才清 WKWebView 缓存(~/Library/WebKit/com.myssia.app、~/Library/Caches/MYIA/)——口传套路,仓内无成文 runbook,如实标注。
