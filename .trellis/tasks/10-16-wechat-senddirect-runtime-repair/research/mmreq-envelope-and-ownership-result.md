# 4.1.15 基础请求包装与完成所有权

本轮落实离线基础包装模块，并缩小原生请求生命周期缺口。**尚未实现可发送的 send_direct；没有真实发送结果。**

## 问题所在与证据边界

已确认的问题位于本地原生调用适配：旧路线错认输出对象，并绕过请求包装和请求对象生命周期。当前没有证据说明微信服务器协议故障，也不能仅凭名称混淆断定 DLL 不可调用。

目标为 WeChat 4.1.15（270135），ARM64 薄片 SHA256：
`6a5bd0cbb39ad3092c15e9debda2db4969eedf1b58caad244d88033a996833a7`。
所有地址均为该薄片的 Ghidra VA，不能直接作为运行时地址。

## 已证明的基础生产链

- `text-contract-pass15/native-fn-4634710.c/.asm`：从请求对象复制路由字段，调用其虚表 `+0x10` 获取内层序列化请求。
- 同函数调用 `0x5563108` 构造外层消息，通过账号对象虚表 `+0x20` 取字段 1；**字段原名未证明**。
- 内层字节写入外层字段 2，外层经 `0x5ab3f60` 序列化，通过 `0x5ded508` 写入 `Task+0x1c8`；设置 `Task+0x1c0=1` 后调用 MMStartTask。
- `text-contract-pass28/native-fn-55653ac.c/.asm` 给出 wire tags；`text-contract-pass35` 的 `0x55657b0/0x5ce61ec` 都检查 required presence mask `0xf`。
- 独立 LLVM 导出 `text-envelope-consumer-complete.asm` 覆盖 `0x5ce5654..0x5ce5df0`（不含末端），补齐 Ghidra function body 缺失的 switch case 指令。

基础字段为：1=uint64、2=bytes、3=int32、4=bool、5=bool。前四字段必须存在；原生基础生产者显式写入字段 3=0、4=false、5=false。序列化器不能因值为零就省略 required 字段。

## 已完成的实现与验证

`mmreq_base_4115.py` 实现纯字节基础包装，不读取账号、进程或用户消息，不调用原生代码。测试 `test_mmreq_base_4115.py` 使用已安装 Google protobuf 运行时作为独立编码/解析参照，包含 25 组数据交叉核对及缺失 required false 的反例。

fresh 结果见 `mmreq-slice-validation.json` 和其中三个 v2 日志：基础模块 5 项通过，既有被动入口回归 15 项通过，6 个 Python 文件 Ruff 通过。初次日志留存脚本因错误的虚拟环境 Ruff 路径中断，未修改产品；查实工具路径后保存了上述完整成功结果。

**实现范围仅为基础外层消息**：账号相关扩展字段 7/9/10/11 尚未覆盖，不能装入完整发送驱动。其输出用于账号包装之前的 `Task+0x1c8`，不能直接替换最终输出缓冲区 x4。

## 完成回调与释放约定

`text-contract-pass42/native-fn-4635b9c.c/.asm`：OnTaskEnd 从 owner 的 taskid map 取得请求裸指针，先移除并释放 map 节点，再处理响应。
请求虚表 `+0x18` 接收内层响应；随后读取请求 `+0x68` 的完成回调对象并调用其虚表 `+0x30`。回调为空时进入 `0x21eccc` 抛异常；只有回调返回非零时，才调用请求虚表 `+8` 销毁请求。
`text-contract-pass43/native-fn-21eccc.c/.asm` 确认该异常分支调用 `__cxa_allocate_exception` 和 `__cxa_throw`；具体异常类型原名不作推断。

因此 Task 中两个 AutoBuffer 的深复制只解决字节存储，不解决请求裸指针、完成 functor 及其捕获对象的生命周期。不能构造空回调对象，也不能在入队返回后立即释放请求。

## 新定位：当前 newsendmsg 工厂与路由

`scan_wechat_cgi_literals_20261016.py` 只在显式二进制常量范围检索，以已证明的16字节相邻密钥、加0x8a再XOR的规则恢复CGI字面量。20个格式命中中，`0x88ada2e` 解出 `/cgi-bin/micromsg-bin/newsendmsg`。这只是定位线索，后续已核对原生代码：

