# 原生执行器 TLS 来源与研究适配约束（2026-10-18）

本切片推进实施55/22，未关闭A7或真实调度/清理缺口。只读冻结二进制，运行自有服务夹具；没有微信加载、附加、原生调用、UI操作、发送或部署。

## 已核验的原生合同

- `0x6662530`无普通参数，通过`0xa24de50`的TLV描述符取线程局部存储，再返回其中的原始执行器指针。Mach-O节为`__DATA.__thread_vars`、类型`0x13`；沿chained fixup和import table独立解出`__tlv_bootstrap`。
- `0x6662554`写相同TLS槽。这里只作为来源证据，不向研究适配器提供setter。此函数跨特殊TLV bootstrap调用保存`x8`，不得推广为一般AAPCS64的callee-saved规则。
- 工作入口`0x6666628`把输入执行器保存在`x19`，调用`pthread_self`并写执行器`+0x28`，在`0x66666b0`设置TLS，调用执行器`+0x10`所指looper的虚槽`+0x10`，正常返回后清TLS及`+0x28`。`pthread_self`的stub与import槽另按原始指令和绑定链核验；这里只证明所选正常路径，未覆盖异常展开。
- `0x6666ec4`调用上述getter，非空时dynamic_cast的源/目标RTTI为`0x9fb1808/0x9fb1a78`，支持其执行器来源。旧恢复条件function的虚槽`+0x30`仍不是线程检查。

原始出处为`text-contract-pass273`的worker/consumer和`text-contract-pass397`的getter/setter。四个完整导出共85条指令逐字节匹配冻结ARM64文件，29个指令位置、4个直接分支目标、2个导入绑定及TLS节类型独立核验；Ghidra日志没有`REPORT SCRIPT ERROR`。合同见`newsendmsg-executor-context-contract.json`。

## 已落地的研究组件

`newsendmsg_executor_operation_4115.hpp`新增`ExecutorResearchOperation`，组合已有`ResearchOperation`。构造时先检查getter和预期执行器身份；空值/不匹配在NativeBody构造与factory之前拒绝。每次`cancel/expire`先重新核对当前执行器，再由底层独立线程生命周期令牌检查控制线程；早到超时和已完成操作也不绕过检查。响应回调、snapshot及task_id观察仍可跨线程；析构不查询TLS、不隐式取消。

这里只检查入口上下文，不持有原生执行器生命周期租约，不设置TLS、不创建替代线程、不自动调度或重试。原生getter本身属于注入的上下文查询；“拒绝错误上下文”指不继续构造正文、调用factory或请求cancel，不声称连getter也不调用。预期指针的活性、服务/模块持有、实际组身份与完整关闭协议仍由后续合同证明。

## Fresh验证

命令：`python3 Library/ai/verify_wechat_executor_context_20261018.py`。

证据：`executor-context-20261018/verification.json`及逐项build/run日志。新夹具9场景通过，覆盖缺getter/预期身份、空/错TLS在正文之前拒绝、同线程TLS改变时保留pending请求、恢复后显式取消一次、已完成控制仍检查、32个异线程伪造相同夹具指针仍拒绝64次、异线程晚到回调深复制且保留超时、跨线程析构不隐式控制，以及解析/factory失败不重试。请求/正文/响应计数全部配平，sent始终false。

依赖夹具`operation`11场景/100次取消完成竞态、`operation_thread`4场景/69次异线程控制拒绝均通过；本机再次观测到thread::id复用而生命周期令牌拒绝控制。三组均以Apple ARM64 C++17严格警告编译运行，新Python验证器Ruff通过。证据记录完整源依赖和合同哈希；账号停止文件SHA256保持`b720bc05887b89181171e54997b0e470c32186bfef4014fb680132bb8757ca5d`。

## 尚未关闭的边界

TLS相等与线程令牌不能证明协程身份、core状态、原生组取消相对首次恢复的顺序，也不能阻止原生外部取消。状态0最终参数释放、所有间接通知、最后持有者与完整排空仍开放；不报告已发生原生泄漏。完整业务字段保持、完整原生适配、真实发送/独立回执和部署仍未完成。

继续点：`0x453df64`的组切换调用者`0x4551eac/0x466dfb8`及关闭入口`0x4671338`；pass398已只读导出前者/关闭入口，须进一步核验寄存器来源及调用上下文后才能用于顺序结论。不得从无显式线程检查推断允许任意线程调用。账号停止约束保持。

## 组切换与关闭调用者后续核验（实施69，55仍未完成）

`text-contract-pass398～401`补齐一条直接调用链：`0x2fec684→0x46735dc→0x4551eac→0x453df64`。其中`0x4551eac`的普通输入是`x0/owner、x1/options`，共享结果通过隐藏`x8`返回；它取全局服务、经`0x466ad74`取`+0x290/+0x298`接口，再以空string调用组切换。空名且有活动组的已选分支依次调用`0x668272c`取消、`0x66823c4`等待、删除虚槽并清`interface+0x10`。这里的等待仍不是完整请求/捕获排空证明，不能把反编译器的移位参数声明当作ABI。

另一条已核验链为Ghidra标识为`_WeChatMain`的四字节跳板`0x1986c→0x2c976c`，后者调用`0x4671338`，再调用服务关闭`0x46698d0`。没有因此给该线程命名、假设它等于执行器线程，或证明关闭前没有在途首次恢复。大函数只按调用点分段检查，没有全函数业务语义或所有前驱保持证明；跳板的伪代码会内联大函数，只采用其四字节原始分支。

Fresh验证命令为`python3 Library/ai/verify_wechat_shutdown_callers_20261018.py`，证据`shutdown-callers-20261018-verification.json`。9份Ghidra选择导出4343条指令匹配冻结文件、26位置/12独立分支核验通过。首次严格连续性检查拒绝`0x2c976c`：Ghidra漏掉`0x2cb2f0`的`brk #1`且提前结束。初版验证器保存在`shutdown-callers-20261018-first-verifier.py`；并未把其失败算作通过。

随后`export_wechat_shutdown_caller_20261018.py`以独立compact-unwind重算`0x2c976c～0x2cb664`范围，LLVM完整导出1982条，覆盖上述brk与额外尾段共220个遗漏位置；去重4563个指令位置均匹配冻结文件。完整输出及边界在`shutdown-callers-20261018-llvm/`，最终验证器重新计算并比对边界；三个本轮Python脚本Ruff通过。没有从异常尾段存在推断其清理语义。所选链已具体化，调用者执行器身份、所有间接影响及与原生首次恢复的全序关系仍缺；55/22/67与A7保持开放，不操作微信或部署。
