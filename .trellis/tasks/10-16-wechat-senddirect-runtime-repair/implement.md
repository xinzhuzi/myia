# Implementation

> **2026-10-16 账号安全停止约束（优先于下列历史步骤）**：用户已报告账号安全重新登录提示。停止微信附加、注入、发送以及截图/AX/激活/键盘/剪贴板/登录/重启操作；自动goal续跑只可处理本地文件和离线证据，不得恢复活体验证或继续要求用户配合测试。旧授权均已消费；本机提示条夹具通过不构成恢复条件。A7未完成。事实、局限及本轮界面操作见 `research/account-safety-stop-20261016.md`。

用户已在现有研究报告后明确要求解决问题，本轮落实其修复指令；不重复申请实施许可。活附加另受目标/用途/时限授权限制。

1. [x] 读取task-tiers；先完成L1再推进L2，L3未放行。
2. [x] 15项事故回归：开配置时doctor不得调execute_send或LLDB；dry-run不得解析PID/LLDB/触发发送；正常CLI拒绝先于取钥/目标解析/PID/占位；raw batch与改锚身份都不能绕过。
3. [x] 实现纯磁盘校验、已证伪配方拒绝及旧驱动拒绝门；不变更其他发送通道。
4. [x] 复用留存Ghidra工程只读导出13个函数；4611条指令/18444字节全部匹配。完成五字段buffer原型及14项假内存回归，记录Task复制/析构边界与未知项。
5. [x] fresh验证：微信桥+桌面资源三项845 passed/14 gated skipped；ruff通过。两套实际安装件被动检查runtime_calls=0，真实启动器cwd=/的dry-run及拒绝路径均无运行时子进程。
6. [x] 0.9.1三方锁与golden同步；备份72个代码/元数据文件，校验后同步独立桥7文件及桌面Python本地wheel；其他依赖不变，原生原型不装机。
7. [x] 更新可执行spec、任务验收与research/verification.md；不提交/归档/启停微信。具体callback/完整生命周期/合格清理执行器及授权后真E2E保留开放，禁止称整体直发完成。
8. [x] 用户要求按层纠正版本JSON：先核验4.1.15(270135)实际磁盘，再备份共享锚表；将失效入口/队列/服务/捕获不变量/ABI字段置null。两套安装件读取、doctor、CLI演练及拒绝路径通过，runtime_calls=0；77项回归通过/1项真机门控跳过。A7和L3继续开放。
9. [x] 用户明确授权一次前台只读观察，最长30秒。独立研究执行器先完成9项真实内嵌LLDB清理验证；实际只附加1次，21.053秒收尾，同PID/启动时间、非停止态、P_TRACED清除且零调试器残留。未自然命中，不重试、不发送；授权已消费。
10. [x] 复用Ghidra只读工程追出默认普通回调注册链；0x465756c仅返回0。10函数633条指令2532字节全部匹配，按SDK独立解码dyld修复链确认虚表槽；详见research/observation-and-callback-result.md。
11. [ ] 证明真实正文Task、CGI/cmdid、包装与完整外部上下文生命周期，再实现可发送适配；当前授权不含发送，A7保持开放，产品拒绝门保持。
12. [x] 离线追出0x4634710通用请求生产链及0x4635b9c完成处理；实现基础MMReq wire包装（required零值/false保留），5项独立protobuf测试和15项被动回归通过、6文件Ruff通过。请求+0x68完成functor及条件析构已定位，文本专用构造/路由和账号扩展仍开放；未附加、未发送、未改产品JSON。详见research/mmreq-envelope-and-ownership-result.md及mmreq-slice-validation.json。
13. [x] 从密文字面量定位并核对newsendmsg原生路由：CGI=/cgi-bin/micromsg-bin/newsendmsg，编号522，工厂0x30c2c1c分配0xe0请求、构造器0x30c2de4、虚表0x9de8268，完成functor接入+0x68，序列化入口0x30c2ed8读取+0x78 protobuf。具体条目字段、上游捕获对象与运行时服务/回执仍未终验；不回填旧schema3执行配方。
14. [x] 进一步留存请求及7个条目wire字段、必填mask0x1d和两个原生生产者来源偏移至research/newsendmsg-4115-static-contract.json。98份导出21883条指令/87532字节匹配，完整consumer另487条匹配；12个虚表槽dyld独立解码通过，新脚本Ruff通过。条目原始字段名/业务语义、上游functor捕获、账号扩展、活体服务和真实发送仍开放。
15. [x] 内层wire编码8项、固定对象身份5项、基础包装5项及被动入口15项通过；字段5哈希的208字节原生叶函数在独立进程对604组合成数据与Python逐项一致。上游完成functor的shared捕获/克隆/析构、首次context决议及原生账号服务来源已证明；调度器线程合同仍开放。
16. [x] 新观察器先通过10项真实LLDB隔离清理测试；用户明确授权后仅执行1次只读窗口，3.822秒完成固定服务身份匹配，成功脱附、同PID/启动时间、非停止态、P_TRACED清除、零残留，无原生调用或发送。授权已消费，见research/live-observe-xk07n8e9/supervisor.json。
17. [x] 实现独立C++完成状态与native body RAII组件，不含加载器或活进程访问。回调ABI/heap转交/首结果保留/shared释放16项、正文构造/解析失败清理9例通过。它们是研究组件，未装入产品；本机ASan连最小布局探针也超时，普通编译运行通过，不声称sanitizer通过。
18. [ ] 核验业务字段输入及原生co调度上下文，完成可执行适配与真实发送回执；不能把服务快照或25项C++离线检查当作完成11/A7。
19. [x] 补录编号响应字段和高层真实x0～x3/x8 ABI；定位co/线程局部组及默认组0xa518700，尚不放行任意线程调用。最终165份函数导出（含重复）28009条指令/112036字节及完整consumer另487条匹配。identity-slice-current-verification.json核对当前合同/C++哈希、已消费授权拒绝、未变化的测试证据与同一微信实例健康状态；33项Python测试、C++16项/9例均通过，未新增附加/调用/发送。

## 用户要求按建议全部完成（2026-10-16，goal active）

