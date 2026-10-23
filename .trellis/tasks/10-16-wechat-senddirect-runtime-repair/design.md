# Design

## Boundaries
产品修改覆盖 plugins/wechat-bridge 的 senddirect.py、CLI直发入口、probe说明及三方版本/组件文档；离线测试放 tests/wechat-bridge。4.1.15 缓冲区原型放本 task research，未经终验不装入产品。禁止恢复旧 Frida/LLDB 编排器。

## Passive checks
新增纯磁盘校验：读取已安装包 Resources/wechat.dylib，解析 ARM64 切片，使用现有 slice_arm64_sha256 比对完整哈希，并确认副锚点字节。doctor 默认验证改用此函数，保留原三态字段，增加验证范围说明，磁盘匹配不能声称运行时调用已成立。dry-run 在创建临时工件、解析PID和LLDB路径前返回离线结果。配置已开不等于调试授权。

## Invalid recipe
4.1.15 完整切片哈希 6a5bd0cbb39ad3092c15e9debda2db4969eedf1b58caad244d88033a996833a7 对应的 schema3 模板直调路线已证伪，真实执行在任何附加前以24拒绝。该身份不会通过换send_entry或改标签重新启用。未验证新原生适配不得接入。

## Correct buffer contract
以留存二进制已核验的 x4 输出参数与原生 __FitSize/Ptr 为依据构造独立原型，避免 AllocWrite 的累积position/length副作用。确认五字段布局和长度重置约束；不把protobuf对象或ActionCode访问器当成缓冲区/序列化器。原型不安装hook、不发Task、不启动宿主，独立依赖注入；适配是否能直发另需实际callback及所有权证明。

## Compatibility and rollout
doctor既有字段保留；磁盘状态仍是ok/mismatch/unknown，但输出声明仅磁盘校验、无live readiness。正常CLI在取钥/目标解析/PID/发送占位之前检查配置及驱动门；execute_send与raw batch仍独立设门。旧4.1.15配方不可借改锚表恢复。离线套件使用人工合成Mach-O。

0.9.1通过回归后，本地构建无依赖wheel；先备份再同步独立桥7个必要文件及桌面Python发行包。核对源码哈希、发行元数据和其余依赖不变，在MYIA_HOME沙箱内检查真实安装件。未重打包/修改签名App资源，未重启App或微信。原生适配不打包不装机；历史备份仅供核验，不自动恢复旧调试行为。release-plugins脚本走Git archive且不包含本组件，本轮未调用。

## Single observation window (ended; authorization consumed)

仅新增research中的前台观察器与Library/ai中的验证脚本；产品拒绝门保持。空debugserver先连接、收到QSetDetachOnError:1的真实OK应答才允许唯一attach；30秒绝对deadline包含握手、观察及清理，提前结束观察并预留脱附验证时间。父进程取消/超时先通知LLDB清理，阻塞时关闭该客户端连接，由已设置的debugserver脱附；必须先用全新隔离夹具证明正常/到时/异常/取消/客户端死亡的内嵌LLDB行为。系统探针独立核验同PID起始时间、P_TRACED清除且非stopped/zombie。

微信窗仅观察0x597d398处的普通MMReq2Buf回调：一个硬件一次性断点，最多读取manager+0x10、对象虚表及+0x50槽和少量代码；不读取正文或密钥，不表达式调用/注入/自动发送/触发UI。无自然命中即如实报告，禁止重试。消费标记独占创建，已结束授权不得复用。

实际窗口21.053秒，单次附加、未自然命中、成功解除且未发送。后续继续指令只推进离线工作，不复用该窗口。

## Offline base envelope and completion ownership

基础MMReq模块位于research/mmreq_base_4115.py；字段1～4必须显式存在，字段5也按原生基础生产者写入false。输出对应账号包装之前的Task+0x1c8，不能当作最终x4。newsendmsg类型、CGI、522编号、构造/序列化和完成functor的shared捕获已静态定位；服务身份已通过一次只读快照。账号扩展仍使用原生生产者，调用线程/业务字段输入仍未完成，模块不装机。

OnTaskEnd先从taskid map移除节点，再调用请求+0x68中的完成functor；空functor抛异常，返回非零才调用请求虚表+8析构。必须保留请求和捕获对象直至完成处理，Task缓冲区深复制不代表这些对象安全。证据与边界见research/mmreq-envelope-and-ownership-result.md。

## Research C++ components and consumed identity window

本机libc++的function大小32/对齐8、string大小24；独立夹具核验+0x18的heap functor转交与虚表+0x30接收引用参数，符合native factory/OnTaskEnd原始指令。newsendmsg_completion_4115.hpp只保留首个错误结果、通过shared_ptr持有状态、不保留或释放原生请求，返回true交由OnTaskEnd删除；回调到达不设置sent=true。newsendmsg_native_body_4115.hpp使用注入的ctor/parser/非删除析构函数及48字节对齐存储，解析失败亦清理，不允许复制/移动。两组件没有微信加载器、地址解析器、附加或发送入口，仅用于后续适配；不得据此放行产品。

