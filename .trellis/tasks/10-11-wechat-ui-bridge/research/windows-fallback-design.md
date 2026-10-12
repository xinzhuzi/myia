# Windows 备胎线设计占位（G1/AC6，不实现）

> 10-11-wechat-ui-bridge Phase G 交付物。按 prd R3/AC6：**本档只落设计占位与启用判据，不实现**；实现待 macOS 线触发 G9 判据后另启子任务。

## 1. 为什么留备胎（G9 启用硬判据，2026-10-12 复核后修订）

macOS 线现状：像素链读已真跑通过（pixel-chain-e2e.md），写通道已归官方 iLink 桥独任——**读线是备胎唯一保的价值**。启用判据（满足其一）：

- macOS 像素链因微信升级连续两周 degraded/不可用（OCR 布局漂移救不回）；
- 微信 macOS 版本破坏截窗能力（TCC/合成帧行为变化）；
- 主人明示要 Windows 侧读取能力。

**反向注记（2026-10-12）**：本地库只读通道（E 段）与 UI 无关且已就位（差 D4 密钥），历史读取不受 UI 面故障影响——备胎的保险价值进一步收窄到「实时读」一角。启用前先算这笔账。

## 2. 协议对齐（桥 CLI 契约 ↔ wxautox4 RESTful 映射）

MYIA 侧只换桥地址（`wechat_bridge_bin` 指向远端适配器），契约不变：

| wechat-bridge CLI | wxautox4 RESTful 对应 | 适配注记 |
|---|---|---|
| `--probe` → 三态+checks | `GET /v1/wechat/status` | wxautox4 无 degraded 语义，适配器按「窗口在场性/登录态」自判映射 |
| `sessions list --json` | `GET /v1/wechat/chats`（列会话） | 字段名映射 name/unread；N 截断在适配器 |
| `messages read <id> -k` | `GET /v1/wechat/messages?chat=<id>` | wxautox4 是真 API 可指定会话（优于 macOS 像素链的「当前打开会话」限制） |
| `send_text` | `POST /v1/wechat/send` | **不建议启用**：macOS 线已归官方 iLink 独任（AC3 第三案），Windows 备胎同样不出站；适配器可拒不实现（exit 15 语义透传） |
| `localdb query` | 无对应 | 本地库在 macOS 数据根，与 Windows 线无关 |

鉴权：wxauto-skill 形态 = Bearer Token（服务端 config.yaml auth.token）；适配器配置面沿用桥组件 config.json，新增 `remote_url/remote_token` 两键（G7 命名纪律，直白）。

## 3. 栈选型（届时复核）

- 首选：cluic/wxauto 本体（7357★ Apache-2.0）+ wxautox4 RESTful 服务（作者官方技能件同款架构，与 MYIA 设想零差）；
- 4.x 兼容性注意：wxauto 主线支持 3.x，4.x 用 fanyuantaier/wechatauto-replica（407★ Apache-2.0）或 WeChatAuto.SDK（274★ MIT，Agent 底座定位）——届时按微信 Windows 版实测选。
- Windows 真机在档：zbj@192.168.0.101（win-machine-facts 记忆），**当前未装微信**（2026-10-11 实测），启用前置=装机+登录（挂小号，G1 决议同源）。

## 4. 启动另立子任务的输入清单

- 本档（协议映射/判据/选型）；
- research/wechat-ui-landscape.md §1.1（Windows 生态全景）；
- macOS 线故障证据（触发判据时的 degraded 记录）。
