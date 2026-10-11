# 微信 UI 自动化生态调研（2026-10-11）

> 本文是 10-11-wechat-ui-bridge 的调研底稿。多路搜索（skills.sh 注册表 / GitHub 仓库搜索×4 形状 / 中文网络搜索×2 / 代码搜索）+ 本机实测。

## 1. 生态地图（按方向）

### 1.1 界面自动化 — Windows（成熟）

| 仓库 | 星级 | 许可证 | 活跃 | 机制/备注 |
|---|---|---|---|---|
| cluic/wxauto | 7357★ | Apache-2.0 | 2026-04 | 鼻祖级，Windows UIAutomation，微信 3.x，收发+监听 |
| fanyuantaier/wechatauto-replica | 407★ | Apache-2.0 | **2026-10-10** | wxauto 复刻，微信 4.x |
| scottfly189/WeChatAuto.SDK | 274★ | MIT | **2026-10-10** | 定位「为 Agent/Harness 提供操作微信能力的 RPA SDK 底座」 |
| LAVARONG/wechat-automation-api | 182★ | — | 2026-09 | Flask+uiautomation 包装 HTTP API，4.0+ |

### 1.2 界面自动化 — macOS（薄弱）

| 仓库 | 星级 | 许可证 | 活跃 | 机制/备注 |
|---|---|---|---|---|
| PatrickHua/wxauto-mac | 5★ | MIT | 2025-06（陈旧） | AX+AppleScript，标称支持 3.9.11+，pip 装；**对 4.1.15 兼容性未知（AC1 实测项）** |
| dragonking-T/wechat-controller | 2★ | 无证 | 2026-04 | AX+键鼠模拟+可选 Claude Vision；免责声明明确封号风险 |
| gh search "wechat macos accessibility" | — | — | — | 0 命中（第 5 种搜索形状，证实生态薄） |

**排除**：thisnick/agent-wechat（170★ 活跃）= WeChat 跑 Docker 容器 + ptrace —— 撞禁 Docker 铁律，且 ptrace 属内存操作。

### 1.3 本地数据库方向（合规重灾区）

2025-10 微信官方函件潮，三大项目删库：
- sjzar/chatlog（9187★）——README 仅剩删库声明（2025-10-20）
- xaoyaoo/PyWxDump（9651★）——删库；活 fork：alanhzw/PyWxDump 99★、bbgouzi123/wx-dump-plus 107★
- Thearas/wechat-db-decrypt-macos（626★）——README 仅剩「遵纪守法，先溜了」

仍活跃：git-jiadong/wechatDataBackup（6420★，Apache-2.0，2026-01）——聊天记录备份导出 GUI。LC044/WeChatMsg（42093★）无许可证停更，仅指针参考。
**风险定性**：删库潮 = 腾讯对工具作者分发行为的合规维权，不是封用户账号；本地只读自己设备数据账号侧零风险，风险面在工具合规层。本档红线仍排除内存密钥提取。

### 1.4 官方零风险通道（互补线）

- 企业微信自建应用：MYIA **W2 已实装**；个人微信关注企业「微信插件」后应用消息落个人微信（Server酱同款机制）。
- apprise 引擎（MYIA 已落地）本机 venv 实测在册五通道：`wechat://`（企微）、`wecombot://`（企微群机器人）、`serverchan://`、`pushplus://`、`wxpusher://`——全官方 API。
- 公众平台测试号：官方沙箱，可作补充。
- 硬边界：给「别人的个人微信」程序化发消息，官方只有企微外部联系人一条路；个人微信之间无官方自动化接口。

### 1.5 技能生态

skills.sh 全是公众号文章类（发布/排版/提取）；无聊天自动化技能。op7418/Claude-to-IM-skill（2888★ MIT）等是 bot API 桥，不在本方向。

## 2. 本机实测证据（2026-10-11）

| 探测 | 命令 | 结果 |
|---|---|---|
| 微信版本 | defaults read Info.plist | **4.1.15** |
| 运行状态 | pgrep -x WeChat | RUNNING |
| 进程族 | System Events 进程枚举 | WeChat + **WeChatAppEx + 5×WeChatAppEx Helper (Renderer)** → Chromium 内核多进程，聊天界面疑似 Web 渲染 |
| AX 窗口 | System Events count windows | **0** |
| CG 窗口 | CGWindowListCopyWindowInfo(OptionAll) | **0 窗口** → 微信在托盘后台态、主窗口未开，AX 零暴露目前是「没开窗」的正常表现，**不是** AX 被屏蔽的结论 |
| AX 权限基线 | System Events 读 Dock/Finder UI elements | 正常 → 本会话宿主已有辅助功能权限，执行段探查免授权 |
| Windows 真机 | ssh zbj@192.168.0.101 tasklist+if exist | **微信未装**（无进程、两个默认路径不存在） |

