# AX 门 LLDB 实开实验回执(2026-10-14)

按档 `.trellis/tasks/archive/2026-10/10-13-wechat-dylib-reverse/research/ax-gate-hunt.md` 的指令级闭环(门 0x70b32bc/钥匙 0x6c4ad50),对在跑微信做 LLDB 实开验证 + AX 树前后对比。

## 0. 环境与前置校验

| 项 | 值 | 证据 |
|---|---|---|
| 微信版本 | 4.1.15(与档一致,dylib 落盘 10-12 18:37 早于 10-13 逆向会话,地址未漂移) | `defaults read /Applications/WeChat.app/Contents/Info.plist CFBundleShortVersionString` → `4.1.15`;`ls -la .../wechat.dylib` → `Oct 12 18:37` |
| 实验进程 | PID 33748(12:17:46 起) | `pgrep -x WeChat` → `33748`;`ps -p 33748 -o lstart` → `Wed Oct 14 12:17:46 2026` |
| slide | `0x135234000` | `vmmap 33748 | grep wechat.dylib` → `__TEXT 135234000-13ed68000`;段长 `0x13ed68000-0x135234000=0x9B34000` 恰为档记 `__DATA_CONST` vmaddr,`__DATA` 基差 `0x9FEC000` 同吻合——映射互锁 |
| slide 双源核验 | LLDB 模块表 vs vmmap 快照一致,attach 时二次确认 | lldb 输出 `MODULE ... __TEXT load=0x135234000 file=0x0 -> slide=0x135234000` + `SLIDE_OK` |

注:实验初期微信自行重启换主(15460→33748,12:17:46)。此前我方仅做过只读操作(ps/vmmap/读档),首次 lldb 对 15460 attach 即报 `no such process`(未停过旧进程、零写入),重启非本实验所致。

## 1. 指令级在体验证(attach 内只读)

slide + 档记 VA,逐字节读回与档比对:

| 角色 | 档记 | 运行期地址 | 在体字节 | 判定 |
|---|---|---|---|---|
| 门:读 m_active | 0x70b32dc `ldrb w8,[x0,#0x8]` | 0x13c2e72dc | `08204039` | ✅ 逐字节吻合 |
| 钥匙:写 m_active | 0x6c4ad50 `strb w1,[x0,#0x8]` | 0x13be7ed50 | `01200039` | ✅ = `0x39000000|(8<<10)|1` 精确编码 |

## 2. 实例定位(堆扫)

- 模式:8 字节 vptr 值 = `slide+0x9fe7e68` = `0x13f21be68`(QCocoaAccessibility 虚表+8,档 §2.2)。
- 扫描域:vmmap 快照全部 MALLOC 区域(126 个),实扫 265,453,568 字节。
- **命中恰 1 处:`0x7434093b0`(MALLOC_SMALL)**——全进程单实例坐实,亦反向验证地址映射与 vptr 值双重正确。

## 3. 实验主线与 AX 树前后对比

| 时刻 | 动作 | 结果 |
|---|---|---|
| 12:26:31 | 基线数树(attach 前,只读) | **1 窗口 / 6 节点** |
| 12:29:50-56 | lldb 会话①:验门+验钥匙+堆扫,预备写钥匙 | 发现 `m_active already=01`——**门已是开的**,写钥匙为 no-op |
| 12:33:17-24 | lldb 会话②:主动写 `m_active 01→00`(关灯) | 回读 `00` ✅ |
| 12:36:21 | osascript 数树(=AX 查询刺激) | 1 窗口 / 6 节点(不变) |
| 12:36:28 | lldb 会话③(只读回看) | **`m_active=01`——AX 查询让微信自把门重新打开** |
| 12:38:20 | 终态数树(门开稳态) | **1 窗口 / 6 节点**(窗"微信"+3×AXButton+深层 2) |

AX 计数命令(`osascript /tmp/axcount.applescript`,System Events 只读递归,不 activate 不抢焦点):
```applescript
on axCount(e)
	tell application "System Events"
		set c to 1
		try
			set kids to UI elements of e
			repeat with k in kids
				set c to c + (my axCount(k))
			end repeat
		end try
	end tell
	return c
end axCount

tell application "System Events"
	set p to first process whose name is "WeChat"
	set winCount to number of windows of p
	set total to 0
	repeat with w in windows of p
		set total to total + (my axCount(w))
	end repeat
	return (winCount as text) & " / " & (total as text)
end tell
```
(AppleScript 雷区:handler 顶层裸用 `UI elements` 等 System Events 术语会编译报 -2741"预期是行的结尾"——handler 体内必须自带 `tell application "System Events"`。)

