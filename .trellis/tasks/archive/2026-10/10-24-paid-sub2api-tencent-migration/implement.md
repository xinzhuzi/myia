# Implement — 付费站迁移腾讯轻量(执行序 + 验证计划)

> 执行纪律:每步「跑 X → 期望 Y」是契约,偏离即停;改配置先备份;两台机均已 Mac 免密(付费站 root@121.43.125.157 / 新机 root@110.40.210.242);服务器间直传先打通互信。
> 主档:~/Project/Server/AI站点/腾讯云服务器-付费.md(状态表同步更新)

## 阶段 0:准备(新机)— 状态:Docker 已装 ✅,剩 8080 放行

- [ ] 0.1 控制台防火墙放行 8080(网页操作:轻量控制台 → 防火墙 → 添加规则 TCP:8080)→ 验证 `nc -z 110.40.210.242 8080` 通(此时无服务,通了说明规则在;不通也无妨,起服后再验 AC4)
- [x] 0.2 新机拉镜像(走已配加速):
  ```bash
  ssh root@110.40.210.242 'docker pull docker.1panel.live/weishaw/sub2api:0.2.18 && docker pull docker.m.daocloud.io/library/postgres:18-alpine && docker pull docker.m.daocloud.io/library/redis:8-alpine && docker pull docker.1panel.live/metacubex/mihomo:v1.19.29'
  ```
  期望:四个镜像 `docker images` 可见
- [x] ~~0.3 打通两机互信~~ 预演改为 Mac 中转流式(旧机只读铁律,不写 authorized_keys);终迁沿用 Mac/云端直传:Mac 公钥已在两机;在新机生成/复用密钥 → 把新机公钥追加到旧机 authorized_keys → 验证 `ssh root@110.40.210.242 'ssh -o BatchMode=yes root@121.43.125.157 echo OK'` 返回 OK

## 阶段 1:文件复制(旧 → 新,直传)

- [x] 1.1 旧机打包(预演 10-24:tar czf - 流式 69.1MiB,旧机零落盘)(排除卷目录与历史备份,按 D3 只带最新备份):
  ```bash
  ssh root@121.43.125.157 'cd /root && tar czf /tmp/paid_migrate.tgz \
    sub2api-deploy/docker-compose.yml sub2api-deploy/.env sub2api-deploy/data \
    sub2api-deploy/mihomo \
    $(ls -t /root/sub2api-deploy/backup_pre_0.2.18_paid_*.sql.gz | head -1 2>/dev/null; echo "") \
    --transform "s|^sub2api-deploy|sub2api-deploy|" 2>/dev/null; ls -lh /tmp/paid_migrate.tgz'
  ```
  期望:tgz 出现,~数十 MB(data/ + mihomo/ + 最新备份)
- [x] 1.2 新机拉取解包(权限 600 已修正):`scp`/直传 → `tar xzf -C /root` → 权限修正 `chmod 600 .env mihomo/config.yaml`
- [x] 1.3 AC1 验证(三组 md5 两机一致):两机 `md5sum docker-compose.yml .env mihomo/config.yaml` 三处一致

## 阶段 2:数据导出导入(docker 方式)

- [x] 2.1 旧机导出(预演:66M,gzip -t 过;⚠️经 Mac 仅 ~50KB/s 耗时 22.5 分钟——终迁改旧机→新机云端直传)(全量即时):
  ```bash
  ssh root@121.43.125.157 'docker exec sub2api-postgres pg_dump -U sub2api -d sub2api | gzip > /root/sub2api-deploy/migrate_full_$(date +%Y%m%d_%H%M).sql.gz && gzip -t <同文件> && ls -lh'
  ```
  期望:新 gz ~67M,gzip -t 通过
- [x] 2.2 新机先起数据层(15 秒双 healthy)(不起 sub2api):`cd /root/sub2api-deploy && docker compose up -d postgres redis` → 两个 healthy
- [x] 2.3 导入(1 分 38 秒,零 ERROR 零 WARNING):
  ```bash
  ssh root@110.40.210.242 'gunzip -c /root/sub2api-deploy/migrate_full_*.sql.gz | docker exec -i sub2api-postgres psql -U sub2api -d sub2api -q'
  ```
  期望:无 ERROR 行(grep -c ERROR = 0 或仅无害 NOTICE)
- [x] 2.4 AC2 验证(四表 73/68/7/37548 两机一致):两机各跑关键表计数对比(accounts/users/proxies/usage_logs,基线 73/68/7/37k+):
  ```bash
  for t in accounts users proxies usage_logs; do echo "$t: $(docker exec sub2api-postgres psql -U sub2api -d sub2api -tAc 'select count(*) from '$t)"; done
  ```
  期望:逐表与旧机一致(proxies 含软删共 7 条,勿以页面 5 条为准)

## 阶段 3:起服验证(新机)

