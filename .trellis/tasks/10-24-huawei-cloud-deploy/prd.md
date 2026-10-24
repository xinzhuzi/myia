# PRD — 华为云无头部署:MYIA 功能核上云替代老线

## Goal

把 MYIA 的 Python 功能核(myssia:采集/分类/评分/推送/cron)以**无头形态**部署到华为云 Linux 服务器,情报线品类 24/7 跑在大陆机房;Mac 上的世事 App 保持现状作管理台与消息平台线(Mac 绑定品类)宿主。部署验收后,华为云老线(ai-news-bot 三件套)正式退役。

## 背景与定位

- 主人 10-24 裁定方向:桌面 App 壳(macOS Tauri)不上云,**功能核上云**——功能挪移本身已由 10-24-huawei-ai-news-absorb 完成(词表/定向优惠/厂商日报/AI信息版式全收编),本任务是**运行位置迁移**。
- 上云增益:①大陆机房直连面(sb.sb/nodeloc/cocoloop/dalao/ZOL/aihot 秒开,被墙源走云 FC 兜底——老线可达性矩阵);②24/7 不睡机(Mac 合盖即断采);③老线退役后服务器资源复用。
- 范围铁律:**只迁情报线**;Mac 绑定品类(weixin=本地微信库、tg_web=本地无头浏览器、telegram 系、feishu-groups)留 Mac,不迁。
- **替换语义(主人令 10-24 二次明确)**:华为云老线(ai-news-bot)的已有功能在本任务内**暂停并替换**——不是并行共存,终态=云端世事功能核唯一发报,老线退役;现状实况=老线(8:30)与 Mac 世事(8:05)**双发同款日报**,暂停时序在 R6 写死。

## Requirements

### R1 部署件(仓库内交付)

- `deploy/huawei-cloud/` 三件:`deploy.sh`(幂等部署:git 拉取钉 commit→uv 环境→数据根种子→凭据 EnvironmentFile 装载校验→systemd 装载)、`myssia-cron.service`(systemd 单元:MYIA_HOME/EnvironmentFile,Restart=always,跑 `myssia cron serve`)、`README.md`(部署手册:前置/部署/升级/回滚/排障,含「源批量 empty 先 curl 直连 vs 代理各测一次」口诀与老线可达性矩阵)。
- 代码装法 = git clone 钉 commit(本仓 main 已推 HEAD;PyPI 0.0.1 落后两个月不用),uv 管理环境;**预期零产品代码改动**——若实施中发现 Linux 兼容缺口,按需最小修并走正常提交(AC8 兜底)。

### R2 品类面(上云集合 = 情报线 11 件)

ai-news / wool / watch-deals / ai-vendor-daily / ai-token-deals / games / stocks / news / gpu-prices / daily-digest,共 10 件(9 采集 + 1 日报;调度对齐既有节奏);config 随仓种子;proxy-pools 的 clash 池上游在**服务器侧**改指本机 mihomo `127.0.0.1:7890`(老线判例:06:00 自动刷节点)——Mac 侧 7897 配置不动。

### R2b 部署前置修复(grill 拷问抓出,Mac 侧先行)

- **ai-token-deals 的 prompt 引擎端点踩死线**:engine_options.prompt.base_url 仍指魔搭(整线 10-24 已亡)——Mac 现役每天 08:00 空转失败;修法=切本地 LM Studio(ai-vendor-watch 同款判例:local-base_url/local-api-key+disable_thinking+超时预算),随 Step 1 落地并全量门禁。

### R3 凭据面(keychain→env 适配)

Linux 无 keychain(secrets.py 已有 `keychain_backend_unavailable` 结构化引导;`env:` 引用是文档明载的 Linux 正道)。四组凭据从 Mac 钥匙串导出值,写入服务器 EnvironmentFile(chmod 600):

| 钥匙串引用(Mac) | env 变量(服务器) | 用途 |
|---|---|---|
| myia/firecrawl/url + api-key | MYIA_FIRECRAWL_URL / MYIA_FIRECRAWL_KEY | wool 被墙源、ai-vendor ZOL 云渲染 |
| myia/llm/local-base-url + local-api-key | MYIA_LLM_BASE_URL / MYIA_LLM_KEY | ai-news 评分+中文译名(端点裁决 R5) |
| myia/push/FEISHU_ANALYST_OPEN_ID | MYIA_PUSH_FEISHU_ANALYST_OPEN_ID | 日报投递目标 |
| 飞书 analyst bot(已盘出:BOT_APP_CREDENTIAL_KEYS["analyst"]=(FEISHU2_APP_ID, FEISHU2_APP_SECRET),feishu_card.py:309;字面 env 名) | FEISHU2_APP_ID / FEISHU2_APP_SECRET(**字面名**) | 出站 bot |
| (target 引用形态)keychain:myia/push/FEISHU_ANALYST_OPEN_ID → env:**FEISHU_ANALYST_OPEN_ID**(钥匙串规范名叶名=环境变量名,resolve_channel_credential 契约 base.py:278) | 同左 | 投递目标 |

- 服务器侧品类配置的 keychain: 引用替换为 env: 形态——**仓库 config 保持 keychain: 不动**(Mac 继续用),部署脚本在服务器副本上做引用改写;零歧义验收 = 服务器任一品类 `--dry-run` 装载过、无 invalid_credential_ref。

### R4 数据面与双跑切割

