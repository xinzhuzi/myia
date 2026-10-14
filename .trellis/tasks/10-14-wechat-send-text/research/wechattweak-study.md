# WeChatTweak 研究(10-14,主人令;链接者立场:只学方法论,零代码复制)

## 事实

- **sunnyyoung/WeChatTweak,13.8k⭐,AGPL-3.0**(判例:AGPL 只看不抄;方法论/格式思想可借鉴,代码零复制)。
- 结构极小:Swift CLI(Patcher/Config/Command/main)+ config.json(逐 build 对位表)。
- **机制**:按 build(CFBundleVersion)查表 → 对 fat binary 的对应 slice 在文件偏移处**覆写 arm64 指令字节**。patch 语义=「函数就地瘫痪」:目标函数开头写 `movz w0,#0; ret`(00008052C0035FD6)= 让函数恒返 false。族别:revoke(撤回处理)/multiInstance/更新检查五件套(startUpdater/checkForUpdates/enableAutoUpdate 等,全瘫=自动更新熔断)。
- **config 即知识库**:`version → identifier → {arch, addr, asm}`。合并线最高 build 34371(3.x 时代);**4.x 全部停在未合并 PR**:#1042/#1043(4.1.13/269602,2026-09)、#1039(4.1.10/268880,2026-07)——贡献者找得到 4.1.x 偏移(=dylib 仍可对位),维护停摆(最后 release 2.0.1=2025-12,push 2026-02)。

## 对我方三条线的启示

1. **SendMsgFtouser 线(待裁决)**:其 config 的「语义标识→逐 build 地址」格式正是我们 LLDB 配方的版本化形态(格式思想借鉴,AGPL 代码不抄);社区在 4.1.10/4.1.13 上持续找到偏移=偏移可维护性有生态佐证。我们与它不同路:它写文件瘫痪函数,我们 attach 调用函数,零改盘零注入。
2. **版本锚定线(修正)**:锚定目标不是 4.1.13——**mmui 主窗上线早于 4.1.13**(WeChat-MCP #8=2026-02 已找不到搜索框,mmui 约 2026 年初的 4.1.x 早期就位)。且 91831 本身就是 4.1.15 却有树(同版本死活分叉)→ 最优解释:**91831 是旧 dylib 时代启动的长命进程,微信热更只在盘上换 dylib,运行中进程不重载**(About 版本号读盘上包,所以显示 4.1.15)。锚定要锚「mmui 上线前」的版本(≈2026 年初之前),代价 8+ 个月版本滞后,需先考证确切版本号再决策。
3. **更新熔断手法**:WeChatTweak 靠瘫更新函数;我们锚定只需微信设置的关自动更新,零 patch。

## 开放问题

- 91831「同版本有树」的 loaded-dylib 热更理论未实证(进程已死无法核;若再现长命有树进程,LLDB `image list` 看 dylib 加载时间即可定案)。
- mmui 主窗确切上线版本号待考证(WeChat 发布日志/社区)。
