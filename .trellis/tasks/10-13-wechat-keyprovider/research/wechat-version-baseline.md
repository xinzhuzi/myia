# 微信版本基线(4.1.15)——版本变了照着对照

> 用途:微信客户端每次自动更新后,先跑本文「版本漂移对照」的对照命令;
> 版本漂移时按「最先失效什么」清单逐项重验,全部绿了才继续用取钥链。
> 本档是任务档 research(含取钥链敏感面),对外只指路不展开——协议文档
> `docs/wechat-keyprovider.md` 的「版本基线」小节指向本档。

## 1. 基线表

| 项 | 基线值(实读/实测) | 证据锚 |
|---|---|---|
| CFBundleShortVersionString | **4.1.15** | 2026-10-13 17:09:50 +0800 实读 `defaults read /Applications/WeChat.app/Contents/Info.plist CFBundleShortVersionString` |
| CFBundleVersion(构建号) | **270135** | 同上时间实读 `… CFBundleVersion` |
| app 安装位 | `/Applications/WeChat.app`(壳 186KB,本体 `Contents/Frameworks/wechat.dylib`) | 桥代码锚 `plugins/wechat-bridge/wechat_bridge/system_checks.py:48`;dylib 形态见 `10-13-wechat-key-subsystem/research/ghidra-static-keyhunt.md` |
| DB 存储根路径形态 | `~/Library/Containers/com.tencent.xinWeChat/Data/Documents/xwechat_files/<wxid>_<设备后缀>/db_storage`(每账号一目录,多账号取 mtime 最新 = 当前登录近似) | 本机在场实证(2026-10-13 `ls -d` 命中,账号目录 `wxid_oc2yhey1xkpw22_8253`);代码锚 `system_checks.py:50-58`(WECHAT_FILES_ROOT)、`localdb.py:112-147`(locate_db_storage) |
| 在场库规模 | page1 目标库 **20 个**(message_0 364MB、fts、contact、session、sns、favorite、emoticon、head_image…),每库独立 salt | E2E 复核实测 `research/e2e-provider-verify.md` §1 |
| 桥侧密钥缓存 keys.json | `<数据根>/wechat-localdb/keys.json`(macOS 缺省数据根 = `~/Library/Application Support/MYIA`,非 `~/.myia`);600/目录 700;键 = 相对 db_storage 的库路径,值 = 64-hex enc_key;20 钥 | E2E 步骤 3(verifiedCount=20);README「落点与配置」 |
| passphrase 缓存 | `~/.wcdb-key-tool/wechat-passphrase.json`(600,单键 `passphrase`,64-hex = 32B);微信**换号/更新会失效**,重跑 lldb-shot 即再取 | 攻坚档终局战报(10-13-wechat-key-crack/research/crack-roadmap.md §🏁);E2E §1(指纹 dcf9260b2a75) |
| 派生协议参数 | `enc_key = PBKDF2-HMAC-SHA512(passphrase, salt_i, 256000 轮, dklen=32)`;salt = 库文件前 16 字节;验真 = 页 1 HMAC(SQLCipher 4 原始密钥语义),macSalt = salt 逐字节 XOR 0x3a,macKey 2 迭代 | verify3 协议(chatlog darwin/v4)= `10-13-wechat-key-crack/research/tools/verify3.py:30-33`;桥端同式 `localdb.py:189-206`;蓝本 `tools/wcdb_key_tool_macos.py:472/103-119`(三方一致,E2E §1) |
| 4.1.15 表形态 | 消息库 = `Msg_<md5(username)>` 分表,**无会话列**(会话 = 表名 md5,`Name2Id` 表在 message 库反查 rowid→user_name,`real_sender_id` 由此解析);内容列候选族含 `message_content`;压缩影子列 `WCDB_CT_message_content` 非 0 非空 = 该行 zstd 压缩(内容 BLOB 魔数 `28 b5 2f fd`) | B0 适配实装 `plugins/wechat-bridge/wechat_bridge/localdb_query.py:75/80/84`(列候选/CT 列/md5 前缀/魔数);实测 246/246 Msg_ 表全覆盖;E2E 步骤 4(zstd_decoded=31,独立比对 5/5) |
| zstd 解码链 | stdlib `compression.zstd`(PEP 784,Python 3.14+)→ pip `zstandard`(自管 3.12 主路,0.4.3 主依赖)→ 媒体占位+计数 | `localdb_query.py:42-48` 两级 import 链;装机态真跑 zstd_available=True/zstd_decoded=28(commit f51d5ac) |
| 本机 attach 实锚 | **本机未重签名即可 attach**:LLDB 断点 `CCKeyDerivationPBKDF -c '$x2==32'` 一击命中(10-13 11:22),全程零重签名——蓝本 prerequisite(重签名)在本机不成立,实证可跳;attach 通道另证:collector `task_for_pid` 7.8GB 可读 | 攻坚档 §🏁 终局战报;Ghidra 静态线补充锚:F3 sqlite3_key 等价物 FUN_058b8fc4、F4 口令驻留掩码(见 `10-13-wechat-key-subsystem/research/ghidra-static-keyhunt.md`) |

