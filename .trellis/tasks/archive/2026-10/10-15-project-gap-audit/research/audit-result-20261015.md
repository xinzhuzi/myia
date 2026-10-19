# 2026-10-15 项目缺口审计结果

## 扫描范围与证据

- 活任务：`.trellis/tasks/` 当前有 backlog、媒体取钥、直发 spawner、直发 UI 创建层及本审计；媒体取钥和直发 UI 创建层均为在途，未另立重复任务。
- CI：GitHub Actions 最近五次 `CI` 均为 `success`（2026-10-15 读取）。
- 运行面：当天 JSONL 日志的采集、去重及朋友圈结构化采集均记录 `failures=0`/`parse_errors=0`；此前关键词命中来自成功行的 `failures=0`，不能当成报障。
- 代码欠项：`desktop/ui-src/src/screens/feed/feed-screen.tsx:1120` 的本地图显示明确排至 v2.2；`src/myssia/engines/fetch_base.py:212` 的住宅代理明确排至 v0.3，均不是本轮遗漏。
- 验证面：四个开发态 UI 冒烟脚本均因 Playwright 缺少默认 `chromium_headless_shell-1223` 而失败；本机 `chromium-1243` Chrome for Testing 存在，且以 `executable_path` 独立探针成功启动。
- 调试运行面：审计结束复查时，微信主进程 PID 91292 的父进程为 `debugserver` PID 7519，父调试器为 `lldb -b -s run34.cmd` PID 7518；微信 flags 为 `4844`，与此前无调试器时的 `4044` 不同。其外层命令来自另一个 ZCode 子代理的 `/tmp/wxsend3/r34` 运行窗口，并非本审计启动；这是当前 P1 风险，必须由该窗口结束并脱附，不能由本审计擅自终止。

## 已处理：开发态 UI 冒烟恢复

`desktop/scripts/browser-module-smoke.py`、`feed-card-smoke.py`、`logs-screen-smoke.py`、`tg-card-smoke.py` 现统一查找 Playwright 缓存中最新 Chrome for Testing，再作为 `executable_path` 启动。缓存不存在时仍让 Playwright 如实报原始缺失错误。

影响分析：四个 `main` 入口的 GitNexus 上游风险均为 `LOW`，无受影响执行流。

验证：`python3 -m py_compile` 通过；四个无头冒烟均 exit 0。它们使用 IPC 夹具和构建产物，只能证明开发态 UI 行为，不能替代 `/Applications` 装机包冒烟。

## 仍开放但不应擅自推进

1. `10-15-media-key-hunt`：离线解析与五份样本预检已通过，但没有真实 AES 密钥；下一次取钥必须取得新的、明确的微信前台单次限时附加授权，不能重挂旧哨兵。
2. `10-15-wechat-senddirect-uicreate`：需继续 UI 创建层动态定位，同样受活进程附加授权限制；当前不可自动执行。
3. 装机包真机冒烟：`desktop/ui-src/e2e/package_smoke.py` 会启动并关闭 `/Applications` 的应用，最长十分钟；本轮未运行，不能以四项开发态冒烟代替。

## 未新增任务的理由

除正在运行的 `run34` 活附加外，未发现新的 P1/P2 产品故障。v2.2 本地图展示与 v0.3 住宅代理均已有明确版本边界；媒体与直发问题已有在途任务。任务看板规定的 `.trellis/scripts/open_task_board.py` 在当前仓库缺失，故不能按该入口生成标准看板；此为 Trellis 工具链文档与实际不一致，待独立维护时处理。
