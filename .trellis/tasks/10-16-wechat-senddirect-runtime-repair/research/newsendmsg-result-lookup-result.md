# 发送作业返回值与本地记录查询边界（2026-10-18，实施60）

本轮只处理冻结的4.1.15 (270135) ARM64文件，未运行、附加或操作微信。账号安全停止约束继续生效，未接线、部署或发送。此证据补齐一段业务返回映射，不是独立回执实现。

## 可直接约束后续适配的结论

发送作业 `0x292ef9c` 首先以 body+0x60 的服务、body+0x30/+0x38 的输入shared pair调用 `0x317ded4`，输出通过隐藏x8写到sp+0x310。只有此结果开头的两个32位数均为0，才进入当前成功分支。该条件只是服务结果检查，不能证明送达。

接着 `0x86e43c` 将结果中指针所指的可选值复制到sp+0x2a0。可选值大小边界：+0及+0x28两份24字节string，中间+0x18有16字节标量区域，+0x40字节恰为1才有值。本轮只命名下游实际使用且已追到用途的两项：+0x1c是local_id，+0x18是存储选择值；其上游生产与剩余区域语义仍缺。不能把选择值当消息类型。

`0x3190538` 的真实ABI为 **x0=service、x1=chat_id string、w2=local_id、w3=存储选择值、隐藏x8=可选record输出**。Ghidra把隐藏返回区排成普通第一个参数，且在内层调用中丢失仍存活的输入参数；不得照其伪代码声明接线。调用点见 `text-contract-pass220/native-fn-292ef9c.asm:259`，入口保存见 `text-contract-pass291/native-fn-3190538.asm:8`。

## 返回记录从哪里来

`0x3190538` 从service+0xb78取对象，转交相同chat_id与两个数值给 `0x32f26b8`，通过隐藏x8得到future；等待 `0x66856fc` 后用 `0x303fe7c` 取可选record。

`0x32f26b8` 先要求非空chat_id及两个非零数值。`0x3289264(chat_id)` 产生1/2的分类值；`0x3bda648` 同时使用此分类和传入的存储选择值，1/2两分支分别通过不同helper取得对象，再dynamic_cast到共同类型；不能把两个不同来源的数值合并成一个type字段。空对象或输入不合格时由 `0x335fcb0` 返回已经结算的无值future。

非空对象路径创建自有capture：chat_id在+0x28，local_id在+0x40，存储shared pair在+0x48/+0x50，completion pair在+0x58/+0x60。`0x33677c4` 移走存储pair，初始化0x278字节record，然后调用 `0x3273830(storage,record,chat_id,local_id,1)`；返回布尔决定发布有值还是无值。提交helper为 `0x3c17870`；本轮没有证明其执行线程或排空。

`0x3273830` 构造function并交给 `0x3aeddb4`，其invoke槽+0x30独立dyld解码到 `0x32aab0c`。该invoke用chat_id调用 `0x30251cc` 获取表字符串，以record binding `0x4cbaf80` 和偏移 **0xf4（既有独立binding证据的local_id）**构造表达式，并把捕获的local_id交给值转换/表达式helper，随后通过存储+8调用 `0x328714c` 查询。查询结果有值才移动record到调用者输出；flag为1时还要求 `0x3280514(storage,output)` bit0为1才返回成功。输出移动发生在这个附加检查之前，失败不能推广为“从未得到记录”。完整比较器和此附加helper的业务语义仍未证明。

发布器 `0x335fdd8` 把可选record放入holder+8，holder虚表0x9df3c00的+0x18槽为 `0x3360070`，后者返回RTTI0x9df3500；RTTI+8独立dyld解码到高位标记指针0x80000000088cfaa4，掩码后读出的精确名称为 `_671c1c9e`，与getter `0x303fe7c` 比较的名称相同。由此把查询发布端与消费端的值类型连上，没有沿用Ghidra的模糊类型。

## 查询之后仍有副作用，不能当独立送达观察

有值时 `0x3190538` 先通过 `0x3025b60` 建记录vector，交给 `0x31b5470(service,chat_id,vector)`，然后才把第一条record移入隐藏返回区并设置+0x278存在标志。后续原调用者在存在位成立时读取record+0xf8（既有binding证据为server_id）。`0x31b5470` 还调用多项更新/通知helper，其完整业务语义未证明，不能省略或声称纯查询。

没有值时 `0x3190538` 写输出首字节及+0x278为0。本地查询miss不是远端发送失败证明；同样，本地命中、server_id非零、future就绪或高层completion结算都不能自动标记sent=true。当前响应解析器仍保持sent=false，本轮没有为了研究进展新增冗余发送包装或修改产品逻辑。

## 验证与剩余

机器合同 `newsendmsg-result-lookup-contract.json`，验证器 `Library/ai/verify_wechat_result_lookup_20261018.py`。14份选择导出共 **2948条指令**逐字节匹配冻结薄片，126个关键位置、24个B/BL目标独立立即数解码、3个dyld槽及精确类型名称核验通过；Ruff通过。结果为 `result-lookup-20261018-verification.json`。未重新执行历史实机检查或把导出一致性当运行证明。

已关闭这条选定返回路线的真实ABI、两个标量的下游用途、查询发布/消费类型关联以及本地记录来源的不确定性。仍缺上游完整返回值生产、完整查询/更新语义、原extra string身份、全部业务字段/记录变更、真实调度与取消/最终释放、完整原生适配和独立回执。A7及实施20～24、55继续开放；账号停止约束保持。

## 同轮追加核验：表名、记录替换与最终证据

前述初版14导出的合同保存在 `newsendmsg-result-lookup-contract-initial.json`，对应初版验证JSON仍保留。当前权威合同为同名无initial后缀的JSON，最终证据为 **result-lookup-20261018-v2-verification.json**：18导出 **3623指令、166位置、37个独立B/BL目标、3个dyld槽**及Ruff通过；初版数字不作为当前合同的完整验证范围。

新增四个helper的核验补出：`0x30251cc` 用原始字面量 **Msg_** 加 `0x6686dd8(chat_id)` 返回string形成表字符串，x0输入、隐藏x8返回，后缀helper语义仍未展开；不能仅凭既有版本经验宣称已证明其完整算法。

查询附加步骤 `0x3280514` 不是纯布尔检查：先调用 `0x4cbfafc(record)`，收集record+0x198、+0x19c、+0x110三个32位键，再由 `0x3aef3f8(storage,set,map)` 提供映射。成功分支通过 `0x3026804` 查键，按结果+0x18字符串分别**替换record+0x18与+0x30**；第三键的字符串交给 `0x4cbb728`，之后调用 `0x4cbf804`。因此不能把构造时的收件人string一路原样保留作为已证明事实。映射表的实际来源、预处理/第三字段setter及全部异常语义仍需核验。

`0x56c9dac` 有特殊空值分支（tag5）和普通分支（tag0xf→0x56c9b48）；尚未证明完整SQL比较器渲染，不写出假定等号SQL。查询helper `0x328714c` 也通过隐藏x8返回可选record，实际普通参数是x0～x4；再次排除把Ghidra显示的输出缓冲区当成普通x0参数的错误。

追加验证第一次因手工把BL位置0x32806d4记为非分支指令0x32806d0而被验证器拒绝；对照原始指令纠正后通过。错误未进入运行配方，没有微信操作。最终合同仍明确send_verified=false、callable_for_send=false、deployed=false；A7及20～24、55未完成。
