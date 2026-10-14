# evidence(10-14 晚轮:Phase 0 工具整备 + Phase 1 r1 活体猎捕;阶段 2/3 战果注记)

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

勘察 6+1 在案;r1 授权桥自动发 1 条→实际出站 0(sendsUsed=0),授权按 uncertain-never-retry 已消耗不重试。**歧义终裁待主人**:零出站授权是否计入 10 帽余量(计入→余 2,P2+P3 需 3 缺 1;仅计出站→余 3 不变);**任何下轮发送前必先就此问裁**;三档口径(design.md 预算账/implement.md 预算账/本节)已按勘误轮统一。

**〔10-15 凌晨更新,依 design-阶段3.md §4 P-0(F5 账本实锤;簿记员转记)〕**阶段 3 动态轮 r1/r2/r3 三发全部经**桥自动发送**触发(round.sh 触发行实证,非主人手发零耗形态),实际出站 3。现行账本=勘察 6+r1 零出站 1+动态轮 3=**9~10/10,余 0~1**;而 P-2 白名单双发矩阵需 2 条。P-0 主人裁决门(先于一切发送):(a) r1 零出站不计→余 1,再批 +1;(b) 直接批 +2;(c) 上调帽;**任何验证发送前未得裁决=不发**。

## 错题集对账

本轮四错 S11-S14+勘误记录(S10 转述失真)已由执行会话随轮入账 `research/错题集.md`(2026-10-14 晚);簿记员本轮纯文档操作(读+ls+pgrep 只读复核),**无新增错条**。

**〔10-15 凌晨对账更新(簿记员)〕**阶段 3 双路探索轮两笔挂账:①动态轮 r2 判别门以 filehelper 为门过宽、旧消息早命中浪费一发(round-reports 原文已标「方法论坑(入册)」)=**新错待入册(S16 候选)**;②错题主表 S11-S14 存在两波双录(执行会话波+勘误轮波,同四事故各入一遍)待合并。**错题集.md 正被并行会话活跃写入(S15 rmtree 事故条目 02:09 落盘在案)——簿记员按红线让道不碰该文件,上两笔挂账待其并入或下轮簿记补。**

## 阶段 2 战果并档注记(10-14 晚勘误轮补记)

阶段 2 猎捕战果(活入口=FUN_043f88e4 实证;归档 031ab38c/043f88e4 角色互换勘误)见 `research/FINDINGS-阶段2.md`。本勘误轮据此对齐四件套:design.md 架构定论与 Step 2.1 布点勘误、prd.md AC3 回执断言撤销(误诊归档在案)、task.json 旧前提撤销、预算口径三档统一(终裁待主人)。本轮纯文档操作:零代码、零微信、零 attach、零发送。

## 阶段 3 双路探索轮(10-14 深夜执行;簿记员 10-15 凌晨转记)

> 背景如实注:本轮产物曾因 **S15 仓库 rmtree 事故**损毁,任务档与 research 件系会话读档逐字重写恢复(远端 HEAD 27e3b255 整仓 clone 回填;/tmp/wxsend3 原件回收,hunt-r3-dynargs md5 对账一致);不可恢复损失清单见错题集 S15(已上报主人)。簿记员按落盘产物+轮报告原文核验转记,零微信零 attach 零发送。