账号/服务核验窗口已消费：3.822秒，单次附加、身份匹配、立即解除、零残留，无原生调用/发送。历史指针不得保存为下次调用配方。后续工作只沿离线合同继续；新的活调试和发送均受原有明确范围约束。

## Offline operation integration and cancellation race

后续组合实现见research/newsendmsg_operation_4115.hpp与newsendmsg_native_response_4115.hpp。原生factory在enqueue后仍访问request，completion必须等待shared publication mutex；取消只删除仍在map的request，不保证completion发生，已被OnTaskEnd取走者仍可晚到。operation显式cancel/expire只发起一次，晚到结果只追加观察，不覆盖本地取消/超时，也不设置sent。response在callback内深拷贝、验证初始化并先ByteSize再cached-array序列化；Python编号解析器不臆定业务含义。析构不隐式调用native；未证明调度/底层排空/模块卸载屏障前不提供加载器或产品接线。fresh范围及局限见research/newsendmsg-cancel-response-result.md。

## Scheduler and request cancellation remain distinct

离线证据见research/newsendmsg-scheduler-lifetime-result.md与newsendmsg-cancel-dispatch-result.md。协程作业的取消入口与OperationFunctions.cancel(service, task_id)作用于不同对象，适配器必须分别持有并处理它们；取消作业不得丢弃已发布请求的task_id或晚到回调状态。运行标志清零、完成入口标志及promise结果均不足以证明最终回调和weak引用已经销毁。具体调度服务、两层取消组合和模块卸载屏障尚未证明，因此不提供加载器或可执行接线。

0x66741a4转发x1=-1到0x66741ac，后者原始指令测试x1符号；Ghidra省略参数的声明不得用作ABI。账号安全停止约束优先于历史活体实验计划：本轮及自动续跑只处理本地文件和离线证据，不恢复微信操作。

## Offline job return ABI

研究声明research/newsendmsg_job_abi_4115.hpp使用opaque JobGroup/JobConfig/Job，返回std::shared_ptr<Job>：在当前Apple ARM64/libc++下，返回区通过隐藏x8，完整入口x0～x3分别为group/config/body/finished，简化入口只接受前三项。原生function参数仍须满足非平凡clone/move/析构合同，不能把Ghidra显示的返回区当成x0普通参数。独立汇编/C++夹具确认主机调用约定，不证明运行时对象身份或调用线程安全；声明没有任何原生地址/加载器，不装机。默认group与配置补齐依赖当前协程/线程及运行状态，禁止仅根据静态默认地址生成可执行版本JSON。证据与局限见research/newsendmsg-job-abi-result.md。

回调内部ABI的独立核验见research/newsendmsg-job-erasure-result.md：正文从function+0x18取得erased对象并调用虚表+0x30；完成回调通过x1转交单字节bool地址。自有汇编调用本机内联/堆存储function均通过，仅证明兼容性。原生完成bool来自作业取消路径，不能替代网络请求错误码或独立送达回执；线程、拥有权、异常及排空合同仍需分别证明。

## Join and final capture destruction

离线核验见research/newsendmsg-join-boundary-result.md。job+0xb8和+0xc8保存同一promise/future状态；发布结果先于关联通知和最终function。普通等待只等待状态非零，协程已就绪分支同样不等最终function销毁；join不是排空屏障。原生0x667f128析构再单独销毁job+0x120/+0x138的完成function及捕获，之后释放promise/future等引用。禁止在join返回、完成标志变化、callback进入或返回时卸载代码或整体释放服务；不得让job内完成function强持有同一job形成自身循环。必须另外证明在途请求、排队通知、最终回调及最后引用释放。自有门控并发夹具验证两个反例场景，不提供原生调度、排空或送达证明；真实group/config/线程与最终拥有者仍未明确，产品拒绝门和账号停止约束保持。

## Normal core teardown and independent request ownership

research/newsendmsg-core-teardown-result.md补齐正常返回的持有链：job持有core，core参数持有job；关联通知中作业组的有效直接注册先移除job节点，最终function返回后core参数清理再释放job，并清零清理器，随后core状态变3。执行器提交的function另持有core，必须区分正文返回与提交闭包销毁。外部job副本仍可延后完成捕获析构，排队通知持有接收方但其job参数只是指针。研究适配器须独立保存task_id/取消控制与回调状态，不能随job/core退出丢弃网络请求控制能力；禁止手工调用原生清理来强迫排空。新增2场景自有组件组合验证正常持有链和job/core销毁后响应晚到，未证明取消/异常路径、真实线程/config/执行器排空，不提供可执行接线或部署许可。

## Exception handlers and owned final notification

