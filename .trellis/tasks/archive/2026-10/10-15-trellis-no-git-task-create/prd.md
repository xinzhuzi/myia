# Trellis: no-git 环境可创建 planning 任务

## Goal

在项目明确禁止 AI 执行 Git 命令时，`task.py create` 仍可创建完整、可验证的 planning 任务，不调用 Git。

## Evidence

`.trellis/scripts/common/task_store.py:473` 无条件执行 `run_git(["branch", "--show-current"], ...)`；随后 `:479` 还会解析默认分支。当前项目 AGENTS.md 的 no-git 铁律禁止该行为，导致任务生成技能无法使用标准创建入口。

## Requirements

- 为 `task.py create` 提供明确的 no-git 路径，保留已有 Git 可用路径的现有语义。
- no-git 路径必须写出可辨认的任务元数据，不能伪造分支或 PR 目标。
- 覆盖 Git 可用、Git 不可调用和显式 base branch 三种情形的自动化测试。
- create 不自动启动任务，不改已有任务；用户授权实施后可通过显式 start --no-git 启动本会话任务；不执行 Git 或归档。

## Acceptance Criteria

- [x] 在禁止 Git 子进程的测试中，`task.py create` 成功生成 planning 任务。
- [x] 生成任务明确表示 branch/base branch 未知或未设置，且不会伪造 `main`。
- [x] Git 可用时现有分支/默认分支行为通过模拟测试（未实际执行 Git）。
- [x] 任务创建后不改变任何 active-task 指针。

## Decision

已采用 null；显式 base_branch 原样保存。create/start --no-git 跳过外部钩子与身份的 worktree 回退。2026-10-16 定向测试含跨会话守卫共 18 项通过；使用标准入口创建并启动后续任务成功。待人审，不归档。