20. [ ] 从取消functor与native任务移除链核验超时、回调并发及请求析构；明确不在LLDB表达式里阻塞等待。
21. [ ] 从原生生产者/记录访问器证明收件人、正文、类型、时间及客户端标识输入；不以旧协议字段名猜当前布局。
22. [ ] 连接正文、factory、拥有的回调与响应复制，形成默认不附加、不装机的完整研究适配器，并以真实host ABI及隔离服务夹具验证正常、拒绝、超时、取消、晚到回调、析构和回执判定。
23. [ ] 完成可审查的单次限时发送实验及清理资格验证，再明确测试收件人/正文并请求新的目标/用途/期限授权。授权前不附加、不注入、不发送。
24. [ ] 在授权范围内执行一次真正发送、独立核验回执，全部验收通过才接入产品及本机两个入口；任务未完成前不提交/归档/复用旧授权。
25. [x] 补出服务取消的精确槽/this调整、ready门和map删除路径，确认队列中取消不调用completion、OnTaskEnd取走后可晚到；证明原生factory/回调之间必须共享发布mutex。新增响应RAII、组合operation和编号响应解析器；5个C++夹具16/9/8/11/1检查或场景、100次取消/完成竞态、41项Python/122 subtests及5文件Ruff通过。182份函数导出28949指令/115796字节、consumer487指令及20个dyld槽独立核对。详见research/newsendmsg-cancel-response-result.md与newsendmsg-integrated-verification.json；没有附加/原生调用/发送/产品接线，业务映射、co上下文、底层排空与独立回执仍开放，20～24不得勾完成。
26. [x] 通过冻结薄片精确列名字面量→xref→0x4cc245c字段binding及访问器，得到message_content/+0x130、create_time/+0x114、source/+0x160、server_id/+0xf8的独立静态证据；0x4cbf804/0x4cbc3ac双向同步local_type/+0x108与type缓存/+0xc。业务同类型关联、收件人方向及client-ID仍未完成，详见research/newsendmsg-business-field-investigation.md；不据此启用适配。
27. [x] 为补齐自然发送的业务字段和线程证据，新增独立factory只读观察器。用户确认手动测试为文件传输助手/“今天真是个好日子”，尚不构成附加授权。22项合成字段测试、12项无副作用授权门及既有研究/被动回归合计75 passed/122 subtests；新C++对象图夹具的真实LLDB清理10场景通过。真实模式关闭协议包日志，仅保存摘要/长度/编号数值/线程栈；观察方案见research/newsendmsg-factory-window-plan.md。未附加微信、未发送、未接入产品；需要新的单次明确授权，A7继续开放。
28. [x] 用户对call_ZJjALN9NhvT4oT0BepKttldH明确授权一次前台只读窗口（最长30秒）后执行。21.173秒、1次附加，服务身份匹配、单个硬件断点未命中；到时成功解除，同PID/启动时间、非停止态、P_TRACED清除、零辅助残留。真实窗口无协议包日志，无注入/原生函数调用/自动发送；授权已消费，独占标记拒绝复用。用户随后明确“窗口结束后才发送”（call_72ObGIUvW72rjqdTzUODzHns）；发送与窗口不重叠，因此本次未命中不能用于判断普通文本调用路线。见research/live-observe-ccgpziio/supervisor.json及factory-window-result.json；A7未完成，不重挂。

29. [x] 用户澄清上一次手动消息在窗口结束后发送，已补记无时间重叠、不能用于判断路线；随后确认输入框已准备且尚未发送。独立第二窗口执行器与授权/消费命名空间已准备，14项无副作用授权门和10项真实LLDB自有夹具清理通过，五文件Ruff通过；真实预检拒绝缺失新授权，没有附加微信。详见research/newsendmsg-factory-second-window-plan.md。新授权未取得、窗口未执行，A7继续开放。

30. [x] 用户对call_1AR09zdZbwO3yE2UDfAnQbZb明确授权后，独立第二工厂窗口执行一次，21.048秒安全结束，身份符合、未命中、同实例继续运行、P_TRACED清除、零辅助残留。模型端就绪检查混用两种时钟，首次剩余值不可用；未发出可以发送提示、未形成有效人工发送对照，不能据此否定调用路线。新授权已消费、标记保留，不重挂；后续先修正本地就绪提示机制。见research/factory-second-window-result.json；A7未完成。

31. [x] 账号安全停止约束下仅推进离线调度生命周期核验。新增15份函数导出，累计240份/40175指令/160700字节匹配；完整consumer另487条匹配；新增2个调度槽独立dyld链解码，19个原始指令位置检查及3脚本Ruff通过。确认运行标志清零早于正文function销毁、完成入口标志和结果发布早于末尾用户回调，不能当作排空或卸载屏障。见research/newsendmsg-scheduler-lifetime-result.md及对应合同JSON。没有运行微信或LLDB，没有产品/安装件/实际版本JSON改动；A7及20～24仍未完成，停止约束保持。

32. [x] 继续仅在冻结薄片核验取消派发：已启动handler向协程核心传递-1并检查状态3/正文尚未进入，未启动handler直接进入完成处理。原始指令证明Ghidra省略了取消码x1；不能照抄单参数声明。新增6份函数导出，累计246份/41483指令/165932字节匹配；consumer另487条匹配，16槽中新增2个取消invoke槽独立dyld链核验，脚本Ruff通过。设计中明确作业取消与网络请求按task_id取消分别处理，均不足以证明排空。见research/newsendmsg-cancel-dispatch-result.md；没有微信/LLDB/账号操作，没有产品接线，A7及20～24仍开放。

33. [x] 仅用留存导出固化作业ABI研究声明：完整入口x0/group、x1/config、x2/body、x3/finished，非平凡16字节句柄通过隐藏x8返回；简化入口省略finished。新增自有汇编/C++夹具，实际捕获寄存器并验证空句柄返回、正文/完成回调及shared/weak持有释放，5场景通过；13个原始指令位置与源哈希核验，新Python脚本Ruff通过。证据见research/newsendmsg-job-abi-result.md及newsendmsg-job-abi-verification.json。未加载/附加/操作微信，未修改产品/真实版本JSON或装机；真实group/config、线程、排空及实际直发仍未证明，A7及20～24保持开放。

34. [x] 补核作业function内部调用ABI：自有汇编按原生形状读取erased对象并调用虚表+0x30，内联/堆正文及内联/堆布尔完成回调4场景通过；11个原始指令位置与源文件哈希核验，新脚本Ruff通过。确认完成bool来自作业取消路径，不是发送/送达成功标志。见research/newsendmsg-job-erasure-result.md及newsendmsg-job-erasure-verification.json；上一切片夹具与证据未修改、未重复运行。没有微信/LLDB/账号操作，无产品接线或装机，A7及20～24保持开放。

35. [x] 仅离线补齐客户端标识输入合同：生产对象+0xb8非空缓存复用，record+0x18经标识格式化链提供时间/本地编号或既有string，固定后缀按原始字节读取为_xwechat_；64位计数器消费加一前原值。研究JSON字段5已补证，6份定点导出769指令及19个关键位置/后缀/thunk核验通过，新验证脚本Ruff通过。见research/newsendmsg-client-id-source-result.md；计数器初始化/线程序列化、记录方向和文本type、完整适配与独立回执仍缺。没有微信/调试器/账号操作，无产品或安装件修改，A7及20～24保持开放。

36. [x] 离线核验context构造/factory生成同一record虚表并保存shared pair；完整到producer的派发仍开放。确认local_type由+0xc低32位和+0x10高32位组成，两个setter分别写半字段后同步64位到+0x108，wire field3只取低半；不能把孤立写1分支定为普通文本。13份导出4903指令/21位置及新脚本Ruff通过，见research/newsendmsg-record-input-result.md和对应合同/验证JSON。未运行/附加/操作微信，未改中央研究JSON、产品/实际配方/安装件，A7和20～24未完成。

37. [x] 沿context调用者离线定位两条payload类型输入链：+0xe4/+0xe8对应两个getter，精确常量为49/1和49/51，另一虚槽恒1不能误作wire类型。22份导出5576指令、11关键位置、2常量、6虚槽dyld链及新脚本Ruff通过，见research/newsendmsg-input-type-result.md及对应合同/验证JSON。普通文本type/完整派发仍开放；无微信/调试器/账号/发送操作，未改产品和安装件，A7和20～24未完成。

38. [x] 仅离线补证类型1正文转换：基础构造类型两半为0/0，真实转换器入口0x4c6eff4设低类型1并复制source+0x130/+0x148至新payload+0x5c8/+0x5e0，隐藏x8返回shared pair；0x4c6f030是内部指令，不是可调用入口。公共helper另复制+0x350并设+0x7c=2，不混为类型字段。6份定点导出232指令、32关键位置和4槽dyld链通过，新验证器/模式扫描脚本Ruff通过，见research/newsendmsg-type-one-content-result.md及对应合同/验证JSON。完整发送身份、派发、方向、线程/排空和独立回执仍未证明；没有微信/调试器/UI/账号操作，未改产品或安装件，A7和20～24未完成。

