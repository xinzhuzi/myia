# design:SendMsgFtouser 直调通道(逆向交接态,2026-10-14 晚)

## 架构定论(实证,不再翻案)

UI 回车 → 逻辑层(未定位)→ 自研协程任务系统(task_service.cc)→ mars::stn 传输(0x490fb20=通用任务投递器,仅作函数指针传入协程,**零 BL 调用者**)→ 网络。0x31ab38c 链=NewSync 收信侧误标(断点 x0 含 NewSync;且 newsendmsg 与 newsync 同在 functionlist XML 相邻条目——误标成因现已完全可解释)。

## 本轮新增(2026-10-14 晚,会话:REA 装机线)

### 已证死路(勿重试)

| 路 | 结论 | 证据 |
|---|---|---|
| ObjC selector 路 | 无 send 族 selector | objc-dump.txt(otool 全量)+ 复扫 |
| BL 直调投递器 | 零调用点(纯函数指针) | /tmp/blscan.py 41M 指令扫描 |
| newsendmsg 字符串 xref | **判据作废**:该串属 mars functionlist XML 传输配置(0x986e82e 可读原文),引用点 10 处全是 mars 配置层非消息组装 | refscan3 + 字符串读取 |
| thunk 区函数起点启发式 | 失败(生成式 accessor 汤,PACIBSP/序言扫描得空函数) | DecompileTargets4 44 字节空壳 |
| 全量自动分析 | 混淆段病理卡死(Decompiler Switch Analyzer);关三分析器后 2h+ 未出仍弃 | headless4.log |
| 0x46391ac 回调静态定位 | ADRP 页级扫描零命中(页 0x4639000 无引用);**注意:该 VA 本身未二次验证(前序会话 slide 推导,或存 slide 误差),零命中≠必死,勿据此地址做任何依赖** | refscan3 |

### 可复用工具链(全在 ~/Downloads/微信反编译/sendmsg-勘察-1014/ 与 ~/Downloads/rea-wechat-decompile/)

1. **noanalysis 定向反编译**(2 分钟级):`analyzeHeadless wxrea2 -process wechat_arm64_thin.dylib -noanalysis -postScript <脚本>`,工程 wxrea2 基址 0 与旧 VA 互通;脚本模板 DecompileTargets*.java
2. **BL 扫描器** /tmp/blscan.py:全 __TEXT 41M 指令解码直调(已证 0x5e1d050 有 27743 调用点=通用 helper,勿当发送专属)
3. **页级 ADRP 扫描** /tmp/refscan3.py:ADRP(+ADD/LDR)取址定位(精确匹配会被寄存器折叠骗,必须页级)
4. cap.py LLDB 断点捕获枪(并行会话遗产,命中即写寄存器+内存+BT 自禁用自继续)
5. Ghidra 12.1.4:@~/ghidra_12.1.4_PUBLIC(arm64 反编译器已按 REA 配方自炼;官方 zip 不含 mac 件)

### 现有产物

- decomp/ 7 个点位部分反编译(含 0x5a2beb0 3.3KB mars 配置层可读 C、0x490fb20 投递器 134 行)
- ~/Downloads/rea-wechat-decompile/ghidra_out/ 五函数(误标线全指纹+投递器)
- blscan.json / refscan3.json 机器可读结果

## 正确路线:运行时明文猎捕协议(执行级,下一步唯一首选)

> 原理:明文 (目标, 内容) 在进入 protobuf 序列化**之前**必然以字节形态存在于堆与寄存器链上;断点钉在传输边界(RPC 家族入口),触发一次受控发送,回扫堆内明文,再从「谁在写这块缓冲」向上归因。静态攀爬已被五条死路封死(见错题集),运行时是唯一未走的正门。

### 前置(每轮必做)