| # | 项 | 结果 | 证据(路径) |
|---|---|---|---|
| E13 | 静态轮(零发送,全程只读):5 次 Ghidra headless(`-process wechat_arm64.dylib -noanalysis` 复用 wxui.gpr,分钟级)+2 个 python 离线解码器 | ✅ 00a05ea0 静态墙定案(全可执行内存字节级扫 ADRP/ADR/LDR-lit 零代码装载,唯一 8B 字面量在 __const 0x9c61f58=混淆清单表普通成员);XOR 文件名解码 1212 路径(**00a05ea0→chat_voice_input_viewmodel.cc:463=阶段2「task_service 族」定性勘误**;043f88e4→task_service.cc;031ab38c→message_manager.cc;045937f8→add_msg_cmd_handler.cc 收信侧);hit4 x1=0x186a0=cmdid 100000(LoopHandleTasks 泵任务号)定案;CGI 注册表直读 newsendmsg reqid=237;UI=Qt C++ 无 ObjC 发送选择器(仅 MessageService 串×2 零 selref);入队 API 三件套签名定案(FUN_00033c40/00033c68/000a6060+000a5ed0) | `research/round-reports-阶段3合流输入.md` 静态轮 JSON(逐字落档);产物 8 件=`/Users/zhengbingjin/Downloads/微信反编译/sendmsg-hunt/`(coro_spawn_hunt{,2,3,4,5}.c、mass_paths_decoded.txt、mass_decode.py、xor_decode.py) |
| E14 | 动态轮三轮(r1 21:42:08/r2 21:47:16/r3 21:49:28 CST,10-14):round.sh 单轮协议=attach→ARMED→桥真发 filehelper→判别门 DONE→SIGINT 收兵→detach;slide=0x12b0e8000,pid 40379 主线程 | ✅ 入口 slide+0x43f88e4 三轮寄存器形态全同;x0=RPC 任务/闭包对象(**x0+0x8=043f88e4 自指=「函数指针入协程故零 BL 调用者」机理坐实**);(user,content) 明文在指针一跳外 msgctx 堆块(r1=x0+0x2e0→0x89ae3e328;r3=x0+0x3a0/+0x520 双引用同块,引用槽逐轮漂移→通用走法=扫 x0 前 ~0x600 qword 指针+512B 探针找 {char[23];u8len} 记录):块+0x130=自 wxid「wxid_oc2yhey1xkpw22」(len 0x13)/+0x148=对端「filehelper」(len 0x0a)/+0x160/+0x178 成对重复/+0x1d8=正文 UTF-8 明文内联(r1「嘻嘻」e5 98 bb×2、r3「嘻嘻嘻嘻」×4,跨轮逐字节同构;串形态=23 容量+末字节裸长度,非 libc++ SSO);三轮全部转储零 protobuf 框架字节=**序列化前 C++ 对象图实证**;x1=0x186a0 恒定标量;x3=0xfffffc088 可读无消息数据;x4 读取失败(如实);r3 收兵 DONE:send_hits=10/subm_hits=328/lldb_exit=143(SIGTERM);0x490fb20 三轮 300+ 杂散命中无一载 filehelper/正文(传输边界旁证,S2 复证);上层链 lr=slide+0x106108(+0x106104 bl +0x105fa8 解引用槽位尾跳),38 帧见 hit_send7_r1.txt | `research/hunt-r3-dynargs/`(ARMED/DONE/LLDB_EXIT、hit_send7_r1.txt、hit_send0_r2_earlystage.txt、hit_send9_r3.txt、cap2.py、round.sh、dumps_r1/dumps_r3、msgctx_{r1_ptr02e0,r3_ptr03a0}.bin、needle.bin);`research/round-reports-阶段3合流输入.md` 动态轮 argsMap JSON(sendsUsed=3) |
| E15 | 轮报告原文落档(双路交付此前仅存会话文本,无产物可复核) | ✅ 静态 C1-C6+动态 argsMap 两 JSON 逐字落盘;**红旗:「q=服务对象+0x1c0」仅存于 C1 原文,sendmsg-hunt/*.c 与本档 research/ 一切反编译/转储产物无独立出处——r4 钉入轮必先形验证(design-阶段3.md §2.4)才准入锚定表** | `research/round-reports-阶段3合流输入.md` 档首注意事项 |
| E16 | 预算实锤(F5) | ⚠️ 触发形态=桥自动发非主人手发(见上预算账 10-15 更新:账本 9~10/10 余 0~1,P-2 需 2);**任何验证发送前未得 P-0 裁决=不发** | round.sh 触发行;design-阶段3.md §4 P-0 |
| E17 | 簿记员本轮(10-15 凌晨) | 纯文档:读+ls+lsof+date+pgrep 只读核验;改本档+prd.md(AC3 勘误+预算括注)+task.json(旧前提描述撤销,状态指针未动)+design-阶段3.md P-2 引注勘误+FINDINGS-阶段2.md 勘误括注;**错题集.md 让道未碰**(并行会话活跃写入)。零代码、零微信操作、零 attach、零发送;未提交插件源码改动(senddirect*.py 等)非簿记员职责面,未核验未记档 | 本节+git diff |
