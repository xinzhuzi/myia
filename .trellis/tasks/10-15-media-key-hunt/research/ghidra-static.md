# Research: 微信 4.1.15 V2 图片 AES 钥静态溯源(Ghidra 免附加)

- Query: wechat.dylib 4.1.15 V2 dat 的 16 字节 AES 钥从哪来(纯静态)
- Scope: internal(dylib 静态逆向 + 本机只读盘上核验)
- Date: 2026-10-15
- 引擎: Ghidra 12.1.4(`~/ghidra_12.1.4_PUBLIC`),复用已分析工程 `~/Downloads/微信反编译/ghidra-wxhunt/ghidra-wxui`
- 二进制: `~/Downloads/微信反编译/ghidra-wxhunt/wechat_arm64.dylib`(薄片;Ghidra 地址 == VA == 薄片文件偏移)
- 反编译产物: `/tmp/wxstatic_out/func_*.c`(20 件;工作稿,关键段已摘录在本档)
- 脚本: `/tmp/wxstatic_scripts/{DecompileStatic,RefsToTargets,RefsToData}.java`

## 一句话结论

**钥不在盘上明文,也不在 CommonCrypto;全链在 dylib 内自带 AES(AES-NI)。钥分两型:(A) 内置默认钥 = `md5("0")` 的 32 位 hex 字符串 `cfcd208495d565ef66e7dff9f98764da` 的前 16 个 ASCII 字节(keyIndex≤1 时用,本机样本实测不匹配→非本账户所用);(B) 每账户钥,由「密钥服务对象」(全局 `DAT_0a45df38`+0x68 shared_ptr)持有,内容是 key 对象内 +0x228 处一条与固定 32 字节掩码异或混淆的 32 字符串;该注册表整体持久化在加密 MMKV 的 `mmkv_key_last_user_account_registry` 键下。运行期取钥只需在 FUN_05a857d4 入口断一次,读 x0 指向的 16 字节即钥匙(坐标见 §6)。**

## 1. V2 dat 头解析(实证反编译,与样本逐字节吻合)

| 函数 | VA | 身份 |
|---|---|---|
| FUN_04b1f390 | `0x4b1f390` | **头读取器**:`strncmp(hdr,"\x07\x08V",3)` + `strncmp(hdr+4,"\x08\x07",2)`;byte[3] 经 FUN_04b56748 数字化为 version(∈{1,2} 才认);`u32@6`=aes_size,`u32@10`=xor_size,`byte@0xe`=flag;`aes_size'=(aes_size&~0xF)+0x10`(对齐+一整块);长度校验 `aes'+xor+0x1f<=filesize` 过则返回 15(头长),否则按 V1 回退(aes=min(len,0x400), xor=min(len-0x400,0x100000), 返回 0=无头) |
| FUN_04b1f92c | `0x4b1f92c` | 头写入器:懒初始化全局 `0xa49c6c4`="\x07\x08V2\x08\x07"(u32 0x32560807 + u16 0x0708),再 append 4+4+1 字节 → 15B 头 |
| FUN_04b1f5c0 | `0x4b1f5c0` | "GetDecryptInputOf"(日志 `secure_file_util.cc:0x7c`):读文件前 15B → FUN_04b1f390;失败走 mars 日志(`FUN_05e1d050`,level 4) |

魔数常量在 173MB 全文件中**唯一**出现于 `0x8ab4b88`(__const 字符串池,`"\x07\x08V2"` 独立 4 字节字面量;全文件 0x32560807/0x07085632 任何端序字节序均仅此一处;无 movz/movk 立即数构造)。注意:该字符串池属于 secure_file_util 编译单元,周边全是 4 字节字符串碎片("GetDecryptIn"/"AesD"/"MMEn"/"tOrD"/"ptBu"/"aes "/" xor"…)与 XOR 混淆 blob(§3)。取用经 SIMD ldr 重组(同 SnsUserTimelineBreakFlagV2 手法,样例 0x39fb6f8)。

## 2. 解密调用链(自顶向下,全实证)

