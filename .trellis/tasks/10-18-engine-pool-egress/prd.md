# 引擎侧 IP 伪装:按源挂池与池配置装机送达链路

## Goal

被爬站不再看到本地 IP 的目标,在抓取栈(引擎侧)落地为**显式、不依赖本机 TUN 开关的池化出口**:按源盘点清单把被墙域源与 CF 风控强站源共 **7 处**挂 `pool:clash`(5 被墙域 + openai-news/hf-blog 观察位升挂,定稿见 Scope①),把池配置的装机送达链路收口(随包蓝本 + doctor/run/cron 自动发现),装机覆盖安装后可实测「经池源出口 IP ≠ 本地直连 ISP IP」。curl_cffi TLS 指纹对齐**终局不采纳**(重开判据备档,design §4)。海外可达无风控墙 API 源维持 direct 的残余风险**显式备档待主人裁决**(见「残余风险与主人裁决」节,不再沉默不动)。

## Background

全部事实依据见 `research/infra-delivery.md`(基建面:数据根/HTTP 栈/打包/池链路/风险)与 `research/source-inventory.md`(源盘点:45 源归置/Clash 实况/门禁),探索员 2026-10-18 只读取证 + 规划员定点复核。要点:

- 本机 Clash Verge 混合口 127.0.0.1:7897 常驻(launchd 服务),经池出口 198.2.214.3(US San Jose)≠ 本地 ISP IP 139.227.235.178(上海联通)——「藏 IP」命题实测成立。
- 当前 mihomo TUN 全局常开,**direct 源的海外可达性隐性依赖 TUN**;`pool:clash` 是把出口显式化、免 TUN 的通道(关 TUN/换机器后 direct 即裸连本地联通出口)。
- 仓库 45 源中仅 reddit-ml 已挂 `pool:clash`(ai-news.yaml:299);被墙域候选 telegram-durov / telegram-mihomo_party_group / deepmind-blog / google-research / qwen-blog 当前 direct 靠 TUN 兜底;openai-news / hf-blog 为 CF 风控强站(可达性不稳 + 403/质询面),原观察位**定稿升挂**(拷问 F2:403 不在 RETRYABLE_STATUS_CODES={429,500,502,503,504},fetch_base.py:145 实测,既不重试也不产生 transport 错,「遇 transport 失败即挂」判据永远等不到触发条件)。
- 装机送达三缺口:① proxy-pools.yaml 不在 tauri.conf.json resources(装机蓝本不带);② doctor config_auto 只认 `<home>/pools.yaml`(实际文件在 `<home>/config/proxy-pools.yaml`,两路不一致);③ run.start 仅显式 params.config 才拼 `--config`、cron job 仅 per-job config_path(装机 16 个 job 仅 1 个带)——挂池源在不带 --config 时 fetch 前结构化报 `proxy_pools_not_configured`。
- 装机数据根品类件与仓库蓝本已漂移,补种**绝不覆盖已存在文件**——装机侧生效必须走数据根手改(**7 处** proxy 值)+ 覆盖安装送代码。

## Scope 基线

**① 按源挂池(以盘点清单为准,含装机配置送达链路)** —— 本任务核心:
- 仓库蓝本 **7 处** `direct → pool:clash`:telegram-durov、telegram-mihomo_party_group(空态预挂,激活即走池)、deepmind-blog、google-research、qwen-blog(以上 5 处 = 被墙域,可达性判据);**openai-news、hf-blog(定稿升挂,拷问 F2)**——CF 风控强站,挂池判据从可达性转为防拉黑(IP 不被分辨,恰是主人需求面);原「观察位维持 direct + 行尾注释」方案取消。
- 观察位机制备档(本批无观察位,供未来 stay-direct 候选升挂用):判据 =「transport 失败**或 403/质询类应用层拒绝**实录即挂」(定稿修正版;原「仅 transport 失败」抓不住应用层拉黑信号——403 不进重试面也不产生 transport 错)。
- stay-direct 清单(research/source-inventory.md §5)一律不动;其中海外可达源的残余风险显式备档(见下「残余风险与主人裁决」节)。
- 装机送达链路:proxy-pools.yaml 进 tauri resources;doctor config_auto 优先 `<home>/config/proxy-pools.yaml` 回落旧 `<home>/pools.yaml`;run.start / cron job_command 在 home 模式无显式 config 时自动发现同一文件。

