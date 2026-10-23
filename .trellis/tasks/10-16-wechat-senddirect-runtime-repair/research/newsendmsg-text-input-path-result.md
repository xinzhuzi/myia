# 类型1输入对象进入文本发送链（离线）

## 新结论

一条明确的数值类型1输入路径已从构造、正文赋值、作业捕获连接至 `0x317df64` 发送服务入口。输入对象的 RTTI 与文本准备函数要求的 RTTI 相同；此前“只看到写1，尚未连接发送身份”的缺口在这条路径上已补证。它不覆盖所有 UI 普通文本入口，也不证明真实执行、当前账号状态或消息送达。

账号安全停止约束保持：本轮仅使用冻结薄片与只读 Ghidra 工程，没有 LLDB、活进程访问、微信/UI/账号操作、发送或登录测试，没有产品/真实版本JSON/安装件变更。

## 对象类型和数值

- 工厂 `0x77bdd0` 分配 `0x610` 字节，隐藏 x8 返回 shared pair；payload 为 allocation+`0x18`，大小 `0x5f8`。
- 构造器 `0x77be90` 调用 base `0x69a714` 后，将 payload 虚表设为 `0x9eb26a0`。原始 dyld 链独立解码其前一槽 `0x9eb2698` → RTTI `0x9eb2598`，与 `0x3105a98` 文本准备阶段的 dynamic_cast 目标一致。RTTI 的 base 槽 `0x9eb25a8` → `0x9eb2580`，不是根据对象偏移猜类型。
- base 初始化输入 `+0xe4/+0xe8` 为 0/0；此表的 `+0x10/+0x18` getter 分别读取这两个32位值，`+0x20` 返回 kind1。
- 同一工厂也被本轮 pass220 的 `0x318edb0`、`0x31f5dd8` 使用，它们写入低值10000。上述两个分支仅用于范围核对，未包含在新验证器的语义结论中；不能仅凭工厂或 RTTI 将任意输入认定为类型1。

## 数值1构造到服务的链

1. 留存 pass171 的 `native-fn-2920b74.c/.asm` 真实函数入口是 `0x291fb70`。它还有前置条件和其他类型分支；本轮只证明数值1分支，入口的完整输入合同尚未解释。
2. 该分支从 incoming x1+`0x18` 读取类型值并比较1；调用 `0x77bdd0` 后，在 `0x2920b74` 写 input+`0xe4`=1，将栈上 local string（sp+`0xf8`）复制至 input+`0x5c8`，将 incoming x1 起始 string 复制至 input+`0x90`。高值沿此路径保留0。`0x2920b74` 是内部 store，不能作为调用入口。
3. 输入 shared pair 保存到 x23/x22，再写入 capture source+`0x28/+0x30`。`0x268f370` 返回的另一组 pair 非空后，复制至 capture source+`0x58/+0x60`，随后调用 `0x292d868` 构造 erased body 并提交 `0x453cce8`。
4. `0x292d868` 分配 `0x70` 字节并写虚表 `0x9db3978`；将输入 pair 移到 body+`0x30/+0x38`、服务 pair 移到 body+`0x60/+0x68`，清空源 pair。不是仅向异步作业借用局部 pair 的地址。
5. 原始 dyld 链独立解码该 body 的 invoke 槽 `0x9db39a8` → `0x292ef9c`。invoke 复制输入 pair 至栈，以 x0=body+`0x60` 的指针值、x1=输入 pair 副本地址、隐藏 x8=result 调用 `0x317ded4`。
6. `0x317ded4` 保留同一输入 pair，以第三参数 w2=1 转发至 `0x317df64`。这个1是 context 构造 flag，与 input+`0xe4` 的消息类型是不同参数。后者构造保留 input pair 的 context，经 `0x3181628/0x3182084` 入队和派发，合同见 forward-queue 结果。

## 与已证明文本路径的组合

此输入的 low/high/kind 为1/0/1；已有实际服务注册表合同将低类型1查为 TextMessageHandler。文本准备阶段接受同一 RTTI，并把 input+`0x5c8` 复制至 context record+`0x130`；文本 producer 从该 record 字符串生成 wire field2。前轮 producer-dispatch 合同已连接第二队列、precheck 和 handler+`0xd8` 的文本生产函数。

这是带门条件的静态组合。准备阶段会返回错误或替换 record；不能据复制偏移断言替换后总保持同一正文。输入+`0x90`、入口参数及 capture string 的完整业务身份尚未确认，不把它们直接命名成可供外部调用的收件人参数。

## 验证及未完成项

验证器 `Library/ai/verify_wechat_text_input_path_20261016.py` 只读冻结文件，独占创建 `newsendmsg-text-input-path-verification.json`（已生成，重复执行不覆盖）。本轮12份导出3467条指令/13868字节匹配、75个关键位置和6个dyld槽核验通过，Ruff通过；四份依赖合同及账号停止记录哈希未变化。完整导出字节匹配不等于全部函数语义已证明，语义范围仅为本报告引用的路径。

新合同：`newsendmsg-text-input-path-contract.json`。剩余项：builder参数来源与完整前置条件、收件人方向、record替换后的关联、真实线程/group/config、取消组合和最终回调排空、完整可执行适配及独立送达。A7和实施20～24保持未完成，产品拒绝门不变；不得把本报告作为实机操作或发送授权。
