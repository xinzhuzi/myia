# 记录构造与类型两半布局核验

本轮继续遵守账号安全停止约束，仅分析冻结薄片及已有 Ghidra 工程。未执行微信、LLDB、debugserver、界面或账号操作；没有修改产品或真实版本配方。

## 已核验的构造侧关联

`text-contract-pass158/native-fn-30ef9e0.asm`：构造context并写入虚表 `0x9de9528`，调用 `0x30efce4`，随后把其隐藏x8返回的shared句柄转入context+0x18/+0x20。`0x30f27e4`还会重新调用该factory并替换相同位置，不能假定这个记录句柄永不变化。

`text-contract-pass157/native-fn-30efce4.asm`：分配包含shared control的0x290字节，将+0x18作为0x278字节record，清零后调用 `0xac6038`。后者在既有pass126明确写入record虚表 `0x9eb04f0`，与数据库binding记录构造一致。factory初始将账号vslot+0x28返回string复制到record+0x18，将输入对象+0x90的string复制到record+0x30；账号getter的最终业务名称和这些字段的发送方向仍未完全证明。

既有producer `0x30bda14` 从x1指向的context句柄中，读取同样的record shared pair +0x18/+0x20后构造wire。以上证明了构造侧的具体记录类型和生产侧的访问形状；尚未追完context从构造到该producer的实际派发链，因此不能声称完整同类型/调用路径已经闭环。

## local_type的64位组成

原始指令提供了两个不同setter：

| 入口 | 写入 | 随后的持久字段同步 |
| --- | --- | --- |
| `0x4cbbd20` | record+0xc的低32位 | 从+0xc读取完整64位，写入+0x108 |
| `0x4cbcfd4` | record+0x10的高32位 | 从+0xc读取完整64位，写入+0x108 |

结合既有binding将+0x108注册为local_type，冻结little-endian布局是 `uint64(high)<<32 | uint32(low)`。producer的field3只执行 `ldr w8,[record,#0xc]`，写入条目+0x18；不会把64位local_type整体当成该32位wire字段。

`0x30efce4` 在 `0x30f0f1c..0x30f0f4c` 从context+8输入对象分别调用vslot+0x10和+0x18，将两个返回值交给上述两个setter。这是两个独立32位来源的直接证据。高半的业务名称仍未证明，不能命名为已确认的子类型或状态。

`0x3107930` 虽然调用低半setter写入1，但它同时复制另一条记录并调用发送者选择/设置相关helper。没有独立证据证明它就是普通文本的正常入口；本轮明确不将其转换为“普通文本type已确认为1”。

## 证据及边界

`newsendmsg-record-input-verification.json`：13份定点导出共4903条指令与完整哈希匹配的薄片一致，21个关键指令位置通过；4轮新增Ghidra运行均readOnly/noanalysis、退出0。新Python验证脚本Ruff通过。该核验只证明静态存储和构造事实，没有运行任何导出的原生函数。

新合同见 `newsendmsg-record-input-contract.json`；上一轮中央研究JSON及客户端标识验证保留原样，哈希未改变。未提供可执行地址加载器，`runtime_observed=false`、`callable_for_send=false`。仍缺完整派发关联、普通文本输入与方向、调度/排空、完整适配及独立回执；A7和实施20～24保持开放，不恢复微信验证。
