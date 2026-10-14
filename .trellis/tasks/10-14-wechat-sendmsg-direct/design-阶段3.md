# design-阶段3:直发通道实施蓝图(双路探索合流,2026-10-14 深夜;grill r1 修订 2026-10-15;r2 修订同日)

> 输入=本轮静态轮(C1-C6,产物 `~/Downloads/微信反编译/sendmsg-hunt/`)+ 动态轮
> r1-r3(产物 `research/hunt-r3-dynargs/`、`/tmp/wxsend3/`)。本文=Phase 2/3
> (implement.md)的执行级设计:**调用配方 / 桥落地面 / 白名单验证 / 风险红线**
> 四问全答,执行者零歧义。可翻案点集中列 §7。
>
> **修订记录 r1**(2026-10-15)八项质询全采纳——硬伤1 svc 指纹改 slide
> 相对量(§2.5/§2.6);硬伤2 补 peer 长度门 `send_direct_target_too_long`(§3.1/
> §3.3/§6);硬伤3 降级矩阵补全三码+单批管线序写死+24 享 rollback+push 侧码表与
> 重试账本 never-retry 谓词(§3.3,上游重试链已亲验实证);硬伤4 测试计划补
> cmd golden/跨通道互锁/UTF-8 字节门(§6);中危5 expr 停态死锁与冻结恢复预案
> (§5)+r4 同步返回实测(§2.4);中危6 双路报告落档+0x1c0 形验证准入门(§0/§2.4);
> 中危7 版本主门升级+模块锁定规则(§2.6);中危8 串构造判例翻案升
> P-0 主人裁决(§4)。
>
> **修订记录 r2**(2026-10-15)五项:[硬伤1]采纳——磁盘 wechat.dylib 是 FAT
> 双切片(x86_64+arm64),整文件哈希≠thin 切片哈希,主门改**切片哈希**并已端到端
> 亲验(FAT 解析+arm64 切片 sha256==thin sha256,§0-F10/§2.6);[硬伤2]采纳——
> r1 修法不闭环:push_local._raise_for_result 对 17/24/自定义码**无分支**,码名只
> 进 message 不进 PushSendError.code,never-retry 谓词永失明;修法写死=直发分支
> 以桥码名**原样**作 code 抛出+全链测试(§3.3/§6-9);[中危3]**驳回**(复核亲跑:
> stat 与 python 双证 thin=173,148,768B=0xa520a60;r2 质询自给十进制与我一致而
> 其十六进制 0xa5340e0 换算有误——0xa5340e0=173,228,256≠173,148,768;原数保留,
> F7 补双重复核证据);[中危4]采纳——磁盘双 wechat.dylib(Resources 357MB FAT
> 主体+Frameworks 84,544B 桩)basename 歧义真实,模块锁定加尺寸门槛+区间断言
> (§2.6);[轻微5]采纳——§6-6 间隔门夹具钉「异指纹」(同指纹先撞指纹门得 dedup
> 非 14,与相邻断言互斥)。

## §0 事实基线(分「亲验」与「引自」,含 grill r1 复核)

**亲验(本蓝图会话内直接读文件/跑命令核对)**:

- F1 入队 API 签名:`FUN_000a6060(q, name, cmdid, task)`——`FUN_00033c7c(q+0x68,task)`
  入队、`FUN_0003b5c4(q+0x10,name)`、`q+0x48=cmdid`、尾虚调 `(*(*q+0x28))(q)` 唤醒泵;
  `FUN_000a5ed0` 同构同参(仅地址不同)。亲读 coro_spawn_hunt5.c:6380-6394、
  coro_spawn_hunt3.c:3868-3880。
- F2 协程帧初始化:`FUN_00033c40(frame,resume,destroy)` 写 `{+0x0=1, +0x8=resume,
  +0x10=destroy, +0x18=FUN_00033c5c}`。亲读 coro_spawn_hunt3.c:3846-3857。
- F3 msgctx 明文块布局(逐字节核 msgctx_r1_ptr02e0.bin / msgctx_r3_ptr03a0.bin):
  `+0x130/+0x148/+0x160/+0x178` 四条 24B 定长记录 `{char value[23]; u8 raw_len}`
  (r1/r3 两轮逐字节同构:`wxid_oc2yhey1xkpw22`+len 0x13、`filehelper`+len 0x0a,成对
  重复);`+0x1c0`={堆指针, 0x26acf 序号, 0};`+0x1d8`=正文 UTF-8 明文内联(r1
  `e5 98 bb×2`、r3 `e5 98 bb×4`)。**串形态=23 容量+末字节裸长度(字节数)**,
  非标准 libc++ SSO。
- F4 泵入口命中形态:pc=slide+0x43f88e4、x1=0x186a0、x0+0x8/+0x10/+0x18=
  {0x43f88e4, 0x43fb37c, 0x33c5c}(与 F2 帧三元组吻合);**回溯帧全是泵机械+CFRunLoop,
  无发送发起者**(异步投递,发起栈在泵恢复时已消亡)。亲读 hit_send7_r1.txt 全帧表。
- F5 **预算实锤**:动态轮 r1/r2/r3 三发全部经桥自动发送触发(round.sh:46-48
  `./bin/wechat-bridge send_text filehelper --file -`),非主人手发零耗形态。
- F6 桥现状:send_text 管线=目标解析→G6/防重→ax.send_text(on_armed/on_receipt_green/
  receipt_query 回调三件)(cli.py:641-770);codes.py 封闭表(新族须先改设计档);
  config.py 封闭键+未知键 fail-fast;push 层 src/myssia/wechat/push_local.py 以
  60s 超时 spawn 桥、exit 码映射瞬态族。
