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
| **BiboyQG/WeChat-MCP** | **275★** | MIT | 2026-03 | **macOS AX + 屏幕截图自动化微信,pip 装 `wechat-mcp-server`;读任意会话/自动回复/发文字朋友圈/加好友/5 个 Claude 子代理;需终端辅助功能权限;macOS UI 线最强现成参考件（深度查找轮补获,首轮仓库搜索漏检）** |
| PatrickHua/wxauto-mac | 5★ | MIT | 2025-06（陈旧） | AX+AppleScript，标称支持 3.9.11+，pip 装；**对 4.1.15 兼容性未知（AC1 实测项）** |
| dragonking-T/wechat-controller | 2★ | 无证 | 2026-04 | AX+键鼠模拟+可选 Claude Vision；免责声明明确封号风险 |
| gh search "wechat macos accessibility" | — | — | — | 0 命中（后续 MCP 形状补获 BiboyQG,证明单形状负向结论不可靠） |

**排除**：thisnick/agent-wechat（170★ 活跃）= WeChat 跑 Docker 容器 + ptrace —— 撞禁 Docker 铁律，且 ptrace 属内存操作；JettChenT/wechat-mcp（47★）= 需**改装版微信客户端**（wechat-exporter 改装教程）+ 仅 3.x —— 改上游红线外。

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

### 1.5 技能生态（find-skills 深度轮,2026-10-11 补）

> 主人纠偏后按 find-skills 完整方法论重查:注册表多关键词 × `gh search code --filename SKILL.md` 多词 × MCP 仓库形状 × 策展目录。首轮单查 "wechat" 的「无聊天自动化技能」结论**作废**。

**技能/能力件形态命中**:
- **cluic/wxauto-skill**（wxauto 官方作者出品）:走 **wxautox4 RESTful API**（作者商业版,闭源收费;免费开源版为 wxauto 本体）;服务跑 Windows + 远程 HTTP + Bearer Token——**Windows 备胎线的现成技能件,连「远程服务+token」架构都与 MYIA 设想一致**
- cacr92/wereply@wechat-automation（444 installs）:微信自动回复,仓库 7★,小体量
- steelan9199/wechat-publisher@pyautogui-automation（670 installs）:pyautogui 路数,偏公众号
- leeguooooo/wechat-use（169 installs）:待深查,低优先

**MCP server 形态命中**（上轮完全漏掉的形状）:
- **yancongya/wechat-mcp-macos**（6★,2026-08 活跃）:**macOS 本地库解密只读参考件**——解密本地 db,聊天记录/搜索/语音转文字/群总结,「零 API 调用纯本地,不修改原始数据库」,contact.db 解出 6000+ 通讯录;密钥途径待读源码定论（AC7 输入）
- **1335907208/wechat-mcp-server**（7★,2026-04）:Windows 本地库只读（进程内存提取密钥→all_keys.json）,只读原则无发送,近实时=轮询会话库
- BiboyQG/WeChat-MCP（275★）:见 §1.2,macOS UI 线
- bkmashiro/weixin-mcp（14★,2026-10-08 极新,MIT,npm）:**官方 ClawBot API 封装**,见 §4
- LupinLin1/wechatlog-mcp-server（40★,MIT,2025-09 停更）:chatlog 系聊天媒体文件下载,指针保留
- lw396/wechat-mcp（19★）:基于 WeChatFerry = **hook 注入,红线外,排除**

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

## 4. 官方 ClawBot 通道（2026-10-11 深度查找轮重大发现）

**腾讯 2026-03-22 正式发布微信 ClawBot 官方插件**:通过 **iLink 协议**开放个人微信 Bot API（接入域名 ilinkai.weixin.qq.com）,启用路径「我-设置-插件」,支持对接 OpenClaw 等 AI 智能体;企业微信侧亦开放智能机器人接入教程（work.weixin.qq.com/index/openclaw）。多来源交叉（知乎手册/CSDN 解析/腾讯云社区/新浪财经,2026-03-22~30）。

**收束性结论**:MYIA `src/myssia/push/weixin.py` 现有出站 = 桥接本机 Hermes → **iLink Bot API —— 正是这条 2026-03 开放的官方合法通道**,只是当时档期（10-03）它尚无「官方开放」的公开名分。据此:

