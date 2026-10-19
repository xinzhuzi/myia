# 2026-10-16 实施验收（待人审）

## 已交付

- 标准十列看板 `.trellis/scripts/open_task_board.py`；只读，统计池显式排除，坏 JSON/未归档记录保留，子任务不额外计数，缺失耗时不猜测。
- 安装件验证器 `desktop/ui-src/e2e/package_managed_smoke.py`；真实已存在解释器，安装件 PYTHONPATH，隔离 MYIA_HOME/HOME，禁止 Telegram 启动宿主，stdin EOF 收尾。检查版本/锁指纹、安装件来源、四个真实只读 RPC、中文编辑备份回读、路径拒绝。失败与超时非零。
- 原 `package_smoke.py` 自管架构提前转交新验证器，不再走旧 GUI 清场和关键路径 SKIP。

## 实跑

`python-tests.log/exit`：64 passed，覆盖 no-git、跨会话守卫、任务看板、managed 验证器、资源清单与 asset scope。

`package-entry.log/exit`：新默认入口 exit0，仅代表明确列出的安装件 RPC 范围。`managed-installed-result.json` 为换装后的真实结果。

`python3 .trellis/scripts/open_task_board.py` 可直接运行；脚本本身不更改任务状态。

## 限制与过程偏差

没有运行 Python 全库测试、系统 WebView、真实 IME、采集/推送或微信链。未运行已禁用哨兵，也没有本轮新附加。

本会话早期 no-git 普通模式测试曾因身份文件缺失，间接触发临时测试目录内的只读 Git/worktree 探测；不符合项目禁令。随后测试统一禁止所有外部子进程，并修复 no-git 身份回退。当前全部相关测试在禁止外部子进程的条件下通过；不能把最后的通过结果描述成早期从未发生此偏差。

未使用子代理：项目指定降级模型当前不可用，按项目兜底由主线程实施与验证。不执行 Git 提交、归档、删除旧包或修改在途研究脚本。
