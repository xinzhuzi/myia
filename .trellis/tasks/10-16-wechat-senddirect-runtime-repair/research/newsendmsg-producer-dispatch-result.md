# 文本 producer 的条件派发链（仅离线）

## 结论与边界

冻结的 WeChat ARM64 4.1.15 (270135) 中，第二队列经已注册的文本 handler 到 `0x3107b0c` producer 的条件静态路径已连接。它补齐前一轮 registration 合同的派发缺口，不证明当前账号执行过该路径，也不证明任意正文可发送或消息送达。

本轮只读取冻结薄片和已有导出；没有执行/附加/激活微信，没有 LLDB、注入、发送、截图、AX、键盘、剪贴板、登录或重启操作，没有产品/真实配方/安装件变更。账号安全停止约束继续生效，不申请新的实机窗口。

## 条件路径

| 阶段 | 入口与关键条件 | 证据 |
| --- | --- | --- |
| 上一阶段连接 | `0x31d15fc` 的准备结果两字为零后，设置 context 状态 6，取得 context key 并调用 `0x31cbd88` | pass187 `native-fn-31d15fc.asm`，`0x31d1ab4` 至 `0x31d1ad4`；准备阶段条件另见 forward-queue 合同 |
| 第二队列 | `0x31cbd88` 从 `*(service+0xb20)+0x88` 按 key 查找；节点存在、vector 非空、首 context 状态 6、`0x318d680` 返回非空 handler 后，设置状态 7 | pass218 `native-fn-31cbd88.asm`，`0x31cbdc0` 至 `0x31cbe08`、`0x31cc0c0` 至 `0x31cc104` |
| 作业捕获 | 分配 `0x48` 字节、虚表 `0x9def470`；捕获 context pair `+8/+10`、handler pair `+18/+20`、service `+28`、key string `+30`，交给 `0x453d344` | 同文件 `0x31cc7c8` 至 `0x31cc888` |
| 作业正文 | 虚表 `+0x30` 槽 `0x9def4a0` 解码为 `0x32243a8`，正文复制两组 shared pair 后调用 `0x3224fe8` | pass215 `native-fn-32243a8.asm`，`0x3224620` 至 `0x322465c`；独立 dyld 链解码 |
| 前置检查 | `0x3224fe8` 调 `0x30d66c0`，后者调用 handler 虚槽 `+0xd0`；文本对应 `0x3107afc`，以零/零尾调结果构造器 `0x304f1cc` | pass213、pass215、pass203 的对应 `.asm`；文本槽 `0x9de9b38` 独立解码 |
| producer | 前置结果两个 32 位字均为零时设状态 10，调用 `0x30d692c`；该包装器调用 handler 虚槽 `+0xd8`，文本槽 `0x9de9b40` 解码为 `0x3107b0c` | pass213 `0x3225084` 至 `0x322508c`、`0x3225258` 至 `0x322528c`；pass211 `0x30d699c` 至 `0x30d69a8`；独立 dyld 链解码 |

这里的“文本 handler”身份依赖上一轮已核验的 `newsendmsg-handler-registration-contract.json` 和 `newsendmsg-text-handler-contract.json`：同一服务的 type key→name→shared handler 查找与文本虚表 `0x9de9a68` 已连接。本轮未修改这两份合同，其哈希保持一致。

## ABI 与拥有权

`0x3224fe8` 的真实参数是 x0=context pair 地址、x1=handler pair 地址，隐藏 x8=result。其 producer 调用前将 x0 设为 handler 对象，x1 指向栈上 context pair 副本，x8 指向本地结果区。Ghidra 把隐藏结果区显示成额外首参，不能直接把反编译函数声明用于调用。

`0x30d692c` 的 x0=handler、x1=context pair 地址、隐藏 x8=调用者提供的结果区。虚调用前保留 record pair（context `+18/+20`）、辅助 pair（`+28/+30`）及 context pair；虚调用后分别释放。`0x30d69a0` 是函数内部的 load 指令，真实入口是 `0x30d692c`，不能把导出文件名作为调用地址。

正文在第一次 helper 前还检查非空 record 的 `0x4a28ef8` 返回值 bit0，未置位时先设 context 状态 9，再继续 helper；此处没有绕过 helper 的路径。该 record 谓词的业务语义仍未证明。

## 原生条件性第二次调用

正文仅在第一次 helper 的两个结果字至少一个非零时检查 `0x30dc518`。该谓词要求第二个 32 位结果字为 `0x66`、context/record/辅助对象非空、context 状态 10、record 谓词 `0x4a28ef8` 非零，且辅助对象首字节 bit0 置位。满足时正文清该字节，再调用 helper 一次；本正文没有包住这两次 helper 的重试循环。

这是冻结指令中的原生行为，绝不是恢复调试器自动重试或发送重试的许可。`0x30dc518` 的实际寄存器是 x0=handler（本函数未使用）、x1=context pair 地址、w2=第二个结果字；Ghidra 调用点的推断原型与此不一致，以原始指令为准。

正文最后调用 `0x3127208(context+0xa0,result)` 发布结果，然后以捕获的 service/key 再调队列入口 `0x31cbd88`。结果发布、队列继续处理和阶段返回都不是独立送达回执，也不是最终回调/weak 引用已经排空的证明。

## 可复现核验

命令：`python3 Library/ai/verify_wechat_producer_dispatch_20261016.py`。验证器只读冻结文件和留存导出，独占创建验证报告；本次已生成，重复执行不会覆盖报告。

- 冻结薄片 SHA256：`6a5bd0cbb39ad3092c15e9debda2db4969eedf1b58caad244d88033a996833a7`。
- 8 份导出、2,950 条指令（11,800 字节）匹配，92 个关键指令位置核验通过。
- 3 个槽使用原始 Mach-O dyld chained fixups 独立解码通过：作业 invoke、文本 precheck、文本 producer。
- 范围 `[0x30c0000,0x3230000)` 的 `LDR #0xd8` 后 1～6 条内同寄存器间接分支模式：126 个 load、1 个模式命中，位置 `0x30d69a0→0x30d69a8`。它只是有边界的定位扫描，不证明全文件唯一，也不分析一般寄存器覆盖；该命中的语义另由完整函数指令和反编译核对。
- Ruff 通过。结果与哈希见 `newsendmsg-producer-dispatch-verification.json`；新合同见 `newsendmsg-producer-dispatch-contract.json`。

## 仍未完成

普通文本输入对象如何构造及其精确类型、收件人方向与 source 身份、真实 group/config/线程约束、取消组合与末尾回调排空、完整可执行适配及独立送达证据仍缺。A7 和实施 20～24 保持未完成；账号安全重新登录的根因仍未确认。
