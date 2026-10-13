# 微信密钥攻坚战·路线图与战况（10-13 立档）

> 主人裁决 B：攻坚到底，天尺度，不占主人时间，打穿自动通电。像素链不开（主人否 OCR 质量）。
> 接力会话：读本档 + tools/ 固化件即可继续，全部上下文自洽。

## 战况快照（2026-10-13 09:3x 第二回填）

**目标**：微信 4.1.15 macOS 数据库钥匙（`key_info.db` 信封,或内存 passphrase）→ `localdb query` 通电 → TMS 群消息精确入情报流。

**模型换血（社区多方实证,解释我方全部零命中根因）**：微信 4.1+ 不再把派生后的 32B raw key 驻留内存,只留一个 **32B 账号级 passphrase**（在可读写堆,无字节特征）;每库真钥匙开库时现算 `enc_key=PBKDF2-HMAC-SHA512(passphrase, salt_i, 256000, 32)`。⇒ x'hex'/裸串/锚定类内容扫描零命中不是形态失配,是**目标物不在可扫形态**;阶段1.5 四模式(S1/S1h/V1/C1)+A1 锚邻域的目标=**passphrase 的堆容器**,仍成立。

**已排除（附证据）**：
| 路线 | 结果 |
|---|---|
| 内存扫·x'hex' 字符串（C 版×2 轮） | 零命中（根因=4.1+ 无 raw key 驻留,见模型换血） |
| 内存扫·三模式宽收集（collector：hex 裸串/salt±512B/x'hex'） | 7794 候选全验证零命中（同上根因） |
| 内存扫·chatlog fts5 锚定模式（collector2/3） | 零命中（含时序修正轮=主人开着 TMS 群时扫——正式失效） |
| LLDB hook CCCryptorCreate（v1-v4 四轮） | ~~断点零命中=4.1.15 AES 静态链~~ **结论已修正（10-13 阶段3）**：钩错层+缺触发——正确符号=系统导出 `CCKeyDerivationPBKDF`（PBKDF2 派生入口）,且需 `preload-symbols false`+账号重登录触发;attach 已登录进程被动等待永不命中。此路线**移出已排除**,转 GATE（见下） |
| 钥匙串机器密钥 | 全量 dump（80+ 条）无任何 wechat/tencent 条目 |
| Windows 指针跳转法移植（collector4,存根模式 tailA/B） | 7.8GB 扫完 deref tried=0——Windows CRT 堆元数据模式在 macOS nano allocator 不存在;思路已按 macOS 堆重绘=collector5 四模式 |
| 零内存直接推导（E1，10 万 HMAC） | 0 命中（10-11 档在案） |
| **key_info_data 离线派生（阶段2,10-13 判死）** | **本地证据判死**：36 行逐字节方差分析与 Windows 4.1.13 模板（luvrell 219 行实测）**逐区间完美同构**——[0,17) 常量17B=17/17、[17,31) 变化14B=1/14 常量、**[31,67) 常量36B=36/36**、[67,171) 变化104B=0/104、[171,175) 常量4B=4/4、[175,179) 变化4B=0/4、[179,180) 常量1B=1/1;其中 [35,67)=32B 跨行常量,对应 EMANUELALIU 判定的「32B 跨库常量,不是密钥」（4995 派生全灭）。⇒ 180B=固定模板+随机字段的**登录凭证记录**,非整体密文;Windows 侧四组独立穷举（decrypt-wxdb AES×5/SM4/DPAPI/XOR/ChaCha20/GCM/CCM、luvrell 15987 窗×51 库、EMANUELALIU 4995 派生、callzhang 12058 窗）全灭+0xlane 判语「登录 key,机器绑定,离线不可还原」。工具=tools/variance_keyinfo.py |

**⭐ GATE·待主人裁决（5 分钟路径 vs 零干预红线）**：LLLD 路=`sudo lldb` attach 微信 → `breakpoint set -n CCKeyDerivationPBKDF -c '$x2 == 32'`（先 `settings set target.preload-symbols false`）→ 断点命令读 x1 32B → 主人微信内退出登录重扫码（触发全库重派生）→ passphrase 到手 → verify3.py 派生验真。蓝本=TANGandXUE/wcdb-key-tool wcdb_key_tool_macos.py（真机 18/18,脚本 /tmp/wcdb_key_tool_macos.py）;交叉源=ai-martin-lau（4.1.10 SIP 开启验证过,双参数形态 x1 直缓冲+libc++ string [size@+8][ptr@+16]）。本机 attach 通道已实证（collector task_for_pid 7.8GB 可读+LLDB 四轮断点能设）。**红线冲突**：断点=瞬时进程干预（读寄存器即拆,不改行为）;且需主人 30 秒配合重登。**主人明示裁决前不动手**。

**已破开的结构（磁盘路战果,10-13 定性修正）**：
- `key_info.db`：单表 **36 行**（10-13 实测;每行=一次登录事件,key_info_md5 36 唯一,后续登录会追加）,user_name_md5=md5(wxid) 对拍 ✓（32/32 唯一=主人单账号）
- `key_info_data` = 180B protobuf 信封：field1(168B 载荷) + field2 varint 2024（版本） + field3 varint 时间戳（行间可变）
- field1 载荷=**固定模板+随机字段的登录凭证**（非整体加密体,方差分析判死离线路线）：`[0,17)` 常量头 `0a a8 01 00 0bb51739 05000001 00000000 00` → [17,31) 变 14B → **[30,67) 37B 常量（含 32B 跨库常量,非密钥）** → [67,171) 变 104B → 尾 field2/3 标记
- 解析+方差工具=tools/variance_keyinfo.py;信封解析见本档 §附录