research/newsendmsg-exception-boundary-result.md以Mach-O unwind/LSDA补出Ghidra正文之外的异常处理：JobBody调用有两种精确RTTI类型的原生处理，随后取消作业组并回到正常销毁流程，其他异常继续展开。最终function调用及外层core入口调用在各自LSDA中没有本地清理落点，不能把正常返回的参数释放推定为异常安全。研究组件newsendmsg_job_finished_4115.hpp仅保护自有、无原生调用的最终通知，捕获并保留首个exception_ptr，不向原生调用层抛出；它不包装JobBody、不替换原生类型处理、不隐式取消，也不证明排空。其捕获对象要求析构不抛出且不强持有同一Job。取消状态0分支只写状态3并返回，真实执行器顺序和后续参数清理仍须补证。8场景host ABI夹具通过不构成完整适配、真实发送或部署依据，账号停止约束保持。

## Executor provenance and owned body start gate

research/newsendmsg-executor-start-gate-result.md已定位发送路线的服务+0x290/+0x298协程接口：默认group与新活动group配置+0x18都取同一接口执行器；普通submit移动/克隆function后入队，正常调用返回后才销毁任务捕获。heap按deadline/sequence排序，编号在队列锁前分配，不能推定并发全局FIFO或以submit返回作排空屏障。job+0x140先于core构造和初次resume提交，因此单凭同一执行器不足以排除外部取消先入队的顺序。研究启动门只以自有JobBody实际进入为准：进入前记录取消并正常跳过正文，进入后且尚未离开才在绑定线程转交一次显式job取消，离开后仅保留独立请求控制；正文异常类型原样传播，不强持有自身Job。门不拦截原生组/外部取消，不提供原生调度器，线程绑定不等于活体身份核验。14场景host ABI/ResearchOperation组合通过；原生状态0最终清理、异常与完整队列/weak引用排空仍需证明。A7及55保持开放，不接线、不部署、不恢复微信操作。

## Executor ticket removal and capture constraints

计划固化已定位的executor+0x10提交（返回64位票据）及+0x20移除（x1保留完整票据、无返回状态），不把+0x20猜作线程检查。移除转至looper+0x38：按票据高32位定位索引、低32位核验代次，普通排队任务在队列互斥锁内销毁捕获并清任务指针，调度记录并未当场整体移除；特殊type2活动分支只标记延后处理。研究捕获析构必须不抛出、不重入此执行器、不调用原生控制，取消/网络请求控制另由协调器在已证明的上下文执行。组等待按作业结果逐个移除节点，不能替代最终回调/捕获及请求排空。新增ABI声明与自有虚槽/请求组合夹具仅作离线验证，不提供实际对象、地址解析或执行入口，不改变原生组/外部取消仍开放的结论。

## Job configuration layout and cancellation precedence

实施57以research/newsendmsg_job_config_4115.hpp补齐初始opaque JobConfig的0x38字节布局：24字节name、三个原始机器字及两个32位值；name自请求复制，机器字零值、word30=-1及flags恰为0x80000000时分别继承组默认值。研究resolve_job_launch仅处理自有快照，既不读取真实组，也不提供执行入口。登记由组/配置bit1控制，但后续组取消查询仍优先于flags bit0的延迟启动；因此flags=3也不能防止已取消组触发Job.cancel，不能作为55的完整解决。实际组状态可能在各步间变化，禁止将快照的未取消当作原子启动许可。8场景/16分支、host ARM64配置偏移/返回ABI及ResearchOperation组合通过；详见newsendmsg-job-config-result.md。组隔离与外部取消、状态0最终清理、真实线程及排空仍缺，不接线、不部署、不恢复微信操作。

## Request control affinity and service shutdown

实施58要求ResearchOperation的cancel/expire与factory处于同一自有线程生命周期，跨线程在本地状态修改及原生调用前抛logic_error；snapshot和完成回调仍可跨线程。线程编号可被复用，本机回归已观测到，故使用每线程独立shared令牌且operation保留其存储，不以std::thread::id相等代替线程存活与身份。此约束不证明该线程是正确原生执行器，也不允许创建线程退出后将控制迁移到替代线程；析构不隐式调用native。服务关闭0x46698d0先调用interface+0x290的0x453e904，后者标记停止、取消/等待活动及默认组，之后上层才继续调用服务+0x250/+0x260对象的虚槽0。跳过组登记会让该作业不在组遍历中，尚无完整关闭协调/请求排空证明时不得以flags=2/3绕开生命周期。core析构中的ID/名称通知不能补作状态0参数清理证明。证据见research/newsendmsg-operation-thread-result.md；8组45场景、100竞态及69次错误线程拒绝通过。真实线程/服务身份、取消可达性/清理、完整字段/适配与独立回执继续开放，不恢复微信操作或部署。

## High-level text routing and forwarded call tag