**② curl_cffi TLS 指纹对齐 = 候选,默认不采纳** —— 判据与理由见 design.md §4:
- 采纳判据(未来任务再裁决):(a) 有池化源在挂池后仍被 TLS 指纹墙(CF 类 403/质询)拦截且该源为目标必需;(b) 接受 facade 完整 duck-type httpx(request/get/stream/aclose + httpx.Response 形状适配,覆盖 RobotsCache/_send_with_retry/图片环 follow_redirects=False 语义);(c) direct 与 pool 两路同改或明确接受两栈分歧。
- 默认建议:不采纳。本任务目标是 IP 层出口显式化,非 TLS 反指纹;curl_cffi 引入有未验证的响应形状适配工作量 + 新依赖(装机 DepsStale 重装链)+ 两栈半吊子伪装风险(research/infra-delivery.md risks 3/4)。

**③ 装机生效 + 覆盖安装**:`just build-desktop` → 按在案判例换装(/Applications/世事.app,旧包备份)→ 数据根 **7 处** proxy 手改(.bak 先行)→ 装机实测验收。

**④ OpenBrowser 登录层 = 非目标(备档触发条件)**:复活 X/Twitter 监控(登录态墙)、啃 WAF/指纹强拦截源、AI 驾驶浏览器兜底层(llm_browser 之外的真人式浏览)任一立项时,再开独立任务裁决浏览器层出口与登录态;本任务不碰任何浏览器登录/指纹面。

**其余非目标**:enrich(LLM 评分)/push(推送通道)出网挂池(rg 实证零支持,属整机指纹面另案);urlwatch/skyvern/tg_web/agent_reach/wechat_local 引擎挂池(硬拒或字段无效);UA 缺省值与 robots 拉取无 UA 问题(网络指纹面另案);cron UI 新增 config 自动发现开关(行为静默收口,不加 UI);装机品类蓝本漂移治理(双份真相问题备档,不在本任务收);**海外可达无风控墙 API 源(games/stocks/credentials/myssia-demo/github releases)挂池——维持 direct 的显式残余风险,备档待主人裁决(见「残余风险与主人裁决」节,非沉默不动)**。

## 残余风险与主人裁决(拷问 F1/F2 收口,2026-10-18 定稿)

- **风险事实**:TUN 关闭的目标态下,stay-direct 清单中的海外可达源——games(epic-free/steam-specials/cheapshark/gog-free)、stocks(yahoo-chart)、credentials(aipocket)、myssia-demo(github-new-stars)、ai-token-deals 的 github releases.atom 直连源(freellmapi/gpt4free)——以本地联通 IP 直连出海,站方可见本地 IP。本批 7 处挂池解决的是被墙域可达性 + CF 强站防拉黑,**不覆盖这批源**。
- **维持 direct 的依据(工程裁量,待主人点头)**:research 实测这批均为无风控墙的公共 API、零登录态,「IP 被拉黑→拒服务」风险低;反向代价是把这批源的可用性绑死 Clash 在线(池挂=源快速失败);收益/代价不平,故不默认挂池。
- **升级路径(主人裁决触发即开第二批)**:若主人裁决「海外站一律不可见本地 IP,宁可丢可用性」,对这批源开同款挂池(同一 clash 池零边际成本,蓝本+数据根同套路);修正版观察判据(transport 失败或 403/质询类应用层拒绝实录即挂)同样适用于这批源的日常观察。
- 本节为显式备档:不再维持「沉默不动」;主人未裁决前,本任务按 stay-direct 执行。
- **裁决结果(2026-10-18,主人令「按照你的建议去做」=开第二批)**:「海外站一律不可见本地 IP」转为执行。名单 **14 处**(蓝本+装机数据根双侧同款):games 四源(epic/steam/cheapshark/gog)、stocks(yahoo-chart)、credentials(aipocket;占位 URL,指向自建部署时按需回 direct)、myssia-demo(github-new-stars)、ai-token-deals 两 github releases 源、ai-news 五厂商源(microsoft-research/mistral-news/anthropic-news-watch/meta-ai-blog-watch/cohere-blog-watch——原残余名单漏列的同类暴露面,依同一裁决补齐)。维持 direct 的同类裁定:aihot(DNS 实测 aihot.news→腾讯 EdgeOne CN 边缘节点,判国内)、credhunter-native(引擎 proxy 消费路径未核验,观察判据适用)、urlwatch 四源(硬拒)、agent_reach/tg_web/firecrawl 云渲染/零 HTTP/自建端点(字段无效或无暴露面,既定)。配套测试:tests/plugins/test_plugins.py `_single_source_config` 单源裁剪代理压回 direct(MockTransport 假客户端,验收面=extract+dedup,同 stocks symbols 收窄先例)。执行记录见 implement.md 第二批节。

