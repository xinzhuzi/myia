# implement — 微信桥：UI 自动化 + 本地库只读

> 执行顺序 = 依赖序；每 Phase 独立成 commit（回滚点）。探查类动作的静默约束见 prd 红线 4。

## Phase A 探查与裁决（先于一切实现）

- [ ] A1 开窗 AX 探查（**须主人知情，微信开窗状态**）：AX 树能力清单——会话列表/消息文本/发送框可达性；Chromium 空树时测 AXManualAccessibility 激活；原始证据落 research/ax-probe-4.1.15.md。→ AC1 前半
- [ ] A2 wxauto-mac 快速冒烟（**G8：限 30 分钟**）：对 4.1.15 跑核心读路径，可用/部分/不可用三值结论即收；借力研读重心转 **BiboyQG/WeChat-MCP**（275★）机制。→ AC1 后半 + D2 输入
- [ ] A3 密钥途径探查（**不依赖开窗，可先行**）：key_info.db 结构只读分析（schema/表/列形状，不导内容）；yancongya/wechat-mcp-macos 源码读密钥获取段；结论 = 零内存方案可行性 + D4 裁决请求。
- [ ] A4 裁决记录：D2（自研/借力 BiboyQG 机制）+ D4（密钥途径）回写 prd 开放决策段；**D1 已决（G1：主力号开发+小号并行注册）——联调挂主力号、操作对象限文件传输助手，小号注册并行推进**。

**验证**：research 下两份探查记录有原始证据；A4 有主人裁决标记。

## Phase B 桥组件骨架

- [ ] B1 组件目录（**组件名 `wechat-bridge`，G7**）+ 组件戳 + `--probe` 三态探针（对齐 weixin.py 桥接形态：子进程、JSON 应答、超时 kill 兜底）
- [ ] B2 CLI 骨架：`sessions/messages/send_text/localdb` 四子命令空实现 + `--json` 机器可读
- [ ] B3 组件下载/注册链路接设置页（受管组件惯例）

**验证**：probe 在无微信开窗时如实报 `bridge_unavailable/degraded`，不装可用。

## Phase C UI 读通道

- [ ] C1 会话列表读取（名称+未读数）
- [ ] C2 指定会话最近 K 条文本消息（媒体类落类型占位）
- [ ] C3 AX 空树 → 像素链兜底（截屏 + local-ocr 三级链，复用基建）

**验证**：真实会话读回文本与客户端显示一致；零前台扰动取证（前后前台进程/窗口列表对照）。→ AC2 + AC4 前半

## Phase D UI 写通道

- [ ] D1 向「文件传输助手」发文本（AX 动作，禁合成鼠标；**桥内频控落地（G6）：单条、≥10s 硬间隔、无批量接口、不可配置**）
- [ ] D2 回执验证（读回消息列表比对）+ 失败不重试语义

**验证**：真实发送一条 + 回执核对 + 静默取证。→ AC3 + AC4 后半

## Phase E 本地库只读通道

- [ ] E1 密钥模块（途径按 A4 裁决；内存搜索若豁免则独立模块+默认关）
- [ ] E2 解密副本至数据根私有区（600 权限，红线 6 全套；**生命周期（G5）：TTL 24h + 容量上限，解密失败触发重建**）
- [ ] E3 `localdb query`：指定会话最近 N 天文本消息（**G4：message/session/contact 三域**，域清单配置化）

**验证**：全链零出网（可加网络断言）；查询结果不入日志；形状级证据（库/表/行数）。→ AC7

## Phase F MYIA 装配

- [ ] F1 push 层 `weixin_local.py` 通道注册（**通道 id `weixin-local`，G7**；三态 + 显式可选语义，对齐 weixin.py；`weixin` 通道名保持归官方 Hermes 桥）
- [ ] F2 sidecar 协议 handler（`_HANDLERS` + 协议测试对账，sidecar-protocol 纪律）
- [ ] F3 消息屏微信卡状态接入三态 + AX 权限引导卡
- [ ] F4 消息屏**只读会话入口**（G2：选会话 → 拉最近消息展示；读回消息不入 store/dedup，G3）
- [ ] F5 门禁全绿（pytest 全量 + vitest + tauri build）+ 装机包刷新换装 + 装机件像素级验证（交付判例）

## Phase G 备胎占位

- [ ] G1 Windows 线接口对齐文档（桥 CLI/JSON 契约 ↔ wxautox4 RESTful 映射 + 启用判据）。→ AC6

## 收尾

- [ ] spec 更新（sidecar-protocol / push 通道清单 / security-baseline 若有增补）
- [ ] research 证据文件脱敏复查（红线 6）
- [ ] archive 流程

## 回滚点

每 Phase 一个 commit；B–F 任一故障不影响 MYIA 主功能（桥=显式可选，降级灰态）；E 的副本与密钥产物清除即可完全回退。
