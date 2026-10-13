# Ghidra 分析管线重建纪实(2026-10-14 凌晨)

## 结论:全套幸存,零重下、零重分析

ask 要求「幸存即复用」——实测 `/tmp` 下上一轮(2026-10-13)管线产物全部幸存,本轮仅做**迁移持久化 + 补导出**,未重下 543MB、未重跑 48 分钟分析。

## 证据链

| # | 事实 | 证据 |
|---|------|------|
| 1 | 管线脚本幸存 | `ls -la /tmp/ghidra-pipeline.sh` → 1050B,Oct 13 20:26 |
| 2 | 上轮管线 exit=0 | `cat /tmp/ghidra-pipeline.exit` → `exit=0` |
| 3 | 全量分析成功 | `/tmp/ghidra-pipeline.log:269` `REPORT: Analysis succeeded for file: file:///private/tmp/wechat_arm64.dylib` |
| 4 | 上轮符号导出成功 | 同 log `:273` `Exported 2383 imports, 2659 exports, 6910 symbols`(产物 2.3MB 幸存) |
| 5 | 薄片与当前本体逐字节一致 | `lipo -thin arm64 -output /tmp/verify_arm64.dylib /Applications/WeChat.app/Contents/Resources/wechat.dylib && cmp -s /tmp/verify_arm64.dylib /tmp/wechat_arm64.dylib` → `cmp_exit=0`(2026-10-14 实测,微信 4.1.15) |
| 6 | 无进程占用 | `pgrep -fl analyzeHeadless` → 空 |

日志中 ERROR 行(PNG 数据/thunk 创建/VarnodeContext 越界)为 173MB 大型 Mach-O 常见分析噪音,不影响 Analysis succeeded 结论。

## 持久化布局(~/ghidra-wxhunt,本轮自 /tmp 同卷 mv)

```
~/ghidra-wxhunt/
├── ghidra-12.1.4.zip                # 569MB 官方包(GitHub 直下,Oct 13 19:57)
├── ghidra-tool/ghidra_12.1.4_PUBLIC # 875MB 解压安装,analyzeHeadless 可用
├── ghidra-wxui/                     # 2.1GB 已分析项目(wxui.gpr + wxui.rep,含 wechat_arm64.dylib 全量分析)
├── wechat_arm64.dylib               # 173MB arm64 薄片(与微信 4.1.15 fat 档 cmp 一致,冻结防漂移)
├── wechat_arm64.dylib_symbols.prev.json  # 上轮导出(备份)
├── export.log / export.exit         # 本轮导出运行日志与退出码
```

## 复跑手册

### 重抽薄片(微信升级后;源文件只读)

```bash
lipo -thin arm64 -output ~/ghidra-wxhunt/wechat_arm64.new.dylib \
  /Applications/WeChat.app/Contents/Resources/wechat.dylib
```

### 重新导入+全量分析(约 42-48 分钟,后台+exit 文件)

```bash
export JAVA_HOME=/opt/homebrew/opt/openjdk; export PATH="$JAVA_HOME/bin:$PATH"
GH=~/ghidra-wxhunt/ghidra-tool/ghidra_12.1.4_PUBLIC
nohup bash -c "\"$GH/support/analyzeHeadless\" ~/ghidra-wxhunt/ghidra-wxui wxui \
  -import ~/ghidra-wxhunt/wechat_arm64.dylib \
  -scriptPath /Users/zhengbingjin/Project/Github/MYIA/.zcode/skills/ghidra-headless/scripts/ghidra_scripts \
  -postScript ExportSymbols.java -postScript ExportFunctions.java \
  > ~/ghidra-wxhunt/analyze.log 2>&1; echo exit=\$? > ~/ghidra-wxhunt/analyze.exit" &
```

### 仅导出(复用已分析项目,分钟级;本轮采用)

```bash
export JAVA_HOME=/opt/homebrew/opt/openjdk; export PATH="$JAVA_HOME/bin:$PATH"
export GHIDRA_OUTPUT_DIR=<输出目录,如本 research/>
~/ghidra-wxhunt/ghidra-tool/ghidra_12.1.4_PUBLIC/support/analyzeHeadless \
  ~/ghidra-wxhunt/ghidra-wxui wxui \
  -process wechat_arm64.dylib -noanalysis \
  -scriptPath /Users/zhengbingjin/Project/Github/MYIA/.zcode/skills/ghidra-headless/scripts/ghidra_scripts \
  -postScript ExportSymbols.java -postScript ExportFunctions.java
```

注意:ExportSymbols.java 符号段上限 10000(上轮实际 6910,未触顶);ExportFunctions.java 每 50 条截断。
Java 依赖:homebrew openjdk(`/opt/homebrew/opt/openjdk`,系统无 JDK)。

## 本轮导出结果(2026-10-14 01:09-01:12,exit=0)

- `wechat_arm64.dylib_symbols.json`(2.3MB):2383 imports / 2659 exports / 6910 symbols,jq 验证可解析
- `wechat_arm64.dylib_functions.json`(178MB):**389,833 个函数**,arch=AARCH64,含签名/参数/调用双方(各截 50),jq 验证可解析
- 运行日志:`~/ghidra-wxhunt/export.log`,退出码:`~/ghidra-wxhunt/export.exit`
