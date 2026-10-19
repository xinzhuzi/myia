# 源盘点结论(45 源 proxy 归置 + Clash 实况 + 门禁)

> **出处**:本件由规划员于 2026-10-18 落盘,内容 = 本轮工作流「探索员」源盘点只读取证结论原样收编(探索员只读不落盘,由规划员代写)。Clash 实况为探索员 2026-10-18 本机实测;门禁部分全部实读核验。
> **规划员定点复核**(2026-10-18):源名/行号抽样核对一致(见文末)。

## 1. clashLive(Clash 实况,2026-10-18 本机 macOS 实测)

① 7897 在听:`nc -z -w 3 127.0.0.1 7897` → "Connection to 127.0.0.1 port 7897 succeeded!";进程面:verge-mihomo 核以 root 常驻(/Library/Application Support/clash-verge-service/cores/verge-mihomo,-ext-ctl-unix 管理 sock)+ Clash Verge.app GUI(user)+ clash-verge-service 特权助手;常态启动方式=launchd 服务 /Library/LaunchDaemons/io.github.clash-verge-rev.clash-verge-rev.service.plist(RunAtLoad+KeepAlive 均在,开机自启、挂了自动拉起),与 config/proxy-pools.yaml:7 注释「常驻,macOS 服务模式 root 进程」一致(只读探测,未改任何配置)。

② 经池出口:`curl -x http://127.0.0.1:7897 https://api.ipify.org` → 198.2.214.3;`curl -x ... https://ipwho.is/` → United States / California / San Jose,ASN 54600 PEG TECH INC。

③ 直连对照:`curl https://api.ipify.org`(shell 无任何 http_proxy/https_proxy 等环境变量,`env | rg -i proxy` 为空)→ 同样 198.2.214.3 —— 两出口相同的根因:mihomo TUN 全局模式在开,路由表 `netstat -rn` 显示 198.18.0.1@utun1024 以 1、2/7、4/6、8/5、16/4、32/3、64/2 覆盖式路由接管全部公网 IPv4,裸 curl 的海外流量也被 TUN 送进同一 mihomo 规则出口。故朴素「直连≠经池」在本机当下不可复现,对照改为 CN 侧回显。

④ 本地真实 ISP IP:`curl http://members.3322.org/dyndns/getip` 与 `curl http://cip.cc` → 139.227.235.178,中国上海联通(cip.cc 三源一致);且经 7897 访问该 CN 站也出 139.227.235.178(mihomo 对 CN 域走 DIRECT 规则)。

**结论**:经池出口(198.2.214.3,US San Jose PEG TECH)≠ 本地 IP(139.227.235.178,上海联通),「藏 IP」命题成立;同时如实记:当前机器 TUN 常开,direct 源抓海外站实际也被同一 mihomo 送出国(与 pool 同出口),pool:clash 的现实增量=显式声明、不依赖 TUN 开关(关 TUN/换机器后 direct 即裸连本地联通出口)。

## 2. gates(改 direct→pool:clash 会触碰的门禁)

① 装载期:`schema.py:843` proxy 缺省 "direct";`:885-893` 词表 direct / pool:<名> / residential:<区域> —— 改值装载合法,不炸加载测试。

② 运行期硬门:BaseEngine.fetch() → _prepare_proxy_transport()(`fetch_base.py:2135-2183`);pools 未注入 → ProxyConfigError `proxy_pools_not_configured`(`fetch_base.py:2010、2171-2176`)。即 `myssia run/test/cron` 必须带 `--config config/proxy-pools.yaml`(ai-news.yaml:282-283 注释同);漏带则该源结构化报错、其余 direct 源不受影响。注意:该 mount 对所有 BaseEngine 子类生效,连 tg_web/agent_reach 这类不实际走 _active_client 的引擎也会因挂 pool 而背上声明依赖。

③ urlwatch 硬拒:`engines/urlwatch.py:357-362` 非 direct 即 `proxy_unsupported` —— zhipu/moonshot/minimax/seed 四源绝不可挂。