39. [x] 仅离线追出上一转换器所属对象及数值1派发：0x4c6eff4属于选择值49/115所建对象的+0x18槽，当前选择器调用+0x10槽，不能倒推为普通文本输入。数值1使用0x9ead718虚表，公共工厂输出0x9eba160类型，区别于已确认数据库record的0x9eb04f0；+0x148等相同偏移不能复用字段名。10份导出2061指令、39关键位置、4槽dyld链及精确16字节announcement@all常量核验，新脚本Ruff通过，见research/newsendmsg-conversion-dispatch-result.md及合同/验证JSON。仍需正向连接发送context、证明业务方向/线程/排空和独立回执；无微信/调试器/UI/账号操作，无产品或安装件修改，A7和20～24未完成。

40. [x] 仅离线从context正向追出按key入队、状态筛选、移除、第二队列及捕获context shared pair的异步回调；作业wrapper原始x0～x4/隐藏x8合同已核验。后续handler的+0x90零结果方法与+0xd8发送producer不同，不能把阶段返回或入队作为发送成功。9450指令、54关键位置、4个dyld槽和constructor thunk匹配冻结文件，新脚本Ruff通过，见research/newsendmsg-forward-queue-result.md及合同/验证JSON。较早准备阶段/handler注册身份到producer的派发、业务方向、真实线程/config/排空及独立回执仍缺；无微信/调试器/UI/账号操作，无产品或安装件修改，A7和20～24未完成。

41. [x] 仅离线补证准备结果成功/flag/非空handler后的状态3阶段：原始x0/handler、x1/context shared pair、隐藏x8/result；kind1还依input+0xd8字节选+0x80/+0x88，已知表后者重定向前者零结果方法。dyld准确解码+0x78=0x30bcd9c，排除误用0x30d7958；两条后继通知分别转入handler+0x18/+0x90容器，实际通知目标仍缺。13份导出8891指令、39关键位置、5槽及重定向x8保留核验，新脚本Ruff通过，见research/newsendmsg-state-three-result.md及合同/验证JSON。没有微信/调试器/UI/账号操作，未改产品或安装件；producer连接、业务方向、线程/排空与独立回执仍未证明，A7和20～24未完成。

42. [x] 离线确认旧已知表0x9de7f68注册为LocationMessageHandler；数值1对应名称TextMessageHandler的工厂生成0x9de9a68。文本+0x78准备方法复制input+0x5c8正文至record+0x130，+0xd8的0x3107b0c按已证明编号字段构建请求并调用共用0x30bee20；不是沿Location业务输入继续推定。两条signalslot通知的直接/执行器分支和record副本invoke已定位。19份导出7494指令、66关键位置、9槽和两个精确名称核验，新脚本Ruff通过，见research/newsendmsg-text-handler-result.md及合同/验证JSON。实际服务注册表到文本producer派发、输入类型/方向、线程/config/末尾排空和独立回执仍缺；无微信/调试器/UI/账号操作，无产品/实际JSON/安装件改动，A7和20～24未完成。

43. [x] 离线连接实际服务注册表与文本选择链：0x317ba5c以x0=service+0xb20所指storage、x1=storage+0x28、x2=弱参数调用0x30e3fb0；两张表分别保存name→handler shared pair与type key→name，0x319a6a8在同一storage查表并通过隐藏x8返回所选pair。补证handler+0x18接收方0x317d1cc复制记录并发通知，+0x90接收方0x317d4ac转发至service+0x228；不当作producer或回执。14份导出5274指令、67关键位置及新脚本Ruff通过，见research/newsendmsg-handler-registration-result.md及合同/验证JSON。context到文本producer、输入方向、线程/config/排空及独立回执仍缺，A7及20～24未完成；无微信/调试器/UI/账号操作，无产品/安装件改动。

44. [x] 离线补证第二队列到文本producer的条件派发：状态6/非空所选handler门后设状态7并构造捕获context/handler shared pair的作业，invoke 0x32243a8经0x3224fe8前置+0xd0零结果门设置状态10，再由真实入口0x30d692c调用+0xd8的文本producer 0x3107b0c。原生错误0x66及辅助bit条件下仅第二次helper调用、结果发布后继续队列均已定位，不代表实机执行/成功回执或调试重试许可。8份导出2950指令、92关键位置、3槽独立dyld解码及有边界模式扫描通过，新脚本Ruff通过；见research/newsendmsg-producer-dispatch-result.md及合同/验证JSON。输入构造/方向、线程/config/排空、完整适配和独立回执仍缺，A7及20～24未完成；无微信/调试器/UI/账号操作，无产品/实际JSON/安装件改动。

45. [x] 离线补证一条数值类型1输入到发送服务的身份链：工厂0x77bdd0的payload虚表前RTTI槽解码为0x9eb2598，与文本准备dynamic_cast目标一致；真实入口0x291fb70在类型1分支写低值1并复制正文至input+0x5c8，捕获同一input shared pair，作业0x292ef9c经0x317ded4进入0x317df64。包装器第三参数1是context flag，不能混作消息类型。12份导出3467指令、75关键位置、6槽独立dyld解码及新脚本Ruff通过，见research/newsendmsg-text-input-path-result.md及合同/验证JSON。builder参数/完整前置条件、方向、record替换关联、线程/config/排空和独立回执仍缺，不声称全部UI文本入口已证明；A7及20～24未完成，无微信/调试器/UI/账号操作，无产品/真实JSON/安装件变更。

46. [x] 离线补证文本准备0x30db798从future提取新record并以+0xf4非零为门替换context shared pair；构造边界的正文string复制/移动及结果容器虚槽返回的类型名称精确对应。未将容器+0x280的另一类型指针误判为getter类型。19份导出4697指令、90关键位置、3槽dyld链及2名称核验通过，新脚本Ruff通过；见research/newsendmsg-record-replacement-result.md及合同/验证JSON。0x326a144的外部记录修改与其他lookup分支、方向、线程/config/排空、完整适配和独立回执仍缺，A7及20～24未完成；无微信/调试器/UI/账号操作，无产品/真实JSON/安装件变更。

47. [x] 离线补证条件性插入回调的local_id来源：vector副本与原record共享+0x208/+0x210整数单元，operation bit0成功且flag==1才回填+0xf4。确认低类型1新建辅助对象两条+0x10均为ret，但source仍有更新，不推定整个正文路径保持。父方法w24在lookup后改为返回字节，不能将后续条件误作原始w4。41份导出5978指令、74关键位置、4槽dyld及新脚本Ruff通过，见research/newsendmsg-record-database-result.md及合同/验证JSON。全部lookup分支、既有辅助对象、收件人方向、线程/config/取消/排空和独立回执仍缺；A7及20～24未完成。没有微信/调试器/UI/账号操作，没有产品/实际JSON/安装件变更。

48. [x] 离线补证server_id门后的0x335bfac回调及0x335c0f0清理：capture参数为x0，移动service pair后调用0x3274034，低字节经future发布；0x56f3a00/0x56f3be0通过隐藏x8写结果，父方法非零分支经0x335bddc复制原record，不是query返回替代record。标签完整业务语义仍未证明，不当作查询命中或发送回执。9份导出2066指令、56关键位置、1精确类型名称及新脚本Ruff通过，见research/newsendmsg-server-id-query-result.md及合同/验证JSON。其他分支、收件人方向、线程/config/取消/排空、完整适配和独立回执仍缺，A7及20～24未完成；没有微信/调试器/UI/账号操作，没有产品/实际JSON/安装件变更。