实施67的research/newsendmsg-text-job-input-result.md补证高层命令wire2在所选文本作业中被日志称call_id，不能当作chat_id或原生收件人输入；capture基址是body+8，复制/析构偏移须保留这一区别。所选完成标志使用非原子byte访问，不证明并发一次性。高层builder先从正文提取category、去精确CDATA外层，并优先按brand_account/emoticon分流，再判断message_type==1；所以完整适配不能仅以类型1和content_xml原文作为任意正文保持合同，也不能缩减成拒绝特殊正文后宣称任意正文支持。必须解决这条分流或证明另一个完整普通文本入口，且仍需真实线程/取消最终释放与独立回执。此切片只核验冻结文件，无产品接线或部署，账号停止约束保持。

## Resume condition and cancellation ordering

research/newsendmsg-state-zero-cancel-result.md补证恢复闭包body+8起是可选function，body+0x28/+0x30为独立core pair；invoke先把body加8，所以capture+0x18所指function的虚槽+0x30是恢复条件，不是执行器线程检查。初次恢复传空条件，不能因此认定它验证过线程。组取消在group锁内直接调用Job.cancel，之后才由Job提交handler；job启动标志早于core构造及初次恢复提交。限定state0取消写3返回、后到恢复跳过的路径尚缺最终参数释放，不能把通知/结果发布或闭包析构当作已解除job/core互持有。需先证明实际调用者线程/生命周期协调或完整原生释放路线；自有显式启动门不拦截原生组取消，禁止手工调用原生清理器补洞。本切片不证明原生泄漏已发生、完整排空或直发能力，账号停止约束保持。

## Native executor TLS and request entry guards

research/newsendmsg-executor-context-result.md补证0x6662530无参返回当前执行器指针，0xa24de50为__thread_vars中的TLV描述符、绑定__tlv_bootstrap；工作入口正常路径先写pthread身份和TLS再运行looper，返回后清除。研究组合ExecutorResearchOperation在正文/factory之前及每次cancel/expire入口核对调用方提供的执行器身份，同时保留ResearchOperation线程生命周期令牌；snapshot/回调可跨线程、析构不隐式查询或控制。不提供TLS setter或通过改TLS冒充执行器，不提供加载器/调度器。身份检查不等于对象生命周期租约、协程身份或关闭屏障，原生组取消与状态0最终清理仍开放。9个新增及15个依赖场景、100竞态和64/69次线程拒绝通过，仍不是完整原生适配或回执证据；A7/55/22不勾完成，账号停止约束保持。

## Signal snapshot ownership and disposal correction

实施70在research/newsendmsg-core-teardown-result.md纠正旧信号字段语义：状态+0x90是pthread_self身份，用于递归派发防重入，不是派发计数、执行器身份或排空屏障。同线程派发内析构通过+0x98延迟回收信号状态；外层finish释放的是信号分配，不是core参数。历史core-teardown合同的active dispatch count标签由signal-dispatch-20261018-v2-verification.json明确取代，历史证据不改写。

登记节点复制为独立快照后，断开原节点不撤销已复制的成员调用；非空executor另获持有接收方pair的闭包，而job参数仍是raw pointer。研究适配不得凭disconnect、信号析构或+0x90清零释放排队回调所需对象/代码；必须证明具体接收方、队列、请求与最后捕获的生命周期。15导出1472指令、75位置/19分支/3导入/3虚槽仅证明所选冻结正常路径，实际作业监听集合、状态0最终参数清理和全序仍开放，不据此接线或部署。

## Selected text launch ownership and pre-body wrapper

实施71的research/newsendmsg-text-job-launch-result.md确认所选builder在launch返回后立即释放shared句柄，其释放函数没有显式cancel/join；正常三参数launch明确传空最终function，不能假设隐藏最终回调补作core参数释放。可选0x28字节包装只拥有inner function，先经当前core执行器+0x18及既有等待入口，再调用原body；其自身析构只释放inner function及包装分配。全局32位值的用途/单位/运行值未证明，不生成配置。包装从JobBody进入，不能作为状态0跳过正文时的清理保证；它也不提供任意线程调用或排空合同。4006位置/100检查/19分支/6槽及Ruff通过仅补充这条所选路线，55/22/A7、完整映射/原生适配/真实回执仍开放，账号停止约束保持。

## Coroutine admission and pending cancellation

实施72的research/newsendmsg-scheduler-admission-result.md区分core+0x268执行器与+0x270对象键控的TLS scheduler：首次恢复回调可先进入pending heap，再按准入树节点数与对象虚槽+0x38返回值比较。null-key默认对象返回UINT64_MAX，不能把通用有限容量情形当作所选发送的已知前提；须先证明group/config实际key来源。pending选中后及模式1提交闭包invoke均会跳过状态3，局部pair释放不等于core参数中的Job引用释放。正常core清理先于准入树退队，退队只触发一次选择；scheduler析构释放pending pair及raw-key树节点，仍不提供完整参数清理屏障。研究适配不能以执行器回调已执行、队列条目消失、树计数下降或容器析构替代Body实际进入/原生最终清理证明。1149位置/108检查/26分支/5槽核验通过仅关闭本容量来源和局部路径疑点；55/22/A7不勾，不据此接线、运行或部署。

