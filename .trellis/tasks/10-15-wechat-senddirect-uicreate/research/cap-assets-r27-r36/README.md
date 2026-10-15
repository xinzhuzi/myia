# cap-assets-r27-r37 战报(10-15 晚,执行会话实录)

运行环境:微信 pid 91292(16:31 重启后的新实例;前一实例 20632 于前序会话 cap33 卡挂后 16:31 换新)。桥 `~/.myia/plugins/wechat-bridge/bin/wechat-bridge`,触发形态 `printf '<needle>' | <桥> send_text filehelper --file -`,全部发送 channel=cgevent_ocr、readback=clipboard_copy。二进制身份门:每窗 attach 后先读双锚点(L3 rva 0x433C5F0 期望 8B `fc6fbca9f65701a9` + bl@0x435E070 期望 4B `6079ff97`),不符拒装断点;每窗收尾后复验,历次 VERIFY_PASS。

## 会话脉络(两段)

### 前序会话(15:05-16:23,未及归档,本会话抢救复盘)

- **cap27(粘贴断点,AC-1)**:断 `-[NSPasteboard dataForType:]`/`stringForType:`(系统符号)。needle 门过 4 次,命中 tid=1 主线程,回溯 16 帧:rva 0x70AC5E8(fn ___lldb_unnamed_symbol384597)← 0x70ABDD4 ← 0x6FD0750 ← 0x6FD2068 ← 0x1C909D4 ← …(Qt 式粘贴处理链)。粘贴时序远早于 spawn(触发后 ~6-10s vs 按钮+0-1s),群消息流下天然安静——**文本进入点锚定**。
- **cap28/29/30/31(粘贴转换链,AC-2 前半)**:
  - 0x70AC5E4 bl stringForType → 0x70AC5E8 返回,x0=NSString(needle 以 **UTF-16LE 内联**在对象 +0x18);
  - 0x70AC5F0 bl 0x382402(NSString→微信串转换)→ 0x70AC5F4 返回,**x19=输出栈槽**(0x16d8xxxx)→ *x19=S(微信串结构 {u32=1,u32=len,0x14,…,0x18,…},needle 内联于 S+0x18 或 S+0x18 指针所指堆缓冲 Q);
  - cap30 补证插入侧:x8=写入目的地(同栈槽家族)。
  - watch 尝试(读/写 watch Q、x8 结构)四跑均只产生 value 抖动,**读者栈未捕获**(驱动层缺陷,非结论)。
- **cap32(按钮窗管线帧正扫,GOLD)**:断三重奏(0x83C750/0x865484/0x866D60)+CAND3 worker 0x434a2ac,needle 门扫 x0-x3。3 GOLD 全在 0x434a2ac:needle(UTF-16 栈结构体 0x16d85f260/0x16d85f840)在 x0/x1;栈=0xa6dfa4(协程机)← 0x433c6f0(协程入口)← 0x435e074(L4)← 0x435ecfc ← 0x435ebe0 ← 0x4717514 ← 0x4b71874 ← RunLoop Source0。
- **cap33(Source0 回调身份爬升)**:驱动 KeyError('P')→ import 崩 → lldb 挂死附加 → 前实例 20632 于 16:31 消亡换新。**从未运行**。

### 本会话(21:11-21:55,7 窗,每窗 sigle-attach+收尾复验)

- **cap34(0x434a2ac 补丁终验·首跑)**:锚点预验 PASS 后四断点齐挂(含三重奏),needle 门扫 x0-x3(v/v+0x18/v+0x40)。触发 rc=0(localdb_receipt=true)但**零门过**(needle 不在 x0-x3 浅层);驱动 Stop() 死锁(已知形态)→ SIGTERM 收尾,复验 PASS。localdb 仅原文(未尝试补丁=无定论)。
- **cap34b(诊断跑)**:门扩到 x0-x28 全寄存器+SP±0x600,每命中留 hits.log。37 命中全在 0x434a2ac(三重奏零命中),**仍零 needle**;干净 detach。→ 复盘 cap32 GOLD 的 needle 结构体距 SP 可达 ~0x1260,34b 栈窗不足。
- **cap34c(出站签名门补丁跑)**:栈窗 0x4000+回溯签名门(帧含 0x435e074/0x433c6f0 才补;防回显侧假阳性)。36 命中,**1 补丁**:n=32 t=按钮+~19s,reg=x24(callee-saved——34/34b 漏扫根源),form=u8,addr=0x93abe09c8(堆),span=43B 写入+读回验证 ✓;栈含完整出站链(此跑经 **RunLoop Timer** 派发,非 Source0)。localdb:**仅原文**(ts=1792070861,先于补丁时刻 19.3s)。→ **该命中=回显二遍**(DB 行落定后的延迟处理),补之不及线;出站首过(按钮时刻)在 0x434a2ac 入口全寄存器+宽栈窗均无正文。
- **cap35(转换族全生命周期正扫)**:断 0x382402(NSString→微信串转换,入口 x0=NSString)+0x70AC5E8/0x70AC5F4。触发 rc=0(2 尝试)全生命周期内 needle 仅 2 GOLD:粘贴瞬间的 pbret+convret(均为 UTF-16)。**回读复制/聚焦哨兵复制/Return 构造/回显插入均不经转换族**——构造直接读 composer 内部存储(微信串形态),不走 NSString 往返。
- **cap36(follow-the-copy watch)**:convret 门过(Q=0x942e026d8,S+0x18 内联);驱动 steward(+2.5s Stop→Q±32MB 扫→挂 watch→Continue)与主收尾线程交叉持 SB API → 死锁,微信 UI 冻结 ~6 分钟,SIGTERM 恢复,复验 PASS。**读者链仍缺**(两次独立实现均在驱动层死锁/空采)。
- **cap37(剪贴板写侧锚定)**:断 `setString:forType:`/`setData:forType:`/`writeObjects:`/`CFPasteboardSetData`(全解析 1 loc,窗内仅 4 次匿名命中)。触发 rc=0 且 readback=clipboard_copy(微信内 Cmd+A/Cmd+C 实跑、pbpaste 取回正文)——**四写 API 零 needle 门过**:copy-out 经风味转义(RTF 类)或私有路径,不暴露原文字节。干净 detach。

