# evidence(10-14 晚轮:Phase 0 工具整备 + Phase 1 r1 活体猎捕)

> 产物根:`/Users/zhengbingjin/Downloads/微信反编译/sendmsg-勘察-1014/`(下称 `<勘察>`)。本档由簿记员依据落盘产物核验后记录(逆向产物只引路径不外发原文)。零伤核验:run-sheet r1 尾行记录新 PID 40379 存活、零 lldb/debugserver 残留;簿记员本轮只读复核 `pgrep -x WeChat`=40379 在跑、`ps aux | grep -E 'lldb|debugserver'` 空。

## Phase 0 工具整备(门 1 绿)

| # | 项 | 结果 | 证据(路径) |
|---|---|---|---|
| E1 | cap.py v2.1(堆扫 ReadMemory 4MB 分块+块尾重叠去重+双探针分级烧窗/线程名过滤/窗口开关+TTL 30s/活体枚举优先 vmmap 回退) | ✅ 干跑 A1-A12 全 PASS | `<勘察>/dryrun/phase0-dryrun.log`(2026-10-14 20:31:22,FAIL 数 0;`<勘察>/tools/test_offline.py` 23/23;干跑样例目录 `<勘察>/dryrun/test-hits-A2…A12、-A8-reg/-A8-mem/-A4-debug、test-hits-C`) |
| E2 | 归因链 attribute.py + fstarts.py(薄片 LC_FUNCTION_STARTS 387,126 起点,唯一函数边界源) | ✅ 假 hit 干跑 C0-C4 全 PASS(slide 错 rc=3 / 残缺 hit rc=2 / 函数表边界 rc=3,均干净退出不猜) | 同上 log C 节;真 hit 归因产物形态见 `<勘察>/hunt/attr_hit_20261014-204122_846.{json,txt}` |
| E3 | blscan.py / refscan3.py 固化进 tools/(/tmp 不可信判例) | ✅ B1-B4 与 /tmp 版既有产物逐点等价(rpc_stub 0x5e1d050=27743 调用点;submitter 0x490fb20=0 不翻案;refscan3 五默认页+xkey 校准页 826 自检非零) | 同上 log B 节;`<勘察>/tools/README.md` 清单与已知边界 |
| E4 | 门 1 判定 | ✅ **绿**(零微信零 attach 零发送) | `<勘察>/dryrun/phase0-dryrun.log` 尾节「FAIL 数: 0」 |

## Phase 1 r1 活体猎捕(轮失败,事故在案,门 2 未达)

| # | 项 | 结果 | 证据(路径) |
|---|---|---|---|
| E5 | run-sheet 八步执行(slide=0x12d034000,锚点 0x490fb20 活体 16B 与薄片逐字节一致;真机冒烟 attach→布防→禁用→detach 零异常) | ✅ 过程完成(结果失败) | `<勘察>/hunt/run-sheet-r1.md` 时间线;`<勘察>/hunt/smoke.log`;`<勘察>/hits/vmmap.txt`(③ 快照留保险) |
| E6 | 触发=桥备选自动发 1 条(filehelper,嘻嘻;本相位唯一授权) | ❌ 桥 3 次断言超时 rc=30「发送未执行」,**实际出站 0 条**(DB 侧 filehelper msg_count=62/last_ts=1791962569 与开火前一致) | run-sheet-r1.md 20:40:19-20:40:54 行与 20:50 回执行 |
| E7 | bp1/bp2 运行时热度与身份实证 | bp2(0x5e1d680)=**4 字节 thunk 死点**(窗口内 ~85/s、全程 5374 次);bp1(0x5e1d050)=108B 协程通用投递辅助 | run-sheet-r1.md 风暴行;错题集 S11 |
| E8 | 堆扫活体真实形态 | lldb 活体枚举 **1342 区/4.37GB**,扫 63.2s 全程冻结微信(scan_elapsed_ms=63181);嘻嘻命中全为输入框粘贴缓冲(utf16 UI 副本+utf8 malloc 串),无 filehelper/protobuf 伴生=非序列化管线 | `<勘察>/hunt/hit_20261014-204122_846.txt`;`<勘察>/hunt/window.log`;错题集 S12 |
| E9 | 死锁与解围 | 触发线程 SBProcess.Stop() 与主线程 Continue() 互锁(mutexwait/cvwait);lldb 前端 SIGINT 无效;**debugserver SIGINT 解围**;此后 ALL BREAKPOINTS DISABLED→Detach success=红线序保持 | `<勘察>/hunt/lldb_sample.txt`;`<勘察>/hunt/lldb_live.log`;错题集 S13 |
| E10 | 微信事故 | detach+1s 微信 58622 SIGTRAP 崩(EXC_BREAKPOINT,PC=0x132e51500=VA 0x5e1d500 从未布防点;报告时 PC 字节=合法 ldp→瞬时 brk 补丁残留);WeChatRelaunch 守护自拉起 40379 | `<勘察>/hunt/WeChat-crash-20261014-204620.ips`;错题集 S14 |
| E11 | 离线归因(r1 hit) | lr=0x131941680→VA 0x490d680→caller 0x490d4d0-0x490da78(mars 投递邻域,上游 BL=1);命中帧=thread_overdue_checker 看门狗=**污染帧非发送证据**;aux filehelper=dylib 静态常量+陈旧堆串(weak 成立) | `<勘察>/hunt/attr_hit_20261014-204122_846.txt` |
| E12 | 门 2 判定 | ❌ **未达**:入口函数 VA 未取得、全函数反编译未跑(无可归因目标,诚实缺失非遗漏) | run-sheet-r1.md「门 2 判定:未达」节 |

## 预算账(簿记员如实转记)

勘察 6+1 在案;r1 授权桥自动发 1 条→实际出站 0(sendsUsed=0),授权按 uncertain-never-retry 已消耗不重试。**歧义留主人裁**:零出站授权是否计入 10 帽余量(计入→余 2,P2+P3 需 3 缺 1;仅计出站→余 3 不变);详见 implement.md 预算账节。

## 错题集对账

本轮四错 S11-S14+勘误记录(S10 转述失真)已由执行会话随轮入账 `research/错题集.md`(2026-10-14 晚);簿记员本轮纯文档操作(读+ls+pgrep 只读复核),**无新增错条**。
