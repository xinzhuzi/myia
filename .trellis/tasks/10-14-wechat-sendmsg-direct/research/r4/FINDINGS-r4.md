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
