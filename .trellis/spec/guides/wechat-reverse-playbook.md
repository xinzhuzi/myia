# 微信 macOS 逆向复跑手册(资产账 + 方法论)

> **目的**:下次继续逆向/反解微信 macOS(或任何同类大型混淆 Mach-O),读本档即可满血续作。两个产物目录(`~/Downloads/微信反编译/`、`~/Downloads/rea-wechat-decompile/`)在原则上**可再生**(全部重建配方在 §3),当前**一律不动**(主人令 2026-10-14:现在不要清理)。
>
> **配套读物**(本档不重复其内容,只给指针):
> - 执行协议(运行时明文猎捕 Step1-4 + run-sheet + 预算账):`.trellis/tasks/10-14-wechat-sendmsg-direct/design.md`(归档后移 `.trellis/tasks/archive/<月>/`)
> - 全谱系错题与防再犯(S1-S10 + 净产出统计):同任务 `research/错题集.md`
> - 工具用法(Phase 1 对接八步):`~/Downloads/微信反编译/sendmsg-勘察-1014/tools/README.md`(已镜像:同任务 `research/tools-mirror/`)
> - 逆向研究正本(AX 门/密钥路线图/管线纪实):`.trellis/tasks/archive/2026-10/10-13-wechat-dylib-reverse/` 等 20 档;`~/Downloads/微信反编译/研究文档/` 为其拷贝

---

## 1. 目标与地址模型(永不过时的锚)

- **对象**:`/Applications/WeChat.app/Contents/Resources/wechat.dylib`(fat 357MB,微信 4.1.15;**真身是 Resources/ 这份,`Frameworks/wechat.dylib` 是 84KB 壳**,勿搞错)。
- **地址换算(四合一)**:Ghidra 地址 == VA == arm64 薄片文件偏移 == fat 文件偏移 − `0xB010000`(arm64 切片在 fat 内 offset=184614912=0xB010000;薄片各段 vmaddr−fileoff≡0;Ghidra 工程基址 0)。文件后备段(字符串/`__objc_selrefs`/`__const`)全适用;纯运行期指针受 chained-fixups 影响,须以 Ghidra 解析值为准。
- **运行时换算**:进程内地址 = VA + slide;slide 取法 `lldb -p <PID> -b -o 'image list -o -f' -o 'detach' | rg wechat.dylib`。
- **微信升级/换包后**:全线地址作废——重抽薄片(§3.1)+ slide 字节级校验(design.md 前置 2 的两条命令:进程内 `x/16bx S+0xVA` 与薄片文件偏移字节比对)后重锚。

## 2. 资产地图

### 2.1 `~/Downloads/微信反编译/`(3.7G,逆向产物新家)

| 子项 | 内容 | 价值分级 |
|---|---|---|
| `README.md` | 资产家目录门牌(2026-10-14 已随本档刷新) | 随目录 |
| `ghidra-wxhunt/ghidra-wxui/` | **已全量分析**的 Ghidra 工程(2.1G,wechat_arm64.dylib,10-13 跑成,42-48min 级) | ⭐高:全量分析有病理卡死前科(§3.4),复用优先于重跑 |
| `ghidra-wxhunt/ghidra-tool/` | Ghidra 12.1.4 第二副本(mac 反编译器修复态未验,用前冒烟)+ 官方 zip 569MB | 可再生(GitHub 直下);优先用 `~/ghidra_12.1.4_PUBLIC` |
| `ghidra-wxhunt/wechat_arm64.dylib` | arm64 薄片 173MB 副本(与 fat cmp 一致,冻结防漂移) | 秒级可再生(§3.1) |
| `ghidra-wxhunt/wechat_arm64.dylib_symbols.prev.json` | 符号导出备份(2383 imports/2659 exports/6910 symbols) | 分钟级可再生(§3.5) |
| `sendmsg-勘察-1014/` | **发送直调勘察主工作区**(工具+证据+反编译产物,详见 §4/§5) | ⭐核心:工具已镜像进仓库,证据件唯一性较强 |
| `wxkey-密钥残留/` | 密钥攻坚残留(collector C 源码/二进制、lldb_keys.log、final_keys 等)。**含真实密钥材料** | 密钥线已破(LLDB 20/20 验真,10-13);sendmsg-direct 线收口后**建议主人整目录删**(处置权在主人) |
| `wxsend-e2e/` | 两张 Qt 无障碍截图(登录前/后) | 小,证据件 |
| `研究文档/` | ax-gate-hunt / crack-roadmap / ghidra-pipeline 三篇拷贝 | 正本在仓库 archive;拷贝可弃 |

