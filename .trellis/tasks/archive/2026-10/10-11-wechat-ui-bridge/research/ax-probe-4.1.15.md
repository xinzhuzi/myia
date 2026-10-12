# A1 开窗 AX 探查 — 微信 4.1.15 macOS(2026-10-11)

> 任务:10-11-wechat-ui-bridge Phase A1(implement.md 操作手册六步照跑)。
> 红线遵守:全程零激活调用、零合成点击、零前台抢夺;对微信只做 AX 属性读 + 两个激活开关的 set 尝试(均被拒,见 §4);**消息文本/会话标题零导出**——本文全部证据只含 role/计数/属性名/错误码/路径形状。
> 可复跑脚本:[ax-probe-script.py](ax-probe-script.py)(复跑指南见 §8;AX 函数需独立 venv,见 §8 铁律 6 说明)。

## 0. 结论速览(AC1 三问直答)

| AC1 问题 | 答案 |
|---|---|
| 能读到什么 | app 元数据(AXTitle len=2 / AXHidden=False / AXFrontmost=False)、**菜单栏系统全树**(7 个菜单栏项、全部菜单项)、窗口 chrome(**仅 3 个 traffic-light 按钮**)、AXMainWindow/AXFocusedWindow 引用本身。**读不到:会话列表(0 cell/0 row)、消息文本(0 AXStaticText)、聊天输入框(0)、发送按钮(0)** |
| 需要什么激活 | **无解**。Chromium 惯例两开关全被拒:pid 85172 与 85178 上 `AXManualAccessibility` set → `-25205 AttributeUnsupported`;`AXEnhancedUserInterface` set → `-25208 NotImplemented`(注意:后者在属性名清单里被**通告**却不可 set,半实现状态) |
| 写通道是否需焦点 | **比焦点问题更糟:AX 写通道整体不可达,与焦点无关**。输入框与发送按钮不在任何进程任何窗口态的 AX 树里(唯一带 AXConfirm 的是系统注入的帮助菜单搜索框,§5.3)。**AC4 冲突裁决预设被触发,且是加强版**——不是「发送必须持焦」而是「AX 发送通道不存在」,AC3 按 prd 预设不得强行达成,降级两案(i 半自动 / ii 显式妥协)提主人裁决时建议追加第三案:(iii) 写通道降级为官方 iLink 桥(`weixin.py`)独任,UI 写判 exit 13/15 |

## 1. 前置检查(手册第 1 步)与窗口态时间线

**执行起点窗口态**:CGWindowList 全量(OptionAll)总 232 窗,微信族 29 窗(主窗形制 1920×1050@layer0 pid 85172 在册)——**非 0 窗**,不触发「0 窗终止」条款;但 29 窗 `kCGWindowIsOnscreen` 全 False(ordered-off 残影态),`pgrep -x WeChat` = RUNNING(pid 85172)。

**探查期间窗口态摇摆**(三次采样 + 交叉核对,这可能影响复跑者的读数):

| 时刻(2026-10-11) | CG OnScreenOnly 微信族 | System Events `count of windows` | pyobjc `AXWindows` | 备注 |
|---|---|---|---|---|
| 探查前段 | 0 | 0 | 0 (len=0) | 全 offscreen,主窗在 server 有名但未 ordered-on |
| 中段(一次) | — | **2**(`微信` + `图片和视频`) | **1** | 主窗+媒体查看器瞬时 ordered-on(主人侧使用痕迹;本探查零激活调用)。**就在这次在场态采样里,树仍只有 chrome(§3)** |
| 探查后段(收口时) | **0** | 0(name 列表空) | 0;`AXMainWindow` 引用仍在 | ordered-out 恢复 |

> 归因注记:窗口态摇摆与主人侧真实使用(媒体查看器窗出现)时间吻合;本探查对微信的全部写操作只有两个激活开关 set 且都收到错误码(-25205/-25208),无任何可致开窗的调用。

## 2. 粗探(手册第 2 步,osascript System Events)

```
osascript -e 'tell application "System Events" to tell process "WeChat" to get count of windows'
→ 0(起点)/ 2(中段,window names = ["图片和视频","微信"])/ 0(收口)

osascript -e '...tell process "WeChat"
  return "windows=" & (count of windows) & " menuBars=" & (count of menu bars) & " menuBar1_items=" & (count of menu bar items of menu bar 1)'
→ windows=0 menuBars=2 menuBar1_items=7

权限基线:count UI elements of menu bar 1 of process "Finder" → 8(会话宿主辅助功能权限在,与 prd Notes 记载一致)
```

## 3. 深探(手册第 3 步,pyobjc AXUIElementCopyAttributeValue)

