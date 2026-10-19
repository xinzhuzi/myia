# 本次单次窗口步骤

- [x] 新增 research/media_window.py：LLDB 异步单次控制、命中上限、finally 脱附；不改生产组件。
- [x] 新增 research/run_media_window.py：前台有界监督、一次消费标记、私有结果、ps 复验。
- [x] 新增 research/test_media_window.py：模拟正常/超时/热度/异常/取消/脱附失败；pytest 必须通过。
- [x] LLDB 无目标导入新模块，确认可导入；原微信未附加。
- [x] 复核 PID/调试占用，告知用户开图；执行一次窗口，总上限 30 秒。实际 3.906 秒，采集结果保存失败，见 research/window-result-20261015.md。
- [x] 确认微信无调试状态和本次调试器残留；失败不重试。授权已消费，修复后仅离线验证。
- [ ] 仅取得参数时离线三样本验真；成功后才走既有供钥与真图终验。未取得则如实记录，不装机。

新增研究函数尚不存在于项目调用图，无生产调用者；影响限定为显式运行的本次研究工具。未修改既有函数，不运行 git/worktree。当前仓库缺少 task-tiering-execution-guide.md，且 task.py 无 analyze 命令；不编造门禁命令，记录迁移边界。

补充验证：LLDB 内嵌 Python 的原生信号处理器返回 None，首轮模拟未覆盖，导致元数据未保存；已修复并新增 research/no_attach_probe.py，在真实 LLDB 解释器以假目标验证清理与落盘，无活进程附加。最终研究测试 16 项 + 原媒体测试 60 项，共 76 passed in 2.30s。缺失采集元数据不再被监督器认作取证成功。真钥、三样本真图、供钥、装机仍未通过，不归档。

## 2026-10-15 离线验收切片

- [x] 新增 research/verify_media_samples.py，复用 load_keys/decrypt_dat，至少三份独立 V2 图像才通过；只报安全元数据。
- [x] 新增合成真实可解码图片测试：正确钥三图、错误钥、缺钥、重复密文/明文、仅魔数假图、损坏图、非 V2；验证零私有输出。
- [x] CLI --help、完整媒体相关测试、本地五个真实 dat 的无附加只读预检；缺钥如实阻塞，不把工具完成写为真图验收完成。

本切片验证：新验收测试 18 项 + 既有 76 项，共 94 passed in 2.29s；现有五份真 dat 均为独立且布局自洽的 V2，CLI 实跑 exit 2 / blocked_missing_key / verified=0 / stderr 为空。完整记录见 research/offline-verifier-result-20261015.md。切片完成，父任务真实验收仍开放。