**验证器（全部就绪，钥匙到手即用）**：`tools/verify3.py` = chatlog darwin/v4 协议（PBKDF2-SHA512 256000 派生 + XOR-0x3a macSalt + 2 迭代 macKey + 页 1 HMAC 比对），对 message_0.db 秒验。

## 机器密钥来源·嫌疑清单（攻坚靶点）

1. **MMKV tinfo（头号）**：`db_storage/MMKV/f2641*b00tinfo.mmkv` 多实例——设备信息（tinfo=terminal/device info）存储，机器密钥大概率派生自其中字段（设备 id/硬件 uuid 等）+ 固定盐 KDF。
2. 派生材料其他候选：IOPlatformUUID / MAC / wxid + 固定串。
3. Secure Enclave（若用则磁盘路死——但 wx 需跨设备迁移，倾向软件派生）。
4. 对照物：**wx 4.x Windows 版同结构**（key_info 生态 Windows 研究更多——`key_info_data` 结构可能同源，Windows 的解包研究可直接借鉴）。

## 四阶段路线

- [ ] **阶段1：MMKV tinfo 解析**（零密码可做）——MMKV 格式解析（腾讯开源格式：文件头+protobuf KV），抽出 tinfo 全字段。（passphrase 模型下预期调低：机器密钥在登录流由服务器侧参与,磁盘派生材料大概率不存在）
- [x] **阶段1.5：v7 已实跑终局——8428 候选全验零命中(10-13)**:S1/S1h/V1/C1 容器+锚邻域(459 裸+31 解引用)全覆盖;passphrase 不在这些形态或 4.1.15 又变。**预案语义 bug 修正:MAXVERIFY=0=零验证非不设限,用 999999**。v7 工具链保留——社区新情报到手即可按新模式重扫。collector5 四模式（S1 std::string 32B/S1h 64hex string/V1 vector/C1 CFData 内联,布局=layout_probe 本机实测）+ **A1 锚邻域（10-13 v7 新增,C 计划）**：锚串 USER_KEYINFO（macOS 同源词实证=key_info.db 唯一索引名 `LoginKeyInfoTable_USER_KEYINFO`）/com.Tencent.WCDB.Config.Cipher/WCDB.Config.Cipher/setCipherKey,UTF-8+UTF-16LE 双编码,仅 RW 区,锚实例 ±128B 窗内 8B 步进裸 32B+窗内 RW 指针解引用,共用 FNV 去重+内联验证器。**v7 自验（10-13 本会话实测）：`--selftest` 六召回全 PASS（S1/S1h/V1/C1/A1裸/A1指针）,-Wall 零警告,扫自身 5710MB;用法守卫 exit2/非root task_for_pid 干净拒绝**。实跑：主人在场 `sudo bash /tmp/wxkey-c/run5.sh`（基线≤10 分钟;HITS 0 且已验证==5000 → `sudo COLLECTOR5_MAXVERIFY=0 bash run5.sh` 不设限重跑）→ hit5.key → verify3.py 交叉验 → 桥 write_key_cache。
- [x] **阶段2：判死不再做**（方差分析+Windows 四组穷举全灭,见排除表末行）。
- [x] **阶段3：Windows 4.x 对照——结论已回填**（10-13）：WeChatMsg 全源码零 key_info 解析（Windows 4.x 唯一实现=wx_info_v4 内存扫+is_ok 验证,参数与我方 verify3 逐位一致）;Windows 侧也无解包算法（key_info_data 机器绑定离线不可还原） ⇒ 本档排除表+GATE 已吸收全部可搬情报。
- [ ] **阶段4：打穿收口**——passphrase/raw key → 派生全库 enc_key → keys.json（600）→ localdb query 真跑 → TMS 群首拉 → 情报流通电 → 10-12 档 AC7 终验。
- [ ] **B 线（若 GATE 批 LLDB 且 CCKeyDerivationPBKDF 在 4.1.15 零命中）**：ai-martin-lau 路线——wechat.dylib（357MB 已定位,WCDB/SQLCipher 串在案）重定位 4.1.15 派生函数特征码（其 4.1.10 参考偏移 0x4a5d840）,launch-and-wait 启动前就位断点;或 ghidra-headless 静态反推 PRAGMA key 装载点持有者类布局。

## 执行方式

- 持久战：闲时任务/后续会话 workflow 接力（读本档+tools 自洽）；每次推进在本档追加战况。
- 终扫（时序修正轮）结果出来后回填「已排除」表。
- 红线不变：只读、密钥材料只落数据根私有区、零微信进程干预（LLDB 路已废恰好回归纯只读）。

## 附录：信封解析（复跑即用）

```python
# 见 tools/ 同款：sqlite3 只读 key_info.db → pb_parse(key_info_data)
# field1 载荷头 14B 结构 + 加密体偏移 28(0x1C) 起取 152B
```

## 10-13 全天终局战报(第 1 攻坚日)

九路全排除(四hex/盐邻域/chatlog锚×时序/API钩/钥匙串/Win指针/v7六模式 8428 验)。**4.1.15 macOS 钥匙获取=当前社区前沿未破**(chatlog 停 4.1.2)。下一步候选:①社区新情报(等 chatlog/PyWxDump 系跟进 4.1.15)→v7 换模式即用 ②阶段1.5 深化(passphrase 若非容器形态=散存/加密态驻留→逆向微信二进制找 PBKDF2 调用点参数寄存器/栈) ③LLDB CCKeyDerivationPBKDF 符号断点(根因修正已入档;主人已口头允 LLDB,下会话可实施:重登微信触发派生时抓参数)。