- F7(grill r1 新增亲验;r2 复核加固)锚点源字节与 thin 基准:thin dylib
  `~/Downloads/rea-wechat-decompile/wechat_arm64_thin.dylib`=**173,148,768 字节
  =0xa520a60**(r2 复核:stat 与 python open('rb').read() 双路径同值;0xa520a60
  展开即 173,148,768——r2 质询所给 0xa5340e0 为换算误差,0xa5340e0=173,228,256),
  sha256=`6a5bd0cbb39ad3092c15e9debda2db4969eedf1b58caad244d88033a996833a7`;
  偏移 0x490fb20 起 16B=`ff c3 05 d1 fc 6f 14 a9 f4 4f 15 a9 fd 7b 16 a9`
  (arm64 序言,指令字节与 slide 无关;亲跑 python 直读)。
- F8(grill r1 新增亲验)**上游自动重试实证**:MYIA 投递层对 immediate 发送失败会
  留账自动重投——src/myssia/push/delivery.py:458-474 捕获 PushSendError 即
  `retry_ledger.enqueue_failure`;retry_ledger.py:289-296 入队门槛只剔除
  死信(classify_dead_error)与配置级(is_config_send_error,
  `_CONFIG_ERROR_CODES`=delivery.py:103-110 六码,不含任何 send 族)——
  **17/不确定态若以普通瞬态码上抛,必被自动重投,穿透桥内 120s 防重窗后即双发**。
  另 push_local.py:96-109 `_CODE_NAME_TO_EXIT` 现状未列 17/23(不确定码落兜底
  weixin_local_send_error,push_local.py:447-478 判例)。PushSendError 本体无
  transient 字段(src/myssia/push/base.py:108-127),分类全靠 code。
- F10(grill r2 新增亲验)**磁盘 dylib 是 FAT 双切片,切片哈希==thin 哈希(端到端
  亲跑)**:`/Applications/WeChat.app/Contents/Resources/wechat.dylib`=357,763,680B,
  fat magic=0xcafebabe、nfat_arch=2——arch0=x86_64(cputype 0x1000007)@0x4000
  size 184,590,112;**arch1=arm64(cputype 0x100000c)@0xb010000 size 173,148,768
  (==thin 尺寸)**;对 arm64 切片字节区间算 sha256=**6a5bd0cb…83a7(==thin 文件
  sha256,逐位同)**,切片首 4 字节=0xfeedfacf(MH_MAGIC_64),切片内 0x490fb20
  锚字节与 F7 同。另磁盘存在**第二个同名文件**`Contents/Frameworks/wechat.dylib`
  =84,544B(桩)——basename 歧义真实(§2.6 模块锁定门槛的依据)。
- F11(grill r2 新增亲验)**_raise_for_result 兜底形态**:push_local.py:403-478,
  family 判定在 :447(`_CODE_NAME_TO_EXIT.get(upstream_code, exit_code)`),仅
  14/10/11/12/13/15/30 有分支,**其余(含 17/24/自定义 exit 1 码)一律落尾部兜底
  `PushSendError("weixin_local_send_error", …)`(:474-478),桥码名只进 message
  (detail),不进 `.code`**——never-retry 谓词若只对 `.code` 比对则永失明
  (§3.3 修法依据)。
- F9(grill r1 新增亲验)sendtarget 三形态解析对 username **无任何长度约束**
  (sendtarget.py:1-46 docstring 全读;username 形态=wxid_…/filehelper/gh_…/
  @chatroom)——`@chatroom` 族 id 实际可超 23 字节。

**引自双路报告原文(现已落档 `research/round-reports-阶段3合流输入.md`,grill r1
中危6 补档)**:C1-C6 全部静态结论(含 22 个 spawn 调用者、PreAdd 家族、CGI=
newsendmsg/237、TU 1212 路径表)、hit4 x0 外层承诺对象存疑注记、r1/r3 引用槽位
漂移(+0x2e0/+0x3a0/+0x520)。**特记**:「q=服务对象+0x1c0」仅存在于 C1 报告
原文,一切反编译/转储产物中无独立出处——r4 必须先形验证(§2.4 准入门)才准
入锚定表。

## §1 差距裁定:还缺一块,一次钉入轮补齐

双路合流后的定性:**观察面已钉死,注入面缺一个函数**。

- 已有:队列 API(F1)、任务对象三元组形态(F2)、明文块逐字节布局(F3)、
  捕获方法论(needle 判别门+3s 窗口,cap2.py v2 实战三连绿)、版本锚定手法
  (slide+16B 字节校验,design.md 前置节)。
- 缺:**(对端, 正文) 形参的发送发起函数 F_send**。UI 槽(Qt 信号间接层)静态墙未破
  (C3);泵断点时发起栈已消亡(F4)——0x43f88e4 是观察点,**不是**注入入口,不可直调。
- 补法(=Phase 2 前置的 **r4 钉入轮**,零预算):断点改布**入队侧**——发起路径投递任务
  是同步调用,入队瞬间的回溯栈**必含** F_send 链。静态轮 C1 已明示此策略
  ("运行时断 000a6060/000a5ed0,过滤 cmdid≠100000,即可拿到真实发送任务的 task 指针"),
  本蓝图把它落成 run-sheet(§2.4)。触发=主人手发(D2 标准形态,零预算)。

## §2 调用配方(LLDB expr 可执行形态)

### §2.0 总则

- 直调全程**零断点**(锚点校验+expr 调用不需要断点)→ SIGKILL lldb 无 int3 残留
  风险;需要断点的只有 r4 钉入轮与「observe 式取服务对象」(§2.3),二者必守
  「禁断点→detach」收兵序(cap2.py:75-86 shutdown 判例)。**但零断点≠零残留**:
  attach 态 expr 直调运行于全线程停止的进程上,若 F_send 阻塞等他线程则冻结面
  成立——死锁/冻结预案见 §5,r4 同步返回实测见 §2.4。
