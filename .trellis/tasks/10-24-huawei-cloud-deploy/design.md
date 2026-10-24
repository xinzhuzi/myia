# design.md — 10-24-huawei-cloud-deploy 技术设计

## §1 架构总览

```
华为云 Linux(老线同机,mihomo:7890 常驻)
├─ /opt/myssia          git clone(钉 commit)+ uv venv(uv sync --all-extras 同型)
├─ /opt/myssia-data     MYIA_HOME(config/ 品类种子 + myssia.db + cron/ + urlwatch/)
├─ /etc/myssia/env      EnvironmentFile(chmod 600,四组凭据值)
└─ systemd myssia-cron.service → uv run myssia cron serve --db /opt/myssia-data/myssia.db
    (at-most-once 既有铁律:tick 文件锁先推进再派发,单机单实例)

Mac(现状不动):世事 App=管理台+消息平台线宿主;切割后情报线 cron 移除,品类配置保留
```

- 数据根不用 `~/.myia` 缺省而显式 `/opt/myssia-data`:与部署目录分离,升级=git pull + uv sync 不碰数据;systemd 显式 MYIA_HOME 注入(与桌面 entry.py 的 env 注入同语义)。
- 无桌面 → 无 sidecar ticker;cron serve 单宿主(独立 serve 宿主是 cron 底座设计内形态,dispatch 上下文 `"cron"` 已有)。

## §2 deploy/huawei-cloud/ 三件契约

### deploy.sh(幂等,重跑安全)

1. 前置自检:python3≥3.11(uv 可代装:uv python install)、uv 在位(无则官方脚本装,**装 uv 本身走 mihomo 代理**)、git、systemd、`timedatectl`/date 记录(时区事实,信息性);
   **大陆网络路由(默认,grill 定)**:git/uv 全程走本机 mihomo——`git -c http.proxy=http://127.0.0.1:7890`、`export HTTPS_PROXY=http://127.0.0.1:7890`(uv 拉 PyPI 与 agent-reach 的 GitHub 直连依赖同路;老线容器 -e HTTP_PROXY=7890 同款判例);**降级备选**:Mac 侧 `git bundle`+`uv cache` 打包 scp(零外网依赖)+ 服务器 `uv sync --no-extra agent-reach`(情报线不用 agent-reach,毙掉 GitHub 直连依赖);
