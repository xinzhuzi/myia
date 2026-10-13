# E2E 独立复核:取钥器模块真数据链(2026-10-13)

验证员:真数据验证员(独立复核,非实现方)| 结论:**全链通过,verifiedCount = 20**

## 0. 环境与红线

- 跑法:仓内直跑(锚点手动等价)`MYIA_HOME=<沙箱> PYTHONPATH=plugins/wechat-bridge python3.14 -m wechat_bridge …`
  - **解释器 = python3.14.4**(非 .venv 3.12):桥 zstd 解码走 stdlib `compression.zstd`(PEP 784,3.14+;localdb_query.py:41-44),.venv 3.12.11 无此模块(实测 `ModuleNotFoundError`)。桥 requires-python >=3.11(pyproject.toml:10),3.14 合规;本机 3.14 实测 `zstd.compress/decompress` 往返 OK。
- sqlcipher 4.19.0(/opt/homebrew/bin/sqlcipher)在场。
- 沙箱:`/tmp/myia-e2e-kp-20261013/`,数据根 = `$SBX/home`(MYIA_HOME env,config.py:60/107-118 解析序)。
- **红线遵守(全程)**:微信 DB 只读(仅 open rb 读页头/枚举;解密走沙箱 staging 拷贝,localdb.py:1014-1015);零 sudo;零微信进程接触;密钥材料零入日志(只记指纹/长度,见 §1);真实数据根 `~/Library/Application Support/MYIA` 零写入(其 keys.json/decrypted 系实现方上午 11:24/11:47 所留——mtime 早于本次会话首写 13:47,本次写入全落沙箱);装机目录 `~/.myia/plugins/wechat-bridge` 只读路过;仓内 git 零改动。
- 观测件:取钥器 spawn 流捕获 = tee 包装(`/tmp/myia-e2e-kp-20261013/provider-tee.sh`,透传仓内 `plugins/wechat-bridge/examples/keyprovider_ref.py` 的 stdout 给桥、tee 一份落 `prov.ndjson.log`;协议零改动)。钥匙文件路径经 env `KEYPROVIDER_REF_KEYS` 传入(桥 spawn 无额外 argv,localdb.py:605-610 `[str(exe)]`,环境继承)。

## 1. 真材料实证(先证存在,只记指纹)

| 材料 | 实证 | 指纹(不记内容) |
|---|---|---|
| passphrase 缓存 | `~/.wcdb-key-tool/wechat-passphrase.json` 在场,size=86B,单键 `passphrase` | 64 hex 字符(=32B),sha256[:12]=`dcf9260b2a75` |
| 真 db_storage | `…/xwechat_files/wxid_oc2yhey1xkpw22_8253/db_storage`(locate_db_storage 解析) | page1 目标库 **20** 个(message_0 364MB … weclaw 8KB),盐已枚举 |

派生(verify3 协议,`$SBX/derive_keys.py`):`enc_key = PBKDF2-HMAC-SHA512(passphrase, salt, 256000, dklen=32)`(wcdb_key_tool_macos.py:472 同式)→ 桥端验真公式 localdb.py:189-206(= verify3.py:30-33 = wcdb_key_tool_macos.py:103-119,三方一致)。

- 正确 passphrase → `keys-ref.json`(600):**自验 20/20 页1 HMAC 通过**
- 错误 passphrase(hex 首字符翻转 1 字节)→ `keys-wrongph.json`(600):**自验 0/20 全拒**

## 2. 逐步证据

### 步骤 1 ✅ 沙箱 keys 缺失 + 未配 provider = 人话错误 + exit 21

```
MYIA_HOME=$SBX/home python3.14 -m wechat_bridge localdb query 50438708676@chatroom --since 3d
→ exit=21 {"code":"key_unavailable","message":"本地库密钥不可得:零内存途径(key_info.db)实测未闭合
  ——行数=36 候选=5226 离线HMAC校验=104520次 命中=0/20库;…;未配置外部取钥器,请在设置中指定可执行文件路径"}
```
法定文案在场(协议 §8,localdb.py:525);E1 负结论如实(先跑完才到 provider 分支判断,resolve_keys 顺序 localdb.py:797-867);沙箱无 keys.json(未污染)。

### 步骤 2 ✅ 配置 provider → 桥 spawn 参考取钥器 → NDJSON 流逐步记录

`localdb key-provider set $SBX/provider-tee.sh` → exit 0 configured;set 校验(绝对路径/存在/可执行,cli.py:315-337);沙箱 config.json 落 `key_provider_path`;`get` 三态查询 = configured。

主链 query(带 `KEYPROVIDER_REF_KEYS=$SBX/keys-ref.json`)桥 spawn 取钥器,**NDJSON 全流**(`prov.ndjson.log`):

```
progress: 读取钥匙文件: /tmp/myia-e2e-kp-20261013/keys-ref.json
progress: 枚举 20 个库,组出 20 把钥匙
result: success=True | keys=20 条(salt_hex→key_hex) | account_id=wxid_oc2yhey1xkpw22 | logs=[key_file=…, dbs_scanned=20, …]
```