**执行段首个动作预判**：微信 4.x 的 Chromium 渲染层默认关闭 AX，开窗后 AX 树可能仍为空/残缺，需测 AXManualAccessibility 激活（CEF/Chromium 惯例）或退化为像素链（screencapture + local-ocr 三级链，MYIA 基建现成）。开窗动作涉及前台性，须主人知情下进行。

## 3. UI 自动化的风险机理（主人三条约束的校准结论）

1. **系统层指纹**：Windows `SendInput` 带 LLKHF_INJECTED 标志；macOS AX 动作非输入事件、来源可辨——客户端**有能力**感知非人操作（无证据表明微信逐项启用，但不保证）。
2. **服务端行为风控**：节奏恒定/深夜连续/无人类噪声，与驱动方式无关。
3. **ToS 字面禁止**，执行裁量权在腾讯；打击波次主打协议号/hook，UI 生态「尚未被打」≠「被豁免」。
4. **后果不对称**：主力号封禁不可逆（支付/社交图谱）。只有官方 API 能给「保证不封」。
5. **收敛路径**：专用小号 + 低频拟人可将风险收敛到可承受（改题设为「牺牲可弃账号」；新号实名+风控更敏感是代价）。

## 4. 与官方通道的关系

本桥（UI 自动化）解决官方通道覆盖不到的两块：**读聊天内容**（官方无任何接口）与**个人微信间程序化发送**（官方仅企微外部联系人路）。推送类需求（情报→主人）应优先走已实装的 W2 企微 + apprise 官方通道，零风险；UI 桥用于读 + 必要的个人微信出站。

## 5. 检索方法备注

负向结论均满足 ≥3 搜索形状（仓库搜索×4 形状 + 中文网络×2 + 代码搜索 + 补充 accessibility 搜索）；GitHub 取证走 gh api（zread 超时一次，回落可用）。

## 6. 本地库只读通道（2026-10-11 主人追加方向,同日实测）

### 6.1 本机数据布局（只读探查,内容未读）

- 数据根：`~/Library/Containers/com.tencent.xinWeChat/Data/Documents/xwechat_files/`
- 当前账号目录：`wxid_oc2yhey1xkpw22_8253/`（wxid + 设备后缀命名）
- `db_storage/` 十四域：MMKV, bizchat, chatbot, contact(+contact_fts 全文索引), emoticon, favorite(+fts), general, hardlink, head_image, **message**, **session**, sns, solitaire, third_app_icon
- message 域形态：`biz_message_0.db` + `.db-wal/-shm` + `.db-first/-last/-incremental.material`（增量物料件）+ `.kvdb`；另有主消息分片库（探查被 head 截断,执行段盘点全量）
- **`all_users/login/<wxid>/key_info.db`**（24KB,10-08 仍活跃写入）——名字直指密钥信息,D4「零内存密钥」头号探查对象

### 6.2 钥匙串核查

`security dump-keychain` 元数据级过滤无微信密钥条目（仅 acct=xinzhuzi / GLM_WEIXIN 等疑似主人自存杂项;按凭据红线未深挖）。**macOS 微信 4.x 的 SQLCipher 密钥大概率不在钥匙串**——chatlog 时代 macOS 路径是搜进程内存,4.x 是否给了 key_info.db 这类落盘新途径 = AC7/D4 的核心探查题。

### 6.3 参考实现（指针,均为外部件按链接者架构处理）

- git-jiadong/wechatDataBackup（6420★,Apache-2.0,活）：Win/Mac 聊天记录导出,macOS 密钥机制可参考其文档/源码思路
- alanhzw/PyWxDump（99★,PyWxDump 删库后活 fork）：Windows 内存搜密钥路数,仅作机制参考
- 删库三项目（chatlog/PyWxDump/wechat-db-decrypt-macos）原理解读类二手文章仍可考（sarv.blog 等）

### 6.4 与 UI 通道的分工

| | UI 通道 | 本地库只读 |
|---|---|---|
| 实时性 | 高（当下收发） | 无（落盘滞后,可轮询 wal 增量近似实时） |
| 深度 | 仅已加载消息 | **全量历史 + fts 全文检索** |
| 账号风险 | ToS 灰区 | **零**（不碰网络不碰进程） |
| 前台扰动 | 需 AX 约束（红线 4） | 零 |
| 主要短板 | AX 树不确定（Chromium） | 密钥途径不确定（D4） |

两通道故障域独立,互为备份:AX 树残缺时本地库兜底读;UI 写通道无风险替代,出站仍归 W2 企微官方通道优先。
