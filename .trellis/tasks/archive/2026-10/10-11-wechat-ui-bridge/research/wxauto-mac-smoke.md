# A2 — wxauto-mac 快速冒烟(G8:限 30 分钟,2026-10-11 实跑)

> 对象:PatrickHua/wxauto-mac(5★,MIT,末次 push 2025-06-17,标称支持微信 3.9.11+)对本机微信 **4.1.15** 的核心读路径。
> 前置状态:微信运行中、**主窗口未开(托盘态,AX 窗口数 0)**;铁律禁止为此开窗——凡因窗口未开的失败**计入结论**。

## 结论:三值 = **unusable**(对 MYIA 用途不可用)

按贡献度排序的依据:

1. **核心读路径在唯一可达状态下失败(实测)**:`WeChat()` init 在 `_find_main_window` 处 10 轮重试后抛 `ElementNotFoundError: 无法找到微信主窗口`(托盘态 0 窗口,失败计入结论)。读类 API(GetSessionList/GetAllFriends/GetChatHistory)全部依赖 init 产出的 `main_window`,级联不可达。
2. **设计上与 MYIA 红线冲突(源码级,与窗口状态无关)**:
   - init **无条件激活微信**(`wxauto_mac.py:111` `self.app.activate()`;实现在 `uiautomation.py:163`)——违反静默铁律「不激活任何 app 窗口」,本次冒烟必须打桩拦下才能合规运行(桩拦截记录见下,activate 确被调用 1 次)。
   - 写通道走 **AppleScript 键盘合成**(`wxauto_mac.py:860-878` `_send_message_applescript` → System Events keystrokes)——同类合成输入,超出红线 4「只走 AX 通道」边界。
3. **包装已坏**:**PyPI 无此包**(`pip install wxauto-mac` 404,README 安装指引失效),只能 GitHub 源装;且**运行时依赖漏声明**(`utils.py:14` `from PIL import Image`,但 METADATA 的 Requires-Dist 仅 pyobjc 三件)——装完即 import 失败,需手工补 Pillow。
4. **陈旧 + 结构错位风险**:末次更新 2025-06(微信 3.9.x 时代),窗口匹配靠标题含 "WeChat"(`wxauto_mac.py:137`);本机 4.1.15 为 WeChatAppEx + 5×Chromium Renderer 的 Web 渲染架构(research/wechat-ui-landscape.md §2),其通用 AX role 选择器对 4.x 树的适配性存疑。
5. **残余未知(如实注记)**:开窗状态下其 AX 选择器能否命中 4.1.15 树**未测**(本档禁止开窗);此未知不影响结论——即便可修,依据 2/3/4 也不作为受管组件候选。G8 决议(借力重心转 BiboyQG/WeChat-MCP)维持。

## 实录(命令原文与输出)

```bash
# 1) 独立临时 venv(未触碰仓库 .venv)
uv venv /tmp/wxauto-mac-smoke            # CPython 3.12.11

# 2) PyPI 装包失败
uv pip install --python /tmp/wxauto-mac-smoke/bin/python wxauto-mac
#   × No solution found: wxauto-mac was not found in the package registry
# 交叉验证:pypi.org/pypi/{wxauto-mac,wxauto_mac,wxauto-mac-py,wxauto4mac}/json → 全 404

# 3) 改 GitHub 源装(偏差:与 README 的 PyPI 指引不同,如实记录)
uv pip install --python /tmp/wxauto-mac-smoke/bin/python \
  "wxauto-mac @ git+https://github.com/PatrickHua/wxauto-mac.git"
#   + wxauto-mac==1.0.0 (from git+...@9afb0550df29955fe477476ee34ebe8edd56d7ea) + pyobjc 系

# 4) import 失败 → 补漏声明依赖
/tmp/wxauto-mac-smoke/bin/python -c "import wxauto_mac"
#   ModuleNotFoundError: No module named 'PIL'   (wxauto_mac/utils.py:14)
uv pip install --python /tmp/wxauto-mac-smoke/bin/python pillow   # + pillow==12.3.0

# 5) 冒烟脚本(activate 打桩,其余原样):/tmp/wxauto-mac-smoke/smoke.py
```

冒烟输出(前后 frontmost 取证:均为 ZCode,**静默铁律零违例**):

```json
{
  "activate_stub_calls": ["activate"],      ← 库 init 确实试图激活微信,被桩拦下
  "wechat_running": true,
  "wechat_version": "4.1.15",               ← 版本探测路径正常
  "find_application": true,
  "ax_window_count": 0,                      ← 托盘态,与 prd Notes 一致
  "init": "ElementNotFoundError: 无法找到微信主窗口"
}
```

GetSessionList/CurrentChat 未执行:构造函数已抛错,`main_window` 不存在,级联不可达(冒烟脚本对两 API 的 try 分支未触达)。

## 源码证据(安装副本:/tmp/wxauto-mac-smoke/lib/python3.12/site-packages/wxauto_mac/)

| 位置 | 事实 |
|---|---|
| `wxauto_mac.py:111` | init 无条件 `self.app.activate()`(静默铁律冲突,本次打桩) |
| `wxauto_mac.py:130-142` | `_find_main_window` 标题含 "WeChat" 匹配,10×0.5s 重试后抛 ElementNotFoundError |
| `wxauto_mac.py:860-878` | 发送走 `osascript` System Events keystrokes(合成键盘输入) |
| `uiautomation.py:163` | `activate()` 实现(NSRunningApplication activate) |
| `utils.py:14` | `from PIL import Image`,Pillow 未在 Requires-Dist(METADATA 核实仅 pyobjc 三件) |

## 与 implement.md 的对账

- 本冒烟 → AC1 后半(wxauto-mac 对 4.1.15 兼容性三值:**unusable**)+ D2 输入(自研 AX vs 借力 BiboyQG;wxauto-mac 不构成第三选项)。
- 30 分钟纪律:全程(venv→装→冒烟→源码核)在时限内完成,未超支。
