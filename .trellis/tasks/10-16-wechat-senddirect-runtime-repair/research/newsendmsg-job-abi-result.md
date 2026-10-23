# 作业返回值与调用寄存器合同（离线，2026-10-16）

账号安全停止约束保持。本切片只读取已留存反汇编并编译/运行自有夹具；没有运行微信、LLDB、界面操作或账号操作，没有修改产品或实际版本JSON。

## 原生入口声明必须包含非平凡返回值

`0x66846b8`保存x0～x3及x8的原始指令表明：x0为group，x1为配置，x2为正文function指针，x3为完成function指针，x8为16字节作业句柄返回区。Ghidra把隐藏返回区显示成普通的首个参数；如果照伪代码的五个参数依次传x0～x4，所有输入都会错位。

`0x6684b8c`是仅接受group、配置和正文function的转发入口，保留相同的隐藏x8返回区，自行准备空的完成function再调用完整入口。正文/完成function是32字节非平凡对象，涉及clone/move/析构，不能替换成整数或普通代码地址。

已新增研究声明`newsendmsg_job_abi_4115.hpp`：以opaque group/config/job类型、`std::shared_ptr<Job>`返回值和两个`std::function`指针表达合同。它没有任何地址解析、加载器、调度器或发送入口；不构造未知配置，也不自动运行真实函数。

证据：`text-contract-pass88/native-fn-66846b8.asm:7`及`:11`保存参数及返回区，`:50`向返回区写两个指针；`text-contract-pass86/native-fn-6684b8c.asm:29`及`:31`保留x8，`:36`、`:37`、`:38`准备两个function参数并转发。13个原始指令位置已与此前逐字节核验的导出对应。

## 独立夹具证明的范围

`test_newsendmsg_job_abi_4115.cpp`与`job_abi_fixture_4115.S`仅链接本机C++标准库：汇编捕获实际x0～x3/x8寄存器，并在x8返回区构造空句柄；另一个自有C++函数返回有所有权的句柄。以下五个夹具场景通过：

1. 完整入口四个参数指针和隐藏返回地址与调用者对象逐项相同，返回空句柄可正常析构。
2. 简化入口三个参数指针及隐藏返回地址逐项相同，不触发正文或完成回调。
3. 自有函数经相同类型的函数指针调用，正文回调执行一次。
4. 同一次调用中的完成回调执行一次并接收true。
5. shared句柄复制与reset保持对象存活，最后一个strong引用退出后对象只析构一次，weak引用可独立释放。

这证明本机Apple ARM64/libc++的类型级调用及夹具所有权行为，不能证明原生group/config有效、原生回调的全部类型已还原、任意线程可调用或真实作业已排空。

## 默认group不能当成运行配方

`0x66845a4`先查询当前协程/线程group，缺失时才取得默认对象；`0x66853a4`在取得group后调用`0x2e0a888`取group+0x108的配置并复制。`0x66846b8`还对配置中的空字段及两个整数哨兵做group默认值补齐。该链依赖运行时对象和状态，不能只把静态默认地址填入版本JSON，也不能认为全零配置已成立。

证据：`text-contract-pass97/native-fn-66845a4.c:9`，`text-contract-pass98/native-fn-6684284.c:14`，`text-contract-pass96/native-fn-66853a4.asm:23`～`:25`及`text-contract-pass97/native-fn-2e0a888.asm:1`；默认补齐见`text-contract-pass88/native-fn-66846b8.asm:24`起。

## fresh验证与开放项

`newsendmsg-job-abi-verification.json`保存编译命令、夹具结果、二进制及所有相关源文件哈希。5场景与13个原始指令位置通过，新Python验证脚本Ruff通过。使用既有`text-contract-byte-verification-v14.json`证明所引用导出的字节来源；本轮没有新增Ghidra导出，也没有把旧产品测试当作新执行结果。

仍缺真实调度对象与线程合同、作业/请求两层取消及尾部引用排空、业务字段关联、可执行适配和独立直发回执。研究声明不装机，`callable_for_send=false`，A7及实施20～24保持开放。账号安全停止约束不解除。
