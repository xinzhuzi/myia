# JSON 参数到类型 1 输入：离线证据

冻结 ARM64 4.1.15 (270135)，SHA256 `6a5bd0cbb39ad3092c15e9debda2db4969eedf1b58caad244d88033a996833a7`。本轮仅使用留存二进制及只读 Ghidra 工程，没有操作微信、调用原生函数、发送或处理账号。账号停止约束继续有效。

## 已确认字段及流向

| 精确 JSON 字段 | 解析结果偏移 | 本条类型 1 路线中的用途 |
|---|---|---|
| `chat_id` | `+0x0` string | 复制到 input `+0x90`，之后 context 构造器复制到 context `+0x38` |
| `message_type` | `+0x18` uint32 | 值为 1 时进入已证明的文本构造分支，设置 input `+0xe4=1` |
| `content_xml_base64` | `+0x20` string，直接内容 flag 为 0 | 非空字符串优先选中；builder 经 `0x206bc` 转换成功后形成正文 |
| `content_xml` | `+0x20` string，直接内容 flag 为 1 | 前一字段未选中时的非空字符串回退；直接复制形成正文 |

字段名称不是根据旧版协议推测：`chat_id` 来自冻结地址 `0x8585938`；`message_type` 由 `0x866d0f8` 的 8 字节和 `0x8489788` 的 4 字节组合；`content_xml_base64` 由 `0x8824cb0` 的 16 字节和立即数尾部 `36 34 00` 组合；`content_xml` 由 `0x84f26e0` 的 8 字节和 `0x8572320` 的 4 字节组合。验证脚本逐项核对这些字节及对应加载位置。

解析器要求 `chat_id` 是非空 tag3 string。`message_type` 支持 tag5/6 经 `0xbbfa44` 的数值路线和 tag3 string 的另一转换路线；完整数值转换语义未证明。表中字段只是当前解析器的部分已审阅输入，不能据此宣称完整 schema 已确定，也不能断言 `content_xml` 一定含合法 XML。

## 调用与 ABI

`0x286fbac` 对传入的 x1 string 调用 `0x74916c`，在其分支中进入 `0x291d53c`。后者将 JSON value 通过 x1、完成对象地址通过 x2 交给 `0x291dab8`，输出通过隐藏 x8。Ghidra 列出的普通参数不能替代原始寄存器合同。

解析成功标记为输出 `+0x48`；`0x291d53c` 要求它恰为 1，再把输出地址作为 x1 交给 `0x291fb70`。协调器原 x2 仍作为 builder x2 传递，它不是解析后的 `chat_id`；该字符串的业务身份仍需追踪。builder x3 是拥有的完成对象地址。

builder 先要求 `0x2ab6388` 返回非空对象。直接内容 flag `+0x40==1` 时，把解析对象 `+0x20` 复制到局部 `sp+0xf8`；否则调用 `0x206bc`。该 helper 调用 `0xabf6c`，返回 `UINT64_MAX` 表示失败，成功才转移输出 string；底层 codec 的完整语义本轮未证明。特殊内容分流先于数值类型分支，不能绕过它们推定任意输入都走类型 1。

数值类型 1 在 `0x2920b68` 调用工厂 `0x77bdd0`，设置低类型 1，然后把局部正文复制到 input `+0x5c8`，将解析对象起始的 `chat_id` string 复制到 input `+0x90`。该 input 到文本 handler/producer 的条件关联已在 `newsendmsg-text-input-path-contract.json` 建立。

## 核验与完成边界

`Library/ai/verify_wechat_builder_json_20261016.py` 对 8 份导出逐条比对冻结文件，共 5320 条指令、65 个关键位置及 4 个精确字段；前序合同及停止记录哈希一致，Ruff 通过。结果见 `newsendmsg-builder-json-verification.json`。这些检查验证冻结证据与已审阅的条件链，不能替代微信运行或真实回执。

仍缺上游路线完整身份、可选 subtype 及错误语义、`chat_id` 经 record 到最终请求的收件人方向、所有记录变更、真实线程/config、取消组合与排空、完整适配及独立送达回执。A7 及实施 20～24 保持未完成。新合同只落 research；不改产品版本 JSON 的禁用状态、不装机、不恢复活体操作或申请新观察窗口。
