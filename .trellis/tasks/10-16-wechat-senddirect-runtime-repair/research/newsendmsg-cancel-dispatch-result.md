# 协程作业取消与网络请求取消的边界（离线，2026-10-16）

账号安全停止约束保持。本切片仅分析冻结薄片及已有Ghidra工程，没有访问微信进程、界面、账号或网络请求；未运行LLDB，未修改产品或安装件。

## 两条作业取消handler

`0x667e8cc`根据作业启动标志选择两个function。独立dyld链核验确认它们的invoke槽：

| 条件 | function虚表 | invoke槽 | 函数 |
| --- | --- | --- | --- |
| 已启动 | `0x9fb2e78` | `0x9fb2ea8` | `0x668082c` |
| 未启动 | `0x9fb2ef8` | `0x9fb2f28` | `0x6680ad8` |

已启动handler先向作业`+0xa8`中的协程对象转交`-1`，再读取协程核心`+0x288`状态；仅在状态为3且作业`+0x150`尚未置位时调用`0x667fc38(job, 1)`。未启动handler直接调用相同完成处理。`+0x150`由正文工作入口`0x667f534`置位，不能把它与`+0x141`运行标志混为一谈。

证据：`text-contract-pass152/native-fn-668082c.asm:4`、`:11`、`:16`及`:23`，`native-fn-6680ad8.asm:1`；核心状态读取见`text-contract-pass153/native-fn-6674168.c:8`，工作入口见`text-contract-pass148/native-fn-667f534.asm:8`。

## Ghidra省略参数，不能直接照抄声明

`0x66741a4`的原始指令仅解引用x0并尾跳`0x66741ac`，保留调用处传入的x1；调用处明确写`x1=-1`。目标原始指令`0x6674404`仍测试x1的符号位，但Ghidra把两个函数都推断成了只有一个参数。此处以寄存器数据流为准，不能把伪代码声明当成可调用ABI。

核心函数在状态0时写状态3并返回；其他状态包含当前TLV对象比较、`+0x3c8`检查、清`+0x3f0`和调用`0x6677e1c`的不同路径。仍未完整核验下层调度和异常清理，不把它描述为可在任意线程调用的同步排空函数。

证据：`text-contract-pass153/native-fn-66741a4.asm:1`；`text-contract-pass154/native-fn-66741ac.asm:15`、`:18`、`:23`、`:151`、`:324`及`:661`。完整指令来源已逐项匹配冻结薄片。

## 适配器必须保留两层取消

上述对象是协程作业，取消它不等于已取消工厂产生的网络请求。现有`newsendmsg_operation_4115.hpp`的`OperationFunctions.cancel(service, task_id)`负责请求服务的取消；它与本切片的作业取消入口属于不同对象和合同。后续适配不得仅停止作业或清运行标志，就丢弃原生task_id及尚可能晚到的请求完成回调。

两条handler均未直接调用已定位的作业join入口`0x667eca4`或`0x6680b64`，但这不证明下层所有路径都不会阻塞。完成入口、promise结果和运行标志也都不足以证明最终用户回调及weak引用已经销毁，限制见`newsendmsg-scheduler-lifetime-result.md`。

配置链还有独立约束：`0x66846b8`把配置`+0x18`为零的值替换为group对象`+0x120`，再经`0x667ddf8`构造作业；group本身还持有作业列表。仅持有一个作业指针并不能据此证明组及调度服务可以销毁。证据：`text-contract-pass88/native-fn-66846b8.c:53`，`text-contract-pass89/native-fn-6682d18.c:53`。

## fresh验证及开放项

`newsendmsg-cancel-dispatch-slot-verification.json`共16槽全部匹配，其中两条取消invoke槽为本轮新增；`text-contract-byte-verification-v14.json`共246份函数导出（含重复）、41483条指令/165932字节匹配，完整consumer另487条匹配。较v13新增6份导出、1308条指令/5232字节。新验证脚本Ruff通过，四次Ghidra均为readOnly/noanalysis、退出0。

尚缺：具体调度服务及尾部引用排空、两层取消组合与超时的完整合同、业务字段关联、可执行适配与独立直发回执。A7及实施20～24仍未完成，不新增活体授权、不恢复测试、不放行产品直发。