## Selected group configuration provenance

实施73补齐所选launch配置+0x20经Job+0x100到core+0x270的复制链；零值直接继承所选group+0x128，默认与活动组构造均清零该字，parent setter不复制配置。未另改的构造配置在已证默认首次构造路径下取得UINT64_MAX；不能把有限容量当作已知故障前提，也不证明当前mutable配置或执行器活性。22导出3971指令与9个独立unwind/LLVM范围2743指令，去重4273位置/82检查/20分支/1槽、173源哈希及Ruff通过。两处内部遗漏由LLVM补齐，初次失败源码保留。见research/newsendmsg-scheduler-config-result.md；实际启动/组切换/关闭协调、状态0最终释放、完整业务映射/适配/真发送及部署仍缺，55/22/A7不勾，无微信操作。

## Launch and external cancellation partial order

实施74以配置组+8的子对象G为基准核对登记锁G+0x78与取消字节G+0xd1：登记返回后才读取消状态/调用Job.start，启动位交换早于core发布及首次恢复提交。126种自有事件合并中65种满足选定分支；在外部取消可重叠、消费方延后且理想串行FIFO的明确假设下，仍存在取消handler先入队。它不证明原生调用者允许该重叠、原生队列FIFO或实际泄漏，但明确了必须另证的外部生命周期协议，不能以相同执行器/TLS/原子位替代。9导出1215指令、59检查/16分支/3槽及62源哈希、Ruff通过；见research/newsendmsg-launch-cancel-order-result.md。55/22/A7和完整映射/适配/真发送/部署仍开放，账号停止约束保持。

## Concrete cancellation producer

实施75将所选空名组切换取消绑定到0x2fc5d68通过默认组提交的正文0x2fec684。零执行器配置从组继承；只有同一全局服务/接口实例且配置未改的条件下，才与所选发送共享配置执行器。这个来源收窄外部重叠假设，但不证明launch跨度不可yield/泵队列/重入、完整关闭或最终参数释放；不能据此放行原生适配。3325位置/63检查、配置链173源哈希及Ruff通过，见research/newsendmsg-group-switch-caller-result.md。55/22/A7及完整映射、真发送、回执与部署仍开放，账号停止约束保持。

## Recipient prerequisite can await before text submission

实施76核验0x2ab6388为service/chat_id/隐藏x8返回pair的前置查找；企业及app有独立路线，普通缓存缺失经0x2b4b150及外层两次调用原生等待。filehelper是精确比较标识，其缓存对象走复制、显式更新+0x54/+0xa8和shared包装；不能用UI显示名、返回对象或call_id替代类型1原始parsed chat_id→input+0x90的赋值来源。完整高层入口可能在最终launch之前等待，故执行器TLS或单独launch不yield都不足以提供任意普通函数栈的调用合同；需认可的协程/服务生命周期与异常清理。77位置/35分支/7字符串及4688位置、9位置/RTTI补核通过，见research/newsendmsg-recipient-lookup-result.md。可变比较初始化及所有间接变更未全证，完整网络字段保持/适配/真实回执仍缺，保持账号停止与产品拒绝门。

## Owned native text input component (implementation77)

实施77已新增研究组件，以已核验0x77bdd0无参/隐藏x8的shared工厂、payload虚表、低/高类型零初值和两个已构造的libc++ string字段为边界。只注入工厂、真实string assignment ABI和调用方另证的期望虚表；先检查身份/初值，再复制chat_id到+0x90和正文到+0x5c8，最后写低类型1。构造失败不暴露半初始化对象，由shared owner释放；不构造protobuf或Task、不解析category、不提供加载器/地址绑定/调度/发送。自有Apple ARM64汇编与C++夹具核验隐藏x8、普通/长/Unicode/特殊category正文、故障与共享所有权。严格/UBSan构建各21场景、1998指令/30位置/7独立BL及精确string assignment导入核验通过；ASan及最小程序均超时，保留限制与失败证据。见research/newsendmsg-text-input-owner-result.md。该组件不是完整适配或任意文本端到端保持证明；查找前置条件、最终record、协程/取消及真实回执继续开放。

## Text service returned value ABI (implementation78)

