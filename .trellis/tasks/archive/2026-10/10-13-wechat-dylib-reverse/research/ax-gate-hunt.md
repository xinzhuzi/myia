# AX 激活门狩猎 + 内部发送路径(2026-10-14)

对象:微信 mac 4.1.15 `Resources/wechat.dylib` 的 arm64 薄片(173MB,`~/ghidra-wxhunt/wechat_arm64.dylib`,与 fat 档 cmp 一致,见 `ghidra-pipeline.md`)。
Ghidra 工程:`~/ghidra-wxhunt/ghidra-wxui`(已全量分析)。狩猎脚本:`research/ghidra_scripts/HuntXref.java`;轮次日志:`research/ax-hunt-round{1..9}.log`(round4b 起反编译可用)。

## 0. 地址映射注记(必读)

**VA = fat 文件偏移 − 0xB010000**,对全部文件后备段精确成立。验证:

- `lipo -detailed_info /Applications/WeChat.app/Contents/Resources/wechat.dylib` → arm64 切片 `offset 184614912` = **0xB010000**(x86_64 切片 offset 16384/size 184590112)。
- 薄片段映射(`otool -l`):`__TEXT` vmaddr 0x0/fileoff 0;`__DATA_CONST` vmaddr 0x9b34000/fileoff 162742272(=0x9b34000);`__DATA` vmaddr 0x9fec000/fileoff 167690240(=0x9fec000)——**vmaddr−fileoff ≡ 0**,故薄片内文件偏移==VA。
- Ghidra 基址 0(`imageBase=00000000`,导出 JSON 首函数 `FUN_00017000`)。

即:**Ghidra 地址 == VA == 薄片文件偏移 == fat 偏移 − 0xB010000**(字符串区/`__objc_selrefs`/`__const` 等文件后备区皆适用;纯运行期指针受 chained-fixups 影响,须以 Ghidra 解析值为准,裸文件读出的是编码 fixup 值——本文所有 typeinfo/虚表指针均取 Ghidra 解析值)。

## 1. 环境修复:mac_arm_64 反编译器

官方 zip(ghidra_12.1.4)只带 linux/win 原生件,`DecompInterface.openProgram=false`,runlog 明示 `ERROR os/mac_arm_64/decompile does not exist`。修复(2026-10-14,exit=0):

```bash
cd .../Ghidra/Features/Decompiler/src/decompile/cpp
make ghidra_opt -j8 ARCH_TYPE="-arch arm64" ADDITIONAL_FLAGS="-w"   # /tmp/decomp_build.exit: exit=0
cp ghidra_opt ../../../../../os/mac_arm_64/decompile                 # 注意:运行时目录是 Features/Decompiler/os/,不是 src/decompile/os/
```

轮4b 起 `openProgram = true`,反编译全通。

## 2. Qt AX 激活门:结论与证据链

### 2.1 门本体(指令级)

**`QCocoaAccessibility::notifyAccessibilityUpdate` @ 0x70b32bc**(虚表槽 +0x20 即 vptr+0x10;由 qWarning helper 0x713c940 打印 "QCocoaAccessibility::notifyAccessibilityUpdate: invalid element" @0x99267f4 反向定位):

```asm
70b32dc: 39402008   ldrb w8, [x0, #0x8]    ; m_active @ this+8
70b32e0: 340005a8   cbz  w8, 0x70b3394     ; ==0 直接返回,不发任何 NSAccessibility 通知
```

反编译同形态:`if ((*(char *)(param_1 + 0x8) == '\0') || !iface->isValid()) return;`——与上游 `qt/qtbase:src/plugins/platforms/cocoa/qcocoaaccessibility.mm` 的 `if (!isActive() || ...) return;` 逐字对应(zread 读 master 源对照)。

### 2.2 门锁与钥匙

