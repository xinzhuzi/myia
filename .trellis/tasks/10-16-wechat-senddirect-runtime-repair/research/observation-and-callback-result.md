# 单次观察与默认回调核验（2026-10-16）

当前 **send_direct 未完成，未发送任何消息**。本轮完成了观察执行器清理验证、一次已授权的微信观察，以及默认回调注册链的静态核验；不能据此启用原生发送。

## 用户授权与实际窗口

用户对 `call_EDiItm3EkUrLX7ZUeObpWbFp` 明确回复“授权上述窗口，最长 30 秒”。范围是当前 WeChat 4.1.15 的一次前台观察，不包含自动发送、UI 触发、表达式调用或原生数据注入。

- 实际窗口共 **21.053 秒、1 次附加、0 次重新附加、0 次发送**。
- `live-observe-aegb31sm/supervisor.json`：`cleanup_ok=true`、`target_recovered=true`、`helpers_remaining=0`；LLDB 与 debugserver 均 exit 0。
- 微信 PID 33589、启动时间 `1792085027.181673` 前后一致，最终 state=2、flags=16388，`P_TRACED=0`。后续独立复查同一进程 state=2、flags=16452，调试位仍清除，两个调试器均无残留。
- 用户及系统 DiagnosticReports 顶层自窗口开始后均无新的 WeChat 报告文件；只查文件元数据，未读取崩溃内容，见`post-window-crash-report-check.json`。未重新做人工流畅度验收。
- 实际 Resources 模块 UUID `0C2F01C0-C197-3286-901D-70E1D007A1C0`，模块基址 `0x13be04000`；0x490fb20 与 0x597d398 两处字节匹配。
- 一个请求观察硬件断点已建立，窗口内 **没有自然命中**，到时 `Detach(False)` 成功。没有命中仅描述本窗口，不能排除其他时间或请求分支。
- `observation-window-consumed.json` 独占创建，任务授权字段已标记 consumed；现有执行入口会拒绝复用。该授权已结束，任何后续附加都必须重新得到明确授权。

## 清理资格验证

`cleanup-qualification.json` 固化了执行器、状态探针与夹具的哈希及 9 个真实 LLDB 场景。测试只启动新建的无网络夹具；无一附加已有应用。正常命中、到时、SIGTERM 取消、内嵌 Python 异常、目标操作前失败、客户端在停止态/运行态死亡、父进程限时强制断开均验证原夹具存活且调试位清除，辅助进程退出。另对经系统探针证明不存在的 PID 验证本机附加失败协议，实际 `vAttach` 前发送的是 `QSetDetachOnError:1`，没有覆盖为 0。

空 debugserver 先收到 detach-on-error 的真实 OK 应答，才允许目标操作；父子使用 `clock_gettime(CLOCK_MONOTONIC)` 共享截止时间，提前结束观察，预留脱附和系统状态复验时间。取消先通知 LLDB，阻塞时关闭该客户端，由已设置的 debugserver 脱附。这些是本机已测场景的证据，不把纯 Python 模拟、LLDB exit 0 或单次成功推广为所有操作系统故障的保证。

隔离测试实际发现并修复了三项兼容问题：LLDB 内嵌 Python 3.9 的 `time.monotonic()` 起点与外部 Python 不同；ConnectRemote/Continue 的状态通知滞后；一次性断点命中后 stop reason data 可以为空。现在使用共享时钟、StopID 和命中 PC；正常与异常均恢复 `None` 信号处理器为 SIG_DFL。

执行器只保留在 research，没有接入产品，也没有解除 `_require_safe_live_driver()`。旧哨兵和旧驱动没有恢复。协议日志所在目录权限为 700，仅留作本机证据，不复制聊天内容到报告。

## 离线默认注册链

窗口结束后仅复用已有 Ghidra 工程，以 `-process / -noanalysis / -readOnly` 做定点查询。没有第二次附加。以下是静态默认初始化关系，**不是本次活体回调采样**：

| 地址 | 已核验关系 | 证据 |
| --- | --- | --- |
| 0x462e4d4 | 创建 0x10 字节回调包装；0x462e5c0 调 0x4656fc4，存到 owner+0x38；0x462e734 取该对象，0x462e738 调 SetMMCallback | callback-registration-pass6/native-fn-462e4d4.asm |
| 0x4656fc4 | 安装虚表 0x9e91af0，将 owner 第二个基类地址放包装+8 | callback-registration-pass7/native-fn-4656fc4.asm |
| 0x5975054 | 日志为 SetMMCallback，取 default MMStnManager 后调用 0x9d3cf0 | callback-registration-pass7/native-fn-5975054.c/.asm |
| 0x9d3cf0 | `str x1,[x0,#0x10]; ret`，保存 manager 的 mmcallback_ | callback-registration-pass8/native-fn-9d3cf0.asm |
| 0x9e91b40 | 虚表+0x50；Ghidra 解析到 0x465756c；独立解析原文件的 format=6 dyld chain，走过 815 个节点确认本槽确实属于修复链，得到相同目标 | callback-slot-verification.json |
| 0x465756c | **`mov w0,#0; ret`**，默认普通 MMReq2Buf 回调为空实现，不能当正文序列化入口 | callback-registration-pass9/native-fn-465756c.asm |

`callback-registration-byte-verification.json`：新增 10 份函数导出、633 条指令、2532 字节与同一 SHA256 的 ARM64 文件全部匹配。虚表独立验证依据本机 SDK `fixup-chains.h` 的结构；原槽值 `0x1000000465756c`，解出的目标为 `0x465756c`，目标 8 字节也吻合。没有依赖对原始指针随意截位。

这一结果缩小了路线：**不能把默认普通回调填进 JSON 当可发送入口**。不能据此声称所有文本都走特殊或 action 分支，也没有证明运行时不存在后续替换回调。

## 仍然开放的交付

1. 真正的任意正文 Task 构造、CGI/cmdid、输出包装和请求对象的关联。
2. 外部上下文、队列、完成回调及析构的完整所有权合同。
3. 可发送的原生适配及另行明确授权后的真实消息回执验收。本窗口只观察，不能用于这一步。

实际版本 JSON 继续保持身份与 4.1.15(270135) 对齐，失效调用字段为 null。A7 未勾选，L3 仍 blocked；未提交、未归档、未装入未经验证的原生代码。

本轮 Python 语法编译与相关 5 文件 ruff 均通过。未重复整套产品回归，因为这轮只改研究执行器和任务工件；此前 845/14 门控跳过的产品验证与本轮 9 项清理验证是不同范围。两位已有只读探子中，bounded_debugger_design 提供了旧执行器风险核验，native_callback_scope 未产生分析；实现与最终核验由主代理完成。