- 红线内解释(待 P-0 裁决 2 确认,§4):**参数缓冲区(expr 语句块局部量/自
  malloc 块)与调用栈装载是「调函数」批准范围的组成部分**;禁写的是微信自有的
  代码/数据,以及被调函数正常业务副作用之外的一切改写。
- 正文/对端一律**非 ASCII 安全形态**(十进制字节数组字面量)进 expr,规避编码层;
  长度语义一律按 **UTF-8 字节长**(F3:len 字节=字节数,嘻嘻=6、8 个汉字=24)。

### §2.1 主配方 Tier-1:直调 F_send(r4 产物,预期形态)

**前提**:r4(§2.4)产出 `F_send` 偏移 + 实参 ABI(形参槽位、串传引用/传值、
this 来源)。以下为桥 `senddirect` 模块生成的 lldb 批式 cmd 文件模板
(按 r4 结论填占位符;`S`=slide,运行期解析):

```lldb
attach -p <PID>
script senddirect_probe.preflight()   # ① slide 解析+版本门(§2.6)+服务对象活性验,失败即置 PREFLIGHT_FAIL 并跳过调用
expr -- (int)({                                                       # ② 直调(串=23容量+末字节裸长,F3 形态)
  unsigned char peer[24] = {102,105,108,101,104,101,108,112,101,114,0,0,0,0,0,0,0,0,0,0,0,0,0,10};
  unsigned char body[24] = {229,152,187,229,152,187,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,6};
  ((int(*)(void*,void*,void*))0x<S+F_send_off>)((void*)0x<svc_ptr>, (void*)peer, (void*)body);
})
script senddirect_probe.postflight()  # ③ 读返回值寄存器 x0 + 微信存活断言,落 SENTINEL JSON
detach
quit
```

(上例字节=`filehelper`+len 10、`嘻嘻`+len 6;`body` 由桥按 stdin 正文逐字节生成。)

**双长度门(grill r1 硬伤2;均在 Python 侧、任何 lldb 动作之前)**:

- **正文门**:UTF-8 字节长 >23 → exit 1 `send_direct_body_too_long`(8 个汉字
  =24B 即拒——长度=字节数非字符数,测试钉死 §6);
- **对端门**:`resolve_target` 得到的 username UTF-8 字节长 >23 → exit 1
  `send_direct_target_too_long`(`@chatroom` 族长 id 真实存在,F9;错一个
  =发错人,宁拒不裁)。
- 两门均为零状态拒(未占位未指纹未 attach),拒后可直接走 OCR 链(§3.3)。
- >23B 支持(堆串形态)为可翻案点 §7-6:r4 若证 F_send 接长串堆形态则升级
  malloc 缓冲放开上限;首版不猜。

**实参 ABI 两形态**(r4 定案后二选一,模板已兼容):

- 传引用(预期):F3 的 24B 记录即对象本体,`peer`/`body` 数组取址传入,如上。
- 传值(struct by value,24B):调用形态改为传 struct——r4 在 F_send 入口 dump
  实参槽内存即可分辨(引用=槽里是指针;传值=槽里直接是 24B 记录)。

**实参生命周期裁定(r4 必验项)**:r4 在 F_send 入口记 `peer/body 实参地址`,同轮泵
命中时比对 msgctx `+0x1d8` 正文地址——**不同=F_send 同步拷贝入自有分配**(预期,
msgctx 本身就是拷贝产物),expr 局部缓冲安全;**相同=别名存疑** → 改用
`expr -- (void*)malloc(24)` 分配+memcpy 装载(自建缓冲,每次发送恒定泄漏 2×24B,
G6 频控下可忽略),并在锚定表 `arg_abi.buffer_mode` 记 `malloc`。

### §2.2 备选 Tier-2:任务克隆入队(默认禁用,可翻案点 §7-3)

若 r4 证明 F_send 不可直调(形参携带 UI 上下文闭包等):用 r4 needle 命中时 dump 的
真实发送任务帧+msgctx 块做蓝本——inferior `malloc` 两块、字节复制(读微信内存+写
**自己的**缓冲,不触微信内存红线)、修内部自指针对齐到克隆基址、按 F3 偏移改写
`+0x148`(对端)与 `+0x1d8`(正文)区、`FUN_000a6060(q, 活 name 串, 同 cmdid, 克隆帧)`
入队。**危害声明**:克隆帧内 shared_ptr 控制块是原任务快照,克隆销毁时对微信活对象
重复 release → 引用计数下溢 → 提前释放/崩溃;启用前须先在 r4 dump 里枚举全部控制块
指针并推导 addref 修正,或经主人明批承担风险。**默认否决,仅当 Tier-1 死且主人
翻案才动工。**

### §2.3 否决 Tier-3:CGI 层直调(newsendmsg/237)

protobuf 组装+会话态+mars 编排全链未知,深度远超收益;研究注记,不做。

### §2.4 r4 钉入轮 run-sheet(Phase 2 前置,零预算)

复用 cap2.py v2 框架与 round.sh 骨架,改三处:

1. **断点**:`bp1=S+0x000a6060`、`bp2=S+0x000a5ed0`(enqueue 双 API,F1 亲验)。
2. **判别门(两级)**:主门=needle(当轮正文原字节,`needle.bin` 机制照抄;**必须
   当轮正文**,filehelper 过宽坑在册)扫 `x3`(task)前 512B+一跳指针(cap2
   `_chase_files` 判例);副门(必开,零成本)=每次命中记一行 `{x1 name 串内容
   16B, x2 cmdid, x3}` 清单——若主门未中(正文未在入队时入帧),按窗口内 cmdid
   清单与泵侧命中时间对账定位发送任务的 cmdid,重开窗以 cmdid 为门再来一次(仍
   主人手发,仍零预算)。
