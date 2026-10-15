# send_direct 攻坚:spawner/ramp 静态定位+任务伪造入队终验

## Goal

主人裁决(10-15):选攻。基于归档档 10-14-wechat-sendmsg-direct §2.7-§2.11 战报:F_exec 同步直调结构性不成立已终案,唯二活路=①Ghidra xref F_exec→ramp→spawner(若 spawner 吃 ctx+msgctx 可直调——msgctx 伪造术+ctx 活捕术已备)②完整任务伪造+enqueue(缺任务→resume/实参映射,泵分发反编译可静态补全)+§2.11 前提②复核(resume 裸指针 or 包装 thunk)

## Requirements

- TBD

## Acceptance Criteria

- [ ] TBD

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
