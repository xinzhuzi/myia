# 微信 mac wechat.dylib 逆向:UI 栈鉴定与自动化路径

## Goal

主人令(2026-10-13):用 ghidra-reverse 技能研究微信 mac 本体(Resources/wechat.dylib 357MB)。目标:①鉴定自绘 UI 栈(andromeda.framework/libEGL/GLES 线索→Skia?自研?);②找 UI 引擎内部无障碍/渲染开关的 Mac 对应物(若有,LLDB 可开);③定位内部发送消息函数路径(字符串 xref:ilink sendmessage/SendMsg)为红线裁决供材料。Ghidra 需重装(12.x,GitHub 直下)

## Requirements

- TBD

## Acceptance Criteria

- [x] AC1(Goal① UI 栈鉴定):mmui 命名空间+andromeda.framework+libEGL/libGLESv2(GPU 渲染),静态链完整 Qt(见侦察记录)。
- [x] AC2(Goal② 无障碍门 Mac 对应物):AX 激活门指令级闭环(见终局注记;开门与否属红线裁决)。
- [x] AC3(Goal③ 发送消息函数路径):SendMsgFtouser 主流程+RPC 桩+CGI 映射定位(见终局注记;是否启用属红线裁决)。

## Notes

- Keep `prd.md` focused on requirements, constraints, and acceptance criteria.
- Lightweight tasks can remain PRD-only.
- For complex tasks, add `design.md` for technical design and `implement.md` for execution planning before `task.py start`.

## 侦察记录(2026-10-13 晚)

- **二进制版图**:真身=Resources/wechat.dylib(357MB 胖档,x86_64+arm64;主壳 186KB+Frameworks 壳 84KB 皆是加载器);已抽 arm64 薄片 /tmp/wechat_arm64.dylib(173MB)。
- **翻案发现**:真身静态链完整 Qt——qt.accessibility.core/cache、QAccessibleFactory/BridgeFactory、qt.widgets.painting、qt.qpa.fonts 字符串俱在(此前"mac 非 Qt"结论系查壳所致,已勘误记忆)。**Qt 无障碍门在 mac 存在,Windows replica 热激活路有 Mac 对应物**。
- **UI 栈**:mmui 命名空间 + andromeda.framework(114KB 壳)+ libEGL/libGLESv2(GPU 渲染)。
- **已试未开门**:①AX 属性激活两级拒(-25208/-25205);②容器 plist kDisableAccessibleKey=false+重启(树仍 5 节点)。
- **Ghidra**:猎钥线档案载 ~/ghidra-wxhunt,现已不存在(全位置搜索无果,疑磁盘清理误清);12.1.4 重下中,全自动管线已挂(/tmp/ghidra-pipeline.sh:下载→解压→headless 导入 arm64 薄片→导符号,exit 落盘)。
- **下一步(Ghidra 就绪后)**:①反编译定位 QAccessible 激活门(静态链符号剥离,靠 qt.* 日志类别字符串与 QAccessibleCache 虚表形态 xref);②顺带 strings xref 找内部发送函数(ilink sendmessage/SendMsg)供红线裁决材料。

## 终局注记(2026-10-14 收口:门+路径双定位,研究闭环归档)

**结论:Ghidra 管线全通(中途修复官方包缺失的 mac_arm_64 反编译器——源码构建 exit=0);AX 激活门与发送路径均指令级定位;启用与否属红线裁决,全程零进程干预、零写微信侧数据。**证据档案=`research/ax-gate-hunt.md`。

- **AX 激活门(指令级闭环)**:门=QCocoaAccessibility::notifyAccessibilityUpdate@0x70b32bc,入口 0x70b32dc `ldrb w8,[x0,#0x8]; cbz→return`(m_active@实例+8,与上游 qcocoaaccessibility.mm 的 !isActive() 逐字对应);钥匙=QPlatformAccessibility::setActive@0x6c4ad50(`strb w1,[x0,#0x8]`+尾跳 0x6c45d60 遍历 bridge);唯一天然写0=基类 ctor@0x6c4a76c(strb wzr);激活入口——上游 3 个 QNSView AX 入口中本体只剩 accessibilityAttributeValue:@0x7093f50 一个保有直调激活(0x7093f68-0x7093f7c:instance()→vtable+0xb0 accessibility()→mov w1,#1→bl 0x6c4ad50),accessibilityHitTest:0x7093fe0 与 accessibilityFocusedUIElement 0x709400c 的激活调用被剥且 activateQtAccessibility selector 全串不存在;配套 QAccessibleCache insert@0x6c48e88/deleteInterface@0x6c489fc/虚表@0x9fd2240(typeinfo@0x9fd22e0,基类 QObject),queryAccessibleInterface@0x6c45c98,qt.accessibility.core/cache 类别对象@0xa519b70/0xa519b98;LLDB 开门最小动作=对 vptr==slide+0x9fe7e68 的实例写 `[inst+8]=1`。
- **发送路径(SendMsgFtouser)**:主流程 FUN_031ab38c(3400B,XOR 现场解码,分支 service id 0xa13/0xa18/0xa1d/0xa23/0xa28/0xa2f 走 RPC 桩 FUN_05e1d050——Ghidra 误标 0571d050,上游 0x45a5b18);谓词 FUN_048a9a38(上游 0x45a5ae8/0x4d20688);网络层 functionlist XML@0x986fb9c:newsendmsg reqid=237/sendmsg reqid=2,long-link /cgi-bin/micromsg-bin/ uslong1-8.wechat.com;ilink 家族 ilink_sdk_core.c@0x875cfe0/ilink_helper.cc@0x8a10270;appmsg 路 CoSendAppMsgCgi@0x88a8fb0→FUN_03092230;排除项:sendMessageToWeTypeWithEncodedData:@0x992fd22 属主类=WeTypeStickerService(输入法贴纸桥,非聊天发送,假阳性排除)。地址映射 VA=fat偏移-0xB010000 三重验证成立。
- **差什么(未竟,如实)**:①开门后树是否变深、微信 mmui 窗 accessibleRoot() 是否返回 nil——静态无法回答,需下一步 LLDB 动态实验(主人裁决,本轮零动态操作);②发送路径参数结构未还原;③引用 setActive 的静态表项 0xa5c25be 未追。