3. **命中捕获清单**:x0-x7 全录;x0(q)与 `q-0x1c0` 各 256B(见下准入门);x3(task)
   0x600B+一跳追;**全回溯帧表+逐帧 `image lookup -a` 符号化**(此时栈必含 F_send
   链);F_send 入口侧定位=回溯帧从 enqueue 向上逐帧离线反编译(wxui.gpr,
   DecompileTargets 模板)找 (对端,正文) 形参函数;实参 ABI dump(§2.1)。

**r4 三个必验项(grill r1 中危5/6/硬伤1 前置)**:

- **0x1c0 准入门**:「q=服务对象+0x1c0」目前仅 C1 报告转述(§0 特记),产物无独立
  出处——r4 dump `q` 与 `q-0x1c0` 后必须**先验形再准入**:svc=q-0x1c0 首八字节
  vptr 落在 dylib __TEXT 内(记 `svc_vtable_off=vptr−S`);svc+0x180/+0x188 呈
  C2 泵注册哈希桶形态;enqueue_a/enqueue_b 两断点各自 x0 是否同一 q(不同则分别
  记录,锚定表带 queue_selector)。任一不过 → 0x1c0 作废,回静态重推导服务对象
  来源(不入锚定表,不猜)。
- **F_send 同步返回实测**:入队命中后 continue,确认发起帧是否同步返回(若 F_send
  投递后还要等锁/等他线程=直调死锁红旗,§5 冻结面;红旗则 Tier-1 降级,升 §7-3
  翻案程序)。
- **svc slide 相对指纹**:记录 `svc_vtable_off`(=vptr−slide)与非指针不变字段
  (svc+0x8..+0x20 中不含指针的定值字节)——供 §2.5 跨重启活性验。

**触发**:主人手发「嘻嘻」→文件传输助手(D2 标准形态,主人说「发」→3s 窗口使能)。
**收兵**:命中即禁断点+DONE+SIGINT→detach(判例序)。**产出**:F_send VA+全函数
反编译+实参 ABI+服务对象获取式+锚定表(§2.6)初版。门=implement.md 门 2。

### §2.5 服务对象/单例获取(两式,r4 定案记入锚定表)

- **式 A global(首选)**:r4 静态段在 Ghidra 里找 enqueue 调用点上游的静态槽
  (全局单例指针或 accessor 函数),锚定表记 `service_ptr_mode:"global"`+
  `service_global_off`(+可选 deref 链);直调前读槽+活性验(下条)。
- **式 B observe(兜底)**:同一 lldb 会话内,`bp=S+0x000a6060` 禁用态布防→使能→
  微信自然任务投递秒级即中(泵轮实证任务面极活跃)→读 x0→**立即禁用**→`svc=x0-0x1c0`
  (先过 §2.4 准入门形态)→验 `q+0x48/+0x68/+0x180/+0x188` 可读且形态合理→接着走
  §2.1 调用。断点窗口秒级,收兵序不变;锚定表记 `service_ptr_mode:"observe_bp"`。
- **活性验=slide 相对量(grill r1 硬伤1 定则)**:vptr 值=slide+vtable 偏移,随
  ASLR 每次重启漂移——**锚定表与校验一律存/比相对量**:运行期读 `svc+0x0` 得
  vptr,断言 `vptr−S == svc_vtable_off`(锚定表项);辅以非指针不变字段
  (`svc_invariants_hex`)逐字节比对。**绝不存 vptr 原始字节**(否则重启即恒假阴性
  →恒 exit 24,通道跨重启即死)。锚定不符→24 拒调,**重锚税=微信版本更新**,
  非每次重启。

### §2.6 版本锚定表与 preflight 版本门(桥私有件,600)

`<数据根>/wechat-bridge/send-direct-anchors.json`(私有路径族,不进 config 键面):

```json
{
  "schema": 3,
  "wechat_version": "4.1.15",
  "dylib_arm64_slice_sha256": "6a5bd0cbb39ad3092c15e9debda2db4969eedf1b58caad244d88033a996833a7",
  "anchor_offset": "0x490fb20",
  "anchor_bytes_hex": "ffc305d1fc6f14a9f44f15a9fd7b16a9",
  "offsets": {
    "pump_resume": "0x43f88e4",
    "enqueue_a": "0xa6060",
    "enqueue_b": "0xa5ed0",
    "send_entry": "0x< r4 产物>",
    "arg_abi": {"peer_slot": "x1", "body_slot": "x2", "string_form": "inline23_rawlen", "by_value": false, "buffer_mode": "expr_local|malloc"},
    "service_ptr_mode": "global|observe_bp",
    "service_global_off": "0x…|null",
    "queue_selector": "enqueue_a|enqueue_b|same",
    "svc_vtable_off": "0x< vptr−slide,r4 记录 >",
    "svc_invariants_hex": "< svc 非指针不变字段字节>"
  }
}
```

**preflight 版本门(双层,grill r2 硬伤1 改定:主门=arm64 切片哈希,非 FAT 整文件)**:

