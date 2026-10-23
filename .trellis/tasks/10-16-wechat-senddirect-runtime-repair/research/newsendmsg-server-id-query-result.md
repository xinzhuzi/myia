# server_id 查询回调与结果标签：离线核验

仅针对冻结 ARM64 4.1.15 (270135)，SHA256 `6a5bd0cbb39ad3092c15e9debda2db4969eedf1b58caad244d88033a996833a7`。本轮只读已有 Ghidra 工程导出；没有执行微信、附加、调用原生函数或操作账号。`account-safety-stop-20261016.md` 继续约束后续工作。

## 参数及所有权

父方法 `0x32cf5e8` 在相应服务门通过、record `+0xf8` 非零且原 w4 非零时，可创建大小 `0x68` 的 capture。invoke=`0x335bfac`、cleanup=`0x335c0f0`；`+0x28` 保存 server_id，`+0x30` 保存选中字符串，`+0x48/+0x50` 是 service pair，`+0x58/+0x60` 是 future pair。

原始指令证明 invoke 的 capture 参数是 x0；Ghidra 伪代码显示的第二参数不能直接用作 ABI。它把 service pair 移到局部并清空 capture 中的 pair，增加 future 引用，然后调用 `0x3274034`：x0=service 指针、x1=字符串地址、x2=server_id。x3 虽复制了 x0，该 callee 未消费它。不能将 capture 或数据库 record 当成查询入口的 this。

query 返回值低字节写到新容器 `+0x8`，经 `0x66696dc` 发布；invoke 随后释放其局部引用。cleanup 负责释放 capture 尚存的 future/service pair、析构长字符串并释放 `0x68` 块。此顺序只证明已审阅对象的持有关系，不证明全局任务排空。

## 查询结果不等于消息记录

`0x3274034` 通过 binding getter `0x4cbaf80` 构造两处偏移 `0xf8` 的表达式，其中一处结合 server_id，再加载 service `+0x8` 并调用 `0x56f3a00`。后者保留隐藏 x8 并传给 `0x56f3be0`，输出是 32 字节局部结果。Ghidra 将隐藏返回区错列为普通参数，原始寄存器优先。

`0x56f3be0` 初始化输出；在 `0x5646028` 返回 bit0 非零、`0x5646030` 返回非零且 `0x5646050` 返回 bit0 为零后，转移 `0x56460a8` 的 vector 并将首字节置 1（若尚非 1）。`0x3274034` 只返回这个首字节。上述 helper 的完整业务语义及全部数据库查询逻辑仍未证明，因此不能把标签擅自命名为“查到消息”或“查询成功”。

future getter `0x22d9f40` 经容器虚槽 `+0x18` 检查类型名称，屏蔽高位后与冻结地址 `0x87dfff0` 的精确字节 `_10a3dae4` 比较；匹配时返回容器 `+0x8`，否则抛异常。父方法在 `0x32d03cc` 读取该字节覆盖 w24。零值可进入正常插入分支；非零路径在 `0x32d0790` 将原 record x20 放入 x1，调用 `0x335bddc`，后者复制/移动原记录并发布。该 query 回调没有返回一份替代的完整 record，也没有任何网络回执。

## 验证与剩余工作

`Library/ai/verify_wechat_server_id_query_20261016.py` 核对 9 份导出的 2066 条指令、56 个关键位置及 1 个精确类型名称，并校验前序合同和停止记录哈希；Ruff 通过。结果为 `newsendmsg-server-id-query-verification.json`。字节匹配只证明留存导出与冻结文件吻合，控制流结论另经审阅，不代表运行观察。

尚未证明其他父方法分支、查询标签的完整业务含义、builder 参数来源和收件人方向、真实线程/config、取消组合与最终排空、完整适配及独立回执。A7 及实施 20～24 仍未完成；不接入产品、不装机、不恢复微信操作或请求新观察窗口。