49. [x] 离线补证一条JSON到类型1输入路线：0x286fbac→0x291d53c→0x291dab8按隐藏x8返回解析对象，+0x48成功门后交给0x291fb70。精确字段chat_id/message_type/content_xml_base64/content_xml由冻结字节对应；chat_id复制到input+0x90/context+0x38，直接内容或转换后的局部正文复制到input+0x5c8。协调器转发的原x2字符串不是解析后的chat_id；其身份及最终收件人方向仍缺。8份导出5320指令、65关键位置、4字段及新脚本Ruff通过，见research/newsendmsg-builder-json-result.md及合同/验证JSON。上游/可选/错误语义、记录变更、线程/config/取消/排空、完整适配和独立回执仍缺，A7及20～24未完成；没有微信/调试器/UI/账号操作，没有产品/实际JSON/安装件变更。

50. [x] 仅离线补出chat_id到普通请求字段1的条件连接：input+0x90写入allocation+0x48，即record+0x30；getter特殊分支依0x4cbd624选值的@qy_u/@qy_g后缀及辅助对象，含@weclaw的结果另走路线。8份导出4068指令、48位置与精确常量/前置哈希核验通过，新验证器Ruff通过。见research/newsendmsg-recipient-route-result.md和验证JSON；research/completion-gap-audit-20261017.md明确业务路线、执行/清理合同、完整集成、真实回执四项缺口，防止继续以导出数代替交付。完整收件人语义、替换/变更保持及其余缺口仍未完成；A7及20～24未勾，没有微信/调试器/UI/账号操作，没有产品/实际JSON/安装件变更。

51. [x] 新增自有job→ResearchOperation→factory→callback/response的组合夹具，使用已有LaunchJob类型及Python wire编码；10场景覆盖正常、启动前/后取消、超时、晚到回调、拒绝、factory异常不重试、句柄销毁及仅取消作业不足以取消请求。首次错误地假定std::function移动后源必空，实际失败后修正，失败源码/日志保留；v2的C++严格编译、对象配平、输入副本检查及验证器Ruff通过。见research/newsendmsg-job-operation-result.md与research/job-operation-integration-20261017-v2/verification.json。仅补实施22的组合夹具，不是原生调度/完整适配/送达证明；A7及20～24仍未完成，账号停止约束保持，无微信/调试器/UI/账号/发送操作，无产品/实际JSON/安装件变化。

52. [x] 离线补证job的promise/future共享同一state，结果发布先于关联通知和最终function；普通等待及协程已就绪分支都不等待最终捕获销毁。独立解码析构槽并追至0x667f128，明确完成function在job析构时才另行销毁；其后释放promise/future等引用。15份定点导出共2703指令、84位置、2析构槽及精确类型名称通过；自有门控并发夹具2场景严格C++编译通过，两验证器Ruff通过。见research/newsendmsg-join-boundary-result.md及两个验证目录；design明确join/回调返回不得作为排空或卸载屏障。最后原生拥有者、排队接收方/基类清理和真实线程/config仍缺，A7及20～24保持开放；无微信/调试器/UI/账号/发送操作，无产品/实际JSON/安装件变更。

53. [x] 离线补齐正常返回的job/core持有与释放：core参数strong持有job，最终function返回后清理参数并清零清理器，随后core状态变3；作业组有效直接通知先移除job节点，执行器闭包另持有core。明确通知闭包的接收方shared pair与raw job参数、两处基类断开/延迟释放分支。33份定点导出4228指令、53位置及7槽dyld链核验；自有group/core/job与既有ResearchOperation组件组合2场景严格C++验证通过，确认外部句柄延后析构及job/core销毁后晚到请求响应仍独立持有/释放，Ruff通过。见research/newsendmsg-core-teardown-result.md及core-teardown-20261017/verification.json。正常路径持有链疑点已补齐，异常/取消/真实执行器及完整排空仍缺；A7及20～24未完成，无微信/调试器/UI/账号/发送操作，无产品/实际JSON/安装件修改。

54. [x] 补证Ghidra未恢复的异常处理落点：冻结Mach-O unwind/LSDA与系统LLVM完整范围1649指令、21位置、8处call-site及两种精确RTTI对应；正文两种原生类型处理与最终function向外展开边界已明确，正常清理顺序不能推广到回调抛出。新增仅用于自有最终通知的异常保护组件，8场景/32路并发及真实host ARM64虚槽调用通过，3脚本Ruff通过；不以catch-all替代JobBody原生处理。状态0取消仅写结束标志，不证明参数清理；真实执行器顺序及此分支最终释放仍开放。见research/newsendmsg-exception-boundary-result.md及exception-boundary-20261017-v2/verification.json；A7及20～24未完成，无微信操作、产品接线或部署。

55. [ ] 从已确认builder/发送作业的config来源定位实际执行器，核对启动与取消是否在同一对象上串行、是否有内联派发及队列保留引用；以此判断状态0取消的可达性和最终参数清理路线。仅凭配置字段相同或状态3不得放行；账号停止约束保持。

    55后续进展（2026-10-18，仍未勾）：补齐恢复闭包的可选条件function与独立core pair布局，纠正capture+0x18虚槽+0x30为执行器线程检查的待查假设；初次恢复明确传空条件。原生组取消锁内直接调用Job.cancel，再由Job向执行器提交handler，不能仅凭共用执行器证明首次恢复先于取消。状态0取消写3后正常返回，后到恢复见3直接跳过；组通知、闭包和core析构均未直接补出参数清理，但未证明所有间接副作用或真实可达性，不报告已发生泄漏。20导出2805指令、69位置/23独立分支/5槽、两个限定状态前缀及Ruff通过；只读pass394补记入口xref。见research/newsendmsg-state-zero-cancel-result.md及对应合同/验证JSON。下一步查服务关闭/组切换与发送的实际线程及生命周期协调，不手工调用原生清理器。A7、11/18/20～24/55/67仍开放，无微信操作、产品接线或部署。

实施55进展（仍未勾）：已定位服务协程接口、默认/活动group及同一具体执行器，普通submit入队、heap按deadline/sequence排序、正常执行后销毁捕获；46份导出7133条指令、47位置和12槽dyld链匹配冻结文件。新增自有正文启动门及ResearchOperation组合夹具，10+4场景（含32个外线程）严格C++/host ARM64 erased调用通过，新验证器Ruff通过；见research/newsendmsg-executor-start-gate-result.md及executor-start-gate-20261017/verification.json。门仅限制协调器显式取消，原生组/外部取消、状态0最终释放、异常及完整排空仍缺；不能把本切片当成完整原生适配或实机成功。A7及20～24、55保持开放，无微信操作或部署。

56. [x] 固化执行器提交/移除的精确ABI及64位票据，核验移除时的捕获析构、普通调度记录剩余持有及组等待边界；以自有host ARM64虚槽和ResearchOperation组合验证捕获/请求分离，防止将移除返回或组空当排空。只写研究组件，不提供加载器、活体入口或产品接线；不替代实施55的状态0清理证明。16份导出2513指令、48位置/5槽核验及5场景严格C++夹具通过，新验证器Ruff通过；证据见research/newsendmsg-executor-ticket-result.md及executor-ticket-20261017-v2/verification.json。初次初始化编译错误及日志保留，未降低警告等级。A7及20～24、55保持开放，无微信操作或部署。

57. [x] 固化原生JobConfig的0x38字节布局、逐字段继承与登记/启动/取消的优先级；用host ARM64寄存器和原始偏移读取验证，组合现有启动门验证延迟启动前的显式取消。12份导出2237指令、48位置及3槽核验通过；8个自有场景含16分支组合、严格C++编译及新验证器Ruff通过。首次C/C++链接声明错误的编译日志保留，仅改新夹具声明。配置快照不代表原子原生状态，不登记/延迟启动仍受组取消优先分支控制；55及A7保持开放。见research/newsendmsg-job-config-result.md及job-config-20261017-v2/verification.json；无微信操作、产品接线或部署。