- **主门=切片哈希(F10 已端到端亲验的算法)**:attach 后经 `image list -o -f` 取
  进程内 wechat.dylib 模块的**磁盘路径**,读文件头判形:
  - `>I` 前 4 字节==0xcafebabe(FAT):按大端解析 fat_header——`nfat_arch`(偏移
    +4)、`nfat_arch × 20B` fat_arch 表(每项 cputype/cpusubtype/offset/size/align
    皆大端);取 **cputype==0x0100000c(arm64)** 的条目,对磁盘文件
    `[offset, offset+size)` 字节区间算 sha256,与 `dylib_arm64_slice_sha256` 比对。
    F10 实测形态:arm64 切片 @0xb010000、size 173,148,768,切片 sha256==thin 文件
    sha256——**锚定表存的即 thin 基准哈希,门算法与基准自洽**;
  - `<I` 前 4 字节==0xfeedfacf(纯 thin):整文件 sha256 直接比;
  - 其他魔数 → 24(形态未知,不猜)。
  成本=一次 173,148,768B(≈165MiB)读+哈希 ≈1-2s(G6 频控下可忽略)。不符 →
  微信已换包,**全线偏移作废**,exit 24——16B 指令序言碰撞率低但失败模式是
  「错地址直调=崩溃/错发」,主门必须强于 16B;**禁止执行者为提速弱化回 16B 单门**
  (r1 中危7 防约面,本门形态已亲验可行,无弱化理由)。
- **副门=16B 锚字节**:读 `S+anchor_offset` 16B 与 `anchor_bytes_hex` 比对
  (F7 亲验值;指令字节与 slide 无关)。任一门不过 → 24,不调用。
- **模块锁定与 S 解析(写死,含 r2 中危4 歧义门槛)**:磁盘上有**两个**同名
  wechat.dylib(Resources 357,763,680B FAT 主体 + Frameworks 84,544B 桩,F10),
  cap2.py:45-52 的「首个 basename 命中即取」**不作数**。锁定规则:
  1. 遍历 target modules,收集 `basename == "wechat.dylib"` 的全部候选;
  2. 过滤 `__TEXT section byte size ≥ 0x8000000`(128MiB 门槛,主体 ~154MiB 过、
     84,544B 桩必拒),要求**恰好一个**幸存——零个或多个 → 24(不猜);
  3. `S = 幸存模块 GetObjectFileHeaderAddress().GetLoadAddress()`;
  4. 区间断言:`S+anchor_offset+16 ≤ S+__TEXT base+size`,不在区内 → 24;
  5. **绝不取主 Executable / 绝不猜固定基址**;模块缺失 → 24。
  (活体模块枚举的「哪个先被枚举」无档可证——上述门槛使其与枚举顺序无关,这是
  把 r2 未运行项转为设计不变量的方式。)

## §3 桥落地面

### §3.1 CLI 契约:新子命令 `send_direct`

```
wechat-bridge send_direct <id> --file - [--dry-run]
```

- **形态**:与 send_text 完全同族——argv 永不载正文(仅 `-`=stdin);`--dry-run`=
  走到版本门+目标解析+活性验,**不占位不指纹不调用**(可无限重跑,锚定链路实测面)。
- **管线序(单次 lldb 批,grill r1 硬伤3b 定序)**:
  1. `_require_chat_id` + `_read_body`;空正文 usage 拒;**双长度门**(§2.1:
     正文/对端 UTF-8 字节长 >23 → `send_direct_body_too_long`/
     `send_direct_target_too_long`,exit 1)——对端门在步骤 3 解析后立即判;
  2. `localdb.locate_db_storage`+`resolve_keys`;
  3. `sendtarget.resolve_target`(**与 send_text 同一目标解析/同码拒发**,
     send_target_not_found/ambiguous)→ 对端长度门;
  4. 前置门:微信不在 → 10;`lldb` 缺(xcode-select 探测)→ exit 1 `lldb_not_found`;
     配置门 `send_direct_enabled`(§3.2)关 → exit 1 `send_direct_disabled`;
  5. G6+防重合成占位(**与 send_text 共用 `SendRateState`,同 flock 同键同窗**——
     G6 不分级豁免,design.md Step 4 既裁);
  6. spawn 单次 lldb 批(§2.1 cmd 文件:attach→preflight[版本门+活性验]→expr→
     postflight→detach;子进程 45s 硬超时)。**preflight 在占位之后执行是既定事实**,
     回滚规则见下;
  7. **回滚规则(镜像 send_text 判例 cli.py:763-767,写死)**:一切 **armed 前**
     BridgeError——含 exit 24(批内 preflight 失败)、`lldb_attach_failed`、armed 前
     超时 30——**一律 `rollback_reserve` 还原占位**,OCR 回退不再撞 G6 14;
  8. **armed 时点=expr 提交前** `mark_fingerprint_pending`(fail-closed 同判例);
     armed 后任何失败**绝不 rollback**(指纹 pending 在档,uncertain-never-retry);
  9. 回执:`receipt_query` 闭包与 send_text 同一(localdb;(5,10,15)s 退避),
     绿 → `mark_fingerprint_sent`;expr 已交回执未绿 → exit 17。
- **应答形状**(send.send 节,键序稳定供 golden 对账):

```json
{"send": {"chat": "…", "target": {"username": "…", "display_name": "…"},
          "sent": true, "channel": "direct", "anchor_build": "4.1.15",
          "lldb": {"attach_ms": 0, "call_rc": 0, "receipt": "green"},
          "elapsed_ms": 0}}
```

### §3.2 配置门(缺省关)

- 新键 **`send_direct_enabled`**(bool,缺省 `false`)——config.py 封闭清单增补+
  BridgeConfig 字段+bool 校验(照 `mem_search_enabled` 判例:design §4「开关默认关,
  主人显式开启才生效」;本通道豁免依据=主人 10-14 直调批令+P-0 裁决 2+本档)。
  组件 component.json `config_defaults`/`redlines` 同步增补(直调=第二例调试器
  豁免,范围=仅 attach+只读观察+函数直调,禁写微信内存/禁注入/禁常驻)。
