# 类型1与正文转换：离线证据及边界

本切片只读取冻结的4.1.15(270135) ARM64文件和留存Ghidra工程，没有运行、附加或操作微信。账号安全停止约束保持，产品和安装件未修改，A7未完成。

## 已核实

- 基础构造器`0x69a714`在payload+0xe0写8字节零（覆盖+0xe4），并将+0xe8写零。因此基础默认类型不是1；+0x7c另设1，不能混为类型字段。
- 转换器真实入口为`0x4c6eff4`，`0x4c6f030`是函数内写入指令地址，不能当作函数入口。原始指令保存x1为source shared handle，保存隐藏x8为返回存储；Ghidra把隐藏返回显示成普通参数，不能照抄其声明。
- 该转换器调用`0x4c6f204`，经`0x4c6f2c4`分配0x658字节容器，payload位于容器+0x18，虚表为`0x9eb2bb8`。工厂也通过隐藏x8写回16字节shared pair。
- 转换器明确写payload+0xe4=1，并将source+0x130字符串复制到payload+0x5c8、source+0x148字符串复制到payload+0x5e0。前两个source偏移与已建立record绑定中的message_content/compress_content一致；本切片没有证明完整发送链中source的同类型身份，不能把偏移一致扩大成完整业务关联。
- `0x4c6c5d0`实际使用x1/source shared handle和x2/payload shared handle：source+0x350复制到payload+0x178，payload+0x7c设2。+0x350业务含义未定，+0x7c不是低类型字段。
- 独立dyld链解码确认新payload虚表+0x10/+0x18/+0x20分别指向读取+0xe4、读取+0xe8、恒返回1的三个不同getter。数据位置`0x9eacf50`指向真实转换器入口，但其所属对象及正常发送时的调用关系仍未证明。

## 验证范围

`newsendmsg-type-one-content-verification.json`核对6份精确导出的232条指令与冻结原始字节、32个关键指令位置和4个dyld槽。新验证器与之前的类型1指令模式扫描脚本均通过Ruff。扫描所得32个位置仅是指令模式命中，不是32条业务发送路径；不据其余未阅读分支作结论。

相关文件：`newsendmsg-type-one-content-contract.json`、`Library/ai/verify_wechat_type_one_content_20261016.py`；导出为pass167、pass171、pass172、pass173及已有pass166中的单个getter。pass168～170的联络记录分支与pass171大型函数只作定位，不纳入本切片语义结论或验证计数。

## 还缺什么

本证据证明了一个“低类型1＋正文偏移复制”的转换路径，没有证明普通文本完整发送入口。还缺转换器所属对象、到context/producer的正向派发、同类型身份和收件人方向、真实group/config/线程与末尾引用排空、完整可执行适配及独立发送回执。可执行配方继续拒绝；本切片不恢复调试窗口、UI、发送、登录或装机。

## 后续归属核验（pass174～182）

已追到该方法属于选择值49/115转换对象的+0x18槽，选择函数实际调用另一个+0x10槽；数值1使用不同转换对象。新公共工厂输出类型的虚表为0x9eba160，与已确认数据库record的0x9eb04f0不同。因此本报告中的成员偏移交叉引用继续只作偏移比较，不能赋予source数据库身份或视作普通文本发送证明。详见`newsendmsg-conversion-dispatch-result.md`与合同/验证JSON；产品拒绝门和账号安全停止约束保持。