## Requirements

- R1(按源挂池·仓库蓝本):config/telegram-channels.yaml(telegram-durov proxy 行 :38)、config/telegram-groups.yaml(telegram-mihomo_party_group :59)、config/ai-news.yaml(deepmind-blog :127 / google-research :138 / qwen-blog :182 / **openai-news :116 / hf-blog :160**,后两处定稿升挂)共 **7 处** `proxy: direct → proxy: pool:clash`(被墙域注释同款;openai/hf 两处注释记「CF 风控强站防拉黑升挂」)。stay-direct 清单零改动。
- R2(池配置随包):desktop/src-tauri/tauri.conf.json resources 增 `"../../config/proxy-pools.yaml": "config/proxy-pools.yaml"`,装机/升级补种到 `<home>/config/proxy-pools.yaml`(既有件不覆盖)。
- R3(装机送达收口·自动发现):三处一致「显式优先,home 模式缺省自动发现 `<home>/config/proxy-pools.yaml`,存在才拼 `--config`」——
  - doctor config_auto(desktop/entry.py:1515-1518):优先 `<home>/config/proxy-pools.yaml`,回落 `<home>/pools.yaml`(旧位兼容);
  - run.start(desktop/entry.py `_m_run_start`):params.config 缺省且 home 模式且池文件在场 → 自动拼;
  - cron job_command(src/myssia/cron/runner.py:175-193):job.config_path 缺省且 env MYIA_HOME 在场且 `$MYIA_HOME/config/proxy-pools.yaml` 存在 → 自动拼(self_command 已 copy os.environ,MYIA_HOME 可达 job 子进程)。
  - dev 模式(无 MYIA_HOME/ctx.home)行为零变化,CLI `myssia run` 显式 --config 契约零变化。
- R4(测试):自动发现新行为各路径有测试(显式优先/自动拼/缺文件不拼/dev 不拼);config_auto 新查找顺序同步 tests/desktop/test_proxy_pool_panel.py 既有断言;全量 pytest 绿。
- R5(装机生效):覆盖安装新包后,数据根 **7 处** proxy 手改(.bak 备份先行;顺序硬约束=先换装后手改,见 implement 8.4),装机 cron/run 池源免逐 job 配 config_path 即生效。
- R6(验收可测):装机后经池源实测出口 IP ≠ 本地直连 ISP IP;装机包含本任务逻辑(资源清单 + sidecar 代码);全量 pytest 绿。

## Acceptance Criteria(终版,2026-10-18 定稿)