2. `git clone https://github.com/xinzhuzi/myia /opt/myssia`(已存在则 fetch+checkout 钉 commit);
3. `cd /opt/myssia && uv venv && uv sync --all-extras`(extras 全量,firecrawl/llm 客户端等);
4. 数据根种子:`/opt/myssia-data/config/` ← 仓 config/*.yaml 拷贝(已有不覆盖,同补种幂等语义)+ **keychain:→env: 引用改写**(sed 表驱动,清单=prd R3 四组+实施时盘出的 FEISHU2_*;改写仅服务器副本);
5. proxy-pools 服务器化:服务器副本 clash 上游 7897→7890(表驱动同上);
6. EnvironmentFile 存在性与 600 校验(值由主人/实施者手填,脚本不落密钥);
7. systemd unit 安装 + enable + start;`cron list` 冒烟。

### myssia-cron.service

- `[Service]`:WorkingDirectory=/opt/myssia;EnvironmentFile=/etc/myssia/env;Environment=MYIA_HOME=/opt/myssia-data;ExecStart=/opt/myssia/.venv/bin/myssia cron serve --db /opt/myssia-data/myssia.db;Restart=always/5s;User=部署用户(非 root,老线容器外运行同权级)。
- `[Install]` multi-user.target;日志走 journald(`journalctl -u myssia-cron` 即排障面)。

### README.md(部署手册)

- 章节:前置(含 mihomo 在位确认)→ 首次部署 → 凭据填写表(变量名/钥匙串来源/Mac 导出命令 `security find-generic-password -s myia -a <名> -w`)→ 数据搬种(见 §4)→ 影子期 → 切割 → 升级(git pull+sync+restart,数据不动)→ 回滚(双向)→ 排障(journald/cron list/「源批量 empty 先 curl 直连 vs 代理各测一次」/enrich 降级判读)。

## §3 凭据与网络

- 引用改写表(部署脚本内置,Mac 仓零改动):

| 服务器配置里 | 替换为 |
|---|---|
| keychain:myia/firecrawl/url | env:MYIA_FIRECRAWL_URL |
| keychain:myia/firecrawl/api-key | env:MYIA_FIRECRAWL_KEY |
| keychain:myia/llm/local-base-url | env:MYIA_LLM_BASE_URL |
| keychain:myia/llm/local-api-key | env:MYIA_LLM_KEY |
| keychain:myia/push/FEISHU_ANALYST_OPEN_ID | env:FEISHU_ANALYST_OPEN_ID(叶名=env 名契约) |
| keychain:myia/llm/modelscope-*(ai-token-deals 残留) | 部署前已切本地(R2b),服务器侧零出现 |
| (bot 预设,无 keychain 引用——BOT_APP_CREDENTIAL_KEYS 字面 env 名,feishu_card.py:309) | EnvironmentFile 直填 FEISHU2_APP_ID= / FEISHU2_APP_SECRET= |

- LLM 端点值(R5 默认):`MYIA_LLM_BASE_URL=http://<Mac 局域网 IP>:1234/v1`(主人 LM Studio 开 0.0.0.0 监听;Mac IP 变更=改 EnvironmentFile 一行);降级语义既有(enrich 失败→关键词粗筛,WARNING 可见)。
- 网络:cloud 上 ai-news 官方 RSS 源(OpenAI/DeepMind 等)在大陆的可达性 → 影子期实测定档;不可达源在服务器副本加 `pool:clash`(mihomo 兜底)——老线实测矩阵说 aihot/ZOL 直连秒开、OpenAI RSS 属海外源预期走池,不猜,影子期核。

## §4 数据搬种(默认方案)

1. 择 Mac 各品类 run 空窗(品类间隔分钟级即可,SQLite 无长事务);
2. 拷贝:`myssia.db` + `~/.myia/urlwatch/cache.db` → scp 上云 `/opt/myssia-data/` 对应位;
3. 云端首轮:9 采集品类各 `run` 一次手动触发——预期全部 dedup seen、零推送(AC4);若有新条目(Mac 停跑间隙产生)按正常语义推,属合理;
4. daily-digest 影子日对照(**grill 修正:dry-run 不渲染模板**——pipeline _push_channel dry_run 分支在 render 前返回;改用 **stdout 通道变体**:服务器侧 daily-digest 副本 push 换 channel stdout→真跑出全文文本,vs Mac 实发同槽 diff 入档;push-quality 冒烟已验证此法);
5. urlwatch cache 搬种=watch-deals 基线平移(否则云端重建基线多一轮盲窗,已有判例)。

## §5 切割与回滚

- 切割序(同一槽窗内完成,避免双发):①Mac `myssia cron remove` 10 件(先 `cp jobs.json jobs.json.bak-切割日期`);②云端 `myssia cron create --category daily-digest --schedule "5 8,12 * * *"`;③云端下一槽真发验收(AC5)。
- 回滚(AC7):反向=云端 systemd stop + Mac `cp jobs.json.bak` 回 + cron list 核对;分钟级。
- Mac 侧品类配置文件保留(回滚即用;也作随时翻回 Mac 宿主的完整面)。

## §6 兼容性预判(实施时核,预期零改)

- 核心六依赖+firecrawl 客户端全跨平台;vision extras 有 darwin 标记不上云(不装 vision extras 即可,uv sync 面核对);
- secrets.py:Linux 无 keychain backend → keychain: 引用结构化报错引导 env:(设计内);env: 路径 Linux/macOS 同码;
- cron jobs.json 路径:MYIA_HOME 锚定(10-24-db-default 判例后 run/cron 同语义);
- **时区链(grill 定)**:cron 时区解析序 = --timezone > 品类 YAML timezone > 服务器本地;云端挂 job 全部经 `myssia cron create --category <品类路径>` 走品类 YAML(情报线品类均带 timezone: Asia/Shanghai)→ 零依赖服务器系统时区;deploy.sh 仍记录 `timedatectl` 事实入档;
- **extras 面(grill 定)**:agent-reach 是 GitHub 直连依赖(URL 钉 tag)且情报线不用——默认代理下全量 sync 无碍;降级备选 `--no-extra agent-reach`;vision 有 darwin 标记,Linux 装不上属 uv 正常跳过;
- 已知真风险:未在 Linux 实跑过的边角(locale UTF-8、文件锁 flock 语义)——前置自检含 `locale | grep UTF-8`;
- **搬种一致性(grill 定)**:Mac 生产库禁 cp 直拷(weixin 品类每 5 分钟在写,并发写期文件拷贝=损坏风险)——一律 `sqlite3 <db> ".backup <目标>"` 在线备份 API(myssia.db 与 urlwatch cache.db 同法),拷备份件上云。



## §8 转换映射总表(华为云现有 → 世事承载,AC10 逐行核对口径)

| # | 华为云现役件 | 世事承载件 | 转换动作 | 状态 |
|---|---|---|---|---|
| 1 | wf_crawl.py 十源论坛采集(linuxsb/btsb/nodeloc/cocoloop/dalao/sb.sb/74站/V2EX×3) | config/wool.yaml(同源面;bt.sb WAF 判死如实弃用,双域复测在案) | 无需动作(收编已毕);服务器大陆直连面更优(被墙源走 firecrawl 云) | 已承载 |
| 2 | wf_crawl 词表四层否决/双信号/硬门槛(10-20 版) | myssia-classifier 0.0.7 词表 v2+裁决序 | 无需动作(金测 78 条钉住) | 已承载 |
| 3 | watch_deals.py(TapNow/RunningHub/海螺 快照diff+量化门槛) | config/watch-deals.yaml(urlwatch 引擎+DEAL_SPECIFIC_KW) | 无需动作;TapNow 降级态双方一致 | 已承载 |
| 4 | ai_daily_report.py 四区块合一卡(AI日报/厂商/羊毛+尾戳) | daily-digest(store_report;版式 10-24 已对齐「AI信息 {date}-{AM/PM}」) | 无需动作 | 已承载 |
| 5 | companies.json(20司)/influencers.json(22V) 标签库 | ai-news custom rules 42 条固化 YAML | 无需动作 | 已承载 |
| 6 | 腾讯股价+GPU 美价国行比价+B站显卡视频 | ai-vendor-daily(vendor_market 引擎) | 无需动作 | 已承载 |
| 7 | aihot 三路(/daily/首页/hot)+X 直链 | ai-news aihot-daily/aihot-hot 源 | 无需动作 | 已承载 |
| 8 | fc_cloud.json(云 FC 兜底凭据) | MYIA firecrawl 云钥 | **凭据转换**:钥匙串值→env:MYIA_FIRECRAWL_URL/KEY(§3 表) | 转换 |
| 9 | llm.json(glm-4-flash 免费已死) | enrich(默认 Mac LM Studio 局域网;翻案=云钥) | **凭据转换**+端点裁决 R5 | 转换 |
| 9b | (连带修复)ai-token-deals prompt 引擎同踩魔搭死线(Mac 现役空转) | 同切本地 LM Studio | R2b 前置修复 | 转换 |
| 10 | push_target.json(AI福利群 chat_id+主人 open_id 双投) | push target(FEISHU_ANALYST_OPEN_ID env) | **凭据转换**;群投递=开放裁决⑤默认不加 | 转换 |
| 11 | mihomo 容器(7890,06:00 刷节点) | **原样保留**——世事 clash 池上游指它 | 零动作(保留声明) | 保留 |
| 12 | 老线状态文件(wooly_sent/daily_sent_items/deals_snapshot/wooly_state) | 不迁移(世事自洽 dedup;搬种用 Mac 库) | 三重归档已在案,零动作 | 如实弃用 |
| 13 | crontab 三条(8:00 采集/8:30 日报/12:00 午轮) | 世事 cron jobs(9 采集+digest) | **S1 注释暂停→S3 世事接管**(§9) | 转换 |
| 14 | 服务器 24/7 常驻 | systemd myssia-cron.service | 本任务交付 | 交付 |

## §9 替换状态机与暂停操作契约(R6 展开)

### 状态机(prd R6 表的实现面)

- 每阶段转换都有**单向门+回退门**:S0→S1(暂停老线)/S1→S0(crontab 恢复);S2→S3(切割)/S3→S2 前态(Mac 恢复 bak+云 digest 移除);回退操作全部分钟级(AC7 演练)。
- 发报方唯一性不变式:任一时点**至多一个发报方**——S0 违反(现状双发,任务首个动作即消除),S1-S4 恒成立。

### S1 时机(grill Q1 待主人裁)

现挂 Step 4 首日;备选提前至 **Step 0(开工首动作)**——消双发更早、主人当周只收一条,代价=部署期内若 Mac 故障则零发报(crontab 恢复分钟级兜底);默认推荐提前。

### S1 老线暂停操作契约(SSH 实操,写进 README)

```bash
# ① 备份(在案即 AC9 证据)
crontab -l > ~/crontab.bak-<日期>
# ② 注释恰好三条(ai-news 链:wf_crawl/watch_deals/ai_daily_report 或 run_daily 封装),
#    sed 匹配串以服务器 crontab -l 实况为准(预演:grep -n 确认命中行数=3±1)
# ③ 核验:crontab -l | grep -v '^#' 不再含 ai-news;next 槽后主收件箱仅一条 Mac 日报
# ④ 保留声明:mihomo/new-api/宝塔零触碰(docker ps 前后快照对照入档)
```

- 注释而非删除:可逆性优先;S4 退役确认后才建议清理(资源回收=主人裁决)。
- ai-news:local 镜像与 /opt/ai-news 目录:S1-S4 全程不动(暂停即止,容器本就 run --rm 无常驻)。

## §7 兼容性总表

- 仓库代码:零改动预期;若 Linux 兼容修,量级最小+AC8 门禁兜底;
- CI:deploy/ 纯脚本+文档,零影响;
- Mac 侧:配置/钥匙串/装机件全不动;唯一动作=切割时 cron 移除(可逆);
- 老线:本任务不碰 ai-news-bot(退役是后续独立动作)。
