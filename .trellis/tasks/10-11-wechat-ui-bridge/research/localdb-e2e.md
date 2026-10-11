# E 段全链验证记录 — localdb(2026-10-11;E1 真跑负结论 + 全链挂起状态)

> 执行件:数据工-本地库(10-11-wechat-ui-bridge Phase E)。
> **红线 6 纪律**:本文零聊天内容、零密钥材料;证据只留形状(计数/路径名/时长/码值)。
> 结论速览:**E1 零内存密钥途径实测不可行(infeasible),AC7 全链真跑挂起,d4Needed=true**;
> E1 校验机制、E2 副本生命周期、E3 三域查询三件均已落地(合成材料单测全绿),
> 密钥可得(D4 裁决引入)即闭合。

## 1. E1 真跑:零内存途径(key_info.db)不可行

### 1.1 本机执行(A3 探查的自然延伸,本轮闭环)

对 `all_users/login/<wxid>/key_info.db`(明文 SQLite,A3 已证)做「解码 → 候选 → 离线校验」全链:

- BLOB 结构(35 行实测,较 A3 的 34 行 +1,单用户不变):
  protobuf 形状 `{f1: bytes(168), f2: varint=2024(版本常数), f3: varint≈写入时间戳}`;
  `md5(blob) == key_info_md5` 完整性关系成立;`key_md5` 列恒空串。
- 候选族(f1 载荷滑窗 / 整 BLOB 滑窗 / sha256 派生,保序去重):**5,081 个**;
- 校验:对 `db_storage` 全部 20 个加密库 page1 做离线 HMAC-SHA512 校验
  (SQLCipher 4 原始密钥语义,salt⊕0x3A + PBKDF2-SHA512 2 轮 mac_key,纯 stdlib):
  **101,620 次校验,0 命中**,全链 0.66s。
- 首轮探查(未去重全族)亦为 0 命中:20,930 试次/20 库。

组件真跑应答(装机同形,`uv run --no-sync python -m wechat_bridge localdb query filehelper --since 7d --json`):

```json
{"error": {"code": "key_unavailable", "message": "本地库密钥不可得:零内存途径(key_info.db)实测未闭合——行数=35 候选=5081 离线HMAC校验=101620次 命中=0/20库;…", "fix_hint": "D4 待主人裁决:…"}}
```

exit=21;`--probe` 同步如实 `degraded`(`localdb_key=unavailable`;bridge_version 0.2.0)。

### 1.2 公开独立旁证(三方 + 逆向结论,与本机实测全数一致)

| 来源(gh search code 实取证) | 结论 |
|---|---|
| EMANUELALIU/wechat-chat-analysis `references/export-playbook.md`(macOS,lldb 系) | key_info_data=180B protobuf(f1=168B);**试遍 4995 种派生(直接取/滑窗/异或/AES-ECB/CBC 正反)全部 HMAC 失败 → 被机器专属密钥加密,文件内不可推导**;4.1.10+ 密钥只在内存 |
| luvrell/wechat-msg-extract `docs/01-密钥获取实测记录.md`(Windows) | 方差分析 3 变化区间,15,987 候选 × 51 库 HMAC 校验**全部未命中**;`key_info_md5` 只是 `md5(key_info_data)`,`key_md5` 列为空(与本机实测同构) |
| callzhang/ceo-agent-service `docs/wechat-channel-and-local-memory-research.md` | 12,058 个 32B 窗口校验 message_0.db 首页 HMAC **无一命中**;引 wechat-dump-rs 作者 0xlane 逆向:**key_info_data 是登录 key(每次登录变),不是数据库 key**,无法离线还原 |
| vincentkoc/weicrawl `internal/unlock/keys.go` | 常量注记原话:`key_info.db is metadata, not a filled wechat_keys.json manifest; use a reviewed extractor to supply real 64-hex SQLCipher keys`——其密钥方案同样回落内存扫描 |

### 1.3 macOS 4.1.x 现存唯一密钥途径 = 红线外

EMANUELALIU playbook 的「已排除死路」表 + 唯一活路:**lldb 附加 + `CCCryptorCreate` 断点取密钥**
(需对 /Applications/WeChat.app ad-hoc 重签)。两处踩线:

1. **调试器附加微信进程读内存 = prd 红线 3**(禁对微信进程做内存读取);
2. **重签微信 = 改上游 app 本体**,违反链接者架构精神(A3 对 wechat-mcp-macos 的重签路径已同样判定「双踩红线不可借」)。

内存扫描路(参考件 `crypto/keys/scanner_macos.py`)同踩红线 3,且 playbook 实测 4.1.x 已不以
hex 文本存密钥、密钥所在内存区 Mach VM 读不到——**技术上也已失效**。

