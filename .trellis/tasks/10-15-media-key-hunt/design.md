# 本次受控单次窗口设计（2026-10-15）

用户已在本聊天回复“确认”，批准微信媒体钥取证一次，前台最长 30 秒；失败或超时不重试。旧哨兵维持封禁。

新研究驱动仅附加当前已核验的 WeChat PID 一次。LLDB 采用异步事件、单线程状态控制，断 CCCrypt/CCCryptorCreate；只读匹配 AES-128-ECB 解密形态的 16 字节参数。最多 16 次断点命中；一秒内五次命中立即收工，最多八个不同参数。正常取证窗口 20 秒，给脱附与外部核验留出时间。

finally 先禁断点、SendAsyncInterrupt、有限等待停止、Detach(False)。外层前台监督从启动计时：24 秒未退出则 TERM，最多再等 2 秒，必要时结束自己的 LLDB 进程。完成后只读核查原微信仍存活、无 P_TRACED、无 debugger 子进程；不会杀死、重启或向微信写内存。

参数仅写独立 /tmp 私有目录内的 0600 文件，不进日志或仓库。驱动结束、脱附确认后，才用已有解密组件离线验证至少三个独立 V2 样本；无法验真即失败停止。不采用旧回调，不在暂停的微信中运行 openssl。

离线模拟验证正常结束、热度熔断、超时、读寄存器/内存异常与取消路径的脱附行为；它不代表已验证真实微信的成功取钥。若能力探针或模拟清理失败，不执行授权窗口。

## 2026-10-15 续做：独立离线三图验收

用户要求选择能推进的未完成项直接执行。本轮复用媒体任务，只实现离线验收工具，不消费或扩大任何活进程授权。工具新增在 research/，复用 scripts/wechat-bridge-mediadecrypt.py 的 load_keys/decrypt_dat/guess_ext；不改生产组件、不供钥、不装机。

输入为显式 dat 路径列表与可选 --key-file（沿用现有 JSON 格式，钥不进入 argv）。必须至少三个不同密文 SHA256，并且至少三份不同解密图像内容；仅 V2 可通过。Pillow 先 verify 再重新打开逐帧 load，格式须与魔数一致，所有提供样本均通过才返回 success=true。限制输入大小和图像像素/帧数，坏图/重复/钥错误均失败；缺钥返回 blocked_missing_key。钥或图片只留内存，stdout 只输出编号、状态、格式、尺寸、总数；不输出路径、哈希、异常文本或钥值，不落解密图片。

复用本仓既有 AES 解密路径，依赖本机 cryptography（禁止为验收回落到含钥 argv 的 openssl）；图像校验参考 Pillow 已安装源代码 Image.verify/PngImageFile.verify/ImageFile.verify（verify 不解码，必须另开后 load），上游 https://github.com/python-pillow/Pillow。独立 research 工具没有生产调用者；本轮不改既有生产符号。
