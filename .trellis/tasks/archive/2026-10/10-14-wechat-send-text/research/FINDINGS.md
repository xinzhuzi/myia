# 微信 4.1.15 Qt 无障碍激活门——静态逆向结论(2026-10-13)

目标档:/tmp/wechat_arm64.dylib(173MB arm64 薄片;Ghidra 工程 /tmp/ghidra-wxui,程序名 wechat_arm64.dylib,imageBase=0)。
**地址换算:全段 vmaddr==fileoff(otool 实证:__TEXT 0/0、__DATA_CONST 0x9b34000/0x9b34000、__DATA 0x9fec000/0x9fec000),文件偏移即静态 VA;运行时地址 = wechat.dylib slide + VA。**

## 结论:门 = QCocoaAccessibility 单例对象 +8 的 1 字节 active bool

微信静态链接 **Qt 5.15.14 定制构建**(证据:/tmp/wxrev/decomp/0706b16c_O_FUN_0706b16c.c L133 字符串 "Loading macOS (Cocoa) platform plugin for Qt 5.15.14")。该构建 QPlatformAccessibility 剥离了 QObject 基(vtable 仅 6 槽)。

### 对象与门定位链
| 元素 | 静态 VA/位置 | 证据 |
|---|---|---|
| QCocoaIntegration 单例指针 DAT_0a52be48 | 0x0a52be48(__DATAS/__common zerofill) | decomp/0706bef4_G(L6 `return DAT_0a52be48;`= instance()) |
| QCA 实例成员偏移 +0x30 | QCocoaIntegration+0x30 | decomp/0706b16c_O L81-83:`__Znwm(0x10);FUN_070b3284();*(param_1+0x30)=…` |
| QCA vtable(vptr 值) | VT@0x9fe7e58,vptr 值 0x9fe7e68 | out/ax_vtables.tsv(RTTI "19QCocoaAccessibility"@0x983b3c9 → ZTI@0x9fe7e98 → VT) |
| **门(数据)** | **QCA 单例 +8(1 字节)** | decomp/070b32bc(L26 `*(char*)(param_1+8)=='\0'` → notify 全跳) |
| **写门函数** | **FUN_06c4ad50(qpa, bool)** @0x06c4ad50 | decomp/06c4ad50_G(L6 `*(char*)(param_1+8)=(char)param_2;` L7 FUN_06c45d60=广播桥数组) |

### 自然置位点(为什么门平时是关的)
QNSView 的三个 AX 入口(AppKit 每次无障碍查询时调)都会先 `activateQtAccessibility`:
- 0x07093f50 accessibilityAttributeValue:(L14-16:`FUN_0706bef4()` 单例 → vtable+0xb0 accessibility() → `FUN_06c4ad50(x,1)`)
- 0x07093fe0 accessibilityHitTest: / 0x0709400c accessibilityFocusedUIElement(同型)
与 qt/qtbase qnsview_accessibility.mm(master)逐行吻合:`- (void)activateQtAccessibility { QCocoaIntegration::instance()->accessibility()->setActive(true); }`。
**门关着的原因**:AXEnhancedUserInterface 写入被拒 → AppKit 视进程 AX 未增强 → 不向 QNSView 发协议查询 → activateQtAccessibility 永不执行 → active 恒 0。另外 QNSView::accessibilityIsIgnored 恒 YES(0x07093f48,Qt 原版设计:容器不入树,靠 accessibilityAttributeValue:(Children) 返回 NSAccessibilityUnignoredChildrenForOnlyChild(childAccessibleElement) 挂 Qt 子树)。

### AX 树构建链(树展开用,不走 active 门)
QNSView::childAccessibleElement(0x07093ed8)→ QWindow::accessibleRoot()(vtable+0x78 懒建)→ QMacAccessibilityElement elementWithId:(0x070b1068)→ QAccessibleCache::instance()(0x06c48cfc,QAC vtable 0x9fd2250)→ interfaceForId → iface->childCount/child → unignoredChildren(0x070b69f4)。

## LLDB 热激活配方(单次执行,G6 频控)
```lldb
(lldb) attach -n WeChat
(lldb) image list -o -f          # 找 wechat.dylib 行,记 ASLR offset 为 S
# P1 定位 + 自检(不匹配即停,防版本漂移)
(lldb) expr -- uint64_t $S  = <slide 十六进制>
(lldb) expr -- uint64_t $integ = *(uint64_t*)($S + 0x0a52be48)
(lldb) expr -- uint64_t $qca    = *(uint64_t*)($integ + 0x30)
(lldb) expr -- *(uint64_t*)$qca          # 必须打印 == $S+0x9fe7e68(QCA vptr)
# P2 写门(两选一;走函数含桥广播,更完整)
(lldb) expr -- ((void(*)(uint64_t,uint64_t))($S + 0x06c4ad50))($qca, 1)
#   或直写字节:  memory write $qca+8 01
# P3(若进程外枚举仍 5 节点)AppKit 侧进程内置增强位(实验步):
(lldb) expr -- (void)[(id)NSApp accessibilitySetValue:(id)@"YES" forAttribute:(id)@"AXEnhancedUserInterface"]
# P4 验证:进程外用 AXUIElement 枚举窗 AXChildren(桥 ax.py),期望 >5 节点;读门验证 FUN_070b32bc 断点
```
主人红线合规:无注入、无重签、无 hook;仅 LLDB 调函数/写字节(已批热激活范围)。

## 产物索引(/tmp/wxrev/)
- out/ax_strings.tsv、ax_vtables.tsv、ax_xref.tsv、ax_objc.tsv、ax_classes.tsv(xref/RTTI/类方法表)
- decomp/(7 轮 240+ 函数:AxHunt/AxDec/AxXref/AxObjc/AxClass/AxGate/AxTail5)
- scripts/(Ax*.java)、tool/(Ghidra 12.1.4 + 自编 arm64 decompiler)、axhunt1.log…axtail5.log

## 未尽事项(如实)
- 运行时未实弹(本任务为静态定位);配方带 vptr 自检兜底。
- P3(AppKit 进程内置 AXEnhancedUserInterface)为推断候选,静态档无 AppKit 内部证据。
- QAccessibleCache 单例惰性构造于 FUN_06c48cfc(__cxa_guard),首查自动就绪,无需预热。