现有服务导出显示0x317df64保存x8，最终交给0x3189980；后者先等待future，再从typed值复制首8字节、+8的libc++ string和+0x20的shared pair，共0x30字节。实施78已核验getter/消费侧与正常析构，新增非平凡返回ABI声明；+0x20目标保持opaque，不猜业务名。严格/UBSan各7场景、1629指令/58位置/10独立BL及RTTI字面量核验通过，见research/newsendmsg-text-service-abi-result.md。服务内部等待意味着执行器TLS检查仍不等于合法协程栈，类型声明和自有夹具不提供调度器/加载器/实际调用资格，也不证明真实回执。

## Initial-resume submission span (implementation79)

实施74/75仍缺的是所选launch能否被同执行器的取消生产者重入。实施79先限定job首次start交换位之后、恢复闭包提交之前的正常路线：0x667e734→0x667378c→0x667a110及0x66738d4→0x6673990。核验该跨度内实际直接callee、虚调用和可变回调入口；如仍有未解析间接入口，保留边界而非遍历所有日志/单例。只读冻结文件，不执行目标，不变更产品或已有原生调度组件。

实施79结果见research/newsendmsg-launch-span-result.md：core构造中的0xa517a48创建通知发生在Job保存core pair前，可在递归锁内直接调用无执行器监听器，也可向监听器自己的执行器提交。0xa517ac0经精确导入确认是初始化guard，不能当关闭通知的debug开关。TLS清string和名称getter已拆明，但真实监听集合/效果未证明，故不再沿“同执行器即不可重入”放行；后续必须证明具体生命周期协调或原生参数完整释放。19导出1883位置/72检查/33分支/5导入、96源哈希和Ruff通过，仅关闭有界调查79，不关闭55/20/22/A7；不改产品、不操作微信或部署。

## Text auxiliary provenance (implementation80)

旧数据库切片只证明aux为空时低类型1选择两类no-op处理器。此轮连接record构造的零pair、低类型setter中的prepare、aux的两种具体shared factory、安装helper及record copy/move；核验非空prepare是否直接保留原对象。以此明确“已存在但有已证来源的aux”与未知既有aux的区别，不将条件性质扩大为全链正文保持；其他callee仍需独立副作用合同。仅冻结静态分析，保持账号停止、产品拒绝门及A7/55/22等开放项。

实施80补齐正常返回的setter→prepare→具体aux工厂→pair安装及copy/move身份合同。非空prepare直接返回，两类aux的+0x10均为ret；高类型setter的aux写入门仅低类型49成立。该结果把“已证明来源且只经过复制/移动”的非空对象与任意既有aux分开，不扩大为所有中间callee保持正文。25导出3286位置/101检查/27独立控制转移/2槽/108哈希及Ruff通过，见research/newsendmsg-text-auxiliary-result.md。原9个开放项和A7不变；下一步核验setter后到文本准备前的metadata/名称映射变更，不再把这两类局部调用重复列为未知。

## Text preparation overwrite ordering (implementation81)

构造期metadata/名称变更早于文本准备，不能仅因它们存在就推断最终正文被覆盖。此轮用0x3105a98全部留存原始指令的本地CFG核验：第二次动态类型检查成功后，正文赋值与后继DB调用、返回之间的支配关系；同时对照首个validator成功但第二次cast失败的可达路径。直接BL/条件分支目标从机器码独立解码，调用边统一仅建正常返回边并显式保留外部callee、异常及并发限制。只读冻结文件及已留存导出，不接产品、不加载目标、不恢复任何微信活体操作。

实施81已核验659指令与101独立控制转移：第二次cast成功后正文赋值0x3106394支配正常返回及typed DB调用0x31063bc；仅首validator成功不能保证，图中存在绕过正文的回退witness，但未证明实机可行。metadata输入+0x5e0到record+0x230对象string+0x18的赋值先于正文输入+0x5c8到record+0x130；下一边界为0x30db798可能返回替换记录。见research/newsendmsg-text-prepare-order-result.md；外部callee/异常/并发和整链字段保持仍缺，原9项及A7不勾，无微信操作。

## Database result record provenance (implementation82)

以0x32cf5e8完整连续指令的本地正常返回CFG检验三处直接发布和一处插入作业提交是否覆盖全部正常返回。结合x20入口记录的所有本地定义，排除在已选复制出口前被另一个record指针替换；异步capture复制/移动和0x326a144修改边界分别核验。调用边仅按AAPCS64正常返回处理，callee别名/全局修改及异常和并发保持未证明；本轮不恢复微信操作。

实施82证明0x32cf5e8全部本地正常返回经过三处直接复制发布或一处插入提交，出口前x20均由入口record而来；capture复制支配提交，invoke先移动再经0x326a144修改后发布。因此后续字段保持调查应聚焦callee和共享子对象修改，不能继续把未知替代查询record作为此处来源缺口。1944位置/45检查/311独立控制转移/31源哈希及Ruff通过，见research/newsendmsg-database-record-outlets-result.md。该性质仅本地正常返回，不提供完整业务字段、协程/取消排空、真实发送或部署证明，原9项/A7保持开放。

