# 注册字段访问器与借用值寿命（实施85，2026-10-18）

本轮补齐实施84所指出的注册访问器合同，不将注册表合同当作运行时所有字段列表的身份证明。只读冻结ARM64文件，保持账号停止约束；未附加、执行目标代码、发送或部署。

## 五类访问器的精确身份

`0x4cc245c`实际构造15个(vtable, member offset)对；五个vtable的+0x10/+0x18/+0x30共15槽均从冻结dyld链独立解码。

| vtable | kind | null检查+0x18 | 读取+0x30 | 注册offset |
|---|---|---|---|---|
| 0x9eb05a8 | 1 | 0x4cc2d88，返回0 | 0x4cc2dac，读32位 | f4/110/114/118/11c/120/124 |
| 0x9eb0650 | 1 | 0x4cc2dd4，返回0 | 0x4cc2df8，读64位 | f8/108/100 |
| 0x9eb06e0 | 1 | 0x4cc2e20，返回0 | 0x4cc2e44，读32位 | 128 |
| 0x9eb0770 | 3 | 0x4cc2e74，返回0 | 0x4cc2e90，返回字符串视图 | 160/130/148 |
| 0x9eb0818 | 4 | 0x4cc2f20，返回0 | 0x4cc2f3c，返回buffer视图 | 178 |

三个标量getter完整指令均为读取accessor+8成员offset、从record+offset读取、ret；无store、无callee调用。这一性质可关闭这些具体标量getter的本地写入疑点，不需要扩大到所有数据库函数。

`0x56fa6f4`完整两条指令只读field+0xf0取得访问器。`0x329728c`初始化operation为空字段列表、mode0、空record指针；初始化本身没有选择上述record注册表，后续字段列表来源仍须连接，不能凭offset相同认定所有元素均属五类访问器。

## 字符串：返回的是借用视图

`0x4cc2e90`按accessor+8取record成员地址，通过隐藏x8把结果写到调用者提供的对象。`0x56c90b0`只读取字符串的inline/heap表示，选择data与length，再到`0x562fd20`，后者存data/length并明确写owner=0。

`0x562fe5c`将临时包装移动到输出并清空临时包装，移动的是视图表示，不是正文载荷。此路未分配或复制payload，也不retain原record字符串存储。输出/局部存储须与原record/payload不重叠，原存储须存活到绑定消费结束。

因此不能把字符串getter返回值称为独立拥有的正文副本。本轮结论专指数据库字段访问器，不能与实施84中后处理摘要的独立字符串复制混为一谈。

## byte vector：同样借用原始载荷

`0x4cc2f3c`把record+offset交给`0x26f387c`。`0x56c9134`读取原vector的begin/end，计算长度，`0x5632804`向新包装写data/length并把owner callback置空；`0x5632750`转移包装的data/length及内部可擦除function，清空临时值。

这里未复制vector载荷，也不拥有/retain原record的vector存储。外层包装的构造、移动与析构不等于载荷深复制；通用function/helper全部效果尚未证明。该包装仅在有效且持续存活的源数据、输出不别名条件下解释。

## 已确定的下一边界

字符串绑定`0x56f4ed4`经backend虚槽+0x48消费视图，buffer绑定`0x56f4f20`经+0x58消费视图。两者都是虚调用包装，并未在此层证明实际后端会复制数据、只读数据或完成消费。不能依据函数名推断SQLITE_TRANSIENT，也不能提前释放record。

下一离线动作限定为：连接实际插入字段列表来源到具体访问器，并确认所选backend+0x48/+0x58的消费合同。不展开无关表/全部SQL，也不把尚未证明的全局别名/并发隐藏起来。

## 验证与完成边界

脚本：`Library/ai/verify_wechat_registered_accessors_20261018.py`。
结果：`research/registered-accessors-20261018/verification.json`。
30份连续导出、1022位置、59个精确位置、190个独立控制转移、15个dyld槽、15个注册pair、99个来源哈希匹配；Ruff通过。新增pass433～438均成功且日志无SCRIPT ERROR。

实施85仅关闭该有限合同。完整字段保持、真实协程/取消最终释放、完整原生适配、真发送及独立回执、部署与原9项/A7继续未完成。无活体操作或新授权申请。