④ IronLaw/品类盲扫豁免现状:GLOBAL_DECLARATION_YAMLS=frozenset({"proxy-pools.yaml"})(`src/myssia/cli.py:3000`,单一真源),`_config_yaml_files` 按文件名过滤(`cli.py:3015-3019`);测试侧同步引用(rg -l 共 10 件):`tests/cli/test_sources_write_surgery.py:23、759-765`(官方品类往返参数化过滤)+ `tests/plugins/{test_maigret,test_media,test_osint,test_plugin_packages,test_theharvester,test_urlwatch,test_proxy_plugin,…}.py`(「插件坏不拦核心」铁律断言,glob config/*.yaml 逐份 load)。来历:bfdc8eeb(2026-10-18)收编 cli.py+3 测试,6540259a 补 test_maigret/media/osint/plugin_packages 四件(上笔 pathspec 漏列),59f37a65 再补 proxy/theharvester/urlwatch 三件——豁免针对的是 proxy-pools.yaml 这个**文件本身**进品类枚举,与品类件里 proxy 值改动无关,proxy 值改动不会重触发这批豁免。

⑤ golden 基件:`tests/fixtures/push_targets_golden/`(冻结副本,MANIFEST 9 件:ai-news/credentials/games/gpu-prices/monitor/news/stocks/wool + tests/fixtures/stocks.yaml)+ push_targets_golden_before.json。`tests/push/test_push_schema_targets.py::TestGoldenRegression`(:244-297)只对 **push 子树** 做逐字段断言(承诺边界 :255-258「只对 push 子树,其余节是合法演化面不拦」)——JSON 里虽有 32 处 "proxy" 快照值(全 direct),但不参与比对 → 改 live config 的 proxy 值**不炸** golden;冻结副本 ai-news.yaml 是旧快照(17 处 proxy: direct,无 pool:clash)同样无碍。重生成命令(仅当评审决定重立基线):`uv run --no-sync python tests/regen_push_targets_golden.py --refreeze`(从活库重冻结+重算 JSON;同源自检不带 --refreeze)。〔定稿勘误 2026-10-18,拷问 F10:原文引用 test_push_schema_targets.py 缺 tests/push/ 目录前缀,已补〕

⑥ 其他 proxy 断言(合成源/临时 pools 文件,不读活库,不受影响):`tests/engines/test_proxy_pool.py`(轮换/被动健康/摘除/熔断/proxy_pool_exhausted 家族/掩码)、`test_proxy_transport.py`、`test_registry.py:423-466`(pool:main 链短路)、`tests/cli/test_cli_full.py:590-638`(doctor proxy 连通性,自建临时池文件)、`tests/desktop/test_proxy_pool_panel.py`(设置面板);`tests/cli/test_sources_write_surgery.py::test_official_category_yaml_roundtrip` 对活品类 yaml 做停用/启用字节往返,不动 proxy 字段,不构成门禁。daily-digest.yaml 分区按**源名**匹配(:98-99),加新源须同步分区清单,但改 proxy 不涉及。

⑦ CI:`.github/workflows/ci.yml:29` 全量 `uv run --no-sync python -m pytest -q --tb=short`。

## 3. notes(引擎 proxy 消费面与出海实况)

① 引擎 proxy 消费面实测(rg 引擎源码):走 _active_client 挂池生效 = static_html / direct_api / crawl4ai(browser proxy 直读 _active_proxy_url,fetch_base.py:2151-2154)/ firecrawl(client 即 _active_client,但注意:挂池只改本机→firecrawl 云端连接的出口,目标站看到的是 firecrawl 云端 IP)/ prompt / telegram(bot 线 httpx,telegram.py:569 有 proxy transport 包装)/ feishu;**不消费**(字段无效)= agent_reach(源码零 proxy 引用,bili-cli/yt-dlp 子进程)、tg_web(chromium 系统网络)、wechat_local 系列(零 HTTP);urlwatch 硬拒。因此 bilibili-watch/youtube-watch yaml 里「遇阻挂 pool(基座已备)」的注释只对 BaseEngine 声明面成立,实际出口不受该字段控制——yt-dlp 抓 YouTube 当前靠系统级 TUN 兜底,若要显式控出口需系统级代理而非 proxy 字段。

② 出海直连可达性现状:本机 mihomo TUN 全局常开(198.18.0.1@utun1024),所有「direct」源的海外流量实际按 mihomo 规则走(CN 域 DIRECT 出上海联通,海外走代理节点)——即当前 direct 源的海外可达性隐性依赖 TUN 开着;pool:clash 是把这份依赖显式化、免 TUN 的通道。

③ 未核验项(如实):credhunter 引擎(exposure/credentials)的 proxy 消费路径未逐行核验(实现在场景件);ai-news aihot 的 firecrawl 云兜底层本机→云端实际出口未测;telegram-groups 当前 bot_token 指向 disabled 键=空态零请求,挂池属激活时配套。

④ 品类件清单口径:config/*.yaml 共 25 件,其中 wechat-stats.yaml.example 为 sidecar 形态样例(无 sources)、proxy-pools.yaml 为全局声明件(非品类),其余 23 件均有 sources;源总数 45(36 显式 direct + 1 pool:clash + 8 无 proxy 行走缺省 direct,缺省由 schema.py:843 提供)。

⑤ config/mcporter.json 非本任务面,未盘。

## 4. poolCandidates(挂池候选清单——本任务范围基线)

| 源 | 品类件:行 | 缘由 |
|---|---|---|
| reddit-ml | config/ai-news.yaml:299 | reddit.com 被墙域,**已挂** pool:clash(全仓唯一);static_html 引擎走 _active_client,池接线生效;run/cron 须带 --config config/proxy-pools.yaml |
| telegram-durov | config/telegram-channels.yaml:25(源名)/:38(proxy 行) | t.me 海外被墙域,当前 direct 能通全靠本机 Clash TUN 全局模式兜底;static_html 引擎消费 _active_client,挂 pool:clash 即显式稳定、不依赖 TUN 开关。挂池后 run/cron 必须带 --config 否则 proxy_pools_not_configured |
| telegram-mihomo_party_group | config/telegram-groups.yaml:42(源名)/:59(proxy 行) | api.telegram.org 被墙;yaml 注释(:59)自己预告「出海按需改 pool:<名称>」;TelegramEngine(BaseEngine,telegram.py:198)走 httpx/_active_client 且 :569 有 proxy transport 包装,池接线已备。当前源为待 token 空态(bot_token 指向 disabled 键),激活时配套挂池 |
| deepmind-blog / google-research / qwen-blog | config/ai-news.yaml:119,130,174(源名)/:127,:138,:182(proxy 行) | google 域(deepmind.google/research.google)与 github.io(qwenlm.github.io)在国内裸连均被墙,当前 direct 全靠本机 TUN 兜底才通;低频 RSS(每日 2 次)挂池零成本。属「候选」:若接受隐性依赖 TUN 可维持现状,追求显式通道则挂 pool:clash |
| openai-news / hf-blog | config/ai-news.yaml:108,152(源名)/:116,:160(proxy 行) | openai.com/huggingface.co 国内可达性不稳定(HF 时断时续);当前直连实测未记失败,列为**观察位候选**,遇 transport 失败再挂池(引擎 static_html 池接线已备) |

> **定稿注(2026-10-18,定稿员)**:openai-news / hf-blog 已由「观察位候选」**定稿升为直接挂池**——CF 风控强站,观察判据(transport 失败)抓不住 403/质询类应用层拉黑信号(403 不在 RETRYABLE_STATUS_CODES,既不重试也不产生 transport 错),而此二站恰是「IP 被分辨→拉黑」的真实风险面。定稿见 prd.md Scope① 与 design.md §2;本表为探索员原始结论存档,以 prd/design 定稿为准。

## 5. stayDirect(维持 direct 清单——本任务不动)

| 源 | 品类件:行 | 缘由 |
|---|---|---|
| zhipu-news-watch / moonshot-home-watch / minimax-home-watch / seed-home-watch | config/ai-news.yaml:315,331,349,363 | urlwatch 引擎硬拒非 direct(engines/urlwatch.py:357-362,proxy≠direct 即 proxy_unsupported 结构化报错;子进程直连抓取铁律) |
| weixin-文件传输助手 / weixin-localdb样例会话 / weixin-通知 / weixin-AI中转站-♾️ AI Token | config/weixin.yaml:61,80;config/weixin-notify.yaml:49;config/weixin-ai-token.yaml:22 | wechat_local 零 HTTP 本机读回(像素/本地桥),引擎源码零 proxy 引用,yaml 注释明示「零 HTTP;robots 面不适用」 |
| linuxsb / dalao / v2ex-free / v2ex-deals / v2ex-share / s74 / nodeloc / cocoloop / sbsb | config/wool.yaml:28,54,79,96,113,134,154,178,202 | 国内社区站直连实测通;v2ex×3 与 s74 走 firecrawl 云渲染——目标站看到的是 firecrawl 云端 IP 而非本机 IP,无藏 IP 需求,挂池只影响本机→firecrawl 端点连接反而多一跳 |
| zol | config/gpu-prices.yaml:12 | detail.zol.com.cn 国内站;firecrawl 云渲染同上 |
| gcores-rss / edumails-nav / ai-token-deals(prompt) / ai-vendor-watch(prompt,已退役) | config/news.yaml:28;config/ai-token-deals.yaml:59;config/ai-vendor-watch.yaml:41 | gcores.com / nav.edumails.cn / linux.sb 系均为国内站直连实测通;prompt 引擎目标站国内+LLM 端点为魔搭(国内),无出海面 |
| bili-ai_news | config/bilibili-watch.yaml:28 | B站国内站;且 agent_reach 引擎源码零 proxy 引用(bili-cli 子进程不消费该字段),挂池无实效只会引入 proxy_pools_not_configured 声明依赖(fetch_base.py:2135-2176 对所有 BaseEngine 子类生效) |
| telegram-clashv8 / telegram-handgame-src / telegram-baidu-pan | config/telegram-web.yaml:81,103,114 | tg_web 引擎走 chromium 系统网络(yaml :76 注释「chromium 走系统网络,mihomo 出口按需系统级配」),proxy 字段不被数据路径消费;当前 web.telegram.org 可达靠系统级 TUN,控出口应走系统配置而非 proxy 字段 |
| epic-free / steam-specials / cheapshark / gog-free / changedetection-watches / yahoo-chart / github-new-stars / aipocket | config/games.yaml:27,65,98,164;config/monitor.yaml:26;config/stocks.yaml:35;config/myssia-demo.yaml:14;config/credentials.yaml:49 | 海外公共 API 国内直连实测通路且无风控墙;monitor 指向自建 changedetection.io 实例属主人自定端点;无藏 IP 必要,遇阻再议 |
| searxng-watch | config/searxng.yaml:39 | 自托管 SearXNG 本机服务(127.0.0.1:8888),必须直连 |
| feishu-ai-relay-group | config/feishu-groups.yaml:22 | open.feishu.cn 国内(引擎 _active_client 虽消费 proxy,但目标国内无需求);源未写 proxy 行,走 schema 缺省 direct |
| daily-digest / exposure-scan / manual-triage / credhunter-native / freellmapi-releases / gpt4free-releases | config/daily-digest.yaml:35;config/exposure.yaml:30,47;config/credentials.yaml:35;config/ai-token-deals.yaml:76,87 | store_report 零抓取(锚 URL 仅铸去重键);credhunter 泳道自管限速/退避(重试=0);github releases.atom 直连实测通——均维持 direct(credhunter 引擎的 proxy 消费路径未逐行核验,如实标注) |
| yt-anthropic | config/youtube-watch.yaml:35 | youtube.com 被墙,但 agent_reach 引擎(yt-dlp 子进程)源码零 proxy 引用——挂 pool 字段无实效;实际出口由系统网络/TUN 决定,当前 TUN 常开故通。yaml :50 注释「遇阻挂 pool(基座已备)」仅指 BaseEngine 声明面,引擎数据面未接线(如实记) |

## 复核记录(规划员,2026-10-18)

- `config/telegram-channels.yaml`:telegram-durov 源名 :25、`proxy: direct` :38 —— 一致。
- `config/telegram-groups.yaml`:telegram-mihomo_party_group 源名 :42、`proxy: direct`(注释「出海按需改 pool:<名称>」):59 —— 一致。
- `config/ai-news.yaml`:openai-news :108/:116、deepmind-blog :119/:127、google-research :130/:138、hf-blog :152/:160、qwen-blog :174/:182、reddit-ml :285/:299(`pool:clash`)、zhipu/moonshot/minimax/seed 四 watch 源 :315/:331/:349/:363 —— 全部一致。
