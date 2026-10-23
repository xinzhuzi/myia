# 内嵌MessagePackedInfo与名称回退（2026-10-18，实施62）

仅使用冻结4.1.15 (270135) ARM64文件、留存Ghidra工程和系统LLVM；未加载/执行目标代码，未运行/附加/操作微信，没有发送、产品接线或部署。账号安全停止约束保持。

## 本轮关闭的具体问题

record+0x198、+0x19c不再只是无类型偏移：record构造器 `0xac6038` 在record+0x190调用 `0x4ea6ba0`，后者安装虚表0x9ec4228。+0x10槽独立dyld解码至 `0x4eb03b0`；六份原始常量片段和末尾立即数重建出的精确类型名为 **micromsg.MessagePackedInfo**。类型名string实际经隐藏x8返回。

其字段1为wire type0、32位值、metadata+8即record+0x198；字段2为wire type0、32位值、metadata+0xc即record+0x19c。存在掩码为metadata+0x74（record+0x204）的bit0/bit1。解析和序列化两边均核对，字段顺序另由实际跳转表0x8af1c40的前两字节00/21独立算出，未照抄Ghidra switch。

与既有插入和查询链相连：`0x32961a4` 把record+0x18/+0x30两份string映射为编号，分别写这两个位置并置存在位；实施61的查询链再通过Name2Id反查并替换这两份string。**这证明双向存储关系，不证明哪份string是当前账号或最终收件人**。账户子对象身份和上游输入方向仍缺，不能据此补成“完整业务映射”。

## 解析失败并非事务回滚

通用入口 `0x5ab3ab8` 先调用message虚槽+0x20清理，再调用+0x40合并输入，成功后检查+0x28；该具体类型的+0x28恒返回1，不要求字段1/2存在。最后还要求输入context+0x24的bit0。长度参数w2在计算end时用SXTW，不能把前置指针差截断后宣称整个长度域均有效。

实际parser直接写metadata字段，后续字段失败可返回0，没有还原之前写入。`0x4cbfafc` 仅在成功时清空并释放原byte vector；失败保留vector，没有向 `0x3280514` 传播可分支检查的错误状态。后者调用后直接收集当前编号并继续名称映射。因此不能假设失败时record保持旧值、失败时已有编号仍完整，或后续更新一定被阻止。此处为静态控制流结论，没有构造微信实机失败输入。

`0x4cbfb58` 反向对metadata计算大小、调整vector后，tail-call至 `0x5ab3f98 ->0x5ab3f9c`。由虚槽+0x58到 `0x5ab3bc0`，后者再经+0x50调用 `0x4eafbbc`；前两位存在标志决定字段1/2的varint写入。没有把+0x38的merge thunk误当作序列化器。完整嵌套schema及未知字段保持仍不在本轮证明范围。

## 第三个名称字段的正文前缀回退

实施61尚未展开的 `0x4cbd8fc` 已核对：实际x0=record、隐藏x8=owned string。只有record+0x18/+0x30任一含 `@chatroom` 或 `@im.chatroom`，且低类型不等于10000，才尝试正文record+0x130的分隔符；其他情况返回空string。

普通分支查找精确两字节 **3a0a（冒号+LF）**，有值则复制此前缀；低类型11000且高类型124时改用 **3a20（冒号+空格）**。无分隔符返回空值；record+0x258仅控制诊断分支，不改变回退结果。这是受类型和会话条件约束的取值，不能对所有正文无条件split，也不能据前缀存在断言发送人身份。

## 导出缺口与验证范围

Ghidra对parser的伪代码展开较多，但指令导出只有62条，遗漏两段：0x4eaef6c～0x4eaf044、0x4eaf05c～0x4eafb90（均为右开区间）。没有用这份稀疏列表冒充完整parser。

冻结Mach-O compact unwind独立给出完整范围 **0x4eaeeb8～0x4eafbbc**。新增 `Library/ai/export_wechat_packed_info_20261018.py` 用系统llvm-objdump导出全部833条连续指令，再逐条与冻结字节比对；输出在 `packed-info-parser-20261018/`。没有改动Ghidra数据库，也没有对目标执行代码。

合同 `newsendmsg-packed-info-contract.json`，验证器 `Library/ai/verify_wechat_packed_info_20261018.py`，最终证据 `packed-info-20261018-verification.json`：17份Ghidra导出2112条指令，LLVM完整parser833条，重合去重后共 **2883个位置**；261处合同位置、35条独立分支目标、7个dyld槽、7份字面量片段、类型名和跳转表目标核验通过。两个新Python脚本Ruff通过。

这些检查证明冻结文件及所述路径的一致性，不是运行时观察。完整parser覆盖不等于完整解释14个字段及嵌套消息；本轮仅声明前两个编号的字段语义、解析失败边界和指定名称回退。仍缺上游方向/账户身份、其余metadata及服务更新、真实执行线程与取消最终释放、完整原生适配、真正发送和独立回执。A7及实施20～24、55保持未完成。