### 3.1 进程族(ps 实况)

主进程 `WeChat` pid 85172;`WeChatAppEx`(Chromium 宿主)pid 85178;6×`WeChatAppEx Helper (Renderer)`(13576/22668/75708/85215/85216/85217);GPU/Network Helper、WeChatHelper×2、XPlayer、crashpad、Sparkle。**聊天内容 = AppEx Chromium 渲染**的判断与 prd Notes 一致,且 CG 全量列表中 700×640@ (610,235) 同界窗口**同时**挂在 85172 与 85178 两名下(宿主层窗口)。

### 3.2 pid 85172(主进程)role 计数(三态采样,形状一致)

| 采样 | 节点 | 深度 | role_counts |
|---|---|---|---|
| 中段(主窗 ordered-on 最佳态) | 211 | 5 | AXWindow×4† AXButton×12† AXGroup×4 AXMenuBar×2 AXMenuBarItem×8 AXMenu×12 **AXMenuItem×166** AXTextField×1† AXTable×1† AXColumn×1† |
| 收口态 | 204 | 5 | 同上形状(AXWindow×2 AXButton×6,菜单项 167) |
| Finder 对照(同脚本) | 428 | 5 | AXImage×51(桌面图标)AXRadioButton×8+RadioGroup、ScrollArea×2、菜单系 333 项、TextField×1† Table×1† |

† 见 §5 归属判定:TextField/Table/Column/一半 Button 全部是**系统菜单机制注入件**,非微信内容。

### 3.3 主窗树轮廓(中段在场态原文,仅 role/子计数/动作名)

```
ROOT AXMainWindow
  AXWindow[children=3]
    AXButton[children=-25212(NoValue)] actions=[AXPress]          ← traffic-light
    AXButton[children=1] actions=[AXPress, AXZoomWindow, AXShowMenu]  ← 缩放钮
      AXGroup[children=1]
        AXGroup[children=0]
    AXButton[children=-25212(NoValue)] actions=[AXPress]          ← traffic-light
ROOT AXFocusedWindow  (同一窗口的第二引用,轮廓相同)
```

**1920×1050 的完整 UI 主窗,AX 树内容 = 3 个窗口控制钮,零业务内容叶子。** 内容区(侧栏/会话列表/聊天区/输入框)在 AX 里完全不存在——AppEx Chromium 渲染面没有向任何进程暴露 AX。

### 3.4 pid 85178(AppEx 宿主)

AXWindows 恒 len=0(三采样);AXMainWindow 收口时 `-25212 NoValue`;全树仅菜单系 168 节点(AXMenuBar×1 + 6 菜单栏项 + 151 菜单项)。它的 CG 窗口(700×640)对 AX 零暴露。

### 3.5 遍历错误码(微信 AX 服务半实现的直接证据)

- `AXChildren` get → `-25212 kAXErrorNoValue` ×6~10 处(traffic-light 按钮等;子树属性在但值永不加载)
- `AXChildren` get → `-25205 kAXErrorAttributeUnsupported` ×1(AXTextField 上)
- 同脚本对 Finder:children 错误仅 -25212/-25200 各 1 且能下钻至深度 5 原生内容 → **走查器能力已验证,微信树空不是脚本缺陷**(对照组证据)

## 4. 空树/激活分支(手册第 4 步)

对两个 pid 都做了 `--force-activation`(不等空树):

| set 目标 | pid 85172 | pid 85178 |
|---|---|---|
| `AXManualAccessibility = true` | `-25205 AttributeUnsupported` | `-25205 AttributeUnsupported` |
| `AXEnhancedUserInterface = true` | `-25208 NotImplemented` | `-25208 NotImplemented` |

- app 级 `AXAttributeNames` 清单(85172)**通告了** `AXEnhancedUserInterface` 却 set 失败;`AXManualAccessibility` 连清单都不在 → **Chromium AX 激活惯例在微信 4.1.15 上整体不存在,无激活路径**。
- set 后等 1.5s 重遍历:节点数零变化(203→203 / 168→168)。

**像素链预研结论(手册第 4 步要求记档)**:AX 激活无解 → UI 读唯一兜底 = screencapture(`-l <windowID>`,不激活不抢焦)+ local-ocr 三级链(MYIA 基建现成)。本次收口时 0 个 onscreen 窗,未执行截屏采样;像素链可行性验证归 Phase C3,前置条件 = 窗口在场(主人知情)。

## 5. 三类目标节点定位(手册第 5 步)

### 5.1 会话列表 cell(含未读 badge 属性名)

