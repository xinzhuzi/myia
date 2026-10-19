# 现成适配与发送调用链补查（2026-10-16）

## 本次回答的问题

用户指出应先查已有成果，不能依赖逐次活体试错。本轮核对指定目录的社区源代码、上游版本与发布说明，并对既有 Ghidra 工程作只读定点查询；未附加、执行、操作或发送微信消息。

## 1. 已有适配是否可以直接使用

- 本地 `weixin-macos` 对应的上游已更名为 [yincongcyincong/wechat_chatter](https://github.com/yincongcyincong/wechat_chatter)。GitHub API 对旧名称的查询返回新名称。
- 本轮固定上游 main 为 `f222f37321f66d3a199cb3c7642f77f7504d85da`，提交时间 2026-09-28。不是根据本地 README 推断现状。
- 本地 `onebot/script.js` 的 71697 字节与该提交的上游文件完全一致。上游文件本轮副本为 `upstream-onebot-script-20261016.js`，SHA-256 `23ec6a69c08ad60d952add1cda8fc59480971f9b595b7a76e3a7b983c17f4356`。
- 本地 `wechat_version/4_1_12_53_mac.json` 与固定提交的上游文件完全一致，blob SHA `22f3044bb7463f76740c2d38f0862743dd0076c8`。其 structVer=2，Req2Buf、BLR、写缓冲区地址均为该版本专属。
- 当前版本目录列出 16 份 mac 版本表，最高为 4.1.12；18 份 release 记录未列出 4.1.15 适配，最新 release v0.0.18 说明增加 4.1.11.53。针对更名后仓库的 4.1.15 issue 查询 total_count=0。旧仓库名的 issue 查询曾返回 422，未将失败当作零结果。
- Firecrawl 的通用查询、精确项目+4.1.15 查询、字段名+4_1_15 查询，没有提供可核验的 4.1.15 适配；第三个查询明确返回 No results found。本结论仅覆盖这些来源，不宣称全网没有其他实现。

因此可以复用现有协议构建和设计资料，但不能将 4.1.12 寄存器/地址直接套在 4.1.15。旧独立 `frida/text.js` 的硬编码地址也不同于当前 onebot 版本表，应区分这些入口。

来源：

- [固定版本表](https://github.com/yincongcyincong/wechat_chatter/blob/f222f37321f66d3a199cb3c7642f77f7504d85da/wechat_version/4_1_12_53_mac.json)
- [固定 onebot 模板](https://github.com/yincongcyincong/wechat_chatter/blob/f222f37321f66d3a199cb3c7642f77f7504d85da/onebot/script.js#L636)
- [发布说明](https://github.com/yincongcyincong/wechat_chatter/releases/tag/v0.0.18)
- 原始 API、搜索结果分别保存在本目录 `upstream-*.json`。

## 2. 这次实际反编译了什么

按 ghidra-headless 技能，复用指定目录 `ghidra-wxhunt/ghidra-wxui/wxui.gpr`。运行采用 `-process wechat_arm64.dylib -noanalysis -readOnly`，没有重新导入或全库分析。脚本 `OfflineSendCallChain.java` 先校验工程输入 SHA-256 与留存文件相同，再导出指定函数的伪代码、指令和引用。运行退出 0，耗时 4.28 秒。

这是新运行的 Ghidra 证据，不冒称 REA 函数级 Evidence。此前的 REA inspect-macho Evidence 及完整 arm64 身份核对仍独立保留。

| VA | 本轮确认的用途与边界 | 新产物 |
| --- | --- | --- |
| 0x5971c24 | 分发器：尝试 0x5980a6c；未处理时调用 0x597d26c，x4 沿途转发 | offline-fn-5971c24.c/.asm |
| 0x5980a6c | 日志明确为 actiontask_mgr.cc / Req2Buf；从管理器取对象后复制其 protobuf，计算编码长度并写入输出缓冲区 | offline-fn-5980a6c.c/.asm |
| 0x5980d74 | x0 为管理器，w1 为查找键；锁住管理器+8，在+0x70容器查找，经 x8 返回两个槽并增加共享引用计数 | offline-fn-5980d74.c/.asm |
| 0x597d26c | 日志明确为 mmstn_manager.cc / MMReq2Buf；普通分支通过 mmcallback_ 虚表+0x50调用；另有独立分支到0x5cc1d14 | offline-fn-597d26c.c/.asm |
| 0x5ded378 | 读取输出对象+8、调用容量辅助函数，并按第三参更新+0x10；不是接受消息对象的函数 | offline-fn-5ded378.c/.asm |
| 0x56300b4 | 返回输出对象首指针加偏移；本调用点偏移为0 | offline-fn-56300b4.c/.asm |
| 0x5ab3f98 | 4字节 thunk；伪代码继续解析0x5ab3f9c，包含虚表+0x48/+0x58调用，不能当作memcpy | offline-fn-5ab3f98.c/.asm |

`offline-callchain-verification.json`：7份导出、435条指令、1740字节与留存文件全部相等；5条关键 BL 边直接从原始 ARM64 字节独立解码核对。覆盖范围是导出的指令；最后一个 thunk 的本轮字节覆盖仅4字节，不自动覆盖伪代码展开的全部目标函数。

伪代码中的参数、返回类型是推断值，不能逐个照抄成调用签名：例如 getter 的隐藏返回槽实际在 x8，主分支实际用 w0 返回是否处理，反编译器分别显示额外参数和 void。寄存器结论依据已核验指令。

## 3. 对旧适配的具体判断

1. `script-4115.js:802` 将 x4 当 Task 并写+0x60，但本轮指令证明 x4 被保存到 x21，随后作为输出对象传给0x5ded378/0x56300b4。不能通过把注释改成 Task 就建立类型关系，也不能照搬旧版中间断点的 x24。
2. `script-4115.js:680–691` 将 x29-0xb8 当四槽 AutoBuffer。实际主分支先将来自管理器的消息复制到这里，再对其执行 protobuf 长度和虚调用序列化；该错误此前构造器证据已确认，本轮主调用链再次吻合。
3. 此前局部命中的0x5981cd4是 action code/标志访问器。主分支日志包含 `ack.has_action_code() == sptask->GetActionCode()`，解释了为何这个虚调用不能当作文本正文序列化器。
4. 主分支与普通 MMReq2Buf 回调分支确实存在静态分流。不能再把在主分支看不到正文解释成“整个微信没有文本序列化路径”，也不能仅凭此次静态分流宣布任意文本必定只走普通分支。

上述类型与参数错误足以否定旧注入方案，不需要再次启动旧工作流来试错；仍没有“新增混淆造成失败”的版本比较证据。

## 4. 已答与仍缺的部分

- 已答：本地社区版本是否落后于上游、已查询来源是否提供4.1.15即用适配、旧参数与对象识别是否错误、主分支之外是否存在MMReq2Buf回调路径。
- 仍缺：普通/特殊分支的具体回调实现与版本对应关系；正文、Task和CGI的完整关联；所有权、析构与安全恢复的完整约束；真正的任意正文直发验收。
- 后续先继续静态追踪实际回调及已有协议构建器，不生成猜测地址的注入配方。若确需运行时取证，需另外明确单次目标、用途、时限及清理机制；本次指令不构成活附加授权。
- 本轮未修改生产桥、未装机、未发送、未恢复五份旧编排器；当前不能报告send_direct已修复。
