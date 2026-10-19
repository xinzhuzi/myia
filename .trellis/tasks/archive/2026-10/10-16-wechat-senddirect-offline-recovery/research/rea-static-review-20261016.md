# 用户指定目录的 REA 离线补核（2026-10-16）

## 本轮实际执行与证据

此前加载了 reverse-engineer-anything 技能，但函数级结论取自既有 Ghidra 输出与崩溃记录，不能称为本轮 REA 反编译。本轮实际使用已安装 REA 6.4.0 CLI 执行了下面的离线检查：

```text
/opt/homebrew/bin/rea inspect-macho /Users/zhengbingjin/Downloads/微信反编译/ghidra-wxhunt/wechat_arm64.dylib --format json --full-output
```

- 返回码 0；完整原始信封保存在 `rea-macho-retained-20261016.json`，294932 字节。
- REA Evidence ID：`ev_109315ba49cf6386a2abad6c8d1d5dfe6f3829412d39a6a7909ceafb98cebf65`。
- 实际 provider：`native-macos`；这是 macOS 原生静态检查，不是 Ghidra 函数反编译。
- REA 报告：Mach-O、arm64、64 位，UUID `0C2F01C0-C197-3286-901D-70E1D007A1C0`。

## 整体字节身份（本地 Python 文件取证，非额外 REA Evidence）

`rea-artifact-identity-20261016.json` 记录了完整文件及已安装 fat dylib 内 arm64 切片的范围哈希：

- 留存文件长度：173148768 字节。
- 已安装文件：`/Applications/WeChat.app/Contents/Resources/wechat.dylib`；应用 Info.plist 版本 4.1.15。
- 已安装 arm64 范围：偏移 184614912、长度 173148768。
- 两者完整 SHA-256 均为 `6a5bd0cbb39ad3092c15e9debda2db4969eedf1b58caad244d88033a996833a7`，与 REA subject digest 相同。

这是整个 arm64 切片的同一性核对，比此前七个 8 字节锚点更完整。它不自动证明已有 Ghidra 数据库的导入来源、分析设置或人工标注正确，也不证明运行时内存未被修改。

## 加密、符号及混淆结论的边界

REA 完整列出 97 条加载命令，exhaustive=true，没有 LC_ENCRYPTION_INFO/LC_ENCRYPTION_INFO_64。LC_DYSYMTAB 记录 nlocalsym=1、nextdefsym=2、nundefsym=2383；当前样本可用的常规本地/导出符号极少。

这些是当前样本的结构观察，不能据此宣布没有代码混淆，也没有旧版二进制比较可证明“升级后新增了混淆”。既有复核中确定的对象类型和参数错误，依然是本地适配失败的直接证据；未把调用 dylib 本身判为不可行。

## 函数分析与复用限制

已确认目录中存在 `ghidra-wxhunt/ghidra-wxui/wxui.gpr` 和对应 `.rep` 工程。已安装 REA 的 `decompile --help` 只公布二进制路径、procedure、snapshot、target-format、provider；其 GhidraLauncher.js 的 ghidraHeadlessArguments 固定创建私有 rea-project 并执行 -import，而没有公布复用已有 .gpr 的路径。

本轮没有再次启动此前已遇到预算限制的整库 REA/Ghidra 自动分析，也没有把现成工程伪装为 REA snapshot。本轮未新增函数级 REA Evidence；原函数结论仍明确归属既有 Ghidra 证据。后续定点调用约定分析可以复用原工程的只读处理能力，需保留工程身份核验和输出来源。

## 当前状态

此次仅新增任务 research 证据；未执行微信、附加调试器、触发发送、恢复哨兵或原工作流。send_direct 正文与 Task/CGI 的对应、真实直发终验仍未完成。
