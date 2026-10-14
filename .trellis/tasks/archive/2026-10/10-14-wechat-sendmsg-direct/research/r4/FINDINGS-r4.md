# r4 钉入轮战果(10-15 晨,P-0 已裁后;桥真发触发,hit2 全证)

## 定案事实(hit2.txt 49 帧全链)

1. **全链路首次完整捕获**:AppKit 事件循环(UI 回车)→ #19..#12 业务层(0x69d-0x709 段)→ #11..#7 协程库(0xa6-0xa8 段)→ #6 FUN_0083e394(协程体)→ #3..#1 队列层 → #0 enqueue_b(0xa5ed0)。cmdid=0x30d40(200000)。
2. **明文对定位(金证)**:栈 0x16d7678d8 起 = 两条 inline23_rawlen 记录并肩——`filehelper`(raw_len=0x0a)@+0 与 `嘻嘻~r4b`(raw_len=0x0a)@+0x48,与设计 F3 的 24B 形态**逐字节吻合**;正文在栈上三副本(局部块/msgctx/任务结构)。
3. **RPC 执行体=FUN_0083e394(协程体)**:双 0x230 块 bzero(=msgctx 形态);`FUN_003c56c4(auStack_640, param_2+8)` 拷串;`FUN_05e1d050(&local_1b0, 2, ...)`=**sendmsg RPC(cmdid=2)**;`while (uVar6 != 0x17)`=inline23 容量拷贝循环。参数:(param_1=ctx 指针, param_2=任务结构指针,串源=param_2+8)。
4. **enqueue 两族勘误(V1 修正)**:hit1(enqueue_a,cmdid=100000)与 hit2(enqueue_b,cmdid=200000)队列对象不同;svc=x0-0x1c0 假设仅对 a 族近似成立(hit1 vptr 合理),对 b 族不成立(V1 形不符,V3 区含「助手」文本)。**设计 §2 的单 svc 假设须按族分立修订**。

## 下轮(r4 续)剩余

- F_send(造任务的上层)尚未钉死:#12-#17 已反编译但均不直调建串函数(链经中间层);用 hit2 全帧 BT 做离线 calleewalk(Ghidra,无需再发消息)即可闭合;
- send-direct-anchors.json 落表(send_entry/ABI/by_value/buffer_mode)待 F_send 定案;
- svc_vtable_off/svc_invariants 按 a/b 族分立重取。

## 工程账

- 触发成本:4 条 filehelper 真发(嘻嘻/嘻嘻!/嘻嘻~r4b/嘻嘻~r4c,P-0 (c) 不限量后合规);微信 pid 40379 全程存活零伤;lldb 用后即 kill 零残留。
- 脚本坑入册:cap4 f-string 中文占位符=NameError;LLDB `command script import` 需 `__lldb_init_module` 钩子否则 install 不跑;指针追扫必须全窗(hit1 教训:needle 深至 +0xf50)。

## cap5 终捕(同晨):直调配方的最后拼图

- **F_exec = FUN_0083e394(param_1=ctx, param_2=msgctx)**:完整执行体断点直捕;param_2=0x16d768288(栈)自身即明文载体。
- **param_2(msgctx)布局定案(可伪造纯数据)**:+0x00 flag=1;**+0x08 对端 inline23**(filehelper,raw_len=0x0a);+0x40 堆指针(0x1f14a9800,语义待解);**+0x48 正文 inline23**(嘻嘻~r4c,0x0a);**+0x130 显示名 inline23**(文件传输助手,0x12);其余大段零——三串槽与 F3 完全对齐。
- **param_1(ctx)=0x8a3913c18(堆)**:首 qword=vtable(slide+0x9c516b8),+8=堆指针链;须活对象(全局槽定位=下一步离线活:扫 data 段引用该 vtable 的全局槽)。
- **直调配方形态(免 spawner 链)**:取活 param_1(全局槽/观测捕获)+伪造 param_2(三 inline23 槽)+call F_exec——比原设计(找 F_send 造任务)更短更可控。
- BT 证实 #6-#13 为协程缝合的 spawner 原栈(0x7097be8→…→0x6fda37c→spawn),无需再追。

## r6/r7 离线续(同晨):ctx 来源结论

- spawner 三件(06fda37c/06fdf3a0/06fd4ae8)与外层四件(07097be8/06ffd1e0/06fbd634/069d32a8)全反编译:DAT 引用全是哈希桶/特性旗,**ctx(param_1)全程参数传递,无全局槽直载**。
- 活探实扫(__DATA/__DATA_CONST 各 4MB,已知地址+VT 双跳两法):**零命中**——ctx 为堆链所有(服务管理器对象持有),不落静态槽。
- **务实路线定案(下轮实施)**:ctx 会话内缓存——同一微信进程内 ctx 长寿;直发首条=桥 OCR 触发+F_exec 断点捕 x0(成本 2 发),缓存 ctx;后续直发=纯 LLDB 直调(1 发/条)。自动化排程场景下首条成本可忽略。anchors 表 service_ptr_mode="observe_bp" 形态(senddirect 已留该枚举位)。
