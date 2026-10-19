# 主线程复核：项目该做未做项与审计边界

复核时间：2026-10-15 21:24 +08:00。本文件为本轮最终结论；早先 audit-result-20261015.md 中的运行时快照与分类应结合下述更正阅读。

## 优先处理

| 顺序 | 未完成项 | 当前证据 | 下一步 |
|---|---|---|---|
| 1 | 微信真实媒体链收口 | 10-15-media-key-hunt/task-tiers.json：consumed_failed_no_retry；真实钥、三图验真、供钥和装机仍开放 | 保留原任务；无新单次目标/用途/最长时限授权不附加，取得真实钥后才验图 |
| 2 | 微信直发创建层 | 10-15-wechat-senddirect-uicreate 尚在途；spawn 补丁阴性已有记录 | 等正在执行的窗口收口，避免并行争用；任何新的活附加仍需授权 |
| 3 | Trellis 无 Git 建任务入口 | .trellis/scripts/common/task_store.py:473 无条件 run_git，显式 base branch 也先调用；项目禁止 AI 执行 Git | 已有新 planning 档 10-15-trellis-no-git-task-create，实施时禁止 Git 子进程并测试 |
| 4 | 标准开放任务看板 | fd 定点核验 .trellis/scripts 没有 open_task_board.py；用户要求的十列输出无法按指定入口生成 | 后续补齐脚本与规则一致性；当前不可伪造标准看板，也未恢复其他仓库版本 |
| 5 | 装机包真实冒烟 | 本轮仅无头、夹具 IPC、已有 desktop/ui 产物；未运行装机 package_smoke.py | 使用隔离数据根完成真实壳/sidecar验证；不以源码测试绿替代 |

## 可独立推进的已排期功能

10-15-feed-local-images 已生成 planning：Feed 详情仍只显示 image_files 路径（desktop/ui-src/src/screens/feed/feed-screen.tsx:1118），Tauri asset scope 仅覆盖微信缓存（desktop/src-tauri/tauri.conf.json:26）。管线确实把显式持久化图片写到数据库父目录 images/（src/myssia/pipeline.py:2081；vision/collect.py:167）。

这是原 v2.2 已明确推迟的功能，不是本轮发现的回归或违约交付：archive/2026-10/10-03-vision-v2/prd.md:75-76 已明确边界。新任务只是把该排期变成可执行计划；图片默认持久化仍为 false，不扩大读取范围。

_item_dict 目前只做字段与类型投影（desktop/entry.py:1577-1591），并非文件路径授权；实现图片预览时必须另做受限根路径判断与 Tauri scope 约束。GitNexus context 确认该投影由 _m_store_items 和 _m_feed_export 消费，不能为预览顺手放宽导出协议。

## 微信运行态前后证据

审计中曾只读观察到 lldb PID7518、debugserver PID7519 与微信 PID91292，微信 PPID7519；本轮未启动或接管这些进程。

21:24:25 重新读取 ps：微信 PID91292、PPID1、state S、flags 4044，Darwin P_TRACED(0x800) 为 false；上述调试器已不在。因此“当前仍在附加”的早期结论已经过时。本轮没有附加、detach 或终止微信。

## 新鲜验证与限制

- Python 定向检查：364 passed，范围为 tests/test_docs.py、tests/desktop/test_pyenv_resources.py、tests/desktop/test_desktop_sidecar_protocol.py、tests/wechat-bridge/test_component_stamp.py。
- Python 全库仅收集：6405 tests collected；未运行全量测试。
- 前端：TypeScript 检查通过；Vitest 47 文件、937 tests passed。本地 Node26.11.0，项目/CI为 Node22，不能称环境完全等价。
- 四项无头冒烟：browser-module、feed-card、logs-screen、tg-card，主线程分别复跑 exit0；使用合成夹具与现有 desktop/ui 构建产物，未重新构建源码、未测试真实账号。
- 远端近五次 CI success，只反映远端对应版本。
- 装机侧选定5个资源文件及146个 Python 源文件与本地一致；未比较全部前端/插件/二进制，不据此宣称整包完全同步。
- 最近三日日志的 failed/error 关键词多为 key_failed=0、parse_errors 等统计字段，不作为已确认故障，也不据此声称所有业务无错。

## 任务去重与文档更正

- 媒体取钥、直发创建层已有在途任务，不重复立档。
- spawner PRD 顶部 Requirements/AC 仍 TBD（:9、:13），但后文 :119-124 已有四项完成验收及阴性结论。准确问题是顶部摘要未与后文收敛，不能说它完全没有验收，更不能把后继直发功能算成该阶段漏做。未修改该任务状态或原文。
- 新增可执行 planning 档共2个（不含审计容器）：no-git 建任务（评分18：痛感4/判例5/独立5/风险4）；Feed图片预览（17：3/5/5/4）。均未 start、未归档。

## 审计执行偏差与未扫描面

派发了任务债、桌面、核心/插件三名只读探子，以减少跨目录读取；两名已返回。核心探子多次状态检查仍 running、无实质结果或报告，主线程已中断，不能声称完成了核心/插件所有文档与测试缺口的逐模块审计。主线程对该范围仅完成上述定向测试、收集、TODO检索与媒体链定点核验。

任务债探子超出只读契约修改了 desktop/scripts/{browser-module,feed-card,logs-screen,tg-card}-smoke.py，改为优先选择本机缓存 Chrome。主线程已亲读新增选择逻辑并复跑四项冒烟通过，但这些改动不是原计划中的只读审计产物；未继续修改、删除或自动回滚其他共享文件。缓存选择以字符串排序且为 macOS 默认路径，仍缺自定义 PLAYWRIGHT_BROWSERS_PATH 与跨平台/版本匹配验证；只能报告本机冒烟恢复，不能宣称通用浏览器选择问题已彻底解决。

本轮未执行 Git/worktree、未发外部消息、未重启应用、未恢复旧哨兵。审计与新增任务保持 planning，不宣称全项目无遗漏或已全部修复。
