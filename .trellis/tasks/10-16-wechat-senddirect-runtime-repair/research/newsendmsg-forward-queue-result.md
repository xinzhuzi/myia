# 从发送context出发的队列与调度链

只读冻结4.1.15(270135)ARM64及留存Ghidra工程。没有运行、附加或操作微信，没有改产品/实际版本JSON/安装件；账号安全停止约束保持，A7未完成。

## 确认的正向片段

- `0x317df64`真实寄存器合同为x0服务、x1输入shared handle指针、x2构造器第三参数（构造器取低字节）、隐藏x8结果区。它分配0xf8字节容器，context位于+0x18；调用`0x30f1c5c`单指令thunk，原始分支目标独立核验为`0x30ef9e0`。
- context构造器保存输入shared pair至+8/+0x10，生成record pair保存至+0x18/+0x20，并将input+0x90字符串复制到context+0x38。这个字符串作为队列key使用，尚不据此定名为收件人。
- 入口调用`0x3181628`将shared context存入service+0xb20所指存储的+0x60容器，再调用`0x3182084(service,context+0x38)`推进处理，最后经`0x3189980`消费context+0x70处的shared结果。结果消费中调用`0x66856fc`和`0x312bae8`，未完整解释其等待语义，不能把入口当作随处安全调用。
- `0x3182084`按key取队列并读取context+0xb4数值状态，经`0x31ce06c`准备，随后`0x31cae30`在当前队列按context指针查找、移动剩余shared pair并缩短末尾。满足结果及flag条件时，将状态设4，放入同存储+0x88容器，再构建异步回调。状态getter/setter`0x30f320c/0x30f3214`与flag getter`0x30f321c`直接使用+b4/+b0，不推定枚举业务名称。

## 回调捕获与后续阶段

正文functor虚表`0x9def270`在+8/+0x10捕获context shared pair，+0x18保存服务，+0x20保存key字符串；+0x30 invoke槽独立dyld解码为`0x322274c`。该invoke先再次推进`0x3182084`，再以捕获context调用`0x31d15fc`，随后处理结果并调用`0x31cba64`，不能把再次推进本身视为重复发送。

另一functor虚表`0x9def2f0`的invoke槽为`0x3222ea4`，它又创建捕获回调并提交`0x453cce8`。这说明完成路径还有下一层，未证明末尾回调排空或模块卸载屏障。

作业wrapper`0x453d344`原始ABI是x0/group wrapper、x1/config、x2/body、x3/finished、x4/option，隐藏x8返回。它从wrapper+0x10取得核心，再调用`0x453c7ac`；Ghidra把返回区当普通参数的伪声明不能照搬。具体group身份、线程和config仍需独立证明。

## handler选择与零返回的边界

`0x31d15fc -> 0x318d680`从context输入对象的三个虚槽读取低类型/高类型/另一种类值，再经`0x319a6a8`查询service存储+0x28中的映射、按名称调用`0x3217130`取得handler。实际选择对象的注册和身份未完全连通。

后续`0x30d58e0`在种类1分支调用handler虚槽+0x90。对此前已识别表`0x9de7f68`，+0x90的精确槽地址`0x9de7ff8`解码为`0x30d8538`：该方法只日志并以0/0构造结果，没有调用已识别发送producer。producer`0x30bda14`在同表+0xd8，是不同阶段/槽；不能拿+0x90的零结果声称发送完成。本结论不推断整个外层链从未发送；较早准备阶段`0x31cf3a4`及producer派发还未完整跟通。

## 验证与下一缺口

新验证器匹配全部本轮函数导出及3份既有上下文导出共9450条指令，54关键位置、4个dyld链槽及constructor thunk核验通过，Ruff通过。完整导出字节通过不代表所有大型函数业务分支均已解释；语义结论严格限于上述定点片段。详见`newsendmsg-forward-queue-contract.json`与`newsendmsg-forward-queue-verification.json`，脚本`Library/ai/verify_wechat_forward_queue_20261016.py`。

下一缺口为准备阶段的handler注册/选择、到+0xd8 producer的精确派发，以及业务输入方向、实际线程/config/末尾排空；完整适配与独立真实回执仍缺。产品保持拒绝，不恢复活体操作。