- [x] 3.1(首轮轮询即 healthy,/health ok,版本 0.2.18) `docker compose up -d` → sub2api healthy;`curl -s localhost:8080/health` = {"status":"ok"};版本接口 = 0.2.18
- [x] 3.2 mihomo(五组出口已记录,零测速):`cd mihomo && docker compose up -d` → `bash node-status.sh` 五组可读,当前出口已自动选(新 IP 表现仅观察记录,不测速——铁律)
- [x] 3.3 admin 登录+代理 7 条核验一致 登录 + IP管理 5 条 + 账号绑定抽查(fanren 系→#1、aiwanwu→#3)
- [x] 3.4 AC4 外部验证:✅10-24 终验通过——用户放行 8080(IPv4+IPv6)后,短暂拉起 sub2api 实测 Mac→110.40.210.242:8080 返回 {"status":"ok"} HTTP 200/26ms,验后停回冷备(IPv6 000 属预期:容器绑 0.0.0.0 仅 IPv4):Mac `curl http://110.40.210.242:8080/health` 200(公网可达)→ **验证通过后立即关闭 8080 防火墙规则(D2)**,阶段 5 切换前再开
- [x] 3.5 整栈停(sub2api/node-proxy Exited(0);postgres/redis 留守 healthy) **按 D1 整栈停(升级版)**:新机 `cd /root/sub2api-deploy && docker compose stop sub2api && cd mihomo && docker compose stop`——sub2api 与 mihomo 全停(73 账号双机调度/测试流量归零、R2 备份不再双写);postgres/redis 纯本地无外联,留着便于抽查;切换前再起
- [x] 3.6 停后快照(冷备基线:Exited(0)/Up healthy/磁盘 161G 余,已在预演报告):`docker ps -a` 状态存档到任务目录(冷备基线)

## 阶段 4:双跑一周(10-24 → 约 10-31)——实为"旧机运行 + 新机冷备"

- [ ] 4.1 每日巡检(只读,~1 分钟):旧机容器 healthy / R2 备份 completed;新机 sub2api+mihomo 保持 stopped、8080 关闭(AC5)
- [ ] 4.2 新机不接真实流量、不动数据;期间旧机正常运营
- [ ] 4.3 **10-30 前置检查(D5)**:zhuzibaijia.site 是否已接入 CF 且回源旧机可用——就绪则阶段 5 域名切换,未就绪走 IP 切换分支(域名后补仅改 DNS)

## 阶段 5:终迁(⚠️提前执行:2026-10-24 上午用户拍板,弃剩余观察期)

> 全程目标 ≤15 分钟停机:旧机停服 → 干净 dump → 传输导入 → 新机起服 → 切流量

- [x] 5.0 8080 已放行且双栈(BIND_HOST 修正:0.0.0.0+[::] 双条目,docker 单[::]是 v6-only 的坑);域名已指新机
- [x] 5.1 旧机停服+最终干净导出(11:17:06 停机;migrate_final_20261024_1117.sql.gz 67M md5=47d25321):
  ```bash
  ssh root@121.43.125.157 'cd /root/sub2api-deploy && docker compose stop sub2api && sleep 5 && docker exec sub2api-postgres pg_dump -U sub2api -d sub2api | gzip > /root/sub2api-deploy/migrate_final_$(date +%Y%m%d_%H%M).sql.gz && gzip -t /root/sub2api-deploy/migrate_final_*.sql.gz && ls -lh'
  ```
- [x] 5.2 云端直传 2 分 45 秒;清库重建导入零 ERROR:
  ```bash
  ssh root@110.40.210.242 'docker compose stop sub2api 2>/dev/null; gunzip -c migrate_final_*.sql.gz | docker exec -i sub2api-postgres psql -U sub2api -d sub2api -c "DROP DATABASE..." # 实操:先 psql 建空库再整库导入,见下方细案'
  ```
  细案(防手滑):新机 `psql -U postgres` 层面 `drop database sub2api; create database sub2api owner sub2api;` → 导入 final → grep ERROR=0
- [x] 5.3 新机起服(sub2api+mihomo 全起,R2 02:00 备份排程随库迁移生效):`docker compose up -d sub2api` + `cd mihomo && docker compose up -d`(撤 D1)→ 重复 AC2/AC3 验证(四表计数=旧机停服时刻;最后一条 usage_log 对齐)
- [x] 5.4 域名即刻生效(http://zhuzibaijia.online:8080 → 200/23ms;www 同通;四表 73/68/7/37548 与旧机一致):域名就绪→CF DNS 切新机(用户无感或改一次 base_url 为域名);未就绪→通告用户改 `http://110.40.210.242:8080`
- [x] 5.5 旧机 sub2api+mihomo 已停(postgres/redis 保留回滚);11:26:00 停机窗口结束,**全程 8 分 54 秒**;回滚=旧机 compose start+用户改回 IP;保留至约 11-07 后释放保持 `docker compose stop`(数据不删),文档记回滚法(旧机 `up -d`+端点改回);**至约 11-14 无回滚需求后释放实例**(D6)

## 回滚总纲

- 阶段 0-4 任一步失败:新机清掉重来,旧机零影响
- 阶段 5 切换后异常:旧机 `docker compose start` + 用户端点改回 121.43.125.157:8080,5 分钟内可回
