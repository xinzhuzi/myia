# 文本准备中的记录替换与类型化结果（仅离线）

冻结 ARM64 4.1.15 (270135)，SHA256 `6a5bd0cbb39ad3092c15e9debda2db4969eedf1b58caad244d88033a996833a7`。
本切片没有启动、附加或操作微信，没有原生调用/发送，没有修改产品配方或安装件。账号停止约束保持；A7及实施20～24未完成。

## 已确认的替换边界

文本准备在复制正文至 `record+0x130` 后调用 `0x30db798`，但该 helper 并非只读访问原记录。
原始 ABI 是 `x0=handler,x1=context shared pair地址,隐藏x8=result`。它先构造0/0默认结果；handler的弱服务控制 `+0x368` 不存在、lock失败或 `+0x360` 为空时，不进入替换。

取得 `context+0x18/+0x20` 的记录pair后，非空分支调用 `0x32cf5ac` 生成future pair，再经 `0x30dc1e0` 提取一个新的记录副本。分配0x290字节shared块，记录位于+0x18并由 `0x2a0cf30` 移动构造。只有新记录 `uint32+0xf4!=0`，才在 `0x30db91c` 替换context中的pair并释放旧引用。
空原记录和新记录+0xf4为0分别调用 `0x30f6650`，原始参数tuple为 `(1,2,4,400)` 与 `(1,2,2,200)`；尚不给四项臆造业务名称。

来源：`text-contract-pass198/native-fn-30db798.asm:8`、`:45`、`:65`、`:88`；`text-contract-pass203/native-fn-3105a98.asm:586`。

## 结果的类型身份已对上

`0x30dc6fc` 从 `0x666a844` 结果取得容器，调用其虚槽+0x18，读取返回type对象的name指针，去除高位后比较 `_f6e3c5f5`，通过才返回容器+0x8，否则抛异常。
独立dyld链解码确认：容器虚表 `0x9df3920` 的+0x18槽是 `0x335bf80`；该方法返回 `0x9df3970`，name槽解码为 `0x80000000088aee40`，掩码后正是比较字串。

因此容器+0x280处另一个 `0x9eb0530` 指针的名称 `_e0c51525`，不能被误认为上述类型检查对象，不能据它宣称ABI类型不匹配。
`0x30dc1e0` 保留future pair，调用 `0x66856fc`、类型化getter，再用 `0xf57630` 复制到隐藏x8输出。这里并未证明任意线程可等待、全局排空或消息送达。

来源：`text-contract-pass223/native-fn-30dc6fc.asm:10`；`text-contract-pass226/native-fn-335bf80.asm:1`；`text-contract-pass222/native-fn-30dc1e0.asm:5`。指针解码留存于验证JSON。

## 复制已证明，完整内容保持尚未证明

`0xf57630` 与 `0x2a0cf30` 均安装数据库记录虚表 `0x9eb04f0`。前者对+0x130执行内联string复制或堆string深拷贝；后者转移24字节表示并清空源表示。该证据仅覆盖构造边界。

`0x32cf5e8` 中有调用 `0x335bddc` 直接复制原记录并发布容器的分支；另一个条件分支复制记录、selected string和两个shared pair到0x2e0字节callback，invoke为 `0x335c1b4`，析构为 `0x335c4ec`。
invoke先移动记录到本地，调用 `0x326a144(service,record,string,flag)`，再经 `0x335c414` 移动记录到类型化容器并传给 `0x66696dc`。不能跳过中间操作，直接把输入正文等同于最终producer正文。
`0x326a144` 会调用 `0x3269bec`（条件更新记录+0x100），并把捕获记录地址的function传给 `0x3aeddb4`。后者及其他lookup分支的修改语义尚未证明，是下一离线定位点。

来源：`text-contract-pass222/native-fn-f57630.asm:100`、`native-fn-2a0cf30.asm:96`；`text-contract-pass224/native-fn-32cf5e8.asm:1173`；`text-contract-pass225/native-fn-335c1b4.asm:29`；`text-contract-pass227/native-fn-326a144.asm:124`；`text-contract-pass228/native-fn-3269bec.asm:308`。

## 方向字段仍按原始规则记录

`0x32cf5ac` 通过 `0x4cbd624` 选择记录string。type不为10000时，`0x4cbd748` 检查非空record+0x18是否等于账号服务虚槽+0x28返回的string，相等选+0x30，不等选+0x18；10000有单独相等分支。
wire字段1的getter `0x30f1d74` 通常复制record+0x30；若selected string满足 `0x4bb4a4c` 且record+0x230对象存在，则取该对象+0x98所指对象的string+0x78。未把这些偏移直接命名为最终收件人。

## 验证与剩余缺口

`python3 Library/ai/verify_wechat_record_replacement_20261016.py` 首次执行通过：19份导出4697条指令逐字节匹配，90个关键位置、3个dyld槽、2组类型名称核验；新脚本Ruff通过。旧文本handler、输入链合同和账号停止记录哈希未变。验证器用独占写入保留本次报告，不应覆盖重跑。

这些是静态证据，不是活体观测、可调用性或成功回执。完整lookup分支/外部记录修改、builder参数来源和收件人方向、真实group/config/线程及末尾排空、完整适配与独立送达仍缺；产品拒绝门保持，不请求新观察窗口。