```
FUN_04b2b9f8  0x4b2b9f8  任务构造/驱动层(2032B)
  └─ FUN_04b2aef4  0x4b2aef4  "ReadAesDecryptBuffer"(secure_file_util.cc:0x448/0x44f/0x454)
       │  读文件(offset@task+0x30, aes_size@task+0x10)
       ├─ FUN_04b1fb1c 0x4b1fb1c  ★取钥(见 §4)
       └─ FUN_046c2994 0x46c2994  "AesEcbDecrypt" 包装(某文件:0x22 行)
            └─ FUN_05a857d4 0x5a857d4  ★ECB 核心:
                 参数 (key,keylen,ct,ctlen,unpad_flag,&out,&outlen)
                 · ctlen%16==0 校验; keylen>0xf → 钳到 0x10(=只用前 16 字节)
                 · memcpy 16B → FUN_05e6f744(&key,0x80,&roundkeys)  密钥扩展(AES-128)
                 · 循环 FUN_05e6ffdc(ct_block,out_block,roundkeys,0)  块解密
                 · unpad: 末字节 n∈[1,16] 合法,否则返回 -3(=ReadAesDecryptBuffer
                   以"关 unpad 重试一次"的 -3 分支来源)
            块分发: FUN_05e6ffdc(36B) = cmp w3,#1 → b 0x5e6f984 / bne 0x5e6fcc0
            硬件轮: AES-NI 函数簇 0x5e702xx-0x5e703xx(aesd/aesmc;另一份 aese 簇 0x571axx)
```

- 解密失败重试逻辑:`ReadAesDecryptBuffer` 首调 `FUN_046c2994(..., padded@task+0x18, ...)`,返回 -3 且 padded≠0 时再调一次 unpad=0。
- **CommonCrypto 与本链无关**:全 dylib 仅 2 处调用 —— `CCCrypt@0x17a34`=crashinfo 加密(硬编码钥 `"WCDYCrshInfoKey!"`+IV `"xWeChatLdrIV2024"`,AES-128-CBC);`CCCryptorCreate@0x58bd1e8`=AES-256(keyLength 0x20)封装。二者皆非媒体路径。dylib 无 AES 软件查表(S-box 0 命中),AES 全走自带 AES-NI 实现。

## 3. 钥的三条供给路径(FUN_04b1fb1c,0x4b1fb1c)

入口参数:u32 keyIndex(来自任务结构 +0x20)。逻辑三支:

1. **keyIndex ≤ 1(默认钥)**:静态 `std::string@0xa49c658` ← `FUN_00255b9c(str, &DAT_0a49c6cc)`(纯 C 字符串拷贝)。`0xa49c6cc` 由 **FUN_0711a7a0**(0x711a7a0)懒初始化:
   ```c
   DAT_0a49c6cc[i] = DAT_08ab4d6b[i & 0xf] ^ DAT_08ab4d7b[i];  // i<0x21
   ```
   - XOR key(16B@0x8ab4d6b): `b2 bf 9b 55 33 f9 5d fb a2 59 73 93 e6 dd 9c b8`
   - 载荷(33B@0x8ab4d7b) 解出: **`cfcd208495d565ef66e7dff9f98764da\x00`** = `md5("0")` 的 hex。
   - 实际 AES-128 钥 = 该字符串**前 16 个 ASCII 字节** `"cfcd208495d565ef"`(0x5a857d4 把 >15 的 keylen 钳为 16)。
2. **keyIndex ≥ 2(每账户/每代钥)**:`FUN_0466aca8` → 服务对象(`DAT_0a45df38`@0xa45df38,0x308B,vtable@0x9e92400)虚方法 **+0x68 = FUN_0466a2fc**(0x466a2fc,拷贝 this+0x68 的 shared_ptr)→ `FUN_045547d8`(0x45547d8)把 key 对象转 std::string:
   - key 对象内 `+0x228` 是混淆钥串,`FUN_045547d8` 用**栈上硬编码 32 字节掩码**异或还原:
     `26 dd 85 a1 7d 22 6f e5 | 46 2c 9f 17 0e 37 81 46 | aa b4 4b d1 92 7a 76 14 | 2c 71 d3 89 6d c9 06 02`
     (u64 LE 常量:0xe56f227da185dd26, 0x4681370e179f2c46, 0x14767a92d14bb4aa, 0x0206c96d89d3712c)
   - key 对象另有 method[1] 返回对象 +0xe0 处的 std::string = 账户注册表序列化体。
3. **无服务对象且有缓存**:返回 `0xa51eec0` 处缓存 std::string(其 `__cxx_global_var_init`=FUN_04b2c2e8;运行期写入点未在静态引用中暴露,推测经指针间接写)。

**oracle 实测(本机样本)**:用默认钥 4 种形态(前 16 ASCII/后 16 ASCII/32ASCII 钳 16/hex 解码 16B)解 `/tmp/wximg/sample1_bd729394.dat` 头 0x400 字节,无一出图像魔数 → **本账户样本用的是路径 2 的每账户钥**(与「每用户钥」已知前提吻合)。

## 4. 持久化:MMKV「最后用户账户注册表」

FUN_0466a420(0x466a420)双向同步账户注册表:

