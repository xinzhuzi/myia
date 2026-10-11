# design — 微信桥：UI 自动化 + 本地库只读

> 前置阅读：[prd.md](prd.md)（需求/红线/AC）、[research/wechat-ui-landscape.md](research/wechat-ui-landscape.md)（生态+本机实测）。

## 1. 组件边界

```
~/.myia/plugins/wechat-bridge/ (受管组件,原生运行)    MYIA 本体 (src/myssia + desktop)
┌─────────────────────────────┐          ┌──────────────────────────────┐
│  wechat-bridge (Python)      │          │  push 层: 注册 weixin-local   │
│  ├─ probe() → 三态           │  ←调用──  │       通道 (G7 命名)          │
│  ├─ sessions/list            │  本地子进程 │  ├─ 探针: 子进程 --probe       │
│  ├─ messages/read            │  或 HTTP  │  ├─ store/dedup: 不接(G3)     │
│  ├─ messages/send_text       │          │  └─ UI: 消息屏三态+只读入口    │
│  └─ localdb/query (只读)     │          │  local-db 通道: CLI + sidecar │
└─────────────────────────────┘          │      handler 挂载             │
                                         └──────────────────────────────┘
```

- **桥 = 独立受管组件 `wechat-bridge`**（G7）：Python 实现，走 pyenv_components 组件戳 + 设置下载组件链路（链接者架构红线）；MYIA 只做子进程调用（首选，同机零网络面），不 vendor 任何上游代码。
- **MYIA 侧新增面最小化**：push 层新通道模块 `weixin_local.py`（对齐 `weixin.py` 的桥接形态；`weixin` 通道名保持归官方 Hermes 桥）、sidecar 协议新增 `localdb.query` 类 handler（进 `_HANDLERS`，走 sidecar-protocol 变更纪律）、消息屏微信卡状态接入 + **只读会话入口**（G2）。

## 2. 三通道契约

| 通道 | 接口 | 实现机制 | 降级 |
|---|---|---|---|
| UI 读 | `sessions list` / `messages read <chat> -k` | AX 属性读（会话列表/消息文本）；Chromium 渲染层 AX 空树时 → AXManualAccessibility 激活 → 仍空则截屏+local-ocr 像素链（MYIA 基建复用） | degraded：像素链质量降级如实标注 |
| UI 写 | `send_text <chat> <text>` | AX 定位发送框 → AXConfirm/AXPress；**禁合成鼠标、禁激活窗口**（红线 4）；**桥内硬频控（G6）**：单条、间隔 ≥10s、无批量接口、不可配置 | 失败即失败，不静默重试（重复发送风险） |
| 本地库读 | `localdb query <chat> --since <d>` | 定位 db_storage → 密钥（D4 途径）→ sqlcipher 解密**副本**至数据根私有区 → 只读 SQL（**G4：message/session/contact 三域，域清单配置可扩**） | 密钥不可得 → degraded + D4 升级主人裁决 |

- 三态定义与 push 层现有惯例对齐：`ok / degraded / bridge_unavailable`。
- 三态判据矩阵（probe 探测项 → 态映射）：

| 探测结果 | 态 | 修复指引 |
|---|---|---|
| 组件未安装 / 版本不符 | `bridge_unavailable` | 设置页下载组件 |
| 微信进程未运行 | `bridge_unavailable` | 启动微信客户端 |
| AX 辅助功能权限缺失 | `bridge_unavailable` | 引导系统设置授权 |
| 微信运行但主窗口未开（UI 通道） | `degraded`（localdb 不受影响） | 打开微信窗口 |
| AX 树空/残缺 | `degraded`（像素链兜底启用） | — |
| 本地库密钥不可得 | `degraded`（localdb 不可用） | D4 裁决项 |
| 全部通过 | `ok` | — |

