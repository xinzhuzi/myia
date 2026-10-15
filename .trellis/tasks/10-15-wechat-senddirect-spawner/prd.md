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
