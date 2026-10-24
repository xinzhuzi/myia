# implement.md — 10-24-huawei-cloud-deploy 执行计划

> 前置阅读:prd.md(R1-R5/AC)/design.md(三件契约/搬种/切割)。SSH 唯一入口:`bash ~/Project/Server/华为云/server-华为云.sh "<cmd>"`(密码动态读 华为云-服务器.md;**key 认证路径下脚本尾打 ❌+exit 1 是假阴性,以有无命令输出为准**——收编 s0 实证判例)。scp 走 ssh key BatchMode。

## Step 0 S1 老线暂停(开工首动作,主人 10-24 裁定提前)

- [ ] 0.1 design §9 契约:SSH `crontab -l > ~/crontab.bak-<日期>` 备份→注释 ai-news 三条(sed 预演行数核对=3±1)→`crontab -l | grep -v '^#'` 核验零 ai-news→`docker ps` 前后快照对照(mihomo/new-api/宝塔零触碰留痕)
- [ ] 0.2 下一发报槽验收:主人收件箱**仅一条 Mac「AI信息」日报**(AC9 前半);异常即恢复备份回 S0(分钟级)

**验证**:备份文件+核验输出+docker 快照三证入档;双发消除。
**回滚点**:crontab 备份恢复即回 S0。

## Step 1 部署件三件(仓库内,先行)

- [ ] 1.1 `deploy/huawei-cloud/deploy.sh`(design §2 契约:幂等/表驱动引用改写/proxy 7890 改写/前置自检含 locale UTF-8 与 uv 安装)
- [ ] 1.2 `deploy/huawei-cloud/myssia-cron.service`(design §2 单元全文)
- [ ] 1.3 `deploy/huawei-cloud/README.md`(手册九节,含 Mac 钥匙串导出命令表与排障口诀)
- [ ] 1.4 (grill 已盘出:FEISHU2_APP_ID/SECRET 字面 env 名,feishu_card.py:309;R3/design §3 表定稿)→ deploy.sh 改写表用定稿名
- [ ] 1.5 **R2b 前置修复**:ai-token-deals prompt 端点魔搭→本地 LM Studio(ai-vendor-watch 判例:local 引用+disable_thinking+fetch 超时预算);装载测试+全量 pytest 门禁

**验证**:`bash -n deploy.sh` 语法;本地 shellcheck(若有);表驱动改写对样例 yaml 单测式自验(sed 演练,dry-run 模式打印 diff)。

## Step 2 服务器环境(SSH 实操)

- [ ] 2.1 前置盘点:OS/systemd/python3 -V/uv/git/mihomo:7890 探活(`curl -x http://127.0.0.1:7890 -sI https://www.google.com | head -1`)、磁盘余量、UTF-8 locale
- [ ] 2.2 跑 deploy.sh(钉 main HEAD commit;**git/uv 全程走 mihomo 代理**——design §2 路由;系统 python 不足则 uv python install);克隆+uv sync 全程留痕
- [ ] 2.3 EnvironmentFile:按 README 表从 Mac 导出四组值手填(值不进 git 不进档;`security find-generic-password -s myia -a <名> -w` 逐把导出→scp→chmod 600);LM Studio 端点值待主人开 0.0.0.0 后填 Mac IP(先占位,影子期前补)
- [ ] 2.4 systemd enable+start;`journalctl -u myssia-cron` 首跳核验;`myssia cron list` 10 品类空表(未挂 job 属预期)

**验证**:AC2 前半(常驻 active)+品类装载抽测(`myssia run config/ai-news.yaml --dry-run --json` exit 0,零 invalid_credential_ref=AC3)。

## Step 3 数据搬种(design §4)

- [ ] 3.1 Mac **在线备份**(grill 定:weixin 每 5 分钟在写,禁 cp 直拷)——`sqlite3 <db> ".backup /tmp/x.db"` 分别备份 myssia.db 与 ~/.myia/urlwatch/cache.db → scp 备份件上云;md5 两端核对
- [ ] 3.2 云端手动跑 9 采集品类各一次(--json 留痕):预期 dedup seen 全留痕、零推送;新条目(停跑间隙)按正常语义放行并记数
- [ ] 3.3 urlwatch 基线平移核验:watch-deals run 后 last_skip_reason=watch_unchanged(非 baseline_seeded)