## 墙(最终判读,交主人裁决)

**构造/CGI 编码点位于 Return 键同步窗口内,直接读取 composer 内部微信串存储;五族锚点无一能在此窗口暴露正文,桥自身断言结构性地封死预 Return 补丁路。**

证据链:

1. spawn 窗补丁全线不传导(承前档 cap20/22/26:槽/真体/全命中/三 caller 路径/P±32MB 全 5 副本)→ CGI 编码先于 spawn。
2. 协程 worker(0x434a2ac)出站首过入口:全 GPR(x0-x28,+0x140 邻域)+SP±0x4000 栈窗,UTF-8/UTF-16 双形零命中(cap34/34b/34c 三跑)→ 构造输入不在该帧可见面。
3. 唯一 needle 可见的异步命中=回显二遍(+19s),补之 localdb 仍原文(cap34c)→ 线内容在一切可补点之前已定。
4. NSString 转换族(0x382402)全生命周期仅粘贴瞬间 2 门过(cap35)→ 构造不走 NSString 往返,转换族不可见构造。
5. 桥 sendui 源码级断言链:回读(Cmd+A/Cmd+C==body)+发送前聚焦断言(哨兵读==body)→ **Return 前任何 composer 存储补丁=断言失败=不发**(_assert_focused「读到异值=真焦点问题,不再等」)。
6. 剪贴板写侧四 API 零 needle(cap37)→ copy-out 亦经转义/私有路径,该侧不可锚。
7. 剩余未测完路线:fine-grained follow-the-copy watch(paste+2.5s 堆扫找持久副本→read watch→Return 时刻读者栈=构造点 PC→该 PC 处补丁)。两次实现(cap28-31、cap36)均死于驱动层(死锁/空采),**概念本身未被证伪**——复用 r23 已验证的轮询采栈骨架 + 单线程化驱动是重开姿势。

## 失败矩阵(本会话 needle 清单,localdb 均有原文行)

| 实验 | 断点 | 改写对象 | 结果 |
|---|---|---|---|
| cap34 | 0x434a2ac+三重奏 | (x0-x3 浅扫零门过) | 未及补丁;原文落库 |
| cap34b | 同上 | (x0-x28+SP±0x600 零门过) | 未及补丁;原文落库 |
| cap34c | 同上+栈窗0x4000+出站签名门 | x24 所指堆副本 43B(回显二遍) | 原文落库 |
| cap35 | 0x382402+粘贴两点 | 无(纯观测) | 仅粘贴 2 GOLD |
| cap36 | 0x70AC5F4 | 无(观测,驱动死锁) | 粘贴锚 S/Q 入档 |
| cap37 | 剪贴板写四符号 | 无(纯观测) | 零 needle |

## 工程课(本会话新增)

- SBBreakpoint 无 SetName(本机 lldb)——bp 身份用 id→sym 映射。
- 驱动多线程交叉持 SB API(一线程 ReadMemory 扫描中、另一线程 breakpoint_iter/Detach)= 新死锁形态;steward/收尾必须单线程化或全走 STOP 哨兵回调自禁(cap34b/c/35/37 的回调自禁+守护 detach 形态干净收尾五连)。
- cap32 GOLD 的 needle 在 callee-saved(x24 等)——门扫描必须 x0-x28 全 GPR,不止参寄存器。
- 回显二遍复用出站签名链(0x435e074/0x433c6f0 帧)——**签名门不能区分出站/回显,只有时间轴能**(DB 行 ts 前后);本会话以 ts 对齐判死 cap34c 补丁命中为回显。
- 每窗锚点预验(attach 后先读双锚点字节,不符拒装)应成为 SOP——新实例/二进制漂移的 fail-safe。

## 留证补齐(复审后,2026-10-15 晚)

- **r36 抢救补全**:mmst1-3.txt(MMStartTask@0x597eda0 三栈,mgr/task 指针,cmdid_0x20000095_in_task=False)+ run36 变体 cap35/drive35(needles c56s/c57s)已并入本目录(变体以 -run36-variant 后缀防撞)。
- **DB 行 ts 独立复核(免附加只读)**:`localdb query filehelper --since 2d` 实测命中 ts=1792070861(cap34c 原文行)——README §cap34c 的「DB 行先于补丁 19.3s」判读锚点现已有库内实证(复审 Note B 闭合)。
- 各窗 VERIFY_PASS 输出未随窗归档(README 为唯一载体);复审已做磁盘态零附加复验:wechat.dylib arm64 slice fat-offset 184614912 处 rva 0x433C5F0→fc6fbca9f65701a9、0x435E070→6079ff97 双锚点字节相符。