## Insertion mutation and copy domains (implementation83)

本轮将0x32961a4及其时间/source/metadata准备拆成明确写域，独立解码所选标量store的基址、宽度与偏移；字节比对不替代别名证明。0x4eafe18会写metadata及嵌套缓存，禁止把长度计算当只读。record copy的字符串、byte vector、内嵌metadata与shared整数/aux必须分别建合同；既不把共享aux误当深复制，也不把metadata合并的顶层分配扩成全部嵌套所有权证明。仅新增冻结导出和核验资料；未证明的callee、别名/并发及最终字段保持继续列为缺口，不接线、不部署、不恢复微信操作。

实施83已核验所选原record写域、9个metadata缓存store、byte vector扩容、名称比较thunk及11个metadata顶层分配/merge分支；三个shared pair的复制及引用递增明确保留对象身份。2110位置/56检查/424分支/27store/91源哈希及Ruff通过，见research/newsendmsg-insertion-mutations-result.md。下一步应核验0x3296b1c/0x3263cd4所接收副本的共享子对象影响；不再将长度函数当只读或整个record copy当全深复制。原9项/A7及整体目标仍未完成。

## Vector consumer exposure (implementation84)

限定两个消费者的参数暴露边界。独立从0x48a1fac机器码推导接受集合，并核验0x3263cd4的类型1跳过路径；该结论仅以进入消费者时低类型仍为1为条件，不反推数据库绑定前后字段保持。对于其他被接受类型，只记录40字节摘要的构造及传参，不遍历整个数据库。插入消费者核验mode2、hidden x8构造和逐字段绑定：完整record会传给访问器虚槽+0x18/+0x30，不能把方法名或未调用setter槽当作只读证明。原有共享local_id写入只作依赖复核。导出缺口必须由冻结字节记录，不能假定缺失指令；账号停止约束和全部整体开放项保持。

实施84已核验接受集合{3,43,10000}、条件类型1跳过、40字节摘要传参及8处带record的访问器虚调用；缺失0x329786c冻结字节实际为BRK #1。13导出2039位置/81检查/364独立控制转移/60哈希及Ruff通过，见research/newsendmsg-vector-consumers-result.md。下一步只核验具体插入字段访问器+0x18/+0x30实现；未关闭全部callee/别名、业务字段/调度/最终清理、完整适配/真实独立回执/部署或原9项/A7。

## Registered accessor value lifetime (implementation85)

从record绑定注册函数的实际15个vtable/offset pair出发核验五类访问器，逐槽独立解码并对标量的完整机器指令作读域判断。字符串与vector不能先假定复制：跟踪隐藏返回值、data/length和owner字段，并区分包装的移动与原载荷拥有。核验仅到已确认绑定包装的虚调用边界，保留实际后端、字段列表是否只含已注册类、别名和并发限制；不据此恢复发送或改产品。

实施85已核验30份连续导出1022位置、59检查/190独立控制转移/15槽/15注册pair/99哈希及Ruff。字符串/vector返回的是借用视图，包装未retain原record存储；不能提前释放源。后续应连接实际字段列表身份和backend+0x48/+0x58的消费合同，不重复把全部具体getter列为未知。见research/newsendmsg-registered-accessors-result.md；原9项/A7及完整目标继续开放，无微信操作或部署。

## Default insertion field-list provenance (implementation86)

所选caller构造空extra-list，operation默认填充经0x4cbaf6c取得record注册列表；节点头0x10使field+0xf0对应node+0x100，复用/追加节点及旧operation复制均显式复制该访问器指针。只以正常构造/复制且无外部/并发列表修改为条件，不伪称注册表全局不可变。查询可写getter中的COW/释放有副作用，后端准备仍为两层+0x10虚调用；0x56f8d94在+a0缓存与0x563f1a8取得之间选择，实际backend身份尚缺。

实施86验证22导出2163位置/74检查/390独立控制转移/4复制对/88哈希及85依赖99哈希复验和Ruff，见research/newsendmsg-insertion-field-list-result.md。下一步核验具体句柄/backend消费，维持借用原存储的寿命要求；原9项/A7及整体目标继续开放，不恢复微信操作或部署。

## Statement identity and conditional copying (implementation87)

实施87将外层包装虚槽+0x10接到connection+0x260，纠正把连接自身相同槽偏移套为绑定接口的风险。新建kind0构造通过0x56455cc的构造阶段虚槽+0x20→0x5693108建立0x9f1cbc0语句；准备、字符串、buffer分别为0x5699d70/0x5699f58/0x569a008。直接分支在statement+0x198 bit0为0时传x4=-1，非空/非负int32长度/成功分配路径明确以真实_memcpy复制入内部存储，CFG核验复制支配成功选择点。借用源仍需活至整个绑定调用返回，可选日志在复制后继续读源。

