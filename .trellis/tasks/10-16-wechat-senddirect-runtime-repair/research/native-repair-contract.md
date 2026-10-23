# 4.1.15 原生缓冲区修复与剩余条件

已落实的产品修复是被动检查和执行拒绝门，两个本机入口都装入0.9.1。
本文件下述原生模块只在research中运行假内存测试，不能当作已打通的发送器。

## 二进制与导出来源

留存arm64文件、安装包Resources切片和既有Ghidra工程输入SHA256均为
`6a5bd0cbb39ad3092c15e9debda2db4969eedf1b58caad244d88033a996833a7`。
已有REA结构证据为 `ev_109315ba49cf6386a2abad6c8d1d5dfe6f3829412d39a6a7909ceafb98cebf65`。
本轮Ghidra只复用既有工程，-process/-noanalysis/-readOnly；未重导入或附加进程。
13个函数共4611条指令/18444字节，按Mach-O的VM/file映射独立逐字节复核全匹配，
见 `export-byte-verification.json`；字节匹配不等于Ghidra的自动签名或类型已经正确。

## 输出缓冲区实现

`output-buffer-4115.cjs` 的 `createBufferWriter({reserve,pointerAtOffset})`
只接受由调用方提供且已核验的原生辅助函数；导入时没有hook、进程发现、定时器或原生调用。

- dispatcher 0x5971c24 的x4为输出AutoBuffer。它不是Task，不能写x4+0x60。
- 五字段为pointer+0、position+8、length+0x10、capacity+0x18、malloc unit+0x20。
- reserve=0x5ded3c4，静态指令证明是__FitSize(buffer,size_t)；Ptr=0x56300b4。
- 先检查对象形状，再用原生扩容；精确复制Uint8Array视图，重置position=0/length=实际长度。
- 拒绝空/过大数据和无效对象；分配或部分写入失败清零有效长度并向上抛错。
- 不释放原生pointer，不改protobuf对象，不替换Task，不修改代码。
- 成功返回 `{serialized:true,bytesWritten:N,sent:false}`，不得转换成发送成功回执。

14项假内存测试通过，覆盖中文、1000字节、连续缩短、切片、内嵌零、容量/整数保护和故障。
这证明独立写入逻辑，不证明传入对象的真实类型和调用时机；调用方必须另外建立所有权证据。

## Task复制与析构的新增证据

`ownership-pass3/native-fn-5daa3c8.c`：原生复制路径复制字符串与容器；对+0x1c8和+0x1f0
分别构造AutoBuffer、清空、取源pointer/length并通过0x5ded508写入副本。
两块buffer是独立复制，不是共享指针槽。

`ownership-pass3/native-fn-46364ec.c`：析构开头依次调用0x5ded188处理+0x1f0和+0x1c8，
再释放字符串和容器。裸复制指针或覆盖对象布局会破坏该析构约定。

`callback-pass2/native-fn-59b73b0.asm`：调用0x5daa6fc复制thunk后进入0x5d5d3bc，
随后析构栈上副本。原始x1由调用方传入；Ghidra对上层函数显示的单参数签名不完整。
`ownership-pass3/native-fn-5d5d3bc.c`：队列包装再次进行原生复制并安排异步执行，
之后析构局部副本。因此不能把局部对象地址、队列提交返回或manager非空视为发送完成。
这些路径仍复制了外部上下文字段，不能仅凭buffer深复制就宣布完整Task生命周期已解决。

## 序列化与包装边界

分发器先走0x5980a6c动作分支；未处理时走0x597d26c。
普通分支通过mmcallback_虚表+0x50。后续静态核验已定位默认注册对象：虚表0x9e91af0的该槽指向0x465756c，仅`mov w0,#0; ret`；它不是正文序列化入口。活体具体对象本次未观察到，不能排除后续替换。完整注册链及独立dyld验证见`observation-and-callback-result.md`。
特殊分支Task+0x1c0==1，经0x5cc1d14尾跳到0x5cc4468。
后者读取Task+0x1c8的已序列化请求、CGI+0x18与cmdid+0x60，再做后续包装。
仅将输出x4替换成原始protobuf可能跳过所需包装，尚无可执行的正确发送配方。

## 未完成，不能放行

1. 正确文本Task、正文/CGI/cmdid/包装链已静态定位，newsendmsg wire及字段5哈希已有独立实现；活体服务身份也已只读匹配。仍需核验业务输入及原生协程上下文，账号扩展应走原生生产者而不手写密钥字段。默认普通回调为空实现不能用于直发。
2. OnTaskEnd依赖请求+0x68的完成functor，返回非零才析构；具体functor的shared捕获、克隆/释放及context首次结算现已证明。完整调度上下文与线程亲和性仍未证明；C++完成状态16项、正文RAII9例仅验证独立组件。
3. 第二观察器通过10项真实LLDB隔离清理验证；用户授权的只读身份窗口实际3.822秒、1次附加、匹配并立即解除、同PID/启动时间、P_TRACED清除且零残留。旧驱动仍拒绝，可发送的完整原生适配尚不存在。
4. 两个只观察授权均已结束、未发送。后续附加须新的明确单次授权，真正发送另须明确收件人/正文范围和独立回执。

上述缺口不通过改偏移、改开关或循环试挂解决。初版为全离线；后续执行两次分别获授权的单次只读观察，无UI操作、无发送、无原生模块装机。最新证据见mmreq-envelope-and-ownership-result.md的第二次窗口/C++组件节。

本轮基础包装实现、独立protobuf回归、完成所有权细节与fresh验证见`mmreq-envelope-and-ownership-result.md`；这项离线实现不构成可发送适配，A7保持开放。