行序合规(progress×2 → result 恰一条终态,协议 §4)。

### 步骤 3 ✅ 桥逐钥页 1 HMAC 验真 → 沙箱 keys.json 落地(600)

- query exit=0;`$SBX/home/wechat-localdb/keys.json` 落地:`-rw-------`(600,write_key_cache localdb.py:482-493;目录 700)。
- 形状:20 条,键=相对 db_storage 库路径,值全 64-hex;值集合 sha256[:12]=`7d3a66543162`。
- **verifiedCount = 20**:全量门槛(len(verified)==len(page_targets)==20,localdb.py:739)不满足即 exit 21——本步 exit 0 即 20/20 全验中。

### 步骤 4 ✅ localdb query 真消息 ≥1 条可读文本 + zstd 解码正确

主链载荷(step234.out):`messages=50`(text 49 + image 1),三域 message/session/contact 全 `ok`,副本 built=4(message_0/biz_message_0/session/contact,405MB)。

- **可读文本**:49 条 text,UTF-8 可读中文(样本头 8 字符呈 `wxid_…` 群聊引用前缀形态;全文按红线 6 不入档)。
- **zstd 解码正确(独立比对)**:`content_decode: zstd_available=True, zstd_decoded=31`。抽最近 5 条压缩行直查解密副本 `Msg_<md5(chat)>` 表:CT=4、BLOB 魔数 `28 b5 2f fd` 全在场 → **独立 `compression.zstd.decompress()` 解压文本与桥输出逐字一致 5/5**(解压 len=96/170/191/156/122,UTF-8 全可读)——真解码,非乱码/占位。
- **缓存命中通路(附加)**:二次查询 exit 0、`copy.kept=4`(副本复用)、取钥器零 spawn(prov.ndjson.log 未再生成)——keys.json 缓存即放行(resolve_keys ①,localdb.py:798-807)。

### 步骤 5 ✅ 负例 ×2:均人话错误 + 不污染 keys.json + exit 21

| 负例 | 构造 | 结果 |
|---|---|---|
| 5a provider 路径指不存在文件 | set 合法路径后 mv 走文件 + rm keys.json | exit 21「取钥器子进程启动失败(FileNotFoundError): …/provider-tee.sh」+ fix_hint(核对路径/可执行位);keys.json 未生成 |
| 5b provider 返回垃圾钥 | 自写协议合规 provider 恒返 `{"*":"0"×64}` | exit 21「验真未全量通过:给出 1 把(含 '*' 通配 1 把),覆盖在场库 20/20(盐不匹配 0 条),页1 HMAC 验真通过 0/20;未入缓存」;keys.json 未生成 |

如实计数、全量门槛、零缓存污染,与协议 §5/§7/§8 逐条吻合。

### 步骤 6 ✅ 换号语义:错误 passphrase(改动一字节)→ HMAC 全拒 + 「需重取」人话错误

tee wrapper + `KEYPROVIDER_REF_KEYS=$SBX/keys-wrongph.json`(20 把全量覆盖、协议形状完全合规,取钥器 success:true)→ 桥端 **HMAC 验真 0/20 全拒** → exit 21「…页1 HMAC 验真通过 0/20;未入缓存」+ fix_hint「不通过说明钥匙与库不匹配(登录态轮换后旧钥失效,**重取后重试**)」——「需重取」语义明示,无静默;keys.json 未生成。假钥在验真门全灭,进不了解密链(红线 6 同源纪律成立)。

## 3. 汇总(RealDataOutcome)

| # | 步 | ok | 关键证据 |
|---|---|---|---|
| 0 | 真材料实证 | ✅ | passphrase 缓存在场(64hex,指纹 dcf9260b2a75);db_storage 20 库盐枚举 |
| 0' | 钥匙派生自验 | ✅ | 正确 20/20;错误 0/20 |
| 1 | keys 缺失态 | ✅ | exit 21 + 法定文案 + E1 如实负结论 |
| 2 | spawn + NDJSON | ✅ | progress×2 + result(keys=20),行序合规 |
| 3 | HMAC 验真 + 缓存 | ✅ | **verifiedCount=20**;keys.json 20 条 600 |
| 4 | 真消息 + zstd | ✅ | 50 条(49 text);zstd_decoded=31;独立比对 5/5 一致;缓存命中 kept=4 |
| 5 | 负例 ×2 | ✅ | spawn 失败/垃圾钥均 exit 21 + 人话 + 零污染 |
| 6 | 换号语义 | ✅ | 0/20 全拒 + 「重取后重试」+ 零污染 |

沙箱留存:`/tmp/myia-e2e-kp-20261013/`(钥匙 600、NDJSON 流、各步 stdout/stderr;405MB 解密副本已清)。原文观测件:step1.out / prov.ndjson.log / step234.out / step4b.out / step5a.out / step5b.out / step6.out。