44连续导出2521位置/116检查/505独立控制转移/5槽/6load/174哈希、两项依赖88/99哈希及Ruff通过，见research/newsendmsg-statement-binding-result.md。构造零flag不能证明配置后的直接分支，旧缓存/池身份及拦截回调捕获/保留仍缺，下一步定点核验0x5640094及拦截配置。完整业务保持、协程/取消最终释放、完整原生适配/真发送/独立回执/部署及原9项/A7保持开放，账号停止约束不变。

## Conditional interception cache ownership (implementation88, partial)

两类setup先保存下层function，再安装带raw processor capture的字符串/buffer function；index是引用参数，invoke须解引用。缓存不能按最初包装是否借用判定最终所有权：字符串对owner=0的有效输入在分配成功后复制，tag3赋值移交owner；buffer先移动包装，在+0x30为空时分配复制，tag4复制共享包装并retain，最后持有者才经0x562e260→0x26f3a48→0x562781c调用free。0x5626f58不检查分配helper返回值，失败路径不构成拥有数据证明。

74导出6412位置/120检查/1285独立控制转移/12槽/4导入/258哈希及87依赖174哈希复验、Ruff通过，见research/newsendmsg-interception-result.md。88保持开放：基础/保存后function身份、raw capture完整寿命及转换helper返回存储的完整寿命仍缺；借用输入至少保持到整次调用全部返回，不能据局部复制或释放链实现提前释放。原9项/A7及完整目标保持开放，账号停止约束不变。

## Interception static lifetime boundary qualified (implementation88)

后续112导出7559位置/191检查/1507独立控制转移及另1原始B/32槽/5导入/2TLV绑定/六组清理形状/371源哈希及前次258哈希复验、Ruff通过，见research/newsendmsg-interception-lifetime-result.md。基础包装初始化连接实际字符串/buffer复制入口；树shared pair拥有processor，statement先清树再清bundle，所选raw function清理仅RET或sized delete，不解引用已经释放的processor。转换存储来自按线程/key缓存，可复用也可free/malloc；返回view不接管所有权。

88只收口有效对象/已知新建配置、正常返回及成功分配、无并发销毁和同TLS/key重入替换条件下的静态边界。实际如何保证这些条件、原生作业/取消最终排空及字段完整保持仍是20/55/22/67的验收内容。下一步回到这些主线，不继续扩大数据库范围；原9项/A7及完整适配、真发送/独立回执/部署均未完成，账号停止约束不变。

## Text service acquisition and local unwind ownership (55/67, partial)

0x268f370以x0 registry/隐藏x8返回service shared pair，描述器键为精确_3d834e75。pending future按_62250804 typed getter取pair；fallback自身也可能等待。两分支前无条件建立当前core guard，零当前core分支仍会读取core+0x288，因此执行器TLS身份不能替代合法协程上下文。正常路径释放guard与optional future；独立LSDA/LLVM补明所选等待/getter/fallback异常先析构guard，再析构optional future后继续展开，guard构造失败只清理已经构造的future。此为局部边界，不覆盖清理器抛出及所有异步拥有者。

builder保留取得的service pair，构造正文时移入body+0x60/+0x68，再供0x317ded4使用；不可用固定裸指针或外层call_id代替。3662冻结指令位置、106检查/705独立控制转移/4槽/4导入/4个LSDA调用位置/78源哈希与Ruff通过，见research/newsendmsg-service-acquisition-result.md。当前core持有不等于新Job启动租约或服务关闭协调；55/67/22/A7、状态0取消最终释放、完整映射/适配/真发送/独立回执/部署仍开放，账号停止约束保持。

## Core publication and external cancellation admission (55, partial)

research/newsendmsg-core-publication-result.md补明：早期启动位不发布后写入的core pair；已启动取消handler及其state getter无空值回落，必须另有发布与生命周期保证。同执行器且无yield/重入的消费约束只解决发布前读取，不阻止外部生产者在首次恢复提交前先提交取消。完整适配须保证真实启动/外部取消生产者的协调或证明状态0最终释放；自有正文门、指针/TLS快照和配置位均不替代此条件。210种抽象顺序不是原生调度执行证据，无崩溃观测，不改原生字段、不手工释放、不接线或部署；原9项/A7与账号停止约束保持。

## Direct receipt evidence and unknown preservation

直发回执显式使用内部receipt_mode，跨query_history/run_query/query_messages保留原始正文并输出outgoing。仅旧形态明确整数isSender支持方向结论；4.1.15的Name2Id不含可信自身份，不能猜。严格闭包要求outgoing is True，未知方向返回None；轮询不再把None或非法返回值当成功查询。普通查询/UI默认不变。pending/禁止重试集成已用合成数据库和假发送器验证；新消息唯一性、服务端送达与完整原生适配继续开放，不据此启用驱动或部署。见research/direct-receipt-evidence-20261018.md。