**验证**:AC4 前半;异常(意外重推)立即停——回查搬种窗与 md5。

## Step 4 影子期(≥1 天)

- [ ] 4.0 ~~S1 老线暂停~~(已前移至 Step 0,主人裁定;此处仅复核暂停仍生效)
- [ ] 4.1 云端挂 9 采集品类 cron(schedule 对齐 Mac 现产表);**daily-digest 不挂**
- [ ] 4.2 影子日对照(grill 修正法):云端 daily-digest **stdout 通道变体**真跑出全文 vs Mac 同槽实发——条数/分区/译名抽查,diff 记录入档
- [ ] 4.2b **影子前置门**:LLM 端点实弹(原 4.4)必须先于影子首日——否则云端缺译名/低价值折叠,对照必失真
- [ ] 4.3 网络定档(AC6):stocks Yahoo 腿经 clash 池 200;wool 被墙源 firecrawl 计数>0;ai-news 海外 RSS 源可达性实测定(不可达源服务器副本加 pool:clash,记表)
- [ ] 4.4 (已前移为 4.2b 影子前置门)LLM 端点实弹:主人开 LM Studio 0.0.0.0 后,云端 enrich+translate 真跑一条出译名(Mac 睡眠耐受=降级降级 WARNING 判读入档)

**验证**:AC4 后半+AC6;影子达标判据=同槽对照内容一致(条数差≤新条目数)且零意外推送。

## Step 5 切割(design §5,同槽窗内)

- [ ] 5.1 Mac:`cp jobs.json jobs.json.bak-<日期>` → `cron remove` 10 件情报线(消息平台线不动)→ list 核对
- [ ] 5.2 云端:挂 daily-digest `5 8,12 * * *` → 下一槽真发一条「AI信息」到分析师私聊
- [ ] 5.3 回滚演练(AC7):非发报窗演练一轮反向操作(云端 stop→Mac 恢复 bak→list 核对→再切回),全程计时分钟级,记录入档

**验证**:AC5+AC7;真发回执截图入档。

## Step 6 收尾

- [ ] 6.1 全档回填(各 AC 证据);若触产品代码:全量 pytest+ruff(AC8)
- [ ] 6.2 提交:deploy/ 三件+任务档;推送
- [ ] 6.2b AC10 转换映射核对:design §8 表 14 行逐行三态核(已承载/转换/如实弃用),核对留痕入档
- [ ] 6.3 交付汇报:上云拓扑图/终态形态(Mac=管理台+消息线,云=唯一情报线)/S4 老线退役确认清单(crontab 已注释+三重归档核验+资源回收**建议清单**——镜像/目录清理留主人动手)

## 依赖图

```
Step0(S1老线暂停·消双发)─→ Step1(仓库件)─→ Step2(环境)─→ Step3(搬种)─→ Step4(影子≥1天)─→ Step5(S3切割)─→ Step6(S4终态)
                              ↑______________回滚预案(R4/R6 状态机回退门)贯穿 0-5______________↑
```

## 风险与预案

| 风险 | 预案 |
|---|---|
| Linux 兼容缺口(未实跑边角) | Step2 装载抽测即暴露;最小修+AC8 门禁 |
| 搬种窗 Mac 在写 | 品类间隔选窗+md5 核对;异常即停 |
| 双发(现状 S0 已存在!) | Step 0 首刀即消(主人已裁);切割序同槽窗完成;影子期 digest 恒不挂 |
| 老线暂停误伤无关服务 | sed 预演行数核对+docker ps 前后快照;可逆(备份恢复) |
| Mac LM Studio 不可达(睡/关) | 降级路径设计内(粗筛+零译名);翻案项=funded 云钥 |
| mihomo 节点失效 | 老线 06:00 刷节点机制沿用;排障口诀在手册 |
