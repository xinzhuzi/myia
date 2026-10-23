# 启动门测试可重复性修正（2026-10-21）

## 缺陷及修正

研究夹具 test_newsendmsg_body_start_gate_4115.cpp 的场景11把 thread_id_reused 为真作为通过条件，并在stdout硬编码true。C++允许线程编号复用，但不保证后继线程必定复用；正确门控可能因此被测试误报失败。

修改只涉及测试及验证器，没有修改产品驱动或线程门控：
- 原测试输出实际布尔值，不把是否复用作为门控正确性的前提。
- 添加 --owner-alive 模式：以promise协调使原线程在替代线程运行期间仍存活，从而保证两个活线程编号不同；仍执行全部11场景并检查替代线程正文不执行、取消被拒绝。
- 既有静态验证器核验实际布尔类型，并将实际观察值写入证据；其余结果仍逐字段精确比较。
- 独立验证器新增green-v3专属证据目录及无复用场景，不覆盖既有red/green/green-v2。

GitNexus对研究C++ main返回Target not found / UNKNOWN；精确引用核验范围是研究测试及两份Library/ai验证器，不能把索引未覆盖当作无影响。

## 本轮命令及结果

1. python3 Library/ai/verify_wechat_body_gate_thread_20261021.py green-v3
   - 4夹具通过：64个替代线程/128次异线程入口拒绝；原门控11场景；operation集成4场景；config集成8场景/16分支组合。
   - 额外--owner-alive运行11场景通过，thread_id_reused=false；证据body-gate-thread-20261021/green-v3/owner-alive.json。
2. python3 Library/ai/verify_wechat_executor_start_gate_20261017.py executor-start-gate-20261021-portability
   - 7133冻结指令、47关键位置核验通过；原门控11场景实际观察复用、operation集成4场景通过。
   - 结果executor-start-gate-20261021-portability/verification.json；target_attached/target_executed/native_function_called/callable_for_send/send_verified均false。
3. uv run --no-sync ruff check Library/ai/verify_wechat_body_gate_thread_20261021.py Library/ai/verify_wechat_executor_start_gate_20261017.py
   - 通过。

## 本轮并行及审计边界

按用户并发指令派发的三个独立只读审计均返回“任务Payload为空”，未执行读取/修改。未重派或盲等，改由主线程核验上述测试与当前回执、图片源文件。子代理未提供本轮审计证据。

回执仍以正文、秒级ts及显式outgoing匹配；现有查询输出没有可用于发送前后比较的稳定记录身份，也没有发送请求与记录的关联。简单增大/缩小时间阈值不能补足同秒、同文历史消息的区分；不得将此层当成真正新消息/服务端送达证明。未做未经证明的baseline接口改动，产品拒绝门维持。

图片终验仍以用户真机接受为准。A7/原开放实施项/L3及整体目标未完成。没有微信操作、附加/注入/发送/登录、部署、Git或归档。
