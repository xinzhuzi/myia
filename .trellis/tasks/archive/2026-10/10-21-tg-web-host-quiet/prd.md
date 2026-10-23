# TG 网页线宿主静默——停用线不再每次启动刷打开群超时告警

## Goal

已停用的 TG 网页监控线宿主进程随 app 启动仍反复拉起并每几分钟报 tg_web_dom_stale open_timeout 告警刷日志;停用线应静默,不产生重复告警。

## Requirements

- 哨兵死键持久化:manager 记致命哨兵(tg_web_logged_out/tg_web_dom_stale)告警时同步落死键标记 `<数据根>/telegram-web/web-line-dead.json`;未知异常(tg_web_error)可能瞬态,不落标。
- 装配期跳过:`assemble_web_manager` 跳过跳过窗(24h TTL)内的死键,note 带停用时刻与重登指引;全死 = manager 不起 + 单条静默 note;部分跳过 = manager 照起 +「备注」级 note(entry/cli 两消费面措辞分档)。
- 自愈与恢复:TTL 过期放行一次重试(清标入列;再死由哨兵重标记);`myssia telegram web-login` 登录成功即时清标。
- 标记读写全 best-effort:损坏/缺失 = 空表,绝不拦装配。

## Acceptance Criteria

- [x] 致命哨兵记告警同步落标;tg_web_error 不落标(manager 级测试双例)
- [x] 装配跳过窗内死键(note 带指引)/全死返回 None+note/过期死键清标放行(装配级测试三例)
- [x] 标记助手往返/清空删文件/TTL 窗/坏时间戳与坏文件容忍(web_line 纯函数测试);web-login 登录成功清标(登录流测试)
- [x] 门禁全绿(tests/telegram 65 + 全量 pytest 6493 + vitest 961 + tsc/build)

## 执行记录

- 触发:10-20 诊断 TG「今日 0 条」时发现——TG 网页线(待重登,job 已停用)
  的宿主随每次 sidecar 启动重演「启动→开群失败 open_timeout→哨兵告警」,
  当天上午 sidecar 多次重启放大成刷屏;主人批「立,然后做」。
- 实现:web_line.py 标记助手五件(dead_marker_path/read/mark/clear/
  fresh_dead_accounts,24h TTL);web_host.py assemble 跳过+过期清标+
  manager `dead_mark_root` 参数+`_record_alert` 落标;web_line 登录流
  成功点清标;entry.py/cli.py note 措辞分「未起/备注」两档。
- 实装语义:换装后首个启动仍会跑一轮死键(open_timeout 一次)落标,此后
  24h 内重启零重试零告警;TTL 到点自动放行一次重试保自愈;重登
  `web-login --account <键> --force` 即时复活。
