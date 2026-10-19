# 实施计划

1. 添加隔离 scratch repo 测试，所有外部子进程均禁止；验证 no-git 创建不调用 Git/钩子、不写会话指针，base_branch 不伪造。
2. 为 create/start 增加 --no-git，普通模式分支逻辑保留；使用 getattrs 保持直接调用兼容。
3. 回归现有 finish 跨会话守卫；通过后在本会话 start --no-git，补规范说明和验收证据。
4. 保持 review 待用户验收；不执行 Git、worktree、归档或删除。

验证：.venv/bin/python -m pytest tests/test_trellis_no_git.py tests/test_trellis_finish_guard.py -q