### 2.2 `~/Downloads/rea-wechat-decompile/`(523M,REA 装机会话工作台)

| 子项 | 内容 | 价值分级 |
|---|---|---|
| `FINDINGS.md` | REA×微信实测总结(UI 驱动硬闸/反编译轴/卡点全景) | 结论已并入本档与任务档 |
| `wechat_arm64_thin.dylib` | 薄片(与 2.1 副本同源同字节,勿再复制第三份) | 秒级可再生 |
| `ghidra_proj/wxrea2` | **免分析(noanalysis)Ghidra 工程**,基址 0,与归档 FUN_ 命名地址互通,可继续定点查询 | 分钟级可再生(§3.3 配方即其诞生过程) |
| `ghidra_scripts/` | DecompileTargets{,2,3,4}.java 定点反编译模板 + DisableSlowAnalyzers.java + QuerySendPath.java | ⭐已镜像进仓库(§2.3) |
| `ghidra_out/` | 五函数反编译产物 + README(方法指纹:XOR 现场解码/RPC 桩调用形状/service_id 0xa13/0xa18/0xa1d/0xa2f/路线修正并载) | 分钟级可再生;指纹结论永载 |
| `run_decompile.sh` + `headless*.log`/`analyze_thin.*`/`observe_*.json`/`doctor.json` | REA 链脚本与全程留痕(长任务监控纪律样板) | 可弃(结论已提) |

### 2.3 仓库内(随 git 永生,目录删光也不丢)