1. 微信在跑:`pgrep -x WeChat`(记录 PID);**并行会话在 attach 则排队等其收工**(`ps aux | rg lldb` 空才动手——双调试器撞 attach 在案)。
2. 取 slide 并**字节级校验**(防 slide 漂移/版本换包,错题集 S6 cousin):
   ```
   lldb -p <PID> -b -o 'image list -o -f' -o 'detach' 2>/dev/null | rg wechat.dylib   # → slide=S
   lldb -p <PID> -b -o "x/16bx S+0x490fb20" -o 'detach'                                # 与薄片文件偏移 0x490fb20 起 16 字节比对
   python3 -c "print(open('/Users/zhengbingjin/Downloads/rea-wechat-decompile/wechat_arm64_thin.dylib','rb').read()[0x490fb20:0x490fb30].hex(' '))"
   ```
   不一致=微信已换包,全线地址作废重锚(重跑 lipo+锚点函数指纹)。
3. 断点枪:cap.py(~/Downloads/微信反编译/sendmsg-勘察-1014/tools/,v2.1)现有能力=寄存器/内存 160B/BT/自禁用/自继续(`return False`)+堆扫。**2026-10-14 晚勘误(grill R2)**:前题「本机 lldb-1703 的 SBProcess 无区域枚举」系 S10 转述失真——该构建实有**零参** `GetMemoryRegions()` 且 attach 态活体可用(亲证 39/60 可读数据区;launch 停 main 态返回空=按不可用回退);堆扫区间源改为**活体枚举优先、vmmap 快照文本回退**(`vmmap <PID> | rg 'MALLOC'` 仍为回退配方,快照滞后=hit 时新增堆区漏扫)。扫明文=回调内 `proc.ReadMemory` 分块(每块 4MB,块尾探针级重叠防跨块漏检)+`bytes.find`,命中地址与前后 128B 上下文写 hit 文件。禁用 lldb `memory find` 命令形态(逐次 HandleCommand 不可靠且慢)。**判据分级(grill R2)**:内容探「嘻嘻」=唯一烧窗判据;目标探「filehelper」(常驻联系人,堆内可有陈旧串)仅记 weak 取证件不烧窗;窗口 TTL 30s(过期自关窗自禁断点)。

### Step 1 触发(零预算方案优先)+ run-sheet

- **首选(主人 10-14 晚已批为标准触发)**:主人手发一条「嘻嘻」到文件传输助手(零自动发送预算消耗,断点只读捕获);配合流程=主人说「发」→ 执行侧 3s 内完成窗口使能 → 主人发送 → 命中后即禁断点;
- 备选:桥真发 1 条:`printf '嘻嘻' | ~/.myia/plugins/wechat-bridge/bin/wechat-bridge send_text <id> --file -`(id 经桥 DB resolve,以桥 doctor 实测为准;正文恒走 stdin,argv 零明文=桥红线)。

**Run-sheet(执行序列,单轮)**:①空 lldb 检查→②取 slide+字节校验→③vmmap 快照→④布断点(见 Step 2)→⑤触发(手发或桥发)→⑥等 hit 文件落盘(≤30s)→⑦`bp SetEnabled(False)`+`detach`(微信零伤在案纪律)→⑧离线归因。**失败恢复**:任何异常=先禁用断点再 detach;微信若崩(未预期)=重启后 slide 重取重锚,绝不带断点重试(错题集 D2)。

**预算账(主人 10-14 晚已裁:总帽 10 条,每条先报后发)**:勘察已用 6+1;余 3=Phase 2 直调验证 1(filehelper)+Phase 3 终验双发 2;猎捕触发=主人手发(0 消耗,标准形态),桥自动触发仅为手发不可行时的备选(占用余量并先报)。

### Step 2 捕获与归因

1. **断点选址与降噪**(0x5e1d050 有 27743 个调用点=通用 helper,裸断必淹)。grill 复裁:~~常量 0x154 过滤~~**降级为弱先验**——该常量恰出自已判「判据作废」的配置层反编译(S4 同源),不得作为过滤依据。改用两层正 filt:
   - **窗口布防(主)**:断点默认禁用;主人/桥发起点前 3s 使能,首个通过堆扫的命中后即再禁用——30s 窗内网络任务个位数,噪声天然受控;
   - **线程名过滤(辅)**:回调首查 `thread.GetName()`,仅 `coroutine *`/`mars::stn` 前缀线程做堆扫(hit3 实证发送任务跑协程线程),其余直接 return False;
   - 布点:bp1=S+0x5e1d050;bp2=S+0x5e1d680(组装入参形态更特异,若噪声低可独用)。