### 1.4 E1 裁定

- A3 的「零内存可行=true」是**候选物在盘**判断;E1 端到端真跑将其推翻:**不可行(infeasible)**。
- 组件侧如实落地:`localdb.acquire_key` = 完整机制 + 如实 exit 21(消息只含形状计数 + D4 指引);
  校验器 `verify_key_for_page` / 候选提取 / 交叉验证全量可单测(合成材料),
  **D4 若裁决引入外部密钥,同一校验器直接复用,全链一步闭合**。
- 内存搜索 = `wechat_bridge/memsearch.py` **默认关空壳**(无进程 API 引用,守卫测试钉死;
  无配置键,启用唯一途径 = D4 豁免后代码层显式改 `MEMORY_SEARCH_ENABLED`),**绝不真跑**。

## 2. E2/E3 落地形态(密钥可得即用;当前真跑挂起)

### 2.1 依赖(design §5.1)

- sqlcipher 缺失 → `brew install sqlcipher` **已执行并记录**:brew 装 SQLCipher 4.19.0
  (`/opt/homebrew/Cellar/sqlcipher/4.19.0`,2026-10-11);组件缺装时结构化报错 + brew 指引(不静默半装,有单测)。
- 密钥材料零 argv 暴露:解密 SQL(key 在内)走 sqlcipher **stdin**,不落进程 argv。

### 2.2 E2 副本生命周期(G5)

- 落点:`<数据根>/wechat-localdb/decrypted/<域>/<库>`,文件 600 / 目录 700;加密原件先拷私有 staging(db+-wal),解密后 staging 即清。
- TTL 24h(配置 `copy_ttl_hours`)失效重建 + 容量上限(配置 `copy_capacity_mb`,缺省 512MB,超限跳过并如实记录)+ 解密失败触发重建(exit 22)。
- 域目标(G4):message→message_0/biz_message_0、session→session.db、contact→contact.db(代码级映射);
  配置扩展域回落该域目录全量 .db(小库优先,容量兜底)。
- 单测(合成加密库真 sqlcipher roundtrip):解密可读/600 权限/TTL kept+rebuilt/capacity 跳过/no_key 跳过/错 key exit 22/staging 清理,全绿。

### 2.3 E3 三域查询(G4)

- message 域:列签名自适应识别消息表(会话列+时间列+内容列齐备;公开参考形态 `Msg_<hash>` 宽表),
  指定会话最近 N 天消息;文本(localType=1)出 `text`,媒体类落「类型+占位」(prd R1a);
  contact 域解析展示名(remark>nickname>alias);session 域 best-effort 会话列表(缺列如实 null)。
- 域副本缺失 = 该域如实降级(`domains` 状态节),message 域缺失 = exit 22;表结构漂移不拖垮全查(红线 7)。
- 查询载荷 = stdout 契约(私人消费面);不入日志/git;**与真实解密副本的 schema 对账归 D4 闭合后**(当前以 4.x 公开参考形状合成单测)。

## 3. AC7 判定(对照 prd)

| AC7 环节 | 状态 |
|---|---|
| 定位 db_storage | ✅ 真跑(20 库枚举) |
| 密钥获取(D4 途径) | ❌ **零内存途径不可行(E1 真跑实锤);挂起,待 D4** |
| 解密副本落私有区 | 机制就绪(合成真跑);真库解密挂起 |
| 只读查询 N 天文本 | 机制就绪(合成真跑);真库查询挂起 |
| 零出网/零进程交互/证据形状化 | ✅ 全程满足 |

**判定:AC7 未闭合,挂起原因唯一 = 密钥(d4Needed=true)**;D4 裁决选项:
①豁免内存搜索(踩红线 1/3,且 4.1.x 技术上已近失效)——不推荐;
②外部密钥引入(all_keys.json 类,由主人以任意可行手段提供,600 权限私有区)→ 组件校验器即闭合全链——推荐;
③放弃本地库通道,桥以 degraded(key_unavailable)如实长灰——始终可选。

## 4. 测试与门禁

- 组件单测:`uv run --no-sync python -m pytest tests/wechat-bridge -q` → **107 passed, 4 skipped**
  (4 = 3 条 `MYIA_WECHAT_E2E=1` 真机探针门控 + 1 条本轮新增真机 `localdb query` 负结论回归,CI 缺省跳过);
  golden 基件经 `MYIA_WECHAT_BRIDGE_REGEN_GOLDEN=1` 再生成后稳定(键序/措辞变更 4 行,契约对账)。
- `uvx ruff@0.16.10 check plugins/wechat-bridge tests/wechat-bridge` → All checks passed。
- 全量门禁 `uv run --no-sync python -m pytest -q` 结果见提交注记(独立跑)。
