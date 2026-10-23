# 本地记录编号回填与辅助对象：离线核验

范围仅为冻结的 WeChat ARM64 4.1.15 (270135)，SHA256 `6a5bd0cbb39ad3092c15e9debda2db4969eedf1b58caad244d88033a996833a7`。本轮没有执行或操作微信，没有运行调试器。账号停止约束继续以 `account-safety-stop-20261016.md` 为准。

## 本地编号来源

正常插入回调 `0x335c1b4 → 0x326a144` 创建 erased function，虚表槽 `0x9df1bc0` 解码到 `0x32961a4`。其捕获包括原 record 地址、映射表地址、flag 地址、选中字符串地址及 service。回调写入映射结果、flag，调用准备 helper，然后通过 `0x2e86b60` 用复制构造 `0xf57630` 建立 record vector。

`0x3296b1c` 使用模式 2；单条路径经 `0x32970cc → 0x32973c8 → 0x32979e0`。最后一项调用 `0x56f4db0`，结果 bit0 成功后，将 `0x56f90e0` 返回值写入 vector record 的 `+0x208` 所指单元。构造器 `0xac6038` 原先创建值为零的 shared 整数单元；复制构造保存同一 `+0x208/+0x210` pair 并增加引用计数，因此原记录读到该结果。

`0x32961a4` 只在 operation bit0 成功且捕获 flag 恰为 1 时，把该单元低 32 位写入原 record `+0xf4`。字段 binding 将此位置命名为 `local_id`，见 `newsendmsg-business-field-investigation.md`。这补齐了上一切片替换门所要求的编号来源；本地编号、operation 成功及 future 发布均不是网络发送或送达回执。

## 分支与正文边界

父方法 `0x32cf5e8` 在 server_id `+0xf8` 为零或原参数 w4 为零时直接进入正常插入分支；其他情况可进入 `0x335bfac` lookup 回调。注意 `0x32d03cc` 已用返回字节覆盖 w24，后面的 `0x32d0468/0x32d0828` 测试不能解释为原始 w4。lookup 返回零仍可进入插入，非零可发布既有记录副本；全部 lookup 分支仍未核验。

`0x4cbf820` 同步类型缓存，仅在 record `+0x240 == 1` 时准备 `+0x220` 辅助对象并调用其虚槽 `+0x10`。低类型为 1 且对象原为空时，字符串比较 `0x4a292e4` 的两种结果分别选择 `0x4cbf170` 或 `0x4cbf3c0`。两者最终虚表的 `+0x10` 分别指向 `0x4ce9cd8`、`0x4cd949c`，两方法均只有 `ret`。该结论只覆盖新建的这两类对象，不能推定既有辅助对象或整条路线保持正文。

随后 `0x4cbf994` 将 `0x4d1dd74` 的字符串输出写入 record `+0x160`（source）；`0x4cbfb58` 还序列化 metadata。不能忽略这些步骤直接复制一份 record 作为完整适配。

## 调用及验证边界

`0x3aeddb4` 克隆 function，经 `0x56f412c → 0x56462d0` 执行嵌套包装。槽 `0x9f23928 → 0x56f4b4c` 在构造局部 context 后调用被捕获 function 的 `+0x30`，再销毁局部对象。它不证明任意线程调用安全或所有任务已排空。

`Library/ai/verify_wechat_record_database_20261016.py` 对 41 份留存导出的 5978 条指令逐条比对冻结文件，检查 74 个关键位置及 4 个独立 dyld 槽，并锁定前序合同和停止记录哈希；Ruff 通过。对应 `newsendmsg-record-database-verification.json`。指令字节吻合证明导出与文件一致，语义结论另依赖上述控制流审阅，不能等同运行验证。

仍缺全部 lookup 分支、既有辅助对象身份、builder 参数来源和收件人方向、真实线程/config、取消组合与最终排空、完整适配及独立回执。A7 及实施 20～24 保持未完成；不启用产品、不装机、不申请新的观察窗口。