58. [x] 修复ResearchOperation取消/超时控制可从任意线程调用的问题：绑定factory线程的独立生命周期令牌，跨线程在状态修改/原生调用前拒绝；保留跨线程响应/观察和晚到结果规则。新增测试实际复现std::thread::id复用导致编号比较漏放，再以令牌解决。8组依赖夹具45场景、100次竞态、新增69次错误线程拒绝、严格C++编译及Ruff通过；13导出2659指令/31位置核验补出服务关闭→组取消/等待→后续服务虚调用顺序，排除仅跳过组登记即可安全接线的推断。失败日志与源码保留，见research/newsendmsg-operation-thread-result.md及operation-thread-20261018-verified/verification.json。仅补55/22的研究组件约束；55、A7及20～24未完成，没有微信操作、产品接线或部署。

59. [x] 补证source重建到普通请求字段6：record+0x240恰为1时更新辅助对象，0x4d1dd74真实ABI为x0输入/隐藏x8返回string，结果覆盖record+0x160；producer仅非空时设置field6。18个顶层字段名/偏移/门及有符号/无符号setter、NUL文本边界已固化到newsendmsg-source-contract.json，metadata byte vector不等于source。15份选择导出3636指令、68位置、13条独立B/BL目标及19名称核验、验证器Ruff通过，见research/newsendmsg-source-result.md和source-mapping-20261018-verification.json。错误抄写的一个构造目标已通过BL解码纠正、无关导出明确排除并保留。嵌套source和精确XML输出、完整record变更/lookup、builder参数来源、原生线程/取消排空及完整适配/独立回执仍缺；A7、20～24及55未完成，没有微信操作或部署。

60. [x] 离线补证发送作业结果到本地记录查询的来源：0x3190538真实x0/service、x1/chat_id、w2/local_id、w3/存储选择值及隐藏x8返回；查询表达式使用record+0xf4，future发布与消费通过精确RTTI相连。额外核验查询后映射替换record+0x18/+0x30，不能假定初始收件人字段保持；本地命中/server_id/回调不等于独立送达。18导出3623指令、166位置、37个独立分支目标、3个dyld槽及Ruff通过；初版与第一次追加验证的抄写错误保留说明，最终见research/newsendmsg-result-lookup-result.md和result-lookup-20261018-v2-verification.json。上游结果生产/映射来源、完整业务链、线程与取消排空、完整适配/独立回执仍缺；A7、20～24、55未勾，无微信操作、产品接线或部署。

61. [x] 离线补齐查询后名称映射来源：Name2Id选择rowid/user_name，批量成功允许缺行且不补查，单键缺失仍可整体返回1；映射已有键不覆盖，后续查缺键插入空string并可覆盖record+0x18/+0x30。第三字段setter精确null跳过、群聊子串/企业后缀回退与隐藏x8返回已固化，前置vector处理不是整record reset。18导出3258指令、211位置、45个独立分支目标、8字面量及Ruff通过；另从冻结字节恢复Ghidra跳过的2个分支并单列，首次连续断言失败诊断保留。见research/newsendmsg-name-map-result.md、newsendmsg-name-map-contract.json及name-map-20261018-verification.json。上游方向/metadata完整schema与账户身份、真实线程/取消最终清理、完整适配/真发送/独立回执仍缺；A7、20～24、55保持未完成，无微信操作、产品接线或部署。

62. [x] 以构造器/虚表/精确类型名确认record+0x190为micromsg.MessagePackedInfo，field1/2为record+0x198/+0x19c的32位varint，双向连到名称映射；不据此命名发送人方向。补证先清理后直接解析、失败无回滚且后续仍查名称，以及群聊条件下从正文冒号+LF/特定类型冒号+空格取前缀的回退。Ghidra parser导出仅62条，另从compact unwind核实全范围并用LLVM补齐833条；17导出2112指令，去重总2883位置、261检查/35分支/7槽/7字面量及两个脚本Ruff通过。见research/newsendmsg-packed-info-result.md、newsendmsg-packed-info-contract.json及packed-info-20261018-verification.json。上游方向/账户身份、嵌套schema、真实线程与取消最终释放、完整适配/真发送/独立回执仍缺；A7、20～24、55保持开放，无微信操作或部署。

63. [x] 补齐账号比较字符串所选安装路线：全局账号→异步捕获→0x467c394构造shared子对象→账号+0x68/+0x70→子对象虚槽+0x18返回+0x48 string；构造输入首string与上游结果+0x70相连，但业务身份与发送人方向仍未命名。纠正工厂/中间方法隐藏x8 ABI，明确最终getter返回借用引用、临时shared在返回前释放，未证明并发替换安全。16导出3532指令、63位置、10分支/6槽/1精确RTTI及Ruff通过；RTTI名称指针高位原样保留，首次错误期望诊断留存。见research/newsendmsg-account-source-result.md及account-source-20261018-v2-verification.json。A7、11/18/20～24/55未完成；上游业务身份、其他替换路线、真实线程/取消最终清理、完整适配与真发送/独立回执/部署仍缺，无微信操作或产品接线。

64. [x] 离线补证登录响应field4/AcctSectResp.field1到结果+0x70的条件生产，但同时发现并核验selector1调用方随后用capture+0x50重写该string，不能直接当作最终账号来源。已连接capture立即构造与结构复制函数，精确业务身份和selector0仍缺。9份Ghidra导出4540指令、LLVM完整parser1088指令（去重5142位置）、186检查/19独立分支/8槽/2类型名及两个脚本Ruff通过；边界从unwind独立重算。见research/newsendmsg-auth-origin-result.md和auth-origin-20261018-verification.json；pass331缺count的失败日志保留，不计成功证据。A7、11/18/20～24/55及四项整体缺口保持开放，无微信操作、产品接线或部署。

65. [x] 补证两条builder的selector0/1及x1首string输入，经两级functor结构复制与thunk进入0x410dc54→0x2fc361c→最终capture覆盖链；selector0所选ready分支连到共同auth consumer，不声称最终值保持。完整LLVM范围/正常控制流逆向定义证明所选x19/x21未受其他分支重用影响，假定AAPCS64保留且不含异常/别名分析。8份Ghidra4172指令、LLVM4246指令，共8418位置、138检查/13分支/3槽、unwind范围重算及3脚本Ruff通过，见research/newsendmsg-login-input-result.md和login-input-20261018-verification.json。原LSDA探针因512字节LEB上限失败，未算作异常证据。业务身份/其他路线、原生线程/取消最终清理、完整适配/真发送/独立回执/部署未完成；A7及11/18/20～24/55保持开放，无微信操作或产品接线。

66. [x] 补证selector0调用点传两个空string；selector1首string来自虚表0x9bf7f90状态+0x18，已连构造器/数值6工厂/map key 0xa51cd78的转换路径及缓存0xa4266c0所选生产。缓存写入时显式传编号键3给0x487929c，未命名业务身份或宣称getter语义/dispatcher/转换保持已证明。16导出3113指令/148检查/25分支/3槽及NUL/RTTI名称、Ruff通过，见research/newsendmsg-login-caller-result.md和login-caller-20261018-verification.json。map/key初始化、完整字段/方向、真实线程/取消最终清理、完整适配/真发送/独立回执/部署仍缺；A7及11/18/20～24/55开放，无微信操作或产品接线。

