# 2026-10-15 单次授权窗口结果

用户在本聊天明确确认微信媒体取钥、前台单次最长 30 秒。本次授权已经消费，禁止复用或修复后重试；固定消费标记 `/tmp/myia-wechat-media-window-20261015.consumed` 存在，不得清除以复跑。旧两份 launch.sh 仍在历史代码前 exit 78。

## 可核验结果

- 本次前台监督执行实际 3.906 秒，未触发 24 秒超时，未取消，LLDB exit 0。
- 监督器确认原 WeChat PID 91292 存活、非停止、P_TRACED=false、自己的 debugserver 子进程残留=0，cleanup_ok=true。
- 独立 ps 复验同一 PID 91292、flags=4004、state=S；未见 lldb/debugserver。
- 私有原始日志含 MEDIA_WINDOW_READY 与 Traceback；未保存 result.json、parameters.json，无可离线验证的钥材料。不知道断点命中数、匹配数及退出原因，不作零命中结论。
- 精确报错：media_window.py 原第 128 行 `signal.signal(signum, handler)`，`TypeError: signal handler must be signal.SIG_IGN, signal.SIG_DFL, or a callable object`。错误发生在 finally 的信号恢复阶段，阻断了随后的结果落盘；外部清理复验已通过。
- 原始日志只在消费标记所记录的私有临时目录，目录 0700、日志 0600，不拷入仓库。

## 修复与离线复验

LLDB 内嵌 Python 旧信号处理器可返回 None；一次性即退出的解释器恢复时将 None 映射为 SIG_DFL。修复后没有再附加微信。

新增 `no_attach_probe.py` 仅使用假 target/process，在真实 LLDB 解释器验证 continue 失败后的禁断点、Detach(False)、信号恢复、result.json 落盘；打印 NO_ATTACH_EMBEDDED_CLEANUP_AND_PERSISTENCE_OK。

监督器同时区分清理成功与采集成功，缺失采集元数据不再返回成功。

fresh command：`.venv/bin/python -m pytest .trellis/tasks/10-15-media-key-hunt/research/test_media_window.py tests/scripts/test_wechat_bridge_mediadecrypt.py tests/wechat-bridge/test_media.py -q` → **76 passed in 2.30s**（研究生命周期 16 + 原媒体合成/协议 60）。另有真实 LLDB 的无附加 TERM 探针：取消与 finally 均执行，exit 0，清理约 0.002 秒。

## 仍开放

真实媒体 AES 钥、至少三张 V2 真图终验、供钥与装机均未完成。没有写钥匙串、没有安装、没有发送微信消息；未运行 git/worktree、未归档。活进程路线需新的本次明确授权；现有单次授权不可沿用。非附加的离线分析不受该限制。