- **搬种式引导(默认,可翻案)**:Mac 生产 `myssia.db` + `~/.myia/urlwatch/cache.db` 停写拷贝上云——去重注册表/已推指纹/评分缓存/urlwatch 基线全量继承,云端**零重推零重评**;备选:全新库+首轮存量波(模板 20 帽有界,一次性)。
- **影子期**:云端 9 采集品类 cron 全开、**daily-digest 不挂**跑 ≥1 天,对照 Mac 同槽产出(条数/分区/译名抽查);期内 Mac 照常发报。
- **切割**:影子达标后 Mac 侧 10 件情报线 cron 移除(jobs.json 备份),云端挂 digest——**同槽只有一方发报**;Mac 消息平台线 cron 不动。
- 回滚:Mac 侧 cron 恢复备份 + 云端 systemd stop,分钟级。

### R5 LLM 端点(开放裁决,默认先行)

- **默认**:enrich 端点指 **Mac LM Studio 局域网地址**(需主人在 LM Studio 侧把监听改 0.0.0.0,一次性)——Mac 睡眠/关机时云端走既有 enrich 降级路径(关键词粗筛+零译名,不阻管线),醒后自愈。
- 翻案项:云端 funded 钥(智谱充值/fuhuagoogle 中转)一键切回云轨(端点三件套纯配置,判例在案)。

### R6 老线暂停与替换时序(主人令:已有功能暂停,替换为世事)

分阶段状态机(每阶段发报方唯一性是硬约束,细节契约见 design §9):

| 阶段 | 老线(华为云) | Mac 世事 | 云端世事(新部署) | 进入条件 |
|---|---|---|---|---|
| S0 现状 | **发**(8:30) | 发(8:05) | — | (双发,即刻要出) |
| S1 老线暂停 | **停**(crontab 三条注释,备份在案) | 发 | 未部署 | **Step 0=开工首动作(主人 10-24 裁「按推荐」:Mac 已稳定,消双发宜早,crontab 恢复分钟级兜底)**;进入即消双发 |
| S2 影子 | 停 | 发(基准方) | 暗跑(采集全开+digest 不挂) | S1+部署+搬种完 |
| S3 切割 | 停 | **停**(情报线 cron 移除) | **发**(唯一发报方) | 影子达标 |
| S4 终态 | 退役确认(数据三重归档核验) | 管理台+消息线 | 唯一情报线 | AC5 真发验收 |

- S1 暂停操作契约:**仅动 ai-news 相关 crontab 三条**(wf_crawl/watch_deals/ai_daily_report 链);**mihomo 容器必须保留**(云端新部署的 clash 池上游);new-api 等无关服务零触碰;暂停可逆(crontab 备份恢复即回 S0)。
- 老线状态文件(wooly_sent/daily_sent_items/deals_snapshot 等)不迁移——MYIA 有自洽去重体系,搬种用 Mac 库;老线数据件已有三重归档(cloud-snapshot-20261017+增量+迁移包)。
- S4 资源回收(ai-news:local 镜像删除/目录清理)=主人裁决项,出建议清单不动手。

### 非目标

- 不做 Linux 桌面构建(Tauri AppImage)——服务器无桌面,GUI 留 Mac;
- 不迁 weixin/telegram 系/feishu-groups(Mac 绑定);
- 不做多机集群/容灾(单机单实例,at-most-once 既有铁律);
- 资源回收(删镜像/清目录)不在本任务动手——S4 出建议清单留主人;
- 不动服务器上与老线无关的服务(new-api/宝塔等)。

## Acceptance Criteria

- [ ] AC1 部署件:`deploy/huawei-cloud/` 三件入库;README 从零跟着走可在干净 Linux 复刻(以华为云实测为准)。
- [ ] AC2 常驻:服务器 systemd 起 `myssia cron serve` 常驻(enabled + active);10 品类全部装载(cron list 在册 + 任一品类 --dry-run exit 0)。
- [ ] AC3 凭据:EnvironmentFile chmod 600;firecrawl/飞书/LLM 三类引用服务器侧全 env: 且可解析(dry-run 零 invalid_credential_ref)。
- [ ] AC4 搬种:拷库后云端首轮各采集品类 run **零推送**(dedup seen 全留痕);影子日同槽对照记录(云端 digest dry-run vs Mac 实发)入档。
- [ ] AC5 切割:Mac 10 件 cron 移除且备份在档;云端 digest 挂上真发一条「AI信息 · 日期-AM/PM」到分析师私聊(回执/截图)。
- [ ] AC6 网络:clash 池上游=服务器 mihomo 7890 实测通(stocks Yahoo 腿经池 200);wool 被墙源经 firecrawl 云端可达(各源计数>0)。
- [ ] AC7 回滚演练:按手册反向操作,分钟级 Mac 恢复发报(演练记录在档)。
- [ ] AC8 门禁:若触产品代码(Linux 兼容修),全量 pytest+ruff 绿;纯部署件则 CI 零影响。
- [ ] AC9 老线暂停与零双发:S1 执行后连续一个发报槽**只收到一条**日报(Mac 版);crontab 备份文件在档;S3 后连续两槽只收云端版;全程任一时点无双发。
- [ ] AC10 转换映射核对:design §8 映射表逐行核「已承载/凭据已转换/如实弃用」三态,留痕入档。

## 开放裁决点(默认已定,可翻案)

1. 引导方式:搬种拷库(默认)/全新库存量波;
2. LLM 端点:Mac LM Studio 局域网(默认,需主人开 0.0.0.0 监听)/云端 funded 钥;
3. 影子期时长:1 天(默认);
4. Mac 侧是否保留周备援(默认否——at-most-once 语义下双跑有双发风险,靠回滚预案兜);
5. 老线推双目标(AI福利群+私聊)→ 世事现仅推分析师私聊;**群推送加挂**=品类 YAML 加一条 push targets 即可(机制现成),默认不加待主人点单。