| 角色 | 地址 | 证据 |
|---|---|---|
| 标志清零(唯一天然写 0) | `QPlatformAccessibility::ctor` **0x6c4a76c** | `str x8,[x0]`(vptr=0x9fd24d8)+ **`strb wzr,[x0,#0x8]`** |
| cocoa ctor | **0x70b3284** | `bl 0x6c4a76c` 后存 vptr 0x9fe7e68;调用者=FUN_0706b16c(QCocoaIntegration ctor 区) |
| **钥匙:setActive(bool)** | **0x6c4ad50** | `strb w1,[x0,#0x8]; mov x0,x1; b 0x6c45d60`(尾跳遍历 bridge 表转发激活) |
| 实例获取 | `QCocoaIntegration::instance` 0x706bef4;`accessibility()`= vtable+0xb0 槽 | 见 0x7093f50 调用序列 |
| 虚表 | QPlatformAccessibility @0x9fd24c8(vptr 0x9fd24d8);QCocoaAccessibility @0x9fe7e58(vptr 0x9fe7e68) | typeinfo 链:16QAccessibleCache@0x9705c38 / 22QPlatformAccessibility@0x9705cb4 / 19QCocoaAccessibility@0x983b3c9;QCocoaAccessibility typeinfo @0x9fe7e98 的 base=@0x9fd2508 |

### 2.3 激活入口:上游 3 个,本体内只剩 1 个

上游 `qnsview_accessibility.mm`:`accessibilityAttributeValue:` / `accessibilityHitTest:` / `accessibilityFocusedUIElement` 三个系统 AX 入口都先 `[self activateQtAccessibility]`(→ `QCocoaIntegration::instance()->accessibility()->setActive(true)`)。

本体(QNSView 方法表 @0x715a088,125 项,相对式 int32 解码):

| 入口 | IMP | 激活调用 |
|---|---|---|
| `accessibilityAttributeValue:` | **0x7093f50** | **有**(devirtualize 成直调):`bl 0x706bef4(instance); ldr x8,[x8,#0xb0](accessibility); blr; mov w1,#0x1; bl 0x6c4ad50(setActive)` @0x7093f68-0x7093f7c |
| `accessibilityHitTest:` | 0x7093fe0 | **无**(只剩 `childAccessibleElement` 转发) |
| `accessibilityFocusedUIElement` | 0x709400c | **无** |

`activateQtAccessibility` selector/字符串在体内**完全不存在**(741,021 行 strings 全表无此串;若三入口都剥掉,ld64 objc 去虚化也无从保留)。setActive 另有一个 DATA 引用 @0xa5c25be(静态表项,未追)。

### 2.4 树供给侧(为什么只有 5 节点)

- `-[QNSView childAccessibleElement]`(selector @0x992a8ac,stub 0x71429c0)→ `platformWindow->window()->accessibleRoot()`(上游);`-[QNSView platformWindow]` @0x7094020(反编译已核)。**若 mmui 自绘窗的 accessibleRoot() 返回 nil,树止步窗级**——与侦察到的"5 节点"吻合(此推断未经动态验证)。
- 按需接口创建链完整在体:`QAccessible::queryAccessibleInterface` @0x6c45c98(先查缓存 0x6c48e10,miss 则 insert)→ 被 QMacAccessibilityElement 方法调用(0x70b159c/0x70b3248/0x70b31b8/0x70b6aec 等)。
- `QAccessibleCache`:**insert @0x6c48e88**(日志 "insert - id:"/" iface:",并 connect QObject::destroyed 自动清除)、**deleteInterface @0x6c489fc**("delete - id:"),虚表 @0x9fd2240(D1 0x6c49e2c/D0 0x6c49e48),typeinfo @0x9fd22e0,**基类=QObject**(base typeinfo @0x9fe0e60,name "7QObject" @0x97ab12d)。
- 日志类别:qt.accessibility.core @0x99145e8(getter FUN_06c44d1c,类别对象 @0xa519b70);qt.accessibility.cache @0x99147fd(类别对象 @0xa519b98)。
- 基类虚函数鉴定:setRootObject @0x6c4a960、initialize @0x6c4aa04(加载 QAccessibleBridge 插件,iid 串 "org.qt-project.Qt.QAccessibleBridgeFactoryInterface" @0x9914836)、cleanup @0x6c4acf4;cocoa 子类把这三个覆写为空 `ret`——**与上游一致,不是篡改**(上游本来就是空实现)。
- `-[QMacAccessibilityElement isAccessibilityEnabled]` @0x70b14b4:元素级 State 位(取 iface vcall+0x80 的 bit0 取反),**不是全局门**。QMacAccessibilityElement:class_ro @0x9ff4ac8(name @0x993465e),方法表 @0x7159a50(39 项)。

### 2.5 LLDB 侧落点(供下步裁决,本轮未做任何动态操作)