## 4. 结论

1. **门/钥匙指令与实例全部在体坐实**(字节级):档记闭环 0x70b32bc/0x6c4ad50/+8 偏移/vptr 0x9fe7e68 无一漂移。
2. **门不是树浅的瓶颈**:`m_active` 在 AX 查询下会被微信自己置 1(档 §2.3 记载的保留激活路径 `accessibilityAttributeValue:@0x7093f50 → setActive(true)@0x6c4ad50` 在体活跃——关灯→查询→自复亮已证);门开状态下树恒 6 节点。
3. **树浅瓶颈在供给侧**:与档 §2.4 预判一致——mmui 自绘窗的 `accessibleRoot()` 疑返 nil,树止步窗级。档 §5 的开放问题"开门后树是否变深"就此动态关闭:**不变深**。
4. 推论:想让 AX 树变深,方向应是树供给侧(Qt 侧 accessibleRoot/接口注册),不是门;或绕开 Qt 走系统侧注入(另立项裁决)。

## 5. 红线遵守

- 只做 1 字节数据写(`m_active`),**零函数调用**(未 call setActive,虽等效)。
- 全程未 activate 微信窗口、未抢焦点(osascript System Events 只读;无 `open`)。
- attach 均快进快出(4-7 秒/次,detach 干净,进程健在无重启无崩溃:三次会话后仍 PID 33748)。
- m_active 终态 = 01 = 发现时原状(门开)。

## 6. 可复现命令

```bash
# 基线/终态计数
osascript /tmp/axcount.applescript
# slide
vmmap $(pgrep -x WeChat) | grep -E "__TEXT.*wechat.dylib"
# vmmap 快照(脚本输入)
vmmap $(pgrep -x WeChat) > /tmp/wxvmmap.txt
# LLDB 三连(会话①②③脚本:/tmp/wxgate_exp.py /tmp/wxgate_off.py /tmp/wxgate_read.py)
xcrun lldb --batch -p $(pgrep -x WeChat) -o 'script exec(open("/tmp/wxgate_exp.py").read())' -o 'detach'
# 树形明细
osascript -e 'tell application "System Events" to tell process "WeChat" to get {name of window 1, role of every UI element of window 1}'
```

原始日志:`/tmp/wxgate_log.txt`(会话①完整输出)、`/tmp/ax_before.txt`/`/tmp/ax_mid.txt`/`/tmp/ax_after.txt`。

## 7. 收工清理

已按指令清理可再生逆向工件(fisher 系与世事.app.bak-* 未触碰;`~/ghidra-wxhunt` 不在清单内未删——档记逆向工程留盘复用):见 prd.md notes 清单。

## 8. 第二轮复跑(PID 93675,13:00-13:14,独立复现验证)

第一轮证据进程 33748 已不在(微信其后又换主两次:82338@12:52 → 85046@12:56:05 → 93675@~13:05)。**换主 3 次零 crashpad 落盘**(`…/app_data/crashinfo/{pending,completed,new}` 全空,12:00 后无任何 .dmp)——非崩溃,疑主人手重开或微信自重拉;且 3 次换主全部早于本轮首次写入(13:07:41),与本轮实验无关。13:16:50 另见瞬时同名进程 15408 与主进程并存、数秒内自退(单实例锁行为)——微信自带重拉/自愈机制的旁证。故在新进程上全流程复跑,构成对第一轮的独立复现。

### 8.1 本轮新增的第三重身份锁

会话① 在门/钥匙字节验证之外加验**虚表槽**:`*(vptr+0x10) == slide+0x70b32bc`(notifyAccessibilityUpdate 槽位)——`VTCHK vptr=0x13ae63e68 slot=0x137f2f2bc expect=0x137f2f2bc match=True`。slide 新值 `0x130e7c000`(LLDB 模块表与 vmmap 双源一致,`/tmp/wxgate_log2.txt`)。

### 8.2 实验主线(PID 93675)

