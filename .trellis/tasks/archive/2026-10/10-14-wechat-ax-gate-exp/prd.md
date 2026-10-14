# 微信 AX 无障碍门 LLDB 实开实验

## Goal

按已归档逆向档(`archive/2026-10/10-13-wechat-dylib-reverse/research/ax-gate-hunt.md`)的指令级闭环(门 0x70b32bc/钥匙 0x6c4ad50)LLDB 实开验证,AX 树前后对比取证;收工清理可再生逆向工件(~4.9G)

## Requirements

- 微信在跑时方可实验(未跑则 blocked 如实,不开微信抢焦点);attach 快进快出秒级,detach 干净。
- 门/钥匙指令在体逐字节核验后方可写入;slide 需模块表与 vmmap 双源互锁。
- 验证 = AXAPI 只读读树(osascript System Events 递归计数,前后对比),不 activate 窗口不抢焦点。
- 写入仅限 1 字节数据写(m_active),零函数调用;终态保持发现时原状(门开)。
- 证据 + 可复现命令落 `research/exp-receipt.md`。
- 收工清理可再生逆向工件;fisher 系 /tmp 件与世事.app.bak-* 勿动。

## Acceptance Criteria

- [x] 微信在跑确认(PID 33748,4.1.15,与档同版本同二进制)——`ps`/`pgrep`/`defaults` 证据在回执 §0
- [x] attach 前基线 AX 树:1 窗口 / 6 节点(12:26:31)
- [x] 门指令在体逐字节吻合:slide+0x70b32dc = `08204039`(ldrb w8,[x0,#8])
- [x] 钥匙指令在体逐字节吻合:slide+0x6c4ad50 = `01200039`(strb w1,[x0,#8])
- [x] 实例唯一命中:vptr=slide+0x9fe7e68 扫 265MB MALLOC 区域恰 1 处(0x7434093b0)
- [x] AX 树前后对比取证:基线 6 节点 → 门开稳态 6 节点(**无显著膨胀**——如实记,见结论)
- [x] 因果对照实验:关灯(写 0)→ AX 查询 → 自复亮(读 1)= 激活路径在体活跃实证
- [x] detach 干净退出,三次会话进程健在无重启无崩溃(终检 PID 33748)
- [x] 可再生逆向工件清理(清单见 Notes)
- [x] 第二轮复跑(微信又换主 3 次后新 PID 93675,13:00-13:14):门/钥匙字节、虚表槽三重锁(vptr+0x10→0x70b32bc)、堆内唯一实例、关灯→AX 查询→自复亮因果对照全部独立复现——回执 §8
- [x] 第二轮树对比:基线 15 → 门开 6(节点数随 UI 状态波动,两态皆窗级截断,无内容级膨胀)
- [x] 换主崩因排查:3 次换主(12:52/12:56/13:05)crashpad 库零 dmp → 非崩溃,且均早于本轮首次写入
- [x] 清理核验:7 项可再生工件 `ls` 确认不存在(第一轮已删,无再生成)

## 结论(详证据见 research/exp-receipt.md)

门/钥匙/实例全部在体坐实,但 **m_active 在 AX 查询下被微信自置 1**(0x7093f50 保留激活路径活跃),门开时树恒 6 节点——**树浅瓶颈在供给侧(accessibleRoot 疑 nil),不在门**。档 §5 开放问题"开门后树是否变深"动态关闭:不变深。后续若要树深,方向为 Qt 侧 accessibleRoot/接口注册或系统侧另途。

第二轮复跑(PID 93675)在新进程上独立复现上述全部结论,并加验虚表槽第三重身份锁;树节点数实测随 UI 状态波动(15↔6)但两态皆窗级截断——供给侧截断结论坐实。

## Notes

- 实验初期微信自行重启换主(15460→33748,12:17:46);此前我方仅只读操作,首次 attach 即 no such process,非实验所致。
- AppleScript 雷区:System Events 术语(`UI elements`)在顶层 handler 裸用编译报 -2741,handler 体内须自带 tell 块。
- 本版 LLDB `SBProcess` 无 `GetNumMemoryRegions`,区域表改由 vmmap 快照文本解析。
- 清理清单(可再生逆向工件,已删,du 实测 5.0G 与指令估 ~4.9G 吻合):`/tmp/wxrev`(1.7G)`/tmp/f7_verify`(2.1G)`/tmp/wxkey-ghidra`(726M)`/tmp/wxkey-fatarm64.dylib`(165M)`/tmp/wxkey-fatarm64-check.dylib`(165M)`/tmp/wxsend-verify`(98M)`/tmp/wxsend-e2e`(29M);`~/ghidra-wxhunt` 不在指令清单内未删(逆向工程留盘复用);fisher 系与世事.app.bak-* 未触碰。
- 本实验工件(可复现证据,留):`/tmp/axcount.applescript` `/tmp/wxgate_exp.py` `/tmp/wxgate_off.py` `/tmp/wxgate_read.py` `/tmp/wxvmmap.txt` `/tmp/wxgate_log.txt` `/tmp/ax_before.txt` `/tmp/ax_mid.txt` `/tmp/ax_after.txt` `/tmp/ax_shape.txt`。
- 第二轮复跑工件(留,`*2` 后缀不覆写一轮):`/tmp/cgwin2.py` `/tmp/cgwin2.out` `/tmp/wxvmmap2.txt` `/tmp/wxgate_exp2.py` `/tmp/wxgate_off2.py` `/tmp/wxgate_read2.py` `/tmp/wxgate_log2.txt` `/tmp/wxgate_log2b.txt` `/tmp/wxgate_log2c.txt` `/tmp/ax_before2.txt` `/tmp/ax_after2.txt` `/tmp/ax_mid2.txt` `/tmp/ax_final2.txt`。坑补记:LLDB 取 __TEXT 段须 `FindSection('__TEXT')`(`GetSectionAtIndex(0).FindSubSection` 找的是段内子节);JXA 枚举 CGWindowList 会段错误,交叉核实走 ctypes(`/tmp/cgwin2.py`)。
