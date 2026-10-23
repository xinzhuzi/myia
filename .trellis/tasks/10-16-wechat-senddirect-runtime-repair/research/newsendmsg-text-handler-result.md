# 文本handler身份与正文进入请求的静态关联

仅处理留存文件：没有附加/调用/发送、没有微信界面/账号操作，没有改产品、实际配方JSON或安装件。账号安全停止约束保持，A7仍未完成。

## 改变下一步的身份发现

此前已知`0x9de7f68`并非文本handler。pass140的初始化函数`0x30e3fb0`在`0x30e5bbc`起从五处只读数据低32位拼装名称，再追加`er\0`，实际为`LocationMessageHandler`；随后调用`0x30eccc4`创建该虚表对象并以此名插入表。它的producer`0x30bda14`可以作为共用wire编码证据，但不能据此解释普通文本的业务准备。

初始化函数开头另一链为`0x30e74f4 -> 0x30e7aa0 -> 0x30e7be8`。pass202名称helper读取`0x88b0090`的16字节并追加`er\0`，得到精确`TextMessageHandler`；工厂分配`0x398`、payload在+0x18，经基础构造后写虚表`0x9de9a68`。初始化函数随后把整数1转为string，与同一名称交给映射插入helper`0x30e7fd4`。后者尚未独立导出；实际服务容器中的注册/选择完整关联仍需证明。

## 正文准备与请求生产

独立dyld链解码文本虚表：+0x78=`0x3105a98`，+0xd8=`0x3107b0c`，+0xe0=`0x31099b8`。+0x80/+0x88/+0x90仍是此前已证的默认阶段方法，不能由这些零结果方法替代producer。

pass203的准备函数`0x3105a98`先调用handler+0xe0验证record及输入动态类型；专门分支将input+0x5c8的string复制到context record+0x130，清record+0x258字节，再进入`0x30db798`。后者可能复制/加载并替换context record，因此这是准备阶段直接关联，尚不能省略下游身份与调度证明。原始ABI为x0/handler、x1/context shared pair地址、隐藏x8/result，不能照抄Ghidra参数列表。

文本producer`0x3107b0c`也使用上述ABI，从context+0x18/+0x20取record。非替代路线构建条目时，正文读取record+0x130、类型读取+0xc低32位、时间读取+0x114，客户端标识沿`0x30f2168 -> 0x33fcc`，可选source读取+0x160，然后调用共享请求helper`0x30bee20`。field1来自`0x30f1d74(context)`：普通后备分支复制record+0x30，另有谓词控制的嵌套对象string分支，尚不能把所有情况统一命名为收件人。producer开头还有`0x4bb6cd4`判定后转向`0x2849004`的替代路线。

响应分支在外层两个错误字为零、响应条目非空且首条错误为零时，把record+0x118设为2，将响应条目+0x28写入record+0xf8。此处仅为静态条件和写入顺序，未观察实际成功，更不构成独立送达回执。

## 两条通知容器

pass200的`0x30d00d0`/`0x30d0a14`均从signalslot容器取得节点。节点executor为空时直接调用节点函数；非空则复制record，构建拥有record副本的function对象，交给executor虚槽+0x10。普通wrapper分配0x2d8、record位于+0x60，invoke为`0x30dcaf4`；带flags者分配0x2e0，flags位于+0x60、record位于+0x68，invoke为`0x30dcee4`。实际订阅节点及执行器身份仍缺，不能据调用返回认定排空或卸载安全。

## 本轮验证及剩余

`Library/ai/verify_wechat_text_handler_20261016.py`核验19份导出7494条指令、66个关键位置、9个虚表槽及两个精确名称，新脚本Ruff通过。合同和证据分别见`newsendmsg-text-handler-contract.json`与`newsendmsg-text-handler-verification.json`。大型初始化函数/producer只解释上述切片，全文字节匹配不等于完整语义审查。RTTI继承也未由当前限定rebase解码器完整证明，不把同offset输入视作同类型。

下一离线目标：将service+b20的数值/名称表与这份初始化表建立直接关系，追出到文本producer+0xd8的真实派发，并继续核验正文输入类型、方向、调度线程/config及末尾排空。真正发送、独立回执、产品接线仍未完成，不安排活体测试。