- **出站（写通道）合规位已站住**:官方 iLink/ClawBot 覆盖,UI 自动化的「写」价值降级为同机便捷补充;
- **读通道才是真缺口**:官方 iLink 是 bot 视角（须对端先与 bot 交互）,读「自己账号的会话与聊天记录」官方无接口——UI AX（当下）+ 本地库只读（历史）正是补这块;
- bkmashiro/weixin-mcp = ClawBot 的 MCP 封装（扫码创建 bot,发文本/图片/文件/视频,收消息 webhook）,可作 MYIA 之外独立验证官方通道的对照件。

## 5. 与官方通道的关系（收束后修订）

本桥两通道解决官方体系覆盖不到的核心:**读自己账号的会话与聊天内容**（官方 iLink/ClawBot 是 bot 视角,须对端先与 bot 交互;企微/公众号各有限制;官方不存在「读个人聊天记录」接口）与**个人微信身份的低摩擦同机收发**。推送类需求（情报→主人）优先走已实装的 W2 企微 + apprise 官方通道,零风险;程序化出站归官方 iLink 通道（MYIA 已桥接）;UI 写通道定位为同机便捷补充。

## 6. 检索方法备注

第一轮（浅查）负向结论被主人纠偏后推翻,补深度轮:注册表多关键词×2、SKILL.md 代码搜索×3 词、MCP 仓库形状、中文网络×3——**共 10+ 形状**;教训:单关键词的「生态没有」结论不可靠,MCP 形状首轮完全漏检。GitHub 取证走 gh api（zread 超时一次，回落可用）。

## 7. 本地库只读通道（2026-10-11 主人追加方向,同日实测）

### 7.1 本机数据布局（只读探查,内容未读）

- 数据根：`~/Library/Containers/com.tencent.xinWeChat/Data/Documents/xwechat_files/`
- 当前账号目录：`wxid_oc2y***[脱敏]_8253/`（wxid + 设备后缀命名）
- `db_storage/` 十四域：MMKV, bizchat, chatbot, contact(+contact_fts 全文索引), emoticon, favorite(+fts), general, hardlink, head_image, **message**, **session**, sns, solitaire, third_app_icon
- message 域形态：`biz_message_0.db` + `.db-wal/-shm` + `.db-first/-last/-incremental.material`（增量物料件）+ `.kvdb`；另有主消息分片库（探查被 head 截断,执行段盘点全量）
- **`all_users/login/<wxid>/key_info.db`**（24KB,10-08 仍活跃写入）——名字直指密钥信息,D4「零内存密钥」头号探查对象

### 7.2 钥匙串核查

`security dump-keychain` 元数据级过滤无微信密钥条目（仅 acct=xinzhuzi / GLM_WEIXIN 等疑似主人自存杂项;按凭据红线未深挖）。**macOS 微信 4.x 的 SQLCipher 密钥大概率不在钥匙串**——chatlog 时代 macOS 路径是搜进程内存,4.x 是否给了 key_info.db 这类落盘新途径 = AC7/D4 的核心探查题。

### 7.3 参考实现（指针,均为外部件按链接者架构处理）

- git-jiadong/wechatDataBackup（6420★,Apache-2.0,活）：Win/Mac 聊天记录导出,macOS 密钥机制可参考其文档/源码思路
- alanhzw/PyWxDump（99★,PyWxDump 删库后活 fork）：Windows 内存搜密钥路数,仅作机制参考
- 删库三项目（chatlog/PyWxDump/wechat-db-decrypt-macos）原理解读类二手文章仍可考（sarv.blog 等）

### 7.4 与 UI 通道的分工

| | UI 通道 | 本地库只读 |
|---|---|---|
| 实时性 | 高（当下收发） | 无（落盘滞后,可轮询 wal 增量近似实时） |
| 深度 | 仅已加载消息 | **全量历史 + fts 全文检索** |
| 账号风险 | ToS 灰区 | **零**（不碰网络不碰进程） |
| 前台扰动 | 需 AX 约束（红线 4） | 零 |
| 主要短板 | AX 树不确定（Chromium） | 密钥途径不确定（D4） |

两通道故障域独立,互为备份:AX 树残缺时本地库兜底读;UI 写通道无风险替代,出站仍归 W2 企微官方通道优先。