- 锚定表路径不入配置(私有路径族固定,§2.6);频控依旧无键(G6 硬编码)。

### §3.3 错误码与降级矩阵(codes.py 增补=本档即 design §6 修订)

| exit | 码名 | 语义 | 降级归属(grill r1 硬伤3a 补全) |
|---|---|---|---|
| 24 | `send_direct_unanchored` | 切片哈希/锚字节/模块/活性验不过(微信已换包)——未调用,零风险+rollback | **→OCR** |
| 1 | `send_direct_disabled` | 配置门关 | push 层**前置跳过直发**(doctor 缓存判 enabled),收到码亦 →OCR |
| 1 | `lldb_not_found` | xcode CLT 缺 | →OCR |
| 1 | `lldb_attach_failed` | attach 拒(并行调试器/权限) | →OCR;**绝不绕过** |
| 1 | `send_direct_body_too_long` | 正文 UTF-8 字节 >23 | →OCR(承诺的「长文走 OCR」唯一执行路径) |
| 1 | `send_direct_target_too_long` | 对端 username 字节 >23 | →OCR(UI 链无此限) |
| 1 | `send_direct_call_failed` | expr 已执行但返回异常+回执红(armed 后) | **→人工,绝不回退绝不自动重试**(与 17 同族:armed 后同指纹 pending 跨通道锁 120s,OCR 同正文重发也被桥拒——交叉防重互锁是有意设计) |
| 复用 | 10/14/17/20/21/22/30 | 微信不在/频控/不确定/库钥族/超时(仅 armed 前) | 10→OCR;14→等待;17→人工 |

**超时与杀伤序列(硬规则)**:lldb 子进程 45s 带宽:先 SIGINT(批式 cmd 余段执行
detach;round.sh 判例)→10s 宽限→SIGKILL。armed(expr 已提交)后超时=17;
armed 前超时=30+rollback。**SIGKILL 不保证 PT_DETACH → 微信可能残留停止态
(冻结非崩溃),检测/恢复预案见 §5。**

**push 侧落地(MYIA 接线批,grill r2 硬伤2 重写:码名必须原样穿透,否则
never-retry 链路失明)**:

1. **直发分支前置拦截(修法核心)**:push_local 直发路径在调
   `_raise_for_result` **之前**先解析桥 stdout 的 `error.code`,按码名三分:
   - `code ∈ {send_uncertain_dedup, send_direct_call_failed}`(never-retry 集):
     `raise PushSendError(code, …)`——**桥码名原样作 `.code`**,镜像 14→
     send_rate_limited 的分支形态但不换名(F11 实证:不这样做则落 :474-478 兜底,
     码名只进 message,谓词永失明,双发面存活);
   - `code ∈ {send_direct_unanchored, send_direct_disabled, lldb_not_found,
     lldb_attach_failed, send_direct_body_too_long, send_direct_target_too_long}`
     (fallback 集)+ family 10:内部转 `send_text` 二段尝试(分级矩阵的执行点),
     二段结果走既有 `_raise_for_result`;
   - 其余:走既有 `_raise_for_result`(14/30 等既有分支不动)。
2. `_raise_for_result` 增 never-retry 分支兜底(防直发路径外的漏网形态,如
   exit 17 从旧 send_text 语义到达):family 17 → `PushSendError(upstream_code
   or "send_uncertain_dedup", …)` 码名原样;`_CODE_NAME_TO_EXIT`(96-109)增列
   `send_uncertain_dedup:17`、`send_direct_unanchored:24`。
3. **重试账本 never-retry 谓词(F8 实证必改)**:delivery 重试链会对非死信非配置级
   的 immediate 失败自动重投——在 delivery.py 增 `is_never_retry_send_error`
   (码集={send_uncertain_dedup, send_direct_call_failed}),`enqueue_failure`
   门槛与 `is_config_send_error` 并列同拒(delivery.py:293 判例位)。**该谓词的
   生效前提=第 1 条的码名原样穿透——二者缺一即漏**(§6-9 全链测试锁双环)。
4. 分级调度矩阵=上表「降级归属」列;`weixin_local_send_channel: "auto"|"ui_only"`
   (缺省 auto=direct-first;disabled/无锚定表时等价 ui_only)。

### §3.4 模块与单测挂点

- 新模块 `wechat_bridge/senddirect.py`(lldb cmd 生成/PREFLIGHT/SENTINEL 协议/
  超时策略/收兵序)+ `senddirect_probe.py`(lldb 内脚本,随包分发);cli.py 增
  `send_direct` 分支;probe.py doctor 增 `direct_channel` 节(§3.5)。
- lldb 驱动协议=round.sh 判例的桥内化:cmd 文件→哨兵文件(ARMED/PREFLIGHT_FAIL/
  DONE/ERROR)→SIGINT 收兵;桥侧全程 `subprocess` + 硬超时,无常驻调试器。
- **cmd 工件是唯一会碰微信内存的产物**:生成函数纯函数化(输入=锚定表+slide+
  目标+正文,输出=cmd 文本),供 §6 golden 直测。

### §3.5 doctor 探针(恒 exit 0,零前台扰动)

`doctor` 应答新增节 `direct_channel`:`{enabled, anchored:
"ok"|"mismatch"|"no_anchor_file"|"unknown", lldb: "ok"|"missing",
last_anchor_build, slice_sha256_matched}`——轻量 attach(无断点)+切片哈希主门
(§2.6 算法)+16B 副门+detach(≈5-8s,含 ~165MiB 读);attach 不畅时如实
`unknown` 不判死。探针失败≠通道失败,发送时自会再验。