67. [ ] 回到已证明JSON→文本input→原生发送服务的完整入口路线，核验0x286fbac的上游派发、转发x2的实际来源及调用线程要求；先区分原生自行生成的字段与适配器必须提供的参数，再决定剩余映射/调度工作。优先关闭发送路径缺口，不继续无边界追登录缓存；不操作微信或部署。

    67进展（2026-10-18，仍未勾）：已证明message::send_message注册→实际0x2857ca4调用→0x286fb58的路线；外层chatbot.WxFunctionCallInput的wire2/3/4分别为转发string/命令名/JSON输入，补连0x2660d9c经同一协程接口提交的所选事件路线。24份导出4343指令、132检查/31分支/4槽/两名称及Ruff通过，见research/newsendmsg-command-dispatch-result.md。下一步核验field2在文本作业体和响应中的完整作用及builder前置条件，线程/取消问题回到55；不再无边界追登录缓存。完整适配/真实发送/独立回执/部署未完成，账号停止约束保持。

    67后续进展（2026-10-18，仍未勾）：wire2转发string从x2复制到body+0x18，所选作业正常成功/失败日志均称call_id；服务调用使用独立input pair，查询另取chat_id。clone/析构及callback移动清零顺序补齐，但非原子完成标志不证明并发一次性。完整builder还显示category抽取/CDATA处理及brand_account、emoticon分流先于类型1，不能仅填message_type=1就承诺任意正文保持。3个unwind完整LLVM范围含旧invoke缺失尾段，加10份Ghidra共3654指令/142检查/35分支/6来源/6槽及字符串、Ruff通过，见research/newsendmsg-text-job-input-result.md。全部gate语义、最终保持与真实线程仍缺；下一步优先回55状态0取消最终释放。A7、11/18/20～24/55/67未关闭，无微信操作、产品接线或部署。

68. [x] 将已核验的实际执行器TLS getter合同落实到研究请求组件：ExecutorResearchOperation在正文/factory前及每次cancel/expire入口核对当前指针，同时保留创建线程生命周期令牌；不设TLS、不隐式调度/取消。4份完整导出85指令、29位置/4分支、TLV节与bootstrap/pthread导入绑定独立核验通过。9个新增场景及15个依赖场景、100竞态、64/69次异线程拒绝、严格host ARM64编译与Ruff通过；见research/newsendmsg-executor-context-result.md、合同及executor-context-20261018/verification.json。只补55/22必要约束，入口指针检查不证明原生组排序、对象活性、状态0最终清理或完整排空；55及A7/11/18/20～24/67仍开放。无微信操作、产品接线、真实发送或部署，账号停止约束保持。

69. [x] 有界补证组切换/服务关闭的实际直接调用者及隐藏x8 ABI：0x2fec684→0x46735dc→0x4551eac→空名组切换；_WeChatMain四字节跳板→0x2c976c→0x4671338→服务关闭。9导出4343指令/26位置/12分支核验，独立unwind+LLVM补齐关闭大函数1982指令，去重4563位置；初次连续性失败源保留，明确Ghidra漏brk及尾段220位置。三个新脚本Ruff通过，见research/newsendmsg-executor-context-result.md后续节及shutdown-callers-20261018-verification.json。未证明大函数所有前驱、执行器身份及首次恢复/取消全序，不以组等待或尾段存在推断最终清理，55及A7/11/18/20～24/67仍未完成；账号停止约束保持，无微信操作或部署。

70. [x] 补齐完成通知快照和信号析构的正常路径语义，并纠正旧报告/合同将+0x90误称派发计数的问题：实际值为pthread_self身份，用于递归派发防重入；+0x98延迟回收的是信号状态，不是协程参数。快照与排队闭包独立保留接收方，原登记断开不撤销已复制调用，job仍为raw参数。15完整导出1472指令、75位置/19独立分支/3导入/3虚槽核验及新脚本Ruff通过；见research/newsendmsg-core-teardown-result.md新增纠正节和signal-dispatch-20261018-v2-verification.json。历史初版源码/结果及旧错误标签保留并标明取代关系。只关闭该信号字段/同步释放边界疑点，具体作业全部监听者、状态0参数最终清理、启动/关闭全序、完整映射/适配及真发送/独立回执/部署仍缺；55/22/A7不勾，无微信操作。

71. [x] 核验所选文本提交的返回句柄、空最终function及可选正文前包装：builder立即释放返回shared句柄，释放函数不显式cancel/join；正常launch路线明确传空最终function。包装先经当前core执行器虚槽+0x18及既有等待入口再调用原body，不能证明未进入body的状态0参数清理。19导出1684条、完整builder2219条、8个独立unwind/LLVM范围677条（补103位置），共4006位置、100检查/19分支/6槽及Ruff通过；见research/newsendmsg-text-job-launch-result.md与text-job-launch-20261018/verification.json。Ghidra内部遗漏和异常尾段保留说明，不扩大为全路径语义或实际可达性证明。55/22/A7及11/18/20～24/67仍未完成，无微信操作、产品接线、真实发送或部署。

72. [x] 核验两层调度的准入容量与排队取消边界：core+0x270对象提供scheduler上限，与core+0x268执行器分开；null-key默认对象明确返回UINT64_MAX，不能据通用容量门误报所选发送实际限流。pending选中及模式1闭包invoke均会跳过状态3；正常参数清理先于准入树退队，退队只触发一次选取，容器析构仅释放pending pair和raw树节点。14导出1061条、9个unwind/LLVM范围716条、去重1149位置/108检查/26分支/5槽及Ruff通过；见research/newsendmsg-scheduler-admission-result.md和scheduler-admission-20261018-v2/verification.json。初版过宽通用函数unwind范围及源码保留，不计新增语义成果。下一步先证所选group/config实际key来源，再判容量分支相关性及启动/取消顺序；55/22/A7及11/18/20～24/67仍开放，无微信操作、真实发送、产品接线或部署。

73. [x] 补齐所选文本launch的config+0x20从零值/所选group+0x128，经Job+0x100传到core+0x270的配置链；默认组与活动组构造均清零该字，parent setter不复制配置。在配置未另改且默认provider走已证首次构造的条件下，上限为UINT64_MAX，不将有限容量作为当前故障前提。22导出3971条及9个unwind/LLVM范围2743条，去重4273位置、82检查/20分支/1槽和173源哈希及Ruff通过；见research/newsendmsg-scheduler-config-result.md及scheduler-config-20261018/verification.json。两条Ghidra内部遗漏由LLVM补齐，首次失败及源码保留。下一步回到实际启动/组切换/关闭协调与状态0最终释放；55/22/A7及11/18/20～24/67仍开放，无微信操作、发送或部署。

74. [x] 核验登记锁先于启动释放、Job启动位早于core发布/首次恢复提交、已启动取消分支向同一执行器提交的局部顺序；相对偏移以配置组+8子对象G为基准。126种自有偏序合并中65种满足选定分支，存在取消先入队与恢复先入队两类；即使假设延后消费的理想串行FIFO，也不能凭锁/原子位推定恢复必先行。该模型显式假设外部取消可重叠，不证明当前原生调用允许、实际时序或泄漏。9导出1215指令/59检查/16独立分支/3槽、62源哈希及Ruff通过，见research/newsendmsg-launch-cancel-order-result.md和launch-cancel-order-20261018/verification.json。仍需实际外部生命周期协议或完整最终释放；55/22/A7及11/18/20～24/67保持开放，无微信操作、发送或部署。

75. [x] 补证具体组切换生产者0x2fc5d68通过全局接口默认组提交正文0x2fec684，正文经0x46735dc→0x4551eac→空名组切换取消/等待。配置执行器槽为零并继承默认组；与所选发送共用执行器的结论以服务/接口实例及配置未变为条件，仍不证明提交跨度不可yield/重入、完整关闭或最终释放。10导出3194指令、两份独立unwind/LLVM范围、去重3325位置/63检查及配置依赖173源哈希、Ruff通过；见research/newsendmsg-group-switch-caller-result.md和group-switch-caller-20261018/verification.json。旧错误等待地址的源码/诊断保留；55/22/A7及11/18/20～24/67保持开放，无微信操作、发送或部署。

