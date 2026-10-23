# 状态3阶段、准确虚表目标与后续通知（离线）

账号安全停止约束保持：没有附加、调用、发送或操作微信界面；没有产品/安装件/实际版本JSON改动。A7未完成，本文不构成可执行发送配方。

## 本轮新增的确证

1. `text-contract-pass184/native-fn-31ce06c.c:251`开始的分支仅在先前结果两个32位字为零、context flag低位为1、`0x318d680`找到非空handler后，将状态设为3并调用`0x30d4354`。原始位置`0x31ce89c`、`0x31ce8a0`、`0x31ce8cc`分别为常量3、状态setter和阶段调用。
2. `text-contract-pass196/native-fn-30d4354.asm`入口保存x0为handler、x1为context shared pair地址、隐藏x8为结果区；Ghidra显示的三个普通参数不能照抄。输入虚槽+0x20返回1时，还读取input+0xd8单字节：等于1调用handler+0x88，否则调用+0x80；返回2/3调用+0xa0。该分支的0xd8是输入成员偏移，不能与handler的producer虚槽+0xd8混为一谈。
3. 冻结虚表`0x9de7f68`经实际dyld fixup链独立解码：+0x78=`0x30bcd9c`，+0x80=`0x30d82d8`，+0x88=`0x303fdf0`，+0xa0=`0x30d8cac`，+0xd8=`0x30bda14`。此前pass195保留的`0x30d7958`不是此表+0x78的目标，不能用于解释该表的准备阶段。
4. `text-contract-pass197/native-fn-303fdf0.c`完整小函数仅复制/保留context shared pair，转调同一handler的+0x80，再释放临时引用。原始指令证明进入虚调用前未改写x8。已知表的+0x80目标`0x30d82d8`仅条件日志并用`0x304f1cc`构造0/0结果。因此状态3阶段仍未证明进入producer，也不能从0/0结果推出发送成功。
5. 状态3函数随后对record通知：kind4调用`0x30d05d0(handler,0x800000000,record)`，该函数进一步调用`0x30d0a14(handler+0x90,flags,record)`；其他kind调用`0x30cfe58(handler,record)`，进一步到`0x30d00d0(handler+0x18,record)`。两个后继通知容器的实际目标尚未追踪，不能断言整条链无producer调用。

## 覆盖与局限

新增pass193～199保留准备、批处理、状态3、重定向及通知函数。对大型`0x3189b24`只读了handler选择/准备、批处理调用及record复制片段，不为整函数提供语义结论；其余未解释分支保持未知。

`Library/ai/verify_wechat_state_three_20261016.py`检查13份导出共8891条指令与同一冻结ARM64薄片一致，核验39个关键位置、5个虚表槽及小重定向函数的x8保留。Ruff通过。报告为`newsendmsg-state-three-verification.json`，合同为`newsendmsg-state-three-contract.json`。字节一致仅证明导出来源，不证明大型函数语义全部正确，更不证明账号或运行时状态。

后续离线缺口：精确追踪`0x30d00d0`/`0x30d0a14`通知容器、证明实际选中handler的注册身份及到`0x30bda14`的连接，再补正文输入方向、线程/config与最终引用排空。真正发送和独立回执仍缺，账号安全停止约束优先，不再安排活体观察窗口。