- pass60/61：该密文只有 `0x30c14a4` 一处原生读取，确实按相同规则解码；该函数用 **x8隐藏返回槽** 写入请求选项，不能照抄Ghidra显示的单参数ABI。
- `newsendmsg-request-options-static.json`：选项的六个u32为 `[522,0,0,1,522,0]`，不采用历史XML表中的237。
- pass62/63：`0x30c2c1c` 分配 **0xe0** 字节请求，调用构造器 **0x30c2de4**，其虚表为 **0x9de8268**，将选项+0x10的522复制到请求+0xc，将CGI复制到请求+0x18。
- 该工厂通过请求虚表+0x20取得内层对象并复制正文，随后将调用方的完成functor**移入/克隆到请求+0x68**，再经服务虚表+0x28入队。`0x30c2c98..0x30c2d54`原始指令已逐段阅读，未执行这些调用。
- pass64/65：请求虚表+0x10为 **0x30c2ed8**，序列化 **请求+0x78** 的protobuf；虚表+0x18为 **0x30c2f80**，把响应解析到 **请求+0xa8**；虚表+0x20的getter **0x30c2fd4**返回请求+0x78。

因此当前CGI、请求编号、具体请求对象构造和正文序列化入口已有静态出处。尚未证明条目字段原名/完整业务语义、完成functor上游捕获对象的完整合同，以及运行中的服务身份与回执。不能把这些离线地址填回旧schema3直调配方后启用。

## 条目wire合同与生产者交叉核对

`newsendmsg-4115-static-contract.json` 留存当前版本的编号、布局、虚表、wire字段与未完成门禁；它是研究合同，`live_ready=false`、`send_verified=false`，不由产品驱动加载。

pass67/68的请求serializer **0x465da58** 写字段1（32位varint）和重复字段2（消息），IsInitialized **0x465dbc0** 要求字段1存在并检查各条目。原生生产者对单条请求明确写入计数1。

pass70的条目serializer **0x465d024** 写七个字段：1嵌套消息、2长度编码字符串、3/4/5为32位varint、6长度编码字符串、7为32位varint。**0x465d30c** 检查presence mask **0x1d**，要求字段1/3/4/5存在；不把字符串推断成已证明的原始protobuf字段名。

pass71的两个生产者 **0x30bda14** 与 **0x30f9248** 都将原生记录+0x30复制到条目字段1的嵌套消息，+0x130到字段2，+0xc到字段3，+0x114到字段4，0x30f2168/0x33fcc结果到字段5；+0x160非空时写字段6。字段7的业务赋值尚未证明。这里只读二进制代码，没有读取用户聊天记录。

## Fresh静态验证与微信状态

`text-contract-byte-verification-v2.json`：98份函数指令导出（含重复导出），21883条指令、87532字节全部匹配冻结薄片；独立完整consumer跨度另有487条指令逐条匹配。这证明指令出处，不等于运行时成功。

`newsendmsg-vtable-slot-verification.json`：12个请求、protobuf及服务虚表槽经Mach-O dyld chained fixup链成员检查和独立解码，目标全部符合Ghidra结果。`newsendmsg-static-verification.json` 保存新脚本Ruff、源码/合同哈希与末次只读状态：WeChat PID33589、state=2、traced=false，无LLDB/debugserver。没有执行任何原生调用。

## 排除与后续边界

AI SDK 的 `0x266dca4 → 0x2672934 → 0x265e9b8` 属于 `ai_sdk_manager.cc`，不能用其0x3eb作为微信聊天请求编号。另已解出sendappmsg的原生请求编号222（`appmsg-request-options-static.json`），它与newsendmsg是不同请求，不能混用。

旧普通MMReq2Buf默认实现0x465756c仍仅返回0。本轮只读复用Ghidra工程、未调用用户禁用的哨兵，未附加、触发UI、注入或发送；实际锚表保持身份校验用途，失效调用字段保留null。A7/L3继续开放。

## 续跑补齐：正文、客户端哈希与服务身份（2026-10-16）

此段更新前文的开放项：嵌套消息schema、上游完成functor具体捕获布局和静态服务来源现已找到，仍保留运行时及真实回执门禁。

### 可运行的离线实现