2. 命中后:x0-x7 全录+每寄存器指向内存 160B(cap.py 现成)+堆内明文扫描(探针=目标串「filehelper」+内容「嘻嘻」双探;protobuf string 字段此层未加密(mmtls 在 CGI 之后),序列化缓冲内当有明文;双探皆无=窗口错失或过滤过狠,重开窗口再来,勿换弱先验常量)。
3. 明文缓冲地址 A_content/A_target → 看哪个寄存器/栈槽离它最近(发送对象与内容通常同帧相邻构造);**注意 A 的写入者可能是序列化器而非明文 API**——从序列化器上爬同样到 API,只是层数多一层,不推翻路线。
4. **从命中地址取真起点**(错题集 S5 的正解):断点布在函数入口(`breakpoint set -a`)时命中地址=入口;若只能布中段,**lr=最近一次 call 的返回地址**,其所属调用者=目标函数的直接上游(`image lookup -a S+lr` 定位 + 薄片反查);对调用者跑 blscan.py 上游扫,逐层上爬到 (用户,内容) 形参函数。

### Step 3 签名推导与直调安全协议

1. 目标函数全函数反编译(DecompileTargets 模板,wxrea2 工程;起点取自 Step 2.4 的运行时真值)。
2. **先只读验证 LLDB expr 机制**:挑同类一个 getter 型函数直调一次,回读返回值(不产生任何副作用)。
3. **`this` 与字符串实参一律复用活对象,不新造**:成员函数直调需活 this——从 API 断点命中的 **x0 取服务对象指针**(长寿命单例),直调前再验活性(读其 vptr 与首次命中时一致,错则重取);std::string 实参同理复用命中帧里的活 string 指针,不在 lldb 里构造 libc++ 临时对象(构造形态跨版本不稳,新造=白担崩溃风险)。
4. 直调发送:filehelper 先行;**回执双通道**(filehelper 的桥 `localdb query` 有已知表名映射缺陷,md5('filehelper')≠实际表名 Msg_0e1945d6…):
   - filehelper → **sqlite 直查** `decrypted/message_0.db`(r3 实证形态:evidence.md #4,按时间窗+内容「嘻嘻」+local_type=1);
   - jiangliushi666 → 桥 `localdb query wxid_... --since 1d`(wxid 路径正常)。
5. 白名单双发终验:filehelper+jiangliushi666/嘻嘻/≤2 条/≥10s 间隔/uncertain-never-retry;
6. 失败即停:任何崩溃/不确定态→禁用断点→detach→如实报告,绝不重试第 4 次(错题集 D2)。

### Step 4 落桥(与 OCR 链分级)

- 通道形态:lldb 批式脚本(桥内 python 子进程驱动,按需 spawn 不常驻——常驻调试器=进程面与崩溃半径扩大)+ 与 OCR 链分级调度(直调=保证级首选,OCR=版本漂移兜底);
- **频控:直调通道同过 send_state G6 flock**(单条、≥10s 硬间隔——桥既定纪律,通道不分级豁免);
- 单测:打字/发送路径强制打桩判例(全仓既定);版本锚定:对位表参照 WeChatTweak「build→地址」格式思想(AGPL 只看不抄);
- doctor 探针三件:slide 字节校验(前置 2 命令)、断点预热(hit 一次即禁用,验证 attach 链路通)、对象指针活性(vptr 比对);探针失败→自动降级 OCR 链并发警示。

### 时间预估与回退

- Step1-2(猎捕+归因):1-2h;Step3(签名+直调):1-2h;Step4(落桥+测试):2-3h。
- 回退:直调线任何环节死→OCR 链(0.8.4,已三连绿)仍是发送主力,直调只是保证级补充,**不阻塞任何其他线**。

