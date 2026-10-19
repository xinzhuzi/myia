# 设计

看板直接读取 tasks 下 task.json；不递归 archive，不调用生命周期工具。采用现有 parent/children 关系；父任务被明确排除时，其开放孩子仍作为顶层展示。无效 JSON 保留诊断行。统一转义 Markdown 表格单元格。

新增可选 `meta.board` 合约：exclude=true 必须有 reason；phase/elapsed/remaining/next/notes 为人工维护的文本，不从 mtime 或 createdAt 推算。状态 review/completed/done 仍属于未归档待核验。无时长数据输出“未记录”。

装机验收复用实际 runtime manifest 和已安装资源入口，独立子进程设置隔离 HOME 数据变量，逐条 JSON-RPC 验证并超时清理仅自有子进程。不会调用旧 package_smoke 的全局杀进程前置步骤。验证器必须校验路径与版本事实，不隐式创建或下载运行时。
