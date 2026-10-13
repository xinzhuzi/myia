# 微信 mac wechat.dylib 逆向:UI 栈鉴定与自动化路径

## Goal

主人令(2026-10-13):用 ghidra-reverse 技能研究微信 mac 本体(Resources/wechat.dylib 357MB)。目标:①鉴定自绘 UI 栈(andromeda.framework/libEGL/GLES 线索→Skia?自研?);②找 UI 引擎内部无障碍/渲染开关的 Mac 对应物(若有,LLDB 可开);③定位内部发送消息函数路径(字符串 xref:ilink sendmessage/SendMsg)为红线裁决供材料。Ghidra 需重装(12.x,GitHub 直下)

## Requirements

- TBD

## Acceptance Criteria

- [ ] TBD

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