| 时刻 | 动作 | 结果 |
|---|---|---|
| 13:00:01 | 首次数树(进程 85046) | **0 窗 / 0 节点**(主窗关闭态;`open -g` 后仍 0/0) |
| 13:03-13:05 | CGWindowList 交叉核实(ctypes 直调 CoreGraphics,`/tmp/cgwin2.py`) | 窗口服务器层 10 窗(含 700×640 内容窗与 1 个在屏 1920×1050 全屏窗),AX 却报 0 窗——**AX 供给迟到**(新进程启动初期);JXA 枚举会段错误,勿走 |
| 13:06:11 | 正式基线(进程已换 93675) | **1 窗 / 15 节点**(窗「微信」,顶层 AXGroup+2×AXButton) |
| 13:07:38-43 | lldb 会话①(attach 5 秒) | slide 双源锁定;门 `08204039`/钥匙 `01200039` 逐字节吻合;虚表槽吻合;扫 184,385,536 字节 96 个 MALLOC 区**唯一命中 `0x8c4c1ced0`(MALLOC_SMALL)**;`m_active` 写前已 01(基线 AX 查询已自开);写 01 → 回读 01;detach 干净 |
| 13:08:42 | 门开态数树 | **1 窗 / 6 节点**(顶层 3×AXButton) |
| 13:11:11-16 | (脚本缺段查找回退,FATAL 于写入前,零写入;修复后重跑) | — |
| 13:13:13-19 | lldb 会话②:主动关灯 | `m_active 01 → 00` 回读 00 ✅ |
| 13:13:19 | 关灯态 AX 查询 | 1 窗 / 6 节点(不变) |
| 13:13:19-25 | lldb 会话③:只读回看 | **`m_active=01`——AX 查询令微信自复亮**(保留激活路径在体活跃,独立复现 §4.2) |
| 13:13:53 | 终态数树 | **1 窗 / 6 节点**;PID 93675 健在,终态门开=发现时原状 |

### 8.3 第二轮结论

1. **第一轮全部核心结论在新进程独立复现**:门/钥匙指令零漂移(新 slide 下仍逐字节吻合)、堆内单实例、AX 查询自开激活路径活跃、门开态树恒窗级浅树。
2. **树节点数随 UI 状态波动(基线 15 → 门开 6),但两态都是窗级截断**(个位数按钮层,永无内容级子树)——「供给侧截断」结论更为坐实:门与树深无关,波动源是微信窗自身内容变化。
3. 新观测(如实记,未深究):新进程启动初期 AX 窗供给迟到(CG 有窗而 AX 报 0),稳定后恢复;对本实验无影响(基线取于稳定后)。

### 8.4 第二轮可复现命令

```bash
PID=$(pgrep -x WeChat)
osascript /tmp/axcount.applescript                                  # 计数(前后/中途)
vmmap $PID > /tmp/wxvmmap2.txt                                      # 区域快照(脚本输入)
xcrun lldb --batch -p $PID -o 'script exec(open("/tmp/wxgate_exp2.py").read())' -o 'detach'   # 验门+验钥匙+堆扫+写钥匙
xcrun lldb --batch -p $PID -o 'script exec(open("/tmp/wxgate_off2.py").read())' -o 'detach'   # 关灯(因果对照)
xcrun lldb --batch -p $PID -o 'script exec(open("/tmp/wxgate_read2.py").read())' -o 'detach'  # 只读回看
/usr/bin/python3 /tmp/cgwin2.py $PID                                # CGWindowList 交叉核实
```

第二轮工件(留证):`/tmp/axcount.applescript`(沿用第一轮)/`/tmp/cgwin2.py` `/tmp/cgwin2.out` `/tmp/wxvmmap2.txt` `/tmp/wxgate_exp2.py` `/tmp/wxgate_off2.py` `/tmp/wxgate_read2.py` `/tmp/wxgate_log2.txt`(会话①完整输出)/`/tmp/wxgate_log2b.txt`(会话②)/`/tmp/wxgate_log2c.txt`(会话③)/`/tmp/ax_before2.txt` `/tmp/ax_after2.txt` `/tmp/ax_mid2.txt` `/tmp/ax_final2.txt`。

脚本坑补记:LLDB Python `module.GetSectionAtIndex(0).FindSubSection('__TEXT')` 取的是段内子节(无效),段本体须 `m.FindSection('__TEXT')` 回退——会话②首跑因此 FATAL(发生在任何写入之前,零副作用)。

## 9. 第二轮收工清理核验

`ls -lad /tmp/wxrev /tmp/f7_verify /tmp/wxkey-ghidra /tmp/wxkey-fatarm64.dylib /tmp/wxkey-fatarm64-check.dylib /tmp/wxsend-verify /tmp/wxsend-e2e` → 全部 `No such file or directory`(13:00 核验,第一轮已删,本轮无再生成)。fisher 系与世事.app.bak-* 未触碰;`~/ghidra-wxhunt` 不在指令清单内未删。