- 开门最小动作 = 找到 QCocoaAccessibility 实例(运行期 vptr == slide+0x9fe7e68,或 `QCocoaIntegration::instance()` vtable+0xb0 槽)后 `*(char*)(inst+8)=1`,等价于 0x6c4ad50 的 `setActive(true)`。
- 但**开了门≠有树**:树要 `accessibleRoot()` 非 nil(见 2.4),而通知(焦点/值变化等)恢复的判定就是本门。微信侧 accessibleRoot 是否实现,静态未证实。

## 3. 内部发送函数路径(红线裁决供材料;零调用、零注入)

| 证据 | 地址/链 | 说明 |
|---|---|---|
| `SendMsgFtouser…` 串 @0x88bac38 | **FUN_031ab38c**(3400B,上游 0x45a5b18) | 发消息主流程:XOR 混淆串现场解码(`(x+0x8a)^k[i&0xf]`)、按会话类型分支,RPC 桩 **FUN_05e1d050**(service id 0xa13/0xa18/0xa1d/0xa23/0xa28/0xa2f 分支),涉及 "newmsgid/sec_msg/bubble_t/preview" 字段簇 @0x88babb8 |
| 同串谓词 | FUN_048a9a38(上游 0x45a5ae8、0x4d20688) | 判断 std::string 是否等于解码后的 "SendMsgFtouser…" |
| appmsg 路 | `CoSendAppMsgCgi` @0x88a8fb0 → FUN_03092230(7 处引用) | 发 AppMsg CGI 侧 |
| 校验路 | `SendMessageCheckForwardMessage` @0x88a7350 → FUN_03078770/0x307c524/0x30734fc | 发送前检查/转发 |
| 网络层 | functionlist XML @0x986fb9c:`newsendmsg` reqid=237、`sendmsg` reqid=2,long-link `/cgi-bin/micromsg-bin/`(uslong1-8.wechat.com) | ilink 长/短链 CGI 映射 |
| ilink 家族 | `ilink_sdk_core.c` @0x875cfe0、`ilink_helper.cc` @0x8a10270、`~ILinkCloudProxy` @0x8a0fc80、`ilink.HttpHeader/ilink.IlinkCmdIt/ilink.IlinkC2CCd` @0x8aeefc0 | 网络栈命名空间 |
| 排除项 | `sendMessageToWeTypeWithEncodedData:` @0x992fd22,IMP 0x44db878,属主类 **WeTypeStickerService**(class_ro @0x9ff0220,name @0x99340f3),调用者 FUN_044dbc3c | 是**微信输入法贴纸桥,不是聊天发送**;`OnSendMessage` @0xa022b6f 零引用 |

红线注记:上述均为静态定位;未 attach 进程、未调用任何内部函数、未写微信侧数据。是否允许通过这些内部路径发消息属主人裁决事项。

## 4. 过程排雷(避免后人踩)

1. `strings -a -t x` 的偏移即 VA(vmaddr==fileoff);但 __DATA_CONST 指针裸读是 chained-fixup 编码值,typeinfo/虚表链必须在 Ghidra 内解。
2. Ghidra Mach-O 块按 section 命名(`const`/`objc_selrefs`),findPtr 扫"块名含 DATA"会漏——改扫全部已初始化块。
3. objdump 立即数印作 `#0x8`,正则写 `#8]` 会全军覆没(本文 setActive 差点因此漏网)。
4. 相对方法表 entsize=0x8000000c(int32 有符号,别用无符号比较);IMP=entry+8+int32@(entry+8)。
5. 上游对照用 zread 读 qt/qtbase master:qcocoaaccessibility.h/.mm、qnsview_accessibility.mm——本体的空虚槽与上游一致,唯一实质差异是 2.3 的两个入口激活调用被剥。

## 5. 诚实边界

- 未动态验证:开门(LLDB 写 +8)后树是否变深、`accessibilityAttributeValue:` 是否会在实际 AX 查询中被触发——静态无法回答,需下一步 LLDB 实验(红线允许范围内由主人裁决)。
- 微信 mmui 窗口类是否实现 accessibleRoot() 未证实(需识别其窗口类虚表,本轮未展开)。
- 0xa5c25be(引用 setActive 的静态表)未追;setActive 全量调用者以 Ghidra xref 为准=2 处(0x7093f7c + 该表项),不存在其他直调。
- 发送路径只到"函数与调用链+RPC 桩+CGI 映射"粒度,参数结构(消息体序列化)未还原。