## §4 白名单验证计划(P-0→P-2,三道门)

### P-0 主人裁决门(两项,先于一切发送)

> **✅ 已裁(2026-10-15 凌晨,主人令原文「C,自动化情况下,可以发无数条信息的」)**:
> 裁决 1=(c) 上调帽——自动化发送总量不限;G6 节奏护栏(单条/≥10s)保留
> (在案红线「必须保证不能被封禁」的防封保护,非预算)。裁决 2(串构造新造
> inline23_rawlen)=依主人总体放行意图**视同已批**(r2 修订缓解面全在档:
> 双长度门/ABI dump/生命周期比对);如主人有异议随时翻案。

1. **预算**(升裁,原有):账本=勘察 6+r1 桥断言超时 1(实际出站 0,计否旧留裁)+
   动态轮桥真发 3(F5 实锤)=**9~10/10,余 0~1**;而 P-2 需 2 条。裁决项:
   (a) r1 零出站不计→余 1,再批 +1;(b) 直接批 +2;(c) 上调帽。
   **任何验证发送前未得裁决=不发。**
2. **串构造判例翻案**(grill r1 中危8,新增;判例 b4fb27e 同款升主人过目):
   design.md:73(同任务前置设计,标「实证」)明令「this 与字符串实参一律复用活
   对象,不新造……不在 lldb 里构造 libc++ 临时对象」;§2.1 改为**自造 24B
   inline23_rawlen 记录**(F3 仅证 msgctx 字段形态,非 F_send 形参形态)。缓解面
   已在档(r4 ABI dump+生命周期比对+双长度门),但「新造 vs 复用活串」的翻案须
   主人一句确认;未确认前 r4 可跑(纯观察),**P-2 前必须落裁**。

### P-1 r4 钉入轮(零预算,§2.4)

主人手发 1 条(嘻嘻→filehelper)换 F_send 全套产物+三必验项(0x1c0 准入/同步
返回/slide 相对指纹);门=implement.md 门 2。

### P-2 白名单双发矩阵(预算 2 条,先报后发)

