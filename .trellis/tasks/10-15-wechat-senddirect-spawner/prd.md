# send_direct 攻坚:spawner/ramp 静态定位+任务伪造入队终验

## Goal

主人裁决(10-15):选攻。基于归档档 10-14-wechat-sendmsg-direct §2.7-§2.11 战报:F_exec 同步直调结构性不成立已终案,唯二活路=①Ghidra xref F_exec→ramp→spawner(若 spawner 吃 ctx+msgctx 可直调——msgctx 伪造术+ctx 活捕术已备)②完整任务伪造+enqueue(缺任务→resume/实参映射,泵分发反编译可静态补全)+§2.11 前提②复核(resume 裸指针 or 包装 thunk)

## Requirements

- 核验 spawner/ramp 与任务入队路线；以 cap19 区分实验及真实 localdb 证据判断可行性。
- 阴性时记录结构性阻塞，保留研究资产，不将其表述为任意正文直发交付，不集成未成功配方。

## Acceptance Criteria

- [x] 已完成下文“验收(AC)”四项研究阶段标准：区分实验、阴性结论、当时窗口健康与资产固化。
- [ ] 任意正文直发产品交付：本路线未实现；不能从 review 状态推断实现。后续社区适配归 uicreate 档，仍缺成功终验。

## Notes

- Keep `prd.md` focused on requirements, constraints, and acceptance criteria.
- Lightweight tasks can remain PRD-only.
- For complex tasks, add `design.md` for technical design and `implement.md` for execution planning before `task.py start`.

## 战报(10-15 攻坚实录)

### R9-R14 静态(Ghidra 复用工程 ~/ghidra-wxui-r2,产物 ~/ghidra-hunt-r9/)

- F_exec(0x83e394)=**vtable 槽 6**;任务对象 0x18B{vptr=0x9c516b8,+8=堆状态块指针,+0x10=小整数状态};slot2=heap clone/slot3=placement 构造器;slot1=带尺寸 delete。
- 入队 API=**FUN_06c4e0a0(payload,ctx)**:new 0x30 节点{vptr=0x9fd2758,[1]=DAT_0849e6a0,[2]=1,[3]=retain,[4]=ctx,[5]=payload}→锁内 push 全局队列 DAT_0a526760→踢泵;同线程内联=FUN_06c4b13c→FUN_06c5e020(执行)→node vtbl[1](delete)。
- 蹦床 FUN_00a6b3d4:RB 树就绪队列遍历,`(*(code*)(*node[5][3])[6])(job, param_2)`——vtable 槽 6 带 msgctx 直调的分发现场。

### R11/R12 实弹(LLDB cap11/cap12,微信 pid 20632 全程存活,发送 2 条落库绿)

- **前提反转(本档最大战果)**:F_exec **不是发送函数,是入站消息处理器**——hit3-8 全是 @chatroom 群消息实流;含「嘻嘻~c11」正文的命中=自家测试消息的**服务端回显**(与发送任务内容不可区分)。cap5 时代「真发必经」实为回显误锚——**五轮直调攻坚全部锚错函数**,亦解释全部撞墙(直调成功也只等于"假装收到一条消息")。
- ctx+8=0x783451e00(堆状态块)/ctx+0x10=0x19;msgctx 布局活体确认(+0x08 peer/+0x48 body/+0x130 display 三 inline23,+0x00=1)。
- 分发链回溯(首次完整):0x6fda37c(嵌套投递)→0xa86510→0xa8087c→0xa81c64→0xa685ec→0xa6b590(蹦床)→F_exec。
- msgctx=主线程栈地址(0x16d8xxxx),同栈位复用。

### R13(在途):入队 API 普查猎真发送入口

- BP 0x6c4e0a0 census 模式:payload vptr_rva 计数+filehelper 邻域旗标——发送窗内带 filehelper 的投递=发送路径任务本尊。

### R13-R17 补录

- R13(POST 普查):BP 0x6c4e0a0 整发送窗**零命中**——发送任务不走该入队口;驱动 GIL 挂死两次(SIGINT 解法定型:Stop() 从脚本线程叫不动运行中进程,二发 SIGINT 走红线收尾)。
- R15(CGI 串):newsendmsg=reqid 237 实锤(内嵌 CGI 配置 XML);但路径串只活在 XML 里,无短定义串可 xref——静态串路死。
- R16(vtable 群落):9 槽任务族 **73 个兄弟类**密集分布在 0x9c50000-0x9c54000,各带独立 exec(互不共享);回显类=0x9c516b8。
- R17(兄弟 exec 抽样):全为薄跳板(真 handler 深层),逐类深挖成本高——转实弹全哨。
- R14/-cap14(73 类 exec 全哨,在途):按钮窗内开火+邻域带 filehelper/正文的非回显类=发送任务类;目标=类身份一次锁定后只深挖一个。

