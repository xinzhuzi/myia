# 本轮离线推进与边界（2026-10-21）

## 已核验并完成的切片

- 三条直发任务上下文：runtime-repair 的两处归档路径现已正确；spawner/uicreate 的空清单已由并行工作补入规范。本线程补入账号安全停止记录，确保旧实验预算/下一窗口建议不被当作当前授权。未改状态、勾选 A7 或归档。
- 当前研究 BodyStartGate 已由并行工作改为 thread-local shared identity token。本线程亲读当前实现并新增独立回归，保持所有生产驱动拒绝门。GitNexus 返回 Target not found / UNKNOWN；精确引用限于研究组件和自有夹具，不能据零索引结果宣称无影响。
- 新测试 test_newsendmsg_body_start_gate_thread_4115.cpp 让两个 gate 跨越创建线程退出，随后顺序启动 64 个替代线程。最终运行 64 个线程均复用旧编号；admit/cancel 的 128 个入口全部拒绝，注入取消调用为零。
- 主线程严格编译/运行 4 个自有夹具：新线程生命周期回归、原门控 11 场景、门控/operation 集成 4 场景、config 集成 8 场景/16 分支组合均通过。证据 body-gate-thread-20261021/green-v2/；新验证脚本 Ruff 通过。该汇编仅调用/读取自有对象。
- 先前桥回归 bridge-regression-20261020.log：885 passed / 14 skipped。
- 本轮图片解码 tests/scripts/test_wechat_bridge_mediadecrypt.py：35 passed；放大组件 feed-local-images.test.tsx：5 passed。日志位于图片任务 research/decoder-regression-20261020-current.log 和 enlargement-regression-20261020-current.log。未重复图片修复、换装或微信操作。

## 失败尝试如实保留

独立回归首次以 red 运行时，共享头文件已被并行修复，测试实际通过，故“应失败”的脚本断言失败；不是旧实现的复现证据。首次 green 的前三夹具通过，config 链接因本线程漏传两份自有汇编失败；green-v2 已补齐并全部通过。red/green 原输出保留，最终成功证据只认 green-v2，不把前述脚本失败当作产品缺陷。

## 仍未完成

真正直发仍缺原生调用上下文与生命周期/取消最终释放保证、完整可执行适配、真实发送及独立回执；现有回执对账还不能证明新消息唯一性、4.1.15 可信自身份或服务端送达。A7、原开放实施项及 L3 不关闭。

图片链已有其他会话的真实取图/装机记录，但本线程只验证上述离线测试，未完成用户真机点击放大验收。spawner/uicreate 的历史研究和失败配方不构成功能交付。

本轮没有附加调试器、执行微信代码、发送、读取微信 UI、操作登录、安装适配、运行 Git 或归档。账号安全停止约束继续生效。子代理已回收结果/停止扩查；空任务消息的实现代理未修改文件，独立验证由主线程完成。