| # | 目标 | 正文 | 通道 | 回执通道 | 判据 |
|---|---|---|---|---|---|
| 0 | — | — | `send_direct --dry-run` | — | 走到活性验即停,零占位零指纹(不耗预算) |
| 1 | filehelper | 嘻嘻 | send_direct | **sqlite 直查** `decrypted/message_0.db`(时间窗+内容+local_type=1;〔勘误 10-15 簿记补落:表名映射「缺陷」已判误诊撤销=design.md Step3.4 勘误——md5(username) 映射成立、真因副本重建时延;sqlite 直查保留为独立第二通道交叉验证〕) | 出站恰 1+回执绿+微信存活 |
| 2 | jiangliushi666 | 嘻嘻 | send_direct | 桥 `localdb query <wxid> --since 1d`(wxid 路径正常) | 同上;与 #1 间隔 ≥10s(G6 自动强制) |
| 3 | filehelper | 嘻嘻(同 #1) | send_direct(立即重跑) | — | **防重验证**:exit 0+`deduped:true, sent:false`,出站仍=2(120s 窗幂等,不耗预算) |
| 4 | filehelper | 嘻嘻(同 #1) | `send_text`(UI/OCR 链,立即) | — | **跨通道互锁验证**:同指纹跨通道被拒(deduped 或 17),出站仍=2(不耗预算,只验状态文件拒发) |

- **AC2/AC3 合并**:#1 即「直调一次成功」验,#2-#4 完成双发+防重+跨通道矩阵;
  总出站=2。
- 全程纪律:uncertain-never-retry;连续 3 次同域失败停手升维(错题集 D2);每条
  先报后发;detach 干净微信零伤在案纪律。
- 终验后收尾:锚定表固化+doctor 三态绿+错题集随发现随补。

## §5 风险与红线

- **批准范围**(主人 10-14 批+P-0 裁决 2 确认):attach + 只读观察 + 函数直调。
  **禁**:写微信自有代码/数据;代码注入(dylib 加载/fishhook/建线程);改签名/改
  entitlement;常驻调试器;绕过 attach 失败(attach 不通=降级,绝不硬闯)。
- 参数缓冲(expr 局部/自 malloc)与被调函数的业务副作用(=发消息本身)属批准范围
  (§2.0 界定,待 P-0 裁决 2);Tier-2 克隆若启用,克隆缓冲同属,但 shared_ptr
  双释放危害须单独明批(§2.2)。
- 断点残留:直调路径零断点;含断点的 r4/observe 式必守「禁断点→detach」,
  超时先 SIGINT 后 SIGKILL(§3.3)。
- **冻结面(grill r1 中危5 新增)**:attach 态 expr 直调运行于全线程停止的进程上;
  若 F_send 阻塞等他线程(投递后等锁/等回执),expr 挂起→45s 超时→SIGINT 对运行中
  expr 常不可中断→+10s SIGKILL lldb,**SIGKILL 不保证 PT_DETACH → 微信可能残留
  停止态(冻结而非崩溃)**。预案:(i) r4 同步返回实测为 Tier-1 前置(§2.4);
  (ii) 任何 SIGKILL 收兵路径后,桥必做**存活探测**(pgrep WeChat + 现有 doctor 零
  成本 ax ping/窗口响应;冻结的判别=进程在而窗口无响应);(iii) 冻结=结构化报告
  `wechat_frozen` + 人工重启指引,**绝不自动 kill 微信**;(iv) 冻结探测分支进
  §6 测试(桩模拟)。
- 版本漂移:arm64 切片哈希主门(§2.6 算法)+16B 副门,不符即 24 拒调,永不「试试看」;微信更新=重锚
  税(非重启,§2.5),OCR 链兜底。
- 隐私:argv 零正文(仅 stdin);诊断/日志只载形状;锚定表不含内容材料;直发载荷
  键与 send_text 同纪律。
- 预算:P-0 两项未裁不发(§4);触发首选主人手发零耗形态。

## §6 测试计划(打桩判例,全离线)

新 `tests/wechat-bridge/test_send_direct.py`(lldb 全桩:monkeypatch
`senddirect._run_lldb` 或 PATH 注入假 lldb 可执行,SENTINEL 协议回放):

1. 门关→exit 1 `send_direct_disabled`;未知配置键仍拒;`send_direct_enabled`
   形状校验;
2. 版本门夹具(切片哈希不符/锚字节不符/模块缺失/双模块歧义)→24,**且断言未生成 expr 段
   cmd + rollback 断言:send_state 还原,后续 `send_text` 不被 14 拦(grill r1
   硬伤3b/硬伤4iv);
3. **cmd 工件 golden(硬伤4i,唯一碰微信内存的产物)**:生成函数直测——peer/body
   十进制字节数组逐字节对账;**len 字节=UTF-8 字节长非字符数**(夹具:「嘻嘻」
   →{229,152,187,229,152,187,…,6};「8 汉字」拒);`0x<S+F_send_off>` 代入
   算术断言;
4. 快乐路(假 lldb 回放 PREFLIGHT_OK+call_rc=0+回执绿夹具)→exit 0+载荷形状
   golden(含 channel:"direct");dry-run→零 send_state 写入;
5. armed 后回执不绿→17 且指纹 pending 在档;armed 前超时→30+rollback 断言;
   dedup 幂等→exit 0 deduped;间隔门→14;目标未解析→`send_target_not_found`;
   空正文→usage;正文 24B(8 汉字)→`send_direct_body_too_long`;对端 41B
   chatroom 夹具→`send_direct_target_too_long`(硬伤2/4iii);
6. **跨通道互锁(硬伤4ii;夹具钉死 r2 轻微5)**:direct 成功后 10s 内
   `send_text` **异指纹**(异正文夹具——同指纹会先撞指纹门得 dedup 而非 14,
   与下条互斥)→14;同指纹跨通道(direct 后立即 text 同正文同目标)→deduped
   幂等 exit 0 零出站;
7. codes 24 名映射;doctor direct_channel 三态;
8. 冻结分支:SIGKILL 收兵桩(SENTINEL 缺失)→存活探测被调→`wechat_frozen`
   结构化报(中危5);
9. MYIA 侧(§3.3,r2 硬伤2 全链形态):**必须从 channel.send 全链驱动**——桩
   runner 回放桥 exit 17 载荷(error.code=send_uncertain_dedup)→断言
   (i)PushSendError.code=="send_uncertain_dedup"(码名原样,非
   weixin_local_send_error);(ii)该异常过 `enqueue_failure` 被拒收(账本空);
   `send_direct_call_failed` 载荷同双断言;**不许只对 is_never_retry_send_error
   谓词函数单测了事**(谓词单测绿而链路漏=r2 硬伤的原形态);降级矩阵全链:
   {24,10,body_too_long,target_too_long} 桩载荷→断言内部转 send_text 二段被调、
   {17,call_failed}→不转二段直接上抛;push_local 码表增列断言。
- 门禁=`uv run --no-sync python -m pytest tests/wechat-bridge -q` 全绿基线不回退
  (本蓝图会话未运行:wechat_bridge/ 现无 senddirect.py,设计阶段无码可跑,落码
  时跑)。

## §7 可翻案点(默认方案+翻案条件)

1. **新子命令 send_direct**(vs send_text --channel):默认新子命令——UI 链 1257
   测试基线零扰动、契约面隔离;翻案条件=主人偏好单入口。
2. **24 号码与 exit1 自定义码族切分**:默认如表;翻案=主人/MYIA UI 映射需要。
3. **Tier-2 任务克隆**:默认否决(shared_ptr 双释放危害);翻案=Tier-1 实证死
   (含 r4 同步返回红旗)且主人明批风险。
4. **锚定表=私有固定路径**(vs 配置键):默认固定;翻案=多锚定表切换需求出现。
5. **doctor 轻 attach**:默认做(零断点);翻案=主人不喜 doctor 附加→降级
   config-only 态。
6. **23B 双长度门**(inline 串容量,正文+对端):默认硬限+引导 OCR;翻案=r4 若证
   F_send 接长串堆形态(则模板升级 malloc 缓冲,上限放开)。
7. **MYIA 分级调度放 push 层**:默认在通道层做矩阵;翻案=改调用方策略。
8. **串构造判例(design.md:73 复用活对象 → §2.1 自造 inline23 记录)**:默认自造
   (缓解=r4 ABI dump+生命周期比对+双长度门);**P-0 裁决 2 未过前不动 P-2**,
   主人不批则回退「复用活串」形态(仅限回放当轮已捕获正文,通道降级为验证件)。

## §8 实施顺序(对齐 implement.md 门制)

1. **P-0 双项裁决**(§4,主人:预算+串构造判例)——阻塞一切发送;
2. **r4 钉入轮**(§2.4,零预算,门 2;三必验项)→ 锚定表 v1;
3. **桥落地**(§3,离线可先行:码/配置/模块/doctor/单测全桩,门=tests 全绿);
4. **P-2 双发矩阵**(§4,预算 2,门 3+AC3;#4 跨通道互锁零耗验证);
5. **收尾**:MYIA 分级调度+重试账本 never-retry 接线+装机冒烟+grill 门 4+
   detect-changes。
