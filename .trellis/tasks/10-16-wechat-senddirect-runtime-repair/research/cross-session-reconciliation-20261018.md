# 跨会话对账与遗留命令入口修复（2026-10-18）

用户要求复用其他AI成果并继续排查。本轮只读取ZCode会话数据库、本地源码与历史证据；没有操作微信进程、界面、登录或发送，没有Git、安装或归档。

## 复用结果

- ZCode“微信 send_direct 直发线”（sess_fb75a5f9-0ba3-4757-b89f-8739bb741c56），最后更新2026-10-16 01:43：报告三次崩溃后停止，未交付可发送适配。会话的建议不构成新的授权。
- ZCode“UI优化”（sess_8e9f0fb8-9cea-4227-bca3-57f595eb7f39），最后更新2026-10-18 18:41：后续主要完成Windows安装与UI交付，并非直发修复。其媒体真图成果有本地承接资料。
- `10-15-media-key-hunt/research/window5-result.md` 已记录供钥与三图通过；`10-16-feed-wx-images/prd.md` 已勾选实现、门禁和装机，用户真机看图仍未勾选。旧媒体看板“密钥未取得”与后续记录冲突，本轮只更正看板并注明历史证据，未重新取钥、解密或查看私人图片。
- 当前安装包Info.plist仍为4.1.15(270135)。整份fat dylib SHA256为5f5a81c4d8b000dec1c7203738fc4dba75ce752b55874fc1b6b5869f9dfb1027；它与研究中的ARM64薄片是不同容器，不能直接比较两个哈希来判断漂移。

## 本轮新增修复

此前五份`drive_wf*.sh`已封禁，但同目录八份`.cmd`的首条命令仍是`process attach`，直接执行`lldb -s`可绕开shell闸。修改范围仅限`truepath/{dis,pre,post,runcap,runcap2,runcap3,runcap4,runcap5}.cmd`：逐份添加前置`quit 78`与说明，完整原文保留在后面。修改前原件以`.original.txt`保存于`legacy-command-guard-20261018`，before.json记录原始SHA256。

这不意味着旧实现可以恢复：独立Python探针、Frida模板、额外CLI命令仍须遵守停止约束。真实LLDB无目标夹具证明，source内的quit可以阻止本文件后续命令，但LLDB仍可能执行另行传入的`-o`命令。不能把本修复宣称成系统级调试器隔离；附加选项也不受这个文件内闸控制。

## 当前验证

- `verify_wechat_legacy_commands_20261018.py`：八个实际命令文件均在首条quit返回78，未执行attach/import；原文后缀与备份SHA256相同。无目标夹具同时记录额外CLI命令仍能执行的限制。结果`legacy-command-guard-20261018/verification.json`。
- 原有`verify_legacy_guards.py`：五份shell入口语法通过、均exit78、外部命令0次；验证期间219个历史文件未变化。
- `uv run --no-sync python -m pytest -q tests/wechat-bridge/test_send_direct_passive.py`：15 passed。初次系统python在收集阶段因缺feedparser失败；改用项目既有uv环境通过，没有安装依赖。
- 新核验脚本Ruff通过。测试范围是遗留入口封禁和产品被动拒绝合同，不是原生发送验证。

## 保留开放

A7、原9个实施项和L3仍开放。完整字段保持、真实协程启动/外部取消协调与最终释放、完整适配、真实发送及独立回执均未补齐；本轮没有将旧注入配方、媒体真图或Windows装机成果冒充直发完成。账号停止记录继续优先，不申请新观察窗口。