- `.trellis/tasks/10-14-wechat-sendmsg-direct/` — design.md(执行协议)/ prd / implement / research/(错题集.md、rea-probe-1014.md、empirical-findings.md、hit2/hit3、cap.py v1、**tools-mirror/**(本次镜像))
- `.zcode/skills/ghidra-headless/scripts/ghidra_scripts/` — ⚠️ 该路径内层经符号链接指向仓库外,**不入 git**(Export*.java 六件原位在盘,盘存可用);**git 内正本镜像=任务 `research/tools-mirror/ghidra-scripts/`**(13 件全:DecompileTargets×4 / DisableSlowAnalyzers / QuerySendPath / Export×6 / SendMsgHunt,2026-10-14 镜像)
- `.trellis/tasks/archive/2026-10/` — 20 个微信相关档正本(10-13-wechat-dylib-reverse=地址模型/AX 门原始出处;10-13-wechat-key-crack=密钥;10-14-wechat-send-text=OCR 发送链;10-14-wechat-ax-gate-exp=AX 树浅定论等)

### 2.4 稳定安装(两目录之外的常驻件)

- `~/ghidra_12.1.4_PUBLIC` — **正牌 Ghidra**(arm64 反编译器已自炼在位;官方 zip 不含 mac 件,修复配方 §3.2)
- JDK:homebrew `openjdk@21`(`JAVA_HOME=/opt/homebrew/opt/openjdk@21`;旧档写过裸 `openjdk`,两者皆可)
- REA CLI 6.4.0 — 轻操作可用(`inspect-macho` 对 357MB fat 直读 OK);**`rea analyze` 对 165MB 薄片超其固定操作预算**(provider_timeout,无环境变量可调;仅 `REA_GHIDRA_STARTUP_TIMEOUT_MS` 存在且是启动预算)——大目标直接走 Ghidra headless 配方

## 3. 复跑配方(目录全删也能满血重建)

### 3.1 重抽薄片(微信升级后必做;源文件只读)

```bash
lipo -thin arm64 -output /tmp/wechat_arm64.dylib \
  /Applications/WeChat.app/Contents/Resources/wechat.dylib
```

### 3.2 Ghidra 就绪(mac 反编译器自炼,一次性)

官方 zip 只带 linux/win 原生件,`DecompInterface.openProgram=false` 报 `os/mac_arm_64/decompile does not exist`。修复(exit=0 在案):

```bash
cd ~/ghidra_12.1.4_PUBLIC/Ghidra/Features/Decompiler/src/decompile/cpp
make ghidra_opt -j8 ARCH_TYPE="-arch arm64" ADDITIONAL_FLAGS="-w"
cp ghidra_opt ../../../../../os/mac_arm_64/decompile   # 运行时目录是 Features/Decompiler/os/,不是 src/decompile/os/
```

新机从零:GitHub Releases 直下 ghidra_12.1.4 zip(543-569MB)解压后照上修。

### 3.3 免分析定向反编译(**默认武器,2 分钟出活**)

```bash
export JAVA_HOME=/opt/homebrew/opt/openjdk@21; export PATH="$JAVA_HOME/bin:$PATH"
GH=~/ghidra_12.1.4_PUBLIC
# 一次性建工程(免分析导入):
"$GH/support/analyzeHeadless" <proj_dir> wxrea2 -import <thin.dylib> -noanalysis
# 之后每次定点查询(改 DecompileTargets.java 里目标地址):
"$GH/support/analyzeHeadless" <proj_dir>/.. wxrea2 -process <thin文件名> -noanalysis \
  -scriptPath <脚本目录> -postScript DecompileTargets.java
```

- 脚本模板:git 内镜像 `.trellis/tasks/10-14-wechat-sendmsg-direct/research/tools-mirror/ghidra-scripts/DecompileTargets.java`(列表塞目标 VA,输出 `<name>_<va>.c`;任务归档后随档移 `archive/<月>/`,fd 定位;`.zcode/skills/...` 下的符号链接副本仅便利,不属 git)。
- **函数起点从运行时断点命中地址取**(准确零猜);静态启发式(序言扫描)会踩 thunk 区生成式 accessor 汤出空壳(错题 S5)。

### 3.4 全量分析(仅当需要全库函数表/交叉引用;**病理警告**)

- 10-13 跑成过一次(42-48min,6910 符号/389,833 函数);**10-14 两试皆废**:混淆段把 `DecompilerSwitchAnalyzer` 卡死 1.5h+ 空转,关三分析器后 2h+ 仍未出。
- 结论:**已有分析工程(`ghidra-wxhunt/ghidra-wxui`)优先复用勿轻弃**;真要重跑:先 `DisableSlowAnalyzers.java`(仓库已镜像),后台+exit 文件,杀进程用 `pkill -9 -f 'ghidra.GhidraClassLoader'`(**`pkill -f analyzeHeadless` 只杀启动壳,java 孤儿会互抢 CPU**),杀后必 `ps` 核零残留。

### 3.5 符号/函数导出(复用已分析工程,分钟级)

```bash
export GHIDRA_OUTPUT_DIR=<输出目录>
"$GH/support/analyzeHeadless" ~/Downloads/微信反编译/ghidra-wxhunt/ghidra-wxui wxui \
  -process wechat_arm64.dylib -noanalysis \
  -scriptPath <repo>/.trellis/tasks/10-14-wechat-sendmsg-direct/research/tools-mirror/ghidra-scripts \
  -postScript ExportSymbols.java -postScript ExportFunctions.java
```

产物:`*_symbols.json`(2.3MB)/`*_functions.json`(178MB,389,833 函数,含调用双方各截 50)。符号段上限 10000(实际 6910 未触顶)。

### 3.6 静态扫描与 LLDB 实弹(tools/ 六件套 + design.md run-sheet)

见 §4 工具速查;执行序列(空 lldb 检查→slide 字节校验→布防禁用态→arm 窗口→触发→hit 落盘→禁断点 detach→离线归因)照 design.md「Run-sheet」;预算账(总帽 10 条已用 6+1)照 design.md。

## 4. 工具链速查(`~/Downloads/微信反编译/sendmsg-勘察-1014/tools/`,干跑 23/23;镜像=任务 research/tools-mirror/)

| 工具 | 一句话用途 | 关键防呆 |
|---|---|---|
| `cap.py` v2.1 | LLDB 断点捕获枪:窗口开关+TTL 30s→线程名过滤(coroutine/mars::stn)→帧捕获→堆扫(4MB 分块+探针重叠+去重+双探针分级)→命中自禁自关自继续 | 判据分级:「嘻嘻」=唯一烧窗判据;「filehelper」只记 weak 不烧窗 |
| `fstarts.py` | 薄片 LC_FUNCTION_STARTS 反查 VA→所属函数(387,126 起点;**符号表已剥光,这是唯一函数边界源**) | — |
| `blscan.py` | BL 直调扫描(`--callers-of 0xVA` 可多次/`--all-index`);41M 指令级 | 0x5e1d050 有 27743 调用点=通用 helper,勿当发送专属 |
| `refscan3.py` | 页级 ADRP(+ADD/LDR)取址扫描 | **取址扫描一律页级**(精确匹配被寄存器折叠骗,错题 S3) |
| `attribute.py` | 归因链:hit 文件 → lr−slide=VA → fstarts 反查调用者 → blscan 上游 → BT 帧映射 | slide 缺失/越界/边界 None=rc≠0 干净退出绝不猜 |
| `test_offline.py` | 全离线干跑(假 lldb+真薄片+真样例 vmmap) | 改工具后必跑 |
| `hunt1_driver.py` + `hunt1_{live,smoke}.cmd` | Phase 1 实弹驱动(lldb 批式) | 冒烟先行 |
| Ghidra 侧 | DecompileTargets*.java / DisableSlowAnalyzers.java(仓库 skill 已镜像) | 见 §3.3/§3.4 |

堆扫区间源:**活体枚举优先**(`SBProcess.GetMemoryRegions()` 零参版,attach 态可用;launch 停 main 态返回空=按不可用回退),vmmap 快照仅回退(快照滞后=hit 时新增堆区漏扫)。

## 5. 已定结论快照(截至 2026-10-14 晚;全档细节在任务 design.md/错题集)

**架构定论(实证,不再翻案)**:UI 回车 → 逻辑层(未定位)→ 自研协程任务系统(task_service.cc)→ mars::stn 传输 → 网络。协程栈切换使 LLDB bt 攀爬只见单帧——**静态攀爬已被五条死路封死,运行时明文猎捕是唯一正门**。

**锚点函数表**(VA;薄片=4.1.15):

| VA | 身份 | 备注 |
|---|---|---|
| `0x490fb20` | mars 通用任务投递器 | **零 BL 调用者**(纯函数指针传入协程);传输边界锚,非发送入口 |
| `0x5e1d050` | RPC 桩 | 27743 调用点=通用 helper;断点选址之一(bp2=0x5e1d680) |
| `0x31ab38c` | ~~发送主流程~~ **NewSync 收信误标** | 指纹(XOR 解码/service_id 0xa13/0xa18/0xa1d/0xa2f)仍有锚定价值;成因=newsendmsg 与 newsync 同在 mars functionlist XML 配置表(0x986e82e)共址 |
| `0x48a9a38` | "SendMsgFtouser" 串谓词 | — |
| `0x88a8fb0` | CoSendAppMsgCgi(appmsg 路) | — |
| `0x70b32bc` | QCocoaAccessibility 激活门(`m_active`@this+8) | AX 线;门开树仍 6 节点=树浅系供给侧非门 |
| `0x490d4d0` | **Phase 1 首命中链 caller**(0x490d4d0-0x490da78) | 2026-10-14 20:42 实弹命中,上游=0x490fb20;**下一步=反编译此函数** |

**已证死路(勿重试)**:ObjC selector 路(全量 otool dump 无 send 族)/ BL 直调投递器(零调用点)/ newsendmsg 字符串 xref 当判据(functionlist 配置表,判据作废)/ thunk 区函数起点启发式 / 全量自动分析 / REA observe-native-ui 对微信硬闸(`NSRunningApplication.launchDate=nil`→capability_unavailable,微信 4.1.15 进程形态不给 launchDate,无 CLI/env 绕口)。

**密钥线(已破,独立于本线)**:LLDB 断点 CCKeyDerivationPBKDF 路 20/20 全库验真(10-13);重取 SOP 与数据根坑见记忆 wechat-key-broken-1013 与归档档。

## 6. 铁律摘录(错题集 S1-S10 精髓;全文=research/错题集.md)

1. **字符串锚定的因果归因必须断点实证**;传输配置表(functionlist)的邻居是「所有网络任务」不是「发送任务」。
2. **取址扫描一律页级匹配**;扫描器先拿「已知引用」做校准用例再信结果。
3. **函数起点从运行时断点命中地址取**;静态启发式仅下策且必须验证产出非空。
4. 大混淆二进制全量分析**必关慢分析器**;杀 Ghidra 杀 `ghidra.GhidraClassLoader` 且杀后核零残留。
5. REA 大目标直接走 headless 配方;**预算类错误先翻 dist 确认旋钮存在再重试**。
6. **共享资源消失先 fd 全盘找+查 memory,再动手恢复**——多会话环境的「消失」默认第一假设是搬迁不是删除。
7. **写执行协议涉及工具能力面,必检兄弟任务档 Notes+memory 已知坑**(S10);「某 API 不存在」类入档必须附原始报错/签名,转述带 API 全名。
8. 连续 3 次同域失败停手升维复盘(D2 元规则,与 send-text 错题集共守)。
9. brew 装新件后必冒烟 `node -e 1 && npx -v`(simdjson 连坐前科)。
10. 真发预算先报后发;失败即停,uncertain-never-retry,绝不带断点重试。

## 7. 目录处置预案(仅记录;**现在一律不动,处置权在主人**)

| 层 | 可弃性 | 依据 |
|---|---|---|
| 薄片两副本 / ghidra zip / 导出 JSON / decomp 产物 / 扫描结果 / ghidra_proj-wxrea2 | 原则上可再生 | §3 配方分钟-小时级全覆盖 |
| `ghidra-wxhunt/ghidra-wxui`(已分析工程) | 谨慎保留 | 重跑 48min 且有病理卡死风险(§3.4) |
| 勘察证据件(hit2/hit3/hunt/objc-dump/base-sendrun 差分/wxsend-e2e 截图) | 唯一性较强 | 运行时取证不可重放(依赖当日进程态);关键结论已文档化 |
| `wxkey-密钥残留/` | **含真实密钥材料** | 密钥线已破;sendmsg-direct 收口后建议主人整目录删(该家 README 已载同议) |
| 仓库镜像(tools-mirror + ghidra-scripts 13 件) | 永生 | 随 git;镜像时点 2026-10-14 晚(cap.py v2.1 / tools README v2.1 / Ghidra Java 脚本 13 件) |

> 镜像纪律:Downloads 侧 `tools/` 仍是**唯一演进源**(并行会话在途);镜像落后时以源为准重镜像,勿双向编辑。