- 探针零成本：进程存在性 + 版本号 + AX 可达性自检，不读消息内容。
- **发送频控的跨进程状态（G6 实现修正）**：桥为一次性子进程，进程退出内存状态即失——频控时间戳**必须落盘** `数据根/wechat-localdb/send_state.json`（上次发送时刻，flock 防并发，非敏感元数据）；每次发送前检查 + 原子更新，间隔不足 10s 直接拒发并返回剩余等待秒数。
- push 层内容版式对齐 `weixin.py` 惯例：TemplateRenderer 在场走模板，缺省内置纯文本版式，长文分块语义随桥（桥侧不预切）。

## 3. 关键设计取舍

1. **子进程 vs 常驻**：首版一次性子进程（对齐 `weixin.py` 桥接 Hermes 的形态，零常驻）；近实时监听（轮询 wal 增量）延后到需求真实出现（产品优先，勿预建）。
2. **解密副本 vs 在线解密**：副本制——解密产物落 `MYIA 数据根/wechat-localdb/`（私有区），微信进程零接触、可缓存可复跑；**生命周期（G5）：TTL 24h 失效重建 + 容量上限**，密钥随登录态轮换导致解密失败即触发重建。副本含敏感内容，进红线 6 管辖（不入 git/日志/外发）。`key_info.db` 活跃写入（10-08 仍变）→ 密钥可能随登录态轮换，副本解密失败 = 重新取密钥的触发信号。
3. **AX vs 像素链**：AX 优先（结构化、零 OCR 误差）；像素链只做 AX 空树时的兜底——微信 4.x Chromium 渲染层 AX 是否开放是 AC1 头号问题，本设计在两态间不预设结论，桥内做能力探测自适应。
4. **Windows 备胎**：协议对齐 = 桥的 CLI/JSON 接口两端一致（macOS AX 实现 ↔ Windows wxautox4 RESTful 实现），MYIA 侧只换桥地址；本档仅落接口对齐文档，不实现。
5. **出站分工**：程序化出站主口 = 现有官方 iLink 桥（`weixin.py`）；UI 写通道仅同机便捷场景（PRD R2 定位），push 层默认路由仍指官方桥。

## 4. 兼容与回滚

- 微信版本探测进探针（4.1.15 基线）；升级后 AX 树/schema 破坏 → degraded + 明确报因，MYIA UI 如实灰态，不崩不假死。
- 组件版本锁（真锁惯例）：桥组件版本 + 适用微信版本范围记录在组件戳。
- 回滚：桥下线 = MYIA 侧 `bridge_unavailable` 灰态（对齐 `weixin.py` 显式可选设计），MYIA 主功能零依赖桥。
- 密钥途径若最终依赖内存搜索（D4 豁免）：单独成模块 + 开关默认关，主人显式开启才生效。

## 5. 执行前置与安全边界

### 5.1 系统依赖（组件安装前置）

- **sqlcipher**：本地库解密依赖 sqlcipher 库（`brew install sqlcipher` + Python 绑定 `sqlcipher3`/`pysqlcipher3` 编译链）。组件安装器须**检测前置并在缺依赖时给出明确指引**，不许静默装到一半失败。
- AX 权限主体：macOS 按 responsible process 归责——桥作为 MYIA 子进程，授权授给 MYIA app 本体即可；**开发期 AI 侧探查走会话宿主授权（已验证在册）**，装机期走设置页引导（F5 验证项）。

### 5.2 消息屏卡面组织（默认方案，UI 稿可翻案）

微信区双卡并排：现有「微信」卡 = 官方 Hermes/iLink 桥（出站主口）；新增「微信本机」卡 = `weixin-local`（UI 收发 + 本地库，三态 + 只读入口）。状态语义独立不混合——两张桥的健康度、降级原因不同，混一张卡会互相污染。

### 5.3 安全边界汇总

- 零出网（本地库通道）；UI 通道仅微信客户端自身流量。
- 解密副本、查询结果 = 私有情报：不入 git、不入日志、不进上下文原文；外发先脱敏（security-baseline）。
- 密钥材料不落明文日志；`all_keys.json` 类产物若产生，存数据根私有区并 600 权限。
- AX 权限：MYIA/桥进程需辅助功能授权，设置页引导一次性授权（装机验证项）。
