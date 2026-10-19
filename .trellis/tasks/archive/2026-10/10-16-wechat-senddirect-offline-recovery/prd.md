# 微信直发线离线接续与旧入口封禁

## Goal

复核 zcode 直发事故，封禁遗留后台编排入口，固化静态类型证据与后续验收门；不附加微信、不发送消息

## Requirements

- 沿用用户既有明确要求：禁后台附加、禁循环重挂、每次活附加须另获授权；本切片只修遗留入口并离线取证。
- 仅给已停止工作流的 drive_wf4.sh / drive_wf5.sh 添加与前代一致的 exit 78 闸，完整保留历史实现。
- 核对 zcode 会话、取消状态、静态反汇编、崩溃报告和已安装微信字节；区分观察、推断和未知。
- 不恢复工作流、不抢焦点、不发消息、不启停微信、不附加、不提交、不归档、不打包未经验证的适配。

## Acceptance Criteria

- [x] 两份入口拒绝执行；假命令探针确认未启动调试器、桥或进程操作，原实验产物哈希不变。
- [x] 静态证据与本机 4.1.15 arm64 指令字节吻合，关键原件有持久副本与 SHA256。
- [x] 记录对象类型错配、x21=1 崩溃现场、清理与授权失效；不再断言第三崩与调试无关。
- [x] 后续方案先补齐类型/调用约定与真实消息关联，单次窗口另授权，未经成功验收禁止接入和装机。

## Notes

- Keep `prd.md` focused on requirements, constraints, and acceptance criteria.
- Lightweight tasks can remain PRD-only.
- For complex tasks, add `design.md` for technical design and `implement.md` for execution planning before `task.py start`.
