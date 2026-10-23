# 发送命令注册、实际派发与上游协程路线（2026-10-18，实施67部分）

## 本轮补齐

冻结ARM64中的命令名为 `message::send_message`：0x28544e4从五个原始常量的低32位及立即数0x65/NUL重建该名，再调用0x286f9c8。后者创建引用计数回调，invoke=0x286fb58，交给0x28569a4写入service+0x20命令表节点+0x40。节点+0x28是另一份注册字符串；它没有作为实际回调x2传入。

实际调用在0x2857ca4：用request+0x18所指string查同一张表；命中后保留节点+0x40回调，读取其+8函数指针，于0x2858278调用。精确参数是x0=回调对象、x1=request+0x20所指string、x2=request+0x10所指string、x3=拥有的completion指针地址。0x286fb58移动completion，经0x286fbac进入既有JSON→builder链，x1/x2不变。此回调采用0x33c40的引用计数/函数指针头，不能按std::function的虚表调用。

request的原生类型名为 `chatbot.WxFunctionCallInput`，从0x55bf46c的常量字节重建。构造器0x559f2a0安装虚表0x9f11538，parser0x55bedc4与serializer0x55bf164相互核对：wire field2→+0x10、field3→+0x18、field4→+0x20；存在位在+0x38。故发送builder转发x2来自外层field2，不是JSON解析后的chat_id，也不是注册时的描述字符串。未恢复官方字段名，不能把它命名为用户名、收件人或客户端消息标识；字符串字节可能相同不改变来源不同这一结论。

所选上游路线也已连通：0x2660d9c从0x4669774取得全局service（槽0xa45df38），由0x466ad74取得service+0x290/+0x298协程接口shared pair；创建虚表0x9d9fa60、invoke+0x30→0x2661260的正文，调用0x453cce8提交。真实寄存器为x0=接口、x1=config地址、x2=拥有正文地址、w3=1、隐藏x8=结果pair。正文数值2路径解析外层事件，0x2684bf0数值0x7d5分支进入0x2686020，后者构造/解析WxFunctionCallInput，取得命令表服务，再同步进入0x2857ca4。复用既有执行器合同；这是所选原生调用路线的静态连接，不证明任意线程安全、当前线程身份或全部调用路线。

## 对适配器的影响

先以完整高层原生链划定输入边界：外部JSON的chat_id、message_type及两个正文入口已经有精确映射；这次另补外层field2的来源。现有原生record/producer链自己生产时间/local_id/client-id/hash并取得账号包装；不应为了写适配器而无限追溯所有登录缓存或在JSON中手工重建这些内部字段。仍须核验高层builder的完整门槛、field2在发送作业中的所有作用及参数保持，不能因此跳过方向/身份、线程与排空验证。

## 验证与失败记录

`python3 Library/ai/verify_wechat_command_dispatch_20261018.py command-dispatch-20261018-verification.json`退出0：24份选择导出4343条原始指令全部匹配冻结文件，132项关键位置、31条独立分支目标、4槽dyld链及两份名称字节通过；新验证器Ruff通过。校验器没有微信加载器或运行调用。

合同SHA256：09f256c9a7fae2750dc05d46f32ed762faf69fd09a6238113841cf28911d5bfa。
校验器SHA256：ea7fd8ec42c1863b8aaf68f8001e33fed5722953e9a06f2d04753822c3a171a1。

新增OfflineDispatchInventory.java仅列已选区域的函数边界/间接调用数量。pass375遇到256函数上限，Ghidra进程仍返回0但日志含REPORT SCRIPT ERROR；该次是失败的定位资料，不计成功验证。pass376/378缩小区域后检查退出码和脚本错误文本；验证器也拒绝SCRIPT ERROR。pass377中其他模块导出、3eabc70另一调用路线及未独立核验的schema构造不计入上述24份证据。

## 剩余与下一步

实施67保留未勾：继续沿已确认文本builder所捕获的field2 string追到作业体及响应，补完整前置条件/参数作用；线程问题回到55的取消状态0、服务关闭和最终拥有者清理，不再转去追登录缓存。A7及11/18/20～24/55保持开放。真实线程身份、完整原生适配、真正发送/独立回执及部署未完成；账号安全停止记录保持，未操作微信、未改产品/安装件、无Git/worktree/删除/归档。
