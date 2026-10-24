# 华为云无头部署手册 — MYIA 功能核(myssia)

> 任务档:`.trellis/tasks/10-24-huawei-cloud-deploy/`(prd/design/implement)。
> 本手册 = design §2 README 契约:前置 → 首次部署 → 凭据 → 数据搬种 → 影子期 → 切割 → 升级 → 回滚 → 排障。
> 铁律:**git/uv 在服务器上全程走本机 mihomo 代理**(大陆直连 GitHub/PyPI 会卡死);
> Mac 侧配置/钥匙串/装机件全不动(切割时仅移除 Mac 情报线 cron,可逆)。

## 目录

1. [前置](#1-前置)
2. [首次部署](#2-首次部署)
3. [凭据填写表(Mac 钥匙串逐把导出)](#3-凭据填写表mac-钥匙串逐把导出)
4. [数据搬种](#4-数据搬种)
5. [影子期](#5-影子期)
6. [切割](#6-切割)
7. [升级](#7-升级)
8. [回滚(双向)](#8-回滚双向)
9. [排障](#9-排障)
- [附录 A:S1 老线暂停操作契约](#附录-as1-老线暂停操作契约)

---

## 1. 前置

| 项 | 要求 | 核验命令 |
|---|---|---|
| OS | Linux x86_64,systemd | `systemd-analyze verify >/dev/null 2>&1; ls /run/systemd/system` |
| 部署用户 | 非 root(如 `deploy`) | `id deploy`(无则 `useradd -m -s /bin/bash deploy`) |
| mihomo 代理 | 常驻 `127.0.0.1:7890`(**老线容器,零触碰保留**) | `curl -x http://127.0.0.1:7890 -sI https://www.google.com \| head -1` 应回 `HTTP/… 200/302` |
| git / 磁盘 | git 在位;`/opt` 余量 ≥3GB(全量 extras ~2GB) | `git --version; df -h /opt` |
| locale | UTF-8(LANG=C 会乱中文) | `locale \| grep UTF-8` |
| python3 | ≥3.11(**不足也无妨**:deploy.sh 用 uv 代装) | `python3 -V` |
| uv | 可缺位(deploy.sh 官方脚本装,走代理) | `uv --version` |
| Mac LM Studio | 影子期**前**:监听改 `0.0.0.0`(R5 默认端点=Mac 局域网) | Mac 上 `curl http://127.0.0.1:1234/v1/models` 有模型即活;云端等价核验 `curl http://<Mac-IP>:1234/v1/models` |

- 时区无硬要求(品类 YAML 全带 `timezone: Asia/Shanghai`,零依赖系统时区);deploy.sh 仍记录 `timedatectl` 事实入档。
- 老线可达性矩阵(design §3;影子期实测定档):**大陆直连面** sb.sb/nodeloc/cocoloop/dalao/ZOL/aihot 秒开;**被墙源** reddit/OpenAI RSS 等走 `pool:clash`(mihomo 兜底);**WAF 判死** bbs.bt.sb 直连不可达 → wool 件已按 firecrawl 云路径兜底。

## 2. 首次部署

```bash
# ① 传三件(在 Mac,scp 走 ssh key BatchMode)
scp -o BatchMode=yes -r deploy/huawei-cloud <user>@<server>:/tmp/

# ② 服务器上跑(以部署用户;deploy.sh 幂等,可重跑)
cd /tmp/huawei-cloud && ./deploy.sh --commit <main-HEAD-sha>
#    不给 --commit 则钉 origin/main HEAD。日志逐行留痕;结束时 systemd active + cron list 冒烟。

# ③ deploy.sh 会停在 EnvironmentFile 占位模板处 → 手填七值(§3)后重跑
```

deploy.sh 干了什么(全部幂等):前置自检(含代理探活/UTF-8/磁盘)→ git clone 钉 commit 到
`/opt/myssia`(git 走 `-c http.proxy=http://127.0.0.1:7890`)→ `uv venv && uv sync --all-extras`
(uv 走 `HTTPS_PROXY` 同代理)→ 数据根种子 `/opt/myssia-data/config/`(已有不覆盖)+
**keychain:→env: 引用改写(仅服务器副本,表驱动五组)** + **clash 上游 7897→7890** →
EnvironmentFile 存在性/600 校验 → systemd 单元安装(替换 `__MYSSIA_USER__`)+ enable + start。

**降级备选(mihomo 节点全死时,零外网依赖)**:

```bash
# Mac 侧打包:
cd <repo> && git bundle create /tmp/myssia.bundle main
uv cache dir   # 把该目录打包为 uv-cache.tar(须含 linux x86_64 轮子:
               # 预取命令 uv pip install --python-platform x86_64-unknown-linux-gnu \
               #   --python-version 3.12 -r <(uv export --all-extras --no-emit-project) --dry-run)
scp -o BatchMode=yes /tmp/myssia.bundle uv-cache.tar <user>@<server>:/tmp/deploy-bundle/
ssh <user>@<server> 'mkdir -p /tmp/deploy-bundle/uv-cache && tar -xf /tmp/deploy-bundle/uv-cache.tar -C /tmp/deploy-bundle/uv-cache'
# 服务器侧:
./deploy.sh --bundle-dir /tmp/deploy-bundle   # bundle 克隆 + UV_CACHE_DIR 离线 sync
                                            # + --no-extra agent-reach(情报线不用,毙掉 GitHub 直连依赖)
```

## 3. 凭据填写表(Mac 钥匙串逐把导出)

服务器 `/etc/myssia/env`(chmod 600;**值不进 git 不进档**)。Mac 钥匙串结构:service=`myia`,
account=规范名全名(`security find-generic-password -s myia -a <规范名> -w` 即导出值,secrets.py 契约)。

| EnvironmentFile 键 | Mac 钥匙串规范名 | Mac 导出命令 | 说明 |
|---|---|---|---|
| `MYIA_FIRECRAWL_URL` | `myia/firecrawl/url` | `security find-generic-password -s myia -a myia/firecrawl/url -w` | wool 被墙源/ai-vendor ZOL 云渲染 |
| `MYIA_FIRECRAWL_KEY` | `myia/firecrawl/api-key` | `security find-generic-password -s myia -a myia/firecrawl/api-key -w` | 同上配对键 |
| `MYIA_LLM_BASE_URL` | `myia/llm/local-base-url` | `security find-generic-password -s myia -a myia/llm/local-base-url -w` | **服务器侧值改写为 `http://<Mac 局域网 IP>:1234/v1`**(R5 默认;Mac IP 变更=改这一行) |
| `MYIA_LLM_KEY` | `myia/llm/local-api-key` | `security find-generic-password -s myia -a myia/llm/local-api-key -w` | LM Studio 本地无鉴权,占位键(任意非空串) |
| `FEISHU_ANALYST_OPEN_ID` | `myia/push/FEISHU_ANALYST_OPEN_ID` | `security find-generic-password -s myia -a myia/push/FEISHU_ANALYST_OPEN_ID -w` | 日报投递目标(叶名=env 名契约,base.py:278) |
| `FEISHU2_APP_ID` | `myia/push/FEISHU2_APP_ID` | `security find-generic-password -s myia -a myia/push/FEISHU2_APP_ID -w` | 出站 bot「AI信息分析师」(**字面 env 名**,feishu_card.py:309 BOT_APP_CREDENTIAL_KEYS;无 keychain: 引用形态,EnvironmentFile 直填) |
| `FEISHU2_APP_SECRET` | `myia/push/FEISHU2_APP_SECRET` | `security find-generic-password -s myia -a myia/push/FEISHU2_APP_SECRET -w` | 同上配对键 |

填写流程:Mac 逐把导出 → `scp` 明文值文件(用完即删)或直接 SSH 手敲 → `sudo chmod 600 /etc/myssia/env`
→ 核验 `sudo grep -cE '^[A-Z0-9_]+=' /etc/myssia/env` ≥7。

**keychain→env 引用改写表**(deploy.sh 内置,仅服务器副本;仓库 config 保持 keychain: 不动):

| 服务器配置里(改写后) | 原(Mac)形态 |
|---|---|
| `env:MYIA_FIRECRAWL_URL` | `keychain:myia/firecrawl/url` |
| `env:MYIA_FIRECRAWL_KEY` | `keychain:myia/firecrawl/api-key` |
| `env:MYIA_LLM_BASE_URL` | `keychain:myia/llm/local-base-url` |
| `env:MYIA_LLM_KEY` | `keychain:myia/llm/local-api-key` |
| `env:FEISHU_ANALYST_OPEN_ID` | `keychain:myia/push/FEISHU_ANALYST_OPEN_ID` |
| (零出现)`keychain:myia/llm/modelscope-*` | R2b 前置修复已切本地;deploy.sh 残留即硬报错 |

## 4. 数据搬种

铁律:**Mac 生产库禁 `cp` 直拷**(weixin 品类每 5 分钟在写,并发写期文件拷贝=损坏风险)——
一律 SQLite 在线备份 API(design §4):

```bash
# Mac 侧(择品类 run 空窗,间隔分钟级即可,SQLite 无长事务):
sqlite3 "$HOME/Library/Application Support/MYIA/myssia.db" ".backup /tmp/myssia-seed.db"
sqlite3 ~/.myia/urlwatch/cache.db ".backup /tmp/urlwatch-cache-seed.db"  # urlwatch 缓存确在 ~/.myia(urlwatch adapter 判例)
scp -o BatchMode=yes /tmp/myssia-seed.db /tmp/urlwatch-cache-seed.db <user>@<server>:/tmp/
md5 /tmp/myssia-seed.db   # 两端核对一致再落位

# 服务器侧落位:
sudo -u deploy cp /tmp/myssia-seed.db /opt/myssia-data/myssia.db
sudo -u deploy mkdir -p /opt/myssia-data/urlwatch && sudo -u deploy cp /tmp/urlwatch-cache-seed.db /opt/myssia-data/urlwatch/cache.db
md5sum /opt/myssia-data/myssia.db   # 与 Mac 端核对

# 云端首轮:9 采集品类各手动跑一次(--json 留痕)——预期 dedup seen 全留痕、零推送
# (新条目按正常语义放行并记数;urlwatch 基线平移后 last_skip_reason=watch_unchanged)
for c in ai-news wool watch-deals ai-vendor-daily ai-token-deals games stocks news gpu-prices; do
  sudo -u deploy env MYIA_HOME=/opt/myssia-data /opt/myssia/.venv/bin/myssia run \
    /opt/myssia-data/config/$c.yaml --config /opt/myssia-data/config/proxy-pools.yaml \
    --dry-run --json | head -40
done
```

## 5. 影子期(≥1 天)

**前置门**:LLM 端点实弹先行——云端 `curl http://<Mac-IP>:1234/v1/models` 通,且 enrich/translate
真跑一条出中文译名(否则云端缺译名/低价值折叠,对照必失真)。

```bash
# 云端挂 9 采集品类 cron(daily-digest 不挂!);schedule 用品类 YAML 自带值
for c in ai-news wool watch-deals ai-vendor-daily ai-token-deals games stocks news gpu-prices; do
  sudo -u deploy env MYIA_HOME=/opt/myssia-data /opt/myssia/.venv/bin/myssia cron create \
    "auto" --category /opt/myssia-data/config/$c.yaml \
    --config /opt/myssia-data/config/proxy-pools.yaml --db /opt/myssia-data/myssia.db
done
sudo -u deploy env MYIA_HOME=/opt/myssia-data /opt/myssia/.venv/bin/myssia cron list
```

- 影子日对照(dry-run 不渲染模板,故用 **stdout 通道变体**):服务器侧 daily-digest 副本
  push 的 channel 改 `stdout` → 真跑出全文 vs Mac 同槽实发,条数/分区/译名抽查 diff 入档。
- 网络定档:stocks Yahoo 腿经 clash 池 200;wool 被墙源 firecrawl 计数>0;ai-news 海外 RSS
  源逐个实测,不可达者在服务器副本加 `pool:clash` 并记表。
- 期内 Mac 照常发报(S1 已停老线,无双发)。

## 6. 切割

同一槽窗内完成(避免双发;发报方唯一性是硬约束):

```bash
# ① Mac:备份 + 移除 10 件情报线(消息平台线 weixin/tg/telegram/feishu-groups 不动)
cp "$HOME/Library/Application Support/MYIA/cron/jobs.json" "$HOME/Library/Application Support/MYIA/cron/jobs.json.bak-$(date +%F)"
myssia cron remove <job-id…×10>   # 以 cron list 实况为准,逐件核对
myssia cron list                   # 核对只剩消息平台线

# ② 云端:挂 daily-digest(任务档 Step 5 定 "5 8,12 * * *";品类 YAML 缺省 "5 8,20 * * *",以 Step 5 实操裁决为准)
sudo -u deploy env MYIA_HOME=/opt/myssia-data /opt/myssia/.venv/bin/myssia cron create \
  "5 8,12 * * *" --category /opt/myssia-data/config/daily-digest.yaml \
  --config /opt/myssia-data/config/proxy-pools.yaml --db /opt/myssia-data/myssia.db

# ③ 下一槽真发验收:主人收件箱收到「AI信息 · 日期-AM/PM」一条(分析师私聊)——回执入档
# ④ 回滚演练(AC7):非发报窗反向走一轮(见 §8),分钟级,计时入档
```

## 7. 升级

数据不动(`/opt/myssia-data` 独立),三步:

```bash
sudo -u deploy ./deploy.sh --commit <new-sha>   # fetch+checkout+uv sync+种子补缺+改写重放+restart
journalctl -u myssia-cron -n 20                 # 升级后首跳核验
```

注意:数据根品类副本**已有不覆盖**(补种幂等)——品类 YAML 语义变更需手动 diff 后更新
服务器副本(改完重放改写:`deploy.sh` 重跑即治愈)。

## 8. 回滚(双向)

| 方向 | 操作 | 时长 |
|---|---|---|
| 云 → Mac(切回 Mac 发报) | ① 云端 `sudo systemctl stop myssia-cron`(停采集+发报);② Mac `cp "$HOME/Library/Application Support/MYIA/cron/jobs.json.bak-<日期>" "$HOME/Library/Application Support/MYIA/cron/jobs.json"` 恢复 + `myssia cron list` 核对;③ 老线若需复活:恢复 crontab 备份(附录 A ① 的文件) | 分钟级 |
| Mac → 云(再切回) | Mac 再移除 + 云端 `sudo systemctl start myssia-cron` + digest job 核对 | 分钟级 |

回滚演练(AC7)在切割后非发报窗走一轮全程计时,记录入档。

## 9. 排障

**口诀:源批量 empty → 先 curl 直连 vs 代理各测一次,再定路由。**

```bash
curl -sI --max-time 10 <源URL> | head -1                      # 直连
curl -x http://127.0.0.1:7890 -sI --max-time 10 <源URL> | head -1   # 走 mihomo
# 直连通+代理死 → 该源留 direct;直连死+代理通 → 服务器副本加 pool:clash;
# 双死 → 源本身问题(站方/WAF),勿瞎改路由。bbs.bt.sb=WAF 判死判例。
```

| 症状 | 判读/处置 |
|---|---|
| 服务没起来 | `systemctl status myssia-cron` + `journalctl -u myssia-cron -n 50`;EnvironmentFile 缺键=启动即失败(fail-fast 属预期) |
| 品类装载报 `invalid_credential_ref` | EnvironmentFile 缺键/值空:§3 表逐键核对;`keychain:` 残留=改写没跑:`./deploy.sh` 重跑治愈 |
| 品类装载报 `env_var_missing` | systemd 单元 EnvironmentFile 没吃到:`systemctl show myssia-cron -p EnvironmentFiles` |
| enrich 全降级(`WARNING` + 零译名/关键词粗筛) | **Mac LM Studio 不可达**(Mac 睡眠/关机/IP 变)=设计内降级,不阻管线,醒后自愈;持续两槽以上才查:Mac 端 LM Studio 是否开 0.0.0.0、`curl http://<Mac-IP>:1234/v1/models` |
| git/uv 卡死 | mihomo 节点失效:06:00 自动刷节点(老线机制),或手动换节点;急用走 §2 降级备选 bundle |
| 意外重推(搬种后) | 立即停(`systemctl stop myssia-cron`)→ 回查搬种窗 md5 与 `deploy-facts.txt` |
| 看 job 实况 | `sudo -u deploy env MYIA_HOME=/opt/myssia-data /opt/myssia/.venv/bin/myssia cron list`;doctor 逐上游健康:`… myssia doctor --config /opt/myssia-data/config/proxy-pools.yaml` |

---

## 附录 A:S1 老线暂停操作契约(design §9)

> 主人 10-24 裁定「按推荐」提前至开工首动作;暂停而非删除,可逆性优先;
> **仅动 ai-news 相关 crontab 三条**;mihomo/new-api/宝塔零触碰。

```bash
# ① 备份(在案即 AC9 证据)
crontab -l > ~/crontab.bak-$(date +%F)
# ② 注释恰好三条(ai-news 链:wf_crawl/watch_deals/ai_daily_report 或 run_daily 封装)
#    sed 匹配串以服务器 crontab -l 实况为准(预演:grep -n 确认命中行数=3±1)
crontab -l | sed 's/^\(.*wf_crawl\)/# \1/; s/^\(.*watch_deals\)/# \1/; s/^\(.*ai_daily_report\)/# \1/' | crontab -
# ③ 核验:非注释行不再含 ai-news 链;下一发报槽主人收件箱仅一条 Mac 日报(AC9)
crontab -l | grep -v '^#' | grep -E 'wf_crawl|watch_deals|ai_daily_report' || echo "✅ 老线已全停"
# ④ 保留声明留痕:docker ps 前后快照对照(mihomo/new-api/宝塔零触碰)
docker ps > ~/docker-ps-before-$(date +%F).txt
# 回滚(恢复老线):crontab ~/crontab.bak-<日期>  —— 分钟级
```

- ai-news:local 镜像与 /opt/ai-news 目录:S1-S4 全程不动(容器本就 `run --rm` 无常驻);
  S4 退役确认后资源回收(镜像/目录清理)=主人裁决项,只出建议清单。


### 手动跑铁律(10-24 杂库事故判例)

手动 `myssia run` 必须**锚定数据根**:`MYIA_HOME=<生产数据根> myssia run <品类> --db <生产库> --config <pools>`(或干脆 `--dry-run`)——漏锚定时 run 的 `--db` 缺省是 **cwd 相对** `./myssia.db`,会跑进任意当前目录的杂库(空去重态→历史库存全按新条目真推,10-24 云侧 5 卡事故实证)。
