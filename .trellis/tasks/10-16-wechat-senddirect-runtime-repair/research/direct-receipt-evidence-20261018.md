# 直发回执方向与未知状态修复（2026-10-18）

## 已修复

1. `_poll_receipt` 原本收到 None 也设置 executed=True，全部未知及非法返回值最终被折叠成 False。现在只有显式 False 记录明确未见；True 立即结束；None/异常/其他值不伪装成一次成功查询。
2. `run_query` 的展示名替换会改写发送者及形如 `wxid:\n` 的正文前缀。新增默认关闭的内部 `receipt_mode`，由直发闭包显式启用，逐层传递 query_history→run_query→query_messages。普通查询/UI保持原行为，直发使用原文。
3. 原闭包仅比正文/时间，入站及方向未知消息也能使之返回 True。回执模式额外返回 outgoing，只有旧形态显式整数 isSender=1/0 有已证方向；异常值/缺列/仅real_sender_id的4.1.15形态均为None。直发只接受字面布尔True；方向未知保留None，不以发送者显示名、me字符串或目录前缀猜当前账号。
4. 完成分支的错误说明区分“未查到已确认的出站回执”和“回执不可用或证据不足”。两者仍保留pending，不回滚为可重发状态。

## 验证

- 轮询红测：3 failed / 6 passed，明确复现全None、异常夹杂None、非法值均被变为False；修复后9通过。
- 方向/原文红测：13 failed，包含同正文入站及方向未知被判True。后续增加混合候选及CLI pending/禁止重试集成测试，共20项通过。
- 最终微信桥完整回归：885 passed / 14 skipped，9.86秒。原始日志：receipt-evidence-final-regression-20261018.log。
- 修改的4个产品Python文件及4个测试文件Ruff全部通过。
- 合成SQLite验证显式isSender方向、异常值、Name2Id不证明自身份、展示改写隔离及默认查询形状不变。合成CLI确认方向未知/入站不报告成功，重复请求不会再次调用假发送器。
- 首次全量回归暴露旧测试替身不接受新参数/没有出站字段；保留首次失败日志，补齐替身的显式参数和出站证据后重新验证，未放松产品判定。旧协议测试仍仅用假LLDB/假数据库，不代表原生调用可用。

## 影响分析与限制

修改前对query_messages/run_query/query_history/_receipt_query_closure/_poll_receipt/execute_send及旧测试helper/method运行GitNexus impact，均LOW。源码直接核对补足索引未连接的模块属性调用；query_history及run_query的索引零调用结果不被当作实际零调用。上一轮新增测试尚未索引，impact返回UNKNOWN，依当前文件定点核对并完整回归。

本轮没有微信附加、进程检查、UI/账号/真实数据库操作、原生调用、发送、装机、Git或归档。产品拒绝门保持。

仍未解决：4.1.15当前账号身份的可信来源、新消息唯一性/同时间旧消息区分、服务端送达、完整业务字段保持、真实原生线程/协程与取消最终清理、完整适配、真正发送及部署。仅Name2Id不能补齐自身份，当前4.1.15匹配正文仍可能得到未知，这是正确保留证据缺口而非原生发送已完成。A7/原9项/L3保持开放；账号安全停止记录继续优先。