- [x] A1 全量测试绿:`uv run --no-sync python -m pytest -q` 通过(CI 同款命令,ci.yml:29 口径)。
- [x] A2 挂池装载门不破:改 proxy 值后品类装载合法——`uv run --no-sync python -m pytest tests/cli/test_sources_write_surgery.py tests/plugins/ -q` 绿(roundtrip 与插件铁律不受影响;含在 A1,单列便于定位)。
- [x] A3 装机实测·出口 IP 分流:覆盖安装 + 数据根手改后,装机 app 设置面板代理池探测(proxy.probe config_auto)报告 exit_ip ≠ `curl -s http://members.3322.org/dyndns/getip` 直连所得本地 ISP IP(探索员基线:经池 198.2.214.3 vs 本地 139.227.235.178;节点可能漂移,判据=不等)。
- [x] A4 装机实测·池源取回(**必须走 R3 自动发现路径**):装机 app 对「TG频道监控」品类发起一次采集——该 job 实测 config_path=None(装机 jobs.json 16 job 中仅 AI资讯 带显式 config_path),恰走 job_command 自动拼 `--config` 路径;判据:telegram-durov 条目正常取回、direct 源不受牵连、日志无 proxy_pools_not_configured。R3 验收 = A4 + A5 的 argv 佐证叠加;**「等既有 AI资讯 cron fire」不构成 R3 验证**(拷问 F7 定稿删去该捷径——它只证明旧显式 --config 路径仍在工作,与自动发现无关)。
- [x] A5 装机包含本任务逻辑:安装件 Resources/config/ 含 proxy-pools.yaml(resources 生效);安装件 Python 文件与源码逐字节一致(package_smoke.py 套路,10-15-feed-local-images 判例形态);装机 run.start/cron 行为符合 R3(日志/argv 佐证自动拼 --config)。
- [x] A6 自动发现行为测试:tests/desktop(run.start + doctor config_auto 顺序)与 tests/cron(job_command)新增用例覆盖:显式 config 优先、home 模式自动拼、池文件缺失不拼、dev 模式零变化。
- [x] A7 换装跨度冒烟(拷问 F4 定稿新增):装机后日报下一期仍送达预期 bot(「AI信息分析师」,abe51b9c 面)且 AI 白嫖分区含三新源(b1684dfc 面);其余 0.0.3..HEAD 跨度面在任务档记录「已跨越、未逐面冒烟」。
  - **验收实录(2026-10-19 20:36 主会话亲验)**:20:05 PM 日报 run 8060 completed+push feishu_card ok=true;装机 daily-digest.yaml:155 `bot: analyst`(AI信息分析师,20:14 botswitch 落地)寻址实证=送达面过。三新源面三证推定:①装机分区清单含 edumails-nav/freellmapi-releases/gpt4free-releases(实读);②同配置今早 8:05 AM 日报 run 6474「AI 白嫖与优惠」分区实render 三源条目(freellmapi v0.16.1/2/3+gpt4free v8.7.7);③PM 期无分区=三源 job 排程 0 8 * * * 仅晨跑,PM 槽窗口空跳分区(设计行为,store_report_window_empty 哨兵注释在 daily-digest.yaml:136)。明早 8:05 AM 日报自然补最后一眼直接目验。

## Notes

- 行为披露(升级说明须带):home 模式 run/cron 缺省自动加载池文件后,原本因漏 --config 报 proxy_pools_not_configured 的池源将直接走池;无 Clash 的装机上,池源(被墙域/风控强站,7+1 处)快速失败(proxy_error/proxy_pool_exhausted,单上游池 3 连败熔断),direct 源不受影响——蓝本默认带 clash 池是单人自用机产品决策,如实披露。
- 池健康态生命周期=单 run 不跨 run:clash 挂=该 run 内该池源快速失败,下一 run 重置重试(v1.2 池化既有语义,本任务零改动)。

## 验收实录(2026-10-19)

A1-A6 全过(明细见 implement.md 收官实录):A3 出口分流 139.227.235.178 vs 198.2.214.3;A4 生产 run 6471 durov 20 条零失败;A5 包内字节级一致;A1 全量 6550 绿(含日期腐烂测试修复)。A7 留待今晚 20:05 新包首期日报(一次性检查已挂 20:21,结果自动回写)。
