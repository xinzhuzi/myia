# PRD — 付费站 sub2api 迁移腾讯轻量(全量复制 → 双跑一周 → 终迁数据)

## Goal

把阿里云付费站(121.43.125.157,sub2api 0.2.18 + mihomo 节点桥,2C2G 老机)整体迁移到腾讯轻量新机(110.40.210.242,4C/7.5G/177G,1024 秒杀购入)。今天完成全量复制与起服验证,双跑观察一周后,仅做一次**最终数据迁移**完成切换。全程旧机为主、用户流量零感知,任何一步失败可回退。

## 背景与现状

- 旧机:sub2api 0.2.18 + postgres 18 + redis 8 + node-proxy(mihomo v1.19.29,43 节点五组全 fallback 架构,详见《AI站点/阿里云服务器-付费-出口节点桥接.md》10-23 章节);数据 ~67M(pg_dump gz)
- 新机:Ubuntu 26.04,Docker 29.1.3 + Compose 2.40.3 已装(2026-10-24),registry 双镜像加速已验证,root/Admin123#,Mac 公钥免密;**除 Docker 外白板**
- 已知差异点:跨境风控按源 IP 计,新 IP 节点表现需重新观察;腾讯轻量防火墙走网页控制台

## 已定案的八项决策(2026-10-24 grill 拷问后拍板,"全按推荐")

- **D1 双跑期新机整栈停(升级)**:原"只停 mihomo"有真缺口——73 账号会被两台机同时调度/测试(上游双份流量风险)+ 02:00 R2 备份双写,而新机数据终迁时反正被覆盖。改为:阶段 3 验证完成后**停 sub2api + mihomo**(外联流量归零;postgres/redis 纯本地可留着),切换前再起
- **D2 8080 验完即关(细化)**:阶段 0 放行用于外部验证,阶段 3 验证通过后**立即关闭**,阶段 5 切换前再开——避免一台"数据陈旧+密码已知"的面板公网暴露一周
- **D3 历史备份只带最新一份**:`backup_pre_0.2.18_paid_*.sql.gz` 随迁,其余留旧机
- **D4 终迁接受停机窗口**:约 10-31 凌晨低峰,**旧机先停服 → 干净 dump → 传输导入 → 新机起服**,全程 10~15 分钟,零数据丢失(1.26GB 库 dump 约 1-2 分钟,传输 ~67M 秒级)
- **D5 域名优先切换**:「zhuzibaijia.site 接入 Cloudflare」列为本任务**阶段 5 前置**(10-30 前就绪);届时未就绪则先 IP 切、域名后补(用户侧只需再改一次,或直接改 DNS 用户无感)
- **D6 旧机退役时间线**:切换后**只读保留 2 周(至约 11-14)**,确认无回滚需求后释放
- **D7 apikey-monitor 不迁**:留旧机,以后要用单开任务
- **D8 新机为 1 年期**(至约 2027-10-24),长期服务可放心落位

## Requirements

- R1 文件层:旧机 `/root/sub2api-deploy/`(docker-compose.yml、.env、data/、mihomo/ 整目录含全部节点凭据与工具脚本)→ 新机同路径,权限保持(.env/config.yaml 600)
- R2 数据层(docker 方式):旧机 `docker exec sub2api-postgres pg_dump | gzip` 全量 → 新机 postgres 容器导入 → 与旧机核对(表数、账号数、用户数、IP管理 5 条代理)
- R3 镜像:新机直接拉(sub2api 0.2.18 / postgres 18-alpine / redis 8-alpine / mihomo v1.19.29),不做 docker save 搬运
- R4 起服验证:全栈 healthy + admin 登录 + 代理/账号绑定完整 + mihomo 五组就绪(node-status 只读,不压测)
- R5 双跑一周:旧机继续承载用户流量;新机按 D1 **sub2api+mihomo 全停**(冷备),不接真实用户(期间数据分叉以旧机为准);按 D2 新机 8080 处于关闭
- R6 终迁(约 10-31,按 D4 走停机窗口、按 D5 域名优先):凌晨旧机停服 → 最终干净 pg_dump → 新机重建导入 → 起服验证 → 重开 8080 → 切流量(域名或 IP)→ 旧机按 D6 只读保留 2 周后释放

## Acceptance Criteria

> 事实基线(2026-10-24 查证):旧库 1.26GB(dump~67M),accounts 73 / users 68 / proxies 7(页面见 5,含软删)/ usage_logs 37k

- [ ] AC1 新机 `ls /root/sub2api-deploy/` 与旧机结构一致,`.env`/`config.yaml` 权限 600,md5 与旧机一致
- [ ] AC2 新机 postgres 导入后:`CREATE TABLE` 数与旧机一致;accounts/users/proxies/usage_logs 四表计数两机一致(proxies 以 7 为基线);admin 可登录
- [ ] AC3 新机 `docker ps` 三容器 healthy;`/health` 200;mihomo 五组 fallback 就绪且 `node-status.sh` 可读(新 IP 表现仅观察记录,不压测)
- [ ] AC4 8080 公网可达验证通过(Mac `curl http://110.40.210.242:8080/health` 200)**后即关闭**(D2),阶段 5 切换前重开
- [ ] AC5 双跑期:旧机服务无中断;新机 sub2api 与 mihomo 均为 stopped、8080 关闭(D1/D2)
- [ ] AC6 终迁(停机窗口内完成):新机数据=旧机停服时刻全量(最后一条 usage_log 对齐);切换后旧机 `docker compose stop` 只读保留,回滚路径=旧机 `up -d` + 用户端点改回
- [ ] AC7 切换形态按 D5 执行:域名就绪则用户端点=域名(HTTPS);未就绪先 IP,域名后补仅改 DNS

## 范围外

- apikey-monitor(旧机另一项目)不迁;zhuzibaijia.site+CF 域名接入为独立任务(可在切换日并行);公益站/华为云不动
