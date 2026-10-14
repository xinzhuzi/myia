# 微信新消息通知线部署启用

## Goal

仓库 config/weixin-notify.yaml(已入库)部署到数据根 config/ + cron 注册 + 白名单(照 weixin.yaml 既有形态)+ 一次真扫描回执(notify-scan 只读)

## Requirements

- 数据根 = `~/Library/Application Support/MYIA`(生产真相源);只动 config/ 与 cron,禁写微信侧任何数据。
- 白名单值照 weixin.yaml 既有 localdb 会话键(`50438708676@chatroom`,weixin.yaml:61),不发明新键;键名用 schema 定名 `chat_whitelist`。
- cron 注册走仓库正道 `myssia cron create`(jobs.json 由 CLI 落,不手写 JSON);分钟级档位照配置面 `*/1 * * * *`。

## Acceptance Criteria

- [x] AC1 配置部署:部署基线一致——部署核验时点(覆写前)diff 逐字一致 exit 0(前次部署已在位,本任务免覆写;备份件 `weixin-notify.yaml.bak-20261014-122531` 留改前态);AC2 白名单回填后数据根版含启用态、预期领先仓库版一处(56-58 行:仓库 `chat_whitelist: []` 出厂空 vs 数据根 `["50438708676@chatroom"]`),此后 diff exit 1 属预期态而非漂移(2026-10-14 15:10+08 复核实跑 EXIT=1,分叉仅此一处)。
- [x] AC2 白名单回填:`chat_whitelist: ["50438708676@chatroom"]`(照 weixin.yaml:61 既有会话键,零新键);YAML 重解析验证通过(channel=notify)。
- [x] AC3 cron 注册:`myssia cron create '*/1 * * * *' --category <数据根>/config/weixin-notify.yaml --name 微信通知 --db <数据根>/myssia.db` → job id `d72dbcbb7cbb`,enabled=true,timezone Asia/Shanghai,deliver local;jobs.json 落位验证通过;品类完整装载校验含白名单(create 早失败机制下 exit 0 = 配置合法)。
- [x] AC4 真扫描回执(桥 notify-scan 只读,stdin 形状照引擎 wechat_local_notify.py:485-493):
  - 首轮(baseline=null):exit 0,events=0(首轮只建基线零事件,防装机首弹轰炸——设计形态),baseline 建立含 1 会话;stats: sessions_scanned=454 / whitelist_sessions=1 / candidates=1 / msg_rows_read=0 / db_busy=False / duration_ms=5(白名单会话在 SessionTable 命中,恒轻实证)。
  - 次轮(带首轮 baseline):exit 0,events=0,candidates=0(水位比较后无未读变化 → 零二次查库,增量路径零误报)。
  - 复核补扫(2026-10-14 15:10+08;上两轮系部署时点一次性回执,本轮以现行真实水位增量路径重放——stdin 照引擎 wechat_local_notify.py:485-493 同构,baseline 取 myssia.db change_baseline 现行 etag):exit 0,events=0,candidates=0;stats: sessions_scanned=458 / whitelist_sessions=1 / msg_rows_read=0 / self_filtered=0 / revoke_events=0 / db_busy=False / duration_ms=4(回执件 /tmp/wxn-scan-out-recheck.json,形状级,正文不外引)。
- [x] AC5 cron 真跑闭环:注册后 ticker 按 */1 分钟级真执行(12:28–12:34 七轮全 completed,`cron runs` 账本),job last_status=ok / failure_streak=0;引擎侧水位键 `wechat-local://watermark/weixin-通知` 在 myssia.db change_baseline 表建立并回写(12:39 +08)——cron 管线→桥→水位回写全链路实证。

## 回执(R 真数据,形状级,正文红线不外引)

- 桥版本:wechat-bridge 0.8.3(notify-scan 需 0.8.0+;`~/.myia/plugins/wechat-bridge/bin/wechat-bridge` 引擎缺省路径与数据根 `python/bin/wechat-bridge` 双位同版)。
- 扫描回执文件:/tmp/wxn-scan-out.json(exit 0;仅本机暂存,不含推送)。
- cron 账本:`myssia cron runs 微信通知` 7 条 completed(source=tick;部署时点 12:28–12:34)。2026-10-14 15:05+08 复核:cron/executions.db 实查 job `d72dbcbb7cbb` 累计 154 条 completed、零其他状态(12:28:04→15:05:11 分钟级连跳);jobs.json last_status=ok / failure_streak=0 / last_run_at 持续推进。
- 私有数据红线:enrich 关/push 仅 macos_notify(本机零网络)/扫描只读解密副本 mode=ro,零微信进程干预。

## Notes

- Keep `prd.md` focused on requirements, constraints, and acceptance criteria.
- Lightweight tasks can remain PRD-only.
