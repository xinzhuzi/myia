# Ghidra 静态猎钥线(2026-10-13)

主人令:本机无 IDA Pro,改用 Ghidra(开源、带反编译),相关技能装进本仓库,然后用静态逆向看能否定位微信密钥。

## 背景事实

- 微信 4.1.15(/Applications/WeChat.app),主程序是 186KB 的壳,本体在 `Contents/Frameworks/wechat.dylib`。
- 本机逆向工具链原为零(只有 Xcode 自带 objdump/otool/nm/strings);JDK 有 brew openjdk 23.0.2(keg-only)。
- Ghidra 最新 12.1.4(2026-09-21),zip 543 MB,解压约 1.4 GB。
- **brew 无 ghidra cask**(实测 exit 1 "No Cask with this name exists"),装机走 GitHub Releases 直下兜底:`https://github.com/NationalSecurityAgency/ghidra/releases/download/Ghidra_12.1.4_build/ghidra_12.1.4_PUBLIC_20260921.zip`。
- 技能选型(装进仓库 .zcode/skills/ 与 .agents/skills/,按既有模式):①trailofbits/skills-curated@ghidra-headless(Trail of Bits 官方策展,装前核许可证);②zhaoxuya520/reverse-skill@ghidra-reverse(MIT 已核)。

## 执行形态

动态工作流 `dwfrun-1bc1a49a-884e-43f8-bfa6-d10b55a4ed21`(脚本 .zcode/workflow-drafts/Ghidra-猎钥.dwf.ts):
装机监督员/技能装填员/侦察员三路并行 → 方案策划+拷问两轮 → 无头导入自动分析(工程落 ~/ghidra-wxhunt/)→ 猎钥(字符串→xref→反编译,AES S-box/SHA 常量/keychain API/HKDF-PBKDF2 形态)→ 发现拷问 → 逐条独立复核 → 看板+报告。
发现实时上 artifact board(待复核/已证实/未复现/存疑),负结果如实入档。

## 红线(沿任务既有威胁模型)

- 只读:不注入、不 hook、不重签微信;分析对象是磁盘上的二进制文件,不动 /Applications/WeChat.app。
- 微信数据库内容/用户数据不读不搬,只报路径形状。

## 状态

- [x] brew 装机尝试(失败,转直下兜底)
- [x] Ghidra 就绪(直下 543MB zip → ~/ghidra-wxhunt/tool,冒烟过)
- [x] 技能落地仓库(ghidra-headless + ghidra-reverse,.zcode/skills/ 与 .agents/skills/ 两处)
- [x] 侦察/分析(arm64 切片抽取,自动分析 48 分钟 exit 0)/猎钥/复核(2026-10-13 完结)

## 终局(9 发现,8 条独立复核成立,1 条核心语义被推翻)

报告全文=工作流 artifact「Ghidra 猎钥报告」;证据在 `~/ghidra-wxhunt/evidence/`(P0-P3 TSV+decomp/)。

**对拿钥直接可用的三件**:
- **F4(口令驻留掩码)**:FUN_058ba638 存口令后整块 XOR 固定 32B 掩码 `b8ec3829 1bd59c96 3f4654d8 f9d7437e 1acc81a6 cad6313c 7bd0f5e7 3238d4af`(存 __const,旧构建 0x8b6d000 可直读);FUN_058bd080 同掩码还原。**解释全部裸 32B 堆扫零命中的根因**——codec 持有的是掩码形态;新判据=任意 32B 堆块 B 与 B^mask 各验一次(掩码周期 i%32)。
- **F3(sqlite3_key 等价物)**:FUN_058b8fc4(db, idx, keyPtr, keyLen) 是全库钥单点(静态调用图内无旁路),arm64 x2/x3=口令指针/长度——重登/启动触发,LLDB 断此即捕获(与攻坚档「翻聊天不触发」结论互证)。
- **F9(地址映射)**:Ghidra VA=fat 偏移−0xB010000(arm64 切片);对拍必须用此换算。

**链路还原**:F1 PBKDF2 唯一直接调用链(FUN_058ba0cc,kCCPBKDF2)/F2 加密 provider 单例表(DAT_0a4e8c20,+0x30 槽=PBKDF2)/F5 pragma 通道(cipher_migrate 触发解掩码+attach;PRAGMA key 不存在)。
**负结果(实查为零)**:SecItem* 0(不用 keychain)/sqlite3_key 符号被剥/tinfo、MMKV 线关闭(F8 的 mmapID 拼造解读被复核推翻,实为 XLogger 日志格式串)/F6 修正:key_info 真正读档候选=FUN_02fd70cc/02fdf62c/0300ee0c(原 FUN_003e6844 是通用哈希容器 insert)。

**⚠️ 最大坑:被析副本≠现装构建**——分析用的是 10-09 拷贝(UUID 8ACF7A2F),现装是 10-12 自动更新(0C2F01C0,同 4.1.15 异 build),常量漂移 +0x4000(__text)/+0x40B0(__const)。掩码/S-box/K 表/PRAGMA 串已验证在现行构建全在——**LLDB 前必须按常量重锚,不重锚全错位 ~16KB**。

## 下一步(优先序)——2026-10-13 17:15 全部了结

1. ~~存量候选双形重验~~:无需——并行会话 11:22 已走 LLDB 路拿到 passphrase(TANGandXUE 蓝本四级链+一键件,断点 `CCKeyDerivationPBKDF $x2==32` 一击命中,20/20 派生验真;Ghidra F3「启动/重登触发」结论指导了触发时机)。
2. ~~LLDB 重锚~~:蓝本走符号断点(无漂移问题),已被 1 覆盖。
3. ~~派生默认值/盐来源~~:蓝本+verify3 协议参数(PBKDF2-SHA512 256000/salt=DB 页1)直接闭环,20 库全验。
4. 后续真线:B0 查询适配(0.4.2 `19c606b`)→ zstd 3.12 主路(0.4.3 `f51d5ac`)→ keyprovider 外置化(10-13-wechat-keyprovider,review)→ **通道切 localdb+排程回 `*/30 9-22`(17:13,*/2 密频遗留即 TCC 弹窗轰炸根因)→ run 148 终验:源 ok,0.16s 49 条,去重沉默**。微信线全闭环。
