# A3 — 密钥途径探查(2026-10-11 实测;D4 裁决输入)

> 对象:`~/Library/Containers/com.tencent.xinWeChat/Data/Documents/xwechat_files/all_users/login/wxid_oc2y***[脱敏]/key_info.db`
> 边界:只读;只记 schema 与形状(计数/长度),**不导任何数据行、不读 BLOB 内容、密钥材料零落盘零入档**(红线 6)。

## 结论

**零内存密钥途径:候选物存在,判定 feasible(待端到端验证)。**

- `key_info.db` **是明文 SQLite**(非 sqlcipher 加密库,implement.md A3 预期的坏情况排除)——头 16 字节命中 `SQLite format 3\0`,`sqlite3 -readonly` 直接可读。
- 列名直指密钥材料在库:`LoginKeyInfoTable(key_md5, key_info_md5, key_info_data BLOB)`;实数据 34 行、单用户、`key_info_data` 恒 **180 字节**非空 BLOB——固定长度封装结构(疑似 protobuf/wrapped keyset,未解码——解码属内容接触,留 D4 裁决后的 E1 做)。
- **端到端未验证**:180 字节材料是否含(或可派生)db_storage 的 SQLCipher 32 字节 key,本轮未测。验证配方已备好且**纯离线、零微信进程接触**(见 §3 校验函数),E1 一步可闭合。
- 参考件 yancongya/wechat-mcp-macos 的 macOS 途径**不是**零内存路(进程内存扫描 + 重签名微信,双踩红线 1/3)——它的价值在**解密与校验配方**(离线可复用),不在密钥获取段。

## 1. key_info.db 实测证据

```bash
FILE=…/all_users/login/wxid_oc2y***[脱敏]/key_info.db
file "$FILE"
# SQLite 3.x database, last written using SQLite version 3027002, writer version 2,
# read version 2, file counter 8, database pages 6, cookie 0x2, schema 4, UTF-8 …
xxd -l 32 "$FILE"
# 00000000: 5351 4c69 7465 2066 6f72 6d61 7420 3300  SQLite format 3.   ← 明文 magic 命中
```

同目录 `-wal`(24752B)/`-shm`(32768B)在场,WAL 模式;三件 mtime 均 2026-10-08 18:17(与 prd「活跃写入」一致)。

**Schema 全录**(`sqlite3 -readonly "$FILE" .schema`,库只读未写):

```sql
CREATE TABLE LoginKeyInfoTable(
  user_name_md5 TEXT,
  key_md5 TEXT,
  key_info_md5 TEXT,
  key_info_data BLOB
);
CREATE UNIQUE INDEX LoginKeyInfoTable_USER_KEYINFO
  ON LoginKeyInfoTable(user_name_md5, key_info_md5);
```

**形状级行证据**(仅计数/长度,无任何值):

```sql
SELECT COUNT(*), COUNT(DISTINCT user_name_md5),
       MIN(length(key_info_data)), MAX(length(key_info_data)),
       SUM(key_info_data IS NULL) FROM LoginKeyInfoTable;
-- 34 | 1 | 180 | 180 | 0
```

解读(形状推断):单用户 34 条目,唯一索引 (user_name_md5, key_info_md5) → 34 个互异 key_info_md5,疑似按库/按版本分条的密钥信息表;`key_md5` 列名提示存有校验用摘要(语义为列名推断,未读值)。

## 2. 参考件机制:yancongya/wechat-mcp-macos(clone 于 /tmp,未入仓库)

「零 API 纯本地」的实态 = **内存扫描派**,macOS 密钥获取段源码证据:

| 位置(仓库内) | 机制 |
|---|---|
| `crypto/keys/scanner_macos.py:17-36` | 密钥获取 = 预编译 C 二进制 `crypto/keys/bin/find_all_keys_macos.arm64/x86_64`(来源 wechat-cli,Apache-2.0) |
| `scanner_macos.py:100-127` | 二进制跑在 db_storage 工作目录,`task_for_pid` 读微信进程内存,产出 `all_keys.json`(每库 `{enc_key, salt}`,600 权限) |
| `scanner_macos.py:39-97` | task_for_pid 被安全策略拦 → **对 /Applications/WeChat.app 重签名**(`codesign --force --sign -` + `get-task-allow` entitlement),要求重启微信 sudo 重跑 |
| `crypto/keys/common.py:19-28` | 候选 key 校验 `verify_enc_key`:取库 page1 前 16 字节 salt → `mac_salt = salt ^ 0x3A` → `pbkdf2_hmac("sha512", key, mac_salt, 2)` 得 mac_key → HMAC-SHA512 对 page1 数据段比对尾部 64 字节存档 HMAC——**纯离线,零进程接触** |
| `crypto/keys/common.py:113` | `cross_verify_keys`:候选 key × 各库 salt 交叉验证 |
| `crypto/decrypt.py:12-32` | 解密配方:SQLCipher 4 页格式,PAGE_SZ=4096,KEY_SZ=32,SALT_SZ=16,RESERVE=80(IV16+HMAC-SHA512 64),AES-256-CBC 逐页解密;`decrypt_wal`(:52-83)按 WAL salt 校验逐帧解密回填 |
| `init-keys.py` | 全程入口 docstring 自认「从微信进程内存中提取数据库加密密钥」 |

**grep 全仓 `key_info` 仅命中局部变量名,零处使用 key_info.db**——参考件未提供零内存途径,MYIA 的 key_info.db 发现是自有增量。

## 3. E1 验证配方(D4 裁决通过后执行,纯离线)

1. 解码 `key_info_data`(180B,先验结构猜测:protobuf/自定义封装;**此步才首次接触密钥内容,产物只落数据根私有区 600 权限**);
2. 得候选 32 字节 key(或先派生)→ 用 §2 `verify_enc_key` 同款 HMAC-SHA512 配方对 `db_storage/message/message_*.db` page1 离线校验;
3. 校验通过 → 零内存全链闭合(定位库→key_info.db 取材料→解密副本→只读查询,AC7 可达);
4. 校验失败 → 材料可能需设备绑定解包或已轮换 → 如实报 `key_unavailable`(design §6 exit 21),D4 升级主人裁决(内存搜索豁免与否)。

## 4. 风险与时效注记

- `key_info.db` 活跃写入 + WAL → 密钥信息可能随登录态轮换(G5 的「解密失败即重建取密钥」触发器同样适用于此途径)。
- 本轮未运行任何解密、未解码任何 BLOB、未触碰微信进程、零出网;clone 的参考件仅在 /tmp 只读源码。