- `newsendmsg_wire_4115.py`：内层请求及全部7个编号字段编码；字段1的嵌套wrapper由pass76/77/79证明只有一个可选长度字段，IsInitialized恒返回1。条目字段1/3/4/5仍必须显式存在；optional absent、空字节和零值分别保留。8项独立Google protobuf测试通过，覆盖24组长度/整数交叉、必填缺失、重复次序及边界。首个手写期望向量误写长度0x0c，独立runtime及实际十字节payload共同证明应为0x0a，已纠正测试。
- `newsendmsg_client_hash_4115.py`：条目字段5来自`GetSendClientId`字符串经`0x33fcc → 0x9ebf8`哈希；尾部1/3字节分支使用有符号字节。`verify_wechat_client_hash_20261016.py`逐字节核验并仅提取208字节无重定位、无外部调用的叶函数，将其链接到全新独立可执行程序，对604组纯合成输入逐项对照Python移植，全部相等。未加载活体微信dylib、未读取真实client ID。原始protobuf字段名仍未恢复，不改称已证实业务名。
- `newsendmsg_identity_4115.py`：有界只读对象身份检查，最多80字节，5项合成对象图测试通过。它本身没有附加、表达式、原生调用或发送能力。

### 完成functor与异步上下文

pass72/74/75/77/79证明：`0x30c295c`分配0x30字节functor，虚表`0x9de82c0`。+8/+0x10为异步上下文/共享控制块，+0x18为steady_clock值，+0x20/+0x28为mutex/其共享控制块。克隆`0x30c31bc/0x30c3224`保留两个共享捕获，销毁`0x30c326c/0x30c3300`释放，后者同时释放functor本体。

虚表+0x30的`0x30c338c`解引用请求/结果参数后尾跳`0x30c3420`。该处理器锁mutex、复制响应，经`0x30c35a0`移交拥有数据的functor，解锁后明确返回1；因此正常返回会使OnTaskEnd调用请求删除析构器。不得把“native enqueue返回”当作完成，不得用空回调，也不得在完成前释放上下文。

pass85/86进一步证明`0x66696dc → 0x6669058`是状态结算：在递归锁内仅当context+0x9c为0时置1，接管+0x90的结果functor，notify_one并按+0xd8条件触发后续处理；已经结算的上下文不重复覆盖。它不是已经证明的任意线程执行器。高层同步包装`0x30bee20`存在重试/等待分支，不能直接在LLDB表达式中照搬，更不能把其内部重试误认为允许循环附加。

### 静态服务来源已证明，活体实例尚未核验

pass72/79/80/81/82/83/84：`0x4669774`读全局`0xa45df38`；账号构造器`0x4666b54`安装虚表`0x9e92400`，其+0x18槽`0x466a318`返回账号+0x250。

`0x4668ad0`创建控制块，调用`0x462e4d4`构造嵌入owner。服务指针是控制块+0x28，owner是控制块+0x18，二者差0x10；账号+0x258保留控制块。owner/owner+8/service虚表分别为`0x9e8fc30/0x9e8fd78/0x9e8fda0`。服务+0x28槽经`0x46353a0`调整this=-0x10后进入通用请求生产者，保留原生账号包装路线而不手写账号密钥扩展。

### 新运行核验方案已完成前置工作，尚无新授权

`newsendmsg-next-runtime-window.md`明确单次前台最多30秒，只核验两处已有代码锚点及80字节固定指针，读完立即解除，不等待消息命中、不调用原生发送函数、不发消息。
独立的`identity_observer_4115.py/run_identity_observer_4115.py`保留旧已消费执行器原样。`identity-cleanup-qualification.json`的10项真实LLDB一次性fixture测试全部通过；原始新检查曾误拒LLDB内部临时dyld硬件断点，现核验所有安装/移除成对、仍禁止软件断点及残留，失败记录留存。

`newsendmsg-slice-validation.json`记录：正文8项、身份5项、基础包装5项、被动入口15项通过，13个Python文件Ruff通过；无新授权的preflight在启动debugserver和创建消费标记前确实拒绝。末次微信PID33589、state=2、P_TRACED=false，LLDB/debugserver均为0。本次未附加微信、未发送、未改产品锚表。

`newsendmsg-lifecycle-slot-verification.json`：21个请求、正文、完成和账号/服务虚表槽独立dyld链成员与解码匹配。指令出处最新计数另以v4验证文件为准（含重复导出，不能称为唯一函数数）。pass80误把0x30c3c34当作查询入口，实际被Ghidra定位至0x30c3a3c；其用途须按完整0x30c3a3c及原生引用解释，不以错误查询地址作为入口。

