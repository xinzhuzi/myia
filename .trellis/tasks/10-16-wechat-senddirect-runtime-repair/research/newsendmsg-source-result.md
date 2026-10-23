# source 重建、调用 ABI 与请求字段6（2026-10-18）

仅分析冻结的 WeChat ARM64 4.1.15 (270135)，SHA256 `6a5bd0cbb39ad3092c15e9debda2db4969eedf1b58caad244d88033a996833a7`。没有运行、附加或操作微信。账号停止记录继续有效，没有产品接线或部署。

## 可用于后续适配的修正

`0x32961a4` 调用 `0x4cbf820` 后再更新 metadata。前者只有在 record+0x240 恰为1时，才经过 record+0x220 的可选虚调用并转入 `0x4cbf994`。因此 source 重建有条件；既有辅助对象的虚实现仍不可忽略。

`0x4cbf994` 复用 record+0x230 的对象；为空时建立0x128字节shared分配，其中+0x18开始的0x110字节对象清零，pair写回record+0x230/+0x238。它把 `0x4d1dd74` 的返回string赋给 record+0x160，再销毁临时string。这一支覆盖旧source，而不是保持原source原文。

原生调用ABI是 **x0=辅助对象、隐藏x8=24字节string返回区**。Ghidra伪代码将返回区显示为param_1、输入显示为param_2；不能据此实现两个普通参数。原始证据：`text-contract-pass231/native-fn-4cbf994.asm:47`；`text-contract-pass287/native-fn-4d1dd74.asm:8`。

## 顶层 source 字段

`0x4d1dd74` 建立名为 `msgsource` 的节点；下表名称逐项从冻结文件的字面量或其解密规则核对。相同偏移均相对source辅助对象，不是record。

| XML节点 | 偏移 | 生成条件 / 值 |
| --- | --- | --- |
| atuserlist | +0x18 | 非空string |
| img_file_name | +0x30 | 非空string |
| alnode | +0x48 | 非空嵌套对象；交0x4d1b7e4 |
| sec_msg_node | +0x58 | 非空嵌套对象；交0x4d1b8f4 |
| share_msg | +0x68 | 非空嵌套对象；交0x4d1bbcc |
| passthrough | +0x78 | 对象非空则建节点；首个string非空才写sec-hash子节点 |
| tmp_node | +0x88 | 非空嵌套对象；交0x4d1bd38 |
| enterprise_info | +0x98 | 非空嵌套对象；交0x4d1bf44 |
| strid | +0x0 | 非空string |
| shareCardMessageStatus | +0xb8 | 非零int32 |
| teenagerModeApplyAgree | +0xcc | 字节恰为1 |
| teenagerModeHasBindGuardianRelationship | +0xcd | 字节恰为1 |
| scene | +0xbc | 非零int32 |
| bizflag | +0xc0 | 非零uint32 |
| msg_cluster_type | +0xc4 | +0xc8存在字节恰为1；值为0仍有节点 |
| kefumenuid | +0xd0 | 非空string |
| greeting_flag | +0x108 | 字节恰为1 |
| msg_wording | +0xa8 | 非空嵌套对象；交0x4d1ecdc |

字符串文本setter `0x5720378` 调用strlen，所以这些文本入口按NUL终止，不能用任意字节片段代替。int32 setter `0x57203c8` 有符号处理；bizflag使用 `0x57204a4` 的uint32路径，不能统一按有符号整数格式化。节点/文本分配可能失败，未据此保证任意内存条件下输出完整。

序列化调用 `0x571fc9c(document,stream,empty_indent,4,0,0)` 后取stream string。当前没有完整验证转义、声明、空节点格式等精确输出字节，不能直接手工生成一个XML字符串当作原生等价物。嵌套对象的完整内部字段也未全部核验。

## 进入请求的路线及另一种 metadata

普通newsendmsg producer `0x3107b0c` 检查 **最终 record+0x160** 的string长度：短string用+0x177字节，长string用+0x168机器字。非空才设置条目+0x34的presence bit0x20，并复制到条目+0x20所指string，即已证明的wire字段6；空时不设置该字段。此处是string赋值而不是strlen，不能把上游文本setter的截断语义套到整个最终source复制。

来源：`text-contract-pass203/native-fn-3107b0c.asm:740`、`:752`、`:763`；原有字段6编号/类型证据仍以 `newsendmsg-4115-static-contract.json` 为准，本轮没有改写原报告或其哈希。

`0x4cbfb58` 则对 **record+0x190** 求序列化大小、调整 **+0x178/+0x180/+0x188 byte vector** 并写入。这不是source string，不能把该vector当成请求字段6，也不能省略source重建直接使用输入旧值。

## 新合同与核验范围

机器可读补充：`newsendmsg-source-contract.json`。验证器 `Library/ai/verify_wechat_source_mapping_20261018.py` 对15份选择导出逐字节核验 **3636条指令**，定点检查68位置，独立解码13条B/BL目标，并重建根节点及18顶层字段名；Ruff通过。结果：`source-mapping-20261018-verification.json`。这是冻结文件一致性与控制流证据，不是真实执行或送达证据。

调查期间曾把document构造目标 `0x572111c` 手工抄成 `0x571111c`，pass288相应导出是无关函数；用冻结BL立即数独立解码发现后，在pass289导出正确目标。无关导出保留但明确排除在合同与验证证据之外，不根据它作任何source结论。

本切片关闭source的顶层输入、重建ABI、record赋值与字段6条件复制这一段的不确定性。它没有关闭：嵌套source语义和精确输出、既有辅助对象/完整记录修改与lookup、builder参数来源、真实线程/取消/全部排空、完整适配器或独立回执。A7、实施20～24和55继续开放；不操作微信、不申请窗口、不部署。
