# 2026-10-15 离线三图验收工具切片

## 当前任务核对

用户要求选择能推进的未完成项直接做。本轮按当前任务原档核对：媒体档仍缺真实钥、三图验证、供钥与装机；uicreate 的创建层/流向/传导验证仍开放且涉及新的活进程授权；spawner AC 已勾完、处于 review，不重复攻击已判死的 spawn 补丁路线；v1.2 池含大量已消号内容，不能按状态 planning 将旧条目当成待实现需求。

规定的 `.trellis/scripts/open_task_board.py` 当前缺失（执行返回 Errno 2），所以未生成或冒充其十列表。按直接子目录 task.json 定位后定点核验上述 PRD。没有修改其他执行会话的指针或任务。

## 已交付

- research/verify_media_samples.py：独立离线 CLI，复用现有 load_keys/decrypt_dat/guess_ext；不附加、不写凭据、不装机、不生成明文图像文件。
- 通过条件：3..32 份不同 V2 密文，至少三份不同解密内容；魔数与解码格式一致，Pillow verify 后重开逐帧 load，所有样本都通过。单文件、像素总量和帧数设上限。
- 依赖 cryptography 进程内 AES，避免旧组件 openssl 兜底将钥放入子进程 argv。图像校验先读本机 Pillow Image/PngImagePlugin/ImageFile 实现，上游 https://github.com/python-pillow/Pillow；verify 不等于完整像素解码。
- 报告只含编号、验证状态、格式、尺寸、帧数、计数，不含钥、私有文件名、哈希、异常原文或图像内容。现有取钥函数的 stderr 不外放。
- research/test_verify_media_samples.py：18 项全合成测试，含 PNG/JPEG/GIF 真编解码、缺钥/错误钥、重复密文、不同密文同图、魔数假图、损坏图、非 V2、三好一坏、容器坏长度、文件/像素/动画帧上限、缺文件、输出零泄密与零明文落盘。

本轮只添加研究工具、测试与本任务资料，并为既有 playbook 增加验收入口；未改生产组件。GitNexus 对新研究符号未收录，不能将 UNKNOWN 当成已评低风险；研究工具没有既有生产调用者。未使用子代理，本轮范围小且文件集中，直接处理。

## fresh verification

命令：`.venv/bin/python -m pytest .trellis/tasks/10-15-media-key-hunt/research/test_verify_media_samples.py .trellis/tasks/10-15-media-key-hunt/research/test_media_window.py tests/scripts/test_wechat_bridge_mediadecrypt.py tests/wechat-bridge/test_media.py -q`

结果：**94 passed in 2.29s**。CLI `--help` 正常。

本机现有五份真实 dat 的只读预检：五个不同密文 SHA256、五份 V2 头布局均自洽。通过当前既有供钥通道执行新 CLI：**exit 2，status=blocked_missing_key，provided=5，required=3，verified=0，stderr 为空**。此结果是准确阻塞，绝非真实图片已解密。

复验微信：原进程存活、P_TRACED=false、无 LLDB/debugserver。旧授权未复用，未再附加。

执行探针时曾将虚拟环境 Python 符号链接 resolve 到基础解释器，导致该子进程无法加载依赖；已使用 sys.executable 保持虚拟环境重跑得到上述明确结果。运行命令应使用 `.venv/bin/python`，不要 resolve 该可执行文件链接。

## 未完成与继续条件

本切片已完成，媒体父任务仍在进行：真实 AES 钥、三份真图终验、供钥与装机均未完成。没有改写产品已完成口径；没有 git/worktree、归档或微信消息发送。下一步可直接用现有钥通道与该工具验真；任何新的活进程附加仍须独立明确授权，不能沿用本次一般继续指令。
