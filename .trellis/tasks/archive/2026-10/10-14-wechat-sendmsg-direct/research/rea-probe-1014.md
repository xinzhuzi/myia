# ⚠️ 本档为过程快照(10-14 晚)。权威文档=同任务 design.md(执行协议)+research/错题集.md(错误全谱系)+implement.md(阶段门);冲突以权威档为准

# REA × 微信自动化实测(2026-10-14)

主人令:①缓存清理 ②REA 试微信自动化发消息 ③梳理卡点。本档为实测证据汇总,反编译产物同目录落盘。

## 一、REA 能否直接驱动微信 UI 发消息 → **不通(REA 侧硬闸,非微信侧)**

实测链:

1. `rea observe-native-ui /Applications/WeChat.app --pid 58622 --window-id 98454`(只读:截图+AX 树,零交互)→ `capability_unavailable / process-identity-unavailable`:"Selected application does not expose a launch time"。
2. 换可执行路径形态重试(`…/MacOS/WeChat`)→ 同错。
3. 源码定位(`bridge/native/ReaNativeUI.swift:55`):`NSRunningApplication(processIdentifier:).launchDate` 为 nil 即 fail-fast,属 PID 复用安全闸,无 CLI/env 绕口。
4. **swift 现场验证**(`/tmp/nsrun_probe.swift`):微信 58622 的 exeURL/bundleId(com.tencent.xinWeChat)/activationPolicy(0)/finishedLaunching 全正常,**唯独 launchDate=NIL**——微信 4.1.15 进程形态不给 AppKit launchDate,REA 的 UI 观察/驱动对微信全线硬挡。

结论:微信 UI 自动化(导航/写入/发送)主场仍是自研 wechat-bridge(AXAPI 直调,无 NSRunningApplication 闸;send_text 三源链已交付归档)。REA 的原生 UI 工具对「不给 launchDate 的进程」整体不可用,不只微信。

## 二、REA 反编译轴 → 通(引擎恢复后)

- `rea inspect-macho` 对 357MB 胖档直读通过(native-macos 引擎,SHA256 evidence 链完整,输出 `observe_*.json` 旁同目录)。
- 薄片已备:`wechat_arm64_thin.dylib`(165MB,lipo -thin arm64)。
- Ghidra 引擎事故与恢复:原 `~/ghidra-wxhunt/` 被并行会话清理(13:29 核验在位,13:5x 消失),已重下 12.1.4 到稳定位 `~/ghidra_12.1.4_PUBLIC`(exit 链留痕 `/tmp/ghidra-rea.exit`),zshrc 与 ZCode MCP 配置已同步改指。

## 三、卡点全景(问:卡在哪里?)

| 线 | 状态 | 卡点/结论 |
|---|---|---|
| send_text UI 链(AX 主+CGEvent/OCR 降级) | ✅ 已交付归档(10-14-wechat-send-text,AC 全勾) | 可用但依赖窗口/焦点;AX 深树不可得 |
| AX 门实验(10-14-wechat-ax-gate-exp) | ✅ 实验闭环 | 门开树仍 6 节点:**树浅=供给侧(accessibleRoot 疑 nil),非门**;深树方向只剩 Qt 侧注册/系统侧另途 |
| **SendMsgFtouser LLDB 直调(10-14-wechat-sendmsg-direct)** | ⏳ **当前主线卡点**:PRD 骨架 Requirements TBD,未动工 | 逆向资产已齐:主流程 FUN_031ab38c(3400B)/RPC 桩 FUN_05e1d050(service id 0xa13…0xa2f)/谓词 FUN_048a9a38/appmsg 路 CoSendAppMsgCgi@0x88a8fb0;VA=fat偏移-0xB010000(见 archive/2026-10/10-13-wechat-dylib-reverse) |
| 并行会话干扰 | ⚠️ 今日在途 | 另一会话在微信上做 LLDB attach(3 次换主,现主 58622@13:45);其收工清理误伤 ~/ghidra-wxhunt。协作约束:不 attach 不 kill,共用文件先 ls 核验 |

## 四、反编译终局(当日完成)→ 见 ghidra_out/README.md

- REA CLI `rea analyze` 对 165MB 薄片**超其固定操作预算**(provider_timeout,无环境变量可调)→ REA 反编译轴对超大目标受限;inspect-macho 等轻操作可用
- 正解配方(**2 分钟出活**):Ghidra headless `-import … -noanalysis` + 定点建函数反编译;**全量自动分析会被混淆段卡死(DecompilerSwitchAnalyzer 1.5h+ 空转,已实证,勿再走)**
- 四函数全拿到:主流程 0x31ab38c(570 行 C,XOR 解码/service id 0xa13…0xa2f 分支指纹全复现)+ RPC 桩 0x5e1d050 + 谓词 0x48a9a38 + CoSendAppMsgCgi 0x88a8fb0;RPC 桩调用形状:`(ret,3,msg,0xa3dd350,0xa3dec10,service_id,0,0)`
- 可复用工程:ghidra_proj/wxrea2(免分析态,基址 0)
- **路线修正补发**:前序会话判定 0x31ab38c 为 NewSync 误标,真发送=协程+mars::stn、方向 0x490fb20 邻域 → 已补反编译 `func_0x490fb20_490fb20.c`(134 行,内部调 0x5e1d978,与 RPC 桩 0x5e1d050 同区相邻,佐证修正路线)