76. [x] 补证builder收件人查找0x2ab6388的ABI、企业/app后缀及缓存/缺失路线，重建filehelper/qqmail/wa_app_kefu_message等7个精确字面量；filehelper已存对象经复制、+0x54/+0xa8显式变更及shared包装。缓存缺失在0x2b4b260/0x2ab66a4进入原生等待，不能仅核对执行器TLS就从普通函数栈调用；类型1仍以parsed chat_id赋input+0x90。19导出2283条加完整builder2219条，3个unwind/LLVM范围补186位置、合并4688位置/77检查/35独立BL/91源哈希，另9位置及RTTI字面量补核、新脚本Ruff通过；见research/newsendmsg-recipient-lookup-result.md、合同及recipient-lookup-20261018/。可变比较值不在文件映射区，未猜或读取运行值；所有间接变更、最终网络方向/正文保持、原生协程和取消最终清理、完整适配/发送/独立回执/部署仍缺。55/67/22/A7及11/18/20～24保持开放，无微信操作。

77. [x] 实现无加载器的原生文本输入研究组件：工厂返回立即持有、校验虚表/初值，精确复制chat_id/正文后写低类型1。Apple ARM64严格构建及UBSan各21场景通过；1998导出指令、30位置、7独立BL、精确string assignment导入和33源哈希核验，新脚本Ruff通过。ASan组件15秒和独立最小程序5秒均无输出超时，子进程已终止并保留失败源码/诊断，不声称ASan或leak检查通过。见research/newsendmsg-text-input-owner-result.md、合同及text-input-owner-qualified-20261018-v2/verification.json。仅关闭该组件；完整映射、协程/取消最终释放、完整适配/真发送/独立回执/部署仍缺，22/A7及其余9项保持开放，账号停止约束保持。

78. [x] 补齐所选服务48字节非平凡返回ABI：两状态字、+8字符串、+0x20 shared pair；0x3189980等待后经typed getter复制，caller正常析构再次印证布局。新增ABI声明和自有ARM64汇编/C++夹具，严格/UBSan各7场景通过；7导出1629指令、58位置、10独立BL、精确RTTI字面量、43源哈希及77依赖33哈希复验、Ruff通过。见research/newsendmsg-text-service-abi-result.md、合同和text-service-abi-20261018/verification.json。服务本身会进入协程等待，不能凭TLS或跳过前置查找从普通栈调用；shared payload保持opaque，零状态/本地对象不当独立回执。仅该ABI组件完成，其余9项/A7仍开放，无微信操作或部署。

79. [x] 定点核验启动跨度：core构造在Job发布core之前派发0xa517a48创建通知；0x667a760可直接调用无执行器监听器，非空执行器监听器经虚槽+0x10提交。0xa517ac0经guard_acquire/release证明为初始化guard，不是通知关闭开关。0x668e56c为TLS string清理及首次构造，名称getter仅3指令；日志链/实际监听集合仍有未证明边界。19导出1883不同指令位置、72检查/33独立分支/5导入及96源哈希、Ruff通过，见research/newsendmsg-launch-span-result.md和launch-span-20261018/verification.json；两处Ghidra内部缺口明确保留。仅关闭此有界调查，不能凭同执行器推定整个启动不可重入；状态0最终清理及55/20/22/A7、其余9项仍开放，无微信操作、真实发送或部署。
80. [x] 补齐普通文本aux来源及局部保持合同：record构造清零+0x220 pair，低类型setter主动prepare，类型1正常返回两类aux；安装helper转入pair，非空prepare直接保留，record copy/move保持身份，高类型setter不执行类型49专属写入，两类+0x10目标均为ret。新增pass427安装helper；25份导出3286位置/101检查/27独立控制转移/2独立槽/108源哈希及Ruff通过，见research/newsendmsg-text-auxiliary-result.md与text-auxiliary-20261018-v2/verification.json。初次合同摘要键错误保留诊断及源码；只证明没有未证中间替换时的局部合同，不证明完整factory/metadata副作用或最终字段保持。A7及11/18/20～24/55/67仍开放，无微信操作、真实发送、产品接线或部署。
81. [x] 核验文本准备局部正常返回CFG：第二次text cast成功后，正文赋值支配typed DB调用和正常返回；仅首个validator成功不足，保留13节点回退结构witness而不声称实机可达。metadata赋值先于正文；固定两者来源/目标及record+0x258清零。659指令/29位置/101独立控制转移、48调用边和9源哈希核验，Ruff通过；见research/newsendmsg-text-prepare-order-result.md及text-prepare-order-20261018/verification.json。外部callee、异常、并发和整链最终字段仍未证明，原9项/A7保持开放，无微信操作、发送或部署。
82. [x] 穷举数据库父流程全部本地正常返回：三处直接复制发布及一处插入作业提交覆盖全部返回；四个复制点的x20均来自入口record，插入capture复制支配提交，invoke先移动再经0x326a144修改、之后发布。6既有导出1944位置/45检查/311独立控制转移/31源哈希及Ruff通过；见research/newsendmsg-database-record-outlets-result.md及database-record-outlets-20261018/verification.json。只关闭本地返回记录来源疑点，不把同源推为字段保持、作业执行或回执；原9项/A7及整体目标仍开放，无微信操作、产品接线或部署。
83. [x] 核验插入更新所选直接写域和metadata缓存副作用；补出vector扩容、比较thunk目标及metadata构造，区分字符串/vector独立存储、metadata新建合并和三个共享pair。12导出2110位置/56检查/424独立分支/27独立store/11嵌套顶层分配分支/91源哈希及Ruff通过，见research/newsendmsg-insertion-mutations-result.md及insertion-mutations-20261018-v2/verification.json。pass428参数错误和v1源码/结果保留，最终以v2为准。未证明所有callee/别名/并发或整链字段保持；下一步定点核验0x3296b1c/0x3263cd4对共享对象影响。原9项/A7保持开放，无微信操作、真实发送、产品接线或部署。
84. [x] 有界核验两个vector消费者的参数暴露：机器码推导后处理只接受3/43/10000；入口低类型仍为1时跳过aux/摘要，全类型1vector不调用摘要处理。其他接受类型只显式传40字节摘要；插入mode2仍把完整record传给字段访问器+0x18/+0x30共8个虚调用，不据此推定只读。复核既有共享ID写入和hidden x8构造，冻结字节补明导出遗漏BRK #1。13导出2039位置/81检查/364独立控制转移/60源哈希、Ruff通过；见research/newsendmsg-vector-consumers-result.md及vector-consumers-20261018/verification.json。下一离线动作是具体插入字段访问器副作用；整链字段保持、协程/取消最终清理、完整适配/真发送/独立回执/部署及原9项/A7未完成，账号停止约束保持。
85. [x] 核验record注册表15对/五类访问器：15个精确dyld槽及标量完整读取指令，field+0xf0入口和operation空初始化。字符串/vector通过包装返回借用data/length，不复制payload或retain原存储；包装移动不能当载荷深复制。字符串/buffer绑定仍委托backend+0x48/+0x58，具体消费与实际字段列表来源未证。30连续导出1022位置/59检查/190独立控制转移/15槽/15注册pair/99源哈希及Ruff通过；见research/newsendmsg-registered-accessors-result.md及registered-accessors-20261018/verification.json。仅有限合同关闭；全链字段保持、协程/取消最终释放、完整适配/真发送/独立回执/部署及原9项/A7保持开放，账号停止约束不变。
86. [x] 连接所选插入字段列表默认来源：caller extra-list计数清零，operation空列表正常路线经record注册表默认填充；field+0xf0=node+0x100的访问器指针在复用/追加及旧列表复制中显式保持。查询可写getter存在COW/共享释放，非只读；准备包装仍经两层+0x10虚槽，句柄可复用+a0缓存或从0x563f1a8重新取得，具体backend未证。22导出2163位置/74检查/390独立控制转移/4独立指针复制对/88源哈希及85依赖99哈希复验、Ruff通过；见research/newsendmsg-insertion-field-list-result.md与insertion-field-list-20261018/verification.json。只在正常构造复制且无外部/并发列表改写条件下连接来源，不证明完整字段保持；backend消费、协程/取消最终释放、完整适配/真发送/独立回执/部署及原9项/A7仍开放，账号停止约束保持。
87. [x] 核验连接取得hidden x8/kind0/owner+0x48两分支；区分连接与实际statement：包装虚槽+0x10读取连接+0x260，新建kind0构造经factory得到0x9f1cbc0语句。5槽独立解码准备/字符串/buffer入口；直接分支显式传-1，真实_memcpy复制到内部存储，本地CFG证明复制支配成功选择点。源须保持到完整绑定返回，不能用构造初值证明运行中没有拦截。44连续导出2521位置/116检查/505独立控制转移/5槽/6load/174源哈希及86依赖88、85依赖99哈希复验、Ruff通过；见research/newsendmsg-statement-binding-result.md和statement-binding-20261018/verification.json。仅条件合同关闭，旧缓存/池身份、拦截callback、其他callee/并发及完整字段/协程/最终清理/原生适配/真发送/独立回执/部署和原9项/A7保持开放，账号停止约束不变。
88. [x] 核验具体连接配置0x5640094对statement+0x198及+0x188 callback的建立路线，确认字符串+0xf8/buffer+0x138拦截分支的实际捕获、委托与保留边界；仅在有证据时连接缓存/池对象身份，不以初值/相同槽偏移放行。目标仍为完整字段保持及最终可发送适配，原9项/A7和账号停止约束保持，无活体操作。仅关闭有效对象/所选新建配置、正常返回/成功分配、无并发销毁和同TLS/key重入替换条件下的静态边界核验，实际运行中如何保证这些条件仍归20/55/22。

