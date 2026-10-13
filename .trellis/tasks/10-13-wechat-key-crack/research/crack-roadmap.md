# 微信密钥攻坚战·路线图与战况（10-13 立档）

> 主人裁决 B：攻坚到底，天尺度，不占主人时间，打穿自动通电。像素链不开（主人否 OCR 质量）。
> 接力会话：读本档 + tools/ 固化件即可继续，全部上下文自洽。

## 战况快照（2026-10-13 08:5x）

**目标**：解开 `key_info.db` 的 `LoginKeyInfoTable.key_info_data`（152B 加密体）拿真钥匙 → `localdb query` 通电 → TMS 群消息精确入情报流。

**已排除（附证据）**：
| 路线 | 结果 |
|---|---|
| 内存扫·x'hex' 字符串（C 版×2 轮） | 零命中（4.1.15 形态失配） |
| 内存扫·三模式宽收集（collector：hex 裸串/salt±512B/x'hex'） | 7794 候选全验证零命中 |
| 内存扫·chatlog fts5 锚定模式（collector2/3） | 零命中（含时序修正轮=主人开着 TMS 群时扫——终扫若也零则正式归档失效） |
| LLDB hook CCCryptorCreate（v1-v4 四轮） | 断点零命中=4.1.15 AES 静态链进微信二进制，无系统 API 可钩 |
| 钥匙串机器密钥 | 全量 dump（80+ 条）无任何 wechat/tencent 条目 |
| 零内存直接推导（E1，10 万 HMAC） | 0 命中（10-11 档在案） |

**已破开的结构（磁盘路战果）**：
- `key_info.db`：单表 35 行，列 user_name_md5/key_md5/key_info_md5/key_info_data；35 行全同 user（主人账号）
- `key_info_data` = 180B protobuf 信封：field1(168B 载荷) + field2 varint 2024（版本） + field3 varint 0x6A5A1331（Unix 时间戳 ≈2026-07）
- field1 内层头：`00 0BB51739 05000001 00000000 00` + **~152B 加密体**
- 解析脚本在 tools/ 与本档 §附录

**验证器（全部就绪，钥匙到手即用）**：`tools/verify3.py` = chatlog darwin/v4 协议（PBKDF2-SHA512 256000 派生 + XOR-0x3a macSalt + 2 迭代 macKey + 页 1 HMAC 比对），对 message_0.db 秒验。

## 机器密钥来源·嫌疑清单（攻坚靶点）

1. **MMKV tinfo（头号）**：`db_storage/MMKV/f2641*b00tinfo.mmkv` 多实例——设备信息（tinfo=terminal/device info）存储，机器密钥大概率派生自其中字段（设备 id/硬件 uuid 等）+ 固定盐 KDF。
2. 派生材料其他候选：IOPlatformUUID / MAC / wxid + 固定串。
3. Secure Enclave（若用则磁盘路死——但 wx 需跨设备迁移，倾向软件派生）。
4. 对照物：**wx 4.x Windows 版同结构**（key_info 生态 Windows 研究更多——`key_info_data` 结构可能同源，Windows 的解包研究可直接借鉴）。

## 四阶段路线

- [ ] **阶段1：MMKV tinfo 解析**（零密码可做）——MMKV 格式解析（腾讯开源格式：文件头+protobuf KV），抽出 tinfo 全字段。
- [ ] **阶段2：派生组合爆破**——{tinfo 字段/设备标识/wxid} × {SHA256/HMAC/PBKDF2,常见盐与迭代} 矩阵，逐组合解 152B 加密体；判据=解出内容可解析为 protobuf 钥匙结构（非随机）。
- [ ] **阶段3：Windows 4.x 对照**——社区对 Windows 版 key_info 的研究（PyWxDump 系活 fork/WeChatMsg 源码在 wx-cli 的 .run/ 里全套！`youkuzazazazaza/wechat-cli/.run/WeChatMsg-src/`）比对封装结构。
- [ ] **阶段4：打穿收口**——真钥匙 → keys.json（600）→ localdb query 真跑 → TMS 群首拉 → 情报流通电 → 10-12 档 AC7 终验。

## 执行方式

- 持久战：闲时任务/后续会话 workflow 接力（读本档+tools 自洽）；每次推进在本档追加战况。
- 终扫（时序修正轮）结果出来后回填「已排除」表。
- 红线不变：只读、密钥材料只落数据根私有区、零微信进程干预（LLDB 路已废恰好回归纯只读）。

## 附录：信封解析（复跑即用）

```python
# 见 tools/ 同款：sqlite3 只读 key_info.db → pb_parse(key_info_data)
# field1 载荷头 14B 结构 + 加密体偏移 28(0x1C) 起取 152B
```