仍待完成：运行中服务身份；调用线程及高层异步上下文合同；用户指定收件人/正文的可执行适配与独立真实回执。`live_ready=false/send_verified=false`，A7不勾选，旧schema3拒绝门不放行。

## 第二次窗口结果及C++组件（更新前文待核验状态）

用户对call_dP05Bw2871pKi3PUUIixinJy明确授权一次前台只读窗口、最长30秒。`live-observe-xk07n8e9/supervisor.json`记录实际3.822秒、仅1次附加；两处代码锚点及10次/80字节账号/服务/owner/control/虚表读取全部符合静态合同，立即成功解除。同PID33589及启动时间，非停止态，P_TRACED清除，辅助残留0。无原生调用、注入或发送。授权已消费，历史对象地址不作为下一次配方。

`newsendmsg_completion_4115.hpp`实现独立拥有的完成状态：强制heap functor，状态由shared_ptr持有，首次结果写入后不覆盖，始终不把回调到达当作sent。C++夹具按工厂heap转交的+0x18指针操作和OnTaskEnd的虚表+0x30引用参数方式实际调用自有libc++回调，覆盖跨线程、克隆、释放和32线程竞争，共16项检查通过。没有执行微信的工厂或回调。

`newsendmsg_native_body_4115.hpp`以48字节、8字节对齐存储及注入的构造/ParseFromArray/非删除析构函数组成RAII。成功、解析返回false/抛错、缺函数、空输入、边界等9例通过；不允许复制/移动。native parser 0x5ab3ab8在解析后检查虚表+0x28初始化条件，不能直接覆盖protobuf布局。该测试使用自有函数，不声称微信原生解析已运行。

`newsendmsg-cpp-verification.json`保存构建命令与源码哈希。ASan+UBSan夹具曾无输出占用CPU，已只终止本次自有夹具；独立最小尺寸探针在ASan下同样5秒超时，普通构建通过。没有sanitizer成功结论；失败没有触碰微信。

pass88/89进一步把高层launch定位到co_job_group：0x66846b8创建拥有job，按context标志经0x6682d18加入持有shared对象的列表；+0x78 mutex保护+b8列表/+c8计数。该证据排除了把context resolve当作通用线程调度的解释，但完整context来源、标志与线程亲和性仍未证明。

pass90～94补录响应合同：外层字段1为嵌套基础响应、2为32位值、3为重复item；初始化mask0x3。item字段1/3～7为32位、2为嵌套wrapper、8为64位。原生生产者还检查两项外部错误均为0、item非空、首项+0x10为0，随后把首项+0x28复制到记录+0xf8；仅队列返回或回调到达不足以宣称成功。原始业务名和完整item必填mask未在本切片恢复。pass93查询0x465e6b8实际落入0x465e660，该错误查询地址不作为入口；响应结论以精确0x465e144/0x465ef20/0x465f2b8/0x465f4a0为据。

当前未解决项收敛为业务输入、co调用上下文、完整适配与指定收件人/正文的真实回执；产品拒绝门继续保持，live_ready/send_verified仍为false。

### 调用上下文来源进一步核对（pass95～98）

原始指令确认高层0x30bee20真实输入为x0=service、x1=inner protobuf、x2=std::string指针、x3=options，x8为48字节结果槽；不能照Ghidra的额外显式param_1签名调用。0x30c0d04同样使用隐藏x8构造超时上下文，经0x66853a4取得当前任务组。0x66845a4先走0x6684284：有协程对象时查询协程局部存储，否则查线程局部存储；为空时以0x6684444初始化全局0xa518700。配置从group+0x108复制，0x2e0a888是`x0+0x108`访问器，不能当作无参数getter。

因此上下文来源已定位到具体入口与默认组，而不是继续把服务指针和协程对象混用。默认组存在仍不证明暂停调试器内表达式调用安全；等待/取消完成和线程亲和性仍须完成可执行合同，未以该结果尝试调用微信。

最新收口证据为`identity-slice-current-verification.json`：v5累计165份导出（含重复）、28009条指令/112036字节全匹配，完整consumer另487条；当前合同与C++源码哈希固定。沿用未变化的33项Python与25项C++检查证据，过期授权在启动调试器前拒绝。末次同一微信实例健康、无新附加或原生调用，仍未发送；A7未完成。本文件此前的v2/v4及待授权描述只代表各阶段历史。