## 2. 版本漂移对照

### 2.1 对照命令(版本变了,先跑这个)

```bash
defaults read /Applications/WeChat.app/Contents/Info.plist CFBundleShortVersionString
# 基线值 = 4.1.15;输出不一致 = 版本已漂移,进入 2.2 清单重验
defaults read /Applications/WeChat.app/Contents/Info.plist CFBundleVersion
# 基线值 = 270135(小版本升级构建号先行漂移,同样按 2.2 重验)
```

### 2.2 版本变了最先失效什么(按序重验)

| 序 | 失效面 | 机理 | 重验动作 |
|---|---|---|---|
| 1 | **passphrase 可能失效**(换号/大版本更新后必失效) | passphrase 与登录态绑定;盐与派生参数也可能随版本变 | **重跑 lldb-shot SOP**:`bash .trellis/tasks/10-13-wechat-key-crack/research/tools/lldb-shot.sh`(osascript 提权弹密码框 → 断点就位 → 微信内退出登录重扫码 30 秒窗口 → 命中自动 detach)→ 派生验真 20/20 → keys.json 续期。若断点零命中 = 派生入口符号/寄存器形态变了,回攻坚档换路线(候选:Ghidra 静态线 F3 断点 `FUN_058b8fc4` 等价物) |
| 2 | **表结构可能漂移** | `Msg_<md5>` 分表/无会话列/`Name2Id` 反查/列名候选族都是 4.1.15 实测形状 | **B0 适配重验**:`localdb query <chat> --since 3d` 须回真消息且可读文本非空;若查询空/报列缺失 → 核 `localdb_query.py` 列签名自适应(_CONTENT_COLS/_CT_CONTENT_COLS/_MD5_TABLE_PREFIX)是否覆盖新形状 |
| 3 | **压缩形态可能变** | `WCDB_CT_message_content` 影子列与 zstd 魔数 `28 b5 2f fd` 是 4.1.15 实测;压缩标记列名/压缩算法都可能换 | **zstd 链重验**:query 载荷 `content_decode` 节须 `zstd_available=True` 且 `zstd_decoded` 与压缩行数相当、`zstd_module_missing`=0;压缩行若变占位 → 核影子列名与魔数是否漂移 |
| 4 | (附带)DB 路径形态 | 容器路径/账号目录命名是 4.x 布局,大版本可能搬 | `localdb query` 报 `db_not_found`(exit 20)时,核 `system_checks.py:50-58` WECHAT_FILES_ROOT 与实际布局 |
| 5 | (附带)attach 通道 | 微信收紧 hardened runtime / 系统更新改 TCG 语义 | lldb-shot 弹权限拒绝/断点设不上时,核「未重签名即可 attach」前提是否仍成立(基线表末行) |

### 2.3 重验通过的判据

- 派生验真 20/20 salts 全中(verify3 协议,页 1 HMAC);
- `localdb query` exit 0,真消息 ≥1 条可读文本,`content_decode` 无 `zstd_module_missing` 占位堆积;
- E2E 复核口径参照 `research/e2e-provider-verify.md`(全链 verifiedCount=20 为绿线)。

## 3. 维护纪律

- 本档基线值只在**实读后**更新(不许抄发布日志);更新时同步改 `docs/wechat-keyprovider.md`「版本基线」小节的当前验证版本。
- 对照命令输出与基线不一致而未重验 → 视为取钥链未知状态,先重验再用;不要拿旧钥硬试(桥端会 HMAC 全拒 exit 21,如实但排查噪音大)。
