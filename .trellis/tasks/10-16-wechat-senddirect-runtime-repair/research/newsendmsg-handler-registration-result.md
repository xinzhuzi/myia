# 文本处理器与实际服务注册表的离线关联

本切片只读取冻结 ARM64 文件与既有 Ghidra 工程；没有加载或操作微信。账号安全停止记录继续优先适用，A7 未完成，产品拒绝门保持。

## 已核验事实

- `text-contract-pass208/native-fn-317ba5c.asm`：服务保存在 x19；0x317bc0c/0x317bc28 从 service+0xb20 取 storage，0x317bc2c 设 x1=storage+0x28，x2 指向本栈弱引用参数，0x317bc34 调 0x30e3fb0。反编译显示的额外首参不符合原始寄存器，不得照抄。
- `text-contract-pass140/native-fn-30e3fb0.asm`：初始化器保留这两个 map；名称 helper 0x30e74f4、文本工厂 0x30e7aa0、handler-map 插入 0x30e7be8 相连。后者将结果 shared pair 移至 node+0x28/+0x30，并清空临时 pair（pass202 的 0x30e7dc8～0x30e7dd0）。既有文本身份合同的 SHA256 本轮重新核对，未修改。
- 同一初始化器将整数 1 经已解析的 std::to_string thunk 0x713ff28 生成键，并将 TextMessageHandler 名称送入另一张表（0x30e403c～0x30e405c）。pass206 与 pass209 证明 0x30e7fd4/0x30e8380 将 key string 放入 node+0x10、名称 string 放入 node+0x28。节点构造器用隐藏 x8 返回，并非反编译显示的普通首参数。
- `text-contract-pass189/native-fn-319a6a8.asm`：选择时再次取 service+0xb20，低/高类型引用经 0x30e3df8 生成键，查 storage+0x28 得名称，再查 storage 得 handler node。0x319aaac～0x319aac0 将 node+0x28/+0x30 的 pair 写入隐藏 x8 返回区并增加强引用。
- `text-contract-pass210/native-fn-30e3df8.asm`：低类型非49走 to_string(low)；49分支拼接下划线和高类型。类型1选择文本 handler 的静态表关系成立，尚不能据此认定任意来源对象的类型或布局。

## 两条通知的实际接收方

`pass208` 在 storage+0x10 链表逐节点取 node+0x28 的 handler，以 0x6686420 注册：

| handler 容器 | 服务成员目标 | 调用包装 | 已核验后继 |
|---|---|---|---|
| +0x18 | 0x317d1cc | 0x3213a30 | 复制 record 到单元素 vector，通知 service+0xc0 的 0x319eef8；另复制一份交给所获服务的 0x3960e34 |
| +0x90 | 0x317d4ac | 0x3213a74 | 调整 this 至 service+0x228，尾调 0x30d0a14 转发 flags/record |

前者包装把 record 参数由 x2 转 x1；后者读取 flags 引用并保留 record。执行器来自 0x466ad74 返回对象+0x10，但其具体类型、队列线程与排空仍未证明。这些是通知链，不是文本 producer+0xd8 的已证明调用点，也不是送达回执。

## 本轮验证与完成边界

`python3 Library/ai/verify_wechat_handler_registration_20261016.py`：14份函数导出共5274条指令逐条匹配冻结文件，67个关键位置通过；新验证器 Ruff 通过。验证器同时核对冻结文件完整 SHA、既有文本合同 SHA 与停止记录 SHA；完整字节匹配不等于已理解函数全部语义。

新研究合同：`newsendmsg-handler-registration-contract.json`，SHA256 `6911f2a4b1956576d0734a5c4f1c7f51687f7ccf772af235cc83ff39a4ef198f`。验证详情：`newsendmsg-handler-registration-verification.json`。

仍缺：context 到文本 producer 的准确虚调用、普通文本输入身份与收件人方向、真实 group/config/线程与末尾排空、完整适配和独立回执。下一步仅从已留存的 context 状态派发继续静态定位；禁止因本切片通过而恢复微信附加/UI/发送/登录实验。没有产品源码、真实版本JSON、安装件或账号状态改动；不提交、不归档。
