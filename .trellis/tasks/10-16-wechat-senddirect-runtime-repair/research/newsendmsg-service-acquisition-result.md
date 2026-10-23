# 所选文本服务取得与局部异常清理（实施55/67部分，2026-10-18）

只读冻结4.1.15 ARM64及既有Ghidra工程。账号安全停止记录继续有效；没有运行/附加/调用微信、UI或账号操作、发送、安装或部署。完整目标仍未完成。

## 已补齐的具体入口

完整builder在0x2920bc4调用0x268f370，真实ABI为x0=registry、隐藏x8=sp+0x88返回shared pair。后者用虚表0x9da2000的描述器查服务；独立dyld解码+0x10=0x26c4024、+0x20=0x26c4070。前者读取RTTI名字指针0x9ded308并去掉高位标记，精确键为`_3d834e75`；后者以x1接收源pair，保留控制块，向隐藏x8复制结果。不是反编译器显示的普通首参数返回区，也没有在此方法里做dynamic_cast。

0x454182c按描述器名字查registry+0x28的pending索引。命中返回的是带+0x18存在标记的future容器，不是可直接当发送服务使用的pair。0x268f370在标记恰为1时等待0x66856fc，再调用0x21b3684；该getter通过真实strcmp核对精确RTTI`_62250804`，返回erased payload+8，外层复制并保留其中service pair。

没有pending结果则调用0x4540bd8。已存在节点时经描述器+0x20复制pair；缺失时构造0x9e870a8正文并交0x666ab58，随后等待并以同一typed getter取pair。该正文捕获registry、名字C指针和描述器指针，其中后两者不是独立拥有的string/shared对象。其invoke为0x4541f78；完整构造/注册副作用、异常取消时的所有排队拥有者仍未证明，不扩大成本轮已完成范围。

## 当前协程要求是无条件的

0x268f370在检查pending标记之前无条件调用0x6676adc。它读取既有当前core相关TLV槽0xa24de80，提升weak pair并把strong pair保存在guard中；非终态时增加core+0x3c8。无当前值的分支在0x6676b50写零pair，随后0x6676b58仍按该pair首指针读取+0x288；不能把它当成普通线程可安全调用的回退，也不能仅凭执行器TLS相等就调用此入口。

guard析构0x6676b84在非终态时减少+0x3c8，并释放保留的core pair。这是当前core的局部保护/持有，不是新文本Job的启动租约，也不拦截其他线程对新Job所在group的取消。本轮不为+0x3c8赋予超出这些机器指令的全局语义，不设置TLS或手工改计数。

## 异常清理覆盖哪些调用

Ghidra的0x268f370正文只到0x268f4cf。独立compact-unwind给出右边界0x268f4f8及LSDA 0x7364e58，LLVM补齐以下landing pads：

- guard构造调用0x268f3b4异常：落0x268f4e4，只清理已经构造的optional future，再继续展开。
- guard构造完成后的等待0x268f3c8、typed getter 0x268f3d0异常：落0x268f4d4，先调用guard析构，再清optional future，最后调用真实`__Unwind_Resume`。
- fallback调用0x268f428异常：落0x268f4d0，再进入同一guard/future清理。

optional future清理0x21b3484只在标记恰为1且控制块非空时递减strong引用、必要时虚析构/release_weak；不是job cancel、join或排空。上述结论要求有效对象、guard构造成功且清理函数正常返回，只覆盖这些本地call-sites；不证明各callee的全部资源/异步工作已经退出。

## 服务指针怎样进入发送作业

builder在0x2920bdc先拒绝空service；0x29216cc从sp+0x88取pair，复制到capture source+0x58并保留引用。0x292d868把它移到body+0x60/+0x68并清空源pair。0x292ef9c从body+0x60取service，调用0x317ded4。它与input pair、chat_id和外层call_id各自分开；不能拿一次固定裸指针快照代替这条拥有链。其他正常/异常退出与取消的完整拥有者仍由20/55/22验收。

## 验证与下一步

`Library/ai/verify_wechat_service_acquisition_20261018.py service-acquisition-20261018-v2`及Ruff通过：12份Ghidra导出和完整builder共3562位置；9个独立unwind/LLVM区间782位置，补100位置、合计3662位置匹配冻结字节；106精确检查、705独立控制转移、4个dyld槽、4个真实导入、4个LSDA调用位置、78源哈希。unwind区间可共享或包括相邻小入口，完整字节覆盖不等于全部语义覆盖。

初次连续性断言发现0x4541f78导出遗漏内部0x4542324；失败源码保留在service-acquisition-20261018/failed-verifier.py。v2明确列出此缺口，由独立LLVM恢复原始B到0x4542330，另保留异常尾段；没有将Ghidra末尾当作完整边界。xref输出共416项而仅保留64，未据它枚举全部调用者。

这次缩小了67的service gate和局部异常清理缺口；不关闭55/67/A7或原9项。下一步应处理新文本Job启动/外部取消之间的真实协调及状态0最终释放，或在有证据的原生API上形成适配器自己的完整生命周期合同。不得把当前协程guard、shared service持有、结果发布或正常局部析构当作服务关闭租约、全队列排空或独立送达。完整业务字段保持、完整原生适配、真发送/独立回执及部署仍缺；不继续向无关registry/账号初始化扩散。
