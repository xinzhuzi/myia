# chat_id 到请求字段1的条件数据流（2026-10-17）

本轮只读取冻结4.1.15(270135) ARM64文件和已有Ghidra工程，不运行微信、不访问账号、不附加、不发送。不能据此启用产品。

## 新确认的连接

- 上轮 `newsendmsg-builder-json-contract.json` 已确认解析 `chat_id` 进入 input+0x90。
- `text-contract-pass157/native-fn-30efce4.asm` 的 0x30efd18 取得 context+8 的 input；0x30efd50 保存分配基址，0x30efd64 确立 record=allocation+0x18。0x30efd9c～0x30efda8 把 input+0x90 复制到 allocation+0x48，即 **record+0x30**。另一条 service virtual+0x28 的字符串写入 allocation+0x30，即 record+0x18；本轮未确认该服务字符串的业务名称。
- `text-contract-pass204/native-fn-30f1d74.asm` 的真实输入是 x0/context、隐藏x8/返回字符串。普通分支复制 record+0x30；record为空时输出空串。不得照抄Ghidra显示的普通输出参数。
- 特殊分支先以 `0x4cbd624(record)` 所选字符串调用 `0x4bb4a4c`。新导出pass245/246证明后者通过0x66881c4检查后缀 **@qy_u / @qy_g**。原始常量0x8ac3920为 `@qy_`，末尾分别来自0x75/0x67和终止零。辅助对象 record+0x230 存在时，改取该对象+0x98所指对象的+0x78字符串；否则回到record+0x30。
- 0x4cbd624对低类型非10000的记录：record+0x18非空且等于上述服务字符串时选择record+0x30，否则选择record+0x18；类型10000另有比较分支。因此不得只检查chat_id后缀就概括整个特殊条件。
- `text-contract-pass203/native-fn-3107b0c.asm` 的0x3107b78取得该结果，结果含 **@weclaw** 时转往0x2849004；其他情况才走普通newsendmsg分支。在普通分支，0x3108640～0x3108644把同一结果复制入条目字段1的字符串包装。

## 证明边界

已经补上“解析chat_id→初始record+0x30→条件getter→普通请求字段1”的静态连接；**尚未证明任意记录替换/外部修改后仍保持同一值，也未证明所有路由、服务字符串业务身份及特殊分支的最终收件人语义**。不把这条条件连接表述为完整收件人方向已终验。

`Library/ai/verify_wechat_recipient_route_20261017.py` 核对8份导出4068条指令、48处关键位置、精确常量及前置合同哈希；Ruff通过。验证器只比较冻结字节与导出并保存来源，不执行反汇编函数；验证报告为 `newsendmsg-recipient-route-verification.json`。

A7及实施20～24继续开放，产品拒绝门保持；完整未完成项见 `completion-gap-audit-20261017.md`。