**未找到。** 全树 0×AXCell / 0×AXRow / 0×AXListItem(三态采样一致)。唯一的 AXTable(children=1 → AXColumn[-25212 NoValue],无任何 AXRow)位于菜单系路径内 = **系统帮助菜单搜索结果表**(macOS 向帮助菜单自动注入),非会话列表。未读 badge 属性名:无从谈起(宿主节点不存在)。

### 5.2 消息区文本形态

**未找到。** 全树 0×AXStaticText。对照:同脚本 Finder 桌面窗能走回 51×AXImage 原生内容。微信聊天文本(Chromium 渲染)对 AX 零暴露。

### 5.3 输入框 + 发送按钮(AXConfirm 可用性)

**未找到(两者)。** 全树唯一 AXTextField 路径 `AXChildren[0]/6/0/0/0`(菜单系内),属性形状 `AXSearchButton + AXClearButton + AXPlaceholderValue + AXSelectedTextRange...`、动作 `[AXShowMenu, AXConfirm]` = **macOS 帮助菜单系统搜索框**(系统注入件,`AXChildren[0]` 即 AXMenuBar、第 7 个菜单栏项 = 帮助菜单)。全树 0×AXButton 除 traffic-light/缩放钮外;**AXConfirm 只出现在上述系统搜索框上,聊天输入框与发送按钮不在 AX 树中,AXConfirm 写通道无从谈起**。

## 6. 对桥设计(design §6 错误码表)的修订含义(建议,裁决归主人/后续 Phase)

1. exit 13 `ax_tree_empty` 在 4.1.15 上**恒真**(不是「偶发空树」而是「内容层永不暴露」)→ probe 探测矩阵「AX 树空/残缺 → degraded(像素链兜底)」应升级为 4.1.15 的**缺省预期态**。
2. exit 15 `send_ax_focus_required` 语义与实测不符:写通道不是「需焦点」而是「不可达」→ 建议码名改 `send_ax_unreachable`(或保留码位改语义),AC3 触发 AC4 降级裁决,两案外加第 (iii) 案(§0)。
3. 版本脆弱性(红线 7)落点:AppEx AX 行为是微信版本函数,组件戳记录「4.1.15 = AX 内容层关闭」基线;每次微信升级后 `--probe` 需重测 §4 两开关 + §5 三类节点(脚本已可复跑)。
4. A2(wxauto-mac 冒烟)预判:其 AX 路数与本次探查同源,对 4.1.15 大概率「不可用」——仍按 G8 限 30 分钟实测收口。

## 7. 探查动作清单(可审计)

- 被执行:CGWindowList 三种 option 采样 ×3 轮、System Events count/name 采样 ×4、pyobjc AX 属性读(AXAttributeNames/AXWindows/AXMainWindow/AXFocusedWindow/AXMenuBar/AXTitle/AXHidden/AXFrontmost/AXChildren/AXRole/AXActionNames/按钮与输入框取值属性)、AXManualAccessibility/AXEnhancedUserInterface set ×2 pid ×2 开关、Finder 对照全走查。
- 未被执行(红线):窗口激活/raise、鼠标键盘合成、AX 动作 perform(含对系统搜索框 AXConfirm 的试触发)、微信进程内存/注入、任何消息文本与会话标题的记录。

## 8. 复跑指南

```bash
# 1) AX 函数在 pyobjc-framework-ApplicationServices,仓库 .venv 未含且铁律 6 禁装 → 独立 venv:
uv venv /tmp/axprobe-venv --python 3.12
VIRTUAL_ENV=/tmp/axprobe-venv uv pip install pyobjc-framework-ApplicationServices pyobjc-framework-Cocoa

# 2) 确认微信窗口在场(CG OnScreenOnly 微信族 > 0 时树里才有窗口可走;ordered-off 态仅菜单系):
/Users/zhengbingjin/Project/Github/MYIA/.venv/bin/python - <<'EOF'
import Quartz
wl = Quartz.CGWindowListCopyWindowInfo(Quartz.kCGWindowListOptionOnScreenOnly, Quartz.kCGNullWindowID)
print([w.get('kCGWindowName') for w in wl if (w.get('kCGWindowOwnerName') or '') in ('微信', 'WeChat')])
EOF

# 3) 探查(零激活,可对多 pid):
/tmp/axprobe-venv/bin/python .trellis/tasks/10-11-wechat-ui-bridge/research/ax-probe-script.py \
  --pid $(pgrep -x WeChat | head -1) --pid $(pgrep -x WeChatAppEx | head -1) \
  [--force-activation] [--json /tmp/ax-probe-run.json]
```

脚本红线内建:取值类属性(AXTitle/AXValue/AXDescription/AXPlaceholderValue)只记类型+长度;文本零落盘。
