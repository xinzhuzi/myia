# 作业与请求取消的组合验证（2026-10-17）

本轮复用已有ResearchOperation、NativeBody、NativeResponse、Completion与LaunchJob类型，新增一个自有串行调度夹具，把此前分开的作业层和请求层组合运行。**不是完整微信适配器，也不证明真实调度器身份/语义。** 没有加载微信、附加调试器、访问界面/账号或发送。

## 实际新增与验证

`test_newsendmsg_job_operation_4115.cpp` 的FixtureFlow在作业正文中创建原有ResearchOperation；通过已有LaunchJob函数指针类型传递非平凡function参数和shared返回句柄。Job/JobGroup/JobConfig全部为夹具自己的实现，不是还原出的微信对象布局。所有控制动作限定于夹具所属线程；这不证明同一线程约束就是微信的完整合同。

输入由现有Python build_request编码，含fixture-only目标、UTF-8正文与必填零值；C++读取本地字节，核对factory持有的正文副本逐字节一致。Body夹具只复制字节，不运行原生protobuf解析器，也不证明字段业务来源。

十个组合场景通过：

| 场景 | 核验 |
|---|---|
| 正常正文→factory→异步callback→响应复制 | 作业完成时请求仍pending；回调后深复制响应，sent仍false |
| 正文前重复取消 | 不构造请求、不调用factory；作业完成回调接收取消标志 |
| 请求入队后重复取消 | 只执行一次按task_id取消，队列请求释放 |
| 请求已被callback侧取走后取消 | 晚到回调保留cancelled终态，不报告发送 |
| 同条件下超时 | 晚到回调保留timed_out终态，不报告发送 |
| 正文启动时期限已过 | factory零调用，失败留存 |
| Body解析夹具拒绝 | factory零调用，Body销毁配平 |
| factory夹具在转交前抛错 | 只调用一次，不重试；不推断真实factory异常后的恢复能力 |
| 作业和Flow句柄均销毁后回调 | 请求保存的Completion继续持有OperationState；回调结束后引用释放 |
| 仅取消作业 | 请求保持pending且按task_id取消计数不变；补做请求层取消才释放 |

## 一次真实失败及修正

首次自有夹具断言 `job && !body && !finished` 失败：本机libc++对这些捕获的std::function移动后不保证源为空。已去掉该错误判据，改为检查目标句柄与最终实际引用/资源释放；源function照常由局部析构处理。不能把源句柄非空当作转交失败，或因此重复提交。

失败的源码、验证器、编译与执行记录保存在 `job-operation-integration-20261017/`；没有覆盖失败记录。修正后结果保存于 `job-operation-integration-20261017-v2/verification.json`：本机Apple ARM64 clang++以C++17及-Wall/-Wextra/-Werror编译成功，10场景、输入副本和对象计数检查通过，新Python验证器Ruff通过。验证报告保存所有相关源文件与二进制哈希。

## 仍未完成

这补上实施22的一部分组合夹具覆盖，**不勾完成22或A7**。实际group/config/线程、原生两层取消派发、末尾weak引用排空和模块卸载屏障仍未证明；夹具静态函数在整个可执行文件寿命中有效，不能证明动态卸载安全。响应示例不是独立送达回执，完整业务字段路线及原生适配器仍缺。账号安全停止约束保持，未改产品、真实版本JSON或安装件。