- 读:MMKV 实例 = 服务对象 `+0x2a0` shared_ptr;`FUN_045321c0(&out, mmkv, "mmkv_key_last_user_account_registry", 0)` 取字节串。
- 写:vtable+0x70(=FUN_04670f64)为真时,`FUN_04532894(mmkv, key, &serialized)` 写回注册表(来源 = key 对象 method[1]()+0xe0 的 string)。
- 键名(运行期拼装):`"mmkv_key_last_user_account_registry"`(分片 "mmkv_key"/"_last_us"/"er_accou"/"nt_reg_c"/"nt"/"ry")。

**盘上核验(只读)**:
- 全容器 84 个 MMKV 存储(`find … -name '*.crc'`)grep `account_registry` 全部未命中 → 该 MMKV 实例为**加密 MMKV**(或键值整体先序列化混淆后再入 KV)。
- `db_storage/MMKV/storage_common` 全零(未用);`xwechat_files/wxid_oc2yhey1xkpw22_8253/config/` 与 `all_users/config/` 下各 MMKV(global_config/login_config/login_configv2 131072B/rs_config/newclientconfig/xlab/…)均无明文键名。
- `all_users/login/<wxid>/key_info.db`(SQLite LoginKeyInfoTable:user_name_md5/key_md5/key_info_md5/key_info_data BLOB)仍在原位(此前任务已核;BLOB 内容是否即注册表/钥未在本次重验,前结论「排空」指无可用明文钥)。

## 5. 钥源头定论

- **盘上无明文源**:钥匙最终形态(16B)仅存在于 (a) 运行期内存,与 (b) 加密 MMKV 内、与 32B 掩码异或混淆的 32 字符串(且 MMKV 实例本身还可能再套一层 MMKV crypt)。零附加路线下,盘上直接取钥需要:定位该 MMKV 实例文件 + 其 crypt key(通常由账户数据派生)+ 还原注册表序列化 + 拆掩码 —— 每层都要再逆向,性价比低于一次前台断点。
- **派生链(静态已定位)**:MMKV(registry) → key 对象(+0x228 掩码串) --32B 掩码 XOR--> 32 字符钥串 → 前 16 字节 = AES-128-ECB 钥。注册表的**首次生成**(登录时服务器下发 or 本地生成)本轮未追(超时收手);FUN_046710fc(0x46710fc)创建服务对象处是继续追的入口。

## 6. 将来前台单次会话的精确断点坐标(本档最大省时交付)

微信进程内地址 = VA + slide(slide 取法:`lldb -p <PID> -b -o 'image list -o -f' -o detach | rg wechat.dylib`;四合一地址模型见 playbook §1)。

| 断点 VA | 命中即得 |
|---|---|
| **`slide+0x5a857d4`**(FUN_05a857d4 入口,首荐) | **x0 = 钥指针,读 16 字节即钥匙本体**;x1=钥长(>15 会被钳 16)、x2=密文、x3=密文长、x4=unpad 标志。命中频率低(仅媒体解密路径),无 CCCrypt 风暴 |
| `slide+0x46c2994`(AesEcbDecrypt 包装) | x3 = std::string* 钥(size 字段在 +0x17 短串/数据指针在首 8 字节;32 字符串) |
| `slide+0x4b1fb1c`(取钥三支分发) | 返回值(s0) = 钥 std::string |
| `slide+0x466a420`(注册表 MMKV 读/写) | 观察 MMKV 键值与注册表序列化体 |
| `slide+0x466a2fc`(服务+0x68 getter) | x0 = key 对象(其 +0x228 = 掩码串) |
| 全局 `slide+0xa49c6cc` | 默认钥串 "cfcd208495d565ef66e7dff9f98764da"(懒初始化后常驻) |
| 全局 `slide+0xa51eec0` | 缓存钥 std::string(布局 24B;data 指针/短串判别看 +0x17 符号位) |

离线验钥:钥串若为 32 hex 字符 → 取前 16 字节作 AES-128-ECB 钥解 dat[15:15+0x400],出 JPEG/PNG/GIF/WebP 魔数即真(样本 aes_size=0x400,头 15B)。

## 7. 诚实边界(时限收手清单)

- 用时约 80 分钟。未完成:keyIndex(task+0x20)的赋值上游(FUN_04b2b9f8 只读了驱动段,构造段未细读);注册表序列化格式(protobuf?自定义?);MMKV 具体实例文件与 crypt key;0x8ab4b08 稀疏 0x07 表的语义(疑为 FUN_04b56748 的字符数字化表);`FUN_04b56748` 本体未反编译。
- 反编译产物在 /tmp/wxstatic_out(会话工作稿);本档为正本。Ghidra 引用/反编译查询用脚本是 DecompileStatic/RefsToTargets/RefsToData(/tmp/wxstatic_scripts),复跑配方同 playbook §3.3。
- 「MMKV 实例加密」是排除法结论(84 存储无明文键名 + 代码确证键名字符串),非直接解开验证。