实施88早期进展（当时未勾选）：74导出6412位置/120检查/1285独立控制转移/12槽/4导入/258源哈希及87依赖174哈希复验、Ruff通过；两类callback捕获与保存下层委托、字符串缓存移动owner/条件分配复制、buffer共享包装与最后持有者free已形成条件合同。buffer分配失败结果未检查，不能无条件认定已拥有数据。见research/newsendmsg-interception-result.md和interception-20261018/verification.json。下一步收窄到基础/保存后function身份、raw processor capture完整寿命及转换helper返回存储的寿命，再回到55/67和完整适配；无微信操作、发送或部署，原9项/A7保持开放。

实施88静态收口：112导出7559位置/191检查/1507独立控制转移及另1原始B/32槽/5导入/2TLV绑定/六组清理形状/371源哈希及前次258哈希复验、Ruff通过。基础function连接已证复制入口；树shared pair拥有processor，先树后bundle析构，所选raw function清理不解引用processor；转换结果借用按线程/key保存且可被后续分配替换的工作区，不能异步持有或手工free。见research/newsendmsg-interception-lifetime-result.md及interception-lifetime-20261018/verification.json。下一步回到55/67的实际准入、串行/重入和取消最终释放；原9项/A7及完整目标未完成，无微信操作、发送或部署。

实施55/67服务取得进展（仍未勾）：补明0x268f370通过精确描述器键_3d834e75取得拥有的service pair；pending/fallback两条路线均可能等待，并无条件建立当前core guard。独立LSDA及遗漏尾段证明所选wait/getter/fallback异常先释放guard，再释放optional future并继续展开；guard构造失败只清future。builder保留service pair后移入body+0x60，与input/chat_id/call_id分开。12导出+完整builder及9个unwind/LLVM区间共3662位置、106检查/705独立控制转移/4槽/4导入/4个LSDA调用位置/78源哈希、Ruff通过，见research/newsendmsg-service-acquisition-result.md与service-acquisition-20261018-v2/verification.json。初次内部缺口失败源码保留；仅局部持有及清理证明，不是服务关闭租约、新Job启动/取消协调或排空屏障。下一步聚焦原生外部取消与状态0最终释放；原9项/A7、完整映射/适配/真发送/独立回执/部署仍开放，账号停止约束保持。

实施55发布边界进展（仍未勾）：job+0x140先置位，job+0xa8/+0xb0随后才发布；已启动取消handler经两指令wrapper及三指令getter直接读取core，无空值回落。1325冻结位置/40检查/180独立控制转移/4个load解码/3槽/88源哈希及前次62哈希复验、Ruff通过，见research/newsendmsg-core-publication-result.md和core-publication-20261018/verification.json。210种有界抽象合并区分两个门槛：同工作线程且无重入的消费可排除发布前读取，但不能排除外部取消先提交、首次恢复后提交。未观察原生崩溃或竞态，未证明实际调用者允许重叠；须证明真实生产者协调或最终释放，不能以本模型或BodyStartGate放行。原9项/A7及完整映射/适配/真发送/独立回执/部署仍开放，账号停止约束保持。

2026-10-18跨会话接续：核对ZCode两条原会话及媒体真图承接资料，修正媒体旧看板的过时未供钥状态，保留历史证据/未重验边界。发现五份shell闸之外，truepath八份LLDB命令可直接source后附加；逐份添加首条quit78并完整保存原文，实际无目标LLDB八份全部拒绝、旧shell五份仍拒绝、15项产品被动回归与Ruff通过。额外CLI命令仍可执行的限制已用独立夹具实证记录，不称全局隔离。见research/cross-session-reconciliation-20261018.md与legacy-command-guard-20261018/verification.json。仅安全入口修复；原9项/A7/L3及完整直发仍未完成，账号停止约束保持，无微信活体操作。

实施55关闭尾部补查（仍未勾）：pass497展开0x453e904末端四个callee，确认getter返回固定全局槽0xa518cb0、容器shared释放与元素虚调用的具体顺序；间接对象身份/效果仍未穷尽，未建立指定core参数最终释放关系，不作排空屏障。266连续位置字节核验与Ruff通过，见research/newsendmsg-shutdown-tail-result.md。该旁路到此为止，不沿日志扩散；实际启动/关闭协调或状态0释放、完整业务映射/适配/真发送/独立回执/部署及原9项/A7均未完成，账号停止约束保持。

2026-10-18产品回执修复：修正直发正文对账删除全部空白的假阳性；CLI明确选择exact_text=True，UI默认保持旧规则。14项新合成用例先13失败/1通过，修复后相关91通过/1跳过；微信桥全套856通过/14跳过（9.45s），修改Python文件Ruff通过。见research/direct-receipt-exact-text-20261018.md。仅正文比较修复，不证明新消息唯一性、出站或服务端送达；未启用驱动、未部署，A7/原9项/L3仍开放，账号停止约束保持，无微信活体操作。

2026-10-18回执证据续修：修正全未知轮询被当作明确未见、展示名改写正文参与对账、同文入站/未知方向消息假绿三处问题，并区分未知错误说明。新增29项合成测试，桥全套885通过/14跳过（9.86s），8个修改Python文件Ruff通过；合成集成确认未验证回执保留pending且同请求不重复调用假发送器。见research/direct-receipt-evidence-20261018.md及receipt-evidence-final-regression-20261018.log。4.1.15自身份、新消息唯一性/服务端送达、原生调度取消最终释放及完整适配仍缺，不勾A7/原9项/L3，不装机或启用，无微信活体操作，账号停止约束保持。