### cap14 全哨战果(73 类 exec 断点×真发 1 条,微信存活)

- **CAND3 金矿**:exec=0x8664d8(vtable **0x9c52cb0**)x1 带本次正文「嘻嘻~c14z」——该类处理 filehelper 消息(回显确认态:发送完成后 12s 才开火,判定为回显/落库层);内层 worker=0x434a2ac,协程机 0xa6dfa4 家族承载。
- **三重奏候选**(发送本体):0x83c750/0x865484/0x866d60 在 t=8.2s 与 t=15.6s(≈按钮窗)各齐射一轮,成对节律=管线事件候选。
- 噪声底:0x8636c0(n=146 恒频)、0x841fe0/0x841e78(24.7s 后)等。
- F_exec(0x9c516b8 类)仅 1 次@24.73s=上轮消息回显,再证与发送无关。
- 回显双层处理:0x9c52cb0 类与 0x9c516b8 类先后各过一遍同一消息。
- R18(在途):三重奏+回显类 handler 静态深挖,定发送本体。

### R18/R19+cap15 终局链(发送 API 锚定)

- cap15(五类定向深扫):**t=16.2s(按钮时刻)类 0x9c52cb0(exec 0x8664d8) x1 即带正文**=发送任务本体(cap14 31.95s 命中才是回显二遍);x0 恒同=服务单例;x1=栈上 msgctx(与 F_exec 消费的同构三槽结构)。
- 回溯上层链(Ghidra R19 反编译):L8(0x4b7182c,全局 svc DAT_0a51f178 vtable+0x30 分发/续体invoke)→L7(0x47174b8,遥测混淆串包装)→L5/L6(0x435ec70/0x435eb50,shared_ptr 续体管道)→L4(0x435e074)→**L3=FUN_0433c5f0(svc, msgctx, continuation, flag)=同步 spawn 函数**:
  - `FUN_003c56c4(dst, param_2)` —— 与 F_exec 消费面同款 0x218 块拷贝(msgctx 直接过手!);
  - `new(0x20){vtable=0x9bf2c18}` 任务对象 + `FUN_00a6de4c(job, msgctx_copy)` 投递;
  - **普通同步函数,无协程体——直调它=以 spawner 身份进场,结构性绕开 §2.9 协程墙**。
- cap16(在途):断 L3 真发捕四参模板(svc/msgctx 0x270/continuation 0x40/flag)→同会话三槽补丁直调→回执验证=全线终验。

### cap16-cap19(直发终验四连)

- **cap16(L3 捕获)**:svc=0x77e72d698(单例)、msgctx 0x270 堆模板、continuation **全零 0x40**、flag=0;needle 门净滤 4 杂项 L3 调用。槽位几何与 F_exec 版不同:**peer@+0x00/body@+0x40/display@+0x120**(各 inline23+末字节裸长度),+0x228 已零。
- **cap17(expr 直调)**:624B 十进制字面量压垮 lldb IR 解释器(unknown error,非 C++ 异常,微信零伤)——直调此路不通,但失败形态与协程墙无关。
- **cap18(原地补丁首验)**:断 L3 入口→needle 命中→**写活 msgctx 正文槽 24B 成功→放行真实调用链**;触发链全绿、微信存活。但库内落行=原始正文、无补丁版回显——首跳补丁未传导到线上内容。
- **cap19(全命中补丁区分实验)**:区分「补错跳(L3 多次命中只补首个)」vs「内容按 msg-id 键在别处」。两跑均未成(首跑 rc=30=osascript 超时——L3 断点在主人活跃群消息流下频繁停机冻 UI,OCR 触发链饿死;重跑在途)。**此实验=重开线的第一发**。
- **工程课**:lldb 批式 Stop() 从脚本线程对运行中进程死锁(SIGTERM 放行+verify3.cmd 字节级复验 L3 修复流程已固化,两轮实拍 INTACT);attach 前必查滞留 lldb。

### 终局判读(本轮交付时的真话)

