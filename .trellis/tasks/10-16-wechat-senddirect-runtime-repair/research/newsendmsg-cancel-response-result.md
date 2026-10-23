# 取消、响应与组合研究适配器（2026-10-16）

## 当前结果与边界

新增 NativeResponse、ResearchOperation 及编号响应解析器，串起 body 构造/parse、factory、拥有状态的 completion、回调内响应深复制和 wire 导出。没有加载器、活进程访问、地址解析、调度上下文入口或产品接线，不调用微信原生代码，不代表真实直发完成。产品拒绝门及版本锚表均未修改。

`newsendmsg-integrated-verification.json` 是本切片最终 fresh 证据；早期 `newsendmsg-operation-verification.json` 是加入工厂发布互斥门之前的历史测试，不覆盖最终文件哈希。未声称 sanitizer 通过。

## 原生取消链及竞态

- 取消functor的 invoke 是 `0x30c39b4 -> 0x30c3a3c`，不是 typequery `0x30c39bc`；handler 调用服务 vslot `+0x30`。
- 实际槽 `0x9e8fdd0 -> 0x46357ac`，thunk 将 service this 减 `0x10` 后跳至 `0x46353a8`；`text-contract-pass103/native-fn-46357ac.asm` 两条指令保留 w1 task id。
- `text-contract-pass20/native-fn-46353a8.c`：owner `+0x18` ready 位为真才执行；持 owner `+0x80` mutex 调用全局 stop 函数，然后查 `+0x70` taskid map。仍在 map 的请求走虚表 `+8` 删除，随后摘节点、解锁。此路径不调用完成functor。
- 该函数指针的磁盘初值 `0x5dad070` 不是运行期最终值。`text-contract-pass11/native-fn-5974418.c` 明确在 InitStaticFuncPtr 写 `0xa124b98 = 0x5973a80`。`text-contract-pass105/native-fn-5973a80.c` 是 MMStopTask，转 manager `0x597ee54`，再 `0x5d5f2cc` 构建 StopTask 工作项。当前静态切片不证明底层网络工作已完全排空。
- `OnTaskEnd 0x4635b9c` 先持同一个 owner mutex 取走请求并摘 map，然后解锁、解析响应、调用 completion，再按非零返回删除请求。因此取消查不到 map 不表示回调结束，晚到回调是允许的竞态。
- `0x6668c44` 只注册 context `+0xa8` cancellation functor；不是执行取消。context 的超时触发和调度器线程/完整排空仍开放。

## 工厂返回前的发布门

`0x30c2c1c` 在 enqueue 后还调用辅助函数并读取 request `+8` 返回 task id。原生上游 `0x30c295c` 持捕获 mutex 跨越 factory/取消注册；回调 `0x30c3420` 在访问 response 之前获取同一 mutex。研究适配器相同地用 shared publication mutex 阻止完成回调提前返回/删除请求。

`test_newsendmsg_publication_4115.cpp` 从工厂内部启动另一个线程，验证该线程不能取得发布锁且请求仍存活，工厂返回后才复制响应并释放请求。它验证真实 host mutex/libc++ 行为，未在微信内执行。

## 响应类型与复制

- request response getter `0x30c2fdc` 精确返回 request `+0xa8`（pass108）。
- NativeResponse 是 56 字节/8字节对齐，ctor `0x465bdcc`，深复制 `0x465f460`，非删除析构 `0x465ed38`。上游完成handler亦调用相同复制函数（pass77）。
- ByteSize `0x465f354` 递归更新缓存。`0x5ab3bc0` 从 vslot `+0x60` 取缓存后按 vslot `+0x50` 序列化，因此必须先 ByteSize，不能直接对尚未缓存的对象调用 array writer。研究组件先 IsInitialized、再 ByteSize、检查本地16MiB上限、序列化并核对尾指针。
- 外层 required mask 3；base mask 3（pass113 `0x465b7a0`）；条目 mask `0x7f`（pass109 `0x465e934`）。条目字段1～7必填，8可选。base/条目字段1为有符号 int32；其他编号和位宽见合同JSON。
- `newsendmsg_response_4115.py` 使用 protobuf 解析复制后的 wire，保留空列表、缺省/空 wrapper 的区别、字段8缺省和所有编号值；不把外层field2臆定为count，不赋予尚未证明的业务字段名，不声明送达或关联成功。

## 隔离验证覆盖

- response RAII：8类，深拷贝后源改变、初始化失败、空/超大、尾指针不符、copy异常和缺函数；构造/析构平衡。
- operation：11类，成功/传输错误/响应错误、32线程取消只发起一次、明确deadline、取消与超时后的晚到完成、发起对象离开后捕获存活、body拒绝和factory异常不重试；另100次完成/取消并发竞争，均无残留对象且 sent=false。
- publication：1类，工厂内已进入异步完成但返回前不得释放请求。
- Python响应：8项，手工wire而非共享schema构造器生成，覆盖required零值/缺字段、负值和宽数字、空列表、optional presence、未知字段、畸形输入和本地上限。
- 全部既有C++组件与33项Python切片/被动回归一并fresh验证，具体结果与源码哈希见 integrated JSON。
- `text-contract-byte-verification-v6.json`：182份函数导出（含重复）、28949条指令/115796字节均匹配冻结薄片，完整consumer另487条匹配。该核验只证明指令来源，不证明行为被执行。
- `newsendmsg-cancel-response-slot-verification.json`：20个槽由独立dyld链解码确认，其中包括取消及响应新增槽。

## 尚未完成，禁止放行

1. 业务输入的当前版本映射、完整账号/客户端标识来源及请求/响应相关性。
2. 原生协程入口与线程约束、context超时触发、取消后的网络与回调排空。
3. 安全的模块生命周期：weak_ptr过期仅证明状态持有计数变化，不能证明回调代码已离开；未提供 dlclose/卸载许可。ResearchOperation析构不隐式调用native cancel；后续前台监督必须在已证明的上下文显式收尾。
4. 清理合格的可执行实验、明确收件人/正文和新的单次目标/用途/期限授权。
5. 真正发送与独立回执、产品接入及两个安装入口终验。两次只读授权已消费，A7保持开放。
