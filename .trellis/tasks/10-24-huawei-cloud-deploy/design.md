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

1. 前置自检:python3≥3.11?uv 在位(无则官方脚本装)、git、systemd;
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
| keychain:myia/push/FEISHU_ANALYST_OPEN_ID | env:MYIA_PUSH_FEISHU_ANALYST_OPEN_ID |
| keychain:myia/llm/modelscope-*(残留引用若在) | 同法或删(已死线) |
| FEISHU2_*(push 通道解析面盘出后补表) | env:MYIA_FEISHU2_* |

- LLM 端点值(R5 默认):`MYIA_LLM_BASE_URL=http://<Mac 局域网 IP>:1234/v1`(主人 LM Studio 开 0.0.0.0 监听;Mac IP 变更=改 EnvironmentFile 一行);降级语义既有(enrich 失败→关键词粗筛,WARNING 可见)。
- 网络:cloud 上 ai-news 官方 RSS 源(OpenAI/DeepMind 等)在大陆的可达性 → 影子期实测定档;不可达源在服务器副本加 `pool:clash`(mihomo 兜底)——老线实测矩阵说 aihot/ZOL 直连秒开、OpenAI RSS 属海外源预期走池,不猜,影子期核。

## §4 数据搬种(默认方案)

1. 择 Mac 各品类 run 空窗(品类间隔分钟级即可,SQLite 无长事务);
2. 拷贝:`myssia.db` + `~/.myia/urlwatch/cache.db` → scp 上云 `/opt/myssia-data/` 对应位;
3. 云端首轮:9 采集品类各 `run` 一次手动触发——预期全部 dedup seen、零推送(AC4);若有新条目(Mac 停跑间隙产生)按正常语义推,属合理;
4. daily-digest 影子日对照:云端 `run daily-digest --dry-run` 出报告文本(不发)vs Mac 实发同槽,人比或 diff 入档;
5. urlwatch cache 搬种=watch-deals 基线平移(否则云端重建基线多一轮盲窗,已有判例)。

## §5 切割与回滚

- 切割序(同一槽窗内完成,避免双发):①Mac `myssia cron remove` 10 件(先 `cp jobs.json jobs.json.bak-切割日期`);②云端 `myssia cron create --category daily-digest --schedule "5 8,12 * * *"`;③云端下一槽真发验收(AC5)。
- 回滚(AC7):反向=云端 systemd stop + Mac `cp jobs.json.bak` 回 + cron list 核对;分钟级。
- Mac 侧品类配置文件保留(回滚即用;也作随时翻回 Mac 宿主的完整面)。

## §6 兼容性预判(实施时核,预期零改)

- 核心六依赖+firecrawl 客户端全跨平台;vision extras 有 darwin 标记不上云(不装 vision extras 即可,uv sync 面核对);
- secrets.py:Linux 无 keychain backend → keychain: 引用结构化报错引导 env:(设计内);env: 路径 Linux/macOS 同码;
- cron jobs.json 路径:MYIA_HOME 锚定(10-24-db-default 判例后 run/cron 同语义);
- 已知唯一真风险:未在 Linux 实跑过的边角(如 locale UTF-8、文件锁 flock 语义)——deploy.sh 前置自检含 `locale | grep UTF-8`。

## §7 兼容性总表

- 仓库代码:零改动预期;若 Linux 兼容修,量级最小+AC8 门禁兜底;
- CI:deploy/ 纯脚本+文档,零影响;
- Mac 侧:配置/钥匙串/装机件全不动;唯一动作=切割时 cron 移除(可逆);
- 老线:本任务不碰 ai-news-bot(退役是后续独立动作)。