1. **已破**:架构全图(队列/节点/vtable/蹦床/入队两族)、F_exec=入站处理器(五轮错锚终案)、发送任务类 0x9c52cb0、**L3=FUN_0433c5f0 同步 spawn 函数(四参形态+槽位几何)**、原地补丁写入真实发送链(零伤)。
2. **未破**:任意正文注入——msgctx 字符串槽补丁不改变线上内容,疑正文按 msg-id 从消息库取(msgctx 串=元数据);下一跳=消息**创建**层(UI 按钮→消息对象构造)或补丁实验区分。
3. **重开 SOP**:cap19 区分实验(脚本在 /tmp/wxsend3/r19/,产物模板/驱动/修复链全套)→阳性则深挖 L3 之上 0x435e074/0x4b7182c 链找消息构造入口;阴性则上溯 UI 层。

## 续攻阶段(主人裁决 10-15:继续攻;执行会话=另开,本节=执行蓝本)

### 目标

任意正文直发(不经 UI/OCR):完成 cap19 区分实验 → 按结果走消息创建层或 L3 之上链 → 产出可复用直发配方 → 桥 senddirect.py 落地(若配方成)。

### 资产地图(执行前先验在位)

- **本档 research/cap-assets/**(11 件,已从 /tmp 抢救):cap19 区分实验全套(cap19.py/drive19.py/run19.cmd)、cap18 原地补丁验证版、cap16 L3 捕获器+四参模板实例(hit1.txt:svc/msgctx 0x270/cont 全零/flag=0)、verify3.py+verify3.cmd(L3 字节级复验修复链)、cap17 CALLRESULT(expr 直调 IR 崩实证)、cap12 hit1.txt(msgctx 全量转储实例)。
- **稳定盘上**(非 /tmp 不会丢):~/ghidra-hunt-r9/(九轮静态产物 hunt_r9-r19_out.txt+HuntR*.java 全套 22 件);~/ghidra-wxui-r2/(Ghidra 已分析工程 ASCII 副本,2.1G);~/ghidra_12.1.4_PUBLIC/(引擎);原件 ~/Downloads/微信反编译/ghidra-wxhunt/。
- 运行环境锚:微信 pid 以 `ps aux | grep WeChat` 现查(20632 会漂);装机桥 ~/.myia/plugins/wechat-bridge/bin/wechat-bridge;触发形态 `printf '<needle>' | <桥> send_text filehelper --file -`。

### 执行序(分支树)

**Step 1 = cap19 区分实验(先行,答案决定一切)**
- 复制 research/cap-assets/cap19{.py,.cmd} 等到新 /tmp/wxsend3/r20/ 改 needle(如 嘻嘻~c20w/直发c20w);**改断点策略**:cap19 两跑死于「L3 断点在活跃群流下频繁停机冻 UI→OCR 触发链 osascript 超时」——三选一:①BP 只在触发粘贴阶段后布防(驱动在 send 启动后 ~10s 再 enable);②改断 L4(0x435e074,L3 唯一静态调用者,疑仅发送路径走,入站不吵)并验证槽位等价;③回调内 needle 预筛只读 x1 头 0x48(减少停机时延)。
- 判据:补丁版正文(直发c20w)出现在 localdb `localdb query filehelper --since 1d` → **阳性**;仅原文 → **阴性**。

**Step 2a(阳性→修命中选错)**:L3 同一发送多次命中,逐次补丁全部命中槽位已在 cap19 形态;定位真正传导线上正文的命中序号 → 直接成配方(断 L3+needle 门+全槽补丁+放行),跳到 Step 4。

**Step 2b(阴性→内容键在消息库)**:正文按 msg-id 从消息库取,msgctx 串=元数据。两路:
- 上溯消息**创建**层:CAND3 回溯 #4-#8(0x435e074→0x435ecfc→0x435ebe0→0x4717514→0x4b7182c)再往上=UI 按钮链;Ghidra callers 逐层上溯找「吃明文文本」的构造点(消息对象 new+text 字段写入处),或
- 下钻 msg-id:msgctx 0x270 内找 msg-id 字段 → 断消息库读点(DB 层)看正文来源——优先前者。
- 原地补丁技术(cap18 已证)直接复用于新命中点。

**Step 3 = 配方固化**:命中点+补丁几何定型 → 写入本档(槽位/长度/守卫/失败矩阵);若命中点参数可直调(非协程体)亦可试 expr 直调(cap17 教训:大数组字面量会压垮 IR——分步 malloc+memcpy 表达式规避)。

**Step 4 = 桥落地(配方成才做)**:senddirect.py 新锚模型(schema-4:命中点/槽位/needle 门),capture_call 流程重写(触发→捕获→补丁→放行),版本 0.9.x→0.10.0;**改桥件必重新打包换装+重产锁(just release-plugins --dry-run)**;门禁 pytest tests/wechat-bridge/ 全绿。

### 红线与工程坑(必读)

1. 微信零伤是绝对红线:断点用后即禁再 detach;失败姿势=异常吞+STOP 哨兵+SIGTERM 放行。
2. **lldl 批式 Stop() 从脚本线程对运行中进程死锁**:驱动收尾用回调返回 True 自停;若挂死=对 lldb 进程 SIGTERM(实证有效),之后必跑 verify3(字节级复验 L3/新命中点,dylib 文件字节=真值源)。
3. **attach 前必查滞留**:`ps aux | grep "lldb -p <pid>"`,有则先 TERM。
4. 回调 needle 门滤杂项(L3 也处理入站/其他消息);stray 只记不补。
5. 主人活跃群流=冻 UI 风险源:优先低频断点(L4/创建层),触发窗内布防。
6. Ghidra 跑法:`analyzeHeadless ~/ghidra-wxui-r2 wxui -process "wechat_arm64.dylib" -noanalysis -scriptPath <dir> -postScript <X>.java`(漏 -process=零程序上下文假成功)。
7. 发送预算不限量(主人已裁),但每条 needle 唯一标记(嘻嘻~cNNx 形态)便于 localdb 溯源。

### 验收(AC)

- [x] cap19 区分实验有结论(阳/阴,localdb 证据行入档)——**阴性**(cap20 实证,原文行 ts=1792043470)
- [x] 阴性分支:如实记墙(墙=CGI 编码先于 spawn 命中,四重证据链见下;spawn 补丁路线架构性判死)
- [x] 微信全程存活零崩溃(pid 20632 全程);结束态字节复验 INTACT(L3+BL 双锚点多轮全 PASS);滞留 lldb 清零
- [x] 战报入档(槽位几何/命中序号/失败矩阵见续攻战报);配方未成→桥 0.10.0 不做(Step4 前提不满足)

## 续攻战报(10-15 下午,执行会话实录;微信 pid 20632 全程存活)

### 静态查证 HuntR20/R21(~/ghidra-hunt-r9/)

- **档案勘误①**:「L4=0x435e074」实为 **bl 指令的返回地址**(bl@0x435e070 的下一条);L4 函数真身入口=**FUN_0435df74**。
- **档案勘误②**:「L4 是 L3 唯一静态调用者」不成立——L3(0x433c5f0)有 **3 个代码 caller**:L4 内 bl@0x435e070、兄弟A FUN_043527f4 内 bl@0x4352830、兄弟B FUN_0435ee58 内尾跳 b@0x435ee8c;另 1 处 DATA 引用(0xa59403d)。
- L4 入口无代码 caller、仅 2 处 DATA 引用(0x9e75190/0xa594273)=函数指针调度(vtable/lambda 表)。**入站链(0xa6xxxx 蹦床族)不经 L4**,断 0x435E070 收窄有效但仍非零噪声(群流杂项走该 bl,~1 命中/3s,只读 0x58 门+静默放行可忍)。
- 兄弟A/B 形态:`L3(*(u64*)(host+0x28), host+0x30, host+0x248, *(byte*)(host+0x298)^1)`——**宿主对象内嵌 msgctx@+0x30、svc 指针@+0x28**;但 L4 队列项=独立 0x270 msgctx 块(mc-0x30 无宿主语义,deref 实证+0x28 非 svc)。两条 spawn 路径容器不同、msgctx 几何同构。
- bl 指令字节互证:0x435E070 处 `6079ff97` 解码=bl 0x433c5f0(bl@0x435E070−0x21A80)✓。

### cap20(cap19 区分实验·断点收窄版)→ 阴性定案

- 断 0x435E070+needle 门只读 0x58:触发链全绿(rc=0,14.4s,cgevent_ocr,localdb_receipt=true)——**上两跑冻 UI 死因(断 L3 入口频繁停机)解除**。needle=嘻嘻~c20w。
- 命中 2 次(n=1 发送跳 mc=0x7762c8918/n=2 疑回显),全命中补 +0x40 槽 wrote=24 ✓;hit1 实证 msgctx:peer=filehelper@+0x00、body=needle@+0x40,**mc=堆地址(发送链 msgctx 在堆,与入站栈版同构不同储)**。
- localdb:仅原文「嘻嘻~c20w」(ts=1792043470),无 forge 版 → **阴性:cap18 非补错跳,H2(内容在别处)成立**。

### cap21(长文本形态观察)→ SSO 双形态机制实锤

- 发 43B needle(嘻嘻~c21x+X×32),body 槽变形:`{ptr@+0x40, len@+0x48=0x2b=43(精确吻合), cap@+0x50=0x30|long-bit}`——「inline23」=libc++ std::string SSO,>23B 堆指针化,**正文真体在堆**。
- 事后 deref ptr=已复用无关数据(「...weclaw」随机串)——**堆串=发送期间临时真体,必须命中时刻当场 deref**。脚本 deref 分支判据 bug:0x1000000000 下限(10 hex 位)>堆地址 9 hex 位,错杀。

### cap22(真体改写终验)→ 仍不传导

- 命中时刻当场 deref 真体=needle 明文 ✓,原位改写 43B forge(嘻嘻~直发c22y+Y×26,读回字节级验证 ✓),触发链 rc=0 → localdb **仍只落原文**。

### cap23-25(read-watchpoint 抓正文消费者)→ 双副本架构定案

- 工程坑:①`SBTarget.WatchAddress` 需第 5 参 SBError;②**SBWatchpoint 无 SetScriptCallbackFunction**(与 breakpoint 不同)——改「驱动守望循环轮询进程 stop 态+采栈+Continue」绕过;③驱动收尾 GIL 挂死形态复现三轮,SIGTERM 兜底 1s 内干净退出(六轮实证)。
- cap25 三断点齐挂(L4 bl+兄弟A bl+兄弟B b):bp 记录实证**多路径负载**——发送跳走 L4(peer 干净),**回显跳走兄弟A/B(peer 槽带 \x83\x07 尾巴)**;cap24 轮 A miss 之谜=发送跳偶走兄弟被「干净 peer 门」滤掉。
- **watch 栈判读(628 命中)**:free(P) 前(A 发送后 0~2.2s)P 的**唯一读者=L3 内 FUN_003c56c4 参数拷贝链**(memmove×9,tid=1 主线程 RunLoop Timer→调度→L8 svc 链);t+2.2s `_xzm_free` 从 L4 续体(rva=0x435ed90)释放 P;之后 600+ 命中全为 allocator 复用噪声(含入站回显链 0x6fda778 帧读复用块)。**CGI/序列化层从未读 P**。

### cap26(正本猎杀)→ 墙定案

- spawn 命中时刻扫 P±32MB 堆窗:找到 **5 处 needle 副本**(P 邻域 ±32KB),全部原位改写 forge+读回验证 ✓,触发 rc=0 → localdb **仍只落原文**(ts=1792046485)。
- **终局判读:发送管线=双副本架构**——按钮时刻创建层先造「正本」(CGI 编码消费后即弃/变换),spawn 的 msgctx 及其真体=纯任务副本;**CGI 编码完成于 spawn 断点命中之前**,spawn 时刻堆中已无可传导的 UTF-8 正本。spawn 补丁路线(槽/真体/全命中/多路径/全副本猎杀)四重证据判死。

### 失败矩阵(本轮 needle 清单,localdb 均有原文行)

| 实验 | 断点 | 改写对象 | 结果 |
|---|---|---|---|
| cap20 | 0x435E070 | 全命中 SSO 短槽 | 原文落库 |
| cap22 | 0x435E070 | 命中时刻真体 43B 原位 | 原文落库 |
| cap26 | 三断点 | P±32MB 全部 5 副本 | 原文落库 |

### 下轮方向(若续攻,超出本档 spawn 主题需另立)

1. **UI 创建层窗口**:按钮 handler 同步栈(cgevent 点击→输入框文本对象→消息构造)。spawn 在 Timer 异步链上,须改断 UI 事件层——无符号,需从 RunLoop/按钮响应链或「输入框取文本」API 入手。
2. **CGI 编码窗口**:newsendmsg(reqid 237)请求体构造点;正本编码后即弃,须抓编码瞬间(memcpy 内容门)。
3. watchpoint 技术(轮询采栈版)与堆窗扫描猎杀可直接复用为新窗口的取证器。

### 工程课(本轮新增)

- lldb watchpoint 无脚本回调→驱动轮询 stop 态+采栈+Continue 可稳定工作(628 栈样本实证)。
- read-watch 事后 deref 必复用失真;**命中时刻当场 deref 是唯一真值**。
- 门设计:干净 peer 门=发送跳;带尾 peer(\x83\x07)=回显跳;多路径负载下断点要三 caller 齐挂。
- cap-assets-r20-r26/(44 件)已固化入档 research/;HuntR20/21.java+输出在 ~/ghidra-hunt-r9/。
