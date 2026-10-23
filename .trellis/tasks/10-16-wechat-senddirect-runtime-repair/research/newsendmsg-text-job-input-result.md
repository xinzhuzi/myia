# 文本作业转发字符串、分流门与捕获释放（2026-10-18）

本切片补齐实施67的所选文本作业用途与部分入口门。完整直发未完成，不提供产品接线。冻结ARM64 SHA256：`6a5bd0cbb39ad3092c15e9debda2db4969eedf1b58caad244d88033a996833a7`。

## 参数现在能区分什么

前一合同已证明外层`chatbot.WxFunctionCallInput` wire2进入builder x2；本次证明它在0x291fb94保存到x20，0x2921660～0x2921684复制到capture+0x10。0x292d868把该string复制到0x70字节body+0x18，同时分别移动completion/input/service的shared pair。

0x292ef9c正常成功与失败分支分别在0x292f5b8/0x292f15c读取该string。冻结密文按原始循环恢复的格式为：

- `call_id=%_ Send message success, chat_id=%_, message_type=%_`
- `call_id=%_ Send message failed, error=%_`

因此可以把**所选作业中观察到的用途**描述为日志call_id；这不是protobuf正式字段名、收件人或送达消息编号的证明。所选0x317ded4调用使用body+0x60服务与body+0x30/+0x38 input pair；0x3190538查询使用body+0x40 chat_id与作业返回的local_id/存储选择值。不能用wire2替代chat_id或原生收件人字段。

0x292fb44复制closure时复制该string并分别保留三个shared pair；0x292d940释放capture时先释放服务、chat_id和input，再释放该string，最后释放completion state。clone/destructor接收capture基址，即body+8；把body偏移直接用于capture会错8字节。

## 任意正文存在的高层入口条件

完整builder范围显示以下顺序：

1. 0x2ab6388接收服务与parsed首string，隐藏x8返回pair；nonnull后继续。其完整查找/变更语义仍未证明。
2. direct-content flag恰为1时复制正文；否则要求0x206bc返回bit0置位。
3. 0x2922400从正文搜索`<category>...</category>`子串；0x2921fc8只在抽取值有精确首尾`<![CDATA[`/`]]>`时去掉这一层。这不是完整XML解析。
4. 抽取值恰为`brand_account`时到0x292285c，恰为`emoticon`时到0x292385c。两条分流都在读取message_type并判断1之前。
5. 其余类型1分支构造input并复制正文/chat_id，还要求0x268f370返回非空服务后才创建和提交作业。

所以“JSON中message_type=1、content_xml填原文”不能作为任意正文原样发送的充分条件。含特殊category子串的正文会先走另一条入口路线；不能靠仅改版本JSON就声称普通文本完整支持，也不能把拒绝这些正文偷换成任意正文验收。后续完整适配必须解决这条分流与正文保持，或证明另一个完整普通文本入口合同。

## 完成与释放仍不可混同

body+8指向completion state。两条正常分支先用普通byte load/store读写state+0，再移动state+8的callback并清零，调用callback+8，随后释放临时持有。这里没有原子claim或本函数内的锁，不能以此证明并发一次性保障；现有回调/响应夹具不能证明原生调度串行。

成功日志先于0x292f828回调；本地record/server_id和该日志均不是独立送达回执。completion state释放也不能替代原生作业、请求、执行器闭包和末尾weak引用的完整排空。

## 核验与复现

- `Library/ai/export_wechat_text_job_20261018.py`：按独立compact-unwind边界导出builder、constructor、invoke共2987条连续LLVM指令；保留全部异常尾段。
- Ghidra旧invoke仅到0x292f93b；LLVM补出0x292f93c～0x292fac4。完整尾段字节通过，不声称已完成异常/别名数据流证明。
- `Library/ai/verify_wechat_text_job_input_20261018.py text-job-input-20261018-verification.json`：13份选择导出共3654指令、142关键位置、35独立分支目标、6个正常流寄存器来源、6个dyld槽及字符串恢复通过。
- 6处来源检查假定AAPCS64保留x19/x20；直接CFG把call视为返回，不加入异常边或证明内存别名，不能据此宣称真实线程安全。
- 两个新Python脚本Ruff通过。首次核验把clone callsite误抄为0x292ef24；读原始导出后改为0x292ef1c，最终核验通过，未改变目标字节或弱化断言。

证据：`newsendmsg-text-job-input-contract.json`、`text-job-input-20261018-verification.json`、`text-job-field2-20261018/`及`text-contract-pass391～393/`。新Ghidra运行均检查`REPORT SCRIPT ERROR`；进程退出0本身不算成功。

## 剩余范围

实施67仍开放：上游所有入口及gate helper语义、完整正文/收件人最终保持和线程要求未闭合。接下来优先回到55的状态0取消最终参数清理，再组合研究适配器。A7、11/18/20～24/55/67未完成；真实发送、独立回执、产品接线与部署均无证据。账号安全停止记录保持，未附加、未执行目标或操作微信。
