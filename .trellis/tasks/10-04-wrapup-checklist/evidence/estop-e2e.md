# 急停双向端到端实证(真冻结包 /Applications/世事.app 00:16 版,2026-10-05 00:37-00:41)

- 沙箱 MYIA_HOME=/tmp/myia-estop-e2e;job estop-e2e(every 1m, fixture 品类,deliver local);app 直跑(静默)。
- 链路:①00:37:33 tick 派发(failed=夹具端口乌龙 8766≠8765,与机制无关)→ ②`cron pause --all` 踩下(marker 确认)→ ③**急停期 70+s 零新派发**(job 每分钟到期,tick 全跳;ticker 心跳持续 4s 级=跳过≠僵死)→ ④`cron resume --all` 解除 → ⑤00:40:33 新 tick **completed**(管线真成功,源 1/1)。
- 结论:estop「跳过派发/不动 ticker/恢复即再燃」在桌面宿主全链成立;操作单步骤 4 的机器可验部分已代验,主人只剩亲手点按钮的体感确认。
