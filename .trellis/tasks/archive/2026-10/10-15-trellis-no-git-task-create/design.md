# 设计

显式 `create --no-git` 跳过分支探测与外部生命周期钩子，并隐含 --no-start；branch 保持 null，base_branch 只接受显式值，否则 null。普通模式保持原行为。start 同样提供 --no-git，保留上下文门和本会话指针语义，跳过分支探测与外部钩子。

参考 CPython argparse 的 store_true 参数模式及项目已有 --no-start；不引新依赖。GitNexus 对这三个脚本符号返回 UNKNOWN，已通过定点调用检索确认边界，不将 UNKNOWN 当 LOW。

启动入口本身受 Git 禁令阻塞，因此本任务作为工具链引导修复先补参数，测试通过后立即通过标准 start --no-git 进入执行状态；不伪造已启动，不动其他会话指针。用户“那你推进解决”已批准本任务实施。
